# DK0-DK3 corrected static audit — 12 DATA.BIN resources

Game: Naruto - Shinobi no Sato no Jintori Gassen (SLPS-03553).
Historical baseline 447631d02db0649abb07f7064ddf250bba81d779; cutoff inclusive 8141a8bd851b00e183797007563168d9ea6fdcdf.
DATA.BIN identity: 66015232 bytes; SHA-256 69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822; resources=12; records=415.
This corrected report supersedes the first DK parse (run 41815588375 attempt 2): that parser used raw source +0x0E as X, disproved by the static loader; its original 415-record numeric findings are invalid.

## K0-K5 evidence scale
- K0: no direct evidence; TIDAK TAHU.
- K1: one weak clue/hypothesis only.
- K2: two independent observations agree, source/data relationship still open.
- K3: multiple byte-level findings corroborate; semantic mapping or resource selection remains incomplete.
- K4: reproducible exact static bytes plus disassembled loader mapping; maximum static grade.
- K5: runtime confirmed in at least two independent launches; not used here.

| Task | Status | K | Result |
|---|---|---:|---|
| DK0 historical commit ledger | TUNTAS | K4 | Two commits after baseline through 8141a8...; both MANUSIA. |
| DK1 layout + loader field map | TUNTAS | K4 | 2 same; 0 different; 10 unclear. |
| DK2 user-value cells (loader-mapped) | TUNTAS | K3 | 30 cells checked against 415 records. |
| DK2 repeated-X vectors | TUNTAS | K3 | 0 X values with differing LV vectors. |
| DK3 LV1=X/2 | TUNTAS | K3 | 167/415 pass; 248 exceptions. |
| DK3 LV2=10*ceil(1.1X) | TUNTAS | K3 | 167/415 pass; 248 exceptions. |
| DK3 LV3-LV5 provenance | SEBAGIAN | K3 | Runtime loader copies stored values; offline formula vs authored table TIDAK TAHU. |

## Critical offset correction from FUN_800F7ADC
Resource record pointer starts at resource+1 and advances by 0x1E. Disassembly proves source mapping:
| Source record bytes | Runtime destination | Field interpretation here |
|---|---|---|
| +0x08..+0x09 | tile+0x0E | adjacent field, not X (known row value 255) |
| +0x0A..+0x0B | tile+0x10 | X candidate |
| +0x0C..+0x0D | tile+0x12 | LV1 |
| +0x0E..+0x0F | tile+0x14 | LV2 |
| +0x10..+0x11 | tile+0x16 | LV3 |
| +0x12..+0x13 | tile+0x18 | LV4 |
| +0x14..+0x15 | tile+0x1A | LV5 |
| +0x16..+0x17 | tile+0x1C | extra |
| +0x18..+0x19 | tile+0x1E | extra |
| +0x1A..+0x1B | tile+0x22 | extra |
| +0x1C..+0x1D | tile+0x24 | extra |
| +0x1E | tile+0x0C | loader reads one byte beyond stride; next record's first byte, EOF on last |

So literal raw source offsets requested by the user (+0x0E as X and +0x10..+0x18 as LV1..5) do not identify those fields. DK1 contains both requested-literal raw values and loader-mapped values; DK2 reports matches under both interpretations. Main DK2/DK3 use the loader-mapped fields to avoid mislabeling raw data.

## DK0 historical commit ledger
| Full commit SHA | Author | Changed files |
|---|---|---|
| b81db45b4ac13d6c69923e25e3c00a4611818d18 | MANUSIA: zuppasoupfifaistimewa-png | 6 files listed below |
- reports/stage1_economy/CI0_CI1_CI2_CI3_STATIC_AUDIT_2026-11-04.md
- reports/stage1_economy/CI0_COMMIT_LEDGER_2026-11-04.tsv
- reports/stage1_economy/CI1_LEVEL_BANK_RECORDS_ALL_2026-11-04.tsv
- reports/stage1_economy/CI1_SELECTOR_RESOURCE_INVENTORY_2026-11-04.tsv
- reports/stage1_economy/CI2_OBSERVATION_CELL_MATCHES_2026-11-04.tsv
- reports/stage1_economy/CI3_HB_FORMULA_TEST_2026-11-04.tsv
| 8141a8bd851b00e183797007563168d9ea6fdcdf | MANUSIA: zuppasoupfifaistimewa-png | 2 files listed below |
- reports/stage1_economy/CI0_CI1_CI2_CI3_STATIC_AUDIT_2026-11-04.md
- reports/stage1_economy/CI0_COMMIT_LEDGER_2026-11-04.tsv
Later preparation and bot-output commits are outside the historical cutoff.

