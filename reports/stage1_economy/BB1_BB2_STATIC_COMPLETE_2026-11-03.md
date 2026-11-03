# BB1–BB2 — hasil final audit statis Barrier / record petak

Tanggal: 3 November 2026
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

## Status

| Tahap | Status | Kelas | Batas |
|---|---|---|---|
| BB1 — field petak +0x0B dan resource 630 | TUNTAS statis | K4 | Semua store +0x0B dipilah menurut objek; dua store benar-benar menulis record tile. Label gameplay exact tetap TIDAK TAHU. |
| BB2 — biaya dan kenaikan level action 3/8 | TUNTAS statis | K4 | Fee, guard saldo, pending debit, dua level nibble dan refresh helper terbukti. Nama gameplay action 3/8 tetap TIDAK TAHU. |
| BB3 — konfirmasi runtime blok transaksi action 3/8 | TUNTAS TERBATAS | K5-terbatas | Run 41550406414: 16/16 uji dispatch-block terisolasi PASS, dua pengulangan per action/level; lihat laporan BB3_RUNTIME_COMPLETE_2026-11-03.md. Bukan uji input gameplay Story Mode dan tidak menetapkan label visual aksi. |

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

## Penutupan BB3 — uji runtime terbatas

Uji runtime terkontrol BB3 selesai pada run 41550406414: 16/16 PASS, nol validation error, dua peluncuran independen untuk masing-masing kombinasi action byte 3/8 dan level nibble 0–3. Status ini menutup konfirmasi runtime pada blok dispatch/transaksi dalam H6 hybrid fixture, bukan demonstrasi input gameplay Story Mode.
- Laporan lengkap: reports/stage1_economy/BB3_RUNTIME_COMPLETE_2026-11-03.md
- Hasil terstruktur: reports/stage1_economy/bb3-h6-action-call-probe-run-41550406414/attempt-1/BB3_ACTION_CALL_RESULTS.tsv
- Ringkasan Actions: reports/stage1_economy/bb3-h6-action-call-probe-run-41550406414/attempt-1/ACTIONS_RUN_SUMMARY.txt


## BB1 — penutupan hipotesis +0x0B, konteks store, dan uji angka

### Semantik yang didukung instruksi

Pada `FUN_800BE0E4`, PC `0x800BE20C` mengosongkan penghitung `s3=0`; PC `0x800BE220` mengambil indeks tautan dari byte record `+0x01`; setiap record yang ditelusuri harus bertipe `5` (uji di `0x800BE260–0x800BE268`) dan nibble pemilik `+0x20 & 0xF000` sama dengan petak awal (`0x800BE270–0x800BE280`). Untuk setiap tautan yang lolos, `s3` bertambah pada delay slot `0x800BE298`. `s3` lalu disalin ke byte `+0x0B` pada petak awal dan anggota rantai (`0x800BE300–0x800BE350)). Ini membuktikan secara statis bahwa +0x0B di record tile adalah **jumlah record type-5 tertaut yang lolos uji owner, tidak termasuk petak awal**; untuk rantai biasa artinya jumlah anggota tertaut selain diri sendiri (kandidat `ukuran rantai−1`).

Bukti tidak menunjukkan pemeriksaan koordinat X/Y atau arah geometris pada segmen ini. Maka identitas “rantai tertaut” K4; klaim bahwa semua tautan selalu berarti petak bersebelahan secara spasial masih TIDAK TAHU sampai penulis/pengisi byte +0x01 dipetakan. Bukan flood-fill berbasis koordinat yang terlihat di segmen ini.

### Dua hipotesis dan falsifier

| Hipotesis | Bukti pendukung | Falsifier |
|---|---|---|
| HA — `+0x0B = jumlah anggota rantai type-5 dengan owner sama selain petak ini` (ukuran rantai−1) | Inisialisasi s3=0; ikuti tautan +0x01; syarat type=5; bandingkan owner bits12–15; s3++ per tautan valid; simpan s3 ke tiap record anggota. | Gugur bila penelusuran runtime menunjukkan tautan +0x01 bukan anggota rantai petak yang sama, atau nilai +0x0B tidak sama dengan jumlah tautan valid dalam record yang ditelusuri. |
| HB — `+0x0B` adalah tag/status bebas yang ditulis dari menu atau sumber non-rantai, tidak mengukur banyaknya anggota | Tidak ada dukungan langsung di record tile; empat writer lain yang ditemukan justru menulis objek selector DAT_8013A680 yang berbeda. | Gugur sebagai penjelasan tunggal karena dua store record tile berasal dari penghitung s3 yang dihasilkan traversal type/owner; empat store lain bukan pointer record tile. Label presentasi masih boleh ikut memakai nilai penghitung. |

### 12 instruksi sebelum dua direct store tile

PC `0x800BE1B0`, `FUN_800BE0E4`, `sb zero,0x0B(v0)` (reset nilai lama):

```asm
800BE180 addiu a1,sp,0x10
800BE184 addu a0,a1,s2
800BE188 lw v1,-0x157c(a3)
800BE18C sll v0,s2,0x3
800BE190 addu v0,v0,s2
800BE194 sll v0,v0,0x3
800BE198 addu v0,v0,s2
800BE19C sll v0,v0,0x2
800BE1A0 addu v0,v0,v1
800BE1A4 lbu v1,0xb(v0)
800BE1A8 nop
800BE1AC sb v1,0x0(a0)
800BE1B0 sb zero,0xb(v0)
```

PC `0x800BE330`, `FUN_800BE0E4`, `sb s3,0x0B(v1)` (menulis hitungan rantai):

```asm
800BE300 addiu v0,s3,0x1
800BE304 move a2,v0
800BE308 blez v0,0x800be354
800BE30C clear s0
800BE310 lui a1,0x8014
800BE314 lw v1,-0x157c(a1)
800BE318 sll v0,a0,0x3
800BE31C addu v0,v0,a0
800BE320 sll v0,v0,0x3
800BE324 addu v0,v0,a0
800BE328 sll v0,v0,0x2
800BE32C addu v1,v0,v1
800BE330 sb s3,0xb(v1)
```

### Cocok dengan observasi angka (data statis, bukan pengukuran gameplay baru)

Record resource index 4 memiliki `+0x0E=120`, `+0x10=60`, `+0x12=140`, `+0x14=265`, `+0x16=530`, `+0x18=1050`; fee field `+0x1A=100`, dan `+0x1C=70`, `+0x1E=84`. Empat nilai pertama sesudah harga cocok tepat dengan observasi pengguna (60/140/265/530); 1050 adalah slot berikut yang belum diamati pengguna, bukan klaim level gameplay baru. `+0x1A=100` tetap fee transaksi pada BB2, bukan harga awal 120.

Perhitungan aritmetis contoh dasar 50/60/70 dengan faktor yang pengguna berikan (bukan hasil runtime): faktor 1.0 → 50/60/70; 1.2 → 60/72/84; 1.5 → 75/90/105; 1.8 → 90/108/126; 2.0 → 100/120/140. Ini konsisten dengan contoh 50→60/72 dan 75/90/105, tetapi belum mengukur perubahan pemilik/tautan di game.

**Putusan BB1 rinci:** SEBAGIAN K4. Penghitungan rantai tertaut type-5/owner-same, semua enam direct store, konteks 12 instruksi untuk dua store tile, dan kecocokan data resource telah ditutup. Belum terbukti bahwa byte tautan +0x01 selalu merepresentasikan tetangga geometris; nama gameplay kanonik +0x0B tetap TIDAK TAHU.
