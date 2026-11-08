# MA0–MA5 follow-up static reconciliation

## Scope and source identity

This is a text-only follow-up to MA run 42429723141. It does not change the run's own results or promote incomplete scans to complete evidence.

- MA run source SHA: `66f5672e19a0c624ca787b482fcaa298822b9de5`
- EXE SHA-256: `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`
- Entry 1 SHA-256: `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`
- KA cross-check source SHA: `819303553e51b0499c81e94c197616e454cfb2a0`
- KA used the same EXE and Entry 1 SHA-256 values above. It is corroborating static evidence, not the MA analyzer's own count.
- Runtime/emulator/game launches: `0`.

## MA1 — scene-record table

The anchor-containing stride-`0x1C` record run begins at `0x800558A4`, not at the anchor itself. The prior stride position `0x80055888` did not satisfy the record pattern. The published TSV contains 31 consecutive records, including the `TITLE` record at `0x800558A4` followed by `LOGO` at the user anchor `0x800558C0`.

**The right boundary is not established.** The run scanned only through `0x80055BFC`; the test at the next stride position `0x80055C08` also returned a valid record. Therefore the table has at least one further record after the 31 records in the TSV. It is incorrect to call `0x80055C08` the end, and no final end address is claimed here.

The record file itself contains all 31 records found in the bounded scan:
`MA1_SCENE_RECORDS.tsv`.

Code-user scan results are narrow:
- Six instructions in EXE form address `0x800558A8` (the six rows in `MA1_SCENE_CODE_USERS.tsv`).
- The scan did not establish a complete indexed table-dispatch chain, a confirmed `index*28` computation, or the subsequent `jalr/jr` table dispatch. Zero candidates in the scale TSV is **not** proof no such code exists outside the recognizer's patterns.
- The pointer-word TSV lists data words equal to the scene-record function pointer values; those words alone do not prove dispatch.

Four requested scene addresses have manual prologs at their targets and a return site each:
| Target | Function range | `jr $ra` |
|---|---|---|
| `0x800B1E88` | `0x800B1E88..0x800B2A57` | `0x800B2A50` |
| `0x800B50AC` | `0x800B50AC..0x800B5787` | `0x800B5780` |
| `0x800B5020` | `0x800B5020..0x800B50AB` | `0x800B50A4` |
| `0x800B2A58` | `0x800B2A58..0x800B501F` | `0x800B5018` |

For `0x800B24C8`, Ghidra and the manual backward prolog both place it within `0x800B1E88`; there is no `jr $ra` or other stack-frame prolog between the parent prolog and target. The scene table has one pointer word to `0x800B1E88` at `0x80055900`. The exact-target direct-call/pointer search found no pointer to the interior address `0x800B24C8` and no direct call to that interior address. This supports the containing-function identification, but does not close all computed indirect callers.

For `0x800BE5D8`, two recorded rows represent the same direct call instruction at `0x800B54F4` from `FUN_800B50AC` (one disassembly row and one Ghidra reference). There is one unique direct call PC, not two separate call sites. Computed indirect callers remain **TIDAK TAHU**.

All six requested `$a2/$a3` call-site origins at `0x800F5F54`, `0x800B54DC`, and `0x800F5EBC` remain **TIDAK TAHU**. The current analyzer stopped at control-flow boundaries before finding a reaching definition. The prior LA reaching-def report also explicitly marks them incoming/no static reaching definition. No guessed constants or memory origins are substituted.

Wallet-authoritative setter remains **TIDAK TAHU**. See `MA1_WALLET_HYPOTHESES.tsv` for three competing candidates and their supports/falsifiers; no candidate is promoted to fact.

## MA2 — selector writers and x provenance

The MA analyzer's own selector table found 13 static `sh` writers to `0x8013EA6E`; the earlier KA static pass on the exact same EXE/Entry 1 hashes enumerated 14. The cross-check reveals one missed PC in MA's current output: `0x800E3B1C`.

