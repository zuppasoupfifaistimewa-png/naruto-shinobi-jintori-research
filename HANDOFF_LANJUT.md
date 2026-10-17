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


### CPU trace attempt 2: instrument script failed to parse

Run [#38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739) failed with exit 134 due `unexpected symbol near '\\'`; the shell helper passed literal `\n` between Lua chunks. No actual PC trace occurred, so this is not evidence of game/ROM failure. Corrected workflow commit [7b8ce73](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/7b8ce731378e0115f616b7ff78874f5d17375e80) now uses one heredoc. Inspect retry [Actions #38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869), looking for the pad setup marker and `PC_TRACE frame=` samples.


### CPU trace attempt 3 — what is actually proven

Run [#38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869) emitted VSync PC/RA/SP samples through at least frame 780, and the separate emulator logfile records `EXEC:PC0(80011448)` / `Execute !`. The process exited 139 (segmentation fault) before the 35-second cap with an incomplete final trace row. Samples mainly show BIOS addresses, but logs do not establish a stable guest hang, and `PCSX.getRegisters()` access inside the callback is a potential test confounder.

Next run [#38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) is counter-only VSync tracing, commit [85d3e4f](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85d3e4ff31732b7788d67e447ea9df136dcb84f5). Look for `VSYNC_TRACE frame=...` counters and the final process exit. If counter-only runs stably but PC reads had segfaulted, add registers only with a safer minimal probe; if it crashes, investigate event callbacks separately.


### CPU tracing: current build requirement

Run [#38975154606](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975154606) could not run the built-in trace: the AnyLinux build based on commit `0c3572c3d` lacks `PCSX.CPU.Trace`, producing `attempt to index field 'CPU' (a nil value)` before any VSync marker. Do not interpret this as a ROM problem.

Latest workflow [commit c994afc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/c994afccfa62efcc01751a7c2b39d89b109d936a) now downloads and SHA-verifies the private upstream HEAD AppImage (hash `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`) from the research release, on Ubuntu 26.04. Check [Actions #38975223698](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975223698). It enables `PCSX.CPU.Trace` only at VSync frame 1620 and disables it at 1680, printing the trace size and last 80 instruction lines. Trace file output should stay in stdout only, with private ROM/BIOS/trace material cleaned on the ephemeral runner.


### GUI timing correction — 2026-10-17

The all-black root captures at 10s/20s from [Actions #38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) were taken before the headless run reached executable entry. Counter-only run [#38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) counted >2,040 VSync events in the 35-second cap and logged `EXEC:PC0` shortly after frame 1,620; therefore early GUI black frames alone do not prove a lasting black screen. Next useful GUI experiment is to extend observation to 60–90 seconds and target the PCSX-Redux window rather than blindly capturing the X root, while keeping frames local/temporary and cleaning them up. A recent attempted workflow edit was not applied; verify the file/commit before assuming extended capture exists.

The newest CPU trace workflow commit [8304b7d](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8304b7dd56be13673e83e84bb738458eca0cfc2d) builds upstream PCSX-Redux from pinned source `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` because both prebuilt AppImages lack `PCSX.CPU.Trace`. Track run [#38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756); once the build step completes, inspect whether it runs the bounded 1620–1680 frame instruction trace and prints the last 80 CPU trace records. If the compiled binary cannot run on host due missing shared libraries, move runtime invocation inside the same builder container rather than treating that as a game failure.


## Latest run links — 2026-10-17

- Extended GUI capture (30/60/90s): [Actions #38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679), workflow commit [aea4c20](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aea4c20accfd6d1c5089a226f52a2c4183d2d9a8). Its private ROM/BIOS and emulator downloads passed; GUI/A-B step was still running at the last check. Check the final log after the run is completed. Temporary frame images should be deleted by cleanup; do not upload them to the repo.
- Built-in CPU trace via pinned upstream source: [Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756), workflow commit [8304b7d](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8304b7dd56be13673e83e84bb738458eca0cfc2d). It was still compiling the pinned source in the official container at last check; build/trace result is not yet established.
- Latest runtime gating/caveat is also in `docs/RUNTIME_TEST_PLAN.md`: do not start RT-001 until both a recognized title/menu and responsive input are independently proven.


## Latest cloud verification and active retests — 2026-10-17

State carried forward; do not repeat the Analog-port or asset-setup steps unless new logs prove a regression.

- **Completed:** [boot test #38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679) verified secret presence, private Release asset retrieval, expected ROM size/SHA-256, CUE structure, BIOS/disc recognition, 187-chunk executable load, and `EXEC:PC0(80011448)` plus `Execute !`. Analog Port 1 removed `Unknown command for pad: 43`. This is executable-entry evidence only, not a visible Naruto title/menu or responsive gameplay.
- **GUI harness flaw fixed:** run #38975931679 measured the Xvfb root (all-black metrics), not the PCSX window. Runner commit [8829933](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8829933b3b6815dce694ebe6d46cd2a1f0fee9f0) installs window-query tools and captures a matching emulator window; if none is found, it records the window tree and avoids the root fallback. Retest: [#39000276365](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365).
- **CPU trace dependency fix:** prior source build #38975445756 failed to launch due missing host `libcapstone.so.5`; no guest trace occurred. Runner commit [d965dcc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/d965dcc864c73818e67d6a1e5f9edc19d4a3a17c) installs `libcapstone-dev` and checks all linked runtime dependencies before running the emulator. Retest: [#39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139).
- Runner setup documentation was corrected; the existing read-only secret and release assets have already been validated in a successful run. Do not ask the user to re-upload ROM, re-create the token, or run the emulator locally.

### Next actions

1. Read the final logs and conclusions of runs #39000276365 and #39000257139. Use the visible-window metrics/OCR only when `CAPTURE_WINDOW` confirms the target, and require title/menu recognition rather than simply nonblack pixels.
2. If the window exists but stays blank, use successful source-built CPU-trace rows to see whether PC moves after `EXEC:PC0`; do not infer that from the job result alone.
3. After a recognizable title/menu is observed, send controlled inputs in the cloud runner and confirm response; only then begin Story Mode rule tests. No screenshots/game assets should be published as workflow artifacts.


## Corrected GUI-window test result — 2026-10-17

Actions #39000276365 completed. The corrected workflow found the actual visible PCSX-Redux window at 30s, 60s, and 90s; all three window captures were uniformly black by metrics (mean=0, stddev=0, colors=1) and OCR was empty. Crucially, the GUI probe itself did not log the 187-chunk completion or EXEC:PC0 / Execute !; only the separate -no-ui headless A/B probes did. Thus this is not yet evidence of a black Naruto frame after game entry. Debug the GUI/headless boot-path discrepancy.

No screenshots, ROM, CUE, BIOS or log artifacts were uploaded, and cleanup completed. The CPU-source-build/dependency retest remains Actions #39000257139; inspect its build, dependency and trace output before inferring guest CPU state.


## Current GUI initialization diagnostic — 2026-10-17

- Window-targeted run [#39000276365](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365) successfully captured the real PCSX-Redux window at 30/60/90s, but each frame was uniformly black and OCR empty. The GUI probe did not log PAD_SETUP, executable chunk completion or EXEC:PC0. Headless A/B probes did log EXEC:PC0, so do not treat the GUI frame as a post-entry game screenshot.
- New diagnostics run: [#39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307), commit [259d587](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/259d587c6b677be7f6466b0ec61edb1940faec49). It checks GLX capabilities with glxinfo under Xvfb and prints GUI stdout/log tails, including whether the Lua PAD_SETUP marker is reached. Inspect the completed run to distinguish GUI initialization from guest boot.
- CPU trace/dependency rerun [#39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) remains active at last check; do not infer anything about guest PC until its actual trace lines appear.


## Handoff — cloud A/B and GUI/trace repairs, 2026-10-17

Repos allowed remain Naruto Research (private) and Naruto Runner (public); do not access Tile Duel. Do not request ROM re-upload or secret recreation.

### Verified results

- Private Release: [research-emulator-pcsx-redux-2026-10-15](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15). Exact AppImage asset hashes and sizes are in docs/PCSX_REDUX_PACKAGE.md.
- Matched headless A/B run [#39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307): both builds read all 187 executable chunks and log EXEC:PC0(80011448) plus Execute !. Analog Port 1 suppresses the earlier Unknown command for pad: 43 warning on both. This is executable-entry evidence only.
- GUI part of that run is different: GLX/Mesa llvmpipe OpenGL 3.3 is available; actual AnyLinux emulator window found, but captures at 30/60/90 seconds are all-black (one color, mean/stddev zero) and OCR empty. GUI log did not reach chunk completion or executable entry.
- AppImage called PCSX-Redux-HEAD-x86_64.AppImage is not the same as source-build used for trace. Package metadata identifies source 9c6f98a0... from 2026-09-28; trace source commit is 6b9df482d7b77b9ae218d9c48c1ce1a43c265206. Neither prebuilt AppImage has the PCSX.CPU.Trace Lua API; source build is needed for instruction trace.

### Workflow changes on runner main

- GUI comparator workflow commit [0c4e3c1](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/0c4e3c172de6beda2c81a73579b45ba25d899ef4) captures both AppImage GUI windows in separate profiles, at 30/60/90 seconds, and cleanup now removes newly introduced images/logs/profile data. Rerun [#39002136781](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002136781) was queued when this handoff was written; inspect both builds' GUI results.
- Source trace workflow commit [16a6faff](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/16a6faff066b913480ad121b497db79df03a9de2) pins builder image ghcr.io/grumpycoders/pcsx-redux-build@sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4, runs dependency checks and emulator inside that image, and extends build timeout to 45 minutes. Rerun [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) was still compiling; do not call it a passed trace until CPU_TRACE_SIZE and CPU_TRACE_LINE outputs appear.

### Next steps

1. Check final logs for runs #39002136781 and #39001985849.
2. If both GUI windows are black before EXEC:PC0, diagnose GUI CPU/disc/CD-read path separately from GLX. Compare with the -no-ui route.
3. If source trace succeeds, inspect VSync counters at frames 1620–1680, CPU_TRACE_SIZE and last 80 instruction lines.
4. Do not test Story Mode until a recognizable title/menu appears and a controlled, logged input visibly changes the game or a reliably identified input state.
5. Keep ROM, BIOS, CUE, captures, saves, RAM dumps and sensitive material out of Git and public artifacts.


## Verifikasi GUI A/B terbaru dan perbaikan harness — 2026-10-17

Run GUI A/B [#39002136781](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002136781) berstatus workflow `success`, tetapi **bukan hasil uji GUI yang berhasil**. Langkah headless di job yang sama tetap membuktikan kedua AppImage membaca disc `SLPS-03553`, menuntaskan 187 chunk executable, dan mencatat `EXEC:PC0(80011448)` serta `Execute !`; keduanya tidak lagi mencatat `Unknown command for pad: 43`. Saat masuk bagian GUI, `gui_probe.sh` berhenti untuk kedua build pada `PAD_SETUP: unbound variable` karena variabel shell tidak diekspor. Tidak ada jendela emulator yang ditemukan dan tidak ada frame yang ditangkap. Karena hasil probe tidak dipaksa menjadi kegagalan job, status `success` hanya berarti step berakhir tanpa kegagalan workflow yang terdeteksi; status itu bukan bukti GUI/game berhasil.

Perbaikan minimal sudah didorong ke runner pada commit [aac684d120ec025c4a87197da8d835f90b89f869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aac684d120ec025c4a87197da8d835f90b89f869): ekspor `PAD_SETUP` sebelum skrip probe GUI dipanggil. Rerun ROM privat [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) sudah dipicu dan masih `in_progress` pada pemeriksaan terakhir; hasil frame, OCR, boot-marker GUI, dan cleanup masih harus diperiksa dari log akhirnya.

CPU-trace run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) juga masih `in_progress`. Secret dan pengunduhan/verifikasi file privat telah dilewati; step source-build di container Docker yang dipatok digest masih berjalan, sedangkan capture trace dan cleanup belum dimulai. Belum ada `CPU_TRACE_SIZE` atau `CPU_TRACE_LINE` yang dapat dipakai untuk analisis.

Current upstream PCSX-Redux yang terverifikasi saat cek adalah [41f3196257d0962942b60983201aade951ebbd54](https://github.com/grumpycoders/pcsx-redux/commit/41f3196257d0962942b60983201aade951ebbd54) (2026-10-17 02:53:17 UTC). AppImage berlabel “HEAD” tetap build source 9c6f98a0, bukan upstream HEAD terkini. Tidak ada bukti bahwa judul/menu tampil atau input gameplay merespons; gate RT-001 tetap tertutup dan Story Mode tidak boleh dimulai.


## Handoff terbaru — hasil GUI A/B sesudah fix dan CPU trace aktif (2026-10-17)

### Status repo

- Research repo tetap **private**; commit `main` sebelum pembaruan catatan ini `6fb27be6d84c8dbebf10d25af24cfc27803a27fe`.
- Runner repo **public**; commit runner terbaru yang diuji adalah `aac684d120ec025c4a87197da8d835f90b89f869`. Workflow CPU trace yang sedang berjalan berasal dari `16a6faff066b913480ad121b497db79df03a9de2`.
- Pemeriksaan pohon repo runner tidak menemukan ROM/ISO/CUE/BIOS, gambar, save state, dump RAM, atau binary emulator yang tersimpan di Git. Run GUI tidak menerbitkan artefak. Cleanup melaporkan file privat dan hasil diagnostik sementara sudah dihapus. Jangan menyimpan media atau hasil trace sensitif pada runner publik.

### GUI A/B: [Actions #39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886)

Workflow berstatus `success`, tetapi GUI/gameboot tidak lulus gate:

- **AnyLinux:** setup Analog PAD_SETUP berjalan; BIOS, disc `SLPS-03553`, SYSTEM.CNF dan BOOT target terlihat pada log GUI. Window emulator ditemukan dan ditangkap pada 30/60/90 detik tanpa memakai root window. Ketiga frame 1280×800 hitam seragam (mean=0, stddev=0, satu warna), OCR Jepang/Inggris kosong. GUI tidak mencatat chunk 187 selesai, `EXEC:PC0`, atau `Execute !`. Proses timeout 100 detik (exit 124).
- **Asset “HEAD”:** gagal membuat window: `Unable to create main window: Couldn't find matching GLX visual`; SDL gagal membuat konteks OpenGL 3.2 lalu mencoba profil 3.0. Tidak ada window/frame, PAD_SETUP atau executable-entry GUI. Exit 137 terjadi setelah batas observasi/eskalasi timeout, bukan bukti crash guest yang terisolasi.
- **Headless tetap terpisah:** kedua AppImage mengenali disc, menyelesaikan 187 chunk, mencapai `EXEC:PC0(80011448)` / `Execute !`, dan tidak lagi mencatat `Unknown command for pad: 43`. Exit 124 merupakan batas observasi 90 detik.

### CPU trace source-build: [Actions #39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849)

Saat pengecekan terakhir, source-build di dalam image Docker ber-digest tetap `in_progress` pada step build; step capture trace dan cleanup belum dimulai. Job mulai 04:17:11 UTC dan step build pada 04:17:26 UTC. API log archive belum tersedia saat run aktif (`BlobNotFound`), jadi belum dapat ditentukan apakah kompilasi bergerak lambat atau tertahan. Batas job 45 menit; pantau status dan baca log lengkap setelah step/run selesai. Jangan duplikasi run, mengubah dependensi, atau menyimpulkan guest hang sebelum log build/capture tersedia. Belum ada output `CPU_TRACE_SIZE` atau `CPU_TRACE_LINE`.

### Lanjutkan dari sini

1. Poll run #39001985849 dan periksa timestamp/hasil tiap step. Jika build gagal, gunakan log build aktual untuk identifikasi penyebab. Bila berhasil, periksa `PCSX_BUILD_RESULT`, shared-library check di image yang sama, semua marker VSync, `CPU_TRACE_SIZE`, `CPU_TRACE_LINE`, dan `TRACE_PROCESS_EXIT`. Exit 124 adalah batas observasi 35 detik yang dirancang, bukan otomatis crash.
2. Jika ada trace instruksi, inspeksi rentang frame 1620–1680 dan identifikasi transisi BIOS → executable game dari rekaman aktual. Verifikasi mapping overlay/loader sebelum menghubungkan alamat statis dengan RAM live.
3. Jika GUI tetap gagal, bandingkan log GUI versus `-no-ui` pada pemuatan CD, inisialisasi CPU, Lua, window/OpenGL, dan progres chunk. Jangan mengubah BIOS/ROM tanpa bukti penyebab.
4. RT-001 tetap **Open / blocked**: jangan mulai Story Mode sampai title/menu Naruto dikenali dan input terkontrol terbukti mengubah gambar atau input-state yang tervalidasi.

## Handoff final — CPU trace source-build selesai, diagnosis lanjutan — 2026-10-17

### Status terkini langsung dari GitHub

- Repo riset tetap **private**, `main` sebelumnya `a004b01315c7555fcb5415fba0d3c663fc9969fe`. Repo runner tetap **public**, `main` `aac684d120ec025c4a87197da8d835f90b89f869`.
- CPU trace [run #39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) selesai `success`, job mulai 04:17:11 UTC dan selesai 04:44:27 UTC. Build pinned source 04:17:26–04:43:46, trace 04:43:46–04:44:21, cleanup 04:44:21–04:44:25. Source `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`; image `ghcr.io/grumpycoders/pcsx-redux-build@sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`.
- `PCSX_BUILD_RESULT` sukses; dependency check `ldd` sukses dalam image yang sama tanpa `not found`. Trace: frames 1620/1650/1680 tercatat; window aktif di 1620; `CPU_TRACE_SIZE=16031631`; `TRACE_RESULT=VSync counter callbacks fired.`; `CPU_TRACE_RESULT=Built-in instruction records were printed.`; exit 124 adalah batas 35s yang dirancang.
- Log trace menunjukkan guest PC loop berulang `0x000015a4–0x000015c4`; load `0x5de4(a3)` bernilai 0, perbandingan register berulang, dan counter `$v1` menurun. Ini belum membuktikan hang permanen atau identitas modul. Trace tidak memuat SYSTEM.CNF, chunk 187, `EXEC:PC0(80011448)` atau `Execute !`.
- Run GUI A/B [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) sudah selesai `success`; itu bukan kelulusan GUI. AnyLinux window berhasil di-capture 30/60/90s tetapi hitam seragam/OCR kosong dan GUI tidak mencapai handoff. Build berlabel “HEAD” gagal startup GLX/OpenGL. Headless prebuilt kedua AppImage—jalur terpisah—tetap mencapai EXEC:PC0, tetapi tak boleh dipakai sebagai bukti bahwa source-build atau GUI mencapai entry.
- Tidak ada artefak Actions. Log cleanup menyatakan semua file ROM/CUE/BIOS/emulator/trace sementara dibersihkan. Tree repo runner publik hanya workflow, docs, README, dan .gitignore.

### Langkah berikutnya

1. Diagnosis beda jalur boot: bandingkan source pinned `-no-ui` dengan headless AnyLinux yang terverifikasi mencapai entry, berfokus pada OpenBIOS reset/CD read, pemuatan `SYSTEM.CNF`, keputusan menjalankan `SLPS_035.53`, dan mapping PC rendah. Catat marker terpisah untuk setiap jalur, jangan menyamakan keluaran.
2. Jika diperlukan, tambahkan sampling guest `PCSX.getRegisters().pc` pada VSync setiap 30 frame atau capture kedua di window frame lebih akhir, bukan mengulangi workflow identik. Build source sebelumnya perlu ~26 menit dan trace tidak dipublikasikan sebagai artefak, jadi setiap rerun harus mengubah observasi dengan alasan teknis yang jelas.
3. Setelah diketahui apakah PC tetap pada loop atau pindah, validasi alias RAM/BIOS/loader dan overlay dari sumber sebelum menetapkan nama fungsi. Jangan menamai alamat berdasarkan dugaan.
4. Perbaiki jalur GUI setelah penyebab perbedaan boot diketahui. Pastikan log GUI sendiri mencatat executable handoff sebelum menilai frame sebagai output game. Build “HEAD” perlu diagnosis startup GLX terpisah.
5. RT-001 tetap **Open / blocked**. Jangan mulai Story Mode sampai title/menu Naruto dikenali dan input terkontrol terbukti responsif.

No ROM, BIOS, screenshots, save state, RAM dump, private trace archive or emulator binary was committed/published to the public runner. Don’t repeat secret setup, asset download or PAD_SETUP work; those already succeeded.

## Tambahan handoff — isolasi selisih versi source (2026-10-17)

Source AnyLinux `0c3572c3db75f97542001e453ae80ba8c3f8acba` dan source trace `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` terpisah 803 commit (verifikasi GitHub compare). Area perubahan besar: `src/core/cdrom.cc`, `src/core/psxinterpreter.cc`, `src/core/pad.cc`, `src/core/psxmem.cc`, serta beberapa file emulator. Pada interpreter, target branch dan pelacakan delay slot berubah menjadi jalur `branchBase()`; ini perlu ditelaah, tetapi bukan bukti penyebab. Perintah headless kedua workflow sama-sama memakai `-interpreter`, bukan dynarec; perbedaan durasi tes masih ada, yaitu 90s untuk AppImage baseline versus 35s untuk source trace.

Sebelum menyebut regresi, buat uji source yang sebanding: batas observasi 90s, print `PCSX.getRegisters().pc` setiap 30 VSync, dan tempatkan jendela trace tambahan di frames 4500–4560. Print marker boot (OpenBIOS, SYSTEM.CNF, chunk 187, EXEC:PC0, Execute !) terpisah dari instruction rows agar tidak terbuang oleh `tail`. Jika guest masih di loop, ambil konteks instruksi cukup lebar di awal dan akhir jendela. Setelah itu inspeksi perubahan CD-ROM dan branch-delay dari diff terarah. Rerun seperti ini punya alasan teknis berbeda dari build sebelumnya; jangan memicu compile identik tanpa tambahan observasi.

Jangan keliru menganggap hasil headless AnyLinux pada versi yang lebih lama membuktikan bahwa source pinned telah boot; jangan pula menyimpulkan source gagal hanya dari capture 35 detik. RT-001 tetap Open/blocked.


## Handoff prioritas — trace lanjutan aktif, jangan gandakan run (2026-10-17)

Run [#39004736399](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39004736399) dipicu oleh workflow commit `d1c5b731befe5afacdfbdf3b9914b9f5e9f9ac64`. Pada pemeriksaan terakhir (2026-10-17 sekitar 05:03 UTC), job `trace-private-rom` masih membangun source; download/verifikasi sudah sukses, langkah capture serta cleanup masih pending. **Periksa run yang sama lebih dahulu; jangan dispatch/commit workflow identik saat run ini aktif.**

Perubahan yang sudah ada di runner: timeout observasi 90s; `PCSX.getRegisters().pc` tiap 30 VSync; trace awal frame 1620–1680 dan akhir frame 4500–4560; output trace hanya agregat frekuensi PC dari 200 record terakhir tiap jendela, tanpa disassembly/operand mentah; boot markers dicetak terpisah; cleanup `if: always()` tetap aktif. Source dan image builder tetap dipatok sama. Setelah run selesai, verifikasi seluruh step dan cleanup, periksa marker boot serta PC awal/akhir dan ringkasan trace, pastikan tidak ada baris instruksi mentah, lalu perbarui bersama-sama `STATUS.md`, `HANDOFF_LANJUT.md`, `ANALYSIS_LOG.md`, `docs/RUNTIME_TEST_PLAN.md`, dan `docs/PCSX_REDUX_PACKAGE.md` dengan hasil aktual.

Source `psxmem.cc` pada pin yang dipakai memetakan PC rendah `0x000015a4–0x000015c4` ke RAM (alias wilayah `0x8000xxxx/0xa000xxxx)); ini hanya bukti pemetaan memori, **bukan** identifikasi pemilik loop sebagai BIOS, loader, atau overlay. Interpretasi harus menunggu PC sampling dan jendela akhir.

Log publik run lama [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) memuat 80 record instruksi/operand. Workflow baru tidak mencetak baris tersebut, tetapi log lama belum terhapus karena tool GitHub yang tersedia di sesi ini tidak mempunyai aksi delete workflow run/log.

## Handoff final — hasil CPU trace 90 detik (#39004736399), 2026-10-17

### Status GitHub yang diverifikasi

- Run [#39004736399](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39004736399) berakhir `success`. Job mulai 05:01:31 UTC, selesai 05:29:40 UTC; dalam WIB 12:01:31–12:29:40. Ketujuh step termasuk build, capture trace, dan cleanup berakhir sukses.
- ROM diverifikasi pada ukuran 325.989.552 byte serta SHA-256 `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`; CUE sementara valid setelah normalisasi path. Source pin `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`; digest image builder `sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`.
- Build source menghabiskan sekitar 26m20s; `PCSX_BUILD_RESULT` muncul dan pemeriksaan `ldd` tanpa dependency `not found` sukses.
- Step capture mencapai batas 90 detik dengan `TRACE_PROCESS_EXIT=124`; itu exit code timeout observasi yang dirancang, bukan crash dengan sendirinya. Kedua jendela agregasi berjalan dan cleanup menghapus ROM/CUE/BIOS, binary source-build, dan trace log sementara. Artifact list kosong.

### Hasil guest PC dan marker boot

- Terekam 158 sampel PC setiap 30 VSync dari frame 30 hingga 4740. Sebanyak 157 sampel bernilai `0x000015a4`; hanya frame 420 bernilai `0x00000870`, kemudian PC kembali ke `0x000015a4`.
- Jendela trace awal 1620–1680 dan akhir 4500–4560 masing-masing melaporkan 200 record yang disampling, 9 PC unik, dan pola alamat teratas yang sama: `0x000015c0` / `0x000015c4` masing-masing 23 kemunculan; `0x000015a4` dan alamat tetangga sekitar 22 kemunculan. Ini mendukung pola loop berulang sepanjang observasi.
- Marker positif terbatas pada OpenBIOS terdeteksi serta disc `SLPS-03553`, ID `SLPS03553`, executable `SLPS_035.53;1`. Tidak ada marker `SYSTEM.CNF`/BOOT, chunk executable 187 selesai, `EXEC:PC0(80011448)`, atau `Execute !`. Tidak ada bukti title/menu.
- Pada bagian runtime log yang sebenarnya (bukan echo isi skrip), tidak ada baris disassembly/operand mentah. Workflow baru mengeluarkan agregat PC saja. Log lama #39001985849 masih dapat diakses dan dilaporkan memuat 80 record instruksi/operand; tool GitHub yang tersedia di sesi ini belum menyediakan operasi delete run/log.

### Kesimpulan dan langkah selanjutnya

Perlakukan `0x000015a4–0x000015c4` sebagai **loop PC yang belum diidentifikasi**. Alamat rendah dipetakan ke RAM oleh konfigurasi memori emulator, tetapi itu tidak cukup untuk menamai pemiliknya sebagai BIOS, loader, atau overlay. Run ini lebih kuat daripada trace 35 detik sebelumnya karena memakai batas observasi 90 detik dan jendela akhir, namun tidak mencapai handoff executable.

Langkah riset berikut yang paling diskriminatif adalah menelusuri sumber OpenBIOS/boot-loader yang sesuai dengan PC rendah dan menentukan apakah pembacaan CD atau event tunggu yang terkait bisa dibuktikan dari sumber/marker. Pertahankan output publik hanya pada boot markers, status tunggu yang terpilih, PC sampling dan agregat; jangan mencetak disassembly/operand mentah. Hindari build identik tanpa hipotesis baru.

**RT-001 tetap Open / blocked:** jangan memulai Story Mode sampai title/menu Naruto terlihat dan input terkontrol terbukti responsif. Jangan meminta ROM upload ulang, secret baru, atau uji laptop. Jangan membuka/menyentuh repo Tile Duel.

## Handoff terbaru — 2026-10-17: capture dan source-current GUI probe

- Live main sebelum perubahan sesi ini cocok dengan SHA yang diketahui: riset `f31f8f8226f3a8bcad823cb54c71fe6a1a160610`, runner `d1c5b731befe5afacdfbdf3b9914b9f5e9f9ac64`. Workflow riset privat baru sudah membuat commit `0654ceb514e22eec8c5ff8f2682e45a9009b58b4`; workflow runner retensi dibuat pada commit `7bf35c7e544c9f7af0da6fede1aa9d7af29edb56`. Selalu cek SHA live lagi sebelum perubahan lanjutan.
- [Run privat #39011515345](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011515345): ROM hash/ukuran lulus; OpenBIOS/disc dikenal; 187 chunk dibaca; `EXEC:PC0(80011448)` dan `Execute !` terlihat. Lua GPU screenshot pada `-no-ui` menghasilkan width=0, height=0, bpp=0 pada frame 1500/1680/1800. Pengolahan gagal karena dimensi nol; cleanup sukses dan tidak ada artefak capture yang terdaftar. Jangan ulangi metode screenshot itu dalam mode `-no-ui`.
- [Run privat #39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) men-test GUI jendela yang sesungguhnya memakai source pin upstream `1525a93676dbece9fe70f10ff129aeaa14eec30d` dan builder yang sudah dipakai dalam build sebelumnya. Pada saat handoff, workflow masih queued/in progress; baca hasil akhirnya sebelum membuat kesimpulan. Capture hanya disimpan sebagai artefak privat ber-retensi 3 hari dan workspace dibersihkan.
- Run publik lama dengan 80 record instruksi mentah [#39001985849] telah dihapus secara selektif melalui [cleanup run #39011611436](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39011611436); API GET sesudahnya memberi 404. Jangan mencetak atau menerbitkan instruksi/operand mentah.
- Baseline berikutnya: jangan build identik. Bandingkan hasil GUI source-current dengan baseline AnyLinux; jika title/menu terlihat, verifikasi respons pad terkontrol terlebih dahulu, kemudian Story Mode. Bila tetap gagal, uji varian BIOS/boot secara terpisah atau emulator PS1 cloud alternatif berdasarkan hasil aktual.
- **RT-001 Open / blocked:** belum ada title/menu terkonfirmasi dan input gameplay terkontrol belum terbukti. Story Mode belum dimulai/tamat.

## Uji emulator alternatif tambahan — 2026-10-17

Workflow privat [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) kini menguji rilis DuckStation resmi, dengan AppImage SHA-256 `c5e6f045f6a242082fcafa9f02d56ad895e233b942728788d232ad0c0c765c24`, ROM yang sama dan OpenBIOS `openbios.bin` dari private release. Harness Xvfb mengambil frame jendela dan mengirim Return/Cross lewat pemetaan keyboard sementara, lalu menyimpan capture sebagai artifact privat 3 hari dan menghapus workspace. Status saat catatan ini dibuat: queued; belum ada hasil boot/menu/input yang bisa disimpulkan. Ini uji kandidat, bukan klaim kompatibilitas.



## Handoff terbaru — hasil aktual DuckStation probe, 2026-10-17

- Run [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) menyelesaikan workflow, tetapi emulator tidak start. Pesan runtime adalah `libOpenGL.so.0` hilang sebelum jendela dibuat; seluruh capture report `no DuckStation window found`, urutan Return/Cross dilewati, dan artifact ZIP ID `12093451882` hanya berisi log stdout 183 byte, tanpa PNG. Ini bukan uji kompatibilitas BIOS/ROM yang valid.
- Saya memperbaiki workflow `.github/workflows/naruto-duckstation-private-probe.yml` dalam commit `058aadea1c664712b62a63cf01fcb3e5598ef047`: instal `libopengl0 libglx0 libgl1` serta glob artifact `captures/*.png`. Rerun [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) perlu dinilai berdasarkan log/frame aktual.
- Source-current PCSX-Redux run [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih membangun source pin `1525a93676dbece9fe70f10ff129aeaa14eec30d`; jangan mulai run build duplikat selama proses itu belum selesai.
- Langkah lanjut: cek hasil akhir kedua run dan artefak privat; jika DuckStation membuka window, pastikan title/menu dikenali lalu buktikan kontrol; jika tidak, perbaiki berdasarkan error baru atau pilih eksperimen yang lebih diskriminatif. Jangan menafsirkan conclusion Actions sebagai keberhasilan game.
- **RT-001 Open / blocked.** Story Mode belum terbukti dimulai atau tamat. Jangan menyentuh repo Tile Duel, meminta ROM upload ulang, atau menaruh ROM/BIOS/screenshot privat/save state/dump memori di repo publik.


## Handoff tambahan — DuckStation EGL dependency, 2026-10-17

Rerun DuckStation [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) mengungkap dependensi kedua yang hilang: `libEGL.so.1` (exit 127 sebelum jendela). Tidak ada capture PNG/OCR dan input dilewati; workflow sukses hanya karena skrip memperlakukan ketidaktersediaan window sebagai nonfatal. Commit `5afd32eca0d32ee191de7f2963f74b53aed89448` menambahkan `libegl1`; run [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) masih berjalan pada boot/capture. Source-current PCSX [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) juga masih build. Periksa kedua hasil aktual sebelum memilih metode berikutnya. RT-001 tetap Open / blocked.


## Handoff final DuckStation probe — 2026-10-17

Run [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) kini berhasil membuka GUI setelah `libegl1` ditambahkan, tetapi hanya menampilkan first-run setup wizard. Halaman BIOS mengatakan DuckStation memerlukan BIOS PS1/PS2; UI mendeteksi satu berkas tetapi tidak menganggapnya BIOS valid. Log mencatat pemetaan berkas dan pencarian Auto BIOS, namun tidak ada marker disc `SLPS-03553`, `SYSTEM.CNF`, atau entry executable. Return mengubah langkah wizard; itu bukan input Naruto. Z/Cross juga belum terbukti diterima game. Artifact privat ID `12094155047` berisi 8 PNG plus stdout; tangkapan ditinjau untuk mengonfirmasi wizard, lalu salinan ZIP lokal dan hasil ekstraksinya dibersihkan. Cleanup runner sukses.

**Keputusan operasional:** jangan meminta BIOS retail baru atau menganggap DuckStation sudah menguji kompatibilitas game. Dengan hanya OpenBIOS yang tersedia, hentikan investigasi DuckStation untuk saat ini dan prioritaskan PCSX-Redux source-current run [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708), yang masih membangun pada pemeriksaan terakhir. RT-001 tetap Open / blocked sampai title/menu dan respons input nyata terlihat.


## Handoff terbaru — hasil source-current dan OpenBIOS A/B, 2026-10-17

### Source-current GUI probe #39011842708
Run [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) selesai `success`; source pin `1525a93676dbece9fe70f10ff129aeaa14eec30d` berhasil dibangun dan dependency check lulus. Pada GUI, capture jendela emulator di 20/40/60/80/95 detik semuanya uniform black (1280×800, mean 0, stddev 0, satu warna), OCR kosong. Marker: disc `SLPS-03553`, OpenBIOS, PAD_SETUP Port 1 Analog, guest PC sampel pada frame 300=`0x000015a4`; tidak ada `SYSTEM.CNF`/BOOT atau `EXEC:PC0`. Artifact privat #12094116949 berisi lima PNG hitam dan stdout. Cleanup sukses. Kesimpulan: build berhasil, GUI game belum boot/terlihat.
### Fastboot vs chunked OpenBIOS #39013612865
Build AnyLinux sama dan ROM sama:
- `openbios.bin` fastboot mencapai `SYSTEM.CNF`, `BOOT`, `EXEC:PC0(80011448)`, dan `Execute !`.
- `openbios-chunked.bin` terhenti setelah progress pembacaan payload (log sampai indeks 40); tidak ada entry marker.
- Capture harness gagal menemukan jendela bagi kedua varian, sehingga tidak ada PNG maupun tes input yang benar-benar dilakukan. Artifact #12094102119 berisi stdout/log saja. Perlakukan perbedaan ini sebagai jalur loader/BIOS yang diskriminatif, bukan bukti title/menu.
### Next run
Run [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) menguji ulang hanya fastboot OpenBIOS dengan window enumeration generik, log window tree, frame/OCR dan input bertahap. Status pertama yang terlihat: queued; periksa status dan artefak aktual sebelum menyimpulkan.
**RT-001 Open / blocked.** Jangan mulai Story Mode hingga title/menu terlihat dan kontrol terbukti merespons. Repo Tile Duel tetap tidak boleh diakses.


## Handoff — fastboot ditangkap tetapi tetap hitam, 2026-10-17

Run [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) menemukan jendela X11 generic (ID 543, 1280×800), sehingga kegagalan pencarian caption sebelumnya memang selector yang terlalu sempit. Gambar sebelum input, sesudah Return, sesudah Z/Cross dan pada 40/65/90s semuanya uniform black; OCR kosong. Log fastboot mencapai `SYSTEM.CNF`, `BOOT`, `EXEC:PC0(80011448)`, `Execute !`. Tombol sudah dikirim ke window yang ditemukan, tetapi karena layar hitam tidak ada respons gameplay yang bisa diverifikasi. Artifact privat #12094179559 berisi frame/log; cleanup sukses.
Run lanjutan [#39015290594](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015290594) mengulang fastboot dengan capture yang sama tetapi tanpa `PCSX.getRegisters()` dalam callback VSync. Ini memeriksa hipotesis bahwa pembacaan register yang pernah mengganggu emulator memengaruhi frame loop. Periksa hasil akhir. Jangan anggap entry handoff sebagai title/menu.
RT-001 tetap Open / blocked.


## Koreksi capture fastboot dan run pengganti — 2026-10-17

**Koreksi wajib:** run [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) melaporkan `CAPTURE_WINDOW id=543`, tetapi 543 adalah ID root Xvfb (`0x21f`), karena regex `.*` juga cocok dengan root. Capture hitam/mean 0/OCR kosong dari run ini bukan evidence visual emulator; tarik kembali kesimpulan bahwa fastboot GUI tampil hitam. Yang tetap sah adalah log fastboot mencapai `SYSTEM.CNF`, `BOOT`, `EXEC:PC0(80011448)`, `Execute !`.
Run #39015290594 memakai logic root-inclusive yang sama dan tidak boleh digunakan untuk memutuskan visual game; commit root-exclusion memicu run pengganti [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649). Workflow commit `83173bb10cfbf905a296f59720c0a63c95bc3a32` kini membaca ID root melalui `xwininfo -root` lalu melewatinya sebelum memilih jendela aplikasi ≥400×250. Validasi capture baru: ID harus bukan ID root, ada `CAPTURE_WINDOW` non-root, dan window tree saat tidak ditemukan harus menunjukkan alasan sebenarnya.
Source-current PCSX run #39011842708 masih sah sebagai capture window aplikasi karena dipilih lewat nama PCSX, dan frame aktualnya memang seragam hitam; tetapi itu build source + chunked BIOS, bukan fastboot. RT-001 tetap Open / blocked.


## Handoff tambahan — aplikasi ada di tree tetapi selector window masih gagal, 2026-10-17

Log run [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649) mengonfirmasi root ID 543 (`0x21f`) sudah dikecualikan. Namun `xdotool search --onlyvisible --name '.*'` hanya mengembalikan root pada kumpulan kandidat, sehingga tidak ada frame/input. Dump root tree pada log justru menunjukkan jendela child nyata `0x200034 "PCSX-Redux"` ukuran 1280×800. Ini **kegagalan selector**, bukan bukti aplikasi tidak membuat window. Boot logs fastboot tetap mencapai `SYSTEM.CNF`, `BOOT`, `EXEC:PC0(80011448)` dan `Execute !`.
Workflow commit `1acd87e9960c0caeb334cffc48ed8aea212212e1` kini parsing XID langsung dari `xwininfo -root -tree`, menyingkirkan root secara eksplisit, memilih window aplikasi non-root ukuran ≥400×250, dan meminta fokus dengan `windowfocus` sebelum Return/Cross. Periksa rerun [#39015610296](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015610296). Belum ada frame game yang valid; RT-001 tetap Open / blocked.


## Handoff — capture aplikasi valid, fastboot tetap hitam (#39015722771), 2026-10-17

Rerun [#39015722771](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015722771) berhasil menangkap **jendela aplikasi yang benar**, XID decimal 2097204 / hex `0x200034`, nama `PCSX-Redux`, ukuran 1280×800. Root Xvfb 543/`0x21f` dikecualikan; pengambilan diambil dari tree X11, bukan selector `xdotool`. Lima frame (pre-input, sesudah Return/Cross, 40/65/90s) tetap hitam uniform (mean 0, stddev 0, satu warna); OCR kosong. Tidak ada register reads di VSync callback pada run ini. Port 1 Analog diset dan tombol dikirim ke jendela PCSX, tetapi layar tidak berubah. Fastboot log sekali lagi mencapai `SYSTEM.CNF`, BOOT, `EXEC:PC0(80011448)`, `Execute !`. Artifact #12095061025 berumur tiga hari; cleanup workspace sukses.
Interpretasi: berbeda dari run #390151/#390154 yang selector-nya cacat, hasil hitam pada #390157 **valid sebagai frame jendela emulator**; grafis game tetap tak tampak walau executable handoff tercapai.
Run [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) menguji backend OpenGL default vs `-softgpu` dengan Mesa llvmpipe/OpenGL 3.3, tanpa mengubah BIOS fastboot, ROM, atau input setup. Periksa frame/log akhirnya. RT-001 tetap Open / blocked.


## Handoff — OpenGL default vs soft GPU sama-sama hitam (#39015919056), 2026-10-17

Run [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) memakai fastboot BIOS, ROM, emulator AnyLinux, controller Analog dan selector X11 non-root yang sama seperti #39015722771. Satu perubahan: argumen `-softgpu` dihapus dan Mesa llvmpipe/OpenGL 3.3 digunakan. `glxinfo -B` mengonfirmasi renderer `llvmpipe (LLVM 21.1.8, 256 bits)`, versi OpenGL 3.3 Compatibility Profile Mesa. Capture jendela PCSX yang sah XID 2097204/ `0x200034` di 20s sebelum input, sesudah Return/Cross, dan 40/65/90s semuanya uniform black, mean 0/stddev 0/satu warna; OCR kosong. Tidak ada PC-register read dalam VSync callback. Log fastboot mencapai SYSTEM.CNF, BOOT, `EXEC:PC0(80011448)`, `Execute !`. Cleanup runner sukses; artifact privat #12094736241, retensi sampai 2026-10-20 08:03 UTC.
Kesimpulan: mengganti backend dari `-softgpu` ke OpenGL tidak mengubah frame; belum ada title/menu atau input game yang terbukti. Langkah berikut: pakai GDB remote untuk snapshot register PC pada beberapa waktu ketika emulator aktif, bukan membaca register dalam callback VSync dan bukan mencetak raw instruction records. RT-001 tetap Open / blocked.


## Tes aktif berikutnya — PC snapshot GDB eksternal, 2026-10-17

Run privat [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234) menggunakan fastboot BIOS dan ROM yang sama, tetapi mengambil PC dari GDB remote eksternal, bukan Lua/VSync. Ini untuk membedakan apakah CPU masih berada di loop pasca-entry atau tidak, tanpa trace instruksi mentah. Saat handoff ini ditulis, Actions masih pada step pemasangan tool; belum ada snapshot PC atau capture baru. Periksa status akhir, PC-only summary, frame/OCR, boot markers dan cleanup sebelum menyimpulkan. RT-001 tetap Open / blocked.


## Keputusan emulator untuk dilanjutkan — 2026-10-17

Pakai **PCSX-Redux AnyLinux prebuilt + OpenBIOS fastboot** sebagai emulator utama. Ini bukan klaim gameplay berhasil; ini jalur dengan kemajuan loader paling jelas dan tanpa gerbang BIOS tambahan:
- Fastboot mencatat `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, `EXEC:PC0(80011448)`, `Execute !`.
- Varian chunked belum mencapai entry marker selama window observasi.
- DuckStation hanya sampai first-run wizard yang meminta BIOS PS1/PS2 yang valid dan tidak menerima OpenBIOS yang tersedia.
- Run fastboot #39015722771/#39015919056 mengambil jendela PCSX yang benar, namun frame tetap hitam di semua interval dan sebelum/sesudah Return/Cross; OCR kosong, jadi RT-001 belum lolos.
- GDB follow-up #39016277234 selesai tetapi snapshot PC eksternal unavailable pada t20/t30/t50/t70 (exit 1) dan timeout pada t90 (exit 124); tidak berhasil mengukur perkembangan PC. Log internal GDB dibersihkan sesuai desain, tidak disimpan.
Langkah berikut: pertahankan PCSX-Redux AnyLinux dan fastboot BIOS; jangan pindah emulator tanpa hasil diskriminatif baru. Fokuskan eksperimen pada penyebab pasca-entry (output GPU/display, CPU forward progress atau interaksi BIOS/firmware) sambil mempertahankan capture non-root. **Jangan mulai menyatakan aturan gameplay sampai title/menu muncul dan tombol memiliki efek nyata.** RT-001 Open / blocked.



## Handoff runtime PCSX-Redux — 2026-10-17 (setelah RSP minimal)

Keputusan tetap PCSX-Redux AnyLinux prebuilt AppImage dari release riset + OpenBIOS fastboot + ROM/CUE privat yang hash-nya diverifikasi di runner. Jangan kembali membandingkan emulator atau mengulangi A/B backend grafis tanpa hipotesis teknis baru.

- Run [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234): GDB multiarch modern tidak cocok dengan subset protokol RSP PCSX-Redux build ini; log mengandung `Unknown GDB command` untuk paket seperti `vCont?`, `qAttached:1` dan lainnya. Jendela PCSX nyata tetap hitam.
- Run [#39017271906](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017271906): klien RSP Python minimal berhasil pada port 3333. `qSupported` dan pembacaan register individual sukses; 10 sampel PC berubah (termasuk alamat dalam rentang EXE utama dan BIOS), `BadVAddr=0`, `Cause=0x400`, target running. Tidak cukup untuk menyimpulkan title/game logic berhasil; seluruh frame tetap hitam dan input tidak menghasilkan perubahan visual.
- Langkah eksperimen terarah berikutnya ialah run [#39017636267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017636267), breakpoint entry `0x80011448` dipasang saat pause lalu GPU MMIO/DMA2 write-watchpoint. Periksa status dan log finalnya sebelum menyimpulkan apa pun.
- Semua artefak capture/diagnostik disimpan sebagai Actions artifact privat berumur 3 hari saja; jangan mengunggah ROM, BIOS, screenshot privat, memory dump atau instruction trace mentah ke repo.
- **RT-001 tetap Open / blocked** sampai title/menu Naruto dikenali dan input game yang terkontrol menghasilkan perubahan yang dapat diamati. Story Mode belum dimulai/tamat.



## Koreksi penting run GPU-watchpoint — 2026-10-17

Jangan memakai run [#39017636267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017636267) sebagai bukti hit breakpoint/watchpoint. Implementasi klien RSP sebelumnya memperlakukan paket konsol `O...` sebagai event stop; sampel PC sesudahnya berada di BIOS, bukan entry `0x80011448`. Ini false positive dari harness, bukan bukti bahwa game menyentuh GPU. Workflow diperbaiki pada commit `5055074671acf8cb2f2512182f8484dc2815552d` untuk mengabaikan paket `O`, mempertahankan paket buffered, menunggu stop packet yang sah, dan memeriksa PC tepat pada EXE entry. Rerun [#39020810743](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39020810743) sedang berjalan; periksa hasil final sebelum kesimpulan.

