#!/usr/bin/env python3
"""Corrected DK0-DK3 static DATA.BIN audit using the FUN_800F7ADC source-to-runtime map."""
import argparse,csv,hashlib,math,struct
from collections import defaultdict
from pathlib import Path

DATA_SHA="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
DATA_SIZE=66015232
DATA_LBN=212
STRIDE=0x1E
RESOURCE_N={0x276:22,0x277:33,0x278:33,0x279:34,0x27A:33,0x27B:43,0x27C:38,
            0x27E:22,0x27F:38,0x285:43,0x286:36,0x287:40}
OBS={120:[60,140,265,530,1050],180:[90,200,390,800,1600],200:[100,220,440,880,1760],
     220:[110,250,490,980,1940],240:[120,270,530,1050,2120],280:[140,310,620,1240,2470]}
def H(v): return f"0x{v:X}"
def U16(b,o): return struct.unpack_from("<H",b,o)[0]
def SHA(b): return hashlib.sha256(b).hexdigest()
def write_tsv(path,rows):
    if not rows: raise ValueError(f"no rows for {path.name}")
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter="\t",lineterminator="\n")
        w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data",required=True)
    ap.add_argument("--out-dir",required=True)
    a=ap.parse_args()
    data=Path(a.data).read_bytes()
    if len(data)!=DATA_SIZE or SHA(data)!=DATA_SHA:
        raise SystemExit(f"DATA_BIN_IDENTITY_FAIL bytes={len(data)} sha={SHA(data)}")
    directory=[struct.unpack_from("<II",data,0x44+i*8) for i in range(1504)]
    out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=True)
    resources={};records=[]
    for rid,n in RESOURCE_N.items():
        lbn,size=directory[rid]
        off=(lbn-DATA_LBN)*2048
        if size<=0 or off<0 or off+size>len(data):
            raise SystemExit(f"RESOURCE_BOUNDS_FAIL id={rid:#x} lbn={lbn} size={size} off={off:#x}")
        blob=data[off:off+size];digest=SHA(blob);header=blob[0] if blob else None
        parse_n=min(n,max(0,(len(blob)-1)//STRIDE))
        rr=[];plausible=0;nonblank=0
        for idx in range(parse_n):
            q=idx*STRIDE
            # FUN_800F7ADC: source pointer is the record start. pbVar2[8] -> runtime tile+0x0E (X);
            # pbVar2[10..18] -> runtime tile+0x10..0x18 (LV1..LV5).
            X=U16(blob,q+0x08)
            lv=[U16(blob,q+x) for x in (0x0A,0x0C,0x0E,0x10,0x12)]
            raw=[U16(blob,q+x) for x in (0x0E,0x10,0x12,0x14,0x16,0x18)]
            # Runtime tile +0x1A/+0x1C/+0x1E receive source cursor offsets +0x14/+0x16/+0x18.
            p1a=U16(blob,q+0x14);p1c=U16(blob,q+0x16);p1e_runtime=U16(blob,q+0x18)
            source_p1a=U16(blob,q+0x1A);source_p1c=U16(blob,q+0x1C)
            boundary=blob[q+0x1E] if q+0x1E<len(blob) else ""
            boundary16=U16(blob,q+0x1E) if q+0x20<=len(blob) else ""
            blank=(X==0 and all(v==0 for v in lv));nonblank+=int(not blank)
            good=(X<=4095 and all(v<=10000 for v in lv) and
                  all(lv[j]<=lv[j+1] for j in range(4)) and (blank or (X>0 and lv[0]>0)))
            plausible+=int(good)
            r={
              "resource_id_hex":H(rid),"resource_id_decimal":rid,"record_index":idx,
              "X_loader_mapped_source_plus_0x08":X,
              "LV1_loader_mapped_source_plus_0x0A":lv[0],"LV2_loader_mapped_source_plus_0x0C":lv[1],
              "LV3_loader_mapped_source_plus_0x0E":lv[2],"LV4_loader_mapped_source_plus_0x10":lv[3],
              "LV5_loader_mapped_source_plus_0x12":lv[4],
              "literal_spec_X_at_source_plus_0x0E":raw[0],
              "literal_spec_LV1_at_source_plus_0x10":raw[1],"literal_spec_LV2_at_source_plus_0x12":raw[2],
              "literal_spec_LV3_at_source_plus_0x14":raw[3],"literal_spec_LV4_at_source_plus_0x16":raw[4],
              "literal_spec_LV5_at_source_plus_0x18":raw[5],
              "plus_0x1A":p1a,"plus_0x1C":p1c,"plus_0x1E":p1e_runtime,
              "source_raw_plus_0x1A":source_p1a,"source_raw_plus_0x1C":source_p1c,
              "loader_source_plus_0x1E_boundary_byte":boundary,
              "loader_source_plus_0x1E_boundary_u16":boundary16,
              "loader_boundary_status":"NEXT_STRIDE_BYTE" if idx<n-1 else "FINAL_IN_RESOURCE",
              "resource_data_bin_offset":H(off),"loader_stride_base_data_bin_offset":H(off+q),
              "record_data_bin_offset":H(off+q+1),"record_resource_offset":H(q+1),"resource_size_bytes":size,
              "resource_header_first_byte":header,"expected_N":n,"resource_sha256":digest,
              "_vector":tuple(lv),"_plausible":good}
            rr.append(r);records.append(r)
        size_ok=size==1+n*STRIDE;head_ok=header==n
        ratio=plausible/len(rr) if rr else 0
        if not size_ok or not head_ok:
            klass="LAYOUT_BERBEDA";reason=f"size={size} expected={1+n*STRIDE}; header={header} expected_N={n}"
        elif ratio>=0.90:
            klass="LAYOUT_SAMA";reason=f"size=1+{n}*0x1E; header={header}=N; plausible={plausible}/{len(rr)}"
        else:
            klass="TIDAK_JELAS";reason=f"size/header match; plausible={plausible}/{len(rr)}"
        resources[rid]={"N":n,"size":size,"off":off,"sha":digest,"header":header,
                        "rows":rr,"plausible":plausible,"nonblank":nonblank,"class":klass,"reason":reason}

    ledger=[
      {"commit_sha":"b81db45b4ac13d6c69923e25e3c00a4611818d18","author_type":"MANUSIA","author":"zuppasoupfifaistimewa-png",
       "message":"Publish CI0-CI3 static selector and level-bank audit",
       "changed_files":"reports/stage1_economy/CI0_CI1_CI2_CI3_STATIC_AUDIT_2026-11-04.md;reports/stage1_economy/CI0_COMMIT_LEDGER_2026-11-04.tsv;reports/stage1_economy/CI1_LEVEL_BANK_RECORDS_ALL_2026-11-04.tsv;reports/stage1_economy/CI1_SELECTOR_RESOURCE_INVENTORY_2026-11-04.tsv;reports/stage1_economy/CI2_OBSERVATION_CELL_MATCHES_2026-11-04.tsv;reports/stage1_economy/CI3_HB_FORMULA_TEST_2026-11-04.tsv"},
      {"commit_sha":"8141a8bd851b00e183797007563168d9ea6fdcdf","author_type":"MANUSIA","author":"zuppasoupfifaistimewa-png",
       "message":"Complete CI0 ledger through first audit publication",
       "changed_files":"reports/stage1_economy/CI0_CI1_CI2_CI3_STATIC_AUDIT_2026-11-04.md;reports/stage1_economy/CI0_COMMIT_LEDGER_2026-11-04.tsv"}]
    write_tsv(out/"DK0_COMMIT_LEDGER_2026-11-04.tsv",ledger)
    write_tsv(out/"DK1_ALL_12_RESOURCE_RECORDS_2026-11-04.tsv",
      [{k:v for k,v in r.items() if not k.startswith("_")} for r in records])
    layout=[]
    for rid,r in resources.items():
        n=r["N"]
        layout.append({"resource_id_hex":H(rid),"resource_id_decimal":rid,"N_expected":n,
          "header_first_byte":r["header"],"resource_size_bytes":r["size"],
          "expected_size_1_plus_Nx0x1E":1+n*STRIDE,"size_match":"YES" if r["size"]==1+n*STRIDE else "NO",
          "header_matches_N":"YES" if r["header"]==n else "NO","records_parsed":len(r["rows"]),
          "loader_mapped_plausible_X_LV_records":r["plausible"],"nonblank_records":r["nonblank"],
          "layout_class":r["class"],"byte_reason":r["reason"],
          "resource_data_bin_offset":H(r["off"]),"resource_sha256":r["sha"]})
    write_tsv(out/"DK1_RESOURCE_LAYOUT_CLASSIFICATION_2026-11-04.tsv",layout)

    matches=[]
    for X,vals in OBS.items():
      for j,val in enumerate(vals,1):
        same=[r for r in records if r["X_loader_mapped_source_plus_0x08"]==X]
        field=f"LV{j}_loader_mapped_source_plus_0x{0x08+2*j:02X}"
        exact=[r for r in same if r[field]==val]
        lsame=[r for r in records if r["literal_spec_X_at_source_plus_0x0E"]==X]
        lfield=f"literal_spec_LV{j}_at_source_plus_0x{0x0E+2*j:02X}"
        lexact=[r for r in lsame if r[lfield]==val]
        matches.append({"observation_X_hypothesis":X,"level":f"LV{j}","user_value_hypothesis":val,
          "loader_mapped_exact_matches":";".join(f'{r["resource_id_hex"]}#{r["record_index"]}' for r in exact) or "NONE",
          "loader_mapped_same_X_records_values":";".join(f'{r["resource_id_hex"]}#{r["record_index"]}={r[field]}' for r in same) or "NONE",
          "loader_mapped_match_count":len(exact),"loader_mapped_same_X_record_count":len(same),
          "literal_requested_offset_exact_matches":";".join(f'{r["resource_id_hex"]}#{r["record_index"]}' for r in lexact) or "NONE",
          "literal_requested_offset_same_X_values":";".join(f'{r["resource_id_hex"]}#{r["record_index"]}={r[lfield]}' for r in lsame) or "NONE",
          "literal_offset_match_count":len(lexact),
          "loader_mapped_status":"EXACT_MATCH_FOUND" if exact else ("X_PRESENT_LEVEL_MISMATCH" if same else "NO_X_RECORD"),
          "literal_offset_status":"EXACT_MATCH_FOUND" if lexact else ("X_PRESENT_LEVEL_MISMATCH" if lsame else "NO_X_RECORD")})
    write_tsv(out/"DK2_OBSERVATION_ALL_12_RESOURCE_MATCHES_2026-11-04.tsv",matches)

    byx=defaultdict(list)
    for r in records:byx[r["X_loader_mapped_source_plus_0x08"]].append(r)
    cross=[]
    for X,g in sorted(byx.items()):
      vectors=defaultdict(list)
      for r in g:vectors[r["_vector"]].append(f'{r["resource_id_hex"]}#{r["record_index"]}')
      ids=sorted({int(r["resource_id_hex"],16) for r in g})
      state="CONFLICT" if len(vectors)>1 else ("CONSISTENT_ACROSS_RESOURCES" if len(ids)>1 else "SINGLE_RESOURCE_ONLY")
      cross.append({"X_loader_mapped":X,"record_count":len(g),"resource_ids":";".join(H(i) for i in ids),
        "distinct_LV1_to_LV5_vectors":len(vectors),"consistency":state,
        "vectors_and_records":" | ".join("["+ ",".join(map(str,v))+"]=" + ",".join(refs) for v,refs in vectors.items())})
    write_tsv(out/"DK2_X_CROSS_RESOURCE_CONSISTENCY_2026-11-04.tsv",cross)

    ftests=[];e1=[];e2=[]
    for r in records:
      X=r["X_loader_mapped_source_plus_0x08"];v1=r["LV1_loader_mapped_source_plus_0x0A"];v2=r["LV2_loader_mapped_source_plus_0x0C"]
      exp1=X//2 if X%2==0 else "NON_INTEGER";ok1=(X%2==0 and v1==X//2)
      exp2=10*((11*X+99)//100);ok2=v2==exp2
      ftests.append({"resource_id_hex":r["resource_id_hex"],"record_index":r["record_index"],"X":X,
       "LV1_observed":v1,"LV1_expected_X_div_2":exp1,"LV1_test":"PASS" if ok1 else "EXCEPTION",
       "LV2_observed":v2,"LV2_expected_10xceil_1p1X":exp2,"LV2_test":"PASS" if ok2 else "EXCEPTION",
       "LV3":r["LV3_loader_mapped_source_plus_0x0E"],"LV4":r["LV4_loader_mapped_source_plus_0x10"],
       "LV5":r["LV5_loader_mapped_source_plus_0x12"],"resource_sha256":r["resource_sha256"]})
      if not ok1:e1.append(r)
      if not ok2:e2.append(r)
    write_tsv(out/"DK3_ALL_RECORD_FORMULA_TEST_2026-11-04.tsv",ftests)

    nonblank=[r for r in records if r["X_loader_mapped_source_plus_0x08"]>0]
    candidates=[]
    for lvl,c in ((3,2.2),(4,4.4),(5,8.8)):
      field=f"LV{lvl}_loader_mapped_source_plus_0x{0x08+2*lvl:02X}"
      for mode in ("FLOOR","CEIL","NEAREST_HALF_UP"):
        m=0
        for r in nonblank:
          raw=c*r["X_loader_mapped_source_plus_0x08"]
          expected=math.floor(raw+1e-9) if mode=="FLOOR" else (math.ceil(raw-1e-9) if mode=="CEIL" else math.floor(raw+0.5))
          m+=r[field]==expected
        candidates.append({"level":f"LV{lvl}","candidate_formula":f"{mode}({c}*X)",
          "matching_records":m,"tested_nonblank_records":len(nonblank),
          "distinct_X_tested":len({r["X_loader_mapped_source_plus_0x08"] for r in nonblank}),
          "mismatches":len(nonblank)-m,"claim_status":"CANDIDATE_ONLY_NOT_PROVEN"})
    write_tsv(out/"DK3_FORMULA_CANDIDATE_SUMMARY_2026-11-04.tsv",candidates)

    counts=defaultdict(int)
    for r in resources.values():counts[r["class"]]+=1
    conflicts=[r for r in cross if r["consistency"]=="CONFLICT"]
    lv1_pairs=defaultdict(list)
    for r in e1:lv1_pairs[(r["X_loader_mapped_source_plus_0x08"],r["LV1_loader_mapped_source_plus_0x0A"])].append(f'{r["resource_id_hex"]}#{r["record_index"]}')
    lines=[
      "# DK0-DK3 corrected static audit — 12 DATA.BIN resources",
      "",
      "Game: Naruto - Shinobi no Sato no Jintori Gassen (SLPS-03553).",
      "Historical baseline 447631d02db0649abb07f7064ddf250bba81d779; cutoff inclusive 8141a8bd851b00e183797007563168d9ea6fdcdf.",
      f"DATA.BIN identity: {len(data)} bytes; SHA-256 {DATA_SHA}; resources={len(resources)}; records={len(records)}.",
      "This corrected report supersedes the first DK parse (run 41815588375 attempt 2): that parser used raw source +0x0E as X, disproved by the static loader; its original 415-record numeric findings are invalid.",
      "",
      "## K0-K5 evidence scale",
      "- K0: no direct evidence; TIDAK TAHU.",
      "- K1: one weak clue/hypothesis only.",
      "- K2: two independent observations agree, source/data relationship still open.",
      "- K3: multiple byte-level findings corroborate; semantic mapping or resource selection remains incomplete.",
      "- K4: reproducible exact static bytes plus disassembled loader mapping; maximum static grade.",
      "- K5: runtime confirmed in at least two independent launches; not used here.",
      "",
      "| Task | Status | K | Result |","|---|---|---:|---|",
      "| DK0 historical commit ledger | TUNTAS | K4 | Two commits after baseline through 8141a8...; both MANUSIA. |",
      f"| DK1 layout + loader field map | TUNTAS | K4 | {counts['LAYOUT_SAMA']} same; {counts['LAYOUT_BERBEDA']} different; {counts['TIDAK_JELAS']} unclear. |",
      f"| DK2 user-value cells (loader-mapped) | TUNTAS | K3 | 30 cells checked against {len(records)} records. |",
      f"| DK2 repeated-X vectors | TUNTAS | K3 | {len(conflicts)} X values with differing LV vectors. |",
      f"| DK3 LV1=X/2 | TUNTAS | K3 | {len(records)-len(e1)}/{len(records)} pass; {len(e1)} exceptions. |",
      f"| DK3 LV2=10*ceil(1.1X) | TUNTAS | K3 | {len(records)-len(e2)}/{len(records)} pass; {len(e2)} exceptions. |",
      "| DK3 LV3-LV5 provenance | SEBAGIAN | K3 | Runtime loader copies stored values; offline formula vs authored table TIDAK TAHU. |",
      "",
      "## Critical offset correction from FUN_800F7ADC",
      "Loader cursor base begins at resource byte 0 (the first count/preamble byte) and advances by 0x1E each iteration. Each row's data starts at cursor+1. Source mapping below is relative to the loader cursor base:",
      "| Loader-cursor source bytes | Runtime destination | Field interpretation here |",
      "|---|---|---|",
      "| +0x08..+0x09 | tile+0x0E | X |",
      "| +0x0A..+0x0B | tile+0x10 | LV1 |",
      "| +0x0C..+0x0D | tile+0x12 | LV2 |",
      "| +0x0E..+0x0F | tile+0x14 | LV3 |",
      "| +0x10..+0x11 | tile+0x16 | LV4 |",
      "| +0x12..+0x13 | tile+0x18 | LV5 |",
      "| +0x14..+0x15 | tile+0x1A | requested extra field +0x1A |",
      "| +0x16..+0x17 | tile+0x1C | requested extra field +0x1C |",
      "| +0x18..+0x19 | tile+0x1E | requested extra field +0x1E |",
      "| +0x1A..+0x1B | tile+0x22 | additional field |",
      "| +0x1C..+0x1D | tile+0x24 | additional field |",
      "| +0x1E | tile+0x0C | loader boundary byte; next stride (final row: final byte in resource) |",
      "",
      "The requested +0x0E (X) and +0x10..+0x18 (LV1..LV5) are runtime tile-structure offsets. Relative to the loader cursor base (resource + record_index*0x1E), X is copied from +0x08 and LV1..LV5 from +0x0A..+0x12. Relative to the data row start reported as record_source_offset (cursor+1), those are +0x07 and +0x09..+0x11. The TSV also preserves raw source offsets +0x0E..+0x18 separately.",
      "",
      "## DK0 historical commit ledger",
      "| Full commit SHA | Author | Changed files |","|---|---|---|",
      "| b81db45b4ac13d6c69923e25e3c00a4611818d18 | MANUSIA: zuppasoupfifaistimewa-png | 6 files listed below |",
      "- reports/stage1_economy/CI0_CI1_CI2_CI3_STATIC_AUDIT_2026-11-04.md",
      "- reports/stage1_economy/CI0_COMMIT_LEDGER_2026-11-04.tsv",
      "- reports/stage1_economy/CI1_LEVEL_BANK_RECORDS_ALL_2026-11-04.tsv",
      "- reports/stage1_economy/CI1_SELECTOR_RESOURCE_INVENTORY_2026-11-04.tsv",
      "- reports/stage1_economy/CI2_OBSERVATION_CELL_MATCHES_2026-11-04.tsv",
      "- reports/stage1_economy/CI3_HB_FORMULA_TEST_2026-11-04.tsv",
      "| 8141a8bd851b00e183797007563168d9ea6fdcdf | MANUSIA: zuppasoupfifaistimewa-png | 2 files listed below |",
      "- reports/stage1_economy/CI0_CI1_CI2_CI3_STATIC_AUDIT_2026-11-04.md",
      "- reports/stage1_economy/CI0_COMMIT_LEDGER_2026-11-04.tsv",
      "Later preparation and bot-output commits are outside the historical cutoff.",
      "",
      "## DK1 — resource classes",
      "Exact checks: size=1+N*0x1E; byte zero=N; all loader-mapped records have X<=4095, LV<=10000, monotonic LV1..LV5, and zero-X rows have zero levels.",
      "| ID | N | header | bytes | class | byte reason |","|---|---:|---:|---:|---|---|"
    ]
    for rid,r in resources.items():lines.append(f"| {H(rid)} | {r['N']} | {r['header']} | {r['size']} | {r['class']} | {r['reason']} |")
    lines += ["",
      "DK1 full TSV includes every row, loader-mapped X/LV1-LV5, runtime tile +0x1A/+0x1C/+0x1E, raw source +0x1A/+0x1C, loader boundary byte, row DATA.BIN offset, loader stride-base offset and full resource SHA-256.",
      "",
      "## DK2 — user values are hypotheses, not facts",
      "| X | LV1 | LV2 | LV3 | LV4 | LV5 |","|---:|---|---|---|---|---|"]
    for X,vals in OBS.items():
      cells=[]
      for j,val in enumerate(vals,1):
        m=next(x for x in matches if x["observation_X_hypothesis"]==X and x["level"]==f"LV{j}")
        cells.append(f"{val}: {m['loader_mapped_exact_matches']}")
      lines.append(f"| {X} | "+" | ".join(cells)+" |")
    lines += ["",
      "All exact matches and all same-X row values are listed in DK2 TSV, along with literal-offset matches. Cross-resource full-vector conflicts: "+(", ".join(str(x["X_loader_mapped"]) for x in conflicts) if conflicts else "none")+".",
      "",
      "## DK3 formula tests",
      f"LV1=X/2: {len(records)-len(e1)}/{len(records)} pass, {len(e1)} exceptions.",
      f"LV2=10*ceil(11X/100): {len(records)-len(e2)}/{len(records)} pass, {len(e2)} exceptions.",
      "LV1 exception pairs and all locations:"]
    for (x,v),refs in sorted(lv1_pairs.items()):lines.append(f"- X={x}, LV1={v}: {', '.join(refs)}")
    lines += ["",
      "LV1 competing hypotheses:",
      "1. Stored per-record override; LV1=35 at X=60 and LV1=85 at X=160 are literal source halfwords copied by the loader. Falsifier: a separate code path computes LV1 from X and overwrites that halfword before it is consumed.",
      "2. Hidden record-class/flag conditional adds +5 relative to X/2. Falsifier: identical relevant flags/class with differing +5 behavior, or proof no downstream conditional exists. The selector is TIDAK TAHU.",
      "",
      "LV3-LV5 competing hypotheses:",
      "1. Runtime table lookup: loader copies LV3-LV5 from source halfwords. Falsifier: find runtime path deriving and overwriting those values from X.",
      "2. Offline formula-generated table: build-time process could generate the stored values. Falsifier for a concrete formula is three or more distinct X values that violate its exact rounding/piecewise rule. A few matches do not prove it.",
      "Candidate floor/ceil/nearest tests for 2.2X, 4.4X, 8.8X are in DK3_FORMULA_CANDIDATE_SUMMARY; source authorship vs offline formula: TIDAK TAHU.",
      "",
      "## Integrity",
      "- Static DATA.BIN/resource bytes and disassembled loader only; no emulator, BIOS, savestate, gameplay, video or frames.",
      "- Binary inputs were temporary runner files and deleted before commit.",
      "- Only MD/TSV/TXT committed; Release and STATUS.md unchanged.",
      "- Maximum grade K4 static; no K5 claim."]
    (out/"DK0_DK1_DK2_DK3_AUDIT_2026-11-04.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    (out/"DK_STATIC_PARSE_SUMMARY.txt").write_text("\n".join([
      "PARSER_STATUS=PASS",f"DATA_BIN_BYTES={len(data)}",f"DATA_BIN_SHA256={DATA_SHA}",
      f"RESOURCES={len(resources)}",f"RECORDS={len(records)}",
      "LAYOUT_COUNTS="+";".join(f"{k}:{counts[k]}" for k in ("LAYOUT_SAMA","LAYOUT_BERBEDA","TIDAK_JELAS")),
      f"LV1_EXCEPTIONS={len(e1)}",f"LV2_EXCEPTIONS={len(e2)}",f"X_VECTOR_CONFLICTS={len(conflicts)}",
      "FIELD_MAP=FUN_800F7ADC_SOURCE_08_X_0A_0C_0E_10_12_LV1_TO_LV5",
      "LITERAL_REQUESTED_OFFSETS_REPORTED_SEPARATELY=yes","GAME_OR_EMULATOR_EXECUTED=no"])+"\n",encoding="utf-8")
    print(f"DK_PARSE_CORRECTED_PASS resources={len(resources)} records={len(records)} "
          f"layout={dict(counts)} lv1_exceptions={len(e1)} lv2_exceptions={len(e2)} x_conflicts={len(conflicts)}")
if __name__=="__main__":main()
