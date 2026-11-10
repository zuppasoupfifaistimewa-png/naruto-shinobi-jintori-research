#!/usr/bin/env python3
"""UE0: immutable-baseline, text-only byte union with bounded registered pruning."""
from __future__ import annotations
import argparse,csv,re,subprocess,tarfile,io
from collections import defaultdict
from pathlib import Path

UNKNOWN={"","TIDAK TAHU","TIDAK_TAHU","UNKNOWN","N/A","NA","NONE","NULL","-"}
CANON={"bytes","instruction_bytes"}
EXTRA={"bytes_or_excerpt_hex","bytes_excerpt_hex_max64","contiguous_bytes","byte_sequence_hex","bytes_hex"}
PC_NAMES=("pc","instruction_pc","address","virtual_address","start_pc")
OFF_NAMES=("file_offset","offset","start_offset","byte_offset")
ID_NAMES=("image","region","entry","resource","module","binary","source_image","image_name","rom_entry","data_entry")
EXE=(0x80010000,385024)
E0=(0x800AD000,110536)
E1=(0x800AD450,596412)

def norm(s): return re.sub(r"[^a-z0-9]+","_",str(s or "").strip().lower()).strip("_")
def val(row,hm,names):
    for n in names:
        if n in hm: return (row.get(hm[n]) or "").strip()
    return ""
def parse_hex(s):
    s=(s or "").strip()
    if not s or s.upper() in UNKNOWN: return None
    try: return int(s,16)
    except Exception: return None
def parse_bytes(s):
    s=(s or "").strip()
    if not s or s.upper() in UNKNOWN: return None,"UNKNOWN"
    toks=re.split(r"[\s,;|]+",s)
    out=[]
    for t in toks:
        if not t or t.upper() in UNKNOWN: continue
        z=t.lower().replace("0x","")
        if not z or not re.fullmatch(r"[0-9a-f]+",z): return None,"MALFORMED"
        if len(z)==2: out.append(int(z,16))
        elif len(z)%2==0: out.extend(int(z[i:i+2],16) for i in range(0,len(z),2))
        else: return None,"MALFORMED"
    return (bytes(out),"OK") if out else (None,"UNKNOWN")
def infer_label(row,hm,source,pc,off):
    for col in ID_NAMES:
        if col not in hm: continue
        raw=(row.get(hm[col]) or "").strip()
        if not raw or raw.upper() in UNKNOWN: continue
        z=norm(raw).upper()
        compact=re.sub(r"[^A-Z0-9]","",raw.upper())
        if compact in {"0","ENTRY0","ENTRY_0","DATA0","DATA_0","E0"} or "ENTRY0" in compact or "DATA0" in compact: return "ENTRY0"
        if compact in {"1","ENTRY1","ENTRY_1","DATA1","DATA_1","E1"} or "ENTRY1" in compact or "DATA1" in compact: return "ENTRY1"
        if "SLPS03553" in compact or compact in {"EXE","MAINEXE","SLPS03553EXE"}: return "EXE"
        return "IMAGE:"+z
    p=source.upper()
    if re.search(r"(^|[/_.-])ENTRY0([/_.-]|$)",p) or "ENTRY0" in p: return "ENTRY0"
    if re.search(r"(^|[/_.-])ENTRY1([/_.-]|$)",p) or "ENTRY1" in p: return "ENTRY1"
    if "SLPS_035.53" in p or "MAIN_EXE" in p or "/EXE/" in p: return "EXE"
    if off is not None:
        # These are DATA.BIN file-offset ranges; no filename-only inference.
        if 0x5F800<=off<0x5F800+E0[1]: return "ENTRY0"
        if 0x10BB000<=off<0x10BB000+E1[1]: return "ENTRY1"
    if pc is not None:
        if EXE[0]<=pc<EXE[0]+EXE[1]: return "EXE"
        in0=E0[0]<=pc<E0[0]+E0[1]; in1=E1[0]<=pc<E1[0]+E1[1]
        if in0 and not in1:return "ENTRY0"
        if in1 and not in0:return "ENTRY1"
    return "UNRESOLVED:"+source
def byte_cols(hm,legacy=False):
    names=[]
    for n,orig in hm.items():
        if legacy:
            if n in CANON:names.append((n,orig))
        elif n in CANON|EXTRA or n.startswith("bytes_") or n.endswith("_bytes") or n.endswith("_bytes_hex"):
            names.append((n,orig))
    return names
