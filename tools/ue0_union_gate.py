#!/usr/bin/env python3
"""UE0: immutable-baseline byte union with a strict 64-byte output gate."""
from __future__ import annotations
import argparse,csv,re
from collections import defaultdict,Counter
from pathlib import Path

BASELINE_DEFAULT="9a6ccb7969a8cf377006dba01f468fb2c9dc4b05"
UNKNOWN={"","TIDAK TAHU","TIDAK_TAHU","UNKNOWN","N/A","NA","NONE","NULL","-"}
BYTE_COLUMNS=("bytes","instruction_bytes","bytes_or_excerpt_hex","bytes_excerpt_hex_max64","contiguous_bytes")
PC_COLUMNS=("pc","instruction_pc","address","virtual_address","start_pc")
OFFSET_COLUMNS=("file_offset","offset","start_offset","byte_offset")
IMAGE_COLUMNS=("image","region","source_image","image_name","binary","binary_name","module","section_image","entry","entry_name","segment","segment_image","section","executable","rom_image","image_id","source_entry")
PATH_COLUMNS=("source_file","file","filename","path","file_path","binary_path","image_path","module_path","rom_path","source")
EXE_BASE,EXE_SIZE=0x80010000,385024
E0_BASE,E0_SIZE=0x800AD000,110536
E1_BASE,E1_SIZE=0x800AD450,596412
def norm(s): return re.sub(r"[^a-z0-9]+","_",str(s or "").strip().lower()).strip("_")
def parse_hex(s):
    s=(s or "").strip()
    if not s or s.upper() in UNKNOWN:return None
    try:return int(s,16)
    except Exception:return None
def parse_bytes(value):
    s=(value or "").strip()
    if not s or s.upper() in UNKNOWN:return None,"UNKNOWN"
    s=re.sub(r"(?i)\bTIDAK[\s_-]+TAHU\b|\bUNKNOWN\b|\bN/?A\b|\bNONE\b|\bNULL\b"," ",s)
    tokens=[x for x in re.split(r"[\s,;|]+",s.strip()) if x]
    out=[]
    for token in tokens:
        z=token.lower()
        if z.startswith("0x"):z=z[2:]
        if not re.fullmatch(r"[0-9a-f]+",z):return None,"MALFORMED"
        if len(z)==2:out.append(int(z,16))
        elif len(z)>2 and len(z)%2==0:out.extend(int(z[i:i+2],16) for i in range(0,len(z),2))
        else:return None,"MALFORMED"
    return (bytes(out),"OK") if out else (None,"UNKNOWN")
def image_label(raw):
    raw=(raw or "").strip()
    if not raw or raw.upper() in UNKNOWN:return None
    compact=re.sub(r"[^A-Z0-9]","",raw.upper())
    if "ENTRY0" in compact or "DATA0" in compact or compact in {"E0"}:return "ENTRY0"
    if "ENTRY1" in compact or "DATA1" in compact or compact in {"E1"}:return "ENTRY1"
    if "SLPS03553" in compact or compact in {"EXE","MAINEXE"}:return "EXE"
    return None
def infer_label(row,hm,source,pc,fo):
    candidates=set()
    for col in IMAGE_COLUMNS:
        if col not in hm:continue
        found=image_label(row.get(hm[col],""))
        if found:candidates.add(found)
    if len(candidates)==1:return next(iter(candidates))
    if len(candidates)>1:return "UNRESOLVED:CONFLICTING_IMAGE_METADATA"
    path_values=[source]
    for col in PATH_COLUMNS:
        if col in hm:
            v=(row.get(hm[col]) or "").strip()
            if v and v.upper() not in UNKNOWN:path_values.append(v)
    path_labels=set()
    for raw in path_values:
        found=image_label(raw)
        if found:path_labels.add(found)
        up=raw.upper()
        if re.search(r"ENTRY[_ -]?0|DATA[_ -]?0",up):path_labels.add("ENTRY0")
        if re.search(r"ENTRY[_ -]?1|DATA[_ -]?1",up):path_labels.add("ENTRY1")
        if "SLPS_035.53" in up or "MAIN_EXE" in up or "/EXE/" in up:path_labels.add("EXE")
    if len(path_labels)==1:return next(iter(path_labels))
    if len(path_labels)>1:return "UNRESOLVED:CONFLICTING_PATH_METADATA"
    if fo is not None:
        matches=[]
        if 0x800<=fo<0x800+EXE_SIZE:matches.append("EXE")
        if 0x5F800<=fo<0x5F800+E0_SIZE:matches.append("ENTRY0")
        if 0x10BB000<=fo<0x10BB000+E1_SIZE:matches.append("ENTRY1")
        if len(matches)==1:return matches[0]
        if len(matches)>1:return "UNRESOLVED:AMBIGUOUS_FILE_OFFSET"
    if pc is not None:
        matches=[]
        if EXE_BASE<=pc<EXE_BASE+EXE_SIZE:matches.append("EXE")
        if E0_BASE<=pc<E0_BASE+E0_SIZE:matches.append("ENTRY0")
        if E1_BASE<=pc<E1_BASE+E1_SIZE:matches.append("ENTRY1")
        if len(matches)==1:return matches[0]
        if len(matches)>1:return "UNRESOLVED:OVERLAPPING_ENTRY_ADDRESS_RANGES"
        return "UNRESOLVED:PC_OUTSIDE_KNOWN_IMAGE_RANGES"
    return "UNRESOLVED:NO_IMAGE_OR_ADDRESS_CONTEXT"