## DK1 — resource classes
Exact checks: size=1+N*0x1E; byte zero=N; all loader-mapped records have X<=4095, LV<=10000, monotonic LV1..LV5, and zero-X rows have zero levels.
| ID | N | header | bytes | class | byte reason |
|---|---:|---:|---:|---|---|
| 0x276 | 22 | 22 | 661 | TIDAK_JELAS | size/header match; plausible=5/22 |
| 0x277 | 33 | 33 | 991 | TIDAK_JELAS | size/header match; plausible=8/33 |
| 0x278 | 33 | 33 | 991 | TIDAK_JELAS | size/header match; plausible=8/33 |
| 0x279 | 34 | 34 | 1021 | TIDAK_JELAS | size/header match; plausible=10/34 |
| 0x27A | 33 | 33 | 991 | TIDAK_JELAS | size/header match; plausible=8/33 |
| 0x27B | 43 | 43 | 1291 | TIDAK_JELAS | size/header match; plausible=11/43 |
| 0x27C | 38 | 38 | 1141 | TIDAK_JELAS | size/header match; plausible=10/38 |
| 0x27E | 22 | 22 | 661 | TIDAK_JELAS | size/header match; plausible=5/22 |
| 0x27F | 38 | 38 | 1141 | TIDAK_JELAS | size/header match; plausible=10/38 |
| 0x285 | 43 | 43 | 1291 | TIDAK_JELAS | size/header match; plausible=16/43 |
| 0x286 | 36 | 36 | 1081 | LAYOUT_SAMA | size=1+36*0x1E; header=36=N; plausible=36/36 |
| 0x287 | 40 | 40 | 1201 | LAYOUT_SAMA | size=1+40*0x1E; header=40=N; plausible=40/40 |

DK1 full TSV includes every record, exact raw requested offsets, loader-mapped X/LV fields, +0x1A, +0x1C, +0x1E, absolute DATA.BIN offsets and resource SHA-256.

## DK2 — user values are hypotheses, not facts
| X | LV1 | LV2 | LV3 | LV4 | LV5 |
|---:|---|---|---|---|---|
| 120 | 60: NONE | 140: NONE | 265: NONE | 530: NONE | 1050: NONE |
| 180 | 90: NONE | 200: NONE | 390: NONE | 800: NONE | 1600: NONE |
| 200 | 100: NONE | 220: NONE | 440: NONE | 880: NONE | 1760: NONE |
| 220 | 110: NONE | 250: NONE | 490: NONE | 980: NONE | 1940: NONE |
| 240 | 120: NONE | 270: NONE | 530: NONE | 1050: NONE | 2120: NONE |
| 280 | 140: NONE | 310: NONE | 620: NONE | 1240: NONE | 2470: NONE |

All exact matches and all same-X row values are listed in DK2 TSV, along with literal-offset matches. Cross-resource full-vector conflicts: none.

