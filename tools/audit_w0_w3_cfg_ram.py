#!/usr/bin/env python3
"""Read-only W0-W2 audit: Release timeline, CFG reaching definitions, savestate RAM."""
from __future__ import annotations
import argparse, csv, hashlib, io, json, os, re, struct, urllib.parse, urllib.request, urllib.error, zipfile
from collections import defaultdict, Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO="zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research"
BASE=0x800AD450; SLOT=0x8013A554; LOW=-23212; PTR=0x801CEF08
RAM_BASE=0x80000000; RAM_BYTES=0x200000
REGS=("zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra")
ALL_GPRS=set(REGS)-{"zero"}
VOLATILE=set(("at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","t8","t9","gp"))
ENTRY1_SHA="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
WINDOW_START=datetime.fromisoformat("2026-10-29T00:10:00+00:00")
WINDOW_END=datetime.fromisoformat("2026-10-29T00:16:00+00:00")

def H(v): return f"0x{v:08X}"
def u32(b,o): return struct.unpack_from("<I",b,o)[0]
def sha(b): return hashlib.sha256(b).hexdigest()
def dt(s):
    if not s: return None
    return datetime.fromisoformat(s.replace("Z","+00:00"))
def read_csv(p):
    with Path(p).open(newline="",encoding="utf-8-sig") as f: return list(csv.DictReader(f))
def write_csv(p,rows,fields=None):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    if fields is None: fields=list(rows[0]) if rows else []
    with p.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(rows)

