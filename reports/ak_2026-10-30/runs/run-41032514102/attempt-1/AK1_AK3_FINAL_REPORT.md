# AK1–AK3 — laporan determinisme replay H6 dan pembanding RAM

Run: 41032514102 attempt 1; job: ak1-ak3; source commit: b7f230947d632e024243a4e12f63c9af46c33a2e.

## Skala bukti K0–K5
K0 = tidak ada bukti atau fakta belum diketahui; K1 = petunjuk tunggal/hipotesis yang belum diverifikasi; K2 = observasi eksplisit dari satu artefak atau log tetapi belum dikorroborasi; K3 = beberapa artefak statis yang konsisten dengan provenance yang dapat ditelusuri; K4 = validasi statis independen, byte/digest atau struktur dapat direproduksi dan dibuktikan, tetapi belum ada uji runtime; K5 = pengamatan runtime yang memenuhi kriteria uji dan direplikasi pada sedikitnya dua peluncuran independen. Bukti statis saja maksimal K4.

## AK1 — TUNTAS | K5
H6 two-launch multi-frame capture valid: True. H6 first divergence: TIDAK ADA DIVERGENSI PADA 180/240/360. Tabel lengkap per launch/frame: AK1_REPLAY.tsv; capture 180/240/360, waktu-ke-frame, hash RAM 2 MiB, tiga word, status capture, wrapper exit, dan emulator exit yang tercatat.

## AK2 — TUNTAS | K5
Two-launch H6/control captures valid: True. Bytewise diff summary: AK2_DIFF_SUMMARY.txt; grouped address ranges: AK2_DIFF_RANGES.tsv. Target source vs H6@180 cannot be attributed solely to 180 frames from these data: TIDAK TAHU; no target-native frame-180 replay comparator is present.

## AK3 — TUNTAS | K4
Dua belas SHA hibrida AE2 berikut tetap TIDAK TAHU: ae2-current-bisect-step1 attempt1/2; step2 attempt1/2; step3 attempt1/2; step4 attempt1/2; step5 attempt1/2; ae2-target-current-all-24-control attempt1/2. Re-check: reports/aj_2026-10-30/runs/run-41028457166/attempt-1/AJ1_RAW_GDB_TABLE.tsv dan AJ1_AJ3_COMPLETION_REPORT.md tidak memuat pemetaan digest untuk enam hibrida × dua attempt ini; tidak ada digest nyata di repo untuk dipasangkan. Tidak ada hash hasil tebakan.
Putusan host/RSI: PARKED_GENERAL_SEARCH; allow only pre-registered one-variable host/RSI A/B with >=2 launches/condition; causality=TIDAK TAHU. H6 determinism tidak membuktikan kausalitas host/RSI; A/B terkontrol satu variabel masih diperlukan.

## Exit/status run
AK_SCRIPT_EXIT_CODE=0; H6_SHA256=d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475; timeout_per_launch_s=600.
Emulator exit code dilaporkan hanya bila string exit eksplisit muncul pada GDB/PCSX log; jika tidak, TIDAK TAHU. GDB wrapper exit adalah kolom berbeda.

## Berkas yang dikomit
AK1_FINDING.txt; AK1_REPLAY.tsv; AK2_DIFF_SUMMARY.txt; AK2_DIFF_RANGES.tsv; logs/*.gdb.txt; logs/*.pcsx.txt; ACTIONS_RUN_SUMMARY.txt; AK1_AK3_FINAL_REPORT.md. Tidak ada ISO, BIOS, savestate, Memory Card, dump RAM, atau biner hibrida.
