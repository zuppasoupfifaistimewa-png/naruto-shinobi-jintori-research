# BA_STATE — final checkpoint BA1 → BA2 → BA3
Tanggal: 2 November 2026
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Baseline audit BA: a3dbdd0375b732928e876954e9a662c69785c00c
Laporan final: reports/stage1_economy/BA_FINAL_REPORT_2026-11-02.md

## Status akhir

| Butir | Status | Kepastian | Lingkup yang selesai |
|---|---|---:|---|
| BA1 | SELESAI | K5 untuk H6 yang diuji | Resource 630 (0x276) diidentifikasi dan dipilih selector 0; 22 record diekstrak. |
| BA2 | SELESAI | K4 statis + K5 layout pada H6 | Peta field loader ditutup; 18 field sumber cocok 1.584/1.584; helper nilai FUN_800B770C direkonstruksi. |
| BA3 | SELESAI | K5 pada H6 hybrid | Dua peluncuran independen, frame 180/360, RAM hash identik per frame; selector=0, ID=630; Memory Card tidak berubah. |

## Bukti primer
- BA1 source records: BA1_STAGE1_RESOURCE_630_RECORDS.tsv.
- BA2 runtime map: BA2_TILE_RUNTIME_FIELD_MAP.tsv.
- BA3 validation: BA3_TILE_FIELD_VALIDATION.tsv dan BA3_TILE_FIELD_MATCH_SUMMARY.txt.
- BA3 runtime report: ba3-h6-tile-resource-runtime-run-41418131290/attempt-1/.
- Selector xrefs: aq1-run-41417885033/attempt-1/ba1-selector-callers-main-exe.txt dan ba1-selector-dat80070cd0-xrefs.csv.

## Formula/kondisi yang terbukti
- Loader callsite 0x800B3ED8: resource ID = FUN_800129E4()+0x276.
- FUN_800129E4 membaca DAT_80070CD0; H6 snapshots mencatat byte itu 0, ID=630.
- FUN_8002D00C memakai indeks direktori ×8 byte.
- Source stride 0x1E; runtime tile stride 0x124.
- FUN_800B770C: H=u16(R+0x10+((u16(R+0x20)>>7)&0x1E)); selector +0x0B memilih faktor 1, 12/10, 15/10, 18/10 atau 2.
- u16(tile+0x1A) terbukti menjadi fee pada FUN_800D15A8 action byte 3/8; jika saldo kerja cukup pending delta menerima -fee. Tidak digeneralisasi ke semua action.

## Batas yang tidak boleh dinaikkan menjadi klaim
- H6 bukan target checkpoint murni: target + CONTROL field 6; tidak ada input gameplay atau RAM poke.
- Nama aksi gameplay 3/8 belum diketahui secara spesifik; cakupan semua jenis build/upgrade belum terbukti.
- V dari FUN_800B770C bukan label semantic universal.
- 0x800AD450 tetap kandidat base impor statis, bukan base runtime global yang sudah dibuktikan.
- FUN_80012780 tidak memiliki direct xref pada export yang tersedia; caller tetap TIDAK TAHU.

## Batas repo dan eksperimen
- Tidak ada ISO/BIOS/savestate/dump RAM/video/frame di-commit.
- Bukti runtime yang dipublikasikan hanya teks/TSV turunan.
- BA3 tanpa input gameplay, setter atau RAM poke; input privat sementara dihapus sebelum publikasi.
