#!/usr/bin/env python3
"""AW1 summarizer for the AQ1/AS1 record-field displacement census."""
import argparse,csv,collections
FIELDS=["+0x0B"]+[f"+0x{x:02X}" for x in range(0x10,0x30,2)]
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--census",required=True);ap.add_argument("--output",required=True);a=ap.parse_args()
    with open(a.census,encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f,delimiter="\t"))
    groups=collections.defaultdict(lambda:{"READ":set(),"WRITE":set(),"OTHER":set(),"pcs":collections.defaultdict(list)})
    rawcounts=collections.Counter()
    for r in rows:
        if r.get("record_type")!="FIELD":continue
        field=r.get("item","");kind=r.get("kind","")
        if field not in FIELDS:continue
        name=r.get("function_name","TIDAK TAHU");entry=r.get("function_entry","TIDAK TAHU")
        key=(field,entry,name);groups[key][kind].add(r.get("pc_or_target",""))
        groups[key]["pcs"][kind].append(r.get("pc_or_target",""))
        rawcounts[(field,kind)]+=1
    with open(a.output,"w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,delimiter="\t")
        w.writerow(["field","function_entry","function_name","access_kinds","read_pcs","write_pcs","other_pcs","base_alias_status"])
        for (field,entry,name),g in sorted(groups.items()):
            kinds=[k for k in ("READ","WRITE","OTHER") if g[k]]
            w.writerow([field,entry,name,";".join(kinds),";".join(sorted(g["pcs"]["READ"])),";".join(sorted(g["pcs"]["WRITE"])),";".join(sorted(g["pcs"]["OTHER"])),"DISPLACEMENT_ONLY_BASE_REGISTER_NOT_PROVEN"])
    print("AW1_FIELD_INVENTORY=PASS distinct_function_field_rows="+str(len(groups)))
    for field in FIELDS:
        parts=[f"{k}={rawcounts[(field,k)]}" for k in ("READ","WRITE","OTHER") if rawcounts[(field,k)]]
        if parts: print(field+" "+ " ".join(parts))
if __name__=="__main__":main()
