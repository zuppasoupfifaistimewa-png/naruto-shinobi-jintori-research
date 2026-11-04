# CH0–CH2 — audit lengkap tabel nilai level petak (snapshot 4 November 2026)

Game: Naruto — Shinobi no Sato no Jintori Gassen (SLPS-03553)  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research  
Baseline ledger: `b841ece9a121c48cc30a14be87813af0ff2b6fa7`  
Cutoff bukti sebelum commit audit ini: `38af8e7796226ef9a3b73535608b2274ec7545ba`  
Metode: pembacaan Git history, TSV resource yang sudah ada, raw-byte MIPS-I scan, dan Ghidra statis. Tidak menjalankan game atau emulator.

## Ringkasan putusan

| Butir | Status | K | Putusan |
|---|---|---:|---|
| CH0 — semua commit baseline → cutoff | TUNTAS | K4 | 60 commit, 48 MANUSIA, 12 BOT; 602 entri perubahan file, 576 path unik. SHA dan path tiap commit ada di ledger TSV. |
| CH1 — semua record resource 630 | TUNTAS | K4 | 22 record; kolom X, lima nilai LV, +0x1A/+0x1C/+0x1E, offset, SHA resource tersedia. |
| CH1 — enam observasi per sel LV1–LV5 | SEBAGIAN | K4 | Resource 630 cocok untuk X=120, 200, 220; resource 638 cocok untuk X=180; X=240 dan 280 tidak ada di kedua kandidat. |
| CH1 — duplicate X di resource 630 | TUNTAS | K4 | Tidak ditemukan X yang berulang dengan tabel LV berbeda. |
| HT — lima nilai LV berasal dari tabel resource | SEBAGIAN | K3–K4 | Tabel tersimpan dan disalin ke RAM terbukti; resource yang dipakai board Stage 1 belum diketahui. |
| HF — lima nilai LV dihitung dari X | BELUM | K1–K2 | Tidak ditemukan generator X→bank LV pada jalur yang diperiksa; bukti belum cukup untuk menyatakan tidak ada formula lain di tempat lain. |
| CH2 — pembaca bank +0x10..+0x18 | TUNTAS | K4 | Enam PC pembaca teridentifikasi; raw-byte scan independen dari referensi langsung Ghidra. |
| CH2 — angka hasil reader ditampilkan | TUNTAS | K4 | Ada numeric overlay pada petak. Label gameplay angka tetap TIDAK TAHU. |
| CH2 — angka itu harga/debit upgrade/toll | BELUM | K1 | Tidak ada bukti transaksi yang mengikat reader ke debit upgrade atau toll. TIDAK TAHU. |
| CH2 — operasi shift/kali dari X untuk membangkitkan lima LV | SEBAGIAN | K3 | Tidak ditemukan pada loader/reader dan fungsi X yang diperiksa; shift/multiply reader diterapkan ke nilai bank setelah dibaca, bukan ke X. |

K statis maksimum K4. Pengamatan pengguna tentang "harga netral" tetap HIPOTESIS K1 sampai label dan transaksi gameplay dibuktikan.

---

## CH0 — ledger commit

Git compare dari baseline sampai cutoff `38af8e7...`:
- 60 commit baru; behind=0.
- 48 commit MANUSIA dan 12 commit BOT.
- 602 entri perubahan file jika daftar file per commit dijumlahkan.
- 576 path file unik.
- Satu commit di dalam rentang adalah empty commit `b0e1de1a0746c94025a13094a58d7ace1e591e14`; metadata Git menunjukkan tidak ada file berubah.
- Ledger memuat 60 SHA penuh, jenis author, nama author, serta semua path file yang berubah (kolom terakhir dipisah titik koma).

Ledger:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/b4af1946598a36b2683d6a53b5a787bd19c70242/reports/stage1_economy/CH0_COMMIT_LEDGER_2026-11-04.tsv

