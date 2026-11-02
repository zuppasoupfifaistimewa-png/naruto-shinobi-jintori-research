# Status BB0–BB3 — audit logika Barrier/Chakra
Tanggal: 2 November 2026
Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)

## Catatan penomoran

Pada branch `main` tidak ditemukan dokumen definisi/acceptance criteria bernama BB0, BB1, atau BB2. Karena itu, tabel di bawah adalah pengelompokan bukti Barrier/Chakra yang memang tersedia di repo, bukan klaim bahwa definisi tahap BB yang mungkin berada di percakapan lain sudah berhasil direkonsiliasi.

## Status

| Tahap | Status | Batas |
|---|---|---|
| BB0 — observasi barrier placement dan debit Chakra | SELESAI untuk satu jalur Story Mode | Satu transaksi teramati; tidak universal. |
| BB1 — sumber data biaya dan pemetaan record petak | SELESAI untuk resource 630 pada H6 | Mapping source/runtime valid; tidak membuktikan seluruh resource/board. |
| BB2 — dekompilasi debit transaksi dan kenaikan level | SELESAI statis K4 untuk action byte 3/8 | Nama gameplay action dan kaitannya secara khusus dengan barrier tetap TIDAK TAHU. |
| BB3 — validasi runtime pembacaan/mutasi transaksi | BELUM | Restore H6 ke PCSX-Redux crash; belum ada hit dispatch atau pembacaan RAM pasca-load. |

## BB0 — barrier placement yang benar-benar teramati

Run 39617444912 menggunakan prompt kontekstual:
- `ここに結界をはりますか？` (Apakah akan memasang penghalang di sini?)
- `必要チャクラ 120` (Chakra yang dibutuhkan: 120)
- Pilihan `はい` (Ya) terlihat tersorot.
- Setelah satu Circle confirm yang sesuai konteks, barrier/orb biru terlihat; HUD Naruto berubah 1500 → 1380, sementara Mizuki tetap 1500.
- Bukti screenshot yang dicatat dalam `docs/SIGSEGV_FORENSICS_2026-10-21.md` memperlihatkan kondisi hasil pada f60, f100, dan f120.

Kesimpulan terbatas: placement pada path tersebut mengurangi Chakra Naruto sebesar 120. Ini tidak membuktikan biaya untuk tile lain, level lain, atau semua tipe barrier.

## BB1 — source data petak

Artefak:
- `reports/stage1_economy/BA_FINAL_REPORT_2026-11-02.md`
- `reports/stage1_economy/BA1_STAGE1_RESOURCE_630_RECORDS.tsv`
- `reports/stage1_economy/BA2_TILE_RUNTIME_FIELD_MAP.tsv`
- `reports/stage1_economy/BA3_TILE_FIELD_VALIDATION.tsv`

Temuan:
- Selector pada empat snapshot H6 memilih resource ID 630.
- Resource 630 berisi 22 record dengan source stride 0x1E; runtime tile stride 0x124.
- 18 field salinan: 1.584/1.584 cocok; dua field initializer: 176/176 cocok; total 1.760/1.760 cocok pada empat snapshot H6.
- Source bytes +0x13..+0x14 disalin sebagai halfword little-endian ke runtime tile+0x1A.
- Source bytes +0x15..+0x16 → tile+0x1C; +0x17..+0x18 → tile+0x1E.
- Untuk resource 630, nilai tile+0x1A per index 0–21 adalah:
  `0, 50, 50, 50, 100, 0, 100, 120, 100, 100, 100, 0, 150, 150, 200, 150, 150, 0, 0, 100, 100, 50`.

Penting: nilai tile+0x1A di atas adalah nominal field resource yang dibaca handler action 3/8. Belum terbukti bahwa seluruh angka tersebut adalah biaya pemasangan Barrier; jangan menyamakan angka prompt 120 pada BB0 dengan semua isi field ini.

## BB2 — jalur statis debit action 3/8

Laporan sumber: `reports/stage1_economy/AZ0_AZ3_FINAL_STATUS_2026-11-02.md`.

Rantai yang ditemukan pada `FUN_800D15A8`:
1. Membaca action byte pada participant manager +0x2EB; cabang yang dianalisis adalah nilai 3 atau 8.
2. Memilih index petak melalui `FUN_800BBD9C()`.
3. Membaca `fee = u16(tile+0x1A)`.
4. Memeriksa bahwa fee tidak melebihi saldo kerja participant +0x04.
5. Jika cukup, menulis pending delta participant +0x2EE = `-fee`.
6. Menaikkan nibble tile+0x20 bits 8–11 dan bits 4–7 masing-masing satu.
7. Memanggil `FUN_800BB004` dan `FUN_800BE464` untuk pembaruan representasi/atribut petak.
8. `FUN_800BE5D8` memproses pending signed delta, menyinkronkan saldo lewat setter `0x8001387C` dan getter `0x800138EC`, lalu membersihkan pending slot.

