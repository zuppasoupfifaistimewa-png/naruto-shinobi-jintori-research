# Kandidat RNG — analisis statis executable utama

Tanggal pemeriksaan: 27 Oktober 2026. Biner tidak dimasukkan ke Git.

- File: `SLPS_035.53`, 385.024 byte.
- SHA-256 terverifikasi: `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
- Header: PC `0x80011448`, base `0x80010000`, text `0x5D800`.
- **Ghidra langkah 3 selesai:** run [#40438574949](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40438574949) berhasil menggunakan Ghidra 12.2, bahasa `MIPS:LE:32:default`, dan mengekspor 1.206 fungsi.
- **Analisis caller langkah 4 selesai untuk empat direct-JAL caller utama:** run [#40438911181](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40438911181) berhasil mengekspor dekompilasi terbatas, instruksi sekitar call site, serta xref ke state dan entry RNG.
- Artefak teks untuk analisis caller: [ghidra-slps-03553-function-index (run #40438911181)](https://api.github.com/repos/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/artifacts/12705950866). Artefak ini berisi TSV/log/dekompilasi teks saja, bukan executable atau proyek Ghidra.

## Temuan RNG

**Keyakinan tinggi:** alamat `0x80035D78` berisi rutin LCG yang menggunakan state global `0x800A3118`. Ghidra mengenali entry fungsi `FUN_80035d78` dengan tubuh sepanjang 48 byte hingga alamat `0x80035DA8`.

Pseudocode yang cocok dengan instruksi:

```c
uint32_t state = *(volatile uint32_t *)0x800A3118;
state = state * 0x41C64E6D + 0x3039;  // modulo 2^32
*(volatile uint32_t *)0x800A3118 = state;
return (state >> 16) & 0x7FFF;
```

Pengali `0x41C64E6D` = 1.103.515.245; penambah `0x3039` = 12.345; output 15 bit. Instruksi kunci: `mult` di `0x80035D88`, `mflo` di `0x80035D8C`, update global di `0x80035D98`, shift di `0x80035D9C`, lalu mask `0x7FFF` pada delay slot `jr $ra` di `0x80035DA4`. **Keyakinan tinggi:** ini generator pseudo-acak yang berperilaku seperti `rand()`; tidak ada simbol debug untuk mengonfirmasi nama sumber.

### Seed setter candidate

Di `0x80035DA8` ada setter yang menulis argumen pertama `$a0` ke global yang sama: `lui $at,0x800A`, `jr $ra`, lalu `sw $a0,0x3118($at)` pada delay slot. Perilakunya cocok dengan `srand(seed)`-like. Ghidra tidak membuat entry fungsi terpisah pada `0x80035DA8` dan xref query tidak menemukan referensi langsung ke alamat itu. Scan tidak menemukan direct-JAL caller setter pada main text. Seed awal, caller tidak langsung, dan kemungkinan penyiapan state oleh kode/overlay belum diketahui. Label “setter” masih interpretasi berdasarkan instruksi, bukan simbol sumber.

## Langkah 4 — direct-JAL callers ke RNG dan dekompilasi Ghidra

Semua pemetaan berikut berasal dari artefak output Ghidra run #40438911181 dan scan signature atas text executable utama. Nama `FUN_...` adalah label otomatis Ghidra, bukan nama semantik.

| Call site RNG | Fungsi pemanggil | Temuan dekompilasi dan penilaian |
|---|---|---|
| `0x80015B14` | `FUN_80015adc`, entry `0x80015ADC`, 160 byte | Membandingkan `param_2 & 0xFF` dengan nilai dari `FUN_800154d4`; jika lolos, mengambil nilai dari `FUN_800158d8`, memasukkan nilai RNG lalu nilai helper lain ke perhitungan modulo, dan memanggil `FUN_800159bc` dengan indeks yang dihasilkan serta parameter batas. **Keyakinan menengah:** pemilihan indeks/offset terbatas pada kumpulan berukuran variabel; objek yang dipilih dan tujuan gameplay belum teridentifikasi. |
| `0x80015BF0` | `FUN_80015b7c`, entry `0x80015B7C`, 240 byte | Jika `DAT_80070d02` bukan nol, loop menjalankan sampai `4 * DAT_80070d02` iterasi. Setiap iterasi menghasilkan RNG, menghitung dua indeks modulo jumlah elemen, lalu menukar byte di tabel mulai `DAT_80070d0a`. **Keyakinan tinggi:** operasi shuffle/permutasi byte pada tabel dengan urutan pertukaran berbasis RNG. Tujuan tabel tetap belum diketahui. |
| `0x8001A460` | `FUN_8001a328`, entry `0x8001A328`, 376 byte | Menginisialisasi daftar lokal; memanggil `FUN_80016c68` untuk kode `0x7F`–`0x86`, menambahkan kode hasil `0,1,2,3,4,5,8,9,0xB` bila pemeriksaan yang sesuai benar, lalu memilih satu elemen melalui `RNG % jumlah_kandidat`. Hasil disimpan ke `DAT_80089DA9`. **Keyakinan tinggi:** pemilih acak dari daftar kandidat yang difilter oleh kondisi. **Belum diketahui:** arti kode dan state global tersebut dalam gameplay. |
| `0x80020C24` | `FUN_80020bf4`, entry `0x80020BF4`, 156 byte | Jika pointer tidak nol dan field pertama bukan 1, menandai field sebagai 1, mengambil RNG, menyimpan nilai RNG modulo `0x1000` ke `param_1[0xD]`, kemudian memanggil `FUN_80020d48(param,0x1000)`, `FUN_80018300(0x4800,2,3,0,0)`, dan `FUN_80018468(0,0xB4)`. **Keyakinan menengah:** inisialisasi struktur dengan nilai pseudo-acak 12-bit; belum terbukti berkaitan langsung dengan mekanik gameplay. |

### Xref ke state RNG

Ghidra menemukan dua referensi langsung ke global `0x800A3118` dalam text executable utama:
- `0x80035D80`: baca state di dalam `FUN_80035d78`.
- `0x80035D98`: tulis state berikutnya di dalam `FUN_80035d78`.

Empat call sites langsung ke `0x80035D78` adalah `0x80015B14`, `0x80015BF0`, `0x8001A460`, dan `0x80020C24`. Query referensi langsung untuk alamat setter `0x80035DA8` menghasilkan nol. Hasil ini **tidak** menyingkirkan pointer/call tidak langsung, alias alamat, data yang menyiapkan state, atau kode overlay/resource di luar text executable utama.

## Keyakinan dan batas

- **Pasti dari analisis byte/Ghidra:** LCG dan alamat state; executable yang diperiksa cocok dengan SHA-256 tercatat; auto-analysis sukses; indeks berisi 1.206 fungsi; empat call sites langsung masuk ke fungsi yang disebutkan; hasil dekompilasi caller sebagaimana artefak.
- **Keyakinan tinggi:** `0x80035D78` adalah generator pseudo-acak; `FUN_80015b7c` melakukan shuffle/permutasi byte; `FUN_8001a328` memilih elemen acak dari daftar kandidat yang difilter.
- **Keyakinan menengah:** `FUN_80015adc` memilih indeks/offset terbatas; `FUN_80020bf4` menginisialisasi struktur dengan nilai 12-bit acak.
- **Belum diketahui:** seed awal; pemanggil tidak langsung dan overlay; pemetaan kode `0x7F`–`0x86` dan `DAT_80089DA9` ke fitur; apakah fungsi-fungsi terkait roulette, turn, battle, AI, atau hadiah.

Tidak ada emulator atau input gameplay yang dijalankan. Analisis statis tidak membuktikan aturan gameplay tanpa pemetaan tabel/state tambahan.

## Langkah 4 — kelanjutan yang tepat

1. Telusuri `FUN_800154d4`, `FUN_800158d8`, dan `FUN_800159bc` untuk mengetahui domain indeks pada `FUN_80015adc`.
2. Telusuri sumber/penulis `DAT_80070d02` dan isi `DAT_80070d0a` untuk mengetahui tabel yang di-shuffle.
3. Telusuri pemanggil/efek `FUN_8001a328`, pemeriksaan `FUN_80016c68(code)`, dan semua referensi ke `DAT_80089DA9` untuk mengenali jenis kandidat.
4. Telusuri pengguna `FUN_80020bf4` serta field `param_1[0xD]` untuk menilai apakah ini runtime saja atau aturan game.
5. Petakan seed setter `0x80035DA8` dan kode/resource overlay secara terpisah; jangan menganggap tiadanya direct-JAL berarti setter tidak dipakai.

## Reproduksi signature scan

```bash
python3 tools/psx_rng_signature_scan.py /path/to/SLPS_035.53
```

Skrip memvalidasi header, SHA-256, dan urutan instruksi; tidak menjalankan executable game.
