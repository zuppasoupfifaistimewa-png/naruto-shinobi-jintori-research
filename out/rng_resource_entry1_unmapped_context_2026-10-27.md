# Ghidra context scan — 36 candidate caller RNG DATA.BIN entry 1

Tanggal: 27 Oktober 2026  
Run: [#40455582988](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455582988)  
Metode: Ghidra 12.2, MIPS little-endian 32-bit, `-noanalysis`, 36 jendela instruksi lokal; tidak menjalankan emulator/gameplay. Artefak asal hanya teks, biner disc tidak menjadi artefak.

## Hasil

Dalam analisis otomatis sebelumnya, 36 dari 144 kata JAL mentah entry 1 belum didekode. Pemindaian terarah ini memaksa disassembly pada alamat-alamat tersebut dan menghasilkan:

- **36/36** instruksi terbaca sebagai `jal 0x80035d78`.
- **36/36** alur instruksi Ghidra menunjukkan target langsung `0x80035D78).
- Batas fungsi pemanggil belum dipetakan oleh metode `-noanalysis`; nama fungsi caller untuk alamat ini masih **UNKNOWN**.
- Base `0x800D0000` tetap **HIPOTESIS**, jadi pemetaan alamat ini bersyarat atas model load yang digunakan.
- Ini menutup masalah “kata mentah belum pernah didekode”, tetapi tidak membuktikan jalur runtime tiap lokasi. Ketika sebuah lokasi mengikuti lompatan tanpa syarat atau dispatch tak langsung, reachability perlu dibedakan dari keberadaan instruksi.

Dengan hasil ini, seluruh 144 lokasi entry 1 kini terdekode sebagai direct-call instruction pada peta analisis kandidat: 108 sudah ditemukan pula oleh auto-analysis biasa dan dikelompokkan pada 50 fungsi; 36 dipulihkan melalui konteks terarah tanpa boundary fungsi. Rincian 108 call site dan 50 fungsi ada di [inventaris entry 1 utama](rng_resource_entry1_ghidra_callers_2026-10-27.md).

## Daftar lengkap 36 alamat yang dipaksa decode

Semua alamat di bawah ditujukan ke `0x80035D78` dan Ghidra melaporkan `ghidra_decoded_flow_to_target=yes`. Fungsi pemanggil masing-masing belum bernama karena analisis lokal tidak melakukan whole-program auto-analysis.

| Call site hipotetis | Hasil |
|---:|---|
| 0x800E7008 | direct JAL terdekode |
| 0x800EC004 | direct JAL terdekode |
| 0x800EC0C8 | direct JAL terdekode |
| 0x800ED1E0 | direct JAL terdekode |
| 0x800FA278 | direct JAL terdekode |
| 0x80129404 | direct JAL terdekode |
| 0x80132C88 | direct JAL terdekode |
| 0x8013332C | direct JAL terdekode |
| 0x80133370 | direct JAL terdekode |
| 0x801334A4 | direct JAL terdekode |
| 0x801334E8 | direct JAL terdekode |
| 0x8013D548 | direct JAL terdekode |
| 0x8013D580 | direct JAL terdekode |
| 0x8013D5B8 | direct JAL terdekode |
| 0x8013D5DC | direct JAL terdekode |
| 0x801454EC | direct JAL terdekode |
| 0x8014A2F0 | direct JAL terdekode |
| 0x8014A570 | direct JAL terdekode |
| 0x8014DD68 | direct JAL terdekode |
| 0x8014DDC8 | direct JAL terdekode |
| 0x8014DE28 | direct JAL terdekode |
| 0x8014DE88 | direct JAL terdekode |
| 0x8014DEE8 | direct JAL terdekode |
| 0x8014DF48 | direct JAL terdekode |
| 0x8014E0D4 | direct JAL terdekode |
| 0x801558FC | direct JAL terdekode |
| 0x8015592C | direct JAL terdekode |
| 0x80155974 | direct JAL terdekode |
| 0x801559B0 | direct JAL terdekode |
| 0x801559CC | direct JAL terdekode |
| 0x801559E8 | direct JAL terdekode |
| 0x80155A04 | direct JAL terdekode |
| 0x80155AB4 | direct JAL terdekode |
| 0x80156478 | direct JAL terdekode |
| 0x8015657C | direct JAL terdekode |
| 0x801565B8 | direct JAL terdekode |

## Bukti alur kontrol lokal tambahan

Dari instruksi yang didekode di jendela-jendela lokal, dua kandidat memiliki sumber branch masuk eksplisit:

- `0x800EC0C8` adalah target `bne s3,v0,0x800EC0C8` pada `0x800EC1DC`.
- `0x8015657C` adalah target `bne v1,v0,0x8015657C` pada `0x8015656C`.

Tidak muncul referensi masuk lain dalam instruksi yang terdekode di jendela lokal. Ini **bukan** hasil xref menyeluruh untuk seluruh resource, jadi tidak boleh dianggap bukti bahwa alamat lain tidak terjangkau. Beberapa kandidat tampak berada di rangkaian blok switch/dispatch (misalnya sesudah `jr v0`); target tidak langsung mungkin menjelaskan mengapa auto-analysis awal melewatkannya.

## Makna untuk Langkah 4

**Pasti secara statis, bersyarat pada base hipotetis:** 36 lokasi ini berisi instruksi JAL yang terdekode dan menunjuk langsung ke RNG.  
**Belum diketahui:** boundary fungsi caller, apakah setiap blok dipakai pada runtime, dan semantik gameplay-nya. Jangan menamai lokasi sebagai roulette/battle/turn tanpa call chain/tabel yang menguatkan.
