#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, os, struct, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_PATH, DATA_PATH, OUT = map(Path, sys.argv[1:4])
INV_PATH = Path("reports/stage1_economy/CI1_SELECTOR_RESOURCE_INVENTORY_2026-11-04.tsv")
BASELINE = os.environ.get("DW0_BASELINE", "2d334348b55dd672b3a2b0e428795c8ce817135b")
SNAPSHOT = os.environ.get("DW0_SNAPSHOT_SHA", subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip())
EXE_BASE, ENTRY_BASE, ENTRY_OFF = 0x80010000, 0x800AD450, 0x10BB000
EXE_SHA = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
DATA_SHA = "69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
ENTRY_SHA = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
ENTRY_SIZE = 596412
G_FEE = 0x80139EFC
SLOT_GLOBAL = 0x8013EA84
OUT.mkdir(parents=True, exist_ok=True)

def hx(b): return " ".join(f"{x:02X}" for x in b)
def h32(v): return f"0x{v & 0xffffffff:08X}"
def h16(v): return f"0x{v & 0xffff:04X}"
def write_tsv(name, rows, fields):
    with (OUT/name).open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for r in rows: w.writerow(r)
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024), b""): h.update(b)
    return h.hexdigest()
def git(args): return subprocess.check_output(["git", *args], text=True).strip()

if len(EXE_PATH.read_bytes()) != 385024 or sha(EXE_PATH) != EXE_SHA:
    raise SystemExit("EXE_IDENTITY_MISMATCH")
data = DATA_PATH.read_bytes()
if len(data) != 66015232 or hashlib.sha256(data).hexdigest() != DATA_SHA:
    raise SystemExit("DATA_BIN_IDENTITY_MISMATCH")
lbn, size = struct.unpack_from("<II", data, 0x4C)
entry_off = (lbn-212)*2048
entry = data[entry_off:entry_off+size]
if (lbn,size,entry_off,len(entry),hashlib.sha256(entry).hexdigest()) != (8778,ENTRY_SIZE,ENTRY_OFF,ENTRY_SIZE,ENTRY_SHA):
    raise SystemExit("ENTRY1_DIRECTORY_MAPPING_MISMATCH")

md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32|CS_MODE_LITTLE_ENDIAN)
md.detail = False
REG = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7",
       "s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
def rn(n): return "$"+REG[n]
def decode(blob, base, file_base):
    out={}
    for off in range(0,len(blob)-3,4):
        b=blob[off:off+4]; pc=base+off; word=int.from_bytes(b,"little")
        ins=next(md.disasm(b,pc,count=1),None)
        text=(ins.mnemonic+" "+ins.op_str).strip() if ins else f".word 0x{word:08X}"
        out[pc]={"pc":pc,"off":off,"fileoff":file_base+off,"bytes":b,"word":word,"text":text,
                 "op":word>>26,"rs":(word>>21)&31,"rt":(word>>16)&31,"rd":(word>>11)&31,
                 "sh":(word>>6)&31,"fn":word&63,"imm":((word&0xffff)^0x8000)-0x8000,
                 "uimm":word&0xffff,"target":word&0x03ffffff,"mnemonic":ins.mnemonic if ins else ".word",
                 "op_str":ins.op_str if ins else ""}
    return out
ins=decode(entry,ENTRY_BASE,ENTRY_OFF)
exe=decode(EXE_PATH.read_bytes(),EXE_BASE,0)

def row(i, origin, reason, base=ENTRY_BASE):
    return {"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
            "instruction":i["text"],"source_pc":h32(i["pc"]),"source":origin,"reason":reason}
def dest_reg(i):
    op,fn=i["op"],i["fn"]
    if op==0:
        if fn in (8,12,13,16,18,24,25,26,27): return None
        return i["rd"] if i["rd"] else None
    if op==3: return 31
    if op in (4,5,6,7,1,2,0x28,0x29,0x2a,0x2b,0x2e,0x38,0x39,0x3a,0x3b): return None
    if op in (8,9,10,11,12,13,14,15,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,
              0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37): return i["rt"] if i["rt"] else None
    return None
def last_def(reg, before, lo, code=ins):
    for pc in range(before-4,lo-4,-4):
        i=code.get(pc)
        if i and dest_reg(i)==reg: return i
    return None
def const_before(reg,before,lo,code=ins,depth=0,seen=None):
    if seen is None: seen=set()
    if depth>10 or (reg,before) in seen: return None
    seen.add((reg,before))
    if reg==0: return 0
    d=last_def(reg,before,lo,code)
    if not d: return None
    op,rs,rt,fn=d["op"],d["rs"],d["rt"],d["fn"]
    if op==0x0f: return (d["uimm"]<<16)&0xffffffff
    if op==0x0d:
        x=const_before(rs,d["pc"],lo,code,depth+1,seen.copy())
        return (x|d["uimm"])&0xffffffff if x is not None else None
    if op in (8,9):
        x=const_before(rs,d["pc"],lo,code,depth+1,seen.copy())
        return (x+d["imm"])&0xffffffff if x is not None else None
    if op==0 and fn in (0x21,0x23,0x25,0x24,0x26):
        x=const_before(rs,d["pc"],lo,code,depth+1,seen.copy())
        y=const_before(rt,d["pc"],lo,code,depth+1,seen.copy())
        if x is None or y is None:return None
        return {0x21:x+y,0x23:x-y,0x25:x|y,0x24:x&y,0x26:x^y}[fn]&0xffffffff
    if op==0 and fn in (0,2):
        x=const_before(rt,d["pc"],lo,code,depth+1,seen.copy())
        return ((x<<d["sh"]) if fn==0 else (x>>d["sh"]))&0xffffffff if x is not None else None
    return None
def trace_reg(reg,before,lo,code=ins,depth=0,seen=None):
    if seen is None: seen=set()
    if depth>6 or (reg,before) in seen:return "TIDAK TAHU: batas trace"
    seen.add((reg,before))
    if reg==0:return "$zero"
    d=last_def(reg,before,lo,code)
    if not d:return f"{rn(reg)} masuk/dinamis"
    s=f"{h32(d['pc'])} {d['text']} [{hx(d['bytes'])}]"
    if d["op"] in (8,9,10,11,12,13,14,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27):
        s+="; src="+trace_reg(d["rs"],d["pc"],lo,code,depth+1,seen.copy())
    elif d["op"]==0 and d["fn"] not in (8,9,16,18,12,13):
        s+="; src="+",".join(trace_reg(r,d["pc"],lo,code,depth+1,seen.copy()) for r in (d["rs"],d["rt"]))
    return s
