# Adaptive Story Mode player — checkpoint and next steps (23 October 2026, 07:30 WIB)

## Verified progress

**Story Mode is NOT complete.** No authentic in-game ending/results screen has been verified. The fully unattended multi-run player/orchestrator is not complete.

### Revision51 and revision52: independent checkpoint restores passed
Run [#39875714125](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39875714125) restored SHA `017c6601ad71f7e420cc5406f20c68367497c416663f07065a862f1484b2c9f7` (21,162,772 bytes, v4), emitted five authentic 1280×800 X11 captures, logged SaveStateLoaded and proved zero input in restore-only mode. Its output SHA was `36f58e705db5db5272ea0ed31fad07cff588fe1adf817fe795dc8d56ffe0e69e` (21,163,043 bytes, v4).
Run [#39876534507](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39876534507) restored that output in another fresh process with five captures and zero button presses. The five frames were all `card_selection` / `WAIT`. This makes SHA `36f58e...` an independently verified parent checkpoint.
Revision52 output candidate SHA `df73f3414c7838d22611a2592d5f2516f903e3e43a1d05911d1964ac07c61265` (21,163,194 bytes, v4) passed structural validation but is not independently restored/promoted.

### Revision53 CIRCLE vs no-input A/B: observed screen transition
Run [#39877412316](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39877412316) completed success:
- Both fresh processes restored the same verified SHA `36f58e...` and had identical F20 (1,024,000 pixel positions matched).
- Memory Card clone hashes were identical: `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- Cycle 1 pressed CIRCLE exactly once (press/release readback passed). By F60/F100/F110/F180 the left/center card was face-up, showing a blue `守` symbol and title `防御集中`; cycle 2 no-input control retained three facedown cards. Visual difference at F60: 297,197 differing pixels. All 10 screenshots were valid; checkpoints were structurally validated.
- Description: `気合いをいれて守る。防御技の、消費チャクラが0になります。` (Bertahan dengan penuh semangat. Biaya Chakra untuk teknik pertahanan menjadi 0.)
- This verifies **one CIRCLE reveals card details at this checkpoint**. It does not establish whether the card is already acquired or whether another confirmation is needed; that remains UNKNOWN.

Revision53 candidate states:
- Action/revealed-card output `adaptive-cycle-01-f180.sstate`, 21,163,007 bytes, v4, SHA-256 `bd2c4b7f187b21350e5157a11a7b6ab99cf2124a67be11b669f93c982bc25fae`.
- Control/facedown output `adaptive-cycle-02-f180.sstate`, 21,162,996 bytes, v4, SHA-256 `6c90ef08511bda6f5329e2ac65c6af6a542fe3c0884918a33f0f35125a19b135`.
Both pass structural validation but are not yet independently restored. Only the action/revealed-card output should be used as candidate source for the next restore-only test.

### Detail-state classifier in progress
Previous classifier calls card details `dialogue` / START because the lower instruction box is orange/gold. In commit `331e2317cc51e386af51dc2d2d0117d459a42391`, added localized ROIs and new state `card_selection_detail` with a distinctive revealed blue/white art signature and default WAIT, prior to generic dialogue. Added a synthetic regression, allowed this state for a controlled A/B expected-state precondition, and added a regression step that must classify all 10 authentic revision53 frames: C01-F20 = `card_selection` / WAIT; C01-F60/F100/F110/F180 = `card_selection_detail` / WAIT; C02-F20/F60/F100/F110/F180 = `card_selection` / WAIT.
Regression run [#39878204502](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39878204502) was still at “Install image dependencies” at last status check. **Do not proceed until it finishes successful.** If it fails, read the exact unit/real-frame mismatch and fix classifier thresholds/order before updating marker. No gameplay action has been started on the new detail classifier yet.

## Next steps

1. Wait for regression #39878204502 to finish. It must pass the synthetic test, previous authentic evidence and the 10 revision53 frames.
2. If green, run revision54 restore-only from #39877412316 action candidate:
```
MODE=ADAPTIVE
SOURCE_RUN=39877412316
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=bd2c4b7f187b21350e5157a11a7b6ab99cf2124a67be11b669f93c982bc25fae
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=CIRCLE
LOOP_CYCLES=1
REVISION=54
```
Require SaveStateLoaded, five genuine 1280×800 captures, all detail frames labelled `card_selection_detail` / WAIT, zero button presses, accepted shutdown and external checkpoint size/v4-header/SHA validation. Do not promote revision54 output until another fresh-process restore confirms it.
3. After that, run revision55 as a two-process matched A/B from the independently restored card-detail checkpoint: `AB_TEST=1`, `AB_ACTION=CIRCLE`, `AB_EXPECTED_STATE=card_selection_detail`, `LOOP_CYCLES=2`, `REVISION=55`. Use identical Memory Card clones, require exact initial-frame parity, exactly one CIRCLE press in action branch and zero in control, all captures valid and checkpoint outputs structurally validated. Compare result screen and subsequent transition. Only infer that the second CIRCLE accepts/acquires the card if paired visual evidence establishes it.
4. Then implement the persistent gameplay state machine and automatic sequential Actions continuation, guarded by verified states, checkpoint hashes, no-progress handling, max retries/segments, and authentic ending detection. Current monitor only checks workflow/artifact health—it does not play or chain sessions. Do not claim unattended completion until multiple Actions segments actually chain without ChatGPT/manual relaunch, and an authentic ending/results screenshot is present.

## Permanent boundaries

- Only repository: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. No other repositories, runner repo or Tile Duel.
- ROM, BIOS, savestates, Memory Cards and authentic gameplay screenshots remain private and must never be committed to Git.
- Japanese text always gets an Indonesian translation immediately alongside in parentheses.
- Rules are VERIFIED / HYPOTHESIS / UNKNOWN based on repeated direct evidence. Story Mode remains **NOT COMPLETE**.
