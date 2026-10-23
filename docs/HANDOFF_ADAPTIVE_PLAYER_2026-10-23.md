# Adaptive Story Mode player — checkpoint and next steps (23 October 2026, 07:09 WIB)

## Current verified state

**Story Mode is NOT complete.** No authentic in-game ending/results screen has been verified. The fully unattended multi-session finisher is not yet implemented or demonstrated.

### Revision 51 — independently restored source; restore-only invariant passed
Player run [#39875714125](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39875714125) completed successfully at 07:05 WIB. It independently restored the revision50 output from run #39872449049 in a fresh emulator process:
- Input checkpoint SHA-256: `017c6601ad71f7e420cc5406f20c68367497c416663f07065a862f1484b2c9f7`, 21,162,772 bytes, header `PCSX-Redux SaveState v4`.
- `ExecutionFlow::SaveStateLoaded` was logged.
- Five authentic external-X11 frames were captured (1280×800).
- The central `sendAction` guard suppressed both the F30 action call and the direct F110 START dialogue call; no `ADAPTIVE_INPUT ... phase=press` event exists.
- The workflow reported `ADAPTIVE_RESTORE_ONLY_NO_INPUT_ASSERT=PASS press_events=0 suppressed_input_calls=2` and `ADAPTIVE_RESTORE_TEST=PASS`.
- Output candidate from run #39875714125: artifact ID `12468331788`, file `adaptive-cycle-01-f180.sstate`, size 21,163,043 bytes, v4 header, SHA-256 `36f58e705db5db5272ea0ed31fad07cff588fe1adf817fe795dc8d56ffe0e69e`. It passes external structural validation, **but is not yet independently restored and must not yet be promoted**.

### Authentic card overlay and classifier correction
The private authentic frames show a three-card selection overlay over the board, with prompts:
- `ゲットする札をえらべ!` (Pilih kartu yang ingin didapat!)
- `もらうチャンス札をえらんでね。` (Silakan pilih kartu kesempatan yang akan diterima.)
- `けってい` (konfirmasi)
- `忍` (shinobi/ninja) appears on the card backs; the pink Chakra indicator shows `60`.

The previous policy misclassified F60/F100/F110/F180 as generic `dialogue` / START because the bottom instruction panel resembles a dialogue box. START was blocked in restore-only mode, so it did not mutate the game. In commit `3f65ba64510783663fb253aa74f554d557d60d42`, card-overlay detection was moved ahead of generic dialogue and a mixed card+dialog synthetic regression was added. The regression also checks all five authentic revision51 screenshots.

Regression [#39876294837](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39876294837) completed successfully at 07:09 WIB. Synthetic tests, ten earlier private authentic frames, and five actual revision51 card-overlay frames all passed. The five actual frames were classified `card_selection` / `WAIT`. This verifies classifier behavior on the available screenshots; it does **not** establish that any card selection/confirm action has the intended game effect.

The player artifact retention has also been raised from 14 to 90 days in the same commit to preserve private checkpoints for the longer multi-run investigation.

## Immediate next operation — revision 52 restore-only

Regression #39876294837 is green. Update marker `experiments/.run-storymode-adaptive-player` to:

```
MODE=ADAPTIVE
SOURCE_RUN=39875714125
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=36f58e705db5db5272ea0ed31fad07cff588fe1adf817fe795dc8d56ffe0e69e
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=CIRCLE
LOOP_CYCLES=1
REVISION=52
```

Commit the marker with a message containing `[RUN-NARUTO-STORYMODE-ADAPTIVE-PLAYER]` to start Actions. Do not promote or reuse the output until this fresh-process restore proves that it restores.

Accept revision52 only if input SHA/size/v4 header validate, explicit `ExecutionFlow::SaveStateLoaded` occurs, five authentic 1280×800 X11 frames exist, the card overlay consistently classifies `card_selection` / `WAIT`, no button press occurs, restore-only assertion passes, shutdown is accepted only through existing strict finished-marker and checkpoint-validation conditions, and the output state passes external size/header/SHA validation. Keep the revision52 output unpromoted until another independent fresh-process restore confirms it.

## After revision52

Once the revision51 output restores successfully, the next controlled test should be a two-process A/B from identical parent checkpoint and cloned identical Memory Cards: one branch sends one CIRCLE only if the actual classifier at F20 returns `card_selection` / `WAIT`, the other branch sends no input. First extend the A/B precondition/guard to accept `card_selection`; do not change the marker to A/B before tests pass. Capture authentic before/after frames and compare the resulting screen, card cursor, Chakra and subsequent transition. Do not infer the confirm result without this matched control. Unknown states stay WAIT. Use START only for true Story Mode dialogue, never to skip a card-selection prompt.

After the card transition is understood, build a persistent state machine / checkpoint manifest and verified bounded-session continuation in Actions. The existing monitor is only an Actions/artifact-health monitor, not a gameplay driver. Do not claim unattended chaining until it completes multiple sequential sessions from verified checkpoints automatically. Do not claim game completion until an authentic ending/results frame exists.

## Permanent constraints

- Only repository: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. No runner repo, Tile Duel, or any other repository.
- ROM, BIOS, savestates, Memory Cards and real gameplay screenshots stay private and never go into Git.
- Translate Japanese text immediately into Indonesian in parentheses.
- Mark mechanics VERIFIED / HYPOTHESIS / UNKNOWN according to direct evidence. Story Mode remains **NOT COMPLETE**.
