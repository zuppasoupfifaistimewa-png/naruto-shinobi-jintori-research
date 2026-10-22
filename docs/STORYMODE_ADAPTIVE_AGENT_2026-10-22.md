## VERIFIED RULE UPDATE — DOWN from Ninjutsu highlights Information (22 October 2026, 18:14 WIB)

Successful matched test [#39768787669](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768787669) used the already restore-validated Ninjutsu checkpoint SHA `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`.

- Parent F20 frames were pixel-identical (1,024,000/1,024,000 pixels); both branches classified `menu_or_unknown_choice`.
- ACTION branch DOWN readback passed press and release; control branch sent NONE/WAIT. Both processes logged `ExecutionFlow::SaveStateLoaded`, used identical-but-separate Memory Cards, produced five validated external X11 captures each, exited 0, and passed post-exit checkpoint size/header/SHA checks.
- In the action branch, the red highlight moved from `忍術` (Ninjutsu) to `情報` (Informasi) by F60. The control branch remained on Ninjutsu until F180. Comparison reported 14,606 different pixels and mean absolute RGB difference 1.04012 at F60/F100/F110/F180.
- **VERIFIED for the tested context:** DOWN advances the highlighted row from Ninjutsu to Information. Combined with the prior Roulette → Ninjutsu test, two successive DOWN presses have been shown to advance one row at each respective menu parent.
- Action checkpoint (#12421302756, private) is 21,162,009 bytes, SHA-256 `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`. It is not a trusted resume point until restored in a fresh process. Next step is `RESTORE_TEST=1` from this exact file; require the load event and post-load images before further menu exploration.

No Circle confirmation on this menu; the existing restriction allows Circle only for a contextual choice with visibly highlighted YES. Story Mode remains not complete.

---

## ACTIVE PROBE — next DOWN transition from Ninjutsu versus NONE (22 October 2026, 18:12 WIB)

Run [#39768787669](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768787669) is configured from the already restored parent SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`, one-action branch DOWN and NONE/WAIT control, separate identical Memory Cards, two cycles. It is intended to test whether the next menu selection after `忍術` (Ninjutsu) is `情報` (Informasi). Do not conclude until the X11 evidence, input readback, parent parity, two fresh-process load events and output checkpoint validation pass. Run was active at container initialization.

---

## VERIFIED UPDATE — fresh-process restore of menu-DOWN checkpoint passed (22 October 2026, 18:10 WIB)

- Run [#39768371975](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768371975) restored action checkpoint SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28` in a new process and logged `ExecutionFlow::SaveStateLoaded`.
- Five genuine external-X11 images at F20/F60/F100/F110/F180 passed 1280x800 integrity checks. The visible selection remains `忍術` (Ninjutsu). Footer `△ マップ` means (Triangle: Map).
- Emulator exit code 0; new post-exit-validated checkpoint is 21,162,575 bytes, SHA-256 `fa03a1840612749810453566a25805e89a4aa21ad64664695e09ed7222b77a9e`, in private artifact #12421326531 only.
- **Next:** matched Triangle-versus-NONE test from this immutable checkpoint. Verify identical F20, separate identical disposable Memory Cards, Triangle input press/release readback, ten authentic external-X11 frames, and both output state hashes. If the map view opens, stop to inspect before any further input. Circle remains unavailable unless a contextually valid YES is visibly highlighted.

Story Mode remains NOT COMPLETE.

---

## VERIFIED UPDATE — fresh-process restore of Ninjutsu-highlight state passed (22 October 2026, 18:10 WIB)

- Restore run [#39768371975](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768371975) loaded the matched DOWN/ACTION checkpoint from run #39767790829. Exact source SHA-256: `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`.
- The log explicitly verified `ExecutionFlow::SaveStateLoaded`; five genuine external-X11 frames were valid, F20 visibly showed the selected `忍術` (Ninjutsu) row, and emulator exit was 0.
- The new state produced by the restore-test process is 21,162,575 bytes, SHA-256 `fa03a1840612749810453566a25805e89a4aa21ad64664695e09ed7222b77a9e`. Its structural checks passed after exit, but do not promote it until another fresh-process restore. Continue to use the source checkpoint above as the pinned parent for the next paired test.
- Next: paired ACTION=DOWN vs NONE/WAIT from the same source and cloned Memory Cards, to test whether DOWN from Ninjutsu moves to `情報` (Informasi). Require identical F20 pixels, matching source hash, input readback, both fresh-process load events and external validation of output checkpoint structure. Do not confirm any menu entry with Circle under the current guard.

Story Mode remains not complete.

---

## NEXT VALIDATION — restore the matched DOWN successor before further gameplay (22 October 2026, 18:08 WIB)

Run [#39768371975](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768371975) is queued to restore the ACTION-branch checkpoint from A/B run #39767790829. Source SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`, size 21,163,486 bytes, private artifact #12420204586 only. Marker revision 21: one cycle, `RESTORE_TEST=1`, other experiment modes disabled.

Do not promote this state to trusted continuation until the fresh process records `ExecutionFlow::SaveStateLoaded`, five authentic post-load X11 frames, process exit, and post-exit size/header/SHA validation for its newly created state. Then use the restored menu selection to design the next bounded directional probe. Story Mode remains not complete.

---

## VERIFIED RULE UPDATE — DOWN advances the current right-side menu highlight one row (22 October 2026, 18:06 WIB)

The matched ACTION-vs-NONE experiment completed successfully in run [#39767790829](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39767790829).

- Parent source checkpoint hash: `7679cfbd3576c3202abcc299b907939ab4e4529e3a0aa260e780806b1e21cc92`.
- Both independent fresh emulator processes logged `ExecutionFlow::SaveStateLoaded`, and each captured 5 authentic external-X11 frames. Both used byte-identical separate Memory Card clones (SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`).
- Both F20 frames were pixel-identical (1,024,000/1,024,000 pixels), with `menu_or_unknown_choice` at the right-side menu. ACTION branch sent one DOWN; press and release readbacks passed. NONE branch sent no button at the action window.
- Visual comparison of authentic captures shows ACTION branch changes selection from `ルーレット` (Roulette) at F20 to `忍術` (Ninjutsu) at F60; NONE branch remains on Roulette through F180. Persistent comparison from F60 onwards found 14,609 differing pixels and mean absolute RGB difference 1.04924.
- **VERIFIED, scoped to this specific menu:** DOWN advances the current menu highlight by one row from Roulette to Ninjutsu. This is not a universal direction/control map for all screens.
- ACTION output checkpoint is structurally valid (21,163,486 bytes, SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`) but is not yet trusted as a continuation source until independently restored in a fresh emulator process. The control state is 21,163,324 bytes, SHA-256 `3da0a41d55e988550ef1a9368652fa909ae06da34c2b4b7bf315f5a820f76aeb`. Private artifact #12420204586 only.
- The next action is a bounded `RESTORE_TEST=1` run from the ACTION checkpoint. Verify the actual `ExecutionFlow::SaveStateLoaded` event and post-load external X11 frames before continuing menu exploration. Keep Circle disallowed for non-YES menu confirmation under the existing conservative policy.

Story Mode remains NOT COMPLETE without authentic ending/results evidence.

---

## VERIFIED UPDATE — single DOWN changed the menu selection in a matched test (22 October 2026, 18:06 WIB)

This is a narrow, controlled observation—not proof that a gameplay turn was committed.

- Run [#39767790829](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39767790829) passed using the same parent SHA in two fresh processes, `7679cfbd3576c3202abcc299b907939ab4e4529e3a0aa260e780806b1e21cc92`.
- Both F20 images were exactly pixel-identical; both states were `menu_or_unknown_choice`. Separate Memory Card clones matched at SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- DOWN arm input readback passed (press=true, release=false); NONE arm sent no buttons. F60 through F180 consistently showed 14,609 pixels differing, and real screenshot review identifies the difference as menu selection moving from `ルーレット` (Roulette) to `忍術` (Ninjutsu). NONE stayed on Roulette.
- Action output checkpoint: 21,163,486 bytes, SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`. Control output checkpoint: 21,163,324 bytes, SHA-256 `3da0a41d55e988550ef1a9368652fa909ae06da34c2b4b7bf315f5a820f76aeb`. Both were externally validated after process exit.
- Use **VERIFIED** only for the exact tested menu behavior; keep cross-menu generalization **HYPOTHESIS**.
- Visible footer `△ マップ` translates to (Triangle: Map). Suggested next safe test: Triangle versus NONE from the same immutable menu parent. Require same F20 pixels, separate identical Memory Card clones, two load events, actual press/release readback, 10 X11 frames and post-exit validation. Do not press Circle unless a valid YES is visibly highlighted. If a map view opens, stop to inspect the map screen before any further input.

Story Mode is not complete, and no ending/results screenshot exists. Artifacts remain private and out of Git.

---

## EXPERIMENT UPDATE — matched menu A/B branches are now reproducible; initial run hit report bug (22 October 2026, 17:59 WIB)

The first one-DOWN-versus-NONE run #39766331759 did not finish its comparison report because Python applied `%` formatting to a `Path` object. This was an audit-code failure, not evidence that DOWN had no effect. Do not promote that run's output checkpoint chain.

Its private evidence showed:
- identical parent checkpoint SHA-256 `7679cfbd3576c3202abcc299b907939ab4e4529e3a0aa260e780806b1e21cc92` for both branches;
- identical independent baseline/action/control Memory Card hashes `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`;
- 0 pixel differences at F20 across 1,024,000 pixels, both states classified `menu_or_unknown_choice`;
- DOWN input readback passed in the action branch; the control branch remained WAIT; each branch output passed size/header/SHA structural validation.

The path-format bug is fixed in commit [0041262a4c83edbabdbfb658ff3c572ad9e3a30c](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/0041262a4c83edbabdbfb658ff3c572ad9e3a30c). Rerun [#39767083708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39767083708) is active. Its outcome must be audited before recording any new rule. Story Mode remains NOT COMPLETE.

---

## VERIFIED UPDATE — two bounded fresh-process cycles passed (22 October 2026, 17:47 WIB)

This verifies resumable bounded sessions, not autonomous completion of Story Mode.

- Run [#39765193287](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39765193287) passed with 10/10 authentic external X11 frames. Both emulator processes logged `ExecutionFlow::SaveStateLoaded`, used sequentially linked checkpoints, and exited with code 0.
- The starting checkpoint was restored in run #39764239171 (21,162,934 bytes, SHA-256 `16f697fa95c16661a639ad46b55f90008e60200d1ee860058b12d7b1110d073b`). New cycle-1 checkpoint: 21,163,161 bytes, SHA-256 `fd46af37af86b0843651ee6baa5d10bd6cb75123d68c87e8319a647130d6b512`. New cycle-2 checkpoint: 21,163,013 bytes, SHA-256 `7679cfbd3576c3202abcc299b907939ab4e4529e3a0aa260e780806b1e21cc92`. Both passed raw size, v4 header and SHA-256 checks in shell after process exit; artifacts remain private (#12419528763).
- Authentic frames show the board transition to Iruka's dialogue `いいかナルト。` (Dengarkan baik-baik, Naruto), START used for skip, then a menu of choices. Because the menu choice isn't calibrated for action beyond conservative waiting, cycle 2 stays `menu_or_unknown_choice/WAIT`.
- Next: paired one-action-versus-NONE menu test from the immutable cycle-2 parent with identical but separate disposable Memory Cards. Press DOWN only when the initial menu screen is confirmed identically in both arms; never use Circle for this probe. The comparison should inspect visible menu selection and subsequent transition; the single pair is experimental evidence, not a general rule.

Story Mode stays NOT COMPLETE pending authentic in-game ending/results evidence.

---

## VERIFIED UPDATE — saved checkpoint was restored in a fresh emulator process (22 October 2026, 17:43 WIB)

The checkpoint continuation mechanism has now passed an actual bounded restore test, but the Story Mode agent is not yet proven capable of multi-stage autonomous completion. Story Mode remains **NOT complete**.

- Smoke run #39763526377 created and externally validated checkpoint `adaptive-cycle-01-f180.sstate` (21,162,617 bytes; SHA-256 `b55495934f9ba98165268627b35904918a4dd3983e6d90bb66e2662dfa059e17`) in private artifact #12419631005.
- Restore run [#39764239171](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39764239171) used that exact hash in a fresh process. Logs recorded `ExecutionFlow::SaveStateLoaded`; five post-restore authentic external-X11 captures passed validation; the emulator exited 0; the checkpoint created by that process passed shell size/header/SHA checks after exit.
- The restored checkpoint (private artifact #12419357425) is 21,162,934 bytes, SHA-256 `16f697fa95c16661a639ad46b55f90008e60200d1ee860058b12d7b1110d073b`.
- The bounded two-cycle continuation test [#39765193287](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39765193287) is active with this exact source checkpoint, `CONTINUATION_TEST=1`, `LOOP_CYCLES=2`. Passing its workflow summary alone is not sufficient: audit its 10 authentic images, two fresh-process load events, checkpoint chain and external post-exit hashes.

Only allow calibrated inputs. The restored board state is `map_after_move` with conservative `WAIT`; it must not blindly input Down/Circle. Keep unknown states fail-closed. No private gameplay images or savestates are committed/publicly linked.

---

## VERIFIED UPDATE — smoke checkpoint saved and externally validated (22 October 2026, 17:35 WIB)

This is a successful one-cycle harness result, **not** proof Story Mode is complete and not yet proof the resulting checkpoint can be restored.

- Run [#39763526377](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39763526377) passed 8 tests and 5/5 authentic 1280x800 external-X11 captures. Input DOWN and START press/release checks passed, with map → dialogue → map_after_move observed; START skipped the visible Japanese dialogue `ここに結界をはります` (Aku akan memasang penghalang di sini).
- Emulator exit code was 0 with `ADAPTIVE_SESSION_FINISHED cycle=1`. The post-exit shell check passed the raw checkpoint length, SaveState v4 header, and SHA-256:
  - `adaptive-cycle-01-f180.sstate`
  - 21,162,617 bytes
  - SHA-256 `b55495934f9ba98165268627b35904918a4dd3983e6d90bb66e2662dfa059e17`
  - private artifact #12419631005 only.
- Workflow source selection is now driven by validated marker fields `SOURCE_RUN`, `SOURCE_ARTIFACT`, `SOURCE_CHECKPOINT`, `SOURCE_SHA256`, `LOOP_CYCLES`, and `RESTORE_TEST`. The restore-test mode must verify the actual `ExecutionFlow::SaveStateLoaded` event plus an external X11 frame after restoration; file size/header/hash is necessary, not sufficient.
- Run [#39764239171](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39764239171) uses the smoke run's exact checkpoint as source with `RESTORE_TEST=1` and `LOOP_CYCLES=1`. Its result is not yet verified.

Do not advance to two cycles unless run #39764239171 proves fresh-process restoration. If it passes, use the newest validated checkpoint from that restore run for a bounded two-cycle continuation. If it fails, stay at restore-only diagnosis. Keep all artifacts private/out of Git; no gameplay image/state is to be publicly linked.

---

## LATEST RUN OUTCOME — checkpoint visibility race remains unresolved (22 October 2026, 17:20 WIB)

The adaptive player is still a prototype. Story Mode is NOT complete; no authentic ending/result capture exists.

- Runs [#39760914530](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39760914530) and [#39761094445](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39761094445) both failed during cycle 1 after 5/5 authentic external-X11 captures and 8/8 synthetic tests passed. DOWN and START press/release readback passed; map→dialogue progression was visible; START skipped the dialogue; F180 returned to map_after_move.
- Immediate Lua validation right after `Support.File:writeMoveSlice(state)` reported a zero-byte file and no v4 header, then the script exited 74. No session-finished marker and no cycle 2.
- Contradiction discovered in the uploaded private artifacts: the saved file had size 21,162,914 bytes (run #39760914530, SHA-256 `f1e04a97452d675d6c6a955acd1a3aa6341a13402ca87895d61d29a6edd11124`) and 21,163,014 bytes (run #39761094445, SHA-256 `64941480e4ff5eebb8497e7458ec83090d3aa2bf533d5290ac18ae882c5ab5e5`) and each begins with the PCSX-Redux SaveState v4 header. This points to a likely write/visibility race, but does not prove a successfully restorable state. Neither file has been validated in a fresh process.
- Next code change should shift size/header/hash validation out of the in-emulator VSync callback. Keep the checkpoint writing call, log only that it returned, defer emulator shutdown outside VSync, and validate/checksum the checkpoint from shell after the emulator process has exited. Fail closed; promote only a checkpoint that passes external checks. The next player run should be configured to one cycle first, then a separate fresh-process restore test.

---

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
