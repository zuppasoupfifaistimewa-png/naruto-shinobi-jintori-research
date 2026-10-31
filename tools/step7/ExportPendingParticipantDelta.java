// ExportPendingParticipantDelta.java
// Locate direct decoded accesses to candidate participant-relative offsets +0x2EE and +0xB44,
// and direct code references to candidate pending-fee/aggregate globals.
// These offsets are searched independently; neither is assigned gameplay semantics.
// Static-only report; imported Entry 1 base is a candidate loader-buffer mapping.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.regex.Pattern;

public class ExportPendingParticipantDelta extends GhidraScript {
    private PrintWriter out;
    private static final long BASE = 0x800AD450L;
    private static final Pattern DISP = Pattern.compile("(?i)(?:0x)?([0-9a-f]+)\\s*\\(");
    private static final int[] CANDIDATE_OFFSETS = {0x2EE, 0xB44};
    private static final long[] GLOBALS = {
        0x8013EBB0L, // candidate pending fee value
        0x8013EAC8L, // board record count
        0x8013EA84L, // board record array base
        0x8013EA74L, // participant object/base pointer slot
        0x8013EA88L  // selected participant
    };

    private void line(String s) { out.println(s); }
    private String hex(long value) { return String.format("0x%08X", value & 0xffffffffL); }

    private String bytes(Instruction ins) {
        try {
            byte[] b = new byte[ins.getLength()];
            currentProgram.getMemory().getBytes(ins.getAddress(), b);
            StringBuilder s = new StringBuilder();
            for (byte v : b) {
                if (s.length() > 0) s.append(' ');
                s.append(String.format("%02X", v & 0xff));
            }
            return s.toString();
        } catch (Exception e) { return "UNAVAILABLE"; }
    }

    private void dumpWindow(Instruction center, int before, int after) {
        if (center == null) return;
        Instruction first = center;
        for (int i=0; i<before && first.getPrevious()!=null; i++) first=first.getPrevious();
        Instruction last = center;
        for (int i=0; i<after && last.getNext()!=null; i++) last=last.getNext();
        for (Instruction ins=first; ins!=null; ins=ins.getNext()) {
            line("  " + ins.getAddress() + " bytes=[" + bytes(ins) + "] " + ins.toString());
            if (ins.getAddress().equals(last.getAddress())) break;
        }
    }

    private void scanDirectDisplacement(int wantedOffset) throws Exception {
        String tag = String.format("%03X", wantedOffset);
        line("");
        line("=== DIRECT_DISPLACEMENT_" + tag + "_BEGIN ===");
        InstructionIterator iter=currentProgram.getListing().getInstructions(true);
        int total=0, loads=0, stores=0, other=0;
        while(iter.hasNext()) {
            monitor.checkCancelled();
            Instruction ins=iter.next();
            java.util.regex.Matcher match=DISP.matcher(ins.toString());
            boolean found=false;
            while(match.find()) {
                try {
                    if(Integer.parseInt(match.group(1),16)==wantedOffset) { found=true; break; }
                } catch(NumberFormatException ignored) { }
            }
            if(!found) continue;
            total++;
            String mnemonic=ins.getMnemonicString().toLowerCase();
            boolean store=mnemonic.startsWith("s");
            boolean load=mnemonic.startsWith("l");
            if(store) stores++; else if(load) loads++; else other++;
            Function f=currentProgram.getFunctionManager().getFunctionContaining(ins.getAddress());
            line("");
            line("=== DIRECT_OFFSET_ACCESS offset="+hex(wantedOffset)+" address="+ins.getAddress()+" ===");
            line("access_kind="+(store?"STORE":(load?"LOAD":"OTHER")));
            line("instruction_bytes=["+bytes(ins)+"] "+ins.toString());
            line("function_entry="+(f==null?"NONE":f.getEntryPoint()));
            line("function_name="+(f==null?"NONE":f.getName()));
            dumpWindow(ins,7,9);
        }
        line("");
        line("offset="+hex(wantedOffset));
        line("direct_offset_total="+total);
        line("direct_offset_load_candidates="+loads);
        line("direct_offset_store_candidates="+stores);
        line("direct_offset_other_candidates="+other);
        line("limitation=decoded textual base+displacement matches only; computed pointers, aliases, indirect references and runtime access not proven");
        line("=== DIRECT_DISPLACEMENT_" + tag + "_END ===");
    }

