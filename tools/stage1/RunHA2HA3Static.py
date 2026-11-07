#!/usr/bin/env python3
"""HA2/HA3 static audit for SLPS-03553. No emulator and no binary outputs."""
from __future__ import annotations
import argparse, csv, hashlib, re, struct
from collections import defaultdict
from pathlib import Path
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_BASE, ENTRY_BASE = 0x80010000, 0x800AD450
EXE_FILE_BASE, ENTRY_FILE_BASE = 0x800, 0x10BB000
EXE_SHA = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
ENTRY_SHA = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
ENTRY_SIZE = 596412
TABLE_VA = 0x80055CF4
TARGETS = {
    "FUN_800154D4": 0x800154D4,
    "FUN_8001552C": 0x8001552C,
    "FUN_800F2A9C": 0x800F2A9C,
    "FUN_800DC2E0": 0x800DC2E0,
    "FUN_800FAAC8": 0x800FAAC8,
    "FUN_800D15A8": 0x800D15A8,
}
REG = ["$zero","$at","$v0","$v1","$a0","$a1","$a2","$a3",
       "$t0","$t1","$t2","$t3","$t4","$t5","$t6","$t7",
       "$s0","$s1","$s2","$s3","$s4","$s5","$s6","$s7",
       "$t8","$t9","$k0","$k1","$gp","$sp","$fp","$ra"]
LOADS={"lb","lh","lw","lbu","lhu","lwl","lwr"}
STORES={"sb","sh","sw","swl","swr"}
MEM=LOADS|STORES

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
def hx(data: bytes) -> str:
    return " ".join(f"{b:02X}" for b in data)
def h32(value: int) -> str:
    return f"0x{value & 0xffffffff:08X}"
def write_tsv(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)
def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
def file_offset(pc: int, image: str) -> int:
    if image=="EXE":
        return EXE_FILE_BASE + (pc-EXE_BASE)
    if image=="ENTRY1":
        return ENTRY_FILE_BASE + (pc-ENTRY_BASE)
    raise ValueError(image)

def decode_image(data: bytes, base: int, image: str, md):
    out={}
    for off in range(0, len(data)-3, 4):
        pc=base+off
        raw=data[off:off+4]
        x=next(md.disasm(raw, pc, count=1), None)
        word=int.from_bytes(raw, "little")
        op=word>>26
        row={
            "pc":pc, "off":off, "fileoff":file_offset(pc,image), "bytes":raw,
            "word":word, "mnemonic":x.mnemonic.lower() if x else ".word",
            "op_str":x.op_str if x else f"0x{word:08X}",
            "text":((x.mnemonic.lower()+" "+x.op_str).strip() if x else f".word 0x{word:08X}"),
            "op":op, "rs":(word>>21)&31, "rt":(word>>16)&31, "rd":(word>>11)&31,
            "sh":(word>>6)&31, "fn":word&63,
            "imm":((word&0xffff)^0x8000)-0x8000, "uimm":word&0xffff,
            "target":word&0x03ffffff, "image":image,
        }
        out[pc]=row
    return out

def dest_reg(i):
    op,fn=i["op"],i["fn"]
    if op==0:
        if fn in (8,): return None
        if fn==9: return 31
        if fn in (16,18,12,13,24,25,26,27): return None
        return i["rd"] or None
    if op in (2,4,5,6,7,1): return None
    if op==3: return 31
    if op in (8,9,10,11,12,13,14,15,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,
              0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x3A,0x3B,0x3C,0x3D,0x3E,0x3F):
        return i["rt"] or None
    return None

def last_def(code, reg, before, lo=None, max_back=96):
    floor=max(lo if lo is not None else min(code), before-max_back*4)
    for pc in range(before-4, floor-1, -4):
        i=code.get(pc)
        if i and dest_reg(i)==reg:
            return i
        if i and i["mnemonic"] in ("jal","jalr"):
            # Caller-saved registers are clobbered; stop the local slice.
            if reg not in (16,17,18,19,20,21,22,23,28,29,30,31):
                return None
    return None

