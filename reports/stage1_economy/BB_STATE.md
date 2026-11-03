# BB_STATE — status terbaru

Tanggal: 3 November 2026  
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

| Tahap | Status | Kelas bukti | Ringkasan dan batas |
|---|---|---|---|
| BB1 | TUNTAS — seluruh target statis selesai | K4 | FUN_800BE0E4 mengikuti tautan +0x01, filter tile type5 dan owner bits12–15 sama, menulis jumlah successor valid ke +0x0B. Resource 22 record membuktikan 22/22 link satu tile ortogonal membentuk ring. FUN_800B770C menerima selector +0x0B 0–4 saja (>=5 return 0) dan menghitung H×100/120/150/180/200%; cocok dengan batas kelompok 1–5 serta contoh 50/60/70. H = u16(tile+0x10+((u16(tile+0x20)>>7)&0x1E)). Report final supplement commit d51fcf3d3db08d18be96fd59620344a8868e69dc. |
| BB2 | SEBAGIAN — debit 3/8, kredit 1/0x1D, fee dan satu jalur action8 dinamis terpetakan | K4 untuk formula/control-flow; K2–K3 untuk label/produser dinamis | Debit 3/8: fee=u16(tile+0x1A), guard participant+0x04, pending−fee manager+0x2EE+player*2, nibble +0x20 bits8–11 dan4–7 masing-masing +1; owner bits12–15 tetap; fee tidak bergantung level. Kredit 1/0x1D: token pesan0xBE, preview C=+0x1E+level(bits8–11)*+0x1C, metadata +0xA18/+0xA1A, phase2 commit pending-positive +0x2EE+player*2 and projected balance +0x51C (gate +0x370==1 and FUN_80102408()==0). Produser immediate: 3@0x800DAA88/FUN_800D9570; 8@0x800EC3A8/FUN_800EB434; 8@0x800EF3CC/function NONE. Jalur tidak langsung: FUN_800EA18C menetapkan +0x2E9=8@0x800EA654, lalu pada queue iVar4==3 menyalin ke +0x2EB@0x800EAA44. 65 writes census belum seluruhnya di-origin trace. Teks token0xBE, label visual action, unit Chakra dan Barrier Release TIDAK TAHU. Latest static AQ1 run41558104325 STATUS=SUCCESS JOB=analyze-entry1-buffer-base JOB_ID=125662? SOURCE_SHA=a15a0fda198625a3dbdfb04052c1929db90da7bf EXIT_CODE=0. Detailed report commit c965445eff5c3dfc97bc8901478e9e73a48f4f64. |
| BB3 | SEBAGIAN — dua percobaan matriks 40 launch masih aktif; full matrix belum terverifikasi | K5 terbatas untuk subcakupan lama; matriks 40-case belum K5 | Run41550406414 16/16 PASS (tile4/action3,8/level0–3/dua launch); run41552617808 20/20 transaksi tetapi RAM snapshot frame2 salah dan exit2; run41553653484 cancelled. Perbaikan concurrency commit87a0e111c8928a75848dad41d830df594bc011c3. Run41556732137 job125657970152 masih IN_PROGRESS step11; run41557380908 job125659457807 masih IN_PROGRESS step11; keduanya belum punya TSV hasil, status cleanup/publish pending. No complete 40-case TSV, matching 2 MiB frame180 RAM reference, Memory Card before/after SHA and exit0; do not claim TUNTAS/K5 full. |

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


## BB2 update — AQ1 41555549917

- Static AQ1 run success: RUN_ID=41555549917; JOB=analyze-entry1-buffer-base; JOB_ID=125653445027; SOURCE_SHA=37beb791fcc48c859b58c312ec1800d44ef77497; EXIT_CODE=0. Compact result: reports/stage1_economy/aq1-run-41555549917/attempt-1/ACTIONS_RUN_SUMMARY.txt.
- 65 manager+0x2EB write sites re-censused; immediate candidates 3 at 0x800DAA88, 8 at 0x800EC3A8 and 8 at 0x800EF3CC. Remaining copies/read-from +0x2E9 and unknown register values still not all traced.
- Positive credit path detail: byte+0x2EB=1/0x1D → DAT_80139F03=1. State1 computes and previews +0x1E + level×+0x1C, then LAB_800D5704 increments state to 2. State2 requires manager+0x370==1 and FUN_80102408()==0, then writes pending positive credit at manager+0x2EE+player*2 and projected balance manager+0x51C. No proof of UI label 結界開放 or currency meaning Chakra.
- BB2 status remains SEBAGIAN. Detailed report update commit d0f950beac863f18ee1c948385e3d8822b65dea7; changed file: reports/stage1_economy/BB1_BB2_STATIC_COMPLETE_2026-11-03.md.


- BB1 final selector multiplier/bound proof: FUN_800B770C checks byte +0x0B < 5, returns zero for 5+, and maps selector0..4 to H, H*12/10, H*15/10, H*18/10, H*2. This resolves the earlier loop-cap discrepancy and establishes 1–5-tile cluster multiplier. Report commit d51fcf3d3db08d18be96fd59620344a8868e69dc; file changed: reports/stage1_economy/BB1_BB2_STATIC_COMPLETE_2026-11-03.md.


