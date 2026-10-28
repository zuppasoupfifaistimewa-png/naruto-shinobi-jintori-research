// ExportJumpTableContext.java
// Dumps a bounded range of raw 32-bit table words without executing game code
// or assuming the supplied Ghidra base is the runtime mapping.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.program.model.mem.MemoryAccessException;
import ghidra.program.model.listing.Instruction;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

public class ExportJumpTableContext extends GhidraScript {
    private int readWord(Address address) throws MemoryAccessException {
        return currentProgram.getMemory().getInt(address);
    }

    private String rawBytes(Address address, int length) throws MemoryAccessException {
        byte[] data = new byte[length];
        currentProgram.getMemory().getBytes(address, data);
        StringBuilder value = new StringBuilder();
        for (int i = 0; i < data.length; i++) {
            if (i != 0) value.append(' ');
            value.append(String.format("%02X", data[i] & 0xFF));
        }
        return value.toString();
    }

    private String sha256(byte[] data) throws Exception {
        byte[] digest = MessageDigest.getInstance("SHA-256").digest(data);
        StringBuilder text = new StringBuilder();
        for (byte b : digest) text.append(String.format("%02x", b & 0xFF));
        return text.toString();
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length != 3) {
            throw new IllegalArgumentException("Args: output-path table-address word-count");
        }
        Address start = toAddr(Long.decode(args[1]));
        int count = Integer.decode(args[2]);
        if (count < 1 || count > 64) {
            throw new IllegalArgumentException("word-count must be 1..64");
        }
        int length = count * 4;
        try (PrintWriter out = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out.println("# Bounded raw table word audit");
            out.println("program=" + currentProgram.getName());
            out.println("language=" + currentProgram.getLanguageID());
            out.println("analysis_mode=noanalysis; raw memory only");
            out.println("game_or_emulator_executed=no");
            out.println("runtime_mapping=HYPOTHESIS_ONLY");
            out.println("table_address=" + start);
            out.println("word_count=" + count);
            out.println("byte_count=" + length);
            MemoryBlock block = currentProgram.getMemory().getBlock(start);
            out.println("memory_block=" + (block == null ? "NONE" : block.getName()));
            if (block == null || !currentProgram.getMemory().contains(start)
                    || !currentProgram.getMemory().contains(start.add(length - 1))) {
                out.println("status=OUTSIDE_IMPORTED_RESOURCE");
                return;
            }

            byte[] bytes = new byte[length];
            currentProgram.getMemory().getBytes(start, bytes);
            out.println("block_start=" + block.getStart());
            out.println("block_end=" + block.getEnd());
            out.println("byte_offset_from_block=0x" + Long.toHexString(start.getOffset()
                    - block.getStart().getOffset()));
            out.println("raw_bytes=" + rawBytes(start, length));
            out.println("sha256_table_bytes=" + sha256(bytes));
            out.println("entries_begin");
            for (int i = 0; i < count; i++) {
                monitor.checkCancelled();
                Address at = start.add(i * 4L);
                int word = readWord(at);
                long unsigned = Integer.toUnsignedLong(word);
                Address possibleTarget = toAddr(unsigned);
                MemoryBlock targetBlock = currentProgram.getMemory().getBlock(possibleTarget);
                Instruction instruction = currentProgram.getListing().getInstructionAt(possibleTarget);
                out.println("index=" + i
                    + "\taddress=" + at
                    + "\toffset=0x" + Long.toHexString(at.getOffset() - block.getStart().getOffset())
                    + "\tword=0x" + String.format("%08X", word)
                    + "\tbytes=" + rawBytes(at, 4)
                    + "\ttarget_in_this_resource=" + currentProgram.getMemory().contains(possibleTarget)
                    + "\ttarget_block=" + (targetBlock == null ? "NONE" : targetBlock.getName())
                    + "\tinstruction_at_target=" + (instruction == null ? "NOT_DECODED" : instruction.toString()));
            }
            out.println("entries_end");
        }
    }
}
