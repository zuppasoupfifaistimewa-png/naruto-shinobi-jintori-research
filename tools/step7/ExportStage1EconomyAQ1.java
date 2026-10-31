// ExportStage1EconomyAQ1.java
// AQ1 bounded static census. Entry 1 import base is a candidate, not runtime proof.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.*;

public class ExportStage1EconomyAQ1 extends GhidraScript {
    private PrintWriter out;
    private static final long TABLE=0x800AD5F4L, RECORD=0x8013EA84L, PARTICIPANT=0x8013EA74L, MANAGER=0x8013A554L;
    private static final long[] HELPERS={0x800B770CL,0x800BDC4CL}, ACCESSORS={0x8001387CL,0x800138ECL};
    private static final int[] FIELDS={0x00,0x0B,0x20};
    private static final Pattern MEM=Pattern.compile("(?i)(0x[0-9a-f]+|[0-9a-f]+)\\s*\\(\\s*[a-z0-9]+\\s*\\)");
    private final Map<String,Function> recordFns=new TreeMap<>(), participantFns=new TreeMap<>(), managerFns=new TreeMap<>();
    private final Set<Function> helperCallerFns=new LinkedHashSet<>();
    private int jumps=0, fields=0, helperCalls=0, accessorCalls=0;

    private String hx(long v){return String.format("0x%08X",v&0xffffffffL);}
    private String clean(String s){return s==null?"":s.replace('\t',' ').replace('\n',' ').replace('\r',' ');}
    private void row(String... c){for(int i=0;i<c.length;i++){if(i>0)out.print('\t');out.print(clean(c[i]));}out.println();}
    private long u32(long a)throws Exception{byte[] b=new byte[4];currentProgram.getMemory().getBytes(toAddr(a),b);return ((long)b[0]&255)|(((long)b[1]&255)<<8)|(((long)b[2]&255)<<16)|(((long)b[3]&255)<<24);}
    private String bytes(Instruction ins){try{byte[] b=new byte[ins.getLength()];currentProgram.getMemory().getBytes(ins.getAddress(),b);StringBuilder s=new StringBuilder();for(byte v:b){if(s.length()>0)s.append(' ');s.append(String.format("%02X",v&255));}return s.toString();}catch(Exception e){return "UNAVAILABLE";}}
    private String excerpt(long a,int max){try{byte[] b=new byte[max];int n=currentProgram.getMemory().getBytes(toAddr(a),b);StringBuilder s=new StringBuilder();for(int i=0;i<n;i++){if(i>0)s.append(' ');s.append(String.format("%02X",b[i]&255));}return s.toString();}catch(Exception e){return "UNAVAILABLE";}}
    private long jalTarget(Instruction ins)throws Exception{byte[] b=new byte[4];currentProgram.getMemory().getBytes(ins.getAddress(),b);long w=((long)b[0]&255)|(((long)b[1]&255)<<8)|(((long)b[2]&255)<<16)|(((long)b[3]&255)<<24);if((w>>>26)!=3)return -1;long pc=ins.getAddress().getOffset();return (((pc+4)&0xF0000000L)|((w&0x03ffffffL)<<2))&0xffffffffL;}
    private Function fn(Instruction i){return currentProgram.getFunctionManager().getFunctionContaining(i.getAddress());}
    private String fe(Function f){return f==null?"TIDAK_TAHU":hx(f.getEntryPoint().getOffset());}
    private String fnm(Function f){return f==null?"TIDAK_TAHU":f.getName();}
    private void collect(long addr,Map<String,Function> into)throws Exception{
        ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(toAddr(addr));
        while(refs.hasNext()){Function f=currentProgram.getFunctionManager().getFunctionContaining(refs.next().getFromAddress());if(f!=null)into.put(f.getEntryPoint().toString(),f);}
        InstructionIterator it=currentProgram.getListing().getInstructions(true);String token=String.format("%08x",addr);
        while(it.hasNext()){Instruction i=it.next();if(i.toString().toLowerCase().contains(token)){Function f=fn(i);if(f!=null)into.put(f.getEntryPoint().toString(),f);}}
    }
    private int disp(Instruction i){Matcher m=MEM.matcher(i.toString());while(m.find()){try{String s=m.group(1).toLowerCase();return (int)Long.parseLong(s.startsWith("0x")?s.substring(2):s,16);}catch(Exception ignored){}}return Integer.MIN_VALUE;}
    private boolean load(String m){return m.startsWith("lb")||m.startsWith("lh")||m.startsWith("lw")||m.startsWith("ld");}
    private boolean store(String m){return m.startsWith("sb")||m.startsWith("sh")||m.startsWith("sw")||m.startsWith("sd");}
    private boolean hasDisp(Function f,int d){if(f==null)return false;InstructionIterator it=currentProgram.getListing().getInstructions(f.getBody(),true);while(it.hasNext())if(disp(it.next())==d)return true;return false;}
    private boolean has(Map<String,Function> m,Function f){return f!=null&&m.containsKey(f.getEntryPoint().toString());}
    private String group(Function f){List<String> g=new ArrayList<>();if(has(recordFns,f))g.add("RECORD_0x8013EA84");if(has(managerFns,f)&&hasDisp(f,0xB44))g.add("MANAGER_+0xB44");if(has(participantFns,f)&&hasDisp(f,0x2EE))g.add("PARTICIPANT_+0x2EE");return g.isEmpty()?"UNCLASSIFIED_DIRECT_CALLER":String.join("+",g);}

