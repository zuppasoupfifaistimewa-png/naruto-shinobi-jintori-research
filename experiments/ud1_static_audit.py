#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,re,struct,subprocess
from collections import defaultdict,deque
from pathlib import Path

EXE_BASE,EXE_OFF,EXE_SIZE=0x80010000,0x800,385024
E0_BASE,E0_OFF,E0_SIZE=0x800AD000,0x5F800,110536
E1_BASE,E1_OFF,E1_SIZE=0x800AD450,0x10BB000,596412
EXE_SHA="a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
DATA_SHA="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
E0_SHA="56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4"
E1_SHA="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
TABLE,STRIDE=0x800558A8,0x1C
WRAPPER=0x800F5DAC
FIXED=(0x800F5DAC,0x800D2520,0x800D46EC)
STOP_FIXED={0x800B50AC,0x8011CE2C}
def hx(v):return f"0x{v:08X}" if v is not None else "TIDAK TAHU"
def u32(data,base,pc,fo=0):
    off=pc-base+fo
    if off<0 or off+4>len(data):return None
    return struct.unpack_from("<I",data,off)[0]
def signed16(v):return v-0x10000 if v&0x8000 else v
def image_for_pc(images,pc):
    return [im for im in images if im["base"]<=pc<im["base"]+len(im["data"])]
def fn_index(im):
    data=im["data"];base=im["base"];starts={}
    for off in range(0,len(data)-3,4):
        w=struct.unpack_from("<I",data,off)[0];op=(w>>26)&63;rs=(w>>21)&31;rt=(w>>16)&31;fn=w&63;imm=w&0xffff
        pc=base+off
        if op==9 and rs==29 and rt==29 and signed16(imm)<0:
            starts[pc]="PROLOG_ADDUI_SP"
        if op==0 and rs==31 and fn==8 and pc+8<base+len(data):
            starts.setdefault(pc+8,"AFTER_JR_RA_DELAY_SLOT")
    ordered=sorted(starts)
    return starts,ordered
def containing_fn(im,pc):
    starts,ordered=im["fn"]
    import bisect
    i=bisect.bisect_right(ordered,pc)-1
    if i<0:return None,None
    st=ordered[i]
    if pc-st>0x10000:return None,None
    return st,starts[st]
def map_function(images,pc):
    c=[]
    for im in image_for_pc(images,pc):
        st,kind=containing_fn(im,pc)
        if st is not None:c.append((im["name"],st,kind))
    return c
def parse_pair_value(w1,w2):
    op=(w1>>26)&63;reg=(w1>>16)&31;hi=w1&0xffff
    op2=(w2>>26)&63;rs=(w2>>21)&31;rt=(w2>>16)&31;lo=w2&0xffff
    if op!=15 or rs!=reg or rt!=reg or op2 not in (9,13):return None
    return (((hi<<16)+signed16(lo))&0xffffffff) if op2==9 else (((hi<<16)|lo)&0xffffffff)
def scan_code_refs(images):
    refs=defaultdict(list)
    for im in images:
        data=im["data"];base=im["base"];name=im["name"]
        words=[struct.unpack_from("<I",data,i)[0] for i in range(0,len(data)-3,4)]
        for idx,w in enumerate(words):
            pc=base+idx*4;op=(w>>26)&63
            if op==3:
                target=((pc+4)&0xF0000000)|((w&0x03ffffff)<<2)
                refs[target].append({"image":name,"call_pc":pc,"kind":"JAL","pair_pc2":None})
            if op==15:
                reg=(w>>16)&31
                for k in range(1,7):
                    if idx+k>=len(words):break
                    w2=words[idx+k];op2=(w2>>26)&63;rs=(w2>>21)&31;rt=(w2>>16)&31
                    if op2 in (9,13) and rs==reg and rt==reg:
                        target=parse_pair_value(w,w2)
                        if target is not None:
                            refs[target].append({"image":name,"call_pc":pc,"kind":"LUI_ADDIU" if op2==9 else "LUI_ORI","pair_pc2":pc+k*4})
                        break
                    if op2 in (8,9,12,13,14,15) and rt==reg:break
    for k in refs:refs[k].sort(key=lambda r:(r["image"],r["call_pc"],r["kind"]))
    return refs
def read_data_refs(images,targets):
    out=defaultdict(list); wanted=set(targets)
    for im in images:
        data=im["data"]
        for off in range(0,len(data)-3,4):
            w=struct.unpack_from("<I",data,off)[0]
            if w in wanted:
                out[w].append({"image":im["name"],"call_pc":im["base"]+off,"kind":"DATA_WORD","pair_pc2":None})
    return out
