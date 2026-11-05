#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, os, re, struct, subprocess, sys
from collections import deque
from pathlib import Path
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_PATH, DATA_PATH, OUT = map(Path, sys.argv[1:4])
BASELINE = os.environ.get("DS0_BASELINE", "c6204f38495c9be76b18c76a9943f17ca835f2f3")
AUDIT_HEAD = os.environ.get("DS0_AUDIT_HEAD", BASELINE)
EXE_BASE, ENTRY_BASE = 0x80010000, 0x800AD450
ENTRY_OFF, ENTRY_SIZE = 0x10BB000, 596412
EXE_SHA = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
DATA_SHA = "69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
ENTRY_SHA = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
G_TABLE_PTR, G_INDEX, G_FEE, HELPER = 0x8013EA84, 0x8013EBB0, 0x80139EFC, 0x80102408
OUT.mkdir(parents=True, exist_ok=True)

def git(args):
    return subprocess.check_output(["git", *args], text=True).strip()
def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()
def hx(data):
    return " ".join(f"{x:02X}" for x in data)
def write_tsv(name, rows, fields=None):
    if fields is None:
        fields = list(rows[0]) if rows else ["STATUS"]
    with (OUT / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)

def commit_ledger():
    revs = git(["rev-list", "--reverse", f"{BASELINE}^..{AUDIT_HEAD}"]).splitlines()
    rows, humans, bots = [], 0, 0
    for rev in revs:
        sha1, author, email, msg = git(["show", "-s", "--format=%H%x09%an%x09%ae%x09%s", rev]).split("\t", 3)
        bot = ("github-actions" in author.lower() or "[bot]" in author.lower()
               or "41898282+github-actions" in email.lower())
        bots += int(bot)
        humans += int(not bot)
        files = git(["diff-tree", "--root", "--no-commit-id", "--name-only", "-r", rev]).splitlines()
        rows.append({"sha_full": sha1, "class": "BOT" if bot else "MANUSIA",
                     "author": author, "email": email, "message": msg, "changed_files": ";".join(files)})
    write_tsv("DS0_COMMIT_LEDGER.tsv", rows,
              ["sha_full","class","author","email","message","changed_files"])
    old_tsv = Path("reports/stage1_economy/DN0_COMMIT_LEDGER_2026-11-05.tsv")
    old_md = Path("reports/stage1_economy/DN0_COMMIT_LEDGER_REPORT_2026-11-05.md")
    old_contains = BASELINE in old_tsv.read_text(encoding="utf-8") if old_tsv.exists() else False
    old_cutoff = "TIDAK TAHU"
    if old_md.exists():
        m = re.search(r"Cutoff inklusif:.*?([0-9a-f]{40})", old_md.read_text(encoding="utf-8"))
        if m:
            old_cutoff = m.group(1)
    (OUT / "DS0_SUMMARY.txt").write_text(
        f"STATUS=TUNTAS\nK=K4\nBASELINE_INCLUSIVE={BASELINE}\nSNAPSHOT_HEAD={AUDIT_HEAD}\n"
        f"TOTAL={len(rows)}\nMANUSIA={humans}\nBOT={bots}\n"
        f"OLD_DN0_CUTOFF={old_cutoff}\nOLD_DN0_CONTAINS_BASELINE={'YES' if old_contains else 'NO'}\n",
        encoding="utf-8")
    return rows, humans, bots, old_cutoff, old_contains

def extract_entry1(data):
    if len(data) != 66015232 or hashlib.sha256(data).hexdigest() != DATA_SHA:
        raise ValueError("DATA_BIN_IDENTITY_MISMATCH")
    lbn, size = struct.unpack_from("<II", data, 0x4C)
    offset = (lbn - 212) * 2048
    raw = data[offset:offset + size]
    if (lbn, size, offset, len(raw), hashlib.sha256(raw).hexdigest()) != (
        8778, ENTRY_SIZE, ENTRY_OFF, ENTRY_SIZE, ENTRY_SHA
    ):
        raise ValueError("ENTRY1_DIRECTORY_MAPPING_MISMATCH")
    return raw

