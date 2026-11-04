
# CH0–CH2 — Audit statis tabel nilai petak dan pembaca level

Tanggal: 4 November 2026  
Game: Naruto — Shinobi no Sato no Jintori Gassen (SLPS-03553)  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research  
Baseline CH0: b841ece9a121c48cc30a14be87813af0ff2b6fa7  
Cutoff ledger CH0 (inklusif): 8daa7013a39395b5ec7a4f82564c4c3fce87c5b8  
Metode: Git history, resource extraction yang telah ada di repo, raw-byte MIPS-I scan, dan Ghidra statis. Tidak menjalankan emulator/game.

## Ringkasan status

| Butir | Status | K | Kesimpulan |
|---|---|---:|---|
| CH0 — ledger commit | TUNTAS | K4 | 44 commit sejak baseline; 33 MANUSIA, 11 BOT; 585 entri file-change; 565 path unik. |
| CH1 — dump seluruh record resource 630 | TUNTAS | K4 | 22 record lengkap, seluruh field yang diminta, offset sumber, offset resource, dan SHA-256 tersedia. |
| CH1 — cocok dengan enam observasi | SEBAGIAN | K4 | Resource 630 cocok pada X=120,200,220; X=180 hanya cocok pada resource 638; X=240,280 tidak ditemukan pada keduanya. |
| CH1 — duplikat X pada resource 630 | TUNTAS | K4 | Semua kelompok X berulang memiliki satu tabel LV yang sama; tidak ada duplicate-X conflict. |
| CH2 — pembaca +0x10..+0x18 | TUNTAS | K4 | Lima load dinamis di FUN_800B770C dan satu reader lain di FUN_800D05B8 ditemukan dari Ghidra serta raw-byte scan. |
| CH2 — angka tabel ditampilkan pada petak | TUNTAS | K4 | FUN_800FC700 mengirim hasil FUN_800B770C ke renderer angka pada koordinat petak. Label gameplay angka tersebut belum diketahui. |
| CH2 — dipakai sebagai debit upgrade/toll | BELUM | K1 | Tidak ditemukan bukti transfer/debit yang mengikat nilai ini pada upgrade atau toll. TIDAK TAHU. |
| HT — nilai LV disimpan di resource | SEBAGIAN | K3–K4 | Loader menyalin lima halfword resource ke record runtime; hubungan observasi dengan resource Stage 1 belum lengkap. |
| HF — nilai LV dihitung langsung dari X | BELUM | K1–K2 | X dibaca dan dibandingkan di beberapa fungsi, tetapi tidak ditemukan formula yang menghasilkan bank LV dari X. |

## CH0 — ledger

Git history baseline → cutoff:
- ahead=44, behind=0; 44 commit.
- 33 commit MANUSIA dan 11 BOT.
- 585 entri perubahan file bila seluruh daftar file per commit dijumlahkan.
- 565 path unik pada keseluruhan ledger.
- TSV memiliki 44 baris data, satu baris untuk setiap commit.

Ledger lengkap (SHA, jenis author, author, semua file yang berubah):
reports/stage1_economy/CH0_COMMIT_LEDGER_2026-11-04.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/a5f50cc11128378eebfc1902c65bb7788d5cae4b/reports/stage1_economy/CH0_COMMIT_LEDGER_2026-11-04.tsv

Cutoff dipilih di commit 8daa7013a39395b5ec7a4f82564c4c3fce87c5b8. Commit setelah cutoff yang hanya memperbarui ledger dan menerbitkan laporan tidak dihitung ke dalam rentang CH0, agar tidak terjadi self-reference.

## CH1 — resource 630 dan nilai observasi

### Dump seluruh record

TSV utama: reports/stage1_economy/CH1_RESOURCE_630_ALL_TILE_RECORDS.tsv

Kolom: indeks record; u16 +0x0E, +0x10, +0x12, +0x14, +0x16, +0x18, +0x1A, +0x1C, +0x1E; offset record di file sumber; offset awal resource di DATA.BIN; SHA-256 resource penuh.

https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/CH1_RESOURCE_630_ALL_TILE_RECORDS.tsv

Identitas resource:
- Resource 630 / ID 0x276: 661 byte; 22 record; stride 0x1E; file offset 0x11DE000; SHA-256 12c1a6ff1870f5c6fe33723beef14d93009b509d70caa882c5c6e8de8535e0c8.
- Resource 638 / ID 0x27E (pembanding): 661 byte; 22 record; stride 0x1E; file offset 0x1474000; SHA-256 d88af9fd0100da3ac3223aa5b1d85f884547b3e3f708ba1dec81cfb923f7775f.

