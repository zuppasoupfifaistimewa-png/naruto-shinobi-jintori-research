#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,io,re,subprocess
from bisect import bisect_right
from collections import defaultdict
from pathlib import Path

RANGES={
 "EXE":(0x800,385024),
 "ENTRY0":(0x5F800,110536),
 "ENTRY1":(0x10BB000,596412),
}
UNKNOWN={"","TIDAK TAHU","UNKNOWN","N/A","NA","NONE","-","NULL"}
def norm(s): return (s or "").strip().lower().replace(" ","_")
def hx(s):
    s=(s or "").strip()
    if not s or s.upper() in UNKNOWN: raise ValueError("missing hex")
    return int(s,16)
def byteval(s):
    s=(s or "").strip()
    if not s or s.upper() in UNKNOWN: raise ValueError("missing bytes")
    p=s.split()
    if len(p)==1 and len(p[0])>2 and len(p[0])%2==0:
        p=[p[0][i:i+2] for i in range(0,len(p[0]),2)]
    if any(len(x)!=2 for x in p): raise ValueError("noncanonical bytes")
    return bytes(int(x,16) for x in p)
def label_for(row,hm,source):
    raw=""
    for key in ("image","region"):
        if key in hm:
            v=(row.get(hm[key],"") or "").strip().upper()
            if v and v not in UNKNOWN:
                raw=v; break
    compact=re.sub(r"[^A-Z0-9]","",raw)
    if compact:
        if "ENTRY0" in compact or "DATA0" in compact: return "ENTRY0"
        if "ENTRY1" in compact: return "ENTRY1"
        if compact in {"EXE","SLPS03553","SLPS03553EXE"} or "SLPS03553" in compact: return "EXE"
        return "IMAGE:"+compact
    if "file_offset" in hm:
        try: fo=hx(row.get(hm["file_offset"],""))
        except Exception: fo=None
        if fo is not None:
            for name,(start,size) in RANGES.items():
                if start<=fo<start+size:return name
    return "UNRESOLVED:"+source
def tracked_tsv(root):
    raw=subprocess.check_output(["git","-C",str(root),"ls-files","-z","--","*.tsv"])
    return [x for x in raw.decode("utf-8","replace").split("\0") if x]
