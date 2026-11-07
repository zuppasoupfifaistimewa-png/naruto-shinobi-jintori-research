#!/usr/bin/env python3
"""IA0-IA5 static-only analysis. Never runs an emulator or emits binary outputs."""
from __future__ import annotations
import csv, hashlib, json, os, re, struct, subprocess, sys, urllib.request
from collections import Counter
from pathlib import Path
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_PATH, ENTRY_PATH, OUT = map(Path, sys.argv[1:4])
BASELINE = os.environ.get("IA_BASELINE", "b9bd69a5c59ca5103a2144deef3604a6b5f5c4a9")
SNAPSHOT = os.environ.get("IA_SNAPSHOT", os.environ.get("GITHUB_SHA", ""))
EXE_BASE, ENTRY_BASE = 0x80010000, 0x800AD450
EXE_FILE, ENTRY_FILE = 0x800, 0x10BB000
EXE_SHA = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
ENTRY_SHA = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
EXE_SIZE, ENTRY_SIZE = 385024, 596412
MANAGER_SLOT, TABLE_VA = 0x8013EA74, 0x80055CF4
REG = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7",
       "s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
LOADS={"lb","lh","lw","lbu","lhu","lwl","lwr","ll"}
STORES={"sb","sh","sw","swl","swr","sc"}
MEM=LOADS|STORES
md=Cs(CS_ARCH_MIPS,CS_MODE_MIPS32|CS_MODE_LITTLE_ENDIAN)
OUT.mkdir(parents=True,exist_ok=True)

