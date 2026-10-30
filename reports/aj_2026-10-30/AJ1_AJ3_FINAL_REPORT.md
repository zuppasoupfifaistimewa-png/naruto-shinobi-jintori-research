# Laporan akhir AJ1–AJ3 — Naruto Jintori SLPS-03553 — 30 Oktober 2026

## Status eksekusi

- AJ1: selesai, K4 (bukti statis dari bytes commit dapat diperiksa ulang).
- AJ2 H6: selesai, K5 (dua peluncuran runtime independen mencapai POST_LOAD_VSYNC=180 dan capture RAM).
- AJ3: baseline H6 identik pada dua peluncuran; pencarian host/RSI tidak diparkir, tetapi dibatasi ke A/B terkendali. Hubungan kausal host/RSI tetap TIDAK TAHU.

## AJ1 — audit bytes pada ee48de4

Sumber tepat: commit ee48de43577d08eeca77f6930d7f49a250cbba83, direktori reports/ae_2026-10-29/deep/raw. Ada 70 log GDB dan 70 log PCSX (35 nama hibrida × dua peluncuran). Tabel semua 70 baris ada di AJ1_RAW_GDB_TABLE.tsv; manifest baru mencantumkan SHA-256 dan ukuran byte setiap satu dari 140 file.

Hasil parse 70 log GDB: 14 SIGSEGV, 17 POST_LOAD_VSYNC=180 + AE_RAM_STATE_CAPTURE=PASS, 39 tanpa marker 180. Exit code eksplisit tidak tercatat pada log GDB, sehingga kolom exit tiap baris adalah TIDAK TAHU. Tujuh nama hibrida tidak mempunyai hash yang bisa dipasangkan dengan TSV historis: ae2-current-bisect-step1 sampai step5, ae2-target-current-all-24-control, dan ae2-target-spu-field6-control; 14 barisnya diberi TIDAK TAHU, bukan direkayasa.

Manifest lama mempunyai 112 entri. Dari jumlah itu, 55 SHA tidak cocok (54 GDB + 1 PCSX), dan ukuran byte pada 55 entri itu juga berbeda; 57 entri cocok penuh. Tidak ada path lama yang hilang, tetapi ada 28 file raw tambahan yang tidak tercantum di manifest lama. Penyebab umum yang terdukung oleh kode ialah output path lama statis (deep/) dipakai ulang tanpa pembersihan; file raw dapat berasal dari beberapa invokasi, sedangkan runtime TSV dan manifest bisa tertinggal pada snapshot berbeda. Run yang menulis setiap versi file satu-per-satu: TIDAK TAHU.

Direct-channel-field-2 dan direct-channel-field-3 masing-masing memiliki dua log dengan marker frame 180 + capture PASS, pada 60,6615–60,7331 detik. Status INCONCLUSIVE_TIMEOUT lama berasal dari TSV eksekusi lain yang menunjukkan wrapper -9 sekitar 10 detik. Kode eksperimen memeriksa marker + capture sebelum cabang SIGINT/timeout; karena itu satu log yang mengandung kedua marker tidak akan dilabel INCONCLUSIVE_TIMEOUT oleh urutan kode yang sama.

Koreksi penting untuk interpretasi ae4_ram_snapshots.tsv: TSV yang terkomit hanya header, tetapi raw GDB AE4 sebenarnya menunjukkan tujuh launch capture PASS pada frame 180 (field3, field4, field5 masing-masing attempt 1/2; field8 attempt 1). Field8 attempt 2 dan dua field10 tidak mempunyai marker. Karena kode hanya menambahkan baris setelah marker, capture PASS, dan file current.sstate tersedia, tujuh launch tersebut semestinya menghasilkan baris jika raw dan TSV berasal dari eksekusi yang sama. Jadi TSV header-only stale/berasal dari snapshot lain, bukan bukti bahwa seluruh AE4 tidak menangkap RAM. Hash RAM AE4 lama: TIDAK TAHU.

## Pembuat ee48de4 dan perbaikan publikasi

Commit ee48de4 diterbitkan oleh Actions run 40966952270 attempt 1, workflow AE1-AE4 recursive SPU bisect, job bisect ID 123773754840. head_sha sumber run: 19d26af1a91e273b5c3bb2717af5032823239b09. Run mulai 2026-10-29T22:34:53Z; job mulai 22:34:57Z dan selesai 23:20:21Z. Log mencatat commit 5b188ce, rebase sukses, lalu AE1_DEEP_EVIDENCE_HEAD=ee48de4 pada 23:20:18Z. Attempt 2/job 123874229459 adalah retry publikasi terpisah yang gagal rebase karena konflik, bukan pembuat commit ee48de4.

