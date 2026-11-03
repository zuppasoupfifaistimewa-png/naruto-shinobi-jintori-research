# BB1–BB2 — bukti audit statis Barrier / record petak

Tanggal: 3 November 2026
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

## Status

| Tahap | Status | Kelas | Batas |
|---|---|---|---|
| BB1 — field petak +0x0B dan resource 630 | TUNTAS statis | K4 | Dua writer tile +0x0B menghitung petak type-5 berurutan dengan owner sama melalui link +0x01. TSV 22 record membuktikan 22/22 link adalah tetangga ortogonal satu tile dan membentuk ring. +0x0B = jumlah petak lanjutan (ukuran rantai−1). Loop code memungkinkan sampai 5 successor (6 total termasuk awal); ini berbeda dari pengamatan pengguna maksimal 5, dan batas aktual gameplay perlu verifikasi runtime/helper. |
| BB2 — transaksi action 3/8 dan producer +0x2EB | SEBAGIAN | K4 untuk blok transaksi/kredit; producer mapping belum lengkap | Debit fee, pending credit state-2, nibble updates dan refresh terbukti; dua producer langsung (3 dan 8) dilacak, tetapi satu store tambahan 8 di 0x800EF3CC belum punya function/caller yang terbukti. Label gameplay action 3/8 tetap TIDAK TAHU. |
| BB3 — konfirmasi runtime blok transaksi action 3/8 | SEBAGIAN | K5-terbatas pada subcakupan lama | Run 41550406414: 16/16 PASS untuk tile4, action3/8, level0–3. Perluasan 40 launch tile4/7 × action3/8 × level0–4 dengan RAM capture frame180 masih berjalan di run 41553653484; bukan uji input gameplay Story Mode. |

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

**Putusan BB1 rinci:** TUNTAS untuk sasaran audit statis K4. Penghitungan tautan type-5/owner-same, enam direct store, konteks 12 instruksi untuk dua store tile, serta 22/22 hubungan link ke tetangga ortogonal sudah ditutup. Label UI kanonik +0x0B tetap TIDAK TAHU. Loop lokal memungkinkan lima successor (enam petak total termasuk awal), bukan lima petak total; pengamatan pengguna bahwa kelompok maksimal lima belum dijelaskan dan perlu uji batas pada runtime atau helper multiplier.


## BB2 — penulis nilai 3/8, perubahan field, dan cabang kredit positif

### Producer participant-manager +0x2EB

Di antara direct store census pada run 41541667221, dua penulis dengan nilai immediate yang terlihat langsung adalah:

| Nilai | PC store | Fungsi | Rantai instruksi penulis |
|---:|---:|---|---|
| 3 | `0x800DAA88` | `FUN_800D9570` | `0x800DAA80 lw v1,-0x158c(v0)`; `0x800DAA84 li v0,3`; `0x800DAA88 sb v0,0x2eb(v1)`. |
| 8 | `0x800EC3A8` | `FUN_800EB434` | `0x800EC39C lui v0,0x8014`; `0x800EC3A0 lw v1,-0x158c(v0)`; `0x800EC3A4 li v0,8`; `0x800EC3A8 sb v0,0x2eb(v1)`. |

Konteks 12 instruksi sebelum store 3: `800DAA58 li v0,6; 800DAA5C sb v0,-0x6145(v1); 800DAA60 lw v1,-0x158c(s0); 800DAA64 j 0x800daa88; 800DAA68 li v0,1 (delay slot); 800DAA6C jal 0x80102898; 800DAA70 li a0,1; 800DAA74 jal 0x801088a8; 800DAA78 nop; 800DAA7C lui v0,0x8014; 800DAA80 lw v1,-0x158c(v0); 800DAA84 li v0,3`. Konteks 12 instruksi sebelum store 8: `800EC378 sll v0,v0,3; 800EC37C addu v0,v0,v1; 800EC380 sll v0,v0,2; 800EC384 addu v0,v0,a2; 800EC388 lh v0,0x24(v0); 800EC38C nop; 800EC390 subu v0,v0,a0; 800EC394 addiu v0,v0,4; 800EC398 sw v0,0x2b4(a3); 800EC39C lui v0,0x8014; 800EC3A0 lw v1,-0x158c(v0); 800EC3A4 li v0,8`.

Census juga menunjukkan penulis register-to-register lain (misalnya `0x800D9BE4` dan `0x800DA414` dalam `FUN_800D9570`, yang menyalin nilai dari manager+0x2E9), serta banyak store lain yang sumber nilainya belum diketahui. Jadi dua PC di atas adalah producer immediate 3/8 yang terverifikasi; belum terbukti bahwa hanya dua jalur itu yang dapat menyiapkan nilai 3/8 pada semua konteks.

### Detail bersama cabang action 3 dan 8

