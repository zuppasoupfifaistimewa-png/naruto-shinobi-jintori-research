# Aturan permainan — bukti kode vs sumber eksternal

## Aturan bukti

Dokumen ini memisahkan tiga tipe bukti:

- **Kode/data ROM:** observasi dari instruksi atau data yang benar-benar dibaca dari file.
- **UI terjemahan/panduan:** transkripsi antarmuka atau penjelasan eksternal; berguna untuk membentuk hipotesis, tetapi tidak membuktikan semua jalur implementasi.
- **Belum pasti:** butuh call chain lengkap, pemetaan overlay, atau uji runtime.

## 1. Papan dan alur dasar — sumber eksternal

Sumber resmi promosi TV Tokyo menggambarkan Story Mode dan Versus/対戦 Mode, serta pertarungan saat memasuki wilayah musuh. Ulasan gameplay Jepang juga menjelaskan roulette untuk bergerak, membangun barrier di petak kosong, menaikkan level barrier untuk meningkatkan pendapatan, dan interaksi dengan wilayah lawan.

Ini selaras dengan konsep board game penguasaan wilayah, tetapi dokumentasi eksternal tersebut bukan bukti formula internal.

## 2. Chakra dan target kemenangan — bukti kode statis

### Struktur dan batas nilai

- Struktur yang diperiksa memiliki empat slot pemain, berjarak 0xB4 byte; nilai Chakra berada pada offset +0x18.
- Getter/setter yang ditelusuri membaca/menulis Chakra di 0x80070EA0 + indeks_pemain × 0xB4 + 0x18.
- Setter 0x8001387C memvalidasi indeks pemain di bawah 4 dan menjepit nilai tersimpan ke rentang inklusif -9.999 sampai 99.999. Ini batas penyimpanan, bukan kondisi menang/kalah.
- Jalur inisialisasi mengisi Chakra awal tiap pemain dari record konfigurasi melalui getter 0x80012A44; nilai sumber berasal dari field +0x04.

### Target kemenangan bukan satu angka global

Executable utama mempunyai tabel konfigurasi pada alamat RAM 0x80057798 (record 0x54 byte) dan tabel kedua pada 0x80064918 (record 0x30 byte). Di tabel pertama, field +0x04 dipakai sebagai Chakra awal dan field +0x08 disalurkan ke getter 0x80012A70 sebagai target pada jalur kemenangan Chakra. Jalur hasil yang dipetakan membandingkan Chakra pemain dengan target terkonfigurasi; saat kondisi opsi terkait aktif (bit 0x200 pada record kondisi yang diperiksa), nilai Chakra yang mencapai/melewati target dapat menetapkan pemain sebagai pemenang.

| Record ID mentah | Chakra awal | Field target (+0x08) | Field +0x0C | Status interpretasi |
|---|---:|---:|---:|---|
| 0x00000A00 | 1.500 | 3.000 | 400 | Jalur target cocok; pemetaan ID ke nama skenario belum selesai |
| 0x00010B01 | 2.000 | 4.000 | 400 | Data tabel; nama skenario belum dipastikan |
| 0x00020C02 | 2.000 | 4.000 | 400 | Data tabel; nama skenario belum dipastikan |
| 0x00081210 | 600 | 0 | 0 | Mungkin kondisi akhir non-target; target 0 tidak boleh ditafsirkan sebagai menang seketika |
| 0x00031403 | 2.500 | 5.000 | 400 | Data tabel; nama skenario belum dipastikan |
| 0x00040E04 | 2.500 | 5.000 | 400 | Data tabel; nama skenario belum dipastikan |
| 0x00081211 | 600 | 0 | 0 | Mungkin kondisi akhir non-target; belum dikonfirmasi |
| 0x00050F0F | 2.500 | 5.000 | 400 | Data tabel; nama skenario belum dipastikan |
| 0x00061106 | 3.000 | 6.000 | 400 | Data tabel; nama skenario belum dipastikan |
| 0x00060809 | 3.000 | 6.000 | 400 | Data tabel; nama skenario belum dipastikan |

