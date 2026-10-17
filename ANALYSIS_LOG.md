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


## OpenBIOS fast-CD boot attempt — 2026-10-15

- Build workflow [#38693918169](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693918169) sukses membuat shell/menu dan fast boot variants. `openbios.bin` adalah `BOOT_MODE=fast`, yang melewati shell dan mencoba boot disc.
- Hash fast boot `openbios.bin`: `25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d`; ELF: `2c8d36e2179841935a1d1331777380502cdb22528d086c99c6388cdcfa54b8aa`. Checksum dari artifact cocok untuk kedua berkas fastboot; release berisi juga varian shell/menu.
- Pengujian lokal dengan AppImage, fastboot OpenBIOS, interpreter/debugger dan CUE disc dilakukan sekitar 12 detik. BIOS-missing dialog tidak muncul, tetapi layar tetap hitam; tidak ada title atau menu yang bisa dipastikan. Ini **belum merupakan boot game yang terverifikasi**.
- Next: periksa CUE/raw-sector layout dan log/PC state; uji CD-ROM boot dengan debug step atau media header yang dikenal sebagai kontrol. Jangan unggah ROM ke repo, jangan meminta pengguna mengirim ulang ROM, dan jangan klaim rule gameplay runtime sampai ada bukti langsung.

## Diagnostik runtime lanjutan: sektor, init kartu memori, dan pad — 2026-10-16

### Pembacaan payload EXE
- Boot CD normal berhasil membaca file konfigurasi, tetapi `loadExe` tersangkut saat membaca payload utama `SLPS_035.53`. Payload sepanjang `0x5D800` byte = 382.976 byte = 187 sektor.
- Percobaan loop 32 sektor dan 8 sektor tidak menyelesaikan masalah. Varian 8 sektor hanya menghasilkan `[CHUNK8] before idx=0 ... bytes=16384` tanpa `after`, sehingga permintaan 16 KB tidak selesai dalam jendela pengamatan.
- Varian diagnostik satu sektor dibangun/diterbitkan dalam [Actions #38697240018](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38697240018). Runtime menunjukkan read 2.048 byte mulai berjalan dan ada progres setidaknya sampai sekitar sektor kesembilan dalam pengamatan singkat, tetapi belum ada bukti full payload read atau entry game pada jalur disc normal.

### Jalur manual/injeksi EXE
- Injeksi payload ke alamat yang ditetapkan header membuat debugger mencapai `EXEC:PC0(80011448)`, `Execute !`, dan `CD_init`; layar tetap hitam. Pastikan `flushCache` dan urutan init CD-ROM benar sebelum mengulang.
- Breakpoint berikutnya menunjukkan startup menunggu dalam inisialisasi kartu memori (`buInit`) karena status kartu tidak berubah. Bypass eksperimental dapat melewati penantian, tetapi belum menghasilkan layar title/menu; jangan menyebutnya boot berhasil.

### Petunjuk protokol kontroler
- Log berulang menunjukkan perintah pad `0x43` (Set Config Mode). Source PCSX-Redux upstream mengidentifikasi command ini di jalur DualShock/analog; bila tipe controller emulator Digital, kode log menampilkan `Unknown command for pad: 43`. Sumber: https://github.com/grumpycoders/pcsx-redux/blob/db9bc8af44e3c77424127b573c17f9583ee2ab95/src/core/pad.cc.
- Hipotesis selanjutnya: ganti Port 1 ke Analog/DualShock dan ulangi boot sebelum melakukan patch game. Belum ada hasil uji setelah perubahan tipe pad, jadi kausalitas belum terbukti.

### Build alternatif yang diunggah pengguna
- File `PCSX-Redux-9c6f98a0-linux-x86_64.zip`, ukuran 90.912.361 byte, disediakan pengguna pada 2026-10-16. Lingkungan eksekusi shell/file gagal saat inspeksi, sehingga isi paket, hash dan kelayakan menjalankan ROM belum diverifikasi. Lakukan verifikasi terlebih dahulu; jangan menaruh file biner besar ke Git history atau release tanpa alasan yang teruji.

### Syarat bukti
- Status sekarang: *executable mulai berjalan dalam jalur manual*, bukan game terkonfirmasi boot. Bukti yang dibutuhkan: log entry yang valid, title/menu yang dikenali, dan input responsif. Sesudah itu baru validasi aturan gameplay dengan state awal terkontrol.


## Percobaan setelah ZIP emulator tersimpan di Library — 2026-10-16

- Melalui Files berhasil mematerialisasi ZIP emulator (90.912.361 byte), ROM sumber (325.989.552 byte), dan CUE (113 byte) ke `/mnt/data/naruto-runtime/`.
- Pemeriksaan lokal gagal sebelum program dijalankan: `container.exec` memberikan `ClientError` untuk listing/file checks dan bahkan `echo runtime-check`; Python di lingkungan analisis dan jalur Python alternatif juga gagal dengan `ClientError`.
- Akibatnya, belum ada daftar isi ZIP, hash ZIP, hasil ekstraksi, versi PCSX-Redux, log run, atau bukti boot baru. Jangan mengartikan kegagalan tool sebagai kerusakan ZIP atau kegagalan emulator. Tidak ada tes runtime baru yang berhasil dilakukan.
- Tindakan saat runtime pulih: verifikasi integritas dan isi ZIP, ekstrak binary ke direktori sementara, cek versi/dependensi, lalu ulangi boot ROM dengan OpenBIOS dan Port 1 Analog/DualShock sebagai hipotesis terpisah. Sukses harus dibuktikan dengan layar title/menu Naruto dan respons input.


## Refinement of controller `0x43` diagnostic hypothesis — 2026-10-16

The exact upstream PCSX-Redux source commit used for the research-kit AppImage was inspected: [`src/core/pad.cc` at `0c3572c3db75f97542001e453ae80ba8c3f8acba`](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/pad.cc).

- `PadType` defines `Digital = 0` and `Analog = 1`. The serialized setting is named `DeviceType`, with `Digital` as its default.
- When the first received command byte is not the normal read command `0x42`, the pad dispatches the DualShock command handler only when `m_type == PadType::Analog`. Otherwise it logs `Unknown command for pad: %02X`. Thus the existing `Unknown command for pad: 43` log is consistent with Port 1 being configured as a Digital controller.
- Important distinction: the Lua method `setAnalogMode(bool)` writes `m_analogMode`; it does **not** change `m_type` or the serialized `DeviceType` controller type. Calling that Lua method alone is not a valid test of the current hypothesis.
- The GUI's `Controller Type` selector updates `SettingDeviceType` and resets/remaps the pad. The next controlled experiment should set Port 1 `Controller Type` to `Analog` through **Configuration → Controls**, confirm that the pad is connected, then repeat the same CD-boot attempt with all other variables unchanged.
- Compare logs before and after. If the `Unknown command for pad: 43` messages disappear, record that protocol-level effect; if the game still hangs or remains black, the controller mismatch was not a sufficient explanation for the boot failure. Do not infer game boot from that log change alone.

Evidence class: static inspection of the emulator source. **This is not yet a runtime result**: this session could not run the emulator because local execution/file tools returned `ClientError`. The contents and hash of the user-provided alternate ZIP remain unverified.

## OpenBIOS source-level CD-read stall hypothesis — 2026-10-16

### Source trace

Pinned source chain:
- PCSX-Redux AppImage root commit: https://github.com/grumpycoders/pcsx-redux/commit/0c3572c3db75f97542001e453ae80ba8c3f8acba, dated 2026-10-01.
- Its src/mips submodule points to OpenBIOS/Nugget commit https://github.com/pcsx-redux/nugget/commit/d93840921b5ad7ed515e95b0e414f1b1e2038b1a.

Relevant source:
- openbios/kernel/psxexe.c: loadExe() reads the 2,048-byte header, then calls syscall_read(fd, text_addr, text_size) once; it does not check the result count before closing and flushing cache.
- openbios/cdrom/filesystem.c: dev_cd_read() rejects a size or offset not aligned to 0x800 bytes and converts the request into 2,048-byte sectors before calling cdromBlockReading().
- openbios/cdrom/helpers.c: cdromBlockReading() polls seek/read startup with bounded cycle counters, but after starting a read it waits for the DNE completion event while checking error/end events; that final wait has no overall timeout. If completion is never delivered, it may wait indefinitely.

The known executable payload is 0x5D800 = 382,976 bytes = 187 sectors; its request size and file offset satisfy the 0x800 alignment guard. The normal-path stall during payload loading is consistent with a CD-ROM read/event completion issue because the log previously showed SYSTEM.CNF read but not EXEC:PC0(80011448). This remains a root-cause hypothesis until a reproducible runtime trace identifies the exact event/state.

### Controller configuration refined

PCSX-Redux source declares PadType::Digital=0 and PadType::Analog=1 and serializes the emulated console pad protocol to DeviceType (default Digital). Upstream tests/core/pad-config.cc confirms DeviceType: 1 means Analog; PadType: 2 is the keyboard host-input source. These settings are distinct. Toggling the keyboard Analog mode binding or Lua setAnalogMode(true) is not equivalent to setting DeviceType.

- Source used by release: https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/pad.cc
- Upstream config fixture: https://github.com/grumpycoders/pcsx-redux/blob/e7ced7b681296ace22f7847f7bb3c9a206315571/tests/core/pad-config.cc

### Emulator package comparison

The user-provided filename PCSX-Redux-9c6f98a0-linux-x86_64.zip maps by its prefix to upstream root commit https://github.com/grumpycoders/pcsx-redux/commit/9c6f98a0ed0581635f9123147e382c248e0f5ddc, a merge dated 2026-09-28. The research AppImage is pinned to a later root commit dated 2026-10-01. Since ZIP contents could not be inspected in this session, do not claim the uploaded archive actually contains that exact build; the filename is evidence only.

### Next controlled runtime test

1. When shell runtime is available, inspect the ZIP without executing it: unzip -t, list files, SHA-256, architecture and dependencies. Prefer the pinned research AppImage if the ZIP offers no newer/testable functionality.
2. Run a clean isolated test with explicit paths: -bios openbios-chunked.bin -iso naruto-shinobi-jintori.cue -run -interpreter -debugger -stdout -lua_stdout -logfile boot-analog.log.
3. Set Port 1 protocol to Analog (DeviceType: 1), host input to keyboard (PadType: 2), and Connected=true. Compare Unknown command for pad: 43 logs; independently verify the title/menu and input response.
4. The executable payload is 187 sectors. Use a longer observation window and log every per-sector read. Determine whether progress completes, stops at a reproducible sector, or waits on a specific CD event. Early progress is not a completed read.
5. Only start gameplay tests after the title/menu is visible and controls respond. No new runtime test occurred in this session because shell and Python tools returned ClientError; this is an environment blocker, not proof that the ZIP is corrupt or that the game cannot run.


## PCSX-Redux ZIP extraction record — 2026-10-16

### Archive validation and extraction

- Materialized the user Library file `PCSX-Redux-9c6f98a0-linux-x86_64.zip` (90,912,361 bytes) to the working container.
- Source ZIP SHA-256: `7e4c9378524ebfa35068944ba4aa9e3ebf7462678bcae33b3e7ae7c57dd99849`.
- `unzip -t` passed with no errors; archive contained exactly one entry: `PCSX-Redux-HEAD-x86_64.AppImage`, 91,474,424 bytes.
- Extracted AppImage SHA-256: `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`. A second materialization from Library compared byte-identical with the extracted local file.
- Embedded `usr/share/pcsx-redux/resources/version.json`: version `9c6f98a0`, build ID 335, changeset `9c6f98a0ed0581635f9123147e382c248e0f5ddc`, build timestamp 2026-09-28 19:56:29 UTC, channel `dev`.
- The extracted AppImage runtime responded to `--appimage-version`, and the embedded squashfs filesystem could be extracted without FUSE. Running the inner emulator failed due requirements `GLIBC_2.42` and `GLIBC_2.43`; this host provides glibc 2.41. Direct AppImage mounting also failed because no suitable `fusermount`/FUSE device is available.
- The source ZIP was replaced in Library by the AppImage output to avoid storing two nearly identical large files at Library quota. The source hash is recorded here. The Library item retains stale ZIP MIME metadata despite the new AppImage bytes.
- Persistent Library manifest: `/Naruto Research Files/PCSX-Redux-EXTRACTION-MANIFEST.md`.
- New Git documentation records details in `docs/PCSX_REDUX_PACKAGE.md`. The actual 91 MB binary was not added to Git history because the current GitHub connector has no binary Release-asset upload action; a distinct 65,747,557-byte AppImage already exists on the research Release (SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`).
- This work verifies the ZIP and extracted AppImage only. It is **not** a runtime verification of Naruto boot, controls, Story Mode, or the ROM's validity.


## Preferred build for GLIBC 2.41 host — 2026-10-16

### Candidate and compatibility evidence

The best candidate located for the glibc 2.41 research host is the x86_64 `AnyLinux` AppImage built from source changeset `0c3572c3db75f97542001e453ae80ba8c3f8acba` on 2026-10-01. It is attached to the research release and the public packager's release. Size 65,747,557 bytes; SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`.

Sources:
- [Packager README](https://github.com/pkgforge-dev/PCSX-Redux-AppImage-Enhanced): states that AnyLinux AppImage bundles dependencies for old/musl Linux distributions and does not require FUSE.
- [x86_64 GitHub Actions run](https://github.com/pkgforge-dev/PCSX-Redux-AppImage-Enhanced/actions/runs/36872881656), 2026-10-01: successful; the log explicitly says `quick-sharun --simple-test` returned “Test went OK.” The packager embeds cross-libc-dlopen and uruntime.
- The repo's earlier smoke-test notes reported GUI launch under Xvfb with a “no BIOS configured” message. This was not a game boot test.

This is a stronger candidate than the Library's `9c6f98a0` AppImage whose inner binary needs GLIBC_2.42/2.43. However, generic smoke tests and portable packaging do not establish game compatibility or stability. In this turn, container.exec and Python returned ServerError even for basic sanity commands, so no fresh test against the Naruto BIN/CUE was performed. Do not claim title/menu, input, stable gameplay, or Story Mode completion.

Next test when runtime access recovers: obtain the exact candidate by release, verify its SHA; use OpenBIOS chunked with CUE, a clean profile, logs, Port 1 `DeviceType: 1` plus keyboard `PadType: 2`, and connected=true. Confirm title/menu and responsive input, then examine the 187-sector EXE read, repeat boot tests, and only afterwards begin Story Mode.


## Current Library package — AnyLinux artifact ZIP (2026-10-16)

The candidate AnyLinux artifact ZIP was downloaded from the packager's GitHub Actions artifact ID 11170447493 and saved in Library as `/Naruto Research Files/PCSX-Redux-0c3572c3d-anylinux-x86_64-artifact.zip`. Actions-reported ZIP digest: `f6c27070b565cbc0554f1093c1374a16aee2b8635c72ef7b141f9ff7bd857ed0`; reported size 65,673,524 bytes. Its standalone AppImage SHA-256 is known from Release metadata: `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`. This is the preferred candidate for glibc 2.41. The previous 91 MB `9c6f98a0` AppImage and its stale Library manifest were replaced/removed; their hashes remain recorded in `docs/PCSX_REDUX_PACKAGE.md`.

The Actions log confirms a generic `quick-sharun --simple-test` passed. That does not test the ROM. No full Naruto boot, input, runtime stability, or Story Mode result is available. Attempts to run simple local commands now return ServerError, so do not claim an end-to-end test was performed.


## Controlled Analog-port boot probe configured — 2026-10-17

### What changed

- Runner workflow commit: [6bd261a0599f192579f8c091ddcb6d28a4042ec7](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/6bd261a0599f192579f8c091ddcb6d28a4042ec7).
- The workflow now passes a Lua setup to each emulator build before execution:

  ```lua
  PCSX.settings.pads[1].DeviceType = 'Analog'
  PCSX.settings.pads[1].Connected = true
  PCSX.SIO0.slots[1].pads[1].map()
  print("PAD_SETUP=port1 analog device connected and remapped")
  ```

- This matches the upstream PCSX-Redux test fixture at [tests/pcsxrunner/rumble.cc](https://github.com/grumpycoders/pcsx-redux/blob/6b9df482d7b77b9ae218d9c48c1ce1a43c265206/tests/pcsxrunner/rumble.cc). Its comment says safe mode starts Port 1 digital and that the controller type is cached at map() time.
- The A/B workflow continues to use the exact same verified ROM SHA-256 `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`, the same temporary normalized CUE, OpenBIOS, interpreter and 90-second limit for both the AnyLinux and upstream HEAD builds. It now includes the Lua setup marker in the selected logs.

### How to interpret the pending log

- A visible `PAD_SETUP=port1 analog device connected and remapped` marker is needed to confirm the Lua setup ran.
- Compare the presence of `Unknown command for pad: 43` against the baseline from Actions run [#38971848277](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38971848277), where both builds emitted the warning.
- Even if the warning disappears, it proves only that the emulator now accepts the configuration command. It does **not** prove the title/menu is rendered or that input works in the game.
- The resulting run log has not yet been captured into this research log. Do not infer success merely from the workflow commit or a passing CI job.

### Next diagnostic gate

First retrieve the run output and confirm the Lua marker and `0x43` result. If the warning is gone but the frame remains black, treat controller configuration as a solved protocol mismatch but **not** a sufficient explanation for the boot/rendering failure. Then run a separate GUI-under-Xvfb test with the same ROM and Analog-port setup, capture the emulator window locally on the ephemeral runner, and report only derived pixel/screen metrics (do not upload ROM, BIOS, EXE, save-state, RAM dump, or game screenshots to the repository). Confirm title/menu recognition and input response before starting gameplay-rule tests.


## Workflow YAML correction — 2026-10-17

- The initial Analog-port workflow edit [6bd261a](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/6bd261a0599f192579f8c091ddcb6d28a4042ec7) accidentally left the Lua heredoc body without YAML block indentation. Do not treat that revision as a valid completed test.
- The indentation was corrected in final workflow commit [0439c1b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/0439c1bbf51d3c1be234150d6bee80c5b812ff1e). The current file was re-fetched and visually checked: heredoc contents and its closing LUA delimiter are now indented at the YAML run-block level, which YAML removes before the shell executes the script.
- No runtime claim is made from these edits. The next evidence must still come from logs of a run using the corrected commit, including the PAD_SETUP marker and presence/absence of the pad 0x43 warning.


## Runtime result: Port 1 Analog probe — 2026-10-17

Runner test [#38973267415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973267415), job `boot-private-rom`, completed successfully using corrected workflow commit `0439c1bbf51d3c1be234150d6bee80c5b812ff1e`.

- Both AnyLinux and upstream HEAD recorded `PAD_SETUP=port1 analog device connected and remapped`, then loaded OpenBIOS, recognized `SLPS-03553`, completed `[CHUNK1] done chunks=187`, and reached `EXEC:PC0(80011448)` / `Execute !`.
- Unlike the baseline [#38971848277](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38971848277), neither build logged `Unknown command for pad: 43` after the explicit Analog DeviceType + Connected + remap setup. Each build was stopped at the 90-second cap (`PROCESS_EXIT=124`) rather than crashing.
- Conclusion: **confirmed emulator protocol-level effect** — configuring Port 1 as Analog removes the observed `0x43` warning while preserving the executable-entry marker. This does not establish that the game title/menu rendered or that buttons worked in-game. The controller setup warning is now separated from the still-open black-screen/boot/rendering problem.

## GUI rendering probe added — 2026-10-17

- Current runner workflow commit: [85c08d9](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85c08d9ea255dc400c0771361abc95817a0a7ba6). New Actions run [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) was observed queued immediately after commit; its final outcome has not yet been recorded here.
- After the same A/B headless run, the workflow launches AnyLinux in a separate Xvfb GUI session with the same verified ROM, temporary CUE, OpenBIOS and Analog setup. It captures frames at 10s and 20s, prints only image size/mean/stddev/color-count and short Japanese/English OCR output, and logs boot/controller markers. Temporary frames and GUI logs are added to the cleanup list, not uploaded as artifacts.
- GUI result must be checked separately. Non-black pixels or OCR text alone are suggestive only; accept boot only if the frame/text supports Naruto title/menu recognition and a later controlled input probe demonstrates response. If still blank, pursue CD event/init and GPU/rendering causes separately.


## GUI probe result and next trace — 2026-10-17

Runner [Actions #38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) completed successfully, including cleanup. The GUI probe ran AnyLinux with the same verified ROM, temporary normalized CUE, OpenBIOS and Analog Port 1 setup under Xvfb. Two desktop captures at 10s and 20s both reported `1280x800`, `mean=0`, `stddev=0`, `colors=1`, and empty Japanese/English OCR output. This confirms the **captured desktop was entirely black** at both times. The selected GUI log lines included BIOS/Disc/PAD_SETUP but did not include `EXEC:PC0` or `Execute !` within the 35-second GUI observation window; headless tests still reached those markers. No screenshot/artifact was uploaded; frames and logs were deleted by cleanup.

Next experiment: a separate lean workflow [naruto-cpu-trace.yml](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/blob/main/.github/workflows/naruto-cpu-trace.yml) adds a listener for the upstream-tested `GPU::Vsync` event and prints the guest PC/RA/SP every 30 frames, up to 600 frames, using the same private ROM with explicit Analog Port 1. Current run [#38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045) was `in_progress` immediately after commit; obtain its final log and interpret it cautiously. If no VSync callbacks occur, distinguish a stalled emulation/hardware timing path from a CPU loop; if PCs are recorded, map recurring addresses against the executable/temporary overlay assumptions. Do not claim rendered title/menu until independently proven.


## CPU trace attempt 1 — inconclusive — 2026-10-17

The runner job [Actions #38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045) exited with code 139 (segmentation fault) about 12 seconds after starting the headless emulator. It had read the disc label and `SYSTEM.CNF`/`BOOT`, but no `PC_TRACE` sample or executable-entry marker was captured. The instrumented build added a Lua VSync listener that removed itself inside its callback at frame 600, so instrumentation is a confounder. This result does not prove the ROM is invalid or that the game code itself crashed.

A retry was committed as [9419800](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/941980021c16dee3e779f6cc1066dad70b187ad4). It combines the pad setup and tracing code into a single `-exec` block and leaves the VSync listener installed until timeout. Check [Actions #38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739) and require real `PC_TRACE frame=...` rows before interpreting any PC values. If that retry fails, simplify to a counter-only VSync callback before reading registers.


### CPU trace attempt 2: failure was Lua script construction — 2026-10-17

Run [#38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739) exited 134. The exact stdout reason is `[string "cmdline:"]:4: unexpected symbol near '\\'`, followed by `Error loading lua string` and `terminate called without an active exception`. This was caused by shell concatenation `printf '%s\\n%s'` embedding a literal backslash-n between the two Lua chunks instead of a line break. The Lua parser rejected the instrumentation before any PC sample; this is not a ROM failure.

Corrected runner workflow commit: [7b8ce73](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/7b8ce731378e0115f616b7ff78874f5d17375e80). It now constructs pad configuration and VSync tracing in a single heredoc, so source lines are separated normally; the listener stays installed through the timeout. Current retry: [Actions #38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869). Check final job logs for `PAD_SETUP`, `PC_TRACE=listener installed`, and actual `PC_TRACE frame=` lines. If Lua parses but segfaults, strip down to a simple VSync counter callback before any register read.


### CPU trace attempt 3 — VSync samples recorded; process later segfaulted — 2026-10-17

Runner [Actions #38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869) ran the corrected single-heredoc Lua script. It printed `PAD_SETUP` and `PC_TRACE=listener installed`, then produced `PC_TRACE frame=` rows from frame 30 through at least frame 780. Sampled PCs frequently included BIOS addresses `BFC0574C`, `BFC05784`, `BFC03C6C`, plus occasional `000000B0` and `00002998`; RA/SP were also captured. The separate emulator logfile recorded `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, and `Execute !`. The process nevertheless ended with `TRACE_PROCESS_EXIT=139` (segmentation fault) before the 35-second cap and the last output row was incomplete. Because the instrumentation reads `PCSX.getRegisters()` inside the VSync callback, that access/formatting is still a possible confounder; do not infer that the game itself caused the fault or that the PC samples prove a stable gameplay loop.

Next isolating run: [Actions #38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602), workflow commit [85d3e4f](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85d3e4ff31732b7788d67e447ea9df136dcb84f5), uses a counter-only `GPU::Vsync` listener with no CPU-register reads and no self-removal. If it survives until timeout and reports increasing VSync counters, callback plumbing is sound and the register read/format path is implicated. If it still crashes, isolate event registration/callback itself or leave Lua tracing aside and use built-in debugger/logs.


### Counter-only trace result — 2026-10-17

Run [Actions #38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) ended with `TRACE_PROCESS_EXIT=124`, the expected 35-second timeout, not a crash. The counter-only `GPU::Vsync` callback logged increasing counts through `VSYNC_TRACE frame=2040`; the same stdout also recorded `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, and `Execute !`. This demonstrates the event callback itself can remain active stably while the emulator completes headless boot. The prior exit 139 is therefore consistent with the register-read/formatting instrumentation as a confounder, though not yet proven conclusively.

The next test [Actions #38974903834](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974903834), workflow commit [ff0faa5](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/ff0faa598c6e19295229b450c6f9d42c83e590fb), keeps the stable counter and only samples PC every 120 VSync callbacks. It acquires `PCSX.getRegisters()` before event registration (following upstream test style), reads only `regs.pc`, and prints decimal values instead of using `%08X`. If it completes to timeout and emits PC lines without crashing, decode the decimal addresses and compare when they cross from BIOS `0xBFC...` to executable entry space `0x80011448`. If it still exits 139, abandon live register access in the callback and use an upstream-supported CPU execution instrumentation approach.


### Built-in trace API mismatch and emulator correction — 2026-10-17

Workflow run [#38975154606](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975154606) used the pinned AnyLinux package based on upstream PCSX-Redux commit `0c3572c3d`. The process aborted immediately with Lua error `attempt to index field 'CPU' (a nil value)` when accessing `PCSX.CPU.Trace`; it logged no VSync counters. I verified that `src/core/pcsxffi.lua` at ref `0c3572c3d` does not expose `PCSX.CPU.Trace`, although a newer upstream source ref does. This was a build/API mismatch, not a ROM failure.

Corrective runner workflow commit [c994afc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/c994afccfa62efcc01751a7c2b39d89b109d936a) now downloads the user-provided/private-release upstream `PCSX-Redux-HEAD-x86_64.AppImage` and verifies SHA-256 `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`; this build was previously verified to reach `EXEC:PC0` on Ubuntu 26.04. It uses the new `PCSX.CPU.Trace` interface for a bounded frame 1620–1680 capture, then prints only the last 80 records, and deletes all media/trace files during runner cleanup. New test [Actions #38975223698](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975223698) has started; read its final logs before drawing conclusions.


### Packaged emulator also lacks built-in CPU tracing — 2026-10-17 correction

Runner [Actions #38975223698](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975223698) was intended to use the private upstream HEAD AppImage, but it aborted with the same `attempt to index field 'CPU' (a nil value)` message before a VSync sample. The uploaded HEAD binary also predates the `PCSX.CPU.Trace` Lua binding; do not confuse this with a game or ROM failure. Thus **neither packaged build currently available in the research release provides the required trace API**.

Current workflow commit [8304b7d](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8304b7dd56be13673e83e84bb738458eca0cfc2d) instead checks out upstream PCSX-Redux source at pinned commit `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`, verifies `src/core/pcsxffi.lua` exposes `Trace = {`, and builds the native CLI binary using upstream's published builder container. Run [Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) was actively building at the time of this note. Only after build success can the frame-1620-to-1680 bounded built-in instruction trace be interpreted; build failures are infrastructure evidence, not ROM behavior.


### Interpret the first GUI captures against boot timing — 2026-10-17

The 10-second and 20-second all-black frames from GUI run [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) were taken before the headless boot's executable-load point. The stable counter-only test [#38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) reached its VSync count 1620 shortly before the separate log emitted `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, and `Execute !` (the entire 35-second test later reached frame 2040). So the 10s/20s black frames cannot by themselves establish a permanent black-screen failure; the GUI test must observe well beyond the ~27–30s point and ideally capture the emulator window rather than the X root. The earlier 35s GUI window may also be borderline due to UI overhead.

Current source-trace runner [#38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) is still building a pinned upstream source revision so the actual built-in CPU trace API can be tested without live register reads. The result must be checked before analysis proceeds.


### Extended GUI observation launched — 2026-10-17

Runner workflow commit [aea4c20](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aea4c20accfd6d1c5089a226f52a2c4183d2d9a8) extends the GUI phase from 35s to 100s and measures frames at 30s, 60s and 90s, still using temporary local captures which cleanup deletes. Current run [#38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679) has both private asset retrieval steps passing and is in the A/B + GUI step; output has not completed yet. This should distinguish early BIOS-only black captures from a persistent blank frame after the expected executable entry point.

Source build/trace workflow [#38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) is also still in `Build pinned upstream PCSX-Redux with CPU trace support`; no claim is made about build success until the step completes. It uses pinned source commit `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` and the official builder image.


## End-to-end private-ROM run and test-harness corrections — 2026-10-17

Reviewed [Actions #38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679) and [CPU trace Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756).

Confirmed by log: read-only secret was present; normalized release assets were retrieved; ROM byte count and SHA-256 matched; the temporary CUE passed structural validation; OpenBIOS identified disc `SLPS-03553`; `SYSTEM.CNF` selected `SLPS_035.53`; all 187 executable chunks completed; and PCSX-Redux printed `EXEC:PC0(80011448)` / `Execute !`. The Analog Port 1 setup was applied to both compared builds and neither emitted `Unknown command for pad: 43`. Both headless processes reached their 90-second caps; the executable-entry marker is not a title-screen or playable-input result.

The 30/60/90-second GUI probe produced root-window metrics of `mean=0`, `stddev=0`, `colors=1` and no OCR text. Inspecting the workflow exposed a test-harness flaw: it invoked `import -window root`, so those metrics described the Xvfb root background, not necessarily PCSX-Redux's own window. Do not use these frames to diagnose guest rendering. Corrective workflow commit [8829933](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8829933b3b6815dce694ebe6d46cd2a1f0fee9f0) now searches for a visible PCSX-Redux window, captures that window only, reports the window tree if it cannot find one, and does not fall back to the root.

The first source-build trace attempt [#38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) successfully compiled the pinned upstream source but the host executable failed before emulation because `libcapstone.so.5` was missing. No trace callbacks ran. Corrective commit [d965dcc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/d965dcc864c73818e67d6a1e5f9edc19d4a3a17c) adds upstream-documented `libcapstone-dev` and a preflight `ldd` check. Retests [#39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) and [#39000276365](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365) were launched on 2026-10-17; inspect final logs before marking either fix successful.

The runner repo remains free of game media and trace assets: the workflows download private files only to the ephemeral runner, then remove them during cleanup. No gameplay formula was newly confirmed in this run.


## Corrected GUI-window capture — result and interpretation (2026-10-17)

Runner Actions #39000276365 completed successfully after commit 8829933. The capture code found a visible PCSX-Redux window at each 30/60/90-second capture point. This fixes the prior root-window measurement flaw. The actual window frames were still uniformly black by ImageMagick statistics (1280x800, mean 0, standard deviation 0, one color); OCR in Japanese/English returned no text.

Do not conclude that the game framebuffer is black after entry: the GUI probe's own log did not emit [CHUNK1] done chunks=187, EXEC:PC0(80011448), or Execute !. Those markers were seen in the headless A/B probes in the same run. Current result is a GUI-vs-headless discrepancy: headless execution reaches the game executable, while GUI-mode boot remains black and lacks the executable-entry markers within the observation window. Next debug question is why the UI-mode boot path differs (window/context/emulator run state/OpenBIOS progress), not yet which game render routine fails. No frame or private game data was uploaded as an artifact.
