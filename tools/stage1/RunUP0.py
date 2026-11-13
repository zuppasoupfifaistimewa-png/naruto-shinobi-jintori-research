#!/usr/bin/env python3
"""UP0: byte-verified reader, caller, writer and control-flow audit."""
from __future__ import annotations
import argparse
import csv
import hashlib
from pathlib import Path

EXE_SIZE = 385024
DATA_SIZE = 66015232
EXE_SHA = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
DATA_SHA = "69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
ENTRY1_SHA = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
EXE_PC, EXE_OFF = 0x80010000, 0x800
E1_PC, E1_OFF, E1_SIZE = 0x800AD450, 0x10BB000, 596412
RAM_POINTER = 0x8013EA84
STRIDE = 0x124
FORWARD_SITES = (0x800B7794, 0x800B77D4, 0x800B783C, 0x800B7884,
                 0x800B78D0, 0x800CE0F4, 0x800D0D70)
REGS = ("zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3",
        "t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7",
        "t8","t9","k0","k1","gp","sp","fp","ra")
MEM = {0x20:("lb",1,"R"),0x21:("lh",2,"R"),0x22:("lwl",4,"R"),
       0x23:("lw",4,"R"),0x24:("lbu",1,"R"),0x25:("lhu",2,"R"),
       0x26:("lwr",4,"R"),0x28:("sb",1,"W"),0x29:("sh",2,"W"),
       0x2A:("swl",4,"W"),0x2B:("sw",4,"W"),0x2E:("swr",4,"W")}
SPECIAL = {0:"sll",2:"srl",3:"sra",4:"sllv",6:"srlv",7:"srav",
           8:"jr",9:"jalr",12:"syscall",13:"break",16:"mfhi",
           17:"mthi",18:"mflo",19:"mtlo",24:"mult",25:"multu",
           26:"div",27:"divu",32:"add",33:"addu",34:"sub",
           35:"subu",36:"and",37:"or",38:"xor",39:"nor",
           42:"slt",43:"sltu"}
IMMEDIATE = {8:"addi",9:"addiu",10:"slti",11:"sltiu",
             12:"andi",13:"ori",14:"xori"}
BRANCH = {4:"beq",5:"bne",6:"blez",7:"bgtz"}
FWD = ["site_id","pc","region","file_offset","index","bytes_4B","instruction",
       "tracked_registers","classification","detail","target_pc"]
DEF = ["region","pc","file_offset","index","bytes_4B","instruction","base_register",
       "displacement","function_start","function_end","instructions_back",
       "status","basis_class","reason","def_chain"]
TRACE = ["site_pc","step","pc","file_offset","bytes_4B","instruction",
         "tainted_before","tainted_after","classification","detail","target_pc"]
BRANCHES = ["region","pc","file_offset","bytes_4B","instruction","target_pc","fallthrough_pc"]
VALIDATION = ["region","pc","file_offset","bytes_4B","instruction","redecoded_instruction",
              "word_hex","match","control_target"]
COUNTS = ["class","count"]

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def write_tsv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore",
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

def reg(n: int) -> str:
    return "$" + REGS[n]

def decode(raw: bytes, pc: int) -> dict:
    if len(raw) != 4:
        raise ValueError("MIPS_WORD_MUST_BE_4_BYTES")
    w = int.from_bytes(raw, "little")
    op, rs, rt = w >> 26, (w >> 21) & 31, (w >> 16) & 31
    rd, sh, fn = (w >> 11) & 31, (w >> 6) & 31, w & 63
    imm = w & 0xFFFF
    simm = imm if imm < 0x8000 else imm - 0x10000
    d = {"word":w,"op":op,"rs":rs,"rt":rt,"rd":rd,"sh":sh,"fn":fn,
         "imm":imm,"simm":simm,"mn":".word","text":f".word 0x{w:08X}",
         "reads":(),"writes":None,"mem":None,"control":False,"target":None}
    if op == 0:
        n = SPECIAL.get(fn)
        if n is None:
            return d
        d["mn"] = n
        if n in ("sll","srl","sra"):
            d.update(reads=(rt,),writes=rd,text=f"{n} {reg(rd)},{reg(rt)},{sh}")
        elif n in ("sllv","srlv","srav"):
            d.update(reads=(rt,rs),writes=rd,text=f"{n} {reg(rd)},{reg(rt)},{reg(rs)}")
        elif n == "jr":
            d.update(reads=(rs,),control=True,text=f"jr {reg(rs)}")
        elif n == "jalr":
            d.update(reads=(rs,),writes=rd,control=True,text=f"jalr {reg(rd)},{reg(rs)}")
        elif n in ("mfhi","mflo"):
            d.update(writes=rd,text=f"{n} {reg(rd)}")
        elif n in ("mthi","mtlo"):
            d.update(reads=(rs,),text=f"{n} {reg(rs)}")
        elif n in ("mult","multu","div","divu"):
            d.update(reads=(rs,rt),text=f"{n} {reg(rs)},{reg(rt)}")
        elif n in ("syscall","break"):
            d["text"] = n
        else:
            d.update(reads=(rs,rt),writes=rd,text=f"{n} {reg(rd)},{reg(rs)},{reg(rt)}")
        return d
    if op == 1:
        n = {0:"bltz",1:"bgez",16:"bltzal",17:"bgezal"}.get(rt,"regimm")
        target = (pc + 4 + (simm << 2)) & 0xFFFFFFFF
        d.update(mn=n,reads=(rs,),control=True,target=target,
                 text=f"{n} {reg(rs)},0x{target:08X}")
        return d
    if op in (2,3):
        target = (((pc + 4) & 0xF0000000) | ((w & 0x03FFFFFF) << 2)) & 0xFFFFFFFF
        n = "j" if op == 2 else "jal"
        d.update(mn=n,control=True,target=target,text=f"{n} 0x{target:08X}")
        return d
    if op in BRANCH:
        n = BRANCH[op]
        reads = (rs,rt) if op in (4,5) else (rs,)
        target = (pc + 4 + (simm << 2)) & 0xFFFFFFFF
        d.update(mn=n,reads=reads,control=True,target=target,
                 text=f"{n} " + ",".join(reg(x) for x in reads) + f",0x{target:08X}")
        return d
    if op in IMMEDIATE:
        n = IMMEDIATE[op]
        val = imm if op in (12,13,14) else simm
        d.update(mn=n,reads=(rs,),writes=rt,
                 text=f"{n} {reg(rt)},{reg(rs)},0x{val & 0xFFFFFFFF:X}")
        return d
    if op == 15:
        d.update(mn="lui",writes=rt,text=f"lui {reg(rt)},0x{imm:04X}")
        return d
    if op in MEM:
        n,width,rw = MEM[op]
        d.update(mn=n,reads=(rs,) if rw=="R" else (rs,rt),
                 writes=rt if rw=="R" else None,mem=(width,rw,simm,rs,rt),
                 text=f"{n} {reg(rt)},{simm}({reg(rs)})")
        return d
    if op in (0x2F,0x32,0x3A):
        n = {0x2F:"cache",0x32:"lwc2",0x3A:"swc2"}[op]
        d.update(mn=n,reads=(rs,),mem=(4,"R" if op==0x32 else "W",simm,rs,rt),
                 text=f"{n} 0x{rt:X},{simm}({reg(rs)})")
        return d
    if op in (0x10,0x11,0x12,0x13):
        cop = op - 0x10
        sub = (w >> 21) & 31
        if sub == 0:
            d.update(mn=f"mfc{cop}",writes=rt,text=f"mfc{cop} {reg(rt)},$c{rd}")
        elif sub == 4:
            d.update(mn=f"mtc{cop}",reads=(rt,),text=f"mtc{cop} $c{rd},{reg(rt)}")
        elif op == 0x10 and fn == 0x10:
            d.update(mn="rfe",text="rfe")
        else:
            d.update(mn=f"cop{cop}",text=f"cop{cop} 0x{w & 0x1FFFFFF:07X}")
        return d
    d.update(mn=f"op_{op:02X}",text=f"op_{op:02X} 0x{w & 0x3FFFFFF:07X}")
    return d

def is_prologue(ins: list[dict], i: int) -> bool:
    d = ins[i]
    if d["mn"] != "addiu" or d["rt"] != 29 or d["rs"] != 29 or d["simm"] >= 0:
        return False
    # Stack save(s) shortly after the frame allocation make this a conservative boundary.
    for q in ins[i+1:min(len(ins),i+9)]:
        if q["mn"] in ("jr","j","jal","jalr"):
            break
        if q["mem"] and q["mem"][1] == "W" and q["mem"][3] == 29 and q["mem"][4] in (31,16,17,18,19,20,21,22,23,30):
            return True
    return False

def build_functions(blob: bytes, base_pc: int) -> tuple[list[dict], list[int]]:
    ins = [decode(blob[i:i+4],base_pc+i) for i in range(0,len(blob)-3,4)]
    starts = [i for i in range(len(ins)) if is_prologue(ins,i)]
    # The first instruction is a boundary only if it is a verified prologue.
    return ins, starts

def const(value: int) -> tuple:
    return ("const", value & 0xFFFFFFFF, "")

def idx(origin: str, factor: int) -> tuple:
    return ("idx", factor, origin)

def add_symbol(a, b):
    if a and b and a[0] == "idx" and b[0] == "idx" and a[2] == b[2]:
        return idx(a[2], a[1] + b[1])
    return None