### Perbandingan enam pengamatan pengguna

Pengamatan tetap HIPOTESIS pengguna. Lima nilai level dibandingkan sebagai lima sel terpisah:

| X / +0x0E | Resource 630 | Resource 638 (pembanding) | Lima nilai LV yang cocok |
|---:|---|---|---|
| 120 | Indeks 4,6,10,20 — cocok | Indeks 1 — cocok | 60, 140, 265, 530, 1050 |
| 180 | Tidak ditemukan | Indeks 8,9,19 — cocok | 90, 200, 390, 800, 1600 |
| 200 | Indeks 12,16 — cocok | Indeks 7 — cocok | 100, 220, 440, 880, 1760 |
| 220 | Indeks 13,15 — cocok | Tidak ditemukan | 110, 250, 490, 980, 1940 |
| 240 | Tidak ditemukan | Tidak ditemukan | Tidak ada record pembanding |
| 280 | Tidak ditemukan | Tidak ditemukan | Tidak ada record pembanding |

Jadi untuk resource 630 saja, kecocokan persis ditemukan pada X=120, 200, dan 220. Dengan resource 638 sebagai pembanding, X=180 juga ditemukan. X=240 dan X=280 tidak ada di kedua resource kandidat. Ini belum membuktikan resource mana yang dipakai board Stage 1.

TSV pembandingan resource 630:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/CH1_OBSERVATION_MATCH_RESOURCE630_2026-11-04.tsv

### Pengulangan X

Pemeriksaan duplicate-X resource 630:
- X=0: indeks 0,5,11,17,18 → 0,0,0,0,0.
- X=100: indeks 2,3,21 → 50,110,220,440,880.
- X=120: indeks 4,6,10,20 → 60,140,265,530,1050.
- X=140: indeks 8,9,19 → 70,160,310,620,1250.
- X=200: indeks 12,16 → 100,220,440,880,1760.
- X=220: indeks 13,15 → 110,250,490,980,1940.

Tidak ada dua record dengan X sama tetapi tabel LV berbeda pada resource 630. TSV:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/CH1_DUPLICATE_X_TABLE_CHECK_RESOURCE630_2026-11-04.tsv

Pemilihan resource:
Tabel mode/state dalam hasil penelitian memiliki 2.844 baris; 2.723 memetakan resource 630, satu baris memetakan resource 638 (mode 65/state 4). Mode/state untuk board Stage 1 belum diidentifikasi. Hubungan resource 630 atau 638 dengan Stage 1: TIDAK TAHU.

## HT dan HF — hipotesis dengan falsifier

### HT — lima nilai level berasal dari tabel resource

Prediksi: lima halfword sudah disimpan dalam resource dan disalin saat record petak dimuat.

Bukti:
- Loader FUN_800F7ADC memindahkan nilai pada +0x10,+0x12,+0x14,+0x16,+0x18 dari record sumber ke field runtime yang sama.
- Stride record sumber 0x1E; stride record runtime 0x124.
- Pada jalur loader yang diperiksa, operasi itu berupa penyalinan halfword; tidak tampak kalkulasi lima nilai tersebut dari X saat pemuatan.
- Nilai observasi cocok untuk tiga X di resource 630 dan satu tambahan X di resource 638; dua X belum ditemukan.

Falsifier yang diminta:
1. Nilai di resource tidak sama dengan observasi — tidak terjadi untuk empat X yang ditemukan; X=240 dan 280 tidak memiliki record pembanding.
2. RAM menghitung nilai dari X saat load — tidak terlihat pada loader FUN_800F7ADC; jalur yang diperiksa menyalin nilai tersimpan.

Putusan HT: SEBAGIAN K3–K4. Keberadaan dan pemindahan tabel terbukti; resource Stage 1 yang tepat dan asal seluruh enam observasi belum terbukti.

### HF — lima nilai level dihitung dari X