Keduanya masuk ke blok transaksi yang sama pada `FUN_800D15A8`:
- `0x800D4470`: membaca byte action dari participant manager `+0x2EB`; cabang 3 dan 8 dialihkan ke blok pemilihan petak/transaksi yang sama.
- `0x800D45D0`: `FUN_800BBD9C` memilih indeks petak; `0x800D45E0` menyimpan indeks terpilih di manager `+0x4A0`.
- `0x800D4628`: baca `u16(tile+0x1A)` sebagai fee; `0x800D462C–0x800D4638` membandingkannya dengan field saldo participant `+0x04`; saldo kurang keluar sebelum transaksi.
- `0x800D46F8`: tulis pending delta `-fee` pada manager `+0x2EE` milik peserta aktif (fee dibaca kembali dari tile+0x1A).
- `0x800D4724–0x800D4764`: mask `0xF0FF` lalu tulis kenaikan satu pada nibble bits 8–11 tile+0x20.
- `0x800D47F4–0x800D4834`: mask `0xFF0F` lalu tulis kenaikan satu pada nibble bits 4–7 tile+0x20.
- Owner bits 12–15 di tile+0x20 tidak disentuh blok ini; tidak ada perubahan pemilik yang terbukti dari jalur bersama ini. Setelahnya `0x800D4840` memanggil `FUN_800BB004`, `0x800D4848` memanggil `FUN_800BE464` untuk refresh.

### Hipotesis label gameplay dan falsifier

| Hipotesis | Status | Falsifier yang membedakan |
|---|---|---|
| HA — action 3 = bangun Barrier, action 8 = upgrade Barrier | HIPOTESIS, K1 | Gugur jika pemetaan prompt/input pada writer `0x800DAA88` dan `0x800EC3A8` menunjukkan label/operasi terbalik atau bukan Barrier; atau jika tile sebelum/sesudah tidak menunjukkan transisi bangun lalu upgrade. |
| HB — action 3 = upgrade Barrier, action 8 = bangun Barrier | HIPOTESIS, K1 | Gugur oleh bukti UI/prompt dan prasyarat tile yang menunjukkan urutan kebalikan HA. |
| HC — salah satu action 3/8 adalah Barrier Release | LEMAH/tidak didukung, K1 | Cabang bersama yang sama justru membuat pending debit negatif dan menaikkan dua nibble level; model release yang menghasilkan kredit positif atau mengurangi level gugur bila cabangnya dibuktikan masuk ke blok bersama ini. Release dapat saja memakai state lain di luar cabang 3/8. |

Tidak ada label gameplay yang dinaikkan menjadi fakta. Kecocokan struktur fee + level tidak cukup untuk menyebut action 3/8 sebagai bangun/upgrade; kemungkinan bahwa operasi ini jenis tile lain belum ditutup.

### Cabang kredit positif yang memakai +0x1E/+0x1C

Dispatcher `FUN_800D15A8` membaca state byte global `DAT_80139F03` di awal (raw load pada `0x800D15CC`, alamat efektif `0x80139F03`). Pada `case 1`, setelah `FUN_80100F64()==0` dan pemeriksaan flag peserta, fungsi mengambil petak terpilih `DAT_8013EB20`, lalu menghitung:

```text
reward = u16(tile+0x1E) + ((u16(tile+0x20) >> 8) & 0xF) * u16(tile+0x1C)
```

Raw PCs: baca level bits 8–11 `0x800D5258–0x800D5264`; baca +0x1C dan multiply `0x800D5268–0x800D5274`; baca +0x1E dan tambah `0x800D5278–0x800D5280`; panggilan `FUN_80108EAC(reward)` di `0x800D5288`; pembentukan `saldo participant + reward` dan panggilan `FUN_80108EBC` di `0x800D52D4–0x800D530C`; lalu `FUN_80108E1C` di `0x800D5314`.

Pada `case 2` juga ada jalur reward/pending terpisah: jika `manager+0x370==1` dan hasil `FUN_80102408()==0`, nilai yang sama `tile+0x1E + level*tile+0x1C` dimasukkan ke akumulator manager+0x4D4 bila flag peserta memenuhi syarat, ditulis ke slot pending `manager+0x2EE + participant_index*2`, dan saldo proyeksi di `manager+0x51C` diperbarui. Jalur case 2 ini tidak boleh disamakan otomatis dengan cabang debit action 3/8.

Satu-satunya direct caller tervalidasi untuk `FUN_800D15A8` pada direct-call scan Entry 1 adalah `FUN_800F3658`, site `0x800F5DAC`. Penulis/pemicu upstream yang mengatur `DAT_80139F03=1` (atau state 2) belum ditemukan; helper `FUN_80108EAC/80108EBC/80108E1C` belum diberi semantik Chakra secara independen di audit ini. Jadi rumus reward positif dan site call-nya K4; klaim bahwa ini pemicu Barrier Release atau reward Chakra masih TIDAK TAHU.

**Putusan BB2 rinci:** SEBAGIAN K4. Blok transaksi fee/pending/dua nibble, dua penulis immediate action 3/8, dan cabang reward positif telah dipetakan. Nama gameplay, seluruh jalur register-based penulis +0x2EB, penulis state kredit, dan pembuktian bahwa resource positif itu Chakra/Barrier Release belum ditutup.


