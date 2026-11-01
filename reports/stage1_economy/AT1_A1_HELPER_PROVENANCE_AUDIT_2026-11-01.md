# AT1 — a1 helper provenance audit

Date: 1 November 2026 (Asia/Jakarta)  
Scope: static MIPS disassembly only; maximum evidence level K4. No emulator, gameplay input, savestate restore, or private binary upload was used.

## Status

**TUNTAS — K4 untuk kesimpulan provenance statis.** Kesimpulan nilai register setelah helper: **a1 = TIDAK TAHU**. Bukti menunjukkan tidak ada jaminan bahwa a1 yang masuk ke helper dipertahankan sampai pemanggilan getter; bukti statis yang tersedia tidak menentukan nilai konkret a1 saat getter pertama dipanggil.

## Verified input and source

- DATA.BIN Entry 1 was previously extracted and imported by the successful Step 7 / AQ1 run **41258690146**, job **124707242427**.
- Entry 1: 596,412 bytes, SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`; static candidate base `0x800AD450`. Runtime mapping remains NOT VALIDATED.
- The text-only Ghidra output `entry1-buffer-base-targets.txt` contains function bodies for `0x80105BCC` and `0x801052E8`, including raw instructions and their call relationship. The import was explicitly marked static and not a runtime mapping proof.
- The main-executable helper audit **41259079319**, job **124708383189**, exported the raw bodies for both `0x80043F18` and `0x80043AB8`. The job completed successfully and the output file contains both function sections. Its old publication validator incorrectly returned INCOMPLETE because its end-of-file regex used a literal `\\Z`; that parser was corrected in workflow commit `8e2eeed39fd36b5224c1e660daed812ccf2365dc`. A corrected Actions run was started separately.

## Caller → helper → renderer → getter

1. In `FUN_801052E8`, PC `0x801053BC` calls `0x80105BCC`; the delay slot at `0x801053C0` is `move a3,s5`.
2. Inside `0x80105BCC`, the original incoming `a1` is used at `0x80105C40` (`addiu a1,a1,0x10`) and stored to the local structure at `0x80105C44`. Then `0x80105C4C: move a1,a3` replaces the argument register with the incoming `a3` value before `0x80105C50: jal 0x80043F18`; the call delay slot is `li a2,1`.
3. `0x80043F18` copies its incoming `a1` to callee-saved `s3` at `0x80043F28`, builds render data, and calls `0x80043AB8` at `0x800443DC`. Its epilogue restores `s4,s3,s2,s1,s0`, but does not restore `a1`.
4. `0x80043AB8` copies its incoming `a1` to `s2` at `0x80043AC8`; it restores `s2` on return. This does not create an ABI preservation guarantee for caller-saved `a1` across the call chain.
5. Back in `0x80105BCC`, after the nested call, the code sets `v0=1` at `0x80105C58`, restores `ra`, and returns. It does not reload or restore the caller's original `a1`.
6. The caller resumes at `0x801053C4` and immediately calls getter `0x800138EC`. Its delay slot `0x801053C8: move a0,s3` establishes `a0=s3`. No instruction between the helper return and this getter call reassigns `a1`.

## Interpretation

- The incoming `a1` is demonstrably repurposed inside `0x80105BCC` before calling the renderer.
- The renderer/helper call chain is not required by the MIPS calling convention to preserve `a1`; the observed epilogues do not restore it.
- Therefore, do **not** label the first getter's `a1` as the original incoming `a1`, as `a3`, or as a valid record index. Its concrete value at `0x801053C4` is **TIDAK TAHU** from the static evidence.
- This supports the existing AT1 getter report's conservative treatment of the caller-saved `a1` on the BLTZ-taken path to the second getter. It does not revise the separate fall-through-path observation that loads a manager pointer into `a1`; that pointer must not be assumed to be a valid index.

## Boundaries

This is a static register-provenance conclusion, not a gameplay/economy semantic conclusion. The import base `0x800AD450` remains a candidate; dynamic mapping and the exact runtime value of `a1` are **TIDAK TAHU**. No streamer-spoken formula was used.

## Evidence files

- `reports/stage1_economy/aq1-run-41258690146/attempt-1/entry1-buffer-base-targets.txt`
- `reports/stage1_economy/aq1-run-41258690146/attempt-1/input-identity.txt`
- `reports/stage1_economy/at1-helper-a1-audit-run-41259079319/attempt-1/seed-helper-detail.txt`
- `reports/stage1_economy/AT1_STATIC_FINAL_REPORT_2026-11-01.md`
- `reports/stage1_economy/AT1_GETTER_CALLS_RECONCILED_2026-11-01.tsv`
