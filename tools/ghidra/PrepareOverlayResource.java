// PrepareOverlayResource.java
// Seed disassembly from documented static candidate locations; their runtime mapping remains hypothetical.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;

public class PrepareOverlayResource extends GhidraScript {
    private static final long[] CANDIDATES = {
        0x80111228L, 0x801112CCL, 0x801113B4L,
        0x801114F0L, 0x80111588L, 0x80112418L,
        0x8012A9C4L, 0x80137AD8L, 0x800EF98CL,
        0x80100D14L, 0x80100DCCL, 0x8011253CL,
        0x800D5608L, 0x800E1188L, 0x800D8918L,
        0x8011C0D0L, 0x8010478CL, 0x80101814L,
        0x80111198L, 0x8012AAFCL
    };

    @Override
    protected void run() throws Exception {
        println("Static overlay survey only; candidate RAM base is a hypothesis, not runtime-validated.");
        for (long raw : CANDIDATES) {
            Address address = toAddr(raw);
            println("");
            println("candidate_address=" + address);
            if (!currentProgram.getMemory().contains(address)) {
                println("status=OUTSIDE_IMPORTED_RESOURCE");
                continue;
            }
            Instruction instruction = currentProgram.getListing().getInstructionAt(address);
            if (instruction == null) {
                boolean decoded = disassemble(address);
                instruction = currentProgram.getListing().getInstructionAt(address);
                println("seed_disassemble=" + decoded);
            } else {
                println("seed_disassemble=already-decoded");
            }
            Function containing = getFunctionContaining(address);
            if (instruction != null && containing == null) {
                containing = createFunction(address, "candidate_" + Long.toHexString(raw));
                println("created_function=" + (containing == null ? "NO" : containing.getName()));
            }
            println("instruction=" + (instruction == null ? "NONE" : instruction.toString()));
            println("function_containing=" + (containing == null ? "NONE" : containing.getName()));
            println("function_entry=" + (containing == null ? "NONE" : containing.getEntryPoint()));
        }
    }
}
