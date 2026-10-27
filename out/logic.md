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
- Langkah 3 — analisis MIPS/Ghidra headless dan ekspor fungsi: **belum dilakukan**.
- Tidak ada ROM, BIOS, savestate, Memory Card, atau bukti privat yang ditambahkan ke repositori.

## Langkah 3 — pemetaan awal fungsi (status parsial)

Ghidra headless **belum dijalankan** karena `ghidraRun`/`analyzeHeadless` tidak terpasang di lingkungan kerja. Ghidra terbaru yang diperiksa berukuran sekitar 570 MB dan mensyaratkan JDK 25, sedangkan lingkungan ini menyediakan JDK 21. Tidak ada klaim bahwa daftar fungsi Ghidra telah diekspor.

Fallback LLVM/heuristik disimpan pada [`out/main_exe_callscan.md`](main_exe_callscan.md):
- 95.744 kata 32-bit dalam text block dipindai untuk pola `jal`.
- Ditemukan 2.873 call-site ber-target di dalam text dan 898 alamat target unik sebagai **kandidat**, bukan 898 fungsi terverifikasi.
- Ditemukan 9 alamat target unik di luar text tetapi dalam rentang RAM, termasuk target efektif `0x800AD454` yang dipanggil dari `0x800115DC`; ini konsisten dengan perlunya menelusuri kode overlay, tetapi belum membuktikan pemetaan overlay.
- Satu jendela kecil `0x800115A0..0x80011604` didisassemble saja; seluruh executable tidak di-dump.

Artefak teks kandidat lokal `main_exe_function_candidates.tsv` berisi 898 kandidat, jumlah pemanggil, indikator prologue heuristik, dan satu caller contoh. Artefak itu tidak memuat biner game dan belum di-commit ke Git.

### Keputusan status

- Langkah 1 — inventaris disc: **SELESAI berdasarkan catatan ekstraksi terdahulu**.
- Langkah 2 — validasi header PS-X EXE: **SELESAI dan diverifikasi langsung**.
- Langkah 3 — Ghidra headless: **BELUM SELESAI**; fallback statis awal tersedia.
- Story Mode dan pemain adaptif tetap **NOT COMPLETE / dijeda**, tidak ada emulator atau input gameplay dijalankan.

