# CC1–CC3 — laporan audit statis Barrier / Chakra
Tanggal: 3 November 2026
Game: Naruto — Shinobi no Sato no Jintori Gassen (SLPS-03553)
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

## Ringkasan status

| Butir | Status | Kelas | Putusan singkat |
|---|---|---:|---|
| CC1 biaya/build/upgrade | SEBAGIAN | K4 pada jalur action 8; K3 untuk pemetaan trigger lainnya | Upgrade Barrier action 8 terbukti mendebit tile+0x1A flat dan menaikkan level satu langkah. Build +0x0E dan tiga pemicu gameplay belum terbukti. |
| CC2 kredit Barrier Release | SEBAGIAN | K4 formula dan jalur Chakra; K1 identitas Release | Kredit positif ke saldo Chakra kanonis terbukti. Apakah event 1/0x1D dan token 0xBE adalah Barrier Release: TIDAK TAHU. |
| CC3 penulis nilai petak | SEBAGIAN | K3 | Tidak ada non-loader writer EA84 yang terkonfirmasi pada subset instruksi yang tersedia. Cakupan writer PC belum lengkap. |
| CC4 runtime | BELUM | K0 | Dilarang berjalan setelah gerbang Actions gagal. Tidak ada H6 launch/poke/Memory Card test. |

## Langkah 0 — write dan Actions

Commit text-only berhasil: `b515f481b3997b3f498305b19974cd0a36127a4a`.
File: `reports/stage1_economy/CC0_WRITE_ACTIONS_PROBE_2026-11-03.txt`.

Pemeriksaan push:
- Combined status: `statuses=[]`.
- Actions: `{"total_count":0,"workflow_runs":[]}`.
- Tidak ada workflow run, job, ataupun exit code. Maka CC4 tidak dijalankan.

## CC1 — pembaca field, biaya, dan jalur upgrade

### Basis tile dan reader inventory

Tile base adalah EA84, slot `0x8013EA84` (`-0x157c` dari `0x80140000`), stride `0x124`. Bukti stride: `sll 3; addu index; sll 3; addu index; sll 2` = index×0x124, ditambahkan ke EA84. EA74 (`-0x158c`) adalah manager peserta stride 0x90, bukan tile.

Inventory reader dari CB2 meliputi 26 fungsi terpilih, bukan keseluruhan EXE:
- tile+0x0E: 3 site. EA84 terbukti pada `0x800D2768` dan `0x800D3BBC`, keduanya di FUN_800D15A8. Site `0x800C9990` (FUN_800C88F0) memakai pointer dari record EA74; aliasnya ke EA84 belum terbukti.
- tile+0x1A: 11 site. EA84 terbukti pada `0x800D0AE4`, `0x800D2520`, `0x800D2ADC`, `0x800D2B5C`, `0x800D3EE4`, `0x800D3F74`, `0x800D4628`, `0x800D46EC`, `0x800E3FBC`, `0x800EB570`. Site `0x800CA748` (FUN_800C88F0) memiliki alias basis yang belum dibuktikan.
- Jadi cakupan terpilih adalah 2/3 reader +0x0E dan 10/11 reader +0x1A dengan basis EA84 terbukti. Jangan menyebutnya census global semua fungsi.

Excerpt MIPS (setiap excerpt singkat):
- `lhu a0,0xe(v0)` @ 0x800D2768
- `lhu a0,0x1a(v0)` @ 0x800D4628
- `lw a1,-0x157c(s2)` @ 0x800D460C

### Action 8: upgrade Barrier teridentifikasi K4

FUN_800EB434 mengumpulkan kandidat petak bertipe 5 milik pemain aktif. Kandidat dibatasi pada level nibble bits 8–11 kurang dari 4; fee minimum berasal dari tile+0x1A. Setelah kandidat dipilih/valid, fungsi menulis event 8:
- 0x800EC3A4: `li v0,8`
- 0x800EC3A8: `sb v0,0x2eb(v1)`

