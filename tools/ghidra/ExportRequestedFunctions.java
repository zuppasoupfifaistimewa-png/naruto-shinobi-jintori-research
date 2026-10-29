// Export full Ghidra-defined disassembly for requested MIPS functions.
// Args: output.txt targetAddress [targetAddress ...]
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSetView;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import java.io.File;
import java.io.PrintWriter;
import java.util.Arrays;

public class ExportRequestedFunctions extends GhidraScript {
    private String hex(Address a) { return a == null ? "UNKNOWN" : String.format("0x%08X", a.getOffset()); }
    private String bytes(byte[] b) {
        StringBuilder s = new StringBuilder();
        for (int i=0;i<b.length;i++) { if (i>0) s.append(' '); s.append(String.format("%02X", b[i] & 0xff)); }
        return s.toString();
    }
    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2) throw new IllegalArgumentException("args: output.txt targetAddress...");
        File output = new File(args[0]);
        output.getParentFile().mkdirs();
        try (PrintWriter out = new PrintWriter(output, "UTF-8")) {
            out.println("Static MIPS disassembly from Ghidra instruction listing; no emulator.");
            out.println("program=" + currentProgram.getName());
            out.println("language=" + currentProgram.getLanguageID());
            out.println("image_min=" + hex(currentProgram.getMinAddress()));
            out.println("image_max=" + hex(currentProgram.getMaxAddress()));
            out.println("requested_targets=" + String.join(",", Arrays.copyOfRange(args,1,args.length)));
            for (int i=1;i<args.length;i++) {
                Address target = toAddr(args[i]);
                out.println();
                out.println("================================================================");
                out.println("REQUESTED_TARGET=" + hex(target));
                if (!currentProgram.getMemory().contains(target)) {
                    out.println("STATUS=UNMAPPED_IN_GHIDRA_PROGRAM");
                    out.println("FUNCTION_BOUNDS=TIDAK TAHU");
                    continue;
                }
                Function f = currentProgram.getFunctionManager().getFunctionContaining(target);
                if (f == null) {
                    out.println("STATUS=NO_GHIDRA_FUNCTION_BOUNDARY");
                    out.println("FUNCTION_BOUNDS=TIDAK TAHU");
                    Instruction ins = currentProgram.getListing().getInstructionAt(target);
                    if (ins != null) out.println("TARGET_INSTRUCTION=" + hex(ins.getAddress()) + " " + bytes(ins.getBytes()) + " " + ins.toString());
                    continue;
                }
                AddressSetView body = f.getBody();
                out.println("STATUS=FUNCTION_FOUND");
                out.println("FUNCTION_NAME=" + f.getName());
                out.println("FUNCTION_ENTRY=" + hex(f.getEntryPoint()));
                out.println("FUNCTION_BODY_MIN=" + hex(body.getMinAddress()));
                out.println("FUNCTION_BODY_MAX=" + hex(body.getMaxAddress()));
                out.println("TARGET_OFFSET_WITHIN_FUNCTION=0x" + Long.toHexString(target.getOffset()-f.getEntryPoint().getOffset()).toUpperCase());
                out.println("FUNCTION_SOURCE=Ghidra function manager body bounds");
                int n=0;
                InstructionIterator it = currentProgram.getListing().getInstructions(body, true);
                while (it.hasNext()) {
                    Instruction ins = it.next();
                    out.printf("%s  %-23s  %-40s  flow=%s  flows=%s%n",
                        hex(ins.getAddress()), bytes(ins.getBytes()), ins.toString(),
                        ins.getFlowType(), Arrays.toString(ins.getFlows()));
                    n++;
                }
                out.println("INSTRUCTION_COUNT=" + n);
                out.println("END_FUNCTION=" + f.getName());
            }
        }
        println("W3_DISASSEMBLY_OUTPUT=" + output.getAbsolutePath());
    }
}