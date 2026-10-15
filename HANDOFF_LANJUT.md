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
- Pengguna menyatakan memiliki salinan di laptop; salinan ini menjadi cadangan tambahan.
- ROM tidak disimpan di repo. Pada chat baru, cari kembali item Library dengan nama persis tersebut jika dibutuhkan dan verifikasi hash sebelum analisis byte-level. Akses ke Library dan koneksi GitHub bergantung pada alat/konteks yang tersedia pada sesi baru; jangan berasumsi berkas otomatis muncul pada filesystem baru.

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

## Berikutnya

1. Reverse-engineer header PK02 dan subformat BIN0/TPK0 menggunakan banyak sampel; catat header, panjang terkompresi/tidak, batas, dan confidence tanpa mengasumsikan makna field.
2. Telusuri semua pemanggil yang mengonsumsi XASECT.BIN; identifikasi arti field kedua dan cek hubungannya dengan DATA2.BIN.
3. Petakan resource scene dan resource yang benar-benar dimuat sebagai kode: offset/LBN, ukuran, alamat RAM, entry point, lifecycle, relokasi.
4. Sesudah itu telusuri call chain aturan gameplay dan transaksi Chakra.
5. Jalankan pengujian terkontrol dengan debugger PS1 bila tersedia dan rekam hasil yang dapat direproduksi.

Dokumen penelitian terkait: [STATUS.md](STATUS.md), [docs/OVERLAY_MAP.md](docs/OVERLAY_MAP.md), [docs/RESOURCE_CATALOG.md](docs/RESOURCE_CATALOG.md), [docs/ROM_STRUCTURE.md](docs/ROM_STRUCTURE.md), [docs/GAME_RULES.md](docs/GAME_RULES.md), [ANALYSIS_LOG.md](ANALYSIS_LOG.md).
