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


## BB2 tambahan — positive-credit branch, rumus, dan pemisahan dari debit 3/8

### Identitas cabang pemicu

Pada event byte manager `+0x2EB`, cabang bernilai `1` dan `0x1D` masuk jalur terpisah dari cabang debit `3` dan `8`. Raw code `FUN_800D15A8`:

- `0x800D4968`: set `DAT_80139F03 = 1` (phase/state awal kredit).
- `0x800D4970`: panggil `FUN_80100DCC(0xBE)`.
- `0x800D4978`: panggil `FUN_80100D14(1)`.
- `0x800D4980`: panggil `FUN_80108EE8()`.

`FUN_80100DCC` di `0x80100DCC` menerima parameter 16-bit dan menyimpannya sebagai ID pada object teks/UI `DAT_8013A1D8[0]`, lalu menyiapkan dan menampilkan jendela teks melalui helper UI. Maka **ID pesan 0xBE benar-benar dipakai oleh jalur kredit**. Namun teks Jepang/terjemahan pesan `0xBE` masih **TIDAK TAHU** karena tabel teks/byte string belum berhasil dipetakan ke entri itu. Jangan terjemahkan ID numerik menjadi label gameplay.

### Rumus nilai kredit — terbukti langsung

Setelah pemilihan tile oleh `FUN_800BBD9C()`, indeks tile disimpan di `DAT_8013EB20`. Untuk record tile tersebut, kode mengambil:

- `L = (u16(tile+0x20) >> 8) & 0xF` (nibble level bits 8–11);
- `B = u16(tile+0x1E)`;
- `G = u16(tile+0x1C)`.

Pada phase `DAT_80139F03 == 1`, raw code sekitar `0x800D5228–0x800D5314` menghitung `C = B + L*G`. Hasil dan saldo proyeksi ditulis ke object preview:
- `FUN_80108EAC(C)` pada callsite `0x800D5288`, menyimpan C ke `DAT_8013A554+0xA18`;
- `FUN_80108EBC(balance+ C)` pada callsite `0x800D530C`, menyimpan hasil saldo ke `DAT_8013A554+0xA1A`;
- `FUN_80108E1C()` menyalakan flag preview `DAT_8013A554+0xA14` setelah cek `FUN_80108E94()`.

Pada phase `DAT_80139F03 == 2`, state menunggu `manager+0x370 == 1`, membaca hasil lewat `FUN_80102408()`, menutup preview lewat `FUN_80108E54()`, dan jika commit diizinkan:
- menulis `C` ke pending credit `manager+0x2EE + playerIndex*2`;
- menulis saldo proyeksi `manager+0x51C = participantBalance(+0x04) + C`;
- menulis `DAT_80139F03 = 0x14` dan memulai update UI berikutnya.

Jadi rumus positif yang terbukti statis adalah:

`CREDIT = u16(tile+0x1E) + (((u16(tile+0x20)>>8)&0xF) * u16(tile+0x1C))`.

Rumus ini **bukan** cabang debit 3/8. Cabang 3/8 tetap memakai fee `u16(tile+0x1A)`, melakukan cek saldo dan menulis `-fee` ke pending debit. Kedua jalur memakai field dan tanda delta yang berbeda.

### Tingkat bukti dan batas interpretasi

| Klaim | Status |
|---|---|
| `+0x2EB=1/0x1D` mengaktifkan phase kredit 1 | TERBUKTI STATIS K4 |
| Pesan/UI memakai ID `0xBE` | TERBUKTI STATIS K4 |
| Nilai preview dan commit = `+0x1E + level×+0x1C` | TERBUKTI STATIS K4 |
| Pending credit ditulis di `manager+0x2EE + player*2`, projected balance di `manager+0x51C` | TERBUKTI STATIS K4 |
| Pesan `0xBE` berarti “Barrier Release/結界開放” | TIDAK TAHU |
| Unit nilai kredit itu Chakra | TIDAK TAHU |
| Identitas visual/gameplay dari event byte 1 dan 0x1D | TIDAK TAHU |

