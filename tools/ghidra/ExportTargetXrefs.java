// ExportTargetXrefs.java
// Export exact Ghidra references to a numeric address and the function index.
// Arguments: xrefCsv functionsCsv entryBase targetAddress
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.File;
import java.io.PrintWriter;

public class ExportTargetXrefs extends GhidraScript {
    private String csv(String s) {
        if (s == null) return "";
        return "\"" + s.replace("\"", "\"\"").replace("\n", " ").replace("\r", " ") + "\"";
    }
    private String hex(long v) { return String.format("0x%08X", v); }
    private String bytes(byte[] b) {
        StringBuilder sb = new StringBuilder();
        for (int i=0;i<b.length;i++) {
            if (i>0) sb.append(' ');
            sb.append(String.format("%02X", b[i] & 0xff));
        }
        return sb.toString();
    }
    @Override
    protected void run() throws Exception {
        String[] a = getScriptArgs();
        if (a.length < 4) throw new IllegalArgumentException("args: xrefCsv functionsCsv entryBase targetAddress");
        File xrefFile = new File(a[0]);
        File functionFile = new File(a[1]);
        Address entryBase = toAddr(a[2]);
        Address target = toAddr(a[3]);
        xrefFile.getParentFile().mkdirs();
        functionFile.getParentFile().mkdirs();
        long end = entryBase.getOffset() + 0x919BCL;
        println("EXPORT_TARGET_XREFS base=" + entryBase + " target=" + target);
        println("program=" + currentProgram.getName());
        println("target_inside_imported_entry1=" + currentProgram.getMemory().contains(target));
        try (PrintWriter out = new PrintWriter(xrefFile, "UTF-8")) {
            out.println("target_address,from_address,entry1_file_offset,reference_type,reference_source,instruction_bytes,instruction_mnemonic,containing_function,function_entry");
            ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(target);
            int count = 0;
            while (refs.hasNext()) {
                Reference r = refs.next();
                Address from = r.getFromAddress();
                Instruction ins = currentProgram.getListing().getInstructionAt(from);
                Function f = currentProgram.getFunctionManager().getFunctionContaining(from);
                String off = "";
                if (from.getOffset() >= entryBase.getOffset() && from.getOffset() < end) {
                    off = String.format("0x%06X", from.getOffset() - entryBase.getOffset());
                }
                String b = ins == null ? "" : bytes(ins.getBytes());
                String m = ins == null ? "NO_INSTRUCTION" : ins.toString();
                out.println(csv(hex(target.getOffset())) + "," + csv(hex(from.getOffset())) + "," +
                    csv(off) + "," + csv(r.getReferenceType().toString()) + "," +
                    csv(r.getSource().toString()) + "," + csv(b) + "," + csv(m) + "," +
                    csv(f == null ? "NONE" : f.getName()) + "," +
                    csv(f == null ? "NONE" : hex(f.getEntryPoint().getOffset())));
                count++;
            }
            println("TARGET_XREF_COUNT=" + count);
        }
        byte[] raw = new byte[4];
        String targetBytes = "UNMAPPED";
        String targetU32 = "UNMAPPED";
        if (currentProgram.getMemory().contains(target)) {
            currentProgram.getMemory().getBytes(target, raw);
            targetBytes = bytes(raw);
            long value = ((long)(raw[0]&0xff)) | ((long)(raw[1]&0xff)<<8) |
                ((long)(raw[2]&0xff)<<16) | ((long)(raw[3]&0xff)<<24);
            targetU32 = hex(value);
        }
        println("TARGET_SLOT_BYTES=" + targetBytes);
        println("TARGET_SLOT_U32_LE=" + targetU32);
        try (PrintWriter out = new PrintWriter(functionFile, "UTF-8")) {
            out.println("function_name,start_address,end_address,entry1_file_offset,end_entry1_file_offset,body_address_count");
            FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
            int n=0;
            while (it.hasNext()) {
                Function f=it.next();
                long s=f.getEntryPoint().getOffset();
                long e=f.getBody().getMaxAddress().getOffset();
                if (s < entryBase.getOffset() || s >= end) continue;
                String so=String.format("0x%06X",s-entryBase.getOffset());
                String eo=(e>=entryBase.getOffset() && e<end)?String.format("0x%06X",e-entryBase.getOffset()):"";
                out.println(csv(f.getName()) + "," + csv(hex(s)) + "," + csv(hex(e)) + "," +
                    csv(so) + "," + csv(eo) + "," + f.getBody().getNumAddresses());
                n++;
            }
            println("FUNCTIONS_IN_ENTRY1=" + n);
        }
    }
}
