# HA1 — Addendum koreksi offset dan excerpt instruksi (2026-11-07)

Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`  
Baseline inklusif: `14dccd2e1d2f92b1b919ad7f0686bf019c71dbf4`  
Analisis statis; tidak menjalankan emulator.

## (a) Offset Entry 1 yang benar

Rumus:
`file_offset = 0x10BB000 + (PC - 0x800AD450)`.

- `0x800F7E64 - 0x800AD450 = 0x4AA14`; `0x10BB000 + 0x4AA14 = 0x01105A14`.
- `0x800F7E68 - 0x800AD450 = 0x4AA18`; `0x10BB000 + 0x4AA18 = 0x01105A18`.

Hasil `0x01105A14/0x01105A18` terkonfirmasi hitung ulang. Pernyataan assistant sebelumnya yang menyebut `0x010FFA14/18` salah dan dicabut.

## (b) Dua instruksi negu dan pengisi register store

Baris `negu` tersedia pada `HA1_NEGU_ROWS.tsv`:
- PC `0x800F2E0C`, Entry 1 file offset `0x011009BC`, bytes `23 10 02 00`, `negu $v0,$v0`.
- PC `0x800F2E64`, Entry 1 file offset `0x01100A14`, bytes `23 10 02 00`, `negu $v0,$v0`.

Keduanya menegasikan nilai return helper `0x8001552C` yang masih berada di `$v0`; bukan `negu $v0,$zero`. File `HA1_STORE_F2CF8_WINDOW.tsv`, `HA1_STORE_F2E38_WINDOW.tsv`, dan `HA1_STORE_F2E68_WINDOW.tsv` dari run HA2/HA3 mencatat instruksi pengisi register di sekitar ketiga store. Masing-masing window dibatasi <=16 instruksi kontigu.

## (c) Helper 0x8001552C dipecah

Excerpt Ghidra lama 19 instruksi kini dipisah:
- `HA1_HELPER_8001552C_00.tsv`: 16 instruksi kontigu.
- `HA1_HELPER_8001552C_01.tsv`: 3 instruksi kontigu.

Setiap file memuat header `pc,file_offset,bytes,instruksi`. Offsets dihitung menurut EXE: `0x800 + (PC - 0x80010000)`.

## (d) Koreksi permalink

Permalink raw sebelumnya tidak semuanya layak dipakai: ada tautan dengan parameter tracking dan ada SHA yang salah/terpotong sehingga bukan permalink commit penuh 40-hex. Semua tautan lama tersebut dicabut. Gunakan hanya permalink raw di laporan akhir yang memiliki SHA penuh yang sudah dihitung panjangnya 40 karakter dan tanpa query parameter.

## Status

HA1: TUNTAS, K4 untuk dua negu, offset, dan pemecahan excerpt. Baris pengisi store yang dilampirkan dari hasil run akan tetap tunduk pada validasi decode bytes dan offset; hasil yang belum diverifikasi ditandai TIDAK TAHU.
