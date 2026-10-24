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