FUN_800D15A8 menerima event 8 bersama event 3 dalam blok transaksi:
- 0x800D4628 membaca u16(tile+0x1A).
- 0x800D4634 menguji saldo peserta terhadap fee.
- 0x800D46EC membaca kembali fee; 0x800D46F4 menegasikannya; 0x800D46F8 menulis pending `-fee` ke manager+0x2EE.
- Nibble bits 8–11 pada tile+0x20 dinaikkan satu di 0x800D4724–0x800D4764; nibble bits 4–7 juga dinaikkan satu di 0x800D47F4–0x800D4834.
- Tidak ada perkalian fee dengan jarak level, shift fee, ataupun tabel m(d) di blok action 3/8.

Kesimpulan: untuk upgrade Barrier yang dipilih oleh producer action 8, debit = u16(tile+0x1A), flat per petak/per operasi; kedua nibble level naik +1. Contoh record 4: fee=100 pada setiap level yang dapat dipilih, bukan 100×m(d). Ini menolak A3 untuk jalur action 8. Kecocokan dengan observasi pengguna tidak mengubah bukti kode statis.

### Event 3, 1, 0x1D, dan 4

- Event 3: ditulis di 0x800DAA88 oleh FUN_800D9570. Ia masuk blok debit/level yang sama dengan 8, tetapi hubungan producer 3 dengan pemasangan Barrier tidak satu-ke-satu dan belum terbukti. Label operasi 3: TIDAK TAHU.
- Event 1 dan 0x1D: jalur terpisah yang menyiapkan state kredit positif, bukan blok debit action 3/8. Keduanya memilih tile, mengatur DAT_80139F03=1, dan masuk jalur formula kredit. Identitasnya sebagai Barrier Release belum terbukti.
- Event 4: FUN_800D15A8 membaca tile+0x0E pada 0x800D2768 dan mengirimkannya ke FUN_80108DC8 untuk UI/preview. Tidak ditemukan penulisan pending debit negatif +0x2EE pada blok tersebut. Maka +0x0E belum terbukti sebagai biaya build.

Tiga pemicu gameplay yang diamati pengguna (bola kristal, berhenti di petak sendiri, akhir putaran) belum dipetakan satu per satu ke event ID/handler. Pemeriksaan own-tile di FUN_800D15A8 pada 0x800D24E0–0x800D25D8 membuktikan filter type 5, owner sama, saldo cukup, dan level+1<5; ini pemeriksaan kandidat/kelayakan, bukan bukti trigger kristal atau akhir putaran. Tidak ada bukti statis untuk lompat level absolut pada action 8; jalur action 8 menaikkan satu level per transaksi.

### 12 instruksi sebelum setter saldo Chakra

Callsite FUN_800BE5D8 → FUN_8001387C berada di 0x800BEC98. Dua belas instruksi tepat sebelumnya:
- 0x800BEC68 `addiu v1,v1,0x4`
- 0x800BEC6C `addu v1,v1,v0`
- 0x800BEC70 `lw v0,0x0(v1)`
- 0x800BEC74 `nop`
- 0x800BEC78 `addiu v0,v0,0x2710`
- 0x800BEC7C `sw v0,0x0(v1)`
- 0x800BEC80 `lw v0,-0x158c(s2)`
- 0x800BEC84 `sll s0,s1,0x3`
- 0x800BEC88 `addu s0,s0,s1`
- 0x800BEC8C `sll s0,s0,0x4`
- 0x800BEC90 `addu v0,v0,s0`
- 0x800BEC94 `lw a1,0x4(v0)`
- 0x800BEC98 `jal 0x8001387c`

EA74 + playerIndex×0x90 + 0x04 adalah saldo kerja peserta. Jadi a1 berasal dari saldo peserta saat itu, setelah FUN_800BE5D8 memproses pending signed delta; a1 BUKAN fee dan bukan fee×m(d). Setter menyinkronkan saldo ke PlayerRecord+0x18.

### Penilaian hipotesis CC1

- A1 (upgrade +1 memakai +0x1A flat; build memakai +0x0E): bagian upgrade didukung K4; bagian build +0x0E belum terbukti. Status SEBAGIAN.
- A2 (build dan upgrade sama-sama +0x1A atau pengali level absolut): untuk action 8, fee +0x1A flat terbukti dan tidak ada pengali level absolut. Untuk build/event 3, biaya Barrier belum diketahui. Status SEBAGIAN.
- A3 (debit=fee×m(d), m(1)=1 dan m(d>1)=2^d): tidak berlaku untuk action 8; action 8 debit flat +0x1A dan menaikkan level +1. Bila pengamatan lompat level terjadi melalui handler lain, handler tersebut belum ditemukan.

