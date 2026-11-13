#!/usr/bin/env python3
"""UQ0 CFG supplement: MIPS delay-slot-aware reaching definitions for caller a0."""
from __future__ import annotations
import argparse, csv, hashlib
from pathlib import Path
import RunUQ0 as UQ

LIMIT=20000
COND={"beq","bne","blez","bgtz","bltz","bgez","bltzal","bgezal","regimm"}
FIELDS=["region","call_pc","target_pc","definition_pc","file_offset","instruction","definition_class",
        "source_registers","cfg_nodes_visited","unresolved_incoming_path","walk_truncated","notes"]

def make_cfg(ins,base):
    n=len(ins); succ=[set() for _ in ins]; post={}; notes=[]
    for i,d in enumerate(ins):
        mn=d["mn"]; pc=base+4*i
        if mn in COND:
            after=set(); t=d.get("target")
            if t is not None:
                q=(int(t)-base)//4
                if 0<=q<n and base+4*q==int(t): after.add(q)
                else: notes.append(f"EXTERNAL_BRANCH:0x{pc:08X}")
            if i+2<n: after.add(i+2)
            if i+1<n: succ[i].add(i+1); post.setdefault(i+1,set()).update(after)
            else: notes.append(f"MISSING_DELAY:0x{pc:08X}")
        elif mn in ("j","jal","jalr","jr"):
            after=set()
            if mn=="j":
                t=d.get("target")
                if t is not None:
                    q=(int(t)-base)//4
                    if 0<=q<n and base+4*q==int(t): after.add(q)
                    else: notes.append(f"EXTERNAL_JUMP:0x{pc:08X}")
            elif mn in ("jal","jalr") and i+2<n: after.add(i+2)
            if i+1<n: succ[i].add(i+1); post.setdefault(i+1,set()).update(after)
            else: notes.append(f"MISSING_DELAY:0x{pc:08X}")
        elif d.get("op") in (20,21,22,23):
            notes.append(f"BRANCH_LIKELY_DELAY_UNMODELED:0x{pc:08X}")
            after=set(); t=(pc+4+(d.get("simm",0)<<2))&0xffffffff; q=(t-base)//4
            if 0<=q<n and base+4*q==t: after.add(q)
            if i+2<n: after.add(i+2)
            if i+1<n: succ[i].add(i+1); post.setdefault(i+1,set()).update(after)
        elif d.get("control"):
            notes.append(f"UNCLASSIFIED_CONTROL:0x{pc:08X}:{mn}")
            if i+1<n: succ[i].add(i+1); post.setdefault(i+1,set()).update({i+2} if i+2<n else set())
        elif i+1<n: succ[i].add(i+1)
    for i,after in post.items(): succ[i]=set(after)
    pred=[set() for _ in ins]
    for i,targets in enumerate(succ):
        for j in targets:
            if 0<=j<n: pred[j].add(i)
    return pred,notes

def reach(ins,pred,call):
    # Include the JAL delay slot itself: its writes are visible to the callee.
    stack=[call+1] if call+1<len(ins) else []
    seen=set(); defs=set(); unknown=False; cut=False
    while stack:
        i=stack.pop()
        if i in seen: continue
        if len(seen)>=LIMIT: cut=True; break
        seen.add(i)
        if ins[i].get("writes")==4: defs.add(i); continue
        if not pred[i]: unknown=True
        else: stack.extend(sorted(pred[i],reverse=True))
    return sorted(defs),unknown,cut,len(seen)

def classify(d):
    src=",".join("$"+UQ.REGS[x] for x in sorted(d.get("reads",set()))) or "NONE"
    mn=d["mn"]
    if mn=="lui": k="CONSTANT_HIGH_HALF"
    elif mn in ("addiu","addi") and d.get("rs")==0: k="CONSTANT_IMMEDIATE"
    elif mn in ("addu","or") and 0 in (d.get("rs"),d.get("rt")): k="REGISTER_COPY"
    elif mn in ("lw","lh","lhu","lb","lbu"): k="MEMORY_LOAD_SOURCE_UNRESOLVED"
    else: k="REGISTER_DERIVED_OR_UNKNOWN"
    return k,src

def self_test():
    b=0x80010000
    enc_i=lambda op,rs,rt,imm: ((op<<26)|(rs<<21)|(rt<<16)|(imm&0xffff)).to_bytes(4,"little")
    enc_j=lambda op,target: ((op<<26)|((target>>2)&0x03ffffff)).to_bytes(4,"little")
    words=[enc_i(4,0,0,4),b"\0"*4,enc_i(9,0,4,1),enc_j(2,b+32),b"\0"*4,
           enc_i(9,0,4,2),enc_j(2,b+32),b"\0"*4,b"\0"*4,
           enc_j(3,0x800B770C),b"\0"*4,b"\0"*4]
    ins=[UQ.dec(x,b+4*i) for i,x in enumerate(words)]
    pred,notes=make_cfg(ins,b); ds,u,t,_=reach(ins,pred,9)
    assert ds==[2,5] and not u and not t,(ds,u,t,notes)
    print("UQ0CFG_SELF_TEST=PASS")