def bounded_join(values,limit=5):
    values=sorted(set(values))
    if not values:return "NONE"
    return ";".join(values[:limit])+(";..." if len(values)>limit else "")
def collect(root):
    maps=defaultdict(dict);origins=defaultdict(lambda:defaultdict(set))
    no_pc=[];malformed=Counter();malformed_sample=defaultdict(list)
    manifest=[];field_counts=Counter();unknown=Counter();valid=Counter();conflicts=0
    files=sorted(root.rglob("*.tsv"))
    for path in files:
        rel=path.relative_to(root).as_posix()
        try:
            with path.open("r",encoding="utf-8-sig",newline="") as f:
                rd=csv.DictReader(f,delimiter="\t")
                if not rd.fieldnames:continue
                hm={norm(x):x for x in rd.fieldnames if x}
                cols=[(n,hm[n]) for n in BYTE_COLUMNS if n in hm]
                if not cols:continue
                pc_col=next((hm[n] for n in PC_COLUMNS if n in hm),None)
                off_col=next((hm[n] for n in OFFSET_COLUMNS if n in hm),None)
                row_count=0
                for row in rd:
                    row_count+=1
                    pc=parse_hex(row.get(pc_col,"")) if pc_col else None
                    fo=parse_hex(row.get(off_col,"")) if off_col else None
                    for col,original in cols:
                        field_counts[col]+=1
                        data,status=parse_bytes(row.get(original,""))
                        if status=="UNKNOWN":unknown[col]+=1;continue
                        if status=="MALFORMED":
                            malformed[(rel,col)]+=1
                            if len(malformed_sample[(rel,col)])<3:malformed_sample[(rel,col)].append(rd.line_num)
                            continue
                        if not data:continue
                        valid[col]+=1
                        label=infer_label(row,hm,rel,pc,fo)
                        source_row=f"{rel}#{rd.line_num}:{col}"
                        if pc is not None:kind="PC";base=pc
                        elif fo is not None:kind="FILE_OFFSET";base=fo
                        else:
                            no_pc.append({"label":label,"kind":"NO_PC","data":data,"source":rel,
                                "line":rd.line_num,"field":col,"source_row":source_row})
                            continue
                        identity=rel if label.startswith("UNRESOLVED:") else ""
                        key=(label,kind,identity)
                        for i,b in enumerate(data):
                            addr=base+i;old=maps[key].get(addr)
                            if old is not None and old!=b:conflicts+=1
                            else:maps[key][addr]=b
                            origins[key][addr].add(source_row)
                manifest.append({"source":rel,"byte_columns":";".join(x[0] for x in cols),
                    "pc_column":pc_col or "NONE","offset_column":off_col or "NONE","rows":row_count})
        except Exception:
            malformed[(rel,"FILE_READ")]+=1
            if len(malformed_sample[(rel,"FILE_READ")])<3:malformed_sample[(rel,"FILE_READ")].append(0)
    return maps,origins,no_pc,malformed,malformed_sample,manifest,field_counts,unknown,valid,conflicts,len(files)
