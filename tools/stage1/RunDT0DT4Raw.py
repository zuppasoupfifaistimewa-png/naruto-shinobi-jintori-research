#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, os, re, struct, subprocess, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_PATH, DATA_PATH, OUT = map(Path, sys.argv[1:4])
BASELINE=os.environ.get("DT0_BASELINE","cc0fead8501722a6ea76fefda8caf2f41df4cd3c")
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
write_tsv("DT1_TILE_MEMORY_FIELDS.tsv",memrows,["pc","operation","base_reg","offset","byte_semantics"])

# Linear constant propagation over the helper is used only to find provable direct writers.
state=[None]*32;state[0]=0;writers=[]
for i in ins_for(0x800EC574,0x800ECB90):
    pc,op,rs,rt,rd,fn,imm=i["pc"],i["op"],i["rs"],i["rt"],i["rd"],i["fn"],i["imm"]
    base=state[rs]
    ea=((base+imm)&0xFFFFFFFF) if isinstance(base,int) else None
    if op in (0x28,0x29,0x2B,0x38,0x39,0x3A,0x3B) and ea==G_FEE:
        val=state[rt]
        isclear=(rt==0 or val==0)
        writers.append({"pc":f"0x{pc:08X}","file_offset":f"0x{i['fileoff']:X}",
                        "bytes":hx(i["bytes"]),"instruction":i["text"],"source_reg":rn(rt),
                        "value_origin":("ZERO_REGISTER" if rt==0 else str(val)),
                        "is_clear": "YES" if isclear else "NO",
                        "position_vs_loop":"BEFORE" if pc<loop0 else "INSIDE/AFTER"})
    if op==0x0F:state[rt]=(i["uimm"]<<16)&0xFFFFFFFF
    elif op in (8,9):
        x=state[rs];state[rt]=((x+imm)&0xFFFFFFFF) if isinstance(x,int) else f"COMPUTED@{pc:08X}"
    elif op==0x0D:
        x=state[rs];state[rt]=(x|i["uimm"]) if isinstance(x,int) else f"COMPUTED@{pc:08X}"
    elif op==0:
        if fn==0:state[rd]=(state[rt]<<i["sh"])&0xFFFFFFFF if isinstance(state[rt],int) else f"COMPUTED@{pc:08X}"
        elif fn==0x21:
            x,y=state[rs],state[rt];state[rd]=((x+y)&0xFFFFFFFF) if isinstance(x,int) and isinstance(y,int) else f"COMPUTED@{pc:08X}"
        elif fn==0x23:
            x,y=state[rs],state[rt];state[rd]=((x-y)&0xFFFFFFFF) if isinstance(x,int) and isinstance(y,int) else f"COMPUTED@{pc:08X}"
        else:
            d=reg_dest(i)
            if d is not None:state[d]=f"COMPUTED@{pc:08X}"
    elif op in (0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27):
        state[rt]=f"LOAD@{pc:08X}"
    elif op==3:state[31]=pc+8
    else:
        d=reg_dest(i)
        if d is not None:state[d]=f"UNKNOWN@{pc:08X}"
write_tsv("DT1_FEE_GLOBAL_WRITERS.tsv",writers,
          ["pc","file_offset","bytes","instruction","source_reg","value_origin","is_clear","position_vs_loop"])

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
(OUT/"DT2_SUMMARY.txt").write_text(
    f"DELAY_SLOT_PC=0x80102434\nDELAY_SLOT_BYTES={hx(slot['bytes']) if slot else 'TIDAK TAHU'}\n"
    f"DELAY_SLOT_INSTRUCTION={slot['text'] if slot else 'TIDAK TAHU'}\n"
    f"RETURN_PATH_2_PC=0x80102430\nV0_BEFORE_DELAY_SLOT={v0_before}\n"
    f"V0_AFTER_DELAY_SLOT={v0_after}\n"
    f"RETURN_VALUE_AT_JR={'TIDAK TAHU' if not slot else trace_origin(2,0x80102438,0x80102408)}\n",
    encoding="utf-8")

# DT3: direct control-flow predecessors, dispatcher/indirect-jump evidence, and index-global reads.
fstart,fend=0x800F3658,0x800F6100
fitems=ins_for(fstart,fend)
calls=(0x800F3830,0x800F5D08)
edges=[]
for i in fitems:
    op=i["op"];t=branch_target(i)
    if op in (4,5,6,7,1):
        cond=i["text"]
        for dest,edge in ((t,"TAKEN"),(i["pc"]+8,"NOT_TAKEN")):
            if fstart<=dest<=fend:
                edges.append({"from_pc":f"0x{i['pc']:08X}","to_pc":f"0x{dest:08X}",
                              "edge":edge,"condition":cond,"delay_slot":at(i["pc"]+4)["text"] if at(i["pc"]+4) else "TIDAK TAHU",
                              "operand_origin": "; ".join(trace_origin(r,i["pc"],fstart) for r in reg_sources(i))})
    elif op in (2,3) and t is not None and fstart<=t<=fend and op==2:
        edges.append({"from_pc":f"0x{i['pc']:08X}","to_pc":f"0x{t:08X}","edge":"DIRECT_JUMP",
                      "condition":"unconditional j","delay_slot":at(i["pc"]+4)["text"] if at(i["pc"]+4) else "TIDAK TAHU",
                      "operand_origin":"—"})
