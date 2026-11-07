#!/usr/bin/env python3
"""KA0-KA5: bounded static-only audit. No emulator/runtime inputs."""
from __future__ import annotations
import csv, hashlib, json, os, re, struct, subprocess, sys, urllib.request
from pathlib import Path
from collections import defaultdict
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_BASE, ENTRY_BASE = 0x80010000, 0x800AD450
EXE_FILE, ENTRY_FILE = 0x800, 0x10BB000
EXE_SHA = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
ENTRY_SHA = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
EXE_SIZE, ENTRY_SIZE = 385024, 596412
REG = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
LOAD_OPS = {0x20:"lb",0x21:"lh",0x23:"lw",0x24:"lbu",0x25:"lhu"}
STORE_OPS = {0x28:"sb",0x29:"sh",0x2b:"sw"}
R_FUN = {0x00:"sll",0x02:"srl",0x03:"sra",0x08:"jr",0x09:"jalr",0x21:"addu",0x23:"subu",0x24:"and",0x25:"or",0x26:"xor",0x2a:"slt",0x2b:"sltu"}
md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_LITTLE_ENDIAN)
md.detail = False

def sign16(v): return (v ^ 0x8000) - 0x8000
def hx(raw): return " ".join(f"{b:02X}" for b in raw)
def fileoff(pc, tag): return (EXE_FILE + pc - EXE_BASE) if tag == "EXE" else (ENTRY_FILE + pc - ENTRY_BASE)
def reg(n): return "$"+REG[n]
def ins_record(pc, raw, tag):
    word=int.from_bytes(raw,"little"); op=word>>26; rs=(word>>21)&31; rt=(word>>16)&31; rd=(word>>11)&31; sh=(word>>6)&31; fn=word&63; imm=sign16(word&0xffff)
    ins=next(md.disasm(raw,pc,count=1),None)
    text=(ins.mnemonic+" "+ins.op_str).strip() if ins else ".word 0x%08X"%word
    return {"pc":pc,"tag":tag,"raw":raw,"word":word,"op":op,"rs":rs,"rt":rt,"rd":rd,"sh":sh,"fn":fn,"imm":imm,"uimm":word&0xffff,"text":text,"mn":(ins.mnemonic.lower() if ins else ".word"),"fileoff":fileoff(pc,tag)}
def decode(blob,tag):
    base,start=(EXE_BASE,EXE_FILE) if tag=="EXE" else (ENTRY_BASE,0)
    data=blob[start:] if tag=="EXE" else blob
    out={}
    for off in range(0,len(data)-3,4):
        raw=data[off:off+4]; pc=base+off
        out[pc]=ins_record(pc,raw,tag)
    return out
def wr(path, rows, fields):
    with Path(path).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n",extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k:("TIDAK TAHU" if r.get(k) is None or r.get(k)=="" else r.get(k)) for k in fields})
def txt(path,s): Path(path).write_text(s,encoding="utf-8")
def base_row(i):
    return {"image":i["tag"],"pc":f"0x{i['pc']:08X}","file_offset":f"0x{i['fileoff']:08X}","bytes":hx(i["raw"]),"instruksi":i["text"]}
def jtarget(i):
    if i["op"] not in (2,3): return None
    return ((i["pc"]+4)&0xF0000000) | ((i["word"]&0x03ffffff)<<2)
def dest(i):
    op=i["op"]; fn=i["fn"]
    if op==0:
        if fn in (8,12,13,24,25,26,27): return None
        if fn==9: return i["rd"] or 31
        return i["rd"] or None
    if op in (2,3,4,5,6,7,0x28,0x29,0x2a,0x2b,0x38,0x39,0x3a,0x3b): return None
    if op in (1,8,9,10,11,12,13,14,15,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37): return i["rt"] or None
    return None
def last_def(code, r, before, lo, limit=768):
    floor=max(lo,before-limit*4)
    for pc in range(before-4,floor-1,-4):
        i=code.get(pc)
        if i and dest(i)==r: return i
    return None
