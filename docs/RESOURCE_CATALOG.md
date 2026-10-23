# Katalog resource biner — hasil analisis statis

Tanggal pemeriksaan: 2026-10-15  
Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`  
Status: analisis statis atas salinan ROM lokal; belum diverifikasi lewat sesi debugger/emulator.

## 1. Sumber dan cakupan

ROM sumber:
- Nama: `Naruto - Shinobi no Sato no Jintori Gassen (Japan).bin`
- Ukuran: 325.989.552 byte
- CRC32: `dfe1f8b3`
- SHA-256: `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`

File yang diekstrak untuk analisis disimpan di lingkungan kerja, bukan di repo. Hash lengkap dicatat di [ROM_STRUCTURE.md](ROM_STRUCTURE.md). ROM asli tidak perlu diduplikasi di Git untuk memulihkan penelitian, selama salinan Library/lokal tersedia dan hash dicocokkan.

## 2. Bootstrap dan direktori resource DATA.BIN

### Bukti langsung

- Extent ISO `DATA.BIN`: LBN 212, ukuran 66.015.232 byte, setara 32.234 sektor data × 2.048 byte; rentang LBN `[212, 32446)`.
- Di `SLPS_035.53`, file offset `0x46098` (runtime `0x80055898`) berisi pasangan uint32 little-endian `0xD4, 0x2F44`.
- `0xD4` = LBN 212; `0x2F44` = 12.100 byte. Nilai tersebut menunjuk ke blok awal DATA.BIN yang berisi bootstrap.
- Bagian `DATA.BIN[0x00:0x44]` merupakan 0x44 byte bootstrap; `DATA.BIN[0x44:0x2F44]` merupakan tabel sebesar `0x2F00) byte.
- Tabel memiliki 1.504 entri × 8 byte. Interpretasi kuat: masing-masing entri adalah dua uint32 little-endian `(LBN, byte_length)`.
- Rutin di sekitar alamat runtime `0x800AD454) menyalin `0x2F00) byte dari `0x800AD494) ke tujuan `0x8006D830). Ini cocok dengan tabel di offset `+0x44) bootstrap.
- Kode membaca panjang dengan pembulatan ke ukuran sektor `0x800) byte sebelum membuat permintaan baca. Ini mendukung interpretasi field kedua sebagai panjang byte.

### Pemeriksaan konsistensi semua entri

- Total entri: 1.504.
- Entri aktif: 1.500.
- Entri berukuran nol: indeks 1491, 1492, 1493, 1494.
- Semua interval aktif setelah pembulatan sektor berada di dalam extent DATA.BIN dan tidak tumpang-tindih.
- Cakupan tabel: 32.227 dari 32.234 sektor; tujuh sektor yang tidak terliput terdiri atas enam sektor awal bootstrap yang dibulatkan dan satu sektor ekor file.
- Jumlah ukuran mentah semua entri aktif: 64.319.716 byte.
- Jumlah ukuran setelah pembulatan per entri ke 2.048 byte: 66.000.896 byte.

**Kesimpulan:** keyakinan tinggi bahwa bootstrap DATA.BIN membangun direktori resource berbasis LBN dan panjang byte. Itu tidak berarti semua resource merupakan overlay kode; sebagian merupakan gambar atau data lain, dan alamat muat/runtime setiap resource belum dipetakan.

## 3. Klasifikasi signature resource

Dari 1.500 entri aktif, klasifikasi signature awal adalah:

| Signature/kelas | Jumlah | Keyakinan/arti saat ini |
|---|---:|---|
| `PK02` | 921 | Container proprietary tampak berulang; format internal belum dipastikan |
| Struktur TIM valid | 246 | Struktur gambar TIM lolos validasi; 29 mode 4-bit, 217 mode 8-bit |
| `NARUTOSceneV001` | 126 | Signature scene berulang; format internal belum dikenal |
| Awalan lain `NARU` | 125 | Kemungkinan kelompok terkait, belum dibuktikan sebagai satu format |
| `PSQ0` | 6 | Format belum dikenal |
| `PSQ1` | 2 | Format belum dikenal |
| `TXT2` | 1 | Format belum dikenal |
| Belum diklasifikasikan | 73 | Perlu pemeriksaan lebih lanjut |

