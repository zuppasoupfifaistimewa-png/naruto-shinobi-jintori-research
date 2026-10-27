// ExportRngCallContext.java
// Locally disassemble narrow instruction windows at statically identified
// DATA.BIN callsite candidates. No whole-program analysis or execution.
import ghidra.app.cmd.disassemble.DisassembleCommand;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSet;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.mem.MemoryAccessException;
import ghidra.program.model.mem.MemoryBlock;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class ExportRngCallContext extends GhidraScript {
    private PrintWriter out;
    private void line(String s) { out.println(s); }

    private int readWord(Address address) throws MemoryAccessException {
        return currentProgram.getMemory().getInt(address);
    }

    private String wordText(Address address) {
        try { return String.format("0x%08X", readWord(address)); }
        catch (MemoryAccessException e) { return "UNREADABLE"; }
    }

    private String bytesText(Address address) {
        byte[] bytes = new byte[4];
        try {
            currentProgram.getMemory().getBytes(address, bytes);
            return String.format("%02X %02X %02X %02X",
                bytes[0] & 0xFF, bytes[1] & 0xFF, bytes[2] & 0xFF, bytes[3] & 0xFF);
        } catch (MemoryAccessException e) {
            return "UNREADABLE";
        }
    }

    private String instructionRecord(Instruction instruction) {
        Address address = instruction.getAddress();
        return address + "\traw_word=" + wordText(address)
            + "\traw_bytes=" + bytesText(address) + "\t" + instruction;
    }

    // Heuristic only: this signature is not itself proof of a function boundary.
    // It looks for addiu sp,sp,-N immediately followed by sw ra,offset(sp).
    private void emitStackFrameSignatureCandidates(Address site) throws Exception {
        MemoryBlock block = currentProgram.getMemory().getBlock(site);
        if (block == null) {
            line("stack_frame_signature_scan=NO_MEMORY_BLOCK");
            return;
        }
        long lowerOffset = site.getOffset() - 0x1000L;
        if (lowerOffset < block.getStart().getOffset()) lowerOffset = block.getStart().getOffset();
        long lastOffset = site.getOffset() - 8L;
        if (lastOffset < lowerOffset) {
            line("stack_frame_signature_candidate_count=0");
            return;
        }

        List<Address> candidates = new ArrayList<>();
        for (Address probe = toAddr(lowerOffset); probe.getOffset() <= lastOffset; probe = probe.add(4)) {
            if ((probe.getOffset() & 0xFFL) == 0) monitor.checkCancelled();
            int first = readWord(probe);
            if ((first & 0xFFFF0000) != 0x27BD0000 || (first & 0x00008000) == 0) continue;
            int second = readWord(probe.add(4));
            if ((second & 0xFFFF0000) == 0xAFBF0000) candidates.add(probe);
        }

        line("stack_frame_signature_pattern=addiu_sp_sp_negative_immediate_then_sw_ra_stack");
        line("stack_frame_signature_candidate_count=" + candidates.size());
        line("stack_frame_signature_candidates_are_heuristics_not_function_boundaries=yes");
        int firstToPrint = Math.max(0, candidates.size() - 24);
        for (int i = candidates.size() - 1; i >= firstToPrint; i--) {
            Address candidate = candidates.get(i);
            line("prologue_candidate=" + candidate
                + " bytes_before_site=" + (site.getOffset() - candidate.getOffset())
                + " word0=" + wordText(candidate)
                + " bytes0=" + bytesText(candidate)
                + " word1=" + wordText(candidate.add(4))
                + " bytes1=" + bytesText(candidate.add(4))
                + " word2=" + wordText(candidate.add(8))
                + " bytes2=" + bytesText(candidate.add(8))
                + " status=HEURISTIC_ONLY");
        }
    }

    private boolean flowsTo(Instruction instruction, Address target) {
        if (instruction == null || !instruction.getFlowType().isCall()) return false;
        Address[] flows = instruction.getFlows();
        if (flows == null) return false;
        for (Address flow : flows) if (target.equals(flow)) return true;
        return false;
    }

    @Override
    protected void run() throws Exception {
        String[] args=getScriptArgs();
        if (args.length<2) throw new IllegalArgumentException("Args: output-path callsite:target [callsite:target ...]");
        List<Address> candidateSites = new ArrayList<>();
        try (PrintWriter writer=new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out=writer;
            line("analysis=bounded linear MIPS context disassembly only");
            line("program="+currentProgram.getName());
            line("program_language="+currentProgram.getLanguageID());
            line("whole_program_autoanalysis_disabled=yes");
            line("emulator_or_gameplay_executed=no");
            line("runtime_mapping=HYPOTHESIS; context is conditional on the supplied base");
            for (int i=1;i<args.length;i++) {
                monitor.checkCancelled();
                String[] pair=args[i].split(":");
                if (pair.length!=2) throw new IllegalArgumentException("Expected callsite:target: "+args[i]);
                Address site=toAddr(Long.decode(pair[0]));
                Address target=toAddr(Long.decode(pair[1]));
                candidateSites.add(site);
                line("");
                line("=== CANDIDATE site="+site+" target="+target+" ===");
                if (!currentProgram.getMemory().contains(site)) {
                    line("status=OUTSIDE_IMPORTED_RESOURCE");
                    continue;
                }
                int word=currentProgram.getMemory().getInt(site);
                line("raw_word=0x"+String.format("%08X",word));
                line("raw_bytes="+bytesText(site));
                long targetCalc=((site.getOffset()+4)&0xF0000000L)
                    | (((long)word & 0x03FFFFFFL) << 2);
                line("mips_jal_target_from_word=0x"+String.format("%08X",targetCalc));
                line("raw_opcode_is_jal="+(((word >>> 26)==3)?"yes":"no"));

                Address start=site.subtract(0x60);
                Address end=site.add(0x20);
                AddressSet restricted=new AddressSet(start,end);
                DisassembleCommand cmd=new DisassembleCommand(start,restricted,false);
                boolean disassembled=cmd.applyTo(currentProgram,monitor);
                line("bounded_disassemble_command_success="+disassembled);
                Instruction instruction=currentProgram.getListing().getInstructionAt(site);
                boolean forcedSiteDisassembly=false;
                if (instruction==null) {
                    forcedSiteDisassembly=disassemble(site);
                    instruction=currentProgram.getListing().getInstructionAt(site);
                }
                line("forced_disassembly_at_candidate_site="+forcedSiteDisassembly);
                boolean flow=flowsTo(instruction,target);
                line("ghidra_instruction_at_site="+(instruction==null?"NONE":instruction.toString()));
                line("ghidra_decoded_flow_to_target="+(flow?"yes":"no"));
                if (instruction!=null && instruction.getFlowType().isCall()) {
                    line("decoded_instruction_is_call=yes");
                    Address[] callFlows=instruction.getFlows();
                    line("decoded_instruction_flows="+java.util.Arrays.toString(callFlows));
                } else line("decoded_instruction_is_call=no");
                Function f=getFunctionContaining(site);
                if(f==null) line("caller_function_boundary=UNMAPPED_WITHOUT_AUTOANALYSIS");
                else line("caller_function_entry="+f.getEntryPoint()+" name="+f.getName()
                    +" body_bytes="+f.getBody().getNumAddresses());

                // Search nearby raw words for common stack-frame signatures, but never
                // create a Function from a heuristic or promote these to validated boundaries.
                emitStackFrameSignatureCandidates(site);

                line("--- CONTEXT_WINDOW ---");
                Instruction first=instruction;
                for(int n=0;n<16 && first!=null && first.getPrevious()!=null;n++) first=first.getPrevious();
                if(first==null) {
                    Address probe=start;
                    for(int n=0;n<40 && probe.compareTo(end)<=0;n++,probe=probe.add(4)) {
                        Instruction candidate=currentProgram.getListing().getInstructionAt(probe);
                        if(candidate!=null) line(instructionRecord(candidate));
                    }
                } else {
                    for(int n=0;n<22 && first!=null;n++,first=first.getNext())
                        line(instructionRecord(first));
                }
                line("--- END_CONTEXT_WINDOW ---");
            }
            line("");
            line("=== INCOMING_CONTROL_FLOW_FROM_DECODED_LOCAL_WINDOWS ===");
            InstructionIterator all=currentProgram.getListing().getInstructions(true);
            while(all.hasNext()) {
                monitor.checkCancelled();
                Instruction source=all.next();
                Address[] flows=source.getFlows();
                if(flows==null || flows.length==0) continue;
                for(Address candidate:candidateSites) {
                    if(source.getAddress().equals(candidate)) continue;
                    for(Address flow:flows) if(candidate.equals(flow)) {
                        line("candidate_site="+candidate+" incoming_source="+source.getAddress()
                            +" source_instruction="+source+" source_flow_type="+source.getFlowType());
                    }
                }
            }
            line("incoming_flow_scan_scope=only instructions decoded in candidate context windows; absence is not whole-resource proof");
            out.flush();
            if(out.checkError()) throw new IllegalStateException("Failed writing call context report.");
        }
    }
}
