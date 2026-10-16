# HANDOFF_LANJUT — Naruto Shinobi Jintori Research

Terakhir diperbarui: 2026-10-15  
Repo: [zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research)  
Branch utama: `main`

## Aturan proyek dan izin kerja

- ChatGPT hanya bekerja pada repo Naruto ini. Pemilik memberi izin berkelanjutan agar ChatGPT boleh membaca, menganalisis, menambah, memperbarui, mengorganisasi, commit, dan push dokumentasi penelitian yang diperlukan tanpa meminta izin ulang untuk setiap perubahan wajar dalam ruang lingkup riset Naruto.
- Izin itu tidak berlaku untuk repo lain. ChatGPT **dilarang mengakses** `zuppasoupfifaistimewa-png/tileduel`.
- Claude hanya ditugaskan ke Tile Duel dan **tidak diizinkan mengakses** repo Naruto.
- Jangan unggah ROM asli, ISO, aset game, dump memori, save state, atau artefak game besar sebagai bagian dari dokumentasi rutin. Repo menyimpan laporan, hash, skrip analisis yang aman bila diperlukan, dan hasil teks.
- Bedakan temuan statis dari pengujian runtime. Jangan menyatakan formula game terkonfirmasi runtime kecuali tesnya benar-benar dijalankan dan direkam.
- Catat perubahan penelitian di `ANALYSIS_LOG.md` dan perbarui dokumen handoff ini saat kesimpulan/next steps berubah.

## ROM sumber dan pemulihan

ROM sumber:
- Nama Library: `Naruto - Shinobi no Sato no Jintori Gassen (Japan).bin`
- Ukuran: 325.989.552 byte
- CRC32: `dfe1f8b3`
- SHA-256: `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`
- Karena kuota internet pengguna sangat terbatas, jangan menjadikan ROM di laptop sebagai sumber kerja dan jangan meminta upload ulang ROM sekitar 300 MB. ROM asli hanya tercatat untuk identitas/hash; sumber byte-level utama untuk riset lanjutan adalah file hasil ekstraksi yang sudah tersimpan di Library. Jika komponen yang diperlukan tidak dapat diakses di Library, dokumentasikan keterbatasan dan cari jalur riset alternatif tanpa membebani kuota.

Hash file hasil ekstraksi dicatat di `docs/ROM_STRUCTURE.md` dan `docs/RESOURCE_CATALOG.md`. Folder hasil ekstraksi pada filesystem kerja tidak dijamin tersedia di chat baru; pulihkan file dari Library terlebih dahulu. Jangan menyarankan ekstraksi ulang dari laptop/upload ulang ROM sebagai langkah standar karena kuota pengguna sangat terbatas.

## Urutan baca saat membuka chat baru

1. Baca file ini.
2. Baca `STATUS.md`.
3. Baca `docs/OVERLAY_MAP.md`.
4. Baca `docs/RESOURCE_CATALOG.md`.
5. Baca `docs/ROM_STRUCTURE.md`, `docs/GAME_RULES.md`, dan bagian terbaru `ANALYSIS_LOG.md`.
6. Baca `docs/EMULATOR_WORKFLOW.md` dan `docs/RUNTIME_TEST_PLAN.md`; emulator/debugger adalah jalur utama untuk memverifikasi aturan gameplay, bukan opsi tambahan.

## Identitas dan struktur disc

- Judul: Naruto: Shinobi no Sato no Jintori Gassen, PS1 Japan.
- Executable: `SLPS_035.53`; load address `0x80010000`, entry PC `0x80011448`, text size `0x5D800`.
- Filesystem ISO: DATA.BIN 66.015.232 byte (LBN 212), DATA2.BIN 166.428.672 byte, DUMMY.BIN 50.667.520 byte, XASECT.BIN 692 byte, executable, SYSTEM.CNF.
- SHA-256 ROM dan file hasil ekstraksi ada dalam dokumen struktur ROM.

## Temuan statis terbaru (2026-10-15)

- Pada executable file offset `0x46098` / RAM `0x80055898`, pasangan `0xD4, 0x2F44` mengarah ke bootstrap DATA.BIN: LBN 212, panjang 12.100 byte.
- Bootstrap DATA.BIN berisi `0x44) byte kode dan tabel `0x2F00) byte (1.504 entri × 8 byte), paling kuat ditafsirkan sebagai `(LBN, byte_length)`.
- 1.500 entri aktif, 4 kosong (1491–1494); interval sektor aktif tidak overlap dan mencakup 32.227 dari 32.234 sektor DATA.BIN.
- Resource signatures: PK02 921; TIM valid 246 (29 4-bit, 217 8-bit); NARUTOSceneV001 126; NARU lainnya 125; PSQ0 6; PSQ1 2; TXT2 1; unclassified 73.
- XASECT.BIN: 86 pasangan. Consumer sekitar `0x80019468` menghitung `index = input >> 4` dan memakai field pertama pasangan sebagai offset aditif; semantik keseluruhan masih hipotesis.
- Tidak ada eksperimen runtime/debugger pada sesi analisis ini. Formula biaya barrier/upgrade, income, battle, kartu, dan semua flag kemenangan masih terbuka.

