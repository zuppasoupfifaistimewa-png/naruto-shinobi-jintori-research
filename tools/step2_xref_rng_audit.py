#!/usr/bin/env python3
"""Read-only A2/A4 audit for SLPS-03553. No emulator or save-state access."""
from __future__ import annotations
import argparse, csv, hashlib, json, re, struct
from collections import Counter, defaultdict
from pathlib import Path

EXE_BASE = 0x80010000
EXE_HEADER = 0x800
EXE_TEXT_SIZE = 0x5D800
ENTRY0_OFFSET, ENTRY0_SIZE, ENTRY0_BASE = 0x5F800, 110536, 0x800AD000
ENTRY1_OFFSET, ENTRY1_SIZE, ENTRY1_BASE = 0x10BB000, 596412, 0x800AD450
OLD_GHIDRA_BASE = 0x800D0000
TARGET = 0x8013A554
LOW = 0xA554
RNG = 0x80035D78
LOADS = {0x20:"lb",0x21:"lh",0x22:"lwl",0x23:"lw",0x24:"lbu",0x25:"lhu",0x26:"lwr",0x27:"lwu",0x30:"ll"}
STORES = {0x28:"sb",0x29:"sh",0x2A:"swl",0x2B:"sw",0x2E:"swr",0x38:"sc"}
SPECIAL_VALID = {0,2,3,4,6,7,8,9,12,13,16,17,18,19,24,25,26,27,32,33,34,35,36,37,38,39,42,43}
PRIMARY_VALID = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,32,33,34,35,36,37,38,40,41,42,43,46,48,49,50,51,56,57,58,59}
REGS=("zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra")
KNOWN_EXE_CALLERS = {0x80015B14:0x80015ADC, 0x80015BF0:0x80015B7C, 0x8001A460:0x8001A328, 0x80020C24:0x80020BF4}

def u32(buf, off): return struct.unpack_from("<I", buf, off)[0]
def sha(buf): return hashlib.sha256(buf).hexdigest()
def s16(x): return x - 0x10000 if x & 0x8000 else x
def fields(w): return ((w>>26)&63,(w>>21)&31,(w>>16)&31,(w>>11)&31,(w>>6)&31,w&63,w&0xffff)
def words(buf): return [u32(buf, i) for i in range(0, len(buf)-3, 4)]
def jal_target(w): return (0x80000000 | ((w & 0x03ffffff) << 2)) if ((w >> 26) & 63) == 3 else None
def is_prologue(w): return (w & 0xffff0000) == 0x27bd0000 and s16(w & 0xffff) < 0
def is_jr_ra(w): return w == 0x03e00008
def op_name(w):
    op,rs,rt,rd,sh,fn,imm=fields(w)
    if op == 0:
        return {0:"sll",2:"srl",3:"sra",4:"sllv",6:"srlv",7:"srav",8:"jr",9:"jalr",
                12:"syscall",13:"break",16:"mfhi",17:"mthi",18:"mflo",19:"mtlo",
                24:"mult",25:"multu",26:"div",27:"divu",32:"add",33:"addu",34:"sub",
                35:"subu",36:"and",37:"or",38:"xor",39:"nor",42:"slt",43:"sltu"}.get(fn,"special")
    return {1:"regimm",2:"j",3:"jal",4:"beq",5:"bne",6:"blez",7:"bgtz",
            8:"addi",9:"addiu",10:"slti",11:"sltiu",12:"andi",13:"ori",14:"xori",
            15:"lui",16:"cop0",17:"cop1",18:"cop2",19:"cop3",
            32:"lb",33:"lh",34:"lwl",35:"lw",36:"lbu",37:"lhu",38:"lwr",
            40:"sb",41:"sh",42:"swl",43:"sw",46:"swr",48:"ll",49:"lwc1",
            50:"lwc2",51:"lwc3",56:"sc",57:"swc1",58:"swc2",59:"swc3"}.get(op,f"op{op:02x}")
def valid_mips(w):
    op,rs,rt,rd,sh,fn,imm=fields(w)
    if op == 0: return fn in SPECIAL_VALID
    if op in PRIMARY_VALID: return True
    return False
