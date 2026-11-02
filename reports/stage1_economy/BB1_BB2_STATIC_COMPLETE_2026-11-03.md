# BB1–BB2 — hasil final audit statis Barrier / record petak

Tanggal: 3 November 2026  
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

## Status

| Tahap | Status | Kelas | Batas |
|---|---|---|---|
| BB1 — field petak +0x0B dan resource 630 | TUNTAS statis | K4 | Semua store +0x0B dipilah menurut objek; dua store benar-benar menulis record tile. Label gameplay exact tetap TIDAK TAHU. |
| BB2 — biaya dan kenaikan level action 3/8 | TUNTAS statis | K4 | Fee, guard saldo, pending debit, dua level nibble dan refresh helper terbukti. Nama gameplay action 3/8 tetap TIDAK TAHU. |
| BB3 — konfirmasi transaksi runtime | BELUM | K0 transaksi; K2 H6 smoke | H6 load/read-only PASS, tetapi probe transaksi masih memperbaiki harness. Run 41543294021 sedang berjalan ketika laporan diperbarui. |

## BB1 — pemetaan semua store +0x0B

Workflow census parser-heksadesimal yang diperbaiki:
- Run 41541206308; job analyze-entry1-buffer-base, ID 125605524941.
- Source SHA b4baaa6cb65715f5c71223440f23e7d88822d504.
- Status workflow SUCCESS; script exit 0.

Census Entry 1: +0x0B memiliki 15 READ, 6 WRITE, 45 OTHER; +0x20 memiliki 332 READ, 78 WRITE, 11 OTHER. OTHER mencakup instruksi unaligned lwl/swl, bukan direct byte-field writes.

| PC | Fungsi | Instruksi | Objek | Makna statis |
|---|---|---|---|---|
| 0x800BE1B0 | FUN_800BE0E4 | sb zero,0x0B(v0) | DAT_8013EA84 + index×0x124 | Reset field tiap record tile |
| 0x800BE330 | FUN_800BE0E4 | sb s3,0x0B(v1) | DAT_8013EA84 + index×0x124 | Menulis hasil hitungan rantai |
| 0x8010CC98 | FUN_8010CC38 | sb v0,0x0B(v1) | DAT_8013A680 | Inisialisasi objek terpisah 0x83C |
| 0x8010CD18 | FUN_8010CD00 | sb a0,0x0B(v0) | DAT_8013A680 | Set selector 0..3 pada objek terpisah |
| 0x8010CDB4 | FUN_8010CD2C | sb v0,0x0B(v1) | DAT_8013A680 | Normalisasi selector objek terpisah |
| 0x8010CDE4 | FUN_8010CDD0 | sb v0,0x0B(v1) | DAT_8013A680 | Reset objek terpisah dan isi default 4 |

Pemisahan pointer terbukti:
- FUN_800BE0E4 mengambil base dari DAT_8013EA84; alamat record dihitung memakai index × 0x124.
- FUN_8010CC38 mengalokasikan 0x83C byte melalui func_0x8002dec4(0x83c), menyimpan pointer di DAT_8013A680, membersihkan objek, lalu mengisi +0x0B = 4.
- FUN_8010CD00, FUN_8010CD2C dan FUN_8010CDD0 memakai pointer DAT_8013A680 yang sama. Empat store ini bukan writer field tile.
- Hit lwl/swl pada +0x0B bukan direct sb writer field.

### Perilaku operasional tile+0x0B

FUN_800BE0E4 melakukan:
1. Loop semua record tile (jumlah DAT_8013EAC8, stride 0x124); salin byte +0x0B ke buffer lokal, lalu kosongkan field tile +0x0B.
2. Untuk tile type 5 yang +0x0B kosong, ambil link-index pada byte +0x01.
3. Ikuti link pada array tile yang sama selama tile berikutnya juga type 5 dan nibble owner bits 12–15 pada tile+0x20 sama. Loop lokal dibatasi lima iterasi.
4. Tulis penghitung rantai iVar8 ke +0x0B pada tile awal dan record rantai yang diikuti; helper 0x800152C8 dan 0x80015274 juga dipanggil memakai owner dan hitungan tersebut.

FUN_800BE464 membaca +0x0B kembali untuk tile type 5. Bila owner sama dengan pemain aktif, tile +0x38 ditambah 0x40 saat +0x0B=0 atau 0x50 bila nonzero. Bila owner berbeda, +0x38 ditambah 0x30 bila +0x0B nonzero. Ini mendukung interpretasi sebagai status/nilai rantai tile type 5 yang memengaruhi atribut/tampilan. Nama gameplay kanonik field +0x0B: TIDAK TAHU. Field ini bukan biaya Chakra, bukan owner ID, dan bukan level nibble.

### Resource 630 — nilai record source/runtime

Resource 630 memiliki 22 record, source stride 0x1E, runtime tile stride 0x124. Mapping BA1 pada empat snapshot H6: 1.584/1.584 field salinan dan 176/176 field initializer cocok. Nama kolom tetap teknis; label gameplay yang belum terbukti tidak ditambahkan.

