// ExportEntry0Helper.java
// Text-only decompilation and intra-resource cross-reference survey for DATA.BIN entry 0.
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

public class ExportEntry0Helper extends GhidraScript {
    private PrintWriter out;
    private void line(String s) { out.println(s); }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 1 || args[0].trim().isEmpty())
            throw new IllegalArgumentException("Provide output path.");
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out = writer;
            Address target = toAddr(0x800BDBFCL);
            line("analysis=static decompilation of DATA.BIN entry 0 helper");
            line("resource=DATA.BIN entry index 0");
            line("entry_file_offset=0x5F800");
            line("entry_bytes=110536 (0x1AF08)");
            line("hypothetical_ram_base=0x800AD000");
            line("runtime_mapping=NOT_VALIDATED");
            line("target=0x800BDBFC");
            line("target_file_offset_under_hypothesis=0x10BFC");
            line("gameplay_or_emulator_executed=no");
            line("");
            if (!currentProgram.getMemory().contains(target))
                throw new IllegalStateException("Target is outside imported memory.");
            Instruction ins = currentProgram.getListing().getInstructionAt(target);
            line("instruction=" + (ins == null ? "NONE" : ins.toString()));
            Function f = getFunctionContaining(target);
            line("function=" + (f == null ? "NONE" : f.getName()));
            line("function_entry=" + (f == null ? "NONE" : f.getEntryPoint()));
            if (f != null) {
                line("function_body_bytes=" + f.getBody().getNumAddresses());
                DecompInterface decompiler = new DecompInterface();
                decompiler.toggleCCode(true);
                decompiler.toggleSyntaxTree(false);
                if (!decompiler.openProgram(currentProgram))
                    throw new IllegalStateException("Decompiler could not open entry0 resource.");
                DecompileResults result = decompiler.decompileFunction(f, 90, monitor);
                if (result != null && result.decompileCompleted() && result.getDecompiledFunction() != null) {
                    line("--- C_DECOMPILATION_BEGIN ---");
                    line(result.getDecompiledFunction().getC());
                    line("--- C_DECOMPILATION_END ---");
                } else {
                    line("decompile_status=FAILED");
                    line("decompile_message=" + (result == null ? "null result" : result.getErrorMessage()));
                }
                decompiler.dispose();
            }
            line("");
            line("=== REFERENCES_TO_HELPER ===");
            ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(target);
            int count = 0;
            while (refs.hasNext()) {
                Reference r = refs.next();
                Function caller = getFunctionContaining(r.getFromAddress());
                line("from=" + r.getFromAddress() + "\ttype=" + r.getReferenceType()
                    + "\tfunction=" + (caller == null ? "NONE" : caller.getName())
                    + "\tfunction_entry=" + (caller == null ? "NONE" : caller.getEntryPoint()));
                count++;
            }
            line("reference_count=" + count);
            line("");
            line("=== INSTRUCTION_WINDOW ===");
            Instruction first = ins;
            for (int i = 0; i < 8 && first != null && first.getPrevious() != null; i++) first = first.getPrevious();
            for (int i = 0; i < 36 && first != null; i++, first = first.getNext())
                line(first.getAddress() + "\t" + first.toString());
            line("interpretation=static candidate only; no runtime call contract has been proven");
            out.flush();
            if (out.checkError()) throw new IllegalStateException("Failed writing entry 0 helper report.");
        }
    }
}
