# Latest continuation checkpoint — 24 October 2026

The handoff was refreshed after offline evidence analysis and regression-only monitor hardening.

- **Latest tested source HEAD before this documentation refresh:** 6d2fdc4553f5eacabf2607c19ebf69bc012c2c51.
- **Latest regression:** [run #40061967694](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40061967694), success; 32/32 tests, authentic screenshot checks and all workflow steps passed. Monitor policy regression from the current source lineage also passed in [run #40061712532](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40061712532).
- New measured F20→F60 blue-proxy motion: Revision65 UP 8.38 px, WAIT 7.17 px, map UP 5.01 px, map WAIT 5.03 px; scene shifts +100 px for both UP branches, 0 px for WAIT. This rules out proxy proximity as an independent target cue. The pink badge still tracks the scene pan (+97.46 px), not a verified focus-ring/panel change.
- Monitor now treats only known, unmarked push skips with no evidence artifact as EXPECTED_GATED_SKIP_NO_GO. Other skips/failures/missing artifacts/stale runs still alert. A gated skip is **not** gameplay success.
- **Readiness remains NO-GO; Story Mode remains NOT COMPLETE.** barrier_level_selection remains WAIT; consumed Revision65 marker/blob 3754a6ddf45a7570c053d9c149b6d80b0862a127 is unchanged and cue token remains absent. No player, restore, or gameplay-input workflow was launched. Keep all private evidence/game assets outside Git.

**Next action:** continue offline analysis from this tested checkpoint only. Do not change the consumed marker or authorize any input until an independently unique submenu target cue is demonstrated from authentic evidence and the fail-closed gate/new marker are explicitly reviewed. Read current STATUS.md and ANALYSIS_LOG.md before continuing. Check actual HEAD again before any write; this documentation refresh is expected to create a separate documentation-only commit.

---

# Handoff target kerja berikutnya — pemain adaptif Story Mode (24 Oktober 2026)

Dokumen ini adalah target kerja yang harus dibaca dari chat baru sebelum mengubah apa pun. Jangan mengulang validasi yang sudah lulus dan jangan menganggap pekerjaan selesai hanya karena regresi teknis hijau.

## Tujuan utama

Membuat pemain adaptif yang aman, terukur, dan akhirnya dapat menjalankan Story Mode Naruto – Shinobi no Sato no Jintori Gassen (Japan, PS1) secara mandiri melalui GitHub Actions tanpa chat ChatGPT harus tetap terbuka. Fokusnya adalah kesiapan operasional pemain adaptif dan kemajuan gameplay yang terverifikasi; **bukan** mengklaim permainan tamat sebelum bukti autentik tersedia. Tidak ada jaminan keberhasilan 100%.

## Titik awal yang wajib dipakai

- Repo yang boleh diakses/diubah: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research` saja.
- HEAD terverifikasi saat handoff dibuat: `1c1e1a7c0aa292ec50c10a1064ca794b58802305`.
- Regresi terakhir: [run #40059425253](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40059425253), **success**, 15/15 langkah, 27 tes lulus.
- Baca dahulu `STATUS.md`, `ANALYSIS_LOG.md`, `docs/HANDOFF_ADAPTIVE_PLAYER_2026-10-23.md`, serta dokumen diagnostik/struktural savestate dan Story Mode yang relevan. Gunakan hasil di sana sebagai fakta yang sudah ada, bukan pekerjaan baru.

## Status dan keputusan yang tidak boleh diabaikan

- Kesiapan pemain adaptif: **NO-GO**.
- Story Mode: **NOT COMPLETE**.
- State `barrier_level_selection` harus tetap `WAIT`; target peningkatan berwarna pink-60 di submenu belum teridentifikasi secara unik.
- Marker `experiments/.run-storymode-adaptive-player` tetap Revision65 yang sudah dikonsumsi; jangan rerun, mengganti, atau menganggapnya sebagai izin untuk input.
- Jangan menambahkan `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` sampai cue benar-benar terverifikasi secara independen.
- Jangan menjalankan player, restore/continuation, atau input gameplay baru saat gate cue belum lulus. Jangan menjalankan gameplay hanya agar monitor berubah hijau. Monitor yang membaca run `skipped` tanpa artifact pemain yang valid adalah status monitoring yang diketahui, bukan bukti gameplay gagal atau maju.
- Workflow fixed-sequence Story Mode dan raw restore/continuation tetap dinonaktifkan dengan `if: false`; pertahankan containment ini.
- Tidak ada ROM, BIOS, Memory Card, savestate, screenshot gameplay, atau artifact privat yang boleh dimasukkan ke Git.

## Prioritas kerja konkret

1. **Verifikasi titik awal dan jangan mengulang.** Periksa HEAD, diff/status, dokumen handoff, dan hasil Actions terbaru di repo yang diizinkan. Pastikan tidak ada run tak terduga yang aktif sebelum tindakan selanjutnya.
2. **Kerjakan blocker yang relevan dengan kesiapan, bukan sekadar membuat CI hijau.** Gunakan hanya screenshot autentik dan artifact privat yang sudah ada untuk menajamkan classifier/state transitions, membedakan terrain/camera pan, foreground pose, pointer, ring cue, dan perubahan panel. Jangan mengulang pengukuran yang sudah ada kecuali untuk reproduksi regresi.
3. **Jaga keputusan fail-closed.** Di submenu level-up, pink-60, proximity pointer, perubahan piksel tunggal, gerakan latar, atau pose karakter tidak cukup sebagai bukti pilihan. Hipotesis cue terkuat yang sudah diketahui adalah ring panah fokus **dan** panel informasi yang cocok berubah untuk tile yang sama. Cue ini masih harus ditunjukkan secara independen pada konteks submenu sebelum input apa pun diizinkan.
4. **Tambahkan tes yang menguji keputusan gameplay-agent, bukan hanya detail citra.** Prioritaskan tes false-positive/false-negative untuk klasifikasi state, `WAIT` saat keyakinan tidak cukup, pencegahan input saat gate gagal, penanganan checkpoint/timeout/recovery, serta keputusan loop autonom yang dapat diaudit. Semua perubahan harus memiliki uji regresi yang spesifik dan tidak membuka trigger gameplay yang tidak disengaja.
5. **Sebelum mengizinkan percobaan input pada masa depan**, wajib ada bukti cue target submenu yang unik dari artifact autentik yang sudah tersedia, tes regresi lulus, marker baru yang ditinjau eksplisit, dan verifikasi bahwa allowlist/fail-closed gate aktif. Jika syarat belum terpenuhi, teruskan pekerjaan offline; jangan melewati gate demi mencoba-coba.
6. **Setelah kesiapan benar-benar didukung bukti**, jalankan percobaan kecil yang terukur dan terisolasi terlebih dahulu. Jangan menargetkan marathon enam jam atau otomatisasi panjang sebelum ada loop pendek yang dapat memutuskan aksi, mendeteksi state baru, berhenti aman, menyimpan checkpoint privat, dan pulih tanpa tindakan manual berulang.
7. **Catat hasil dan handoff setiap kali ada perubahan** di `STATUS.md`, `ANALYSIS_LOG.md`, serta dokumen handoff yang tepat. Catat commit, run ID, kesimpulan tes, evidensi, blocker, dan satu langkah berikutnya. Bedakan dengan tegas `VERIFIED`, `HYPOTHESIS`, dan `UNKNOWN`.

## Aturan gameplay dan bukti

- Bukti visual gameplay harus berasal dari screenshot autentik emulator/game, bukan gambar web.
- Bila dialog Story Mode sudah dikenali, gunakan **START** untuk melewati dialog, bukan Circle.
- Letakkan terjemahan Indonesia persis di samping teks Jepang dalam tanda kurung.
- Jangan menyatakan Story Mode tamat tanpa bukti kuat yang autentik dan dapat diverifikasi. Selama belum terbukti, status tetap **NOT COMPLETE**.
- Tujuan akhirnya adalah dapat dijalankan oleh GitHub Actions tanpa chat ChatGPT terbuka; chat adalah tempat pengembangan/audit, bukan runtime wajib.

## Format laporan setiap sesi

Laporkan singkat: (1) checkpoint/commit yang benar-benar diperiksa, (2) pekerjaan yang berubah, (3) tes/Actions yang benar-benar dijalankan beserta hasilnya, (4) dampak pada kesiapan dengan alasan bukti, (5) blocker yang tersisa, dan (6) langkah berikutnya. Jangan menyamakan regresi sukses dengan kesiapan pemain atau keberhasilan menyelesaikan permainan.
