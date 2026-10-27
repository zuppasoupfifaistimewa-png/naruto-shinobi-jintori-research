# Peta loader, modul, dan overlay — status sementara

## Ringkasan

Peta loader/overlay **belum lengkap**. Bagian ini menyimpan titik awal yang ditemukan agar analisis berikutnya dapat dilanjutkan tanpa menganggap alamat statis sebagai pemetaan runtime final.

## Executable utama

- File: SLPS_035.53
- RAM load address: 0x80010000
- Entry PC dari header: 0x80011448
- Text size: 0x5D800
- Format: PS-X EXE

Ini merupakan referensi alamat paling kuat saat ini karena berasal dari header executable.

## Modul data

| File | Observasi | Status |
|---|---|---|
| DATA.BIN | Bootstrap 0x44 byte diikuti direktori 0x2F00 byte berisi 1.504 entri resource (LBN, panjang byte); isi resource mencakup kode dan aset | Direktori resource didukung bukti langsung; format resource individual dan seluruh alamat muat masih belum dipetakan |
| DATA2.BIN | File besar dalam filesystem ISO | Format, segmentasi kode/data, dan loader belum dipastikan |
| DUMMY.BIN | File besar dalam filesystem ISO | Tujuan dan kemungkinan penggunaan runtime belum dipastikan |
| XASECT.BIN | File kecil 692 byte | Format dan hubungan dengan loader belum dipastikan |

Analisis byte-level lanjutan memperkuat hubungan bootstrap DATA.BIN dengan alamat sekitar 0x800AD450: rutin pada offset file DATA.BIN +0x04 berada di sekitar 0x800AD454 dan menyalin direktori +0x44 berukuran 0x2F00 ke RAM 0x8006D830. Ini menunjukkan pemetaan untuk blok bootstrap/direktori tersebut, tetapi **tidak berarti seluruh DATA.BIN dimuat sebagai satu overlay kontigu**. Alamat muat dan lifecycle resource lain tetap perlu dipetakan.

## Lokasi kode yang telah dicatat dan status pemetaan

### Executable utama (alamat tetap dalam SLPS_035.53)

| Alamat RAM | Perilaku yang diamati | Kepastian |
|---|---|---|
| 0x80012A44 | Getter konfigurasi yang mengembalikan field Chakra awal | Tinggi |
| 0x80012A70 | Getter target konfigurasi yang dibandingkan pada cabang kemenangan berbasis Chakra | Tinggi untuk peran target |
| 0x8001387C | Setter Chakra; memvalidasi indeks pemain < 4 dan menjepit nilai ke -9.999…99.999 | Tinggi |
| 0x800138EC | Getter Chakra untuk struktur pemain utama | Tinggi |
| 0x80012780 | Memilih record dari tabel konfigurasi 0x80064918 (stride 0x30) dan mengisi global konfigurasi | Tinggi untuk pemilihan/salin data |
| 0x80012EAC–0x80012Fxx | Memilih record dari tabel 0x80057798 (stride 0x54) dan menyalin field ke global konfigurasi | Tinggi untuk pemilihan/copy field |

Tabel konfigurasi pada executable utama:
- 0x80057798 (file offset 0x47F98): record stride 0x54. Empat word awal pada record memuat ID mentah / field +0x04 / +0x08 / +0x0C seperti (0xA00, 1500, 3000, 400), (0x10B01, 2000, 4000, 400), (0x20C02, 2000, 4000, 400), (0x81210, 600, 0, 0), (0x31403, 2500, 5000, 400), (0x40E04, 2500, 5000, 400), (0x81211, 600, 0, 0), (0x50F0F, 2500, 5000, 400), (0x61106, 3000, 6000, 400), (0x60809, 3000, 6000, 400).
- 0x80064918 (file offset 0x55118): record stride 0x30. Sekurangnya 13 record awal nonnol memiliki 1500, 3000, 400 di field +0x04/+0x08/+0x0C. Raw ID belum dipetakan lengkap ke nama mode/stage.
- Field +0x04 disalin ke global 0x80070C80 dan dipakai untuk inisialisasi Chakra; field +0x08 masuk melalui getter 0x80012A70 sebagai target; field +0x0C disalurkan ke getter 0x80012A90, tetapi semantiknya belum diketahui.
- Cabang kandidat pada resource DATA.BIN membaca target dari `0x80012A70`, membandingkan sebuah field record per peserta terhadapnya, dan pada sejumlah jalur memeriksa bit `0x200` atau menulis state sebelum memanggil routine transisi. Karena base entry-1 `0x800D0000`, beberapa boundary fungsi, serta efek `0x800EF98C`/`0x80100D14`/`0x80100DCC` belum tervalidasi, jangan menyebutnya jalur pemenang final: makna field, kondisi kemenangan, dan hasil transisi tetap **UNKNOWN**. Lihat [review semantik Step 6](STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md) dan [Step 8](STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md).