if len(EXE_PATH.read_bytes()) != 385024 or sha(EXE_PATH) != EXE_SHA:
    raise ValueError("EXE_IDENTITY_MISMATCH")
exe = EXE_PATH.read_bytes()
entry = extract_entry1(DATA_PATH.read_bytes())
md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_LITTLE_ENDIAN)
regnames = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3",
            "t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7",
            "t8","t9","k0","k1","gp","sp","fp","ra"]
def rn(n):
    return regnames[n]

def decode(module, raw, base, filebase):
    items = []
    for off in range(0, len(raw) - 3, 4):
        b = raw[off:off+4]
        pc = base + off
        word = int.from_bytes(b, "little")
        ins = next(md.disasm(b, pc, count=1), None)
        text = (ins.mnemonic + (" " + ins.op_str if ins and ins.op_str else "")) if ins else f".word 0x{word:08X}"
        items.append({"module":module,"pc":pc,"file_off":filebase+off,"bytes":b,"word":word,
                      "op":word>>26,"rs":(word>>21)&31,"rt":(word>>16)&31,
                      "rd":(word>>11)&31,"sh":(word>>6)&31,"fn":word&63,
                      "imm":((word&65535)^32768)-32768,"target":word&0x03FFFFFF,"text":text})
    return items
by = {
    "MAIN_EXE": decode("MAIN_EXE", exe[0x800:], EXE_BASE, 0x800),
    "ENTRY1": decode("ENTRY1", entry, ENTRY_BASE, 0)
}
pcmap = {i["pc"]:i for items in by.values() for i in items}
def call_target(i):
    return ((i["pc"] + 4) & 0xF0000000) | (i["target"] << 2)
starts = {m:set() for m in by}
for i in pcmap.values():
    if i["op"] == 3:
        t = call_target(i)
        if t in pcmap:
            starts[i["module"]].add(t)
    if i["op"] == 9 and i["rs"] == 29 and i["rt"] == 29 and i["imm"] < 0:
        starts[i["module"]].add(i["pc"])
for m, items in by.items():
    if items:
        starts[m].add(items[0]["pc"])
starts["ENTRY1"].add(HELPER)

def function(module, pc):
    if module == "ENTRY1" and 0x800EC574 <= pc <= 0x800ECBB8:
        return "FUN_800ec574"
    candidates = [x for x in starts[module] if x <= pc]
    if not candidates:
        return "TIDAK TAHU"
    return f"FUN_{max(candidates):08x}"

def fileoff(i):
    if i["module"] == "MAIN_EXE":
        return 0x800 + (i["pc"] - EXE_BASE)
    return ENTRY_OFF + (i["pc"] - ENTRY_BASE)

def prior(module, pc, n=12):
    items = by[module]
    k = next((j for j,x in enumerate(items) if x["pc"] == pc), None)
    return ([], b"") if k is None or k < n else (items[k-n:k], b"".join(x["bytes"] for x in items[k-n:k]))

def raw_context(module, pc, n=12):
    p, b = prior(module, pc, n)
    return " || ".join(f"0x{x['pc']:08X} {x['text']}" for x in p), hx(b), p

def basic_row(i):
    return {"module":i["module"],"pc":f"0x{i['pc']:08X}","file_offset":f"0x{fileoff(i):X}",
            "function":function(i["module"],i["pc"]),"bytes":hx(i["bytes"]),"instruction":i["text"]}

# DS1: exact address arithmetic and index provenance.
ledger, humans, bots, old_cutoff, old_contains = commit_ledger()
load_pc = 0x800D246C
trace_pcs = list(range(0x800D2450, 0x800D2484, 4))
rows = []
for pc in trace_pcs:
    i = pcmap.get(pc)
    if i:
        r = basic_row(i)
        r["role"] = ("LOAD_BASE_POINTER" if pc == 0x800D2450 else
                     "INDEX_SCALE" if 0x800D2454 <= pc <= 0x800D2468 else
                     "LOAD_BYTE" if pc == load_pc else "STORE_FEE_GLOBAL" if pc == 0x800D2480 else "CONTEXT")
        rows.append(r)
write_tsv("DS1_TABLE_ADDRESS_TRACE.tsv", rows,
          ["module","pc","file_offset","function","role","bytes","instruction"])
