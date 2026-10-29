// Export full Ghidra-defined disassembly for requested MIPS functions.
// Args: output.txt targetAddress [targetAddress ...]
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSetView;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.File;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

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
        if (args.length < 2) throw new IllegalArgumentException("args: output.txt targetAddress... [--xref-out=path]");
        File output = new File(args[0]);
        output.getParentFile().mkdirs();
        String xrefPath = null;
        List<String> targetArgs = new ArrayList<>();
        for (int i=1; i<args.length; i++) {
            if (args[i].startsWith("--xref-out=")) xrefPath = args[i].substring("--xref-out=".length());
            else targetArgs.add(args[i]);
        }
        Set<String> uniqueCallers = new LinkedHashSet<>();
        try (PrintWriter out = new PrintWriter(output, "UTF-8")) {
            out.println("Static MIPS disassembly from Ghidra instruction listing; no emulator.");
            out.println("program=" + currentProgram.getName());
            out.println("language=" + currentProgram.getLanguageID());
            out.println("image_min=" + hex(currentProgram.getMinAddress()));
            out.println("image_max=" + hex(currentProgram.getMaxAddress()));
            out.println("requested_targets=" + String.join(",", targetArgs.toArray(new String[0])));
            for (int i=0;i<targetArgs.size();i++) {
                Address target = toAddr(targetArgs.get(i));
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
        if (xrefPath != null) {
            File xf = new File(xrefPath);
            xf.getParentFile().mkdirs();
            try (PrintWriter xout = new PrintWriter(xf, "UTF-8")) {
                xout.println("STATIC_MAIN_EXE_XREFS; no emulator; target PCs are exact MIPS helper entry addresses");
                for (String token : targetArgs) {
                    Address target = toAddr(token);
                    xout.println();
                    xout.println("TARGET=" + hex(target));
                    ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(target);
                    while (refs.hasNext()) {
                        Reference ref = refs.next();
                        Address from = ref.getFromAddress();
                        Function caller = currentProgram.getFunctionManager().getFunctionContaining(from);
                        Instruction callInsn = currentProgram.getListing().getInstructionAt(from);
                        xout.printf("XREF\t%s\t%s\t%s\t%s\t%s\t%s\t%s%n",
                            hex(target), hex(from), ref.getReferenceType().toString(),
                            caller == null ? "TIDAK_TAHU" : caller.getName(),
                            caller == null ? "" : hex(caller.getEntryPoint()),
                            caller == null ? "" : hex(caller.getBody().getMinAddress()),
                            caller == null ? "" : hex(caller.getBody().getMaxAddress()),
                            callInsn == null ? "NO_INSTRUCTION" : callInsn.toString().replace('\t',' '));
                        if (caller != null) uniqueCallers.add(hex(caller.getEntryPoint()));
                    }
                }
                for (String entryHex : uniqueCallers) {
                    Address entry = toAddr(entryHex);
                    Function caller = currentProgram.getFunctionManager().getFunctionAt(entry);
                    if (caller == null) continue;
                    xout.println();
                    xout.println("CALLER_FUNCTION\t" + caller.getName() + "\t" + hex(caller.getEntryPoint()) +
                        "\t" + hex(caller.getBody().getMinAddress()) + "\t" + hex(caller.getBody().getMaxAddress()));
                    InstructionIterator it = currentProgram.getListing().getInstructions(caller.getBody(), true);
                    while (it.hasNext()) {
                        Instruction ins = it.next();
                        xout.printf("INS\t%s\t%s\t%s\t%s%n", hex(ins.getAddress()), bytes(ins.getBytes()),
                            ins.toString().replace('\t',' '), ins.getFlowType());
                    }
                }
            }
            println("HELPER_XREF_OUTPUT=" + xf.getAbsolutePath() + " callers=" + uniqueCallers.size());
        }
        println("W3_DISASSEMBLY_OUTPUT=" + output.getAbsolutePath());
    }
}