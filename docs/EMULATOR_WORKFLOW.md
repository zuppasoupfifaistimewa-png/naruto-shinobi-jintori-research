## TUJUAN UTAMA YANG TIDAK BOLEH TERLEWAT — tamatkan Story Mode dan pastikan aturan main (2026-10-19)

Jangan berhenti setelah emulator berhasil boot, menu terbuka, atau dialog selesai. **Tujuan akhir riset adalah memainkan Story Mode sampai layar akhir/tamat yang meyakinkan, lalu menyusun aturan main yang pasti berdasarkan pengamatan langsung dalam game dan bukti yang dapat diaudit.**

Setelah emulator stabil:
1. Lanjutkan dari checkpoint valid bila tersedia; dialog Story Mode dilewati dengan **START**, bukan Circle. Circle hanya dipakai untuk menu yang sudah terbukti memerlukannya. Setiap aksi dikirim satu per satu dan diikuti pemeriksaan screenshot.
2. Identifikasi kapan gameplay aktif dimulai, tujuan misi, kendali karakter, pergerakan, aksi/serangan/pertahanan, giliran bila berlaku, biaya aksi dan penggunaan Chakra, perebutan wilayah, barrier/penghalang, kartu, roulette, efek tiap mekanik, syarat menang/kalah, pergantian stage, serta variasi stage.
3. Mainkan setiap tahap Story Mode sampai tamat. Catat urutan tahap, keadaan awal, input, perubahan layar/status/Chakra/wilayah, hasil tiap aksi, dan bukti screenshot sebelum/sesudah. Jangan menebak jika layar hitam, crash, transisi ambigu, atau hasil input tidak jelas; rancang eksperimen pembeda satu variabel pada satu waktu.
4. Simpan tabel aturan dengan tiga label yang tidak boleh dicampur:
   - **TERVERIFIKASI** — terlihat langsung dari gameplay atau eksperimen terkontrol yang berulang, dengan screenshot/log dan kondisi uji tercatat.
   - **HIPOTESIS** — penjelasan yang masuk akal tetapi bukti belum cukup atau masih ada alternatif.
   - **BELUM DIUJI / BELUM DIKETAHUI** — mekanik atau kondisi belum berhasil dipicu/diamati.
   Tambahkan sumber bukti dan langkah pengujian yang diperlukan untuk setiap aturan.
5. Jangan menyatakan aturan sebagai pasti hanya berdasarkan nama fungsi, analisis kode, readback controller, status workflow, atau sumber luar tanpa konfirmasi gameplay. Jangan menyatakan Story Mode tamat tanpa bukti kuat dari layar akhir/ending.
6. Setelah eksperimen penting, perbarui STATUS.md, HANDOFF_LANJUT.md, HANDOFF_CHAT_BARU_2026-10-19.md, ANALYSIS_LOG.md, dan docs/RUNTIME_TEST_PLAN.md agar sesi berikutnya langsung melanjutkan dari hasil terakhir tanpa mengulang run berhasil.
7. Setiap tulisan Jepang yang diperlihatkan ke pengguna harus langsung diikuti terjemahan Bahasa Indonesia di sebelahnya dalam tanda kurung. Utamakan screenshot dari hasil eksperimen kita sendiri, bukan gambar web.

---


## Status optimasi runner — crash awal dan guard restore checkpoint (2026-10-19)

Timeout job saat ini 360 menit; SoftGPU tetap digunakan dan timeout proses emulator internal adalah 20.400 detik (5 jam 40 menit). Jalur bermain menonaktifkan raw GPU dump dan sampling GDB/RSP untuk mengurangi overhead. Namun dua run sebelumnya (`#39205262049` dan `#39205556772`) mengalami segmentation fault, masing-masing exit 139 sebelum frame 5.999; keduanya belum menghasilkan screenshot progres atau savestate valid. Run pertama sempat salah berstatus workflow success, lalu pemeriksaan exit code diperbaiki agar kegagalan emulator membuat step gagal.

Penyebab crash belum dipastikan. Panggilan getDumpFrames tanpa GPU dump sudah dihapus tetapi run berikutnya tetap crash. Commit terbaru `88d5cfa8833ef39e286431f5e8bedf2584485804` menambahkan pemeriksaan `io.open` sebelum memanggil Support.File.open/loadSaveState untuk menghindari loader native menerima file checkpoint yang tidak ada.

