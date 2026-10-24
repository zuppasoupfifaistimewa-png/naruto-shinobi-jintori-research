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
