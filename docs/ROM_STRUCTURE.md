# Struktur ROM dan identitas disc

## Identitas file sumber

Nama file yang diteliti: Naruto - Shinobi no Sato no Jintori Gassen (Japan).bin

| Properti | Nilai |
|---|---|
| Ukuran | 325.989.552 byte |
| Format | Dump disc PS1 raw sector, 2352 byte/sector |
| Jumlah sektor hasil pembagian ukuran/2352 | 138.601 |
| Serial disc | SLPS-03553 |
| CRC32 | dfe1f8b3 |
| SHA-256 | 58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88 |

CRC32 cocok dengan catatan dump BIN di [GameGear Archive](https://gamegear.net/archive/games/psx/naruto-shinobi-no-sato-no-jintori-gassen-japan). Nilai SHA-256 di atas adalah hasil hashing atas file yang diteliti dalam sesi ini; sumber eksternal yang dikutip di sini tidak dipakai untuk mengklaim kecocokan SHA-256.

## Boot configuration

Isi SYSTEM.CNF yang terbaca:

- BOOT = cdrom:\SLPS_035.53;1
- TCB = 4
- EVENT = 16
- STACK = 801fff00

Serial dalam nama executable cocok dengan serial disc SLPS-03553.

## Daftar file pada filesystem ISO yang diekstrak

| Nama | Ukuran byte | Catatan |
|---|---:|---|
| DATA.BIN | 66.015.232 | Berisi bootstrap kode, direktori resource 1.504 entri, lalu resource berbasis LBN; format sebagian besar resource belum teridentifikasi |
| DATA2.BIN | 166.428.672 | Konten besar; fungsi/format internal belum dipetakan penuh |
| DUMMY.BIN | 50.667.520 | Konten belum dipetakan penuh |
| SLPS_035.53 | 385.024 | Executable PS-X EXE |
| SYSTEM.CNF | 68 | Konfigurasi boot |
| XASECT.BIN | 692 | Tujuan/format belum dipastikan |

Angka ukuran di tabel mengacu pada listing filesystem ISO yang dibuat dari dump. ISO hasil ekstraksi tidak disimpan di repo ini.

## Executable utama

| Field | Nilai |
|---|---|
| File | SLPS_035.53 |
| Ukuran file | 385.024 byte |
| Alamat muat | 0x80010000 |
| Program counter | 0x80011448 |
| Text size | 0x5D800 |

Nilai di atas dibaca dari header PS-X EXE. PC menunjukkan alamat entry point yang tersimpan pada header; ini tidak berarti seluruh gameplay berlangsung di executable utama.

## Struktur sektor

Dump sumber menggunakan sektor raw berukuran 2352 byte. Pada pemeriksaan sebelumnya, payload data diekstrak menjadi filesystem ISO terpisah untuk memeriksa nama file dan header. File sumber aslinya tidak diubah.

## Batas interpretasi

- DATA.BIN memuat blok yang tampak sebagai instruksi MIPS R3000A, sehingga tidak tepat menganggapnya hanya sebagai arsip aset.
- Keberadaan instruksi MIPS dalam file besar tidak cukup untuk menentukan alamat runtime-nya tanpa mengetahui format container, entry point, relokasi, serta loader.
- Belum ditemukan semua aturan sebagai teks Shift-JIS biasa; teks mungkin disimpan dalam format lain, tabel glyph/resource, atau data terkompresi/terenkode.
- Jangan melakukan perubahan atau menyimpan ulang file BIN/ISO selama proses analisis.

## Direktori resource dan hash hasil ekstraksi lokal

Pemeriksaan lanjutan menemukan direktori resource di awal `DATA.BIN`: bootstrap `0x44) byte dan tabel `0x2F00) byte berisi 1.504 entri berukuran 8 byte. Setiap entri aktif paling kuat diinterpretasikan sebagai LBN sektor CD dan panjang byte. Detail analisis serta signature ada di [docs/RESOURCE_CATALOG.md](RESOURCE_CATALOG.md).

Hash SHA-256 berikut dihitung pada salinan file yang diekstrak secara lokal. File-file ini **tidak diunggah ke repo**:

| File | Ukuran byte | SHA-256 |
|---|---:|---|
| DATA.BIN | 66.015.232 | `69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822` |
| DATA2.BIN | 166.428.672 | `be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9` |
| DUMMY.BIN | 50.667.520 | `cac5c852e95c90475a2879f51b6b949afea2df0cb540b2a2743bd791af4c47a2` |
| SLPS_035.53 | 385.024 | `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569` |
| SYSTEM.CNF | 68 | `e5ffa72c5845508ae48b07140c712c9423ff6af733164b57628d1d9cece9ae71` |
| XASECT.BIN | 692 | `df257fbdabdb848f845466246abf4a36fdb6cf17815fc3a76ff7d7585d1953f0` |


## Penyimpanan file hasil ekstraksi untuk chat berikutnya

File hasil ekstraksi telah diarsipkan di Library ChatGPT, folder `Naruto Research Files`. Lima file tersedia dalam bentuk aslinya; `DATA2.BIN` disimpan sebagai `DATA2.BIN.zip` karena batas kapasitas Library. Lihat [HANDOFF_LANJUT.md](../HANDOFF_LANJUT.md) untuk lokasi persis dan prosedur pemulihan. Semua file game tetap di luar repo.
