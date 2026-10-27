# Langkah 4 — hasil runtime RNG + roulette

- Actions run: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40471968654
- Uji: checkpoint roulette f120 yang sama; dua cabang Circle f30; satu cabang Circle f60; target capture semua cabang F177; tiap cabang memakai proses emulator baru, CPU interpreter, breakpoint eksekusi RNG dan pembacaan RAM state.
- Screenshot X11 dibandingkan pada viewport game ter-normalisasi crop (105,22)-(1175,760) untuk mengecualikan chrome/menu emulator yang berubah antarproses.
- Sumber checkpoint read-only; ROM/BIOS/Memory Card/savestate hanya di ruang privat runner. Screenshot eksternal X11 hanya disimpan pada artefak Actions, tidak di Git.

## Hasil
- SAME_SAVESTATE_SAME_DELAY_DETERMINISM=UNKNOWN
- SAME_DELAY_STATE_SAMPLES_MATCH=True
- SAME_DELAY_CALL_TRACE_MATCH=False
- SAME_DELAY_GAME_VIEWPORT_MATCH=False
- DIFFERENT_DELAY_FRAME_FREE_CALL_SEQUENCE_MATCH=True
- DIFFERENT_DELAY_STATE_SAMPLES_MATCH=True
- DIFFERENT_DELAY_GAME_VIEWPORT_MATCH=False
- DIFFERENT_DELAY_OBSERVED_RNG_OR_VIEWPORT_EFFECT=YES
- RUNTIME_RNG_CALLSITES=80105f48, 8010b0e8, 8010c20c, 8010c248, 8010c68c
- Catatan: callsite runtime dihitung sebagai RA-8 pada entry 0x80035D78; urutan caller tanpa frame dipakai untuk membedakan stream RNG dari pergeseran timing VSync.

## Log hasil per cabang
- R30A: load=True, finished=False, RNG hits=127, samples=F1=0xdb75c114 (calls=0), F20=0xdb75c114 (calls=0), F30=0xdb75c114 (calls=0), F38=0x03f64fb2 (calls=2), F60=0x3c3c2ca6 (calls=126), F80=0x3c3c2ca6 (calls=126), F100=0x3c3c2ca6 (calls=126), F150=0x3c3c2ca6 (calls=126), F160=0x3c3c2ca6 (calls=126), F170=0x3c3c2ca6 (calls=126), seed setter hits post-load=0, F177 viewport SHA256=MISSING.
  Caller hits: F32 8010b0e8 state=db75c114, F32 8010b0e8 state=bb6f7dbd, F38 8010c20c state=03f64fb2, F38 8010c248 state=91d45b03, F38 8010c20c state=f277da80, F38 8010c248 state=409b38b9, F38 8010c20c state=a575b4fe, F38 8010c248 state=cab7a45f, F38 8010c20c state=84c01eac, F38 8010c248 state=742da775, F38 8010c20c state=99f4230a, F38 8010c248 state=935c277b, F38 8010c20c state=96667998, F38 8010c248 state=e63e45f1, F38 8010c20c state=4b3965d6, F38 8010c248 state=9dfbc057, F38 8010c20c state=d3159744, F38 8010c248 state=b6e0502d, F38 8010c20c state=a5be0962, F38 8010c248 state=9c920af3, F38 8010c20c state=5476e3b0, F38 8010c248 state=fa1ec229, F38 8010c20c state=72f759ae, F38 8010c248 state=db38634f, F38 8010c20c state=635e8adc, F38 8010c248 state=5fb857e5, F38 8010c20c state=0c6362ba, F38 8010c248 state=2441e56b, F38 8010c20c state=1fb778c8, F38 8010c248 state=9a9b8d61.