Tabel kedua di 0x80064918 memiliki sekurangnya 13 record awal nonnol yang diperiksa dengan field awal/target 1.500/3.000 dan field +0x0C = 400. Ini membuktikan bahwa target dipilih lewat konfigurasi dan 3.000 bukan target universal bagi semua record.

**Batas bukti dan confidence:**
- **Tinggi:** field +0x04 dipakai sebagai nilai awal Chakra; field +0x08 dipakai sebagai target pada cabang kemenangan.
- **Menengah–tinggi:** cabang dengan kondisi bit 0x200 dapat menetapkan pemenang ketika Chakra mencapai/melewati target; base RAM resource gameplay masih perlu validasi loader.
- **Belum diketahui:** makna field +0x0C (400 atau 0), pemetaan ID mentah ke nama Story stage/Party rule, dan seluruh mode yang memilih salah satu tabel.
- Terjemahan fan untuk Story Act 01 menyebut target 3.000 Chakra. Ini cocok dengan salah satu record, tetapi mapping ID satu-ke-satu belum terbukti.

Semua temuan bagian ini berasal dari analisis statis atas berkas Library; tidak ada eksperimen gameplay runtime yang dijalankan.

## 3. Barrier/petak — status

### Yang diketahui dari struktur kode

Data petak diproses sebagai bitfield. Pada jalur yang diperiksa, empat bit paling atas dipakai sebagai ID pemilik. Field lainnya ditafsirkan oleh beberapa cabang sebagai atribut/jenis/level petak, tetapi pemetaan lengkap semua bit belum selesai.

Ada label internal atau nama resource seperti ESTATE, LVUP_ESTATE, CHAKRA_DOWN, FUUIN_GET, NINJYUTU, dan KABE dalam data yang diperiksa. Label tersebut merupakan petunjuk untuk pencarian, bukan bukti tunggal tentang rumus atau perilaku.

### Contoh UI terjemahan yang pernah dicatat

- Contoh biaya membangun barrier pada petak kosong: 60 Chakra.
- Contoh barrier level 1: nilai 100, durability 2/2.
- Contoh peningkatan level 1 menjadi 2: biaya 150 Chakra.
- Ada contoh barrier level 1 lain dengan nilai 50.

Angka ini berasal dari contoh tampilan/transkripsi panduan. Nilai barrier yang berbeda menjadi alasan untuk tidak menyimpulkan ada satu nilai tetap untuk semua barrier. Hingga call chain kode transaksi ditemukan, 60 dan 150 **bukan biaya universal terkonfirmasi**.

### Hal yang harus dilacak

- Apakah harga berasal dari field pada record petak, tipe barrier, level, karakter, atau kondisi skenario.
- Apakah saldo Chakra diperiksa sebelum transaksi dan apakah saldo boleh negatif.
- Aturan upgrade, maksimum level, durability awal, pengurangan durability saat diserang, serta kondisi hilangnya pemilik.
- Kapan pendapatan diproses: saat pemain mendarat, saat lawan mendarat, saat giliran selesai, atau kombinasi kondisi.
- Apakah kemenangan pertarungan langsung mengambil barrier atau melewati tahapan tambahan.

## 4. Battle dan wilayah musuh — sumber eksternal

Halaman promosi resmi TV Tokyo menyebut wilayah musuh dapat direbut dengan paksa dan bahwa memasuki wilayah musuh memicu battle. Ulasan gameplay Jepang 2025 menyebut pemain dapat menyerang barrier, merusak/menghancurkannya, dan mengambil barrier lawan setelah menang.

Ini merupakan petunjuk gameplay dari sumber eksternal. Formula peluang menang, statistik yang dipakai, pengaruh jutsu, damage per ronde, dan biaya Chakra belum ditelusuri sampai tuntas dari kode.

## 5. Kartu — deskripsi dari transkripsi komunitas

