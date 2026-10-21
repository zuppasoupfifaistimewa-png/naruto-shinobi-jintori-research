# Eksperimen konfirmasi Circle kedua — 21 Oktober 2026

## Tujuan

Membandingkan dua cabang dari checkpoint induk yang sama: (A) Circle awal lalu menunggu tanpa input kedua; (B) Circle awal lalu Circle kedua pada prompt `けってい`. Tujuan akhirnya ialah mengamati apakah cabang B benar-benar bergerak ke tahap Story Mode berikutnya, serta menyimpan dan memvalidasi checkpoint privat baru bila state lanjutan berhasil dicapai.

## Batasan dan baseline

- Checkpoint induk tidak boleh ditimpa: 21.162.405 byte, SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`.
- AppImage patched yang dipakai ulang memiliki SHA-256 `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`.
- Sebelum eksperimen ini, run [#39526690265](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39526690265) lulus pada 08:21 WIB. Frame 180 dari cabang Circle menampilkan panel `任務内容`, target `3000チャクラためる`, dan prompt `けってい`. Panel itu menjadi baseline untuk menentukan waktu input kedua.
- ROM, BIOS, checkpoint/savestate, dan Memory Card tidak disimpan ke Git. Data runtime tetap privat dan hanya berada pada runner/artefak Actions privat.

## Run #39527646447 — gagal sebelum konfirmasi kedua

Run: [#39527646447](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39527646447)  
Mulai 08:29:49 WIB; selesai 08:35:20 WIB pada 21 Oktober 2026. Status akhir: `failure`.

### Observasi dari log

- Prasyarat runtime lulus: unduhan emulator, checkpoint induk, Memory Card privat, dan validasi hash. Kedua proses mencatat `CIRCLE_TIMELINE_LOAD_EVENT=PASS` dan `CIRCLE_TIMELINE_LOAD_RETURNED=1`.
- Kedua cabang merekam pembacaan input yang sesuai untuk tap Circle pertama pada frame 30 dan pelepasan frame 38 (`status=PASS`).
- Cabang `CIRCLE_WAIT` merekam screenshot sampai frame 181. Proses tidak menghasilkan VSync/screenshot tambahan dan berakhir karena batas timeout 240 detik (`code=124`).
- Cabang `CIRCLE_SECOND` mengalami native segmentation fault (`code=139`) setelah screenshot frame 175. Versi workflow ini menjadwalkan Circle kedua untuk frame 185; karena proses crash sebelum frame 180, tombol kedua **tidak pernah dikirim**.
- Akibatnya, run ini tidak membuktikan apakah prompt dikonfirmasi atau Story Mode maju. Tidak ada checkpoint lanjutan yang dibuat, dan pengujian pemulihan dalam proses emulator baru tidak dijalankan.
- Artefak privat #12314525232, `naruto-storymode-circle-followup-private`, 11.542 byte, digest ZIP `sha256:92fc55004d23241c80cf6a7c76fcf24a5291747207fd2a2854723f3ed7477ca4`. Artefak tersebut berisi log/stdout dan metadata screenshot, tetapi tidak menyertakan berkas piksel mentah; penanganan gagal sebelum konversi screenshot dijalankan. Ini kekurangan harness, bukan bukti tentang makna tombol dalam game.

## Run #39528879636 — input di frame 180 terkirim, tetapi game berhenti memajukan frame

Run: [#39528879636](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39528879636)  
Mulai 08:42:32 WIB; selesai 08:44:41 WIB pada 21 Oktober 2026. Status workflow: `failure`.

- Cabang `CIRCLE_WAIT` selesai normal di frame 181. Log menunjukkan checkpoint dimuat, event/load-return PASS, tap Circle awal di frame 30 dan release di 38 terdeteksi; screenshot ditangkap pada frame 1–181 yang dipilih.
- Cabang `CIRCLE_SECOND` juga memuat checkpoint dan mendeteksi tap Circle awal. Screenshot frame 175 memperlihatkan panel misi serta prompt `けってい`; panel yang sama sudah jelas pada frame 180.
- Setelah screenshot f180, skrip mengirim Circle kedua dan pembacaan pad mencatat `readback=true status=PASS`. Frame 181 masih identik secara piksel dengan cabang tunggu (`mad=0.000, exact=1.00000`). Cabang konfirmasi kemudian tidak menghasilkan frame 182 atau lebih jauh dan keluar dengan timeout 45 detik (`code=124`). Ini tidak membuktikan tombol kedua tidak bekerja; efek gameplay setelah input tetap tidak diketahui karena tidak ada frame lanjutan.
- Karena frame 240 tidak tercapai, checkpoint baru tidak dibuat dan pemulihan dalam proses emulator baru tidak dijalankan. Checkpoint induk tidak berubah.
- Artefak privat #12314526644 berisi 103 file, 4.105.985 byte, digest ZIP `sha256:dfbb9526dc4d14d81d46ed3c0acf676b299ea179aba47f17e8e6eef7dec66f05`, termasuk screenshot PNG, raw RGB dan log. Artefak bersifat privat dan tidak dimasukkan ke Git.

## Eksperimen ulang #39529241370

Run [#39529241370](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39529241370) dimulai pukul 08:46:27 WIB. Pada pemeriksaan 08:46:31 WIB, status `in_progress`, runner sedang menginisialisasi container.

Perubahan eksperimen yang baru:
- Screenshot frame 175 diambil terlebih dahulu (frame ini secara visual sudah memperlihatkan prompt), lalu Circle kedua dikirim pada callback frame 175; release dijadwalkan pada frame 183.
- Screenshot tambahan frame 176–178 disiapkan agar respons langsung setelah input dapat diperiksa.
- Batas 45 detik per proses tetap dipertahankan. Artefak menyimpan screenshot PNG, data mentah, log, dan laporan privat meskipun cabang gagal.
- Checkpoint baru hanya akan dibuat bila cabang konfirmasi mencapai frame 240; jika dibuat, workflow mengujinya dalam proses emulator baru.

Hasil #39529241370 perlu ditambahkan setelah run dan artefaknya diverifikasi.

## Klasifikasi kesimpulan saat ini

- **Terverifikasi:** checkpoint induk berhasil dimuat oleh emulator untuk kedua cabang pada run #39527646447; input Circle pertama diterima oleh API pad; cabang tunggu memiliki capture sampai frame 181; cabang kedua crash sebelum input kedua.
- **Hipotesis:** UI/gameplay dapat berhenti memajukan VSync pada panel konfirmasi atau emulator mengalami jalur crash yang dipicu saat melanjutkan cabang tersebut. Data saat ini belum membedakan penyebabnya.
- **Belum terverifikasi:** efek Circle kedua pada prompt `けってい`; apakah permainan maju ke tahap Story Mode berikutnya; apakah checkpoint setelah konfirmasi dapat dipulihkan; syarat/aturan gameplay lebih jauh; tamat Story Mode.

Jangan menganggap panel atau teks target sebagai bukti bahwa target Chakra telah tercapai. Jangan menyatakan Story Mode tamat tanpa bukti runtime yang kuat.
