// ExportOverlaySurvey.java
// Text-only decompilation/xref survey of DATA.BIN entry 1 at a provisional RAM base.
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;

public class ExportOverlaySurvey extends GhidraScript {
    private PrintWriter out;
    private void line(String s) { out.println(s); }

    private void dumpTarget(DecompInterface decompiler, long raw) {
        Address address = toAddr(raw);
        line("");
        line("=== CANDIDATE " + address + " ===");
        if (!currentProgram.getMemory().contains(address)) {
            line("status=OUTSIDE_IMPORTED_RESOURCE");
            return;
        }
        Instruction instruction = currentProgram.getListing().getInstructionAt(address);
        line("instruction=" + (instruction == null ? "NONE" : instruction.toString()));
        Function f = getFunctionContaining(address);
        line("function_containing=" + (f == null ? "NONE" : f.getName()));
        line("function_entry=" + (f == null ? "NONE" : f.getEntryPoint()));
        if (f != null) {
            line("function_body_bytes=" + f.getBody().getNumAddresses());
            DecompileResults result = decompiler.decompileFunction(f, 90, monitor);
            if (result != null && result.decompileCompleted() && result.getDecompiledFunction() != null) {
                line("--- C_DECOMPILATION_BEGIN ---");
                line(result.getDecompiledFunction().getC());
                line("--- C_DECOMPILATION_END ---");
            } else {
                line("decompile_status=FAILED");
                line("decompile_message=" + (result == null ? "null result" : result.getErrorMessage()));
            }
        }
        if (instruction == null) return;
        Instruction first = instruction;
        for (int i = 0; i < 8 && first.getPrevious() != null; i++) first = first.getPrevious();
        line("--- INSTRUCTION_WINDOW_BEGIN ---");
        for (int i = 0; i < 28 && first != null; i++, first = first.getNext())
            line(first.getAddress() + "\\t" + first.toString());
        line("--- INSTRUCTION_WINDOW_END ---");
    }

    private void dumpRefs(long raw, String label) {
        Address target = toAddr(raw);
        line("");
        line("=== REFERENCES_TO " + label + " target=" + target + " ===");
        int count = 0;
        ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(target);
        while (refs.hasNext()) {
            Reference r = refs.next();
            Function f = getFunctionContaining(r.getFromAddress());
            line("from=" + r.getFromAddress() + "\\ttype=" + r.getReferenceType()
                + "\\tfunction=" + (f == null ? "NONE" : f.getName())
                + "\\tfunction_entry=" + (f == null ? "NONE" : f.getEntryPoint()));
            count++;
        }
        line("reference_count=" + count);
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 1 || args[0].trim().isEmpty())
            throw new IllegalArgumentException("Provide output text path as script argument 1.");
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out = writer;
            line("analysis=static survey of DATA.BIN entry 1");
            line("entry_index=1");
            line("entry_file_offset=0x10BB000");
            line("entry_bytes=596412");
            line("hypothetical_ram_base=0x800D0000");
            line("hypothesis_boundary=base inferred from older static reference consistency; not runtime-validated");
            line("gameplay_or_emulator_executed=no");

            DecompInterface decompiler = new DecompInterface();
            decompiler.toggleCCode(true);
            decompiler.toggleSyntaxTree(false);
            if (!decompiler.openProgram(currentProgram))
                throw new IllegalStateException("Decompiler could not open overlay resource.");
            long[] candidates = {0x80111228L,0x801112CCL,0x801113B4L,0x801114F0L,0x80111588L,0x80112418L};
            for (long address : candidates) dumpTarget(decompiler, address);

            // Step 6: trace target-check callers, transition routines and Chakra mutation callers.
            long[] followups = {
                0x8012A9C4L, 0x80137AD8L, 0x800EF98CL,
                0x80100D14L, 0x80100DCCL, 0x8011253CL,
                0x800D5608L, 0x800E1188L, 0x800D8918L,
                0x8011C0D0L, 0x8010478CL, 0x80101814L,
                0x80111198L, 0x8012AAFCL, 0x800BDBFCL
            };
            for (long address : followups) dumpTarget(decompiler, address);

            dumpRefs(0x80012A44L, "main_chakra_initial_getter");
            dumpRefs(0x80012A70L, "main_chakra_target_getter");
            dumpRefs(0x8001387CL, "main_chakra_setter");
            dumpRefs(0x800138ECL, "main_player_chakra_getter");
            dumpRefs(0x80070C80L, "main_initial_chakra_global");
            dumpRefs(0x800EF98CL, "transition_FUN_800EF98C");
            dumpRefs(0x80100D14L, "transition_FUN_80100D14");
            dumpRefs(0x80100DCCL, "transition_FUN_80100DCC");
            dumpRefs(0x8011253CL, "threshold_failure_branch_8011253C");
            dumpRefs(0x800BDBFCL, "external_resource_target_FUN_800BDBFC");
            decompiler.dispose();
            out.flush();
            if (out.checkError()) throw new IllegalStateException("Failed writing overlay survey.");
        }
    }
}
