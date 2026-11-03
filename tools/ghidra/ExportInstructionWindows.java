import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.*;
import java.nio.charset.StandardCharsets;

public class ExportInstructionWindows extends GhidraScript {
    private PrintWriter out;
    private void line(String s) { out.println(s); }
    private String bytes(Instruction ins) throws Exception {
        byte[] raw = new byte[ins.getLength()];
        currentProgram.getMemory().getBytes(ins.getAddress(), raw);
        StringBuilder b = new StringBuilder();
        for (byte v : raw) {
            if (b.length() > 0) b.append(' ');
            b.append(String.format("%02X", v & 0xff));
        }
        return b.toString();
    }
    private void dump(Address address, int before, int after) throws Exception {
        line("");
        line("=== ADDRESS " + address + " ===");
        Instruction center = currentProgram.getListing().getInstructionAt(address);
        Function f = currentProgram.getFunctionManager().getFunctionContaining(address);
        line("instruction=" + (center == null ? "NOT_DECODED" : center.toString()));
        line("function=" + (f == null ? "NONE" : f.getName()));
        line("function_entry=" + (f == null ? "NONE" : f.getEntryPoint().toString()));
        line("function_body_bytes=" + (f == null ? "NONE" : Long.toString(f.getBody().getNumAddresses())));
        if (center != null) {
            Instruction first=center, last=center;
            for(int i=0;i<before && first.getPrevious()!=null;i++) first=first.getPrevious();
            for(int i=0;i<after && last.getNext()!=null;i++) last=last.getNext();
            for(Instruction ins=first; ins!=null; ins=ins.getNext()) {
                line(ins.getAddress()+" bytes=["+bytes(ins)+"] "+ins.toString());
                if(ins.getAddress().equals(last.getAddress())) break;
            }
        }
        if (f != null) {
            line("--- REFERENCES_TO_FUNCTION ---");
            ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(f.getEntryPoint());
            int count=0;
            while(refs.hasNext()) {
                Reference ref=refs.next();
                Function caller=currentProgram.getFunctionManager().getFunctionContaining(ref.getFromAddress());
                line("from="+ref.getFromAddress()+" type="+ref.getReferenceType()
                    +" caller="+(caller==null?"NONE":caller.getName())
                    +" caller_entry="+(caller==null?"NONE":caller.getEntryPoint()));
                count++;
            }
            line("reference_count="+count);
            line("--- END_REFERENCES ---");
        }
    }
    @Override
    protected void run() throws Exception {
        String[] args=getScriptArgs();
        if(args.length<2) throw new IllegalArgumentException("Args: output-path address [address ...]");
        File file=new File(args[0]);
        File parent=file.getParentFile();
        if(parent!=null) parent.mkdirs();
        try(PrintWriter w=new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(file), StandardCharsets.UTF_8)))) {
            out=w;
            line("analysis=selected MIPS instruction windows");
            line("program="+currentProgram.getName());
            line("program_language="+currentProgram.getLanguageID());
            line("game_or_emulator_executed=no");
            line("binary_uploaded_as_artifact=no");
            for(int i=1;i<args.length;i++) {
                monitor.checkCancelled();
                dump(toAddr(Long.decode(args[i])),20,28);
            }
            out.flush();
            if(out.checkError()) throw new IllegalStateException("Failed writing instruction windows.");
        }
    }
}
