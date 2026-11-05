# DL0–DL3 — audit lanjutan statis hasil DK0–DK3

Tanggal audit: 2026-11-05  
Game: Naruto — Shinobi no Sato no Jintori Gassen (SLPS-03553)  
Basis data: commit DK output `1d1d60ff1b9fc18713a21a679fb3d5d2c06ed32d`  
Run yang diaudit: `41817953399`, attempt 2  
Batas: statis saja; tidak menjalankan game/emulator, BIOS, savestate, atau mengambil ISO/dump/video/frame untuk audit lanjutan ini.

## Ringkasan status

| Target | Status | K | Putusan |
|---|---|---:|---|
| DL0 — ledger inklusif 8141a8... sampai 1d1d60... | TUNTAS | K4 | 9 commit: 5 MANUSIA, 4 BOT. Git compare melaporkan 8 commit sesudah baseline; dengan baseline inklusif menjadi 9, cocok dengan jumlah ledger. |
| DL1 — resource 0x286 dan 0x287 | TUNTAS | K4 | 76 record; struktur loader-offset SAMA. X, LV1–LV5, dan runtime +0x1A/+0x1C/+0x1E nol. Byte raw sumber +0x1A/+0x1C tetap bervariasi. Hex excerpt kontigu 23 byte per record tersedia di bawah. |
| DL2 — hipotesis LV3–LV5 | SEBAGIAN | K3 | Dua model numerik falsifiable diuji pada 13 X unik; model doubling delta lulus 3/13, model skala field ekstra lulus 0/13. Konsistensi vector untuk X berulang lulus 13/13. Rumus pembangkit asli TIDAK TAHU. |
| DL2 — LV1 pada X=60 dan X=160 | SEBAGIAN | K3 | Nilai tersimpan +5 dari X/2 pada dua kelompok itu; minimal dua penyebab bersaing tetap terbuka. |
| DL3 — resource khusus Stage 1 Naruto vs Mizuki | BELUM | K0 | TIDAK TAHU. Matriks selector/resource tidak dipetakan ke label Stage 1 atau pasangan mode/state Stage 1. |

K statis maksimum K4. Tidak ada klaim K5.

## DL0 — ledger semua commit, baseline inklusif

Rentang: `8141a8bd851b00e183797007563168d9ea6fdcdf` (inklusif) sampai `1d1d60ff1b9fc18713a21a679fb3d5d2c06ed32d` (inklusif).

Git compare baseline → HEAD menghasilkan `ahead_by=8`, `behind_by=0`, `total_commits=8`. Ledger mencakup 8 commit sesudah baseline ditambah baseline itu sendiri: **9 commit**. Ini setara dengan hitungan rentang inklusif `git rev-list --count 8141a8bd851b00e183797007563168d9ea6fdcdf^..1d1d60ff1b9fc18713a21a679fb3d5d2c06ed32d` = 9.

Total: **9 commit = 5 MANUSIA + 4 BOT**. Daftar file-change dihitung per commit, total 47 entri (bukan jumlah path unik).

| Full SHA | Author | Pesan |
|---|---|---|
| `8141a8bd851b00e183797007563168d9ea6fdcdf` | MANUSIA — zuppasoupfifaistimewa-png | Complete CI0 ledger through first audit publication |
| `f9645cdcc79da3a370ae36334000f94bbd5841d5` | MANUSIA — zuppasoupfifaistimewa-png | Add one-job static DK0-DK3 DATA.BIN audit |
| `fc4d649eb94994f8f5bf0e128fe67b09b711618a` | BOT — github-actions[bot] | Publish DK0-DK3 static DATA.BIN audit run 41815588375 |
| `217ce9df11f8ad1223a5196fa6c00a4c8fd0fd8a` | MANUSIA — zuppasoupfifaistimewa-png | Correct DK0-DK3 source field offsets from tile loader |
| `9da947fd5c46c30bc9f732d6dcbf0abad8c0213a` | BOT — github-actions[bot] | Publish DK0-DK3 static DATA.BIN audit run 41816597358 |
| `c71d656735e1704ac3edac52422f9db2dca8508c` | MANUSIA — zuppasoupfifaistimewa-png | Correct runtime tile offsets for DK0-DK3 resource audit |
| `0a6b61816446c47aaebabc5959b85d75099e1f27` | BOT — github-actions[bot] | Publish DK0-DK3 static DATA.BIN audit run 41817415683 |
| `c7684b30cb720b40282679f0616408b8703a32b6` | MANUSIA — zuppasoupfifaistimewa-png | Fix DATA.BIN loader stride base and runtime extra fields |
| `1d1d60ff1b9fc18713a21a679fb3d5d2c06ed32d` | BOT — github-actions[bot] | Publish DK0-DK3 static DATA.BIN audit run 41817953399 |

