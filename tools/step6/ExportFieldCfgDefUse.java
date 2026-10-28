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
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.BufferedWriter;
import java.util.ArrayList;
import java.util.List;
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
    // Bounded whole-view audit for the unresolved object-base slot used by the field trace.
    // This reports exact xrefs plus a heuristic LUI+signed-displacement pattern; it does not
    // claim complete alias analysis or runtime mapping.
    private long instructionWord(Instruction ins) throws Exception {
        byte[] b = new byte[ins.getLength()];
        currentProgram.getMemory().getBytes(ins.getAddress(), b);
        if (b.length != 4) return -1L;
        return ((long)b[0] & 0xffL)
            | (((long)b[1] & 0xffL) << 8)
            | (((long)b[2] & 0xffL) << 16)
            | (((long)b[3] & 0xffL) << 24);
    }

    private int destinationRegister(long word) {
        if (word < 0 || word > 0xffffffffL) return -1;
        int opcode = (int)((word >>> 26) & 0x3f);
        int rt = (int)((word >>> 16) & 0x1f);
        int rd = (int)((word >>> 11) & 0x1f);
        if (opcode == 0x00) {
            int funct = (int)(word & 0x3f);
            if (funct == 0x08 || funct == 0x0c || funct == 0x0d) return -1;
            return rd;
        }
        switch (opcode) {
            case 0x02: return -1;
            case 0x03: return 31;
            case 0x04: case 0x05: case 0x06: case 0x07:
            case 0x14: case 0x15: case 0x16: case 0x17:
            case 0x28: case 0x29: case 0x2a: case 0x2b:
            case 0x2c: case 0x2d: case 0x2e: case 0x2f:
                return -1;
            case 0x08: case 0x09: case 0x0a: case 0x0b:
            case 0x0c: case 0x0d: case 0x0e: case 0x0f:
            case 0x20: case 0x21: case 0x22: case 0x23:
            case 0x24: case 0x25: case 0x26: case 0x27:
            case 0x30: case 0x31: case 0x32: case 0x33:
            case 0x37: case 0x38: case 0x39: case 0x3a:
            case 0x3d: case 0x3f:
                return rt;
            default:
                return -1;
        }
    }

    private boolean isLoadStoreOpcode(int opcode) {
        return (opcode >= 0x20 && opcode <= 0x2f)
            || (opcode >= 0x30 && opcode <= 0x3f);
    }

    private void auditGlobalPointerSlot() throws Exception {
        final long slotValue = 0x8013A554L;
        final int highHalf = 0x8014;
        final int lowHalf = 0xA554;
        Address slot = toAddr(slotValue);
        line("");
        line("=== GLOBAL_POINTER_SLOT_AUDIT_BEGIN target=" + slot + " ===");
        line("scope=whole decoded DATA.BIN entry-1 program view; load base remains hypothetical");
        line("method=exact Ghidra xrefs plus bounded raw-MIPS LUI/high-half and load-store immediate candidate scan");
        line("runtime_mapping=NOT_VALIDATED; completeness=NOT_CLAIMED");
        try {
            byte[] raw = new byte[4];
            currentProgram.getMemory().getBytes(slot, raw);
            line(String.format("static_slot_bytes=%02X %02X %02X %02X", raw[0] & 0xff, raw[1] & 0xff, raw[2] & 0xff, raw[3] & 0xff));
            long value = ((long)raw[0] & 0xffL) | (((long)raw[1] & 0xffL) << 8)
                | (((long)raw[2] & 0xffL) << 16) | (((long)raw[3] & 0xffL) << 24);
            line(String.format("static_slot_word_little_endian=0x%08X (file-view bytes only; not runtime pointer)", value));
        } catch (Exception e) {
            line("static_slot_bytes=UNAVAILABLE reason=" + e.getClass().getSimpleName());
        }

        List<Reference> refs = new ArrayList<Reference>();
        ReferenceIterator refIt = currentProgram.getReferenceManager().getReferencesTo(slot);
        while (refIt.hasNext()) refs.add(refIt.next());
        line("exact_reference_manager_count=" + refs.size());
        for (Reference ref : refs) {
            Instruction ins = currentProgram.getListing().getInstructionAt(ref.getFromAddress());
            Function f = currentProgram.getFunctionManager().getFunctionContaining(ref.getFromAddress());
            line("exact_xref from=" + ref.getFromAddress()
                + " type=" + ref.getReferenceType()
                + " source=" + ref.getSource()
                + " function=" + (f == null ? "NONE" : f.getEntryPoint())
                + " instruction=" + (ins == null ? "NO_INSTRUCTION_AT_SOURCE" : ins.toString()));
        }

        List<Instruction> all = new ArrayList<Instruction>();
        InstructionIterator iter = currentProgram.getListing().getInstructions(true);
        while (iter.hasNext()) all.add(iter.next());
        int candidateCount = 0;
        int matchedLuiCount = 0;
        for (int i = 0; i < all.size(); i++) {
            Instruction ins = all.get(i);
            long w = instructionWord(ins);
            if (w < 0) continue;
            int opcode = (int)((w >>> 26) & 0x3f);
            int rs = (int)((w >>> 21) & 0x1f);
            int rt = (int)((w >>> 16) & 0x1f);
            int imm = (int)(w & 0xffff);
            if (!isLoadStoreOpcode(opcode) || imm != lowHalf) continue;
            long effective = (0x80140000L + (long)(short)imm) & 0xffffffffL;
            if (effective != slotValue) continue;
            candidateCount++;
            Function candidateFunction = currentProgram.getFunctionManager().getFunctionContaining(ins.getAddress());
            int foundLuiIndex = -1;
            boolean controlFlowBetween = false;
            int start = Math.max(0, i - 24);
            for (int j = i - 1; j >= start; j--) {
                Instruction prior = all.get(j);
                Function priorFunction = currentProgram.getFunctionManager().getFunctionContaining(prior.getAddress());
                if (candidateFunction != null && priorFunction != null
                    && !candidateFunction.getEntryPoint().equals(priorFunction.getEntryPoint())) break;
                long pw = instructionWord(prior);
                if (pw < 0) continue;
                int pop = (int)((pw >>> 26) & 0x3f);
                int prt = (int)((pw >>> 16) & 0x1f);
                int pimm = (int)(pw & 0xffff);
                if (pop == 0x0f && prt == rs && pimm == highHalf) {
                    foundLuiIndex = j;
                    break;
                }
                if (prior.getFlowType().isJump() || prior.getFlowType().isCall()
                    || prior.getFlowType().isConditional()) controlFlowBetween = true;
                if (destinationRegister(pw) == rs) break;
            }
            if (foundLuiIndex >= 0) matchedLuiCount++;
            line("candidate_load_store address=" + ins.getAddress()
                + " opcode=" + ins.getMnemonicString()
                + " base_reg_index=" + rs + " data_reg_index=" + rt
                + " signed_immediate=" + (short)imm
                + " computed_if_base_0x80140000=0x" + Long.toHexString(effective)
                + " function=" + (candidateFunction == null ? "NONE" : candidateFunction.getEntryPoint())
                + " preceding_lui_8014_same_base_within_24_instructions=" + (foundLuiIndex >= 0 ? all.get(foundLuiIndex).getAddress() : "NONE")
                + " intervening_control_flow=" + controlFlowBetween
                + " raw=" + ins.toString());
            int from = Math.max(0, i - 2);
            int to = Math.min(all.size() - 1, i + 2);
            for (int k = from; k <= to; k++) {
                Instruction ctx = all.get(k);
                line("  context " + ctx.getAddress() + " " + ctx.toString());
            }
        }
        line("decoded_instruction_count=" + all.size());
        line("candidate_load_store_count_for_signed_disp_A554=" + candidateCount);
        line("candidates_with_preceding_LUI_8014_same_base_within_24_instruction_records=" + matchedLuiCount);
        line("limits=heuristic same-register scan only; it may include false positives and misses split-immediate, computed, indirect, cross-function, alternate-base, undecoded, or runtime-relocated accesses");
        line("=== GLOBAL_POINTER_SLOT_AUDIT_END ===");
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
            auditGlobalPointerSlot();
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
