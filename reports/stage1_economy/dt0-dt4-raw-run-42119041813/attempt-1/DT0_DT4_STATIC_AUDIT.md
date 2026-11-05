# DT0–DT4 — raw-byte static audit

BASELINE_INCLUSIVE=2f72b3a2807f1022048083d6d07ad527adaa7cf7
SNAPSHOT_SHA=dd91e9df41ccc05f48917abfc91d44366bde458b
DT0_TOTAL=2 MANUSIA=2 BOT=0

## DT1
Loop raw instruction window: 31 instructions, 0x800ECA0C–0x800ECA84; complete bytes in DT1_LOOP_RAW.tsv.
Register origins for t0/t1/t2/a2/a3 are in DT1_REGISTER_ORIGINS.tsv; unresolved incoming definitions are kept as TIDAK TAHU.
Direct writers of 0x80139EFC found before/inside the loop: 3; exact CLEAR stores are marked is_clear=YES in DT1_FEE_GLOBAL_WRITERS.tsv.
Tile field loads, packed tile+0x20 halfword path, and operands at 0x800ECAA0 are in their respective TSV files. The bit field is not assigned a gameplay name unless proven by its consumers.

## DT2
0x80102434: FF FF 02 24 addiu $v0, $zero, -1.
Second path returns through jr at 0x80102430; v0 before slot trace: 0x80102424 lw $v0, 0xea8($v1) [A8 0E 62 8C]; basis=0x8010240C lw $v1, -0x5dd4($v0) [2C A2 43 8C]; basis=0x80102408 lui $v0, 0x8014 [14 80 02 3C]; after slot trace: 0x80102424 lw $v0, 0xea8($v1) [A8 0E 62 8C]; basis=0x8010240C lw $v1, -0x5dd4($v0) [2C A2 43 8C]; basis=0x80102408 lui $v0, 0x8014 [14 80 02 3C].
DATA.BIN excerpt: offset 0x11493C8, 64 bytes max, table base 0x8013B818; see DT2_TABLE_EXCERPT.txt.

## DT3
Call-site incoming edges and indirect dispatcher evidence are in DT3_CALLSITE_PREDECESSORS.tsv and DT3_INDIRECT_DISPATCHERS.tsv.
State/event numeric value is reported only where a static branch operand or table entry proves it; otherwise it is TIDAK TAHU due to indirect/data-dependent dispatch.

## DT4
All four input values are user-supplied hypotheses, not observed ROM facts. H1=100×2^d; H2=100×multiplier lookup {1:1,2:4,3:8,4:16}.
Both candidate models are distinct and are checked against d=1..4; no parameter is fitted from fewer than three points.
