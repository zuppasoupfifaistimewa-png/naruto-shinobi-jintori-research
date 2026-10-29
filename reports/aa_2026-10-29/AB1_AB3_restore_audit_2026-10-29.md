# AB1–AB3 audit — 2026-10-29

Scope: repository-only evidence review. No ISO, BIOS, savestate, RAM dump, or screenshot was uploaded or committed by this report. Story Mode completion is NOT VERIFIED.

## Results

### AB1(a) — GDB harness and log excerpts: SEBAGIAN, K4 for workflow defect; runtime diagnosis BELUM, K0

Reviewed workflow `.github/workflows/aa1-restore-gdb-diagnostic.yml` at `64be99b0ea2d`.

Directly visible harness defects:
- GDB commands use `-ex 'echo \\n=== AA1 NATIVE BACKTRACE ===\\n'`; shell single quotes pass the backslash sequences literally, so this does not reliably request actual newline delimiters.
- The report filter includes selected `#N` frames and signal text, but truncates to `tail -n 90`; it does not preserve the required first 40 and last 250 lines of both GDB and PCSX logs.
- It does not explicitly run `info threads`, `thread apply all bt 12`, `x/3i $pc`, `info registers rip rsi rdi rcx`, or capture `info proc mappings` around the PC.
- It therefore cannot yet meet the requested diagnostic capture contract.

No AA1 diagnostic run output was retrieved for this audit, so there is no verified target/control native crash stack to attribute the restore failure to. I have not changed or dispatched the workflow in this report.

### AB1(b) — top-level protobuf comparison: BELUM, K0

Known file sizes from the task/checkpoint records: target 21,163,286 bytes; control 21,162,546 bytes; delta +740 bytes. This arithmetic is verified, but no raw protobuf bytes were downloaded or parsed here. Field tags, field lengths, per-field SHA-256 values, and the field responsible for the delta are **TIDAK TAHU**. Do not infer that the 740-byte difference itself caused restore failure.

### AB1(c) — checkpoint provenance and run comparison: SEBAGIAN, K4

Run #39262213468 job #118092519254 completed successfully. Its log explicitly records `STORY_CHECKPOINT_SAFE_POINT frame=10055 save_ok=true reason=stable_non_dialog`, then `STORY_CHECKPOINT_FRAME=10055`; it uploaded checkpoint artifact #12196796917 (not expired at audit time; expiry 2026-11-02T15:03:35Z) and Memory Card artifact #12196517326 (not expired at audit time; expiry 2026-11-02T15:03:37Z). The run is evidence of a checkpoint being saved, not evidence that this raw target state restored successfully. The older run's “frame 5999” detail was not independently established from the excerpts examined here.

Run #39867730674 job #120134061270 downloaded/validated its source checkpoint and Memory Card, ran the adaptive observe-decide-act-verify-checkpoint loop, and ended with `corrupted size vs. prev_size`, `ADAPTIVE_SESSION_EXIT cycle=1 code=134`, and step failure exit 92. Artifact #12464258211 remains available until 2026-11-05T22:51:03Z. This indicates a heap-corruption/abort symptom in that adaptive run, not proof that the AA1 target savestate loaded successfully there. No successful target-state load event was found in the inspected log excerpts.

Run #40844474886 is explicitly cold-boot only: `checkpoint_load=NO; cold boot only`. Three replay attempts ended with exit code 124; run 1 reports frame 5999 capture timeout, then emulator exited before frames 8999, 9030, and 9105. This run cannot be used as a savestate-restore failure reproduction because it never attempted to restore a savestate. It differs materially from #39262213468, which ran through VSync 10055 and saved a checkpoint. Exact complete flag/step-by-step comparison remains incomplete.

### AB1(d) — anonymous release-asset access and exposure mitigation: BELUM, K0

The current repository is public. The workflow source uses authenticated `GH_TOKEN` to fetch Release asset IDs 647346873 (game BIN), 652373928 (SCPH-7502 BIOS ZIP), and 686794219 (raw savestate). That proves authenticated workflow access only; it does **not** establish whether anonymous `curl` can download them. The anonymous HTTP checks could not be completed through the available web fetch path. Do not claim private/public status for these assets without the requested unauthenticated HTTP status/redirect test.

No Release visibility changes were made. No asset was deleted, and no hash evidence was altered.

## AB2 — LCG / write watchpoints: NOT RUN, K0

Gate not satisfied: there is no verified stable restore plus a no-input screenshot independently showing the board/roulette phase from the target or control. No Lua breakpoint was run, no input was injected, and no LCG exponent k was calculated. The existing fail-closed cue remains UNKNOWN/WAIT. Do not run AB2 until the gate is met.

## AB3 — function/state tracing and static header rule: BELUM, K0

No run was made for Exec breakpoints at 0x8002DEC4 and 0x8002DFE4. Values for a0, [a0-4], and state 0x800A2918 offsets +0x8/+0xC before/after return are TIDAK TAHU. “payload+8” and “state+8” are not interchangeable.

The requested static reads at [0x801CEF04], comparison against 0x16C, slot 0x8013A554 → 0x801CEF08, and disassembly quote for func_80035B08 were not re-extracted from a pinned text artifact in this pass; results remain TIDAK TAHU.

## Final gate

- AB1: SEBAGIAN; primary root cause of target restore failure remains UNPROVEN.
- AB2: BELUM; gate closed.
- AB3: BELUM.
- Story Mode: NOT VERIFIED COMPLETE.
- Public binaries/private checkpoint exposure: unresolved; anonymous access needs a real curl check before any mitigation decision.
