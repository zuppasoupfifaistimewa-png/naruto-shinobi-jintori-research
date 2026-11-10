#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,struct,subprocess
from collections import defaultdict
from pathlib import Path
from capstone import Cs,CS_ARCH_MIPS,CS_MODE_MIPS32,CS_MODE_LITTLE_ENDIAN

EXE_BASE,EXE_OFF,EXE_SIZE=0x80010000,0x800,385024
E0_BASE,E0_OFF,E0_SIZE=0x800AD000,0x5F800,110536
E1_BASE,E1_OFF,E1_SIZE=0x800AD450,0x10BB000,596412
EXE_SHA="a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
DATA_SHA="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
E0_SHA="56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4"
E1_SHA="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
LIMIT=64; TABLE=0x800558A8; STRIDE=28
TARGETS={0x800D15A8:"KREDIT_FUN_800D15A8",0x800D2520:"FEE_800D2520",0x800D46EC:"FEE_800D46EC"}
md=Cs(CS_ARCH_MIPS,CS_MODE_MIPS32|CS_MODE_LITTLE_ENDIAN); md.detail=False

def write_tsv(path,fields,rows):
    with Path(path).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        w.writeheader()
        for r in rows:w.writerow({k:r.get(k,"TIDAK TAHU") for k in fields})
def hnorm(x):return (x or "").strip().lower().replace(" ","_")
def hx(s):
    s=(s or "").strip()
    if not s or s.upper() in {"TIDAK TAHU","UNKNOWN","N/A","NONE","-"}:raise ValueError("missing hex")
    return int(s,16)
def blob_bytes(s):
    s=(s or "").strip()
    if not s or s.upper() in {"TIDAK TAHU","UNKNOWN","N/A","NONE","-"}:raise ValueError("missing bytes")
    p=s.split()
    if not p or any(len(x)!=2 for x in p):raise ValueError("noncanonical byte string")
    return bytes(int(x,16) for x in p)
def label_for(img,fo,source):
    raw=(img or "").strip().upper(); compact="".join(c for c in raw if c.isalnum())
    if compact:
        if "ENTRY0" in compact or "DATA0" in compact:return "ENTRY0"
        if "ENTRY1" in compact:return "ENTRY1"
        if compact in {"EXE","SLPS03553","SLPS03553EXE"} or "SLPS03553" in compact:return "EXE"
        return "IMAGE:"+compact
    if fo is not None:
        if EXE_OFF<=fo<EXE_OFF+EXE_SIZE:return "EXE"
        if E0_OFF<=fo<E0_OFF+E0_SIZE:return "ENTRY0"
        if E1_OFF<=fo<E1_OFF+E1_SIZE:return "ENTRY1"
    p=source.upper()
    if "ENTRY0" in p or "ENTRY_0" in p:return "ENTRY0"
    if "ENTRY1" in p or "ENTRY_1" in p:return "ENTRY1"
    if "EXE" in p or "SLPS_035.53" in p:return "EXE"
    return "UNRESOLVED:"+source