def api(path):
    token=os.environ.get("GITHUB_TOKEN")
    if not token: raise RuntimeError("GITHUB_TOKEN missing")
    url=path if path.startswith("https://") else "https://api.github.com/repos/"+REPO+"/"+path.lstrip("/")
    req=urllib.request.Request(url,headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28","User-Agent":"naruto-static-audit"})
    with urllib.request.urlopen(req,timeout=60) as res: return res.read(),dict(res.headers)

def w0(out,run_id):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    def iso(d): return d.isoformat().replace("+00:00","Z") if d else ""
    relraw,_=api("releases/tags/naruto-checkpoint-39262213468")
    rel=json.loads(relraw)
    assetsraw,_=api(f"releases/{rel['id']}/assets?per_page=100")
    assets=json.loads(assetsraw)
    target=[a for a in assets if a.get("id")==686794219 or a.get("name")=="storymode-checkpoint-run-39262213468.raw.sstate"]
    asset=target[0] if target else {}
    # Query two adjacent UTC dates. A previous-day run can still be active at 00:10.
    runs=[]
    for page in range(1,21):
        q=urllib.parse.urlencode({"created":"2026-10-28..2026-10-29","per_page":100,"page":page})
        raw,_=api("actions/runs?"+q); data=json.loads(raw)
        batch=data.get("workflow_runs",[])
        runs.extend(batch)
        if len(batch)<100: break
    window_runs=[]
    for r in runs:
        created=dt(r.get("created_at")); started=dt(r.get("run_started_at")); completed=dt(r.get("updated_at") if r.get("status")!="completed" else r.get("run_started_at"))
        # For completed runs, use their explicit run-level completed_at when present.
        end=dt(r.get("completed_at")) or (dt(r.get("updated_at")) if r.get("status")=="completed" else None)
        begin=started or created
        intersects=bool(created and created<=WINDOW_END and (end is None or end>=WINDOW_START) and (begin is None or begin<=WINDOW_END))
        if intersects: window_runs.append(r)
    run_rows=[]; job_rows=[]; release_steps=[]; excerpt=[]
    # Retrieve jobs for each run which intersects the interval; also any checkpoint/release-labelled run that day.
    candidate_runs={r["id"]:r for r in window_runs}
    for r in runs:
        created=dt(r.get("created_at"))
        if created and WINDOW_START.replace(hour=0,minute=0) <= created <= WINDOW_END and re.search(r"release|checkpoint|preserv",str(r.get("name","")+" "+r.get("path","")),re.I):
            candidate_runs[r["id"]]=r
    for r in sorted(window_runs,key=lambda x:(x.get("created_at",""),x.get("id",0))):
        run_rows.append({"run_id":r.get("id"),"workflow_name":r.get("name"),"workflow_path":r.get("path"),
          "created_at":r.get("created_at"),"run_started_at":r.get("run_started_at"),"completed_at":r.get("completed_at"),
          "run_attempt":r.get("run_attempt"),"head_sha":r.get("head_sha"),"head_branch":r.get("head_branch"),
          "event":r.get("event"),"status":r.get("status"),"conclusion":r.get("conclusion"),"html_url":r.get("html_url"),
          "intersects_00_10_to_00_16Z":"YES"})
    for r in sorted(candidate_runs.values(),key=lambda x:(x.get("created_at",""),x.get("id",0))):
        try:
            raw,_=api(f"actions/runs/{r['id']}/jobs?per_page=100&filter=latest")
            jobs=json.loads(raw).get("jobs",[])
        except Exception as e:
            job_rows.append({"run_id":r["id"],"job_id":"","job_name":"","error":str(e)})
            continue
        for j in jobs:
            js=dt(j.get("started_at")); je=dt(j.get("completed_at"))
            ja=bool((js is None and r.get("status") in ("queued","in_progress")) or (js and js<=WINDOW_END and (je is None or je>=WINDOW_START)))
            if r["id"] in {x["id"] for x in window_runs} and ja:
                job_rows.append({"run_id":r["id"],"job_id":j.get("id"),"job_name":j.get("name"),
                  "status":j.get("status"),"conclusion":j.get("conclusion"),"started_at":j.get("started_at"),
                  "completed_at":j.get("completed_at"),"run_attempt":j.get("run_attempt"),"head_sha":r.get("head_sha"),
                  "event":r.get("event"),"active_in_window":"YES"})
            steps=j.get("steps") or []
            matched=[s for s in steps if re.search(r"release|asset|upload|publish|preserv",str(s.get("name","")),re.I)]
            for st in matched:
                release_steps.append({"run_id":r["id"],"workflow_name":r.get("name"),"head_sha":r.get("head_sha"),
                  "branch":r.get("head_branch"),"event":r.get("event"),"job_id":j.get("id"),"job_name":j.get("name"),
                  "step_number":st.get("number"),"step_name":st.get("name"),"step_status":st.get("status"),
                  "step_conclusion":st.get("conclusion"),"step_started_at":st.get("started_at"),"step_completed_at":st.get("completed_at"),
                  "start_vs_release_created":"UNKNOWN"})
            # Read logs only for jobs that contain release-related steps, for timestamped API-operation evidence.
            if matched:
                try:
                    data,_=api(f"actions/jobs/{j['id']}/logs")
                    try:
                        z=zipfile.ZipFile(io.BytesIO(data))
                        txt="\n".join(z.read(n).decode("utf-8","replace") for n in z.namelist() if n.endswith(".txt"))
                    except zipfile.BadZipFile:
                        txt=data.decode("utf-8","replace")
                    for line in txt.splitlines():
                        if re.search(r"/releases|release_id=|release_asset_id=|release_url=|upload-result|created_at|http.?404|preserve raw savestate",line,re.I):
                            if len(excerpt)<2000: excerpt.append(f"run={r['id']} job={j['id']} {line[:900]}")
                except Exception as e:
                    excerpt.append(f"run={r['id']} job={j.get('id')} LOG_FETCH_ERROR={str(e)[:200]}")
    # The timestamp comparison can exclude a post-creation workflow as a creator, but cannot prove which external actor created it.
    created=dt(rel.get("created_at"))
    candidates=[]
    for st in release_steps:
        ss=dt(st.get("step_started_at")); se=dt(st.get("step_completed_at"))
        if ss and created and ss<=created and (se is None or se>=created):
            st["start_vs_release_created"]="TIME_OVERLAP_NOT_PROOF"; candidates.append(st)
        elif ss and created and ss>created:
            st["start_vs_release_created"]="STARTED_AFTER_RELEASE_RECORD"
        elif se and created and se<created:
            st["start_vs_release_created"]="FINISHED_BEFORE_RELEASE_RECORD"
        else: st["start_vs_release_created"]="TIME_NOT_ENOUGH"
    write_csv(out/"w0_runs_active_window.csv",run_rows)
    write_csv(out/"w0_jobs_active_window.csv",job_rows)
    write_csv(out/"w0_release_related_steps.csv",release_steps)
    (out/"w0_release_job_log_excerpts.txt").write_text("\n".join(excerpt)+"\n",encoding="utf-8")
    releaselines=[
      "W0 RELEASE CREATOR TIMELINE — UTC; API fields and Actions jobs/steps",
      f"query_window={iso(WINDOW_START)}..{iso(WINDOW_END)}",
      f"runs_fetched_created_2026-10-28_to_2026-10-29={len(runs)}",
      f"runs_intersecting_window={len(window_runs)}",
      f"jobs_active_in_window={len(job_rows)}",
      f"release_related_steps_in_candidate_runs={len(release_steps)}",
      f"release_tag={rel.get('tag_name')}",
      f"release_id={rel.get('id')}",
      f"release_created_at={rel.get('created_at')}",
      f"release_published_at={rel.get('published_at')}",
      f"release_author={((rel.get('author') or {}).get('login','UNKNOWN'))}",
      f"release_asset_id={asset.get('id','UNKNOWN')}",
      f"release_asset_created_at={asset.get('created_at','UNKNOWN')}",
      f"release_asset_updated_at={asset.get('updated_at','UNKNOWN')}",
      f"release_asset_uploader={((asset.get('uploader') or {}).get('login','UNKNOWN'))}",
      f"release_asset_name={asset.get('name','UNKNOWN')}",
      f"release_asset_size_bytes={asset.get('size','UNKNOWN')}",
      f"release_asset_state_sha256_expected=00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d",
      f"release_timestamp_precedes_run_40792708405_start={'YES' if created and dt('2026-10-29T00:14:11Z') and created<dt('2026-10-29T00:14:11Z') else 'NO'}",
      f"release_step_time_overlaps_created_at={len(candidates)}",
      "creator_conclusion=TIDAK TAHU unless an API creation event is uniquely attributable; author=github-actions[bot] identifies the uploader/actor account, not a specific workflow run.",
      "creator_rule=Any candidate step starting after Release.created_at cannot have created that record. A time-overlapping step alone is not proof absent an attributable creation event in the logged/API evidence.",
      f"current_audit_run={run_id}",
    ]
    (out/"w0_release_timeline_summary.txt").write_text("\n".join(releaselines)+"\n",encoding="utf-8")

@dataclass
class Ins:
    pc:int; word:int; op:int; rs:int; rt:int; rd:int; sh:int; fn:int; imm:int
    name:str="unknown"; ctl:str=""; branch:bool=False; likely:bool=False; writes:set=None; target:int|None=None; unknown:bool=False
    def __post_init__(self):
        if self.writes is None: self.writes=set()
def decode(pc,w):
    op=(w>>26)&63; rs=(w>>21)&31; rt=(w>>16)&31; rd=(w>>11)&31; sh=(w>>6)&31; fn=w&63; imm=((w&65535)-65536 if w&32768 else w&65535)
    x=Ins(pc,w,op,rs,rt,rd,sh,fn,imm)
    def wr(n):
        if n: x.writes.add(REGS[n])
    if op==0:
        x.name={0:"sll",2:"srl",3:"sra",4:"sllv",6:"srlv",7:"srav",8:"jr",9:"jalr",12:"syscall",13:"break",15:"sync",16:"mfhi",17:"mthi",18:"mflo",19:"mtlo",24:"mult",25:"multu",26:"div",27:"divu",32:"add",33:"addu",34:"sub",35:"subu",36:"and",37:"or",38:"xor",39:"nor",42:"slt",43:"sltu"}.get(fn,"unknown-special")
        if fn==8: x.ctl="jr"
        elif fn==9: x.ctl="jalr";wr(rd or 31)
        elif fn in (0,2,3,4,6,7,16,18,32,33,34,35,36,37,38,39,42,43): wr(rd)
        elif fn not in (12,13,15,17,19,24,25,26,27): x.unknown=True;x.writes.update(ALL_GPRS)
    elif op in (2,3):
        x.name="j" if op==2 else "jal";x.ctl=x.name;x.target=((pc+4)&0xF0000000)|((w&0x3ffffff)<<2)
        if op==3:wr(31)
    elif op==1 or op in (4,5,6,7,20,21,22,23):
        x.branch=True;x.ctl="branch";x.target=(pc+4+(imm<<2))&0xffffffff
        if op==1:
            x.name={0:"bltz",1:"bgez",2:"bltzl",3:"bgezl",16:"bltzal",17:"bgezal",18:"bltzall",19:"bgezall"}.get(rt,"regimm");x.likely=rt in (2,3,18,19)
            if rt in (16,17,18,19):wr(31)
        else:
            x.name={4:"beq",5:"bne",6:"blez",7:"bgtz",20:"beql",21:"bnel",22:"blezl",23:"bgtzl"}[op];x.likely=op in (20,21,22,23)
    elif op in range(8,16):
        x.name={8:"addi",9:"addiu",10:"slti",11:"sltiu",12:"andi",13:"ori",14:"xori",15:"lui"}[op];wr(rt)
    elif op in (32,33,34,35,36,37,38,39):
        x.name={32:"lb",33:"lh",34:"lwl",35:"lw",36:"lbu",37:"lhu",38:"lwr",39:"lwu"}[op];wr(rt)
    elif op in (40,41,42,43,46):x.name={40:"sb",41:"sh",42:"swl",43:"sw",46:"swr"}[op]
    elif op==48:x.name="ll";wr(rt)
    elif op in (49,50,53,55):x.name={49:"lwc1",50:"lwc2",53:"ldc1",55:"ldc2"}[op]
    elif op in (57,58,61,63):x.name={57:"swc1",58:"swc2",61:"sdc1",63:"sdc2"}[op]
    elif op in (47,51):x.name={47:"cache",51:"pref"}[op]
    elif op in (16,17,18,19):
        x.name={16:"cop0",17:"cop1",18:"cop2",19:"cop3"}[op]
        if rs in (0,2):wr(rt)
        elif rs==8:x.ctl="cop-branch";x.branch=True;x.target=(pc+4+(imm<<2))&0xffffffff
    else:x.name=f"unknown-op-{op:02X}";x.unknown=True;x.writes.update(ALL_GPRS)
    return x

def iline(x):
    return f"{H(x.pc)} {x.word.to_bytes(4,'little').hex(' ').upper()} {x.name} w=0x{x.word:08X}"
def funcs(path):
    out=[]
    for r in read_csv(path):
        try:
            s=int(r["start_address"],16);e=int(r["end_address"],16)
            if s<=e:out.append((s,e,r.get("function_name","")))
        except:pass
    return out
def build_cfg(entry,s,e,name):
    inst={}
    for pc in range(s,e+1,4):
        o=pc-BASE
        if o<0 or o+4>len(entry):continue
        inst[pc]=decode(pc,u32(entry,o))
    pcs=sorted(inst)
    if not pcs:return None
    leaders={pcs[0]}; owners=defaultdict(list);amb=[]
    for pc,x in inst.items():
        if not x.ctl:continue
        if pc+4 in inst:leaders.add(pc+4);owners[pc+4].append(pc)
        if pc+8 in inst:leaders.add(pc+8)
        if x.target is not None and x.target in inst:leaders.add(x.target)
    for d,os_ in owners.items():
        if len(os_)!=1:amb.append(f"delay slot {H(d)} has owners "+",".join(H(v) for v in os_))
        elif inst[d].ctl:amb.append(f"control in delay slot {H(d)} owned by {H(os_[0])}")
        for pc,x in inst.items():
            if x.target==d and pc not in os_:amb.append(f"branch/jump {H(pc)} targets delay slot {H(d)}")
    sl=sorted(leaders); blocks=[]
    for ix,l in enumerate(sl):
        end=sl[ix+1] if ix+1<len(sl) else None
        ps=[p for p in pcs if p>=l and (end is None or p<end)]
        if ps:blocks.append({"id":name+":"+H(l),"start":l,"end":ps[-1],"pcs":ps})
    p2b={p:b["id"] for b in blocks for p in b["pcs"]}
    pred=defaultdict(list);edges=[]
    def edge(src,dst,kind,flow=True,call=None,note=""):
        sb=p2b.get(src,"");db=p2b.get(dst,"") if dst is not None else ""
        ob={"function":name,"source_block":sb,"source_pc":H(src),"edge_type":kind,
            "target_block":db,"target_pc":H(dst) if dst is not None else "",
            "dataflow_edge":"YES" if flow and db else "NO","call_pc":H(call) if call is not None else "","note":note}
        edges.append(ob)
        if flow and db and sb:pred[db].append(ob)
    for pc,x in inst.items():
        if not x.ctl:continue
        if pc+4 in inst:edge(pc,pc+4,"EXECUTE_DELAY_SLOT",True,note="MIPS delay slot executes before transfer")
        else:amb.append(f"{H(pc)} control has no delay slot in Ghidra function bounds")
    for b in blocks:
        last=b["end"];x=inst[last]; os_=owners.get(last,[])
        if os_:
            if len(os_)!=1:continue
            cp=os_[0]; c=inst[cp]
            if c.branch:
                edge(last,c.target,"BRANCH_TAKEN",True,note="target after delay")
                if c.likely:
                    edge(cp,c.after if hasattr(c,"after") else cp+8,"LIKELY_ANNUL_FALLTHROUGH",True,note="branch-likely not taken annuls delay slot")
                else:edge(last,cp+8,"BRANCH_NOT_TAKEN",True,note="fallthrough after delay")
            elif c.ctl=="j":edge(last,c.target,"JUMP_TARGET",True)
            elif c.ctl in ("jal","jalr"):
                edge(cp,c.target,"CALL_TARGET",False,cp,"interprocedural target not same activation")
                edge(last,cp+8,"CALL_RETURN",True,cp,"caller-saved GPRs clobbered on return edge")
            elif c.ctl=="jr":
                edge(last,None,"RETURN" if c.rs==31 else "INDIRECT_EXIT",False,note="transfer after delay")
            else: edge(last,None,"CONTROL_EXIT_UNKNOWN",False)
        elif x.ctl:
            if x.ctl in ("jal","jalr"):edge(last,x.target,"CALL_TARGET",False,last)
        else:
            if last+4 in inst:edge(last,last+4,"SEQUENTIAL",True)
    for b in blocks:
        for pc in b["pcs"]:
            x=inst[pc]
            for r in x.writes:
                if r=="zero":continue
    regs=[r for r in REGS if r!="zero"]
    entryblock=p2b[pcs[0]]
    ins={b["id"]:{r:set() for r in regs} for b in blocks}
    outs={b["id"]:{r:set() for r in regs} for b in blocks}
    def cpystate(st):return {r:set(st[r]) for r in regs}
    def edge_xform(st,e):
        z=cpystate(st)
        if e["edge_type"]=="CALL_RETURN" and e["call_pc"]:
            for r in VOLATILE:z[r]={f"CALL:{e['call_pc']}:{r}"}
        return z
    changed=True;rounds=0
    while changed and rounds<500:
        rounds+=1;changed=False
        for b in blocks:
            ni={r:set() for r in regs}
            if b["id"]==entryblock:
                for r in regs:ni[r].add("ENTRY:"+r)
            for e in pred.get(b["id"],[]):
                z=edge_xform(outs[e["source_block"]],e)
                for r in regs:ni[r].update(z[r])
            if ni!=ins[b["id"]]:ins[b["id"]]=ni;changed=True
            z=cpystate(ni)
            for pc in b["pcs"]:
                for r in inst[pc].writes:
                    if r!="zero":z[r]={f"{H(pc)}:{r}"}
            if z!=outs[b["id"]]:outs[b["id"]]=z;changed=True
    before={}
    for b in blocks:
        z=cpystate(ins[b["id"]])
        for pc in b["pcs"]:
            before[pc]=cpystate(z)
            for r in inst[pc].writes:
                if r!="zero":z[r]={f"{H(pc)}:{r}"}
    # Recursive, path-sensitive-enough constant evaluation over reaching definitions.
    cache={};stack=set();CAP=64
    def values_before(pc,r):
        if r=="zero":return {0},False
        defs=before.get(pc,{}).get(r,set())
        if not defs:return set(),True
        values=set();unknown=False
        for d in defs:
            vv,uu=evaldef(d);values|=vv;unknown=unknown or uu
            if len(values)>CAP:return set(),True
        return values,unknown or not values
    def evaldef(d):
        if d.startswith(("ENTRY:","CALL:")):return set(),True
        if d in cache:return cache[d]
        if d in stack:return set(),True
        try:p,r=d.split(":",1);pc=int(p,16);x=inst[pc]
        except:return set(),True
        stack.add(d);res=calc(pc,r,x);stack.remove(d);cache[d]=res;return res
    def calc(pc,r,x):
        op,rs,rt,rd,fn,sh,imm=x.op,x.rs,x.rt,x.rd,x.fn,x.sh,x.imm
        if x.unknown:return set(),True
        if x.name=="jal" and r=="ra":return {pc+8},False
        if x.name=="jalr" and r in x.writes:return {pc+8},False
        def src(n):return values_before(pc,REGS[n])
        if op==15 and r==REGS[rt]:return {((x.word&65535)<<16)&0xffffffff},False
        if op in (8,9,10,11,12,13,14) and r==REGS[rt]:
            vs,u=src(rs)
            if u or not vs:return set(),True
            out=set()
            for a in vs:
                if op in (8,9):v=a+imm
                elif op==10:v=int((a if a<0x80000000 else a-0x100000000)<imm)
                elif op==11:v=int(a<(imm&0xffffffff))
                elif op==12:v=a&(x.word&65535)
                elif op==13:v=a|(x.word&65535)
                else:v=a^(x.word&65535)
                out.add(v&0xffffffff)
            return (out,False) if len(out)<=CAP else (set(),True)
        if op==0 and r==REGS[rd]:
            if fn in (0,2,3):
                vs,u=src(rt)
                if u or not vs:return set(),True
                return {((a<<sh) if fn==0 else ((a&0xffffffff)>>sh) if fn==2 else ((a if a<0x80000000 else a-0x100000000)>>sh))&0xffffffff for a in vs},False
            fns={32:lambda a,b:a+b,33:lambda a,b:a+b,34:lambda a,b:a-b,35:lambda a,b:a-b,36:lambda a,b:a&b,37:lambda a,b:a|b,38:lambda a,b:a^b,39:lambda a,b:~(a|b),42:lambda a,b:int((a if a<0x80000000 else a-0x100000000)<(b if b<0x80000000 else b-0x100000000)),43:lambda a,b:int(a<b)}
            if fn not in fns:return set(),True
            va,ua=src(rs);vb,ub=src(rt)
            if ua or ub or not va or not vb or len(va)*len(vb)>CAP:return set(),True
            z={fns[fn](a,b)&0xffffffff for a in va for b in vb}
            return (z,False) if len(z)<=CAP else (set(),True)
        return set(),True
    blocks_out=[];reads=[]
    for b in blocks:
        outsedge=[e for e in edges if e["source_block"]==b["id"]]
        own=owners.get(b["start"],[])
        blocks_out.append({"function":name,"block_id":b["id"],"start_pc":H(b["start"]),"end_pc":H(b["end"]),
          "instruction_count":len(b["pcs"]),"instructions":" | ".join(iline(inst[p]) for p in b["pcs"]),
          "delay_slot_owner":H(own[0]) if len(own)==1 else ("AMBIGUOUS" if own else ""),
          "successors":"; ".join(f"{e['edge_type']}->{e['target_block'] or e['target_pc'] or 'EXIT'}" for e in outsedge),
          "cfg_caveat":"; ".join(sorted(set(amb)))})
    for pc in pcs:
        x=inst[pc]
        if x.op!=35 or x.imm!=LOW:continue
        reg=REGS[x.rs];defs=sorted(before[pc].get(reg,set()))
        vals=set();unknown=False;details=[]
        for d in defs:
            v,u=evaldef(d);vals|=v;unknown=unknown or u
            details.append(d+"=>"+(",".join(H(z) for z in sorted(v)) if v else "UNKNOWN"))
        eff={(v+LOW)&0xffffffff for v in vals}
        if amb or not defs or unknown or not vals:cls="UNRESOLVED";reason="Fail-closed: CFG ambiguity or unknown/entry-live reaching definition."
        elif eff=={SLOT}:cls="RESOLVED_SLOT";reason="All reaching definitions resolve to base 0x80140000; base + (-23212) = 0x8013A554."
        elif SLOT not in eff:cls="RESOLVED_OTHER";reason="All reaching definitions are known and none resolves to 0x8013A554."
        else:cls="UNRESOLVED";reason="Reaching definitions disagree about slot versus non-slot address."
        reads.append({"pc":H(pc),"function":name,"base_register":reg,"immediate_signed":LOW,"target_register":REGS[x.rt],
          "reaching_definition_ids":";".join(defs),"reaching_definitions_with_values":"; ".join(details),
          "possible_base_values":";".join(H(v) for v in sorted(vals)),"possible_effective_addresses":";".join(H(v) for v in sorted(eff)),
          "class":cls,"reason":reason,"cfg_ambiguity":"; ".join(sorted(set(amb))),
          "dataflow_rounds":rounds,"dataflow_converged":"YES" if not changed else "NO"})
    return {"blocks":blocks_out,"edges":edges,"reads":reads,"ambiguous":amb,"rounds":rounds,"converged":not changed}
def w1(entry,candidate,function_csv,v3_csv,out):
    fns=funcs(function_csv); v3=read_csv(v3_csv)
    if len(v3)!=32:raise SystemExit(f"V3_ROW_COUNT_NOT_32:{len(v3)}")
    targets=[]
    for row in v3:
        pc=int(row["pc"],16); hits=[f for f in fns if f[0]<=pc<=f[1]]
        if len(hits)!=1:raise SystemExit(f"FUNCTION_BOUNDARY_NOT_UNIQUE:{H(pc)}:{hits}")
        targets.append((pc,row,hits[0]))
    cache={}
    for _,_,f in targets:
        if f[2] not in cache:cache[f[2]]=build_cfg(entry,*f)
    reads=[];blocks=[];edges=[]
    oldmap={0x801073A4:"RESOLVED_SLOT",0x8010749C:"RESOLVED_SLOT",0x80104AE8:"RESOLVED_OTHER",0x801060E8:"RESOLVED_OTHER"}
    for pc,row,f in targets:
        result=cache[f[2]]; hit=[r for r in result["reads"] if int(r["pc"],16)==pc]
        if len(hit)!=1:raise SystemExit(f"CFG_READER_NOT_UNIQUE:{H(pc)}:{len(hit)}")
        rr=dict(hit[0]); old=oldmap.get(pc,"UNRESOLVED")
        rr["previous_v3_classification"]=row.get("classification","")
        rr["previous_conservative_2_2_28_classification"]=old
        rr["previous_vs_cfg"]="UNCHANGED" if old==rr["class"] else "CHANGED"
        rr["change_explanation"]=("No class change from prior conservative grouping." if old==rr["class"] else
          "Reclassified using explicit block predecessors, MIPS delay-slot edges and caller-saved clobbers; see all reaching definitions and path edges. Prior rule marked every cross-control path unresolved.")
        reads.append(rr)
        for b in result["blocks"]:blocks.append(b)
        for e in result["edges"]:edges.append(e)
    scan={}
    for r in read_csv(candidate):
        if r.get("kind","").upper()=="READ" and r.get("effective_address_if_pair","").upper()=="UNRESOLVED":
            scan[int(r["instruction_pc"],16)]=r
    pcs={pc for pc,_,_ in targets}
    if len(scan)!=32 or set(scan)!=pcs:
        raise SystemExit(f"SCAN_V3_JOIN_MISMATCH: scan_unresolved={len(scan)} V3={len(v3)} shared={len(set(scan)&pcs)}")
    joins=[]
    for rr in reads:
        pc=int(rr["pc"],16);sr=scan[pc]
        joins.append({"pc":rr["pc"],"scan_kind":sr.get("kind",""),"scan_mnemonic":sr.get("mnemonic",""),
          "scan_instruction_word":sr.get("instruction_word",""),"scan_effective_address_if_pair":sr.get("effective_address_if_pair",""),
          "scan_reason":"no matching same-register LUI within the scan's 32-instruction-word lookback",
          "v3_prior_class":rr["previous_v3_classification"],"cfg_class":rr["class"],"join_status":"PASS"})
    write_csv(Path(out)/"w1_32_reader_cfg_classification.csv",reads)
    write_csv(Path(out)/"w1_cfg_basic_blocks.csv",blocks)
    write_csv(Path(out)/"w1_cfg_edges.csv",edges)
    write_csv(Path(out)/"w1_scan_unresolved_to_v3_join.csv",joins)
    counts=Counter(r["class"] for r in reads); changed=[r for r in reads if r["previous_vs_cfg"]=="CHANGED"]
    special=[]
    for pc in (0x80104AE8,0x801060E8):
        r=next(x for x in reads if int(x["pc"],16)==pc)
        special.append(f"{r['pc']}: class={r['class']}; definitions={r['reaching_definitions_with_values']}; effective={r['possible_effective_addresses']}; reason={r['reason']}")
    lines=[
      "W1 CFG REACHING-DEFINITION AUDIT; STATIC ONLY; NO EMULATOR",
      f"v3_rows={len(v3)} scan_extended_unresolved_READ_LW_rows={len(scan)}",
      f"v3_pc_set_equals_scan_unresolved_pc_set={'PASS' if set(scan)==pcs else 'FAIL'}",
      f"join_rows={len(joins)} join_all_32_pass={'PASS' if len(joins)==32 else 'FAIL'}",
      f"unique_reader_functions={len(cache)} cfg_reader_total={len(reads)}",
      f"RESOLVED_SLOT={counts.get('RESOLVED_SLOT',0)} RESOLVED_OTHER={counts.get('RESOLVED_OTHER',0)} UNRESOLVED={counts.get('UNRESOLVED',0)}",
      "previous_conservative_counts=RESOLVED_SLOT:2,RESOLVED_OTHER:2,UNRESOLVED:28",
      f"class_changes={len(changed)} changed_pcs="+(",".join(r["pc"] for r in changed) if changed else "NONE"),
      f"max_dataflow_rounds={max(x['dataflow_rounds'] for x in reads)}",
      f"functions_with_cfg_caveat={sum(bool(x and x['ambiguous']) for x in cache.values())}",
      "special_80104AE8="+special[0],"special_801060E8="+special[1],
      "method=Basic-block CFG; targets, branch joins, jump joins, delay-slot blocks, call-return edges; reaching definitions solved to fixed point; known-constant transfer only for supported GPR instructions.",
      "limitation=Static may-path analysis; a syntactic invalid address does not prove that path is taken at runtime. Any function-level delay-slot/CFG ambiguity forces that function's reader rows to UNRESOLVED.",
    ]
    (Path(out)/"w1_cfg_summary.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    (Path(out)/"w1_classification_changes.txt").write_text("\n".join(
      f"{r['pc']}: {r['previous_conservative_2_2_28_classification']} -> {r['class']} | {r['change_explanation']} | reaching={r['reaching_definitions_with_values']} | eff={r['possible_effective_addresses']}" for r in reads)+"\n",encoding="utf-8")

