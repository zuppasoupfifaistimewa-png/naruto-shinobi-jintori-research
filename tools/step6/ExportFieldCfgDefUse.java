// ExportFieldCfgDefUse.java
// CFG-aware SSA/P-code audit for selected DATA.BIN entry-1 functions.
// The resource load base is hypothetical, not a runtime mapping.
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.pcode.HighFunction;
import ghidra.program.model.pcode.PcodeBlock;
import ghidra.program.model.pcode.PcodeOp;
import ghidra.program.model.pcode.PcodeOpAST;
import ghidra.program.model.pcode.Varnode;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

public class ExportFieldCfgDefUse extends GhidraScript {
    private PrintWriter out;
    private static final long[] FIELD_OFFSETS = {
        0xB30L, 0xB38L, 0xB40L, 0xB44L, 0xB2AL, 0xA1CL, 0x5AACL
    };
    private void line(String s) { out.println(s); }
    private String address(Address a) { return a == null ? "NONE" : a.toString(); }
    private String varnode(Varnode v) {
        if (v == null) return "NONE";
        StringBuilder b = new StringBuilder(v.toString());
        b.append("{size=").append(v.getSize());
        if (v.isConstant()) b.append(",const=0x").append(Long.toHexString(v.getOffset()));
        b.append(",space=").append(v.getAddress().getAddressSpace().getName());
        b.append(",address=").append(v.getAddress());
        b.append(",input=").append(v.isInput());
        b.append(",unique=").append(v.isUnique()).append("}");
        return b.toString();
    }
    private boolean targetConstant(Varnode v) {
        if (v == null || !v.isConstant()) return false;
        long value = v.getOffset() & 0xffffffffL;
        for (long target : FIELD_OFFSETS) if (value == target) return true;
        return false;
    }
    private void traceDefinition(Varnode v, int depth, Set<String> seen, String prefix) {
        if (v == null) { line(prefix + " varnode=NONE"); return; }
        line(prefix + " varnode=" + varnode(v));
        if (depth <= 0) { line(prefix + " trace_stop=DEPTH_LIMIT"); return; }
        PcodeOp def = v.getDef();
        if (def == null) {
            line(prefix + " trace_stop=NO_SSA_DEFINITION (input/constant/address-tied or unavailable)");
            return;
        }
        String key = address(def.getSeqnum().getTarget()) + ":" + def.getOpcode() + ":" + v.toString();
        if (!seen.add(key)) { line(prefix + " trace_stop=REPEATED_SSA_NODE"); return; }
        PcodeBlock parent = def.getParent();
        line(prefix + " defining_op address=" + def.getSeqnum().getTarget()
            + " opcode=" + def.getMnemonic()
            + " block_index=" + (parent == null ? "NONE" : parent.getIndex())
            + " output=" + varnode(def.getOutput())
            + " input_count=" + def.getNumInputs());
        for (int i = 0; i < def.getNumInputs(); i++)
            line(prefix + " input_" + i + "=" + varnode(def.getInput(i)));
        if (def.getMnemonic().equals("MULTIEQUAL"))
            line(prefix + " note=PHI_MERGE_ACROSS_CONTROL_FLOW_PREDECESSORS");
        for (int i = 0; i < def.getNumInputs(); i++) {
            Varnode input = def.getInput(i);
            if (input != null && !input.isConstant())
                traceDefinition(input, depth - 1, seen, prefix + "." + i);
        }
    }
    private String bytesOf(Instruction ins) {
        try {
            byte[] b = new byte[ins.getLength()];
            currentProgram.getMemory().getBytes(ins.getAddress(), b);
            StringBuilder s = new StringBuilder();
            for (byte v : b) { if (s.length() > 0) s.append(' '); s.append(String.format("%02X", v & 0xff)); }
            return s.toString();
        } catch (Exception e) { return "UNAVAILABLE"; }
    }
    private void exportFunction(long requested, DecompInterface decompiler) throws Exception {
        Address target = toAddr(requested);
        line("");
        line("=== FUNCTION_AUDIT_BEGIN requested=" + target + " ===");
        Function f = currentProgram.getFunctionManager().getFunctionAt(target);
        if (f == null) {
            Function containing = currentProgram.getFunctionManager().getFunctionContaining(target);
            line("function_entry_validation=FAIL_NOT_FUNCTION_ENTRY");
            line("containing_function_entry=" + (containing == null ? "NONE" : containing.getEntryPoint()));
            line("audit_status=PARTIAL_BOUNDARY_NOT_VALIDATED");
            line("=== FUNCTION_AUDIT_END ===");
            return;
        }
        line("function_entry_validation=PASS");
        line("function_name=" + f.getName());
        line("function_entry=" + f.getEntryPoint());
        line("function_body_min=" + f.getBody().getMinAddress());
        line("function_body_max=" + f.getBody().getMaxAddress());
        line("function_body_address_count=" + f.getBody().getNumAddresses());
        line("function_body_boundary_basis=Ghidra_function_body_on_hypothetical_entry1_base");
        line("--- MIPS_BODY_BEGIN ---");
        InstructionIterator instructions = currentProgram.getListing().getInstructions(f.getBody(), true);
        while (instructions.hasNext()) {
            Instruction ins = instructions.next();
            line(ins.getAddress() + " bytes=" + bytesOf(ins) + " " + ins);
        }
        line("--- MIPS_BODY_END ---");
        DecompileResults result = decompiler.decompileFunction(f, 120, monitor);
        if (result == null || !result.decompileCompleted() || result.getHighFunction() == null) {
            line("decompile_status=FAILED");
            line("decompile_message=" + (result == null ? "null result" : result.getErrorMessage()));
            line("audit_status=PARTIAL_NO_SSA");
            line("=== FUNCTION_AUDIT_END ===");
            return;
        }
        line("decompile_status=SUCCESS");
        HighFunction high = result.getHighFunction();
        line("pcode_analysis=high-level SSA p-code with parent basic-block IDs; not a runtime trace");
        line("--- DECOMPILATION_BEGIN ---");
        if (result.getDecompiledFunction() != null) line(result.getDecompiledFunction().getC());
        line("--- DECOMPILATION_END ---");
        line("--- SSA_PCODE_BEGIN ---");
        Iterator<PcodeOpAST> ops = high.getPcodeOps();
        int count = 0, matched = 0;
        while (ops.hasNext()) {
            PcodeOp op = ops.next();
            count++;
            PcodeBlock parent = op.getParent();
            StringBuilder rendered = new StringBuilder();
            rendered.append("pc=").append(op.getSeqnum().getTarget())
                .append(" block=").append(parent == null ? "NONE" : parent.getIndex())
                .append(" opcode=").append(op.getMnemonic())
                .append(" output=").append(varnode(op.getOutput())).append(" inputs=");
            boolean hasFieldConstant = false;
            for (int i = 0; i < op.getNumInputs(); i++) {
                Varnode v = op.getInput(i);
                if (i > 0) rendered.append(" | ");
                rendered.append(i).append(":").append(varnode(v));
                if (targetConstant(v)) hasFieldConstant = true;
            }
            boolean memoryOp = op.getMnemonic().equals("LOAD") || op.getMnemonic().equals("STORE");
            boolean cfgOp = op.getMnemonic().equals("CBRANCH") || op.getMnemonic().equals("BRANCH")
                || op.getMnemonic().equals("BRANCHIND") || op.getMnemonic().equals("MULTIEQUAL");
            if (hasFieldConstant || memoryOp || cfgOp) {
                line(rendered.toString());
                if (hasFieldConstant) {
                    matched++;
                    line("  FIELD_OFFSET_CONSTANT_MATCH=yes");
                    if (op.getOutput() != null)
                        traceDefinition(op.getOutput(), 4, new HashSet<String>(), "  def_chain_output");
                    for (int i = 0; i < op.getNumInputs(); i++) {
                        Varnode input = op.getInput(i);
                        if (input != null && !input.isConstant())
                            traceDefinition(input, 4, new HashSet<String>(), "  def_chain_input_" + i);
                    }
                }
            }
        }
        line("--- SSA_PCODE_END ---");
        line("pcode_ops_total=" + count);
        line("pcode_ops_with_target_field_constant=" + matched);
        line("control_flow_ops_emitted=yes");
        line("ssa_def_use_basis=Varnode definitions and MULTIEQUAL merges across CFG blocks when present");
        line("limitations=SSA may not resolve aliasing through arbitrary pointer loads, indirect calls, other functions, or runtime relocation; hypothetical base only");
        line("audit_status=SUCCESS_STATIC_SSA_EXPORT");
        line("=== FUNCTION_AUDIT_END ===");
    }
    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2) throw new IllegalArgumentException("Args: output-path function-entry-address [more]");
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out = writer;
            line("analysis=Ghidra CFG-aware static field provenance using decompiler SSA/P-code");
            line("program=" + currentProgram.getName());
            line("resource=DATA.BIN entry index 1; file_offset=0x10BB000; bytes=596412");
            line("hypothetical_load_base=0x800D0000");
            line("runtime_mapping=HYPOTHESIS_ONLY_NOT_VALIDATED");
            line("game_or_emulator_executed=no");
            line("gameplay_input_sent=no");
            line("savestate_restored=no");
            line("private_binary_uploaded_as_artifact=no");
            DecompInterface decompiler = new DecompInterface();
            decompiler.toggleCCode(true);
            decompiler.toggleSyntaxTree(true);
            if (!decompiler.openProgram(currentProgram))
                throw new IllegalStateException("Decompiler could not open entry-1 program.");
            for (int i = 1; i < args.length; i++) exportFunction(Long.decode(args[i]), decompiler);
            decompiler.dispose();
            out.flush();
            if (out.checkError()) throw new IllegalStateException("Failed writing CFG/SSA audit report.");
        }
    }
}
