# BB1/BB2 — addendum penelusuran chain selector dan producer action

Tanggal: 3 November 2026  
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

## Putusan addendum

- BB1 tetap TUNTAS K4 dalam batas fungsi/array yang diekstrak: field petak +0x0B adalah jumlah link berikutnya yang diterima pada rantai tile type 5 dengan owner sama. Apakah relasi link selalu merupakan ketetanggaan geometris: TIDAK TAHU.
- BB2: mekanisme transaksi action byte 3/8 dan jalur kredit positif terpetakan K4; audit producer masih SEBAGIAN karena store tambahan action 8 di 0x800EF3CC belum dapat ditempatkan ke fungsi/caller. Label gameplay action 3/8 juga TIDAK TAHU.

## BB1 — rumus persis +0x0B dan batas rantai

Dekomplikasi FUN_800BE0E4 menunjukkan:

1. Untuk seluruh record, fungsi menyalin tile+0x0B ke buffer lokal lalu mengosongkan field tersebut.
2. Untuk tile awal bertipe 5 yang +0x0B masih nol, fungsi mengambil indeks berikutnya dari byte tile+0x01.
3. Setiap target link yang diperiksa harus bertipe 5 dan memiliki nibble owner bits 12–15 di tile+0x20 yang sama dengan tile awal.
4. Untuk setiap link yang lolos, iVar8 bertambah satu. Iterasi berhenti ketika terjadi mismatch atau setelah lima link diterima (iVar3 < 5).
5. Jika iVar8 tidak nol, fungsi menulis nilai iVar8 ke +0x0B pada tile awal dan semua record yang diikuti. Jumlah penulisan iVar8+1; jadi +0x0B = jumlah record lanjutan / panjang rantai minus satu, bukan jumlah record total.
6. Nilai iVar8−1 dikirim ke func_0x800152C8 dan func_0x80015274, yang selanjutnya mengubah state turunan per-owner.

Batas numerik penting: loop menerima paling banyak lima link lanjutan. Secara struktur, tile awal ditambah sampai lima target link berarti fungsi dapat menulis rantai berisi sampai enam record, jika seluruh link valid dan tidak kembali ke record yang sama. Ini berbeda dari pengamatan pengguna bahwa kelompok maksimum lima; belum ada bukti apakah data board/aturan lain membatasi kasus keenam. Karena itu jangan menyatakan batas gameplay maksimum lima sebagai fakta statis.

Fungsi tidak memeriksa koordinat atas/bawah/kiri/kanan atau menjalankan flood-fill geometris. Ia hanya mengikuti indeks link +0x01, lalu memeriksa type 5 dan owner nibble. Maka yang terbukti ialah rantai link bertipe 5 dengan owner sama. Apakah setiap link selalu mewakili petak yang bersentuhan secara geometris: TIDAK TAHU.

### Hipotesis yang dapat dibedakan

| Hipotesis | Isi | Bukti saat ini | Falsifier |
|---|---|---|---|
| HA — link mewakili petak berdekatan | +0x01 menyambungkan tile yang benar-benar bertetangga; +0x0B menjadi ukuran kelompok terhubung dikurangi satu. | Konsisten dengan fungsi yang mengikuti +0x01 dan menahan rantai pada type 5 + owner sama, tetapi tidak ada koordinat/arah yang dibandingkan pada fungsi ini. | Satu contoh board yang valid menunjukkan link +0x01 menuju tile yang tidak berbagi sisi/titik tetangga menurut geometri board, atau writer link terbukti memakai urutan non-geometris. |
| HB — link adalah urutan/asosiasi, belum terbukti tetangga geometris | +0x0B hanya menghitung link lanjutan yang lolos type/owner; relasi fisik tile belum ditentukan. | Didukung langsung oleh instruksi yang diekstrak; fungsi tidak membaca koordinat/arah. | Pemetaan runtime/static pada sekurang-kurangnya tiga relasi berbeda menunjukkan setiap link valid selalu menunjuk tetangga geometris dan penulis +0x01 membangun hubungan itu dari tabel tetangga. |

HA dan HB bukan klaim yang sama: HB adalah deskripsi minimum yang terbukti; HA memerlukan bukti tambahan dari struktur board atau producer link.

### Check aritmetika ke pengamatan 50/60/70

Ini hanya memeriksa konsistensi aritmetika berdasarkan multiplier yang diamati pengguna, bukan bukti tambahan bahwa game menerapkan angka multiplier tersebut pada semua board. Dengan H = 50, 60, 70:

| Ukuran kelompok yang diamati | Multiplier observasi | Kandidat selector (= kelompok−1) | H50 | H60 | H70 |
|---:|---:|---:|---:|---:|---:|
| 1 | 100% | 0 | 50 | 60 | 70 |
| 2 | 120% | 1 | 60 | 72 | 84 |
| 3 | 150% | 2 | 75 | 90 | 105 |
| 4 | 180% | 3 | 90 | 108 | 126 |
| 5 | 200% | 4 | 100 | 120 | 140 |

