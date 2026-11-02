// ExportBB2ActionByteAudit.java
// Exhaustive static scan for MIPS memory operands at displacement +0x2EB in Entry 1.
// Functions referring to participant base global 0x8013EA74 are tagged separately.
// A displacement hit by itself is not treated as proof of the effective base alias.
// For each occurrence, export PC, function, 12 preceding instructions and <=64 raw bytes.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.*;

public class ExportBB2ActionByteAudit extends GhidraScript {
 private static final long PARTICIPANT_SLOT=0x8013EA74L, HANDLER=0x800D15A8L;
 private static final Pattern MEM=Pattern.compile("(?i)(?:0x)?0*2eb\\s*\\(\\s*([a-z0-9]+)\\s*\\)");
 private static final Pattern STORE=Pattern.compile("(?i)^_?(sb|sh|sw|sd)\\s+([a-z0-9]+)\\s*,");
 private static final Pattern LI=Pattern.compile("(?i)^_?li\\s+([a-z0-9]+)\\s*,\\s*(0x[0-9a-f]+|-?[0-9]+)");
 private static final Pattern ADDIU=Pattern.compile("(?i)^_?addiu\\s+([a-z0-9]+)\\s*,\\s*zero\\s*,\\s*(-?[0-9]+)");
 private PrintWriter out;
 private final Map<String,Function> participantFns=new TreeMap<>();
 private int reads=0,writes=0,other=0,inScope=0;

