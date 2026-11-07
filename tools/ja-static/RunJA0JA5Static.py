#!/usr/bin/env python3
"""JA0-JA5: bounded, text-only static reverse-engineering audit."""
from __future__ import annotations
import csv, hashlib, json, os, re, struct, subprocess, sys, urllib.request
from collections import Counter
from pathlib import Path
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_BASE, ENTRY_BASE = 0x80010000, 0x800AD450
MANAGER_SLOT = 0x8013EA74
EXE_FILE, ENTRY_FILE = 0x800, 0x10BB000
EXE_SHA = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
ENTRY_SHA = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
EXE_SIZE, ENTRY_SIZE = 385024, 596412
BASELINE = os.environ.get("JA_BASELINE", "09c071e6c496b61b0689499a641faa3aa482b145")
SNAPSHOT = os.environ.get("GITHUB_SHA", "")
OUT = Path(sys.argv[3]); OUT.mkdir(parents=True, exist_ok=True)
EXE_PATH, ENTRY_PATH = Path(sys.argv[1]), Path(sys.argv[2])
EXE_DETAIL, ENTRY_DETAIL, EXE_TARGETS, ZERO_DETAIL = map(Path, sys.argv[4:8])
PLUS530_PATH, EXE_PLUS4_PATH, PLUS4_PATH = map(Path, sys.argv[8:11])
REG = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7",
       "s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
LOADS = {"lb","lh","lw","lbu","lhu","lwl","lwr","ll"}
STORES = {"sb","sh","sw","swl","swr","sc"}
md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_LITTLE_ENDIAN)

def hx(b): return " ".join(f"{x:02X}" for x in b)
def h32(x): return f"0x{x & 0xffffffff:08X}"
def write_tsv(name, rows, fields):
    with (OUT/name).open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({key:("TIDAK TAHU" if row.get(key) is None or row.get(key)=="" else row.get(key)) for key in fields})
def write_text(name, s): (OUT/name).write_text(s, encoding="utf-8")
def fileoff(pc, tag):
    return EXE_FILE + pc - EXE_BASE if tag == "EXE" else ENTRY_FILE + pc - ENTRY_BASE

def decode_image(blob, tag):
    base, start = (EXE_BASE, EXE_FILE) if tag == "EXE" else (ENTRY_BASE, 0)
    data = blob[start:] if tag == "EXE" else blob
    out={}
    for off in range(0, len(data)-3, 4):
        raw=data[off:off+4]; pc=base+off; word=int.from_bytes(raw,"little")
        ins=next(md.disasm(raw,pc,count=1),None)
        mn=ins.mnemonic.lower() if ins else ".word"
        out[pc]={"pc":pc,"fileoff":fileoff(pc,tag),"bytes":raw,"word":word,
          "mn":mn,"text":(mn+" "+ins.op_str).strip() if ins else f".word {h32(word)}",
          "op":word>>26,"rs":(word>>21)&31,"rt":(word>>16)&31,"rd":(word>>11)&31,
          "sh":(word>>6)&31,"fn":word&63,"imm":((word&0xffff)^0x8000)-0x8000,
          "uimm":word&0xffff,"target":word&0x03ffffff}
    return out

def dest_reg(i):
    op,fn=i["op"],i["fn"]
    if op==0:
        if fn in (8,12,13,24,25,26,27,0x18,0x19,0x1a,0x1b): return None
        if fn==9: return i["rd"] or 31
        return i["rd"] or None
    if op==3: return 31
    if op in (1,2,4,5,6,7,0x28,0x29,0x2a,0x2b,0x2e,0x38,0x39,0x3a,0x3b): return None
    if op in (8,9,10,11,12,13,14,15,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,
              0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37): return i["rt"] or None
    return None

def last_def(code, reg, before, lo, max_back=1024):
    floor=max(lo, before-max_back*4)
    for pc in range(before-4, floor-1, -4):
        i=code.get(pc)
        if not i: continue
        if dest_reg(i)==reg:
            if reg in set(range(4,16)) | {24,25}:
                for cp in range(before-4, max(lo-4, i["pc"]-8), -4):
                    c=code.get(cp)
                    if c and (c["op"]==3 or (c["op"]==0 and c["fn"]==9)): return None
            return i
        if (i["op"]==3 or (i["op"]==0 and i["fn"]==9)) and reg in set(range(4,16)) | {24,25}:
            return None
    return None

def const_reg(code, reg, before, lo, depth=0, seen=None):
    if reg==0: return 0
    if depth>10: return None
    seen=set() if seen is None else seen
    if (reg,before) in seen: return None
    seen.add((reg,before)); d=last_def(code,reg,before,lo)
    if d is None: return None
    op,rs,rt,fn=d["op"],d["rs"],d["rt"],d["fn"]
    if op==0x0f: return (d["uimm"]<<16)&0xffffffff
    if op in (8,9):
        a=const_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
        return None if a is None else (a+d["imm"])&0xffffffff
    if op==0x0d:
        a=const_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
        return None if a is None else (a|d["uimm"])&0xffffffff
    if op==0 and fn in (0,0x21,0x23,0x25):
        if fn==0:
            a=const_reg(code,rt,d["pc"],lo,depth+1,seen.copy())
            return None if a is None else (a<<d["sh"])&0xffffffff
        a=const_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
        b=const_reg(code,rt,d["pc"],lo,depth+1,seen.copy())
        if a is None or b is None:return None
        return ({0x21:a+b,0x23:a-b,0x25:a|b}[fn])&0xffffffff
    return None

def trace_reg(code, tag, reg, before, lo, site_pc, role, out_rows, seen=None, depth=0):
    if depth>12:return "TIDAK TAHU: trace depth"
    seen=set() if seen is None else seen
    key=(reg,before)
    if key in seen:return "TIDAK TAHU: trace cycle"
    seen.add(key)
    if reg==0:return "CONSTANT_ZERO"
    d=last_def(code,reg,before,lo)
    if d is None:return "ENTRY_OR_CALLER_REGISTER=$"+REG[reg]
    row={"image":tag,"pc":h32(d["pc"]),"file_offset":h32(d["fileoff"]),"bytes":hx(d["bytes"]),
         "instruksi":d["text"],"site_pc":h32(site_pc),"role":role,"register":"$"+REG[reg]}
    out_rows.append(row)
    mn,op,rs,rt,fn=d["mn"],d["op"],d["rs"],d["rt"],d["fn"]
    if mn in LOADS:
        ea=const_reg(code,rs,d["pc"],lo)
        row["role"]="VALUE_LOAD"
        row["origin_detail"]="EA="+(h32((ea+d["imm"])&0xffffffff) if ea is not None else "DYNAMIC_BASE($"+REG[rs]+")"+(f"{d['imm']:+#x}"))
        if ea is None and rs!=0:
            return mn+" from dynamic EA; base "+trace_reg(code,tag,rs,d["pc"],lo,site_pc,"LOAD_BASE",out_rows,seen.copy(),depth+1)
        return row["origin_detail"]
    if op in (8,9,0x0c,0x0d,0x0e):
        op_name={8:"ADDI",9:"ADDIU",0x0c:"ANDI",0x0d:"ORI",0x0e:"XORI"}[op]
        row["role"]="VALUE_TRANSFORM"
        sub=trace_reg(code,tag,rs,d["pc"],lo,site_pc,"SOURCE",out_rows,seen.copy(),depth+1)
        row["origin_detail"]=op_name+" source="+sub+" immediate="+h32(d["uimm"])
        return row["origin_detail"]
    if op==0 and fn in (0,0x20,0x21,0x22,0x23,0x24,0x25,0x26):
        if fn==0:
            sub=trace_reg(code,tag,rt,d["pc"],lo,site_pc,"SOURCE",out_rows,seen.copy(),depth+1)
            row["role"]="VALUE_TRANSFORM"; row["origin_detail"]="SLL source="+sub
            return row["origin_detail"]
        left=trace_reg(code,tag,rs,d["pc"],lo,site_pc,"SOURCE_L",out_rows,seen.copy(),depth+1)
        right=trace_reg(code,tag,rt,d["pc"],lo,site_pc,"SOURCE_R",out_rows,seen.copy(),depth+1)
        row["role"]="VALUE_COMBINE"; row["origin_detail"]=mn+" left="+left+" right="+right
        return row["origin_detail"]
    row["role"]="VALUE_UNRESOLVED"; row["origin_detail"]="definition="+h32(d["pc"])
    return row["origin_detail"]

