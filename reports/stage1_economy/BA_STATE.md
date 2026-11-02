# BA_STATE — urutan BA1 → BA2 → BA3
Tanggal: 2026-11-02
Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`
Baseline yang diminta: `a3dbdd0375b732928e876954e9a662c69785c00c`
Status file ini: checkpoint kemajuan sementara; BA1 belum tuntas.

## Status per butir

| Butir | Status | Kepastian | Ringkasan |
|---|---|---:|---|
| BA1 | BERJALAN / SEBAGIAN | K3 | Ghidra mengurai loader FUN_800F7ADC dan menegaskan header count + 22? record 0x1E; byte mapping setiap field runtime tile telah didump. Resource spesifik belum ditemukan; two callers dan empat helper parser sedang diekspor. Run 41414694038 aktif. |
| BA2 | BELUM | K0 | Belum dimulai. |
| BA3 | BELUM | K0 | Belum dimulai; runtime harus tetap H6/hibrida dan ≥2 peluncuran. |

## PC/SHA kunci BA1

- Loader tile: `FUN_800F7ADC`, alamat kandidat impor Entry 1.
- Helper pemilih nilai per-level: `FUN_800B770C`; selector byte +0x0B tidak dianggap level Barrier.
- Sumber record stride: `0x1E` byte; runtime tile stride: `0x124` byte.
- Salinan yang telah didukung catatan statis sebelumnya: source `+0x14/+0x15` → runtime tile `+0x1A/+0x1B`.
- DATA.BIN: 66,015,232 byte; SHA-256 `69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822`.
- Entry 1: file offset `0x10BB000`, 596,412 byte; SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`; base impor `0x800AD450` hanya kandidat statis, runtime mapping belum tervalidasi.
- DATA.BIN directory: bootstrap +0x44, 1,504 entri × 8 byte; 1,500 aktif dan 4 kosong.
- Pengamatan pengguna 60/140/265/530, harga 120 adalah input uji, bukan nilai sumber yang sudah cocok.

## Actions yang sudah berjalan

1. Run `41413492667`, job `125171706081`, source SHA `7401c086ae7bba001143cb268c445c59bc30ebd6`: workflow conclusion failure, Ghidra step shell exit 127 karena baris terakhir `-postScript ExportTileResourceLoader...` tidak disambung ke `-analysisTimeoutPerFile`. Ekstraksi/inventaris dan cleanup lulus. Ringkasan Action sudah dikomit di:
   `reports/stage1_economy/aq1-run-41413492667/attempt-1/ACTIONS_RUN_SUMMARY.txt`
   Hasil scan: `BA1_DATA_SCAN_SUMMARY.txt` menyebut 0 raw candidate; ini belum menguji resource PK02 terdekompresi.
2. Perbaikan shell continuation dikomit pada source SHA `0a33f7bb3aa00c1ded456f5874d60d13384d2826`.
3. Run ulang: `41413850863`, job `125172847213`, status terakhir yang terlihat `in_progress`. Periksa hasil dan log sebelum menyatakan BA1.

## Mapping byte loader (K4 statis untuk mapping saja; belum berarti BA1 selesai)

`FUN_800F7ADC` static body at `ba1-tile-resource-loader.txt`:
- buffer[0] = record count; `record_ptr = buffer + 1`; `record_ptr += 0x1E` per item.
- Record +0,+1,+2,+3,+4 -> tile +0,+1,+2,+3,+4.
- Record +6 -> tile +5; record +5 is not copied. Tile +6 initialized 0.
- Record +7/+8 -> tile hw +0x0E.
- Record +9/+10 -> tile hw +0x10.
- Record +11/+12 -> tile hw +0x12.
- Record +13/+14 -> tile hw +0x14.
- Record +15/+16 -> tile hw +0x16.
- Record +17/+18 -> tile hw +0x18.
- Record +19/+20 -> tile hw +0x1A (price source candidate).
- Record +21/+22 -> tile hw +0x1C.
- Record +23/+24 -> tile hw +0x1E.
- Tile hw +0x20 initialized to constant `0xF020`; record +25/+26 -> tile hw +0x22; +27/+28 -> tile hw +0x24; record +29 -> tile byte +0x0C.
- This confirms source→runtime layout statically at the function under import base `0x800AD450` (not runtime validation). It does not prove which resource is Stage 1's 22-record table.

## Langkah berikut

1. Selesaikan run `41413850863`; periksa `ba1-tile-resource-loader.txt`, khususnya argumen loader, sumber resource ID, parser source→runtime byte mapping, dan helper yang menangani resource.
2. Dengan ID/offset sumber yang dibuktikan loader, ekstrak persis 22 × 0x1E record ke TSV. Jika resource berbentuk PK02, telusuri decoder yang dipanggil loader; jangan menyimpulkan tidak ada tabel dari scan byte mentah.
3. Verifikasi semua field runtime +0x10..+0x1E (halfword), field harga +0x1A dan nibble level bits 8–11 di +0x20. Uji HA dan HB dengan nilai observasi, catat cocok/tidak dan falsifier; jika tidak terbukti, tetap TIDAK TAHU.
4. Commit hasil final BA1 bersama pembaruan file ini. Baru setelah BA1 tuntas, mulai BA2.

## Batas tetap

- Jangan mengulang AZ0–AZ3.
- B44 bukan Barrier Release; jangan menautkan jalur B44 ke 結界開放.
- Tidak ada klaim runtime K5 dari analisis statis.
- Jangan upload ISO/BIOS/savestate/dump RAM/video/frame atau ubah Release/visibilitas repo.
- Jangan menamai aksi/gameplay dari nilai manager tanpa producer/caller yang membuktikan.