def provenance(ins: list[dict], start: int, end: int, base_reg: int, arg_values: dict[int,tuple]|None=None) -> tuple[str,str,str,list[int]]:
    arg_values = arg_values or {}
    chain: list[int] = []
    active: set[tuple[int,int]] = set()
    memo: dict[tuple[int,int], tuple|None] = {}

    def find_def(r: int, before: int) -> int|None:
        lo=max(start,before-128)
        for j in range(before-1,lo-1,-1):
            if ins[j]["writes"] == r:
                return j
            if ins[j]["control"]:
                return None
        return None

    def resolve(r: int, before: int, depth: int=0):
        if r == 0:
            return const(0)
        key=(r,before)
        if key in memo:
            return memo[key]
        if depth > 32 or key in active:
            return None
        active.add(key)
        di=find_def(r,before)
        if di is None:
            val=arg_values.get(r,idx(f"ARG_{REGS[r]}",1) if r in (4,5,6,7) else None)
            memo[key]=val
            active.discard(key)
            return val
        d=ins[di]
        chain.append(di)
        val=None
        if d["mn"] == "lui":
            val=const(d["imm"] << 16)
        elif d["mn"] in ("addiu","addi","ori","andi"):
            if d["rs"] == 0:
                val=const(d["imm"] if d["mn"]!="addiu" else d["simm"])
            else:
                a=resolve(d["rs"],di,depth+1)
                if a and a[0]=="const":
                    n=a[1]
                    if d["mn"] in ("addiu","addi"): n=(n+d["simm"]) & 0xFFFFFFFF
                    elif d["mn"]=="ori": n=n|d["imm"]
                    elif d["mn"]=="andi": n=n&d["imm"]
                    val=const(n)
                elif a and a[0] in ("idx","pointer","record","lvbase") and d["mn"] in ("addiu","addi") and d["simm"]==0:
                    val=a
                elif a and a[0] in ("memval","derived"):
                    val=("derived",a,d["mn"],d["simm"] if d["mn"] in ("addiu","addi") else d["imm"])
        elif d["mem"] and d["mem"][1]=="R":
            width,_,disp,rs,_=d["mem"]
            a=resolve(rs,di,depth+1)
            if a and a[0]=="const" and ((a[1]+disp)&0xFFFFFFFF)==RAM_POINTER and d["mn"]=="lw":
                val=("pointer",RAM_POINTER,"P_FROM_8013EA84")
            elif a and a[0] in ("pointer","record","record_offset","lvbase"):
                val=("memval",a,disp,width)
        elif d["mn"] in ("sll","srl","sra"):
            a=resolve(d["rt"],di,depth+1)
            if d["mn"]=="sll" and a and a[0]=="idx":
                val=idx(a[2],a[1]*(1<<d["sh"]))
            elif a and a[0] in ("memval","derived"):
                val=("derived",a,d["mn"],d["sh"])
        elif d["mn"] in ("addu","add","or"):
            a=resolve(d["rs"],di,depth+1)
            b=resolve(d["rt"],di,depth+1)
            if d["mn"]=="or" and a and a[0]=="const" and a[1]==0: val=b
            elif d["mn"]=="or" and b and b[0]=="const" and b[1]==0: val=a
            elif d["mn"] in ("addu","add") and a and a[0] in ("pointer","record","lvbase","idx") and b and b[0]=="const" and b[1]==0: val=a
            elif d["mn"] in ("addu","add") and b and b[0] in ("pointer","record","lvbase","idx") and a and a[0]=="const" and a[1]==0: val=b
            elif a and b and a[0]=="idx" and b[0]=="idx" and a[2]==b[2]:
                val=idx(a[2],a[1]+b[1])
            elif a and a[0]=="pointer" and b and b[0]=="idx":
                val=("record" if b[1]==STRIDE else "lvbase" if b[1]==2 else "pointer_offset",b[1],b[2])
            elif b and b[0]=="pointer" and a and a[0]=="idx":
                val=("record" if a[1]==STRIDE else "lvbase" if a[1]==2 else "pointer_offset",a[1],a[2])
            elif a and a[0]=="record" and b and b[0]=="derived":
                val=("record_offset",a[1],a[2],"MEMORY_DERIVED_OFFSET")
            elif b and b[0]=="record" and a and a[0]=="derived":
                val=("record_offset",b[1],b[2],"MEMORY_DERIVED_OFFSET")
            elif a and a[0]=="record_offset" and b and b[0]=="derived":
                val=("record_offset",a[1],a[2],"MULTIPLE_DERIVED_OFFSETS")
            elif b and b[0]=="record_offset" and a and a[0]=="derived":
                val=("record_offset",b[1],b[2],"MULTIPLE_DERIVED_OFFSETS")
            elif a and a[0]=="const" and b and b[0]=="idx": val=b
            elif b and b[0]=="const" and a and a[0]=="idx": val=a
        elif d["mn"] == "mflo":
            lo=max(start,di-128)
            mi=None
            for j in range(di-1,lo-1,-1):
                if ins[j]["mn"] in ("mult","multu","div","divu"):
                    mi=j; break
                if ins[j]["control"]:
                    break
            if mi is not None and ins[mi]["mn"] in ("mult","multu"):
                chain.append(mi)
                m=ins[mi]
                a=resolve(m["rs"],mi,depth+1); b=resolve(m["rt"],mi,depth+1)
                if a and b and a[0]=="idx" and b[0]=="const": val=idx(a[2],a[1]*b[1])
                elif b and a and b[0]=="idx" and a[0]=="const": val=idx(b[2],b[1]*a[1])
        memo[key]=val
        active.discard(key)
        return val

    value=resolve(base_reg,end)
    chain=sorted(set(chain))
    if value and value[0]=="pointer":
        return "TERBUKTI","EA84_POINTER","basis berasal dari lw pada alamat 0x8013EA84; tanpa skala record",chain
    if value and value[0]=="record":
        return "TERBUKTI","RECORD_BASE_INDEX_X_0x124",f"EA84 pointer + index*0x124; sumber indeks={value[2]}",chain
    if value and value[0]=="record_offset":
        return "TERBUKTI","RECORD_BASE_INDEX_X_0x124_PLUS_MEMORY_OFFSET",f"EA84 pointer + index*0x124 + derived value from record memory; offset meaning TIDAK TAHU; sumber indeks={value[2]}",chain
    if value and value[0]=="lvbase":
        return "TERBUKTI","LV_BASE_INDEX_X_2",f"EA84 pointer + index*2; sumber indeks={value[2]}",chain
    return "TAK TERSELESAIKAN","TIDAK TAHU","def-chain mundur 128 instruksi/awal fungsi tidak membuktikan basis EA84 dan skala indeks",chain

def nearest_func(starts: list[int], i: int) -> int|None:
    prev=[x for x in starts if x<=i]
    return prev[-1] if prev else None

def scan_region(blob: bytes, region: str, base_pc: int, base_off: int):
    ins,starts=build_functions(blob,base_pc)
    rows=[]; branches=[]; validation=[]
    for i,d in enumerate(ins):
        pc=base_pc+4*i; off=base_off+4*i; raw=blob[4*i:4*i+4]
        if d["mn"] in ("beq","bne"):
            branches.append({"region":region,"pc":f"0x{pc:08X}","file_offset":f"0x{off:08X}",
                "bytes_4B":" ".join(f"{x:02X}" for x in raw),"instruction":d["text"],
                "target_pc":f"0x{d['target']:08X}","fallthrough_pc":f"0x{pc+8:08X}"})
        validate_candidate = ((d["mn"] in ("lh","lhu") and d["mem"] is not None and 0x0E <= d["mem"][2] <= 0x1E)
                              or d["mn"] in ("beq","bne"))
        if raw and validate_candidate:
            again=decode(bytes.fromhex(" ".join(f"{x:02X}" for x in raw)),pc)
            validation.append({"region":region,"pc":f"0x{pc:08X}","file_offset":f"0x{off:08X}",
                "bytes_4B":" ".join(f"{x:02X}" for x in raw),"instruction":d["text"],
                "redecoded_instruction":again["text"],"word_hex":f"0x{d['word']:08X}",
                "match":"YES" if again["text"]==d["text"] and again["word"]==d["word"] else "NO",
                "control_target":f"0x{d['target']:08X}" if d["target"] is not None else ""})
        if d["mn"] not in ("lh","lhu") or not (0x0E <= d["mem"][2] <= 0x1E):
            continue
        _,_,disp,base,_=d["mem"]
        func=nearest_func(starts,i)
        reason=[]
        if base==29: reason.append("BASIS_SP")
        if disp & 1: reason.append("DISPLACEMENT_GANJIL")
        if func is None: reason.append("AWAL_FUNGSI_TIDAK_TERBUKTI")
        chain=[]
        status="TAK TERSELESAIKAN"; basis="TIDAK TAHU"; expr=""; chain_text=""
        func_start_pc=f"0x{base_pc+4*func:08X}" if func is not None else ""
        func_end=""
        if func is not None:
            ret_end=next((x+1 for x in range(i,len(ins)) if ins[x]["mn"]=="jr" and ins[x]["rs"]==31),len(ins))
            next_start=next((x for x in starts if x>i),len(ins))
            end=min(ret_end,next_start)
            func_end=f"0x{base_pc+4*end:08X}"
        if not reason:
            status,basis,expr,chain=provenance(ins,func,i,base)
            if status!="TERBUKTI":
                reason.append("DEF_CHAIN_TIDAK_MENCAPAI_BASIS_EA84")
        else:
            # Keep the exact rejection reason instead of pretending the candidate was analyzed as a base.
            pass
        chain_text=";".join(f"0x{base_pc+4*j:08X}:{ins[j]['text']}" for j in chain[-24:])
        category=("TERBUKTI" if status=="TERBUKTI" and not reason else
                  "DIKECUALIKAN" if any(x in ("BASIS_SP","DISPLACEMENT_GANJIL") for x in reason) else
                  "TAK_TERSELESAIKAN")
        rows.append({"region":region,"pc":f"0x{pc:08X}","file_offset":f"0x{off:08X}",
            "index":i,"bytes_4B":" ".join(f"{x:02X}" for x in raw),"instruction":d["text"],
            "base_register":reg(base),"displacement":f"0x{disp:02X}","function_start":func_start_pc,
            "function_end":func_end,"instructions_back":i-func if func is not None else "",
            "status":status if category!="DIKECUALIKAN" else "DIKECUALIKAN",
            "basis_class":basis,"reason":";".join(reason) if reason else expr,
            "def_chain":chain_text})
    return ins,starts,rows,branches,validation