def pointer_from_slot(reg,before,lo,slot_global=SLOT_GLOBAL,depth=0,seen=None):
    if seen is None:seen=set()
    if depth>8 or (reg,before) in seen:return False
    seen.add((reg,before))
    if reg==0:return False
    d=last_def(reg,before,lo,ins)
    if not d:return False
    op,rs,rt,fn=d["op"],d["rs"],d["rt"],d["fn"]
    if op in (0x23,0x20,0x21,0x24,0x25):
        base=const_before(rs,d["pc"],lo)
        if base is not None and ((base+d["imm"])&0xffffffff)==slot_global:
            return True
    if op in (8,9):
        return pointer_from_slot(rs,d["pc"],lo,slot_global,depth+1,seen.copy())
    if op==0 and fn in (0x21,0x23,0x25,0x24,0x26):
        return pointer_from_slot(rs,d["pc"],lo,slot_global,depth+1,seen.copy()) or pointer_from_slot(rt,d["pc"],lo,slot_global,depth+1,seen.copy())
    return False
def branch_target(i):
    op=i["op"]; pc=i["pc"]
    if op in (1,4,5,6,7):
        return (pc+4+(i["imm"]<<2))&0xffffffff
    if op in (2,3):
        return (((pc+4)&0xf0000000)|(i["target"]<<2))&0xffffffff
    return None
def branch_kind(i):
    op,rt=i["op"],i["rt"]
    if op==4:return "CONDITIONAL: "+rn(i["rs"])+" == "+rn(rt)
    if op==5:return "CONDITIONAL: "+rn(i["rs"])+" != "+rn(rt)
    if op==6:return "CONDITIONAL: "+rn(i["rs"])+" <= 0"
    if op==7:return "CONDITIONAL: "+rn(i["rs"])+" > 0"
    if op==1:
        return "CONDITIONAL: "+rn(i["rs"])+(" < 0" if rt in (0,2,16,18) else " >= 0" if rt in (1,3,17,19) else " REGIMM")
    if op==2:return "UNCONDITIONAL J"
    if op==3:return "UNCONDITIONAL JAL"
    return "OTHER"

# Approximate function starts, used only to bound local register-origin traces.
function_starts={ENTRY_BASE}
for i in ins.values():
    if i["op"]==3:
        t=((i["pc"]+4)&0xf0000000)|(i["target"]<<2)
        if t in ins:function_starts.add(t)
    if i["op"]==9 and i["rs"]==29 and i["rt"]==29 and i["imm"]<0:
        function_starts.add(i["pc"])
def function_at(pc):
    return max((x for x in function_starts if x<=pc),default=ENTRY_BASE)

# DW0 — inclusive baseline ledger, distinguishing analysis snapshot from publication.
ancestor=subprocess.run(["git","merge-base","--is-ancestor",BASELINE,SNAPSHOT]).returncode==0
if not ancestor: raise SystemExit("DW0_BASELINE_NOT_ANCESTOR_OF_SNAPSHOT")
revs=git(["rev-list","--reverse",f"{BASELINE}^..{SNAPSHOT}"]).splitlines()
ledger=[]; humans=bots=0
for rev in revs:
    fields=git(["show","-s","--format=%H%x09%an%x09%ae%x09%s",rev]).split("\t",3)
    sh,author,email,msg=fields
    bot=("github-actions" in author.lower() or "[bot]" in author.lower() or "41898282+github-actions" in email.lower())
    bots+=int(bot); humans+=int(not bot)
    files=git(["diff-tree","--root","--no-commit-id","--name-only","-r",rev]).splitlines()
    ledger.append({"sha_full":sh,"class":"BOT" if bot else "MANUSIA","author":author,
                   "author_email":email,"message":msg,"changed_files":";".join(files),
                   "source":"git rev-list baseline^..snapshot","reason":"commit masuk hitungan inklusif baseline"})
write_tsv("DW0_COMMIT_LEDGER.tsv",ledger,
          ["sha_full","class","author","author_email","message","changed_files","source","reason"])
head_analysis=git(["rev-parse","HEAD"])
if head_analysis != SNAPSHOT: raise SystemExit("DW0_HEAD_SNAPSHOT_MISMATCH")
write_tsv("DW0_SUMMARY.tsv",[{"baseline_inclusive":BASELINE,"snapshot_source_sha":SNAPSHOT,
    "head_at_analysis":head_analysis,"total_inclusive":len(ledger),"human":humans,"bot":bots,
    "publication_bot_commit_included":"NO; publication is after analysis snapshot",
    "reason":"snapshot_source_sha and HEAD_at_analysis are recorded separately; publication commit is outside this ledger"}],
    ["baseline_inclusive","snapshot_source_sha","head_at_analysis","total_inclusive","human","bot",
     "publication_bot_commit_included","reason"])

# DW1 — read every byte from the 12 selector-linked DATA.BIN extents, then parse 1-byte header + 30-byte records.
expected={0x276,0x277,0x278,0x279,0x27a,0x27b,0x27c,0x27e,0x27f,0x285,0x286,0x287}
with INV_PATH.open(encoding="utf-8",newline="") as f:
    inv=list(csv.DictReader(f,delimiter="\t"))
resources=[]
for r in inv:
    rid=int(r["resource_id_hex"],16)
    if rid in expected:
        resources.append({"selector":int(r["selector_byte"],0),"resource_id":rid,
                          "offset":int(r["data_bin_offset"],16),"size":int(r["size_bytes"])})
if {r["resource_id"] for r in resources} != expected or len(resources)!=12:
    raise SystemExit("DW1_SELECTOR_RESOURCE_INVENTORY_SET_MISMATCH")
