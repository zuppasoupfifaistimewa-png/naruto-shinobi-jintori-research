#!/usr/bin/env python3
"""UE1: Entry-1-only static scene/caller audit. No binary outputs."""
from __future__ import annotations
import argparse,csv,hashlib,struct
from bisect import bisect_right
from collections import defaultdict,deque
from pathlib import Path

BASE=0x800AD450; OFFSET=0x10BB000; SIZE=596412
SHA="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
SCENE=0x800B50AC; MID=0x800F3658; TARGET=0x800D15A8
FEE=(0x800D2520,0x800D46EC)
RANGES=((0x800B50AC,0x800B54DC,"SCENE_HANDLER"),(0x800F3658,0x800F5DAC,"CREDIT_WRAPPER"))
def hx(x): return f"0x{x:08X}" if x is not None else "TIDAK TAHU"
def u32(data,pc):
    off=pc-BASE
    if off<0 or off+4>len(data): return None
    return struct.unpack_from("<I",data,off)[0]
def fields(w):
    return (w>>26&63,w>>21&31,w>>16&31,w>>11&31,w>>6&31,w&63,w&0xffff)
def prolog(w):
    if w is None:return False
    op,rs,rt,rd,sh,fn,imm=fields(w)
    return op==9 and rs==29 and rt==29 and (imm&0x8000)!=0
def jrra(w):
    if w is None:return False
    op,rs,rt,rd,sh,fn,imm=fields(w)
    return op==0 and rs==31 and rt==0 and rd==0 and sh==0 and fn==8
def direct(w,pc):
    op=w>>26&63
    if op in (2,3):return ("J" if op==2 else "JAL",((pc+4)&0xF0000000)|((w&0x03ffffff)<<2))
    return None
def owner(pc,starts,data,jr):
    i=bisect_right(starts,pc)-1
    if i<0:return None
    st=starts[i]
    j=bisect_right(jr,st-1)
    if j<len(jr) and jr[j]<pc:return None
    return st