def forward_sites(ins: list[dict], starts: list[int], blob: bytes, region: str,
                  base_pc: int, base_off: int):
    rows=[]; summaries=[]
    idxmap={base_pc+4*i:i for i in range(len(ins))}
    for site_id,pc in enumerate(FORWARD_SITES,1):
        i=idxmap.get(pc)
        if i is None:
            summaries.append({"site_id":site_id,"pc":f"0x{pc:08X}","status":"TAK TERSELESAIKAN","reason":"PC tidak ada di Entry1"})
            continue
        d0=ins[i]
        if d0["mn"] not in ("lh","lhu") or d0["mem"][2]!=0x10:
            summaries.append({"site_id":site_id,"pc":f"0x{pc:08X}","status":"TAK TERSELESAIKAN","reason":"byte/instruksi bukan pembaca +0x10 yang diharapkan"})
            continue
        taint={d0["mem"][4]}; start=nearest_func(starts,i)
        stop=min(len(ins),i+65)
        end_reason="BATAS_64_INSTRUKSI"
        if start is not None:
            ret_end=next((x+1 for x in range(i,len(ins)) if ins[x]["mn"]=="jr" and ins[x]["rs"]==31),len(ins))
            next_start=next((x for x in starts if x>i),len(ins))
            func_end=min(ret_end,next_start)
            stop=min(stop,func_end)
            if stop==func_end: end_reason="AKHIR_FUNGSI_JR_RA"
        used=[]
        trace_start=len(rows)
        for j in range(i+1,stop):
            d=ins[j]; raw=blob[j*4:j*4+4]
            before=set(taint); used_regs=set(d["reads"]) & before
            cls="TIDAK_MENGGUNAKAN_NILAI"; detail=""
            call_args=sorted(before & {4,5,6,7}) if d["mn"] in ("jal","jalr") else []
            if call_args:
                cls="ARGUMEN_JAL"
                target=(f"0x{d['target']:08X}" if d["target"] is not None else "INDIRECT")
                detail=f"{d['mn']} target={target}; tainted_args="+",".join(reg(x) for x in call_args)
            elif used_regs:
                if d["mn"] in ("beq","bne","blez","bgtz","bltz","bgez","slt","sltu","slti","sltiu"):
                    cls="DIBANDINGKAN"; detail=f"{d['mn']} target="+(f"0x{d['target']:08X}" if d["target"] else "NON_BRANCH")
                elif d["mn"] in ("mult","multu","div","divu"):
                    cls="DIKALI_ATAU_DIBAGI"; detail=d["mn"]
                elif d["mem"] and d["mem"][1]=="W":
                    cls="DISIMPAN"; detail=f"{d['mn']} base={reg(d['mem'][3])} offset={d['mem'][2]}"
                elif d["mem"] and d["mem"][1]=="R":
                    cls="DIGUNAKAN_SEBAGAI_BASIS_ALAMAT"; detail=f"{d['mn']} displacement={d['mem'][2]}"
                elif d["mn"] in ("add","addu","addi","addiu","sub","subu"):
                    cls="OPERASI_ARITMETIKA"; detail=d["mn"]
                elif d["mn"] in ("sll","srl","sra","sllv","srlv","srav"):
                    cls="SHIFT"; detail=d["mn"]
                else:
                    cls="DIGUNAKAN"; detail=d["mn"]
            if d["writes"] is not None:
                taint.discard(d["writes"])
                if used_regs: taint.add(d["writes"])
            rows.append({"site_id":site_id,"pc":f"0x{pc:08X}","region":region,
                "file_offset":f"0x{base_off+j*4:08X}","index":j,"bytes_4B":" ".join(f"{x:02X}" for x in raw),
                "instruction":d["text"],"tracked_registers":",".join(reg(x) for x in sorted(before)),
                "classification":cls,"detail":detail,
                "target_pc":f"0x{d['target']:08X}" if d["target"] is not None else ""})
            used.append(cls)
            if not taint:
                end_reason="TAINT_HABIS"; break
            if d["mn"]=="jr" and d["rs"]==31:
                end_reason="AKHIR_FUNGSI_JR_RA"; break
        summaries.append({"site_id":site_id,"pc":f"0x{pc:08X}",
            "status":"TERTELUSURI" if len(rows)>trace_start else "TAK TERSELESAIKAN",
            "decoded_instructions":len(used),"terminal_reason":end_reason,
            "destinations":";".join(sorted(set(x for x in used if x!="TIDAK_MENGGUNAKAN_NILAI"))) or "TIDAK TERLIHAT"})
    return rows,summaries

def self_test():
    pc=0x80010000
    # bne $t0,$t1,+3 => target pc+4+12 = 0x80010010
    word=(5<<26)|(8<<21)|(9<<16)|3
    d=decode(word.to_bytes(4,"little"),pc)
    assert d["mn"]=="bne" and d["target"]==0x80010010
    # beq $a0,$zero,-2 => target pc-4
    word=(4<<26)|(4<<21)|((0xFFFE)&0xFFFF)
    d=decode(word.to_bytes(4,"little"),pc)
    assert d["mn"]=="beq" and d["target"]==(pc-4)
    assert decode(bytes.fromhex("10 00 42 84"),0x80010000)["text"]=="lh $v0,16($v0)"
    def rword(rs,rt,rd,sh,fn):
        return (rs<<21)|(rt<<16)|(rd<<11)|(sh<<6)|fn
    def iword(op,rs,rt,imm):
        return (op<<26)|(rs<<21)|(rt<<16)|(imm & 0xFFFF)
    words=[
      iword(0x0F,0,2,0x8014),                 # lui v0,0x8014
      iword(0x23,2,3,-5500),                 # lw v1,-5500(v0) -> *(0x8013EA84)
      rword(0,4,2,3,0),                      # sll v0,a0,3
      rword(2,4,2,0,33),                     # addu v0,v0,a0
      rword(0,2,2,3,0),                      # sll v0,v0,3
      rword(2,4,2,0,33),                     # addu v0,v0,a0
      rword(0,2,2,2,0),                      # sll v0,v0,2 => index*0x124
      rword(2,3,2,0,33),                     # addu v0,v0,v1 => record base
      iword(0x25,2,3,32),                    # lhu v1,32(v0)
      rword(0,3,3,7,2),                      # srl v1,v1,7
      iword(0x0C,3,3,0x1E),                  # andi v1,v1,0x1e
      rword(2,3,2,0,33),                     # addu v0,v0,v1
      iword(0x25,2,2,16),                    # lhu v0,16(v0)
    ]
    synthetic=[decode((w & 0xFFFFFFFF).to_bytes(4,"little"),0x800B7700+4*i)
               for i,w in enumerate(words)]
    st,basis,detail,_=provenance(synthetic,0,len(synthetic)-1,2)
    assert st=="TERBUKTI" and basis=="RECORD_BASE_INDEX_X_0x124_PLUS_MEMORY_OFFSET", (st,basis,detail)
    print("UO0_SELF_TEST=PASS branch targets, byte decode and EA84/index*0x124 derived-memory def-chain")


def taint_step(d, regs, hi, lo):
    out=set(regs); used=set(d["reads"]) & out; mn=d["mn"]
    if mn in ("mult","multu","div","divu"):
        active=bool(set(d["reads"]) & out)
        return out,active,active
    if mn=="mthi": return out,bool(d["reads"] and d["reads"][0] in out),lo
    if mn=="mtlo": return out,hi,bool(d["reads"] and d["reads"][0] in out)
    if mn=="mfhi" and d["writes"] is not None:
        if hi: out.add(d["writes"])
        else: out.discard(d["writes"])
    elif mn=="mflo" and d["writes"] is not None:
        if lo: out.add(d["writes"])
        else: out.discard(d["writes"])
    elif d["writes"] is not None:
        out.discard(d["writes"])
        if used: out.add(d["writes"])
    return out,hi,lo

