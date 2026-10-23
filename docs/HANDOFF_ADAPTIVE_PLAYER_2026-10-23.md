# Adaptive Story Mode player — checkpoint and next steps (23 October 2026, 07:34 WIB)

## Verified progress

**Story Mode is NOT complete.** There is no verified authentic ending/results frame yet. The unattended multi-run finisher is still not implemented.

### Revision51/52: independent checkpoint restoration
Run [#39875714125](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39875714125) restored SHA `017c6601ad71f7e420cc5406f20c68367497c416663f07065a862f1484b2c9f7` (21,162,772 bytes, v4), captured five external-X11 screenshots 1280×800, logged SaveStateLoaded and recorded zero pressed buttons in restore-only mode. Output SHA `36f58e705db5db5272ea0ed31fad07cff588fe1adf817fe795dc8d56ffe0e69e` (21,163,043 bytes, v4).
Run [#39876534507](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39876534507) independently restored that output in another fresh process. Five frames, SaveStateLoaded, zero presses and checkpoint validation passed; all five actual frames classified `card_selection` / `WAIT`. SHA `36f58e...` is a verified parent source.
Revision52 output candidate SHA `df73f3414c7838d22611a2592d5f2516f903e3e43a1d05911d1964ac07c61265` (21,163,194 bytes, v4) is structurally valid but remains unpromoted.

### Revision53: CIRCLE reveals card detail (acquisition still unknown)
Matched A/B run [#39877412316](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39877412316) used two fresh processes from parent SHA `36f58e...`, identical Memory Card clones (SHA `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`) and pixel-identical F20. The action branch pressed CIRCLE exactly once; control pressed no buttons. At F60 onward, action branch showed a face-up card with blue `守` emblem and title `防御集中`; the control retained three facedown cards. The description `気合いをいれて守る。防御技の、消費チャクラが0になります。` translates to “Bertahan dengan penuh semangat. Biaya Chakra untuk teknik pertahanan menjadi 0.”
**VERIFIED:** On this checkpoint, one CIRCLE reveals the card detail panel. **UNKNOWN:** whether it has been acquired/accepted or needs another CIRCLE. No assumption about acquisition should be made until the next controlled A/B.

Revision53 candidate outputs:
- Action/revealed-card checkpoint `adaptive-cycle-01-f180.sstate`, 21,163,007 bytes, v4, SHA-256 `bd2c4b7f187b21350e5157a11a7b6ab99cf2124a67be11b669f93c982bc25fae`.
- Control/facedown checkpoint `adaptive-cycle-02-f180.sstate`, 21,162,996 bytes, v4, SHA-256 `6c90ef08511bda6f5329e2ac65c6af6a542fe3c0884918a33f0f35125a19b135`.
Both passed structural validation but neither had yet been independently restored. Only the action checkpoint is selected for revision54 restore-only.

### Card-detail classifier: regression and real frames PASSED
Commit `331e2317cc51e386af51dc2d2d0117d459a42391` added localized blue/white card-art features and a dedicated `card_selection_detail` state. This state returns WAIT, never START. The intermediate regression #39878204502 failed only a static assertion expecting a literal state-specific shell message; the assertion was corrected in commit `a7f9f5da2a8ad2cb39af27aef48e24bf926fc11c`.
Latest regression [#39878572840](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39878572840) completed **success** on commit `a7f9f5da2a8ad2cb39af27aef48e24bf926fc11c`: 13 unit tests passed, all earlier private authentic screenshot checks passed, and all 10 genuine revision53 screenshots passed state regression:
- C01-F20 = `card_selection` / WAIT
- C01-F60/F100/F110/F180 = `card_selection_detail` / WAIT
- C02-F20/F60/F100/F110/F180 = `card_selection` / WAIT
This verifies classification of these authentic screenshots; it does not prove CIRCLE's acquisition semantics.

## Immediate operation — revision54 restore-only

The marker is configured for:
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
Revision54 must independently restore in a fresh process, log explicit SaveStateLoaded, capture five authentic 1280×800 frames, classify the F20/F60/F100/F110/F180 states as `card_selection_detail` / WAIT, emit zero button presses and pass external checkpoint size/v4-header/SHA validation. Do not promote revision54 output until another fresh-process restore confirms it.

## Then revision55: second-CIRCLE vs WAIT A/B

Only after revision54 passes all gates, set marker for a matched A/B using revision54's verified output as common parent: `AB_TEST=1`, `AB_ACTION=CIRCLE`, `AB_EXPECTED_STATE=card_selection_detail`, `LOOP_CYCLES=2`, `REVISION=55`. Use identical cloned Memory Cards and fresh emulator processes, require exact F20 image parity, action branch exactly one CIRCLE press/release, control branch zero presses, valid ten screenshots and structurally validated outputs. Inspect screenshot differences and title/prompt/return-to-board to determine whether the second CIRCLE acquires the card or causes another effect. Do not encode the result into policy until paired visual evidence establishes it.

## Longer-term goal

After card semantics and route/menu actions are calibrated, build a durable checkpoint manifest and an Actions continuation controller that launches each bounded next segment only after verifying prior result and checkpoint hashes, resumes on safe states, caps retries/no-progress, and detects authentic ending/results. The current monitor checks workflow/artifact health only; it is not a gameplay driver. Do not claim automatic full-story chaining until multiple successful segments chain without manual/chat relaunch, and do not claim Story Mode complete without an authentic ending/results frame.

## Permanent boundaries

- Only repository: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`; no runner repo, Tile Duel or other repository.
- ROM, BIOS, savestates, Memory Cards and real gameplay screenshots remain private and never enter Git.
- Translate Japanese text into Indonesian immediately in parentheses.
- Mechanics are VERIFIED / HYPOTHESIS / UNKNOWN according to direct evidence. Story Mode remains **NOT COMPLETE**.