def scan_refs(data,starts,jr):
    refs=[]
    words=[u32(data,BASE+i*4) for i in range(len(data)//4)]
    for i,w in enumerate(words):
        if w is None:continue
        pc=BASE+i*4;d=direct(w,pc)
        if d and d[1] in FEE:
            refs.append((d[1],pc,d[0],owner(pc,starts,data,jr)))
        op,rs,rt,rd,sh,fn,imm=fields(w)
        if op==15:
            reg=rt;hi=imm
            for k in range(1,7):
                j=i+k
                if j>=len(words):break
                w2=words[j];o,s,t,dd,ss,ff,ii=fields(w2)
                if o==9 and s==reg and t==reg:
                    dest=((hi<<16)+((ii^0x8000)-0x8000))&0xffffffff
                    if dest in FEE:refs.append((dest,pc,"LUI_ADDIU",owner(pc,starts,data,jr)))
                    break
                if o==13 and s==reg and t==reg:
                    dest=(hi<<16)|ii
                    if dest in FEE:refs.append((dest,pc,"LUI_ORI",owner(pc,starts,data,jr)))
                    break
                if o in (8,9,12,13,14,15) and t==reg:break
        if w in FEE:
            refs.append((w,pc,"DATA_WORD",owner(pc,starts,data,jr)))
    return sorted(set(refs),key=lambda x:(x[0],x[1],x[2]))
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--data",required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
    raw=Path(a.data).read_bytes()
    if OFFSET+SIZE>len(raw):raise SystemExit("UE1_ENTRY1_BOUNDS_FAIL")
    data=raw[OFFSET:OFFSET+SIZE]
    digest=hashlib.sha256(data).hexdigest()
    if digest!=SHA:raise SystemExit("UE1_ENTRY1_SHA256_FAIL")
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    starts=[BASE+i for i in range(0,len(data)-3,4) if prolog(u32(data,BASE+i))]
    jr=[BASE+i for i in range(0,len(data)-3,4) if jrra(u32(data,BASE+i))]
    rows=[]
    for lo,hi,name in RANGES:
        ps=[p for p in starts if lo<=p<=hi]; js=[p for p in jr if lo<=p<=hi]
        for pc in ps:rows.append({"segment":name,"kind":"PROLOG_ADDIU_SP","pc":hx(pc)})
        for pc in js:rows.append({"segment":name,"kind":"JR_RA","pc":hx(pc)})
    def write(path,header,rows):
        with (out/path).open("w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=header,delimiter="\t",extrasaction="ignore",lineterminator="\n");w.writeheader();w.writerows(rows)
    write("UE1_RANGE_PROLOGS_JR.tsv",["segment","kind","pc"],rows)
    to_mid=[]
    for i in range(len(data)//4):
        pc=BASE+i*4;d=direct(u32(data,pc),pc)
        if d and d[1]==MID:to_mid.append({"pc":hx(pc),"kind":d[0],"target":hx(d[1]),"caller_function":hx(owner(pc,starts,data,jr))})
    write("UE1_ALL_JUMP_TO_F3658.tsv",["pc","kind","target","caller_function"],to_mid)
    direct_b=u32(data,0x800B54DC);direct_f=u32(data,0x800F5DAC)
    b=direct(direct_b,0x800B54DC) if direct_b is not None else None
    f=direct(direct_f,0x800F5DAC) if direct_f is not None else None
    chain_ok=(SCENE in starts and MID in starts and b is not None and b[0]=="JAL" and b[1]==MID and
              f is not None and f[0]=="JAL" and f[1]==TARGET)
    # Direct call graph within ENTRY1; reverse graph preserves bounded caller ancestry.
    callers=defaultdict(set);indirect=defaultdict(int)
    for i in range(len(data)//4):
        pc=BASE+i*4;w=u32(data,pc);fn=owner(pc,starts,data,jr)
        if fn is None:continue
        op,rs,rt,rd,sh,fun,imm=fields(w)
        if op==0 and fun==9:indirect[fn]+=1
        d=direct(w,pc)
        if d and d[1] in starts:callers[d[1]].add(fn)
    refs=scan_refs(data,starts,jr); rrows=[]; chain_rows=[]
    for target,pc,kind,fn in refs:
        if fn is None:
            status="TIDAK TAHU_NO_FUNCTION_OWNER";chain="TIDAK TAHU"
        elif fn==SCENE:
            status="SCENE_HANDLER";chain=hx(SCENE)
        else:
            q=deque([(fn,[fn])]);seen={fn};found=None;depth_limited=False
            while q:
                node,path=q.popleft()
                if len(path)>12:depth_limited=True;continue
                for parent in sorted(callers.get(node,set())):
                    if parent==SCENE:found=[SCENE]+path;break
                    if parent not in seen:seen.add(parent);q.append((parent,[parent]+path))
                if found:break
            if found:
                status="REACHED_SCENE_HANDLER_BOUNDED";chain=" -> ".join(hx(x) for x in found)
            elif indirect.get(fn,0):
                status="TIDAK TAHU_DYNAMIC_CALLER";chain="TIDAK TAHU"
            elif depth_limited:
                status="TIDAK TAHU_DEPTH_LIMIT";chain="TIDAK TAHU"
            else:
                status="NOT_SEEN_TO_SCENE_HANDLER_IN_ENTRY1_GRAPH";chain=hx(fn)
        rrows.append({"target":hx(target),"image":"ENTRY1","reference_pc":hx(pc),"kind":kind,
                      "containing_function":hx(fn),"caller_chain_status":status,"caller_chain":chain})
        if fn is not None:
            chain_rows.append({"target":hx(target),"reference_pc":hx(pc),"owner_function":hx(fn),
                               "status":status,"caller_chain":chain,"indirect_call_count_in_owner":indirect.get(fn,0)})
    write("UE1_FEE_REFERENCES.tsv",["target","image","reference_pc","kind","containing_function","caller_chain_status","caller_chain"],rrows)
    write("UE1_FEE_CALLER_CHAINS.tsv",["target","reference_pc","owner_function","status","caller_chain","indirect_call_count_in_owner"],chain_rows)
    chain=[
      {"step":1,"source":hx(SCENE),"instruction_pc":hx(0x800B54DC),"instruction_kind":b[0] if b else "TIDAK TAHU","target":hx(b[1]) if b else "TIDAK TAHU","status":"PASS" if b and b[1]==MID and b[0]=="JAL" else "FAIL"},
      {"step":2,"source":hx(MID),"instruction_pc":hx(0x800F5DAC),"instruction_kind":f[0] if f else "TIDAK TAHU","target":hx(f[1]) if f else "TIDAK TAHU","status":"PASS" if f and f[1]==TARGET and f[0]=="JAL" else "FAIL"}
    ]
    write("UE1_CHAIN.tsv",["step","source","instruction_pc","instruction_kind","target","status"],chain)
    summary=["UE1_ENTRY1_ONLY_STATIC_SCENE_AUDIT",f"ENTRY1_SHA256={digest}",f"ENTRY1_SIZE={len(data)}",
      f"ENTRY1_BASE={hx(BASE)}",f"CHAIN_SCENE_PROLOG={str(SCENE in starts).upper()}",
      f"CHAIN_WRAPPER_PROLOG={str(MID in starts).upper()}",
      f"JAL_800B54DC_TO_800F3658={'PASS' if b and b[0]=='JAL' and b[1]==MID else 'FAIL'}",
      f"JAL_800F5DAC_TO_800D15A8={'PASS' if f and f[0]=='JAL' and f[1]==TARGET else 'FAIL'}",
      f"CHAIN_STATUS={'PASS' if chain_ok else 'FAIL'}",
      f"RANGE_800B50AC_800B54DC_PROLOGS={sum(1 for x in rows if x['segment']=='SCENE_HANDLER' and x['kind']=='PROLOG_ADDIU_SP')}",
      f"RANGE_800B50AC_800B54DC_JR_RA={sum(1 for x in rows if x['segment']=='SCENE_HANDLER' and x['kind']=='JR_RA')}",
      f"RANGE_800F3658_800F5DAC_PROLOGS={sum(1 for x in rows if x['segment']=='CREDIT_WRAPPER' and x['kind']=='PROLOG_ADDIU_SP')}",
      f"RANGE_800F3658_800F5DAC_JR_RA={sum(1 for x in rows if x['segment']=='CREDIT_WRAPPER' and x['kind']=='JR_RA')}",
      f"ALL_ENTRY1_JAL_OR_J_TO_800F3658={len(to_mid)}",
      f"ENTRY1_FEE_0x800D2520_REFERENCES={sum(1 for x in refs if x[0]==FEE[0])}",
      f"ENTRY1_FEE_0x800D46EC_REFERENCES={sum(1 for x in refs if x[0]==FEE[1])}",
      f"ENTRY1_FEE_REFERENCES_WITH_FUNCTION_OWNER={sum(1 for x in refs if x[3] is not None)}",
      f"ENTRY1_SCENE_HANDLER_DIRECT_CALLER_FUNCTIONS={len(callers.get(SCENE,set()))}",
      "SCOPE=ENTRY1_ONLY; EXE and ENTRY0 are not scanned", "OUTPUT=addresses/metrics only; no bytes excerpt"]
    (out/"UE1_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary))
    return 0 if chain_ok else 2
if __name__=="__main__":raise SystemExit(main())