Kesimpulan: jalur biaya action 3/8 secara statis K4. Nama gameplay action 3 vs 8 dan hubungan langsungnya dengan barrier placement yang terlihat di BB0 belum teridentifikasi. Rumus positif `tile+0x1E + level × tile+0x1C` adalah cabang terpisah; label gameplay-nya tetap TIDAK TAHU.

### BB2 — pemetaan PC instruksi yang dapat dipakai untuk verifikasi BB3

Pemeriksaan ulang dekompilasi dan raw MIPS untuk `FUN_800D15A8` (Entry 1, ukuran body 17.944 byte) mengonfirmasi bahwa label `case 3` dan `case 8` berada dalam satu blok transaksi pada `LAB_800D4468`. Jadi kedua nilai action-byte itu memang target uji yang benar; kesimpulan tersebut tidak berasal dari menafsirkan nilai jenis petak.

Urutan instruksi raw yang terkait:

| PC | Instruksi/makna |
|---|---|
| `0x800D4468` | Memuat pointer manager; blok `switch(action byte +0x2EB)` dimulai pada label ini. |
| `0x800D4470` | Membaca action byte `manager+0x2EB`; jump table membedakan action. |
| `0x800D45D0` | Memanggil `FUN_800BBD9C()` untuk memilih petak. |
| `0x800D45E0` | Menyimpan indeks terpilih ke `manager+0x4A0`. |
| `0x800D4628` | Membaca `u16(tile+0x1A)` sebagai fee. |
| `0x800D462C`–`0x800D4638` | Membaca saldo kerja `participant+0x04`, membandingkan fee dengan saldo, dan menuju jalur gagal bila saldo kurang. |
| `0x800D46EC`–`0x800D46F8` | Membaca fee, menegasikan nominalnya, lalu menyimpan signed delta ke `participant_manager+0x2EE`. |
| `0x800D4724`–`0x800D4764` | Menghapus dan menulis ulang nibble bits 8–11 dengan level lama +1. |
| `0x800D47F4`–`0x800D4834` | Menghapus dan menulis ulang nibble bits 4–7 dengan level lama +1. |
| `0x800D4840`, `0x800D4848` | Memanggil `FUN_800BB004` dan `FUN_800BE464` sesudah mutasi level. |

Ini memperkuat BB2 sebagai K4 statis. Probe BB3 saat ini memasang breakpoint pada dispatch `0x800D4468`, sesudah return selector `0x800D45D8`, dan sebelum refresh tile `0x800D4838`; ketiga lokasi tersebut berada di dalam blok yang telah dicocokkan dengan instruksi di atas.

Catatan semantik: nama gameplay untuk action byte 3 dan 8 masih **TIDAK TAHU**. Keduanya hanya terbukti masuk ke satu blok transaksi yang sama pada fungsi ini.

### Fixture uji BB3 yang disiapkan

Probe fungsi sementara memakai index petak 4 pada snapshot H6 yang telah dipetakan ke resource 630. Nilai `tile[4]+0x1A` pada record resource 630 adalah **100**. Probe menguji action byte 3 dan 8 untuk nibble level bits 8–11 bernilai 0, 1, 2, dan 3, masing-masing dua peluncuran independen. Selama uji, tidak ada tombol gameplay; RAM hanya diubah dalam proses emulator disposable, dan Memory Card kerja harus tetap sama.

Hasil yang diharapkan dari jalur statis bila cabang berhasil: pending delta pemain aktif `-100`; nibble bits 8–11 bertambah satu; nibble bits 4–7 bertambah satu; tile refresh dipanggil pada PC `0x800D4840` dan `0x800D4848`. Ini adalah ekspektasi uji yang diturunkan dari instruksi, bukan hasil runtime yang sudah teramati. Probe belum menjalankan positive control; hasil untuk kontrol tersebut tetap **TIDAK DIUJI**.

## BB3 — hasil uji runtime dan blocker

### Restore H6 dan pembacaan RAM — terkonfirmasi pada dua smoke launch

Run `41527796204`:
- Source SHA: `25d2436e30ac02cbb751c3463acabbfab0841ce2` (Actions source commit tercatat penuh pada ringkasan run).
- Job `125559902986`; script exit 0; wall 2.135 detik.
- `SaveStateLoaded=PASS`, pemanggilan load kembali, pembacaan memory-file PASS.
- Tile array `0x8013B818`, jumlah petak 22; manager `0x801EFBB8`.
- Kartu sementara nol 128 KiB identik sebelum/sesudah; RAM writes NONE; gameplay input NONE.

