# Follow-up timeline Circle versus START — 21 Oktober 2026

## Rangkuman eksekusi

Run pertama follow-up setelah perbaikan jalur artefak: [#39525735032](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39525735032).

- Status workflow: `failure`; mulai 08:10:15 WIB, selesai 08:14:54 WIB.
- Semua prasyarat runtime berhasil: AppImage, checkpoint, Memory Card, serta game/BIOS berhasil diunduh dan lolos hash. Error jalur lama dari run #39525534387 sudah terselesaikan.
- Kegagalan terjadi pada langkah observasi karena cabang `NONE` timeout setelah 180 detik. Log runner: `CIRCLE_TIMELINE_BRANCH_EXIT mode=NONE code=124`. Cabang NONE punya screenshot sampai frame 150 tetapi tidak mencapai marker penutupan; cabang Circle dan START sama-sama menghasilkan screenshot frame 180 dan marker `BRANCH_DONE`.
- Artifact privat #12313911764: [lihat run/artifact](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39525735032), 3.921.811 byte, digest `sha256:69e2ec87b8581dd8b3082359dacfdcf61acc15d315ca88482d1abae5814a87ac`, kedaluwarsa 4 November 2026 sekitar 08:14:48 WIB.
- Checkpoint induk tidak berubah: SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`. AppImage patched tetap hash `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`.

## Temuan yang tetap dapat digunakan

Screenshot pada frame yang sama tersedia untuk ketiga cabang hingga frame 150. Cabang NONE adalah baseline deterministik pada titik yang berhasil ditangkap.

| Frame | Circle tap awal versus NONE | START tap awal versus NONE |
|---:|---|---|
| 20–35 | Identik | Identik |
| 37 | MAD 17.547; 15.772% piksel identik | Identik, MAD 0 |
| 38 | MAD 22.766; 12.383% piksel identik | Identik, MAD 0 |
| 45 | MAD 33.514; 9.398% piksel identik | Identik, MAD 0 |
| 90 | MAD 52.710; 7.445% piksel identik | Identik, MAD 0 |
| 120 | MAD 42.308; 8.132% piksel identik | Identik, MAD 0 |
| 150 | MAD 42.588; 7.979% piksel identik | Identik, MAD 0 |
| 180 | Tidak bisa dibandingkan: NONE tidak punya frame 180 | Tidak bisa dibandingkan: NONE tidak punya frame 180 |

Pada cabang Circle, perubahan visual yang dimulai di frame 37 bertahan melewati frame 150. Cabang START tidak menghasilkan perubahan yang terlihat di frame-frame cocok sampai 150. Ini bukti respons visual yang terkait dengan Circle pada timing awal, tetapi bukan bukti fungsi spesifik tombol atau progres Story Mode kanonis. Perubahan kamera/scene juga terjadi tanpa input; screenshot saja tidak cukup untuk menamai aksi.

Observasi tambahan yang hanya tersedia pada cabang input di frame 180: cabang Circle menampilkan panel Jepang berjudul “任務内容” (isi misi), dengan baris “3000チャクラためる” (mengumpulkan/menabung 3.000 Chakra) dan “ついか条件なし” (tanpa syarat tambahan), serta prompt konfirmasi “けってい”. Cabang START pada f180 masih memperlihatkan papan dan efek visual di petak, bukan panel yang sama. Karena baseline NONE tidak mempunyai f180, tampilan panel ini adalah petunjuk kuat adanya perbedaan jalur, tetapi tidak berdiri sendiri sebagai bukti kausal penuh terhadap baseline pada waktu yang sama.

## Validasi final dan kondisi workflow saat ini

- Follow-up pertama [#39525735032](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39525735032) gagal pada verifikasi awal akibat path staging lama; emulator tidak dijalankan pada run tersebut.
- Follow-up kedua [#39526446924](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39526446924) menjalankan ketiga cabang dan menghasilkan bukti lengkap. Status job gagal hanya karena langkah akhir `cat` membaca nama file laporan lama setelah laporan baru berhasil ditulis. Evidence-nya tetap valid.
- Validasi final [#39526690265](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39526690265) selesai dengan status `success` pada 08:21:22 WIB, durasi sekitar 1 menit 21 detik. Artifact privat #12313342874 berukuran 2.755.974 byte, digest ZIP `sha256:9988b3d34c24441ad13c8453f2e41af60cde0698a2f7b30130a2fc46c5b02a8d`, kedaluwarsa 4 November 2026 sekitar 08:21:17 WIB.
- Perbaikan workflow pada commit `fb1d3b779611cb7938370d018290b2e2be7b1328` menyelaraskan path laporan dan daftar frame metrik dengan screenshot yang benar-benar diambil. Report sekarang menampilkan frame terpilih: 20, 29, 30, 35, 37, 38, 39, 45, 90, 120, 150, 180.
- Hasil pengamatan tidak berubah: perbandingan yang valid hingga frame 150 menunjukkan Circle awal berbeda mulai frame 37 dan masih berbeda pada frame 150; START awal identik dengan baseline pada semua frame cocok hingga 150. Panel misi yang tampak pada screenshot Circle f180 adalah observasi endpoint tambahan; NONE f180 tidak ada sehingga tidak dilakukan perbandingan langsung pada f180.
- Parent checkpoint tidak berubah: 21.162.405 byte, SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`. AppImage patched: `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`.

## Langkah teknis berikutnya

Gunakan kembali checkpoint parent yang sama pada cabang baru untuk menguji apakah input Circle kedua pada panel `任務内容` dengan prompt `けってい` mengonfirmasi/memasuki langkah Story Mode selanjutnya. Bandingkan cabang “tunggu tanpa input kedua” dengan cabang “tap Circle kedua”, ambil screenshot rapat sebelum/sesudah input, dan jika perlu simpan checkpoint baru lewat `PCSX.createSaveState()` hanya ke artifact privat lalu verifikasi restore dalam proses emulator kedua. Jangan menimpa checkpoint parent, jangan menganggap tujuan 3.000 Chakra sudah tercapai hanya karena teks target terlihat, dan gunakan START untuk dialog Story Mode hanya setelah dialog benar-benar teramati.

## Status riset

- **Terverifikasi:** pemulihan checkpoint pada follow-up berhasil; hash asset valid; cabang Circle dan START selesai hingga f180 pada run parsial; perbandingan tepat sampai f150 tersedia.
- **Dugaan/hipotesis:** Circle awal menyebabkan aksi/transisi internal game yang tercermin sebagai respons visual. Makna persisnya belum diketahui.
- **Belum terverifikasi:** input START tidak punya efek pada konteks lain; pergerakan karakter/kamera pada tingkat state game; progres Story Mode kanonis; save/load Memory Card dari menu game; tamat Story Mode.

Jangan menyatakan Story Mode berlanjut atau tamat berdasarkan run ini saja.
