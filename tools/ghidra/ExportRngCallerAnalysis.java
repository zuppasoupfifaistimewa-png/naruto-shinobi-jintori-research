// ExportRngCallerAnalysis.java
// Targeted static analysis for the four known direct callers of the LCG candidate.
// Exports only text: limited decompilation, nearby instructions, and known xrefs.
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

public class ExportRngCallerAnalysis extends GhidraScript {
    private PrintWriter out;

    private void line(String value) {
        out.println(value);
    }

    private void dumpFunction(DecompInterface decompiler, long entryOffset, String expectedCallSite) {
        Address entry = toAddr(entryOffset);
        Function function = getFunctionAt(entry);
        line("");
        line("=== FUNCTION entry=" + entry + " expected_call_site=" + expectedCallSite + " ===");
        if (function == null) {
            line("function_status=NOT_FOUND_AT_EXPECTED_ENTRY");
            Function containing = getFunctionContaining(toAddr(Long.decode(expectedCallSite)));
            if (containing != null) {
                line("containing_function_entry=" + containing.getEntryPoint());
                line("containing_function_name=" + containing.getName());
            }
            return;
        }
        line("name=" + function.getName());
        line("body_address_count=" + function.getBody().getNumAddresses());
        line("source_type=" + function.getSymbol().getSource());
        DecompileResults result = decompiler.decompileFunction(function, 90, monitor);
        if (result != null && result.decompileCompleted() && result.getDecompiledFunction() != null) {
            line("--- C_DECOMPILATION_BEGIN ---");
            line(result.getDecompiledFunction().getC());
            line("--- C_DECOMPILATION_END ---");
        } else {
            line("decompile_status=FAILED");
            line("decompile_message=" + (result == null ? "null result" : result.getErrorMessage()));
        }

        Address site;
        try {
            site = toAddr(Long.decode(expectedCallSite));
        } catch (Exception e) {
            line("callsite_parse_error=" + e.getMessage());
            return;
        }
        Instruction instruction = currentProgram.getListing().getInstructionAt(site);
        line("--- CALLSITE_INSTRUCTIONS_BEGIN ---");
        if (instruction == null) {
            line("callsite_instruction=NOT_FOUND");
        } else {
            Instruction first = instruction;
            for (int i = 0; i < 3 && first.getPrevious() != null; i++) {
                first = first.getPrevious();
            }
            for (int i = 0; i < 12 && first != null; i++, first = first.getNext()) {
                line(first.getAddress() + "\t" + first.toString());
            }
        }
        line("--- CALLSITE_INSTRUCTIONS_END ---");
    }


    private void dumpSimpleFunction(DecompInterface decompiler, long entryOffset) {
        Address entry = toAddr(entryOffset);
        Function function = getFunctionAt(entry);
        line("");
        line("=== HELPER_FUNCTION entry=" + entry + " ===");
        if (function == null) {
            Function containing = getFunctionContaining(entry);
            line("function_status=NOT_FOUND_AT_ENTRY");
            if (containing != null) {
                line("containing_function_entry=" + containing.getEntryPoint());
                line("containing_function_name=" + containing.getName());
            }
            return;
        }
        line("name=" + function.getName());
        line("body_address_count=" + function.getBody().getNumAddresses());
        line("source_type=" + function.getSymbol().getSource());
        DecompileResults result = decompiler.decompileFunction(function, 90, monitor);
        if (result != null && result.decompileCompleted() && result.getDecompiledFunction() != null) {
            line("--- C_DECOMPILATION_BEGIN ---");
            line(result.getDecompiledFunction().getC());
            line("--- C_DECOMPILATION_END ---");
        } else {
            line("decompile_status=FAILED");
            line("decompile_message=" + (result == null ? "null result" : result.getErrorMessage()));
        }
        line("--- HELPER_INSTRUCTIONS_BEGIN ---");
        Instruction instruction = currentProgram.getListing().getInstructionAt(entry);
        for (int i = 0; i < 28 && instruction != null; i++, instruction = instruction.getNext()) {
            line(instruction.getAddress() + "\\t" + instruction.toString());
        }
        line("--- HELPER_INSTRUCTIONS_END ---");
    }

