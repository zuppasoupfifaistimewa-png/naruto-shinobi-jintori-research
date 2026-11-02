// ExportBB2TileNibbleAudit.java
// Static, exhaustive displacement audit for candidate tile fields +0x20 and +0x0B.
// It records 12 instructions before/after every access and a raw excerpt <=64 bytes.
// Nibble labels are inferred only from immediately adjacent shifts/masks; base alias to
// the runtime tile pointer is NOT presumed from displacement alone.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.*;

public class ExportBB2TileNibbleAudit extends GhidraScript {
    private static final Pattern MEM = Pattern.compile("(?i)\\b(?:0x)?0*(20|b)\\s*\\(\\s*([a-z0-9]+)\\s*\\)");
    private static final Pattern SHIFT = Pattern.compile("(?i)^_?srl\\s+([a-z0-9]+)\\s*,\\s*([a-z0-9]+)\\s*,\\s*(0x[0-9a-f]+|[0-9]+)");
    private static final Pattern ANDI = Pattern.compile("(?i)^_?andi\\s+([a-z0-9]+)\\s*,\\s*([a-z0-9]+)\\s*,\\s*(0x[0-9a-f]+|[0-9]+)");
    private static final Pattern SLL = Pattern.compile("(?i)^_?sll\\s+([a-z0-9]+)\\s*,\\s*([a-z0-9]+)\\s*,\\s*(0x[0-9a-f]+|[0-9]+)");
    private static final Pattern OR = Pattern.compile("(?i)^_?or\\s+([a-z0-9]+)\\s*,\\s*([a-z0-9]+)\\s*,\\s*([a-z0-9]+)");
    private PrintWriter out;
    private int reads20=0,writes20=0,other20=0,reads0b=0,writes0b=0,other0b=0;

