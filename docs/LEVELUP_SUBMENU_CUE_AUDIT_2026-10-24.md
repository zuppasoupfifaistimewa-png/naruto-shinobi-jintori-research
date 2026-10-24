## Supplemental visual audit — Revision62 matched-state LEFT→Circle A/B (24 October 2026)

### Artifact provenance and controlled start
- Run [#39940196133](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39940196133), private artifact `12495906030`; ZIP size `11,441,461` bytes and SHA-256 `b07efa5e448a78ce9f81392a094e645d9089a50baabadbca64646615cff83270`, matching GitHub artifact metadata.
- The report records F20 action/control parity (`1,024,000` identical pixels), the same parent checkpoint SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`, and both branches in `barrier_level_selection`. Both card clones match at SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- C01 sent LEFT at F30/F38, then Circle at F70/F78; all press/release readbacks passed. C02 remained no-input/WAIT. The artifact has authentic 1280×800 C01/C02 captures at F20/F60/F100/F110/F180.

### Cue-specific observations
- The prompt `レベルアップする結界をえらんでください` (Pilih penghalang yang akan dinaikkan levelnya), plus `けってい` (konfirmasi/pilih) and `もどる` (kembali), remains on the captured submenu. The visual audit found no selected-tile outline, unique focus ring, or corresponding tile-specific statistics/panel transition.
- The pink `60` badge is more exposed in the LEFT branch while the candidate remains more covered by the fixed HUD in control. This unequal visibility makes badge presence/visibility unsuitable as a controlled target cue. The action frames also change the board composition and Naruto pose.
- Artifact comparison reports `693755/693655/693270/693882` differing pixels at F60/F100/F110/F180. These broad deltas and the logged `WAIT` observations do not isolate a tile-attached selection effect; Circle produced no sampled submenu/panel transition.

### Disposition
- **VERIFIED:** matched initial submenu state and input trace. **HYPOTHESIS:** camera/view movement, animation, and fixed-HUD unocclusion explain the large image deltas and badge exposure. **UNKNOWN:** the target tile and its unique selection cue.
- This is a visual supplement to the already passing historical-frame policy fixture, not new proof of target semantics. The adjacent Revision47 artifact/run #39868722262 is a documented `roulette` A/B, not a submenu candidate.
- Keep `barrier_level_selection = WAIT`, target cue **UNKNOWN**, adaptive readiness **NO-GO**, Story Mode **NOT COMPLETE**, Revision65 marker unchanged at blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`, and cue token absent. No `.sstate` was opened/restored; no emulator/input/player workflow ran; no private evidence was committed.

### Next minimum evidence
Continue only with a distinct authenticated same-start-state A/B where the same candidate tile is clearly unobstructed in both branches and a repeatable cue physically attached to that tile changes with selection, preferably with a matching tile-specific information-panel change. Otherwise preserve UNKNOWN/WAIT and keep the cue gate closed.

---

## Offline follow-up — previously undocumented Revision58 artifact triage (24 October 2026)

### Scope and artifact provenance
- Audit-start `main` HEAD: `6b0a32f6c3e9bd791b701cb5d90adee9ecb0e058`. Only this repository was read or changed.
- Historical run [#39905240818](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39905240818) failed on 23 October 2026 and has private artifact [#12480856146](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39905240818). API artifact metadata: 3,075,304 bytes, digest `sha256:ca829197c7be852580e0527f071d2fc3711ff2433d17ed020f000fb52dbc4acf`.
- The ZIP manifest includes only one branch: `C01-F20.png`, `C01-F60.png`, `C01-F100.png`, `C01-F110.png`, plus text logs and JSON. There is no `C02` branch, no `C01-F180.png`, no A/B comparison report and no savestate file. The only recorded input file is `action-cycle-01.txt` with `CIRCLE`.
- Inspection used only these four authentic emulator screenshot PNGs and textual/JSON records. No savestate was opened or restored. No emulator was launched and no gameplay input was issued during this audit.

### What the authentic screenshots establish
- At F20, `decision-cycle-01.json` identifies `barrier_choice` and CIRCLE with `YES` visibly highlighted and a calibrated 120-Chakra cost. The visible Japanese prompt is `結界をレベルアップしますか?` (Apakah ingin menaikkan level penghalang?), with `はい` (Ya) and `いいえ` (Tidak).
- At F60/F100/F110, the screenshots visibly show the submenu prompt `レベルアップする結界をえらんでください` (Pilih penghalang yang akan dinaikkan levelnya), with footer hints `けってい` (konfirmasi) and `もどる` (kembali). Thus, this run authenticates the transition from the upgrade confirmation prompt to the level-up submenu by F60.
- The older frozen decision JSON misclassifies the F60/F100/F110 screenshots as `dialogue` and predicts `START`, despite the smaller submenu panel and its confirm/back footer. `action-cycle-01.txt` records only CIRCLE; this audit found no record that START was actually pressed in those later frames. This is evidence of a prior classifier-state error, not proof of a selected tile.
- Descriptive image comparison (all screenshots are 1280×800): F60↔F100 differs at 47,940 pixels (mean absolute RGB difference 1.72836); F100↔F110 differs at 43,590 pixels (1.00860); F60↔F110 differs at 53,358 pixels (2.07506). The character/tile ROI `(555,270,700,455)` changes at 14,375 of 26,825 pixels between F100 and F110, whereas the prompt-panel ROI `(120,560,700,730)` is pixel-identical between those two frames. These are descriptive animation measurements only, not classifier thresholds. The changing character/kunai/scene pixels cannot be attributed to a tile-selection cue without a matched control branch.

### Evidence classification and disposition
- **VERIFIED:** the authentic run displays `barrier_level_selection` prompt by F60 after the CIRCLE confirmation action; the captured prompt asks the player to choose a barrier to level up.
- **NOT ESTABLISHED:** which tile is targeted, whether Naruto's sprite/blue tile/nearby red-orange mark denotes focus, or whether a unique focus cue changes with target selection. This artifact is a single continuation path, not a matched-start-state action/control A/B.
- **UNKNOWN remains UNKNOWN:** keep `barrier_level_selection = WAIT`, target cue **UNKNOWN**, adaptive-player readiness **NO-GO**, and Story Mode **NOT COMPLETE**. Do not edit consumed Revision65 marker `3754a6ddf45a7570c053d9c149b6d80b0862a127`; do not add `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1`; do not start a player workflow just to bypass the gate.
- This review found no qualifying new target-cue evidence. Required evidence remains a distinct authenticated A/B from the same submenu start state, same candidate tile clearly unobstructed in both branches, and repeatable tile-anchored focus change (preferably corroborated by a tile-specific information-panel change), with matching runtime input/readback and no-input control records.

---

## Follow-up audit — distinct historical LEFT/CIRCLE A/B checks; no unique target cue (24 October 2026)

### Authenticated runs examined offline

- Run [#39908484177](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39908484177), artifact `12481932174`: LEFT action versus no-input control. F20 begins from matched `barrier_level_selection` decisions and all 1,024,000 pixels are identical. At F60/F100/F110/F180 the pairwise differing-pixel counts are 693,755/693,655/693,270/693,882 (mean absolute RGB difference 17.71671/17.62710/17.54281/17.62892). Runtime log confirms LEFT press/release readback but reports `state_changed=false`; the classifier stays `WAIT` through F180.
- In #39908484177, an exploratory mask inside `(525,145,660,225)` (`R>150`, `R>1.3×G`, `B>100`, `|R−B|<100`) counts pinkish pixels action/control as `146/146` at F20, `1160/172` at F60, `1076/162` at F100, `852/146` at F110. This diagnostic is not a target detector. The rise corresponds to the badge becoming more exposed under the HUD in the action branch; the control badge is still partly occluded. In instruction glyph ROI `(170,595,660,690)`, bright-pixel mask (`R,G,B>190`) counts are 1,658 in each branch with XOR 0 at F20/F60/F100/F110. The prompt remains `レベルアップする結界をえらんでください` (Pilih penghalang yang akan dinaikkan levelnya); the image difference does not establish a selected target because the target is not equally unobstructed across branches.
- Run [#39909132189](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39909132189), artifact `12481644668`: CIRCLE action versus WAIT control. Runtime logs record press/release readback but no state transition. C01/C02 pairs at F20/F60/F100/F110/F180 are all pixel-identical (zero differing pixels; mean absolute RGB difference 0). The badge is still partly covered by the HUD in both branches. This is limited to the observed frames and does not prove Circle is ineffective in every possible state.
- Run [#39946344909](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39946344909), artifact `12498880615`, was rejected as an independent cue result: `C02-F180.png` and `ab-comparison-report.txt` are missing, and its UP/camera-pan context overlaps already documented Revision64/65 evidence.

### Source/resource check

The current tracked tree has the screenshot classifier and an offline calibration helper, not the game renderer. `docs/ROM_STRUCTURE.md` and `docs/RESOURCE_CATALOG.md` document `SLPS_035.53`, `DATA.BIN`, `DATA2.BIN` and other extracted ROM files as local/off-repo inputs. The checked-in tree contains no game executable, extracted resource binary, or source implementation that maps submenu tile geometry or selected-target rendering. That avenue cannot presently resolve the cue from this repository alone.

### Classification and disposition

- **VERIFIED:** matched initial states for #39908484177 and #39909132189; the LEFT action has no observed classifier state change, while the sampled CIRCLE branch is pixel-identical to control. The current monitor report says player run #39975090690 is `skipped` with no player artifact.
- **HYPOTHESIS:** viewport movement/HUD unocclusion explains the pink badge's changed visibility in LEFT action branch; it is not verified from renderer source.
- **UNKNOWN:** which barrier tile, if any, is uniquely selected in the level-up submenu.

Keep `barrier_level_selection = WAIT`, target cue **UNKNOWN**, adaptive readiness **NO-GO**, Story Mode **NOT COMPLETE**. Keep consumed marker blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` and keep `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` absent. Required next evidence: a distinct authenticated matched-state A/B with the same candidate tile unobstructed in both branches and a reproducible cue anchored to that tile, preferably plus a matching tile-specific stats-panel change. No emulator, restore, continuation or gameplay input was run; only PNGs and text/JSON were examined, and no private evidence was committed.

---
# Addendum — distinct Revision59 evidence checked (24 October 2026)

### Source and scope
- Run [#39907655833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39907655833), private artifact `12482055310`, Revision59.
- This is separate from the Revision64/65 artifacts already compared; it is **not** an independent matched-state A/B for target selection. C01 begins at the upgrade confirmation prompt and transitions into the submenu following Circle; C02 begins already in the submenu and remains there after Circle.
- Inspected PNG screenshots plus decision/log text only. Savestate files in the artifact were not opened, read, or used; no emulator or input was executed.

### Offline measurements
F60/F100/F110/F180 candidate-ring counts: C01 `0/67/59/0`, C02 `52/67/67/64`. The broad ROI gold-panel mask stays near 2,559–2,566 pixels versus the calibrated map-positive threshold 5,000. Bright-text mask changes inside the submenu prompt region were zero for sampled within-branch frame transitions. These map-context thresholds are negative checks, not a general proof that the cue cannot exist.

The submenu prompt `レベルアップする結界をえらんでください` (Pilih penghalang yang akan dinaikkan levelnya), footer `けってい` (Konfirmasi/pilih, Circle), `もどる` (Kembali, X), badge pulse/visibility, character/kunai motion, and broad pixel deltas do not uniquely identify which barrier is selected. Current agent returns `WAIT` for the state, and current audit helper only accepts the calibrated map ring + matching statistics panel + text transition composite.

### Disposition
No unique cue found. Keep `barrier_level_selection = WAIT`, target cue **UNKNOWN**, readiness **NO-GO**, Story Mode **NOT COMPLETE**. Keep Revision65 marker `3754a6ddf45a7570c053d9c149b6d80b0862a127` untouched and cue token absent. No private evidence files added to Git. No code tests rerun: documentation-only update.

Next: find only an existing authenticated, same-start-state action/control artifact with an unobstructed tile cue, or continue available source-level work inside this repo. If there is no available evidence/source, do not guess or inject input; preserve UNKNOWN/WAIT.

---

# Level-up submenu target-cue audit — 24 October 2026

## Purpose and evidence scope

This is an offline-only comparison of already-existing authenticated emulator screenshots. No emulator, player workflow, savestate restore, continuation, or gameplay input was launched for this audit. Source screenshots were extracted temporarily from private GitHub Actions artifacts and are not included in Git.

- Revision64 source: Actions run [#39942178665](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39942178665), private artifact `12496637328`.
- Revision65 source: Actions run [#39947481094](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39947481094), private artifact `12498688466`.
- The comparison covers the five authentic captures from each branch: F20, F60, F100, F110, and F180 for C01 and C02. All images are 1280×800.

## New result: Revision64 and Revision65 are duplicate visual evidence

Every corresponding PNG in the two artifacts is pixel-identical. All ten comparisons returned `array_equal=true`, `differing_pixels=0`, and `mean_absolute_RGB_difference=0.000000`.

| Branch | Frame | Differing pixels | Mean absolute RGB difference |
|---|---:|---:|---:|
| C01 | F20 | 0 | 0.000000 |
| C01 | F60 | 0 | 0.000000 |
| C01 | F100 | 0 | 0.000000 |
| C01 | F110 | 0 | 0.000000 |
| C01 | F180 | 0 | 0.000000 |
| C02 | F20 | 0 | 0.000000 |
| C02 | F60 | 0 | 0.000000 |
| C02 | F100 | 0 | 0.000000 |
| C02 | F110 | 0 | 0.000000 |
| C02 | F180 | 0 | 0.000000 |

The private runtime logs distinguish the input protocols, even though the rendered frames do not. Revision64 reports one UP press/release at frames 30/38 in C01 and no input in C02. Revision65 reports UP at 30/38 and Circle at 70/78 in C01, with PAD readback confirming press and release; C02 remains the no-input control. Both report every observed frame as `barrier_level_selection` / `WAIT`.

**Interpretation:** the delivered Circle input in Revision65 produced no visible screen-state change in the captured F60–F180 observations compared with Revision64. This does not prove Circle can never have an effect in another game state, but it is not evidence that a target was selected or confirmed. Revision64 and Revision65 must not be counted as independent visual confirmations.

## Additional independent context — historical LEFT→Circle A/B

Actions run [#39940196133](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39940196133), artifact `12495906030`, contains the earlier LEFT→Circle A/B. The updated regression downloads this authentic evidence and checks all ten frames at F20/F60/F100/F110/F180 for C01 and C02. Result from Actions [#40069923244](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40069923244): `AUTHENTIC_HISTORICAL_LEFT_CIRCLE_BARRIER_POLICY=PASS checked=10 all_wait=true` (34 unit tests passed; workflow success). This is a new policy-coverage fixture, not evidence that either LEFT or Circle selected the intended barrier.

The LEFT branch badge remains partly hidden by the fixed HUD. A distinct UP branch from run #39942178665 exposes the pink badge at roughly `(455,234)-(533,301)` in F60, yet red focus-ring counts remain 66/58/66/80 at F60/F100/F110/F180. Those values remain below the calibrated unknown-context ceiling 100 and far below the positive map-UP count 811. The matching stats-panel footprint and panel-text transition are also absent. Thus improved visibility still does not uniquely identify a selected target.

The new workflow step asserts only the current safe state (`barrier_level_selection` / `WAIT`) on historical screenshots. It makes no gameplay, emulator, restore, or PAD calls and does not relax the existing fail-closed gate.

## Cue candidates and disposition

| Candidate cue | Offline finding | Decision |
|---|---|---|
| Pink `60` badge or brightness pulse | The pulse is shared across UP and WAIT in the known map comparison. In the submenu A/B, badge exposure is confounded by scene/camera displacement and fixed-HUD occlusion. | Reject as a unique target cue. |
| Badge screen position or visibility | The earlier terrain registration places the approximately 100 px displacement in the scene/camera motion; the badge is partly hidden by the fixed HUD in the control frames. | Reject as a selection proof. |
| Red directional focus arrows plus matching tile-information panel | These form a positive cue in the known map context, but the nested level-up submenu shows no equivalent ring-plus-panel composite. Existing counts remain map UP `811 / 8,312 / 635`, map WAIT `62 / 8,629 / 15`, submenu UP `66 / 2,452 / 3,221`, submenu WAIT `67 / 2,566 / 39` (ring / gold panel / text-mask delta). | Map-only signature; does not verify submenu target. |
| Blue/orange pointer proxy | Previously identified as part of the character's hand-held kunai sprite. | Excluded from cursor evidence. |
| Character pose or sprite motion | It can change after a directional input without a classifier state change. | Not a target-selection cue. |
| Instruction panel and Circle/X footer | The submenu prompt/footer remain unchanged in the sampled action/control images; no tile-specific level/value/durability panel appears. | Insufficient to identify the selected target. |

The Japanese prompt is `レベルアップする結界をえらんでください` (Pilih penghalang yang akan dinaikkan levelnya). The footer labels are `けってい` (konfirmasi/pilih, Circle) and `もどる` (kembali, X). Their presence documents the available controls, not which tile is currently selected.

## Safety decision

- `barrier_level_selection = WAIT`; unique target cue remains **UNKNOWN**.
- Adaptive-player readiness remains **NO-GO**; Story Mode remains **NOT COMPLETE**.
- Keep `experiments/.run-storymode-adaptive-player` at the consumed Revision65 marker blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` without modification.
- Keep `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` absent. Do not bypass the cue gate, launch gameplay, restore a checkpoint, or inject another input to resolve this ambiguity.
- No ROM, BIOS, Memory Card, savestate, screenshot, or private evidence artifact was added to Git.

## Next offline action

Do not re-run or double-count Revision64/65: their ten matching screenshots are duplicates. Continue only with a distinct, already-authenticated artifact that makes the candidate tile visible in both action and control without the fixed HUD hiding the discriminating pixels. If no such evidence exists, preserve `UNKNOWN` / `WAIT` rather than infer selection from color, camera movement, sprite pose, or a successful PAD readback. The last code regression remains Actions run [#40066679351](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40066679351), success (34 tests, all 15 workflow steps); this change is documentation-only, so that passing code result was not unnecessarily rerun.