def blank_expr():
    return {"ptr":0,"const":0,"terms":{},"unknown":False}
def add_expr(a,b,sign=1):
    z={"ptr":a["ptr"]+sign*b["ptr"],"const":(a["const"]+sign*b["const"])&0xffffffff,
       "terms":dict(a["terms"]),"unknown":a["unknown"] or b["unknown"]}
    for k,v in b["terms"].items():z["terms"][k]=z["terms"].get(k,0)+sign*v
    z["terms"]={k:v for k,v in z["terms"].items() if v}
    return z
def scale_expr(a,n):
    return {"ptr":a["ptr"]*n,"const":(a["const"]*n)&0xffffffff,
            "terms":{k:v*n for k,v in a["terms"].items() if v*n},"unknown":a["unknown"]}
def effective_addr(code,i,lo):
    base=const_reg(code,i["rs"],i["pc"],lo)
    return ((base+i["imm"])&0xffffffff) if base is not None else None
def expr_reg(code,reg,before,lo,depth=0,seen=None):
    if depth>12:return {"ptr":0,"const":0,"terms":{},"unknown":True}
    seen=set() if seen is None else seen
    if (reg,before) in seen:return {"ptr":0,"const":0,"terms":{},"unknown":True}
    seen.add((reg,before))
    if reg==0:return blank_expr()
    d=last_def(code,reg,before,lo)
    if d is None:return {"ptr":0,"const":0,"terms":{"ENTRY_$"+REG[reg]:1},"unknown":False}
    op,rs,rt,fn=d["op"],d["rs"],d["rt"],d["fn"]
    if d["mn"] in LOADS:
        ea=effective_addr(code,d,lo)
        if ea==MANAGER_SLOT:return {"ptr":1,"const":0,"terms":{},"unknown":False}
        return {"ptr":0,"const":0,"terms":{"LOAD@"+f"{d['pc']:08X}":1},"unknown":ea is None}
    if op in (8,9):
        a=expr_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
        a["const"]=(a["const"]+d["imm"])&0xffffffff
        return a
    if op==0x0f:return {"ptr":0,"const":(d["uimm"]<<16)&0xffffffff,"terms":{},"unknown":False}
    if op==0x0d:
        a=expr_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
        if not a["terms"] and not a["ptr"]:a["const"]=(a["const"]|d["uimm"])&0xffffffff
        else:a["unknown"]=True
        return a
    if op==0 and fn in (0,2,3):
        a=expr_reg(code,rt,d["pc"],lo,depth+1,seen.copy())
        if fn==0:return scale_expr(a,1<<d["sh"])
        if fn==2:return {"ptr":0,"const":(a["const"]>>d["sh"]),"terms":{},"unknown":True}
        return {"ptr":0,"const":0,"terms":{"SRA@"+f"{d['pc']:08X}":1},"unknown":True}
    if op==0 and fn in (0x20,0x21,0x22,0x23):
        a=expr_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
        b=expr_reg(code,rt,d["pc"],lo,depth+1,seen.copy())
        return add_expr(a,b,-1 if fn in (0x22,0x23) else 1)
    if op==0 and fn==0x25:
        if rs==0:return expr_reg(code,rt,d["pc"],lo,depth+1,seen.copy())
        if rt==0:return expr_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
    return {"ptr":0,"const":0,"terms":{"DEF@"+f"{d['pc']:08X}":1},"unknown":True}
def expr_text(e):
    parts=[]
    if e["ptr"]:parts.append(str(e["ptr"])+"*EA74_PTR")
    if e["const"]:parts.append(h32(e["const"]))
    parts.extend(str(v)+"*"+k for k,v in sorted(e["terms"].items()))
    return " + ".join(parts) if parts else "0"
def value_origin(code,reg,before,lo):
    c=const_reg(code,reg,before,lo)
    if c is not None:
        d=last_def(code,reg,before,lo)
        kind="LITERAL_OR_IMMEDIATE" if d and d["op"] in (8,9,0x0f,0x0d) and (d["rs"]==0 or d["op"]==0x0f) else "CONSTANT_EXPRESSION"
        return kind+"="+h32(c)
    d=last_def(code,reg,before,lo)
    if d is None:return "ENTRY_OR_CALLER_VALUE=$"+REG[reg]
    if d["mn"] in LOADS:
        ea=effective_addr(code,d,lo)
        return "MEMORY_LOAD@"+h32(d["pc"])+"; EA="+(h32(ea) if ea is not None else "DYNAMIC")
    return h32(d["pc"])+" "+d["text"]+"; expression="+expr_text(expr_reg(code,reg,before,lo))

def instr_row(tag, i):
    return {"image":tag,"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),
            "bytes":hx(i["bytes"]),"instruksi":i["text"],"word":h32(i["word"])}

def bounded_window(code, tag, pc, lo=0):
    start=max(lo,pc-7*4)
    while start<=pc and start not in code:start+=4
    rows=[]
    for q in range(start,pc+9*4,4):
        if q not in code:break
        rows.append(instr_row(tag,code[q]))
        if len(rows)>=16:break
    return rows

def parse_details(path, tag):
    if not path.exists():return {},{}
    s=path.read_text(encoding="utf-8",errors="replace")
    blocks=list(re.finditer(r"=== TARGET (?:0x)?([0-9A-Fa-f]{8}) ===",s))
    functions={}; xrefs={}
    for n,m in enumerate(blocks):
        b=s[m.start():blocks[n+1].start() if n+1<len(blocks) else len(s)]
        target=int(m.group(1),16)
        f=re.search(r"function_entry=(?:0x)?([0-9A-Fa-f]{8})",b)
        functions[target]=int(f.group(1),16) if f else target
        for r in re.finditer(r"reference_from=(?:0x)?([0-9A-Fa-f]{8}) reference_type=([^\s]+).*?caller_entry=(?:0x)?([0-9A-Fa-f]{8}) caller_name=([^\r\n]+)",b):
            xrefs[(tag,target,int(r.group(1),16))]=(int(r.group(3),16),r.group(4).strip(),r.group(2))
    return functions,xrefs

def restrict_to_ghidra_code(code, path):
    if not path.exists():return {},{"listed":0,"kept":0,"mismatch":0,"outside":0}
    kept={}; listed=0;mismatch=0;outside=0
    for line in path.read_text(encoding="utf-8",errors="replace").splitlines():
        if not line.startswith("CODE_INSTRUCTION="):continue
        listed+=1
        parts=line[len("CODE_INSTRUCTION="):].split("|",2)
        if len(parts)!=3:continue
        try:pc=int(parts[0],16);raw=bytes.fromhex(parts[1])
        except Exception:continue
        i=code.get(pc)
        if i is None:outside+=1;continue
        if raw!=i["bytes"] or len(raw)!=4:mismatch+=1;continue
        kept[pc]=i
    return kept,{"listed":listed,"kept":len(kept),"mismatch":mismatch,"outside":outside}

def parse_function_ranges(path, tag):
    if not path.exists():return []
    rows=[]
    for line in path.read_text(encoding="utf-8",errors="replace").splitlines():
        m=re.match(r"^FUNCTION_RANGE=((?:0x)?[0-9A-Fa-f]{8})\|((?:0x)?[0-9A-Fa-f]{8})\|((?:0x)?[0-9A-Fa-f]{8})\|(.+)$",line)
        if not m:continue
        entry,start,end,name=m.groups()
        rows.append({"image":tag,"pc":h32(int(entry,16)),"file_offset":h32(fileoff(int(entry,16),tag))
          if (tag!="EXE" or int(entry,16)>=EXE_BASE) and (tag!="ENTRY1" or int(entry,16)>=ENTRY_BASE) else "TIDAK TAHU",
          "bytes":"TIDAK TAHU","instruksi":"FUNCTION_RANGE metadata only",
          "function_start":h32(int(start,16)),"function_end":h32(int(end,16)),"function_name":name})
    return rows

def containing_function(pc, ranges):
    matches=[r for r in ranges if int(r["function_start"],16)<=pc<=int(r["function_end"],16)]
    if not matches:return None
    return min(matches,key=lambda r:int(r["function_end"],16)-int(r["function_start"],16))

