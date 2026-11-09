#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, io, json, re, subprocess, sys
from collections import defaultdict
from pathlib import Path

LIMIT=64
FIXED_TRIMS=(
    ("ENTRY1",0x800D77C4,0x800D77C8),
    ("ENTRY1",0x800D7D4C,0x800D7D50),
    ("ENTRY1",0x800F5DCC,0x800F5DD0),
    # The BE5D8 manual excerpt begins four bytes before its function entry.
    # Remove only that pre-entry word; preserve the complete eight-byte prolog.
    ("ENTRY1",0x800BE5BC,0x800BE5C0),
    ("EXE",0x80011A1C,0x80011A28),
)
PROTECTED=(
    ("EXE",0x80011A28,0x80011A68),
    ("ENTRY1",0x800B50AC,0x800B50B4),
    ("ENTRY1",0x800BE5D8,0x800BE5E0),
)

def norm_image(value):
    raw=(value or "").strip().upper()
    compact=re.sub(r"[^A-Z0-9]","",raw)
    if "ENTRY1" in compact:
        return "ENTRY1"
    if compact in {"EXE","SLPS03553","SLPS03553EXE"} or "SLPS03553" in compact:
        return "EXE"
    return None

def parse_pc(value):
    return int(str(value).strip(),16)

def parse_payload(value):
    tokens=str(value).split()
    if not tokens or any(not re.fullmatch(r"[0-9A-Fa-f]{2}",x) for x in tokens):
        raise ValueError("BYTES_NOT_TWO_DIGIT_HEX_TOKENS")
    return bytes(int(x,16) for x in tokens)

