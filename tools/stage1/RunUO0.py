#!/usr/bin/env python3
"""UO0: bounded, byte-verified MIPS census and register provenance for PS1 fields."""
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

def provenance(ins: list[dict], start: int, end: int, base_reg: int) -> tuple[str,str,str,list[int]]:
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
            val=idx(f"ARG_{REGS[r]}",1) if r in (4,5,6,7) else None
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
                elif a and a[0]=="idx" and d["mn"] in ("addiu","addi") and d["simm"]==0:
                    val=a
        elif d["mn"] == "lw":
            _,_,disp,rs,_=d["mem"]
            a=resolve(rs,di,depth+1)
            if a and a[0]=="const" and ((a[1]+disp)&0xFFFFFFFF)==RAM_POINTER:
                val=("pointer",RAM_POINTER,"P_FROM_8013EA84")
            elif d["mn"]=="lw":
                val=idx(f"LOAD_RESULT_REG_{REGS[r]}",1)
        elif d["mn"] in ("sll","srl","sra"):
            a=resolve(d["rt"],di,depth+1)
            if d["mn"]=="sll" and a and a[0]=="idx":
                val=idx(a[2],a[1]*(1<<d["sh"]))
        elif d["mn"] in ("addu","add","or"):
            a=resolve(d["rs"],di,depth+1)
            b=resolve(d["rt"],di,depth+1)
            if d["mn"]=="or" and a and a[0]=="const" and a[1]==0: val=b
            elif d["mn"]=="or" and b and b[0]=="const" and b[1]==0: val=a
            elif a and b and a[0]=="idx" and b[0]=="idx" and a[2]==b[2]:
                val=idx(a[2],a[1]+b[1])
            elif a and a[0]=="pointer" and b and b[0]=="idx":
                val=("record" if b[1]==STRIDE else "lvbase" if b[1]==2 else "pointer_offset",b[1],b[2])
            elif b and b[0]=="pointer" and a and a[0]=="idx":
                val=("record" if a[1]==STRIDE else "lvbase" if a[1]==2 else "pointer_offset",a[1],a[2])
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
        elif i-func>128: reason.append("LEBIH_DARI_128_INSTRUKSI_DARI_AWAL_FUNGSI")
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
        stop=min(len(ins),i+64)
        end_reason="BATAS_64_INSTRUKSI"
        if start is not None:
            ret_end=next((x+1 for x in range(i,len(ins)) if ins[x]["mn"]=="jr" and ins[x]["rs"]==31),len(ins))
            next_start=next((x for x in starts if x>i),len(ins))
            func_end=min(ret_end,next_start)
            stop=min(stop,func_end)
            if stop==func_end: end_reason="AKHIR_FUNGSI_JR_RA"
        used=[]
        for j in range(i,stop):
            d=ins[j]; raw=blob[j*4:j*4+4]
            before=set(taint); used_regs=set(d["reads"]) & before
            cls="TIDAK_MENGGUNAKAN_NILAI"; detail=""
            if used_regs:
                if d["mn"]=="jal":
                    args=sorted(before & {4,5,6,7})
                    cls="ARGUMEN_JAL" if args else "JAL_TIDAK_MEMBAWA_ARGUMEN_TAINT"
                    detail=f"jal target=0x{d['target']:08X}; tainted_args="+",".join(reg(x) for x in args)
                elif d["mn"] in ("beq","bne","blez","bgtz","bltz","bgez","slt","sltu","slti","sltiu"):
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
            "status":"TERTELUSURI" if rows else "TAK TERSELESAIKAN",
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
    print("UO0_SELF_TEST=PASS branch targets, little-endian MIPS and lh/lhu")

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--exe",type=Path); ap.add_argument("--data-bin",type=Path)
    ap.add_argument("--out-dir",type=Path); ap.add_argument("--self-test",action="store_true")
    a=ap.parse_args()
    if a.self_test:
        self_test(); return 0
    if not all((a.exe,a.data_bin,a.out_dir)):
        ap.error("--exe --data-bin --out-dir required")
    exe=a.exe.read_bytes(); data=a.data_bin.read_bytes()
    if len(exe)!=EXE_SIZE or digest(exe)!=EXE_SHA: raise SystemExit("UO0_EXE_IDENTITY_MISMATCH")
    if len(data)!=DATA_SIZE or digest(data)!=DATA_SHA: raise SystemExit("UO0_DATA_BIN_IDENTITY_MISMATCH")
    e1=data[E1_OFF:E1_OFF+E1_SIZE]
    if len(e1)!=E1_SIZE or digest(e1)!=ENTRY1_SHA: raise SystemExit("UO0_ENTRY1_IDENTITY_MISMATCH")
    exeb=exe[EXE_OFF:]
    e_ins,e_starts,e_rows,e_br,e_val=scan_region(exeb,"EXE",EXE_PC,EXE_OFF)
    d_ins,d_starts,d_rows,d_br,d_val=scan_region(e1,"ENTRY1",E1_PC,E1_OFF)
    forward,forward_summaries=forward_sites(d_ins,d_starts,e1,"ENTRY1",E1_PC,E1_OFF)
    rows=e_rows+d_rows
    dropped_sp=sum("BASIS_SP" in r["reason"] for r in rows)
    dropped_odd=sum("DISPLACEMENT_GANJIL" in r["reason"] for r in rows)
    proven=sum(r["status"]=="TERBUKTI" for r in rows)
    unresolved=sum(r["status"]=="TAK TERSELESAIKAN" for r in rows)
    excluded=sum(r["status"]=="DIKECUALIKAN" for r in rows)
    both_excluded=sum("BASIS_SP" in r["reason"] and "DISPLACEMENT_GANJIL" in r["reason"] for r in rows)
    counts=[{"class":"TOTAL_LH_LHU_DISP_0E_1E","count":len(rows)},
      {"class":"DIKECUALIKAN_SP_BASIS","count":dropped_sp},
      {"class":"DIKECUALIKAN_DISPLACEMENT_GANJIL","count":dropped_odd},
      {"class":"DIKECUALIKAN_SP_DAN_GANJIL","count":both_excluded},
      {"class":"TERBUKTI_BASIS_EA84","count":proven},
      {"class":"TAK_TERSELESAIKAN","count":unresolved},
      {"class":"DIKECUALIKAN_UNIK","count":excluded},
      {"class":"BRANCH_BEQ_BNE","count":len(e_br)+len(d_br)},
      {"class":"FORWARD_7_SITES_ROWS","count":len(forward)}]
    out=a.out_dir; out.mkdir(parents=True,exist_ok=True)
    write_tsv(out/"UO0_LH_LHU_DEFCHAIN.tsv",DEF,rows)
    write_tsv(out/"UO0_FORWARD_7_SITES.tsv",FWD,forward)
    write_tsv(out/"UO0_FORWARD_SUMMARY.tsv",["site_id","pc","status","decoded_instructions","terminal_reason","destinations","reason"],forward_summaries)
    write_tsv(out/"UO0_BEQ_BNE_TARGETS.tsv",BRANCHES,e_br+d_br)
    write_tsv(out/"UO0_DECODE_VALIDATION.tsv",VALIDATION,e_val+d_val)
    write_tsv(out/"UO0_CANDIDATE_COUNTS.tsv",COUNTS,counts)
    mismatch=sum(x["match"]!="YES" for x in e_val+d_val)
    summary=[
      "UO0_STATIC_DISASSEMBLY_AND_PROVENANCE",
      "STATUS=TUNTAS" if mismatch==0 else "STATUS=SEBAGIAN",
      "EVIDENCE=K4 maksimum; byte EXE/Entry1 dan decoder MIPS statis",
      "K5=NOT_APPLICABLE_STATIC_ONLY",
      f"EXE_SHA256={digest(exe)}",f"DATA_BIN_SHA256={digest(data)}",f"ENTRY1_SHA256={digest(e1)}",
      "EXE_MAPPING=0x800+(PC-0x80010000)",
      "ENTRY1_MAPPING=0x10BB000+(PC-0x800AD450)",
      f"LH_LHU_DISPLACEMENT_0E_1E_TOTAL={len(rows)}",
      f"EXCLUDED_SP_BASE_ROWS={dropped_sp}",
      f"EXCLUDED_ODD_DISPLACEMENT_ROWS={dropped_odd}",
      f"EXCLUDED_SP_AND_ODD_OVERLAP_ROWS={both_excluded}",
      f"UNIQUE_EXCLUDED_ROWS={excluded}",
      f"PROVEN_EA84_BASE_ROWS={proven}",
      f"UNRESOLVED_ROWS={unresolved}",
      f"BEQ_BNE_DECODED_WITH_TARGET={len(e_br)+len(d_br)}",
      f"DECODE_VALIDATION_ROWS={len(e_val)+len(d_val)}",
      f"DECODE_VALIDATION_MISMATCHES={mismatch}",
      f"FORWARD_7_SITES_ROWS={len(forward)}",
      "FIELD_MEANING=TIDAK TAHU",
      "EMULATOR_USED=NO",
      "NOTE=TERBUKTI hanya untuk rantai register basis; tidak membuktikan makna gameplay",
    ]
    (out/"UO0_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary),flush=True)
    return 0 if mismatch==0 else 2

if __name__=="__main__":
    raise SystemExit(main())
