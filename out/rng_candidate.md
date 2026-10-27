# Kandidat RNG — analisis statis executable utama

Tanggal pemeriksaan: 27 Oktober 2026. Biner tidak dimasukkan ke Git.

- File: `SLPS_035.53`, 385.024 byte.
- SHA-256 terverifikasi: `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
- Header: PC `0x80011448`, base `0x80010000`, text `0x5D800`.
- **Validasi Ghidra selesai:** Actions run [#40438574949](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40438574949) sukses menggunakan Ghidra 12.2 dan bahasa `MIPS:LE:32:default`. Indeks `functions.tsv` berisi 1.206 fungsi; artefak teks tidak berisi executable. [Artefak output](https://api.github.com/repos/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/artifacts/12704922603).

## Temuan RNG

**Keyakinan tinggi:** alamat `0x80035D78` berisi rutin LCG yang menggunakan state global `0x800A3118`. Urutan instruksi cocok dengan scan signature eksak dan Ghidra mengenali fungsi `FUN_80035d78` sepanjang 48 byte hingga alamat `0x80035DA8`.

Pseudocode yang cocok dengan instruksi:

```c
uint32_t state = *(volatile uint32_t *)0x800A3118;
state = state * 0x41C64E6D + 0x3039;  // modulo 2^32
*(volatile uint32_t *)0x800A3118 = state;
return (state >> 16) & 0x7FFF;
```

Pengali `0x41C64E6D` = 1.103.515.245; penambah `0x3039` = 12.345; hasilnya 15 bit. Instruksi kunci: `mult` di `0x80035D88`, `mflo` di `0x80035D8C`, update global di `0x80035D98`, shift di `0x80035D9C`, lalu mask `0x7FFF` pada delay slot `jr $ra` di `0x80035DA4`. **Keyakinan tinggi:** ini generator pseudo-acak yang berperilaku seperti `rand()`; tidak ada simbol debug yang mengonfirmasi nama sumber.

Di `0x80035DA8` ada setter yang menulis argumen pertama `$a0` ke global yang sama: `lui $at,0x800A`, `jr $ra`, lalu `sw $a0,0x3118($at)` pada delay slot. Perilakunya cocok dengan `srand(seed)`-like. **Catatan Ghidra:** indeks otomatis tidak membuat entry fungsi terpisah pada `0x80035DA8` (entry fungsi yang diekspor di alamat itu tidak ada); fungsi setter masih perlu dibuat/diperiksa sebagai kandidat entrypoint. Tidak ditemukan direct-JAL caller untuk setter di text utama. Seed awal dan jalur panggilan tak langsung/overlay belum diketahui.

## Direct-JAL callers ke RNG

Call-site langsung hasil scan signature berikut semuanya berada di fungsi yang ditemukan Ghidra. Nama `FUN_...` adalah label otomatis, bukan nama semantik.

| Call site RNG | Fungsi Ghidra yang memuat call site | Bukti konteks dan interpretasi awal |
|---|---|---|
| `0x80015B14` | `FUN_80015adc`, entry `0x80015ADC`, 160 byte | Hasil RNG digabung dengan hasil helper `0x800158D8`, di-shift/mask, lalu dipakai menghitung remainder sebelum call `0x800159BC`. Konsisten dengan offset/posisi acak berbatas; domain belum dikenal. |
| `0x80015BF0` | `FUN_80015b7c`, entry `0x80015B7C`, 240 byte | Di loop membaca tabel dengan `lhu`, menghitung `rand % bound`, lalu menukar dua byte memakai `lbu`/`sb`. **Keyakinan menengah:** shuffle/permutasi byte berbasis RNG; tujuan tabel belum diketahui. |
| `0x8001A460` | `FUN_8001a328`, entry `0x8001A328`, 376 byte | Setelah helper `0x80016C68` dengan argumen `0x82`–`0x86`, hasil dipakai sebagai indeks modulo jumlah pilihan lokal dan byte pilihan disimpan ke global `0x80097DA9`. Fitur belum dipastikan. |
| `0x80020C24` | `FUN_80020bf4`, entry `0x80020BF4`, 156 byte | Hasil RNG disimpan ke field struktur; kode selanjutnya memakai batas `0x1000` dan helper `0x80020D48`, `0x80018300`, `0x80018468`. Bisa berupa runtime/allocation helper, belum terbukti sebagai mekanik gameplay. |

Call-site tersebut adalah direct-JAL yang ditemukan pada text utama, bukan seluruh pemakaian RNG. Panggilan via pointer, kode/overlay lain, dan seed initialization belum dihitung.

## Keyakinan dan batas

- **Pasti:** ukuran/hash executable terverifikasi oleh workflow; pola LCG eksak ditemukan di `0x80035D78); 1.206 fungsi diekspor Ghidra; empat direct-JAL call sites dan fungsi Ghidra yang memuat tiap call site tercatat dalam output.
- **Keyakinan tinggi:** `0x80035D78` adalah generator LCG; `0x80035DA8` berperilaku seperti setter seed.
- **Belum diketahui:** seed awal, caller via pointer/overlay, dan domain gameplay (roulette, turn, battle, AI, hadiah).
- Tidak ada emulator atau gameplay input yang dijalankan. Keberhasilan langkah 3 bukan bukti aturan gameplay tertentu.

## Langkah 4 — pekerjaan berikutnya

1. Buka fungsi pemanggil di indeks Ghidra dan periksa dekompilasi terbatas pada `FUN_80015adc`, `FUN_80015b7c`, `FUN_8001a328`, `FUN_80020bf4`.
2. Cari seluruh referensi baca/tulis ke global `0x800A3118` serta caller tidak langsung dan resource/overlay. Scan direct-JAL hanya mencakup text executable utama.
3. Tentukan siapa yang memanggil setter `0x80035DA8` sebelum menyimpulkan seed awal.
4. Kaitkan caller dengan perilaku gameplay hanya setelah argumen, tabel, dan efek samping mendukungnya; nama otomatis bukan bukti fitur.

## Reproduksi scan signature

```bash
python3 tools/psx_rng_signature_scan.py /path/to/SLPS_035.53
```

Skrip memvalidasi header, SHA-256, dan urutan instruksi; tidak menjalankan executable game.
