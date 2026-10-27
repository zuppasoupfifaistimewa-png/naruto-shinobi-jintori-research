// ExportFunctionIndex.java
// Text-only export: function address, name, namespace, byte count, thunk and source.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;

public class ExportFunctionIndex extends GhidraScript {
    private String clean(String value) {
        if (value == null) return "";
        return value.replace("\\", "\\\\").replace("\t", "\\t")
                    .replace("\r", "\\r").replace("\n", "\\n");
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 1 || args[0].trim().isEmpty()) {
            throw new IllegalArgumentException("Provide output TSV path as script argument 1.");
        }

        int count = 0;
        try (PrintWriter out = new PrintWriter(new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(args[0]), StandardCharsets.UTF_8)))) {
            out.println("entry_address\tname\tnamespace\tbody_bytes\tis_thunk\tsource_type");
            FunctionIterator functions = currentProgram.getFunctionManager().getFunctions(true);
            while (functions.hasNext()) {
                Function function = functions.next();
                String address = String.format("0x%08X", function.getEntryPoint().getOffset());
                String namespace = function.getParentNamespace() == null
                    ? "" : function.getParentNamespace().getName(true);
                long bodyBytes = function.getBody().getNumAddresses();
                out.print(address);
                out.print("\t"); out.print(clean(function.getName()));
                out.print("\t"); out.print(clean(namespace));
                out.print("\t"); out.print(bodyBytes);
                out.print("\t"); out.print(function.isThunk());
                out.print("\t"); out.println(function.getSource().name());
                count++;
            }
            out.flush();
            if (out.checkError()) {
                throw new IllegalStateException("Could not write TSV function index.");
            }
        }

        println("Exported " + count + " function rows to " + args[0]);
        if (count == 0) {
            throw new IllegalStateException("Ghidra reported zero functions; refusing to mark export successful.");
        }
    }
}
