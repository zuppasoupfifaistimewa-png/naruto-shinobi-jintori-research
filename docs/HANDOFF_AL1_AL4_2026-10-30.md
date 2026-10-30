# Handoff AL1–AL4 — Naruto Shinobi no Sato no Jintori Gassen (30 Oktober 2026)

## Identitas dan checkpoint
- Game: Naruto – Shinobi no Sato no Jintori Gassen (PS1), SLPS-03553.
- Repo yang diizinkan: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research.
- Run final: GitHub Actions #41042679829, job ak1-ak3, conclusion success.
- Source SHA untuk run: 7e457a0ccae1fc9d499dc8d1c5020a4bab73b079.
- Commit hasil run asli: 493e6bf6bc4f2cc54c2221fe29a3e0d69ce70fd4.
- Commit addendum AL2/runtime cross-check terakhir sebelum handoff: 5f16e7c31aff56b952e3b68fc0dae2ee221836f2.
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

### AL2 — SELESAI DENGAN BATAS EVIDENCE
- Empat player record pada 0x80070EA0 + n*0xB4. Candidate ID +0x0A..+0x0C, Chakra +0x18..+0x1B; semua field ini 0 changed bytes dalam empat perbandingan.
- 0x800A3118 (RNG state) dan 0x8013A554 (pointer slot) masing-masing 0 changed bytes.
- 0x80066E7C callback/tick-like counter: 2 changed bytes pada keempat perbandingan; K4 untuk label statis, K5 hanya untuk observasi byte yang diulang runtime. Jangan nyatakan counter gameplay atau RNG.
- Runtime cross-check: 0x8013A554 berisi LE32 0x801CEF08 pada frame1/60/180/240/360 dalam kedua H6 dan kedua kontrol (K5 untuk relasi pointer yang teramati).
- Di 0x801CEF08, byte pertama 0x01 di H6 dan 0x00 di kontrol pada frame180, kedua pasangan attempt. Satu byte dialokasikan tepat ke first byte. Kelompok AK2 0x801CEF08..0x801CEF23 punya 3 changed bytes; dua byte lain tetap TIDAK TAHU. Extent dan fungsi blok tetap UNKNOWN.
- Total target-source vs H6 attempt1/2: 4.050 byte = counter 2 + TIDAK TAHU 4.048.
- Total H6 vs control attempt1/2: 56.977 byte = counter 2 + first byte block 1 + TIDAK TAHU 56.974.
- Relabel AL2 tidak menjalankan emulator baru; memakai AK2_DIFF_RANGES.tsv terkomit dan cross-check AK1_REPLAY.tsv preflight terkomit.

### AL3 — SELESAI, konsisten dua peluncuran
Target-source RAM vs H6:
- D1=390 byte berbeda.
- D60=651.
- D180=4.050.
- Dari 4.050 byte beda @180: 235 sudah beda di frame1; 3.815 pertama muncul setelah frame1.
- Sebanyak 155 posisi beda di frame1 sudah tidak berbeda lagi pada frame180.
- Kedua attempt menghasilkan angka identik.
- Target-native restore sebelumnya SIGSEGV; tidak ada pembanding runtime target murni. H6 tetap hibrida.

### AL4 — ENAM HIBRIDA REKONSTRUKSI
Input target SHA: 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d.
Input control SHA: 9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492.
Generator merekonstruksi hanya ChannelData.current (SPU field6 -> Channel field6 -> data field1 -> field8 occurrence1); biner hibrida tidak disimpan.
- ae2-target-current-all-24-control: semua 24 channel current dari control; REKONSTRUKSI SHA-256 fa3d5a21d8520259b47bb495815787f21abff425f35c595ba4065231b5f20f9a.
- ae2-current-bisect-step1: target-current channel 1–12; SHA-256 24e6270816e706662a2f5ddc68f1f0c915fb8943ba2871ad9410c5dddc1a4919.
- ae2-current-bisect-step2: target-current channel 1–6; SHA-256 3d0affe00b99f22b1d098761c306e59b9d082021f77ab09a60c6fdce29e3bacc.
- ae2-current-bisect-step3: target-current channel 1–3; SHA-256 2fd7379cc90bb0337ddf52b5b48392d04b0f69926a7fd74a2ef9aeea98c268da.
- ae2-current-bisect-step4: target-current channel 1; SHA-256 85f0010e2b6555c4c9f0010fc2e81077867a5147cc4f5ce388ded48e4b570bbe.
- ae2-current-bisect-step5: target-current channel 2; SHA-256 c810d3a4ada50d50fdd234b98ac611c56f0034af7bb1e1bc1cedf8a5c1b2ef6e.
Semua enam definisi dan hash bertanda REKONSTRUKSI; jalur cabang historis dibuktikan dari dua log per kasus. Kandidat akhir adalah channel 2.

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
- AL1–AL4 final report: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/5f16e7c31aff56b952e3b68fc0dae2ee221836f2/reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL1_AL4_FINAL_REPORT.md
- Actions summary: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/5f16e7c31aff56b952e3b68fc0dae2ee221836f2/reports/ak_2026-10-30/runs/run-41042679829/attempt-1/ACTIONS_RUN_SUMMARY.txt
- AL2 relabel table: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/5f16e7c31aff56b952e3b68fc0dae2ee221836f2/reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL2_FIELD_RELABEL.tsv
- AL2 runtime cross-check: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/5f16e7c31aff56b952e3b68fc0dae2ee221836f2/reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL2_RUNTIME_CROSSCHECK.txt
- AL3 decomposition: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/5f16e7c31aff56b952e3b68fc0dae2ee221836f2/reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL3_BYTE_DECOMPOSITION.tsv
- AL4 reconstructions: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/5f16e7c31aff56b952e3b68fc0dae2ee221836f2/reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL4_HYBRID_RECONSTRUCTIONS.tsv
