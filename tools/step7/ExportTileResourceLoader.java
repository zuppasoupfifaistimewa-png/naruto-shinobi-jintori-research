// ExportTileResourceLoader.java
// Static-only bounded export of the tile resource loader at 0x800F7ADC.
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;

public class ExportTileResourceLoader extends GhidraScript {
    private PrintWriter out;
    private void p(String s) { out.println(s); }
    private String bytes(Instruction i) throws Exception {
        byte[] b=new byte[i.getLength()];
        currentProgram.getMemory().getBytes(i.getAddress(),b);
        StringBuilder s=new StringBuilder();
        for(byte v:b){if(s.length()>0)s.append(' ');s.append(String.format("%02X",v&255));}
        return s.toString();
    }
    private void window(Instruction at,int before,int after)throws Exception{
        if(at==null){p("WINDOW=UNAVAILABLE");return;}
        Instruction first=at,last=at;
        for(int n=0;n<before&&first.getPrevious()!=null;n++)first=first.getPrevious();
        for(int n=0;n<after&&last.getNext()!=null;n++)last=last.getNext();
        for(Instruction i=first;i!=null;i=i.getNext()){
            p(i.getAddress()+" bytes=["+bytes(i)+"] "+i);
            if(i.getAddress().equals(last.getAddress()))break;
        }
    }
    private void target(long raw,DecompInterface d)throws Exception{
        Address a=toAddr(raw);
        p("");p("=== TARGET 0x"+Long.toHexString(raw)+" ===");
        if(!currentProgram.getMemory().contains(a)){p("STATUS=OUTSIDE_IMPORTED_IMAGE");return;}
        Instruction at=currentProgram.getListing().getInstructionAt(a);
        if(at==null){try{disassemble(a);at=currentProgram.getListing().getInstructionAt(a);}catch(Exception e){p("DISASSEMBLY_ERROR="+e.getMessage());}}
        Function f=currentProgram.getFunctionManager().getFunctionAt(a);
        if(f==null&&at!=null){
            try{createFunction(a,"FUN_"+String.format("%08x",raw));}
            catch(Exception e){p("CREATE_FUNCTION_ERROR="+e.getMessage());}
            f=currentProgram.getFunctionManager().getFunctionAt(a);
        }
        p("instruction_at_target="+(at==null?"NONE":at.toString()));
        if(f==null){p("FUNCTION=NONE");window(at,16,96);return;}
        p("function_entry="+f.getEntryPoint());
        p("function_name="+f.getName());
        p("function_bytes="+f.getBody().getNumAddresses());
        p("--- RAW_BODY_BEGIN ---");
        InstructionIterator it=currentProgram.getListing().getInstructions(f.getBody(),true);
        int n=0;
        while(it.hasNext()&&n<2048){Instruction i=it.next();p(i.getAddress()+" bytes=["+bytes(i)+"] "+i);n++;}
        p("--- RAW_BODY_END ---");
        p("raw_instruction_count="+n);
        DecompileResults r=d.decompileFunction(f,120,monitor);
        if(r!=null&&r.decompileCompleted()&&r.getDecompiledFunction()!=null){
            p("--- C_BEGIN ---");p(r.getDecompiledFunction().getC());p("--- C_END ---");p("DECOMPILE=SUCCESS");
        }else{p("DECOMPILE=FAILED "+(r==null?"null":r.getErrorMessage()));}
        p("--- XREFS_TO_FUNCTION_BEGIN ---");
        ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(f.getEntryPoint());
        int count=0;
        while(refs.hasNext()){
            Reference ref=refs.next();count++;
            Instruction ci=currentProgram.getListing().getInstructionAt(ref.getFromAddress());
            Function owner=currentProgram.getFunctionManager().getFunctionContaining(ref.getFromAddress());
            p("xref="+ref.getFromAddress()+" type="+ref.getReferenceType()+" owner="+(owner==null?"TIDAK_TAHU":owner.getEntryPoint()));
            if(ci!=null)window(ci,4,4);
        }
        p("xref_count="+count);p("--- XREFS_TO_FUNCTION_END ---");
        p("--- JAL_CALLS_IN_FUNCTION_BEGIN ---");
        it=currentProgram.getListing().getInstructions(f.getBody(),true);
        while(it.hasNext()){
            Instruction i=it.next();
            if(!"jal".equalsIgnoreCase(i.getMnemonicString()))continue;
            Object[] ops=i.getOpObjects(0);
            String target=ops.length>0?ops[0].toString():"TIDAK_TAHU";
            p("CALLSITE="+i.getAddress()+" TARGET="+target+" INSN="+i);
            window(i,3,2);
        }
        p("--- JAL_CALLS_IN_FUNCTION_END ---");
    }
    @Override protected void run()throws Exception{
        String[] args=getScriptArgs();
        if(args.length<2)throw new IllegalArgumentException("Args: output-path target-address...");
        try(PrintWriter w=new PrintWriter(new BufferedWriter(new OutputStreamWriter(new FileOutputStream(args[0]),StandardCharsets.UTF_8)))){
            out=w;
            p("analysis=static Ghidra instruction/decompilation export");
            p("program="+currentProgram.getName());
            p("entry1_base=0x800AD450 (static import candidate; runtime mapping unvalidated)");
            p("game_or_emulator_executed=no");
            p("binary_uploaded_as_artifact=no");
            DecompInterface d=new DecompInterface();d.toggleCCode(true);d.toggleSyntaxTree(false);
            if(!d.openProgram(currentProgram))throw new IllegalStateException("Decompiler open failed");
            for(int n=1;n<args.length;n++)target(Long.decode(args[n]),d);
            d.dispose();out.flush();if(out.checkError())throw new IllegalStateException("output write failed");
        }
    }
}
