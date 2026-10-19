## KOREKSI TERBARU — restore gagal karena field BIOS save-state; uji perbaikan antre (2026-10-19)

- [Run #39232852795](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39232852795) mengunduh artifact #12167524755 dengan sukses, kemudian emulator segfault (exit 139) sebelum menghasilkan screenshot setelah restore. Artifact kegagalannya hanya 1.190 byte; tidak berisi checkpoint baru.
- Bukti kuat mengarah ke sanitizer sebelumnya: ia menghapus field protobuf tetap `Memory.rom` (0x80000/512 KiB). Pada source pin PCSX-Redux, schema `src/core/sstate.h` mendefinisikan ROM sebagai `FixedBytes<0x00080000>`; implementasi protobuf di `src/support/protobuf.h` melakukan commit salinan FixedBytes, sementara state tanpa field itu tidak memiliki buffer valid. Ini konsisten dengan crash segera setelah `STORY_RESUME_ARTIFACT=present` dan BIOS berhasil dimuat. Belum ada bukti screenshot restore; **savestate sanitizer lama belum layak dianggap bisa dipulihkan**.
- Perbaikan pada commit `f4ea6b0169ef23c70be980602f91a65b3457c02c`: artifact tetap menyimpan savestate tanpa BIOS. Sesudah artifact diunduh, workflow memvalidasi BIOS lokal 512 KiB yang sudah diverifikasi, lalu menyisipkan kembali field `Memory.rom` hanya di runner sebelum `PCSX.loadSaveState`. File state yang sudah direkonstruksi dihapus bersama workspace; tidak diunggah ulang sebagai artifact.
- [Run #39233268705](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39233268705) menguji restore dengan rekonstruksi lokal tersebut; status terakhir antre. Periksa log `RESTORE_BIOS_REHYDRATE=PASS`, `EMULATOR_EXIT_CODE`, screenshot sesudah load, dan artifact sebelum mengklaim penyimpanan berhasil.
- Run #39205699071 tetap menyediakan artifact privat #12167524755 sampai 26 Oktober 2026 sekitar 13:47 WIB. Checkpoint menunjukkan adegan pembuka yang mulai meredup, bukan gameplay aktif. Detektor fade sudah diperbaiki dengan ambang kecerahan; itu pun belum dianggap berhasil sampai hasil run baru diperiksa.
- Story Mode belum tamat. Setiap dialog harus dilewati dengan START, bukan Circle; setiap aturan permainan harus didukung screenshot dan eksperimen yang benar-benar teramati.

---

## HASIL TERBARU — checkpoint berhasil dibuat; gameplay belum tercapai (2026-10-19)

### Run #39205699071 selesai
[Run #39205699071](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39205699071) berstatus workflow/job `success`, tetapi ini **bukan tamat Story Mode** dan tidak membuktikan sesi permainan sudah mencapai gameplay aktif.

- Artifact privat `naruto-storymode-checkpoint-private`, ID `12167524755`, berukuran 9.956.624 byte; dapat diakses sampai 26 Oktober 2026 sekitar 13:47 WIB.
- File `storymode-checkpoint.sstate` ada di artifact, ukuran 20.638.254 byte, SHA-256 `6365f18e2ad4531698976932a7d1dacc8834a47beba24e6c65d6d7d8e67a7223`.
- Log sanitizer: `STORY_SAVESTATE_SANITIZE=PASS`; 21.162.546 byte mentah menjadi 20.638.254 byte setelah field BIOS tertanam dihapus. `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`, dan pembersihan workspace berhasil.
- Ini checkpoint nyata, bukan sekadar kode penyimpanan. Namun **restore belum diuji**, jadi belum aman dinyatakan dapat digunakan sampai ada pengujian lintas-run yang sukses.

### Temuan visual yang harus diperhatikan
- Gerbang Mode Select frame 5999 dan adegan narasi frame 8999 lolos.
- Watcher mengirim START pada frame 9035 dan ulang pada frame 9110; readback hanya membuktikan tombol terbaca, bukan bahwa dialog telah maju.
- Screenshot frame 9035 dan 9065 masih menunjukkan dialog pembuka. Screenshot frame 9290 masih memperlihatkan dialog yang sama dengan layar jauh lebih gelap (rata-rata intensitas RGB sekitar 67, dibanding sekitar 146 sebelumnya). Karena itu `STORY_NON_DIALOG_STABLE=PASS frame=9285` adalah **false positive saat fade**, bukan bukti gameplay baru. Checkpoint tersimpan tepat di dekat transisi ini.
- Jangan menganggap START sudah terbukti berhasil melewati dialog ini. Lanjutkan dari checkpoint dan amati transisi; perbaiki klasifikasi layar gelap lebih dulu.

### Run pemulihan terpicu
[Run #39232852795](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39232852795) dibuat dari commit `077f576f33e8f65eea0504382383d6cc67d5cff6`, status terakhir `queued`. Run ini mencoba memuat artifact checkpoint `#39205699071` dan menambahkan syarat kecerahan rata-rata agar fade gelap tidak diklasifikasikan sebagai layar non-dialog. Tunggu status run ini, lalu periksa:
1. Apakah langkah pemulihan benar-benar mengunduh artifact dan log menunjukkan pemanggilan loader.
2. Apakah emulator tetap hidup setelah load tanpa kembali ke cold boot.
3. Screenshot terbaru setelah pemulihan—terutama apakah fade berlanjut ke adegan berikutnya atau kembali ke dialog.
4. Apakah checkpoint selanjutnya disanitasi, diunggah, dan dapat dipulihkan.

Tetap berlaku: setiap dialog dilewati dengan **START**, bukan Circle. Tidak ada aksi gameplay yang boleh ditebak sebelum layar diidentifikasi. Semua teks Jepang yang dicatat harus disertai terjemahan Bahasa Indonesia langsung di sebelahnya. Story Mode belum tamat; kontrol karakter, serangan/pertahanan, Chakra, wilayah/barrier, kartu/roulette, kondisi menang/kalah, dan perpindahan stage tetap belum diverifikasi dari gameplay aktif.

---

## TUJUAN UTAMA YANG TIDAK BOLEH TERLEWAT — tamatkan Story Mode dan pastikan aturan main (2026-10-19)

Jangan berhenti setelah emulator berhasil boot, menu terbuka, atau dialog selesai. **Tujuan akhir riset adalah memainkan Story Mode sampai layar akhir/tamat yang meyakinkan, lalu menyusun aturan main yang pasti berdasarkan pengamatan langsung dalam game dan bukti yang dapat diaudit.**

Setelah emulator stabil:
1. Lanjutkan dari checkpoint valid bila tersedia; dialog Story Mode dilewati dengan **START**, bukan Circle. Circle hanya dipakai untuk menu yang sudah terbukti memerlukannya. Setiap aksi dikirim satu per satu dan diikuti pemeriksaan screenshot.
2. Identifikasi kapan gameplay aktif dimulai, tujuan misi, kendali karakter, pergerakan, aksi/serangan/pertahanan, giliran bila berlaku, biaya aksi dan penggunaan Chakra, perebutan wilayah, barrier/penghalang, kartu, roulette, efek tiap mekanik, syarat menang/kalah, pergantian stage, serta variasi stage.
3. Mainkan setiap tahap Story Mode sampai tamat. Catat urutan tahap, keadaan awal, input, perubahan layar/status/Chakra/wilayah, hasil tiap aksi, dan bukti screenshot sebelum/sesudah. Jangan menebak jika layar hitam, crash, transisi ambigu, atau hasil input tidak jelas; rancang eksperimen pembeda satu variabel pada satu waktu.
4. Simpan tabel aturan dengan tiga label yang tidak boleh dicampur:
   - **TERVERIFIKASI** — terlihat langsung dari gameplay atau eksperimen terkontrol yang berulang, dengan screenshot/log dan kondisi uji tercatat.
   - **HIPOTESIS** — penjelasan yang masuk akal tetapi bukti belum cukup atau masih ada alternatif.
   - **BELUM DIUJI / BELUM DIKETAHUI** — mekanik atau kondisi belum berhasil dipicu/diamati.
   Tambahkan sumber bukti dan langkah pengujian yang diperlukan untuk setiap aturan.
5. Jangan menyatakan aturan sebagai pasti hanya berdasarkan nama fungsi, analisis kode, readback controller, status workflow, atau sumber luar tanpa konfirmasi gameplay. Jangan menyatakan Story Mode tamat tanpa bukti kuat dari layar akhir/ending.
6. Setelah eksperimen penting, perbarui STATUS.md, HANDOFF_LANJUT.md, HANDOFF_CHAT_BARU_2026-10-19.md, ANALYSIS_LOG.md, dan docs/RUNTIME_TEST_PLAN.md agar sesi berikutnya langsung melanjutkan dari hasil terakhir tanpa mengulang run berhasil.
7. Setiap tulisan Jepang yang diperlihatkan ke pengguna harus langsung diikuti terjemahan Bahasa Indonesia di sebelahnya dalam tanda kurung. Utamakan screenshot dari hasil eksperimen kita sendiri, bukan gambar web.

---


## Status optimasi runner — crash awal dan guard restore checkpoint (2026-10-19)

Timeout job saat ini 360 menit; SoftGPU tetap digunakan dan timeout proses emulator internal adalah 20.400 detik (5 jam 40 menit). Jalur bermain menonaktifkan raw GPU dump dan sampling GDB/RSP untuk mengurangi overhead. Namun dua run sebelumnya (`#39205262049` dan `#39205556772`) mengalami segmentation fault, masing-masing exit 139 sebelum frame 5.999; keduanya belum menghasilkan screenshot progres atau savestate valid. Run pertama sempat salah berstatus workflow success, lalu pemeriksaan exit code diperbaiki agar kegagalan emulator membuat step gagal.

Penyebab crash belum dipastikan. Panggilan getDumpFrames tanpa GPU dump sudah dihapus tetapi run berikutnya tetap crash. Commit terbaru `88d5cfa8833ef39e286431f5e8bedf2584485804` menambahkan pemeriksaan `io.open` sebelum memanggil Support.File.open/loadSaveState untuk menghindari loader native menerima file checkpoint yang tidak ada.

Run terbaru untuk menguji guard tersebut: [#39205699071](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39205699071). Pada pemeriksaan terakhir proses emulator masih berjalan; jangan klaim berhasil sampai screenshot dan log setelah run diperiksa. Save state baru boleh dipindahkan jika sanitizer mencatat PASS; artefak #12165850239 dan #12165635987 tidak berisi savestate dan tidak boleh dipakai sebagai checkpoint resume.

# Naruto: Shinobi no Sato no Jintori Gassen — penelitian ROM

Repositori ini menyimpan catatan penelitian statis terhadap ROM PlayStation 1 Jepang **Naruto: Shinobi no Sato no Jintori Gassen**. Fokusnya adalah struktur disc/executable, pemetaan kode, aturan permainan, dan rencana verifikasi lewat debugger/emulator.

## Batasan dan keselamatan kerja

- Repo ini terpisah dari proyek Tile Duel. Jangan menggabungkan keduanya.
- ROM/ISO, executable game, BIOS retail tersendiri, raw RAM/VRAM/GPU dump, dan aset game besar tidak disimpan di repo. Save kartu memori dan savestate yang telah disanitasi boleh dipindahkan hanya lewat artifact/cache/repositori **private** sesuai docs/EMULATOR_WORKFLOW.md.
- Temuan diberi label **terkonfirmasi dari kode**, **observasi struktur**, **sumber eksternal**, atau **belum terverifikasi**. Jangan mengubah dugaan menjadi fakta.
- **Batas agen:** repo ini khusus ChatGPT atas izin berkelanjutan pemilik untuk melakukan perubahan penelitian secara otomatis. Claude tidak diizinkan mengakses repo Naruto; Claude hanya untuk repo Tile Duel. Jangan pernah menggabungkan kedua proyek.
- Belum ada pengujian gameplay terinstrumentasi yang dilakukan dalam sesi analisis ini. Laporan emulator dari situs eksternal bukan pengganti pengujian aturan secara terkontrol.


## Kebijakan save/checkpoint terbaru (2026-10-19)

Atas instruksi pengguna, save kartu memori/game save dan savestate emulator yang telah disanitasi boleh ditransfer melalui private GitHub Actions artifact, Actions cache, atau repositori private untuk mempertahankan progres antar-job. Workflow saat ini menggunakan artifact private berumur 7 hari dan menyediakan input resume_run_id. Field BIOS yang tertanam harus dihapus dan keberhasilan sanitizer diverifikasi sebelum upload. Larangan atas ROM/ISO, BIOS retail tersendiri, serta raw GPU/VRAM/RAM dump tetap berlaku. Simpanan dalam cache/repositori diizinkan oleh aturan, tetapi hanya artifact yang saat ini aktif di workflow.

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

Extracted package provenance, checksums, Library location and runtime compatibility: [docs/PCSX_REDUX_PACKAGE.md](docs/PCSX_REDUX_PACKAGE.md). The preferred AnyLinux artifact ZIP is retained in ChatGPT Library; see the current package record for its path, hashes, compatibility evidence, and unverified game-boot status.


## Recommended emulator for glibc 2.41

Use the research-release `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage`, whose packaging/build smoke evidence and compatibility limits are documented in [docs/PCSX_REDUX_PACKAGE.md](docs/PCSX_REDUX_PACKAGE.md). The former 91 MB `9c6f98a0` Library AppImage required newer GLIBC symbols and has been replaced by the preferred AnyLinux artifact ZIP.
