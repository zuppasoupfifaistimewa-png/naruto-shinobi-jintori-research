# NA0-NA5 static audit — SLPS-03553

Baseline inklusif: 7bcfef67d0adf89b7ab0cb20e040790f15766017
Source SHA: 4cc242dbd482303ff8204bd92d4a56202eba2423
EXE SHA-256: a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569
Entry 1 SHA-256: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a
EMULATOR_LAUNCHES=0.

## Status per butir
- NA0: SEBAGIAN K2 — py_compile 68/68; .py aktual=67; sumber .txt dihitung=1; validasi bytes/offset/decode=15893/15893; excerpt maksimum=124 B; pelanggaran=4.
- NA1: SEBAGIAN K3 — scene record=39; enam base PC dianalisis; asal argumen/wallet/index dan CFG pemanggilan belum seluruhnya tertutup.
- NA2: SEBAGIAN K3 — sw 0x118($gp)=2; assignment $gp=2; writer EA88/39EFC=66; lw M=2085; x=d dan batas 52 TIDAK TAHU.
- NA3: SEBAGIAN K3 — edge ke B24C8=0; static JALR BE5D8=0; unresolved JALR=12; computed caller belum tertutup.
- NA4: TUNTAS K4 — hanya statis; emulator/game 0; tanpa BIOS/savestate/RAM dump/video; tanpa biner di commit.
- NA5: BELUM K1 — x=d belum terbukti; biaya lompat level d>=2 TIDAK TAHU; tanpa angka asumsi atau fitting.

## Batas bukti
Scene table anchor=0x800558A4; stride=0x1C; jumlah record=39.
NA2 M-use census is bounded and linear; it is not a whole-program CFG/alias writer proof. An empty recognizer is not evidence of no writers.
V0 continuity rows only pass when every intervening instruction exists, no v0 redef, no call, and no branch entry is seen. Otherwise TIDAK TAHU.
NA3 counts recognized code and constant indirect targets only; computed/dynamic targets remain TIDAK TAHU.

## Validasi NA0
PY_COMPILE=68/68; PY_FILES=67; TXT_SOURCE_FILES=1.
FILE_OFFSET_RAW_DECODE_CHECKS=15893; DECODED_INSTRUCTIONS=15773; FAIL=0.
AGGREGATED_MAX_CONTIGUOUS_BYTES=124; OVER_LIMIT_GROUPS=4; STATUS=FAIL.
ACTIONS_SNAPSHOT_ROWS=1252; commit-trigger run list is published separately.

## Ledger final parent (publication commit dikecualikan)

- Baseline inklusif: 7bcfef67d0adf89b7ab0cb20e040790f15766017
- HEAD parent tepat sebelum commit publikasi: 4cc242dbd482303ff8204bd92d4a56202eba2423
- Rentang dihitung: 7bcfef67d0adf89b7ab0cb20e040790f15766017^..4cc242dbd482303ff8204bd92d4a56202eba2423; commit publikasi laporan sendiri tidak dihitung.
- Commit total tanpa publikasi: **2**; manusia: **1**; bot: **1**.
- Dengan commit publikasi bot: **3**; manusia: **1**; bot: **2**.
- Klasifikasi bot memakai heuristik nama/email; identitas ambigu harus ditinjau.
