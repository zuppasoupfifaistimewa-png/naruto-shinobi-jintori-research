// PrepareRebasedEntry1.java
// Seed the same documented entry-1 offsets as the 0x800D0000 import,
// translated by file offset to candidate base 0x800AD450.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;

public class PrepareRebasedEntry1 extends GhidraScript {
    private static final long OLD_BASE = 0x800D0000L;
    private static final long NEW_BASE = 0x800AD450L;
    private static final long SIZE = 0x919BCL;
    private static final long[] OLD_CANDIDATES = {
        0x80111228L, 0x801112CCL, 0x801113B4L, 0x801114F0L,
        0x80111588L, 0x80112418L, 0x8011C0D0L, 0x8011253CL,
        0x800EF98CL, 0x80100D14L, 0x80100DCCL
    };

    @Override
    protected void run() throws Exception {
        println("scope=static candidate function seed only; no emulator/gameplay");
        println("old_reference_base=0x800D0000 new_candidate_base=0x800AD450");
        for (long old : OLD_CANDIDATES) {
            long offset = old - OLD_BASE;
            if (offset < 0 || offset >= SIZE) {
                println("old_candidate=0x" + Long.toHexString(old) + " status=OUT_OF_ENTRY_RANGE");
                continue;
            }
            Address a = toAddr(NEW_BASE + offset);
            if (!currentProgram.getMemory().contains(a)) {
                println("candidate=" + a + " status=OUTSIDE_IMPORTED_RESOURCE");
                continue;
            }
            Instruction ins = currentProgram.getListing().getInstructionAt(a);
            boolean forced = false;
            if (ins == null) {
                forced = disassemble(a);
                ins = currentProgram.getListing().getInstructionAt(a);
            }
            Function f = getFunctionContaining(a);
            if (ins != null && f == null) {
                f = createFunction(a, "rebased_candidate_" + Long.toHexString(offset));
            }
            println("old=0x" + Long.toHexString(old)
                + " file_offset=0x" + Long.toHexString(offset)
                + " candidate=" + a
                + " disassemble=" + forced
                + " instruction=" + (ins == null ? "NONE" : ins.toString())
                + " function=" + (f == null ? "NONE" : f.getName())
                + " function_entry=" + (f == null ? "NONE" : f.getEntryPoint().toString()));
        }
    }
}
