#!/usr/bin/env python3
"""Read-only MIPS32 little-endian audit for slot 0x8013A554.
Input binaries are transient runner files only. Outputs are text/CSV only.
"""
from __future__ import annotations
import csv, hashlib, sys
from pathlib import Path
from collections import Counter

DATA_OFFSET = 0x10BB000
ENTRY_SIZE = 596412
ENTRY_SHA = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
ENTRY_BASE = 0x800AD450
SLOT = 0x8013A554
REGS = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
CALLER_SAVED = set(["at","v0","v1","a0","a1","a2","a3"] + [f"t{i}" for i in range(10)])
MASK = 0xFFFFFFFF

def s16(x): return x - 0x10000 if x & 0x8000 else x
def sx(v): return v & MASK

def decode(w):
    op=(w>>26)&0x3f; rs=(w>>21)&31; rt=(w>>16)&31; rd=(w>>11)&31; sh=(w>>6)&31; fn=w&63; imm=s16(w&0xffff)
    d={"word":w,"op":op,"rs":rs,"rt":rt,"rd":rd,"sh":sh,"fn":fn,"imm":imm,"writes":[],"control":False,"mnem":".word","args":f"0x{w:08X}","kind":"OTHER"}
    def reg(n): return REGS[n]
    if op==0:
        names={0:"sll",2:"srl",3:"sra",4:"sllv",6:"srlv",7:"srav",8:"jr",9:"jalr",12:"syscall",13:"break",16:"mfhi",17:"mthi",18:"mflo",19:"mtlo",24:"mult",25:"multu",26:"div",27:"divu",32:"add",33:"addu",34:"sub",35:"subu",36:"and",37:"or",38:"xor",39:"nor",42:"slt",43:"sltu"}
        d["mnem"]=names.get(fn,".word"); d["args"]=f"0x{w:08X}"
        if fn in (0,2,3): d["args"]=f"{reg(rd)}, {reg(rt)}, {sh}"; d["writes"]=[reg(rd)] if rd else []
        elif fn in (4,6,7): d["args"]=f"{reg(rd)}, {reg(rt)}, {reg(rs)}"; d["writes"]=[reg(rd)] if rd else []
        elif fn==8: d["args"]=reg(rs); d["control"]=True
        elif fn==9: d["args"]=f"{reg(rd)}, {reg(rs)}"; d["writes"]=[reg(rd)] if rd else []; d["control"]=True
        elif fn in (12,13): d["control"]=True
        elif fn in (16,18): d["args"]=reg(rd); d["writes"]=[reg(rd)] if rd else []
        elif fn in (17,19): d["args"]=reg(rs)
        elif fn in (24,25,26,27): d["args"]=f"{reg(rs)}, {reg(rt)}"
        elif fn in (32,33,34,35,36,37,38,39,42,43):
            d["args"]=f"{reg(rd)}, {reg(rs)}, {reg(rt)}"; d["writes"]=[reg(rd)] if rd else []
        d["kind"]="R"
    elif op in (2,3):
        d["mnem"]="j" if op==2 else "jal"; d["args"]=f"0x{(((w&0x03ffffff)<<2) | 0x80000000):08X}"; d["control"]=True
        if op==3: d["writes"]=["ra"]
        d["kind"]="J"
    elif op in (4,5,6,7,1):
        names={4:"beq",5:"bne",6:"blez",7:"bgtz",1:"regimm"}
        d["mnem"]=names[op]
        target = (ENTRY_BASE + 0) # formatter will calculate target based on PC if needed
        if op in (4,5): d["args"]=f"{reg(rs)}, {reg(rt)}, offset {imm:+d}"
        elif op in (6,7): d["args"]=f"{reg(rs)}, offset {imm:+d}"
        else: d["args"]=f"{reg(rs)}, rt={rt}, offset {imm:+d}"
        d["control"]=True; d["kind"]="BR"
    elif op in (8,9,10,11,12,13,14,15):
        names={8:"addi",9:"addiu",10:"slti",11:"sltiu",12:"andi",13:"ori",14:"xori",15:"lui"}
        d["mnem"]=names[op]
        d["args"]=f"{reg(rt)}, {reg(rs)}, {imm if op not in (12,13,14,15) else (w&0xffff if op!=15 else hex(w&0xffff))}"
        if op==15: d["args"]=f"{reg(rt)}, 0x{w&0xffff:04X}"
        d["writes"]=[reg(rt)] if rt else []; d["kind"]="I"
    elif op in (32,33,34,35,36,37,38,39,40,41,42,43,46,48,49,50,53,56,57,58,61):
        names={32:"lb",33:"lh",34:"lwl",35:"lw",36:"lbu",37:"lhu",38:"lwr",39:"lwu",40:"sb",41:"sh",42:"swl",43:"sw",46:"swr",48:"ll",49:"lwc1",50:"lwc2",53:"ldc1",56:"sc",57:"swc1",58:"swc2",61:"sdc1"}
        d["mnem"]=names.get(op,".word"); d["args"]=f"{reg(rt)}, {imm}({reg(rs)})"
        d["writes"]=[reg(rt)] if op in (32,33,34,35,36,37,38,39,48,49,50,53) and rt else []
        d["kind"]="LOAD" if op in (32,33,34,35,36,37,38,39,48,49,50,53) else "STORE"
    elif op==16:
        d["mnem"]="cop0"; d["args"]=f"0x{w&0x03ffffff:07X}"; d["kind"]="COP"
    return d

