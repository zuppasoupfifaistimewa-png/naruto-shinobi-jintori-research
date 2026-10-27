// ExportResourceFunction.java
// Static same-address export for one DATA.BIN entry-1 candidate. The base is hypothetical.
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

public class ExportResourceFunction extends GhidraScript {
    private PrintWriter out;
    private void line(String s) { out.println(s); }
    private String bytes(Instruction ins) throws Exception {
        byte[] b = new byte[ins.getLength()];
        currentProgram.getMemory().getBytes(ins.getAddress(), b);
        StringBuilder sb = new StringBuilder();
        for (byte v : b) { if (sb.length() > 0) sb.append(' '); sb.append(String.format("%02X", v & 0xFF)); }
        return sb.toString();
    }
    private void dumpWindow(Address center, int before, int after) throws Exception {
        Instruction ins = currentProgram.getListing().getInstructionAt(center);
        if (ins == null) { line("window_status=NO_INSTRUCTION_AT_CENTER"); return; }
        Instruction first = ins;
        for (int i = 0; i < before && first.getPrevious() != null; i++) first = first.getPrevious();
        Instruction current = first;
        int emitted = 0;
        while (current != null && emitted < before + after + 1) {
            line(current.getAddress() + " bytes=[" + bytes(current) + "] " + current);
            current = current.getNext();
            emitted++;
        }
    }
    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2) throw new IllegalArgumentException("Args: output-path target-address");
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out = writer;
            Address target = toAddr(Long.decode(args[1]));
            Address rngCall = toAddr(0x800ED8E4L);
            Address rngTarget = toAddr(0x80035D78L);
            line("analysis=Ghidra static export of one DATA.BIN entry-1 candidate");
            line("program=" + currentProgram.getName());
            line("program_language=" + currentProgram.getLanguageID());
            line("resource=DATA.BIN entry index 1");
            line("resource_file_offset=0x10BB000");
            line("resource_bytes=596412");
            line("hypothetical_load_base=0x800D0000");
            line("runtime_mapping=HYPOTHESIS_ONLY_NOT_VALIDATED");
            line("game_or_emulator_executed=no");
            line("gameplay_input_sent=no");
            line("savestate_restored=no");
            line("binary_uploaded_as_artifact=no");
            line("target_requested=" + target);
            Instruction atTarget = currentProgram.getListing().getInstructionAt(target);
            line("instruction_at_target=" + (atTarget == null ? "NONE" : atTarget.toString()));
            Function f = currentProgram.getFunctionManager().getFunctionAt(target);
            if (f == null) {
                Function containing = currentProgram.getFunctionManager().getFunctionContaining(target);
                line("function_entry_validation=FAIL_TARGET_NOT_FUNCTION_ENTRY");
                line("containing_function_entry=" + (containing == null ? "NONE" : containing.getEntryPoint()));
                line("function_body_bytes=" + (containing == null ? "NONE" : containing.getBody().getNumAddresses()));
                line("boundary_status=NOT_VALIDATED");
                dumpWindow(target, 8, 12);
                line("export_status=PARTIAL_NO_VALIDATED_FUNCTION_ENTRY");
                out.flush();
                return;
            }
            Address endExclusive = f.getBody().getMaxAddress().add(1);
            line("function_entry_validation=PASS");
            line("function_name=" + f.getName());
            line("function_entry=" + f.getEntryPoint());
            line("function_body_min=" + f.getBody().getMinAddress());
            line("function_body_max=" + f.getBody().getMaxAddress());
            line("function_body_bytes=" + f.getBody().getNumAddresses());
            line("function_end_exclusive=" + endExclusive);
            line("function_thunk=" + f.isThunk());
            line("boundary_source=Ghidra automatic-analysis function body in this resource-only import");
            line("--- RAW_FUNCTION_BODY_BEGIN ---");
            InstructionIterator it = currentProgram.getListing().getInstructions(f.getBody(), true);
            int count = 0;
            boolean rngCallFound = false;
            while (it.hasNext()) {
                Instruction ins = it.next();
                line(ins.getAddress() + " bytes=[" + bytes(ins) + "] " + ins);
                if (ins.getAddress().equals(rngCall)) {
                    Address[] flows = ins.getFlows();
                    if (ins.getFlowType().isCall() && flows != null)
                        for (Address flow : flows) if (rngTarget.equals(flow)) rngCallFound = true;
                }
                count++;
                if (count > 4096) { line("RAW_FUNCTION_BODY_TRUNCATED=instruction_limit_4096"); break; }
            }
            line("--- RAW_FUNCTION_BODY_END ---");
            line("raw_instruction_count_emitted=" + count);
            line("expected_rng_callsite=" + rngCall);
            Instruction call = currentProgram.getListing().getInstructionAt(rngCall);
            line("rng_callsite_instruction=" + (call == null ? "NONE" : call.toString()));
            line("rng_callsite_bytes=" + (call == null ? "NONE" : bytes(call)));
            line("rng_callsite_direct_flow_to_0x80035D78=" + (rngCallFound ? "yes" : "no"));
            Instruction delay = currentProgram.getListing().getInstructionAt(rngCall.add(4));
            line("rng_callsite_delay_slot=" + (delay == null ? "NONE" : delay.toString()));
            line("rng_callsite_delay_slot_bytes=" + (delay == null ? "NONE" : bytes(delay)));
            DecompInterface decompiler = new DecompInterface();
            decompiler.toggleCCode(true);
            decompiler.toggleSyntaxTree(false);
            if (!decompiler.openProgram(currentProgram))
                throw new IllegalStateException("Decompiler could not open resource program.");
            DecompileResults result = decompiler.decompileFunction(f, 90, monitor);
            if (result != null && result.decompileCompleted() && result.getDecompiledFunction() != null) {
                line("--- C_DECOMPILATION_BEGIN ---");
                line(result.getDecompiledFunction().getC());
                line("--- C_DECOMPILATION_END ---");
                line("decompile_status=SUCCESS");
            } else {
                line("decompile_status=FAILED");
                line("decompile_message=" + (result == null ? "null result" : result.getErrorMessage()));
            }
            decompiler.dispose();
            line("export_status=SUCCESS");
            line("interpretation_limit=static candidate under hypothetical resource base; no gameplay rule or runtime mapping asserted");
            out.flush();
            if (out.checkError()) throw new IllegalStateException("Failed writing target function report.");
        }
    }
}
