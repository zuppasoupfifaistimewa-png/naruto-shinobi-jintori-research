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

                line("--- CONTEXT_WINDOW ---");
                Instruction first=instruction;
                for(int n=0;n<16 && first!=null && first.getPrevious()!=null;n++) first=first.getPrevious();
                if(first==null) {
                    Address probe=start;
                    for(int n=0;n<40 && probe.compareTo(end)<=0;n++,probe=probe.add(4)) {
                        Instruction candidate=currentProgram.getListing().getInstructionAt(probe);
                        if(candidate!=null) line(candidate.getAddress()+"\t"+candidate.toString());
                    }
                } else {
                    for(int n=0;n<22 && first!=null;n++,first=first.getNext())
                        line(first.getAddress()+"\t"+first.toString());
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
