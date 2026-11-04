# CI0–CI3 — audit statis matriks selector dan bank level (4 November 2026)

Game: Naruto — Shinobi no Sato no Jintori Gassen (SLPS-03553)
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Snapshot input: 447631d02db0649abb07f7064ddf250bba81d779 (main sebelum publikasi audit ini)
Metode: Git compare, census mode/state, inventory DATA.BIN, tabel record yang telah diekstrak, serta uji aritmetika statis. Tanpa emulator/game.

## Ringkasan

| Butir | Status | K | Hasil |
|---|---|---:|---|
| CI0 — ledger commit sejak SHA dasar | TUNTAS | K4 | Main identik dengan SHA dasar; 0 commit baru dan 0 file-change. |
| CI1 — selector dan inventaris resource | TUNTAS | K4 | 2.816 baris matriks (256 mode × 11 state), 12 selector/resource ID unik. |
| CI1 — format 661 B | TUNTAS | K4 | Hanya 0x276 dan 0x27E: 1+22×0x1E; TSV gabungan 44 record. Sepuluh resource lain dilabeli bukan format ini. |
| CI2 — enam observasi × lima level | SEBAGIAN | K4 | X=120,180,200,220 cocok; X=240,280 tidak cocok pada dua resource format teridentifikasi. |
| CI2 — konsistensi vector bagi X berulang | TUNTAS | K4 | 44 record, 10 X unik, 0 konflik. |
| CI3 — HA tabel tersimpan | SEBAGIAN | K3–K4 | Konsisten dengan loader yang menyalin lima halfword; belum menggeneralisasi seluruh format resource. |
| CI3 — HB LV1=X/2 dan LV2=ceil10(1,1X) | SEBAGIAN | K4 | LV1 gagal 7/44; LV2 cocok 44/44. HB gabungan gugur sebagai aturan universal. |
| Selector papan Stage 1 Naruto vs Mizuki | BELUM | K0 | TIDAK TAHU; matriks belum menghubungkan nama stage ke pasangan mode/state. |

## CI0 — commit ledger

Compare 447631d02db0649abb07f7064ddf250bba81d779...main menghasilkan status identical, ahead_by=0, behind_by=0, total_commits=0, files=[]. Jadi daftar SHA, penulis, dan file per commit kosong. TSV ledger memuat header dan nol baris data; jumlah dihitung dari compare objek Git, bukan jumlah file pada commit laporan audit.

Status: TUNTAS — K4.

## CI1 — matriks selector ke resource

Matriks numerik berisi 2.816 baris: mode 0–255, masing-masing state 0–10 (11 baris per mode). Selector yang muncul: 0, 1, 2, 3, 4, 5, 6, 8, 9, 15, 16, 17. Rumus ID yang berlaku pada matriks ini: resource_id = 0x276 + selector.

| Selector | Resource ID (hex/desimal) | Baris mode/state | Offset DATA.BIN | Ukuran | SHA-256 | Bentuk |
|---:|---:|---:|---:|---:|---|---|
| 0 | 0x276 (630) | 2723 | 0x11DE000 | 661 | 12c1a6ff1870f5c6fe33723beef14d93009b509d70caa882c5c6e8de8535e0c8 | 1+22x0x1E (661 B) |
| 1 | 0x277 (631) | 11 | 0x1232800 | 991 | e4c1470a598703c9459571c4802904f80bfd5e96ca069418cae3a7b0d673a555 | bukan format ini |
| 2 | 0x278 (632) | 13 | 0x1287000 | 991 | 1d7eca0253024b88f57eb3e28acab6494452a3bda8a118e6fcdb1551921345b6 | bukan format ini |
| 3 | 0x279 (633) | 10 | 0x12D7800 | 1021 | a457bda090d93bf9ff1a7b2b892766c1776b977d8043939bb381edfc9935127c | bukan format ini |
| 4 | 0x27a (634) | 17 | 0x132C000 | 991 | 513392e5c938374ca8bc2cf90f683417260714bbe3edc7fa6f68da2aa3c0b9b7 | bukan format ini |
| 5 | 0x27b (635) | 2 | 0x137F800 | 1291 | 2036d837199026dffcd99b37e41e493fd1c254553973211578f405103a774313 | bukan format ini |
| 6 | 0x27c (636) | 4 | 0x13D4000 | 1141 | 20e055504bd6ee5c982ff2bd4ce20304d045b02534f0076e6b915011aafaec54 | bukan format ini |
| 8 | 0x27e (638) | 1 | 0x1474000 | 661 | d88af9fd0100da3ac3223aa5b1d85f884547b3e3f708ba1dec81cfb923f7775f | 1+22x0x1E (661 B) |
| 9 | 0x27f (639) | 4 | 0x14C8800 | 1141 | 2f99b52515900865f19a16e0eed91b604230e2306afa51e4ad6b8b059b0e0dbb | bukan format ini |
| 15 | 0x285 (645) | 7 | 0x16C2800 | 1291 | c2843af4917d167de695bf488032651f43c56a9f42a2d9182022f15323620011 | bukan format ini |
| 16 | 0x286 (646) | 14 | 0x1715800 | 1081 | 52b1d447ed06b45e8a73eb607d664e5df41b85f07fb6b6a61d797b2588580c60 | bukan format ini |
| 17 | 0x287 (647) | 10 | 0x1768800 | 1201 | f077385eb94eddb71164239533498528b7195bc493e42caccf2e713336e1d9a9 | bukan format ini |

