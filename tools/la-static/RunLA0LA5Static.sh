#!/usr/bin/env bash
set -euo pipefail
EXE="$1"
ENTRY="$2"
OUT="$3"
BASELINE="$4"
SOURCE_SHA="$5"
EXE_CODE="$6"
ENTRY_CODE="$7"
mkdir -p "$OUT"
python3 - "$EXE" "$ENTRY" "$OUT" "$BASELINE" "$SOURCE_SHA" "$EXE_CODE" "$ENTRY_CODE" <<'PY'
from __future__ import annotations
import csv, hashlib, json, os, re, struct, subprocess, sys, urllib.request
from collections import defaultdict
from pathlib import Path
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_BASE, ENTRY_BASE = 0x80010000, 0x800AD450
EXE_FILE, ENTRY_FILE = 0x800, 0x10BB000
EXE_SHA = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
ENTRY_SHA = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
EXE_SIZE, ENTRY_SIZE = 385024, 596412
REG = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
LOADS = {0x20:"lb",0x21:"lh",0x23:"lw",0x24:"lbu",0x25:"lhu"}
STORES = {0x28:"sb",0x29:"sh",0x2b:"sw"}
md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_LITTLE_ENDIAN)
md.detail = False
exe_path, entry_path, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
baseline, source = sys.argv[4], sys.argv[5]
out.mkdir(parents=True, exist_ok=True)

def hx(b): return " ".join(f"{x:02X}" for x in b)
def h32(v): return f"0x{v & 0xffffffff:08X}"
def sign16(v): return (v ^ 0x8000) - 0x8000
def reg(r): return "$"+REG[r]
def fileoff(pc, tag): return EXE_FILE + pc - EXE_BASE if tag=="EXE" else ENTRY_FILE + pc - ENTRY_BASE
def rec(pc, raw, tag):
    w=int.from_bytes(raw,"little"); op=w>>26; rs=(w>>21)&31; rt=(w>>16)&31
    rd=(w>>11)&31; sh=(w>>6)&31; fn=w&63
    ins=next(md.disasm(raw,pc,count=1),None)
    txt=(ins.mnemonic+" "+ins.op_str).strip() if ins else f".word {h32(w)}"
    return {"pc":pc,"tag":tag,"raw":raw,"word":w,"op":op,"rs":rs,"rt":rt,"rd":rd,
            "sh":sh,"fn":fn,"imm":sign16(w&0xffff),"uimm":w&0xffff,
            "text":txt,"mn":ins.mnemonic.lower() if ins else ".word",
            "fileoff":fileoff(pc,tag)}
def decode(blob, tag):
    base,start=(EXE_BASE,EXE_FILE) if tag=="EXE" else (ENTRY_BASE,0)
    data=blob[start:] if tag=="EXE" else blob
    return {base+p:rec(base+p,data[p:p+4],tag) for p in range(0,len(data)-3,4)}
def wr(path, rows, fields):
    with Path(path).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({k:("TIDAK TAHU" if row.get(k) is None or row.get(k)=="" else row.get(k)) for k in fields})
def txt(path, value): Path(path).write_text(value,encoding="utf-8")
def base_row(i):
    return {"image":i["tag"],"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),
            "bytes":hx(i["raw"]),"instruksi":i["text"]}
def direct_target(i):
    if i["op"] not in (2,3): return None
    return ((i["pc"]+4)&0xF0000000) | ((i["word"]&0x03ffffff)<<2)
def dest(i):
    op,fn=i["op"],i["fn"]
    if op==0:
        if fn in (8,12,13,24,25,26,27): return None
        if fn==9: return i["rd"] or 31
        return i["rd"] or None
    if op in (2,4,5,6,7,0x28,0x29,0x2a,0x2b,0x38,0x39,0x3a,0x3b): return None
    if op==3: return 31
    if op in (1,8,9,10,11,12,13,14,15,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37): return i["rt"] or None
    return None
def last_def(code, r, before, lo, limit=2048):
    floor=max(lo,before-limit*4)
    for pc in range(before-4,floor-1,-4):
        i=code.get(pc)
        if not i: continue
        # $a0-$a3/$t0-$t7/$t8-$t9 are caller-saved: stop at an earlier call.
        if r in set(range(4,16)) | {24,25} and (i["op"]==3 or (i["op"]==0 and i["fn"]==9)):
            return None
        if dest(i)==r: return i
    return None
def const_value(code,r,before,lo,depth=0,seen=None):
    if r==0:return 0,"ZERO"
    if depth>12:return None,"DEPTH_LIMIT"
    seen=set() if seen is None else seen
    key=(r,before)
    if key in seen:return None,"CYCLE"
    seen.add(key)
    d=last_def(code,r,before,lo)
    if not d:return None,"NO_STATIC_DEF"
    op,fn=d["op"],d["fn"]
    if op==15:return (d["uimm"]<<16)&0xffffffff,"LUI"
    if op in (8,9,13,12,14):
        a,why=const_value(code,d["rs"],d["pc"],lo,depth+1,seen)
        if a is None:return None,why
        if op in (8,9):return (a+d["imm"])&0xffffffff,"ADDIU"
        if op==13:return (a|d["uimm"])&0xffffffff,"ORI"
        if op==12:return (a&d["uimm"])&0xffffffff,"ANDI"
        return (a^d["uimm"])&0xffffffff,"XORI"
    if op==0 and fn in (0,2,3,0x21,0x23,0x24,0x25,0x26):
        a,wa=const_value(code,d["rs"],d["pc"],lo,depth+1,seen.copy())
        b,wb=const_value(code,d["rt"],d["pc"],lo,depth+1,seen.copy())
        if fn==0 and b is not None:return (b<<d["sh"])&0xffffffff,"SLL"
        if fn==2 and b is not None:return b>>d["sh"],"SRL"
        if fn==3 and b is not None:return b>>d["sh"],"SRA"
        if a is None or b is None:return None,"RUNTIME_OPERAND"
        if fn==0x21:return (a+b)&0xffffffff,"ADDU"
        if fn==0x23:return (a-b)&0xffffffff,"SUBU"
        if fn==0x24:return a&b,"AND"
        if fn==0x25:return a|b,"OR"
        if fn==0x26:return a^b,"XOR"
    return None,"DYNAMIC_OR_UNSUPPORTED"
def eff_addr(code,i,lo):
    b,why=const_value(code,i["rs"],i["pc"],lo)
    return (b+i["imm"])&0xffffffff if b is not None else None,why
def expr_reg(code,r,before,lo,depth=0,seen=None):
    if r==0:return "0"
    if depth>14:return "TIDAK TAHU:DEPTH"
    seen=set() if seen is None else seen
    key=(r,before)
    if key in seen:return "TIDAK TAHU:CYCLE"
    seen.add(key)
    d=last_def(code,r,before,lo)
    if not d:return "INCOMING_"+reg(r)
    op,fn=d["op"],d["fn"]
    if op==15:return h32(d["uimm"]<<16)
    if op in (8,9):return "("+expr_reg(code,d["rs"],d["pc"],lo,depth+1,seen.copy())+f"{d['imm']:+d})"
    if op==13:return "("+expr_reg(code,d["rs"],d["pc"],lo,depth+1,seen.copy())+f"|{h32(d['uimm'])})"
    if op in LOADS:
        ea,why=eff_addr(code,d,lo)
        size={0x20:"8s",0x21:"16s",0x23:"32",0x24:"8",0x25:"16"}[op]
        return f"MEM{size}[{h32(ea)}]" if ea is not None else f"MEM{size}[{reg(d['rs'])}{d['imm']:+d}]"
    if op==0 and fn==0:return "("+expr_reg(code,d["rt"],d["pc"],lo,depth+1,seen.copy())+f"<<{d['sh']})"
    if op==0 and fn in (0x21,0x23):
        sym="+" if fn==0x21 else "-"
        return "("+expr_reg(code,d["rs"],d["pc"],lo,depth+1,seen.copy())+sym+expr_reg(code,d["rt"],d["pc"],lo,depth+1,seen.copy())+")"
    if op==0 and fn==0x25:
        if d["rs"]==0:return expr_reg(code,d["rt"],d["pc"],lo,depth+1,seen.copy())
        if d["rt"]==0:return expr_reg(code,d["rs"],d["pc"],lo,depth+1,seen.copy())
    return f"DEF@{h32(d['pc'])}:{d['text']}"