Tabel cocok secara aritmetika dengan contoh pengguna. Ia tidak membuktikan bahwa +0x0B adalah nilai multiplier selector itu sendiri, bahwa multiplier berlaku ke nilai tertentu, atau bahwa kelompok terbesar dalam game benar-benar lima. Kode FUN_800BE0E4 menghitung link count; jalur yang menerjemahkan field itu ke selector/multiplier angka belum diselesaikan oleh addendum ini.

### Semua direct sb +0x0B dan instruksi sebelum store

Sumber census parser heksadesimal: run 41541206308, job 125605524941, source SHA b4baaa6cb65715f5c71223440f23e7d88822d504. Kolom pre12 di bawah adalah instruksi tepat sebelum masing-masing store dalam urutan PC. Bila fungsi dimulai kurang dari 12 instruksi sebelum store, semua instruksi tersedia sejak entry dicatat dan panjang yang lebih pendek tidak dipalsukan.

| PC store | Fungsi / objek | Instruksi sebelum store (paling dekat di kanan) |
|---|---|---|
| 0x800BE1B0 | FUN_800BE0E4; DAT_8013EA84 + index×0x124 | 0x800BE180 lui a3,0x8014; 0x800BE184 addu a0,a1,s2; 0x800BE188 lw v1,-0x157c(a3); 0x800BE18C sll v0,s2,3; 0x800BE190 addu v0,v0,s2; 0x800BE194 sll v0,v0,3; 0x800BE198 addu v0,v0,s2; 0x800BE19C sll v0,v0,2; 0x800BE1A0 addu v0,v0,v1; 0x800BE1A4 lbu v1,0x0b(v0); 0x800BE1A8 nop; 0x800BE1AC sb v1,0(a0) |
| 0x800BE330 | FUN_800BE0E4; DAT_8013EA84 + index×0x124 | 0x800BE300 addiu v0,s3,1; 0x800BE304 move a2,v0; 0x800BE308 blez v0,0x800be354; 0x800BE30C clear s0; 0x800BE310 lui a1,0x8014; 0x800BE314 lw v1,-0x157c(a1); 0x800BE318 sll v0,a0,3; 0x800BE31C addu v0,v0,a0; 0x800BE320 sll v0,v0,3; 0x800BE324 addu v0,v0,a0; 0x800BE328 sll v0,v0,2; 0x800BE32C addu v1,v0,v1 |
| 0x8010CC98 | FUN_8010CC38; object DAT_8013A680, bukan tile array | 0x8010CC68 sw v0,-0x5980(s0); 0x8010CC6C move a0,v0; 0x8010CC70 clear a1; 0x8010CC74 jal 0x80035d48; 0x8010CC78 li a2,0x83c; 0x8010CC7C lw v1,-0x5980(s0); 0x8010CC80 nop; 0x8010CC84 sw zero,0(v1); 0x8010CC88 li v0,3; 0x8010CC8C sb v0,0x7b9(v1); 0x8010CC90 lw v1,-0x5980(s0); 0x8010CC94 li v0,4 |
| 0x8010CD18 | FUN_8010CD00; object DAT_8013A680, bukan tile array | Entry fungsi 0x8010CD00: 0x8010CD00 andi a0,a0,0xff; 0x8010CD04 sltiu v0,a0,4; 0x8010CD08 beq v0,zero,0x8010cd24; 0x8010CD0C lui v0,0x8014; 0x8010CD10 lw v0,-0x5980(v0); 0x8010CD14 nop |
| 0x8010CDB4 | FUN_8010CD2C; object DAT_8013A680, bukan tile array | 0x8010CD84 lw v0,-0x5980(s0); 0x8010CD88 nop; 0x8010CD8C sw zero,4(v0); 0x8010CD90 lbu v0,0x0b(v0); 0x8010CD94 nop; 0x8010CD98 sltiu v0,v0,4; 0x8010CD9C bne v0,zero,0x8010cdb8; 0x8010CDA0 nop; 0x8010CDA4 jal 0x80013610; 0x8010CDA8 nop; 0x8010CDAC lw v1,-0x5980(s0); 0x8010CDB0 nop |
| 0x8010CDE4 | FUN_8010CDD0; object DAT_8013A680, bukan tile array | Entry fungsi 0x8010CDD0: 0x8010CDD0 lui v0,0x8014; 0x8010CDD4 lw v1,-0x5980(v0); 0x8010CDD8 nop; 0x8010CDDC sw zero,0(v1); 0x8010CDE0 li v0,4 |

