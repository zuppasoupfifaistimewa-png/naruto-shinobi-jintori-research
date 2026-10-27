# Kandidat RNG — analisis statis executable utama

Tanggal pemeriksaan: 27 Oktober 2026. Biner tidak dimasukkan ke Git.

- File lokal: `SLPS_035.53`, 385.024 byte.
- SHA-256 diverifikasi langsung: `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
- Header: PC `0x80011448`, base `0x80010000`, text `0x5D800`.

## Temuan

**Keyakinan tinggi:** alamat `0x80035D78` berisi rutin LCG yang menggunakan state global `0x800A3118`. Urutan instruksi diverifikasi dengan scan signature eksak dan disassembly LLVM atas text yang dimuat pada base alamat header.

Pseudocode yang cocok dengan instruksi:

```c
uint32_t state = *(volatile uint32_t *)0x800A3118;
state = state * 0x41C64E6D + 0x3039;  // modulo 2^32
*(volatile uint32_t *)0x800A3118 = state;
return (state >> 16) & 0x7FFF;
```

Pengali `0x41C64E6D` = 1.103.515.245; penambah `0x3039` = 12.345; hasilnya 15 bit. Instruksi kunci: `mult` di `0x80035D88`, `mflo` di `0x80035D8C`, update global di `0x80035D98`, shift di `0x80035D9C`, lalu mask `0x7FFF` pada delay slot `jr $ra` di `0x80035DA4`. Ini sangat cocok dengan fungsi `rand()`-like, tetapi tidak ada simbol debug untuk mengonfirmasi nama sumber.

Di `0x80035DA8` ada setter yang menulis argumen pertama `$a0` ke global yang sama: `lui $at,0x800A`, `jr $ra`, lalu `sw $a0,0x3118($at)` pada delay slot. Perilakunya cocok dengan `srand(seed)`-like. Tidak ditemukan direct-JAL caller untuk setter di text utama; seed awal dan jalur panggilan tak langsung/overlay belum diketahui.

## Direct-JAL callers ke RNG

| Call site | Petunjuk instruksi setelah kembali | Interpretasi awal |
|---|---|---|
| `0x80015B14` | Nilai dipindah ke register saved; jalur selanjutnya menggeser dan mem-mask ke 8 bit | Transformasi/indeks berbasis RNG, tujuan belum diketahui |
| `0x80015BF0` | Hasil `rand` diikuti `div`/ `mfhi` terhadap nilai tabel `lhu` | Konsisten dengan indeks modulo jumlah/nilai tabel |
| `0x8001A460` | Hasil diikuti `div`/ `mfhi` dengan pembagi register `$s0` | Konsisten dengan pilihan modulo batas |
| `0x80020C24` | Hasil langsung disimpan ke field struktur melalui pointer `$s0` | Semantik field belum diketahui |

Empat call site tersebut adalah direct-JAL yang ditemukan pada text utama. Itu **bukan** jumlah seluruh penggunaan RNG game; panggilan via pointer dan kode/overlay lain belum dihitung.

## Keyakinan dan batas

- **Pasti dari byte/hash yang diperiksa:** opcode berurutan pada dua alamat, konstanta, akses state, serta empat direct-JAL caller di atas.
- **Keyakinan tinggi:** `0x80035D78` adalah generator pseudo-acak LCG berperilaku seperti `rand()`; `0x80035DA8` adalah seed setter.
- **Belum diketahui:** seed awal, pemanggil via pointer/overlay, dan domain gameplay (roulette, turn, battle, AI, hadiah) yang mengonsumsi nilai.
- Hasil ini **bukan output Ghidra**. Langkah 3 Ghidra masih tertunda karena runner belum menerima input privat.

## Reproduksi

```bash
python3 tools/psx_rng_signature_scan.py /path/to/SLPS_035.53
```

Skrip memvalidasi header, SHA-256 dan urutan instruksi; ia tidak menjalankan executable game. Selanjutnya cocokkan caller ini dengan indeks fungsi Ghidra setelah handoff privat selesai, lalu cari semua xref ke `0x800A3118`.