### Koreksi/penutupan pemicu state kredit positif

Dalam dispatcher yang sama, sebelum rumus reward state 1/2, ada switch langsung pada byte `participant_manager+0x2EB` (raw `lbu` PC `0x800D4470`, dispatch PC `0x800D4468`):

- `case 1` dan `case 0x1D` memanggil `FUN_800BBD9C` untuk memilih petak, memanggil `FUN_800FAD68` dengan index petak, kemudian menulis `DAT_80139F03=1` dan menyiapkan pesan/UI via `FUN_80100DCC(0xBE)`, `FUN_80100D14(1)`, `FUN_80108EE8()`.
- `case 3` dan `case 8` masuk blok debit/level bersama yang telah didokumentasikan; jalur itu mengisi pending `-tile+0x1A`, menaikkan dua nibble, lalu mengakhiri state kembali ke 0.
- Saat state global menjadi 1, dispatcher menjalankan formula `tile+0x1E + level*tile+0x1C` dan meneruskan jumlahnya ke helper kredit `FUN_80108EAC`/ `FUN_80108EBC`. Pada tahap state 2 berikutnya, formula yang sama masuk ke akumulator/pending per pemain jika syarat manager+0x370 dan pemilihan tile terpenuhi.

Ini menutup sumber *state-machine trigger* positif di dalam dispatcher: byte +0x2EB bernilai 1 atau 0x1D menghasilkan state global 1. Ia belum menutup siapa yang pertama kali menulis +0x2EB dengan nilai tersebut di semua konteks (manager handler input/upstream), maupun label gameplay-nya. Maka hipotesis bahwa nilai 1/0x1D adalah jalur Barrier Release masih HIPOTESIS K1, bukan fakta; falsifier: bila pengamatan prompt/hasil menunjukkan operasi lain atau perubahan selain melepas Barrier, label gugur. Hipotesis alternatif: nilai 1/0x1D adalah klaim/aksi tile lain yang memberi nilai positif rutin; falsifier: menu/UI atau uji runtime yang memperlihatkan perintah Barrier Release dan perubahan Barrier yang konsisten akan menggugurkan alternatif ini.

**Status pemicu kredit:** terpetakan statis K4 sampai boundary `+0x2EB ∈ {1,0x1D} → DAT_80139F03=1 → reward positive branch`; trigger upstream untuk menulis byte, definisi currency helper, dan identifikasi Barrier Release tetap TIDAK TAHU.


### Producer eksplisit pemicu kredit (nilai +0x2EB = 1 dan 0x1D)

Audit writer TSV + konteks disassembly juga menemukan immediate producer untuk dua byte yang masuk ke state kredit positif:

| Nilai | PC store | Fungsi/identitas | Rantai instruksi sumber |
|---:|---:|---|---|
| 1 | `0x800CF94C` | Fungsi tidak teridentifikasi oleh census (function entry TIDAK TAHU) | `0x800CF93C li v1,1`; `0x800CF940 sb v1,0x2ea(v0)`; `0x800CF944 lw v0,-0x158c(s0)`; `0x800CF948 nop`; `0x800CF94C sb v1,0x2eb(v0)`. |
| 0x1D | `0x800E0928` | `FUN_800E03B0` | `0x800E0914 lw v0,-0x158c(v1)`; `0x800E0918 li a0,0x1d`; `0x800E091C sb a0,0x2ea(v0)`; `0x800E0920 lw v0,-0x158c(v1)`; `0x800E0924 nop`; `0x800E0928 sb a0,0x2eb(v0)`. |

Untuk store `0x800CF94C`, 12 instruksi pendahulu lengkap: `800CF91C jal 0x8010ABF8; 800CF920 li a0,1; 800CF924 lui v0,0x8014; 800CF928 sb zero,-0x6144(v0); 800CF92C lw v1,-0x158c(s0); 800CF930 li v0,5; 800CF934 sb v0,0x2e9(v1); 800CF938 lw v0,-0x158c(s0); 800CF93C li v1,1; 800CF940 sb v1,0x2ea(v0); 800CF944 lw v0,-0x158c(s0); 800CF948 nop`. Untuk store `0x800E0928`, 12 instruksi pendahulu lengkap: `800E08F8 sw v0,0x2b4(a3); 800E08FC lui v1,0x8014; 800E0900 li v0,0xff; 800E0904 sw v0,-0x6120(v1); 800E0908 lui v0,0x8014; 800E090C sw zero,-0x611c(v0); 800E0910 lui v1,0x8014; 800E0914 lw v0,-0x158c(v1); 800E0918 li a0,0x1d; 800E091C sb a0,0x2ea(v0); 800E0920 lw v0,-0x158c(v1); 800E0924 nop`.

Jadi rantai dalam dispatcher yang sudah terbukti adalah:

```text
manager+0x2EB == 1 atau 0x1D
  -> FUN_800D15A8 dispatch action pada 0x800D4470
  -> pilih petak (FUN_800BBD9C)
  -> DAT_80139F03 = 1
  -> state-1 credit formula tile+0x1E + level*tile+0x1C
```