def fields_for(path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        rd=csv.DictReader(f,delimiter="\t")
        if not rd.fieldnames:return None
        hm={norm(x):x for x in rd.fieldnames if x}
    pc=hm.get("pc") or hm.get("instruction_pc")
    by=hm.get("bytes") or hm.get("instruction_bytes")
    return (hm,pc,by) if pc and by else None
def group_ranges(addresses):
    out=[]
    for label,aset in addresses.items():
        vals=sorted(aset)
        if not vals:continue
        a=b=vals[0]
        for n in vals[1:]:
            if n==b+1:b=n
            else:out.append((label,a,b));a=b=n
        out.append((label,a,b))
    return out
def scan(root,files):
    addresses=defaultdict(set); malformed=0; eligible=0; aliases=0
    for rel in files:
        path=root/rel
        try: meta=fields_for(path)
        except Exception: malformed+=1; continue
        if not meta:continue
        hm,pc_col,bytes_col=meta; eligible+=1
        if "instruction_pc" in hm or "instruction_bytes" in hm or ("image" not in hm and "region" not in hm):aliases+=1
        try:
            with path.open("r",encoding="utf-8-sig",newline="") as f:
                rd=csv.DictReader(f,delimiter="\t")
                for row in rd:
                    try:
                        pc=hx(row.get(pc_col,"")); data=byteval(row.get(bytes_col,""))
                        label=label_for(row,hm,rel)
                    except Exception: malformed+=1; continue
                    addresses[label].update(range(pc,pc+len(data)))
        except Exception: malformed+=1
    return addresses,eligible,aliases,malformed
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",required=True);ap.add_argument("--out",required=True)
    a=ap.parse_args();root=Path(a.root).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    files=tracked_tsv(root)
    before,eligible,aliases,malformed=scan(root,files)
    groups=group_ranges(before)
    large=[x for x in groups if x[2]-x[1]+1>64 and not x[0].startswith("UNRESOLVED:")]
    bylabel=defaultdict(list)
    for label,start,end in large:bylabel[label].append((start,end))
    ix={k:([x[0] for x in sorted(v)],sorted(v)) for k,v in bylabel.items()}
    protected=lambda rel: (Path(rel).name.upper().startswith(("UB1_","UC1_")) or Path(rel).name.upper()=="DX1_ALL_PLUS1A_ACCESS.TSV")
    trimmed=[];changed=[]
    for rel in files:
        path=root/rel
        try: meta=fields_for(path)
        except Exception: continue
        if not meta:continue
        hm,pc_col,bytes_col=meta
        removals=[]
        try:
            with path.open("r",encoding="utf-8-sig",newline="") as f:
                rd=csv.DictReader(f,delimiter="\t"); prev=rd.line_num
                for row in rd:
                    lo=prev+1;hi=rd.line_num;prev=hi
                    try:
                        pc=hx(row.get(pc_col,"")); data=byteval(row.get(bytes_col,"")); label=label_for(row,hm,rel)
                    except Exception:continue
                    if label not in ix:continue
                    starts,ranges=ix[label];i=bisect_right(starts,pc)-1
                    if i<0:continue
                    gs,ge=ranges[i]
                    if not (gs<=pc<=ge):continue
                    if pc>=gs and pc+len(data)-1<=gs+63:continue
                    if protected(rel):continue
                    removals.append((lo,hi,pc,label))
        except Exception:continue
        if not removals:continue
        raw=path.read_bytes();bom=raw.startswith(b"\xef\xbb\xbf")
        text=raw.decode("utf-8-sig");lines=text.splitlines(keepends=True)
        drop=set()
        for lo,hi,pc,label in removals:
            drop.update(range(lo,hi+1))
            trimmed.append({"source":rel,"line_number":lo,"pc":f"0x{pc:08X}","label":label})
        kept="".join(line for n,line in enumerate(lines,1) if n not in drop)
        path.write_bytes((b"\xef\xbb\xbf" if bom else b"")+kept.encode("utf-8"))
        changed.append(rel)
    after,eligible2,aliases2,malformed2=scan(root,files)
    after_groups=group_ranges(after)
    remaining_clear=sum(1 for label,s,e in after_groups if e-s+1>64 and not label.startswith("UNRESOLVED:"))
    remaining_unresolved=sum(1 for label,s,e in after_groups if e-s+1>64 and label.startswith("UNRESOLVED:"))
    protected_left=sum(1 for label,s,e in after_groups if e-s+1>64 and not label.startswith("UNRESOLVED:"))
    with (out/"UC0_TRIMMED_ROWS.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["source","line_number","pc","label"],delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(trimmed)
    (out/"UC0_TRIMMED_FILES.txt").write_text("".join(x+"\n" for x in changed),encoding="utf-8")
    (out/"UC0_UNRESOLVED_OVER_64_GROUPS_COUNT.txt").write_text(f"{remaining_unresolved}\n",encoding="ascii")
    rc=0 if remaining_clear==0 else 4
    lines=[
      "UC0_UNION_GATE",
      f"TRACKED_TSV_FILES={len(files)}",
      f"ELIGIBLE_BYTE_TSV_FILES={eligible}",
      f"ALIAS_OR_REGION_FALLBACK_FILES={aliases}",
      f"INITIAL_LABELED_GROUPS_OVER_64B={len(large)}",
      f"TRIMMED_ROWS={len(trimmed)}",
      f"TRIMMED_FILES={len(changed)}",
      f"REMAINING_LABELED_GROUPS_OVER_64B={remaining_clear}",
      f"REMAINING_UNRESOLVED_GROUPS_OVER_64B={remaining_unresolved}",
      f"MALFORMED_ROWS_OR_FILES={malformed+malformed2}",
      "PROTECTED_FILES=UB1_*.tsv,UC1_*.tsv,DX1_ALL_PLUS1A_ACCESS.tsv",
      "REMOVAL_REPORT=UC0_TRIMMED_ROWS.tsv (source,line_number,pc,label; no byte values)",
      "UNRESOLVED_POLICY=per-source-file isolation; only count reported",
      f"STATUS={'PASS' if rc==0 else 'FAIL'}",
      f"EXIT_CODE={rc}",
    ]
    (out/"UC0_UNION_GATE_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines))
    return rc
if __name__=="__main__":raise SystemExit(main())
