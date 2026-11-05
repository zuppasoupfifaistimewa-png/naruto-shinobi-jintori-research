# DS0-DS4 — audit statis raw-byte

Snapshot inklusif=c6204f38495c9be76b18c76a9943f17ca835f2f3; baseline=c6204f38495c9be76b18c76a9943f17ca835f2f3.

## DS0
TUNTAS K4: 1 commit = 1 manusia + 0 bot.
Ledger DN0 sebelumnya berhenti di 087e0e9a91d50c824352fa0ab0d823a7cf471858; baseline terdapat dalam TSV lama: TIDAK.
Rincian commit, author/email, pesan, dan berkas perubahan: DS0_COMMIT_LEDGER.tsv.

## DS1 — pembacaan byte pada FUN_800D15A8
PC 0x800D2450 membaca pointer dari slot global 0x8013EA84; ini alamat slot pointer, bukan nilai base tabel.
PC 0x800D2454-0x800D2468 menghitung base + 292*idx = base + 0x124*idx. Stride statis terverifikasi: 0x124 byte.
PC 0x800D246C melakukan lbu $v1,($v0). Asal indeks $v1 ditelusuri di DS1_INDEX_ORIGIN_TRACE.tsv. Jika register berasal dari argumen/definisi di luar fungsi, nilai numerik indeks = TIDAK TAHU.
Basis efektif tabel adalah nilai pointer yang dibaca dari global 0x8013EA84. Nilai pointer runtime = TIDAK TAHU kecuali writer langsung membuktikan konstanta; scan writer ada di DS1_TABLE_POINTER_GLOBAL_WRITERS.tsv.
Isi byte tabel aktual = TIDAK TAHU: lbu membaca melalui pointer runtime; byte instruksi tidak menyediakan isi memori yang ditunjuk. DS1_PRELOAD_12_RAW.tsv memuat 12 instruksi dan excerpt 48 byte; DS1_TABLE_ADDRESS_TRACE.tsv memuat operasi alamat per PC.

## DS2 — FUN_80102408
Jumlah direct JAL raw ke 0x80102408 di EXE + Entry1: 25; PC/fungsi dan 12 instruksi sebelum call di DS2_FUN_80102408_CALLERS.tsv.
Disassembly CFG reachable: 9 instruksi; return PC terjangkau: 2.
DS2_FUN_80102408_RAW_DISASSEMBLY.tsv memuat PC, file offset, byte mentah, dan instruksi. DS2_FUN_80102408_RETURN_PATHS.tsv memuat setiap return jr $ra; return nonkonstanta, load, call, atau hasil merge diberi TIDAK TAHU dengan alasan per PC.
Edge jump/tail/indirect yang tidak diikuti dicatat di DS2_FUN_80102408_UNRESOLVED_EDGES.tsv; karena itu daftar CFG reachable dibedakan dari klaim seluruh fungsi jika edge belum terurai.

## DS3 — global index 0x8013EBB0
Writer global langsung yang alamat efektifnya dapat dihitung: 144; reader langsung: 149.
Detail PC, fungsi, register sumber, asal nilai atau alasan TIDAK TAHU, 12 instruksi pra-store, dan excerpt 48 byte: DS3_INDEX_GLOBAL_WRITERS.tsv. Reader: DS3_INDEX_GLOBAL_READS.tsv.
FUN_800EC574 membaca halfword 0x8013EBB0 dan menggeser kiri satu bit untuk index 2-byte. Dua direct JAL ke helper yang ditemukan ada pada DS3_FUN_800F3658_PRECALL_CONTEXT.tsv; masing-masing berisi 12 instruksi sebelum call, delay slot, serta instruksi setelah call. Writer via pointer alias/dynamic yang tidak terurai = TIDAK TAHU.

## DS4 — jalur biaya lompatan d>=2
Rantai level-sekarang vs target -> fee -> global 0x80139EFC = TIDAK TAHU. PC 0x800ECA3C-0x800ECA64 menunjukkan pemrosesan halfword/nibble tetapi tidak mengikat level sekarang ke target d. PC 0x800ECAA0 menjalankan mult dan 0x800ECAA4 mflo; hasil disimpan ke manager+0x4F0, bukan terbukti ke global fee. PC 0x800ECBB8 memindahkan nilai global fee yang sudah ada (dinegasikan) ke manager+0x2EE. Fragmen itu belum menghubungkan hasil multiply/target d dengan global 0x80139EFC.
H1 hipotesis: fee = fee_dasar x 2^d untuk d>=2. Falsifier: satu titik kontrol d>=2 dengan fee_dasar terukur yang menyimpang, atau data-flow raw yang membuktikan operand bukan d/hasil tidak menuju fee.
H2 hipotesis: multiplier diambil dari tabel menurut d (kandidat 4, 8, 16 untuk d=2,3,4). Falsifier: data-flow raw membuktikan tidak ada lookup berdasar d, atau lookup/titik kontrol menghasilkan multiplier berbeda.
Ketiga observasi pengguna d=2/3/4 dibandingkan untuk H1 dan H2 di DS4_USER_HYPOTHESIS_POINT_TESTS.tsv. Semua adalah HIPOTESIS pengguna, bukan fakta kode. H1 dan H2 sama-sama cocok 3/3 sehingga tidak terbedakan oleh tiga titik itu. Tidak dilakukan fitting dari kurang dari tiga titik.

## Batas bukti
Statis maksimum K4; tanpa emulator. Nama fungsi di luar target JAL langsung adalah nearest-JAL/prologue heuristic. Global writer scan memakai effective address yang dapat direkonstruksi secara linear; alias tidak langsung dan aliran lintas fungsi yang tidak tertaut = TIDAK TAHU.

## File pipeline yang diubah dalam commit pemicu
- .github/workflows/dq1-dq3-raw-static.yml
- tools/stage1/RunDS0DS4Raw.py