### BB2 fee completion details

- Action 3/8 debit block uses tile+0x1A, not neutral-price +0x0E. Tile4 resource630 observed neutral price=120 and fee=100; the same fee field is not multiplied by level, so for this tile every level operation costs 100. Other type4 tiles carry fee fields 50,100,120,150,200 respectively; fee is per tile, not global.
- Two tile level nibbles at tile+0x20 bits8–11 and bits4–7 each increment +1; owner bits12–15 do not change on that path. Pre/post value calculations are stored in participant manager+0x922/+0x924 via FUN_800B770C.
- Latest independent static census run 41556229574: STATUS=SUCCESS, JOB=analyze-entry1-buffer-base, JOB_ID=125655667589, SOURCE_SHA=dc0046b205d4490e5a91f1075fe6eab0a082aa50, EXIT_CODE=0. Compact text summary: reports/stage1_economy/aq1-run-41556229574/attempt-1/ACTIONS_RUN_SUMMARY.txt.
- Detailed evidence report latest commit 06fcbfa113ca745e66f200ff7981ed6e419e491e; changed file: reports/stage1_economy/BB1_BB2_STATIC_COMPLETE_2026-11-03.md.


### BB2 — hasil statis terakhir

- Run 41557054116: STATUS=SUCCESS, JOB=analyze-entry1-buffer-base, JOB_ID=125658376355, SOURCE_SHA=28b3c7380f483e0e158e6089851d7d4a4e72e3e8, EXIT_CODE=0. Ringkasan: reports/stage1_economy/aq1-run-41557054116/attempt-1/ACTIONS_RUN_SUMMARY.txt.
- Laporan bukti: commit a87d24ac83379317d559dfb3743ea79ff25f8566; file berubah: reports/stage1_economy/BB1_BB2_STATIC_COMPLETE_2026-11-03.md.
- Rumus kredit, preview, dan pending commit terdokumentasi. Teks ID 0xBE dan identitas gameplay/currency masih TIDAK TAHU; BB2 belum boleh TUNTAS.

### BB3 — run baru setelah perbaikan cancellation

- Commit perbaikan workflow: 87a0e111c8928a75848dad41d830df594bc011c3; file berubah: .github/workflows/bb3-h6-action-call-probe.yml.
- Run 41557380908, job 125659457807, source SHA 87a0e111c8928a75848dad41d830df594bc011c3; status IN_PROGRESS. Steps 1–10 completed successfully and the 40-launch step 11 is running. H6 smoke-test PASS.
- Previous run 41553653484 was cancelled and did not produce the full matrix TSV; its smoke-test must not be reported as action-test success.



### BB2 latest producer refinement — commit c965445eff5c3dfc97bc8901478e9e73a48f4f64

- Changed file: reports/stage1_economy/BB1_BB2_STATIC_COMPLETE_2026-11-03.md.
- Indirect action8 route in FUN_800EA18C: manager+0x2E9=8 at PC0x800EA654; later queue iVar4==3 copies that value into +0x2EA and +0x2EB at PCs0x800EAA40/0x800EAA44, then sets +0x2E9=0x0F. This supplements direct immediate 8 stores at 0x800EC3A8 and 0x800EF3CC, and direct immediate3 at 0x800DAA88.
- The function FUN_800BA9F8 is an overlay/sprite helper; its call parameter8 is not itself an action-byte producer.
- The latest Step7 static trace extension is commit 424743337e525da13d8a376aaede756c0b7f1400; changed file: .github/workflows/step7-entry1-buffer-base-audit.yml. It adds DATA.BIN targets FUN_800C2570 and FUN_80100E9C to trace dynamic event and message rendering. Run41559535429 (job125666521042) was IN_PROGRESS at last poll, source SHA424743337e525da13d8a376aaede756c0b7f1400; await only current repository result, do not assume success.

### BB3 poll update

- Run41557380908 job125659457807 still IN_PROGRESS at last poll, step10 smoke PASS and step11 40 isolated launches active. Run41556732137 job125657970152 also remained IN_PROGRESS on earlier source. No results or TSV have been published, so status is unchanged.



### Status workflow terkini (3 November 2026)

- BB3 run41556732137/job125657970152: IN_PROGRESS, step11 "Run 40 isolated H6 function-call launches"; cleanup and text-only publication pending.
- BB3 run41557380908/job125659457807: IN_PROGRESS, step11 "Run 40 isolated H6 function-call launches"; H6 smoke step10 SUCCESS, cleanup/publication pending.
- Static Step7 run41559535429/job125666521042: IN_PROGRESS, step11 "Recount AQ1 TSV and commit text-only report"; source SHA424743337e525da13d8a376aaede756c0b7f1400. This run includes targets FUN_800C2570 and FUN_80100E9C; no result has been published yet.
- BB2 dynamic producer report commit c965445eff5c3dfc97bc8901478e9e73a48f4f64; changed file reports/stage1_economy/BB1_BB2_STATIC_COMPLETE_2026-11-03.md.
- Workflow expansion commit 424743337e525da13d8a376aaede756c0b7f1400; changed file .github/workflows/step7-entry1-buffer-base-audit.yml.
