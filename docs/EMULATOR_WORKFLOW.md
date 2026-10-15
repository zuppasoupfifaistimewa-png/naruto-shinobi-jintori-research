# Alur penelitian runtime dengan emulator PS1

Tanggal dibuat: 2026-10-15

## Prinsip

Emulator/debugger merupakan jalur penelitian utama bersama analisis statis bila tujuan kita menetapkan aturan permainan. Analisis byte/dekompilasi menghasilkan hipotesis; emulator dipakai untuk memeriksa state nyata sebelum/sesudah aksi, mengamati jalur kode yang benar-benar dieksekusi, dan menguji apakah sebuah aturan punya pengecualian menurut mode/skenario.

Jangan pernah menyebut aturan “terbukti runtime” kecuali ada log uji yang bisa diulang. Jangan menyalin ROM, BIOS, memory card, save state, screen capture berisi aset besar, atau dump RAM ke GitHub. Catatan teks, hash, breakpoint, register relevan, dan hasil terukur boleh disimpan.

## Status ketersediaan emulator dalam sesi ini

- ROM dibuka dari Library ChatGPT (bukan diunggah ulang dari laptop) dan SHA-256 terverifikasi: `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`.
- File sumber adalah raw-sector 2352 byte; mode byte sektor pertama adalah 2. Untuk emulator yang meminta CUE, gunakan 1 track `MODE2/2352` dengan file BIN yang sudah dimiliki.
- Pemeriksaan environment pada 2026-10-15 tidak menemukan executable PCSX-Redux, Mednafen, DuckStation, PCSX2, atau RetroArch. Xvfb tersedia, tetapi akses jaringan container gagal pada resolusi DNS sehingga binary emulator tidak dapat dipasang dari rilis di sesi ini.
- Karena itu, pada tanggal ini belum ada game boot atau uji gameplay runtime yang benar-benar dijalankan. Ini blocker environment yang eksplisit, bukan alasan untuk mengubah hasil statis menjadi klaim runtime. Jangan meminta pengguna upload ulang ROM ~326 MB; file sudah tersedia di Library untuk analisis dan pengguna juga menyimpan salinan lokal.

## Emulator yang diprioritaskan

### 1. PCSX-Redux — pilihan utama untuk debugging