def trace_defs(code,r,before,lo,site,depth=0,seen=None,rows=None):
    if rows is None:rows=[]
    if depth>=8 or r==0:return rows
    seen=set() if seen is None else seen
    if (r,before) in seen:return rows
    seen.add((r,before))
    d=last_def(code,r,before,lo)
    if not d:return rows
    q=base_row(d);q.update({"call_pc":h32(site),"argument":reg(r),"depth":depth,"origin_expression":expr_reg(code,r,before,lo)})
    rows.append(q)
    op,fn=d["op"],d["fn"]
    if op in (8,9,12,13,14):trace_defs(code,d["rs"],d["pc"],lo,site,depth+1,seen.copy(),rows)
    elif op in LOADS:trace_defs(code,d["rs"],d["pc"],lo,site,depth+1,seen.copy(),rows)
    elif op==0 and fn==0:trace_defs(code,d["rt"],d["pc"],lo,site,depth+1,seen.copy(),rows)
    elif op==0 and fn in (0x21,0x23,0x24,0x25,0x26,0x2a,0x2b):
        trace_defs(code,d["rs"],d["pc"],lo,site,depth+1,seen.copy(),rows)
        trace_defs(code,d["rt"],d["pc"],lo,site,depth+1,seen.copy(),rows)
    return rows
def find_prolog(code,pc,lo,span=0x5000):
    floor=max(lo,pc-span)
    for q in range(pc-4,floor-1,-4):
        i=code.get(q)
        if not i:continue
        if i["op"]==9 and i["rs"]==29 and i["rt"]==29 and i["imm"]<0:
            for k in range(1,13):
                s=code.get(q+4*k)
                if not s:break
                if s["op"] in STORES and s["rs"]==29 and s["rt"]==31:
                    return q,"stack adjustment followed by ra store"
    return None,"NO_CLEAR_PROLOG_IN_SCAN_WINDOW"
def rows_window(code,pc,group,offset=0,count=16):
    rows=[]
    for k in range(offset,offset+count):
        i=code.get(pc+k*4)
        if i:
            z=base_row(i);z["excerpt_id"]=group;rows.append(z)
    return rows
def pointer_words(blob,tag,target):
    base,start=(EXE_BASE,EXE_FILE) if tag=="EXE" else (ENTRY_BASE,0)
    data=blob[start:]; needle=struct.pack("<I",target); outrows=[]; p=0
    while True:
        p=data.find(needle,p)
        if p<0:break
        if p % 4: p+=1; continue
        pc=base+p
        outrows.append({"image":tag,"pc":h32(pc),"file_offset":h32(fileoff(pc,tag)),
                        "bytes":hx(data[p:p+4]),"instruksi":"DATA_POINTER_WORD",
                        "value":h32(target),"classification":"POINTER_WORD_CANDIDATE"})
        p+=1
    return outrows
def parse_code_pcs(path):
    pcs=set()
    for line in Path(path).read_text(encoding="utf-8",errors="replace").splitlines():
        if line.startswith("CODE_INSTRUCTION="):
            try: pcs.add(int(line.split("=",1)[1].split("|",1)[0],16))
            except Exception: pass
    return pcs
def parse_target_refs(path,target):
    out=[]; active=False
    for line in Path(path).read_text(encoding="utf-8",errors="replace").splitlines():
        if line.startswith("TARGET="):
            try: active=int(line.split("=",1)[1],16)==target
            except Exception: active=False
        elif active and line.startswith("REF="):
            p=line.split("=",1)[1].split("|")
            if len(p)>=4:
                try: out.append({"pc":int(p[0],16),"kind":p[1],"caller_entry":p[2],"caller_name":p[3]})
                except Exception: pass
    return out
def all_pointer_callers(codes,target,valid_pcs):
    rows=[]
    for tag,code in codes:
        lo=EXE_BASE if tag=="EXE" else ENTRY_BASE
        for pc,i in code.items():
            if pc not in valid_pcs.get(tag,set()): continue
            t=direct_target(i)
            if t==target:
                z=base_row(i);z.update({"target":h32(target),"kind":"JAL" if i["op"]==3 else "J","classification":"DIRECT_CODE_REFERENCE"})
                rows.append(z)
            if i["op"]==0 and i["fn"] in (8,9):
                val,why=const_value(code,i["rs"],pc,lo)
                if val==target:
                    z=base_row(i);z.update({"target":h32(target),"kind":"JALR" if i["fn"]==9 else "JR","classification":"STATIC_REGISTER_TARGET","target_register":reg(i["rs"])})
                    rows.append(z)
    return rows

exe=exe_path.read_bytes(); entry=entry_path.read_bytes()
if len(exe)!=EXE_SIZE or hashlib.sha256(exe).hexdigest()!=EXE_SHA: raise SystemExit("EXE_VERIFY_FAIL")
if len(entry)!=ENTRY_SIZE or hashlib.sha256(entry).hexdigest()!=ENTRY_SHA: raise SystemExit("ENTRY1_VERIFY_FAIL")
ce_all,ci_all=decode(exe,"EXE"),decode(entry,"ENTRY1")
exe_code_pcs=parse_code_pcs(sys.argv[6]); entry_code_pcs=parse_code_pcs(sys.argv[7])
if not exe_code_pcs or not entry_code_pcs: raise SystemExit("GHIDRA_CODE_EXPORT_EMPTY")
ce={pc:i for pc,i in ce_all.items() if pc in exe_code_pcs}
ci={pc:i for pc,i in ci_all.items() if pc in entry_code_pcs}
codes=[("EXE",ce),("ENTRY1",ci)]
valid_pcs={"EXE":exe_code_pcs,"ENTRY1":entry_code_pcs}
EXE_REFS=parse_target_refs(sys.argv[6],0x800B50AC)
ENTRY_B50_REFS=parse_target_refs(sys.argv[7],0x800B50AC)
ENTRY_BE_REFS=parse_target_refs(sys.argv[7],0x800BE5D8)
# LA0 — source and checked-out HEAD snapshots; all events/pages for Actions.
subprocess.run(["git","merge-base","--is-ancestor",baseline,source],check=True)
def commit_rows(sha):
    raw=subprocess.check_output(["git","log","--format=%H%x09%an%x09%ae%x09%s",f"{baseline}^..{sha}"]).decode().splitlines()
    rows=[]
    for line in raw:
        p=line.split("\t",3)
        if len(p)<4:continue
        c,n,e,m=p
        bot=("[bot]" in n.lower() or "dependabot" in n.lower() or "bot" in n.lower())
        rows.append({"sha":c,"author":n,"email":e,"class":"BOT" if bot else "HUMAN","subject":m})
    return rows
src_commits=commit_rows(source)
head_sha=subprocess.check_output(["git","rev-parse","HEAD"]).decode().strip()
head_commits=commit_rows(head_sha)
wr(out/"LA0_LEDGER_COMMITS_SOURCE.tsv",src_commits,["sha","author","email","class","subject"])
wr(out/"LA0_LEDGER_COMMITS_HEAD.tsv",head_commits,["sha","author","email","class","subject"])
counts=[]
for label,sha,rs in [("SOURCE",source,src_commits),("HEAD_AT_ANALYSIS",head_sha,head_commits)]:
    counts.append({"snapshot":label,"sha":sha,"commits_total":len(rs),
                   "human":sum(x["class"]=="HUMAN" for x in rs),"bot":sum(x["class"]=="BOT" for x in rs)})
