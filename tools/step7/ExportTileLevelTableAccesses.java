// Export decoded memory instructions accessing tile level-table fields +0x10..+0x18.
// Deliberately does not inspect +0xEA8 or +0x1A.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.*;

public class ExportTileLevelTableAccesses extends GhidraScript {
    private static final Set<Long> FIELDS = new HashSet<>(Arrays.asList(0x10L,0x12L,0x14L,0x16L,0x18L));
    private static final Pattern MEM = Pattern.compile("(?i)(-?0x[0-9a-f]+|-?[0-9]+)\\s*\\(\\s*([a-z0-9]+)\\s*\\)");
    private PrintWriter out;
    private final Map<String,Integer> totals = new TreeMap<>();

    private String hx(long v) { return String.format("0x%08X",v & 0xffffffffL); }
    private String clean(String s) { return s==null?"":s.replace('\t',' ').replace('\n',' ').replace('\r',' '); }
    private String bytes(Instruction i) {
        try {
            byte[] b=new byte[i.getLength()];
            currentProgram.getMemory().getBytes(i.getAddress(),b);
            StringBuilder s=new StringBuilder();
            for(byte x:b){if(s.length()>0)s.append(' ');s.append(String.format("%02X",x&255));}
            return s.toString();
        } catch(Exception e) { return "UNAVAILABLE"; }
    }
    private List<Instruction> previous(Instruction c,int n) {
        List<Instruction>a=new ArrayList<>();
        Function f=currentProgram.getFunctionManager().getFunctionContaining(c.getAddress());
        Instruction x=c;
        for(int k=0;k<n;k++){
            x=x.getPrevious();
            if(x==null || (f!=null && !f.getBody().contains(x.getAddress()))) break;
            a.add(x);
        }
        Collections.reverse(a);
        return a;
    }
    private String pre12(List<Instruction>a) {
        StringBuilder s=new StringBuilder();
        for(Instruction i:a){
            if(s.length()>0)s.append(" || ");
            s.append(hx(i.getAddress().getOffset())).append(" ").append(i.toString()).append(" [").append(bytes(i)).append("]");
        }
        return s.toString();
    }
    private String excerpt64(List<Instruction>a,Instruction current) {
        List<Instruction> all=new ArrayList<>(a); all.add(current);
        StringBuilder s=new StringBuilder(); int count=0;
        for(Instruction i:all){
            String b=bytes(i);
            if("UNAVAILABLE".equals(b))continue;
            for(String x:b.split(" ")){
                if(count>=64)return s.toString().trim();
                if(s.length()>0)s.append(' ');
                s.append(x); count++;
            }
        }
        return s.toString().trim();
    }
    private void row(String...c){for(int i=0;i<c.length;i++){if(i>0)out.print('\t');out.print(clean(c[i]));}out.println();}

    @Override protected void run() throws Exception {
        String[] args=getScriptArgs();
        if(args.length<1)throw new IllegalArgumentException("Args: output TSV");
        try(PrintWriter w=new PrintWriter(new BufferedWriter(new OutputStreamWriter(new FileOutputStream(args[0]),StandardCharsets.UTF_8)))){
            out=w;
            row("image","pc","function_entry","function_name","field_offset","mnemonic",
                "base_register","value_or_destination_register","access","instruction",
                "instruction_bytes","previous_12_instructions_with_bytes","raw_excerpt_bytes_le_max_64");
            InstructionIterator it=currentProgram.getListing().getInstructions(true);
            while(it.hasNext()){
                Instruction ins=it.next();
                String mn=ins.getMnemonicString().toLowerCase();
                String kind=(mn.equals("sb")||mn.equals("sh")||mn.equals("sw"))?"WRITE":
                    (mn.equals("lb")||mn.equals("lbu")||mn.equals("lh")||mn.equals("lhu")||mn.equals("lw"))?"READ":"";
                if(kind.isEmpty())continue;
                Matcher mm=MEM.matcher(ins.toString());
                if(!mm.find())continue;
                long off;
                try{off=Long.decode(mm.group(1));}catch(Exception e){continue;}
                if(!FIELDS.contains(off))continue;
                String base=mm.group(2);
                String dataReg=ins.toString().trim().split("\\s+",2).length>1?
                    ins.toString().trim().split("\\s+",2)[1].split(",")[0]:"TIDAK_TAHU";
                Function f=currentProgram.getFunctionManager().getFunctionContaining(ins.getAddress());
                List<Instruction> pre=previous(ins,12);
                row(currentProgram.getName(),hx(ins.getAddress().getOffset()),
                    f==null?"TIDAK_TAHU":hx(f.getEntryPoint().getOffset()),
                    f==null?"TIDAK_TAHU":f.getName(),String.format("+0x%02X",off),mn,
                    base,dataReg,kind,ins.toString(),bytes(ins),pre12(pre),excerpt64(pre,ins));
                String key=String.format("%s|+0x%02X|%s",currentProgram.getName(),off,kind);
                totals.put(key,totals.getOrDefault(key,0)+1);
            }
            out.println("META\tTOTALS");
            for(Map.Entry<String,Integer> e:totals.entrySet())
                row("META",e.getKey(),Integer.toString(e.getValue()));
            out.flush();
            if(out.checkError())throw new IllegalStateException("write failed");
        }
    }
}