p, b = prior("ENTRY1", load_pc, 12)
write_tsv("DS1_PRELOAD_12_RAW.tsv", [basic_row(i) for i in p],
          ["module","pc","file_offset","function","bytes","instruction"])

def dest(i):
    op,fn = i["op"],i["fn"]
    if op == 0:
        if fn in (0x08,0x18,0x19,0x1A,0x1B):
            return None
        return i["rd"] if i["rd"] else None
    if op in (0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27):
        return i["rt"] if i["rt"] else None
    if op == 3:
        return 31
    return None
def sources(i):
    op,fn,rs,rt = i["op"],i["fn"],i["rs"],i["rt"]
    if op == 0:
        if fn in (0x00,0x02,0x03): return [rt]
        if fn in (0x08,0x09): return [rs]
        if fn in (0x10,0x12): return []
        return [rs,rt]
    if op == 0x0F: return []
    if op in (0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E): return [rs]
    if op in (0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27): return [rs]
    return []
def last_def(module, reg, before, low):
    for i in reversed(by[module]):
        if low <= i["pc"] < before and dest(i) == reg:
            return i
    return None

index_trace = []
pending = [(3,0x800D2454,"INDEX_v1")]
seen = set()
while pending and len(index_trace) < 16:
    reg,before,role = pending.pop(0)
    if (reg,before) in seen: continue
    seen.add((reg,before))
    d = last_def("ENTRY1",reg,before,0x800D15A8)
    if d is None:
        index_trace.append({"register":rn(reg),"role":role,"definition_pc":"TIDAK TAHU",
                            "instruction":"TIDAK TAHU: tidak ada definisi sebelum pemakaian dalam batas FUN_800D15A8; register masuk/argumen atau definisi luar fungsi.",
                            "source_registers":"TIDAK TAHU","definition_bytes":"","previous_12_hex":"TIDAK TAHU"})
        continue
    _, raw, _ = raw_context("ENTRY1",d["pc"],12)
    index_trace.append({"register":rn(reg),"role":role,"definition_pc":f"0x{d['pc']:08X}",
                        "instruction":d["text"],"source_registers":",".join(rn(x) for x in sources(d)),
                        "definition_bytes":hx(d["bytes"]),"previous_12_hex":raw})
    for sr in sources(d):
        if sr and len(index_trace)+len(pending) < 16:
            pending.append((sr,d["pc"],"OPERAND_OF_"+rn(reg)))
write_tsv("DS1_INDEX_ORIGIN_TRACE.tsv", index_trace,
          ["register","role","definition_pc","instruction","source_registers","definition_bytes","previous_12_hex"])

