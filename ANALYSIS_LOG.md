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
