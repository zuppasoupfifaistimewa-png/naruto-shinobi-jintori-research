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

## Perbaikan pada eksperimen ulang #39528879636

Run berikutnya mulai 08:42:32 WIB. Pada pemeriksaan awal, statusnya `in_progress` dan runner sedang menginisialisasi container.

Perbaikan metodologi yang diunggah sebelum run itu:
- Cabang tunggu berhenti di frame 181 agar tidak menunggu tanpa batas setelah VSync tampak berhenti.
- Pada cabang konfirmasi, screenshot frame 180 diambil lebih dahulu, lalu Circle kedua dikirim pada callback frame 180; pelepasan dijadwalkan pada frame 188.
- Proses dibatasi 45 detik per cabang.
- Jika proses crash/timeout atau checkpoint tidak terbentuk, langkah laporan tetap berlanjut agar screenshot yang sempat diambil dapat dikonversi dan log/report dapat diunggah. Berkas screenshot mentah kini ikut ke artefak privat untuk memungkinkan pemulihan.
- Jika cabang konfirmasi mencapai frame 240 dan membuat checkpoint, workflow menyalin checkpoint itu (tanpa mengubah checkpoint induk), lalu mengujinya dari proses emulator baru. Jika frame 240 tidak tercapai, status pemulihan wajib dicatat sebagai tidak dijalankan karena checkpoint tidak tersedia.

Hasil akhir run #39528879636 harus ditambahkan ke dokumen ini setelah status dan artefaknya diverifikasi.

## Klasifikasi kesimpulan saat ini

- **Terverifikasi:** checkpoint induk berhasil dimuat oleh emulator untuk kedua cabang pada run #39527646447; input Circle pertama diterima oleh API pad; cabang tunggu memiliki capture sampai frame 181; cabang kedua crash sebelum input kedua.
- **Hipotesis:** UI/gameplay dapat berhenti memajukan VSync pada panel konfirmasi atau emulator mengalami jalur crash yang dipicu saat melanjutkan cabang tersebut. Data saat ini belum membedakan penyebabnya.
- **Belum terverifikasi:** efek Circle kedua pada prompt `けってい`; apakah permainan maju ke tahap Story Mode berikutnya; apakah checkpoint setelah konfirmasi dapat dipulihkan; syarat/aturan gameplay lebih jauh; tamat Story Mode.

Jangan menganggap panel atau teks target sebagai bukti bahwa target Chakra telah tercapai. Jangan menyatakan Story Mode tamat tanpa bukti runtime yang kuat.
