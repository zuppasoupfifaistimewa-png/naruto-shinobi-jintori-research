# Ringkasan akhir AU0–AU3 — 1 November 2026

Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`, branch `main`.  
Base audit: `a065e7d2a8932569a4e0a819e5562b365bb29c6e`.  
HEAD sumber sebelum file laporan ini dibuat: `4e71d5eb9e9d1cafade9508b534d8f80a684ad2e`.  
Perbandingan GitHub base→HEAD sumber: 69 commit maju, 0 di belakang; 103 berkas berbeda. Status di daftar menggunakan padanan `git diff --name-status` (A=added, M=modified, D=deleted). Laporan ini sendiri menambahkan satu berkas lagi.

## Status pekerjaan

| AU | Status | Tingkat bukti | Hasil ringkas |
|---|---|---|---|
| AU0 | TUNTAS | K5 terbatas | Laporan AT2/AT3 direkonsiliasi; run AT3 41259662960 mereplikasi tiga file hasil secara identik; dua kegagalan infrastruktur dicatat; jadwal A/C dibandingkan. |
| AU1 | TUNTAS | K5 untuk getter runtime; K4 untuk disassembly | Badan penuh setter/getter diekspor (28 dan 16 instruksi); klaim getter lama dikoreksi; register runtime konsisten dengan indeks a0 dan pointer record return a0. |
| AU2 | TUNTAS | K4 | Tabel 14 setter berisi instruksi asal a0/a1 dan ekspresi simbolik + konstanta; tanpa tafsir ekonomi. |
| AU3 | SEBAGIAN | K0 sampai run berakhir | Workflow runtime telah mulai, prasyarat lolos, tetapi langkah emulator masih berlangsung pada pemeriksaan terakhir; belum ada hasil AU3 yang dapat dinyatakan. |

### AU0 — perbaikan laporan dan pemeriksaan AT3

Run replikasi: **41259662960**, job **124710123732**, status PASS, source SHA `968c1a55731e09f815a1d1d385e1bf3edf792279`, kode keluar desimal **0**.

Git blob SHA-1 (40 digit) FRAMES/HITS/EVENTS sama antara run 41256458701 dan 41259662960; isi masing-masing file juga byte-identik. SHA-256 konten lengkap (64 digit):
- FRAMES: `2203119098ab42d1f914f426a7a87bd4db960867e5c526c12bfbe79c8138039b`
- HITS: `0f86efe06cdb366231953af711176db5ba113bfdcc0e0b85eccbac1f653031b6`
- EVENTS: `fa58b5a2dc74945267a7aefb2e97348d448daffc9664572aaa22642b14366cff`

Pada K2, masing-masing jadwal C dan A (dua launch per jadwal) mencatat getter 720 hit dan getter-return 720; setter dan helper masing-masing 0 pada window frame 180–360. K0 tidak memantau breakpoint. Nol hit bukan bukti fungsi tidak digunakan di luar window ini. Hash RAM 2 MiB A berbeda dari C pada frame 180/240/360; nilai lengkap ada di laporan AT3.

Run gagal:
- 41256334815, job 124700189639, source SHA `832ccdfe2cc15f0622be23fbfff33f8d104e0a6a`, exit 1: parser menolak jadwal B, emulator belum berjalan.
- 41256208915, job 124699799885, source SHA `390e989e87840232ee30fb3bc5a2aaf831a3419a`, exit 22: HTTP 401 saat precheck unduhan checkpoint; emulator belum berjalan.
- 41258300049: path executable salah, subprocess 127; diperbaiki sebelum replikasi sukses 41259662960.

### AT2 — flag emulator

Run **41256330348**, job **124700159848**, source SHA `9e5a60cb468593c7d9049691d55f687e059066e5`, exit code desimal **0**. Seluruh eksperimen menggunakan H6 **HIBRIDA** (checkpoint target sebagai dasar + CONTROL protobuf field 6), bukan target murni.

- F1 `-dynarec`: dua launch cocok dengan baseline AK1 pada RAM 2 MiB frame 180/240/360.
- F2 `-interpreter`: dua launch cocok dengan baseline AS3 K0 pada frame yang sama.
- Terbukti hanya kesamaan snapshot byte pada titik itu, bukan kesamaan seluruh runtime atau makna ekonomi/gameplay.

### AU1 — koreksi getter dan disassembly

Ghidra run **41274567492**, job **124754117941**, source SHA `7def692176e0ac7e21bff0d4a9a5eca8baf70880`, exit code desimal **0**. Full getter `0x800138EC`: a0 masuk adalah indeks; instruksi pertama `move a1,a0) menimpa a1 caller-supplied; callee membentuk pointer record di a0. Full setter `0x8001387C): a0 indeks, a1 nilai; batas nilai `-9999..99999`, store word di `0x80070EA0 + index*0xB4 + 0x18`. Field `+0x18) tidak diberi makna ekonomi oleh laporan ini.

### AU3 — runtime terpisah

Run **41274625876**, job **124754181385**, source SHA `214d6641b67b035300d7d8efbd117318d7a3f81b`. Pada pemeriksaan terakhir, status `in_progress`; semua langkah setup (emulator, disc, BIOS, checkpoint, CONTROL, Memory Card, Xvfb) lulus dan langkah eksekusi empat launch sedang berlangsung. Desain: interpreter, C/no-input dan A/CIRCLE frame 60–61, dua launch per jadwal; breakpoint hanya setter `0x8001387C) dan helper `0x800B770C), getter off; window frame 1–600; RAM 2 MiB di 180/360/600. Timeout per launch 1800 detik. Tidak ada hit count, RAM hash, exit code, atau kesimpulan AU3 yang dilaporkan sebelum artefak Actions tersedia.

## Pembatasan bukti

- H6 selalu merujuk H6 **HIBRIDA**, bukan target-pure.
- Static/disassembly maksimum K4.
- K5 dibatasi pada kondisi yang memiliki sedikitnya dua launch dan hanya pada objek/jendela yang diamati.
- Hash snapshot menunjukkan identitas byte pada snapshot itu; tidak menetapkan sebab perubahan atau makna data.
- Nol hit bukan bukti bahwa routine tidak pernah dipakai.
- Tidak ada interpretasi ekonomi tanpa bukti instruksi.
- Visibilitas repo dan Release tidak diubah. Tidak ada ISO, BIOS, savestate, RAM dump, video, atau frame biner dimasukkan ke commit AU0–AU3.

## Daftar semua berkas berubah sejak base

`git diff --name-status` padanan GitHub Compare base `a065e7d2a8932569a4e0a819e5562b365bb29c6e` → HEAD sumber di atas:
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
A	`reports/stage1_economy/AU1_ACCESSOR_DISASSEMBLY_2026-11-01.md`
A	`reports/stage1_economy/AU2_SETTER_ARGUMENTS_2026-11-01.tsv`
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
A	`reports/stage1_economy/AU0_FINAL_REPORT_2026-11-01.md` (berkas laporan ini)
