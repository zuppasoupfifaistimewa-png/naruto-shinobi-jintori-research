## RESTORE VERIFIED — roulette state from revision45 survives a fresh process (revision46)

Run #39868354205 passed restore-only. Private artifact #12465131490 passed ZIP integrity. The source from run #39867730674 / artifact #12464258211 / `adaptive-cycle-01-f180.sstate` was 21,162,546 bytes/v4, SHA-256 `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`. Fresh process logged SaveStateLoaded and restore PASS; five valid authentic 1280×800 screenshots all show the wheel; exit0; new output externally validated.

Input SHA `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492` is promoted as independently restorable roulette-state checkpoint. New output `6d76dbd23d5d01dc1f145d6837b987ae3232fff383ad23eb5262c375ca4828ea`, 21,162,423 bytes/v4, not promoted until another independent restore.

Next revision47: paired CIRCLE vs WAIT from this exact roulette input, using `AB_EXPECTED_STATE=roulette`, `AB_ACTION=CIRCLE`, source run #39867730674 / artifact #12464258211 / checkpoint adaptive-cycle-01-f180.sstate / hash above, AB_TEST=1, two cycles, restore/continuation off. Preserve all paired acceptance gates. Visual target: determine if Circle stops/commits roulette result while WAIT keeps wheel moving. Workflow commit `11b308f162aa1ef2f5b5167cd17b4340718a03de` adds state-specific Circle gate and the strictly gated native-exit 134 recovery. Do not use Circle to skip dialogue; START only. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision46 restore-only for wheel checkpoint after Circle

Run #39868354205 is active at head `096a5cdc411e3ce26fd44f9bde8ff4ed909313c7`; started 05:55:24 WIB; timeout about 06:15:24 WIB. Source run #39867730674 / artifact #12464258211 / `adaptive-cycle-01-f180.sstate` / SHA-256 `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`, size 21,162,546, v4. Marker has RESTORE_TEST=1, one cycle, REVISION=46.

Revision45's genuine images show Circle changed Roulette menu to a spinning wheel at F60/F100/F110/F180 and its button readback passed, but native shutdown aborted at exit134 after session finished; no control branch ran. Keep Circle-to-wheel HYPOTHESIS until matched A/B passes. Checkpoint header/hash/size passed local file inspection. Workflow commit `11b308f162aa1ef2f5b5167cd17b4340718a03de` now only recovers exit134 when session-finished marker and external checkpoint validation pass, and permits `AB_EXPECTED_STATE=roulette` only with Circle.

Require revision46 fresh-process load event, restore PASS, five authentic 1280×800 X11 images with roulette visible, accepted exit, external output checkpoint validation. Do not run another player in parallel; do not promote revision46 output until its own independent restore. Story Mode NOT COMPLETE. Use START for dialogue.

---

## REVISION45 PARTIAL — Circle opened the roulette wheel; shutdown aborted before control

Run #39867730674 failed after the ACTION session. Private artifact #12464258211 passed ZIP integrity; direct inspection of authentic C01 screenshots shows the command menu with `ルーレット` (Roulette) highlighted at F20, then roulette wheel by F60/F100/F110/F180 after one Circle press/release (readback true/false). The emulator then logged session finished but aborted with `corrupted size vs. prev_size`, exit134 before control cycle; no paired control images/report. Keep the gameplay interpretation as **HYPOTHESIS** until A/B is complete.

ACTION state candidate in that artifact: `adaptive-cycle-01-f180.sstate`, 21,162,546 bytes, v4, SHA-256 `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`. Only local structural validation so far; not promoted until fresh-process restore.

Workflow commit `11b308f162aa1ef2f5b5167cd17b4340718a03de` adds a narrowly gated recovery of exit134 only if a session-finished marker and external post-exit checkpoint validation pass, and permits `AB_EXPECTED_STATE=roulette` only with Circle.

Next revision46 restore-only from run #39867730674/artifact #12464258211/file adaptive-cycle-01-f180.sstate/SHA `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`. Verify wheel in five authentic screenshots, load event, exit/checkpoint gates, and new output validation. Then revision47 Circle vs WAIT from roulette-state source to test wheel stopping/selection. START remains the only dialogue-skip input. Story Mode NOT COMPLETE.

---

## ACTIVE — revision45 contextual Circle on Roulette menu

Run #39867730674 active; started 05:49:51 WIB, timeout about 06:09:51 WIB. Source run #39866820866 / artifact #12463489344 / checkpoint adaptive-cycle-01-f180.sstate / SHA-256 `609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`. Restore run #39867381637 independently confirmed F20 with `ルーレット` (Roulette) highlighted. Marker: AB_TEST=1, AB_ACTION=CIRCLE, AB_EXPECTED_STATE=menu_or_unknown_choice, two cycles. Workflow permits Circle only under menu-state guard.

Audit strict A/B gates and screenshot pair after run termination. Confirm actual Circle input readback true/false and whether action opens roulette; WAIT should remain menu. No Circle for dialogue; START only. Story Mode remains NOT COMPLETE.

---

## RESTORE VERIFIED — roulette-highlighted menu checkpoint is independently loadable (revision44)

Run #39867381637 passed restore-only. Private artifact #12464118614 passed ZIP integrity. Actual C01-F20 image displays `ルーレット` (Roulette) highlighted in the command menu. New process logged `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`; five real 1280×800 screenshots, exit0, external output size/v4-header/SHA validation passed.

Input checkpoint from run #39866820866 / artifact #12463489344 / adaptive-cycle-01-f180.sstate: size 21,162,920, v4, SHA-256 `609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`. This exact source is promoted as restorable. New output `0499c0f73799ac18f53a08bfd2c63a45738d8b56fcd32f157d6b0b7b596c19e3`, 21,163,308 bytes/v4, remains unpromoted until its own restore.

Next revision45, Circle vs WAIT on that menu source. Marker: source run 39866820866/artifact naruto-storymode-adaptive-player-private/checkpoint adaptive-cycle-01-f180.sstate/SHA 609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7; AB_TEST=1; AB_ACTION=CIRCLE; AB_EXPECTED_STATE=menu_or_unknown_choice; two cycles; restore/continuation off. Workflow commit `2ec5011c5c81f00e686690570bf4349f9124c531` adds CIRCLE to the menu-state allowlist only, not the map-state list. Require all A/B acceptance gates and screenshot proof. Circle is used for the visibly highlighted Roulette selection only, never for dialogue; use START for dialogue. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision44 independently restores CROSS-returned Roulette menu

Run #39867381637 is active, started 05:46:45 WIB; timeout about 06:06:45 WIB. It loads run #39866820866 / private artifact #12463489344 / checkpoint adaptive-cycle-01-f180.sstate / SHA-256 `609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`, RESTORE_TEST=1, one cycle.

Require explicit SaveStateLoaded and restore PASS, five authentic 1280×800 X11 captures with F20 displaying command menu and `ルーレット` (Roulette) highlighted, exit0, external output state size/v4-header/SHA. Promote only input 609823… after all pass. Do not run parallel player.

Revision43 established that CROSS returns from the map to the command menu and leaves Roulette highlighted at F100/F180, while WAIT stays in map. Next revision45 tests one CIRCLE versus WAIT in this visually verified menu context; CIRCLE is forbidden on dialogue and cannot serve as dialogue skip. Use START. Story Mode remains NOT COMPLETE.

---

## VERIFIED — CROSS exits map view to command menu (revision43)

Run #39866820866 passed the matched CROSS-vs-WAIT A/B. Private artifact #12463489344 was audited. Same source SHA `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8` in both fresh processes; two load events, exact F20 parity, identical cards, CROSS input true/false, WAIT control, ten authentic 1280×800 frames, exit0 both, output checkpoints externally validated and comparison report.

**VERIFIED, narrow:** one CROSS from the map screen exits to the command menu; ACTION C01-F100/F180 shows `ルーレット` (Roulette) highlighted. WAIT leaves the map open with Naruto's cell panel. This is return/menu navigation only.

ACTION state candidate: 21,162,920 bytes, v4, SHA-256 `609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`; CONTROL hash `57fd76c4f133dc485e5bbfc49f8cb6e0e86593780812827bee1a43668ae80e84`. Both unpromoted until independently restored.

Next revision44 restore-only the ACTION output; manually verify the F20 Roulette highlight survives a fresh load, five real captures, exit0 and output checkpoint validation. Then revision45 Circle-vs-WAIT from that verified command-menu state after adding Circle to menu-only A/B allowlist. It is justified by the visually highlighted Roulette row and is not dialogue skipping; dialogue always uses START. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision43 corrected CROSS-vs-WAIT probe

Run #39866820866 active, started 05:41:57 WIB, timeout about 06:01:57 WIB. Run42 failed before gameplay because the final shell whitelist omitted CROSS; artifact #12463119868 was setup-only. Workflow commit `417663b21ce0cd9218ef8c312913a90d65381788` fixes it. Revision43 marker is verified and source checkpoint is exact SHA `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8` from run #39786019434, independently restored in #39786899480. AB_TEST=1, CROSS, expected map_after_move, 2 cycles.