Bukti yang meringankan HF:
- Ada fungsi yang membaca X +0x0E langsung dari record petak.
- Namun reader level utama FUN_800B770C memakai selector pada +0x20 untuk memilih nilai bank yang sudah tersimpan dari +0x10 dan seterusnya.
- FUN_800F0C10 membaca X; salah satu jalurnya melakukan perbandingan slt antara X dan nilai lain. Ini bukti penggunaan X sebagai input kondisi, bukan bukti pembuatan lima nilai LV.
- Tidak ditemukan pada jalur yang diperiksa operasi shift/kali yang mengambil X lalu menghasilkan kelima nilai LV.

Falsifier yang diminta:
1. Dua petak X sama tetapi tabel level berbeda — tidak ditemukan pada resource 630.
2. Tidak ada satu rumus integer X→LV yang cocok — pendekatan faktor sederhana tidak menjelaskan semua nilai, tetapi belum ada pembuktian matematis bahwa tidak ada formula integer lain.

Pendekatan [0,5; 1,1; 2,2; 4,4; 8,8] × X plus residual hanyalah heuristik K1–K2:
- X=120: residual [0,+8,+1,+2,-6]
- X=180: residual [0,+2,-6,+8,+16]
- X=200: residual [0,0,0,0,0]
- X=220: residual [0,+8,+6,+12,+4]

Residual = observasi dikurangi hasil perkalian faktor pendekatan. Pola ini bukan rumus game terverifikasi.

Putusan HF: BELUM K1–K2. X dibaca dan digunakan sebagai kondisi/display di beberapa jalur, tetapi tidak terbukti sebagai sumber perhitungan kelima nilai LV.

## CH2 — pembacaan bank level dan konteks pemakaian

### Loader dan reader utama

FUN_800F7ADC menyalin lima halfword dari resource ke record runtime. Reader utama adalah FUN_800B770C:
1. Mengambil record dari base DAT_8013EA84 dengan stride 0x124.
2. Membaca selector u16 pada +0x20.
3. Menghitung (selector >> 7) & 0x1E.
4. Menambah hasilnya ke base record dan membaca lhu pada effective offset +0x10 + ((u16[+0x20] >> 7) & 0x1E).

Lima PC load terkonfirmasi di FUN_800B770C, semua cocok dengan scan raw-byte:
- 0x800B7794: lhu v0,0x10(v0), bytes 10 00 42 94.
- 0x800B77D4: lhu v1,0x10(v0), bytes 10 00 43 94.
- 0x800B783C: lhu v0,0x10(v0), bytes 10 00 42 94.
- 0x800B7884: lhu v1,0x10(v0), bytes 10 00 43 94.
- 0x800B78D0: lhu v0,0x10(v0), bytes 10 00 42 94.

Reader tambahan: FUN_800D05B8, PC 0x800D0D70, lhu a0,0x10(v0), bytes 10 00 44 94.

### 12 instruksi sebelum load utama + raw bytes

PC load contoh: 0x800B7794. Di bawah ini 12 instruksi sebelumnya dan instruksi load tersebut (13 instruksi):

    0x800B7764 lw v1,-0x157c(v0) [84 EA 43 8C]
    0x800B7768 sll v0,a0,0x3     [C0 10 04 00]
    0x800B776C addu v0,v0,a0     [21 10 44 00]
    0x800B7770 sll v0,v0,0x3     [C0 10 02 00]
    0x800B7774 addu v0,v0,a0     [21 10 44 00]
    0x800B7778 sll v0,v0,0x2     [80 10 02 00]
    0x800B777C addu v0,v0,v1     [21 10 43 00]
    0x800B7780 lhu v1,0x20(v0)   [20 00 43 94]
    0x800B7784 nop               [00 00 00 00]
    0x800B7788 srl v1,v1,0x7     [C2 19 03 00]
    0x800B778C andi v1,v1,0x1e   [1E 00 63 30]
    0x800B7790 addu v0,v0,v1     [21 10 43 00]
    0x800B7794 lhu v0,0x10(v0)   [10 00 42 94]

Raw bytes little-endian untuk window yang sama (52 byte, <=64 byte):

    84 EA 43 8C C0 10 04 00 21 10 44 00 C0 10 02 00
    21 10 44 00 80 10 02 00 21 10 43 00 20 00 43 94
    00 00 00 00 C2 19 03 00 1E 00 63 30 21 10 43 00
    10 00 42 94

### Kalkulasi setelah membaca tabel