Dua resource yang berukuran tepat 661 byte memiliki header count 0x16 (=22) dan 22 record stride 0x1E:
- 0x276 / 630: offset 0x11DE000; 661 B; SHA-256 12c1a6ff1870f5c6fe33723beef14d93009b509d70caa882c5c6e8de8535e0c8.
- 0x27E / 638: offset 0x1474000; 661 B; SHA-256 d88af9fd0100da3ac3223aa5b1d85f884547b3e3f708ba1dec81cfb923f7775f.

Resource 0x277, 0x278, 0x279, 0x27A, 0x27B, 0x27C, 0x27F, 0x285, 0x286, 0x287 berukuran selain 661 B dan diberi label 'bukan format ini'. Tidak disimpulkan stride, record count, atau semantik field untuk sepuluh resource itu.

TSV inventaris: CI1_SELECTOR_RESOURCE_INVENTORY_2026-11-04.tsv.
TSV 44 record (kolom CH1 + resource_id): CI1_LEVEL_BANK_RECORDS_ALL_2026-11-04.tsv.

### Excerpt kode mentah (52 byte)

Pada PC 0x800B7764–0x800B7794, reader membaca halfword selector pada tile+0x20, shift 7, mask 0x1E, lalu lhu field terpilih relatif dari +0x10. Berikut 13 instruksi MIPS-I / 52 byte mentah:

```
84 EA 43 8C C0 10 04 00 21 10 44 00 C0 10 02 00
21 10 44 00 80 10 02 00 21 10 43 00 20 00 43 94
00 00 00 00 C2 19 03 00 1E 00 63 30 21 10 43 00
10 00 42 94
```

Pola ini membuktikan indexed read terhadap field pada jalur reader tersebut. Laporan CH0–CH2 terdahulu mendokumentasikan loader FUN_800F7ADC menyalin lima halfword sumber ke runtime +0x10..+0x18 pada blok yang diperiksa. Itu tidak mengidentifikasi resource untuk Story Mode Stage 1.

Status inventaris: TUNTAS — K4.

## CI2 — pencocokan per sel pengamatan

Seluruh angka X/LV dalam tugas diperlakukan sebagai HIPOTESIS/PENGAMATAN PENGGUNA, bukan fakta gameplay. Syarat cocok: record harus memiliki X yang sama dan field LV terkait harus sama persis.

