# BB_STATE — status terbaru

Tanggal: 3 November 2026  
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

| Tahap | Status | Kelas bukti | Ringkasan dan batas |
|---|---|---|---|
| BB1 | TUNTAS dalam cakupan statis | K4 | Semua enam direct byte store +0x0B Entry 1 telah dipilah. Hanya dua menulis record petak di DAT_8013EA84 + index×0x124; empat lainnya menulis objek selector DAT_8013A680. Perilaku statis +0x0B ialah nilai/status rantai tile type 5 per owner; nama gameplay kanonik tetap TIDAK TAHU. Resource 630: 22 record; mapping empat snapshot H6 cocok 1.760/1.760 field. |
| BB2 | TUNTAS dalam cakupan statis | K4 | Action byte 3/8 di FUN_800D15A8 membaca fee u16(tile+0x1A), memeriksa saldo participant+0x04, menyimpan pending delta −fee pada manager+0x2EE, menaikkan nibble tile+0x20 bits 8–11 dan 4–7 masing-masing satu, lalu memanggil FUN_800BB004 dan FUN_800BE464. Nama gameplay action 3/8 tetap TIDAK TAHU. |
| BB3 | SEBAGIAN — runtime terbatas telah lolos; perluasan penuh masih berjalan | K5-terbatas pada subcakupan lama; K0 hasil matriks baru sampai diterbitkan | Run 41550406414: 16/16 PASS untuk tile 4, action 3/8, level 0–3, dua launch/kondisi; pending −100, kedua nibble +1, kedua refresh helper tercapai, Memory Card disposable tetap identik. Ini direct dispatch-block test pada H6 HIBRIDA, tanpa input kontrol. Perluasan baru run 41553653484 sedang menjalankan 40 launch: tile 4/7 × action 3/8 × level 0–4 × dua launch; snapshot RAM 2 MiB pre-poke ditangkap setelah post-load VSync 180 agar bisa dibandingkan dengan baseline frame-180. Belum ada TSV final atau exit code script. |

## PC acuan

- BB1: FUN_800BE0E4 reset tile+0x0B di 0x800BE1B0 dan menulis hitungan rantai di 0x800BE330; FUN_800BE464 membaca +0x0B di 0x800BE544 dan 0x800BE5A0.
- BB2: FUN_800D15A8; action byte dibaca di 0x800D4470; dispatch block mulai 0x800D4468; selector FUN_800BBD9C dipanggil di 0x800D45D0; fee dibaca di 0x800D4628; pending debit ditulis di 0x800D46F8; nibble bits 8–11 diubah pada 0x800D4724–0x800D4764; nibble bits 4–7 diubah pada 0x800D47F4–0x800D4834; refresh di 0x800D4840/0x800D4848.
- BB3: direct probe memasuki dispatch di 0x800D4464, memeriksa action byte di 0x800D4470, memilih tile di 0x800D45D0, mencapai helper refresh di 0x800D4840/0x800D4848, dan kembali ke sentinel 0x80011448.

## Run, job, dan commit penting

- BB1 parser-corrected census: run 41541206308, job 125605524941, source SHA b4baaa6cb65715f5c71223440f23e7d88822d504, workflow SUCCESS, script exit 0.
- Expanded BB1/BB2 function detail and direct caller census: run 41541667221, job 125607103118, source SHA 3ef6c43fd1fb3f352546bb538a61aa2ef2ce5a96, workflow SUCCESS, script exit 0.
- BB1/BB2 static report: reports/stage1_economy/BB1_BB2_STATIC_COMPLETE_2026-11-03.md.
- BB3 runtime limited pass: run 41550406414, job 125636294382, source SHA 57ee8f4cba1ff2b15b1a9674d8dfbeb63fcfbf5e, workflow SUCCESS, script exit 0, 16/16 PASS, Memory Card unchanged.
- BB3 expanded level 0–4 single-tile attempt: run 41552617808, source SHA 109742216f46251dfd16648b9ec6795dcdfcccbf; 20/20 transaction bodies behaved as expected, but validation failed because RAM capture at post-load VSync 2 was compared to frame-180/frame-360 references. Pre-poke SHA was 70dd6e9301e4375950595c32d5214b53eea31ab9f95ae56a4ebfa9f7cc9365e0; load-event SHA 3ad7b85c857a868d91df4b3f1049c23889a0dc482ad7ee390ac8b6c05c3190f4. Neither is a valid frame-180 baseline.
- BB3 frame-aligned two-tile probe: commit c1a81420980eaca43a5369f3ecf7f9af4b534c57, changed files experiments/bb3_h6_action_call_probe.py and .github/workflows/bb3-h6-action-call-probe.yml; adds wait for post-load VSync 180, exact frame RAM references, tile indices 4 and 7, fee expectations 100 and 120, and a 40-condition matrix.
- BB3 matrix indentation fix: commit 889838f3b52a2211881ff64228dceaf22db11ba7, changed file experiments/bb3_h6_action_call_probe.py.
- BB3 current Actions run: run 41553653484, job ID 125647454203, source SHA 889838f3b52a2211881ff64228dceaf22db11ba7; workflow/job still in progress at this update. Active step: Run 40 isolated H6 function-call launches. Final TSV, summary, script exit code, workflow-script exit code not yet available.

## Baseline RAM SHA references

- H6 hybrid frame 180, two-launch stable SHA-256: 5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7.
- H6 hybrid frame 360, two-launch stable SHA-256: 4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907.
- Both reference hashes come from BA3 run 41418131290 and repeated BA3 run 41419506538; each captured 2 MiB RAM at explicit post-load VSync frames; two independent launches agreed per frame. Frame-180 and frame-360 hashes are intentionally different.

## Batas tetap

- Semantik kanonik field petak +0x0B: TIDAK TAHU.
- Nama aksi visual/gameplay untuk action byte 3 dan 8: TIDAK TAHU. Jangan menyebut action 3/8 sebagai Barrier placement tanpa bukti UI/gameplay.
- BB3 yang sudah lulus menguji direct dispatch-block dengan frame/register disiapkan pada H6 hybrid. Tidak ada controller input; hasil tidak membuktikan alur UI/Story Mode murni.
- Rumus positif 3 petak: floor(sum(nilai 3 petak milik pemain)/2)+400 adalah kontrol terpisah dan belum diuji dalam BB3.
- H6 adalah fixture HIBRIDA, bukan checkpoint target murni atau save Story Mode murni.
- Adaptive-player automation tetap dijeda. Tidak ada perubahan ke Tile Duel atau repositori lain.
- Tidak ada ROM/ISO, BIOS, savestate, Memory Card, raw RAM dump, screenshot/video/frame atau binary yang dikomit/dipublikasikan.