Keterangan: byte +0x2EA ditulis lebih dahulu oleh dua producer tersebut; +0x2EB menerima nilai yang sama. Ini menutup producer immediate untuk dua trigger ini, namun bukan seluruh 65 store manager+0x2EB (banyak yang menyalin manager+0x2E9 atau memiliki state lain). Tidak ada dasar menyebut label UI 1/0x1D sebagai Barrier Release tanpa prompt/hasil gameplay terverifikasi.


## Revisi cakupan 3 November 2026

Laporan ini adalah kompilasi bukti statis, bukan klaim semua subbutir BB2 dan BB3 sudah ditutup. Addendum terbaru menambahkan:
- rumus tepat tile+0x0B, batas iterasi lima link lanjutan, ketidakpastian hubungan link dengan geometri tetangga, hipotesis/falsifier, dan check aritmetika terhadap observasi H50/60/70;
- semua enam direct store +0x0B beserta urutan instruksi sebelum store;
- producer manager+0x2EB bernilai 3/8, caller langsung yang tervalidasi, store 8 tambahan yang belum punya function/caller, serta jalur kredit positif state-2.

Lihat laporan pendamping:
reports/stage1_economy/BB1_BB2_PRODUCER_AND_CLUSTER_ADDENDUM_2026-11-03.md

BB2 belum TUNTAS penuh karena producer value 8 di PC 0x800EF3CC dan label gameplay action 3/8 belum terselesaikan. BB3 belum TUNTAS penuh karena run perluasan level0–4/tile4&7 dan hash RAM 2 MiB pra-poke frame180 masih belum terbit.


## BB1 — bukti geometri link +0x01 pada 22 petak

Saya gunakan kembali TSV resource 630 yang sudah ada dari BA1 (tidak ada ekstraksi ROM/runtime baru): `reports/stage1_economy/BA1_STAGE1_RESOURCE_630_RECORDS.tsv`. Untuk tiap 22 record, nilai `runtime_tile_b_01` adalah indeks record berikutnya; `runtime_tile_h_22` dan `runtime_tile_h_24` adalah pasangan koordinat yang disimpan di record. Pemeriksaan 22 sisi, termasuk wrap dari record 21 ke 0, menghasilkan 22/22 langkah orthogonal tepat satu posisi: horizontal `|dx|=40,dy=0` atau vertikal `dx=0,|dy|=36`; tidak ada diagonal, lompat, atau link yang keluar jalur.

| Dari | Ke (+0x01) | (x,y) asal → tujuan | Δx | Δy | Geometri |
|---:|---:|---|---:|---:|---|
| 0 | 1 | (199,150) → (239,150) | 40 | 0 | satu tile horizontal |
| 1 | 2 | (239,150) → (279,150) | 40 | 0 | satu tile horizontal |
| 2 | 3 | (279,150) → (319,150) | 40 | 0 | satu tile horizontal |
| 3 | 4 | (319,150) → (359,150) | 40 | 0 | satu tile horizontal |
| 4 | 5 | (359,150) → (399,150) | 40 | 0 | satu tile horizontal |
| 5 | 6 | (399,150) → (399,186) | 0 | 36 | satu tile vertikal |
| 6 | 7 | (399,186) → (439,186) | 40 | 0 | satu tile horizontal |
| 7 | 8 | (439,186) → (439,222) | 0 | 36 | satu tile vertikal |
| 8 | 9 | (439,222) → (439,258) | 0 | 36 | satu tile vertikal |
| 9 | 10 | (439,258) → (439,294) | 0 | 36 | satu tile vertikal |
| 10 | 11 | (439,294) → (439,330) | 0 | 36 | satu tile vertikal |
| 11 | 12 | (439,330) → (399,330) | -40 | 0 | satu tile horizontal |
| 12 | 13 | (399,330) → (359,330) | -40 | 0 | satu tile horizontal |
| 13 | 14 | (359,330) → (319,330) | -40 | 0 | satu tile horizontal |
| 14 | 15 | (319,330) → (279,330) | -40 | 0 | satu tile horizontal |
| 15 | 16 | (279,330) → (239,330) | -40 | 0 | satu tile horizontal |
| 16 | 17 | (239,330) → (239,294) | 0 | -36 | satu tile vertikal |
| 17 | 18 | (239,294) → (199,294) | -40 | 0 | satu tile horizontal |
| 18 | 19 | (199,294) → (199,258) | 0 | -36 | satu tile vertikal |
| 19 | 20 | (199,258) → (199,222) | 0 | -36 | satu tile vertikal |
| 20 | 21 | (199,222) → (199,186) | 0 | -36 | satu tile vertikal |
| 21 | 0 | (199,186) → (199,150) | 0 | -36 | satu tile vertikal; tutup ring |