### Modul gameplay hasil pemetaan sementara (bukan executable utama)

DATA.BIN entry index 1 berada pada file offset 0x10BB000, ukuran 596.412 byte, dan berisi campuran string/event dan instruksi kode. Pemetaan sementara ke alamat RAM 0x800D0000 menghasilkan banyak referensi internal yang konsisten dalam kisaran 0x800D0000–0x8016xxxx. Titik jalur target pada peta statis ini antara lain 0x80111228, 0x801112CC, 0x801113B4, 0x801114F0, 0x80111588, dan 0x80112418. **Alamat kandidat belum divalidasi lewat breakpoint loader; gunakan sebagai peta statis sementara, bukan bukti runtime.**

DATA.BIN entry index 0 berada pada file offset 0x5F800, ukuran 110.536 byte; referensi internal mengarah konsisten ke area sekitar 0x800AD000. Base ini juga masih menunggu validasi loader.

### Koreksi terhadap label alamat lama

Label lama yang menyebut 0x800EC200 sebagai pemeriksaan target Chakra dan sekitar 0x800F70D0 sebagai aritmetika Chakra **ditarik kembali**: pemetaan modul sebelumnya tidak dibuktikan, dan alamat tersebut tidak boleh dipakai untuk klaim fungsi. Alamat resource/overlay dapat bertumpang tindih atau berubah menurut base pemetaan. Setiap klaim berikutnya harus mencatat identitas resource, offset file, asumsi base, dan alasan referensi internalnya konsisten.



## Rencana melengkapi peta overlay dan aturan gameplay

1. Prioritas pertama: telusuri call chain aksi ESTATE (membangun barrier) dan LVUP_ESTATE (upgrade), termasuk sumber harga, pemeriksaan saldo, nilai Chakra sebelum/sesudah, dan perubahan field petak.
2. Prioritas kedua: identifikasi kapan income diproses, rumusnya, hubungan level barrier dengan income, dan perubahan kepemilikan setelah kunjungan atau battle.
3. Prioritas ketiga: telusuri pengeluaran Chakra saat battle/jutsu, damage/durability, roulette, serta handler kartu menggunakan referensi ke setter/getter Chakra.
4. Lacak selektor tabel konfigurasi 0x80057798 dan 0x80064918 sampai raw ID bisa dipetakan ke Story/Party mode, tanpa menebak nama mode dari ID mentah.
5. Untuk setiap fungsi/data kandidat, cantumkan identitas resource, offset file, ukuran, base RAM hipotesis, bukti referensi silang, serta confidence. Jangan memberi nama fungsi hanya karena ada konstanta yang sama.
6. Jika emulator/debugger tersedia, validasi call chain dengan breakpoint dan tes terkontrol. Jika tidak, tandai semua kesimpulan sebagai statis.
7. Format PK02/BIN0/TPK0 dilanjutkan hanya saat dibutuhkan untuk memulihkan kode/parameter yang relevan dengan aturan gameplay.

## Direktori resource DATA.BIN — hasil byte-level 2026-10-15

Temuan berikut menggantikan status sebelumnya yang menganggap keberadaan tabel resource masih sekadar dugaan:

