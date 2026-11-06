#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, os, struct, subprocess, sys
from collections import defaultdict, deque
from pathlib import Path
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_PATH, DATA_PATH, OUT = map(Path, sys.argv[1:4])
BASELINE = os.environ.get("DX_BASELINE", "2d5becc3a70716cf78563233504b800b3c9609e0")
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
exe=decode(EXE_PATH.read_bytes(),EXE_BASE,0)
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
        if fn in (8,9,12,13,16,18,24,25,26,27): return None
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

def last_def(reg,before,lo,code):
    for pc in range(before-4,lo-4,-4):
        i=code.get(pc)
        if i and dest_reg(i)==reg:return i
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
    if seen is None:seen=set()
    if depth>6 or (reg,before) in seen:return "TIDAK TAHU: batas def-chain"
    seen.add((reg,before))
    if reg==0:return "$zero"
    d=last_def(reg,before,lo,code)
    if not d:return rn(reg)+" masuk/dinamis"
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
    elif mn=="mflo":
        mul=next((code[p] for p in range(d["pc"]-4,max(lo-4,d["pc"]-0x44),-4)
                  if p in code and code[p]["mnemonic"] in ("mult","multu")),None)
        if mul:s+=" <- "+h32(mul["pc"])+" "+mul["text"]+" ("+trace_reg(mul["rs"],mul["pc"],lo,code,depth+1,seen.copy())+"; "+trace_reg(mul["rt"],mul["pc"],lo,code,depth+1,seen.copy())+")"
    return s[:900]

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