Dengan disassembly `FUN_800BE0E4` yang mem-follow `+0x01`, memvalidasi tipe 5 dan owner bits 12–15 yang sama, menaikkan penghitung untuk setiap anggota berurutan, serta menulis penghitung ke anggota rantai, interpretasi HA kini didukung: `tile+0x0B = jumlah petak type-5 berurutan dengan owner sama selain dirinya sendiri (ukuran rantai−1)`, dibatasi lima successor oleh loop, yakni hingga enam petak total termasuk petak awal. Link list resource memang membentuk ring spasial petak yang saling berdampingan. Ini bukan flood-fill 2D bebas; ini scan berurutan di perimeter 22-petak.

**Falsifier yang tersisa:** hipotesis HA akan gugur jika resource/board alternatif menampilkan link+0x01 melompati posisi tetangga atau jika runtime satu kelompok owner sama menunjukkan nilai +0x0B berbeda antar anggota yang seharusnya satu run. Hipotesis HB (tag/status tak terkait adjacency) gugur oleh kombinasi uji type/owner, counter traversal, dan 22/22 koordinat tetangga di resource ini. Pengujian contoh 50/60/70 tetap aritmetika terhadap faktor pengguna 100/120/150/180/200%, bukan observasi gameplay baru.

**Putusan BB1:** TUNTAS dalam lingkup statis yang diminta, K4. Jalur perimeter adjacency, rule same-type/same-owner, dan counter size−1 didukung bukti code+data 22 record. Batas counter yang tampak adalah 5 successor/6 petak total; beda dengan batas kelompok 5 pada pengamatan pengguna, sehingga batas gameplay final masih TIDAK TAHU dan bukan sesuatu yang boleh disimpulkan dari loop saja. Label naratif UI +0x0B tetap TIDAK TAHU.


## Errata BB1 — hitungan batas kelompok (kode vs observasi)

Pemeriksaan ulang instruksi di `0x800BE248–0x800BE298` memastikan kondisi loop adalah `s0 < 5` untuk **successor**. `s3` dimulai dari 0 dan bertambah pada delay slot `0x800BE298` untuk setiap successor yang lolos (maksimal lima); nilai itu ditulis ke +0x0B dan disebarkan ke `s3+1` record mulai dari petak awal. Dengan demikian, kode ini secara lokal dapat menghasilkan +0x0B=5, yaitu enam petak total dalam rantai. Itu bertentangan dengan observasi pengguna yang menyebut kelompok paling besar lima dan selector hanya 0–4.

Hipotesis yang mungkin menjelaskan perbedaan: (HA) helper `FUN_800152C8` / `FUN_80015274` atau tahap pemilihan/validasi setelah pembentukan rantai membatasi nilai yang digunakan untuk faktor kelompok sampai selector 4; falsifier: uji runtime pada enam tile owner sama memperlihatkan nilai selector 5 dipakai untuk pengali 200%. (HB) pengamatan maksimal lima mencerminkan batas setup/board Story Mode, sedangkan field +0x0B secara umum dapat menyimpan lima successor; falsifier: satu board legal dengan enam tile berurutan owner sama menghasilkan rantai +0x0B=5 dan bonus/UI aktif pada enam tile. Keduanya HIPOTESIS K1; bukti statis yang ada hanya membuktikan kapasitas counter, bukan aturan clamp final atau multiplier.

Karena itu, simpulan yang aman: **+0x0B = jumlah successor valid; maksimum yang diizinkan loop ini lima successor (enam total)**. Apakah selector bonus benar-benar dibatasi 0–4 dan ukuran kelompok gameplay maksimum lima petak masih TIDAK TAHU, sampai helper/rantai runtime dibuktikan.


## BB2 errata — penulis ketiga nilai action 8

Census lengkap 65 store ke `participant_manager+0x2EB` menunjukkan satu direct immediate store lain yang sebelumnya belum disorot:

- PC `0x800EF3CC`, enclosing function/function entry TIDAK TAHU pada census; instruksi store `sb a0,0x2eb(v0)`. Sebelum store, `0x800EF3C8 li a0,0x8`, sehingga ini adalah producer immediate nilai 8 (field base berasal dari `lw v0,-0x158c(a0)` di `0x800EF3BC`).
- 12 instruksi sebelum store: `800EF39C nop; 800EF3A0 subu v0,v0,a0; 800EF3A4 addiu v0,v0,4; 800EF3A8 sw v0,0x2b4(a3); 800EF3AC lui a0,0x8014; 800EF3B0 lw v1,-0x158c(a0); 800EF3B4 li v0,9; 800EF3B8 sb v0,0x2e9(v1); 800EF3BC lw v0,-0x158c(a0); 800EF3C0 li v1,0xff; 800EF3C4 sw v1,0x348(v0); 800EF3C8 li a0,8`.

Maka direct immediate write yang teridentifikasi kini: action byte 3 pada `FUN_800D9570/0x800DAA88`; action byte 8 pada `FUN_800EB434/0x800EC3A8`; dan action byte 8 pada `0x800EF3CC` dengan enclosing function belum terpetakan. Ini memperjelas bahwa pemetaan producer +0x2EB belum selesai: census berisi 65 writes, banyak yang menyalin +0x2E9 atau memakai register dinamis, dan function `0x800EF3CC` belum dilabeli. Action 3/8 tidak boleh disebut dua producer tunggal.