def table_fields(exe):
    rows=[]
    for i in range(8):
        rb=TABLE+STRIDE*i
        for field in (4,12):
            v=u32(exe,EXE_BASE,rb+field,EXE_OFF)
            rows.append({"entry":i,"record_base":hx(rb),"field_offset":f"+0x{field:02X}","field_address":hx(rb+field),"value":hx(v),"raw":v})
    return rows
def tracked(root):
    b=subprocess.check_output(["git","-C",str(root),"ls-files","-z","--","*.tsv"])
    return [x for x in b.decode("utf-8","replace").split("\0") if x]
def byte_parse(s):
    p=(s or "").strip().split()
    try:
        if len(p)==1 and len(p[0])>2 and len(p[0])%2==0:p=[p[0][i:i+2] for i in range(0,len(p[0]),2)]
        if not p or any(len(x)!=2 for x in p):return None
        return bytes(int(x,16) for x in p)
    except Exception:return None
def validate_bytes_tsv(root,files,wanted):
    seen=defaultdict(set)
    for rel in files:
        try:
            with (root/rel).open("r",encoding="utf-8-sig",newline="") as f:
                rd=csv.DictReader(f,delimiter="\t")
                if not rd.fieldnames:continue
                hm={re.sub(r"\s+","_",x.strip().lower()):x for x in rd.fieldnames if x}
                pc_col=hm.get("pc") or hm.get("instruction_pc");by_col=hm.get("bytes") or hm.get("instruction_bytes")
                if not pc_col or not by_col:continue
                for row in rd:
                    try:pc=int((row.get(pc_col) or "").strip(),16)
                    except Exception:continue
                    if pc not in wanted:continue
                    b=byte_parse(row.get(by_col,""))
                    if b:seen[pc].add(b[:4])
        except Exception:continue
    result={}
    for pc,expected in wanted.items():
        got=seen.get(pc,set())
        result[pc]="MATCH" if expected.intersection(got) else ("CONFLICT" if got else "NO_TSV_ROW")
    return result
def tsv_rows(path):
    try:
        with path.open("r",encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f,delimiter="\t"))
    except Exception:return []
def compare_dx1_la2(root):
    dx=sorted(root.rglob("DX1_ALL_PLUS1A_ACCESS.tsv"))
    la=sorted(root.rglob("LA2_GLOBAL_INPUT_ACCESSES.tsv"))
    def latest(paths):
        def key(p):
            nums=re.findall(r"\d+",str(p))
            return (int(nums[-1]) if nums else -1,str(p))
        return max(paths,key=key) if paths else None
    dp,lp=latest(dx),latest(la)
    if not dp or not lp:return ["DX1_FILE="+(str(dp.relative_to(root)) if dp else "TIDAK TAHU"),"LA2_FILE="+(str(lp.relative_to(root)) if lp else "TIDAK TAHU"),"DX1_LA2_COMPARISON=TIDAK TAHU_missing_file"]
    dr=tsv_rows(dp);lr=tsv_rows(lp)
    def col(row,*names):
        low={k.strip().lower():v for k,v in row.items() if k}
        for n in names:
            if n in low:return low[n]
        return ""
    dxrows=[];larows=[]
    for r in dr:
        region=col(r,"region","image").strip().upper()
        try:pc=int(col(r,"pc"),16)
        except Exception:continue
        if region=="EXE":
            sig=(col(r,"bytes"),col(r,"instruction","instruksi").strip().lower())
            dxrows.append((pc,sig))
    for r in lr:
        image=col(r,"image","region").strip().upper()
        try:pc=int(col(r,"pc"),16)
        except Exception:continue
        if image=="EXE":
            sig=(col(r,"bytes"),col(r,"instruction","instruksi").strip().lower())
            larows.append((pc,sig))
    bysig=defaultdict(set)
    for pc,sig in larows:bysig[sig].add(pc)
    direct=plus=minus=0
    for pc,sig in dxrows:
        pset=bysig.get(sig,set())
        if pc in pset:direct+=1
        if pc+0x800 in pset:plus+=1
        if pc-0x800 in pset:minus+=1
    return [
      "DX1_FILE="+str(dp.relative_to(root)),
      "LA2_FILE="+str(lp.relative_to(root)),
      f"DX1_EXE_ROWS={len(dxrows)}",
      f"LA2_EXE_ROWS={len(larows)}",
      f"SAME_SIGNATURE_DIRECT_PC_MATCHES={direct}",
      f"DX1_PC_PLUS_0x800_MATCHES_LA2={plus}",
      f"DX1_PC_MINUS_0x800_MATCHES_LA2={minus}",
      "DX1_SOURCE_MODIFIED=NO",
      "INTERPRETATION="+("TIDAK TAHU_no_comparable_EXE_rows" if not larows else "counts are exact signature+PC comparisons; offsets are hypotheses, not remapped facts"),
    ]
