# LIVE ADDENDUM — CFG-aware SSA trace, 27 Oktober 2026 21:41 WIB

Run [#40522772847](https://github.com/zuppasoupfivaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40522772847) completed/success at 21:38:32 WIB. Artifact #12741234990, 234.210 B, ZIP SHA-256 `7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9`. New script exports high-level SSA/P-code and CFG block IDs for functions `0x8012C544` and `0x8012CACC`; detail report [STEP6_CFG_SSA_DATAFLOW_AUDIT_2026-10-27.md](STEP6_CFG_SSA_DATAFLOW_AUDIT_2026-10-27.md).

The first function reads `+0xB30) and `+0xB38`, adds them and writes `+0xB40`; it is also a guarded initialization path that clears several fields, writes helper output to `+0xB2E/+0xB2F), sets `+0xB4A=0x1E) and marks `+0xA1C=1). Second function's `+0xB44) consumer is under a branch/merge. SSA helps follow value definitions across basic blocks but traces to indirect/address-tied definitions at pointer slot `0x8013A554`; alias/runtime pointer value remain unresolved. Candidate base `0x800D0000) remains hypothetical. Step 6(a) partial, 6(b) blocked, 6(c) partial, 6(d) unknown.

---

# Step 6 — bounded register/value provenance audit (27 Oktober 2026)

## Checkpoint and reproducibility

- Repository: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`, branch `main`.
- Scanner change: commit [`0afc0eec4a5c12e4df5a17c771c8b0d28d7a99dd`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/0afc0eec4a5c12e4df5a17c771c8b0d28d7a99dd), source blob `54a957f692f252d086c36da7de9481bc75badac9`.
- Static scan: [GitHub Actions #40511758146](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40511758146), **completed/success** at 20:25:48 WIB on 27 October 2026. The job's 14 steps all completed successfully, including analysis, private-workspace cleanup, text-only validation and artifact upload.
- Artifact [#12737611770](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40511758146/artifacts/12737611770): `step6-resource-field-static-scan`, 229,233 bytes, API digest / local SHA-256 `b84ff017cdbefb8ece6d04a7c8bef66b3fdc27b61412e91e10cc01485225b126`; expiry 10 November 2026 20:25:35 WIB.
- The artifact was downloaded for validation; local SHA-256 matched API digest. ZIP contains six text/log files only: `disc-extraction.log`, `field-offset-scan.txt`, `ghidra-headless.log`, `input-identity.txt`, `resource-profile.txt`, and `scan-result.txt`. Reported `text_only_output_count=6`, `private_binary_in_artifact=no`, and `STEP6_PRIVATE_CLEANUP=PASS`.
- Input identity validation reports DATA.BIN 66,015,232 bytes, entry 1 at file offset `0x10BB000`, size 596,412 bytes, SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`; extraction inputs were removed before Ghidra execution.

## New code path and actual fixture results

`tools/step6/ExportStructOffsetAccesses.java` now emits an additional conservative backwards trace of the value used as each recognized memory operand's base register. Within one decoded function and a bounded linear history, it recognizes a limited set of MIPS value-building operations such as `lui`, `ori`, `addiu/addi`, `move`, `addu`, logic operations and `sll`. It emits a constant only where that limited expression can be evaluated; otherwise it marks loads, undefined values, function boundaries, control-flow boundaries and depth/cycle limits explicitly. This supplements, but does not replace, the existing limited `move)-alias hint.

The new fixtures executed in the successful Ghidra scan and emitted:

- `memory_displacement_parser_fixture=PASS sample=sb_v0,0x2e9(v1)`
- `register_provenance_address_constructor_fixtures=PASS cases=lui_ori_addiu_sign-extension`

The address-construction fixture verifies four concrete arithmetic expectations: `lui 0x800D → 0x800D0000`, OR-composition with `0x0B30 → 0x800D0B30`, signed `addiu` with `0xFFFC → 0x800CFFFC`, and sign-extension of `-0x3C → -60`. These are tool fixtures, not observations of a runtime resource base.

## Evidence added by this run

- The scan still traversed **98,357 decoded instructions** in the candidate entry-1 Ghidra view and emitted the direct-displacement inventory between explicit BEGIN/END markers.
- Counts match the prior direct-operand census for the four priority offsets: `+0xB30` one read/no writes; `+0xB38` one read/no writes; `+0xB40` no reads/one write; `+0xB44` one read/one write.
- Raw instruction bytes and dataflow remain: `0x8012C634 lw v0,0xB30(a0)` (`30 0B 82 8C`), `0x8012C638 lw v1,0xB38(a0)` (`38 0B 83 8C`), `0x8012C640 addu v0,v0,v1` (`21 10 43 00`), and `0x8012C644 sw v0,0xB40(a0)` (`40 0B 82 AC`). At `0x8012C604`, `sw zero,0xB44(v0)` (`44 0B 40 AC`) is in the delay slot of `jal 0x80012AC0`; at `0x8012CB14`, `lw a2,0xB44(v1)` (`44 0B 66 8C`) forwards the loaded value to argument `a2) before a candidate call to `0x8001B364`.
- At the `+0xB30/+0xB38/+0xB40` access group, `a0` is loaded at `0x8012C628` by `lw a0,-0x5AAC(s0)` (the role of `s0` is not established). The new backwards trace terminates at a control-flow boundary while trying to establish `s0`'s source. At the `+0xB44` read, tracing `v1` hits the branch boundary at `0x8012CAF8`. These are concrete examples of why the new trace does **not** establish a complete object/base identity.

## Acceptance status and explicit limits

- **TERVERIFIKASI — tool behavior:** the bounded address-construction fixtures passed in the actual scan; the decoded-view direct memory-operand census remains present and the existing priority-offset counts were reproduced.
- **TERVERIFIKASI-STATIS — operations only:** the four priority offsets have the read/write/dataflow described above within the candidate entry-1 view.
- **HIPOTESIS:** DATA.BIN entry-1 base `0x800D0000).
- **UNKNOWN/BLOCKED:** actual runtime base and relocation; full effective-address reconstruction across branches/calls; global reader/writer and alias closure; split-immediate or indirect-pointer coverage outside the current bounded resolver; undecoded/inaccurately bounded regions; identity and semantic meaning of fields.
- The resolver is explicitly not a control-flow graph/dataflow engine, does not propagate values across branch/call boundaries, and is not proof of whole-program aliasing. Ambiguous values remain symbolic or unresolved. No game/emulator was executed, no gameplay input was sent, and no savestate was restored.
- **Step 6(b) remains BLOCKED; Step 6 overall remains SEBAGIAN.** No field is newly labelled Chakra, cost, barrier, turn, level-up, victory or loss. Step 7 runtime resource mapping, Step 8 rule semantics and other open criteria are unchanged.

## Next evidence gate

Before promoting Step 6(b), a subsequent analysis must cover effective-address-building instructions and indirect bases across control-flow boundaries with explicit coverage limits or a suitable control-flow/dataflow engine, and reconcile those results with raw MIPS call/data references. For Step 7, do not repeat the old no-hit target `0x800AD454` absent new static reachability evidence. The latest full criterion matrix is `docs/STEP4_10_LIVE_RECONCILIATION_2026-10-27.md`.