**Update status BB2:** tetap SEBAGIAN K4 untuk blok transaksi, karena writer coverage dan identitas aksi masih belum selesai. Hipotesis HA/HB mengenai 3/8 sebagai bangun/upgrade tetap belum dipastikan; hipotesis alternatif yang harus diuji adalah beberapa writer nilai 8 merupakan state/flow yang berbeda dan masuk dispatch code yang sama hanya berdasarkan byte action. Falsifier untuk kesatuan semantik 8: runtime/trace menunjukkan 0x800EC3A8 dan 0x800EF3CC masuk caller/prompt/tile prerequisites yang berbeda atau hasil state yang berbeda. Untuk klaim bahwa keduanya satu aksi: konsistensi flow/UI/field effects di kedua producer dan dispatch menjadi bukti pendukung.


## BB2 update dari AQ1 run 41555549917 — alur preview → kredit final

Run AQ1 tambahan berhasil: `RUN_ID=41555549917`, `JOB=analyze-entry1-buffer-base`, `JOB_ID=125653445027`, `SOURCE_SHA=37beb791fcc48c859b58c312ec1800d44ef77497`, `EXIT_CODE=0`. Census baru tetap menghasilkan 65 write sites ke participant manager `+0x2EB`; direct immediate 3/8 candidate yang teridentifikasi tetap 3 site: 3 di `0x800DAA88` (`FUN_800D9570`), 8 di `0x800EC3A8` (`FUN_800EB434`), 8 di `0x800EF3CC` (function entry TIDAK TAHU). Ini tidak menghapus 62 write sites lain: 31 store v0/2 store zero/2 store v1 tidak ditentukan oleh immediate literal statis dan banyak context membaca `+0x2E9` sebelum copy ke `+0x2EB`. Kandidat immediate bernilai 1, 0x1D, 2, 0x4, 0xE, 0xF, 0x18, 0x25, 0x28, 0x50–0x55, 0x72 dan lainnya adalah action values berbeda; jangan dianggap sebagai action3/8.

### Pembuktian kesinambungan state kredit

Decompile `FUN_800D15A8` menunjukkan secara eksplisit:
1. Switch atas `participant_manager+0x2EB`: action byte `1` atau `0x1D` memilih tile, memanggil `FUN_800FAD68(tile)`, lalu menetapkan `DAT_80139F03=1` dan pesan/UI index `0xBE`.
2. State `DAT_80139F03==1` mengecek `FUN_80100F64()==0`, kemudian menghitung `reward=u16(tile+0x1E)+((u16(tile+0x20)>>8)&0xF)*u16(tile+0x1C)`; memanggil `FUN_80108EAC(reward)` dan `FUN_80108EBC(participant+0x04+reward)`, lalu `FUN_80108E1C()`.
3. Setelah kode pada `LAB_800D5704`, `DAT_80139F03 = DAT_80139F03 + 1`; artinya state 1 benar-benar bergerak ke state 2, bukan state kredit terpisah yang tidak berkaitan.
4. State `DAT_80139F03==2` memerlukan `manager+0x370==1`; mengambil `FUN_80102408()`; saat hasil 0, jalur menulis reward yang sama ke pending `manager+0x2EE + participant_index*2`, memperbarui projected balance `manager+0x51C = participant+0x04+reward`, dan (untuk flag pemain tertentu) menambahkan jumlah itu ke akumulator `manager+0x4D4`; lalu bergeser ke state `0x14` untuk animasi/penyelesaian.

Jadi temuan kuatnya adalah **action byte 1/0x1D → pemilihan tile → preview nilai → state2 finalisasi pending kredit positif**. Belum terbukti nama UI index 0xBE adalah `結界開放`, atau identitas nilai yang diteruskan ke `FUN_80108EAC/8EBC` adalah Chakra (bisa saja nilai resource lain). Karena itu BB2 target B (jumlah Chakra dari Barrier Release) tetap TIDAK TAHU walaupun formula reward/pending credit sudah K4 secara statis.

### Dua hipotesis target Barrier Release dan falsifier

| Hipotesis | Status | Falsifier |
|---|---|---|
| HR1 — rangkaian action byte 1/0x1D → state1→2 adalah Barrier Release dan formula di atas adalah nilai Chakra yang diterima | HIPOTESIS K1; alur pending positif mendukung tetapi label tidak tersedia | Gugur bila UI index0xBE dibuktikan bukan `結界開放`, atau bila input/peristiwa Barrier Release tidak pernah menghasilkan manager+0x2EB 1/0x1D dan state2 ini. |
| HR2 — rangkaian 1/0x1D adalah aksi petak lain (misalnya cashout/claim) yang memberi resource positif, bukan Barrier Release | HIPOTESIS K1; tidak ada nama UI yang berhasil diambil | Gugur bila UI index0xBE atau rekaman input gameplay yang sah menghubungkan tepat rangkaian ini ke `結界開放` dan hasil Chakra. |

