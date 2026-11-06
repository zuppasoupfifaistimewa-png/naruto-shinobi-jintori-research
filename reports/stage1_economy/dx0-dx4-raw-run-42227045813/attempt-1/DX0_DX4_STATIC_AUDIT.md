# DX0–DX4 — audit statis seluruh EXE dan DATA.BIN Entry 1

BASELINE_INCLUSIVE=c405f9261c3beea2ed4e3695222108c51a7ad636
SNAPSHOT_SOURCE_SHA=56d1ba6a0ac7e874a3229a494e896336a38e7380
DX0_SNAPSHOT_TOTAL=4 HUMAN=3 BOT=1
DX0_EXPECTED_FINAL_AFTER_ONE_BOT_PUBLICATION=5 HUMAN=3 BOT=2
EXE_SHA256=a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569
DATA_BIN_SHA256=69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822
ENTRY1_SHA256=9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a; SIZE=596412; FILE_OFFSET=0x10BB000; BASE=0x800AD450

## Status per DX
DX0: TUNTAS K4 — seluruh commit dihitung inklusif baseline sampai SHA snapshot. Hitungan final HEAD sesudah publikasi bot diverifikasi ulang setelah run.
DX1: TUNTAS K4 untuk census linear full-image jika scan selesai; atribusi fungsi tetap heuristik dan hasil perlu dibaca dengan asal register basis setiap baris.
DX2: SEBAGIAN K4 — CFG intra-fungsi direct edges/delay-slot; indirect JR/JALR ditandai sebagai exit yang tidak terpecahkan. Semantik pemicu tetap dibatasi.
DX3: SEBAGIAN K4 — operator dan origin statis pada root yang diminta; register dinamis yang belum terikat ke selisih level tetap TIDAK TAHU.
DX4: TUNTAS K4 untuk membandingkan tiga prediksi dengan empat angka HIPOTESIS PENGGUNA; formula ROM aktual tetap TIDAK TAHU.

## DX1 — full-scan displacement +0x1A
Hit keseluruhan EXE+Entry 1=172; hit yang diberi label fungsi FUN_800D15A8 oleh function-entry heuristic=7.
DX1_ALL_PLUS1A_ACCESS.tsv menyimpan setiap PC, offset, byte, instruction, fungsi dugaan, register basis, asal slot/global atau konstanta, dan trace register. DX1_D15A8_WINDOW_PLUS1A.tsv memberikan window PC D15A8 untuk spot-check.
DW4_TILE_PLUS1A_ACCESSES.tsv kosong karena analyzer DW4 hanya men-scanning instruksi yang reachable di basic block FUN_80102408. Itu bukan full Entry 1 / EXE scan dan tidak menguji FUN_800D15A8. Tidak ada kontradiksi.
Temuan AZ3/DP3 tentang tile+0x1A bertahan sejauh bukti lama: FUN_800F7ADC menyalin resource+0x14/+0x15 ke tile+0x1A; handler FUN_800D15A8 disebut memakai u16(tile+0x1A) pada action 3/8 dan menyiapkan pending -fee. DX1 menyajikan pemindaian instruksi penuh untuk menilai PC/base langsung; base yang trace-nya tidak mengikat slot EA84 atau alamat 0x8013B818 jangan dianggap tile tanpa bukti.

