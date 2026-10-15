# Log analisis dan handoff

Tanggal ringkasan: 2026-10-15

Catatan ini merangkum pekerjaan yang sudah dijalankan dan batasannya agar sesi/agen berikutnya dapat melanjutkan tanpa mengulang asumsi.

## Pemeriksaan file

- File yang dianalisis: Naruto - Shinobi no Sato no Jintori Gassen (Japan).bin.
- Ukuran file: 325.989.552 byte.
- Format yang terdeteksi: PS1 raw sector, stride 2352 byte, 138.601 sektor.
- Payload diekstrak sementara untuk membangun ISO dan membaca filesystem; file asli tidak diubah.
- Serial disc: SLPS-03553.
- CRC32: dfe1f8b3.
- SHA-256: 58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88.
- ISO memuat DATA.BIN, DATA2.BIN, DUMMY.BIN, SLPS_035.53, SYSTEM.CNF, XASECT.BIN; ukuran lengkap tercatat di docs/ROM_STRUCTURE.md.
- SYSTEM.CNF menunjuk ke SLPS_035.53; executable utama header-memuat base 0x80010000, PC 0x80011448, text size 0x5D800.

## Analisis kode statis

- Disassembly awal mengindikasikan instruksi MIPS R3000A di executable utama dan beberapa blok DATA.BIN.
- Tidak ditemukan teks aturan kunci sebagai string Shift-JIS literal biasa di file yang diekstrak pada pencarian awal. Struktur string/resource perlu dipetakan lebih lanjut.
- Struktur pemain yang digunakan beberapa rutin memiliki empat slot, stride 0xB4 byte, field Chakra pada offset +0x18.
- Setter Chakra membatasi rentang ke -9.999 sampai 99.999.
- Target konfigurasi 3.000 ditemukan dan dipakai oleh cabang pemeriksaan target pada jalur akhir pertandingan yang ditelusuri.
- Field kepemilikan petak diperiksa sebagai bagian bitfield, dengan empat bit teratas dipakai sebagai ID owner pada jalur yang diperiksa.
- Sejumlah alamat rutin dan flag akhir permainan masih merupakan label kerja; lihat docs/OVERLAY_MAP.md.

## Sumber gameplay sekunder yang diperiksa

- Transkripsi UI Story Mode dan kartu dari proyek terjemahan fan.
- Panduan Jepang yang menguraikan unlock dan opsi Party Mode.
- Materi promosi TV Tokyo.
- Ulasan gameplay Jepang tahun 2025.
- Data identitas disc dari GameGear Archive dan PSX Data Center.

Informasi eksternal digunakan untuk membuat hipotesis tentang makna kode, bukan menggantikan bukti runtime. Biaya 60/150 yang ditunjukkan oleh contoh UI tidak dinyatakan sebagai formula universal.

## Eksekusi runtime

- Dalam sesi terdahulu, emulator PS1 tidak ditemukan pada lingkungan eksekusi lokal.
- Upaya berikutnya untuk menjalankan terminal/Python ditolak oleh lingkungan, sehingga pemetaan overlay dan tes debugger tidak dapat dilanjutkan.
- GameGear Archive punya catatan pihak ketiga bahwa dump repack CHD boot pada Mednafen PSX HW selama uji otomatis 64 detik. Penelitian ini sendiri belum melaksanakan uji terkontrol terhadap barrier, battle, kartu, atau kondisi menang.

## Arahan untuk kelanjutan