Perubahan untuk menyempurnakan audit setelah cutoff ledger:
- `4a6dd39ebcf6cf85b3d3477bd4b1f6c57187cf53` — `reports/stage1_economy/CH0_COMMIT_LEDGER_2026-11-04.tsv` (menambahkan 16 commit yang sebelumnya belum terdaftar).
- `b4af1946598a36b2683d6a53b5a787bd19c70242` — `reports/stage1_economy/CH2_LEVEL_BANK_READER_WINDOWS_2026-11-04.tsv` (memperbaiki label kolom agar tepat sesuai urutan isi).
Kedua commit audit ini berada sesudah cutoff 38af8e7 dan sengaja tidak dimasukkan ke ledger snapshot 60 commit, agar rentang yang dihitung tidak berubah sendiri saat ledger dipublikasikan. Commit publikasi laporan ini juga di luar cutoff.

---

## CH1 — data tabel resource 630

Resource 630:
- index/ID: 630 / `0x276`
- ukuran: 661 byte; 22 record; stride sumber `0x1E`
- offset DATA.BIN: `0x11DE000`
- SHA-256 resource penuh: `12c1a6ff1870f5c6fe33723beef14d93009b509d70caa882c5c6e8de8535e0c8`

TSV seluruh 22 record berisi:
`record_index`, u16 `+0x0E`, u16 `+0x10,+0x12,+0x14,+0x16,+0x18`, u16 `+0x1A,+0x1C,+0x1E`, source file offset, resource file offset, dan SHA-256 resource:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/b4af1946598a36b2683d6a53b5a787bd19c70242/reports/stage1_economy/CH1_RESOURCE_630_ALL_TILE_RECORDS.tsv

Resource pembanding 638:
- index/ID: 638 / `0x27E`
- ukuran: 661 byte; 22 record; stride sumber `0x1E`
- offset DATA.BIN: `0x1474000`
- SHA-256: `d88af9fd0100da3ac3223aa5b1d85f884547b3e3f708ba1dec81cfb923f7775f`

### Perbandingan setiap sel pengamatan

Setiap baris membandingkan lima sel LV secara terpisah. `YES` berarti nilai resource sama persis dengan pengamatan pada level tersebut.

| X | Record 630 | Record 638 | LV1 | LV2 | LV3 | LV4 | LV5 | Hasil |
|---:|---|---|---|---|---|---|---|---|
| 120 | 4, 6, 10, 20 | 1 | YES | YES | YES | YES | YES | Cocok di 630 dan 638 |
| 180 | — | 8, 9, 19 | — | — | — | — | — | Cocok kelima sel di 638; tidak ada di 630 |
| 200 | 12, 16 | 7 | YES | YES | YES | YES | YES | Cocok di 630 dan 638 |
| 220 | 13, 15 | — | YES | YES | YES | YES | YES | Cocok di 630 |
| 240 | — | — | NO | NO | NO | NO | NO | Tidak ditemukan di kedua kandidat |
| 280 | — | — | NO | NO | NO | NO | NO | Tidak ditemukan di kedua kandidat |

Nilai yang cocok:
- X=120: `[60, 140, 265, 530, 1050]`
- X=180: `[90, 200, 390, 800, 1600]`
- X=200: `[100, 220, 440, 880, 1760]`
- X=220: `[110, 250, 490, 980, 1940]`

TSV per sel untuk resource 630:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/b4af1946598a36b2683d6a53b5a787bd19c70242/reports/stage1_economy/CH1_OBSERVATION_MATCH_RESOURCE630_2026-11-04.tsv

Bukti record resource 638 dan semua tabel kandidat:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/b4af1946598a36b2683d6a53b5a787bd19c70242/reports/stage1_economy/aq1-run-41803736009/attempt-1/BA1_TILE_TABLE_RECORDS.tsv

Pemilihan resource untuk board Story Mode Stage 1 masih TIDAK TAHU. Census mode/state memiliki banyak pemetaan ke resource 630 dan satu baris ke 638 (mode 65/state 4), tetapi state Stage 1 yang benar belum ditentukan.

### Duplicate X

