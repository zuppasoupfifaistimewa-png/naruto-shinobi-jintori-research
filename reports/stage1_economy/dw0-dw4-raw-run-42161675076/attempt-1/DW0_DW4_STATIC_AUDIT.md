# DW0–DW4 — audit statis raw DATA.BIN / Entry 1

BASELINE_INCLUSIVE=2d334348b55dd672b3a2b0e428795c8ce817135b
SNAPSHOT_SOURCE_SHA=26bcab51a7e93b10f7e8e902f040eb223df07396
HEAD_AT_ANALYSIS=26bcab51a7e93b10f7e8e902f040eb223df07396
DW0_TOTAL_INCLUSIVE=6 HUMAN=5 BOT=1

## DW0 — commit ledger
Ledger bersifat inklusif dari baseline sampai snapshot; commit publikasi Actions terjadi sesudah snapshot dan tidak masuk hitungan.

## DW1 — 12 resource, tile byte +0x00
Selector inventory yang diverifikasi: 12 resource; jumlah record dari 1-byte header + N record x 0x1E = 415.
Total byte +0x00 bernilai 1: 29; bernilai 5: 0.
Histogram byte ada di DW1_BYTE00_HISTOGRAM.tsv; ringkasan setiap resource dan initial tile+0x20 ada di DW1_RESOURCE_SUMMARY.tsv.
Record tanpa byte +0x00 dan record terpotong dihitung eksplisit; header byte dilaporkan tetapi tidak diasumsikan sebagai N.
FUN_800F7ADC menulis initializer tile+0x20 = 0xF020; sehingga nibble awal bits12–15=0xF dan bits8–11=0 untuk setiap tile yang diinisialisasi. Ini bukan field sumber resource.
Arti gameplay 1 dan 5 tidak ditetapkan dari histogram. Kode yang terverifikasi: value 1 mengambil cabang bookkeeping daftar tile pada loader; value 5 adalah filter pertama pada loop ekonomi. Label jenis/status gameplay tetap TIDAK TAHU.

## Status per level
DW0: TUNTAS K4 — commit ledger inklusif dihitung dari git history pada snapshot; commit bot publikasi dipisahkan.
DW1: TUNTAS K4 untuk histogram/format resource dan initializer tile+0x20; arti gameplay nilai byte tetap TIDAK TAHU.
DW2: SEBAGIAN K4 — helper dan jalur normal statis terbukti; indirect entry/semantik gameplay lane masih perlu batasan tambahan.
DW3: SEBAGIAN K4 — formula lookup dan tabel terbukti; penulisan tile+0x1F/+0x00 dipetakan sebagai kandidat berdasarkan def-chain pointer, bukan alias runtime.
DW4: SEBAGIAN K4 — seluruh direct CFG helper dipetakan; fee_dasar/label semantik tile dan nilai dinamis yang tidak tersimpan statis tetap TIDAK TAHU.

## DW2 — global 0x80139EFC dan helper
Loop 0x800ECA2C/0x800ECA34 membaca tile+0x00; bila byte=5 dan nibble bits12–15 tile+0x20 sama dengan t0 dinamis, loop menambahkan 1+nibble bits8–11 ke 0x80139EFC.
FUN_8001552C pada 0x8001552C menambahkan a0+a1 sebagai alamat, memuat u16, menambah 1, lalu menyimpan u16 itu. Tetapi nilai kembalian bukan u16 tersebut: delay slot JR RA di 0x80015544 mengatur v0=1 sebelum return.
Karena 0x800ECAD4 memanggil helper itu dan 0x800ECAE0 langsung menyimpan v0, jalur normal meng-overwrite akumulator loop di 0x80139EFC menjadi 1. 0x800ECBA8 kemudian membaca u16 global itu, 0x800ECBB0 menegasikan, dan delay slot 0x800ECBB8 menyimpan halfword hasilnya ke manager+0x2EE. Isi/arti gameplay lane +0x2EE tetap TIDAK TAHU.
Scan branch/J/JAL langsung ke label 0x800ECAD0, 0x800ECB4C, 0x800ECB88, 0x800ECBBC dari luar blok menghasilkan nol referensi langsung; target tidak langsung/JR yang tidak bisa ditetapkan dari byte statis tetap TIDAK TAHU. Karena itu kesimpulan nilai 1 berlaku pada jalur normal yang melewati JAL helper dan store 0x800ECAE0.

## DW3 — jr 0x800F5CE0
0x800F5C74 memuat base pointer slot global 0x8013EA74; indeks record awal berasal dari global 0x8013EA88. Indeks ini dikali stride record 0x124, lalu 0x800F5C94 membaca byte current-record+0x1F.
Byte +0x1F tersebut kemudian dikali 0x124. Base pointer kedua dimuat dari slot 0x8013EA84; 0x800F5CB4 menambahkan base, dan 0x800F5CB8 membaca byte pada selected-record+0x00. Byte +0x00 itulah selector JR; 0x800F5CC0 mensyaratkan selector <9, sedangkan >=9 jatuh ke 0x800F5D88.
DW3_INDEXED_TILE_BYTE_LOOKUP.tsv merinci seluruh instruksi dan skala. DW3_EA74_TILE_PLUS1F_ACCESS.tsv memuat akses kandidat ke tile+0x1F; DW3_EA84_TILE_BYTE00_READERS.tsv/WRITERS.tsv memuat reader/writer kandidat byte +0x00. DW3_TILE_ARRAY_SLOT_XREFS.tsv mencakup slot EA74, EA84 dan EA88.
Slot global 0x8013EA84 sendiri ditulis pada dua PC statis yang terdeteksi (lihat DW3_TILE_ARRAY_SLOT_XREFS.tsv). Tabel 64-entri luar di 0x800AEA20 mengarah ke area dispatcher pada selector 9, 10, 12, 13, 14 dan 51.

## DW4 — FUN_80102408 dan tile+0x1A
DW4_FUN_80102408_RAW.tsv kini memuat seluruh basic block yang dicapai dari entry 0x80102408 melalui kedua sisi branch, bukan berhenti pada JR RA pertama. DW4_FUN_80102408_MEMORY_ACCESSES.tsv memetakan semua akses memori yang terlihat; DW4_TILE_PLUS1A_ACCESSES.tsv mengisolasi displacement +0x1A.
Ketiga writer global pada 0x800D09C8, 0x800DFA28 dan 0x800EA1D4 masing-masing didahului JAL langsung ke 0x80102408 (lihat DW4_CALLS_TO_FUN_80102408.tsv dan DW4_THREE_WRITER_CONTEXT.tsv). Base/argumen dinamis tetap TIDAK TAHU kecuali register origin terbukti.
fee_dasar tetap simbolik/TIDAK TAHU kecuali sumbernya terbukti. H1/H2prime/H3 adalah hipotesis, bukan konstanta ROM. Untuk d>=2 ketiganya ekuivalen; satu nilai ukur pada d>=2 yang tidak sama dengan fee_dasar*2^d memfalsifikasi aturan bersama. d=1 memisahkan H1 dari H2prime/H3.

## Validity
Input identity checks passed for EXE, DATA.BIN and DATA.BIN Entry 1. No emulator/game was run. No BIOS, savestate, raw DATA.BIN, ISO, EXE, screenshots, video, or frames are included in the committed outputs; the private input is temporary and cleaned by the workflow.
All findings are static (maximum K4). Dynamic values, unproven aliases, and gameplay labels remain TIDAK TAHU.