def const_reg(code, reg, before, lo=None, depth=0, seen=None):
    if depth>12: return None
    if seen is None: seen=set()
    key=(reg,before)
    if key in seen: return None
    seen.add(key)
    d=last_def(code,reg,before,lo)
    if d is None: return 0 if reg==0 else None
    op,rs,rt,fn=d["op"],d["rs"],d["rt"],d["fn"]
    if op==0x0f: return (d["uimm"]<<16)&0xffffffff
    if op in (8,9):
        x=const_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
        return ((x+d["imm"])&0xffffffff) if x is not None else None
    if op==0x0d:
        x=const_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
        return ((x|d["uimm"])&0xffffffff) if x is not None else None
    if op==0:
        if fn==0:
            x=const_reg(code,rt,d["pc"],lo,depth+1,seen.copy())
            return ((x<<d["sh"])&0xffffffff) if x is not None else None
        if fn==2:
            x=const_reg(code,rt,d["pc"],lo,depth+1,seen.copy())
            return (x>>d["sh"]) if x is not None else None
        if fn in (0x21,0x23,0x24,0x25,0x26,0x27):
            x=const_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
            y=const_reg(code,rt,d["pc"],lo,depth+1,seen.copy())
            if x is None or y is None: return None
            if fn==0x21: return (x+y)&0xffffffff
            if fn==0x23: return (x-y)&0xffffffff
            if fn==0x24: return x&y
            if fn==0x25: return x|y
            if fn==0x26: return x^y
            if fn==0x27: return (~(x|y))&0xffffffff
    return None

def effective_addr(code,i,lo=None):
    base=const_reg(code,i["rs"],i["pc"],lo)
    return ((base+i["imm"])&0xffffffff) if base is not None else None

def trace_reg(code,reg,before,lo=None,depth=0,seen=None):
    if reg==0: return "$zero"
    if depth>5: return "DEPTH_LIMIT"
    if seen is None: seen=set()
    key=(reg,before)
    if key in seen: return "CYCLE"
    seen.add(key)
    d=last_def(code,reg,before,lo)
    if d is None: return f"{REG[reg]}=INPUT_OR_DYNAMIC"
    m=d["mnemonic"]
    head=f"{h32(d['pc'])} {d['text']}"
    op,rs,rt,fn=d["op"],d["rs"],d["rt"],d["fn"]
    if op in (8,9,10,11,12,13,14):
        return head+" <- "+trace_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
    if op in (0x20,0x21,0x23,0x24,0x25,0x27):
        ea=effective_addr(code,d,lo)
        suffix=f" [EA={h32(ea)}]" if ea is not None else ""
        return head+suffix+"; base <- "+trace_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
    if op==0 and fn in (0,2,3):
        return head+" <- "+trace_reg(code,rt,d["pc"],lo,depth+1,seen.copy())
    if op==0 and fn in (0x21,0x23,0x24,0x25,0x26,0x27):
        return head+" <- "+trace_reg(code,rs,d["pc"],lo,depth+1,seen.copy())+" ; "+trace_reg(code,rt,d["pc"],lo,depth+1,seen.copy())
    return head

def is_manager_pointer(code, reg, before, lo=None, depth=0, seen=None):
    if depth>8: return False
    if seen is None: seen=set()
    if (reg,before) in seen: return False
    seen.add((reg,before))
    d=last_def(code,reg,before,lo)
    if d is None: return False
    if d["mnemonic"]=="lw" and effective_addr(code,d,lo)==0x8013EA74:
        return True
    if d["op"]==0 and d["fn"]==0x21:
        return (is_manager_pointer(code,d["rs"],d["pc"],lo,depth+1,seen.copy()) or
                is_manager_pointer(code,d["rt"],d["pc"],lo,depth+1,seen.copy()))
    if d["op"] in (8,9) and d["imm"]==0:
        return is_manager_pointer(code,d["rs"],d["pc"],lo,depth+1,seen.copy())
    return False

def manager_index(code, base_reg, before, lo=None):
    d=last_def(code,base_reg,before,lo)
    if d is None: return ("TIDAK TAHU","TIDAK TAHU")
    candidates=[]
    if d["op"]==0 and d["fn"]==0x21:
        for r in (d["rs"],d["rt"]):
            if is_manager_pointer(code,r,d["pc"],lo):
                other=d["rt"] if r==d["rs"] else d["rs"]
                candidates.append(other)
    elif d["op"] in (8,9) and d["imm"]==0 and is_manager_pointer(code,d["rs"],d["pc"],lo):
        candidates.append(0)
    for scaled in candidates:
        if scaled==0:
            return ("0","manager pointer direct; no index term in this local addiu")
        sd=last_def(code,scaled,d["pc"],lo)
        if sd and sd["op"]==0 and sd["fn"]==0 and sd["sh"]==1:
            idxreg=sd["rt"]
            return (REG[idxreg],trace_reg(code,idxreg,sd["pc"],lo))
        return (REG[scaled],trace_reg(code,scaled,d["pc"],lo))
    return ("TIDAK TAHU",trace_reg(code,base_reg,before,lo))