## Berikutnya — prioritaskan aturan gameplay

1. Telusuri handler aksi bangun (ESTATE) dan upgrade (LVUP_ESTATE): sumber biaya, pemeriksaan Chakra sebelum transaksi, delta Chakra, dan field petak yang ditulis. Jangan samakan contoh UI 60/150 dengan formula universal.
2. Telusuri pemicu income dan transfer wilayah: kapan Chakra bertambah/berkurang, apakah level barrier mengubah income, dan kapan kepemilikan berganti.
3. Telusuri battle, roulette, jutsu, dan kartu lewat perubahan state/call chain, bukan inventarisasi container aset tanpa tujuan gameplay.
4. Petakan raw ID tabel 0x80057798 dan 0x80064918 ke Story/Party config; field target +0x08 tidak sama untuk semua record.
5. Jika emulator/debugger tersedia pada lingkungan, rancang tes memakai file yang sudah di Library. Jika tidak tersedia, beri label hasil sebagai analisis statis.
6. Perbarui GAME_RULES.md, OVERLAY_MAP.md, STATUS.md, dan ANALYSIS_LOG.md setelah penemuan yang dapat direproduksi.

Dokumen penelitian terkait: [STATUS.md](STATUS.md), [docs/OVERLAY_MAP.md](docs/OVERLAY_MAP.md), [docs/RESOURCE_CATALOG.md](docs/RESOURCE_CATALOG.md), [docs/ROM_STRUCTURE.md](docs/ROM_STRUCTURE.md), [docs/GAME_RULES.md](docs/GAME_RULES.md), [ANALYSIS_LOG.md](ANALYSIS_LOG.md).


## Arsip file kerja — pembaruan 2026-10-15

Enam file hasil ekstraksi ISO disimpan di Library ChatGPT pada folder `Naruto Research Files` untuk memudahkan pemulihan lintas chat. ROM asli tetap terpisah; file game tidak diunggah ke GitHub.

| File / artefak | Lokasi Library | Status |
|---|---|---|
| `DATA.BIN` | `/Naruto Research Files/DATA.BIN` | Tersimpan |
| `DATA2.BIN` | `/Naruto Research Files/DATA2.BIN.zip` | Tersimpan sebagai ZIP; ekstrak sebelum analisis byte-level |
| `DUMMY.BIN` | `/Naruto Research Files/DUMMY.BIN` | Tersimpan |
| `SLPS_035.53` | `/Naruto Research Files/SLPS_035.53` | Tersimpan |
| `SYSTEM.CNF` | `/Naruto Research Files/SYSTEM.CNF` | Tersimpan |
| `XASECT.BIN` | `/Naruto Research Files/XASECT.BIN` | Tersimpan |

`DATA2.BIN` berukuran 166.428.672 byte dan tidak muat ditambahkan mentah karena batas kapasitas Library. Kompresi ZIP mengurangi berkasnya menjadi sekitar 42 MiB. SHA-256 DATA2.BIN hasil ekstraksi ZIP sudah diverifikasi pada 2026-10-15: be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9. ZIP DATA2.BIN.zip yang tersimpan di Library memiliki SHA-256 67e7a372c6d02379d8cc715d15f3521c0914b8f17ee6e2f66a2bc32695367668.

Catatan untuk chat baru: cari file di Library dengan path di atas; jangan mengasumsikan file otomatis ada di filesystem. Jika akses Library gagal, pengguna juga menyimpan ROM asli di laptop sehingga file dapat diekstrak ulang. Jangan menghapus file Library lain untuk memberi ruang tanpa instruksi pengguna.


## Penemuan trace Chakra — 2026-10-15

