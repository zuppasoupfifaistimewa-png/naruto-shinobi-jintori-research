# DV0–DV4 — audit statis raw-byte Naruto Jintori

BASELINE_INCLUSIVE=7040cd08a79107a45de6571e875de4fadb165c8a
SNAPSHOT_SOURCE_SHA=fed79376ccd639ffaad6f30ddf6feb080e6a8b3b
DV0_TOTAL_INCLUSIVE=3 HUMAN=3 BOT=0
HEAD_AT_ANALYSIS=SNAPSHOT_SOURCE_SHA; publication bot commit is created afterwards and is not included in the inclusive ledger.

## DV1 — FUN_800EC574
Raw block PC 0x800EC9CC..0x800ECBD0: 130 decoded instruction slots; bytes and exact file offsets are in DV1_FUN_800EC574_BLOCK_RAW.tsv.
Accumulator loop: tile index is scaled by 0x124; tile+0 must equal t2=5; bits12-15 of tile+0x20 must equal dynamic t0; bits8-11 are added as 1+nibble to global 0x80139EFC for each accepted tile.
At 0x800ECBB8 the loaded global value is dynamic/TIDAK TAHU, negated, then stored as a halfword at manager-relative +0x2EE. No runtime numeric value is claimed.
Direct +0x4F0 load references found: 13; all candidates and first local uses are in DV1_MANAGER_PLUS4F0_READERS.tsv.

## DV2 — indirect dispatch
CFG representative path rows=46; branch edges in target slices=18. Runtime selector values remain TIDAK TAHU; required values are 44 and 2 to select the known handler slots.
Direct writes to displacement +0x2E9 found=253; selector-source stores through a0 in caller region=28. These are candidates, not proof of pointer identity.

## DV3 — source resource record and tile fields
FUN_800F7ADC loader code slots examined=254; direct source-load/destination-store candidates=2.
DATA.BIN header candidates of exactly 415 x 0x1E bytes=0. Histograms are emitted only for those exact extents; resource identity requires cross-reference to loader code.
Tidak ada sumber field atau initial nibble +0x20 yang dianggap terkonfirmasi tanpa load/store dataflow yang cocok. Lihat DV3_FIELD_MAPPING_STATUS.tsv.

## DV4 — fee hypotheses
H2' lookup {1:1,2:4,3:8,4:16,5:32} is algebraically identical to H3 (d=1: base; d>=2: base*2^d). Only d=1 distinguishes H1 from the H2'/H3 pair. No point distinguishes H2' from H3.
fee_dasar=100 and 50 are input hypotheses, not estimates. No fitting is performed.

All PCs use Entry 1 mapping file_offset=0x10BB000+(PC-0x800AD450). Static only; no emulator/runtime/savestate; only text/TSV outputs.
