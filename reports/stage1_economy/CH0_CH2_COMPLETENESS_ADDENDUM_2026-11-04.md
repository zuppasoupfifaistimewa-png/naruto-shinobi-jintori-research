# CH0–CH2 — completeness addendum

Tanggal: 4 November 2026  
Game: Naruto — Shinobi no Sato no Jintori Gassen (SLPS-03553)  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research  
Snapshot histori yang diaudit: `b841ece9a121c48cc30a14be87813af0ff2b6fa7` → `a20b4b3027604347bd4febbc92ea3d6c82f006da` (47 commit, ahead 47, behind 0).  
Metode: audit statis Git, TSV resource, raw-byte MIPS-I scan dan hasil Ghidra yang sudah tersimpan di repo. Tidak menjalankan emulator.

## Putusan ringkas

| Butir | Status | K | Putusan |
|---|---|---:|---|
| CH0 — seluruh commit pada snapshot | TUNTAS | K4 | 47/47 commit: 44 baris ledger utama + 3 commit publikasi pada addendum. |
| CH1 — seluruh record resource 630 | TUNTAS | K4 | 22 record, semua kolom yang diminta dan SHA resource penuh tersedia. |
| CH1 — banding enam pengamatan | SEBAGIAN | K4 | X=120,200,220 cocok seluruh lima sel di resource 630; X=180 cocok di resource 638, bukan 630; X=240,280 tidak ditemukan pada kedua resource yang dibandingkan. |
| CH1 — duplicate X | TUNTAS | K4 | Tidak ditemukan dua record resource 630 dengan X sama tetapi tabel LV berbeda. |
| HT — LV disimpan sebagai tabel resource | SEBAGIAN | K3–K4 | Loader menyalin lima halfword; resource Stage 1 yang benar dan asal seluruh observasi belum teridentifikasi. |
| HF — LV dihitung langsung dari X | BELUM | K1–K2 | Tidak ditemukan kalkulasi lima nilai dari X pada jalur yang diperiksa; belum dibuktikan bahwa tidak ada formula lain di jalur lain. |
| CH2 — pembaca bank level | TUNTAS | K4 | Enam load terindeks +0x10..+0x18 pada dua fungsi, dengan 12 instruksi pendahulu dan raw window 52 byte per PC. |
| CH2 — tampil sebagai angka petak/UI | TUNTAS | K4 | FUN_800FC700 mengirim hasil reader ke jalur renderer digit; reader kedua melewatkan nilai ke helper UI. Label angka secara gameplay: TIDAK TAHU. |
| CH2 — debit upgrade/toll | BELUM | K1 | Tidak ada bukti langsung bahwa bank level tersebut dipakai sebagai jumlah debit atau toll. TIDAK TAHU. |

## CH0 — rekonsiliasi ledger

Git compare dari baseline ke snapshot `a20b4b3027604347bd4febbc92ea3d6c82f006da` menghasilkan 47 commit. Ledger utama yang sudah ada memuat 44 commit sampai cutoff `8daa7013a39395b5ec7a4f82564c4c3fce87c5b8`; tiga commit publikasi yang berada sesudah cutoff kini dicantumkan di file suplemen:

- `349dfe1665fe18b237afba3b90c7b582d7974ad1` — MANUSIA — `reports/stage1_economy/CH0_COMMIT_LEDGER_2026-11-04.tsv`
- `a5f50cc11128378eebfc1902c65bb7788d5cae4b` — MANUSIA — `reports/stage1_economy/CH0_COMMIT_LEDGER_2026-11-04.tsv`
- `a20b4b3027604347bd4febbc92ea3d6c82f006da` — MANUSIA — `reports/stage1_economy/CH0_CH1_CH2_TILE_ECONOMY_AUDIT_2026-11-04.md`

Dengan demikian 44 + 3 = 47 commit pada snapshot awal lengkap. File ini dan dua file suplemen audit dibuat sesudah snapshot tersebut; commit publikasi artefak audit baru itu tidak dimasukkan ke hitungan historis snapshot.

Ledger utama:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/a20b4b3027604347bd4febbc92ea3d6c82f006da/reports/stage1_economy/CH0_COMMIT_LEDGER_2026-11-04.tsv