### Daftar file per commit

**8141a8bd851b00e183797007563168d9ea6fdcdf — 2 file**
- `reports/stage1_economy/CI0_CI1_CI2_CI3_STATIC_AUDIT_2026-11-04.md`
- `reports/stage1_economy/CI0_COMMIT_LEDGER_2026-11-04.tsv`

**f9645cdcc79da3a370ae36334000f94bbd5841d5 — 2 file**
- `.github/workflows/dk0-dk3-databin-static.yml`
- `tools/step7/ExportDK0DK1DK2DK3Static.py`

**fc4d649eb94994f8f5bf0e128fe67b09b711618a — 10 file**
- `reports/stage1_economy/dk0-dk3-static-run-41815588375/attempt-2/ACTIONS_RUN_SUMMARY.txt`
- `reports/stage1_economy/dk0-dk3-static-run-41815588375/attempt-2/DK0_COMMIT_LEDGER_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41815588375/attempt-2/DK0_DK1_DK2_DK3_AUDIT_2026-11-04.md`
- `reports/stage1_economy/dk0-dk3-static-run-41815588375/attempt-2/DK1_ALL_12_RESOURCE_RECORDS_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41815588375/attempt-2/DK1_RESOURCE_LAYOUT_CLASSIFICATION_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41815588375/attempt-2/DK2_OBSERVATION_ALL_12_RESOURCE_MATCHES_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41815588375/attempt-2/DK2_X_CROSS_RESOURCE_CONSISTENCY_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41815588375/attempt-2/DK3_ALL_RECORD_FORMULA_TEST_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41815588375/attempt-2/DK3_FORMULA_CANDIDATE_SUMMARY_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41815588375/attempt-2/DK_STATIC_PARSE_SUMMARY.txt`

**217ce9df11f8ad1223a5196fa6c00a4c8fd0fd8a — 1 file**
- `tools/step7/ExportDK0DK1DK2DK3Static.py`

**9da947fd5c46c30bc9f732d6dcbf0abad8c0213a — 10 file**
- `reports/stage1_economy/dk0-dk3-static-run-41816597358/attempt-1/ACTIONS_RUN_SUMMARY.txt`
- `reports/stage1_economy/dk0-dk3-static-run-41816597358/attempt-1/DK0_COMMIT_LEDGER_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41816597358/attempt-1/DK0_DK1_DK2_DK3_AUDIT_2026-11-04.md`
- `reports/stage1_economy/dk0-dk3-static-run-41816597358/attempt-1/DK1_ALL_12_RESOURCE_RECORDS_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41816597358/attempt-1/DK1_RESOURCE_LAYOUT_CLASSIFICATION_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41816597358/attempt-1/DK2_OBSERVATION_ALL_12_RESOURCE_MATCHES_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41816597358/attempt-1/DK2_X_CROSS_RESOURCE_CONSISTENCY_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41816597358/attempt-1/DK3_ALL_RECORD_FORMULA_TEST_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41816597358/attempt-1/DK3_FORMULA_CANDIDATE_SUMMARY_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41816597358/attempt-1/DK_STATIC_PARSE_SUMMARY.txt`

**c71d656735e1704ac3edac52422f9db2dca8508c — 1 file**
- `tools/step7/ExportDK0DK1DK2DK3Static.py`

