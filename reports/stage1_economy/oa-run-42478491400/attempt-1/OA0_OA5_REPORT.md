# OA0–OA5 — hasil akhir yang dapat diverifikasi

Game: Naruto — Shinobi no Sato no Jintori Gassen (SLPS-03553)
Baseline inklusif: dc7a78f3882ff9c22ae6b09df8b8b8e657bb6137
Source workflow commit: 744a8f2ae7527cf7ef1781667c93735c293acb24
HEAD saat publikasi laporan ini: akan dicatat pada commit publikasi.
Ruang lingkup: OA0–OA3 statis; OA4 hanya dua restore checkpoint CONTROL; tidak ada input gameplay atau watchpoint.

## Status per butir

| Butir | Status | K | Hasil yang dapat dibuktikan |
|---|---|---:|---|
| OA0 | SEBAGIAN | K2 | py_compile 69/69 lulus. Analyzer berhenti dengan exit 1 sebelum validasi offset/decode, audit excerpt agregat, dan penghapusan baris. |
| OA1 | BELUM | K1 | Ghidra/code-listing step selesai, tetapi output analisis tidak berhasil dipublikasikan. Asal a2/a3 semua jalur, caller callee, dan chain scene belum dapat diverifikasi dari artefak akhir. |
| OA2 | BELUM | K1 | Tidak ada audit final yang tersimpan untuk asal s0, semua matrix writer/loader/copy, E3B1C, kesinambungan v0, atau sumber v1 pada sw 0x118($gp). |
| OA3 | BELUM | K1 | Tidak ada hasil final tersimpan untuk CFG fall-through B24C8 dan penelusuran 12 JALR. |
| OA4 | SEBAGIAN | K4 | Dua restore identik berhasil: SaveStateLoaded 1× pada setiap launch, masing-masing 180 VSync, baca wilayah M berhasil, globals identik dan SHA wilayah identik. Nilai TSV individual tidak terselamatkan ke repo. |
| OA5 | BELUM | K1 | x=d belum terbukti; biaya lompatan level d≥2 tetap TIDAK TAHU. Tidak memakai 400/800/1600 dan tidak melakukan fitting. |

Subhasil OA4: **reproducibility CONTROL = TUNTAS K5 untuk dua launch yang diuji**. Status OA4 keseluruhan tetap SEBAGIAN K4 karena enam nilai scalar dan TSV 0x540 byte tidak dapat dipulihkan dari log setelah push publikasi gagal. Tidak ada kesimpulan x=d dari dump.

## Penyebab kegagalan OA0–OA3

Run 42478491400 menjalankan Ghidra step, lalu py_compile 69/69. Analyzer keluar dengan kode 1 pada RunOA0OA5.py baris 540: csv.DictReader diberi delimiter literal "\\t" (dua karakter), sehingga Python melempar TypeError: delimiter must be a 1-character string. Kegagalan terjadi saat membaca NA2_EA88_39EFC_WRITERS.tsv untuk rekonsiliasi summary, sebelum tahap validasi raw/offset/decode, audit union kutipan, dan cleanup kutipan.

Karena itu:
- OA0_FILE_OFFSET_RAW_DECODE_VALIDATION = TIDAK TAHU (tahap tidak tercapai).
- OA0_AGGREGATE_EXCERPT_AUDIT = TIDAK TAHU (tahap tidak tercapai); tidak boleh dinyatakan PASS.
- Baris kutipan JA/KA/LA/MA/NA yang dihapus = 0. Penghapusan tidak dijalankan.
- Kelompok kutipan lama yang sudah diketahui dari laporan NA pada baseline tetap: ENTRY1 0x800B549C..0x800B5517 (124 B), 0x800E4800..0x800E4843 (68 B), 0x800F5E7C..0x800F5EDF (100 B), 0x800F5F14..0x800F5F5B (72 B). Ini adalah hasil NA sebelumnya, bukan hasil agregat OA terbaru.

## OA4 CONTROL — bukti runtime dari log runner

