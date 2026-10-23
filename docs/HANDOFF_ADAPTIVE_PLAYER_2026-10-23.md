# Adaptive Story Mode player — checkpoint and next steps (23 October 2026, 07:03 WIB)

## Status

**Story Mode is NOT complete.** No authenticated ending/results screenshot has been verified. The adaptive player is a checkpoint-based prototype; unattended chaining through the full Story Mode is not yet implemented or verified.

- Last player test: [run #39872449049](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39872449049), revision 50, succeeded. It restored a checkpoint in a fresh process, captured five real external-X11 frames, sent DOWN, later skipped visible Iruka dialogue with START, and reached a three-card-back overlay. This was partial progress only.
- Candidate output checkpoint from that run: artifact `naruto-storymode-adaptive-player-private`, file `adaptive-cycle-01-f180.sstate`, 21,162,772 bytes, PCSX-Redux SaveState v4, SHA-256 `017c6601ad71f7e420cc5406f20c68367497c416663f07065a862f1484b2c9f7`. **Not independently restored and not promoted.**
- Restore-only hard guard was added to `.github/workflows/naruto-storymode-adaptive-player.yml` in commit `0ddc5fb879ea20e575a640fa2207f8fc10c9bdce`. `RESTORE_TEST=1` now blocks every call to the central `sendAction` before button lookup/pad mutation, including normal frame-30 actions and the direct START dialogue path. The workflow requires five authentic captures, checks for zero button-press events, and records the blocked calls.
- Regression test was added in commit `da728ffd7b9b80da7dbbdefb712d8b0be8ced81a`. [Regression run #39875557447](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39875557447) completed successfully. This proves the code/static regression gate passed; **the no-input guarantee has not yet been exercised in an emulator restore-only run**.
- Direct visual review of the private authentic `C01-F180.png` from run #39872449049 confirms three card backs over the board and a pink Chakra icon marked `60`; the card backs show `忍` (shinobi/ninja). In ROI x=370..930, y=220..530, the measured bright-white ratio is 0.1974 and low-chroma-gray ratio is 0.2083, exceeding the classifier thresholds 0.12 and 0.16. This supports the detector calibration but does not yet prove runtime classification or card-selection behavior; revision51 must show `card_selection` / WAIT from a fresh restored process. Do not select a card or send Circle based only on the synthetic test.

## Immediate next operation — revision 51 restore-only

Use the only permitted repository, `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. Update `experiments/.run-storymode-adaptive-player` to:

```
MODE=ADAPTIVE
SOURCE_RUN=39872449049
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=017c6601ad71f7e420cc5406f20c68367497c416663f07065a862f1484b2c9f7
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=CIRCLE
LOOP_CYCLES=1
REVISION=51
```

Commit the marker change with commit message containing `[RUN-NARUTO-STORYMODE-ADAPTIVE-PLAYER]` to start the player workflow. Do not change or trigger this marker before the regression passes (it has now passed).

Accept revision 51 only if all conditions pass: input checkpoint SHA/size/header validation; explicit `ExecutionFlow::SaveStateLoaded`; five authentic 1280×800 external-X11 captures; F20 visibly restores the three-card overlay; no `ADAPTIVE_INPUT ... phase=press` event; at least one `ADAPTIVE_RESTORE_ONLY_INPUT_SUPPRESSED` event; `ADAPTIVE_RESTORE_ONLY_NO_INPUT_ASSERT=PASS`; accepted shutdown; and output checkpoint validated externally for size, v4 header, and SHA-256. Inspect the actual private screenshot before making semantic claims. Keep the newly emitted output unpromoted until an independent fresh-process restore confirms it.

If restored successfully, review the actual card-overlay screenshot and calibrate its classifier conservatively. Unknown states must remain WAIT. Never use Circle to skip dialogue; use START only for Story Mode dialogue.

## Longer-term engineering goal

Once restore-only is verified and card UI semantics are established, implement a persistent state machine with a checkpoint manifest, deterministic bounded emulator segments, screen/action/result verification, crash recovery, and automatic continuation between Actions runs. The monitor workflow currently checks Actions/artifact health; it does not drive the game or prove progress. Do not claim unattended chaining or game completion until exercised end-to-end and evidenced by a genuine in-game ending/results screen.

## Permanent boundaries

- Only repository: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. Do not access or modify the runner repository, Tile Duel, or any other repository.
- ROM, BIOS, savestates, Memory Cards, and genuine gameplay screenshots remain private and must not be committed to Git.
- Translate any Japanese text immediately into Indonesian in parentheses.
- Mark each rule VERIFIED / HYPOTHESIS / UNKNOWN based on evidence. Story Mode remains NOT COMPLETE until authentic ending evidence is verified.
