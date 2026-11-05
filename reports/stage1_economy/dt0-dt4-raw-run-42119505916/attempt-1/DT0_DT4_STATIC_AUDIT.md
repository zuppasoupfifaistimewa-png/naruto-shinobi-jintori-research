# DU0–DU5 — laporan koreksi audit statis Naruto Jintori

Baseline inklusif DU0: 2f72b3a2807f1022048083d6d07ad527adaa7cf7
Snapshot DU0 (commit sumber run kedua): 524d2421e72ce8707c37d9564f4e95eb5cc9fcb9
HEAD saat publikasi hasil run kedua: 867d82e72d8385dbc36570f4d9d052461b7e7520
DU0: TOTAL=4, MANUSIA=3, BOT=1, K4. HEAD akhir berbeda dari snapshot; commit publikasi run kedua berada sesudah snapshot dan tidak masuk hitungan.

## DU1 — workflow dan Actions
TUNTAS, K4. Tiga interpolasi aktif dan tidak ada token literal \$\{\{ tersisa. Izin actions:read hanya untuk membaca job id pada summary; contents:write tetap untuk output teks.
Run 42119041813, job raw-static-dt0-dt4 / 127566269838, source SHA dd91e9df41ccc05f48917abfc91d44366bde458b, exit 0.
Run 42119505916, job raw-static-dt0-dt4 / 127567860789, source SHA 524d2421e72ce8707c37d9564f4e95eb5cc9fcb9, exit 0.
Keduanya memverifikasi sumber, membersihkan input biner sementara, dan hanya mengomit teks. Tidak ada emulator.

## DU2 — FUN_800EC574
TUNTAS, K4 untuk bytes/data-flow statis. DT1_LOOP_RAW.tsv berisi 31 instruksi termasuk 0x800ECA68/6C; offset mengikuti 0x10BB000+(PC-0x800AD450), sehingga 0x800ECA0C=0x10FA5BC.
Sebelum loop: t0 dari lhu -0x1578(base 0x80140000), alamat 0x8013EA88; t1 dari lw -0x157c, alamat slot 0x8013EA84; t2=5; a2=0x80140000 dari lui di 0x800ECA00; a3 dari lw -0x1538, alamat 0x8013EAC8. Nilai runtime field yang berasal dari load tetap TIDAK TAHU. Backward slice dua callsite tersimpan di DT1_CALLER_REGISTER_ORIGINS.tsv; untuk 0x800F3830 tidak ada definisi lokal yang dapat dipastikan dari awal fungsi.
Filter tile: byte tile+0x00 harus sama dengan 5; nibble bits12–15 dari halfword tile+0x20 harus sama dengan t0. Bits8–11 diekstrak dan fee global bertambah 1+nibble untuk tiap tile yang lolos. Makna gameplay spesifik dari byte 5 / nibble level tetap TIDAK TAHU.
Operand mult 0x800ECAA0: a0 berasal dari global index 0x8013EBB0; v0 berasal dari global fee 0x80139EFC; hasil ditulis ke manager+0x4F0. Label ekonomi/gameplay hasil perkalian tetap hipotesis.
CLEAR: tujuh store sumber $zero cocok dengan census DS. 0x800EC9CC adalah CLEAR di fungsi yang sama, tepat sebelum loop. Nilai awal nol dari load RAM tidak dihitung CLEAR. Penulis nonzero termasuk 0x800ECA64 (update loop) dan 0x800ECAE0 (di luar loop); nilai ECAE0 TIDAK TAHU karena berasal dari load mutable.
Hipotesis global: (1) akumulator biaya lintasan/move yang di-reset sebelum scan dan menjumlahkan 1+nibble untuk tile cocok; falsifier: bukti pemanggil menggunakannya sebagai skor board umum atau tidak mereset per aksi. (2) accumulator biaya/score tile kategori 5 untuk operasi ekonomi/territory; falsifier: bukti konsumen langsung membayar movement path dan perubahan global terbatas pada rute. Keduanya bukan fakta game terkonfirmasi.

## DU3 — return dan tabel
TUNTAS, K4. Delay slot 0x80102434 = FF FF 02 24, addiu v0,zero,-1; return jalur jr 0x80102430 adalah 0xFFFFFFFF. Tabel offset 0x11493C8, base 0x8013B818, excerpt 64 byte seluruhnya 00.
JR v0 di 0x800F5CE0 memakai tabel base 0x800AEB78, file offset 0x10BC728; sembilan pointer (36 byte) dalam DT3_JR_V0_TABLE.txt.

## DU4 — dispatch menuju dua JAL
TUNTAS, K4. Call 0x800F3830 berasal dari jr v0 0x800F3788, tabel 0x800AEA20. Slot ke-44 pada 0x800AEAD0 berisi pointer 0x800F3830; selector byte dari 0x800F3760 bernilai 44 dan lolos pemeriksaan <64 di 0x800F3768/6C.
Call 0x800F5D08 berasal dari jr v0 0x800F5CE0, tabel 0x800AEB78. Slot ke-2 pada 0x800AEB80 berisi 0x800F5D08; selector dari 0x800F5CB8 bernilai 2 dan lolos pemeriksaan <9 di 0x800F5CC0/C4. Ini pemetaan statis selector->handler, bukan klaim label nama event.

## DU5 — fee hypotheses
TUNTAS sebagai uji model, K1 (hipotesis; bukan formula ROM). fee_dasar=100 adalah input hipotesis. Pada d=1..4: H1 memprediksi 200/400/800/1600 (3/4 cocok); H2 lookup independen {1:1,2:3,3:6,4:10} memprediksi 100/300/600/1000 (1/4 cocok); H3 aturan pengguna memprediksi 100/400/800/1600 (4/4 cocok). Prediksi untuk basis B dan falsifier tiap model berada di DU5_MODEL_FALSIFIERS.txt. H2 sengaja alternatif terpisah, bukan hasil ROM atau salinan observasi.