### Koreksi caller map

Direct call `FUN_800D15A8` tervalidasi dari `FUN_800F3658` pada PC `0x800F5DAC`; `FUN_800EB434` juga dipanggil `FUN_800F3658` di `0x800F5CF8`. Untuk `FUN_800D9570`, callsite `0x800F5E1C` tervalidasi sebagai raw JAL namun enclosing caller function ditandai UNMAPPED pada census; jangan menyebut caller-nya sebagai `FUN_800F3658`.

**Putusan BB2 setelah run ini:** tetap SEBAGIAN. Perilaku debit action3/8 dan rantai preview→pending-credit kini K4 secara statis; pemetaan nama action, identitas currency, Barrier Release, dan penelusuran semua 65 producer masih belum tuntas.


## BB1 penutup — helper pengali + batas selector terbukti

Run statis AQ1 `41555549917` mengekstrak fungsi Main EXE `FUN_800B770C` dengan dekompilasi dan instruksi mentah. Fungsi menerima indeks tile (a0), menghitung record `tile = base + index*0x124`, lalu membaca `lbu tile+0x0B` (PC `0x800B7730`). Instruksi `sltiu v0,v1,5` pada `0x800B7738` diikuti `beq v0,zero,0x800B7798` pada `0x800B773C`; jika selector >=5 fungsi kembali dengan v0=0. Hanya 0–4 dapat masuk jump table pada `0x800B7744–0x800B7758`.

Untuk selector sah, base H yang dibaca ialah `u16(tile + 0x10 + ((u16(tile+0x20)>>7)&0x1E))`. Lima target tabel mengimplementasikan:

| `tile+0x0B` | Instruksi/fungsi | Hasil | Pengali |
|---:|---|---:|---:|
| 0 | return `H` | `H` | 100% |
| 1 | `H*0xC / 10` | `H*12/10` | 120% |
| 2 | `H*0xF / 10` | `H*15/10` | 150% |
| 3 | `H*0x12 / 10` | `H*18/10` | 180% |
| 4 | `H<<1` | `H*2` | 200% |
| >=5 | early return, nilai v0 dari `sltiu` = 0 | 0 | tidak diterapkan |

Ini menutup selisih batas yang terdeteksi pada loop penghitung `FUN_800BE0E4`: loop dapat secara lokal menulis hingga lima successor (+0x0B=5), tetapi helper nilai ekonomi secara eksplisit menolak selector 5 atau lebih. Jadi rentang ekonomi yang benar-benar diterima adalah 0–4, cocok dengan kelompok 1–5 petak dan pengali 100/120/150/180/200% dari observasi pengguna. Ini bukan sekadar hipotesis clamp lewat helper lain; pemeriksaan nilai dan pemetaan multiplier berada langsung di fungsi pemakai +0x0B.

**Putusan BB1 final:** TUNTAS statis K4. Rumus nilai ekonomi per petak terpetakan: `H = u16(tile + 0x10 + ((u16(tile+0x20)>>7)&0x1E))`; `V = floor(H * [10,12,15,18,20][tile+0x0B] / 10)` (untuk selector 4 implementasinya shift-left satu; rentang nilai integer positif sama). Selector 5+ menghasilkan 0. Uji aritmetika contoh H=50/60/70: selector0 = 50/60/70; selector1 = 60/72/84; selector2 = 75/90/105; selector3 = 90/108/126; selector4 = 100/120/140. Cocok dengan contoh pengguna, tanpa memaksakan angka pengamatan di luar bukti.

### Bukti raw yang dapat diperiksa

- Baca selector dan batas: `0x800B7730 lbu v1,0x0B(v0)`; `0x800B7738 sltiu v0,v1,5`; `0x800B773C beq v0,zero,0x800b7798`.
- Tabel target: `0x800B7744–0x800B7758` (jump table; dispatch berdasarkan selector).
- Kasus 0 dan base H: `0x800B7790 addu v0,v0,v1`; `0x800B7794 lhu v0,0x10(v0)`.
- Kasus 1: `0x800B77DC–0x800B7804`, multiplier 12/10.
- Kasus 2: `0x800B7844–0x800B784C`, multiplier 15/10.
- Kasus 3: `0x800B788C–0x800B7898`, multiplier 18/10.
- Kasus 4: `0x800B78D0–0x800B78DC`, multiplier 2.
- Sumber raw/decompile: `reports/stage1_economy/aq1-run-41555549917/attempt-1/entry1-helper-function-detail.txt`, fungsi DATA.BIN context target `800B770C`; alamat target relatif pada mapping resource entry 1. Entry 1 helper merupakan referensi pembanding; fungsi ekonomi yang dihitung di Main EXE tetap sama perilakunya, sedangkan pemetaan resource entry 1 diverifikasi sebelumnya.


## BB2 tambahan — fee +0x1A dan apakah biaya berubah per level?

### Kesimpulan kode transaksi

