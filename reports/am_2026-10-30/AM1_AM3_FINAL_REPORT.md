# Laporan akhir AM1–AM3 — Naruto: Shinobi no Sato no Jintori Gassen (SLPS-03553)
Tanggal: 30 Oktober 2026
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

## Ringkasan status
| Butir | Status | K | Hasil |
|---|---|---:|---|
| AM1 — koreksi AL2 dan cakupan digest | TUNTAS | K5 untuk nilai byte H6/control; K4 untuk field mapping | Dua word Chakra masing-masing 1 byte berubah; RNG 4 byte berubah; total empat comparison direkonsiliasi. SHA RAM menghitung 2 MiB, field RAM hasil decode 8 MiB. |
| AM2 — jumlah langkah LCG | TUNTAS | K5 untuk sampel RNG yang direplikasi; hasil aritmetika deterministik | 8/8 transisi bernilai k minimum 0 karena state sebelum/sesudah identik 0x06CF4B77. |
| AM3 — PCSX-Redux H6 CIRCLE A/B | TUNTAS | K5 untuk replay H6 yang direplikasi dua launch per jadwal | A dan B masing-masing deterministik pada lima frame sampel; A vs B berbeda pertama kali di frame 180. |

K0 dipakai untuk informasi yang tidak terbukti; sisa byte yang belum dapat ditempatkan tetap TIDAK TAHU. Story Mode TIDAK dinyatakan tamat. H6 bukan target murni.

## AM1 — koreksi AL2 (tanpa emulator)
Sumber: AK1_REPLAY.tsv dan AK2_DIFF_RANGES.tsv, run #41042679829, job ak1-ak3, ID job 124019605576, source SHA 7e457a0ccae1fc9d499dc8d1c5020a4bab73b079, output commit asal 493e6bf6bc4f2cc54c2221fe29a3e0d69ce70fd4. AM1 tidak meluncurkan emulator.

- 0x80070EB8 / P0 Chakra: H6 0x5DC = DC 05 00 00; control 0x564 = 64 05 00 00; tepat 1 byte berbeda, K5.
- 0x80070F6C / P1 Chakra: nilai dan byte sama seperti di atas; tepat 1 byte berbeda, K5.
- 0x800A3118 / RNG: H6 0x06CF4B77 = 77 4B CF 06; control 0x1962C6BB = BB C6 62 19; tepat 4 byte berbeda, K5.
- Candidate-ID P0–P3=0; Chakra P2/P3=0; pointer slot 0x8013A554=0; block first byte 0x801CEF08=1; callback/tick-like 0x80066E7C=2. K5 pada byte runtime yang diulang; makna gameplay setiap field tetap TIDAK TAHU.

Empat total (label known + TIDAK TAHU = total):
1. H6 attempt1 vs control attempt1: 9 + 56.968 = 56.977 byte.
2. H6 attempt2 vs control attempt2: 9 + 56.968 = 56.977 byte.
3. Target source vs H6 attempt1: 2 + 4.048 = 4.050 byte.
4. Target source vs H6 attempt2: 2 + 4.048 = 4.050 byte.

Cakupan digest: RAM_BYTES=0x200000; ram_2mib_sha256 menghitung 2 MiB pertama. ram_segment_bytes=8388608 hanya panjang field RAM hasil decode (8 MiB), bukan cakupan SHA. Apakah segmen 8 MiB merupakan mirror 2 MiB: TIDAK TAHU. Nama kolom benar dan tidak diganti.

Commit koreksi AM1: f699b73be9f2941328bcc53496ddbcf006504a52.
Berkas berubah pada commit AM1:
- reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL2_FIELD_RELABEL.tsv
- reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL2_RELABEL_NOTES.txt
- reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL2_RUNTIME_CROSSCHECK.txt
- reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AL1_AL4_FINAL_REPORT.md
- docs/HANDOFF_AL1_AL4_2026-10-30.md
- experiments/am2_rng_lcg.py
- reports/am_2026-10-30/AM2_RNG_LCG_RESULTS.tsv
- reports/am_2026-10-30/AM2_RNG_LCG_REPORT.md
- experiments/AM3_INPUT_SCHEDULE.tsv

## AM2 — LCG (tanpa emulator)
Input: AK1_REPLAY.tsv dari run 41042679829; kedua attempt H6 memiliki RNG 0x800A3118=0x06CF4B77 pada frame 1, 60, 180, 240, 360.
Mult=0x41C64E6D, add=0x3039, state 32-bit. Untuk delapan pasangan frame berurutan:
- attempt1: 1→60, 60→180, 180→240, 240→360: k=0 masing-masing.
- attempt2: 1→60, 60→180, 180→240, 240→360: k=0 masing-masing.
Alasan: S_after identik dengan S_before; k=0 adalah nilai minimum. Batas pencarian skrip 2^24; tidak ada interpretasi gameplay.

SHA-256 skrip: b1e000e8d3a592018674a1b465b718754a0fca9d1aa000d086fedd97d5f7c2e6.
SHA-256 output TSV (dikoreksi dan diverifikasi): 96835dc15c7a04783ea32cf8f74ccff52fc443d4108d73b1fc9c32007a689e52.

## AM3 — runtime PCSX-Redux headless, H6 hybrid
H6 SHA-256=d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475. Bukan target murni.

