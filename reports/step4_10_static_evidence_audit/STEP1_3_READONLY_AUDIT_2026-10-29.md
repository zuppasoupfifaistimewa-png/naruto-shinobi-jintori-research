# Audit read-only Langkah 1–3 — 29 Oktober 2026

## Batas kerja dan input
Analisis statis saja. Tidak ada emulator/gameplay yang dijalankan, tidak ada input tombol, dan tidak ada savestate yang dimuat. Repo yang dipakai hanya `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`.

Identitas statis yang diverifikasi dalam Actions run #40789339014:
- `SLPS_035.53`: 385.024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
- `DATA.BIN`: 66.015.232 byte, SHA-256 `69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822`.
- Entry 1: offset `0x10BB000`, 596.412 byte, SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`.

Dump RAM 2 MiB terpisah dengan SHA-256 yang diminta `3ad7b85c857a868d91df4b3f1049c23889a0dc482ad7ee390ac8b6c05c3190f4` tidak tersedia sebagai berkas dump di workspace ini. Arsip savestate ada, tetapi tidak dipakai untuk membangun ulang RAM karena instruksi melarang rekonstruksi isi RAM. Oleh sebab itu Langkah 1 tidak dapat dikerjakan dengan benar.

## Matriks status
| Langkah | Status | Kriteria | Bukti / keyakinan |
|---|---|---|---|
| 1a–1b | TIDAK BISA | Gagal dinilai; tidak ada dump RAM mentah | Dump 2 MiB hilang; savestate tidak dipakai sebagai pengganti. K5. |
| 2 | SEBAGIAN | Hitungan dan sampel awal sesuai; validasi Ghidra dengan seeding fungsi yang setara masih menunggu run susulan | Run #40789339014, CSV A2 di folder run tersebut; hitungan statis K2, pemetaan runtime K4. |
| 3 | SEBAGIAN | Semua 144 JAL diklasifikasi, tetapi 97/144 masih TIDAK PASTI dan validitas jalur kontrol belum dibuktikan penuh | CSV A4 entry 1 dan 4 pemanggil EXE; pengelompokan instruksi K3, semantik gameplay K5. |

## Langkah 1 — perbandingan runtime
**TIDAK BISA:** dump RAM mentah tidak tersedia. Karena itu tidak saya buat:
- perbandingan blok 4 KiB DATA.BIN entry 1 dengan RAM pada offset `0xAD450`;
- pencarian geser potongan 64 byte;
- 94 baris perbandingan blok EXE asli pada offset RAM `0x10000`.

Savestate hanya tercatat tersedia sebagai arsip; tidak dimuat atau diurai untuk menyintesis dump RAM.

## Langkah 2 — XREF `0x8013A554`
Run [#40789339014](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40789339014) selesai success dan menyimpan CSV sanitasi di `reports/step4_10_static_evidence_audit/run_40789339014/`.

### Hitungan yang dapat diulang
- XREF Ghidra baru pada base kandidat `0x800AD450`: **324 baris** = 322 READ + 2 WRITE; sumber XREF bertanda `ANALYSIS`.
- Scan extended raw MIPS: **326 kandidat** = 324 READ + 2 WRITE, semuanya di DATA.BIN entry 1. EXE dan entry 0: 0 READ / 0 WRITE / 0 ADDRESS untuk pola displacement `-0x5AAC`.
- Pasangan LUI `0x8014` dalam maksimum 32 instruksi sebelumnya, dengan register basis tidak ditimpa: 292 READ + 2 WRITE. Dalam 98 pasangan, ada instruksi kontrol alur di antaranya; pasangan tersebut bukan bukti dominance CFG.
- Hasil Ghidra lama 194 XREF (192 READ + 2 WRITE) vs scan ketat lama 137: irisan 79, 58 scan-only, 115 Ghidra-only.
- Kelas satu-per-lokasi pada rekonsiliasi: 58 scan-only = 56 “muncul di Ghidra sesudah rebase” + 2 “tidak berada di fungsi Ghidra rebase”; 115 Ghidra-only = 96 “pasangan LUI ditemukan dengan rentang 32 instruksi” + 19 “tidak ada LUI tidak-tertimpa dalam rentang itu”.
- Audit sampel disassembly: 32 baris, yakni 10 sampel untuk masing-masing kelas berjumlah lebih dari 10 dan semua 2 sampel untuk kelas berjumlah 2. CSV menyimpan word mentah, bytes, disassembly, dan status encoding MIPS untuk tiap sampel.
- Ghidra-only baru vs scan extended = 32; ambang dukungan base lama salah adalah <57,5. Dengan impor awal ini, ambang tersebut **terpenuhi**. Ini bukti pemilahan statis saja; bukan validasi base loader runtime.

### Target slot
Alamat virtual `0x8013A554) terletak pada offset entry 1 `0x8D104) untuk kandidat base `0x800AD450`. Bytes file `00 00 00 00`, u32 little-endian `0x00000000`. Nilai RAM TIDAK DIKETAHUI; hash dump yang diminta tidak membuktikan bahwa dump tersedia pada sesi ini.

Bukti CSV:
- `a2_ghidra_rebased_xrefs.csv`
- `a2_expanded_xref_candidates.csv`
- `a2_expanded_xref_summary.csv`
- `a2_old_ghidra_xrefs_194.csv`
- `a2_legacy_xref_reconciliation.csv`
- `a2_reconciliation_class_summary.csv`
- `a2_reconciliation_sample_audit.csv`
- `a2_target_slot_static_value.csv`

## Langkah 3 — 144 JAL RNG dalam entry 1
Run awal mengklasifikasi tepat **144/144** site JAL mentah ke `0x80035D78`:
- `VALID`: 47
- `TIDAK PASTI`: 97
- `DATA`: 0

Pengelompokan total 144 site: 11 pola DIV/remainder, 40 pola MASK_ONLY, 90 tanpa mask/modulus langsung dalam jendela 32 kata, dan 3 MASK_AND_DIV. Untuk semua baris VALID, kolom bukti mask/modulus diisi instruksi atau `TIDAK ADA`. Label fungsi gameplay setiap baris tetap `TIDAK TERBUKTI`. Klasifikasi ini adalah hasil statis awal; pemeriksaan jalur CFG/runtime tidak dibuktikan oleh encoding yang valid saja.

CSV:
- `a4_entry1_rng_calls_classified.csv` (144 baris)
- `a4_entry1_rng_groups.csv`

### Empat pemanggil langsung di EXE
- `0x80015B14`, kandidat fungsi `0x80015ADC): RNG disimpan dari `v0` ke `s1` di sekitar `0x80015B1C`; pembagian `div s1,v0` di `0x80015B38), remainder melalui `mfhi` di `0x80015B3C). Operand pembagi `v0` dibatasi byte oleh `andi v0,v0,0xFF` pada `0x80015B34`. Arti gameplay TIDAK TERBUKTI.
- `0x80015BF0`, kandidat fungsi `0x80015B7C): `lhu v1,0(s3)` di `0x80015BF8`, `div v0,v1` di `0x80015C00), `mfhi` di `0x80015C04). Pembagi merupakan nilai runtime; nilai konstannya TIDAK DIKETAHUI. Arti gameplay TIDAK TERBUKTI.
- `0x8001A460`, fungsi `0x8001A328): `div v0,s0` di `0x8001A46C), `mfhi` di `0x8001A470); hasil dipakai untuk indeks sebelum byte dibaca di `0x8001A484) dan ditulis ke alamat efektif `0x80089DA9` di `0x8001A48C`. Arti tabel/gameplay TIDAK TERBUKTI.
- `0x80020C24`, fungsi `0x80020BF4`: tidak ada DIV/ANDI langsung yang dikenali scanner sederhana, tetapi raw MIPS di `0x80020C30–0x80020C44` memperlihatkan koreksi signed-remainder melalui BGEZ/SRA/ADDIU/SRA/SLL/SUBU; keluaran RNG PS1 nonnegatif, sehingga jalur BGEZ plus delay-slot SRA dan SLL/SUBU menghasilkan sisa 12-bit (modulo `0x1000`). Hasil disimpan di field objek `+0x34` oleh `sw v0,0x34(s0)` di `0x80020C48`. Nama/arti objek TIDAK TERBUKTI.

Bukti EXE:
- `a4_exe_rng_calls_refined.csv`
- `a4_rng_callers.csv`
- `static-audit.txt`

## Batas interpretasi dan run susulan
Impor pertama base `0x800AD450` memberi 88 nama fungsi unik yang berisi sumber XREF. Pre-script `tools/ghidra/PrepareRebasedEntry1.java` kemudian ditambahkan untuk menyemai kandidat fungsi pada offset file yang sama seperti impor lama.

Run susulan [#40789851311](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40789851311) berhasil pada impor Ghidra, scanner, dan cleanup (langkah 10–12), serta log runner mencatat kembali XREF baru 324, kelas rekonsiliasi yang sama, dan 144 JAL entry-1 (47 VALID/97 TIDAK PASTI). Namun langkah penyimpanan ke repo gagal: `git push` ditolak `fetch first`/non-fast-forward karena `main` bertambah setelah checkout; upload artifact dilewati. Maka keluaran CSV per lokasi yang berasal dari seeded run tidak tersedia di repo, dan angka per lokasi tetap dikutip dari keluaran pertama yang tersimpan. Ini bukan kegagalan Ghidra atau emulator.

Commit `c12c272875c419c9120583144ac81620246d7477` memperbaiki workflow agar rebase pada `origin/main` sebelum push, menulis log sebagai `.txt` agar tidak diabaikan `.gitignore`, dan mencatat pola remainder aritmetis pada pemanggil `0x80020C24`. Run tindak lanjut [#40790387202](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40790387202) telah masuk antrean; belum ada keluaran baru darinya saat laporan diperbarui.

Run Ghidra statis terpisah [#40789217602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40789217602) masih menganalisis entry 0. Batas maksimum workflow-nya 35 menit sejak mulai 06:42:39 WIB, yakni 07:17:39 WIB; ini batas timeout, bukan prediksi saat selesai normal.

Story Mode tidak disentuh dan tidak dinyatakan tamat.