def const_value(code,r,before,lo,depth=0,seen=None):
    if r==0: return 0,"ZERO"
    if depth>8: return None,"DEPTH_LIMIT"
    seen=set() if seen is None else seen
    key=(r,before)
    if key in seen: return None,"CYCLE"
    seen.add(key)
    d=last_def(code,r,before,lo)
    if not d: return None,"NO_DEF_IN_FUNCTION"
    op,fn,imm=d["op"],d["fn"],d["imm"]
    if op==15: return (d["uimm"]<<16)&0xffffffff,"LUI"
    if op in (8,9,13,12,14):
        src,why=const_value(code,d["rs"],d["pc"],lo,depth+1,seen)
        if src is None: return None,why
        if op in (8,9): return (src+imm)&0xffffffff,"ADDIU"
        if op==13: return (src|d["uimm"])&0xffffffff,"ORI"
        if op==12: return (src&d["uimm"])&0xffffffff,"ANDI"
        return (src^d["uimm"])&0xffffffff,"XORI"
    if op==0 and fn in (0,2,3,0x21,0x23,0x24,0x25,0x26):
        a,wa=const_value(code,d["rs"],d["pc"],lo,depth+1,seen.copy())
        b,wb=const_value(code,d["rt"],d["pc"],lo,depth+1,seen.copy())
        if a is None or b is None: return None,"RUNTIME_OPERAND"
        if fn==0: return (b<<d["sh"])&0xffffffff,"SLL"
        if fn==2: return b>>d["sh"],"SRL"
        if fn==3: return (b>>d["sh"]),"SRA"
        if fn==0x21: return (a+b)&0xffffffff,"ADDU"
        if fn==0x23: return (a-b)&0xffffffff,"SUBU"
        if fn==0x24: return a&b,"AND"
        if fn==0x25: return a|b,"OR"
        if fn==0x26: return a^b,"XOR"
    if op in LOAD_OPS: return None,"DYNAMIC_LOAD"
    return None,"UNSUPPORTED_DEF_"+d["mn"]
def trace_reg(code,r,before,lo,depth=0,seen=None,rows=None,limit=8):
    if rows is None: rows=[]
    if depth>=limit or r==0: return rows
    seen=set() if seen is None else seen
    key=(r,before)
    if key in seen: return rows
    seen.add(key)
    d=last_def(code,r,before,lo)
    if not d: return rows
    row=base_row(d); row.update({"register":reg(r),"depth":depth,"trace_role":"DEF","interpretasi":""})
    op,fn=d["op"],d["fn"]
    if op==15: row["interpretasi"]="konstanta high dari LUI"
    elif op in (8,9,12,13,14):
        row["interpretasi"]="immediate transform; operand sumber ditelusuri"
        trace_reg(code,d["rs"],d["pc"],lo,depth+1,seen,rows,limit)
    elif op in LOAD_OPS:
        row["interpretasi"]=f"load {LOAD_OPS[op]} dari {reg(d['rs'])}{d['imm']:+#x}; nilai memori dinamis kecuali alamat konstan"
        trace_reg(code,d["rs"],d["pc"],lo,depth+1,seen,rows,limit)
    elif op==0:
        if fn in (0,2,3): row["interpretasi"]="shift; operand sumber ditelusuri"; trace_reg(code,d["rt"],d["pc"],lo,depth+1,seen,rows,limit)
        elif fn in (0x21,0x23,0x24,0x25,0x26,0x2a,0x2b):
            row["interpretasi"]="operasi register; kedua operand ditelusuri"
            trace_reg(code,d["rs"],d["pc"],lo,depth+1,seen,rows,limit)
            trace_reg(code,d["rt"],d["pc"],lo,depth+1,seen,rows,limit)
        elif fn==9: row["interpretasi"]="jalr/hasil link"
        else: row["interpretasi"]="definisi register belum terklasifikasi"
    else: row["interpretasi"]="definisi belum dapat direduksi statis"
    rows.append(row)
    return rows
def parse_addr(s):
    m=re.search(r"(?:0x)?([0-9A-Fa-f]{8})$",s.strip())
    return int(m.group(1),16) if m else None
def parse_ghidra(path):
    pcs=set(); ranges=[]; refs=defaultdict(list); targets={}; current_target=None
    p=Path(path)
    if not p.exists(): return pcs,ranges,refs,targets
    for line in p.read_text(encoding="utf-8",errors="replace").splitlines():
        if line.startswith("CODE_INSTRUCTION="):
            field=line.split("=",1)[1].split("|",1)[0]
            a=parse_addr(field)
            if a is not None: pcs.add(a)
        elif line.startswith("FUNCTION_RANGE="):
            z=line.split("=",1)[1].split("|",3)
            if len(z)>=4:
                try:
                    ent,lo,hi=parse_addr(z[0]),parse_addr(z[1]),parse_addr(z[2])
                    if ent is not None and lo is not None and hi is not None: ranges.append((lo,hi,ent,z[3]))
                except: pass
        elif line.startswith("TARGET="):
            current_target=parse_addr(line.split("=",1)[1])
            if current_target is not None: targets[current_target]="seen"
        elif line.startswith("REF="):
            z=line.split("=",1)[1].split("|",3)
            if len(z)>=4 and current_target is not None:
                try:
                    caller=parse_addr(z[0])
                    if caller is not None: refs[current_target].append((caller,z[3],z[1]))
                except: pass
    return pcs,ranges,refs,targets