def const_reg_before(ins, before, r, depth=0):
    if r==0: return 0
    if depth>10: return None
    for q in range(before-1,max(-1,before-33),-1):
        d=ins[q]
        if d["writes"]!=r: continue
        if d["mn"]=="lui": return (d["imm"]<<16)&0xFFFFFFFF
        if d["mn"] in ("addiu","addi","ori","andi"):
            if d["rs"]==0: return (d["simm"] if d["mn"] in ("addiu","addi") else d["imm"])&0xFFFFFFFF
            v=const_reg_before(ins,q,d["rs"],depth+1)
            if v is None:return None
            if d["mn"] in ("addiu","addi"):return (v+d["simm"])&0xFFFFFFFF
            if d["mn"]=="ori":return v|d["imm"]
            return v&d["imm"]
        if d["mn"]=="sll":
            v=const_reg_before(ins,q,d["rt"],depth+1)
            return None if v is None else (v<<d["sh"])&0xFFFFFFFF
        return None
    return None

def forward_graph(site_id, site_pc, ins, blob, region, base_pc, base_off):
    idxmap={base_pc+4*i:i for i in range(len(ins))}
    first_idx=idxmap.get(site_pc)
    rows=[]; calls=[]; returns=[]; seen=set(); terminals=set()
    if first_idx is None:
        return rows,{"site_id":site_id,"pc":f"0x{site_pc:08X}","status":"TIDAK TAHU",
          "decoded_instructions":0,"terminal_reason":"PC_TIDAK_ADA","destinations":"","return_v0":"TIDAK TAHU"},calls
    first=ins[first_idx]
    if first["mn"] not in ("lh","lhu") or not first["mem"] or first["mem"][2]!=0x10:
        return rows,{"site_id":site_id,"pc":f"0x{site_pc:08X}","status":"TIDAK TAHU",
          "decoded_instructions":0,"terminal_reason":"BUKAN_U16_PLUS_0x10","destinations":first["text"],"return_v0":"TIDAK TAHU"},calls
    # State: instruction index, tainted GPRs, HI/LO, call-return stack, depth and path steps.
    queue=[(first_idx+1,{first["mem"][4]},False,False,(),0)]
    max_states=2500; max_steps=180
    while queue and len(seen)<max_states:
        i,regs,hi,lo,stack,steps=queue.pop(0)
        key=(i,tuple(sorted(regs)),hi,lo,stack)
        if key in seen or i<0 or i>=len(ins) or steps>=max_steps: continue
        seen.add(key)
        d=ins[i]; mn=d["mn"]; pc=base_pc+4*i; raw=blob[4*i:4*i+4]
        before=set(regs); used=set(d["reads"]) & before
        after,hi2,lo2=taint_step(d,before,hi,lo)
        control=mn in ("j","jal","jalr","jr") or bool(d["control"])
        slot=None; slot_after=set(after); slot_hi=hi2; slot_lo=lo2
        if control and i+1<len(ins):
            slot=ins[i+1]; slot_after,slot_hi,slot_lo=taint_step(slot,slot_after,slot_hi,slot_lo)
        cls="TIDAK_MENGGUNAKAN_NILAI"; detail=""
        if mn in ("jal","jalr"):
            args=sorted(before & {4,5,6,7})
            target=d["target"] if mn=="jal" else const_reg_before(ins,i,d["rs"])
            ts=f"0x{target:08X}" if target is not None else "TIDAK TAHU"
            cls="CALL_AND_RETURN"
            detail=f"target={ts}; tainted_args="+(",".join(reg(x) for x in args) if args else "NONE")+"; delay-slot dieksekusi; caller-saved hasil lama di-clobber"
            calls.append({"site_id":site_id,"site_pc":f"0x{site_pc:08X}","call_pc":f"0x{pc:08X}",
              "target_pc":ts,"tainted_arguments":",".join(reg(x) for x in args) or "NONE"})
        elif mn=="jr":
            if d["rs"]==31:
                cls="RETURN_V0_TAINTED" if 2 in slot_after else "RETURN_V0_UNTAINTED"
                detail="jr $ra; delay-slot diproses; "+("v0 membawa taint" if 2 in slot_after else "v0 tidak membawa taint")
            else:
                target=const_reg_before(ins,i,d["rs"])
                cls="JR_INDIRECT"; detail="jr "+reg(d["rs"])+"; target="+(f"0x{target:08X}" if target is not None else "TIDAK TAHU")
        elif mn in ("beq","bne","blez","bgtz","bltz","bgez"):
            cls="BRANCH_TAINTED" if used else "BRANCH"
            detail=f"target=0x{d['target']:08X}; target dan fallthrough dieksplorasi"
        elif mn in ("mult","multu","div","divu"):
            cls="HI_LO_TAINT" if used else "HI_LO_OPERATION"; detail=mn
        elif mn in ("mfhi","mflo"):
            cls="HI_LO_READ"; detail=f"{mn}; taint={'YES' if (hi if mn=='mfhi' else lo) else 'NO'}"
        elif used:
            if d["mem"] and d["mem"][1]=="W":cls="STORE_TAINTED";detail=f"{mn} base={reg(d['mem'][3])} disp={d['mem'][2]}"
            elif d["mem"] and d["mem"][1]=="R":cls="LOAD_TAINTED_ADDRESS";detail=f"{mn} disp={d['mem'][2]}"
            else:cls="ARITHMETIC_OR_COMPARE";detail=mn
        rows.append({"site_id":site_id,"pc":f"0x{site_pc:08X}","region":region,"file_offset":f"0x{base_off+4*i:08X}",
          "index":i,"bytes_4B":" ".join(f"{x:02X}" for x in raw),"instruction":d["text"],
          "tracked_registers":",".join(reg(x) for x in sorted(before)),"classification":cls,"detail":detail,
          "target_pc":f"0x{d['target']:08X}" if d["target"] is not None else "",
          "trace_pc":f"0x{pc:08X}","tainted_after":",".join(reg(x) for x in sorted(after))})
        if slot is not None:
            slotraw=blob[4*(i+1):4*(i+2)]
            rows.append({"site_id":site_id,"pc":f"0x{site_pc:08X}","region":region,
              "file_offset":f"0x{base_off+4*(i+1):08X}","index":i+1,
              "bytes_4B":" ".join(f"{x:02X}" for x in slotraw),"instruction":slot["text"],
              "tracked_registers":",".join(reg(x) for x in sorted(after)),"classification":"DELAY_SLOT",
              "detail":"delay slot "+mn,"target_pc":"","trace_pc":f"0x{pc+4:08X}",
              "tainted_after":",".join(reg(x) for x in sorted(slot_after))})
        if mn=="jr" and d["rs"]==31:
            if stack:
                cont=stack[-1]; newstack=stack[:-1]
                # Caller-saved regs are undefined after return except the newly returned v0.
                returned_v0=(2 in slot_after)
                returned=set(slot_after) - {3,4,5,6,7,8,9,10,11,12,13,14,15,24,25}
                if returned_v0: returned.add(2)
                else: returned.discard(2)
                queue.append((cont,returned,False,False,newstack,steps+1))
            else:
                returns.append("RETURN_V0_TAINTED" if 2 in slot_after else "RETURN_V0_UNTAINTED")
                terminals.add("RETURN_TO_CALLER")
            continue
        if control:
            nregs=set(slot_after); nhi=slot_hi; nlo=slot_lo
            if mn in ("jal","jalr"):
                target=d["target"] if mn=="jal" else const_reg_before(ins,i,d["rs"])
                target_idx=idxmap.get(target) if target is not None else None
                # T registers and old v0/v1 are caller-saved; keep tainted a0-a3 for callee input.
                for rr in (2,3,8,9,10,11,12,13,14,15,24,25): nregs.discard(rr)
                nhi=False; nlo=False
                if target_idx is not None and len(stack)<8:
                    queue.append((target_idx,nregs,nhi,nlo,stack+(i+2,),steps+1))
                elif i+2<len(ins):
                    # Unresolved/out-of-image callee is opaque; its returned v0 is not inferred.
                    for rr in (2,3,4,5,6,7,8,9,10,11,12,13,14,15,24,25): nregs.discard(rr)
                    queue.append((i+2,nregs,False,False,stack,steps+1))
            elif mn=="j":
                ti=idxmap.get(d["target"])
                if ti is not None:queue.append((ti,nregs,nhi,nlo,stack,steps+1))
                else:terminals.add("J_TARGET_OUTSIDE_REGION")
            elif mn=="jr":
                target=const_reg_before(ins,i,d["rs"]);ti=idxmap.get(target) if target is not None else None
                if ti is not None:queue.append((ti,nregs,nhi,nlo,stack,steps+1))
                else:terminals.add("JR_TARGET_TIDAK_TAHU")
            else:
                ti=idxmap.get(d["target"])
                if ti is not None:queue.append((ti,set(nregs),nhi,nlo,stack,steps+1))
                if i+2<len(ins):queue.append((i+2,set(nregs),nhi,nlo,stack,steps+1))
            continue
        if i+1<len(ins):queue.append((i+1,after,hi2,lo2,stack,steps+1))
    dest=sorted({x["classification"] for x in rows if x["classification"] not in ("TIDAK_MENGGUNAKAN_NILAI","BRANCH","DELAY_SLOT")})
    rv=";".join(sorted(set(returns))) or "TIDAK TAHU"
    summary={"site_id":site_id,"pc":f"0x{site_pc:08X}","status":"TERTELUSURI" if rows else "TIDAK TAHU",
      "decoded_instructions":len(rows),"terminal_reason":"STATE_LIMIT" if len(seen)>=max_states else ";".join(sorted(terminals)) or ("RETURN_V0" if returns else "TRACE_BOUND_OR_NO_RETURN"),
      "destinations":";".join(dest) or "TIDAK TERLIHAT","return_v0":rv}
    return rows,summary,calls

