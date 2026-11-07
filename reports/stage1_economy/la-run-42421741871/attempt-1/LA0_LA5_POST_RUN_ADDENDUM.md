# LA0-LA5 post-run correction addendum

Final Actions run: 42421741871; job la0-la5-static (128552266995), completed/success; analyzer exit 0. This addendum records corrections verified by direct instruction rows after the main report was published.

- FUN_800BE5D8 begins with its own prolog at the target: 0x800BE5D8 addiu sp,sp,-0x30; 0x800BE5DC sw ra,0x2c(sp). The earlier backward-only heuristic candidate 0x800BE0E4 was not the function entry. Direct caller: 0x800B54F4 jal 0x800BE5D8 in FUN_800B50AC.
- B50AC data-word positions 0x80055904 and 0x80055920 are each at +4 of record candidates beginning at 0x80055900 and 0x8005591C; +8 in both is 0x800B5020. Thus 0x1C is a structural candidate stride, not proof of an indexed dispatch table. No resolved code user was found.
- The helper 0x8001552C compares $s0 against the return from 0x800154D4 using sltu at 0x80015540 and branches at 0x80015544 before indexing the table at 0x80055CEC + 16*x + 8. Whether the bound function returns 52 is TIDAK TAHU.
- The two removed JA files are replaced by LA0_JA_REPLACEMENT_EXCERPTS.tsv (6 nonduplicate FUN_80014F10 rows) and LA0_JA_REPLACEMENT_CALLER_WINDOWS.tsv (112 rows in seven groups of 16 instructions / 64 bytes). The B54DC context is covered by the retained KA3_BE5D8_CALLER_WINDOWS.tsv; three overlapping F5F1C/F5F2C/F5F54 contexts were merged to one 64-byte excerpt. Aggregate union maximum across all retained JA/KA TSV rows plus replacements: 64 bytes.

Changed files in this correction publication:
- Updated reports/stage1_economy/la-run-42421741871/attempt-1/LA0_JA_REPLACEMENT_AUDIT.txt
- Updated reports/stage1_economy/la-run-42421741871/attempt-1/LA1_B50AC_TABLE_ASSESSMENT.txt
- Updated reports/stage1_economy/la-run-42421741871/attempt-1/LA3_BE5D8_BOUNDARY_STATUS.txt
- Updated reports/stage1_economy/la-run-42421741871/attempt-1/LA0_LA5_STATIC_REPORT.md
- Added reports/stage1_economy/la-run-42421741871/attempt-1/LA0_JA_REPLACEMENT_CALLER_WINDOWS.tsv


## Subsequent static correction — target prolog recognition

A code review found that the backward-only `find_prolog()` search begins at `PC-4`; it therefore skipped a prolog located exactly at target `0x800BE5D8` and returned the preceding candidate `0x800BE0E4`. The helper now checks the target PC and next instruction first for `addiu $sp,$sp,-N` followed by `sw $ra,...($sp)`, then falls back to the backward scan. The published `LA3_BE5D8_MANUAL_FUNCTION.tsv` target-context rows now identify `0x800BE5D8` as the function entry, consistent with the direct instruction evidence in `LA3_BE5D8_BOUNDARY_STATUS.txt`.

This is a source/report-only correction. No Actions run was started after this edit, to preserve the one-run budget; the corrected helper has **not** been executed in a new run. The prior run summary remains a record of run `42421741871`, not validation of this post-run code correction.

Changed files in this correction commit:
- `tools/la-static/RunLA0LA5Static.sh`
- `reports/stage1_economy/la-run-42421741871/attempt-1/LA3_BE5D8_MANUAL_FUNCTION.tsv`
- `reports/stage1_economy/la-run-42421741871/attempt-1/LA0_LA5_POST_RUN_ADDENDUM.md`


## Final checked-out HEAD ledger reconciliation

The inclusive ledger is extended through the verified pre-publication HEAD snapshot `c57b11d6075ba52a8165e62f1c745265e92ec4e4`: **25 commits total (23 human, 2 bot)**, counting from baseline `5a4cd3167beb3a0dba61a48bc6471496ec6fe34f` inclusive. The source snapshot used by LA analysis remains `191492f06ffebaec0a34cbfe1f131790f0d89627`: 9 commits (8 human, 1 bot). The classification is heuristic based on author identity/email. The repository Actions census remains 1,245 runs over 13 pages for all events (81 scheduled), and 66/66 tracked Python scripts passed `py_compile` in run `42421741871`. The commit publishing this updated ledger is excluded because it cannot count itself.

Changed files in this ledger reconciliation commit:
- `reports/stage1_economy/la-run-42421741871/attempt-1/LA0_LEDGER_COMMITS_FINAL_HEAD.tsv`
- `reports/stage1_economy/la-run-42421741871/attempt-1/LA0_LEDGER_COMMIT_COUNTS.tsv`
- `reports/stage1_economy/la-run-42421741871/attempt-1/LA0_LEDGER_SUMMARY.txt`
- `reports/stage1_economy/la-run-42421741871/attempt-1/LA0_LA5_STATIC_REPORT.md`
- `reports/stage1_economy/la-run-42421741871/attempt-1/LA0_LA5_POST_RUN_ADDENDUM.md`
