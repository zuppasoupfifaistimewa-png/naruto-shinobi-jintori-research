# Audit UH0–UH3 — baseline c7da18…

**Baseline inklusif:** `c7da18bef75f6e6905d495b72710f50aaf1bb5b0`. Analisis statis membaca repo pada baseline; laporan ini diterbitkan setelah addendum statis. Tidak ada kode emulasi atau workflow yang diubah.

| Bagian | Status | Level | Ringkasan |
|---|---|---:|---|
| UH0 manifest b74d931 | **TUNTAS** | K4 | 63.121 baris induk dipetakan ke 319 berkas dalam 5.536 rentang inklusif; selisih API 1.311 dialokasikan tepat ke 3 berkas. |
| UH0 konflik byte | **TUNTAS** | K4 | Gate: 14.001 observasi konflik; 3.512 koordinat konflik unik; 10.489 observasi tambahan pada koordinat yang sama. |
| UH1 writer | **SEBAGIAN** | K4/K2/K0 | 307 PC writer terinventaris dalam cakupan census EXE/ENTRY1 yang tersedia; cakupan SW, SH +1C/+1E, dan ENTRY0 belum lengkap. |
| UH2 runtime | **BELUM** | K0 | Tidak ada launch/watchpoint; batas array dan alamat aman belum diketahui. |
| UH3 ledger | **TUNTAS** | K4 | 7 commit termasuk baseline, 33 event no-renames, 1.361 tambahan/439 penghapusan; 1 Actions schedule run, tanpa push/dispatch. |

## UH0 — baris yang dipangkas dan konflik byte

Commit yang diperiksa: parent `c87e124daeb4e007c555bc07eab811bfe61e6afb`, child `b74d931cf9855c16c3d3e22b10a11cf94c7c2d04`. Perubahan commit: 336 path (319 modified, 17 added, 0 removed). Manifest bersumber dari metadata gate `UF0_TRIMMED_ROWS.tsv`: 63.121 row keys unik pada 319 berkas, digabung menjadi 5.536 rentang nomor baris induk 1-based dan inklusif. Tidak ada byte nilai yang disimpan. Tidak ada baris TSV yang dihapus oleh audit ini.

GitHub REST melaporkan total commit deletion 63.121, tetapi penjumlahan field deletion per-file hanya 61.810. Seluruh selisih 1.311 teralokasi dari registry trim:
- `aq1-run-41318572706/attempt-1/aw1-helper-call-windows.tsv`: 650 baris;
- `aq1-run-41559535429/attempt-1/aw1-helper-call-windows.tsv`: 650 baris;
- `aq1-run-41803736009/attempt-1/bb2-tile-nibble-access.tsv`: 11 baris.
Ketiga field deletion per-file API bernilai 0; metadata trim tetap menyediakan path dan nomor baris induknya. Jumlah 650+650+11 = 1.311; tidak ada selisih tersisa yang perlu ditebak.

Definisi konflik gate: pada setiap koordinat komposit (label image, jenis koordinat, identitas sumber bila label belum terselesaikan, alamat), byte strict-hex pertama dijadikan nilai acuan. Setiap observasi berikutnya yang berbeda dari nilai pertama menambah satu *observasi konflik*; nilai acuan tidak diganti. Jadi 14.001 adalah hitungan per-observasi, sedangkan 3.512 adalah koordinat unik yang mengalami konflik. Selisih 10.489 merupakan observasi tambahan pada koordinat yang sudah konflik, bukan jumlah pasangan semua nilai yang berbeda.

## UH1 — store medan petak dan D15A8

Tabel gabungan berisi 307 PC unik pada EXE/ENTRY1: 139 store SB pada +0x1A/+0x1C/+0x1E (MA2), 130 write pada +0x1A (DX1; 123 SH dan 7 SB), serta 42 store SH +0x20 yang alias basisnya ke slot 0x8013EA84 (DY2). PC duplikat lintas census dicatat sekali. Dari 139 SB, 97 berbasis stack ditandai stack-local, bukan penulisan petak terverifikasi; 42 non-stack adalah kandidat yang alias dan stride-nya belum terbukti. Dua SH +0x1A di FUN_800F7ADC (PC 0x800F7D9C dan 0x800F7DB0) beralias EA84 dan memakai 0x124*index, tetapi keduanya loader copy, bukan biaya upgrade.