def parse_zero_detail(path):
    if not path.exists():return {}
    s=path.read_text(encoding="utf-8",errors="replace")
    out={}
    blocks=re.split(r"(?=^TARGET=)",s,flags=re.M)
    for b in blocks:
        m=re.search(r"^TARGET=(?:0x)?([0-9A-Fa-f]{8})",b,re.M)
        if not m:continue
        pc=int(m.group(1),16)
        get=lambda key: (re.search(r"^"+key+r"=(.*)$",b,re.M).group(1).strip()
                         if re.search(r"^"+key+r"=(.*)$",b,re.M) else "TIDAK TAHU")
        refs=[]
        for line in re.findall(r"^REF=(.*)$",b,re.M): refs.append(line)
        out[pc]={"entry":get("FUNCTION_ENTRY"),"name":get("FUNCTION_NAME"),
                 "start":get("FUNCTION_BODY_START"),"end":get("FUNCTION_BODY_END"),
                 "contains":get("FUNCTION_BODY_CONTAINS_TARGET"),"refs":refs}
    return out

def rows_tsv(path):
    if not path.exists():return []
    with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f,delimiter="\t"))

def get_api(url,token):
    req=urllib.request.Request(url,headers={"Authorization":"Bearer "+token,
      "Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"})
    with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)

def ledger(pyrows):
    commits=[];runs=[];errors=[]
    if not SNAPSHOT:return commits,runs,["SNAPSHOT_SHA_MISSING"]
    try:shas=subprocess.check_output(["git","rev-list","--reverse",BASELINE+"^.."+SNAPSHOT],text=True).splitlines()
    except Exception as e:
        errors.append("REV_LIST:"+type(e).__name__)
        shas=[BASELINE]+subprocess.check_output(["git","rev-list","--reverse",BASELINE+".."+SNAPSHOT],text=True).splitlines()
    token=os.environ.get("GH_TOKEN",""); repo=os.environ.get("GITHUB_REPOSITORY","")
    seen=set()
    for sha in shas:
        m=subprocess.check_output(["git","show","-s","--format=%H%x09%an%x09%ae%x09%cn%x09%ce%x09%s",sha],text=True).rstrip("\n").split("\t",5)
        if len(m)==6:
            bot=any(("bot" in x.lower() or "github-actions" in x.lower()) for x in m[1:5])
            commits.append({"sha":m[0],"type":"BOT" if bot else "MANUSIA","author":m[1],
              "author_email":m[2],"committer":m[3],"committer_email":m[4],"subject":m[5]})
        if not token or not repo:
            errors.append("ACTIONS_API_AUTH_UNAVAILABLE");continue
        page=1
        while True:
            try:j=get_api(f"https://api.github.com/repos/{repo}/actions/runs?head_sha={sha}&per_page=100&page={page}",token)
            except Exception as e:errors.append("ACTIONS_API:"+sha+":"+type(e).__name__);break
            items=j.get("workflow_runs",[])
            for run in items:
                rid=str(run.get("id"))
                if rid in seen:continue
                seen.add(rid); jobs=[]
                try:
                    jj=get_api(f"https://api.github.com/repos/{repo}/actions/runs/{rid}/jobs?per_page=100",token)
                    jobs=[str(z.get("name","?"))+":"+str(z.get("status","?"))+"/"+str(z.get("conclusion") or "NONE") for z in jj.get("jobs",[])]
                except Exception as e:errors.append("JOBS_API:"+rid+":"+type(e).__name__)
                runs.append({"run_id":rid,"event":run.get("event"),"workflow":run.get("name"),
                  "workflow_path":run.get("path"),"head_sha":run.get("head_sha"),"status":run.get("status"),
                  "conclusion":run.get("conclusion") or "NONE","attempt":run.get("run_attempt"),
                  "created_at":run.get("created_at"),"jobs":";".join(jobs) or "TIDAK TAHU",
                  "exit_code":"TIDAK_TAHU_API_NO_PROCESS_EXIT_CODE"})
            if len(items)<100:break
            page+=1
    rid=str(os.environ.get("GITHUB_RUN_ID",""))
    if rid and rid not in seen:
        runs.append({"run_id":rid,"event":os.environ.get("GITHUB_EVENT_NAME","push"),
          "workflow":"JA0-JA5 isolated static audit","workflow_path":".github/workflows/ja0-ja5-static.yml",
          "head_sha":SNAPSHOT,"status":"in_progress","conclusion":"NONE",
          "attempt":os.environ.get("GITHUB_RUN_ATTEMPT","1"),"created_at":"TIDAK_TAHU",
          "jobs":"ja0-ja5-static:in_progress/NONE","exit_code":"TIDAK_TAHU_RUNNING"})
    write_tsv("JA0_LEDGER_COMMITS.tsv",commits,
      ["sha","type","author","author_email","committer","committer_email","subject"])
    write_tsv("JA0_LEDGER_ACTIONS.tsv",runs,
      ["run_id","event","workflow","workflow_path","head_sha","status","conclusion","attempt","created_at","jobs","exit_code"])
    py_ok=sum(r["status"]=="PASS" for r in pyrows)
    write_text("JA0_LEDGER_SUMMARY.txt",
      "BASELINE_INCLUSIVE="+BASELINE+"\nSOURCE_SHA="+SNAPSHOT+"\n"+
      f"COMMITS_TOTAL={len(commits)}\nCOMMITS_HUMAN={sum(r['type']=='MANUSIA' for r in commits)}\n"+
      f"COMMITS_BOT={sum(r['type']=='BOT' for r in commits)}\nACTIONS_RUNS_ALL_EVENTS={len(runs)}\n"+
      f"ACTIONS_SCHEDULED={sum(r['event']=='schedule' for r in runs)}\nPY_COMPILE_TOTAL={len(pyrows)}\n"+
      f"PY_COMPILE_PASS={py_ok}\nPY_COMPILE_FAIL={len(pyrows)-py_ok}\nACTIONS_API_ERRORS={len(errors)}\n"+
      "\n".join(errors))
    write_text("JA0_FINAL_IA_LEDGER_RECONCILIATION.txt",
      "PRIOR_IA0_LEDGER_SOURCE_SHA=09c071e6c496b61b0689499a641faa3aa482b145\n"+
      "PRIOR_IA0_COMMITS_TOTAL=10\nPRIOR_IA0_COMMITS_HUMAN=7\nPRIOR_IA0_COMMITS_BOT=3\n"+
      "PRIOR_IA0_ACTIONS_RUNS_ALL_EVENTS=6\nPRIOR_IA0_ACTIONS_SCHEDULED=0\n"+
      "PRIOR_IA0_PY_COMPILE=64/64\n"+
      "RECONCILIATION=The prior IA ledger is retained as a baseline snapshot; JA0 recomputes its own inclusive ledger from the JA source SHA.\n"+
      "SOURCE_SHA="+SNAPSHOT+"\n")
    return commits,runs,errors