| X pengamatan | Record yang cocok persis (resource#record, indeks 0-based) | Lima daftar sel identik? |
|---:|---|---|
| 120 | 0x276#4, 0x276#6, 0x276#10, 0x276#20, 0x27E#1 | Ya |
| 180 | 0x27E#8, 0x27E#9, 0x27E#19 | Ya |
| 200 | 0x276#12, 0x276#16, 0x27E#7 | Ya |
| 220 | 0x276#13, 0x276#15 | Ya |
| 240 | — | Ya |
| 280 | — | Ya |

Rincian hasil:
- X=120: 0x276 record 4, 6, 10, 20; 0x27E record 1.
- X=180: 0x27E record 8, 9, 19.
- X=200: 0x276 record 12, 16; 0x27E record 7.
- X=220: 0x276 record 13, 15.
- X=240: tidak ada record cocok untuk LV1–LV5.
- X=280: tidak ada record cocok untuk LV1–LV5.

Untuk tiap X yang cocok, kelima sel nilai memiliki daftar record yang sama. Untuk X=240 dan 280 tidak ada kecocokan pada setiap level. Sepuluh resource lain digunakan oleh matriks, tetapi field X/LV tidak dibaca atau ditebak karena formatnya berbeda.

Uji duplikat X atas semua 44 record: 10 X unik, konflik vector lima level = 0.
TSV pencocokan per sel: CI2_OBSERVATION_CELL_MATCHES_2026-11-04.tsv.

Status kecocokan observasi: SEBAGIAN — K4 (hanya untuk dua resource yang layout-nya telah dikenali).
Status konflik X berulang: TUNTAS — K4 (44 record dua resource format 661 B).

## CI3 — hipotesis bersaing dan falsifier

### HA — lima nilai LV merupakan field tabel tersimpan

Bukti pendukung: dua resource format 661 B menyimpan lima halfword pada +0x10,+0x12,+0x14,+0x16,+0x18; loader yang dianalisis menyalin halfword itu ke record runtime; reader memilih salah satu berdasarkan selector level. Tidak ada X berulang dengan vector LV berbeda pada 44 record.

Falsifier HA:
1. X sama tetapi vector lima level berbeda — tidak ditemukan pada 44 record.
2. Loader yang diperiksa menghitung bank LV dari X alih-alih menyalin field — tidak tampak pada blok loader FUN_800F7ADC yang didokumentasikan.
3. Format resource lain memasok bank LV dengan cara berbeda — belum diuji; sepuluh resource non-format tidak diasumsikan layout-nya.

Kesimpulan: HA lebih cocok dengan data/jalur yang sudah dibuktikan, tetapi kata 'hanya' untuk seluruh game belum terbukti global. SEBAGIAN — K3–K4.

### HB — LV1=X/2 dan LV2=ceil10(1,1×X)

Uji:
- LV1_expected = X/2, nilai harus integer tepat.
- LV2_expected = 10 × ceil(1,1 × X / 10) = 10 × ceil(11X/100).

Pada semua 44 record format 661 B:
- LV1: 7 pengecualian:
- 0x276 record 1: X=60, LV1=35, X/2=30.
- 0x276 record 7: X=160, LV1=85, X/2=80.
- 0x27E record 4: X=160, LV1=85, X/2=80.
- 0x27E record 6: X=160, LV1=85, X/2=80.
- 0x27E record 10: X=160, LV1=85, X/2=80.
- 0x27E record 20: X=160, LV1=85, X/2=80.
- 0x27E record 21: X=160, LV1=85, X/2=80.
- LV2: 0 pengecualian dari 44 record.

Karena LV1 memiliki tujuh pengecualian, HB sebagai pasangan aturan universal gugur pada data yang diuji. Subaturan LV2 sendiri cocok 44/44, tetapi ini tidak membuktikan LV2 dihitung saat runtime: nilainya juga tersimpan di tabel. LV3–LV5 tidak diuji dengan formula tambahan.

TSV semua hasil per record: CI3_HB_FORMULA_TEST_2026-11-04.tsv.
Status uji HB: TUNTAS — K4 untuk 44 record format 661 B; BELUM untuk sepuluh resource non-format.

### Selector Stage 1 Naruto vs Mizuki

Matriks menghubungkan mode/state dengan selector/resource, tetapi bukti yang diperiksa tidak menghubungkan label 'Stage 1 Naruto vs Mizuki' ke mode/state tertentu. Mode 65/state 4 memetakan ke 0x27E; itu bukan bukti bahwa mode/state tersebut adalah Stage 1. Selector papan Stage 1: TIDAK TAHU — BELUM K0.

## Actions, batas, dan integritas

Tidak ada Actions run baru untuk audit ini. Koneksi GitHub yang tersedia menyediakan pembacaan dan commit, tetapi tidak menyediakan pemanggilan workflow_dispatch. Workflow CH2 yang ada hanya berjalan pada perubahan tools/step7/ExportTileLevelBankScale.py dan menghasilkan subtype expansion dari input record lama; mengubah script tersebut semata-mata untuk memicu run yang tidak menambah census tidak dilakukan.

Pemeriksaan Actions API: queued=0, in_progress=0, waiting=0, requested=0. Run CH2 terdahulu 41808407107 (SUCCESS; job export-and-check-level-bank; source SHA 81d4a336dc4c9e8152d6c88f4d7608d4429d88a6; exit code 0) adalah run lama, bukan hasil tugas ini.

Tidak menjalankan emulator atau game. Tidak mengubah STATUS.md, Release, atau visibilitas repo. Tidak mengomit ISO, BIOS, savestate, dump RAM, video, atau frame.