resource_rows=[]; hist_rows=[]; excerpt_lines=[]; total_hist=Counter(); total_records=0
for r in sorted(resources,key=lambda x:x["selector"]):
    off,size=r["offset"],r["size"]
    blob=data[off:off+size]
    if len(blob)!=size: raise SystemExit(f"DW1_RESOURCE_TRUNCATED_{r['resource_id']:03X}")
    rem=(size-1)%0x1e
    if rem: raise SystemExit(f"DW1_RECORD_SIZE_REMAINDER_{r['resource_id']:03X}_{rem}")
    n=(size-1)//0x1e
    head=blob[0]
    h=Counter(); missing=truncated=0
    for j in range(n):
        start=1+j*0x1e
        rec=blob[start:start+0x1e]
        if len(rec)==0: missing+=1; continue
        if len(rec)<0x1e: truncated+=1
        h[rec[0]]+=1
    total_hist.update(h); total_records+=n
    for val,count in sorted(h.items()):
        hist_rows.append({"resource_id":f"0x{r['resource_id']:03X}","selector":f"0x{r['selector']:03X}",
                          "byte_value":f"0x{val:02X}","count":count,"source_offset":h32(off+1),
                          "reason":"histogram byte pertama tiap record 0x1E B; tidak menganggap byte sebagai label gameplay"})
    resource_rows.append({"selector":f"0x{r['selector']:03X}","resource_id":f"0x{r['resource_id']:03X}",
      "data_bin_offset":h32(off),"size_bytes":size,"header_byte":f"0x{head:02X}",
      "record_size":"0x1E","record_count_by_extent":n,"size_remainder":rem,
      "count_byte_1":h.get(1,0),"count_byte_5":h.get(5,0),
      "records_without_byte_00":missing,"truncated_records":truncated,
      "tile20_initial_word":"0xF020","tile20_bits12_15":"0xF","tile20_bits8_11":"0x0",
      "tile20_initialized_record_count":n,"source":"CI1 selector inventory + verified DATA.BIN SHA",
      "reason":"extent = 1-byte header + N full 0x1E-byte records; N is derived from extent length"})
    excerpt=blob[:64]
    excerpt_lines.append(f"RESOURCE=0x{r['resource_id']:03X} SELECTOR=0x{r['selector']:03X} OFFSET=0x{off:X} SIZE={size} EXCERPT_BYTES={len(excerpt)}\nHEX={hx(excerpt)}")
if total_records != 415: raise SystemExit(f"DW1_TOTAL_RECORD_COUNT_MISMATCH_{total_records}")
for val,count in sorted(total_hist.items()):
    hist_rows.append({"resource_id":"TOTAL","selector":"ALL","byte_value":f"0x{val:02X}","count":count,
                      "source_offset":"MULTIPLE","reason":"gabungan 12 resource yang lolos verifikasi extent"})
resource_rows.append({"selector":"ALL","resource_id":"TOTAL","data_bin_offset":"MULTIPLE","size_bytes":sum(r["size"] for r in resources),
 "header_byte":"MULTIPLE","record_size":"0x1E","record_count_by_extent":total_records,"size_remainder":0,
 "count_byte_1":total_hist.get(1,0),"count_byte_5":total_hist.get(5,0),
 "records_without_byte_00":0,"truncated_records":0,"tile20_initial_word":"0xF020",
 "tile20_bits12_15":"0xF","tile20_bits8_11":"0x0","tile20_initialized_record_count":total_records,
 "source":"verified extents across all 12 selector resources","reason":"aggregate row; runtime initializer applies per loaded tile"})
write_tsv("DW1_RESOURCE_SUMMARY.tsv",resource_rows,
 ["selector","resource_id","data_bin_offset","size_bytes","header_byte","record_size","record_count_by_extent",
  "size_remainder","count_byte_1","count_byte_5","records_without_byte_00","truncated_records",
  "tile20_initial_word","tile20_bits12_15","tile20_bits8_11","tile20_initialized_record_count","source","reason"])
write_tsv("DW1_BYTE00_HISTOGRAM.tsv",hist_rows,
 ["resource_id","selector","byte_value","count","source_offset","reason"])
(OUT/"DW1_RESOURCE_EXCERPTS.txt").write_text("\n\n".join(excerpt_lines)+"\n",encoding="utf-8")

# DW2 — every direct control-flow edge into the requested labels, the global fee/accumulator flow and helper raw code.
targets=[0x800ECAD0,0x800ECB4C,0x800ECB88,0x800ECBBC]
edge_rows=[]
for i in ins.values():
    dst=branch_target(i)
    if dst not in targets: continue
    if 0x800EC9CC <= i["pc"] <= 0x800ECBD4: continue
    edge_rows.append({"target_pc":h32(dst),"source_pc":h32(i["pc"]),
      "file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),"instruction":i["text"],
      "edge_kind":branch_kind(i),"condition":branch_kind(i) if i["op"] not in (2,3) else "always",
      "source":"full Entry 1 direct branch/J/JAL scan",
      "reason":"direct target matches label; source PC is outside 0x800EC9CC..0x800ECBD4"})
write_tsv("DW2_EXTERNAL_ENTRIES.tsv",edge_rows,
 ["target_pc","source_pc","file_offset","bytes","instruction","edge_kind","condition","source","reason"])

flow_pcs=[0x800EC9CC,0x800ECA2C,0x800ECA34,0x800ECA3C,0x800ECA44,0x800ECA48,
          0x800ECA4C,0x800ECA50,0x800ECA58,0x800ECA5C,0x800ECA60,0x800ECA64,
          0x800ECA7C,0x800ECAD0,0x800ECAD4,0x800ECAD8,0x800ECAE0,
          0x800ECB0C,0x800ECB4C,0x800ECB58,0x800ECB60,0x800ECB70,0x800ECB88,
          0x800ECBA8,0x800ECBB0,0x800ECBB4,0x800ECBB8,0x800ECBBC,0x800ECBC0,0x800ECBC8]
flow_rows=[]
for pc in flow_pcs:
    i=ins.get(pc)
    if not i: continue
    role="raw instruction in fee/debit path"
    if pc==0x800ECA64: role="writes loop accumulator to global 0x80139EFC"
    if pc==0x800ECAD0: role="loads helper argument a0 from stack+0x18; runtime value dynamic"
    if pc==0x800ECAD4: role="calls FUN_8001552C; returned v0 is consumed by following store"
    if pc==0x800ECAE0: role="overwrites global 0x80139EFC with the helper return value in v0"
    if pc==0x800ECBA8: role="reads u16 from global 0x80139EFC before negation"
    if pc==0x800ECBB0: role="negates the dynamically loaded global value"
    if pc==0x800ECBB8: role="stores negated value as halfword at manager base+0x2EE"
    if pc==0x800ECBBC: role="loads second helper argument from stack+0x18"
    if pc==0x800ECBC0: role="second JAL to FUN_8001552C in this code window"
    flow_rows.append({"pc":h32(pc),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
      "instruction":i["text"],"global_80139EFC_role":role,
      "source":"verified Entry 1 bytes, offset=0x10BB000+(PC-0x800AD450)",
      "reason":"PC-specific instruction decode; dynamic load/JAL return is not mislabeled as a constant"})
write_tsv("DW2_FEE_DEBIT_FLOW.tsv",flow_rows,
 ["pc","file_offset","bytes","instruction","global_80139EFC_role","source","reason"])

# Find all direct JALs to 0x8001552C in Entry 1 and dump each call's nearby context.
helper_calls=[]
for i in ins.values():
    if i["op"]==3 and branch_target(i)==0x8001552C:
        helper_calls.append(i)