## CC2 — kredit positif dan kemungkinan Barrier Release

### Callers FUN_800D15A8

Raw-JAL scan Entry 1 memeriksa 149.103 aligned words. Satu direct-JAL callsite tervalidasi ke FUN_800D15A8 ditemukan:
- PC 0x800F5DAC: `jal 0x800d15a8`.
- Function boundary/caller pada export terakhir: UNMAPPED. Kondisi upstream yang mengantar eksekusi ke callsite itu: TIDAK TAHU.
- Scan ini menutup direct JAL yang ditemukan pada export tersebut; indirect/JALR/dynamic call tidak dapat dikesampingkan.

Di dalam FUN_800D15A8, event +0x2EB=1 atau 0x1D memilih tile melalui FUN_800BBD9C/FUN_800FAD68 dan mengatur DAT_80139F03=1. Pada PC 0x800D4970 fungsi memanggil FUN_80100DCC; delay slot 0x800D4974 memasang argumen 0xBE. Ini membuktikan token pesan 0xBE dipakai di cabang tersebut; teks Jepangnya TIDAK TAHU dan tidak membuktikan nama Barrier Release.

### Formula dan commit Chakra (K4)

Untuk tile terpilih:
`C = u16(tile+0x1E) + (((u16(tile+0x20) >> 8) & 0xF) * u16(tile+0x1C))`

PC utama:
- 0x800D5258–0x800D5264: ekstrak level nibble bits 8–11.
- 0x800D5268: `lhu a0,0x1c(v1)`
- 0x800D5270: `mult v0,a0`
- 0x800D5278: `lhu a0,0x1e(v1)`
- 0x800D5280: `addu a0,a0,v0`
- 0x800D5288: kirim C ke helper preview FUN_80108EAC.

State berikutnya mensyaratkan manager+0x370==1 dan FUN_80102408()==0 sebelum menulis nilai positif ke manager+0x2EE+playerIndex*2 serta saldo proyeksi manager+0x51C. FUN_800BE5D8 mengonsumsi pending signed delta dan memanggil FUN_8001387C; setter menulis:
`PlayerRecord = 0x80070EA0 + playerIndex*0xB4 + 0x18`.
Alamat kanonis field Chakra: 0x80070EB8 untuk player 0. Maka formula C sebagai kredit Chakra pada jalur positif terbukti K4.

Untuk record 4, C level index 0–4 = 84/154/224/294/364. Untuk record 7 = 112/196/280/364/448. Cabang kredit ini membaca +0x1E, +0x1C, dan level; tidak membaca fee +0x1A atau nominal biaya yang dibayar sebelumnya. Dengan demikian B3 didukung K4 untuk cabang ini. Belum ada bukti pengali kelompok 100–200% diterapkan lagi pada C; kode formula positif tersebut menghitung C secara langsung.

### Hipotesis CC2

- B1 (C adalah kredit pada jalur event kandidat): formula dan kredit Chakra terbukti K4. B1 sebagai *hasil Barrier Release* masih belum terbukti.
- B2 (kredit hanya penjualan/cashout, bukan Release): TIDAK TAHU. Cabang event 1/0x1D dan token 0xBE belum diberi label gameplay.
- B3 (hanya bergantung pada level/field ekonomi, bukan jumlah yang dibayar): didukung K4 untuk cabang positif yang dipetakan. Falsifier: nilai paid/fee ternyata masuk ke operand kredit di jalur yang sama atau ada pengali tambahan pada saat commit.
- HR1: event 1/0x1D + token 0xBE adalah Barrier Release. Falsifier: tabel pesan atau gameplay normal menunjukkan token/branch merupakan aksi selain Release.
- HR2: event itu adalah aksi tile/cashout lain. Falsifier: pemetaan pesan dan gameplay normal menghubungkannya langsung ke label 結界開放 serta pelepasan Barrier.

Putusan: jumlah Chakra C pada cabang kredit positif diketahui K4; apakah cabang itu Barrier Release (結界開放) tetap TIDAK TAHU.

