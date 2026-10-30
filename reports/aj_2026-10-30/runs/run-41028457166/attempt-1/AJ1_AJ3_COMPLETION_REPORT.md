# AJ1–AJ3 — laporan final audit AE1 dan uji H6

Tanggal: 30 Oktober 2026. Sumber audit statis: commit ee48de43577d08eeca77f6930d7f49a250cbba83. Actions runtime H6: run 41028457166, attempt 1, job h6 / ID 123972149171. Workflow result: success; skrip H6 exit 0.

## AJ1 — log mentah dan provenance

Tabel lengkap AJ1_RAW_GDB_TABLE.tsv memuat 70 baris GDB: 35 hibrida × dua peluncuran. Setiap baris berisi nama hibrida, SHA-256 hibrida (atau TIDAK TAHU), hasil raw GDB, elapsed_since_launch_s (atau TIDAK TAHU), kode keluar eksplisit di raw log (atau TIDAK TAHU), SHA-256 log, ukuran byte, dan path.

Hasil parse mentah: 14 SIGSEGV; 17 POST_LOAD_VSYNC=180 + AE_RAM_STATE_CAPTURE; 39 tanpa marker frame 180. Tidak ada kode keluar akhir yang tertulis eksplisit di 70 log GDB, jadi kolom exit tetap TIDAK TAHU; tidak diganti dengan exit wrapper dari tabel lama.

**direct-channel-field-2** — SHA-256 hibrida 2e67da72470863953558d33180ed859a36745dd84ab1586975b60e8753f4a39c (64 karakter). Attempt 1: marker 180 + capture PASS, elapsed 60.733078241348 s, exit TIDAK TAHU. Attempt 2: marker 180 + capture PASS, elapsed 60.71901845932 s, exit TIDAK TAHU.

**direct-channel-field-3** — SHA-256 hibrida e5612c3c625b3ac29bf197ed9b652610e0f6d2a1b71d69c9dec02d2e3dcfe1d7 (64 karakter). Attempt 1: marker 180 + capture PASS, elapsed 60.67808175087 s, exit TIDAK TAHU. Attempt 2: marker 180 + capture PASS, elapsed 60.661514043808 s, exit TIDAK TAHU.

SHA H6 untuk dua baris AE2 telah dipulihkan dari rekaman digest yang terkomit pada reports/ae_2026-10-29/runtime-results.tsv: d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475. Masih ada 12 baris TIDAK TAHU (enam hibrida × dua peluncuran: ae2-current-bisect-step1..5 dan ae2-target-current-all-24-control), karena tidak ada rekaman SHA hibrida yang dapat dipasangkan di TSV terkomit. Tidak ada hash yang ditebak.

### Mengapa direct-field-2/3 sebelumnya INCONCLUSIVE_TIMEOUT

Skrip experiments/ae1_channel_fields_bisect.py mengklasifikasikan marker AE_POST_LOAD_VSYNC=180 + AE_RAM_STATE_CAPTURE=PASS sebelum memeriksa SIGINT/timeout. Maka raw GDB yang berisi dua marker sukses tidak mungkin menjadi INCONCLUSIVE_TIMEOUT oleh parser itu.

Raw GDB direct-field-2/3 yang terkomit memuat marker 180 dan capture PASS pada ~60,66–60,73 detik; TSV lama mencatat wrapper exit -9 dan sekitar 10 detik. Dua kumpulan output ini tidak konsisten dan bukan pasangan satu eksekusi. Penyebab struktural yang terlihat di kode: workflow lama menulis berulang ke reports/ae_2026-10-29/deep/ yang sama, dengan nama file tetap, lalu melakukan rebase/push. Output run berbeda dapat menimpa sebagian log sementara TSV/manifest dari eksekusi lain ikut terpublikasi.

### Mengapa ae4_ram_snapshots.tsv hanya header

Raw AE4 yang terkomit mempunyai tujuh peluncuran dengan marker 180 + capture PASS: field3 attempt 1/2, field4 attempt 1/2, field5 attempt 1/2, dan field8 attempt 1. Field8 attempt 2 serta kedua attempt field10 tidak memiliki marker 180.