Dua writer tile yang terbukti adalah 0x800BE1B0 dan 0x800BE330. Empat store lain mengakses pointer DAT_8013A680 yang berbeda, yaitu object selector/menu 0x83C byte; jangan dihitung sebagai writer field record tile.

## BB2 — producer action byte +0x2EB dan jalur kredit positif

### Producer eksplisit yang sudah dilacak

| Store PC | Fungsi / nilai yang ditulis | Caller langsung dan konteks | Kekuatan |
|---|---|---|---|
| 0x800DAA88 | FUN_800D9570: li v0,3 pada 0x800DAA84, kemudian sb v0,0x2eb(v1). | Caller tervalidasi: FUN_800F3658 di 0x800F5E1C. Di fungsi producer ada pemeriksaan FUN_801029F8(5), syarat manager+0x370 == 1, input/menu hasil FUN_80102408, dan cabang state yang memeriksa flag manager+0x360; pada satu jalur jika nilai action lama 2, nilai baru menjadi 1, selain itu nilai baru 3. | K4 untuk instruksi literal 3 dan caller; pemetaan controller/menu intent yang tepat masih belum terbukti. |
| 0x800EC3A8 | FUN_800EB434: li v0,8 pada 0x800EC3A4, kemudian sb v0,0x2eb(v1). | Caller tervalidasi: FUN_800F3658 di 0x800F5CF8. Fungsi merupakan state machine global DAT_80139F39; jalur case 8 yang memanggil FUN_80100F64() dan mendapat hasil 0 menulis action 8 serta mengubah beberapa global state/flag sebelum FUN_80113E6C(3). | K4 untuk instruksi literal 8 dan caller. Hubungan case 8 dengan label gameplay belum terbukti. |
| 0x800EF3CC | Store sb a0,0x2eb(v0); urutan terdekat: 0x800EF3B4 li v0,9; 0x800EF3B8 sb v0,0x2e9(v1); 0x800EF3BC lw v0,-0x158c(a0); 0x800EF3C0 li v1,0xff; 0x800EF3C4 sw v1,0x348(v0); 0x800EF3C8 li a0,8; 0x800EF3CC sb a0,0x2eb(v0). | Ghidra tidak mengembalikan function entry/caller untuk alamat ini dalam census sekarang. Objek manager +0x2EB yang dituju dapat dilacak, tetapi fungsi/trigger lebih jauh belum diketahui. | Store nilai 8 terkonfirmasi K4; identitas producer/caller TIDAK TAHU. |

Ada pula beberapa store +0x2EB yang menyalin nilai dari +0x2E9 ke +0x2EB, contohnya di FUN_800EB434 pada 0x800EB6F8; itu propagation nilai state, bukan konstanta producer baru. Banyak store lain menetapkan byte lain (0x51,0x52,0x54,0x55,0xF, dan sebagainya), sehingga tidak boleh dianggap sebagai producer 3/8 tanpa pemeriksaan nilai aktual register.

Peta producer BB2 belum lengkap. Store eksplisit tambahan 0x800EF3CC masih tanpa function boundary/caller. Maka bagian producer BB2 tetap SEBAGIAN, meskipun blok penerima action 3/8 dalam FUN_800D15A8 terpetakan K4.

### Dua hipotesis label gameplay (belum dipilih)

| Hipotesis | Dugaan | Falsifier |
|---|---|---|
| H-A | Action byte 3 = bangun/pasang Barrier; action byte 8 = upgrade Barrier. | Falsified oleh rekaman gameplay normal yang menunjukkan byte3 selalu ditulis saat upgrade atau byte8 saat pemasangan, disertai tile dan UI yang dapat diperiksa. |
| H-B | Action byte 8 = bangun/pasang Barrier; action byte 3 = upgrade Barrier. | Falsified oleh rekaman gameplay normal yang menunjukkan byte8 selalu ditulis saat upgrade atau byte3 saat pemasangan, disertai tile dan UI yang dapat diperiksa. |

Kedua dugaan belum diverifikasi melalui input kontrol/menu. Fakta bahwa kedua nilai memasuki cabang transaksi yang sama tidak cukup untuk menentukan nama aksi. Mungkin pula salah satunya dipakai oleh konteks UI lain. Nama action 3 dan 8 tetap TIDAK TAHU; jangan menamakannya Barrier placement, upgrade atau release sebelum ada bukti UI/gameplay.

### Pemicu kredit positif di FUN_800D15A8

Selain cabang action 3/8 yang menulis debit, dekompilasi fungsi menunjukkan cabang terpisah di case DAT_80139F03 == 2:

- syarat awal: manager+0x370 == 1;
- panggilan FUN_80102408() disimpan ke DAT_8013EBB0; nilai hasil 0 memasuki jalur kredit; nilai lain tidak menjalankan kredit ini;
- FUN_800BBD9C() memilih tile index dan menyimpannya sebagai DAT_8013EB20;
- untuk tile terpilih:
  credit = u16(tile+0x1E) + ((u16(tile+0x20) >> 8) & 0xF) × u16(tile+0x1C);