# Resolve direct effective-address reads/writes to the two globals.
def scan_global(target):
    reads, writes = [], []
    for module, items in by.items():
        st = [None]*32
        st[0] = 0
        for i in items:
            pc,op,rs,rt,rd,sh,fn,imm = (i[k] for k in ("pc","op","rs","rt","rd","sh","fn","imm"))
            if pc in starts[module] and pc != items[0]["pc"]:
                st = [None]*32
                st[0] = 0
            base = st[rs]
            ea = ((base+imm)&0xFFFFFFFF) if isinstance(base,int) else None
            if op in (0x20,0x21,0x23,0x24,0x25) and ea == target:
                reads.append({"module":module,"pc":f"0x{pc:08X}","file_offset":f"0x{fileoff(i):X}",
                              "function":function(module,pc),"bytes":hx(i["bytes"]),"instruction":i["text"]})
            if op in (0x28,0x29,0x2B) and ea == target:
                src = st[rt]
                origin = f"CONST_{src:08X}" if isinstance(src,int) else (
                    src if isinstance(src,str) else "TIDAK TAHU: register sumber tidak terpropagasi")
                ctxt, raw, _ = raw_context(module,pc,12)
                writes.append({"module":module,"pc":f"0x{pc:08X}","file_offset":f"0x{fileoff(i):X}",
                               "function":function(module,pc),"source_register":rn(rt),
                               "value_origin":origin,"bytes":hx(i["bytes"]),
                               "instruction":i["text"],"previous_12":ctxt,"excerpt_12_hex":raw})
            if op == 0x0F:
                st[rt] = (i["word"] & 0xFFFF) << 16
            elif op in (0x08,0x09,0x0C,0x0D,0x0E):
                x = st[rs]; u = i["word"] & 0xFFFF
                if op in (0x08,0x09):
                    st[rt] = (x+imm)&0xFFFFFFFF if isinstance(x,int) else f"COMPUTED_AT_0x{pc:08X}"
                elif isinstance(x,int):
                    st[rt] = (x&u) if op==0x0C else (x|u) if op==0x0D else (x^u)
                else: st[rt] = f"COMPUTED_AT_0x{pc:08X}"
            elif op == 0 and fn in (0x00,0x02,0x03,0x21,0x23,0x24,0x25,0x26):
                x,y=st[rs],st[rt]
                if fn==0x00 and isinstance(y,int): st[rd]=(y<<sh)&0xFFFFFFFF
                elif fn in (0x02,0x03) and isinstance(y,int): st[rd]=(y>>sh)&0xFFFFFFFF
                elif isinstance(x,int) and isinstance(y,int):
                    z={0x21:x+y,0x23:x-y,0x24:x&y,0x25:x|y,0x26:x^y}[fn]
                    st[rd]=z&0xFFFFFFFF
                else: st[rd]=f"COMPUTED_AT_0x{pc:08X}"
            elif op in (0x20,0x21,0x23,0x24,0x25):
                st[rt] = f"LOAD_GLOBAL_0x{target:08X}" if ea==target else f"LOAD_AT_0x{pc:08X}"
            elif op == 3:
                for r in (2,3,4,5,6,7,8,9,10,11,12,13,14,15,24,25):
                    st[r] = f"CALL_RETURN_AT_0x{pc:08X}"
    return reads,writes

ptr_reads, ptr_writes = scan_global(G_TABLE_PTR)
idx_reads, idx_writes = scan_global(G_INDEX)
write_tsv("DS1_TABLE_POINTER_GLOBAL_WRITERS.tsv",ptr_writes,
          ["module","pc","file_offset","function","source_register","value_origin","bytes","instruction","previous_12","excerpt_12_hex"])
write_tsv("DS3_INDEX_GLOBAL_WRITERS.tsv",idx_writes,
          ["module","pc","file_offset","function","source_register","value_origin","bytes","instruction","previous_12","excerpt_12_hex"])
write_tsv("DS3_INDEX_GLOBAL_READS.tsv",idx_reads,
          ["module","pc","file_offset","function","bytes","instruction"])

# DS2: direct JAL census and reachable MIPS control flow in FUN_80102408.
callers = []
for module,items in by.items():
    for i in items:
        if i["op"]==3 and call_target(i)==HELPER:
            ctxt,raw,_=raw_context(module,i["pc"],12)
            callers.append({"module":module,"pc":f"0x{i['pc']:08X}","function":function(module,i["pc"]),
                            "target":f"0x{HELPER:08X}","file_offset":f"0x{fileoff(i):X}",
                            "bytes":hx(i["bytes"]),"previous_12":ctxt,"excerpt_12_hex":raw})
write_tsv("DS2_FUN_80102408_CALLERS.tsv",callers,
          ["module","pc","function","target","file_offset","bytes","previous_12","excerpt_12_hex"])

