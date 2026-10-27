# Langkah 4 — penelusuran statis RNG dan pemanggil langsung

Tanggal: 27 Oktober 2026  
Status: **SELESAI untuk cakupan executable utama dan helper daftar yang dapat ditelusuri statis**. Arti gameplay daftar/kandidat, seed runtime, dan kode overlay tidak dianggap selesai oleh laporan ini.

## Sumber dan reproduksi

- Executable: `SLPS_035.53`, 385.024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
- Run Ghidra + helper/cross-reference trace: [Actions #40439763833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40439763833), sukses.
- Artefak teks saja: [ghidra-slps-03553-function-index, artifact 12705072941](https://api.github.com/repos/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/artifacts/12705072941).
- Tidak ada emulator/gameplay yang dijalankan. Executable disc dan resource tidak masuk Git atau artefak; hanya hasil teks yang diarsipkan.

## Generator dan seed

Rutin di `0x80035D78` membaca state global `0x800A3118`, mengalikan dengan `0x41C64E6D`, menambahkan `0x3039` modulo (2^{32}), menyimpan state, dan mengembalikan `(state >> 16) & 0x7FFF`. Bukti instruksi langsung dan empat pemanggil langsung terdeteksi di executable utama.

Di `0x80035DA8` ada urutan instruksi yang cocok dengan setter state berbasis argumen `$a0`, tetapi Ghidra tidak menemukan referensi langsung ke alamat itu pada executable utama. Seed awal dan pemanggil tidak langsung belum diketahui; absennya referensi langsung bukan bukti bahwa setter tidak pernah digunakan melalui pointer/overlay.

## Empat pemanggil langsung

| Call site RNG | Fungsi | Kesimpulan statis yang didukung |
|---|---|---|
| `0x80015B14` | `FUN_80015adc` | Membentuk indeks dari nilai RNG dan helper pembatas, lalu memanggil helper penyisipan. Fungsi berada pada jalur pembentukan/pemilihan elemen daftar berbatas. |
| `0x80015BF0` | `FUN_80015b7c` | Melakukan pertukaran pasangan elemen byte berulang; konsisten dengan pengacakan urutan daftar. |
| `0x8001A460` | `FUN_8001a328` | Memilih secara acak satu nilai dari daftar lokal kandidat yang disaring oleh bitset. Nilai disimpan ke `DAT_80089DA9`. |
| `0x80020C24` | `FUN_80020bf4` | Menyimpan nilai RNG modulo `0x1000` ke field `param_1[0xD]`, lalu memanggil helper yang menulis `0x1000` ke field struktur dan routine tambahan. Hubungan ke mekanik gameplay belum dibuktikan. |

## Helper dan struktur daftar yang ditelusuri

- `FUN_800154d4` mengembalikan `DAT_8006D794`, dipakai sebagai batas/limit pembentukan kandidat.
- `FUN_800158d8` mengembalikan byte penghitung di `DAT_80070D02`.
- `FUN_800159bc` menyisipkan byte ke daftar mulai `DAT_80070D0A), menggeser elemen berikutnya, dan menambah penghitung. Insertion dibatasi oleh nilai `DAT_8006D794` dan ukuran maksimum `0x40`.
- `FUN_80015610` membaca data dari tabel `DAT_8005603C` dengan indeks parameter kurang dari `0x12`; ia menyalin byte sampai sentinel `0xFF` dengan batas 64 entri, menulis penghitung terkait `DAT_80070D02`/field berikutnya, lalu memanggil routine shuffle dan mereset word cursor. Format logis penuh kedua segmen daftar belum dipastikan.
- `FUN_80015768` mengambil byte awal dari `DAT_80070D0A`, memanggil helper pembaru daftar dan shuffle, lalu mengembalikan byte yang tadi dibaca.
- `FUN_800157C4` membaca elemen `DAT_80070D0A` melalui indeks cursor `DAT_80070D06`.
- `FUN_80016c68(code)` menguji bit `code` pada bitset sekitar `DAT_80070770` untuk kode kurang dari `0xA0`. `FUN_8001a328` memeriksa kode `0x7F`–`0x86` dan menambahkan kandidat `0,1,2,3,4,5,8,9,0xB` sesuai hasil test sebelum mengambil satu kandidat acak.

## Hasil dan batas interpretasi

**Keyakinan tinggi:** perilaku aritmetika LCG, empat call site langsung, insertion/shuffle daftar byte, bit-test, dan pemilihan dari daftar kandidat sebagaimana dekompilasi Ghidra.  
**Belum diketahui:** nama/arti gameplay tabel `DAT_8005603C`, kode yang disimpan pada `DAT_80089DA9`, seed runtime, pengaruh helper tambahan pada gameplay, serta pemanggil di modul/overlay lain.

Dengan demikian Langkah 4 selesai sebagai **pemetaan teknis statis atas RNG + helper daftar yang terlihat pada executable utama**. Pemetaan runtime dan semantik gameplay dilanjutkan di Langkah 5 dan 6, bukan ditebak dari label `FUN_...`.