Untuk +0x20, 42 SH store pada 16 fungsi ENTRY1 memiliki alias basis ke slot EA84. Hanya PC 0x800D5A1C juga telah dikonfirmasi dengan ekspresi indeks *per-PC* 0x124. Pada FUN_800D15A8, store itu berada di state case 0x15: counter DAT_80139ec2 bertambah, dan store dilakukan hanya ketika hasil kenaikan sama dengan 0x21 (33). Nilai yang ditulis adalah konstanta 0xF020 sebagai bagian dari inisialisasi beberapa field record, lalu counter direset dan state menjadi 8. Ini bukan increment level setiap pemanggilan. Makna gameplay state dan nibble halfword +0x20 tetap TIDAK TAHU.

Batas inventaris: belum tersedia census global SW untuk +1A/+1C/+1E, census global SH untuk +1C/+1E, dan writer census ENTRY0. ENTRY0 artifact run 41290779708 hanya mengeluarkan indeks fungsi parsial; Ghidra timeout pada 1.800 detik dengan body-overlap errors; alamat RAM 0x800AD000 masih hipotesis dan runtime mapping tidak tervalidasi. Writer petak ENTRY0 tetap TIDAK TAHU (K0). Karena itu UH1 tetap SEBAGIAN.

**Rumus biaya upgrade lompat level d>=2: TIDAK TAHU.** Nilai 400/800/1600 tetap K1/hipotesis. Belum ada rantai debit atau konstanta biaya yang terikat ke transaksi upgrade.

## UH2 — runtime read-only

Tidak ada emulator launch untuk UH2. Slot 0x8013EA84 adalah pointer dinamis, bukan alamat awal RAM final yang cukup untuk menentukan rentang seluruh record. Jumlah record, indeks yang sah, dan seluruh alias medan belum terbukti; karena itu tidak dipasang watchpoint pada alamat tebakan. Tidak ada TSV nilai bernama di frame 1/900, jumlah hit watchpoint PC/RA, status instrumented=true, ataupun hash Memory Card sebelum/sesudah. Tidak ada run Actions UH2 baru.

Pyflakes/YAML/dry fail-fast tidak dijalankan pada sesi ini karena tidak ada skrip atau workflow yang diubah; pyflakes tidak tersedia lokal. Tidak ada source SHA run baru: tidak ada emulasi UH2. Kode yang dianalisis tetap baseline c7da18be….

## UH3 — ledger baseline-inclusive

Ledger dari baseline sampai HEAD pra-publikasi `14e911b706f9ea27dff96cd9f735e043bfd8b066` mencakup 7 commit (termasuk baseline), 33 event file no-renames, 1.361 additions, dan 439 deletions. Commit berurutan: `c7da18be`, `02ad6ea6`, `46948b55`, `c3fd42bc`, `2ba02b4f`, `7676e8e3`, `14e911b7`.

Query Actions sejak 2026-11-11 05:38:31Z menghasilkan total_count=1: run `42977820741`, event schedule, 2026-11-11 07:12:39Z (14:12:39 WIB), status completed/success, job `monitor` id `130380930819`, source SHA baseline c7da18be…. Log tidak mencetak exit code proses terpisah; 0 hanya inferensi dari job success. Artifact monitoring tidak diunggah karena `monitoring-report.txt` tidak ditemukan. Monitor menyatakan tidak ada adaptive player run pada latest 50; ini bukan progres gameplay atau bukti Story Mode selesai. Tidak ada push atau workflow_dispatch run yang ditemukan.

## Berkas yang diubah oleh publikasi koreksi ini

- `reports/stage1_economy/uh-audit-2026-11-11/UH0_B74_DELETED_LINE_MANIFEST.tsv`
- `reports/stage1_economy/uh-audit-2026-11-11/UH0_SUMMARY.txt`
- `reports/stage1_economy/uh-audit-2026-11-11/UH1_TILE_WRITER_AUDIT.tsv`
- `reports/stage1_economy/uh-audit-2026-11-11/UH1_SUMMARY.txt`
- `reports/stage1_economy/uh-audit-2026-11-11/UH3_COMMITS.tsv`
- `reports/stage1_economy/uh-audit-2026-11-11/UH3_FILE_EVENTS_NO_RENAMES.tsv`
- `reports/stage1_economy/uh-audit-2026-11-11/UH3_SUMMARY.txt`
- `reports/stage1_economy/uh-audit-2026-11-11/UH_FINAL_REPORT.md`

Ledger snapshot mengecualikan commit publikasi ini sendiri. STATUS.md dan Release tidak diubah; tidak ada ROM, BIOS, Memory Card, savestate, RAM dump, executable, DATA.BIN, atau biner yang ditambahkan.