No parallel player. Accept only when all paired gates pass (load events, source SHA, F20 parity, identical cards, CROSS true/false readback, WAIT, ten genuine 1280×800 frames, exit0 both, checkpoint validations, comparison report) and screenshots show whether CROSS returns to menu. Footer `× もどる` (Cross: Kembali) gives a hypothesis only. Story Mode remains NOT COMPLETE.

---

## REVISION42 FAILS BEFORE GAMEPLAY — CROSS late shell gate fixed

Run #39866476856 failed before the emulator was launched. Artifact #12463119868 contains only a 4,505-byte setup dump; no screenshot evidence exists. Cause: selector/Lua accepted CROSS for map-state A/B, but final shell whitelist still omitted CROSS. Workflow commit `417663b21ce0cd9218ef8c312913a90d65381788` adds it. Menu-state gate is unchanged and does not allow CROSS.

Retry revision43 using the exact stable source checkpoint from run #39786019434 / artifact #12428777970 / adaptive-cycle-01-f180.sstate / SHA `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`, with AB_TEST=1, AB_ACTION=CROSS, AB_EXPECTED_STATE=map_after_move, 2 cycles, RESTORE_TEST=0, CONTINUATION_TEST=0. Require all paired gates and visual evidence before classifying. Hypothesis: the visible footer `× もどる` (Cross: Kembali) returns from map view; WAIT keeps the map. Circle is not used. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision42 CROSS-vs-WAIT on map return UI

Run #39866476856 is active. Started 22:39 UTC on 22 October / 05:39 WIB 23 October; hard timeout about 05:59 WIB. Exact source run #39786019434 / artifact #12428777970 / checkpoint adaptive-cycle-01-f180.sstate / SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`. Marker AB_TEST=1, AB_ACTION=CROSS, AB_EXPECTED_STATE=map_after_move, LOOP_CYCLES=2, revision42. Workflow blob `494baab78b7237fa80674526c583e0fdfc74c140` allows CROSS only for map-state A/B. The source screenshot has `× もどる` (Cross: Kembali), so this probes back-navigation without confirming any tile.

Do not start a parallel player. Require all existing matched A/B gates and manually inspect screenshots: CROSS should only be classified as return-to-menu if ACTION actually leaves the map while WAIT remains there. All source SHA/load event/button readback/screenshot parity/capture/exit/checkpoint/report gates must pass. Story Mode remains NOT COMPLETE.
 

---

## RESTORE VERIFIED — Naruto-cell focus checkpoint is independently loadable (revision41)

Run #39786899480 passed all restore-only gates. Private artifact #12428873919 ZIP integrity passed; actual F20 screenshot shows Naruto cell panel `レベル` (Level)1, `結界価値` (Nilai penghalang)60, `耐久値` (Daya tahan)2/2. Explicit `ExecutionFlow::SaveStateLoaded`, restore PASS, five external 1280×800 screenshots, exit0 and post-exit output size/v4-header/SHA validation observed.

Input source from run #39786019434 / artifact #12428777970 / `adaptive-cycle-01-f180.sstate`: size 21,163,100, v4, SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`. It is now independently restore-proven. New output from run41, SHA-256 `93bd0c3e401bd7b8c96bc8b405bd46b13fef2afaf317c2ec47af5412c1b52595`, 21,162,593 bytes/v4, remains unpromoted until its own restore.

Workflow change commit `7ac1b2371b7d0ce48b87b59130a8560db771a962` adds CROSS to map-state-only actions. Screen footer `× もどる` (Cross: Kembali) makes a CROSS-vs-WAIT matched test appropriate as the safest route back from the map. Menu-state gate still restricts actions to DOWN/TRIANGLE.

Next revision42 from source run #39786019434/artifact #12428777970/file `adaptive-cycle-01-f180.sstate`/SHA `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`: AB_TEST=1, AB_ACTION=CROSS, AB_EXPECTED_STATE=map_after_move, 2 cycles, restore and continuation off. Require all paired gates. Inspect if CROSS goes to prior menu while WAIT remains map. Don't use Circle for dialogue; START only. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision41 restore-only validates Naruto-cell focus state

Run #39786899480 is active; started 20:26:48 WIB, timeout around 20:46:48 WIB. Source run #39786019434 / private artifact #12428777970 / adaptive-cycle-01-f180.sstate / SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`, size21,163,100, v4. Settings RESTORE_TEST=1, one cycle, revision41. Do not launch parallel player.

Required: explicit SaveStateLoaded and restore PASS; five real 1280×800 captures; F20 retains Naruto cell panel Level1/barrier60/durability2/2; exit0; external validation of new output size/header/SHA. Promote only input hash 73947… if restore passes; new output remains unpromoted until its own restore.

Revision40 verified only focus: UP from empty land140 returns focus to Naruto cell60; WAIT retains empty-land140 panel. No character movement/capture/ownership inference. Story Mode remains NOT COMPLETE.

---

## VERIFIED INPUT RULE — UP returns board focus to Naruto cell (revision40)

Run #39786019434 passed paired UP versus WAIT from the independently restored source SHA `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`. Artifact #12428777970 confirms two fresh loads; exact F20 pixel parity; identical cards; UP press/release true/false; WAIT control; ten authentic 1280×800 images; exits0; output state external checks and comparison report.

**VERIFIED, cursor only:** UP from `空き地` (Tanah kosong) value140 changes focus/panel to Naruto's cell with `レベル` (Level)1, `結界価値` (Nilai penghalang)60, `耐久値` (Daya tahan)2/2; WAIT retains empty land140. No actual character movement, capture or ownership change is verified.

ACTION output candidate `adaptive-cycle-01-f180.sstate`, 21,163,100 bytes/v4, SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8` in private artifact #12428777970 remains unpromoted pending a fresh-process restore. Next revision41 restore-only must log SaveStateLoaded, capture five authentic 1280×800 screens retaining Naruto cell60, exit0, and output size/v4-header/SHA checks. Story Mode remains NOT COMPLETE.

---

## VERIFIED MAP INPUT — UP changes focus from empty land140 to Naruto tile60 (revision40)

Run #39786019434 passed all matched UP-vs-WAIT gates from source SHA `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`. Artifact #12428777970: 2 fresh processes, 2 load events, identical F20 frames, map_after_move in both, same Memory Card clones, UP press/release true/false, WAIT control, ten authentic 1280×800 X11 frames, exit0 in both, output savestate size/v4/SHA validations, comparison report.

**VERIFIED, narrow:** UP from focused `空き地` (Tanah kosong), value140, changes board focus/panel to Naruto cell, showing `レベル` (Level) 1, `結界価値` (Nilai penghalang)60 and `耐久値` (Daya tahan)2/2; WAIT retains empty-land140 panel. No actual Naruto movement or capture/ownership is inferred. Paired difference F60 719585 px/MAD26.80691; F100 719273/26.76006; F110 719213/26.75687; F180 719644/26.93719.

ACTION candidate output from run #39786019434 / artifact #12428777970: `adaptive-cycle-01-f180.sstate`, 21,163,100 bytes, v4, SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`. Not promoted before fresh-process restore. Next revision41 restore-only from this source; require load event, five authentic screenshots retaining Naruto-cell panel, exit0 and external output size/header/SHA validation. The output emitted by restore run remains unpromoted until its own fresh restore. Story Mode remains NOT COMPLETE.

---

## ACTIVE QUEUE — revision40 tests UP vs WAIT; fixed runtime action guard

