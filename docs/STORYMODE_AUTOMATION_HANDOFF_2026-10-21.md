# Automation Handoff — 2026-10-21

## Status: partial success, full automatic completion not yet built

Controlled checkpoint restore / single-action-vs-NONE probes / external X11 screenshot validation / pixel comparison / private successor savestate creation have all worked in the runs below. This is not yet a general-purpose adaptive player and Story Mode is not proven complete.

- RIGHT vs NONE: run 39606938717. Button readback passed, but post screenshots were pixel-identical; RIGHT did not move the vertical menu highlight.
- DOWN vs NONE: run 39607704007. Real external X11 shows highlight moved from ルーレット (Roulette) to 忍術 (Ninjutsu/teknik ninja). DOWN is verified for menu navigation in this context.
- Circle vs NONE: run 39608389644. Circle opened the roulette screen from the original f175 menu context. This was contextual menu confirmation, not dialogue skip. Circle branch f120 checkpoint SHA-256: 2550b90ce717822b5f04dcb0df3202816a383ea1e2d1a1779737d5d4d175b953 (21,161,990 bytes).
- No-input roulette follow-through: run 39609425942. Restored Circle branch f120 in a fresh process, sent no inputs, captured genuine external X11 at frames 20/60/100 and saved successor f120 checkpoint SHA-256 7c8c8bfa4a15132a6c9a046aa842fc01d2f294d6e04d53262c20287566432222 (21,162,475 bytes). Wheel continued visibly moving: mean RGB diff f20→f60 18.447444; f60→f100 18.405337. No final roulette result is established.
- Private artifact for run 39609425942: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39609425942/artifacts/12350232045; digest sha256:baf34328b15ca6e2e4fc8e697dcb9e0130772d44cd6328fed6d13e62adb9e1ad; expires 2026-11-04.

## Verified vs not yet implemented

Verified: checkpoint restore in fresh emulator process; source checkpoint kept unchanged; one-input/no-input differential probes; input readback; external X11 screenshots; pixel comparisons; private successor savestate; experiment handoff and cleanup.

Not verified/built: general game-state classifier; reliable adaptive decision logic; generic automatic recovery from arbitrary crash; autonomous multi-session progression through every mission; verified Story Mode ending. Do not claim full hands-off completion or game completion.

## Next steps

1. Preserve f175 and roulette branch checkpoints; never overwrite the immutable source.
2. Investigate roulette settling: run a longer no-input observation from the private wheel checkpoint, then test a candidate stop input only with matched controlled comparison if needed.
3. Verify roulette result and return-to-board transition from external X11 evidence.
4. Extend the probe harness into a state-aware loop with checkpoints before risky actions, validation after actions, crash recovery and session-to-session progress manifests.
5. Continue Story Mode without restarting from the title.
6. Prove the end with actual in-game ending evidence, not workflow success.

## Non-negotiable constraints

- Only repo: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research . Never access/modify Tile Duel or other repos.
- Gameplay evidence must be genuine emulator screenshots captured externally via X11; never use web images as gameplay evidence.
- In Story Mode dialogue, use START to skip; do not use Circle to skip dialogue.
- Japanese text must be followed immediately by Indonesian translation in parentheses.
- Never commit ROM, BIOS, savestates or Memory Card to Git. Keep these and gameplay artifacts private.
- Label findings verified / hypothesis / unknown.
- On a new chat, read STATUS.md, HANDOFF_CHAT_BARU_2026-10-19.md, docs/STORYMODE_POST178_CONTINUATION_2026-10-21.md, docs/STORYMODE_AUTOMATION_WORKFLOW_2026-10-21.md, docs/SIGSEGV_FORENSICS_2026-10-21.md and this file before acting.