def disasm_line(pc, w, d):
    b=w.to_bytes(4,"little").hex(" ").upper()
    target=""
    if d["op"] in (4,5,6,7,1):
        target=f" ; branch=0x{(pc+4+(d['imm']<<2))&MASK:08X}"
    if d["op"] in (2,3):
        target=f" ; jump=0x{(((pc+4)&0xF0000000)|((w&0x03FFFFFF)<<2))&MASK:08X}"
    return f"0x{pc:08X}  {b:<11}  {d['mnem']:<8} {d['args']}{target}"

def entry_word(entry, pc):
    off=pc-ENTRY_BASE
    if off<0 or off+4>len(entry): return None
    return int.from_bytes(entry[off:off+4],"little")

def compute_reg(reg, before_pc, start, entry, depth=0, seen=None):
    """Conservative linear backward reaching-definition analysis; no emulator/runtime execution."""
    if reg=="zero": return {"value":0,"source_pc":"","source":"","status":"CONSTANT_ZERO","chain":"zero"}
    if depth>30: return {"value":None,"source_pc":"","source":"","status":"DEPTH_LIMIT","chain":"depth limit"}
    if seen is None: seen=set()
    key=(reg,before_pc)
    if key in seen: return {"value":None,"source_pc":"","source":"","status":"CYCLE","chain":"cycle"}
    seen=seen|{key}
    pc=before_pc-4
    while pc>=start:
        w=entry_word(entry,pc)
        if w is None: break
        d=decode(w)
        # A call destroys caller-saved values even though JAL only writes RA architecturally.
        if d["op"]==3 and reg in CALLER_SAVED:
            return {"value":None,"source_pc":f"0x{pc:08X}","source":disasm_line(pc,w,d),"status":"CALL_CLOBBER_OR_ENTRY_LIVE_IN","chain":f"{reg} crossed JAL at 0x{pc:08X}"}
        if reg not in d["writes"]:
            pc-=4
            continue
        source=disasm_line(pc,w,d)
        val=None; status="UNRESOLVED_DEFINITION"; chain=source
        op,rs,rt,rd,imm,fn=d["op"],d["rs"],d["rt"],d["rd"],d["imm"],d["fn"]
        if op==15 and REGS[rt]==reg:
            val=(w&0xffff)<<16; status="CONSTANT_LUI"; chain=f"{source} => 0x{val:08X}"
        elif op in (8,9,10,11,12,13,14) and REGS[rt]==reg:
            srcval=compute_reg(REGS[rs],pc,start,entry,depth+1,seen)["value"]
            if op in (8,9) and (srcval is not None or rs==0):
                val=sx((srcval or 0)+imm); status="CONSTANT_ADDI"
            elif op==13 and (srcval is not None or rs==0):
                val=sx((srcval or 0)|(w&0xffff)); status="CONSTANT_ORI"
            elif op==12 and (srcval is not None or rs==0):
                val=sx((srcval or 0)&(w&0xffff)); status="CONSTANT_ANDI"
            elif op==14 and (srcval is not None or rs==0):
                val=sx((srcval or 0)^(w&0xffff)); status="CONSTANT_XORI"
            elif op in (10,11) and srcval is not None:
                val=int(srcval < imm) if op==10 else int((srcval&MASK)<(imm&MASK)); status="CONSTANT_COMPARE"
            if val is not None: chain=f"{source} ; rs={REGS[rs]} value={('0x%08X'%srcval) if srcval is not None else '0'} => 0x{val:08X}"
        elif op==0 and fn in (0,2,3) and REGS[rd]==reg:
            srcval=compute_reg(REGS[rt],pc,start,entry,depth+1,seen)["value"]
            if srcval is not None:
                val=sx(srcval << d["sh"] if fn==0 else (srcval&MASK)>>d["sh"] if fn==2 else ((srcval if srcval<0x80000000 else srcval-0x100000000)>>d["sh"]))
                status="CONSTANT_SHIFT"; chain=f"{source} => 0x{val:08X}"
        elif op==0 and fn in (32,33,34,35,36,37,38,39,42,43) and REGS[rd]==reg:
            a=compute_reg(REGS[rs],pc,start,entry,depth+1,seen)["value"]; b=compute_reg(REGS[rt],pc,start,entry,depth+1,seen)["value"]
            if a is not None and b is not None:
                if fn in (32,33): val=sx(a+b)
                elif fn in (34,35): val=sx(a-b)
                elif fn==36: val=a&b
                elif fn==37: val=a|b
                elif fn==38: val=a^b
                elif fn==39: val=sx(~(a|b))
                elif fn==42: val=int((a if a<0x80000000 else a-0x100000000) < (b if b<0x80000000 else b-0x100000000))
                elif fn==43: val=int(a<b)
                status="CONSTANT_RTYPE"; chain=f"{source} ; rs=0x{a:08X} rt=0x{b:08X} => 0x{val:08X}"
            elif fn in (33,37) and rs==0 and b is not None:
                val=b; status="REGISTER_COPY"; chain=f"{source} => 0x{val:08X}"
            elif fn in (33,37) and rt==0 and a is not None:
                val=a; status="REGISTER_COPY"; chain=f"{source} => 0x{val:08X}"
        # Loads, stack restores, and computed values from unknown inputs are deliberately unresolved.
        return {"value":val,"source_pc":f"0x{pc:08X}","source":source,"status":status if val is not None else status,"chain":chain}
    return {"value":None,"source_pc":"","source":"","status":"FUNCTION_ENTRY_LIVE_IN_OR_NO_PRIOR_DEF","chain":f"no in-function definition of {reg} before 0x{before_pc:08X}"}