predrows=[]
for call in calls:
    incoming=[e for e in edges if int(e["to_pc"],16)==call]
    for e in incoming:
        predrows.append({"call_pc":f"0x{call:08X}",**e,"classification":"DIRECT_PREDECESSOR"})
    if not incoming:
        predrows.append({"call_pc":f"0x{call:08X}","from_pc":"TIDAK ADA EDGE LANGSUNG",
                         "to_pc":f"0x{call:08X}","edge":"LIKELY_INDIRECT_OR_CASE_ENTRY",
                         "condition":"TIDAK TAHU: tidak ada target branch/j statis langsung ke alamat JAL",
                         "delay_slot":"—","operand_origin":"periksa JR/function-pointer dispatcher",
                         "classification":"NO_DIRECT_PREDECESSOR"})
write_tsv("DT3_CALLSITE_PREDECESSORS.tsv",predrows,
          ["call_pc","from_pc","to_pc","edge","condition","delay_slot","operand_origin","classification"])
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

# DT4: user-supplied figures remain hypotheses, explicitly test the two distinct models on all four points.
obs={1:100,2:400,3:800,4:1600}
fee=100
rows=[]
for d,v in obs.items():
    h1=fee*(2**d)
    # H2 is the distinct fixed multiplier-lookup hypothesis carried forward from DS4.
    m={1:1,2:4,3:8,4:16}[d]
    h2=fee*m
    rows.append({"distance_d":d,"fee_dasar_hypothesis":fee,"user_observation_hypothesis":v,
                 "H1_exponential_100x2powd":h1,"H1_result":"COCOK" if h1==v else "TIDAK COCOK",
                 "H2_lookup_multiplier":m,"H2_value":h2,"H2_result":"COCOK" if h2==v else "TIDAK COCOK"})
write_tsv("DT4_HYPOTHESIS_TEST.tsv",rows,
          ["distance_d","fee_dasar_hypothesis","user_observation_hypothesis","H1_exponential_100x2powd","H1_result","H2_lookup_multiplier","H2_value","H2_result"])

# Compact generated report: interpretation deliberately distinguishes static proof from user hypotheses.
lines=[
"# DT0–DT4 — raw-byte static audit",
"",
f"BASELINE_INCLUSIVE={BASELINE}",
f"SNAPSHOT_SHA={AUDIT_HEAD}",
f"DT0_TOTAL={len(ledger)} MANUSIA={humans} BOT={bots}",
"",
"## DT1",
f"Loop raw instruction window: {len(loop)} instructions, 0x{loop0:08X}–0x{loop1:08X}; complete bytes in DT1_LOOP_RAW.tsv.",
"Register origins for t0/t1/t2/a2/a3 are in DT1_REGISTER_ORIGINS.tsv; unresolved incoming definitions are kept as TIDAK TAHU.",
f"Direct writers of 0x80139EFC found before/inside the loop: {len(writers)}; exact CLEAR stores are marked is_clear=YES in DT1_FEE_GLOBAL_WRITERS.tsv.",
"Tile field loads, packed tile+0x20 halfword path, and operands at 0x800ECAA0 are in their respective TSV files. The bit field is not assigned a gameplay name unless proven by its consumers.",
"",
"## DT2",
f"0x80102434: {hx(slot['bytes'])+' '+slot['text'] if slot else 'TIDAK TAHU'}.",
f"Second path returns through jr at 0x80102430; v0 before slot trace: {v0_before}; after slot trace: {v0_after}.",
"DATA.BIN excerpt: offset 0x11493C8, 64 bytes max, table base 0x8013B818; see DT2_TABLE_EXCERPT.txt.",
"",
"## DT3",
"Call-site incoming edges and indirect dispatcher evidence are in DT3_CALLSITE_PREDECESSORS.tsv and DT3_INDIRECT_DISPATCHERS.tsv.",
"State/event numeric value is reported only where a static branch operand or table entry proves it; otherwise it is TIDAK TAHU due to indirect/data-dependent dispatch.",
"",
"## DT4",
"All four input values are user-supplied hypotheses, not observed ROM facts. H1=100×2^d; H2=100×multiplier lookup {1:1,2:4,3:8,4:16}.",
"Both candidate models are distinct and are checked against d=1..4; no parameter is fitted from fewer than three points.",
""
]
(OUT/"DT0_DT4_STATIC_AUDIT.md").write_text("\n".join(lines),encoding="utf-8")
