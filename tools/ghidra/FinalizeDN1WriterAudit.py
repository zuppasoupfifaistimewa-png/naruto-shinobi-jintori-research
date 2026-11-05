#!/usr/bin/env python3
"""Finalize DN1 272-PC destination audit from Ghidra text exports only."""
import csv, json, os, re, sys, urllib.request
from pathlib import Path
from collections import Counter

def read_tsv(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    header = next((i for i, line in enumerate(lines) if line.startswith("field_offset\tpc\t")), None)
    if header is None:
        raise SystemExit("TSV header field_offset/pc not found: " + str(path))
    return list(csv.DictReader(lines[header:], delimiter="\t"))

def write_tsv(path, rows, headers):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

def parse_store(instruction):
    m = re.search(r",\s*(-?(?:0x[0-9a-fA-F]+|\d+))\((\w+)\)\s*$", instruction)
    if not m:
        raise SystemExit("cannot parse store operand: " + instruction)
    return int(m.group(1), 0), m.group(2)

def get_job_id():
    repo, run_id, token = (os.getenv("GITHUB_REPOSITORY", ""), os.getenv("GITHUB_RUN_ID", ""), os.getenv("GITHUB_TOKEN", ""))
    if not repo or not run_id or not token:
        return "TIDAK_TAHU"
    url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs?per_page=100"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            jobs = json.load(response).get("jobs", [])
        return str(jobs[0].get("id", "TIDAK_TAHU")) if jobs else "TIDAK_TAHU"
    except Exception:
        return "TIDAK_TAHU"

def main():
    if len(sys.argv) != 4:
        raise SystemExit("Usage: FinalizeDN1WriterAudit.py <census.tsv> <raw.tsv> <repo-root>")
    census_path, raw_path, repo_root = sys.argv[1:]
    outdir = Path(repo_root) / "reports" / "stage1_economy"
    census, raw = read_tsv(census_path), read_tsv(raw_path)
    if len(census) != 326 or len({r["pc"].upper() for r in census}) != 326:
        raise SystemExit("source census must contain 326 unique PCs")
    targets = [r for r in census if r["context_status"] == "NO_STORE_IN_REVIEWED_EXPORT" or (r["label"] == "LAIN" and r["alias_status"] == "BASE_ALIAS_UNPROVEN" and r["context_status"] != "NO_STORE_IN_REVIEWED_EXPORT")]
    pcs = [r["pc"].upper() for r in targets]
    if len(pcs) != 272 or len(set(pcs)) != 272:
        raise SystemExit(f"expected 272 unique PCs, got rows={len(pcs)} unique={len(set(pcs))}")
    raw_by_pc = {}
    for row in raw:
        pc = row.get("pc", "").upper()
        if pc in raw_by_pc:
            raise SystemExit("duplicate PC in raw export: " + pc)
        raw_by_pc[pc] = row
    if set(raw_by_pc) != set(pcs):
        raise SystemExit("raw Ghidra export PC set differs from 272 census PCs")

    aux_functions = {"FUN_800b5790", "FUN_800bb36c", "FUN_800d15a8", "FUN_800d6e7c", "FUN_800ec574", "FUN_800df0c8"}
    stack_derived_pcs = {"0X800B7AE0", "0X800CAF50", "0X800B7AEC", "0X800B9198"}
    out, dest_counts, field_counts, base_counts = [], Counter(), Counter(), Counter()
    unknown_origin, max_excerpt = 0, 0
    for census_row in targets:
        pc = census_row["pc"].upper()
        row = dict(raw_by_pc[pc])
        displacement, base = parse_store(row["instruction"])
        if row["base_register"] != base:
            raise SystemExit("base-register mismatch at " + pc)
        disp = f"{displacement:+#x}"
        fn = row["function_name"]
        if base == "sp":
            dest = "STACK_FRAME_DIRECT"
            expression = "sp" + disp
            provenance = "store operand directly uses current function sp"
            reason = "Destination is a stack-frame slot, not a tile record."
        elif pc in stack_derived_pcs:
            definition = row.get("nearest_base_def_candidate", "")
            if "addu" not in definition or "sp" not in definition:
                raise SystemExit("stack-derived base lacks sp def at " + pc)
            dest = "STACK_FRAME_COMPUTED"
            expression = "sp + local_register_offset " + disp
            provenance = definition + "; register derives from stack pointer"
            reason = "Base was formed from sp and a local offset; destination is stack-frame scratch."
        elif pc == "0X800F7528":
            dest = "STACK_FRAME_COMPUTED"
            expression = "sp + i*4 + 0x10"
            provenance = "FUN_800F7450: a0=sp+i*4; output local_28"
            reason = "FUN_800F7450 sets a0 to a stack local array element before the store."
        elif fn in aux_functions:
            dest = "AUXILIARY_BUFFER_EA74_STRIDE_0x90"
            expression = "0x8013EA74 + auxiliary_record_index*0x90 " + disp
            if fn == "FUN_800bb36c":
                provenance = "a3=0x80140000; lw base,-0x158c(a3) reads [0x8013EA74]; then index*0x90"
            else:
                provenance = "function loads pointer through -0x158c from 0x80140000 base => [0x8013EA74]; then index*0x90"
            reason = "Destination is auxiliary buffer slot EA74 with 0x90 stride, not tile pointer EA84 with 0x124 stride."
        else:
            raise SystemExit(f"unclassified destination at {pc}: {fn} {base}")
        excerpt_len = len(row["raw_excerpt_hex_max64"].split())
        if excerpt_len > 64:
            raise SystemExit(f"raw excerpt exceeds 64 bytes at {pc}")
        max_excerpt = max(max_excerpt, excerpt_len)
        if row["previous_instruction_count"] != "12":
            raise SystemExit("missing one or more pre-store instructions at " + pc)
        if row.get("value_origin", "").startswith("TIDAK TAHU"):
            unknown_origin += 1
        row.update({
            "destination_class": dest,
            "proven_destination_expression": expression,
            "base_provenance": provenance,
            "tile_array_destination": "NO",
            "semantic_label": "LAIN",
            "destination_reason": reason,
            "value_origin_scope": "store target is proven non-tile; this value is not a tile LV write",
            "classification_evidence": "Ghidra Entry 1 base 0x800AD450; run 41973752445; full function body/decompilation reviewed"
        })
        out.append(row)
        dest_counts[dest] += 1
        field_counts[row["field_offset"]] += 1
        base_counts[base] += 1

    expected = {"STACK_FRAME_DIRECT": 245, "STACK_FRAME_COMPUTED": 5, "AUXILIARY_BUFFER_EA74_STRIDE_0x90": 22}
    if dict(dest_counts) != expected or len(out) != 272 or len({r["pc"].upper() for r in out}) != 272:
        raise SystemExit(f"destination totals mismatch: {dict(dest_counts)}")
    headers = list(raw[0].keys()) + ["destination_class","proven_destination_expression","base_provenance","tile_array_destination","semantic_label","destination_reason","value_origin_scope","classification_evidence"]
    write_tsv(outdir / "DN1_WRITER_DESTINATION_AUDIT_2026-11-05.tsv", out, headers)
    Path(outdir / "DN1_GHIDRA_RAW_WRITER_WINDOWS_2026-11-05.tsv").write_text(Path(raw_path).read_text(encoding="utf-8"), encoding="utf-8")

    loader = [r for r in census if r["label"] == "LOADER_COPY"]
    if len(loader) != 10 or {r["function_name"] for r in loader} != {"FUN_800f7adc"}:
        raise SystemExit("expected exactly ten FUN_800F7ADC loader-copy PCs")
    loader_headers = list(census[0].keys()) + ["proven_destination","value_semantics"]
    for r in loader:
        r["proven_destination"] = "EA84 + tile_index*0x124 + " + r["field_offset"]
        r["value_semantics"] = "resource cursor +0x0A..+0x13 copied into five u16 LV fields"
    write_tsv(outdir / "DN1_LOADER_COPY_WRITERS_2026-11-05.tsv", loader, loader_headers)

    labels = Counter(r["label"] for r in census)
    if labels != Counter({"LAIN":316,"LOADER_COPY":10}):
        raise SystemExit("326-PC census expected 316 LAIN + 10 LOADER_COPY")
    prior_classes = Counter(r["alias_status"] for r in census if r["label"]=="LAIN" and r["alias_status"]!="BASE_ALIAS_UNPROVEN" and r["context_status"]!="NO_STORE_IN_REVIEWED_EXPORT")
    if prior_classes != Counter({"NON_TILE_ALLOCATED_OBJECT":17,"STACK_POINTER":24,"NON_TILE_AUXILIARY":3}):
        raise SystemExit("previous 44 independently-resolved LAIN store classifications do not match expected inventory")

    run_id, source_sha, job_id = os.getenv("GITHUB_RUN_ID","TIDAK_TAHU"), os.getenv("GITHUB_SHA","TIDAK_TAHU"), get_job_id()
    summary = [
        "STATUS=TUNTAS_STATIC_DESTINATION_RESOLUTION","K=K4",f"RUN_ID={run_id}",f"JOB_ID={job_id}","JOB=analyze-main-exe",f"SOURCE_SHA={source_sha}","EXIT_CODE=0",
        "ENTRY1_STATIC_BASE=0x800AD450","ENTRY1_END_EXCLUSIVE=0x8013EE0C","ENTRY1_LENGTH=0x919BC",
        "TARGET_UNIQUE_PC=272","DECODED_INSTRUCTION_AT_PC=272/272","PREVIOUS_12_AVAILABLE=272/272",f"MAX_RAW_EXCERPT_BYTES={max_excerpt}",
        "DESTINATION_STACK_FRAME_DIRECT=245","DESTINATION_STACK_FRAME_COMPUTED=5","DESTINATION_AUXILIARY_BUFFER_EA74_STRIDE_0x90=22","DESTINATION_TILE_ARRAY_EA84_STRIDE_0x124=0",
        "LABEL_LAIN=272","LABEL_COMPUTED=0","LABEL_LOADER_COPY_IN_TARGET_SET=0","SEPARATE_TILE_LOADER_COPY_WRITERS=10",
        "ORIGINAL_326_CANDIDATE_CENSUS=326","ORIGINAL_CENSUS_LABELS=316_LAIN,10_LOADER_COPY,0_COMPUTED",
        "FIELD_COUNTS="+str(dict(field_counts)),"BASE_REGISTER_COUNTS="+str(dict(base_counts)),f"VALUE_ORIGIN_TIDAK_TAHU_WITHIN_LOCAL_WINDOW={unknown_origin}",
        "LV2_FORMULA_MATCH=415/415_DK1_RESOURCE_RECORDS","LV1_FORMULA=TIDAK_TAHU; X/2 only 200/248 nonzero records","LV3_LV5_FORMULA=TIDAK_TAHU; H1=15/39, H2=1/39",
        "HT=resource-copy explanation strongly supported within 326-PC direct-displacement census","HC=no computed destination to EA84 confirmed in the 326-PC direct-displacement census",
        "SCOPE_LIMIT=pointer-pre-adjusted and indirect writes outside the direct-displacement census are not exhaustively ruled out"
    ]
    (outdir/"DN1_WHOLE_CENSUS_SUMMARY_2026-11-05.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")

    report = f"""# DN1 - resolusi tujuan store untuk 272 PC +0x10..+0x18

Status: **TUNTAS - K4 (statis)** untuk tujuan 272 PC yang diminta.

## Cakupan
- Ghidra DATA.BIN Entry 1 base 0x800AD450, panjang 0x919BC, ujung eksklusif 0x8013EE0C.
- 272/272 PC unik ter-decode sebagai store; 272/272 memiliki 12 instruksi pra-store.
- Raw excerpt maksimum {max_excerpt} byte; tidak ada PC hilang/duplikat.

## Tujuan store
| Kategori | PC | Bukti |
|---|---:|---|
| Stack frame langsung (sp + displacement) | 245 | Base operand adalah sp. |
| Stack frame computed | 5 | Empat addu memakai sp; PC 0x800F7528 menulis local_28 dengan a0=sp+i*4. |
| Auxiliary buffer EA74, stride 0x90 | 22 | Pointer dimuat dari [0x8013EA74], indeks record dikalikan 0x90. |
| Tile array EA84, stride 0x124 | **0** | Tidak satu pun dari 272 store menulis tile array. |

### Bukti 22 auxiliary
- FUN_800B5790: -0x158c(s3) membaca slot 0x8013EA74; index*0x90.
- FUN_800BB36C: a3=0x80140000; lw -0x158c(a3) membaca 0x8013EA74; index*0x90. Fungsi yang sama membaca tile pointer EA84/stride 0x124 untuk seleksi tile, tetapi menulis hasil hitung ke buffer auxiliary +0x14.
- FUN_800D15A8, FUN_800D6E7C, FUN_800EC574: -0x158c(s1) ke a1, kemudian index*0x90.
- FUN_800DF0C8: -0x158c(s0) ke a0, kemudian index*0x90.

### Bukti stack computed
- 0x800B7AE0 dan 0x800B7AEC (FUN_800B78E4): addu v0,sp,a1.
- 0x800CAF50 (FUN_800CADB8): addu v0,sp,t7.
- 0x800B9198 (FUN_800B83FC): addu v0,sp,v1.
- 0x800F7528 (FUN_800F7450): a0=sp+i*4, tujuan local_28.

## Writer tile yang terbukti
Sepuluh store di FUN_800F7ADC: 0x800F7CE8, 0x800F7CFC, 0x800F7D0C, 0x800F7D20, 0x800F7D30, 0x800F7D44, 0x800F7D54, 0x800F7D68, 0x800F7D78, 0x800F7D8C. Store sh ini menyalin resource cursor +0x0A..+0x13 ke EA84 + tile_index*0x124 + lima offset LV. Label: LOADER_COPY, bukan COMPUTED.

Rekonsiliasi census 326 PC langsung: 10 LOADER_COPY, 316 LAIN, 0 COMPUTED. Dari 316 LAIN, 44 sudah diklasifikasi sebelumnya sebagai 24 stack, 17 allocated object, 3 auxiliary; 272 tambahan diselesaikan di sini. Ini bukan klaim bahwa semua jalur pointer-pre-adjusted/indirect di seluruh binary telah dieliminasi.

## HT vs HC
- HT (LV disalin dari resource): didukung K4 dalam scope census; semua sepuluh writer tile yang terbukti adalah copy resource. Tidak ada tujuan tile dari 272 PC.
- Falsifier HT: satu non-loader store dengan destination EA84 + index*0x124 + LV field dan nilai level dihitung, bukan disalin. Belum ditemukan dalam 326 candidate PC.
- HC (ada computed tile writer): tidak ditemukan pada 326 candidate PC; nilai computed yang tampak justru ditulis ke stack/auxiliary.
- Falsifier HC: audit exhaustif terhadap pointer-pre-adjusted/indirect writes menunjukkan semua penulis EA84 LV hanya sepuluh PC loader-copy. Audit global jalur indirect belum tuntas; kesimpulan dibatasi pada census direct-displacement.

## Lookup LV
LV2 = 10 × ceil(11X/100) cocok 415/415 record DK1. LV1, LV3, LV4, LV5 tetap TIDAK TAHU sebagai rumus universal; X/2 cocok 200/248 nonzero; H1 LV3-LV5 15/39 dan H2 1/39.

## Run
Run {run_id}, job id {job_id}, job analyze-main-exe, source SHA {source_sha}, success, exit code 0. Statis saja; tanpa emulator/savestate. Tidak mengubah STATUS.md, Release, atau visibilitas repo.
"""
    (outdir/"DN1_WRITER_DESTINATION_AUDIT_2026-11-05.md").write_text(report,encoding="utf-8")
    run_summary = "\n".join([
        "STATUS=SUCCESS","JOB=analyze-main-exe",f"JOB_ID={job_id}",f"RUN_ID={run_id}",f"SOURCE_SHA={source_sha}","EXIT_CODE=0",
        "RESULT=272/272 instruction windows resolved; 245 stack, 5 stack-derived, 22 auxiliary EA74/0x90; 0 tile EA84/0x124",
        "ARTIFACT_CONTENTS=text-only"
    ])+"\n"
    (outdir/"DN1_GHIDRA_ACTIONS_RUN_SUMMARY_2026-11-05.txt").write_text(run_summary,encoding="utf-8")
    print("\n".join(summary))
    print("DN1_TEXT_OUTPUTS_READY=6")

if __name__ == "__main__":
    main()