    private void jumpTable()throws Exception{
        for(int n=0;n<5;n++){long slot=TABLE+4L*n;try{long target=u32(slot);Function f=currentProgram.getFunctionManager().getFunctionContaining(toAddr(target));String ex=excerpt(target,64);int length=ex.equals("UNAVAILABLE")||ex.isEmpty()?0:ex.split(" ").length;row("JUMP",String.valueOf(n),hx(slot),hx(target),hx(target),fe(f),fnm(f),ex,String.valueOf(length),"branch-target excerpt capped at 64 bytes");jumps++;}catch(Exception e){row("JUMP",String.valueOf(n),hx(slot),"TIDAK_TAHU","TIDAK_TAHU","TIDAK_TAHU","TIDAK_TAHU","UNAVAILABLE","0","TABLE_READ_FAIL");}}
    }
    private void fieldAccesses()throws Exception{
        Map<String,Function> scope=new TreeMap<>();scope.putAll(recordFns);
        for(Function f:helperCallerFns)if(f!=null)scope.put(f.getEntryPoint().toString(),f);
        for(long a:HELPERS){Function f=currentProgram.getFunctionManager().getFunctionAt(toAddr(a));if(f!=null)scope.put(f.getEntryPoint().toString(),f);}
        for(Function f:scope.values()){InstructionIterator it=currentProgram.getListing().getInstructions(f.getBody(),true);while(it.hasNext()){
            Instruction i=it.next();int d=disp(i);boolean valid=false;for(int x:FIELDS)if(d==x)valid=true;if(!valid)continue;
            String mn=i.getMnemonicString().toLowerCase(),kind=load(mn)?"READ":store(mn)?"WRITE":"OTHER";
            String basis=has(recordFns,f)?"FUNCTION_XREF_RECORD_SLOT":"HELPER_OR_CALLER_SCOPE";
            row("FIELD",String.format("+0x%02X",d),kind,hx(i.getAddress().getOffset()),fe(f),fnm(f),bytes(i),i.toString(),basis,"displacement candidate; base-register alias is not proven");
            fields++;
        }}
    }
    private void calls()throws Exception{
        InstructionIterator it=currentProgram.getListing().getInstructions(true);
        while(it.hasNext()){Instruction i=it.next();if(!"jal".equalsIgnoreCase(i.getMnemonicString()))continue;long t=jalTarget(i);if(t<0)continue;
            boolean h=false,a=false;for(long x:HELPERS)if(t==x)h=true;for(long x:ACCESSORS)if(t==x)a=true;if(!h&&!a)continue;
            Function f=fn(i);if(h){helperCalls++;if(f!=null)helperCallerFns.add(f);}
            if(a)accessorCalls++;
            row(h?"HELPER_CALL":"ACCESSOR_CALL",hx(t),hx(i.getAddress().getOffset()),fe(f),fnm(f),bytes(i),i.toString(),a?group(f):"DIRECT_HELPER_CALL","direct JAL site; indirect JALR unresolved");
        }
    }
    @Override protected void run()throws Exception{
        String[] args=getScriptArgs();if(args.length<1)throw new IllegalArgumentException("Args: output TSV path");
        collect(RECORD,recordFns);collect(PARTICIPANT,participantFns);collect(MANAGER,managerFns);
        try(PrintWriter w=new PrintWriter(new BufferedWriter(new OutputStreamWriter(new FileOutputStream(args[0]),StandardCharsets.UTF_8)))){
            out=w;
            row("record_type","item","kind","pc_or_target","function_entry","function_name","bytes_or_excerpt_hex","instruction_or_context","scope_or_group","notes");
            row("META","Entry1","STATIC","0x800AD450","runtime_mapping=NOT_VALIDATED","slice=0x10BB000/596412","sha256=9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a","static-only","no gameplay/runtime","candidate import base");
            jumpTable();calls();fieldAccesses();
            row("TOTAL","jump_rows",String.valueOf(jumps),"field_access_rows",String.valueOf(fields),"helper_call_sites",String.valueOf(helperCalls),"accessor_call_sites",String.valueOf(accessorCalls),"record_slot_xref_function_count",String.valueOf(recordFns.size()),"JALR=TIDAK_TAHU");
            row("LIMIT","field offset scan only","function scope = record-slot xrefs + helper functions/callers","no computed alias proof","no semantic names assigned","direct callers only; unresolved indirect control flow");
            out.flush();if(out.checkError())throw new IllegalStateException("AQ1 TSV write failure");
        }
    }
}