# JA0-JA5 static report
Baseline inklusif: 09c071e6c496b61b0689499a641faa3aa482b145
Source SHA: 570f19c472b5238349909873ac6c68afc84359df
EXE SHA-256: a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569
Entry 1 SHA-256: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a
Runtime status: NO EMULATOR / NO GAME / NO BIOS / NO SAVESTATE / NO RAM SNAPSHOT.

## Status
JA0=TUNTAS K4; commits=2; all-event runs=1; scheduled=0; py_compile=65/65.
JA1=SEBAGIAN K4 static for FUN_80014F10 body; wallet-authoritative setter TIDAK TAHU. Direct/code caller rows=13; target-14F10 callers=1.
JA2=SEBAGIAN K3; writers traced=3/3; dynamic x domain TIDAK TAHU; x=d not proven.
JA3=SEBAGIAN K3; zero-writer targets=2/2; actual parent function / v0 index status is reported per target.
JA4=TUNTAS K4; no runtime execution.
JA5=SEBAGIAN K3; only a conditional x=0 reset value is numeric; all dynamic cases remain symbolic.

## JA0 — ledger
See JA0_LEDGER_COMMITS.tsv, JA0_LEDGER_ACTIONS.tsv, JA0_PYCOMPILE.tsv, JA0_LEDGER_SUMMARY.txt and JA0_SOURCE_COMMIT_FILES.tsv.
The final IA baseline ledger is copied as complete TSVs: 10 commits (7 human, 3 bot), 6 all-event runs, 0 scheduled, 64/64 py_compile. See JA0_IA_FINAL_LEDGER_COMMITS.tsv, JA0_IA_FINAL_LEDGER_ACTIONS.tsv, JA0_IA_FINAL_PYCOMPILE.tsv and JA0_IA_FINAL_LEDGER_SUMMARY.txt.

## JA1 — function and caller analysis
FUN_80014F10 body is split into JA1_FUN_80014F10_BODY.tsv excerpts of at most 16 instructions (64 bytes) each.
Call sites, exact JAL words, LUI+ADDIU/ORI pairs, raw pointer-word candidates and argument origins: JA1_CALL_SITES.tsv and JA1_EXACT_JAL_WORDS.tsv; contiguous windows: JA1_CALLER_WINDOWS.tsv.
Participant field +4 manager-backed census: JA1_RECORD_PLUS4.tsv.
The function computes 0x80070F34 + owner*0xB4, reads the current word, compares with argument a1, and writes a1 only when it is greater. The instruction-level proof is the 14F10 body TSV; it is not the participant +4 setter. Wallet-authoritative meaning remains TIDAK TAHU.
Decompilation normalized per instruction: JA1_FUN_80014F10_DECOMPILATION.tsv. Competing hypotheses and falsifiers: JA1_HYPOTHESIS_SUPPORT.tsv and JA1_HYPOTHESIS_FALSIFIERS.tsv.

## JA2 — manager+0x530 provenance
Per-site backward slices: JA2_X_ORIGIN.tsv; summary: JA2_X_SITE_SUMMARY.tsv; callsites to setter/writer functions: JA2_FUNCTION_CALLERS.tsv.
Table H, all 52 static entries: JA2_H_TABLE_52.tsv. Reachable-index conclusion: JA2_H_REACHABLE.tsv.
D49D8 source is a dynamic load; EC844/EC868 are masked dynamic values if their stores execute. The dynamic upstream inputs and full runtime-reachable x set are TIDAK TAHU. The literal zero store is a reset value, not proof that x=0 is an active delta.
Hypotheses x=d versus effect/item are K1 and include at least two instruction supports plus falsifier in JA2_HYPOTHESES.tsv. Neither is proven.

## JA3 — zero writer parents and index
Function manager, incoming references, v0 origin and participant-index conclusion are tabulated in JA3_ZERO_WRITER_CONTEXT.tsv. Instruction evidence windows and v0 definitions are in JA3_ZERO_WRITER_EVIDENCE.tsv. If Ghidra reports the site itself as a function entry, that does not alone prove this is the logical caller's function boundary; unresolved cases remain TIDAK TAHU.

## JA4 — runtime exclusion
No game, emulator, BIOS, savestate, runtime execution, or controlled input was used in this stage.

## JA5 — symbolic only
JA5_SYMBOLIC_PREDICTIONS.tsv uses only the literal x=0 reset store as a conditional case and otherwise retains H(x) symbolically. No fitting and no mapping x=d is asserted.

## TIDAK TAHU
- Wallet-authoritative setter and whether participant +4 is the permanent wallet.
- Whether any JALR / pointer-table candidate dispatches a relevant function at runtime.
- Dynamic origins and complete domain of manager+0x530, including the three requested writer values.
- Whether x is delta-level d or an effect/item/action selector.
- Actual enclosing function/caller for each zero-writer when the Ghidra function boundary remains split or missing.
- Effective manager base and participant index for the two zero-writer $v0 stores.
- Operational reachability of x=0 following the reset write.
- Any numeric upgrade cost for d>=2.