def apply(i,state):
    s=list(state); op,rs,rt,rd,sh,fn,imm=(i[k] for k in ("op","rs","rt","rd","sh","fn","imm"))
    def put(r,v):
        if r: s[r]=v
    def con(v): return isinstance(v,int)
    x,y=s[rs],s[rt]; pc=i["pc"]; u=i["word"]&0xFFFF
    if op==0x0F: put(rt,(u<<16)&0xFFFFFFFF)
    elif op in (0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E):
        if op in (0x08,0x09): put(rt,(x+imm)&0xFFFFFFFF if con(x) else f"COMPUTED_AT_0x{pc:08X}")
        elif op==0x0C: put(rt,x&u if con(x) else f"COMPUTED_AT_0x{pc:08X}")
        elif op==0x0D: put(rt,x|u if con(x) else f"COMPUTED_AT_0x{pc:08X}")
        elif op==0x0E: put(rt,x^u if con(x) else f"COMPUTED_AT_0x{pc:08X}")
        else: put(rt,f"COMPUTED_AT_0x{pc:08X}")
    elif op in (0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27):
        put(rt,f"LOAD_AT_0x{pc:08X}:{i['text']}")
    elif op==0:
        if fn==0x00: put(rd,(y<<sh)&0xFFFFFFFF if con(y) else f"COMPUTED_AT_0x{pc:08X}")
        elif fn in (0x02,0x03): put(rd,(y>>sh)&0xFFFFFFFF if con(y) else f"COMPUTED_AT_0x{pc:08X}")
        elif fn in (0x21,0x23,0x24,0x25,0x26):
            if con(x) and con(y):
                z={0x21:x+y,0x23:x-y,0x24:x&y,0x25:x|y,0x26:x^y}[fn]
                put(rd,z&0xFFFFFFFF)
            elif fn==0x21 and x==0: put(rd,y)
            elif fn==0x21 and y==0: put(rd,x)
            else: put(rd,f"COMPUTED_AT_0x{pc:08X}")
        elif fn in (0x10,0x12): put(rd,f"HI_LO_AT_0x{pc:08X}")
        elif fn==0x09: put(rd,f"INDIRECT_CALL_RETURN_AT_0x{pc:08X}")
    return tuple(s)

def merge(old,new):
    if old is None: return new,True
    joined=tuple(a if a==b else None for a,b in zip(old,new))
    return joined,joined!=old

def cfg_helper():
    states={HELPER:tuple([0]+[None]*31)}
    q=deque([HELPER]); seen=set(); returns={}; exits=[]; steps=0
    def add(pc,state,reason):
        nonlocal steps
        steps+=1
        if pc not in pcmap or pcmap[pc]["module"]!="ENTRY1":
            exits.append((pc,reason)); return
        new,changed=merge(states.get(pc),state)
        if changed: states[pc]=new; q.append(pc)
    while q and steps<30000:
        pc=q.popleft(); state=states[pc]
        if (pc,state) in seen: continue
        seen.add((pc,state))
        i=pcmap[pc]; op,fn,rs,imm=i["op"],i["fn"],i["rs"],i["imm"]
        delay=pcmap.get(pc+4)
        ds=apply(delay,state) if delay and delay["module"]=="ENTRY1" else state
        if op==0 and fn==0x08:
            if rs==31: returns.setdefault(pc,set()).add(ds[2])
            else: exits.append((pc,"INDIRECT_JUMP_"+rn(rs)))
            continue
        if op==3:
            after=list(ds)
            for r in (2,3,4,5,6,7,8,9,10,11,12,13,14,15,24,25):
                after[r]=f"CALL_RETURN_AT_0x{pc:08X}"
            after[31]=pc+8
            add(pc+8,tuple(after),"AFTER_DIRECT_CALL")
            continue
        if op==0 and fn==0x09:
            after=list(ds)
            for r in (2,3,4,5,6,7,8,9,10,11,12,13,14,15,24,25):
                after[r]=f"INDIRECT_RETURN_AT_0x{pc:08X}"
            after[31]=pc+8
            add(pc+8,tuple(after),"AFTER_JALR")
            continue
        if op==2:
            target=call_target(i)
            if target in starts["ENTRY1"] and target!=HELPER:
                exits.append((pc,f"TAIL_JUMP_TO_0x{target:08X}"))
            else: add(target,ds,"DIRECT_JUMP")
            continue
        if op in (0x01,0x04,0x05,0x06,0x07,0x14,0x15,0x16,0x17):
            target=(pc+4+imm*4)&0xFFFFFFFF
            add(target,ds,"BRANCH_TAKEN")
            add(pc+8,ds,"BRANCH_NOT_TAKEN")
            continue
        add(pc+4,apply(i,state),"FALLTHROUGH")
    reachable=sorted({pc for pc,state in seen})
    dis=[]
    for pc in reachable:
        i=pcmap[pc]
        role="RETURN" if i["op"]==0 and i["fn"]==8 and i["rs"]==31 else "CALL" if i["op"]==3 else "BRANCH" if i["op"] in (1,4,5,6,7,0x14,0x15,0x16,0x17) else "INSTRUCTION"
        dis.append({"pc":f"0x{pc:08X}","file_offset":f"0x{fileoff(i):X}","function":"FUN_80102408",
                    "bytes":hx(i["bytes"]),"instruction":i["text"],"role":role})
    ret=[]
    for pc,values in sorted(returns.items()):
        i=pcmap[pc]; ctxt,raw,_=raw_context("ENTRY1",pc,12)
        for value in sorted(values,key=lambda v:str(v)):
            numeric=isinstance(value,int)
            ret.append({"return_pc":f"0x{pc:08X}","function":"FUN_80102408",
                        "return_v0":f"0x{value:08X}" if numeric else "TIDAK TAHU",
                        "status":"KONSTANTA_TERBUKTI" if numeric else "TIDAK TAHU",
                        "reason":"$v0 konstan dari aliran MIPS statis." if numeric else
                                 "Nilai $v0 berasal dari load/call/computation/merge yang tidak dapat ditentukan statis.",
                        "return_instruction":i["text"],"bytes":hx(i["bytes"]),
                        "previous_12":ctxt,"excerpt_12_hex":raw})
    return dis,ret,exits,steps