def hx(b): return " ".join(f"{x:02X}" for x in b)
def h32(v): return f"0x{v & 0xffffffff:08X}"
def write_tsv(name,rows,fields):
    with (OUT/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        w.writeheader(); w.writerows(rows)
def write_text(name,value): (OUT/name).write_text(value,encoding="utf-8")
def fileoff(pc,tag): return EXE_FILE+pc-EXE_BASE if tag=="EXE" else ENTRY_FILE+pc-ENTRY_BASE
def decode(blob,base,tag):
    code={}
    for off in range(0,len(blob)-3,4):
        raw=blob[off:off+4]; pc=base+off; word=int.from_bytes(raw,"little")
        x=next(md.disasm(raw,pc,count=1),None); mn=x.mnemonic.lower() if x else ".word"
        code[pc]={"pc":pc,"off":off,"fileoff":fileoff(pc,tag),"bytes":raw,"word":word,
          "mn":mn,"text":(mn+" "+x.op_str).strip() if x else f".word 0x{word:08X}",
          "op":word>>26,"rs":(word>>21)&31,"rt":(word>>16)&31,"rd":(word>>11)&31,
          "sh":(word>>6)&31,"fn":word&63,"imm":((word&0xffff)^0x8000)-0x8000,
          "uimm":word&0xffff,"target":word&0x03ffffff}
    return code
def dest_reg(i):
    op,fn=i["op"],i["fn"]
    if op==0:
        if fn in (8,9,12,13,24,25,26,27): return None
        return i["rd"] or None
    if op==3:return 31
    if op in (1,2,4,5,6,7,0x28,0x29,0x2a,0x2b,0x2e,0x38,0x39,0x3a,0x3b):return None
    if op in (8,9,10,11,12,13,14,15,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,
              0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37):return i["rt"] or None
    return None
CALLER_SAVED=set(range(4,16))|{24,25}
def last_def(code,reg,before,lo,max_back=1024):
    floor=max(lo,before-max_back*4)
    for pc in range(before-4,floor-1,-4):
        i=code.get(pc)
        if not i: continue
        if dest_reg(i)==reg:
            if reg in CALLER_SAVED:
                for cp in range(before-4,max(lo-4,i["pc"]-8),-4):
                    c=code.get(cp)
                    if c and (c["op"]==3 or (c["op"]==0 and c["fn"]==9)): return None
            return i
        if (i["op"]==3 or (i["op"]==0 and i["fn"]==9)) and reg in CALLER_SAVED:return None
    return None
def const_reg(code,reg,before,lo,depth=0,seen=None):
    if reg==0:return 0
    if depth>12:return None
    seen=set() if seen is None else seen
    if (reg,before) in seen:return None
    seen.add((reg,before)); d=last_def(code,reg,before,lo)
    if d is None:return None
    op,rs,rt,fn=d["op"],d["rs"],d["rt"],d["fn"]
    if op==0x0f:return (d["uimm"]<<16)&0xffffffff
    if op in (8,9,0x0d,0x0e):
        a=const_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
        if a is None:return None
        if op in (8,9):return (a+d["imm"])&0xffffffff
        if op==0x0d:return (a|d["uimm"])&0xffffffff
        return (a^d["uimm"])&0xffffffff
    if op==0 and fn in (0,2,3):
        a=const_reg(code,rt,d["pc"],lo,depth+1,seen.copy())
        if a is None:return None
        return ((a<<d["sh"]) if fn==0 else (a>>d["sh"]))&0xffffffff
    if op==0 and fn in (0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27):
        a=const_reg(code,rs,d["pc"],lo,depth+1,seen.copy())
        b=const_reg(code,rt,d["pc"],lo,depth+1,seen.copy())
        if a is None or b is None:return None
        return {0x20:a+b,0x21:a+b,0x22:a-b,0x23:a-b,0x24:a&b,0x25:a|b,0x26:a^b,0x27:~(a|b)}[fn]&0xffffffff
    return None
def blank(): return {"ptr":0,"const":0,"terms":{},"unknown":False}
def add_expr(a,b,sign=1):
    z={"ptr":a["ptr"]+sign*b["ptr"],"const":(a["const"]+sign*b["const"])&0xffffffff,
       "terms":dict(a["terms"]),"unknown":a["unknown"] or b["unknown"]}
    for k,v in b["terms"].items():z["terms"][k]=z["terms"].get(k,0)+sign*v
    z["terms"]={k:v for k,v in z["terms"].items() if v}; return z
def scale_expr(a,n):
    return {"ptr":a["ptr"]*n,"const":(a["const"]*n)&0xffffffff,
            "terms":{k:v*n for k,v in a["terms"].items() if v*n},"unknown":a["unknown"]}
def effective(code,i,lo):
    b=const_reg(code,i["rs"],i["pc"],lo)
    return ((b+i["imm"])&0xffffffff) if b is not None else None
def expr_reg(code,reg,before,lo,depth=0,seen=None):
    if depth>12:return {"ptr":0,"const":0,"terms":{},"unknown":True}
    seen=set() if seen is None else seen
    if (reg,before) in seen:return {"ptr":0,"const":0,"terms":{},"unknown":True}
    seen.add((reg,before))
    if reg==0:return blank()
    d=last_def(code,reg,before,lo)
    if d is None:return {"ptr":0,"const":0,"terms":{"ENTRY_$"+REG[reg]:1},"unknown":False}
    op,rs,rt,fn=d["op"],d["rs"],d["rt"],d["fn"]
    if d["mn"] in LOADS:
        ea=effective(code,d,lo)
        if ea==MANAGER_SLOT:return {"ptr":1,"const":0,"terms":{},"unknown":False}
        return {"ptr":0,"const":0,"terms":{"LOAD@"+f"{d['pc']:08X}":1},"unknown":ea is None}
    if op in (8,9):
        a=expr_reg(code,rs,d["pc"],lo,depth+1,seen.copy()); a["const"]=(a["const"]+d["imm"])&0xffffffff; return a
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
    p=[]
    if e["ptr"]:p.append(str(e["ptr"])+"*EA74_PTR")
    if e["const"]:p.append(h32(e["const"]))
    p.extend(str(v)+"*"+k for k,v in sorted(e["terms"].items()))
    return " + ".join(p) if p else "0"
def value_origin(code,reg,before,lo):
    c=const_reg(code,reg,before,lo)
    if c is not None:
        d=last_def(code,reg,before,lo)
        kind="LITERAL_OR_IMMEDIATE" if d and d["op"] in (8,9,0x0f,0x0d) and (d["rs"]==0 or d["op"]==0x0f) else "CONSTANT_EXPRESSION"
        return kind+"="+h32(c)
    d=last_def(code,reg,before,lo)
    if d is None:return "ENTRY_OR_CALLER_VALUE=$"+REG[reg]
    if d["mn"] in LOADS:
        ea=effective(code,d,lo)
        return "MEMORY_LOAD@"+h32(d["pc"])+"; EA="+(h32(ea) if ea is not None else "DYNAMIC")
    return h32(d["pc"])+" "+d["text"]+"; expression="+expr_text(expr_reg(code,reg,before,lo))
def rows_tsv(path):
    if not path.exists():return []
    with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f,delimiter="\t"))