Catatan kartu dari terjemahan komunitas yang pernah dibaca mencakup contoh efek berikut (nama Inggris dapat merupakan terjemahan nonresmi):

| Nama terjemahan yang dicatat | Efek yang disebut dalam sumber | Bukti |
|---|---|---|
| Lessons | +100 Chakra | UI/transkripsi komunitas, belum diverifikasi rumus kode |
| Seal Binding | +400 Chakra | UI/transkripsi komunitas |
| How Chakra Works | +500 Chakra | UI/transkripsi komunitas |
| Attack Power Up | +1 Attack Power | UI/transkripsi komunitas |
| Skill Points | +1 Skill Point | UI/transkripsi komunitas |
| Senbon | Lawan melewatkan giliran | UI/transkripsi komunitas |
| Attack Concentration | Mengurangi setengah biaya Chakra jutsu serang | UI/transkripsi komunitas; pembulatan/peraturan minimum belum diketahui |
| Weight | Dua roulette berikutnya dibatasi 1–3 | UI/transkripsi komunitas |
| Physical Activation | Dua roulette berikutnya 10–12 | UI/transkripsi komunitas |

Daftar ini bukan katalog final seluruh kartu. Angka dan implementasi tiap efek perlu ditautkan ke ID kartu, handler efek, dan call chain yang memperbarui state.

## 6. Scroll of Seals dan kondisi Party Mode — panduan eksternal

Panduan Jepang mencatat beberapa syarat untuk membuka opsi kemenangan Party Mode tambahan setelah syarat Story tertentu dipenuhi:

1. “Red ink/drop out” setelah pemain pernah mencapai Chakra negatif.
2. Pertandingan dipaksa berakhir setelah jumlah giliran yang ditentukan; panduan menyebut 40 giliran.
3. Menang sambil membawa Scroll of Seals setelah menggunakan Ultimate Chakra Great Absorption, dengan syarat berjalan mengelilingi map.
4. Menang sambil membawa Scroll of Seals setelah semua teknik scroll digunakan.

Ini adalah opsi yang disebut terbuka melalui progres Story menurut panduan tersebut—bukan satu kumpulan syarat yang otomatis berlaku pada semua pertandingan. Flag kode untuk setiap opsi belum dipasangkan satu per satu dengan menu dan data skenario.

## 7. Kondisi akhir — observasi kode statis

- Kode mempunyai beberapa cabang akhir yang dikendalikan flag kondisi dan field konfigurasi.
- Flag yang terlihat diperiksa termasuk 0x001, 0x002, 0x004, 0x008, 0x020, 0x040, 0x080, 0x100, 0x200, dan 0x1000; belum seluruhnya dipetakan ke label menu.
- Cabang kemenangan berbasis Chakra menggunakan target dari getter 0x80012A70 dan kondisi terkait yang memeriksa bit 0x200 pada record kondisi yang ditelusuri.
- Pada jalur target yang dipetakan, Chakra pemain dibandingkan dengan target dan pemain yang mencapai/melewatinya dapat ditetapkan sebagai pemenang. Ini temuan statis; belum ada uji runtime.
- Ada cabang yang menyimpan 0xFF sebagai ID pemenang. Makna hasil seri/tanpa pemenang belum dapat dipastikan tanpa menelusuri pemanggil dan/atau mengamati hasil runtime.
- Ada pemeriksaan nilai Chakra negatif dan transisi status, tetapi belum terbukti semua mode langsung mengeliminasi pemain pada nilai negatif.

Jangan samakan target konfigurasi 0 dengan kemenangan instan. Record dengan target 0 kemungkinan dipakai pada kondisi akhir lain, tetapi pemetaannya belum selesai.

## 7A. Apa yang dibuktikan jalur setter Chakra — dan yang tidak

Penelusuran call site memperlihatkan mengapa pemanggilan setter 0x8001387C harus dibaca bersama instruksi sebelumnya:

- Banyak call site, misalnya 0x800D6D60, 0x800D6E04, 0x800D7AB0, 0x800D7B14, 0x800D8DE8, dan 0x801016E8, mengambil nilai Chakra dari sebuah record lalu menyalinnya ke struktur pemain aktif. Call site tersebut sendiri **bukan** bukti biaya atau pengurangan Chakra.
- Dalam state machine resource yang sementara dipetakan ke base 0x800D0000, jumlah pending +0xB44 diproses bertahap pada state +0xB2A == 7: sebagian nilai diterapkan ke Chakra pemain yang ditunjuk +0xB2B lewat getter/setter, lalu jumlah pending dikurangi sampai habis. Nilai itu disalin dari +0xB40, yang dibentuk dari +0xB30 + +0xB38. Ini menunjukkan mekanisme untuk menerapkan perubahan Chakra secara bertahap, tetapi belum membuktikan bahwa jumlahnya adalah biaya barrier. Sumber field +0xB30/+0xB38 serta identitas aksinya belum diketahui.
- Jalur sekitar 0x8011C0D0 memiliki cabang yang membalik tanda nilai Chakra untuk pemain dan menjepit batas negatif ke -9.999. Namun, identitas pemicu/label menu yang memilih jalur ini belum cukup jelas; jangan menamakannya sebagai aturan “red debt” atau kartu tertentu tanpa bukti tambahan.
- Base alamat resource di atas masih kandidat hasil pencocokan referensi internal dan belum divalidasi melalui breakpoint loader/emulator. Alamat tersebut merupakan bukti disassembly statis, bukan observasi saat permainan berjalan.

Dengan demikian, biaya bangun/upgrade hanya dapat dinyatakan **terlihat pada UI contoh** (60 dan 150 Chakra), belum diketahui sebagai konstanta atau formula kode. Langkah berikutnya harus menemukan sumber pengisian delta, pemeriksaan saldo sebelum transaksi, dan mutasi field petak pada aksi ESTATE/LVUP_ESTATE.
 
## 8. Kesimpulan saat ini

**Aturan yang paling kuat dari kode:** setter membatasi nilai Chakra; konfigurasi menyediakan Chakra awal dan target yang bervariasi; pada cabang target tertentu, pemain menang setelah Chakra mencapai atau melewati target. 3.000 berlaku pada sebagian record, bukan target universal. Angka 60 dan 150 dari contoh UI belum terbukti sebagai biaya universal. Formula bangun/upgrade barrier, income, durability, battle, roulette, efek seluruh kartu, dan label seluruh flag masih memerlukan tracing lanjutan serta validasi runtime bila emulator tersedia.


## Referensi eksternal — hanya bukti UI/panduan

- [Transkripsi UI Story Mode oleh proyek terjemahan komunitas](https://github.com/juanoliveira82/naruto-ps1_translation-english/blob/master/Story-mode.md): Act 01 menampilkan target Chakra 3000; tampilan bangun barrier menunjukkan kebutuhan 60 Chakra; contoh upgrade level 1 ke level 2 menunjukkan kebutuhan 150 Chakra; contoh barrier level 1 menunjukkan nilai 100 dan durability 2/2, sementara contoh lain menunjukkan nilai 50. Ini bukti bahwa angka tersebut tampil dalam konteks tertentu, bukan bukti harga universal untuk setiap petak/barrier.
- [Materi TV Tokyo tentang game PS1](https://www.tv-tokyo.co.jp/anime/naruto2002/goods/playstation.html): sumber promosi untuk Story/Versus serta pertarungan saat masuk wilayah lawan.
- [Halaman pengembang/kontraktor ROUTE134 tentang game](https://route134.stars.ne.jp/service/naruto.html): uraian umum tentang permainan papan penguasaan wilayah, gerak roulette, penggunaan Chakra untuk mengambil petak, serta battle saat memasuki wilayah musuh.

Sumber UI/eksternal ini membantu memberi nama pada aksi dan membuat hipotesis; mereka tidak menggantikan call chain kode atau tes runtime untuk menetapkan rumus universal.