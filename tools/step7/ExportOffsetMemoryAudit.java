// Export decoded memory accesses at raw offsets +0xEA8 and tile-field +0x1A.
// The companion Python script independently scans the raw EXE and Entry-1 bytes.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.address.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.*;

public class ExportOffsetMemoryAudit extends GhidraScript {
    private static final Pattern MEM = Pattern.compile("(?i)(-?0x[0-9a-f]+|-?[0-9]+)\\s*\\(\\s*([a-z0-9]+)\\s*\\)");
    private static final Pattern STORE = Pattern.compile("(?i)^_?(sb|sh|sw)\\s+([a-z0-9]+)\\s*,");
    private static final Pattern DEF = Pattern.compile("(?i)^_?(li|lui|move|addu|addiu|subu|ori|andi|lw|lbu|lhu|lh|lb|sll|srl|sra|or|and|nor|xor|slti|sltiu|mflo|mfhi)\\s+([a-z0-9]+)\\s*,\\s*(.*)$");
    private PrintWriter out;
    private int ea8W=0, ea8R=0, oneAW=0, oneAR=0;

    private String hx(long v) { return String.format("0x%08X", v & 0xffffffffL); }
    private String clean(String s) { return s==null ? "" : s.replace('\t',' ').replace('\n',' ').replace('\r',' '); }
    private String bytes(Instruction i) {
        try {
            byte[] b = new byte[i.getLength()];
            currentProgram.getMemory().getBytes(i.getAddress(), b);
            StringBuilder s = new StringBuilder();
            for (byte x : b) { if (s.length()>0) s.append(' '); s.append(String.format("%02X",x&255)); }
            return s.toString();
        } catch (Exception e) { return "UNAVAILABLE"; }
    }
    private List<Instruction> previous(Instruction c, int n) {
        List<Instruction> a = new ArrayList<>();
        Function f = currentProgram.getFunctionManager().getFunctionContaining(c.getAddress());
        Instruction x = c;
        for (int k=0;k<n;k++) {
            x = x.getPrevious();
            if (x==null || (f!=null && !f.getBody().contains(x.getAddress()))) break;
            a.add(x);
        }
        Collections.reverse(a);
        return a;
    }
    private String regDefTrace(String reg, List<Instruction> prior, int depth) {
        if (depth>3) return reg+" provenance depth limit";
        for (int k=prior.size()-1;k>=0;k--) {
            String t=prior.get(k).toString().trim();
            Matcher m=DEF.matcher(t);
            if (!m.find() || !reg.equalsIgnoreCase(m.group(2))) continue;
            String op=m.group(1).toLowerCase(), args=m.group(3).trim();
            String result=hx(prior.get(k).getAddress().getOffset())+" "+t+" ["+bytes(prior.get(k))+"]";
            if (op.equals("lui") || op.equals("li")) return result+"; immediate source";
            Matcher mm=MEM.matcher(args);
            if (mm.find()) {
                String base=mm.group(2);
                String imm=mm.group(1);
                String child=regDefTrace(base,prior.subList(0,k),depth+1);
                String suffix="";
                try {
                    long d=Long.decode(imm);
                    if (child.toLowerCase().contains("lui") && child.matches("(?s).*0x8014.*") && d==-0x5dd4L)
                        suffix="; effective source address=0x8013A22C (global pointer slot); loaded value is pointer";
                } catch(Exception ignored) {}
                return result+"; base provenance: "+child+suffix;
            }
            Matcher src=Pattern.compile("^([a-z0-9]+)").matcher(args);
            if (src.find() && !op.equals("li") && !op.equals("lui")) {
                String sreg=src.group(1);
                if (!sreg.equalsIgnoreCase(reg) && !sreg.matches("[0-9]+"))
                    return result+"; input provenance: "+regDefTrace(sreg,prior.subList(0,k),depth+1);
            }
            return result;
        }
        return "TIDAK TAHU (no local definition in preceding window for "+reg+")";
    }
    private String formatPre(List<Instruction> a) {
        StringBuilder s=new StringBuilder();
        if (a.size()!=12) s.append("PRE12_COUNT=").append(a.size()).append("; ");
        for (Instruction i:a) {
            if (s.length()>0 && s.charAt(s.length()-1)!=' ') s.append(" || ");
            s.append(hx(i.getAddress().getOffset())).append(" ").append(i.toString()).append(" [").append(bytes(i)).append("]");
        }
        return s.toString();
    }
    private String excerpt64(List<Instruction> a, Instruction store) {
        StringBuilder s=new StringBuilder(); int count=0;
        List<Instruction> all=new ArrayList<>(a); all.add(store);
        for(Instruction i:all) {
            String b=bytes(i);
            if("UNAVAILABLE".equals(b)) continue;
            for(String x:b.split(" ")) {
                if(count>=64) return s.toString().trim();
                if(s.length()>0) s.append(' ');
                s.append(x); count++;
            }
        }
        return s.toString().trim();
    }
    private void row(String... c) { for(int i=0;i<c.length;i++){if(i>0)out.print('\t');out.print(clean(c[i]));}out.println(); }

