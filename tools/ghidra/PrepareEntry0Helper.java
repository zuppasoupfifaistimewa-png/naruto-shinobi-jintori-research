// PrepareEntry0Helper.java
// Seed static analysis of DATA.BIN entry 0 at a provisional base to inspect helper 0x800BDBFC.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;

public class PrepareEntry0Helper extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Address target = toAddr(0x800BDBFCL);
        if (!currentProgram.getMemory().contains(target)) {
            throw new IllegalStateException("Target helper 0x800BDBFC is outside imported DATA.BIN entry 0.");
        }
        if (currentProgram.getListing().getInstructionAt(target) == null) {
            boolean ok = disassemble(target);
            if (!ok || currentProgram.getListing().getInstructionAt(target) == null) {
                throw new IllegalStateException("Could not seed disassembly at " + target);
            }
        }
        Function f = getFunctionContaining(target);
        if (f == null) f = createFunction(target, "candidate_800bdbfc");
        if (f == null) throw new IllegalStateException("Could not create helper function at " + target);
        println("target=" + target);
        println("function=" + f.getName());
        println("entry=" + f.getEntryPoint());
        println("body_bytes=" + f.getBody().getNumAddresses());
        println("warning=base 0x800AD000 is a static hypothesis, not runtime validated");
    }
}
