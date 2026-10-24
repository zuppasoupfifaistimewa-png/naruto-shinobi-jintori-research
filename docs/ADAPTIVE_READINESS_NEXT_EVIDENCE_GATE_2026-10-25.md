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
