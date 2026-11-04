# CH2 — ekspansi bank nilai level menurut subtype tile

Tanggal: 4 November 2026  
Game: Naruto — Shinobi no Sato no Jintori Gassen (SLPS-03553)  
Metode: ekspansi statis hasil dekompilasi MIPS + TSV resource yang sudah dikomit. Tidak menjalankan ROM atau emulator.

## Putusan

| Butir | Status | K | Hasil |
|---|---|---:|---|
| Rumus reader lima nilai LV | TUNTAS | K4 | `FUN_800B770C` memilih satu halfword +0x10..+0x18 melalui selector level, lalu mengubah nilai menurut subtype tile +0x0B. |
| Ekspansi dua resource | TUNTAS | K4 | 44 record dari resource 630 dan 638 × 5 subtype × 5 level = 1.100 baris keluaran. |
| Kaitan subtype +0x0B dengan ukuran rantai type-5 | SEBAGIAN | K3–K4 | Konsisten dengan BB1: +0x0B menyimpan jumlah successor link; ukuran rantai = link count + 1 untuk jalur type-5 yang diaudit. |
| Kaitan output reader dengan harga/debit upgrade/toll | BELUM | K1 | Tidak terbukti. TIDAK TAHU. |
| Resource terpilih untuk board Stage 1 | BELUM | K1 | Resource 630 dan 638 adalah dua kandidat table-shape; konfigurasi/mode-state Stage 1 belum terpetakan. TIDAK TAHU. |

## Rumus eksak yang ditemukan

Lima nilai tersimpan pada record runtime:
- LV1 = u16(tile + 0x10)
- LV2 = u16(tile + 0x12)
- LV3 = u16(tile + 0x14)
- LV4 = u16(tile + 0x16)
- LV5 = u16(tile + 0x18)

Reader `FUN_800B770C(tile_index)` membaca selector dari `u16(tile+0x20)`:
`selector = (u16(tile+0x20) >> 7) & 0x1E`

Maka alamat halfword efektif:
`tile + 0x10 + selector`

Sesudah halfword level terpilih, byte subtype `tile+0x0B` memilih transformasi integer berikut:

| subtype `+0x0B` | Transformasi reader | Faktor nominal | Link successor bila semantik BB1/type-5 berlaku | Ukuran rantai kandidat |
|---:|---|---:|---:|---:|
| 0 | `v` | 1,0× | 0 | 1 record |
| 1 | `(v × 12) // 10` | 1,2× | 1 | 2 record |
| 2 | `(v × 15) // 10` | 1,5× | 2 | 3 record |
| 3 | `(v × 18) // 10` | 1,8× | 3 | 4 record |
| 4 | `v << 1` | 2,0× | 4 | 5 record |

Pembagian dilakukan sesudah perkalian; hasil untuk subtype 1–3 adalah integer floor. Cabang subtype 4 adalah shift-left satu bit. Kasus subtype lain mengembalikan 0.

**Pemisahan penting:** nilai subtype 0–4 tidak tersimpan sebagai lima tabel LV yang berbeda di resource. Lima halfword disalin dari resource saat load; reader kemudian mengambil salah satu berdasarkan level dan menerapkan faktor subtype. Ini rumus pasca-load yang terbukti K4. Ia bukan rumus yang membangkitkan nilai LV dari X (+0x0E).

Hubungan dengan BB1 bersyarat: audit BB1 menyimpulkan bahwa untuk tile type 5, +0x0B menghitung successor link dalam rantai owner yang sama. Karena itu ukuran rantai dapat dibaca sebagai `+0x0B + 1` pada konteks type-5 tersebut. Jangan generalisasikan ke semua tile type sebelum writer/caller untuk setiap tipe diperiksa.

## Contoh numerik

Contoh resource 630, record indeks 4, X=120, bank tersimpan:
`[60, 140, 265, 530, 1050]`

| subtype +0x0B | LV1 | LV2 | LV3 | LV4 | LV5 |
|---:|---:|---:|---:|---:|---:|
| 0 | 60 | 140 | 265 | 530 | 1050 |
| 1 | 72 | 168 | 318 | 636 | 1260 |
| 2 | 90 | 210 | 397 | 795 | 1575 |
| 3 | 108 | 252 | 477 | 954 | 1890 |
| 4 | 120 | 280 | 530 | 1060 | 2100 |

Contoh resource 638, record indeks 8, X=180, bank tersimpan:
`[90, 200, 390, 800, 1600]`

| subtype +0x0B | LV1 | LV2 | LV3 | LV4 | LV5 |
|---:|---:|---:|---:|---:|---:|
| 0 | 90 | 200 | 390 | 800 | 1600 |
| 1 | 108 | 240 | 468 | 960 | 1920 |
| 2 | 135 | 300 | 585 | 1200 | 2400 |
| 3 | 162 | 360 | 702 | 1440 | 2880 |
| 4 | 180 | 400 | 780 | 1600 | 3200 |