**0a6b61816446c47aaebabc5959b85d75099e1f27 — 10 file**
- `reports/stage1_economy/dk0-dk3-static-run-41817415683/attempt-1/ACTIONS_RUN_SUMMARY.txt`
- `reports/stage1_economy/dk0-dk3-static-run-41817415683/attempt-1/DK0_COMMIT_LEDGER_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817415683/attempt-1/DK0_DK1_DK2_DK3_AUDIT_2026-11-04.md`
- `reports/stage1_economy/dk0-dk3-static-run-41817415683/attempt-1/DK1_ALL_12_RESOURCE_RECORDS_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817415683/attempt-1/DK1_RESOURCE_LAYOUT_CLASSIFICATION_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817415683/attempt-1/DK2_OBSERVATION_ALL_12_RESOURCE_MATCHES_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817415683/attempt-1/DK2_X_CROSS_RESOURCE_CONSISTENCY_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817415683/attempt-1/DK3_ALL_RECORD_FORMULA_TEST_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817415683/attempt-1/DK3_FORMULA_CANDIDATE_SUMMARY_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817415683/attempt-1/DK_STATIC_PARSE_SUMMARY.txt`

**c7684b30cb720b40282679f0616408b8703a32b6 — 1 file**
- `tools/step7/ExportDK0DK1DK2DK3Static.py`

**1d1d60ff1b9fc18713a21a679fb3d5d2c06ed32d — 10 file**
- `reports/stage1_economy/dk0-dk3-static-run-41817953399/attempt-2/ACTIONS_RUN_SUMMARY.txt`
- `reports/stage1_economy/dk0-dk3-static-run-41817953399/attempt-2/DK0_COMMIT_LEDGER_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817953399/attempt-2/DK0_DK1_DK2_DK3_AUDIT_2026-11-04.md`
- `reports/stage1_economy/dk0-dk3-static-run-41817953399/attempt-2/DK1_ALL_12_RESOURCE_RECORDS_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817953399/attempt-2/DK1_RESOURCE_LAYOUT_CLASSIFICATION_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817953399/attempt-2/DK2_OBSERVATION_ALL_12_RESOURCE_MATCHES_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817953399/attempt-2/DK2_X_CROSS_RESOURCE_CONSISTENCY_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817953399/attempt-2/DK3_ALL_RECORD_FORMULA_TEST_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817953399/attempt-2/DK3_FORMULA_CANDIDATE_SUMMARY_2026-11-04.tsv`
- `reports/stage1_economy/dk0-dk3-static-run-41817953399/attempt-2/DK_STATIC_PARSE_SUMMARY.txt`

## DL1 — resource 0x286 / 0x287

### Ringkasan record dan klasifikasi byte

| Resource | Entry | Header byte 0 | Record | Ukuran | Uji ukuran + byte count | X/LV nonzero | Class |
|---|---:|---:|---:|---:|---|---:|---|
| 0x286 | 646 | 0x24 = 36 | 36 | 1081 B | 1 + 36×0x1E = 1081; header=36 | 0/36 | **SAMA** |
| 0x287 | 647 | 0x28 = 40 | 40 | 1201 B | 1 + 40×0x1E = 1201; header=40 | 0/40 | **SAMA** |

Alasan klasifikasi bukan ukuran saja:
1. Byte pertama masing-masing resource adalah hitungan record (0x24 dan 0x28), sama dengan jumlah record yang dapat diparse.
2. Loader statis `FUN_800F7ADC` memakai cursor stride `0x1E` dan memetakan halfword pada sumber cursor `+0x08,+0x0A,+0x0C,+0x0E,+0x10,+0x12` ke X dan LV1–LV5, serta sumber `+0x14,+0x16,+0x18` ke runtime tile `+0x1A,+0x1C,+0x1E`.
3. Pada 36/36 dan 40/40 baris, keenam nilai X/LV tersebut nol; tiga field ekstra hasil copy juga nol; urutan field tetap lolos plausibility check. Tidak ada field bergeser yang dibutuhkan untuk memperoleh nilai yang masuk akal.
4. Sumber mentah setelah field yang disalin tetap bukan padding nol: raw source `+0x1A` dan `+0x1C` berisi halfword yang berubah; source boundary `+0x1E` adalah `0xFF` untuk semua record.

Putusan **SAMA** berarti skema/offset record yang dibaca loader selaras dengan resource bank yang sama, bukan bahwa semua isi kedua resource identik. Karena beberapa byte prefix `+0x00..+0x07` tidak disimpan pada TSV parser, tidak ada klaim bahwa seluruh record byte-for-byte identik dengan record resource lain.

