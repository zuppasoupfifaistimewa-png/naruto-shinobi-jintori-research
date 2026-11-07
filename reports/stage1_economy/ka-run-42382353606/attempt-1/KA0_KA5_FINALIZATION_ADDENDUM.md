# KA0-KA5 finalization and evidence limits

Baseline inklusif: `656503e9e21cb4baf3185969abf7b15d05a149c6`
Analysis source SHA: `495592eb62ef776fde30d50a96c358e4d2737d3a`
Report publication SHA: `20b9f58205eaaff375ac266f0cbd55f6d786fcf3`
Run: `42382353606`; job: `ka0-ka5-static`; job ID: `128432437635`.

## Final Actions reconciliation

The GitHub Actions run and job completed with `completed/success`; the job step exit is 0. The nested analyzer exit code recorded by the workflow is 1. These are different statuses: the workflow deliberately captures the analyzer result under `set +e` and returns success from the step so that it can publish partial evidence and clean up.

- Python compilation: 66/66 PASS.
- Ghidra EXE: exit 0.
- Ghidra Entry 1: exit 0.
- Private binary cleanup: PASS.
- Emulator/game/BIOS/savestate/RAM: not used; `EMULATOR_LAUNCHES=0`.
- No binary was committed.

**Analyzer exit-code note:** source inspection shows the analyzer's final output guard scans the entire temporary output directory and rejects every extension other than `.txt`, `.tsv`, and `.md`. At the point the analyzer is called, the earlier workflow steps have created Ghidra `.log` and `.exit` side files in that same directory. This is a workflow/analyzer guard-order issue, not a reported Ghidra or extraction failure. The full Ghidra logs were temporary and intentionally not published, so this diagnosis is a static control-flow explanation rather than a copied log line. The existing `ACTIONS_RUN_SUMMARY.txt` therefore remains `STATUS=PARTIAL`, `EXIT_CODE=1` for the analyzer result; do not relabel it PASS.

## KA0 ledger

Snapshot from inclusive baseline through analyzer source SHA:
- Commits: 2 total = 2 human + 0 bot.
- All-event Actions runs: 1,239 across 13 API pages; 79 scheduled.
- Tracked Python scripts compiled: 66/66 PASS.
- The KA run itself was still in progress when the source-time ledger was collected. Final external reconciliation: run 42382353606 = completed/success; job ka0-ka5-static = completed/success; analyzer exit = 1. See `KA0_FINAL_RUN_RECONCILIATION.txt`.

## KA1 — caller and wallet

- The scan found two EXE data-word candidates containing `0x800B50AC`, at EXE PC `0x80055904` (file offset `0x46104`) and PC `0x80055920` (file offset `0x46120`). They are pointer-word candidates, not proven JAL/J or a confirmed dispatch table. The bounded caller-window file is header-only; actual indirect caller/reachability remains **TIDAK TAHU**.
- Requested direct call sites decode to the expected callees: `0x800F5F54 -> 0x800F2A9C`, `0x800B54DC -> 0x800F3658`, and `0x800F5EBC -> 0x800DC2E0`.
- The recorded backward slices provide some $a0/$a1 reaching definitions, but $a2/$a3 remain **TIDAK TAHU**. The slices are static nearest-definition traces, not path-sensitive proofs for every branch.
- `FUN_80014F10` is not proven to set the permanent wallet; JA shows it updates an owner-indexed record at +0x94 only if the new argument is larger.
- Wallet-authoritative setter and the meaning of record +0x04 remain **TIDAK TAHU**. H1/H2 are only K1 hypotheses with falsifiers in `KA1_WALLET_HYPOTHESES.tsv`.

## KA2 — globals and x

The code census found 21 stores with statically resolved constant effective addresses:
- `0x8013EA6E`: 14 `sh` stores.
- `0x8013EB1C`: 3 `sb` stores.
- `0x80139EC7`: 4 `sb` stores; each stores `$zero` (a clear/reset write).

These are the constant-address stores enumerated from Ghidra's imported-code listing. Dynamic/indirect base writers are not ruled out and remain **TIDAK TAHU**. Values for many EA6E/EB1C stores are loaded from memory; their ultimate semantic origin is not resolved by the published backward slices.

For manager +0x530, the three JA writer paths remain:
- `0x800D49D8`: `sw $v0,0x530($a2)`, with `lbu $v0,($v1)` at `0x800D49D0`; the source effective address is dynamic and its address calculation depends on the three global fields.
- `0x800EC844` and `0x800EC868`: store the byte read from `0x80139EC7`; JA also records the low-byte mask.

Thus 0..255 is a **conditional byte-value range for those paths**, not a proven set of operationally reachable x values. The 52-entry H table is present at indices 0..51, but no guard proving x<52 was established. Neither `x=d` nor `x=effect/item/action selector` is proven; both remain K1 hypotheses with falsifiers.

