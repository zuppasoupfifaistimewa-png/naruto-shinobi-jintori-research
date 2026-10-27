# Logika game — Naruto: Shinobi no Sato no Jintori Gassen (PS1)

Status: riset logika gameplay; pemain adaptif tetap dijeda.
Aturan: catat hanya bukti, pisahkan fakta dari hipotesis, jangan commit ROM/BIOS/savestate/Memory Card/bukti privat.

## Langkah 1 — identitas disc dan daftar file

Status langkah: **SELESAI BERDASARKAN CATATAN EKSTRAKSI LOKAL TERDAHULU**. Ekstraksi tidak dijalankan ulang pada putaran ini.

### Identitas disc

- File sumber: `Naruto - Shinobi no Sato no Jintori Gassen (Japan).bin`
- Ukuran: **325.989.552 byte**
- Format: raw-sector PS1, **2.352 byte/sektor**
- Jumlah sektor hasil pembagian ukuran: **138.601**
- Serial disc: **SLPS-03553**
- CRC32 tercatat: `dfe1f8b3`
- SHA-256 tercatat: `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`

### File pada filesystem disc yang diekstrak

| File | Ukuran byte | Interpretasi saat ini |
|---|---:|---|
| `SLPS_035.53` | 385.024 | executable utama PS-X EXE |
| `DATA.BIN` | 66.015.232 | berisi bootstrap dan direktori resource 1.504 entri; sebagian resource belum diidentifikasi |
| `DATA2.BIN` | 166.428.672 | file besar; fungsi/format internal belum dipetakan penuh |
| `DUMMY.BIN` | 50.667.520 | belum dipetakan penuh |
| `SYSTEM.CNF` | 68 | konfigurasi boot |
| `XASECT.BIN` | 692 | format/tujuan belum dipastikan |

### Konfigurasi boot

`SYSTEM.CNF` tercatat berisi:

- `BOOT = cdrom:\\SLPS_035.53;1`
- `TCB = 4`
- `EVENT = 16`
- `STACK = 801fff00`

### Tingkat keyakinan

- **Pasti (berdasarkan catatan ekstraksi sebelumnya):** nama executable boot dan ukuran enam file di atas, sebagaimana dicatat di `docs/ROM_STRUCTURE.md`.
- **Pasti (catatan checksum lokal sebelumnya):** CRC32/SHA-256 yang tercantum; checksum ini belum dihitung ulang dalam putaran ini.
- **Mungkin:** `DATA.BIN` memuat resource yang dapat menyertakan kode/overlay. Instruksi MIPS yang tampak di dalam file besar tidak dengan sendirinya membuktikan alamat muat runtime atau fungsinya.
- **Belum diketahui:** file/overlay mana yang mengimplementasikan roulette, klaim wilayah, biaya/rampas Chakra, battle, syarat menang, dan RNG.

### Provenance

Temuan ini disalin dari `docs/ROM_STRUCTURE.md` dan `docs/RESOURCE_CATALOG.md`, yang mendokumentasikan analisis lokal terdahulu. File disc dan file hasil ekstraksi tetap di luar Git; tidak ada biner game yang ditambahkan ke repo.

## Status langkah berikutnya

- Langkah 2 — membaca/memvalidasi header PS-X EXE: **belum dilakukan ulang pada putaran ini**; nilai header tercatat di `docs/ROM_STRUCTURE.md`.
- Langkah 3–10 — menelusuri fungsi dan membuktikan rumus gameplay: **belum selesai**.

## Langkah 2 — validasi header PS-X EXE

Status langkah: **SELESAI — header dibaca langsung dari salinan Library** pada putaran ini. File tidak dijalankan dan tidak didekompilasi.

### Hasil pembacaan