## DK3 formula tests
LV1=X/2: 167/415 pass, 248 exceptions.
LV2=10*ceil(11X/100): 167/415 pass, 248 exceptions.
LV1 exception pairs and all locations:
- X=3584, LV1=4609: 0x277#17, 0x277#27, 0x277#31, 0x27B#9, 0x27B#40, 0x27B#41, 0x27C#37, 0x27F#37, 0x285#41
- X=8704, LV1=17409: 0x276#14, 0x278#14, 0x279#15, 0x279#20, 0x279#21, 0x27A#13, 0x27A#16, 0x27B#13, 0x27B#15, 0x27C#33, 0x27C#36, 0x27E#12, 0x27E#13, 0x27E#14, 0x27E#15, 0x27E#16, 0x27F#33, 0x27F#36, 0x285#13, 0x285#15
- X=13824, LV1=27649: 0x277#28, 0x277#29, 0x277#30, 0x278#20, 0x279#16, 0x279#17, 0x279#18, 0x27A#14, 0x27A#15, 0x27B#14, 0x27B#19, 0x27C#12, 0x27C#34, 0x27C#35, 0x27F#12, 0x27F#34, 0x27F#35
- X=17920, LV1=34560: 0x276#1, 0x277#1, 0x277#2, 0x277#26, 0x278#2, 0x278#3, 0x279#2, 0x279#3, 0x279#10, 0x279#11, 0x279#12, 0x27A#1, 0x27A#2, 0x27A#31, 0x27A#32, 0x27C#1, 0x27C#2, 0x27C#27, 0x27C#28, 0x27F#1, 0x27F#2, 0x27F#27, 0x27F#28
- X=18944, LV1=37889: 0x27B#18, 0x27C#13, 0x27F#13, 0x285#18
- X=26624, LV1=50689: 0x27C#14, 0x27F#14
- X=28160, LV1=56320: 0x276#2, 0x276#3, 0x276#21, 0x277#3, 0x277#24, 0x277#25, 0x278#4, 0x278#5, 0x278#22, 0x278#32, 0x279#4, 0x279#5, 0x279#8, 0x279#9, 0x27A#3, 0x27A#5, 0x27A#28, 0x27A#29, 0x27B#1, 0x27B#27, 0x27B#28, 0x27B#30, 0x27B#35, 0x27B#36, 0x27C#3, 0x27C#4, 0x27F#3, 0x27F#4, 0x285#1, 0x285#27, 0x285#28, 0x285#30, 0x285#35, 0x285#36
- X=35840, LV1=2304: 0x276#4, 0x276#6, 0x276#10, 0x276#20, 0x277#5, 0x277#6, 0x279#6, 0x27A#6, 0x27A#7, 0x27A#26, 0x27A#27, 0x27B#25, 0x27B#26, 0x27B#37, 0x27C#6, 0x27C#25, 0x27E#1, 0x27F#6, 0x27F#25, 0x285#25, 0x285#26, 0x285#37
- X=40960, LV1=13824: 0x276#8, 0x276#9, 0x276#19, 0x277#7, 0x277#8, 0x277#14, 0x277#15, 0x277#21, 0x277#22, 0x278#6, 0x278#23, 0x278#24, 0x279#25, 0x279#26, 0x27A#23, 0x27A#25, 0x27B#38, 0x27C#7, 0x27C#23, 0x27C#24, 0x27E#2, 0x27E#3, 0x27F#7, 0x27F#23, 0x27F#24, 0x285#38
- X=46080, LV1=26624: 0x276#7, 0x277#9, 0x278#8, 0x278#9, 0x278#30, 0x278#31, 0x27A#9, 0x27A#10, 0x27A#21, 0x27A#22, 0x27B#4, 0x27B#5, 0x27B#34, 0x27C#8, 0x27C#22, 0x27E#4, 0x27E#6, 0x27E#10, 0x27E#20, 0x27E#21, 0x27F#8, 0x27F#22, 0x285#4, 0x285#5, 0x285#34
- X=51200, LV1=34304: 0x277#11, 0x277#12, 0x277#16, 0x278#10, 0x278#11, 0x278#17, 0x278#18, 0x279#27, 0x279#31, 0x279#32, 0x27A#11, 0x27B#6, 0x27B#32, 0x27B#33, 0x27C#9, 0x27C#10, 0x27C#17, 0x27C#18, 0x27E#8, 0x27E#9, 0x27E#19, 0x27F#9, 0x27F#10, 0x27F#17, 0x27F#18, 0x285#6, 0x285#32, 0x285#33
- X=56320, LV1=47104: 0x276#12, 0x276#16, 0x278#12, 0x278#25, 0x278#26, 0x279#23, 0x279#30, 0x27A#20, 0x27B#7, 0x27B#21, 0x27B#31, 0x27C#16, 0x27C#29, 0x27C#30, 0x27E#7, 0x27F#16, 0x27F#29, 0x27F#30, 0x285#7, 0x285#21, 0x285#31
- X=64000, LV1=59904: 0x276#13, 0x276#15, 0x277#18, 0x278#15, 0x278#16, 0x278#29, 0x279#22, 0x27A#19, 0x27B#12, 0x27B#16, 0x27B#22, 0x27B#23, 0x27B#42, 0x285#12, 0x285#16, 0x285#22, 0x285#42

LV1 competing hypotheses:
1. Stored per-record override; LV1=35 at X=60 and LV1=85 at X=160 are literal source halfwords copied by the loader. Falsifier: a separate code path computes LV1 from X and overwrites that halfword before it is consumed.
2. Hidden record-class/flag conditional adds +5 relative to X/2. Falsifier: identical relevant flags/class with differing +5 behavior, or proof no downstream conditional exists. The selector is TIDAK TAHU.

LV3-LV5 competing hypotheses:
1. Runtime table lookup: loader copies LV3-LV5 from source halfwords. Falsifier: find runtime path deriving and overwriting those values from X.
2. Offline formula-generated table: build-time process could generate the stored values. Falsifier for a concrete formula is three or more distinct X values that violate its exact rounding/piecewise rule. A few matches do not prove it.
Candidate floor/ceil/nearest tests for 2.2X, 4.4X, 8.8X are in DK3_FORMULA_CANDIDATE_SUMMARY; source authorship vs offline formula: TIDAK TAHU.

## Integrity
- Static DATA.BIN/resource bytes and disassembled loader only; no emulator, BIOS, savestate, gameplay, video or frames.
- Binary inputs were temporary runner files and deleted before commit.
- Only MD/TSV/TXT committed; Release and STATUS.md unchanged.
- Maximum grade K4 static; no K5 claim.
