// ExportBA1SelectorMatrix.java
// Static-only reconstruction of FUN_80012EAC's selector lookup:
//   selector = *(u8 *)(0x80058758 + mode*0x84 + state*0x0c)
//   resource = selector + 0x276
// The code does not claim which mode/state is Story Stage 1.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;

public class ExportBA1SelectorMatrix extends GhidraScript {
    private static final long MATRIX = 0x80058758L;
    private static final long CONFIG = 0x80057798L;
    private static final int MODE_COUNT = 256;
    private static final int STATE_COUNT = 11;
    private static final int MODE_STRIDE = 0x84;
    private static final int STATE_STRIDE = 0x0C;
    private static final int CONFIG_STRIDE = 0x54;

    private int u8(long address) throws Exception {
        return currentProgram.getMemory().getByte(toAddr(address)) & 0xff;
    }
    private long u32(long address) throws Exception {
        byte[] b = new byte[4];
        currentProgram.getMemory().getBytes(toAddr(address), b);
        return ((long)b[0]&255L) | (((long)b[1]&255L)<<8) |
               (((long)b[2]&255L)<<16) | (((long)b[3]&255L)<<24);
    }
    private String csv(String s) {
        return "\"" + s.replace("\"", "\"\"") + "\"";
    }
    @Override
    protected void run() throws Exception {
        String[] args=getScriptArgs();
        if(args.length<1) throw new IllegalArgumentException("Args: output TSV path");
        try(PrintWriter out=new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out.println("mode\tstate\tmatrix_address\tconfig_index\tconfig_row_address\tselector_byte\tresource_id_hex\tdata_bin_entry_index\tconfig_b30_u32\tconfig_byte_2e\tstatus");
            Map<Integer,Integer> selectorCounts=new LinkedHashMap<>();
            Map<Integer,Integer> resourceCounts=new LinkedHashMap<>();
            int rows=0, unmapped=0;
            for(int mode=0;mode<MODE_COUNT;mode++) {
                for(int state=0;state<STATE_COUNT;state++) {
                    long ma=MATRIX + (long)mode*MODE_STRIDE + (long)state*STATE_STRIDE;
                    try {
                        int ix=u8(ma);
                        long ca=CONFIG + (long)ix*CONFIG_STRIDE;
                        int selector=u8(ca);
                        long b30=u32(ca+0x0c);
                        int gate=u8(ca+0x2e);
                        int resource=0x276+selector;
                        selectorCounts.put(selector,selectorCounts.getOrDefault(selector,0)+1);
                        resourceCounts.put(resource,resourceCounts.getOrDefault(resource,0)+1);
                        out.println(mode+"\t"+state+"\t0x"+Long.toHexString(ma)+"\t"+ix+
                          "\t0x"+Long.toHexString(ca)+"\t"+selector+
                          "\t0x"+Integer.toHexString(resource)+"\t"+resource+
                          "\t"+b30+"\t"+gate+"\tPASS");
                        rows++;
                    } catch(Exception e) {
                        out.println(mode+"\t"+state+"\t0x"+Long.toHexString(ma)+"\tTIDAK_TAHU\tTIDAK_TAHU\tTIDAK_TAHU\tTIDAK_TAHU\tTIDAK_TAHU\tTIDAK_TAHU\tTIDAK_TAHU\tUNMAPPED");
                        unmapped++;
                    }
                }
            }
            out.println();
            out.println("# SUMMARY");
            out.println("# matrix_rows="+rows);
            out.println("# unmapped_rows="+unmapped);
            for(Map.Entry<Integer,Integer> e:selectorCounts.entrySet())
                out.println("# selector_"+e.getKey()+"_count="+e.getValue()+" resource_id=0x"+Integer.toHexString(0x276+e.getKey()));
            for(Map.Entry<Integer,Integer> e:resourceCounts.entrySet())
                out.println("# resource_"+e.getKey()+"_count="+e.getValue());
            out.flush();
            if(out.checkError()) throw new IllegalStateException("BA1 selector matrix write failed");
        }
    }
}
