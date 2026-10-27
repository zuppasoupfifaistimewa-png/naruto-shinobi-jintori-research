// PrepareStep6Resource.java
// Seed only previously documented DATA.BIN entry-1 candidates before static analysis.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;

public class PrepareStep6Resource extends GhidraScript {
    private static final long[] CANDIDATES = {
        0x80111228L, 0x801112CCL, 0x801113B4L, 0x801114F0L,
        0x80111588L, 0x80112418L, 0x8011C0D0L, 0x8011253CL,
        0x800EF98CL, 0x80100D14L, 0x80100DCCL
    };

    @Override
    protected void run() throws Exception {
        println("scope=targeted static seed candidates in DATA.BIN entry 1");
        println("base=0x800D0000 HYPOTHESIS_ONLY");
        println("game_or_emulator_executed=no");
        for (long raw : CANDIDATES) {
            Address a = toAddr(raw);
            if (!currentProgram.getMemory().contains(a)) {
                println("candidate=" + a + " status=OUTSIDE_IMPORTED_RESOURCE");
                continue;
            }
            Instruction ins = currentProgram.getListing().getInstructionAt(a);
            if (ins == null) {
                boolean ok = disassemble(a);
                ins = currentProgram.getListing().getInstructionAt(a);
                println("candidate=" + a + " forced_disassembly=" + ok);
            }
            Function f = getFunctionContaining(a);
            if (ins != null && f == null) f = createFunction(a, "step6_candidate_" + Long.toHexString(raw));
            println("candidate=" + a + " instruction=" + (ins == null ? "NONE" : ins.toString())
                + " function=" + (f == null ? "NONE" : f.getName())
                + " entry=" + (f == null ? "NONE" : f.getEntryPoint()));
        }
    }
}