def address_groups(maps,origins):
    groups=[]
    for key,items in maps.items():
        label,kind,identity=key
        addresses=sorted(items)
        if not addresses:continue
        start=previous=addresses[0]
        def emit(a,z):
            src_rows=set()
            for pos in range(a,z+1):src_rows.update(origins[key][pos])
            sources={x.split("#",1)[0] for x in src_rows}
            groups.append({"label":label,"kind":kind,"start":a,"blob":bytes(items[pos] for pos in range(a,z+1)),
                "source_identity":identity,"source_count":len(sources),"sources_sample":bounded_join(sources,2),
                "source_rows_sample":bounded_join(src_rows,2),"source_rows_count":len(src_rows)})
        for pos in addresses[1:]:
            if pos!=previous+1:emit(start,previous);start=pos
            previous=pos
        emit(start,previous)
    return groups
def format_group(g):
    blob=g["blob"];length=len(blob);start=g.get("start");emitted=min(length,64)
    return {"label":g["label"],"label_status":"UNRESOLVED" if g["label"].startswith("UNRESOLVED:") else "RESOLVED",
      "label_reason":g["label"].split(":",1)[1] if g["label"].startswith("UNRESOLVED:") else "MATCHED_CONTEXT",
      "kind":g["kind"],"start":f"0x{start:08X}" if start is not None else "TIDAK TAHU_NO_PC",
      "end_exclusive":f"0x{start+emitted:08X}" if start is not None else "TIDAK TAHU_NO_PC",
      "original_bytes":length,"emitted_bytes":emitted,"pruned_bytes":max(0,length-emitted),
      "source_identity":g.get("source_identity",""),"source_count":g["source_count"],
      "source_rows_count":g["source_rows_count"],"sources_sample":g["sources_sample"],
      "source_rows_sample":g["source_rows_sample"],
      "byte_payload":"OMITTED; metadata only; no byte excerpts published",
      "action":"PRUNED_TO_64" if length>64 else "METADATA_ONLY"}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",required=True);ap.add_argument("--out",required=True)
    ap.add_argument("--baseline",default=BASELINE_DEFAULT);ap.add_argument("--legacy-summary",required=True)
    a=ap.parse_args();root=Path(a.root).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    maps,origins,no_pc,malformed,malformed_sample,manifest,field_counts,unknown,valid,conflicts,file_count=collect(root)
    groups=address_groups(maps,origins)
    groups.extend({"label":x["label"],"kind":"NO_PC","start":None,"blob":x["data"],
      "source_identity":x["source_row"],"source_count":1,"sources_sample":x["source"],
      "source_rows_sample":x["source_row"],"source_rows_count":1} for x in no_pc)
    groups.sort(key=lambda g:(g["label"],g["kind"],g["start"] if g["start"] is not None else -1,g["source_identity"]))
    over=[g for g in groups if len(g["blob"])>64]
    final=[format_group(g) for g in groups]
    post_over=[g for g in final if int(g["emitted_bytes"])>64]
    legacy=Path(a.legacy_summary).read_text(encoding="utf-8")
    match=re.search(r"INITIAL_LABELED_GROUPS_OVER_64B=(\d+)",legacy)
    if not match:raise SystemExit("UE0_LEGACY_GROUP_COUNT_MISSING")
    legacy_labeled=int(match.group(1))
    pc_labeled=sum(1 for g in over if g["kind"]=="PC" and not g["label"].startswith("UNRESOLVED:"))
    file_labeled=sum(1 for g in over if g["kind"]=="FILE_OFFSET" and not g["label"].startswith("UNRESOLVED:"))
    no_pc_labeled=sum(1 for g in over if g["kind"]=="NO_PC" and not g["label"].startswith("UNRESOLVED:"))
    unresolved_over=sum(1 for g in over if g["label"].startswith("UNRESOLVED:"))
    unresolved_all=sum(1 for g in groups if g["label"].startswith("UNRESOLVED:"))
    header=["label","label_status","label_reason","kind","start","end_exclusive","original_bytes","emitted_bytes",
      "pruned_bytes","source_identity","source_count","source_rows_count","sources_sample","source_rows_sample",
      "byte_payload","action"]
    def write(name,fields,rows):
        with (out/name).open("w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
            w.writeheader();w.writerows(rows)
    write("UE0_UNION_GROUPS.tsv",header,final)
    pruned_rows=[format_group(g) for g in over]
    write("UE0_PRUNED_GROUPS.tsv",header,pruned_rows)
    write("UE0_UNRESOLVED_GROUPS.tsv",header,[format_group(g) for g in groups if g["label"].startswith("UNRESOLVED:")])
    write("UE0_UNRESOLVED_OVER_64B_GROUPS.tsv",header,[format_group(g) for g in over if g["label"].startswith("UNRESOLVED:")])
    write("UE0_OVER_64B_GROUPS.tsv",header,post_over)
    with (out/"UE0_PRUNED_GROUPS.tsv").open("r",encoding="utf-8",newline="") as f:
        registered=sum(1 for _ in csv.DictReader(f,delimiter="\t"))
    unregistered=max(0,len(over)-registered)
    write("UE0_SOURCE_MANIFEST.tsv",["source","byte_columns","pc_column","offset_column","rows"],manifest)
    badrows=[]
    for (source,col),count in sorted(malformed.items()):
        badrows.append({"source":source,"field":col,"malformed_cells":count,
                        "sample_lines":";".join(map(str,malformed_sample[(source,col)]))})
    write("UE0_MALFORMED_SUMMARY.tsv",["source","field","malformed_cells","sample_lines"],badrows)
    frows=[]
    for col in BYTE_COLUMNS:
        frows.append({"byte_column":col,"cells_seen":field_counts[col],"valid_cells":valid[col],
                      "unknown_cells":unknown[col],"malformed_cells":sum(n for (s,c),n in malformed.items() if c==col)})
    write("UE0_FIELD_COUNTS.tsv",["byte_column","cells_seen","valid_cells","unknown_cells","malformed_cells"],frows)
    reconciliation="PASS" if legacy_labeled==18 and pc_labeled==31 else "NOT_RECONCILED"
    lines=["UE0_IMMUTABLE_BASELINE_BYTE_UNION",f"BASELINE_INCLUSIVE={a.baseline}",
      f"BASELINE_TSV_FILES={file_count}",f"BYTE_FIELDS_SCANNED={sum(field_counts.values())}",
      "BYTE_COLUMNS_INCLUDED=bytes;instruction_bytes;bytes_or_excerpt_hex;bytes_excerpt_hex_max64;contiguous_bytes",
      f"LEGACY_LABELED_GROUPS_OVER_64B={legacy_labeled}",f"EXPANDED_PC_LABELED_GROUPS_OVER_64B={pc_labeled}",
      f"EXPANDED_FILE_OFFSET_LABELED_GROUPS_OVER_64B={file_labeled}",
      f"EXPANDED_NO_PC_LABELED_GROUPS_OVER_64B={no_pc_labeled}",
      f"EXPANDED_UNRESOLVED_GROUPS_OVER_64B={unresolved_over}",f"EXPANDED_ALL_GROUPS_OVER_64B={len(over)}",
      f"RECONCILIATION_DELTA_PC_GROUPS={pc_labeled-legacy_labeled}",f"RECONCILIATION_18_VS_31={reconciliation}",
      f"UNRESOLVED_GROUPS_TOTAL={unresolved_all}",f"PRUNED_GROUPS_REGISTERED={registered}",
      f"UNRESOLVED_GROUPS_PRUNED_AND_REGISTERED={unresolved_over}",
      f"POST_PRUNE_GROUPS_OVER_64B={len(post_over)}",f"UNREGISTERED_OVER_64B_GROUPS={unregistered}",
      f"NO_PC_ROWS={len(no_pc)}",f"BYTE_CONFLICTS={conflicts}",f"MALFORMED_SOURCE_FIELD_PAIRS={len(malformed)}",
      "UNKNOWN_TOKEN_POLICY=TIDAK TAHU/UNKNOWN/N/A/NA/NONE/NULL/- are not bytes",
      "LABEL_POLICY=explicit image metadata, source/path context, unique file-offset range, then unique PC image range",
      "UNRESOLVED_POLICY=preserve per-source TSV identity; unresolved groups are not merged across files",
      "NO_PC_POLICY=every valid byte cell without PC or file offset is retained as its own source-row group",
      "PRUNE_POLICY=every group longer than 64 bytes is clipped to a 64-byte metadata span and registered; no byte payload is published",
      "OUTPUT_BYTE_EXCERPTS=0; aggregate quoted-byte budget 64B not consumed",
      "SOURCE_POLICY=baseline worktree read-only; no source TSV modified/deleted",
      f"STATUS={'PASS' if not post_over and not unregistered else 'FAIL'}",
      f"EXIT_CODE={1 if post_over or unregistered else 0}"]
    (out/"UE0_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines))
    return 1 if post_over or unregistered else 0
if __name__=="__main__":raise SystemExit(main())