def parse_details(path):
    if not path.exists():return {}
    s=path.read_text(encoding="utf-8",errors="replace")
    marks=list(re.finditer(r"=== TARGET (?:0x)?([0-9A-Fa-f]{8}) ===",s)); out={}
    for n,m in enumerate(marks):
        block=s[m.start():marks[n+1].start() if n+1<len(marks) else len(s)]
        target=int(m.group(1),16); fm=re.search(r"function_entry=(?:0x)?([0-9A-Fa-f]{8})",block)
        rawm=re.search(r"--- RAW_FUNCTION_BODY_BEGIN ---\s*(.*?)\s*--- RAW_FUNCTION_BODY_END ---",block,re.S)
        raw={}
        if rawm:
            for line in rawm.group(1).splitlines():
                mm=re.search(r"(?:0x)?([0-9A-Fa-f]{8})\s+bytes=\[([0-9A-Fa-f ]+)\]\s+(.+)$",line.strip())
                if mm:
                    pc=int(mm.group(1),16); b=bytes.fromhex(mm.group(2))
                    if len(b)==4:
                        x=next(md.disasm(b,pc,count=1),None); word=int.from_bytes(b,"little")
                        mn=x.mnemonic.lower() if x else ".word"
                        raw[pc]={"pc":pc,"bytes":b,"word":word,"mn":mn,
                          "text":(mn+" "+x.op_str).strip() if x else ".word",
                          "op":word>>26,"rs":(word>>21)&31,"rt":(word>>16)&31,"rd":(word>>11)&31,
                          "sh":(word>>6)&31,"fn":word&63,"imm":((word&0xffff)^0x8000)-0x8000,
                          "uimm":word&0xffff}
        cm=re.search(r"--- C_DECOMPILATION_BEGIN ---\s*(.*?)\s*--- C_DECOMPILATION_END ---",block,re.S)
        out[target]={"entry":int(fm.group(1),16) if fm else target,"raw":raw,
                     "decomp":cm.group(1).strip() if cm else ""}
    return out
