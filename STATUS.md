# Status penelitian

Terakhir dirangkum: 2026-10-15

## Ringkasan

**Status: analisis statis awal dengan jejak konfigurasi target Chakra yang lebih kuat; belum lengkap dan belum tervalidasi melalui debugging gameplay.**

**Sumber wajib:** kuota internet pengguna sangat terbatas. Jangan meminta upload ROM/ISO sekitar 300 MB dan jangan mengandalkan ROM laptop. Gunakan file hasil ekstraksi di Library pada /Naruto Research Files/. Jika tidak dapat diakses, laporkan kendala alih-alih meminta upload ulang.

Pemeriksaan sebelumnya mengekstrak struktur ISO dari dump PS1 raw-sector, membaca SYSTEM.CNF, mengidentifikasi executable utama, melakukan inspeksi/disassembly awal MIPS, dan menemukan beberapa struktur serta jalur kode. Namun, pemetaan overlay belum lengkap, rumus gameplay belum seluruhnya terhubung ke semua pemanggil, dan sesi emulator/debugger terkontrol belum dijalankan.

## Temuan yang didukung langsung oleh kode/data ROM

1. Executable boot yang dirujuk SYSTEM.CNF adalah SLPS_035.53.
2. Header executable mencatat alamat muat 0x80010000, PC 0x80011448, dan text size 0x5D800.
3. Struktur pemain yang diakses beberapa getter/setter memiliki empat slot; stride struktur 0xB4 byte dan nilai Chakra pada offset +0x18.
4. Setter Chakra yang diperiksa membatasi nilai tersimpan pada rentang -9.999 sampai 99.999. Ini bukan kondisi menang/kalah.
5. Jalur kode membandingkan Chakra pemain dengan target konfigurasi dari getter 0x80012A70; jika kondisi target terkait (bit 0x200) aktif, Chakra yang mencapai/melewati target dapat menetapkan pemain sebagai pemenang. Tabel konfigurasi utama memuat pasangan awal/target 1.500/3.000, 2.000/4.000, 2.500/5.000, 3.000/6.000 serta dua record awal 600/0 yang kondisi pemilihannya belum dipetakan. Jadi 3.000 bukan target universal.
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
- Lanjutkan reverse-engineering format resource yang kini terindeks melalui direktori di DATA.BIN; format PK02/BIN0/TPK0, NARUTOSceneV001, PSQ0/PSQ1, serta tujuan penuh XASECT.BIN masih belum diketahui.
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

## Pembaruan hasil pemeriksaan lokal — 2026-10-15

Pemeriksaan byte-level terhadap salinan kerja ROM mengonfirmasi temuan baru berikut. Hasil ini **statis**; belum ada tes gameplay terinstrumentasi.

