import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;

public class ExportDN1WriterWindows extends GhidraScript {
    private static final Set<String> LOADER_COPY = new HashSet<>(Arrays.asList(
        "800F7CE8","800F7CFC","800F7D0C","800F7D20","800F7D30",
        "800F7D44","800F7D54","800F7D68","800F7D78","800F7D8C"));
    private static final Pattern STORE = Pattern.compile(
        "^(sb|sh|sw|sd|swc[0-9]+|sdc[0-9]+)\\s+([^,]+),.*\\(([^)]+)\\)$",
        Pattern.CASE_INSENSITIVE);

    private String clean(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\").replace("\t", " ").replace("\r", " ").replace("\n", " ");
    }
    private String hexBytes(Instruction ins) throws Exception {
        byte[] raw = new byte[ins.getLength()];
        currentProgram.getMemory().getBytes(ins.getAddress(), raw);
        StringBuilder b = new StringBuilder();
        for (byte v : raw) {
            if (b.length() > 0) b.append(' ');
            b.append(String.format("%02X", v & 0xff));
        }
        return b.toString();
    }
    private String[] storeOperands(Instruction ins) {
        if (ins == null) return new String[] {"", ""};
        Matcher m = STORE.matcher(ins.toString().trim());
        if (!m.matches()) return new String[] {"", ""};
        return new String[] {m.group(3).trim(), m.group(2).trim()};
    }
    private String mnemonic(Instruction ins) {
        return ins == null ? "" : ins.getMnemonicString().toLowerCase(Locale.ROOT);
    }
    private String defCandidate(Instruction center, String reg) {
        if (center == null || reg == null || reg.isEmpty() || reg.equals("zero")) return "";
        Instruction p = center.getPrevious();
        for (int n=0; n<12 && p!=null; n++, p=p.getPrevious()) {
            String asm=p.toString().trim();
            String[] split=asm.split("\\s+",2);
            if (split.length<2) continue;
            String m=split[0].toLowerCase(Locale.ROOT);
            String dst=split[1].split(",",2)[0].trim();
            if (dst.equals(reg)) return p.getAddress()+" "+asm;
        }
        return "";
    }
    private String valueOrigin(String reg, String def) {
        if ("zero".equals(reg)) return "KONSTANTA_NOL";
        if (def == null || def.isEmpty()) return "TIDAK_TAHU — tidak ada definisi register di 12 instruksi sebelumnya";
        String asm=def.substring(def.indexOf(' ')+1).trim();
        String m=asm.split("\\s+",2)[0].toLowerCase(Locale.ROOT);
        if (m.startsWith("lbu") || m.startsWith("lb") || m.startsWith("lhu") ||
            m.startsWith("lh") || m.startsWith("lw") || m.startsWith("lwc") || m.startsWith("lwc1"))
            return "LOAD_MEMORI_LOKAL — sumber alamat belum ditelusuri";
        if (m.equals("li") || m.equals("lui") || m.equals("addi") || m.equals("addiu") ||
            m.equals("ori") || m.equals("xori") || m.equals("andi") || m.equals("addu") ||
            m.equals("add") || m.equals("subu") || m.equals("sub") || m.equals("sll") ||
            m.equals("srl") || m.equals("sra") || m.equals("mult") || m.equals("multu") ||
            m.equals("div") || m.equals("divu"))
            return "DEF_LOKAL_ARITMETIK_ATAU_IMMEDIATE — belum dibuktikan sebagai formula level";
        if (m.equals("move") || m.equals("or")) return "SALIN_REG_LOKAL — sumber register belum ditelusuri";
        return "DEF_LOKAL_LAIN — rantai def-use belum ditutup";
    }
    private String dumpWindow(Instruction center, List<Instruction> previous) throws Exception {
        StringBuilder b=new StringBuilder();
        for (Instruction i: previous) {
            if (b.length()>0) b.append(" || ");
            b.append(i.getAddress()).append(" bytes=[").append(hexBytes(i)).append("] ").append(i);
        }
        if (center!=null) {
            if (b.length()>0) b.append(" || ");
            b.append(center.getAddress()).append(" bytes=[").append(hexBytes(center)).append("] ").append(center);
        }
        return b.toString();
    }
    private String excerpt(List<Instruction> previous, Instruction center) throws Exception {
        StringBuilder b=new StringBuilder();
        int used=0;
        List<Instruction> all=new ArrayList<>(previous);
        if (center!=null) all.add(center);
        for (Instruction i: all) {
            byte[] raw=new byte[i.getLength()];
            currentProgram.getMemory().getBytes(i.getAddress(),raw);
            for (byte v:raw) {
                if (used>=64) return b.toString().trim();
                if (used>0) b.append(' ');
                b.append(String.format("%02X",v&0xff));
                used++;
            }
        }
        return b.toString();
    }
    @Override
    protected void run() throws Exception {
        String[] args=getScriptArgs();
        if (args.length<2) throw new IllegalArgumentException("Args: output-tsv input-census-tsv");
        Path output=Paths.get(args[0]);
        List<String> input=Files.readAllLines(Paths.get(args[1]),StandardCharsets.UTF_8);
        Path parent=output.getParent();
        if (parent!=null) Files.createDirectories(parent);
        int header=-1;
        for (int i=0;i<input.size();i++) if (input.get(i).startsWith("field_offset\\tpc\\t")) { header=i; break; }
        if (header<0) throw new IllegalArgumentException("DM1 census header not found");
        StringBuilder out=new StringBuilder();
        out.append("field_offset\\tpc\\tfunction_entry\\tfunction_name\\tinstruction\\tinstruction_bytes\\tbase_register\\tvalue_register\\tprevious_instruction_count\\tprevious_12_plus_store\\tvalue_origin\\tnearest_value_def_candidate\\tnearest_base_def_candidate\\tlabel\\talias_status\\tcontext_status\\traw_excerpt_hex_max64\\treason\\n");
        int target=0, decoded=0, stores=0, loader=0, notDecoded=0, notStore=0;
        for (int i=header+1;i<input.size();i++) {
            monitor.checkCancelled();
            String[] c=input.get(i).split("\\t",-1);
            if (c.length<14) continue;
            String ctx=c[13], oldLabel=c[11], alias=c[12];
            boolean wanted=ctx.equals("NO_STORE_IN_REVIEWED_EXPORT") ||
                (oldLabel.equals("LAIN") && alias.equals("BASE_ALIAS_UNPROVEN") && !ctx.equals("NO_STORE_IN_REVIEWED_EXPORT"));
            if (!wanted) continue;
            target++;
            String field=c[0], pc=c[1], oldEntry=c[2], oldName=c[3];
            Address a;
            try { a=toAddr(Long.decode(pc)); }
            catch (Exception e) { a=null; }
            Instruction center=(a==null)?null:currentProgram.getListing().getInstructionAt(a);
            Function f=(a==null)?null:currentProgram.getFunctionManager().getFunctionContaining(a);
            String fEntry=f==null?oldEntry:f.getEntryPoint().toString();
            String fName=f==null?oldName:f.getName();
            List<Instruction> previous=new ArrayList<>();
            if (center!=null) {
                decoded++;
                Instruction first=center;
                for (int n=0;n<12 && first.getPrevious()!=null;n++) first=first.getPrevious();
                for (Instruction p=first;p!=null;p=p.getNext()) {
                    if (p.getAddress().equals(center.getAddress())) break;
                    previous.add(p);
                }
            } else {
                notDecoded++;
            }
            String inst=center==null?"TIDAK_TERSEDIA":center.toString();
            String instBytes=center==null?"TIDAK_TERSEDIA":hexBytes(center);
            String[] operands=storeOperands(center);
            boolean isStore=operands[0].length()>0;
            if (isStore) stores++; else if(center!=null) notStore++;
            String base=isStore?operands[0]:"TIDAK_TAHU";
            String value=isStore?operands[1]:"TIDAK_TAHU";
            String vdef=isStore?defCandidate(center,value):"";
            String bdef=isStore?defCandidate(center,base):"";
            String label="LAIN";
            String upper=pc.replace("0X","").replace("0x","").toUpperCase(Locale.ROOT);
            if (LOADER_COPY.contains(upper)) { label="LOADER_COPY"; loader++; }
            String origin=isStore?valueOrigin(value,vdef):(center==null?"TIDAK_TAHU — alamat tidak ter-decode pada listing":"TIDAK_TAHU — PC kandidat bukan instruksi store");
            String reason;
            String status;
            if (center==null) { status="PC_NOT_DECODED"; reason="TIDAK TAHU — listing Ghidra tidak memiliki instruksi tepat pada PC"; }
            else if (!isStore) { status="PC_NOT_STORE"; reason="PC census tidak decode menjadi sb/sh/sw/sd; belum membuktikan store field"; }
            else { status="STORE_DECODED_DEF_USE_OPEN"; reason="store ter-decode; nilai hanya memiliki nearest-def lokal, base belum dibuktikan EA84 + index*0x124"; }
            String window=dumpWindow(center,previous);
            String raw=excerpt(previous,center);
            out.append(clean(field)).append('\\t').append(clean(pc)).append('\\t')
               .append(clean(fEntry)).append('\\t').append(clean(fName)).append('\\t')
               .append(clean(inst)).append('\\t').append(clean(instBytes)).append('\\t')
               .append(clean(base)).append('\\t').append(clean(value)).append('\\t')
               .append(previous.size()).append('\\t').append(clean(window)).append('\\t')
               .append(clean(origin)).append('\\t').append(clean(vdef)).append('\\t')
               .append(clean(bdef)).append('\\t').append(label).append('\\t')
               .append("BASE_ALIAS_UNPROVEN").append('\\t').append(status).append('\\t')
               .append(clean(raw)).append('\\t').append(clean(reason)).append('\\n');
        }
        Files.write(output,out.toString().getBytes(StandardCharsets.UTF_8));
        println("DN1_TARGET_ROWS="+target);
        println("DN1_DECODED_PC="+decoded);
        println("DN1_STORE_DECODED="+stores);
        println("DN1_PC_NOT_STORE="+notStore);
        println("DN1_PC_NOT_DECODED="+notDecoded);
        println("DN1_LOADER_COPY_MATCHES="+loader);
        println("DN1_COMPUTED_CONFIRMED=0 (bounded nearest-def is not proof)");
        println("DN1_OUTPUT="+output);
    }
}