1. Pada executable `SLPS_035.53`, file offset `0x46098` (RAM `0x80055898`) tersimpan pasangan little-endian `0x000000D4, 0x00002F44`. Nilai pertama adalah LBN 212, tepat extent ISO dari `DATA.BIN`; nilai kedua 12.100 byte.
2. Bootstrap yang ditunjuk pasangan tersebut mempunyai ukuran `0x2F44. `DATA.BIN` offset `0x00–0x43` berisi kode bootstrap; mulai offset `0x44` terdapat tabel sebesar `0x2F00 byte.
3. Tabel berisi 1.504 entri berukuran 8 byte. Interpretasi paling kuat untuk setiap entri ialah dua uint32 little-endian: LBN CD dan panjang data dalam byte. Kode mengonversi panjang menjadi jumlah sektor dengan pembulatan ke atas pada batas `0x800) byte.
4. Kode di sekitar `0x800AD454` menyalin `0x2F00 byte dari `0x800AD494` ke alamat `0x8006D830, konsisten dengan menyalin tabel dari offset `+0x44 bootstrap. Lokasi pemanggilan di executable menyetel alamat tujuan pada delay slot.
5. Dari 1.504 entri, 1.500 aktif dan empat berukuran nol (indeks 1491–1494). Interval sektor entri aktif tidak saling tumpang-tindih dan berada di dalam extent `DATA.BIN` pada LBN [212, 32446). Total interval yang tercakup adalah 32.227 sektor dari 32.234 sektor file. Tujuh sektor selisih cocok dengan enam sektor bootstrap yang dibulatkan dan satu sektor akhir yang tidak tercakup.

Ini memberikan keyakinan **tinggi** bahwa executable memakai bootstrap DATA.BIN untuk mendaftarkan direktori resource berbasis LBN/panjang. Ini belum mengidentifikasi format setiap resource atau seluruh pemuatan runtime. Detail signature dan hash tercatat di [RESOURCE_CATALOG.md](RESOURCE_CATALOG.md).

## Survei kode DATA.BIN entry index 1 — 2026-10-27

Run Ghidra [#40439763833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40439763833) berhasil memvalidasi sumber disc, mengekstrak DATA.BIN sementara, dan menganalisis entry index 1 (offset 0x10BB000, 596.412 byte; SHA-256 potongan 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a). Artefak hasil teks: [artifact 12705072941](https://api.github.com/repos/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/artifacts/12705072941). Base impor 0x800D0000 masih hipotesis; runtime loader belum dibuktikan.

Enam lokasi kandidat pada base tersebut — 0x80111228, 0x801112CC, 0x801113B4, 0x801114F0, 0x80111588, 0x80112418 — memanggil getter target utama 0x80012A70. Dua pemanggil lainnya berada pada FUN_8012A9C4 (call site 0x8012AA2C) dan FUN_80137AD8 (call site 0x80137C34). Instruksi pada enam target menghitung alamat record dengan stride 0x90, membandingkan field word dengan nilai yang dikembalikan getter, lalu pada jalur yang lolos menulis field state dan/atau memanggil FUN_800EF98C; salah satu jalur memanggil FUN_80100D14(1) dan FUN_80100DCC(0xDF) setelah pembandingan. Ini merupakan bukti statis yang kuat bagi jalur pemeriksaan threshold target Chakra, bukan bukti final bahwa suatu lokasi merupakan event kemenangan Story Mode.

Referensi ke setter Chakra utama 0x8001387C juga ditemukan dari sembilan call sites di resource, termasuk fungsi kandidat FUN_800D5608, FUN_800E1188, FUN_800D8918, FUN_8011C0D0, FUN_8010478C, dan FUN_80101814. Referensi ke getter nilai Chakra pemain 0x800138EC muncul pada 16 call sites. Detail dekompilasi fungsi-fungsi itu menjadi target Langkah 6.

Jaga label fakta/hipotesis: call target dan operasi perbandingan adalah temuan statis; penamaan event serta base RAM masih provisional sampai mapping loader/runtime divalidasi. Emulator/gameplay tidak dijalankan; resource tidak dimasukkan ke Git/artifact.
