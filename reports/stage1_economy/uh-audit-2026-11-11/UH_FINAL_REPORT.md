# Audit UH0–UH3 — baseline c7da18…

**Baseline inklusif:** `c7da18bef75f6e6905d495b72710f50aaf1bb5b0`. Audit ini menggabungkan pemeriksaan statis, data runtime lama yang sudah tersimpan, dan rekonsiliasi riwayat Git/Actions. Tidak ada kode emulasi atau workflow yang diubah. Run runtime UE2 yang ditemukan berada sebelum baseline; tidak diperlakukan sebagai run baru pada source baseline.

| Bagian | Status | Level | Ringkasan |
|---|---|---:|---|
| UH0 manifest b74d931 | **TUNTAS** | K4 | 63.121 baris induk dipetakan ke 319 berkas dalam 5.536 rentang inklusif; selisih API 1.311 dialokasikan tepat ke 3 berkas. |
| UH0 konflik byte | **TUNTAS** | K4 | 14.001 observasi konflik; 3.512 koordinat konflik unik; 10.489 observasi tambahan pada koordinat yang sama. |
| UH1 writer | **SEBAGIAN** | K4/K2/K0 | 307 PC unik dari census EXE/ENTRY1; Entry0, SW, dan sebagian SH belum tercakup. |
| UH2 runtime | **SEBAGIAN** | K5/K0 | Dua trace NO_INPUT lama 900-frame identik (K5 untuk Exec trace); snapshot field petak dan write-watch masih tidak tersedia (K0). |
| UH3 ledger | **TUNTAS** | K4 | 8 commit baseline-inclusive, 41 event file no-renames, 2.002 tambahan/845 penghapusan; 1 Actions schedule run. |

## UH0 — baris yang dipangkas dan konflik byte

Commit yang diperiksa: parent `c87e124daeb4e007c555bc07eab811bfe61e6afb`, child `b74d931cf9855c16c3d3e22b10a11cf94c7c2d04`. Perubahan commit: 336 path (319 modified, 17 added, 0 removed). Manifest bersumber dari metadata gate `UF0_TRIMMED_ROWS.tsv`: 63.121 row keys unik pada 319 berkas, digabung menjadi 5.536 rentang nomor baris induk 1-based dan inklusif. Tidak ada byte nilai yang disimpan. Tidak ada baris TSV yang dihapus oleh audit ini.

GitHub REST melaporkan total commit deletion 63.121, tetapi penjumlahan field deletion per-file hanya 61.810. Seluruh selisih 1.311 teralokasi dari registry trim:
- `aq1-run-41318572706/attempt-1/aw1-helper-call-windows.tsv`: 650 baris;
- `aq1-run-41559535429/attempt-1/aw1-helper-call-windows.tsv`: 650 baris;
- `aq1-run-41803736009/attempt-1/bb2-tile-nibble-access.tsv`: 11 baris.
Ketiga field deletion per-file API bernilai 0; metadata trim tetap menyediakan path dan nomor baris induknya. Jumlah 650+650+11 = 1.311; tidak ada selisih tersisa yang perlu ditebak.

Definisi konflik gate: pada setiap koordinat komposit (label image, jenis koordinat, identitas sumber bila label belum terselesaikan, alamat), byte strict-hex pertama dijadikan nilai acuan. Setiap observasi berikutnya yang berbeda dari nilai pertama menambah satu observasi konflik; nilai acuan tidak diganti. Jadi 14.001 adalah hitungan per-observasi, sedangkan 3.512 adalah koordinat unik yang mengalami konflik. Selisih 10.489 merupakan observasi tambahan pada koordinat yang sudah konflik, bukan jumlah pasangan semua nilai yang berbeda.

## UH1 — store medan petak dan D15A8