- SHA-256 ROM cocok dengan catatan yang sudah ada: `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`.
- Di executable utama, offset file `0x46098` (alamat runtime `0x80055898`) berisi pasangan little-endian `0xD4, 0x2F44`: LBN 212 dan panjang 12.100 byte, yang menunjuk ke awal `DATA.BIN`.
- Awal `DATA.BIN` terdiri dari bootstrap sepanjang `0x44) byte diikuti direktori `0x2F00) byte: 1.504 entri × 8 byte, paling kuat ditafsirkan sebagai pasangan `(LBN, byte_length)`.
- 1.500 entri tidak kosong dan 4 kosong (indeks 1491–1494). Semua interval sektor entri aktif berada dalam rentang `DATA.BIN` dan tidak tumpang-tindih; direktori mencakup 32.227 dari 32.234 sektor file.
- Klasifikasi signature awal atas 1.500 resource aktif: 921 `PK02`, 246 struktur TIM valid, 126 `NARUTOSceneV001`, 125 signature lain berawalan `NARU`, 6 `PSQ0`, 2 `PSQ1`, 1 `TXT2`, dan 73 belum diklasifikasikan. Pemindaian longgar mendeteksi 264 kandidat magic TIM; 18 gagal validasi struktur dan tidak dihitung sebagai TIM valid.
- `XASECT.BIN` berisi hitungan 86 diikuti 86 pasangan 32-bit. Konsumen di sekitar `0x80019468` mengindeks pasangan dengan `input >> 4) dan memakai field pertama sebagai offset aditif. Arti semantik lengkap field dan kaitan field kedua dengan stream/media masih belum pasti.

Lihat [docs/RESOURCE_CATALOG.md](docs/RESOURCE_CATALOG.md) untuk hitungan, batas inferensi, hash file hasil ekstraksi, serta langkah analisis berikutnya. Handoff lintas-chat ada di [HANDOFF_LANJUT.md](HANDOFF_LANJUT.md).


## Persistensi file untuk analisis lintas chat

File ekstraksi disimpan di Library ChatGPT pada folder `Naruto Research Files`; `DATA2.BIN` tersedia sebagai ZIP terkompresi. Baca tabel lokasi pada `HANDOFF_LANJUT.md` dan verifikasi hash sesudah pemulihan sebelum melanjutkan analisis.


## Pembaruan analisis aturan gameplay — 2026-10-15

- Tabel konfigurasi executable 0x80057798 ber-stride 0x54; tabel kedua 0x80064918 ber-stride 0x30. Field +0x04 dipakai sebagai Chakra awal, field +0x08 sebagai target pada cabang kemenangan, sementara makna field +0x0C belum ditemukan.
- Nilai teramati pada tabel pertama mencakup 1500/3000, 2000/4000, 2500/5000, 3000/6000; ada dua record 600/0 yang tidak boleh ditafsirkan sebagai kemenangan instan.
- Label lama 0x800EC200 sebagai pembanding target Chakra dan 0x800F70D0 sebagai aritmetika Chakra dicabut karena base/identitas modul belum diverifikasi.
- File Library yang digunakan pada sesi ini: SLPS_035.53, DATA.BIN, XASECT.BIN, DATA2.BIN hasil unzip. Hash DATA2.BIN hasil unzip cocok: be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9.
- Belum ada tes runtime. Prioritas berikutnya: transaksi biaya bangun/upgrade, income, perubahan kepemilikan dan transaksi battle melalui pemanggil setter Chakra dan label event ESTATE/LVUP_ESTATE.


## Trace aturan Chakra — tambahan 2026-10-15

- Kode pembanding target di resource gameplay (base hipotesis 0x800D0000) memastikan syarat cabang target adalah Chakra saat ini >= target konfigurasi bila bit kondisi 0x200 aktif. Target dibaca lewat getter 0x80012A70. Alamat resource masih statis sementara karena loader belum diverifikasi runtime.
- Pemanggilan setter Chakra 0x8001387C banyak berupa sinkronisasi salinan record. State machine sementara pada resource DATA.BIN membentuk +0xB40 dari +0xB30 + +0xB38, lalu pada state +0xB2A == 7 memproses jumlah pending +0xB44 bertahap ke Chakra pemain +0xB2B. Sumber operand dan semantik event belum ditemukan; ini bukan bukti biaya barrier.
- Karena sumber nilai transaksi belum terhubung, biaya build/upgrade universal masih belum terbukti. Angka 60 dan 150 hanya tercatat pada contoh UI tertentu dalam transkripsi komunitas.


## Status emulator/runtime — 2026-10-15

- Emulator/debugger kini ditetapkan sebagai jalur riset utama untuk memvalidasi aturan, bersama reverse-engineering statis; bukan sekadar alternatif opsional.
- Diprioritaskan PCSX-Redux karena dokumentasi resminya mendukung CPU debugger, breakpoint dan GDB server; Mednafen dapat digunakan untuk cek silang. Rujukan dan protokol uji ada di [docs/EMULATOR_WORKFLOW.md](docs/EMULATOR_WORKFLOW.md).
- Pada awal sesi executable emulator tidak tersedia dan DNS container gagal. PCSX-Redux kemudian diunduh dari GitHub Actions artifact/release, diverifikasi, dan antarmukanya berhasil dijalankan lewat Xvfb. Namun, belum ada bukti bahwa game mencapai menu/title atau bahwa gameplay sudah diuji.
- ROM di Library berhasil dimaterialisasikan dan SHA-256 cocok; tidak dibutuhkan upload ulang dari laptop pengguna.


## Emulator tersimpan di repo — 2026-10-15

- PCSX-Redux Linux x86_64 AppImage diunggah sebagai Release asset di [research-emulator-pcsx-redux-2026-10-15](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15), bukan Git history. Ukuran 65.747.557 byte; SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c. GitHub Actions run 38692549397 sukses mendownload dan memverifikasi binary.
- AppImage dapat diluncurkan di Xvfb, tetapi layar menunjukkan “No BIOS loaded, emulation halted”; belum ada boot game ataupun uji gameplay.
- Workflow build OpenBIOS open-source ada di .github/workflows/build-openbios.yml. Run #38693358323 berhasil membangun dan merilis varian default (shell/menu); run #38693918169 sedang membangun varian default plus `BOOT_MODE=fast`. OpenBIOS bukan BIOS retail Sony.
- Jangan meminta upload ulang ROM. ROM hash diverifikasi dari Library; CUE dibuat untuk BIN raw-sector MODE2/2352.


## Update OpenBIOS — 2026-10-15

- Run [#38693358323](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693358323) berhasil membangun OpenBIOS dari source upstream PCSX-Redux pada commit 0c3572c3db75f97542001e453ae80ba8c3f8acba dan melampirkan asset ke release.
- Varian OpenBIOS default: `openbios.bin` 524.288 byte, SHA-256 `713ea2aed58606282b3ff5e91d77f8c5892ea36f5adcd279d2c7dd26604a625d`; ELF debug `openbios.elf` SHA-256 `d0d4cc73c9546e1e6af86d38ec894f5a6c81090ccdf97b1a3a39885c56af7bfc`. Checksum lengkap di release asset `OPENBIOS-SHA256SUMS`.
- Uji lokal dengan BIOS ini tidak lagi menampilkan pesan “No BIOS loaded”, tetapi frame yang terekam berupa bentuk geometris/gelap tanpa menu atau title game yang dapat dikonfirmasi. Ini belum membuktikan boot Naruto.
- [Run #38693918169](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693918169) sedang membangun varian `BOOT_MODE=fast` yang melewati shell BIOS dan mencoba boot CD secara langsung, bersama varian shell/menu normal. Periksa hasil workflow dan hash sebelum menggunakan asset tersebut.