Kode hanya menambah baris RAM bila marker 180, capture PASS, dan runtime/current.sstate tersedia. Karena tujuh raw log memenuhi dua kondisi pertama, TSV header-only tidak cocok dengan raw yang terkomit bila dianggap satu run. Kesimpulan: TSV stale/berasal dari snapshot run berbeda karena output directory bersama. SHA RAM/word tujuh capture historis itu TIDAK TAHU; nilainya tidak tertulis di GDB text log dan TSV yang semestinya menyimpan nilainya kosong.

### Manifest

Raw file terkomit: 70 GDB + 70 PCSX = 140 file. Manifest lama: 112 entri; SHA mismatch 55 (54 GDB + 1 PCSX); ukuran mismatch 55; path hilang 0; cocok penuh 57; 28 file raw tambahan tidak dicakup manifest lama. COMMITTED_RAW_MANIFEST.sha256.txt menghitung SHA-256 dan ukuran dari bytes persis commit sumber.

### Run/job pembuat ee48de4

Commit ee48de43577d08eeca77f6930d7f49a250cbba83 dibuat 2026-10-29T23:20:16Z. Pembuatnya Actions run 40966952270 attempt 1, job bisect ID 123773754840; job mulai 22:34:57Z dan selesai 23:20:21Z. Log job merekam commit lokal 5b188ce, rebase sukses, lalu AE1_DEEP_EVIDENCE_HEAD=ee48de4… pada 23:20:18Z. Attempt 2/job 123874229459 adalah retry berbeda yang gagal publikasi saat git pull --rebase karena konflik add/add/content, exit 1; bukan job pembuat ee48de4.

### Perbaikan publikasi

Workflow AE1 lama kini menulis ke folder run/attempt unik. Workflow AJ1/H6 juga memakai reports/aj_2026-10-30/runs/run-<RUN_ID>/attempt-<ATTEMPT>/. Ringkasan dan tabel diparse langsung dari raw log pada folder audit/runtime masing-masing; tidak ada lagi output raw bersama yang ditimpa lintas run. Tidak ada file biner privat dimasukkan.

## AJ2 — H6 dua peluncuran headless

### Definisi dan identitas

Target source SHA 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d, 21.163.286 byte. Control source SHA 9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492, 21.162.546 byte. H6 = target base dengan seluruh top-level field 6/SPU diganti dari control; label: **BUKAN target murni**. Ukuran hibrida sementara 21.162.538 byte.

SHA-256 H6 = d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475 (64 karakter), sama dengan digest referensi terkomit pada hasil AE2. PCSX-Redux pin 0c3572c3d, headless Xvfb, input game NONE. Timeout tiap peluncuran 180 s; batas minimum 2 × 62.745 + 30 = 155.490 s, jadi 180 s memenuhi.

### RAM

| Sumber | SHA-256 RAM 2 MiB | Ukuran region RAM pada savestate |
|---|---|---:|
| Target asli | 3ad7b85c857a868d91df4b3f1049c23889a0dc482ad7ee390ac8b6c05c3190f4 | 8.388.608 byte |
| H6 attempt 1 | 4c964aaca0afccc68317acd0726fec680c305b903cd426e70afe3d8ac1f1e741 | 8.388.608 byte |
| H6 attempt 2 | 4c964aaca0afccc68317acd0726fec680c305b903cd426e70afe3d8ac1f1e741 | 8.388.608 byte |

Kedua launch H6 identik pada RAM 2 MiB di marker post-load VSync 180; hash tersebut berbeda dari target asli. Jadi H6 repeatable pada titik ukur ini, tetapi tidak mengembalikan RAM target.

| Alamat | Target raw bytes | H6 attempt 1/2 raw bytes | LE32 |
|---|---|---|---:|
| 0x80070EB8 | dc 05 00 00 | dc 05 00 00 | 0x000005DC (1500) |
| 0x80070F6C | dc 05 00 00 | dc 05 00 00 | 0x000005DC (1500) |
| 0x8013A554 | 08 ef 1c 80 | 08 ef 1c 80 | 0x801CEF08 |

