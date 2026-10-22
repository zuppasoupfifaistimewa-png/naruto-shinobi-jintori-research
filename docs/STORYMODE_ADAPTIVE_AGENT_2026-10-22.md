## VERIFIED UPDATE — state classifier and checkpoint shutdown safeguards (22 October 2026, 17:12 WIB)

The adaptive agent remains a prototype; Story Mode completion is not verified.

- Latest classifier regression [#39759649670](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39759649670) passed 8 synthetic tests plus 10 authentic private X11 frames.
- The former dual-HUD-only `battle_untrained` rule was too broad. The tested green board with route/tile symbols and both player HUDs is now `map_after_move`, with action WAIT. Only non-board dual-HUD screens fall through to `battle_untrained`, also WAIT. The exact checked frames are in private artifact #12416489109, not Git.
- Fresh process two-session run #39758737690 created two states and logged a load event in session 2, but failed because the outer watchdog checked before the second state/marker appeared. Both states in the private artifact had full raw size:
  - cycle 1: 21,162,838 bytes, SHA-256 `81487394b180a47c59165b49bae21f4d278b600d9fbf83c14086a9629da1c2b4`;
  - cycle 2: 21,162,485 bytes, SHA-256 `42c4ad60397ade407508c4393fac21c21db6f12c88c5efc77deb05a2daa827f5`.
- The next attempt #39759822818 captured all five cycle-1 frames and correctly detected map -> dialogue -> map_after_move, including a START tap at F110. It then terminated with native exit 139 and its checkpoint was only 2,097,152 bytes: **structurally invalid and unsafe to resume**. No cycle 2 ran. Treat the capture/decision portion as evidence, not a successful checkpoint run.
- Current engineering changes in workflow commit `6bca6f80853292b5ebe7033ea0e1a0d2d58be569`:
  1. Validate raw checkpoint size (>21,000,000 bytes) and PCSX-Redux SaveState v4 header immediately after writing.
  2. Defer emulator quit outside the GPU::Vsync callback using a nextTick callback.
  3. Permit recovery from exit 139 only when the session-finished marker and raw checkpoint size/header validation both pass.
  4. Make the external watcher wait for all captures, all checkpoints, and the fresh-process completion marker; fail quickly if the orchestrator dies with missing evidence.
- Player run #39760914530 was triggered on the prior workflow revision before these latest safeguards and was still in progress on last check. The updated revision-14 run #39761094445 is queued behind the existing concurrency lock. Do not launch a third run; inspect these in order and check the version/commit associated with each.
- One controlled sequence shows DOWN changing the route counter 4 -> 3, followed by dialogue `ここに結界をはります` (Aku akan memasang penghalang di sini), START to skip the dialogue, and by F180 a red barrier/seal graphic with Mizuki Chakra 1380 vs 1500 at the earlier F110 image while Naruto remained 1380. This remains HYPOTHESIS without a matched NONE branch at the same parent; do not declare a universal NPC barrier rule/cost from it.

### Operational rule
Never treat a checkpoint as valid merely because the API created a file or the log says CREATED. Require raw size, v4 header, SHA-256, and successful restore in a fresh process before promoting it to the next resume point. Do not broaden the autonomous policy beyond calibrated visual states. Story Mode stays NOT COMPLETE until an original in-game ending/results screenshot is verified.

---

# Story Mode adaptive agent — 22 October 2026

## Purpose and maturity

This adds the first runnable screenshot-driven adaptive control loop. It is an agent prototype, not proof that Story Mode is complete. It must not report completion without authentic evidence from the game's ending.

## Implementation

- `tools/storymode_adaptive_agent.py`: classifies one authentic external X11 frame and chooses one conservative action. It produces JSON state, confidence, visual feature measurements, action, and reason; it does not retain screenshots itself.
- `tests/test_storymode_adaptive_agent.py`: six synthetic tests for the known signatures, fail-closed behavior, dialogue skip, contextual barrier choice, and rotation after a map state persists. All six passed in regression run [#39753391179](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39753391179).
- `.github/workflows/naruto-storymode-adaptive-regression.yml`: unit-tests the classifier and checks five authentic X11 frames from private artifact #12386984413; it emits only JSON summaries to job logs and does not upload screenshots. Run #39753391179 passed all five real-frame expectations.
- `.github/workflows/naruto-storymode-adaptive-player.yml`: restores a verified board checkpoint in a fresh PCSX-Redux process, executes eight observe/decide/input/verify/checkpoint cycles, and uploads screenshots, JSON decisions, logs and savestates as a private 14-day Actions artifact.
- The live loop pauses the emulator at frames 20, 60, 100 and 180 of each cycle. It captures the root X11 window externally; it does not use PCSX's internal screenshot API. Inputs are sent only after the F20 observation, then read back and released at relative frame 38. F100/F180 classify the outcome; F180 is checkpointed before continuation.

## Calibrated state signatures

The features were checked against real X11 images extracted from private artifacts, including the roulette experiment (#39685868421), the START-dialog experiment (#39620432917), the route/dialog experiment (#39616129634), and the Mizuki dialogue comparison (#39619671384). These pictures remain private and are not committed to Git.

- **Roulette:** red and gold pixel proportions in the known left-side wheel region. The latest A/B experiment found that one Circle press and no input were identical at F100 and F180; both branches had returned to the board by F180. Current default: wait for a full observation window; only try one Circle press if the wheel still persists at the next observation.
- **Dialogue:** calibrated gold/orange lower message frame plus white dialogue text. Action: START, which is the verified Story Mode dialogue-skip button.
- **Barrier choice:** choice panel, blue cost glyph calibrated to 120 Chakra, and red highlight ellipse in the top YES row. Circle is permitted only when YES is visibly highlighted; otherwise wait. The visual signature is not a general-purpose OCR parser for every choice screen.
- **Map:** green map field in the center with no wheel and no lower dialogue. The first controlled route direction is DOWN, previously verified to move a route step (counter 2 to 1) and trigger dialogue. If the map remains the observed state after a prior direction, the agent tries the next direction as a controlled probe instead of spamming one button.
- **Encounter/battle layout:** private authentic frames C01-F100/F180 and C02-F20 from failed run #39687675432 show two colored player-status panels across the top. The classifier now has a corresponding dual-HUD signature and labels this state battle_untrained with action WAIT. This recognizes the tested encounter layout only; it does not solve attack, defense, turn switching, or results.
- **Right-side menu/unknown choice:** separate class, deliberately no input unless more context is calibrated.
- **Unrecognized state:** action WAIT. It must not blindly press Circle in untrained battle/result screens.

The encounter signature was calibrated from private real-emulator frames; screenshots remain private and are not committed. It has not been validated against every battle variant or result screen, which remain UNKNOWN.

## Latest known source and run

Immutable source checkpoint came from run [#39685868421](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39685868421), private artifact `naruto-storymode-next-roulette-circle-diff-private`: `next-roulette-result-none-f180.sstate`, 21,162,945 bytes, SHA-256 `19388b5a9b59c77e443f47abdc7c6f98251ef4a1be1b512378faab217a658ae9`. The source is copied read-only before launch.

Adaptive test run [#39687675432](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39687675432) completed **failure**. The original tests passed 5/5; external X11 captures were valid for C01-F20/F60/F100/F180 and C02-F20. Private screenshot inspection shows C01-F20/F60 are route views, while C01-F100/F180 and C02-F20 show the encounter layout with status panels. The old green-background-only classifier wrongly classified those encounter frames as map; the agent therefore selected DOWN and then RIGHT. The separate repeated-cycle control loop also stopped advancing after C02-F20; exact gate/VSync root cause remains unresolved. It timed out with only 5/32 images and 1/8 checkpoints. Private artifact #12386984413 contains the partial evidence and expires 4 November 2026. The post-fix regression run #39753391179 verified 5 authentic frames: route frames C01-F20/F60 classify as map; encounter frames C01-F100/F180 and C02-F20 classify as battle_untrained and choose WAIT. Six synthetic unit tests also pass. This validates classifier safety for these five captured frames only; it does not fix the runner hang or prove route progress. Do not count this as an autonomous eight-cycle run or Story Mode progress. A scheduled monitor now exists at `.github/workflows/naruto-storymode-adaptive-monitor.yml`; it checks Actions health every 15 minutes and on player-run completion, but cannot by itself establish in-game progress or ending.

## Privacy and correctness constraints

Only the Naruto research repository is permitted. ROM, BIOS, Memory Card, savestates and authentic gameplay images stay out of Git and must remain in private runtime storage/Actions artifacts. Japanese strings must be followed immediately by Indonesian translations in reports. This workflow must never claim Story Mode completion without the original in-game ending evidence.

## Remaining work

1. Review every state/action/verification from the eight-cycle run, including real screenshots and checkpoint hashes.
2. Add calibrated battle, roulette-result, win/loss, round/turn-result states when their screenshots exist. An unrecognized state must remain a no-input stop, never a fabricated action.
3. Exercise crash recovery from the last validated private checkpoint; current workflow saves one checkpoint per cycle and uploads artifacts on failure, but a restart after an emulator-process crash still needs explicit verification.
4. Continue from the newest verified checkpoint in bounded batches. The agent is not yet proven to finish all Story Mode stages.