1. Otorisasi tetap: pemilik memberi ChatGPT izin berkelanjutan untuk memperbarui repo Naruto secara otomatis sesuai kebutuhan penelitian. Izin ini hanya berlaku pada repo ini; Claude ditetapkan khusus untuk Tile Duel dan tidak boleh mengakses repo Naruto.
2. Jangan mengunggah file ROM/ISO, aset game, dump memori, atau save state ke repositori.
3. Mulai dari direktori resource DATA.BIN yang kini dipetakan; selidiki format PK02/BIN0/TPK0, consumer XASECT, dan relasi DATA2.BIN.
4. Uji aturan di emulator/debugger, lalu simpan log dan hasil secara teks/screenshot yang tidak mengandung aset berhak cipta yang tidak diperlukan.
5. Pelihara label confidence dan catat semua koreksi terhadap temuan lama.
6. Jangan pernah menyentuh repo Tile Duel dalam pekerjaan penelitian ini.

## Pembaruan byte-level dan klasifikasi resource — 2026-10-15

- Mengambil kembali ROM sumber dari Library ChatGPT ke folder kerja lokal; hash lengkap cocok dengan nilai yang sudah tercatat di docs/ROM_STRUCTURE.md. Pengguna juga menyimpan salinan di laptop.
- Mengekstrak enam file filesystem ISO ke salinan kerja lokal, tanpa mengubah ROM sumber dan tanpa mengunggah ROM/ISO/aset ke GitHub.
- Memverifikasi direktori di DATA.BIN: 0x44 byte bootstrap, 0x2F00 byte tabel, 1.504 entri × 8 byte; 1.500 entri aktif dan empat entri kosong pada indeks 1491–1494.
- Memverifikasi bahwa entri aktif tidak tumpang-tindih dan seluruh interval yang dibulatkan ke sektor berada dalam extent DATA.BIN. Total cakupan direktori 32.227 dari 32.234 sektor.
- Klasifikasi signature: PK02 921, TIM valid 246 (29 4-bit; 217 8-bit), NARUTOSceneV001 126, NARU lainnya 125, PSQ0 enam, PSQ1 dua, TXT2 satu, belum terklasifikasi 73.
- Pemeriksaan XASECT.BIN menemukan 86 pasangan 32-bit. Consumer di sekitar 0x80019468 menghitung indeks input >> 4, mengindeks pasangan dengan stride 8, lalu menggunakan field pertama sebagai offset aditif. Makna penuh field masih belum ditentukan.
- Semua analisis tersebut statis. Belum ada pengujian gameplay dengan debugger/emulator dan belum ada formula barrier, pendapatan, battle, atau efek kartu yang dinaikkan statusnya menjadi terkonfirmasi runtime.
- Detail lengkap: docs/RESOURCE_CATALOG.md dan HANDOFF_LANJUT.md.


## Arsip file ekstraksi di Library — 2026-10-15

- Menyimpan `DATA.BIN`, `DUMMY.BIN`, `SLPS_035.53`, `SYSTEM.CNF`, dan `XASECT.BIN` di Library pada folder `Naruto Research Files`.
- `DATA2.BIN` mentah gagal disimpan karena batas kapasitas Library; mengompresnya menjadi ZIP sekitar 42 MiB dan berhasil menyimpan `DATA2.BIN.zip`.
- File game tidak ditambahkan ke GitHub. Jangan menghapus item Library lain tanpa izin. Detail pemulihan ada di `HANDOFF_LANJUT.md`.
- Fokus riset selanjutnya tetap mencari aturan gameplay yang pasti: trace jalur transaksi Chakra, barrier/upgrade, income, battle, dan victory flags; bongkar format resource hanya bila jalur kode terbukti bergantung padanya.


## Pembaruan penelusuran aturan gameplay dan aturan sumber data — 2026-10-15

### Sumber file dan batas kuota

- Melanjutkan analisis dari file hasil ekstraksi yang sudah berada di Library; tidak membutuhkan dan tidak meminta upload ulang ROM 300 MB dari laptop.
- Hash SHA-256 yang cocok dengan catatan terdahulu: SLPS_035.53 = a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569; DATA.BIN = 69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822; XASECT.BIN = df257fbdabdb848f845466246abf4a36fdb6cf17815fc3a76ff7d7585d1953f0; DATA2.BIN hasil unzip = be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9. ZIP DATA2.BIN.zip = 67e7a372c6d02379d8cc715d15f3521c0914b8f17ee6e2f66a2bc32695367668.