Hasil resource 630:
- X=0: indeks 0, 5, 11, 17, 18 → tabel `0,0,0,0,0`.
- X=100: indeks 2, 3, 21 → `50,110,220,440,880`.
- X=120: indeks 4, 6, 10, 20 → `60,140,265,530,1050`.
- X=140: indeks 8, 9, 19 → `70,160,310,620,1250`.
- X=200: indeks 12, 16 → `100,220,440,880,1760`.
- X=220: indeks 13, 15 → `110,250,490,980,1940`.

Tidak ada duplicate-X conflict. TSV:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/b4af1946598a36b2683d6a53b5a787bd19c70242/reports/stage1_economy/CH1_DUPLICATE_X_TABLE_CHECK_RESOURCE630_2026-11-04.tsv

### Hipotesis HT dan HF serta falsifier

**HT — tabel tersimpan di resource.**  
Bukti langsung K4: loader `FUN_800F7ADC` menyalin lima halfword sumber ke runtime `+0x10..+0x18`. Record sumber ber-stride `0x1E`, record runtime ber-stride `0x124`. Pada blok pemuatan yang diperiksa, lima field itu dibaca dari sumber dan ditulis ke offset runtime yang sama; tidak terlihat lima nilai LV dihitung dari X saat blok itu berjalan.

Falsifier HT:
1. Nilai resource tidak sama dengan observasi — belum terjadi untuk X=120, 180 (resource 638), 200, dan 220; X=240/280 belum punya record pembanding.
2. RAM dihitung dari X saat load — tidak terlihat pada blok loader `FUN_800F7ADC` yang diperiksa; yang terlihat adalah pemindahan halfword tersimpan.
Putusan: SEBAGIAN K3–K4 karena pemilihan resource Stage 1 belum diketahui.

**HF — bank LV dihitung langsung dari X.**  
X `+0x0E` memang dibaca dalam beberapa fungsi, tetapi reader bank utama `FUN_800B770C` memilih salah satu dari lima halfword yang telah tersimpan. `FUN_800F0C10` menggunakan X untuk perbandingan kondisi; itu bukan pembangkit lima nilai LV.

Falsifier HF:
1. Dua record X sama dengan tabel LV berbeda — tidak ditemukan dalam resource 630.
2. Tidak ada satu rumus integer X→LV yang dapat menghasilkan semua tabel — belum dibuktikan secara matematis untuk seluruh fungsi/game. Tidak ditemukannya rumus pada jalur terpilih bukan bukti global bahwa rumus tidak ada.
Putusan: BELUM K1–K2.

**Heuristik pola pengguna (bukan rumus kode terverifikasi).**  
Dengan faktor pendekatan `[0,5; 1,1; 2,2; 4,4; 8,8] × X`, residual `observasi − hasil perkalian` adalah:

| X | Residual LV1..LV5 |
|---:|---|
| 120 | `[0, +8, +1, +2, -6]` |
| 180 | `[0, +2, -6, +8, +16]` |
| 200 | `[0, 0, 0, 0, 0]` |
| 220 | `[0, +8, +6, +12, +4]` |
| 240 | `[0, +6, +2, -6, +8]` |
| 280 | `[0, +2, +4, +8, +6]` |

Ini hanya pendekatan K1–K2 berdasarkan pengamatan pengguna, tidak boleh diperlakukan sebagai formula game atau sebagai bukti bahwa nilai dihitung saat runtime.

---

## CH2 — pembaca bank level dan kegunaan hasil

### Pembaca terindeks level

Reader utama: `FUN_800B770C`. Basis record diperoleh dari pointer global `DAT_8013EA84`; stride runtime yang dihitung adalah `0x124`. Reader membaca:
`selector = (u16(tile+0x20) >> 7) & 0x1E`
lalu mengambil halfword pada:
`tile + 0x10 + selector`
yang memilih salah satu dari `+0x10,+0x12,+0x14,+0x16,+0x18`.

Lima lokasi load:
- PC `0x800B7794`, `FUN_800B770C`: `lhu v0,0x10(v0)`.
- PC `0x800B77D4`, `FUN_800B770C`: `lhu v1,0x10(v0)`.
- PC `0x800B783C`, `FUN_800B770C`: `lhu v0,0x10(v0)`.
- PC `0x800B7884`, `FUN_800B770C`: `lhu v1,0x10(v0)`.
- PC `0x800B78D0`, `FUN_800B770C`: `lhu v0,0x10(v0)`.
- Reader tambahan PC `0x800D0D70`, `FUN_800D05B8`: `lhu a0,0x10(v0)`; hasil diteruskan ke `FUN_80108DC8`, tetapi label pemakaiannya belum diketahui.