- Setter 0x8001387C banyak dipakai untuk sinkronisasi nilai yang tersalin dari record pemain; jangan menafsirkan semua pemanggil sebagai biaya/pengurangan.
- State machine (base resource sementara 0x800D0000) membentuk nilai +0xB40 dari +0xB30 + +0xB38, lalu pada state +0xB2A == 7 memproses jumlah pending +0xB44 bertahap ke Chakra pemain yang ditunjuk +0xB2B, mengurangi pending sampai selesai. Ini mekanisme transfer/perubahan nilai Chakra, bukan bukti khusus biaya barrier. Sumber +0xB30/+0xB38 dan semantik event belum ditemukan.
- Jalur kemenangan Chakra sekitar 0x80111200–0x80111280 membandingkan Chakra pemain terhadap getter target 0x80012A70 ketika kondisi bit 0x200 aktif. Kondisi menang adalah current >= target pada jalur ini. Base resource belum divalidasi lewat loader runtime.
- Prioritas segera: cari penulis field +0xB44 dan kaitkan event ESTATE/LVUP_ESTATE dengan pemeriksaan saldo, sumber biaya, dan perubahan field petak. Jangan mengklaim 60/150 sebagai rumus universal.

## Aturan persistensi kuota — wajib dibaca

Pengguna memiliki kuota internet sangat terbatas sehingga upload ulang ROM/ISO sekitar 300 MB tidak realistis. Jangan mengandalkan ROM laptop pengguna; jangan meminta upload ulang untuk meneruskan riset. Mulai dari file ekstraksi yang disimpan di Library pada /Naruto Research Files/. Gunakan Files untuk menemukan dan mematerialisasikan file saat diperlukan, lalu cocokkan hash terhadap docs/ROM_STRUCTURE.md dan docs/RESOURCE_CATALOG.md. File Library tidak otomatis muncul di filesystem chat baru. Jika file yang diperlukan tidak dapat diakses, dokumentasikan kendala dan lanjutkan analisis dari dokumentasi/repo; minta transfer hanya bila pengguna secara eksplisit menawarkan alternatif.

## Pembaruan aturan gameplay statis — 2026-10-15

- Tabel konfigurasi executable pada alamat RAM 0x80057798 memakai stride 0x54; pasangan Chakra awal/target mencakup 1500/3000, 2000/4000, 2500/5000, 3000/6000 serta dua record 600/0 yang kondisi pemilihannya belum diketahui.
- Tabel lain pada 0x80064918 (stride 0x30) menunjukkan pasangan 1500/3000 pada sekurangnya 13 record awal nonnol yang diperiksa.
- Field +0x04 digunakan sebagai Chakra awal; field +0x08 sebagai target pada cabang kemenangan yang ditelusuri; field +0x0C (400/0) belum dipahami.
- Label lama 0x800EC200 (target Chakra) dan sekitar 0x800F70D0 (aritmetika Chakra) ditarik kembali karena base/identitas modul belum diverifikasi.
- Tidak ada uji runtime emulator/debugger yang diselesaikan. Biaya, income, battle, roulette, dan semua efek kartu tetap terbuka.


## Kebijakan dan status emulator — 2026-10-15

- Jalur penelitian resmi sekarang mencakup penggunaan emulator/debugger sebagai prioritas untuk menguji aturan yang ditemukan secara statis. Emulator utama yang direkomendasikan adalah PCSX-Redux (debugger CPU, memory editor, breakpoint, GDB server); Mednafen dapat dipakai untuk cek silang.
- Detail setup/eksperimen: [docs/EMULATOR_WORKFLOW.md](docs/EMULATOR_WORKFLOW.md), [docs/RUNTIME_TEST_PLAN.md](docs/RUNTIME_TEST_PLAN.md).
- Pada awal sesi executable emulator tidak tersedia dan DNS container gagal. Setelah itu PCSX-Redux diunduh melalui GitHub Actions artifact dari release, hash diverifikasi, dan antarmuka berhasil dijalankan di Xvfb. GUI boot sudah diuji, tetapi game belum terkonfirmasi mencapai menu/title; jangan klaim gameplay runtime.
- Jangan meminta pengguna upload ulang ROM atau ISO sekitar 326 MB. Sumber file untuk analisis tetap Library; bila runtime memerlukan interaksi emulator yang tidak dapat dilakukan environment ini, gunakan prosedur tercatat dan simpan hanya log teks/screenshot yang diperlukan, tanpa mengunggah ROM, BIOS, save state, atau dump memori ke repo.


## Emulator research kit — 2026-10-15