dis,rets,edges,cfg_steps=cfg_helper()
write_tsv("DS2_FUN_80102408_RAW_DISASSEMBLY.tsv",dis,
          ["pc","file_offset","function","bytes","instruction","role"])
write_tsv("DS2_FUN_80102408_RETURN_PATHS.tsv",rets,
          ["return_pc","function","return_v0","status","reason","return_instruction","bytes","previous_12","excerpt_12_hex"])
write_tsv("DS2_FUN_80102408_UNRESOLVED_EDGES.tsv",
          [{"pc":f"0x{pc:08X}","reason":reason} for pc,reason in edges],["pc","reason"])
(OUT/"DS2_FUN_80102408_SUMMARY.txt").write_text(
    f"FUNCTION=FUN_80102408\nDIRECT_JAL_CALLERS={len(callers)}\n"
    f"REACHABLE_RAW_INSTRUCTIONS={len(dis)}\nRETURN_PC_COUNT={len({r['return_pc'] for r in rets})}\n"
    f"RETURN_ROWS={len(rets)}\nUNRESOLVED_OR_TAIL_EDGES={len(edges)}\nCFG_WORKLIST_STEPS={cfg_steps}\n"
    f"CFG_LIMIT_REACHED={'YES' if cfg_steps>=30000 else 'NO'}\n"
    "Nonconstant, call-return, load-derived, or merged $v0 values are TIDAK TAHU.\n",
    encoding="utf-8")

# DS3: JALs to the manager helper and their raw pre-call context.
manager_calls=[]
for i in by["ENTRY1"]:
    if i["op"]==3 and call_target(i)==0x800EC574:
        ctxt,raw,_=raw_context("ENTRY1",i["pc"],12)
        delay=pcmap.get(i["pc"]+4); after=pcmap.get(i["pc"]+8)
        manager_calls.append({"pc":f"0x{i['pc']:08X}","function":function("ENTRY1",i["pc"]),
                              "jal":i["text"],"bytes":hx(i["bytes"]),
                              "previous_12":ctxt,"excerpt_12_hex":raw,
                              "delay_slot":delay["text"] if delay else "TIDAK TAHU",
                              "after_call":after["text"] if after else "TIDAK TAHU"})
write_tsv("DS3_FUN_800F3658_PRECALL_CONTEXT.tsv",manager_calls,
          ["pc","function","jal","bytes","previous_12","excerpt_12_hex","delay_slot","after_call"])

# DS4: distinguish evidence candidates from the full, still unproved fee chain.
candidate_pcs=[0x800ECA3C,0x800ECA44,0x800ECA48,0x800ECA4C,0x800ECA50,0x800ECA58,
               0x800ECA5C,0x800ECA60,0x800ECA64,0x800ECAA0,0x800ECAA4,0x800ECAA8,
               0x800ECBA8,0x800ECBB0,0x800ECBB8]
