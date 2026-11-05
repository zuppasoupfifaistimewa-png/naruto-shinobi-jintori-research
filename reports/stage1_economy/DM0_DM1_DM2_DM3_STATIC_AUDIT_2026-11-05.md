# DM0–DM3 — audit statis LV writer dan selector resource
Tanggal: 5 November 2026  
Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`  
HEAD awal sebelum publikasi audit ini: `6fa859e1f9cfdad7b968cd0df36f19a7fe50a5c1`  
Metode: file teks, TSV census, dan disassembly MIPS statis. Tanpa game/emulator, BIOS, savestate, ISO, dump, video, frame, dan tanpa Actions.

## Ringkasan status

| Tugas | Status | K | Putusan |
|---|---|---:|---|
| DM0 ledger | TUNTAS | K4 | 1 commit inklusif; 1 manusia, 0 bot. |
| DM1 writer LV | SEBAGIAN | K2–K4 | 331 candidate WRITE di census (bukan 326); 10 LOADER_COPY terverifikasi, 274 stack-local, 47 base alias belum terbukti, 0 COMPUTED yang terkonfirmasi. |
| DM2 formula LV3–LV5 | SEBAGIAN | K3 | H1 15/39 dan H2 1/39 per-level; tidak ada 13/13 X. |
| DM3 selector dan Stage 1 | SEBAGIAN | K4 / K0 | Dua writer langsung 0x80070CD0 ditemukan K4; selector untuk Story Mode Stage 1 tetap TIDAK TAHU K0. |

K4 adalah batas statis. Tidak ada K5.

## DM0 — ledger

Rentang inklusif: `6fa859e1f9cfdad7b968cd0df36f19a7fe50a5c1` sampai HEAD yang sama sebelum publikasi laporan ini. Git compare `6fa859e1f9cfdad7b968cd0df36f19a7fe50a5c1^...${base}` menghasilkan ahead_by=1, behind_by=0, total_commits=1; cocok dengan `git rev-list --count 6fa859e1f9cfdad7b968cd0df36f19a7fe50a5c1^..6fa859e1f9cfdad7b968cd0df36f19a7fe50a5c1`.

| SHA | Penulis | Pesan |
|---|---|---|
| `6fa859e1f9cfdad7b968cd0df36f19a7fe50a5c1` | MANUSIA — zuppasoupfifaistimewa-png | Record DL0-DL3 static audit and corrected commit ledger |

Total 1 commit: **1 MANUSIA + 0 BOT**. Satu file yang diubah: `reports/stage1_economy/DL0_DL1_DL2_DL3_AUDIT_2026-11-05.md`.

TSV: `reports/stage1_economy/DM0_COMMIT_LEDGER_2026-11-05.tsv`.

## DM1 — census penulis +0x10..+0x18

Input `aq1-economy-census.tsv` pada `6fa859e1f9cfdad7b968cd0df36f19a7fe50a5c1` berisi FIELD/WRITE:
| Offset | Candidate PC |
|---|---:|
| +0x10 | 148 |
| +0x12 | 13 |
| +0x14 | 65 |
| +0x16 | 7 |
| +0x18 | 98 |
| **Jumlah** | **331** |

PC unik = 331. Jumlah 326 dan “208 belum terselesaikan” dari permintaan tidak berhasil direproduksi dari file census ini; saya tidak menyesuaikan jumlah dengan dugaan.

| Klasifikasi hasil verifikasi | Jumlah |
|---|---:|
| LOADER_COPY terverifikasi | 10 |
| LAIN — base `sp` (stack local/save/temporary) | 274 |
| LAIN — base non-stack, alias ke tile belum terbukti | 47 |
| COMPUTED terkonfirmasi | 0 |
| Total candidate PC | 331 |

**Sepuluh PC loader** pada `FUN_800F7ADC`: `0x800F7CE8`, `0x800F7CFC`, `0x800F7D0C`, `0x800F7D20`, `0x800F7D30`, `0x800F7D44`, `0x800F7D54`, `0x800F7D68`, `0x800F7D78`, `0x800F7D8C`. Ini menyalin little-endian u16 dari source cursor +0x0A/+0x0C/+0x0E/+0x10/+0x12 ke tile +0x10/+0x12/+0x14/+0x16/+0x18. Untuk masing-masing, TSV memuat 12 instruksi pra-store dan byte instruksinya. Pola low byte, load high byte, shift 8, OR, store setengahword menunjukkan copy, bukan formula dari X.

Untuk 274 kandidat `(sp)`, offset itu adalah stack slot. Untuk 47 kandidat non-stack, census hanya menyatakan displacement dan tidak membuktikan register base adalah tile base dengan stride 0x124; pre-store 12 ditandai tidak tersedia alih-alih diisi rekaan. Karena itu DM1 **SEBAGIAN**: saya tidak menyebut 47 itu computed tile writer dan tidak menyimpulkan COMPUTED tidak ada di luar cakupan.

**Falsifier tabel tersimpan:** satu writer non-loader yang base-nya terbukti tile+record×0x124, menghitung nilai, lalu menimpa LV sebelum reader memakainya. Belum ada falsifier seperti itu pada bukti yang bisa diaudit di snapshot ini.

TSV semua 331 kandidat: `reports/stage1_economy/DM1_TILE_LEVEL_WRITER_CENSUS_2026-11-05.tsv`.

## DM2 — uji dua hipotesis rekursif baru

Sumber: DK1 loader-mapped, 12 resource, 415 record, 248 nonzero, 13 X berbeda: 60,100,120,140,160,180,200,220,240,260,280,300,320. Formula ditetapkan sebelum scoring; tidak ada fitting dari kurang dari 3 titik.

- **H1:** LV berikutnya = nearest-5-half-up(2.0 × level prediksi sebelumnya), diterapkan rekursif dari LV2 ke LV3→LV4→LV5.
- **H2:** LV berikutnya = ceil-to-10(1.9 × level prediksi sebelumnya), diterapkan rekursif.

| Hipotesis | LV3 | LV4 | LV5 | Total | 3 level cocok sekaligus |
|---|---:|---:|---:|---:|---:|
| H1 | 6/13 | 5/13 | 4/13 | 15/39 | 3/13 |
| H2 | 1/13 | 0/13 | 0/13 | 1/39 | 0/13 |

Tidak ada yang lulus 13/13.

| X | Observed LV3/LV4/LV5 | H1 prediksi | H1 | H2 prediksi | H2 |
|---:|---|---|---|---|---|
| 60 | 135/265/530 | 140/280/560 | G/G/G | 140/270/520 | G/G/G |
| 100 | 220/440/880 | 220/440/880 | L/L/L | 210/400/760 | G/G/G |
| 120 | 265/530/1050 | 280/560/1120 | G/G/G | 270/520/990 | G/G/G |
| 140 | 310/620/1250 | 320/640/1280 | G/G/G | 310/590/1130 | L/G/G |
| 160 | 360/710/1410 | 360/720/1440 | L/G/G | 350/670/1280 | G/G/G |
| 180 | 390/800/1600 | 400/800/1600 | G/L/L | 380/730/1390 | G/G/G |
| 200 | 440/880/1760 | 440/880/1760 | L/L/L | 420/800/1520 | G/G/G |
| 220 | 490/980/1940 | 500/1000/2000 | G/G/G | 480/920/1750 | G/G/G |
| 240 | 530/1050/2120 | 540/1080/2160 | G/G/G | 520/990/1890 | G/G/G |
| 260 | 580/1150/2290 | 580/1160/2320 | L/G/G | 560/1070/2040 | G/G/G |
| 280 | 620/1240/2470 | 620/1240/2480 | L/L/G | 590/1130/2150 | G/G/G |
| 300 | 660/1320/2640 | 660/1320/2640 | L/L/L | 630/1200/2280 | G/G/G |
| 320 | 710/1410/2820 | 720/1440/2880 | G/G/G | 690/1320/2510 | G/G/G |

Falsifier untuk setiap hipotesis universal: satu nilai observed berbeda dari prediksi rekursifnya; kedua hipotesis sudah difalsifikasi. H1 masih kandidat parsial, bukan rumus terverifikasi. H2 praktis gugur pada data ini.

TSV skor per X dan per level: `reports/stage1_economy/DM2_LV3_LV5_NEW_HYPOTHESES_2026-11-05.tsv`.

## DM3 — penulis selector 0x80070CD0

XREF statis langsung menunjukkan dua store dan satu read:
- **PC 0x800127E8, FUN_80012780:** `sb v0,0x50(s0)`; s0 = 0x80070C80, sehingga tujuan 0x80070CD0. v0 berasal dari byte pertama config row `0x80064918 + ((param1 & 0xFF) × 0x30)`. Kondisi parameter low byte; caller/ikatan mode-state untuk parameter ini belum ditemukan.
- **PC 0x80012F4C, FUN_80012EAC:** `sb v0,0x50(s1)`; s1 = 0x80070C80. v0 berasal dari byte pertama row `0x80057798 + config_index×0x54`. config_index dibaca dari matriks `0x80058758 + 4×(33×mode + 3×state)`, dengan mode = u32[0x80070734] dan state = u8[0x8007073C]. Ini writer langsung yang jelas bergantung pada pasangan mode/state.
- **Reader:** PC 0x800129E8, FUN_800129E4, `lbu v0,0xCD0(v0)`.

Matriks selector memiliki 2.844 baris; 2.816 berisi selector nonblank. Distribusi: `0:2723; 1:11; 2:13; 3:10; 4:17; 5:2; 6:4; 8:1; 9:4; 15:7; 16:14; 17:10`. Contoh: mode 65/state 4 → selector 8 → resource 0x27E/Entry 638. Ini tidak membuktikan Stage 1.

Hipotesis untuk Stage 1:
- **HA:** selector 5 → resource 0x27B/Entry 635. Falsifier: jalur Stage1 → mode/state → matrix/config terbukti menghasilkan selain 5.
- **HB:** selector 0 → resource 0x276/Entry 630. Falsifier: jalur Stage1 terbukti menghasilkan byte selain 0. H6 mode/state 0/0 adalah diagnosis terpisah, bukan bukti Story Mode Stage 1.
- **HC (kandidat pembanding):** mode65/state4 → selector8 → 0x27E; falsifier: pasangan Stage 1 bukan mode65/state4 atau selector hasilnya berbeda.

**TIDAK TAHU — K0 untuk resource Stage 1 Naruto vs Mizuki.** Belum ada bukti yang menghubungkan identitas/flow Stage 1 Story Mode ke mode/state global yang dipakai FUN_80012EAC; direct caller FUN_80012780 juga tak diketahui. HA/HB/HC tetap hipotesis.

TSV writer selector dan window 12 instruksi: `reports/stage1_economy/DM3_SELECTOR_WRITERS_2026-11-05.tsv`.

## Batas dan file commit

Statis saja. Tidak ada emulator/game, BIOS, savestate, ISO, dump, video, frame, atau run Actions. Tidak mengubah `STATUS.md`, Release, atau visibilitas repo.

Berkas yang ditambahkan:
- `reports/stage1_economy/DM0_DM1_DM2_DM3_STATIC_AUDIT_2026-11-05.md`
- `reports/stage1_economy/DM0_COMMIT_LEDGER_2026-11-05.tsv`
- `reports/stage1_economy/DM1_TILE_LEVEL_WRITER_CENSUS_2026-11-05.tsv`
- `reports/stage1_economy/DM2_LV3_LV5_NEW_HYPOTHESES_2026-11-05.tsv`
- `reports/stage1_economy/DM3_SELECTOR_WRITERS_2026-11-05.tsv`