def dest_reg(w):
    op,rs,rt,rd,sh,fn,imm=fields(w)
    if op == 0:
        if fn in (8,12,13,24,25,26,27): return None
        if fn in (16,18): return rd
        if fn == 9: return rd if rd else 31
        return rd if rd else None
    if op in (2,4,5,6,7,28,29,30,31,40,41,42,43,46,56,57,58,59) or op in (16,17,18,19): return None
    if op == 3: return 31
    if op in LOADS or op in (1,8,9,10,11,12,13,14,15,17,18,19,48,49,50,51): return rt
    return None
def instruction_desc(w):
    op,rs,rt,rd,sh,fn,imm=fields(w); m=op_name(w)
    if op in LOADS or op in STORES: return f"{m} {REGS[rt]},{s16(imm):#x}({REGS[rs]})"
    if op in (8,9,10,11,12,13,14,15): return f"{m} {REGS[rt]},{REGS[rs]},{s16(imm):#x}"
    if op in (2,3): return f"{m} target=0x{(0x80000000|((w&0x03ffffff)<<2)):08X}"
    if op == 0: return f"{m} rs={REGS[rs]} rt={REGS[rt]} rd={REGS[rd]} sh={sh} fn=0x{fn:02X}"
    return f"{m} word=0x{w:08X}"
def write_csv(path, rows, fields_order=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    if fields_order is None: fields_order=list(rows[0].keys()) if rows else []
    with path.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=fields_order,extrasaction="ignore");wr.writeheader();wr.writerows(rows)
def read_csv(path):
    if not path or not Path(path).exists(): return []
    with Path(path).open(newline="",encoding="utf-8-sig") as f: return list(csv.DictReader(f))
def parse_old_xrefs(path):
    rows=[]
    patt=re.compile(r"^exact_xref from=([0-9a-fA-F]+) type=(\S+) source=(\S+) function=(\S+) instruction=(.*)$")
    for line in Path(path).read_text(encoding="utf-8",errors="replace").splitlines():
        m=patt.match(line)
        if not m: continue
        pc=int(m.group(1),16); off=pc-OLD_GHIDRA_BASE
        rows.append({"legacy_view_base":f"0x{OLD_GHIDRA_BASE:08X}","pc_old_view":f"0x{pc:08X}",
                     "entry1_file_offset":f"0x{off:06X}","type":m.group(2),"source":m.group(3),
                     "function":("0x"+m.group(4).upper()) if m.group(4)!="NONE" else "NONE",
                     "instruction":m.group(5),"evidence":"run 40611660635 artifact 12783307599 field-cfg-defuse.txt"})
    return rows

def lui_pair_for(ws, i, rs, max_back=32):
    """Find prior LUI rt==base-register, imm==0x8014 without intervening clobber."""
    low=max(0,i-max_back)
    crossed_control=False
    for j in range(i-1,low-1,-1):
        w=ws[j]; op,r_s,rt,rd,sh,fn,imm=fields(w)
        if op==0x0f and rt==rs:
            if imm==0x8014: return j,crossed_control
            return None,crossed_control
        if dest_reg(w)==rs: return None,crossed_control
        if op in (1,2,3,4,5,6,7) or (op==0 and fn in (8,9)): crossed_control=True
    return None,crossed_control

def scan_a2(data, file_label, base, source_offset=0):
    ws=words(data); rows=[]
    for i,w in enumerate(ws):
        op,rs,rt,rd,sh,fn,imm=fields(w)
        if s16(imm) != -0x5AAC: continue
        if op in LOADS: kind="READ"
        elif op in STORES: kind="WRITE"
        elif op==9: kind="ADDRESS"
        else: continue
        lui_i,crossed=lui_pair_for(ws,i,rs,32)
        # Also note whether exact legacy same-basic-block scanner already found it.
        rows.append({
          "file":file_label,"instruction_pc":f"0x{base+4*i:08X}",
          "file_offset":f"0x{source_offset+4*i:06X}","instruction_word":f"0x{w:08X}",
          "bytes_le":w.to_bytes(4,"little").hex(" ").upper(),"mnemonic":op_name(w),"kind":kind,
          "base_register":REGS[rs],"target_register":REGS[rt],
          "immediate_signed":s16(imm),
          "lui_pc":f"0x{base+4*lui_i:08X}" if lui_i is not None else "NOT_FOUND_WITHIN_32",
          "lui_file_offset":f"0x{source_offset+4*lui_i:06X}" if lui_i is not None else "",
          "distance_words":i-lui_i if lui_i is not None else "",
          "control_instruction_between_pair":str(crossed).lower() if lui_i is not None else "unknown",
          "effective_address_if_pair":f"0x{((0x80140000+s16(imm))&0xffffffff):08X}" if lui_i is not None else "UNRESOLVED",
          "confidence_note":"linear register provenance only; control-flow dominance/aliasing not proven"
        })
    return rows