### Hex excerpt mentah

Excerpt berikut adalah 23 byte kontigu dari **cursor sumber `+0x08` sampai dan termasuk `+0x1E`**, bukan seluruh record 0x1E-byte. Nilai ditulis dalam urutan byte little-endian. Delapan byte prefix `+0x00..+0x07` tidak termasuk excerpt.

**Resource 0x286**
- Record #0: `00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 DF 00 97 02 FF`  
  Decode tail: raw `+0x1A=0x00DF=223`; raw `+0x1C=0x0297=663`; boundary `+0x1E=FF`.
- Record #1: `00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 DF 00 76 02 FF`  
  Tail: raw `+0x1A=223`; raw `+0x1C=630`; boundary `FF`.
- Record #2: `00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 DF 00 57 02 FF`  
  Tail: raw `+0x1A=223`; raw `+0x1C=599`; boundary `FF`.
- Record #18 (tengah dari 36): `00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 A0 00 97 02 FF`  
  Tail: raw `+0x1A=160`; raw `+0x1C=663`; boundary `FF`.

**Resource 0x287**
- Record #0: `00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 DF 00 B7 02 FF`  
  Tail: raw `+0x1A=223`; raw `+0x1C=695`; boundary `FF`.
- Record #1: `00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 DF 00 97 02 FF`  
  Tail: raw `+0x1A=223`; raw `+0x1C=663`; boundary `FF`.
- Record #2: `00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 DF 00 76 02 FF`  
  Tail: raw `+0x1A=223`; raw `+0x1C=630`; boundary `FF`.
- Record #20 (tengah dari 40): `00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 A0 00 B7 02 FF`  
  Tail: raw `+0x1A=160`; raw `+0x1C=695`; boundary `FF`.

**Pembedaan nama kolom penting:** TSV memisahkan `plus_0x1A` (runtime tile field yang di-copy dari source cursor +0x14) dari `source_raw_plus_0x1A` (halfword raw pada cursor +0x1A). Yang berubah antara 223 dan 160 adalah kolom kedua. Nilai 663/630/599/... berada pada `source_raw_plus_0x1C`, bukan pada source `+0x1A`. Jadi jangan menamai urutan 223/663/630/599 sebagai satu kolom +0x1A. Field runtime `+0x1A/+0x1C/+0x1E` hasil copy tetap 0 pada dua resource tersebut.

Pola raw:
- 0x286: `source_raw_plus_0x1A` = 223 untuk record 0–17, lalu 160 untuk 18–35. `source_raw_plus_0x1C` membentuk urutan turun 663, 630, 599, 567, 535, 503, 471, 439, 407, 375, 343, 311, 279, 247, 215, 183, 151, 119; urutan ini berulang pada setengah kedua.
- 0x287: raw `+0x1A` = 223 untuk record 0–19, lalu 160 untuk 20–39. Raw `+0x1C` turun dari 695, 663, 630, 599, 567, 535, 503, 471, 439, 407, 375, 343, 311, 279, 247, 215, 183, 151, 119, 81; pola berulang pada setengah kedua.

## DL2 — uji 13 vector X nonnol

Vektor berasal dari seluruh 12 resource setelah loader mapping, bukan dari kolom literal sumber yang keliru. X yang diuji: 60, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320. Semua 13 kelompok memiliki sekurangnya dua record; vector LV1–LV5 dan tiga field ekstra konsisten pada duplikasi X.

Definisi:
- `d21=LV2−LV1`, `d32=LV3−LV2`, `d43=LV4−LV3`, `d54=LV5−LV4`.
- `A=runtime tile +0x1A`, `C=runtime tile +0x1C`, `E=runtime tile +0x1E`.
- Hipotesis HΔ: `d43=2×d32` dan `d54=2×d43` secara tepat.
- Hipotesis Haux: `d32=round_half_up(1.5×E)`, `d43=round_half_up(3×E)`, `d54=round_half_up(6×E)` secara tepat. Ini model skala field ekstra, bukan formula 2.2X/4.4X/8.8X.
- Pemeriksaan kolom ekstra: `C=round_half_up(0.7×A)` dan `E=round_half_up(0.7×X)`.
- Htable: tabel stored/copy; prediksi uji yang tersedia ialah vector LV sama untuk setiap X berulang di lintas resource. Ini menguji konsistensi tabel, bukan membuktikan bahwa pembuat tabel tidak memakai formula offline.