Suplemen tiga commit:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2bbdbfafc145844a9c8ba086d725f56ac93c66b8/reports/stage1_economy/CH0_PUBLICATION_COMMITS_ADDENDUM_2026-11-04.tsv

## CH1 — resource dan perbandingan

Resource 630 / ID 0x276 berukuran 661 byte; berisi 22 record, stride 0x1E, offset DATA.BIN 0x11DE000, SHA-256:
`12c1a6ff1870f5c6fe33723beef14d93009b509d70caa882c5c6e8de8535e0c8`.

Dump TSV meliputi indeks, u16 +0x0E, +0x10, +0x12, +0x14, +0x16, +0x18, +0x1A, +0x1C, +0x1E, offset record sumber, offset resource, dan SHA-256 resource penuh.

Banding enam pengamatan pengguna (tetap HIPOTESIS, bukan fakta game):

| X | LV1–LV5 observasi | Resource 630 | Hasil sel |
|---:|---|---|---|
| 120 | 60,140,265,530,1050 | record 4,6,10,20 | 5/5 cocok |
| 180 | 90,200,390,800,1600 | tidak ada record X=180 | 0/5 di resource 630; 5/5 ada di resource 638 |
| 200 | 100,220,440,880,1760 | record 12,16 | 5/5 cocok |
| 220 | 110,250,490,980,1940 | record 13,15 | 5/5 cocok |
| 240 | 120,270,530,1050,2120 | tidak ada record X=240 | 0/5, tidak ada record pembanding pada resource 638 |
| 280 | 140,310,620,1240,2470 | tidak ada record X=280 | 0/5, tidak ada record pembanding pada resource 638 |

Sumber record lengkap:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/a20b4b3027604347bd4febbc92ea3d6c82f006da/reports/stage1_economy/CH1_RESOURCE_630_ALL_TILE_RECORDS.tsv

TSV cocok/tidak cocok per sel:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/a20b4b3027604347bd4febbc92ea3d6c82f006da/reports/stage1_economy/CH1_OBSERVATION_MATCH_RESOURCE630_2026-11-04.tsv

Duplicate-X:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/a20b4b3027604347bd4febbc92ea3d6c82f006da/reports/stage1_economy/CH1_DUPLICATE_X_TABLE_CHECK_RESOURCE630_2026-11-04.tsv

### Hipotesis dan falsifier

**HT — lima nilai LV tersimpan sebagai tabel resource.** Loader statis `FUN_800F7ADC` menyalin lima halfword pada offset +0x10..+0x18 dari record sumber ke field runtime yang sama; jalur loader yang ditinjau tidak menghitung nilai tersebut dari X. Ini mendukung HT pada K3–K4. Falsifier HT: resource yang benar untuk board ternyata tidak memuat angka yang diamati, atau jalur load menghitung ulang nilai dari X. Untuk X=180, resource 638 cocok persis tetapi resource 630 tidak memiliki recordnya; untuk X=240 dan 280 tidak ditemukan record pada resource 630 maupun 638. Mode/state Stage 1 yang memilih resource tepat: TIDAK TAHU.

**HF — bank LV dihitung langsung dari X.** Falsifier kuat yang diminta pengguna adalah dua record X sama tetapi tabel LV berbeda; hal tersebut tidak ditemukan pada resource 630. Jalur reader utama juga membaca nilai bank yang telah tersimpan. Namun ini belum membuktikan ketiadaan semua rumus X di seluruh game; HF tetap BELUM K1–K2, bukan falsified K4.

Perkiraan faktor `[0,5; 1,1; 2,2; 4,4; 8,8] × X` hanya heuristik. Residual per LV (observasi dikurangi hasil perkalian):

| X | Residual LV1..LV5 |
|---:|---|
| 120 | 0, +8, +1, +2, −6 |
| 180 | 0, +2, −6, +8, +16 |
| 200 | 0, 0, 0, 0, 0 |
| 220 | 0, +8, +6, +12, +4 |
| 240 | 0, +6, +2, −6, +8 |
| 280 | 0, +2, +4, +8, +6 |

Residual itu tidak membentuk rumus game terverifikasi. Paling jauh K1–K2.