Di blok transaksi bersama `FUN_800D15A8`, fee diambil sebagai `u16(tile+0x1A)` pada PC `0x800D4628`; saldo peserta dibaca dari `participant+0x04` di `0x800D462C` dan dibandingkan di `0x800D4634`. Saldo yang lebih kecil dari fee keluar sebelum transaksi. Kemudian fee yang sama dibaca lagi di `0x800D46EC`, dinegasikan pada `0x800D46F4`, dan ditulis sebagai pending debit ke `manager+0x2EE` di `0x800D46F8`.

Fee tidak diambil dari nibble level, tidak dikalikan level, dan tidak berubah setelah kode menaikkan nibble pada `tile+0x20` (bits 8–11 dan bits 4–7 masing-masing +1). Dengan demikian, untuk satu record tile yang sama, setiap pemanggilan transaksi di cabang 3/8 memakai fee `tile+0x1A` yang sama di level 0/1/2/3/4. Level menentukan nilai ekonomi pre/post yang dihitung lewat `FUN_800B770C` (PC `0x800D4658` dan `0x800D4780`), bukan fee.

### Data fee per tile dalam resource Entry 630 (22 record)

Untuk record tipe 4 (petak ekonomi) pada resource 630, TSV `BA1_TILE_TABLE_RECORDS.tsv` dari AQ1 run 41555549917 menunjukkan:

| Record index | Harga neutral +0x0E | H field +0x10 | Fee +0x1A | +0x1C | +0x1E |
|---:|---:|---:|---:|---:|---:|
| 1 | 60 | 35 | 50 | 35 | 42 |
| 2 | 100 | 50 | 50 | 35 | 70 |
| 3 | 100 | 50 | 50 | 35 | 70 |
| 4 | 120 | 60 | 100 | 70 | 84 |
| 6 | 120 | 60 | 100 | 70 | 84 |
| 7 | 160 | 85 | 120 | 84 | 112 |
| 8 | 140 | 70 | 100 | 70 | 98 |
| 9 | 140 | 70 | 100 | 70 | 98 |
| 10 | 120 | 60 | 100 | 70 | 84 |
| 12 | 200 | 100 | 150 | 105 | 140 |
| 13 | 220 | 110 | 150 | 105 | 154 |
| 14 | 260 | 130 | 200 | 140 | 182 |
| 15 | 220 | 110 | 150 | 105 | 154 |
| 16 | 200 | 100 | 150 | 105 | 140 |
| 19 | 140 | 70 | 100 | 70 | 98 |
| 20 | 120 | 60 | 100 | 70 | 84 |
| 21 | 100 | 50 | 50 | 35 | 70 |

Record 4 cocok tepat dengan observasi pengguna: harga petak neutral +0x0E=120; nilai H level pertama +0x10=60, selanjutnya +0x12=140, +0x14=265, +0x16=530; field fee +0x1A=100. Maka untuk tile itu, **fee cabang action 3/8 = 100 pada tiap level yang diizinkan**, sepanjang transaksi tetap memakai record tile yang sama. Pada resource Entry 630, fee bervariasi antarpetak tipe 4 (50/100/120/150/200), jadi ini bukan konstanta global semua tile. Record tipe non-ekonomi tidak dicantumkan karena field nilainya nol.

Perbedaan yang perlu dijaga: `+0x0E` berperan sebagai harga/angka dasar petak netral yang diamati pengguna; `+0x1A` adalah fee debit cabang action 3/8. Jangan menyamakan 120 dengan fee transaksi 100.

### Perubahan field saat transaksi

| Field | Operasi | Kesimpulan statis |
|---|---|---|
| `tile+0x20[11:8]` | baca nibble, +1, mask 0xF0FF, tulis nibble baru di bits 8–11 (PC 0x800D46A4–0x800D4764) | Level yang dipakai `H` bertambah satu. |
| `tile+0x20[7:4]` | baca nibble, +1, mask 0xFF0F, tulis nibble baru di bits 4–7 (PC 0x800D47B4–0x800D4834) | Nibble kedua ikut bertambah satu; nama semantiknya TIDAK TAHU. |
| `tile+0x20[15:12]` | tidak dimask/diganti oleh operasi di atas | Owner bits tidak berubah pada transaksi ini. |
| `manager+0x2EE` | tulis `-u16(tile+0x1A)` | Pending debit fee. |
| `manager+0x922`, `manager+0x924` | tulis hasil `FUN_800B770C` sebelum/sesudah perubahan level | Nilai tile ekonomi pre/post. |

**Putusan target A BB2:** fee operasi yang dipakai cabang action 3/8 adalah field `+0x1A`, dan fee tidak naik per level. Untuk tile contoh (record 4 Entry 630), fee statisnya 100 pada setiap pemanggilan; variasi fee antarpetak dibaca langsung dari record masing-masing. Label gameplay cabang (bangun, upgrade, atau operasi Barrier lain) belum dibuktikan, sehingga kesimpulan biaya Barrier per level secara literal tetap menunggu identitas aksi.
