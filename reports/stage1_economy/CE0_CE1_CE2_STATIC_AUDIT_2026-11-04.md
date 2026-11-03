# CE0–CE2 — koreksi ledger dan audit statis jalur ekonomi
Tanggal: 4 November 2026
Game: Naruto — Shinobi no Sato no Jintori Gassen (SLPS-03553)
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Baseline/source HEAD: `cd90b281f45cada726e80c3f87661e5ae5494303`
Sumber utama: laporan CD0–CD3, hasil scanner AQ1 41730277650, Ghidra Entry 1.

## Putusan

| Butir | Status | K | Ringkasan |
|---|---|---:|---|
| CE0 ledger CD | TUNTAS | K4 | Jumlah serta nama berkas dihitung dari objek commit Git; koreksi disimpan di laporan baru ini. |
| CE1(a) caller | TUNTAS | K4 | `FUN_800F3658` memakai switch/jump-table byte manager+`0x2E9`, case 9 menuju JAL `0x800D15A8`. Tidak ada compare literal `==9` tepat sebelum JAL. |
| CE1(b) debit | TUNTAS | K4 | Event 3/8 membaca `u16(tile+0x1A)`, cek saldo kerja, pending `-fee` pada manager+`0x2EE`. |
| CE1(c) setter | TUNTAS | K4 | `lw a1,0x4(v0)` di `0x800BEC94` memasok saldo kerja ke setter di `0x800BEC98`. |
| CE1(d) beda 3/8 | SEBAGIAN | K3 | Gate action 8 terbukti sebagai tile tipe 5 milik pemain dan level di bawah batas; transaksi keduanya identik. Kondisi sumber action 3 dan pesan tersendiri belum tertutup. |
| CE1(e) level base-0 | TUNTAS | K4 | Untuk display pada jalur UI yang diperiksa, bits 8–11 ditambah 1 sebelum helper display. |
| CE2 lompat level d≥2 | SEBAGIAN | K3 | Tidak ada pengali level pada blok transaksi 3/8; census di luar blok berisi kandidat pembaca/penulis nibble, tetapi belum ada UI target-level yang terbukti menerapkan biaya 4×/8×/16×. |
| CE2 action 3 netral vs upgrade | BELUM | K1/K2 | Action 8 = upgrade petak tipe 5 milik pemain; event 3 TIDAK TAHU apakah build netral atau aksi tile lain. |

Skala: temuan statis maksimum K4; K5 memerlukan hasil runtime terukur minimal dua peluncuran. Semua pengamatan pengguna mengenai d=2/3/4 tetap HIPOTESIS K1, bukan fakta runtime baru.

---

## CE0 — koreksi ledger CD

### Commit #5 yang benar

SHA penuh yang dikonfirmasi dari objek Git:
`eeba76256c6b2c729c9b65e4e30db0f36dd42b7f`

- Parent: `de1e4c9568e543b6dc5af6f7c54c25e5123cbd11`
- Jumlah berkas dari commit API GitHub: **57**
- Daftar di bawah adalah path penuh dalam commit, bukan daftar yang disimpulkan dari laporan lama.
- Laporan CD lama menulis SHA yang kurang/keliru karakter dan tidak ditimpa.