def parse_ghidra_functions(path: Path):
    text=path.read_text(encoding="utf-8",errors="replace") if path.exists() else ""
    funcs={}
    marker=re.compile(r"=== TARGET (?:0x)?([0-9A-Fa-f]{8}) ===")
    matches=list(marker.finditer(text))
    for n,m in enumerate(matches):
        start=m.start()
        end=matches[n+1].start() if n+1<len(matches) else len(text)
        block=text[start:end]
        target=int(m.group(1),16)
        fentry_match=re.search(r"function_entry=(?:0x)?([0-9A-Fa-f]{8})",block)
        fentry=int(fentry_match.group(1),16) if fentry_match else target
        rawpart=""
        rawm=re.search(r"--- RAW_FUNCTION_BODY_BEGIN ---\s*(.*?)\s*--- RAW_FUNCTION_BODY_END ---",block,re.S)
        if rawm: rawpart=rawm.group(1)
        rawrows=[]
        for line in rawpart.splitlines():
            mm=re.search(r"(?:0x)?([0-9A-Fa-f]{8})\s+bytes=\[([0-9A-Fa-f ]+)\]\s+(.+)$",line.strip())
            if not mm: continue
            rawrows.append({"pc":int(mm.group(1),16),"bytes":bytes.fromhex(mm.group(2)),"ghidra":mm.group(3)})
        c_match=re.search(r"--- C_DECOMPILATION_BEGIN ---\s*(.*?)\s*--- C_DECOMPILATION_END ---",block,re.S)
        decomp=c_match.group(1).strip() if c_match else ""
        refs_match=re.search(r"--- REFERENCES_TO_FUNCTION_BEGIN ---\s*(.*?)\s*--- REFERENCES_TO_FUNCTION_END ---",block,re.S)
        refs=refs_match.group(1).strip() if refs_match else ""
        fname=re.search(r"function_name=(.+)",block)
        funcs[target]={"target":target,"entry":fentry,"block":block,"raw":rawrows,"decomp":decomp,
                       "refs":refs,"name":fname.group(1).strip() if fname else f"FUN_{target:08X}"}
    return funcs,text

def parse_return_expressions(decomp):
    return re.findall(r"\breturn\s+([^;]+);",decomp)

def rows_from_function(func,image,blob,base):
    rows=[]
    for r in func["raw"]:
        pc=r["pc"]; raw=r["bytes"]
        offset=file_offset(pc,image)
        if len(raw)!=4:
            continue
        x=next(md.disasm(raw,pc,count=1),None)
        text=(x.mnemonic.lower()+" "+x.op_str).strip() if x else ".word 0x"+raw[::-1].hex().upper()
        rows.append({"pc":h32(pc),"file_offset":f"0x{offset:X}","bytes":hx(raw),"instruksi":text,
                     "_pc":pc,"_bytes":raw})
    return rows

def split_instruction_rows(out,stem,rows,max_rows=16):
    rows=sorted(rows,key=lambda x:int(x["_pc"]))
    chunks=[];cur=[]
    for r in rows:
        if cur and (r["_pc"]!=cur[-1]["_pc"]+4 or len(cur)>=max_rows):
            chunks.append(cur);cur=[]
        cur.append(r)
    if cur: chunks.append(cur)
    for i,chunk in enumerate(chunks):
        clean=[{k:v for k,v in r.items() if not k.startswith("_")} for r in chunk]
        write_tsv(out/f"{stem}_{i:02d}.tsv",clean,["pc","file_offset","bytes","instruksi"])
    return len(chunks),sum(map(len,chunks))

def write_store_window(out,stem,code,pc0,pc1,image):
    base=ENTRY_BASE if image=="ENTRY1" else EXE_BASE
    end=pc1+4
    rows=[]
    for pc in range(pc0,end,4):
        i=code.get(pc)
        if not i: continue
        rows.append({"pc":h32(pc),"file_offset":f"0x{i['fileoff']:X}","bytes":hx(i["bytes"]),"instruksi":i["text"]})
    write_tsv(out/(stem+".tsv"),rows,["pc","file_offset","bytes","instruksi"])
    return len(rows)