helper_call_rows=[]
for call in helper_calls:
    lo=max(ENTRY_BASE,call["pc"]-0x10)
    hi=min(ENTRY_BASE+len(entry)-4,call["pc"]+0x14)
    for pc in range(lo,hi+1,4):
        i=ins.get(pc)
        if i:
            role="call-site context"
            if pc==call["pc"]-4: role="call argument setup immediately before JAL"
            if pc==call["pc"]: role="JAL FUN_8001552C"
            helper_call_rows.append({"call_pc":h32(call["pc"]),"pc":h32(pc),"file_offset":h32(i["fileoff"]),
              "bytes":hx(i["bytes"]),"instruction":i["text"],"role":role,
              "source":"Entry 1 direct JAL cross-reference","reason":"argument/value provenance needs runtime data where a load or stack byte is dynamic"})
write_tsv("DW2_HELPER_CALL_CONTEXT.tsv",helper_call_rows,
 ["call_pc","pc","file_offset","bytes","instruction","role","source","reason"])

# Decode FUN_8001552C and account for MIPS JR delay-slot return semantics.
helper_start=0x8001552C
helper_raw=[]; helper_ret=[]
for pc in range(helper_start,helper_start+0x400,4):
    i=exe.get(pc)
    if not i: break
    helper_raw.append({"pc":h32(pc),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
       "instruction":i["text"],"source":"SLPS_035.53 at EXE base 0x80010000",
       "reason":"raw helper instruction through JR RA and its executed delay slot"})
    if i["op"]==0 and i["fn"]==8 and i["rs"]==31:
        d=last_def(2,pc,helper_start,exe)
        ret_origin=(f"{h32(d['pc'])} {d['text']} [{hx(d['bytes'])}]" if d else "TIDAK TAHU: v0 has no definition before JR")
        delay=exe.get(pc+4)
        delay_text=delay["text"] if delay else "TIDAK TAHU"
        delay_bytes=hx(delay["bytes"]) if delay else "TIDAK TAHU"
        returned=const_before(2,pc+8,helper_start,exe)
        helper_ret.append({"return_pc":h32(pc),"return_bytes":hx(i["bytes"]),
          "v0_before_delay_slot":ret_origin,"delay_slot_pc":h32(pc+4),
          "delay_slot_bytes":delay_bytes,"delay_slot_instruction":delay_text,
          "v0_after_delay_slot":h32(returned) if returned is not None else "TIDAK TAHU",
          "interpretation":"MIPS executes the JR delay slot before return; v0_after_delay_slot is the actual returned value"})
        if delay:
            helper_raw.append({"pc":h32(pc+4),"file_offset":h32(delay["fileoff"]),"bytes":hx(delay["bytes"]),
             "instruction":delay["text"],"source":"SLPS_035.53 at EXE base 0x80010000",
             "reason":"JR RA delay slot executes before control returns"})
        break
write_tsv("DW2_FUN_8001552C_RAW.tsv",helper_raw,
 ["pc","file_offset","bytes","instruction","source","reason"])
write_tsv("DW2_FUN_8001552C_RETURN.tsv",helper_ret,
 ["return_pc","return_bytes","v0_before_delay_slot","delay_slot_pc","delay_slot_bytes",
  "delay_slot_instruction","v0_after_delay_slot","interpretation"])


# Explicitly retain the corrected file offsets for the two byte+0x00 checks.
corrected=[]
for pc,what in [(0x800ECA2C,"lbu tile+0x00"),(0x800ECA34,"branch compare against immediate 5")]:
    i=ins[pc]
    corrected.append({"pc":h32(pc),"correct_file_offset":h32(ENTRY_OFF+(pc-ENTRY_BASE)),
      "bytes":hx(i["bytes"]),"instruction":i["text"],"source":"Entry 1 offset formula",
      "reason":what+"; corrected mapping replaces prior offset transcription"})
write_tsv("DW2_CORRECTED_FILE_OFFSETS.tsv",corrected,
 ["pc","correct_file_offset","bytes","instruction","source","reason"])

# DW3 — selector dispatcher raw instructions, index provenance, writer candidates and outer table.
dispatch_start,dispatch_end=0x800F5C98,0x800F5CE0
disp_rows=[]
for pc in range(dispatch_start,dispatch_end+4,4):
    i=ins.get(pc)
    if not i: continue
    disp_rows.append({"pc":h32(pc),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
      "instruction":i["text"],"source":"Entry 1 verified bytes","reason":"complete requested inclusive range 0x800F5C98..0x800F5CE0"})
write_tsv("DW3_JR_800F5CE0_RAW.tsv",disp_rows,
 ["pc","file_offset","bytes","instruction","source","reason"])

index_regs=[]
for pc in range(0x800F5C80,0x800F5CB4,4):
    i=ins.get(pc)
    if i and i["op"]==0 and i["fn"] in (0,2):
        # Shift that constructs/scales the selector index before the add at 0x800F5CB4.
        if pc <= 0x800F5CB0:
            src=i["rt"]; dst=i["rd"]
            origin=trace_reg(src,pc,function_at(pc))
            index_regs.append({"pc":h32(pc),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
              "instruction":i["text"],"source_register":rn(src),"source_origin":origin,
              "reason":"shift instruction in the index-building window"})
# Explicitly trace register feeding the lbu effective address.
read=ins.get(0x800F5CB8)
base_trace=trace_reg(read["rs"],read["pc"],function_at(read["pc"])) if read else "TIDAK TAHU"
index_origin=trace_reg(2,0x800F5CB0,function_at(0x800F5CB0))
write_tsv("DW3_SELECTOR_INDEX_ORIGIN.tsv",index_regs+[
 {"pc":"SUMMARY","file_offset":"—","bytes":"—","instruction":"lbu at 0x800F5CB8 reads tile-record+0x00 from base pointer 0x8013EA84 indexed by (tile-from-0x8013EA74 field+0x1F * 0x124)",
  "source_register":"$v0","source_origin":index_origin,
  "reason":"0x800F5C94 first reads current tile+0x1F; scale sequence 0x800F5CA0..0x800F5CB0 multiplies that byte by 0x124; 0x800F5CB4 adds pointer from 0x8013EA84; 0x800F5CB8 reads byte at +0x00; base-register origin: "+base_trace}],
 ["pc","file_offset","bytes","instruction","source_register","source_origin","reason"])

