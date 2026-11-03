# BB_STATE — status terbaru

Tanggal: 3 November 2026  
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

| Tahap | Status | Kelas bukti | Ringkasan dan batas |
|---|---|---|---|
| BB1 | TUNTAS dalam cakupan statis | K4 | Semua enam direct byte store +0x0B Entry 1 telah dipilah. Dua store menulis record petak DAT_8013EA84 + index×0x124; empat lain menulis objek selector DAT_8013A680. FUN_800BE0E4 menghitung jumlah link lanjutan type-5 dengan owner sama, lalu menulis count itu ke semua record rantai. Hubungan link dengan tetangga geometris, batas gameplay maksimum lima, dan label gameplay +0x0B tetap TIDAK TAHU. Resource 630: 22 record; mapping 4 snapshot H6 cocok 1.760/1.760 field. |
| BB2 | SEBAGIAN | K4 untuk blok transaksi/debit/kredit; K2–K3 untuk producer mapping | FUN_800D15A8 membaca fee u16(tile+0x1A), memeriksa saldo+0x04, mengisi pending debit−fee pada +0x2EE, menaikkan nibble bits8–11 dan bits4–7, lalu refresh. Cabang kredit terpisah state DAT_80139F03=2 dengan input FUN_80102408()==0 menulis +0x1E + level×+0x1C. Producer byte3 (FUN_800D9570) dan byte8 (FUN_800EB434) serta caller FUN_800F3658 diketahui; store 8 ketiga PC0x800EF3CC belum punya function entry/caller. Nama gameplay action 3/8 tetap TIDAK TAHU. |
| BB3 | SEBAGIAN — K5-terbatas pada subcakupan lama | K5-terbatas | Run 41550406414: 16/16 PASS untuk tile4, action3/8, level0–3, dua peluncuran independen/kondisi; delta pending−100, kedua nibble naik, kedua refresh tercapai, Memory Card disposable tidak berubah. Run 41552617808: 20/20 launch transaksi menghasilkan perubahan yang diharapkan untuk level0–4, tetapi RAM pre-poke ditangkap pada 2 VSync dan tidak cocok baseline frame180/frame360; script exit2. Run 41553653484 masih in_progress pada langkah 40 launch: tile4/7 × action3/8 × level0–4 × dua launch; RAM pre-poke harus dicapture setelah 180 post-load VSync agar dibandingkan baseline frame180. Belum ada TSV final/summary/exit code untuk run ini. |

## PC acuan

- BB1: FUN_800BE0E4 reset tile+0x0B di 0x800BE1B0 dan menulis nilai rantai di 0x800BE330; FUN_800BE464 membaca +0x0B di 0x800BE544 dan 0x800BE5A0.
- BB2: FUN_800D15A8; action byte dibaca di 0x800D4470; dispatch block mulai 0x800D4468; selector FUN_800BBD9C di 0x800D45D0; fee dibaca di 0x800D4628; pending debit ditulis di 0x800D46F8; level nibble bits8–11 di 0x800D4724–0x800D4764; bits4–7 di 0x800D47F4–0x800D4834; refresh 0x800D4840/0x800D4848.
- BB2 producer: byte3 write 0x800DAA88 (FUN_800D9570), caller FUN_800F3658 PC0x800F5E1C; byte8 write 0x800EC3A8 (FUN_800EB434), caller FUN_800F3658 PC0x800F5CF8; extra byte8 write 0x800EF3CC not attributed to a Ghidra function/caller.
- BB2 credit trigger: FUN_800D15A8 case DAT_80139F03==2, manager+0x370==1, FUN_80102408()==0; credit tile+0x1E + (tile+0x20 bits8–11)×tile+0x1C, pending to participant manager+0x2EE + participant_index×2.
- BB3: direct dispatch probe enters 0x800D4464, observes action byte 0x800D4470, selector 0x800D45D0, refresh helpers 0x800D4840/0x800D4848, returns sentinel 0x80011448.

## Bukti statis dan laporan