def validate_instruction_tsvs(out):
    fields=["pc","file_offset","bytes","instruksi"]
    scanned=0
    files=0
    errors=[]
    for path in sorted(out.glob("*.tsv")):
        with path.open("r",encoding="utf-8",newline="") as f:
            reader=csv.DictReader(f,delimiter="\t")
            if reader.fieldnames!=fields:
                continue
            files+=1
            rows=list(reader)
        pcs=[]
        for line_no,row in enumerate(rows,2):
            scanned+=1
            try:
                pc=int(row["pc"],16)
                offset=int(row["file_offset"],16)
                image="ENTRY1" if pc>=ENTRY_BASE else "EXE"
                expected=file_offset(pc,image)
                raw=bytes.fromhex(row["bytes"])
                if offset!=expected:
                    errors.append(f"{path.name}:{line_no}: offset {offset:#x}, expected {expected:#x}")
                    continue
                if len(raw)!=4:
                    errors.append(f"{path.name}:{line_no}: instruction is {len(raw)} bytes")
                    continue
                decoded=next(md.disasm(raw,pc,count=1),None)
                text_value=(decoded.mnemonic.lower()+" "+decoded.op_str).strip() if decoded else ".word 0x"+raw[::-1].hex().upper()
                if text_value!=row["instruksi"]:
                    errors.append(f"{path.name}:{line_no}: decode {text_value!r}, recorded {row['instruksi']!r}")
                pcs.append(pc)
            except Exception as exc:
                errors.append(f"{path.name}:{line_no}: {type(exc).__name__}: {exc}")
        streak=0
        prior=None
        for pc in sorted(pcs):
            streak=streak+1 if prior is not None and pc==prior+4 else 1
            if streak>16:
                errors.append(f"{path.name}: contiguous run exceeds 16 instructions at {pc:#x}")
                break
            prior=pc
    report=[
        f"INSTRUCTION_TSV_FILES={files}",
        f"INSTRUCTION_ROWS_VALIDATED={scanned}",
        f"INVALID_ROWS={len(errors)}",
        "EXE_OFFSET_FORMULA=0x800+(PC-0x80010000)",
        "ENTRY1_OFFSET_FORMULA=0x10BB000+(PC-0x800AD450)",
        "MAX_CONTIGUOUS_INSTRUCTIONS_PER_EXCERPT=16",
    ]
    report.extend(errors[:100])
    write_text(out/"HA_TSV_VALIDATION_SUMMARY.txt","\n".join(report)+"\n")
    if errors:
        raise SystemExit("TSV_VALIDATION_FAILED="+str(len(errors)))
    return files,scanned

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--exe",type=Path,required=True)
    ap.add_argument("--entry1",type=Path,required=True)
    ap.add_argument("--ghidra-exe",type=Path,required=True)
    ap.add_argument("--ghidra-entry1",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    out=a.out;out.mkdir(parents=True,exist_ok=True)
    exe=a.exe.read_bytes();entry=a.entry1.read_bytes()
    if len(exe)!=385024 or sha(exe)!=EXE_SHA: raise SystemExit("EXE_IDENTITY_MISMATCH")
    if len(entry)!=ENTRY_SIZE or sha(entry)!=ENTRY_SHA: raise SystemExit("ENTRY1_IDENTITY_MISMATCH")
    global md
    md=Cs(CS_ARCH_MIPS,CS_MODE_MIPS32|CS_MODE_LITTLE_ENDIAN);md.detail=True
    ex=decode_image(exe,EXE_BASE,"EXE",md)
    en=decode_image(entry,ENTRY_BASE,"ENTRY1",md)
    exe_funcs,exe_text=parse_ghidra_functions(a.ghidra_exe)
    ent_funcs,ent_text=parse_ghidra_functions(a.ghidra_entry1)

    # HA1: corrected helper excerpt split at 16 instructions, plus exact NEG U rows and store windows.
    helper=exe_funcs.get(0x8001552C) or exe_funcs.get(0x800154D4)
    helper_rows=rows_from_function(helper,"EXE",exe,EXE_BASE) if helper else []
    helper_rows=[r for r in helper_rows if 0x8001552C<=int(r["pc"],16)<=0x80015574]
    helper_chunks,helper_n=split_instruction_rows(out,"HA1_HELPER_8001552C",helper_rows,16)
    negrows=[]
    for pc in (0x800F2E0C,0x800F2E64):
        i=en.get(pc)
        if i:
            negrows.append({"pc":h32(pc),"file_offset":f"0x{file_offset(pc,'ENTRY1'):X}",
                            "bytes":hx(i["bytes"]),"instruksi":i["text"]})
    write_tsv(out/"HA1_NEGU_ROWS.tsv",negrows,["pc","file_offset","bytes","instruksi"])
    window_n=0
    for stem,p0,p1 in [
        ("HA1_STORE_F2CF8_WINDOW",0x800F2CE4,0x800F2CF8),
        ("HA1_STORE_F2E38_WINDOW",0x800F2E04,0x800F2E38),
        ("HA1_STORE_F2E68_WINDOW",0x800F2E50,0x800F2E68),
    ]:
        window_n+=write_store_window(out,stem,en,p0,p1,"ENTRY1")

    # Function-body excerpts: each individual TSV contains at most 16 contiguous instructions.
    chunk_counts={}
    for key,funcs,image,blob,code in [
        ("HA2_FUN_800154D4",exe_funcs,"EXE",exe,ex),
        ("HA2_FUN_8001552C",exe_funcs,"EXE",exe,ex),
        ("HA2_FUN_800F2A9C",ent_funcs,"ENTRY1",entry,en),
        ("HA3_FUN_800DC2E0",ent_funcs,"ENTRY1",entry,en),
        ("HA3_FUN_800FAAC8",ent_funcs,"ENTRY1",entry,en),
        ("HA3_FUN_800D15A8",ent_funcs,"ENTRY1",entry,en),
    ]:
        pc=TARGETS[key.replace("HA2_","").replace("HA3_","")]
        f=funcs.get(pc)
        if f and f["raw"]:
            rr=rows_from_function(f,image,blob,EXE_BASE if image=="EXE" else ENTRY_BASE)
            nrows=sum(1 for r in rr)
            n_chunks,_=split_instruction_rows(out,key,rr,16)
            chunk_counts[key]=(nrows,n_chunks)
        else:
            chunk_counts[key]=(0,0)

    # Helper body, Ghidra return expression, and table entries.
    hf=exe_funcs.get(0x800154D4)
    helper_lines=[
        "HA2_HELPER_FUNCTION=FUN_800154D4",
        "GHIDRA_FUNCTION_FOUND="+("YES" if hf else "NO"),
        "RAW_INSTRUCTION_COUNT="+str(len(hf["raw"]) if hf else 0),
        "DECOMPILE_AVAILABLE="+("YES" if hf and hf["decomp"] else "NO"),
    ]
    helper_returns=parse_return_expressions(hf["decomp"]) if hf else []
    helper_lines.append("DECOMPILED_RETURN_EXPRESSIONS="+(" | ".join(helper_returns) if helper_returns else "TIDAK TAHU"))
    bound=None
    if helper_returns:
        vals=[]
        for expr in helper_returns:
            s=expr.strip().strip("()")
            if re.fullmatch(r"(?:0x[0-9a-fA-F]+|[0-9]+)[uUlL]*",s):
                vals.append(int(re.match(r"(0x[0-9a-fA-F]+|[0-9]+)",s).group(1),0))
            else:
                vals.append(None)
        if vals and all(v is not None and v==vals[0] for v in vals):
            bound=vals[0]
    helper_lines.append("BOUND="+(str(bound) if bound is not None else "TIDAK TAHU"))
    table_rows=[]
    table_offset=file_offset(TABLE_VA,"EXE")
    helper_lines.append(f"TABLE_VA={h32(TABLE_VA)}")
    helper_lines.append(f"TABLE_FILE_OFFSET=0x{table_offset:X}")
    helper_lines.append("TABLE_STRIDE=0x10")
    helper_lines.append("TABLE_VALUE_FIELD_OFFSET=+0x8")
    if bound is not None and 0<=bound<=0x10000 and table_offset+bound*16<=len(exe):
        for idx in range(bound):
            addr=TABLE_VA+idx*0x10
            pos=table_offset+idx*0x10
            raw=exe[pos+8:pos+12]
            value=int.from_bytes(raw,"little")
            table_rows.append({"index":idx,"alamat":h32(addr+8),"file_offset":f"0x{pos+8:X}",
                               "bytes":hx(raw),"u32":value})
        for ci in range(0,len(table_rows),16):
            write_tsv(out/f"HA2_TABLE_VALUES_{ci//16:02d}.tsv",table_rows[ci:ci+16],
                      ["index","alamat","file_offset","bytes","u32"])
        if table_rows:
            vals=[r["u32"] for r in table_rows]
            ratios=[]
            for x,y in zip(vals,vals[1:]):
                ratios.append("UNDEFINED_ZERO_DENOMINATOR" if x==0 else f"{y/x:.9g}")
            numeric=[x for x in ratios if not x.startswith("UNDEFINED")]
            helper_lines.extend([
                "TABLE_ROWS="+str(len(table_rows)),
                "TABLE_MIN="+str(min(vals)),
                "TABLE_MAX="+str(max(vals)),
                "SEQUENTIAL_RATIO_MIN="+(str(min(map(float,numeric))) if numeric else "TIDAK TERHITUNG"),
                "SEQUENTIAL_RATIO_MAX="+(str(max(map(float,numeric))) if numeric else "TIDAK TERHITUNG"),
                "SEQUENTIAL_RATIO_UNDEFINED_COUNT="+str(sum(x.startswith("UNDEFINED") for x in ratios)),
            ])
        else:
            helper_lines.append("TABLE_ROWS=0")
    else:
        helper_lines.append("TABLE_ROWS=TIDAK DIHASILKAN; bound tidak konstan atau di luar batas tervalidasi")
    write_text(out/"HA2_HELPER_TABLE_SUMMARY.txt","\n".join(helper_lines)+"\n")

    # F2A9C C-decomp, refs, and return expressions.
    f2=ent_funcs.get(0x800F2A9C)
    rets=parse_return_expressions(f2["decomp"]) if f2 else []
    return_rows=[]
    if f2:
        void_function=bool(re.search(r"\bvoid\s+"+re.escape(f2["name"])+r"\s*\(",f2["decomp"]))
        epilogs=sum(1 for r in f2["raw"] if re.search(r"\bjr\s+\$?ra\b",r["ghidra"],re.I))
        bare_returns=len(re.findall(r"\breturn\s*;",f2["decomp"])) if void_function else 0
        if bare_returns:
            for idx in range(bare_returns):
                return_rows.append({"return_index":idx,
                    "decompiled_expression":"return; (C function type void)",
                    "mips_v0":"NO_DEFINED_RETURN_VALUE; ABI does not define residual $v0 for void",
                    "physical_jr_ra_count":epilogs})
        else:
            for idx,expr in enumerate(rets):
                return_rows.append({"return_index":idx,"decompiled_expression":expr.strip(),
                    "mips_v0":"TIDAK TAHU; decompiled expression not mapped to a unique MIPS return path",
                    "physical_jr_ra_count":epilogs})
    write_tsv(out/"HA2_F2A9C_RETURN_PATHS.tsv",return_rows,
              ["return_index","decompiled_expression","mips_v0","physical_jr_ra_count"])

    # Key arithmetic / condition instructions in F2A9C.
    keyrows=[]
    if f2:
        for r in rows_from_function(f2,"ENTRY1",entry,ENTRY_BASE):
            pc=int(r["pc"],16); i=en.get(pc)
            if not i: continue
            relevant=(i["mnemonic"] in {"and","andi","mult","multu","mflo","subu","sub","addiu","addu","lw","lbu","lh","lhu","beq","bne","beqz","bnez","slt","slti","sltiu"})
            if relevant and (i["imm"] in (0x530,-0x158f,-0x6104,-0x14f4,0x2ee) or i["mnemonic"] in {"and","andi","mult","multu","mflo","subu","sub","beq","bne","slt","slti","sltiu"}):
                keyrows.append({k:r[k] for k in ("pc","file_offset","bytes","instruksi")})
    write_tsv(out/"HA2_F2A9C_KEY_INSTRUCTIONS.tsv",keyrows,["pc","file_offset","bytes","instruksi"])

    # Search computed callers and raw absolute pointer occurrences.
    indirect=[]
    for image,code,blob in (("EXE",ex,exe),("ENTRY1",en,entry)):
        for i in code.values():
            if i["mnemonic"] in ("jalr","jr"):
                target=const_reg(code,i["rs"],i["pc"])
                if target==0x800F2A9C:
                    indirect.append({"pc":h32(i["pc"]),"file_offset":f"0x{i['fileoff']:X}",
                                     "bytes":hx(i["bytes"]),"instruksi":i["text"],
                                     "image":image,"kind":"RESOLVED_COMPUTED_TRANSFER",
                                     "target":h32(target),"origin":trace_reg(code,i["rs"],i["pc"])})
        needle=struct.pack("<I",0x800F2A9C)
        start=0
        while True:
            pos=blob.find(needle,start)
            if pos<0: break
            pc=(EXE_BASE+pos) if image=="EXE" else (ENTRY_BASE+pos)
            indirect.append({"pc":h32(pc),"file_offset":f"0x{file_offset(pc,image):X}",
                             "bytes":hx(needle),"instruksi":"raw pointer word 0x800F2A9C",
                             "image":image,"kind":"ABSOLUTE_POINTER_CANDIDATE",
                             "target":h32(0x800F2A9C),"origin":"table membership/function-pointer use TIDAK TERBUKTI"})
            start=pos+1
    write_tsv(out/"HA2_F2A9C_INDIRECT_CALL_CANDIDATES.tsv",indirect,
              ["pc","file_offset","bytes","instruksi","image","kind","target","origin"])

    # HA3 full manager+0x2EE census with an explicit index-origin trace.
    manager_rows=[]; index_instrs={}
    function_starts_entry=[
        0x800B1E88,0x800B2A58,0x800BE5D8,0x800D15A8,0x800DC2E0,
        0x800E3E74,0x800E6470,0x800E9220,0x800EC574,0x800F0C10,
        0x800F2A9C,0x800FAAC8,0x800DFEE8,0x800EB290,
    ]
    for image,code in (("EXE",ex),("ENTRY1",en)):
        starts=function_starts_entry if image=="ENTRY1" else [EXE_BASE]
        for i in sorted(code.values(),key=lambda q:q["pc"]):
            if i["mnemonic"] not in MEM or i["imm"]!=0x2ee: continue
            lo=max((z for z in starts if z<=i["pc"]),default=(ENTRY_BASE if image=="ENTRY1" else EXE_BASE))
            if not is_manager_pointer(code,i["rs"],i["pc"],lo):
                continue
            idxreg,idxtrace=manager_index(code,i["rs"],i["pc"],lo)
            read=i["mnemonic"] in LOADS
            value_trace="loaded value -> "+REG[i["rt"]] if read else trace_reg(code,i["rt"],i["pc"],lo)
            manager_rows.append({
                "pc":h32(i["pc"]),"file_offset":f"0x{i['fileoff']:X}","bytes":hx(i["bytes"]),
                "instruksi":i["text"],"access":"READ" if read else "WRITE",
                "image":image,"function":h32(lo),"manager_base":"0x8013EA74",
                "index_register":idxreg,"index_origin":idxtrace,
                "write_source_class":"REGISTER_NOT_LITERAL_ZERO" if not read and i["rt"]!=0 else ("LITERAL_ZERO" if not read else "—"),
                "value_origin":value_trace,
            })
            if idxreg not in ("TIDAK TAHU","0") and idxreg.startswith("$"):
                d=last_def(code,REG.index(idxreg),i["pc"],lo)
                if d:
                    for pc in range(max(lo,d["pc"]-0x20),d["pc"]+4,4):
                        q=code.get(pc)
                        if q:
                            index_instrs[(image,q["pc"],q["bytes"])]=q
    write_tsv(out/"HA3_MANAGER_2EE_INDEXED_CENSUS.tsv",manager_rows,
              ["pc","file_offset","bytes","instruksi","access","image","function","manager_base",
               "index_register","index_origin","write_source_class","value_origin"])
    iw=[]
    for (image,pc,raw),i in sorted(index_instrs.items(),key=lambda x:(x[0][0],x[0][1])):
        iw.append({"pc":h32(i["pc"]),"file_offset":f"0x{i['fileoff']:X}",
                   "bytes":hx(i["bytes"]),"instruksi":i["text"]})
    write_tsv(out/"HA3_INDEX_ORIGIN_INSTRUCTIONS.tsv",iw,["pc","file_offset","bytes","instruksi"])

    # Global operand census for the three operands feeding F2A9C.
    globals_rows=[]
    wanted={0x8013EA71:"G_BYTE",0x80139EFC:"Q_U32",0x8013EA74:"MANAGER_SLOT",0x8013EB0C:"IDX_GLOBAL"}
    for image,code in (("EXE",ex),("ENTRY1",en)):
        for i in code.values():
            if i["mnemonic"] not in MEM: continue
            ea=effective_addr(code,i)
            if ea not in wanted: continue
            globals_rows.append({"pc":h32(i["pc"]),"file_offset":f"0x{i['fileoff']:X}",
                                 "bytes":hx(i["bytes"]),"instruksi":i["text"],
                                 "image":image,"global":wanted[ea],
                                 "access":"READ" if i["mnemonic"] in LOADS else "WRITE",
                                 "effective_address":h32(ea)})
    write_tsv(out/"HA2_GLOBAL_OPERAND_ACCESS.tsv",globals_rows,
              ["pc","file_offset","bytes","instruksi","image","global","access","effective_address"])

    # Preserve compact reader decompilation and direct function references for manual terminal-use adjudication.
    reader_summary=[]
    for pc,label in ((0x800F2A9C,"READ_800F2E80_IN_F2A9C"),
                     (0x800DC2E0,"READ_800DCFE8_IN_DC2E0"),
                     (0x800FAAC8,"READ_800FAAEC_IN_FAAC8")):
        f=ent_funcs.get(pc)
        if not f:
            reader_summary.append(f"{label}=FUNCTION_NOT_FOUND\n")
            continue
        dest=out/f"HA3_{label}.txt"
        write_text(dest,
            f"FUNCTION={f['name']}\nENTRY={h32(f['entry'])}\n"
            f"RAW_INSTRUCTION_COUNT={len(f['raw'])}\n\nC_DECOMPILATION:\n{f['decomp'] or 'TIDAK ADA'}\n\n"
            f"REFERENCES_TO_FUNCTION:\n{f['refs'] or 'TIDAK ADA'}\n")
        reader_summary.append(f"{label}=EXPORTED; {dest.name}; raw_instructions={len(f['raw'])}")
    write_text(out/"HA3_READER_EXPORT_SUMMARY.txt","\n".join(reader_summary)+"\n")

    # Compact run findings and validation counters.
    counts={
        "helper_raw_instructions":len(helper_rows),
        "helper_excerpt_files":helper_chunks,
        "store_window_instructions":window_n,
        "helper_table_rows":len(table_rows),
        "f2a9c_return_exprs":len(rets),
        "f2a9c_key_instructions":len(keyrows),
        "indirect_call_candidates":len(indirect),
        "manager_2ee_census_rows":len(manager_rows),
        "nonzero_manager_writes":sum(1 for r in manager_rows if r["write_source_class"]=="REGISTER_NOT_LITERAL_ZERO"),
        "index_origin_instruction_rows":len(iw),
        "global_operand_rows":len(globals_rows),
    }
    summary=[
        "STATUS=PASS_RAW_IDENTITY_AND_STATIC_SCAN",
        f"EXE_SHA256={EXE_SHA}",f"ENTRY1_SHA256={ENTRY_SHA}",
        "GAME_OR_EMULATOR_EXECUTED=no","BIOS_OR_SAVESTATE_USED=no",
        "BINARY_OUTPUT_COMMITTED=no",
    ]
    for k,v in counts.items(): summary.append(f"{k.upper()}={v}")
    for k,(n,ch) in chunk_counts.items(): summary.append(f"{k}_INSTRUCTIONS={n}; CHUNK_FILES={ch}; MAX_INSTRUCTIONS_PER_FILE=16")
    summary.append("HELPER_BOUND="+(str(bound) if bound is not None else "TIDAK TAHU"))
    summary.append("HELPER_BOUND_SOURCE=FUN_800154D4 reads DAT_8006D794 via GP+0x118; value not statically bounded here")
    summary.append("HA3_TERMINAL_USE=manual Ghidra C review required; see three reader exports and final addendum")
    validate_instruction_tsvs(out)
    write_text(out/"HA2_HA3_STATIC_SUMMARY.txt","\n".join(summary)+"\n")

if __name__=="__main__":
    main()
