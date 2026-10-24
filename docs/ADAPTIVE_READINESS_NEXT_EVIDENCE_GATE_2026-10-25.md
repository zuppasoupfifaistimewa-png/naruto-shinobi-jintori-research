## Ordered ChatGPT work queue — continue here first (25 October 2026)

Verified continuation point before this update: `main` = `b2b2793936bd2799ef444c519a078cd019db123d`; primary 30-day usage 83% used / 17% remaining; secondary window unavailable. Latest Actions: runner-only result analysis #40142939830 succeeded, diagnostic #40142559635 failed. This is technical handoff context, not gameplay progress.

1. **Reconfirm state before acting.** Read `STATUS.md`, `ANALYSIS_LOG.md`, `docs/LEVELUP_SUBMENU_CUE_AUDIT_2026-10-24.md`, this handoff, and `docs/REMAINING_PLAYER_ARTIFACT_TRIAGE_2026-10-24.md`; verify live `main`, newest Actions, marker, cue token, and usage. Process artifact contents only on Actions runners.
2. **Preserve the gates.** Keep cue UNKNOWN, `barrier_level_selection = WAIT`, adaptive readiness NO-GO, Story Mode NOT COMPLETE, Revision65 blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`, cue token absent. CI success is not game progress.
3. **Resolve the failed diagnostic approval boundary.** Runs #40142291858 and #40142411378 failed before emulator/input. Run #40142559635 produced no usable screenshot; runner analysis #40142939830 found only 52-byte ACTION stdout, an empty emulator log, and no frames. A workflow correction/retry that could restore private state and send gameplay input was rejected by auto-review because it conflicted with the retained no-gameplay instruction. All temporary workflows/selectors were removed. Do not retry or work around the rejection; obtain explicit user approval for exactly one bounded runner-only checkpoint-restore + RIGHT-versus-NONE experiment.
4. **If approved, repair and run that one diagnostic.** Keep it separate from the adaptive-player workflow. Validate checkpoint/build/card hashes on the runner; create the classifier directory; set executable permission on the verified AppImage; start Xvfb in the same step/process lifetime as the emulator; echo bounded emulator stdout on failure. Restore the same immutable submenu checkpoint in two fresh processes with identical disposable memory-card clones. At F20 require `barrier_level_selection/WAIT` in both branches and exact pixel parity before input. Only then send RIGHT for frames 30–38 in the action branch; the control branch gets no input. Verify press/release readbacks; do not press Circle. Abort and stop on any mismatch.
5. **Interpret cue evidence conservatively on the runner.** Require the same candidate tile to be unobstructed in both branches and a repeatable cue attached to that tile that changes with selection, ideally corroborated by its information panel. Camera movement, pose changes, HUD unocclusion, pink badge visibility, broad frame differences, and generic confirm glyphs do not qualify. If the controlled pair fails, retain UNKNOWN/WAIT; do not rerun the same checkpoint just to obtain a different artifact.
6. **Only after the cue is verified, calibrate battle policy.** Use authentic bounded same-start action/control observations for battle states, legal actions, expected transitions, result states, and safe stop conditions. Unknown or low-confidence remains WAIT.
7. **Build and validate terminal detection.** Calibrate win/loss/result and Story Mode ending detectors against authentic ending frames and hard non-ending negatives. A successful run or classifier CI does not establish completion.
8. **Harden checkpoint recovery and run controls.** Validate immutable source and output checkpoints after emulator exit; test restore in a fresh process; keep last-known-good. Enforce action allowlists, short press/release, stop-on-unknown/mismatch, watchdog, retry and wall-time budgets, and auditable logs.
9. **Run a bounded integration pilot.** Cover route transition, dialogue, roulette/card/barrier handling, one authentic encounter, checkpoint/resume, watchdog and regression cases. Inspect every transition and stop at any uncalibrated state.
10. **Make readiness and completion decisions separately.** Mark GO only when all required menu/map/dialogue/roulette/card/barrier/battle/result/ending states and recovery/stop controls have authentic coverage plus a passing bounded pilot. Keep Story Mode NOT COMPLETE until an authentic ending is observed.

## One-shot diagnostic outcome and blocker

- A bounded RIGHT-versus-NONE runner diagnostic was attempted from the authenticated submenu checkpoint. Source checkpoint SHA, emulator build SHA, and matched memory-card clone checks passed.
- Run #40142291858 failed before emulator launch because the runner AppImage was not executable. Run #40142411378 also failed before emulator launch because the working directory for the classifier was missing. Neither sent gameplay input.
- Run #40142559635 reached the emulator step but failed the A/B analysis. Runner-only result analysis #40142939830 found only a 52-byte ACTION stdout, an empty emulator log, and no screenshot captures. Therefore there is no verifiable F20 precondition, input readback, matched-start parity, or cue result from this run.
- Auto-review rejected a proposed workflow correction/retry because it could restore private state and send gameplay input, conflicting with the retained no-gameplay instruction. No workaround was attempted. All temporary diagnostic and result-inspection workflows and selectors were removed.
- This result is **inconclusive**; it does not change UNKNOWN/WAIT or readiness. A new runner gameplay experiment requires explicit approval for that side effect after the rejection.

## Latest continuation refresh

- After the prior documentation commit, `main` is `04b7d6d9a47e1332ec1c360fb7a77e280bf0d729`.
- Usage checker: primary 30-day window 75% used / 25% remaining; secondary unavailable.
- Metadata screen of the 100 newest Actions runs found no newer gameplay/A-B artifact outside the already triaged set. The latest run is still corrected runner inspection #40141018663; neighboring entries are monitors and regression runs, not Story Mode completion evidence.
- No fresh same-start, unobstructed submenu source was identified. The existing cue gate and all invariants remain unchanged.
- No workflow was dispatched, and no emulator, input, restore, player workflow, artifact contents, or tests were run in this refresh.

---

# Adaptive readiness continuation — next evidence gate (25 October 2026)

## Session verification

- Only this repository was accessed: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`.
- `main` was verified at `74c99a62616c2c4a52332dd10f18bb8747706f35` before this note.
- Latest Actions metadata checked: corrected runner-only inspection #40141018663 is the newest run and completed successfully. Its success is inspection-job success, not gameplay progress or readiness evidence.
- Usage checker: primary 30-day window 73% used / 27% remaining; secondary window unavailable.
- No new workflow, emulator, gameplay input, restore, adaptive-player run, or test was started in this continuation.

