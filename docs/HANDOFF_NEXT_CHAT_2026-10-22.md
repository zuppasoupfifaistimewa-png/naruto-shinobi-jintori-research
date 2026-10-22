## REVISION45 AUDIT — Circle reached roulette, but the A/B failed at shutdown

Run #39867730674 failed after capturing the ACTION branch and before starting the WAIT branch. Artifact #12464258211 passed ZIP integrity; real screenshots C01-F20/F60/F100/F110/F180 were inspected. F20 showed `ルーレット` (Roulette) highlighted in the source command menu; Circle input readback true/false passed. F60 through F180 display the roulette wheel.

After `ADAPTIVE_SESSION_FINISHED cycle=1`, PCSX-Redux aborted with `corrupted size vs. prev_size`, exit 134. Thus there are no C02 control captures and no A/B report. Classify “Circle from Roulette row opens wheel” as HYPOTHESIS / partial observation only until a matched A/B passes.

The artifact contains ACTION checkpoint `adaptive-cycle-01-f180.sstate`, size 21,162,546, v4 header, SHA-256 `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`. It has only local structural validation and is not promoted until independently restored.

Workflow fix commit `11b308f162aa1ef2f5b5167cd17b4340718a03de` accepts native exit134 only after the session-finished marker exists and the post-exit checkpoint passes external validation; this should allow valid private evidence to survive the known shutdown abort without masking earlier failures. The workflow also now accepts expected state `roulette` only paired with `AB_ACTION=CIRCLE`.

Next revision46 restore-only:
```
MODE=ADAPTIVE
SOURCE_RUN=39867730674
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=CIRCLE
LOOP_CYCLES=1
REVISION=46
```
Require SaveStateLoaded/restore PASS, five authentic 1280×800 screens with wheel visible, exit0 or session-finished+external checkpoint validation, and new output size/v4-header/SHA validation. Don't promote new output before it too restores. Once input verified, revision47 Circle-vs-WAIT from `roulette` state should test stopping/selecting the wheel result. Do not use Circle to skip dialogue; START only. Story Mode remains NOT COMPLETE.

---

## ACTIVE PLAYER — revision45 Circle vs WAIT on visibly highlighted Roulette menu

