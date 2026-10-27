# Indeks panggilan executable utama — scan statis pendahuluan

Tanggal pemeriksaan: 2026-10-27  
Sumber lokal: `SLPS_035.53`, ukuran 385.024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.  
Cakupan kode dari header: file offset `0x800..0x5DFFF`, alamat muat `0x80010000`, ukuran text `0x5D800`. Biner tetap di luar Git.

## Status Langkah 3

**Ghidra tersedia di GitHub Actions, tetapi analisis executable masih BELUM SELESAI.** Run [#40434733043](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40434733043) sukses memasang Ghidra 12.2 dengan Temurin JDK 25 dan memverifikasi launcher `support/analyzeHeadless`; cache instalasi disimpan untuk run berikutnya. Lingkungan kerja lokal sebelumnya tidak memiliki `ghidraRun` atau `analyzeHeadless`. Karena analisis executable game belum dijalankan dengan Ghidra, hasil di bawah tetap merupakan fallback LLVM/heuristik, bukan daftar fungsi hasil Ghidra.

## Metode fallback

- Membaca hanya text block yang dinyatakan header PS-X EXE; membuat wrapper ELF sementara di luar repo agar LLVM dapat melakukan disassembly MIPS.
- Memindai kata 32-bit beralignment 4 byte untuk pola instruksi `jal`. Hasil hitungan meliputi kemungkinan false positive bila sebagian text berisi data/tabel.
- Men-disassemble jendela kecil di sekitar pemanggil `0x800115DC`; tidak melakukan dump/dekompilasi seluruh executable.

## Ringkasan hasil

| Ukuran | Hasil |
|---|---:|
| Ukuran text yang dipindai | 382.976 byte (`0x5D800`) |
| Kata 32-bit yang diperiksa | 95.744 |
| Kata yang cocok dengan opcode `jal` dan target di dalam text | 2.873 call sites |
| Alamat target `jal` unik di dalam text | 898 kandidat |
| Kandidat dengan penyesuaian stack negatif dalam 4 instruksi awal | 538 |
| Kandidat dengan penyimpanan `$ra` ke stack dalam 6 instruksi awal | 461 |
| Target `jal` unik di luar text tetapi dalam rentang RAM `0x80000000..0x801FFFFF` | 9 (10 call sites) |

Angka-angka di atas **tidak** boleh ditafsirkan sebagai jumlah fungsi sebenarnya. Alamat target langsung adalah kandidat awal; fungsi yang dipanggil lewat pointer, entry yang tidak dipanggil dengan `jal`, blok data, serta kode overlay memerlukan analisis yang lebih lengkap.

## Temuan terpilih

1. Pemanggilan di `0x800115DC` memiliki target efektif `0x800AD454`, di luar rentang text executable utama. Target ini konsisten dengan alamat rutin yang sudah dicatat dalam `docs/RESOURCE_CATALOG.md` sebagai bagian kode/loader yang perlu dianalisis di konteks `DATA.BIN`. **Keyakinan: mungkin** bahwa ini jalur ke kode overlay; relokasi dan rentang instruksi target belum divalidasi langsung pada langkah ini.
2. Kandidat target internal dengan jumlah pemanggil tertinggi (bukan penamaan fungsi): `0x80037138` (78 sites), `0x8002DFE4` (52), `0x80035D48` (49), `0x80035E78` (45), `0x80035418` (43), `0x80022044` (40), `0x8002DEC4` (35), `0x80043D48` (33), `0x8002FBF4` (29), dan `0x800448F8` (28).
3. Target lain dalam rentang RAM, di luar text utama: `0x8007D5AC`, `0x800AF6B4`, `0x800AF6D4`, `0x8011E070`, `0x8011F1C8`, `0x80129EBC`, `0x80142A40`, dan `0x8017D5C0`. Semuanya perlu diperiksa satu per satu; alamat saja tidak membuktikan bahwa target adalah entry fungsi yang sah.

## Disassembly lokal terpilih

Jendela `0x800115A0..0x80011604` menunjukkan panggilan:

- `0x800115DC: jal 0x800AD454`
- delay slot `0x800115E0: addiu $4, $16, -0x27D0`

Disassembly berasal dari wrapper ELF sementara yang alamat text-nya dipasang pada `0x80010000`. Ini cukup untuk membuktikan bahwa kata instruksi yang terbaca mengodekan panggilan tersebut, tetapi bukan bukti bahwa seluruh `DATA.BIN` telah dipetakan dengan benar.

## Artefak kandidat

Indeks lengkap berisi 898 alamat target `jal` internal, jumlah caller, dua indikator prologue heuristik, dan satu caller contoh disimpan sebagai artefak kerja lokal `main_exe_function_candidates.tsv`. Artefak ini tidak berisi biner game. Versi file lengkap tersebut belum dimasukkan ke Git; ringkasan yang dapat ditinjau di repo ada dalam dokumen ini. Untuk mengulang scan pada salinan executable lokal, gunakan [tools/psx_exe_call_target_scan.py](../tools/psx_exe_call_target_scan.py); skrip menghasilkan TSV ke folder `out/` dan tidak memerlukan paket Python eksternal.

## Kesimpulan dan langkah lanjutan

- **Pasti:** executable/header dan batas text telah diverifikasi pada langkah sebelumnya; LLVM dapat mendisassemble jendela terpilih pada alamat yang dipasang dari header.
- **Mungkin:** setidaknya beberapa call sites menuju kode yang berada di luar text executable utama, termasuk `0x800AD454`, sehingga pemetaan loader/overlay relevan.
- **Belum diketahui:** daftar fungsi definitif, batas setiap fungsi, lokasi roulette/battle/Chakra/RNG.
- Langkah berikutnya: sediakan salinan `SLPS_035.53` ke runner melalui mekanisme privat yang aman (bukan Git), jalankan `analyzeHeadless` dengan bahasa MIPS little-endian 32-bit pada `0x80010000`, lalu ekspor symbol/function entry ke artefak teks. Jangan mengklaim fallback ini sebagai output Ghidra.


## Pembaruan pipeline Ghidra — 27 Oktober 2026

Pipeline untuk tahap berikutnya sudah dibuat: [workflow Ghidra statis](../.github/workflows/ghidra-static-analyze-psx-exe.yml), skrip persiapan entrypoint, dan skrip ekspor TSV [`tools/ghidra/ExportFunctionIndex.java`](../tools/ghidra/ExportFunctionIndex.java). Namun ini baru **pipeline siap konfigurasi**, bukan hasil analisis Ghidra.

Run memerlukan Actions secret `PSX_EXE_DOWNLOAD_URL` berisi direct-download HTTPS privat. Biner divalidasi terhadap ukuran 385.024 byte, magic `PS-X EXE`, dan SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`. Tanpa secret tersebut, belum ada fungsi hasil Ghidra dan fallback di atas tetap satu-satunya indeks yang tersedia. Panduan: [`docs/GHIDRA_PRIVATE_EXE_HANDOFF.md`](../docs/GHIDRA_PRIVATE_EXE_HANDOFF.md). Workflow menyimpan hanya teks sebagai artefak; executable dan project sementara dibersihkan dari runner.