def build_ia_final_ledger():
    base="b9bd69a5c59ca5103a2144deef3604a6b5f5c4a9"
    final="09c071e6c496b61b0689499a641faa3aa482b145"
    shas=subprocess.check_output(["git","rev-list","--reverse",base+"^.."+final],text=True).splitlines()
    commits=[]
    for sha in shas:
        m=subprocess.check_output(["git","show","-s","--format=%H%x09%an%x09%ae%x09%cn%x09%ce%x09%s",sha],text=True).rstrip("\n").split("\t",5)
        if len(m)!=6:continue
        bot=any(("bot" in x.lower() or "github-actions" in x.lower()) for x in m[1:5])
        commits.append({"sha":m[0],"type":"BOT" if bot else "MANUSIA","author":m[1],
          "author_email":m[2],"committer":m[3],"committer_email":m[4],"subject":m[5]})
    source=Path("reports/stage1_economy/ia0-ia5-static-run-42359729128/attempt-1")
    old_actions=rows_tsv(source/"IA0_LEDGER_ACTIONS.tsv")
    for row in old_actions:
        if row.get("run_id")=="42359729128":
            row["status"]="completed";row["conclusion"]="success"
            row["jobs"]="ia0-ia5-static:completed/success"
            row["exit_code"]="0 (ACTIONS_RUN_SUMMARY.txt)"
    old_py=rows_tsv(source/"IA0_PYCOMPILE.tsv")
    if len(commits)!=10 or sum(r["type"]=="MANUSIA" for r in commits)!=7 or sum(r["type"]=="BOT" for r in commits)!=3:
        raise RuntimeError("IA final commit ledger count mismatch")
    if len(old_actions)!=6 or sum(r.get("event")=="schedule" for r in old_actions)!=0:
        raise RuntimeError("IA final Actions ledger count mismatch")
    if len(old_py)!=64 or sum(r.get("status")=="PASS" for r in old_py)!=64:
        raise RuntimeError("IA final py_compile ledger mismatch")
    fields_c=["sha","type","author","author_email","committer","committer_email","subject"]
    fields_a=["run_id","event","workflow","workflow_path","head_sha","status","conclusion","attempt","created_at","jobs","exit_code"]
    write_tsv("JA0_IA_FINAL_LEDGER_COMMITS.tsv",commits,fields_c)
    write_tsv("JA0_IA_FINAL_LEDGER_ACTIONS.tsv",old_actions,fields_a)
    write_tsv("JA0_IA_FINAL_PYCOMPILE.tsv",old_py,["path","status","reason"])
    summary=("BASELINE_INCLUSIVE="+base+"\nSOURCE_SHA="+final+"\n"+
      "COMMITS_TOTAL=10\nCOMMITS_HUMAN=7\nCOMMITS_BOT=3\n"+
      "ACTIONS_RUNS_ALL_EVENTS=6\nACTIONS_SCHEDULED=0\n"+
      "PY_COMPILE_TOTAL=64\nPY_COMPILE_PASS=64\nPY_COMPILE_FAIL=0\n"+
      "FINAL_IA_RUN_42359729128=completed/success; job=ia0-ia5-static; exit_code=0\n")
    write_text("JA0_IA_FINAL_LEDGER_SUMMARY.txt",summary)
    write_text("JA0_FINAL_IA_LEDGER_RECONCILIATION.txt",
      "IA_FINAL_LEDGER_COPIED_AND_RECONCILED_IN_THIS_JA_RUN_DIRECTORY=yes\n"+
      "COMMITS_TOTAL=10 (7 human, 3 bot)\nACTIONS_RUNS_ALL_EVENTS=6\n"+
      "ACTIONS_SCHEDULED=0\nPY_COMPILE=64/64\n"+
      "FINAL_IA_SOURCE_SHA="+final+"\n"+
      "THE_10TH_COMMIT_IS_09c071e6c496b61b0689499a641faa3aa482b145 (github-actions[bot])\n"+
      "THE_6TH_RUN_42359729128_IS_COMPLETED_SUCCESS_EXIT_CODE_0\n")
    return {"commits":len(commits),"human":7,"bot":3,"runs":len(old_actions),"scheduled":0,
            "py_total":len(old_py),"py_pass":64}

def detail_function_entry(functions, target):
    return functions.get(target,target)

def scan_calls(codes, xrefs, function_ranges):
    targets={0x80014F10:"FUN_80014F10",0x800F2A9C:"FUN_800F2A9C",
             0x800F3658:"FUN_800F3658",0x800DC2E0:"FUN_800DC2E0",
             0x800D15A8:"FUN_800D15A8",0x800EC574:"FUN_800EC574",
             0x800E7B38:"FUN_800E7B38",0x800E8190:"FUN_800E8190",
             0x800C5978:"FUN_800C5978",0x800DB29C:"FUN_800DB29C"}
    rows=[]; windows=[]
    for tag,code in codes.items():
        for pc,i in sorted(code.items()):
            target=None;kind=None
            if i["op"] in (2,3):
                target=((pc+4)&0xf0000000)|(i["target"]<<2)
                kind="JAL" if i["op"]==3 else "J"
            elif i["op"]==0 and i["fn"]==9:
                fr0=containing_function(pc,function_ranges.get(tag,[]))
                lo0=int(fr0["pc"],16) if fr0 else 0
                target=const_reg(code,i["rs"],pc,lo0)
                kind="JALR_CONSTANT" if target is not None else "JALR_DYNAMIC"
            if target in targets:
                caller=xrefs.get((tag,target,pc))
                if caller:
                    lo,name,ref_type=caller
                else:
                    fr=containing_function(pc,function_ranges.get(tag,[]))
                    lo=int(fr["pc"],16) if fr else None
                    name=fr["function_name"] if fr else "TIDAK TAHU"
                    ref_type="TIDAK TAHU"
                args={}
                for reg in range(4,8):
                    args["a"+str(reg-4)] = trace_arg_origin(code,reg,pc+8,lo) if lo is not None else "TIDAK TAHU: caller function boundary unavailable"
                row=instr_row(tag,i)
                row.update({"target":h32(target),"target_name":targets[target],"kind":kind,
                    "caller_entry":h32(lo) if lo is not None else "TIDAK TAHU","caller_function":name})
                for k,v in args.items():row["arg_"+k]=v
                row["reference_type"]=ref_type
                rows.append(row)
                for w in bounded_window(code,tag,pc,lo or 0):
                    w["call_pc"]=h32(pc);windows.append(w)
            # References that Ghidra resolves to the target but whose instruction is not a direct
            # J/JAL are retained separately as possible indirect or table-dispatch edges.
            # Track materialized function pointers; these are candidates, not proof of dispatch.
            if i["op"]==0x0f:
                reg=i["rt"]
                for q in range(pc+4,min(pc+9*4,pc+36),4):
                    j=code.get(q)
                    if not j:continue
                    if j["op"] in (8,9,0x0d) and j["rs"]==reg and j["rt"]==reg:
                        val=(((i["uimm"]<<16)+j["imm"]) if j["op"] in (8,9) else ((i["uimm"]<<16)|j["uimm"]))&0xffffffff
                        if val in targets:
                            rr=instr_row(tag,i);rr.update({"bytes":hx(i["bytes"]+j["bytes"]),
                              "instruksi":i["text"]+" ; "+j["text"],
                              "pair_pc":h32(j["pc"]),"pair_file_offset":h32(j["fileoff"]),
                              "pair_bytes":hx(j["bytes"]),"pair_instruction":j["text"],
                              "target":h32(val),"target_name":targets[val],
                              "kind":"LUI_PLUS_"+j["mn"].upper()})
                            fr=containing_function(pc,function_ranges.get(tag,[]))
                            rr["caller_entry"]=fr["pc"] if fr else "TIDAK TAHU"
                            rr["caller_function"]=fr["function_name"] if fr else "TIDAK TAHU"
                            rr.update({"arg_a0":"TIDAK TAHU","arg_a1":"TIDAK TAHU",
                              "arg_a2":"TIDAK TAHU","arg_a3":"TIDAK TAHU"})
                            rows.append(rr)
    direct_keys={(r["image"],int(r["pc"],16),r["target"]) for r in rows if re.fullmatch(r"0x[0-9A-Fa-f]{8}",r["pc"])}
    for (tag,target,pc),(lo,name,ref_type) in xrefs.items():
        if (tag,pc,h32(target)) in direct_keys:continue
        i=codes[tag].get(pc)
        if i is None:continue
        args={f"arg_a{k}":trace_arg_origin(codes[tag],reg,pc+8,lo) for k,reg in enumerate(range(4,8))}
        row=instr_row(tag,i)
        row.update({"target":h32(target),"target_name":targets.get(target,"TIDAK TAHU"),
          "kind":"GHIDRA_REFERENCE_NON_DIRECT","caller_entry":h32(lo),"caller_function":name,
          "reference_type":ref_type,**args})
        rows.append(row)
    # Raw pointer-word census includes unaligned offsets; it does not imply a call.
    ptr=[]
    raw_by={"EXE":EXE_PATH.read_bytes(),"ENTRY1":ENTRY_PATH.read_bytes()}
    for tag,data in raw_by.items():
        for target,label in targets.items():
            pat=struct.pack("<I",target);start=0
            while True:
                off=data.find(pat,start)
                if off<0:break
                start=off+1
                if tag=="EXE":
                    pc="HEADER" if off<EXE_FILE else h32(EXE_BASE+off-EXE_FILE)
                    fo=off
                else:
                    pc=h32(ENTRY_BASE+off);fo=ENTRY_FILE+off
                ptr.append({"image":tag,"pc":pc,"file_offset":h32(fo),"bytes":hx(data[off:off+4]),
                    "instruksi":"DATA_WORD_POINTER_CANDIDATE","target":h32(target),"target_name":label,
                    "kind":"POINTER_WORD","caller_entry":"TIDAK TAHU","caller_function":"TIDAK TAHU",
                    "arg_a0":"TIDAK TAHU","arg_a1":"TIDAK TAHU","arg_a2":"TIDAK TAHU","arg_a3":"TIDAK TAHU"})
    fields=["image","pc","file_offset","bytes","instruksi","pair_pc","pair_file_offset","pair_bytes","pair_instruction",
            "word","target","target_name","kind","reference_type","caller_entry","caller_function",
            "arg_a0","arg_a1","arg_a2","arg_a3"]
    write_tsv("JA1_CALL_SITES.tsv",rows+ptr,fields)
    write_tsv("JA1_CALLER_WINDOWS.tsv",windows,["image","pc","file_offset","bytes","instruksi","call_pc"])
    return rows,ptr,windows

