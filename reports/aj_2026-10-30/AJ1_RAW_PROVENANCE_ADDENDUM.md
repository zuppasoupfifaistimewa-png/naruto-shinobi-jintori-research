# Addendum provenance AJ1 — 30 Oktober 2026

Audit dilakukan terhadap bytes persis pada ee48de43577d08eeca77f6930d7f49a250cbba83.

## Rekonsiliasi raw, manifest, dan TSV

Direktori raw pada commit sumber mempunyai 140 berkas (70 GDB + 70 PCSX), yaitu 35 nama hibrida, masing-masing dua peluncuran GDB. Manifest lama hanya mempunyai 112 entri: 55 SHA berbeda (54 berkas GDB dan 1 berkas PCSX), dan pada 55 entri itu ukuran byte juga berbeda. Sebanyak 57 entri cocok penuh; tidak ada path dalam manifest lama yang hilang dari raw saat ini. Sebaliknya, ada 28 berkas raw saat ini yang sama sekali tidak tercantum di manifest lama. Hasil ini membuktikan bahwa raw directory, manifest, runtime-results.tsv, runtime-case-summary.tsv, dan ae4_ram_snapshots.tsv bukan satu snapshot keluaran yang konsisten.

Tujuh nama hibrida yang ada dalam raw GDB tetapi tidak memiliki SHA hibrida yang dapat dipasangkan dari TSV historis adalah: ae2-current-bisect-step1, ae2-current-bisect-step2, ae2-current-bisect-step3, ae2-current-bisect-step4, ae2-current-bisect-step5, ae2-target-current-all-24-control, dan ae2-target-spu-field6-control. Untuk 14 baris peluncuran tersebut, SHA hibrida ditulis TIDAK TAHU; SHA tidak diturunkan dari nama file atau diasumsikan dari hibrida lain.

Dari seluruh 70 raw GDB: 14 SIGSEGV, 17 mempunyai marker POST_LOAD_VSYNC=180 bersama AE_RAM_STATE_CAPTURE=PASS, dan 39 tidak mempunyai marker 180. Kode exit eksplisit tidak tersedia pada 70 log sehingga kolom exit tetap TIDAK TAHU.

## Direct Channel field 2/3

Keempat peluncuran direct-channel-field-2/3 mempunyai marker 180 dan capture PASS (60,6615–60,7331 detik sejak launch). TSV lama menandainya INCONCLUSIVE_TIMEOUT dan runtime-results.tsv historis menunjukkan wrapper -9 pada sekitar 10 detik. Kode eksperimen menguji marker 180 + capture PASS sebelum cabang SIGINT/timeout; dua keluaran itu tidak mungkin berasal dari pembacaan log identik dengan algoritme status yang sama. Tabel status lama merupakan hasil eksekusi berbeda/stale.

## AE4 RAM snapshots

Raw logs yang kini terkomit memuat marker 180 + capture PASS pada:
- ae4-ad3-field3-target-in-control: attempt 1 dan 2.
- ae4-ad3-field4-target-in-control: attempt 1 dan 2.
- ae4-ad3-field5-target-in-control: attempt 1 dan 2.
- ae4-ad3-field8-target-in-control: attempt 1 saja.

Field 8 attempt 2 dan kedua attempt field 10 tidak menunjukkan marker 180. Karena kode AE4 menambahkan baris RAM hanya sesudah marker 180, capture PASS, dan file runtime/current.sstate tersedia, tujuh log AE4 sukses di atas semestinya menghasilkan baris snapshot bila semua artefak berasal dari satu run. Namun ae4_ram_snapshots.tsv yang terkomit hanya berisi header. Jadi penjelasan yang didukung ialah TSV tersebut stale/berasal dari snapshot run berbeda; tidak benar menyimpulkan bahwa semua peluncuran AE4 gagal mencapai 180. SHA RAM/word pada peluncuran-peluncuran lama itu tidak dapat dipulihkan hanya dari log GDB teks: TIDAK TAHU.

## Asal dan mekanisme ketidakselarasan

Actions run 40966952270 attempt 1, job bisect 123773754840 (mulai 2026-10-29T22:34:57Z, selesai 2026-10-29T23:20:21Z) menerbitkan commit ee48de4. Attempt 2 job 123874229459 adalah retry publikasi yang konflik dan bukan pembuat commit tersebut. Skrip lama menulis ke satu output path statis deep/ dan membuat direktori dengan exist_ok tanpa membersihkan file lama. Beberapa invokasi dapat meninggalkan file raw dari percobaan berbeda sementara TSV/manifest hanya mencerminkan subset atau snapshot lain. Run spesifik yang menulis tiap versi log dan setiap TSV lama: TIDAK TAHU; nama file dan hash tidak menyediakan provenance per-file.

## Perubahan mitigasi

Workflow AE1 lama kini membuat reports/ae_2026-10-29/deep/runs/run-<id>/attempt-<attempt> dan hanya men-stage direktori unik tersebut. Workflow audit/H6 memakai pola run/attempt yang sama dan menurunkan tabel status langsung dari raw GDB di folder run, bukan mengandalkan runtime TSV sebelumnya. Manifest baru menulis SHA-256 dan ukuran byte untuk setiap file raw persis dari commit sumber. Tidak ada file ISO, BIOS, savestate, Memory Card, dump RAM, atau hibrida yang masuk repo.
