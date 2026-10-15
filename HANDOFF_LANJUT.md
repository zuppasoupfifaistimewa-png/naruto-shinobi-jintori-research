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