    private String hx(long v){return String.format("0x%08X",v&0xffffffffL);}
    private String clean(String s){return s==null?"":s.replace('\t',' ').replace('\n',' ').replace('\r',' ');}
    private long num(String s){try{return s.toLowerCase().startsWith("0x")?Long.parseLong(s.substring(2),16):Long.parseLong(s);}catch(Exception e){return -1;}}
    private Function owner(Instruction i){return currentProgram.getFunctionManager().getFunctionContaining(i.getAddress());}
    private byte[] raw(Instruction i){
        try{byte[] b=new byte[i.getLength()];currentProgram.getMemory().getBytes(i.getAddress(),b);return b;}
        catch(Exception e){return new byte[0];}
    }
    private String bytes(Instruction i){
        byte[] b=raw(i);StringBuilder s=new StringBuilder();
        for(byte x:b){if(s.length()>0)s.append(' ');s.append(String.format("%02X",x&255));}
        return s.toString();
    }
    private List<Instruction> previous(Instruction c,int n){
        List<Instruction>a=new ArrayList<>();Function f=owner(c);Instruction x=c;
        for(int k=0;k<n;k++){x=x.getPrevious();if(x==null||(f!=null&&!f.getBody().contains(x.getAddress())))break;a.add(x);}
        Collections.reverse(a);return a;
    }
    private List<Instruction> next(Instruction c,int n){
        List<Instruction>a=new ArrayList<>();Function f=owner(c);Instruction x=c;
        for(int k=0;k<n;k++){x=x.getNext();if(x==null||(f!=null&&!f.getBody().contains(x.getAddress())))break;a.add(x);}
        return a;
    }
    private String format(List<Instruction>a){
        StringBuilder b=new StringBuilder();
        for(Instruction i:a){if(b.length()>0)b.append(" || ");b.append(hx(i.getAddress().getOffset())).append(" ").append(i).append(" [").append(bytes(i)).append("]");}
        return b.toString();
    }
    private String excerpt(List<Instruction>pre,Instruction c,List<Instruction>post){
        List<Instruction>all=new ArrayList<>();
        int start=Math.max(0,pre.size()-8);
        all.addAll(pre.subList(start,pre.size()));all.add(c);all.addAll(post.subList(0,Math.min(12,post.size())));
        StringBuilder b=new StringBuilder();int total=0;
        for(Instruction i:all){for(byte x:raw(i)){if(total>=64)return b.toString().trim();if(b.length()>0)b.append(' ');b.append(String.format("%02X",x&255));total++;}}
        return b.toString().trim();
    }
    private String nibbleName(int shift){
        switch(shift){case 0:return "BITS_0_3";case 4:return "BITS_4_7";case 8:return "BITS_8_11";case 12:return "BITS_12_15";default:return "TIDAK_TAHU";}
    }
    private String classify(Instruction ins,List<Instruction>pre,List<Instruction>post,String access,int off){
        if(off==0x0b)return "SELECTOR_BYTE_SEMANTIC_TIDAK_TAHU";
        if("READ".equals(access)){
            // A direct extraction sequence: load, then optional nops, srl #0/4/8/12, andi 0xF.
            for(int i=0;i<Math.min(6,post.size());i++){
                Matcher sm=SHIFT.matcher(post.get(i).toString());
                if(sm.find()){
                    int sh=(int)num(sm.group(3));
                    if(sh==0||sh==4||sh==8||sh==12){
                        for(int k=i+1;k<Math.min(i+4,post.size());k++){
                            Matcher am=ANDI.matcher(post.get(k).toString());
                            if(am.find()&&num(am.group(3))==15)return nibbleName(sh)+"_READ_EXTRACTED";
                        }
                    }
                }
                Matcher am=ANDI.matcher(post.get(i).toString());
                if(am.find()){
                    long mask=num(am.group(3));
                    if(mask==0xf000)return "BITS_12_15_MASK_READ";
                    if(mask==0x0f00)return "BITS_8_11_MASK_READ";
                    if(mask==0x00f0)return "BITS_4_7_MASK_READ";
                    if(mask==0x000f)return "BITS_0_3_MASK_READ";
                }
            }
            return "NIBBLE_NOT_IDENTIFIED_FROM_LOCAL_SEQUENCE";
        }
        if("WRITE".equals(access)){
            // An ANDI with the complement of one nibble immediately before a store identifies it.
            for(int i=pre.size()-1;i>=Math.max(0,pre.size()-12);i--){
                Matcher am=ANDI.matcher(pre.get(i).toString());
                if(am.find()){
                    long mask=num(am.group(3));
                    if(mask==0x0fff)return "BITS_12_15_WRITE_MASK";
                    if(mask==0xf0ff)return "BITS_8_11_WRITE_MASK";
                    if(mask==0xff0f)return "BITS_4_7_WRITE_MASK";
                    if(mask==0xfff0)return "BITS_0_3_WRITE_MASK";
                }
                Matcher sl=SLL.matcher(pre.get(i).toString());
                if(sl.find()){
                    int sh=(int)num(sl.group(3));
                    if(sh==4||sh==8||sh==12){
                        for(int k=i+1;k<pre.size();k++){
                            Matcher om=OR.matcher(pre.get(k).toString());
                            if(om.find())return nibbleName(sh)+"_WRITE_REBUILD";
                        }
                    }
                }
            }
            return "WRITE_NIBBLE_NOT_IDENTIFIED_FROM_LOCAL_SEQUENCE";
        }
        return "OTHER";
    }
    private void row(String...a){for(int i=0;i<a.length;i++){if(i>0)out.print('\t');out.print(clean(a[i]));}out.println();}
    @Override protected void run() throws Exception{
        String[]args=getScriptArgs();if(args.length<1)throw new IllegalArgumentException("Args: output TSV");
        try(PrintWriter w=new PrintWriter(new BufferedWriter(new OutputStreamWriter(new FileOutputStream(args[0]),StandardCharsets.UTF_8)))){
            out=w;
            row("record_type","pc","function_entry","function_name","field_offset","access","base_register","tile_base_alias","nibble_candidate","instruction","instruction_bytes","pre12_instructions","next12_instructions","raw_excerpt_bytes_le_64");
            InstructionIterator it=currentProgram.getListing().getInstructions(true);
            while(it.hasNext()){
                Instruction ins=it.next();Matcher mm=MEM.matcher(ins.toString());if(!mm.find())continue;
                int off=Integer.parseInt(mm.group(1),16);String base=mm.group(2);
                if("sp".equalsIgnoreCase(base))continue;
                String mn=ins.getMnemonicString().toLowerCase();
                String kind=(mn.equals("sb")||mn.equals("sh")||mn.equals("sw")||mn.equals("sd"))?"WRITE":
                    (mn.equals("lb")||mn.equals("lbu")||mn.equals("lh")||mn.equals("lhu")||mn.equals("lw")||mn.equals("ld"))?"READ":"OTHER";
                Function f=owner(ins);
                String entry=f==null?"TIDAK_TAHU":hx(f.getEntryPoint().getOffset());
                String name=f==null?"TIDAK_TAHU":f.getName();
                List<Instruction>pre=previous(ins,12),post=next(ins,12);
                String label=classify(ins,pre,post,kind,off);
                row("FIELD_ACCESS",hx(ins.getAddress().getOffset()),entry,name,off==0x20?"+0x20":"+0x0B",kind,base,
                    "DISPLACEMENT_CANDIDATE_BASE_ALIAS_NOT_PROVEN",label,ins.toString(),bytes(ins),format(pre),format(post),excerpt(pre,ins,post));
                if(off==0x20){if("READ".equals(kind))reads20++;else if("WRITE".equals(kind))writes20++;else other20++;}
                else {if("READ".equals(kind))reads0b++;else if("WRITE".equals(kind))writes0b++;else other0b++;}
            }
            row("META","TOTALS","","","+0x20","READ="+reads20+";WRITE="+writes20+";OTHER="+other20,"","",
                "alias=not proven","","","","","");
            row("META","TOTALS","","","+0x0B","READ="+reads0b+";WRITE="+writes0b+";OTHER="+other0b,"","",
                "alias=not proven","","","","","");
            out.flush();if(out.checkError())throw new IllegalStateException("BB2 tile nibble export failed");
        }
    }
}
