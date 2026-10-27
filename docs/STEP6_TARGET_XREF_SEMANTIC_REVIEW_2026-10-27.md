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

## Addendum — penelusuran dataflow statis atas output runner yang sudah ada (27 Oktober 2026)

Review tambahan ini memakai raw job log dari runner-only review [#40473737136](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136), job `122086773431`, yang menampilkan potongan dekompilasi dan xref dari artefak teks yang sudah ada. Ini bukan run game dan bukan bukti runtime. Base DATA.BIN entry 1 `0x800D0000` tetap HIPOTESIS.

1. **Dataflow yang dapat ditulis tanpa menamai mekanik:** pseudocode `0x8011C0D0` membandingkan argumen dengan sebuah global lalu berhenti bila sama. Pada cabang argumen nonzero, ia mengubah field global dan field byte pada record peserta ber-stride `0x90`; loop membaca word pada offset record `+0x04`, menghitung negasinya, menjepit nilai di bawah `-9999` ke `-9999`, menyimpannya kembali, kemudian memanggil setter main EXE `0x8001387C(index, nilai)`. Itu mendukung operasi negasi/clamp dan aliran ke setter, bukan arti “biaya”, “pengembalian”, “barrier”, atau “level-up”.
2. Cabang nilai nol/nonzero di routine yang sama juga menguji jumlah dua field pendek pada struktur lain terhadap `0x101` dan memanggil helper berbeda. Identitas struktur, makna parameter, serta alasan threshold `0x101` belum diketahui. Jangan menyamakan threshold ini dengan nilai Chakra.
3. Dalam pseudocode di sekitar kandidat `0x80111228`, `0x801112CC`, `0x801113B4`, `0x801114F0`, dan `0x80111588`, jalur bersyarat membandingkan getter target `0x80012A70` dengan field record yang dihitung menggunakan stride `0x90`; setelah pemeriksaan flag/helper yang berbeda, jalur tersebut menulis byte global-relative `+0x58B` dan nilai 16-bit di `+0x5D2` (nilai yang terlihat mencakup `0`, `4`, `8`, `0x20`, `0x200`, dan `0x1000`) sebelum memanggil `0x800EF98C`. Ini bukti urutan statis bersyarat pada peta kandidat; arti selector, kode, dan routine transisi masih UNKNOWN.
4. Hasil dekompilasi untuk `0x800E1188` secara eksplisit memperingatkan adanya data instruksi/kontrol alur buruk. Ia tidak boleh dipakai untuk menafsirkan semua branch, delay slot, atau efek akhir tanpa disassembly instruksi mentah yang tervalidasi dan batas fungsi yang diperbaiki. `0x80100D14` dan `0x80100DCC` juga belum layak diperlakukan sebagai pseudocode transisi final.
5. Koreksi inventaris setelah membuka seluruh runner-review artifact #12719587873 (teks `step6-audit-artifact.txt`, SHA-256 `1db6a88093c67b84c17cdc36c464d21d7931a79cd9c6b373a110ec75c5b31e1d` — verifikasi checksum lokal/metadata sebelum mengandalkan hash tersebut). Instruksi di entry-1 base hipotetis `0x800D0000` secara eksplisit menulis `+0x2E9 = 0x3F` dan `+0x2E5 = 0` pada fungsi kandidat `0x80111228`, `0x801112CC`, `0x801113B4`, `0x801114F0`, dan `0x80111588`; `+0x58B` mendapat byte selektor/indeks dari beberapa sumber, global byte `0x80139F3B` diset `0`, lalu beberapa jalur menulis kode 16-bit ke `+0x5D2` (`0x200`, `8`, `4`, `0x20`, atau melalui cabang `0`/`0x1000`). Ini fakta static-store, bukan makna gameplay. `+0xB30`, `+0xB38`, `+0xB40`, `+0xB44` tetap belum terpetakan oleh sumber yang ditinjau; tidak ditemukannya pada artefak ini bukan bukti tiadanya penggunaan di seluruh program.

### Keputusan setelah tracing tambahan

Temuan #1–#3 memperbaiki aliran data yang telah diketahui namun **tidak menutup** kriteria Langkah 6. Tetap **SEBAGIAN**: base RAM resource, sumber/pemakai seluruh field/delta, boundary MIPS yang rusak, dan kaitan dengan efek permainan masih belum tersedia. Langkah berikutnya yang benar-benar membedakan hipotesis adalah menelusuri instruksi MIPS mentah dan semua operand/store untuk field yang belum terpetakan; jangan menurunkan makna gameplay dari nilai konstanta atau nama default Ghidra.

## Addendum — raw MIPS verification of target-gated stores (27 Oktober 2026)

**Bukti primer:** artifact teks #12719587873 dari review runner-only [Actions #40473737136](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136), ZIP SHA-256 e1ea68c92bcbf645fde3c991c8a47192b815987d8044f2d599c163c1f3ec9fb9, ukuran 13.977 byte. Analisis ini membaca teks/disassembly yang telah ada; tidak menjalankan game. DATA.BIN entry 1: offset file 0x10BB000, ukuran 596.412 byte, SHA-256 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a. Seluruh interpretasi alamat entry 1 tetap bersyarat pada base hipotetis 0x800D0000, bukan mapping RAM runtime.

### Instruksi, operand, branch, dan delay slot

Pola sll v0,v1,3; addu v0,v0,v1; sll v0,v0,4 menghitung indeks × 0x90. Instruksi addiu s0,s0,4 dan delay slot addu s0,s0,v0 membentuk alamat word record +0x04. Setelah jal 0x80012A70 (getter target Chakra), instruksi lw v1,0(s0); slt v1,v1,v0; bne v1,zero,0x8011253C; nop mengarahkan nilai record yang lebih kecil dari target ke cabang failure. Ini fakta statis tentang operand dan alur kontrol; bukan bukti bahwa target merupakan kondisi menang universal.

| Site | Instruksi/cabang yang diamati | Store atau kelanjutan pada jalur diterima | Batas bukti |
|---|---|---|---|
| 0x80111228 | Hitung record stride 0x90 dan cabang record_word < target ke 0x8011253C. | Raw window mencakup byte store +0x58B, +0x2E9=0x3F, +0x2E5=0 dan clear global byte efektif 0x80139F3B. Dekompilasi melaporkan +0x5D2=0x200 lalu 0x800EF98C; raw window berhenti sebelum store +0x5D2. | Nilai 0x200 didukung dekompilasi terpilih, bukan raw window tersebut; arti transisi tidak diketahui. |
| 0x801112CC | Sebelum getter: lhu record+0x0A; andi 0x200; beq zero ke 0x8011253C. Delay slot beq adalah addiu s0,s0,4 dan tetap dieksekusi. Lalu ada tes record_word < target. | Store byte +0x58B, +0x2E9=0x3F, +0x2E5=0; dekompilasi menyebut +0x5D2=8 sebelum 0x800EF98C. | Arti flag 0x200 dan kode 8 UNKNOWN. |
| 0x801113B4 | Hitung indeks × 0x90, panggil getter dengan alamat field tersusun pada delay slot, lalu branch jika record_word < target. | Store +0x58B, +0x2E9=0x3F, +0x2E5=0, clear global 0x80139F3B; dekompilasi menyebut +0x5D2=4 dan call 0x800EF98C. | Makna byte dan kode 4 UNKNOWN. |
| 0x801114F0 | Setelah tes target, jal 0x800BDBFC dengan delay slot li a0,0x20; hasil v0 dibandingkan dengan global efektif 0x8013EBB0; mismatch menuju 0x8011253C. | Setelah kedua tes lolos, store +0x58B, +0x2E9=0x3F, +0x2E5=0; dekompilasi menyebut +0x5D2=0x20 lalu 0x800EF98C. | Arti hasil helper/gate UNKNOWN. |
| 0x80111588 | Cabang record_word < target memiliki delay slot lui v0,0x8014. Byte untuk +0x58B dibaca dari alamat efektif 0x8013EA8A. Call 0x80012AD0 diikuti delay slot yang membersihkan byte global 0x80139F3B. | Store +0x2E9=0x3F, +0x2E5=0; dekompilasi melaporkan +0x5D2=0 atau 0x1000 berdasarkan bit 0x1000 dari hasil helper. | Tidak menetapkan arti state atau aksi. |
| 0x80112418 | Pada jalur accepted, jal 0x80100D14 memiliki delay slot li a0,1; jal berikutnya 0x80100DCC memiliki delay slot li a0,0xDF. | Jendela menunjukkan store +0x2E5=0 dan +0x2E9=0x18 pada jalur lanjutan tertentu. | Batas fungsi/control-flow transisi bermasalah; outcome gameplay UNKNOWN. |

Field +0x2E9 dan +0x2E5 terbukti ditulis pada jalur-jalur terpilih, tetapi semua pembaca, inisialisasi lintas jalur, dan makna field belum dipetakan tuntas. Field +0xB30, +0xB38, +0xB40, +0xB44 tidak muncul dalam artifact terarah ini; itu BELUM TERUJI pada cakupan artifact, bukan bukti tidak ada pemakaian di seluruh resource. Kandidat transisi 0x800EF98C, 0x80100D14, 0x80100DCC masih memiliki masalah batas fungsi/control-flow.

**Keputusan Step 6 tetap SEBAGIAN.** Bukti baru memperjelas operand, kondisi, cabang dan delay slot; base runtime, dataflow pending lengkap, serta efek gameplay tetap belum dibuktikan.

## Addendum — jalur perubahan record/Chakra pada 0x8011C0D0 (27 Oktober 2026)

Sumber tetap artifact runner-only #12719587873 dari [Actions #40473737136](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136), SHA-256 ZIP e1ea68c92bcbf645fde3c991c8a47192b815987d8044f2d599c163c1f3ec9fb9. Body Ghidra yang tersedia untuk kandidat 0x8011C0D0 berukuran 408 byte; raw instruction window yang diarsipkan hanya mencakup prolog sampai sekitar 0x8011C118, sehingga rincian loop berikut didukung dekompilasi terarah, bukan seluruh urutan instruksi mentah.

### Dataflow yang didukung dekompilasi terarah

1. Argumen masuk dinormalisasi ke byte (andi a0,a0,0xFF). Nilai dibandingkan dengan byte global efektif 0x80139F70; jika sama, fungsi kembali tanpa perubahan.
2. Jika nilainya berbeda, fungsi memperbarui global 0x80139F70 dan menulis byte argumen ke pointer_global_0x8013EA74 + 0x618. Pemanggil yang memasok argumen dan arti field +0x618 belum diidentifikasi.
3. Jika argumen nol, fungsi tidak menjalankan loop negasi Chakra; ia menguji (signed short)[base+0x10] + (unsigned short)[base+0x14] < 0x101. Pada jalur yang lolos, ia memanggil 0x8003F5D0(base+0x10, word[base+0x18]); jika tidak, ia menulis byte 1 ke base+0x94A lalu memanggil 0x800F96A4.
4. Jika argumen nonzero, fungsi memilih record dengan indeks global efektif 0x8013EA88, menghitung record stride 0x90, lalu menulis byte 8 di record+0x22. Ia kemudian mengiterasi jumlah peserta dari byte global efektif 0x8013EA71. Untuk setiap indeks i, word pada table + i*0x90 + 0x04 dibaca, dinegasikan, dijepit agar tidak kurang dari -9999, disimpan ke field yang sama, lalu nilai baru dan indeks diteruskan ke setter main EXE 0x8001387C.
5. Sesudah loop, pemeriksaan sum yang sama terhadap 0x101 memilih call 0x8003F5D0 dan 0x800F96A4, atau jalur yang menulis byte 1 ke base+0x94A dan memanggil 0x800F96A4. Parameter kedua 0x8003F5D0 pada cabang nonzero berasal dari word base+0x61C, berbeda dari cabang zero yang membaca base+0x18.

### Batas interpretasi

TERVERIFIKASI-STATIS (pada model base hipotetis): mask argumen byte, compare/update ke global 0x80139F70, write +0x618, pemilihan record stride 0x90, operasi negasi/clamp/store pada word +0x04, pemanggilan setter per peserta, syarat sum <0x101, dan store alternatif +0x94A=1 sebagaimana didekompilasi.

UNKNOWN: siapa yang memanggil fungsi dengan nilai 0/nonzero; arti state byte global; apakah negasi/clamp mewakili biaya, refund, normalisasi atau pembaruan transaksi sementara; makna +0x22, +0x618, +0x61C, +0x94A, +0x10, +0x14, +0x18; efek 0x8003F5D0 dan 0x800F96A4. Tidak tersedia nilai sebelum/sesudah runtime yang dapat dipakai untuk memberi label gameplay.

Kriteria pending +0xB30/+0xB38/+0xB40/+0xB44 tetap BELUM TERUJI pada cakupan artifact. Site 0x8011C0D0 tidak mengakses offset tersebut dalam dekompilasi yang tersedia; ini tidak membuktikan bahwa offset tersebut tidak digunakan oleh fungsi lain. Status Step 6 tetap SEBAGIAN.

## Addendum — penelusuran penuh artifact store fields

Artifact runner-only [#40473737136](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136), outer artifact #12719587873 (13,977 bytes, ZIP SHA-256 `e1ea68c92bcbf645fde3c991c8a47192b815987d8044f2d599c163c1f3ec9fb9`), berisi hasil teks yang mengambil sumber dari Ghidra run #40455975408; fungsi dan instruction window yang relevan ada pada `step6-audit-artifact.txt`. `+0x2E9` dan `+0x2E5` sekarang bukan UNKNOWN untuk eksistensi store: nilainya tercatat pada lima kandidat di atas. Namun operand object-base di pseudocode memakai register yang tidak selalu terbukti/bernama dan entry-1 base runtime belum tervalidasi, jadi field semantics di game tetap UNKNOWN. Offset `+0xB30/+0xB38/+0xB40/+0xB44` memerlukan xref/store scan tambahan atas seluruh relevant code, bukan inferensi dari scan parsial.