- R30B: load=True, finished=False, RNG hits=127, samples=F1=0xdb75c114 (calls=0), F20=0xdb75c114 (calls=0), F30=0xdb75c114 (calls=0), F38=0x03f64fb2 (calls=2), F60=0x3c3c2ca6 (calls=126), F80=0x3c3c2ca6 (calls=126), F100=0x3c3c2ca6 (calls=126), F150=0x3c3c2ca6 (calls=126), F160=0x3c3c2ca6 (calls=126), F170=0x3c3c2ca6 (calls=126), seed setter hits post-load=0, F177 viewport SHA256=MISSING.
  Caller hits: F32 8010b0e8 state=db75c114, F32 8010b0e8 state=bb6f7dbd, F38 8010c20c state=03f64fb2, F38 8010c248 state=91d45b03, F38 8010c20c state=f277da80, F38 8010c248 state=409b38b9, F38 8010c20c state=a575b4fe, F38 8010c248 state=cab7a45f, F38 8010c20c state=84c01eac, F38 8010c248 state=742da775, F38 8010c20c state=99f4230a, F38 8010c248 state=935c277b, F38 8010c20c state=96667998, F38 8010c248 state=e63e45f1, F38 8010c20c state=4b3965d6, F38 8010c248 state=9dfbc057, F38 8010c20c state=d3159744, F38 8010c248 state=b6e0502d, F38 8010c20c state=a5be0962, F38 8010c248 state=9c920af3, F38 8010c20c state=5476e3b0, F38 8010c248 state=fa1ec229, F38 8010c20c state=72f759ae, F38 8010c248 state=db38634f, F38 8010c20c state=635e8adc, F38 8010c248 state=5fb857e5, F38 8010c20c state=0c6362ba, F38 8010c248 state=2441e56b, F38 8010c20c state=1fb778c8, F38 8010c248 state=9a9b8d61.
- DELAY60: load=True, finished=False, RNG hits=127, samples=F1=0xdb75c114 (calls=0), F20=0xdb75c114 (calls=0), F30=0xdb75c114 (calls=0), F38=0x03f64fb2 (calls=2), F60=0x3c3c2ca6 (calls=126), F80=0x3c3c2ca6 (calls=126), F100=0x3c3c2ca6 (calls=126), F150=0x3c3c2ca6 (calls=126), F160=0x3c3c2ca6 (calls=126), F170=0x3c3c2ca6 (calls=126), seed setter hits post-load=0, F177 viewport SHA256=MISSING.
  Caller hits: F32 8010b0e8 state=db75c114, F32 8010b0e8 state=bb6f7dbd, F38 8010c20c state=03f64fb2, F38 8010c248 state=91d45b03, F38 8010c20c state=f277da80, F38 8010c248 state=409b38b9, F38 8010c20c state=a575b4fe, F38 8010c248 state=cab7a45f, F38 8010c20c state=84c01eac, F38 8010c248 state=742da775, F38 8010c20c state=99f4230a, F38 8010c248 state=935c277b, F38 8010c20c state=96667998, F38 8010c248 state=e63e45f1, F38 8010c20c state=4b3965d6, F38 8010c248 state=9dfbc057, F38 8010c20c state=d3159744, F38 8010c248 state=b6e0502d, F38 8010c20c state=a5be0962, F38 8010c248 state=9c920af3, F38 8010c20c state=5476e3b0, F38 8010c248 state=fa1ec229, F38 8010c20c state=72f759ae, F38 8010c248 state=db38634f, F38 8010c20c state=635e8adc, F38 8010c248 state=5fb857e5, F38 8010c20c state=0c6362ba, F38 8010c248 state=2441e56b, F38 8010c20c state=1fb778c8, F38 8010c248 state=9a9b8d61.

## Gate assessment
- Roulette runtime: four distinct caller addresses are observed while the verified roulette checkpoint is loaded; visible roulette viewport is pixel-identical across these f30/f35 timing probes through F100. This identifies roulette-window activity, but does not yet map a call to the final selected roulette outcome.
- Battle runtime caller: UNKNOWN; this probe starts from roulette checkpoint and has not entered battle.
- Seed source at game startup: not settled by a post-load window if no setter breakpoint is seen; static candidate setter remains documented.
- Alternative RNG/non-function randomness: static signature scan does not exclude other algorithms, tables, frame-derived values or code decoded only at runtime.
- STEP 4 OVERALL: SEBAGIAN until the battle caller, runtime seed lifecycle and alternative-randomness scope are proved.