    private void dumpReferences(long targetOffset, String label) {
        Address target = toAddr(targetOffset);
        line("");
        line("=== REFERENCES_TO " + label + " target=" + target + " ===");
        int count = 0;
        ReferenceIterator references = currentProgram.getReferenceManager().getReferencesTo(target);
        while (references.hasNext()) {
            Reference reference = references.next();
            Function function = getFunctionContaining(reference.getFromAddress());
            line("from=" + reference.getFromAddress()
                + "\ttype=" + reference.getReferenceType()
                + "\toperand=" + reference.getOperandIndex()
                + "\tfunction=" + (function == null ? "NO_FUNCTION" : function.getName())
                + "\tfunction_entry=" + (function == null ? "NONE" : function.getEntryPoint()));
            count++;
        }
        line("reference_count=" + count);
    }

    private void dumpInstructionWindow(long startOffset, long endExclusive, String label) {
        line("");
        line("=== INSTRUCTION_WINDOW " + label + " " + toAddr(startOffset)
            + ".." + toAddr(endExclusive) + " (end exclusive) ===");
        Address current = toAddr(startOffset);
        Address end = toAddr(endExclusive);
        int count = 0;
        while (current.compareTo(end) < 0) {
            Instruction instruction = currentProgram.getListing().getInstructionAt(current);
            if (instruction != null) {
                line(instruction.getAddress() + "\t" + instruction.toString());
                Address next = instruction.getMaxAddress().add(1);
                current = next;
                count++;
            } else {
                current = current.add(4);
            }
        }
        line("instruction_count=" + count);
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 1 || args[0].trim().isEmpty()) {
            throw new IllegalArgumentException("Provide output text path as script argument 1.");
        }
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out = writer;
            line("analysis=targeted Ghidra decompilation and xref inspection");
            line("executable=SLPS_035.53");
            line("executable_sha256=a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569");
            line("emulator_or_gameplay_executed=no");
            line("interpretation_boundary=FUN labels are default names; gameplay role is not inferred from names alone");

            DecompInterface decompiler = new DecompInterface();
            decompiler.toggleCCode(true);
            decompiler.toggleSyntaxTree(false);
            if (!decompiler.openProgram(currentProgram)) {
                throw new IllegalStateException("Decompiler could not open imported program.");
            }
            dumpFunction(decompiler, 0x80015ADCL, "0x80015B14");
            dumpFunction(decompiler, 0x80015B7CL, "0x80015BF0");
            dumpFunction(decompiler, 0x8001A328L, "0x8001A460");
            dumpFunction(decompiler, 0x80020BF4L, "0x80020C24");

            // Step 4 helper trace: domains, filtering predicates, and downstream initializers.
            dumpSimpleFunction(decompiler, 0x800154D4L);
            dumpSimpleFunction(decompiler, 0x80015610L);
            dumpSimpleFunction(decompiler, 0x80015768L);
            dumpSimpleFunction(decompiler, 0x800157C4L);
            dumpSimpleFunction(decompiler, 0x800158D8L);
            dumpSimpleFunction(decompiler, 0x800159BCL);
            dumpSimpleFunction(decompiler, 0x80016C68L);
            dumpSimpleFunction(decompiler, 0x80020D48L);
            dumpSimpleFunction(decompiler, 0x80018300L);
            dumpSimpleFunction(decompiler, 0x80018468L);

            // Xrefs to RNG and candidate/global table locations (some may be outside loaded text).
            dumpReferences(0x8006D794L, "bounded_candidate_limit_DAT_8006D794");
            dumpReferences(0x80070770L, "candidate_filter_bitset_DAT_80070770");
            dumpReferences(0x800A3118L, "rng_state_global");
            dumpReferences(0x80035D78L, "lcg_candidate");
            dumpReferences(0x80035DA8L, "seed_setter_candidate");
            dumpReferences(0x80070D02L, "shuffled_table_count_DAT_80070D02");
            dumpReferences(0x80070D0AL, "shuffled_table_base_DAT_80070D0A");
            dumpReferences(0x80089DA9L, "candidate_choice_DAT_80089DA9");
            dumpInstructionWindow(0x80035D60L, 0x80035DC0L, "LCG_AND_SEED_SETTER");
            decompiler.dispose();
            out.flush();
            if (out.checkError()) {
                throw new IllegalStateException("Failed writing targeted RNG analysis.");
            }
        }
    }
}
