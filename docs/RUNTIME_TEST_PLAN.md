# Rencana uji runtime PS1

## Tujuan

Menghubungkan temuan statis dengan keadaan permainan yang benar-benar diamati. **Belum ada pengujian gameplay terkontrol yang diselesaikan dalam sesi penelitian ini.** Laporan kompatibilitas eksternal hanya menyatakan ROM pernah boot pada test rig; itu tidak membuktikan rumus permainan.

## Persiapan

1. Gunakan ROM yang identitas/hash-nya dicatat di docs/ROM_STRUCTURE.md. Jangan patch ROM asli.
2. Pilih emulator/debugger PS1 yang mendukung breakpoint MIPS, inspeksi RAM, save state, trace instruksi, serta log akses memori. Catat nama dan versi emulator.
3. Gunakan salinan kerja lokal dengan hak yang sesuai; jangan mengunggah ROM ke repo.
4. Catat setiap test case: hash ROM, emulator/build, mode permainan, skenario, pemain aktif, aksi, nilai awal, nilai akhir, PC breakpoint, dan alamat RAM yang berubah.
5. Jalankan baseline tanpa aksi khusus untuk membedakan perubahan normal per giliran dari perubahan akibat aksi.

## Variabel yang dipantau

- Empat struktur pemain yang diduga berstride 0xB4 dan field Chakra pada offset +0x18: verifikasi ulang di RAM setelah loader/overlay aktif.
- ID pemain aktif dan penghitung giliran.
- Field petak: owner bits, level/jenis, durability, nilai/harga, dan atribut yang belum dipetakan.
- Konfigurasi target/opsi skenario.
- ID kartu yang dipilih, ID jutsu, hasil roulette, keadaan battle, dan ID pemenang.

Alamat RAM yang diketahui dari static analysis harus diperlakukan sebagai breakpoint awal saja sampai overlay dan alokasi RAM diverifikasi.

## Matriks eksperimen

### A. Inisialisasi Story Stage 1

- Mulai stage pertama dari keadaan bersih.
- Catat Chakra setiap pemain sebelum dan sesudah inisialisasi.
- Temukan record konfigurasi yang dibaca saat stage dimulai.
- Konfirmasi hubungan field +0x04, +0x08, +0x0C dengan nilai awal, target, dan parameter lain.
- Pastikan siapa yang menang jika Chakra sama dengan target dan jika satu angka di bawah target; gunakan keadaan yang aman/reproducible.

### B. Membangun barrier

- Pilih petak kosong dengan saldo Chakra yang cukup.
- Catat saldo sebelum konfirmasi, saat transaksi, dan sesudah barrier muncul.
- Ulangi dengan tipe petak/skenario berbeda bila tersedia.
- Breakpoint pada setter Chakra serta rutin perubahan field petak.
- Temukan asal nilai biaya di register/memori, bukan hanya konstanta yang kebetulan terlihat di disassembly.
- Uji saldo tepat di bawah, sama dengan, dan di atas biaya yang terlihat di UI jika memungkinkan.

### C. Meningkatkan level barrier

- Mulai dari barrier level 1 yang nilai/durability awalnya dicatat.
- Catat saldo, level, nilai, dan durability sebelum/sesudah upgrade.
- Ulangi untuk level dan tipe barrier berbeda.
- Pisahkan biaya upgrade dari biaya bangun dan dari animasi/transisi UI.

### D. Pendapatan dan kunjungan ke petak

- Jalankan satu giliran yang melewati petak sendiri dan petak lawan dengan save state yang sama.
- Catat saldo masing-masing pemain sebelum/sesudah pendaratan dan akhir giliran.
- Uji apakah pendapatan datang pada pemilik, pengunjung, atau keduanya; apakah efek bergantung level/tipe/bonus.
- Ulangi tanpa lawan mendarat untuk mendapat baseline.

### E. Battle, damage, dan pengambilalihan barrier

- Siapkan pertarungan pada barrier musuh dengan kondisi karakter/jutsu yang dapat diulang.
- Catat saldo dan field barrier sebelum battle, di setiap titik damage, setelah menang/kalah.
- Uji jutsu berbeda dan karakter berbeda.
- Bandingkan kemenangan di wilayah tanpa barrier bila bisa dibuat.
- Pisahkan biaya untuk mulai menyerang, biaya jutsu, damage durability, transfer kepemilikan, dan hadiah setelah menang.

### F. Kartu

Untuk setiap kartu:
- Catat ID kartu dan ID handler yang dipanggil.
- Catat semua state sebelum/sesudah: Chakra, statistik, skip-turn/status, hasil roulette berikutnya, kepemilikan Scroll of Seals, serta penghitung.
- Untuk kartu yang memodifikasi beberapa roulette, uji kedua lemparan dan kapan efek habis.
- Uji batas maksimum/minimum dan cara pembulatan.
- Bandingkan hasil dengan transkripsi di docs/GAME_RULES.md dan dokumentasi komunitas.

### G. Kondisi kemenangan alternatif

- Temukan record/bit opsi yang dipilih lewat menu Party Mode.
- Untuk setiap opsi, lakukan satu test case positif (syarat terpenuhi) dan satu negatif (satu syarat tidak terpenuhi).
- Periksa kapan game menetapkan ID pemenang, kapan mengubah screen/state, dan arti field pemenang 0xFF.
- Uji target Chakra tanpa opsi tambahan dan target dengan opsi tambahan untuk melihat prioritas kondisi ketika beberapa syarat terpenuhi bersamaan.

## Format tabel hasil

| Test ID | Kondisi awal | Aksi | Nilai/state sebelum | Nilai/state sesudah | PC/overlay | Hasil | Status |
|---|---|---|---|---|---|---|---|
| RT-001 | Belum dijalankan | — | — | — | — | — | Open |

Setiap test harus dilengkapi screenshot atau log debugger dan, jika relevan, hash/save-state untuk reproduksi. Jangan menyebut formula “terbukti runtime” tanpa hasil yang bisa diulang.

## Kriteria selesai

- Loader/overlay aktif teridentifikasi untuk setiap breakpoint.
- Nilai biaya/pendapatan berasal dari field atau rumus yang terpetakan sampai pemanggilnya.
- Formula yang memiliki cabang berbeda dites pada sekurangnya satu contoh per cabang penting.
- Semua flag opsi kemenangan dapat dikaitkan dengan pilihan menu/data record dan hasil permainan.
- Hasil runtime sesuai analisis statis; bila berbeda, catat perbedaan dan revisi hipotesis.
- Laporan final membedakan aturan normal, variasi skenario, dan kondisi yang hanya tersedia setelah unlock.