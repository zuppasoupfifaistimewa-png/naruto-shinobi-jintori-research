# Story Mode adaptive agent — 22 October 2026

## Purpose and maturity

This adds the first runnable screenshot-driven adaptive control loop. It is an agent prototype, not proof that Story Mode is complete. It must not report completion without authentic evidence from the game's ending.

## Implementation

- `tools/storymode_adaptive_agent.py`: classifies one authentic external X11 frame and chooses one conservative action. It produces JSON state, confidence, visual feature measurements, action, and reason; it does not retain screenshots itself.
- `tests/test_storymode_adaptive_agent.py`: synthetic visual-state tests for the known signatures, fail-closed behavior, dialogue skip, contextual barrier choice, and rotation after a map state persists.
- `.github/workflows/naruto-storymode-adaptive-player.yml`: restores a verified board checkpoint in a fresh PCSX-Redux process, executes eight observe/decide/input/verify/checkpoint cycles, and uploads screenshots, JSON decisions, logs and savestates as a private 14-day Actions artifact.
- The live loop pauses the emulator at frames 20, 60, 100 and 180 of each cycle. It captures the root X11 window externally; it does not use PCSX's internal screenshot API. Inputs are sent only after the F20 observation, then read back and released at relative frame 38. F100/F180 classify the outcome; F180 is checkpointed before continuation.

## Calibrated state signatures

The features were checked against real X11 images extracted from private artifacts, including the roulette experiment (#39685868421), the START-dialog experiment (#39620432917), the route/dialog experiment (#39616129634), and the Mizuki dialogue comparison (#39619671384). These pictures remain private and are not committed to Git.

- **Roulette:** red and gold pixel proportions in the known left-side wheel region. The latest A/B experiment found that one Circle press and no input were identical at F100 and F180; both branches had returned to the board by F180. Current default: wait for a full observation window; only try one Circle press if the wheel still persists at the next observation.
- **Dialogue:** calibrated gold/orange lower message frame plus white dialogue text. Action: START, which is the verified Story Mode dialogue-skip button.
- **Barrier choice:** choice panel, blue cost glyph calibrated to 120 Chakra, and red highlight ellipse in the top YES row. Circle is permitted only when YES is visibly highlighted; otherwise wait. The visual signature is not a general-purpose OCR parser for every choice screen.
- **Map:** green map field in the center with no wheel and no lower dialogue. The first controlled route direction is DOWN, previously verified to move a route step (counter 2 to 1) and trigger dialogue. If the map remains the observed state after a prior direction, the agent tries the next direction as a controlled probe instead of spamming one button.
- **Right-side menu/unknown choice:** separate class, deliberately no input unless more context is calibrated.
- **Unrecognized state:** action WAIT. It must not blindly press Circle in battle/result screens.

Battle and turn-result screens have not yet been calibrated with authentic examples. Until such images are obtained and independently validated, those states are not considered solved by this agent.

## Latest known source and run

Immutable source checkpoint came from run [#39685868421](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39685868421), private artifact `naruto-storymode-next-roulette-circle-diff-private`: `next-roulette-result-none-f180.sstate`, 21,162,945 bytes, SHA-256 `19388b5a9b59c77e443f47abdc7c6f98251ef4a1be1b512378faab217a658ae9`. The source is copied read-only before launch.

Adaptive test run [#39687675432](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39687675432) completed **failure**. Tests passed 5/5; external X11 captures were valid for C01-F20/F60/F100/F180 and C02-F20. Cycle 1 chose DOWN and button readback passed, but the expected route/dialog transition was not detected and the repeated-cycle runner stopped advancing after C02-F20. It timed out with only 5/32 images and 1/8 checkpoints. Private artifact #12386984413 contains the partial evidence and expires 4 November 2026. Do not count this as an autonomous eight-cycle run or Story Mode progress. A scheduled monitor now exists at `.github/workflows/naruto-storymode-adaptive-monitor.yml`; it checks Actions health every 15 minutes and on player-run completion, but cannot by itself establish in-game progress or ending.

## Privacy and correctness constraints

Only the Naruto research repository is permitted. ROM, BIOS, Memory Card, savestates and authentic gameplay images stay out of Git and must remain in private runtime storage/Actions artifacts. Japanese strings must be followed immediately by Indonesian translations in reports. This workflow must never claim Story Mode completion without the original in-game ending evidence.

## Remaining work

1. Review every state/action/verification from the eight-cycle run, including real screenshots and checkpoint hashes.
2. Add calibrated battle, roulette-result, win/loss, round/turn-result states when their screenshots exist. An unrecognized state must remain a no-input stop, never a fabricated action.
3. Exercise crash recovery from the last validated private checkpoint; current workflow saves one checkpoint per cycle and uploads artifacts on failure, but a restart after an emulator-process crash still needs explicit verification.
4. Continue from the newest verified checkpoint in bounded batches. The agent is not yet proven to finish all Story Mode stages.