**Putusan BB2:** tetap **SEBAGIAN**. Rumus debit 3/8 dan rumus kredit 1/0x1D sudah dibuktikan statis K4, tetapi label pesan/aksi dan identitas currency belum dapat dikonfirmasi; 65 store site `+0x2EB` juga belum seluruhnya ditrace sampai asal nilai. Jangan mengubah sebutan field/ID menjadi “chakra”, “bangun barrier”, atau “Barrier Release” tanpa bukti string/UI yang tepat.

### Bukti raw yang dapat diperiksa

- Dispatcher nilai kredit dan pesan: `0x800D4968–0x800D4980`.
- Dispatcher debit 3/8 dan fee: `0x800D45D0–0x800D46F8` (fee read `0x800D4628`, pending debit write `0x800D46F8`).
- Rumus kredit dan preview: `0x800D5228–0x800D531C`; helper write preview `FUN_80108EAC`, `FUN_80108EBC`, `FUN_80108E1C`.
- Commit pending credit dan projected balance: phase 2 dalam dekompilasi `FUN_800D15A8`; writes `manager+0x2EE + player*2`, `manager+0x51C`, `DAT_80139F03=0x14`.
- Helpers: `FUN_80108EAC` (`+0xA18)), `FUN_80108EBC` (`+0xA1A)), `FUN_80108E1C/FUN_80108E54` (flag `+0xA14)), `FUN_80100DCC` (message token), `FUN_80102408` (reads current queued value), `FUN_80102600(8)` (removes/clears queued item 8).
- Source text: `reports/stage1_economy/aq1-run-41557054116/attempt-1/bb2-d15a8-function-detail.txt`; blob SHA-256 Git blob ID `f07601490638a53e45fb40738ec200f107422129`. Caller graph: `reports/stage1_economy/aq1-run-41557054116/attempt-1/bb2-d15a8-direct-callers.txt`.
- AQ1 run `41557054116`: STATUS=SUCCESS, JOB=analyze-entry1-buffer-base, JOB_ID=125658376355, SOURCE_SHA=`28b3c7380f483e0e158e6089851d7d4a4e72e3e8`, EXIT_CODE=0; summary `reports/stage1_economy/aq1-run-41557054116/attempt-1/ACTIONS_RUN_SUMMARY.txt`.

## BB2 errata — producer dynamic untuk action byte 8

### Temuan jalur +0x2E9 ke +0x2EB di FUN_800EA18C

Census 65 store ke participant manager +0x2EB menunjukkan tiga store immediate yang jelas untuk nilai debit: action 3 pada PC 0x800DAA88 (FUN_800D9570), action 8 pada 0x800EC3A8 (FUN_800EB434), dan action 8 pada 0x800EF3CC (function entry TIDAK TAHU). Tetapi ada jalur producer tidak langsung yang juga dapat mengirim nilai 8 ke dispatcher:

1. FUN_800EA18C memanggil FUN_80102408() dan menyimpan hasil antrean ke iVar4.
2. Saat iVar4 == 1, fungsi memilih tile melalui rantai link, menyimpan indeks tile ke manager+0x2E8 pada PC 0x800EA648, lalu menulis manager+0x2E9 = 8 pada PC 0x800EA654. Manager+0x2EA menerima hasil FUN_800C2570(3) pada PC 0x800EA660–0x800EA664.
3. Pada pemanggilan/fase berikutnya, saat iVar4 == 3, kode membaca manager+0x2E9 pada PC 0x800EAA38, menyalinnya ke manager+0x2EA pada 0x800EAA40, dan menyalinnya ke manager+0x2EB pada 0x800EAA44. Sesudah itu manager+0x2E9 diubah menjadi 0x0F pada 0x800EAA50, sehingga nilai yang masuk +0x2EB adalah nilai sebelum sentinel 0x0F ditetapkan.
4. Nilai 8 ini memasuki switch FUN_800D15A8 yang sama dengan nilai 3/8; tidak ada bukti dalam blok tersebut bahwa 8 mempunyai operasi debit berbeda dari case 3.

Jalur ini melengkapi bukti bahwa nilai +0x2EB=8 tidak hanya berasal dari store literal. Namun hubungan lintas pemanggilan/frames dan prasyarat queue-state harus diuji runtime untuk memastikan tidak ada writer lain yang mengganti +0x2E9 sebelum event iVar4==3.

### Pemisahan producer langsung dan tidak langsung

| Kelas producer | PC | Nilai yang disalurkan | Bukti |
|---|---:|---:|---|
| Immediate direct | 0x800DAA88 | 3 | li v0,3; sb v0,0x2EB(v1) dalam FUN_800D9570. |
| Immediate direct | 0x800EC3A8 | 8 | li v0,8; sb v0,0x2EB(v1) dalam FUN_800EB434. |
| Immediate direct | 0x800EF3CC | 8 | li a0,8; sb a0,0x2EB(v0); function entry TIDAK TAHU. |
| State-copy path | 0x800EA654 → 0x800EAA44 | 8 candidate | +0x2E9=8 ditulis pada 0x800EA654, kemudian disalin ke +0x2EB pada cabang iVar4==3 di 0x800EAA44. |

Catatan agar tidak salah menafsirkan: pemanggilan FUN_800BA9F8(8, tile) pada FUN_800D9570 adalah helper penggambaran/animasi tile; badannya hanya mengisi offset tampilan tile+0x4C..+0x66, bukan menulis manager +0x2E9/+0x2EA/+0x2EB. Jadi argumen 8 di pemanggilan itu bukan bukti action byte 8.

### Hipotesis tambahan + falsifier

| Hipotesis | Status | Falsifier |
|---|---|---|
| H8A — jalur FUN_800EA18C iVar4=1 lalu iVar4=3 merupakan satu rangkaian interaksi yang secara valid menyalurkan 8 ke +0x2EB | HIPOTESIS K2, didukung urutan store state dan salinan pada satu fungsi | Gugur bila runtime menunjukkan state +0x2E9 selalu diganti sebelum iVar4=3, atau penyalinan +0x2EB tidak terjadi pada satu alur input yang konsisten. |
| H8B — direct writers 0x800EC3A8/0x800EF3CC adalah satu-satunya sumber action 8 yang relevan; jalur FUN_800EA18C adalah state UI/animasi lain | HIPOTESIS K1, masih mungkin karena queue phase dan pemanggilan antarframe belum diuji | Gugur jika runtime memaksa state +0x2E9=8 dari FUN_800EA18C lalu event iVar4=3 dan terbukti +0x2EB menjadi 8 sebelum masuk FUN_800D15A8. |

**Update BB2:** tetap SEBAGIAN K4 untuk isi cabang transaksi, tetapi cakupan producer +0x2EB sekarang lebih lengkap: 65 write sites disensus, tiga direct immediate sites 3/8 teridentifikasi, dan satu state-copy route 8 ditelusuri. Belum semua 65 store dan semua kemungkinan jalur register/queue ditelusuri sampai asal input; label aksi, teks ID 0xBE, currency Chakra, dan Barrier Release tetap TIDAK TAHU.

## BB2 errata koreksi delay-slot + hasil Step7 run75

### Koreksi tepat untuk callsite FUN_800C2570

Pada `FUN_800EA18C`, nilai `manager+0x2E9=8` memang disimpan di PC `0x800EA654`. Tetapi uraian lama yang menyebut `manager+0x2EA` menerima return dari `FUN_800C2570(3)` tidak tepat. Instruksi mentah menunjukkan:

```asm
800EA64C lw v1,-0x158c(s0)
800EA650 li v0,0x8
800EA654 sb v0,0x2e9(v1)
800EA658 lw v1,-0x158c(s0)
800EA65C li v0,0x3
800EA660 jal 0x800c2570
800EA664 _sb v0,0x2ea(v1)    # delay slot: simpan konstanta 3 sebelum callee mulai
```

Jadi `+0x2EA=3` adalah substate/phase yang ditetapkan oleh delay slot; bukan hasil return helper. `FUN_800C2570` tidak menerima argumen 3 dan dekompilasinya bertipe `void`.

### Apa yang benar-benar dilakukan FUN_800C2570

Raw/decompile pada Entry 1:

- baca start tile `manager+0x2E8`, byte start-link/offset `manager+0x366`, dan batas iterasi `manager+0x2E7`;
- ikuti indeks link petak berurutan (record link dari offset `+0x01` yang dipilih lewat offset per-pemain);
- hitung langkah yang record tujuannya bukan type `6`;
- hentikan traversal ketika mencapai petak type `3` atau penghitung mencapai batas `manager+0x2E7`;
- simpan indeks tile akhir ke `manager+0x389` pada delay slot return `0x800C2678`.

Jadi helper ini mengatur posisi tile yang ditelusuri dan menyimpan hasil posisi ke `+0x389`; ia tidak menulis saldo, fee, owner, atau teks UI. Caller yang terverifikasi mencakup `FUN_800EA18C` pada site `0x800EA660` dan `FUN_800EF9A4` pada site `0x800F0B58`.

### Bukti dynamic action-8 setelah koreksi

Urutan yang tetap terbukti statis adalah:

1. `0x800EA654: sb 8, manager+0x2E9`; `0x800EA664: sb 3, manager+0x2EA` sebagai delay slot.
2. `FUN_800C2570` menelusuri link tile dan menulis indeks akhir ke `manager+0x389`.
3. Pada state antrean `iVar4==3` di pemanggilan/fase lanjut, `0x800EAA38` membaca `manager+0x2E9`, `0x800EAA40` menyalinnya ke `+0x2EA`, dan `0x800EAA44` menyalinnya ke `+0x2EB`.
4. Setelah copy, `0x800EAA50` mengganti `+0x2E9` menjadi sentinel `0x0F`.

Dengan demikian candidate dynamic action byte `8` pada `+0x2EB` berasal dari `+0x2E9=8` yang sudah diset lebih dulu, bukan dari return FUN_800C2570. Kontrol-flow ini K4 statis; konsistensi antar-pemanggilan belum dikonfirmasi oleh BB3 karena run 40-launch belum menghasilkan hasil.

### Helper flag UI pesan

`FUN_80100E9C` yang ikut diekspor pada Step7 run75 hanya mengubah field `DAT_8013A1D8+0xB8`:
- parameter 0 → tulis 1 ke `+0xB8`;
- parameter nonzero → tulis 0 ke `+0xB8`.

`FUN_80100DCC` memanggil helper ini sebagai bagian dari setup message window. Fungsi tersebut bukan string-table lookup dan tidak memetakan token `0xBE` ke teks Jepang. Oleh karena itu arti pesan `0xBE` tetap TIDAK TAHU; tidak boleh diterjemahkan sebagai `結界開放` atau Barrier Release tanpa sumber string yang tepat.

### Run statis Step7 41559535429

`run-summary.txt` melaporkan `STATUS=SUCCESS`, `JOB=analyze-entry1-buffer-base`, `JOB_ID=125666521042`, `SOURCE_SHA=424743337e525da13d8a376aaede756c0b7f1400`, dan `EXIT_CODE=0`. Private input/project cleanup tercatat PASS. Ghidra tidak menjalankan game/emulator dan tidak mengirim gameplay input. Run mempublikasikan 52 file teks/TSV, termasuk export fungsi `FUN_800C2570` dan `FUN_80100E9C`.

- Summary: `reports/stage1_economy/aq1-run-41559535429/attempt-1/ACTIONS_RUN_SUMMARY.txt`
- Raw function evidence blob: `bb2-d15a8-function-detail.txt`, Git blob SHA `cd92a9edabca777a652fc61c83e0a46e73c6530d`.
- Changed files from publication commit: 52 text/TSV files under `reports/stage1_economy/aq1-run-41559535429/attempt-1/`.

**Putusan BB2 setelah koreksi:** tetap SEBAGIAN. Dynamic source action8 lebih jelas, namun producer `+0x2E9/+0x2EA` lain belum seluruhnya di-origin trace; makna UI action dan unit currency masih TIDAK TAHU.

## BB2 errata — lebih banyak sumber queued-state untuk event +0x2EB

### Batas census

Pada export fungsi Entry 1 yang digunakan oleh AQ1 run 41559535429, ditemukan 65 store ke participant-manager +0x2EB, 95 store ke +0x2E9, dan 11 store ke +0x2EA di dalam fungsi yang dipilih/diekspor. Angka tersebut adalah coverage dari function set audit ini, bukan klaim seluruh ROM telah dipindai menyeluruh. Karena sebagian event ditetapkan lewat pola copy +0x2E9 → +0x2EB, direct immediate store 3/8 bukan satu-satunya jalan yang bisa mencapai dispatcher.

### Sumber antrian nilai 8

Selain dynamic route FUN_800EA18C yang sudah dijelaskan di atas, dua producer antrean lain yang terverifikasi statis:

| Fungsi | PC | Byte yang ditulis | Instruksi/context |
|---|---:|---|---|
| FUN_800D15A8 | 0x800D3334 | manager+0x2E9=8 | 0x800D332C li v0,8; 0x800D3330 jal FUN_80113F58; 0x800D3334 sb v0,0x2E9(a0) (delay slot call). Ini menyiapkan queue-state, bukan direct write ke +0x2EB. |
| FUN_800F3658 | 0x800F4CC8 | manager+0x2E9=8 | 0x800F4CC4 li v0,8; 0x800F4CC8 sb v0,0x2E9(v1). |
| FUN_800F3658 | 0x800F4CD4 | manager+0x2EA=3 | 0x800F4CD0 li v0,3; 0x800F4CD4 sb v0,0x2EA(v1). Ini pasangan substate queue, bukan event action 3. |
| FUN_800EA18C | 0x800EA654 | manager+0x2E9=8 | li v0,8; sb v0,0x2E9(v1). |
| FUN_800EA18C | 0x800EA664 | manager+0x2EA=3 | Delay slot sesudah jal FUN_800C2570; konstanta 3 ditulis sebelum helper berjalan, bukan nilai balik helper. |

Penting: +0x2E9=8 adalah queued state. Belum setiap callsite di atas dibuktikan mencapai +0x2EB=8 dalam urutan yang sama di runtime. Jalur EA18C memiliki bukti transfer berikutnya yang eksplisit: queue state iVar4==3 menyalin +0x2E9 ke +0x2EA dan +0x2EB di 0x800EAA40/0x800EAA44, kemudian mengganti +0x2E9 menjadi 0x0F. Untuk D15A8/F3658, ada state-copy/dispatch yang berkaitan di codebase, tetapi belum dibuktikan satu trace runtime untuk setiap cabang.

### Sumber queued-state kandidat 0x1D untuk credit route

Dua lokasi statis mengisi byte manager +0x2E9 dengan 0x1D:

- FUN_800D15A8, PC 0x800D5400: setelah state memeriksa field manager +0x4CC dan projected balance +0x51C, instruksi li v0,0x1D; sb v0,0x2E9(v1).
- FUN_800DC2E0, PC 0x800DD4A0: salah satu kondisi pada branch status manager +0x4F0<0, daftar/kelompok +0x4CC tidak kosong, dan func_0x80012AD0() & 1 == 0 mengisi +0x2E9=0x1D. Pada state machine yang sama, case 0x10 kemudian dapat menulis delta ke pending participant +0x2EE + player*2 dan menyalin +0x2E9 → +0x2EB di PC 0x800DC530 setelah helper/message path FUN_800C2FD8(0x25B). Ini menunjukkan rute queued-state 0x1D secara statis; interpretasi event final tetap tidak diberi nama gameplay.

### Peran FUN_800D9570: menyalin state perintah

Dalam FUN_800D9570, hasil FUN_80102408() dipakai sebagai selector beberapa cabang. Cabang seperti uVar6==7, 3, 1, 0, dan 2 membaca manager +0x2EA, menyalinnya ke +0x2E9, melakukan update peserta/tile, lalu melalui FUN_800C2FD8(0x25F) menyalin nilai +0x2E9 ke +0x2EB sebelum menandai +0x2E9=0x12. Ini menguatkan bahwa +0x2EA dan +0x2E9 adalah tahap perintah/queue; nilainya tidak boleh otomatis diberi arti aksi gameplay hanya karena kebetulan 3 atau 8.

Satu helper dalam jalur tersebut, external func_0x800143AC, belum dipetakan dalam export ini. Oleh karena itu asal lengkap semua nilai register yang mengalir ke +0x2EA/+0x2E9 belum tertutup.

### Hipotesis dan falsifier yang tersisa

| Hipotesis | Status | Falsifier |
|---|---|---|
| H8A — queued-state +0x2E9=8 dari D15A8/F3658/EA18C adalah jalur-jalur berbeda yang akhirnya mengirim event 8 ke dispatcher bila fase/transisi berikutnya berhasil | HIPOTESIS K2; dukungan dari direct state writes dan transfer EA18C yang terbukti | Gugur untuk suatu jalur jika runtime menunjukkan queue phase berakhir/diganti sebelum salinan ke +0x2EB, atau +0x2EB tidak bernilai 8 ketika dispatcher membaca event. |
| H8B — hanya sebagian queue-state 8 yang benar-benar mencapai case debit 8; sisanya state UI/animasi atau event lanjutan yang berbeda | HIPOTESIS K2; didukung adanya beberapa phase dan perubahan sentinel | Gugur jika trace runtime setiap source menghasilkan +0x2EB=8 tepat sebelum switch dispatcher dan selalu mengeksekusi block debit yang sama. |
| H1D-A — queued-state +0x2E9=0x1D dari D15A8/DC2E0 berakhir pada credit branch 1/0x1D | HIPOTESIS K2; alur copy DC2E0 ke +0x2EB ditunjukkan statis; hubungan D15A8 per case belum seluruhnya dipastikan | Gugur jika runtime menunjukkan state berubah sebelum copy atau dispatch byte bukan 0x1D. |
| H1D-B — beberapa source 0x1D adalah state transisi/akhir dan bukan pemicu credit yang sama | HIPOTESIS K1/K2; sejumlah PC berada pada bagian state machine yang berbeda | Gugur jika trace runtime menunjukkan masing-masing source berakhir pada dispatcher +0x2EB=0x1D dan menjalankan preview→commit credit state1→2 yang sama. |

Putusan BB2: tetap SEBAGIAN. Perilaku debit 3/8 dan formula/pending credit sudah K4 statis. Audit kini membedakan immediate producer, queue producer, substate, dan copy ke event field. Producer origin untuk keseluruhan 65 store belum tertutup, serta teks token 0xBE, identitas gameplay untuk event 3/8 dan 1/0x1D, unit currency Chakra, serta nama Barrier Release semuanya tetap TIDAK TAHU.

## BB2 penutup tambahan — pending credit terbukti masuk ke saldo Chakra kanonis

### Pemroses antrean manager+0x2EE

Direct-caller census Entry 1 membuktikan `FUN_800BE5D8` adalah caller langsung setter `FUN_8001387C` pada PC `0x800BEC98`. Decompilation function `FUN_800BE5D8` menunjukkan ia memproses empat slot signed-short `manager+0x2EE + playerIndex*2`:

1. Bila pending slot bukan nol, fungsi mengambil saldo kerja participant `manager+0x04 + playerIndex*0x90` dan menginisialisasi state animasi perubahan saldo.
2. Tanda pending membedakan operasi tambah dan kurang. Nilai absolut dipecah ke digit, lalu saldo kerja dinaikkan/diturunkan bertahap dalam satuan 1, 10, 100, 1000, atau 10000 sesuai digit yang sedang dianimasikan.
3. Setelah tiap langkah, fungsi memanggil `FUN_8001387C(playerIndex, participantBalance)` dan membaca balik melalui `FUN_800138EC(playerIndex)`; hasil getter ditulis kembali ke mirror `participant+0x04`.
4. Saat semua digit habis, fungsi mengosongkan slot pending `manager+0x2EE + playerIndex*2`.

Jika bit sharing `func_0x80012AD0() & 0x1000` aktif, fungsi juga dapat menyalin pending delta ke peserta lain yang memiliki field identitas/kelompok sama pada `participant+0x0E`; hal ini merupakan aturan distribusi tim yang terpisah dari rumus nilai tile dan perlu tetap diperlakukan sebagai kondisi mode.

### Hubungan setter ke field Chakra

Raw/decompile `FUN_8001387C` (Main EXE):
- PC `0x800138C4` membentuk base `0x80070EA0`;
- PC `0x800138C8–0x800138DC` menghitung `playerIndex * 0xB4`;
- PC `0x800138E0` menjalankan `sw a1,0x18(a0)`;
- decompile: `*(int *)(&DAT_80070EB8 + playerIndex * 0xB4) = value`, dengan validasi indeks `<4` dan clamp `-9999..99999`.

Getter `FUN_800138EC` membaca field yang persis sama pada `0x80070EA0 + playerIndex*0xB4 + 0x18`. Audit AZ3 yang sudah ada mengidentifikasi field PlayerRecord `+0x18` sebagai saldo Chakra kanonis; participant `+0x04` adalah saldo kerja/shadow yang disinkronkan lewat getter/setter. Dengan demikian rantai kredit positif kini tertutup secara statis:

`FUN_800D15A8 state 1/2 → C=tile+0x1E+level×tile+0x1C → pending manager+0x2EE → FUN_800BE5D8 → FUN_8001387C → PlayerRecord+0x18 (Chakra)`.

Jadi jumlah Chakra yang dikreditkan oleh cabang positif tersebut adalah `C = u16(tile+0x1E) + (((u16(tile+0x20)>>8)&0xF) * u16(tile+0x1C))`, untuk petak yang dipilih dan level bits 8–11 pada saat perhitungan. Ini terkonfirmasi K4 statis, bukan runtime K5 untuk rute kredit.

### Batas identitas peristiwa

| Pernyataan | Status |
|---|---|
| Nilai rumus `C` ditampilkan sebagai preview dan disimpan sebagai pending positif | TERBUKTI K4 |
| Pending positif diproses ke PlayerRecord+0x18, saldo Chakra kanonis | TERBUKTI K4 |
| `manager+0x2EE` adalah antrean perubahan saldo bertanda; positif menambah dan negatif mengurangi | TERBUKTI K4 |
| Pesan token `0xBE` menampilkan label Jepang `結界開放` | TIDAK TAHU |
| Event `+0x2EB=1/0x1D` adalah Barrier Release, bukan aksi tile lain | TIDAK TAHU |
| Nilai `C` tersebut merupakan hasil Barrier Release secara spesifik | TIDAK TAHU sampai label/aksi pemicunya dipetakan |

Dua hipotesis tetap terbuka, dengan falsifier:
- **HR1:** event `+0x2EB=1/0x1D` dan message token `0xBE` adalah Barrier Release yang mengkredit `C` Chakra. Gugur jika tabel pesan/UI membuktikan token `0xBE` bukan `結界開放`, atau gameplay normal dengan label itu tidak memasuki state 1→2 ini.
- **HR2:** event yang sama adalah aksi lain (misalnya klaim/cashout petak) yang mengkredit `C` Chakra. Gugur jika tabel pesan/UI yang cocok atau pengamatan gameplay normal menghubungkan token `0xBE` dan state 1→2 secara langsung ke `結界開放`.

**Putusan BB2 setelah bukti setter:** formula Chakra dan jalur debit/pending kini K4 statis. BB2 masih **SEBAGIAN**, karena identitas Barrier Release/action, teks token `0xBE`, dan asal seluruh store action byte belum tertutup. Jangan ganti TIDAK TAHU dengan nama aksi yang hanya diduga.

### Bukti primer

- Caller/func detail `FUN_800BE5D8`, termasuk direct setter caller PC `0x800BEC98`: `reports/stage1_economy/aq1-run-41559535429/attempt-1/az3-setter-direct-callers-entry1.txt`, blob SHA `fdf8e77b8a18496bc1941c9485cbe336f0eb131e`.
- Setter/getter Main EXE: `reports/stage1_economy/aq1-run-41559535429/attempt-1/az3-setter-caller-main-exe-detail.txt`, blob SHA `35a20f7f527f2f4c0a09d14792653029adcf508e`.
- Penetapan field +0x18 sebagai saldo Chakra kanonis dan participant+0x04 sebagai shadow telah tercatat di `reports/stage1_economy/AZ0_AZ3_FINAL_STATUS_2026-11-02.md`.
- Static Actions run `41559535429`: STATUS=SUCCESS; JOB=`analyze-entry1-buffer-base`; JOB_ID=`125666521042`; SOURCE_SHA=`424743337e525da13d8a376aaede756c0b7f1400`; EXIT_CODE=`0`. Summary: `reports/stage1_economy/aq1-run-41559535429/attempt-1/ACTIONS_RUN_SUMMARY.txt`.