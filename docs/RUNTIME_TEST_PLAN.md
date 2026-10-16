# Status terbaru 2026-10-17 — sesudah tes kontroler Analog

- Run [#38973267415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973267415) sukses. Port 1 disetel ke Analog, tersambung, dan di-remap sebelum boot.
- AnyLinux dan upstream HEAD sama-sama mengenali disc `SLPS-03553`, menyelesaikan pemuatan 187 sektor executable, mencapai `EXEC:PC0(80011448)` lalu `Execute !`. Peringatan `Unknown command for pad: 43` hilang pada kedua log; sebelumnya muncul pada keduanya di run baseline #38971848277.
- Ini mengonfirmasi koreksi protokol controller, tetapi **belum membuktikan** title/menu dan input in-game. Kedua tes headless tetap mencapai batas 90 detik.
- GUI probe baru ada pada workflow commit [85c08d9](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85c08d9ea255dc400c0771361abc95817a0a7ba6), run [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926). Pada saat catatan ini ditambahkan, run masih terlihat in progress; ambil log akhirnya untuk memeriksa dua frame pada detik 10 dan 20, metrik piksel, OCR Jepang/Inggris, dan penanda boot. Frame dan log GUI sementara dihapus oleh cleanup.

---

# Rencana uji runtime PS1

## Tujuan dan status

Emulator/debugger adalah jalur riset utama bersama analisis statis, bukan sekadar opsi terakhir. Gunakan runtime untuk memverifikasi nilai sebelum/sesudah aksi dan menguji cabang kode yang benar-benar berjalan. **Belum ada pengujian gameplay runtime terkontrol yang diselesaikan.** Lihat [EMULATOR_WORKFLOW.md](EMULATOR_WORKFLOW.md) untuk pilihan emulator dan prosedur yang lebih rinci.

Pada 2026-10-15, PCSX-Redux AppImage sudah dipaketkan ke release repo Naruto dan SHA-256-nya diverifikasi via GitHub Actions. GUI berhasil dijalankan pada layar virtual. OpenBIOS default sudah dibangun dan disimpan sebagai Release asset, tetapi uji dengan BIOS tersebut belum menghasilkan bukti visual bahwa game masuk ke menu/title. Workflow #38693918169 berhasil membangun varian shell/menu dan `BOOT_MODE=fast`. Uji lokal dengan `-bios openbios.bin -interpreter -debugger -iso game.cue -run` pada varian fastboot menghasilkan layar hitam setelah sekitar 12 detik; belum terkonfirmasi bahwa game mencapai title/menu. Gunakan asset release beserta checksum, lalu cari sebab boot tidak terlihat sebelum mengklaim runtime berhasil. Jangan meminta upload ulang ROM ~326 MB dari laptop.

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

## Status boot sebelum uji gameplay — pembaruan 2026-10-16

Boot masih bermasalah, jadi pengujian aturan gameplay (biaya, income, battle, efek kartu, kemenangan) belum dimulai. Jangan lanjut ke test case RT-001 sampai game menampilkan menu/title yang dikenali dan kontrol terbukti responsif.

Fakta terakhir:
- Normal CD boot membaca `SYSTEM.CNF` tetapi macet di pengambilan payload `SLPS_035.53`.
- Varian pemuat 1 sektor menunjukkan progres pembacaan, sedangkan 8 sektor/16 KB dan 32 sektor belum menyelesaikan payload. Varian diagnostik satu sektor: [Actions #38697240018](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38697240018).
- Jalur inject EXE mencapai `0x80011448` dan `CD_init`, tetapi layar hitam; perhatikan `flushCache`, init CD-ROM dan wait init kartu memori.
- Ada petunjuk input: perintah pad `0x43` muncul saat emulator kemungkinan memakai tipe Digital; uji konfigurasi Port 1 Analog/DualShock terlebih dahulu. Petunjuk sumber: https://github.com/grumpycoders/pcsx-redux/blob/db9bc8af44e3c77424127b573c17f9583ee2ab95/src/core/pad.cc.
- ZIP alternatif yang baru diunggah pengguna belum dapat diperiksa/dijalankan oleh runtime pada sesi ini. Jangan mengubah kesimpulan status boot hanya karena file alternatif sudah tersedia.

Urutan lanjutan yang disarankan: (1) verifikasi isi dan cara menjalankan ZIP alternatif saat lingkungan file tersedia; (2) set Port 1 Analog/DualShock; (3) ulangi CD boot dengan BIOS OpenBIOS, log CPU dan cache flush yang benar; (4) minimalkan bypass kartu memori sehingga hanya satu variabel berubah per eksperimen; (5) simpan hash emulator/BIOS/ROM dan log, bukan dump biner.
