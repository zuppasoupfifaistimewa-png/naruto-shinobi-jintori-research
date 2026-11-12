#!/usr/bin/env python3
"""UN1: recompute X/LV and compare two saved frame-1 byte snapshots."""
from __future__ import annotations
import argparse,csv
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BYTES=ROOT/"reports/ui-audit-2026-11-12/um/run-43211668588/attempt-1/UM1/UM1_BYTES.tsv"
TABLE=ROOT/"reports/stage1_economy/DN1_DK1_X_LV_TABLE_2026-11-05.tsv"
RECORDS=tuple([f"A:{i}" for i in range(23)]+["A:43"])
OUT_FIELDS=["launch","record","X_u16_0E","LV1_u16_10","LV2_u16_12","LV3_u16_14","LV4_u16_16","LV5_u16_18","u16_1A","u16_1C","u16_1E","u16_00","u16_20","DN1_X_MATCH","DN1_LV_MATCH","ratio_1C_over_1A","ratio_1E_over_1C"]
PAIR_FIELDS=["X_u16_0E","u16_1A","record_count","records"]
RATIO_FIELDS=["ratio_type","ratio","record_count","records"]
COMPARE_FIELDS=["record","MEASURE_1_X","MEASURE_2_X","X_equal","LV1_LV5_equal","selected_fields_equal","all_0x124_bytes_equal","mismatch_offsets"]
SUMMARY_FIELDS=["item","value"]
def read(path):
    with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f,delimiter="\t"))
