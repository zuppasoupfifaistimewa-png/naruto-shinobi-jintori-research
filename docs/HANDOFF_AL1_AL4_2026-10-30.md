# Handoff AL1–AL4 — Naruto Shinobi no Sato no Jintori Gassen (30 Oktober 2026)

## Identitas dan checkpoint
- Game: Naruto – Shinobi no Sato no Jintori Gassen (PS1), SLPS-03553.
- Repo yang diizinkan: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research.
- Run final: GitHub Actions #41042679829, job ak1-ak3, numeric job ID 124019605576, conclusion success.
- Source SHA untuk run: 7e457a0ccae1fc9d499dc8d1c5020a4bab73b079.
- Commit hasil run asli: 493e6bf6bc4f2cc54c2221fe29a3e0d69ce70fd4.
- Commit addendum AL2/runtime cross-check terakhir sebelum handoff: f699b73be9f2941328bcc53496ddbcf006504a52.
- H6 adalah HIBRIDA, bukan target murni: target base + top-level field 6 (SPU) dari control. H6 SHA-256: d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475.

## Putusan AL
Semua hasil yang diminta pada tugas AL tersedia. Ringkasan Actions berstatus PASS, JOB=ak1-ak3, EXIT_CODE=0.

### AL1 — LULUS
- Empat peluncuran: H6 attempt1/2 dan CONTROL_NOT_TARGET attempt1/2.
- Setiap peluncuran menangkap POST_LOAD_VSYNC 1, 60, 180, 240, 360.
- PCSX.quit(0) dipanggil langsung di callback capture frame360, tanpa nextTick bersarang kedua.
- Keempat log GDB menunjukkan marker pemanggilan dan [Inferior ... exited normally]; parser final merekam exit emulator 0 desimal dari sumber GDB.
- Watchdog frame1200 tidak muncul pada keempat peluncuran.
- Baseline H6 2 MiB pada kedua attempt cocok dengan AK1:
  - frame180: 4c964aaca0afccc68317acd0726fec680c305b903cd426e70afe3d8ac1f1e741
  - frame240: 16880faeccfca1fbd42d199c1543b00ec8a065bcd53545d14ea4657c9a6c2d5c
  - frame360: a9ac5282e9fb9ad1e77f46ef0c291af8e7e5f27b477b6b31e319f971e7dd9942
- Waktu-ke-frame360 terlama: 98.708170175552 detik. Timeout per peluncuran 600 detik; batas >=2x terpenuhi.
- Penyebab internal kenapa pola nested nextTick pada kode AK lama tidak berlaku: TIDAK TAHU. Log lama menunjukkan watchdog pada frame1200 dan GDB exited with code 065; 065 adalah oktal = 53 desimal. Log lama tidak memiliki marker sebelum/sesudah callback bersarang. Perbaikan direct-call terbukti; akar sebab historis tidak boleh ditebak.

### AL2 — DIKOREKSI AM1 (tanpa peluncuran emulator)
- Sumber: AK1_REPLAY.tsv dan AK2_DIFF_RANGES.tsv dari run #41042679829; job ak1-ak3, ID 124019605576; source SHA 7e457a0ccae1fc9d499dc8d1c5020a4bab73b079; output commit run 493e6bf6bc4f2cc54c2221fe29a3e0d69ce70fd4.
- P0 Chakra 0x80070EB8: H6 0x5DC (DC 05 00 00) vs kontrol 0x564 (64 05 00 00) = 1 byte berbeda, K5.
- P1 Chakra 0x80070F6C: sama = 1 byte berbeda, K5.
- RNG 0x800A3118: H6 0x06CF4B77 (77 4B CF 06) vs kontrol 0x1962C6BB (BB C6 62 19) = 4 byte berbeda, K5.
- Candidate ID P0–P3=0; Chakra P2/P3=0; pointer slot 0; block first byte 1; callback/tick-like counter 2.
- H6/control attempt1 dan attempt2 masing-masing total 56,977 = field known 9 + TIDAK TAHU 56,968.
- Target-source/H6 attempt1 dan attempt2 masing-masing total 4,050 = callback/tick-like 2 + TIDAK TAHU 4,048; semua label Chakra/RNG lainnya 0.
- K5 hanya menyatakan pengamatan byte runtime berulang pada dua attempt; fungsi gameplay tetap TIDAK TAHU. Dua byte lain di grup 0x801CEF08..0x801CEF23 tetap tak terlokasi.
- Cakupan digest: ram_2mib_sha256 menghitung first 2 MiB (RAM_BYTES=0x200000). ram_segment_bytes=8,388,608 adalah panjang field RAM hasil decode; bukan bytes yang di-hash. Apakah 8 MiB itu mirror 2 MiB: TIDAK TAHU. Nama kolom tepat, tidak diganti.

