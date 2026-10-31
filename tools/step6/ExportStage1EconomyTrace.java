// ExportStage1EconomyTrace.java
// Stage 1 economy audit: direct calls to participant-value helpers and candidate
// DATA.BIN entry-1 functions. Static listing/decompilation only; resource base is hypothetical.
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.mem.MemoryBlock;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;

public class ExportStage1EconomyTrace extends GhidraScript {
    private PrintWriter out;
    private DecompInterface decompiler;
    private final Map<String, Function> callers = new LinkedHashMap<String, Function>();
    private final Map<Long, Integer> callCounts = new LinkedHashMap<Long, Integer>();
    private final Map<String, Boolean> dumped = new LinkedHashMap<String, Boolean>();
    private static final long[] CALLEES = {
        0x8001387CL, // structural participant-record setter
        0x800138ECL, // paired participant-record getter
        0x80012A70L, // configured Chakra-target getter candidate
        0x80012A44L, // initial participant-value getter candidate
        0x800BDC4CL  // numeric helper called by candidate resource logic; mapping/meaning unresolved
    };
    private static final long[] CANDIDATE_ADDRESSES = {
        0x800D5608L, 0x800E1188L, 0x800D8918L, 0x8011C0D0L,
        0x8010478CL, 0x80101814L, 0x80111090L, 0x800F1FE4L,
        0x8012AC04L, 0x8012C544L, 0x8012CACC
    };
    private void line(String s) { out.println(s); }
    private String hex(long v) { return String.format("0x%08X", v & 0xffffffffL); }
    private String bytes(Instruction ins) {
        try {
            byte[] b = new byte[ins.getLength()];
            currentProgram.getMemory().getBytes(ins.getAddress(), b);
            StringBuilder s = new StringBuilder();
            for (byte v : b) {
                if (s.length() > 0) s.append(' ');
                s.append(String.format("%02X", v & 0xff));
            }
            return s.toString();
        } catch (Exception e) { return "UNAVAILABLE"; }
    }
    private long word(Instruction ins) {
        try {
            byte[] b = new byte[4];
            currentProgram.getMemory().getBytes(ins.getAddress(), b);
            return ((long)b[0] & 0xffL)
                | (((long)b[1] & 0xffL) << 8)
                | (((long)b[2] & 0xffL) << 16)
                | (((long)b[3] & 0xffL) << 24);
        } catch (Exception e) { return -1L; }
    }
    private long jalTarget(Instruction ins) {
        long w = word(ins);
        if (w < 0 || (w >>> 26) != 3) return -1L;
        long pc = ins.getAddress().getOffset();
        return (((pc + 4L) & 0xF0000000L) | ((w & 0x03ffffffL) << 2)) & 0xffffffffL;
    }
    private void dumpWindow(Instruction center, int before, int after) {
        if (center == null) { line("  context=NO_DECODED_INSTRUCTION"); return; }
        Instruction first = center;
        for (int i=0; i<before && first.getPrevious()!=null; i++) first=first.getPrevious();
        Instruction last = center;
        for (int i=0; i<after && last.getNext()!=null; i++) last=last.getNext();
        for (Instruction cur=first; cur!=null; cur=cur.getNext()) {
            line("  " + cur.getAddress() + " bytes=[" + bytes(cur) + "] " + cur.toString());
            if (cur.getAddress().equals(last.getAddress())) break;
        }
    }
    private void dumpFunction(Function f, String reason) throws Exception {
        if (f == null) return;
        String key=f.getEntryPoint().toString();
        if (dumped.containsKey(key)) {
            line("FUNCTION_ALREADY_EXPORTED entry=" + key + " reason=" + reason);
            return;
        }
        dumped.put(key, Boolean.TRUE);
        line("");
        line("=== CANDIDATE_FUNCTION_BEGIN entry=" + f.getEntryPoint() + " ===");
        line("reason=" + reason);
        line("function_name=" + f.getName());
        line("function_body_min=" + f.getBody().getMinAddress());
        line("function_body_max=" + f.getBody().getMaxAddress());
        line("function_body_address_count=" + f.getBody().getNumAddresses());
        line("function_boundary=Ghidra boundary in hypothetical entry-1 import; runtime reachability not established");
        line("--- RAW_BODY_BEGIN ---");
        InstructionIterator it=currentProgram.getListing().getInstructions(f.getBody(), true);
        int count=0;
        while(it.hasNext()) {
            Instruction ins=it.next();
            line(ins.getAddress() + " bytes=[" + bytes(ins) + "] " + ins.toString());
            count++;
            if(count>=700) { line("RAW_BODY_TRUNCATED=700_INSTRUCTIONS"); break; }
        }
        line("--- RAW_BODY_END ---");
        line("raw_instruction_count_emitted=" + count);
        DecompileResults result=decompiler.decompileFunction(f,90,monitor);
        if(result!=null && result.decompileCompleted() && result.getDecompiledFunction()!=null) {
            line("--- C_DECOMPILATION_BEGIN ---");
            line(result.getDecompiledFunction().getC());
            line("--- C_DECOMPILATION_END ---");
            line("decompile_status=SUCCESS");
        } else {
            line("decompile_status=FAILED");
            line("decompile_message=" + (result==null ? "null result" : result.getErrorMessage()));
        }
        line("=== CANDIDATE_FUNCTION_END ===");
    }
    private void dumpCandidateAddress(long raw) throws Exception {
        Address a=toAddr(raw);
        line("");
        line("=== REQUESTED_ADDRESS " + a + " ===");
        Instruction ins=currentProgram.getListing().getInstructionAt(a);
        Function f=currentProgram.getFunctionManager().getFunctionContaining(a);
        line("instruction_at_address=" + (ins==null ? "NONE" : ins.toString()));
        line("containing_function=" + (f==null ? "NONE" : f.getEntryPoint()));
        if(f!=null) dumpFunction(f,"requested_address=" + hex(raw));
        else dumpWindow(ins,8,24);
    }
    private void scanDirectCalls() throws Exception {
        for(long callee:CALLEES) callCounts.put(callee,0);
        InstructionIterator it=currentProgram.getListing().getInstructions(true);
        while(it.hasNext()) {
            monitor.checkCancelled();
            Instruction ins=it.next();
            if(!"jal".equalsIgnoreCase(ins.getMnemonicString())) continue;
            long target=jalTarget(ins);
            if(target<0 || !callCounts.containsKey(target)) continue;
            callCounts.put(target,callCounts.get(target)+1);
            Function caller=currentProgram.getFunctionManager().getFunctionContaining(ins.getAddress());
            line("");
            line("=== DIRECT_JAL_CALLSITE target=" + hex(target) + " pc=" + ins.getAddress() + " ===");
            line("instruction_bytes=[" + bytes(ins) + "] " + ins.toString());
            line("caller_function=" + (caller==null ? "NONE" : caller.getEntryPoint()));
            line("caller_name=" + (caller==null ? "NONE" : caller.getName()));
            dumpWindow(ins,6,4);
            if(caller!=null) callers.put(caller.getEntryPoint().toString(),caller);
        }
        line("");
        line("=== DIRECT_JAL_COUNTS_BEGIN ===");
        for(long callee:CALLEES) line("direct_jal_target=" + hex(callee) + " count=" + callCounts.get(callee));
        line("direct_jal_only=yes; jalr/indirect calls are not counted");
        line("=== DIRECT_JAL_COUNTS_END ===");
    }
    private void scanAsciiLabels() throws Exception {
        line("");
        line("=== ASCII_LABEL_SCAN_BEGIN ===");
        MemoryBlock block=currentProgram.getMemory().getBlock(toAddr(0x800D0000L));
        if(block==null) { line("entry1_block=NOT_FOUND"); return; }
        int size=(int)block.getSize();
        byte[] data=new byte[size];
        currentProgram.getMemory().getBytes(block.getStart(),data);
        String[] labels={"ESTATE","LVUP_ESTATE","CHAKRA_DOWN","KABE","FUUIN_GET","NINJYUTU"};
        for(String label:labels) {
            byte[] needle=label.getBytes(StandardCharsets.US_ASCII);
            int found=0;
            for(int i=0;i<=data.length-needle.length;i++) {
                boolean same=true;
                for(int j=0;j<needle.length;j++) if(data[i+j]!=needle[j]) { same=false; break; }
                if(same) {
                    line("ascii_label=" + label + " file_offset=" + String.format("0x%X",i)
                        + " hypothetical_address=" + hex(block.getStart().getOffset()+i));
                    found++;
                }
            }
            line("ascii_label_count=" + label + " count=" + found);
        }
        line("scope=literal ASCII tokens in entry-1 bytes only; absence does not disprove UI/resource labels elsewhere");
        line("=== ASCII_LABEL_SCAN_END ===");
    }
    @Override
    protected void run() throws Exception {
        String[] args=getScriptArgs();
        if(args.length<1) throw new IllegalArgumentException("Args: output-path");
        try(PrintWriter writer=new PrintWriter(new BufferedWriter(
            new OutputStreamWriter(new FileOutputStream(args[0]),StandardCharsets.UTF_8)))) {
            out=writer;
            line("analysis=Stage 1 economy static audit");
            line("program=" + currentProgram.getName());
            line("resource=DATA.BIN entry index 1; file_offset=0x10BB000; bytes=596412");
            line("hypothetical_load_base=0x800D0000");
            line("runtime_mapping=HYPOTHESIS_ONLY_NOT_VALIDATED");
            line("game_or_emulator_executed=no");
            line("gameplay_input_sent=no");
            line("savestate_restored=no");
            line("private_binary_uploaded_as_artifact=no");
            scanAsciiLabels();
            decompiler=new DecompInterface();
            decompiler.toggleCCode(true);
            decompiler.toggleSyntaxTree(false);
            if(!decompiler.openProgram(currentProgram))
                throw new IllegalStateException("Cannot open DATA.BIN entry-1 program.");
            scanDirectCalls();
            for(Function f:callers.values()) dumpFunction(f,"caller_of_participant_value_or_target_helper");
            line("");
            line("=== REQUESTED_CANDIDATE_ADDRESSES_BEGIN ===");
            for(long a:CANDIDATE_ADDRESSES) dumpCandidateAddress(a);
            line("=== REQUESTED_CANDIDATE_ADDRESSES_END ===");
            decompiler.dispose();
            out.flush();
            if(out.checkError()) throw new IllegalStateException("Failed writing Stage 1 economy trace.");
        }
    }
}
