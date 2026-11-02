#!/usr/bin/env python3
"""Inventory DATA.BIN resources and find 22-record Stage 1 tile-table candidates.
No source binary is ever written to the repository or an Actions artifact.
"""
import argparse,csv,hashlib,struct
from pathlib import Path

DATA_SHA="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
DATA_SIZE=66015232
LBN_BASE=212
TABLE_OFF=0x44
ENTRY_COUNT=1504
STRIDE=0x1E
KNOWN_LEVELS=(60,140,265,530)
PRICE=120

def sha(b): return hashlib.sha256(b).hexdigest()
def u16(b,o): return struct.unpack_from("<H",b,o)[0]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data",required=True)
    ap.add_argument("--out-dir",required=True)
    a=ap.parse_args()
    data=Path(a.data).read_bytes()
    if len(data)!=DATA_SIZE or sha(data)!=DATA_SHA:
        raise SystemExit(f"DATA.BIN identity mismatch: bytes={len(data)} sha={sha(data)}")
    table=data[TABLE_OFF:TABLE_OFF+ENTRY_COUNT*8]
    entries=[struct.unpack_from("<II",table,i*8) for i in range(ENTRY_COUNT)]
    out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=True)
    inventory=[];candidates=[]
    for idx,(lbn,length) in enumerate(entries):
        if length==0:
            inventory.append({"index":idx,"lbn":lbn,"length":0,"offset":"NA","sha256":"NA","magic":"EMPTY","record30_aligned":"NO","record22_candidate":"NO"})
            continue
        off=(lbn-LBN_BASE)*2048
        chunk=data[off:off+length]
        if len(chunk)!=length or off<0 or off+length>len(data):
            raise SystemExit(f"resource bounds invalid index={idx}")
        magic=chunk[:16].hex(" ").upper()
        aligned=(length%STRIDE==0)
        hit_desc=[]
        # The known source +0x14 -> runtime +0x1A mapping is fixed by FUN_800F7ADC.
        # The +0x10..+0x16 source correspondence remains a candidate until the loader map is closed.
        # Search 22-record windows at each 0x1E boundary; do not label any hit as proof by itself.
        for start in range(0,max(0,length-22*STRIDE+1),STRIDE):
            hits=[]
            for rec in range(22):
                base=start+rec*STRIDE
                if base+0x16>len(chunk): break
                if (u16(chunk,base+0x0A),u16(chunk,base+0x0C),u16(chunk,base+0x0E),u16(chunk,base+0x10),u16(chunk,base+0x14))==(60,140,265,530,120):
                    hits.append(rec)
            if hits:
                hit_desc.append(f"start=0x{start:X};matching_record_indices={','.join(map(str,hits))}")
                candidates.append({"index":idx,"lbn":lbn,"length":length,"offset":f"0x{off:X}","resource_sha256":sha(chunk),
                                   "table_start":f"0x{start:X}","matching_records":",".join(map(str,hits)),
                                   "basis":"candidate source fields +0x0A/+0x0C/+0x0E/+0x10/+0x14; validate against FUN_800F7ADC"})
        inventory.append({"index":idx,"lbn":lbn,"length":length,"offset":f"0x{off:X}","sha256":sha(chunk),
                          "magic":magic,"record30_aligned":"YES" if aligned else "NO",
                          "record22_candidate":"YES" if hit_desc else "NO"})
    with (out/"BA1_DATA_BIN_RESOURCE_INVENTORY.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(inventory[0]),delimiter="\t");w.writeheader();w.writerows(inventory)
    with (out/"BA1_RESOURCE_CANDIDATES.tsv").open("w",encoding="utf-8",newline="") as f:
        cols=("index","lbn","length","offset","resource_sha256","table_start","matching_records","basis")
        w=csv.DictWriter(f,fieldnames=cols,delimiter="\t");w.writeheader();w.writerows(candidates)
    (out/"BA1_DATA_SCAN_SUMMARY.txt").write_text(
        "STATUS=PASS\n"
        f"data_bytes={len(data)}\n"
        f"data_sha256={sha(data)}\n"
        f"directory_entries={len(entries)}\n"
        f"active_entries={sum(1 for x in entries if x[1])}\n"
        f"zero_length_entries={sum(1 for x in entries if not x[1])}\n"
        f"resource_candidates_with_known_value_pattern={len(candidates)}\n"
        "pattern_status=HYPOTHESIS_ONLY_UNTIL_SOURCE_TO_RUNTIME_MAP_IS_CONFIRMED\n"
        "record_stride_source=0x1E\n"
        "runtime_record_stride=0x124\n"
        "known_mapping=source+0x14/+0x15 -> runtime tile+0x1A (from FUN_800F7ADC static report)\n",
        encoding="utf-8")
    print(f"BA1_DATA_SCAN=PASS active={sum(1 for x in entries if x[1])} candidates={len(candidates)}")
if __name__=="__main__": main()
