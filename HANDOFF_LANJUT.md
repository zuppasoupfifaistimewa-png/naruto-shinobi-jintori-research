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

Hash file hasil ekstraksi lokal dicatat di `docs/ROM_STRUCTURE.md` dan `docs/RESOURCE_CATALOG.md`. Folder hasil ekstraksi yang ada pada lingkungan kerja saat ini tidak dijamin tersedia pada chat baru; ekstrak ulang hanya dari ROM terverifikasi jika diperlukan.

## Urutan baca saat membuka chat baru

1. Baca file ini.
2. Baca `STATUS.md`.
3. Baca `docs/OVERLAY_MAP.md`.
4. Baca `docs/RESOURCE_CATALOG.md`.
5. Baca `docs/ROM_STRUCTURE.md`, `docs/GAME_RULES.md`, dan bagian terbaru `ANALYSIS_LOG.md`.
6. Baca `docs/RUNTIME_TEST_PLAN.md` sebelum menyusun eksperimen runtime.

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


## Aturan persistensi kuota — wajib dibaca

Pengguna memiliki kuota internet sangat terbatas sehingga upload ulang ROM/ISO sekitar 300 MB tidak realistis. Jangan mengandalkan ROM laptop pengguna; jangan meminta upload ulang untuk meneruskan riset. Mulai dari file ekstraksi yang disimpan di Library pada /Naruto Research Files/. Gunakan Files untuk menemukan dan mematerialisasikan file saat diperlukan, lalu cocokkan hash terhadap docs/ROM_STRUCTURE.md dan docs/RESOURCE_CATALOG.md. File Library tidak otomatis muncul di filesystem chat baru. Jika file yang diperlukan tidak dapat diakses, dokumentasikan kendala dan lanjutkan analisis dari dokumentasi/repo; minta transfer hanya bila pengguna secara eksplisit menawarkan alternatif.

## Pembaruan aturan gameplay statis — 2026-10-15

- Tabel konfigurasi executable pada alamat RAM 0x80057798 memakai stride 0x54; pasangan Chakra awal/target mencakup 1500/3000, 2000/4000, 2500/5000, 3000/6000 serta dua record 600/0 yang kondisi pemilihannya belum diketahui.
- Tabel lain pada 0x80064918 (stride 0x30) menunjukkan pasangan 1500/3000 pada sekurangnya 13 record awal nonnol yang diperiksa.
- Field +0x04 digunakan sebagai Chakra awal; field +0x08 sebagai target pada cabang kemenangan yang ditelusuri; field +0x0C (400/0) belum dipahami.
- Label lama 0x800EC200 (target Chakra) dan sekitar 0x800F70D0 (aritmetika Chakra) ditarik kembali karena base/identitas modul belum diverifikasi.
- Tidak ada uji runtime emulator/debugger yang diselesaikan. Biaya, income, battle, roulette, dan semua efek kartu tetap terbuka.
