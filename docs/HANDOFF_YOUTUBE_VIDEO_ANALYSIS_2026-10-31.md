# Handoff — YouTube gameplay analysis and ROM cross-check (31 October 2026)

## Project boundary
- Project: Naruto – Shinobi no Sato no Jintori Gassen (PS1), SLPS-03553.
- Permitted repository only: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research.
- Do not access or modify Tile Duel or another Naruto runner repository.
- Keep ROM, BIOS, Memory Card, savestate, RAM dump, raw video/audio, frames, and private screenshots outside Git.
- Keep findings separated as VERIFIED, VIDEO-OBSERVED, HYPOTHESIS, or UNKNOWN. The new video-only guide uses the requested labels TERAMATI, HIPOTESIS, and BELUM DIKETAHUI while preserving the distinction between video observation and ROM verification.
- Do not start gameplay, restore a checkpoint, or send adaptive-player input unless the existing fail-closed gates and explicit permissions allow it.

## Video source
- URL: https://www.youtube.com/watch?v=r30Rs_NuExc
- Video ID: r30Rs_NuExc
- Metadata title: INILAH GAME NARUTO MONOPOLI PS 1 PRASEJARAH! - Naruto: Shinobi no Sato no Jintori Kassen Indonesia
- Channel metadata: Kevin Tedja.
- Transcript retrieval: completed in Indonesian; prior checkpoint records 5 credits used.
- Visual watch/scene analysis: completed for exact video ID; prior checkpoint records 25 credits used. The result was read from the existing completed job; it was not re-submitted.
- Coverage: 00:00–173:15. The video reaches the Stage 4 Land of Waves mission briefing but does not show Stage 4 gameplay/completion.

## Primary results

### New chronological video-only play guide
The guide covers the opening menu through the final Stage 4 briefing, and marks each mechanic as TERAMATI, HIPOTESIS, or BELUM DIKETAHUI. It also explains the limits of the broad timestamped scene breakdown and does not invent per-turn inputs or formulas.

### Source analysis and transcript
Video scene-by-scene report:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/c9b980143cdf32a8c70aaa7467662e23efd7b911/reports/youtube_source_access/VIDEO_WATCH_ANALYSIS_2026-10-31.md

Transcript candidate notes (updated after visual analysis):
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cb547e6499157346d0ae8cd2ebcec9416889b6ef/reports/youtube_source_access/TRANSCRIPT_PRELIMINARY_GAMEPLAY_NOTES_2026-10-31.md

Pipeline log:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/52bb4c7e0d22b78e663175fd1272f9d2e737593c/docs/YOUTUBE_VIDEO_ANALYSIS_PIPELINE_2026-10-31.md

## Key video observations (not ROM-verified)
- Stage 1 vs Mizuki: mission target 3,000 Chakra; starting Chakra 1,500 each; board movement roulette 1–8; barrier/node levels up to 5; scroll cards and battle.
- Stage 2 vs Sakura, with Naruto + Konohamaru: target 4,000; starting Chakra 2,000 each.
- Stage 3 Team 7 Bell Test: Naruto/Sasuke/Sakura/Kakashi; target 4,000; starting Chakra 2,000 each.
- Challenge Stage: separate tree-climbing minigame; Naruto vs Sasuke; video analysis reports 600 Chakra and win by reaching top or draining opponent Chakra to 0.
- Stage 4 briefing: Land of Waves, Demon Brothers/Zabuza; target 5,000; no stage completion shown.
- Visual analysis reports barrier build/upgrade, toll, attack/defense choices and roulette, takeover roulette 10+, scroll/card effects, negative Chakra and barrier release. Exact formulas remain unknown.
- Japanese UI examples and Indonesian translations appear adjacent in the detailed report.

## ROM cross-check already documented
- Static game-rule table has records matching Stage 1 values (1,500/3,000), Stage 2/3 values (2,000/4,000), several 2,500/5,000 records, and two 600/0 records.
- Video values corroborate some configuration field interpretations, but no exact scenario-to-record mapping has been proved.
- Static Chakra setter permits negative values within its storage clamp; video reports Mizuki at negative Chakra before barrier release. This is a correlation, not proof of release threshold/selection formula.
- Static RNG call sites have not been mapped to the three visible randomization contexts (movement 1–8, takeover 10+, battle attack/defense).
- Victory scene values reported by visual analysis (Stage 1 ~9,963; Stage 2 ~5,806; Stage 3 ~10,690) are not the mission target numbers. Do not infer trigger timing from the final score alone.

ROM cross-check and evidence levels:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/5f63725d8928022dc0ad390d0866fb9bf138f231/docs/GAME_RULES.md

Prioritized test plan:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/ecbf9d202c611f126ae649e23aaa6a3e6e96a616/docs/RUNTIME_TEST_PLAN.md

## Next work
1. For a deeper video-only pass, obtain precise visual timestamps/frame-level notes for each menu action, one full neutral/own/opponent tile transaction, one complete battle, one card/trap effect, and the first frame where victory is triggered. The existing scene breakdown alone does not support exact per-turn control instructions.
2. Continue offline code/data audit to identify the selector that chooses each scenario configuration record; prove the record ID-to-stage mapping before changing labels.
3. Trace the victory-check chain around the Chakra target, including the option flag and any node/milestone gate. Compare trigger timing, not only the final Chakra value.
4. Trace node ownership/level/toll/barrier durability and adjacent-node fields from data layout through the transaction handler.
5. Separate RNG call chains for board movement, battle attack/defense, and barrier takeover; never assume they share the same random range.
6. Map scroll/card/trap effect IDs and their state changes. Test one effect per controlled experiment when runtime gates permit.
7. Treat the tree-climbing Challenge Stage as a separate state machine; test the candidate 600/0 configuration mapping independently.
8. Reuse validated emulator evidence/checkpoints only. Do not run Story Mode or modify adaptive player based solely on the external video report.

## Status
- YouTube metadata check: completed.
- Indonesian transcript: completed.
- Visual scene-by-scene analysis: completed.
- Chronological video-only play guide: completed and committed.
- Text-only report and ROM cross-check: completed.
- Internal ROM logic mapping and controlled runtime verification of these candidate mechanics: incomplete.
- Story Mode: not proven complete.
