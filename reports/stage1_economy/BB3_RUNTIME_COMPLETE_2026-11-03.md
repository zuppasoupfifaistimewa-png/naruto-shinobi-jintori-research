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


---

## Ekspansi matriks 40 launch — hasil akhir run 41556732137

Laporan 16/16 di atas adalah hasil awal. Ekspansi yang diminta ke dua tile dan lima level kini selesai pada run berikut.

<badge>40/40 PASS — K5 terbatas</badge>

| Parameter | Hasil |
|---|---|
| Run | 41556732137 |
| Job | bb3-h6-action-call-probe-release |
| Job ID | 125657970152 |
| Source SHA | 296785adc21e399d8b4882cc75a9fda6c8539045 |
| Workflow | SUCCESS |
| Script exit code | 0 |
| Kasus | 40/40 PASS, 0 gagal, 0 validation errors |
| Timeout | 360 s per launch |
| Launch terlama run ini | 51.642 s |

Matriksnya lengkap dan unik: tile 4/7 × action byte 3/8 × level nibble 8–11 0–4 × dua launch. Setiap gabungan tile/action memiliki 10 baris dan semua status PASS. Tidak ada kombinasi hilang atau duplikat.

### Hasil runtime per tile

| Tile | tile+0x0E | Fee tile+0x1A | Action | Jumlah kasus | Pending delta semua level |
|---:|---:|---:|---:|---:|---:|
| 4 | 120 | 100 | 3 | 10 | -100 |
| 4 | 120 | 100 | 8 | 10 | -100 |
| 7 | 160 | 120 | 3 | 10 | -120 |
| 7 | 160 | 120 | 8 | 10 | -120 |

Untuk setiap baris, action dispatch tercapai dan byte pada dispatch sama dengan byte yang dipoke; tile pilihan sama dengan tile target; fungsi refresh FUN_800BB004 dan FUN_800BE464 tercapai; pending delta adalah negatif fee tile+0x1A; nibble bits8–11 dan bits4–7 masing-masing bertambah satu; wrapper exit code 0. Saldo participant pada snapshot sebelum pending diterapkan tetap 1500, sedangkan pending memuat -100 atau -120. Ini sesuai dengan transaksi pending debit, bukan bukti saldo final setelah fase penerapan pending.

### Pemeriksaan integritas

- RAM pra-poke diambil pada post-load VSync 180; ukuran tepat 2,097,152 byte untuk semua 40 launch.
- SHA-256 RAM frame180 cocok untuk seluruh launch: 5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7.
- Referensi RAM frame360 (4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907) tidak cocok karena snapshot yang dibandingkan adalah frame180; ini bukan kegagalan.
- Memory Card disposable 128 KiB tidak berubah pada seluruh 40 launch. SHA sebelum/sesudah: fa43239bcee7b97ca62f007cc68487560a39e19f74f3dde7486db3f98df8e471.
- H6 fixture SHA-256: d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475 (HIBRIDA).
- Tidak ada RAM dump, savestate, Memory Card, ROM/ISO, BIOS, frame, gambar, video, atau binary yang dipublikasikan. RAM write hanya sementara di proses emulator disposable.

### Putusan BB3

**BB3 TUNTAS K5 untuk cakupan matriks direct function-call action byte 3/8 pada fixture H6 HIBRIDA.** Dua peluncuran independen per kombinasi memberi hasil konsisten pada semua 40 kasus. Ini menutup permintaan BB3 untuk memaksa action 3/8 pada tile yang dipilih dan level 0–4, serta merekam pending fee dan perubahan nibble.

Batas tetap:
- Probe tidak mengirim controller input atau memainkan Story Mode normal; karena itu action 3/8 belum boleh dinamai “bangun Barrier” atau “upgrade Barrier”.
- Ini bukan uji positive-credit byte 1/0x1D dan tidak mengonfirmasi bahwa reward positif adalah Chakra atau Barrier Release.
- Formula pemasukan akhir giliran floor(sum nilai petak milik pemain /2)+400 tidak diuji dalam probe ini.

### Berkas hasil terbaru

- TSV 40 baris: reports/stage1_economy/bb3-h6-action-call-probe-run-41556732137/attempt-1/BB3_ACTION_CALL_RESULTS.tsv
- Ringkasan validasi: reports/stage1_economy/bb3-h6-action-call-probe-run-41556732137/attempt-1/BB3_ACTION_CALL_SUMMARY.txt
- Run summary ringkas yang baru dikomit: reports/stage1_economy/bb3-h6-action-call-probe-run-41556732137/attempt-1/BB3_VERIFIED_SUMMARY.txt
- Actions summary: reports/stage1_economy/bb3-h6-action-call-probe-run-41556732137/attempt-1/ACTIONS_RUN_SUMMARY.txt

Ringkasan Actions menyimpan STATUS, JOB, SOURCE_SHA, dan EXIT_CODE; hasil rinci diverifikasi ulang independen: 40 baris unik, semua PASS, 0 error.