- Checkpoint: adaptive-cycle-02-f180.sstate.
- Source run: 39907655833; artifact 12482055310; metadata valid, expired=false.
- ZIP SHA-256: a0f45156dfd489f24c8dc8e122c33a048c7b9ac34b935ac828523593d21ca2a8.
- Checkpoint SHA-256: 705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35.
- Launch 1: exit 0; SaveStateLoaded=1; post-load VSync=180; M region READ.
- Launch 2: exit 0; SaveStateLoaded=1; post-load VSync=180; M region READ.
- GLOBALS_IDENTICAL=YES.
- M region SHA-256 launch 1 = a6b6b518d8b4eff42275f2dd574a78f5741870fc33cebacc79e27a4602d281a7.
- M region SHA-256 launch 2 = a6b6b518d8b4eff42275f2dd574a78f5741870fc33cebacc79e27a4602d281a7.
- M_REGION_IDENTICAL=YES; GAMEPLAY_INPUT=NONE; WATCHPOINTS=0; RAM_BINARY_EXPORTED=no; COLD_BOOT_FALLBACK=no.
- Isi scalar TSV dan byte TSV tidak ada pada branch karena publikasi commit run ditolak. Karena itu nilai aktual keenam scalar = TIDAK TAHU pada rekaman repo ini.

## Rekonsiliasi NA2 yang bisa dilakukan dari file sumber

NA2_SELECTOR_AND_HELPER_SUMMARY.txt pada NA lama menyebut EA6E_SOURCE_LHU_8013EA88=0. Namun NA2_EA88_39EFC_WRITERS.tsv memiliki tiga baris target 0x8013EA88 dengan source_expression MEM16[0x8013EA6E], yaitu PC 0x800D44F4, 0x800D733C, dan 0x800D7928. Ini dicatat sebagai kontradiksi antar-artefak; summary NA lama tidak diubah. Bukti tersebut tidak cukup untuk menyimpulkan semantik selector atau x=d.

## DN1 — tabel lookup resource yang menjadi data, bukan biaya

DN1 tetap TUNTAS K4: 415 record dari 12 resource, 14 nilai X. Nilai LV1–LV5 konsisten per-X di sampel tersebut. LV2 = 10×ceil(11X/100) cocok 415/415; LV1 dan LV3–LV5 tidak mempunyai rumus universal yang terkonfirmasi. Tabel X→LV tidak membuktikan biaya transaksi upgrade atau nilai x sebagai jarak lompatan.

## Semua run setelah baseline

Rincian seluruh run setelah commit baseline (termasuk monitor terjadwal dan semua workflow yang tidak sengaja terpicu) ada di OA0_RUN_LEDGER.tsv. Empat workflow LA/KA/MA/NA terpicu karena filter lama mereka mencakup **/*.py; trigger tersebut tidak disengaja. Konektor yang tersedia tidak menyediakan aksi pembatalan run. KA, MA, NA menyelesaikan job dan mempublikasikan laporan masing-masing; LA gagal pada push publikasi dengan fetch-first. OA menjalankan dua restore CONTROL, tetapi push publikasi OA juga ditolak fetch-first akibat commit bersamaan.

## Commit ledger dan batas perubahan

OA0_COMMIT_LEDGER.tsv mencantumkan setiap commit dari baseline inklusif sampai publikasi laporan ini beserta daftar berkas A/M/D per commit. Tidak ada workflow lama, STATUS.md, Release, atau biner yang diubah oleh commit setup OA atau commit laporan manual ini. Tidak ada baris lama JA/KA/LA/MA/NA yang dihapus oleh OA karena analyzer berhenti sebelum tahap itu. Bot KA/MA/NA menambah laporan baru di direktori run masing-masing akibat workflow tak sengaja yang terpicu.

## Kesimpulan

Tujuan utama belum tercapai. Formula biaya upgrade petak untuk lompatan d≥2 tetap **BELUM K1 — TIDAK TAHU**. DN1 hanya memberikan nilai lookup X→LV. OA4 memberi bukti repeatability checkpoint CONTROL pada dua launch, tetapi tidak menghubungkan byte matriks dengan dua level, jarak d, atau formula biaya.