Run [#39786019434](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39786019434) is queued. Marker revision40 uses source run #39779256427 / artifact naruto-storymode-adaptive-player-private / adaptive-cycle-01-f180.sstate / SHA-256 58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a; AB_TEST=1; AB_ACTION=UP; AB_EXPECTED_STATE=map_after_move; two cycles. Do not launch another player.

Run39 #39784493293 failed before emulator due to runtime shell gate still requiring DOWN/TRIANGLE; selector and Lua accepted UP. Tiny artifact #12427839381 contains no screenshots, so there is no gameplay result. Fixed at commit d62a04e831ea185f13efafc5e061d5a8dbb945ce (workflow blob 73c864d2eba5579be26da732832a467be876b2d1).

Required gates after completion: exact input source SHA both arms; two load events; F20 identical pixels/map_after_move state; identical Memory Card clones; UP true/false readback; WAIT control; ten authentic 1280×800 shots; exit0 both; external state size/v4/SHA checks both; report. Review screenshots for focus change. Never confirm/select a tile. Story Mode is NOT COMPLETE.

---

## ACTIVE — revision39 directional UP probe from map cell140

Run #39784493293 is active, started 20:10:11 WIB; timeout about 20:30:11 WIB. At its checkout, the marker was verified: source run #39779256427 / artifact naruto-storymode-adaptive-player-private / checkpoint adaptive-cycle-01-f180.sstate / SHA-256 58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a; AB_TEST=1; AB_ACTION=UP; AB_EXPECTED_STATE=map_after_move; two cycles; revision39. Workflow supports UP/DOWN/LEFT/RIGHT on the map state. Do not launch another player.

After completion require: exact parent SHA both arms; explicit load events; identical F20/state map_after_move; cloned cards identical; UP true/false readback; WAIT control; ten authentic 1280×800 images; two exit0s; both checkpoints external size/v4-header/SHA validation; comparison report. Review screenshots for focus change versus WAIT. No confirm input.

Preferred source checkpoint is the independently restored value-140 state from run #39779256427, SHA 58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a. Revision38's alternative output loads technically but first restored frame differs transiently from later stable frames. Story Mode remains NOT COMPLETE; no movement/capture/ending claimed.

---

## ACTIVE — revision39 UP vs WAIT (map-state directional test)

Run #39784493293 is active; started 20:10:11 WIB, timeout about 20:30:11 WIB. At the run's checkout, marker and workflow were checked: source run #39779256427/artifact #124258055? checkpoint adaptive-cycle-01-f180.sstate/SHA `58d8f551cc4cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e` (use the actual full source below, not the abbreviated typo in this note): source SHA `58d8f551ccf3a3af9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e` — see exact committed marker for definitive value. Settings: AB_TEST=1; AB_ACTION=UP; AB_EXPECTED_STATE=map_after_move; two cycles.

[Correction for source identity: the exact verified marker SHA is `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`. Use that exact value.]

After completion, require identical F20s/state, two load events, equal Memory Cards, UP input true/false readback, WAIT, ten genuine 1280×800 images, exit0, two external output validations and comparison report. Directly review whether UP transitions focus from `空き地` (Tanah kosong) value140 to Naruto tile/value60. Do not confirm a tile. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision39 UP-vs-WAIT probes reverse navigation from empty land

Run #39784493293 active, started 20:10:11 WIB; timeout about 20:30:11 WIB. Marker HEAD `4893e1e0eb6cdcaf9fff052c9c794ae62327858a` verified. Source: run #39779256427/artifact #12425858092/adaptive-cycle-01-f180.sstate/SHA `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`; AB_ACTION=UP, AB_EXPECTED_STATE=map_after_move, AB_TEST=1, LOOP_CYCLES=2, revision39. Only this player active.

Require same parent SHA, 2 load events, F20 exact image/state parity, byte-equal card clones, UP readback true/false, WAIT control, 10 authentic X11 captures, exits0, both checkpoint structural/hash validation and report. Inspect whether UP highlights Naruto tile60; only verify what actual images demonstrate. Do not confirm/select any tile. Story Mode remains not complete.

---

## REVISION38 RESTORE CAVEAT — second-DOWN cursor target not stable across resumed frames

Run #39783158903 passed technical restore of revision37 ACTION output hash `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`, logged SaveStateLoaded/restore PASS, produced 5 genuine 1280×800 screenshots, exited0, and validated new output SHA `c4acb2b62a9891b597c1195a2dead7ccce902abddf0c5ec9b4c50b76142a7a33` (21,162,978 bytes/v4). However C01-F20 looks temporarily like a scrolled view with a number near 100 while F60-F180 settle back near the 140-value area. The generic classifier stays map_after_move, so no exact cursor claim. Treat 4989… as technically loadable but not a stable semantic cursor checkpoint. Output c4ac… is also not promoted until independently restored.

Revision39 next tests UP vs WAIT from trusted checkpoint hash `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a` from run #39779256427/artifact #12425858092. Restored separately in run #39780143613. It showed `空き地` (Tanah kosong), value140 at F20. Use AB_TEST=1, AB_ACTION=UP, AB_EXPECTED_STATE=map_after_move, RESTORE_TEST=0, CONTINUATION_TEST=0, two cycles, revision39. Workflow commit b3c78426f8c11b406f0fedbffb01bd667e7ffb5 expands map A/B directional inputs UP/DOWN/LEFT/RIGHT while constraining menu inputs. Require all A/B gates; inspect whether UP returns to Naruto tile60. No tile confirmation. Story Mode not complete.

---

## REVISION 38 RESTORE PASSED — verified input is usable

Run #39783158903 succeeded. Private retry artifact #12427598163 passed ZIP integrity. It shows explicit ExecutionFlow::SaveStateLoaded, ADAPTIVE_RESTORE_TEST=PASS, five authentic 1280×800 X11 captures, accepted emulator exit 0, and output checkpoint validation. The restored board/cursor arrangement matches the post-second-DOWN state. Early tile digits are obscured by leaves; later frames show 140, so do not treat that variation as a tile-value change.

Promoted input checkpoint from run #39782011370 / artifact #12426797521 / adaptive-cycle-01-f180.sstate: size 21,162,960; v4; SHA-256 `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`. Newly emitted output from run38 (21,162,978 bytes, v4, SHA-256 `c4acb2b62a9891b597c1195a2dead7ccce902abddf0c5ec9b4c50b76142a7a33`) stays unpromoted pending its own fresh-process restore.

Next change workflow validation to allow UP/DOWN/LEFT/RIGHT only for map A/B directional probes; exclude confirm buttons. Run RIGHT-versus-WAIT from source 4989fc1f… with all existing evidence gates. Story Mode remains NOT COMPLETE, and no movement/capture/ownership rule or ending is established. Use START for dialogue; keep gameplay files private/out of Git.

---

## RESTORE VERIFIED — revision37 post-second-DOWN source is restorable (revision38)

Run #39783158903 passed restore-only from run #39782011370 / artifact #12426797521 / checkpoint adaptive-cycle-01-f180.sstate / SHA-256 `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`, size 21,162,960, v4. Valid retry artifact #12427598163 confirms load event, `ADAPTIVE_RESTORE_TEST=PASS`, five real 1280×800 X11 screenshots retaining map/cursor post-second-DOWN state, exit0 and external output checkpoint validation. Apparent 100/142 in early frames is foliage occluding digits; later frames show 140. Exact input SHA 4989… promoted.

New output SHA `c4acb2b62a9891b597c1195a2dead7ccce902abddf0c5ec9b4c50b76142a7a33`, size21,162,978,v4 remains unpromoted pending its own fresh-process restore.

Next revision39: extend bounded map A/B valid inputs to the four directions only (UP/DOWN/LEFT/RIGHT). Exclude Triangle and all confirm buttons from the map-direction whitelist. Probe RIGHT vs WAIT from source #39782011370/artifact #12426797521/checkpoint adaptive-cycle-01-f180.sstate/SHA 4989fc1f…; AB_EXPECTED_STATE=map_after_move, two cycles. Require all existing pair gates and manually inspect cursor/viewport. No confirming a tile. Story Mode remains NOT COMPLETE.

---

## VERIFIED MAP FOCUS — revision37 second DOWN (22 October 2026)

Run #39782011370 passed the matched DOWN-vs-WAIT experiment with source SHA `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`. Artifact #12426797521 verified: two explicit SaveStateLoaded events, exact F20 parity, same disposable cards, DOWN press/release true/false, WAIT control, ten authentic 1280×800 captures, exits0, both checkpoint external validations and comparison report.

Narrow VERIFIED observation: a second DOWN from empty land value140 shifts the map viewport upward and places cursor/focus toward the adjacent lower tile near the Naruto-marked board position; WAIT keeps the previous frame with tile140 under cursor and pink tile60 above. Focus/view change only. Do not claim the character moved or captured territory.

Action output candidate hash `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`, 21,162,960 bytes, v4, artifact #12426797521. Must be independently restored in revision38 before promotion. Then inspect workflow input mappings and safely identify how to enter real gameplay; only DOWN and TRIANGLE are currently permitted in A/B validation. No confirm input until selection vs move semantics are clear. Story Mode NOT COMPLETE; use START for dialogue, no Circle, gameplay files remain private/out of Git.

---

## ACTIVE — revision38 restore-only checkpoint for post-second-DOWN view

Run #39783158903 active at 20:00:55 WIB; timeout about 20:20:55 WIB. Marker pins the revision37 ACTION output from run #39782011370 / artifact #12426797521 / checkpoint adaptive-cycle-01-f180.sstate / SHA `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`. RESTORE_TEST=1, one cycle, rev38. Only one player may run.

Accept source after `ExecutionFlow::SaveStateLoaded`, `ADAPTIVE_RESTORE_TEST=PASS`, five authentic 1280×800 images retaining post-second-DOWN map view, exit0 and external output state size/v4-header/SHA verification. New state emitted is unpromoted until its own independent restore. Story Mode still incomplete; focus/scroll is not movement/capture.

---

## VERIFIED BOARD VIEW RESPONSE — second DOWN shifts view again (revision37, 22 October 2026)

Matched run #39782011370 passed all technical gates from parent hash `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`. Artifact #12426797521 shows two explicit restore events, exact F20 image parity, identical Memory Card clones, DOWN true/false readback, WAIT control, ten authentic external 1280×800 images, exit0 twice, both outputs externally validated, comparison report present.

**VERIFIED, scoped:** another DOWN from the prior scrolled map state produces another upward viewport/focus response, with panel hidden and cursor near the lower board area by Naruto's marker; WAIT lets the viewport settle back and restores `空き地` (Tanah kosong), value140 info pane. Diff: F60 780637 pixels/MAD22.66488; F100 780562/22.68538; F110 781298/22.66071; F180 780622/22.62887. Does not identify exact target tile or prove actual movement/capture/ownership.

Next restore-only revision38 source: run #39782011370 private artifact #12426797521 / adaptive-cycle-01-f180.sstate / SHA `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`, RESTORE_TEST=1, one cycle. Pass only with load event, five authentic frames retaining second-DOWN board view, exit0 and external output checkpoint validation. New output remains unpromoted without its own restore. Story Mode not complete.

---

## ACTIVE — revision37 second DOWN probe from scrolled map state

Run #39782011370 active; started 19:52:49 WIB, timeout about 20:12:49 WIB. It uses independently restore-proven source run #39780755350 / artifact #12426786721 / checkpoint adaptive-cycle-01-f180.sstate / SHA `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`. Marker is AB_TEST=1, DOWN, expected map_after_move, two cycles, revision37. Do not start another player while active.

Require exact source hashes, two load events, F20 map-state pixel parity, identical cards, DOWN readback true/false, WAIT control, ten authentic 1280×800 screenshots, both exit0, both output state validation, comparison report. Review all paired post-input images to see whether second DOWN advances the board again. No tile confirmation and no claim of character movement/capture. Story Mode is NOT COMPLETE.

---

## RESTORE VERIFIED — scrolled board state from revision35 is restorable (revision36)

Run #39781495023 passed restore-only from revision35 ACTION output, source SHA `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`, 21,162,766 bytes, v4, from private artifact #12426786721. Private restore artifact #12426677790 shows explicit load event and restore PASS, five valid authentic 1280×800 X11 screenshots, post-DOWN scrolled board retained at F20, exit0, new output checkpoint externally validated. Thus source b971… is promoted as independently restorable.

New emitted output SHA `4fd72504031c7aaa73bd7fa18e2f7a8d79b428643cea3c588ea4596ad5e90777` (21,163,103, v4) remains unpromoted until its own fresh process restore.

Next revision37: matched DOWN versus WAIT from source run #39780755350 / artifact #12426786721 / `adaptive-cycle-01-f180.sstate` / SHA b9717348…; set AB_TEST=1, AB_ACTION=DOWN, AB_EXPECTED_STATE=map_after_move, LOOP_CYCLES=2, RESTORE_TEST=0, CONTINUATION_TEST=0. Require all paired gates; inspect whether view/focus shifts further. No tile confirmation and no inference of character movement/capture. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision36 restore-only of board after DOWN (22 October 2026, 19:49 WIB)

Only active player is #39781495023; start 19:49:08 WIB and timeout about 20:09:08 WIB. The marker's source is the revision35 ACTION output in run #39780755350 / private artifact #12426786721 / adaptive-cycle-01-f180.sstate / SHA-256 `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`. RESTORE_TEST=1, one cycle. Don't run a player in parallel.

Pass only if the fresh process logs `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`, 5 real 1280×800 X11 captures retain the scrolled post-DOWN board focus, exit0, and output savestate passes size/v4-header/SHA external checks. Input checkpoint b9717348… can be promoted upon that evidence. New output remains unpromoted until its own restore.

Story Mode not complete. DOWN from empty-land changes focus/view; don't infer move or territory capture. Keep game assets private/out of Git and use START for dialogue.

---

## VERIFIED BOARD INPUT — DOWN from empty-land focus changes view/selection (revision35, 22 October 2026)

Matched run #39780755350 passed every paired A/B gate using source hash `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`. Private artifact #12426786721 was downloaded after run completed. Two fresh processes and load events; exact F20 parity 1,024,000 pixels; same disposable cards; DOWN input true/false; WAIT control; ten authentic X11 captures 1280×800; exits0; both savestate outputs externally checked; comparison report generated.

**VERIFIED, narrow:** one DOWN from focused `空き地` (Tanah kosong), barrier value140, changes observed board focus/view: viewport scrolls upward and the empty-land panel disappears; cursor appears aligned toward a lower tile near Naruto's board marker. WAIT retains empty-land panel and initial framing. Do not claim the character moved, captured a tile or changed ownership, because the post-action panel does not name its focus. F60 diff 783594 pixels/MAD27.28084; F100 783324/27.36300; F110 783287/27.31514; F180 783630/27.39113.

Next restore-only revision36 tests ACTION output run #39780755350/artifact #12426786721/file adaptive-cycle-01-f180.sstate/SHA `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff` (21,162,766 bytes/v4). Require new-process load event, five authentic frames preserving post-DOWN view, exit0, external output state size/header/SHA. Do not promote the output emitted by the restore run until that output itself restores.
Story Mode remains NOT COMPLETE.

---

## ACTIVE RUN — revision 35 DOWN from empty-land tile versus WAIT (22 October 2026, 19:44 WIB)

Run [#39780755350](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780755350) is `in_progress` from 19:43:50 WIB; latest active step is repository checkout, no artifact yet, 20-minute timeout about 20:03:50 WIB. Do not run players in parallel.

Source run #39779256427 / artifact #12425858092 / `adaptive-cycle-01-f180.sstate`, SHA `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`. Revision 35 runs A/B DOWN against NONE/WAIT, expected state `map_after_move`. Inspect exact logs, image parity, input true/false, two load events, ten 1280×800 external captures, exits, and output validations. Only infer focused-tile change if screenshots prove it. Never confirm a destination. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision35 probes DOWN from empty-land focus (22 October 2026, 19:44 WIB)

Only active player is run #39780755350 (started 19:43:50 WIB; timeout about 20:03:50 WIB). The exact committed marker uses source run #39779256427 / artifact #12425858092 / adaptive-cycle-01-f180.sstate / SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`; AB_TEST=1, AB_ACTION=DOWN, AB_EXPECTED_STATE=map_after_move, two cycles. Source was restored in a new process in run34, preserving the empty-land focus; this source is trusted.

After run35 ends, require all paired gates: exact input SHA both arms, two restore events, F20 image parity and map_after_move state, identical disposable Memory Cards, DOWN true/false readback, ten actual 1280×800 X11 frames, exit 0 both arms, both checkpoint validations, comparison report; inspect actual screenshots. This tests focus only. Do not confirm/select a tile or infer capture/territory change.

Story Mode not complete. Use START for dialogue; keep assets private/out of Git.

---

## RESTORE PASSED — empty-land focus checkpoint is trusted (revision34, 22 October 2026, 19:42 WIB)

Run [#39780143613](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780143613) passed independent restoration of the ACTION output produced by revision33. Source run #39779256427 / artifact #12425858092 / `adaptive-cycle-01-f180.sstate`, SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`, size 21,162,559, v4. The private restore artifact #12425913759 verifies explicit `ExecutionFlow::SaveStateLoaded`, `ADAPTIVE_RESTORE_TEST=PASS`, five valid 1280×800 external-X11 screenshots, fresh process exit0, external post-exit source output size/header/SHA validation. C01-F20 actual screenshot is board state with `空き地` (Tanah kosong), barrier value140 selected. This exact input source is now promoted/restorable.

New output from the restore smoke is not promoted: 21,163,018 bytes, v4, SHA-256 `75f0752616695e0d6d141e3cc051774f5e84defe6944371fb0bc34840c83ce9f`.

Next revision35: paired DOWN vs WAIT from that trusted map checkpoint. Marker fields: SOURCE_RUN=39779256427; SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private; SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate; SOURCE_SHA256=58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a; RESTORE_TEST=0; CONTINUATION_TEST=0; AB_TEST=1; AB_ACTION=DOWN; AB_EXPECTED_STATE=map_after_move; LOOP_CYCLES=2; REVISION=35. Require all paired gates and visual review; observe next tile focus only; do not confirm/select. Story Mode remains NOT COMPLETE.

---

## ACTIVE RESTORE-ONLY — verify the map empty-land focus checkpoint (revision34)

Run #39780143613 is active, started 19:39:28 WIB; timeout about 19:59:28 WIB. Marker was verified at its committed head and uses source run #39779256427 / artifact naruto-storymode-adaptive-player-private / checkpoint adaptive-cycle-01-f180.sstate / SHA-256 58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a, RESTORE_TEST=1, LOOP_CYCLES=1, REVISION=34. Last status showed X11/tool installation active, no artifact yet. Do not start other player.

Accept source only after new emulator process logs ExecutionFlow::SaveStateLoaded; five authentic external X11 captures are 1280×800 and F20 visibly retains 空き地 (Tanah kosong), value 140 focus; exit code 0; emitted new checkpoint passes size/v4-header/SHA validation. The emitted output of run34 remains unpromoted until that output gets its own fresh-process restore.

Revision33 board focus rule is VERIFIED narrowly: DOWN on the verified Naruto tile focuses neighboring empty land; WAIT leaves Naruto tile focused. It does not prove movement/capture/ownership change. Story Mode remains NOT COMPLETE.

---

## ACTIVE RUN — revision 34 restore-only checkpoint validation (22 October 2026, 19:39 WIB)

Run [#39780143613](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780143613) is in progress, started 19:39:28 WIB; timeout at approx 19:59:28 WIB. It is restore-only and must send no gameplay input.

Source is run #39779256427 / private artifact #12425858092 / checkpoint `adaptive-cycle-01-f180.sstate` / SHA `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`, a revision-33 ACTION output with map focus changed by DOWN to `空き地` (Tanah kosong), barrier value 140. After the process finishes, check source SHA, explicit SaveStateLoaded event, restore PASS, five authentic 1280×800 X11 captures, exit 0, output checkpoint integrity, and actual C01-F20 image. Only promote the source if this independent restore visibly preserves the focus. Do not promote the newly emitted output until it is restored in another process.

---

## VERIFIED BOARD RULE — one DOWN changes focused tile to empty land (revision 33, 22 October 2026, 19:38 WIB)

Matched A/B run [#39779256427](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39779256427) fully passed the explicit map-view state gate. Private artifact #12425858092: both arms loaded the same source SHA b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc in separate processes; two SaveStateLoaded events; same cloned Memory Cards; pixel-identical F20; DOWN press/release true/false; WAIT control; ten authentic external-X11 frames at 1280×800; exit 0 twice; both checkpoint outputs validated; comparison report generated.

**VERIFIED, scoped to this exact board state:** one DOWN changes focused tile from Naruto's tile (Level 1, barrier value 60, durability 2/2) to adjacent 空き地 (Tanah kosong) with barrier value 140; WAIT leaves Naruto's tile focused. No actual player move/capture/ownership change is established. Both classifier labels stay map_after_move; visual manual review of C01/C02 screenshots establishes the focus change.

Next: fresh-process restore of ACTION output SHA 58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a from run #39779256427, artifact #12425858092, file adaptive-cycle-01-f180.sstate, revision34 restore-only. Require load event, five genuine screenshots that retain empty land value 140 focus, exit 0 and external size/header/SHA validation. Do not promote the new output produced by that restore until it itself is restored. Stop before confirming/selecting a tile.

Story Mode remains NOT COMPLETE. All gameplay artifacts remain private and out of Git. Use START for dialogue.

---

## VERIFIED — DOWN changes focused map tile; restore output before continuation (22 October 2026, 19:37 WIB)

Run [#39779256427](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39779256427) revision 33 passed every paired acceptance gate. Private artifact #12425858092 was audited. Two independent emulator processes loaded the identical map source SHA `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`; each logged SaveStateLoaded; cloned Memory Cards were identical; F20 states matched pixel-for-pixel (1,024,000 px) and both classify `map_after_move`; DOWN press/release readback true/false; WAIT control; ten authentic external 1280×800 frames; both exits 0; both output checkpoints passed external post-exit validation. Comparison report generated.

**VERIFIED, scoped to this exact board:** one DOWN changes the focused tile from Naruto's tile (`レベル` (Level) 1, `結界価値` (Nilai penghalang) 60, `耐久値` (Daya tahan) 2/2) to adjacent `空き地` (Tanah kosong), barrier value 140, level ---, durability -/-. WAIT keeps original tile focused. This is focus/selection movement only; do not infer actual Naruto movement, capture, ownership change, or battle progression. Classifier state stays `map_after_move`; manual authentic screenshot comparison is decisive.

ACTION output candidate: run #39779256427 / private artifact #12425858092 / `adaptive-cycle-01-f180.sstate`, 21,162,559 bytes, header v4, SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`. CONTROL output: 21,162,390 bytes, v4, SHA `3796ff4ba91fef93ddf1078daa1785e043c3d5b5424a03c8cb53a62c6d3858a4`. Neither is promoted until independently restored.

### Revision 34 — restore-only
Use source run #39779256427, artifact `naruto-storymode-adaptive-player-private`, file `adaptive-cycle-01-f180.sstate`, SHA `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`; set `RESTORE_TEST=1`, `CONTINUATION_TEST=0`, `AB_TEST=0`, `LOOP_CYCLES=1`, `REVISION=34`. No button input. Require load event, five genuine X11 captures, exit 0, external size/header/SHA validation; manually inspect F20 for retained empty-land focus. If passes, promote this exact source candidate as a restorable state. Keep the new restore-run output unpromoted until another fresh-process restore validates it. Story Mode remains NOT COMPLETE; START skips dialogue.

---

## ACTIVE RUN — revision 33 checks DOWN on map with explicit expected-state validator (22 October 2026, 19:33 WIB)

Run [#39779256427](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39779256427) is in progress from 19:32:59 WIB; X11 tools/workspace prep is the latest active step. Timeout deadline approximately 19:52:59 WIB. Wait for this single player to finish; do not start parallel runs.

Config: source run #39776518701 / private artifact #12425305517 / `adaptive-cycle-01-f180.sstate` / source SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`; `AB_TEST=1`, `AB_ACTION=DOWN`, `AB_EXPECTED_STATE=map_after_move`, `LOOP_CYCLES=2`, restore/continuation tests disabled, revision 33. This explicit state repairs revision 32's failure, where an older workflow checkout erroneously expected `menu_or_unknown_choice` on F20.

After completion audit every evidence gate and manually inspect the private artifact. Revision32 screenshots tentatively show DOWN focuses the empty land `空き地` (Tanah kosong) / value 140 instead of Naruto's value-60 tile, but its run must remain HYPOTHESIS due final validation failure. Only revision33's clean corrected A/B evidence may promote that rule to VERIFIED. No confirmation input and no destination selection. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision 33 map directional A/B uses explicit expected state (22 October 2026, 19:33 WIB)

Run [#39779256427](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39779256427) is active, started 19:32:59 WIB; timeout about 19:52:59 WIB. Do not start a parallel player. Its marker explicitly sets AB_EXPECTED_STATE=map_after_move and pins the independently restored source SHA b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc from run #39776518701.

After it ends, require exact parent SHA / two load events, F20 map_after_move state and pixel parity, byte-identical Memory Card clones, DOWN press/release readback true/false, WAIT control, ten authentic 1280×800 frames, two exit 0s, post-exit checkpoint validation for both outputs and the generated comparison report. Review screenshots. The candidate effect (DOWN moves board focus from Naruto's tile to adjacent empty land 空き地 (Tanah kosong), value 140) remains HYPOTHESIS until corrected run passes.

Revision32 (#39777917775) had the right input and screenshots but failed because its old checkout forced menu_or_unknown_choice in the final A/B state gate; do not promote its outputs. Story Mode remains NOT COMPLETE. Keep gameplay evidence private/out of Git; use START to skip dialogue.

---

## REVISION 32 DIAGNOSTIC — old state-parity gate rejected correct map baseline (22 October 2026, 19:30 WIB)

Run #39777917775 failed the workflow's final semantic-state gate, not the emulator session. Artifact #12426395775 shows both arms loaded source SHA b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc in fresh processes; F20 was pixel-identical (0 mismatch/1,024,000 pixels); two load events; ACTION DOWN readback true then false; control WAIT; 10 authentic 1280×800 captures; both emulator exits 0; and both output checkpoint structure/hash validations passed. Failure: old checkout SHA b77f74af5b258dfcd7d8bfbeeeca0c685c5fc7b7 hard-coded Python states to menu_or_unknown_choice, while both actual F20 states correctly classify as map_after_move. No ab-comparison-report.txt was written. Neither output state is promoted.

Manual paired screenshot inspection suggests (HYPOTHESIS only) DOWN moved focus away from Naruto's board tile (Level 1, barrier value 60, durability 2/2) to an adjacent empty tile labeled 空き地 (Tanah kosong), barrier value 140. ACTION/control differ by over 719,000 pixels after input, but only a corrected run should promote the rule to VERIFIED.

Revision 33 must set AB_EXPECTED_STATE=map_after_move and run the current workflow with source pinned to run #39776518701 / private artifact #12425305517 / adaptive-cycle-01-f180.sstate / SHA b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc. Use AB_TEST=1, AB_ACTION=DOWN, LOOP_CYCLES=2, RESTORE_TEST=0, CONTINUATION_TEST=0, REVISION=33. Verify the actual marker after commit. Accept only if source hashes, map F20 parity, input readback, two load events, 10 images, exits, output checkpoint validation, and comparison report all pass. Keep the inferred tile-focus effect HYPOTHESIS until then.

Story Mode remains NOT COMPLETE. No confirmed ending/result evidence. Use START for dialogue skipping and keep gameplay assets private/out of Git.

---

## CORRECTION — active revision32 may execute DOWN; only later validator is stale (22 October 2026, 19:25 WIB)

At run #39777917775's checkout SHA b77f74af5b258dfcd7d8bfbeeeca0c685c5fc7b7, Lua precondition accepts map_after_move and classifier WAIT, so the ACTION arm may send DOWN. The later shell/Python state gate still insists menu_or_unknown_choice, however, making workflow failure likely after evidence capture. This corrects the prior note that asserted the run would not send DOWN. The actual result must be decided from run logs and its private artifact, not assumed from configuration.

Only this run is active. Do not trigger another player. After completion, audit exact action input/readback, two restore events, F20 parity, ten authentic X11 captures, both exits and state validation. If the late gate fails, store the failure and retain the directional effect as HYPOTHESIS only. For the corrected next probe, require a new marker with AB_EXPECTED_STATE=map_after_move using workflow commit 4c074472e885c75ce618e4e0f5aefd6a8833a0c9.

---

## ACTIVE CONFIGURATION BLOCKER — map A/B expected-state field missing (22 October 2026, 19:24 WIB)

Only player run #39777917775 is active (started 19:23:17 WIB; timeout about 19:43:17 WIB). The committed marker for revision32 omitted AB_EXPECTED_STATE=map_after_move. Because the source checkpoint is a board/map state SHA b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc but workflow defaults the missing expected state to menu_or_unknown_choice, the Lua precondition should fail closed and choose WAIT. Expect the shell's strict gates to reject this run. Do not launch parallel player or infer any map-direction rule from it.

After completion, audit its actual logs and private artifact. For the corrected run, create revision 33 with all of:
- SOURCE_RUN=39776518701; SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private; SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate; SOURCE_SHA256=b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc
- RESTORE_TEST=0; CONTINUATION_TEST=0; AB_TEST=1; AB_ACTION=DOWN; AB_EXPECTED_STATE=map_after_move; LOOP_CYCLES=2; REVISION=33
Verify the committed marker's literal content before launch. Existing workflow commit 4c074472e885c75ce618e4e0f5aefd6a8833a0c9 has the expected-state support; this missing field is the current blocker.

Story Mode remains NOT COMPLETE. The map-view source is independently restored and trusted; directional movement is still unverified. Keep all gameplay screenshots/ROM/BIOS/savestates/Memory Cards out of Git and use START for dialogue.

---

## RESTORE GATE PASSED — current map-view source is independently restorable (22 October 2026, 19:21 WIB)

Restore-only run [#39777301626](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39777301626) independently restored the revision-30 ACTION/map-view checkpoint from run #39776518701, SHA-256 b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc, size 21,163,227, v4. Five genuine external-X11 captures passed at 1280×800; ExecutionFlow::SaveStateLoaded and ADAPTIVE_RESTORE_TEST=PASS were explicit; all captured frames remain map_after_move; emulator exit 0; new output checkpoint externally validated. Artifact #12423949987 is private. This exact source is promoted as a trusted restorable continuation checkpoint.

The newly produced output SHA a2a3c36918155dc4356da2664bfa7880c9605c62260389b85f85262c942b2fe7 (21,162,251 bytes, v4) is not promoted until another fresh-process restore.

Workflow commit 4c074472e885c75ce618e4e0f5aefd6a8833a0c9 updates matched A/B preconditions to use explicit AB_EXPECTED_STATE; it permits map_after_move only for AB_ACTION=DOWN and validates frame-state parity against the configured state. This must be proven by revision 32 before treating this new branch as reliable.

### Revision 32: directional DOWN probe on map board
Source must remain b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc, run #39776518701 / private artifact #12425305517 / adaptive-cycle-01-f180.sstate. Set RESTORE_TEST=0, CONTINUATION_TEST=0, AB_TEST=1, AB_ACTION=DOWN, AB_EXPECTED_STATE=map_after_move, LOOP_CYCLES=2, REVISION=32. ACTION issues only one DOWN; control WAIT. Hard gates: both F20 states map_after_move, pixel-identical images, same exact parent hash, two load events, byte-identical card clones, button readback press true/release false, ten genuine X11 captures, exit code 0, both checkpoints post-exit validated. Do not make another run while this player is active. Inspect screenshots and stop before confirming any tile.
Story Mode remains NOT COMPLETE. Use START to skip any actual dialogue. Never use web images as gameplay evidence; keep ROM/BIOS/state/cards/screenshots outside Git. Translate Japanese labels immediately into Indonesian.

---

## ACTIVE RUN — map navigation probe in revision 32 (22 October 2026, 19:23 WIB)

Run [#39777917775](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39777917775) is currently in progress, started 19:23:17 WIB; the latest step is installing X11 tools/private workspace. Timeout at ~19:43:17 WIB if not completed earlier. No player run may be launched in parallel.

Config is source run #39776518701 / artifact `naruto-storymode-adaptive-player-private` / checkpoint `adaptive-cycle-01-f180.sstate` / SHA `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`; ACTION=DOWN versus NONE/WAIT, AB_TEST=1, 2 cycles, revision32. The workflow's starting-state precondition was changed in commit `5f8ae63b4374cb730ef197d797dffd0e823db141` to allow either `menu_or_unknown_choice` or `map_after_move` only with WAIT classification.

Await completion, then verify exact parent hash, F20 parity, actual input readback, 2 load events, 10 authentic X11 images, clean/accepted exits and external post-exit checkpoint checks. Inspect pixels before describing effects; never confirm the highlighted map tile. Story Mode remains NOT COMPLETE.

---

## RESTORE-VERIFIED MAP VIEW — controlled DOWN probe is next (22 October 2026, 19:20 WIB)

Run [#39777301626](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39777301626) passed. Actual private artifact #12423949987 was inspected, including C01-F20. The original revision-30 ACTION checkpoint from run #39776518701 / artifact #12425305517, `adaptive-cycle-01-f180.sstate`, SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`, size 21,163,227 and v4 header, was loaded in a fresh process and remained on the tile/map screen. Logs show `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`; five 1280×800 external-X11 captures validate; emulator exit 0; external new-output verification passes.

**Promoted trusted source:** `b5715ba7...` is now restore-proven map-view state.
**Do not promote the new restore-run output:** 21,162,251 bytes, SHA-256 `a2a3c36918155dc4356da2664bfa7880c9605c62260389b85f85262c942b2fe7`, v4. It must be restored independently before use.

Workflow commit `5f8ae63b4374cb730ef197d797dffd0e823db141` extends the matched-test starting-state guard from only `menu_or_unknown_choice` to (`menu_or_unknown_choice` OR `map_after_move`), still requiring action WAIT. This allows a safe action-vs-WAIT probe from the screenshot-confirmed map screen. The control cycle's safety guard already allows `map_after_move` + WAIT.

### Next run — revision 32
Source run #39776518701, artifact `naruto-storymode-adaptive-player-private`, checkpoint `adaptive-cycle-01-f180.sstate`, SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`; settings `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `AB_TEST=1`, `AB_ACTION=DOWN`, `LOOP_CYCLES=2`, `REVISION=32`. Run it only when no other player run is active. Pair DOWN vs WAIT, check same F20 pixels/state, exact parent source both arms, readback press/release, two load events, 10 authentic 1280×800 screenshots, accepted exits, both post-exit state validations. Visually review all post-action screenshots for map cursor movement. No Circle, no destination confirmation. Keep ambiguous rules HYPOTHESIS/UNKNOWN.
Story Mode remains NOT COMPLETE and must not be reported as completed without genuine ending/results evidence. Dialogue skipping is START.

---

## VERIFIED RULE — Triangle opens the board/map view from the View-map row (22 October 2026, 19:15 WIB)

Run [#39776518701](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39776518701) fully passed matched TRIANGLE versus WAIT from the verified-restorable menu parent `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7`. Both arms logged `ExecutionFlow::SaveStateLoaded`, identical Memory Card clones, identical 1,024,000-pixel F20 screenshots, input true/false readback, ten authentic external 1280×800 X11 captures, exit code 0, and external post-exit checkpoint validation.

**VERIFIED, exact tested context:** with `マップを見る` (Lihat peta) highlighted, TRIANGLE opens the board/map screen by F60; WAIT keeps the menu open. Verified by direct inspection of C01-F60 against C02-F60 in private artifact #12425305517; classifier agrees with ACTION `map_after_move` and control `menu_or_unknown_choice`. The board screenshot includes status `レベル` (Level) 1, `結界価値` (Barrier value) 60, `耐久値` (Durability) 2/2, and footer `△ マップ` (Triangle: Map). No tile/destination chosen.

ACTION output state `adaptive-cycle-01-f180.sstate`: 21,163,227 bytes, v4 header, SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`; private artifact #12425305517. Must not use as continuation until an independent fresh-process restore proves it.

Next use revision31 restore-only:
```
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
Require fresh process `ExecutionFlow::SaveStateLoaded`, five authentic captures confirming the map view, accepted exit and external size/header/SHA validation. Only after this run completes, one DOWN-versus-WAIT probe can test map movement; keep the experiment short, paired and fail-closed. Do not confirm a tile without clear visual grounding.

Story Mode remains NOT COMPLETE. Continue START dialogue skip; keep all ROM/BIOS/savestate/Memory Card/screenshots out of Git. Translate Japanese labels into Indonesian immediately beside each occurrence.

---

## VERIFIED — Triangle opens tile/map view; validate that output before further input (22 October 2026, 19:15 WIB)

Matched experiment [run #39776518701](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39776518701) passed every evidence gate. Private artifact #12425305517 was manually reviewed. Same source SHA `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7` in both new processes; both log `ExecutionFlow::SaveStateLoaded`; Memory Card clones identical; F20 pixel parity (1,024,000 pixels); TRIANGLE press/release true/false; ten authentic external-X11 captures 1280×800; exit 0 in both arms; both outputs externally validated.

**VERIFIED, scoped to the tested state:** a TRIANGLE input while `マップを見る` (Lihat peta) is highlighted opens a tile/map view by F60. NONE/WAIT stays in the prior menu. Actual ACTION F60/F180 screens show hex/tile positions, tile values and a character panel; footer `× もどる` translates as (X: Kembali). Do not select a destination during this test. This does not prove any movement, capture, attack, defense, territory or battle rule.

ACTION output candidate: source run #39776518701, private artifact #12425305517, file `adaptive-cycle-01-f180.sstate`, size 21,163,227, v4 header, SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`. Not yet promoted: it must be loaded in a separate new emulator process and visually retain the map view. CONTROL output hash `dc91b2756581456e75dee8cd836dc7b3c1e43fde88978dbf15545f231a6c0f98`, 21,163,215 bytes, also unpromoted.

### Revision 31 restore-only test
Use source run #39776518701 / artifact `naruto-storymode-adaptive-player-private` / `adaptive-cycle-01-f180.sstate` / SHA `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`; set `RESTORE_TEST=1`, `CONTINUATION_TEST=0`, `AB_TEST=0`, `LOOP_CYCLES=1`, `REVISION=31`. No input is allowed. Require `ExecutionFlow::SaveStateLoaded`, five genuine 1280×800 X11 screenshots, an accepted exit and post-exit output size/header/SHA validation; inspect F20 for the same tile/map view. Only after success promote the revision-30 ACTION input checkpoint as trusted. Keep the new output unpromoted until it is itself restored.

Next later-stage research, after the restore gate passes: inspect the tile layout and displayed values in the map view before planning a single-variable direction probe. Story Mode remains NOT COMPLETE; the finish screen has not been observed. Keep all gameplay assets private/out of Git; START is the only dialogue skip.

---

## RESTORE-VERIFIED CHECKPOINT — next A/B should probe Triangle (22 October 2026, 19:11 WIB)

Restore-only run [#39776089816](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39776089816) passed. Private artifact #12425065836 confirms `ExecutionFlow::SaveStateLoaded`, `ADAPTIVE_RESTORE_TEST=PASS`, five external-X11 captures at 1280×800, exit code 0, and post-exit external checkpoint validation. It restored the revision-28 ACTION checkpoint (run #39775176728) with exact SHA-256 `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7`, 21,162,344 bytes, v4 header; inspected F20 visibly retains `マップを見る` (Lihat peta) as the selected row. **This exact original checkpoint is promoted as restorable.**

New output checkpoint from restore-only run: 21,163,104 bytes, SHA-256 `9d1ed105227c095c42396595bccd51ecf06f564ae5342f01377dec1f3aa94292`, v4; not promoted until that output itself is independently restored.

### Revision 30 — matched Triangle versus WAIT
Use source run #39775176728, artifact `naruto-storymode-adaptive-player-private`, file `adaptive-cycle-01-f180.sstate`, source SHA `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7`, `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `AB_TEST=1`, `AB_ACTION=TRIANGLE`, `LOOP_CYCLES=2`, `REVISION=30`. Do not start another run until the prior player run has terminated. Require all paired evidence gates (same exact parent, byte-identical F20 screenshots/states, Triangle press/release true/false readback, two `ExecutionFlow::SaveStateLoaded` events, ten external 1280×800 X11 captures, accepted exits, both output checkpoint external validations). Manually review screenshots to decide if Triangle opens the map; don't rely on the generic classifier. Stop at map view without selecting a destination.

The revision-28 rule stays VERIFIED only for the observed state: DOWN moves the selected row from `情報` (Informasi) to `マップを見る` (Lihat peta). Story Mode remains NOT COMPLETE. Keep all gameplay assets private and out of Git; START is the dialogue-skip input.

---

## LATEST VERIFIED RESULT — DOWN moves Information highlight to View map (22 October 2026, 19:05 WIB)

Run [#39775176728](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39775176728) fully passed the required paired experiment. Private artifact #12424660712 was reviewed. Source parent SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e) was identical for both fresh processes; each logged `ExecutionFlow::SaveStateLoaded`; cloned Memory Cards were hash-identical; F20 images were pixel-identical; DOWN press/release readback passed; ten 1280×800 external-X11 images passed; both emulator exits were 0; and both output states passed external size/header/SHA validation.

**VERIFIED, scoped rule:** from the right-hand menu row `情報` (Informasi), one DOWN shifts the red selection marker to `マップを見る` (Lihat peta); NONE/WAIT leaves Information selected. Paired images show this transition, with 14,636 differing pixels / mean absolute RGB difference 1.05798 in all post-action comparisons. The vision classifier remains at `menu_or_unknown_choice`; visually verify the highlighted Japanese row rather than trusting its generic state label. This does not yet show that the map itself is open.

ACTION checkpoint candidate: run #39775176728, private artifact #12424660712, `adaptive-cycle-01-f180.sstate`, size 21,162,344, v4 header, SHA-256 `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7`. It remains unpromoted until an independent fresh-process restore succeeds. Control output `adaptive-cycle-02-f180.sstate`: 21,162,426 bytes, SHA-256 `30b062df8985fa79f8c9f79e076cb464f1ff73143103e249dba5d35ca94324d5`; not promoted either.

### Next controlled cycle
1. Run revision 29 as restore-only from source run 39775176728 / artifact `naruto-storymode-adaptive-player-private` / checkpoint `adaptive-cycle-01-f180.sstate` / SHA `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7`, with `RESTORE_TEST=1`, `AB_TEST=0`, `CONTINUATION_TEST=0`, `LOOP_CYCLES=1`. Require load-event log, five authentic 1280×800 captures, visible retained map-row highlight, accepted exit, and external output state validation.
2. Only after that run completes, start revision 30 as matched TRIANGLE-versus-WAIT from the now independently restore-proven candidate; require all existing pair gates. Inspect the resulting screens; stop at map view, no destination selection.
3. Keep screenshots/states/card/ROM/BIOS out of Git. START skips dialogue in Story Mode. Story Mode remains NOT COMPLETE; final completion requires genuine in-game ending/result evidence.


---

## CURRENT ACTION — revision 28 matched DOWN/NONE run queued (22 October 2026, 19:02 WIB)

Marker revision 28 was committed at `e31ebb2afbe1145746e480e9a0f020854621a82f`, triggering [run #39775176728](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39775176728). At the latest check it is **in progress**, with the step `Install X11 tools and prepare private workspace` active. It started at 19:02:38 WIB; the workflow job has a 20-minute hard timeout (around 19:22:38 WIB if not completed earlier). It tests ACTION=DOWN against NONE/WAIT from the known-restorable Information parent `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`; 2 cycles, `AB_TEST=1`. Do not start another player run. Next chat must check this exact run, its latest job steps and artifacts/logs, then apply the strict paired-evidence gates documented here. Job timeout is 20 minutes after a runner starts; queued wait has no reliable ETA. Story Mode remains NOT COMPLETE.

---

## LATEST RESULT — restore smoke passed; run paired action/control next (22 October 2026, 18:48 WIB)

Run [#39772650469](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39772650469) completed with success. Revision 27/source SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e` restored in a fresh emulator process; explicit `ExecutionFlow::SaveStateLoaded`, five genuine 1280×800 X11 captures, exit code 0 and post-exit size/header/hash verification all passed. New output: 21,162,547 bytes, v4, SHA-256 `cb53613ffa09e57d0f6d927d9e82bf603937871a07a9ed24c0955735cf258fdc`, private artifact #12422499045. It is a valid emitted checkpoint but **not a promoted continuation source** until a fresh process restores it.

Next: revision 28 paired A/B from the known source #39768787669 / SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`, ACTION DOWN versus NONE/WAIT, two cycles. Require parent frame/state parity; action press/release readback; two load events; all 10 external-X11 frames; accepted exits; and external output checkpoint size/header/SHA checks. The previous action-only observation that DOWN from `情報` (Informasi) may move to `マップを見る` (Lihat peta) remains HYPOTHESIS, not a verified rule. Story Mode is not complete.

---

## ACTIVE SMOKE — validate single-nextTick shutdown with a restore-only run (22 October 2026, 18:45 WIB)

Run [#39772650469](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39772650469) uses the known-restorable Information state SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`, `RESTORE_TEST=1`, `LOOP_CYCLES=1`, revision 27. It was still installing X11 tools at the last check (active since 18:43:28 WIB). Current workflow has the established single out-of-VSync nextTick quit; both prior drain approaches timed out while paused. Check load event, five external X11 frames, exit and external size/header/SHA validation before any new gameplay probe. Do not fire a parallel run or promote untested checkpoints.

---

## DIAGNOSTIC UPDATE — use single deferred quit after paused drain loops stalled (22 October 2026, 18:39 WIB)

Run #39771377339 failed before the control branch. It did capture five authentic external-X11 frames and its output state was full-size (21,162,276 bytes), had PCSX-Redux SaveState v4 header, and SHA-256 `a2d055634da951b8c9703ac1d30ac0981d4508404527604ddf4e803fe08935b5` in private artifact #12423430123. But the 12 chained nextTick loop did not advance after pausing, leading to watchdog rc=124. The file is not promoted as a resume source because clean emulator completion and the paired test did not happen.
- The preceding 12-VSync drain (#39770465538) had the same watchdog timeout. Both artifacts' savestates were full-sized/headered on inspection, but neither drain implementation proved clean completion.
- Workflow commit `df6e3d5afab0a9efeac89aa8bcb0be2e273ef631` returns to single `pauseEmulator()` then `PCSX.nextTick(function() PCSX.quit(0) end)`, with only shell-side external validation post-exit. Accept native exit 139 only if checkpoint passes validation and the session-finished sentinel is present.
- The visual sequence suggests DOWN from `情報` (Informasi) may highlight `マップを見る` (Lihat peta), but without the control arm this is HYPOTHESIS, not a verified game rule.

Next run should be a one-cycle `RESTORE_TEST=1` smoke using pinned known-restorable source SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`. Require the load event, five post-load external-X11 images, process completion, and external checkpoint validation before resuming paired gameplay.

---
## DIAGNOSTIC UPDATE — VSync drain did not advance after checkpoint; retest with host nextTick chain (22 October 2026, 18:31 WIB)

Run [#39770465538](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39770465538) stopped at the ACTION branch. Its 12-VSync drain did not receive further frame events after save and the emulator hit the 120-second timeout (exit 124). Private artifact #12422367156 contains 5 valid genuine X11 frames and a file measured at 21,162,494 bytes with the expected v4 header and SHA-256 `0c33a47cb9e6f2dfb09c568410ca125acbae6f46f84692b8589a5c903442f564`. The images suggest DOWN selected `マップを見る` (Lihat peta) from `情報` (Informasi), but the NONE branch did not run and allowed shutdown plus output validation did not finish. Record this only as HYPOTHESIS, not a verified rule.

Workflow commit `3e052b8e77cfcd966f5e5e05a2f7341ed2ff0374` now pauses after save and calls quit only after a chain of 12 `PCSX.nextTick` callbacks, instead of a VSync-dependent drain. Retest from the immutable, known-restorable parent SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`; only trust output after two-branch parity/input evidence, allowed process exit, and external size/header/hash checks.

Story Mode is not complete.

---

## DIAGNOSTIC UPDATE — VSync drain stalled after a full-sized write (22 October 2026, 18:31 WIB)

- Run #39770465538 captured all five authentic X11 frames for the ACTION arm and read DOWN press/release correctly. Its checkpoint file was 21,162,494 bytes, v4 header, SHA-256 `0c33a47cb9e6f2dfb09c568410ca125acbae6f46f84692b8589a5c903442f564`, but the process timed out (exit 124) after `ADAPTIVE_SHUTDOWN_DRAIN_BEGIN` without `ADAPTIVE_SHUTDOWN_DRAIN=PASS`. No control arm ran, so no matched rule conclusion is allowed.
- First drain implementation relied on more `GPU::Vsync` callbacks; none arrived after F180. Commit [`3e052b8`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/3e052b8e77cfcd966f5e5e05a2f7341ed2ff0374) changes to pause + 12 bounded `PCSX.nextTick` callbacks before quit outside VSync. Treat this as unverified until a fresh retry exits cleanly and both outputs pass post-exit validation.
- Source parent remains independently restored run #39768787669 action state: SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`. Keep marker as rev25 until explicitly triggering one revision26 retry with ACTION=DOWN, control=NONE. Never promote the timeout checkpoint.
- Story Mode is still NOT COMPLETE; no ending/results image exists.

---

## DIAGNOSTIC UPDATE — Information-down matched test stopped on invalid checkpoint (22 October 2026, 18:23 WIB)

Run [#39769826213](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39769826213) produced five valid authentic X11 captures for the ACTION arm, with F20 showing `情報` (Informasi) selected. The source SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e` and identical Memory Card clones were verified; DOWN press/release readbacks passed. However, the emulator exited 139 and the new savestate file was only 2,097,152 bytes; external size validation rejected it, so no control branch ran and no rule result can be claimed.

Workflow commit `13da48ab08ef40d0be8c8bbc850b7babbb9b107e` adds a controlled 12-VSync no-input drain after write/close and before pause/quit. This is a best-effort flush safeguard; retry output must still pass external size/header/SHA and matched-state guards. Never trust a checkpoint only from the successful write/close log. Story Mode remains NOT COMPLETE.

---

## ACTIVE PROBE — next row after Information menu item (22 October 2026, 18:20 WIB)

Run [#39769826213](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39769826213) is active from the proven-restorable Information-selection parent checkpoint `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`. ACTION sends one DOWN; control sends NONE/WAIT; Memory Cards are cloned from the same baseline but stored separately. This tests whether the highlight moves from `情報` (Informasi) to `マップを見る` (Lihat peta). Do not claim until matching F20 frames, input readback, both load events and checkpoint validation are audited. Run was starting at the last check.

---

## VERIFIED UPDATE — Information-highlight checkpoint restored (22 October 2026, 18:18 WIB)

- Run [#39769265269](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39769265269) successfully restored the ACTION checkpoint from #39768787669 with exact source SHA-256 `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`.
- The emulator logged `ExecutionFlow::SaveStateLoaded`, produced five authentic external-X11 captures with F20 visually retaining `情報` (Informasi) selected, and exited 0.
- New restore-run output checkpoint is 21,162,446 bytes with SHA-256 `6159214a9006127c70f190f0d64b2ed3fb7f9e58ffddd5e4546a0a18820114c6` and passed external size/header/SHA validation after exit. It remains unpromoted until it is itself restored in a fresh process. Continue from the proven-reloadable pinned source `aa399bd...`.
- Next: matched DOWN-versus-NONE test from Information parent to test if DOWN highlights `マップを見る` (Lihat peta). Circle is forbidden unless a contextual choice visibly highlights YES. Story Mode not complete.

---

## VERIFIED UPDATE — second DOWN navigation step passed matched test (22 October 2026, 18:14 WIB)

- Run [#39768787669](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768787669) passed with identical F20 parent images (1,024,000/1,024,000 pixels), separate but byte-identical Memory Cards, two explicit `ExecutionFlow::SaveStateLoaded` events, ten authentic external-X11 frames and two clean emulator exits.
- ACTION branch pressed/released DOWN with readback true/false; NONE branch sent no input. Visual review shows ACTION moving the selection from `忍術` (Ninjutsu) to `情報` (Information), while NONE stayed on Ninjutsu. Visual delta: 14,606 pixels and mean absolute RGB difference 1.04012 at F60/F100/F110/F180.
- Narrow rule: **VERIFIED** one DOWN moves the current right-side menu highlight Ninjutsu→Information from this exact tested state. Generalizing to other menus remains UNKNOWN/HYPOTHESIS; keep rules scoped.
- Neither output savestate from this run should be promoted to a continuation source before fresh-process restoration. The already restored checkpoint #39768371975 is the approved source for the next experiment: 21,162,575 bytes; SHA-256 `fa03a1840612749810453566a25805e89a4aa21ad64664695e09ed7222b77a9e`; it displays Ninjutsu highlighted and `△ マップ` (Triangle: Map).
- Next action is Triangle-versus-NONE from that immutable source. Stop at the map view if opened and inspect before any further action. Do not confirm or select map targets with Circle.

Story Mode remains NOT COMPLETE; no authentic ending/results screenshot exists.

---

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
