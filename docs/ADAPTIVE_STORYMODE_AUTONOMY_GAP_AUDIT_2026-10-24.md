## Persisted readiness gates — GO before the first full autonomous attempt

A complete Story Mode run is **not** required to declare readiness. Readiness means the system has passed component and bounded integration checks that justify a first full autonomous attempt. It does not guarantee success. Story Mode may be marked COMPLETE only after authentic ending evidence from an actual run.

1. **State coverage:** authenticate the expected path's menus, map, dialogue, roulette, card/barrier choices, battle phases, results, and ending. Validate on representative authentic frames, including difficult transitions and negative lookalikes. Low-confidence or unknown state always maps to WAIT and a safe stop.
2. **Evidence-backed actions:** every progress-changing action has matched-start action/control evidence and a repeatable expected result. Confirm the observed state before acting again. The barrier-submenu target must have a unique tile-attached cue, unobscured in both branches and preferably corroborated by tile-specific panel data.
3. **Battle policy:** qualify turn, attack, defense, confirmation, and aftermath decisions in bounded authentic encounters. Unmeasured branches remain WAIT; the agent must stop safely when it cannot choose.
4. **Input safety:** central allowlist; bounded press duration; verified press and release; no held input on errors, timeout, or shutdown; the cue and state gates run before any PAD mutation. Regression evidence must include blocked/unknown cases.
5. **Checkpoint and recovery:** validate checkpoint size/header/hash after emulator exit, restore it in a fresh process, verify the loaded state and external frame, and preserve the last known-good checkpoint through a failed session.
6. **Autonomous loop:** bounded batches can chain verified checkpoints without repeated chat decisions. Add watchdogs, retry/time budgets, state-regression detection, private audit logs/artifacts, and automatic stop on unknown state or failed verification. A bounded pilot should cover a route transition, dialogue, and at least one resolved encounter across fresh-process sessions; the whole story need not be played first.
7. **Ending detection:** validate a terminal-state detector against authentic ending frames and hard non-ending examples. This can be qualified from existing authentic evidence; it does not require a prior full autonomous completion. The actual run still needs authentic ending evidence before Story Mode is declared complete.

Set readiness GO only after each applicable gate above has a recorded pass. Do not convert a regression/workflow pass into Story Mode progress. Current blockers remain: cue UNKNOWN, `barrier_level_selection = WAIT`, battle policy untrained, and no ending detector.

## Token- and quota-conscious continuation

Use the repository checkpoint and this checklist as durable memory. Read the current top status and this handoff first; open older audit sections only for a concrete unresolved question. Batch independent metadata reads, do not download or remeasure evidence already audited, and avoid running Actions for documentation-only updates. Keep each session to one concrete offline objective and record its result once. Resume later from the latest handoff rather than repeating exploratory work. Usage limits are account-enforced; do not attempt to bypass them.

---

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