- PCSX-Redux Linux x86_64 AppImage dipublikasikan sebagai Release asset (tidak masuk Git history): [Research Emulator release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15). Asset: `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage`, size 65.747.557 byte, SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`. Repo privat; chat baru perlu akses connector GitHub/repo untuk mengunduh asset.
- Download, verifikasi hash dan best-effort Xvfb launcher check sukses pada GitHub Actions run [#38692549397](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38692549397). Ini hanya menguji launcher, bukan game.
- Uji GUI pertama menunjukkan “No BIOS loaded, emulation halted”. OpenBIOS default kini berhasil dibangun dan dilampirkan ke release oleh [Actions run #38693358323](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693358323). `openbios.bin` 524.288 byte, SHA-256 `713ea2aed58606282b3ff5e91d77f8c5892ea36f5adcd279d2c7dd26604a625d`; `openbios.elf` SHA-256 `d0d4cc73c9546e1e6af86d38ec894f5a6c81090ccdf97b1a3a39885c56af7bfc`. Uji dengan OpenBIOS tidak lagi menampilkan dialog BIOS kosong, tetapi layar yang terekam tidak membuktikan game telah boot. [Run #38693918169](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693918169) berhasil membangun varian `BOOT_MODE=fast` untuk mencoba auto-boot CD. Hash `openbios.bin` fastboot adalah `25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d`; hash ELF `2c8d36e2179841935a1d1331777380502cdb22528d086c99c6388cdcfa54b8aa`. Uji lokal menghasilkan layar hitam setelah kira-kira 12 detik; title/menu Naruto belum terkonfirmasi. Lanjutkan troubleshooting boot tanpa meminta upload ulang ROM dan jangan mengunduh atau menyimpan retail Sony BIOS.
- Launcher example setelah OpenBIOS tersedia: `pcsx-redux -bios /path/openbios.bin -interpreter -debugger -gdb -iso /path/game.cue -run`. File CUE harus berada bersama BIN dan menyebut nama BIN persis. Jangan meminta upload ulang ROM.
- Dokumen prosedur: [docs/EMULATOR_WORKFLOW.md](docs/EMULATOR_WORKFLOW.md), [docs/RUNTIME_TEST_PLAN.md](docs/RUNTIME_TEST_PLAN.md).

## Status runtime terbaru dan langkah lanjut — 2026-10-16

**Status:** game belum terkonfirmasi mencapai title/menu. Jangan menyebut gameplay runtime berhasil.

### Temuan terakhir
- ROM sumber tetap file Library; jangan meminta upload ulang sekitar 326 MB dan jangan mengunggah ROM/EXE/save state/dump memori ke repo.
- PCSX-Redux AppImage + OpenBIOS disimpan sebagai release assets: [research emulator release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15).
- Jalur CD normal membaca disc label `SLPS-03553`, membuka `SYSTEM.CNF;1`, membaca `BOOT = cdrom:\\SLPS_035.53;1`, lalu mencetak `boot file cdrom:\\SLPS_035.53;1`; pembacaan payload EXE tidak langsung mencapai `EXEC:PC0(80011448)`.
- EXE `SLPS_035.53` berukuran 385.024 byte: header 2.048 byte dan payload 382.976 byte (`0x5D800`, 187 sektor).
- Build chunked 32 sektor dan 8 sektor tidak mengatasi hang. Pada test 8 sektor, log berhenti setelah `[CHUNK8] before idx=0 ... bytes=16384`, tidak ada pesan `after`.
- Build diagnostik satu sektor sukses dibangun dan diterbitkan lewat [Actions #38697240018](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38697240018). Log menunjukkan pembacaan 2.048 byte mulai berjalan dan sedikitnya sektor pertama serta kemajuan sekitar sektor kesembilan terlihat setelah uji singkat sekitar 25 detik; belum ada bukti payload selesai dibaca atau game mencapai title.
- Jalur injeksi executable/debugger secara manual pernah mencapai `EXEC:PC0(80011448)`, `Execute !`, dan `CD_init`, namun layar tetap hitam. Jalur itu bukan boot disc biasa dan perlu memastikan `flushCache` dilakukan setelah injeksi.
- Dengan breakpoint diagnostik, jalur startup kemudian terlihat menunggu di rutin inisialisasi kartu memori (`buInit`/status kartu); bypass sementara melewati penantian tetapi belum memunculkan game.
- Petunjuk kompatibilitas input: log berulang menunjukkan perintah pad `0x43` (Set Config Mode), sementara konfigurasi PCSX-Redux yang dipakai kemungkinan `DeviceType=Digital`. Source upstream PCSX-Redux menunjukkan perintah non-`Read` seperti ini ditangani melalui jalur DualShock hanya jika `PadType::Analog`; bila tipe Digital, emulator mencatat `Unknown command for pad: 43`. Rujukan kode: https://github.com/grumpycoders/pcsx-redux/blob/db9bc8af44e3c77424127b573c17f9583ee2ab95/src/core/pad.cc. **Hipotesis belum diuji**: atur Port 1 ke Analog/DualShock, ulangi boot, dan amati apakah perintah 0x43 terjawab serta apakah startup maju.
- Pengguna mengunggah alternatif `PCSX-Redux-9c6f98a0-linux-x86_64.zip` (90.912.361 byte). File sudah terlihat/materialisasi dicoba, tetapi belum dapat diperiksa atau dijalankan karena shell/runtime file tool gagal merespons pada sesi tersebut. Jangan klaim ZIP alternatif sudah diuji atau mengunggahnya ke release sebelum isi dan kebutuhan dependensinya diverifikasi.

### Langkah saat melanjutkan
1. Coba kembali memeriksa ZIP unggahan pengguna dan gunakan build alternatif jika memang executable yang cocok tersedia.
2. Di PCSX-Redux, ubah controller Port 1 dari Digital menjadi Analog (DualShock), lalu ulangi jalur CD normal.
3. Bila jalur bypass dipakai, pastikan payload `SLPS_035.53` dimuat ke `text_addr`, cache di-flush, CD-ROM sudah diinisialisasi, dan startup kartu memori ditangani secara terukur—hindari bypass permanen yang mengubah banyak variabel sekaligus.
4. Simpan log/screenshot teks minimum dan hash build; jangan menyimpan ROM, BIOS retail Sony, save state, atau RAM dump di repo.
5. Kriteria sukses: log mencapai entry game **dan** layar menunjukkan title/menu Naruto yang dikenali. Setelah itu baru mulai test gameplay terkontrol.

Dokumen prosedur: [docs/EMULATOR_WORKFLOW.md](docs/EMULATOR_WORKFLOW.md), [docs/RUNTIME_TEST_PLAN.md](docs/RUNTIME_TEST_PLAN.md).


## Alternatif PCSX-Redux ZIP dari pengguna — pembaruan 2026-10-16

- **Tersimpan dan terverifikasi di Library ChatGPT** pada `/Naruto Research Files/PCSX-Redux-9c6f98a0-linux-x86_64.zip`.
- Ukuran: 90.912.361 byte; MIME `application/zip`.
- Library `file_id`: `file_00000000ff2c820781db759026d06ce2`; `library_file_id`: `libfile_1e46fb09892c819186df7299888b8b8f`.
- Asal: lampiran percakapan yang sudah ada; file disalin langsung melalui referensi lampiran ke Library, tanpa meminta pengguna mengunggah ulang. Penghapusan `DATA.BIN` dan `DUMMY.BIN` memberikan ruang yang diperlukan.
- Catatan: ZIP **sudah tersimpan**, tetapi isi arsip, SHA-256, dependensi, dan kemampuan menjalankannya masih belum diverifikasi. Percobaan pemeriksaan sebelumnya terhambat oleh `ClientError`/masalah runtime. Jangan mengklaim ZIP ini telah diuji hingga pemeriksaan benar-benar berhasil.
- Instruksi untuk chat baru: cari/materialisasikan file dari Library dengan nama/path di atas terlebih dahulu. Jangan meminta upload ulang ZIP atau ROM. Jangan menghapus file Library lain tanpa instruksi eksplisit.
- Jalur emulator alternatif sementara tetap PCSX-Redux AppImage + OpenBIOS yang sudah ada di [Research Emulator Release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15).



## Percobaan akses emulator setelah ZIP disimpan di Library — 2026-10-16

### Apa yang berhasil
- ZIP emulator alternatif, ROM BIN, dan CUE berhasil ditemukan dari Library dan dimaterialisasi melalui Files ke lokasi kerja yang dilaporkan:
  - `/mnt/data/naruto-runtime/PCSX-Redux-9c6f98a0-linux-x86_64.zip` — 90.912.361 byte.
  - `/mnt/data/naruto-runtime/Naruto - Shinobi no Sato no Jintori Gassen (Japan).bin` — 325.989.552 byte.
  - `/mnt/data/naruto-runtime/naruto-shinobi-jintori.cue` — 113 byte.
- Path tersebut berasal dari respons materialisasi Files; itu sendiri **tidak membuktikan** lingkungan shell dapat membaca file tersebut.

### Kendala sesi
- `container.exec` gagal dengan `ClientError` pada perintah pemeriksaan file, termasuk percobaan sederhana `echo runtime-check`.
- Python tool di lingkungan analisis gagal saat inisialisasi ulang, dan pemeriksaan ulang melalui Python serta Python yang terlihat ke pengguna juga gagal dengan `ClientError`.
- Karena itu isi ZIP belum dapat dilihat, daftar file arsip dan SHA-256 ZIP belum dapat diperoleh, binary belum diekstrak, dan PCSX-Redux **belum dijalankan pada sesi ini**. Tidak ada tes boot baru dari percobaan ini; status tetap belum terverifikasi.
- Ini adalah kendala tool/runtime, bukan bukti bahwa ZIP rusak atau emulator tidak bisa berjalan. Jangan simpulkan salah satunya tanpa tes.

### Langkah berikutnya saat eksekusi lokal pulih
1. Periksa ZIP tanpa menjalankan binary: `unzip -t`, daftar isi, SHA-256, arsitektur dan izin executable.
2. Ekstrak ke direktori terpisah yang dapat ditulis; jalankan binary dengan `--version` atau opsi bantuan terlebih dahulu dan catat dependensi yang hilang.
3. Siapkan OpenBIOS dari Release yang sudah ada; jangan gunakan/mencari retail Sony BIOS.
4. Jalankan ROM melalui CUE dengan interpreter/debugger dan log. Uji Port 1 Analog/DualShock sesuai hipotesis command pad `0x43`, tetapi ubah satu variabel setiap percobaan.
5. Sukses hanya jika title/menu Naruto terlihat dan input terbukti merespons. Jangan masukkan ROM/EXE/save state/RAM dump ke repo.


## Refined next emulator experiment — 2026-10-16

For the pending controller test, change Port 1's **Controller Type** to **Analog** in PCSX-Redux (Configuration → Controls). Do not treat the separate “Analog mode” checkbox or Lua `pad.setAnalogMode(true)` as an equivalent change: in the exact source commit used by the research-kit AppImage, `DeviceType` selects the emulated pad protocol (Digital=0, Analog=1), while `m_analogMode` is a different setting. Only the Analog controller type routes non-`0x42` commands such as `0x43` to the DualShock command handler.

Repeat the same boot attempt with the same ROM/CUE, OpenBIOS variant, CPU mode and other settings; only change Port 1's Controller Type. Compare whether `Unknown command for pad: 43` disappears, and independently verify the title/menu and input. Source evidence and limitations are logged at the end of `ANALYSIS_LOG.md`. This experiment has **not** been run in the current session because the execution runtime is returning `ClientError`.

## OpenBIOS source-level CD-read stall hypothesis — 2026-10-16

1. The next boot test must distinguish a CD read/event stall from BIOS configuration or controller protocol. Prefer the research-release AppImage pinned to root commit 0c3572c3db75f97542001e453ae80ba8c3f8acba (2026-10-01) unless inspection proves the user ZIP is more suitable. The filename PCSX-Redux-9c6f98a0-linux-x86_64.zip points to upstream commit 9c6f98a0ed0581635f9123147e382c248e0f5ddc (2026-09-28), but ZIP contents/hash are unverified.
2. Configure Port 1 in a fresh/portable PCSX settings profile: host input source PadType=2 (keyboard), emulated PS1 controller protocol DeviceType=1 (Analog/DualShock), Connected=true. Do not confuse DeviceType with the separate keyboard Analog mode binding.
3. Launch with explicit BIOS/CUE and logs. PCSX-Redux CLI supports -bios, -iso (BIN/CUE), -run, -interpreter, -debugger, -stdout, -lua_stdout and -logfile. Example, adjusting only filesystem paths:
   ./PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage -portable /tmp/naruto-pcsx-test -bios /path/to/openbios-chunked.bin -iso /path/to/naruto-shinobi-jintori.cue -run -interpreter -debugger -stdout -lua_stdout -logfile /tmp/naruto-pcsx-test/boot-analog.log
4. Source-level reason for the previous stall: OpenBIOS loadExe() reads the 2,048-byte header, then requests the 382,976-byte payload (187 sectors) via one syscall_read; dev_cd_read() translates aligned bytes to sectors; cdromBlockReading() waits for the DNE completion event while checking errors but has no overall timeout in that wait loop. This is compatible with a stuck CD event, but does not prove the actual runtime root cause.
5. Observe a long enough period for all 187 sectors and log each chunk completion, LBA, CD event/status, and PC. If the same LBA/event stalls repeatedly, use that evidence before changing the BIOS patch. Then verify title/menu pixels and input separately. Do not begin Story Mode testing before both title/menu and responsive input are confirmed.

Current blocker: Files materialization reports the ROM, CUE, EXE, DATA2 archive and user ZIP were copied to working paths, but container.exec and Python returned ClientError even on simple commands. No new runtime test was possible in this session. Never claim gameplay/Story Mode success without runtime evidence. Do not upload the ROM, game EXE, retail BIOS, save states or RAM dumps to GitHub.


## PCSX-Redux ZIP extraction record — 2026-10-16

1. Retrieve `/Naruto Research Files/PCSX-Redux-HEAD-x86_64.AppImage` from Library if you need the extracted `9c6f98a0` package. Its expected SHA-256 is `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`. The Library also has `PCSX-Redux-EXTRACTION-MANIFEST.md`.
2. The original ZIP's SHA-256 was `7e4c9378524ebfa35068944ba4aa9e3ebf7462678bcae33b3e7ae7c57dd99849`; it contained only that single AppImage and was replaced in Library by the extracted AppImage due the Library storage limit.
3. The build's embedded metadata identifies changeset `9c6f98a0ed0581635f9123147e382c248e0f5ddc`, build ID 335 (2026-09-28). Do not confuse this with the existing research-release emulator AppImage pinned to `0c3572c3db75f97542001e453ae80ba8c3f8acba` (SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`).
4. The extracted binary is not runnable in the current research container without a compatible userspace: its dependencies require GLIBC_2.42/2.43; the current host is glibc 2.41. The outer AppImage runtime answers `--appimage-version`, but mounting the AppImage fails due missing FUSE/fusermount. This is an environment compatibility blocker; do not infer the package or ROM is corrupt.
5. The repository has a package inventory in `docs/PCSX_REDUX_PACKAGE.md`. The 91 MB new AppImage is in Library, not Git history; the available GitHub connector cannot upload binary Release assets. The repository's existing release has a distinct smaller AppImage. Before resuming game boot tests, choose a build compatible with the actual host/glibc and available graphics backend. Do not claim runtime success based only on this extraction.


