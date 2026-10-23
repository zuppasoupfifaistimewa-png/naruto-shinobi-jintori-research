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

## Run #39529241370 — tap kedua di frame 175, tetapi frame berhenti setelah f180

Run: [#39529241370](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39529241370)  
Mulai 08:46:27 WIB; selesai 08:47:46 WIB. Status: `failure`.

- Cabang `CIRCLE_WAIT` menuntaskan penangkapan sampai frame 181 dan keluar normal.
- Cabang konfirmasi mengambil screenshot f175 lalu mengirim Circle kedua; pad-readback menyatakan `true/PASS`. Screenshot f176, f177, f178, f179, dan f180 masih pixel-identik dengan cabang tunggu. Tidak ada f181 pada cabang konfirmasi; proses berakhir setelah timeout 45 detik (`code=124`).
- Jadi tap dikirim dan input pad berubah, tetapi tidak ada perubahan gambar yang terlihat dalam frame pasca-input yang tersedia. Frame/game emulasi berhenti sebelum release dijadwalkan pada f183. Ini membuat eksperimen tidak bisa membedakan apakah game menunggu pelepasan tombol, emulator macet, atau ada penyebab lain.
- Tidak ada state baru; restore di proses emulator baru tidak dijalankan.
- Artefak privat #12314327303, 4.659.232 byte, digest ZIP `sha256:f370dd9bbf5efe0903d21326d8dc5fe0638c08e35e15e2c91b156529b31ca975`, berisi PNG/raw RGB/log serta laporan. Artefak tetap privat dan tidak ada aset game yang ditambahkan ke Git.

## Run #39529605910 — tap pendek, gambar berubah di f184 tetapi kontrol gagal

Run: [#39529605910](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39529605910)  
Mulai 08:50:22 WIB; selesai 08:51:45 WIB. Status: `failure`.

- Kedua proses emulator mengalami segmentation fault (`code=139`): cabang tunggu sekitar f180; cabang Circle kedua setelah mengambil screenshot f184. Cabang tunggu menghasilkan screenshot yang bisa dipakai sampai f179; metadata untuk f180 ada tetapi berkas raw-nya berukuran 0, sehingga konverter berhenti dan laporan komparatif workflow tidak selesai.
- Pada cabang konfirmasi, Circle kedua dikirim setelah screenshot f175 (`readback=true/PASS`) dan dilepas setelah screenshot f178 (`readback=false/PASS`). Screenshot f175–f179 pixel-identik dengan cabang tunggu untuk frame yang tersedia.
- Screenshot f181 masih tampak seperti panel misi; f182 memperlihatkan perubahan visual kecil (MAD antarfame 3.413; 95.99% piksel sama); f183 sama dengan f182; f184 menunjukkan lingkaran merah besar di sisi kanan bawah (MAD f183→f184 7.786; 90.87% piksel sama). Panel `任務内容`, target `3000チャクラためる`, dan prompt `けってい` masih tampak. Tidak ada frame tunggu pembanding yang valid untuk f180 ke atas, jadi perubahan f182/f184 belum bisa diatribusikan dengan yakin kepada input kedua daripada animasi/masalah runtime.
- Karena eksperimen versi ini menyimpan hanya pada f240 dan proses crash di f184, tidak ada checkpoint konfirmasi atau pemulihan lintas-proses. Checkpoint induk tetap utuh.
- Artefak privat #12315236554, 4.882.885 byte, digest ZIP `sha256:da1f2ac778eab9ea1a4633d972b0ed8b72b8396b8f417436b2499bec8cf82221`, disimpan privat. PNG/raw dipulihkan dan dianalisis lokal; tidak ada berkas game/BIOS/savestate dimasukkan ke Git.

## Run #39530038534 — checkpoint pada f178 dan pemulihan lintas-proses sukses

Run: [#39530038534](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39530038534)  
Mulai 09:00:08 WIB; selesai 09:01:53 WIB pada 21 Oktober 2026. Status workflow: `success`.

- Kedua cabang memuat checkpoint induk dengan `CIRCLE_TIMELINE_LOAD_EVENT=PASS` dan `CIRCLE_TIMELINE_LOAD_RETURNED=1`. Cabang tunggu selesai normal pada frame 178. Cabang kedua mengirim tap Circle pertama pada f30–f38, kemudian tap Circle konfirmasi setelah screenshot f175 dan melepasnya pada f178; log pad menunjukkan press `readback=true status=PASS` dan release `readback=false status=PASS`.
- Perbandingan screenshot yang cocok sampai f178 memberikan `mad=0.000, exact=1.00000` pada semua frame yang tersedia. Jadi tidak ada perubahan visual terukur antara cabang tunggu dan cabang Circle-kedua hingga f178. Ini **tidak** membuktikan Circle kedua tak bekerja; game belum diamati melewati panel/prompt setelah input tersebut.
- Workflow menyimpan checkpoint privat segera setelah input release pada f178. Ukurannya **21.162.838 byte**; SHA-256 **`a87529407736b1b7648785db8644d3c10f0b8d5d12f1557c63d9a3155b22fa83`**.
- Checkpoint tersebut disalin ke lingkungan kerja sementara dan diuji dalam proses emulator yang baru: `CIRCLE_FOLLOWUP_FRESH_PROCESS_RELOAD_EXIT=0`, load event PASS, loader-return PASS, screenshot f1 dan f10 tersedia, `BRANCH_DONE mode=RELOAD_CONFIRM frame=10`, serta `CIRCLE_FOLLOWUP_FRESH_PROCESS_RESTORE=PASS`. Ini memverifikasi pemulihan checkpoint ini pada build patched yang dipakai run; bukan bukti progres Story Mode.
- Manifest melaporkan `CIRCLE_FOLLOWUP_PARENT_STATE_MUTATION=NO`. Checkpoint induk tetap 21.162.405 byte, SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`.
- Artefak privat #12314982935, nama `naruto-storymode-circle-followup-private`, ukuran 6.032.044 byte, digest ZIP `sha256:e23112ce7a6c2a7b65b6cc8dfa15bf41e94528228b6896060337fac68a5d7033`. Artefak mengandung bukti PNG/log dan berkas savestate privat; tidak ada ROM, BIOS, savestate, atau isi Memory Card yang dimasukkan ke Git. Artefak kedaluwarsa setelah periode retensi Actions (14 hari).

## Langkah berikutnya

Checkpoint setelah tap kedua sekarang dapat dipulihkan dalam proses baru. Kelanjutan riset paling aman adalah memuat checkpoint privat itu dalam eksperimen terpisah dan menjalankan beberapa VSync tambahan tanpa input untuk melihat apakah game melanjutkan transisi setelah key release; bandingkan terhadap checkpoint cabang tunggu dengan jumlah VSync sama. Jangan menimpa checkpoint induk. Simpan checkpoint turunan serta bukti runtime di artefak privat dan verifikasi hash/restore setiap kali.

## Klasifikasi kesimpulan saat ini

- **Terverifikasi:** checkpoint induk dimuat di dua cabang terisolasi; input Circle kedua diterima controller override pada f175 dan dilepas pada f178; screenshot tunggu/konfirmasi identik sampai f178; checkpoint turunan f178 tersimpan dan lulus uji restore pada proses emulator baru selama 10 VSync.
- **Hipotesis:** proses emulator pada beberapa run terdahulu berhenti memajukan VSync atau crash di sekitar panel konfirmasi; run #39530038534 dapat menyimpan dan memulihkan state f178 sebelum crash berikutnya, tetapi penyebab masalah VSync/segfault belum diketahui.
- **Belum terverifikasi:** apakah Circle kedua pada prompt `けってい` memicu kemajuan Story Mode setelah frame 178; aturan gameplay lainnya; save/load Memory Card dari dalam game; dan tamat Story Mode.

Jangan menganggap panel atau teks target sebagai bukti bahwa target Chakra telah tercapai. Jangan menyatakan Story Mode tamat tanpa bukti runtime yang kuat.


## Follow-up kelanjutan checkpoint pascakonfirmasi — run #39546339666

Eksperimen berikutnya selesai pada 21 Oktober 2026 pukul 11:53:02 WIB (mulai 11:51:43; durasi sekitar 1 menit 19 detik), status workflow `success`. Artefak privat [#12321752942](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39546339666/artifacts/12321752942) menyimpan bukti PNG/raw dan log. Laporan terperinci: [STORYMODE_POST178_CONTINUATION_2026-10-21.md](STORYMODE_POST178_CONTINUATION_2026-10-21.md).

- Checkpoint turunan ini berhasil dipulihkan di proses baru dan menjalankan 62 VSync tanpa input; hash checkpoint induk dan turunan tetap tidak berubah.
- Cabang kontrol tanpa Circle kedua crash kode 139 setelah screenshot f187. Cabang turunan berjalan normal sampai f62 lokal (kira-kira ekuivalen kontrol f240). Gambar identik sampai kontrol f181/turunan f3, lalu berubah mulai kontrol f182/turunan f4.
- UI pascakonfirmasi menunjukkan panel `任務内容` masih ada, prompt `けってい` hilang dan cap merah mirip `決` muncul. Ini bukti visual respons atas konfirmasi, tetapi belum bukti masuk gameplay aktif. Workflow `success` menunjukkan harness/artefak sukses; emulator kontrol sendiri gagal dengan kode 139.
- Tahap selanjutnya: checkpoint baru pada panel pascakonfirmasi yang stabil, validasi restore di proses baru, kemudian uji cabang input terisolasi. Story Mode belum terbukti tamat; save/load Memory Card dari dalam game belum diverifikasi.
