# DV0–DV4 — audit statis raw-byte Naruto Jintori

BASELINE_INCLUSIVE=7040cd08a79107a45de6571e875de4fadb165c8a
SNAPSHOT_SOURCE_SHA=fed79376ccd639ffaad6f30ddf6feb080e6a8b3b
DV0_TOTAL_INCLUSIVE=3 HUMAN=3 BOT=0
HEAD_AT_ANALYSIS=SNAPSHOT_SOURCE_SHA; publication bot commit 407612565c23300cdbb9a766e083ce044e4cffbe dibuat setelah snapshot dan tidak masuk hitungan DV0.

## DV1 — FUN_800EC574

Raw block PC 0x800EC9CC..0x800ECBD0 berisi 130 word instruksi; seluruh byte dan file offset ada di DV1_FUN_800EC574_BLOCK_RAW.tsv. Rumus offset: 0x10BB000 + (PC - 0x800AD450).

Loop 0x800ECA0C..0x800ECA84 membentuk indeks tile * 0x124. Tile lolos filter pertama jika byte tile+0x00 == 5; filter kedua membandingkan nibble bits12–15 dari halfword tile+0x20 dengan register t0 yang nilainya dinamis. Untuk tile yang lolos, nibble bits8–11 ditambah 1 dan diakumulasikan ke global 0x80139EFC. Artinya instruksi mendukung penjumlahan 1+nibble per tile yang lolos; nilai akumulator aktual bergantung runtime dan TIDAK TAHU dari statis.

Urutan debit yang benar:
- 0x800ECBA8: lhu v0,-0x6104(v0), membaca global 0x80139EFC. Nilai hasil load dinamis, TIDAK TAHU.
- 0x800ECBB0: negu v0,v0.
- 0x800ECBB4: j 0x800EC928.
- 0x800ECBB8 (delay slot): sh v0,0x2ee(v1), menyimpan halfword hasil negasi ke lane manager relatif +0x2EE.
Jadi bukan 0x800ECBB8 yang melakukan load atau negu; PC tersebut adalah store delay-slot.

DV1_MANAGER_PLUS4F0_READERS.tsv menemukan 13 kecocokan displacement +0x4F0. Tujuh kecocokan 0x800ADA8C..0x800ADABC memakai base $zero dan bukan bukti baca field manager. Enam lainnya adalah load melalui base register dinamis:
- 0x800DD464 FUN_800DC2E0: nilai dipakai untuk bgez.
- 0x800E5688 FUN_800E562C: nilai dipakai untuk bgez dan negu.
- 0x800E56AC FUN_800E562C: nilai dipakai untuk bgez dan negu.
- 0x80120A08 FUN_801205B4: nilai dipakai tes bit 0x2.
- 0x80120A30 FUN_801205B4: nilai dipakai tes bit 0x4.
- 0x80122014 FUN_80121D40: nilai digabung dengan OR.
Base untuk keenam load itu dinamis dan identitasnya terhadap objek manager yang menerima hasil mult di 0x800ECAA0 belum terbukti. Karena itu semuanya kandidat pembaca +0x4F0, bukan enam pembaca manager yang terkonfirmasi. Nilai operand mult dan semua hasil load dinamis tetap TIDAK TAHU.

## DV2 — CFG dan selector

DV2_REPRESENTATIVE_PATHS.tsv memberi satu jalur CFG representatif dari awal FUN_800F3658 ke jr 0x800F3788. Cabang di jalur dan kondisinya:
- 0x800F3688 beqz v0 -> ke 0x800F36A4 hanya bila v0==0.
- 0x800F36B4 bnez v0 -> ke 0x800F36FC bila v0!=0.
- 0x800F36C8 bne v1,v0 -> ke 0x800F36FC bila v1!=v0.
- 0x800F36DC beqz v0 -> ke 0x800F36F8 bila v0==0.
- 0x800F370C bnez v0 -> fallback 0x800F605C bila v0!=0.
- 0x800F371C beqz v0 -> ke 0x800F3734 bila v0==0.
- 0x800F372C beqz v0 -> fallback 0x800F605C bila v0==0.
- 0x800F3748 beq v1,v0 -> ke 0x800F3754 bila byte +0x2E9 sama dengan 8.
- 0x800F3768 sltiu v0,v1,0x40 dan 0x800F376C beqz v0 -> fallback bila selector >=64. Agar tabel memilih handler 0x800F3830, selector harus 44; 44 < 64 lolos.
Tabel 0x800AEA20 + 44*4 beralamat 0x800AEAD0, bytes 30 38 0F 80 -> pointer 0x800F3830. Nilai runtime byte manager+0x2E9 tidak diketahui dari statis.

Untuk jr 0x800F5CE0, tabel pada 0x800AEB78 memakai selector yang dibaca pada 0x800F5CB8. Pemeriksaan batas 0x800F5CC0 membatasi selector <9; jika selector 2, slot 0x800AEB80 berisi bytes 08 5D 0F 80 -> handler 0x800F5D08. Ini membuktikan pemetaan tabel selector 2 ke handler, tetapi CFG konservatif intrafungsi tidak menemukan jalur dari awal FUN_800F3658 ke jr 0x800F5CE0 karena alur melewati indirect-jump lain. Keterjangkauan dari entry fungsi dan nilai selector runtime tetap TIDAK TAHU.

