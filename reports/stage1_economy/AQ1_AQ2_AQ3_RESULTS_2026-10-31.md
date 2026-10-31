# AQ1 / AQ2 / AQ3 — Stage 1 Economy Results (2026-10-31)

Repository: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`
Scope: Naruto — Shinobi no Sato no Jintori Gassen (PS1), SLPS-03553.
Baseline HEAD supplied: `4a97f2579e96307c6ffa9298f71cf18b6076ae61`.
Report content was first committed at `44ecc294692be49d54fee9a759cb3d489b534d37`; subsequent commits record raw-permalink verification.

## Executive status

- AQ1 static Ghidra census: **SUCCESS / completed**. This is a static candidate census under Entry 1's candidate import base `0x800AD450`; it does not establish runtime address mapping or complete indirect-call resolution.
- AQ2 H6 no-gameplay-input frame-180 capture: **PASS / completed**. Two independent launches returned identical first-2-MiB RAM SHA and identical 22-record snapshots. H6 remains **HYBRID**, not target-pure.
- AQ3 video frame/saldo inspection: **BLOK FRAME**. No video frame asset or raw frame from a timestamp was available in this chat; no new video ledger was created.

## AQ1 — Static Ghidra census

Workflow run `41169411383`, job `124443914305`, result SUCCESS, exit code 0.
Source checkout: `55d6619c95477e5188347133154f286973ce6e44`.
Entry 1 identity: directory index 1, file offset `0x10BB000`, 596412 bytes, SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`.
Candidate import base: `0x800AD450`; runtime mapping remains **NOT VALIDATED**.

### Five jump-table entries at 0x800AD5F4

| Index | Table slot | Target / PC | Containing function |
|---:|---|---|---|
| 0 | 0x800AD5F4 | 0x800B7760 | FUN_800b770c (entry 0x800B770C) |
| 1 | 0x800AD5F8 | 0x800B77A0 | FUN_800b770c (entry 0x800B770C) |
| 2 | 0x800AD5FC | 0x800B7808 | FUN_800b770c (entry 0x800B770C) |
| 3 | 0x800AD600 | 0x800B7850 | FUN_800b770c (entry 0x800B770C) |
| 4 | 0x800AD604 | 0x800B789C | FUN_800b770c (entry 0x800B770C) |

The TSV stores a 64-byte excerpt from each branch target. All five targets are inside the same Ghidra function body. The branch-table read itself is static at the candidate base; runtime reachability has not been proven.

### Record-field displacement census

Recounted from the published TSV (1,282 data rows including 1 META, 5 JUMP, 39 ACCESSOR_CALL, 47 HELPER_CALL, 1,188 FIELD, 1 TOTAL, 1 LIMIT):

| Offset | READ | WRITE | OTHER | Total |
|---|---:|---:|---:|---:|
| +0x00 | 582 | 107 | 17 | 706 |
| +0x0B | 10 | 2 | 0 | 12 |
| +0x20 | 354 | 111 | 5 | 470 |
| **Total** | **946** | **220** | **22** | **1,188** |

The 1,188 entries were found in 97 unique function scopes reached from references to record pointer slot `0x8013EA84`, the two helper functions, and their direct callers. These are **candidate displacement accesses**, not 1,188 independently proven record-pointer aliases: the script does not establish base-register dataflow for every row. It may both include same-offset accesses to another structure and miss computed/indirect aliases outside this scope. Thus the output is not claimed as a mathematically complete global xref census. Excerpts/instructions and PCs are retained row-by-row in the TSV.

### Direct callers of FUN_800B770C / FUN_800BDC4C

- Direct JAL sites to `0x800B770C`: **44**.
- Direct JAL sites to `0x800BDC4C`: **3**.
- Total direct helper call sites: **47**.

Every direct call-site PC, caller entry/function and 64-byte local excerpt is in the TSV. Callers without a Ghidra function assignment remain `TIDAK TAHU`. Indirect JALR callers are unresolved.

### Direct callers of Chakra setter/getter

| Caller context classification | Setter 0x8001387C | Getter 0x800138EC |
|---|---:|---:|
| Record-slot xref + participant +0x2EE scope | 5 | 1 |
| Record-slot xref only | 2 | 2 |
| Participant +0x2EE scope only | 1 | 1 |
| Manager +0xB44 scope | 4 | 4 |
| Unclassified direct caller | 2 | 17 |
| **Total** | **14** | **25** |

Group totals are direct JAL sites classified by containing function's static references and candidate displacement scope; they do not prove that every call passes a particular record object or semantic transaction context. Full PC/function/instruction rows are in the TSV.

Semantic labels `build`, `upgrade`, `income`, `release` are **TIDAK TAHU** from this census. It must not be used to infer the meaning of +0x0B from streamer statements. Ghidra analysis and text export succeeded; game/emulator was not executed in AQ1.

## AQ2 — Two H6 hybrid no-input captures at frame 180

Workflow run `41169411368`, job `124443914422`, result PASS, script exit code 0.
Source checkout: `55d6619c95477e5188347133154f286973ce6e44`.
Method: two independent launches; no gameplay input; savestate loaded and RAM captured after 180 post-load GPU VSync frames.
Memory Card SHA before/after was unchanged in both launches.