## Preferred build for GLIBC 2.41 host — 2026-10-16

### Preferred emulator build and unverified game compatibility

Use `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage` from the [existing research release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15), not the Library's `9c6f98a0` build that requires GLIBC_2.42/2.43. Candidate size 65,747,557 bytes; SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`. Packager says AnyLinux bundles dependencies, supports old/musl distributions, and avoids FUSE. GitHub Actions build log (run 36872881656 on 2026-10-01) shows `quick-sharun --simple-test` passed. This confirms generic launch smoke testing only, not Naruto game boot.

Run the full test when the runtime tool is usable again; the current container and Python services return ServerError:
1. Get the AnyLinux AppImage from the research release and verify the SHA-256 above.
2. Retrieve the exact ROM and `naruto-shinobi-jintori.cue` from Library; do not upload ROM/BIOS to GitHub.
3. Run with `openbios-chunked.bin`, isolated PCSX profile and log. Set PS1 Port 1 protocol to Analog (`DeviceType: 1`), keyboard as host input (`PadType: 2`), and `Connected=true`.
4. Prove menu and controls work. Monitor the complete 187-sector EXE payload read, CD events and entry PC. Repeat boot before starting Story Mode. Do not promise “no obstacles” or claim Story Mode success until these tests genuinely pass.


