# Hasil probe Circle timeline — 21 Oktober 2026

## Ringkasan run

- Workflow: [#39524697802 — Naruto Story Mode Circle timeline probe](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39524697802)
- Status: `success`; mulai 08:00:08 WIB, selesai 08:01:54 WIB pada 21 Oktober 2026; durasi 1 menit 46 detik.
- Artifact privat: [#12311254886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39524697802), `naruto-storymode-circle-timeline-private`; 5.487.105 byte; digest ZIP GitHub `sha256:b121b6df1037a4877f688a450b841cd9e1112fe753625b7132548468117269f4`; kedaluwarsa 4 November 2026 08:01:48 WIB.
- Kelima cabang (NONE, CIRCLE_TAP_EARLY, CIRCLE_HOLD30, CIRCLE_TAP_LATE, LEFT_TAP_EARLY) sukses memuat checkpoint yang sama dalam proses terpisah, merekam `CIRCLE_TIMELINE_LOAD_EVENT=PASS`, `CIRCLE_TIMELINE_LOAD_RETURNED=1`, dan `CIRCLE_TIMELINE_BRANCH_DONE`. Semua screenshot sesuai rencana tersedia hingga frame 90.
- Checkpoint induk: 21.162.405 byte, SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`. Hash parent pada laporan sama; `CIRCLE_TIMELINE_PARENT_STATE_MUTATION=NO`.
- AppImage PCSX-Redux patched yang dipakai ulang: SHA-256 `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`. Tidak ada rebuild emulator pada run ini.

## Hasil visual yang terukur

Perbandingan dilakukan pada jumlah VSync yang sama, dengan cabang NONE sebagai baseline deterministik.

| Cabang | Input | Hasil gambar |
|---|---|---|
| NONE | Tanpa tombol | Baseline; kamera/area papan sendiri berubah selama animasi waktu. |
| CIRCLE_TAP_EARLY | Circle ditekan pada frame 30 lalu dilepas pada frame 38 | Gambar identik dengan baseline pada frame 20, 29, 30, 32, dan 35; perubahan pertama pada frame 37 (mean absolute RGB difference 17.547; 15.772% piksel identik), lalu perbedaan membesar sampai frame 90 (MAD 52.710; 7.445% piksel identik). |
| CIRCLE_HOLD30 | Circle ditahan 30 frame dari frame 30 | Identik dengan CIRCLE_TAP_EARLY pada semua titik screenshot yang diperiksa sampai frame 90. Belum ada bukti bahwa tahan lebih lama menambah efek. |
| CIRCLE_TAP_LATE | Circle ditekan pada frame 60 lalu dilepas pada frame 68 | Identik dengan NONE pada semua titik screenshot sampai frame 90. |
| LEFT_TAP_EARLY | Tombol kiri ditekan pada frame 30 lalu dilepas pada frame 38 | Identik dengan NONE pada semua titik screenshot sampai frame 90. |

Visual cabang Circle awal berbeda secara nyata dari baseline: pada frame 90 komposisi papan/kamera berubah dan sprite karakter muncul pada area permainan. Namun baseline juga mengalami animasi kamera tanpa input. Bukti yang kuat adalah **input Circle awal berkaitan dengan respons visual tambahan**, bukan bahwa fungsi gameplay spesifiknya sudah diketahui. Gambar saja belum cukup untuk menyatakan apakah ini memilih, mengonfirmasi, memulai gerakan, atau memicu transisi.

Log `pad.getButton` menegaskan bahwa emulator membaca press dan release. Pembacaan sisi emulator ini tidak cukup sendiri untuk membuktikan aksi semantik di game; perubahan visual pada cabang Circle awal memberi bukti runtime pendukung.

## Interpretasi dan status

- **Terverifikasi secara runtime:** semua cabang dapat memulihkan checkpoint parent yang sama; semua pengamatan frame 90 selesai; input press/release terjadi pada sisi emulator; parent state tidak berubah.
- **Dukungan bukti sedang:** tap Circle pada timing awal menghasilkan cabang visual yang berbeda mulai frame 37 dan terus berbeda sampai frame 90.
- **Belum terverifikasi:** makna pasti Circle; apakah papan/turn/gameplay benar-benar sudah maju secara kanonis; pemetaan kontrol gerak; save/load Memory Card dalam game; penyelesaian Story Mode.
- Tombol LEFT tidak mengubah screenshot pada timing yang diuji. Ini tidak membuktikan tombol arah tidak berfungsi dalam semua konteks.
- Hasil sebelumnya #39523066920 berhenti setelah frame 150 karena timeout cabang, tanpa marker selesai. Retry #39524697802 memperbaiki batas observasi dengan menyelesaikan seluruh cabang sampai frame 90; hasilnya sukses.

## Langkah lanjutan yang disarankan

1. Pertahankan checkpoint parent serta AppImage yang terhash; jangan menimpa atau mengubah checkpoint induk.
2. Gunakan cabang baru dari checkpoint yang sama, bukan meneruskan keadaan dari screenshot branch yang sudah berubah. Perpanjang observasi cabang NONE, tap Circle awal, dan tap START awal hingga setidaknya frame 180 (dan lebih jauh bila transisi belum stabil); ambil screenshot rapat di sekitar frame 30–45 dan setelah frame 90 untuk membedakan animasi dari perubahan state.
3. Bila perubahan visual berlanjut, catat indikator UI/papan yang berubah dan cari apakah ada dialog/menu atau prompt kontrol; baru lakukan input kedua berdasarkan tampilan yang benar-benar terlihat. Pertahankan klasifikasi hipotesis untuk makna tombol sampai ada bukti semantik.
4. Jangan mengklaim Story Mode tamat atau Memory Card in-game tervalidasi tanpa bukti runtime eksplisit.

ROM, BIOS, savestate, dan isi Memory Card tidak dimasukkan ke Git; aset privat hanya digunakan sementara pada runner.
