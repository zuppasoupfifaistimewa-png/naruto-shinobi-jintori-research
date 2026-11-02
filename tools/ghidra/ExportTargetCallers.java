// ExportTargetCallers.java
// Compare raw direct-JAL candidates with Ghidra-decoded direct flows for one
// imported resource. Only selected callers are deeply decompiled; the complete
// candidate/caller address inventory remains text-only.
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.mem.MemoryAccessException;
import ghidra.program.model.mem.MemoryBlock;
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
        int word;
        Instruction instruction;
        Function function;
        boolean flowValidated;
        Hit(Address t, Address s, int w, Instruction i, Function f, boolean v) {
            target=t; site=s; word=w; instruction=i; function=f; flowValidated=v;
        }
    }

    private boolean hasFlow(Instruction instruction, Address target) {
        if (instruction == null || !instruction.getFlowType().isCall()) return false;
        Address[] flows = instruction.getFlows();
        if (flows == null) return false;
        for (Address flow : flows) if (target.equals(flow)) return true;
        return false;
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2 || args[0].trim().isEmpty())
            throw new IllegalArgumentException("Args: output-path target-address [target-address ...]");
        List<Address> targets = new ArrayList<>();
        for (int i=1; i<args.length; i++) targets.add(toAddr(Long.decode(args[i])));
        List<Hit> rawHits = new ArrayList<>();
        List<Hit> validatedHits = new ArrayList<>();
        Map<String, Function> uniqueFunctions = new LinkedHashMap<>();
        Map<String, Function> selectedForDecompile = new LinkedHashMap<>();

        try (PrintWriter writer = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out=writer;
            line("analysis=Ghidra raw-JAL vs decoded direct-flow comparison");
            line("program="+currentProgram.getName());
            line("program_language="+currentProgram.getLanguageID());
            line("entrypoint_or_emulator_executed=no");
            line("address_model=candidate resource base only; runtime loading is not proven");
            line("targets="+targets.toString());

            int wordsScanned=0;
            MemoryBlock[] blocks=currentProgram.getMemory().getBlocks();
            for (MemoryBlock block : blocks) {
                long size=block.getSize();
                for (long offset=0; offset+4<=size; offset+=4) {
                    if ((offset & 0x3FFFL)==0) monitor.checkCancelled();
                    Address site=block.getStart().add(offset);
                    int word;
                    try { word=currentProgram.getMemory().getInt(site); }
                    catch (MemoryAccessException e) { continue; }
                    wordsScanned++;
                    if ((word >>> 26) != 3) continue; // MIPS JAL opcode
                    long destination=((site.getOffset()+4) & 0xF0000000L)
                        | (((long)word & 0x03FFFFFFL) << 2);
                    Address decodedTarget=toAddr(destination);
                    Address matched=null;
                    for (Address target:targets) if (target.equals(decodedTarget)) {
                        matched=target; break;
                    }
                    if (matched==null) continue;
                    Instruction instruction=currentProgram.getListing().getInstructionAt(site);
                    boolean validated=hasFlow(instruction,matched);
                    Function f=getFunctionContaining(site);
                    Hit hit=new Hit(matched,site,word,instruction,f,validated);
                    rawHits.add(hit);
                    if (validated) {
                        validatedHits.add(hit);
                        if (f!=null) uniqueFunctions.putIfAbsent(f.getEntryPoint().toString(),f);
                    }
                }
            }

            line("aligned_words_scanned="+wordsScanned);
            line("raw_jal_candidate_count="+rawHits.size());
            line("ghidra_decoded_direct_callsite_count="+validatedHits.size());
            line("unique_validated_caller_functions_with_boundary="+uniqueFunctions.size());
            line("");
            line("=== RAW_JAL_CANDIDATES ===");
            for (Hit hit:rawHits) {
                String status=hit.flowValidated?"VALIDATED_GHIDRA_DIRECT_CALL":
                    (hit.instruction==null?"RAW_WORD_ONLY_INSTRUCTION_NOT_DECODED":"RAW_WORD_NOT_FLOW_CONFIRMED");
                line("target="+hit.target+" site="+hit.site+" word=0x"+String.format("%08X",hit.word)
                    +" status="+status);
                if(hit.function!=null) line("caller_entry="+hit.function.getEntryPoint()
                    +" caller_name="+hit.function.getName()
                    +" caller_body_bytes="+hit.function.getBody().getNumAddresses());
                else line("caller_function=UNMAPPED");
                if(hit.instruction!=null) line("decoded_instruction="+hit.instruction);
            }

            line("");
            line("=== GHIDRA_VALIDATED_DIRECT_CALLS ===");
            for(Hit hit:validatedHits) {
                line("target="+hit.target+" site="+hit.site+" instruction="+hit.instruction);
                if(hit.function==null) line("caller_function=UNMAPPED");
                else line("caller_entry="+hit.function.getEntryPoint()
                    +" caller_name="+hit.function.getName()
                    +" caller_body_bytes="+hit.function.getBody().getNumAddresses());
            }

            // For the Chakra balance setter, decompile every unique validated direct
            // caller. Earlier exports only listed these callers and left their bodies
            // unexamined, which was insufficient to audit Q-cost dataflow.
            boolean auditingChakraSetter=false;
            for (Address target:targets)
                if (target.getOffset()==0x8001387CL) auditingChakraSetter=true;
            if (auditingChakraSetter) {
                for (Hit hit:validatedHits) {
                    if (hit.function!=null)
                        selectedForDecompile.putIfAbsent(hit.function.getEntryPoint().toString(),hit.function);
                }
                line("decompilation_mode=ALL_VALIDATED_DIRECT_CALLER_FUNCTIONS_FOR_0x8001387C");
            } else {
                // Preserve the previous seed-setter and bounded RNG-caller behavior.
                for (Hit hit:validatedHits) {
                    if (hit.function!=null && hit.target.getOffset()==0x80035DA8L)
                        selectedForDecompile.putIfAbsent(hit.function.getEntryPoint().toString(),hit.function);
                }
                for (Hit hit:validatedHits) {
                    if (hit.target.getOffset()==0x80035D78L && hit.function!=null
                        && selectedForDecompile.size()<13)
                        selectedForDecompile.putIfAbsent(hit.function.getEntryPoint().toString(),hit.function);
                }
                line("decompilation_mode=SEED_CALLERS_THEN_UP_TO_12_RNG_CALLERS");
            }
            int decompileTimeoutSeconds=auditingChakraSetter?45:15;
            line("");
            line("detailed_decompilation_timeout_seconds="+decompileTimeoutSeconds);
            line("detailed_decompilation_count="+selectedForDecompile.size());

            DecompInterface decompiler=new DecompInterface();
            decompiler.toggleCCode(true);
            decompiler.toggleSyntaxTree(false);
            if(!decompiler.openProgram(currentProgram))
                throw new IllegalStateException("Decompiler could not open imported program.");
            for(Function f:selectedForDecompile.values()) {
                monitor.checkCancelled();
                line("");
                line("=== SELECTED_CALLER_FUNCTION entry="+f.getEntryPoint()+" name="+f.getName()
                    +" body_bytes="+f.getBody().getNumAddresses()+" ===");
                DecompileResults result=decompiler.decompileFunction(f,decompileTimeoutSeconds,monitor);
                if(result!=null && result.decompileCompleted() && result.getDecompiledFunction()!=null) {
                    line("--- C_DECOMPILATION_BEGIN ---");
                    line(result.getDecompiledFunction().getC());
                    line("--- C_DECOMPILATION_END ---");
                } else {
                    line("decompile_status=FAILED_OR_TIMEOUT");
                    line("decompile_message="+(result==null?"null result":result.getErrorMessage()));
                }
            }
            decompiler.dispose();
            out.flush();
            if(out.checkError()) throw new IllegalStateException("Failed writing caller report.");
        }
    }
}