Validasi koreksi: pemindaian magic yang longgar menemukan 264 kandidat `10 00 00 00`, tetapi 18 gagal pemeriksaan struktur TIM dan dikecualikan dari hitungan TIM valid.

Subsignature pada 921 entri `PK02` yang terlihat saat ini:

| Versi/subsignature | Jumlah |
|---|---:|
| v3 `BIN0` | 715 |
| v2 `BIN0` | 132 |
| v2 `TPK0` | 50 |
| v4 `BIN0` | 13 |
| v1 `BIN0` | 6 |
| v3 `TPK0` | 5 |

Jangan menetapkan arti `PK02`, `BIN0`, atau `TPK0` hanya dari signature; format resmi atau layout header belum ditetapkan.

## 4. XASECT.BIN dan DATA2.BIN

- Ukuran `XASECT.BIN`: 692 byte.
- Field awal uint32 bernilai 86, diikuti 86 pasangan uint32.
- Field pertama pasangan berurutan monoton naik dari 0 hingga 79.184.
- Field kedua berada dalam rentang 224.256–6.129.664 dan selalu kelipatan 512; semua nilai berada dalam ukuran `DATA2.BIN`.
- Kode di sekitar `0x80019468`, dari jalur pemanggil sekitar `0x800191B0`, menghitung indeks `input >> 4`, mengalikan dengan 8, membaca field pertama pasangan, lalu menambahkannya ke nilai yang dikembalikan helper lain.

Bukti ini memastikan setidaknya satu konsumen memakai field pertama sebagai offset aditif yang dipilih lewat indeks. Kesamaan pola field kedua dengan offset di DATA2.BIN belum membuktikan semantik tabel XA atau struktur media tertentu. Unit dan arti kedua field masih terbuka.

## 5. SHA-256 hasil ekstraksi lokal

| File | Ukuran byte | SHA-256 |
|---|---:|---|
| `DATA.BIN` | 66.015.232 | `69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822` |
| `DATA2.BIN` | 166.428.672 | `be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9` |
| `DUMMY.BIN` | 50.667.520 | `cac5c852e95c90475a2879f51b6b949afea2df0cb540b2a2743bd791af4c47a2` |
| `SLPS_035.53` | 385.024 | `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569` |
| `SYSTEM.CNF` | 68 | `e5ffa72c5845508ae48b07140c712c9423ff6af733164b57628d1d9cece9ae71` |
| `XASECT.BIN` | 692 | `df257fbdabdb848f845466246abf4a36fdb6cf17815fc3a76ff7d7585d1953f0` |

## 6. Langkah lanjutan

1. Reverse-engineer header `PK02` dengan membandingkan sampel berbagai ukuran dan signature `BIN0`/`TPK0`; uji setiap dugaan field terhadap batas buffer sebelum memberi nama.
2. Tentukan struktur scene `NARUTOSceneV001` serta hubungan resource dengan loader dan alamat RAM.
3. Telusuri seluruh pemanggil konsumen XASECT; uji hipotesis offset dengan beberapa indeks, lalu cari pengguna field kedua.
4. Peta resource yang benar-benar dieksekusi sebagai kode dan identifikasi alamat muat, ukuran di RAM, entry point, lifecycle, dan kemungkinan relokasi.
5. Setelah peta resource lebih kuat, lanjutkan call chain transaksi Chakra/aturan gameplay.
6. Gunakan debugger PS1 untuk validasi runtime bila tersedia. Hingga itu dilakukan, semua temuan dokumen ini tetap berlabel **analisis statis**.