Tidak ada koefisien yang dipasangkan/di-fit dari satu atau dua titik; angka 1.5/3/6 dan relasi 2× adalah model kandidat eksplisit yang diuji tepat terhadap seluruh 13 X.

| X | LV1/LV2/LV3/LV4/LV5 | d21/d32/d43/d54 | A/C/E | Prediksi d32/d43/d54 Haux | HΔ | Haux | Htable, vector X berulang |
|---:|---|---|---|---|---|---|---|
| 60 | 35/70/135/265/530 | 35/65/130/265 | 50/35/42 | 63/126/252 | GAGAL | GAGAL | LULUS (23 record) |
| 100 | 50/110/220/440/880 | 60/110/220/440 | 50/35/70 | 105/210/420 | LULUS | GAGAL | LULUS (34 record) |
| 120 | 60/140/265/530/1050 | 80/125/265/520 | 100/70/84 | 126/252/504 | GAGAL | GAGAL | LULUS (22 record) |
| 140 | 70/160/310/620/1250 | 90/150/310/630 | 100/70/98 | 147/294/588 | GAGAL | GAGAL | LULUS (26 record) |
| 160 | 85/180/360/710/1410 | 95/180/350/700 | 120/84/112 | 168/336/672 | GAGAL | GAGAL | LULUS (25 record) |
| 180 | 90/200/390/800/1600 | 110/190/410/800 | 120/84/126 | 189/378/756 | GAGAL | GAGAL | LULUS (28 record) |
| 200 | 100/220/440/880/1760 | 120/220/440/880 | 150/105/140 | 210/420/840 | LULUS | GAGAL | LULUS (21 record) |
| 220 | 110/250/490/980/1940 | 140/240/490/960 | 150/105/154 | 231/462/924 | GAGAL | GAGAL | LULUS (17 record) |
| 240 | 120/270/530/1050/2120 | 150/260/520/1070 | 200/140/168 | 252/504/1008 | GAGAL | GAGAL | LULUS (9 record) |
| 260 | 130/290/580/1150/2290 | 160/290/570/1140 | 200/140/182 | 273/546/1092 | GAGAL | GAGAL | LULUS (20 record) |
| 280 | 140/310/620/1240/2470 | 170/310/620/1230 | 220/154/196 | 294/588/1176 | GAGAL | GAGAL | LULUS (17 record) |
| 300 | 150/330/660/1320/2640 | 180/330/660/1320 | 220/154/210 | 315/630/1260 | LULUS | GAGAL | LULUS (4 record) |
| 320 | 160/360/710/1410/2820 | 200/350/700/1410 | 250/175/224 | 336/672/1344 | GAGAL | GAGAL | LULUS (2 record) |

Hasil:
- HΔ lulus hanya X=100, 200, 300 (3/13); gugur sebagai aturan universal karena 10 X memfalsifikasinya.
- Haux gagal pada semua 13 X. Sementara itu relasi field ekstra `C≈0.7A` dan `E≈0.7X` lulus 13/13, sehingga field ekstra berhubungan secara numerik dengan X/A tetapi tidak menjelaskan delta LV menurut Haux.
- Htable konsisten pada 13/13 X: tidak ditemukan vector LV yang berbeda untuk X berulang di seluruh 415 record. Loader statis menyalin halfword stored ke runtime. Ini bukti tabel tersimpan/copy, tetapi tidak membedakan apakah nilai tabel dahulu dibuat manual atau dihasilkan offline.
- Kesimpulan LV3–LV5: **rumus asli TIDAK TAHU**. Jangan mengklaim faktor 2.2/4.4/8.8 sebagai formula kode; kandidat langsung dengan pembulatan floor/ceil/nearest yang tercatat dalam DK juga hanya cocok 59 dari 248 record nonblank untuk tiap level.

### Hipotesis LV3–LV5 dan falsifier