FUN_800B770C memilih cabang berdasarkan byte record +0x0B:
- subtype 0: nilai tabel tanpa skala;
- subtype 1: (nilai_tabel × 12) / 10;
- subtype 2: (nilai_tabel × 15) / 10;
- subtype 3: (nilai_tabel × 18) / 10;
- subtype 4: nilai_tabel << 1.

Jadi shift/perkalian yang ditemukan dalam reader diterapkan pada nilai yang sudah dibaca dari bank tabel, berdasarkan subtype +0x0B; itu bukan bukti kalkulasi level dari X +0x0E.

### Bukti jalur tampilan angka

Caller FUN_800FC700 menunjukkan:
- untuk record dengan byte subtype +0x00 = 4, nilai +0x0E dikirim langsung ke func_0x8001b364 sebagai angka di koordinat petak;
- untuk subtype +0x00 = 5, fungsi memanggil FUN_800B770C, lalu mengirim nilai negatif hasilnya ke helper yang sama pada koordinat petak;
- FUN_8001B364 meneruskan ke FUN_8001B39C; fungsi tersebut mengubah integer menjadi digit dan memanggil FUN_800448F8 untuk menggambar glyph angka.

Ini membuktikan ada numeric overlay pada petak yang memakai nilai tabel. Ini tidak cukup untuk menyebutnya “harga upgrade”, “debit upgrade”, atau “toll”; label gameplay angka itu tetap TIDAK TAHU. Tidak ditemukan bukti jalur debit upgrade/toll yang mengikat nilai tersebut ke transaksi.

### Pembacaan X +0x0E

Ghidra + raw-byte scan menemukan pembacaan X langsung dari record tile (base DAT_8013EA84, stride 0x124) pada:
- FUN_800F0C10: PC 0x800F0CD0, 0x800F0D34, 0x800F0EDC, 0x800F0EFC — lhu +0x0E.
- FUN_800BD114: PC 0x800BD610, 0x800BD614 — dua lbu +0x0E.
- FUN_800BDEAC: PC 0x800BE000, 0x800BE004 — dua lbu +0x0E.
- FUN_800C88F0: PC 0x800C9330/0x800C9334, 0x800C9990, 0x800C9CC0/0x800C9CC4, 0x800CA0D4/0x800CA0D8, 0x800CA7D0/0x800CA7D4.
- FUN_800D15A8: PC 0x800D2768, 0x800D3BBC — lhu +0x0E.
- FUN_800FC700: PC 0x800FC930 (lhu +0x0E) serta 0x800FC9F8/0x800FC9FC (lbu +0x0E).

Contoh perbandingan pada FUN_800F0C10: setelah lhu a0,0x0E(a2) di PC 0x800F0EDC, instruksi 0x800F0EEC adalah slt v0,v0,a0, yakni membandingkan X dengan nilai lain. Ini membuktikan pembacaan/penggunaan X sebagai kondisi; bukan perhitungan lima nilai level. Pada jalur reader bank, lima nilai tetap diambil dari tabel melalui selector +0x20.

### Agregasi

FUN_800BDC4C mengiterasi record tile terpilih, memanggil FUN_800B770C, lalu mengakumulasi hasil pembacaan. Kegunaan gameplay agregat itu belum diidentifikasi; tidak saya labeli sebagai pembayaran atau toll.

### Data keluaran CH2

Raw scanner menguji 8.299 kandidat instruksi MIPS-I ter-alignment pada displacement +0x0E/+0x10/+0x12/+0x14/+0x16/+0x18 untuk Entry 1 dan Main EXE. Kandidat mentah bukan semuanya akses tile; konfirmasi fungsi dan alias berasal dari Ghidra. File output:
- Raw summary: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41803736009/attempt-1/tile-level-raw-mips-summary.txt
- Raw candidate TSV: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41803736009/attempt-1/tile-level-raw-mips-candidates.tsv
- Ghidra Entry 1 accesses: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41803736009/attempt-1/tile-level-accesses-entry1.tsv
- Ghidra Main EXE accesses: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41803736009/attempt-1/tile-level-accesses-exe.tsv
- Caller code: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41803736009/attempt-1/tile-level-reader-callers-entry1.txt
- Callee renderer: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41803736009/attempt-1/tile-level-value-callee-main-exe.txt
- Loader detail: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41803736009/attempt-1/ba1-tile-resource-loader.txt

## GitHub Actions — status, job, source SHA, exit

Seluruh run berikut bersifat statis. Dua run berstatus CANCELLED sebelum job dibuat, sehingga exit code memang N/A. Tidak ada run yang masih berjalan saat audit ditutup.

