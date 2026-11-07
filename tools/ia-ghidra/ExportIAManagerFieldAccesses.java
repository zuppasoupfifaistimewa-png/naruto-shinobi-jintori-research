import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.*;

/** Static census of instruction memory operands at one displacement.
 * The global slot is 0x8013EA74 = 0x80140000 - 0x158c.
 * Only same-function slot loads are marked as manager candidates.
 */
public class ExportIAManagerFieldAccesses extends GhidraScript {
    private static final Pattern MEM = Pattern.compile(
        "(?i),\\s*(-?0x[0-9a-f]+|-?[0-9]+)\\(([^)]+)\\)\\s*$");
    private String clean(String s) {
        return s == null ? "" : s.replace('\t',' ').replace('\r',' ').replace('\n',' ');
    }
    private void row(PrintWriter out, String... cells) {
        for (int i=0;i<cells.length;i++) { if(i>0) out.print('\t'); out.print(clean(cells[i])); }
        out.println();
    }
    private boolean loadsManagerSlot(Function f) {
        if (f == null) return false;
        boolean base = false, load = false;
        InstructionIterator it = currentProgram.getListing().getInstructions(f.getBody(), true);
        while (it.hasNext()) {
            String s = it.next().toString().toLowerCase(Locale.ROOT);
            if (s.matches(".*lui\\s+[a-z0-9]+,\\s*0x8014.*")) base = true;
            if (s.matches(".*lw\\s+[a-z0-9]+,\\s*-0x158c\\([a-z0-9]+\\).*")) load = true;
            if (base && load) return true;
        }
        return false;
    }
    @Override protected void run() throws Exception {
        String[] args=getScriptArgs();
        if(args.length<2) throw new IllegalArgumentException("Args: output-tsv displacement");
        int wanted=(int)Long.decode(args[1]).longValue();
        File f=new File(args[0]); File p=f.getParentFile(); if(p!=null)p.mkdirs();
        int all=0, same=0;
        try(PrintWriter out=new PrintWriter(new BufferedWriter(
            new OutputStreamWriter(new FileOutputStream(f), StandardCharsets.UTF_8)))) {
            row(out,"pc","function_entry","function_name","mnemonic","instruction",
                "manager_slot_load_same_function","displacement","base_register");
            InstructionIterator it=currentProgram.getListing().getInstructions(true);
            while(it.hasNext()) {
                monitor.checkCancelled();
                Instruction ins=it.next();
                Matcher m=MEM.matcher(ins.toString().trim());
                if(!m.find()) continue;
                int disp;
                try { disp=(int)Long.decode(m.group(1)).longValue(); } catch(Exception e) { continue; }
                if(disp!=wanted) continue;
                all++;
                Function fn=currentProgram.getFunctionManager().getFunctionContaining(ins.getAddress());
                boolean candidate=loadsManagerSlot(fn);
                if(candidate)same++;
                row(out,ins.getAddress().toString(),fn==null?"NONE":fn.getEntryPoint().toString(),
                    fn==null?"NONE":fn.getName(),ins.getMnemonicString(),ins.toString(),
                    candidate?"YES":"NO",String.format("0x%X",disp),m.group(2));
            }
            row(out,"TOTAL","","","","instruction_count="+all,
                "same_function_manager_candidates="+same,"","", "");
            out.flush(); if(out.checkError()) throw new IOException("TSV write failed");
        }
        println("IA_ACCESS_DISPLACEMENT="+String.format("0x%X",wanted));
        println("IA_ACCESS_TOTAL="+all);
        println("IA_ACCESS_MANAGER_FUNCTION_CANDIDATES="+same);
    }
}