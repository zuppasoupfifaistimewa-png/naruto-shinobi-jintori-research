# Adaptive Story Mode player — checkpoint and next steps (23 October 2026, 07:14 WIB)

## Current result — Story Mode remains NOT COMPLETE

There is still no authentic in-game ending/results screenshot. A robust, unattended multi-session player is not yet implemented or verified; this work is still a controlled adaptive-player research prototype.

### Revision 51: no-input restore gate passed
Run [#39875714125](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39875714125) independently restored source SHA-256 `017c6601ad71f7e420cc5406f20c68367497c416663f07065a862f1484b2c9f7` (21,162,772 bytes; PCSX-Redux SaveState v4) in a fresh emulator process. It emitted five authentic 1280×800 external-X11 captures, logged `ExecutionFlow::SaveStateLoaded`, and proved no button was pressed in `RESTORE_TEST=1`: `ADAPTIVE_RESTORE_ONLY_NO_INPUT_ASSERT=PASS press_events=0 suppressed_input_calls=2`. It output candidate state SHA-256 `36f58e705db5db5272ea0ed31fad07cff588fe1adf817fe795dc8d56ffe0e69e`, 21,163,043 bytes, v4.

### Revision 52: candidate from revision51 restored and card state recognized
Run [#39876534507](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39876534507) completed success. The input checkpoint `36f58e705db5db5272ea0ed31fad07cff588fe1adf817fe795dc8d56ffe0e69e` was independently restored; explicit load event and five real 1280×800 captures passed. No press event occurred; the workflow logged `ADAPTIVE_RESTORE_ONLY_NO_INPUT_ASSERT=PASS press_events=0 suppressed_input_calls=1`. The authentic revision52 frames at F20/F60/F100/F110/F180 all classify as `card_selection` / `WAIT` with confidence 0.97, despite a gold/orange lower instruction panel.

Revision52 output candidate: artifact ID `12468413789`, `adaptive-cycle-01-f180.sstate`, 21,163,194 bytes, v4 header, SHA-256 `df73f3414c7838d22611a2592d5f2516f903e3e43a1d05911d1964ac07c61265`. It passes external structural validation, but is **not yet independently restored or promoted**.

### Card overlay rule and A/B preparation
Actual private screenshots show the board overlain by three card backs and instructions:
- `ゲットする札をえらべ!` (Pilih kartu yang ingin didapat!)
- `もらうチャンス札をえらんでね。` (Silakan pilih kartu kesempatan yang akan diterima.)
- `けってい` (konfirmasi)
- `忍` (shinobi/ninja); pink Chakra indicator `60`.

The previous classifier let a generic dialogue box win and suggested START, but restore-only suppressed it, so no input occurred. Commit `3f65ba64510783663fb253aa74f554d557d60d42` moved card-overlay recognition above generic dialogue. [Regression #39876294837](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39876294837) passed 11 synthetic tests, 10 earlier authentic-frame checks and all five authentic revision51 card-overlay frames; the latter all classified `card_selection` / `WAIT`.

Commit `f7e89824cfb644f0f2e2a33b12f487c10811d815` added card-selection A/B support: if the declared expected state is `card_selection`, only `CIRCLE` is accepted for the action branch; control is WAIT. Its regression, [#39876658165](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39876658165), passed.

A further A/B isolation hardening was added in commit `f3801c86552a9de6dd28c8836bb5e59b02454f43`: A/B mode suppresses the otherwise automatic START at F110, and asserts that the action branch has exactly one press and the control branch has none. Regression [#39876847536](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39876847536) is pending its final checks at the time of this handoff. Do not trigger the A/B player until it is green.

## Next operation — revision 53 card confirmation vs WAIT

Use the already independently restored checkpoint from revision51 as the common parent—not the unverified revision52 output—so both branches start from a known checkpoint:

```
MODE=ADAPTIVE
SOURCE_RUN=39875714125
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=36f58e705db5db5272ea0ed31fad07cff588fe1adf817fe795dc8d56ffe0e69e
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=CIRCLE
AB_EXPECTED_STATE=card_selection
LOOP_CYCLES=2
REVISION=53
```

Only write this marker with commit message containing `[RUN-NARUTO-STORYMODE-ADAPTIVE-PLAYER]` after regression #39876847536 succeeds. The AB runner creates identical cloned Memory Cards and restores the same parent checkpoint in two separate processes. It must fail closed unless F20 in both branches is classified `card_selection` / `WAIT`. Action branch may press CIRCLE once at F30; it must not send START or any other input later in the AB session. Control branch must record zero press events. Compare the two real screenshot sequences, the card cursor/selection/result, Chakra and post-action transition. Do not claim that CIRCLE selects/accepts a card unless the paired visual difference establishes this. Keep both outputs as candidates until each is independently restored.

If the A/B proves an appropriate card transition, build a persistent state machine/checkpoint manifest and automatic bounded-session continuation in Actions. The scheduled monitor only checks run/artifact health; it does not drive gameplay. Keep continuation behind verified state/action preconditions, output checkpoint structural checks, no-progress/crash recovery and ending detection. Do not claim autonomous end-to-end completion until multiple sessions are chained without chat/manual relaunch and authentic ending/results evidence appears.

## Permanent constraints

- Only `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`; do not access or change other repos, runner repo, or Tile Duel.
- ROM, BIOS, savestates, Memory Cards and real gameplay screenshots stay private and out of Git.
- Translate Japanese text immediately into Indonesian in parentheses.
- Mark mechanics VERIFIED / HYPOTHESIS / UNKNOWN according to direct evidence. Story Mode remains **NOT COMPLETE**.