def w2(rampath,out,run_id):
    ram=Path(rampath).read_bytes()
    if len(ram)!=RAM_BYTES:raise SystemExit(f"RAM_SIZE_MISMATCH:{len(ram)}")
    po=PTR-RAM_BASE;so=SLOT-RAM_BASE
    if po<0 or po+2900>len(ram):raise SystemExit("PTR_REGION_OUTSIDE_RAM")
    region=ram[po:po+2900];p=u32(ram,so);rows=[]
    for n in range(4):
        off=0x478+0x58*n;raw=region[off:off+4];val=u32(raw,0)
        rows.append({"field":f"word_at_+0x{off:03X}","n":n,"region_offset":H(off),"virtual_address":H(PTR+off),
          "raw_bytes_le":raw.hex(" ").upper(),"u32_le":H(val),"decimal":val,"predicted_after_init":"0x00000002",
          "match_prediction":"PASS" if val==2 else "MISMATCH"})
    off=0x620;raw=region[off:off+1];val=raw[0]
    rows.append({"field":"byte_at_+0x620","n":"","region_offset":H(off),"virtual_address":H(PTR+off),
      "raw_bytes_le":raw.hex(" ").upper(),"u32_le":H(val),"decimal":val,"predicted_after_init":"0x000000FF",
      "match_prediction":"PASS" if val==255 else "MISMATCH"})
    out=Path(out);write_csv(out/"w2_predicted_vs_checkpoint_values.csv",rows,
      ["field","n","region_offset","virtual_address","raw_bytes_le","u32_le","decimal","predicted_after_init","match_prediction"])
    lines=["W2 DIRECT SAVESTATE RAM PARSE; EMULATOR NOT LAUNCHED",
      "source_checkpoint_run=39262213468",f"audit_run={run_id}",f"ram_prefix_bytes={len(ram)}",
      f"ram_prefix_sha256={sha(ram)}",f"requested_region_address={H(PTR)}",f"requested_region_bytes={len(region)}",
      f"requested_region_end_exclusive={H(PTR+len(region))}",f"requested_region_sha256={sha(region)}",
      f"slot_address={H(SLOT)}",f"slot_raw_bytes_le={ram[so:so+4].hex(' ').upper()}",
      f"slot_actual_u32_le={H(p)}",f"slot_equals_requested_pointer={'YES' if p==PTR else 'NO'}",
      f"predicted_words_match={sum(r['match_prediction']=='PASS' for r in rows[:4])}/4",
      f"predicted_byte_match={'YES' if rows[4]['match_prediction']=='PASS' else 'NO'}",
      "No raw RAM dump or private CSV committed; only derived values, summaries and SHA-256 digests.",
      "Prediction source: function FUN_80104690 writes 2 to pointer+0x478+0x58*n for n=0..3 and byte 0xFF to pointer+0x620; the checkpoint may reflect another lifecycle state."]
    (out/"w2_checkpoint_ram_summary.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    for x in ("entry","candidate","function_csv","v3","ram","out","run_id"):ap.add_argument("--"+x,required=True)
    a=ap.parse_args();entry=Path(a.entry).read_bytes()
    if len(entry)!=596412 or sha(entry)!=ENTRY1_SHA:raise SystemExit("ENTRY1_IDENTITY_MISMATCH")
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"analysis-input-identity.txt").write_text(
      f"entry1_bytes={len(entry)}\nentry1_sha256={sha(entry)}\nentry1_base={H(BASE)}\nsource_v3_commit=b8e8911534a97dcc6fd38319ecd8c4befc14c996\nsource_v3_run=40815320809\n",encoding="utf-8")
    w0(out,a.run_id)
    # Correct the earlier over-attribution: Release.created_at precedes run 407927's start.
    prior=out/"V1-reconciliation.md"
    if prior.exists():
        txt=prior.read_text(encoding="utf-8")
        revised="""## (b) Release creator evidence
          - Release API reports created_at=2026-10-29T00:14:06Z, Release ID 427327611, asset ID 686794219, actor github-actions[bot].
          - Run 40792708405 started at approximately 2026-10-29T00:14:11Z, after the Release record's created_at. That run therefore cannot be proven to have created the Release record.
          - W0 queries all Actions runs/jobs overlapping 00:10–00:16Z and records Release/asset/publish-related step timestamps and relevant log excerpts. With available evidence, creator conclusion is TIDAK TAHU unless a prior job's creation event is uniquely attributable.
          - Release API: https://api.github.com/repos/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tags/naruto-checkpoint-39262213468
          - Release URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/naruto-checkpoint-39262213468"""
        start=txt.find("## (b) Release creator evidence")
        end=txt.find("## (c)",start+1) if start>=0 else -1
        if start>=0 and end>=0:
            txt=txt[:start]+revised+"\n\n"+txt[end:]
        prior.write_text(txt,encoding="utf-8")
    w1(entry,a.candidate,a.function_csv,a.v3,out)
    w2(a.ram,out,a.run_id)
if __name__=="__main__":
    main()