H6 composition:
- Target source checkpoint SHA-256: `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`, 21,163,286 bytes.
- Control checkpoint SHA-256: `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`, 21,162,546 bytes.
- H6 hybrid SHA-256: `d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475`.
- H6 is target savestate base with top-level SPU field 6 sourced from CONTROL. It is **not a pure target checkpoint**.

| Attempt | RAM SHA (first 2 MiB @ 0x80000000) | Pointer slot 0x8013EA84 | Count slot 0x8013EAC8 | Rows |
|---:|---|---|---:|---:|
| 1 | 4c964aaca0afccc68317acd0726fec680c305b903cd426e70afe3d8ac1f1e741 | 0x8013B818 | 22 | 22 |
| 2 | 4c964aaca0afccc68317acd0726fec680c305b903cd426e70afe3d8ac1f1e741 | 0x8013B818 | 22 | 22 |

Both hashes match the expected AK1 H6@180 SHA:
`4c964aaca0afccc68317acd0726fec680c305b903cd426e70afe3d8ac1f1e741`.

The record stride is `0x124`. Indices 0–21 were read in both attempts. Snapshot observations, identically repeated in both launches:

- `+0x0B` distribution: `0:22` (all 22 records have byte value 0).
- `+0x20` halfword: `61472` (`0xF020`) for every record.
- Selected B offset: `+0x10` for every record, according to `((u16(+0x20) >> 7) & 0x1E) + 0x10`.
- The selected B values, indices 0–21: `0, 35, 50, 50, 60, 0, 60, 85, 70, 70, 60, 0, 100, 110, 130, 110, 100, 0, 0, 70, 60, 50`.
- The `FUN_800B770C` result was recomputed for every record from selected B and selector +0x0B; **22/22 matched** in each attempt.
- `+0x00` observed-value distribution per attempt: `0:1, 1:2, 2:2, 4:17`. These are raw values only; no status meaning is assigned here.

Values 60, 100, 50, 150 and 580 appear in selected/table halfwords in this snapshot; 2700 did not appear in the examined 16 halfwords per record. These are **comparison-only coincidences**, not evidence of build cost, upgrade price, income, toll or release value. The selector distribution is only the H6@180 sample and does not establish all selector modes.

Capture caveat: the two emulator launches reached frame 180 and produced valid RAM snapshots at approximately 61.198 s and 60.157 s. The outer run waited to the 600 s launch timeout and GDB wrapper exit was `-9` in both attempts; emulator exit code is **TIDAK TAHU**. This does not invalidate the already-created and byte-identical frame-180 RAM snapshots, but it means normal emulator shutdown was not established. Both private RAM dumps, checkpoints, BIOS, disc and Memory Card working copies were removed before publication; only TSV/TXT outputs were committed.

### Evidence scale (K0–K5)

- AQ1 static census: **K3 maximum for candidate code/arithmetic facts**, not K4. The base mapping and complete source-to-mutation transaction chains remain open.
- AQ2 H6@180 raw-state snapshot: **K5 for reproducibility of this exact H6 hybrid snapshot only**, because two independent runtime launches produced the same 2-MiB SHA and same 22-record data. This does not elevate the semantics of +0x0B, tile ownership, balance, build/upgrade, income, or release to K5.
- AQ3: **BLOK FRAME**, so no frame-derived K rating is assigned.

## AQ3 — Video timestamp and balance reading

BLOK FRAME — no raw frame/video asset from the requested timestamp was available in this chat, so a numeric balance reading cannot be verified. No additional video ledger has been created.

## Published run summaries and outputs

AQ1:
- `reports/stage1_economy/aq1-run-41169411383/attempt-1/aq1-economy-census.tsv`
- `reports/stage1_economy/aq1-run-41169411383/attempt-1/aq1-recount.txt`
- `reports/stage1_economy/aq1-run-41169411383/attempt-1/run-summary.txt`
- `reports/stage1_economy/aq1-run-41169411383/attempt-1/ACTIONS_RUN_SUMMARY.txt`

AQ2:
- `reports/stage1_economy/aq2-run-41169411368/attempt-1/AQ2_H6_FRAME180_RECORDS.tsv`
- `reports/stage1_economy/aq2-run-41169411368/attempt-1/AQ2_LAUNCHES.tsv`
- `reports/stage1_economy/aq2-run-41169411368/attempt-1/AQ2_H6_SUMMARY.txt`
- `reports/stage1_economy/aq2-run-41169411368/attempt-1/ACTIONS_RUN_SUMMARY.txt`

Repository policy respected: no ISO, BIOS, savestate, raw RAM dump, video or frame image was committed. Release/visibility settings were not changed.


## Raw permalink verification follow-up

- Run: `41171434910`; job: `124450039018`; status: **FAILURE**; exit code: **1**.
- The runner used `curl` against all eight raw permalinks pinned to `44ecc294692be49d54fee9a759cb3d489b534d37`. Every request returned HTTP **404**.
- The connected GitHub file/API reader successfully retrieved the same eight file contents, but this does not override the curl result. Repository metadata reports visibility `public`; no repository visibility or Release setting was changed. The discrepancy between API retrieval and raw-host HTTP 404 remains **UNRESOLVED**.
- The detailed per-path status is stored in `reports/stage1_economy/raw-link-check-41171434910/CURL_HTTP_STATUS.tsv`.