def collect(root,legacy=False):
    maps=defaultdict(dict); origins=defaultdict(lambda:defaultdict(set)); sequences=[]
    malformed=[]; manifest=[]; conflicts=0; valid=0; unknown=0
    files=sorted(root.rglob("*.tsv"))
    for path in files:
        rel=path.relative_to(root).as_posix()
        try:
            with path.open("r",encoding="utf-8-sig",newline="") as f:
                rd=csv.DictReader(f,delimiter="\t")
                if not rd.fieldnames: continue
                hm={norm(x):x for x in rd.fieldnames if x}
                cols=byte_cols(hm,legacy)
                if not cols: continue
                pc_col=next((hm[x] for x in PC_NAMES if x in hm),None)
                off_col=next((hm[x] for x in OFF_NAMES if x in hm),None)
                row_count=0
                for row in rd:
                    row_count+=1
                    rawpc=(row.get(pc_col) or "").strip() if pc_col else ""
                    rawoff=(row.get(off_col) or "").strip() if off_col else ""
                    pc=parse_hex(rawpc); off=parse_hex(rawoff)
                    for n,original in cols:
                        b,status=parse_bytes(row.get(original,""))
                        if status=="UNKNOWN": unknown+=1; continue
                        if status=="MALFORMED":
                            malformed.append((rel,rd.line_num,original,"NON_HEX_BYTE_FIELD"));continue
                        if not b: continue
                        if legacy and (pc is None): continue
                        label=infer_label(row,hm,rel,pc,off)
                        valid+=1
                        if pc is not None:
                            kind="PC"; start=pc
                            key=(label,kind)
                            for j,x in enumerate(b):
                                pos=start+j
                                old=maps[key].get(pos)
                                if old is not None and old!=x: conflicts+=1
                                else: maps[key][pos]=x
                                origins[key][pos].add(rel+"#"+str(rd.line_num)+":"+n)
                        elif off is not None:
                            kind="FILEOFF"; start=off; key=(label,kind)
                            for j,x in enumerate(b):
                                pos=start+j
                                old=maps[key].get(pos)
                                if old is not None and old!=x: conflicts+=1
                                else: maps[key][pos]=x
                                origins[key][pos].add(rel+"#"+str(rd.line_num)+":"+n)
                        else:
                            # Bytes without a PC/offset stay isolated by source row and field.
                            sequences.append({"label":label,"kind":"NO_PC","start":0,"data":b,
                                              "source":rel,"line":rd.line_num,"field":n})
                manifest.append((rel,len(cols),pc_col or "NONE",off_col or "NONE",row_count))
        except Exception as e:
            malformed.append((rel,0,"FILE","READ_"+type(e).__name__))
    return maps,origins,sequences,malformed,manifest,conflicts,valid,unknown
def groups_from(maps,origins,sequences):
    out=[]
    for (label,kind),items in maps.items():
        vals=sorted(items)
        if not vals: continue
        st=pr=vals[0]
        def emit(a,z):
            src=set()
            for k in range(a,z+1): src.update(origins[(label,kind)][k])
            out.append({"label":label,"kind":kind,"start":a,"end":z+1,"length":z-a+1,
                        "source_count":len({x.split("#",1)[0] for x in src}),"sources":";".join(sorted({x.split("#",1)[0] for x in src})),
                        "source_rows":";".join(sorted(src))})
        for n in vals[1:]:
            if n!=pr+1:emit(st,pr);st=n
            pr=n
        emit(st,pr)
    for s in sequences:
        out.append({"label":s["label"],"kind":"NO_PC","start":None,"end":None,"length":len(s["data"]),
                    "source_count":1,"sources":s["source"],"source_rows":f'{s["source"]}#{s["line"]}:{s["field"]}'})
    return out