Alasan: dibuat untuk riset/reverse-engineering PS1, menyediakan CPU debugger, memory editor, breakpoint, dan GDB server yang dapat digunakan dengan GDB/Ghidra. Dokumentasi resmi:
- [Repo dan unduhan PCSX-Redux](https://github.com/grumpycoders/pcsx-redux)
- [Debugging overview](https://pcsx-redux.consoledev.net/Debugging/introduction/)
- [GDB server dan watchpoints](https://pcsx-redux.consoledev.net/Debugging/gdb-server/)
- [Command-line flags](https://pcsx-redux.consoledev.net/cli_flags/)
- [Lua breakpoints](https://pcsx-redux.consoledev.net/Lua/breakpoints/)

Konfigurasi debugging CPU:
1. Gunakan build resmi Windows x64 atau Linux x86-64 yang sesuai platform.
2. Boot disc BIN/CUE. BIOS harus dikonfigurasi sesuai kemampuan emulator; bila kompatibilitas boot bermasalah, coba BIOS konsol yang dimiliki secara sah atau opsi OpenBIOS yang disediakan/dikonfigurasi emulator. Jangan mengunduh atau mengunggah BIOS dari sumber tak tepercaya.
3. Matikan Dynarec dan aktifkan debugger karena fitur debugging CPU tertentu memerlukan interpreter.
4. Jika memakai GDB: aktifkan GDB server di Configuration > Emulation; aktifkan debugger juga. Server default di dokumentasi PCSX-Redux adalah localhost:3333. Jalankan GDB multiarch/MIPS yang sesuai, lalu `target remote localhost:3333`.
5. Untuk penelitian kode tanpa simbol, pasang breakpoint pada alamat executable utama yang sudah terpetakan. Jangan pasang breakpoint overlay dengan alamat RAM hipotesis sampai loader/base overlay dikonfirmasi.

Bila emulator sudah terbuka, contoh command-line resmi untuk memuat image adalah:
```text
pcsx-redux -interpreter -debugger -gdb -iso "path/to/game.cue" -run
```
Nama biner/argumen build dapat berbeda sedikit; verifikasi dengan `-help` pada build yang dipakai.

### 2. Mednafen — alternatif untuk cek silang

Mednafen PSX juga memiliki debugger dasar, termasuk breakpoint eksekusi dan breakpoint baca/tulis memori:
- [Dokumentasi debugger Mednafen](https://mednafen.github.io/documentation/debugger.html)
- [Dokumentasi modul PlayStation](https://mednafen.github.io/documentation/psx.html)

Gunakan Mednafen untuk cek silang boot dan observasi sederhana bila PCSX-Redux tidak berjalan. Karena fitur debugger antarmodul tidak sama, catat build, pengaturan, dan batas debugger yang dipakai.

## Berkas BIN/CUE

Jika BIN yang dimiliki adalah dump raw-sector 2352 byte yang sama, file CUE pendamping harus berada di folder yang sama dengan BIN dan merujuk nama file BIN secara tepat. Contoh untuk nama ROM penelitian:
```cue
FILE "Naruto - Shinobi no Sato no Jintori Gassen (Japan).bin" BINARY
  TRACK 01 MODE2/2352
    INDEX 01 00:00:00
```
Mode 2 berasal dari mode byte sector pertama yang diperiksa. Jangan menulis ulang atau memodifikasi file BIN sumber. Hash harus tetap cocok dengan `docs/ROM_STRUCTURE.md`.

## Urutan uji aturan gameplay

Setiap uji memakai state awal yang sama atau mencatat tepat bagaimana state awal diperoleh. Simpan save state di luar repo; untuk mencegah kerusakan save, lakukan tes pada salinan memory card atau jangan gunakan save state bersamaan dengan memory card game asli.

### RT-001 — boot dan kalibrasi address

- Catat versi/build emulator, setting CPU (interpreter, debugger), jenis BIOS, SHA-256 ROM, dan apakah game benar-benar masuk ke menu.
- Pastikan breakpoint executable utama bekerja, misalnya entry PC dari header `0x80011448`.
- Verifikasi setter/getter Chakra di executable utama (`0x8001387C`, `0x800138EC`) sebelum mengasumsikan address state RAM.
- Catat nilai argumen register saat breakpoint, PC, return address, dan nilai RAM yang relevan. Signature alamat overlay harus disertai identitas resource dan base yang sudah diamati, bukan hanya hasil dugaan.

### RT-002 — biaya bangun barrier (ESTATE)

1. Dapatkan state saat giliran pemain berada di petak kosong; catat pemain aktif, Chakra, koordinat/ID petak, serta tampilan biaya di UI.
2. Pasang breakpoint pada setter Chakra dan pada jalur kode/event yang benar-benar dipanggil setelah memilih ESTATE.
3. Rekam instruksi pemanggil, register argumen, nilai sebelum/sesudah setter, dan field petak yang berubah.
4. Ulangi pada saldo cukup dan tidak cukup, serta tipe petak atau skenario lain. Pisahkan angka UI dari nilai yang dipakai sebagai operand transaksi.
5. Kesimpulan formula memerlukan asal nilai harga, pemeriksaan saldo, delta Chakra, dan mutasi petak tersambung dalam call chain.

### RT-003 — upgrade barrier (LVUP_ESTATE)

- Ulangi RT-002 untuk barrier level 1 ke 2 dan, jika mungkin, tingkat berikutnya.
- Catat Chakra, level, nilai barrier, durability, owner, dan tile ID sebelum/sesudah aksi.
- Jangan menyamakan perubahan nilai/durability dengan biaya; setiap field dibuktikan melalui alamat dan instruksi penulisnya.

### RT-004 — pendapatan

- Gunakan state yang dapat diulang; bandingkan jalur mendarat di tile kosong, tile sendiri, dan tile lawan.
- Rekam Chakra pemain sebelum/sesudah mendarat, akhir giliran, dan fase event bila ada.
- Ulangi pada level barrier berbeda untuk menentukan apakah pendapatan tergantung level, nilai petak, tipe, bonus, atau kondisi skenario.

### RT-005 — battle, durability, dan pengambilalihan

- Rekam state petak dan pemain sebelum battle, setiap perubahan Chakra, statistik pertarungan, durability, serta owner setelah menang/kalah.
- Bandingkan kondisi tanpa barrier, barrier level berbeda, dan jutsu yang berbeda bila dapat dilakukan secara reproduktif.
- Pisahkan biaya mulai battle, biaya jutsu, damage, penghancuran barrier, hadiah, dan transfer owner.

### RT-006 — kondisi menang Chakra

- Identifikasi record konfigurasi yang dipilih dari tabel 0x80057798/0x80064918.
- Untuk konfigurasi dengan target yang diketahui, amati keadaan tepat di bawah target dan ketika target tercapai/dilewati.
- Catat flag kondisi yang aktif, Chakra semua pemain, target getter, hasil/ID pemenang, dan PC saat hasil berubah.
- Ulangi dengan opsi mode berbeda. Record bertarget 0 jangan ditafsirkan sebagai kemenangan seketika sebelum cabang pilihannya diketahui.

## Format bukti yang wajib

Untuk setiap hasil, tulis:
- Test ID; versi emulator; jenis BIOS; hash ROM; mode dan stage.
- State awal yang tepat, aksi input, nilai Chakra dan field petak sebelum/sesudah.
- Breakpoint PC; identitas executable/resource + offset file + base RAM; register relevan; call chain sejauh yang terpetakan.
- Hasil yang diamati, pengulangan yang berhasil/gagal, confidence, serta hal yang belum diketahui.

Simpan log atau ringkasan debugger sebagai teks. Jangan menyimpan save state, ROM, BIOS, atau dump memori ke repo.

## Kriteria menaikkan status keyakinan

- **Statis saja:** rumus/branch terlihat pada executable/resource, namun belum diamati saat gameplay.
- **Runtime teramati:** perubahan direkam saat aksi tertentu dilakukan di emulator; bila satu kali saja, tulis bahwa hasil belum direplikasi.
- **Runtime tereplikasi:** hasil sama muncul pada sedikitnya dua pengulangan dengan state awal terkontrol.
- **Aturan mapan:** call chain statis cocok dengan state runtime dan variasi skenario/cabang penting telah diuji.
