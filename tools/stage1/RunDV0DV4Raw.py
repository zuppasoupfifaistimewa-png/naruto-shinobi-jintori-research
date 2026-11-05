#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, os, struct, subprocess, sys
from pathlib import Path
from collections import Counter
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_PATH, DATA_PATH, OUT = map(Path, sys.argv[1:4])
BASELINE = "7040cd08a79107a45de6571e875de4fadb165c8a"
SNAPSHOT = os.environ.get("DT0_AUDIT_HEAD", subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip())
ENTRY_BASE=0x800AD450
ENTRY_OFF=0x10BB000
ENTRY_SIZE=596412
DATA_SHA="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
EXE_SHA="a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
ENTRY_SHA="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
OUT.mkdir(parents=True,exist_ok=True)
REG=["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
def rn(r): return REG[r]
def hx(b): return " ".join(f"{x:02X}" for x in b)
def hxpc(x): return f"0x{x:08X}" if x is not None else "TIDAK TAHU"
def write_tsv(name, rows, fields):
    with (OUT/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore")
        w.writeheader()
        for r in rows: w.writerow(r)
def git(args): return subprocess.check_output(["git",*args],text=True).strip()
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

if len(EXE_PATH.read_bytes())!=385024 or sha(EXE_PATH)!=EXE_SHA: raise SystemExit("EXE_IDENTITY_MISMATCH")
data=DATA_PATH.read_bytes()
if len(data)!=66015232 or hashlib.sha256(data).hexdigest()!=DATA_SHA: raise SystemExit("DATA_BIN_IDENTITY_MISMATCH")
lbn,size=struct.unpack_from("<II",data,0x4C)
entry_off=(lbn-212)*2048
entry=data[entry_off:entry_off+size]
if (lbn,size,entry_off,len(entry),hashlib.sha256(entry).hexdigest())!=(8778,ENTRY_SIZE,ENTRY_OFF,ENTRY_SIZE,ENTRY_SHA):
    raise SystemExit("ENTRY1_DIRECTORY_MAPPING_MISMATCH")

md=Cs(CS_ARCH_MIPS,CS_MODE_MIPS32|CS_MODE_LITTLE_ENDIAN); md.detail=False
ins={}
for off in range(0,len(entry)-3,4):
    b=entry[off:off+4]; pc=ENTRY_BASE+off; word=int.from_bytes(b,"little")
    cap=next(md.disasm(b,pc,count=1),None)
    text=(cap.mnemonic+" "+cap.op_str).strip() if cap else f".word 0x{word:08X}"
    ins[pc]={"pc":pc,"off":off,"fileoff":ENTRY_OFF+off,"bytes":b,"word":word,"text":text,
             "op":word>>26,"rs":(word>>21)&31,"rt":(word>>16)&31,"rd":(word>>11)&31,
             "sh":(word>>6)&31,"fn":word&63,"imm":((word&65535)^32768)-32768,"uimm":word&65535,
             "target":word&0x03FFFFFF}
def at(pc): return ins.get(pc)
def show(i):
    return {"pc":hxpc(i["pc"]),"file_offset":f"0x{i['fileoff']:X}","bytes":hx(i["bytes"]),
            "instruction":i["text"]}
def reg_dest(i):
    op,fn=i["op"],i["fn"]
    if op==0:
        if fn in (8,9,16,18,24,25,26,27): return 31 if fn==9 else None
        return i["rd"] or None
    if op in (2,3,4,5,6,7,1,0x2A,0x2B): return 31 if op==3 else None
    if op in (8,9,10,11,12,13,14,15,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,
              0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x3A,0x3B,0x3C,0x3D,0x3E,0x3F):
        return i["rt"] or None
    return None
def reg_sources(i):
    op,fn,rs,rt=i["op"],i["fn"],i["rs"],i["rt"]
    if op==0:
        if fn in (0,2,3): return [rt]
        if fn in (8,9): return [rs]
        if fn in (16,18,12,13): return []
        return [rs,rt]
    if op in (1,4,5): return [rs,rt] if op!=1 else [rs]
    if op in (6,7): return [rs]
    if op in (8,9,10,11,12,13,14): return [rs]
    if op in (0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27): return [rs]
    if op in (0x28,0x29,0x2A,0x2B,0x38,0x39,0x3A,0x3B): return [rs,rt]
    return []
def last_def(reg,before,lo):
    for pc in range(before-4,lo-4,-4):
        i=at(pc)
        if i and reg_dest(i)==reg: return i
    return None
def trace(reg,before,lo,depth=0,seen=None):
    if seen is None: seen=set()
    if depth>5 or (reg,before) in seen: return "TIDAK TAHU: batas trace/cycle"
    seen.add((reg,before))
    d=last_def(reg,before,lo)
    if d is None: return "TIDAK TAHU: register masuk/tidak ada definisi statis dalam batas"
    s=f"{hxpc(d['pc'])} {d['text']} [{hx(d['bytes'])}]"
    op=d["op"]
    if op in (8,9,10,11,12,13,14,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27) and d["rs"]:
        s+="; basis="+trace(d["rs"],d["pc"],lo,depth+1,seen.copy())
    elif op==0 and d["fn"] not in (0,2,3,8,9,16,18):
        s+="; src="+",".join(trace(r,d["pc"],lo,depth+1,seen.copy()) for r in reg_sources(d))
    return s
def const_before(reg,before,lo,depth=0,seen=None):
    if seen is None: seen=set()
    if depth>8 or (reg,before) in seen: return None
    seen.add((reg,before)); d=last_def(reg,before,lo)
    if d is None: return None
    op,rs,rt,fn=d["op"],d["rs"],d["rt"],d["fn"]
    if op==0x0F: return (d["uimm"]<<16)&0xFFFFFFFF
    if op in (8,9):
        x=const_before(rs,d["pc"],lo,depth+1,seen.copy())
        return ((x+d["imm"])&0xFFFFFFFF) if x is not None else None
    if op==0x0D:
        x=const_before(rs,d["pc"],lo,depth+1,seen.copy())
        return (x|d["uimm"])&0xFFFFFFFF if x is not None else None
    if op==0:
        if fn in (0,2):
            x=const_before(rt,d["pc"],lo,depth+1,seen.copy())
            return ((x<<d["sh"]) if fn==0 else (x>>d["sh"]))&0xFFFFFFFF if x is not None else None
        if fn in (0x21,0x23,0x24,0x25,0x26,0x27):
            x=const_before(rs,d["pc"],lo,depth+1,seen.copy()); y=const_before(rt,d["pc"],lo,depth+1,seen.copy())
            if x is None or y is None:return None
            return {0x21:(x+y),0x23:(x-y),0x24:(x&y),0x25:(x|y),0x26:(x^y),0x27:(~(x|y))&0xFFFFFFFF}[fn]&0xFFFFFFFF
    if op in (0x20,0x21,0x23,0x24,0x25):
        base=const_before(rs,d["pc"],lo,depth+1,seen.copy())
        if base is not None:
            ea=(base+d["imm"])&0xFFFFFFFF
            if ENTRY_BASE<=ea<ENTRY_BASE+len(entry):
                off=ea-ENTRY_BASE; width={0x20:1,0x21:2,0x23:4,0x24:1,0x25:2}[op]
                if off+width<=len(entry):
                    return int.from_bytes(entry[off:off+width],"little",signed=op in (0x20,0x21,0x23))
    return None
def vaddr_bytes(addr,n):
    if addr is None or not ENTRY_BASE<=addr<ENTRY_BASE+len(entry): return b""
    return entry[addr-ENTRY_BASE:addr-ENTRY_BASE+n]
function_starts={ENTRY_BASE}
for i in ins.values():
    if i["op"]==3:
        t=((i["pc"]+4)&0xF0000000)|(i["target"]<<2)
        if t in ins:function_starts.add(t)
    if i["op"]==9 and i["rs"]==29 and i["rt"]==29 and i["imm"]<0:function_starts.add(i["pc"])
def function_at(pc): return max((x for x in function_starts if x<=pc),default=ENTRY_BASE)
def branch_target(i):
    if i["op"] in (1,4,5,6,7): return (i["pc"]+4+(i["imm"]<<2))&0xFFFFFFFF
    if i["op"] in (2,3): return (((i["pc"]+4)&0xF0000000)|(i["target"]<<2))&0xFFFFFFFF
    return None
def reason_block(pc):
    m={
      0x800EC9CC:"CLEAR: store zero ke global 0x80139EFC sebelum scan tile",
      0x800ECA0C:"Ambil indeks tile dari manager/action +0x14f4",
      0x800ECA14:"Mulai pembentukan offset tile, scale 292 (0x124)",
      0x800ECA18:"Tambah indeks untuk membentuk indeks*9",
      0x800ECA1C:"Lanjutan scale indeks tile",
      0x800ECA20:"Lanjutan scale indeks tile",
      0x800ECA24:"Lanjutan scale indeks tile menjadi indeks*0x124",
      0x800ECA28:"Tambah pointer dasar tile dari slot global",
      0x800ECA2C:"Baca byte tile+0x00",
      0x800ECA34:"Syarat filter: byte tile+0x00 dibandingkan dengan t2=5",
      0x800ECA3C:"Baca halfword tile+0x20",
      0x800ECA44:"Ekstrak bit 12-15 dari tile+0x20",
      0x800ECA48:"Syarat kedua: nibble bits12-15 dibandingkan dengan t0 dinamis",
      0x800ECA4C:"Delay slot branch; geser halfword 8 bit untuk nibble bits8-11",
      0x800ECA50:"Baca akumulator global 0x80139EFC",
      0x800ECA58:"Tambah konstanta 1 untuk tile yang lolos filter",
      0x800ECA5C:"Mask nibble bits8-11 dengan 0xF",
      0x800ECA60:"Tambahkan 1+nibble bits8-11 ke akumulator",
      0x800ECA64:"Tulis akumulator baru ke 0x80139EFC",
      0x800ECA68:"Muat ulang indeks tile",
      0x800ECA70:"Naikkan indeks tile",
      0x800ECA74:"Simpan indeks tile",
      0x800ECA78:"Bandingkan indeks dengan batas a3 dinamis",
      0x800ECA7C:"Ulangi loop jika indeks belum mencapai a3",
      0x800ECAA0:"Perkalian operand dari global index 0x8013EBB0 dengan akumulator 0x80139EFC",
      0x800ECAA8:"Simpan hasil mult ke manager+0x4F0 (bergantung instruksi aktual)",
      0x800ECBB8:"Negasi nilai dinamis hasil baca akumulator global 0x80139EFC",
      0x800ECBBC:"Simpan halfword hasil negasi ke manager lane +0x2EE (relatif s0)"
    }
    return m.get(pc,"Instruksi raw di blok FUN_800EC574; periksa opcode/operand dan alur sekitar")
def fmt_ea(i,lo):
    b=const_before(i["rs"],i["pc"],lo)
    return (b+i["imm"])&0xFFFFFFFF if b is not None else None

# DV0 — inclusive ledger through the source snapshot of this run; publication bot commit is later.
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
write_tsv("DV0_COMMIT_LEDGER.tsv",ledger,["sha_full","class","author","author_email","message","changed_files","source","reason"])
write_tsv("DV0_SUMMARY.tsv",[{"baseline_inclusive":BASELINE,"snapshot_source_sha":SNAPSHOT,
    "snapshot_head_at_analysis":SNAPSHOT,"total_inclusive":len(ledger),"human":humans,"bot":bots,
    "publication_bot_commit_included":"NO; it is created after this source snapshot",
    "reason":"HEAD pada saat analyzer berjalan sama dengan snapshot sumber workflow; publikasi Actions terjadi sesudahnya"}],
    ["baseline_inclusive","snapshot_source_sha","snapshot_head_at_analysis","total_inclusive","human","bot","publication_bot_commit_included","reason"])

# DV1 — every instruction in the complete requested block, with the source PC for each row.
block0,block1=0x800EC9CC,0x800ECBD0
block=[i for i in sorted(ins.values(),key=lambda x:x["pc"]) if block0<=i["pc"]<=block1]
blockrows=[]
for i in block:
    r=show(i); r.update({"function":"FUN_800EC574 (address-range context)","source_pc":hxpc(i["pc"]),
      "source":"Entry 1 raw bytes; fileoff=0x10BB000+(PC-0x800AD450)","reason":reason_block(i["pc"])})
    blockrows.append(r)
write_tsv("DV1_FUN_800EC574_BLOCK_RAW.tsv",blockrows,
    ["pc","file_offset","bytes","instruction","function","source_pc","source","reason"])

# Exact dynamic accumulator use near 0x800ECBB8; do not label a loaded register as a constant.
accrows=[]
for pc in range(0x800ECBA0,0x800ECBD1,4):
    i=at(pc)
    if not i: continue
    ea=fmt_ea(i,function_at(pc)) if i["op"] in (0x20,0x21,0x23,0x24,0x25,0x28,0x29,0x2B) else None
    accrows.append({"pc":hxpc(pc),"file_offset":f"0x{i['fileoff']:X}","bytes":hx(i["bytes"]),
      "instruction":i["text"],"effective_address":hxpc(ea),
      "value_status":"TIDAK TAHU: runtime load/mutable accumulator" if i["op"] in (0x20,0x21,0x23,0x24,0x25) else "operasi/register statis pada instruksi",
      "source_pc":hxpc(pc),"reason":reason_block(pc) if pc in (0x800ECBB8,0x800ECBBC) else "konteks pemuatan/transformasi/penyimpanan nilai akumulator"})
write_tsv("DV1_ACCUMULATOR_TO_MANAGER_LANE.tsv",accrows,
    ["pc","file_offset","bytes","instruction","effective_address","value_status","source_pc","reason"])

# Find all reads at displacement +0x4F0 and list their first consumers until clobber.
reader_rows=[]
for i in ins.values():
    if i["op"] not in (0x20,0x21,0x23,0x24,0x25) or i["imm"]!=0x4F0: continue
    fs=function_at(i["pc"]); dest=i["rt"]; uses=[]
    for j in sorted((x for x in ins.values() if x["pc"]>i["pc"] and function_at(x["pc"])==fs),key=lambda x:x["pc"]):
        if dest in reg_sources(j):
            uses.append(f"{hxpc(j['pc'])} {hx(j['bytes'])} {j['text']}")
        if reg_dest(j)==dest: break
        if len(uses)>=16: break
    base_trace=trace(i["rs"],i["pc"],fs)
    reader_rows.append({"pc":hxpc(i["pc"]),"file_offset":f"0x{i['fileoff']:X}","bytes":hx(i["bytes"]),
      "function":f"FUN_{fs:08X} (heuristik)","instruction":i["text"],"base_register":rn(i["rs"]),
      "base_origin":base_trace,"destination_register":rn(dest),
      "first_uses":" || ".join(uses) if uses else "TIDAK TAHU: tidak ada pemakaian lokal sebelum register ditimpa/akhir fungsi",
      "classification":"MANAGER_CANDIDATE" if i["rs"]==16 else "BASE_IDENTITY_TIDAK_TAHU",
      "source_pc":hxpc(i["pc"]),
      "reason":"load dari offset +0x4F0; base $s0 cocok dengan objek manager pada store hasil perkalian di FUN_800EC574" if i["rs"]==16 else "offset +0x4F0 ditemukan, tetapi identitas base manager tidak terbukti hanya dari displacement"})
write_tsv("DV1_MANAGER_PLUS4F0_READERS.tsv",reader_rows,
    ["pc","file_offset","bytes","function","instruction","base_register","base_origin","destination_register","first_uses","classification","source_pc","reason"])

# DV2 — intraprocedural CFG and required selector values for both indirect dispatchers.
FSTART,FEND=0x800F3658,0x800F6100
region={pc:i for pc,i in ins.items() if FSTART<=pc<=FEND}
def succ_edges(i):
    pc=i["pc"]; op=i["op"]; t=branch_target(i); slot=at(pc+4)
    slottext=(f"{hxpc(slot['pc'])} {hx(slot['bytes'])} {slot['text']}" if slot else "TIDAK TAHU")
    out=[]
    if op in (1,4,5,6,7):
        if t in region: out.append((t,"TAKEN",slottext))
        if pc+8 in region: out.append((pc+8,"NOT_TAKEN",slottext))
    elif op==2:
        if t in region: out.append((t,"JUMP",slottext))
    elif op==3:
        if pc+8 in region: out.append((pc+8,"CALL_RETURN_FALLTHROUGH",slottext))
    elif op==0 and i["fn"]==8: pass
    else:
        if pc+4 in region: out.append((pc+4,"SEQUENTIAL",slottext))
    return out
graph={pc:succ_edges(i) for pc,i in region.items()}
def forward(start):
    seen=set(); stack=[start]
    while stack:
        p=stack.pop()
        if p in seen or p not in region: continue
        seen.add(p)
        stack.extend(d for d,_,_ in graph.get(p,[]))
    return seen
def reverse_to(target):
    rev={}
    for p,es in graph.items():
        for d,k,s in es: rev.setdefault(d,[]).append((p,k,s))
    seen=set(); stack=[target]
    while stack:
        p=stack.pop()
        if p in seen: continue
        seen.add(p)
        stack.extend(x[0] for x in rev.get(p,[]))
    return seen,rev
reach=forward(FSTART)
cfgrows=[]; pathrows=[]
dispatch_specs=[
 {"jr":0x800F3788,"selector_pc":0x800F3760,"required":44,"range_pc":0x800F3768,"range":64,
  "name":"manager+0x2E9","table":0x800AEA20,"slot_addr":0x800AEAD0,"target":0x800F3830},
 {"jr":0x800F5CE0,"selector_pc":0x800F5CB8,"required":2,"range_pc":0x800F5CC0,"range":9,
  "name":"byte at 0x800F5CB8 via pointer","table":0x800AEB78,"slot_addr":0x800AEB80,"target":0x800F5D08}
]
for spec in dispatch_specs:
    target=spec["jr"]; anc,rev=reverse_to(target); good=reach&anc
    # Include every branch/control edge in the start-to-target slice and both alternatives.
    for pc in sorted(good):
        i=region[pc]
        if i["op"] not in (1,4,5,6,7): continue
        regs=reg_sources(i)
        vals="; ".join(f"{rn(r)}={('TIDAK TAHU: dinamis' if const_before(r,pc,FSTART) is None else hxpc(const_before(r,pc,FSTART)))}" for r in regs)
        cond=i["text"]
        for dest,kind,slottext in graph.get(pc,[]):
            in_slice="YES" if dest in good else "NO"
            cfgrows.append({"target_jr":hxpc(target),"from_pc":hxpc(pc),"to_pc":hxpc(dest),
              "edge":kind,"branch_bytes":hx(i["bytes"]),"branch_instruction":i["text"],
              "condition_registers":",".join(rn(r) for r in regs),"static_values":vals,
              "delay_slot":slottext,"edge_can_reach_target":in_slice,"source_pc":hxpc(pc),
              "reason":"CFG intrafungsi; edge dipertahankan hanya sebagai relasi statis, bukan bukti kondisi runtime"})
    # One shortest representative instruction path, plus a predecessor set in CFG table above.
    from collections import deque
    q=deque([(FSTART,[FSTART])]); seen={FSTART}; found=None
    while q:
        p,path=q.popleft()
        if p==target: found=path; break
        for d,_,_ in graph.get(p,[]):
            if d not in seen: seen.add(d); q.append((d,path+[d]))
    if found:
        for n,p in enumerate(found):
            i=region[p]
            pathrows.append({"target_jr":hxpc(target),"step":n,"pc":hxpc(p),
              "file_offset":f"0x{i['fileoff']:X}","bytes":hx(i["bytes"]),"instruction":i["text"],
              "source_pc":hxpc(p),"reason":"salah satu jalur CFG terpendek dari entry fungsi; bukan satu-satunya jalur"})
    else:
        pathrows.append({"target_jr":hxpc(target),"step":"—","pc":"TIDAK TAHU","file_offset":"—","bytes":"—",
          "instruction":"TARGET_NOT_REACHED_BY_STATIC_CFG","source_pc":"—",
          "reason":"tidak ditemukan jalur intrafungsi dari FUN_800F3658 pada CFG konservatif"})
write_tsv("DV2_CFG_BRANCH_EDGES.tsv",cfgrows,
    ["target_jr","from_pc","to_pc","edge","branch_bytes","branch_instruction","condition_registers","static_values","delay_slot","edge_can_reach_target","source_pc","reason"])
write_tsv("DV2_REPRESENTATIVE_PATHS.tsv",pathrows,
    ["target_jr","step","pc","file_offset","bytes","instruction","source_pc","reason"])

selector_rows=[]
for s in dispatch_specs:
    load=at(s["selector_pc"]); chk=at(s["range_pc"]); br=at(s["range_pc"]+4)
    base=fmt_ea(load,function_at(load["pc"])) if load and load["op"] in (0x20,0x21,0x23,0x24,0x25) else None
    slotoff=ENTRY_OFF+(s["slot_addr"]-ENTRY_BASE)
    raw=vaddr_bytes(s["slot_addr"],4)
    selector_rows.append({"jr_pc":hxpc(s["jr"]),"selector_pc":hxpc(s["selector_pc"]),
      "selector_bytes":hx(load["bytes"]) if load else "TIDAK TAHU","selector_instruction":load["text"] if load else "TIDAK TAHU",
      "selector_required_for_target":s["required"],"selector_runtime_value":"TIDAK TAHU: lbu mengambil byte data runtime",
      "range_check_pc":hxpc(s["range_pc"]),"range_check":chk["text"] if chk else "TIDAK TAHU",
      "fallback_branch":br["text"] if br else "TIDAK TAHU","required_value_passes":f"{s['required']} < {s['range']} = YES",
      "base_origin":trace(load["rs"],load["pc"],FSTART) if load else "TIDAK TAHU",
      "table_base":hxpc(s["table"]),"slot_address":hxpc(s["slot_addr"]),
      "table_file_offset":f"0x{slotoff:X}","slot_bytes":hx(raw),"slot_target":hxpc(int.from_bytes(raw,"little")) if len(raw)==4 else "TIDAK TAHU",
      "source_pc":hxpc(s["selector_pc"]),"reason":"nilai selector yang diperlukan agar slot tabel menunjuk ke handler; tidak menyatakan bahwa runtime benar-benar memilih nilai ini"})
write_tsv("DV2_SELECTOR_REQUIREMENTS.tsv",selector_rows,
    ["jr_pc","selector_pc","selector_bytes","selector_instruction","selector_required_for_target","selector_runtime_value",
     "range_check_pc","range_check","fallback_branch","required_value_passes","base_origin","table_base","slot_address",
     "table_file_offset","slot_bytes","slot_target","source_pc","reason"])

# All direct byte/half/word stores to field +0x2E9 are writer candidates for the manager selector.
manager_writers=[]
for i in ins.values():
    if i["op"] not in (0x28,0x29,0x2B) or i["imm"]!=0x2E9: continue
    fs=function_at(i["pc"]); value=const_before(i["rt"],i["pc"],fs) if i["rt"] else 0
    manager_writers.append({"pc":hxpc(i["pc"]),"file_offset":f"0x{i['fileoff']:X}","bytes":hx(i["bytes"]),
      "function":f"FUN_{fs:08X} (heuristik)","instruction":i["text"],"base_register":rn(i["rs"]),
      "base_origin":trace(i["rs"],i["pc"],fs),"value_register":rn(i["rt"]),
      "value_origin":trace(i["rt"],i["pc"],fs) if i["rt"] else "ZERO_REGISTER",
      "value_static":hxpc(value),"can_write_44":"YES" if value==44 else ("NO" if value is not None else "TIDAK TAHU"),
      "source_pc":hxpc(i["pc"]),"reason":"store dengan displacement +0x2E9; kecocokan sebagai manager hanya jika base pointer memang objek manager"})
write_tsv("DV2_MANAGER_2E9_WRITER_CANDIDATES.tsv",manager_writers,
    ["pc","file_offset","bytes","function","instruction","base_register","base_origin","value_register","value_origin","value_static","can_write_44","source_pc","reason"])

# Selector-2 byte uses a0 + 4*index at 0x800F5CB8; find direct stores through a0 in same caller region.
sel2_store_rows=[]
for i in ins.values():
    if i["op"] not in (0x28,0x29,0x2B) or i["rs"]!=4 or not (FSTART<=i["pc"]<=FEND): continue
    fs=function_at(i["pc"]); val=const_before(i["rt"],i["pc"],FSTART) if i["rt"] else 0
    sel2_store_rows.append({"pc":hxpc(i["pc"]),"file_offset":f"0x{i['fileoff']:X}","bytes":hx(i["bytes"]),
      "function":f"FUN_{FSTART:08X} (caller region)","instruction":i["text"],"base_register":"a0",
      "value_origin":trace(i["rt"],i["pc"],FSTART) if i["rt"] else "ZERO_REGISTER",
      "value_static":hxpc(val),"address_relation":"candidate write through a0; exact scaled index/address equality TIDAK TAHU",
      "source_pc":hxpc(i["pc"]),"reason":"base register a0 matches selector table base register; pointer identity/time-of-write not established"})
write_tsv("DV2_SELECTOR2_A0_STORE_CANDIDATES.tsv",sel2_store_rows,
    ["pc","file_offset","bytes","function","instruction","base_register","value_origin","value_static","address_relation","source_pc","reason"])

# DV3 — inspect loader, find 30-byte record arrays in the DATA.BIN directory candidate list.
loader_pc=0x800F7ADC
loader_fs=function_at(loader_pc)
loader_end=min([x for x in function_starts if x>loader_fs] or [ENTRY_BASE+len(entry)])
# Keep loader window bounded to the recognized function or 0x600 instructions.
loader_ins=[i for i in sorted(ins.values(),key=lambda x:x["pc"]) if loader_pc<=i["pc"]<min(loader_end,loader_pc+0x1800)]
loader_rows=[]
for i in loader_ins:
    ismem=i["op"] in (0x20,0x21,0x23,0x24,0x25,0x28,0x29,0x2B)
    off=i["imm"] if ismem else None
    role="instruksi loader"
    if ismem and off is not None and 0<=off<0x1E and i["op"] in (0x20,0x21,0x23,0x24,0x25):
        role="kandidat baca field record sumber 0x1E B"
    if ismem and off in (0,0x20) and i["op"] in (0x28,0x29,0x2B):
        role="kandidat tulis field tile +0x00/+0x20"
    loader_rows.append({"pc":hxpc(i["pc"]),"file_offset":f"0x{i['fileoff']:X}","bytes":hx(i["bytes"]),
      "instruction":i["text"],"function":f"FUN_{loader_fs:08X} (heuristik; loader diminta 0x800F7ADC)",
      "memory_role":role,"base_origin":trace(i["rs"],i["pc"],loader_fs) if ismem else "—",
      "value_origin":trace(i["rt"],i["pc"],loader_fs) if ismem and i["op"] in (0x28,0x29,0x2B) else "—",
      "source_pc":hxpc(i["pc"]),"reason":"raw instruction di fungsi loader; klasifikasi berdasarkan opcode/displacement, belum menyamakan register pointer tanpa bukti"})
write_tsv("DV3_LOADER_FUN_800F7ADC_RAW.tsv",loader_rows,
    ["pc","file_offset","bytes","instruction","function","memory_role","base_origin","value_origin","source_pc","reason"])

# Adjacent load->store copies from a 30-byte source record into tile fields; report only direct dataflow candidates.
copy_rows=[]
for i in loader_ins:
    if i["op"] not in (0x20,0x21,0x24,0x25): continue
    dest=reg_dest(i)
    if dest is None: continue
    for j in loader_ins:
        if not (i["pc"]<j["pc"]<=i["pc"]+0x20): continue
        if j["op"] not in (0x28,0x29,0x2B) or j["rt"]!=dest or j["imm"] not in (0,0x20): continue
        copy_rows.append({"load_pc":hxpc(i["pc"]),"load_file_offset":f"0x{i['fileoff']:X}","load_bytes":hx(i["bytes"]),
          "load_instruction":i["text"],"source_field_offset":i["imm"],"source_base_register":rn(i["rs"]),
          "store_pc":hxpc(j["pc"]),"store_file_offset":f"0x{j['fileoff']:X}","store_bytes":hx(j["bytes"]),
          "store_instruction":j["text"],"destination_field_offset":j["imm"],"shared_value_register":rn(dest),
          "source_pc":hxpc(i["pc"]),"reason":"register hasil load dipakai langsung sebagai operand store dalam jarak <=0x20 byte; pointer identity tetap perlu cek base_origin"})
write_tsv("DV3_TILE_FIELD_COPY_CANDIDATES.tsv",copy_rows,
    ["load_pc","load_file_offset","load_bytes","load_instruction","source_field_offset","source_base_register",
     "store_pc","store_file_offset","store_bytes","store_instruction","destination_field_offset","shared_value_register","source_pc","reason"])

# Directory-like candidate table: (LBA,size) pairs from DATA.BIN header; accept only fully in-file mappings.
dir_rows=[]; candidates=[]
for off in range(0x4C,min(0x204C,len(data)-8),8):
    l,s=struct.unpack_from("<II",data,off)
    fo=(l-212)*2048
    if l>=212 and 0<s<8_000_000 and 0<=fo and fo+s<=len(data):
        rec={"directory_pair_offset":f"0x{off:X}","lba":l,"size_bytes":s,"data_bin_file_offset":f"0x{fo:X}",
             "records_if_30B":s//30 if s%30==0 else "NOT_DIVISIBLE",
             "records_if_12450B": "YES" if s==415*30 else "NO",
             "sha256":hashlib.sha256(data[fo:fo+s]).hexdigest(),
             "source":"DATA.BIN header candidate (LBA,size)","reason":"pair accepted only because mapped extent lies within DATA.BIN"}
        dir_rows.append(rec)
        if s==415*30:
            candidates.append((off,l,s,fo))
write_tsv("DV3_DATA_BIN_DIRECTORY_CANDIDATES.tsv",dir_rows,
    ["directory_pair_offset","lba","size_bytes","data_bin_file_offset","records_if_30B","records_if_12450B","sha256","source","reason"])

# Per-byte histograms for every confidently sized 415 x 30-byte resource candidate.
hist_rows=[]
for index,(doff,l,s,fo) in enumerate(candidates):
    blob=data[fo:fo+s]
    for field in range(30):
        counts=Counter(blob[r*30+field] for r in range(415))
        hist_rows.append({"resource_candidate":index,"directory_pair_offset":f"0x{doff:X}","lba":l,
          "resource_file_offset":f"0x{fo:X}","record_count":415,"record_size":30,"field_offset":f"0x{field:02X}",
          "histogram":";".join(f"0x{k:02X}:{counts[k]}" for k in sorted(counts)),
          "source":"DATA.BIN bytes at candidate extent, record stride 0x1E",
          "reason":"histogram byte-for-byte across exactly 415 records; resource identity requires loader cross-reference"})
write_tsv("DV3_415x30_RESOURCE_BYTE_HISTOGRAMS.tsv",hist_rows,
    ["resource_candidate","directory_pair_offset","lba","resource_file_offset","record_count","record_size","field_offset","histogram","source","reason"])

# Consolidated status for requested mappings and initial nibble; never guess when source/resource mapping is unresolved.
field_status=[]
field_status.append({"item":"source field copied to tile+0x00","result":"TIDAK TAHU: no verified load/store mapping unless DV3_TILE_FIELD_COPY_CANDIDATES.tsv identifies a matching source load and destination store",
  "source_pc":hxpc(loader_pc),"reason":"need matching load pointer to 0x1E record and store pointer to tile record"})
field_status.append({"item":"source field for tile+0x20 bits12-15","result":"TIDAK TAHU: require bitfield transformation and matching tile+0x20 store",
  "source_pc":hxpc(loader_pc),"reason":"field offset cannot be assigned from displacement coincidence alone"})
field_status.append({"item":"source field for tile+0x20 bits8-11","result":"TIDAK TAHU: require bitfield transformation and matching tile+0x20 store",
  "source_pc":hxpc(loader_pc),"reason":"field offset cannot be assigned from displacement coincidence alone"})
field_status.append({"item":"12 resources x 415 records","result":f"FOUND_CANDIDATES={len(candidates)}; expected 12 fully mapped entries of exactly 12450 B each",
  "source_pc":"DATA.BIN directory candidate scan","reason":"candidate extent must also be confirmed as the resources used by FUN_800F7ADC"})
field_status.append({"item":"initial nibble(s) tile+0x20 after loader","result":"TIDAK TAHU unless loader copy and resource field offsets are confirmed",
  "source_pc":hxpc(loader_pc),"reason":"no assumption from file image or zero-initialized RAM; value must be grounded in loader store"})
write_tsv("DV3_FIELD_MAPPING_STATUS.tsv",field_status,["item","result","source_pc","reason"])

# DV4 — requested hypotheses; H2' is algebraically identical to H3 for all d=1..5.
multipliers={1:1,2:4,3:8,4:16,5:32}
fee_rows=[]
for base in (100,50):
    for d in range(1,6):
        h1=base*(2**d); h2=multipliers[d]*base; h3=base if d==1 else base*(2**d)
        fee_rows.append({"fee_dasar":base,"distance_d":d,"H1_fee_dasar_x_2powd":h1,
          "H2prime_lookup_multiplier":multipliers[d],"H2prime_prediction":h2,
          "H3_piecewise_prediction":h3,"H2prime_equals_H3":"YES" if h2==h3 else "NO",
          "separates_H1_from_H2prime_H3":"YES" if h1!=h2 else "NO",
          "separates_H2prime_from_H3":"NO","test_note":"uji d=1 memisahkan H1 dari pasangan H2'/H3" if d==1 else "tidak membedakan ketiganya; semua prediksi sama",
          "source":"hypothesis definitions supplied by user","reason":"aritmetika langsung; bukan fitting dan bukan bukti ROM"})
write_tsv("DV4_FEE_PREDICTIONS.tsv",fee_rows,
    ["fee_dasar","distance_d","H1_fee_dasar_x_2powd","H2prime_lookup_multiplier","H2prime_prediction",
     "H3_piecewise_prediction","H2prime_equals_H3","separates_H1_from_H2prime_H3","separates_H2prime_from_H3","test_note","source","reason"])

# Compact report; keep all remaining uncertainty explicit.
notes=[
"# DV0–DV4 — audit statis raw-byte Naruto Jintori",
"",
f"BASELINE_INCLUSIVE={BASELINE}",
f"SNAPSHOT_SOURCE_SHA={SNAPSHOT}",
f"DV0_TOTAL_INCLUSIVE={len(ledger)} HUMAN={humans} BOT={bots}",
"HEAD_AT_ANALYSIS=SNAPSHOT_SOURCE_SHA; publication bot commit is created afterwards and is not included in the inclusive ledger.",
"",
"## DV1 — FUN_800EC574",
f"Raw block PC 0x{block0:08X}..0x{block1:08X}: {len(block)} decoded instruction slots; bytes and exact file offsets are in DV1_FUN_800EC574_BLOCK_RAW.tsv.",
"Accumulator loop: tile index is scaled by 0x124; tile+0 must equal t2=5; bits12-15 of tile+0x20 must equal dynamic t0; bits8-11 are added as 1+nibble to global 0x80139EFC for each accepted tile.",
"At 0x800ECBB8 the loaded global value is dynamic/TIDAK TAHU, negated, then stored as a halfword at manager-relative +0x2EE. No runtime numeric value is claimed.",
f"Direct +0x4F0 load references found: {len(reader_rows)}; all candidates and first local uses are in DV1_MANAGER_PLUS4F0_READERS.tsv.",
"",
"## DV2 — indirect dispatch",
f"CFG representative path rows={len(pathrows)}; branch edges in target slices={len(cfgrows)}. Runtime selector values remain TIDAK TAHU; required values are 44 and 2 to select the known handler slots.",
f"Direct writes to displacement +0x2E9 found={len(manager_writers)}; selector-source stores through a0 in caller region={len(sel2_store_rows)}. These are candidates, not proof of pointer identity.",
"",
"## DV3 — source resource record and tile fields",
f"FUN_800F7ADC loader code slots examined={len(loader_ins)}; direct source-load/destination-store candidates={len(copy_rows)}.",
f"DATA.BIN header candidates of exactly 415 x 0x1E bytes={len(candidates)}. Histograms are emitted only for those exact extents; resource identity requires cross-reference to loader code.",
"Tidak ada sumber field atau initial nibble +0x20 yang dianggap terkonfirmasi tanpa load/store dataflow yang cocok. Lihat DV3_FIELD_MAPPING_STATUS.tsv.",
"",
"## DV4 — fee hypotheses",
"H2' lookup {1:1,2:4,3:8,4:16,5:32} is algebraically identical to H3 (d=1: base; d>=2: base*2^d). Only d=1 distinguishes H1 from the H2'/H3 pair. No point distinguishes H2' from H3.",
"fee_dasar=100 and 50 are input hypotheses, not estimates. No fitting is performed.",
"",
"All PCs use Entry 1 mapping file_offset=0x10BB000+(PC-0x800AD450). Static only; no emulator/runtime/savestate; only text/TSV outputs."
]
(OUT/"DV0_DV4_STATIC_AUDIT.md").write_text("\n".join(notes)+"\n",encoding="utf-8")
