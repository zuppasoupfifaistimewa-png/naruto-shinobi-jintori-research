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
