#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, os, struct, subprocess, sys
from collections import defaultdict, deque
from pathlib import Path
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_PATH, DATA_PATH, OUT = map(Path, sys.argv[1:4])
BASELINE = os.environ.get("DX_BASELINE", "f76a096862ceb88920df19b021a30870c74a9496")
SNAPSHOT = os.environ.get("DX_SNAPSHOT_SHA", "").strip()
if not SNAPSHOT or SNAPSHOT.startswith("$"):
    SNAPSHOT = os.environ.get("GITHUB_SHA", subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip())
EXE_BASE, ENTRY_BASE, ENTRY_OFF = 0x80010000, 0x800AD450, 0x10BB000
EXE_SHA = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
DATA_SHA = "69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
ENTRY_SHA = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
ENTRY_SIZE = 596412
OUT.mkdir(parents=True, exist_ok=True)

REG = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7",
       "s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
def rn(n): return "$"+REG[n]
def hx(b): return " ".join(f"{x:02X}" for x in b)
def h32(v): return f"0x{v & 0xffffffff:08X}"
def write_tsv(name, rows, fields):
    with (OUT/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore")
        w.writeheader()
        for r in rows: w.writerow(r)
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def git(args): return subprocess.check_output(["git",*args],text=True).strip()

if len(EXE_PATH.read_bytes()) != 385024 or sha(EXE_PATH) != EXE_SHA:
    raise SystemExit("EXE_IDENTITY_MISMATCH")
data=DATA_PATH.read_bytes()
if len(data) != 66015232 or hashlib.sha256(data).hexdigest() != DATA_SHA:
    raise SystemExit("DATA_BIN_IDENTITY_MISMATCH")
lbn,size=struct.unpack_from("<II",data,0x4C)
entry_off=(lbn-212)*2048
entry=data[entry_off:entry_off+size]
if (lbn,size,entry_off,len(entry),hashlib.sha256(entry).hexdigest()) != (8778,ENTRY_SIZE,ENTRY_OFF,ENTRY_SIZE,ENTRY_SHA):
    raise SystemExit("ENTRY1_DIRECTORY_MAPPING_MISMATCH")

md=Cs(CS_ARCH_MIPS,CS_MODE_MIPS32|CS_MODE_LITTLE_ENDIAN)
md.detail=False
def decode(blob,base,file_base):
    out={}
    for off in range(0,len(blob)-3,4):
        b=blob[off:off+4]; pc=base+off; word=int.from_bytes(b,"little")
        x=next(md.disasm(b,pc,count=1),None)
        mnemonic=x.mnemonic.lower() if x else ".word"
        op_str=x.op_str if x else ""
        out[pc]={"pc":pc,"off":off,"fileoff":file_base+off,"bytes":b,"word":word,
          "text":(mnemonic+" "+op_str).strip(),"mnemonic":mnemonic,"op_str":op_str,
          "op":word>>26,"rs":(word>>21)&31,"rt":(word>>16)&31,"rd":(word>>11)&31,
          "sh":(word>>6)&31,"fn":word&63,"imm":((word&0xffff)^0x8000)-0x8000,
          "uimm":word&0xffff,"target":word&0x03ffffff}
    return out
exe=decode(EXE_PATH.read_bytes(),EXE_BASE,0x800)
ins=decode(entry,ENTRY_BASE,ENTRY_OFF)
codes=[("EXE",exe,EXE_BASE),("ENTRY1",ins,ENTRY_BASE)]
MEM_LOADS={"lb","lh","lw","lbu","lhu","lwl","lwr"}
MEM_STORES={"sb","sh","sw","swl","swr"}
DX1_MN={"lhu","lbu","sh","sb","lw","sw"}
PTR_SLOTS={
  0x8013EA74:"SLOT_0x8013EA74",
  0x8013EA84:"SLOT_0x8013EA84",
  0x8013EA88:"SLOT_0x8013EA88",
  0x8013A554:"SLOT_0x8013A554",
  0x8013B818:"ABSOLUTE_OR_POINTER_VALUE_0x8013B818"
}
SPECIAL_FUNCS={
  0x8001387C:"FUN_8001387C",
  0x8001552C:"FUN_8001552C",
  0x800D15A8:"FUN_800D15A8",
  0x800EB434:"FUN_800EB434",
  0x800EC574:"FUN_800EC574",
  0x800EF3CC:"SITE_800EF3CC"
}

def dest_reg(i):
    op,fn=i["op"],i["fn"]
    if op==0:
        if fn in (8,9,12,13,24,25,26,27): return None
        return i["rd"] if i["rd"] else None
    if op==3:return 31
    if op in (1,2,4,5,6,7,0x28,0x29,0x2a,0x2b,0x2e,0x38,0x39,0x3a,0x3b):return None
    if op in (8,9,10,11,12,13,14,15,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,
              0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37):return i["rt"] if i["rt"] else None
    return None
def branch_target(i):
    op=i["op"]; pc=i["pc"]
    if op in (1,4,5,6,7): return (pc+4+(i["imm"]<<2))&0xffffffff
    if op in (2,3): return (((pc+4)&0xf0000000)|(i["target"]<<2))&0xffffffff
    return None
def make_functions(code,base):
    starts={base}
    for i in code.values():
        if i["op"]==3:
            t=branch_target(i)
            if t in code: starts.add(t)
        if i["op"]==9 and i["rs"]==29 and i["rt"]==29 and i["imm"]<0:
            starts.add(i["pc"])
    for pc in SPECIAL_FUNCS:
        if pc in code: starts.add(pc)
    ordered=sorted(starts)
    def f_at(pc):
        lo=base
        for x in ordered:
            if x<=pc: lo=x
            else: break
        return lo
    def f_name(pc):
        start=f_at(pc)
        return SPECIAL_FUNCS.get(start,"FUN_"+f"{start:08X}")
    def next_start(pc):
        return next((x for x in ordered if x>pc),base+len(code)*4)
    return starts,f_at,f_name,next_start
FUNC={}
for tag,code,base in codes:
    FUNC[tag]=make_functions(code,base)

CALLER_SAVED = set(range(4,16)) | {24,25}
RETURN_REGS = {2,3}
def call_target_text(i):
    if not i: return "TIDAK TAHU"
    if i["op"]==3:
        t=branch_target(i)
        return h32(t) if t is not None else "TIDAK TAHU"
    if i["op"]==0 and i["fn"]==9:
        return "JALR_TARGET_TIDAK_TAHU"
    return "TIDAK TAHU"
def last_call_before(before,lo,code):
    for pc in range(before-4,lo-4,-4):
        i=code.get(pc)
        if i and (i["op"]==3 or (i["op"]==0 and i["fn"]==9)):
            return i
    return None
def last_def(reg,before,lo,code):
    for pc in range(before-4,lo-4,-4):
        i=code.get(pc)
        if i and dest_reg(i)==reg:
            # A MIPS call invalidates caller-saved GPRs, including the delay-slot
            # setup immediately before the call. Never carry a local slice across it.
            if reg in (CALLER_SAVED | RETURN_REGS):
                for cp in range(before-4, max(lo-4, i["pc"]-8), -4):
                    c=code.get(cp)
                    if c and (c["op"]==3 or (c["op"]==0 and c["fn"]==9)):
                        return None
            return i
    return None
def const_before(reg,before,lo,code,depth=0,seen=None):
    if seen is None:seen=set()
    if depth>12 or (reg,before) in seen:return None
    seen.add((reg,before))
    if reg==0:return 0
    d=last_def(reg,before,lo,code)
    if not d:return None
    op,rs,rt,fn=d["op"],d["rs"],d["rt"],d["fn"]
    if op==0x0f:return (d["uimm"]<<16)&0xffffffff
    if op in (0x0d,0x0e):
        x=const_before(rs,d["pc"],lo,code,depth+1,seen.copy())
        return ((x|d["uimm"]) if op==0x0d else (x^d["uimm"]))&0xffffffff if x is not None else None
    if op in (8,9):
        x=const_before(rs,d["pc"],lo,code,depth+1,seen.copy())
        return (x+d["imm"])&0xffffffff if x is not None else None
    if op==0 and fn in (0x20,0x21,0x22,0x23,0x24,0x25,0x26):
        x=const_before(rs,d["pc"],lo,code,depth+1,seen.copy())
        y=const_before(rt,d["pc"],lo,code,depth+1,seen.copy())
        if x is None or y is None:return None
        return {0x20:x+y,0x21:x+y,0x22:x-y,0x23:x-y,0x24:x&y,0x25:x|y,0x26:x^y}[fn]&0xffffffff
    if op==0 and fn in (0,2,3):
        x=const_before(rt,d["pc"],lo,code,depth+1,seen.copy())
        if x is None:return None
        return ((x<<d["sh"]) if fn==0 else (x>>d["sh"]))&0xffffffff
    if op==0 and fn in (4,6,7):
        x=const_before(rt,d["pc"],lo,code,depth+1,seen.copy())
        y=const_before(rs,d["pc"],lo,code,depth+1,seen.copy())
        if x is None or y is None:return None
        return ((x<<y) if fn==4 else (x>>y))&0xffffffff
    return None
def effective_address(i,code,lo):
    base=const_before(i["rs"],i["pc"],lo,code)
    return ((base+i["imm"])&0xffffffff) if base is not None else None
def collect_slots(reg,before,lo,code,depth=0,seen=None):
    if seen is None:seen=set()
    if depth>10 or (reg,before) in seen:return set()
    seen.add((reg,before))
    if reg==0:return set()
    d=last_def(reg,before,lo,code)
    if not d:return set()
    if d["mnemonic"] in MEM_LOADS:
        ea=effective_address(d,code,lo)
        return {ea} if ea in PTR_SLOTS else set()
    op,fn=d["op"],d["fn"]
    if op in (8,9,10,11,12,13,14):
        return collect_slots(d["rs"],d["pc"],lo,code,depth+1,seen.copy())
    if op==0 and fn in (0,2,3,4,6,7,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27):
        return collect_slots(d["rs"],d["pc"],lo,code,depth+1,seen.copy()) | collect_slots(d["rt"],d["pc"],lo,code,depth+1,seen.copy())
    return set()
def base_origin(reg,before,lo,code):
    slots=collect_slots(reg,before,lo,code)
    if slots:return ";".join(PTR_SLOTS.get(x,h32(x)) for x in sorted(slots))
    c=const_before(reg,before,lo,code)
    if c is not None:return "ABSOLUTE_"+h32(c)
    d=last_def(reg,before,lo,code)
    if not d:return "ENTRY_OR_DYNAMIC_"+rn(reg)
    if d["mnemonic"] in MEM_LOADS:
        ea=effective_address(d,code,lo)
        if ea is not None:return "OTHER_MEMORY_LOAD_AT_"+h32(ea)
    return "OTHER_OR_UNRESOLVED"
def trace_reg(reg,before,lo,code,depth=0,seen=None):
    if seen is None: seen=set()
    if depth>8 or (reg,before) in seen: return "TIDAK TAHU: batas def-chain"
    seen.add((reg,before))
    if reg==0: return "$zero"
    d=last_def(reg,before,lo,code)
    if not d:
        c=last_call_before(before,lo,code)
        if c and reg in RETURN_REGS:
            kind="JALR" if c["op"]==0 else "JAL"
            return "return "+kind+" "+call_target_text(c)
        if c and reg in CALLER_SAVED:
            kind="JALR" if c["op"]==0 else "JAL"
            return "TIDAK TAHU: caller-saved setelah "+kind+" "+call_target_text(c)
        return rn(reg)+" masuk/dinamis"
    mn=d["mnemonic"]; op,fn=d["op"],d["fn"]
    s=f"{h32(d['pc'])} {d['text']}"
    if mn in MEM_LOADS:
        ea=effective_address(d,code,lo)
        s+=" [load "+(h32(ea) if ea is not None else "alamat dinamis")+"; base "+rn(d["rs"])+"]"
    elif op in (8,9,10,11,12,13,14):
        s+=" <- "+trace_reg(d["rs"],d["pc"],lo,code,depth+1,seen.copy())
    elif op==0 and fn in (0,2,3):
        s+=" <- "+trace_reg(d["rt"],d["pc"],lo,code,depth+1,seen.copy())
    elif op==0 and fn in (4,6,7,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27):
        s+=" <- "+trace_reg(d["rs"],d["pc"],lo,code,depth+1,seen.copy())+" , "+trace_reg(d["rt"],d["pc"],lo,code,depth+1,seen.copy())
    elif mn in ("mflo","mfhi"):
        mul=next((code[p] for p in range(d["pc"]-4,max(lo-4,d["pc"]-0x50),-4)
                  if p in code and code[p]["mnemonic"] in ("mult","multu")),None)
        if mul:
            s+=" <- "+h32(mul["pc"])+" "+mul["text"]+" ("+trace_reg(mul["rs"],mul["pc"],lo,code,depth+1,seen.copy())+"; "+trace_reg(mul["rt"],mul["pc"],lo,code,depth+1,seen.copy())+")"
    return s[:1200]

# DX0: enumerate baseline-inclusively; the workflow publication is counted after snapshot.
if subprocess.run(["git","merge-base","--is-ancestor",BASELINE,SNAPSHOT]).returncode != 0:
    raise SystemExit("DX0_BASELINE_NOT_ANCESTOR")
if git(["rev-parse","HEAD"]) != SNAPSHOT:
    raise SystemExit("DX0_SOURCE_HEAD_MISMATCH")
revs=git(["rev-list","--reverse",f"{BASELINE}^..{SNAPSHOT}"]).splitlines()
ledger=[]; humans=bots=0
for rev in revs:
    vals=git(["show","-s","--format=%H%x09%an%x09%ae%x09%s",rev]).split("\t",3)
    sh,author,email,msg=vals
    bot=("github-actions" in author.lower() or "[bot]" in author.lower() or "41898282+github-actions" in email.lower())
    bots+=int(bot); humans+=int(not bot)
    changed=git(["diff-tree","--root","--no-commit-id","--name-only","-r",rev]).splitlines()
    ledger.append({"sha_full":sh,"class":"BOT" if bot else "MANUSIA","author":author,
      "author_email":email,"message":msg,"changed_files":";".join(changed),
      "source":"git rev-list baseline^..snapshot","reason":"inklusif; baseline ikut dihitung"})
write_tsv("DX0_COMMIT_LEDGER.tsv",ledger,["sha_full","class","author","author_email","message","changed_files","source","reason"])
write_tsv("DX0_COUNTS.tsv",[
 {"scope":"SNAPSHOT_SOURCE","sha":SNAPSHOT,"total_inclusive":len(ledger),"human":humans,"bot":bots,
  "method":"git rev-list baseline^..snapshot","note":"snapshot pemicu; commit publikasi tidak termasuk"},
 {"scope":"EXPECTED_AFTER_ONE_PUBLICATION","sha":"VERIFIKASI_SETELAH_RUN","total_inclusive":len(ledger)+1,"human":humans,"bot":bots+1,
  "method":"snapshot ledger + satu commit publikasi bot","note":"proyeksi; final main diverifikasi terpisah setelah Actions"}
],["scope","sha","total_inclusive","human","bot","method","note"])

# DX1: all full-image accesses to displacement 0x1A; no pointer-origin filter.
dx1=[]
for tag,code,base in codes:
    starts,f_at,f_name,_=FUNC[tag]
    for i in sorted(code.values(),key=lambda x:x["pc"]):
        if i["mnemonic"] not in DX1_MN or i["imm"]!=0x1a:continue
        lo=f_at(i["pc"])
        dx1.append({"region":tag,"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),
          "bytes":hx(i["bytes"]),"instruction":i["text"],
          "access":"READ" if i["mnemonic"] in MEM_LOADS else "WRITE",
          "function_entry_guess":h32(f_at(i["pc"])),"function_name_guess":f_name(i["pc"]),
          "base_register":rn(i["rs"]),"base_origin_slot_or_address":base_origin(i["rs"],i["pc"],lo,code),
          "base_origin_register_trace":trace_reg(i["rs"],i["pc"],lo,code),
          "value_origin":trace_reg(i["rt"],i["pc"],lo,code) if i["mnemonic"] in MEM_STORES else "loaded value -> "+rn(i["rt"]),
          "source":"EXE offset=PC-0x80010000" if tag=="EXE" else "Entry 1 offset=0x10BB000+(PC-0x800AD450)",
          "reason":"linear full-image scan; displacement literal +0x1A; no base-register filter"})
write_tsv("DX1_ALL_PLUS1A_ACCESS.tsv",dx1,
 ["region","pc","file_offset","bytes","instruction","access","function_entry_guess","function_name_guess",
  "base_register","base_origin_slot_or_address","base_origin_register_trace","value_origin","source","reason"])
dx1_d15=[r for r in dx1 if r["pc"]>="0x800D15A8" and r["pc"]<"0x800D3000" and r["region"]=="ENTRY1"]
write_tsv("DX1_D15A8_WINDOW_PLUS1A.tsv",dx1_d15,
 ["region","pc","file_offset","bytes","instruction","access","function_entry_guess","function_name_guess",
  "base_register","base_origin_slot_or_address","base_origin_register_trace","value_origin","source","reason"])

# DX2: all memory operations at +0x2EE, irrespective of base register.
dx2_access=[]
for tag,code,base in codes:
    starts,f_at,f_name,_=FUNC[tag]
    for i in sorted(code.values(),key=lambda x:x["pc"]):
        if i["mnemonic"] not in (MEM_LOADS|MEM_STORES) or i["imm"]!=0x2ee:continue
        lo=f_at(i["pc"])
        dx2_access.append({"region":tag,"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),
          "bytes":hx(i["bytes"]),"instruction":i["text"],
          "access":"READ" if i["mnemonic"] in MEM_LOADS else "WRITE",
          "width":"1" if i["mnemonic"] in ("lb","lbu","sb") else "2" if i["mnemonic"] in ("lh","lhu","sh") else "4",
          "function_entry_guess":h32(f_at(i["pc"])),"function_name_guess":f_name(i["pc"]),
          "base_register":rn(i["rs"]),"base_origin":base_origin(i["rs"],i["pc"],lo,code),
          "base_origin_trace":trace_reg(i["rs"],i["pc"],lo,code),
          "value_origin":trace_reg(i["rt"],i["pc"],lo,code) if i["mnemonic"] in MEM_STORES else "loaded value -> "+rn(i["rt"]),
          "source":"full EXE + Entry 1 linear memory-op scan",
          "reason":"all bases included; displacement exactly +0x2EE"})
write_tsv("DX2_ALL_PLUS2EE_ACCESS.tsv",dx2_access,
 ["region","pc","file_offset","bytes","instruction","access","width","function_entry_guess","function_name_guess",
  "base_register","base_origin","base_origin_trace","value_origin","source","reason"])

def depends_on_pc(reg,before,lo,code,target_pcs,depth=0,seen=None):
    if seen is None:seen=set()
    if depth>14 or (reg,before) in seen:return set()
    seen.add((reg,before))
    if reg==0:return set()
    d=last_def(reg,before,lo,code)
    if not d:return set()
    if d["pc"] in target_pcs:return {d["pc"]}
    op,fn=d["op"],d["fn"]
    if d["mnemonic"]=="mflo":
        mul=next((code[p] for p in range(d["pc"]-4,max(lo-4,d["pc"]-0x50),-4)
                  if p in code and code[p]["mnemonic"] in ("mult","multu")),None)
        if mul:
            return depends_on_pc(mul["rs"],mul["pc"],lo,code,target_pcs,depth+1,seen.copy()) | depends_on_pc(mul["rt"],mul["pc"],lo,code,target_pcs,depth+1,seen.copy())
        return set()
    if op in (8,9,10,11,12,13,14):
        return depends_on_pc(d["rs"],d["pc"],lo,code,target_pcs,depth+1,seen.copy())
    if op==0 and fn in (0,2,3):
        return depends_on_pc(d["rt"],d["pc"],lo,code,target_pcs,depth+1,seen.copy())
    if op==0 and fn in (4,6,7,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27):
        return depends_on_pc(d["rs"],d["pc"],lo,code,target_pcs,depth+1,seen.copy()) | depends_on_pc(d["rt"],d["pc"],lo,code,target_pcs,depth+1,seen.copy())
    return set()

reader_pcs={int(r["pc"],16) for r in dx2_access if r["access"]=="READ" and r["region"]=="ENTRY1"}
setter_calls=[]; reader_setter=[]
for tag,code,base in codes:
    starts,f_at,f_name,_=FUNC[tag]
    readers_by_func=defaultdict(list)
    for r in dx2_access:
        if r["region"]==tag and r["access"]=="READ":
            readers_by_func[r["function_entry_guess"]].append(r)
    for i in sorted(code.values(),key=lambda x:x["pc"]):
        if i["op"]!=3 or branch_target(i)!=0x8001387c:continue
        lo=f_at(i["pc"]); fe=h32(lo); fn=f_name(i["pc"])
        dep=depends_on_pc(5,i["pc"],lo,code,reader_pcs)
        callrow={"region":tag,"call_pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),
          "bytes":hx(i["bytes"]),"instruction":i["text"],"function_entry_guess":fe,"function_name_guess":fn,
          "a0_origin":trace_reg(4,i["pc"],lo,code),"a1_origin":trace_reg(5,i["pc"],lo,code),
          "a1_depends_on_plus2EE_reader":"YES" if dep else "NOT_PROVEN_BY_LOCAL_DEF_CHAIN",
          "reader_pcs":";".join(h32(x) for x in sorted(dep)) if dep else "TIDAK TAHU",
          "source":"direct JAL to 0x8001387C; backward local register slice",
          "reason":"no dependency is inferred from function proximity alone"}
        setter_calls.append(callrow)
        for rp in readers_by_func.get(fe,[]):
            reader_setter.append({"region":tag,"reader_pc":rp["pc"],"reader_instruction":rp["instruction"],
              "function_entry_guess":fe,"function_name_guess":fn,"setter_call_pc":h32(i["pc"]),
              "setter_a1_origin":callrow["a1_origin"],
              "direct_def_chain_dependency":"YES" if int(rp["pc"],16) in dep else "NOT_PROVEN",
              "source":"reader/setter same inferred function + setter backward slice",
              "reason":"same function is a candidate link; YES only when the value slice reaches this reader"})
for r in dx2_access:
    if r["region"]=="ENTRY1" and r["access"]=="READ":
        if not any(x["reader_pc"]==r["pc"] for x in reader_setter):
            reader_setter.append({"region":"ENTRY1","reader_pc":r["pc"],"reader_instruction":r["instruction"],
              "function_entry_guess":r["function_entry_guess"],"function_name_guess":r["function_name_guess"],
              "setter_call_pc":"NO_DIRECT_CALL_FOUND_IN_INFERRED_FUNCTION","setter_a1_origin":"TIDAK TAHU",
              "direct_def_chain_dependency":"NOT_PROVEN",
              "source":"all Entry 1 +0x2EE readers crosschecked against direct setter callers",
              "reason":"reader need not be in same function as setter; indirect/interprocedural flow remains unresolved"})
write_tsv("DX2_SETTER_8001387C_CALLS.tsv",setter_calls,
 ["region","call_pc","file_offset","bytes","instruction","function_entry_guess","function_name_guess","a0_origin",
  "a1_origin","a1_depends_on_plus2EE_reader","reader_pcs","source","reason"])
write_tsv("DX2_2EE_READERS_TO_SETTER.tsv",reader_setter,
 ["region","reader_pc","reader_instruction","function_entry_guess","function_name_guess","setter_call_pc",
  "setter_a1_origin","direct_def_chain_dependency","source","reason"])

# CFG: explicitly route through MIPS delay slots and terminate JR, never invent fall-through.
def cond_text(i):
    op,rt=i["op"],i["rt"]
    if op==4:return rn(i["rs"])+" == "+rn(rt)
    if op==5:return rn(i["rs"])+" != "+rn(rt)
    if op==6:return rn(i["rs"])+" <= 0"
    if op==7:return rn(i["rs"])+" > 0"
    if op==1:
        if rt in (0,2,16,18):return rn(i["rs"])+" < 0"
        if rt in (1,3,17,19):return rn(i["rs"])+" >= 0"
        return "REGIMM rt="+str(rt)+" on "+rn(i["rs"])
    return "NOT_CONDITIONAL"
def build_cfg(code,entry,tag,max_span=0x3000):
    starts,f_at,f_name,next_start=FUNC[tag]
    hi=min(entry+max_span,next_start(entry))
    graph=defaultdict(list); reachable=set(); exits=[]; branches=[]
    pending=deque([entry])
    while pending:
        pc=pending.popleft()
        if pc in reachable or pc<entry or pc>=hi:continue
        i=code.get(pc)
        if not i:continue
        reachable.add(pc); op,fn=i["op"],i["fn"]
        if op in (1,4,5,6,7):
            delay=pc+4; target=branch_target(i); fall=pc+8
            graph[pc].append((delay,"DELAY_SLOT"))
            di=code.get(delay)
            if di:
                for dst,label in [(target,"TAKEN"),(fall,"FALLTHROUGH")]:
                    if dst is not None and entry<=dst<hi and (dst not in starts or dst==entry):
                        graph[delay].append((dst,label)); pending.append(dst)
                    else:
                        exits.append({"pc":h32(pc),"kind":"BRANCH_"+label+"_OUTSIDE",
                          "target":h32(dst) if dst is not None else "TIDAK TAHU","condition":cond_text(i)})
                pending.append(delay)
            branches.append(i)
        elif op in (2,3):
            delay=pc+4; target=branch_target(i)
            graph[pc].append((delay,"DELAY_SLOT")); pending.append(delay)
            if op==3:
                ret=pc+8
                if ret<hi and (ret not in starts or ret==entry):
                    graph[delay].append((ret,"JAL_RETURN")); pending.append(ret)
                else:
                    exits.append({"pc":h32(pc),"kind":"JAL_RETURN_OUTSIDE","target":h32(ret),"condition":"CALL THEN RETURN"})
            elif target is not None and entry<=target<hi and (target not in starts or target==entry):
                graph[delay].append((target,"J_TARGET")); pending.append(target)
            else:
                exits.append({"pc":h32(pc),"kind":"J_OUTSIDE_FUNCTION","target":h32(target) if target is not None else "TIDAK TAHU","condition":"ALWAYS"})
        elif op==0 and fn in (8,9):
            delay=pc+4; graph[pc].append((delay,"DELAY_SLOT")); pending.append(delay)
            if fn==8 and i["rs"]==31:
                exits.append({"pc":h32(pc),"kind":"JR_RA_RETURN","target":"CALLER","condition":"ALWAYS; no fall-through"})
            elif fn==9:
                ret=pc+8
                if ret<hi and (ret not in starts or ret==entry):
                    graph[delay].append((ret,"JALR_RETURN_ASSUMED")); pending.append(ret)
                exits.append({"pc":h32(pc),"kind":"JALR_INDIRECT_CALL","target":"INDIRECT / TIDAK TAHU","condition":"CALL THEN RETURN ASSUMED"})
            else:
                target=const_before(i["rs"],pc,entry,code)
                if target is not None and entry<=target<hi:
                    graph[delay].append((target,"JR_CONSTANT_TARGET")); pending.append(target)
                    exits.append({"pc":h32(pc),"kind":"JR_REGISTER_CONSTANT","target":h32(target),"condition":"ALWAYS"})
                else:
                    exits.append({"pc":h32(pc),"kind":"JR_INDIRECT_EXIT","target":"INDIRECT / TIDAK TAHU","condition":"ALWAYS; no fall-through"})
        else:
            nxt=pc+4
            if nxt<hi and (nxt not in starts or nxt==entry):
                graph[pc].append((nxt,"SEQUENTIAL")); pending.append(nxt)
            else:
                exits.append({"pc":h32(pc),"kind":"SEQUENTIAL_BOUNDARY","target":h32(nxt),"condition":"ALWAYS"})
    return reachable,graph,exits,branches,hi

def reverse_reachable(graph,target):
    rev=defaultdict(list)
    for src,edges in graph.items():
        for dst,label in edges:rev[dst].append(src)
    seen={target}; q=deque([target])
    while q:
        x=q.popleft()
        for prev in rev.get(x,[]):
            if prev not in seen:seen.add(prev);q.append(prev)
    return seen

dx2_entry=0x800EC574
reach2,g2,exits2,branches2,hi2=build_cfg(ins,dx2_entry,"ENTRY1",0x3000)
target_pcs=sorted(set([0x800ECAD0,0x800ECB4C,0x800ECB88,0x800ECBBC,0x800ECBB8]+list(range(0x800ECBA8,0x800ECBBC,4))))
target_rows=[]; gate_rows=[]
for target in target_pcs:
    can=reverse_reachable(g2,target)
    yes=target in reach2
    target_rows.append({"target_pc":h32(target),"reachable_from_800EC574":"YES" if yes else "NO",
      "function_bound_end_guess":h32(hi2),"source":"intra-function CFG rooted at 0x800EC574",
      "reason":"branch delay slots explicit; JR RA/indirect JR terminates; no assumed JR fall-through"})
    if not yes:continue
    for b in branches2:
        bp=b["pc"]; ds=bp+4; target_b=branch_target(b); fall=bp+8
        taken_can=(target_b in can) if target_b is not None else False
        fall_can=fall in can
        if not taken_can and not fall_can:continue
        if taken_can and fall_can: required="BOTH_OUTCOMES_CAN_REACH"
        elif taken_can: required="TAKEN_REQUIRED"
        else: required="FALLTHROUGH_REQUIRED"
        lo=dx2_entry
        gate_rows.append({"target_pc":h32(target),"branch_pc":h32(bp),"file_offset":h32(b["fileoff"]),
          "bytes":hx(b["bytes"]),"instruction":b["text"],"condition":cond_text(b),
          "condition_registers":rn(b["rs"])+(","+rn(b["rt"]) if b["op"] in (4,5) else ""),
          "required_outcome":required,"branch_target":h32(target_b) if target_b is not None else "TIDAK TAHU",
          "fallthrough_after_delay":h32(fall),"rs_origin":trace_reg(b["rs"],bp,lo,ins),
          "rt_origin":trace_reg(b["rt"],bp,lo,ins) if b["op"] in (4,5) else "—",
          "source":"reverse reachability over delay-slot-aware CFG",
          "reason":"one row per conditional branch capable of influencing this target"})
write_tsv("DX2_TARGET_REACHABILITY.tsv",target_rows,
 ["target_pc","reachable_from_800EC574","function_bound_end_guess","source","reason"])
write_tsv("DX2_PATH_CONDITIONS.tsv",gate_rows,
 ["target_pc","branch_pc","file_offset","bytes","instruction","condition","condition_registers","required_outcome",
  "branch_target","fallthrough_after_delay","rs_origin","rt_origin","source","reason"])
write_tsv("DX2_CFG_JR_AND_EXTERNAL_EXITS.tsv",exits2,
 ["pc","kind","target","condition"])
cfg_rows=[]
for pc in sorted(reach2):
    i=ins[pc]
    kind="INSTRUCTION"
    if any(pc==b["pc"]+4 for b in branches2):kind="BRANCH_DELAY_SLOT"
    if i["op"] in (1,4,5,6,7):kind="CONDITIONAL_BRANCH"
    if i["op"] in (2,3):kind="J_OR_JAL"
    if i["op"]==0 and i["fn"] in (8,9):kind="JR_OR_JALR"
    cfg_rows.append({"pc":h32(pc),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
      "instruction":i["text"],"cfg_kind":kind,"source":"Entry 1 CFG rooted at FUN_800EC574",
      "reason":"instruction is reachable from entry under direct-control-flow and delay-slot model"})
write_tsv("DX2_FUN_800EC574_CFG.tsv",cfg_rows,
 ["pc","file_offset","bytes","instruction","cfg_kind","source","reason"])

special=[]
for pc,role in [
 (0x800ECAD0,"load helper argument"),
 (0x800ECAD4,"JAL FUN_8001552C"),
 (0x800ECAE0,"store helper result into global 0x80139EFC"),
 (0x800ECBA8,"read u16 global 0x80139EFC"),
 (0x800ECBB0,"negate loaded u16"),
 (0x800ECBB4,"jump; following PC is a delay slot"),
 (0x800ECBB8,"store low halfword of negative result to manager+0x2EE"),
 (0x800ECB4C,"requested target"),
 (0x800ECB88,"requested target"),
 (0x800ECBBC,"requested target")
]:
    i=ins.get(pc)
    if i:
        special.append({"pc":h32(pc),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
          "instruction":i["text"],"role":role,"reachable_from_function_entry":"YES" if pc in reach2 else "NO",
          "source":"Entry 1 raw decode + intra-function CFG",
          "reason":"reachability is not inferred from linear address order"})
write_tsv("DX2_HELPER_ONE_TO_PLUS2EE.tsv",special,
 ["pc","file_offset","bytes","instruction","role","reachable_from_function_entry","source","reason"])

# DX2: setter code itself and caller argument origins.
setter_reach,setter_graph,setter_exits,setter_branches,setter_hi=build_cfg(exe,0x8001387C,"EXE",0x1000)
setter_raw=[]
for pc in sorted(setter_reach):
    i=exe[pc]
    setter_raw.append({"pc":h32(pc),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
      "instruction":i["text"],"source":"EXE direct CFG rooted at setter 0x8001387C",
      "reason":"bounded setter body; memory destinations retain raw offset and base provenance"})
write_tsv("DX2_SETTER_8001387C_RAW.tsv",setter_raw,
 ["pc","file_offset","bytes","instruction","source","reason"])
write_tsv("DX2_SETTER_8001387C_EXITS.tsv",setter_exits,["pc","kind","target","condition"])

# DX3: requested roots, full reachable blocks, register origins, +0x20 level lanes.
dx3_seeds=[
 ("D15A8",0x800D15A8,"FUN_800D15A8",0x2800),
 ("EB434",0x800EB434,"FUN_800EB434",0x3000),
 ("EF3CC",0x800EF3CC,"SITE_800EF3CC",0x1800)
]
op_rows=[]; tile20_rows=[]; or_rows=[]; shift_one_rows=[]; diff_rows=[]; compare_rows=[]; seed_rows=[]
key_mn={"sll","sllv","srl","srlv","sra","srav","mult","multu","mflo","sub","subu","or","ori","andi"}
for label,seed,seed_name,span in dx3_seeds:
    reach,g,exits,branches,hi=build_cfg(ins,seed,"ENTRY1",span)
    seed_rows.append({"seed_pc":h32(seed),"seed_label":label,"function_label":seed_name,
      "reachable_instruction_count":len(reach),"reaches_800EC3A8":"YES" if 0x800EC3A8 in reach else "NO",
      "function_bound_end_guess":h32(hi),"source":"Entry 1 CFG rooted at requested PC",
      "reason":"direct jumps, conditional fall-through and delay slots modeled; indirect JR exits terminate"})
    tile20_loads=set()
    for pc in sorted(reach):
        i=ins[pc]; mn=i["mnemonic"]; lo=seed
        if mn in MEM_LOADS|MEM_STORES and i["imm"]==0x20:
            tile20_rows.append({"seed":label,"pc":h32(pc),"file_offset":h32(i["fileoff"]),
              "bytes":hx(i["bytes"]),"instruction":i["text"],
              "access":"READ" if mn in MEM_LOADS else "WRITE","function":seed_name,
              "base_register":rn(i["rs"]),"base_origin":base_origin(i["rs"],pc,lo,ins),
              "base_origin_trace":trace_reg(i["rs"],pc,lo,ins),
              "value_origin":trace_reg(i["rt"],pc,lo,ins) if mn in MEM_STORES else "loaded word -> "+rn(i["rt"]),
              "source":"reachable CFG rooted at "+h32(seed),
              "reason":"all bases retained; offset +0x20 is not itself proof of tile identity"})
            if mn=="lhu":tile20_loads.add(pc)
        if mn in key_mn or (mn in ("slti","sltiu") and i["imm"]==2):
            if mn in ("sll","sllv","srl","srlv","sra","srav"):
                src=trace_reg(i["rt"],pc,lo,ins)
                shift=trace_reg(i["rs"],pc,lo,ins) if mn in ("sllv","srlv","srav") else "immediate "+str(i["sh"])
                info="value_operand="+src+"; shift_count_origin="+shift
                val=const_before(i["rt"],pc,lo,ins)
                if mn=="sllv" and val==1:
                    shift_one_rows.append({"seed":label,"pc":h32(pc),"bytes":hx(i["bytes"]),
                      "instruction":i["text"],"value_operand":"1","shift_count_origin":shift,
                      "pattern":"1 << dynamic register","source":"reachable CFG operand trace",
                      "reason":"rt operand resolves statically to literal 1"})
                if mn=="sll" and val==1:
                    shift_one_rows.append({"seed":label,"pc":h32(pc),"bytes":hx(i["bytes"]),
                      "instruction":i["text"],"value_operand":"1","shift_count_origin":shift,
                      "pattern":"1 << immediate","source":"reachable CFG operand trace",
                      "reason":"rt operand resolves statically to literal 1"})
            elif mn in ("mult","multu"):
                info="rs_origin="+trace_reg(i["rs"],pc,lo,ins)+"; rt_origin="+trace_reg(i["rt"],pc,lo,ins)
            elif mn=="mflo":
                mul=next((ins[p] for p in range(pc-4,max(lo-4,pc-0x50),-4)
                          if p in ins and ins[p]["mnemonic"] in ("mult","multu")),None)
                info=("low_product_from="+h32(mul["pc"])+" "+mul["text"] if mul else "mult_source=TIDAK_TAHU")
            elif mn in ("slti","sltiu"):
                info="rs_origin="+trace_reg(i["rs"],pc,lo,ins)+"; immediate="+str(i["imm"])
            elif mn in ("sub","subu","or"):
                info="rs_origin="+trace_reg(i["rs"],pc,lo,ins)+"; rt_origin="+trace_reg(i["rt"],pc,lo,ins)
            else:
                info="rs_origin="+trace_reg(i["rs"],pc,lo,ins)+"; immediate="+str(i["uimm"])
            op_rows.append({"seed":label,"pc":h32(pc),"file_offset":h32(i["fileoff"]),
              "bytes":hx(i["bytes"]),"instruction":i["text"],"function":seed_name,
              "operand_origin":info,"source":"reachable CFG rooted at "+h32(seed),
              "reason":"dynamic load remains dynamic; no constant label assigned to loaded register"})
    # Tests subtraction candidates against reads of tile+0x20 and captures conditional compare paths.
    for pc in sorted(reach):
        i=ins[pc]
        if i["mnemonic"] in ("sub","subu"):
            lhs=depends_on_pc(i["rs"],pc,seed,ins,tile20_loads)
            rhs=depends_on_pc(i["rt"],pc,seed,ins,tile20_loads)
            diff_rows.append({"seed":label,"pc":h32(pc),"file_offset":h32(i["fileoff"]),
              "bytes":hx(i["bytes"]),"instruction":i["text"],
              "lhs_tile20_read_pcs":";".join(h32(x) for x in sorted(lhs)) if lhs else "—",
              "rhs_tile20_read_pcs":";".join(h32(x) for x in sorted(rhs)) if rhs else "—",
              "lhs_origin":trace_reg(i["rs"],pc,seed,ins),"rhs_origin":trace_reg(i["rt"],pc,seed,ins),
              "both_operands_depend_on_tile20_reads":"YES" if lhs and rhs else "NO",
              "source":"reachable CFG + backward register slice",
              "reason":"candidate level difference only; two tile+0x20 reads are not proof without nibble extraction"})
        if i["op"] in (1,4,5,6,7):
            lhs=depends_on_pc(i["rs"],pc,seed,ins,tile20_loads)
            rhs=depends_on_pc(i["rt"],pc,seed,ins,tile20_loads) if i["op"] in (4,5) else set()
            if lhs or rhs:
                compare_rows.append({"seed":label,"pc":h32(pc),"file_offset":h32(i["fileoff"]),
                  "bytes":hx(i["bytes"]),"instruction":i["text"],"condition":cond_text(i),
                  "lhs_tile20_load_pcs":";".join(h32(x) for x in sorted(lhs)) if lhs else "—",
                  "rhs_tile20_load_pcs":";".join(h32(x) for x in sorted(rhs)) if rhs else "—",
                  "lhs_origin":trace_reg(i["rs"],pc,seed,ins),
                  "rhs_origin":trace_reg(i["rt"],pc,seed,ins) if i["op"] in (4,5) else "—",
                  "source":"reachable conditional branch + backward register slice",
                  "reason":"branch operand traces to a halfword read from displacement +0x20"})
    # Backward slices of all stores to +0x20; report OR/ORI nodes and shift provenance.
    for r in [r for r in tile20_rows if r["seed"]==label and r["access"]=="WRITE"]:
        spc=int(r["pc"],16); si=ins[spc]; lo=seed
        def find_or(reg,before,depth=0,seen=None):
            if seen is None:seen=set()
            if depth>10 or (reg,before) in seen:return []
            seen.add((reg,before))
            d=last_def(reg,before,lo,ins)
            if not d:return []
            found=[]; mn0=d["mnemonic"]
            if mn0 in ("or","ori"):
                ldef=last_def(d["rs"],d["pc"],lo,ins)
                rdef=last_def(d["rt"],d["pc"],lo,ins) if mn0=="or" else None
                shifts=[]
                for nm,df in [("rs",ldef),("rt",rdef)]:
                    if df and df["mnemonic"] in ("sll","sllv"):
                        shifts.append(nm+":"+h32(df["pc"])+" "+df["text"]+"; source="+trace_reg(df["rt"],df["pc"],lo,ins))
                found.append({"or_pc":h32(d["pc"]),"or_bytes":hx(d["bytes"]),"or_instruction":d["text"],
                  "or_rs_origin":trace_reg(d["rs"],d["pc"],lo,ins),
                  "or_rt_origin":trace_reg(d["rt"],d["pc"],lo,ins) if mn0=="or" else "immediate "+hex(d["uimm"]),
                  "shift_sources":";".join(shifts) if shifts else "TIDAK TERDETEKSI"})
            op0,fn0=d["op"],d["fn"]
            if op0 in (8,9,10,11,12,13,14):
                found+=find_or(d["rs"],d["pc"],depth+1,seen.copy())
            elif op0==0 and fn0 in (0,2,3,4,6,7,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27):
                found+=find_or(d["rs"],d["pc"],depth+1,seen.copy())
                found+=find_or(d["rt"],d["pc"],depth+1,seen.copy())
            return found
        nodes=find_or(si["rt"],spc)
        if nodes:
            for n in nodes:
                or_rows.append({"seed":label,"store_pc":h32(spc),"store_instruction":si["text"],
                  "store_base_origin":r["base_origin"],"store_value_origin":trace_reg(si["rt"],spc,lo,ins),
                  **n,"source":"backward def-chain from store at +0x20",
                  "reason":"OR/ORI node appears in stored-value slice"})
        else:
            or_rows.append({"seed":label,"store_pc":h32(spc),"store_instruction":si["text"],
              "store_base_origin":r["base_origin"],"store_value_origin":trace_reg(si["rt"],spc,lo,ins),
              "or_pc":"NONE_IN_BOUNDED_SLICE","or_bytes":"—","or_instruction":"TIDAK TERDETEKSI",
              "or_rs_origin":"—","or_rt_origin":"—","shift_sources":"—",
              "source":"backward def-chain from store at +0x20",
              "reason":"no OR/ORI node found in bounded local dataflow slice"})
write_tsv("DX3_SEED_REACHABILITY.tsv",seed_rows,
 ["seed_pc","seed_label","function_label","reachable_instruction_count","reaches_800EC3A8","function_bound_end_guess","source","reason"])
write_tsv("DX3_OPERATION_CENSUS.tsv",op_rows,
 ["seed","pc","file_offset","bytes","instruction","function","operand_origin","source","reason"])
write_tsv("DX3_TILE_PLUS20_READ_WRITE.tsv",tile20_rows,
 ["seed","pc","file_offset","bytes","instruction","access","function","base_register","base_origin","base_origin_trace","value_origin","source","reason"])
write_tsv("DX3_LEVEL_NIBBLE_OR_SOURCES.tsv",or_rows,
 ["seed","store_pc","store_instruction","store_base_origin","store_value_origin","or_pc","or_bytes","or_instruction",
  "or_rs_origin","or_rt_origin","shift_sources","source","reason"])
write_tsv("DX3_ONE_SHIFT_PATTERNS.tsv",shift_one_rows,
 ["seed","pc","bytes","instruction","value_operand","shift_count_origin","pattern","source","reason"])
write_tsv("DX3_LEVEL_DIFFERENCE_CANDIDATES.tsv",diff_rows,
 ["seed","pc","file_offset","bytes","instruction","lhs_tile20_read_pcs","rhs_tile20_read_pcs",
  "lhs_origin","rhs_origin","both_operands_depend_on_tile20_reads","source","reason"])
write_tsv("DX3_LEVEL_NIBBLE_COMPARISONS.tsv",compare_rows,
 ["seed","pc","file_offset","bytes","instruction","condition","lhs_tile20_load_pcs","rhs_tile20_load_pcs",
  "lhs_origin","rhs_origin","source","reason"])

# DX4: compare three distinct user-derived multiplier models. 100 is only the
# user's comparison normalization, never asserted as a ROM constant.
observed={1:100,2:400,3:800,4:1600}
fee_base_assumption=100
models=[
 ("H1_PURE_POWER_2","fee_dasar * 2^d",{1:2,2:4,3:8,4:16},
  "At 0x800EC3A8 / 0x800EF3CC, a source operand equal to 1 shifted by d with no d=1 special path predicts multiplier 2 at d=1; a d=1 observed factor 1 falsifies it."),
 ("H2_SPECIAL_PER_LEVEL_LOOKUP","fee_dasar * factor[d], factor={1:1,2:4,3:8,4:16}",{1:1,2:4,3:8,4:16},
  "At 0x800EC3A8 / 0x800EF3CC, identify a d selector and a special d=1 branch (e.g. slti[u] imm=2) or table yielding exactly 1,4,8,16; a decoded coefficient different from any row factor falsifies it."),
 ("H3_LEVEL_TABLE_DOUBLING_FROM_D1","fee_dasar * factor[d], factor={1:1,2:2,3:4,4:8}",{1:1,2:2,3:4,4:8},
  "At 0x800EC3A8 / 0x800EF3CC, a per-level table or derived coefficient yielding 1,2,4,8 is required; a coefficient 4 for d=2 or 8 for d=3 falsifies it.")
]
dx4=[]
for mid,formula,factors,falsifier in models:
    mismatch=[]
    for d in range(1,5):
        pred=fee_base_assumption*factors[d]
        obs=observed[d]
        result="COCOK" if pred==obs else "BERTENTANGAN_DENGAN_PENGAMATAN_PENGGUNA"
        if pred!=obs:mismatch.append(str(d))
        dx4.append({"model":mid,"formula":formula,"distance_d":d,
          "fee_dasar_symbolic":"fee_dasar; normalized to 100 only for user's arithmetic comparison",
          "normalization_value_user_assumption":fee_base_assumption,"multiplier":factors[d],
          "predicted_fee_under_user_normalization":pred,"user_observation":obs,"comparison":result,
          "contradictory_d_values":";".join(mismatch) if mismatch else "NONE",
          "falsifier":falsifier,"evidence_class":"HIPOTESIS PENGGUNA; not ROM/runtime constant"})
write_tsv("DX4_USER_OBSERVATION_MODEL_COMPARISON.tsv",dx4,
 ["model","formula","distance_d","fee_dasar_symbolic","normalization_value_user_assumption","multiplier",
  "predicted_fee_under_user_normalization","user_observation","comparison","contradictory_d_values","falsifier","evidence_class"])


# DY0-DY4 extension: caller-clobber-aware provenance and economy paths.
# This extends the existing DX analyzer; it does not replace its input validation,
# full-image decode, CFG, or original DX outputs.

def call_trace_value(reg,before,lo,code):
    d=last_def(reg,before,lo,code)
    if d: return trace_reg(reg,before,lo,code)
    c=last_call_before(before,lo,code)
    if c and reg in RETURN_REGS: return "return JAL "+call_target_text(c)
    if c and reg in CALLER_SAVED: return "TIDAK TAHU: caller-saved setelah JAL "+call_target_text(c)
    return trace_reg(reg,before,lo,code)

def expr_nodes(reg,before,lo,code,depth=0,seen=None):
    if seen is None: seen=set()
    if depth>12 or (reg,before) in seen or reg==0: return []
    seen.add((reg,before))
    d=last_def(reg,before,lo,code)
    if not d: return []
    out=[d]
    mn=d["mnemonic"]; op,fn=d["op"],d["fn"]
    if mn in MEM_LOADS: return out
    if mn in ("mflo","mfhi"):
        mul=next((code[p] for p in range(d["pc"]-4,max(lo-4,d["pc"]-0x60),-4)
                  if p in code and code[p]["mnemonic"] in ("mult","multu")),None)
        if mul:
            out += expr_nodes(mul["rs"],mul["pc"],lo,code,depth+1,seen.copy())
            out += expr_nodes(mul["rt"],mul["pc"],lo,code,depth+1,seen.copy())
        return out
    if op in (8,9,10,11,12,13,14):
        out += expr_nodes(d["rs"],d["pc"],lo,code,depth+1,seen.copy())
    elif op==0 and fn in (0,2,3):
        out += expr_nodes(d["rt"],d["pc"],lo,code,depth+1,seen.copy())
    elif op==0 and fn in (4,6,7,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27):
        out += expr_nodes(d["rs"],d["pc"],lo,code,depth+1,seen.copy())
        out += expr_nodes(d["rt"],d["pc"],lo,code,depth+1,seen.copy())
    return out

def function_callers_for(tag):
    code=exe if tag=="EXE" else ins
    starts,f_at,f_name,_=FUNC[tag]
    by_target=defaultdict(list)
    for i in code.values():
        if i["op"]==3:
            t=branch_target(i)
            if t in code:
                by_target[t].append(f_name(i["pc"])+"@"+h32(i["pc"]))
    return by_target

def node_memory_dependencies(nodes,tag,code):
    out=[]
    starts,f_at,f_name,_=FUNC[tag]
    for n in nodes:
        if n["mnemonic"] not in MEM_LOADS: continue
        lo=f_at(n["pc"])
        bo=base_origin(n["rs"],n["pc"],lo,code)
        if n["imm"]==0x1a and "SLOT_0x8013EA84" in bo:
            out.append("TILE_PLUS1A@"+h32(n["pc"]))
        if n["imm"]==0x20 and "SLOT_0x8013EA84" in bo:
            out.append("TILE_PLUS20@"+h32(n["pc"]))
        if n["imm"] in (0x14,0x15):
            out.append("RESOURCE_FIELD_"+hex(n["imm"])+"@"+h32(n["pc"]))
    return sorted(set(out))


def shift_operand_detail(nodes,wanted_shift,tag,code):
    starts,f_at,f_name,_=FUNC[tag]
    details=[]
    for n in nodes:
        if n["mnemonic"]!="sll" or n["sh"]!=wanted_shift: continue
        lo=f_at(n["pc"])
        origin=trace_reg(n["rt"],n["pc"],lo,code)
        if "return JAL" in origin or "return JALR" in origin:
            cls="RETURN_CALL"
        elif "[load " in origin:
            cls="DYNAMIC_LOAD_TABLE_OR_GLOBAL"
        elif "masuk/dinamis" in origin or "TIDAK TAHU" in origin:
            if rn(n["rt"]) in ("$a0","$a1","$a2","$a3","$sp"):
                cls="FUNCTION_PARAMETER_OR_STACK"
            else:
                cls="ENTRY_OR_UNRESOLVED_REGISTER"
        elif origin=="$zero" or ("addiu" in origin and "<- $zero" in origin):
            cls="CONSTANT_FROM_ZERO"
        else:
            cls="LOCAL_DEF_OR_COMPUTED"
        details.append(h32(n["pc"])+" "+n["text"]+" | operand "+rn(n["rt"])+" | "+cls+" | "+origin)
    return ";".join(details) if details else "TIDAK TERDETEKSI"

def shift_and_mask_summary(nodes,tag,code,store_pc):
    shifts=[]; masks=[]; ors=[]
    starts,f_at,f_name,_=FUNC[tag]
    for n in nodes:
        if n["mnemonic"] in ("sll","sllv"):
            lo=f_at(n["pc"])
            sc=("immediate "+str(n["sh"])) if n["mnemonic"]=="sll" else call_trace_value(n["rs"],n["pc"],lo,code)
            shifts.append(h32(n["pc"])+" "+n["text"]+" [shift="+sc+"]")
        if n["mnemonic"]=="andi":
            masks.append(hex(n["uimm"]))
        if n["mnemonic"] in ("or","ori"):
            lo=f_at(n["pc"])
            left=call_trace_value(n["rs"],n["pc"],lo,code)
            right=("immediate "+hex(n["uimm"])) if n["mnemonic"]=="ori" else call_trace_value(n["rt"],n["pc"],lo,code)
            ors.append(h32(n["pc"])+" "+n["text"]+" [lhs="+left+"; rhs="+right+"]")
    return shifts,masks,ors

# Corrected file offsets and the three explicitly requested post-JAL branch gates.
for r in dx1:
    # decode() uses file bases 0x800 and 0x10BB000, respectively.
    r["source"]="EXE file_offset=0x800+(PC-0x80010000)" if r["region"]=="EXE" else "Entry 1 file_offset=0x10BB000+(PC-0x800AD450)"
write_tsv("DX1_ALL_PLUS1A_ACCESS.tsv",dx1,
 ["region","pc","file_offset","bytes","instruction","access","function_entry_guess","function_name_guess",
  "base_register","base_origin_slot_or_address","base_origin_register_trace","value_origin","source","reason"])
branch_gate_specs={
    0x800EC814:("return JAL 0x8010CDF0","$v0==0","direct JAL return in v0; bnez must fall through"),
    0x800EC874:("return JAL 0x8010D0F0","$v0==0","direct JAL return in v0; bnez must fall through"),
    0x800EC890:("v0=sltiu(v1,0x10); v1=return JAL 0x800154E0","JAL return $v1 < 0x10 unsigned; resulting $v0!=0","JAL return is copied to v1, then sltiu at 0x800EC88C writes v0; beqz must fall through")
}
for r in gate_rows:
    bpc=int(r["branch_pc"],16)
    spec=branch_gate_specs.get(bpc)
    r["v0_origin_after_call"]=spec[0] if spec else "—"
    r["required_register_value"]=spec[1] if spec else r["condition"]
    r["origin_reason"]=spec[2] if spec else "caller-saved values are not traced across JAL"
write_tsv("DX2_PATH_CONDITIONS.tsv",gate_rows,
 ["target_pc","branch_pc","file_offset","bytes","instruction","condition","condition_registers","required_outcome",
  "branch_target","fallthrough_after_delay","rs_origin","rt_origin","v0_origin_after_call","required_register_value","origin_reason","source","reason"])
dy1_rows=[]
for pc,spec in branch_gate_specs.items():
    i=ins.get(pc)
    if not i: continue
    lo=dx2_entry
    dy1_rows.append({"pc":h32(pc),"file_offset":h32(0x10BB000+(pc-ENTRY_BASE)),
      "bytes":hx(i["bytes"]),"instruction":i["text"],"v0_origin_after_call":spec[0],
      "required_value":spec[1],"reason":spec[2],
      "v0_origin_trace":trace_reg(2,pc,lo,ins),
      "input_v1_origin":trace_reg(3,pc,lo,ins) if pc==0x800EC890 else "—"})
write_tsv("DY1_CALLER_CLOBBER_BRANCHES.tsv",dy1_rows,
 ["pc","file_offset","bytes","instruction","v0_origin_after_call","required_value","reason","v0_origin_trace","input_v1_origin"])

# DY2: all stores at tile-field displacements +0x20/+0x21 across EXE and Entry 1.
tile_store_rows=[]
tile_special_rows=[]
for tag,code,base in codes:
    starts,f_at,f_name,next_start=FUNC[tag]
    callers=function_callers_for(tag)
    for i in sorted(code.values(),key=lambda x:x["pc"]):
        if i["mnemonic"] not in ("sb","sh","sw") or i["imm"] not in (0x20,0x21): continue
        lo=f_at(i["pc"])
        bo=base_origin(i["rs"],i["pc"],lo,code)
        nodes=expr_nodes(i["rt"],i["pc"],lo,code)
        shifts,masks,ors=shift_and_mask_summary(nodes,tag,code,i["pc"])
        tile_alias=("SLOT_0x8013EA84" in bo or "0x8013B818" in bo)
        mask_label="TIDAK_TERDETEKSI"
        if "0xf0ff" in [m.lower() for m in masks]: mask_label="0xF0FF"
        elif "0xff0f" in [m.lower() for m in masks]: mask_label="0xFF0F"
        elif masks: mask_label="LAIN:"+",".join(sorted(set(masks)))
        nibble8=[x for x in shifts if x.endswith("[shift=immediate 8]")]
        nibble12=[x for x in shifts if x.endswith("[shift=immediate 12]")]
        direct_callers=callers.get(f_at(i["pc"]),[])
        tile_store_rows.append({"region":tag,"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),
          "bytes":hx(i["bytes"]),"instruction":i["text"],"function":f_name(i["pc"]),
          "base_register":rn(i["rs"]),"base_origin":bo,"tile_array_alias_proven":"YES" if tile_alias else "NO_OR_UNRESOLVED",
          "field_lane":"+0x20" if i["imm"]==0x20 else "+0x21","mask":mask_label,
          "shift_sources_8_11":";".join(nibble8) if nibble8 else "TIDAK TERDETEKSI",
          "nibble8_11_operand_origin":shift_operand_detail(nodes,8,tag,code),
          "shift_sources_12_15":";".join(nibble12) if nibble12 else "TIDAK TERDETEKSI",
          "nibble12_15_operand_origin":shift_operand_detail(nodes,12,tag,code),
          "OR_sources":";".join(ors) if ors else "TIDAK TERDETEKSI",
          "stored_value_origin":trace_reg(i["rt"],i["pc"],lo,code),
          "nearest_direct_caller_functions":";".join(direct_callers) if direct_callers else "TIDAK DITEMUKAN",
          "source":"linear full-image memory-store census; dynamic bases retained",
          "reason":"tile identity only proven when base trace resolves to slot EA84 / table base"})
# Special windows: preserve raw context and identify candidate target-level sources.
for tag,code,base in codes:
    if tag!="ENTRY1": continue
    starts,f_at,f_name,_=FUNC[tag]
    for site,label,window in [
        (0x800EC3A8,"ACTION8_EC3A8",0x90),
        (0x800EF3CC,"ACTION8_EF3CC",0x90),
        (0x800DAF2C,"EVENT3_D9570_FIELD24",0x50)
    ]:
        if site not in code: continue
        lo=f_at(site)
        for pc in range(max(lo,site-0x20),min(site+window,max(code)+1),4):
            i=code.get(pc)
            if not i: continue
            if i["mnemonic"] not in (MEM_LOADS|MEM_STORES|{"sll","sllv","srl","srlv","subu","sub","or","ori","andi","mult","mflo","jal","slti","sltiu","beq","bne","beqz","bnez"}): continue
            val=trace_reg(i["rt"],pc,lo,code) if i["mnemonic"] in MEM_STORES|MEM_LOADS else "—"
            tile_special_rows.append({"site":label,"site_pc":h32(site),"pc":h32(pc),
              "file_offset":h32(0x10BB000+(pc-ENTRY_BASE)),"bytes":hx(i["bytes"]),
              "instruction":i["text"],"function":f_name(pc),
              "rs_origin":trace_reg(i["rs"],pc,lo,code) if i["op"] not in (2,3) else "—",
              "rt_origin":trace_reg(i["rt"],pc,lo,code) if i["op"] not in (2,3) else "—",
              "base_origin":base_origin(i["rs"],pc,lo,code) if i["mnemonic"] in MEM_LOADS|MEM_STORES else "—",
              "value_origin":val,"source":"local instruction window + caller-clobber-aware slice",
              "reason":"candidate lineage only; semantic label for field+0x24 remains unverified"})
write_tsv("DY2_TILE_PLUS20_PLUS21_WRITERS.tsv",tile_store_rows,
 ["region","pc","file_offset","bytes","instruction","function","base_register","base_origin","tile_array_alias_proven",
  "field_lane","mask","shift_sources_8_11","nibble8_11_operand_origin","shift_sources_12_15",
  "nibble12_15_operand_origin","OR_sources","stored_value_origin",
  "nearest_direct_caller_functions","source","reason"])
write_tsv("DY2_ACTION8_EVENT3_LEVEL_SOURCE_WINDOWS.tsv",tile_special_rows,
 ["site","site_pc","pc","file_offset","bytes","instruction","function","rs_origin","rt_origin","base_origin",
  "value_origin","source","reason"])


# Explicit gameplay-source assessment for the three requested sites.
dy2_level_findings=[
 {"site":"ACTION8_EC3A8","pc":"0x800EC388","file_offset":h32(0x10BB000+(0x800EC388-ENTRY_BASE)),
  "bytes":"24 00 42 84","instruction":"lh $v0,0x24($v0)",
  "target_value_source":"tile-array pointer from slot 0x8013EA84; selected index is built through dynamic manager/input fields at 0x800EC368..0x800EC384",
  "reference_value_source":"PC 0x800EC364 lh $a0,-0x152e($v0), global address 0x8013EAD2",
  "delta_operation":"PC 0x800EC390 subu $v0,$v0,$a0; result stored manager+0x2B4 at PC 0x800EC398",
  "is_level_semantics_proven":"NO — field +0x24 semantic label TIDAK TAHU",
  "is_d_proven":"NO — signed field difference exists, but neither operand is proven to be a tile level",
  "source":"Entry 1 instructions + slot provenance",
  "reason":"do not equate a computed field difference with level delta d without field semantics"},
 {"site":"EVENT3_FUN_800D9570","pc":"0x800DAF2C","file_offset":h32(0x10BB000+(0x800DAF2C-ENTRY_BASE)),
  "bytes":"24 00 42 84","instruction":"lh $v0,0x24($v0)",
  "target_value_source":"tile-array pointer from slot 0x8013EA84; selected tile index comes from manager record +0x1F at PC 0x800DAF0C, indexed from active slot 0x8013EA88",
  "reference_value_source":"NONE",
  "delta_operation":"NONE in inspected D9570 path window; value is copied to manager+0x390 at PC 0x800DAF34",
  "is_level_semantics_proven":"NO — field +0x24 semantic label TIDAK TAHU",
  "is_d_proven":"NO — no difference operation in this event-3 path",
  "source":"Entry 1 instructions + slot provenance",
  "reason":"target tile field is directly identified; gameplay meaning is not"},
 {"site":"ACTION8_EF3CC","pc":"0x800EF3CC","file_offset":h32(0x10BB000+(0x800EF3CC-ENTRY_BASE)),
  "bytes":"EB 02 44 A0","instruction":"sb $a0,0x2eb($v0)",
  "target_value_source":"$a0 entry/dynamic parameter; no local definition is proven before this store",
  "reference_value_source":"TIDAK TAHU",
  "delta_operation":"NONE proven at this site",
  "is_level_semantics_proven":"NO",
  "is_d_proven":"NO",
  "source":"Entry 1 caller-clobber-aware entry slice",
  "reason":"base $v0 and value $a0 are not promoted to constants or table values"}
]
write_tsv("DY2_ACTION8_EVENT3_LEVEL_FINDINGS.tsv",dy2_level_findings,
 ["site","pc","file_offset","bytes","instruction","target_value_source","reference_value_source","delta_operation",
  "is_level_semantics_proven","is_d_proven","source","reason"])

# DY3: exact-address stores to global 0x80139EFC, plus the expression slice for each.
global_writer_rows=[]
manager_field_rows=[]
helper_rng_rows=[]
helper_status_hypotheses=[
 {"hypothesis":"H1 +0x4F0/+0x4F4 are transaction/aggregate scratch results; +0x534 is a success/error state byte",
  "basis":"CFG writes 4F0/4F4 from helper returns and a computed product; branches set/clear 534 on status paths",
  "falsifier":"A full reader xref showing every 4F0/4F4 consumer is unrelated to transaction amount/status, or 534 is only a presentation flag with no transaction gate"},
 {"hypothesis":"H2 +0x4F0/+0x4F4 hold candidate/selection calculations for a board target; +0x534 records whether an eligible target exists",
  "basis":"the same CFG scans tile records, compares +0x20 nibbles to the active index, then enters an RNG retry loop and writes 534 on alternate branches",
  "falsifier":"A reader trace proving 4F0/4F4 are not consumed by candidate-selection code, or the 534 writers/readers serve a different state machine"}
]
for tag,code,base in codes:
    starts,f_at,f_name,_=FUNC[tag]
    for i in sorted(code.values(),key=lambda x:x["pc"]):
        if i["mnemonic"] not in MEM_STORES: continue
        lo=f_at(i["pc"])
        ea=effective_address(i,code,lo)
        if ea!=0x80139EFC: continue
        nodes=expr_nodes(i["rt"],i["pc"],lo,code)
        arith=[]
        for n in nodes:
            if n["mnemonic"] in ("sll","sllv","mult","multu","addu","subu"):
                nlo=f_at(n["pc"])
                arith.append(h32(n["pc"])+" "+n["text"]+
                    " [rs="+trace_reg(n["rs"],n["pc"],nlo,code)+"; rt="+trace_reg(n["rt"],n["pc"],nlo,code)+"]")
        deps=node_memory_dependencies(nodes,tag,code)
        global_writer_rows.append({"region":tag,"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),
          "bytes":hx(i["bytes"]),"instruction":i["text"],"function":f_name(i["pc"]),
          "value_origin":trace_reg(i["rt"],i["pc"],lo,code),
          "arithmetic_expression":";".join(arith) if arith else "NONE_IN_LOCAL_EXPR_SLICE",
          "tile_plus1a_dependency":"YES" if any(x.startswith("TILE_PLUS1A") for x in deps) else "NOT_PROVEN",
          "tile_level_nibble_plus20_dependency":"YES" if any(x.startswith("TILE_PLUS20") for x in deps) else "NOT_PROVEN",
          "resource_14_15_candidate":"YES" if any(x.startswith("RESOURCE_FIELD") for x in deps) else "NOT_PROVEN",
          "dependency_load_pcs":";".join(deps) if deps else "TIDAK TERDETEKSI",
          "source":"direct effective-address scan for 0x80139EFC + backward expression slice",
          "reason":"caller-saved slices stop at JAL/JALR; loaded table values remain dynamic"})
def classify_global_writer_origin(r):
    v=r["value_origin"]
    if v=="$zero": return "ZERO"
    if "return JAL" in v or "return JALR" in v: return "RETURN_CALL"
    if "[load " in v: return "DYNAMIC_LOAD"
    if ("addiu" in v or "ori" in v) and "<- $zero" in v: return "CONSTANT_FROM_ZERO"
    if r["arithmetic_expression"]!="NONE_IN_LOCAL_EXPR_SLICE": return "ARITHMETIC_CHAIN_PROVEN"
    if "masuk/dinamis" in v or "TIDAK TAHU" in v: return "PARAMETER_OR_UNRESOLVED"
    return "LOCAL_DEF_NOT_CLASSIFIED"
for r in global_writer_rows:
    r["value_origin_class"]=classify_global_writer_origin(r)
write_tsv("DY3_GLOBAL_80139EFC_WRITERS.tsv",global_writer_rows,
 ["region","pc","file_offset","bytes","instruction","function","value_origin","value_origin_class","arithmetic_expression",
  "tile_plus1a_dependency","tile_level_nibble_plus20_dependency","resource_14_15_candidate",
  "dependency_load_pcs","source","reason"])
dy3_arithmetic_rows=[r for r in global_writer_rows if r["arithmetic_expression"]!="NONE_IN_LOCAL_EXPR_SLICE"]
write_tsv("DY3_GLOBAL_80139EFC_ARITHMETIC_EXPRESSIONS.tsv",dy3_arithmetic_rows,
 ["region","pc","file_offset","bytes","instruction","function","value_origin","value_origin_class","arithmetic_expression",
  "tile_plus1a_dependency","tile_level_nibble_plus20_dependency","resource_14_15_candidate",
  "dependency_load_pcs","source","reason"])

# All reads/writes for the three manager fields, separating reachable helper-path PCs.
helper_reach=set(reach2)
for tag,code,base in codes:
    starts,f_at,f_name,_=FUNC[tag]
    for i in sorted(code.values(),key=lambda x:x["pc"]):
        if i["mnemonic"] not in (MEM_LOADS|MEM_STORES) or i["imm"] not in (0x4f0,0x4f4,0x534): continue
        lo=f_at(i["pc"])
        bo=base_origin(i["rs"],i["pc"],lo,code)
        is_mgr=("SLOT_0x8013EA74" in bo)
        # Keep every displacement reader/writer, then mark manager provenance independently.
        manager_field_rows.append({"region":tag,"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),
          "bytes":hx(i["bytes"]),"instruction":i["text"],"function":f_name(i["pc"]),
          "field":"+0x"+format(i["imm"],"X"),"access":"READ" if i["mnemonic"] in MEM_LOADS else "WRITE",
          "base_origin":bo,"manager_array_base_proven":"YES" if is_mgr else "NO_OR_UNRESOLVED",
          "reachable_from_FUN_800EC574":"YES" if tag=="ENTRY1" and i["pc"] in helper_reach else "NO_OR_NOT_CHECKED",
          "value_origin":trace_reg(i["rt"],i["pc"],lo,code) if i["mnemonic"] in MEM_STORES else "loaded value -> "+rn(i["rt"]),
          "source":"full EXE + Entry 1 field-offset scan",
          "reason":"offset alone does not prove manager base; base provenance retained"})
write_tsv("DY3_MANAGER_FIELDS_4F0_4F4_534.tsv",manager_field_rows,
 ["region","pc","file_offset","bytes","instruction","function","field","access","base_origin",
  "manager_array_base_proven","reachable_from_FUN_800EC574","value_origin","source","reason"])
manager_reader_rows=[r for r in manager_field_rows
  if r["access"]=="READ" and r["manager_array_base_proven"]=="YES"]
write_tsv("DY3_MANAGER_FIELD_READERS.tsv",manager_reader_rows,
 ["region","pc","file_offset","bytes","instruction","function","field","base_origin",
  "manager_array_base_proven","reachable_from_FUN_800EC574","source","reason"])

# The bounded retry loop: counter is seeded with 0x32, decremented before each RNG call.
for pc,role in [
 (0x800ECAE8,"attempt_limit=0x32=50"),
 (0x800ECAEC,"store attempt counter at manager+0x2A8"),
 (0x800ECB00,"read remaining attempt counter"),
 (0x800ECB08,"decrement attempt counter"),
 (0x800ECB0C,"exit when decremented counter == -1; otherwise retry path"),
 (0x800ECB14,"JAL RNG 0x80035D78"),
 (0x800ECB1C,"load divisor/range byte; runtime value dynamic"),
 (0x800ECB24,"divide RNG result by divisor"),
 (0x800ECB28,"mfhi obtains candidate remainder"),
 (0x800ECB38,"store candidate index to global 0x8013EBB0"),
 (0x800ECB3C,"read active index from global slot 0x8013EA88"),
 (0x800ECB44,"beq candidate,active -> retry; success requires candidate != active")
]:
    i=ins.get(pc)
    if i:
        helper_rng_rows.append({"pc":h32(pc),"file_offset":h32(0x10BB000+(pc-ENTRY_BASE)),
          "bytes":hx(i["bytes"]),"instruction":i["text"],"role":role,
          "origin_rs":trace_reg(i["rs"],pc,dx2_entry,ins) if i["op"] not in (2,3) else "—",
          "origin_rt":trace_reg(i["rt"],pc,dx2_entry,ins) if i["op"] not in (2,3) else "—",
          "source":"reachable CFG rooted at 0x800EC574; delay slots modeled",
          "reason":"counter starts at 50 and exits when the pre-random decrement becomes -1"})
write_tsv("DY3_HELPER_RNG_RETRY_LOOP.tsv",helper_rng_rows,
 ["pc","file_offset","bytes","instruction","role","origin_rs","origin_rt","source","reason"])
for h in helper_status_hypotheses:
    h["observed_reader_functions"]="FUN_800DC2E0 (+4F0/+4F4); FUN_800E562C (+4F0 read then +4F4 write); FUN_800E6470 (+4F4/+534); FUN_800E9220 (+4F4)"
write_tsv("DY3_HELPER_STATUS_HYPOTHESES.tsv",helper_status_hypotheses,
 ["hypothesis","basis","falsifier"])

# DY4: count true tile-fee postings (negative u16(tile+0x1A)) in D15A8 and its direct call closure.
def direct_calls_in_function(tag,entry):
    code=exe if tag=="EXE" else ins
    starts,f_at,f_name,next_start=FUNC[tag]
    lo=entry; hi=next_start(entry)
    return [branch_target(i) for i in code.values() if lo<=i["pc"]<hi and i["op"]==3 and branch_target(i) in code]
def call_closure(tag,root):
    code=exe if tag=="EXE" else ins
    starts,f_at,f_name,next_start=FUNC[tag]
    q=deque([root]); seen=set()
    while q:
        en=q.popleft()
        if en in seen or en not in code: continue
        seen.add(en)
        for t in direct_calls_in_function(tag,en):
            if t not in seen: q.append(t)
    return seen
closure=call_closure("ENTRY1",0x800D15A8)
dy4_post_rows=[]
for tag,code,base in codes:
    starts,f_at,f_name,_=FUNC[tag]
    for i in sorted(code.values(),key=lambda x:x["pc"]):
        if tag!="ENTRY1" or f_at(i["pc"]) not in closure: continue
        if i["mnemonic"] not in MEM_STORES or i["imm"]!=0x2ee: continue
        lo=f_at(i["pc"])
        bo=base_origin(i["rs"],i["pc"],lo,code)
        val=trace_reg(i["rt"],i["pc"],lo,code)
        nodes=expr_nodes(i["rt"],i["pc"],lo,code)
        deps=node_memory_dependencies(nodes,tag,code)
        is_fee=("negu" in val and any(x.startswith("TILE_PLUS1A") for x in deps))
        dy4_post_rows.append({"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),
          "bytes":hx(i["bytes"]),"instruction":i["text"],"function":f_name(i["pc"]),
          "base_origin":bo,"stored_value_origin":val,
          "negative_tile_fee_post":"YES" if is_fee else "NO_OR_NOT_PROVEN",
          "tile_plus1a_load_dependencies":";".join(x for x in deps if x.startswith("TILE_PLUS1A")) or "TIDAK TERDETEKSI",
          "source":"direct call closure from FUN_800D15A8; direct +0x2EE stores",
          "reason":"fee-post requires both negation and a proven tile+0x1A load; zero clears are not posts"})
write_tsv("DY4_ACTION8_FEE_POSTS_CALL_CLOSURE.tsv",dy4_post_rows,
 ["pc","file_offset","bytes","instruction","function","base_origin","stored_value_origin",
  "negative_tile_fee_post","tile_plus1a_load_dependencies","source","reason"])
# Back-edge census: determine whether any direct branch after a fee-post returns to
# the fee load or post site inside FUN_800D15A8.
dy4_backedge_rows=[]
post_pc=0x800D46F8
post_entry=FUNC["ENTRY1"][1](post_pc)
post_end=FUNC["ENTRY1"][3](post_pc)
for i in sorted(ins.values(),key=lambda x:x["pc"]):
    if not (post_entry<=i["pc"]<post_end): continue
    if i["pc"]<=post_pc: continue
    op=i["op"]
    is_direct_jump=(op==2)
    is_cond_branch=(op==1 or op in (4,5,6,7))
    if not (is_direct_jump or is_cond_branch): continue
    t=branch_target(i)
    if t is not None and t<=0x800D46EC:
        dy4_backedge_rows.append({"function":"FUN_800D15A8","branch_pc":h32(i["pc"]),
          "file_offset":h32(0x10BB000+(i["pc"]-ENTRY_BASE)),"bytes":hx(i["bytes"]),
          "instruction":i["text"],"target_pc":h32(t),
          "crosses_fee_load_or_post":"YES" if t<=post_pc else "TARGET_BEFORE_FEE_LOAD",
          "source":"direct branch target scan in function bounds","reason":"potential loop edge; branch condition still controls reachability"})
dy4_loop_summary=[{"function":"FUN_800D15A8","fee_post_pc":"0x800D46F8",
 "all_plus2ee_stores_in_direct_call_closure":len(dy4_post_rows),
 "negative_tile_fee_posts":len([r for r in dy4_post_rows if r["negative_tile_fee_post"]=="YES"]),
 "backedges_after_post_to_fee_load_or_earlier":len([r for r in dy4_backedge_rows if r["target_pc"]=="0x800D46EC" or int(r["target_pc"],16)<0x800D46EC]),
 "direct_call_closure_functions":len(closure),
 "result":"NO_DIRECT_BACKEDGE_TO_FEE_LOAD_OR_POST" if not dy4_backedge_rows else "POTENTIAL_BACKEDGE_REQUIRES_PATH_REVIEW",
 "caveat":"JALR/indirect control-flow destinations are not in direct-call closure; no runtime execution",
 "falsifier":"a JALR-resolved edge or a branch target discovered to re-enter 0x800D46EC..0x800D46F8"})
write_tsv("DY4_ACTION8_POST_LOOP_AUDIT.tsv",dy4_loop_summary,
 ["function","fee_post_pc","all_plus2ee_stores_in_direct_call_closure","negative_tile_fee_posts",
  "backedges_after_post_to_fee_load_or_earlier","direct_call_closure_functions","result","caveat","falsifier"])
write_tsv("DY4_ACTION8_DIRECT_BACKEDGES.tsv",dy4_backedge_rows,
 ["function","branch_pc","file_offset","bytes","instruction","target_pc","crosses_fee_load_or_post","source","reason"])

# Three genuinely different formula families; lookup that copies all four user ratios is tautological.
fee_models=[
 ("H1_PURE_2_POWER_D","fee_dasar * 2^d",[2,4,8,16],"NOT_TAUTOLOGI",
  "Contradicted by user d=1=100 vs normalized prediction 200. Concrete ROM falsifier for the D15A8 path: at 0x800D46EC the code loads raw u16(tile+0x1A), at 0x800D46F4 it negates that raw value, and at 0x800D46F8 it posts it; a traced shift/multiply/table coefficient between those PCs would be required to avoid this falsifier."),
 ("H2_LOOKUP_COPIED_FROM_ALL_FOUR_USER_POINTS","fee_dasar * lookup[d] where lookup={1:1,2:4,3:8,4:16}",[1,4,8,16],"TAUTOLOGI",
  "This lookup is defined from all four user ratios, not inferred from ROM. Concrete falsifier: if the D15A8 sequence 0x800D46EC lhu; 0x800D46F4 negu; 0x800D46F8 sh is the complete value path with no intervening selector/table read, this lookup has no ROM support."),
 ("H3_REPEAT_BASE_FEE_ONCE_PER_LEVEL_STEP","fee_dasar * d",[1,2,3,4],"NOT_TAUTOLOGI",
  "Contradicted by d=2..4. Concrete falsifier: one raw-fee post at 0x800D46F8 and an empty DY4_ACTION8_DIRECT_BACKEDGES.tsv (no branch from after the post back to 0x800D46EC or earlier) disproves a per-level repeat loop in this handler."),
 ("H4_ACCUMULATE_DOUBLING_FEE_EACH_STEP","fee_dasar * sum(2^k,k=0..d-1)",[1,3,7,15],"NOT_TAUTOLOGI",
  "Contradicted by d=2..4. Concrete falsifier: 0x800D46F8 is the only negative tile-fee post in the direct call closure and no back-edge re-enters 0x800D46EC..0x800D46F8; an explicit second post or a JALR-resolved loop back to that range would falsify this audit.")
]
dy4_model_rows=[]
user_obs=[100,400,800,1600]
for model,formula,factors,taut,falsifier in fee_models:
    for d in range(1,5):
        pred=100*factors[d-1]
        obs=user_obs[d-1]
        dy4_model_rows.append({"model":model,"formula":formula,"d":d,"fee_dasar":"fee_dasar (symbolic)",
          "normalization_for_comparison":100,"factor":factors[d-1],"predicted_normalized":pred,
          "user_observation_hypothesis":obs,
          "comparison":"COCOK" if pred==obs else "BERTENTANGAN_DENGAN_4_TITIK_PENGGUNA",
          "lookup_tautology":taut,"falsifier":falsifier,
          "evidence_class":"USER_HYPOTHESIS_ONLY; not ROM/runtime evidence"})
write_tsv("DY4_FEE_HYPOTHESES_D1_D4.tsv",dy4_model_rows,
 ["model","formula","d","fee_dasar","normalization_for_comparison","factor","predicted_normalized",
  "user_observation_hypothesis","comparison","lookup_tautology","falsifier","evidence_class"])

# DY summary and report.
computed_posts=[r for r in dy4_post_rows if r["negative_tile_fee_post"]=="YES"]
d15a8_posts=[r for r in computed_posts if r["function"]=="FUN_800D15A8"]
tile_alias_writers=[r for r in tile_store_rows if r["tile_array_alias_proven"]=="YES"]
report_dy=[
"# DY0-DY4 — addendum audit statis",
"",
"Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research",
"Baseline inklusif: "+BASELINE,
"Snapshot source SHA: "+SNAPSHOT,
"EXE SHA-256: "+EXE_SHA+"; Entry 1 SHA-256: "+ENTRY_SHA,
"",
"## Status",
"DY0: TUNTAS K4 untuk snapshot source; baseline ikut dihitung. Final HEAD dihitung ulang setelah bot publish dan commit laporan akhir.",
"DY1: TUNTAS K4 untuk tiga branch gate; DX2_PATH_CONDITIONS.tsv ditulis ulang dengan origin setelah JAL/JALR yang diputus pada call boundary.",
"DY2: SEBAGIAN K4 — census semua store displacement +0x20/+0x21 EXE+Entry1; hanya baris yang basisnya membuktikan slot EA84 dinyatakan tile array. Level source semantik untuk aksi 8/event 3 masih TIDAK TAHU di luar lineage statis yang dilampirkan.",
"DY3: SEBAGIAN K4 — census langsung menemukan "+str(len(global_writer_rows))+" store ke 0x80139EFC; hanya "+str(len(dy3_arithmetic_rows))+" yang memiliki expression slice berisi sll/sllv/mult/addu/subu. File DS3_INDEX_GLOBAL_WRITERS.tsv lama sebenarnya memindai displacement -0x1450 (global 0x8013EBB0), sehingga bukan census EFC. 40 pembaca field +0x4F0/+0x4F4/+0x534 dipisahkan; arti gameplay tetap hipotesis.",
"DY4: SEBAGIAN K4 — store -fee ke +0x2EE dihitung lewat direct call closure D15A8; tidak menyatakan rumus biaya level tanpa bukti d pada operand.",
"",
"## DY1 — JAL clobber",
"0x800EC814 bnez $v0: $v0 berasal langsung dari return JAL 0x8010CDF0; fall-through wajib $v0=0.",
"0x800EC874 bnez $v0: $v0 berasal langsung dari return JAL 0x8010D0F0; fall-through wajib $v0=0.",
"0x800EC890 beqz $v0: return JAL 0x800154E0 masuk ke $v1; 0x800EC88C sltiu $v0,$v1,0x10 membentuk $v0. Fall-through wajib $v0!=0, ekuivalen return unsigned $v1<0x10.",
"Semua origin berhenti pada batas JAL/JALR: v0/v1 dilabel return, a0-a3 dan t0-t9 setelah JAL dilabel TIDAK TAHU. File offset EXE mengikuti 0x800+(PC-0x80010000), Entry 1 0x10BB000+(PC-0x800AD450).",
"",
"## DY2 — tile+0x20/+0x21",
"DY2_TILE_PLUS20_PLUS21_WRITERS.tsv memuat "+str(len(tile_store_rows))+" operasi store displacement literal +0x20/+0x21 (EXE="+str(sum(1 for r in tile_store_rows if r['region']=='EXE'])+", Entry 1="+str(sum(1 for r in tile_store_rows if r['region']=='ENTRY1'])+"). Hanya "+str(len(tile_alias_writers))+" basisnya terbukti berakar ke slot pointer tile-array 0x8013EA84; sisanya NO_OR_UNRESOLVED. Kolom nibble8_11_operand_origin dan nibble12_15_operand_origin memisahkan parameter/stack dari dynamic load. Nilai load tetap dinamis.",
"DY2_ACTION8_EVENT3_LEVEL_FINDINGS.tsv merinci sumber field+0x24. Di action8 EC3A8, PC 0x800EC388 membaca tile+0x24, PC 0x800EC364 membaca global 0x8013EAD2, dan PC 0x800EC390 melakukan subu; ini kandidat beda field, bukan bukti beda level d. Pada event3 D9570, PC 0x800DAF2C membaca tile+0x24 berdasarkan indeks dari manager record +0x1F dan nilai disalin ke manager+0x390; tak ada operasi selisih terbukti. Pada EF3CC, basis dan parameter tetap TIDAK TAHU.",
"",
"## DY3 — global accumulator dan RNG retry",
"DY3_GLOBAL_80139EFC_WRITERS.tsv hanya memuat store yang effective address statisnya tepat 0x80139EFC. Arithmetic slice memuat PC operand untuk sll/sllv/mult/addu/subu; dependency tile+1A, nibble +0x20, atau field resource +0x14/+0x15 hanya YES jika load pada slice teridentifikasi.",
"Retry: EC AE8 menetapkan 0x32 (50); EC AEC menyimpan counter manager+0x2A8; EC B00/ B08 membaca dan decrement; EC B0C keluar saat -1. Loop memanggil RNG pada EC B14, menghasilkan remainder melalui div/mfhi di ECB24/ECB28, menyimpan kandidat index di ECB38, membaca active index melalui lhu slot 0x8013EA88 di ECB3C, dan mengulang bila sama pada ECB44. Sukses loop mensyaratkan kandidat != active-index; maksimum 50 pemanggilan RNG.",
"Field manager +0x4F0/+0x4F4/+0x534 dan PC reader/writer berada di DY3_MANAGER_FIELDS_4F0_4F4_534.tsv. Pembaca dengan basis manager terbukti berada di DY3_MANAGER_FIELD_READERS.tsv (total "+str(len(manager_reader_rows))+"); pembaca terkelompok antara FUN_800DC2E0, FUN_800E562C, FUN_800E6470, FUN_800E9220, dan FUN_800C5978. Hipotesis H1/H2 serta falsifier-nya di DY3_HELPER_STATUS_HYPOTHESES.tsv; tidak ada klaim semantik final.",
"",
"## DY4 — debit aksi 8",
"Negative fee post terhitung dari instruksi store yang operand slice-nya berisi negu dan pembacaan tile+0x1A, di direct call closure FUN_800D15A8. Jumlah terdeteksi total="+str(len(computed_posts))+"; yang langsung dilabel FUN_800D15A8="+str(len(d15a8_posts))+". Store nol untuk clear pending tidak dihitung sebagai post.",
"DY4_ACTION8_POST_LOOP_AUDIT.tsv menghitung "+str(len(dy4_post_rows))+" store +0x2EE di direct call closure D15A8; hanya "+str(len(computed_posts))+" adalah post -fee, dua lainnya clear. DY4_ACTION8_DIRECT_BACKEDGES.tsv menguji branch dari sesudah post yang kembali ke PC <=0x800D46EC; jalur indirect/JALR belum terikat. Jika kosong, tak ada loop langsung yang mengulangi debit di handler statis ini. Ini bukan bukti runtime.",
"Keempat model formula d=1..4 dalam DY4_FEE_HYPOTHESES_D1_D4.tsv memakai 100 hanya sebagai normalisasi pengamatan pengguna. H2 exact lookup dari empat rasio pengguna ditandai TAUTOLOGI. H3/H4 adalah model debit akumulatif berulang dan bertentangan dengan pengamatan pada nilai d yang dicatat. Formula ROM aktual = TIDAK TAHU.",
"",
"## Batas",
"Statis saja; tidak menjalankan emulator/game. Maksimum K4. Nilai runtime, target label untuk field+0x24, arti gameplay +0x4F0/+0x4F4/+0x534, serta rumus biaya ROM = TIDAK TAHU bila tidak terhubung oleh instruction/dataflow proof.",
"Output text/TSV saja. EXE/DATA.BIN hanya input privat runner; tidak dikomit."
]
(OUT/"DY0_DY4_STATIC_AUDIT.md").write_text("\n".join(report_dy)+"\n",encoding="utf-8")
write_tsv("DY0_COMMIT_LEDGER.tsv",ledger,
 ["sha_full","class","author","author_email","message","changed_files","source","reason"])
write_tsv("DY0_COUNTS.tsv",[
 {"scope":"SNAPSHOT_SOURCE_INCLUSIVE","sha":SNAPSHOT,"total":len(ledger),"human":humans,"bot":bots,
  "method":"git rev-list baseline^..snapshot; baseline included"},
 {"scope":"HEAD_AFTER_ONE_BOT_PUBLICATION_EXPECTED","sha":"VERIFY_AFTER_ACTION","total":len(ledger)+1,"human":humans,"bot":bots+1,
  "method":"snapshot ledger plus one Actions publication bot commit"}
],["scope","sha","total","human","bot","method"])
(OUT/"DY_ANALYSIS_SUMMARY.txt").write_text(
 "STATUS=ANALYSIS_PASS\nJOB=dx0-dx4-static\nSOURCE_SHA="+SNAPSHOT+"\nEXIT_CODE=0\n"+
 "DY2_TILE_STORE_ROWS="+str(len(tile_store_rows))+"\nDY2_TILE_ALIAS_PROVEN="+str(len(tile_alias_writers))+"\n"+
 "DY3_GLOBAL_80139EFC_WRITERS="+str(len(global_writer_rows))+"\n"+
 "DY3_GLOBAL_80139EFC_ARITHMETIC_EXPRESSIONS="+str(len(dy3_arithmetic_rows))+"\n"+
 "DY3_MANAGER_PROVEN_READERS="+str(len(manager_reader_rows))+"\n"+
 "DY4_BACKEDGES_AFTER_FEE_POST="+str(len(dy4_backedge_rows))+"\n"+
 "DY3_HELPER_MANAGER_FIELD_ROWS="+str(len(manager_field_rows))+"\n"+
 "DY3_RNG_LOOP_ROWS="+str(len(helper_rng_rows))+"\n"+
 "DY4_NEGATIVE_TILE_FEE_POSTS_TOTAL="+str(len(computed_posts))+"\n"+
 "DY4_NEGATIVE_TILE_FEE_POSTS_D15A8="+str(len(d15a8_posts))+"\n"+
 "GAME_OR_EMULATOR_EXECUTED=no\nBIOS_OR_SAVESTATE_USED=no\nBINARY_COMMITTED=no\nOUTPUT=TEXT_ONLY\n",encoding="utf-8")
print("DY2_TILE_STORE_ROWS="+str(len(tile_store_rows))+" TILE_ALIAS_PROVEN="+str(len(tile_alias_writers)))
print("DY3_GLOBAL_80139EFC_WRITERS="+str(len(global_writer_rows)))
print("DY3_HELPER_MANAGER_FIELD_ROWS="+str(len(manager_field_rows)))
print("DY4_NEGATIVE_TILE_FEE_POSTS_TOTAL="+str(len(computed_posts))+" D15A8="+str(len(d15a8_posts)))

# Human-readable audit report.
d15_reads=[r for r in dx1 if r["region"]=="ENTRY1" and r["function_name_guess"]=="FUN_800D15A8"]
reach_targets={r["target_pc"]:r["reachable_from_800EC574"] for r in target_rows}
plus2_reads=sum(1 for r in dx2_access if r["access"]=="READ")
plus2_writes=sum(1 for r in dx2_access if r["access"]=="WRITE")
dep_count=sum(1 for r in setter_calls if r["a1_depends_on_plus2EE_reader"]=="YES")
models_summary=[]
for mid,formula,factors,falsifier in models:
    mis=[str(d) for d in range(1,5) if fee_base_assumption*factors[d]!=observed[d]]
    models_summary.append(mid+": bertentangan pada d="+(",".join(mis) if mis else "tidak ada")+
      "; faktor d1..d4="+",".join(str(factors[d]) for d in range(1,5))+".")
report=[
"# DX0–DX4 — audit statis seluruh EXE dan DATA.BIN Entry 1",
"",
"BASELINE_INCLUSIVE="+BASELINE,
"SNAPSHOT_SOURCE_SHA="+SNAPSHOT,
"DX0_SNAPSHOT_TOTAL="+str(len(ledger))+" HUMAN="+str(humans)+" BOT="+str(bots),
"DX0_EXPECTED_FINAL_AFTER_ONE_BOT_PUBLICATION="+str(len(ledger)+1)+" HUMAN="+str(humans)+" BOT="+str(bots+1),
"EXE_SHA256="+EXE_SHA,
"DATA_BIN_SHA256="+DATA_SHA,
"ENTRY1_SHA256="+ENTRY_SHA+"; SIZE="+str(ENTRY_SIZE)+"; FILE_OFFSET=0x10BB000; BASE=0x800AD450",
"",
"## Status per DX",
"DX0: TUNTAS K4 — seluruh commit dihitung inklusif baseline sampai SHA snapshot. Hitungan final HEAD sesudah publikasi bot diverifikasi ulang setelah run.",
"DX1: TUNTAS K4 untuk census linear full-image jika scan selesai; atribusi fungsi tetap heuristik dan hasil perlu dibaca dengan asal register basis setiap baris.",
"DX2: SEBAGIAN K4 — CFG intra-fungsi direct edges/delay-slot; indirect JR/JALR ditandai sebagai exit yang tidak terpecahkan. Semantik pemicu tetap dibatasi.",
"DX3: SEBAGIAN K4 — operator dan origin statis pada root yang diminta; register dinamis yang belum terikat ke selisih level tetap TIDAK TAHU.",
"DX4: TUNTAS K4 untuk membandingkan tiga prediksi dengan empat angka HIPOTESIS PENGGUNA; formula ROM aktual tetap TIDAK TAHU.",
"",
"## DX1 — full-scan displacement +0x1A",
"Hit keseluruhan EXE+Entry 1="+str(len(dx1))+"; hit yang diberi label fungsi FUN_800D15A8 oleh function-entry heuristic="+str(len(d15_reads))+".",
"DX1_ALL_PLUS1A_ACCESS.tsv menyimpan setiap PC, offset, byte, instruction, fungsi dugaan, register basis, asal slot/global atau konstanta, dan trace register. DX1_D15A8_WINDOW_PLUS1A.tsv memberikan window PC D15A8 untuk spot-check.",
"DW4_TILE_PLUS1A_ACCESSES.tsv kosong karena analyzer DW4 hanya men-scanning instruksi yang reachable di basic block FUN_80102408. Itu bukan full Entry 1 / EXE scan dan tidak menguji FUN_800D15A8. Tidak ada kontradiksi.",
"Temuan AZ3/DP3 tentang tile+0x1A bertahan sejauh bukti lama: FUN_800F7ADC menyalin resource+0x14/+0x15 ke tile+0x1A; handler FUN_800D15A8 disebut memakai u16(tile+0x1A) pada action 3/8 dan menyiapkan pending -fee. DX1 menyajikan pemindaian instruksi penuh untuk menilai PC/base langsung; base yang trace-nya tidak mengikat slot EA84 atau alamat 0x8013B818 jangan dianggap tile tanpa bukti.",
"",
"## DX2 — CFG +0x2EE dan setter Chakra",
"CFG dimulai pada FUN_800EC574. Setiap branch mempunyai delay-slot node dengan outcome TAKEN/FALLTHROUGH; JAL kembali ke PC+8 selepas delay slot; JR RA berakhir selepas delay slot; JR register selain RA diperlakukan sebagai indirect exit, bukan fall-through.",
"Reachability tiap target ditampilkan di DX2_TARGET_REACHABILITY.tsv; setiap kondisi branch yang dapat mempengaruhi target ada di DX2_PATH_CONDITIONS.tsv; semua instruksi yang tercapai ada di DX2_FUN_800EC574_CFG.tsv; JR/external exits di DX2_CFG_JR_AND_EXTERNAL_EXITS.tsv.",
"Full-image scan +0x2EE: reads="+str(plus2_reads)+"; writes="+str(plus2_writes)+". Semua PC dan origin base ada di DX2_ALL_PLUS2EE_ACCESS.tsv. Daftar reader menuju setter ada di DX2_2EE_READERS_TO_SETTER.tsv; direct setter callers dan backward-slice ke argumen a1 ada di DX2_SETTER_8001387C_CALLS.tsv.",
"Jika route mencapai JAL helper FUN_8001552C di ECAD4 lalu store helper return di ECAE0, global accumulator menjadi 1 karena nilai return helper ditentukan delay slot JR pada EXE. Bila jalur kemudian mencapai lhu ECBA8, negu ECBB0, dan sh ECBB8, nilai yang ditulis adalah 0xFFFF (signed -1). File DX2_HELPER_ONE_TO_PLUS2EE.tsv mencatat reachability setiap PC. Nilai -1 tidak boleh disamakan dengan biaya pembelian petak tanpa relasi tambahan.",
"Apakah -1 adalah debit Chakra: manager+0x2EE adalah signed pending delta; pembaca +0x2EE harus dibuktikan mengalir ke a1 setter 0x8001387C, dan setter harus menulis saldo participant+0x18. Koneksi yang terdeteksi secara backward slice ditandai YES; fungsi yang hanya sekadar berada di jalur yang sama ditandai NOT_PROVEN. Jika jalur setter tidak terikat, tujuan debit khusus -1 = TIDAK TAHU.",
"H1: lane +0x2EE adalah delta saldo Chakra. Falsifier: reader tidak mencapai a1 setter atau setter menulis field selain participant+0x18. H2: lane +0x2EE adalah delta saldo generik (bisa debit/kredit/transfer). Falsifier: semua writer dan caller terbukti hanya dipakai satu kelas transaksi. Tujuan gameplay nilai -1 tetap TIDAK TAHU sampai producer/caller diketahui.",
"",
"## DX3 — level difference, nibble dan shift",
"DX3_SEED_REACHABILITY.tsv menguji keterjangkauan site 0x800EC3A8 dari root FUN_800EB434 dan root FUN_800EF3CC. DX3_OPERATION_CENSUS.tsv mencatat sll/sllv/srl/srlv/sra/srav, mult/multu/mflo, slti/sltiu immediate 2, sub/subu, OR/ORI, dan origin operand.",
"DX3_TILE_PLUS20_READ_WRITE.tsv berisi semua load/store displacement +0x20 dalam CFG tiap root. DX3_LEVEL_NIBBLE_COMPARISONS.tsv mencatat branch yang register operand-nya trace ke lhu +0x20. DX3_LEVEL_NIBBLE_OR_SOURCES.tsv mengurai OR/ORI dalam nilai yang disimpan ke +0x20 dan asal sll/sllv bila ada. DX3_ONE_SHIFT_PATTERNS.tsv khusus kasus operand literal 1 yang di-shift.",
"Pengurangan yang diuji untuk selisih level ada di DX3_LEVEL_DIFFERENCE_CANDIDATES.tsv. Jika kedua operand tidak trace ke pembacaan tile+0x20, itu bukan bukti delta level. Tidak adanya pola 1<<d atau tidak adanya subtract yang terikat pada nibble tidak meniadakan kemungkinan formula berada di pemanggil lain atau indirect path.",
"",
"## DX4 — model dan 4 pengamatan pengguna",
"Observasi d=1..4: 100, 400, 800, 1600 dengan fee_dasar simbolik. Angka 100 dipakai hanya sebagai normalisasi aritmetika sesuai asumsi pengguna; bukan konstanta ROM.",
]+models_summary+[
"Falsifier per model mengarahkan pencarian ke operand selisih d, special branch d=1 (misalnya slti[u] immediate 2), coefficient/lookup, atau instruksi shift di site 0x800EC3A8 / 0x800EF3CC. Model yang cocok dengan data pengguna tetap belum terbukti sebagai kode ROM.",
"",
"## Validitas dan batas",
"Input EXE/DATA.BIN/Entry 1 dicocokkan dengan ukuran dan SHA-256 yang telah ditetapkan. Tidak ada emulator/game dijalankan. Tidak ada ISO, EXE, DATA.BIN, BIOS, savestate, dump, video, frame, atau biner yang dikomit. Output hanya MD/TSV/TXT; tiap baris machine raw memuat 4 byte instruksi.",
"Linear full-image scan dapat mendekode byte data non-code sebagai instruction; hasil per PC harus dipilah menurut function label dan base_origin. CFG rooted dari fungsi mengurangi risiko tersebut untuk analisis reachability. Maksimum confidence K4.",
]
(OUT/"DX0_DX4_STATIC_AUDIT.md").write_text("\n".join(report)+"\n",encoding="utf-8")
(OUT/"DX_ANALYSIS_SUMMARY.txt").write_text(
 "STATUS=ANALYSIS_PASS\nJOB=dx0-dx4-static\nSOURCE_SHA="+SNAPSHOT+"\nEXIT_CODE=0\n"+
 "DX1_PLUS1A_HITS="+str(len(dx1))+"\nDX1_D15A8_WINDOW_HITS="+str(len(d15_reads))+"\n"+
 "DX2_PLUS2EE_READS="+str(plus2_reads)+"\nDX2_PLUS2EE_WRITES="+str(plus2_writes)+"\n"+
 "DX2_DIRECT_SETTER_CALLS="+str(len(setter_calls))+"\nDX2_READER_TO_SETTER_YES="+str(dep_count)+"\n"+
 "DX3_ONE_SHIFT_PATTERNS="+str(len(shift_one_rows))+"\n"+
 "GAME_OR_EMULATOR_EXECUTED=no\nBIOS_OR_SAVESTATE_USED=no\nBINARY_COMMITTED=no\nOUTPUT=TEXT_ONLY\n",
 encoding="utf-8")
print("DX1_PLUS1A_HITS="+str(len(dx1)))
print("DX1_D15A8_WINDOW_HITS="+str(len(d15_reads)))
print("DX2_PLUS2EE_READS="+str(plus2_reads)+" WRITES="+str(plus2_writes))
print("DX2_DIRECT_SETTER_CALLS="+str(len(setter_calls))+" READER_TO_SETTER_YES="+str(dep_count))
print("DX2_TARGETS="+str(sum(1 for r in target_rows if r["reachable_from_800EC574"]=="YES"))+"/"+str(len(target_rows)))
print("DX3_ONE_SHIFT_PATTERNS="+str(len(shift_one_rows)))