## CC3 — penulis +0x10..+0x18 dan rumus dari +0x0E

Inventory terpilih `aw1-tile-field-function-inventory.tsv` berisi 100 fungsi, dengan 224 baris akses pada offset +0x10/+0x12/+0x14/+0x16/+0x18 dan 326 unique candidate writer PCs. Export instruksi gabungan yang tersedia memuat instruksi untuk 118 dari 326 PC; 208 PC lain belum memiliki instruction window pada artefak yang diperiksa. Inventory ini juga menandai basis displacement sebagai belum terbukti; basis harus diverifikasi lewat instruksi per fungsi.

Di antara 19 store halfword `sh` yang berhasil diperiksa:
- Loader FUN_800F7ADC adalah satu-satunya writer yang basisnya terbukti EA84 + index×0x124. PC 0x800F7CE8/0x800F7CFC menulis +0x10; 0x800F7D0C/0x800F7D20 menulis +0x12; 0x800F7D30/0x800F7D44 menulis +0x14; 0x800F7D54/0x800F7D68 menulis +0x16; 0x800F7D78/0x800F7D8C menulis +0x18. Nilai dibaca dari byte record sumber dan dirakit menjadi halfword; ini loader, bukan rumus gameplay.
- FUN_800B2A58 dan FUN_800B63F4 juga punya `sh` pada displacement +0x10/+0x12/+0x18, tetapi basis `-0x1550` adalah objek teralokasi 0x2D4 byte, bukan EA84.
- FUN_800F6988 menulis `sh` pada +0x10/+0x12/+0x18 terhadap basis auxiliary `0x8013ED28 + param_2*0x24`, bukan EA84. Store itu bukan penulis tile.

Putusan terbatas: **tidak ditemukan non-loader writer halfword ke record tile EA84** dalam instruction windows yang berhasil diperiksa. Ini bukan klaim mutlak seluruh program, karena 208 candidate writer PCs belum mempunyai instruction window dan hanya 100 fungsi terpilih masuk inventory. Status CC3 SEBAGIAN K3.

Untuk perhitungan nilai dari harga tile+0x0E:
- Reader +0x0E yang terbukti EA84 dalam FUN_800D15A8 hanya ditemukan pada 0x800D2768 dan 0x800D3BBC; keduanya mengirim nilai ke helper FUN_80108DC8/UI.
- Pada bukti tersebut tidak terlihat rumus yang menghitung +0x10..+0x18 dari +0x0E.
- Fungsi FUN_800F6988 mengambil nilai +0x10/+0x12/+0x18 dari tabel parameter internal, bukan dari tile+0x0E.
- Karena coverage writer belum lengkap, putusan yang aman adalah: rumus runtime dari +0x0E **belum ditemukan pada subset yang diperiksa**, bukan tidak ada di seluruh EXE.

## Cakupan dan artefak sumber utama

- `CB2_STATIC_BARRIER_COST_CREDIT_AUDIT_2026-11-03.md`: reader +0x0E/+0x1A, transaksi action 3/8, 12 instruksi setter, formula credit.
- `BB2_PRODUCER_TRACE_UPDATE_2026-11-03.md`: action 8 sebagai upgrade Barrier; batas event 3; token 0xBE; producer/event detail.
- `BB1_BB2_STATIC_COMPLETE_2026-11-03.md`: jalur formula, writer/loader context, setter Chakra.
- `aq1-run-41567757209/attempt-1/aw1-tile-field-function-inventory.tsv`: 100-function field inventory.
- `aq1-run-41567757209/attempt-1/az3-resource-economy-function-detail.txt`: instruction windows untuk fungsi terpilih.
- `aq1-run-41567757209/attempt-1/bb2-d15a8-function-detail.txt` dan `bb2-d15a8-direct-callers.txt`: dispatch, direct callsite, formula state credit.
- `aq1-run-41567757209/attempt-1/ba1-tile-loader-callers.txt`: loader basis EA84 dan stride.

Tidak ada emulator atau runtime dijalankan dalam audit CC ini. Tidak ada ISO/ROM, BIOS, savestate, Memory Card, RAM dump, video, frame, atau data biner yang diunggah. STATUS.md tidak diubah.
