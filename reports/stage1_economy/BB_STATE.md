# BB_STATE — status terbaru

Tanggal: 3 November 2026  
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

| Tahap | Status | Kelas bukti | Ringkasan dan batas |
|---|---|---|---|
| BB1 | TUNTAS — audit statis selesai | K4 | FUN_800BE0E4 mengikuti link +0x01, filter type5 dan owner bits12–15 sama, lalu menulis jumlah successor valid ke +0x0B. Existing TSV resource 630: 22/22 link satu tile ortogonal membentuk ring. Nilai +0x0B = successor count/ukuran rantai−1. Kode loop memungkinkan 5 successor (hingga 6 petak total); ini berbeda dari observasi pengguna maksimal 5 petak/selector 0–4, sehingga clamp gameplay masih TIDAK TAHU. Nilai resource index4 +0x0E=120; +0x10..+0x16=60/140/265/530 cocok observasi. Errata report commit 55d440a7889e459892cd5f7e4802ede5742967e0. |
| BB2 | SEBAGIAN — transaksi debit/kredit terpetakan, producer coverage belum lengkap | K4 untuk jalur transaksi; K2–K3 untuk identitas producer/action | Action 3/8 berbagi jalur: fee u16(tile+0x1A), guard saldo+0x04, pending−fee +0x2EE, nibble 8–11 dan 4–7 tile+0x20 masing-masing +1; owner tidak berubah. Producer 3: 0x800DAA88 FUN_800D9570. Producer 8: 0x800EC3A8 FUN_800EB434 dan 0x800EF3CC (function entry TIDAK TAHU). Positive credit trigger +0x2EB=1 (0x800CF94C; function unresolved) atau 0x1D (FUN_800E03B0/0x800E0928) → DAT_80139F03=1 → +0x1E+level×+0x1C. Banyak dari 65 stores +0x2EB belum ditrace; nama action dan currency Chakra/Barrier Release TIDAK TAHU. Report latest commit 146e8aa6fb2664599a3a7ad3a03501b91a4c5d4e. |
| BB3 | SEBAGIAN — runtime K5-terbatas pada subcakupan lama; perluasan masih berjalan | K5-terbatas | Run 41550406414: 16/16 PASS untuk tile4, action3/8, level0–3, dua launch/kondisi; pending−100, kedua nibble naik, dua refresh tercapai, Memory Card disposable tidak berubah. Run 41552617808: 20/20 launch pada action3/8, level0–4 menunjukkan perubahan transaksi yang diharapkan, tetapi RAM pra-poke dicapture pada 2 VSync dan tidak cocok dengan baseline frame180/frame360; script exit2. Run 41553653484 masih IN_PROGRESS pada matriks 40 launch: tile4/7 × action3/8 × level0–4 × dua launch; pra-poke RAM 2 MiB dicapture setelah 180 post-load VSync agar bisa dibandingkan dengan baseline frame180. Belum ada TSV final/summary/exit code. |

## PC acuan

- BB1: FUN_800BE0E4 reset tile+0x0B di 0x800BE1B0 dan menulis nilai rantai di 0x800BE330; FUN_800BE464 membaca +0x0B di 0x800BE544 dan 0x800BE5A0.
- BB2 transaksi: FUN_800D15A8; action byte dibaca di 0x800D4470; dispatch block mulai 0x800D4468; selector FUN_800BBD9C di 0x800D45D0; fee dibaca di 0x800D4628; pending debit ditulis di 0x800D46F8; nibble bits8–11 diubah 0x800D4724–0x800D4764; bits4–7 diubah 0x800D47F4–0x800D4834; refresh 0x800D4840/0x800D4848.
- BB2 producer: action3 store 0x800DAA88 (FUN_800D9570), raw JAL site 0x800F5E1C (caller function UNMAPPED); action8 store 0x800EC3A8 (FUN_800EB434), direct caller FUN_800F3658 at 0x800F5CF8; extra action8 store 0x800EF3CC has no function boundary/caller. FUN_800D15A8 caller FUN_800F3658 at 0x800F5DAC.
- BB2 positive credit: FUN_800D15A8 state DAT_80139F03==2, requires manager+0x370==1 and FUN_80102408()==0; credit = tile+0x1E + level(bits8–11)×tile+0x1C, pending per participant at manager+0x2EE + participant_index×2.
- BB3: direct dispatch probe enters 0x800D4464, observes action byte 0x800D4470, selector 0x800D45D0, refresh helpers 0x800D4840/0x800D4848, returns sentinel 0x80011448.

