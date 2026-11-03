# BB3 — penutupan uji runtime blok transaksi action byte 3/8

Tanggal: 3 November 2026
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

## Putusan

**TUNTAS TERBATAS — K5 pada cakupan uji runtime blok dispatch/transaksi.**

GitHub Actions run 41550406414 menyelesaikan seluruh 16 uji terisolasi:
- Action byte: 3 dan 8.
- Nibble tile+0x20 bits 8–11 sebelum transaksi: 0, 1, 2, 3.
- Dua peluncuran emulator independen untuk tiap kombinasi.
- Hasil: **16/16 PASS**, VALIDATION_ERRORS=0, FIRST_FAILURE_DIAGNOSTIC=NONE.
- Semua pemeriksaan Memory Card disposable: SHA-256 sebelum/sesudah sama.
- Script exit code: **0**.
- Workflow: **SUCCESS**; job bb3-h6-action-call-probe-release, job ID **125636294382**.
- Source SHA: 57ee8f4cba1ff2b15b1a9674d8dfbeb63fcfbf5e.

Ringkasan Actions yang dikomit:
- Status: K5_TERBATAS
- Run ID: 41550406414
- Job ID: 125636294382
- Source SHA: 57ee8f4cba1ff2b15b1a9674d8dfbeb63fcfbf5e
- Exit code: 0

Raw run summary (commit penerbitan b4f5fddfa402f05cb6a5a4c48e17b251817198eb):
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/b4f5fddfa402f05cb6a5a4c48e17b251817198eb/reports/stage1_economy/bb3-h6-action-call-probe-run-41550406414/attempt-1/ACTIONS_RUN_SUMMARY.txt

Data hasil lengkap:
- reports/stage1_economy/bb3-h6-action-call-probe-run-41550406414/attempt-1/BB3_ACTION_CALL_RESULTS.tsv
- reports/stage1_economy/bb3-h6-action-call-probe-run-41550406414/attempt-1/BB3_ACTION_CALL_SUMMARY.txt

## Metode dan batas uji

Uji ini bukan permainan dengan input kontrol. Probe memuat checkpoint H6 hibrida dengan SHA-256:

d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475

Lalu menjalankan blok dispatch secara langsung dengan register/frame CPU yang disiapkan. Frame 0x30-byte disusun sesuai prolog FUN_800D15A8; PC diarahkan ke dispatch block 0x800D4464; byte aksi diperiksa di 0x800D4470. Breakpoint selector memaksa index tile 4 dan memverifikasi nilai balik register. Ini menguji isi blok transaksi MIPS, bukan apakah pengguna dapat mencapai opsi tersebut melalui menu atau alur Story Mode.

Semua penulisan RAM berlangsung sementara pada emulator disposable. ROM/BIOS/savestate/Memory Card/RAM mentah tidak dipublikasikan. Hanya nilai scalar, hasil TSV, dan hash kartu disposable yang dicatat.

## Perilaku runtime terukur

Kondisi tile terpilih pada semua 16 peluncuran:
- Tile index: **4**.
- tile+0x1A fee: **100**.
- Participant index: **0**.
- Saldo participant sebelum dan sesudah blok: **1500 → 1500**.
- Pending delta manager+0x2EE: **0 → −100** (delta **−100**).
- Refresh FUN_800BB004: tercapai.
- Refresh FUN_800BE464: tercapai.
- Kartu disposable: tidak berubah, SHA-256 fa43239bcee7b97ca62f007cc68487560a39e19f74f3dde7486db3f98df8e471.

Saldo participant tetap 1500 selama blok ini karena transaksi menulis pending delta −fee pada manager; uji ini tidak mengklaim bahwa saldo final sudah dikomit oleh tahap pemrosesan selanjutnya.

### Hasil level untuk masing-masing action byte 3 dan 8

| Action byte | Level awal bits 8–11 | tile+0x20 sebelum | tile+0x20 sesudah | Bits 8–11 | Bits 4–7 | Pengulangan |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 0 | 0xF020 | 0xF130 | 0 → 1 | 2 → 3 | 2/2 PASS |
| 3 | 1 | 0xF120 | 0xF230 | 1 → 2 | 2 → 3 | 2/2 PASS |
| 3 | 2 | 0xF220 | 0xF330 | 2 → 3 | 2 → 3 | 2/2 PASS |
| 3 | 3 | 0xF320 | 0xF430 | 3 → 4 | 2 → 3 | 2/2 PASS |
| 8 | 0 | 0xF020 | 0xF130 | 0 → 1 | 2 → 3 | 2/2 PASS |
| 8 | 1 | 0xF120 | 0xF230 | 1 → 2 | 2 → 3 | 2/2 PASS |
| 8 | 2 | 0xF220 | 0xF330 | 2 → 3 | 2 → 3 | 2/2 PASS |
| 8 | 3 | 0xF320 | 0xF430 | 3 → 4 | 2 → 3 | 2/2 PASS |

Dengan demikian, pada kondisi yang diuji, kedua action byte berbagi perilaku transaksi: fee dibaca dari u16(tile+0x1A), pending delta diisi −fee, nibble level bits 8–11 dan bits 4–7 masing-masing naik satu, kemudian kedua helper refresh dijalankan.

## Kesimpulan per BB

- BB1 — TUNTAS K4 statis: dua direct store +0x0B pada tile record telah dipisahkan dari empat writer objek selector; perilaku rantai tile type 5 ditemukan, label gameplay exact tetap TIDAK TAHU.
- BB2 — TUNTAS K4 statis: jalur fee, guard saldo, pending debit, dua level nibble, dan refresh helper telah dipetakan.
- BB3 — TUNTAS TERBATAS K5: blok transaksi diuji dalam 16 peluncuran independen yang konsisten, dua pengulangan per kondisi, semua PASS.

## Batas yang belum diselesaikan oleh BB3

1. Fixture H6 adalah HIBRIDA, bukan checkpoint Story Mode murni.
2. Probe memaksa masuk ke blok dispatch dan memilih tile index 4; tidak ada input controller atau demonstrasi gameplay normal.
3. Nama aksi visual/gameplay yang direpresentasikan byte 3 atau 8 tetap TIDAK TAHU. Jangan menyatakan keduanya pasti Barrier placement.
4. Rumus positif floor(sum(nilai 3 petak milik pemain)/2)+400 tidak dijalankan dalam BB3; rumus itu merupakan kontrol terpisah.
5. Uji ini mengamati pending debit pada manager, bukan tahap lanjutan yang menerapkan pending delta ke saldo final participant.

Dengan batas itu, BB3 ditutup untuk sasaran yang didefinisikan: konfirmasi runtime blok transaksi action byte 3/8. Pekerjaan identifikasi semantik gameplay dan verifikasi alur input Story Mode tetap merupakan pekerjaan lanjutan, bukan kegagalan BB3 pada cakupan ini.
