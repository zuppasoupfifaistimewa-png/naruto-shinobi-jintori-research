// ExportPerRecordCallerGraph.java
// Bounded direct-call graph and post-call context for FUN_800B770C callers.
// Static only: the resource base is a candidate loader-buffer mapping.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.TreeMap;

public class ExportPerRecordCallerGraph extends GhidraScript {
    private PrintWriter out;
    private static final long BASE = 0x800AD450L;
    private static final long TARGET = 0x800B770CL;
    private static final long[] WATCH = {
        0x8001387CL, // participant-value setter
        0x800138ECL, // participant-value getter
        0x80012A70L, // configured target getter
        0x800BDC4CL, // aggregate helper
        0x8001B364L, // drawing helper
        0x800BDBFCL,
        0x800B7464L
    };
    private final Map<String, Function> callers = new LinkedHashMap<String, Function>();
    private final Map<Long, Integer> globalCounts = new TreeMap<Long, Integer>();

    private void line(String s) { out.println(s); }
    private String hex(long v) { return String.format("0x%08X", v & 0xffffffffL); }

    private long readWord(Instruction ins) throws Exception {
        byte[] b = new byte[4];
        currentProgram.getMemory().getBytes(ins.getAddress(), b);
        return ((long)b[0] & 0xffL)
            | (((long)b[1] & 0xffL) << 8)
            | (((long)b[2] & 0xffL) << 16)
            | (((long)b[3] & 0xffL) << 24);
    }

    private long directJalTarget(Instruction ins) throws Exception {
        long word = readWord(ins);
        if ((word >>> 26) != 3) return -1L;
        long pc = ins.getAddress().getOffset();
        return (((pc + 4L) & 0xF0000000L) | ((word & 0x03ffffffL) << 2)) & 0xffffffffL;
    }

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
        } catch (Exception e) {
            return "UNAVAILABLE";
        }
    }

    private void dumpWindow(Instruction center, int before, int after) throws Exception {
        if (center == null) return;
        Instruction first = center;
        for (int i = 0; i < before && first.getPrevious() != null; i++) first = first.getPrevious();
        Instruction last = center;
        for (int i = 0; i < after && last.getNext() != null; i++) last = last.getNext();
        for (Instruction ins = first; ins != null; ins = ins.getNext()) {
            line("  " + ins.getAddress() + " bytes=[" + bytes(ins) + "] " + ins.toString());
            if (ins.getAddress().equals(last.getAddress())) break;
        }
    }

    private boolean watched(long target) {
        for (long value : WATCH) if (value == target) return true;
        return false;
    }

    private void scanTargetCallers() throws Exception {
        int sites = 0;
        InstructionIterator all = currentProgram.getListing().getInstructions(true);
        while (all.hasNext()) {
            monitor.checkCancelled();
            Instruction ins = all.next();
            if (!"jal".equalsIgnoreCase(ins.getMnemonicString())) continue;
            long target = directJalTarget(ins);
            if (target != TARGET) continue;
            sites++;
            Function caller = currentProgram.getFunctionManager().getFunctionContaining(ins.getAddress());
            line("");
            line("=== B770C_CALLSITE address=" + ins.getAddress() + " ===");
            line("instruction_bytes=[" + bytes(ins) + "] " + ins.toString());
            line("caller_function_entry=" + (caller == null ? "NONE" : caller.getEntryPoint()));
            line("caller_function_name=" + (caller == null ? "NONE" : caller.getName()));
            if (caller != null) callers.put(caller.getEntryPoint().toString(), caller);
            line("--- PRE_AND_POST_CALL_CONTEXT_BEGIN ---");
            dumpWindow(ins, 8, 12);
            line("--- PRE_AND_POST_CALL_CONTEXT_END ---");
        }
        line("");
        line("direct_b770c_callsite_count=" + sites);
        line("unique_caller_function_count=" + callers.size());
    }

    private void scanCaller(Function f) throws Exception {
        line("");
        line("=== CALLER_FUNCTION_BEGIN entry=" + f.getEntryPoint() + " ===");
        line("function_name=" + f.getName());
        line("body_min=" + f.getBody().getMinAddress());
        line("body_max=" + f.getBody().getMaxAddress());
        line("body_address_count=" + f.getBody().getNumAddresses());
        Map<Long, Integer> counts = new TreeMap<Long, Integer>();
        Map<Long, Instruction> firstSites = new TreeMap<Long, Instruction>();
        InstructionIterator iter = currentProgram.getListing().getInstructions(f.getBody(), true);
        while (iter.hasNext()) {
            Instruction ins = iter.next();
            if (!"jal".equalsIgnoreCase(ins.getMnemonicString())) continue;
            long target = directJalTarget(ins);
            if (target < 0) continue;
            if (watched(target)) {
                counts.put(target, counts.getOrDefault(target, 0) + 1);
                globalCounts.put(target, globalCounts.getOrDefault(target, 0) + 1);
                if (!firstSites.containsKey(target)) firstSites.put(target, ins);
                line("  watched_call pc=" + ins.getAddress() + " target=" + hex(target)
                    + " bytes=[" + bytes(ins) + "] " + ins.toString());
            }
        }
        for (Map.Entry<Long,Integer> e : counts.entrySet()) {
            line("  watched_target_summary target=" + hex(e.getKey()) + " count=" + e.getValue());
            if (firstSites.containsKey(e.getKey())) {
                line("  context_for_target=" + hex(e.getKey()));
                dumpWindow(firstSites.get(e.getKey()), 5, 8);
            }
        }
        line("=== CALLER_FUNCTION_END ===");
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 1) throw new IllegalArgumentException("Args: output-path");
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out = writer;
            line("analysis=direct caller graph for Entry 1 per-record value helper");
            line("resource=DATA.BIN directory index 1; DATA.BIN offset=0x10BB000; bytes=596412");
            line("hypothetical_import_base=" + hex(BASE));
            line("base_status=STATIC_CANDIDATE_FROM_LOADER_GLOBAL; runtime memory not captured");
            line("target_function=" + hex(TARGET));
            line("watched_targets=0x8001387C,0x800138EC,0x80012A70,0x800BDC4C,0x8001B364,0x800BDBFC,0x800B7464");
            line("game_or_emulator_executed=no");
            line("gameplay_input_sent=no");
            line("savestate_restored=no");
            line("private_binary_uploaded_as_artifact=no");
            scanTargetCallers();
            for (Function f : callers.values()) scanCaller(f);
            line("");
            line("=== GLOBAL_WATCHED_CALL_COUNTS_BEGIN ===");
            for (Map.Entry<Long,Integer> e : globalCounts.entrySet())
                line("target=" + hex(e.getKey()) + " total_direct_calls_across_callers=" + e.getValue());
            line("NOTE=indirect JALR calls and calls outside decoded function bodies are not included");
            line("=== GLOBAL_WATCHED_CALL_COUNTS_END ===");
            out.flush();
            if (out.checkError()) throw new IllegalStateException("Failed writing caller graph.");
        }
    }
}