def function_span(ins, starts, idx):
    st=nearest_func(starts,idx)
    if st is None: st=idx
    end=len(ins)
    for q in range(idx,len(ins)):
        if ins[q]["mn"]=="jr" and ins[q]["rs"]==31:
            end=min(len(ins),q+2); break
        if q>st and q in starts and q-idx>4:
            end=q; break
    return st,end

def independent_decode(raw,pc):
    if len(raw)!=4:raise ValueError("INDEPENDENT_MIPS_WORD_LENGTH")
    w=int.from_bytes(raw,"little");op=(w>>26)&63;rs=(w>>21)&31;rt=(w>>16)&31
    rd=(w>>11)&31;sh=(w>>6)&31;fn=w&63;imm=w&65535;sx=imm if imm<32768 else imm-65536
    mn=".word";target=None;text=f".word 0x{w:08X}"
    if op==0:
        mn={0:"sll",2:"srl",3:"sra",4:"sllv",6:"srlv",7:"srav",8:"jr",9:"jalr",12:"syscall",13:"break",16:"mfhi",17:"mthi",18:"mflo",19:"mtlo",24:"mult",25:"multu",26:"div",27:"divu",32:"add",33:"addu",34:"sub",35:"subu",36:"and",37:"or",38:"xor",39:"nor",42:"slt",43:"sltu"}.get(fn,".word")
        if mn in ("sll","srl","sra"):text=f"{mn} {reg(rd)},{reg(rt)},{sh}"
        elif mn in ("sllv","srlv","srav"):text=f"{mn} {reg(rd)},{reg(rt)},{reg(rs)}"
        elif mn=="jr":text=f"jr {reg(rs)}"
        elif mn=="jalr":text=f"jalr {reg(rd)},{reg(rs)}"
        elif mn in ("syscall","break"):text=mn
        elif mn in ("mfhi","mflo"):text=f"{mn} {reg(rd)}"
        elif mn in ("mthi","mtlo"):text=f"{mn} {reg(rs)}"
        elif mn in ("mult","multu","div","divu"):text=f"{mn} {reg(rs)},{reg(rt)}"
        elif mn!=".word":text=f"{mn} {reg(rd)},{reg(rs)},{reg(rt)}"
    elif op==1:
        mn={0:"bltz",1:"bgez",16:"bltzal",17:"bgezal"}.get(rt,"regimm")
        target=(pc+4+(sx<<2))&0xFFFFFFFF;text=f"{mn} {reg(rs)},0x{target:08X}"
    elif op in (2,3):
        mn="j" if op==2 else "jal";target=(((pc+4)&0xF0000000)|((w&0x03FFFFFF)<<2))&0xFFFFFFFF;text=f"{mn} 0x{target:08X}"
    elif op in (4,5,6,7):
        mn={4:"beq",5:"bne",6:"blez",7:"bgtz"}[op];target=(pc+4+(sx<<2))&0xFFFFFFFF
        args=f"{reg(rs)},{reg(rt)}" if op in (4,5) else reg(rs);text=f"{mn} {args},0x{target:08X}"
    elif op in (8,9,10,11,12,13,14):
        mn={8:"addi",9:"addiu",10:"slti",11:"sltiu",12:"andi",13:"ori",14:"xori"}[op]
        value=imm if op in (12,13,14) else sx;text=f"{mn} {reg(rt)},{reg(rs)},0x{value&0xFFFFFFFF:X}"
    elif op==15:mn="lui";text=f"lui {reg(rt)},0x{imm:04X}"
    elif op in (0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x28,0x29,0x2A,0x2B,0x2E):
        mn={0x20:"lb",0x21:"lh",0x22:"lwl",0x23:"lw",0x24:"lbu",0x25:"lhu",0x26:"lwr",0x28:"sb",0x29:"sh",0x2A:"swl",0x2B:"sw",0x2E:"swr"}[op]
        text=f"{mn} {reg(rt)},{sx}({reg(rs)})"
    elif op in (0x2F,0x32,0x3A):
        mn={0x2F:"cache",0x32:"lwc2",0x3A:"swc2"}[op];text=f"{mn} 0x{rt:X},{sx}({reg(rs)})"
    elif op in (0x10,0x11,0x12,0x13):
        cop=op-0x10;sub=(w>>21)&31
        if sub==0:mn=f"mfc{cop}";text=f"{mn} {reg(rt)},$c{rd}"
        elif sub==4:mn=f"mtc{cop}";text=f"{mn} $c{rd},{reg(rt)}"
        elif op==0x10 and fn==0x10:mn="rfe";text="rfe"
        else:mn=f"cop{cop}";text=f"{mn} 0x{w&0x1FFFFFF:07X}"
    elif op not in (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15):
        mn=f"op_{op:02X}";text=f"{mn} 0x{w&0x3FFFFFF:07X}"
    return {"mn":mn,"target":target,"text":text,"word":w}

def setup_arg(ins,ix,r,base_pc):
    for q in range(ix-1,max(-1,ix-17),-1):
        if ins[q]["writes"]==r:return f"0x{base_pc+4*q:08X}:{ins[q]['text']}"
        if ins[q]["control"]:break
    return "TIDAK TAHU"

def next_v0_use(ins,ix,base_pc):
    found=[]
    for q in range(ix+1,min(len(ins),ix+18)):
        d=ins[q]
        if d["control"] or d["mn"] in ("jr","j","jal","jalr"):break
        if 2 in d["reads"]:found.append(f"0x{base_pc+4*q:08X}:{d['text']}")
    return ";".join(found) if found else "TIDAK TERLIHAT_DALAM_16_INSTRUKSI"