def containing(ranges,pc):
    xs=[x for x in ranges if x[0]<=pc<=x[1]]
    return min(xs,key=lambda x:x[1]-x[0]) if xs else None
def target_rows(code,ghidra_pcs,target):
    rows=[]
    for pc,i in code.items():
        if pc in ghidra_pcs and jtarget(i)==target:
            z=base_row(i); z.update({"kind":"J/JAL","target":f"0x{target:08X}","classification":"Ghidra instruction listing"})
            rows.append(z)
    for pc,i in code.items():
        if pc in ghidra_pcs and i["op"]==15:
            # LUI candidates paired with ADDIU/ORI to the exact target.
            for q in range(pc+4,pc+17,4):
                n=code.get(q)
                if n and n["rs"]==i["rt"] and n["op"] in (9,13):
                    v=((i["uimm"]<<16)+(n["imm"] if n["op"]==9 else n["uimm"]))&0xffffffff
                    if v==target:
                        z=base_row(i); z.update({"kind":"LUI+ADDIU/ORI","target":f"0x{target:08X}","classification":"constant construction","second_pc":f"0x{q:08X}","second_instruksi":n["text"]}); rows.append(z)
    return rows
def ptr_rows(blob,tag,target):
    base,start=(EXE_BASE,EXE_FILE) if tag=="EXE" else (ENTRY_BASE,0)
    data=blob[start:] if tag=="EXE" else blob
    out=[]
    needle=struct.pack("<I",target)
    p=0
    while True:
        p=data.find(needle,p)
        if p<0: break
        pc=base+p
        out.append({"image":tag,"pc":f"0x{pc:08X}","file_offset":f"0x{fileoff(pc,tag):08X}","bytes":hx(data[p:p+4]),"instruksi":"DATA_POINTER_WORD","kind":"pointer-word candidate","target":f"0x{target:08X}"})
        p+=1
    return out