Penulis selector:
- 253 store kandidat dengan displacement +0x2E9 ditemukan di Entry 1; tidak ada penulis nilai 44 yang dapat dibuktikan ke objek manager yang sama.
- Dua store statis yang terbaca konstan pada alamat kandidat +0x2E9 berasal dari $zero (nilai 0) pada 0x800B2460 FUN_800B1E88 dan 0x800B2E84 FUN_800B2A58; bukan 44.
- Ada 28 store melalui $a0 di rentang FUN_800F3658. Ini belum membuktikan penulisan ke alamat slot selector sumber yang dibaca di 0x800F5CB8. Store kandidat 0x800F5868 menulis konstanta 2 ke +0x23($a0), tetapi kesamaan alamat dengan slot selector yang dibaca juga TIDAK TAHU.
Jadi penulis aktual untuk selector 44 dan byte selector 2 tetap TIDAK TAHU.

## DV3 — field record dan tile

Pemetaan loader statis FUN_800F7ADC:
- record sumber +0x00 -> tile +0x00 (u8). 0x800F7BB8 membaca byte dari cursor sumber ($s1); 0x800F7BC0 menulis byte yang sama ke tile pointer ($a0). Cursor awal dibentuk di 0x800F7B38 (s1=s4+1), melewati byte count/header; tiap record bertambah 0x1E.
- record +0x05 dilewati; record +0x06 disalin ke tile +0x05.
- Tile +0x20 tidak disalin dari record. 0x800F7E64 ori v0,zero,0xf020; 0x800F7E68 sh v0,0x20(a1). Maka nilai awal word adalah 0xF020: bits12–15 = 0xF dan bits8–11 = 0. Tidak ada field sumber record untuk kedua nibble ini pada tahap loader.
- Field mapping lengkap yang sudah diinventarisasi ada di BA2_TILE_RUNTIME_FIELD_MAP.tsv; peta khusus PC+alasan untuk pertanyaan ini ada di DV3_CONFIRMED_TILE_FIELD_MAP.tsv.

Makna gameplay byte 5 atau 1 tidak terbukti:
- byte 5 dipakai sebagai syarat filter di loop ekonomi pada 0x800ECA34.
- byte 1 dikenali loader di 0x800F7BD8; cabang itu menambahkan indeks tile ke daftar yang ditopang counter/list di sekitar 0x800F7BE8..0x800F7C0C.
Fungsi internal ini diketahui, tetapi arti 5 dan 1 sebagai jenis tile/status gameplay adalah TIDAK TAHU.

Histogram 12 resource x 415 record belum dapat disusun. DV3_DATA_BIN_DIRECTORY_CANDIDATES.tsv tidak menemukan extent tepat 12,450 byte (415*0x1E). CI1_SELECTOR_RESOURCE_INVENTORY_2026-11-04.tsv memang memuat 12 resource-selector, tetapi hanya ID 630 dan 638 yang berformat 1+22x0x1E (661 byte); sepuluh resource lain tidak cocok format itu. Dengan demikian identitas dataset 12x415 belum terverifikasi dan DV3_415x30_RESOURCE_BYTE_HISTOGRAMS.tsv hanya berisi header. Tidak ada histogram yang dikarang.

## DV4 — hipotesis fee

H2' lookup {1:1,2:4,3:8,4:16,5:32} identik secara aljabar dengan H3 (d=1: fee_dasar; d>=2: fee_dasar*2^d). Satu-satunya titik yang membedakan H1 dari pasangan H2'/H3 adalah d=1, untuk fee_dasar=100 maupun 50. Tidak ada titik d=1..5 yang membedakan H2' dari H3. fee_dasar tetap parameter hipotesis, bukan konstanta ROM; tidak ada fitting.

## Validitas run dan batasan

Run 42125095938: STATUS PASS, job raw-static-dt0-dt4 (job ID 127587123057), source SHA fed79376ccd639ffaad6f30ddf6feb080e6a8b3b, exit code 0. Input mentah lolos verifikasi dan cleanup privat PASS; tidak ada emulator/game, BIOS, atau savestate; tidak ada biner yang dikomit; output teks saja.

Catatan metadata: ACTIONS_RUN_SUMMARY.txt mempertahankan ANALYSIS_BASELINE_SHA=2f72b3a... dari template workflow lama. Untuk pekerjaan DV ini baseline sebenarnya yang digunakan oleh analyzer dan DV0_COMMIT_LEDGER.tsv adalah 7040cd08a79107a45de6571e875de4fadb165c8a; snapshot sumbernya fed79376ccd639ffaad6f30ddf6feb080e6a8b3b. Jangan memakai field baseline generik pada summary sebagai basis ledger DV0.

Semua kesimpulan di atas statis, maksimum K4. Nilai register hasil load data, selector runtime, penulis yang alamat dasarnya belum dibuktikan, dan label gameplay yang tidak punya jalur bukti eksplisit ditandai TIDAK TAHU.
