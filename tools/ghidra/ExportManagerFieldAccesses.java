// Export all MIPS instructions using displacement +0xB44 from DATA.BIN Entry 1.
// The base object is not assumed to be manager unless the function also contains
// the global-slot load pattern; all candidates are emitted with that caveat.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.*;

public class ExportManagerFieldAccesses extends GhidraScript {
 private PrintWriter out;
 private String clean(String s){return s==null?"":s.replace('\t',' ').replace('\n',' ').replace('\r',' ');}
 private void row(String... a){for(int i=0;i<a.length;i++){if(i>0)out.print('\t');out.print(clean(a[i]));}out.println();}
 private boolean hasManagerSlotLoad(Function f){
  InstructionIterator it=currentProgram.getListing().getInstructions(f.getBody(),true);
  boolean lui=false,load=false;
  while(it.hasNext()){String x=it.next().toString().toLowerCase();
   if(x.matches(".*lui [a-z0-9]+,0x8014.*"))lui=true;
   if(x.contains("lw ")&&x.contains("-0x5aac("))load=true;
  }
  return lui&&load;
 }
 private String entry(Function f){return f==null?"TIDAK_TAHU":f.getEntryPoint().toString();}
 @Override protected void run() throws Exception {
  String[] a=getScriptArgs();if(a.length<2)throw new IllegalArgumentException("Args: output and displacement");
  int disp=(int)Long.decode(a[1]).longValue();
  try(PrintWriter w=new PrintWriter(new BufferedWriter(new OutputStreamWriter(new FileOutputStream(a[0]),StandardCharsets.UTF_8)))){
   out=w;row("pc","function_entry","function_name","mnemonic","instruction","manager_slot_load_same_function","classification");
   Map<String,Function> funcs=new TreeMap<>();int count=0;
   InstructionIterator it=currentProgram.getListing().getInstructions(true);
   while(it.hasNext()){
    Instruction ins=it.next();String text=ins.toString().toLowerCase();
    Matcher m=Pattern.compile("(?i)(?:0x)?([0-9a-f]+)\\(").matcher(text);
    boolean hit=false;while(m.find()){try{if((int)Long.parseLong(m.group(1),16)==disp){hit=true;break;}}catch(Exception ignored){}}
    if(!hit)continue;
    Function f=currentProgram.getFunctionManager().getFunctionContaining(ins.getAddress());
    if(f!=null)funcs.put(entry(f),f);
    boolean manager=f!=null&&hasManagerSlotLoad(f);
    row(ins.getAddress().toString(),entry(f),f==null?"NONE":f.getName(),ins.getMnemonicString(),ins.toString(),
        manager?"YES":"NO","B44_DISPLACEMENT; BASE_ALIAS_REQUIRES_REVIEW");
    count++;
   }
   row("TOTAL","","","","instruction_count="+count,"unique_functions="+funcs.size(),"");
   for(Function f:funcs.values())row("FUNCTION",entry(f),f.getName(),"","","",hasManagerSlotLoad(f)?"SLOT_LOAD_IN_SAME_FUNCTION":"SLOT_LOAD_NOT_SEEN");
   out.flush();if(out.checkError())throw new IllegalStateException("write failed");
  }
 }
}
