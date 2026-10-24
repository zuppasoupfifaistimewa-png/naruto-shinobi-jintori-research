# Latest continuation checkpoint — 24 October 2026

This checkpoint supersedes the older status bullets below. It was refreshed after the offline submenu cue-composite regression passed.

- **Current tested code/test HEAD:** `d1c0428381581b80814bebf6557f5579594bb9da`.
- **Latest regression:** [Actions run #40064182088](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40064182088) — `success`, 33/33 unit tests in 4.872 seconds; all workflow steps passed, including existing authenticated screenshot policy checks and the new level-up cue composite.
- **New cue audit:** map-UP reference ring/frame/text = 811 / 8,312 / 635; map-WAIT = 62 / 8,629 / 15; Revision65 submenu-UP = 66 / 2,452 / 3,221; submenu-WAIT = 67 / 2,566 / 39. Require ring + statistics-panel footprint + panel-text transition together. The large submenu text delta is rejected because the ring and expected panel footprint are absent. Four prompt-text comparisons return zero bright-text-mask changes.
- These are offline measurements on existing authentic private evidence from runs #39947481094 and #39786019434. They do **not** establish a unique level-up target cue.
- `barrier_level_selection` remains **WAIT**; target cue remains **UNKNOWN**; readiness remains **NO-GO**; Story Mode remains **NOT COMPLETE**.
- Consumed marker `experiments/.run-storymode-adaptive-player` remains Revision65, blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`, unchanged. `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` remains absent. All pre-download/PAD checks and legacy workflow containment remain in force.
- No player, emulator, restore, or gameplay-input workflow was run. Private evidence and all game assets stay outside Git.
- Monitor failures #40048510714, #40034304421 and #40010286618 still refer to the intentionally gated/skipped historical player run #39975090690 without a valid evidence artifact. Do not start gameplay just to clear monitor warnings; a gated skip is neither gameplay success nor game failure.

**Next action:** continue offline with the existing authenticated submenu screenshots. Search for a unique, tile-anchored cue independent of camera pan, HUD unocclusion, and character pose. Do not replace the marker, set the cue token, or inject input until that submenu-specific cue is independently demonstrated and a new marker, allowlist, pre-download/PAD gate, and regression are reviewed. Then record the specific evidence rather than inferring from the map-only reference.

---

# Handoff target kerja berikutnya — pemain adaptif Story Mode (24 Oktober 2026)

Dokumen ini adalah target kerja yang harus dibaca dari chat baru sebelum mengubah apa pun. Jangan mengulang validasi yang sudah lulus dan jangan menganggap pekerjaan selesai hanya karena regresi teknis hijau.

## Tujuan utama

Membuat pemain adaptif yang aman, terukur, dan akhirnya dapat menjalankan Story Mode Naruto – Shinobi no Sato no Jintori Gassen (Japan, PS1) secara mandiri melalui GitHub Actions tanpa chat ChatGPT harus tetap terbuka. Fokusnya adalah kesiapan operasional pemain adaptif dan kemajuan gameplay yang terverifikasi; **bukan** mengklaim permainan tamat sebelum bukti autentik tersedia. Tidak ada jaminan keberhasilan 100%.

## Titik awal yang wajib dipakai

- Repo yang boleh diakses/diubah: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research` saja.
- HEAD terverifikasi untuk kelanjutan ini: `d1c0428381581b80814bebf6557f5579594bb9da`.
- Regresi terakhir: [run #40064182088](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40064182088), **success**, 33/33 tes, semua langkah workflow lulus.
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