def write_tsv(path,fields,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n");w.writeheader()
        for row in rows:w.writerow({k:row.get(k,"TIDAK TAHU") for k in fields})
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",required=True);ap.add_argument("--exe",required=True);ap.add_argument("--data",required=True);ap.add_argument("--out",required=True)
    a=ap.parse_args();root=Path(a.root).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    exe=Path(a.exe).read_bytes();data=Path(a.data).read_bytes()
    if len(exe)!=EXE_SIZE or hashlib.sha256(exe).hexdigest()!=EXE_SHA:raise SystemExit("UD1_EXE_IDENTITY_FAIL")
    if len(data)!=66015232 or hashlib.sha256(data).hexdigest()!=DATA_SHA:raise SystemExit("UD1_DATA_BIN_IDENTITY_FAIL")
    e0=data[E0_OFF:E0_OFF+E0_SIZE];e1=data[E1_OFF:E1_OFF+E1_SIZE]
    if hashlib.sha256(e0).hexdigest()!=E0_SHA or hashlib.sha256(e1).hexdigest()!=E1_SHA:raise SystemExit("UD1_ENTRY_IDENTITY_FAIL")
    images=[{"name":"EXE","base":EXE_BASE,"data":exe},{"name":"ENTRY0","base":E0_BASE,"data":e0},{"name":"ENTRY1","base":E1_BASE,"data":e1}]
    for im in images:im["fn"]=fn_index(im)
    fields=table_fields(exe)
    stops=set(STOP_FIXED)|{r["raw"] for r in fields if r["raw"] not in (None,0)}
    code=scan_code_refs(images)
    fixed_data=read_data_refs(images,set(FIXED)|stops)
    # Function status for every +04/+0C table field.
    scene=[]
    for r in fields:
        raw=r["raw"];maps=image_for_pc(images,raw) if raw is not None else []
        funcs=map_function(images,raw) if maps else []
        starts=[x for x in funcs if x[1]==raw]
        scene.append({**{k:v for k,v in r.items() if k!="raw"},
          "candidate_images":";".join(im["name"] for im in maps) if maps else "TIDAK TAHU",
          "function_start":"YES" if starts else ("INSIDE_FUNCTION" if funcs else "TIDAK TAHU_NOT_FUNCTION"),
          "boundary_methods":";".join(f"{n}:{kind}" for n,_,kind in starts) if starts else "TIDAK TAHU"})
    # Reverse graph from wrapper routine, depth <= 6.
    wf=map_function(images,WRAPPER)
    wrapper_start=wf[0][1] if wf else WRAPPER
    wrapper_method=wf[0][2] if wf else "TIDAK TAHU_NO_BOUNDARY"
    queue=deque([(wrapper_start,0)])
    if wrapper_start!=WRAPPER:queue.append((WRAPPER,0))
    seen={(wrapper_start,0),(WRAPPER,0)};chains=[];reached=set()
    while queue:
        callee,depth=queue.popleft()
        if depth>=6:continue
        for r in code.get(callee,[]):
            funcs=map_function(images,r["call_pc"])
            fn=funcs[0][1] if funcs else None
            fimg=funcs[0][0] if funcs else "TIDAK TAHU"
            fkind=funcs[0][2] if funcs else "TIDAK TAHU_NO_BOUNDARY"
            stop="YES" if fn in stops else "NO"
            chains.append({"depth":depth+1,"callee_function":hx(callee),"image":r["image"],"call_pc":hx(r["call_pc"]),
              "caller_function":hx(fn),"caller_image":fimg,"caller_boundary":fkind,"kind":r["kind"],
              "stop_reached":stop,"stop_reason":"SCENE_TABLE_OR_KNOWN_HANDLER" if stop=="YES" else "CONTINUE"})
            if stop=="YES":reached.add(fn);continue
            if fn is not None and depth+1<6 and (fn,depth+1) not in seen:
                seen.add((fn,depth+1));queue.append((fn,depth+1))
    # Full reference inventory for the three requested targets, including raw data words.
    xrows=[]
    for target in FIXED:
        for r in code.get(target,[]):
            funcs=map_function(images,r["call_pc"]);fn=funcs[0][1] if funcs else None
            xrows.append({"target":hx(target),"image":r["image"],"reference_pc":hx(r["call_pc"]),"kind":r["kind"],
              "containing_function":hx(fn),"function_boundary":funcs[0][2] if funcs else "TIDAK TAHU"})
        for r in fixed_data.get(target,[]):
            funcs=map_function(images,r["call_pc"]);fn=funcs[0][1] if funcs else None
            xrows.append({"target":hx(target),"image":r["image"],"reference_pc":hx(r["call_pc"]),"kind":"DATA_WORD",
              "containing_function":hx(fn),"function_boundary":funcs[0][2] if funcs else "DATA_OR_TIDAK_TAHU"})
    # Validation: code instruction bytes are compared with all tracked byte-bearing TSV rows at the PC.
    edge_refs={}
    for target in set(FIXED)|{int(x["callee_function"],16) for x in chains if x["callee_function"].startswith("0x")}:
        for r in code.get(target,[]):
            pc=r["call_pc"]
            ims=[im for im in images if im["name"]==r["image"] and im["base"]<=pc<im["base"]+len(im["data"])]
            if ims:
                off=pc-ims[0]["base"];edge_refs.setdefault(pc,set()).add(ims[0]["data"][off:off+4])
    for r in chains:
        try:target=int(r["callee_function"],16)
        except Exception:continue
        for ref in code.get(target,[]):
            pc=ref["call_pc"];ims=[im for im in images if im["name"]==ref["image"] and im["base"]<=pc<im["base"]+len(im["data"])]
            if ims:
                off=pc-ims[0]["base"];edge_refs.setdefault(pc,set()).add(ims[0]["data"][off:off+4])
    validation=validate_bytes_tsv(root,tracked(root),edge_refs)
    vrows=[{"pc":hx(pc),"validation":validation.get(pc,"TIDAK TAHU")} for pc in sorted(edge_refs)]
    known_call=any(int(r["reference_pc"],16)==0x800D15A8 and r["target"]==hx(WRAPPER) and r["kind"]=="JAL" for r in xrows)
    write_tsv(out/"UD1_CALLER_CHAINS.tsv",["depth","callee_function","image","call_pc","caller_function","caller_image","caller_boundary","kind","stop_reached","stop_reason"],chains)
    write_tsv(out/"UD1_TARGET_XREFS.tsv",["target","image","reference_pc","kind","containing_function","function_boundary"],xrows)
    write_tsv(out/"UD1_SCENE_FIELD_FUNCTIONS.tsv",["entry","record_base","field_offset","field_address","value","candidate_images","function_start","boundary_methods"],scene)
    write_tsv(out/"UD1_EDGE_BYTE_VALIDATION.tsv",["pc","validation"],vrows)
    dxlines=compare_dx1_la2(root)
    (out/"UD1_DX1_LA2_COMPARISON.txt").write_text("\n".join(dxlines)+"\n",encoding="utf-8")
    levels={d:sum(1 for x in chains if x["depth"]==d) for d in range(1,7)}
    lines=[
      "UD1_STATIC_REVERSE_CALLER_AUDIT",
      f"WRAPPER_TARGET={hx(WRAPPER)}",
      f"WRAPPER_FUNCTION_START={hx(wrapper_start)}",
      f"WRAPPER_BOUNDARY_METHOD={wrapper_method}",
      f"KNOWN_CALLSITE_0x800D15A8_JAL_TO_WRAPPER={'FOUND' if known_call else 'TIDAK TAHU'}",
      f"CALLER_EDGES_DEPTH_1={levels[1]}",
      f"CALLER_EDGES_DEPTH_2={levels[2]}",
      f"CALLER_EDGES_DEPTH_3={levels[3]}",
      f"CALLER_EDGES_DEPTH_4={levels[4]}",
      f"CALLER_EDGES_DEPTH_5={levels[5]}",
      f"CALLER_EDGES_DEPTH_6={levels[6]}",
      f"STOP_ROOTS_REACHED={len(reached)}",
      "STOP_ROOT_VALUES="+",".join(hx(x) for x in sorted(stops)),
      f"FEE_0x800D2520_XREFS={sum(1 for r in xrows if r['target']==hx(0x800D2520))}",
      f"FEE_0x800D46EC_XREFS={sum(1 for r in xrows if r['target']==hx(0x800D46EC))}",
      f"SCENE_PLUS04_PLUS0C_FIELDS={len(scene)}",
      f"SCENE_FIELDS_FUNCTION_START={sum(1 for r in scene if r['function_start']=='YES')}",
      f"SCENE_FIELDS_INSIDE_FUNCTION={sum(1 for r in scene if r['function_start']=='INSIDE_FUNCTION')}",
      f"SCENE_FIELDS_TIDAK_TAHU={sum(1 for r in scene if r['function_start'].startswith('TIDAK TAHU'))}",
      f"EDGES_WITH_BYTE_TSV_VALIDATION={len(vrows)}",
      f"BYTE_TSV_MATCH={sum(1 for r in vrows if r['validation']=='MATCH')}",
      f"BYTE_TSV_CONFLICT={sum(1 for r in vrows if r['validation']=='CONFLICT')}",
      f"BYTE_TSV_NO_ROW={sum(1 for r in vrows if r['validation']=='NO_TSV_ROW')}",
      "NO_BYTES_EXCERPT_EMITTED=YES",
      "NO_GLOBAL_ABSENCE_CLAIM=YES",
    ]
    (out/"UD1_STATIC_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines));print("\n".join(dxlines))
if __name__=="__main__":main()
