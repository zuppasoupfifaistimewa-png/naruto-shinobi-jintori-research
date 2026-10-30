# AJ1 — audit ulang bukti mentah AE1

Sumber bytes: commit ee48de43577d08eeca77f6930d7f49a250cbba83; seluruh isi raw dibaca melalui git show, bukan working tree terbaru.
Log GDB: 70; log PCSX: 70; jumlah pasangan hibrida/peluncuran GDB: 70.
Manifest lama: 112 entri; SHA tidak cocok: 55; ukuran tidak cocok: 55; path hilang: 0.
Manifest baru: 140 berkas raw, SHA-256 dan ukuran dihitung dari bytes persis pada commit sumber.
Tabel tiap hibrida × peluncuran: AJ1_RAW_GDB_TABLE.tsv.
Daftar mismatch manifest lama: OLD_MANIFEST_MISMATCHES.tsv.

## Direct Channel field 2/3
- direct-channel-field-2 attempt 1: POST_LOAD_VSYNC=180 + AE_RAM_STATE_CAPTURE; elapsed_since_launch_s=60.733078241348; hybrid_sha256=2e67da72470863953558d33180ed859a36745dd84ab1586975b60e8753f4a39c; exit=TIDAK TAHU.
- direct-channel-field-2 attempt 2: POST_LOAD_VSYNC=180 + AE_RAM_STATE_CAPTURE; elapsed_since_launch_s=60.71901845932; hybrid_sha256=2e67da72470863953558d33180ed859a36745dd84ab1586975b60e8753f4a39c; exit=TIDAK TAHU.
- direct-channel-field-3 attempt 1: POST_LOAD_VSYNC=180 + AE_RAM_STATE_CAPTURE; elapsed_since_launch_s=60.67808175087; hybrid_sha256=e5612c3c625b3ac29bf197ed9b652610e0f6d2a1b71d69c9dec02d2e3dcfe1d7; exit=TIDAK TAHU.
- direct-channel-field-3 attempt 2: POST_LOAD_VSYNC=180 + AE_RAM_STATE_CAPTURE; elapsed_since_launch_s=60.661514043808; hybrid_sha256=e5612c3c625b3ac29bf197ed9b652610e0f6d2a1b71d69c9dec02d2e3dcfe1d7; exit=TIDAK TAHU.

## Mengapa TSV lama menyebut INCONCLUSIVE_TIMEOUT
Skrip eksperimen menilai marker AE_POST_LOAD_VSYNC=180 dan AE_RAM_STATE_CAPTURE=PASS sebelum mengecek SIGINT/timeout. Karena itu, satu log yang berisi dua marker tersebut tidak akan diklasifikasikan INCONCLUSIVE_TIMEOUT oleh kode yang sama.
Log mentah direct-channel-field-2/3 pada commit sumber berisi marker 180 dan capture PASS, tetapi TSV lama berisi wrapper exit -9 dan durasi sekitar 10 detik. Ini adalah keluaran dari eksekusi yang berbeda atau artefak bercampur, bukan satu hasil konsisten. Workflow lama menulis ke deep/ yang sama pada setiap run, lalu melakukan rebase/push; output statis itu memungkinkan log diganti sementara TSV/manifest lama tetap ada.

## Mengapa ae4_ram_snapshots.tsv hanya header
TSV yang terkomit berisi 0 baris data di luar header. Kode hanya menambahkan baris RAM bila status launch POST_LOAD_VSYNC=180 dan runtime/current.sstate ada. Launch timeout tanpa kedua prasyarat tidak menulis snapshot; header-only berarti tidak ada capture yang memenuhi syarat pada eksekusi pembuat TSV. Karena raw GDB yang terkomit menunjukkan marker namun TSV kosong, keduanya tidak boleh dianggap satu set output run.

## Run/job pembuat ee48de4
Actions run 40966952270 attempt 1, job bisect ID 123773754840, mulai 2026-10-29T22:34:57Z dan selesai 2026-10-29T23:20:21Z. Log job merekam commit lokal 5b188ce, rebase sukses, lalu AE1_DEEP_EVIDENCE_HEAD=ee48de43577d08eeca77f6930d7f49a250cbba83 pada 2026-10-29T23:20:18Z. Attempt 2/job 123874229459 adalah retry terpisah yang mengalami konflik publikasi.

## Perbaikan publikasi
Workflow audit/H6 baru menyimpan setiap output pada reports/aj_2026-10-30/runs/run-<GITHUB_RUN_ID>/attempt-<GITHUB_RUN_ATTEMPT>. Ringkasan dan tabel diparse langsung dari log GDB pada direktori run tersebut; tidak ada penulisan ulang deep/raw yang dipakai bersama.
Tidak ada ISO, BIOS, savestate, Memory Card, RAM dump, atau berkas hibrida yang disimpan ke repo.