 private String hx(long v){return String.format("0x%08X",v&0xffffffffL);}
 private String clean(String s){return s==null?"":s.replace('\t',' ').replace('\n',' ').replace('\r',' ');}
 private void row(String... c){for(int i=0;i<c.length;i++){if(i>0)out.print('\t');out.print(clean(c[i]));}out.println();}
 private String bytes(Instruction i){
  try{byte[] b=new byte[i.getLength()];currentProgram.getMemory().getBytes(i.getAddress(),b);StringBuilder s=new StringBuilder();for(byte x:b){if(s.length()>0)s.append(' ');s.append(String.format("%02X",x&255));}return s.toString();}
  catch(Exception e){return "UNAVAILABLE";}
 }
 private Function owner(Instruction i){return currentProgram.getFunctionManager().getFunctionContaining(i.getAddress());}
 private List<Instruction> beforeList(Instruction c,int n){
  List<Instruction>a=new ArrayList<>();Function f=owner(c);Instruction x=c;
  for(int k=0;k<n;k++){x=x.getPrevious();if(x==null||(f!=null&&!f.getBody().contains(x.getAddress())))break;a.add(x);}
  Collections.reverse(a);return a;
 }
 private String beforeText(List<Instruction>a){
  StringBuilder b=new StringBuilder();if(a.size()!=12)b.append("PRE12_COUNT=").append(a.size()).append("; ");
  for(Instruction i:a){if(b.length()>0&&b.charAt(b.length()-1)!=' ')b.append(" || ");b.append(hx(i.getAddress().getOffset())).append(" ").append(i).append(" [").append(bytes(i)).append("]");}
  return b.toString();
 }
 private String excerpt64(List<Instruction>a,Instruction c){
  StringBuilder b=new StringBuilder();int n=0;List<Instruction>all=new ArrayList<>(a);all.add(c);
  for(Instruction i:all){String x=bytes(i);if("UNAVAILABLE".equals(x))continue;for(String oct:x.split(" ")){if(n>=64)return b.toString().trim();if(b.length()>0)b.append(' ');b.append(oct);n++;}}
  return b.toString().trim();
 }
 private String valueCandidate(Instruction i,List<Instruction>prior){
  Matcher sm=STORE.matcher(i.toString());if(!sm.find())return "NOT_A_STORE";String reg=sm.group(2);
  for(int k=prior.size()-1;k>=0;k--){String t=prior.get(k).toString().trim();Matcher m=LI.matcher(t);
   if(m.find()&&reg.equalsIgnoreCase(m.group(1)))return "NEAREST_LI="+m.group(2)+"; CANDIDATE_ONLY";
   m=ADDIU.matcher(t);if(m.find()&&reg.equalsIgnoreCase(m.group(1)))return "NEAREST_ADDIU_ZERO="+m.group(2)+"; CANDIDATE_ONLY";
  }
  return "TIDAK_TAHU; store_register="+reg;
 }
 private void collectParticipantFunctions()throws Exception{
  ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(toAddr(PARTICIPANT_SLOT));
  while(refs.hasNext()){Function f=currentProgram.getFunctionManager().getFunctionContaining(refs.next().getFromAddress());if(f!=null)participantFns.put(f.getEntryPoint().toString(),f);}
  String token=String.format("%08x",PARTICIPANT_SLOT);InstructionIterator it=currentProgram.getListing().getInstructions(true);
  while(it.hasNext()){Instruction i=it.next();if(i.toString().toLowerCase().contains(token)){Function f=owner(i);if(f!=null)participantFns.put(f.getEntryPoint().toString(),f);}}
  Function h=currentProgram.getFunctionManager().getFunctionAt(toAddr(HANDLER));if(h!=null)participantFns.put(h.getEntryPoint().toString(),h);
 }
 @Override protected void run()throws Exception{
  String[]args=getScriptArgs();if(args.length<1)throw new IllegalArgumentException("Args: output TSV");
  try(PrintWriter w=new PrintWriter(new BufferedWriter(new OutputStreamWriter(new FileOutputStream(args[0]),StandardCharsets.UTF_8)))){
   out=w;collectParticipantFunctions();
   row("record_type","pc","function_entry","function_name","access","base_register","participant_global_function_scope","instruction","instruction_bytes","candidate_stored_value","pre12_instructions","raw_excerpt_bytes_le_64");
   InstructionIterator it=currentProgram.getListing().getInstructions(true);
   while(it.hasNext()){
    Instruction i=it.next();Matcher mm=MEM.matcher(i.toString());if(!mm.find())continue;String reg=mm.group(1),mn=i.getMnemonicString().toLowerCase();
    String kind=(mn.equals("sb")||mn.equals("sh")||mn.equals("sw")||mn.equals("sd"))?"WRITE":
      (mn.equals("lb")||mn.equals("lbu")||mn.equals("lh")||mn.equals("lhu")||mn.equals("lw")||mn.equals("ld"))?"READ":"OTHER";
    Function f=owner(i);String entry=f==null?"TIDAK_TAHU":hx(f.getEntryPoint().getOffset());String name=f==null?"TIDAK_TAHU":f.getName();
    boolean scope=f!=null&&participantFns.containsKey(f.getEntryPoint().toString());if(scope)inScope++;
    if("WRITE".equals(kind))writes++;else if("READ".equals(kind))reads++;else other++;
    List<Instruction>prior=beforeList(i,12);String v="READ".equals(kind)?"NOT_APPLICABLE":"WRITE".equals(kind)?valueCandidate(i,prior):"TIDAK_TAHU";
    row("ACTION_BYTE_ACCESS",hx(i.getAddress().getOffset()),entry,name,kind,reg,
      scope?"PARTICIPANT_GLOBAL_XREF_OR_HANDLER":"GLOBAL_DISPLACEMENT_ONLY",i.toString(),bytes(i),v,beforeText(prior),excerpt64(prior,i));
   }
   row("META","PARTICIPANT_GLOBAL",hx(PARTICIPANT_SLOT),"","FUNCTIONS","",String.valueOf(participantFns.size()),
     "","", "displacement scan=all Entry 1 memory operands +0x2EB; effective base remains a separate review","","");
   row("META","TOTALS","","","READ="+reads+";WRITE="+writes+";OTHER="+other,"","IN_PARTICIPANT_SCOPE="+inScope,"","","","","");
   out.flush();if(out.checkError())throw new IllegalStateException("BB2 action-byte export failed");
  }
 }
}
