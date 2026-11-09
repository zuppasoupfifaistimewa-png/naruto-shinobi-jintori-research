# NA0-NA5 static audit — SLPS-03553

Baseline inklusif: 7bcfef67d0adf89b7ab0cb20e040790f15766017
Source SHA: 0b23ad24c77f31591609adceca365aa3aca944e2
EXE SHA-256: a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569
Entry 1 SHA-256: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a
EMULATOR_LAUNCHES=0.

## Status per butir
- NA0: TUNTAS K4 — py_compile 71/71; .py aktual=70; sumber .txt dihitung=1; validasi bytes/offset/decode=15850/15850; excerpt maksimum=64 B; pelanggaran=0.
- NA1: SEBAGIAN K3 — scene record=39; enam base PC dianalisis; asal argumen/wallet/index dan CFG pemanggilan belum seluruhnya tertutup.
- NA2: SEBAGIAN K3 — sw 0x118($gp)=2; assignment $gp=2; writer EA88/39EFC=66; lw M=2084; store M-turunan=964; writer M+0x530=4; x=d/ID dan batas 52 TIDAK TAHU.
- NA3: SEBAGIAN K3 — edge Ghidra ke B24C8=0; edge raw terdecode=0; static JALR Ghidra BE5D8=0; raw JALR target match=0; computed caller tetap TIDAK TAHU.
- NA4: TUNTAS K4 — hanya statis; emulator/game 0; tanpa BIOS/savestate/RAM dump/video; tanpa biner di commit.
- NA5: BELUM K1 — x=d belum terbukti; biaya lompat level d>=2 TIDAK TAHU; tanpa angka asumsi atau fitting.

## Batas bukti
Scene table anchor=0x800558A4; stride=0x1C; jumlah record=39.
NA2 M-use census is bounded and linear; exact M+0x530 writer rows and the D49A4-D49D8 primary read path are separately tabulated. This still does not close every alias/CFG path to the matrix-cell writers.
V0 continuity rows only pass when every intervening instruction exists, no v0 redef, no call, and no branch entry is seen. Otherwise TIDAK TAHU.
NA3 compares Ghidra code with a full raw aligned-instruction sweep. Raw matches outside recognized code remain unverified; computed/dynamic targets remain TIDAK TAHU.
## Validasi NA0
PY_COMPILE=71/71; PY_FILES=70; TXT_SOURCE_FILES=1.
FILE_OFFSET_RAW_DECODE_CHECKS=15850; DECODED_INSTRUCTIONS=15730; FAIL=0.
AGGREGATED_MAX_CONTIGUOUS_BYTES=64; OVER_LIMIT_GROUPS=0; STATUS=PASS.
ACTIONS_SNAPSHOT_ROWS=1308; commit-trigger run list is published separately.

## Ledger final parent (publication commit dikecualikan)

- Baseline inklusif: 7bcfef67d0adf89b7ab0cb20e040790f15766017
- HEAD parent tepat sebelum commit publikasi: 80a58f52e6e6144590a19e7ca54cc6f2e495dd5d
- Rentang dihitung: 7bcfef67d0adf89b7ab0cb20e040790f15766017^..80a58f52e6e6144590a19e7ca54cc6f2e495dd5d; commit publikasi laporan sendiri tidak dihitung.
- Commit total tanpa publikasi: **136**; manusia: **82**; bot: **54**.
- Dengan commit publikasi bot: **137**; manusia: **82**; bot: **55**.
- Klasifikasi bot memakai heuristik nama/email; identitas ambigu harus ditinjau.