### AL3 — SELESAI, konsisten dua peluncuran
Target-source RAM vs H6:
- D1=390 byte berbeda.
- D60=651.
- D180=4.050.
- Dari 4.050 byte beda @180: 235 sudah beda di frame1; 3.815 pertama muncul setelah frame1.
- Sebanyak 155 posisi beda di frame1 sudah tidak berbeda lagi pada frame180.
- Kedua attempt menghasilkan angka identik.
- Target-native restore sebelumnya SIGSEGV; tidak ada pembanding runtime target murni. H6 tetap hibrida.

### AL4 — REKONSTRUKSI ENAM HIBRIDA
Input target SHA: 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d.
Input control SHA: 9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492.
Generator merekonstruksi hanya ChannelData.current (SPU field6 -> Channel field6 -> data field1 -> field8 occurrence1); biner hibrida tidak disimpan.
- ae2-target-current-all-24-control: semua 24 channel current dari control; REKONSTRUKSI SHA-256 fa3d5a21d8520259b47bb495815787f21abff425f35c595ba4065231b5f20f9a.
- ae2-current-bisect-step1: target-current channel 1–12; SHA-256 24e6270816e706662a2f5ddc68f1f0c915fb8943ba2871ad9410c5dddc1a4919.
- ae2-current-bisect-step2: target-current channel 1–6; SHA-256 3d0affe00b99f22b1d098761c306e59b9d082021f77ab09a60c6fdce29e3bacc.
- ae2-current-bisect-step3: target-current channel 1–3; SHA-256 2fd7379cc90bb0337ddf52b5b48392d04b0f69926a7fd74a2ef9aeea98c268da.
- ae2-current-bisect-step4: target-current channel 1; SHA-256 85f0010e2b6555c4c9f0010fc2e81077867a5147cc4f5ce388ded48e4b570bbe.
- ae2-current-bisect-step5: target-current channel 2; SHA-256 c810d3a4ada50d50fdd234b98ac611c56f0034af7bb1e1bc1cedf8a5c1b2ef6e.
Semua enam definisi dan hash bertanda REKONSTRUKSI; jalur cabang historis dibuktikan dari dua log per kasus. Kandidat akhir adalah channel 2. Status AL4 adalah REKONSTRUKSI, bukan hasil asli atau bukti gameplay.

## Skala K0–K5
K0 tidak ada bukti/unknown; K1 petunjuk tunggal belum diverifikasi; K2 observasi eksplisit satu artefak/log; K3 beberapa artefak statis konsisten; K4 pemetaan/struktur statis dapat direproduksi (maksimum untuk statis); K5 runtime memenuhi kriteria dan berulang pada >=2 peluncuran independen.

## Batas dan larangan yang tetap berlaku
- Host/RSI tetap DIPARKIR.
- Hasil AL bukan bukti Story Mode tamat. Story Mode belum dinyatakan selesai.
- Repo tetap satu-satunya repo proyek yang digunakan.
- Tidak ada ISO, BIOS, savestate, Memory Card, dump RAM mentah, atau biner hibrida dikomit. Job cleanup Actions sukses.
- Jangan mengubah Release atau visibilitas repo.
- Bila chat baru dibuka, baca handoff ini terlebih dahulu beserta laporan AL final; jangan mengulang run AL tanpa alasan baru.

