# BB_STATE — status terbaru

Tanggal: 3 November 2026  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

| Tahap | Status | Kelas | Ringkasan |
|---|---|---|---|
| BB1 | TUNTAS statis | K4 | Semua store +0x0B Entry 1 terpilah. Hanya dua store pada record tile DAT_8013EA84 + index×0x124; empat store lain memakai objek selector DAT_8013A680. Perilaku tile+0x0B adalah nilai/status rantai tile type 5 per owner. Nama gameplay exact tetap TIDAK TAHU. Resource 630: 22 record; mapping empat snapshot H6 cocok 1.760/1.760 field. |
| BB2 | TUNTAS statis | K4 | Action byte 3/8 dalam FUN_800D15A8 membaca fee u16(tile+0x1A), memeriksa saldo participant+0x04, menulis pending delta −fee pada manager+0x2EE, menaikkan nibble tile+0x20 bits 8–11 dan 4–7 masing-masing satu, lalu memanggil FUN_800BB004/FUN_800BE464. Nama aksi 3/8 tetap TIDAK TAHU. |
| BB3 | BELUM | K0 transaksi; K2 smoke | H6 read-only smoke PASS dua launch. Probe lama tidak start setup, lifecycle diperbaiki dan kemudian SETUP_FAIL karena konstanta Lua belum ada. Commit berikutnya menambahkan konstanta. Run 41543294021 sedang berlangsung; belum ada hasil transaksi. |

## PC acuan

- BB1: FUN_800BE0E4 reset 0x800BE1B0 dan tulis hitungan rantai 0x800BE330; FUN_800BE464 membaca field +0x0B di 0x800BE544 dan 0x800BE5A0.
- BB2: FUN_800D15A8 dispatch 0x800D4470; selector 0x800D45D0; fee 0x800D4628; pending debit 0x800D46F8; level nibble writes 0x800D4728/0x800D4764 dan 0x800D47F8/0x800D4834; refresh 0x800D4840/0x800D4848.

## Run dan commit

- BB1 parser-corrected census: run 41541206308, job 125605524941, source SHA b4baaa6cb65715f5c71223440f23e7d88822d504, workflow SUCCESS, script exit 0.
- Expanded BB1/BB2 function detail and direct caller census: run 41541667221, job 125607103118, source SHA 3ef6c43fd1fb3f352546bb538a61aa2ef2ce5a96, workflow SUCCESS, script exit 0.
- BB1/BB2 final static report: reports/stage1_economy/BB1_BB2_STATIC_COMPLETE_2026-11-03.md; committed at c8ddfb90ede88552662ec59c47125a88be2f2092.
- BB3 lifecycle fix: commit 59998bf31c4efee0fc3ed6729d973b2f6f20e031, changed file experiments/bb3_h6_action_call_probe.py.
- BB3 Lua fixture constants fix: commit d99f57ba98e5b2fc598299ceb69bf1ecc7a2f4c6, changed file experiments/bb3_h6_action_call_probe.py.
- BB3 run 41542947152 (source 59998bf...): H6 smoke PASS; BB3 setup failed before dispatch due missing Lua TILE_INDEX/TILE_STRIDE declarations; not a game failure.
- BB3 current run 41543294021 (source d99f57ba98e5b2fc598299ceb69bf1ecc7a2f4c6): status pending/in progress at last check; transaction result not yet known.

Batas tetap: H6 adalah fixture HIBRIDA, bukan target Story Mode murni. Adaptive-player automation tetap dijeda. Tidak ada perubahan ke Tile Duel atau repositori lain. Tidak ada ROM/ISO, BIOS, savestate, Memory Card, raw RAM, screenshot/video atau binary yang diunggah.