def analyze(exe,data,out):
    if len(exe)!=UQ.EXE_SIZE or hashlib.sha256(exe).hexdigest()!=UQ.EXE_SHA: raise SystemExit("EXE_SHA_MISMATCH")
    if len(data)!=UQ.DATA_SIZE or hashlib.sha256(data).hexdigest()!=UQ.DATA_SHA: raise SystemExit("DATA_SHA_MISMATCH")
    e1=data[UQ.ENTRY1_IN_DATA:UQ.ENTRY1_IN_DATA+UQ.E1_SIZE]
    if len(e1)!=UQ.E1_SIZE or hashlib.sha256(e1).hexdigest()!=UQ.ENTRY1_SHA: raise SystemExit("ENTRY1_SHA_MISMATCH")
    regions=[]
    for name,base,blob,off in (("EXE",UQ.EXE_BASE,exe[UQ.EXE_OFF:],UQ.EXE_OFF),("ENTRY1",UQ.E1_BASE,e1,UQ.E1_OFF)):
        ins=[UQ.dec(blob[p:p+4],base+p) for p in range(0,len(blob)-3,4)]
        pred,notes=make_cfg(ins,base); regions.append((name,base,off,ins,pred,notes))
    rows=[]; calls=multi=unknown_calls=no_defs=cut_calls=note_count=0
    for name,base,off,ins,pred,notes in regions:
        note_count+=len(notes)
        for i,d in enumerate(ins):
            if d["mn"]!="jal" or d.get("target") not in UQ.TARGETS: continue
            calls+=1; defs,unknown,cut,visited=reach(ins,pred,i)
            multi+=len(defs)>1; unknown_calls+=unknown; no_defs+=not defs; cut_calls+=cut
            for q in defs:
                k,src=classify(ins[q]); pc=base+4*q
                rows.append(dict(region=name,call_pc=f"0x{base+4*i:08X}",target_pc=f"0x{int(d['target']):08X}",
                    definition_pc=f"0x{pc:08X}",file_offset=f"0x{pc-base+off:08X}",instruction=ins[q]["text"],
                    definition_class=k,source_registers=src,cfg_nodes_visited=visited,
                    unresolved_incoming_path="YES" if unknown else "NO",walk_truncated="YES" if cut else "NO",
                    notes="CFG_REACHABLE; delay-slot aware; source register ancestry not recursively resolved"))
            if unknown or cut or not defs:
                rows.append(dict(region=name,call_pc=f"0x{base+4*i:08X}",target_pc=f"0x{int(d['target']):08X}",
                    definition_pc="TIDAK TAHU",file_offset="TIDAK TAHU",instruction="INCOMING_OR_UNRESOLVED_PATH",
                    definition_class="TIDAK TAHU",source_registers="TIDAK TAHU",cfg_nodes_visited=visited,
                    unresolved_incoming_path="YES",walk_truncated="YES" if cut else "NO",
                    notes="At least one predecessor path has no proven reaching definition"))
    out.mkdir(parents=True,exist_ok=True)
    with (out/"UQ0_CFG_CALLER_A0.tsv").open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=FIELDS,delimiter="\t",extrasaction="ignore",lineterminator="\n"); wr.writeheader(); wr.writerows(rows)
    status="TUNTAS" if calls==45 and unknown_calls==0 and no_defs==0 and cut_calls==0 and note_count==0 else "SEBAGIAN"
    lines=["UQ0_CFG_A0_DELAY_SLOT_AWARE_REACHING_DEFINITION_SUPPLEMENT",f"STATUS={status}",
      "EVIDENCE=K4 static EXE/Entry1 bytes; CFG model, not runtime evidence",f"EXE_SHA256={UQ.EXE_SHA}",
      f"DATA_BIN_SHA256={UQ.DATA_SHA}",f"ENTRY1_SHA256={UQ.ENTRY1_SHA}",f"DIRECT_CALLS_AUDITED={calls}",
      f"CALLS_WITH_MULTIPLE_REACHING_A0_DEFS={multi}",f"CALLS_WITH_UNRESOLVED_INCOMING_PATH={unknown_calls}",
      f"CALLS_WITH_NO_A0_DEFINITION={no_defs}",f"CALLS_WITH_TRUNCATED_WALK={cut_calls}",f"DEFINITION_ROWS={len(rows)}",
      f"CONTROL_FLOW_MODEL_NOTES={note_count}","DELAY_SLOT_SEMANTICS=control -> delay slot -> target/fallthrough/return",
      "BRANCHES=both conditional outcomes; branch-likely semantics explicitly noted as incomplete",
      "PROVENANCE_LIMIT=register sources shown but full ancestry/interprocedural values remain TIDAK TAHU",
      "GAMEPLAY_MEANING=TIDAK TAHU"]
    (out/"UQ0_CFG_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines),flush=True)
    return 0

def main():
    p=argparse.ArgumentParser(); p.add_argument("--exe",type=Path); p.add_argument("--data-bin",type=Path)
    p.add_argument("--out-dir",type=Path); p.add_argument("--self-test",action="store_true"); a=p.parse_args()
    if a.self_test: self_test(); return 0
    if not a.exe or not a.data_bin or not a.out_dir: p.error("--exe --data-bin --out-dir required")
    return analyze(a.exe.read_bytes(),a.data_bin.read_bytes(),a.out_dir)

if __name__=="__main__": raise SystemExit(main())