# Exact references to pointer slot 0x8013EA84 and all store candidates through a register
# whose local def-chain begins with a load from that slot.
slot_refs=[]; slot_stores=[]
for i in sorted(ins.values(),key=lambda x:x["pc"]):
    op=i["op"]
    if op in (0x23,0x20,0x21,0x24,0x25,0x2b,0x29,0x28):
        b=const_before(i["rs"],i["pc"],function_at(i["pc"]))
        ea=((b+i["imm"])&0xffffffff) if b is not None else None
        if ea==SLOT_GLOBAL:
            slot_refs.append({"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
              "instruction":i["text"],"access":"WRITE" if op in (0x2b,0x29,0x28) else "READ",
              "source":"absolute effective-address reconstruction","reason":"base constant plus displacement equals slot global 0x8013EA84"})
    if op in (0x28,0x29,0x2b):
        fs=function_at(i["pc"])
        if pointer_from_slot(i["rs"],i["pc"],fs):
            slot_stores.append({"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
              "instruction":i["text"],"function_start":h32(fs),"base_pointer_origin":trace_reg(i["rs"],i["pc"],fs),
              "value_origin":trace_reg(i["rt"],i["pc"],fs),
              "source":"local static def-chain from load of global 0x8013EA84",
              "reason":"candidate store through pointer fetched from slot; exact tile/index alias must still be checked"})
write_tsv("DW3_SLOT_GLOBAL_XREFS.tsv",slot_refs,
 ["pc","file_offset","bytes","instruction","access","source","reason"])
write_tsv("DW3_SELECTOR_FIELD_WRITER_CANDIDATES.tsv",slot_stores,
 ["pc","file_offset","bytes","instruction","function_start","base_pointer_origin","value_origin","source","reason"])

# Isolate stores to selected-tile byte +0x00 through the 0x8013EA84 pointer slot.
tile_byte0_writers=[]
tile_byte0_reads=[]
tile_plus1f_access=[]
slot_globals={0x8013EA74,0x8013EA84,0x8013EA88}
slot_xrefs=[]
for i in sorted(ins.values(),key=lambda x:x["pc"]):
    op=i["op"]; fs=function_at(i["pc"])
    isload=op in (0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27)
    isstore=op in (0x28,0x29,0x2A,0x2B,0x2E)
    if isload or isstore:
        base=const_before(i["rs"],i["pc"],fs)
        ea=((base+i["imm"])&0xffffffff) if base is not None else None
        if ea in slot_globals:
            slot_xrefs.append({"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
              "instruction":i["text"],"slot_global":h32(ea),"access":"WRITE" if isstore else "READ",
              "source":"absolute effective-address reconstruction",
              "reason":"resolved global address = base register + signed displacement"})
    if isstore and i["imm"]==0 and pointer_from_slot(i["rs"],i["pc"],fs,slot_global=0x8013EA84):
        tile_byte0_writers.append({"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
          "instruction":i["text"],"function_start":h32(fs),"base_pointer_origin":trace_reg(i["rs"],i["pc"],fs),
          "value_origin":trace_reg(i["rt"],i["pc"],fs),"source":"base-register def chain includes load through slot 0x8013EA84",
          "reason":"candidate write to selected-array record +0x00; array-object alias/runtime target index is not fully resolved"})
    if isload and i["imm"]==0 and pointer_from_slot(i["rs"],i["pc"],fs,slot_global=0x8013EA84):
        tile_byte0_reads.append({"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
          "instruction":i["text"],"function_start":h32(fs),"base_pointer_origin":trace_reg(i["rs"],i["pc"],fs),
          "source":"base-register def chain includes load through slot 0x8013EA84",
          "reason":"candidate read from selected-array record +0x00"})
    if (isload or isstore) and i["imm"]==0x1f and pointer_from_slot(i["rs"],i["pc"],fs,slot_global=0x8013EA74):
        tile_plus1f_access.append({"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
          "instruction":i["text"],"function_start":h32(fs),"access":"WRITE" if isstore else "READ",
          "base_pointer_origin":trace_reg(i["rs"],i["pc"],fs),
          "value_origin":trace_reg(i["rt"],i["pc"],fs) if isstore else "—",
          "source":"base-register def chain includes load through slot 0x8013EA74",
          "reason":"candidate access to source-array record +0x1F; exact record alias depends on dynamic index"})
write_tsv("DW3_TILE_ARRAY_SLOT_XREFS.tsv",slot_xrefs,
 ["pc","file_offset","bytes","instruction","slot_global","access","source","reason"])
write_tsv("DW3_EA84_TILE_BYTE00_READERS.tsv",tile_byte0_reads,
 ["pc","file_offset","bytes","instruction","function_start","base_pointer_origin","source","reason"])
write_tsv("DW3_EA84_TILE_BYTE00_WRITERS.tsv",tile_byte0_writers,
 ["pc","file_offset","bytes","instruction","function_start","base_pointer_origin","value_origin","source","reason"])
write_tsv("DW3_EA74_TILE_PLUS1F_ACCESS.tsv",tile_plus1f_access,
 ["pc","file_offset","bytes","instruction","function_start","access","base_pointer_origin","value_origin","source","reason"])

# Explicit indexed lookup chain: current record +0x1F selects another record whose +0x00 byte is the JR selector.
lookup_pcs=[0x800F5C70,0x800F5C74,0x800F5C7C,0x800F5C84,0x800F5C88,0x800F5C8C,0x800F5C90,
            0x800F5C94,0x800F5C98,0x800F5C9C,0x800F5CA0,0x800F5CA4,0x800F5CA8,0x800F5CAC,
            0x800F5CB0,0x800F5CB4,0x800F5CB8,0x800F5CC0,0x800F5CC4]
lookup_role={
 0x800F5C74:"loads base pointer from global slot 0x8013EA74",
 0x800F5C7C:"loads current tile index from global 0x8013EA88",
 0x800F5C84:"begin scaling current tile index",
 0x800F5C88:"index*9 step",
 0x800F5C8C:"index*0x124 final stride step",
 0x800F5C90:"adds current-tile-array base",
 0x800F5C94:"reads current tile record byte +0x1F; this byte is the next record index",
 0x800F5C98:"loads address high half for second tile-array slot",
 0x800F5C9C:"loads base pointer from global slot 0x8013EA84",
 0x800F5CA0:"begin multiplying tile+0x1F index",
 0x800F5CA4:"index*9 step",
 0x800F5CA8:"index*72 step",
 0x800F5CAC:"index*73 step",
 0x800F5CB0:"shifts to index*0x124",
 0x800F5CB4:"adds second tile-array base pointer",
 0x800F5CB8:"reads selected tile record byte +0x00; value becomes JR selector",
 0x800F5CC0:"checks selector < 9",
 0x800F5CC4:"branches to fallback when selector >= 9"
}
lookup_rows=[]
for pc in lookup_pcs:
    i=ins.get(pc)
    if i:
        lookup_rows.append({"pc":h32(pc),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
          "instruction":i["text"],"role":lookup_role.get(pc,"lookup chain instruction"),
          "source":"Entry 1 raw-byte decode","reason":"specific static dataflow role; dynamic pointer/index values remain unknown"})