### Jejak konfigurasi target Chakra

- Dalam executable utama, tabel 0x80057798 (file offset 0x47F98) menggunakan stride 0x54. Record yang diperiksa memuat (ID mentah, +0x04, +0x08, +0x0C): (0xA00,1500,3000,400), (0x10B01,2000,4000,400), (0x20C02,2000,4000,400), (0x81210,600,0,0), (0x31403,2500,5000,400), (0x40E04,2500,5000,400), (0x81211,600,0,0), (0x50F0F,2500,5000,400), (0x61106,3000,6000,400), (0x60809,3000,6000,400).
- Field +0x04 disalin ke global 0x80070C80 dan jalur inisialisasi meneruskannya ke setter Chakra; confidence tinggi bahwa ini nilai awal. Field +0x08 masuk lewat getter 0x80012A70 dan dipakai sebagai target pada cabang hasil dengan kondisi yang mencakup bit 0x200. Confidence tinggi untuk peran target, menengah–tinggi untuk pemetaan modul gameplay karena loader belum dipastikan runtime.
- Tabel kedua di 0x80064918 (file offset 0x55118, stride 0x30) menunjukkan nilai 1500/3000 pada sekurangnya 13 record awal nonnol yang diperiksa.
- Arti field +0x0C (400 atau 0) serta mapping raw ID ke nama stage/mode belum diketahui. Target 0 pada sebuah record tidak boleh diperlakukan sebagai kemenangan otomatis.
- Sumber terjemahan Story Act 01 menyebut target 3000; ini cocok dengan satu record, tetapi mapping ID satu-ke-satu belum terbukti.

### Peta kode dan koreksi

- DATA.BIN entry index 1 berada pada file offset 0x10BB000 dan berukuran 596.412 byte. Pemetaan sementara ke base RAM 0x800D0000 menghasilkan referensi internal konsisten, tetapi belum dikonfirmasi lewat breakpoint loader.
- Dalam peta statis tersebut, cabang sekitar 0x80111228, 0x801112CC, 0x801113B4, 0x801114F0, 0x80111588 dan 0x80112418 memeriksa kondisi target dan Chakra pemain sebelum mengubah pemenang/state hasil.
- Label terdahulu bahwa 0x800EC200 adalah pembanding target dan sekitar 0x800F70D0 aritmetika Chakra ditarik kembali karena identitas/base modul belum dibuktikan.
- Setter Chakra 0x8001387C menjepit ke [-9999, 99999]; nilai Chakra ada di +0x18 dalam struktur empat slot dengan stride 0xB4.

### Yang belum terkonfirmasi dan tugas berikutnya

- Belum ditemukan formula universal biaya barrier/upgrade, income, damage/durability battle, roulette, atau semua efek kartu. Angka UI 60 dan 150 bukan formula universal terkonfirmasi.
- Prioritas berikutnya adalah menelusuri call chain event ESTATE dan LVUP_ESTATE, transaksi Chakra, pendapatan, dan perubahan kepemilikan. Pemanggil setter yang perlu dipilah berdasarkan konteks termasuk 0x800D6D60, 0x800D6E04, 0x800D7AB0, 0x800D7B14, 0x800D8DE8, 0x801016E8, 0x80104790, 0x8010F554, 0x8012CD0C, 0x8012CD60, dan 0x8012D1E8; lokasi pemanggil saja tidak menetapkan makna transaksi.
- Tidak ada tes runtime debugger/emulator yang selesai. Semua klaim di atas tetap analisis statis.


## Penelusuran Chakra: setter, delta event, dan batas inferensi — 2026-10-15