Berkas yang benar-benar diubah oleh commit #5:
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/ACTIONS_RUN_SUMMARY.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/BA1_DATA_BIN_RESOURCE_INVENTORY.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/BA1_DATA_SCAN_SUMMARY.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/BA1_RESOURCE_CANDIDATES.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/BA1_TILE_TABLE_CANDIDATES.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/BA1_TILE_TABLE_RECORDS.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/BA1_TILE_TABLE_SCAN_SUMMARY.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/BB2_FULL_DATABIN_TEXT_SCAN.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/aq1-deep-context.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/aq1-economy-census.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/aq1-recount.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/aw1-helper-call-windows.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/aw1-manager-b38-accesses.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/aw1-manager-b40-accesses.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/aw1-manager-b44-accesses.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/aw1-manager-function-detail.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/aw1-manager-status.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/aw1-tile-field-function-inventory.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/aw2-numeric-instruction-literals.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/aw2-numeric-occurrences.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/aw2-static-data-scan.md`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/ay1-ay2-entry1.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/ay1-ay2-exe.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/ay1-ay2-sha256.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/ay2-exe-random-byte-check.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/az3-main-exe-economic-helper-detail.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/az3-resource-economy-function-detail.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/az3-setter-call-windows-entry1.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/az3-setter-call-windows-main-exe.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/az3-setter-caller-main-exe-detail.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/az3-setter-direct-callers-entry1.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/az3-setter-direct-callers-main-exe.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/az3-starting-balance-global-detail.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/ba1-mode-state-resource-selector.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/ba1-resource-parser-main-exe.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/ba1-selector-callers-main-exe.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/ba1-selector-dat80070cd0-xrefs.csv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/ba1-selector-main-exe-functions.csv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/ba1-tile-loader-callers.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/ba1-tile-resource-loader.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/bb2-action-byte-access.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/bb2-d15a8-direct-callers.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/bb2-d15a8-focused.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/bb2-d15a8-function-detail.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/bb2-entry1-numeric-literals.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/bb2-event-direct-callers.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/bb2-event-function-detail.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/bb2-event-instruction-windows.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/bb2-full-databin-text-scan.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/bb2-message-object-functions.csv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/bb2-message-object-xrefs.csv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/bb2-tile-nibble-access.tsv`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/entry1-buffer-base-targets.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/entry1-helper-function-detail.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/helper-a1-provenance-status.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/input-identity.txt`
- `reports/stage1_economy/aq1-run-41729541613/attempt-1/run-summary.txt`

### Commit #12 — pemeriksaan daftar 38 berkas

SHA penuh: `7c0f0bf9236efc2ae39977d82218884d014313fb`

- Parent: `fffa1b6bfbb5ea23b27db89fbd12c138e881097b`
- Jumlah berkas dari objek Git: **38**
- `ay1-ay2-exe.tsv` **tidak ada** dalam daftar commit ini. File dengan nama tersebut ada pada commit #5 (run 41729541613), bukan pada commit #12 (run 41730277650).

Berkas yang benar-benar diubah oleh commit #12:
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/ACTIONS_RUN_SUMMARY.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/BA1_DATA_BIN_RESOURCE_INVENTORY.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/BA1_DATA_SCAN_SUMMARY.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/BA1_RESOURCE_CANDIDATES.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/BA1_TILE_TABLE_CANDIDATES.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/BA1_TILE_TABLE_RECORDS.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/BA1_TILE_TABLE_SCAN_SUMMARY.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/BB2_FULL_DATABIN_TEXT_SCAN.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/aq1-recount.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/aw1-helper-call-windows.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/aw1-manager-b38-accesses.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/aw1-manager-b40-accesses.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/aw1-manager-b44-accesses.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/aw1-manager-function-detail.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/aw2-numeric-instruction-literals.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/ay1-ay2-entry1.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/az3-resource-economy-function-detail.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/az3-setter-call-windows-entry1.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/az3-setter-direct-callers-entry1.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/ba1-tile-loader-callers.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/ba1-tile-resource-loader.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/bb2-action-byte-access.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/bb2-d15a8-direct-callers.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/bb2-d15a8-focused.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/bb2-d15a8-function-detail.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/bb2-entry1-numeric-literals.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/bb2-event-direct-callers.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/bb2-event-function-detail.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/bb2-event-instruction-windows.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/bb2-full-databin-text-scan.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/bb2-message-object-functions.csv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/bb2-message-object-xrefs.csv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/bb2-tile-nibble-access.tsv`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/cd1-raw-indirect-call-candidates.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/entry1-buffer-base-targets.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/entry1-helper-function-detail.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/input-identity.txt`
- `reports/stage1_economy/aq1-run-41730277650/attempt-1/run-summary.txt`

### Putusan koreksi

- Hash commit #5 dikoreksi menjadi `eeba76256c6b2c729c9b65e4e30db0f36dd42b7f`.
- Jumlah commit #5 = 57; jumlah commit #12 = 38.
- Klaim sebelumnya bahwa daftar commit #12 memuat `ay1-ay2-exe.tsv` ditarik kembali.
- Metode: daftar `files[]` milik tiap objek commit, dihitung dan ditampilkan apa adanya dari Git; tidak menghitung dari seluruh tree repo.

---

## CE1 — potongan statis (Entry 1, base kandidat 0x800AD450)

Semua byte berikut adalah byte little-endian yang diekspor dari Ghidra pada Entry 1 dengan model alamat yang dipakai laporan AQ1. Potongan per item tetap ≤64 byte. `0x800AD450` adalah base mapping kandidat static-import; pemetaan runtime bukan syarat klaim statis di bawah dan tetap dibatasi oleh warning laporan AQ1.

### (a) Prolog dan caller ke FUN_800D15A8

- Fungsi: `FUN_800F3658`, prolog PC `0x800F3658`.
  `800F3658 [D0 FF BD 27] addiu sp,sp,-0x30`
- Fungsi sama, pembacaan byte action manager+`0x2E9`:
  `800F3760 [E9 02 43 90] lbu v1,0x2e9(v0)`
- Dispatcher switch memakai pemeriksaan batas tabel, bukan branch equality 9:
  `800F3768 [40 00 62 2C] sltiu v0,v1,0x40`
  `800F376C [3B 0A 40 10] beq v0,zero,0x800f605c`
- Decompilation `FUN_800F3658`: `switch(manager+0x2E9) { case 9: FUN_800D15A8(); }`
- Site panggilan:
  `800F5DAC [6A 45 03 0C] jal 0x800d15a8`
  `800F5DB0 [00 00 00 00] nop`

**Koreksi interpretasi:** switch/case 9 membuktikan nilai dispatch 9. Instruksi mentah di sekitar JAL tidak berupa compare literal `manager+0x2E9 == 9`; byte tersebut dibaca lalu diindeks melalui jump-table, sesudah pemeriksaan batas.

### (b) Debit event 3/8

Fungsi: `FUN_800D15A8`.

- Fee tile dibaca sebagai unsigned halfword di `tile+0x1A`:
  `800D4628 [1A 00 44 94] lhu a0,0x1a(v0)`
- Saldo kerja participant dibaca dari `participant+0x04`:
  `800D462C [04 00 62 8C] lw v0,0x4(v1)`
- Perbandingan dan keluar bila saldo kurang:
  `800D4634 [2A 10 44 00] slt v0,v0,a0`
  `800D4638 [88 02 40 14] bne v0,zero,0x800d505c`
- Fee dibaca ulang lalu dinegasikan:
  `800D46EC [1A 00 42 94] lhu v0,0x1a(v0)`
  `800D46F4 [23 10 02 00] subu v0,zero,v0`
- Signed pending debit:
  `800D46F8 [EE 02 82 A4] sh v0,0x2ee(a0)`

Arti kode: `pending[player] = -u16(tile+0x1A)`; sebelum itu saldo kerja `participant+0x04` harus ≥ fee. Field harga `tile+0x0E` tidak menjadi operand debit pada blok ini.

### (c) Argument a1 di setter

Fungsi: `FUN_800BE5D8`, caller langsung setter `FUN_8001387C`.

`800BEC94 [04 00 45 8C] lw a1,0x4(v0)`
`800BEC98 [1F 4E 00 0C] jal 0x8001387c`

Di C decomp, `v0` adalah manager pointer + `playerIndex*0x90`; jadi `a1) adalah saldo kerja setelah pending signed diproses. Getter `FUN_800138EC` dipanggil sesudah setter, lalu nilai kanonis ditulis balik ke `participant+0x04`.

