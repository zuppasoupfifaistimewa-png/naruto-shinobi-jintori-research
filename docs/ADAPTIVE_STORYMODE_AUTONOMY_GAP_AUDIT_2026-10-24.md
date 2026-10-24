# Offline readiness audit — autonomous Story Mode (24 October 2026)

## Audit baseline and scope
- Only repository: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`.
- Live main HEAD at review start: `9acbd5eed24bdc81165358d63ed594600dae488c`; its parent is the documented checkpoint `2a5fa920ab544f125041f3fefd8f202ab702601b`.
- Static review covered the adaptive classifier, the bounded player workflow, regression workflow/tests, current marker, and status/handoff. This is not a new screenshot/artifact audit.

## What already works
- The agent reads an external 1280×800 X11 frame, emits state/confidence/features/action/reason as JSON, and maintains small history for repeated map/roulette observations.
- Calibrated policy is state-scoped: START for recognized story dialogue; CIRCLE only for the visibly selected YES barrier prompt or stable revealed-card detail with its Circle glyph; conservative route movement; delayed roulette confirmation.
- Unknown states fail closed. In particular, `barrier_level_selection` and `battle_untrained` both return WAIT.
- The Actions runner bounds each invocation to one or two 180-frame cycles. It captures at F20/F60/F100/F110/F180, checks button press/release readback, restores a selected source checkpoint in a fresh process, validates saved state size/header/hash after emulator exit, and keeps output in a private artifact.

## What prevents Story Mode completion
1. **Target selection:** no unique tile-anchored cue is proven in `barrier_level_selection`; action must remain WAIT.
2. **Combat:** battle is explicitly untrained and no authentic paired battle evidence supports a move/attack/defense/turn policy. WAIT is required.
3. **Outcomes and completion:** result/win/loss and Story Mode ending states are not calibrated. The runner's only progress marker is a map-to-dialogue/battle transition; it cannot certify an ending.
4. **Autonomy scope:** the present workflow is a bounded experiment/checkpoint runner capped at two 180-frame cycles, not an unattended full-story controller.

Longer sessions or more input cannot resolve any of these evidence gaps and would reduce observability. The fastest valid route is to reuse qualifying existing evidence if it exists, then implement policy only for states with a repeatable authenticated action/control outcome.

## Current verified state
- Target cue: **UNKNOWN**.
- `barrier_level_selection`: **WAIT**.
- Adaptive-player readiness: **NO-GO**.
- Story Mode: **NOT COMPLETE**.
- Revision65 marker: consumed; blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`, untouched.
- Latest monitor #40102319836 succeeded on source `2a5fa920...`, but reported player #39975090690 as gated skip with no evidence artifact. Latest classifier regression #40071317759 passed 35 tests on code checkpoint `c0b7d489...`; neither is a gameplay completion result.

## Next work
1. Search only remaining distinct authenticated private artifacts for matched-start submenu selection evidence and battle/result action/control pairs. Do not repeat the documented Revision58–65 cue audits, count duplicate Revision64/65 images, or open/restore savestates.
2. Add no new game action unless a matched authentic comparison shows it changes a specific state repeatably; retain WAIT otherwise.
3. Build result/ending classification only from authentic result/ending captures, and require that classifier to produce a distinct completion candidate with an audit trail.
4. Qualify bounded checkpoint chaining and automatic stop/recovery on timeout, state regression, or unknown state before considering a longer unattended session.

No tests, emulator, restore, player workflow, gameplay inputs, or marker edits were performed in this review. Keep screenshots, ROM/BIOS, Memory Cards, savestates, and private artifacts outside Git.