Run `41528938163`:
- Source SHA: `4370d13dfa4c9f1aeaaf5ebb36cd3ce93ba8ea0d`.
- Job `125563840401`; script exit 0; wall 2.416 detik.
- H6 load event PASS dan memory-file read PASS; tile array/count/manager konsisten dengan smoke pertama.
- Kartu sementara identik; RAM writes NONE; gameplay input NONE.

Ringkasan kedua run berada pada:
- `reports/stage1_economy/bb3-h6-smoke-run-41527796204/attempt-1/`
- `reports/stage1_economy/bb3-h6-smoke-run-41528938163/attempt-1/`

Makna bukti: **pemulihan H6 dan akses baca RAM sekarang terbukti berfungsi pada dua peluncuran independen**. Bukti ini sendiri belum menguji action byte 3/8.

### Uji function-call 16 kasus — BELUM memperoleh hasil akhir

Fixture uji:
- Petak index 4, resource 630, fee field `tile+0x1A=100`.
- Action byte 3 dan 8 × nibble level bits 8–11 = 0,1,2,3 × dua attempt independen.
- Pengaturan RAM dilakukan hanya pada proses emulator disposable. Tidak ada tombol gameplay ditekan. Kartu yang digunakan adalah file nol sementara 128 KiB, bukan Memory Card pengguna.

Kriteria lulus yang dipasang pada probe terbaru:
1. 16 baris hasil, seluruh pasangan action/level tercakup dua kali.
2. Breakpoint dispatch tercapai dan action byte saat dispatch tepat sesuai input.
3. Selector mengembalikan index 4 dan nilai tersebut tersimpan di manager+0x4A0.
4. Fee 100; pending sebelum 0, sesudah −100, delta −100.
5. Nibble bits 8–11 dimulai dari level fixture yang diminta dan naik satu; nibble bits 4–7 juga naik satu.
6. Kedua refresh helper `0x800D4840` dan `0x800D4848` benar-benar tercapai.
7. Wrapper exit 0, kartu sementara tidak berubah, dua attempt pada setiap kasus.

Run `41528133484` (source SHA `3e0e33d877945590033a0671d41d4fc33f69a7a7`, job `125561061837`) berhasil melewati H6 smoke di dalam workflow, tetapi langkah 16 peluncuran masih berstatus berjalan saat laporan ini diperbarui. Belum ada hasil/TSV yang dapat dipakai untuk menyimpulkan transaksi.

Run lama `41527261817` dan `41527576341` tidak boleh dianggap lulus: keduanya terhambat library/runtime loader. Run `41527251225` pada workflow lama juga masih terhenti di build lama dan bukan sumber valid untuk transaksi.

Run terbaru `41529469001` (source SHA `227ee88f06d6618c8f4e0726407f70b4e2e75e05`, job `125565631539`) menggunakan workflow concurrency group v4 dan timeout/watchdog 360. Run telah menyelesaikan ekstraksi dan verifikasi PCSX rilis, validasi input, serta smoke-test H6; langkah 11/14 `Run 16 isolated H6 function-call launches` masih berjalan. Belum ada TSV hasil akhir yang dapat dipakai untuk menyimpulkan transaksi.

Kontrol positif rumus 3 petak tetap **TIDAK DIUJI**. Probe ini juga belum menguji commit saldo kanonik melalui `FUN_800BE5D8`; ia mengamati pending delta dan perubahan field level pada cabang transaksi.

Keputusan: **BB3 BELUM TUNTAS** sampai hasil 16 kasus lulus sesuai kriteria. Tidak ada dasar untuk menyebut nama gameplay action-byte 3/8 atau menyamakannya dengan aksi pemasangan Barrier pada BB0.

## Kesimpulan akhir

BB0, BB1, dan BB2 selesai hanya dalam batas eksplisit di atas. BB3 belum selesai. Karena nama/criteria BB0–BB2 tidak tercatat di repo, kesesuaian pengelompokan ini terhadap checklist BB asli tidak dapat dipastikan (**TIDAK TAHU**). Tidak ada dasar untuk menyatakan seluruh BB0–BB3 telah selesai.

Tidak ada ROM/ISO, BIOS, savestate, Memory Card, raw RAM, screenshot, video, atau binary yang dikomit dalam laporan ini.


---

## Addendum pemeriksaan lanjutan — 3 November 2026

Pembaruan ini mempertahankan putusan batas bukti di atas; tidak mengubah hasil lama menjadi klaim runtime baru.

### BB2 — pemeriksaan ulang akses action byte

Run static census `41533205025`:
- Job: `analyze-entry1-buffer-base`
- Job ID: `125578418688`
- Source SHA: `111bf1a3f4177f356e513d2fdea1de2c50f6e697`
- Status: `SUCCESS`, exit code `0`
- Output utama: `aq1-run-41533205025/attempt-1/bb2-action-byte-access.tsv` dan `bb2-d15a8-function-detail.txt`.

