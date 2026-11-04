#!/usr/bin/env python3
import argparse,csv,hashlib,math,struct
from collections import defaultdict
from pathlib import Path
DATA_SHA="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
DATA_SIZE=66015232; STRIDE=0x1e
NS={0x276:22,0x277:33,0x278:33,0x279:34,0x27a:33,0x27b:43,0x27c:38,0x27e:22,0x27f:38,0x285:43,0x286:36,0x287:40}
OBS={120:[60,140,265,530,1050],180:[90,200,390,800,1600],200:[100,220,440,880,1760],
220:[110,250,490,980,1940],240:[120,270,530,1050,2120],280:[140,310,620,1240,2470]}
def H(x): return f"0x{x:X}"
def U(b,o): return struct.unpack_from("<H",b,o)[0]
def sha(b): return hashlib.sha256(b).hexdigest()
def write(p,rows):
 with p.open("w",encoding="utf-8",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(rows)
def main():
 a=argparse.ArgumentParser();a.add_argument("--data",required=True);a.add_argument("--out-dir",required=True);z=a.parse_args()
 d=Path(z.data).read_bytes();o=Path(z.out_dir);o.mkdir(parents=True,exist_ok=True)
 if len(d)!=DATA_SIZE or sha(d)!=DATA_SHA: raise SystemExit("DATA_BIN_IDENTITY_FAIL")
 directory=[struct.unpack_from("<II",d,0x44+i*8) for i in range(1504)]
 res={}; records=[]
 for rid,n in NS.items():
  lbn,size=directory[rid]; off=(lbn-212)*2048
  if size<=0 or off<0 or off+size>len(d): raise SystemExit(f"RESOURCE_BOUNDS_FAIL_{rid:X}")
  b=d[off:off+size]; digest=sha(b); header=b[0]; rows=[]; good=0; blanks=0
  for i in range(n):
   q=1+i*STRIDE
   if q+0x1e>len(b): break
   X=U(b,q+0x0e); lv=[U(b,q+x) for x in (0x10,0x12,0x14,0x16,0x18)]
   blank=X==0 and not any(lv); blanks+=int(blank)
   plausible=X<=4095 and all(v<=10000 for v in lv) and all(lv[j]<=lv[j+1] for j in range(4)) and (blank or (X>0 and lv[0]>0))
   good+=int(plausible)
   cross=U(b,q+0x1e) if q+0x20<=len(b) else ""
   r={"resource_id_hex":H(rid),"record_index":i,"X":X,**{f"LV{j+1}":lv[j] for j in range(5)},
      "plus_0x1A":U(b,q+0x1a),"plus_0x1C":U(b,q+0x1c),
      "plus_0x1E_cross_boundary_u16":cross,
      "plus_0x1E_status":"EOF_OUT_OF_RANGE" if cross=="" else "CROSSES_RECORD_BOUNDARY",
      "resource_data_bin_offset":H(off),"record_data_bin_offset":H(off+q),
      "record_resource_offset":H(q),"resource_size_bytes":size,
      "header_first_byte":header,"expected_N":n,"resource_sha256":digest,
      "_vector":tuple(lv),"_good":plausible}
   rows.append(r);records.append(r)
  sizeok=size==1+n*STRIDE; headok=header==n
  if not sizeok or not headok:
   status="LAYOUT_BERBEDA"; reason=f"size={size}/{1+n*STRIDE}; header={header}/{n}"
  elif rows and good/len(rows)>=.9:
   status="LAYOUT_SAMA";reason=f"size=1+{n}*0x1E; header={header}=N; plausible={good}/{len(rows)}"
  else: status="TIDAK_JELAS";reason=f"size/header match; plausible={good}/{len(rows)}"
  res[rid]={"n":n,"size":size,"off":off,"sha":digest,"header":header,"good":good,"blanks":blanks,"rows":rows,"status":status,"reason":reason}
 # Historical commit ledger; cutoff inclusive.
 ledger=[
 {"commit_sha":"b81db45b4ac13d6c69923e25e3c00a4611818d18","author_type":"MANUSIA","author":"zuppasoupfifaistimewa-png","message":"Publish CI0-CI3 static selector and level-bank audit","changed_files":"reports/stage1_economy/CI0_CI1_CI2_CI3_STATIC_AUDIT_2026-11-04.md;reports/stage1_economy/CI0_COMMIT_LEDGER_2026-11-04.tsv;reports/stage1_economy/CI1_LEVEL_BANK_RECORDS_ALL_2026-11-04.tsv;reports/stage1_economy/CI1_SELECTOR_RESOURCE_INVENTORY_2026-11-04.tsv;reports/stage1_economy/CI2_OBSERVATION_CELL_MATCHES_2026-11-04.tsv;reports/stage1_economy/CI3_HB_FORMULA_TEST_2026-11-04.tsv"},
 {"commit_sha":"8141a8bd851b00e183797007563168d9ea6fdcdf","author_type":"MANUSIA","author":"zuppasoupfifaistimewa-png","message":"Complete CI0 ledger through first audit publication","changed_files":"reports/stage1_economy/CI0_CI1_CI2_CI3_STATIC_AUDIT_2026-11-04.md;reports/stage1_economy/CI0_COMMIT_LEDGER_2026-11-04.tsv"}]
 write(o/"DK0_COMMIT_LEDGER_2026-11-04.tsv",ledger)
 rec=[{k:v for k,v in r.items() if not k.startswith("_")} for r in records]
 write(o/"DK1_ALL_12_RESOURCE_RECORDS_2026-11-04.tsv",rec)
 layout=[]
 for rid,r in res.items():
  n=r["n"]
  layout.append({"resource_id_hex":H(rid),"N_expected":n,"header_first_byte":r["header"],"resource_size_bytes":r["size"],
   "expected_size_1_plus_Nx0x1E":1+n*STRIDE,"size_match":"YES" if r["size"]==1+n*STRIDE else "NO",
   "header_matches_N":"YES" if r["header"]==n else "NO","records_parsed":len(r["rows"]),
   "plausible_X_LV_records":r["good"],"blank_records":r["blanks"],"layout_class":r["status"],
   "byte_reason":r["reason"],"resource_data_bin_offset":H(r["off"]),"resource_sha256":r["sha"]})
 write(o/"DK1_RESOURCE_LAYOUT_CLASSIFICATION_2026-11-04.tsv",layout)
 matches=[]
 for X,vals in OBS.items():
  same=[r for r in records if r["X"]==X]
  for j,val in enumerate(vals,1):
   exact=[r for r in same if r[f"LV{j}"]==val]
   matches.append({"observation_X_hypothesis":X,"level":f"LV{j}","user_value_hypothesis":val,
    "exact_matches_resource_record":";".join(f'{r["resource_id_hex"]}#{r["record_index"]}' for r in exact) or "NONE",
    "same_X_records_and_values":";".join(f'{r["resource_id_hex"]}#{r["record_index"]}={r[f"LV{j}"]}' for r in same) or "NONE",
    "exact_match_count":len(exact),"same_X_record_count":len(same),
    "status":"EXACT_MATCH_FOUND" if exact else ("X_PRESENT_LEVEL_MISMATCH" if same else "NO_X_RECORD")})
 write(o/"DK2_OBSERVATION_ALL_12_RESOURCE_MATCHES_2026-11-04.tsv",matches)
 byx=defaultdict(list)
 for r in records: byx[r["X"]].append(r)
 cross=[]
 for X,g in sorted(byx.items()):
  vv=defaultdict(list)
  for r in g: vv[r["_vector"]].append(f'{r["resource_id_hex"]}#{r["record_index"]}')
  ids=sorted({int(r["resource_id_hex"],16) for r in g})
  state="CONFLICT" if len(vv)>1 else ("CONSISTENT_ACROSS_RESOURCES" if len(ids)>1 else "SINGLE_RESOURCE_ONLY")
  cross.append({"X":X,"record_count":len(g),"resource_ids":";".join(H(x) for x in ids),
   "distinct_LV_vectors":len(vv),"consistency":state,
   "vectors_and_records":" | ".join("["+ ",".join(map(str,k))+"]=" + ",".join(v) for k,v in vv.items())})
 write(o/"DK2_X_CROSS_RESOURCE_CONSISTENCY_2026-11-04.tsv",cross)
 ftests=[];e1=[];e2=[]
 for r in records:
  X=r["X"];exp1=X//2 if X%2==0 else f"{X}/2";ok1=X%2==0 and r["LV1"]==X//2
  exp2=10*((11*X+99)//100);ok2=r["LV2"]==exp2
  ftests.append({"resource_id_hex":r["resource_id_hex"],"record_index":r["record_index"],"X":X,
   "LV1":r["LV1"],"LV1_expected_X_div_2":exp1,"LV1_test":"PASS" if ok1 else "EXCEPTION",
   "LV2":r["LV2"],"LV2_expected_ceil10_1p1X":exp2,"LV2_test":"PASS" if ok2 else "EXCEPTION",
   "LV3":r["LV3"],"LV4":r["LV4"],"LV5":r["LV5"],"resource_sha256":r["resource_sha256"]})
  if not ok1:e1.append(r)
  if not ok2:e2.append(r)
 write(o/"DK3_ALL_RECORD_FORMULA_TEST_2026-11-04.tsv",ftests)
 cand=[];nb=[r for r in records if r["X"]>0]
 for j,c in ((3,2.2),(4,4.4),(5,8.8)):
  for mode in ("FLOOR","CEIL","NEAREST_HALF_UP"):
   m=0
   for r in nb:
    v=c*r["X"]; exp=math.floor(v+1e-9) if mode=="FLOOR" else (math.ceil(v-1e-9) if mode=="CEIL" else math.floor(v+.5))
    m+=r[f"LV{j}"]==exp
   cand.append({"level":f"LV{j}","candidate_formula":f"{mode}({c}*X)","matches":m,"tested_nonblank_records":len(nb),"distinct_X_tested":len({r["X"] for r in nb}),"mismatches":len(nb)-m,"claim":"CANDIDATE_ONLY_NOT_PROVEN"})
 write(o/"DK3_FORMULA_CANDIDATE_SUMMARY_2026-11-04.tsv",cand)
 counts=defaultdict(int)
 for r in res.values():counts[r["status"]]+=1
 conflicts=[r for r in cross if r["consistency"]=="CONFLICT"];n=len(records)
 lines=["# DK0-DK3 static audit: all 12 DATA.BIN resources","",
 "Game: Naruto - Shinobi no Sato no Jintori Gassen (SLPS-03553).",
 "Historical baseline 447631d02db0649abb07f7064ddf250bba81d779; inclusive cutoff 8141a8bd851b00e183797007563168d9ea6fdcdf.",
 f"DATA.BIN: {len(d)} bytes; SHA-256 {DATA_SHA}; resources={len(res)}; records={n}. No emulator/game execution.","",
 "## Evidence scale K0-K5",
 "- K0: no direct evidence; TIDAK TAHU.",
 "- K1: one weak clue/hypothesis; uncorroborated.",
 "- K2: two independent observations agree, but code/data chain remains open.",
 "- K3: byte-level static findings corroborate, but mapping or semantics remain incomplete.",
 "- K4: byte-exact reproducible static evidence with sufficient resource/reader linkage; maximum static grade.",
 "- K5: runtime behavior reproduced in at least two launches; not in scope.","",
 "| Task | Status | K | Finding |","|---|---|---:|---|",
 "| DK0 ledger | TUNTAS | K4 | 2 historical commits: 2 MANUSIA, 0 BOT. |",
 f"| DK1 parse 12 resources | TUNTAS | K3 | {counts['LAYOUT_SAMA']} sama; {counts['LAYOUT_BERBEDA']} berbeda; {counts['TIDAK_JELAS']} tidak jelas. |",
 f"| DK2 30 user cells | TUNTAS | K3 | Checked against {n} records; user inputs remain hypotheses. |",
 f"| DK2 repeated-X vectors | TUNTAS | K3 | {len(conflicts)} cross-resource conflicts. |",
 f"| DK3 LV1=X/2 | TUNTAS | K3 | {len(e1)} exceptions / {n}. |",
 f"| DK3 LV2=10*ceil(11X/100) | TUNTAS | K3 | {len(e2)} exceptions / {n}. |",
 "| DK3 LV3-LV5 source rule | SEBAGIAN | K3 | Formula candidates tested; offline formula vs stored table origin TIDAK TAHU. |","",
 "## DK0 exact commit ledger",
 "b81db45b4ac13d6c69923e25e3c00a4611818d18 — MANUSIA zuppasoupfifaistimewa-png — 6 files:",
 "- reports/stage1_economy/CI0_CI1_CI2_CI3_STATIC_AUDIT_2026-11-04.md",
 "- reports/stage1_economy/CI0_COMMIT_LEDGER_2026-11-04.tsv",
 "- reports/stage1_economy/CI1_LEVEL_BANK_RECORDS_ALL_2026-11-04.tsv",
 "- reports/stage1_economy/CI1_SELECTOR_RESOURCE_INVENTORY_2026-11-04.tsv",
 "- reports/stage1_economy/CI2_OBSERVATION_CELL_MATCHES_2026-11-04.tsv",
 "- reports/stage1_economy/CI3_HB_FORMULA_TEST_2026-11-04.tsv",
 "8141a8bd851b00e183797007563168d9ea6fdcdf — MANUSIA zuppasoupfifaistimewa-png — 2 files:",
 "- reports/stage1_economy/CI0_CI1_CI2_CI3_STATIC_AUDIT_2026-11-04.md",
 "- reports/stage1_economy/CI0_COMMIT_LEDGER_2026-11-04.tsv",
 "This audit publication and its Actions result are later commits, outside the historical cutoff.","",
 "## DK1 layout classification",
 "Rules checked: exact size 1+N*0x1E; first byte equals N; plausible X<=4095, LV<=10000 and nondecreasing, zero-X records have all LV zero.",
 "| Resource | N | first byte | bytes | class | byte reason |","|---|---:|---:|---:|---|---|"]
 for rid,r in res.items():lines.append(f"| {H(rid)} | {r['n']} | {r['header']} | {r['size']} | {r['status']} | {r['reason']} |")
 lines += ["","Offset +0x1E is beyond the 0x1E-byte record stride: TSV value is a next-record boundary diagnostic (or EOF on final record), not an in-record field. +0x1A/+0x1C are inside the stride.","",
 "## DK2 exact matches per cell (user inputs are hypotheses, not game facts)","",
 "| X | LV1 | LV2 | LV3 | LV4 | LV5 |","|---:|---|---|---|---|---|"]
 for X,vals in OBS.items():
  cells=[]
  for j,v in enumerate(vals,1):
   m=next(q for q in matches if q["observation_X_hypothesis"]==X and q["level"]==f"LV{j}")
   cells.append(f"{v}: {m['exact_matches_resource_record']}")
  lines.append(f"| {X} | "+" | ".join(cells)+" |")
 lines += ["","Per-cell TSV lists every same-X record/value as well as exact matches. Cross-resource X vector conflicts: "+(", ".join(str(r["X"]) for r in conflicts) if conflicts else "none in parsed data")+". See DK2_X_CROSS_RESOURCE_CONSISTENCY TSV.","",
 "## DK3",
 f"LV1=X/2: {n-len(e1)}/{n} pass; {len(e1)} exceptions; exact rows in DK3_ALL_RECORD_FORMULA_TEST TSV.",
 f"LV2=10*ceil(11X/100): {n-len(e2)}/{n} pass; {len(e2)} exceptions.",
 "LV1 exceptions: "+("; ".join(f'{r["resource_id_hex"]}#{r["record_index"]}:X={r["X"]},LV1={r["LV1"]}' for r in e1) or "NONE")+".",
 "LV2 exceptions: "+("; ".join(f'{r["resource_id_hex"]}#{r["record_index"]}:X={r["X"]},LV2={r["LV2"]}' for r in e2) or "NONE")+".",
 "",
 "LV1 exception hypotheses: (H1) explicit stored overrides; falsifier is a loader/constructor that recalculates and overwrites LV1 from X. (H2) a conditional +5 modifier for an unidentified record attribute; falsifier is the same attribute without +5 or a copy-only loader lacking conditional arithmetic. Which attribute, if any, selects +5 for X=60->35 and X=160->85: TIDAK TAHU.",
 "",
 "LV3-LV5 hypotheses: (H1) explicit stored lookup values selected by level; falsifier is a loader that derives/writes the fields from X. (H2) an offline authoring formula or piecewise formula generated the stored table; falsify a specific formula with three or more distinct X records that violate its exact rounding/piecewise rule. Matching three points alone does not prove a formula. Candidate tests for floor/ceil/nearest 2.2X, 4.4X, 8.8X are in DK3_FORMULA_CANDIDATE_SUMMARY TSV. Whether table values were manually authored or formula-generated: TIDAK TAHU.",
 "",
 "## Integrity",
 "- Original BIN/CUE and DATA.BIN were temporary runner inputs only; removed before commit.",
 "- No BIOS, savestate, emulator, gameplay, video/frame, or raw dumps used.",
 "- Only text MD/TSV/TXT committed; Release and STATUS.md unchanged.",
 "- Maximum static evidence grade K4; no K5 claim."]
 (o/"DK0_DK1_DK2_DK3_AUDIT_2026-11-04.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
 (o/"DK_STATIC_PARSE_SUMMARY.txt").write_text(f"STATUS=PASS\nDATA_BIN_BYTES={len(d)}\nDATA_BIN_SHA256={DATA_SHA}\nRESOURCES={len(res)}\nRECORDS={n}\nLV1_EXCEPTIONS={len(e1)}\nLV2_EXCEPTIONS={len(e2)}\nX_VECTOR_CONFLICTS={len(conflicts)}\nGAME_OR_EMULATOR_EXECUTED=no\n",encoding="utf-8")
 print(f"DK_PARSE_PASS resources={len(res)} records={n} lv1_exceptions={len(e1)} lv2_exceptions={len(e2)} x_conflicts={len(conflicts)}")
if __name__=="__main__": main()