def write(path,fields,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n");w.writeheader();w.writerows(rows)
def u16(b,o):return b[o]|(b[o+1]<<8)
def ratio(a,b):return f"{float(Fraction(a,b)):.6f}" if b else "TIDAK TERDEFINISI"
def pack(rows):
    result={}
    for r in rows:
        k=(r["launch"],r["record"]);o=int(r["offset"],16);v=int(r["byte_hex"],16)
        if o in result.setdefault(k,{}):raise ValueError(f"duplicate_byte_{k}_{o:x}")
        result[k][o]=v
    return result
def self_test():
    assert u16({0x0e:0x34,0x0f:0x12},0x0e)==0x1234
    assert ratio(35,50)=="0.700000" and ratio(84,70)=="1.200000"
    print("UN1_SELF_TEST=PASS little-endian u16, ratios, offset selection")
def main():
    p=argparse.ArgumentParser();p.add_argument("--bytes",type=Path,default=BYTES);p.add_argument("--table",type=Path,default=TABLE);p.add_argument("--out-dir",type=Path);p.add_argument("--self-test",action="store_true");a=p.parse_args()
    if a.self_test:self_test();return 0
    if not a.out_dir:p.error("--out-dir required")
    raw=read(a.bytes);dnrows=read(a.table);dn={int(r["X"]):[int(r[f"LV{i}"]) for i in range(1,6)] for r in dnrows}
    grouped=pack([r for r in raw if r["frame"]=="1"]);launches=sorted({k[0] for k in grouped})
    if not {"MEASURE_1","MEASURE_2"}.issubset(set(launches)):raise SystemExit("UN1_TWO_MEASURE_LAUNCHES_MISSING")
    if len(grouped)!=48:raise SystemExit(f"UN1_FRAME1_RECORDS_EXPECTED_48_GOT_{len(grouped)}")
    output=[];by={}
    for launch in ("MEASURE_1","MEASURE_2"):
        by[launch]={}
        for record in RECORDS:
            b=grouped.get((launch,record))
            if b is None or set(b)!=set(range(0x124)):raise ValueError(f"incomplete_{launch}_{record}")
            v={"X_u16_0E":u16(b,0x0e),"u16_1A":u16(b,0x1a),"u16_1C":u16(b,0x1c),"u16_1E":u16(b,0x1e),"u16_00":u16(b,0),"u16_20":u16(b,0x20)}
            lv=[u16(b,o) for o in (0x10,0x12,0x14,0x16,0x18)]
            for i,value in enumerate(lv,1):v[f"LV{i}_u16_{(0x0e+2*i):02X}"]=value
            table=dn.get(v["X_u16_0E"])
            v["DN1_X_MATCH"]="YES" if table is not None else "NO"
            v["DN1_LV_MATCH"]="YES" if table==lv else "NO"
            v["ratio_1C_over_1A"]=ratio(v["u16_1C"],v["u16_1A"])
            v["ratio_1E_over_1C"]=ratio(v["u16_1E"],v["u16_1C"])
            by[launch][record]=v;output.append({"launch":launch,"record":record,**v})
    pairs=Counter((r["X_u16_0E"],r["u16_1A"]) for r in output);pair_rows=[]
    for (x,a1),n in sorted(pairs.items()):
        pair_rows.append({"X_u16_0E":x,"u16_1A":a1,"record_count":n,"records":";".join(r["launch"]+"/"+r["record"] for r in output if r["X_u16_0E"]==x and r["u16_1A"]==a1)})
    ratio_rows=[]
    for typ,key in (("1C/1A","ratio_1C_over_1A"),("1E/1C","ratio_1E_over_1C")):
        c=Counter(r[key] for r in output if r[key]!="TIDAK TERDEFINISI")
        for val,n in sorted(c.items()):
            ratio_rows.append({"ratio_type":typ,"ratio":val,"record_count":n,"records":";".join(r["launch"]+"/"+r["record"] for r in output if r[key]==val)})
    comparisons=[]
    for record in RECORDS:
        b1=grouped[("MEASURE_1",record)];b2=grouped[("MEASURE_2",record)]
        mism=[f"0x{o:03X}" for o in range(0x124) if b1[o]!=b2[o]]
        x1=by["MEASURE_1"][record];x2=by["MEASURE_2"][record]
        lvkeys=[f"LV{i}_u16_{(0x0e+2*i):02X}" for i in range(1,6)]
        same_x=x1["X_u16_0E"]==x2["X_u16_0E"]
        same_lv=all(x1[k]==x2[k] for k in lvkeys)
        fields=("X_u16_0E","u16_1A","u16_1C","u16_1E","u16_00","u16_20")
        same_selected=all(x1[k]==x2[k] for k in fields)
        comparisons.append({"record":record,"MEASURE_1_X":x1["X_u16_0E"],"MEASURE_2_X":x2["X_u16_0E"],"X_equal":"YES" if same_x else "NO","LV1_LV5_equal":"YES" if same_lv else "NO","selected_fields_equal":"YES" if same_selected else "NO","all_0x124_bytes_equal":"YES" if not mism else "NO","mismatch_offsets":";".join(mism)})
    dnmatched=sum(r["DN1_X_MATCH"]=="YES" and r["DN1_LV_MATCH"]=="YES" for r in output)
    selected=sum(r["selected_fields_equal"]=="YES" and r["LV1_LV5_equal"]=="YES" for r in comparisons)
    full=sum(r["all_0x124_bytes_equal"]=="YES" for r in comparisons)
    k5=dnmatched==48 and selected==24
    status="TUNTAS" if k5 else "SEBAGIAN"
    summary=[("STATUS",status),("OBSERVATION_EVIDENCE","K5" if k5 else "K2"),("RELATIONSHIP_EVIDENCE","K2; associations do not assign field meanings"),("FRAME1_RECORDS",len(output)),("RECORDS_PER_LAUNCH",24),("LAUNCHES","MEASURE_1;MEASURE_2"),("X_AND_LV1_LV5_DN1_MATCH",f"{dnmatched}/48"),("SELECTED_FIELDS_AND_LV_CROSS_LAUNCH_MATCH",f"{selected}/24"),("FULL_0x124_RECORD_BYTES_EQUAL",f"{full}/24"),("UNIQUE_X_PLUS_1A_PAIRS",len(pairs)),("VALID_1C_OVER_1A_RECORDS",sum(r["u16_1A"]!=0 for r in output)),("UNIQUE_1C_OVER_1A_RATIOS",len({r["ratio_1C_over_1A"] for r in output if r["ratio_1C_over_1A"]!="TIDAK TERDEFINISI"})),("VALID_1E_OVER_1C_RECORDS",sum(r["u16_1C"]!=0 for r in output)),("UNIQUE_1E_OVER_1C_RATIOS",len({r["ratio_1E_over_1C"] for r in output if r["ratio_1E_over_1C"]!="TIDAK TERDEFINISI"})),("X_DEFINITION","X=u16(+0x0E); X=2*u16(+0x1A) is withdrawn"),("FIELD_MEANING","TIDAK TAHU")]
    out=a.out_dir;write(out/"UN1_RECORDS.tsv",OUT_FIELDS,output);write(out/"UN1_UNIQUE_X_1A.tsv",PAIR_FIELDS,pair_rows);write(out/"UN1_RATIOS.tsv",RATIO_FIELDS,ratio_rows);write(out/"UN1_MEASURE_COMPARISON.tsv",COMPARE_FIELDS,comparisons);write(out/"UN1_SUMMARY.tsv",SUMMARY_FIELDS,[{"item":k,"value":v} for k,v in summary])
    print(f"UN1_{status} K5={k5} DN1={dnmatched}/48 selected={selected}/24 full={full}/24 pairs={len(pairs)}")
    return 0 if k5 else 2
if __name__=="__main__":raise SystemExit(main())