def write_ledger(out,baseline,source):
    subprocess.run(["git","merge-base","--is-ancestor",baseline,source],check=True)
    commits=subprocess.check_output(["git","log","--format=%H%x09%an%x09%ae%x09%s",f"{baseline}^..{source}"]).decode().splitlines()
    cr=[]
    for line in commits:
        p=line.split("\t",3)
        if len(p)<4: continue
        sha,name,email,msg=p
        bot=("github-actions[bot]" in name or "dependabot" in name.lower() or "noreply.github.com" in email or "bot" in name.lower())
        cr.append({"sha":sha,"author":name,"email":email,"class":"BOT" if bot else "HUMAN","subject":msg})
    wr(out/"KA0_LEDGER_COMMITS.tsv",cr,["sha","author","email","class","subject"])
    api="https://api.github.com/repos/"+os.environ["GITHUB_REPOSITORY"]+"/actions/runs?per_page=100&page="
    token=os.environ.get("GH_TOKEN","")
    allruns=[]; page=1; total=None
    while page<=50:
        req=urllib.request.Request(api+str(page),headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"})
        with urllib.request.urlopen(req,timeout=45) as r: j=json.loads(r.read().decode())
        if total is None: total=j.get("total_count")
        rs=j.get("workflow_runs",[]); allruns.extend(rs)
        if not rs or len(allruns)>=int(total or 0): break
        page+=1
    ar=[]
    for x in allruns:
        ar.append({"run_id":x.get("id"),"name":x.get("name"),"event":x.get("event"),"status":x.get("status"),"conclusion":x.get("conclusion") or "TIDAK_TAHU","head_sha":x.get("head_sha"),"created_at":x.get("created_at")})
    wr(out/"KA0_LEDGER_ACTIONS.tsv",ar,["run_id","name","event","status","conclusion","head_sha","created_at"])
    pyrows=[]
    pyfiles=subprocess.check_output(["git","ls-files","-z","*.py"]).decode().split("\0")
    cache=Path(os.environ.get("PY_COMPILE_TSV",out/"KA0_PYCOMPILE.tsv"))
    # py_compile results are created by workflow, read them into the ledger.
    if cache.exists():
        with cache.open(encoding="utf-8") as f: pyrows=list(csv.DictReader(f,delimiter="\t"))
    n=len(cr); humans=sum(x["class"]=="HUMAN" for x in cr); bots=n-humans
    summary=(f"BASELINE_INCLUSIVE={baseline}\nSOURCE_SHA={source}\nCOMMITS_TOTAL={n}\nCOMMITS_HUMAN={humans}\nCOMMITS_BOT={bots}\n"+
             f"ACTIONS_RUNS_ALL_EVENTS={len(ar)}\nACTIONS_API_TOTAL_COUNT={total}\nACTIONS_PAGES_READ={page}\nACTIONS_SCHEDULED={sum(x['event']=='schedule' for x in ar)}\n"+
             f"PY_COMPILE_TOTAL={len(pyrows)}\nPY_COMPILE_PASS={sum(x.get('status')=='PASS' for x in pyrows)}\nPY_COMPILE_FAIL={sum(x.get('status')!='PASS' for x in pyrows)}\n"+
             "LEDGER_SCOPE=baseline^..source_sha (baseline inclusive); all workflow-run events; tracked Python scripts\n")
    txt(out/"KA0_LEDGER_SUMMARY.txt",summary)
    manifest=subprocess.check_output(["git","show","--format=","--name-status",source]).decode().strip()
    txt(out/"KA0_SOURCE_COMMIT_FILES.tsv","status\tpath\n"+manifest.replace("\t","\t")+( "\n" if manifest else ""))
    return cr,ar,pyrows
def main():
    exe=Path(sys.argv[1]).read_bytes(); entry=Path(sys.argv[2]).read_bytes()
    gh_exe=Path(sys.argv[3]); gh_entry=Path(sys.argv[4]); out=Path(sys.argv[5]); baseline=sys.argv[6]; source=sys.argv[7]
    out.mkdir(parents=True,exist_ok=True)
    if len(exe)!=EXE_SIZE or hashlib.sha256(exe).hexdigest()!=EXE_SHA: raise SystemExit("EXE_VERIFY_FAIL")
    if len(entry)!=ENTRY_SIZE or hashlib.sha256(entry).hexdigest()!=ENTRY_SHA: raise SystemExit("ENTRY1_VERIFY_FAIL")
    ce,ci=decode(exe,"EXE"),decode(entry,"ENTRY1")
    e_pcs,e_ranges,e_refs,e_targets=parse_ghidra(gh_exe); i_pcs,i_ranges,i_refs,i_targets=parse_ghidra(gh_entry)
    # KA0 ledger and current compile output.
    (commits,runs,pyrows)=write_ledger(out,baseline,source)
    # KA1: references/calls to FUN_800B50AC, direct and constant/pointer candidates.
    target=0x800B50AC
    ref_rows=[]
    for tag,code,pcs,refs,blob in [("EXE",ce,e_pcs,e_refs,exe),("ENTRY1",ci,i_pcs,i_refs,entry)]:
        for r in target_rows(code,pcs,target):
            r["image"]=tag; ref_rows.append(r)
        for r in ptr_rows(blob,tag,target): ref_rows.append(r)
        for caller,name,typ in refs.get(target,[]):
            x=code.get(caller)
            if x:
                z=base_row(x); z.update({"kind":"Ghidra reference "+typ,"target":f"0x{target:08X}","caller_function":name,"classification":"Ghidra reference"})
                ref_rows.append(z)
    wr(out/"KA1_B50AC_CALLERS.tsv",ref_rows,["image","pc","file_offset","bytes","instruksi","kind","target","classification","second_pc","second_instruksi","caller_function"])
    # Each call-site context is one bounded 16-instruction / 64-byte window.
    ka1_windows=[]
    seenw=set()
    for rr in ref_rows:
        if rr.get("kind") not in ("J/JAL",) and not str(rr.get("kind","")).startswith("Ghidra reference"): continue
        try: cp=int(rr["pc"],16)
        except: continue
        tag=rr.get("image",""); code=ce if tag=="EXE" else ci; pcs=e_pcs if tag=="EXE" else i_pcs
        if cp not in code or (pcs and cp not in pcs): continue
        key=(tag,cp)
        if key in seenw: continue
        seenw.add(key)
        for dlt in range(-7,9):
            insn=code.get(cp+dlt*4)
            if insn and (not pcs or insn["pc"] in pcs):
                z=base_row(insn); z.update({"call_pc":f"0x{cp:08X}","window_offset":dlt})
                ka1_windows.append(z)
    wr(out/"KA1_B50AC_CALLER_WINDOWS.tsv",ka1_windows,["image","pc","file_offset","bytes","instruksi","call_pc","window_offset"])
    # Detailed arguments at explicitly specified call PCs. Caller target addresses are verified below.
    calls=[("ENTRY1",0x800F5F54,0x800F2A9C),("ENTRY1",0x800B54DC,0x800F3658),("ENTRY1",0x800F5EBC,0x800DC2E0)]
    arg_rows=[]
    for tag,pc,want in calls:
        code=ci; ranges=i_ranges; target_ins=code.get(pc); fn=containing(ranges,pc); lo=fn[2] if fn else max(ENTRY_BASE,pc-0x1000)
        actual=jtarget(target_ins) if target_ins else None
        for r in (4,5,6,7):
            chain=trace_reg(code,r,pc,lo,limit=8)
            if not chain:
                arg_rows.append({"image":tag,"call_pc":f"0x{pc:08X}","call_target":f"0x{actual:08X}" if actual else "TIDAK TAHU","expected_target":f"0x{want:08X}","arg_register":reg(r),"origin_type":"TIDAK TAHU","depth":"TIDAK TAHU","evidence_pc":"TIDAK TAHU","file_offset":"TIDAK TAHU","bytes":"TIDAK TAHU","instruksi":"TIDAK TAHU","interpretasi":"No static reaching definition inside inferred function boundary"})
            for x in chain:
                arg_rows.append({"image":tag,"call_pc":f"0x{pc:08X}","call_target":f"0x{actual:08X}" if actual else "TIDAK TAHU","expected_target":f"0x{want:08X}","arg_register":reg(r),"origin_type":"TRACE","depth":x["depth"],"evidence_pc":x["pc"],"file_offset":x["file_offset"],"bytes":x["bytes"],"instruksi":x["instruksi"],"interpretasi":x["interpretasi"]})
    wr(out/"KA1_CALL_ARGUMENT_ORIGINS.tsv",arg_rows,["image","call_pc","call_target","expected_target","arg_register","origin_type","depth","evidence_pc","file_offset","bytes","instruksi","interpretasi"])
    wallet=("WALLET_AUTHORITATIVE_SETTER=TIDAK TAHU\n"+
      "FUN_80014F10 is not proven to write the participant wallet: JA evidence shows owner-indexed max update at record offset +0x94.\n"+
      "Candidate H1: participant record +0x04 may be wallet; support: repeated +0xB4-stride accesses and prior JA census of write candidates. Falsifier: direct cross-reference shows +0x04 belongs to a different field or is only UI/cache state.\n"+
      "Candidate H2: manager slot +0x4F4 may carry a signed settlement amount/delta; support: lw at ENTRY1 0x800DD1B8 and sign-normalization at 0x800DD1C8, followed by reset store at 0x800DD1DC. Falsifier: data-flow proves it is not wallet/balance state.\n"+
      "Neither candidate is asserted as the authoritative wallet setter (K1).\n")
    txt(out/"KA1_WALLET_STATUS.txt",wallet)
    wr(out/"KA1_WALLET_HYPOTHESES.tsv",[
      {"hypothesis":"H1 participant record +0x04 is wallet","support_1":"JA1_RECORD_PLUS4.tsv: repeated +0xB4-stride record accesses","support_2":"JA1_PLUS4_CONFIRMED_WRITES.tsv: five confirmed write sites, not semantic proof","falsifier":"A complete setter/reader trace identifies +0x04 as another field or transient cache"},
      {"hypothesis":"H2 manager slot +0x4F4 is authoritative wallet/delta","support_1":"ENTRY1 0x800DD1B8 lw $a1,0x4f4($a1)","support_2":"ENTRY1 0x800DD1C8 negu $a1,$a1 on negative branch; caller later clears slot","falsifier":"A complete producer/consumer trace shows slot is not wallet or settlement delta"}
    ],["hypothesis","support_1","support_2","falsifier"])
    # KA2: exact known-constant-address writers to the three globals; dynamic bases are explicitly left unresolved.
    globals_=[0x80139EC7,0x8013EA6E,0x8013EB1C]
    gw=[]; go=[]
    for tag,code,pcs,ranges in [("EXE",ce,e_pcs,e_ranges),("ENTRY1",ci,i_pcs,i_ranges)]:
        for pc,i in code.items():
            if pc not in pcs or i["op"] not in STORE_OPS: continue
            cv,why=const_value(code,i["rs"],pc,0x80010000 if tag=="EXE" else ENTRY_BASE)
            ea=((cv+i["imm"])&0xffffffff) if cv is not None else None
            size={0x28:1,0x29:2,0x2b:4}[i["op"]]
            for g in globals_:
                if ea is not None and ea<=g<ea+size:
                    z=base_row(i); z.update({"target_global":f"0x{g:08X}","store_op":STORE_OPS[i["op"]],"effective_address":f"0x{ea:08X}","width":size,"base_origin":why,"value_register":reg(i["rt"]),"classification":"EXACT_CONSTANT_EA" if ea==g else "OVERLAP_CONSTANT_EA"})
                    gw.append(z)
                    fn=containing(ranges,pc); lo=fn[2] if fn else (0x80010000 if tag=="EXE" else ENTRY_BASE)
                    for tr in trace_reg(code,i["rt"],pc,lo,limit=8):
                        q={"image":tag,"site_pc":f"0x{pc:08X}","target_global":f"0x{g:08X}","depth":tr["depth"],"evidence_pc":tr["pc"],"file_offset":tr["file_offset"],"bytes":tr["bytes"],"instruksi":tr["instruksi"],"interpretasi":tr["interpretasi"]}
                        go.append(q)
    wr(out/"KA2_GLOBAL_WRITERS.tsv",gw,["image","pc","file_offset","bytes","instruksi","target_global","store_op","effective_address","width","base_origin","value_register","classification"])
    wr(out/"KA2_GLOBAL_WRITER_VALUE_ORIGINS.tsv",go,["image","site_pc","target_global","depth","evidence_pc","file_offset","bytes","instruksi","interpretasi"])
    # Inherited, byte-bounded x writer evidence; explicitly record domains supported by lbu/andi.
    xsites=[
      ("ENTRY1",0x800D49D8,0x800D49D0,"sw $v0,0x530($a2)","lbu $v0,($v1)","0..255 conditional on executing path; source EA dynamic"),
      ("ENTRY1",0x800EC844,0x800EC81C,"sw $v0,0x530($v1)","lbu $v0,-0x6139($s0); andi 0xff","0..255 conditional on executing path"),
      ("ENTRY1",0x800EC868,0x800EC81C,"sw $v0,0x530($v1)","lbu $v0,-0x6139($s0); andi 0xff","0..255 conditional on executing path"),
    ]
    xrows=[]
    for tag,site,loadpc,store,sourceinstr,domain in xsites:
        i=ci.get(site); l=ci.get(loadpc)
        for insn,role in [(l,"VALUE_SOURCE"),(i,"X_STORE")]:
            if insn:
                z=base_row(insn); z.update({"site_pc":f"0x{site:08X}","role":role,"conditional_domain":domain})
                xrows.append(z)
    wr(out/"KA2_MANAGER_530_X_PROVENANCE.tsv",xrows,["image","pc","file_offset","bytes","instruksi","site_pc","role","conditional_domain"])
    # Extract/republish all 52 H values and index guard result.
    hrows=[]
    for k in range(52):
        off=0x464F4+(k*0x10)
        if off+4<=len(exe):
            val=int.from_bytes(exe[off:off+4],"little"); signed=val if val<0x80000000 else val-0x100000000
            pc=EXE_BASE+(off-EXE_FILE)
            hrows.append({"image":"EXE","pc":f"0x{pc:08X}","file_offset":f"0x{off:08X}","bytes":hx(exe[off:off+4]),"instruksi":"DATA_TABLE_U32","index":k,"H_raw_u32":f"0x{val:08X}","H_signed":signed})
    wr(out/"KA2_H_TABLE_52.tsv",hrows,["image","pc","file_offset","bytes","instruksi","index","H_raw_u32","H_signed"])
    x_domain="0..255 conditional, derived from byte loads / ANDI 0xFF in the three JA x-writer chains; execution reachability not established."
    txt(out/"KA2_X_DOMAIN.txt","X_DOMAIN="+x_domain+"\nH_TABLE_ENTRIES=52 (index 0..51)\nBOUNDS_PROVEN=NO\nDYNAMIC_EA_OR_POINTER_WRITERS=TIDAK TAHU\n")
    wr(out/"KA2_X_HYPOTHESES.tsv",[
      {"hypothesis":"x equals level delta d","support_1":"D49D8 receives lbu result (byte-valued); it is read at F2A9C","support_2":"DC2E0 has signed manager+0x4F4 settlement-like value; proximity is contextual only","falsifier":"A reachable writer assigns x from independent effect/item/action data, or complete caller provenance fails to link x to d"},
      {"hypothesis":"x is effect/item/action selector","support_1":"EC844/EC868 copy masked global byte 0x80139EC7 to manager+0x530","support_2":"F2A9C reads manager+0x530 and calls table helper 0x8001552C","falsifier":"Complete writer provenance proves every reachable x comes only from signed level delta d"}
    ],["hypothesis","support_1","support_2","falsifier"])
    # KA3 callers to BE5D8 and the B24C8 zero-store context.
    k3=[]
    for caller,name,typ in i_refs.get(0x800BE5D8,[]):
        z=ci.get(caller)
        if z:
            b=base_row(z); b.update({"kind":"Ghidra reference "+typ,"target":"0x800BE5D8","caller_function":name}); k3.append(b)
    for r in target_rows(ci,i_pcs,0x800BE5D8):
        r["image"]="ENTRY1"; r["caller_function"]="TIDAK TAHU"; k3.append(r)
    for r in ptr_rows(entry,"ENTRY1",0x800BE5D8): k3.append(r)
    wr(out/"KA3_BE5D8_CALLERS.tsv",k3,["image","pc","file_offset","bytes","instruksi","kind","target","caller_function","classification"])
    ka3_windows=[]; seen3=set()
    for rr in k3:
        if rr.get("kind") not in ("J/JAL",) and not str(rr.get("kind","")).startswith("Ghidra reference"): continue
        try: cp=int(rr["pc"],16)
        except: continue
        if cp not in ci or (i_pcs and cp not in i_pcs) or cp in seen3: continue
        seen3.add(cp)
        for dlt in range(-7,9):
            insn=ci.get(cp+dlt*4)
            if insn and (not i_pcs or insn["pc"] in i_pcs):
                z=base_row(insn); z.update({"call_pc":f"0x{cp:08X}","window_offset":dlt})
                ka3_windows.append(z)
    wr(out/"KA3_BE5D8_CALLER_WINDOWS.tsv",ka3_windows,["image","pc","file_offset","bytes","instruksi","call_pc","window_offset"])
    site=0x800B24C8; siteins=ci.get(site); fn=containing(i_ranges,site)
    lo=fn[2] if fn else max(ENTRY_BASE,site-0x1000)
    ctx=[]
    if siteins:
        z=base_row(siteins); z.update({"role":"TARGET_STORE","function_entry":f"0x{fn[2]:08X}" if fn else "TIDAK TAHU","function_name":fn[3] if fn else "TIDAK TAHU"})
        ctx.append(z)
        for tr in trace_reg(ci,siteins["rt"],site,lo,limit=8) if siteins["op"] in STORE_OPS else []:
            q={k:tr[k] for k in ["image","pc","file_offset","bytes","instruksi"] if k in tr}
            q.update({"role":"VALUE_REGISTER_ORIGIN","function_entry":f"0x{fn[2]:08X}" if fn else "TIDAK TAHU","function_name":fn[3] if fn else "TIDAK TAHU"})
            ctx.append(q)
        for tr in trace_reg(ci,siteins["rs"],site,lo,limit=8):
            q={k:tr[k] for k in ["image","pc","file_offset","bytes","instruksi"] if k in tr}
            q.update({"role":"V0_BASE_ORIGIN","function_entry":f"0x{fn[2]:08X}" if fn else "TIDAK TAHU","function_name":fn[3] if fn else "TIDAK TAHU"})
            ctx.append(q)
    wr(out/"KA3_B24C8_FUNCTION_V0_CONTEXT.tsv",ctx,["image","pc","file_offset","bytes","instruksi","role","function_entry","function_name"])
    z24=[]
    for dlt in range(-7,9):
        insn=ci.get(site+dlt*4)
        if insn and (not i_pcs or insn["pc"] in i_pcs):
            z=base_row(insn); z.update({"target_pc":f"0x{site:08X}","window_offset":dlt})
            z24.append(z)
    wr(out/"KA3_B24C8_WINDOW.tsv",z24,["image","pc","file_offset","bytes","instruksi","target_pc","window_offset"])
    refs_to_fn=[]
    if fn:
        entrypc=fn[2]
        for r in target_rows(ci,i_pcs,entrypc):
            r["image"]="ENTRY1"; r["caller_function"]="TIDAK TAHU"; refs_to_fn.append(r)
        for caller,name,typ in i_refs.get(entrypc,[]):
            z=ci.get(caller)
            if z:
                b=base_row(z); b.update({"kind":"Ghidra reference "+typ,"target":f"0x{entrypc:08X}","caller_function":name}); refs_to_fn.append(b)
    wr(out/"KA3_B24C8_PARENT_CALLERS.tsv",refs_to_fn,["image","pc","file_offset","bytes","instruksi","kind","target","caller_function","classification"])
    status3=("B24C8_CONTAINING_FUNCTION="+(fn[3] if fn else "TIDAK TAHU")+
             "\nB24C8_FUNCTION_ENTRY="+(f"0x{fn[2]:08X}" if fn else "TIDAK TAHU")+
             "\nB24C8_V0_BASE=see KA3_B24C8_FUNCTION_V0_CONTEXT.tsv; dynamic if not reduced\n")
    txt(out/"KA3_BOUNDARY_STATUS.txt",status3)
    # KA4.
    txt(out/"KA4_STATIC_ONLY.txt","EMULATOR_LAUNCHES=0\nGAME_EXECUTIONS=0\nBIOS_USED=no\nSAVESTATE_USED=no\nRAM_DUMP_USED=no\n")
    # KA5: strictly symbolic; no fitted constants and no numeric claim for out-of-range x.
    wr(out/"KA5_SYMBOLIC_COST.tsv",[
      {"condition":"if x in 0..51 and helper uses H[x]","symbolic_result":"H(x) = H_TABLE_52[x]","evidence":"JA2_H_TABLE_52.tsv + F2A9C manager+0x530 read; index use still requires exact helper trace"},
      {"condition":"x in 52..255 under current conditional byte domain","symbolic_result":"TIDAK TAHU / outside the 52-entry table; adjacent-memory semantics unknown","evidence":"No proven bounds guard x<52"},
      {"condition":"x=d","symbolic_result":"TIDAK TAHU; x=d unproven","evidence":"KA2_X_HYPOTHESES.tsv"},
      {"condition":"x=effect/item/action selector","symbolic_result":"TIDAK TAHU; selector meaning unproven","evidence":"KA2_X_HYPOTHESES.tsv"}
    ],["condition","symbolic_result","evidence"])
    # Main report and safety checks.
    statuses=["KA0=SEBAGIAN K3 (ledger/compile snapshot; run snapshot status finalized externally)","KA1=SEBAGIAN K3/K4 (byte/code evidence; wallet setter TIDAK TAHU)","KA2=SEBAGIAN K3 (three x writer chains; global dynamic writers and reachable x subset TIDAK TAHU)","KA3=SEBAGIAN K3 (caller census; B24C8 boundary may remain TIDAK TAHU)","KA4=TUNTAS K4 (EMULATOR_LAUNCHES=0)","KA5=SEBAGIAN K2 (conditional H(x), no numeric cost formula)"]
    report=("# KA0-KA5 static audit\n\n"+f"Baseline inklusif: {baseline}\nSource SHA: {source}\nEXE SHA-256: {EXE_SHA}\nEntry 1 SHA-256: {ENTRY_SHA}\nRuntime: EMULATOR_LAUNCHES=0.\n\n## Status\n"+"\n".join("- "+s for s in statuses)+
      "\n\n## Findings\n- KA1: direct call/reference candidates to FUN_800B50AC are in KA1_B50AC_CALLERS.tsv; argument origin slices at the three requested call PCs are in KA1_CALL_ARGUMENT_ORIGINS.tsv. Wallet-authoritative setter remains TIDAK TAHU.\n"+
      "- KA2: direct constant effective-address stores to globals 0x80139EC7, 0x8013EA6E and 0x8013EB1C are enumerated in KA2_GLOBAL_WRITERS.tsv. Indirect/dynamic bases remain TIDAK TAHU. Three manager+0x530 source chains have byte-limited conditional domain 0..255; no proof that x is delta d or that x<52.\n"+
      "- KA3: all Ghidra/direct references found for FUN_800BE5D8 are in KA3_BE5D8_CALLERS.tsv. B24C8 inferred function and $v0 origin are in KA3_B24C8_FUNCTION_V0_CONTEXT.tsv; missing ranges remain TIDAK TAHU.\n"+
      "- KA4: static-only; no emulator launch.\n"+
      "- KA5: only conditional H(x) expression for x in 0..51; out-of-range behavior unknown. No use of 400/800/1600, no fitting, no MATCH/CONTRADICTS labels.\n\n## TIDAK TAHU\n"+
      "- Wallet-authoritative setter and exact semantics of participant record +0x04.\n- Complete caller set for B50AC if indirect dispatch or Ghidra references are unresolved.\n"+
      "- Dynamic/indirect writers to the three global addresses and upstream origins of unresolved bases.\n- Full reachable values for x and whether x represents d or effect/item/action selector.\n"+
      "- Whether x is guarded to 0..51 before H table lookup and out-of-range behavior.\n"+
      "- B24C8's parent function/callers/$v0 base/index if Ghidra fails to establish a function boundary.\n"+
      "- Any numeric upgrade cost for level jumps d>=2.\n\n## Files\nAll instruction evidence TSV excerpts include image, PC, file offset, bytes and decoded instruction. Any single excerpt must remain <=64 contiguous bytes. Runtime was not used.\n")
    txt(out/"KA0_KA5_FINAL_REPORT.md",report)
    # Ensure no committed output can contain binary data or non-text extensions.
    bad=[str(p) for p in out.rglob("*") if p.is_file() and p.suffix.lower() not in {".txt",".tsv",".md"}]
    if bad: raise SystemExit("NON_TEXT_OUTPUT_BLOCKED="+repr(bad))
    print("KA_ANALYSIS=PASS")
    print("KA0_COMMITS="+str(len(commits))+" KA0_RUNS="+str(len(runs))+" KA0_PYCOMPILE="+str(sum(x.get("status")=="PASS" for x in pyrows))+"/"+str(len(pyrows)))
    print("KA1_CALLER_ROWS="+str(len(ref_rows))+" KA1_ARG_ROWS="+str(len(arg_rows))+" KA2_GLOBAL_WRITERS="+str(len(gw))+" KA3_BE5D8_REFS="+str(len(k3)))
if __name__=="__main__": main()
