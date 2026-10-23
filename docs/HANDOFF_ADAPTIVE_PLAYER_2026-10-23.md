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

### Revision60 — LEFT changed character pose; target semantics still unknown

Run [#39908484177](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39908484177) succeeded as a matched A/B on the revision59 checkpoint. Regression run #39908408445 passed (17 unit tests). Source checkpoint SHA-256 was `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`. Identical F20 screenshots and identical Memory Card clone hashes satisfied the A/B precondition. Exactly one LEFT press/release occurred on action branch C01; control C02 had zero presses. Both branches produced valid v4 output checkpoints:
- C01 action output: 21,163,471 bytes, SHA-256 `702e2f28c28fe78b4732d1876617d19489b27394c24f98ffd4ea2e8259ec30de`
- C02 control output: 21,163,489 bytes, SHA-256 `2e17f143a03ad507ae68d2e06f5f5871a1e3674eb7b6e843125ac3efd5882a36`

Classifier state remained `barrier_level_selection` throughout both branches. Visual inspection of real screenshots shows the character sprite/pose differs between LEFT branch and no-input control, while the prompt 「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya) remains. This is a **verified response to LEFT input**, but it is only a **hypothesis** that the pose/facing indicates the intended target; no target marker or successful barrier-level change is yet verified. Normal adaptive policy should remain WAIT in this submenu until the next action has been calibrated.

Next probe: use action checkpoint C01 above as source and compare one CIRCLE confirm against zero-input control. This tests whether the current left-facing/LEFT-action checkpoint actually commits a target selection and advances. It is a short state-transition test, not a requirement to finish Story Mode.

### Revision61 — Circle did not commit the barrier choice