## Current Library package — AnyLinux artifact ZIP (2026-10-16)

Current Library package is `/Naruto Research Files/PCSX-Redux-0c3572c3d-anylinux-x86_64-artifact.zip` (workflow artifact ID 11170447493; Actions-reported ZIP digest `f6c27070b565cbc0554f1093c1374a16aee2b8635c72ef7b141f9ff7bd857ed0`). Extract the AppImage and verify its SHA-256 is `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`. The standalone candidate also exists in the [research GitHub release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15). It is a better glibc-2.41 candidate than `9c6f98a0` because AnyLinux packaging bundles dependencies and avoids FUSE; the packaging CI smoke test passed.

**Still untested:** the packager's smoke test is not a Naruto game test. The previous `9c6f98a0` binary needed GLIBC_2.42/2.43, was replaced in Library, and its historical hashes are retained in `docs/PCSX_REDUX_PACKAGE.md`. The separate extracted-manifest file was removed as stale. Container/Python calls currently return ServerError, so a fresh full boot test was not possible. On recovery, verify the AnyLinux binary hash; boot the exact ROM/CUE with OpenBIOS chunked, isolated profile and logs; set Port 1 `DeviceType: 1`, keyboard `PadType: 2`, `Connected=true`; confirm title/menu, input and complete 187-sector read; only then progress into Story Mode.