def func_contains(pc, functions):
    for f in functions:
        try:
            if int(f.get("start_address","0"),16) <= pc <= int(f.get("end_address","0"),16):
                return f.get("function_name","UNKNOWN")
        except (ValueError,TypeError): pass
    return ""
def read_ghidra_functions(path):
    rows=read_csv(path)
    for r in rows:
        for key in ("start_address","end_address","entry1_file_offset","end_entry1_file_offset"):
            if r.get(key,"").startswith("0x"): r[key]=r[key].upper()
    return rows
def instr_at_entry(entry, off):
    if off < 0 or off+4 > len(entry) or off%4: return None
    w=u32(entry,off)
    return {"word":w,"bytes":entry[off:off+4].hex(" ").upper(),"mnemonic":op_name(w),"desc":instruction_desc(w),
            "valid":valid_mips(w),"op":(w>>26)&63,"imm":s16(w&0xffff)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--exe",required=True);ap.add_argument("--data",required=True);ap.add_argument("--out",required=True)
    ap.add_argument("--legacy-ghidra-text",required=True);ap.add_argument("--legacy-scan-csv",required=True)
    ap.add_argument("--new-ghidra-xrefs",required=True);ap.add_argument("--new-ghidra-functions",required=True)
    args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    exe=Path(args.exe).read_bytes(); dat=Path(args.data).read_bytes()
    if len(exe)!=385024 or exe[:8]!=b"PS-X EXE": raise SystemExit(f"EXE identity failure size={len(exe)}")
    if len(dat)!=66015232: raise SystemExit(f"DATA.BIN size failure {len(dat)}")
    if sha(exe)!="a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569": raise SystemExit("EXE SHA mismatch")
    if sha(dat)!="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822": raise SystemExit("DATA.BIN SHA mismatch")
    text=exe[EXE_HEADER:EXE_HEADER+EXE_TEXT_SIZE]
    entry0=dat[ENTRY0_OFFSET:ENTRY0_OFFSET+ENTRY0_SIZE]
    entry1=dat[ENTRY1_OFFSET:ENTRY1_OFFSET+ENTRY1_SIZE]
    if len(entry0)!=ENTRY0_SIZE or len(entry1)!=ENTRY1_SIZE: raise SystemExit("entry slice length mismatch")
    if sha(entry0)!="56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4": raise SystemExit("entry0 SHA mismatch")
    if sha(entry1)!="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a": raise SystemExit("entry1 SHA mismatch")

    # A2 expanded low-displacement scan: exe text, entry 0 and entry 1.
    all_scan=[]
    all_scan += scan_a2(text,"SLPS_035.53 text",EXE_BASE,EXE_HEADER)
    all_scan += scan_a2(entry0,"DATA.BIN entry 0",ENTRY0_BASE,ENTRY0_OFFSET)
    all_scan += scan_a2(entry1,"DATA.BIN entry 1",ENTRY1_BASE,ENTRY1_OFFSET)
    write_csv(out/"a2_expanded_xref_candidates.csv",all_scan)
    summary=[]
    for file_label in ("SLPS_035.53 text","DATA.BIN entry 0","DATA.BIN entry 1"):
        for kind in ("READ","WRITE","ADDRESS"):
            rr=[r for r in all_scan if r["file"]==file_label and r["kind"]==kind]
            summary.append({"file":file_label,"kind":kind,"low_immediate_sites":len(rr),
                            "lui_8014_pair_within_32_no_clobber":sum(r["lui_pc"]!="NOT_FOUND_WITHIN_32" for r in rr),
                            "control_instruction_crossed_among_pairs":sum(r["control_instruction_between_pair"]=="true" for r in rr),
                            "unresolved_same_register_provenance":sum(r["lui_pc"]=="NOT_FOUND_WITHIN_32" for r in rr)})
    write_csv(out/"a2_expanded_xref_summary.csv",summary)

    # Legacy reference sets: preserve all historic locations and the prior strict scan list.
    old_xrefs=parse_old_xrefs(args.legacy_ghidra_text)
    write_csv(out/"a2_old_ghidra_xrefs_194.csv",old_xrefs)
    if len(old_xrefs)!=194: raise SystemExit(f"legacy XREF baseline expected 194, got {len(old_xrefs)}")
    oldscan=read_csv(args.legacy_scan_csv)
    scan_offsets={int(r["file_offset"],16) for r in oldscan if r.get("scenario","").startswith("base_0x800AD450")}
    xref_offsets={int(r["entry1_file_offset"],16) for r in old_xrefs if 0 <= int(r["entry1_file_offset"],16) < len(entry1)}
    if len(scan_offsets)!=137 or len(xref_offsets)!=194: raise SystemExit(f"legacy baseline counts mismatch scan={len(scan_offsets)} xrefs={len(xref_offsets)}")
    common=scan_offsets & xref_offsets
    scan_only=scan_offsets-xref_offsets
    ghidra_only=xref_offsets-scan_offsets
    if (len(common),len(scan_only),len(ghidra_only))!=(79,58,115):
        raise SystemExit(f"legacy set reconciliation unexpected common/scan-only/ghidra-only={(len(common),len(scan_only),len(ghidra_only))}")

    expanded_entry_offsets={int(r["file_offset"],16)-ENTRY1_OFFSET for r in all_scan
                            if r["file"]=="DATA.BIN entry 1" and r["lui_pc"]!="NOT_FOUND_WITHIN_32"}
    newxrefs=read_csv(args.new_ghidra_xrefs)
    new_xref_offsets=set()
    for r in newxrefs:
        raw=r.get("entry1_file_offset","")
        if raw.startswith("0x"):
            off=int(raw,16)
            if 0 <= off < len(entry1): new_xref_offsets.add(off)
    functions=read_ghidra_functions(args.new_ghidra_functions)

    # One and only one cause class for every legacy unmatched location.
    rec=[]
    def add_rec(side, off, oldrow, candrow, inst):
        pc_new=ENTRY1_BASE+off
        fn=func_contains(pc_new,functions)
        if side=="SCAN_ONLY":
            if off in new_xref_offsets:
                cause="OLD_GHIDRA_VIEW_MISSED_REFERENCE_NOW_PRESENT_AFTER_REBASE"
            elif fn:
                cause="RAW_PAIR_IN_REBASED_FUNCTION_GHIDRA_REFERENCE_MANAGER_DID_NOT_REPORT"
            else:
                cause="RAW_PAIR_NOT_INSIDE_REBASED_GHIDRA_FUNCTION"
        else:
            if off in expanded_entry_offsets:
                cause="EXTENDED_32_WORD_LUI_PROVENANCE_RECOVERS_LEGACY_GHIDRA_SITE"
            elif inst and inst["op"] in set(LOADS)|set(STORES) and inst["imm"]==-0x5AAC:
                cause="NO_UNCLOBBERED_SAME_REGISTER_LUI_8014_WITHIN_32_WORDS"
            else:
                cause="LEGACY_XREF_NOT_REPRODUCED_BY_REQUESTED_RAW_PATTERN"
        rec.append({
          "legacy_difference_side":side,"entry1_file_offset":f"0x{off:06X}",
          "pc_old_ghidra_view":f"0x{OLD_GHIDRA_BASE+off:08X}",
          "pc_rebased_view":f"0x{ENTRY1_BASE+off:08X}",
          "old_ghidra_type":oldrow.get("type","") if oldrow else "",
          "prior_scan_kind":candrow.get("kind","") if candrow else "",
          "prior_scan_word":candrow.get("instruction","") if candrow else "",
          "raw_word":f"0x{inst['word']:08X}" if inst else "UNAVAILABLE",
          "raw_bytes_le":inst["bytes"] if inst else "UNAVAILABLE",
          "raw_disassembly":inst["desc"] if inst else "UNAVAILABLE",
          "raw_instruction_validity":"VALID_MIPS_ENCODING" if inst and inst["valid"] else "NOT_CLASSIFIED_AS_VALID_MIPS",
          "rebased_ghidra_function":fn or "NONE",
          "rebased_ghidra_reference_present":str(off in new_xref_offsets).lower(),
          "cause_class":cause,
          "cause_claim_scope":"single evidence class assigned by stated decision rule; not a causal runtime claim"
        })
    oldscan_by_off={int(r["file_offset"],16):r for r in oldscan if r.get("scenario","").startswith("base_0x800AD450")}
    oldxref_by_off={int(r["entry1_file_offset"],16):r for r in old_xrefs}
    for off in sorted(scan_only): add_rec("SCAN_ONLY",off,oldxref_by_off.get(off),oldscan_by_off.get(off),instr_at_entry(entry1,off))
    for off in sorted(ghidra_only): add_rec("GHIDRA_ONLY",off,oldxref_by_off.get(off),oldscan_by_off.get(off),instr_at_entry(entry1,off))
    write_csv(out/"a2_legacy_xref_reconciliation.csv",rec)
    class_counts=Counter((r["legacy_difference_side"],r["cause_class"]) for r in rec)
    write_csv(out/"a2_reconciliation_class_summary.csv",[
      {"side":side,"cause_class":cause,"locations":n,"sample_rule":"audit all if <10; otherwise select 10 diverse offsets"}
      for (side,cause),n in sorted(class_counts.items())
    ])
    # At least ten examples per larger class; audit every location for smaller classes.
    samples=[]
    for (side,cause),n in sorted(class_counts.items()):
        pool=[r for r in rec if r["legacy_difference_side"]==side and r["cause_class"]==cause]
        chosen=pool[:min(10,n)]
        for r in chosen:
            samples.append({**r,"sample_verification":"raw entry1 bytes and instruction encoding independently recomputed from SHA-verified DATA.BIN slice"})
    write_csv(out/"a2_reconciliation_sample_audit.csv",samples)

    # Target slot file bytes at entry-1 offset 0x8D104 for the requested candidate base.
    target_off=TARGET-ENTRY1_BASE
    target_bytes=entry1[target_off:target_off+4]
    target_word=struct.unpack("<I",target_bytes)[0]
    write_csv(out/"a2_target_slot_static_value.csv",[{
      "target_virtual_address":f"0x{TARGET:08X}","entry1_candidate_base":f"0x{ENTRY1_BASE:08X}",
      "entry1_file_offset":f"0x{target_off:06X}","file_bytes_le":target_bytes.hex(" ").upper(),
      "file_u32_le":f"0x{target_word:08X}","file_u32_le_decimal":target_word,
      "ram_dump_sha256":"3ad7b85c857a868d91df4b3f1049c23889a0dc482ad7ee390ac8b6c05c3190f4",
      "ram_dump_value":"NOT AVAILABLE IN CURRENT WORKSPACE; not reconstructed from savestate",
      "static_meaning":"raw file word only; runtime pointer/value not inferred"
    }])
    old_ghidra_only_vs_expanded=len(new_xref_offsets-expanded_entry_offsets)
    base_old_supported=old_ghidra_only_vs_expanded < 58

    # A4 function candidates detected with A1's stack-prologue / after-jr+delay heuristic.
    ew=words(text); rw=words(entry1)
    starts={i for i,w in enumerate(rw) if is_prologue(w)}
    for i in range(2,len(rw)):
        if is_jr_ra(rw[i-2]): starts.add(i)
    starts_sorted=sorted(starts)
    def prior_start(i,max_bytes=0x100):
        for s in reversed(starts_sorted):
            if s>i: continue
            if (i-s)*4 > max_bytes: break
            return s
        return None
    def rng_usage(ws, i, base):
        masks=[]; divs=[]; remainder=[]; constants={}; consumers=[]
        stop=min(len(ws),i+34)
        for j in range(i+2,stop):  # JAL delay slot at i+1 executes before RNG returns
            w=ws[j];op,rs,rt,rd,sh,fn,imm=fields(w);pc=base+4*j
            if op==0x0c and rs==2:
                masks.append(f"ANDI {REGS[rt]},v0,0x{imm:04X}@0x{pc:08X}")
            if op==9 and rs==0: constants[rt]=s16(imm)
            elif op==13 and rs==0: constants[rt]=imm
            elif op==15: constants[rt]=(imm<<16)&0xffffffff
            elif dest_reg(w) is not None:
                dr=dest_reg(w)
                if dr in constants and not (op==0x0d and rs in constants): constants.pop(dr,None)
            if op==0 and fn in (0x1a,0x1b):
                divs.append(f"{op_name(w).upper()}@0x{pc:08X} dividend={REGS[rs]} divisor={REGS[rt]}"+
                            (f"(const={constants[rt]})" if rt in constants else "(value unresolved)"))
                remainder.append("DIV_MFHI_PATTERN_CANDIDATE")
            if op==0 and fn==0x10 and divs:
                remainder[-1]="DIV_MFHI_REMAINDER"
            if len(consumers)<4:
                if op in LOADS|STORES and (rs==2 or rt==2):
                    consumers.append(f"{pc:#010x}:{instruction_desc(w)}")
                elif op in (4,5,6,7) and rs==2:
                    consumers.append(f"{pc:#010x}:{instruction_desc(w)}")
                elif op==0 and rs==2:
                    consumers.append(f"{pc:#010x}:{instruction_desc(w)}")
        summary=[]
        summary.extend(masks)
        summary.extend(divs)
        if not summary: summary=["TIDAK ADA"]
        return "; ".join(summary), "; ".join(consumers) if consumers else "NO_CLEAR_DIRECT_USE_IN_32_WORD_WINDOW", bool(masks),bool(divs)
    new_functions=functions
    rng_rows=[]
    for i,w in enumerate(rw):
        if jal_target(w)!=RNG: continue
        pc=ENTRY1_BASE+i*4
        st=prior_start(i)
        pathvalid=bool(st is not None and all(valid_mips(x) for x in rw[st:i+1]))
        fn=func_contains(pc,new_functions)
        if pathvalid and fn:
            klass="VALID"
        elif not fn and st is None:
            klass="DATA"
        else:
            klass="TIDAK PASTI"
        maskmod,use,mhas,dhas=rng_usage(rw,i,ENTRY1_BASE)
        rng_rows.append({
          "call_pc":f"0x{pc:08X}","entry1_file_offset":f"0x{i*4:06X}",
          "call_word":f"0x{w:08X}","target":"0x80035D78","classification":klass,
          "a1_prior_function_start":f"0x{ENTRY1_BASE+st*4:08X}" if st is not None else "TIDAK TERBUKTI",
          "linear_path_all_known_mips":str(pathvalid).lower(),
          "ghidra_containing_function":fn or "NONE",
          "mask_modulus_evidence":maskmod if maskmod else "TIDAK ADA",
          "first_direct_uses":use,"pattern_group":"MASK_AND_DIV" if mhas and dhas else "MASK_ONLY" if mhas else "DIV_OR_REMAINDER" if dhas else "NO_DIRECT_MASK_MODULUS_32_WORDS",
          "semantic_function_label":"TIDAK TERBUKTI"
        })
    write_csv(out/"a4_entry1_rng_calls_classified.csv",rng_rows)
    if len(rng_rows)!=144:
        raise SystemExit(f"Expected 144 raw JAL RNG candidates in entry 1, got {len(rng_rows)}")
    groups=Counter((r["classification"],r["pattern_group"]) for r in rng_rows)
    write_csv(out/"a4_entry1_rng_groups.csv",[{"classification":k[0],"pattern_group":k[1],"calls":v,
              "interpretation":"instruction-pattern grouping only; no gameplay feature name assigned"} for k,v in sorted(groups.items())])

    # Four EXE calls: fixed confirmed function starts, same result-use scan window.
    exrows=[]
    for i,w in enumerate(ew):
        if jal_target(w)!=RNG: continue
        pc=EXE_BASE+4*i
        st=KNOWN_EXE_CALLERS.get(pc)
        maskmod,use,mhas,dhas=rng_usage(ew,i,EXE_BASE)
        exrows.append({
          "call_pc":f"0x{pc:08X}","call_word":f"0x{w:08X}","target":"0x80035D78",
          "confirmed_function_start":f"0x{st:08X}" if st else "TIDAK TERBUKTI",
          "mask_modulus_evidence":maskmod if maskmod else "TIDAK ADA",
          "first_direct_uses":use,
          "pattern_group":"MASK_AND_DIV" if mhas and dhas else "MASK_ONLY" if mhas else "DIV_OR_REMAINDER" if dhas else "NO_DIRECT_MASK_MODULUS_32_WORDS",
          "semantic_function_label":"TIDAK TERBUKTI"
        })
    write_csv(out/"a4_exe_rng_calls_refined.csv",exrows)
    if len(exrows)!=4: raise SystemExit(f"Expected 4 main EXE direct RNG calls, got {len(exrows)}")

    log=[
      "READ-ONLY STATIC AUDIT: no emulator launched; no input injected; no savestate parsed/restored; no RAM dump reconstructed.",
      f"EXE_BYTES={len(exe)} EXE_SHA256={sha(exe)}",
      f"DATA_BIN_BYTES={len(dat)} DATA_BIN_SHA256={sha(dat)}",
      f"ENTRY0_BYTES={len(entry0)} ENTRY0_SHA256={sha(entry0)} ENTRY0_BASE_HYPOTHESIS=0x{ENTRY0_BASE:08X}",
      f"ENTRY1_BYTES={len(entry1)} ENTRY1_SHA256={sha(entry1)} ENTRY1_BASE_CANDIDATE=0x{ENTRY1_BASE:08X}",
      f"A2_EXPANDED_CANDIDATES={len(all_scan)}",
      "A2_EXPANDED_SUMMARY="+json.dumps(summary,sort_keys=True),
      f"A2_LEGACY_XREF_COUNTS old_Ghidra={len(old_xrefs)} old_scan={len(scan_offsets)} common={len(common)} scan_only={len(scan_only)} Ghidra_only={len(ghidra_only)}",
      "A2_RECON_CLASS_COUNTS="+json.dumps([{"side":k[0],"class":k[1],"count":v} for k,v in sorted(class_counts.items())],sort_keys=True),
      f"A2_NEW_GHIDRA_REBASED_XREFS={len(new_xref_offsets)}",
      f"A2_NEW_GHIDRA_ONLY_VS_EXPANDED_SCAN={old_ghidra_only_vs_expanded} BASE_OLD_HYPOTHESIS_SUPPORTED_BY_THRESHOLD={str(base_old_supported).lower()} threshold=<58",
      f"A2_TARGET_FILE_ADDRESS=0x{TARGET:08X} entry1_offset=0x{target_off:06X} file_word=0x{target_word:08X}; RAM_DUMP_VALUE=NOT_AVAILABLE",
      f"A4_ENTRY1_RAW_JAL_COUNT={len(rng_rows)} A4_CLASS_COUNTS={json.dumps(dict(Counter(r['classification'] for r in rng_rows)),sort_keys=True)}",
      f"A4_EXE_RAW_JAL_COUNT={len(exrows)}",
      "CAVEATS: Ghidra XREFs are static-analysis references in a rebased binary view, not runtime observations; function classification uses A1-style prologue/return heuristic plus Ghidra function containment and linear MIPS word validity."
    ]
    (out/"step2-3-static-audit.log").write_text("\n".join(log)+"\n",encoding="utf-8")
    meta={"exe_sha256":sha(exe),"data_bin_sha256":sha(dat),"entry1_sha256":sha(entry1),
          "new_ghidra_xref_count":len(new_xref_offsets),"legacy_xref_count":len(old_xrefs),
          "legacy_scan_count":len(scan_offsets),"legacy_common":len(common),"legacy_scan_only":len(scan_only),
          "legacy_ghidra_only":len(ghidra_only),"expanded_scan_count":len(all_scan),
          "new_ghidra_only_vs_expanded_scan":old_ghidra_only_vs_expanded,
          "base_old_threshold_lt_58":base_old_supported,"entry1_rng_raw_jals":len(rng_rows),
          "entry1_rng_classes":dict(Counter(r["classification"] for r in rng_rows)),
          "exe_rng_raw_jals":len(exrows),"ram_dump_available":False}
    (out/"step2-3-static-audit.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print("\n".join(log))

if __name__=="__main__": main()