write_tsv("DW3_INDEXED_TILE_BYTE_LOOKUP.tsv",lookup_rows,
 ["pc","file_offset","bytes","instruction","role","source","reason"])

# The 9-entry secondary jump table referenced by 0x800F5CC8..0x800F5CE0.
secondary_base=0x800AEB78
secondary_rows=[]
for idx in range(9):
    off=secondary_base-ENTRY_BASE+idx*4
    raw=entry[off:off+4]
    target=int.from_bytes(raw,"little")
    secondary_rows.append({"selector":idx,"slot_pc":h32(secondary_base+idx*4),
      "file_offset":h32(ENTRY_OFF+off),"bytes":hx(raw),"target":h32(target),
      "source":"DATA.BIN Entry 1 table bytes",
      "reason":"index 0..8 allowed by sltiu at 0x800F5CC0"})
write_tsv("DW3_SECONDARY_JR_800F5CE0_TABLE_9.tsv",secondary_rows,
 ["selector","slot_pc","file_offset","bytes","target","source","reason"])

# 64-entry outer dispatch table at 0x800AEA20.
table_base=0x800AEA20
table_off=table_base-ENTRY_BASE
outer_rows=[]; relevant=[]
for idx in range(64):
    off=table_off+idx*4
    if off<0 or off+4>len(entry): continue
    raw=entry[off:off+4]; target=int.from_bytes(raw,"little")
    inside=0x800F5C98 <= target <= 0x800F5E00
    r={"selector":idx,"slot_pc":h32(ENTRY_BASE+off),"file_offset":h32(ENTRY_OFF+off),
       "bytes":hx(raw),"target":h32(target),"points_into_dispatcher_area":"YES" if inside else "NO",
       "source":"DATA.BIN Entry 1 table bytes at 0x800AEA20",
       "reason":"little-endian 32-bit table entry; dispatcher area bounded 0x800F5C98..0x800F5E00"}
    outer_rows.append(r)
    if inside: relevant.append(r)
write_tsv("DW3_OUTER_JR_800F3788_TABLE_64.tsv",outer_rows,
 ["selector","slot_pc","file_offset","bytes","target","points_into_dispatcher_area","source","reason"])
write_tsv("DW3_OUTER_TABLE_DISPATCHER_TARGETS.tsv",relevant,
 ["selector","slot_pc","file_offset","bytes","target","points_into_dispatcher_area","source","reason"])

# DW4 — callers/writers and exact code for FUN_80102408; preserve symbolic fee_dasar hypothesis.
writer_pcs=[0x800D09C8,0x800DFA28,0x800EA1D4]
writer_context=[]
for wpc in writer_pcs:
    for pc in range(wpc-0x30,wpc+0x34,4):
        i=ins.get(pc)
        if i:
            writer_context.append({"writer_pc":h32(wpc),"pc":h32(pc),"file_offset":h32(i["fileoff"]),
              "bytes":hx(i["bytes"]),"instruction":i["text"],
              "role":"named fee-global writer" if pc==wpc else "caller/writer local context",
              "source":"Entry 1 raw bytes","reason":"context window only; does not assert a runtime argument constant"})
write_tsv("DW4_THREE_WRITER_CONTEXT.tsv",writer_context,
 ["writer_pc","pc","file_offset","bytes","instruction","role","source","reason"])

fee_target=0x80102408
call_rows=[]
for i in sorted(ins.values(),key=lambda x:x["pc"]):
    if i["op"]==3 and branch_target(i)==fee_target:
        fs=function_at(i["pc"])
        row0={"call_pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
          "instruction":i["text"],"function_start_heuristic":h32(fs),
          "a0_origin":trace_reg(4,i["pc"],fs),"a1_origin":trace_reg(5,i["pc"],fs),
          "a2_origin":trace_reg(6,i["pc"],fs),"a3_origin":trace_reg(7,i["pc"],fs),
          "source":"Entry 1 direct JAL scan","reason":"static argument provenance; memory-loaded values remain dynamic"}
        call_rows.append(row0)
write_tsv("DW4_CALLS_TO_FUN_80102408.tsv",call_rows,
 ["call_pc","file_offset","bytes","instruction","function_start_heuristic",
  "a0_origin","a1_origin","a2_origin","a3_origin","source","reason"])

# DW4 — build the complete direct-CFG region of FUN_80102408, including both sides of conditional branches.
fee_reach=set(); fee_delay_slots=set(); fee_external=[]
fee_stack=[fee_target]
fee_limit=fee_target+0x300
while fee_stack:
    pc=fee_stack.pop()
    if pc in fee_reach or pc<fee_target or pc>=fee_limit: continue
    i=ins.get(pc)
    if i is None: continue
    fee_reach.add(pc)
    op=i["op"]
    succ=[]
    if op in (1,4,5,6,7):
        fee_delay_slots.add(pc+4)
        succ.extend([pc+4,pc+8])
        t=branch_target(i)
        if t is not None: succ.append(t)
    elif op in (2,3):
        fee_delay_slots.add(pc+4)
        succ.append(pc+4)
        if op==3: succ.append(pc+8)
        else:
            t=branch_target(i)
            if t is not None: succ.append(t)
    elif op==0 and i["fn"]==8:
        fee_delay_slots.add(pc+4)
        succ.append(pc+4)
    elif op==0 and i["fn"]==9:
        fee_delay_slots.add(pc+4)
        succ.append(pc+4)
        fee_external.append({"source_pc":h32(pc),"bytes":hx(i["bytes"]),"instruction":i["text"],
          "target":"INDIRECT / TIDAK TAHU","reason":"jalr/jr non-ra is not statically resolved in this function"})
    elif pc in fee_delay_slots:
        succ=[]
    else:
        succ.append(pc+4)
    for nxt in succ:
        if nxt in fee_delay_slots:
            fee_stack.append(nxt)
        elif fee_target <= nxt < fee_limit:
            fee_stack.append(nxt)
        elif nxt != pc+4 and nxt >= fee_limit:
            fee_external.append({"source_pc":h32(pc),"bytes":hx(i["bytes"]),"instruction":i["text"],
              "target":h32(nxt),"reason":"direct control edge escapes bounded FUN_80102408 CFG region"})