| Field | Offset header | Nilai | Makna |
|---|---:|---:|---|
| Magic | `0x00` | `PS-X EXE` | Signature executable PS1 |
| Initial PC / entry point | `0x10` | `0x80011448` | Alamat instruksi awal |
| Initial GP | `0x14` | `0x00000000` | Nilai GP yang tersimpan di header |
| Text load address | `0x18` | `0x80010000` | Alamat muat blok program |
| Text size | `0x1C` | `0x0005D800` (382.976 byte) | Ukuran blok program menurut header |
| Data load address/size | `0x20/0x24` | `0 / 0` | Tidak ada blok data terpisah yang dideklarasikan pada field ini |
| BSS address/size | `0x28/0x2C` | `0 / 0` | Tidak ada BSS yang dideklarasikan pada field ini |
| Initial SP base | `0x30` | `0x801FFFF0` | Nilai stack awal pada header |
| Initial SP offset | `0x34` | `0` | Offset stack tambahan |

### Konsistensi ukuran dan alamat

- Ukuran file aktual: **385.024 byte** = `0x5E000`.
- Header PS-X EXE berukuran `0x800` byte; `0x800 + text_size(0x5D800) = 0x5E000`. Ukuran cocok tepat dengan akhir file.
- Rentang alamat program berdasarkan load address + text size adalah `[0x80010000, 0x8006D800)`.
- Entry point `0x80011448` berada di dalam rentang tersebut; offset entry point dari awal blok muat adalah `0x1448`.

### Hash dan tingkat keyakinan

- SHA-256 file yang dibaca: `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`; sama dengan hash yang tercatat di `docs/ROM_STRUCTURE.md` dan `docs/RESOURCE_CATALOG.md`.
- **Pasti:** nilai byte header, ukuran file, kecocokan ukuran text dengan file, dan entry point berada di rentang text. Nilai dihitung dari file lokal dan diverifikasi terhadap catatan lama.
- **Mungkin:** kode gameplay penting juga dimuat dari resource/overlay lain. Header ini hanya mendeskripsikan executable utama; tidak cukup untuk menyatakan roulette, battle, transaksi Chakra, atau RNG berada di file ini.
- Catatan perbedaan yang perlu dipertahankan: `SYSTEM.CNF` mencatat `STACK = 801fff00`, sedangkan header EXE memiliki initial SP base `0x801FFFF0`. Ini adalah field berbeda pada dua sumber; jangan menyamakannya atau menyimpulkan bug tanpa menelusuri loader.

## Status setelah Langkah 2