def parse_access_list(path,tag,code,disp):
    out=[]
    for r in rows_tsv(path):
        if r.get("manager_slot_load_same_function")!="YES":continue
        try:pc=int(r["pc"],16); lo=int(r["function_entry"],16)
        except Exception:continue
        i=code.get(pc)
        if not i or i["mn"] not in MEM or i["imm"]!=disp:continue
        e=expr_reg(code,i["rs"],pc,lo); tw=[(k,v) for k,v in e["terms"].items() if v==0x90]
        dynamic_idx=(e["ptr"]==1 and e["const"]==0 and len(e["terms"])==1 and len(tw)==1 and not e["unknown"])
        constant_idx=(e["ptr"]==1 and not e["terms"] and not e["unknown"] and e["const"]%0x90==0)
        confirmed=dynamic_idx or constant_idx
        idx=tw[0][0] if dynamic_idx else str(e["const"]//0x90) if constant_idx else "TIDAK TAHU"
        store=i["mn"] in STORES
        out.append({"image":tag,"pc":h32(pc),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
          "instruksi":i["text"],"kind":"WRITE" if store else "READ",
          "index":idx,
          "value_origin":value_origin(code,i["rt"],pc,lo) if store else "READ_FROM_RECORD_FIELD",
          "function_entry":h32(lo),"base_expression":expr_text(e),
          "classification":"RECORD_EA74_INDEX_STRIDE_0x90_CONFIRMED" if confirmed else "CANDIDATE_NOT_PROVEN"})
    return out
def parse_writers(path,tag,code):
    rows=[]
    for r in rows_tsv(path):
        if r.get("manager_slot_load_same_function")!="YES":continue
        try:pc=int(r["pc"],16); lo=int(r["function_entry"],16)
        except Exception:continue
        i=code.get(pc)
        if not i or i["mn"] not in STORES or i["imm"]!=0x530:continue
        e=expr_reg(code,i["rs"],pc,lo); exact=e["ptr"]==1 and e["const"]==0 and not e["terms"] and not e["unknown"]
        c=const_reg(code,i["rt"],pc,lo); origin=value_origin(code,i["rt"],pc,lo)
        if c is not None:kind="LITERAL_OR_TURUNAN_KONSTAN"
        elif "MEMORY_LOAD@" in origin:kind="TABEL_ATAU_MEMORI_DINAMIS"
        elif "ENTRY_OR_CALLER" in origin:kind="ARGUMEN_ATAU_STATE_CALLER"
        else:kind="TURUNAN_DINAMIS"
        rows.append({"image":tag,"pc":h32(pc),"file_offset":h32(i["fileoff"]),"bytes":hx(i["bytes"]),
          "instruksi":i["text"],"function_entry":h32(lo),"base_expression":expr_text(e),
          "base_class":"EXACT_MANAGER_PLUS_0x530" if exact else "MANAGER_BASE_UNRESOLVED",
          "x_origin_class":kind,"x_constant":h32(c) if c is not None else "TIDAK TAHU",
          "x_value_origin":origin,"reachability":"STATIC_STORE_SITE_ONLY"})
    return rows
def scan_literal_words(exe,entry):
    needles={0x800F2A9C:"F2A9C",0x800F3658:"F3658"}; rows=[]; counts=Counter()
    for tag,data,base in (("EXE",exe,EXE_BASE),("ENTRY1",entry,ENTRY_BASE)):
        for value,label in needles.items():
            pat=struct.pack("<I",value); start=0
            while True:
                off=data.find(pat,start)
                if off<0:break
                start=off+1; counts[(tag,label)]+=1
                if tag=="EXE" and off<EXE_FILE:pc="HEADER"
                else:pc=h32(base+(off-EXE_FILE if tag=="EXE" else off))
                rows.append({"image":tag,"target":label,"pc":pc,
                  "file_offset":h32(off if tag=="EXE" else ENTRY_FILE+off),
                  "bytes":hx(data[off:off+4]),"instruksi":"DATA_WORD_OR_POINTER_LITERAL",
                  "word":h32(value),"alignment":"ALIGNED_4" if off%4==0 else "UNALIGNED"})
    return rows,counts
def get_api(url,token):
    req=urllib.request.Request(url,headers={"Authorization":"Bearer "+token,
      "Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"})
    with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
def ledger():
    commits=[]; runs=[]; errors=[]
    if not SNAPSHOT:return commits,runs,["SNAPSHOT_SHA_MISSING"]
    try:shas=subprocess.check_output(["git","rev-list","--reverse",BASELINE+"^.."+SNAPSHOT],text=True).splitlines()
    except Exception as e:
        errors.append("REV_LIST_PARENT_RANGE:"+type(e).__name__)
        shas=[BASELINE]+subprocess.check_output(["git","rev-list","--reverse",BASELINE+".."+SNAPSHOT],text=True).splitlines()
    token=os.environ.get("GH_TOKEN",""); repo=os.environ.get("GITHUB_REPOSITORY","")
    for sha in shas:
        m=subprocess.check_output(["git","show","-s","--format=%H%x09%an%x09%ae%x09%cn%x09%ce%x09%s",sha],text=True).rstrip("\n").split("\t",5)
        if len(m)==6:
            bot=any(("bot" in x.lower() or "github-actions" in x.lower()) for x in m[1:5])
            commits.append({"sha":m[0],"type":"BOT" if bot else "MANUSIA","author":m[1],"author_email":m[2],
              "committer":m[3],"committer_email":m[4],"subject":m[5]})
        if not token or not repo:errors.append("ACTIONS_API_AUTH_UNAVAILABLE");continue
        page=1
        while True:
            try:j=get_api(f"https://api.github.com/repos/{repo}/actions/runs?head_sha={sha}&per_page=100&page={page}",token)
            except Exception as e:errors.append("ACTIONS_API:"+sha+":"+type(e).__name__);break
            items=j.get("workflow_runs",[])
            for run in items:
                jobs=[]
                try:
                    jj=get_api(f"https://api.github.com/repos/{repo}/actions/runs/{run['id']}/jobs?per_page=100",token)
                    jobs=[str(z.get("name","?"))+":"+str(z.get("status","?"))+"/"+str(z.get("conclusion") or "NONE") for z in jj.get("jobs",[])]
                except Exception as e:errors.append("JOBS_API:"+str(run.get("id"))+":"+type(e).__name__)
                runs.append({"run_id":run.get("id"),"event":run.get("event"),"workflow":run.get("name"),
                  "workflow_path":run.get("path"),"head_sha":run.get("head_sha"),"status":run.get("status"),
                  "conclusion":run.get("conclusion") or "NONE","attempt":run.get("run_attempt"),
                  "created_at":run.get("created_at"),"jobs":";".join(jobs) or "TIDAK TAHU",
                  "exit_code":"TIDAK_TAHU_API_NO_PROCESS_EXIT_CODE"})
            if len(items)<100:break
            page+=1
    rid=os.environ.get("GITHUB_RUN_ID","")
    if rid and not any(str(x["run_id"])==rid for x in runs):
        runs.append({"run_id":rid,"event":os.environ.get("GITHUB_EVENT_NAME","push"),
          "workflow":"IA0-IA5 static audit","workflow_path":".github/workflows/ia0-ia5-static-audit.yml",
          "head_sha":SNAPSHOT,"status":"in_progress","conclusion":"NONE","attempt":os.environ.get("GITHUB_RUN_ATTEMPT","1"),
          "created_at":"TIDAK TAHU","jobs":"ia0-ia5-static:in_progress/NONE","exit_code":"TIDAK_TAHU_RUNNING"})
    return commits,runs,errors
def main():
    exe=EXE_PATH.read_bytes(); entry=ENTRY_PATH.read_bytes()
    if len(exe)!=EXE_SIZE or hashlib.sha256(exe).hexdigest()!=EXE_SHA:raise SystemExit("EXE_IDENTITY_MISMATCH")
    if len(entry)!=ENTRY_SIZE or hashlib.sha256(entry).hexdigest()!=ENTRY_SHA:raise SystemExit("ENTRY1_IDENTITY_MISMATCH")
    ec=decode(exe[EXE_FILE:],EXE_BASE,"EXE"); ic=decode(entry,ENTRY_BASE,"ENTRY1")
    commits,runs,ledger_errors=ledger()
    pyrows=rows_tsv(OUT/"IA0_PYCOMPILE.tsv"); py_ok=sum(x.get("status")=="PASS" for x in pyrows); py_bad=len(pyrows)-py_ok
    write_tsv("IA0_LEDGER_COMMITS.tsv",commits,["sha","type","author","author_email","committer","committer_email","subject"])
    write_tsv("IA0_LEDGER_ACTIONS.tsv",runs,["run_id","event","workflow","workflow_path","head_sha","status","conclusion","attempt","created_at","jobs","exit_code"])
    write_text("IA0_LEDGER_SUMMARY.txt",
      "BASELINE_INCLUSIVE="+BASELINE+"\nSOURCE_SHA="+SNAPSHOT+"\n"+
      f"COMMITS_TOTAL={len(commits)}\nCOMMITS_HUMAN={sum(x['type']=='MANUSIA' for x in commits)}\n"+
      f"COMMITS_BOT={sum(x['type']=='BOT' for x in commits)}\nACTIONS_RUNS_ALL_EVENTS={len(runs)}\n"+
      f"ACTIONS_SCHEDULED={sum(x['event']=='schedule' for x in runs)}\nPY_COMPILE_TOTAL={len(pyrows)}\n"+
      f"PY_COMPILE_PASS={py_ok}\nPY_COMPILE_FAIL={py_bad}\nACTIONS_API_ERRORS={len(ledger_errors)}\n"+
      "\n".join(ledger_errors))
    plus4=[]
    for tag,code in (("EXE",ec),("ENTRY1",ic)):
        plus4.extend(parse_access_list(OUT/(tag+"_PLUS4.tsv"),tag,code,4))
    write_tsv("IA1_RECORD_PLUS4_CENSUS.tsv",plus4,
      ["image","pc","file_offset","bytes","instruksi","kind","index","value_origin","function_entry","base_expression","classification"])
    xwriters=[]
    for tag,code in (("EXE",ec),("ENTRY1",ic)):
        xwriters.extend(parse_writers(OUT/(tag+"_PLUS530.tsv"),tag,code))
    write_tsv("IA2_X_WRITER_PROVENANCE.tsv",xwriters,
      ["image","pc","file_offset","bytes","instruksi","function_entry","base_expression","base_class","x_origin_class","x_constant","x_value_origin","reachability"])
    write_tsv("IA2_MANAGER_530_WRITERS.tsv",xwriters,
      ["image","pc","file_offset","bytes","instruksi","function_entry","base_expression","base_class","x_origin_class","x_constant","x_value_origin","reachability"])
    proven_x=set(); dynamic_x=False
    for x in xwriters:
        if x["base_class"]!="EXACT_MANAGER_PLUS_0x530":dynamic_x=True
        if x["x_constant"]!="TIDAK TAHU":
            v=int(x["x_constant"],16)
            if v<52:proven_x.add(v)
            else:dynamic_x=True
        else:dynamic_x=True
    reachable=",".join(str(x) for x in sorted(proven_x)) if proven_x and not dynamic_x else "TIDAK TAHU (writer/value provenance not closed)"
    exdetails=parse_details(OUT/"ghidra-exe-14f10.txt"); fd=exdetails.get(0x80014F10,{})
    decomp=fd.get("decomp","")
    write_text("IA1_FUN_80014F10_DECOMPILE.txt",
      "FUNCTION=0x80014F10\nFUNCTION_ENTRY="+(h32(fd.get("entry",0)) if fd else "TIDAK TAHU")+
      "\nDECOMPILATION="+("AVAILABLE" if decomp else "TIDAK TAHU")+
      "\n\n"+(decomp+"\n" if decomp else "TIDAK TAHU: Ghidra target body/decompilation was not emitted.\n"))
    direct=[]
    for i in fd.get("raw",{}).values():
        if i["op"]==3:direct.append((((i["pc"]+4)&0xf0000000)|(i["target"]<<2))&0xffffffff)
    write_text("IA1_WALLET_TRACE.txt",
      "TARGET=FUN_80014F10\nDIRECT_JAL_TARGETS="+(",".join(h32(x) for x in sorted(set(direct))) if direct else "TIDAK TAHU")+
      "\nRECORD_PLUS4_WRITE_SITES="+str(sum(x["kind"]=="WRITE" and "CONFIRMED" in x["classification"] for x in plus4))+
      "\nAUTHORITATIVE_WALLET_SETTER=TIDAK TAHU: direct calls do not establish permanent wallet mutation.\n")
    lrows,lcounts=scan_literal_words(exe,entry)
    write_tsv("IA3_POINTER_WORD_SCAN.tsv",lrows,
      ["image","target","pc","file_offset","bytes","instruksi","word","alignment"])
    idetails=parse_details(OUT/"ghidra-entry-targets.txt"); zero=[]
    for site in (0x800B24C8,0x800BEDA4):
        detail=idetails.get(site,{}); fn=detail.get("entry",site); loc=detail.get("raw",{})
        if not loc:
            zero.append({"pc":h32(site),"function_entry":h32(fn),"status":"TARGET_BODY_MISSING",
              "index":"TIDAK TAHU","base_expression":"TIDAK TAHU","index_origin":"TIDAK TAHU"})
            continue
        i=loc.get(site) or ic.get(site)
        if not i:
            zero.append({"pc":h32(site),"function_entry":h32(fn),"status":"INSTRUCTION_MISSING",
              "index":"TIDAK TAHU","base_expression":"TIDAK TAHU","index_origin":"TIDAK TAHU"})
            continue
        e=expr_reg(loc,i["rs"],site,fn); tw=[(k,v) for k,v in e["terms"].items() if v==2]
        idx=tw[0][0] if e["ptr"]==1 and len(tw)==1 and len(e["terms"])==1 and not e["unknown"] else (
            "0" if e["ptr"]==1 and not e["terms"] and not e["unknown"] else "TIDAK TAHU")
        idx_origin="CONSTANT_ZERO" if idx=="0" else tw[0][0] if idx!="TIDAK TAHU" else "TIDAK TAHU"
        zero.append({"pc":h32(site),"function_entry":h32(fn),"file_offset":h32(ENTRY_FILE+site-ENTRY_BASE),
          "bytes":hx(i["bytes"]),"instruksi":i["text"],"base_expression":expr_text(e),"index":idx,
          "index_origin":idx_origin,"status":"INDEX_DERIVED_STATISTICALLY" if idx!="TIDAK TAHU" else "INDEX_TIDAK_TAHU"})
        win=[]
        for pc in range(max(fn,site-15*4),site+1,4):
            q=loc.get(pc) or ic.get(pc)
            if q:win.append({"pc":h32(pc),"file_offset":h32(ENTRY_FILE+pc-ENTRY_BASE),
              "bytes":hx(q["bytes"]),"instruksi":q["text"]})
        write_tsv("IA3_ZERO_WRITER_"+f"{site:08X}"+"_WINDOW.tsv",win,
          ["pc","file_offset","bytes","instruksi"])
    write_tsv("IA3_ZERO_WRITER_INDICES.tsv",zero,
      ["pc","function_entry","file_offset","bytes","instruksi","base_expression","index","index_origin","status"])
    preds=[]; table_file=EXE_FILE+TABLE_VA-EXE_BASE
    for x in sorted(proven_x):
        raw=struct.unpack_from("<I",exe,table_file+16*x)[0]
        signed=raw if raw<0x80000000 else raw-0x100000000
        preds.append({"x":x,"H_raw_u32":h32(raw),"H_signed":signed,
          "F2CF8":"low16(H(x)*(G-2))","F2E38":"low16(-H(x)*(G-1-Q))",
          "F2E68":"low16(-H(x))","scope":"Exact table word; G and Q symbolic"})
    if not preds:
        preds=[{"x":"TIDAK TAHU","H_raw_u32":"TIDAK TAHU","H_signed":"TIDAK TAHU",
          "F2CF8":"low16(H(x)*(G-2))","F2E38":"low16(-H(x)*(G-1-Q))",
          "F2E68":"low16(-H(x))","scope":"x domain not established from IA2"})
    write_tsv("IA5_SYMBOLIC_STORE_PREDICTIONS.tsv",preds,
      ["x","H_raw_u32","H_signed","F2CF8","F2E38","F2E68","scope"])
    ia0="TUNTAS" if pyrows and py_bad==0 and not ledger_errors else "SEBAGIAN"
    ia1="SEBAGIAN" if plus4 or fd else "BELUM"
    ia2="SEBAGIAN" if xwriters else "BELUM"
    ia3="TUNTAS" if len(zero)==2 and all(x.get("status")=="INDEX_DERIVED_STATISTICALLY" for x in zero) else "SEBAGIAN"
    ia4="TUNTAS"; ia5="TUNTAS" if proven_x and not dynamic_x else "SEBAGIAN"
    ia0k="K4" if ia0=="TUNTAS" else "K3"
    lc={f"{a}_{b}":lcounts[(a,b)] for a in ("EXE","ENTRY1") for b in ("F2A9C","F3658")}
    report=f"""IA0-IA5 - audit statis helper, participant record, dan x
Baseline inklusif: {BASELINE}
Source SHA: {SNAPSHOT}
EXE SHA-256: {EXE_SHA}; Entry 1 SHA-256: {ENTRY_SHA}
Tidak ada emulator/game, input kontrol, BIOS, savestate, atau runtime replay.

STATUS
IA0={ia0} ({ia0k}); {len(commits)} commit inklusif; {len(runs)} run semua event; py_compile {py_ok}/{len(pyrows)}.
IA1={ia1} (K4); {len(plus4)} akses dari fungsi yang memuat slot manager; wallet setter otoritatif belum terbukti.
IA2={ia2} (K3); {len(xwriters)} writer/calon writer; x terjangkau={reachable}.
IA3={ia3} (K4); pointer counts={lc}.
IA4=TUNTAS (K4); peluncuran emulator/game=0.
IA5={ia5} (K3); prediksi dibatasi oleh x yang terbukti IA2; G/Q simbolik.

IA1 FUN_80014F10 DAN RECORD +4
Dekompilasi disimpan di IA1_FUN_80014F10_DECOMPILE.txt. Akses per-site ada di IA1_RECORD_PLUS4_CENSUS.tsv. RECORD_EA74_INDEX_STRIDE_0x90_CONFIRMED hanya diberikan jika ekspresi alamat membuktikan pointer EA74 ditambah satu indeks berkoefisien 0x90. CANDIDATE_NOT_PROVEN tetap kandidat, bukan akses peserta terkonfirmasi.
IA1_WALLET_TRACE.txt berisi JAL langsung dan alasan status setter.
TIDAK TAHU: apakah FUN_80014F10/callee mengubah saldo otoritatif; pemanggilan fungsi tidak membuktikan setter wallet.

IA2 MANAGER+0x530 (x)
IA2_X_WRITER_PROVENANCE.tsv berisi setiap store kandidat, asal base, dan asal nilai. Nilai literal/konstanta dapat dikenali; nilai load memori, argumen masuk, dan asal dinamis tetap TIDAK TAHU sampai provenance tertutup.
Himpunan x: {reachable}. Himpunan lengkap tidak diklaim apabila writer dinamis/calon base unresolved atau store tanpa reload global manager terlewat.
Dua hipotesis K1:
Hx1 - x terkait selisih level d. Dukungan: (1) x menjadi indeks H pada jalur F2A9C; (2) jalur terpisah DC2E0 meneruskan delta participant-record ke FUN_80014F10, sehingga mekanisme tetangga memang memproses delta. Falsifier: satu writer manager+0x530 terbukti memasok ID efek/item atau nilai non-delta.
Hx2 - x adalah ID efek/item/aksi. Dukungan: (1) H adalah lookup heterogen signed; (2) x adalah field manager terpisah dan tidak dihitung di F2A9C, sehingga selector eksternal masih mungkin. Falsifier: semua writer manager+0x530 yang terjangkau terbukti menyalin tepat selisih level d dan tidak ada writer selector lain.
Keduanya dugaan K1; tidak ada angka observasi eksternal, fitting, atau komparasi.

IA3 POINTER LITERAL DAN ZERO-WRITER
IA3_POINTER_WORD_SCAN.tsv berisi semua byte-word 0x800F2A9C/0x800F3658 di EXE dan Entry 1 termasuk unaligned. PC/file offset memakai formula masing-masing image. IA3_ZERO_WRITER_INDICES.tsv menurunkan basis/indeks untuk 0x800B24C8 dan 0x800BEDA4; tiap window per-site maksimum 16 instruksi/64 byte.

IA5 PREDIKSI SIMBOLIK
Hanya x yang terbukti oleh IA2 yang dipakai untuk lookup H. Store:
F2CF8 = low16(H(x)*(G-2))
F2E38 = low16(-H(x)*(G-1-Q))
F2E68 = low16(-H(x))
Jika domain x tidak tertutup, output mempertahankan H(x) dan rumus simbolik; x tidak disamakan dengan d.

TIDAK TAHU TERSISA
- Setter wallet otoritatif FUN_80014F10/callee dan kepastian record+4 sebagai saldo permanen.
- Akses +4 dari pointer yang diwariskan caller/alias tanpa reload slot global dalam fungsi yang sama.
- Writer +0x530 melalui pointer alias/caller, nilai tabel dinamis, dan domain x lengkap.
- Apakah x sama dengan d atau ID efek/item; kedua hipotesis K1.
- Apakah word pointer di scan adalah instruksi call, data tabel, atau literal tak dieksekusi; scan byte tidak membuktikan dispatch.
- Semantik transaksi runtime berada di luar tahap statis ini.
"""
    write_text("IA0_IA5_STATIC_REPORT.md",report)
    summary=("STATUS="+("PASS" if ia0=="TUNTAS" and ia3=="TUNTAS" else "PARTIAL")+
      "\nJOB=ia0-ia5-static\nSOURCE_SHA="+SNAPSHOT+"\nEXIT_CODE=0\n"+
      f"IA0={ia0}\nIA1={ia1}\nIA2={ia2}\nIA3={ia3}\nIA4={ia4}\nIA5={ia5}\n"+
      "GAME_OR_EMULATOR_EXECUTED=no\nBINARY_COMMITTED=no\n")
    write_text("ACTIONS_RUN_SUMMARY.txt",summary)
    print(summary)
    print("COUNTS="+json.dumps({"commits":len(commits),"runs":len(runs),"pycompile":len(pyrows),
      "record_plus4":len(plus4),"x_writers":len(xwriters),"reachable_x":reachable,
      "pointer_counts":lc,"zero_indices":zero},ensure_ascii=False))
if __name__=="__main__":main()
