# Ringkasan akhir AU0–AU3 — 1 November 2026

Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`, branch `main`.  
Base audit: `a065e7d2a8932569a4e0a819e5562b365bb29c6e`.  
HEAD sumber inventaris (sebelum update laporan induk): `e7925cfcd69c6487a5bb2ab8cce672b5a589a099`.  
Perbandingan base→HEAD sumber inventaris: 84 commit maju, 0 di belakang; 114 berkas berbeda. Daftar di bawah adalah padanan `git diff --name-status` (A=added, M=modified, D=deleted); semua 114 path termasuk artefak AU3.

## Status pekerjaan

| AU | Status | Tingkat bukti | Hasil ringkas |
|---|---|---|---|
| AU0 | TUNTAS | K5 terbatas | Replikasi AT3 41259662960 identik pada tiga artefak; kegagalan infrastruktur dan perbedaan A/C dicatat. |
| AU1 | TUNTAS | K4 statis; K5 runtime terbatas | Disassembly penuh setter/getter (28/16 instruksi); klaim operand getter dikoreksi dan konsisten dengan event runtime. |
| AU2 | TUNTAS | K4 | Seluruh 14 setter memiliki asal instruksi a0/a1, PC, fungsi, dan ekspresi simbolik; tanpa tafsir ekonomi. |
| AU3 | TUNTAS | K5 terbatas | Empat launch interpreter sukses; 12/12 snapshot PASS; input A PASS; Memory Card tetap; nol hit setter/helper hanya untuk window frame 1–600. |

### AU0 — perbaikan laporan dan pemeriksaan AT3

Run replikasi **41259662960**, job **124710123732**, source SHA `968c1a55731e09f815a1d1d385e1bf3edf792279`, status PASS, exit code desimal **0**. FRAMES/HITS/EVENTS byte-identik terhadap run 41256458701. SHA-256 konten penuh:
- FRAMES: `2203119098ab42d1f914f426a7a87bd4db960867e5c526c12bfbe79c8138039b`
- HITS: `0f86efe06cdb366231953af711176db5ba113bfdcc0e0b85eccbac1f653031b6`
- EVENTS: `fa58b5a2dc74945267a7aefb2e97348d448daffc9664572aaa22642b14366cff`

Pada K2, jadwal C dan A (dua launch per jadwal) masing-masing mencatat getter 720 hit dan getter-return 720; setter/helper masing-masing 0 pada window frame 180–360. Nol hit bukan bukti fungsi tidak digunakan di luar window.

Run gagal yang tetap dicatat sebagai kegagalan infrastruktur, bukan bukti game:
- **41256334815**, job 124700189639, source SHA `832ccdfe2cc15f0622be23fbfff33f8d104e0a6a`, exit 1: parser menolak jadwal B, emulator belum berjalan.
- **41256208915**, job 124699799885, source SHA `390e989e87840232ee30fb3bc5a2aaf831a3419a`, exit 22: HTTP 401 saat precheck checkpoint; emulator belum berjalan.
- **41258300049**: executable path salah, subprocess 127; diperbaiki sebelum replikasi 41259662960.

### AT2 — perbandingan dynarec/interpreter

Run **41256330348**, job **124700159848**, source SHA `9e5a60cb468593c7d9049691d55f687e059066e5`, exit code 0. Seluruh eksperimen H6 **HIBRIDA** (target checkpoint sebagai dasar + CONTROL protobuf field 6), bukan target murni:
- F1 `-dynarec`: dua launch cocok dengan baseline AK1 pada RAM 2 MiB frame 180/240/360.
- F2 `-interpreter`: dua launch cocok dengan baseline AS3 K0 pada frame sama.
- Terbukti hanya kecocokan byte snapshot pada titik capture tersebut, bukan seluruh runtime atau makna ekonomi/gameplay.

### AU1 — getter dan setter lengkap

Ghidra run **41274567492**, job **124754117941**, source SHA `7def692176e0ac7e21bff0d4a9a5eca8baf70880`, exit code 0. Getter `0x800138EC): a0 masuk adalah indeks; instruksi pertama `move a1,a0` menyalin indeks ke a1 dan menimpa a1 caller-supplied; callee membentuk pointer record di a0. Setter `0x8001387C): a0 indeks, a1 nilai; nilai dibatasi `-9999..99999`; store word ke `0x80070EA0 + index*0xB4 + 0x18`. Field `+0x18` tidak diberi makna ekonomi.

### AU2 — 14 caller setter

Tuntas K4. Berkas `AU2_SETTER_ARGUMENTS_2026-11-01.tsv` menyimpan semua 14 PC, fungsi caller, instruksi asal a0, instruksi asal/bentuk akhir a1, serta ekspresi simbolik dan konstanta literal. Tidak ada label chakra/biaya/ekonomi yang ditambahkan tanpa bukti instruksi.

### AU3 — runtime setter/helper (selesai)

Run **41274625876**, job **124754181385**, source SHA `214d6641b67b035300d7d8efbd117318d7a3f81b`, status `success`, exit code desimal **0**. H6 **HIBRIDA**, SHA-256 `d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475`. Interpreter `-debugger -interpreter`; breakpoint **hanya** setter `0x8001387C` dan helper `0x800B770C`, getter off; aktif frame 1–600.

| Jadwal/launch | Exit emulator | Wall time (s) | Readback CIRCLE | Memory Card |
|---|---:|---:|---|---|
| C/1 | 0 | 241.088 | Tidak berlaku | Tidak berubah |
| C/2 | 0 | 240.482 | Tidak berlaku | Tidak berubah |
| A/1 | 0 | 240.669 | Press/release PASS | Tidak berubah |
| A/2 | 0 | 240.903 | Press/release PASS | Tidak berubah |

Timeout 1800 detik, >=2x waktu terlama 241.088 detik. 12/12 snapshot PASS di frame 180/360/600. Dalam masing-masing jadwal, hash dua launch identik di semua frame; A dan C berbeda di semua frame yang dibandingkan. Setter/helper masing-masing 0 hit di C dan A, dan file event hanya header. Itu hanya nol hit pada window/kondisi ini, bukan bukti tidak pernah dipanggil.

Laporan rinci dengan seluruh 12 hash RAM: `AU3_RUNTIME_AUDIT_2026-11-01.md`. Ringkasan Actions: `au3-setter-helper-run-41274625876/attempt-1/ACTIONS_RUN_SUMMARY.txt`.

## Pembatasan bukti

- H6 selalu dilabeli **HIBRIDA**, bukan target-pure.
- Statis/disassembly maksimum K4.
- K5 hanya berlaku untuk kondisi dengan sedikitnya dua peluncuran, dan hanya pada objek/jendela yang diuji.
- Hash snapshot tidak menetapkan sebab perubahan atau makna data.
- Nol hit bukan bukti routine tidak pernah dipakai.
- Tidak ada interpretasi ekonomi tanpa bukti instruksi.
- Visibilitas repo dan Release tidak diubah; tidak ada ISO, BIOS, savestate, RAM dump, video, atau frame biner dikomit.

## Daftar semua berkas berubah sejak base

Padanan `git diff --name-status` dari base `a065e7d2a8932569a4e0a819e5562b365bb29c6e` ke HEAD sumber `e7925cfcd69c6487a5bb2ab8cce672b5a589a099` (A=added, M=modified, D=deleted):
A	`.github/workflows/at1-entry1-helper-a1-provenance.yml`
A	`.github/workflows/at2-h6-flags-ab.yml`
A	`.github/workflows/at3-an2-schedule-k0-k2.yml`
A	`.github/workflows/au3-setter-helper-interpreter.yml`
M	`.github/workflows/step4-helper-return-static-audit.yml`
M	`.github/workflows/step7-entry1-buffer-base-audit.yml`
A	`experiments/at2_h6_flags_ab.py`
A	`experiments/at3_an2_schedule_k0_k2.py`
A	`experiments/au3_setter_helper_interpreter.py`
A	`reports/stage1_economy/AT1_A1_HELPER_PROVENANCE_AUDIT_2026-11-01.md`
A	`reports/stage1_economy/AT1_FIELD_DIFF_2026-11-01.tsv`
A	`reports/stage1_economy/AT1_FIELD_DIFF_PC_FUNCTION.tsv`
A	`reports/stage1_economy/AT1_FIELD_DIFF_SUMMARY.tsv`
A	`reports/stage1_economy/AT1_GETTER_CALLS.tsv`
A	`reports/stage1_economy/AT1_GETTER_CALLS_RECONCILED_2026-11-01.tsv`
A	`reports/stage1_economy/AT1_SETTER_CALLS.tsv`
A	`reports/stage1_economy/AT1_SETTER_CALLS_RECONCILED_2026-11-01.tsv`
A	`reports/stage1_economy/AT1_STATIC_AUDIT_2026-11-01.md`
A	`reports/stage1_economy/AT1_STATIC_FINAL_REPORT_2026-11-01.md`
A	`reports/stage1_economy/AT2_RUNTIME_AUDIT_2026-11-01.md`
A	`reports/stage1_economy/AT3_RUNTIME_AUDIT_2026-11-01.md`
A	`reports/stage1_economy/AU0_FINAL_REPORT_2026-11-01.md`
A	`reports/stage1_economy/AU1_ACCESSOR_DISASSEMBLY_2026-11-01.md`
A	`reports/stage1_economy/AU2_SETTER_ARGUMENTS_2026-11-01.tsv`
A	`reports/stage1_economy/AU3_RUNTIME_AUDIT_2026-11-01.md`
A	`reports/stage1_economy/aq1-run-41258690146/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/aq1-run-41258690146/attempt-1/aq1-deep-context.tsv`
A	`reports/stage1_economy/aq1-run-41258690146/attempt-1/aq1-economy-census.tsv`
A	`reports/stage1_economy/aq1-run-41258690146/attempt-1/aq1-recount.txt`
A	`reports/stage1_economy/aq1-run-41258690146/attempt-1/entry1-buffer-base-targets.txt`
A	`reports/stage1_economy/aq1-run-41258690146/attempt-1/helper-a1-provenance-status.txt`
A	`reports/stage1_economy/aq1-run-41258690146/attempt-1/input-identity.txt`
A	`reports/stage1_economy/aq1-run-41258690146/attempt-1/run-summary.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41258009379/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41258067708/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41258067708/attempt-1/AT1_HELPER_A1_DETAIL.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41258067708/attempt-1/analysis-status.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41258067708/attempt-1/ghidra-exit.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41258067708/attempt-1/input-identity.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41260683654/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41260683654/attempt-1/AT1_HELPER_A1_DETAIL.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41260683654/attempt-1/analysis-status.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41260683654/attempt-1/ghidra-exit.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41260683654/attempt-1/input-identity.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41260751877/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41260751877/attempt-1/AT1_HELPER_A1_DETAIL.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41260751877/attempt-1/analysis-status.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41260751877/attempt-1/ghidra-exit.txt`
A	`reports/stage1_economy/at1-entry1-helper-a1-provenance-run-41260751877/attempt-1/input-identity.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41257708406/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41257708406/attempt-1/ANALYSIS_STATUS.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41257708406/attempt-1/input-identity.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41257708406/attempt-1/seed-helper-detail.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41258911810/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41258911810/attempt-1/input-identity.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41258911810/attempt-1/seed-helper-detail.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41259079319/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41259079319/attempt-1/input-identity.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41259079319/attempt-1/seed-helper-detail.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41260739233/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41260739233/attempt-1/input-identity.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41260739233/attempt-1/seed-helper-detail.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41274555827/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41274555827/attempt-1/input-identity.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41274555827/attempt-1/seed-helper-detail.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41274567492/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41274567492/attempt-1/AU1_ACCESSOR_EXPORT_SUMMARY.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41274567492/attempt-1/input-identity.txt`
A	`reports/stage1_economy/at1-helper-a1-audit-run-41274567492/attempt-1/seed-helper-detail.txt`
A	`reports/stage1_economy/at2-h6-flags-run-41256208915/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at2-h6-flags-run-41256330348/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at2-h6-flags-run-41256330348/attempt-1/AT2_BASELINE_COMPARISON.tsv`
A	`reports/stage1_economy/at2-h6-flags-run-41256330348/attempt-1/AT2_FRAMES.tsv`
A	`reports/stage1_economy/at2-h6-flags-run-41256330348/attempt-1/AT2_LAUNCHES.tsv`
A	`reports/stage1_economy/at2-h6-flags-run-41256330348/attempt-1/AT2_SCRIPT_EXIT_CODE.txt`
A	`reports/stage1_economy/at2-h6-flags-run-41256330348/attempt-1/AT2_SUMMARY.txt`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256295999/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256334815/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256334815/attempt-1/AT3_BREAKPOINT_EVENTS.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256334815/attempt-1/AT3_FRAMES.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256334815/attempt-1/AT3_HIT_COUNTS.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256334815/attempt-1/AT3_LAUNCHES.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256334815/attempt-1/AT3_SCRIPT_EXIT_CODE.txt`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256334815/attempt-1/AT3_SUMMARY.txt`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256458701/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256458701/attempt-1/AT3_BREAKPOINT_EVENTS.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256458701/attempt-1/AT3_FRAMES.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256458701/attempt-1/AT3_HIT_COUNTS.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256458701/attempt-1/AT3_LAUNCHES.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256458701/attempt-1/AT3_SCRIPT_EXIT_CODE.txt`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41256458701/attempt-1/AT3_SUMMARY.txt`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41258300049/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41258300049/attempt-1/AT3_BREAKPOINT_EVENTS.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41258300049/attempt-1/AT3_FRAMES.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41258300049/attempt-1/AT3_HIT_COUNTS.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41258300049/attempt-1/AT3_LAUNCHES.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41258300049/attempt-1/AT3_SCRIPT_EXIT_CODE.txt`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41258300049/attempt-1/AT3_SUMMARY.txt`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41259662960/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41259662960/attempt-1/AT3_BREAKPOINT_EVENTS.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41259662960/attempt-1/AT3_FRAMES.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41259662960/attempt-1/AT3_HIT_COUNTS.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41259662960/attempt-1/AT3_LAUNCHES.tsv`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41259662960/attempt-1/AT3_SCRIPT_EXIT_CODE.txt`
A	`reports/stage1_economy/at3-an2-schedule-k0-k2-run-41259662960/attempt-1/AT3_SUMMARY.txt`
A	`reports/stage1_economy/au3-setter-helper-run-41274625876/attempt-1/ACTIONS_RUN_STATUS.txt`
A	`reports/stage1_economy/au3-setter-helper-run-41274625876/attempt-1/ACTIONS_RUN_SUMMARY.txt`
A	`reports/stage1_economy/au3-setter-helper-run-41274625876/attempt-1/AT3_SCRIPT_EXIT_CODE.txt`
A	`reports/stage1_economy/au3-setter-helper-run-41274625876/attempt-1/AU3_BREAKPOINT_EVENTS.tsv`
A	`reports/stage1_economy/au3-setter-helper-run-41274625876/attempt-1/AU3_FRAMES.tsv`
A	`reports/stage1_economy/au3-setter-helper-run-41274625876/attempt-1/AU3_HIT_COUNTS.tsv`
A	`reports/stage1_economy/au3-setter-helper-run-41274625876/attempt-1/AU3_LAUNCHES.tsv`
A	`reports/stage1_economy/au3-setter-helper-run-41274625876/attempt-1/AU3_SCRIPT_EXIT_CODE.txt`
A	`reports/stage1_economy/au3-setter-helper-run-41274625876/attempt-1/AU3_SUMMARY.txt`
