// PreparePsxExe.java
// Set a known PS-X EXE entrypoint so headless auto-analysis has a code root.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

public class PreparePsxExe extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Address entry = toAddr(0x80011448L);
        if (!currentProgram.getMemory().contains(entry)) {
            throw new IllegalStateException("Expected PS-X EXE entrypoint is outside loaded memory: " + entry);
        }

        if (currentProgram.getListing().getInstructionAt(entry) == null) {
            boolean decoded = disassemble(entry);
            if (!decoded || currentProgram.getListing().getInstructionAt(entry) == null) {
                throw new IllegalStateException("Could not disassemble entrypoint " + entry);
            }
        }

        Function function = getFunctionAt(entry);
        if (function == null) {
            function = createFunction(entry, "entry_SLPS_035_53");
        }
        if (function == null) {
            throw new IllegalStateException("Could not create entrypoint function at " + entry);
        }

        println("Prepared PS-X EXE entrypoint: " + entry);
        println("Entrypoint function: " + function.getName());
        println("Main text block starts at 0x80010000; file bytes are loaded from offset 0x800.");
    }
}
