// Export bounded instruction windows around all direct JAL sites to target helper functions.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.address.Address;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.*;

public class ExportCallWindows extends GhidraScript {
 private PrintWriter out;
 private String clean(String s){return s==null?"":s.replace('\t',' ').replace('\n',' ').replace('\r',' ');}
 private void row(String...a){for(int i=0;i<a.length;i++){if(i>0)out.print('\t');out.print(clean(a[i]));}out.println();}
 private String hexBytes(Instruction ins)throws Exception{
  byte[] b=new byte[ins.getLength()];currentProgram.getMemory().getBytes(ins.getAddress(),b);
  StringBuilder s=new StringBuilder();for(byte x:b){if(s.length()>0)s.append(' ');s.append(String.format("%02X",x&255));}return s.toString();
 }
 @Override protected void run() throws Exception{
  String[] args=getScriptArgs();if(args.length<2)throw new IllegalArgumentException("Args: output target1 [target2...]");
  Set<Long> targets=new HashSet<>();for(int i=1;i<args.length;i++)targets.add(Long.decode(args[i]));
  Pattern p=Pattern.compile("(?i)jal\\s+0x([0-9a-f]+)");
  try(PrintWriter w=new PrintWriter(new BufferedWriter(new OutputStreamWriter(new FileOutputStream(args[0]),StandardCharsets.UTF_8)))){
   out=w;row("target","callsite_pc","function_entry","function_name","relative_position","instruction_pc","bytes","instruction");
   int calls=0;
   InstructionIterator it=currentProgram.getListing().getInstructions(true);
   while(it.hasNext()){
    Instruction call=it.next();if(!"jal".equalsIgnoreCase(call.getMnemonicString()))continue;
    Matcher m=p.matcher(call.toString());if(!m.find())continue;
    long target=Long.parseLong(m.group(1),16);if(!targets.contains(target))continue;
    calls++;Function f=currentProgram.getFunctionManager().getFunctionContaining(call.getAddress());
    long base=call.getAddress().getOffset();
    for(int delta=-48;delta<=64;delta+=4){
     Address a=toAddr(base+delta);Instruction ins=currentProgram.getListing().getInstructionAt(a);
     if(ins==null)continue;
     String rel=delta<0?"PRE":(delta==0?"CALL":"POST");
     row(String.format("0x%08X",target),String.format("0x%08X",base),
         f==null?"NONE":f.getEntryPoint().toString(),f==null?"NONE":f.getName(),
         rel,String.format("0x%08X",ins.getAddress().getOffset()),hexBytes(ins),ins.toString());
    }
   }
   row("TOTAL","","","","","direct_calls="+calls,"","window=-12..+16 instructions");
   out.flush();if(out.checkError())throw new IllegalStateException("write failed");
  }
 }
}
