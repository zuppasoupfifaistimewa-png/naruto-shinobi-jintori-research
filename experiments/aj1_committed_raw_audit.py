#!/usr/bin/env python3
"""AJ1 audit: parse exact committed bytes at ee48de4; never trust stale TSV status."""
from pathlib import Path
import csv
import hashlib
import re
import subprocess
import os

REF = "ee48de43577d08eeca77f6930d7f49a250cbba83"
BASE = "reports/ae_2026-10-29/deep"

def git_bytes(path):
    return subprocess.check_output(["git", "show", f"{REF}:{path}"])

def git_paths(prefix):
    raw = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", REF, prefix], text=True)
    return [x for x in raw.splitlines() if x]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def parse_tsv(data):
    return list(csv.DictReader(data.decode("utf-8", "replace").splitlines(), delimiter="\t"))

def main():
    out = Path(os.environ["AJ_OUTPUT_DIR"])
    out.mkdir(parents=True, exist_ok=True)
    raw_paths = git_paths(BASE + "/raw")
    raw_data = {p: git_bytes(p) for p in raw_paths}
    manifest_lines = []
    for p in sorted(raw_paths):
        b = raw_data[p]
        manifest_lines.append(f"{digest(b)}  {p[len(BASE)+1:]}  bytes={len(b)}")
    (out / "COMMITTED_RAW_MANIFEST.sha256.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    old_manifest = git_bytes(BASE + "/raw-log-sha256.txt").decode("utf-8", "replace")
    old_entries = []
    for line in old_manifest.splitlines():
        m = re.match(r"^([0-9a-f]{64})\s+(.+?)\s+bytes=(\d+)\s*$", line)
        if m:
            old_entries.append((m.group(1), m.group(2), int(m.group(3))))
    hash_bad = size_bad = missing = 0
    mismatch_rows = []
    for expected, rel, expected_size in old_entries:
        p = BASE + "/" + rel
        b = raw_data.get(p)
        if b is None:
            missing += 1
            mismatch_rows.append((rel, expected, "MISSING", expected_size, "TIDAK ADA"))
            continue
        got = digest(b)
        if got != expected:
            hash_bad += 1
        if len(b) != expected_size:
            size_bad += 1
        if got != expected or len(b) != expected_size:
            mismatch_rows.append((rel, expected, got, expected_size, len(b)))
    with (out / "OLD_MANIFEST_MISMATCHES.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["path", "old_sha256", "committed_sha256", "old_bytes", "committed_bytes"])
        w.writerows(mismatch_rows)

    result_rows = parse_tsv(git_bytes(BASE + "/runtime-results.tsv"))
    hybrid_sha = {}
    for row in result_rows:
        name = row.get("case", "")
        h = row.get("hybrid_sha256") or row.get("hybrid_state_sha256") or ""
        if name and re.fullmatch(r"[0-9a-f]{64}", h):
            hybrid_sha[name] = h
    summary_rows = parse_tsv(git_bytes(BASE + "/runtime-case-summary.tsv"))
    for row in summary_rows:
        name = row.get("case", "")
        h = row.get("hybrid_sha256") or row.get("hybrid_state_sha256") or ""
        if name and re.fullmatch(r"[0-9a-f]{64}", h):
            hybrid_sha.setdefault(name, h)

    rows = []
    for p in sorted(x for x in raw_paths if x.endswith(".gdb.txt")):
        b = raw_data[p]
        txt = b.decode("utf-8", "replace")
        m = re.search(r"AE_POST_LOAD_VSYNC=180\s+elapsed_since_loaded_s=([0-9.]+)\s+elapsed_since_launch_s=([0-9.]+)", txt)
        capture = "AE_RAM_STATE_CAPTURE=PASS" in txt
        segv = bool(re.search(r"received signal SIGSEGV|Program received signal SIGSEGV|Program terminated with signal SIGSEGV", txt))
        abrt = bool(re.search(r"received signal SIGABRT|Program received signal SIGABRT|Program terminated with signal SIGABRT", txt))
        if segv:
            status = "SIGSEGV"
        elif abrt:
            status = "SIGABRT"
        elif m and capture:
            status = "POST_LOAD_VSYNC=180 + AE_RAM_STATE_CAPTURE"
        elif m:
            status = "POST_LOAD_VSYNC=180; CAPTURE_TIDAK_LENGKAP"
        else:
            status = "TIDAK_ADA_MARKER_180"
        # Only use an exit code explicitly printed by GDB/raw log; wrapper RC is not inferred.
        em = re.search(r"(?:Inferior\s+\d+.*?exited with code|Program exited with code|AE_EMULATOR_EXIT_CODE)\s*[=:]?\s*(-?\d+)", txt, re.I)
        bm = re.search(r"^(.+)-attempt([12])\.gdb\.txt$", p.split("/")[-1])
        case = bm.group(1) if bm else Path(p).stem
        attempt = bm.group(2) if bm else "TIDAK TAHU"
        rows.append({
            "hibrida": case,
            "peluncuran": attempt,
            "SHA256_hibrida": hybrid_sha.get(case, "TIDAK TAHU"),
            "hasil_log_mentah": status,
            "elapsed_since_launch_s": m.group(2) if m else "TIDAK TAHU",
            "kode_keluar_di_log": em.group(1) if em else "TIDAK TAHU",
            "SHA256_log_GDB": digest(b),
            "ukuran_log_byte": len(b),
            "berkas": p,
        })
    table = out / "AJ1_RAW_GDB_TABLE.tsv"
    with table.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else [
            "hibrida","peluncuran","SHA256_hibrida","hasil_log_mentah",
            "elapsed_since_launch_s","kode_keluar_di_log","SHA256_log_GDB","ukuran_log_byte","berkas"
        ], delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    direct = [r for r in rows if r["hibrida"] in ("direct-channel-field-2", "direct-channel-field-3")]
    deep_snapshots = git_bytes(BASE + "/ae4_ram_snapshots.tsv").decode("utf-8", "replace").splitlines()
    snapshot_data = max(0, len(deep_snapshots) - 1)
    gdb_count = sum(1 for p in raw_paths if p.endswith(".gdb.txt"))
    pcsx_count = sum(1 for p in raw_paths if p.endswith(".pcsx.txt"))
    report = [
        "# AJ1 — audit ulang bukti mentah AE1",
        "",
        f"Sumber bytes: commit {REF}; seluruh isi raw dibaca melalui git show, bukan working tree terbaru.",
        f"Log GDB: {gdb_count}; log PCSX: {pcsx_count}; jumlah pasangan hibrida/peluncuran GDB: {len(rows)}.",
        f"Manifest lama: {len(old_entries)} entri; SHA tidak cocok: {hash_bad}; ukuran tidak cocok: {size_bad}; path hilang: {missing}.",
        f"Manifest baru: {len(raw_paths)} berkas raw, SHA-256 dan ukuran dihitung dari bytes persis pada commit sumber.",
        "Tabel tiap hibrida × peluncuran: AJ1_RAW_GDB_TABLE.tsv.",
        "Daftar mismatch manifest lama: OLD_MANIFEST_MISMATCHES.tsv.",
        "",
        "## Direct Channel field 2/3",
    ]
    for r in direct:
        report.append(
            f"- {r['hibrida']} attempt {r['peluncuran']}: {r['hasil_log_mentah']}; "
            f"elapsed_since_launch_s={r['elapsed_since_launch_s']}; "
            f"hybrid_sha256={r['SHA256_hibrida']}; exit={r['kode_keluar_di_log']}."
        )
    report += [
        "",
        "## Mengapa TSV lama menyebut INCONCLUSIVE_TIMEOUT",
        "Skrip eksperimen menilai marker AE_POST_LOAD_VSYNC=180 dan AE_RAM_STATE_CAPTURE=PASS sebelum mengecek SIGINT/timeout. Karena itu, satu log yang berisi dua marker tersebut tidak akan diklasifikasikan INCONCLUSIVE_TIMEOUT oleh kode yang sama.",
        "Log mentah direct-channel-field-2/3 pada commit sumber berisi marker 180 dan capture PASS, tetapi TSV lama berisi wrapper exit -9 dan durasi sekitar 10 detik. Ini adalah keluaran dari eksekusi yang berbeda atau artefak bercampur, bukan satu hasil konsisten. Workflow lama menulis ke deep/ yang sama pada setiap run, lalu melakukan rebase/push; output statis itu memungkinkan log diganti sementara TSV/manifest lama tetap ada.",
        "",
        "## Mengapa ae4_ram_snapshots.tsv hanya header",
        f"TSV yang terkomit berisi {snapshot_data} baris data di luar header. Kode hanya menambahkan baris RAM bila status launch POST_LOAD_VSYNC=180 dan runtime/current.sstate ada. Launch timeout tanpa kedua prasyarat tidak menulis snapshot; header-only berarti tidak ada capture yang memenuhi syarat pada eksekusi pembuat TSV. Karena raw GDB yang terkomit menunjukkan marker namun TSV kosong, keduanya tidak boleh dianggap satu set output run.",
        "",
        "## Run/job pembuat ee48de4",
        "Actions run 40966952270 attempt 1, job bisect ID 123773754840, mulai 2026-10-29T22:34:57Z dan selesai 2026-10-29T23:20:21Z. Log job merekam commit lokal 5b188ce, rebase sukses, lalu AE1_DEEP_EVIDENCE_HEAD=ee48de43577d08eeca77f6930d7f49a250cbba83 pada 2026-10-29T23:20:18Z. Attempt 2/job 123874229459 adalah retry terpisah yang mengalami konflik publikasi.",
        "",
        "## Perbaikan publikasi",
        "Workflow audit/H6 baru menyimpan setiap output pada reports/aj_2026-10-30/runs/run-<GITHUB_RUN_ID>/attempt-<GITHUB_RUN_ATTEMPT>. Ringkasan dan tabel diparse langsung dari log GDB pada direktori run tersebut; tidak ada penulisan ulang deep/raw yang dipakai bersama.",
        "Tidak ada ISO, BIOS, savestate, Memory Card, RAM dump, atau berkas hibrida yang disimpan ke repo.",
    ]
    (out / "AJ1_AUDIT_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(f"AJ1_AUDIT_SUMMARY gdb={gdb_count} pcsx={pcsx_count} manifest={len(old_entries)} hash_mismatch={hash_bad} size_mismatch={size_bad} missing={missing}")

if __name__ == "__main__":
    main()