- Pemeriksaan callsite `jal 0x1387C` pada resource yang sementara dipetakan ke `0x800D0000` menunjukkan beberapa panggilan hanya menyalin field Chakra yang sudah ada dari record runtime ke setter pemain aktif. Daftar itu mencakup `0x800D6D60`, `0x800D6E04`, `0x800D7AB0`, `0x800D7B14`, `0x800D8DE8`, `0x801016E8`; jadi daftar pemanggil setter tidak bisa dipakai sebagai daftar transaksi biaya.
- State machine sekitar `0x8012C600` mereset `+0xB44`, lalu membentuk `+0xB40 = +0xB30 + +0xB38`. Dalam state 7 (`+0xB2A == 7`), jalur `0x8012CD04–0x8012CD74` menggunakan `+0xB44` sebagai jumlah pending yang diterapkan bertahap ke Chakra pemain `+0xB2B` melalui getter/setter; pending dikurangi saat diproses dan field dibersihkan setelah selesai. Ini mekanisme perubahan Chakra bertahap, bukan bukti bahwa field itu khusus biaya barrier. Penulis `+0xB30/+0xB38` dan identitas aksi tetap belum ditemukan.
- Jalur di sekitar `0x8011C0D0` mempunyai cabang yang membalik tanda field nilai pemain dan menjepit nilai negatif terendah ke `-9999`, lalu memanggil setter Chakra. Pemicu dan identitas aturan belum dipastikan, sehingga belum diberi label sebagai efek kartu atau kondisi kekalahan.
- Jalur target kemenangan diperiksa lagi di `0x80111200–0x80111280`: getter kondisi menghasilkan bitmask; jika `bit 0x200` aktif, kode memanggil getter target `0x80012A70`, membaca nilai Chakra pemain dari field awal record pemain pada indeks yang dipilih, dan membandingkannya dengan target. `slt(current,target)` membuat jalur non-menang ketika `current < target`; ketika `current >= target`, kode menulis indeks pemain ke field pemenang dan mengubah state hasil. Confidence tinggi untuk arti perbandingan di dalam disassembly, tetapi identitas base modul tetap hasil pemetaan statis sementara.
- Tidak ada uji runtime dijalankan. Tidak ditemukan cukup bukti untuk mengklaim 60 Chakra sebagai harga semua barrier atau 150 Chakra sebagai harga semua upgrade. Prioritas berikutnya: telusuri penulis `+0xB44`, pemanggil event `ESTATE`/`LVUP_ESTATE`, pemeriksaan saldo, dan penulisan data petak untuk menghubungkan angka UI ke rumus/parameter.


## Keputusan emulator-first dan pemeriksaan environment — 2026-10-15

- Menetapkan penggunaan emulator/debugger sebagai jalur riset utama kedua setelah analisis statis. Sasaran: amati perubahan Chakra, field tile, event/state, damage, kepemilikan, dan kondisi pemenang secara langsung, lalu cocokkan dengan call chain.
- PCSX-Redux dipilih sebagai opsi utama karena ada dokumentasi resmi untuk debugger CPU, breakpoint memori, GDB server/watchpoints, command line load image, dan Lua breakpoint. Mednafen adalah alternatif dengan debugger PSX dasar serta breakpoint baca/tulis.
- Sumber rujukan: https://github.com/grumpycoders/pcsx-redux ; https://pcsx-redux.consoledev.net/Debugging/introduction/ ; https://pcsx-redux.consoledev.net/Debugging/gdb-server/ ; https://pcsx-redux.consoledev.net/cli_flags/ ; https://mednafen.github.io/documentation/debugger.html .
- File ROM diambil dari Library, bukan upload ulang laptop; SHA-256 diverifikasi ulang dan cocok: `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`. CUE eksperimen mengidentifikasi satu track MODE2/2352 sesuai mode byte sektor pertama. ROM asli tidak diubah.
- Kendala sesi 2026-10-15: tidak ada executable PS1 emulator yang ditemukan pada path runtime; DNS jaringan container gagal sehingga binary tidak dapat dipasang di sesi ini. Oleh sebab itu tidak ada game boot atau eksperimen runtime yang berhasil dilakukan. Catatan ini mencegah klaim palsu bahwa pengujian sudah berjalan.
- Protokol dan daftar eksperimen baru: [docs/EMULATOR_WORKFLOW.md](docs/EMULATOR_WORKFLOW.md), [docs/RUNTIME_TEST_PLAN.md](docs/RUNTIME_TEST_PLAN.md). Fokus uji awal: breakpoint executable utama di setter/getter Chakra; kemudian telusuri cost/ESTATE, LVUP_ESTATE, income, battle, dan target kemenangan setelah base overlay dikonfirmasi.


