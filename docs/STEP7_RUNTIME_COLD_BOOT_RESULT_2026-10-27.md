# Langkah 7 — hasil runtime cold-boot (27 Oktober 2026)

Status: **SEBAGIAN**. Struktur DATA.BIN dan alur salin bootstrap didukung bukti statis, tetapi pemetaan loader/resource saat runtime, base RAM, relokasi, dan lifecycle belum dikonfirmasi.

## Run terbaru: observability A/B

- Run diagnostik: [#40479865235](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40479865235), selesai `success` pada 27 Oktober 2026 09:21:48 UTC (durasi 157 detik).
- Sumber workflow: commit `51cce7fe07ce5b73b83a5296b4a1d1d86b424ce6`; perubahan tambah kontrol `-debugger` tanpa breakpoint, lalu menjalankan probe empat target dengan `-no-debugger`.
- Artefak teks-only: [#12722187784](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40479865235/artifacts/12722187784), ukuran 3.801 byte, SHA-256 ZIP `b9537035eb6ffed66a0aadd5ab48db88715ed2e2128bcf46a48f374c7306ac26`, belum kedaluwarsa saat diperiksa.
- Semua langkah workflow selesai; pengunduhan dan checksum sumber lulus; `STEP7_PRIVATE_CLEANUP=PASS`. Tidak ada restore savestate, input gameplay, screenshot, RAM dump, atau biner game/BIOS dalam artefak.
- Pra-uji tanpa breakpoint (`-no-debugger`) mencapai VSync frame 50, lalu timeout 124 pada batas 25 detik. Kontrol `-debugger` tanpa breakpoint mencapai frame 40, lalu timeout 124 pada batas 18 detik. Keduanya menunjukkan kemajuan emulator yang lambat tetapi ada.
- Probe dengan empat breakpoint (`0x800AD454`, `0x800AD45C`, `0x80035DA8`, `0x80035D78`) hanya melaporkan frame 1, 2, 3 sebelum timeout 124 pada batas 70 detik. Tidak ada hit breakpoint loader/seed/RNG yang dapat diterima.
- **Koreksi observabilitas laporan:** report otomatis mencetak `DEBUGGER_CONTROL_MAX_VSYNC_FRAME=0`, karena regex ekstraksi metrik tidak cocok dengan raw log. Nilai itu jangan dipakai; baris raw log membuktikan frame 1, 2, 3, 10, 20, 30, 40 teramati pada kontrol debugger. Perbaiki regex parser pada iterasi berikutnya.
- Interpretasi paling kuat: kombinasi pemasangan/penanganan breakpoint membuat observasi terhambat atau sangat lambat; bukti belum mengidentifikasi komponen yang tepat. Ini **bukan** bukti loader/seed setter tidak pernah berjalan dan bukan hasil hit target negatif yang konklusif.

## Matriks kriteria Step 7

| Kriteria | Status | Bukti / batas |
|---|---|---|
| Identitas sumber yang diuji | TERVERIFIKASI | Ukuran/SHA disc, CUE, BIOS, emulator diverifikasi di runner privat. |
| Cold boot tanpa restore/input | TERVERIFIKASI | Run #40477367700 dan #40479865235; tidak ada input atau restore. |
| Progress emulator pada kontrol tanpa breakpoint | SEBAGIAN | Frame 50 pra-uji dan frame 40 kontrol debugger; keduanya mencapai timeout batas waktu, bukan kondisi frame terminasi normal. |
| Breakpoint copy sebelum/sesudah | BELUM TERBUKTI | Tidak ada hit yang diterima pada probe empat breakpoint. |
| Checksum/register source/destination | BELUM TERUJI | Tidak ada callback valid pada breakpoint copy. |
| Seed setter dan caller saat boot | UNKNOWN | Tidak ada hit yang diterima pada probe yang observasinya terhambat. |
| Base/lifecycle resource runtime | UNKNOWN | Tidak ada sampel runtime yang menetapkan pemetaan. |

## Keputusan dan eksperimen selanjutnya

Jangan ulangi probe identik empat-breakpoint. Eksperimen diagnostik berikutnya harus mengisolasi **satu breakpoint per cold boot** dengan batas waktu singkat, sumber diverifikasi, tanpa input dan tanpa restore. Mulai dari satu target yang paling informatif; catat frame progress, PC, hit count, dan timeout secara terpisah. Perbaiki regex laporan untuk menghitung angka frame dari raw log, serta pertahankan artifact teks-only dan cleanup. Jika satu breakpoint saja kembali menghambat kemajuan, lakukan kontrol listener-only dan uji breakpoint tanpa callback logging sebelum meningkatkan cakupan.

Story Mode tetap **TIDAK TERBUKTI TAMAT**.
