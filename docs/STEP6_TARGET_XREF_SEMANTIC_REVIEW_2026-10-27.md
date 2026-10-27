# Langkah 6 — tinjauan xref target, setter, dan batas semantik (27 Oktober 2026)

Status: **SEBAGIAN**. Hasil Ghidra pada base resource kandidat menunjukkan alur kode yang berguna, tetapi belum membuktikan pemetaan RAM resource saat runtime, field cost/turn, ataupun akibat gameplay final.

## Provenance

- Sumber executable dan resource berasal dari run Ghidra [#40455975408](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455975408), yang hanya mengarsipkan laporan teks.
- Review terarah artefak Ghidra dijalankan pada runner di [#40473737136](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136). Job berstatus `success`; artefak hasil [#12719587873](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/artifacts/12719587873), SHA-256 ZIP `e1ea68c92bcbf645fde3c991c8a47192b815987d8044f2d599c163c1f3ec9fb9`, 13,977 bytes. Pemeriksaan itu memakai artefak teks yang sudah ada, tidak mengunduh ulang disc dan tidak menjalankan game.
- Konteks DATA.BIN entry 1 memakai base analisis kandidat `0x800D0000`; alamat base tersebut **HIPOTESIS**, bukan mapping RAM runtime terverifikasi.

## Temuan yang dapat didukung bukti statis

1. Xref Ghidra terhadap getter target Chakra utama `0x80012A70` menemukan 8 referensi di address map kandidat entry 1. Xref terhadap setter Chakra `0x8001387C` menemukan 9 referensi dan getter Chakra pemain `0x800138EC` menemukan 16 referensi. Hitungan ini berarti referensi terdekode pada peta kandidat—bukan bukti bahwa seluruh fungsi merupakan caller cost/win-condition.
2. `0x8012A9C4` membaca koordinat/struktur UI dan memanggil getter target sebelum menggambar nilai. `0x80137AD8` juga membaca target, iterasi bit/entri, dan memanggil helper penggambaran. Kedua fungsi ini merupakan contoh konkret mengapa xref getter saja tidak boleh diklasifikasikan sebagai pemeriksaan kemenangan.
3. Kandidat `0x80112418` membandingkan hasil getter target dengan sebuah field record dan, pada cabang bersyarat, memanggil `0x80100D14(1)` dan `0x80100DCC(0xDF)`. Hasil dekompilasi dua routine transisi tersebut menunjukkan batas fungsi/register tak terselesaikan dan pola kontrol yang tidak dapat dipercaya sebagai pseudocode akhir. Hubungan dengan transisi gameplay masih **UNKNOWN**.
4. `0x800E1188` memiliki peringatan data instruksi/kontrol alur. Decompiled body menggunakan stride peserta `0x90`, membaca/menormalisasi field record, serta memanggil setter/getter Chakra. Ini cukup untuk memilih fungsi sebagai target tracing lebih lanjut, bukan untuk mengklaim ia mengurangi Chakra, memeriksa barrier, atau menentukan hasil.
5. `0x800D8918` juga memiliki peringatan kontrol alur; body menginisialisasi field participant record dari getter/getter konfigurasi. Makna seluruh field belum dibuktikan.
6. Referensi ke kandidat fungsi transition `0x800EF98C` berjumlah 10; `0x80100D14` berjumlah 74; `0x80100DCC` berjumlah 51; dan ke kandidat branch target/failure `0x8011253C` berjumlah 14 pada laporan review. Xref counts bukan call graph runtime final.

## Belum terpenuhi

- Mapping runtime untuk entry DATA.BIN/base hipotetis dan resolusi pointer antar-resource.
- Disassembly yang menyelamatkan boundary/control flow pada `0x800EF98C`, `0x80100D14`, `0x80100DCC`, serta caller yang memiliki `NONE` pada kolom containing-function.
- Bukti yang menghubungkan call chain dengan penambahan/pengurangan Chakra, barrier, cost/turn, atau hasil kemenangan yang tampak pada game.
- Verifikasi field cost-like `+0xB30`, `+0xB38`, `+0xB40`, `+0xB44` dan offsets `+0x58B`, `+0x2E9`, `+0x2E5`, `+0x5D2` dengan semantic evidence.

## Keputusan

**Langkah 6 = SEBAGIAN.** Kemajuan ini memperbaiki inventaris xref dan menghindari penafsiran berlebihan terhadap fungsi UI. Bukti yang tersedia belum memenuhi kriteria mapping RAM dan semantik gameplay runtime. Lanjutkan analisis statis/call-chain yang dapat ditutup terlebih dahulu; setiap nama mekanik tetap HIPOTESIS atau UNKNOWN sampai ada bukti yang berdiri sendiri.
