// ExportEntry0TargetFunction.java
// Bounded, targeted raw-MIPS disassembly/decompilation for selected DATA.BIN entry0 addresses.
// This is static only. A manually-created function from local control flow is a candidate
// function boundary, not proof of runtime reachability or the resource's actual RAM mapping.
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;

public class ExportEntry0TargetFunction extends GhidraScript {
    private PrintWriter out;
    private void line(String s) { out.println(s); }

    private String rawBytes(Instruction ins) throws Exception {
        byte[] bytes = new byte[ins.getLength()];
        currentProgram.getMemory().getBytes(ins.getAddress(), bytes);
        StringBuilder b = new StringBuilder();
        for (byte value : bytes) {
            if (b.length() > 0) b.append(' ');
            b.append(String.format("%02X", value & 0xFF));
        }
        return b.toString();
    }

    private void dumpWindow(Address address, int before, int after) throws Exception {
        Instruction center = currentProgram.getListing().getInstructionAt(address);
        if (center == null) {
            line("window_status=NO_DECODED_INSTRUCTION_AT_TARGET");
            return;
        }
        Instruction first = center;
        for (int i = 0; i < before && first.getPrevious() != null; i++) first = first.getPrevious();
        Instruction last = center;
        for (int i = 0; i < after && last.getNext() != null; i++) last = last.getNext();
        for (Instruction ins = first; ins != null; ins = ins.getNext()) {
            line("  " + ins.getAddress() + " bytes=[" + rawBytes(ins) + "] " + ins);
            if (ins.getAddress().equals(last.getAddress())) break;
        }
    }

    private void dumpRawJalCandidates(Address target) throws Exception {
        MemoryBlock block = currentProgram.getMemory().getBlock(target);
        line("");
        line("=== RAW_JAL_WORD_SCAN_TO_TARGET " + target + " ===");
        line("scan_semantics=raw word pattern only; embedded data can cause false positives");
        if (block == null) {
            line("scan_status=NO_MEMORY_BLOCK");
            return;
        }
        long start = block.getStart().getOffset();
        long end = block.getEnd().getOffset();
        int count = 0;
        for (long pc = (start + 3L) & ~3L; pc + 3L <= end; pc += 4L) {
            monitor.checkCancelled();
            Address at = toAddr(pc);
            int word;
            try {
                word = currentProgram.getMemory().getInt(at);
            } catch (Exception ignored) { continue; }
            if ((word >>> 26) != 3) continue; // raw MIPS JAL opcode
            long resolved = ((pc + 4L) & 0xF0000000L) | ((Integer.toUnsignedLong(word) & 0x03FFFFFFL) << 2);
            if (resolved == target.getOffset()) {
                Instruction decoded = currentProgram.getListing().getInstructionAt(at);
                line("candidate_site=" + at + "\tword=0x" + String.format("%08X", word)
                    + "\tdecoded_instruction=" + (decoded == null ? "NO" : decoded.toString()));
                count++;
            }
        }
        line("raw_jal_word_candidate_count=" + count);
        line("interpretation=address-pattern candidates are not accepted callers without decoded instruction/control-flow confirmation");
    }

    private void dumpTarget(Address target, DecompInterface decompiler) throws Exception {
        line("");
        line("=== TARGET " + target + " ===");
        line("resource_base=0x800AD000 (hypothesis only)");
        line("target_offset_under_hypothesis=0x" + Long.toHexString(target.getOffset() - 0x800AD000L));
        line("runtime_mapping=NOT_VALIDATED");
        if (!currentProgram.getMemory().contains(target)) {
            line("target_status=OUTSIDE_IMPORTED_MEMORY");
            return;
        }

        Instruction at = currentProgram.getListing().getInstructionAt(target);
        line("instruction_before_local_disassembly=" + (at == null ? "NONE" : at.toString()));
        if (at == null) {
            try {
                disassemble(target);
                at = currentProgram.getListing().getInstructionAt(target);
                line("target_local_disassemble=ATTEMPTED");
            } catch (Exception e) {
                line("target_local_disassemble=FAILED " + e.getMessage());
            }
        }
        Function f = currentProgram.getFunctionManager().getFunctionAt(target);
        if (f == null && at != null) {
            try {
                createFunction(target, "FUN_" + target.toString().substring(2).toLowerCase());
            } catch (Exception e) {
                line("manual_function_creation=FAILED " + e.getMessage());
            }
            f = currentProgram.getFunctionManager().getFunctionAt(target);
        }
        if (f == null) {
            line("function_at_target=NONE");
            dumpWindow(target, 8, 40);
            dumpRawJalCandidates(target);
            return;
        }

        line("function_name=" + f.getName());
        line("function_entry=" + f.getEntryPoint());
        line("function_body_address_count=" + f.getBody().getNumAddresses());
        line("function_signature=" + f.getSignature());
        line("function_boundary_confidence=MANUALLY_SEEDED_FROM_TARGET; validate raw return/tail jumps");

        int n = 0;
        line("--- RAW_FUNCTION_BODY_BEGIN ---");
        InstructionIterator it = currentProgram.getListing().getInstructions(f.getBody(), true);
        while (it.hasNext()) {
            Instruction ins = it.next();
            line(ins.getAddress() + " bytes=[" + rawBytes(ins) + "] " + ins);
            n++;
            if (n >= 2048) {
                line("raw_body_truncated=instruction_limit_2048");
                break;
            }
        }
        line("--- RAW_FUNCTION_BODY_END ---");
        line("raw_instruction_count_emitted=" + n);

        DecompileResults result = decompiler.decompileFunction(f, 60, monitor);
        if (result != null && result.decompileCompleted() && result.getDecompiledFunction() != null) {
            line("--- C_DECOMPILATION_BEGIN ---");
            line(result.getDecompiledFunction().getC());
            line("--- C_DECOMPILATION_END ---");
            line("decompile_status=SUCCESS");
        } else {
            line("decompile_status=FAILED");
            line("decompile_message=" + (result == null ? "null result" : result.getErrorMessage()));
        }

        int refsCount = 0;
        line("--- REFERENCES_TO_TARGET_BEGIN ---");
        ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(f.getEntryPoint());
        while (refs.hasNext()) {
            Reference ref = refs.next();
            line("reference_from=" + ref.getFromAddress() + "\ttype=" + ref.getReferenceType()
                + "\tsource=" + ref.getSource());
            refsCount++;
        }
        line("references_in_this_entry0_view=" + refsCount);
        line("--- REFERENCES_TO_TARGET_END ---");
        dumpWindow(target, 8, 16);
        dumpRawJalCandidates(target);
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2)
            throw new IllegalArgumentException("Args: output-path target-address [target-address ...]");
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out = writer;
            line("analysis=bounded targeted DATA.BIN entry0 function inspection");
            line("program=" + currentProgram.getName());
            line("program_language=" + currentProgram.getLanguageID());
            line("gameplay_or_emulator_executed=no");
            line("gameplay_input_sent=no");
            line("savestate_restored=no");
            line("private_binary_uploaded_as_artifact=no");
            DecompInterface decompiler = new DecompInterface();
            decompiler.toggleCCode(true);
            decompiler.toggleSyntaxTree(false);
            if (!decompiler.openProgram(currentProgram))
                throw new IllegalStateException("Could not open target program for decompilation.");
            for (int i = 1; i < args.length; i++) {
                monitor.checkCancelled();
                dumpTarget(toAddr(Long.decode(args[i])), decompiler);
            }
            decompiler.dispose();
            out.flush();
            if (out.checkError()) throw new IllegalStateException("Failed writing target-function report.");
        }
    }
}
