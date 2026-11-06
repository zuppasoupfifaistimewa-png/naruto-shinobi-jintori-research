# DZ0-DZ4 — addendum statis biaya/level petak

Baseline inklusif: c405f9261c3beea2ed4e3695222108c51a7ad636
Snapshot source SHA: 56d1ba6a0ac7e874a3229a494e896336a38e7380
DZ0: TUNTAS K4 untuk snapshot; ledger DX0_COMMIT_LEDGER.tsv dan DX0_COUNTS.tsv menghitung dari baseline inklusif. Snapshot dan HEAD pascapublikasi dibedakan di ringkasan run/repo.
DZ1: TUNTAS K4 jika file DZ1_SELF_CHECK_SUMMARY.txt PASS; validasi tiap pasangan PC/file_offset TSV serta decode byte 4-byte terhadap instruction. Script syntax harus lolos py_compile sebelum workflow.
DZ2: SEBAGIAN K4. Window fee lengkap ada di DZ2_D15A8_FEE_WINDOW_800D46B0_800D4840.tsv; census semua reader/writer EA 0x8013EB0C ada di DZ2_GLOBAL_8013EB0C_READ_WRITE_CENSUS.tsv. Old nibble 8-11/4-7 terbukti dibanding/dikurangkan dengan EB0C: TIDAK TAHU — tidak ada joint def-chain proof dalam FUN_800D15A8. Formula biaya ROM dan level d tidak diasumsikan.
DZ3: SEBAGIAN K4. Branch/jump lokal ke <=0x800D46EC: 270. Back-edge pasca-post ke fee load: 0. Table JR F5CE0 diperiksa 9 target; unresolved JR/JALR tetap TIDAK TAHU. Store +0x2EE terinventarisasi di DZ3_ACTION8_ALL_PLUS2EE_STORE_PATHS.tsv; ECBB8 status=YES_DIRECT_OR_KNOWN_TABLE.
DZ4: SEBAGIAN K4. Semua lh/lhu/sh displacement +0x24 ada di DZ4_TILE_PLUS24_ALL_LH_LHU_SH_CENSUS.tsv; tile-array base terbukti pada 160 baris. Dua/tiga fan-out spesifik dicatat di DZ4_TILE_PLUS24_VALUE_REFERENCE_FANOUT.tsv; makna owner/level/lainnya tetap hipotesis terfalsifikasi dalam DZ4_TILE_PLUS24_SEMANTIC_HYPOTHESES.tsv.
ECAEC: sw -0x1458 setelah lui 0x8014 => global 0x8013EBA8; bukan manager+0x2A8, bukan 0x8013EB0C, bukan 0x8013EBB0.
Fee dasar tetap simbolik. Angka 100/400/800/1600 adalah hipotesis pengguna, bukan konstanta ROM. Tidak dilakukan fit berbasis kurang dari 3 titik. Statis maksimum K4; tanpa runtime/K5.
Tidak ada emulator/game/BIOS/savestate dijalankan. Tidak ada biner/video/frame dikomit.