def main_up0(a):
    exe=a.exe.read_bytes();data=a.data_bin.read_bytes()
    if len(exe)!=EXE_SIZE or digest(exe)!=EXE_SHA:raise SystemExit("UP0_EXE_IDENTITY_MISMATCH")
    if len(data)!=DATA_SIZE or digest(data)!=DATA_SHA:raise SystemExit("UP0_DATA_BIN_IDENTITY_MISMATCH")
    e1=data[E1_OFF:E1_OFF+E1_SIZE]
    if len(e1)!=E1_SIZE or digest(e1)!=ENTRY1_SHA:raise SystemExit("UP0_ENTRY1_IDENTITY_MISMATCH")
    regions=[]
    for blob,name,pc,off in ((exe[EXE_OFF:],"EXE",EXE_PC,EXE_OFF),(e1,"ENTRY1",E1_PC,E1_OFF)):
        ii,ss=build_functions(blob,pc);regions.append((blob,name,pc,off,ii,ss))
    rmap={x[1]:x for x in regions};targets={0x800B76BC,0x800B770C}
    fwd=[];fsum=[];fcalls=[];disasm=[];callers=[];literals=[];writers=[];rmw=[];sitebases=[]
    for blob,name,pcbase,offbase,ins,starts in regions:
        if name=="ENTRY1":
            for sid,site in enumerate(FORWARD_SITES,1):
                rr,ss,cc=forward_graph(sid,site,ins,blob,name,pcbase,offbase);fwd+=rr;fsum.append(ss);fcalls+=cc
        for target in targets:
            if target>=pcbase and (target-pcbase)%4==0 and (target-pcbase)//4<len(ins):
                ti=(target-pcbase)//4;st,en=function_span(ins,starts,ti)
                for q in range(st,en):
                    d=ins[q];raw=blob[4*q:4*q+4]
                    disasm.append({"region":name,"pc":f"0x{pcbase+4*q:08X}","file_offset":f"0x{offbase+4*q:08X}",
                      "bytes_4B":" ".join(f"{v:02X}" for v in raw),"instruction":d["text"],
                      "function_boundary":"START" if q==st else "END" if q==en-1 else ""})
        for q,d in enumerate(ins):
            raw=blob[4*q:4*q+4];target=None;kind=""
            if d["mn"] in ("jal","j") and d["target"] in targets:target=d["target"];kind=d["mn"].upper()
            elif d["mn"]=="jalr":
                val=const_reg_before(ins,q,d["rs"])
                if val in targets:target=val;kind="JALR_CONST"
            if kind:
                st,_=function_span(ins,starts,q);args=[setup_arg(ins,q,k,pcbase) for k in (4,5,6,7)]
                callers.append({"region":name,"pc":f"0x{pcbase+4*q:08X}","file_offset":f"0x{offbase+4*q:08X}",
                  "bytes_4B":" ".join(f"{v:02X}" for v in raw),"instruction":d["text"],"call_kind":kind,
                  "target_pc":f"0x{target:08X}","caller_function_start":f"0x{pcbase+4*st:08X}",
                  "setup_a0":args[0],"setup_a1":args[1],"setup_a2":args[2],"setup_a3":args[3],
                  "setup_status":"BUKTI" if all(v!="TIDAK TAHU" for v in args) else "TIDAK TAHU",
                  "v0_after_return":next_v0_use(ins,q,pcbase)})
            elif d["mn"]=="jalr":
                callers.append({"region":name,"pc":f"0x{pcbase+4*q:08X}","file_offset":f"0x{offbase+4*q:08X}",
                  "bytes_4B":" ".join(f"{v:02X}" for v in raw),"instruction":d["text"],"call_kind":"JALR_TARGET_TIDAK_TAHU",
                  "target_pc":"TIDAK TAHU","caller_function_start":"","setup_a0":setup_arg(ins,q,4,pcbase),
                  "setup_a1":setup_arg(ins,q,5,pcbase),"setup_a2":setup_arg(ins,q,6,pcbase),
                  "setup_a3":setup_arg(ins,q,7,pcbase),"setup_status":"TIDAK TAHU",
                  "v0_after_return":next_v0_use(ins,q,pcbase)})
        for off in range(len(blob)-3):
            value=int.from_bytes(blob[off:off+4],"little")
            if value in targets:
                literals.append({"region":name,"file_offset":f"0x{offbase+off:08X}",
                  "pc_if_code":f"0x{pcbase+off:08X}","literal_value":f"0x{value:08X}","target_class":"READER_FUNCTION_CANDIDATE"})
        for q,d in enumerate(ins):
            if d["mn"] not in ("sb","sh","sw","swl","swr") or not d["mem"] or d["mem"][1]!="W":continue
            _,_,disp,baser,src=d["mem"]
            if disp not in (0x20,0x21):continue
            st,_=function_span(ins,starts,q);ps,pb,pd,_=provenance(ins,st,q,baser)
            if baser==29:bclass="$sp"
            elif ps=="TERBUKTI" and "RECORD_BASE_INDEX_X_0x124" in pb:bclass="EA84+index*0x124 TERBUKTI"
            elif ps=="TERBUKTI":bclass="LAIN (basis statis terbukti)"
            else:bclass="TIDAK TAHU"
            if d["mn"]=="sb" and disp==0x20:bit="TIDAK (byte +0x20 saja)"
            elif d["mn"] in ("sb","sh","sw") and (disp==0x21 or (d["mn"] in ("sh","sw") and disp==0x20)):bit="YA (store menjangkau byte +0x21)"
            else:bit="TIDAK TAHU (SWL/SWR lane)"
            writers.append({"region":name,"pc":f"0x{pcbase+4*q:08X}","file_offset":f"0x{offbase+4*q:08X}",
              "bytes_4B":" ".join(f"{v:02X}" for v in blob[4*q:4*q+4]),"instruction":d["text"],
              "base_register":reg(baser),"data_register":reg(src),"function_start":f"0x{pcbase+4*st:08X}",
              "basis_class":bclass,"basis_detail":pd,"bits_8_11_written":bit})
            if d["mn"]=="sh" and disp==0x20:
                for p in range(max(st,q-7),q):
                    ld=ins[p]
                    if ld["mn"]=="lhu" and ld["mem"] and ld["mem"][2]==0x20 and ld["mem"][3]==baser:
                        lineage={ld["writes"]};ops=[]
                        for z in range(p+1,q):
                            op=ins[z]
                            if op["mn"] in ("andi","ori") and op["rs"] in lineage:
                                lineage.add(op["rt"]);ops.append(z)
                        if ops and src in lineage:
                            rmw.append({"region":name,"load_pc":f"0x{pcbase+4*p:08X}",
                              "mask_ops":";".join(f"0x{pcbase+4*z:08X}:{ins[z]['text']}" for z in ops),
                              "store_pc":f"0x{pcbase+4*q:08X}","store_instruction":d["text"],
                              "mask_immediates":";".join(f"0x{ins[z]['imm']:04X}" for z in ops),
                              "basis_class":bclass,"bits_8_11_written":"YA: sh +0x20 menulis setengahword penuh"})
        if name=="ENTRY1":
            for site in (0x800CE0F4,0x800D0D70):
                if site<pcbase or (site-pcbase)%4:continue
                si=(site-pcbase)//4
                if si>=len(ins):
                    sitebases.append({"site_pc":f"0x{site:08X}","function_start":"TIDAK TAHU",
                      "caller_pc":"TIDAK TAHU","caller_function_start":"TIDAK TAHU","base_register":"TIDAK TAHU",
                      "basis_status":"TIDAK TAHU","basis_class":"TIDAK TAHU","def_chain":"",
                      "setup_a0":"TIDAK TAHU","setup_a1":"TIDAK TAHU","setup_a2":"TIDAK TAHU","setup_a3":"TIDAK TAHU",
                      "reason":"PC DI LUAR ENTRY 1"})
                    continue
                if not ins[si]["mem"] or ins[si]["mem"][2]!=0x10:
                    sitebases.append({"site_pc":f"0x{site:08X}","function_start":"TIDAK TAHU",
                      "caller_pc":"TIDAK TAHU","caller_function_start":"TIDAK TAHU","base_register":"TIDAK TAHU",
                      "basis_status":"TIDAK TAHU","basis_class":"TIDAK TAHU","def_chain":"",
                      "setup_a0":"TIDAK TAHU","setup_a1":"TIDAK TAHU","setup_a2":"TIDAK TAHU","setup_a3":"TIDAK TAHU",
                      "reason":"BYTE/INSTRUKSI TIDAK MEMBUKTIKAN PEMBACA U16 +0x10"})
                    continue
                st,en=function_span(ins,starts,si)
                br=ins[si]["mem"][3]
                function_start_pc=pcbase+4*st
                function_end_pc=pcbase+4*en
                incoming=[]
                for caller_region in regions:
                    _,cname,cpc,_,cins,cstarts=caller_region
                    for cq,cd in enumerate(cins):
                        ctarget=None
                        if cd["mn"] in ("jal","j"):
                            ctarget=cd["target"]
                        elif cd["mn"]=="jalr":
                            ctarget=const_reg_before(cins,cq,cd["rs"])
                        if ctarget is None or not (function_start_pc<=ctarget<function_end_pc):
                            continue
                        cst=nearest_func(cstarts,cq)
                        if cst is None:
                            cst=cq
                        # Do not mistake an intra-function j/branch for an incoming caller.
                        if cname==name and cst==st:
                            continue
                        incoming.append((cname,cins,cstarts,cq,cpc,cst))
                if not incoming:
                    ps,pb,pd,ch=provenance(ins,st,si,br)
                    sitebases.append({"site_pc":f"0x{site:08X}","function_start":f"0x{function_start_pc:08X}",
                      "caller_pc":"TIDAK TAHU","caller_function_start":"TIDAK TAHU",
                      "base_register":reg(br),"basis_status":"TERBUKTI" if ps=="TERBUKTI" and "RECORD_BASE_INDEX_X_0x124" in pb else "TIDAK TAHU",
                      "basis_class":pb,"def_chain":";".join(f"0x{pcbase+4*z:08X}:{ins[z]['text']}" for z in ch),
                      "setup_a0":"TIDAK TAHU","setup_a1":"TIDAK TAHU","setup_a2":"TIDAK TAHU","setup_a3":"TIDAK TAHU",
                      "reason":"TIDAK ADA CALLSITE TERBUKTI; "+pd})
                for cname,cins,cstarts,cq,cpc,cst in incoming:
                    arg_values={}
                    setup_text=[]
                    for argreg in (4,5,6,7):
                        setup_idx=None
                        for z in range(cq-1,max(cst-1,cq-17),-1):
                            if cins[z]["writes"]==argreg:
                                setup_idx=z
                                break
                            if cins[z]["control"]:
                                break
                        setup_text.append(f"0x{cpc+4*setup_idx:08X}:{cins[setup_idx]['text']}" if setup_idx is not None else "TIDAK TAHU")
                    # Propagate any caller-saved or callee-saved register reaching the call;
                    # a0-a3 setup evidence remains bounded separately to 16 instructions above.
                    for incoming_reg in range(1,32):
                        if incoming_reg==29:
                            continue
                        istatus,ibasis,_,_=provenance(cins,cst,cq,incoming_reg)
                        if istatus=="TERBUKTI" and ibasis=="EA84_POINTER":
                            arg_values[incoming_reg]=("pointer",RAM_POINTER,"P_FROM_CALLER_EA84")
                        elif istatus=="TERBUKTI" and "RECORD_BASE_INDEX_X_0x124" in ibasis:
                            arg_values[incoming_reg]=("record",STRIDE,"CALLER_RECORD")
                        elif istatus=="TERBUKTI" and ibasis=="LV_BASE_INDEX_X_2":
                            arg_values[incoming_reg]=("lvbase",2,"CALLER_LV_BASE")
                        else:
                            arg_values[incoming_reg]=idx(f"CALLER_{cname}_{cpc+4*cq:08X}_{REGS[incoming_reg]}",1)
                    ps,pb,pd,ch=provenance(ins,st,si,br,arg_values)
                    proven=ps=="TERBUKTI" and ("RECORD_BASE_INDEX_X_0x124" in pb)
                    sitebases.append({"site_pc":f"0x{site:08X}","function_start":f"0x{function_start_pc:08X}",
                      "caller_pc":f"0x{cpc+4*cq:08X}","caller_function_start":f"0x{cpc+4*cst:08X}",
                      "base_register":reg(br),"basis_status":"TERBUKTI" if proven else "TIDAK TAHU",
                      "basis_class":pb,"def_chain":";".join(f"0x{pcbase+4*z:08X}:{ins[z]['text']}" for z in ch),
                      "setup_a0":setup_text[0],"setup_a1":setup_text[1],"setup_a2":setup_text[2],"setup_a3":setup_text[3],
                      "reason":pd if proven else "ARGUMENT_CALLER_TIDAK_MEMBUKTIKAN_RANTAI_LUI_LW_EA84_INDEX_X_0x124"})
    entry_ins=rmap["ENTRY1"][4]
    entry_by_pc={E1_PC+4*i:d for i,d in enumerate(entry_ins)}
    def at(pc):
        return entry_by_pc.get(pc)
    def exact(pc,mn,**fields):
        d=at(pc)
        return bool(d and d["mn"]==mn and all(d.get(k)==v for k,v in fields.items()))
    def instruction(pc,text):
        d=at(pc)
        return bool(d and d["text"]==text)
    dispatch_addr=None
    dispatch_ok=(
      exact(0x800B7738,"sltiu",rs=3,rt=2,imm=5) and
      exact(0x800B773C,"beq",rs=2,rt=0,target=0x800B7798) and
      exact(0x800B7740,"sll",rd=3,rt=3,sh=2) and
      exact(0x800B7744,"lui",rt=2,imm=0x800B) and
      exact(0x800B7748,"addiu",rs=2,rt=2,simm=-0x2A0C) and
      exact(0x800B774C,"addu",rd=3,rs=3,rt=2) and
      exact(0x800B7750,"lw",rt=2,rs=3) and
      exact(0x800B7758,"jr",rs=2))
    jumptable_rows=[]
    if dispatch_ok:
        dispatch_addr=0x800AD5F4
        table_offset=E1_OFF+(dispatch_addr-E1_PC)
        for selector in range(5):
            pos=table_offset+selector*4
            raw=data[pos:pos+4]
            target=int.from_bytes(raw,"little")
            site_id_by_target={0x800B7760:1,0x800B77A0:2,0x800B7808:3,
                               0x800B7850:4,0x800B789C:5}
            sid=site_id_by_target.get(target)
            trace=[x for x in fwd if sid is not None and x["site_id"]==sid]
            sequence=";".join(f'{x["trace_pc"]}:{x["instruction"]}' for x in trace)
            expression="TIDAK TAHU"
            input_reg="TIDAK TAHU"
            formula_status="SEQUENCE_ONLY"
            reader_site=f"0x{FORWARD_SITES[sid-1]:08X}" if sid else "TIDAK TAHU"
            common_div10=all((
              instruction(0x800B77E8,"lui $v1,0x6666"),
              instruction(0x800B77EC,"ori $v1,$v1,0x6667"),
              instruction(0x800B77F0,"mult $v0,$v1"),
              instruction(0x800B77F4,"mfhi $v1"),
              instruction(0x800B77F8,"sra $v1,$v1,2"),
              instruction(0x800B77FC,"sra $v0,$v0,31"),
              instruction(0x800B7800,"jr $ra"),
              instruction(0x800B7804,"subu $v0,$v1,$v0")))
            if target==0x800B7760:
                direct_ok=(exact(0x800B7780,"lhu",rt=3,rs=2,simm=0x20) and
                  exact(0x800B7788,"srl",rd=3,rt=3,sh=7) and
                  exact(0x800B778C,"andi",rs=3,rt=3,imm=0x1E) and
                  exact(0x800B7790,"addu",rd=2,rs=2,rt=3) and
                  exact(0x800B7794,"lhu",rt=2,rs=2,simm=0x10))
                if direct_ok:
                    expression="U16(record+0x10+((U16(record+0x20)>>7)&0x1E))"
                    input_reg="RECORD_MEMORY"
                    formula_status="TERBUKTI_BYTE"
            elif target==0x800B77A0:
                scale12=all((
                  instruction(0x800B77DC,"sll $v0,$v1,1"),
                  instruction(0x800B77E0,"addu $v0,$v0,$v1"),
                  instruction(0x800B77E4,"sll $v0,$v0,2")))
                if scale12 and common_div10:
                    expression="signed_trunc((12*V1)/10)"
                    input_reg="$v1"
                    formula_status="TERBUKTI_BYTE_SEQUENCE"
            elif target==0x800B7808:
                scale15=all((
                  instruction(0x800B7844,"sll $v1,$v0,4"),
                  instruction(0x800B7848,"j 0x800B77E8"),
                  instruction(0x800B784C,"subu $v0,$v1,$v0")))
                if scale15 and common_div10:
                    expression="signed_trunc((15*V0)/10)"
                    input_reg="$v0"
                    formula_status="TERBUKTI_BYTE_SEQUENCE"
            elif target==0x800B7850:
                scale18=all((
                  instruction(0x800B788C,"sll $v0,$v1,3"),
                  instruction(0x800B7890,"addu $v0,$v0,$v1"),
                  instruction(0x800B7894,"j 0x800B77E8"),
                  instruction(0x800B7898,"sll $v0,$v0,1")))
                if scale18 and common_div10:
                    expression="signed_trunc((18*V1)/10)"
                    input_reg="$v1"
                    formula_status="TERBUKTI_BYTE_SEQUENCE"
            elif target==0x800B789C:
                double_ok=(instruction(0x800B78D8,"sll $v0,$v0,1") and
                           instruction(0x800B78DC,"jr $ra"))
                if double_ok:
                    expression="2*V0"
                    input_reg="$v0"
                    formula_status="TERBUKTI_BYTE_SEQUENCE"
            jumptable_rows.append({"selector_value":selector,"table_entry_pc":f"0x{dispatch_addr+selector*4:08X}",
              "file_offset":f"0x{pos:08X}","bytes_4B":" ".join(f"{v:02X}" for v in raw),
              "jump_target_pc":f"0x{target:08X}","reader_site_pc":reader_site,
              "input_register":input_reg,"expression_candidate":expression,
              "formula_status":formula_status,"operation_sequence":sequence})
    exprs=[]
    for row in jumptable_rows:
        exprs.append({"site_id":row["selector_value"],"reader_site":row["reader_site_pc"],
          "expression_candidate":row["expression_candidate"],
          "multiplier_candidates":"TIDAK TAHU" if row["expression_candidate"]=="TIDAK TAHU" else row["expression_candidate"],
          "divisor_candidates":"TIDAK TAHU","jump_0x800B77E8":row["jump_target_pc"],
          "return_v0":row["formula_status"]})
    defs_rows=[]
    for bb,nn,pp,oo,ii,ss in regions: defs_rows.extend(scan_region(bb,nn,pp,oo)[2])
    out=a.out_dir;out.mkdir(parents=True,exist_ok=True)
    entry_rows=[];selector_rows=[];r=rmap["ENTRY1"];ii=r[4];ss=r[5]
    for target in sorted(targets):
        ix=(target-r[2])//4
        if 0<=ix<len(ii):
            st,en=function_span(ii,ss,ix);count=sum(1 for x in callers if x["target_pc"]==f"0x{target:08X}")
            selectors=sorted({reg(k) for q in range(st,en) if ii[q]["mn"] in ("beq","bne","blez","bgtz","bltz","bgez") for k in ii[q]["reads"] if 4<=k<=7})
            entry_rows.append({"entry_pc":f"0x{target:08X}","nearest_function_start":f"0x{r[2]+4*st:08X}",
              "function_end":f"0x{r[2]+4*en:08X}","is_prologue":str(st==ix and ix in ss).upper(),
              "direct_caller_count":count,"selector_registers":";".join(selectors) or "TIDAK TAHU"})
            for q in range(st,en):
                d=ii[q]
                if d["mn"] in ("beq","bne","blez","bgtz","bltz","bgez","slti","sltiu"):
                    regs_used=sorted({reg(k) for k in d["reads"] if 4<=k<=7})
                    if regs_used:
                        raw=r[0][q*4:q*4+4]
                        selector_rows.append({"region":"ENTRY1","entry_pc":f"0x{target:08X}",
                          "pc":f"0x{r[2]+4*q:08X}","file_offset":f"0x{r[3]+4*q:08X}",
                          "bytes_4B":" ".join(f"{v:02X}" for v in raw),"instruction":d["text"],
                          "kind":"ARGUMENT_BRANCH_OR_COMPARE","selector_register_candidate":";".join(regs_used),
                          "target_pc":f"0x{d['target']:08X}" if d["target"] is not None else "",
                          "immediate_candidate":f"0x{d['imm']:04X}" if d["mn"] in ("slti","sltiu") else "TIDAK ADA"})
                if d["mn"]=="jr" and d["rs"]!=31:
                    for p in range(max(st,q-12),q+1):
                        raw=r[0][p*4:p*4+4];dd=ii[p]
                        selector_rows.append({"region":"ENTRY1","entry_pc":f"0x{target:08X}",
                          "pc":f"0x{r[2]+4*p:08X}","file_offset":f"0x{r[3]+4*p:08X}",
                          "bytes_4B":" ".join(f"{v:02X}" for v in raw),"instruction":dd["text"],
                          "kind":"INDIRECT_JUMP_CONTEXT","selector_register_candidate":reg(d["rs"]),
                          "target_pc":"","immediate_candidate":"TIDAK TAHU"})
    write_tsv(out/"UP0_FUNCTION_ENTRY_POINTS.tsv",["entry_pc","nearest_function_start","function_end","is_prologue","direct_caller_count","selector_registers"],entry_rows)
    write_tsv(out/"UP0_SELECTOR_BRANCHES.tsv",["region","entry_pc","pc","file_offset","bytes_4B","instruction","kind","selector_register_candidate","target_pc","immediate_candidate"],selector_rows)
    validation=[]; unique={}
    def addv(region,pc,off,rawhex,instr,source):unique[(region,pc)]=(region,pc,off,rawhex,instr,source)
    for x in disasm:addv(x["region"],x["pc"],x["file_offset"],x["bytes_4B"],x["instruction"],"FUNCTION")
    for x in fwd:addv(x["region"],x["trace_pc"],x["file_offset"],x["bytes_4B"],x["instruction"],"FORWARD")
    for x in callers:addv(x["region"],x["pc"],x["file_offset"],x["bytes_4B"],x["instruction"],"CALLER")
    for x in writers:addv(x["region"],x["pc"],x["file_offset"],x["bytes_4B"],x["instruction"],"WRITER")
    for x in selector_rows:addv(x["region"],x["pc"],x["file_offset"],x["bytes_4B"],x["instruction"],"SELECTOR_BRANCH")
    for x in defs_rows:addv(x["region"],x["pc"],x["file_offset"],x["bytes_4B"],x["instruction"],"LH_LHU_DEFCHAIN")
    for region,pc,off,rawhex,instr,source in unique.values():
        raw=bytes.fromhex(rawhex);pi=int(pc,16);prod=decode(raw,pi);ind=independent_decode(raw,pi)
        ok=(prod["mn"]==ind["mn"] and prod["target"]==ind["target"] and prod["text"]==ind["text"] and instr==ind["text"])
        validation.append({"source":source,"region":region,"pc":pc,"file_offset":off,
          "bytes_4B":rawhex,"instruction":instr,"independent_instruction":ind["text"],
          "independent_control_target":f"0x{ind['target']:08X}" if ind["target"] is not None else "",
          "match":"YES" if ok else "NO"})
    write_tsv(out/"UP0_FORWARD_7_SITES.tsv",FWD+["trace_pc","tainted_after"],fwd)
    write_tsv(out/"UP0_FORWARD_SUMMARY.tsv",["site_id","pc","status","decoded_instructions","terminal_reason","destinations","return_v0"],fsum)
    write_tsv(out/"UP0_FORWARD_CALLS.tsv",["site_id","site_pc","call_pc","target_pc","tainted_arguments"],fcalls)
    write_tsv(out/"UP0_READER_FUNCTION_DISASSEMBLY.tsv",["region","pc","file_offset","bytes_4B","instruction","function_boundary"],disasm)
    write_tsv(out/"UP0_CALLERS.tsv",["region","pc","file_offset","bytes_4B","instruction","call_kind","target_pc","caller_function_start","setup_a0","setup_a1","setup_a2","setup_a3","setup_status","v0_after_return"],callers)
    write_tsv(out/"UP0_POINTER_LITERALS.tsv",["region","file_offset","pc_if_code","literal_value","target_class"],literals)
    write_tsv(out/"UP0_RECORD_WRITERS.tsv",["region","pc","file_offset","bytes_4B","instruction","base_register","data_register","function_start","basis_class","basis_detail","bits_8_11_written"],writers)
    write_tsv(out/"UP0_RMW_U16_20.tsv",["region","load_pc","mask_ops","store_pc","store_instruction","mask_immediates","basis_class","bits_8_11_written"],rmw)
    write_tsv(out/"UP0_SITE_BASES_2_SITES.tsv",["site_pc","function_start","caller_pc","caller_function_start","base_register","basis_status","basis_class","def_chain","setup_a0","setup_a1","setup_a2","setup_a3","reason"],sitebases)
    write_tsv(out/"UP0_CASE_MULTIPLIERS.tsv",["site_id","reader_site","expression_candidate","multiplier_candidates","divisor_candidates","jump_0x800B77E8","return_v0"],exprs)
    write_tsv(out/"UP0_SELECTOR_JUMPTABLE.tsv",["selector_value","table_entry_pc","file_offset","bytes_4B","jump_target_pc","reader_site_pc","input_register","expression_candidate","formula_status","operation_sequence"],jumptable_rows)
    write_tsv(out/"UP0_DECODE_VALIDATION.tsv",["source","region","pc","file_offset","bytes_4B","instruction","independent_instruction","independent_control_target","match"],validation)
    write_tsv(out/"UP0_LH_LHU_DEFCHAIN.tsv",DEF,defs_rows)

    mismatch=sum(x["match"]!="YES" for x in validation)
    summary=["UP0_BYTE_VERIFIED_READER_TRACER_AND_WRITER_AUDIT",
      "STATUS="+("TUNTAS" if mismatch==0 and len(fsum)==7 and dispatch_ok and len(jumptable_rows)==5 else "SEBAGIAN"),
      "EVIDENCE=K4 maksimum; byte EXE dan Entry 1; statis","K5=NOT_APPLICABLE_STATIC_ONLY",
      f"EXE_SHA256={digest(exe)}",f"DATA_BIN_SHA256={digest(data)}",f"ENTRY1_SHA256={digest(e1)}",
      "ENTRY1_MAPPING=0x10BB000+(PC-0x800AD450)",f"FORWARD_SITES_PROCESSED={len(fsum)}",
      f"FORWARD_SITES_TRACED={sum(1 for x in fsum if x['status']=='TERTELUSURI')}",
      f"FUNCTION_DISASSEMBLY_ROWS={len(disasm)}",f"CALLER_ROWS={len(callers)}",
      f"POINTER_LITERAL_ROWS={len(literals)}",f"RECORD_WRITER_ROWS={len(writers)}",
      f"RMW_U16_PLUS_0x20_ROWS={len(rmw)}",f"SITE_BASE_ROWS={len(sitebases)}",
      f"SITE_BASE_TIDAK_TAHU={sum(1 for x in sitebases if x['basis_status']!='TERBUKTI')}",
      f"DISPATCH_TABLE_BYTE_VALIDATED={'YES' if dispatch_ok else 'NO'}",
      f"SELECTOR_JUMPTABLE_ROWS={len(jumptable_rows)}",
      f"SELECTOR_FORMULAS_BYTE_VALIDATED={sum(1 for x in jumptable_rows if x['formula_status'] in ('TERBUKTI_BYTE','TERBUKTI_BYTE_SEQUENCE'))}",
      f"SELECTOR_FORMULAS_TIDAK_TAHU={sum(1 for x in jumptable_rows if x['formula_status'].startswith('TIDAK_TAHU'))}",
      f"INDEPENDENT_DECODE_ROWS={len(validation)}",f"INDEPENDENT_DECODE_MISMATCHES={mismatch}",
      "FIELD_GAMEPLAY_MEANING=TIDAK TAHU","NOTE=offset memori tidak diberi makna gameplay tanpa bukti"]
    (out/"UP0_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8");print("\n".join(summary),flush=True)
    return 0 if mismatch==0 and len(fsum)==7 and dispatch_ok and len(jumptable_rows)==5 else 2

