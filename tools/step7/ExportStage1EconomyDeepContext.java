// ExportStage1EconomyDeepContext.java — static Ghidra evidence for AS1/AS2.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.*;

public class ExportStage1EconomyDeepContext extends GhidraScript {
 private PrintWriter out;
 private static final long RECORD=0x8013EA84L, PARTICIPANT=0x8013EA74L, MANAGER=0x8013A554L;
 private static final long[] HELPERS={0x800B770CL,0x800BDC4CL};
 private static final int[] FIELDS={0x00,0x0B,0x20};
 private static final Pattern MEM=Pattern.compile("(?i)(0x[0-9a-f]+|[0-9a-f]+)\\s*\\(\\s*[a-z0-9]+\\s*\\)");
 private final Map<String,Function> recordFns=new TreeMap<>(),participantFns=new TreeMap<>(),managerFns=new TreeMap<>(),helperFns=new TreeMap<>(),dumped=new TreeMap<>();
 private int setterCalls=0,getterCalls=0,fieldFnCount=0;
 private String hx(long v){return String.format("0x%08X",v&0xffffffffL);}
 private String clean(String s){return s==null?"":s.replace('\t',' ').replace('\n',' ').replace('\r',' ');}
 private void row(String... c){for(int i=0;i<c.length;i++){if(i>0)out.print('\t');out.print(clean(c[i]));}out.println();}
 private String fe(Function f){return f==null?"TIDAK_TAHU":hx(f.getEntryPoint().getOffset());}
 private String fnm(Function f){return f==null?"TIDAK_TAHU":f.getName();}
 private String bytes(Instruction i){try{byte[] b=new byte[i.getLength()];currentProgram.getMemory().getBytes(i.getAddress(),b);StringBuilder s=new StringBuilder();for(byte x:b){if(s.length()>0)s.append(' ');s.append(String.format("%02X",x&255));}return s.toString();}catch(Exception e){return "UNAVAILABLE";}}
 private Function fn(Instruction i){return currentProgram.getFunctionManager().getFunctionContaining(i.getAddress());}
 private long jalTarget(Instruction i)throws Exception{byte[] b=new byte[4];currentProgram.getMemory().getBytes(i.getAddress(),b);long w=((long)b[0]&255)|(((long)b[1]&255)<<8)|(((long)b[2]&255)<<16)|(((long)b[3]&255)<<24);if((w>>>26)!=3)return -1;long pc=i.getAddress().getOffset();return (((pc+4)&0xF0000000L)|((w&0x03ffffffL)<<2))&0xffffffffL;}
 private void collect(long a,Map<String,Function> into)throws Exception{
  ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(toAddr(a));
  while(refs.hasNext()){Function f=currentProgram.getFunctionManager().getFunctionContaining(refs.next().getFromAddress());if(f!=null)into.put(f.getEntryPoint().toString(),f);}
  InstructionIterator it=currentProgram.getListing().getInstructions(true);String token=String.format("%08x",a);
  while(it.hasNext()){Instruction i=it.next();if(i.toString().toLowerCase().contains(token)){Function f=fn(i);if(f!=null)into.put(f.getEntryPoint().toString(),f);}}
 }
 private int disp(Instruction i){Matcher m=MEM.matcher(i.toString());while(m.find()){try{String s=m.group(1).toLowerCase();return (int)Long.parseLong(s.startsWith("0x")?s.substring(2):s,16);}catch(Exception ignored){}}return Integer.MIN_VALUE;}
 private boolean hasField(Function f){if(f==null)return false;InstructionIterator it=currentProgram.getListing().getInstructions(f.getBody(),true);while(it.hasNext()){int d=disp(it.next());for(int x:FIELDS)if(d==x)return true;}return false;}
 private void collectHelpers()throws Exception{InstructionIterator it=currentProgram.getListing().getInstructions(true);while(it.hasNext()){Instruction i=it.next();if(!"jal".equalsIgnoreCase(i.getMnemonicString()))continue;long t=jalTarget(i);for(long h:HELPERS)if(t==h){Function f=fn(i);if(f!=null)helperFns.put(f.getEntryPoint().toString(),f);}}}
 private String before(Instruction c,int n){List<Instruction>a=new ArrayList<>();Instruction x=c;Function owner=fn(c);for(int i=0;i<n;i++){x=x.getPrevious();if(x==null||(owner!=null&&!owner.getBody().contains(x.getAddress())))break;a.add(x);}Collections.reverse(a);StringBuilder b=new StringBuilder();if(a.size()!=n)b.append("PRECALL_COUNT=").append(a.size()).append("; ");for(Instruction i:a){if(b.length()>0&&b.charAt(b.length()-1)!=' ')b.append(" || ");b.append(hx(i.getAddress().getOffset())).append(" ").append(i).append(" [").append(bytes(i)).append("]");}return b.toString();}
 private String after(Instruction c,int n){Instruction x=c.getNext();if(x!=null)x=x.getNext();Function owner=fn(c);StringBuilder b=new StringBuilder();int count=0;while(x!=null&&count<n&&(owner==null||owner.getBody().contains(x.getAddress()))){if(b.length()>0)b.append(" || ");b.append(hx(x.getAddress().getOffset())).append(" ").append(x).append(" [").append(bytes(x)).append("]");x=x.getNext();count++;}if(count<n){if(b.length()>0)b.append(" || ");b.append("POSTRETURN_COUNT=").append(count);}return b.toString();}
 private void dump(Function f,String why)throws Exception{if(f==null)return;String k=f.getEntryPoint().toString();if(dumped.containsKey(k))return;dumped.put(k,f);row("FUNCTION_BEGIN",why,fe(f),fnm(f),"body_bytes="+f.getBody().getNumAddresses());InstructionIterator it=currentProgram.getListing().getInstructions(f.getBody(),true);int n=0;while(it.hasNext()&&n<3000){Instruction i=it.next();row("INSN",why,fe(f),hx(i.getAddress().getOffset()),bytes(i),i.getMnemonicString(),i.toString());n++;}if(it.hasNext())row("FUNCTION_TRUNCATED",why,fe(f),fnm(f),"limit=3000");row("FUNCTION_END",why,fe(f),fnm(f),"instructions="+n);}
 private void fieldFunctions()throws Exception{Map<String,Function> scope=new TreeMap<>();scope.putAll(recordFns);scope.putAll(helperFns);for(long h:HELPERS){Function f=currentProgram.getFunctionManager().getFunctionAt(toAddr(h));if(f!=null)scope.put(f.getEntryPoint().toString(),f);}for(Function f:scope.values())if(hasField(f)){boolean r=recordFns.containsKey(f.getEntryPoint().toString());row("FIELD_SCOPE_FUNCTION",r?"FUNCTION_XREF_RECORD_SLOT":"HELPER_OR_CALLER_SCOPE",fe(f),fnm(f),"HAS_DISP_00_0B_20");fieldFnCount++;}}
 private void contexts()throws Exception{InstructionIterator it=currentProgram.getListing().getInstructions(true);while(it.hasNext()){Instruction i=it.next();if(!"jal".equalsIgnoreCase(i.getMnemonicString()))continue;long t=jalTarget(i);if(t!=0x8001387CL&&t!=0x800138ECL)continue;Function f=fn(i);String kind=t==0x8001387CL?"SETTER_8001387C":"GETTER_800138EC";if(t==0x8001387CL)setterCalls++;else getterCalls++;Instruction d=i.getNext();row("CALL_CONTEXT",kind,hx(t),hx(i.getAddress().getOffset()),fe(f),fnm(f),before(i,12),d==null?"TIDAK_TAHU":hx(d.getAddress().getOffset())+" "+d+" ["+bytes(d)+"]",after(i,18),"12 pre-jal instructions; delay slot; return starts jal+8");dump(f,kind);}Function f=currentProgram.getFunctionManager().getFunctionAt(toAddr(0x801052E8L));if(f!=null)dump(f,"GETTER_CALLER_ENTRY_0x801052E8");}
 @Override protected void run()throws Exception{
  String[] a=getScriptArgs();if(a.length<1)throw new IllegalArgumentException("Args: output TSV");
  collect(RECORD,recordFns);collect(PARTICIPANT,participantFns);collect(MANAGER,managerFns);collectHelpers();
  try(PrintWriter w=new PrintWriter(new BufferedWriter(new OutputStreamWriter(new FileOutputStream(a[0]),StandardCharsets.UTF_8)))){
   out=w;row("record_type","scope_or_target","address","function_entry","function_name","context_before_or_detail","delay_slot","postreturn_context","notes");
   row("META","RECORD_SLOT",hx(RECORD),"TIDAK_TAHU","TIDAK_TAHU","recordFns_count="+recordFns.size(),"PARTICIPANT_SLOT="+hx(PARTICIPANT),"MANAGER_SLOT="+hx(MANAGER),"same Ghidra ref/token collection logic as AQ1 exporter");
   row("META","HELPER_CALLER_FUNCTIONS","","","","count="+helperFns.size(),"helper_targets=0x800B770C;0x800BDC4C","","");
   for(Function f:recordFns.values())row("RECORD_XREF_FUNCTION","FUNCTION_XREF_RECORD_SLOT",fe(f),fe(f),fnm(f),"recordFns metadata membership","","","direct ref or operand-token match");
   fieldFunctions();row("FIELD_SCOPE_TOTAL","DISTINCT_FUNCTIONS","","","","count="+fieldFnCount,"census should contain 93+4 functions","","");
   contexts();row("CALL_CONTEXT_TOTAL","DIRECT_JAL","","","","setter_calls="+setterCalls,"getter_calls="+getterCalls,"","JALR not covered");
   out.flush();if(out.checkError())throw new IllegalStateException("AS1/AS2 export failed");
  }
 }
}