Census gabungan berisi 307 PC unik di EXE/ENTRY1:
- MA2: 139 SB unik ke displacement +0x1A/+0x1C/+0x1E, terpecah +0x1A=7, +0x1C=42, +0x1E=90; 97 memakai base register `$sp` (stack-local), 42 memakai base register non-stack yang belum membuktikan alias/stride petak.
- DX1: 130 write unik ke +0x1A, terdiri 123 SH dan 7 SB.
- DY2: 42 SH +0x20 dengan alias basis ke slot `0x8013EA84`; hanya PC `0x800D5A1C` juga memiliki bukti stride per-PC `0x124`.
- Empat PC MA2/DX1 muncul di dua census tetapi dihitung sekali: `0x800B396C`, `0x800B589C`, `0x800B5E2C`, `0x8011FF90`. Persamaan union: 139+130+42−4=307.

Dua SH +0x1A di `FUN_800F7ADC` (PC `0x800F7D9C` dan `0x800F7DB0`) beralias ke EA84 dan memakai indeks × `0x124`, tetapi keduanya adalah loader copy, bukan bukti debit upgrade. Empat puluh satu store SH +0x20 lainnya belum memiliki pembuktian stride per-PC. Makna nibble pada halfword +0x20 dan apakah itu level gameplay tetap **TIDAK TAHU**.

Di `FUN_800D15A8`, state case `0x15` menaikkan `DAT_80139ec2`; store +0x20 terjadi hanya saat hasil kenaikan sama dengan `0x21` (33). Nilai yang ditulis adalah konstanta `0xF020` sebagai bagian inisialisasi multi-field, kemudian counter direset dan state menjadi 8. Ini bukan increment level di setiap pemanggilan. Formula biaya upgrade dengan lompatan level d≥2 tetap **TIDAK TAHU**; nilai 400/800/1600 hanya K1.

Entry0 kini diperiksa dari artefak ZIP Ghidra run `41290779708` (SHA-256 `bea77586b6b2091f840405557cae65c4b1aea2babfd967c1c5d7eb77a9292af5`). Arsip itu mengekspor 38 baris indeks fungsi, 30 baris literal instruksi, dan satu catatan helper `0x800BDBFC` tanpa referensi. Log berisi 2.676.692 baris; autoanalysis berhenti tepat pada 1.800 detik, 29 body fungsi gagal diperbaiki karena overlap, dan tiga instruksi delay-slot invalid. Ada tiga direct JAL yang tervalidasi ke target RNG, tetapi caller function boundary tidak terikat. Base `0x800AD000` tetap hipotesis, bukan mapping runtime. Artefak tidak berisi census SB/SH/SW per-PC. Karena itu writer petak Entry0 tetap **TIDAK TAHU (K0)**. Cakupan SW +1A/+1C/+1E global serta SH +1C/+1E global juga belum tuntas. UH1 tetap SEBAGIAN.

## UH2 — trace runtime lama dan batas bukti

Run lama `42965928825` memang ada; run itu bukan run baru dalam audit ini dan source SHA-nya `0ff400d97cd1a39a9356d1c2af65690e837be72f`, sebelum baseline UH `c7da18be…`. Job `130343034778` berstatus completed/success; UG2 exit 0. Dua kondisi `NO_INPUT` masing-masing berjalan 900 frame, memuat save state, dan keluar kode 0. Empat Exec breakpoint adalah `0x800D15A8`, `0x800B54DC`, `0x800F3658`, dan `0x800F5DAC`; masing-masing mencatat 450 total hit per launch.

Setiap peluncuran NO_INPUT menyimpan 32 event (8 event per breakpoint, dibatasi pada jendela awal frame 1–30). Perbandingan 32 tuple berdasarkan frame, label/alamat breakpoint, PC, RA, a0, dan seluruh GPR r0–r31 identik antara peluncuran 1 dan 2. Ini K5 hanya untuk pengulangan trace Exec breakpoint tersebut, bukan untuk seluruh logika atau penulisan memori petak. Kartu memori dibaca read-only 0444 dan hash sebelum/sesudah sama (`78b6d4ac9ab4d23caf7e5f04f83539bf5d994cccfb0a709d14ac53d05c8e21ef`); hash checkpoint setelah kedua peluncuran juga sama (`705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`).

