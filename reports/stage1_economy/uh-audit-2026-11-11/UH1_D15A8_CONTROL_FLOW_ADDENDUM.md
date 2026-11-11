# UH1 addendum — FUN_800D15A8 store and state-machine context

AUDIT_BASELINE_INCLUSIVE=c7da18bef75f6e6905d495b72710f50aaf1bb5b0
REVIEWED_REPO_HEAD_BEFORE_ADDENDUM=2ba02b4fbadcdd2974ce77b54a6c4e70d0708a2d
EVIDENCE_CLASS=STATIC_ONLY
MAX_CONFIDENCE=K4
GAME_OR_EMULATOR_EXECUTED=NO
GAMEPLAY_INPUT_SENT=NO
SAVESTATE_RESTORED=NO
CODE_OR_WORKFLOW_CHANGED=NO

## Scope and source identity

This addendum rechecks only the previously unresolved interpretation of the ENTRY1 store at PC 0x800D5A1C. It uses retained text artifacts:

- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-d15a8-focused.txt`: Ghidra selected-function audit of `FUN_800D15A8`, function body 17,944 bytes, decompilation SUCCESS. The run summary reports SOURCE_SHA `27a716552d7638feedc09fb103c6f3545431765e`, ENTRY1 SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`, size 596,412 bytes, file offset 0x10BB000, and imported base 0x800AD450 as a static candidate.
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-d15a8-direct-callers.txt`: Ghidra direct-reference export.
- `reports/stage1_economy/DY2_TILE_ARRAY_WRITERS_ANNOTATED.tsv` and `reports/stage1_economy/uh-audit-2026-11-11/UH1_TILE_WRITER_AUDIT.tsv`: exact store PC, instruction bytes, source immediate and base-slot provenance.
- `reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA2_HA3_STATIC_SUMMARY.txt`: independent retained static scan reports the same ENTRY1 SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`.

The imported base 0x800AD450 remains a static hypothesis, not runtime-validated. Any PC-to-file-offset mapping below is conditional on that import mapping.

## Exact store and record address

The writer census identifies:

- PC 0x800D5A18: `ori $v1, $zero, 0xF020`
- PC 0x800D5A1C: bytes `20 00 43 A4`, instruction `sh $v1, 0x20($v0)`
- destination base provenance: slot 0x8013EA84
- decompiled destination expression: `DAT_8013eb20 * 0x124 + DAT_8013ea84`
- store destination: that indexed record base plus 0x20.

This closes a narrow gap in the earlier UH1 table: its `stride_0x124_proven=NO_PER_PC_TRACE` label was conservative because the instruction-window trace did not carry the complete index expression. The BB2 decompilation does carry that expression immediately for the same store PC. Therefore, stride 0x124 is supported for this one PC (K4 static); this must not be generalized to all 42 `sh +0x20` writers.

Using the retained Entry1 import candidate, the byte offset is:
`0x10BB000 + (0x800D5A1C - 0x800AD450) = 0x010E35CC`.
This matches the writer-table file offset. Runtime mapping remains unvalidated.

## Control-flow context

The function decompilation has a top-level `switch(DAT_80139f03)`; the meanings of the state variable and case labels are not named by the source.

A path in case 0x02, after its checks and a zero result from `FUN_80102408`, writes `DAT_80139f03 = 0x14`. Case 0x14 then calls three helpers and reaches a shared block that increments `DAT_80139f03` by one and resets `DAT_80139ec2` to zero. This provides a static path into case 0x15; it does not establish a user-visible mechanic name.

In case 0x15, each invocation first increments `DAT_80139ec2`. The branch is:

1. If the incremented counter equals 0x21 (33), the function initializes the selected record at `DAT_8013eb20 * 0x124 + DAT_8013EA84`: byte +0x00 becomes 4; halfword +0x20 becomes 0xF020; and additional fields +0x28, +0x30, +0x32, +0x34, +0x36, +0x37, +0x38, +0x3A, +0x3C, +0x3D, +0x3E, +0x40, +0x42, +0x44, +0x46, and +0x48 are initialized. It calls `FUN_800BE0E4`, decrements the separate object byte at `DAT_8013EA74 + 0x4CC`, resets the counter, and sets the state variable to 8.
2. Otherwise, it examines the selected record. Only when record byte +0x00 equals 5 and the global `_DAT_8013EA8A` equals the top nibble of halfword +0x20 does it subtract 0x80 from record fields +0x44 and +0x46.

Thus the +0x20 store is part of a multi-field record initialization on a counter-gated state-machine branch. Its source is the immediate constant 0xF020, not an increment of a prior value. The alternative branch uses +0x20 as a packed halfword while modifying other fields. Other code in the same function extracts distinct nibbles from +0x20 (shifts/masks 12, 8, 4, and 0) and passes them to helper calls; their semantic labels are not established.

The retained Ghidra reference section lists one direct callsite to this function: `FUN_800F3658` at PC 0x800F5DAC. A direct call reference and historical function-breakpoint hits do not prove that the state-0x15 branch or the 0xF020 store executes on every call or every frame.

## Revised conclusions

- **K4 static:** the specific PC 0x800D5A1C writes immediate 0xF020 to record field +0x20 using the indexed base expression `DAT_8013eb20 * 0x124 + DAT_8013ea84`.
- **K4 static:** that write occurs in state case 0x15 under the counter-equals-33 branch and accompanies initialization of multiple other record fields.
- **Not supported:** interpreting this store as `level += 1`, a per-call level increment, an upgrade fee, a Chakra debit, or a universal writer pattern.
- **TIDAK TAHU:** semantic meanings of byte +0x00, the four +0x20 nibbles, helper `FUN_800BE0E4`, the record's gameplay role, and the event/action that initiates the overall state sequence.
- **Unchanged:** the other 41 `sh +0x20` writers remain subject to their individual provenance limits; all ENTRY0 writer claims remain K0; UH2 remains BELUM. No conclusion about Q1 income, Q2 build/upgrade prices, Q3 barrier release, or Story Mode completion changes.

No emulator was launched. No ROM, BIOS, Memory Card, savestate, RAM dump, executable, DATA.BIN, image, video, or other binary is included in this report.