Run terbaru untuk menguji guard tersebut: [#39205699071](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39205699071). Pada pemeriksaan terakhir proses emulator masih berjalan; jangan klaim berhasil sampai screenshot dan log setelah run diperiksa. Save state baru boleh dipindahkan jika sanitizer mencatat PASS; artefak #12165850239 dan #12165635987 tidak berisi savestate dan tidak boleh dipakai sebagai checkpoint resume.

# Alur penelitian runtime dengan emulator PS1

Tanggal dibuat: 2026-10-15

## Prinsip

Emulator/debugger merupakan jalur penelitian utama bersama analisis statis bila tujuan kita menetapkan aturan permainan. Analisis byte/dekompilasi menghasilkan hipotesis; emulator dipakai untuk memeriksa state nyata sebelum/sesudah aksi, mengamati jalur kode yang benar-benar dieksekusi, dan menguji apakah sebuah aturan punya pengecualian menurut mode/skenario.

Jangan pernah menyebut aturan “terbukti runtime” kecuali ada log uji yang bisa diulang. ROM/ISO, executable game, retail Sony BIOS tersendiri, raw RAM/VRAM/GPU dump, dan aset game privat tetap tidak boleh diunggah. Kebijakan terbaru mengizinkan memory-card/game save dan savestate yang telah disanitasi melalui private artifact, cache, atau repositori private; sanitizer wajib membuang BIOS tertanam dan log harus menunjukkan PASS sebelum transfer. Lihat README.md dan bagian revisi save/checkpoint di catatan handoff terbaru. OpenBIOS adalah pengganti BIOS open-source yang terpisah dan boleh disimpan bersama checksum serta atribusi lisensinya. Catatan teks, hash, breakpoint, register relevan, dan hasil terukur boleh disimpan.

## Status pemasangan emulator dalam sesi ini

- ROM dibuka dari Library ChatGPT (bukan diunggah ulang dari laptop) dan SHA-256 diverifikasi: `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`.
- GitHub Actions mengunduh PCSX-Redux Linux x86_64 AppImage dari paket tidak resmi Package Forge dan memverifikasi ukuran 65.747.557 byte serta SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`. Aset berjangka panjang ada di [release research emulator](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15). Repo ini privat; akses download bergantung pada izin akun/connector.
- Run yang berhasil: [GitHub Actions #38692549397](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38692549397). Smoke-test hanya membuktikan AppImage dapat dieksekusi dan GUI tidak langsung keluar; ini **bukan** bukti game berhasil boot.
- Screenshot GUI awal menunjukkan pesan “No BIOS loaded, emulation halted”. OpenBIOS shell/default kemudian berhasil dibangun dan ditambahkan ke release melalui [Actions run #38693358323](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693358323). Asset `openbios.bin` berukuran 524.288 byte; SHA-256 `713ea2aed58606282b3ff5e91d77f8c5892ea36f5adcd279d2c7dd26604a625d`; `openbios.elf` SHA-256 `d0d4cc73c9546e1e6af86d38ec894f5a6c81090ccdf97b1a3a39885c56af7bfc`. Uji lokal dengan OpenBIOS menghilangkan dialog BIOS tak tersedia, tetapi layar yang terekam tidak menunjukkan menu/game yang dapat dikenali; belum terbukti bahwa Naruto boot. Workflow berikutnya sedang membangun dua varian: shell/menu default dan `BOOT_MODE=fast` untuk mencoba boot CD langsung. Run [#38693918169](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693918169) berhasil membangun dan mengunggah varian `BOOT_MODE=fast`; hash `openbios.bin` fastboot: `25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d`, hash `openbios.elf`: `2c8d36e2179841935a1d1331777380502cdb22528d086c99c6388cdcfa54b8aa`. Uji lokal memakai varian ini, tetapi layar tetap hitam setelah sekitar 12 detik dan log tidak memberi bukti bahwa title/menu game muncul. Jadi OpenBIOS tersedia, tetapi boot game masih **belum terkonfirmasi**.
- File disc merupakan raw-sector 2352 byte dan mode byte sektor pertama adalah 2. CUE pendamping yang sesuai menggunakan satu track `MODE2/2352`; gunakan nama BIN lokal yang sama persis dalam CUE.
- Jangan meminta upload ulang ROM ~326 MB. Gunakan berkas yang sudah disimpan di Library dan asset emulator dari release repo.

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
2. Boot disc BIN/CUE. Prioritaskan OpenBIOS open-source dari release penelitian; OpenBIOS bukan BIOS retail Sony dan kompatibilitas tiap game tidak dijamin. Varian `openbios.bin` yang sudah ada adalah build normal shell/menu; varian `BOOT_MODE=fast` sedang dipersiapkan agar dapat mencoba boot CD otomatis. Jangan mengunduh atau mengunggah BIOS retail dari sumber tak tepercaya.
3. Matikan Dynarec dan aktifkan debugger karena fitur debugging CPU tertentu memerlukan interpreter.
4. Jika memakai GDB: aktifkan GDB server di Configuration > Emulation; aktifkan debugger juga. Server default di dokumentasi PCSX-Redux adalah localhost:3333. Jalankan GDB multiarch/MIPS yang sesuai, lalu `target remote localhost:3333`.
5. Untuk penelitian kode tanpa simbol, pasang breakpoint pada alamat executable utama yang sudah terpetakan. Jangan pasang breakpoint overlay dengan alamat RAM hipotesis sampai loader/base overlay dikonfirmasi.

Bila emulator sudah terbuka, contoh command-line resmi untuk memuat image adalah:
```text
pcsx-redux -bios "path/to/openbios.bin" -interpreter -debugger -gdb -iso "path/to/game.cue" -run
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

Setiap uji memakai state awal yang sama atau mencatat tepat bagaimana state awal diperoleh. Save kartu memori dan savestate yang telah disanitasi boleh disimpan/ditransfer di artifact, cache, atau repositori private. Gunakan salinan memory card eksperimen dan jangan menimpa save asli; jangan gunakan savestate bersamaan dengan memory card asli yang tidak sinkron.

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

Simpan log atau ringkasan debugger sebagai teks. Save kartu memori dan savestate tersanitasi boleh disimpan di repositori private sesuai kebijakan baru. ROM/ISO, BIOS retail tersendiri, serta raw RAM/VRAM/GPU dumps tetap dilarang.

## Kriteria menaikkan status keyakinan

- **Statis saja:** rumus/branch terlihat pada executable/resource, namun belum diamati saat gameplay.
- **Runtime teramati:** perubahan direkam saat aksi tertentu dilakukan di emulator; bila satu kali saja, tulis bahwa hasil belum direplikasi.
- **Runtime tereplikasi:** hasil sama muncul pada sedikitnya dua pengulangan dengan state awal terkontrol.
- **Aturan mapan:** call chain statis cocok dengan state runtime dan variasi skenario/cabang penting telah diuji.

## Catatan boot terbaru — 2026-10-16

Status boot tetap belum berhasil diverifikasi secara visual. Gunakan catatan ini sebagai sumber terbaru untuk troubleshooting:

- Jalur disc normal mengenali label disc `SLPS-03553` serta membaca `SYSTEM.CNF;1`, tetapi berhenti saat payload executable sedang dimuat sebelum log `EXEC:PC0(80011448)`.
- `SLPS_035.53` berukuran 385.024 byte; payload text 382.976 byte (`0x5D800` atau 187 sektor).
- Chunk 32 sektor dan 8 sektor gagal menyelesaikan bacaan payload. Varian 8 sektor mencatat `[CHUNK8] before idx=0 ... bytes=16384` tanpa log selesai untuk pemanggilan itu.
- Varian diagnostik satu sektor dibangun lewat [Actions #38697240018](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38697240018). Pembacaan satu sektor (2.048 byte) mulai menunjukkan progres dalam uji singkat, tetapi belum ada bukti seluruh payload selesai atau menu Naruto tampil.
- Jalur manual yang memasukkan executable ke RAM pernah mencapai `EXEC:PC0(80011448)`, `Execute !`, dan `CD_init`, tetapi tampilan hitam. Pastikan `flushCache` dipanggil dan urutan init CD-ROM tidak dilewati. Jalur itu masih belum menghasilkan boot game terverifikasi.
- Breakpoint berikutnya tampak menunggu di init kartu memori (`buInit`). Bypass sementara melewati tunggu tetapi masih hitam.
- Perintah kontroler `0x43` (Set Config Mode) terlihat berulang. Source PCSX-Redux hanya meneruskan perintah DualShock seperti ini di mode Analog, sedangkan tipe Digital mencatat `Unknown command for pad: 43`. Sumber: https://github.com/grumpycoders/pcsx-redux/blob/db9bc8af44e3c77424127b573c17f9583ee2ab95/src/core/pad.cc. **Ini hipotesis yang belum diuji:** ubah Port 1 ke Analog/DualShock, ulangi boot dan lihat apakah perintah 0x43 diproses.
- ZIP alternatif dari pengguna, `PCSX-Redux-9c6f98a0-linux-x86_64.zip` (90.912.361 byte), belum diperiksa atau dijalankan karena runtime shell/file tool gagal pada sesi 2026-10-16. Jangan mengklaim build ini berfungsi; periksa kembali saat akses filesystem pulih.

**Kriteria sukses tetap ketat:** log mencapai entry game, layar menunjukkan title/menu Naruto yang dikenali, lalu kontrol merespons. Jangan menganggap layar hitam atau entry executable saja sebagai boot sukses. Jangan mengunggah ROM/ISO, EXE game, Sony BIOS retail tersendiri, atau raw RAM/VRAM/GPU dump. Savestate tersanitasi dan memory-card save boleh dipindahkan melalui penyimpanan private sesuai kebijakan baru.