## Raw permalink untuk checkpoint laporan
Semua URL di bawah adalah raw permalink dengan SHA commit penuh:
- AL1–AL4 final report: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/f699b73be9f2941328bcc53496ddbcf006504a52/reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL1_AL4_FINAL_REPORT.md
- Actions summary: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/f699b73be9f2941328bcc53496ddbcf006504a52/reports/ak_2026-10-30/runs/run-41042679829/attempt-1/ACTIONS_RUN_SUMMARY.txt
- AL2 relabel table: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/f699b73be9f2941328bcc53496ddbcf006504a52/reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL2_FIELD_RELABEL.tsv
- AL2 runtime cross-check: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/f699b73be9f2941328bcc53496ddbcf006504a52/reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL2_RUNTIME_CROSSCHECK.txt
- AL3 decomposition: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/f699b73be9f2941328bcc53496ddbcf006504a52/reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL3_BYTE_DECOMPOSITION.tsv
- AL4 reconstructions: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/f699b73be9f2941328bcc53496ddbcf006504a52/reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL4_HYBRID_RECONSTRUCTIONS.tsv

## AM2 — hasil analisis LCG (tanpa emulator)
Input: AK1_REPLAY.tsv dari run 41042679829 (output commit 493e6bf6bc4f2cc54c2221fe29a3e0d69ce70fd4); H6 SHA d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475. Nilai RNG 0x800A3118 di frame 1/60/180/240/360 sama dengan 0x06CF4B77 pada kedua attempt. Delapan transisi berurutan menghasilkan k minimum 0 (state before=after); skrip tetap mendukung pencarian sampai 2^24. Tidak ada penafsiran gameplay.

## AM3 — CIRCLE timing A/B headless replay (TUNTAS, K5)
- Run berhasil: 41048937290; job `am3-h6-circle-ab`; ID job numerik 124039892346; conclusion success; kode keluar skrip 0.
- Source commit runner: 4fbbbdf278ca71e0c84cb651287096561e9b4878.
- Commit publikasi hasil: 51a66a060f3d4efda7eac7ada408b8d8ac88fe4c.
- H6 SHA-256 d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475 (hybrid, bukan target murni).
- Empat peluncuran valid (A attempt1/2, B attempt1/2); seluruh 20 capture pada frame 1/60/180/240/360 PASS. Setiap peluncuran mencatat tombol CIRCLE press dan release dengan readback PASS, PCSX.quit(0), serta GDB exited normally (kode emulator desimal 0). Watchdog tidak muncul.
- A: CIRCLE press frame 60/release 61; dua launch RAM SHA identik pada semua lima frame.
- B: CIRCLE press frame 90/release 91; dua launch RAM SHA identik pada semua lima frame.
- A vs B: RAM SHA sama pada frame 1 dan 60; berbeda pertama pada frame 180; tetap berbeda di 240 dan 360. Ini observasi RAM runtime pada H6 hybrid, bukan interpretasi gameplay.
- SHA RAM mencakup 2 MiB pertama (base 0x80000000); `ram_segment_bytes=8388608` adalah panjang field RAM hasil decode (8 MiB), bukan bytes yang di-hash. Mirror 8 MiB tetap TIDAK TAHU.
- Waktu-ke-frame360 maksimum 142.59486198425 detik; timeout per launch 600 detik (>=2x). Cleanup ISO/BIOS/Memory Card/savestate/RAM/emulator sementara berhasil.
- Batas eksperimen: runner memakai satu file Memory Card referensi yang sama untuk empat launch dan tidak mencatat hash sebelum/sesudah. Karena itu perbedaan A/B adalah hasil sampel yang nyata, tetapi penyebab eksklusifnya tidak dikunci pada timing tombol saja; isolasi Memory Card per launch diperlukan untuk klaim kausal lebih kuat.
- Percobaan awal AM3 run 41048752354, job ID 124039280097, gagal sebelum emulator karena HTTP 401 dari ekspresi workflow yang ter-escape; kode keluar 22; emulator launches=0. Kesalahan diperbaiki pada source commit 4fbbb...; tidak mencemari hasil run sukses.

