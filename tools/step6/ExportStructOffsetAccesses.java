// ExportStructOffsetAccesses.java
// Search already-decoded instructions for exact immediate offsets of the Step 6 candidate fields.
// Hits are candidates only: an immediate constant alone does not establish a struct-field semantic.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.scalar.Scalar;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.HashSet;
import java.util.Set;
import java.util.TreeMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ExportStructOffsetAccesses extends GhidraScript {
    private PrintWriter out;
    private DecompInterface decompiler;
    private final Set<String> dumpedFunctions = new HashSet<>();
    private static final long BASE = 0x800D0000L;
    private static final long LENGTH = 0x919BCL;
    private static final int MAX_REPORTED_PER_OFFSET = 200;
    private static final long[] TARGETS = {
        0xB30L, 0xB38L, 0xB40L, 0xB44L, 0xB2AL,
        0x58BL, 0x2E9L, 0x2E5L, 0x5D2L, 0x618L, 0x61CL, 0x94AL, 0x22L
    };
    private final Map<Long, Integer> counts = new LinkedHashMap<>();
    private final Map<Long, Integer> emitted = new LinkedHashMap<>();
    private final Map<Long, Integer> memoryCounts = new LinkedHashMap<>();
    private final Map<Long, Integer> memoryEmitted = new LinkedHashMap<>();
    // Inventory every decoded direct base+displacement memory operand, not only named candidates.
    private final Map<Long, int[]> displacementInventory = new TreeMap<>();
    private static final Set<Long> UNBOUNDED_FIELD_OFFSETS = new HashSet<>();
    static {
        UNBOUNDED_FIELD_OFFSETS.add(0xB30L);
        UNBOUNDED_FIELD_OFFSETS.add(0xB38L);
        UNBOUNDED_FIELD_OFFSETS.add(0xB40L);
        UNBOUNDED_FIELD_OFFSETS.add(0xB44L);
    }
    private static final Pattern DESTINATION_REGISTER = Pattern.compile("^\\S+\\s+([a-z][a-z0-9]*)\\s*,", Pattern.CASE_INSENSITIVE);
    private static final Pattern REGISTER_TOKEN = Pattern.compile("(?i)^(?:zero|at|v[01]|a[0-3]|t[0-9]|s[0-7]|k[01]|gp|sp|fp|ra)$");
    private static final Pattern MEMORY_DISPLACEMENT = Pattern.compile("(?i)^_?(lb|lbu|lh|lhu|lw|lwl|lwr|lwu|sb|sh|sw|swl|swr|sc)\\s+[^,]+,\\s*(-?(?:0x[0-9a-f]+|[0-9]+))\\(([^)]+)\\)");

    private void line(String s) { out.println(s); }

    private String hex(long value) { return String.format("0x%X", value); }

    private boolean isStoreMnemonic(String mnemonic) {
        String m = mnemonic.toLowerCase();
        return m.matches("sb|sh|sw|sd|swl|swr|sdl|sdr|sc|scd");
    }

    private boolean isMemoryMnemonic(String mnemonic) {
        String m = mnemonic.toLowerCase();
        return m.matches("l[bhdwq]|lbu|lhu|lwu|lwl|lwr|sb|sh|sw|sd|swl|swr|sdl|sdr|sc|scd");
    }

    private String bytes(Instruction ins) {
        try {
            byte[] b = ins.getBytes();
            StringBuilder sb = new StringBuilder();
            for (byte value : b) sb.append(String.format("%02X", value & 0xFF));
            return sb.toString();
        } catch (Exception e) {
            return "UNAVAILABLE";
        }
    }

    private String refTargets(Address from) {
        StringBuilder sb = new StringBuilder();
        for (Reference r : currentProgram.getReferenceManager().getReferencesFrom(from)) {
            if (sb.length() > 0) sb.append(",");
            sb.append(r.getReferenceType()).append("->").append(r.getToAddress());
            if (sb.length() > 240) { sb.append(",..."); break; }
        }
        return sb.length() == 0 ? "none" : sb.toString();
    }

    private void dumpMatch(Instruction ins, int operand, Scalar scalar, long target, long count) {
        int shown = emitted.getOrDefault(target, 0);
        if (shown >= MAX_REPORTED_PER_OFFSET) return;
        emitted.put(target, shown + 1);
        Function f = getFunctionContaining(ins.getAddress());
        long rawAddress = ins.getAddress().getOffset();
        long fileOffset = rawAddress - BASE;
        line("MATCH field=+" + hex(target) + " occurrence=" + (shown + 1) + " total_after_scan=" + count);
        line("  address=" + ins.getAddress() + " entry1_file_offset=" + (fileOffset >= 0 && fileOffset < LENGTH ? hex(fileOffset) : "OUTSIDE_HYPOTHETICAL_ENTRY1"));
        line("  instruction_bytes=" + bytes(ins) + " mnemonic=" + ins.getMnemonicString() + " text=" + ins.toString());
        line("  operand_index=" + operand + " scalar_unsigned=" + hex(scalar.getUnsignedValue())
            + " scalar_signed=" + scalar.getSignedValue() + " operand_type=0x" + Integer.toHexString(ins.getOperandType(operand)));
        line("  access_class=" + (isMemoryMnemonic(ins.getMnemonicString()) ? "LOAD_STORE_OPCODE_CANDIDATE" : "OTHER_IMMEDIATE; inspect manually"));
        line("  function=" + (f == null ? "NONE_OR_UNMAPPED" : f.getName()) + " function_entry=" + (f == null ? "NONE" : f.getEntryPoint()));
        Instruction p2 = ins.getPrevious();
        Instruction p1 = p2 == null ? null : p2.getPrevious();
        Instruction n1 = ins.getNext();
        Instruction n2 = n1 == null ? null : n1.getNext();
        line("  context_previous2=" + (p1 == null ? "NONE" : p1.toString()));
        line("  context_previous1=" + (p2 == null ? "NONE" : p2.toString()));
        line("  context_next1=" + (n1 == null ? "NONE" : n1.toString()));
        line("  context_next2=" + (n2 == null ? "NONE" : n2.toString()));
        line("  references_from_instruction=" + refTargets(ins.getAddress()));
    }

    private void dumpContextAndFunction(Instruction ins, Function f, long target) {
        Instruction first = ins;
        for (int i = 0; i < 8 && first.getPrevious() != null; i++) first = first.getPrevious();
        line("=== MEMORY_ACCESS_CONTEXT_BEGIN address=" + ins.getAddress() + " ===");
        Instruction current = first;
        for (int i = 0; current != null && i < 17; i++, current = current.getNext()) {
            line("  " + current.getAddress() + " bytes=[" + bytes(current) + "] "
                + current.getMnemonicString() + " " + current.toString());
            if (current.getAddress().equals(ins.getAddress()) && current.getNext() == null) break;
        }
        line("=== MEMORY_ACCESS_CONTEXT_END ===");
        if (f == null) {
            line("decompiled_function=NO_FUNCTION_BOUNDARY");
            return;
        }
        String entry = f.getEntryPoint().toString();
        line("function_entry_for_memory_access=" + entry + " function_name=" + f.getName()
            + " body_bytes=" + f.getBody().getNumAddresses());
        if (!dumpedFunctions.add(entry)) return;
        line("=== FIELD_ACCESS_FUNCTION_DECOMPILATION_BEGIN entry=" + entry + " ===");
        DecompileResults result = decompiler.decompileFunction(f, 90, monitor);
        if (result != null && result.decompileCompleted() && result.getDecompiledFunction() != null) {
            line(result.getDecompiledFunction().getC());
            line("decompile_status=SUCCESS");
        } else {
            line("decompile_status=FAILED");
            line("decompile_message=" + (result == null ? "null result" : result.getErrorMessage()));
        }
        line("=== FIELD_ACCESS_FUNCTION_DECOMPILATION_END entry=" + entry + " ===");
        if (target == 0xB30L || target == 0xB38L || target == 0xB40L || target == 0xB44L) {
            dumpIncomingFunctionReferences(f);
        }
    }

    private void dumpIncomingFunctionReferences(Function f) {
        line("=== FUNCTION_ENTRY_REFERENCES_BEGIN entry=" + f.getEntryPoint() + " name=" + f.getName() + " ===");
        ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(f.getEntryPoint());
        int total = 0;
        int emittedRefs = 0;
        final int maxRefs = 50;
        while (refs.hasNext()) {
            Reference ref = refs.next();
            total++;
            if (emittedRefs >= maxRefs) continue;
            emittedRefs++;
            Address from = ref.getFromAddress();
            Instruction ins = currentProgram.getListing().getInstructionAt(from);
            Function owner = getFunctionContaining(from);
            line("INCOMING_REF from=" + from + " type=" + ref.getReferenceType()
                + " source=" + ref.getSource() + " operand=" + ref.getOperandIndex()
                + " caller_entry=" + (owner == null ? "NONE" : owner.getEntryPoint())
                + " caller_name=" + (owner == null ? "NONE" : owner.getName()));
            if (ins == null) {
                line("  callsite_instruction=NOT_DECODED");
                continue;
            }
            Instruction first = ins;
            for (int i = 0; i < 4 && first.getPrevious() != null; i++) first = first.getPrevious();
            line("  CALLSITE_CONTEXT_BEGIN");
            Instruction current = first;
            for (int i = 0; current != null && i < 9; i++, current = current.getNext()) {
                line("    " + current.getAddress() + " bytes=[" + bytes(current) + "] "
                    + current.getMnemonicString() + " " + current.toString());
            }
            line("  CALLSITE_CONTEXT_END");
        }
        line("incoming_function_reference_count=" + total
            + (total > maxRefs ? " emitted=" + maxRefs + " cap_reached=yes" : " emitted=" + emittedRefs));
        line("=== FUNCTION_ENTRY_REFERENCES_END ===");
    }

    private void dumpBaseRegisterDefinitionTrace(Instruction ins, String initialRegister) {
        line("=== BASE_REGISTER_TRACE_BEGIN access=" + ins.getAddress() + " initial=" + initialRegister + " ===");
        Function accessFunction = getFunctionContaining(ins.getAddress());
        String currentRegister = initialRegister.trim();
        int definitions = 0;
        for (int link = 0; link < 6 && REGISTER_TOKEN.matcher(currentRegister).matches(); link++) {
            Instruction cursor = ins.getPrevious();
            boolean found = false;
            for (int i = 0; cursor != null && i < 24; i++, cursor = cursor.getPrevious()) {
                Function owner = getFunctionContaining(cursor.getAddress());
                if (accessFunction != null && (owner == null || !owner.getEntryPoint().equals(accessFunction.getEntryPoint()))) {
                    line("  trace_stop=function_boundary_or_unknown at=" + cursor.getAddress());
                    break;
                }
                String mnemonic = cursor.getMnemonicString().toLowerCase();
                if (mnemonic.startsWith("b") || mnemonic.equals("j") || mnemonic.equals("jal")
                        || mnemonic.equals("jalr") || mnemonic.equals("jr")) {
                    line("  trace_stop=control_flow at=" + cursor.getAddress() + " instruction=" + cursor.toString());
                    break;
                }
                if (isStoreMnemonic(mnemonic)) continue; // stores do not define the first operand register
                Matcher def = DESTINATION_REGISTER.matcher(cursor.toString().trim());
                if (!def.find() || !def.group(1).equalsIgnoreCase(currentRegister)) continue;
                found = true;
                definitions++;
                line("  definition_" + definitions + " register=" + currentRegister + " address=" + cursor.getAddress()
                        + " bytes=" + bytes(cursor) + " instruction=" + cursor.toString());
                String[] split = cursor.toString().trim().split("\\s+", 2);
                if (split.length < 2 || !split[0].equalsIgnoreCase("move")) {
                    line("  alias_trace_stop=definition_not_simple_move");
                    break;
                }
                String[] operands = split[1].split(",");
                if (operands.length < 2) {
                    line("  alias_trace_stop=unparsed_move_operands");
                    break;
                }
                String sourceRegister = operands[1].trim();
                if (!REGISTER_TOKEN.matcher(sourceRegister).matches()) {
                    line("  alias_trace_stop=move_source_not_register source=" + sourceRegister);
                    break;
                }
                currentRegister = sourceRegister;
                break;
            }
            if (!found) {
                line("  alias_trace_stop=no_destination_definition_within_linear_window register=" + currentRegister);
                break;
            }
        }
        line("  traced_move_definitions=" + definitions + " interpretation=bounded linear alias hints only");
        line("=== BASE_REGISTER_TRACE_END ===");
    }

    private void dumpMemoryMatch(Instruction ins, long target, long displacement, long count, String baseRegister, String accessDirection) {
        int shown = memoryEmitted.getOrDefault(target, 0);
        if (shown >= MAX_REPORTED_PER_OFFSET && !UNBOUNDED_FIELD_OFFSETS.contains(target)) return;
        memoryEmitted.put(target, shown + 1);
        Function f = getFunctionContaining(ins.getAddress());
        long rawAddress = ins.getAddress().getOffset();
        long fileOffset = rawAddress - BASE;
        line("MEMORY_MATCH field=+" + hex(target) + " occurrence=" + (shown + 1) + " total_after_scan=" + count);
        line("  address=" + ins.getAddress() + " entry1_file_offset=" + (fileOffset >= 0 && fileOffset < LENGTH ? hex(fileOffset) : "OUTSIDE_HYPOTHETICAL_ENTRY1"));
        line("  instruction_bytes=" + bytes(ins) + " mnemonic=" + ins.getMnemonicString() + " text=" + ins.toString());
        line("  parsed_memory_displacement=" + hex(displacement) + " access_class=LOAD_STORE_OPCODE_CANDIDATE");
        line("  base_register=" + baseRegister + " access_direction=" + accessDirection);
        line("  function=" + (f == null ? "NONE_OR_UNMAPPED" : f.getName()) + " function_entry=" + (f == null ? "NONE" : f.getEntryPoint()));
        line("  references_from_instruction=" + refTargets(ins.getAddress()));
        dumpContextAndFunction(ins, f, target);
        dumpBaseRegisterDefinitionTrace(ins, baseRegister);
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 1 || args[0].trim().isEmpty())
            throw new IllegalArgumentException("Provide the output report path.");
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out = writer;
            line("analysis=Ghidra decoded-instruction scan for exact immediate offsets");
            line("resource=DATA.BIN entry 1");
            line("entry_bytes=596412 (0x919BC)");
            line("sha256=9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a");
            line("hypothetical_base=0x800D0000; runtime_mapping=NOT_VALIDATED");
            line("game_or_emulator_executed=no");
            line("private_binary_uploaded=no");
            line("field_semantics=UNASSIGNED; every hit requires instruction-context review");
            line("extended_operand_context=8 instructions before and after each memory-displacement match");
            line("direct_memory_operand_inventory=ALL decoded base-plus-displacement operands in candidate entry view");
            line("direct_memory_operand_match_cap_for_B30_B38_B40_B44=NONE");
            line("base_register_trace=up to 24 prior linear instructions per alias; stops at branch/call/return and is not whole-program pointer analysis");
            decompiler = new DecompInterface();
            decompiler.toggleCCode(true);
            decompiler.toggleSyntaxTree(false);
            if (!decompiler.openProgram(currentProgram))
                throw new IllegalStateException("Could not initialize decompiler for memory-field context.");
            for (long t : TARGETS) { counts.put(t, 0); emitted.put(t, 0); memoryCounts.put(t, 0); memoryEmitted.put(t, 0); }
            // Self-test against known MIPS memory-operand syntax before scanning the program.
            Matcher fixture = MEMORY_DISPLACEMENT.matcher("sb v0,0x2e9(v1)");
            if (!fixture.find() || Long.decode(fixture.group(2)) != 0x2E9L)
                throw new IllegalStateException("memory displacement parser regression: known sb v0,0x2e9(v1) must parse");
            line("memory_displacement_parser_fixture=PASS sample=sb_v0,0x2e9(v1)");

            InstructionIterator it = currentProgram.getListing().getInstructions(true);
            long instructions = 0, inEntry = 0;
            while (it.hasNext()) {
                monitor.checkCancelled();
                Instruction ins = it.next();
                instructions++;
                if (!currentProgram.getMemory().contains(ins.getAddress())) continue;
                long addr = ins.getAddress().getOffset();
                if (addr < BASE || addr >= BASE + LENGTH) continue;
                inEntry++;
                for (int op = 0; op < ins.getNumOperands(); op++) {
                    Scalar scalar;
                    try { scalar = ins.getScalar(op); } catch (Exception e) { scalar = null; }
                    if (scalar == null) continue;
                    long immediate16 = scalar.getUnsignedValue() & 0xFFFFL;
                    for (long target : TARGETS) {
                        if (immediate16 != target) continue;
                        int old = counts.get(target);
                        int now = old + 1;
                        counts.put(target, now);
                        dumpMatch(ins, op, scalar, target, now);
                    }
                }
                Matcher memory = MEMORY_DISPLACEMENT.matcher(ins.toString().trim());
                if (memory.find()) {
                    long displacement;
                    try { displacement = Long.decode(memory.group(2)); }
                    catch (NumberFormatException e) { displacement = Long.MIN_VALUE; }
                    String baseRegister = memory.group(3).trim();
                    String mnemonic = ins.getMnemonicString().toLowerCase();
                    int[] histogram = displacementInventory.get(displacement);
                    if (histogram == null) {
                        histogram = new int[3]; // total direct operands, reads, writes
                        displacementInventory.put(displacement, histogram);
                    }
                    histogram[0]++;
                    if (mnemonic.startsWith("l")) histogram[1]++;
                    else if (isStoreMnemonic(mnemonic)) histogram[2]++;
                    String direction = mnemonic.startsWith("l") ? "READ" : (isStoreMnemonic(mnemonic) ? "WRITE" : "UNKNOWN");
                    for (long target : TARGETS) {
                        if (displacement != target) continue;
                        int now = memoryCounts.get(target) + 1;
                        memoryCounts.put(target, now);
                        dumpMemoryMatch(ins, target, displacement, now, baseRegister, direction);
                    }
                }
            }
            line("");
            line("=== SUMMARY ===");
            line("decoded_instructions_all_program=" + instructions);
            line("decoded_instructions_within_hypothetical_entry1=" + inEntry);
            line("match_output_cap_per_offset=" + MAX_REPORTED_PER_OFFSET);
            for (long t : TARGETS)
                line("offset=+" + hex(t) + " decoded_immediate_hits=" + counts.get(t)
                    + " immediate_emitted=" + emitted.get(t)
                    + " memory_displacement_hits=" + memoryCounts.get(t)
                    + " memory_emitted=" + memoryEmitted.get(t)
                    + (counts.get(t) > MAX_REPORTED_PER_OFFSET || memoryCounts.get(t) > MAX_REPORTED_PER_OFFSET ? " CAP_REACHED; additional hits omitted" : ""));
            line("=== DIRECT_MEMORY_DISPLACEMENT_INVENTORY_BEGIN ===");
            line("format=disp total_direct_operands reads writes");
            for (Map.Entry<Long, int[]> item : displacementInventory.entrySet()) {
                int[] v = item.getValue();
                line("direct_displacement=" + hex(item.getKey()) + " total=" + v[0] + " reads=" + v[1] + " writes=" + v[2]);
            }
            line("=== DIRECT_MEMORY_DISPLACEMENT_INVENTORY_END ===");
            line("limitation=Inventory covers only Ghidra-decoded direct displacement(base) instructions in candidate base view. Base-register trace is linear and bounded. It does not prove object identity or capture pointer arithmetic, split immediates, aliases beyond trace window, undecoded code or alternate structure bases.");
            out.flush();
            if (out.checkError()) throw new IllegalStateException("Failed writing offset-access report.");
            decompiler.dispose();
        }
    }
}