## DX2 — CFG +0x2EE dan setter Chakra
CFG dimulai pada FUN_800EC574. Setiap branch mempunyai delay-slot node dengan outcome TAKEN/FALLTHROUGH; JAL kembali ke PC+8 selepas delay slot; JR RA berakhir selepas delay slot; JR register selain RA diperlakukan sebagai indirect exit, bukan fall-through.
Reachability tiap target ditampilkan di DX2_TARGET_REACHABILITY.tsv; setiap kondisi branch yang dapat mempengaruhi target ada di DX2_PATH_CONDITIONS.tsv; semua instruksi yang tercapai ada di DX2_FUN_800EC574_CFG.tsv; JR/external exits di DX2_CFG_JR_AND_EXTERNAL_EXITS.tsv.
Full-image scan +0x2EE: reads=3; writes=22. Semua PC dan origin base ada di DX2_ALL_PLUS2EE_ACCESS.tsv. Daftar reader menuju setter ada di DX2_2EE_READERS_TO_SETTER.tsv; direct setter callers dan backward-slice ke argumen a1 ada di DX2_SETTER_8001387C_CALLS.tsv.
Jika route mencapai JAL helper FUN_8001552C di ECAD4 lalu store helper return di ECAE0, global accumulator menjadi 1 karena nilai return helper ditentukan delay slot JR pada EXE. Bila jalur kemudian mencapai lhu ECBA8, negu ECBB0, dan sh ECBB8, nilai yang ditulis adalah 0xFFFF (signed -1). File DX2_HELPER_ONE_TO_PLUS2EE.tsv mencatat reachability setiap PC. Nilai -1 tidak boleh disamakan dengan biaya pembelian petak tanpa relasi tambahan.
Apakah -1 adalah debit Chakra: manager+0x2EE adalah signed pending delta; pembaca +0x2EE harus dibuktikan mengalir ke a1 setter 0x8001387C, dan setter harus menulis saldo participant+0x18. Koneksi yang terdeteksi secara backward slice ditandai YES; fungsi yang hanya sekadar berada di jalur yang sama ditandai NOT_PROVEN. Jika jalur setter tidak terikat, tujuan debit khusus -1 = TIDAK TAHU.
H1: lane +0x2EE adalah delta saldo Chakra. Falsifier: reader tidak mencapai a1 setter atau setter menulis field selain participant+0x18. H2: lane +0x2EE adalah delta saldo generik (bisa debit/kredit/transfer). Falsifier: semua writer dan caller terbukti hanya dipakai satu kelas transaksi. Tujuan gameplay nilai -1 tetap TIDAK TAHU sampai producer/caller diketahui.

## DX3 — level difference, nibble dan shift
DX3_SEED_REACHABILITY.tsv menguji keterjangkauan site 0x800EC3A8 dari root FUN_800EB434 dan root FUN_800EF3CC. DX3_OPERATION_CENSUS.tsv mencatat sll/sllv/srl/srlv/sra/srav, mult/multu/mflo, slti/sltiu immediate 2, sub/subu, OR/ORI, dan origin operand.
DX3_TILE_PLUS20_READ_WRITE.tsv berisi semua load/store displacement +0x20 dalam CFG tiap root. DX3_LEVEL_NIBBLE_COMPARISONS.tsv mencatat branch yang register operand-nya trace ke lhu +0x20. DX3_LEVEL_NIBBLE_OR_SOURCES.tsv mengurai OR/ORI dalam nilai yang disimpan ke +0x20 dan asal sll/sllv bila ada. DX3_ONE_SHIFT_PATTERNS.tsv khusus kasus operand literal 1 yang di-shift.
Pengurangan yang diuji untuk selisih level ada di DX3_LEVEL_DIFFERENCE_CANDIDATES.tsv. Jika kedua operand tidak trace ke pembacaan tile+0x20, itu bukan bukti delta level. Tidak adanya pola 1<<d atau tidak adanya subtract yang terikat pada nibble tidak meniadakan kemungkinan formula berada di pemanggil lain atau indirect path.

## DX4 — model dan 4 pengamatan pengguna
Observasi d=1..4: 100, 400, 800, 1600 dengan fee_dasar simbolik. Angka 100 dipakai hanya sebagai normalisasi aritmetika sesuai asumsi pengguna; bukan konstanta ROM.
H1_PURE_POWER_2: bertentangan pada d=1; faktor d1..d4=2,4,8,16.
H2_SPECIAL_PER_LEVEL_LOOKUP: bertentangan pada d=tidak ada; faktor d1..d4=1,4,8,16.
H3_LEVEL_TABLE_DOUBLING_FROM_D1: bertentangan pada d=2,3,4; faktor d1..d4=1,2,4,8.
Falsifier per model mengarahkan pencarian ke operand selisih d, special branch d=1 (misalnya slti[u] immediate 2), coefficient/lookup, atau instruksi shift di site 0x800EC3A8 / 0x800EF3CC. Model yang cocok dengan data pengguna tetap belum terbukti sebagai kode ROM.

## Validitas dan batas
Input EXE/DATA.BIN/Entry 1 dicocokkan dengan ukuran dan SHA-256 yang telah ditetapkan. Tidak ada emulator/game dijalankan. Tidak ada ISO, EXE, DATA.BIN, BIOS, savestate, dump, video, frame, atau biner yang dikomit. Output hanya MD/TSV/TXT; tiap baris machine raw memuat 4 byte instruksi.
Linear full-image scan dapat mendekode byte data non-code sebagai instruction; hasil per PC harus dipilah menurut function label dan base_origin. CFG rooted dari fungsi mengurangi risiko tersebut untuk analisis reachability. Maksimum confidence K4.
