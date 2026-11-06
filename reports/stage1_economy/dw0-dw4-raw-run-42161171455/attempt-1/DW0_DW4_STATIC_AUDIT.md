# DW0–DW4 — audit statis raw DATA.BIN / Entry 1

BASELINE_INCLUSIVE=2d334348b55dd672b3a2b0e428795c8ce817135b
SNAPSHOT_SOURCE_SHA=7c4abdc5166ee69b79e4a2e0f9da8adbd89a2bb9
HEAD_AT_ANALYSIS=7c4abdc5166ee69b79e4a2e0f9da8adbd89a2bb9
DW0_TOTAL_INCLUSIVE=4 HUMAN=4 BOT=0

## DW0 — commit ledger
Ledger bersifat inklusif dari baseline sampai snapshot; commit publikasi Actions terjadi sesudah snapshot dan tidak masuk hitungan.

## DW1 — 12 resource, tile byte +0x00
Selector inventory yang diverifikasi: 12 resource; jumlah record dari 1-byte header + N record x 0x1E = 415.
Total byte +0x00 bernilai 1: 29; bernilai 5: 0.
Histogram byte ada di DW1_BYTE00_HISTOGRAM.tsv; ringkasan setiap resource dan initial tile+0x20 ada di DW1_RESOURCE_SUMMARY.tsv.
Record tanpa byte +0x00 dan record terpotong dihitung eksplisit; header byte dilaporkan tetapi tidak diasumsikan sebagai N.
FUN_800F7ADC menulis initializer tile+0x20 = 0xF020; sehingga nibble awal bits12–15=0xF dan bits8–11=0 untuk setiap tile yang diinisialisasi. Ini bukan field sumber resource.
Arti gameplay 1 dan 5 tidak ditetapkan dari histogram. Kode yang terverifikasi: value 1 mengambil cabang bookkeeping daftar tile pada loader; value 5 adalah filter pertama pada loop ekonomi. Label jenis/status gameplay tetap TIDAK TAHU.

## DW2 — global 0x80139EFC dan helper
Loop 0x800ECA2C/0x800ECA34 membaca tile+0x00; bila byte=5 dan nibble bits12–15 tile+0x20 sama dengan t0 dinamis, loop menambahkan 1+nibble bits8–11 ke 0x80139EFC.
PC 0x800ECAE0 menulis v0 ke global yang sama setelah JAL 0x8001552C pada 0x800ECAD4; a0 sebelumnya dimuat dari stack+0x18 di 0x800ECAD0. Nilai return helper akan dijelaskan dari DW2_FUN_8001552C_RAW.tsv/RETURN.tsv.
Debit membaca halfword global di 0x800ECBA8, menegasikan di 0x800ECBB0, lalu menyimpan ke manager+0x2EE di delay slot 0x800ECBB8. Jangan menyamakan store ini dengan global write.
Hubungan accumulator-loop ke debit hanya sah jika jalur kontrol tidak melewati/menimpa write 0x800ECAE0; external edges dan raw function helper terlampir. Nilai runtime hasil load tetap TIDAK TAHU.

## DW3 — jr 0x800F5CE0
Raw instructions 0x800F5C98..0x800F5CE0 beserta bytes ada di DW3_JR_800F5CE0_RAW.tsv. Selector dibaca pada 0x800F5CB8 melalui base pointer yang dimuat dari slot global 0x8013EA84; formula index/effective address dan writer candidates dilampirkan.
DW3_OUTER_JR_800F3788_TABLE_64.tsv berisi semua 64 slot tabel luar; DW3_OUTER_TABLE_DISPATCHER_TARGETS.tsv hanya slot yang targetnya berada pada rentang dispatcher yang diuji. Pointer slot global dan writer alias dibedakan.

## DW4 — fee tile+0x1A
Three writer call-site contexts, direct calls to FUN_80102408, and the complete sequential helper decode are attached. A +0x1A store is evidence of an offset operation, not by itself proof that the base is the tile object; the output preserves that distinction.
fee_dasar remains a symbolic unknown unless a static path proves its source. H1/H2prime/H3 are hypotheses, not ROM constants or fitted values. For d>=2, all three predictions coincide; a value that differs from fee_dasar*2^d falsifies the shared rule. d=1 separates H1 from H2prime/H3.

## Validity
Input identity checks passed for EXE, DATA.BIN and DATA.BIN Entry 1. No emulator/game was run. No BIOS, savestate, raw DATA.BIN, ISO, EXE, screenshots, video, or frames are included in the committed outputs; the private input is temporary and cleaned by the workflow.
All findings are static (maximum K4). Dynamic values, unproven aliases, and gameplay labels remain TIDAK TAHU.
