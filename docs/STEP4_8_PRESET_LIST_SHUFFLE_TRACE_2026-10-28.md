# Step 4 / Step 8 — trace daftar berindeks 18 preset dan helper pengacak

Tanggal: 28 Oktober 2026 (WIB)  
Fokus: menurunkan operasi yang benar-benar terlihat di main executable, tanpa menebak nama fitur dari angka mentah.

## Bukti sumber

- Workflow/artefak: [run #40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524), [artefak teks #12739676233](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524/artifacts/12739676233).
- SHA-256 ZIP artefak: `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d`.
- Main EXE (private runner input; tidak disimpan dalam repo/artefak): 385,024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
- Bukti kerja: raw MIPS dalam output `spimdisasm`, jendela fungsi Ghidra, referensi alamat, dan perbandingan Ghidra/m2c. Output teks di artefak cukup untuk audit ulang; berkas game mentah tidak diperlukan di laporan.

## Hasil statis

### 1. Pemilih baris dan dua buffer

Fungsi `0x80015610` (body `[0x80015610, 0x80015748)`) memeriksa argumen `param` terhadap `0x12`: nilai 0–17 diterima; nilai >=18 mengembalikan 0.

Untuk masing-masing kelompok `g=0,1`, instruksi menghitung sumber:

`0x8005603C + param * 0x40 + g * 0x480`

Isi disalin byte-per-byte ke buffer aktif:

`0x80070D0A + g * 0x40`

Penyalinan berhenti ketika menemukan byte sentinel `0xFF` atau mencapai 64 byte. Panjang tersimpan sebagai halfword di `0x80070D02 + g*2`; indeks/cursor terkait di-reset ke nol pada `0x80070D06 + g*2`.

Pemanggil langsung yang teridentifikasi:
- `0x80012820`, dari badan fungsi `0x80012780`: argumen berasal dari byte offset `+2` pada record ber-stride `0x30` dalam tabel sekitar `0x80064918`.
- `0x80012F90`, dari badan `0x80012EAC`: argumen berasal dari byte offset `+2` pada descriptor yang dipilih lewat kalkulasi terkait `0x80057798`.

Ini membuktikan jalur pemuatan dua daftar berindeks dari tabel statis. **Belum membuktikan nama fitur daftar, apakah byte berarti kartu, tile, aksi, urutan giliran, atau resource lain.**

### 2. Isi data yang tertanam

Pembacaan tabel dari data EXE menunjukkan dua blok kelompok untuk setiap indeks 0–17 identik byte-per-byte dalam keadaan statis.

| Indeks | Panjang hingga `0xFF` pada masing-masing blok | Catatan |
|---:|---:|---|
| 0 | 51 | Ada sentinel |
| 1 | 55 | Ada sentinel |
| 2 | 59 | Ada sentinel |
| 3 | 57 | Ada sentinel |
| 4 | 61 | Ada sentinel |
| 5 | 62 | Ada sentinel |
| 6 | 62 | Ada sentinel |
| 7 | 62 | Ada sentinel |
| 8 | 11 | Ada sentinel |
| 9–17 | 64 byte | 64 byte sumber seluruhnya `0x00`; tidak ada sentinel dalam blok 64 byte |

Panjang dihitung dari offset awal hingga byte pertama `0xFF`, atau 64 bila tidak ada sentinel. Untuk indeks 9–17, kode loader tidak menafsirkan blok nol itu sebagai daftar kosong: karena tidak menemukan `0xFF`, jalur statis akan menyalin 64 byte nol dan menyimpan panjang 64. Ini adalah fakta implementasi; apakah indeks tersebut tak terpakai, data cadangan, atau konfigurasi khusus **belum diketahui**. Jangan menyimpulkan bahwa ID 0 valid atau invalid secara semantik hanya dari bentuk tabel ini.

### 3. Perilaku helper `0x80015B7C`: kedua pemanggilan memilih daftar pertama

Badan executable yang kembali ke pemanggil pada `0x80015C64` dan memulihkan stack pada delay slot `0x80015C68`, sesuai batas Ghidra `0x80015C6C`. Label spimdisasm `nonmatching func_80015B7C, 0x580` terlalu lebar dan melampaui return sebenarnya; gunakan instruksi return mentah dan batas fungsi Ghidra untuk soal boundary ini.

Pada alamat `0x80015B9C`, fungsi menimpa argumen masuk dengan `addu a0,zero,zero`. Sesudah itu:
- mengambil count dari `0x80070D02` (daftar pertama), bukan `0x80070D04`;
- menggunakan offset buffer `0 << 6 = 0`, sehingga basisnya `0x80070D0A`;
- jika count `n` bukan nol, mengulang `4*n` kali;
- pada iterasi `i`, menukar byte pada indeks `i mod n` dengan indeks `RNG mod n`, menggunakan fungsi RNG `0x80035D78`.

Ini bukan pengacakan Fisher–Yates standar: loop menjalankan empat putaran posisi kiri secara siklik dengan posisi kanan pseudo-acak. Yang lebih penting, argumen kelompok yang dikirim pemanggil diabaikan pada awal helper. Karena `0x80015610` memanggil `0x80015B7C(g)` dua kali untuk `g=0,1`, kedua pemanggilan secara statis mengacak buffer pertama dan menggunakan count pertama; helper ini tidak mengacak buffer kedua.

Helper `0x800158D8` juga secara literal membaca byte dari `0x80070D02` tanpa membaca argumen masuk. Fungsi lain di sekitar `0x800158E8` dan `0x800159BC` menargetkan offset/basis kelompok nol pada jalur yang terlihat dalam jendela instruksi yang diaudit. Ini memperkuat prioritas untuk mengaudit konsumen buffer kedua, tetapi tidak cukup untuk menyebutnya sebagai bug atau mengasumsikan maksud programmer.

### 4. Apa artinya bagi riset logika game

Yang sekarang diketahui secara statis:
1. Ada tabel dengan 18 indeks yang lolos guard fungsi pemuat.
2. Setiap indeks mengarahkan pemuatan dua blok byte 64-entry dari sumber berjarak `0x480`.
3. Untuk indeks 0–8, kedua blok sumber identik dan berakhir dengan sentinel dengan panjang berbeda; indeks 9–17 berisi 64 byte nol tanpa sentinel.
4. Fungsi yang dinamai `0x80015B7C` di laporan lama tidak memakai parameter kelompoknya: operasi swap yang tampak hanya menyasar daftar pertama.

Yang belum diketahui:
- nama/makna record dan tiap byte ID;
- apakah semua 18 indeks benar-benar dipakai oleh gameplay;
- siapa yang mengonsumsi daftar kedua dan apakah ada kode lain yang mengubah/mengacaknya;
- apakah pengacakan ini berhubungan dengan kartu, giliran, roulette, papan, atau pertarungan;
- kaitan runtime antara fungsi, kondisi permainan, dan efek visual/hasilnya.

## Eksperimen savestate terisolasi — hasil dan batas

Sumber checkpoint privat berasal dari run #39262213468. Raw state berukuran 21,163,286 byte dengan SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`; state sanitasi berukuran 20,638,994 byte dengan SHA-256 `b94e61502b63a81107f48153932ccbef21bede8c7f53d4b01e6e013ecb8979eb`.

- [Percobaan restore mentah #40613996374](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40613996374): BIOS/game/state/card terverifikasi; PCSX-Redux crash `SIGSEGV`/exit 139 sesudah `RESTORE_LOAD_BEGIN`. Tidak ada bukti bahwa `loadSaveState` kembali atau event `SaveStateLoaded` berjalan.
- [Percobaan rekonstruksi #40614208610](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40614208610): BIOS dimasukkan kembali ke state sanitasi; hasil SHA-256 identik dengan raw source (`00fab826…f6c3d`), kemudian terjadi `SIGSEGV` pada titik yang sama. Ini mengonfirmasi rekonstruksi byte, **bukan** percobaan dengan representasi state yang berbeda.

Tak ada tombol gameplay dikirim pada kedua percobaan. Karena loader crash dua kali dengan byte state yang sama, pengujian restore dihentikan; pengulangan identik tidak diharapkan memberi bukti baru. Screenshot asal checkpoint tetap hanya jangkar visual, bukan bukti aturan internal. Tidak ada state mentah, ROM/BIN/CUE/EXE, BIOS, Memory Card, atau RAM dump dimasukkan ke Git maupun artefak hasil baru.

## Status dan langkah lanjut

- Step 4: **SEBAGIAN** — hubungan RNG/pengacak dengan pemilihan/hasil gameplay belum terikat.
- Step 5: **SEBAGIAN** — caller terpilih dan struktur lokal ditelusuri, bukan keseluruhan EXE.
- Step 8: **SEBAGIAN**, subkriteria aturan gameplay utama tetap **UNKNOWN**.
- Restore savestate: **FAIL pada dua pemanggilan loader; jangan ulangi tanpa perubahan hipotesis atau emulator/state-format bukti baru**.
- Story Mode: **TIDAK TERBUKTI TAMAT**.
- Adaptive player: tidak dijalankan atau diubah.

Prioritas berikutnya: audit secara statis semua referensi ke count/buffer kedua dan fungsi yang memanggil `0x800158E8`/`0x800159BC`, lalu cocokkan daftar byte dengan tabel descriptor sebelum memilih eksperimen gameplay baru. Sampai ada checkpoint yang terbukti bisa dipulihkan, jangan mengklaim eksperimen A/B dari checkpoint ini dapat direproduksi.


<!-- descriptor-selector-crosscheck-2026-10-28 -->
## Cross-check: selector yang benar-benar muncul pada descriptor

Ada dua pemanggil langsung `jal 0x80015610` di main EXE (`0x80012820` dan `0x80012F90`), dan kedua argumen berasal dari byte `+2` pada tabel descriptor. Pembacaan data mentah memberi hasil berikut:

- Descriptor `0x80064918`, stride `0x30`, 18 record: byte `+2` adalah `[0,1,2,3,4,5,6,7,4,4,4,4,4,4,4,5,8,8]`.
- Descriptor `0x80057798`, stride `0x54`, 18 record: byte `+2` adalah `[0,1,2,8,3,4,8,5,6,6,0,0,0,0,0,0,3,5]`.

Dua tabel descriptor yang ditelusuri hanya memberikan selector 0–8 ke pemanggil langsung tersebut. Jadi blok sumber selector 9–17 yang tersusun sebagai 64 byte nol **tidak dipilih oleh dua descriptor ini**. Fungsi loader sendiri menerima selector hingga 17, tetapi jangan menyebut selector 9–17 reachable dari alur ini tanpa bukti pemanggil lain atau jalur tak langsung. Sebaliknya, ini juga belum membuktikan bahwa selector 9–17 tak pernah dipakai di seluruh game; batas kesimpulan hanya dua callsite dan dua tabel yang diaudit.