## CH2 — pembaca tabel

Raw MIPS scan menelusuri 8.299 kandidat instruksi MIPS-I ter-alignment pada displacement +0x0E/+0x10/+0x12/+0x14/+0x16/+0x18 untuk Entry 1 dan Main EXE. Setelah alias object/function diperiksa statis, enam load level-bank terkonfirmasi:

- `FUN_800B770C`: PC `0x800B7794`, `0x800B77D4`, `0x800B783C`, `0x800B7884`, `0x800B78D0`.
- `FUN_800D05B8`: PC `0x800D0D70`.

Setiap PC membaca instruksi `lhu ...,0x10(base)`; 12 instruksi sebelumnya mengambil u16 selector dari tile+0x20, menggeser 7 bit, mem-mask `0x1E`, dan menambahkan offset hasilnya ke base tile. Effective field yang terbaca adalah:
`tile + 0x10 + ((u16(tile + 0x20) >> 7) & 0x1E)`,
yakni salah satu dari +0x10,+0x12,+0x14,+0x16,+0x18.

Enam baris window mencatat 12 instruksi sebelum load, instruksi load, dan 52 byte raw little-endian (13 instruksi total) untuk tiap PC:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/608df3e36083177df150ed72ac908cb977fddb98/reports/stage1_economy/CH2_LEVEL_BANK_READER_WINDOWS_2026-11-04.tsv

Pada `FUN_800B770C`, subtype byte +0x0B memilih transformasi atas nilai tabel yang telah dibaca: subtype 0 tanpa skala; subtype 1 ×12/10; subtype 2 ×15/10; subtype 3 ×18/10; subtype 4 ×2. Perkalian/shift ini diterapkan pada **nilai bank hasil load**, bukan sebagai rumus dari X +0x0E.

Jalur `FUN_800FC700` mengirim hasil `FUN_800B770C` ke `FUN_8001B364` dan jalur renderer digit; jadi keberadaan tampilan angka petak terdukung K4. Reader `FUN_800D05B8` juga mengirim nilai hasil load ke helper `FUN_80108DC8`; label tampilan tepatnya TIDAK TAHU. Apakah angka itu secara gameplay merupakan harga upgrade, debit upgrade, atau toll: BELUM K1 / TIDAK TAHU. Tidak ada bukti transfer/debit yang mengikat bank level ini sebagai nominal transaksi.

## GitHub Actions

Run statis utama untuk raw-byte scan dan Ghidra:
- Run: `41803736009`
- Status: `SUCCESS`
- Job: `126485597657`
- Source SHA: `48c16d73d788d69657c05b494f1a06d86fd5485b`
- Exit code: `0`

Ringkasan teks sudah berada di repo:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/8daa7013a39395b5ec7a4f82564c4c3fce87c5b8/reports/stage1_economy/aq1-run-41803736009/attempt-1/ACTIONS_RUN_SUMMARY.txt

Laporan CH0–CH2 utama juga mencatat seluruh run terkait, termasuk dua kegagalan tool/build dan dua pembatalan tanpa job/exit code:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/a20b4b3027604347bd4febbc92ea3d6c82f006da/reports/stage1_economy/CH0_CH1_CH2_TILE_ECONOMY_AUDIT_2026-11-04.md

## Batas dan hal yang belum diketahui

- Resource 630 memuat tabel LV lengkap, tetapi tidak semua pengamatan pengguna cocok dengan resource tersebut. Resource 638 menjelaskan X=180 saja; board/mode Stage 1 yang dipilih tetap TIDAK TAHU.
- Kode memilih nilai tersimpan berdasarkan selector level; transformasi subtype adalah pasca-load. Rumus pembangkit asli dari X tidak ditemukan.
- Kaitan angka tersebut dengan harga/debit upgrade atau toll tidak terbukti. Jangan menyebutnya harga upgrade sampai ada bukti transaksi tersendiri.
- Tidak ada emulator dijalankan dalam pekerjaan ini.
- Tidak ada perubahan Release, `STATUS.md`, atau visibilitas repo; tidak ada ISO, BIOS, savestate, dump RAM, screenshot/frame, atau video yang dikomit.