Workflow AE1 lama diperbaiki agar menulis ke reports/ae_2026-10-29/deep/runs/run-<id>/attempt-<attempt> dan hanya men-stage folder unik tersebut. Workflow AJ1/H6 yang baru memakai pola run/attempt yang sama dan membuat ringkasan dari raw log per run. Tidak ada status Release yang diubah.

## AJ2 — H6 dua peluncuran headless

H6 dibentuk dari target checkpoint SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d, dengan hanya top-level field 6 (SPU) diganti oleh field 6 dari control SHA-256 9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492. Label: target-base + SPU field-6 control; BUKAN target murni. Hibrida sementara 21,163,? bytes tidak dikomit; fingerprint hibridanya diverifikasi sebagai SHA-256 64 karakter:
d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475.

Runtime pin PCSX-Redux 0c3572c3d, no-input, dua proses independen. Timeout masing-masing 180 detik. Waktu tercepat/terlama historis untuk H6 frame 180: hingga 62,745 detik; batas minimal yang diminta 2 × 62,745 + 30 = 155,490 detik. Timeout 180 detik memenuhi batas. Dua peluncuran baru mencapai POST_LOAD_VSYNC=180 dan AE_H6_RAM_CAPTURE=PASS pada:
- Attempt 1: 70,561992883682 detik sejak launch.
- Attempt 2: 70,531628608704 detik sejak launch.

Target savestate:
- RAM field bytes: 8.388.608.
- SHA-256 first 2 MiB: 3ad7b85c857a868d91df4b3f1049c23889a0dc482ad7ee390ac8b6c05c3190f4.

H6 pada masing-masing peluncuran:
- RAM field bytes: 8.388.608.
- SHA-256 first 2 MiB: 4c964aaca0afccc68317acd0726fec680c305b903cd426e70afe3d8ac1f1e741.
- Kedua SHA H6 2 MiB identik: YA.

Tiga word pada savestate target dan pada kedua H6 sama:
- 0x80070EB8: bytes dc 05 00 00; LE32 0x000005DC (1500).
- 0x80070F6C: bytes dc 05 00 00; LE32 0x000005DC (1500).
- 0x8013A554: bytes 08 ef 1c 80; LE32 0x801CEF08.

Walaupun tiga word cocok, SHA RAM 2 MiB target berbeda dari H6. Jadi target RAM penuh tidak identik dengan H6; hanya tiga alamat terpilih cocok.

Kedua wrapper timeout berakhir dengan return code -9 setelah wall time sekitar 185,003/185,004 detik (180 detik + grace 5 detik). Emulator exit code normal tidak ditemukan di log: TIDAK TAHU. Karena marker 180 dan file capture PASS sudah ada pada kedua peluncuran, hasil snapshot RAM tetap sah untuk perbandingan frame yang diminta; -9 tidak dilabel SIGSEGV. Skrip analisis H6 keluar 0; Actions job run 41028457166/job 123972149171 berkesimpulan success dan mempublikasikan summary.

## AJ3 — rencana dan putusan

Dua launch H6 yang berbeda menghasilkan SHA 2 MiB dan ketiga word identik pada frame post-load 180, memenuhi K5 awal untuk repeatability H6. Lanjutkan dengan sedikitnya tiga replay tambahan sambil membekukan kedua savestate sumber, hash H6, emulator pin, BIOS/ISO/Card, flags, headless display dan no-input; bandingkan bytes RAM 2 MiB dan ketiga word. Setelah baseline tetap identik, lakukan A/B satu variabel host/RSI per kondisi dengan minimal dua launch per kondisi dan catat delta RAM penuh. Putusan: pencarian basis RAM SPU host/RSI TIDAK DIPARKIR, tetapi hanya sebagai A/B terkendali; apakah host/RSI benar-benar menentukan basis RAM SPU tetap TIDAK TAHU sampai variabel itu diisolasi dan hasilnya direplikasi.

## Artefak yang dikomit

- AJ1_RAW_GDB_TABLE.tsv — seluruh tabel per hibrida × launch.
- COMMITTED_RAW_MANIFEST.sha256.txt — manifest baru untuk 140 file raw persis pada ee48de4.
- OLD_MANIFEST_MISMATCHES.tsv — rincian 55 mismatch.
- AJ1_AUDIT_REPORT.md dan AJ1_RAW_PROVENANCE_ADDENDUM.md — penjelasan ketidakselarasan manifest/TSV.
- H6_TWO_LAUNCH_RAM.tsv dan H6_RUNTIME_EVIDENCE.txt — hasil dua peluncuran H6 dan perbandingan target.
- ACTIONS_RUN_SUMMARY.txt — status, job, SHA, timeout dan exit wrapper per launch.
- H6_HYBRID_IDENTITY.sha256.txt — fingerprint teks saja.
- AJ3_REPLAY_DETERMINISM_PLAN.md — rencana replay determinism/host-RSI.

Tidak ada ISO, BIOS, savestate, Memory Card, dump RAM, atau file hibrida biner yang dikomit.