Run [#39867730674](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39867730674) active, started 05:49:51 WIB, hard timeout about 06:09:51 WIB. Exact source is run #39866820866 / artifact #12463489344 / `adaptive-cycle-01-f180.sstate` / SHA-256 `609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`, independently restored in run44 and visually showing `ルーレット` (Roulette) highlighted. Marker: AB_TEST=1; AB_ACTION=CIRCLE; AB_EXPECTED_STATE=menu_or_unknown_choice; two cycles, restore/continuation off; revision45. Current workflow blob `4021462372a7573132783b21285d35b0da25eab8` permits Circle only in the menu-state A/B branch.

Do not launch parallel player. Require all paired gates after completion: exact source SHA, two load events, F20 parity, menu state both arms, cloned cards identical, Circle true/false readback, WAIT control, ten authentic 1280×800 X11 frames, both exits0, both checkpoint validations, comparison report. Visually inspect whether Circle opens roulette; WAIT should leave highlighted menu. This is contextual menu confirmation, not dialogue skip. Use START for any dialogue. Story Mode remains NOT COMPLETE.

---

## REVISION44 RESTORE PASSED — Roulette menu selection is preserved

Run [#39867381637](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39867381637) succeeded at 22:48:12 UTC / 05:48:12 WIB. Private artifact #12464118614 passed ZIP integrity; the authentic F20 screenshot shows the command menu with `ルーレット` (Roulette) highlighted. The fresh emulator process logged `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`; five valid 1280×800 X11 captures, exit0, external output checkpoint validation all passed.

Promoted input source from run #39866820866 / artifact #12463489344 / `adaptive-cycle-01-f180.sstate`: 21,162,920 bytes, v4, SHA-256 `609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`. It is independently restore-proven. The new output from run44 is not promoted: 21,163,308 bytes/v4/SHA `0499c0f73799ac18f53a08bfd2c63a45738d8b56fcd32f157d6b0b7b596c19e3`.

Next revision45 Circle-vs-WAIT from the known Roulette-highlighted menu:
```
MODE=ADAPTIVE
SOURCE_RUN=39866820866
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=CIRCLE
AB_EXPECTED_STATE=menu_or_unknown_choice
LOOP_CYCLES=2
REVISION=45
```
Workflow commit `2ec5011c5c81f00e686690570bf4349f9124c531` permits Circle only for the menu-state A/B guard; map-state guard excludes it. Require all strict paired gates and directly inspect screenshots to verify that Circle enters roulette while WAIT leaves the menu. This is a visible menu confirmation, never a dialogue skip. Any dialogue is skipped with START. Story Mode remains NOT COMPLETE.

---

## ACTIVE PLAYER — revision44 restore-only of Roulette-highlighted command menu

Run [#39867381637](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39867381637) active; started 05:46:45 WIB and hard timeout about 06:06:45 WIB. Exact source: run #39866820866 / artifact #12463489344 / adaptive-cycle-01-f180.sstate / SHA-256 `609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`, size 21,162,920, v4. RESTORE_TEST=1, one cycle, revision44. Do not start another player.

Revision43 VERIFIED that CROSS from map returns to command menu: ACTION F100/F180 show `ルーレット` (Roulette) highlighted; WAIT remains map. Revision44 must confirm this menu state survives a fresh emulator process: SaveStateLoaded/restore PASS, five real 1280×800 screenshots, F20 Roulette highlight, exit0, external output checkpoint size/v4-header/SHA validation. Promote only input hash 609823…52bbffb7 upon success; the restore run's output itself remains unpromoted until an independent restore.

After pass, run revision45 CIRCLE vs WAIT from the proven menu checkpoint. Workflow permits CIRCLE only for menu-state A/B, never map or dialogue. Source screenshots already show Roulette selected. Inspect new captures to confirm wheel entry; Circle must never be used for dialogue skipping—use START. Story Mode remains NOT COMPLETE.

---

## LATEST VERIFIED MENU NAVIGATION — CROSS returns from map to command menu (revision43)

Run [#39866820866](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39866820866) success at 22:43:31 UTC / 05:43:31 WIB. Private artifact #12463489344 passed ZIP integrity and actual paired screenshots were inspected. Both processes loaded source SHA `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`, two load events, exact F20 pixel parity, identical disposable cards, CROSS true/false input readback, WAIT control, ten valid authentic X11 images, exit0 both, two validated output states, and comparison report.

**VERIFIED in this exact state:** CROSS exits the map view back to the right-side command menu. C01-F60 shows a two-option transition UI; C01-F100/F180 visibly show `ルーレット` (Roulette) highlighted. WAIT remains on the board map and Naruto cell panel. No character move/capture claim.

ACTION output candidate in artifact #12463489344 / run #39866820866 / adaptive-cycle-01-f180.sstate: 21,162,920 bytes, v4, SHA-256 `609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`. CONTROL output: 21,162,981 bytes, SHA `57fd76c4f133dc485e5bbfc49f8cb6e0e86593780812827bee1a43668ae80e84`. Both are structure-validated but unpromoted pending restore.

Next revision44: restore-only ACTION/menu checkpoint from run #39866820866/artifact naruto-storymode-adaptive-player-private/file adaptive-cycle-01-f180.sstate/SHA `609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`. Require load event, five authentic 1280×800 X11 images retaining Roulette highlight at F20, exit0, external output validation. Only then promote the input source.

Then revision45 Circle-vs-WAIT from that exact restored command-menu state: source screenshot demonstrates Roulette highlighted, and Circle is the known contextual menu confirm, not dialogue skip. Extend workflow menu guard to permit Circle only when state is `menu_or_unknown_choice`; dialogue classification must fail the precondition. Require all A/B gates and manually inspect Roulette entry. Use START for any Story Mode dialogue; never Circle for dialogue. Story Mode remains NOT COMPLETE.

---

## ACTIVE PLAYER — revision43 retry of CROSS vs WAIT (23 October 2026)

Run [#39866820866](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39866820866) active, started 05:41:57 WIB, hard timeout about 06:01:57 WIB. Revision42 failed before emulator because a final shell whitelist omitted CROSS; artifact #12463119868 had only 4,505 bytes and no gameplay screenshots. Workflow commit `417663b21ce0cd9218ef8c312913a90d65381788` fixes the remaining allowlist. The new run checkout uses this correction.

Exact marker: SOURCE_RUN=39786019434; SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private; SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate; SOURCE_SHA256=73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8; RESTORE_TEST=0; CONTINUATION_TEST=0; AB_TEST=1; AB_ACTION=CROSS; AB_EXPECTED_STATE=map_after_move; LOOP_CYCLES=2; REVISION=43. The source SHA is independently restore-proven by run #39786899480.

Do not start another player. After completion audit all A/B evidence gates and inspect authentic screenshots. Expected hypothesis, grounded in the visible footer `× もどる` (Cross: Kembali): ACTION returns to menu while WAIT remains map. Do not classify without actual image comparison. Story Mode NOT COMPLETE.

---

## REVISION42 BLOCKER — workflow final allowlist still omitted CROSS

Run #39866476856 failed before emulator launch. Artifact #12463119868 is only 4,505 bytes of setup/log data; there are no screenshots or gameplay evidence. Selector and Lua accepted CROSS, but a later shell validation still allowed only UP/DOWN/LEFT/RIGHT/TRIANGLE. Workflow fix commit `417663b21ce0cd9218ef8c312913a90d65381788` added CROSS to that final allowlist. CROSS remains permitted only for `map_after_move`; menu state still only allows DOWN/TRIANGLE.

Next revision43 retries from the unchanged restorable Naruto-cell/map checkpoint:
```
MODE=ADAPTIVE
SOURCE_RUN=39786019434
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=CROSS
AB_EXPECTED_STATE=map_after_move
LOOP_CYCLES=2
REVISION=43
```
Require exact source hash in both processes, two load events, F20 pixel parity and map state, identical cloned cards, CROSS press/release true/false, WAIT control, ten authentic 1280×800 X11 captures, both exit0, both output checkpoints post-exit size/v4-header/SHA verified, comparison report, manual screenshot review. The screen footer is `× もどる` (Cross: Kembali), so the hypothesis is return-to-menu versus WAIT staying in map; do not claim it until the A/B screenshots prove it. No Circle/confirm. Story Mode remains NOT COMPLETE.

---

## ACTIVE PLAYER — revision42 CROSS vs WAIT, map return prompt

Run [#39866476856](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39866476856) is active, started 22:39 UTC on 22 October (05:39 WIB on 23 October); hard timeout about 05:59 WIB if still running. Marker checkout verified:
```
MODE=ADAPTIVE
SOURCE_RUN=39786019434
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=CROSS
AB_EXPECTED_STATE=map_after_move
LOOP_CYCLES=2
REVISION=42
```
Workflow blob `494baab78b7237fa80674526c583e0fdfc74c140` allows CROSS for map-state only; menu actions remain DOWN/TRIANGLE. It tests the authentic footer `× もどる` (Cross: Kembali), comparing a one-press CROSS with WAIT. At last check the job was in container initialization and had no artifact. Do not launch another player.

Audit every paired gate after completion: exact source hash both arms, 2 load events, identical F20/state map_after_move, identical cloned cards, CROSS press/release true/false, WAIT control, 10 authentic 1280×800 frames, both exits0, both output checkpoints external size/v4-header/SHA verified, comparison report generated. Directly inspect screenshots: does ACTION return to the prior menu while WAIT stays on the map? This is not a tile-confirmation action. Story Mode remains NOT COMPLETE.
 

---

## REVISION41 RESTORE PASSED — Naruto-cell focus state is independently restorable

Run [#39786899480](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39786899480) success. Private artifact #12428873919 passed ZIP integrity and was visually inspected. The actual F20 screenshot shows Naruto's panel: `レベル` (Level) 1, `結界価値` (Nilai penghalang) 60, `耐久値` (Daya tahan) 2/2. New process logs `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`; five authentic 1280×800 captures, exit0, and output size/header/SHA checks all passed.

Promoted input source: run #39786019434 / artifact #12428777970 / `adaptive-cycle-01-f180.sstate`, 21,163,100 bytes, v4 header, SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`. The new output from #39786899480 is unpromoted: 21,162,593 bytes, v4, SHA-256 `93bd0c3e401bd7b8c96bc8b405bd46b13fef2afaf317c2ec47af5412c1b52595`; restore it independently before reuse.

Workflow commit `7ac1b2371b7d0ce48b87b59130a8560db771a962` permits CROSS only as a map-state A/B action (it is not permitted for menu state). The screen footer `× もどる` (Cross: Kembali) supports a minimal matched test that CROSS backs out of the map while WAIT stays on the map.

Next marker revision42:
```
MODE=ADAPTIVE
SOURCE_RUN=39786019434
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=CROSS
AB_EXPECTED_STATE=map_after_move
LOOP_CYCLES=2
REVISION=42
```
Require exact source hash both processes, 2 load events, identical F20 pixels/map state, identical cloned cards, CROSS press/release true/false, WAIT control, ten genuine 1280×800 X11 captures, exit0 twice, both output savestates externally validated, comparison report, and screenshot review. This is only a return-menu probe. No Circle/confirmation. Story Mode remains NOT COMPLETE; use START for dialogue skips.

---

## ACTIVE PLAYER — revision41 restore-only for verified Naruto-tile focus (22 October 2026, 20:27 WIB)

Run [#39786899480](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39786899480) is active, started 20:26:48 WIB, timeout around 20:46:48 WIB. Exact committed marker uses source run #39786019434 / private artifact #12428777970 / adaptive-cycle-01-f180.sstate / SHA `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`, RESTORE_TEST=1, one cycle, revision41. Do not start another player.

Source checkpoint is ACTION output from revision40 UP/WAIT A/B and visually shows Naruto's cell focused (Level1, barrier value60, durability2/2). Run must log SaveStateLoaded + restore PASS, have five authentic 1280×800 X11 captures retaining that panel at F20, exit0 and externally validate output size/v4-header/SHA. Promote only the exact input hash 73947… after success; new output stays unpromoted until an independent restore.

Revision40 verified narrow focus rule: UP from empty land140 returns focus/panel to Naruto's cell60; WAIT preserves empty land140. No actual Naruto movement or capture/ownership proven. Story Mode remains NOT COMPLETE.

---

## REVISION40 VERIFIED — UP returns focus to Naruto's tile (22 October 2026)

Run [#39786019434](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39786019434) passed paired UP-vs-WAIT from source SHA `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`. Artifact #12428777970 inspected. Two load events; exact F20 parity; identical disposable cards; UP true/false input readback; WAIT control; ten authentic 1280×800 captures; both exits0; both outputs external validated; comparison report.

**VERIFIED, focus only:** UP from `空き地` (Tanah kosong) value140 changes the focused tile/panel to Naruto's cell, showing `レベル` (Level)1, `結界価値` (Nilai penghalang)60, `耐久値` (Daya tahan)2/2. WAIT stays on empty land140. No claim of character movement/capture/ownership.

ACTION output candidate from run #39786019434 / artifact #12428777970 / `adaptive-cycle-01-f180.sstate`: 21,163,100 bytes, v4, SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`; control SHA `eb182a883b1666a7a9badbbf06fda2de960fc84ec4b040799791a174134714a3`. Neither promoted pending restore.

Next revision41: restore-only fresh process from run #39786019434 / artifact `naruto-storymode-adaptive-player-private` / `adaptive-cycle-01-f180.sstate` / SHA `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`. Require load event, five authentic frames retaining Naruto-cell value60 panel, exit0 and external output validation. Do not promote new restore output until that file itself is restored.

Story Mode remains NOT COMPLETE. All assets private/out of Git; use START for dialogue, never Circle for dialogue.

---

## LATEST VERIFIED MAP RULE — UP returns focus to Naruto cell (revision40, 22 October 2026)

Run [#39786019434](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39786019434) fully passed matched UP-versus-WAIT from the independently restored revision33 source SHA `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`. Artifact #12428777970 was inspected. Both processes logged `ExecutionFlow::SaveStateLoaded`; cloned Memory Cards matched; F20 images were pixel-identical (1,024,000 pixels); both F20 states `map_after_move`; UP press/release readback true/false; control WAIT; ten authentic 1280×800 screenshots; both exits0; both output checkpoints externally validated for size/v4-header/SHA; comparison report exists.

**VERIFIED, only focus/selection:** one UP with `空き地` (Tanah kosong) value140 focused changes the visible tile focus/panel to Naruto's cell, where the panel shows `レベル` (Level) 1, `結界価値` (Nilai penghalang) 60, `耐久値` (Daya tahan) 2/2. WAIT preserves empty-land140 focus. This proves cursor/board selection only, not actual movement/capture/ownership. Image difference: F60 719,585 pixels/MAD 26.80691; F100 719,273/26.76006; F110 719,213/26.75687; F180 719,644/26.93719.

ACTION output candidate from run #39786019434/artifact #12428777970: `adaptive-cycle-01-f180.sstate`, 21,163,100 bytes, v4, SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`. CONTROL output: 21,162,751 bytes, SHA `eb182a883b1666a7a9badbbf06fda2de960fc84ec4b040799791a174134714a3`. Do not promote either until independently restored.

Next revision41: restore-only from source run #39786019434 / artifact `naruto-storymode-adaptive-player-private` / `adaptive-cycle-01-f180.sstate` / SHA `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`; RESTORE_TEST=1, CONTINUATION_TEST=0, AB_TEST=0, LOOP_CYCLES=1. Require fresh-process load event, five genuine 1280×800 captures retaining Naruto panel/value60, exit0 and external output checkpoint validation. Only if successful promote that input checkpoint; new output remains unpromoted until its own restore. Do not launch another player until prior run ends.

Story Mode remains NOT COMPLETE. Avoid confirm inputs until semantics are clear; all gameplay assets must stay private/out of Git. Use START for dialogue skipping.

---

## ACTIVE QUEUE — revision40 UP vs WAIT; revision39 was a setup-only failure (22 October 2026, 20:21 WIB)

Run [#39786019434](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39786019434) is queued with the corrected marker:
```
MODE=ADAPTIVE
SOURCE_RUN=39779256427
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=UP
AB_EXPECTED_STATE=map_after_move
LOOP_CYCLES=2
REVISION=40
```
Source SHA is from revision33's known map state where `空き地` (Tanah kosong), value140, is focused and which revision34 independently restored. Do not start other player runs concurrently.

Revision39 #39784493293 failed before emulator launch because shell guard still accepted only DOWN/TRIANGLE even though selector/Lua policy allowed UP. Its artifact #12427839381 is only 4,504 bytes with setup information and has no gameplay screenshots; no gameplay conclusion. Workflow corrected in commit #d62a04e831ea185f13efafc5e061d5a8dbb945ce (current workflow blob 73c864d2eba5579be26da732832a467be876b2d1), runtime guard now allows four directions and Triangle.

After revision40 terminates, require: source hash exact per arm, two load events, both F20 map_after_move and pixel-identical, same cloned Memory Cards, UP readback pressed true/released false, WAIT control, ten authentic 1280×800 X11 shots, both exit0, both output checkpoints external validated for size/header/SHA, comparison report. Inspect paired frames before classify. No Circle/confirm, no tile selection. Story Mode remains NOT COMPLETE.

---

## ACTIVE PLAYER — revision39 UP vs WAIT from verified cell-140 state (22 October 2026, 20:11 WIB)

Run #39784493293 is active, started 20:10:11 WIB, timeout about 20:30:11 WIB. Exact committed marker is verified at its checkout: SOURCE_RUN=39779256427; SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private; SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate; SOURCE_SHA256=58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a; RESTORE_TEST=0; CONTINUATION_TEST=0; AB_TEST=1; AB_ACTION=UP; AB_EXPECTED_STATE=map_after_move; LOOP_CYCLES=2; REVISION=39. Workflow blob 5a9b4697b0f19c1c5e8015852f5a90c57261ae9f supports the directional map probe. Do not launch another player.

After completion audit exact source SHA both arms, two SaveStateLoaded events, F20 pixel parity/state, identical cloned Memory Cards, UP press/release readback true/false, WAIT control, ten authentic 1280×800 captures, exits0, both output checkpoints validated for size/v4-header/SHA and comparison report generated. Inspect whether UP changes focus from 空き地 (Tanah kosong), value140, compared with WAIT. Do not confirm a tile.

Source was independently restored in #39780143613. Revision38 output was loadable but its first post-load frame temporarily differed before later frames settled; it is not the preferred continuation source. Story Mode remains NOT COMPLETE, with no confirmed movement/capture/ownership/ending evidence.

---

## ACTIVE PLAYER — revision39 UP versus WAIT from known empty-land state

Run [#39784493293](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39784493293) is active, started 20:10:11 WIB; hard timeout about 20:30:11 WIB. Marker/head SHA `4893e1e0eb6cdcaf9fff052c9c794ae62327858a` is verified; workflow commit `b3c78426f8c11b406f0fedbffb01bd667e7ffb5e` supports map directions. Exact marker pins the independently restored cell140 state from run #39779256427/artifact #12425858092/file adaptive-cycle-01-f180.sstate/SHA `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a` and sets AB_ACTION=UP, AB_EXPECTED_STATE=map_after_move, AB_TEST=1, two cycles, restore/continuation tests off, revision39.

Do not start parallel player. When done, check load events, exact source hashes, pixel-equal F20 / map_after_move, identical memory-card clones, UP readback true/false, WAIT control, 10 authentic 1280×800 captures, two exits0, output checkpoints validated, and report. Manually inspect if UP returns to Naruto tile60 instead of empty land140. No Circle or tile confirmation. Story Mode remains NOT COMPLETE.

Revision38 audit caveat: the second-DOWN candidate was technically loaded but its apparent near-100 F20 visual settled back near 140 by F60; do not treat it as persistent selected-cell change.

---

## REVISION38 AUDIT — load passed, but later frames return to the 140-value board state (22 October 2026, 20:05 WIB)

Run [#39783158903](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39783158903) succeeded. Artifact #12427598163: source hash `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`, 21,162,960 bytes/v4; explicit SaveStateLoaded + restore PASS; 5 genuine 1280×800 screenshots; exit0; new output `c4acb2b62a9891b597c1195a2dead7ccce902abddf0c5ec9b4c50b76142a7a33`, 21,162,978 bytes/v4, externally validated. The F20 screenshot after restore shows a transient scrolled view/number near 100; F60/F100/F110/F180 settle back near the tile value140. All classifier results remain `map_after_move`, so the classifier can't resolve the exact selected tile.

Thus hash 4989… is technically loadable, but do not promote it as a stable continuation cursor state: observed tile/focus appearance does not stay constant through later frames. Run38's output c4ac… stays unpromoted too.

Next revision39: UP vs WAIT from known source run #39779256427 / artifact #12425858092 / `adaptive-cycle-01-f180.sstate` / SHA `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`. This exact input source independently restored in #39780143613 and displayed `空き地` (Tanah kosong), value140 at F20. Set AB_TEST=1, AB_ACTION=UP, AB_EXPECTED_STATE=map_after_move, RESTORE_TEST=0, CONTINUATION_TEST=0, LOOP_CYCLES=2, REVISION=39. Current workflow commit b3c78426 allows map-state directions UP/DOWN/LEFT/RIGHT and only DOWN/TRIANGLE at menu. Ensure marker and checkout use that workflow before trigger. Require all A/B acceptance gates and inspect whether UP switches to Naruto tile value60. No Circle/confirm. Story Mode remains NOT COMPLETE.

---

## REVISION 38 PASSED — source checkpoint independently restorable (22 October 2026, 20:04 WIB)

Run #39783158903 succeeded. Private artifact #12427598163 was re-downloaded and passed ZIP integrity. The fresh process logged ExecutionFlow::SaveStateLoaded and ADAPTIVE_RESTORE_TEST=PASS; five authentic external-X11 screenshots (1280×800), exit code 0, and external output-state size/v4-header/SHA validation all passed. Images retain the board/cursor arrangement after the second DOWN. Early tile digits are partly obscured by animated foliage; later captures clearly show 140.

Restored source from run #39782011370 / artifact #12426797521 / adaptive-cycle-01-f180.sstate: 21,162,960 bytes, v4, SHA-256 `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`. This exact source is promoted as restorable.

New output from #39783158903: 21,162,978 bytes, v4, SHA-256 `c4acb2b62a9891b597c1195a2dead7ccce902abddf0c5ec9b4c50b76142a7a33`. Do not use as a source until independently restored.

Next: make bounded map A/B allow only UP/DOWN/LEFT/RIGHT for directional probes and exclude confirm buttons. Then do RIGHT vs WAIT from the promoted source. Keep all previous paired gates and inspect genuine screenshots; do not confirm any tile. Story Mode remains NOT COMPLETE. No movement/capture/ownership or ending is established. All game assets stay private and out of Git; START skips dialogue.

---

## RESTORE PASS — revision37 ACTION checkpoint independently restored (revision38, 22 October 2026, 20:04 WIB)

Run [#39783158903](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39783158903) success. After an initial corrupted download, a retry of private artifact #12427598163 passed ZIP integrity. Reviewed actual emulator frames C01-F20/F60/F100/F110/F180: post-second-DOWN board/cursor arrangement persists. In F20 the tile digits look like 100 and in F60 142 due transient leaves covering the digits; F100/F110/F180 clearly show 140. Do not treat this as a state-value change.

Source from run #39782011370 / artifact #12426797521 / `adaptive-cycle-01-f180.sstate`: 21,162,960 bytes, v4, SHA-256 `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`. Fresh process logs `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`; five 1280×800 authentic captures; exit0; external output size/header/SHA validation. Exact input SHA 4989… is now promoted as restorable. New output from #39783158903, 21,162,978 bytes, v4, SHA `c4acb2b62a9891b597c1195a2dead7ccce902abddf0c5ec9b4c50b76142a7a33`, not promoted pending its own restore.

Next, modify only the bounded workflow input gate to permit UP/DOWN/LEFT/RIGHT for map A/B probes while still excluding confirm buttons, then revision39 RIGHT vs WAIT from the promoted map checkpoint. Require all paired gates, exact source SHA, 2 load events, pixel-identical F20 state/map_after_move, identical disposable cards, RIGHT true/false input readback, WAIT control, ten real X11 screenshots, exit0 both, checkpoint size/v4-header/SHA validations for both, report generated. Inspect focus change; no confirmation. No parallel player.

Story Mode remains NOT COMPLETE. No evidence of actual movement/capture/ownership. Use START for actual dialogue, keep game files private/out of Git.

---

## LATEST VERIFIED RESULT — revision37 second DOWN changes board focus/view (22 October 2026, 19:56 WIB)

Run [#39782011370](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39782011370) success at 19:54:29 WIB. Private artifact #12426797521 inspected. Both fresh processes restored source SHA `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`; both logged `ExecutionFlow::SaveStateLoaded`; same Memory Card clones; F20 pixels identical 1,024,000/1,024,000; state map_after_move both; DOWN true/false readback; WAIT control; ten authentic 1280×800 X11 captures; exits0; both outputs validated size/v4 header/SHA; comparison report generated.

**VERIFIED, limited to focus/view:** when the empty-land tile value140 is selected, another DOWN shifts the board viewport upward and cursor focus appears toward the adjacent lower cell at the Naruto-marked position. WAIT keeps the pink value60 tile visible above the gray value140 tile and leaves the original framing/cursor. Visual comparison differences F60 780637/MAD22.66488; F100 780562/22.68538; F110 781298/22.66071; F180 780622/22.62887. The classifier reports map_after_move for both; conclusion from authentic paired image inspection. Do not claim actual character movement, territory capture or ownership change.

Checkpoint outputs remain unpromoted:
- ACTION source candidate run #39782011370 artifact #12426797521: `adaptive-cycle-01-f180.sstate`, 21,162,960 bytes, v4, SHA-256 `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`.
- WAIT control: `adaptive-cycle-02-f180.sstate`, 21,163,049 bytes, SHA `cd7a70d67001e67177333df0c332e745e28c01c92851f92c21445250d108c63c`.

Next revision38 restore-only:
MODE=ADAPTIVE
SOURCE_RUN=39782011370
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=DOWN
LOOP_CYCLES=1
REVISION=38

Require fresh load event, five genuine external-X11 captures retaining post-second-DOWN view/focus, exit0, external output state size/header/SHA. Promote only that exact input after success. The next restore output itself remains unpromoted pending another independent restore. Then inspect input mapping and design a next one-variable action to transition from selected map cell toward real Story Mode play. No Circle for dialogue; START only. Story Mode remains NOT COMPLETE.

---

## ACTIVE RUN — revision38 restore second-DOWN viewport checkpoint

Run [#39783158903](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39783158903) active, started 20:00:55 WIB, hard timeout about 20:20:55 WIB. Marker verified:
MODE=ADAPTIVE; SOURCE_RUN=39782011370; SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private; SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate; SOURCE_SHA256=4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177; RESTORE_TEST=1; CONTINUATION_TEST=0; AB_TEST=0; LOOP_CYCLES=1; REVISION=38. Do not start any parallel player.

Upon completion, audit source validation, explicit SaveStateLoaded event, restore PASS, five genuine 1280×800 frames, F20 visual showing the second-DOWN board viewport state, exit0 and new output external size/v4-header/SHA. Only then promote the exact input source hash. New restore output remains unpromoted until a separate fresh-process load succeeds.

Story Mode remains NOT COMPLETE. Directional probes establish view/focus response only, not movement or territory capture. Use START to skip dialogue and keep all game assets out of Git.

---

## LATEST VERIFIED RESULT — repeat DOWN triggers another board-view shift (revision37)

Run [#39782011370](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39782011370) completed success at 19:54:29 WIB. Private artifact #12426797521 audited. Both fresh processes loaded exact parent SHA `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`; two load events; identical cloned cards; F20 exact pixel parity; DOWN press/release true/false; WAIT control; 10 authentic 1280×800 X11 images; exits0 twice; both output savestates externally validated; comparison report generated.

**VERIFIED, narrow:** second DOWN from the post-DOWN scrolled board triggers another upward viewport scroll, keeps the cell information panel hidden, and puts the cursor visually over the lower area near Naruto's marker. WAIT lets the screen settle back to the prior board framing and restores `空き地` (Tanah kosong), value140 panel. Diff metrics F60 780637/MAD22.66488; F100 780562/22.68538; F110 781298/22.66071; F180 780622/22.62887. This is board focus/view response only; target tile semantics, movement, capture and ownership remain unknown.

ACTION candidate from #39782011370 / artifact #12426797521: `adaptive-cycle-01-f180.sstate`, 21,162,960 bytes, v4, SHA-256 `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`. CONTROL output: 21,163,049 bytes, v4, SHA `cd7a70d67001e67177333df0c332e745e28c01c92851f92c21445250d108c63c`. Neither is promoted yet.

Exact revision38: restore-only from run #39782011370/artifact `naruto-storymode-adaptive-player-private`/file `adaptive-cycle-01-f180.sstate`/hash `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`; RESTORE_TEST=1, CONTINUATION_TEST=0, AB_TEST=0, AB_ACTION=DOWN, LOOP_CYCLES=1, REVISION=38. Require load event, five authentic external 1280×800 images retaining post-second-DOWN view, exit0, output checkpoint post-exit external validation. Do not start parallel players; the new revision38 output remains unpromoted until restored separately.

Story Mode remains NOT COMPLETE. Keep all gameplay assets private/out of Git; use START for dialogue.

---

## ACTIVE PLAYER — revision37 tests repeat DOWN from the post-DOWN board view

Only active player is run [#39782011370](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39782011370), started 19:52:49 WIB, hard timeout about 20:12:49 WIB. Marker is verified and pins the independently restored state SHA `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff` from run #39780755350/artifact #12426786721; AB_TEST=1; AB_ACTION=DOWN; AB_EXPECTED_STATE=map_after_move; two cycles; RESTORE_TEST=0; CONTINUATION_TEST=0; revision37. Do not launch another player in parallel.

After the run completes, require both exact source hashes, load events, F20 exact pixel parity plus map_after_move state, identical card clones, true/false DOWN readback, WAIT control, ten authentic X11 screenshots at 1280×800, exits0, both output states post-exit validated, and comparison report. Visually determine whether one more DOWN changes focus/scroll further. No Circle/confirmation. Distinguish tile focus from actual movement or capture; Story Mode remains NOT COMPLETE.

---

## RESTORE PASS — post-DOWN board scroll is a proven restorable checkpoint state (22 October 2026, 19:51 WIB)

Run [#39781495023](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39781495023) success. Inspected private artifact #12426677790. It restored revision35 ACTION output from run #39780755350, source SHA-256 `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff` (21,162,766 bytes, v4); explicit `ExecutionFlow::SaveStateLoaded`, `ADAPTIVE_RESTORE_TEST=PASS`, five real 1280×800 X11 captures, visually retained post-DOWN scrolled board, exit0, and externally validated new output state. Exact input hash b971… is now promoted as independently restorable.

New restore output is not promoted: `adaptive-cycle-01-f180.sstate`, size 21,163,103, v4, SHA-256 `4fd72504031c7aaa73bd7fa18e2f7a8d79b428643cea3c588ea4596ad5e90777`.

Next revision37 is a second DOWN-vs-WAIT probe from trusted post-DOWN view, with source run #39780755350 / private artifact #12426786721 / `adaptive-cycle-01-f180.sstate` / SHA `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`; AB_TEST=1, AB_ACTION=DOWN, AB_EXPECTED_STATE=map_after_move, two cycles, RESTORE_TEST=0, CONTINUATION_TEST=0. Inspect view and tile panel after input. Keep every previous paired acceptance gate. No parallel player, no Circle/confirm. Story Mode NOT COMPLETE.

---

## ACTIVE RUN — revision36 restore-only checkpoint gate (22 October 2026, 19:49 WIB)

Run [#39781495023](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39781495023) is active, started 19:49:08 WIB; hard timeout approximately 20:09:08 WIB. Exact committed marker:
MODE=ADAPTIVE; SOURCE_RUN=39780755350; SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private; SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate; SOURCE_SHA256=b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff; RESTORE_TEST=1; CONTINUATION_TEST=0; AB_TEST=0; LOOP_CYCLES=1; REVISION=36. Do not start parallel players.

Restore source is ACTION output from revision35 DOWN/WAIT A/B, private artifact #12426786721. Required: explicit SaveStateLoaded / ADAPTIVE_RESTORE_TEST, 5 authentic 1280×800 captures with post-DOWN scrolled/focused board view retained, emulator exit0, external size/v4-header/SHA check for the newly emitted output. Promote only the exact input b9717348… upon success; do not promote restore output until that output itself is freshly restored.

Revision35 passed matched A/B and visually showed DOWN causing map viewport/focus movement; WAIT retained empty-land panel. This verifies focus/view response only, not character move or capture. Story Mode remains NOT COMPLETE; use START for dialogue; private game assets never enter Git.

---

## LATEST VERIFIED BOARD NAVIGATION — DOWN scrolls board view from empty-land focus (revision35)

Run [#39780755350](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780755350) fully passed corrected DOWN-vs-WAIT A/B from the independently restored source SHA `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`. Private artifact #12426786721 was inspected. Exact parent source on both fresh processes; two load events; identical cards; F20 state map_after_move and pixel-identical images; DOWN press/release true/false; WAIT control; 10 authentic 1280×800 X11 images; both exits0; both output checkpoints validated for size/v4 header/SHA; comparison report present.

**VERIFIED, strict scope:** when `空き地` (Tanah kosong) value140 is focused on the board, one DOWN changes the observed focus/view: the map scrolls upward and the empty-land information pane disappears, cursor aligns toward the lower tile near Naruto's marker. WAIT retains the empty-land pane and original framing. Since action-state panel doesn't label the new focus, claim only a focus/view change; no assertion that Naruto moved or captured a tile. Visual differences: F60 783594 pixels/MAD27.28084; F100 783324/27.36300; F110 783287/27.31514; F180 783630/27.39113.

ACTION output from run #39780755350, artifact #12426786721, `adaptive-cycle-01-f180.sstate`, 21,162,766 bytes, v4, SHA-256 `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`. CONTROL output 21,162,804 bytes, v4, SHA `e333d408701dcafb40a4d8489a88492fd772a5dc02bdd0fa7b3775bfc1ddc212`. Neither promoted yet.

Exact next step revision36: restore-only fresh process from run #39780755350 / artifact naruto-storymode-adaptive-player-private / checkpoint adaptive-cycle-01-f180.sstate / SHA `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`, with RESTORE_TEST=1, CONTINUATION_TEST=0, AB_TEST=0, LOOP_CYCLES=1, REVISION=36. Require load event, five authentic external 1280×800 frames retaining post-DOWN board state, exit0, external output state validation. Do not launch any player until prior finishes. Newly emitted restore output remains unpromoted until its own fresh-process restore.

Story Mode still NOT COMPLETE. Keep game artifacts private/out of Git; START dialogue skip; no claim of capture or completion without direct evidence.

---

## ACTIVE RUN — revision 35 map DOWN versus WAIT (22 October 2026, 19:44 WIB)

Inspect [run #39780755350](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780755350) first. Current Actions state is `in_progress`, created 19:43:50 WIB; its job is checking out the research repo; no artifact is available yet. Approximate 20-minute timeout: 20:03:50 WIB. Do not run a second player in parallel.

Marker: `SOURCE_RUN=39779256427`, private artifact `naruto-storymode-adaptive-player-private`, checkpoint `adaptive-cycle-01-f180.sstate`, SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`; `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `AB_TEST=1`, `AB_ACTION=DOWN`, `AB_EXPECTED_STATE=map_after_move`, `LOOP_CYCLES=2`, `REVISION=35`. This is a one-input DOWN versus WAIT probe from a fresh-process-restored state where `空き地` (Tanah kosong) / value 140 is focused. Require all standard paired evidence gates. Inspect authentic screenshots; no confirm/select.

---

## ACTIVE PLAYER — revision35 second board-focus probe (22 October 2026, 19:44 WIB)

Run #39780755350 is active, started 19:43:50 WIB; hard timeout about 20:03:50 WIB. Exact pinned source is now independently restored: run #39779256427, private artifact #12425858092, adaptive-cycle-01-f180.sstate, SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`, representing the map with `空き地` (Tanah kosong, barrier value140) focused. Marker verified:
```
MODE=ADAPTIVE
SOURCE_RUN=39779256427
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=DOWN
AB_EXPECTED_STATE=map_after_move
LOOP_CYCLES=2
REVISION=35
```
Workflow currently contains expected map-state gate. Do not run another player in parallel.

Audit after completion: same parent hash in both fresh processes, two `ExecutionFlow::SaveStateLoaded` events, map_after_move F20 exact pixel parity, same cloned Memory Cards, DOWN readback pressed/released true/false, WAIT control, 10 authentic 1280×800 X11 captures, exits0, both output checkpoint external size/header/SHA validators and comparison report. Inspect whether ACTION shifts focus from empty-land140 to the adjacent cell. Until actual images verify, do not classify. No destination confirmation.

Story Mode still NOT COMPLETE. Keep private artifact files out of Git, and use START for dialogue.

---

## LATEST RESTORE VERIFIED — current source is the focused empty-land cell (22 October 2026, 19:42 WIB)

Restore-only run [#39780143613](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780143613) passed. It independently loaded run #39779256427 / private artifact #12425858092 / `adaptive-cycle-01-f180.sstate`, input SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`, 21,162,559 bytes, v4. Artifact #12425913759 log contains `ExecutionFlow::SaveStateLoaded`, `ADAPTIVE_RESTORE_TEST=PASS`, five valid authentic 1280×800 X11 images, emulator exit0, and output state post-exit structural/hash validation. C01-F20 was visually inspected and shows `空き地` (Tanah kosong), barrier value 140, Level ---, durability -/-. The exact input source SHA is now independently restore-proven and promoted.

Restore run's newly generated output is not promoted: `adaptive-cycle-01-f180.sstate`, 21,163,018 bytes, v4, SHA-256 `75f0752616695e0d6d141e3cc051774f5e84defe6944371fb0bc34840c83ce9f`.

Exact next marker revision35:
```
MODE=ADAPTIVE
SOURCE_RUN=39779256427
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=DOWN
AB_EXPECTED_STATE=map_after_move
LOOP_CYCLES=2
REVISION=35
```
Use workflow with expected-state support (main workflow blob SHA `2f3d82359ebbbfeeb705005287c8af7ee3855df0`). Before running verify the committed marker has every field. No player runs concurrently. Required evidence: exact source hash both arms, 2 load events, map_after_move state and pixel-identical F20s, equal card clones, DOWN press/release readback, 10 external X11 images, both exits0, both output checkpoints validated, and comparison report. Inspect the focused cell after DOWN vs WAIT; do not select/confirm any tile.

Previously VERIFIED: menu DOWN row advances in tested states; TRIANGLE from `マップを見る` (Lihat peta) opens board; DOWN on Naruto's focused tile moves focus to adjacent empty land value 140. This does not prove movement/capture/ownership. Story Mode remains NOT COMPLETE. Keep all gameplay artifacts private and out of Git; use START for dialogue.

---

## ACTIVE RUN — restore-test the verified map-direction result (revision34)

Run [#39780143613](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780143613) has been triggered from the correct committed marker, revision34. It restores the ACTION output from revision33, run #39779256427, artifact naruto-storymode-adaptive-player-private, checkpoint adaptive-cycle-01-f180.sstate, SHA-256 58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a. Settings are RESTORE_TEST=1, CONTINUATION_TEST=0, AB_TEST=0, LOOP_CYCLES=1.

Started 19:39:28 WIB; timeout about 19:59:28 WIB. At last check, X11/tools installation was active and artifact not yet available. Do not start parallel player. Confirm explicit ExecutionFlow::SaveStateLoaded, five authentic external 1280×800 captures with empty land 空き地 (Tanah kosong)/value 140 visibly focused, exit 0 and external size/header/SHA validation. Only then promote that exact source. New output from this restore test is not promoted until it too is restored in a further fresh process.

Revision33 rule is VERIFIED in narrow scope: one DOWN changes board focus from Naruto's tile (barrier value 60; Level 1, durability 2/2) to adjacent empty land (空き地 (Tanah kosong), value 140); WAIT preserves Naruto's tile. Does not establish capture, territory ownership or character movement. Story Mode remains NOT COMPLETE.

---

## CURRENT RUN — revision 34 restores the map-focus checkpoint (22 October 2026, 19:39 WIB)

First inspect [run #39780143613](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780143613). It is in progress, started 19:39:28 WIB, with a 20-minute timeout (approx deadline 19:59:28 WIB). This is restore-only; no input is sent. Do not start another player while this run is active.

Source candidate: run #39779256427 / artifact #12425858092 / `adaptive-cycle-01-f180.sstate`, 21,162,559 bytes, `PCSX-Redux SaveState v4`, SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`. Expected screen: the map view retains focus on `空き地` (Tanah kosong), barrier value 140, level --- and durability -/-. Require load event, restore PASS, five genuine 1280×800 external-X11 images, accepted exit code 0, and post-exit external output state validation. Manually inspect C01-F20. Promote this exact source checkpoint only if the new process clearly retains the same tile focus. The output generated by the restore run itself stays unpromoted until a separate restore test.

---

## LATEST VERIFIED RESULT — board DOWN moves focus to adjacent empty land (22 October 2026, 19:38 WIB)

Run [#39779256427](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39779256427) fully passed the corrected matched A/B experiment with AB_EXPECTED_STATE=map_after_move. Private artifact #12425858092 was downloaded after upload completed and audited. Both arms restored source SHA b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc in two fresh processes; two load events; identical card clones; exact F20 parity (0/1,024,000 differing pixels); DOWN input readback true/false; WAIT control; 10 valid authentic 1280×800 X11 captures; exits 0; both output checkpoints externally validated for size/v4 header/SHA; comparison report exists.

**VERIFIED (narrow):** on the map board with the Naruto tile focused, one DOWN changes the focused tile to adjacent 空き地 (Tanah kosong) valued 140; WAIT retains Naruto's tile. ACTION C01-F60 shows 空き地 (Tanah kosong), レベル (Level) ---, 結界価値 (Nilai penghalang) 140, 耐久値 (Daya tahan) -/-. CONTROL C02-F60 shows Naruto, レベル (Level) 1, 結界価値 (Nilai penghalang) 60, 耐久値 (Daya tahan) 2/2. This only verifies tile focus; no character movement/capture/ownership change is claimed. Pixel differences: F60 719,192 / mean abs RGB 26.80650; F100 719,200 / 26.89202; F110 719,631 / 26.85752; F180 718,997 / 26.84018. Classifier remains map_after_move for both, so manually inspect screenshots.

ACTION checkpoint candidate from #39779256427, artifact #12425858092: adaptive-cycle-01-f180.sstate, 21,162,559 bytes, v4 header, SHA-256 58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a. CONTROL output 21,162,390 bytes SHA-256 3796ff4ba91fef93ddf1078daa1785e043c3d5b5424a03c8cb53a62c6d3858a4. Neither output promoted yet.

Exact next marker, revision 34 restore-only:
MODE=ADAPTIVE
SOURCE_RUN=39779256427
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=DOWN
LOOP_CYCLES=1
REVISION=34

Require load event, five authentic X11 frames showing 空き地 (Tanah kosong) / tile value 140 still focused, exit 0, and external output size/header/SHA validation. If successful, promote the source checkpoint. Do not start another player concurrently; then plan the next controlled tile-navigation/selection probe without confirming any destination.

Story Mode remains NOT COMPLETE. No authenticated ending/results evidence. All gameplay assets remain private/out of Git, and dialogue must be skipped with START.

---

## VERIFIED RESULT — map DOWN selection and revision 34 restore gate (22 October 2026, 19:37 WIB)

Run [#39779256427](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39779256427), revision 33, completed success. Private artifact #12425858092 was audited end-to-end.

Matched gates passed: same source SHA in two fresh processes (`b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`); two `ExecutionFlow::SaveStateLoaded` events; identical cloned Memory Cards (`ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`); F20 pixels identical over 1,024,000 pixels and both states `map_after_move`; DOWN press/readback true and release/readback false; control WAIT; ten authentic 1280×800 external-X11 captures; both emulator exits 0; both output checkpoint states passed post-exit size/v4-header/SHA validation. A/B report generated successfully. Pixel differences: F60 719,192 / MAD 26.80650; F100 719,200 / 26.89202; F110 719,631 / 26.85752; F180 718,997 / 26.84018.

**VERIFIED (scoped):** one DOWN from map state switches the focused tile from Naruto's tile (level 1, barrier value 60, durability 2/2) to the adjacent empty land `空き地` (Tanah kosong) with value 140, level --- and durability -/-. WAIT stays on the original tile. This proves focus/selection changes only—not avatar movement, ownership, capture, or turn rules. Actual screenshots were manually compared; classifier label remains `map_after_move` for both branches.

Do not promote either revision33 output before restore. ACTION candidate: source run #39779256427 / private artifact #12425858092 / `adaptive-cycle-01-f180.sstate` / 21,162,559 bytes / SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`, v4. CONTROL output SHA `3796ff4ba91fef93ddf1078daa1785e043c3d5b5424a03c8cb53a62c6d3858a4`, 21,162,390 bytes, v4. Neither is promoted.

Next, revision 34 restore-only using ACTION candidate:
```
MODE=ADAPTIVE
SOURCE_RUN=39779256427
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=DOWN
LOOP_CYCLES=1
REVISION=34
```
No input is allowed. Require fresh-process load event, five real 1280×800 external-X11 captures, accepted exit, external output validation, and manual visual confirmation that F20 still focuses the empty-land 140 tile. Only then promote the input checkpoint. New output from the restore-only process remains unpromoted until that output itself is restored.

Story Mode is NOT COMPLETE; no authentic ending/result evidence. Do not confirm map destination or use Circle to skip dialogue; use START.

---

## CURRENT RUN — revision 33 explicit map-state A/B (22 October 2026, 19:33 WIB)

Inspect [run #39779256427](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39779256427) first. It is `in_progress`, created 19:32:59 WIB, with X11 tool preparation currently active. Job timeout: 20 minutes, approximate deadline 19:52:59 WIB. No player run may be launched in parallel.

Marker is explicitly configured:
```
MODE=ADAPTIVE
SOURCE_RUN=39776518701
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=DOWN
AB_EXPECTED_STATE=map_after_move
LOOP_CYCLES=2
REVISION=33
```
This uses the already fresh-process-restored map checkpoint. Required acceptance gates: both branches use the exact parent SHA, cloned Memory Cards hash-identical, F20 state `map_after_move` and pixel-perfect images, separate `ExecutionFlow::SaveStateLoaded` events, DOWN press/release readback true/false, ten authentic external 1280×800 X11 captures, accepted exit code 0, both output states pass external size/header/SHA validation, and the comparison report completes. Afterward inspect actual paired F60/F100/F110/F180 images.

Run #39777917775 remains a failed workflow execution due its obsolete F20 semantic state expectation (menu) even though both branches loaded the exact map parent, F20 images were pixel-identical, DOWN input was sent/read back, ten authentic captures existed, both exits were zero and both outputs passed structural validation. Screenshots suggest (HYPOTHESIS pending clean run33) DOWN moves focus from the Naruto tile, `結界価値` (Nilai penghalang) 60 / `耐久値` (Daya tahan) 2/2, to the adjacent empty tile `空き地` (Tanah kosong), value 140. Neither failed-run output is promoted. Do not confirm any tile or use Circle to skip dialogue.

---

## ACTIVE PLAYER — revision 33 corrected map DOWN/WAIT experiment (22 October 2026, 19:33 WIB)

Player run [#39779256427](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39779256427) is active; it started 19:32:59 WIB and has hard timeout about 19:52:59 WIB. Do not start another player until it finishes. The committed marker now includes AB_EXPECTED_STATE=map_after_move, AB_ACTION=DOWN, AB_TEST=1, LOOP_CYCLES=2, RESTORE_TEST=0, CONTINUATION_TEST=0, source run #39776518701 / artifact naruto-storymode-adaptive-player-private / file adaptive-cycle-01-f180.sstate / SHA b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc.

Audit run #39779256427 after completion. Required: both fresh processes load the exact parent hash and log SaveStateLoaded; F20 state in both arms exactly map_after_move and images pixel-identical; cloned disposable Memory Cards identical; ACTION DOWN input readback true/false; control WAIT; all ten authentic 1280×800 X11 captures; both emulator exit codes 0; output states post-exit validated for size, v4 header and SHA; and ab-comparison-report.txt generated. Inspect actual images before classifying any result.

Revision 32 (#39777917775) ran the same input but its workflow checkout hard-coded F20 states to menu_or_unknown_choice, so the workflow failed at that late gate despite valid captures, exits and checkpoint structures. Its images suggest DOWN moved focus from Naruto's tile to empty land (空き地, Tanah kosong) with barrier value 140; control remains on Naruto's tile value 60. This stays HYPOTHESIS until the corrected revision33 gate fully passes. Do not select/confirm a tile. Story Mode remains NOT COMPLETE.

---

## REVISION 32 RESULT — evidence captured; corrected run needed because validator expected menu (22 October 2026, 19:30 WIB)

Run [#39777917775](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39777917775) finished failure. The emulator work itself completed: both fresh processes loaded source SHA b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc and logged SaveStateLoaded; C01/C02 F20 images were pixel-identical; DOWN press/release was true/false; WAIT control sent no button; all 10 authentic external-X11 captures passed at 1280×800; both emulator exits were 0; both output checkpoints passed size/v4-header/SHA validation. Artifact #12426395775 is private.

Why workflow failed: run checkout SHA b77f74af5b258dfcd7d8bfbeeeca0c685c5fc7b7 did not include AB_EXPECTED_STATE support and its Python validation explicitly required both F20 states to equal menu_or_unknown_choice. Actual states were map_after_move/map_after_move, as expected from the source, so the gate failed and no ab-comparison-report.txt was written. Treat run #39777917775 as **not a clean A/B pass**.

Actual screenshots were manually inspected and suggest that DOWN changes focus from the Naruto tile (Level 1, barrier value 60, durability 2/2) to an adjacent empty-land tile marked 空き地 (Tanah kosong), barrier value 140, with action/control image difference >719,000 pixels after input. This is currently HYPOTHESIS, not VERIFIED. Output states ACTION SHA 927d87eb775f375deb47af348d837319ceb65d4baa58c8523042090f377b2efa (21,162,270 bytes) and CONTROL SHA 7aaf5fc780748fee27a84669a942c598e8340e9952234e47bab47795755d67a1 (21,162,320 bytes) passed structure validation but are not promoted.

Latest main workflow commit 4c074472e885c75ce618e4e0f5aefd6a8833a0c9 adds explicit AB_EXPECTED_STATE. Now rerun as revision 33 with this exact marker:
MODE=ADAPTIVE
SOURCE_RUN=39776518701
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=DOWN
AB_EXPECTED_STATE=map_after_move
LOOP_CYCLES=2
REVISION=33

Re-read the committed marker literal before launch. Require 2 load events, exact source SHA per arm, matched map_after_move F20 state and pixel parity, input readback, ten authentic captures, exit code 0, both checkpoint validations, and a generated ab-comparison-report.txt. Do not start parallel player runs. If DOWN again changes the focused empty land from Naruto's tile without confirmation, that can be classified narrowly as VERIFIED; don't use Circle and don't select a destination.

Story Mode remains NOT COMPLETE. Use START for actual dialogue; keep private artifacts outside Git.

---

## CORRECTION — current revision 32 checkout has a late A/B validator mismatch (22 October 2026, 19:25 WIB)

Run #39777917775 is still the only active player; do not start another. Important correction to the previous section: workflow checkout SHA b77f74af5b258dfcd7d8bfbeeeca0c685c5fc7b7 does NOT use AB_EXPECTED_STATE. Its Lua precondition accepts either menu_or_unknown_choice or map_after_move when the classifier action is WAIT, so the ACTION arm may indeed send DOWN from the board. But a later shell gate and the Python state-parity validator hard-code menu_or_unknown_choice; the run can therefore fail after valid captures, input readback and state-file checks. Do not assume no input was sent; audit the actual branch stdout and screenshot artifact.

After the run terminates, check all 10 authentic screenshots, source hashes, F20 parity, explicit load events, DOWN press/release true/false, exits and output-state validation. Even if visual movement appears, treat it as HYPOTHESIS unless the required paired gates pass. Corrected workflow commit 4c074472e885c75ce618e4e0f5aefd6a8833a0c9 adds AB_EXPECTED_STATE; a clean rerun needs a fresh marker including AB_EXPECTED_STATE=map_after_move, only after this run ends.


---

## ACTIVE BLOCKER — revision 32 did not include its expected map state (22 October 2026, 19:24 WIB)

Run [#39777917775](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39777917775) is the only active player; last check had X11 workspace installation in progress, started 19:23:17 WIB, timeout at about 19:43:17 WIB. Marker content at the current committed blob has no AB_EXPECTED_STATE field, so workflow defaults it to menu_or_unknown_choice while source SHA b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc is map_after_move. The input precondition should fail closed, selecting WAIT rather than DOWN, then likely fail final assertions. This is a configuration bug, not a gameplay finding. Do not run another player until #39777917775 completes and is audited.

When run finishes, inspect log/artifact. If precondition failed, set a fresh marker revision 33 with exact source run #39776518701/artifact naruto-storymode-adaptive-player-private/checkpoint adaptive-cycle-01-f180.sstate/SHA b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc and add AB_EXPECTED_STATE=map_after_move, AB_TEST=1, AB_ACTION=DOWN, LOOP_CYCLES=2, RESTORE_TEST=0, CONTINUATION_TEST=0. Re-read the committed marker to verify the field exists before treating the run as ready. Workflow commit 4c074472e885c75ce618e4e0f5aefd6a8833a0c9 added support for the expected state but this marker omission prevents using that support.

Previously verified: revision 30 Triangle opens the board view; revision 31 restores that map-view checkpoint in a fresh process. Board directional behavior remains unknown until corrected A/B succeeds. Story Mode remains NOT COMPLETE.

---

## LATEST RESTORE PASS — map view checkpoint is usable (22 October 2026, 19:21 WIB)

Run [#39777301626](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39777301626) passed a fresh-process restore of the Triangle/ACTION map-view candidate from #39776518701. Exact source: 21,163,227 bytes, PCSX-Redux SaveState v4, SHA-256 b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc. Evidence in private artifact #12423949987: explicit ExecutionFlow::SaveStateLoaded, ADAPTIVE_RESTORE_TEST=PASS, five validated authentic 1280×800 X11 captures, F20 through F180 remain in map_after_move, emulator exit 0, and output size/header/SHA validation. The exact source hash is now promoted as an independently restored continuation checkpoint.

New unpromoted output from restore run #39777301626: 21,162,251 bytes, v4, SHA-256 a2a3c36918155dc4356da2664bfa7880c9605c62260389b85f85262c942b2fe7.

The workflow A/B precondition now takes AB_EXPECTED_STATE. Commit 4c074472e885c75ce618e4e0f5aefd6a8833a0c9 allows the verified map_after_move state only with a DOWN probe, and dynamically checks both branches' expected start state rather than assuming a menu. This new workflow logic remains untested until revision 32 completes.

Exact next marker:
MODE=ADAPTIVE
SOURCE_RUN=39776518701
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=DOWN
AB_EXPECTED_STATE=map_after_move
LOOP_CYCLES=2
REVISION=32

Require F20 map_after_move state in both arms, pixel-exact parity, two explicit load events, identical disposable Memory Cards, DOWN press/release readback, ten authentic 1280×800 frames, accepted exit 0 and both output checkpoint external validations. Compare F60/F100/F110/F180 from ACTION vs WAIT. Do not confirm/select a destination; stop at the first changed selection/state. No parallel player runs.

Story Mode remains NOT COMPLETE. Existing VERIFIED scope: menu DOWN advances the observed row; Triangle from View map opens the board view. Rules for board navigation/territory capture/combat remain unknown until paired evidence. Use START for dialogue skipping and keep gameplay assets private/out of Git.

---

## CURRENT RUN — revision 32 is active (22 October 2026, 19:23 WIB)

Exact run to inspect first: [#39777917775](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39777917775). It started at 19:23:17 WIB; latest state is `in_progress`, with `Install X11 tools and prepare private workspace` active. Hard job timeout: 20 minutes from runner start, approximate deadline 19:43:17 WIB. Wait for this player run to finish; do not trigger a parallel run.

Revision 32 config: source run #39776518701, artifact `naruto-storymode-adaptive-player-private`, checkpoint `adaptive-cycle-01-f180.sstate`, SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`; `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `AB_TEST=1`, `AB_ACTION=DOWN`, `LOOP_CYCLES=2`, `REVISION=32`. ACTION DOWN versus control NONE/WAIT from map view. Workflow commit `5f8ae63b4374cb730ef197d797dffd0e823db141` extends the starting precondition to accept `map_after_move` with classifier action WAIT.

When complete, audit raw logs and artifact: ensure exact source SHA both branches; F20 images/state match; one DOWN press/release is read back `true`/`false`; both `ExecutionFlow::SaveStateLoaded` events; 10 authentic 1280×800 X11 screenshots; both process exits accepted; both output states externally validate size, v4 header and SHA-256. Visually inspect F60/F100/F110/F180 action and control images to classify the map response. Never confirm a destination. No result is available yet; Story Mode remains NOT COMPLETE.

---

## LATEST CHECKPOINT — map view restores cleanly; next run revision 32 (22 October 2026, 19:20 WIB)

Run [#39777301626](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39777301626) restore-only completed with success at 19:20:11 WIB. Private artifact #12423949987 was audited and C01-F20 visually opened. It proves the map view is restored in a fresh emulator process:
- Source from run #39776518701 / artifact #12425305517 / `adaptive-cycle-01-f180.sstate`; 21,163,227 bytes; v4 header; SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`.
- `ExecutionFlow::SaveStateLoaded`, `ADAPTIVE_RESTORE_TEST=PASS`, five authentic external-X11 images at 1280×800, exit 0, source and output integrity checks passed. Manually reviewed F20 shows the same map/tile view, status panel and footer `× もどる` (X: Kembali), with no input issued by the restore run.
- Therefore promote source SHA `b5715ba7...` as the trusted map-view state.
- New output SHA `a2a3c36918155dc4356da2664bfa7880c9605c62260389b85f85262c942b2fe7`, 21,162,251 bytes, v4, emitted by the restore process is still not trusted until a separate restore test.

Workflow commit `5f8ae63b4374cb730ef197d797dffd0e823db141` now allows the A/B initial precondition from `map_after_move` with classifier action WAIT (or the former right-menu state). The prior precondition blocked a map-origin action probe despite the source being visually calibrated. This change only edits the workflow path; it does not start a player run.

### Next run — revision 32, map DOWN vs WAIT
```
MODE=ADAPTIVE
SOURCE_RUN=39776518701
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=DOWN
LOOP_CYCLES=2
REVISION=32
```
ACTION will send exactly one DOWN at the established input window; CONTROL waits. This is a navigation observation only: no Circle/confirmation and no map destination selection. Require same source SHA in both arms, same F20 pixels and state, both load events, input true/false readback, ten authentic 1280×800 X11 captures, exits, and external validation of both outputs. Manually compare screenshots at F60/F100/F110/F180; do not treat `map_after_move` label alone as a proven cursor movement. Keep classification scoped to what the screenshots directly establish.

Rule table in brief:
- **VERIFIED:** DOWN from `情報` (Informasi) highlights `マップを見る` (Lihat peta).
- **VERIFIED:** TRIANGLE with `マップを見る` (Lihat peta) highlighted opens tile/map view; WAIT stays in menu.
- **VERIFIED:** map checkpoint SHA `b5715ba7...` restores and keeps the map view visible.
- **UNKNOWN:** what DOWN does from the map/tile view; movement, costs, territory/barrier behavior and combat are not yet established.
Story Mode is NOT COMPLETE; no authentic ending/results image. Keep all artifacts private/out of Git; use START to skip dialogue.

---

## LATEST VERIFIED RULE — TRIANGLE from View map opens the board (22 October 2026, 19:15 WIB)

Run [#39776518701](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39776518701) successfully completed the paired TRIANGLE-vs-WAIT experiment. Private artifact #12425305517 inspected. Same source parent in both arms: SHA `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7`; separate fresh emulator processes, two explicit `ExecutionFlow::SaveStateLoaded` logs, equal cloned Memory Cards, pixel-identical F20 parent frames, Triangle press true / release false readback, ten valid 1280×800 external-X11 captures, exit 0 for both sessions, and both checkpoint output files passed external size/header/SHA validation.

Visual rule classification: **VERIFIED, scoped to this menu state** — with `マップを見る` (Lihat peta) highlighted, one TRIANGLE opens the board/map view; control WAIT leaves the selection menu open. Actual ACTION screenshot C01-F60 shows the forest board, Naruto marker/status panel (`レベル` (Level) 1, `結界価値` (Barrier value) 60, `耐久値` (Durability) 2/2) and footer `△ マップ` (Triangle: Map); control C02-F60 shows the same menu rows and red highlight at View map. Differences: 286,259 pixels (mean abs RGB 21.80974) at F60; 282,661/21.70455 at F100; 279,162/21.18977 at F110; 286,921/21.80548 at F180. The agent classifier reports `map_after_move` in ACTION and `menu_or_unknown_choice` in control. No map destination was selected.

ACTION output candidate from run #39776518701 / private artifact #12425305517: `adaptive-cycle-01-f180.sstate`, 21,163,227 bytes, v4 header, SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`. Control output is 21,163,215 bytes, hash `dc91b2756581456e75dee8cd836dc7b3c1e43fde88978dbf15545f231a6c0f98`. Neither output is promoted yet.

Exact next step: configure revision 31 as a restore-only smoke of the ACTION/map-view candidate:
```
MODE=ADAPTIVE
SOURCE_RUN=39776518701
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=DOWN
LOOP_CYCLES=1
REVISION=31
```
Require explicit load event, five authentic X11 screenshots showing map view retained at F20, successful exit and external validation of its new output checkpoint. Do not trigger parallel player runs. Once revision31 is verified, use the restored map state for a single DOWN-vs-WAIT probe in two fresh processes; inspect tile highlight/state first and do not confirm/choose a destination unless the intended item is visibly clear.

Story Mode still NOT COMPLETE. Never claim ending without authentic in-game ending/results evidence. Use START to skip dialogue; Japanese text must include adjacent Indonesian translations; all gameplay artifacts remain private/out of Git.

---

## LATEST VERIFIED RESULT — Triangle opened the map view; next restore-only (22 October 2026, 19:15 WIB)

Run [#39776518701](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39776518701), revision 30, completed with success at 19:14:34 WIB. Private artifact #12425305517 was audited.

**VERIFIED in this exact state:** The matched ACTION TRIANGLE branch enters a map/tile view from the right-side menu with `マップを見る` (Lihat peta) highlighted; the NONE/WAIT control remains in the prior menu. Parent SHA for both: `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7`. F20 images were pixel-identical across 1,024,000 pixels; each process logged `ExecutionFlow::SaveStateLoaded`; Triangle press/release readback passed true/false; ten authentic external-X11 captures validated at 1280×800; both processes exited 0 and both outputs passed external post-exit size/header/SHA validation. Paired differences: F60 286,259 pixels (MAD 21.80974), F100 282,661 (21.70455), F110 279,162 (21.18977), F180 286,921 (21.80548). Screenshot F60 and F180 in ACTION clearly show the hex/tile view and footer `× もどる` (X: Kembali), while CONTROL remains in menu. No map target was selected.

ACTION candidate output from run #39776518701, artifact #12425305517: `adaptive-cycle-01-f180.sstate`, 21,163,227 bytes, v4, SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`. This new output is still not promoted until it is independently restored. CONTROL output: 21,163,215 bytes, SHA-256 `dc91b2756581456e75dee8cd836dc7b3c1e43fde88978dbf15545f231a6c0f98`; also not promoted.

Next is revision 31 restore-only from the ACTION candidate:
```
MODE=ADAPTIVE
SOURCE_RUN=39776518701
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=DOWN
LOOP_CYCLES=1
REVISION=31
```
This must send no gameplay input. Require the explicit load event, five authentic 1280×800 post-load X11 captures, accepted exit and external output validation; manually verify that F20 retains the map view. On success, source run #39776518701's ACTION output is a trusted map-view checkpoint. After that, begin one-variable map movement probes from the inspected state. Do not choose a target until the actual map layout and on-screen costs are understood.

Story Mode is NOT COMPLETE; no ending/results evidence exists. Keep all gameplay files out of Git and private; use START for Story Mode dialogue skipping.

---

## RESTORE SMOKE PASSED — exact next step revision 30 (22 October 2026, 19:11 WIB)

Run [#39776089816](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39776089816) completed with Actions success. Audited its private artifact #12425065836: source from run #39775176728, SHA-256 `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7`, size 21,162,344, header v4; `ExecutionFlow::SaveStateLoaded` plus `ADAPTIVE_RESTORE_TEST=PASS`; five authentic 1280×800 external-X11 screenshots; exit 0; external post-exit checkpoint validation. C01-F20 was opened and visibly shows `マップを見る` (Lihat peta) selected. Thus the revision-28 ACTION output is now an independently restored, trusted source checkpoint.

The restore run emitted a new output state, 21,163,104 bytes, v4, SHA-256 `9d1ed105227c095c42396595bccd51ecf06f564ae5342f01377dec1f3aa94292` in private artifact #12425065836. Do not promote this *new* output until it is independently restored.

Next, revision 30 is a matched TRIANGLE-vs-WAIT test from the original, now proven-restorable checkpoint in run #39775176728/artifact #12424660712:
```
MODE=ADAPTIVE
SOURCE_RUN=39775176728
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=TRIANGLE
LOOP_CYCLES=2
REVISION=30
```
ACTION sends Triangle at the F30-F38 input window; CONTROL sends WAIT. Required gates: both arms load this exact source SHA in separate processes; identical F20 pixels and menu state; Triangle press/release readback; both load events; 10 authentic X11 captures; accepted exits; external post-exit size/header/SHA for both output states. Inspect actual paired screenshots for map-screen entry; classifier `menu_or_unknown_choice` alone is not sufficient. If the map opens, stop and inspect it; do not choose a destination. Do not start a parallel run.

Revision 28 VERIFIED DOWN rule remains narrow: Information→`マップを見る` (Lihat peta) highlight. Story Mode remains NOT COMPLETE; keep gameplay artifacts private/out of Git, use START to skip Story Mode dialogue, translate Japanese text alongside it.

---

## LATEST VERIFIED RESULT / EXACT NEXT ACTION — revision 28 completed (22 October 2026, 19:05 WIB)

Run [#39775176728](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39775176728) has completed successfully. I inspected the actual private artifact #12424660712 (not just the Actions conclusion). Source for both arms was the exact restorable parent SHA-256 `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`; separate fresh processes logged `ExecutionFlow::SaveStateLoaded`; Memory Card clones had identical SHA; F20 screenshots matched across 1,024,000 pixels; DOWN press/release readback was true/false; all 10 external-X11 captures validated at 1280×800; both emulator processes exited 0; both output checkpoints passed external size/v4-header/SHA validation.

Actual screenshot review proves the narrow menu rule **VERIFIED**: from `情報` (Informasi), one DOWN moves selection to `マップを見る` (Lihat peta) by F60; the NONE/WAIT control stays on Information through F180. Reported post-action difference is 14,636 pixels / mean absolute RGB difference 1.05798 at F60, F100, F110, F180. Classifier labels remain generic `menu_or_unknown_choice`; do not claim semantic classifier recognition.

Outputs:
- ACTION source candidate from run #39775176728, artifact #12424660712, `adaptive-cycle-01-f180.sstate`: 21,162,344 bytes, SHA-256 `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7`, v4 header, externally validated. **Not promoted yet** until restored in a new process.
- NONE control `adaptive-cycle-02-f180.sstate`: 21,162,426 bytes, SHA-256 `30b062df8985fa79f8c9f79e076cb464f1ff73143103e249dba5d35ca94324d5`, v4 header, externally validated; not a preferred continuation source.

Next exact step: launch one non-parallel restore smoke using the ACTION candidate above:
```
MODE=ADAPTIVE
SOURCE_RUN=39775176728
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=DOWN
LOOP_CYCLES=1
REVISION=29
```
After the fresh-process restore, verify load event, five authentic X11 captures, that the Information menu remains with `マップを見る` (Lihat peta) highlighted, accepted emulator exit, and external output size/header/SHA. The exact INPUT source SHA is promoted only if that test proves it was loaded in the new process and visually retains state. Then run a separate matched `TRIANGLE` versus `WAIT` probe from this restored map-row selection (new revision 30 only after revision 29 finishes); capture F20/F60/F100/F110/F180 in both arms, check parity/input readback/two load events/exits/checkpoints, and stop at the map screen without selecting a destination.

Story Mode remains NOT COMPLETE. No ending/results screenshot verified; never claim completion. Keep all gameplay artifacts private/out of Git; use START for dialogue skipping; add Indonesian translations alongside Japanese text.

---

## CURRENT ACTION — revision 28 matched DOWN/NONE run queued (22 October 2026, 19:02 WIB)

Marker revision 28 was committed at `e31ebb2afbe1145746e480e9a0f020854621a82f`, triggering [run #39775176728](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39775176728). At the latest check it is **in progress**, with the step `Install X11 tools and prepare private workspace` active. It started at 19:02:38 WIB; the workflow job has a 20-minute hard timeout (around 19:22:38 WIB if not completed earlier). It tests ACTION=DOWN against NONE/WAIT from the known-restorable Information parent `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`; 2 cycles, `AB_TEST=1`. Do not start another player run. Next chat must check this exact run, its latest job steps and artifacts/logs, then apply the strict paired-evidence gates documented here. Job timeout is 20 minutes after a runner starts; queued wait has no reliable ETA. Story Mode remains NOT COMPLETE.

---

## LATEST RESULT — smoke completed successfully; next paired DOWN test (22 October 2026, 18:48 WIB)

Run [#39772650469](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39772650469) completed successfully (run #27 / revision 27). It restored source checkpoint SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e` from #39768787669, logged `ExecutionFlow::SaveStateLoaded`, captured five authentic 1280×800 external-X11 frames, exited 0, and validated its new output after exit. Output hash: `cb53613ffa09e57d0f6d927d9e82bf603937871a07a9ed24c0955735cf258fdc`; size 21,162,547 bytes; v4 header; private artifact #12422499045. F20 visibly retains `情報` (Informasi) selected. This passes the shutdown smoke, but the new output file remains **unpromoted until that output itself is restored in a fresh process**.

The next marker revision 28 has been prepared to run a matched A/B from the exact same known-restorable parent SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`: ACTION=DOWN vs control NONE/WAIT; `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `AB_TEST=1`, `LOOP_CYCLES=2`. Check the current run before launching anything else. Required evidence: identical F20 pixels/state, DOWN press/release readback, two `ExecutionFlow::SaveStateLoaded` logs, ten valid authentic X11 screenshots, both process exits accepted, and both output savestates externally passing size/header/SHA checks. Do not promote either new output until each is restored in a fresh process. If push has not created a run, inspect the commit/Actions state before retrying; never create parallel player runs.

Verified menu facts remain narrowly scoped: from the exact parent menu, DOWN moves Roulette→Ninjutsu and then Ninjutsu→Information with paired control evidence. Information→`マップを見る` (Lihat peta) remains HYPOTHESIS pending the matched DOWN/NONE result. Story Mode remains NOT COMPLETE. Follow all privacy/input constraints in the existing handoff below.

---

## ACTIVE RUN — revision 27 restore smoke using single-nextTick shutdown (22 October 2026, 18:45 WIB)

Run [#39772650469](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39772650469) is in progress with `RESTORE_TEST=1`, one cycle, pinned source SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e` from #39768787669's already-restored Information-selection checkpoint. It started 18:42:49 WIB; at 18:45 WIB it was still installing X11 tools (that step started 18:43:28 WIB). No new frames/artifact yet; don't start a parallel run.

Workflow commit `df6e3d5afab0a9efeac89aa8bcb0be2e273ef631` uses single pause + `PCSX.nextTick(function() PCSX.quit(0) end)` outside VSync; recursive drains are removed because they stalled under pause. Await audit of load event, five authentic X11 frames, emulator exit and external post-exit state size/header/SHA. Only then retry A/B on the same pinned source.

Story Mode remains NOT COMPLETE; DOWN from `情報` (Informasi) to `マップを見る` (Lihat peta) remains HYPOTHESIS without a completed NONE branch.

---

## LATEST DIAGNOSTIC — paused nextTick drain stalled; single-nextTick restored and smoke test next (22 October 2026, 18:39 WIB)

- A/B retry #39771377339 did not complete. It captured five genuine ACTION-arm X11 frames; source Information checkpoint hash remained `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`, identical Memory Card clones, and DOWN press/release readbacks were valid. The output checkpoint in private artifact #12423430123 is 21,162,276 bytes with v4 header and SHA-256 `a2d055634da951b8c9703ac1d30ac0981d4508404527604ddf4e803fe08935b5`; however, a chained 12-callback `nextTick` drain while paused did not progress, so watchdog rc=124 killed the session before the control branch. Do not promote this output, and do not mark the Information→Map item behavior VERIFIED.
- Previous VSync drain test #39770465538 also timed out rc=124. Its output file was full-size with v4 header in its private artifact, but clean process completion was not achieved.
- Workflow commit `df6e3d5afab0a9efeac89aa8bcb0be2e273ef631` restores the known established single quit callback outside VSync: pause then `PCSX.nextTick(function() PCSX.quit(0) end)`. Shell validation still happens after the emulator exits. Native exit 139 is accepted only if session finished and the state validates externally.
- Visual review of the one-arm #39771377339 frames suggests DOWN moved the selection from `情報` (Informasi) to `マップを見る` (Lihat peta), but the NONE control was not run; classify this as HYPOTHESIS only.

Next trigger revision 27 with `RESTORE_TEST=1`, `LOOP_CYCLES=1`, source the already restore-validated checkpoint `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e` from run #39768787669. Require explicit `ExecutionFlow::SaveStateLoaded`, five authentic post-load X11 images, end-of-process result and externally validated output state. Only then retry A/B.

Story Mode remains NOT COMPLETE; private gameplay assets remain out of Git.

---

## LATEST DIAGNOSTIC — second Information-down A/B attempt timed out; nextTick-drain retry next (22 October 2026, 18:31 WIB)

- Run [#39770465538](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39770465538) timed out (exit 124) before the control branch. It had five valid authentic ACTION frames, DOWN press/release readback, identical cloned Memory Card hashes and exact parent source `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`. The 12-VSync drain did not progress after save; emulator did not exit before 120s. Private artifact #12422367156 contains an apparently full-size checkpoint (21,162,494 bytes, v4 header, SHA-256 `0c33a47cb9e6f2dfb09c568410ca125acbae6f46f84692b8589a5c903442f564`) and authentic screenshots showing the ACTION branch highlight on `マップを見る` (Lihat peta) from F60 onward, but no NONE control branch was produced and exit 124 means the official post-exit workflow guard did not pass. Keep the action result HYPOTHESIS and do not use its output as a trusted source.
- Workflow commit `3e052b8e77cfcd966f5e5e05a2f7341ed2ff0374` removes the VSync countdown and uses a paused recursive chain of 12 `PCSX.nextTick` callbacks before quit; not yet validated.
- Next run is marker revision 26, same known-restorable Information parent SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`, ACTION=DOWN versus NONE/WAIT, two cycles. Require the whole matched audit and structural/hash validation for both checkpoint outputs before making a rule VERIFIED. No Circle confirmation.

Story Mode remains NOT COMPLETE.

---

## LATEST DIAGNOSTIC — checkpoint full-sized, but drain stalled and process timed out (22 October 2026, 18:31 WIB)

Story Mode is **NOT COMPLETE**. No ending/results screenshot exists.

- Run [#39770465538](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39770465538) failed in the first ACTION branch before control/NONE ran. It captured five authentic 1280x800 X11 frames and DOWN readback passed. It logged session finished and drain begin but not drain pass; emulator timeout exit was 124.
- The private artifact #12422367156 contains the full-sized checkpoint, 21,162,494 bytes, v4 header, SHA-256 `0c33a47cb9e6f2dfb09c568410ca125acbae6f46f84692b8589a5c903442f564`. Though structurally full-sized, it came from a timeout session and is **not trusted**; do not use it as a source. The NONE branch did not run, so no matched A/B conclusion.
- Root cause of the first drain strategy: waiting for additional GPU::Vsync callbacks stalled after F180. Workflow commit [`3e052b8`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/3e052b8e77cfcd966f5e5e05a2f7341ed2ff0374) now pauses gameplay and recursively schedules 12 bounded `PCSX.nextTick` callbacks before `PCSX.quit(0)`; this needs a bounded run to verify it.
- Current marker is still revision25, pinned to the independently restore-verified Information parent from run #39768787669: SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`. Next: set revision26 (same source, two cycles, AB_ACTION=DOWN), observe only one run and audit all 10 X11 frames, parent parity, inputs, two load events, normal exits and both externally verified output checkpoint files.
- Do not infer Information→`マップを見る` (Lihat peta) from run #39770465538. The source-only parent remains the last trusted state. Do not use Circle.

---

## LATEST DIAGNOSTIC — Information-down experiment blocked by truncated checkpoint; retry with drain window (22 October 2026, 18:23 WIB)

- Run [#39769826213](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39769826213) failed before branch 2. C01-F20/F60/F100/F110/F180 authentic X11 screenshots validated; baseline/source hash was `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`; Memory Card clones were identical; DOWN readback press/release passed. Process exited 139 and checkpoint was truncated at 2,097,152 bytes, so validator failed and watcher stopped with code 92. This is not a gameplay result, and no checkpoint from this run is trusted.
- The authentic F20 screenshot shows `情報` (Informasi) selected in the right menu; no conclusion is made about DOWN from this run.
- Workflow commit `13da48ab08ef40d0be8c8bbc850b7babbb9b107e` adds a 12-VSync no-input drain period after write/close before pausing and scheduling quit outside VSync. This is intended to allow a delayed save-slice flush; it is not yet proven.
- Retry revision 25 is expected to rerun the same matched DOWN/NONE test using the exact same immutable, restore-verified Information parent above. Verify ten frames, equal F20, both inputs/load events, and both external post-exit checkpoint checks. Do not use the 2 MiB checkpoint.

Story Mode not complete; keep evidence private and out of Git.

---

## ACTIVE RUN — test DOWN from Information to the next row (22 October 2026, 18:20 WIB)

Run [#39769826213](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39769826213) is active (marker revision 24): exact parent source from #39768787669, `adaptive-cycle-01-f180.sstate`, SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`; ACTION=DOWN vs NONE/WAIT; two identical-bytes but separate Memory Card copies; two fresh emulator processes. The question is whether DOWN from `情報` (Informasi) moves highlight to `マップを見る` (Lihat peta).

Audit after completion: exact parent hash on both branches, F20 pixel-identical screenshots and matched menu state, press/release input readback, 10 authentic external-X11 captures, two load events, both post-exit size/header/SHA checkpoint validations, and normal/allowed exits. Do not infer item semantics or use Circle. The run was initializing at the last status check.

Story Mode remains NOT COMPLETE; continue keeping screenshot/savestate/Memory Card/ROM/BIOS artifacts private and out of Git.

---

## LATEST VERIFIED UPDATE — Information state restored; next matched menu probe active/next (22 October 2026, 18:18 WIB)

- Fresh-process restore run [#39769265269](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39769265269) succeeded. Source from A/B run #39768787669: `adaptive-cycle-01-f180.sstate`, 21,162,009 bytes, SHA-256 `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`.
- Evidence includes exact `ExecutionFlow::SaveStateLoaded` event, `ADAPTIVE_RESTORE_TEST=PASS`, five 1280x800 authentic external-X11 captures that were visually reviewed; F20 still shows the red highlight on `情報` (Informasi); normal exit 0.
- New output checkpoint generated by the restore process: 21,162,446 bytes, SHA-256 `6159214a9006127c70f190f0d64b2ed3fb7f9e58ffddd5e4546a0a18820114c6`, private artifact #12421358860. It passed post-exit size/header/SHA validation but is not yet trusted because it hasn't itself been restored.
- Source hash `aa399bd...` is now confirmed restorable and should remain the pinned parent for the next probe: one DOWN versus NONE/WAIT, cloned identical Memory Cards, test whether highlight moves from `情報` (Informasi) to `マップを見る` (Lihat peta). Require initial F20 pixel parity and all normal A/B evidence guards. No Circle.
- Current result/rules: DOWN Roulette→Ninjutsu and DOWN Ninjutsu→Information are VERIFIED only for their observed parent states. Do not generalize beyond context.

---

## LATEST VERIFIED MENU RESULT — second DOWN reaches Information (22 October 2026, 18:14 WIB)

Story Mode is **NOT COMPLETE**.

- Run [#39768787669](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768787669) completed successfully. Two fresh processes used the same parent checkpoint SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`, separate byte-identical Memory Card clones SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`, and each logged `ExecutionFlow::SaveStateLoaded`.
- Ten authentic X11 frames passed 1280x800 validation. Parent F20 images matched pixel-for-pixel; the ACTION branch sent one DOWN with true/false press/release readback and the NONE branch sent no input. ACTION changed the highlight from `忍術` (Ninjutsu) to `情報` (Information) by F60; control retained Ninjutsu. Difference: 14,606 pixels at F60/F100/F110/F180 (mean absolute RGB difference 1.04012). Both emulator processes exited 0.
- Output states passed post-exit structural validation but are **not** trusted restore sources until independently loaded in a fresh emulator process: ACTION 21,162,009 bytes, SHA-256 `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`; NONE 21,162,184 bytes, SHA-256 `06cea778aaaf838271fafa58734c3e236e7d5aa3f63d578a786012640fbbde52`. Evidence artifact #12421302756 remains private.
- **VERIFIED, narrow scope:** one DOWN moves selection from Ninjutsu to Information from that exact checkpoint/menu state.

### Next step — Triangle vs NONE
Use the already restored menu checkpoint from run #39768371975, artifact #12421326531, `adaptive-cycle-01-f180.sstate`, 21,162,575 bytes, SHA-256 `fa03a1840612749810453566a25805e89a4aa21ad64664695e09ed7222b77a9e`. It displays Ninjutsu highlighted and the footer `△ マップ` (Triangle: Map). Use two fresh emulator processes and independent identical disposable Memory Card clones; compare 10 authentic external-X11 captures, require exact F20 pixel parity, Triangle press/release readback, post-exit checkpoint size/header/SHA, and stop at the map view without selecting anything. Do not press Circle.

---

## LATEST VERIFIED UPDATE — DOWN advances Ninjutsu to Information; new action checkpoint needs restore test (22 October 2026, 18:14 WIB)

- Successful run [#39768787669](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768787669) performed a matched DOWN-vs-NONE test from previously restore-validated Ninjutsu checkpoint SHA `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`.
- Both initial F20 frames were pixel-identical (0 mismatch/1,024,000 pixels); action/control states both classify `menu_or_unknown_choice`; cloned Memory Cards were byte-identical; two `ExecutionFlow::SaveStateLoaded` events logged; DOWN readback press/release passed; control sent WAIT only; both processes exited 0; both output checkpoints passed size/header/SHA validation.
- Authentic external-X11 frames show the red highlight move from `忍術` (Ninjutsu) to `情報` (Informasi) by F60 only in the DOWN branch, while NONE remains on Ninjutsu. F60/F100/F110/F180 comparisons: 14,606 differing pixels, mean absolute RGB difference 1.04012. Record **VERIFIED only for these tested menu states**: a DOWN press advances the highlighted row one step.
- Action checkpoint in private artifact #12421302756: `adaptive-cycle-01-f180.sstate`, 21,162,009 bytes, SHA-256 `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`. Control checkpoint: 21,162,184 bytes, SHA-256 `06cea778aaaf838271fafa58734c3e236e7d5aa3f63d578a786012640fbbde52`. Do not promote either until a fresh process restores it.
- Next: revision 23 restore-only from ACTION checkpoint (run #39768787669/artifact #12421302756), `RESTORE_TEST=1`, one cycle. Require `ExecutionFlow::SaveStateLoaded`, five valid post-load external-X11 frames with Information highlighted, allowed exit and external output checkpoint verification. Circle remains prohibited for menu confirmation without a visible YES.

Story Mode remains NOT COMPLETE.

---

## ACTIVE RUN — matched test of DOWN from Ninjutsu (22 October 2026, 18:12 WIB)

Run [#39768787669](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768787669) is active, marker revision 22. Both fresh-process branches use the same verified parent checkpoint from #39767790829 (`adaptive-cycle-01-f180.sstate`, SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28)) and separate identical Memory Card clones. ACTION=DOWN, control=NONE/WAIT. Require pixel-identical F20 frames and `menu_or_unknown_choice` state in both branches, input press/release readback, two load events, and external output checkpoint checks. Inspect the frames to see whether the red selection moves from `忍術` (Ninjutsu) to `情報` (Informasi). The run was in progress at container initialization at last status check.

---

## LATEST VERIFIED CHECKPOINT — menu-DOWN state restored (22 October 2026, 18:10 WIB)

Story Mode is **NOT COMPLETE**.

- Restore run [#39768371975](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768371975) passed in a fresh emulator process. It used the exact ACTION checkpoint from #39767790829 (21,163,486 bytes, SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`) and explicitly logged `ExecutionFlow::SaveStateLoaded`.
- Five real external-X11 captures at 1280x800 passed and were visually checked. All show the right-side menu with `忍術` (Ninjutsu) highlighted. Other labels: `ルーレット` (Roulette), `情報` (Information), `マップを見る` (View map). Footer `△ マップ` means (Triangle: Map).
- Emulator session-finished marker and exit 0 were verified. New checkpoint was externally validated after process exit: `adaptive-cycle-01-f180.sstate`, 21,162,575 bytes, SHA-256 `fa03a1840612749810453566a25805e89a4aa21ad64664695e09ed7222b77a9e`, private artifact #12421326531.
- Next bounded probe: Triangle-versus-NONE from this exact parent checkpoint, separate equal-hash disposable Memory Cards, new emulator process for each arm, five authentic X11 captures per arm. Require pixel-identical F20, Triangle press/release readback and compare whether the menu opens a map. Stop after a map view appears; do not select any map target or use Circle.

Keep all ROM/BIOS/Memory Cards/savestates/screenshots out of Git. No completion claim without authentic ending/results evidence.

---

## LATEST VERIFIED UPDATE — matched DOWN successor can be restored; repeat direction probe next (22 October 2026, 18:10 WIB)

- Restore run [#39768371975](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768371975) passed. It used the ACTION branch checkpoint from A/B run #39767790829, exact source SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`, and logged `ExecutionFlow::SaveStateLoaded`. Five external X11 images passed 1280x800 validation; F20 visually showed the `忍術` (Ninjutsu) row selected, and the process exited 0. Post-exit size/header/SHA checks on the new output state also passed.
- The new output checkpoint itself (21,162,575 bytes; SHA-256 `fa03a1840612749810453566a25805e89a4aa21ad64664695e09ed7222b77a9e`) remains an unpromoted private artifact (#12421326531), because no fresh process has restored that output file yet. Keep the previously tested source `76b5962f...` as the immutable test parent.
- Next trigger revision 22 as a matched ACTION=DOWN vs NONE/WAIT test from run #39767790829's `adaptive-cycle-01-f180.sstate`, SHA above, `AB_TEST=1`, `LOOP_CYCLES=2`. Audit whether DOWN moves Ninjutsu to `情報` (Informasi), with exact F20 pixel parity, input press/release readback, independent matching Memory Cards, two successful loads, and both output size/header/SHA checks. No Circle; no assumption about what a menu item does.

Story Mode remains NOT COMPLETE. Only this Naruto research repo is permitted; keep screenshots, savestates, Memory Cards, ROM and BIOS out of Git and artifact contents private.

---

## LATEST ACTIVE STEP — restore menu-DOWN output checkpoint (22 October 2026, 18:08 WIB)

Restore-only run [#39768371975](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768371975) is queued with marker revision 21. Source is the ACTION-branch output from successful A/B run #39767790829, artifact #12420204586, file `adaptive-cycle-01-f180.sstate`, 21,163,486 bytes, SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`. It uses `RESTORE_TEST=1` and one cycle.

Audit explicit `ExecutionFlow::SaveStateLoaded`, five authentic X11 post-load images, process exit, and the new checkpoint's external post-exit size/header/SHA checks. The successful A/B result established that DOWN moved the highlighted menu row from `ルーレット` (Roulette) to `忍術` (Ninjutsu), versus NONE remaining on Roulette; do not continue gameplay from the action checkpoint unless this restore test passes. Story Mode is still NOT COMPLETE.

---

## NEWEST HANDOFF UPDATE — menu DOWN effect VERIFIED; validate action checkpoint restore next (22 October 2026, 18:06 WIB)

Story Mode is still **NOT COMPLETE**; there is no authentic ending/results image.

### Matched A/B test result
- Successful corrected run [#39767790829](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39767790829) restored the same immutable parent hash `7679cfbd3576c3202abcc299b907939ab4e4529e3a0aa260e780806b1e21cc92` in two fresh processes, with separate action/control Memory Cards copied from an identical baseline.
- F20 parent screenshots matched pixel-for-pixel (0 mismatches / 1,024,000 pixels); both state classifiers returned `menu_or_unknown_choice`. All ten external-X11 images passed PNG/resolution validation; both emulator sessions logged `ExecutionFlow::SaveStateLoaded` and exited 0. Both checkpoints passed external shell size/header/SHA validation.
- One DOWN press/release was verified in the action branch; NONE/WAIT was used in the control branch. The action branch selection moved from `ルーレット` (Roulette) to `忍術` (Ninjutsu) between F20 and F60, while the control remained on Roulette through F180. F60/F100/F110/F180 each had 14,609 differing pixels and mean absolute RGB difference 1.04924. Private screenshot artifact #12420204586 was visually reviewed.
- Record as **VERIFIED only for this exact menu and context**: DOWN moves selected row one step down from Roulette to Ninjutsu. Do not generalize to other states.
- Action checkpoint in private artifact #12420204586: 21,163,486 bytes, SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`. Control checkpoint: 21,163,324 bytes, SHA-256 `3da0a41d55e988550ef1a9368652fa909ae06da34c2b4b7bf315f5a820f76aeb`. Neither is a trusted resume point until fresh-process restoration is independently verified.
- The earlier failed #39767083708 completed the paired comparison but failed a final dialogue guard that incorrectly applied to the A/B mode. It did not invalidate the visual finding. The guard was fixed and #39767790829 passed.

### Exact next action
Trigger a one-cycle restore-only run using run #39767790829's private artifact `naruto-storymode-adaptive-player-private`, checkpoint `adaptive-cycle-01-f180.sstate`, and exact SHA above; set `RESTORE_TEST=1`, `CONTINUATION_TEST=0`, `AB_TEST=0`, `LOOP_CYCLES=1`, increment the marker revision. Audit explicit `ExecutionFlow::SaveStateLoaded`, five post-load X11 images, exit result, and the new checkpoint's post-exit size/header/SHA. If it passes, continue from the verified Ninjutsu-highlight state using controlled direction probes; do not confirm non-YES menu items with Circle. Keep all screenshots/savestates private/out of Git.

---

## NEWEST HANDOFF UPDATE — matched menu action test passed; Triangle/Map probe is next (22 October 2026, 18:06 WIB)

Story Mode remains **NOT complete**.

### Verified A/B test
- Run [#39767790829](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39767790829) passed from parent checkpoint `adaptive-cycle-02-f180.sstate` from run #39765193287, SHA-256 `7679cfbd3576c3202abcc299b907939ab4e4529e3a0aa260e780806b1e21cc92`.
- Two fresh emulator processes loaded the exact same parent; F20 images matched pixel-for-pixel (1,024,000 pixels). Both began in `menu_or_unknown_choice`.
- Memory Cards were independent disposable clones with matching SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- Branch ACTION pressed/released DOWN with true/false readback; branch CONTROL sent no button. At F60/F100/F110/F180, visual differences were consistently 14,609 pixels (mean absolute RGB difference 1.04924). Visual review shows the red selection marker moved from `ルーレット` (Roulette) to `忍術` (Ninjutsu) only in the DOWN arm; control stayed on `ルーレット` (Roulette).
- Both outputs passed post-exit size/header/SHA checks. Action checkpoint SHA `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`; control checkpoint SHA `3da0a41d55e988550ef1a9368652fa909ae06da34c2b4b7bf315f5a820f76aeb`. Keep private artifact #12420204586 private.

### Narrow conclusion
`VERIFIED`: one DOWN moves the menu selection from Roulette to Ninjutsu from this exact parent state. `HYPOTHESIS`: the same exact directional behavior generalizes to all menus. This does not prove a gameplay turn was committed; no confirm button was sent.

### Next action
At the same menu screenshot, footer `△ マップ` means (Triangle: Map). If continuing automatically, test one Triangle press/release versus NONE from the same pinned menu checkpoint, same cloned disposable Memory Cards, two fresh processes and ten external-X11 captures. Require exact F20 pixel parity and compare the displayed state/selection. Do not use Circle; the user allows it only when a contextually valid YES is visibly highlighted. If Triangle opens a map view, capture and inspect that screen before selecting anything.

All assets/evidence remain private/out of Git. Only this repository is allowed. No Story Mode completion claim without authentic ending/results evidence.

---

## NEWEST HANDOFF UPDATE — matched A/B baseline confirmed; path-format bug fixed, rerun active (22 October 2026, 17:59 WIB)

Story Mode is still **NOT COMPLETE**.

- A/B run #39766331759 got through both emulator branches: 10/10 genuine X11 captures, both branch Memory Cards cloned byte-identically, both fresh processes logged `ExecutionFlow::SaveStateLoaded`, DOWN press/release readback passed for the ACTION arm, NONE/WAIT sent no input, and both output states passed external post-exit size/header/SHA validation. But it failed at final comparison with `TypeError: unsupported operand type(s) for %: 'PosixPath' and 'int'`; do not count its paired report as completed, and do not promote its output checkpoints.
- Reviewing its private artifact #12419789546 established both F20 classifications were `menu_or_unknown_choice` and the two frame arrays were pixel-identical (0 mismatching pixels out of 1,024,000). The Memory Card baseline/clones share SHA `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`; the exact immutable parent SHA for both arms was `7679cfbd3576c3202abcc299b907939ab4e4529e3a0aa260e780806b1e21cc92`.
- Workflow path formatting was fixed in commit [0041262a4c83edbabdbfb658ff3c572ad9e3a30c](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/0041262a4c83edbabdbfb658ff3c572ad9e3a30c). Run [#39767083708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39767083708) repeats the same bounded test on revision 19 and was active at this update.

Next: audit run #39767083708 and its private 10-frame artifact. Require same initial F20 pixels/state, exact same source hash, byte-identical independent Memory Card clones, DOWN press/release readback, WAIT-only control, both checkpoint validations, and a completed visual-difference report. If the menu remains unchanged and the report is completed, classify DOWN's effect only in this particular menu/timing context—not as a global rule. Keep the artifact private; don't commit frames/savestates.

---

## NEWEST HANDOFF UPDATE — two-cycle continuation passed; paired menu-action experiment next (22 October 2026, 17:47 WIB)

Story Mode is **NOT complete**.

- Run [#39765193287](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39765193287) passed the bounded two-cycle continuation test. Ten authentic external-X11 screenshots passed 1280x800 validation and were visually checked from private artifact #12419528763. Both emulator sessions logged `ExecutionFlow::SaveStateLoaded`; cycle 2 resumed the precise SHA of cycle 1's externally validated checkpoint; both sessions exited 0.
- Cycle 1 checkpoint: 21,163,161 bytes; SHA-256 `fd46af37af86b0843651ee6baa5d10bd6cb75123d68c87e8319a647130d6b512`.
- Cycle 2 checkpoint: 21,163,013 bytes; SHA-256 `7679cfbd3576c3202abcc299b907939ab4e4529e3a0aa260e780806b1e21cc92`.
- Both states passed shell validation after their emulator processes ended. The screenshot sequence showed map_after_move → Iruka dialogue → START skip → right-side menu. The Japanese text `いいかナルト。` means (Dengarkan baik-baik, Naruto). On the cycle-2 menu, classifier chose `WAIT` because the menu choice semantics are not yet fully calibrated. This is correct fail-closed behavior, not a game completion.
- Next experiment should be a paired `DOWN` versus `NONE/WAIT` test starting from the exact immutable cycle-2 checkpoint above. Clone the same baseline Memory Card into two separate disposable files, fresh emulator process per branch, capture five external X11 frames each, require same F20 parent screen before applying DOWN only in the action branch, then compare highlight/visual transition. Keep Circle out of the experiment and START only for visible dialogue. Record only directly supported observations; do not generalize beyond the test.

Story Mode not complete. Keep ROM, BIOS, Memory Cards, savestates and all X11 images out of Git; private artifact stays private. Only the permitted research repo may be accessed or changed.

---

## NEWEST HANDOFF UPDATE — checkpoint restore verified; two-cycle continuation active (22 October 2026, 17:43 WIB)

Story Mode is **NOT complete**; no authentic ending/results screenshot exists.

### Verified checkpoint chain
- Smoke run #39763526377 succeeded; private checkpoint #12419631005: `adaptive-cycle-01-f180.sstate`, 21,162,617 bytes, SHA-256 `b55495934f9ba98165268627b35904918a4dd3983e6d90bb66e2662dfa059e17`.
- Fresh-process restore run [#39764239171](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39764239171) succeeded and was audited. It explicitly logged `ADAPTIVE_LOAD_EVENT=PASS event=ExecutionFlow::SaveStateLoaded`, validated five authentic external-X11 captures after load, exited 0, and shell validation after exit confirmed its checkpoint size/header/SHA-256:
  - artifact #12419357425 (private)
  - `adaptive-cycle-01-f180.sstate`
  - 21,162,934 bytes
  - SHA-256 `16f697fa95c16661a639ad46b55f90008e60200d1ee860058b12d7b1110d073b`
- Workflow commits now allow an immutable source selector and a continuation-test mode. Continuation mode has a two-cycle-only guard, requires 10 authentic captures, two fresh-process load events, external post-exit checkpoint validation, a passing cycle-2 policy guard and differing F20/F180 screenshot hashes within each cycle.
- Run [#39765193287](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39765193287) has been triggered at marker revision 17 from run #39764239171's exact checkpoint hash, `RESTORE_TEST=0`, `CONTINUATION_TEST=1`, `LOOP_CYCLES=2`. It was in progress during this update (container initialization); no result is yet verified.

### Exact next action
Inspect run #39765193287 after completion: confirm ten 1280x800 authentic external X11 frames and inspect them privately; both sessions must log `ExecutionFlow::SaveStateLoaded`; ensure session 2 resumes the hash of session 1's validated checkpoint; both new savestates must pass shell size/header/SHA checks after process exit; verify cycle-2 policy guard, visual-delta checks, and normal process exit. If any condition fails, do not promote its checkpoint or begin the matched one-action-versus-NONE gameplay experiment.

Keep ROM, BIOS, Memory Cards, savestates and gameplay screenshots out of Git and keep artifacts private. Use START for visible Story Mode dialogue; Circle only when the contextually valid YES choice is visibly highlighted. Translate Japanese directly into Indonesian parentheses. Never claim completion without authentic ending/results evidence.

---

## NEWEST HANDOFF UPDATE — one-cycle smoke checkpoint validated; fresh-process restore underway (22 October 2026, 17:35 WIB)

Story Mode is **NOT complete**. No authentic ending/results screenshot exists. The smoke checkpoint passed external structural validation but has not yet been restored by a fresh process.

### Verified smoke run
- Run [#39763526377](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39763526377) succeeded with `LOOP_CYCLES=1`, workflow revision 15. Eight adaptive unit tests passed.
- Authentic external-X11 frames C01-F20, F60, F100, F110 and F180 all passed 1280x800 PNG integrity checks; all five were reviewed from private artifact #12419631005. They show map → dialogue → map_after_move. DOWN and START button readback passed on press and release. START skipped visible dialogue `ここに結界をはります` (Aku akan memasang penghalang di sini).
- Run finished with session marker and emulator exit 0. Shell, only after emulator exit, validated the resulting checkpoint size/header/SHA-256:
  - file: `adaptive-cycle-01-f180.sstate`
  - size: 21,162,617 bytes
  - SHA-256: `b55495934f9ba98165268627b35904918a4dd3983e6d90bb66e2662dfa059e17`
  - artifact #12419631005 (private, 14-day retention). Never commit or publicly link the checkpoint or gameplay frames.
- The workflow was generalized to read a validated source artifact/run/checkpoint/hash from the marker. It records the exact `ExecutionFlow::SaveStateLoaded` event and supports a one-cycle restore test without demanding a new map→dialogue transition from a post-move map.
- Current marker revision 16 is set to `SOURCE_RUN=39763526377`, `SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private`, `SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate`, the SHA above, `RESTORE_TEST=1`, `LOOP_CYCLES=1`.
- Restore run [#39764239171](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39764239171) was triggered. At last inspection it had started but had no verified result yet.

### Exact next action
Audit run #39764239171 plus its private artifact. Require all five authentic X11 images, a clear `ExecutionFlow::SaveStateLoaded` log line, a post-restore capture at C01-F20, clean/allowed shutdown, and external post-exit size/header/SHA validation of the newly generated checkpoint. If it passes, use that run's checkpoint as the source for the next bounded two-cycle continuation. If it fails, do not run two cycles; diagnose and retry a bounded restore-only test.

Keep prior conclusions conservative: single-sequence barrier/Chakra effects remain HYPOTHESIS pending matched NONE control; Story Mode has not ended. All repo/privacy/input/Japanese-translation constraints remain in force.

---

## NEWEST HANDOFF UPDATE — both adaptive retries failed on checkpoint visibility race (22 October 2026, 17:20 WIB)

This section supersedes any older wording below that says runs #39760914530 or #39761094445 are still running/queued. Both have ended in **failure**; no player run is active or waiting for the concurrency lock. Story Mode is **NOT complete**, and no authentic ending/results screenshot exists.

### What was actually verified
- Regression [#39759649670](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39759649670) is successful: 8 synthetic tests and 10/10 expected classes on authentic private external-X11 frames.
- Run [#39760914530](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39760914530) and run [#39761094445](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39761094445) each passed 8 synthetic tests, validated all 5 cycle-1 external-X11 captures, and read back DOWN and START press/release correctly. The actual visible sequence remained board → dialogue → board; dialogue was skipped with START. Neither run entered cycle 2.
- Both Lua sessions reported the immediate checkpoint probe as `bytes=0 header=false` and ended with exit code 74 before the session-finished marker. Fast-fail watcher in #39761094445 worked as intended rather than wasting the full watchdog.
- But each uploaded private artifact later contained a 21 MB savestate with the PCSX-Redux SaveState v4 header:
  - run #39760914530, artifact #12417638677: 21,162,914 bytes, SHA-256 `f1e04a97452d675d6c6a955acd1a3aa6341a13402ca87895d61d29a6edd11124`.
  - run #39761094445, artifact #12417554193: 21,163,014 bytes, SHA-256 `64941480e4ff5eebb8497e7458ec83090d3aa2bf533d5290ac18ae882c5ab5e5`.
- Most plausible working diagnosis is that the checkpoint’s file length/header are not readable immediately during the VSync callback, while the file is finalized later. This is **not proven**. Neither checkpoint has been restored in a fresh emulator process; do not call it trusted just because the artifact has a header and expected length.
- The C01-F180 authentic X11 view shows the green Konoha board, a red barrier/seal marker, Naruto and Mizuki both displaying 1380 Chakra, and the Mizuki token on the board. This repeats the observed screen only; the barrier/cost/NPC-causation question remains a hypothesis until matched against NONE from the same parent. No screenshot/state is committed or publicly linked.

### Exact next-step sequence
1. Patch `.github/workflows/naruto-storymode-adaptive-player.yml` first. Remove the in-VSync immediate length/header rejection after `Support.File:writeMoveSlice(state)`; log only that the write/close call returned. Keep the existing deferred quit outside VSync. Let the shell orchestrator, **after the emulator process exits**, decide whether the checkpoint is usable by checking file size >21,000,000, the v4 header and SHA-256. The shell must still fail closed if any check fails.
2. Set `experiments/.run-storymode-adaptive-player` to `LOOP_CYCLES=1` and increment REVISION. That marker push triggers the player workflow. This should be the next smoke run; do not run two cycles at once.
3. Audit the one-cycle result: 5 valid real X11 captures, input press/release readback, correct START handling, observed map→dialogue progression, completed session marker, shutdown result, raw checkpoint length/header/hash, and progress-report. Full size/header by itself is not restore proof.
4. Once that smoke run passes, test a bounded fresh-process restore using the resulting immutable checkpoint; require a real `ExecutionFlow::SaveStateLoaded` log and post-restore frame capture. Only then run the next two-cycle continuation.
5. After a successful restore, branch into the matched one-action-versus-NONE experiment from the same immutable checkpoint and disposable cloned Memory Card. Unknown visual states remain WAIT; Circle only for a visibly highlighted YES prompt; START skips dialogue.

Do not trigger an additional workflow run until step 1 is committed. The source parent for current runs remains the immutable board/roulette checkpoint from #39685868421 (21,162,945 bytes; SHA-256 `19388b5a9b59c77e443f47abdc7c6f98251ef4a1be1b512378faab217a658ae9`). Only repo `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research` is allowed; keep ROM, BIOS, Memory Card, savestates and gameplay screenshots out of Git, and private artifacts private. Translate Japanese immediately to Indonesian in parentheses. Never claim Story Mode is complete without authentic ending/result evidence.

---

## VERIFIED UPDATE — fresh-session adaptive experiment and classifier correction (22 October 2026, 17:05 WIB)

**Story Mode is NOT complete.** There is no authenticated in-game ending/result screenshot. All current work is bounded automation engineering and rule observation, not a completed full Story Mode run.

### Latest evidence
- Adaptive classifier regression [#39759649670](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39759649670) succeeded: 8 synthetic tests and 10 authentic private external-X11 frames passed their expected classifications.
- The regression proved the old battle_untrained signature was a false positive on this board state. The screenshot shows a green board, route/tile symbols and two character HUDs. The agent now labels this tested signature map_after_move and chooses WAIT; a dual HUD alone is not enough to infer combat. This calibration applies only to the 10 verified frames, not every battle or result screen.
- Player run [#39758737690](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39758737690) produced 10/10 valid external-X11 screenshots and two checkpoint files; its failure was a watchdog race because the watcher checked the checkpoint count before the second checkpoint and fresh-process completion marker appeared. The private artifact is #12416489109, digest sha256:89feb663fd76b514f574a195302551d72928e08256d330ff39a4def4a66fcfc2.
  - Cycle 1: adaptive-cycle-01-f180.sstate, 21,162,838 bytes, SHA-256 81487394b180a47c59165b49bae21f4d278b600d9fbf83c14086a9629da1c2b4.
  - Cycle 2: adaptive-cycle-02-f180.sstate, 21,162,485 bytes, SHA-256 42c4ad60397ade407508c4393fac21c21db6f12c88c5efc77deb05a2daa827f5.
  - Cycle 2's session log showed a successful save-state load event, with the cycle-1 hash as its resume source. The workflow conclusion is nevertheless failure; do not represent it as a run-level success.
- In this single observed sequence, DOWN input was read back press/release, the route counter changed 4 to 3, and a visible dialogue appeared. The Japanese phrase ここに結界をはります (Aku akan memasang penghalang di sini) was visible at F100/F110; START was sent as the dialogue action. At F180, a red barrier/seal symbol was visible, with Mizuki's displayed Chakra 1380 versus 1500 at F100/F110, while Naruto showed 1380. This is a **single-run hypothesis only** until a matched no-input branch from the same parent confirms causality; do not assert it as a universal NPC rule or cost.
- Player run [#39759822818](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39759822818) completed `failure`. It produced 5 valid external-X11 frames for cycle 1; the log showed checkpoint creation and session completion, but the raw checkpoint was only 2,097,152 bytes and failed structural validation, followed by native exit 139. No cycle 2 was attempted. Private artifact #12417747322 remains private.
- Workflow commit `6bca6f80853292b5ebe7033ea0e1a0d2d58be569` added checkpoint-size/header validation and moved quit outside GPU::Vsync. Run [#39760914530](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39760914530) tests these safeguards; it was still in progress at last check and its older watcher may consume the full 240-second window if the orchestrator exits early. Updated run [#39761094445](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39761094445) is queued behind the workflow concurrency lock and adds early watcher exit when the orchestrator dies. Do not create another trigger.
- Recent relevant commits: classifier 358f6b69384c6933754677a2bc9ecde83c4c1100; synthetic test update b25e5270028ba40ccd3a0742418c88697545e30f; authentic 10-frame regression 4116fd8922022a1f32cb090fcf802c3095ee6daf; player watcher synchronization c72fa9955392fe3b27faab319be8acdb80449b47; this handoff/status must be kept synchronized after the current run resolves.

### Next actions, in order
1. Inspect run #39759822818 to conclusion and confirm checkpoint count, both hashes, load events for both fresh sessions, external X11 validations and exit code. Do not expand past two cycles unless all pass.
2. After a clean two-session pass, use the newest validated board-transition checkpoint as an immutable parent; run a matched one-action-versus-NONE experiment on separate fresh emulator processes and cloned disposable Memory Cards. Capture external X11 before/after; compare route counter, token position, HUD Chakra, barrier objects and next screen.
3. If the counter advances into dialogue, press START only. If a barrier-confirmation prompt is visible, Circle is permitted only when the YES choice is visibly highlighted. Keep unknown states at WAIT.
4. Do not infer attack, defense, battle outcome, or universal Chakra costs from the current board HUD. Record rules as VERIFIED only after repeatable controlled evidence; single sequence remains HYPOTHESIS.
5. Only declare Story Mode complete after authentic original in-game ending/results evidence.

### Fixed boundaries
Only zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research may be accessed or modified. Never use other repos. ROM, BIOS, Memory Card, savestates and gameplay screenshots remain private runtime/Actions artifacts and never enter Git. Use authentic external X11 screenshots, never web images or the PCSX internal screenshot API for gameplay proof. Translate Japanese phrases immediately in Indonesian parentheses. Use START to skip dialogue; never Circle for dialogue skipping.

---

# Handoff — Naruto Story Mode autonomous continuation (22 October 2026)

## Objective
Finish Naruto – Shinobi no Sato no Jintori Gassen (Japan) Story Mode from the latest verified continuation checkpoint and extract accurate gameplay rules with direct evidence. The chat must not need to stay open. Work and evidence must be persisted in GitHub Actions artifacts and repository research notes.

## Strict boundaries
- The only permitted repository is `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. Do not inspect or modify Tile Duel or any other repository.
- Never commit ROM, BIOS, Memory Card, savestates, or authentic gameplay screenshots. Keep them private in runtime storage/private Actions artifacts.
- Use authentic external X11 captures of the running emulator for gameplay evidence; never use web images or PCSX's internal screenshot API as gameplay evidence.
- In Story Mode dialogues, use START to skip. Use Circle only for a contextually justified confirmation, such as a visibly highlighted Yes choice.
- Translate each Japanese phrase immediately into Indonesian parentheses.
- Label conclusions VERIFIED, HYPOTHESIS, or UNKNOWN. Do not claim Story Mode completion without authentic final in-game ending/results evidence.

## Actual state as of 22 October 2026
- Story Mode is NOT complete; no final ending evidence exists.
- The adaptive prototype is in `tools/storymode_adaptive_agent.py`; synthetic tests passed 5/5 during run [#39687675432](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39687675432).
- The adaptive loop is not yet reliable and has NOT demonstrated a complete successful multi-cycle run. Do not claim independent end-to-end play, or that gameplay is continuously running between chats.
- Player run [#39687675432](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39687675432), job 119525856234, failed. Private evidence artifact 12386984413 (`naruto-storymode-adaptive-player-private`, 5,371,835 bytes) is retained until 4 November 2026. Keep it private.
- Exact evidence in job logs and inspected private screenshots: captures C01-F20/F60/F100/F180 and C02-F20 were valid 1280x800 external X11 images. C01-F20/F60 show the route view; C01-F100/F180 and C02-F20 show an encounter scene with Naruto/Mizuki status panels at the top. The old green-background heuristic mislabeled the encounter as map and selected DOWN then RIGHT. The runner additionally stopped producing phase captures after C02-F20. Only 5/32 images and 1/8 checkpoints were produced. Treat this as a classifier plus harness/loop failure, not proof that the route action was successful.
- The Lua gate pauses the emulator, prints ADAPTIVE_CAPTURE_READY, then waits in a `PCSX.nextTick` callback for a gate file, polling with `os.execute("sleep 0.05")`. The cycle-one gates worked but the second cycle did not advance. This pattern is the first suspect for the hang; confirm it from private artifacts/logs before choosing a fix. The outer `timeout` killed the process with exit 124 after 240 seconds; the log does not establish a definitive root cause.
- Added `.github/workflows/naruto-storymode-adaptive-regression.yml`. Run [#39753391179](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39753391179) passed: all six synthetic unit tests and all five expectations against authentic private X11 frames passed. C01-F20/F60 classify as map; C01-F100/F180 and C02-F20 classify as battle_untrained/WAIT. This proves classification on the tested five frames only, not the accuracy of all screen states or that gameplay can continue autonomously.
- Monitor workflow `.github/workflows/naruto-storymode-adaptive-monitor.yml` runs on a schedule and on player-run completion. It checks GitHub Actions run state, age, conclusion and whether an evidence artifact exists. It does NOT inspect gameplay progress, validate screenshots/checkpoints, or prove the game is advancing. Monitor run [#39735171093](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39735171093) failed because it correctly flagged the failed adaptive run.
- The player workflow `.github/workflows/naruto-storymode-adaptive-player.yml` is manually/marker triggered and bounded to 20 minutes; the internal emulator wrapper has a 240-second timeout. It does not yet chain resumable player sessions automatically. Do not confuse the scheduled monitor with an autonomous gameplay scheduler.
- Current immutable source checkpoint used by the adaptive prototype was `next-roulette-result-none-f180.sstate` from run #39685868421, size 21,162,945 bytes, SHA-256 `19388b5a9b59c77e443f47abdc7c6f98251ef4a1be1b512378faab217a658ae9`. This is a valid board/roulette continuation checkpoint, not proof of the latest point in Story Mode. Do not overwrite it; use read-only copies for experiments.
- Relevant observed rules so far: START skipped dialogue and led to a new roulette screen after Mizuki's dialogue; after the earlier roulette, DOWN moved the route token one step/counter 2→1 and triggered Iruka dialogue; on the visible barrier prompt, Japanese `ここに結界をはりますか？` means “Apakah akan memasang penghalang di sini?”, `必要チャクラ 120` means “Chakra yang dibutuhkan: 120”, `はい` means “Ya”, and `いいえ` means “Tidak”. Circle confirmed visibly highlighted Yes; a barrier appeared and Naruto Chakra changed 1500→1380 (Mizuki remained 1500). These are direct observed findings; do not generalize an action's effect beyond tested context.
- Latest roulette A/B (run #39685868421): Circle and NONE branches were pixel-identical at F100/F180 and both returned to the board; do not spam Circle while the wheel may be settling.
- Monitoring report is not a push notification. GitHub Actions monitor failures are visible in Actions/job summary; no claim of proactive ChatGPT messaging when the chat is closed.

## Required next engineering sequence
1. Inspect the private player artifact 12386984413 (especially authentic C02-F20 and Lua/emulator logs) to verify the stall location; do not publish or commit screenshot/state files.
2. Re-run the new battle_untrained regression tests and verify real private C02-F20 now classifies as battle_untrained/WAIT. The screenshot-derived dual-status-HUD signature was added after inspecting artifact #12386984413. Then fix the separate emulator-control handshake so one capture/gate cannot deadlock the VSync/tick callback. Consider decoupling polling from the emulator's event callback or using a non-blocking gate/state machine; preserve externally captured X11 evidence. Add explicit per-phase watchdogs and a fail-fast timeout that records last phase, stdout tail, and checkpoint hash.
3. Change the control loop to save a checkpoint before/after each bounded action window and resume each next bounded session from the last checkpoint that passed structural/restore and visual validation. Do not assume a savestate is valid just because the API wrote one.
4. Rerun a short smoke test from the known board checkpoint first (one cycle, strict timeout). Confirm capture, input readback, emulator VSync advancement, expected visual change or controlled no-change, checkpoint creation, and successful restore. Then test 2–3 cycles. Do not expand to longer runs until they pass.
5. Improve state classification only with real private emulator frames. Unknown/battle/result screens must remain fail-closed WAIT until calibrated; collect controlled visual before/after evidence for new states.
6. Only after smoke tests pass, add automatic session continuation: a serialized bounded player workflow that resumes from the newest validated private checkpoint, with a single-run concurrency lock, retry/backoff and a hard maximum per run/day to conserve GitHub Free minutes. A scheduled monitor should verify progress fields/checkpoint timestamps and compare evidence, not just workflow health. Avoid an infinite workflow loop that consumes quota.
7. Rule extraction: use paired A/B experiments from a shared read-only parent savestate and cloned Memory Card; vary one action; capture true emulator screenshots; log game state, coordinates/route counter, Chakra, barriers/ownership, selected options, dialogue and next transition. Repeat in multiple contexts and classify results as VERIFIED/HYPOTHESIS/UNKNOWN. Keep artifacts private and turn observations into Indonesian docs.
8. Only record complete Story Mode after a real in-game ending/results screen is captured and independently verified.

## Suggested first message in the new chat
“Gunakan GPT-6. Lanjutkan riset Naruto – Shinobi no Sato no Jintori Gassen (Japan) dari handoff terbaru. Repo yang boleh diakses/diubah HANYA `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. Baca `docs/HANDOFF_NEXT_CHAT_2026-10-22.md`, `STATUS.md`, `HANDOFF_CHAT_BARU_2026-10-19.md`, `docs/STORYMODE_ADAPTIVE_AGENT_2026-10-22.md`, dan workflow adaptive player/monitor versi terbaru. Mulai dengan memeriksa artifact privat run #39687675432 dan memperbaiki hang siklus kedua; jangan melakukan run panjang sebelum one-cycle smoke test sukses. Jangan akses repo lain. Gameplay screenshot harus asli dari external X11 emulator capture; START untuk melewati dialog; Circle hanya untuk konfirmasi kontekstual. Jangan commit ROM/BIOS/Memory Card/savestate/screenshot. Terjemahkan teks Jepang langsung ke Bahasa Indonesia. Jangan klaim tamat tanpa bukti ending game yang autentik. Chat tidak boleh menjadi prasyarat bagi proses gameplay yang berjalan mandiri.”
