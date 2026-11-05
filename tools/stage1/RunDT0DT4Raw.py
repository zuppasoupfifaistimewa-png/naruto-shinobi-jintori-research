#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, os, re, struct, subprocess, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_PATH, DATA_PATH, OUT = map(Path, sys.argv[1:4])
BASELINE=os.environ.get("DT0_BASELINE","2f72b3a2807f1022048083d6d07ad527adaa7cf7")
AUDIT_HEAD=os.environ.get("DT0_AUDIT_HEAD", subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip())
ENTRY_BASE=0x800AD450
ENTRY_OFF=0x10BB000
ENTRY_SIZE=596412
DATA_SHA="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
EXE_SHA="a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
ENTRY_SHA="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
G_FEE=0x80139EFC
G_INDEX=0x8013EBB0
TABLE_BASE=0x8013B818
TABLE_FILE_OFF=0x11493C8
OUT.mkdir(parents=True,exist_ok=True)

REG=["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
def rn(n): return REG[n]
def hx(b): return " ".join(f"{x:02X}" for x in b)
def write_tsv(name,rows,fields=None):
    if fields is None: fields=list(rows[0]) if rows else ["STATUS"]
    with (OUT/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore")
        w.writeheader()
        for r in rows:w.writerow(r)
def git(args): return subprocess.check_output(["git",*args],text=True).strip()
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

if len(EXE_PATH.read_bytes())!=385024 or sha(EXE_PATH)!=EXE_SHA: raise SystemExit("EXE_IDENTITY_MISMATCH")
data=DATA_PATH.read_bytes()
if len(data)!=66015232 or hashlib.sha256(data).hexdigest()!=DATA_SHA: raise SystemExit("DATA_BIN_IDENTITY_MISMATCH")
lbn,size=struct.unpack_from("<II",data,0x4C)
entry_off=(lbn-212)*2048
entry=data[entry_off:entry_off+size]
if (lbn,size,entry_off,len(entry),hashlib.sha256(entry).hexdigest())!=(8778,ENTRY_SIZE,ENTRY_OFF,ENTRY_SIZE,ENTRY_SHA):
    raise SystemExit("ENTRY1_DIRECTORY_MAPPING_MISMATCH")
md=Cs(CS_ARCH_MIPS,CS_MODE_MIPS32|CS_MODE_LITTLE_ENDIAN)
md.detail=False
ins={}
for off in range(0,len(entry)-3,4):
    b=entry[off:off+4];pc=ENTRY_BASE+off;word=int.from_bytes(b,"little")
    cap=next(md.disasm(b,pc,count=1),None)
    text=(cap.mnemonic+" "+cap.op_str).strip() if cap else f".word 0x{word:08X}"
    ins[pc]={"pc":pc,"off":off,"fileoff":ENTRY_OFF+off,"bytes":b,"word":word,"text":text,
             "op":word>>26,"rs":(word>>21)&31,"rt":(word>>16)&31,"rd":(word>>11)&31,
             "sh":(word>>6)&31,"fn":word&63,"imm":((word&65535)^32768)-32768,
             "uimm":word&65535,"target":word&0x03FFFFFF}
def at(pc): return ins.get(pc)
def show(i):
    return {"pc":f"0x{i['pc']:08X}","file_offset":f"0x{i['fileoff']:X}","bytes":hx(i["bytes"]),"instruction":i["text"]}
def reg_dest(i):
    op,fn=i["op"],i["fn"]
    if op==0:
        if fn in (8,9,16,18,24,25,26,27):return 31 if fn==9 else None
        return i["rd"] or None
    if op in (2,3,4,5,6,7,1,0x2A,0x2B):return 31 if op==3 else None
    if op in (8,9,10,11,12,13,14,15,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x3A,0x3B,0x3C,0x3D,0x3E,0x3F):
        return i["rt"] or None
    return None
def reg_sources(i):
    op,fn,rs,rt=i["op"],i["fn"],i["rs"],i["rt"]
    if op==0:
        if fn in (0,2,3):return [rt]
        if fn in (8,9):return [rs]
        if fn in (16,18):return []
        if fn in (12,13):return []
        return [rs,rt]
    if op in (1,4,5):return [rs,rt] if op!=1 else [rs]
    if op in (6,7):return [rs]
    if op in (8,9,10,11,12,13,14):return [rs]
    if op in (0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27):return [rs]
    if op in (0x28,0x29,0x2A,0x2B,0x38,0x39,0x3A,0x3B):return [rs,rt]
    return []
def branch_target(i):
    op=i["op"];pc=i["pc"]
    if op in (4,5,6,7) or op==1:
        return (pc+4+(i["imm"]<<2))&0xFFFFFFFF
    if op in (2,3):
        return (((pc+4)&0xF0000000)|(i["target"]<<2))&0xFFFFFFFF
    return None
def branch_kind(i):
    if i["op"]==1:
        return "REGIMM_"+("BLTZ" if i["rt"]==0 else "BGEZ" if i["rt"]==1 else f"RT{i['rt']}")
    return {4:"BEQ",5:"BNE",6:"BLEZ",7:"BGTZ",2:"J",3:"JAL"}.get(i["op"],"")
def ins_for(pc0,pc1):
    return [ins[p] for p in sorted(ins) if pc0<=p<=pc1]
def last_def(reg,before,lo):
    for pc in range(before-4,lo-4,-4):
        i=at(pc)
        if i and reg_dest(i)==reg:return i
    return None
def trace_origin(reg,before,lo,depth=0,seen=None):
    if seen is None:seen=set()
    if (reg,before) in seen or depth>4:return "cycle/depth limit"
    seen.add((reg,before))
    d=last_def(reg,before,lo)
    if d is None:return "TIDAK TAHU: register masuk/tidak ada definisi statis dalam batas fungsi"
    out=f"0x{d['pc']:08X} {d['text']} [{hx(d['bytes'])}]"
    # For common immediate and load forms, report source/base register provenance.
    op=d["op"]; rs=d["rs"]
    if op in (8,9,10,11,12,13,14) or op in (0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27):
        if rs!=0:out+="; basis="+trace_origin(rs,d["pc"],lo,depth+1,seen.copy())
    elif op==0 and d["fn"] not in (0,2,3,8,9,16,18):
        out+="; src="+",".join(trace_origin(x,d["pc"],lo,depth+1,seen.copy()) for x in reg_sources(d))
    return out

# Function boundaries and a conservative static constant/data-flow resolver.
function_starts={ENTRY_BASE}
for _i in ins.values():
    if _i["op"]==3:
        _t=((_i["pc"]+4)&0xF0000000)|(_i["target"]<<2)
        if _t in ins:function_starts.add(_t)
    if _i["op"]==9 and _i["rs"]==29 and _i["rt"]==29 and _i["imm"]<0:
        function_starts.add(_i["pc"])
def function_at(pc):
    return max((x for x in function_starts if x<=pc),default=ENTRY_BASE)
def const_before(reg,before,lo,depth=0,seen=None):
    if seen is None:seen=set()
    if depth>8 or (reg,before) in seen:return None
    seen.add((reg,before))
    d=last_def(reg,before,lo)
    if d is None:return None
    op,rs,rt,rd,fn=d["op"],d["rs"],d["rt"],d["rd"],d["fn"]
    if op==0x0F:return (d["uimm"]<<16)&0xFFFFFFFF
    if op in (8,9):
        x=const_before(rs,d["pc"],lo,depth+1,seen.copy())
        return ((x+d["imm"])&0xFFFFFFFF) if x is not None else None
    if op==0x0D:
        x=const_before(rs,d["pc"],lo,depth+1,seen.copy())
        return (x|d["uimm"])&0xFFFFFFFF if x is not None else None
    if op==0:
        if fn==0:
            x=const_before(rt,d["pc"],lo,depth+1,seen.copy())
            return (x<<d["sh"])&0xFFFFFFFF if x is not None else None
        if fn==2:
            x=const_before(rt,d["pc"],lo,depth+1,seen.copy())
            return (x>>d["sh"])&0xFFFFFFFF if x is not None else None
        if fn in (0x21,0x23,0x24,0x25,0x26,0x27):
            x=const_before(rs,d["pc"],lo,depth+1,seen.copy())
            y=const_before(rt,d["pc"],lo,depth+1,seen.copy())
            if x is None or y is None:return None
            if fn==0x21:return (x+y)&0xFFFFFFFF
            if fn==0x23:return (x-y)&0xFFFFFFFF
            if fn==0x24:return x&y
            if fn==0x25:return x|y
            if fn==0x26:return x^y
            if fn==0x27:return ~(x|y)&0xFFFFFFFF
    if op in (0x20,0x21,0x23,0x24,0x25):
        base=const_before(rs,d["pc"],lo,depth+1,seen.copy())
        if base is None:return None
        addr=(base+d["imm"])&0xFFFFFFFF
        if ENTRY_BASE<=addr<ENTRY_BASE+len(entry):
            off=addr-ENTRY_BASE
            width={0x20:1,0x21:2,0x23:4,0x24:1,0x25:2}[op]
            if off+width<=len(entry):
                return int.from_bytes(entry[off:off+width],"little",signed=(op in (0x20,0x21,0x23)))
    return None
def const_label(v):
    return "TIDAK TAHU" if v is None else f"0x{v:08X}"
def vaddr_bytes(addr,n=64):
    if addr is None or not (ENTRY_BASE<=addr<ENTRY_BASE+len(entry)):return b""
    return entry[addr-ENTRY_BASE:addr-ENTRY_BASE+n]
def control_kind(i):
    if i["op"] in (1,4,5,6,7):return "CONDITIONAL_BRANCH"
    if i["op"] in (2,3):return "DIRECT_JUMP_OR_CALL"
    if i["op"]==0 and i["fn"] in (8,9):return "REGISTER_JUMP"
    return "NORMAL"
def indexed_table_base(load_ins,lo):
    # For lw v0,(v1), follow the address-forming addu and choose its constant
    # operand as the table base; the other operand is selector*4.
    if load_ins is None:return None
    d=last_def(load_ins["rs"],load_ins["pc"],lo)
    if d and d["op"]==0 and d["fn"]==0x21:
        vals=[const_before(r,d["pc"],lo) for r in (d["rs"],d["rt"])]
        for v in vals:
            if v is not None and ENTRY_BASE<=v<ENTRY_BASE+len(entry):return v
    return const_before(load_ins["rs"],load_ins["pc"],lo)

# DT0: baseline inclusive through the exact source commit of this workflow run.
revs=git(["rev-list","--reverse",f"{BASELINE}^..{AUDIT_HEAD}"]).splitlines()
ledger=[];humans=bots=0
for rev in revs:
    fields=git(["show","-s","--format=%H%x09%an%x09%ae%x09%s",rev]).split("\t",3)
    sh,author,email,msg=fields
    bot=("github-actions" in author.lower() or "[bot]" in author.lower() or "41898282+github-actions" in email.lower())
    bots+=int(bot);humans+=int(not bot)
    files=git(["diff-tree","--root","--no-commit-id","--name-only","-r",rev]).splitlines()
    ledger.append({"sha_full":sh,"class":"BOT" if bot else "MANUSIA","author":author,
                   "author_email":email,"message":msg,"changed_files":";".join(files)})
write_tsv("DT0_COMMIT_LEDGER.tsv",ledger,["sha_full","class","author","author_email","message","changed_files"])
write_tsv("DT0_SUMMARY.txt",[{"STATUS":"TUNTAS","K":"K4","BASELINE_INCLUSIVE":BASELINE,
          "SNAPSHOT_SHA":AUDIT_HEAD,"TOTAL_INCLUSIVE":len(ledger),"MANUSIA":humans,"BOT":bots,
          "AHEAD_AFTER_BASELINE":max(0,len(ledger)-1)}],
          ["STATUS","K","BASELINE_INCLUSIVE","SNAPSHOT_SHA","TOTAL_INCLUSIVE","MANUSIA","BOT","AHEAD_AFTER_BASELINE"])

# DT1: complete raw-byte instruction window, register origins, table-field semantics, and global writers.
loop0,loop1=0x800ECA0C,0x800ECA84
loop=ins_for(loop0,loop1)
looprows=[]
for i in loop:
    s=show(i);s["role"]="LOOP"
    looprows.append(s)
write_tsv("DT1_LOOP_RAW.tsv",looprows,["pc","file_offset","bytes","instruction","role"])
firstuses={}
memrows=[]
for i in loop:
    op=i["op"];rs=i["rs"];rt=i["rt"]
    if op in (0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27):
        memrows.append({"pc":f"0x{i['pc']:08X}","operation":i["text"],"base_reg":rn(rs),
                        "offset":f"{i['imm']:+#x}","byte_semantics":"memory field access"})
    for r in reg_sources(i):
        firstuses.setdefault(r,i["pc"])
origins=[]
for r in (8,9,10,6,7):
    fu=firstuses.get(r)
    d=last_def(r,fu,0x800EC574) if fu else None
    origins.append({"register":rn(r),"first_use_pc":f"0x{fu:08X}" if fu else "TIDAK DIGUNAKAN DALAM WINDOW",
                    "definition_pc":f"0x{d['pc']:08X}" if d else ("TIDAK TAHU" if fu else "—"),
                    "definition_instruction":d["text"] if d else ("register masuk / definisi luar window" if fu else "—"),
                    "definition_bytes":hx(d["bytes"]) if d else "—",
                    "origin_trace":trace_origin(r,fu,0x800EC574) if fu else "—"})
write_tsv("DT1_REGISTER_ORIGINS.tsv",origins,
          ["register","first_use_pc","definition_pc","definition_instruction","definition_bytes","origin_trace"])
# Backward slices of t0/t1/t2/a2/a3 at both known call sites, separate from
# the helper-local definitions just above.
caller_rows=[]
for callpc in (0x800F3830,0x800F5D08):
    for reg in (8,9,10,6,7):
        d=last_def(reg,callpc,0x800F3658)
        val=const_before(reg,callpc,0x800F3658)
        caller_rows.append({"call_pc":f"0x{callpc:08X}","register":rn(reg),
            "last_definition_pc":f"0x{d['pc']:08X}" if d else "TIDAK TAHU",
            "last_definition":d["text"] if d else "TIDAK TAHU: belum ada definisi di caller sejak awal fungsi",
            "definition_bytes":hx(d["bytes"]) if d else "—",
            "origin_trace":trace_origin(reg,callpc,0x800F3658),
            "constant_at_call":const_label(val)})
write_tsv("DT1_CALLER_REGISTER_ORIGINS.tsv",caller_rows,
          ["call_pc","register","last_definition_pc","last_definition","definition_bytes","origin_trace","constant_at_call"])
write_tsv("DT1_TILE_MEMORY_FIELDS.tsv",memrows,["pc","operation","base_reg","offset","byte_semantics"])

# Census direct writes to 0x80139EFC over the whole Entry 1, including CLEARs.
call_a2={c:const_before(6,c,0x800F3658) for c in (0x800F3830,0x800F5D08)}
a2_proven=all(v==0x80140000 for v in call_a2.values())
writers=[];clears=[];unknown_fee_candidates=[]
for i in ins.values():
    if i["op"] not in (0x28,0x29,0x2B) or i["imm"]!=-0x6104:continue
    fs=function_at(i["pc"])
    base=const_before(i["rs"],i["pc"],fs)
    ea=((base+i["imm"])&0xFFFFFFFF) if base is not None else None
    if i["rs"]==6 and 0x800EC574<=i["pc"]<=0x800ECBFF:
        if a2_proven:ea=G_FEE
        else:
            unknown_fee_candidates.append({"pc":f"0x{i['pc']:08X}","bytes":hx(i["bytes"]),
                "instruction":i["text"],"base_register":"a2",
                "base_at_call_800F3830":const_label(call_a2[0x800F3830]),
                "base_at_call_800F5D08":const_label(call_a2[0x800F5D08]),
                "reason":"TIDAK TAHU: parameter a2 tidak terbukti 0x80140000"})
            continue
    if ea!=G_FEE:continue
    val=const_before(i["rt"],i["pc"],fs) if i["rt"]!=0 else 0
    clear=(i["rt"]==0 or val==0)
    row={"pc":f"0x{i['pc']:08X}","file_offset":f"0x{i['fileoff']:X}",
         "function":f"FUN_{fs:08X} (heuristik)","bytes":hx(i["bytes"]),
         "instruction":i["text"],"base_register":rn(i["rs"]),
         "base_value":const_label(base),"value_register":rn(i["rt"]),
         "value_origin":trace_origin(i["rt"],i["pc"],fs) if i["rt"] else "ZERO_REGISTER",
         "value_constant":const_label(val),"is_clear":"YES" if clear else "NO",
         "relationship_to_loop":"BEFORE_LOOP" if i["pc"]<loop0 else ("IN_LOOP" if loop0<=i["pc"]<=loop1 else "OUTSIDE_LOOP"),
         "a2_callpath_base_proven":"YES" if a2_proven else "NO"}
    writers.append(row)
    if clear:clears.append(row)
write_tsv("DT1_FEE_GLOBAL_WRITERS.tsv",writers,
          ["pc","file_offset","function","bytes","instruction","base_register","base_value",
           "value_register","value_origin","value_constant","is_clear","relationship_to_loop","a2_callpath_base_proven"])
write_tsv("DT1_FEE_GLOBAL_CLEARS.tsv",clears,
          ["pc","file_offset","function","bytes","instruction","base_register","base_value",
           "value_register","value_origin","value_constant","relationship_to_loop","a2_callpath_base_proven"])
write_tsv("DT1_FEE_WRITE_CANDIDATES.tsv",unknown_fee_candidates,
          ["pc","bytes","instruction","base_register","base_at_call_800F3830","base_at_call_800F5D08","reason"])
(OUT/"DT1_CLEAR_CENSUS_SUMMARY.txt").write_text(
    f"PREVIOUS_DS_CENSUS_CLEAR_COUNT=7\nCURRENT_RAW_STATIC_CLEAR_COUNT={len(clears)}\n"
    f"CURRENT_RAW_STATIC_ALL_FEE_WRITES={len(writers)}\n"
    f"CALLER_A2_AT_800F3830={const_label(call_a2[0x800F3830])}\n"
    f"CALLER_A2_AT_800F5D08={const_label(call_a2[0x800F5D08])}\n"
    f"A2_GLOBAL_BASE_PROVEN_FOR_BOTH_CALLS={'YES' if a2_proven else 'NO'}\n"
    f"CENSUS_MATCH={'YES' if len(clears)==7 else 'NO'}\n"
    f"CENSUS_MISMATCH_REASON={'TIDAK TAHU: parameterized/indirect writer resolution incomplete' if len(clears)!=7 else '—'}\n",
    encoding="utf-8")

# Operand provenance and complete tile+0x20 packed-halfword path, without inventing gameplay labels.
mult=at(0x800ECAA0)
multrows=[]
if mult:
    for r,role in ((mult["rs"],"MULT_OPERAND_RS"),(mult["rt"],"MULT_OPERAND_RT")):
        multrows.append({"pc":"0x800ECAA0","role":role,"register":rn(r),
                         "origin_trace":trace_origin(r,mult["pc"],0x800EC574)})
write_tsv("DT1_MULTIPLY_ORIGINS.tsv",multrows,["pc","role","register","origin_trace"])
packed=[]
for i in ins_for(0x800EC574,0x800ECBB8):
    if i["op"] in (0x21,0x25,0x29) and i["imm"]==0x20:
        packed.append({"pc":f"0x{i['pc']:08X}","bytes":hx(i["bytes"]),"instruction":i["text"],
                       "next_8": " || ".join(f"0x{x['pc']:08X} {x['text']}" for x in ins_for(i["pc"]+4,i["pc"]+32))})
write_tsv("DT1_TILE_PLUS20_TRACE.tsv",packed,["pc","bytes","instruction","next_8"])

# DT2: exact delay-slot bytes and the value placed in v0 along the beqz/second return path.
slot=at(0x80102434)
retrows=[]
for pc in (0x8010241C,0x80102424,0x80102428,0x80102430,0x80102434):
    i=at(pc)
    if i:retrows.append({"pc":f"0x{pc:08X}","bytes":hx(i["bytes"]),"instruction":i["text"],
                         "meaning":"branch/return-path instruction"})
v0_before=trace_origin(2,0x80102430,0x80102408)
v0_after=trace_origin(2,0x80102434,0x80102408) if slot else "TIDAK TAHU"
write_tsv("DT2_RETURN_PATH.tsv",retrows,["pc","bytes","instruction","meaning"])
data_excerpt=data[TABLE_FILE_OFF:TABLE_FILE_OFF+64]
(OUT/"DT2_TABLE_EXCERPT.txt").write_text(
    f"DATA_BIN_FILE_OFFSET=0x{TABLE_FILE_OFF:X}\n"
    f"RUNTIME_TABLE_BASE=0x{TABLE_BASE:08X}\n"
    f"BYTE_COUNT={len(data_excerpt)}\nHEX={hx(data_excerpt)}\n"
    f"SHA256={hashlib.sha256(data_excerpt).hexdigest()}\n",encoding="utf-8")
retconst=const_before(2,0x80102438,function_at(0x80102430))
return_value=(f"0x{retconst:08X}" if retconst is not None else
              "TIDAK TAHU: nilai v0 setelah delay slot bergantung pada register/data yang tidak konstan secara statis")
(OUT/"DT2_SUMMARY.txt").write_text(
    f"DELAY_SLOT_PC=0x80102434\nDELAY_SLOT_BYTES={hx(slot['bytes']) if slot else 'TIDAK TAHU'}\n"
    f"DELAY_SLOT_INSTRUCTION={slot['text'] if slot else 'TIDAK TAHU'}\n"
    f"RETURN_PATH_2_PC=0x80102430\nV0_BEFORE_DELAY_SLOT={v0_before}\n"
    f"V0_AFTER_DELAY_SLOT={v0_after}\n"
    f"RETURN_VALUE_AT_JR={return_value}\n",
    encoding="utf-8")

# DT3: direct control-flow predecessors, dispatcher/indirect-jump evidence, and index-global reads.
fstart,fend=0x800F3658,0x800F6100
fitems=ins_for(fstart,fend)
calls=(0x800F3830,0x800F5D08)
edges=[]
for i in ins.values():
    op=i["op"];target=branch_target(i);pc=i["pc"]
    if op in (4,5,6,7,1):
        regs=reg_sources(i)
        vals=[f"{rn(r)}={const_label(const_before(r,pc,function_at(pc)))}" for r in regs]
        cond=f"{i['text']} ; "+", ".join(vals)
        if target is not None:
            edges.append({"from_pc":pc,"to_pc":target,"edge":"TAKEN","condition":cond,
                          "delay_slot":at(pc+4)["text"] if at(pc+4) else "TIDAK TAHU"})
        edges.append({"from_pc":pc,"to_pc":pc+8,"edge":"NOT_TAKEN","condition":cond,
                      "delay_slot":at(pc+4)["text"] if at(pc+4) else "TIDAK TAHU"})
    elif op==2 and target is not None:
        edges.append({"from_pc":pc,"to_pc":target,"edge":"UNCONDITIONAL_J",
                      "condition":"selalu; j direct","delay_slot":at(pc+4)["text"] if at(pc+4) else "TIDAK TAHU"})
predrows=[]
for call in calls:
    incoming=[e for e in edges if e["to_pc"]==call]
    prev=at(call-4);beforeprev=at(call-8)
    if prev and (beforeprev is None or control_kind(beforeprev)=="NORMAL"):
        incoming.append({"from_pc":prev["pc"],"to_pc":call,"edge":"SEQUENTIAL_FALLTHROUGH",
                         "condition":"sekuensial; tidak ada transfer kontrol sebelumnya","delay_slot":"—"})
    if incoming:
        for e in incoming:
            predrows.append({"call_pc":f"0x{call:08X}","from_pc":f"0x{e['from_pc']:08X}",
                "to_pc":f"0x{call:08X}","edge":e["edge"],"condition":e["condition"],
                "delay_slot":e["delay_slot"],
                "operand_origin":"branch operand origins/static constants embedded in condition",
                "classification":"STATIC_PREDECESSOR"})
    else:
        predrows.append({"call_pc":f"0x{call:08X}","from_pc":"TIDAK ADA PREDECESSOR LANGSUNG",
            "to_pc":f"0x{call:08X}","edge":"NO_DIRECT_STATIC_EDGE",
            "condition":"TIDAK TAHU: tidak ada branch/jump direct atau fall-through valid; cek tabel dispatch jr v0",
            "delay_slot":"—","operand_origin":"DT3_JR_DISPATCH_TABLES.tsv",
            "classification":"INDIRECT_OR_UNRESOLVED"})

# Find immediate-register dispatchers and their source loads within the containing function.
jrrows=[]
for i in fitems:
    if i["op"]==0 and i["fn"]==8:
        r=i["rs"];d=last_def(r,i["pc"],fstart)
        context=ins_for(max(fstart,i["pc"]-0x30),i["pc"])
        jrrows.append({"jr_pc":f"0x{i['pc']:08X}","jr_bytes":hx(i["bytes"]),
                       "jr_instruction":i["text"],"target_reg_origin":trace_origin(r,i["pc"],fstart),
                       "preceding_context":" || ".join(f"0x{x['pc']:08X} {x['text']}" for x in context)})
write_tsv("DT3_INDIRECT_DISPATCHERS.tsv",jrrows,
          ["jr_pc","jr_bytes","jr_instruction","target_reg_origin","preceding_context"])
# Direct loads of the global event/index word in the function.
idxrows=[];st=[None]*32;st[0]=0
for i in fitems:
    op,rs,rt,imm=i["op"],i["rs"],i["rt"],i["imm"]
    base=st[rs];ea=((base+imm)&0xFFFFFFFF) if isinstance(base,int) else None
    if op in (0x20,0x21,0x23,0x24,0x25) and ea==G_INDEX:
        idxrows.append({"pc":f"0x{i['pc']:08X}","file_offset":f"0x{i['fileoff']:X}",
                        "bytes":hx(i["bytes"]),"instruction":i["text"],"destination":rn(rt),
                        "later_condition_uses":"; ".join(f"0x{x['pc']:08X} {x['text']}" for x in ins_for(i["pc"]+4,min(fend,i["pc"]+0x30)) if x["op"] in (1,4,5,6,7))})
    if op==0x0F:st[rt]=(i["uimm"]<<16)&0xFFFFFFFF
    elif op in (8,9):
        x=st[rs];st[rt]=((x+imm)&0xFFFFFFFF) if isinstance(x,int) else f"COMPUTED@{i['pc']:08X}"
    elif op==0x0D:
        x=st[rs];st[rt]=(x|i["uimm"]) if isinstance(x,int) else f"COMPUTED@{i['pc']:08X}"
    elif op in (0x20,0x21,0x23,0x24,0x25):st[rt]=f"LOAD@{i['pc']:08X}"
    elif op==0 and i["fn"]==0x21:
        x,y=st[rs],st[rt];st[i["rd"]]=((x+y)&0xFFFFFFFF) if isinstance(x,int) and isinstance(y,int) else f"COMPUTED@{i['pc']:08X}"
    elif op==0 and i["fn"] in (0,2,3):st[i["rd"]]=f"COMPUTED@{i['pc']:08X}"
    else:
        d=reg_dest(i)
        if d is not None:st[d]=f"UNKNOWN@{i['pc']:08X}"
write_tsv("DT3_INDEX_GLOBAL_ACCESSES.tsv",idxrows,
          ["pc","file_offset","bytes","instruction","destination","later_condition_uses"])
ptrrows=[]
for target in calls:
    needle=struct.pack("<I",target)
    pos=entry.find(needle)
    while pos>=0:
        ptrrows.append({"target":f"0x{target:08X}","entry_offset":f"0x{pos:X}",
                        "data_bin_file_offset":f"0x{ENTRY_OFF+pos:X}","bytes":hx(needle),
                        "interpretation":"candidate absolute pointer; table membership not proven"})
        pos=entry.find(needle,pos+1)
write_tsv("DT3_ABSOLUTE_POINTER_REFS.tsv",ptrrows,
          ["target","entry_offset","data_bin_file_offset","bytes","interpretation"])
# Resolve every JR v0 dispatch in FUN_800F3658; the key 0x800F5CE0 table
# derives from constant base operand of the preceding indexed-address addu.
dispatch_rows=[];dispatch_words=[]
for jr in [i for i in fitems if i["op"]==0 and i["fn"]==8 and i["rs"]==2]:
    load=at(jr["pc"]-8)
    if not load or load["op"] not in (0x20,0x21,0x23,0x24,0x25):continue
    base_reg=load["rs"]
    table_va=indexed_table_base(load,function_at(load["pc"]))
    add_def=last_def(base_reg,load["pc"],function_at(load["pc"]))
    shift_def=last_def(1 if False else base_reg,add_def["pc"],function_at(load["pc"])) if add_def else None
    # Selector is generally the byte loaded before the <<2 index scaling.
    selector_def=None
    if shift_def and shift_def["op"]==0 and shift_def["fn"]==0 and shift_def["sh"]==2:
        selector_def=last_def(shift_def["rt"],shift_def["pc"],function_at(load["pc"]))
    if selector_def is None and add_def and add_def["op"]==0 and add_def["fn"]==0x21:
        for rr in (add_def["rs"],add_def["rt"]):
            _d=last_def(rr,add_def["pc"],function_at(load["pc"]))
            if _d and _d["op"]==0 and _d["fn"]==0 and _d["sh"]==2:
                selector_def=last_def(_d["rt"],_d["pc"],function_at(load["pc"]));break
    selector_reg=selector_def["rt"] if selector_def and selector_def["op"] in (0x20,0x21,0x23,0x24,0x25) else None
    selector_src=(f"0x{selector_def['pc']:08X} {selector_def['text']}" if selector_def else "TIDAK TAHU")
    count=None;rangecheck="TIDAK TAHU"
    for q in range(jr["pc"]-4,max(function_at(jr["pc"]),jr["pc"]-0x30)-4,-4):
        cand=at(q)
        if cand and cand["op"]==0x0B: # sltiu rt,rs,imm
            count=cand["uimm"];rangecheck=f"0x{q:08X} {cand['text']}";break
    length=min(64,(count*4 if count is not None else 64))
    raw=vaddr_bytes(table_va,length)
    base_off=(ENTRY_OFF+(table_va-ENTRY_BASE)) if table_va is not None and ENTRY_BASE<=table_va<ENTRY_BASE+len(entry) else None
    dispatch_rows.append({"jr_pc":f"0x{jr['pc']:08X}","jr_bytes":hx(jr["bytes"]),
        "table_address":const_label(table_va),"table_file_offset":f"0x{base_off:X}" if base_off is not None else "TIDAK TAHU",
        "selector_register":rn(selector_reg) if selector_reg is not None else "TIDAK TAHU",
        "selector_source":selector_src,"range_check":rangecheck,"entry_count":count if count is not None else "TIDAK TAHU",
        "excerpt_bytes":len(raw),"excerpt_hex":hx(raw) if raw else "TIDAK TAHU: table base not statically addressable in Entry 1"})
    if raw:
        for off in range(0,len(raw)-3,4):
            value=int.from_bytes(raw[off:off+4],"little")
            dispatch_words.append({"jr_pc":f"0x{jr['pc']:08X}","table_address":f"0x{table_va:08X}",
                "table_file_offset":f"0x{base_off+off:X}","selector_index":off//4,
                "target_value":f"0x{value:08X}",
                "target_is_800F3830":"YES" if value==0x800F3830 else "NO",
                "target_is_800F5D08":"YES" if value==0x800F5D08 else "NO"})
write_tsv("DT3_JR_DISPATCH_TABLES.tsv",dispatch_rows,
    ["jr_pc","jr_bytes","table_address","table_file_offset","selector_register","selector_source","range_check","entry_count","excerpt_bytes","excerpt_hex"])
write_tsv("DT4_INDIRECT_TABLE_TARGETS.tsv",dispatch_words,
    ["jr_pc","table_address","table_file_offset","selector_index","target_value","target_is_800F3830","target_is_800F5D08"])
key=[r for r in dispatch_rows if r["jr_pc"]=="0x800F5CE0"]
(OUT/"DT3_JR_V0_TABLE.txt").write_text(
    "JR_PC=0x800F5CE0\n"+
    (f"TABLE_ADDRESS={key[0]['table_address']}\nTABLE_FILE_OFFSET={key[0]['table_file_offset']}\n"
     f"SELECTOR_REGISTER={key[0]['selector_register']}\nSELECTOR_SOURCE={key[0]['selector_source']}\n"
     f"RANGE_CHECK={key[0]['range_check']}\nENTRY_COUNT={key[0]['entry_count']}\n"
     f"EXCERPT_BYTE_COUNT={key[0]['excerpt_bytes']}\nEXCERPT_HEX={key[0]['excerpt_hex']}\n"
     if key else "TABLE_ADDRESS=TIDAK TAHU: jr/table relation not resolved\n"),encoding="utf-8")
cond_rows=[]
for i in fitems:
    if i["op"] not in (1,4,5,6,7):continue
    regs=reg_sources(i)
    cond_rows.append({"branch_pc":f"0x{i['pc']:08X}","bytes":hx(i["bytes"]),
        "instruction":i["text"],"registers":",".join(rn(r) for r in regs),
        "register_origins":"; ".join(trace_origin(r,i["pc"],function_at(i["pc"])) for r in regs),
        "static_values":"; ".join(f"{rn(r)}={const_label(const_before(r,i['pc'],function_at(i['pc'])))}" for r in regs),
        "branch_target":f"0x{branch_target(i):08X}" if branch_target(i) is not None else "—"})
write_tsv("DT4_REGISTER_CONDITIONS.tsv",cond_rows,
          ["branch_pc","bytes","instruction","registers","register_origins","static_values","branch_target"])

# DU5: all supplied fee values remain hypotheses; compare three predeclared models.
obs={1:100,2:400,3:800,4:1600}
fee_dasar=100
# Independent lookup challenger; not copied from the supplied fee observations.
H2_LOOKUP={1:1,2:3,3:6,4:10}
rows=[]
for d,user_value in obs.items():
    h1=fee_dasar*(2**d)
    h2=fee_dasar*H2_LOOKUP[d]
    h3=fee_dasar if d==1 else fee_dasar*(2**d)
    rows.append({"distance_d":d,"fee_dasar_hypothesis":fee_dasar,"user_observation_hypothesis":user_value,
        "H1_fee_dasar_times_2powd":h1,"H1_match":"COCOK" if h1==user_value else "TIDAK COCOK",
        "H2_lookup_multiplier":H2_LOOKUP[d],"H2_predicted_fee":h2,
        "H2_match":"COCOK" if h2==user_value else "TIDAK COCOK",
        "H3_user_rule_predicted_fee":h3,"H3_match":"COCOK" if h3==user_value else "TIDAK COCOK",
        "H1_prediction_other_base":"B*2^d","H2_prediction_other_base":f"B*{H2_LOOKUP[d]}",
        "H3_prediction_other_base":"B if d=1, otherwise B*2^d"})
write_tsv("DU5_FEE_MODEL_TEST.tsv",rows,
    ["distance_d","fee_dasar_hypothesis","user_observation_hypothesis",
     "H1_fee_dasar_times_2powd","H1_match","H2_lookup_multiplier","H2_predicted_fee","H2_match",
     "H3_user_rule_predicted_fee","H3_match","H1_prediction_other_base","H2_prediction_other_base","H3_prediction_other_base"])
(OUT/"DU5_MODEL_FALSIFIERS.txt").write_text(
    "STATUS=HYPOTHESIS_TEST_ONLY\n"
    "H1=fee_dasar*2^d; another base B predicts B*2^d; falsifier: one controlled distance/base yields a different fee.\n"
    "H2=predeclared lookup multipliers {1:1,2:3,3:6,4:10}; another base B predicts B*M[d]; falsifier: any controlled point disagrees with M[d]. It is a competing testable candidate, not ROM evidence and not copied from observations.\n"
    "H3=user rule: d=1 gives fee_dasar; d>=2 gives fee_dasar*2^d; another base B predicts B at d=1 and B*2^d at d>=2; falsifier: one controlled point violates this piecewise rule.\n"
    "All four d=1..4 points are tested. fee_dasar=100 is an input hypothesis, not a fitted parameter. No model is fitted from fewer than three points.\n",
    encoding="utf-8")

# Compact generated report: interpretation deliberately distinguishes static proof from user hypotheses.
lines=[
"# DT0–DT4 — raw-byte static audit",
"",
f"BASELINE_INCLUSIVE={BASELINE}",
f"SNAPSHOT_SHA={AUDIT_HEAD}",
f"DU0_SNAPSHOT_SHA={AUDIT_HEAD}",
f"DU0_TOTAL={len(ledger)} MANUSIA={humans} BOT={bots}",
"",
"## DT1",
f"Loop raw instruction window: {len(loop)} instructions, 0x{loop0:08X}–0x{loop1:08X}; complete bytes in DT1_LOOP_RAW.tsv.",
"Register origins for t0/t1/t2/a2/a3 are in DT1_REGISTER_ORIGINS.tsv; unresolved incoming definitions are kept as TIDAK TAHU.",
f"All direct Entry 1 stores resolved to 0x80139EFC: {len(writers)}; CLEAR stores: {len(clears)} (previous DS census expectation 7). See DT1_FEE_GLOBAL_CLEARS.tsv and DT1_CLEAR_CENSUS_SUMMARY.txt.",
"Tile field loads, packed tile+0x20 halfword path, and operands at 0x800ECAA0 are in their respective TSV files. The bit field is not assigned a gameplay name unless proven by its consumers.",
"",
"## DT2",
f"0x80102434: {hx(slot['bytes'])+' '+slot['text'] if slot else 'TIDAK TAHU'}.",
f"Second path returns through jr at 0x80102430; v0 before slot trace: {v0_before}; after slot trace: {v0_after}.",
"DATA.BIN excerpt: offset 0x11493C8, 64 bytes max, table base 0x8013B818; see DT2_TABLE_EXCERPT.txt.",
"",
"## DT3",
"CFG incoming edges are in DT3_CALLSITE_PREDECESSORS.tsv; selector conditions in DT4_REGISTER_CONDITIONS.tsv; indirect tables in DT3_JR_DISPATCH_TABLES.tsv and DT3_JR_V0_TABLE.txt.",
"State/event numeric value is reported only where a static branch operand or table entry proves it; otherwise it is TIDAK TAHU due to indirect/data-dependent dispatch.",
"",
"## DT4",
"All input values are user-supplied hypotheses, not observed ROM facts. H1, independent lookup H2 and piecewise user rule H3 are tested in DU5_FEE_MODEL_TEST.tsv.",
"fee_dasar=100 is an input hypothesis. H2 multipliers {1:1,2:3,3:6,4:10} are an independent falsifiable alternative, not ROM evidence.",
""
]
(OUT/"DT0_DT4_STATIC_AUDIT.md").write_text("\n".join(lines),encoding="utf-8")
