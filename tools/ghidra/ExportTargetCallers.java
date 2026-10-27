// ExportTargetCallers.java
// Validate direct MIPS call flows to selected main-EXE targets from a single
// imported resource. Emits only functions that directly call those targets.
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class ExportTargetCallers extends GhidraScript {
    private PrintWriter out;
    private void line(String s) { out.println(s); }

    private static class Hit {
        Address target;
        Address site;
        Instruction instruction;
        Function function;
        Hit(Address t, Address s, Instruction i, Function f) {
            target=t; site=s; instruction=i; function=f;
        }
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2 || args[0].trim().isEmpty())
            throw new IllegalArgumentException("Args: output-path target-address [target-address ...]");
        List<Address> targets = new ArrayList<>();
        for (int i=1; i<args.length; i++) targets.add(toAddr(Long.decode(args[i])));
        Map<String, Function> uniqueFunctions = new LinkedHashMap<>();
        List<Hit> hits = new ArrayList<>();
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out=writer;
            line("analysis=Ghidra-validated direct call-flow scan");
            line("program="+currentProgram.getName());
            line("program_language="+currentProgram.getLanguageID());
            line("entrypoint_or_emulator_executed=no");
            line("address_model=candidate resource base only; runtime loading is not proven");
            line("targets="+targets.toString());

            InstructionIterator iterator=currentProgram.getListing().getInstructions(true);
            int scanned=0;
            while(iterator.hasNext()) {
                monitor.checkCancelled();
                Instruction instruction=iterator.next();
                scanned++;
                if(!instruction.getFlowType().isCall()) continue;
                Address[] flows=instruction.getFlows();
                if(flows==null || flows.length==0) continue;
                for(Address target: targets) {
                    for(Address flow: flows) {
                        if(!target.equals(flow)) continue;
                        Function f=getFunctionContaining(instruction.getAddress());
                        hits.add(new Hit(target,instruction.getAddress(),instruction,f));
                        if(f!=null) uniqueFunctions.putIfAbsent(f.getEntryPoint().toString(),f);
                    }
                }
            }
            line("instruction_count_scanned="+scanned);
            line("validated_direct_callsite_count="+hits.size());
            line("unique_caller_function_count="+uniqueFunctions.size());
            line("");
            line("=== VALIDATED_CALLSITES ===");
            for(Hit hit: hits) {
                line("target="+hit.target+" callsite="+hit.site+" instruction="+hit.instruction);
                if(hit.function==null) line("caller_function=UNMAPPED");
                else line("caller_entry="+hit.function.getEntryPoint()
                    +" caller_name="+hit.function.getName()
                    +" caller_body_bytes="+hit.function.getBody().getNumAddresses());
            }

            DecompInterface decompiler=new DecompInterface();
            decompiler.toggleCCode(true);
            decompiler.toggleSyntaxTree(false);
            if(!decompiler.openProgram(currentProgram))
                throw new IllegalStateException("Decompiler could not open imported program.");
            for(Function f: uniqueFunctions.values()) {
                monitor.checkCancelled();
                line("");
                line("=== CALLER_FUNCTION entry="+f.getEntryPoint()+" name="+f.getName()
                    +" body_bytes="+f.getBody().getNumAddresses()+" ===");
                DecompileResults result=decompiler.decompileFunction(f,90,monitor);
                if(result!=null && result.decompileCompleted() && result.getDecompiledFunction()!=null) {
                    line("--- C_DECOMPILATION_BEGIN ---");
                    line(result.getDecompiledFunction().getC());
                    line("--- C_DECOMPILATION_END ---");
                } else {
                    line("decompile_status=FAILED");
                    line("decompile_message="+(result==null?"null result":result.getErrorMessage()));
                }
                for(Hit hit:hits) {
                    if(hit.function==null || !hit.function.getEntryPoint().equals(f.getEntryPoint())) continue;
                    line("--- CALLSITE_CONTEXT target="+hit.target+" site="+hit.site+" ---");
                    Instruction first=hit.instruction;
                    for(int n=0;n<4 && first.getPrevious()!=null;n++) first=first.getPrevious();
                    for(int n=0;n<12 && first!=null;n++,first=first.getNext())
                        line(first.getAddress()+"\t"+first.toString());
                }
            }
            decompiler.dispose();
            out.flush();
            if(out.checkError()) throw new IllegalStateException("Failed writing caller report.");
        }
    }
}