| Index | tile+0x0E | +0x10 | +0x12 | +0x14 | +0x16 | +0x18 | fee +0x1A | +0x1C | +0x1E |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 60 | 35 | 70 | 135 | 265 | 530 | 50 | 35 | 42 |
| 2 | 100 | 50 | 110 | 220 | 440 | 880 | 50 | 35 | 70 |
| 3 | 100 | 50 | 110 | 220 | 440 | 880 | 50 | 35 | 70 |
| 4 | 120 | 60 | 140 | 265 | 530 | 1050 | 100 | 70 | 84 |
| 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 6 | 120 | 60 | 140 | 265 | 530 | 1050 | 100 | 70 | 84 |
| 7 | 160 | 85 | 180 | 360 | 710 | 1410 | 120 | 84 | 112 |
| 8 | 140 | 70 | 160 | 310 | 620 | 1250 | 100 | 70 | 98 |
| 9 | 140 | 70 | 160 | 310 | 620 | 1250 | 100 | 70 | 98 |
| 10 | 120 | 60 | 140 | 265 | 530 | 1050 | 100 | 70 | 84 |
| 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 12 | 200 | 100 | 220 | 440 | 880 | 1760 | 150 | 105 | 140 |
| 13 | 220 | 110 | 250 | 490 | 980 | 1940 | 150 | 105 | 154 |
| 14 | 260 | 130 | 290 | 580 | 1150 | 2290 | 200 | 140 | 182 |
| 15 | 220 | 110 | 250 | 490 | 980 | 1940 | 150 | 105 | 154 |
| 16 | 200 | 100 | 220 | 440 | 880 | 1760 | 150 | 105 | 140 |
| 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 19 | 140 | 70 | 160 | 310 | 620 | 1250 | 100 | 70 | 98 |
| 20 | 120 | 60 | 140 | 265 | 530 | 1050 | 100 | 70 | 84 |
| 21 | 100 | 50 | 110 | 220 | 440 | 880 | 50 | 35 | 70 |

Nilai +0x1A hanya terbukti sebagai fee yang dibaca cabang transaksi BB2. Jangan menyamakan semua angka ini dengan biaya pemasangan Barrier. Observasi BB0 yang terpisah hanya membuktikan satu transaksi kontekstual: prompt 必要チャクラ 120 dan saldo Naruto 1500→1380. Data mentah: reports/stage1_economy/BA1_STAGE1_RESOURCE_630_RECORDS.tsv.

## BB2 — transaksi action byte 3/8 pada FUN_800D15A8

Raw MIPS dan dekompilasi FUN_800D15A8 mengonfirmasi kasus switch action byte 3 dan 8 masuk ke blok transaksi yang sama.

| PC | Perilaku |
|---|---|
| 0x800D4470 | lbu v0,0x2eb(v0): baca action byte manager +0x2EB |
| 0x800D45D0 | jal 0x800BBD9C: pilih index tile |
| 0x800D45E0 | simpan index ke manager +0x4A0 |
| 0x800D4628 | baca u16(tile+0x1A) sebagai fee |
| 0x800D462C–0x800D4638 | bandingkan fee dengan saldo participant +0x04; saldo kurang keluar dari transaksi |
| 0x800D46EC–0x800D46F8 | negasikan fee dan simpan pending delta -fee ke manager +0x2EE pada participant aktif |
| 0x800D4724–0x800D4764 | naikkan nibble tile +0x20 bits 8–11 satu tingkat; hasil dibatasi di bawah 5 |
| 0x800D47F4–0x800D4834 | naikkan nibble tile +0x20 bits 4–7 satu tingkat |
| 0x800D4840 | panggil FUN_800BB004 |
| 0x800D4848 | panggil FUN_800BE464 |

Direct-call scan Entry 1 run 41541667221 menemukan satu caller tervalidasi: FUN_800F3658 pada PC 0x800F5DAC, yang memanggil FUN_800D15A8. Decomp caller lengkap belum tersedia.

Nama gameplay action byte 3 dan 8: TIDAK TAHU. Jangan menyebutnya otomatis sebagai aksi Barrier placement. Rumus positif 3 petak milik pemain bukan bagian cabang ini dan belum diuji dalam BB3.

## BB3 — yang masih terbuka

H6 smoke dua launch sebelumnya berhasil: SaveStateLoaded PASS, tile array 0x8013B818, tile count 22, manager 0x801EFBB8, memory-file read PASS, RAM writes NONE, Memory Card disposable tetap sama.

Probe lama 41536404671 berhenti pada setup pertama, bukan transaksi. Commit 59998bf31c4efee0fc3ed6729d973b2f6f20e031 memperbaiki lifecycle: SaveStateLoaded hanya menandai event; setelah load call kembali, emulator di-resume; setup didefer sampai dua GPU VSync.

Run 41542947152 berhasil melewati smoke dan mencapai BB3_POST_LOAD_VSYNC=2, tetapi SETUP_FAIL karena Lua belum mendeklarasikan TILE_INDEX/TILE_STRIDE. Ini bug harness, bukan bukti transaksi game gagal. Commit d99f57ba98e5b2fc598299ceb69bf1ecc7a2f4c6 menambahkan kedua konstanta. Run berikutnya 41543294021 sedang berjalan saat laporan ini diperbarui.

Kriteria BB3 tetap: dispatch tercapai; action byte benar; tile index benar; pending delta -fee; kedua nibble naik; dua refresh helper tercapai; dua launch independen; kartu disposable tidak berubah. Sampai hasil lulus tersedia, BB3 tetap BELUM TUNTAS.

## Kesimpulan

- BB1: TUNTAS statis K4 dalam cakupan array tile Entry 1 dan resource 630.
- BB2: TUNTAS statis K4 untuk transaksi action byte 3/8 dalam FUN_800D15A8.
- BB3: BELUM TUNTAS, transaksi runtime belum lulus.
- Tidak ada ROM/ISO, BIOS, savestate, Memory Card, raw RAM dump, screenshot/video/frame, atau binary yang dikomit dalam laporan ini.
