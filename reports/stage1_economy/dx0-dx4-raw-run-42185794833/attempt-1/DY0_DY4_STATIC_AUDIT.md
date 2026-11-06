# DY0-DY4 — addendum audit statis

Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Baseline inklusif: f76a096862ceb88920df19b021a30870c74a9496
Snapshot source SHA: c191c117ba567607df0feab8e4fc11adce015807
EXE SHA-256: a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569; Entry 1 SHA-256: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a

## Status
DY0: TUNTAS K4 untuk snapshot source; baseline ikut dihitung. Final HEAD dihitung ulang setelah bot publish dan commit laporan akhir.
DY1: TUNTAS K4 untuk tiga branch gate; DX2_PATH_CONDITIONS.tsv ditulis ulang dengan origin setelah JAL/JALR yang diputus pada call boundary.
DY2: SEBAGIAN K4 — census semua store displacement +0x20/+0x21 EXE+Entry1; hanya baris yang basisnya membuktikan slot EA84 dinyatakan tile array. Level source semantik untuk aksi 8/event 3 masih TIDAK TAHU di luar lineage statis yang dilampirkan.
DY3: SEBAGIAN K4 — direct writer global 0x80139EFC dan expression slices; helper retry loop 50 iterasi dan field manager ditemukan, arti gameplay tetap hipotesis.
DY4: SEBAGIAN K4 — store -fee ke +0x2EE dihitung lewat direct call closure D15A8; tidak menyatakan rumus biaya level tanpa bukti d pada operand.

## DY1 — JAL clobber
0x800EC814 bnez $v0: $v0 berasal langsung dari return JAL 0x8010CDF0; fall-through wajib $v0=0.
0x800EC874 bnez $v0: $v0 berasal langsung dari return JAL 0x8010D0F0; fall-through wajib $v0=0.
0x800EC890 beqz $v0: return JAL 0x800154E0 masuk ke $v1; 0x800EC88C sltiu $v0,$v1,0x10 membentuk $v0. Fall-through wajib $v0!=0, ekuivalen return unsigned $v1<0x10.
Semua origin berhenti pada batas JAL/JALR: v0/v1 dilabel return, a0-a3 dan t0-t9 setelah JAL dilabel TIDAK TAHU. File offset EXE mengikuti 0x800+(PC-0x80010000), Entry 1 0x10BB000+(PC-0x800AD450).

## DY2 — tile+0x20/+0x21
DY2_TILE_PLUS20_PLUS21_WRITERS.tsv memuat seluruh operasi store dengan displacement literal +0x20/+0x21 di EXE dan Entry 1. Base slot EA84 dipisahkan dari store yang belum terbukti berasal dari tile array. Mask dan OR-source berasal dari expression slice per PC; hasil tidak boleh ditafsirkan sebagai konstanta saat berasal dari load dinamis/JAL.
Action 8 sites 0x800EC3A8 dan 0x800EF3CC serta event 3 FUN_800D9570 disajikan sebagai jendela instruksi di DY2_ACTION8_EVENT3_LEVEL_SOURCE_WINDOWS.tsv. Event3 D9570 membaca signed halfword +0x24 dari alamat berbasis indeks dan parameter pointer; apakah itu level target = TIDAK TAHU. Nilai beda level d yang eksplisit = TIDAK TERBUKTI dari jendela ini.

## DY3 — global accumulator dan RNG retry
DY3_GLOBAL_80139EFC_WRITERS.tsv hanya memuat store yang effective address statisnya tepat 0x80139EFC. Arithmetic slice memuat PC operand untuk sll/sllv/mult/addu/subu; dependency tile+1A, nibble +0x20, atau field resource +0x14/+0x15 hanya YES jika load pada slice teridentifikasi.
Retry: EC AE8 menetapkan 0x32 (50); EC AEC menyimpan counter manager+0x2A8; EC B00/ B08 membaca dan decrement; EC B0C keluar saat -1. Loop memanggil RNG pada EC B14, menghasilkan remainder melalui div/mfhi di ECB24/ECB28, menyimpan kandidat index di ECB38, membaca active index melalui lhu slot 0x8013EA88 di ECB3C, dan mengulang bila sama pada ECB44. Sukses loop mensyaratkan kandidat != active-index; maksimum 50 pemanggilan RNG.
Field manager +0x4F0/+0x4F4/+0x534 dan PC reader/writer berada di DY3_MANAGER_FIELDS_4F0_4F4_534.tsv. H1/H2 arti gameplay disediakan sebagai hipotesis yang dapat difalsifikasi di DY3_HELPER_STATUS_HYPOTHESES.tsv; tidak ada klaim semantik final.

## DY4 — debit aksi 8
Negative fee post terhitung dari instruksi store yang operand slice-nya berisi negu dan pembacaan tile+0x1A, di direct call closure FUN_800D15A8. Jumlah terdeteksi total=1; yang langsung dilabel FUN_800D15A8=1. Store nol untuk clear pending tidak dihitung sebagai post.
Jika tidak ada back-edge di sekitar site post yang mengeksekusinya berulang, bukti statis ini mendukung satu post -fee per pemanggilan handler, bukan perkalian otomatis d. Ini bukan bukti runtime.
Keempat model formula d=1..4 dalam DY4_FEE_HYPOTHESES_D1_D4.tsv memakai 100 hanya sebagai normalisasi pengamatan pengguna. H2 exact lookup dari empat rasio pengguna ditandai TAUTOLOGI. H3/H4 adalah model debit akumulatif berulang dan bertentangan dengan pengamatan pada nilai d yang dicatat. Formula ROM aktual = TIDAK TAHU.

## Batas
Statis saja; tidak menjalankan emulator/game. Maksimum K4. Nilai runtime, target label untuk field+0x24, arti gameplay +0x4F0/+0x4F4/+0x534, serta rumus biaya ROM = TIDAK TAHU bila tidak terhubung oleh instruction/dataflow proof.
Output text/TSV saja. EXE/DATA.BIN hanya input privat runner; tidak dikomit.