- fungsi menampilkan nilai melalui FUN_80108EAC(credit) dan total participant+credit melalui FUN_80108EBC(...);
- jika flag participant +0x0A & 0x100 atau +0x0C & 0x20 aktif, nilai yang sama ditambahkan ke akumulator manager +0x4D4;
- nilai positif itu kemudian ditulis ke slot pending participant manager+0x2EE + participant_index×2, dan total participant+credit disimpan di manager+0x51C;
- state berubah ke DAT_80139F03=0x14, diikuti helper UI/animasi.

Caller langsung yang tervalidasi untuk FUN_800D15A8 adalah FUN_800F3658 di 0x800F5DAC. Cabang kredit tersebut berbeda dari action 3/8; jangan menyamakan rumus kredit per tile ini dengan rumus pemasukan akhir putaran yang telah dikonfirmasi pengguna (floor(sum nilai seluruh petak milik pemain / 2) + 400). Hubungan waktu/gameplay kedua mekanisme itu belum dibuktikan di sini.

## Status yang harus diteruskan

- BB1: TUNTAS K4 untuk makna operasional link-count; geometri neighbor dan batas kelompok gameplay tetap TIDAK TAHU.
- BB2: SEBAGIAN K4 — blok transaksi debit dan kredit positif terbukti; producer action 3 dan salah satu producer 8 ditelusuri, tetapi store 8 di 0x800EF3CC masih belum mempunyai function/caller, dan label gameplay action 3/8 belum dipastikan.
- BB3: lihat BB_STATE.md. Runtime 16/16 pada tile4, level0–3 telah lulus K5-terbatas. Matriks perluasan 40 launch dan capture SHA RAM pada frame180 masih menunggu hasil publikasi Actions.

## Bukti primer

- Census +0x0B: reports/stage1_economy/aq1-run-41541206308/attempt-1/bb2-tile-nibble-access.tsv.
- Census writer action byte: reports/stage1_economy/aq1-run-41541667221/attempt-1/bb2-action-byte-access.tsv.
- Decomp dan raw MIPS: reports/stage1_economy/aq1-run-41541667221/attempt-1/bb2-d15a8-function-detail.txt.
- Caller langsung FUN_800D15A8: reports/stage1_economy/aq1-run-41541667221/attempt-1/bb2-d15a8-direct-callers.txt.


### Target B — apakah kredit state-2 adalah 結界開放?

Jalur state-2 di FUN_800D15A8 adalah kandidat yang perlu diperiksa, bukan bukti bahwa Barrier Release telah ditemukan:

- PC 0x800D5118 membaca manager+0x370 dan mensyaratkan nilai 1.
- PC 0x800D5128 memanggil FUN_80102408; PC 0x800D514C membelok keluar bila hasilnya bukan 0.
- PC 0x800D5154 memanggil FUN_800BBD9C untuk memilih tile.
- PC 0x800D5268 membaca tile+0x1C; PC 0x800D5278 membaca tile+0x1E; level bits8–11 dibaca dari tile+0x20.
- PC 0x800D5288 memanggil FUN_80108EAC dengan nilai tile+0x1E + level×tile+0x1C; PC 0x800D530C/0x800D5314 memanggil helper yang menampilkan total baru dan mengubah state UI.
- Dekompilasi menunjukkan nilai yang sama ditulis ke slot pending participant manager+0x2EE + participant_index×2. Cumulative manager+0x4D4 hanya diperbarui jika flag participant tertentu aktif.

Dua hipotesis yang saat ini belum bisa dipilih:

| Hipotesis | Dugaan | Falsifier |
|---|---|---|
| H-R1 | State-2 positif adalah payout ketika pemain melakukan 結界開放; nilai tile/level menjadi Chakra yang dikembalikan setelah barrier dibuka. | Falsified bila gameplay normal yang jelas menampilkan 結界開放 berjalan tanpa memasuki state-2 / tanpa pending credit rumus tersebut, atau jika state-2 juga terpicu pada aksi non-release yang teridentifikasi. |
| H-R2 | State-2 adalah payout/penyelesaian tile-action lain yang bukan Barrier Release. | Falsified bila gameplay normal dengan label 結界開放 secara berulang memicu state-2, memilih tile, dan menghasilkan pending credit sesuai rumus di atas, sementara aksi tile lain tidak. |

Belum ada run yang menghubungkan label UI Jepang 結界開放, manager action byte, DAT_80139F03 state-2, dan perubahan saldo secara berurutan. Karena itu target B — identitas dan jumlah Chakra dari Barrier Release — masih **TIDAK TAHU**. Direct dispatch BB3 untuk action byte 3/8 tidak menguji state-2. B44 tetap bukan Barrier Release.