TSV reader windows yang sudah dikoreksi label kolomnya berisi, untuk setiap enam PC, 12 instruksi sebelum load, instruksi load, dan 52 byte mentah (13 instruksi termasuk load):
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/b4af1946598a36b2683d6a53b5a787bd19c70242/reports/stage1_economy/CH2_LEVEL_BANK_READER_WINDOWS_2026-11-04.tsv

Contoh lengkap PC `0x800B7794` — 12 instruksi sebelum load:
```
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
```
52 byte mentah:
```
84 EA 43 8C C0 10 04 00 21 10 44 00 C0 10 02 00
21 10 44 00 80 10 02 00 21 10 43 00 20 00 43 94
00 00 00 00 C2 19 03 00 1E 00 63 30 21 10 43 00
10 00 42 94
```

Raw-byte MIPS scan terpisah menemukan 8.299 kandidat instruksi aligned dengan displacement exact `+0x0E/+0x10/+0x12/+0x14/+0x16/+0x18` pada Entry 1 dan Main EXE. Ringkasan:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/b4af1946598a36b2683d6a53b5a787bd19c70242/reports/stage1_economy/aq1-run-41803736009/attempt-1/tile-level-raw-mips-summary.txt
Kandidat mentah:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/b4af1946598a36b2683d6a53b5a787bd19c70242/reports/stage1_economy/aq1-run-41803736009/attempt-1/tile-level-raw-mips-candidates.tsv

Batas interpretasi: scanner raw mengidentifikasi opcode/displacement, bukan membuktikan setiap kandidat adalah akses record tile. Alias base-register dan fungsi diverifikasi terpisah dengan Ghidra. Base import Entry 1 `0x800AD450` adalah kandidat mapping statis; pemetaan runtime Entry 1 tidak divalidasi di audit ini. Alamat tile indeks 4 `0x8013BCA8` dari log CE3 tidak dipakai untuk mengklaim base pointer yang sama; stride aritmetika `4 × 0x124 = 0x490` konsisten, tetapi alias runtime spesifik tetap belum dibuktikan.

### Skala subtype setelah pembacaan bank

Setelah nilai bank terpilih, `FUN_800B770C` memakai byte subtype `tile+0x0B`:
| subtype +0x0B | Operasi pada nilai tabel `v` | Faktor nominal |
|---:|---|---:|
| 0 | `v` | 1,0× |
| 1 | `(v × 12) // 10` | 1,2× |
| 2 | `(v × 15) // 10` | 1,5× |
| 3 | `(v × 18) // 10` | 1,8× |
| 4 | `v << 1` | 2,0× |
| selain 0–4 | `0` | — |

Pembagian subtype 1–3 adalah integer floor. Ini perkalian/shift pada **nilai yang sudah dibaca dari tabel**, bukan operasi yang mengambil X `+0x0E` lalu menghasilkan bank LV.

Ekspansi statis 44 record resource 630/638 × 5 subtype × 5 level = 1.100 baris:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/b4af1946598a36b2683d6a53b5a787bd19c70242/reports/stage1_economy/ch2-level-bank-scale-run-41808407107/attempt-1/CH2_LEVEL_BANK_OUTPUT_BY_SUBTYPE.tsv
Ringkasan faktor dan sumber input:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/b4af1946598a36b2683d6a53b5a787bd19c70242/reports/stage1_economy/ch2-level-bank-scale-run-41808407107/attempt-1/CH2_LEVEL_BANK_SCALE_SUMMARY.txt

### Tampilan, harga, debit dan toll

`FUN_800FC700` mengirim hasil `FUN_800B770C` ke jalur renderer angka `FUN_8001B364 → FUN_8001B39C → FUN_800448F8`. Dengan demikian yang terbukti adalah numeric overlay/angka pada petak. Bukti itu tidak memberi label gameplay angka sebagai harga.

