# Adaptive Story Mode player — checkpoint and next steps (23 October 2026, 07:18 WIB)

## Verified state

**Story Mode is NOT complete.** No authentic in-game ending/result screen is verified. Unattended session-to-session chaining is not built yet.

### Revision 51/52: checkpoint restored twice; no-input behavior verified
- Run [#39875714125](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39875714125) restored source SHA-256 `017c6601ad71f7e420cc5406f20c68367497c416663f07065a862f1484b2c9f7` (21,162,772 bytes, PCSX-Redux SaveState v4), captured five authentic 1280×800 external-X11 screenshots, and passed the restore-only guard with zero pressed buttons and two suppressed requests.
- Revision51 emitted state candidate `36f58e705db5db5272ea0ed31fad07cff588fe1adf817fe795dc8d56ffe0e69e`, 21,163,043 bytes, v4.
- Run [#39876534507](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39876534507) independently restored the revision51 output in a fresh emulator process. It captured five authentic frames, logged `ExecutionFlow::SaveStateLoaded`, passed `ADAPTIVE_RESTORE_ONLY_NO_INPUT_ASSERT=PASS press_events=0 suppressed_input_calls=1`, and classified each F20/F60/F100/F110/F180 frame as `card_selection` / `WAIT` at confidence 0.97. Therefore SHA `36f58e705db5db5272ea0ed31fad07cff588fe1adf817fe795dc8d56ffe0e69e` is an independently verified reusable parent checkpoint for the next controlled test.
- Revision52 output candidate (artifact #12468413789): `adaptive-cycle-01-f180.sstate`, 21,163,194 bytes, v4, SHA-256 `df73f3414c7838d22611a2592d5f2516f903e3e43a1d05911d1964ac07c61265`. It passes structural validation but is not independently restored/promoted; do not use it as parent yet.

### Card overlay classifier and A/B safeguards
Authentic frames show three cards over the board and instructions:
- `ゲットする札をえらべ!` (Pilih kartu yang ingin didapat!)
- `もらうチャンス札をえらんでね。` (Silakan pilih kartu kesempatan yang akan diterima.)
- `けってい` (konfirmasi)
- `忍` (shinobi/ninja) on the card backs; Chakra indicator `60`.

A generic lower gold/orange instruction box caused the earlier policy to mistake the card picker for dialogue. The workflow in commit `3f65ba64510783663fb253aa74f554d557d60d42` moved card-overlay detection ahead of generic dialogue. Regression [#39876294837](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39876294837) checked the changed classifier against five authentic screenshots: all `card_selection` / `WAIT`.

Card A/B preconditions were added in `f7e89824cfb644f0f2e2a33b12f487c10811d815`: only CIRCLE is permitted when the declared expected state is `card_selection`, with a WAIT control branch. Commit `f3801c86552a9de6dd28c8836bb5e59b02454f43` isolates the A/B by suppressing direct automatic START during that experiment, checks for exactly one press on the action branch and zero press events on the control branch, and adds a static test. A source-slicing error in an intermediate static test caused regression run #39877051224 to fail; it was corrected. Latest regression [#39877110916](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39877110916) passed completely on commit `25141c41a77b55340d4a8cc077cec76a4589f502`, including 12 unit tests, prior authentic evidence checks, and the five real revision51 overlay images. **A/B action isolation is now code-reviewed and regression-tested, but its emulator behavior remains to be demonstrated.**

## Immediate next operation — revision 53 CIRCLE-vs-WAIT A/B

The next marker is written below. It deliberately uses revision51 output SHA `36f58e705db5db5272ea0ed31fad07cff588fe1adf817fe795dc8d56ffe0e69e` as parent, because run #39876534507 independently restored it. Do not substitute the newer but unverified revision52 output.

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

Commit the marker with message containing `[RUN-NARUTO-STORYMODE-ADAPTIVE-PLAYER]` to start GitHub Actions. The workflow clones an identical Memory Card into both branches and uses fresh emulator processes restored from the same parent checkpoint.

Acceptance gates: F20 in both branches must classify `card_selection` / `WAIT`; the action branch sends exactly one CIRCLE with successful press/release readback; it may not send START or any other input later in the A/B session; control branch has zero press events; the two branches' initial F20 screenshots must match; all ten external-X11 captures must be valid; both output checkpoints must pass size/v4-header/SHA validation. Inspect private images from F20/F60/F100/F110/F180 in each branch and compare card cursor, resulting screen, Chakra and later transition. If preconditions fail, the runner must abort/no-op rather than guess. Do not declare CIRCLE the correct card action unless the controlled visual change substantiates that.

If A/B demonstrates the card transition, continue with an explicit state/action/result policy, checkpoint manifest and verified sequential Actions continuation. Current monitor only checks workflow/artifact health; it does not drive gameplay. For unattended chaining, each next segment must be dispatched only from a successful preceding artifact, validated checkpoint and safe state. Keep unknown states at WAIT; use START only for true Story Mode dialogue, not card instructions. Stop or flag no-progress/corrupt state; never silently claim completion. Full autonomous chaining and Story Mode completion remain **NOT VERIFIED** until demonstrated with multiple automatically chained segments and an authentic ending/results screen.

## Permanent constraints

- Only `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`; do not access or change other repositories, the runner repo, or Tile Duel.
- ROM, BIOS, savestates, Memory Cards and authentic gameplay screenshots stay private and out of Git.
- Translate Japanese text immediately into Indonesian in parentheses.
- Mechanics are VERIFIED / HYPOTHESIS / UNKNOWN depending on repeatable evidence. Story Mode remains **NOT COMPLETE**.