cand=[]
for pc in candidate_pcs:
    i=pcmap.get(pc)
    if i:
        ctxt,raw,_=raw_context("ENTRY1",pc,12)
        cand.append({"pc":f"0x{pc:08X}","function":function("ENTRY1",pc),
                     "instruction":i["text"],"bytes":hx(i["bytes"]),
                     "previous_12":ctxt,"excerpt_12_hex":raw,
                     "interpretation":"Kandidat pembacaan level/nibble, operasi multiply, atau transfer pending debit; rantai d->fee->0x80139EFC belum terbukti."})
write_tsv("DS4_LEVEL_FEE_CANDIDATE_WINDOWS.tsv",cand,
          ["pc","function","instruction","bytes","previous_12","excerpt_12_hex","interpretation"])
points=[]
for d,observed in [(2,400),(3,800),(4,1600)]:
    h1=100*(2**d); mult={2:4,3:8,4:16}[d]; h2=100*mult
    points.append({"d":d,"fee_dasar":100,"observasi_pengguna_hipotesis":observed,
                   "H1_fee_dasar_x_2_pow_d":h1,"H1":"COCOK" if h1==observed else "TIDAK COCOK",
                   "H2_multiplier_lookup":mult,"H2_fee_dasar_x_multiplier":h2,
                   "H2":"COCOK" if h2==observed else "TIDAK COCOK"})
write_tsv("DS4_USER_HYPOTHESIS_POINT_TESTS.tsv",points,
          ["d","fee_dasar","observasi_pengguna_hipotesis","H1_fee_dasar_x_2_pow_d","H1",
           "H2_multiplier_lookup","H2_fee_dasar_x_multiplier","H2"])