Yang belum diambil:
- nilai field petak bernama pada frame 1 dan frame 900;
- watchpoint write dengan PC/RA dan jumlah semua hit;
- alamat/count record yang sah pada checkpoint UE2 yang sama.

Trace lama hanya menangkap GPR di jendela awal, bukan snapshot RAM pada frame 900. Ia menggunakan Exec breakpoint, bukan write-watchpoint. Slot `0x8013EA84` adalah pointer dinamis; rentang record dan batas indeks yang aman untuk checkpoint UE2 belum terbukti. Run lama tidak membuktikan baseline source c7da secara langsung. Karena itu UH2 **SEBAGIAN**: repeatability trace lama K5, nilai field dan write-watch tetap K0. Tidak ada emulator launch baru atau write watch dipasang pada alamat tebakan.

## UH3 — ledger baseline-inclusive

Ledger kini mencakup baseline dan 7 commit descendant sampai HEAD pra-publikasi `73ca2708ca47be05d89e85a5a6978d1c1de0ec88`: total 8 commit, 41 event file no-renames, 2.002 additions, 845 deletions. Commit tambahan `73ca2708` sendiri mengubah 8 file laporan (641 additions/406 deletions), kini dimasukkan sebagai event ledger. Commit publikasi koreksi ini dikecualikan agar snapshot tidak melingkar.

Delapan commit: `c7da18be`, `02ad6ea6`, `46948b55`, `c3fd42bc`, `2ba02b4f`, `7676e8e3`, `14e911b7`, `73ca2708`.

Query Actions sejak baseline menghasilkan total_count=1: run `42977820741`, event schedule, 2026-11-11 07:12:39Z (14:12:39 WIB), status completed/success, job `monitor` id `130380930819`, source SHA baseline c7da18be…. Exit code 0 hanya inferensi dari job success; process code tidak dicetak terpisah. Artifact monitoring tidak diunggah karena `monitoring-report.txt` tidak ditemukan. Tidak ada push atau workflow_dispatch run yang ditemukan. Story Mode completion tetap NOT PROVEN.

## Putusan akhir

- **UH0: TUNTAS K4.**
- **UH1: SEBAGIAN K4/K2/K0.** Untuk menuntaskan: diperlukan census store penuh yang mencakup instruction width/field yang hilang dan Entry0 dengan mapping tervalidasi.
- **UH2: SEBAGIAN K5/K0.** Untuk menuntaskan: diperlukan snapshot field dan all-hit write watch pada checkpoint/source yang tepat setelah active record range terbukti.
- **UH3: TUNTAS K4.**

Dengan bukti repo yang tersedia dan pembatasan tidak meluncurkan emulator baru, UH1 dan UH2 tidak dapat dinyatakan tuntas tanpa mengarang data. Ini batas bukti, bukan klaim bahwa game tidak menulis atau tidak menggunakan field tersebut.

## Berkas yang diubah oleh publikasi koreksi ini

- `reports/stage1_economy/uh-audit-2026-11-11/UH1_SUMMARY.txt`
- `reports/stage1_economy/uh-audit-2026-11-11/UH1_ENTRY0_ARTIFACT_AUDIT.txt`
- `reports/stage1_economy/uh-audit-2026-11-11/UH2_BLOCKER.txt`
- `reports/stage1_economy/uh-audit-2026-11-11/UH2_UE2_TRACE_RECONCILIATION.tsv`
- `reports/stage1_economy/uh-audit-2026-11-11/UH3_COMMITS.tsv`
- `reports/stage1_economy/uh-audit-2026-11-11/UH3_FILE_EVENTS_NO_RENAMES.tsv`
- `reports/stage1_economy/uh-audit-2026-11-11/UH3_SUMMARY.txt`
- `reports/stage1_economy/uh-audit-2026-11-11/UH_FINAL_REPORT.md`

STATUS.md dan Release tidak disentuh. Tidak ada ROM, BIOS, Memory Card, savestate, RAM dump, executable, DATA.BIN, atau biner yang ditambahkan.