- Addendum BB1/BB2: reports/stage1_economy/BB1_BB2_PRODUCER_AND_CLUSTER_ADDENDUM_2026-11-03.md
- Kompilasi bukti statis: reports/stage1_economy/BB1_BB2_STATIC_COMPLETE_2026-11-03.md (status telah dikoreksi: BB2 SEBAGIAN).
- BB1 census parser-heksadesimal: run 41541206308, job 125605524941, source SHA b4baaa6cb65715f5c71223440f23e7d88822d504, workflow SUCCESS, script exit0.
- Expanded BB1/BB2 census: run 41541667221, job 125607103118, source SHA 3ef6c43fd1fb3f352546bb538a61aa2ef2ce5a96, workflow SUCCESS, script exit0.
- BB2 producer/caller expansion: workflow edit commit b68ba43a183519b1a5b3ef499f92c660432ebe8a; changed file .github/workflows/step7-entry1-buffer-base-audit.yml; Step7 run 41554925881 queued, source SHA b68ba43a183519b1a5b3ef499f92c660432ebe8a.
- BB3 runtime limited PASS: run 41550406414, job125636294382, source SHA57ee8f4cba1ff2b15b1a9674d8dfbeb63fcfbf5e, workflow SUCCESS, script exit0, 16/16 PASS.
- BB3 20-launch level0–4 one-tile attempt: run41552617808, job125643691591, source SHA109742216f46251dfd16648b9ec6795dcdfcccbf, 20/20 launches, card unchanged, but RAM references mismatched due capture at 2 post-load VSync; script exit2 and wrapper process exit2.
- BB3 frame-aligned two-tile matrix fix: commit c1a81420980eaca43a5369f3ecf7f9af4b534c57 changed experiments/bb3_h6_action_call_probe.py and .github/workflows/bb3-h6-action-call-probe.yml; waits to post-load VSync180, compares exact RAM references, tiles4/7, fees100/120, 40 conditions.
- BB3 matrix loop indentation fix: commit 889838f3b52a2211881ff64228dceaf22db11ba7; changed experiments/bb3_h6_action_call_probe.py.
- BB3 current run: run41553653484, job125647454203, source SHA889838f3b52a2211881ff64228dceaf22db11ba7, workflow/job in_progress at last check, active step “Run 40 isolated H6 function-call launches”, 10/16 prior steps passed, no step failure yet.

## Baseline RAM SHA references

- Frame180 two-launch stable RAM2MiB SHA-256: 5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7.
- Frame360 two-launch stable RAM2MiB SHA-256: 4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907.
- Both hashes are from BA3 runs 41418131290 and repeated 41419506538. They are intentionally different frames and not interchangeable.

## Batas tetap

- Geometri neighbor dari tile+0x01 link: TIDAK TAHU; code proves link-chain only.
- Gameplay max group size five: belum dibuktikan statis; loop accepts at most five forward links and can therefore touch up to six records (start + five).
- Gameplay name for +0x0B and action bytes3/8: TIDAK TAHU.
- No normal UI/controller-input Story Mode proof in BB3; it is direct dispatch-block test in H6 hybrid fixture.
- User-confirmed end-turn income formula floor(sum nilai seluruh petak milik pemain /2)+400 has not been re-tested in BB3 and is separate from per-tile positive delta.
- H6 is HIBRIDA, not pure Story Mode.
- Adaptive-player automation stays paused. No access/modification to Tile Duel or other repositories.
- No ROM/ISO, BIOS, savestate, Memory Card, raw RAM dump, screenshot/video/frame or binary uploaded/published.


### BB1 completion

- Status: TUNTAS (statis, K4). 22/22 edge rows in reports/stage1_economy/BA1_STAGE1_RESOURCE_630_RECORDS.tsv have a one-tile orthogonal delta through +0x01 links. Report and falsifiers: reports/stage1_economy/BB1_BB2_STATIC_COMPLETE_2026-11-03.md, commit 31462f2168a79de208fa03bbfdf65b5cfad836e7.
- Changed file for report commit: reports/stage1_economy/BB1_BB2_STATIC_COMPLETE_2026-11-03.md.

### BB2 refinements

- Action 3 immediate writer 0x800DAA88 in FUN_800D9570; action 8 immediate writer 0x800EC3A8 in FUN_800EB434. Positive branch triggers from byte 1 at 0x800CF94C (function entry unresolved) or 0x1D at 0x800E0928 in FUN_800E03B0, then state global DAT_80139F03=1, then positive formula +0x1E+level×+0x1C. Action labels/currency identity still TIDAK TAHU.
- Current detailed report commit: 61f38a400ac6982be7702160f3ece49eebe4e1be was superseded for BB1 addendum by report commit 31462f2168a79de208fa03bbfdf65b5cfad836e7; BB2 sections remain in same report path.

