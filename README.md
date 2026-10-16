# Naruto: Shinobi no Sato no Jintori Gassen — penelitian ROM

Repositori ini menyimpan catatan penelitian statis terhadap ROM PlayStation 1 Jepang **Naruto: Shinobi no Sato no Jintori Gassen**. Fokusnya adalah struktur disc/executable, pemetaan kode, aturan permainan, dan rencana verifikasi lewat debugger/emulator.

## Batasan dan keselamatan kerja

- Repo ini terpisah dari proyek Tile Duel. Jangan menggabungkan keduanya.
- ROM asli, ISO hasil ekstraksi, dump memori, save state, dan aset game berukuran besar **tidak disimpan di repo ini**.
- Temuan diberi label **terkonfirmasi dari kode**, **observasi struktur**, **sumber eksternal**, atau **belum terverifikasi**. Jangan mengubah dugaan menjadi fakta.
- **Batas agen:** repo ini khusus ChatGPT atas izin berkelanjutan pemilik untuk melakukan perubahan penelitian secara otomatis. Claude tidak diizinkan mengakses repo Naruto; Claude hanya untuk repo Tile Duel. Jangan pernah menggabungkan kedua proyek.
- Belum ada pengujian gameplay terinstrumentasi yang dilakukan dalam sesi analisis ini. Laporan emulator dari situs eksternal bukan pengganti pengujian aturan secara terkontrol.

## Mulai membaca

1. [STATUS.md](STATUS.md) — ringkasan status dan batas kepastian.
2. [docs/ROM_STRUCTURE.md](docs/ROM_STRUCTURE.md) — identitas disc, file, hash, dan executable.
3. [docs/OVERLAY_MAP.md](docs/OVERLAY_MAP.md) — loader/overlay dan apa yang masih belum dipetakan.
4. [docs/RESOURCE_CATALOG.md](docs/RESOURCE_CATALOG.md) — direktori DATA.BIN, signature resource, XASECT.BIN, serta hash file hasil ekstraksi.
5. [docs/GAME_RULES.md](docs/GAME_RULES.md) — aturan gameplay, bukti kode, contoh UI, dan sumber eksternal.
6. [docs/RUNTIME_TEST_PLAN.md](docs/RUNTIME_TEST_PLAN.md) — daftar pengujian yang dibutuhkan untuk menutup gap.
7. [docs/SOURCES.md](docs/SOURCES.md) — sumber primer dan sekunder.
8. [ANALYSIS_LOG.md](ANALYSIS_LOG.md) — catatan kronologis ringkas dari pemeriksaan yang sudah dilakukan.

## Identitas ringkas ROM

- Judul: Naruto: Shinobi no Sato no Jintori Gassen
- Platform: PlayStation (PS1), Jepang
- Serial: SLPS-03553
- Ukuran file sumber: 325.989.552 byte
- CRC32: dfe1f8b3
- SHA-256: 58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88

CRC32 cocok dengan catatan dump GameGear Archive. Lihat [sumber dan batasnya](docs/SOURCES.md).

## Titik pemulihan untuk chat baru

Mulai dari [HANDOFF_LANJUT.md](HANDOFF_LANJUT.md), lalu baca STATUS.md, docs/OVERLAY_MAP.md, docs/RESOURCE_CATALOG.md, dan ANALYSIS_LOG.md. ROM asli tidak disimpan di repo; cari file bernama `Naruto - Shinobi no Sato no Jintori Gassen (Japan).bin` di Library ChatGPT bila byte-level analysis diperlukan. Pengguna juga menyimpan salinan ROM di laptop.

## Prinsip penulisan

Alamat, ukuran, dan hash di dokumen ini adalah catatan hasil pemeriksaan yang sudah dilakukan. Setiap kesimpulan aturan yang belum dihubungkan sampai ke jalur kode lengkap dan belum diuji runtime harus tetap berstatus belum pasti.

## Emulator package record

Extracted package provenance, checksums, Library location and runtime compatibility: [docs/PCSX_REDUX_PACKAGE.md](docs/PCSX_REDUX_PACKAGE.md). The 91 MB `9c6f98a0` AppImage itself is retained in ChatGPT Library; the existing GitHub Release carries a different, pinned emulator build.
