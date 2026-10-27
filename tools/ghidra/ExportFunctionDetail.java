// ExportFunctionDetail.java
// Runner-only static audit of selected main-executable functions: decompilation,
// raw decoded MIPS body, and cross-references. Output is text only.
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

public class ExportFunctionDetail extends GhidraScript {
    private PrintWriter out;
    private void line(String value) { out.println(value); }

    private String rawBytes(Instruction ins) throws Exception {
        byte[] bytes = new byte[ins.getLength()];
        currentProgram.getMemory().getBytes(ins.getAddress(), bytes);
        StringBuilder b = new StringBuilder();
        for (byte value : bytes) {
            if (b.length() > 0) b.append(' ');
            b.append(String.format("%02X", value & 0xff));
        }
        return b.toString();
    }

    private void dumpWindow(Instruction center, int before, int after) throws Exception {
        if (center == null) {
            line("instruction_window=UNAVAILABLE");
            return;
        }
        Instruction first=center;
        for(int i=0; i<before && first.getPrevious()!=null; i++) first=first.getPrevious();
        Instruction last=center;
        for(int i=0; i<after && last.getNext()!=null; i++) last=last.getNext();
        for(Instruction ins=first; ins!=null; ins=ins.getNext()) {
            line("  " + ins.getAddress() + " bytes=[" + rawBytes(ins) + "] " + ins.toString());
            if(ins.getAddress().equals(last.getAddress())) break;
        }
    }

    private void dumpTarget(Address target, DecompInterface decompiler) throws Exception {
        line("");
        line("=== TARGET " + target + " ===");
        Instruction at=currentProgram.getListing().getInstructionAt(target);
        line("instruction_at_target=" + (at==null ? "NONE" : at.toString()));
        Function f=currentProgram.getFunctionManager().getFunctionAt(target);
        if(f==null) f=currentProgram.getFunctionManager().getFunctionContaining(target);
        if(f==null) {
            line("function=NONE");
            dumpWindow(at, 8, 16);
            return;
        }
        line("function_name=" + f.getName());
        line("function_entry=" + f.getEntryPoint());
        line("function_body_bytes=" + f.getBody().getNumAddresses());
        line("function_return_type=" + f.getReturnType().getName());
        line("function_signature=" + f.getSignature());
        line("function_thunk=" + f.isThunk());

        line("--- RAW_FUNCTION_BODY_BEGIN ---");
        InstructionIterator instructions=currentProgram.getListing().getInstructions(f.getBody(), true);
        int n=0;
        while(instructions.hasNext()) {
            Instruction ins=instructions.next();
            line(ins.getAddress() + " bytes=[" + rawBytes(ins) + "] " + ins.toString());
            n++;
            if(n>4096) {
                line("RAW_FUNCTION_BODY_TRUNCATED=instruction_limit_4096");
                break;
            }
        }
        line("--- RAW_FUNCTION_BODY_END ---");
        line("raw_instruction_count_emitted=" + n);

        DecompileResults result=decompiler.decompileFunction(f, 90, monitor);
        if(result!=null && result.decompileCompleted() && result.getDecompiledFunction()!=null) {
            line("--- C_DECOMPILATION_BEGIN ---");
            line(result.getDecompiledFunction().getC());
            line("--- C_DECOMPILATION_END ---");
            line("decompile_status=SUCCESS");
        } else {
            line("decompile_status=FAILED");
            line("decompile_message=" + (result==null ? "null result" : result.getErrorMessage()));
        }

        line("--- REFERENCES_TO_FUNCTION_BEGIN ---");
        ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(f.getEntryPoint());
        int refsCount=0;
        while(refs.hasNext()) {
            Reference ref=refs.next();
            Instruction callerIns=currentProgram.getListing().getInstructionAt(ref.getFromAddress());
            Function caller=currentProgram.getFunctionManager().getFunctionContaining(ref.getFromAddress());
            line("reference_from=" + ref.getFromAddress()
                + " reference_type=" + ref.getReferenceType()
                + " source=" + ref.getSource()
                + " caller_entry=" + (caller==null ? "NONE" : caller.getEntryPoint())
                + " caller_name=" + (caller==null ? "NONE" : caller.getName()));
            if(callerIns!=null) {
                line("  callsite_context:");
                dumpWindow(callerIns, 1, 2);
            }
            refsCount++;
        }
        line("reference_count=" + refsCount);
        line("--- REFERENCES_TO_FUNCTION_END ---");
    }

    @Override
    protected void run() throws Exception {
        String[] args=getScriptArgs();
        if(args.length<2) throw new IllegalArgumentException(
            "Args: output-path target-address [target-address ...]");
        try(PrintWriter writer=new PrintWriter(new BufferedWriter(
            new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out=writer;
            line("analysis=Ghidra selected-function static audit");
            line("program=" + currentProgram.getName());
            line("program_language=" + currentProgram.getLanguageID());
            line("loaded_executable_base=0x80010000 (PS-X EXE header verified by workflow)");
            line("game_or_emulator_executed=no");
            line("gameplay_input_sent=no");
            line("savestate_restored=no");
            line("binary_uploaded_as_artifact=no");
            DecompInterface decompiler=new DecompInterface();
            decompiler.toggleCCode(true);
            decompiler.toggleSyntaxTree(false);
            if(!decompiler.openProgram(currentProgram))
                throw new IllegalStateException("Decompiler could not open main executable.");
            for(int i=1;i<args.length;i++) dumpTarget(toAddr(Long.decode(args[i])),decompiler);
            decompiler.dispose();
            out.flush();
            if(out.checkError()) throw new IllegalStateException("Failed writing selected-function audit.");
        }
    }
}