Dua nilai 1500 cocok dengan angka yang dilaporkan untuk checkpoint target. Namun parser savestate yang terkomit memberi label semantik UNKNOWN; laporan ini menyatakan bytes/LE32, bukan membuktikan independen bahwa alamat tersebut secara semantik adalah Chakra. Word pada 0x8013A554 juga belum terbukti sebagai pointer object.

### Waktu dan exit

| Attempt | elapsed ke marker 180 | Hasil | GDB wrapper exit | Exit emulator di raw log |
|---:|---:|---|---:|---|
| 1 | 70.561992883682 s | 180 + RAM capture PASS | -9 | TIDAK TAHU |
| 2 | 70.531628608704 s | 180 + RAM capture PASS | -9 | TIDAK TAHU |

Kedua capture terjadi sebelum wrapper dihentikan watchdog pada 180 s (+ kill grace 5 s), sehingga wall time sekitar 185 s. Skrip H6 exit 0, job h6 success, workflow Actions success. Exit -9 adalah GDB wrapper akibat watchdog, bukan exit normal emulator dan bukan SIGSEGV. Bukti RAM diambil sebelum watchdog.

## AJ3 — replay determinism dan basis host/RSI

**Rencana:** bekukan H6 SHA d57b6261…3475, PCSX-Redux 0c3572c3d, BIOS SCPH-7502, ISO/CUE, Memory Card, flags, dan urutan load. Jalankan proses baru independen dari H6 yang sama dan ukur RAM 2 MiB serta tiga word pada offset VSync post-load 180, 240, 360, lalu titik setelah input. Dua peluncuran kini telah identik pada marker 180; langkah berikut menguji apakah kesamaan berlanjut pada 240/360 tanpa input, kemudian mengulang jadwal input identik (START untuk dialog hanya bila dialog terverifikasi) dan membandingkan RAM pada frame yang sama untuk mencari frame divergensi pertama. Setiap run/attempt tetap punya folder unik; yang dikomit hanya teks tersanitasi, bukan RAM dump atau savestate.

**Putusan eksplisit: pencarian basis RAM SPU host/RSI DIPARKIR SEMENTARA — YA.** H6 repeatable pada frame 180 tetapi hash RAM berbeda dari target, sehingga belum membuktikan basis RAM target atau asal host/RSI. Audit pointer AF1 menunjukkan field current (field 8) target pada banyak channel bernilai 0xD5E7578F, di luar rentang SPU RAM 0x80000; nilai control berbeda dan beberapa sentinel-like. Audit STEP6 pada 0x8013A554 masih terhalang konflik code/data mapping pada base statis hipotetis. Belum ada dasar menyebut word itu RSI/host pointer atau menetapkan basis RAM host/RSI. Semantik/provenance host/RSI: **TIDAK TAHU**. Jalur riset tidak dibatalkan; dibuka lagi setelah replay multi-frame H6 dan mapping runtime address-space dipastikan.

## Status akhir

- AJ1 audit raw/manifest: selesai, K4 (bukti statis).
- AJ2 H6 di frame 180: dua peluncuran runtime identik untuk RAM 2 MiB, K5 untuk determinisme H6 pada titik ukur itu.
- Replay multi-frame: belum dilakukan.
- Semantik Chakra/0x8013A554 dan basis RAM host/RSI: TIDAK TAHU.
- Story Mode: **BELUM TERBUKTI TAMAT**.
- ISO, BIOS, savestate target/control, Memory Card, hibrida, dan RAM dump hanya dipakai sementara di runner, lalu dibersihkan. Tidak disimpan di repo; status Release tidak diubah.

## Ringkasan Actions

Run 41028457166; job h6 ID 123972149171; workflow success; H6 script exit 0; H6 SHA-256 d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475; timeout tiap launch 180 s. Attempt 1/2 masing-masing memperoleh marker 180 + capture PASS, wrapper exit -9, emulator exit normal TIDAK TAHU. Ringkasan run ada di ACTIONS_RUN_SUMMARY.txt, detail dua peluncuran di H6_TWO_LAUNCH_RAM.tsv dan H6_RUNTIME_EVIDENCE.txt.
