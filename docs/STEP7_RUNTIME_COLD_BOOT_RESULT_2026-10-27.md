# Langkah 7 — hasil runtime cold-boot (27 Oktober 2026)

Status: **SEBAGIAN**. Struktur DATA.BIN dan alur salin bootstrap didukung bukti statis, tetapi pemetaan loader/resource saat runtime, base RAM, relokasi, dan lifecycle belum dikonfirmasi.

## Run historis: observability A/B (#40479865235)

- Run diagnostik: [#40479865235](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40479865235), selesai `success` pada 27 Oktober 2026 09:21:48 UTC (durasi 157 detik).
- Sumber workflow: commit `51cce7fe07ce5b73b83a5296b4a1d1d86b424ce6`; perubahan tambah kontrol `-debugger` tanpa breakpoint, lalu menjalankan probe empat target dengan `-no-debugger`.
- Artefak teks-only: [#12722187784](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40479865235/artifacts/12722187784), ukuran 3.801 byte, SHA-256 ZIP `b9537035eb6ffed66a0aadd5ab48db88715ed2e2128bcf46a48f374c7306ac26`, belum kedaluwarsa saat diperiksa.
- Semua langkah workflow selesai; pengunduhan dan checksum sumber lulus; `STEP7_PRIVATE_CLEANUP=PASS`. Tidak ada restore savestate, input gameplay, screenshot, RAM dump, atau biner game/BIOS dalam artefak.
- Pra-uji tanpa breakpoint (`-no-debugger`) mencapai VSync frame 50, lalu timeout 124 pada batas 25 detik. Kontrol `-debugger` tanpa breakpoint mencapai frame 40, lalu timeout 124 pada batas 18 detik. Keduanya menunjukkan kemajuan emulator yang lambat tetapi ada.
- Probe dengan empat breakpoint (`0x800AD454`, `0x800AD45C`, `0x80035DA8`, `0x80035D78`) hanya melaporkan frame 1, 2, 3 sebelum timeout 124 pada batas 70 detik. Tidak ada hit breakpoint loader/seed/RNG yang dapat diterima.
- **Koreksi historis dan tindak lanjut:** run ini mencetak `DEBUGGER_CONTROL_MAX_VSYNC_FRAME=0` karena regex yang saat itu aktif salah escaping. Raw log sebenarnya mencatat frame 1, 2, 3, 10, 20, 30, 40. Regex shell/Python kemudian diperbaiki dan fixture regresi lulus pada #40484417534 (`frames=1,2,3,10,20,30,40 max=40`); hasil runtime single-breakpoint koreksi tercatat di addendum bawah dan pada run #40484548650.
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

## Addendum — perbaikan parser dan cold boot satu breakpoint (27 Oktober 2026)

### Koreksi parser yang teruji

- Workflow parser diperbaiki pada commit [b7e44fca665436a9e6acf45e55a13121574afff9](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/b7e44fca665436a9e6acf45e55a13121574afff9) agar shell `sed` dan Python memakai escape regex yang benar.
- Regression test [#40484417534](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484417534) selesai success. Raw log menyatakan `STEP7_FRAME_PARSER_FIXTURE_PASS frames=1,2,3,10,20,30,40 max=40`; artinya parser sekarang mengembalikan angka yang benar dari fixture, tidak hanya workflow berwarna hijau.

### Cold boot satu breakpoint — bukti dari raw log

- Run [#40484519812](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484519812), source SHA `9edbcb3063a41588ca739e644b9dc9b29c585b3f`. Aset sumber diverifikasi: disc `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`; CUE `be70d64f856e17aadc02cdcba7510234f5a11523216baddb3b247c95cec820b8`; arsip BIOS `b436489c574457560489bfaad11b2a2171c684edba34d69de107b7b26dfc0e3a`; emulator `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`; BIOS ekstrak `5e84a94818cf5282f4217591fefd88be36b9b174b3cc7cb0bcd75199beb450f1`.
- Pra-uji tanpa breakpoint mencapai frame 50 (batas 25 detik, exit 124). Pada run awal, kontrol debugger listener-only mencapai frame 50; run koreksi melaporkan frame 1, 2, 3, 10, 20, 30, 40, 50, 60 (batas 18 detik, exit 124) dengan `DEBUGGER_CONTROL_MAX_VSYNC_FRAME=60` hasil parser.
- Cold boot target mendaftarkan **satu breakpoint saja** pada kandidat `0x800AD454`, callback hanya mencatat PC/frame/hit count, tanpa restore/input. Run awal mencatat progress hingga frame 100; run koreksi mencatat progress frame 1–3 lalu kelipatan 10 sampai frame 120. Parser akhir melaporkan `SINGLE_BREAKPOINT_HIT=NO`, hit count `0`, dan `SINGLE_BREAKPOINT_DONE=NO`; emulator exit 124 pada batas 35 detik. Ini membedakan hasil dari probe empat breakpoint yang macet di frame 1–3: satu breakpoint dengan callback ringan tetap mengizinkan kemajuan, tetapi alamat target tidak menghasilkan hit yang diamati dalam jendela terbatas.
- Tahap report assembler pada run awal gagal dengan `SyntaxError: '[' was never closed`; artefak #12723834084 (1.894 byte, digest ZIP `6188c32e73a0984133c5c1f4ac3a37dcacde677458ec56c7fdf100ba25c73968`) bukan ringkasan lengkap yang valid. Raw log tetap membuktikan progress hingga frame 100 tanpa hit dan cleanup PASS. Commit koreksi assembler `8326c07f71caeab12924133b0812ec7e86b8b1f7` diuji pada run [#40484548650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650), selesai `success` pada 10:00:47 UTC (durasi sekitar 291 detik). Artefak teks-only #12724961702 berukuran 3.960 byte, digest ZIP SHA-256 `27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71`, belum expired saat diperiksa. Report parser menghasilkan `SINGLE_BREAKPOINT_HIT=NO`, `SINGLE_BREAKPOINT_FIRST_HIT_FRAME=UNKNOWN`, `SINGLE_BREAKPOINT_FIRST_HIT_COUNT=0`, `SINGLE_BREAKPOINT_DONE=NO`, `SINGLE_BREAKPOINT_FINAL_FRAMES=UNKNOWN`, `SINGLE_BREAKPOINT_FINAL_HITS=UNKNOWN`, `VSYNC_PROGRESS_SEEN=YES`, `DEBUGGER_CONTROL_MAX_VSYNC_FRAME=60`, dan `DEBUGGER_CONTROL_EXIT=124`. Raw log menampilkan target-probe progress frame 1–120 pada kelipatan 10; emulator exit 124 pada batas 35 detik. Semua steps lulus dan `STEP7_PRIVATE_CLEANUP=PASS`.
- `STEP7_PRIVATE_CLEANUP=PASS` terbukti pada run #40484519812, #40484548650, dan #40485987817. Ketiga cold boot ini tidak mengirim input gameplay atau memulihkan savestate; tidak ada screenshot, RAM dump, disc, BIOS, atau aset privat runtime yang ditambahkan ke Git.

### Interpretasi dan batas

Temuan historis mendukung bahwa empat breakpoint dapat memperburuk observabilitas dan satu breakpoint ber-callback minimal tetap membiarkan progress hingga frame 120. Tidak ada hit pada kandidat `0x800AD454`, sehingga PC/register/copy size/checksum source/destination tidak tersampel; base entry 0/1 tetap HIPOTESIS. **Langkah 7 tetap SEBAGIAN.** Probe kandidat seed setter `0x80035DA8` telah dilakukan terpisah untuk Step 4(a); hasil no-hit dan bug fallback report dicatat pada addendum berikutnya.


## Addendum — probe terpisah kandidat seed setter (Step 4(a), 27 Oktober 2026)

Probe runtime [#40485987817](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817) menguji **satu** breakpoint pada kandidat `0x80035DA8`, cold boot tanpa input/restore, batas target 35 detik. Source assets lolos checksum. Preflight frame 50, kontrol listener-only maksimum frame 60, target progress sampai frame 120 tanpa `STEP7_SINGLE_BP_HIT`, lalu exit 124 akibat timeout bounded. Cleanup privat `PASS`. Artefak teks #12724933081 berukuran 4.003 byte, ZIP SHA-256 `74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6`.

Report artefak dari run ini memiliki bug fallback: field `SINGLE_BREAKPOINT_PC` menyebut `0x800AD454` saat tidak ada hit. Baris raw log `STEP7_SINGLE_BP_READY targets=1 target=0x80035DA8` adalah bukti konfigurasi target yang benar. Source fallback diperbaiki pada `a6734d7fc57ff6dfab9b8135cd5661bf0278c437`; validator [#40486315324](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40486315324) lulus fixture no-hit fallback dan parser callback sintetis. Karena tidak ada hit, runtime `$a0/$ra/caller` tetap UNKNOWN. Hasil ini tidak memvalidasi base/resource loader ataupun membuktikan kandidat setter tidak pernah berjalan pada jalur lain.

Keputusan: **Step 7 tetap SEBAGIAN**. Kandidat seed setter adalah pemeriksaan tambahan yang relevan terutama ke Step 4(a); hasil no-hit bounded tidak menaikkan atau menurunkan status mapping runtime. Jangan ulangi kedua target single-breakpoint tanpa hipotesis baru.