## Handoff setelah controlled Analog-port probe — 2026-10-17

1. Baca pembaruan terakhir pada `STATUS.md` dan `ANALYSIS_LOG.md`. Jangan mengulangi analisis source controller dari awal.
2. Baseline A/B: runner Actions [#38971848277](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38971848277) membuktikan kedua build mencapai `EXEC:PC0`, tetapi juga keduanya mencatat `Unknown command for pad: 43`; title/menu dan input belum terbukti.
3. Runner workflow terbaru ada pada commit [0439c1b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/0439c1bbf51d3c1be234150d6bee80c5b812ff1e). Setup Lua mengatur `PCSX.settings.pads[1].DeviceType = 'Analog'`, `Connected = true`, memanggil `PCSX.SIO0.slots[1].pads[1].map()`, lalu mencetak marker `PAD_SETUP=...`. Ini mengikuti contoh di tes internal upstream `tests/pcsxrunner/rumble.cc`.
4. **Tugas prioritas pertama:** temukan/ambil log run setelah commit di atas dan periksa marker Lua serta apakah pesan `0x43` masih ada. Hasil run tersebut belum dicatat sebagai terverifikasi, jadi jangan menganggap perubahan berhasil hanya karena file workflow telah di-commit.
5. Jika warning `0x43` hilang, lakukan tes GUI Xvfb yang terpisah memakai ROM/CUE dan BIOS sama; ukur atau kenali frame game di runner tanpa mengunggah screenshot game. Selanjutnya uji apakah input direspons. Jika tetap hitam, lanjutkan diagnosis jalur CD/read completion, cache/entry, init kartu memori dan rendering secara terpisah.
6. Jangan mengunggah ROM, game EXE, retail BIOS, save state, RAM dump, atau screenshot yang memuat aset game ke repo. Batas repo tetap Naruto Research/Runner saja, tidak menyentuh Tile Duel.

Correction: the initial workflow commit had malformed indentation inside the Lua heredoc. The corrected, current runner workflow is commit [0439c1b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/0439c1bbf51d3c1be234150d6bee80c5b812ff1e). Use only a run started from this corrected workflow when reading the Analog-port experiment result; no successful runtime outcome has been verified yet.


## Temuan runtime terbaru — 2026-10-17

1. Buka Actions run [#38973267415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973267415): tes Analog-port sudah sukses. Kedua build mencetak `PAD_SETUP=...`, mencapai `EXEC:PC0(80011448)`, dan tidak lagi mencatat `Unknown command for pad: 43`; baseline run #38971848277 mencatat warning itu pada keduanya.
2. Jangan menyatakan game tampil: kedua proses tetap berhenti oleh timeout 90 detik, dan tes ini menggunakan `-no-ui`. Menu Naruto serta respons input masih belum terbukti.
3. Workflow terbaru commit [85c08d9](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85c08d9ea255dc400c0771361abc95817a0a7ba6), Actions run [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926), menambahkan GUI probe Xvfb pada AnyLinux. Ambil hasil run tersebut, periksa metrik frame 10/20 detik dan OCR; tangkapan layar/log disimpan sementara lalu dibersihkan di runner.
4. Jika tampilan masih hitam, jangan ulang tes Analog yang sekarang terjawab. Pisahkan diagnosis jalur CD completion / OpenBIOS init / cache entry dan render-GPU. Input in-game baru boleh diuji setelah title/menu yang dikenali tampil.


## GUI result — 2026-10-17

- GUI/Xvfb test [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) is completed. Frames at 10s and 20s are both all-black according to image statistics (`1280x800`, mean 0, stddev 0, 1 unique color); OCR had no text. The filtered GUI output did not show `EXEC:PC0` or `Execute !` during 35 seconds, while the headless A/B test did. The 0x43 pad warning remains resolved by Port 1 Analog.
- Inspect latest CPU trace [Actions #38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045) from new workflow `.github/workflows/naruto-cpu-trace.yml`. It should log a `PC_TRACE=listener installed` marker and periodic `PC_TRACE frame=... PC=... RA=... SP=...` samples from `GPU::Vsync`.
- If VSync fires, use sampled PC values to identify whether the guest advances or repeats a loop; map addresses only after validating whether they land in the fixed executable or a mapped resource. If no samples fire, inspect the boot markers and consider CPU/GPU timing or the event source. Do not upload captured game images, ROM, BIOS, executable, RAM dump, or save state to the repository.


### CPU tracing retry — 2026-10-17

The first VSync/PC trace run [#38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045) segfaulted with code 139 after ~12 seconds and recorded no PC samples. Do not interpret it as a game/ROM failure because the new Lua listener is a confounder. Workflow commit [9419800](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/941980021c16dee3e779f6cc1066dad70b187ad4) now combines all Lua setup into one `-exec` and leaves the listener installed until timeout; run [#38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739) is the retry. First check if `PC_TRACE frame=` samples exist. If retry still crashes, use a VSync counter-only listener first; then add PC reads only after that works.