wr(out/"LA0_LEDGER_COMMIT_COUNTS.tsv",counts,["snapshot","sha","commits_total","human","bot"])
token=os.environ.get("GH_TOKEN","")
api="https://api.github.com/repos/"+os.environ["GITHUB_REPOSITORY"]+"/actions/runs?per_page=100&page="
allruns=[]; page=1; total=0
while True:
    req=urllib.request.Request(api+str(page),headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"})
    with urllib.request.urlopen(req,timeout=60) as response: j=json.loads(response.read().decode())
    total=int(j.get("total_count",0)); rs=j.get("workflow_runs",[]); allruns.extend(rs)
    if not rs or len(allruns)>=total:break
    page+=1
    if page>100:raise RuntimeError("ACTIONS_PAGINATION_LIMIT")
ar=[{"run_id":x.get("id"),"name":x.get("name"),"event":x.get("event"),"status":x.get("status"),
     "conclusion":x.get("conclusion") or "TIDAK TAHU","head_sha":x.get("head_sha"),
     "created_at":x.get("created_at")} for x in allruns]
wr(out/"LA0_LEDGER_ACTIONS.tsv",ar,["run_id","name","event","status","conclusion","head_sha","created_at"])
pyfile=out/"LA0_PYCOMPILE.tsv"
if not pyfile.exists():
    pyrows=[]
    tracked=subprocess.check_output(["git","ls-files","-z","*.py"]).decode().split("\0")
    for name in [x for x in tracked if x]:
        try:subprocess.run([sys.executable,"-m","py_compile",name],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);st="PASS";msg=""
        except Exception as e:st="FAIL";msg=str(e)
        pyrows.append({"path":name,"status":st,"reason":msg})
    wr(pyfile,pyrows,["path","status","reason"])
pyrows=list(csv.DictReader(pyfile.open(encoding="utf-8"),delimiter="\t"))
manifest=subprocess.check_output(["git","show","--format=","--name-status",source]).decode().strip()
txt(out/"LA0_SOURCE_COMMIT_FILES.tsv","status\tpath\n"+manifest+"\n")
txt(out/"LA0_LEDGER_SUMMARY.txt",
    f"BASELINE_INCLUSIVE={baseline}\nSOURCE_SHA={source}\nHEAD_AT_ANALYSIS={head_sha}\n"+
    f"SOURCE_COMMITS_TOTAL={len(src_commits)}\nSOURCE_COMMITS_HUMAN={sum(x['class']=='HUMAN' for x in src_commits)}\nSOURCE_COMMITS_BOT={sum(x['class']=='BOT' for x in src_commits)}\n"+
    f"HEAD_COMMITS_TOTAL={len(head_commits)}\nHEAD_COMMITS_HUMAN={sum(x['class']=='HUMAN' for x in head_commits)}\nHEAD_COMMITS_BOT={sum(x['class']=='BOT' for x in head_commits)}\n"+
    f"ACTIONS_RUNS_ALL_EVENTS={len(ar)}\nACTIONS_API_TOTAL_COUNT={total}\nACTIONS_PAGES_READ={page}\nACTIONS_SCHEDULED={sum(x['event']=='schedule' for x in ar)}\n"+
    f"PY_COMPILE_TOTAL={len(pyrows)}\nPY_COMPILE_PASS={sum(x.get('status')=='PASS' for x in pyrows)}\nPY_COMPILE_FAIL={sum(x.get('status')!='PASS' for x in pyrows)}\n"+
    "BOT_CLASSIFICATION=author name contains [bot], bot, or dependabot; review identity before treating classification as canonical\n"+
    "HEAD_SCOPE=checked-out HEAD before final report publication commit; self-inclusion of that later commit is not possible in its own ledger\n")
txt(out/"LA0_ACTIONS_PAGINATION.txt",f"TOTAL_COUNT={total}\nRUNS_FETCHED={len(ar)}\nPAGES_READ={page}\nALL_EVENTS=yes\n")
# LA1(a) — pointer candidates and references around the two 0x800B50AC words.
target=0x800B50AC
ptrs=[]
for tag,blob in [("EXE",exe),("ENTRY1",entry)]:ptrs.extend(pointer_words(blob,tag,target))
wr(out/"LA1_B50AC_POINTER_WORDS.tsv",ptrs,["image","pc","file_offset","bytes","instruksi","value","classification"])
# Four bounded neighboring record candidates only. No long contiguous raw-byte export.
candidate_record_bases=[0x800558E4,0x80055900,0x8005591C,0x80055938]
region_rows=[]
for record_base in candidate_record_bases:
    for field_offset in (0,4,8):
        pc=record_base+field_offset
        off=pc-EXE_BASE+EXE_FILE
        raw=exe[off:off+4]
        if len(raw)!=4:continue
        val=int.from_bytes(raw,"little")
        region_rows.append({"image":"EXE","pc":h32(pc),"file_offset":h32(off),"bytes":hx(raw),
                            "instruksi":"DATA_WORD","value":h32(val),
                            "classification":"TARGET_POINTER" if val==target else "NEIGHBOR_WORD"})
wr(out/"LA1_B50AC_TABLE_REGION.tsv",region_rows,
   ["image","pc","file_offset","bytes","instruksi","value","classification"])
ref_users=[]
for tag,code in codes:
    lo=EXE_BASE if tag=="EXE" else ENTRY_BASE
    for pc,i in code.items():
        if pc not in valid_pcs.get(tag,set()): continue
        if i["op"] in LOADS:
            expr=expr_reg(code,i["rs"],pc,lo)
            ea,why=eff_addr(code,i,lo)
            if (ea is not None and 0x800558C0<=ea<0x80055980) or ("0x80055904" in expr or "0x80055920" in expr):
                z=base_row(i);z.update({"base_expression":expr,"effective_address":h32(ea) if ea is not None else "DYNAMIC_INDEX",
                                        "register_destination":reg(i["rt"]),"next_jump_register":"TIDAK TAHU"})
                for q in range(pc+4,pc+0x41,4):
                    j=code.get(q)
                    if j and j["op"]==0 and j["fn"] in (8,9):
                        jexpr=expr_reg(code,j["rs"],q,lo)
                        z["next_jump_register"]=h32(q)+" "+j["text"]+" target_expr="+jexpr
                        break
                ref_users.append(z)
        if i["op"]==15 and i["uimm"]==0x8005:
            for q in range(pc+4,pc+0x31,4):
                n=code.get(q)
                if n and n["rs"]==i["rt"] and n["op"] in (8,9,13):
                    val=((i["uimm"]<<16)+(n["imm"] if n["op"] in (8,9) else n["uimm"]))&0xffffffff
                    if 0x800558C0<=val<0x80055980:
                        z=base_row(i);z.update({"base_expression":"LUI+ADDIU/ORI","effective_address":h32(val),
                            "register_destination":reg(n["rt"]),"next_jump_register":"basis_candidate"})
                        ref_users.append(z)
wr(out/"LA1_B50AC_TABLE_USERS.tsv",ref_users,["image","pc","file_offset","bytes","instruksi","base_expression","effective_address","register_destination","next_jump_register"])
direct_b50=[]
for tag,code in codes:
    lo=EXE_BASE if tag=="EXE" else ENTRY_BASE
    for pc,i in code.items():
        t=direct_target(i)
        if t==target:
            z=base_row(i);z.update({"kind":"JAL" if i["op"]==3 else "J","target":h32(target),"classification":"DIRECT_CALL_OR_TAIL_JUMP"})
            direct_b50.append(z)
        if i["op"]==0 and i["fn"] in (8,9):
            v,why=const_value(code,i["rs"],pc,lo)
            if v==target:
                z=base_row(i);z.update({"kind":"JALR" if i["fn"]==9 else "JR","target":h32(target),"classification":"CONSTANT_REGISTER_TARGET"})
                direct_b50.append(z)
for tag, refs in [("EXE",EXE_REFS),("ENTRY1",ENTRY_B50_REFS)]:
    for x in refs:
        pc=x["pc"]; i=(ce if tag=="EXE" else ci).get(pc)
        z=base_row(i) if i else {"image":tag,"pc":h32(pc),"file_offset":h32(fileoff(pc,tag)),"bytes":"TIDAK TAHU","instruksi":"GHIDRA_REFERENCE"}
        z.update({"kind":"GHIDRA_"+x["kind"],"target":h32(target),"classification":"GHIDRA_XREF caller="+x["caller_name"]+" entry="+x["caller_entry"]})
        direct_b50.append(z)
wr(out/"LA1_B50AC_DIRECT_CALLS.tsv",direct_b50,["image","pc","file_offset","bytes","instruksi","kind","target","classification"])

# UA1: exact target forms, with each hit classified independently.
jal_word=((3<<26)|((target>>2)&0x03ffffff))&0xffffffff
if jal_word!=0x0C02D42B: raise SystemExit("UA1_JAL_ENCODING_MISMATCH")
ua1_rows=[]
for p in ptrs:
    ua1_rows.append({"image":p["image"],"class":"U32_LE_POINTER_WORD",
        "pc":p["pc"],"file_offset":p["file_offset"],"bytes":p["bytes"],
        "instruksi":"DATA_POINTER_WORD value="+h32(target),
        "paired_pc":"NONE","paired_file_offset":"NONE",
        "paired_bytes":"NONE","paired_instruksi":"NONE"})
for tag,code in codes:
    lo=EXE_BASE if tag=="EXE" else ENTRY_BASE
    for pc,i in sorted(code.items()):
        direct=direct_target(i)
        if direct==target:
            klass="DIRECT_JAL" if i["op"]==3 else "DIRECT_J"
            ua1_rows.append({"image":tag,"class":klass,"pc":h32(pc),
                "file_offset":h32(i["fileoff"]),"bytes":hx(i["raw"]),
                "instruksi":i["text"],"paired_pc":"NONE",
                "paired_file_offset":"NONE","paired_bytes":"NONE",
                "paired_instruksi":"NONE"})
        if i["op"]==0 and i["fn"] in (8,9):
            value,why=const_value(code,i["rs"],pc,lo)
            if value==target:
                klass="CONSTANT_JALR" if i["fn"]==9 else "CONSTANT_JR"
                ua1_rows.append({"image":tag,"class":klass,"pc":h32(pc),
                    "file_offset":h32(i["fileoff"]),"bytes":hx(i["raw"]),
                    "instruksi":i["text"]+" target_register="+reg(i["rs"]),
                    "paired_pc":"NONE","paired_file_offset":"NONE",
                    "paired_bytes":"NONE","paired_instruksi":"NONE"})
        if i["op"]==15 and i["uimm"]==0x800B:
            source_reg=i["rt"]
            for distance in range(1,9):
                q=code.get(pc+4*distance)
                if q is None: break
                if q["op"] in (1,2,3,4,5,6,7) or (q["op"]==0 and q["fn"] in (8,9)):
                    break
                if q["op"] in (9,13) and q["rs"]==source_reg:
                    low=(q["imm"] if q["op"]==9 else q["uimm"])
                    value=((i["uimm"]<<16)+low)&0xffffffff
                    if value==target:
                        ua1_rows.append({"image":tag,
                            "class":"LUI_800B_ADDIU_ORI_50AC_PAIR",
                            "pc":h32(pc),"file_offset":h32(i["fileoff"]),
                            "bytes":hx(i["raw"]),"instruksi":i["text"],
                            "paired_pc":h32(q["pc"]),
                            "paired_file_offset":h32(q["fileoff"]),
                            "paired_bytes":hx(q["raw"]),
                            "paired_instruksi":q["text"]})
                    break
                if dest(q)==source_reg:
                    break
for tag,refs in [("EXE",EXE_REFS),("ENTRY1",ENTRY_B50_REFS)]:
    for x in refs:
        pc=x["pc"]; code=ce if tag=="EXE" else ci; ins=code.get(pc)
        ua1_rows.append({"image":tag,"class":"GHIDRA_XREF",
            "pc":h32(pc),"file_offset":h32(fileoff(pc,tag)),
            "bytes":hx(ins["raw"]) if ins else "TIDAK TAHU",
            "instruksi":ins["text"] if ins else "TIDAK TAHU",
            "paired_pc":"NONE","paired_file_offset":"NONE",
            "paired_bytes":"NONE",
            "paired_instruksi":"caller="+x["caller_name"]+" entry="+x["caller_entry"]})
ua1_rows.sort(key=lambda x:(x["image"],int(x["pc"],16),x["class"]))
wr(out/"UA1_TARGET_REFERENCES.tsv",ua1_rows,
   ["image","class","pc","file_offset","bytes","instruksi",
    "paired_pc","paired_file_offset","paired_bytes","paired_instruksi"])

# Nine caller-context instructions total: 36 contiguous bytes.
caller_pc=0x80011A28
caller_rows=[]
for q in range(caller_pc-0x20,caller_pc+4,4):
    ins=ce_all.get(q)
    if ins:
        caller_rows.append({"image":"EXE","pc":h32(q),
            "file_offset":h32(ins["fileoff"]),"bytes":hx(ins["raw"]),
            "instruksi":ins["text"],
            "role":"JALR_V0" if q==caller_pc else "PRECALL_CONTEXT"})
wr(out/"UA1_CALLER_11A28_CONTEXT.tsv",caller_rows,
   ["image","pc","file_offset","bytes","instruksi","role"])
v0_def=last_def(ce_all,2,caller_pc,EXE_BASE)
v0_expr=expr_reg(ce_all,2,caller_pc,EXE_BASE)
v0_ea, v0_ea_reason=(eff_addr(ce_all,v0_def,EXE_BASE)
    if v0_def and v0_def["op"] in LOADS else (None,"NOT_A_LOAD"))
if v0_ea in (0x80055904,0x80055920):
    table_v0_status="YES_STATIC_LOAD_FROM_TARGET_POINTER_SLOT"
elif v0_def is None:
    table_v0_status="TIDAK TAHU_NO_STATIC_V0_DEFINITION"
else:
    table_v0_status="NO_DIRECT_STATIC_LOAD_MATCH; DYNAMIC_OR_INDIRECT_PATH_NOT_EXCLUDED"

# First return after 0x800B54DC and the next recognizable function prolog.
boundary_start=0x800B54E0
boundary_end=0x800B5800
first_jr=None
for q in range(boundary_start,boundary_end,4):
    ins=ci.get(q)
    if ins and ins["op"]==0 and ins["fn"]==8 and ins["rs"]==31:
        first_jr=ins
        break
next_prolog=None
next_prolog_store=None
if first_jr is not None:
    for q in range(first_jr["pc"]+8,boundary_end,4):
        ins=ci.get(q)
        if not (ins and ins["op"]==9 and ins["rs"]==29 and
                ins["rt"]==29 and ins["imm"]<0):
            continue
        for k in range(1,13):
            st=ci.get(q+4*k)
            if st is None: break
            if st["op"] in STORES and st["rs"]==29 and st["rt"]==31:
                next_prolog=ins
                next_prolog_store=st
                break
        if next_prolog is not None: break
boundary_rows=[{
    "range_start":"0x800B54E0","range_end_exclusive":"0x800B5800",
    "first_jr_ra_pc":h32(first_jr["pc"]) if first_jr else "TIDAK TAHU",
    "first_jr_ra_instruction":first_jr["text"] if first_jr else "TIDAK TAHU",
    "next_prolog_pc":h32(next_prolog["pc"]) if next_prolog else "TIDAK TAHU",
    "next_prolog_instruction":next_prolog["text"] if next_prolog else "TIDAK TAHU",
    "next_prolog_sw_ra_pc":h32(next_prolog_store["pc"]) if next_prolog_store else "TIDAK TAHU",
    "status":"RETURN_AND_NEXT_PROLOG_FOUND" if first_jr and next_prolog else
             ("RETURN_FOUND_NEXT_PROLOG_TIDAK_TAHU" if first_jr else "FIRST_JR_RA_TIDAK_TAHU")
}]
wr(out/"UA1_B50AC_FUNCTION_END.tsv",boundary_rows,
   ["range_start","range_end_exclusive","first_jr_ra_pc",
    "first_jr_ra_instruction","next_prolog_pc","next_prolog_instruction",
    "next_prolog_sw_ra_pc","status"])

pointer_pcs=sorted(int(x["pc"],16) for x in ptrs if x["image"]=="EXE")
deltas=[pointer_pcs[i+1]-pointer_pcs[i] for i in range(len(pointer_pcs)-1)]
stride_note="TIDAK TAHU: fewer than two pointer-word addresses in EXE"
if len(pointer_pcs)>=2:
    stride_note="candidate spacing(s)="+",".join(h32(x) for x in sorted(set(deltas)))+"; repeated entries alone do not prove table base/stride without an indexed load+jump user"
txt(out/"LA1_B50AC_TABLE_ASSESSMENT.txt",
    "POINTER_WORDS_AT="+",".join(h32(x) for x in pointer_pcs)+"\n"+
    "OBSERVED_SPACING="+",".join(h32(x) for x in deltas)+"\n"+
    "TABLE_BASE_AND_STRIDE="+stride_note+"\n"+
    "TABLE_USER_EVIDENCE=see LA1_B50AC_TABLE_USERS.tsv; require base + scaled index + lw + jalr/jr chain before naming a dispatch table\n"+
    "CALLERS=see LA1_B50AC_DIRECT_CALLS.tsv and pointer-word candidates; absence of a resolved indirect dispatch is not a zero-caller proof\n")
# LA1(b): caller-boundary scan and reaching definitions of a2/a3.
calls=[0x800F5F54,0x800B54DC,0x800F5EBC]
call_targets={0x800F5F54:0x800F2A9C,0x800B54DC:0x800F3658,0x800F5EBC:0x800DC2E0}
argrows=[]; argdefs=[]
for cp in calls:
    i=ci.get(cp); pro,reason=find_prolog(ci,cp,ENTRY_BASE)
    lo=pro if pro is not None else ENTRY_BASE
    t=direct_target(i) if i else None
    argrows.append({"image":"ENTRY1","pc":h32(cp),"file_offset":h32(fileoff(cp,"ENTRY1")),
        "bytes":hx(i["raw"]) if i else "TIDAK TAHU","instruksi":i["text"] if i else "TIDAK TAHU",
        "expected_target":h32(call_targets[cp]),"actual_target":h32(t) if t else "TIDAK TAHU",
        "manual_prolog":h32(pro) if pro else "TIDAK TAHU","prolog_reason":reason})
    for r in (6,7):
        chain=trace_defs(ci,r,cp,lo,cp)
        if not chain:
            argdefs.append({"image":"ENTRY1","pc":h32(cp),"file_offset":h32(fileoff(cp,"ENTRY1")),
                "bytes":"TIDAK TAHU","instruksi":"TIDAK TAHU","argument":reg(r),"depth":0,
                "origin_expression":"INCOMING/NO_STATIC_REACHING_DEF","note":"TIDAK TAHU"})
        for q in chain:
            q["note"]="linear backward def-use slice; not path-sensitive"
            argdefs.append(q)
wr(out/"LA1_CALL_SITES_PROLOGS.tsv",argrows,["image","pc","file_offset","bytes","instruksi","expected_target","actual_target","manual_prolog","prolog_reason"])
wr(out/"LA1_A2_A3_REACHING_DEFS.tsv",argdefs,["image","pc","file_offset","bytes","instruksi","call_pc","argument","depth","origin_expression","note"])
# wallet authority: replay the exact 14F10 body and competing falsifiable hypotheses.
body=[]
for k in range(16):
    i=ce.get(0x80014F28+k*4)
    if i:body.append(base_row(i)|{"excerpt_id":"FUN_80014F10_CORE_64B"})
wr(out/"LA1_FUN_80014F10_CORE_EXCERPT.tsv",body,["image","pc","file_offset","bytes","instruksi","excerpt_id"])
wallet=[
 {"hypothesis":"H1: participant record +0x04 is wallet-like balance field","support_1":"JA1_RECORD_PLUS4.tsv / JA1_PLUS4_CONFIRMED_WRITES.tsv: +0x04 has multiple record-stride write candidates","support_2":"player record candidates use 0xB4 stride; setter/reader closure has not tied +0x04 to visible wallet","falsifier":"A complete caller+reader trace shows +0x04 is only cache, flag, or unrelated state"},
 {"hypothesis":"H2: manager+0x4F4 is authoritative wallet or settlement accumulator","support_1":"ENTRY1 0x800DD1B8 loads 0x4F4 into $a1 and 0x800DD1C8 conditionally negates it","support_2":"nearby caller sequence invokes 0x80014F10 with this value and clears 0x4F4 on its completion path","falsifier":"A complete producer/consumer trace shows +0x4F4 is transient settlement data and never persistent wallet"},
 {"hypothesis":"H3: FUN_80014F10 is the authoritative wallet setter","support_1":"function writes participant-stride record at +0x94 when new argument exceeds old value","support_2":"body core reads, compares, and conditionally stores the argument","falsifier":"body computes 0x80070F34 + owner*0xB4 then accesses +0x94, not candidate +0x04"}
]
wr(out/"LA1_WALLET_HYPOTHESES.tsv",wallet,["hypothesis","support_1","support_2","falsifier"])
txt(out/"LA1_WALLET_STATUS.txt","WALLET_AUTHORITATIVE_SETTER=TIDAK TAHU\n"+
    "FUN_80014F10 core: participant-indexed max-update at +0x94; this is not proof of the authoritative wallet setter.\n"+
    "The +0x04 and +0x4F4 candidates remain competing K1 hypotheses; see LA1_WALLET_HYPOTHESES.tsv.\n")
# LA2(a): resolve D49D0 and identify whether the effective address is a static table.
site=0x800D49D0
formula=expr_reg(ci,3,site,ENTRY_BASE)
a2expr=expr_reg(ci,6,0x800D49D8,ENTRY_BASE)
drows=rows_window(ci,0x800D49A4,"D49D0_ADDRESS_DATAFLOW_64B_A",0,16)
wr(out/"LA2_D49D0_ADDRESS_DATAFLOW.tsv",drows,["image","pc","file_offset","bytes","instruksi","excerpt_id"])
xrows=[]
for g in (0x8013EA6E,0x8013EB1C,0x8013EA74,0x8013EA88,0x80139EFC):
    for pc,i in ci.items():
        if pc not in valid_pcs["ENTRY1"]: continue
        if i["op"] in LOADS or i["op"] in STORES:
            ea,why=eff_addr(ci,i,ENTRY_BASE)
            width={0x20:1,0x21:2,0x23:4,0x24:1,0x25:2,0x28:1,0x29:2,0x2b:4}.get(i["op"],1)
            if ea is not None and ea<=g<ea+width:
                z=base_row(i);z.update({"target_global":h32(g),"effective_address":h32(ea),
                     "access":LOADS.get(i["op"],STORES.get(i["op"])),"base_origin":why})
                xrows.append(z)
wr(out/"LA2_GLOBAL_INPUT_ACCESSES.tsv",xrows,["image","pc","file_offset","bytes","instruksi","target_global","effective_address","access","base_origin"])
txt(out/"LA2_D49D0_EFFECTIVE_ADDRESS.txt",
    "LOAD_PC=0x800D49D0\nLOAD_INSTRUCTION="+ci[site]["text"]+"\n"+
    "V1_EXPRESSION="+formula+"\n"+
    "A2_MANAGER_BASE_EXPRESSION="+a2expr+"\n"+
    "EXPECTED_REDUCTION_FROM_LOCAL_CHAIN=MEM32[0x8013EA74] + 0x10 + MEM8[0x8013EB1C] + (MEM16[0x8013EA6E] * 144)\n"+
    "INTERPRETATION=address depends on a runtime-loaded manager pointer and two mutable global fields; it is not a fixed file address on this proof\n"+
    "STATIC_TABLE=NO_STATIC_TABLE_BASE_PROVEN\n"+
    "BYTE_SET_OF_LBU_RESULT=TIDAK TAHU (data bytes are selected through runtime state; no static byte set can be claimed)\n"+
    "LIMIT=nearest-definition slice only; not path-sensitive; global aliases/writers remain separate\n")
# LA2(b): all statically resolved sb/sh/sw writes overlapping 0x80139EC4..EC7.
glo,ghi=0x80139EC4,0x80139EC7
gw=[]; unresolved=[]
for tag,code in codes:
    lo=EXE_BASE if tag=="EXE" else ENTRY_BASE
    for pc,i in code.items():
        if pc not in valid_pcs.get(tag,set()): continue
        if i["op"] not in STORES:continue
        width={0x28:1,0x29:2,0x2b:4}[i["op"]]
        ea,why=eff_addr(code,i,lo)
        if ea is None:
            if -0x7000<=i["imm"]<=0x7000:
                unresolved.append({"image":tag,"pc":h32(pc),"file_offset":h32(i["fileoff"]),
                    "bytes":hx(i["raw"]),"instruksi":i["text"],"offset":i["imm"],
                    "base_register":reg(i["rs"]),"reason":"base not statically constant; dynamic alias not ruled out"})
            continue
        if ea<=ghi and ea+width-1>=glo:
            val,vwhy=const_value(code,i["rt"],pc,lo)
            expr=expr_reg(code,i["rt"],pc,lo)
            z=base_row(i);z.update({"effective_address":h32(ea),"width_bytes":width,
                "overlap":h32(max(ea,glo))+".."+h32(min(ea+width-1,ghi)),
                "value_constant":h32(val) if val is not None else "TIDAK TAHU",
                "value_expression":expr,"base_construction":why,"value_class":vwhy})
            gw.append(z)
wr(out/"LA2_80139EC4_EC7_WRITERS.tsv",gw,["image","pc","file_offset","bytes","instruksi","effective_address","width_bytes","overlap","value_constant","value_expression","base_construction","value_class"])
wr(out/"LA2_DYNAMIC_STORE_BASE_CENSUS.tsv",unresolved,["image","pc","file_offset","bytes","instruksi","offset","base_register","reason"])
# LA2(c): every store at displacement +0x530, irrespective of base register.
xstores=[]
for tag,code in codes:
    lo=EXE_BASE if tag=="EXE" else ENTRY_BASE
    for pc,i in code.items():
        if pc in valid_pcs.get(tag,set()) and i["op"] in STORES and i["imm"]==0x530:
            val,why=const_value(code,i["rt"],pc,lo)
            z=base_row(i);z.update({"base_register":reg(i["rs"]),"value_register":reg(i["rt"]),
                "value_constant":h32(val) if val is not None else "TIDAK TAHU",
                "value_expression":expr_reg(code,i["rt"],pc,lo),"value_origin_class":why,
                "base_expression":expr_reg(code,i["rs"],pc,lo)})
            xstores.append(z)
wr(out/"LA2_ALL_MANAGER_PLUS530_STORES.tsv",xstores,["image","pc","file_offset","bytes","instruksi","base_register","value_register","value_constant","value_expression","value_origin_class","base_expression"])
# LA2(d): bounded instruction excerpts at F2A9C and EXE helper 8001552C.
bounds=[]
for tag,code,pc in [("ENTRY1",ci,0x800F2A9C),("EXE",ce,0x8001552C)]:
    for q in range(0,32,16):
        for z in rows_window(code,pc,tag+"_"+h32(pc)+"_CHUNK_"+str(q//16+1),q,16):
            z["target_pc"]=h32(pc);bounds.append(z)
wr(out/"LA2_BOUNDS_CONTEXT.tsv",bounds,["image","pc","file_offset","bytes","instruksi","excerpt_id","target_pc"])
guard=[]
for tag,code,pc in [("ENTRY1",ci,0x800F2A9C),("EXE",ce,0x8001552C)]:
    lo=ENTRY_BASE if tag=="ENTRY1" else EXE_BASE
    for q in range(pc,pc+0x180,4):
        i=code.get(q)
        if not i:continue
        if i["op"] in (4,5,6,7,1) or (i["op"]==0 and i["fn"] in (0x2a,0x2b)):
            z=base_row(i);z.update({"function_pc":h32(pc),"branch_or_compare":"yes",
                "left_expr":expr_reg(code,i["rs"],q,lo),"right_expr":expr_reg(code,i["rt"],q,lo)})
            guard.append(z)
wr(out/"LA2_BOUNDS_BRANCHES.tsv",guard,["image","pc","file_offset","bytes","instruksi","function_pc","branch_or_compare","left_expr","right_expr"])
hyp=[
 {"hypothesis":"H1 x equals level delta d (not proven; K1)","support_1":"0x800D49D0 loads a byte from an address indexed by 0x8013EA6E and 0x8013EB1C within a manager-derived base","support_2":"0x800D49D8 writes that loaded byte into manager+0x530, later consumed by F2A9C","falsifier":"A complete caller/dataflow trace proves the indexed byte is an effect/action selector independent of old/new level difference"},
 {"hypothesis":"H2 x is an effect/item/action selector (not proven; K1)","support_1":"D49D0 source is a byte selected from a mutable manager-backed record, not a direct subtraction of level operands in the local reaching-definition chain","support_2":"two other +0x530 stores copy the low byte read from 0x80139EC7; meaning of this global remains unknown despite its zero clears","falsifier":"A complete upstream trace proves all reachable +0x530 values are derived solely from signed level delta d"}
]
wr(out/"LA2_X_ID_HYPOTHESES.tsv",hyp,["hypothesis","support_1","support_2","falsifier"])
# LA3: direct/static-resolvable caller census for BE5D8 plus raw pointer words.
bt=0x800BE5D8
bcalls=all_pointer_callers(codes,bt,valid_pcs)
for x in ENTRY_BE_REFS:
    pc=x["pc"]; i=ci.get(pc)
    z=base_row(i) if i else {"image":"ENTRY1","pc":h32(pc),"file_offset":h32(fileoff(pc,"ENTRY1")),"bytes":"TIDAK TAHU","instruksi":"GHIDRA_REFERENCE"}
    z.update({"target":h32(bt),"kind":"GHIDRA_"+x["kind"],"classification":"GHIDRA_XREF caller="+x["caller_name"]+" entry="+x["caller_entry"]})
    bcalls.append(z)
wr(out/"LA3_BE5D8_CALLERS.tsv",bcalls,["image","pc","file_offset","bytes","instruksi","target","kind","classification","target_register"])
bptr=[]
for tag,blob in [("EXE",exe),("ENTRY1",entry)]:bptr.extend(pointer_words(blob,tag,bt))
wr(out/"LA3_BE5D8_POINTER_WORDS.tsv",bptr,["image","pc","file_offset","bytes","instruksi","value","classification"])
# B24C8: find enclosing manual prolog and all static callers to that function entry.
b24=0x800B24C8
bpro,breason=find_prolog(ci,b24,ENTRY_BASE)
bentry=bpro
bi=ci.get(bt); bn=ci.get(bt+4)
# The target itself may be the first instruction of the function. Check it
# before searching backward, otherwise a previous function prolog is returned.
if bi and bn and bi["op"]==9 and bi["rs"]==29 and bi["rt"]==29 and bi["imm"]<0 and bn["op"]==43 and bn["rs"]==29 and bn["rt"]==31:
    be_pro,be_reason=bt,"PROLOG_AT_TARGET_ADDiuSP_SWRA"
else:
    be_pro,be_reason=find_prolog(ci,bt,ENTRY_BASE)
be_entry=be_pro
be_rows=[]
for k in range(-7,9):
    i=ci.get(bt+k*4)
    if i:
        z=base_row(i);z.update({"target_pc":h32(bt),"manual_function_entry":h32(be_entry) if be_entry else "TIDAK TAHU"})
        be_rows.append(z)
wr(out/"LA3_BE5D8_MANUAL_FUNCTION.tsv",be_rows,["image","pc","file_offset","bytes","instruksi","target_pc","manual_function_entry"])
txt(out/"LA3_BE5D8_BOUNDARY_STATUS.txt","TARGET_FUNCTION=0x800BE5D8\nMANUAL_PROLOG="+(h32(be_entry) if be_entry else "TIDAK TAHU")+"\nBOUNDARY_METHOD="+be_reason+"\nCALLER_CENSUS=LA3_BE5D8_CALLERS.tsv plus LA3_BE5D8_POINTER_WORDS.tsv\n")
b24rows=[]
for k in range(-7,9):
    i=ci.get(b24+k*4)
    if i:
        z=base_row(i);z.update({"target_pc":h32(b24),"manual_function_entry":h32(bentry) if bentry else "TIDAK TAHU"})
        b24rows.append(z)
wr(out/"LA3_B24C8_MANUAL_CONTEXT.tsv",b24rows,["image","pc","file_offset","bytes","instruksi","target_pc","manual_function_entry"])
caller_rows=[]
if bentry is not None:
    for tag,code in codes:
        lo=EXE_BASE if tag=="EXE" else ENTRY_BASE
        for pc,i in code.items():
            if direct_target(i)==bentry:
                z=base_row(i);z.update({"target_function_entry":h32(bentry),"kind":"JAL" if i["op"]==3 else "J","classification":"DIRECT_CALLER"})
                caller_rows.append(z)
            if i["op"]==0 and i["fn"] in (8,9):
                v,why=const_value(code,i["rs"],pc,lo)
                if v==bentry:
                    z=base_row(i);z.update({"target_function_entry":h32(bentry),"kind":"JALR" if i["fn"]==9 else "JR","classification":"STATIC_REGISTER_TARGET"})
                    caller_rows.append(z)
wr(out/"LA3_B24C8_FUNCTION_CALLERS.tsv",caller_rows,["image","pc","file_offset","bytes","instruksi","target_function_entry","kind","classification"])
txt(out/"LA3_B24C8_BOUNDARY_STATUS.txt",
    "TARGET_STORE=0x800B24C8\nMANUAL_PROLOG="+(h32(bentry) if bentry else "TIDAK TAHU")+"\n"+
    "BOUNDARY_METHOD="+breason+"\nCALLERS=see LA3_B24C8_FUNCTION_CALLERS.tsv\n"+
    "LIMIT=backward linear prolog heuristic; if no unique prolog then function/caller set remain TIDAK TAHU\n")
# LA4 static-only and LA5 symbolic only for x whose identity/domain are not yet established.
txt(out/"LA4_STATIC_ONLY.txt","EMULATOR_LAUNCHES=0\nGAME_EXECUTIONS=0\nBIOS_USED=no\nSAVESTATE_USED=no\nRAM_DUMP_USED=no\n")
hrows=[]
for k in range(52):
    off=0x464F4+k*0x10
    val=int.from_bytes(exe[off:off+4],"little")
    pc=EXE_BASE+(off-EXE_FILE)
    signed=val if val<0x80000000 else val-0x100000000
    hrows.append({"image":"EXE","pc":h32(pc),"file_offset":h32(off),"bytes":hx(exe[off:off+4]),
                  "instruksi":"DATA_TABLE_U32","index":k,"H_raw_u32":h32(val),"H_signed":signed})
wr(out/"LA5_H_TABLE_52.tsv",hrows,["image","pc","file_offset","bytes","instruksi","index","H_raw_u32","H_signed"])
wr(out/"LA5_SYMBOLIC_UPGRADE_COST.tsv",[
 {"condition":"if runtime x supplied to F2A9C is proven in 0..51 and helper 0x8001552C is proven to consume H[x]","symbolic_result":"H(x)=u32[0x80055CF4 + 16*x] (conditional table lookup only)","status":"CONDITIONAL; x identity/range not proven in LA2"},
 {"condition":"x=d for level jump d>=2","symbolic_result":"TIDAK TAHU; x=d not established","status":"UNPROVEN"},
 {"condition":"x outside 0..51","symbolic_result":"TIDAK TAHU; out-of-range guard and memory behavior not established","status":"UNPROVEN"},
 {"condition":"numerical upgrade cost","symbolic_result":"TIDAK TAHU; no numeric formula derived","status":"UNKNOWN"}
],["condition","symbolic_result","status"])
# Replace the two oversized JA excerpts with bounded, deduplicated snippets.
def read_tsv(path):
    try:return list(csv.DictReader(Path(path).open(encoding="utf-8-sig"),delimiter="\t"))
    except Exception:return []
tracked=subprocess.check_output(["git","ls-files","-z","reports/stage1_economy"]).decode().split("\0")
deleted={"reports/stage1_economy/ja-run-42367635732/attempt-1/JA1_FUN_80014F10_BODY.tsv",
         "reports/stage1_economy/ja-run-42367635732/attempt-1/JA1_CALLER_WINDOWS.tsv"}
already=set()
for p in [x for x in tracked if x.endswith(".tsv") and ("ja-run-" in x or "ka-run-" in x) and x not in deleted]:
    for r in read_tsv(p):
        if r.get("image") in ("EXE","ENTRY1") and r.get("pc") and r.get("bytes"):
            try:already.add((r["image"],int(r["pc"],16)))
            except Exception:pass
replace=[]
for k in range(16):
    i=ce.get(0x80014F28+4*k)
    if i and ("EXE",i["pc"]) not in already:
        z=base_row(i);z.update({"source_file":"JA1_FUN_80014F10_BODY.tsv","excerpt_group":"FUN_80014F10_CORE_64B"})
        replace.append(z)
oldpath=Path("reports/stage1_economy/ja-run-42367635732/attempt-1/JA1_CALLER_WINDOWS.tsv")
for r in read_tsv(oldpath):
    try:pc=int(r["pc"],16);cp=r.get("call_pc","");tag=r.get("image","")
    except Exception:continue
    if tag not in ("EXE","ENTRY1") or (tag,pc) in already:continue
    raw=bytes(int(x,16) for x in r["bytes"].split())
    if len(raw)!=4:continue
    replace.append({"image":tag,"pc":r["pc"],"file_offset":r.get("file_offset","TIDAK TAHU"),
       "bytes":r["bytes"],"instruksi":r.get("instruksi","TIDAK TAHU"),
       "source_file":"JA1_CALLER_WINDOWS.tsv","excerpt_group":"CALLER_"+str(cp)})
wr(out/"LA0_JA_REPLACEMENT_EXCERPTS.tsv",replace,
   ["image","pc","file_offset","bytes","instruksi","source_file","excerpt_group"])
allpcs=defaultdict(set)
for p in [x for x in tracked if x.endswith(".tsv") and ("ja-run-" in x or "ka-run-" in x) and x not in deleted]:
    for r in read_tsv(p):
        try:
            if r.get("image") in ("EXE","ENTRY1") and r.get("pc") and r.get("bytes"):
                n=len(bytes(int(x,16) for x in r["bytes"].split()))
                if n==4:allpcs[r["image"]].add(int(r["pc"],16))
        except Exception:pass
for r in replace:
    try:allpcs[r["image"]].add(int(r["pc"],16))
    except Exception:pass
maxrun=0
for tag,pcs in allpcs.items():
    run=0;prev=None
    for pc in sorted(pcs):
        run=run+4 if prev is not None and pc==prev+4 else 4
        maxrun=max(maxrun,run);prev=pc
txt(out/"LA0_JA_REPLACEMENT_AUDIT.txt",
    "DELETED_ONLY=\n"+"\n".join(sorted(deleted))+"\n"+
    "REPLACEMENT_ROWS="+str(len(replace))+"\nREPLACEMENT_MAX_EXCERPT_BYTES=64\n"+
    "AGGREGATED_MAX_CONTIGUOUS_BYTES_ACROSS_RETAINED_JA_KA_TSV_ROWS="+str(maxrun)+"\n"+
    "NOTE=aggregate de-duplicates retained JA/KA TSV instruction rows by image+PC; prior independent evidence can overlap into longer contiguous ranges. New replacement excerpts stay within 16 words (64 B) per group.\n")
# Main report.
statuses=[
 "LA0=TUNTAS K3 if commit/run pagination and py_compile ledgers are complete; bot classification is heuristic",
 "LA1=SEBAGIAN K4; UA1 exact target-form census and caller/function-boundary context exported; table extent and dynamic dispatch remain TIDAK TAHU",
 "LA2=SEBAGIAN K3; D49D0 address expression and static store sites recorded; selected byte/domain and x semantics remain TIDAK TAHU",
 "LA3=SEBAGIAN K2/K3; direct/static-resolvable callers plus manual prolog scan; dynamic JALR/table refs remain TIDAK TAHU",
 "LA4=TUNTAS K4; static-only exclusion explicit (EMULATOR_LAUNCHES=0)",
 "LA5=BELUM K1; no numerical upgrade cost for d>=2 and x=d not proven"
]
report=("# LA0-LA5 static audit — SLPS-03553\n\n"+
 f"Baseline inklusif: {baseline}\nSource SHA: {source}\nHEAD saat analisis: {head_sha}\nEXE SHA-256: {EXE_SHA}\nEntry 1 SHA-256: {ENTRY_SHA}\nRuntime: EMULATOR_LAUNCHES=0.\n\n## Status\n"+
 "\n".join("- "+s for s in statuses)+
 "\n\n## Findings\n"+
 "- LA0: baseline-inclusive commit ledger, Actions all-event pagination, and py_compile seluruh skrip Python tercatat di LA0_LEDGER_* dan LA0_PYCOMPILE.tsv. Snapshot HEAD adalah sebelum commit publikasi laporan; commit publikasi tidak dapat menghitung dirinya sendiri.\n"+
 "- LA1/UA1: UA1_TARGET_REFERENCES.tsv memisahkan literal u32 LE, J/JAL, constant JR/JALR, pasangan LUI 0x800B + ADDIU/ORI 0x50AC, serta Ghidra xrefs. Jal encoding dihitung dari target 0x800B50AC dan harus 0x0C02D42B. UA1_CALLER_11A28_CONTEXT.tsv dan UA1_B50AC_FUNCTION_END.tsv mencatat konteks caller dan ujung fungsi. Pointer-table base/stride/count serta dynamic dispatch tetap TIDAK TAHU tanpa indexed-load+jump path.\n"+
 "- LA2: alamat efektif D49D0 harus dibaca dari LA2_D49D0_EFFECTIVE_ADDRESS.txt. Jika alamat bergantung pada pointer manager dan global mutable, byte result lbu tidak dapat dinyatakan sebagai himpunan statis. Store census mencakup dua image dan mencatat basis unresolved.\n"+
 "- LA3: BE5D8 census mencakup direct calls/jumps, constant jalr/jr, pointer words; target indirect tidak diinferensikan tanpa bukti. B24C8 parent memakai manual prolog heuristic.\n"+
 "- LA4: tidak ada emulator, game execution, BIOS, savestate, atau RAM dump.\n"+
 "- LA5: H table dicatat terpisah. Formula simbolik bersyarat bukan formula upgrade yang terbukti karena domain/identitas x unresolved. Hipotesis angka 400/800/1600 tidak dipakai; tidak ada fitting atau MATCH/CONTRADICTS.\n\n## TIDAK TAHU\n"+
 "- Basis/stride tabel pointer dan seluruh pengguna indirect sekitar 0x80055904/0x80055920 bila tidak ada chain LW+JALR yang terpecahkan.\n"+
 "- Definisi path-specific a2/a3 bila berasal dari incoming caller registers atau melintasi cabang.\n"+
 "- Setter wallet permanen otoritatif; H1/H2/H3 tetap hipotesis.\n"+
 "- Nilai runtime 0x8013EA6E, 0x8013EB1C, 0x8013EA74, byte terpilih D49D0, serta domain x yang dapat dicapai.\n"+
 "- Dynamic alias writers yang tidak dapat dipetakan ke effective address konstan.\n"+
 "- Apakah x=d atau effect/item/action selector; guard x<52 dan perilaku di luar tabel.\n"+
 "- Rumus numerik biaya upgrade untuk lompatan level d>=2.\n\n"+
 "Setiap baris bukti instruksi memiliki image, PC, file offset, bytes, instruksi. Setiap kutipan kontigu dipotong maksimum 64 byte. Static only.\n")
txt(out/"LA0_LA5_STATIC_REPORT.md",report)
bad=[str(p) for p in out.rglob("*") if p.is_file() and p.suffix.lower() not in {".txt",".tsv",".md"}]
if bad:raise SystemExit("NON_TEXT_OUTPUT_BLOCKED="+repr(bad))
print("LA_ANALYSIS=PASS")
print("LA0_SOURCE_COMMITS="+str(len(src_commits))+" HEAD_COMMITS="+str(len(head_commits))+" ACTIONS_RUNS="+str(len(ar))+" PAGES="+str(page))
print("LA0_PYCOMPILE="+str(sum(x.get("status")=="PASS" for x in pyrows))+"/"+str(len(pyrows)))
print("LA1_B50AC_POINTERS="+str(len(ptrs))+" TABLE_USERS="+str(len(ref_users))+" DIRECT_CALLS="+str(len(direct_b50)))
ua1_pair_count=sum(1 for x in ua1_rows if x["class"]=="LUI_800B_ADDIU_ORI_50AC_PAIR")
ua1_direct_count=sum(1 for x in ua1_rows if x["class"] in {"DIRECT_JAL","DIRECT_J","CONSTANT_JALR","CONSTANT_JR"})
ua1_xref_count=sum(1 for x in ua1_rows if x["class"]=="GHIDRA_XREF")
boundary_status=boundary_rows[0]["status"]
ua1_status="TUNTAS" if boundary_status=="RETURN_AND_NEXT_PROLOG_FOUND" else "SEBAGIAN"
ua1_summary=[
    "STATUS="+ua1_status,
    "CONFIDENCE=K4",
    "TARGET=0x800B50AC",
    "JAL_WORD_LITTLE_ENDIAN=0x0C02D42B",
    "U32_LE_POINTER_HITS="+str(len(ptrs)),
    "DIRECT_J_JAL_JR_JALR_HITS="+str(ua1_direct_count),
    "LUI_800B_ADDIU_ORI_50AC_PAIRS="+str(ua1_pair_count),
    "GHIDRA_XREF_ROWS="+str(ua1_xref_count),
    ("POINTER_IMAGES="+",".join(sorted(set(x["image"] for x in ptrs))) if ptrs else "POINTER_IMAGES=NONE"),
    "CANDIDATE_RECORD_BASES=0x800558E4,0x80055900,0x8005591C,0x80055938",
    "CANDIDATE_RECORD_SPACING=0x1C; table membership and extent TIDAK TAHU",
    "TABLE_ENTRY_COUNT=TIDAK TAHU",
    "TABLE_FEEDS_V0_AT_11A28="+table_v0_status,
    "V0_LAST_DEFINITION="+(h32(v0_def["pc"])+" "+v0_def["text"] if v0_def else "TIDAK TAHU"),
    "V0_EXPRESSION="+v0_expr,
    "FIRST_JR_RA_AFTER_B54DC="+(h32(first_jr["pc"])+" "+first_jr["text"] if first_jr else "TIDAK TAHU"),
    "NEXT_PROLOG_AFTER_FIRST_JR_RA="+(h32(next_prolog["pc"])+" "+next_prolog["text"] if next_prolog else "TIDAK TAHU"),
    "FUNCTION_END_STATUS="+boundary_status,
    "SOURCE_SCOPE=verified EXE and Entry 1; code candidates restricted to Ghidra CODE_INSTRUCTION map",
    "NO_RUNTIME=YES",
    "MATCHING_TSV=UA1_TARGET_REFERENCES.tsv;UA1_CALLER_11A28_CONTEXT.tsv;UA1_B50AC_FUNCTION_END.tsv"
]
txt(out/"UA1_TARGET_REFERENCE_SUMMARY.txt","\n".join(ua1_summary)+"\n")
print("UA1_STATUS="+ua1_status+" POINTERS="+str(len(ptrs))+" DIRECT="+str(ua1_direct_count)+" PAIRS="+str(ua1_pair_count)+" FIRST_JR="+(h32(first_jr["pc"]) if first_jr else "TIDAK TAHU")+" NEXT_PROLOG="+(h32(next_prolog["pc"]) if next_prolog else "TIDAK TAHU"))
print("LA2_EC7_WRITERS="+str(len(gw))+" PLUS530_STORES="+str(len(xstores))+" X_EXPR="+formula)
print("LA3_BE5D8_CALLERS="+str(len(bcalls))+" B24C8_PROLOG="+(h32(bentry) if bentry else "TIDAK_TAHU"))
print("EMULATOR_LAUNCHES=0")
PY