def write_tsv(path,fields,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        w.writeheader()
        for r in rows:w.writerow({k:r.get(k,"TIDAK TAHU") for k in fields})
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",required=True);ap.add_argument("--out",required=True)
    ap.add_argument("--baseline",default="9a6ccb7969a8cf377006dba01f468fb2c9dc4b05")
    a=ap.parse_args(); root=Path(a.root).resolve(); out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    legacy=collect(root,True); full=collect(root,False)
    lm,lo,ls,lbad,lman,lc,lv,lu=legacy
    fm,fo,fs,fbad,fman,fc,fv,fu=full
    lg=groups_from(lm,lo,ls); fg=groups_from(fm,fo,fs)
    legacy_over=[g for g in lg if g["length"]>64]
    initial_over=[g for g in fg if g["length"]>64]
    # Clip only derived union output; never rewrite or delete a source TSV.
    final_groups=[];pruned=[]
    for g in fg:
        if g["length"]<=64:
            final_groups.append(g);continue
        pruned.append({"label":g["label"],"kind":g["kind"],"start":g["start"],"end_exclusive":g["end"],
                       "original_bytes":g["length"],"retained_bytes":64,"pruned_bytes":g["length"]-64,
                       "source_count":g["source_count"],"sources":g["sources"],"source_rows":g["source_rows"]})
        z=dict(g);z["length"]=64
        if z["kind"]=="NO_PC": z["source_rows"]=g["source_rows"]
        else:z["end"]=int(g["start"])+64
        final_groups.append(z)
    post_over=[g for g in final_groups if g["length"]>64]
    init_fields=["label","kind","start","end_exclusive","bytes","source_count","sources","source_rows"]
    def to_row(g):
        return {"label":g["label"],"kind":g["kind"],"start":f'0x{g["start"]:08X}' if g["kind"]!="NO_PC" else "TIDAK TAHU_NO_PC",
                "end_exclusive":f'0x{g["end"]:08X}' if g["end"] is not None else "TIDAK TAHU_NO_PC",
                "bytes":g["length"],"source_count":g["source_count"],"sources":g["sources"],"source_rows":g["source_rows"]}
    write_tsv(out/"UE0_UNION_GROUPS.tsv",init_fields,[to_row(g) for g in final_groups])
    write_tsv(out/"UE0_INITIAL_OVER_64B_GROUPS.tsv",init_fields,[to_row(g) for g in initial_over])
    write_tsv(out/"UE0_OVER_64B_GROUPS.tsv",init_fields,[to_row(g) for g in post_over])
    pr_fields=["label","kind","start","end_exclusive","original_bytes","retained_bytes","pruned_bytes","source_count","sources","source_rows"]
    write_tsv(out/"UE0_PRUNED_GROUPS.tsv",pr_fields,pruned)
    write_tsv(out/"UE0_MALFORMED_ROWS.tsv",["source","line","field","reason"],
              [{"source":x[0],"line":x[1],"field":x[2],"reason":x[3]} for x in fbad])
    write_tsv(out/"UE0_SOURCE_MANIFEST.tsv",["source","byte_columns","pc_column","offset_column","rows"],
              [{"source":x[0],"byte_columns":x[1],"pc_column":x[2],"offset_column":x[3],"rows":x[4]} for x in fman])
    labeled=lambda g:not g["label"].startswith("UNRESOLVED:")
    lines=["UE0_IMMUTABLE_BASELINE_BYTE_UNION",f"BASELINE_INCLUSIVE={a.baseline}",
      f"BASELINE_TSV_FILES={len(fman)}",f"FULL_BYTE_FIELDS={sum(x[1] for x in fman)}",
      f"LEGACY_CANONICAL_PC_GROUPS_OVER_64B={len(legacy_over)}",
      f"LEGACY_CANONICAL_LABELED_GROUPS_OVER_64B={sum(1 for g in legacy_over if labeled(g))}",
      f"ALL_BYTE_FIELDS_GROUPS_OVER_64B={len(initial_over)}",
      f"ALL_BYTE_FIELDS_LABELED_GROUPS_OVER_64B={sum(1 for g in initial_over if labeled(g))}",
      f"ALL_BYTE_FIELDS_UNRESOLVED_GROUPS_OVER_64B={sum(1 for g in initial_over if not labeled(g))}",
      f"ALL_BYTE_FIELDS_NO_PC_GROUPS_OVER_64B={sum(1 for g in initial_over if g['kind']=='NO_PC')}",
      f"PRUNED_GROUPS_REGISTERED={len(pruned)}",f"PRUNED_BYTES={sum(x['pruned_bytes'] for x in pruned)}",
      f"POST_PRUNE_GROUPS_OVER_64B={len(post_over)}",f"VALID_BYTE_FIELDS={fv}",f"UNKNOWN_BYTE_TOKENS_SKIPPED={fu}",
      f"BYTE_CONFLICTS={fc}",f"MALFORMED_ROWS={len(fbad)}",
      "UNKNOWN_TOKEN_POLICY=TIDAK TAHU/UNKNOWN/N/A/NA/NONE/NULL/- are not bytes",
      "LABEL_POLICY=explicit row image/region/entry/resource/module fields; unambiguous source path; unique image address/file-offset range; otherwise per-source UNRESOLVED",
      "NO_PC_POLICY=each source row and byte field isolated; >64B derived sequence clipped to 64B and registered",
      "SOURCE_POLICY=immutable git snapshot; no source TSV modified or deleted",
      "RECONCILIATION=legacy canonical pc+bytes scan and expanded byte-column/no-PC scan both computed from the same baseline",
      f"STATUS={'PASS' if not post_over else 'FAIL'}",f"EXIT_CODE={1 if post_over else 0}"]
    (out/"UE0_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines))
    return 1 if post_over else 0
if __name__=="__main__": raise SystemExit(main())