def self_test_up0():
    pc=0x80010000;word=(5<<26)|(8<<21)|(9<<16)|3;raw=word.to_bytes(4,"little")
    dec=independent_decode(raw,pc);assert dec["mn"]=="bne" and dec["target"]==pc+16
    def rw(rs,rt,rd,fn):return ((rs<<21)|(rt<<16)|(rd<<11)|fn).to_bytes(4,"little")
    def iw(op,rs,rt,imm):return ((op<<26)|(rs<<21)|(rt<<16)|(imm&0xffff)).to_bytes(4,"little")
    def trace(words):
        blob=b"".join(words);ii=[decode(blob[z:z+4],pc+4*(z//4)) for z in range(0,len(blob),4)]
        return forward_graph(1,pc,ii,blob,"TEST",pc,0)[1]
    s=trace([iw(0x25,4,2,0x10),rw(2,9,0,25),rw(0,0,2,18),rw(31,0,0,8),bytes(4)])
    assert s["return_v0"]=="RETURN_V0_TAINTED",s
    # A later untainted multiply overwrites HI/LO; mflo must then clear the old taint.
    s=trace([iw(0x25,4,2,0x10),rw(2,9,0,25),rw(10,11,0,25),rw(0,0,2,18),rw(31,0,0,8),bytes(4)])
    assert s["return_v0"]=="RETURN_V0_UNTAINTED",s
    call=((3<<26)|(((pc+0x40)>>2)&0x3ffffff)).to_bytes(4,"little")
    s=trace([iw(0x25,4,2,0x10),call,bytes(4),rw(31,0,0,8),bytes(4)])
    assert s["return_v0"]=="RETURN_V0_UNTAINTED",s
    print("UP0_SELF_TEST=PASS independent decoder, delay slot, HI/LO, jr-ra and jal clobber")

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--exe",type=Path);ap.add_argument("--data-bin",type=Path)
    ap.add_argument("--out-dir",type=Path);ap.add_argument("--self-test",action="store_true")
    a=ap.parse_args()
    if a.self_test:self_test_up0();return 0
    if not all((a.exe,a.data_bin,a.out_dir)):ap.error("--exe --data-bin --out-dir required")
    return main_up0(a)

if __name__=="__main__":
    raise SystemExit(main())
