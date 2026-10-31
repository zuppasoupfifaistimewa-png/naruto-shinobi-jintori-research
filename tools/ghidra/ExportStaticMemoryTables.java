// ExportStaticMemoryTables.java
// Read-only dump of selected main-EXE data slots and compact tables.
// File-image values are not automatically runtime values.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;

public class ExportStaticMemoryTables extends GhidraScript {
    private PrintWriter out;
    private void line(String s) { out.println(s); }
    private String hex(long v) { return String.format("0x%08X", v & 0xffffffffL); }

    private void dump(String specification) throws Exception {
        String[] parts = specification.split(":", 2);
        if (parts.length != 2) throw new IllegalArgumentException("Expected address:length, got " + specification);
        long rawAddress = Long.decode(parts[0]);
        int length = Integer.decode(parts[1]);
        if (length < 1 || length > 65536) throw new IllegalArgumentException("Invalid range length: " + length);
        Address address = toAddr(rawAddress);
        line("");
        line("=== DATA_RANGE_BEGIN address=" + hex(rawAddress) + " bytes=" + length + " ===");
        line("loaded_image_range=yes; this is the executable file image, not a runtime memory snapshot");
        if (!currentProgram.getMemory().contains(address)
            || !currentProgram.getMemory().contains(toAddr(rawAddress + length - 1))) {
            line("range_status=OUTSIDE_IMPORTED_MEMORY_OR_UNMAPPED");
            line("=== DATA_RANGE_END ===");
            return;
        }
        byte[] bytes = new byte[length];
        currentProgram.getMemory().getBytes(address, bytes);
        StringBuilder all = new StringBuilder();
        for (int i = 0; i < bytes.length; i++) {
            if (i > 0) all.append(' ');
            all.append(String.format("%02X", bytes[i] & 0xff));
        }
        line("raw_hex=" + all.toString());
        for (int off = 0; off < length; off += 4) {
            int n = Math.min(4, length - off);
            long word = 0;
            for (int i = 0; i < n; i++) word |= ((long)bytes[off + i] & 0xffL) << (8 * i);
            StringBuilder b = new StringBuilder();
            for (int i = 0; i < n; i++) {
                if (i > 0) b.append(' ');
                b.append(String.format("%02X", bytes[off + i] & 0xff));
            }
            StringBuilder ascii = new StringBuilder();
            for (int i = 0; i < n; i++) {
                int v = bytes[off + i] & 0xff;
                ascii.append(v >= 32 && v <= 126 ? (char)v : '.');
            }
            line("word address=" + hex(rawAddress + off)
                + " bytes=[" + b + "] little_endian=" + hex(word)
                + " ascii=[" + ascii + "]");
        }
        ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(address);
        int count = 0;
        while (refs.hasNext()) {
            Reference ref = refs.next();
            line("xref_from=" + ref.getFromAddress()
                + " type=" + ref.getReferenceType()
                + " operand=" + ref.getOperandIndex());
            count++;
            if (count >= 200) {
                line("xref_output_cap=200");
                break;
            }
        }
        line("exact_xrefs_to_range_start_emitted=" + count);
        line("=== DATA_RANGE_END ===");
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2) throw new IllegalArgumentException("Args: output-path address:length [more ranges]");
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out = writer;
            line("analysis=read-only static executable data-slot dump");
            line("program=" + currentProgram.getName());
            line("program_language=" + currentProgram.getLanguageID());
            line("gameplay_or_emulator_executed=no");
            line("gameplay_input_sent=no");
            line("savestate_restored=no");
            line("private_binary_uploaded_as_artifact=no");
            for (int i = 1; i < args.length; i++) {
                monitor.checkCancelled();
                dump(args[i]);
            }
            out.flush();
            if (out.checkError()) throw new IllegalStateException("Failed writing static memory table report.");
        }
    }
}