Belum ditemukan jalur transaksi yang mengikat hasil reader ke:
- biaya upgrade barrier;
- pengurangan saldo/debit upgrade;
- toll atau pembayaran saat melintas.

Untuk ketiga makna transaksi itu statusnya **BELUM / TIDAK TAHU**. Jangan menyamakan teks angka pada tile dengan harga tanpa bukti debit/pending transaction yang memakai nilai tersebut.

### Agregasi nilai tile

`FUN_800BDC4C` menyaring tile bertipe 5 dan owner nibble yang sama, memanggil `FUN_800B770C` untuk tile tersebut, lalu menjumlahkan hasilnya. Return yang terbukti:
`floor(sum(reader_value(tile_i)) / 2) + FUN_80012A8C()`
Fungsi ini sendiri mengembalikan nilai agregat; tidak terlihat menulis atau mendebit saldo. Gameplay meaning agregat dan makna getter dasar `FUN_80012A8C()`: TIDAK TAHU. Ini tidak membuktikan harga upgrade atau toll.

### X +0x0E: perbandingan vs formula

X `+0x0E` dibaca pada sejumlah PC, termasuk:
- `FUN_800F0C10`: `0x800F0CD0`, `0x800F0D34`, `0x800F0EDC`, `0x800F0EFC` (lhu).
- `FUN_800D15A8`: `0x800D2768`, `0x800D3BBC` (lhu).
- Ada akses byte/halfword kandidat lain di fungsi perbandingan dan renderer yang dicantumkan pada audit CH0–CH2 sebelumnya.

Salah satu contoh `FUN_800F0C10`: X dibaca pada `0x800F0EDC`, kemudian dipakai dalam instruksi `slt` untuk membandingkan terhadap nilai lain. Ini penggunaan X sebagai kondisi. Tidak ada formula shift/multiply yang terbukti mengubah X menjadi lima nilai LV pada blok loader/reader yang diperiksa. Rumus subtype di atas berada sesudah lhu bank dan memakai nilai bank tersebut.

---

## GitHub Actions

Run static expansion yang berhasil:
- Run ID: `41808407107`
- Workflow: `ch2-level-bank-scale-static`
- Job: `export-and-check-level-bank`
- Job ID: `126501133341`
- Status/conclusion: SUCCESS
- Source SHA: `81d4a336dc4c9e8152d6c88f4d7608d4429d88a6`
- Script exit code: `0`
- `GAME_OR_EMULATOR_EXECUTED=no`
- Hasil: `records=44 subtype_cases=5 levels=5 rows=1100`

Ringkasan Actions (status, job, SHA, exit code):
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/b4af1946598a36b2683d6a53b5a787bd19c70242/reports/stage1_economy/ch2-level-bank-scale-run-41808407107/attempt-1/ACTIONS_RUN_SUMMARY.txt

Run percobaan sebelumnya:
- Run ID `41808275888`, FAILURE, job `export-and-check-level-bank`, job ID `126500693809`, source SHA `d87c3914e9b4edc473d7a27862ce9641b2fac20b`, script exit 1.
- Penyebab: kesalahan delimiter TSV pada parser; sudah diperbaiki dan run berikutnya PASS.

Tidak ada GitHub Actions run berstatus queued/in_progress/requested/waiting/pending saat pemeriksaan ditutup.

---

## Batas dan integritas audit

1. Tidak ada emulator atau ROM yang dijalankan untuk audit ini.
2. Tidak mengubah Release `naruto-checkpoint-39262213468`, `STATUS.md`, atau visibilitas repository.
3. Tidak ada ISO, BIOS, savestate, dump RAM, video, atau frame yang dikomit.
4. Tidak meneliti ulang rumus chakra release, H6 kredit, atau gate `+0xEA8`.
5. Kesimpulan utama saat ini: **tabel lima nilai LV per petak tersimpan di resource lalu dibaca secara indexed-level; subtype dapat mengubah hasil reader; numeric overlay terbukti; label harga/debit/toll belum terbukti.**