report=[
"# DS0-DS4 — audit statis raw-byte","",
f"Snapshot inklusif={AUDIT_HEAD}; baseline={BASELINE}.","",
"## DS0",
f"TUNTAS K4: {len(ledger)} commit = {humans} manusia + {bots} bot.",
f"Ledger DN0 sebelumnya berhenti di {old_cutoff}; baseline terdapat dalam TSV lama: {'YA' if old_contains else 'TIDAK'}.",
"Rincian commit, author/email, pesan, dan berkas perubahan: DS0_COMMIT_LEDGER.tsv.","",
"## DS1 — pembacaan byte pada FUN_800D15A8",
"PC 0x800D2450 membaca pointer dari slot global 0x8013EA84; ini alamat slot pointer, bukan nilai base tabel.",
"PC 0x800D2454-0x800D2468 menghitung base + 292*idx = base + 0x124*idx. Stride statis terverifikasi: 0x124 byte.",
"PC 0x800D246C melakukan lbu $v1,($v0). Asal indeks $v1 ditelusuri di DS1_INDEX_ORIGIN_TRACE.tsv. Jika register berasal dari argumen/definisi di luar fungsi, nilai numerik indeks = TIDAK TAHU.",
"Basis efektif tabel adalah nilai pointer yang dibaca dari global 0x8013EA84. Nilai pointer runtime = TIDAK TAHU kecuali writer langsung membuktikan konstanta; scan writer ada di DS1_TABLE_POINTER_GLOBAL_WRITERS.tsv.",
"Isi byte tabel aktual = TIDAK TAHU: lbu membaca melalui pointer runtime; byte instruksi tidak menyediakan isi memori yang ditunjuk. DS1_PRELOAD_12_RAW.tsv memuat 12 instruksi dan excerpt 48 byte; DS1_TABLE_ADDRESS_TRACE.tsv memuat operasi alamat per PC.","",
"## DS2 — FUN_80102408",
f"Jumlah direct JAL raw ke 0x80102408 di EXE + Entry1: {len(callers)}; PC/fungsi dan 12 instruksi sebelum call di DS2_FUN_80102408_CALLERS.tsv.",
f"Disassembly CFG reachable: {len(dis)} instruksi; return PC terjangkau: {len({r['return_pc'] for r in rets})}.",
"DS2_FUN_80102408_RAW_DISASSEMBLY.tsv memuat PC, file offset, byte mentah, dan instruksi. DS2_FUN_80102408_RETURN_PATHS.tsv memuat setiap return jr $ra; return nonkonstanta, load, call, atau hasil merge diberi TIDAK TAHU dengan alasan per PC.",
"Edge jump/tail/indirect yang tidak diikuti dicatat di DS2_FUN_80102408_UNRESOLVED_EDGES.tsv; karena itu daftar CFG reachable dibedakan dari klaim seluruh fungsi jika edge belum terurai.","",
"## DS3 — global index 0x8013EBB0",
f"Writer global langsung yang alamat efektifnya dapat dihitung: {len(idx_writes)}; reader langsung: {len(idx_reads)}.",
"Detail PC, fungsi, register sumber, asal nilai atau alasan TIDAK TAHU, 12 instruksi pra-store, dan excerpt 48 byte: DS3_INDEX_GLOBAL_WRITERS.tsv. Reader: DS3_INDEX_GLOBAL_READS.tsv.",
"FUN_800EC574 membaca halfword 0x8013EBB0 dan menggeser kiri satu bit untuk index 2-byte. Dua direct JAL ke helper yang ditemukan ada pada DS3_FUN_800F3658_PRECALL_CONTEXT.tsv; masing-masing berisi 12 instruksi sebelum call, delay slot, serta instruksi setelah call. Writer via pointer alias/dynamic yang tidak terurai = TIDAK TAHU.","",
"## DS4 — jalur biaya lompatan d>=2",
"Rantai level-sekarang vs target -> fee -> global 0x80139EFC = TIDAK TAHU. PC 0x800ECA3C-0x800ECA64 menunjukkan pemrosesan halfword/nibble tetapi tidak mengikat level sekarang ke target d. PC 0x800ECAA0 menjalankan mult dan 0x800ECAA4 mflo; hasil disimpan ke manager+0x4F0, bukan terbukti ke global fee. PC 0x800ECBB8 memindahkan nilai global fee yang sudah ada (dinegasikan) ke manager+0x2EE. Fragmen itu belum menghubungkan hasil multiply/target d dengan global 0x80139EFC.",
"H1 hipotesis: fee = fee_dasar x 2^d untuk d>=2. Falsifier: satu titik kontrol d>=2 dengan fee_dasar terukur yang menyimpang, atau data-flow raw yang membuktikan operand bukan d/hasil tidak menuju fee.",
"H2 hipotesis: multiplier diambil dari tabel menurut d (kandidat 4, 8, 16 untuk d=2,3,4). Falsifier: data-flow raw membuktikan tidak ada lookup berdasar d, atau lookup/titik kontrol menghasilkan multiplier berbeda.",
"Ketiga observasi pengguna d=2/3/4 dibandingkan untuk H1 dan H2 di DS4_USER_HYPOTHESIS_POINT_TESTS.tsv. Semua adalah HIPOTESIS pengguna, bukan fakta kode. H1 dan H2 sama-sama cocok 3/3 sehingga tidak terbedakan oleh tiga titik itu. Tidak dilakukan fitting dari kurang dari tiga titik.","",
"## Batas bukti",
"Statis maksimum K4; tanpa emulator. Nama fungsi di luar target JAL langsung adalah nearest-JAL/prologue heuristic. Global writer scan memakai effective address yang dapat direkonstruksi secara linear; alias tidak langsung dan aliran lintas fungsi yang tidak tertaut = TIDAK TAHU.","",
"## File pipeline yang diubah dalam commit pemicu",
"- .github/workflows/dq1-dq3-raw-static.yml",
"- tools/stage1/RunDS0DS4Raw.py"
]
(OUT/"DS0_DS4_STATIC_AUDIT_2026-11-05.md").write_text("\n".join(report)+"\n",encoding="utf-8")
print("DS0=PASS")
print(f"TOTAL={len(ledger)} MANUSIA={humans} BOT={bots}")
print(f"DS1_POINTER_WRITERS={len(ptr_writes)} INDEX_TRACE_ROWS={len(index_trace)}")
print(f"DS2_CALLERS={len(callers)} RETURNS={len({r['return_pc'] for r in rets})} REACHABLE={len(dis)}")
print(f"DS3_INDEX_WRITERS={len(idx_writes)} READS={len(idx_reads)} MANAGER_CALLERS={len(manager_calls)}")
print("DS4_CHAIN=TIDAK_TAHU")
