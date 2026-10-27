# Indeks panggilan executable utama — scan statis pendahuluan

Tanggal pemeriksaan: 2026-10-27  
Sumber lokal: `SLPS_035.53`, ukuran 385.024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.  
Cakupan kode dari header: file offset `0x800..0x5DFFF`, alamat muat `0x80010000`, ukuran text `0x5D800`. Biner tetap di luar Git.

## Status Langkah 3 — selesai

Ghidra 12.2 headless analysis **berhasil dijalankan atas executable itu sendiri** pada Actions run [#40438574949](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40438574949). File `SLPS_035.53` diekstrak sementara dari BIN/CUE Release, lalu lolos pemeriksaan ukuran 385.024 byte, signature `PS-X EXE`, dan SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.

Ghidra memakai `MIPS:LE:32:default`, load base `0x80010000`, file offset `0x800`, panjang text `0x5D800`, dan entry point `0x80011448`. Analisis dan post-script sukses; `functions.tsv` berisi **1.206 fungsi** (1.207 baris termasuk header). Hasil teks tersedia di [artefak run #40438574949](https://api.github.com/repos/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/artifacts/12704922603), dengan retensi hingga 10 November 2026. Tidak ada executable atau proyek Ghidra yang dimasukkan ke artefak atau Git, dan tidak ada emulator/gameplay dijalankan.

Indeks ini adalah output Ghidra terverifikasi; hasil fallback di bawah tetap hanya heuristik panggilan dan bukan jumlah fungsi.

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


## Pembaruan Ghidra terverifikasi — 27 Oktober 2026

Run [#40438574949](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40438574949) menyelesaikan pipeline Ghidra: source BIN/CUE tervalidasi, executable diekstrak dan hash cocok, pemindaian RNG berhasil, Ghidra auto-analysis sukses, dan ekspor fungsi sukses (1.206 fungsi). Tidak diperlukan repository secret; workflow menggunakan release-asset API yang tersedia di repo. Artefak teks: [ghidra-slps-03553-function-index](https://api.github.com/repos/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/artifacts/12704922603).

Indeks Ghidra mengidentifikasi fungsi yang memuat empat call-site RNG:

- `0x80015B14` berada dalam `FUN_80015adc` (entry `0x80015ADC`, 160 byte).
- `0x80015BF0` berada dalam `FUN_80015b7c` (entry `0x80015B7C`, 240 byte).
- `0x8001A460` berada dalam `FUN_8001a328` (entry `0x8001A328`, 376 byte).
- `0x80020C24` berada dalam `FUN_80020bf4` (entry `0x80020BF4`, 156 byte).

Label `FUN_...` adalah nama default dari Ghidra, bukan fungsi semantik yang sudah diketahui. Rutinitas LCG ada pada `0x80035D78`; setter yang diduga seed setter berada pada `0x80035DA8`, tetapi indeks tidak mendeteksi entry terpisah pada alamat setter dan tidak ada direct-JAL caller setter yang terdeteksi di main text. Langkah 4 sekarang dapat dilanjutkan dengan memeriksa dekompilasi terbatas keempat caller, xref global `0x800A3118`, dan kode/overlay tanpa menyatakan fitur gameplay sebelum efek samping membuktikannya. Detail: [out/rng_candidate.md](rng_candidate.md).

Batas: keberhasilan analisis kode statis bukan bukti bahwa aturan roulette, battle, biaya Chakra, barrier atau kemenangan telah dipahami. Status Story Mode/adaptive player tetap NOT COMPLETE / paused; cue UNKNOWN, `barrier_level_selection = WAIT`, readiness NO-GO, Revision65 unchanged.
