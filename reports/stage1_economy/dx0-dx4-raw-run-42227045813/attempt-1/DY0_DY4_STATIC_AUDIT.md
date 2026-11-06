# DY0-DY4 — addendum audit statis

Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Baseline inklusif: c405f9261c3beea2ed4e3695222108c51a7ad636
Snapshot source SHA: 56d1ba6a0ac7e874a3229a494e896336a38e7380
EXE SHA-256: a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569; Entry 1 SHA-256: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a

## Status
DY0: TUNTAS K4 untuk snapshot source; baseline ikut dihitung. Final HEAD dihitung ulang setelah bot publish dan commit laporan akhir.
DY1: TUNTAS K4 untuk tiga branch gate; DX2_PATH_CONDITIONS.tsv ditulis ulang dengan origin setelah JAL/JALR yang diputus pada call boundary.
DY2: SEBAGIAN K4 — census semua store displacement +0x20/+0x21 EXE+Entry1; hanya baris yang basisnya membuktikan slot EA84 dinyatakan tile array. Level source semantik untuk aksi 8/event 3 masih TIDAK TAHU di luar lineage statis yang dilampirkan.
DY3: SEBAGIAN K4 — census langsung menemukan 44 store ke 0x80139EFC; hanya 2 yang memiliki expression slice berisi sll/sllv/mult/addu/subu. File DS3_INDEX_GLOBAL_WRITERS.tsv lama sebenarnya memindai displacement -0x1450 (global 0x8013EBB0), sehingga bukan census EFC. 40 pembaca field +0x4F0/+0x4F4/+0x534 dipisahkan; arti gameplay tetap hipotesis.
DY4: SEBAGIAN K4 — store -fee ke +0x2EE dihitung lewat direct call closure D15A8; tidak menyatakan rumus biaya level tanpa bukti d pada operand.

## DY1 — JAL clobber
0x800EC814 bnez $v0: $v0 berasal langsung dari return JAL 0x8010CDF0; fall-through wajib $v0=0.
0x800EC874 bnez $v0: $v0 berasal langsung dari return JAL 0x8010D0F0; fall-through wajib $v0=0.
0x800EC890 beqz $v0: return JAL 0x800154E0 masuk ke $v1; 0x800EC88C sltiu $v0,$v1,0x10 membentuk $v0. Fall-through wajib $v0!=0, ekuivalen return unsigned $v1<0x10.
Semua origin berhenti pada batas JAL/JALR: v0/v1 dilabel return, a0-a3 dan t0-t9 setelah JAL dilabel TIDAK TAHU. File offset EXE mengikuti 0x800+(PC-0x80010000), Entry 1 0x10BB000+(PC-0x800AD450).

## DY2 — tile+0x20/+0x21
DY2_TILE_PLUS20_PLUS21_WRITERS.tsv memuat 730 operasi store displacement literal +0x20/+0x21 (EXE=294, Entry 1=436). Hanya 50 basisnya terbukti berakar ke slot pointer tile-array 0x8013EA84; sisanya NO_OR_UNRESOLVED. Kolom nibble8_11_operand_origin dan nibble12_15_operand_origin memisahkan parameter/stack dari dynamic load. Nilai load tetap dinamis.
DY2_ACTION8_EVENT3_LEVEL_FINDINGS.tsv merinci sumber field+0x24. Di action8 EC3A8, PC 0x800EC388 membaca tile+0x24, PC 0x800EC364 membaca global 0x8013EAD2, dan PC 0x800EC390 melakukan subu; ini kandidat beda field, bukan bukti beda level d. Pada event3 D9570, PC 0x800DAF2C membaca tile+0x24 berdasarkan indeks dari manager record +0x1F dan nilai disalin ke manager+0x390; tak ada operasi selisih terbukti. Pada EF3CC, basis dan parameter tetap TIDAK TAHU.

## DY3 — global accumulator dan RNG retry
DY3_GLOBAL_80139EFC_WRITERS.tsv hanya memuat store yang effective address statisnya tepat 0x80139EFC. Arithmetic slice memuat PC operand untuk sll/sllv/mult/addu/subu; dependency tile+1A, nibble +0x20, atau field resource +0x14/+0x15 hanya YES jika load pada slice teridentifikasi.
Retry: EC AE8 menetapkan 0x32 (50); EC AEC menyimpan counter global 0x8013EBA8; EC B00/ B08 membaca dan decrement; EC B0C keluar saat -1. Loop memanggil RNG pada EC B14, menghasilkan remainder melalui div/mfhi di ECB24/ECB28, menyimpan kandidat index di ECB38, membaca active index melalui lhu slot 0x8013EA88 di ECB3C, dan mengulang bila sama pada ECB44. Sukses loop mensyaratkan kandidat != active-index; maksimum 50 pemanggilan RNG.
Field manager +0x4F0/+0x4F4/+0x534 dan PC reader/writer berada di DY3_MANAGER_FIELDS_4F0_4F4_534.tsv. Pembaca dengan basis manager terbukti berada di DY3_MANAGER_FIELD_READERS.tsv (total 23); pembaca terkelompok antara FUN_800DC2E0, FUN_800E562C, FUN_800E6470, FUN_800E9220, dan FUN_800C5978. Hipotesis H1/H2 serta falsifier-nya di DY3_HELPER_STATUS_HYPOTHESES.tsv; tidak ada klaim semantik final.

## DY4 — debit aksi 8
Negative fee post terhitung dari instruksi store yang operand slice-nya berisi negu dan pembacaan tile+0x1A, di direct call closure FUN_800D15A8. Jumlah terdeteksi total=1; yang langsung dilabel FUN_800D15A8=1. Store nol untuk clear pending tidak dihitung sebagai post.
DY4_ACTION8_POST_LOOP_AUDIT.tsv menghitung 3 store +0x2EE di direct call closure D15A8; hanya 1 adalah post -fee, dua lainnya clear. DY4_ACTION8_DIRECT_BACKEDGES.tsv menguji branch dari sesudah post yang kembali ke PC <=0x800D46EC; jalur indirect/JALR belum terikat. Jika kosong, tak ada loop langsung yang mengulangi debit di handler statis ini. Ini bukan bukti runtime.
Keempat model formula d=1..4 dalam DY4_FEE_HYPOTHESES_D1_D4.tsv memakai 100 hanya sebagai normalisasi pengamatan pengguna. H2 exact lookup dari empat rasio pengguna ditandai TAUTOLOGI. H3/H4 adalah model debit akumulatif berulang dan bertentangan dengan pengamatan pada nilai d yang dicatat. Formula ROM aktual = TIDAK TAHU.

## Batas
Statis saja; tidak menjalankan emulator/game. Maksimum K4. Nilai runtime, target label untuk field+0x24, arti gameplay +0x4F0/+0x4F4/+0x534, serta rumus biaya ROM = TIDAK TAHU bila tidak terhubung oleh instruction/dataflow proof.
Output text/TSV saja. EXE/DATA.BIN hanya input privat runner; tidak dikomit.
