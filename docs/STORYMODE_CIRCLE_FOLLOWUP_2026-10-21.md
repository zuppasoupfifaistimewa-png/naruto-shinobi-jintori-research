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

## Perbaikan follow-up selanjutnya

Run [#39526446924](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39526446924) sedang berjalan dengan konfigurasi yang dikoreksi pada workflow `.github/workflows/naruto-storymode-circle-followup.yml` commit `4551c1ab9de0334caea8c1aa2bea23bcdcacabab`:

- Mengurangi snapshot yang diambil dari 17 menjadi 12 frame per cabang untuk menekan biaya capture.
- Cabang `NONE` sekarang menghentikan proses setelah menangkap frame 150, supaya tidak menunggu ke frame 180 ketika output no-input sudah berhenti maju.
- Cabang Circle dan START tetap diamati sampai frame 180. Perbandingan antar-cabang yang dijadikan dasar kesimpulan hanya dilakukan pada frame cocok sampai 150; frame 180 adalah observasi tambahan untuk kedua input, bukan perbandingan terhadap baseline.
- Timeout tiap cabang dinaikkan dari 180 menjadi 240 detik.
- Parent checkpoint tetap dipakai ulang pada proses baru untuk setiap cabang dan tidak ditimpa. ROM, BIOS, checkpoint, dan Memory Card tetap dibersihkan dari runner temporer dan tidak dikomit ke Git.

## Status riset

- **Terverifikasi:** pemulihan checkpoint pada follow-up berhasil; hash asset valid; cabang Circle dan START selesai hingga f180 pada run parsial; perbandingan tepat sampai f150 tersedia.
- **Dugaan/hipotesis:** Circle awal menyebabkan aksi/transisi internal game yang tercermin sebagai respons visual. Makna persisnya belum diketahui.
- **Belum terverifikasi:** input START tidak punya efek pada konteks lain; pergerakan karakter/kamera pada tingkat state game; progres Story Mode kanonis; save/load Memory Card dari menu game; tamat Story Mode.

Jangan menyatakan Story Mode berlanjut atau tamat berdasarkan run ini saja.
