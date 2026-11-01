// Static manager-field writer and caller provenance audit for SLPS-03553.
// Ghidra-only static analysis. Text/TSV output; no runtime or emulator interaction.
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.pcode.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.mem.MemoryBlock;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class ExportManagerEconomyWriters extends GhidraScript {
    private static final long MANAGER_SLOT = 0x8013A554L;
    private static final long[] TARGETS = {0xB2AL, 0xB30L, 0xB38L};
    private static final long[] FUNCTIONS = {0x80109994L, 0x801048F0L, 0x80109974L, 0x80109984L, 0x80012A8CL};
    private PrintWriter out;
    private String module = "UNSPECIFIED";
    private int confirmedStores = 0, unresolvedStores = 0, refCount = 0, pointerWords = 0, jalrCount = 0;

    private static final class Sym {
        Long constant;
        Long managerOffset;
        String expr;
        Sym(Long c, Long m, String e) { constant=c; managerOffset=m; expr=e; }
        static Sym c(long v) { return new Sym(v,null,fmt(v)); }
        static Sym m(long v) { return new Sym(null,v,"MANAGER"+(v==0?"":signed(v))); }
        static Sym u(String s) { return new Sym(null,null,s); }
    }
    private static String fmt(long v) {
        return v < 0 ? "-0x"+Long.toHexString(-v) : "0x"+Long.toHexString(v);
    }
    private static String signed(long v) { return v < 0 ? "-0x"+Long.toHexString(-v) : "+0x"+Long.toHexString(v); }
    private static boolean targetOffset(long x) { for(long t:TARGETS) if(x==t) return true; return false; }
    private static long signedConstant(Varnode v) {
        long x=v.getOffset();
        int bits=v.getSize()*8;
        if(bits>0 && bits<64 && ((x >>> (bits-1))&1L)!=0) x -= (1L<<bits);
        return x;
    }
    private String addrExpr(Address a) { return a==null ? "TIDAK_TAHU" : "0x"+Long.toHexString(a.getOffset()); }

    private Sym eval(Varnode v, Set<String> seen, int depth) {
        if(v==null) return Sym.u("NULL");
        if(depth>64) return Sym.u("DEPTH_LIMIT("+v+")");
        // Ghidra's RAM-address varnodes are not always reported as constants.
        if(v.isAddress()) {
            long address=v.getAddress().getOffset();
            return Sym.c(address);
        }
        if(v.isConstant()) return Sym.c(signedConstant(v));
        // Each child evaluation gets a sibling-safe copy of this path set.
        seen=new HashSet<String>(seen);
        String key=v.toString()+"@"+(v.getDef()==null?"INPUT":v.getDef().getSeqnum().toString());
        if(!seen.add(key)) return Sym.u("CYCLE("+v+")");
        PcodeOp op=v.getDef();
        if(op==null) return Sym.u("INPUT("+v+")");
        int code=op.getOpcode();
        try {
            if(code==PcodeOp.LOAD && op.getNumInputs()>=2) {
                Sym a=eval(op.getInput(1),seen,depth+1);
                if(a.constant!=null && (a.constant.longValue()&0xffffffffL)==MANAGER_SLOT) return Sym.m(0);
                if(a.managerOffset!=null) return Sym.u("LOAD(MANAGER"+signed(a.managerOffset)+")");
                if(a.constant!=null) {
                    long value=readWord(a.constant.longValue());
                    if(value!=Long.MIN_VALUE) return Sym.c(value);
                }
                return Sym.u("LOAD("+a.expr+")");
            }
            if(code==PcodeOp.COPY || code==PcodeOp.CAST || code==PcodeOp.INT_ZEXT ||
               code==PcodeOp.INT_SEXT || code==PcodeOp.SUBPIECE) {
                return eval(op.getInput(0),seen,depth+1);
            }
            if(code==PcodeOp.MULTIEQUAL && op.getNumInputs()>0) {
                Sym first=eval(op.getInput(0),seen,depth+1);
                for(int i=1;i<op.getNumInputs();i++) {
                    Sym next=eval(op.getInput(i),seen,depth+1);
                    boolean same=(first.constant!=null && next.constant!=null && first.constant.equals(next.constant)) ||
                                 (first.managerOffset!=null && next.managerOffset!=null && first.managerOffset.equals(next.managerOffset)) ||
                                 (first.constant==null && next.constant==null && first.managerOffset==null && next.managerOffset==null && first.expr.equals(next.expr));
                    if(!same) return Sym.u("PHI("+first.expr+" | "+next.expr+")");
                }
                return first;
            }
            if(code==PcodeOp.PTRADD && op.getNumInputs()>=2) {
                Sym a=eval(op.getInput(0),seen,depth+1), b=eval(op.getInput(1),seen,depth+1);
                long scale=1;
                if(op.getNumInputs()>2) {
                    Sym z=eval(op.getInput(2),seen,depth+1);
                    if(z.constant!=null) scale=z.constant;
                }
                if(a.managerOffset!=null && b.constant!=null) return Sym.m(a.managerOffset+b.constant*scale);
                if(a.constant!=null && (a.constant.longValue()&0xffffffffL)==MANAGER_SLOT && b.constant!=null) return Sym.m(b.constant*scale);
                if(b.constant!=null && (b.constant.longValue()&0xffffffffL)==MANAGER_SLOT && a.constant!=null) return Sym.m(a.constant*scale);
                if(a.constant!=null && b.constant!=null) return Sym.c(a.constant+b.constant*scale);
                return Sym.u("PTRADD("+a.expr+","+b.expr+",scale="+scale+")");
            }
            if(code==PcodeOp.PTRSUB && op.getNumInputs()>=2) {
                Sym a=eval(op.getInput(0),seen,depth+1), b=eval(op.getInput(1),seen,depth+1);
                if(a.managerOffset!=null && b.constant!=null) return Sym.m(a.managerOffset-b.constant);
                if(a.constant!=null && b.constant!=null) return Sym.c(a.constant-b.constant);
                return Sym.u("PTRSUB("+a.expr+","+b.expr+")");
            }
            if(code==PcodeOp.INT_ADD) {
                Sym a=eval(op.getInput(0),seen,depth+1), b=eval(op.getInput(1),seen,depth+1);
                if(a.managerOffset!=null && b.constant!=null) return Sym.m(a.managerOffset+b.constant);
                if(b.managerOffset!=null && a.constant!=null) return Sym.m(b.managerOffset+a.constant);
                if(a.constant!=null && (a.constant.longValue()&0xffffffffL)==MANAGER_SLOT && b.constant!=null) return Sym.m(b.constant);
                if(b.constant!=null && (b.constant.longValue()&0xffffffffL)==MANAGER_SLOT && a.constant!=null) return Sym.m(a.constant);
                if(a.constant!=null && b.constant!=null) return Sym.c(a.constant+b.constant);
                return Sym.u("("+a.expr+" + "+b.expr+")");
            }
            if(code==PcodeOp.INT_SUB) {
                Sym a=eval(op.getInput(0),seen,depth+1), b=eval(op.getInput(1),seen,depth+1);
                if(a.managerOffset!=null && b.constant!=null) return Sym.m(a.managerOffset-b.constant);
                if(a.constant!=null && b.constant!=null) return Sym.c(a.constant-b.constant);
                return Sym.u("("+a.expr+" - "+b.expr+")");
            }
            if(code==PcodeOp.INT_MULT || code==PcodeOp.INT_DIV || code==PcodeOp.INT_SDIV ||
               code==PcodeOp.INT_AND || code==PcodeOp.INT_OR || code==PcodeOp.INT_XOR ||
               code==PcodeOp.INT_LEFT || code==PcodeOp.INT_RIGHT || code==PcodeOp.INT_SRIGHT) {
                Sym a=eval(op.getInput(0),seen,depth+1), b=eval(op.getInput(1),seen,depth+1);
                return Sym.u("("+a.expr+" OP"+code+" "+b.expr+")");
            }
            if(code==PcodeOp.INT_2COMP || code==PcodeOp.INT_NEGATE) {
                Sym a=eval(op.getInput(0),seen,depth+1);
                return a.constant!=null ? Sym.c(-a.constant) : Sym.u("OP"+code+"("+a.expr+")");
            }
            if(code==PcodeOp.CALL || code==PcodeOp.CALLIND) {
                Sym t=op.getNumInputs()>0 ? eval(op.getInput(0),seen,depth+1) : Sym.u("TARGET?");
                StringBuilder b=new StringBuilder("CALL_RET(").append(t.expr);
                for(int i=1;i<op.getNumInputs() && i<=4;i++) b.append(",").append(eval(op.getInput(i),seen,depth+1).expr);
                return Sym.u(b.append(")").toString());
            }
            if(code==PcodeOp.INDIRECT && op.getNumInputs()>0) return eval(op.getInput(0),seen,depth+1);
            return Sym.u("P"+code+"("+op.toString()+")");
        } catch(Exception e) {
            return Sym.u("EVAL_ERROR("+v+")");
        }
    }
    private Sym eval(Varnode v) { return eval(v,new HashSet<String>(),0); }
    private long readWord(long a) {
        try {
            byte[] b=new byte[4]; currentProgram.getMemory().getBytes(toAddr(a),b);
            return ((long)b[0]&255L)|(((long)b[1]&255L)<<8)|(((long)b[2]&255L)<<16)|(((long)b[3]&255L)<<24);
        } catch(Exception e) { return Long.MIN_VALUE; }
    }
    private String bytes(Address a, int max) {
        try {
            byte[] b=new byte[max]; int n=currentProgram.getMemory().getBytes(a,b);
            StringBuilder s=new StringBuilder();
            for(int i=0;i<n;i++){if(i>0)s.append(' ');s.append(String.format("%02X",b[i]&255));}
            return s.toString();
        } catch(Exception e) { return "UNAVAILABLE"; }
    }
    private String before(Instruction center, Function owner, int count) {
        List<Instruction> a=new ArrayList<Instruction>();
        Instruction p=center;
        for(int i=0;i<count;i++) {
            p=p.getPrevious();
            if(p==null || (owner!=null && !owner.getBody().contains(p.getAddress()))) break;
            a.add(p);
        }
        Collections.reverse(a);
        StringBuilder s=new StringBuilder();
        for(Instruction i:a) {
            if(s.length()>0)s.append(" || ");
            s.append(addrExpr(i.getAddress())).append(" ").append(i.toString());
        }
        if(a.size()!=count) s.insert(0,"PRECOUNT="+a.size()+"; ");
        return s.toString();
    }
    private String functionEntry(Function f) { return f==null?"NONE":addrExpr(f.getEntryPoint()); }
    private String functionName(Function f) { return f==null?"NONE":f.getName(); }
    private void row(String... fields) {
        for(int i=0;i<fields.length;i++){if(i>0)out.print('\t');out.print(clean(fields[i]));}
        out.println();
    }
    private String clean(String s) { return s==null?"":s.replace('\t',' ').replace('\n',' ').replace('\r',' '); }
    private boolean candidate(Function f) {
        InstructionIterator it=currentProgram.getListing().getInstructions(f.getBody(),true);
        while(it.hasNext()) {
            String s=it.next().toString().toLowerCase();
            if(s.contains("-0x5aac") || s.contains("0xb2a(") || s.contains("0xb30(") || s.contains("0xb38(")) return true;
        }
        return false;
    }
    private boolean storeOp(PcodeOp op) { return op.getOpcode()==PcodeOp.STORE && op.getNumInputs()>=3; }
    private String targetName(long off) { return off==0xB2A?"MANAGER+0xB2A":off==0xB30?"MANAGER+0xB30":off==0xB38?"MANAGER+0xB38":"OTHER"; }
    private boolean hasDelaySlot(String m) {
        String x=m==null?"":m.toLowerCase();
        return x.equals("j")||x.equals("jal")||x.equals("jr")||x.equals("jalr")||
            x.equals("beq")||x.equals("bne")||x.equals("blez")||x.equals("bgtz")||
            x.equals("bltz")||x.equals("bgez")||x.equals("bc1t")||x.equals("bc1f");
    }
    private boolean isStoreMnemonic(String m) {
        String x=m==null?"":m.toLowerCase();
        return x.startsWith("sw")||x.startsWith("sb")||x.startsWith("sh")||
            x.equals("sc")||x.equals("sdc1")||x.equals("sdc2")||x.equals("s.d");
    }
    private Address actualStoreAddress(Address pcodePc) {
        Instruction at=currentProgram.getListing().getInstructionAt(pcodePc);
        if(at!=null && hasDelaySlot(at.getMnemonicString())) {
            Address delayAddress=pcodePc.add(at.getLength());
            Instruction delay=currentProgram.getListing().getInstructionAt(delayAddress);
            if(delay!=null && isStoreMnemonic(delay.getMnemonicString())) return delay.getAddress();
            // Ghidra may attach the delay-slot STORE p-code to the control-transfer PC
            // without creating a separate listing instruction. Decode its raw word.
            try {
                byte[] raw=new byte[4]; currentProgram.getMemory().getBytes(delayAddress,raw);
                long word=((long)raw[0]&255L)|(((long)raw[1]&255L)<<8)|(((long)raw[2]&255L)<<16)|(((long)raw[3]&255L)<<24);
                int opcode=(int)((word>>>26)&0x3f), imm=(short)(word&0xffff);
                if((opcode==0x28||opcode==0x29||opcode==0x2a||opcode==0x2b||opcode==0x2c||opcode==0x2d) &&
                   (imm==0xB2A||imm==0xB30||imm==0xB38)) return delayAddress;
            } catch(Exception ignored) {}
        }
        return pcodePc;
    }
    private String regName(int n) {
        String[] r={"zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"};
        return n>=0&&n<r.length?r[n]:"r"+n;
    }
    private String instructionTextAtStore(Address pc, Instruction ins) {
        if(ins!=null) return ins.toString();
        try {
            byte[] raw=new byte[4]; currentProgram.getMemory().getBytes(pc,raw);
            long w=((long)raw[0]&255L)|(((long)raw[1]&255L)<<8)|(((long)raw[2]&255L)<<16)|(((long)raw[3]&255L)<<24);
            int op=(int)((w>>>26)&0x3f), rs=(int)((w>>>21)&31), rt=(int)((w>>>16)&31), imm=(short)(w&0xffff);
            String m=op==0x28?"sb":op==0x29?"sh":op==0x2b?"sw":op==0x2a?"swl":op==0x2c?"swr":op==0x2d?"sdl":"store";
            return m+" "+regName(rt)+","+fmt(imm)+"("+regName(rs)+") [delay-slot raw decode]";
        } catch(Exception e) { return "INSTRUCTION_NOT_DECODED"; }
    }
    private String preStoreWindow(Address pcodePc, Address storePc, Function owner, Instruction storeIns) {
        if(!storePc.equals(pcodePc)) {
            Instruction branch=currentProgram.getListing().getInstructionAt(pcodePc);
            if(branch!=null) {
                String prev=before(branch,owner,11);
                return (prev.length()==0?"":prev+" || ")+addrExpr(branch.getAddress())+" "+branch.toString();
            }
        }
        return storeIns==null?"":before(storeIns,owner,12);
    }
    private boolean instructionHasTargetOffset(Instruction ins) {
        if(ins==null) return false;
        String s=ins.toString().toLowerCase();
        return s.contains("0xb2a(")||s.contains("0xb30(")||s.contains("0xb38(");
    }
    private void scanWriters() throws Exception {
        DecompInterface d=new DecompInterface();
        d.toggleCCode(false); d.toggleSyntaxTree(true);
        if(!d.openProgram(currentProgram)) throw new IllegalStateException("Decompiler could not open program");
        FunctionIterator fs=currentProgram.getFunctionManager().getFunctions(true);
        int scanned=0, decompileFailures=0;
        while(fs.hasNext()) {
            monitor.checkCancelled();
            Function f=fs.next();
            if(!candidate(f)) continue;
            DecompileResults r=d.decompileFunction(f,30,monitor);
            if(r==null || !r.decompileCompleted() || r.getHighFunction()==null) {
                decompileFailures++;
                row("DECOMPILE_UNAVAILABLE",module,functionEntry(f),functionName(f),"TIDAK_TAHU","",r==null?"NULL":r.getErrorMessage());
                continue;
            }
            scanned++;
            Iterator<PcodeOpAST> ops=r.getHighFunction().getPcodeOps();
            while(ops.hasNext()) {
                PcodeOpAST op=ops.next();
                if(!storeOp(op)) continue;
                Address pcodePc=op.getSeqnum().getTarget();
                Address pc=actualStoreAddress(pcodePc);
                Instruction ins=currentProgram.getListing().getInstructionAt(pc);
                Sym target=eval(op.getInput(1));
                String source=eval(op.getInput(2)).expr;
                int width=op.getInput(2).getSize();
                if(target.managerOffset!=null && targetOffset(target.managerOffset)) {
                    long off=target.managerOffset;
                    row("WRITER_CONFIRMED",module,addrExpr(pc),functionEntry(f),functionName(f),targetName(off),
                        String.valueOf(width),source,instructionTextAtStore(pc,ins),
                        preStoreWindow(pcodePc,pc,f,ins),bytes(pc,64),
                        "Pcode STORE target resolves through LOAD at global manager slot 0x8013A554; static");
                    confirmedStores++;
                } else if(instructionHasTargetOffset(ins)) {
                    row("WRITER_CANDIDATE_UNRESOLVED",module,addrExpr(pc),functionEntry(f),functionName(f),
                        target.expr,String.valueOf(width),source,instructionTextAtStore(pc,ins),preStoreWindow(pcodePc,pc,f,ins),bytes(pc,64),
                        "store has target displacement but manager base alias is not proven by this function-local def-use");
                    unresolvedStores++;
                }
            }
        }
        d.dispose();
        row("WRITER_SCAN_TOTAL",module,"","","","confirmed="+confirmedStores,"unresolved="+unresolvedStores,
            "candidate_functions_decompiled="+scanned,"decompile_failures="+decompileFailures,
            "manager_slot=0x8013A554 runtime_observation=0x801CEF08","","");
    }
    private void callerRefs(long target) throws Exception {
        Address a=toAddr(target);
        ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(a);
        DecompInterface decomp=new DecompInterface();
        decomp.toggleCCode(false); decomp.toggleSyntaxTree(true);
        decomp.openProgram(currentProgram);
        while(refs.hasNext()) {
            Reference ref=refs.next();
            Address from=ref.getFromAddress();
            Function caller=currentProgram.getFunctionManager().getFunctionContaining(from);
            Instruction ins=currentProgram.getListing().getInstructionAt(from);
            Instruction delay=ins==null?null:currentProgram.getListing().getInstructionAt(from.add(ins.getLength()));
            row("CALLER_REFERENCE",module,addrExpr(a),addrExpr(from),functionEntry(caller),functionName(caller),
                ref.getReferenceType().toString(),ref.getSource().toString(),
                ins==null?"DATA_OR_UNDECODED":ins.toString(),
                (ins==null?"":before(ins,caller,12))+" || DELAY_SLOT="+(delay==null?"NONE":addrExpr(delay.getAddress())+" "+delay.toString()),
                bytes(from,16),"ReferenceManager xref; call/data type retained");
            if(caller!=null && ins!=null && (ref.getReferenceType().isCall() || hasDelaySlot(ins.getMnemonicString()))) {
                DecompileResults dr=decomp.decompileFunction(caller,30,monitor);
                if(dr!=null && dr.decompileCompleted() && dr.getHighFunction()!=null) {
                    Iterator<PcodeOpAST> callOps=dr.getHighFunction().getPcodeOps();
                    while(callOps.hasNext()) {
                        PcodeOpAST call=callOps.next();
                        if(call.getOpcode()!=PcodeOp.CALL || call.getNumInputs()<2) continue;
                        Sym callee=eval(call.getInput(0));
                        if(callee.constant==null || (callee.constant.longValue()&0xffffffffL)!=target) continue;
                        String arg0=eval(call.getInput(1)).expr;
                        row("CALL_ARGUMENT_PROVENANCE",module,addrExpr(a),addrExpr(call.getSeqnum().getTarget()),
                            functionEntry(caller),functionName(caller),"a0_argument","Pcode CALL input[1]",
                            arg0,"",bytes(call.getSeqnum().getTarget(),64),
                            "static decompiler def-use for first ABI argument; PHI/CALL_RET/INPUT indicate source not fully resolved");
                    }
                }
            }
            refCount++;
        }
        decomp.dispose();
        for(MemoryBlock b:currentProgram.getMemory().getBlocks()) {
            if(!b.isInitialized()) continue;
            long start=b.getStart().getOffset(), end=start+b.getSize(), p=start;
            for(;p+4<=end;p++) {
                long word=readWord(p);
                if((word&0xffffffffL)==target) {
                    row("FUNCTION_POINTER_WORD",module,addrExpr(a),addrExpr(toAddr(p)),b.getName(),
                        "value="+addrExpr(toAddr(word)),bytes(toAddr(p),4),
                        "4-byte target pointer found at any byte alignment; table/caller semantics still need xref/control-flow confirmation");
                    pointerWords++;
                }
            }
        }
    }
    private void exportEconomyGlobalSource() throws Exception {
        long target=0x80070C88L;
        Address a=toAddr(target);
        MemoryBlock block=currentProgram.getMemory().getBlock(a);
        String blockName=block==null?"UNMAPPED":block.getName();
        String value="NO_INITIALIZED_BYTES";
        String raw="";
        if(block!=null && block.isInitialized() && block.contains(a)) {
            raw=bytes(a,4);
            long word=readWord(target);
            if(word!=Long.MIN_VALUE) value=fmt(word);
        }
        row("ECONOMY_GLOBAL_META",module,addrExpr(a),"","","_DAT_80070C88",
            blockName,value,raw,"","","FUN_80012A8C statically reads this global; numerical value only if loaded/initialized bytes exist");
        int refsFound=0;
        ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(a);
        while(refs.hasNext()) {
            Reference ref=refs.next();
            Address from=ref.getFromAddress();
            Function owner=currentProgram.getFunctionManager().getFunctionContaining(from);
            Instruction ins=currentProgram.getListing().getInstructionAt(from);
            row("ECONOMY_GLOBAL_XREF",module,addrExpr(a),addrExpr(from),functionEntry(owner),functionName(owner),
                ref.getReferenceType().toString(),ref.getSource().toString(),
                ins==null?"DATA_OR_UNDECODED":ins.toString(),
                ins==null?"":before(ins,owner,12),bytes(from,16),
                "ReferenceManager xref; store/load semantics require opcode inspection");
            refsFound++;
        }
        InstructionIterator it=currentProgram.getListing().getInstructions(true);
        while(it.hasNext()) {
            Instruction ins=it.next();
            String text=ins.toString().toLowerCase();
            // 0x80070C88 may be referenced through LUI 0x8007 + displacement 0xC88,
            // or an equivalent signed displacement based on another register.
            if(text.contains("0xc88(") || text.contains("-0x3978(")) {
                Function owner=currentProgram.getFunctionManager().getFunctionContaining(ins.getAddress());
                row("ECONOMY_GLOBAL_DISPLACEMENT_CANDIDATE",module,addrExpr(a),addrExpr(ins.getAddress()),
                    functionEntry(owner),functionName(owner),ins.getMnemonicString(),ins.toString(),
                    "effective address requires preceding base-register provenance",
                    owner==null?"":before(ins,owner,12),bytes(ins.getAddress(),16),
                    "static instruction contains displacement candidate for global +0x80070C88; validate its base register");
            }
        }
        row("ECONOMY_GLOBAL_XREF_TOTAL",module,addrExpr(a),"","","",
            "reference_manager_refs="+refsFound,"memory_block="+blockName,"value="+value,
            "unaligned_function_pointer_words_total="+pointerWords,"","","no runtime");
    }
    private void dumpFunction(long target) throws Exception {
        Address targetAddress=toAddr(target);
        Function f=currentProgram.getFunctionManager().getFunctionAt(targetAddress);
        if(f==null) {
            // Entry 1 may reference a main-EXE routine that Ghidra did not discover
            // from its own entry point. Force static disassembly/function creation.
            try {
                if(currentProgram.getListing().getInstructionAt(targetAddress)==null) disassemble(targetAddress);
                f=currentProgram.getFunctionManager().getFunctionAt(targetAddress);
                if(f==null && currentProgram.getMemory().contains(targetAddress)) f=createFunction(targetAddress,null);
            } catch(Exception e) {
                row("FUNCTION_FORCE_CREATE_ERROR",module,addrExpr(targetAddress),"","","ERROR",e.toString(),"","","","","static");
            }
        }
        if(f==null) {
            row("FUNCTION_BODY_UNAVAILABLE",module,addrExpr(targetAddress),"","","NO_FUNCTION","","","","","","no function created after static disassembly attempt");
            return;
        }
        DecompInterface d=new DecompInterface();
        d.toggleCCode(true); d.toggleSyntaxTree(true); d.openProgram(currentProgram);
        DecompileResults r=d.decompileFunction(f,60,monitor);
        String c=(r!=null&&r.decompileCompleted()&&r.getDecompiledFunction()!=null)
            ? r.getDecompiledFunction().getC() : "DECOMPILE_UNAVAILABLE";
        row("FUNCTION_DECOMPILE",module,addrExpr(f.getEntryPoint()),"",functionEntry(f),functionName(f),
            "C_BODY","static decompiler",c,"","","no runtime");
        InstructionIterator it=currentProgram.getListing().getInstructions(f.getBody(),true);
        while(it.hasNext()) {
            Instruction ins=it.next();
            row("FUNCTION_INSTRUCTION",module,addrExpr(f.getEntryPoint()),addrExpr(ins.getAddress()),
                functionEntry(f),functionName(f),ins.getMnemonicString(),ins.toString(),
                "", "",bytes(ins.getAddress(),4),"static disassembly for provenance context");
        }
        d.dispose();
    }
    private void countJalr() throws Exception {
        InstructionIterator it=currentProgram.getListing().getInstructions(true);
        while(it.hasNext()) {
            Instruction ins=it.next();
            if("jalr".equalsIgnoreCase(ins.getMnemonicString())) {
                jalrCount++;
                Function owner=currentProgram.getFunctionManager().getFunctionContaining(ins.getAddress());
                row("INDIRECT_CALL_SITE",module,"TARGET_UNRESOLVED",addrExpr(ins.getAddress()),
                    functionEntry(owner),functionName(owner),"JALR","",""+ins.toString(),"",
                    bytes(ins.getAddress(),16),"dynamic register target not statically tied to either requested entry");
            }
        }
    }
    @Override protected void run() throws Exception {
        String[] args=getScriptArgs();
        if(args.length>0) module=args[0];
        String path=args.length>1?args[1]:null;
        if(path==null) throw new IllegalArgumentException("Args: module output.tsv");
        try(PrintWriter w=new PrintWriter(new BufferedWriter(new OutputStreamWriter(new FileOutputStream(path),StandardCharsets.UTF_8)))) {
            out=w;
            row("record_type","module","target_or_function","pc_or_ref","function_entry_or_block","function_name_or_detail",
                "field_or_ref_type","width_or_ref_source","value_expression_or_instruction","pre_store_12_instructions","bytes_excerpt_hex_max64","notes");
            row("META",module,"manager_slot=0x8013A554","runtime_observation=0x801CEF08",
                "target_fields=0xB2A;0xB30;0xB38","program="+currentProgram.getName(),
                "STATIC_ONLY","NO_EMULATOR","game_or_emulator_executed=no","","",
                "all functions with manager-slot displacement or direct target-field displacement are candidate-scanned");
            scanWriters();
            for(long t:FUNCTIONS) callerRefs(t);
            if(module.equals("MAIN_EXE")) {
                exportEconomyGlobalSource();
                dumpFunction(0x80012A8CL);
            }
            if(module.equals("ENTRY1")) dumpFunction(0x800EDD68L);
            countJalr();
            row("INDIRECT_CALL_LIMIT",module,"FUN_80109994;FUN_801048F0;FUN_80109974;FUN_80109984","","","",
                "jalr_count="+jalrCount,"pointer_words="+pointerWords,"reference_manager_refs="+refCount,
                "unresolved dynamic CALLIND sites may remain; no runtime caller inference","","");
            out.flush();
            if(out.checkError()) throw new IllegalStateException("Output write failure");
        }
    }
}