### AM3 hasil per frame (SHA-256 first 2 MiB)
| Frame pasca-load | A (CIRCLE f60) | B (CIRCLE f90) | A vs B |
|---:|---|---|---|
| 1 | 418c0566904bab0fa777f99a1a446c5526d2392cb07821b144c75045e820be8e | 418c0566904bab0fa777f99a1a446c5526d2392cb07821b144c75045e820be8e | sama |
| 60 | 8de5a60f4610845fc918111e727703b1a271dfb14484198c67d3e080d59ba53f | 8de5a60f4610845fc918111e727703b1a271dfb14484198c67d3e080d59ba53f | sama |
| 180 | 0506518f28d38e560ddd6dc183f87c428353678c5f51f1f61bd541970f03f736 | a856bc6ec6ac3a7e8b94956373585f767eb023f0945f600b95db9041e7e9b219 | berbeda |
| 240 | 1c149e3b658d734c2bcf0965ac3d2c0896878c848db3ef43c4c5968041a53549 | d52662110e77cde9dd9f3753039577d9eea17743bfa6318fafd1d89dfd465297 | berbeda |
| 360 | d1418071ebbc9ae17f5cb8a7dbcd16ee89bafe0d6a53a979ece5713bf38fc192 | c6e6aed802da200798cc7c0319903f7d90c2b69e1595e14d79f73484c9c88d97 | berbeda |

Word yang tercatat pada semua capture AM3:
- 0x80070EB8 = 0x000005DC (bytes DC 05 00 00)
- 0x80070F6C = 0x000005DC (bytes DC 05 00 00)
- 0x800A3118 = 0x06CF4B77 (bytes 77 4B CF 06)
- 0x8013A554 = 0x801CEF08 (bytes 08 EF 1C 80)

Raw permalink hasil AM3 (commit publikasi penuh):
- ACTIONS_RUN_SUMMARY.txt: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/51a66a060f3d4efda7eac7ada408b8d8ac88fe4c/reports/am_2026-10-30/runs/run-41048937290/attempt-1/ACTIONS_RUN_SUMMARY.txt
- AM3_COMPARISON_SUMMARY.txt: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/51a66a060f3d4efda7eac7ada408b8d8ac88fe4c/reports/am_2026-10-30/runs/run-41048937290/attempt-1/AM3_COMPARISON_SUMMARY.txt
- AM3_REPLAY.tsv: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/51a66a060f3d4efda7eac7ada408b8d8ac88fe4c/reports/am_2026-10-30/runs/run-41048937290/attempt-1/AM3_REPLAY.tsv

## Putusan AM dan batas proyek
- AM1=TUNTAS; AM2=TUNTAS; AM3=TUNTAS pada cakupan H6 hybrid sebagaimana batas di atas.
- AL4 tetap REKONSTRUKSI.
- Story Mode belum dinyatakan tamat. Tidak ada bukti tamat yang diajukan oleh AM1–AM3.
- Jangan mengulang AM1–AM3 atau AL1–AL4 yang sudah benar. Langkah lanjutan yang relevan adalah memperbaiki batas MCD pada uji kausal berikutnya atau melanjutkan riset lain yang belum terverifikasi; jangan memakai hasil H6 sebagai target-native proof.


## Errata AN1 — 30 Oktober 2026

- Hitungan sementara H6 vs CONTROL sebesar 3 byte diketahui + 56.974 byte TIDAK TAHU sudah superseded. Koreksi AM1 yang benar pada masing-masing dari dua attempt adalah **9 byte diketahui/berlabel + 56.968 byte TIDAK TAHU = 56.977 byte berbeda**. Angka 9 adalah byte berbeda yang dapat dipetakan ke label, bukan byte identik/tidak berubah. Rincian label serta batas semantik mengikuti laporan AM1.
- Run gagal #41048752354: job `am3-h6-circle-ab`, ID numerik 124039280097, source SHA `240c448205b047f6dcbcb475c8f8b9cfca20c30a`; commit keluaran ringkasan bot `123654ee3a2159befb477980286d460313a61420` (short `123654e`); setup HTTP 401, kode keluar 22, emulator tidak diluncurkan.
- Commit `4fbbbdf278ca71e0c84cb651287096561e9b4878` adalah perbaikan workflow, bukan output commit run gagal tersebut. Run sukses AM3 #41048937290 dipublikasikan pada `51a66a060f3d4efda7eac7ada408b8d8ac88fe4c`.
- H6 tetap hybrid (target base + SPU top-level field 6 dari CONTROL), bukan target murni. Story Mode tidak diklaim tamat.