def trace_arg_origin(code,reg,before,lo):
    d=last_def(code,reg,before,lo)
    if d is None:return "TIDAK TAHU: entry/caller register"
    op,rs,rt,fn=d["op"],d["rs"],d["rt"],d["fn"]
    if d["mn"] in LOADS:
        ea=const_reg(code,rs,d["pc"],lo)
        return d["mn"]+" EA="+(h32((ea+d["imm"])&0xffffffff) if ea is not None else "DYNAMIC(base=$"+REG[rs]+")")
    if op==0x0f:return "LUI_CONST="+h32((d["uimm"]<<16)&0xffffffff)
    if op in (8,9,0x0c,0x0d):
        sub=const_reg(code,rs,d["pc"],lo)
        if sub is not None:
            val=({8:sub+d["imm"],9:sub+d["imm"],0x0c:sub&d["uimm"],0x0d:sub|d["uimm"]}[op])&0xffffffff
            return "CONSTANT="+h32(val)
        return d["mn"]+" from $"+REG[rs]+" immediate="+h32(d["uimm"])
    if op==0 and fn in (0x21,0x23,0x25):
        a=const_reg(code,rs,d["pc"],lo);b=const_reg(code,rt,d["pc"],lo)
        if a is not None and b is not None:
            val={0x21:a+b,0x23:a-b,0x25:a|b}[fn]&0xffffffff
            return "CONSTANT="+h32(val)
        return d["mn"]+" operands=$"+REG[rs]+",$"+REG[rt]
    return "DEF@"+h32(d["pc"])+" "+d["text"]

def make_function_body(exe_code, function_ranges):
    target=0x80014F10
    fr=containing_function(target,function_ranges.get("EXE",[]))
    if fr:
        start=int(fr["function_start"],16);end=int(fr["function_end"],16)
        entry=fr["pc"]
    else:
        start=target;end=0x80014F64;entry=h32(target)
    pcs=[q for q in range(start,end+1,4) if q in exe_code]
    groups=[];current=[]
    for q in pcs:
        if current and (q!=current[-1]+4 or len(current)>=16):
            groups.append(current);current=[]
        current.append(q)
    if current:groups.append(current)
    rows=[];out=[]
    for group_no,group in enumerate(groups,1):
        for q in group:
            row=instr_row("EXE",exe_code[q]);row["excerpt_id"]=f"FUN_80014F10_{group_no:02d}"
            rows.append(row);out.append(row)
        if len(group)>16:raise RuntimeError("FUN_80014F10 body excerpt cap exceeded")
    write_tsv("JA1_FUN_80014F10_BODY.tsv",out,
      ["image","pc","file_offset","bytes","instruksi","word","excerpt_id"])
    decomp=[]
    meanings={
      0x80014F10:"owner = argument a0 & 0xFF",
      0x80014F14:"valid owner range: owner < 4",
      0x80014F1C:"invalid-owner path clears return value",
      0x80014F28:"base address constant construction begins (0x80070EA0)",
      0x80014F2C:"owner index scaled for the 0xB4-stride record",
      0x80014F34:"multiply owner by 0x30",
      0x80014F3C:"multiply owner by 0xB4",
      0x80014F40:"field offset +0x94 is added to record base",
      0x80014F48:"load existing u32 value at owner-record +0x94",
      0x80014F50:"compare existing value < argument a1",
      0x80014F5C:"conditionally write argument a1 when greater",
      0x80014F60:"valid-owner return path",
      0x80014F64:"valid-owner return value = 1"
    }
    for row in rows:
        pc=int(row["pc"],16)
        if pc in meanings:
            decomp.append({**row,"decomp_statement":meanings[pc]})
    write_tsv("JA1_FUN_80014F10_DECOMPILATION.tsv",decomp,
      ["image","pc","file_offset","bytes","instruksi","decomp_statement"])
    return rows