Tabel contoh menunjukkan nilai reader untuk lima kemungkinan subtype, bukan bahwa satu tile yang sama benar-benar melewati kelima subtype. Nilai dasar X=120 dan X=180 di atas tetap berasal dari record resource; transformasi berasal dari byte subtype +0x0B.

## Hasil Actions dan berkas

Run pertama:
- Run ID: `41808275888`
- Status: FAILURE
- Job: `export-and-check-level-bank`, job ID `126500693809`
- Source SHA: `d87c3914e9b4edc473d7a27862ce9641b2fac20b`
- Script exit code: 1
- Penyebab: delimiter TSV pada parser dua karakter, bukan satu karakter tab. Ringkasan kegagalan disimpan.

Run perbaikan:
- Run ID: `41808407107`
- Status: SUCCESS
- Job: `export-and-check-level-bank`, job ID `126501133341`
- Source SHA: `81d4a336dc4c9e8152d6c88f4d7608d4429d88a6`
- Script exit code: 0
- Hasil: `CH2_LEVEL_BANK_EXPANSION=PASS records=44 subtype_cases=5 levels=5 rows=1100`

Output TSV 1.100 baris:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8308adf3ab3bbb1360dbe0ac4620adaa2f4b4ef0/reports/stage1_economy/ch2-level-bank-scale-run-41808407107/attempt-1/CH2_LEVEL_BANK_OUTPUT_BY_SUBTYPE.tsv

Ringkasan ekspansi:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8308adf3ab3bbb1360dbe0ac4620adaa2f4b4ef0/reports/stage1_economy/ch2-level-bank-scale-run-41808407107/attempt-1/CH2_LEVEL_BANK_SCALE_SUMMARY.txt

Ringkasan Actions sukses (mencantumkan job ID dan source SHA):
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/56eb46d739c1a34708377f68b0d1aeb6edbc6d10/reports/stage1_economy/ch2-level-bank-scale-run-41808407107/attempt-1/ACTIONS_RUN_SUMMARY.txt

Ringkasan Actions gagal:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/e03da947ebbe53d7338bd2c2ab61436194f6fc96/reports/stage1_economy/ch2-level-bank-scale-run-41808275888/attempt-1/ACTIONS_RUN_SUMMARY.txt

Raw window 12 instruksi pra-load untuk keenam reader:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/608df3e36083177df150ed72ac908cb977fddb98/reports/stage1_economy/CH2_LEVEL_BANK_READER_WINDOWS_2026-11-04.tsv

## Batas kesimpulan

1. Nilai +0x10..+0x18 adalah bank data tabel yang disalin dari resource. Reader dapat menghasilkan keluaran yang lebih tinggi menurut subtype +0x0B. Ini memperlihatkan hubungan nilai level dan struktur link tile, bukan hubungan perhitungan dari X.
2. Belum ada bukti yang menghubungkan hasil `FUN_800B770C` secara langsung ke debit transaksi upgrade, harga peningkatan barrier, atau toll. Fungsi juga dipakai dalam jalur angka/tampilan dan agregasi; makna gameplay seluruh caller belum dibuktikan.
3. Dua table-shape yang ditemukan dari scan ketat resource 630 dan 638. Peta konfigurasi mode/state mencatat resource 630 pada banyak baris dan resource 638 pada satu baris (mode 65/state 4); baris yang benar untuk board Story Mode Stage 1 belum diketahui. Karena itu jangan menetapkan resource 630 sebagai Stage 1 hanya dari jumlah pemakaiannya.
4. Rumus pengali sederhana yang dikalikan dengan X tidak digunakan reader untuk membentuk bank LV. Nilai bank dibaca dari resource lalu diskalakan berdasarkan subtype. Hipotesis HF tentang formula X→LV belum terbukti; hasil ini hanya menguatkan HT bahwa tabel tersimpan.
5. Tidak ada emulator/game yang dijalankan pada pekerjaan ini. Tidak ada perubahan Release, `STATUS.md`, atau visibilitas repo. Tidak ada ISO, BIOS, savestate, dump RAM, frame, atau video yang dikomit.

## Berkas yang ditambahkan/diubah selama perluasan ini

- `.github/workflows/ch2-level-bank-scale-static.yml`
- `tools/step7/ExportTileLevelBankScale.py`
- `reports/stage1_economy/ch2-level-bank-scale-run-41808275888/attempt-1/ACTIONS_RUN_SUMMARY.txt`
- `reports/stage1_economy/ch2-level-bank-scale-run-41808407107/attempt-1/ACTIONS_RUN_SUMMARY.txt`
- `reports/stage1_economy/ch2-level-bank-scale-run-41808407107/attempt-1/CH2_LEVEL_BANK_OUTPUT_BY_SUBTYPE.tsv`
- `reports/stage1_economy/ch2-level-bank-scale-run-41808407107/attempt-1/CH2_LEVEL_BANK_SCALE_SUMMARY.txt`