| Run | Status | Job ID | Source SHA | Exit |
|---|---|---:|---|---:|
| 41800043936 | SUCCESS | 126473295597 | 4b459d00185374df7ebe9a6c42d631ea3ccdc604 | 0 |
| 41800173595 | FAILURE | 126474751606 | 178be910c55cdcc52393ef06e74ea5d9218f2ee9 | 127 |
| 41801147922 | FAILURE | 126476923702 | 5777c6aca85bbe1b5489e37f37c0de66f2ad5226 | 1 |
| 41801621667 | SUCCESS | 126478518577 | b8efccaa2605dfe09608bf4a96a3231a7765a4e9 | 0 |
| 41802560703 | SUCCESS | 126481618011 | ec3ba6dcf0c9bbbbbc5c2765614a4c05819dab14 | 0 |
| 41803298049 | SUCCESS | 126484076736 | e00a0dbd3c4e85e8f0643d8ed86c07428f0627c3 | 0 |
| 41803303026 | CANCELLED | — | 1d1cf3f544524aa4a7244d1d8eff6947db23d799 | N/A |
| 41803308974 | CANCELLED | — | 63bf90b0a24c46ccb7b59cb953fb4f2e34b747f3 | N/A |
| 41803736009 | SUCCESS | 126485597657 | 48c16d73d788d69657c05b494f1a06d86fd5485b | 0 |

Run 418001 gagal pada langkah shell/command (exit 127). Run 418011 gagal pada kompilasi exporter Java (exit 1); ringkasan bot lama salah menulis exit 0, dan sudah dikoreksi ke exit 1. Kedua run CANCELLED tidak mempunyai job, sehingga tidak ada process exit code.

Permalink raw ringkasan teks tiap run:
- 41800043936: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41800043936/attempt-1/ACTIONS_RUN_SUMMARY.txt
- 41800173595: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41800173595/attempt-1/ACTIONS_RUN_SUMMARY.txt
- 41801147922: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41801147922/attempt-1/ACTIONS_RUN_SUMMARY.txt
- 41801621667: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41801621667/attempt-1/ACTIONS_RUN_SUMMARY.txt
- 41802560703: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41802560703/attempt-1/ACTIONS_RUN_SUMMARY.txt
- 41803298049: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41803298049/attempt-1/ACTIONS_RUN_SUMMARY.txt
- 41803303026: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41803303026/attempt-1/ACTIONS_RUN_SUMMARY.txt
- 41803308974: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41803308974/attempt-1/ACTIONS_RUN_SUMMARY.txt
- 41803736009: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41803736009/attempt-1/ACTIONS_RUN_SUMMARY.txt

## Commit yang dibuat selama audit ini

- 4b459d00185374df7ebe9a6c42d631ea3ccdc604: tools/step7/ScanRawMipsOffsets.py; tools/step7/ExportOffsetMemoryAudit.java; reports/stage1_economy/CH1_RESOURCE_630_ALL_TILE_RECORDS.tsv.
- b8efccaa2605dfe09608bf4a96a3231a7765a4e9: tools/step7/ExportTileLevelTableAccesses.java.
- 8daa7013a39395b5ec7a4f82564c4c3fce87c5b8: reports/stage1_economy/aq1-run-41801147922/attempt-1/ACTIONS_RUN_SUMMARY.txt; reports/stage1_economy/aq1-run-41803303026/attempt-1/ACTIONS_RUN_SUMMARY.txt; reports/stage1_economy/aq1-run-41803308974/attempt-1/ACTIONS_RUN_SUMMARY.txt.
- 609b42b1c0247419bc3c67bc9799c7340ddcf26a: reports/stage1_economy/CH0_COMMIT_LEDGER_2026-11-04.tsv.
- 349dfe1665fe18b237afba3b90c7b582d7974ad1: reports/stage1_economy/CH0_COMMIT_LEDGER_2026-11-04.tsv.
- a5f50cc11128378eebfc1902c65bb7788d5cae4b: reports/stage1_economy/CH0_COMMIT_LEDGER_2026-11-04.tsv.

Laporan ini tidak mengubah Release, STATUS.md, atau visibilitas repo. Tidak ada ISO, BIOS, savestate, dump RAM, frame, atau video yang dikomit. Tidak ada emulator yang dijalankan.