1. **HΔ — selisih level geometris.** Prediksi tepat `d43=2d32` dan `d54=2d43`. Falsifier: satu vector X dengan salah satu kesamaan tidak terpenuhi. Data memfalsifikasi 10 dari 13 X; HΔ bukan aturan universal.
2. **Haux — skala level dari field ekstra.** Prediksi tepat `d32=round(1.5E)`, `d43=round(3E)`, `d54=round(6E)`. Falsifier: satu X yang menyimpang pada salah satu delta. Semua 13 X menyimpang; Haux gugur pada data yang diuji.
3. **Htable — stored value table yang dicopy.** Prediksi: record X sama mempunyai vector LV sama dan loader menyalin halfword tersebut. Falsifier: vector berbeda pada X sama, atau jalur kode menghitung/menimpa LV dari X sebelum digunakan. Tidak ada konflik vector pada 415 record; loader copy didukung statis. Apakah tabel itu disusun manual atau dibuat dengan formula offline tetap TIDAK TAHU.

### LV1: pengecualian X/2+5 pada X=60 dan X=160

| X | LV1 tersimpan | X/2 | Selisih | Jumlah record |
|---:|---:|---:|---:|---:|
| 60 | 35 | 30 | +5 | 23 |
| 160 | 85 | 80 | +5 | 25 |

Dua hipotesis bersaing:
1. **H1 — override per record/tabel.** Nilai LV1=35 dan 85 disimpan langsung pada masing-masing record dan dicopy loader. Falsifier: temukan jalur kode yang menghitung ulang LV1 dari X dan menimpa halfword tersimpan sebelum dibaca.
2. **H2 — bonus +5 berbasis class/flag.** Record dari kelas/flag tertentu menambahkan +5 di atas X/2; X=60 dan 160 kebetulan berada pada kelas tersebut. Falsifier: record dengan class/flag yang sama tidak konsisten menerima +5, atau audit seluruh caller membuktikan tidak ada pembacaan class/flag yang mengendalikan bonus.

Status kedua hipotesis: **HIPOTESIS**, belum dipilih. Kemunculan hanya pada dua nilai X tidak cukup untuk meng-fit piecewise formula atau menyimpulkan rentang X.

## DL3 — pemilihan resource Stage 1 Naruto vs Mizuki

**TIDAK TAHU — K0 — BELUM.**

Bukti yang tersedia hanya:
- selector resource generik memiliki pemetaan `resource_id = 0x276 + selector` pada inventory yang diaudit;
- resource 0x276/0x27E cocok dengan skema 661 B; resource 0x286/0x287 cocok dengan stride/field-map yang sama tetapi seluruh X/LV kosong;
- matriks mode/state mencatat hitungan pemakaian selector, tetapi belum mengikat label Story Mode “Stage 1 Naruto vs Mizuki” ke mode/state tertentu;
- hasil runtime BA3 yang menunjukkan selector 0 dan resource 630 berasal dari dua H6 restore diagnostik tanpa input gameplay, bukan bukti pemilihan untuk Story Mode Stage 1.

Karena tidak ada jembatan byte/code dari label Stage 1 → mode/state → selector, tidak sah menyatakan resource 0x276, 0x27E, 0x286, 0x287, atau yang lain sebagai resource Stage 1. K0 dipertahankan sesuai aturan.

## GitHub Actions run 41817953399

Run status: `completed / success`; attempt 2.  
Job tunggal: `parse-all-target-resources`, status `completed / success`.  
Source SHA: `c7684b30cb720b40282679f0616408b8703a32b6`.  
Exit code: `0`.  
Ringkasan run tercatat sebagai file teks di folder attempt-2; tidak ada emulator/game, BIOS atau savestate yang dipakai, dan tidak ada binary committed.

File run summary:  
`reports/stage1_economy/dk0-dk3-static-run-41817953399/attempt-2/ACTIONS_RUN_SUMMARY.txt`

## Batas dan integritas

- Audit lanjutan ini menggunakan teks hasil DK, disassembly/field mapping yang sudah dipublikasikan, dan aritmetika pada TSV.
- Tidak menjalankan emulator atau game; tidak memakai BIOS/savestate.
- Tidak mengambil ISO/disc image/dump/video/frame untuk audit lanjutan.
- Tidak mengubah Release, `STATUS.md`, atau visibilitas repo.
- Tidak memasukkan binary ke commit.