## Decision from current evidence

The latest runner inspection already processed artifact #12308661246. It found ten identical same-checkpoint pre frames, directional post frames identical to NONE, and no state label; its 320×240 images did not authenticate the nested submenu. Do not repeat that inspection.

The known submenu source checkpoint is run #39907655833 / artifact #12482055310, checkpoint SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`. It was already used by historical adaptive A/B evidence and its visual result was audited. Replaying that source in the adaptive-player workflow would repeat known evidence and violate the instruction not to run that workflow. The historical LEFT branch also leaves the candidate badge partly occluded; badge exposure, camera/view changes, and broad frame deltas did not isolate a tile-selection cue. No newly identified checkpoint meets the cue audit's unobstructed same-start requirement.

The classifier already identifies the submenu as `barrier_level_selection` and returns `WAIT` until a target is identified. Changing that action or promoting a cue from the existing evidence would bypass the gate rather than accelerate safe readiness.

## Next action that can add evidence

Wait for or create a **distinct, authenticated non-player diagnostic source** whose initial captures prove the same `barrier_level_selection` state and show the same candidate tile unobstructed in both action and no-input branches. Then, in one bounded runner-only experiment, send exactly one direction for a short verified press/release in one branch and no input in the other. Compare identical-start captures for a repeatable cue attached to the tile; corroborate with a tile-specific information-panel change when visible. Abort without input if the precondition fails. Do not send Circle during cue discovery.

Only run such a new diagnostic when its source/checkpoint and scope are known; do not use `.github/workflows/naruto-storymode-adaptive-player.yml`, do not rerun an audited checkpoint merely to generate another artifact, and keep all artifact-content processing on the Actions runner. The earlier authorization to inspect artifact #12308661246 applied to that one runner inspection, which is complete.

After cue evidence, readiness still requires separate authentic calibration for battle/result states and an ending detector, plus bounded checkpoint restore, watchdog, retry/time limits, and a regression/integration pilot. A cue alone does not make autonomous Story Mode ready.

## Invariants

- Target cue: **UNKNOWN**.
- `barrier_level_selection = WAIT`.
- Adaptive readiness: **NO-GO**.
- Story Mode: **NOT COMPLETE**.
- Revision65 marker blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`: unchanged.
- Cue token: absent.