def main():
    if len(sys.argv)!=5:
        raise SystemExit("usage: audit_slot_provenance.py DATA.BIN candidates.csv functions.csv output_dir")
    data_path,cand_path,func_path,outdir=map(Path,sys.argv[1:])
    data=data_path.read_bytes()
    if len(data)!=66015232: raise SystemExit(f"DATA_BIN_SIZE_MISMATCH:{len(data)}")
    if hashlib.sha256(data).hexdigest()!="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822":
        raise SystemExit("DATA_BIN_SHA256_MISMATCH")
    if DATA_OFFSET+ENTRY_SIZE>len(data): raise SystemExit("ENTRY_RANGE_BAD")
    entry=data[DATA_OFFSET:DATA_OFFSET+ENTRY_SIZE]
    entry_sha=hashlib.sha256(entry).hexdigest()
    if entry_sha!=ENTRY_SHA: raise SystemExit(f"ENTRY_SHA256_MISMATCH:{entry_sha}")
    outdir.mkdir(parents=True,exist_ok=True)
    with cand_path.open(newline="",encoding="utf-8-sig") as f: candidates=list(csv.DictReader(f))
    unresolved=[r for r in candidates if r.get("effective_address_if_pair")=="UNRESOLVED"]
    if len(unresolved)!=32: raise SystemExit(f"EXPECTED_32_UNRESOLVED_CANDIDATES_GOT:{len(unresolved)}")
    with func_path.open(newline="",encoding="utf-8-sig") as f: funcs=list(csv.DictReader(f))
    func_ranges=[]
    for f in funcs:
        try: func_ranges.append((int(f["start_address"],16),int(f["end_address"],16),f["function_name"]))
        except (ValueError,KeyError): pass

    # Complete instruction disassembly for the two functions requested.
    dis_path=outdir/"v2_target_functions_full_disassembly.txt"
    selected=[]
    targets=[("FUN_80104690",0x80104690,0x8010478B),("FUN_8010478c",0x8010478C,0x801047CB)]
    with dis_path.open("w",encoding="utf-8") as f:
        f.write("Read-only disassembly of DATA.BIN entry 1; base 0x800AD450; no emulator.\n")
        f.write(f"DATA.BIN_SHA256=69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822\nENTRY1_SHA256={entry_sha}\n")
        f.write("Function bounds sourced from Ghidra export run 40789339014, commit 8b70e004f0df21bbb250a3c0b918a19e76ce0a21.\n\n")
        for name,start,end in targets:
            f.write(f"## {name} 0x{start:08X}..0x{end:08X} (inclusive)\n")
            refs=[]
            for c in candidates:
                try: pc=int(c["instruction_pc"],16)
                except: continue
                if start<=pc<=end and int(c.get("immediate_signed","0"))==-23212:
                    refs.append(c)
            for pc in range(start,end+1,4):
                w=entry_word(entry,pc)
                if w is None:
                    f.write(f"0x{pc:08X}  <OUTSIDE_ENTRY1>\n"); continue
                d=decode(w)
                marks=[c for c in refs if int(c["instruction_pc"],16)==pc]
                suffix=""
                if marks:
                    c=marks[0]
                    suffix=f"  ; SLOT_XREF_CANDIDATE kind={c['kind']} base={c['base_register']} target_reg={c['target_register']} static_effective={c['effective_address_if_pair']}"
                f.write(disasm_line(pc,w,d)+suffix+"\n")
            f.write("\n")

    # Resolve the address implied by each register+immediate from an in-function backward definition scan.
    reader_rows=[]
    with (outdir/"v3_32_reader_base_register_trace.csv").open("w",newline="",encoding="utf-8") as f:
        fields=["pc","entry1_relative_offset","function","instruction","base_register","immediate_signed","nearest_base_definition_pc","nearest_base_definition_instruction","base_value_if_constant","computed_effective_address","classification","trace_status","trace_chain","control_flow_caveat","source_run_id","source_commit"]
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader()
        for row in sorted(unresolved,key=lambda r:int(r["instruction_pc"],16)):
            pc=int(row["instruction_pc"],16); rel=pc-ENTRY_BASE; w=entry_word(entry,pc)
            if w is None: raise SystemExit(f"CANDIDATE_PC_OUTSIDE_ENTRY:{pc:#x}")
            d=decode(w)
            base=REGS[d["rs"]]; imm=s16(w&0xffff)
            owners=[(s,e,n) for s,e,n in func_ranges if s<=pc<=e]
            if len(owners)!=1:
                fn="FUNCTION_BOUNDARY_UNKNOWN"; result={"value":None,"source_pc":"","source":"","status":"NO_UNIQUE_CONTAINING_FUNCTION","chain":f"containing functions={len(owners)}"}; start=pc
            else:
                start,end,fn=owners[0]
                result=compute_reg(base,pc,start,entry)
            eff=sx(result["value"]+imm) if result["value"] is not None else None
            if eff is None: cls="UNRESOLVED"
            elif eff==SLOT: cls="RESOLVED_TO_0x8013A554"
            else: cls="RESOLVED_TO_OTHER_ADDRESS"
            # Mark conditional/control flow only as a caveat; this linear scan is not CFG dominance proof.
            source_pc=int(result["source_pc"],16) if result["source_pc"] else None
            controls=[]
            if source_pc is not None:
                for p in range(source_pc+4,pc,4):
                    ww=entry_word(entry,p)
                    if ww is not None and decode(ww)["control"]:
                        controls.append(f"0x{p:08X}")
            caveat=("control instruction(s) between reaching definition and use: "+",".join(controls)) if controls else "linear backward scan; full CFG dominance/alias analysis not performed"
            base_str=f"0x{result['value']:08X}" if result["value"] is not None else ""
            eff_str=f"0x{eff:08X}" if eff is not None else ""
            out={"pc":f"0x{pc:08X}","entry1_relative_offset":f"0x{rel:06X}","function":fn,"instruction":disasm_line(pc,w,d),"base_register":base,"immediate_signed":imm,"nearest_base_definition_pc":result["source_pc"],"nearest_base_definition_instruction":result["source"],"base_value_if_constant":base_str,"computed_effective_address":eff_str,"classification":cls,"trace_status":result["status"],"trace_chain":result["chain"],"control_flow_caveat":caveat,"source_run_id":"40789339014","source_commit":"8b70e004f0df21bbb250a3c0b918a19e76ce0a21"}
            writer.writerow(out); reader_rows.append(out)
    counts=Counter(r["classification"] for r in reader_rows)
    summary=outdir/"slot-provenance-summary.txt"
    summary.write_text("\n".join([
        "STATIC ONLY — no emulator, no gameplay input, no savestate restore",
        "DATA_BIN_SHA256=69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822",
        f"ENTRY1_SHA256={entry_sha}",
        "candidate_source=run 40789339014 artifact a2_expanded_xref_candidates.csv",
        "candidate_source_commit=https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/8b70e004f0df21bbb250a3c0b918a19e76ce0a21",
        f"v3_total={len(reader_rows)}",
        f"resolved_to_0x8013A554={counts['RESOLVED_TO_0x8013A554']}",
        f"resolved_to_other_address={counts['RESOLVED_TO_OTHER_ADDRESS']}",
        f"unresolved={counts['UNRESOLVED']}",
        "method=linear in-function backwards reaching-definition search, recursive constant propagation for LUI/ADDIU/ORI/ANDI/XORI/basic R-type; loads/stack restores/caller-saved registers across JAL are unresolved unless value follows from an explicit supported definition",
        "caveat=not a complete MIPS CFG/dataflow proof; every CSV row contains the local trace and any intervening control instructions",
    ])+"\n",encoding="utf-8")
    print(summary.read_text(encoding="utf-8"))
    print(f"V2_DISASSEMBLY_LINES={sum(1 for _ in dis_path.open(encoding='utf-8'))}")
    print(f"V3_ROWS={len(reader_rows)}")
if __name__=="__main__": main()
