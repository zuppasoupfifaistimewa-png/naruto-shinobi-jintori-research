# Aturan permainan — bukti kode vs sumber eksternal

## Aturan bukti

Dokumen ini memisahkan tiga tipe bukti:

- **Kode/data ROM:** observasi dari instruksi atau data yang benar-benar dibaca dari file.
- **UI terjemahan/panduan:** transkripsi antarmuka atau penjelasan eksternal; berguna untuk membentuk hipotesis, tetapi tidak membuktikan semua jalur implementasi.
- **Belum pasti:** butuh call chain lengkap, pemetaan overlay, atau uji runtime.

## 1. Papan dan alur dasar — sumber eksternal

Sumber resmi promosi TV Tokyo menggambarkan Story Mode dan Versus/対戦 Mode, serta pertarungan saat memasuki wilayah musuh. Ulasan gameplay Jepang juga menjelaskan roulette untuk bergerak, membangun barrier di petak kosong, menaikkan level barrier untuk meningkatkan pendapatan, dan interaksi dengan wilayah lawan.

Ini selaras dengan konsep board game penguasaan wilayah, tetapi dokumentasi eksternal tersebut bukan bukti formula internal.

## 2. Chakra — bukti kode

### Struktur pemain

- Empat slot pemain ditemukan pada struktur yang diperiksa.
- Jarak antarstruktur: 0xB4 byte.
- Offset +0x18 berisi nilai Chakra pada jalur getter/setter yang ditelusuri.
- Setter yang diperiksa menjepit nilai tersimpan ke rentang -9.999 sampai 99.999.

### Target skenario awal

Pada konfigurasi skenario awal yang ditelusuri terdapat nilai 1.500, 3.000, dan 400 pada offset record +0x04, +0x08, dan +0x0C. Jalur kondisi target menggunakan 3.000 untuk membandingkan nilai pemain. Makna tepat dari 1.500 dan 400 belum terkonfirmasi penuh.

Pada cabang target yang diperiksa, kode membandingkan nilai Chakra terhadap target dan dapat menetapkan ID pemain sebagai pemenang jika nilai mencapai atau melampaui target.

**Batas klaim:** tidak disimpulkan bahwa semua skenario dan Party Mode memakai target 3.000.

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

- Jalur pemeriksaan akhir memiliki banyak cabang yang digerakkan oleh flag kondisi dan nilai konfigurasi.
- Flag yang terlihat diperiksa mencakup bit seperti 0x001, 0x002, 0x004, 0x008, 0x020, 0x040, 0x080, 0x100, 0x200, dan 0x1000.
- Cabang target Chakra berhubungan dengan perbandingan target dan penetapan pemenang.
- Ada cabang yang menulis 0xFF ke field ID pemenang. Maknanya sebagai hasil seri/tanpa pemenang masih harus dipastikan dengan menelusuri pemanggil serta mengamati keadaan hasil saat runtime.
- Ada pemeriksaan nilai negatif dan perubahan keadaan. Belum terbukti bahwa setiap pemain langsung tereliminasi pada Chakra negatif.

Jangan memberi nama pada semua flag hanya berdasarkan nilai bit atau panduan; cocokkan terlebih dahulu record opsi, pemrosesan menu, dan jalur hasil.

## 8. Kesimpulan saat ini

Yang paling kuat didukung oleh kode adalah batas setter Chakra, struktur pemain yang sudah dipetakan sebagian, bitfield kepemilikan petak pada jalur yang diperiksa, dan cabang target Chakra untuk skenario awal. Biaya barrier/upgrade, formula income/durability/battle, roulette, efek seluruh kartu, dan label seluruh flag kondisi masih memerlukan penelusuran statis lengkap serta pengujian runtime.