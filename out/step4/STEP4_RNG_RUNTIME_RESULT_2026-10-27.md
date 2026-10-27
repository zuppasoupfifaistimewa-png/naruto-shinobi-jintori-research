# Langkah 4 — hasil runtime RNG + roulette

- Actions run: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40470255341
- Uji: checkpoint roulette f120 yang sama; dua cabang Circle f30; satu cabang Circle f35 (jeda berbeda); tiap cabang memakai proses emulator baru, CPU interpreter, breakpoint eksekusi RNG dan pembacaan RAM state.
- Sumber checkpoint read-only; ROM/BIOS/Memory Card/savestate hanya di ruang privat runner. Screenshot eksternal X11 hanya disimpan pada artefak Actions, tidak di Git.

## Hasil
- SAME_SAVESTATE_SAME_DELAY_DETERMINISM=FAIL
- SAME_DELAY_STATE_SAMPLES_MATCH=True
- SAME_DELAY_CALL_TRACE_MATCH=True
- SAME_DELAY_FINAL_SCREENSHOT_MATCH=False
- DIFFERENT_DELAY_OBSERVED_EFFECT=YES
- RUNTIME_RNG_CALLSITES=8010b0e8, 8010c20c, 8010c248, 8010c68c
- Catatan: callsite runtime dihitung sebagai RA-8 pada entry 0x80035D78.

## Log hasil per cabang
- R30A: load=True, finished=True, RNG hits=126, samples=F1=0xdb75c114, F20=0xdb75c114, F30=0xdb75c114, F38=0x03f64fb2, F60=0x3c3c2ca6, F80=0x3c3c2ca6, F100=0x3c3c2ca6, seed setter hits post-load=0, F100 SHA256=f4314e86b9c6e7b7496618422c9ca8298c36d99eabb05f86e672c9882a96af27.
  Caller hits: F32 8010b0e8 state=db75c114, F32 8010b0e8 state=bb6f7dbd, F38 8010c20c state=03f64fb2, F38 8010c248 state=91d45b03, F38 8010c20c state=f277da80, F38 8010c248 state=409b38b9, F38 8010c20c state=a575b4fe, F38 8010c248 state=cab7a45f, F38 8010c20c state=84c01eac, F38 8010c248 state=742da775, F38 8010c20c state=99f4230a, F38 8010c248 state=935c277b, F38 8010c20c state=96667998, F38 8010c248 state=e63e45f1, F38 8010c20c state=4b3965d6, F38 8010c248 state=9dfbc057, F38 8010c20c state=d3159744, F38 8010c248 state=b6e0502d, F38 8010c20c state=a5be0962, F38 8010c248 state=9c920af3, F38 8010c20c state=5476e3b0, F38 8010c248 state=fa1ec229, F38 8010c20c state=72f759ae, F38 8010c248 state=db38634f, F38 8010c20c state=635e8adc, F38 8010c248 state=5fb857e5, F38 8010c20c state=0c6362ba, F38 8010c248 state=2441e56b, F38 8010c20c state=1fb778c8, F38 8010c248 state=9a9b8d61.
- R30B: load=True, finished=True, RNG hits=126, samples=F1=0xdb75c114, F20=0xdb75c114, F30=0xdb75c114, F38=0x03f64fb2, F60=0x3c3c2ca6, F80=0x3c3c2ca6, F100=0x3c3c2ca6, seed setter hits post-load=0, F100 SHA256=8da4be68fa62a3db8a1a04220144963fa0a5c6c2b4ab76667e5a26bcc52cbbff.
  Caller hits: F32 8010b0e8 state=db75c114, F32 8010b0e8 state=bb6f7dbd, F38 8010c20c state=03f64fb2, F38 8010c248 state=91d45b03, F38 8010c20c state=f277da80, F38 8010c248 state=409b38b9, F38 8010c20c state=a575b4fe, F38 8010c248 state=cab7a45f, F38 8010c20c state=84c01eac, F38 8010c248 state=742da775, F38 8010c20c state=99f4230a, F38 8010c248 state=935c277b, F38 8010c20c state=96667998, F38 8010c248 state=e63e45f1, F38 8010c20c state=4b3965d6, F38 8010c248 state=9dfbc057, F38 8010c20c state=d3159744, F38 8010c248 state=b6e0502d, F38 8010c20c state=a5be0962, F38 8010c248 state=9c920af3, F38 8010c20c state=5476e3b0, F38 8010c248 state=fa1ec229, F38 8010c20c state=72f759ae, F38 8010c248 state=db38634f, F38 8010c20c state=635e8adc, F38 8010c248 state=5fb857e5, F38 8010c20c state=0c6362ba, F38 8010c248 state=2441e56b, F38 8010c20c state=1fb778c8, F38 8010c248 state=9a9b8d61.
- DELAY35: load=True, finished=True, RNG hits=126, samples=F1=0xdb75c114, F20=0xdb75c114, F30=0xdb75c114, F38=0x03f64fb2, F60=0x3c3c2ca6, F80=0x3c3c2ca6, F100=0x3c3c2ca6, seed setter hits post-load=0, F100 SHA256=bffcc420e0feb559b4b4e7e06b606d8cf735a95f5490270dba23f16cbae66088.
  Caller hits: F32 8010b0e8 state=db75c114, F32 8010b0e8 state=bb6f7dbd, F38 8010c20c state=03f64fb2, F38 8010c248 state=91d45b03, F38 8010c20c state=f277da80, F38 8010c248 state=409b38b9, F38 8010c20c state=a575b4fe, F38 8010c248 state=cab7a45f, F38 8010c20c state=84c01eac, F38 8010c248 state=742da775, F38 8010c20c state=99f4230a, F38 8010c248 state=935c277b, F38 8010c20c state=96667998, F38 8010c248 state=e63e45f1, F38 8010c20c state=4b3965d6, F38 8010c248 state=9dfbc057, F38 8010c20c state=d3159744, F38 8010c248 state=b6e0502d, F38 8010c20c state=a5be0962, F38 8010c248 state=9c920af3, F38 8010c20c state=5476e3b0, F38 8010c248 state=fa1ec229, F38 8010c20c state=72f759ae, F38 8010c248 state=db38634f, F38 8010c20c state=635e8adc, F38 8010c248 state=5fb857e5, F38 8010c20c state=0c6362ba, F38 8010c248 state=2441e56b, F38 8010c20c state=1fb778c8, F38 8010c248 state=9a9b8d61.

## Gate assessment
- Roulette runtime: callers only count as observed in the verified roulette checkpoint window; link to a visible outcome remains an interpretation unless delay branch differences support it.
- Battle runtime caller: UNKNOWN; this workflow starts from roulette checkpoint and has not entered battle.
- Seed source at game startup: not settled by a post-load window if no setter breakpoint is seen; static candidate setter remains documented.
- Alternative RNG/non-function randomness: static signature scan does not exclude other algorithms, tables, frame-derived values or code decoded only at runtime.
- STEP 4 OVERALL: SEBAGIAN until the battle caller, runtime seed lifecycle and alternative-randomness scope are proved.

