# Status penelitian

Terakhir dirangkum: 2026-10-15

## Ringkasan

**Status: analisis statis awal; belum lengkap dan belum tervalidasi melalui debugging gameplay.**

Pemeriksaan sebelumnya mengekstrak struktur ISO dari dump PS1 raw-sector, membaca SYSTEM.CNF, mengidentifikasi executable utama, melakukan inspeksi/disassembly awal MIPS, dan menemukan beberapa struktur serta jalur kode. Namun, pemetaan overlay belum lengkap, rumus gameplay belum seluruhnya terhubung ke semua pemanggil, dan sesi emulator/debugger terkontrol belum dijalankan.

## Temuan yang didukung langsung oleh kode/data ROM

1. Executable boot yang dirujuk SYSTEM.CNF adalah SLPS_035.53.
2. Header executable mencatat alamat muat 0x80010000, PC 0x80011448, dan text size 0x5D800.
3. Struktur pemain yang diakses beberapa getter/setter memiliki empat slot; stride struktur 0xB4 byte dan nilai Chakra pada offset +0x18.
4. Setter Chakra yang diperiksa membatasi nilai tersimpan pada rentang -9.999 sampai 99.999. Ini bukan kondisi menang/kalah.
5. Jalur pemeriksaan akhir yang ditelusuri memuat cabang kondisi target Chakra. Untuk skenario awal yang dipetakan, nilai target konfigurasi adalah 3.000; pada cabang target yang sesuai, pemain yang memenuhi atau melampaui target dapat ditetapkan sebagai pemenang.
6. Data petak diperlakukan sebagai bitfield; jalur yang diperiksa memakai empat bit teratas sebagai ID pemilik. Arti seluruh bit lainnya belum terpetakan.
7. Kode memeriksa sejumlah flag kondisi akhir, tetapi label yang sesuai dengan semua pilihan menu belum terpetakan secara lengkap.

Alamat dan penjelasan lebih detail ada di docs/ROM_STRUCTURE.md, docs/OVERLAY_MAP.md, dan docs/GAME_RULES.md.

## Temuan dari UI terjemahan/panduan eksternal — bukan bukti formula universal

- Story stage 1 diterjemahkan sebagai Naruto melawan Mizuki dengan target 3.000 Chakra.
- Dalam contoh tampilan, biaya membangun barrier ditampilkan 60 Chakra; suatu contoh barrier level 1 menampilkan nilai 100 dan durability 2/2; suatu contoh peningkatan level 1 ke 2 menampilkan biaya 150.
- Sumber lain menampilkan barrier level 1 bernilai 50, sehingga nilai tidak boleh dianggap tetap tanpa memahami parameter/tipe barrier dan konteksnya.
- Beberapa deskripsi kartu memberi contoh penambahan Chakra, peningkatan statistik, atau manipulasi roulette.

Contoh UI di atas belum membuktikan bahwa 60 dan 150 adalah biaya universal atau bahwa formula seluruh barrier sudah diketahui.

## Pekerjaan terbuka utama

- Petakan loader, offset file, alamat muat, ukuran, entry point, dan lifecycle untuk seluruh overlay.
- Tentukan format arsip/resource DATA.BIN, DATA2.BIN, DUMMY.BIN, dan XASECT.BIN serta keterkaitan mereka dengan kode dan data.
- Temukan dan dokumentasikan sumber setiap harga barrier, biaya upgrade, pendapatan, nilai, level, dan durability.
- Petakan seluruh bitfield petak dan struktur barrier berdasarkan pembacaan serta penulisan field.
- Identifikasi jalur transaksi Chakra untuk bangun/upgrade/pendapatan/serangan/kartu dan efek pembatas nilainya.
- Hubungkan setiap flag kondisi menang ke record skenario, pilihan menu, dan tampilan teks.
- Telusuri algoritma roulette dan efek semua kartu sampai ke pemanggil sebenarnya.
- Jalankan skenario terkontrol di emulator/debugger dan bandingkan perubahan memori dengan analisis statis.

## Batas lingkungan saat ini

Pada pemeriksaan sebelumnya, tidak ditemukan emulator PS1 yang tersedia di lingkungan analisis; percobaan eksekusi terminal/Python berikutnya juga gagal karena lingkungan menolak eksekusi. Karena itu belum ada log eksekusi gameplay dari sesi kita. Laporan GameGear Archive bahwa ROM boot di test rig Mednafen adalah sumber eksternal dan bukan pengujian khusus biaya atau rumus permainan.

## Status confidence

- **Tinggi untuk metadata disc/EXE**: didukung header, SYSTEM.CNF, ukuran, hash, dan pencocokan CRC eksternal.
- **Tinggi untuk batas setter Chakra**: instruksi setter terlihat dan rentang penjepitan nilai telah diidentifikasi.
- **Menengah untuk cabang target skenario awal**: nilai target dari record konfigurasi dan jalur perbandingan ditemukan; pemetaan lengkap semua skenario tetap terbuka.
- **Rendah/belum pasti untuk biaya dan formula gameplay**: belum ada call chain lengkap ditambah tes runtime terkontrol.