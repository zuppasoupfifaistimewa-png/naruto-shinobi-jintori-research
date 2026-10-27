# Langkah 4 — hasil runtime RNG + roulette

- Actions run: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40468099590
- Uji: checkpoint roulette f120 yang sama; dua cabang Circle f30; satu cabang Circle f60; tiap cabang memakai proses emulator baru, CPU interpreter, breakpoint eksekusi RNG dan pembacaan RAM state.
- Sumber checkpoint read-only; ROM/BIOS/Memory Card/savestate hanya di ruang privat runner. Screenshot eksternal X11 hanya disimpan pada artefak Actions, tidak di Git.

## Hasil
- SAME_SAVESTATE_SAME_DELAY_DETERMINISM=UNKNOWN
- SAME_DELAY_STATE_SAMPLES_MATCH=False
- SAME_DELAY_CALL_TRACE_MATCH=True
- SAME_DELAY_FINAL_SCREENSHOT_MATCH=False
- DIFFERENT_DELAY_OBSERVED_EFFECT=NO_DIFFERENCE_OBSERVED
- RUNTIME_RNG_CALLSITES=NONE OBSERVED
- Catatan: callsite runtime dihitung sebagai RA-8 pada entry 0x80035D78.

## Log hasil per cabang
- R30A: load=False, finished=False, RNG hits=0, samples=NONE, seed setter hits post-load=0, F180 SHA256=MISSING.
- R30B: load=False, finished=False, RNG hits=0, samples=NONE, seed setter hits post-load=0, F180 SHA256=MISSING.
- DELAY60: load=False, finished=False, RNG hits=0, samples=NONE, seed setter hits post-load=0, F180 SHA256=MISSING.

## Gate assessment
- Roulette runtime: callers only count as observed in the verified roulette checkpoint window; link to a visible outcome remains an interpretation unless delay branch differences support it.
- Battle runtime caller: UNKNOWN; this workflow starts from roulette checkpoint and has not entered battle.
- Seed source at game startup: not settled by a post-load window if no setter breakpoint is seen; static candidate setter remains documented.
- Alternative RNG/non-function randomness: static signature scan does not exclude other algorithms, tables, frame-derived values or code decoded only at runtime.
- STEP 4 OVERALL: SEBAGIAN until the battle caller, runtime seed lifecycle and alternative-randomness scope are proved.

