// Enumerate selected code immediate literals, including 0xBE (decimal 190), in MIPS instructions.
// Rows are code-literal candidates, not economic semantic labels or data-table xrefs.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.*;

public class ExportNumericLiteralReferences extends GhidraScript {
 private PrintWriter out;
 private static final Set<Long> VALUES=new HashSet<>(Arrays.asList(50L,60L,100L,150L,190L));
 private String clean(String s){return s==null?"":s.replace('\t',' ').replace('\n',' ').replace('\r',' ');}
 private void row(String...a){for(int i=0;i<a.length;i++){if(i>0)out.print('\t');out.print(clean(a[i]));}out.println();}
 @Override protected void run() throws Exception {
  String[] args=getScriptArgs();if(args.length<1)throw new IllegalArgumentException("output path required");
  Pattern p=Pattern.compile("(?i)(?:^|[, ])(-?)0x([0-9a-f]+)(?=$|[, ])");
  try(PrintWriter w=new PrintWriter(new BufferedWriter(new OutputStreamWriter(new FileOutputStream(args[0]),StandardCharsets.UTF_8)))){
   out=w;row("pc","function_entry","function_name","instruction_bytes","instruction","literal_decimal","literal_hex","operand_class");
   int count=0;
   InstructionIterator it=currentProgram.getListing().getInstructions(true);
   while(it.hasNext()){
    Instruction ins=it.next();String text=ins.toString();Matcher m=p.matcher(text);
    while(m.find()){
     long v=Long.parseLong(m.group(2),16);
     if(VALUES.contains(v)){
      Function f=currentProgram.getFunctionManager().getFunctionContaining(ins.getAddress());
      row(ins.getAddress().toString(),f==null?"NONE":f.getEntryPoint().toString(),
          f==null?"NONE":f.getName(),bytes(ins),text,(m.group(1).equals("-")?"-":"")+Long.toString(v),
          (m.group(1).equals("-")?"-":"")+"0x"+m.group(2).toUpperCase(),
          "IMMEDIATE_LITERAL_NOT_DATA_TABLE_XREF");count++;
     }
    }
   }
   row("TOTAL","","","","","instruction_literal_rows="+count,"","");
   out.flush();if(out.checkError())throw new IllegalStateException("write failure");
  }
 }
 private String bytes(Instruction i)throws Exception{
  byte[] b=new byte[i.getLength()];currentProgram.getMemory().getBytes(i.getAddress(),b);
  StringBuilder s=new StringBuilder();for(byte x:b){if(s.length()>0)s.append(' ');s.append(String.format("%02X",x&255));}return s.toString();
 }
}
