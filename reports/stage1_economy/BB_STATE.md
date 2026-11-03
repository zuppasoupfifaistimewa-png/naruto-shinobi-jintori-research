# BB_STATE — status terbaru

Tanggal: 3 November 2026
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

| Tahap | Status | Kelas bukti | Ringkasan dan batas |
|---|---|---|---|
| BB1 | TUNTAS dalam cakupan statis | K4 | Semua enam direct byte store +0x0B Entry 1 telah dipilah. Hanya dua menulis record petak di DAT_8013EA84 + index×0x124; empat lain menulis objek selector DAT_8013A680. Arti gameplay kanonik +0x0B tetap TIDAK TAHU; perilaku statisnya nilai/status rantai tile type 5 per owner. Resource 630: 22 record; mapping empat snapshot H6 cocok 1.760/1.760 field. |
| BB2 | TUNTAS dalam cakupan statis | K4 | Action byte 3/8 dalam FUN_800D15A8 membaca fee u16(tile+0x1A), memeriksa saldo participant+0x04, menyimpan pending delta −fee pada manager+0x2EE, menaikkan nibble tile+0x20 bits 8–11 dan 4–7 masing-masing satu, lalu memanggil FUN_800BB004 dan FUN_800BE464. Nama gameplay action 3/8 tetap TIDAK TAHU. |
| BB3 | TUNTAS TERBATAS — konfirmasi runtime blok transaksi | K5-terbatas | Run 41550406414: 16/16 peluncuran independen PASS (action 3/8 × level nibble 0–3 × 2 pengulangan); 0 validation errors; kedua refresh helper tercapai; delta pending −100; kedua nibble naik; Memory Card disposable tidak berubah. Pengujian masuk langsung ke blok dispatch dengan register/frame yang disiapkan, tanpa input kontrol; fixture H6 adalah hibrida, bukan Story Mode murni. Ini bukan bukti nama aksi visual atau seluruh alur UI/gameplay. |

## PC acuan

- BB1: FUN_800BE0E4 reset tile+0x0B di 0x800BE1B0 dan menulis hitungan rantai di 0x800BE330; FUN_800BE464 membaca +0x0B di 0x800BE544 dan 0x800BE5A0.
- BB2: FUN_800D15A8; action byte dibaca di 0x800D4470; dispatch block mulai 0x800D4468; selector FUN_800BBD9C dipanggil di 0x800D45D0; fee dibaca di 0x800D4628; pending debit ditulis di 0x800D46F8; nibble bits 8–11 diubah pada 0x800D4724–0x800D4764; nibble bits 4–7 diubah pada 0x800D47F4–0x800D4834; refresh di 0x800D4840/0x800D4848.
- BB3: probe memasuki dispatch di 0x800D4464, mengamati lbu action byte di 0x800D4470, pemilihan tile di 0x800D45D0, dua refresh helper di 0x800D4840/0x800D4848, dan kembali ke sentinel 0x80011448.

## Run, job, dan commit penting

- BB1 parser-corrected census: run 41541206308, job 125605524941, source SHA b4baaa6cb65715f5c71223440f23e7d88822d504, workflow SUCCESS, script exit 0.
- Expanded BB1/BB2 function detail and direct caller census: run 41541667221, job 125607103118, source SHA 3ef6c43fd1fb3f352546bb538a61aa2ef2ce5a96, workflow SUCCESS, script exit 0.
- BB1/BB2 static report: reports/stage1_economy/BB1_BB2_STATIC_COMPLETE_2026-11-03.md.
- BB3 post-load sequencing fix: commit 59998bf31c4efee0fc3ed6729d973b2f6f20e031; changed experiments/bb3_h6_action_call_probe.py.
- BB3 Lua tile constants: commit d99f57ba98e5b2fc598299ceb69bf1ecc7a2f4c6; changed experiments/bb3_h6_action_call_probe.py.
- BB3 AppImage FFmpeg library isolation: commit b18bf57a19736418466345212e2dc6c6433bd268; changed experiments/aj2_h6_ram_probe.py, experiments/bb3_h6_action_call_probe.py, .github/workflows/bb3-h6-action-call-probe.yml.
- BB3 structured-register direct CPU setup: commit 6a36f6617a947a35efb992163278aed8449921b8; changed experiments/bb3_h6_action_call_probe.py.
- BB3 H6 state-gate staging/measurement: commit cd52c764ff01b89f0cdb147198696232aac138db; changed experiments/bb3_h6_action_call_probe.py.
- BB3 dispatch-block entry with recreated function frame: commit 9c04073ce5c5a5c6768b07d9f211079c32d707ab; changed experiments/bb3_h6_action_call_probe.py.
- BB3 Lua expected-fee and per-predicate validation fix: commit 57ee8f4cba1ff2b15b1a9674d8dfbeb63fcfbf5e; changed experiments/bb3_h6_action_call_probe.py.
- BB3 final controlled runtime run: run 41550406414; job bb3-h6-action-call-probe-release, job ID 125636294382; source SHA 57ee8f4cba1ff2b15b1a9674d8dfbeb63fcfbf5e; workflow conclusion SUCCESS; script exit 0; result STATUS=K5_TERBATAS; 16/16 PASS; validation errors 0; Memory Card unchanged all.

## Batas yang tetap berlaku

- Semantik kanonik field petak +0x0B: TIDAK TAHU.
- Nama aksi visual/gameplay untuk action byte 3 dan 8: TIDAK TAHU. Jangan menyebut action 3/8 sebagai Barrier placement tanpa bukti UI/gameplay tambahan.
- BB3 memverifikasi blok transaksi secara runtime melalui direct dispatch-block test dengan frame/register disiapkan di H6 hybrid. Tidak ada controller input; hasil ini tidak menutup Story Mode gameplay path atau identitas aksi visual.
- Rumus positif 3 petak: floor(sum(nilai 3 petak milik pemain)/2)+400 adalah kontrol terpisah dan TIDAK DIUJI dalam BB3.
- H6 adalah fixture HIBRIDA, bukan save Story Mode murni.
- Adaptive-player automation tetap dijeda. Tidak ada perubahan ke Tile Duel atau repositori lain.
- Tidak ada ROM/ISO, BIOS, savestate, Memory Card, raw RAM dump, screenshot/video/frame atau binary yang dikomit/dipublikasikan.