def access_census(path, tag, code):
    rows=[]
    for r in rows_tsv(path):
        if r.get("manager_slot_load_same_function")!="YES":continue
        try:pc=int(r["pc"],16);lo=int(r["function_entry"],16)
        except Exception:continue
        i=code.get(pc)
        if not i or i["imm"]!=4 or i["mn"] not in LOADS|STORES:continue
        row=instr_row(tag,i)
        e=expr_reg(code,i["rs"],pc,lo)
        tw=[(k,v) for k,v in e["terms"].items() if v==0x90]
        dynamic_idx=(e["ptr"]==1 and e["const"]==0 and len(e["terms"])==1 and len(tw)==1 and not e["unknown"])
        constant_idx=(e["ptr"]==1 and not e["terms"] and not e["unknown"] and e["const"]%0x90==0)
        confirmed=dynamic_idx or constant_idx
        idx=tw[0][0] if dynamic_idx else str(e["const"]//0x90) if constant_idx else "TIDAK TAHU"
        row.update({"kind":"WRITE" if i["mn"] in STORES else "READ",
          "function_entry":h32(lo),"base_register":"$"+REG[i["rs"]],
          "index":idx,"base_expression":expr_text(e),
          "classification":"RECORD_EA74_INDEX_STRIDE_0x90_CONFIRMED" if confirmed else "CANDIDATE_NOT_PROVEN",
          "value_origin":value_origin(code,i["rt"],pc,lo) if i["mn"] in STORES else "READ_FIELD"})
        rows.append(row)
    return rows

def x_writer_rows(path):
    return [r for r in rows_tsv(path) if r.get("manager_slot_load_same_function")=="YES"
            and r.get("displacement","").lower()=="0x530"
            and r.get("mnemonic","").lower() in {"sw","sh","sb"}]

def trace_x_sites(entry_code, entry_functions):
    sites=[(0x800D49D8,0x800D15A8,"store manager+530 at D49D8"),
           (0x800EC844,0x800EC574,"store manager+530 at EC844"),
           (0x800EC868,0x800EC574,"store manager+530 at EC868")]
    trace_rows=[];summary=[]
    for pc,fn,label in sites:
        i=entry_code.get(pc)
        if not i:
            summary.append({"image":"ENTRY1","pc":h32(pc),"file_offset":h32(fileoff(pc,"ENTRY1")),
              "bytes":"TIDAK TAHU","instruksi":"TIDAK TAHU","site_pc":h32(pc),
              "function_entry":h32(fn),"source_class":"TIDAK TAHU","domain":"TIDAK TAHU",
              "conclusion":"STORE_INSTRUCTION_NOT_DECODED"})
            continue
        chain=[]
        origin=trace_reg(entry_code,"ENTRY1",i["rt"],pc,fn,pc,"X_VALUE",chain)
        for n,r in enumerate(chain):
            r["chain_order"]=n+1
            r["site_label"]=label
            trace_rows.append(r)
        d=last_def(entry_code,i["rt"],pc,fn)
        mask="NONE"
        if d and d["op"]==0x0c and d["uimm"]==0xff:mask="LOW8"
        const=const_reg(entry_code,i["rt"],pc,fn)
        domain=("single constant "+h32(const) if const is not None else
                "0..255 conditional LOW8 only" if mask=="LOW8" else "TIDAK TAHU")
        summary.append({"image":"ENTRY1","pc":h32(pc),"file_offset":h32(i["fileoff"]),
          "bytes":hx(i["bytes"]),"instruksi":i["text"],"site_pc":h32(pc),
          "function_entry":h32(fn),"source_class":origin,"domain":domain,
          "mask":mask,"conclusion":"VALUE_SOURCE_NOT_CLOSED"})
    write_tsv("JA2_X_ORIGIN.tsv",trace_rows,
      ["image","pc","file_offset","bytes","instruksi","site_pc","site_label","role","register","origin_detail","chain_order"])
    write_tsv("JA2_X_SITE_SUMMARY.tsv",summary,
      ["image","pc","file_offset","bytes","instruksi","site_pc","function_entry","source_class","domain","mask","conclusion"])
    return summary

def make_h_table(exe_blob, entry_code):
    table=0x80055CF4
    off=EXE_FILE+table-EXE_BASE
    rows=[]
    for x in range(52):
        raw=exe_blob[off+16*x:off+16*x+4]
        if len(raw)!=4:continue
        v=int.from_bytes(raw,"little");s=v if v<0x80000000 else v-0x100000000
        rows.append({"image":"EXE","pc":h32(table+16*x),"file_offset":h32(off+16*x),
          "bytes":hx(raw),"instruksi":"DATA_TABLE_U32","index":x,"H_raw_u32":h32(v),"H_signed":s})
    write_tsv("JA2_H_TABLE_52.tsv",rows,
      ["image","pc","file_offset","bytes","instruksi","index","H_raw_u32","H_signed"])
    # A literal-zero reset is conditional evidence, not proof of an operational selector.
    zi=entry_code.get(0x800E8174)
    if zi and zi["mn"]=="sw" and zi["rt"]==0 and zi["imm"]==0x530:
        reach=[{"x":"0 (conditional reset store only)","table_index":"0","status":"VALUE_WRITTEN_NOT_PROVEN_READ_BY_F2A9C",
                "evidence_pc":h32(zi["pc"]),"image":"ENTRY1","file_offset":h32(zi["fileoff"]),
                "bytes":hx(zi["bytes"]),"instruksi":zi["text"]}]
    else:
        reach=[{"x":"TIDAK TAHU","table_index":"TIDAK TAHU","status":"ZERO_RESET_WRITER_NOT_VERIFIED",
                "evidence_pc":"TIDAK TAHU","image":"ENTRY1","file_offset":"TIDAK TAHU",
                "bytes":"TIDAK TAHU","instruksi":"TIDAK TAHU"}]
    write_tsv("JA2_H_REACHABLE.tsv",reach,
      ["x","table_index","status","evidence_pc","image","file_offset","bytes","instruksi"])
    return rows

def zero_target_report(zero_meta, entry_code, entry_blob, function_ranges):
    summaries=[];windows=[]
    for pc in (0x800B24C8,0x800BEDA4):
        meta=zero_meta.get(pc,{})
        i=entry_code.get(pc)
        fr=containing_function(pc,function_ranges.get("ENTRY1",[]))
        function_entry=fr["pc"] if fr else meta.get("entry","TIDAK TAHU")
        name=fr["function_name"] if fr else meta.get("name","TIDAK TAHU")
        fn_int=int(function_entry,16) if re.fullmatch(r"(?:0x)?[0-9a-fA-F]{8}",function_entry) else None
        lo=fn_int if fn_int is not None else max(ENTRY_BASE,pc-0x400)
        v0origin="TIDAK TAHU";idx="TIDAK TAHU"
        if i and (fr is not None or fn_int is not None):
            chain=[]
            e=expr_reg(entry_code,i["rs"],pc,lo)
            v0origin=expr_text(e)
            terms=[(k,v) for k,v in e["terms"].items() if v==2]
            if e["ptr"]==1 and not e["unknown"] and len(e["terms"])==1 and len(terms)==1 and e["const"]==0:
                idx=terms[0][0]
            elif e["ptr"]==1 and not e["unknown"] and not e["terms"] and e["const"]%2==0:
                idx=str(e["const"]//2)
            trace_reg(entry_code,"ENTRY1",i["rs"],pc,lo,pc,"STORE_BASE_V0",chain)
            for n,r in enumerate(chain):
                r["target_pc"]=h32(pc);r["function_entry"]=function_entry
                r["chain_order"]=n+1
                windows.append(r)
        incoming=";".join(meta.get("refs",[])) or "TIDAK TAHU"
        summary={"image":"ENTRY1","pc":h32(pc),"file_offset":h32(fileoff(pc,"ENTRY1")),
          "bytes":hx(i["bytes"]) if i else "TIDAK TAHU",
          "instruksi":i["text"] if i else "TIDAK TAHU",
          "function_entry":function_entry,"function_name":name,
          "body_contains_target":meta.get("contains","TIDAK TAHU"),
          "incoming_references":incoming,"v0_base_origin":v0origin,
          "participant_index":idx if idx!="TIDAK TAHU" else "TIDAK TAHU: $v0 effective-base provenance not closed"}
        summaries.append(summary)
        for row in bounded_window(entry_code,"ENTRY1",pc,lo):
            row["target_pc"]=h32(pc);row["window_type"]="target-local";windows.append(row)
    write_tsv("JA3_ZERO_WRITER_CONTEXT.tsv",summaries,
      ["image","pc","file_offset","bytes","instruksi","function_entry","function_name",
       "body_contains_target","incoming_references","v0_base_origin","participant_index"])
    write_tsv("JA3_ZERO_WRITER_EVIDENCE.tsv",windows,
      ["image","pc","file_offset","bytes","instruksi","target_pc","window_type","role","register","origin_detail","chain_order"])
    return summaries

def main():
    exe=EXE_PATH.read_bytes();entry=ENTRY_PATH.read_bytes()
    if len(exe)!=EXE_SIZE or hashlib.sha256(exe).hexdigest()!=EXE_SHA:raise SystemExit("EXE_IDENTITY_MISMATCH")
    if len(entry)!=ENTRY_SIZE or hashlib.sha256(entry).hexdigest()!=ENTRY_SHA:raise SystemExit("ENTRY1_IDENTITY_MISMATCH")
    ecraw=decode_image(exe,"EXE");icraw=decode_image(entry,"ENTRY1")
    ec,exe_code_stats=restrict_to_ghidra_code(ecraw,EXE_TARGETS)
    ic,entry_code_stats=restrict_to_ghidra_code(icraw,ZERO_DETAIL)
    write_text("JA0_CODE_IMPORT_SUMMARY.txt",
      "SCAN_DOMAIN=Ghidra-decoded instructions only; raw data words are separately pointer-scanned.\n"+
      "EXE_LISTED={listed}\nEXE_KEPT={kept}\nEXE_BYTE_MISMATCH={mismatch}\nEXE_OUTSIDE_IMAGE={outside}\n".format(**exe_code_stats)+
      "ENTRY1_LISTED={listed}\nENTRY1_KEPT={kept}\nENTRY1_BYTE_MISMATCH={mismatch}\nENTRY1_OUTSIDE_IMAGE={outside}\n".format(**entry_code_stats))
    codes={"EXE":ec,"ENTRY1":ic}
    pyrows=rows_tsv(OUT/"JA0_PYCOMPILE.tsv")
    commits,runs,ledger_errors=ledger(pyrows)
    ia_final=build_ia_final_ledger()
    src_changes=subprocess.check_output(["git","diff-tree","--no-commit-id","--name-status","-r",SNAPSHOT],text=True).splitlines()
    src_rows=[]
    for line in src_changes:
        parts=line.split("\t",1)
        if len(parts)==2:
            src_rows.append({"commit_sha":SNAPSHOT,"status":parts[0],"path":parts[1]})
    write_tsv("JA0_SOURCE_COMMIT_FILES.tsv",src_rows,["commit_sha","status","path"])
    ef,xrefe=parse_details(EXE_DETAIL,"EXE")
    inf,xrefi=parse_details(ENTRY_DETAIL,"ENTRY1")
    function_ranges={"EXE":parse_function_ranges(EXE_TARGETS,"EXE"),
                     "ENTRY1":parse_function_ranges(ZERO_DETAIL,"ENTRY1")}
    all_ranges=function_ranges["EXE"]+function_ranges["ENTRY1"]
    write_tsv("JA0_FUNCTION_RANGES.tsv",all_ranges,
      ["image","pc","file_offset","bytes","instruksi","function_start","function_end","function_name"])
    xrefs={**xrefe,**xrefi}

    call_rows,pointer_rows,call_windows=scan_calls(codes,xrefs,function_ranges)
    body=make_function_body(ec,function_ranges)
    rec4=access_census(EXE_PLUS4_PATH,"EXE",ec)+access_census(PLUS4_PATH,"ENTRY1",ic)
    write_tsv("JA1_RECORD_PLUS4.tsv",rec4,
      ["image","pc","file_offset","bytes","instruksi","kind","function_entry","base_register","index","base_expression","classification","value_origin"])
    zero_meta=parse_zero_detail(ZERO_DETAIL)
    xsummary=trace_x_sites(ic,inf)
    hrows=make_h_table(exe,ic)
    zsummary=zero_target_report(zero_meta,ic,entry,function_ranges)

    jal_words={0x0C0053C4:0x80014F10,0x0C03CAA7:0x800F2A9C,
               0x0C03CD96:0x800F3658,0x0C0370B8:0x800DC2E0}
    exact=[]
    for tag,code in codes.items():
        for word,target in jal_words.items():
            for pc,i in code.items():
                if i["word"]==word:
                    row=instr_row(tag,i)
                    row.update({"word":h32(word),"target":h32(target),"target_name":
                      {0x80014F10:"FUN_80014F10",0x800F2A9C:"FUN_800F2A9C",
                       0x800F3658:"FUN_800F3658",0x800DC2E0:"FUN_800DC2E0"}[target]})
                    exact.append(row)
    write_tsv("JA1_EXACT_JAL_WORDS.tsv",exact,
      ["image","pc","file_offset","bytes","instruksi","word","target","target_name"])

    # Attach detailed argument rows for calls into the three relevant Entry 1 functions.
    d15_callers=[r for r in call_rows if r.get("target") in (h32(0x800D15A8),h32(0x800EC574))]
    write_tsv("JA2_FUNCTION_CALLERS.tsv",d15_callers,
      ["image","pc","file_offset","bytes","instruksi","target","target_name","kind","caller_entry","caller_function",
       "arg_a0","arg_a1","arg_a2","arg_a3"])

    # Hypotheses have explicit supports and falsifiers, tied to decoded instructions.
    hypotheses=[]
    for pc in (0x80014F48,0x80014F50,0x80014F5C,0x80014F64):
        i=ec.get(pc)
        if i:
            r=instr_row("EXE",i)
            r.update({"hypothesis":"H1_FUN14F10_MAX_FIELD_UPDATE","role":"SUPPORT",
              "interpretation":"Owner-indexed +0x94 field is read/compared/conditionally overwritten; wallet semantics not established."})
            hypotheses.append(r)
    for r in rec4:
        if r["kind"]=="WRITE":
            h=dict(r);h.update({"hypothesis":"H2_PARTICIPANT_PLUS4_IS_SEPARATE_STATE","role":"SUPPORT",
              "interpretation":"Participant record +4 has write sites, but authority/wallet semantics are unproven."})
            hypotheses.append(h)
            if len([x for x in hypotheses if x["hypothesis"]=="H2_PARTICIPANT_PLUS4_IS_SEPARATE_STATE"])>=4:break
    if not hypotheses:
        hypotheses=[{"image":"TIDAK TAHU","pc":"TIDAK TAHU","file_offset":"TIDAK TAHU","bytes":"TIDAK TAHU",
          "instruksi":"TIDAK TAHU","hypothesis":"WALLET","role":"NO_EVIDENCE","interpretation":"No supporting instruction rows exported."}]
    write_tsv("JA1_HYPOTHESIS_SUPPORT.tsv",hypotheses,
      ["image","pc","file_offset","bytes","instruksi","hypothesis","role","interpretation"])
    falsifiers=[
      {"hypothesis":"H1_FUN14F10_MAX_FIELD_UPDATE","falsifier":"A complete caller/dataflow proof that +0x94 is the authoritative wallet and that this max assignment is the wallet mutation."},
      {"hypothesis":"H2_PARTICIPANT_PLUS4_IS_SEPARATE_STATE","falsifier":"A complete alias/caller census showing +4 writes only temporary/display state and never reaches the authoritative wallet getter/setter."}
    ]
    write_tsv("JA1_HYPOTHESIS_FALSIFIERS.tsv",falsifiers,["hypothesis","falsifier"])
    jrows=[]
    def exact_row(image,pc):
        code=ec if image=="EXE" else ic
        return instr_row(image,code[pc]) if pc in code else None
    for hyp,sites,falsifier in [
      ("Hx1_X_EQUALS_DELTA_LEVEL",
       [("ENTRY1",0x800D49D8,"dynamic x write"),
        ("ENTRY1",0x800F2B58,"F2A9C reads x from manager+0x530"),
        ("ENTRY1",0x800F2B5C,"F2A9C sends x to table lookup helper"),
        ("ENTRY1",0x800DC2E0,"delta settlement parent function entry; see actual helper callsite rows")],
       "Any reachable writer/caller provenance proving x is assigned a non-delta effect/item/action selector."),
      ("Hx2_X_IS_EFFECT_ITEM_SELECTOR",
       [("ENTRY1",0x800EC844,"x masked to low 8 bits then stored"),
        ("ENTRY1",0x800EC868,"second x masked to low 8 bits then stored"),
        ("EXE",0x80055D44,"H table contains a signed negative entry at x=5")],
       "Complete writer/caller provenance proving every reachable x is copied from a computed level delta and no independent selector writer exists.")
    ]:
        for image,pc,note in sites:
            row=exact_row(image,pc)
            if row:
                row.update({"hypothesis":hyp,"role":"SUPPORT_K1","interpretation":note,"falsifier":falsifier})
                jrows.append(row)
    for call in call_rows:
        if call.get("target")==h32(0x80014F10):
            r=dict(call)
            r.update({"hypothesis":"Hx1_X_EQUALS_DELTA_LEVEL","role":"SUPPORT_K1",
              "interpretation":"DC2E0 caller passes participant owner and a second numeric argument to FUN_80014F10; this is delta-adjacent context, not proof x is that delta.",
              "falsifier":"Any reachable writer/caller provenance proving x is assigned a non-delta effect/item/action selector."})
            jrows.append(r)
    write_tsv("JA2_HYPOTHESES.tsv",jrows,
      ["image","pc","file_offset","bytes","instruksi","hypothesis","role","interpretation","falsifier"])

    # JA5 is limited to the only literal x observed in a manager+0x530 writer: a conditional reset to zero.
    h0=hrows[0] if hrows else None
    pred=[]
    if h0:
        zi=ic.get(0x800E8174)
        pred.append({"image":"ENTRY1","pc":h32(zi["pc"]) if zi else "TIDAK TAHU",
          "file_offset":h32(zi["fileoff"]) if zi else "TIDAK TAHU",
          "bytes":hx(zi["bytes"]) if zi else "TIDAK TAHU",
          "instruksi":zi["text"] if zi else "TIDAK TAHU",
          "x":"0 conditional reset only","H_raw_u32":h0["H_raw_u32"],"H_signed":h0["H_signed"],
          "F2CF8":"low16(H(0)*(G-2))","F2E38":"low16(-H(0)*(G-1-Q))",
          "F2E68":"low16(-H(0))","scope":"Only if helper reads the field after this reset writer; not a proven active gameplay x."})
    di=ic.get(0x800D49D8)
    pred.append({"image":"ENTRY1","pc":h32(di["pc"]) if di else "TIDAK TAHU",
      "file_offset":h32(di["fileoff"]) if di else "TIDAK TAHU",
      "bytes":hx(di["bytes"]) if di else "TIDAK TAHU","instruksi":di["text"] if di else "TIDAK TAHU",
      "x":"TIDAK TAHU for dynamic writers","H_raw_u32":"TIDAK TAHU","H_signed":"TIDAK TAHU",
      "F2CF8":"low16(H(x)*(G-2))","F2E38":"low16(-H(x)*(G-1-Q))",
      "F2E68":"low16(-H(x))","scope":"Dynamic x domain not closed by JA2; no d mapping/fitting."})
    write_tsv("JA5_SYMBOLIC_PREDICTIONS.tsv",pred,
      ["image","pc","file_offset","bytes","instruksi","x","H_raw_u32","H_signed","F2CF8","F2E38","F2E68","scope"])

    # Machine instruction excerpt windows never exceed 16 instructions / 64 bytes.
    for group in (call_windows,):
        counts=Counter(r.get("call_pc") for r in group)
        if any(n>16 for n in counts.values()):raise RuntimeError("JA instruction excerpt >16 rows")
    for excerpt in ("FUN_80014F10_01","FUN_80014F10_02"):
        if sum(r["excerpt_id"]==excerpt for r in body)>16:raise RuntimeError("JA function excerpt >16 rows")

    wallet_calls=[r for r in call_rows if r["target"]==h32(0x80014F10)]
    f2_calls=[r for r in call_rows if r["target"] in {h32(0x800F2A9C),h32(0x800F3658),h32(0x800DC2E0)}]
    py_ok=sum(r["status"]=="PASS" for r in pyrows)
    ia0="TUNTAS" if pyrows and py_ok==len(pyrows) and not ledger_errors else "SEBAGIAN"
    ia1="SEBAGIAN" if body and rec4 else "BELUM"
    ia2="SEBAGIAN" if len(xsummary)==3 else "BELUM"
    ia3="SEBAGIAN" if len(zsummary)==2 else "BELUM"
    ia4="TUNTAS"; ia5="SEBAGIAN"
    summary=f"""# JA0-JA5 static report
Baseline inklusif: {BASELINE}
Source SHA: {SNAPSHOT}
EXE SHA-256: {EXE_SHA}
Entry 1 SHA-256: {ENTRY_SHA}
Runtime status: NO EMULATOR / NO GAME / NO BIOS / NO SAVESTATE / NO RAM SNAPSHOT.

## Status
JA0={ia0} K4; commits={len(commits)}; all-event runs={len(runs)}; scheduled={sum(x['event']=='schedule' for x in runs)}; py_compile={py_ok}/{len(pyrows)}.
JA1={ia1} K4 static for FUN_80014F10 body; wallet-authoritative setter TIDAK TAHU. Direct/code caller rows={len(call_rows)}; target-14F10 callers={len(wallet_calls)}.
JA2={ia2} K3; writers traced={len(xsummary)}/3; dynamic x domain TIDAK TAHU; x=d not proven.
JA3={ia3} K3; zero-writer targets={len(zsummary)}/2; actual parent function / v0 index status is reported per target.
JA4=TUNTAS K4; no runtime execution.
JA5={ia5} K3; only a conditional x=0 reset value is numeric; all dynamic cases remain symbolic.

## JA0 — ledger
See JA0_LEDGER_COMMITS.tsv, JA0_LEDGER_ACTIONS.tsv, JA0_PYCOMPILE.tsv, JA0_LEDGER_SUMMARY.txt and JA0_SOURCE_COMMIT_FILES.tsv.
The final IA baseline ledger is copied as complete TSVs: 10 commits (7 human, 3 bot), 6 all-event runs, 0 scheduled, 64/64 py_compile. See JA0_IA_FINAL_LEDGER_COMMITS.tsv, JA0_IA_FINAL_LEDGER_ACTIONS.tsv, JA0_IA_FINAL_PYCOMPILE.tsv and JA0_IA_FINAL_LEDGER_SUMMARY.txt.

## JA1 — function and caller analysis
FUN_80014F10 body is split into JA1_FUN_80014F10_BODY.tsv excerpts of at most 16 instructions (64 bytes) each.
Call sites, exact JAL words, LUI+ADDIU/ORI pairs, raw pointer-word candidates and argument origins: JA1_CALL_SITES.tsv and JA1_EXACT_JAL_WORDS.tsv; contiguous windows: JA1_CALLER_WINDOWS.tsv.
Participant field +4 manager-backed census: JA1_RECORD_PLUS4.tsv.
The function computes 0x80070F34 + owner*0xB4, reads the current word, compares with argument a1, and writes a1 only when it is greater. The instruction-level proof is the 14F10 body TSV; it is not the participant +4 setter. Wallet-authoritative meaning remains TIDAK TAHU.
Decompilation normalized per instruction: JA1_FUN_80014F10_DECOMPILATION.tsv. Competing hypotheses and falsifiers: JA1_HYPOTHESIS_SUPPORT.tsv and JA1_HYPOTHESIS_FALSIFIERS.tsv.

## JA2 — manager+0x530 provenance
Per-site backward slices: JA2_X_ORIGIN.tsv; summary: JA2_X_SITE_SUMMARY.tsv; callsites to setter/writer functions: JA2_FUNCTION_CALLERS.tsv.
Table H, all 52 static entries: JA2_H_TABLE_52.tsv. Reachable-index conclusion: JA2_H_REACHABLE.tsv.
D49D8 source is a dynamic load; EC844/EC868 are masked dynamic values if their stores execute. The dynamic upstream inputs and full runtime-reachable x set are TIDAK TAHU. The literal zero store is a reset value, not proof that x=0 is an active delta.
Hypotheses x=d versus effect/item are K1 and include at least two instruction supports plus falsifier in JA2_HYPOTHESES.tsv. Neither is proven.

## JA3 — zero writer parents and index
Function manager, incoming references, v0 origin and participant-index conclusion are tabulated in JA3_ZERO_WRITER_CONTEXT.tsv. Instruction evidence windows and v0 definitions are in JA3_ZERO_WRITER_EVIDENCE.tsv. If Ghidra reports the site itself as a function entry, that does not alone prove this is the logical caller's function boundary; unresolved cases remain TIDAK TAHU.

## JA4 — runtime exclusion
No game, emulator, BIOS, savestate, runtime execution, or controlled input was used in this stage.

## JA5 — symbolic only
JA5_SYMBOLIC_PREDICTIONS.tsv uses only the literal x=0 reset store as a conditional case and otherwise retains H(x) symbolically. No fitting and no mapping x=d is asserted.

## TIDAK TAHU
- Wallet-authoritative setter and whether participant +4 is the permanent wallet.
- Whether any JALR / pointer-table candidate dispatches a relevant function at runtime.
- Dynamic origins and complete domain of manager+0x530, including the three requested writer values.
- Whether x is delta-level d or an effect/item/action selector.
- Actual enclosing function/caller for each zero-writer when the Ghidra function boundary remains split or missing.
- Effective manager base and participant index for the two zero-writer $v0 stores.
- Operational reachability of x=0 following the reset write.
- Any numeric upgrade cost for d>=2.
"""
    write_text("JA0_JA5_STATIC_REPORT.md",summary)
    write_text("JA1_WALLET_CONCLUSION.txt",
      "FUN_80014F10=owner-indexed max update to 0x80070F34+owner*0xB4, not proven wallet setter.\n"+
      "Callee has no demonstrated participant-record+4 store.\n"+
      "Wallet-authoritative setter=TIDAK TAHU.\n")
    write_text("JA4_STATIC_ONLY.txt",
      "EMULATOR_LAUNCHES=0\nGAME_EXECUTIONS=0\nBIOS_USED=no\nSAVESTATE_USED=no\nRAM_DUMP_USED=no\n")
    write_text("JA3_REPLACEMENT_FOR_REMOVED_GHIDRA_EXPORTS.txt",
      "The two oversized raw Ghidra dumps were removed under the approved exception.\n"+
      "Bounded replacements: JA1_FUN_80014F10_BODY.tsv, JA1_CALLER_WINDOWS.tsv, JA3_ZERO_WRITER_EVIDENCE.tsv.\n"+
      "Each contiguous excerpt is at most 16 MIPS instructions / 64 bytes.\n")
    print("JA0="+ia0+" JA1="+ia1+" JA2="+ia2+" JA3="+ia3+" JA4="+ia4+" JA5="+ia5)
    print("COMMITS="+str(len(commits))+" RUNS="+str(len(runs))+" PYCOMPILE="+str(py_ok)+"/"+str(len(pyrows)))
    print("IA_FINAL_LEDGER="+str(ia_final))

if __name__=="__main__":
    main()