## Pemasangan PCSX-Redux dan uji launcher — 2026-10-15

- PCSX-Redux dipaketkan ke Naruto repo melalui workflow `.github/workflows/publish-pcsx-redux.yml` sebagai Release asset, bukan Git object. Release: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15. Ukuran asset 65.747.557 byte; SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`, cocok dengan digest yang diterbitkan package source.
- GitHub Actions run 38692549397 sukses: unduh, validasi hash dan size, best-effort launch smoke test via Xvfb, workflow artifact (retention 90 hari) dan release assets terunggah.
- AppImage dijalankan di environment melalui Xvfb. GUI memang muncul dan teridentifikasi game serial SLPS03553 pada daftar/halaman emulator, tetapi memunculkan dialog “No BIOS loaded, emulation halted”. Tidak ada boot game, tidak ada input gameplay atau runtime game state yang diamati.
- Untuk tahap berikutnya, workflow `.github/workflows/build-openbios.yml` membangun OpenBIOS open-source dari repository upstream PCSX-Redux pinned full source commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`. Workflow awal gagal karena ref commit singkat tidak diterima checkout action; pinned source diperbaiki menjadi full SHA. Run perbaikan #38693323975 harus diverifikasi. OpenBIOS adalah BIOS replacement open-source, bukan Sony retail BIOS.
- ROM didapat dari Library dengan SHA-256 yang cocok, tanpa meminta upload ulang dari laptop. Binary emulator tetap sebagai Release asset terpisah untuk menjaga Git history kecil.


## Uji PCSX-Redux dengan OpenBIOS — 2026-10-15

- OpenBIOS berhasil dikompilasi pada GitHub Actions run `38693358323` dari source PCSX-Redux pinned commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`; workflow merilis asset `openbios.bin`, `openbios.elf`, dan checksum/source provenance.
- Varian default `openbios.bin` berukuran 524.288 byte, SHA-256 `713ea2aed58606282b3ff5e91d77f8c5892ea36f5adcd279d2c7dd26604a625d`. Varian ELF debug SHA-256 `d0d4cc73c9546e1e6af86d38ec894f5a6c81090ccdf97b1a3a39885c56af7bfc`. Keduanya cocok dengan `OPENBIOS-SHA256SUMS` pada artifact yang diunduh dan diverifikasi.
- Launch PCSX-Redux menggunakan `-bios openbios.bin -interpreter -debugger -iso game.cue -run` tidak lagi menampilkan “No BIOS loaded”, tetapi frame yang terekam menunjukkan bentuk geometris besar/gelap dan tidak memberi bukti yang cukup bahwa game mencapai menu/title. Jangan tandai boot game berhasil.
- Workflow run `38693918169` sedang menyiapkan dua variant OpenBIOS: normal shell/menu dan `BOOT_MODE=fast` agar CD boot dicoba langsung. Setelah selesai, ambil asset via release atau GitHub Actions artifact, validasi checksum, lalu ulangi tes boot.
- AppImage emulator tetap sebagai Release asset terpisah dengan hash `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`. Repo tidak menyimpan ROM atau BIOS retail.