fee_raw=[]; fee_returns=[]; fee_access_rows=[]; fee_store_candidates=[]
load_ops={0x20:"lb",0x21:"lh",0x22:"lwl",0x23:"lw",0x24:"lbu",0x25:"lhu",0x26:"lwr"}
store_ops={0x28:"sb",0x29:"sh",0x2A:"swl",0x2B:"sw",0x2E:"swr"}
for pc in sorted(fee_reach):
    i=ins[pc]
    fee_raw.append({"pc":h32(pc),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
      "instruction":i["text"],"source":"Entry 1 FUN_80102408 direct CFG",
      "reason":"reachable instruction; both conditional branch alternatives are retained"})
    if i["op"] in load_ops or i["op"] in store_ops:
        access="READ" if i["op"] in load_ops else "WRITE"
        fee_access_rows.append({"pc":h32(pc),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
          "instruction":i["text"],"access":access,"width":load_ops.get(i["op"],store_ops.get(i["op"])),
          "base_register":rn(i["rs"]),"displacement":i["imm"],
          "base_origin":trace_reg(i["rs"],pc,fee_target),
          "value_origin":trace_reg(i["rt"],pc,fee_target) if access=="WRITE" else "loaded value -> "+rn(i["rt"]),
          "source":"FUN_80102408 direct-CFG memory access",
          "reason":"all visible memory operations included; offset +0x1A is isolated in dedicated report"})
        if i["imm"]==0x1a:
            if access=="WRITE":
                fee_store_candidates.append({"pc":h32(pc),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
                  "instruction":i["text"],"store_width":store_ops[i["op"]],
                  "value_origin":trace_reg(i["rt"],pc,fee_target),"base_origin":trace_reg(i["rs"],pc,fee_target),
                  "source":"FUN_80102408 direct CFG store displacement +0x1A",
                  "reason":"exact displacement; object identity depends on runtime base pointer"})
    if i["op"]==0 and i["fn"]==8 and i["rs"]==31:
        delay=ins.get(pc+4)
        fee_returns.append({"return_pc":h32(pc),"bytes":hx(i["bytes"]),
          "delay_slot_pc":h32(pc+4) if delay else "TIDAK TAHU",
          "delay_slot_instruction":delay["text"] if delay else "TIDAK TAHU",
          "delay_slot_bytes":hx(delay["bytes"]) if delay else "TIDAK TAHU",
          "v0_before_delay_slot":trace_reg(2,pc,fee_target),
          "v0_after_delay_slot":trace_reg(2,pc+8,fee_target),
          "source":"FUN_80102408 direct CFG",
          "reason":"return path and executed JR delay slot; value may remain dynamic"})
write_tsv("DW4_FUN_80102408_RAW.tsv",fee_raw,
 ["pc","file_offset","bytes","instruction","source","reason"])
write_tsv("DW4_FUN_80102408_MEMORY_ACCESSES.tsv",fee_access_rows,
 ["pc","file_offset","bytes","instruction","access","width","base_register","displacement","base_origin","value_origin","source","reason"])
write_tsv("DW4_TILE_PLUS1A_ACCESSES.tsv",[r for r in fee_access_rows if r["displacement"]==0x1a],
 ["pc","file_offset","bytes","instruction","access","width","base_register","displacement","base_origin","value_origin","source","reason"])
write_tsv("DW4_TILE_PLUS1A_STORES.tsv",fee_store_candidates,
 ["pc","file_offset","bytes","instruction","store_width","value_origin","base_origin","source","reason"])
write_tsv("DW4_FUN_80102408_RETURNS.tsv",fee_returns,
 ["return_pc","bytes","delay_slot_pc","delay_slot_instruction","delay_slot_bytes",
  "v0_before_delay_slot","v0_after_delay_slot","source","reason"])
write_tsv("DW4_FUN_80102408_CONTROL_EDGES.tsv",fee_external,
 ["source_pc","bytes","instruction","target","reason"])


hyp=[]
for d in range(2,6):
    hyp.append({"distance_d":d,"fee_dasar":"SYMBOLIC / TIDAK TAHU",
      "H1":"fee_dasar * 2^d","H2prime":"fee_dasar * {2:4,3:8,4:16,5:32}[d]",
      "H3":"fee_dasar * 2^d","models_equivalent_for_d_ge_2":"YES",
      "falsifier":"satu nilai fee terukur pada d>=2 yang != fee_dasar*2^d memfalsifikasi aturan bersama",
      "discriminator_note":"d>=2 tidak membedakan H1/H2prime/H3; d=1 diperlukan untuk memisahkan H1 dari H2prime/H3",
      "user_observation_status":"HIPOTESIS PENGGUNA; bukan data ROM/runtime yang diverifikasi"})
hyp.append({"distance_d":1,"fee_dasar":"SYMBOLIC / TIDAK TAHU","H1":"2 * fee_dasar",
  "H2prime":"1 * fee_dasar","H3":"1 * fee_dasar","models_equivalent_for_d_ge_2":"N/A",
  "falsifier":"nilai d=1 memisahkan H1 dari H2prime/H3",
  "discriminator_note":"H2prime dan H3 tetap identik; butuh rumus/kasus lain untuk membedakan definisi",
  "user_observation_status":"HIPOTESIS PENGGUNA; bukan data ROM/runtime yang diverifikasi"})
write_tsv("DW4_FEE_MODELS_AND_FALSIFIERS.tsv",hyp,
 ["distance_d","fee_dasar","H1","H2prime","H3","models_equivalent_for_d_ge_2",
  "falsifier","discriminator_note","user_observation_status"])