Workflow run 1 (gagal sebelum emulator):
- run 41048752354; job ID 124039280097; source commit 240c448205b047f6dcbcb475c8f8b9cfca20c30a.
- Gagal HTTP 401 karena ekspresi workflow GitHub Actions ter-escape; exit code 22; emulator launches=0. Cleanup berhasil.
Workflow diperbaiki pada commit 4fbbbdf278ca71e0c84cb651287096561e9b4878.

Workflow run 2 (hasil final):
- run 41048937290; job am3-h6-circle-ab; ID job numerik 124039892346; conclusion success.
- source commit 4fbbbdf278ca71e0c84cb651287096561e9b4878.
- output commit 51a66a060f3d4efda7eac7ada408b8d8ac88fe4c.
- timeout per peluncuran 600 detik; maksimum waktu-ke-frame360 142.59486198425 detik; syarat >=2x terpenuhi.
- Empat launch valid; 20/20 capture PASS; CIRCLE press/release readback PASS di empat launch; semua emulator exit desimal 0; watchdog tidak muncul; cleanup berhasil.
- RAM hash selalu atas 2 MiB pertama pada base 0x80000000; ram_segment_bytes=8388608 menunjukkan panjang field decode 8 MiB.

### Putusan determinisme
A (CIRCLE frame60, release61): dua launch identik pada frame 1,60,180,240,360.
B (CIRCLE frame90, release91): dua launch identik pada semua frame sampel.
A vs B: SHA sama pada frame1 dan60; berbeda pertama kali pada frame180; tetap berbeda pada frame240 dan360.

| Frame | A (2 launch identik) | B (2 launch identik) | A vs B |
|---:|---|---|---|
| 1 | 418c0566904bab0fa777f99a1a446c5526d2392cb07821b144c75045e820be8e | 418c0566904bab0fa777f99a1a446c5526d2392cb07821b144c75045e820be8e | sama |
| 60 | 8de5a60f4610845fc918111e727703b1a271dfb14484198c67d3e080d59ba53f | 8de5a60f4610845fc918111e727703b1a271dfb14484198c67d3e080d59ba53f | sama |
| 180 | 0506518f28d38e560ddd6dc183f87c428353678c5f51f1f61bd541970f03f736 | a856bc6ec6ac3a7e8b94956373585f767eb023f0945f600b95db9041e7e9b219 | berbeda |
| 240 | 1c149e3b658d734c2bcf0965ac3d2c0896878c848db3ef43c4c5968041a53549 | d52662110e77cde9dd9f3753039577d9eea17743bfa6318fafd1d89dfd465297 | berbeda |
| 360 | d1418071ebbc9ae17f5cb8a7dbcd16ee89bafe0d6a53a979ece5713bf38fc192 | c6e6aed802da200798cc7c0319903f7d90c2b69e1595e14d79f73484c9c88d97 | berbeda |

Word yang diamati pada semua sampel AM3:
- 0x80070EB8=0x000005DC
- 0x80070F6C=0x000005DC
- 0x800A3118=0x06CF4B77
- 0x8013A554=0x801CEF08

Batas desain: satu file Memory Card referensi yang sama digunakan untuk empat launch; tidak ada hash pra/pasca tiap launch. Maka A vs B memang berbeda pada RAM yang disampling, tetapi timing-only causality belum terkunci; uji kausal lebih kuat perlu copy Memory Card identik terpisah per launch dan checksum pra/pasca.

## Status akhir
- AM1=TUNTAS, K5 untuk byte H6/control berulang; byte yang tidak terlokasi K0/TIDAK TAHU.
- AM2=TUNTAS, K5 pada input RNG yang diulang; k minimum 0 untuk semua transisi.
- AM3=TUNTAS, K5 untuk pola runtime H6 yang diulang pada dua launch per jadwal; A vs B beda pertama di frame180.
- AL4=REKONSTRUKSI.
- Story Mode belum dinyatakan tamat; AM1–AM3 bukan bukti Story Mode tamat.
- Tidak ada ISO, BIOS, Memory Card, savestate, dump RAM mentah, atau biner hybrid dikomit. Output publik hanya teks/log.


## Errata AN1 — koreksi hitungan H6/CONTROL dan identitas Actions

- Angka sementara 3 byte diketahui + 56.974 byte TIDAK TAHU dicabut. Nilai yang benar setelah AM1 untuk masing-masing dari dua comparison H6-vs-control adalah **9 byte diketahui/berlabel + 56.968 byte TIDAK TAHU = 56.977 byte berbeda**. Kata “tidak berubah” tidak menggambarkan nilai 9 tersebut; itu adalah byte delta yang dapat diberi label.
- Run gagal 41048752354 memakai job `am3-h6-circle-ab`, ID `124039280097`, source SHA `240c448205b047f6dcbcb475c8f8b9cfca20c30a`. Output summary dipublikasikan bot sebagai commit `123654ee3a2159befb477980286d460313a61420` (`123654e`); setup gagal HTTP 401 dengan exit code 22 sebelum emulator diluncurkan.
- Commit `4fbbbdf278ca71e0c84cb651287096561e9b4878` adalah perbaikan workflow. Output run sukses AM3 41048937290 adalah commit `51a66a060f3d4efda7eac7ada408b8d8ac88fe4c`.
- H6 tetap hybrid, bukan target murni. Story Mode tidak dinyatakan tamat.