    @Override protected void run() throws Exception {
        String[] args=getScriptArgs();
        if(args.length<1) throw new IllegalArgumentException("Args: output TSV");
        try(PrintWriter w=new PrintWriter(new BufferedWriter(new OutputStreamWriter(new FileOutputStream(args[0]),StandardCharsets.UTF_8)))) {
            out=w;
            row("image","record_type","pc","function_entry","function_name","field_offset","mnemonic","base_register",
                "stored_or_loaded_register","access","instruction","instruction_bytes","base_register_origin",
                "stored_value_origin","pre12_instructions_full","raw_excerpt_bytes_le_64");
            InstructionIterator it=currentProgram.getListing().getInstructions(true);
            while(it.hasNext()) {
                Instruction ins=it.next();
                String mn=ins.getMnemonicString().toLowerCase();
                String kind=(mn.equals("sb")||mn.equals("sh")||mn.equals("sw"))?"WRITE":
                    (mn.equals("lb")||mn.equals("lbu")||mn.equals("lh")||mn.equals("lhu")||mn.equals("lw"))?"READ":"";
                if(kind.isEmpty()) continue;
                Matcher mm=MEM.matcher(ins.toString());
                if(!mm.find()) continue;
                long off;
                try { off=Long.decode(mm.group(1)); } catch(Exception e) { continue; }
                if(off!=0xEA8L && off!=0x1AL) continue;
                String base=mm.group(2);
                Matcher sm=STORE.matcher(ins.toString());
                String dataReg=sm.find()?sm.group(2):ins.toString().trim().split("\\s+",2).length>1?
                    ins.toString().trim().split("\\s+",2)[1].split(",")[0]:"TIDAK_TAHU";
                Function f=currentProgram.getFunctionManager().getFunctionContaining(ins.getAddress());
                List<Instruction> pre=previous(ins,12);
                String baseTrace=regDefTrace(base,pre,0);
                String valueTrace=kind.equals("WRITE")?regDefTrace(dataReg,pre,0):"NOT_APPLICABLE_READ";
                row(currentProgram.getName(), "MEMORY_OFFSET_ACCESS", hx(ins.getAddress().getOffset()),
                    f==null?"TIDAK_TAHU":hx(f.getEntryPoint().getOffset()),
                    f==null?"TIDAK_TAHU":f.getName(), off==0xEA8L?"+0xEA8":"+0x1A",
                    mn,base,dataReg,kind,ins.toString(),bytes(ins),baseTrace,valueTrace,formatPre(pre),excerpt64(pre,ins));
                if(off==0xEA8L && kind.equals("WRITE")) ea8W++;
                if(off==0xEA8L && kind.equals("READ")) ea8R++;
                if(off==0x1AL && kind.equals("WRITE")) oneAW++;
                if(off==0x1AL && kind.equals("READ")) oneAR++;
            }
            row("META","TOTALS","","","","+0xEA8","WRITE="+ea8W+";READ="+ea8R,"","","","","","","","","");
            row("META","TOTALS","","","","+0x1A","WRITE="+oneAW+";READ="+oneAR,"","","","","","","","","");
            out.flush();
            if(out.checkError()) throw new IllegalStateException("ExportOffsetMemoryAudit output failed");
        }
    }
}