def write_tsv(path, fields, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.writer(stream,delimiter="\t",lineterminator="\n")
        writer.writerow(fields)
        writer.writerows(rows)

def evidence_paths(stage,new_output):
    paths=set(p for p in stage.rglob("*.tsv") if p.is_file())
    if new_output and new_output.exists():
        # Only UB1 is the new byte-evidence deliverable for this run.
        # LA1-LA5/UA1 outputs already exist in the historical archive and
        # are deliberately not republished as duplicate current-run excerpts.
        paths.update(p for p in new_output.rglob("UB1*.tsv") if p.is_file())
    return sorted(paths,key=lambda p:str(p))

def scan(paths,root,new_output):
    rows=[]
    malformed=[]
    ignored=0
    for path in paths:
        try:
            with path.open("r",encoding="utf-8-sig",newline="") as stream:
                reader=csv.DictReader(stream,delimiter="\t")
                names={str(k).strip().lower():k for k in (reader.fieldnames or [])}
                if not {"image","pc","bytes"}.issubset(names):
                    continue
                for line,row in enumerate(reader,start=2):
                    raw_image=(row.get(names["image"]) or "").strip()
                    image=norm_image(raw_image)
                    if image is None:
                        ignored+=1
                        continue
                    pc_text=(row.get(names["pc"]) or "").strip()
                    bytes_text=(row.get(names["bytes"]) or "").strip()
                    # TIDAK TAHU is an explicit unresolved placeholder, not malformed byte evidence.
                    if "TIDAK TAHU" in pc_text.upper() or "TIDAK TAHU" in bytes_text.upper():
                        ignored+=1
                        continue
                    try:
                        pc=parse_pc(pc_text)
                        payload=parse_payload(bytes_text)
                    except Exception as exc:
                        malformed.append([display_path(path,root,new_output),line,image,
                                          row.get(names["pc"]) or "",row.get(names["bytes"]) or "",
                                          type(exc).__name__+":"+str(exc)])
                        continue
                    rows.append((path,line,image,pc,payload))
        except Exception as exc:
            malformed.append([display_path(path,root,new_output),"FILE","TIDAK TAHU","","",
                              type(exc).__name__+":"+str(exc)])
    return rows,malformed,ignored

def display_path(path,root,new_output):
    try:
        return path.relative_to(root).as_posix()
    except Exception:
        try:
            return "CURRENT_OUTPUT/"+path.relative_to(new_output).as_posix()
        except Exception:
            return str(path)

def overlaps(a,b,c,d):
    return a<d and a+c>b

def protected(image,pc,size):
    return any(image==label and pc<end and pc+size>start
               for label,start,end in PROTECTED)

def is_protected_new_evidence(path,new_output):
    if not new_output:
        return False
    try:
        if not (path==new_output or new_output in path.parents):
            return False
    except Exception:
        return False
    # UB1 rows are the requested new static evidence and are never auto-pruned.
    # UB3 files are ledgers/status, not excerpt sources, and are kept intact.
    return path.name.startswith(("UB1_","UB3_"))

def remove_gap(paths,root,new_output,image,start,end,reason,allow_new=False):
    removed=[]
    guards=[]
    changed=[]
    for path in paths:
        is_new=bool(new_output and (path==new_output or new_output in path.parents))
        if is_new and not allow_new:
            continue
        try:
            raw=path.read_bytes()
            bom=raw.startswith(b"\xef\xbb\xbf")
            source=raw.decode("utf-8-sig")
            physical=source.splitlines(keepends=True)
            reader=csv.reader(io.StringIO(source,newline=""),delimiter="\t")
            header=next(reader)
        except (UnicodeDecodeError,csv.Error,StopIteration):
            continue
        hm={str(name).strip().lower():i for i,name in enumerate(header)}
        if not {"image","pc","bytes"}.issubset(hm):
            continue
        cursor=reader.line_num
        kept=physical[:cursor]
        count=0
        for cells in reader:
            line_end=reader.line_num
            record=physical[cursor:line_end]
            cursor=line_end
            try:
                if len(cells)<=max(hm["image"],hm["pc"],hm["bytes"]):
                    kept.extend(record);continue
                label=norm_image(cells[hm["image"]])
                pc=parse_pc(cells[hm["pc"]])
                payload=parse_payload(cells[hm["bytes"]])
            except Exception:
                kept.extend(record);continue
            if label!=image or not (pc<end and pc+len(payload)>start):
                kept.extend(record);continue
            if protected(label,pc,len(payload)):
                guards.append([display_path(path,root,new_output),line_end,label,
                               f"0x{pc:08X}",len(payload),f"0x{start:08X}-0x{end-1:08X}"])
                kept.extend(record);continue
            removed.append([display_path(path,root,new_output),line_end,label,
                            f"0x{pc:08X}",len(payload),f"0x{start:08X}-0x{end-1:08X}",reason])
            count+=1
        if cursor<len(physical):
            kept.extend(physical[cursor:])
        if count:
            out="".join(kept).encode("utf-8")
            if bom:
                out=b"\xef\xbb\xbf"+out
            path.write_bytes(out)
            changed.append(path)
    tracked=[p for p in changed if p.is_relative_to(root)]
    if tracked:
        subprocess.run(["git","add","--",*[p.relative_to(root).as_posix() for p in tracked]],
                       cwd=root,check=True)
    return removed,guards

def union(rows):
    values={}
    origins=defaultdict(list)
    conflicts=set()
    for path,line,image,pc,payload in rows:
        for offset,byte in enumerate(payload):
            key=(image,pc+offset)
            old=values.get(key)
            if old is not None and old!=byte:
                conflicts.add(key)
            else:
                values[key]=byte
            origins[key].append((path,line,pc,len(payload)))
    grouped=defaultdict(list)
    for image,address in values:
        grouped[image].append(address)
    spans=[]
    for image,addresses in grouped.items():
        addresses.sort()
        if not addresses:
            continue
        first=previous=addresses[0]
        for address in addresses[1:]:
            if address!=previous+1:
                spans.append((image,first,previous+1))
                first=address
            previous=address
        spans.append((image,first,previous+1))
    return values,origins,conflicts,sorted(spans)

def auto_trim(paths,root,new_output,audit_rows,guard_rows):
    iterations=0
    failures=[]
    while iterations<2048:
        iterations+=1
        rows,malformed,_=scan(paths,root,new_output)
        values,origins,conflicts,spans=union(rows)
        over=[(image,start,end) for image,start,end in spans if end-start>LIMIT]
        if not over:
            return iterations-1,failures,malformed,conflicts,spans
        image,start,end=over[0]
        upper=min(start+LIMIT,end-4)
        selected=None
        for gap in range(upper,start-1,-4):
            if (gap-start)%4:
                continue
            refs=set()
            for address in range(gap,gap+4):
                refs.update(origins.get((image,address),[]))
            if not refs:
                continue
            # Never cut current-run UB1/UB3 evidence to make the gate appear green.
            if any(is_protected_new_evidence(p,new_output) for p,_,_,_ in refs):
                continue
            if any(protected(image,row_pc,row_size) for _,_,row_pc,row_size in refs):
                continue
            selected=gap
            break
        if selected is None:
            failures.append([image,f"0x{start:08X}",f"0x{end:08X}",end-start,
                             "NO_SAFE_ARCHIVE_GAP;CURRENT_OUTPUT_AND_PROTECTED_ROWS_RETAINED"])
            return iterations,failures,malformed,conflicts,spans
        removed,guards=remove_gap(paths,root,new_output,image,selected,selected+4,
                                  "AUTO_UNION_4B_GAP",allow_new=True)
        audit_rows.extend(removed)
        guard_rows.extend(guards)
        if not removed:
            failures.append([image,f"0x{start:08X}",f"0x{end:08X}",end-start,
                             f"NO_ARCHIVE_ROWS_REMOVED_AT_0x{selected:08X}"])
            return iterations,failures,malformed,conflicts,spans
    failures.append(["TIDAK TAHU","","","", "ITERATION_LIMIT_2048"])
    rows,malformed,_=scan(paths,root,new_output)
    values,origins,conflicts,spans=union(rows)
    return iterations,failures,malformed,conflicts,spans

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",required=True,type=Path)
    parser.add_argument("--new-output",required=True,type=Path)
    parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args()
    root=args.root.resolve()
    stage=root/"reports"/"stage1_economy"
    new_output=args.new_output.resolve()
    out=args.out.resolve()
    out.mkdir(parents=True,exist_ok=True)
    audit=[]
    guards=[]
    fixed_fail=[]
    # The fixed four edge trims apply only to already-published archive evidence.
    archive_paths=sorted((p for p in stage.rglob("*.tsv") if p.is_file()),key=lambda p:str(p))
    for image,start,end in FIXED_TRIMS:
        removed,blocked=remove_gap(archive_paths,root,new_output,image,start,end,
                                   "FIXED_EDGE_TRIM",allow_new=False)
        audit.extend(removed)
        guards.extend(blocked)
        if blocked:
            fixed_fail.extend(blocked)
    paths=evidence_paths(stage,new_output)
    iterations,auto_fail,malformed,conflicts,spans=auto_trim(
        paths,root,new_output,audit,guards)
    # Final independent pass after all edits.
    paths=evidence_paths(stage,new_output)
    rows,malformed,ignored=scan(paths,root,new_output)
    values,origins,conflicts,spans=union(rows)
    over=[(im,st,en,en-st) for im,st,en in spans if en-st>LIMIT]
    write_tsv(out/"LA0_ARCHIVE_UNION_TRIM.tsv",
              ["source_file","source_line_end","image","pc","byte_count","trim_range","reason"],audit)
    write_tsv(out/"LA0_ARCHIVE_UNION_GUARDS.tsv",
              ["source_file","source_line_end","image","pc","byte_count","protected_range"],guards)
    write_tsv(out/"LA0_ARCHIVE_UNION_SPANS.tsv",
              ["image","start_pc","end_pc_exclusive","contiguous_bytes"],
              [[im,f"0x{st:08X}",f"0x{en:08X}",en-st] for im,st,en in spans])
    write_tsv(out/"LA0_ARCHIVE_UNION_OVERLIMIT.tsv",
              ["image","start_pc","end_pc_exclusive","contiguous_bytes"],
              [[im,f"0x{st:08X}",f"0x{en:08X}",n] for im,st,en,n in over])
    write_tsv(out/"LA0_ARCHIVE_UNION_MALFORMED.tsv",
              ["source_file","source_line","image","pc","bytes","reason"],malformed)
    summary=[
      "STATUS="+("PASS" if not (over or conflicts or malformed or guards or auto_fail or fixed_fail) else "FAIL"),
      "LIMIT_BYTES=64",
      "SCANNED_TSV_FILES="+str(len(paths)),
      "ELIGIBLE_BYTE_TSV_FILES="+str(len({r[0] for r in rows})),
      "VALID_BYTE_ROWS="+str(len(rows)),
      "UNIQUE_BYTE_ADDRESSES="+str(len(values)),
      "UNION_MAX_CONTIGUOUS_BYTES="+str(max((en-st for _,st,en in spans),default=0)),
      "UNION_OVER_64_GROUPS="+str(len(over)),
      "BYTE_OVERLAP_CONFLICT_ADDRESSES="+str(len(conflicts)),
      "MALFORMED_BYTE_ROWS="+str(len(malformed)),
      "FIXED_EDGE_TRIM_ROWS="+str(sum(1 for r in audit if r[-1]=="FIXED_EDGE_TRIM")),
      "AUTO_UNION_TRIM_ROWS="+str(sum(1 for r in audit if r[-1]=="AUTO_UNION_4B_GAP")),
      "AUTO_UNION_ITERATIONS="+str(iterations),
      "PROTECTED_WINDOW_INTERSECTIONS="+str(len(guards)),
      "UNRESOLVED_OR_UNKNOWN_ROWS_IGNORED="+str(ignored),
      "F5DCC_FIXED_TRIM_ROWS="+str(sum(1 for r in audit if r[2]=="ENTRY1" and r[5]=="0x800F5DCC-0x800F5DCF")),
      "CURRENT_OUTPUT_EVIDENCE_CUT=NO",
      "STATUS_MD_MODIFIED=NO",
      "RELEASES_MODIFIED=NO",
      "BINARY_OUTPUT=NONE",
    ]
    if auto_fail:
        summary.append("AUTO_TRIM_FAILURES="+json.dumps(auto_fail,sort_keys=True))
    if fixed_fail:
        summary.append("FIXED_TRIM_FAILURES="+json.dumps(fixed_fail,sort_keys=True))
    (out/"LA0_ARCHIVE_UNION_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary))
    if over or conflicts or malformed or guards or auto_fail or fixed_fail:
        raise SystemExit(1)

if __name__=="__main__":
    main()
