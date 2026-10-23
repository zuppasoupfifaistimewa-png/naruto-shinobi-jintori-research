## Revision57 result — chained gameplay progress, 23 October 2026

Run [#39904672868](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39904672868) completed successfully. It restored revision56's CIRCLE-action checkpoint and ran two bounded sessions in fresh emulator processes, capturing ten authentic 1280x800 external-X11 frames and validating both output savestates. Logs confirm:
- cycle 1: `before=dialogue action=START observed_after=map_after_move state_changed=true`;
- cycle 2: `before=map_after_move action=WAIT observed_after=barrier_choice state_changed=true`;
- sequential fresh-process checkpoint continuation and visual deltas passed.
Output checkpoint cycle 2: `adaptive-cycle-02-f180.sstate`, 21,163,287 bytes, SHA-256 `d487b8ac7cc3d90b543865ef1831acd696df41337e447472f6faa41acdaada1d`.

This is actual observed gameplay-state progression, but **not proof of a completed turn, mission, or Story Mode**. The system is usable for further bounded adaptive continuation but is not yet a proven hands-off Story Mode finisher. The next run continues from the barrier-choice checkpoint and should only take the calibrated CIRCLE branch if YES is visibly selected; otherwise it safely waits. Continue from this checkpoint rather than restarting.
 
---

## Strategy reset — 23 October 2026, after revision56

The objective is to **reach Story Mode completion through adaptive play**, not to prove every single game rule before attempting the game. The previous sequence spent too much time in narrowly-scoped validation; from this checkpoint onward, experiments should be limited to blockers that prevent progress.

### Revision56 result — successful matched action/control run

Run [#39904097181](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39904097181) succeeded. The branches began from identical parent checkpoint SHA-256 `475d40dc3b966060ad110fe46c060058030aa4d7bbd24df8e30f906b90cc1dd9`, with pixel-identical F20 states. Exactly one CIRCLE press/release was registered on the action branch; the control branch did not press a button. The action branch then classified F60 as `dialogue`, F100 as `map_after_move`, and F180 as `dialogue`; control remained `card_selection_detail` through F180. Both output checkpoints passed v4-header, size and SHA validation.

**Verified:** CIRCLE from the revealed-card detail state causes a different downstream visual/game state from waiting, reaching dialogue/map-transition-looking states in this run. **Not yet verified:** whether that action formally acquires the card, its strategic effect, or whether the later board transition counts as a completed turn. Output action checkpoint candidate: `adaptive-cycle-01-f180.sstate`, 21,163,141 bytes, SHA-256 `9df5b924478fb22c427735dc186e481c1cea0ff12900134eab94711352c30742`.

### Immediate strategy

Run revision57 in normal adaptive continuation mode using the action-branch checkpoint above as its source. Perform two bounded sessions chained through a newly written checkpoint; use screenshot observation, classifier decisions, real START presses to skip visible dialogue, and save-state validation. Do not run a restore-only or another matched A/B merely to re-prove already demonstrated mechanics. The immediate success criterion is a safe adaptive action followed by an authentic state change and valid resumed checkpoint. If this succeeds, continue chaining bounded gameplay runs and investigate only blockers such as battle decisions, no-progress loops or crashes.

The classifier still fails closed on untrained battle/unknown states; this can stall progress and should be the next practical blocker to address if encountered, rather than a reason to postpone all gameplay. No claim of full unattended play or Story Mode completion is permitted until a chained player demonstrates sustained progress and an authentic ending/results screen is privately verified.

Permanent boundaries continue: use only this research repository; keep the ROM, BIOS, savestates, Memory Cards and screenshots private (never commit them); translate Japanese text immediately into Indonesian in parentheses; use START for dialogue, not Circle.
 
---

## LIVE RUN NOTE — revision55 restore-only (in_progress; checked 23 October 2026, 07:40 WIB)

The revision55 marker has been committed and GitHub Actions run [#39879445016](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39879445016) is currently `in_progress` (last update `2026-10-23T00:39:56Z`). It is a restore-only test from revision54 output SHA-256 `219d03ab90b594c27430f91460319c6a4c9a3b05b6463871406ac777873bedf8`; it does NOT issue gameplay input. Job timeout is 20 minutes from 07:39 WIB, so if it remains stuck it should stop by about 07:59 WIB. Do not launch another player run or change the marker while this run is active. After it completes, inspect its five private captures, restore-only/no-press log, source load event, and output state size/v4-header/SHA before deciding on revision56. The intended next gameplay experiment remains one further CIRCLE vs WAIT A/B with `AB_EXPECTED_STATE=card_selection_detail`, but only after revision55 restore-only succeeds.

---

# Adaptive Story Mode player — checkpoint and next steps (23 October 2026, 07:38 WIB)

## Verified state

**Story Mode is NOT complete.** No authentic ending/results frame has been verified. The fully unattended multi-run player is not yet implemented.

### Revision53 A/B: one CIRCLE reveals card details
Run [#39877412316](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39877412316) compared exactly one CIRCLE with no input from identical fresh-process parent checkpoint SHA-256 `36f58e705db5db5272ea0ed31fad07cff588fe1adf817fe795dc8d56ffe0e69e`, identical Memory Card clones `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`, pixel-identical F20 frames and exactly one press vs zero. Action branch revealed a card with a blue `守` emblem, title `防御集中`, and description `気合いをいれて守る。防御技の、消費チャクラが0になります。` (Bertahan dengan penuh semangat. Biaya Chakra untuk teknik pertahanan menjadi 0). The control branch stayed on facedown cards. **Verified:** first CIRCLE reveals card detail. **Unknown:** whether a second CIRCLE accepts/acquires it.

Action checkpoint candidate from run #39877412316: 21,163,007 bytes, v4, SHA-256 `bd2c4b7f187b21350e5157a11a7b6ab99cf2124a67be11b669f93c982bc25fae`. It was later restored independently by revision54. The matched control output SHA was `6c90ef08511bda6f5329e2ac65c6af6a542fe3c0884918a33f0f35125a19b135` and remains non-promoted.

### Classifier and authentic-image regression passed
Commit `331e2317cc51e386af51dc2d2d0117d459a42391` added localized card-art ROI checks and state `card_selection_detail` with WAIT. Regression [#39878572840](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39878572840) succeeded after a static assertion correction (`a7f9f5da2a8ad2cb39af27aef48e24bf926fc11c`): 13 unit tests passed; all 10 authentic revision53 screenshots matched:
- C01-F20: `card_selection` / WAIT
- C01-F60/F100/F110/F180: `card_selection_detail` / WAIT
- C02-F20/F60/F100/F110/F180: `card_selection` / WAIT.

### Revision54 restore-only passed
Run [#39878936772](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39878936772) independently loaded revision53 action checkpoint `bd2c4b7f187b21350e5157a11a7b6ab99cf2124a67be11b669f93c982bc25fae` in a fresh emulator process. The private artifact was manually audited:
- `ExecutionFlow::SaveStateLoaded` present.
- All five authentic external-X11 frames are 1280×800.
- `ADAPTIVE_RESTORE_ONLY_NO_INPUT_ASSERT=PASS press_events=0 suppressed_input_calls=1`.
- Every frame F20/F60/F100/F110/F180 classifies `card_selection_detail` / WAIT, confidence 0.97.
- Output `adaptive-cycle-01-f180.sstate`: 21,162,165 bytes, header `PCSX-Redux SaveState v4`, SHA-256 `219d03ab90b594c27430f91460319c6a4c9a3b05b6463871406ac777873bedf8`. This hash independently verified local artifact bytes, but the output itself must still be restored by one more fresh process before promotion.

## Next immediate operation — revision55 restore-only

Run revision55 from the revision54 output to prove that newly emitted state resumes independently too:

```
MODE=ADAPTIVE
SOURCE_RUN=39878936772
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=219d03ab90b594c27430f91460319c6a4c9a3b05b6463871406ac777873bedf8
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=CIRCLE
LOOP_CYCLES=1
REVISION=55
```

Accept only explicit SaveStateLoaded, five valid authentic 1280×800 captures, all detail frames `card_selection_detail` / WAIT, zero press events, successful/accepted shutdown, and external output checkpoint size/v4-header/SHA validation. After revision55, its output may serve as the common parent for the second-CIRCLE vs WAIT A/B; do not use revision54 output in gameplay before this independent restore.

## Next experiment — revision56 second-CIRCLE vs WAIT

After revision55 success, set `AB_TEST=1`, `AB_ACTION=CIRCLE`, `AB_EXPECTED_STATE=card_selection_detail`, `LOOP_CYCLES=2`, `REVISION=56`, and use revision55's independently restored output SHA and run ID as source. Two fresh processes must use identical cloned Memory Cards, pixel-identical F20 frames, exactly one CIRCLE press/release in action branch, zero presses in control, five authentic captures per branch, and structurally valid outputs. Compare reveal/selection/confirmation prompt, return-to-board, Chakra and later transition. Only encode the effect if the matched evidence supports it.

## Longer-term goal

After this action is understood and other menu/route actions are calibrated, implement automatic bounded-session continuation through GitHub Actions with a checkpoint manifest, output hash validation, safe-state/action gating, no-progress/crash recovery, maximum segments/retries and genuine ending detection. Current monitor checks run/artifact health only; it does not drive gameplay or chain sessions. Do not claim end-to-end automation until multiple runs chain without ChatGPT/manual relaunch. Story Mode remains **NOT COMPLETE** until an authentic ending/results screenshot is verified.

## Permanent constraints

- Only `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. No other repository, runner repo or Tile Duel.
- ROM, BIOS, savestates, Memory Cards and authentic screenshots remain private and never enter Git.
- Translate Japanese text immediately into Indonesian in parentheses.
- Mark rules VERIFIED / HYPOTHESIS / UNKNOWN from direct evidence.

---

## Revision58 diagnosis and Revision59 readiness test — 23 October 2026

Run [#39905240818](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39905240818) failed before producing checkpoints. Its private artifact #12480856146 was inspected. Authentic frames C01-F60/F100/F110 show a small lower-left instruction panel reading 「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya), with Circle confirm and X back controls. These frames were misclassified as `dialogue` solely because the panel has an orange/gold border; the agent then sent START even though this was not dialogue. The process timed out before F180; checkpoints were 0/2. This is a classifier/harness policy failure, not proof that the parent checkpoint is corrupt.

Fix committed to this research repo:
- `tools/storymode_adaptive_agent.py` — v0.3.0 distinguishes the calibrated smaller nested barrier-selection panel from the full-width ornate story-dialogue panel; the nested selection action follows its explicit Circle-confirm prompt and must be verified by the next observation.
- `tests/test_storymode_adaptive_agent.py` — adds synthetic regressions for this submenu and for the full-width dialogue signature.
- `.github/workflows/naruto-storymode-adaptive-player.yml` — continuation policy guard recognizes the new calibrated state.

Commits: `afdbfad5c87bd8d0a1a029f70e668919e5c0e08f`, `a00026dca5a7be60f78b35d642fa0d954912df82`, `ae93fc15a2238ccbf608fcae785b56f1293ad0e8`.

Next, run Revision59 from the last valid Revision57 checkpoint (not Revision58, which emitted no checkpoint), using two bounded fresh-process segments. Success means the new classifier passes unit tests against regression fixtures, no START is issued on the barrier-selection submenu, each segment reaches F180, both checkpoint files pass v4 header/size/SHA validation, and the second segment really reloads the first segment's checkpoint. This is only a short readiness test; **do not treat story completion as a prerequisite**. If this passes, extend the unattended-session readiness tests and implement/validate self-chaining separately. Story Mode is not confirmed complete.

### Regression correction — v0.3.0 sparse dialogue, 23 October 2026

The regression dataset contains authentic empty/full-width dialogue frames whose orange-border ratio is only about 0.079 (but the top-border ROI is about 0.108). The dialogue threshold was therefore adjusted from 0.10 to 0.07 while retaining the full-width header threshold of 0.08; the real Revision58 submenu has header orange about 0.020 and remains distinguishable. Updated commit: `59abbb758a1ed0dfe813746afee75e9d68f240e5`.

Classifier regression run [#39907832073](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39907832073) completed **success** after the synthetic regressions and authentic external-X11 policy checks, including legacy dialogue frames, card overlay frames, and revealed-card frames. Revision59 gameplay run [#39907655833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39907655833) was still in progress at the last check; inspect its actual conclusion and private screenshots/checkpoints before promoting anything.

### Revision60 — controlled barrier-target direction probe launched

The classifier policy now returns WAIT for `barrier_level_selection` by default because the selected target is not yet visually verified. This avoids repeating Circle while the submenu remains unchanged. Commit `40fc562f4c4d0913381fc2dc24b1fda88ff01493`; the added safety regressions are in `10c1b5b29bf5cc7c4e34bbffd70ad94b5dd7122c`.

The final regression run before the gameplay probe, [#39908408445](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39908408445), passed after tests validated the workflow source that adds a one-direction-vs-WAIT A/B branch. The first earlier regression failures were stale concurrent runs on commits that predated the workflow change; the latest applicable run is green.

Revision60 [#39908484177](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39908484177) has been triggered with:
- source: revision59 run #39907655833, private artifact `naruto-storymode-adaptive-player-private`, checkpoint `adaptive-cycle-02-f180.sstate`, SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`;
- `AB_TEST=1`, `AB_ACTION=LEFT`, `AB_EXPECTED_STATE=barrier_level_selection`, two independent emulator processes from identical parent state, one LEFT input on action branch and zero inputs on control branch.
The target is not to finish Story Mode. Inspect private authentic frames and logs to see whether LEFT changes the selected barrier; if it does not, retain WAIT as the default and probe another direction only when warranted by evidence.