### (d) Apa yang berbeda pada action 3 dan 8

**Masuk/gate:**
- Action 8 memiliki gate khusus pada `FUN_800D15A8`: tile harus bertipe 5; owner bits 12–15 harus sama dengan pemain aktif; fee `tile+0x1A` tidak boleh melebihi saldo kerja; dan `(bits8–11 + 1) < 5). Jika kondisi ini gagal, jalur memanggil `FUN_80100D14(0)` dan tidak masuk transaksi.
- Pada switch validasi tile yang sama tidak ada `case 3` dengan gate identik. Kondisi/produser yang menyiapkan action 3 belum dapat disamakan dengan gate action 8.

**Transaksi yang sama untuk action 3 dan 8:**
- fee: `u16(tile+0x1A)`, bukan tabel fee×level.
- pending: signed `-fee` pada `manager+0x2EE+player*2`.
- nibble bits 8–11: ditulis ulang menjadi nilai lama +1.
- nibble bits 4–7: ditulis ulang menjadi nilai lama +1.
- owner bits 12–15 dipertahankan oleh mask/rebuild pada blok transaksi; tidak ada pergantian owner dalam mutasi bersama ini.
- refresh `FUN_800BB004` dan `FUN_800BE464`, lalu manager+`0x2E9` diset ke `0x16`.

Byte contoh mutasi dua nibble (setiap item ≤64 byte):
`800D4724 [FF F0 63 30] andi v1,v1,0xf0ff`
`800D4764 [20 00 62 A4] sh v0,0x20(v1)`
`800D47F4 [0F FF 63 30] andi v1,v1,0xff0f`
`800D4834 [20 00 62 A4] sh v0,0x20(v1)`

**Pesan/label:**
- Tidak ditemukan token pesan berbeda khusus antara action 3 dan 8 di blok transaksi bersama; pesan teks tersendiri untuk masing-masing action: **TIDAK TAHU**.
- Token `0xBE` ada pada jalur event 1/0x1D (PC `0x800D4974` delay slot setelah helper pesan), bukan bukti pesan untuk action 3/8.
- Nama gameplay action 3 tetap **TIDAK TAHU**. Nama “build Barrier dari netral” belum dibuktikan.

### (e) Apakah level disimpan berbasis-0?

**Ya untuk nilai bits 8–11 pada jalur UI yang ditelusuri (K4 statis terbatas pada jalur itu).** Kode membaca nibble mentah, mengekstrak 0–15, kemudian menambah 1 sebagai argumen helper display:

`800D27D8 [20 00 44 94] lhu a0,0x20(v0)`
`800D27E0 [02 22 04 00] srl a0,a0,0x8`
`800D27E4 [0F 00 84 30] andi a0,a0,0xf`
`800D27E8 [6C 23 04 0C] jal 0x80108db0`
`800D27EC [01 00 84 24] addiu a0,a0,0x1`

Delay slot `addiu +1` memberi nilai tampilan satu tingkat di atas nilai nibble. Ini juga konsisten dengan gate action 8 `(nibble+1)<5` dan transaksi yang menulis `nibble+1`. Klaim ini tidak otomatis mengidentifikasi makna gameplay nibble bits 4–7 secara global.

---

## CE2 — penelusuran biaya lompat level

### Jalur transaksi yang benar-benar tertutup

Dalam blok action 3/8, fee dibaca langsung dari `tile+0x1A` lalu dinegasikan. Tidak ada shift fee berdasarkan d, loop yang mengulang debit, atau lookup `m(d)` pada blok itu. Maka hipotesis “action 3/8 memakai `fee << d`” **tidak cocok** dengan jalur transaksi yang diperiksa.

Sampel record resource 4 pada census table: `+0x0E=120`, `+0x1A=100`. Debit kode action 3/8 menggunakan `+0x1A=100`; angka 120 pada `+0x0E` bukan sumber debit yang digunakan blok ini. Belum terbukti bahwa `+0x0E` merupakan biaya bangun netral; jangan menyebutnya demikian tanpa jalur writer/debit yang cocok.

### Census pembaca/penulis nibble di luar FUN_800D15A8

Sumber: `bb2-tile-nibble-access.tsv` pada run `41730277650`. Ini menampilkan seluruh baris yang classifier ekspornya beri label bits 4–7 atau bits 8–11, dan mengecualikan fungsi transaksi `FUN_800D15A8`. Daftar berikut adalah *candidate access*, bukan bukti semua base register menunjuk tile: setiap baris memakai catatan `DISPLACEMENT_CANDIDATE_BASE_ALIAS_NOT_PROVEN`.

Jumlah classifier: 48 baris terklasifikasi. Meta seluruh offset kandidat `+0x20`: READ=334, WRITE=77, OTHER=11 (bukan berarti semuanya pembaca nibble level).

- `FUN_800b2a58`: 0x800B448C bits8_11 read_EXTRACTED; 0x800B44B0 bits4_7 write; 0x800B499C bits4_7 read_EXTRACTED; 0x800B49CC bits4_7 write-mask; 0x800B4A08 bits4_7 write
- `FUN_800b94e8`: 0x800B980C bits4_7 read_EXTRACTED; 0x800B9C3C bits4_7 read_EXTRACTED
- `FUN_800bb004`: 0x800BB028 bits8_11 read_EXTRACTED
- `FUN_800c815c`: 0x800C8194 bits8_11 read_EXTRACTED
- `FUN_800c88f0`: 0x800C8DAC bits8_11 read_EXTRACTED; 0x800C91C0 bits8_11 read_EXTRACTED; 0x800C99F8 bits8_11 read_EXTRACTED; 0x800CA74C bits8_11 read_EXTRACTED
- `FUN_800cadb8`: 0x800CB2F4 bits8_11 read_EXTRACTED
- `FUN_800cbeb0`: 0x800CC4A0 bits4_7 read_EXTRACTED; 0x800CC880 bits4_7 read_EXTRACTED
- `FUN_800ce628`: 0x800CE908 bits8_11 read_EXTRACTED
- `FUN_800d05b8`: 0x800D0730 bits8_11 read_EXTRACTED; 0x800D0A70 bits8_11 read_EXTRACTED; 0x800D0D08 bits8_11 read_EXTRACTED; 0x800D0DB8 bits4_7 read_EXTRACTED
- `FUN_800db29c`: 0x800DBEF8 bits8_11 read_EXTRACTED; 0x800DBF40 bits4_7 write
- `FUN_800dd7c0`: 0x800DE450 bits4_7 read_EXTRACTED; 0x800DE484 bits4_7 write-mask; 0x800DE498 bits4_7 write
- `FUN_800e3e74`: 0x800E3F50 bits8_11 read_EXTRACTED; 0x800E4128 bits8_11 read_EXTRACTED; 0x800E418C bits8_11 write-mask; 0x800E41E0 bits8_11 write; 0x800E425C bits4_7 read_EXTRACTED; 0x800E42C0 bits4_7 write-mask; 0x800E4314 bits4_7 write
- `FUN_800e5e0c`: 0x800E6090 bits8_11 read_EXTRACTED
- `FUN_800eb434`: 0x800EB534 bits8_11 read_EXTRACTED; 0x800EBB2C bits8_11 read_EXTRACTED
- `FUN_800edd68`: 0x800EE224 bits4_7 read_EXTRACTED; 0x800EE23C bits8_11 read_EXTRACTED; 0x800EE268 bits4_7 write-mask; 0x800EE27C bits4_7 write
- `FUN_800f1ccc`: 0x800F1DD4 bits4_7 read_EXTRACTED; 0x800F2018 bits8_11 read_EXTRACTED
- `FUN_800f2050`: 0x800F209C bits4_7 read_EXTRACTED
- `FUN_800f7adc`: 0x800F7E68 bits8_11 write
- `FUN_800fb80c`: 0x800FBA14 bits4_7 read_EXTRACTED; 0x800FBEAC bits4_7 read_EXTRACTED
- `TIDAK_TAHU`: 0x800EEC18 bits8_11 read_EXTRACTED; 0x800FB674 bits4_7 read_EXTRACTED

### UI target-level dan hasil penelusuran lompat

- `FUN_800EB434` (producer action 8) memindai record tile tipe 5 yang owner-nya sama dengan pemain dan bits 8–11 < 4; ia menghimpun pilihan dan memakai fee `tile+0x1A` untuk memilih biaya terendah. Ini membuktikan pemilihan kandidat petak upgrade satu langkah, bukan pemilih target level d=2/3/4.
- Fungsi yang terklasifikasi seperti `FUN_800D05B8`, `FUN_800DB29C`, `FUN_800E3E74`, `FUN_800EDD68`, `FUN_800F1CCC` membaca/menulis nibble; census belum membuktikan bahwa mereka adalah UI pemilih target-level atau mengalikan fee. Untuk fungsi-fungsi itu peran UI/transaksi: **TIDAK TAHU**.
- Tidak ditemukan bukti pada ekspor saat ini untuk loop d kali atau tabel 1/4/8/16 di jalur action 3/8. Tidak dapat digeneralisasi ke semua aksi lain.

### Hipotesis bersaing dan falsifier

| Hipotesis | Status | Falsifier yang bisa diuji |
|---|---|---|
| HA: pemilih target memanggil blok transaksi dengan fee `base×2^d` (d=2/3/4). | BELUM; tidak cocok dengan blok 3/8 yang memakai fee flat. | Trace PC dari pemilih target sampai pending write dan tunjukkan ada shift/tabel fee keyed by d; bila pending tetap `-tile+0x1A`, HA gugur untuk jalur itu. |
| HB: lompat level memakai event/jalur lain dengan fee berbeda (mis. field lain atau multiplikasi sebelum pending). | Masih mungkin, TIDAK TAHU. | Census producer event dan semua pending writer lengkap; trace bahwa semua jalur masuk ke debit +0x1A yang sama tanpa operand lain akan menggugurkan HB. |
| HC: biaya lompat = d kali biaya satu langkah. | Konflik dengan pengamatan pengguna 400 saat base 100 dan d=2, tetapi pengamatan itu K1/HIPOTESIS, bukan runtime terverifikasi. | Uji satu kasus d=2 pada kondisi sama: 200 akan mendukung HC; 400 akan menggugurkannya. |

### Event 3: bangun netral atau upgrade?

**TIDAK TAHU.** Action 8 telah terikat secara statis ke jalur upgrade satu level pada tile tipe 5 milik pemain. Action 3 menggunakan mutasi debit/level yang sama ketika mencapai blok transaksi, tetapi kondisi asal event 3 dan tipe/owner petak saat producer memicunya belum tertutup. Perbedaan `+0x0E=120` versus `+0x1A=100` pada record 4 tidak membuktikan bahwa 120 adalah biaya build; hanya `+0x1A` yang terbukti menjadi debit action 3/8.

---

## Batas dan integritas

- Tidak ada runtime H6 baru dalam laporan ini; tidak ada klaim K5.
- Tidak ada klaim “Barrier Release” untuk event 1/0x1D; token pesan 0xBE dan nama aksinya tetap TIDAK TAHU.
- Tidak menyebut B44 sebagai Barrier Release.
- Tidak mengubah Release `naruto-checkpoint-39262213468`, visibilitas repo, atau `STATUS.md`.
- Tidak mengunggah ROM/ISO, BIOS, savestate, dump RAM, Memory Card, screenshot, video, atau frame.
- Static max K4. Runtime kredit CE3 masih pekerjaan terpisah.

## Commit yang membuat laporan ini

Commit baru ini hanya akan menambah satu berkas:
- `reports/stage1_economy/CE0_CE1_CE2_STATIC_AUDIT_2026-11-04.md` (1 file).
