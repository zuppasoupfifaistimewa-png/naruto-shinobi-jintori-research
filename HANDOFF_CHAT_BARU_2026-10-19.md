## Hasil terbaru menggantikan status eksperimen sebelumnya — run #39178662131 (2026-10-19)

Run [#39178662131](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39178662131) **sudah selesai** dengan status success, jadi jangan menjalankan ulang run tersebut. Artifact privat [#12155879252](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39178662131/artifacts/12155879252) telah diunduh dan screenshot dibaca langsung.

**Bukti visual yang baru terverifikasi:**
- Frame 2.670: menu `はじめから` / `ロード`, panah di pilihan pertama.
- DOWN 2.710–2.720: pada frame 2.720 panah berada di `ロード`.
- UP 2.740–2.750: pada frame 2.749/2.750 panah kembali di `はじめから`.
- Circle menu 2.780–2.810: overlay menu menghilang; sesudah beberapa frame gelap/hitam, frame 3.399 langsung memperlihatkan `モードセレクト` dengan `ストーリーモード` tersorot. Layar Mode Select stabil pada checkpoint hingga frame 5.999. Hitam pada frame 2.950–3.199 sendiri tidak dijadikan bukti mode.
- Jadi Start → navigasi DOWN/UP → Circle pada `はじめから` secara visual membawa permainan ke Mode Select. **Story Mode belum dimulai** karena belum ada Circle kedua atau bukti layar gameplay.

Baseline yang wajib dipertahankan: SCPH-7502 (EU); CD ID `SLPS03553`; EXE `SLPS_035.53;1`; PCSX-Redux source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`; SoftGPU; Port 1 Analog/Auto.

Cleanup run terverifikasi: `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`, dan perintah akhir menghapus workspace runtime. Isi ZIP artifact yang diperiksa hanyalah summary/log teks, screenshot PNG pilihan, dan RSP summary; tidak ada ROM, BIOS, save, atau raw GPU/VRAM dump. Artifact berumur tiga hari.

## Rencana langkah berikutnya untuk chat baru

1. Baca bagian hasil terbaru ini, lalu periksa workflow aktif dan dokumen RT-001 sebelum menyunting.
2. Pada cold boot baru ulangi sequence yang telah terbukti: Start press/release 2.650–2.680; DOWN 2.710–2.720; UP 2.740–2.750; Circle pada menu 2.780–2.810.
3. Terus ambil bukti sampai Mode Select terlihat (run ini: frame 3.399 dan stabil hingga 5.999). Karena `ストーリーモード` sudah tersorot pada layar tersebut, rencana Circle kedua pada frame 6.100–6.130, dengan screenshot tepat sebelum/sesudah dan observasi diperpanjang sampai frame 9.000 atau lebih.
4. Klaim Story Mode dimulai hanya jika screenshot setelah Circle kedua menunjukkan transisi nyata ke layar Story Mode/gameplay; jangan membuat inferensi dari frame hitam, `PAD_INJECT PASS`, atau status workflow.
5. Pertahankan SCPH-7502, SLPS03553 / `SLPS_035.53;1`, PCSX-Redux pin, SoftGPU dan Port 1 Analog/Auto. Jangan sentuh Tile Duel. Jangan commit/upload ROM, BIOS, save, raw GPU/VRAM dump atau file privat; cek cleanup sampai akhir.
6. **Jangan membuat run duplikat** untuk #39178662131; run tersebut sudah selesai. Langkah berikutnya adalah eksperimen baru dengan sequence lengkap di atas.

---

# HANDOFF CHAT BARU — Naruto PS1 (2026-10-19)

Dokumen ini dibuat sebagai handoff terbaru. Baca dokumen ini terlebih dahulu saat melanjutkan riset. Instruksi pengguna di sini **menggantikan** instruksi lebih lama yang meminta Start saja dan melarang Circle.

## Instruksi pengguna paling baru

Jika Start sudah membuka menu utama Naruto, gunakan **panah arah (D-pad)** untuk memilih opsi, lalu tekan **Circle/O** untuk menjalankan opsi yang dipilih. Lakukan eksperimen selanjutnya di chat baru, bukan di chat sebelumnya. Jangan berhenti pada menu utama hanya karena instruksi lama menyebut jangan menekan Circle.

Target berikutnya: pilih `はじめから` (“Mulai dari awal”), pastikan layar berikutnya melalui screenshot nyata, lalu lanjut ke Mode Select dan Story Mode setelah setiap layar diidentifikasi.

## Baseline status yang telah dibuktikan

Repositori yang boleh dikerjakan hanya `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`.
Dokumentasi utama: `STATUS.md`, `HANDOFF_LANJUT.md`, `ANALYSIS_LOG.md`, dan `docs/RUNTIME_TEST_PLAN.md`. Workflow aktif untuk uji boot: `.github/workflows/naruto-scph7502-gpu-traffic-summary.yml`.

Konfigurasi runtime yang dipertahankan:
- Game disc ID `SLPS03553`; executable `SLPS_035.53;1`.
- Retail PlayStation BIOS SCPH-7502 (EU).
- PCSX-Redux source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`.
- SoftGPU; Port 1 controller Analog / Auto.
- ROM, BIOS, save, raw GPU/VRAM dump, serta file privat tidak boleh di-commit atau masuk artifact. Artifact hanya perlu ringkasan dan screenshot bukti minimum; hapus aset sementara sebelum upload.

## Hasil run relevan

### Run #39145309203 — menu terbuka (bukti utama)
https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39145309203
Artifact privat #12143433923. Start ditekan di VSync/frame 2650 dan dilepas 2680. Frame 2670 menunjukkan menu dengan panah pada `はじめから` dan opsi kedua `ロード`; menu tetap terlihat sampai frame 2999. Run ini **tidak** mengirim Circle.

### Run #39149443247 — Start lalu Circle, hasil belum tuntas
https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39149443247
Urutan Start 2650–2680 lalu Circle 2750–2780 dalam boot yang sama. Menu menghilang/fade; frame 2900–2999 hitam seragam. Tidak ada tulisan `モードセレクト` yang berhasil dibaca. Jangan simpulkan Mode Select/Story Mode dari layar hitam, tetapi catat bahwa Circle mungkin memicu transisi atau loading yang memerlukan observasi lebih panjang.

### Run #39176328030 — menu tetap stabil dengan Start saja (paling baru)
https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39176328030
Artifact #12155370415 (retensi tiga hari). Frame 2650 menampilkan judul Naruto dan prompt Start; frame 2670 menampilkan menu; frame 2999 tetap menampilkan menu. Input hanya Start press 2650/release 2680. Tidak ada Circle atau tombol arah di run ini. Run selesai pada level workflow, dan visualnya membuktikan Start membuka menu serta menu tetap stabil bila tidak dikonfirmasi.

### Dokumentasi dan workflow saat ini
- HEAD `main` terakhir yang diketahui: `c83fe4ef86992c762533c0712dc2755764ee5b75`.
- Commit tersebut memperbarui `STATUS.md`, `HANDOFF_LANJUT.md`, `ANALYSIS_LOG.md`, dan `docs/RUNTIME_TEST_PLAN.md` untuk merekam hasil Start-only.
- Workflow saat ini masih berisi **Start saja**: press pada frame 2650, release pada frame 2680. Perlu ubah input sequence untuk eksperimen lanjutan di chat baru dan cek file workflow sebelum menyunting.

## Rencana uji berikutnya

1. Periksa file workflow aktual, log terakhir, artifact #12155370415 bila masih ada, dan catatan status. Jangan menjalankan duplikat run lama atau mengandalkan ringkasan tanpa memeriksa file aktual.
2. Setiap GitHub Actions run melakukan **cold boot baru**; jadi skrip harus mengulangi urutan penuh dalam satu boot yang sama: tunggu prompt judul → Start → tunggu hingga menu muncul → gunakan D-pad untuk menavigasi/menegaskan pilihan `はじめから` → Circle/O untuk konfirmasi.
3. Menu yang terlihat saat ini sudah menaruh panah di `はじめから`. Untuk menunjukkan navigasi secara eksplisit tanpa meninggalkan pilihan yang dimaksud, pertimbangkan tap Down lalu Up (dengan press/release terpisah), kemudian Circle; pastikan frame waktunya setelah menu terbuka. Ambil checkpoint sebelum dan sesudah tiap input. Jangan mengirim input menu saat title prompt masih tampil.
4. Observasi melebihi frame 3000 bila perlu, karena eksperimen Start+Circle sebelumnya hanya melihat layar hitam sampai frame 2999. Tangkap checkpoint setelah 3000 (mis. 3300, 3600, 4200, 4800, hingga 6000 bila batas runner memungkinkan) agar transisi/loading dapat dibedakan dari hasil yang belum diketahui. Simpan hanya screenshot minimum yang dibutuhkan.
5. Jika layar baru muncul, baca tulisan/opsi Jepang yang benar-benar ada. Jangan menganggap layar hitam berarti Mode Select. Setelah layar teridentifikasi, baru rancang input berikutnya untuk memilih Story Mode; terus kumpulkan bukti visual, input sequence dan log.
6. Status `PAD_INJECT ... PASS` hanya membuktikan API emulator membaca balik nilai input; respons game harus dibuktikan melalui perubahan visual atau state gameplay yang terukur. Workflow `success` juga bukan bukti gameplay sukses.
7. Jangan menjalankan Story Mode secara spekulatif dengan input beruntun. Lanjutkan selangkah demi selangkah: menu → pilihan mulai dari awal → bukti layar tujuan → Mode Select → Story Mode → kontrol gameplay → progres/tamat.

## Status tujuan RT-001 saat handoff

- Boot game hingga logo DIMPS/title Naruto: **terbukti**.
- Tekan Start dari layar judul untuk membuka menu: **terbukti secara visual**.
- Pilih `はじめから` dengan navigasi arah + Circle: **belum terbukti**.
- Mode Select: **belum terbukti**.
- Story Mode benar-benar dimulai: **belum terbukti**.
- Respons kontrol saat gameplay, pengujian mekanik, dan tamat Story Mode: **belum terbukti**.

Instruksi pengguna terbaru (berlaku mulai handoff ini): gunakan panah arah untuk memilih opsi dan Circle untuk menjalankannya setelah menu dibuka. Instruksi lama “jangan tekan Circle” sudah tidak berlaku untuk eksperimen lanjutan ini.