def audit_uc0(root,out):
    names=subprocess.check_output(["git","-C",str(root),"ls-files","-z","--","*.tsv"]).decode().split("\0")
    files=[x for x in names if x]; vals={}; origins=defaultdict(set); conflicts=set()
    candidates=set(); aliases=set(); malformed=[]; valid_rows=0; unresolved=set()
    for rel in files:
        try:
            with (root/rel).open("r",encoding="utf-8-sig",newline="") as f:
                rd=csv.DictReader(f,delimiter="\t")
                if not rd.fieldnames:continue
                hm={hnorm(x):x for x in rd.fieldnames if x}
                pc_col=hm.get("pc") or hm.get("instruction_pc")
                by_col=hm.get("bytes") or hm.get("instruction_bytes")
                if not pc_col or not by_col:continue
                candidates.add(rel)
                if "instruction_pc" in hm or "instruction_bytes" in hm or ("image" not in hm and "file_offset" in hm):aliases.add(rel)
                for row in rd:
                    rp=row.get(pc_col,""); rb=row.get(by_col,"")
                    if not rp or not rb or rb.strip().upper() in {"TIDAK TAHU","UNKNOWN","N/A","NONE","-"}:continue
                    try:
                        pc=hx(rp); data=blob_bytes(rb)
                        fo=hx(row.get(hm["file_offset"],"")) if "file_offset" in hm and row.get(hm["file_offset"],"").strip() else None
                        label=label_for(row.get(hm["image"],"") if "image" in hm else "",fo,rel)
                    except Exception as e:
                        malformed.append({"source":rel,"line":rd.line_num,"reason":type(e).__name__+":"+str(e)});continue
                    if label.startswith("UNRESOLVED:"):unresolved.add(label)
                    valid_rows+=1
                    for i,b in enumerate(data):
                        k=(label,pc+i)
                        if k in vals and vals[k]!=b:conflicts.add(k)
                        else:vals[k]=b
                        origins[k].add(rel)
        except Exception as e:
            malformed.append({"source":rel,"line":0,"reason":"FILE_READ_"+type(e).__name__+":"+str(e)})
    by_label=defaultdict(list)
    for label,addr in vals:by_label[label].append(addr)
    groups=[]
    for label,addresses in sorted(by_label.items()):
        addresses.sort()
        if not addresses:continue
        start=prev=addresses[0]
        def emit(a,b):
            srcs=sorted(set().union(*(origins[(label,n)] for n in range(a,b+1))))
            groups.append({"label":label,"start_pc":f"0x{a:08X}","end_exclusive_pc":f"0x{b+1:08X}",
                           "bytes":b+1-a,"source_count":len(srcs),"sources":";".join(srcs)})
        for addr in addresses[1:]:
            if addr!=prev+1:emit(start,prev);start=addr
            prev=addr
        emit(start,prev)
    over=[g for g in groups if g["bytes"]>LIMIT]
    write_tsv(out/"UC0_BYTE_UNION_GROUPS.tsv",["label","start_pc","end_exclusive_pc","bytes","source_count","sources"],groups)
    write_tsv(out/"UC0_OVER_64B_GROUPS.tsv",["label","start_pc","end_exclusive_pc","bytes","source_count","sources"],over)
    write_tsv(out/"UC0_MALFORMED_ROWS.tsv",["source","line","reason"],malformed)
    lines=["UC0_ALL_TRACKED_TSV_BYTE_UNION",f"TRACKED_TSV_FILES={len(files)}",
           f"ELIGIBLE_TSV_FILES={len(candidates)}",f"ALIAS_OR_FALLBACK_TSV_FILES={len(aliases)}",
           f"VALID_BYTE_ROWS={valid_rows}",f"UNIQUE_IMAGE_ADDRESS_BYTES={len(vals)}",
           f"CONTIGUOUS_GROUPS={len(groups)}",f"GROUPS_OVER_64B={len(over)}",
           f"CONFLICTING_IMAGE_ADDRESS_BYTES={len(conflicts)}",f"MALFORMED_ROWS={len(malformed)}",
           f"UNRESOLVED_LABELS={len(unresolved)}",
           "UNRESOLVED_LABEL_POLICY=kept separate per source TSV; no cross-file merge without defensible image identity",
           "LIMIT_POLICY=64 bytes per contiguous group; audit-only; no old TSV edited or deleted"]
    (out/"UC0_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    return lines

def u32(data,base,pc):
    off=pc-base
    if off<0 or off+4>len(data):return None
    return struct.unpack_from("<I",data,off)[0]
def parts(w):return ((w>>26)&63,(w>>21)&31,(w>>16)&31,(w>>11)&31,(w>>6)&31,w&63,w&0xffff)
def prolog(data,base,pc):
    w=u32(data,base,pc)
    if w is None:return False
    op,rs,rt,rd,sh,fn,imm=parts(w)
    if not(op==9 and rs==29 and rt==29 and (imm&0x8000)):return False
    for n in range(1,13):
        q=u32(data,base,pc+4*n)
        if q is None:break
        o,s,t,d,h,f,im=parts(q)
        if o==0x2B and s==29 and t==31:return True
    return False
def maps_at(pc,images):
    return [(n,d,b) for n,d,b in images if b<=pc<b+len(d) and prolog(d,b,pc)]
def calls_in_function(data,base,start,max_bytes=0x1000):
    off=start-base
    if off<0 or off+4>len(data):return [],False
    regs={0:0}; rows=[]; ended=False
    for ins in md.disasm(data[off:min(len(data),off+max_bytes)],start):
        w=int.from_bytes(ins.bytes,"little");op,rs,rt,rd,sh,fn,imm=parts(w)
        if op==3:
            t=((ins.address+4)&0xF0000000)|((w&0x03ffffff)<<2)
            rows.append({"pc":ins.address,"kind":"JAL","target":t,"status":"DIRECT"});regs[31]=None
        elif op==0 and fn==9:
            t=regs.get(rs)
            rows.append({"pc":ins.address,"kind":"JALR","target":t,"status":"STATIC_REGISTER" if t is not None else "TIDAK_TAHU_DYNAMIC"})
            regs[rd or 31]=None
        if op==15:regs[rt]=(imm<<16)&0xffffffff
        elif op in (8,9):
            v=regs.get(rs);regs[rt]=((v+((imm^0x8000)-0x8000))&0xffffffff) if v is not None else None
        elif op==13:
            v=regs.get(rs);regs[rt]=(v|imm) if v is not None else None
        elif op==12:
            v=regs.get(rs);regs[rt]=(v&imm) if v is not None else None
        elif op==0 and fn in (0,2,3):
            v=regs.get(rt);regs[rd]=((v<<sh)&0xffffffff if fn==0 else (v>>sh if v is not None else None)) if v is not None else None
        elif op==0 and fn in (0x21,0x23,0x25,0x24,0x26):
            a,b=regs.get(rs),regs.get(rt);z=None
            if a is not None and b is not None:
                if fn==0x21:z=(a+b)&0xffffffff
                elif fn==0x23:z=(a-b)&0xffffffff
                elif fn==0x25:z=a|b
                elif fn==0x24:z=a&b
                else:z=a^b
            regs[rd]=z
        elif op in (0x20,0x21,0x23,0x24,0x25):regs[rt]=None
        elif op==0 and fn not in (8,9,12,13,24,25,26,27) and rd:regs[rd]=None
        if op==0 and fn==8 and rs==31:ended=True;break
    return rows,ended

def audit_uc1(exe,data,out):
    e0=data[E0_OFF:E0_OFF+E0_SIZE];e1=data[E1_OFF:E1_OFF+E1_SIZE]
    if len(exe)!=EXE_SIZE or hashlib.sha256(exe).hexdigest()!=EXE_SHA:raise SystemExit("UC1_EXE_IDENTITY_FAIL")
    if hashlib.sha256(data).hexdigest()!=DATA_SHA:raise SystemExit("UC1_DATA_BIN_IDENTITY_FAIL")
    if hashlib.sha256(e0).hexdigest()!=E0_SHA or hashlib.sha256(e1).hexdigest()!=E1_SHA:raise SystemExit("UC1_ENTRY_SLICE_IDENTITY_FAIL")
    images=[("EXE",exe,EXE_BASE),("ENTRY0",e0,E0_BASE),("ENTRY1",e1,E1_BASE)]
    cols=[];handlers=[];edges=[];reach=[]
    for i in range(8):
        base=TABLE+STRIDE*i; words=[]
        for c in range(8):
            pc=base+4*c;v=u32(exe,EXE_BASE,pc);words.append(v)
            cols.append({"entry":i,"record_base":f"0x{base:08X}","column":c,"field_offset":f"+0x{4*c:X}",
                         "address":f"0x{pc:08X}","word_u32":f"0x{v:08X}" if v is not None else "TIDAK TAHU",
                         "field_role":"FUNCTION_POINTER" if c==2 else "OTHER_WORD",
                         "overlaps_next_record":"YES" if c==7 and i<7 else "NO"})
        target=words[2];cands=maps_at(target,images) if target is not None else []
        handlers.append({"entry":i,"record_base":f"0x{base:08X}","function_pointer_slot":f"0x{base+8:08X}",
                         "handler_target":f"0x{target:08X}" if target is not None else "TIDAK TAHU",
                         "candidate_images":";".join(x[0] for x in cands) if cands else "TIDAK TAHU",
                         "mapping_status":"PROLOG_CONFIRMED" if len(cands)==1 else ("AMBIGUOUS_PROLOG_MAP" if len(cands)>1 else "TIDAK TAHU_NO_PROLOG")})
        queue=[(n,d,b,target,0) for n,d,b in cands];seen=set()
        while queue:
            name,buf,b,fn,depth=queue.pop(0)
            if (name,fn) in seen or depth>3:continue
            seen.add((name,fn)); cr,ended=calls_in_function(buf,b,fn)
            for call in cr:
                t=call["target"];tm=maps_at(t,images) if t is not None else []
                edges.append({"handler_entry":i,"handler_target":f"0x{target:08X}","depth":depth,
                              "source_image":name,"function_start":f"0x{fn:08X}","call_pc":f"0x{call['pc']:08X}",
                              "kind":call["kind"],"target_pc":f"0x{t:08X}" if t is not None else "TIDAK TAHU",
                              "target_images":";".join(x[0] for x in tm) if tm else "TIDAK TAHU","resolution":call["status"]})
                if t is not None and depth<3:
                    queue.extend((tn,td,tb,t,depth+1) for tn,td,tb in tm)
            if not ended:
                edges.append({"handler_entry":i,"handler_target":f"0x{target:08X}","depth":depth,
                              "source_image":name,"function_start":f"0x{fn:08X}","call_pc":"TIDAK TAHU",
                              "kind":"FUNCTION_END","target_pc":"TIDAK TAHU","target_images":"TIDAK TAHU",
                              "resolution":"NO_JR_RA_WITHIN_0x1000"})
        local=[x for x in edges if x["handler_entry"]==i]
        for t,label in TARGETS.items():
            found=[x for x in local if x["target_pc"]==f"0x{t:08X}"]
            unknown=any(x["resolution"] in {"TIDAK_TAHU_DYNAMIC","NO_JR_RA_WITHIN_0x1000"} for x in local)
            st="REACHED" if found else ("TIDAK TAHU_DYNAMIC_OR_UNBOUNDED" if unknown else "NOT_SEEN_WITHIN_DEPTH_3")
            reach.append({"handler_entry":i,"handler_target":f"0x{target:08X}" if target is not None else "TIDAK TAHU",
                          "target":f"0x{t:08X}","target_role":label,"status":st,
                          "matching_call_pcs":";".join(x["call_pc"] for x in found)})
    write_tsv(out/"UC1_TABLE_COLUMNS.tsv",["entry","record_base","column","field_offset","address","word_u32","field_role","overlaps_next_record"],cols)
    write_tsv(out/"UC1_HANDLERS.tsv",["entry","record_base","function_pointer_slot","handler_target","candidate_images","mapping_status"],handlers)
    write_tsv(out/"UC1_CALL_EDGES.tsv",["handler_entry","handler_target","depth","source_image","function_start","call_pc","kind","target_pc","target_images","resolution"],edges)
    write_tsv(out/"UC1_TARGET_REACHABILITY.tsv",["handler_entry","handler_target","target","target_role","status","matching_call_pcs"],reach)
    return handlers,edges,reach

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",required=True);p.add_argument("--exe",required=True);p.add_argument("--data",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();root=Path(a.root).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    s0=audit_uc0(root,out);h,e,r=audit_uc1(Path(a.exe).read_bytes(),Path(a.data).read_bytes(),out)
    lines=s0+["UC1_STATIC_ENTRY0_TO_ENTRY7","EXE_FILE_OFFSET_FORMULA=0x800 + (PC - 0x80010000)",
      "ENTRY0_FILE_OFFSET=0x5F800; SIZE=110536; STATIC_IMPORT_BASE=0x800AD000 (not runtime proof)",
      "ENTRY1_FILE_OFFSET=0x10BB000; SIZE=596412; STATIC_IMPORT_BASE=0x800AD450",
      "TABLE_FORMULA=0x800558A8 + 28*entry; function pointer at +8; columns +0..+28",
      f"HANDLER_RECORDS={len(h)}",f"CALL_GRAPH_EDGES={len(e)}",f"TARGET_REACHABILITY_ROWS={len(r)}",
      "CALL_GRAPH_DEPTH_MAX=3","CALL_GRAPH_POLICY=linear bounded decode to JR RA or 0x1000 bytes; traverses only prolog-confirmed mappings",
      "UNRESOLVED_JALR_AND_NONRETURNING_SCAN=TIDAK TAHU; NOT_SEEN_WITHIN_DEPTH_3 is not proof of global absence",
      "NO_BINARY_OUTPUT=YES"]
    (out/"UC0_UC1_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines))
if __name__=="__main__":main()
