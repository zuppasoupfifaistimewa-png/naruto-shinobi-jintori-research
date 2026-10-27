# Scan signature generator RNG — 27 Oktober 2026

Run: [#40455975609](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455975609)  
Artefak teks: `step4-rng-resource-reference-scan` #12712700556.

## Cakupan

Scan statis mencari pasangan instruksi MIPS yang membentuk konstanta pengali `0x41C64E6D` dari `LUI 0x41C6` diikuti `ORI/ADDIU 0x4E6D` pada register yang sama, lalu instruksi MULT/MULTU dalam jendela 8 word. Ini hanya detector pola: temuan perlu konteks disassembly dan ketidakadaan bukan bukti absolut.

Semua file yang discan cocok dengan ukuran dan SHA-256 baseline:
- `SLPS_035.53`: 385.024 byte; SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
- `DATA.BIN`: 66.015.232 byte; SHA-256 `69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822`.
- `DATA2.BIN`: 166.428.672 byte; SHA-256 `be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9`.
- `DUMMY.BIN`: 50.667.520 byte; SHA-256 `cac5c852e95c90475a2879f51b6b949afea2df0cb540b2a2743bd791af4c47a2`.
- `XASECT.BIN`: 692 byte; SHA-256 `df257fbdabdb848f845466246abf4a36fdb6cf17815fc3a76ff7d7585d1953f0`.

## Hasil signature

| File | Konstruksi `0x41C64E6D` + MULT yang cocok | Instruksi dengan immediate `0x3039` |
|---|---:|---:|
| `SLPS_035.53` | **1** | **1** |
| `DATA.BIN` | 0 | 29 |
| `DATA2.BIN` | 0 | 2 |
| `DUMMY.BIN` | 0 | 0 |
| `XASECT.BIN` | 0 | 0 |

Satu kandidat di executable utama ada pada:
- `LUI` file offset `0x26578` → alamat program `0x80035D78`.
- `ORI/ADDIU` file offset `0x26584` → alamat program `0x80035D84`.
- `MULT/MULTU` terkait file offset `0x26588` → alamat program `0x80035D88`.
- Instruksi immediate `0x3039` file offset `0x26590` → alamat program `0x80035D90`.

Alamat tersebut cocok dengan rutin LCG main EXE yang sudah ditelusuri. Ini tidak mengidentifikasi generator lain dengan konstanta berbeda; ini hanya berarti scan tidak menemukan pengulangan signature khusus LCG yang sama dalam byte resource yang diperiksa. 29 hit immediate `0x3039` pada DATA.BIN dan dua hit di DATA2.BIN tidak dianggap generator RNG karena tidak disertai konstruksi pengali yang dicari.

## Kesimpulan dengan keyakinan

- **Pasti:** signature dari LCG yang diketahui ditemukan pada `0x80035D78` di executable utama.
- **Tidak ditemukan:** materialisasi pengali yang sama dan MULT terkait pada raw `DATA.BIN`, `DATA2.BIN`, `DUMMY.BIN`, atau `XASECT.BIN`.
- **Belum diketahui:** RNG alternatif dengan konstanta lain; fungsi RNG pada resource setelah dekompresi/dekripsi; pemanggilan via pointer/jump table yang tidak berbentuk direct JAL.
- Pemindaian tidak menjalankan emulator/gameplay dan tidak mengunggah biner sebagai artefak.