## Run, job, commit and evidence

- BB1 corrected census: run 41541206308, job125605524941, source SHA b4baaa6cb65715f5c71223440f23e7d88822d504, workflow SUCCESS, script exit0.
- Expanded BB1/BB2 census: run 41541667221, job125607103118, source SHA 3ef6c43fd1fb3f352546bb538a61aa2ef2ce5a96, workflow SUCCESS, script exit0.
- BB2 producer/caller expansion: workflow commit b68ba43a183519b1a5b3ef499f92c660432ebe8a; changed file .github/workflows/step7-entry1-buffer-base-audit.yml. Step7 run41554925881, job125651375879, source SHA b68ba43a183519b1a5b3ef499f92c660432ebe8a, workflow SUCCESS, script exit0. It exports FUN_800F3658 and probes 0x800EF3CC; the third store still has function=NONE.
- Addendum: reports/stage1_economy/BB1_BB2_PRODUCER_AND_CLUSTER_ADDENDUM_2026-11-03.md. It contains chain semantics +0x0B, all six writers/pre-store instruction windows, producer table/callers, state2 positive credit, and hypotheses/falsifiers for neighbor geometry and Barrier Release.
- Static synthesis: reports/stage1_economy/BB1_BB2_STATIC_COMPLETE_2026-11-03.md; corrected to classify BB2 as SEBAGIAN.
- BB3 limited runtime pass: run41550406414, job125636294382, source SHA57ee8f4cba1ff2b15b1a9674d8dfbeb63fcfbf5e, workflow SUCCESS, script exit0, 16/16 PASS.
- BB3 20-launch level0–4 single-tile test: run41552617808, job125643691591, source SHA109742216f46251dfd16648b9ec6795dcdfcccbf, all20 transaction bodies produced expected pending/nibble/refresh changes; Memory Card unchanged; RAM reference checks failed because capture happened at post-load VSync2 rather than frame180; script exit2, workflow-script exit2.
- BB3 frame-aligned two-tile matrix code: commit c1a81420980eaca43a5369f3ecf7f9af4b534c57 changed experiments/bb3_h6_action_call_probe.py and .github/workflows/bb3-h6-action-call-probe.yml; adds frame180 pre-poke RAM sampling, exact frame reference hashes, tile4/7, fees100/120, matrix40.
- BB3 matrix-loop indentation fix: commit889838f3b52a2211881ff64228dceaf22db11ba7 changed experiments/bb3_h6_action_call_probe.py.
- BB3 current run: run41553653484, job125647454203, source SHA889838f3b52a2211881ff64228dceaf22db11ba7; status IN_PROGRESS at last check, active “Run 40 isolated H6 function-call launches”, 10/16 steps successful, no step failure. A later same workflow run41554278531 is pending on older source SHA05f714017a86b7b26e1013a48bdd85e209b173eb.

## Baseline RAM SHA references

- Frame180, two-launch stable 2MiB RAM SHA-256: 5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7.
- Frame360, two-launch stable 2MiB RAM SHA-256: 4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907.
- These hashes come from BA3 runs 41418131290 and repeated 41419506538; frame180 and frame360 are distinct and must not be treated as interchangeable.

## Batas tetap

- Link tile+0x01 dibuktikan sebagai linked chain type-5/owner sama; kedekatan geometris belum terbukti.
- Loop FUN_800BE0E4 accepts max five forward links, potentially six records including start; gameplay max group size five is not yet statically proven.
- Gameplay name for tile+0x0B and action bytes3/8: TIDAK TAHU.
- Positive state2 credit is a candidate for Barrier Release but remains TIDAK TAHU; hypotheses/falsifiers are in the addendum. Do not label B44 as Barrier Release.
- No normal UI/controller-input Story Mode proof in BB3; BB3 is direct dispatch-block test on H6 hybrid fixture.
- User-confirmed end-turn income formula floor(sum owned-tile values /2)+400 is distinct; it has not been retested in BB3.
- H6 is HIBRIDA, not pure Story Mode.
- Adaptive-player automation remains paused. No changes to Tile Duel or other repos.
- No ROM/ISO, BIOS, savestate, Memory Card, raw RAM dump, screenshot/video/frame or binary uploaded/published.