    private void dumpStaticBytes(long address, int count) {
        line("");
        line("=== STATIC_BYTE_EXCERPT_BEGIN address="+hex(address)+" length="+count+" ===");
        try {
            byte[] data=new byte[count];
            currentProgram.getMemory().getBytes(toAddr(address),data);
            for(int i=0;i<data.length;i+=16) {
                StringBuilder row=new StringBuilder();
                int stop=Math.min(i+16,data.length);
                for(int j=i;j<stop;j++) {
                    if(row.length()>0) row.append(' ');
                    row.append(String.format("%02X",data[j]&0xff));
                }
                line("address="+hex(address+i)+" bytes=["+row+"]");
            }
        } catch(Exception e) {
            line("read_status=UNAVAILABLE reason="+e.getClass().getSimpleName());
        }
        line("=== STATIC_BYTE_EXCERPT_END ===");
    }

    private void scanGlobalReferences(long raw) throws Exception {
        Address target=toAddr(raw);
        line("");
        line("=== GLOBAL_XREF_BEGIN target="+hex(raw)+" ===");
        try {
            byte[] b=new byte[4];
            currentProgram.getMemory().getBytes(target,b);
            long value=((long)b[0]&0xffL)|(((long)b[1]&0xffL)<<8)
                |(((long)b[2]&0xffL)<<16)|(((long)b[3]&0xffL)<<24);
            line("loaded_image_bytes="+String.format("%02X %02X %02X %02X",b[0]&0xff,b[1]&0xff,b[2]&0xff,b[3]&0xff));
            line("loaded_image_word="+hex(value));
            line("loaded_image_value_is_not_runtime_state=yes");
        } catch(Exception e) {
            line("loaded_image_value=UNAVAILABLE reason="+e.getClass().getSimpleName());
        }
        ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(target);
        int count=0;
        while(refs.hasNext()) {
            Reference ref=refs.next();
            Instruction ins=currentProgram.getListing().getInstructionAt(ref.getFromAddress());
            Function f=currentProgram.getFunctionManager().getFunctionContaining(ref.getFromAddress());
            line("xref_from="+ref.getFromAddress()+" type="+ref.getReferenceType()
                +" caller="+(f==null?"NONE":f.getEntryPoint())
                +" instruction="+(ins==null?"NONE":ins.toString()));
            if(ins!=null) dumpWindow(ins,4,4);
            count++;
            if(count>=160) { line("xref_output_cap=160"); break; }
        }
        line("xref_count_emitted="+count);
        line("=== GLOBAL_XREF_END ===");
    }

    @Override
    protected void run() throws Exception {
        String[] args=getScriptArgs();
        if(args.length<1) throw new IllegalArgumentException("Args: output-path");
        try(PrintWriter writer=new PrintWriter(new BufferedWriter(
            new OutputStreamWriter(new FileOutputStream(args[0]),StandardCharsets.UTF_8)))) {
            out=writer;
            line("analysis=Entry 1 pending participant delta and toll-global provenance scan");
            line("resource=DATA.BIN directory index 1; offset=0x10BB000; bytes=596412");
            line("hypothetical_import_base="+hex(BASE));
            line("base_status=STATIC_CANDIDATE_FROM_LOADER_GLOBAL; runtime memory not captured");
            line("candidate_offsets=participant-relative +0x2EE and +0xB44; direct-offset scan only, no semantic assignment");
            line("game_or_emulator_executed=no");
            line("gameplay_input_sent=no");
            line("savestate_restored=no");
            line("private_binary_uploaded_as_artifact=no");
            for(int offset:CANDIDATE_OFFSETS) scanDirectDisplacement(offset);
            dumpStaticBytes(0x800AD5F4L,32);
            for(long global:GLOBALS) scanGlobalReferences(global);
            out.flush();
            if(out.checkError()) throw new IllegalStateException("Failed writing pending participant delta trace.");
        }
    }
}