Run [#39909132189](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39909132189) succeeded as a matched Circle-versus-WAIT experiment from Revision60's LEFT-action checkpoint. Its private artifact #12481644668 was reviewed; it remains private, alongside the savestates.

Verified facts:
- Source checkpoint was Revision60 run #39908484177, action branch C01 at F180: `adaptive-cycle-01-f180.sstate`, 21,163,471 bytes, SHA-256 `702e2f28c28fe78b4732d1876617d19489b27394c24f98ffd4ea2e8259ec30de`.
- Both branches loaded the exact parent; F20 pixel parity passed (1,024,000 pixels) and Memory Card clones had identical SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- C01 action input CIRCLE press readback=true and release readback=false both passed; C02 control had no button press.
- Output checkpoints passed v4 header/size validation: C01 action 21,162,761 bytes, SHA-256 `9d3ae8dd94348d3cd45c149cae619d08fcdd7c185eeca8a656a3856beba064cf`; C02 control 21,162,868 bytes, SHA-256 `70283b676653717788cb4a31d7540a0a369f14f977228e7d4b12cf0791fc44a7`.
- Across F60, F100, F110 and F180, action and control frames had **exactly zero differing pixels**. Both remained classified `barrier_level_selection`. Therefore Circle was sent successfully but did not produce any visible gameplay effect in this state.

**Interpretation:** LEFT caused a reproducible visible pose/facing difference in Revision60, but that pose did not establish a verified target selection. A subsequent isolated Circle on the left-action checkpoint had no effect. Keep normal policy at WAIT for this submenu.

### Next task for the new chat: one-session LEFT → CIRCLE vs no-input control

Do not run another unmodified Revision61-style probe. Implement a bounded A/B sequence in the existing workflow: from the untouched pre-LEFT checkpoint (Revision59 run #39907655833, `adaptive-cycle-02-f180.sstate`, SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`), action branch should press LEFT at F30, release at F38, capture/inspect F60, then press CIRCLE at F70 and release at F78; control branch gets no input. Keep captures at F20/F60/F100/F110/F180 and compare pixels/states. Add explicit environment variables and tight allowlists; A/B may issue exactly the two configured presses on C01 and zero on C02. Test releases, exact source SHA, F20 pixel parity, state verification, checkpoint validation and private evidence upload. Add unit/source regression for the two-action protocol before triggering the run. Do not press START unless dialogue is actually detected; do not use Circle to skip dialogue. The aim is to verify a short barrier-target transition only, not complete Story Mode.

Current marker remains Revision61 (already executed); do not accidentally rerun it. Only the research repository may be touched. ROM, BIOS, Memory Card, screenshots and savestates must remain private artifacts and must never be committed. Story Mode completion remains unverified and is not a readiness acceptance requirement.


## Current handoff — Revision62 A/B result (23 October 2026)

The tasks specified in the previous handoff are complete. Regression [#39939979616](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39939979616) passed 18 tests and authentic X11 policy checks. Revision62 [#39940196133](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39940196133) passed operational assertions and uploaded private artifact #12495906030. Marker commit: d6cf0d6b05f96b1f0f6d346bd935f31185ee51f3. Protocol code/test commit: 11ea522ef63e0d90f96ff3aabb8ae3f7ccf5451c.

The selected source was Revision59 run #39907655833 artifact naruto-storymode-adaptive-player-private, checkpoint adaptive-cycle-02-f180.sstate, SHA-256 705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35, size 21,162,799 bytes; independently checked v4 header/hash. A/B invariants all passed: F20 parity at 1,024,000 pixels, identical Memory Card clones, C01 only LEFT@F30/F38 then CIRCLE@F70/F78 with true/false readbacks, C02 zero presses, all ten external-X11 1280×800 captures, and two v4 output checkpoints:
- C01: 21,163,248 bytes, SHA-256 cf868811502f65f3cd03b7c860acd9ae30dd705f183e226e530dde7066a82bcc
- C02: 21,163,035 bytes, SHA-256 a7062297e5311a67f607fb693597c4ecf963b97f83dacb911815bce40011f5a3

**Result:** the LEFT→CIRCLE sequence has not proven barrier selection. Both branches remain barrier_level_selection; 「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya) remains unchanged, and no selected-target highlight/state transition is verifiable. The LEFT branch visibly changes pose/scene composition, but that is not target-selection evidence. The incremental C01 F60→F100 difference is approximately the same as the no-input idle animation, and the prompt crop is pixel-identical. Therefore the default action policy remains WAIT in this submenu.

Do not rerun Revision62's consumed marker. Next work is a bounded, matched test to discover a target-selection visual cue/valid direction, with exact allowlist, source hash, screenshots, press/release readbacks, and checkpoint validation. Read the latest STATUS.md and ANALYSIS_LOG.md before proceeding. Do not require Story Mode completion for readiness, but also do not state the player is ready for unattended Story Mode yet.

## Current handoff — Revision63 UP vs WAIT result (23 October 2026)

**Current readiness: NO-GO.** The player can restore and run bounded, logged experiments with input readback/checkpoint assertions. The barrier-selection target is still not identified, so normal policy must remain WAIT in `barrier_level_selection`. Story Mode completion is neither this experiment's goal nor a readiness prerequisite; no completion claim is supported.

### Completed run and private evidence

- Regression: [#39939979616](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39939979616), success, 18 unit/source tests.
- Player: [#39942178665](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39942178665), success, protocol commit `91b9bbffb3c1a7c8a51ae944f229a29583c021e3`, private evidence artifact #12496637328.
- Marker `experiments/.run-storymode-adaptive-player` is consumed revision 63 and must not be rerun. It used source checkpoint from Revision59 run #39907655833, `adaptive-cycle-02-f180.sstate`, 21,162,799 bytes, v4, SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`. The immutable-source gate passed; no source checkpoint was changed.
- A/B preconditions all passed: each fresh process emitted `ExecutionFlow::SaveStateLoaded`; both F20 frames were identical across 1,024,000 pixels; Memory Card baseline/action/control clones had identical SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`. C01 had exactly one UP press at F30 and release at F38 with successful true/false readbacks; C02 had zero input. Ten authentic 1280×800 external-X11 captures were validated.
- Output checkpoints: C01 21,163,397 bytes, v4, SHA-256 `5557188cfa2ce12a70030b8bd650c181a2172f2934185290eb7352faa9754e40`; C02 21,163,426 bytes, v4, SHA-256 `80782b47cf17e8d5bdc414af468c63eb098916c50235f98c092a676cca53b71e`. Both passed external header/size/SHA checks. Native emulator exit values 139/124 were only accepted by the wrapper after its session-finished and checkpoint-validation conditions were met.
- Visual result: UP changes the board/view composition and exposes other colored map markers, but the prompt `「レベルアップする結界をえらんでください」` (Pilih penghalang yang akan dinaikkan levelnya) remains. The classifier still reports `barrier_level_selection` in every captured observation; no reliable target highlight or confirmed selection was verified. Action and control differ strongly at F60, but the target-selection semantics remain UNKNOWN. Do not encode UP as a target-selection rule; regular policy remains WAIT.

### Recommended next work

To test whether navigation followed by confirmation does anything, implement an explicitly allowlisted `UP_THEN_CIRCLE` vs no-input A/B from the same validated Revision59 parent. The existing workflow only accepts `NONE` or the earlier consumed `LEFT_THEN_CIRCLE` sequence, so **do not edit the marker to UP_THEN_CIRCLE yet**.

First:
1. Extend the player workflow's shell/Lua validation and timed sequence to accept only `AB_TEST=1`, expected state `barrier_level_selection`, first action UP, second action CIRCLE, two cycles, and restore/continuation flags zero. Keep all other sequences rejected.
2. Press UP at F30 and release at F38; require F60 to still be the calibrated submenu with WAIT classifier action and no dialogue/unknown result before allowing CIRCLE at F70, released at F78. On any state mismatch, stop and fail closed.
3. Add regression assertions for allowlist, timing, F60 gate, exact press/release counts, zero control input, and private checkpoint validation. Wait for regression to pass before changing the marker.
4. Use the same immutable Revision59 source SHA unless there is a clear reason otherwise. Require matched F20 pixels, identical Memory Card clones, explicit load events, ten authentic captures, exact input readbacks and v4/header/size/SHA checks for both new outputs. Keep screenshots and savestates in private Actions artifacts; never add them to Git.
5. Inspect the private output evidence visually and compare the instruction-panel crop before inferring that Circle selected a target. If there is still no clear state change, keep WAIT and choose a new probe based on the actual screen rather than cycling arbitrary input.

### Transfer notes

Latest durable result is recorded at the end of `STATUS.md` and `ANALYSIS_LOG.md`. The only permitted repo remains this research repository. START is for genuine dialogue only, Circle is not a dialogue skip, Japanese text gets immediate Indonesian translation in parentheses, unknown states fail safely, and Story Mode completion is not a present qualification requirement.


## Revision64 — UP_THEN_CIRCLE protocol implemented; regression gate pending (23 October 2026)

The private Revision63 artifact #12496637328 was downloaded and all ten F20/F60/F100/F110/F180 screenshots were visually reviewed. UP changes the visible composition at F60, while the instruction 「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya) remains; target selection is still UNKNOWN and normal policy remains WAIT.

Workflow changes are on commit 0073b9be0a541f52173a58dd68a32814fdacb625; regression assertions are on 813cc644f9898fd58a09f5678d6619c6f610df8f. The allowlisted protocol requires exactly UP press/release at F30/F38, then an F60 external screenshot classified barrier_level_selection + WAIT, before Circle press/release at F70/F78. If F60 is dialogue, unknown, or any other state, the workflow exits safely before Circle. Both shell and Lua validators restrict the sequence to AB_TEST=1, expected state barrier_level_selection, AB_ACTION=UP, AB_SECOND_ACTION=CIRCLE, LOOP_CYCLES=2, and restore/continuation flags 0. Regressions also enforce input counts, releases, zero control presses, matched F20 pixels, Memory Card equality, SaveStateLoaded events, ten captures, and checkpoint structural/hash checks.

The test-file push should trigger the configured regression workflow, but its run ID and final conclusion could not be independently retrieved using the currently available Actions inspection methods. Thus **regression is not yet confirmed PASS**. Do not change the marker or start Revision64 until a green run is verified. Current marker still contains consumed Revision63 settings and must not be rerun.

Source checkpoint remains unchanged: Revision59 run #39907655833, artifact naruto-storymode-adaptive-player-private, adaptive-cycle-02-f180.sstate, 21,162,799 bytes, v4, SHA-256 705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35. Keep ROM, BIOS, Memory Card, savestates and screenshots private/out of Git. Story Mode completion is not a qualification prerequisite.


### Revision64 final regression hardening — 23 October 2026

A source-level audit caught and fixed two regression-compatibility details before any player run:
- The workflow now sets `sequenceAction=nil` and assigns LEFT/UP only for the two explicitly recognized sequence names. This prevents the ordinary `AB_SEQUENCE=NONE` single-action A/B protocol from being mistakenly treated as an armed two-action sequence in Lua.
- The existing LEFT_THEN_CIRCLE source regression now checks the shared `AB_ACTION` timed assertion used by both sequences, while retaining the exact allowlist tuple and explicit LEFT outcome assertions.

Latest workflow commit: `a7e59dee93de44b7958f317a6239eda048e7951d`. Latest test commit: `123efe8480d50a1589d00dc3dd87e003b310e1bb`. A source-level sweep checked 54 literal `assertIn(..., workflow)` expectations in the test module against the current workflow; all 54 matched. This is only a static consistency check, **not a substitute for the actual regression workflow**. The Actions run conclusion still has not been independently retrieved, and the latest test commit should trigger the regression workflow again.

Keep marker `experiments/.run-storymode-adaptive-player` unchanged at consumed Revision63; do not rerun it and do not launch Revision64 until a green regression run is explicitly verified. All private evidence/source-checkpoint constraints above remain in force.

## Revision64 preflight audit — 23 October 2026

- Latest regression run [#39944753664](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39944753664), workflow run 33, completed **success** on test commit `123efe8480d50a1589d00dc3dd87e003b310e1bb`. The completed job log independently records **19 tests / OK**, `AUTHENTIC_X11_REGRESSION=PASS checked=10`, `AUTHENTIC_CARD_OVERLAY_DIALOGUE_PRIORITY=PASS checked=5`, and `AUTHENTIC_REVEALED_CARD_DETAIL=PASS checked=10`; all job steps passed. Main's workflow and test blob SHAs match the regression checkout (`60b613d2d6c7efde32452b16399814962308e541` and `5b60db1a22646a9b4176169462c193ae243b2a66`), so the result covers the current source files.
- The Revision63 player marker was read before any edit and is consumed; it remains unchanged in this preflight record. No concurrent player run was found in the recent Actions run list.
- Downloaded the source artifact for run [#39907655833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39907655833), private artifact `#12482055310`. Inside it, `adaptive-cycle-02-f180.sstate` was independently rechecked: **21,162,799 bytes**, `PCSX-Redux SaveState v4` header, SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`. This matched checkpoint has not been modified. Authentic private screenshot `C02-F180.png` displays `「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya)`, consistent with the intended `barrier_level_selection` parent.
- Audited the current player workflow's shell and Lua guards. Only the exact `AB_TEST=1`, `AB_EXPECTED_STATE=barrier_level_selection`, `AB_ACTION=UP`, `AB_SEQUENCE=UP_THEN_CIRCLE`, `AB_SECOND_ACTION=CIRCLE`, two-cycle tuple, with restore/continuation flags 0, is accepted. Lua independently validates the same sequence; C01 requires F20 state `barrier_level_selection` plus classifier action `WAIT`, presses UP at F30 and releases at F38, then requires the real F60 observation to remain `barrier_level_selection` / `WAIT` before authorizing Circle at F70/release F78. Any F20/F60 mismatch or unarmed sequence quits before the second input. Shell assertions enforce exactly two C01 press/release pairs, no unexpected C01 presses, zero control presses, equal initial F20 pixels, equal Memory Card clones (expected SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`), two `ExecutionFlow::SaveStateLoaded` events, ten authentic external-X11 1280×800 screenshots, and structural/header/size/SHA validation for both private output checkpoints.
- Regression is green and the Revision64 preflight is technically qualified. This is a **bounded qualification experiment only**, not proof that the player is ready for unattended Story Mode completion. If F60 is not the calibrated submenu with WAIT, do not send Circle. Keep all ROM, BIOS, Memory Card, savestate, and gameplay screenshots private and out of Git.

### Exact next marker (prepare only after this preflight record)

Do not reuse Revision63. Revision64 marker values are:
```
MODE=ADAPTIVE
SOURCE_RUN=39907655833
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-02-f180.sstate
SOURCE_SHA256=705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=UP
AB_EXPECTED_STATE=barrier_level_selection
AB_SEQUENCE=UP_THEN_CIRCLE
AB_SECOND_ACTION=CIRCLE
LOOP_CYCLES=2
REVISION=64
```

The marker push must use commit message containing `[RUN-NARUTO-STORYMODE-ADAPTIVE-PLAYER]` because the workflow job checks for that token. After the run, inspect its private artifact/logs and all ten screenshots before interpreting any apparent screen change. Verify checkpoint outputs and then append the result to `STATUS.md`, `ANALYSIS_LOG.md`, and this handoff.
 
## Revision64 runtime audit — 23 October 2026

Run [#39946344909](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39946344909) failed in the adaptive loop after the private artifact upload succeeded; private artifact #12498880615 is available. This is a harness timeout failure, **not** an F60 safety-gate rejection.

- The immutable Revision59 source was re-verified at SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`. Both fresh emulator processes logged `ExecutionFlow::SaveStateLoaded`; their F20 images were identical across 1,024,000 pixels. Memory Card clones matched SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- C01 classified F20 and F60 as `barrier_level_selection` / `WAIT`; the F60 authorization gate passed. C01 sent exactly UP at F30/released F38 and Circle at F70/released F78, with successful true/false readbacks. The C02 control branch sent zero input through F110.
- C01 reached F180 and its checkpoint passed external validation: `adaptive-cycle-01-f180.sstate`, 21,163,031 bytes, header `PCSX-Redux SaveState v4`, SHA-256 `35cb550a62732cc6ed757e21914b46c1c0f1b2266182e2ea7761a6d401046014`. **Do not promote this checkpoint**: it has not been independently restored.
- The private artifact has only nine authentic 1280×800 external-X11 screenshots: C01 F20/F60/F100/F110/F180 and C02 F20/F60/F100/F110. C02's emulator hit the 60-second wrapper timeout (exit 124) at F110, so C02 F180 and its output checkpoint are missing. The orchestrator reported `ADAPTIVE_ORCHESTRATOR_EARLY_EXIT missing=['C02-F180'] checkpoints=1/2` and the job failed with exit code 92. Full A/B acceptance therefore failed.
- At C01 F60/F100/F180, `「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya)` remained visible. From C01 F60 to F100, the instruction-panel ROI (x=140..685,y=565..715) and footer ROI (x=660..1130,y=685..770) each had zero differing pixels; both corresponding control ROIs were also stable. Whole-screen action/control differences mostly reflect the UP-induced view composition change and are not evidence that a target was selected. **Target/confirmation semantics remain UNKNOWN.**
- Required repair: increase only the per-emulator wrapper timeout from 60 to 90 seconds. Keep the Actions job capped at 20 minutes, preserve all shell/Lua allowlists and the F60 fail-closed gate, and add a source regression that verifies this bounded timeout. Do not launch the next player run until the resulting regression workflow is independently verified green. Revision64 is consumed; never rerun it. Use a fresh Revision65 marker against the same immutable Revision59 source only after regression passes.

Readiness remains **NO-GO**. Story Mode completion has not been proved and is not this qualification test's acceptance criterion. ROM, BIOS, Memory Card, savestates, and screenshots remain private and out of Git.

### Revision65 retry gate

1. Change the emulator wrapper timeout from 60s to 90s, keeping the 20-minute job timeout and the exact existing UP_THEN_CIRCLE allowlists/state gate/input timings intact.
2. Add a regression requiring the 90s bound and retaining the 20-minute job cap. The test-file push triggers regression; verify a green run with synthetic and authentic-screen checks before touching the marker.
3. After green regression only, set a new Revision65 marker with the exact Revision59 source and the same `UP_THEN_CIRCLE` A/B tuple. Use commit message token `[RUN-NARUTO-STORYMODE-ADAPTIVE-PLAYER]`.
4. Inspect the new private artifact: require ten authentic 1280×800 captures, two explicit `ExecutionFlow::SaveStateLoaded` events, identical F20 pixels, matching Memory Card clones, exact press/release readbacks/counts, passing F60 WAIT-state guard, and two external checkpoint header/size/SHA validations.
5. Do not promote a checkpoint without independently restoring it. If the prompt remains unchanged after Circle, keep target/confirmation UNKNOWN and select the next probe only from grounded visual evidence.