- Langkah 1 — identitas disc dan listing file: **SELESAI dari catatan ekstraksi terdahulu**.
- Langkah 2 — validasi header: **SELESAI**.
- Langkah 3 — penyiapan Ghidra headless di GitHub Actions: **selesai**; analisis executable dan ekspor fungsi: **belum dilakukan** (run [#40434733043](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40434733043) memverifikasi launcher saja).
- Tidak ada ROM, BIOS, savestate, Memory Card, atau bukti privat yang ditambahkan ke repositori.

## Langkah 3 — pemetaan awal fungsi (status parsial)

Ghidra 12.2 dan Temurin JDK 25 **sudah dipasang serta launcher `support/analyzeHeadless` telah diverifikasi pada GitHub Actions** di run [#40434733043](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40434733043). Eksekusi Ghidra untuk mengimpor dan menganalisis `SLPS_035.53` **belum dilakukan**, sehingga daftar fungsi Ghidra belum diekspor.

Fallback LLVM/heuristik disimpan pada [`out/main_exe_callscan.md`](main_exe_callscan.md):
- 95.744 kata 32-bit dalam text block dipindai untuk pola `jal`.
- Ditemukan 2.873 call-site ber-target di dalam text dan 898 alamat target unik sebagai **kandidat**, bukan 898 fungsi terverifikasi.
- Ditemukan 9 alamat target unik di luar text tetapi dalam rentang RAM, termasuk target efektif `0x800AD454` yang dipanggil dari `0x800115DC`; ini konsisten dengan perlunya menelusuri kode overlay, tetapi belum membuktikan pemetaan overlay.
- Satu jendela kecil `0x800115A0..0x80011604` didisassemble saja; seluruh executable tidak di-dump.

Artefak teks kandidat lokal `main_exe_function_candidates.tsv` berisi 898 kandidat, jumlah pemanggil, indikator prologue heuristik, dan satu caller contoh. Artefak itu tidak memuat biner game dan belum di-commit ke Git.

### Keputusan status

- Langkah 1 — inventaris disc: **SELESAI berdasarkan catatan ekstraksi terdahulu**.
- Langkah 2 — validasi header PS-X EXE: **SELESAI dan diverifikasi langsung**.
- Langkah 3 — penyiapan Ghidra headless di Actions: **SELESAI**; analisis executable dan ekspor fungsi Ghidra: **BELUM SELESAI**.
- Story Mode dan pemain adaptif tetap **NOT COMPLETE / dijeda**, tidak ada emulator atau input gameplay dijalankan.

Skrip scan yang dapat diulang pada salinan executable lokal: [`tools/psx_exe_call_target_scan.py`](../tools/psx_exe_call_target_scan.py). Skrip menulis indeks target/caller sebagai teks ke folder `out/`; biner tetap lokal. Hasil fallback dan batas interpretasinya dicatat di [`out/main_exe_callscan.md`](main_exe_callscan.md).


## Pembaruan jalur Ghidra — 27 Oktober 2026

Pipeline analisis statis kini disiapkan di workflow [`ghidra-static-analyze-psx-exe.yml`](../.github/workflows/ghidra-static-analyze-psx-exe.yml), dengan skrip [`PreparePsxExe.java`](../tools/ghidra/PreparePsxExe.java) dan [`ExportFunctionIndex.java`](../tools/ghidra/ExportFunctionIndex.java). Workflow mengimpor hanya rentang text dari offset file `0x800`, memakai bahasa `MIPS:LE:32:default` di `0x80010000`, membuat entrypoint `0x80011448`, lalu menulis indeks fungsi dalam TSV.

**Status: pipeline sudah ditambahkan, eksekusi analisis belum dimulai.** Runner membutuhkan repository Actions secret `PSX_EXE_DOWNLOAD_URL` yang mengarah ke unduhan HTTPS privat executable tepat 385.024 byte. Ukuran, magic `PS-X EXE`, dan SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569` diverifikasi sebelum Ghidra dijalankan. Jika tidak cocok, file ditolak dan dihapus.

Panduan setelan satu kali: [`docs/GHIDRA_PRIVATE_EXE_HANDOFF.md`](../docs/GHIDRA_PRIVATE_EXE_HANDOFF.md). Konektor yang tersedia tidak dapat membuat secret Actions atau menyalin biner Library langsung ke runner; karena itu run belum bisa dipicu sebelum secret dibuat oleh pemilik repo. Biner tidak masuk Git maupun artefak; yang diunggah hanya laporan/log teks. Tidak ada emulator atau input gameplay dijalankan.


## Langkah 4 — temuan awal RNG (27 Oktober 2026)

Analisis statis lokal yang dapat direproduksi menemukan pola LCG eksak di `0x80035D78`, state di `0x800A3118`, pengali `0x41C64E6D`, penambah `0x3039`, dan output `(state >> 16) & 0x7FFF`. Rutin di `0x80035DA8` menulis argumen pertama ke state yang sama dan berperilaku seperti seed setter.

Direct-JAL callers yang ditemukan di text utama: `0x80015B14`, `0x80015BF0`, `0x8001A460`, `0x80020C24`. Belum diketahui pemanggil via pointer/overlay, seed awal, atau fungsi gameplay tiap caller. Laporan lengkap: [`out/rng_candidate.md`](rng_candidate.md); skrip reproduksi: [`tools/psx_rng_signature_scan.py`](../tools/psx_rng_signature_scan.py).

**Status langkah:** Langkah 4 menemukan kandidat RNG dengan keyakinan tinggi menggunakan fallback statis lokal, tetapi pemetaan ke fungsi/domain gameplay menunggu xref Ghidra. Langkah 3 Ghidra masih parsial/belum selesai: pipeline sudah dibuat, tapi runner belum menerima input privat. Tidak ada emulator/input gameplay yang dijalankan.


Penyelarasan pipeline setelah temuan Langkah 4: workflow [`ghidra-static-analyze-psx-exe.yml`](../.github/workflows/ghidra-static-analyze-psx-exe.yml) sekarang juga menjalankan `tools/psx_rng_signature_scan.py` terhadap executable yang sama setelah validasi hash. Jika handoff privat selesai, satu run akan menghasilkan daftar fungsi Ghidra dan laporan signature/caller RNG dalam satu artefak teks.


## Koreksi status — Ghidra dan langkah 4 (27 Oktober 2026)

Bagian status langkah 3 yang lebih lama di atas ditulis sebelum analisis executable benar-benar berhasil. **Gunakan bagian ini sebagai status terbaru.**

### Langkah 3 — impor, auto-analysis, dan ekspor fungsi Ghidra

**SELESAI.** GitHub Actions run [#40438574949](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40438574949) berhasil dengan Ghidra 12.2, Temurin JDK 25, dan bahasa `MIPS:LE:32:default`. Runner mengekstrak `SLPS_035.53` sementara dari aset BIN/CUE Release; input cocok dengan ukuran 385.024 byte, signature `PS-X EXE`, dan SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.

Pengaturan impor: file offset `0x800`, ukuran text `0x5D800`, load base `0x80010000`, entry point `0x80011448`. Pesan log mengonfirmasi `Analysis succeeded` dan `Post-analysis succeeded`. Export `functions.tsv` selesai dengan **1.206 fungsi**. Artefak teks yang dapat diunduh: [ghidra-slps-03553-function-index (run #40438574949)](https://api.github.com/repos/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/artifacts/12704922603). Binary dan proyek sementara tidak dimasukkan ke Git atau artefak; tidak ada emulator/gameplay dijalankan.

### Langkah 4 — RNG: bukti statis dan peta caller awal

- **Keyakinan tinggi:** generator LCG pada `0x80035D78` menggunakan state `0x800A3118`, dengan rumus `state = state * 0x41C64E6D + 0x3039` (modulo (2^{32})), kemudian mengembalikan `(state >> 16) & 0x7FFF`.
- **Keyakinan tinggi:** `0x80035DA8` menulis argumen `$a0` ke state yang sama; perilaku cocok dengan setter seed. Namun, Ghidra auto-analysis tidak mengekspor entry fungsi terpisah pada alamat itu dan scan tidak menemukan direct-JAL caller di main text. Seed awal belum diketahui.
- Scan menemukan empat direct-JAL call sites pada main text, dan indeks Ghidra memetakan ke fungsi pemanggil:
  - `0x80015B14` dalam `FUN_80015adc` (entry `0x80015ADC`, 160 byte).
  - `0x80015BF0` dalam `FUN_80015b7c` (entry `0x80015B7C`, 240 byte).
  - `0x8001A460` dalam `FUN_8001a328` (entry `0x8001A328`, 376 byte).
  - `0x80020C24` dalam `FUN_80020bf4` (entry `0x80020BF4`, 156 byte).
- Nama `FUN_...` ialah label default, bukan pengetahuan tentang makna gameplay. Konteks caller awal mendukung kemungkinan shuffle/permutasi pada salah satu rutin dan indeks pilihan berbatas pada lainnya, tetapi tujuan tabel/field belum dipastikan.
- Scan ini hanya menghitung direct-JAL pada text executable utama; pemanggilan tak langsung, seed initialization, dan kode/resource overlay belum tercakup.

Detail dan link artefak: [out/rng_candidate.md](rng_candidate.md), [out/main_exe_callscan.md](main_exe_callscan.md).

### Langkah berikutnya

Lanjutkan Langkah 4 secara terfokus: dekompilasi terbatas empat fungsi pemanggil, kumpulkan xref load/store untuk global `0x800A3118`, dan inspeksi instruksi tepat pada setter `0x80035DA8`. Jangan menyebut caller sebagai roulette, battle, AI, atau mekanik gameplay sebelum flow, tabel, dan efek samping menunjukkan hubungan itu. Status adaptive player tetap dijeda: target cue UNKNOWN, `barrier_level_selection = WAIT`, readiness NO-GO, Story Mode NOT COMPLETE, Revision65 tidak diubah.


## Hasil lanjutan Langkah 4 — dekompilasi empat caller RNG (27 Oktober 2026)

Pembaruan ini menggantikan daftar pekerjaan Langkah 4 sebelumnya yang menyebut dekompilasi empat caller sebagai langkah berikutnya. Hasil bersumber dari artefak teks [run #40438911181](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40438911181); tidak ada emulator atau input gameplay.

1. `FUN_80015b7c` (entry `0x80015B7C`, 240 byte) mengulang hingga `4 * DAT_80070d02` iterasi ketika jumlah elemen bukan nol. Pada setiap iterasi ia mengambil RNG, menghitung indeks modulo jumlah elemen dan menukar dua byte dalam tabel mulai `DAT_80070d0a`. **Keyakinan tinggi:** shuffle/permutasi byte; domain tabel belum diketahui.
2. `FUN_8001a328` (entry `0x8001A328`, 376 byte) membuat daftar kandidat dari pemeriksaan `FUN_80016c68(0x7F..0x86)`, lalu memilih elemen dengan `RNG % jumlah_kandidat` dan menyimpannya ke `DAT_80089DA9`. **Keyakinan tinggi:** pemilih acak atas daftar kandidat yang difilter. Arti kode/state belum diketahui; label gameplay tidak ditebak.
3. `FUN_80015adc` (entry `0x80015ADC`, 160 byte) memeriksa batas dari helper `FUN_800154d4`, lalu menghitung indeks/offset dengan nilai `FUN_800158d8` dan RNG sebelum memanggil `FUN_800159bc`. **Keyakinan menengah:** pilihan indeks terbatas; makna semantik membutuhkan penelusuran helper/tabel.
4. `FUN_80020bf4` (entry `0x80020BF4`, 156 byte) menginisialisasi struktur kalau pointer valid dan field pertama belum bernilai 1, mengambil nilai RNG, menyimpan nilai 12-bit (`RNG % 0x1000`) ke `param_1[0xD]`, kemudian memanggil tiga helper. **Keyakinan menengah:** inisialisasi struktur dengan nilai pseudo-acak; hubungan dengan gameplay belum dibuktikan.

Ghidra hanya menemukan dua referensi langsung ke state global `0x800A3118` pada text utama: baca di `0x80035D80` dan tulis di `0x80035D98`, keduanya dalam LCG. Empat direct-JAL callers terpetakan pada tabel di [out/rng_candidate.md](rng_candidate.md). Query untuk reference langsung ke setter kandidat `0x80035DA8` menghasilkan nol; ini belum menyingkirkan caller tak langsung, alias atau kode overlay.

### Status Langkah 4

**SELESAI sebagai inventaris awal RNG + empat caller langsung dan dekompilasi tingkat pertama; BELUM SELESAI sebagai pemetaan RNG gameplay penuh.** Hal yang masih harus dikerjakan adalah menelusuri helper, sumber dan isi tabel `DAT_80070d02/DAT_80070d0a`, pemanggil `FUN_8001a328`, semua referensi ke `DAT_80089DA9`, pengguna `FUN_80020bf4`, serta seed setter/overlay. Jangan menyimpulkan aturan roulette, turn, battle, AI, hadiah atau kemenangan sebelum hubungan itu dibuktikan.

Adaptive player masih dijeda: target cue UNKNOWN, `barrier_level_selection = WAIT`, readiness NO-GO, Story Mode NOT COMPLETE, Revision65 tidak diubah.

## Langkah 4 selesai — helper RNG dan daftar kandidat (27 Oktober 2026)

Run Ghidra [#40439763833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40439763833) berhasil. Helper yang ditelusuri menunjukkan FUN_800154d4 membaca batas DAT_8006D794; FUN_800158d8 membaca jumlah di DAT_80070D02; FUN_800159bc menyisipkan byte kandidat ke daftar mulai DAT_80070D0A dengan batas maksimum 64 elemen; FUN_80015610 mengisi daftar dari tabel DAT_8005603C dengan sentinel 0xFF; FUN_80015b7c mengacak urutan; dan FUN_80016c68 menguji bit kandidat pada bitset DAT_80070770. FUN_8001a328 memilih acak dari nilai 0,1,2,3,4,5,8,9,0xB setelah pemeriksaan bit untuk kode 0x7F–0x86. Arti gameplay tabel dan nilai pilihan masih UNKNOWN. Laporan: [STEP4_RNG_TRACE_2026-10-27.md](../docs/STEP4_RNG_TRACE_2026-10-27.md).

## Langkah 5 selesai — survei entry resource DATA.BIN (27 Oktober 2026)

Ghidra menganalisis entry 1 pada offset 0x10BB000 (596.412 byte, SHA-256 potongan 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a) dengan base hipotesis 0x800D0000. Enam lokasi kandidat memanggil getter target Chakra 0x80012A70, membandingkan field record dengan nilai target, lalu mengubah field state/memanggil transisi pada jalur yang lolos. Dua call sites lain menuju getter berada di FUN_8012A9C4 dan FUN_80137AD8. Laporan lengkap: [STEP5_DATABIN_ENTRY1_ANALYSIS_2026-10-27.md](../docs/STEP5_DATABIN_ENTRY1_ANALYSIS_2026-10-27.md).

## Langkah 6 — antrean analisis statis berikutnya

Dekompilasi FUN_800EF98C, FUN_80100D14, FUN_80100DCC, FUN_8012A9C4, FUN_80137AD8, dan konsumen setter Chakra. Tujuannya mengenali transisi state/event, tabel record dan field terkait, bukan mengklaim hasil permainan. Base overlay 0x800D0000 tetap hipotesis. Status pemain adaptif tidak berubah: cue UNKNOWN, barrier_level_selection = WAIT, readiness NO-GO, Story Mode NOT COMPLETE, Revision65 tidak diubah.


## Checkpoint otoritatif audit Langkah 1–10 — 27 Oktober 2026

Bagian checkpoint ini memperbarui status yang tersebar dalam catatan historis di atas tanpa menghapus riwayat lama. Gunakan laporan audit terbaru untuk status per langkah dan batas bukti:

- Audit Langkah 1–10: [docs/REVERSE_ENGINEERING_AUDIT_STEPS_1_10_2026-10-27.md](../docs/REVERSE_ENGINEERING_AUDIT_STEPS_1_10_2026-10-27.md).
- Arsip permanen dekompilasi Ghidra/m2c untuk empat caller RNG: [out/step5/STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md](step5/STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md).
- HEAD saat awal audit: 62a4c114b7ac7a55ae9eb6d91bc4c9bfaef1c2ef. Analisis Ghidra terbaru [Actions #40442572534](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40442572534) berhasil dan menghasilkan 1.206 baris fungsi untuk executable utama. Step 5 Ghidra/m2c [Actions #40449144521](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40449144521) berhasil pada SHA tersebut; empat dari empat caller RNG memiliki output Ghidra dan m2c yang tersimpan permanen.
- Langkah 1–5 berstatus SELESAI dalam cakupan yang ditentukan dalam laporan. Langkah 6–8 dan 10 SELESAI SEBAGIAN; Langkah 9 TERBLOKIR karena belum ada uji fungsi MIPS terisolasi yang tervalidasi. Base DATA.BIN entry 1 0x800D0000 dan entry 0 0x800AD000 tetap hipotesis runtime.
- RNG terpetakan secara statis pada 0x80035D78 dengan state 0x800A3118 dan empat direct-JAL callers main EXE. Seed runtime dan caller tak langsung tetap UNKNOWN.
- Cabang resource yang membandingkan record terhadap getter target Chakra telah ditemukan secara statis, tetapi base resource, makna beberapa field/transisi, sumber delta +0xB30/+0xB38/+0xB40/+0xB44, dan apakah cabang tersebut berarti kemenangan Story Mode universal belum terbukti.
- Actions query pada audit tidak menemukan run aktif atau antrean. Tidak ada workflow gameplay/player dijalankan dalam sesi audit ini. Jangan mengubah marker Revision65, policy, atau readiness gate sebagai bagian dari reverse engineering statis.

Status laporan ini tidak menyatakan Story Mode tamat atau seluruh aturan permainan selesai direverse-engineer.
