# DT0–DT4 — raw-byte static audit

BASELINE_INCLUSIVE=2f72b3a2807f1022048083d6d07ad527adaa7cf7
SNAPSHOT_SHA=524d2421e72ce8707c37d9564f4e95eb5cc9fcb9
DU0_SNAPSHOT_SHA=524d2421e72ce8707c37d9564f4e95eb5cc9fcb9
DU0_TOTAL=4 MANUSIA=3 BOT=1

## DT1
Loop raw instruction window: 31 instructions, 0x800ECA0C–0x800ECA84; complete bytes in DT1_LOOP_RAW.tsv.
Register origins for t0/t1/t2/a2/a3 are in DT1_REGISTER_ORIGINS.tsv; unresolved incoming definitions are kept as TIDAK TAHU.
All direct Entry 1 stores resolved to 0x80139EFC: 38; CLEAR stores: 15 (previous DS census expectation 7). See DT1_FEE_GLOBAL_CLEARS.tsv and DT1_CLEAR_CENSUS_SUMMARY.txt.
Tile field loads, packed tile+0x20 halfword path, and operands at 0x800ECAA0 are in their respective TSV files. The bit field is not assigned a gameplay name unless proven by its consumers.

## DT2
0x80102434: FF FF 02 24 addiu $v0, $zero, -1.
Second path returns through jr at 0x80102430; v0 before slot trace: 0x80102424 lw $v0, 0xea8($v1) [A8 0E 62 8C]; basis=0x8010240C lw $v1, -0x5dd4($v0) [2C A2 43 8C]; basis=0x80102408 lui $v0, 0x8014 [14 80 02 3C]; after slot trace: 0x80102424 lw $v0, 0xea8($v1) [A8 0E 62 8C]; basis=0x8010240C lw $v1, -0x5dd4($v0) [2C A2 43 8C]; basis=0x80102408 lui $v0, 0x8014 [14 80 02 3C].
DATA.BIN excerpt: offset 0x11493C8, 64 bytes max, table base 0x8013B818; see DT2_TABLE_EXCERPT.txt.

## DT3
CFG incoming edges are in DT3_CALLSITE_PREDECESSORS.tsv; selector conditions in DT4_REGISTER_CONDITIONS.tsv; indirect tables in DT3_JR_DISPATCH_TABLES.tsv and DT3_JR_V0_TABLE.txt.
State/event numeric value is reported only where a static branch operand or table entry proves it; otherwise it is TIDAK TAHU due to indirect/data-dependent dispatch.

## DT4
All input values are user-supplied hypotheses, not observed ROM facts. H1, independent lookup H2 and piecewise user rule H3 are tested in DU5_FEE_MODEL_TEST.tsv.
fee_dasar=100 is an input hypothesis. H2 multipliers {1:1,2:3,3:6,4:10} are an independent falsifiable alternative, not ROM evidence.