# Compact text report with confidence boundaries and all relevant file links to raw artefacts.
lines=[
"# DW0–DW4 — audit statis raw DATA.BIN / Entry 1",
"",
f"BASELINE_INCLUSIVE={BASELINE}",
f"SNAPSHOT_SOURCE_SHA={SNAPSHOT}",
f"HEAD_AT_ANALYSIS={head_analysis}",
f"DW0_TOTAL_INCLUSIVE={len(ledger)} HUMAN={humans} BOT={bots}",
"",
"## DW0 — commit ledger",
"Ledger bersifat inklusif dari baseline sampai snapshot; commit publikasi Actions terjadi sesudah snapshot dan tidak masuk hitungan.",
"",
"## DW1 — 12 resource, tile byte +0x00",
f"Selector inventory yang diverifikasi: {len(resources)} resource; jumlah record dari 1-byte header + N record x 0x1E = {total_records}.",
f"Total byte +0x00 bernilai 1: {total_hist.get(1,0)}; bernilai 5: {total_hist.get(5,0)}.",
"Histogram byte ada di DW1_BYTE00_HISTOGRAM.tsv; ringkasan setiap resource dan initial tile+0x20 ada di DW1_RESOURCE_SUMMARY.tsv.",
"Record tanpa byte +0x00 dan record terpotong dihitung eksplisit; header byte dilaporkan tetapi tidak diasumsikan sebagai N.",
"FUN_800F7ADC menulis initializer tile+0x20 = 0xF020; sehingga nibble awal bits12–15=0xF dan bits8–11=0 untuk setiap tile yang diinisialisasi. Ini bukan field sumber resource.",
"Arti gameplay 1 dan 5 tidak ditetapkan dari histogram. Kode yang terverifikasi: value 1 mengambil cabang bookkeeping daftar tile pada loader; value 5 adalah filter pertama pada loop ekonomi. Label jenis/status gameplay tetap TIDAK TAHU.",
"",
"## Status per level",
"DW0: TUNTAS K4 — commit ledger inklusif dihitung dari git history pada snapshot; commit bot publikasi dipisahkan.",
"DW1: TUNTAS K4 untuk histogram/format resource dan initializer tile+0x20; arti gameplay nilai byte tetap TIDAK TAHU.",
"DW2: SEBAGIAN K4 — helper dan jalur normal statis terbukti; indirect entry/semantik gameplay lane masih perlu batasan tambahan.",
"DW3: SEBAGIAN K4 — formula lookup dan tabel terbukti; penulisan tile+0x1F/+0x00 dipetakan sebagai kandidat berdasarkan def-chain pointer, bukan alias runtime.",
"DW4: SEBAGIAN K4 — seluruh direct CFG helper dipetakan; fee_dasar/label semantik tile dan nilai dinamis yang tidak tersimpan statis tetap TIDAK TAHU.",
"",
"## DW2 — global 0x80139EFC dan helper",
"Loop 0x800ECA2C/0x800ECA34 membaca tile+0x00; bila byte=5 dan nibble bits12–15 tile+0x20 sama dengan t0 dinamis, loop menambahkan 1+nibble bits8–11 ke 0x80139EFC.",
"FUN_8001552C pada 0x8001552C menambahkan a0+a1 sebagai alamat, memuat u16, menambah 1, lalu menyimpan u16 itu. Tetapi nilai kembalian bukan u16 tersebut: delay slot JR RA di 0x80015544 mengatur v0=1 sebelum return.",
"Karena 0x800ECAD4 memanggil helper itu dan 0x800ECAE0 langsung menyimpan v0, jalur normal meng-overwrite akumulator loop di 0x80139EFC menjadi 1. 0x800ECBA8 kemudian membaca u16 global itu, 0x800ECBB0 menegasikan, dan delay slot 0x800ECBB8 menyimpan halfword hasilnya ke manager+0x2EE. Isi/arti gameplay lane +0x2EE tetap TIDAK TAHU.",
"Scan branch/J/JAL langsung ke label 0x800ECAD0, 0x800ECB4C, 0x800ECB88, 0x800ECBBC dari luar blok menghasilkan nol referensi langsung; target tidak langsung/JR yang tidak bisa ditetapkan dari byte statis tetap TIDAK TAHU. Karena itu kesimpulan nilai 1 berlaku pada jalur normal yang melewati JAL helper dan store 0x800ECAE0.",
"",
"## DW3 — jr 0x800F5CE0",
"0x800F5C74 memuat base pointer slot global 0x8013EA74; indeks record awal berasal dari global 0x8013EA88. Indeks ini dikali stride record 0x124, lalu 0x800F5C94 membaca byte current-record+0x1F.",
"Byte +0x1F tersebut kemudian dikali 0x124. Base pointer kedua dimuat dari slot 0x8013EA84; 0x800F5CB4 menambahkan base, dan 0x800F5CB8 membaca byte pada selected-record+0x00. Byte +0x00 itulah selector JR; 0x800F5CC0 mensyaratkan selector <9, sedangkan >=9 jatuh ke 0x800F5D88.",
"DW3_INDEXED_TILE_BYTE_LOOKUP.tsv merinci seluruh instruksi dan skala. DW3_EA74_TILE_PLUS1F_ACCESS.tsv memuat akses kandidat ke tile+0x1F; DW3_EA84_TILE_BYTE00_READERS.tsv/WRITERS.tsv memuat reader/writer kandidat byte +0x00. DW3_TILE_ARRAY_SLOT_XREFS.tsv mencakup slot EA74, EA84 dan EA88.",
"Slot global 0x8013EA84 sendiri ditulis pada dua PC statis yang terdeteksi (lihat DW3_TILE_ARRAY_SLOT_XREFS.tsv). Tabel 64-entri luar di 0x800AEA20 mengarah ke area dispatcher pada selector 9, 10, 12, 13, 14 dan 51.",
"",
"## DW4 — FUN_80102408 dan tile+0x1A",
"DW4_FUN_80102408_RAW.tsv kini memuat seluruh basic block yang dicapai dari entry 0x80102408 melalui kedua sisi branch, bukan berhenti pada JR RA pertama. DW4_FUN_80102408_MEMORY_ACCESSES.tsv memetakan semua akses memori yang terlihat; DW4_TILE_PLUS1A_ACCESSES.tsv mengisolasi displacement +0x1A.",
"Ketiga writer global pada 0x800D09C8, 0x800DFA28 dan 0x800EA1D4 masing-masing didahului JAL langsung ke 0x80102408 (lihat DW4_CALLS_TO_FUN_80102408.tsv dan DW4_THREE_WRITER_CONTEXT.tsv). Base/argumen dinamis tetap TIDAK TAHU kecuali register origin terbukti.",
"fee_dasar tetap simbolik/TIDAK TAHU kecuali sumbernya terbukti. H1/H2prime/H3 adalah hipotesis, bukan konstanta ROM. Untuk d>=2 ketiganya ekuivalen; satu nilai ukur pada d>=2 yang tidak sama dengan fee_dasar*2^d memfalsifikasi aturan bersama. d=1 memisahkan H1 dari H2prime/H3.",

"",
"## Validity",
"Input identity checks passed for EXE, DATA.BIN and DATA.BIN Entry 1. No emulator/game was run. No BIOS, savestate, raw DATA.BIN, ISO, EXE, screenshots, video, or frames are included in the committed outputs; the private input is temporary and cleaned by the workflow.",
"All findings are static (maximum K4). Dynamic values, unproven aliases, and gameplay labels remain TIDAK TAHU."
]
(OUT/"DW0_DW4_STATIC_AUDIT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
