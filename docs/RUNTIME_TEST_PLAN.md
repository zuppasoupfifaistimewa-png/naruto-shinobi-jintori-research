# Rencana uji runtime PS1

## Tujuan dan status

Emulator/debugger adalah jalur riset utama bersama analisis statis, bukan sekadar opsi terakhir. Gunakan runtime untuk memverifikasi nilai sebelum/sesudah aksi dan menguji cabang kode yang benar-benar berjalan. **Belum ada pengujian gameplay runtime terkontrol yang diselesaikan.** Lihat [EMULATOR_WORKFLOW.md](EMULATOR_WORKFLOW.md) untuk pilihan emulator dan prosedur yang lebih rinci.

Pada 2026-10-15, pemeriksaan environment tidak menemukan executable emulator. Akses jaringan dari container gagal pada resolusi DNS, sehingga emulator tidak dapat dipasang saat sesi berjalan. ROM dapat diakses dari Library dan hashnya cocok; kendala saat ini adalah tidak tersedianya emulator yang bisa dieksekusi di environment, bukan kebutuhan mengunggah ulang ROM. Jangan meminta upload ulang ROM ~326 MB dari laptop.

## Persiapan

1. Prioritaskan PCSX-Redux untuk breakpoint CPU, memory editor, dan GDB server; lihat [EMULATOR_WORKFLOW.md](EMULATOR_WORKFLOW.md). Mednafen adalah alternatif untuk cek silang.
2. Gunakan image BIN/CUE dengan hash dari `docs/ROM_STRUCTURE.md`; jangan patch ROM asli. CUE harus merujuk file BIN yang sama dan track Mode 2/2352.
3. Catat versi/build emulator, jenis BIOS, setting CPU/interpreter/debugger, hash ROM, mode permainan, skenario, pemain aktif, aksi, nilai awal/akhir, PC breakpoint dan alamat RAM yang berubah.
4. Jalankan baseline dari state awal terkontrol. Untuk pengulangan, simpan state/memory card eksperimen di luar repo dan jangan menimpa save asli.
5. Jangan menganggap alamat overlay statis sebagai RAM live sebelum loader/base overlay dikonfirmasi. Mulai dari breakpoint executable utama dan verifikasi perubahan RAM.

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