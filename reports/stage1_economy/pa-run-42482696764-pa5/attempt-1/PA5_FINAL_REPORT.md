# PA5 — uji simbolik dan falsifier H1/H2

Baseline inklusif: 3f730c73dc628d02f360b7ac12961e6f3e4b1584
PA4 data directory: reports/stage1_economy/pa-run-42482696764-pa4/attempt-1
PA4_CONTROL_SNAPSHOTS=TUNTAS K5 (dua restore checkpoint identik)
SCALARS_IDENTICAL=YES
M_REGION_IDENTICAL=YES
M_REGION_BYTES=1344
M_POINTER=2149514168 (0x801EFBB8)
M_REGION_END=0x801F00F7
M_REGION_SHA256_LAUNCH1=a6b6b518d8b4eff42275f2dd574a78f5741870fc33cebacc79e27a4602d281a7
M_REGION_SHA256_LAUNCH2=a6b6b518d8b4eff42275f2dd574a78f5741870fc33cebacc79e27a4602d281a7

## Pemeriksaan snapshot desimal
Keenam scalar yang direkonsiliasi:
- M pointer 0x8013EA74 = 2149514168
- I selector 0x8013EA6E = 0
- B scalar 0x8013EB1C = 0
- 0x8013EA88 = 5
- 0x80139EFC = 0
- gp+0x118 (0x8006D794) = 52

Kedua TSV scalar identik. Kedua TSV M mempunyai header ram_addr/values_dec, masing-masing 1344 baris nilai byte, alamat berurutan [0x801EFBB8,0x801F00F7], seluruh nilai dalam rentang u8, dan isi file sama persis.
Catatan: job PA5 pertama gagal mengonsumsi data karena parser .upper() mengubah prefix 0x menjadi 0X. Pemeriksaan koreksi ini membaca ulang file yang sudah dipublikasikan menggunakan normalisasi prefix yang mempertahankan 0x; tidak mengubah hasil mentah PA4. Hotfix parser PA5 berada di tools/pa/RunPA5Symbolic.pytxt (commit 2c6fd1e7b51274945ed9cf2ec8dd465743225df4).

## Uji hipotesis
H1 (x=d): **BELUM K1 — TIDAK DAPAT DIUJI.** Snapshot ini hanya satu checkpoint yang diulang. Tidak ada transaksi berlabel jarak lompatan d dan nilai x. Falsifier: transaksi terikat dengan x!=d, atau x tetap saat d berubah.
H2 (x=effect_id): **BELUM K1 — TIDAK DAPAT DIUJI.** Tidak ada label semantik effect_id atau pemetaan ID->x terkonfirmasi. Falsifier: ID sama memetakan x berbeda, atau prediksi dari ID gagal pada sampel terpisah.
Kesamaan isi RAM adalah bukti repeatability checkpoint saja; setiap korelasi byte terhadap kandidat ID atau nilai petak tetap hanya KORELASI, bukan bukti semantik.

## Formula biaya
Biaya upgrade petak untuk lompatan d>=2: **BELUM K1 — TIDAK TAHU**. Belum ada relasi simbolik debit/charge yang ditutup. Tidak menggunakan angka 400/800/1600 dan tidak melakukan fitting.

## Ledger
PA5_RUN_LEDGER.tsv dan PA5_COMMIT_LEDGER.tsv merekam seluruh run Actions dan commit baseline-inclusive. Hasil job PA5 awal (termasuk status publikasi) ada di ACTIONS_RUN_SUMMARY.txt; parser yang dipakai job tersebut masih versi sebelum hotfix, sehingga rekonsiliasi scalar dan M region dikoreksi dari TSV PA4 yang telah dipublikasikan.

## Commit file list
Koreksi PA5 ini mengubah:
- M reports/stage1_economy/pa-run-42482696764-pa5/attempt-1/PA5_FINAL_REPORT.md
- M reports/stage1_economy/pa-run-42482696764-pa5/attempt-1/PA5_SYMBOLIC_COST_STATUS.tsv
- M reports/stage1_economy/pa-run-42482696764-pa5/attempt-1/PA5_CONTROL_SCALAR_RECONCILIATION.tsv
- A reports/stage1_economy/pa-run-42482696764-pa5/attempt-1/PA5_RECHECK_SUMMARY.txt
- A reports/stage1_economy/pa-run-42482696764-pa5/attempt-1/PA5_RECHECK_COMMIT_FILES.tsv