Cross-run reconciled census:
- 14 `sh` writers to `0x8013EA6E): 12 source values loaded by `lhu` from `0x8013EA88`, and 2 loaded by `lhu` from `0x80139EFC`. These are dynamic memory values, not constants.
- 3 `sb` writers to `0x8013EB1C`: at `0x800D77C4` and `0x800D7D4C`, the source register is statically established by `lui $v0,0x8014`; the byte actually stored is therefore `0x00`. At `0x800E4840`, the source value in `$v0` remains **TIDAK TAHU**.
- 4 observed `sb $zero` clears of `0x80139EC7`: `0x800E8A8C`, `0x800E93D4`, `0x800EB410`, and `0x800EC84C`. Each stores `0x00`.

Each reconciled store and its source evidence is tabulated in `MA2_SELECTOR_WRITER_CROSSCHECK.tsv`. Supporting raw static inputs are the KA `KA2_GLOBAL_WRITERS.tsv` and `KA2_GLOBAL_WRITER_VALUE_ORIGINS.tsv` files under run 42428060234. The MA output remains authoritative for what its own recognizer found; the cross-check only fills the documented missed writer and refines source provenance where separate trace evidence exists.

The byte read at `0x800D49D0` is computed from:
`MEM32[0x8013EA74] + 0x10 + MEM8[0x8013EB1C] + 144*MEM16[0x8013EA6E]`.
The `144*I` multiplier is statically visible as `(I*9)<<4`. The selected cell is read with `lbu` and placed into manager+`0x530` with `sw`; therefore the loaded x value is zero-extended and constrained to `0..255` at this read site.

That does **not** prove how all cells in this dynamic matrix are written. The MA store census found no writer whose expression matched its three global-address anchors; this is a recognizer result, not a proof of no writers. Alias-derived and dynamically based store addresses remain **TIDAK TAHU**. Consequently:
- H1 (`x=d`) is not established or falsified.
- H2 (`x=effect/item/action ID`) is not established or falsified.
- The three `manager+0x530` write paths are not semantically closed; the two copies from `0x80139EC7` are not sufficient to label x globally as an effect ID.
- The formula for a level jump `d>=2` remains unknown.

## MA2(c)/MA5 — helper bound and lookup

At `0x800154D4`, the function is exactly:
`lw $v0,0x118($gp); jr $ra; nop`.
It returns the 32-bit value loaded from `0x118($gp)`, not a compile-time constant. Whether that dynamic value equals 52 is **TIDAK TAHU**. The 52 visible H-table entries (indices 0..51 in the earlier table dump) do not by themselves prove the value returned by this function.

At `0x8001552C`, the helper compares x with that dynamic bound using unsigned `sltu`. When x is below the bound, it loads the word at table base `0x80055CEC + 16*x + 8`; this is the conditional expression `H(x)=u32[0x80055CF4+16*x]`. When the comparison falls through to `0x80015564`, `move $v0,$zero` sets the returned value to zero through the shared epilogue.

The bound and x-domain precondition are therefore dynamic/unresolved; this is not evidence that the helper limit is 52 or that every x belongs to the 52 visible entries.

## MA0 integrity and publication

The MA run completed successfully as an Actions job, with:
- Actions inventory: 1249/1249 runs across 13 pages; 81 scheduled; no active runs at final census.
- Python compilation: 68/68.
- File-offset/raw-byte/decode validation: 15,619/15,619 rows; 15,517 decoded instructions; zero failures.
- Ghidra EXE and Entry 1 steps: exit 0.
- Analyzer: exit 0; cleanup: pass; emulator/game/BIOS/savestate launches: zero.
- Final-parent ledger includes the baseline commit and all commits through the source commit immediately before publication: 5 total (4 human, 1 bot). The MA publication commit itself is excluded.

MA0 remains **SEBAGIAN** because the aggregate excerpt audit found a 68-byte contiguous run at Entry 1 `0x800F5D8C..0x800F5DCF`. Its provenance is:
- `LA2_GLOBAL_INPUT_ACCESSES.tsv` contributes the 4-byte row at `0x800F5D8C`.
- `LA0_JA_REPLACEMENT_CALLER_WINDOWS.tsv` contributes the following 64-byte window starting at `0x800F5D90`.
- The overlapping MA row at `0x800F5DA8` is already contained within that existing span.

Those two old LA files are not the two oversize excerpt files the original MA instructions authorized deleting. They were not modified here because the instruction prohibited edits/deletions beyond the two named LA files. The 68-byte violation is therefore reported, not hidden. The aggregate audit also recorded zero conflicting duplicate addresses.

## Final assessment

- MA0: **SEBAGIAN K2** — all inventory/compile/decode checks pass, but the aggregate 64-byte ceiling is not met.
- MA1: **SEBAGIAN K3** — 31 records enumerated; left boundary supported; right boundary and table dispatch/indexed users not closed; wallet and requested call arguments unresolved.
- MA2: **SEBAGIAN K3** — key reader/address formula is strong static evidence; writer cross-check is reconciled across same-image hashes; dynamic matrix writer closure and x semantics remain unresolved.
- MA3: **SEBAGIAN K3** — B24C8 parent identified inside B1E88; indirect caller closure incomplete; BE5D8 has one unique direct caller PC.
- MA4: **TUNTAS K4** — this phase was static-only.
- MA5: **BELUM K1** — no numerical upgrade-cost formula for `d>=2`.

No runtime facts, fitting, or assumed price progression are used.