Census displacement `+0x2EB` berisi 131 temuan: 65 instruksi WRITE, 63 READ, dan 1 OTHER. Angka ini adalah hit pencarian displacement, **bukan** 131 akses yang semuanya telah dibuktikan memakai base register participant-manager. Karena sebagian alias base register belum terbukti, jangan gunakan total 65/63 sebagai jumlah final writer/reader field manager.

Bukti BB2 yang tetap K4 berasal dari rantai instruksi langsung pada `FUN_800D15A8`:
- `0x800D4470` membaca action byte `manager+0x2EB`; switch mengarah ke satu blok bersama untuk case 3 dan 8.
- `0x800D45D0` memanggil selector petak; `0x800D45E0` menyimpan index hasil.
- `0x800D4628` membaca fee `u16(tile+0x1A)`; pemeriksaan saldo ada pada `0x800D462C–0x800D4638`.
- `0x800D46EC–0x800D46F8` menulis signed pending delta `-fee` pada manager `+0x2EE).
- `0x800D4724–0x800D4764` menaikkan nibble bits 8–11 satu tingkat.
- `0x800D47F4–0x800D4834` menaikkan nibble bits 4–7 satu tingkat.
- `0x800D4840` dan `0x800D4848` memanggil refresh helper `FUN_800BB004` dan `FUN_800BE464`.

Rantai ini membuat debit action 3/8 dan mutasi dua nibble dapat diperiksa langsung dari raw MIPS/dekompilasi. Makna nama action 3/8 tetap **TIDAK TAHU**; jangan menyamakannya dengan aksi pemasangan Barrier yang diamati di BB0.

### BB3 — pembaruan uji

Dua smoke run:
- `41527796204`, job `125559902986`: H6 load dan read-only memory-file PASS; wall 2.135 s.
- `41528938163`, job `125563840401`: H6 load dan read-only memory-file PASS; wall 2.416 s.
- Keduanya membaca tile array `0x8013B818`, jumlah 22, manager `0x801EFBB8`; Memory Card disposable tidak berubah. Tidak ada RAM write atau gameplay input dalam smoke.

Hasil function-call lama `41459907683`:
- Job `125326000381`, source SHA `c5fb0ff42a90c0530bd20f65b93e74f121f55cc9`, workflow conclusion SUCCESS, tetapi **hasil probe BB3 hanya SEBAGIAN**.
- 16 baris dibuat; PASS 0/16; seluruh 16 berstatus `NO_RESULT`; wrapper exit `-11` (emulator berhenti abnormal); wall masing-masing sekitar 2.55–2.75 s.
- Hash Memory Card disposable sama sebelum/sesudah setiap baris.
- Jadi run workflow SUCCESS tidak berarti pemanggilan fungsi atau transaksi berhasil.

Run function-call `41529469001`:
- Job `125565631539`, source SHA `227ee88f06d6618c8f4e0726407f70b4e2e75e05`.
- Pada pemeriksaan 3 November 2026 sekitar 05:18 WIB, job masih `in_progress` pada langkah 16 peluncuran. Belum ada TSV/ringkasan akhir; transaksi belum dapat dinilai.

Perbaikan diagnosis BB3 telah dikomit pada `4159e1b27018cae970eac64013e25a98c78013ee` (berkas diubah: `experiments/bb3_h6_action_call_probe.py`). Probe berikutnya berhenti setelah kasus pertama yang tidak PASS dan menyimpan cuplikan log emulator sebagai teks terbatas, sehingga kegagalan pertama dapat diperiksa tanpa mengulang seluruh matriks 16 kasus. Workflow run `41536404671`, source SHA `4159e1b27018cae970eac64013e25a98c78013ee`, masih `pending` saat catatan ini dibuat; hasilnya belum tersedia.

### Putusan setelah addendum

- BB0: selesai terbatas untuk satu jalur Story Mode yang benar-benar diamati; biaya 120 Chakra hanya berlaku pada transaksi tersebut.
- BB1: selesai untuk resource 630 pada H6, bukan semua resource/board.
- BB2: selesai statis K4 untuk cabang action-byte 3/8, bukan identifikasi nama aksi.
- BB3: belum tuntas. Smoke H6 berhasil, tetapi tidak ada bukti runtime transaksi debit dan kenaikan level yang lulus.

Karena dokumen acceptance criteria BB0–BB3 asli tidak ditemukan dalam repo, kesesuaian label ini dengan checklist BB di percakapan lain tetap **TIDAK TAHU**. H6 adalah fixture hibrida, bukan Story Mode murni. Tidak ada dasar untuk mengklaim BB0–BB3 seluruhnya selesai.
