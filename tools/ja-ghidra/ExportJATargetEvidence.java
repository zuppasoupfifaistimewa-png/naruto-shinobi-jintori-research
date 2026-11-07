import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressRange;
import ghidra.program.model.address.AddressRangeIterator;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;

public class ExportJATargetEvidence extends GhidraScript {
    private PrintWriter out;
    private void line(String s) { out.println(s); }

    private void window(Address center, int before, int after, String label) throws Exception {
        Instruction at=currentProgram.getListing().getInstructionAt(center);
        line(label+"_WINDOW_BEGIN");
        if(at==null) {
            line("WINDOW_UNAVAILABLE="+center);
            line(label+"_WINDOW_END");
            return;
        }
        Instruction first=at;
        for(int i=0;i<before && first.getPrevious()!=null;i++) first=first.getPrevious();
        Instruction last=at;
        for(int i=0;i<after && last.getNext()!=null;i++) last=last.getNext();
        int n=0;
        for(Instruction ins=first;ins!=null;ins=ins.getNext()) {
            line("INS="+ins.getAddress()+"|"+ins.toString());
            n++;
            if(ins.getAddress().equals(last.getAddress()) || n>=16) break;
        }
        line("WINDOW_INSTRUCTION_COUNT="+n);
        line(label+"_WINDOW_END");
    }

    @Override
    protected void run() throws Exception {
        String[] args=getScriptArgs();
        if(args.length<2) throw new IllegalArgumentException("Args: output-path target-address [target-address ...]");
        try(PrintWriter writer=new PrintWriter(new BufferedWriter(
            new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out=writer;
            line("IMAGE="+currentProgram.getName());
            InstructionIterator code=currentProgram.getListing().getInstructions(true);
            while(code.hasNext()) {
                Instruction ins=code.next();
                byte[] bytes=new byte[ins.getLength()];
                currentProgram.getMemory().getBytes(ins.getAddress(),bytes);
                StringBuilder hex=new StringBuilder();
                for(byte value:bytes) {
                    if(hex.length()>0) hex.append(' ');
                    hex.append(String.format("%02X",value & 0xff));
                }
                line("CODE_INSTRUCTION="+ins.getAddress()+"|"+hex.toString()+"|"+ins.toString());
            }
            FunctionIterator all=currentProgram.getFunctionManager().getFunctions(true);
            while(all.hasNext()) {
                Function fn=all.next();
                AddressRangeIterator ranges=fn.getBody().getAddressRanges();
                while(ranges.hasNext()) {
                    AddressRange range=ranges.next();
                    line("FUNCTION_RANGE="+fn.getEntryPoint()+"|"+range.getMinAddress()+"|"+range.getMaxAddress()+"|"+fn.getName());
                }
            }
            line("BASE_MODEL=Ghidra imported image; no runtime claim");
            for(int i=1;i<args.length;i++) {
                Address target=toAddr(Long.decode(args[i]));
                line("");
                line("TARGET="+target);
                Instruction ins=currentProgram.getListing().getInstructionAt(target);
                line("TARGET_INSTRUCTION="+(ins==null?"TIDAK_TAHU":ins.toString()));
                Function f=currentProgram.getFunctionManager().getFunctionContaining(target);
                if(f==null) {
                    line("CONTAINING_FUNCTION=TIDAK_TAHU");
                    line("FUNCTION_ENTRY=TIDAK_TAHU");
                    line("FUNCTION_NAME=TIDAK_TAHU");
                    line("FUNCTION_BODY_CONTAINS_TARGET=NO_FUNCTION");
                } else {
                    line("CONTAINING_FUNCTION="+f.getName());
                    line("FUNCTION_ENTRY="+f.getEntryPoint());
                    line("FUNCTION_NAME="+f.getName());
                    line("FUNCTION_BODY_START="+f.getBody().getMinAddress());
                    line("FUNCTION_BODY_END="+f.getBody().getMaxAddress());
                    line("FUNCTION_BODY_CONTAINS_TARGET="+f.getBody().contains(target));
                }
                ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(target);
                int count=0;
                while(refs.hasNext()) {
                    Reference ref=refs.next();
                    Function caller=currentProgram.getFunctionManager().getFunctionContaining(ref.getFromAddress());
                    line("REF="+ref.getFromAddress()+"|"+ref.getReferenceType()+"|"+
                        (caller==null?"TIDAK_TAHU":caller.getEntryPoint())+"|"+
                        (caller==null?"TIDAK_TAHU":caller.getName()));
                    window(ref.getFromAddress(),7,8,"REF_"+count);
                    count++;
                }
                line("REFERENCE_COUNT="+count);
                window(target,7,8,"TARGET");
            }
            out.flush();
            if(out.checkError()) throw new IllegalStateException("JA target evidence write failed");
        }
    }
}