## KA3 — calls and B24C8

- The one direct caller established for `FUN_800BE5D8` is `FUN_800B50AC`, via JAL at Entry 1 PC `0x800B54F4`. No claim is made that the caller set is complete beyond the searched Ghidra/direct-reference evidence.
- At `0x800B24C8`, the store is `sh $zero,0x2ee($v0)`. The immediately preceding `lw $v0,-0x158c($a0)` at `0x800B24C0` loads the manager pointer from global address `0x8013EA74`. The imported code listing does not provide a containing function boundary or caller for B24C8; wrapper/function entry and caller set remain **TIDAK TAHU**. No participant index should be inferred from this store.

## KA4 and KA5

- KA4: **TUNTAS K4** — `EMULATOR_LAUNCHES=0`; static-only exclusion is explicit.
- KA5: **SEBAGIAN K2** — only a conditional expression `H(x)` is recorded if x is within 0..51 and the relevant helper uses that table. The helper/table indexing relationship and x-to-delta mapping are not proven. No numerical cost formula for d>=2 is established. User-proposed 400/800/1600 were not used, no fitting was performed, and no MATCH/CONTRADICTS label was assigned.

## Status (final interpretation)

- KA0: **SEBAGIAN K3** — commit/run/compile ledger captured; run finalized separately, with analyzer exit 1.
- KA1: **SEBAGIAN K3** — call sites and partial argument slices; B50AC indirect caller and wallet setter unresolved.
- KA2: **SEBAGIAN K3** — 21 constant-address store sites plus three x writer paths; dynamic writers and operational x domain unresolved.
- KA3: **SEBAGIAN K3** — one direct BE5D8 caller; B24C8 function/caller boundary unresolved.
- KA4: **TUNTAS K4**.
- KA5: **SEBAGIAN K2** — conditional H(x) only, no cost formula.

## Remaining TIDAK TAHU

1. Permanent wallet setter and semantic identity of participant record +0x04.
2. Whether either EXE word candidate dispatches FUN_800B50AC, and the complete direct/indirect caller set.
3. Path-specific values for $a2/$a3 at all three requested call sites; semantic contents of loaded $a0/$a1 values.
4. Dynamic/indirect writers to 0x80139EC7, 0x8013EA6E, and 0x8013EB1C; ultimate origins of dynamic stored values.
5. Full reachable operational x set; whether x is d or effect/item/action ID.
6. Whether x is bounded to 0..51 before H lookup; behavior outside that table.
7. Enclosing function, wrapper, caller set, and logical index interpretation for B24C8.
8. Numerical upgrade cost formula for level jumps d>=2.

## Changed files by commit

**Commit 495592eb62ef776fde30d50a96c358e4d2737d3a** (analysis source; parent baseline):
- Added `.github/workflows/ka0-ka5-static.yml`.
- Added `tools/ka-static/RunKA0KA5Static.py`.

**Commit 20b9f58205eaaff375ac266f0cbd55f6d786fcf3** (Actions publication; parent analysis source):
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/ACTIONS_RUN_SUMMARY.txt`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA0_KA5_FINAL_REPORT.md`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA0_LEDGER_ACTIONS.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA0_LEDGER_COMMITS.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA0_LEDGER_SUMMARY.txt`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA0_PUBLISH_COMMIT_FILES.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA0_PYCOMPILE.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA0_SOURCE_COMMIT_FILES.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA1_B50AC_CALLERS.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA1_B50AC_CALLER_WINDOWS.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA1_CALL_ARGUMENT_ORIGINS.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA1_WALLET_HYPOTHESES.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA1_WALLET_STATUS.txt`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA2_GLOBAL_WRITERS.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA2_GLOBAL_WRITER_VALUE_ORIGINS.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA2_H_TABLE_52.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA2_MANAGER_530_X_PROVENANCE.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA2_X_DOMAIN.txt`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA2_X_HYPOTHESES.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA3_B24C8_FUNCTION_V0_CONTEXT.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA3_B24C8_PARENT_CALLERS.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA3_B24C8_WINDOW.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA3_BE5D8_CALLERS.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA3_BE5D8_CALLER_WINDOWS.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA3_BOUNDARY_STATUS.txt`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA4_STATIC_ONLY.txt`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/KA5_SYMBOLIC_COST.tsv`.
- Added `reports/stage1_economy/ka-run-42382353606/attempt-1/cleanup.txt`.

**Finalization commit (this addendum publication):**
- Adds `reports/stage1_economy/ka-run-42382353606/attempt-1/KA0_KA5_FINALIZATION_ADDENDUM.md`.
- Adds `reports/stage1_economy/ka-run-42382353606/attempt-1/KA0_FINAL_RUN_RECONCILIATION.txt`.

No pre-existing repository file was changed by these commits. No Release or protected file was modified.
