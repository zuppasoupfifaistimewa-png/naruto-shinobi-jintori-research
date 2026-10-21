## HASIL TERBARU — Circle timeline probe selesai (21 Oktober 2026, 08:01 WIB)

- Run [#39524697802](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39524697802) berstatus `success`, mulai 08:00:08 WIB dan selesai 08:01:54 WIB (durasi 1 menit 46 detik). Tidak ada Actions run aktif yang perlu ditunggu untuk eksperimen ini.
- Artifact privat [#12311254886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39524697802) berisi screenshot/log lima cabang hingga frame 90. Digest ZIP: `sha256:b121b6df1037a4877f688a450b841cd9e1112fe753625b7132548468117269f4`; kedaluwarsa 4 November 2026 sekitar 08:01:48 WIB.
- Semua cabang (NONE, CIRCLE_TAP_EARLY, CIRCLE_HOLD30, CIRCLE_TAP_LATE, LEFT_TAP_EARLY) sukses memuat checkpoint, menyelesaikan capture sampai frame 90, dan mencatat marker cabang selesai. Checkpoint induk 21.162.405 byte, SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`; laporan memastikan `CIRCLE_TIMELINE_PARENT_STATE_MUTATION=NO`. AppImage patched digunakan ulang tanpa rebuild, SHA-256 `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`.
- Temuan visual: cabang Circle yang ditekan pada frame 30 identik dengan baseline sampai frame 35, berbeda mulai frame 37, dan tetap sangat berbeda pada frame 90. Menahan Circle 30 frame menghasilkan gambar identik dengan tap singkat di semua titik yang diukur. Circle yang ditekan pada frame 60 dan tombol LEFT pada frame 30 menghasilkan gambar identik dengan baseline sampai frame 90.
- Kesimpulan yang dibolehkan: Circle awal menghasilkan respons visual yang berbeda pada timing ini. **Fungsi game yang tepat belum diketahui**; perubahan scene/camera juga terjadi tanpa input di baseline. Tombol kiri yang tidak mengubah gambar pada timing ini tidak membuktikan bahwa arah tidak bekerja dalam konteks lain.
- Rincian metrik, hash, batas interpretasi, dan rencana lanjutan: [docs/STORYMODE_CIRCLE_TIMELINE_2026-10-21.md](docs/STORYMODE_CIRCLE_TIMELINE_2026-10-21.md).
- Langkah berikut: buat cabang baru dari checkpoint parent yang sama dan perpanjang observasi untuk NONE, Circle awal, dan START awal melewati frame 90 (target sekurangnya frame 180), dengan screenshot rapat di sekitar perubahan frame 37 serta setelah frame 90. Jangan menimpa parent; jangan menamai aksi Circle atau menyatakan Story Mode maju/tamat tanpa bukti runtime.
- **Status keseluruhan:** checkpoint patched dapat dipulihkan dan uji kontrol ini selesai; progres Story Mode kanonis, save/load Memory Card in-game, dan tamat Story Mode belum terbukti. ROM, BIOS, savestate, dan Memory Card tetap di luar Git.

---

---

## Koreksi hasil run Circle timeline — 21 Oktober 2026

- Run [#39523066920](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39523066920) selesai `failure` pada 21 Oktober 2026 pukul 07:55:38 WIB; mulai 07:43:47 WIB; durasi 11 menit 51 detik. Kegagalan ada pada langkah perbandingan, bukan saat unduh aset atau pemulihan checkpoint. Batas workflow 35 menit tidak tercapai.
- Checkpoint induk tervalidasi ulang: 21.162.405 byte, SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`. Binary patched yang digunakan kembali SHA-256 `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`. Semua cabang memuat checkpoint dan log mencatat `CIRCLE_TIMELINE_LOAD_EVENT=PASS` dan `CIRCLE_TIMELINE_LOAD_RETURNED=1`.
- Artifak privat [#12312483553](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39523066920) diunduh dan screenshot diperiksa. Semua lima cabang berhenti pada screenshot frame 150 tanpa `CIRCLE_TIMELINE_BRANCH_DONE`; tidak ada screenshot frame 180/240/300. Langkah menjalankan tiap cabang memberi batas timeout 120 detik, sehingga kegagalan kemungkinan adalah batas per-cabang sebelum frame 300. Ini keterbatasan harness; tidak menunjukkan kegagalan memulihkan checkpoint.
- Temuan parsial dari screenshot sinkron per frame:
  - `NONE` adalah baseline deterministik.
  - `CIRCLE_TAP_EARLY`: tombol Circle ditekan pada frame 30; screenshot sama dengan baseline pada frame 20–35, lalu berbeda mulai frame 37 (mean absolute RGB difference 17.547; pixel identik 15.772%). Pada frame 150 tampak transisi visual/figur karakter di jalur petak, berbeda dengan baseline. Ini **bukti awal input Circle memicu respons visual pada konteks/timing itu**, tetapi aksi game yang tepat (memilih, menggerakkan, atau konfirmasi) belum dipastikan.
  - `CIRCLE_HOLD30`: pola screenshot identik dengan tap awal pada seluruh frame yang tersedia; belum ada bukti menahan Circle memberi efek tambahan.
  - `CIRCLE_TAP_LATE`: menekan Circle pada frame 90 tidak mengubah screenshot terhadap baseline sampai frame 150.
  - `LEFT_TAP_EARLY`: screenshot identik dengan baseline sampai frame 150.
- Pembacaan tombol `pad.getButton` benar pada press/release, tetapi itu sendiri hanya memverifikasi sisi emulator; simpulan gameplay harus didasarkan pada respons visual di atas.
- Uji berikutnya dipersingkat untuk menyelesaikan cabang sampai frame 90, dengan batas timeout per-cabang yang sesuai. Pakai lagi checkpoint induk dan AppImage patched yang sama, tanpa build ulang; jangan menyentuh atau menimpa checkpoint induk.
- **Status:** checkpoint bisa dipulihkan; ada indikasi Circle awal menimbulkan transisi visual; kontrol gerakan/aksi belum teridentifikasi penuh, Story Mode belum dinyatakan berlanjut secara kanonis atau tamat, dan Memory Card save/load in-game belum terverifikasi.

---

## Hasil terbaru — uji respons tombol dan probe waktu Circle (21 Oktober 2026)

- Run [#39513285641](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39513285641) selesai `success` setelah 39 menit 39 detik (21 Oktober 2026, 06:10–06:50 WIB). Artifact privat [#12308661246](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39513285641) diunduh dan screenshot/log diperiksa.
- Kesepuluh cabang kontrol (NONE, START, CIRCLE, CROSS, TRIANGLE, SQUARE, UP, DOWN, LEFT, RIGHT) berhasil memuat checkpoint yang sama, mencatat event `ExecutionFlow::SaveStateLoaded`, dan mengonfirmasi pembacaan tombol tekan/lepas. Semua kontrol selain CIRCLE memiliki screenshot akhir identik dengan cabang NONE pada frame yang dibandingkan. CIRCLE berbeda nyata: mean absolute RGB difference `52.71042`, pixel identik `7.4453%`.
- Ini **bukan bukti final makna tombol Circle**: screenshot NONE sendiri berubah antara frame 20 dan frame 90 karena scene terus beranimasi. Hasil tersebut hanya membuktikan Circle berasosiasi dengan respons visual yang berbeda; perlu kontrol timing lebih rapat untuk memisahkan respons input dari animasi kamera/scene.
- Binary hasil rebuild dengan source base `0c3572c3db75f97542001e453ae80ba8c3f8acba` dan patch SPU/ADPCM dua-file yang sama diunggah sebagai bagian artifact privat #12308661246. SHA-256 AppImage: `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`; patch SHA-256 `9588ee95651c9841c4bc5e25bd34b4be41ac100a955511817f8a92901245b7b5`; applied diff SHA-256 `754d471acb8b7c468251d20ef19ac7fe8a4f66ec0d7f67807d07ac7aa9b0b46c`.
- Workflow [.github/workflows/naruto-storymode-circle-timeline.yml](.github/workflows/naruto-storymode-circle-timeline.yml) memakai ulang binary tersebut tanpa build ulang dan mengambil snapshot berturut-turut untuk NONE, CIRCLE tap lebih awal, Circle ditahan 30 frame, Circle tap terlambat, dan LEFT tap. Setiap cabang memuat checkpoint yang sama di proses baru dan menggunakan salinan Memory Card sementara; checkpoint induk tidak ditimpa.
- Run baru [#39523066920](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39523066920) sedang `in_progress`; saat pemeriksaan terakhir runner berada di tahap inisialisasi container. Workflow memiliki batas maksimum 35 menit sejak mulai 07:43:47 WIB, jadi batas maksimum waktunya sekitar **08:18:47 WIB pada 21 Oktober 2026**. Perkiraan praktis belum pasti; karena tidak ada rebuild emulator, target kerja sekitar 5–15 menit setelah runner mulai aktif, selama unduhan/runner tidak macet.
- **Story Mode belum dinyatakan berlanjut atau tamat.** Menunggu hasil time-series agar respons Circle bisa ditafsirkan dengan lebih hati-hati. Save/load Memory Card dalam game juga tetap belum diverifikasi. ROM, BIOS, savestate, dan isi Memory Card tetap di luar Git.

---

## Operasional terbaru — checkpoint patched diverifikasi, kontrol gameplay sedang diprobe (21 Oktober 2026)

- Artefak privat [#12268621845 dari run #39426068247](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39426068247) berhasil diunduh langsung. ZIP 2.367.857 byte; SHA-256 ZIP `dc701311a82855c61a95b37a99fd86e2580b0a475682cb7ad8fa9d5a33737358`, cocok dengan digest artifact GitHub.
- Checkpoint lanjutan diekstrak dari `captures/storymode-checkpoint-next.raw.sstate`: 21.162.405 byte, SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`; cocok dengan `probe-manifest.txt`. Screenshot checkpoint menunjukkan papan permainan. Manifest juga mengonfirmasi probe lama tidak memberi input controller (`PROBE_CONTROLLER_INPUT=none`).
- Artifact lama tidak berisi binary AppImage—hanya checkpoint, screenshot, log, schema, patch-diff, dan build manifest. Karena runner lama sudah dibersihkan, workflow baru akan membangun ulang PCSX-Redux dari base `0c3572c3db75f97542001e453ae80ba8c3f8acba` dengan patch dua-file SPU/ADPCM yang sama.
- Workflow [.github/workflows/naruto-storymode-control-probe.yml](.github/workflows/naruto-storymode-control-probe.yml) ditambahkan pada commit [`fde550b`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/fde550b37102d6bbf3890938cca03ce703718d38). Trigger sekali pakai dibuat lalu dihapus; file marker tidak tertinggal di repo.
- Run [#39513285641](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39513285641) sedang berjalan. Rencana probe: pada proses baru, masing-masing cabang memuat ulang checkpoint induk yang sama dan menguji satu input saja (NONE/START/CIRCLE/CROSS/TRIANGLE/SQUARE/UP/DOWN/LEFT/RIGHT), mengambil screenshot sebelum dan sesudah, lalu membandingkan hasil. Tidak ada cabang yang menimpa checkpoint induk; masing-masing memakai salinan Memory Card sementara.
- Run [#39513291249](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39513291249) berstatus `skipped` karena marker dihapus dan bukan eksperimen gameplay.
- **Belum ada input gameplay yang diterapkan sebagai progres Story Mode kanonis.** Tunggu hasil screenshot per tombol sebelum memilih tindakan berikutnya. Game belum terbukti tamat; save/load Memory Card in-game tetap belum terverifikasi. ROM, BIOS, savestate, dan Memory Card tidak dimasukkan ke Git.

---

# HANDOFF TERBARU — 20 Oktober 2026: probe SPU/ADPCM sedang berjalan

## Run aktif dan hasil yang sudah diketahui

- [Run #39373493482](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39373493482) terkonfirmasi dibuat pada event `push`, dari commit marker [f1a0d7f0](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/f1a0d7f0c2a574c07b875e38a3c6f7ffa561daa6). Pada pemeriksaan terbaru job masih `in_progress`: unduhan checkpoint dan Memory Card, validasi raw/staging, verifikasi aset runtime, serta schema API pada binary pinned semuanya sukses; build emulator varian sedang berjalan. Artifact final dan hasil restore belum tersedia. Jangan menyatakan probe atau restore PASS sebelum log/manifest final tersedia.
- [Run #39372712212](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39372712212) adalah percobaan pemicu terdahulu. Log membuktikan checkpoint berhasil diunduh, tetapi unduhan Memory Card gagal `Not Found` karena `run-id: ${{ inputs.source_run_id }}` kosong pada event push. Workflow tidak mencapai staging/schema/build/loader. Perbaikan fallback ada di [commit b44efaab](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/b44efaab64716db2c018212587989103c9ffa83b), diterapkan untuk kedua langkah unduh.
- [Run manual #39372202653](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39372202653) gagal terpisah pada SDL display preflight; Xvfb dan `XDG_RUNTIME_DIR` sudah ditambahkan sebelum run terbaru. Kegagalan preflight bukan bukti state rusak.
- Workflow sementara dibatasi hanya pada marker path, lalu trigger dibuang ([commit e925b438](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/e925b438b69bac29003dc73f0908bbc1dd0eae9a)) dan marker dihapus ([commit 192bf21](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/192bf21d05d1dfc559110d66080e25940354eb29)). Branch main bersih dari trigger/marker sementara; workflow kembali manual-only dengan perbaikan fallback.

## Checkpoint dan kriteria lanjut

Raw source run `39262213468`: frame 10055; ukuran 21.163.286 byte; SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`; screenshot SHA-256 `101b94a4d171d228e0224948872b65b88bf84fd0d92dc8ddd0b6cfeb21f790a8`. Tidak boleh diubah atau disanitasi.

Periksa run #39373493482 untuk semua gerbang: hash source/staging identik, schema API tanpa loader berhasil, schema pinned dan varian konsisten, patch dua-file SPU satu-satunya perubahan, event `ExecutionFlow::SaveStateLoaded`, loader kembali normal, sedikitnya 180 VSync, screenshot cocok, checkpoint lanjutan dibuat, lalu checkpoint dimuat di proses emulator baru dengan gerbang setara. Simpan log, manifest, screenshot, hash, dan alasan setiap kegagalan. Jika ada gerbang gagal, diagnosa dan perbaiki secara minimal sebelum mencoba lagi.

Story Mode belum terbukti dipulihkan lintas-proses atau tamat. Aturan gameplay masih harus dibuktikan dari observasi langsung; save/load Memory Card in-game belum diverifikasi. Tidak ada ROM, BIOS, savestate, atau Memory Card yang boleh masuk Git.

---

# HANDOFF TAMBAHAN — perbandingan struktural raw savestate (20 Oktober 2026)

**Dokumen hasil analisis read-only:** [docs/SAVESTATE_STRUCTURAL_COMPARISON_2026-10-20.md](docs/SAVESTATE_STRUCTURAL_COMPARISON_2026-10-20.md) — commit [dbe20783f90971f69a1abc56fb492da736882661](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/dbe20783f90971f69a1abc56fb492da736882661).

- Pembanding raw yang berhasil lintas-run masih hanya checkpoint boot dari [Run A #39255438457](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255438457) ke [Run B #39255549341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255549341). Belum ditemukan bukti raw checkpoint Story Mode pulih lintas-run.
- Raw boot: 21.124.144 byte, SHA-256 `a4672dd49fbfa76ef60de410c50460d77e115181fc3e205a215ab9f5f1e601d7`. Raw board frame 10055 dari [Run #39262213468](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468): 21.163.286 byte, SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`.
- Diff read-only: header `PCSX-Redux SaveState v4` sama; raw board +39.142 byte. Top-level field `6` berubah ukuran paling besar (+38.943); field ini berisi subfield/record yang berubah lebih kaya pada checkpoint board. Nama semantik field masih harus dipastikan dari schema build yang sama; jangan klaim field tersebut penyebab crash sebelum bukti.
- BIOS pada kedua state raw sama byte-per-byte (512 KiB, SHA-256 `5e84a94818cf5282f4217591fefd88be36b9b174b3cc7cb0bcd75199beb450f1`). Varian tersanitasi dari artifact board menghapus hanya field BIOS di top-level field `3`: ukuran menjadi 20.638.994 byte, SHA-256 `b94e61502b63a81107f48153932ccbef21bede8c7f53d4b01e6e013ecb8979eb`. Payload top-level field `6` sama persis antara raw board dan varian tersanitasi.
- Konsekuensi: jangan ulangi receiver raw board tanpa perubahan diagnosis dan jangan langsung menguji sanitizer sebagai pengganti. Eksperimen berikutnya: verifikasi dahulu apakah build emulator yang sama menyediakan API Lua `PCSX.getSaveStateProtoSchema()`. Jika tersedia, ambil schema tanpa memanggil loader; jika tidak, cari sumber schema read-only yang cocok dengan build tersebut. Petakan field yang berubah (utama field `6` dan subfield yang hanya muncul di board). Setelah itu, kalau ada subfield spesifik yang layak diuji, buat varian terpisah dengan satu transformasi yang terukur serta manifest parent hash/transformasi/hash varian. Uji diagnostik harus berhenti setelah gerbang restore; jangan lanjutkan gameplay dari varian eksperimen.
- Pemeriksaan tidak mengubah savestate sumber, tidak mengubah hash artifact, tidak menjalankan ulang source 90 menit, dan tidak menaruh ROM/BIOS/state/Memory Card ke Git. Tidak ada Actions run aktif saat diperiksa. Game masih belum terbukti tamat; mekanik gameplay belum terverifikasi.

---

# HANDOFF TERBARU — 20 Oktober 2026: GDB membuktikan SIGSEGV di dalam raw savestate loader

## Fakta diagnostik terbaru

- Source checkpoint tetap dari run [#39262213468](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468), frame 10055 di board screen. Ukuran 21.163.286 byte; SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`. Screenshot sumber 320×240, SHA-256 `101b94a4d171d228e0224948872b65b88bf84fd0d92dc8ddd0b6cfeb21f790a8`.
- Receiver terbaru [#39314115221](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39314115221) memvalidasi dan menyalin checkpoint **tanpa perubahan byte**: `STORY_RAW_SOURCE_VALIDATION=PASS` dan `STORY_RAW_STATE_STAGED_UNCHANGED=PASS`, keduanya melaporkan ukuran/hash yang sama.
- Phase log yang di-flush menunjukkan `LUA_SCRIPT_START` → `FIRST_GPU_VSYNC_ENTERED` → `NEXT_TICK_ENTERED` → `SAVESTATE_FILE_OPEN_OK` → `PCSX_LOADSAVESTATE_BEGIN`. GDB kemudian menangkap SIGSEGV pada thread `pcsx-redux` selama panggilan loader; `PCSX_LOADSAVESTATE_PCALL_RETURNED` dan event `ExecutionFlow::SaveStateLoaded` tidak muncul.
- Temuan native pada artifact diagnostik privat #12216519993 dari [run #39314115221](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39314115221): PC `0x7ffff0fad6d0` dipetakan ke `AppDir/shared/bin/pcsx-redux`; disassembly berhenti di `movzbl (%rsi),%ecx`; RSI=`0xffffffffd736a15f`, alamat tidak valid/tidak dipetakan. GDB merekam 72 frame, tetapi fungsi tidak bernama karena executable ter-strip. Kesimpulan yang didukung: dereferensi alamat tidak valid di jalur native selama pemuatan savestate. Fungsi penyebab dan alasan pointer tidak valid belum dapat dipastikan; jangan menyatakan state rusak tanpa pembanding yang lebih kuat.
- Akibatnya screenshot pascarestore gagal karena emulator keluar sebelum capture; tidak ada bukti ≥180 VSync maupun checkpoint lanjutan. **Raw Story Mode restore belum berhasil; progres belum terbukti aman dipulihkan.** Run sumber 90 menit tidak dijalankan ulang, dan checkpoint sumber tidak dimodifikasi.
- Run [#39313917935](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39313917935) juga menangkap SIGSEGV di dalam loader. #39313679196 bukan stack trace emulator yang valid (GDB mengikuti helper `mkdir`); #39313520942 gagal ketika path staging Lua salah; #39313409415 gagal mengunduh artifact karena run-id pada action belum memakai variabel `SOURCE_RUN_ID`. Kedua masalah itu telah diperbaiki.
- Workflow receiver saat ini tidak mempunyai pemicu `push` sementara. Diagnostik permanen di `.github/workflows/naruto-raw-storymode-restore.yml` meliputi GDB dengan `follow-fork-mode parent`, penanda fase Lua, register, disassembly, pencarian simbol, dan memory mappings. Commit terakhir yang menghapus pemicu sementara: [68639076b5b6a971d62bd8a5a73c60a9ba406d11](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/68639076b5b6a971d62bd8a5a73c60a9ba406d11). Kedua langkah unduhan artifact kini memakai run ID yang diselesaikan dari variabel `SOURCE_RUN_ID`.
- Jangan sentuh repositori Tile Duel. Jangan tambahkan ROM, BIOS, raw savestate, atau Memory Card ke Git. Memory Card kandidat 131.072 byte masih berstatus `UNVERIFIED_REQUIRES_IN_GAME_SAVE_AND_RELOAD`. Game belum terbukti tamat; dialog Story Mode dilewati dengan START, bukan Circle.

## Langkah berikutnya

1. Jangan langsung mengulangi receiver berkali-kali dengan setup yang identik: gejala native dan alamat fault kini terdokumentasi. Analisis read-only perbedaan raw checkpoint board-screen dengan raw boot checkpoint yang pernah pulih lintas-run, terutama format/isi state, tanpa mentransformasi checkpoint sumber.
2. Bila melakukan kontrol eksperimen selanjutnya, gunakan checkpoint sumber #39262213468 dan validasi hash/ukuran sebelum serta sesudah staging; jangan jalankan ulang sumber 90 menit. Bedakan startup, fase sebelum loader, dan di dalam `PCSX.loadSaveState()` dengan phase log/GDB.
3. Hanya tandai restore PASS setelah event `ExecutionFlow::SaveStateLoaded`, panggilan loader kembali normal, ≥180 VSync pascarestore, screenshot sama/masuk akal terhadap source, dan checkpoint lanjutan benar-benar diunggah. Jika salah satu hilang, status tetap gagal/belum terverifikasi.

---

# HANDOFF TERBARU — 20 Oktober 2026: receiver raw Story Mode crash saat startup

## Hasil terbaru untuk dilanjutkan

- Source run [#39262213468](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468) tetap menyediakan raw savestate frame 10055 dari layar papan permainan: ukuran 21.163.286 byte, SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d. Screenshot sumber 320×240, SHA-256 101b94a4d171d228e0224948872b65b88bf84fd0d92dc8ddd0b6cfeb21f790a8. Jangan transformasikan atau timpa file sumber.
- Receiver [#39312125361](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39312125361) benar-benar berjalan pada runner baru. Validasi manifest/hash/screenshot PASS; pesan `STORY_RAW_STATE_STAGED_UNCHANGED=PASS` memastikan byte di staging sama dengan raw source. Emulator, game, BIOS dan memory card berhasil diunduh/diverifikasi.
- **Receiver gagal exit 139 / segmentation fault** beberapa detik setelah emulator mulai. Log sampai pada retail BIOS SCPH-7502, CD ID SLPS03553, executable SLPS_035.53;1, `KERNEL SETUP!`, `BIOS Trace1: 0x07`. Tidak ada `STORY_SAVESTATE_RESTORE_PAUSE_REQUESTED`, `ExecutionFlow::SaveStateLoaded`, `STORY_SAVESTATE_LOAD_CALL_RETURNED=1`, atau screenshot immediate restore. Karena log load-event tidak ada, ini belum memastikan apakah save-state deserialization sudah dimulai atau crash terjadi pada startup sebelum callback. Jangan menyatakan raw file korup hanya dari hasil ini.
- Artifact privat diagnostic #12216866405 sudah diunduh dan diperiksa. File penting: `pcsx.stdout.txt`, `pcsx.log.txt`, `important-log-lines.txt`, `story-dialog-watch-summary.txt`, `storymode-restore-comparison.txt`, manifest (state baru = 0), dan screenshot sumber. Tidak ada checkpoint lanjutan. Artifact Memory Card #12216691714 masih status kandidat; in-game save/load belum terbukti.
- Perbaikan yang sudah permanen: kedua source artifact diunduh ke `$WORK/source-artifact` dan `$WORK/source-card`; runtime dependencies termasuk `python3-pil` dipasang **sebelum** source screenshot validator. Pemicu push khusus yang digunakan satu kali untuk meluncurkan receiver telah dihapus kembali di commit [d0b24b64fcc3c6d8d309252a53d0e291d1f2b36f](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/d0b24b64fcc3c6d8d309252a53d0e291d1f2b36f). Run #39311930637 adalah percobaan terdahulu yang masih gagal karena Pillow belum tersedia sebelum validator, bukan uji restore yang berhasil.
- STATUS.md diperbarui dengan hasil dan tautan baru pada commit [4058fcadbd0b7f16d4f62900ce307a08e04d89eb](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/4058fcadbd0b7f16d4f62900ce307a08e04d89eb).

## Langkah diagnostik selanjutnya

1. Perbarui receiver workflow `.github/workflows/naruto-raw-storymode-restore.yml` untuk memasang GDB lalu jalankan AppRun melalui `gdb --batch` dengan `thread apply all bt` saat SIGSEGV. Tambahkan pesan debug Lua yang di-flush sebelum dan sesudah `PCSX.loadSaveState()` dan tepat pada awal `GPU::Vsync` callback.
2. Picu receiver lagi dari sumber yang sama: run ID **39262213468**. Workflow_dispatch biasa tersedia di halaman [receiver workflow](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/workflows/naruto-raw-storymode-restore.yml), gunakan branch main dan `source_run_id=39262213468`. Koneksi di sesi ini sebelumnya tidak punya aksi dispatch langsung, jadi pemicu satu-kali pernah dilakukan melalui commit push yang digate pesan pasti; bila menggunakan cara itu lagi, hapus pemicu setelah run tercipta.
3. Raw checkpoint hanya ditransfer melalui artifact privat, tanpa sanitasi/rehidrasi; tidak ada raw state atau Memory Card di Git. Pertahankan ROM/BIOS privat. Jangan jalankan ulang sumber 90 menit.
4. Hanya beri status restore PASS bila hash cocok, event `ExecutionFlow::SaveStateLoaded` ada, loader kembali, ≥180 VSync pascarestore, screenshot source/pulih cocok, dan checkpoint lanjutan dihasilkan.

**Kondisi game:** visual telah mencapai papan permainan pada frame 10055, tetapi belum ada bukti raw checkpoint tersebut bisa diload di runner lain. Game belum tamat; aturan kontrol karakter dan mekanik belum terverifikasi. Dialog dilewati dengan START, bukan Circle; jangan menambah input tanpa identifikasi screenshot.

---

# PEMBARUAN HANDOFF — 20 Oktober 2026: checkpoint board-screen dan fix receiver

## Fakta terbaru yang sudah diperiksa

- Run sumber [#39262213468](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468) berakhir sukses. Dialog gate PASS pada frame 8999; setelah watcher meminta START, frame 10055 memperlihatkan scene papan dari sudut atas, tile bernomor, token biru/merah, dan UI karakter/statistik. Ini terverifikasi sebagai kemajuan visual keluar dari narasi pembuka ke papan permainan, tetapi kontrol, mekanik, menang/kalah, stage lanjutan, dan tamat belum terbukti.
- Artifact privat #12196796917 memuat raw checkpoint yang dihasilkan langsung oleh PCSX.createSaveState() di frame 10055, reason=stable_non_dialog. Ukuran 21.163.286 byte; SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d. Hash dan byte diverifikasi dengan membaca file di ZIP, serta cocok dengan manifest.
- Screenshot sumber frame 10055: 320×240; SHA-256 101b94a4d171d228e0224948872b65b88bf84fd0d92dc8ddd0b6cfeb21f790a8. Ini screenshot aktual dari artifact riset, bukan gambar web.
- Receiver [#39274593965](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39274593965) gagal dua kali di validasi sumber sebelum emulator mulai, exit 41, error Missing raw-state manifest. Penyebab terbukti adalah folder tidak cocok: download artifact memakai runner.temp, sementara WORK menunjuk /tmp/naruto-storymode-raw-resume. Jadi hasil ini **bukan** bukti bahwa savestate Story Mode crash atau tidak dapat di-restore; loader tidak pernah dipanggil.
- Fix telah di-commit ke main pada [4b0bbe0d838e42a688e907372dcb8682fa80c967](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/4b0bbe0d838e42a688e907372dcb8682fa80c967): download kedua artifact dipindahkan ke WORK. Retry attempt 2 pada run lama menggunakan revisi workflow lama dan mengulang error yang sama; fix belum diuji.
- Untuk menjalankan kode yang telah diperbaiki, buka [workflow Naruto raw Story Mode restore and continuation](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/workflows/naruto-raw-storymode-restore.yml), klik **Run workflow** di branch main, masukkan source_run_id **39262213468**, lalu pantau run baru. Wajib mengonfirmasi validasi SHA/ukuran, SaveStateLoaded, screenshot post-restore yang cocok dengan sumber, ≥180 VSync, dan checkpoint lanjutan.
- Memory Card artifact #12196517326 adalah file 131.072 byte, SHA-256 ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5, tetapi tetap UNVERIFIED_REQUIRES_IN_GAME_SAVE_AND_RELOAD. Jangan mengklaim save/load game telah berhasil.
- Workflow fix dan catatan status terbaru ada di main; STATUS.md juga telah diperbarui di commit 7a7ff914c1803db6557bbf360f4656b8cac71505.

**Prioritas berikutnya:** jalankan receiver dari UI GitHub dengan source_run_id=39262213468. Jangan menjalankan ulang run sumber 90 menit, jangan mengubah raw state, jangan mengunggah ROM/BIOS/savestate ke Git, jangan sentuh repo Tile Duel. Jika restore lolos, lanjutkan gameplay selangkah demi selangkah dan ambil raw checkpoint baru setelah progres nyata.

---

# HANDOFF TERBARU — RAW SAVESTATE ANTAR-RUNNER (19 Oktober 2026)

## Snapshot eksperimen terkini

- **Jangan batalkan:** [run utama #39262213468](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468), commit `e396eac00631001b7a0e68d7701c70aec10dec19`, status terakhir `in_progress`; verifikasi aset selesai, emulator sedang berjalan, artifact belum tersedia.
- Run #39261524544 gagal di shell karena `raw_resume_verify: unbound variable` sebelum emulator mulai. Ini kesalahan orchestration, bukan tes savestate; tak ada checkpoint baru. Diperbaiki di commit `e396eac...`; jangan mengulang run gagal ini.
- Workflow utama kini memberi waktu maksimal 90 menit ke proses emulator (job 100 menit), menyimpan salinan byte-asli hasil `PCSX.createSaveState()` sebelum langkah sanitizer diagnostik, menyiapkan manifest ukuran/SHA-256 dan screenshot checkpoint yang sama, serta retensi artifact privat 14 hari. Jangan edit file workflow utama saat runner aktif.
- Workflow penerima `naruto-raw-storymode-restore.yml` (commit terakhir `ddcf1e0...`) otomatis berjalan pada event `workflow_run` setelah workflow utama selesai. Ia melakukan validasi ketat pada manifest/state/screenshot, menerima hanya raw state, menyalinnya tanpa transformasi, memeriksa ukuran/hash, memuat pada proses emulator baru tanpa sanitizer/rehidrasi BIOS, menangkap `ExecutionFlow::SaveStateLoaded`, menuntut ≥180 VSync, dan membandingkan screenshot pascarestore dengan screenshot dari safe point sumber. Hanya jika tes itu lulus emulator diizinkan melanjutkan.
- Checkpoint sumber awal harus berupa layar stabil pascadialog dengan `reason=stable_non_dialog`, frame ≥9000, dan `STORY_DIALOG_VISUAL_GATE=PASS`. Sesudah raw restore valid, jalur penerima menunggu setidaknya 600 VSync sebelum memutuskan titik layar stabil berikutnya, membuat raw checkpoint baru, dan mengunggah state/manifest/screenshot untuk handoff berikutnya. Jika gate atau screenshot gagal, runner berhenti—jangan memakai savestate boot sebagai pengganti gameplay.
- Push run #39262100556, #39262163072, #39262211513 untuk file workflow penerima adalah event `push` tanpa job restore dan **bukan** percobaan emulator. Workflow penerima baru relevan saat workflow utama selesai atau dispatch manual yang menyertakan run ID valid.
- Bukti dasar tetap: raw savestate lintas-run boot berhasil pada #39255438457 → #39255549341; sanitizer positive-control #39257735369 juga pulih untuk state boot. Tidak satu pun bukti itu menunjukkan Story Mode sudah pulih. Memory Card 131.072 byte yang ada masih bertanda `UNVERIFIED_REQUIRES_IN_GAME_SAVE_AND_RELOAD`. **Story Mode belum terbukti tamat.**

## Urutan tindak lanjut

1. Periksa #39262213468 hingga terminal: exit code, `STORY_DIALOG_VISUAL_GATE`, event input START dan perubahan screenshot (bukan hanya input readback), `STORY_CHECKPOINT_SAFE_POINT`, serta manifest raw.
2. Periksa artifact privat; cocokkan ukuran/hash raw dengan manifest serta screenshot checkpoint. Jangan unggah ROM/ISO atau BIOS.
3. Periksa run workflow penerima yang dipicu otomatis; pastikan event restore, ≥180 VSync, dan perbandingan screenshot PASS. Bila run penerima tidak muncul setelah sumber selesai, selidiki trigger/action log terlebih dahulu.
4. Baru setelah restore tengah Story Mode terbukti, lanjutkan stage berikutnya dan simpan raw state sebelum runner habis. Setelah itu uji Memory Card dari alur save/load di dalam game.
5. Setiap aksi/dialog dituntun screenshot; dialog selalu **START**, bukan Circle. Label aturan sebagai **TERVERIFIKASI**, **HIPOTESIS**, atau **BELUM DIUJI**. Jangan mengubah fakta historis atau klaim progres berdasarkan kesimpulan workflow saja.

## HASIL BARU — raw savestate benar-benar pulih lintas-run (19 Oktober 2026)

- **TERVERIFIKASI, terbatas pada boot awal:** [Run A #39255438457](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255438457) membuat raw state melalui `PCSX.createSaveState()` pada VSync 60, tanpa sanitasi. File berukuran **21.124.144 byte**, SHA-256 `a4672dd49fbfa76ef60de410c50460d77e115181fc3e205a215ab9f5f1e601d7`. Artifact sumber privat #12187367829: [unduh dari GitHub](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255438457/artifacts/12187367829).
- **TERVERIFIKASI lintas-run:** [Run B #39255549341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255549341) berjalan sebagai workflow-run baru di runner/workspace dan proses emulator yang baru. B mengunduh artifact A, memverifikasi ukuran serta SHA-256 sama (`SOURCE_ARTIFACT_VERIFY=PASS`, `SOURCE_FILE_UNMODIFIED=1)), lalu memulihkannya.
- Bukti restore B: `ExecutionFlow::SaveStateLoaded`, `LOAD_CALL_RETURNED=1`, `ExecutionFlow::Run`, **180 VSync pascarestore**, exit 0, dan gerbang akhir PASS. Screenshot valid **640×508**, PNG 20.521 byte; SHA-256 `90aa21b6943bac231e4c0e888923a5d1e9658de28ce5c715b9328b17c046db21`. Bukti privat artifact #12187962047: [unduh dari GitHub](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255549341/artifacts/12187962047).
- Screenshot menunjukkan **logo boot Sony Computer Entertainment**; raw state dibuat di sekitar `KERNEL SETUP!`, bukan di tengah Story Mode. Jadi hasil ini membuktikan portabilitas savestate mentah lintas runner/proses **untuk state boot awal saja**.
- **BELUM TERBUKTI:** pemulihan checkpoint tengah Story Mode. Restore checkpoint lama yang disanitasi masih SIGSEGV/exit 139 pada tahap D run #39252214331. Akar penyebab sanitizer belum diketahui. Tidak ada progres Story Mode yang boleh dianggap aman; Story Mode belum dilanjutkan dan game belum terbukti tamat.
- Langkah berikutnya: gunakan raw boot state yang sudah terbukti sebagai kontrol positif, bandingkan sanitizer dengan perubahan satu faktor per eksperimen, dan jangan mengubah checkpoint lama. Setelah sanitizer dipahami, buat raw checkpoint baru saat gameplay Story Mode benar-benar aktif dan wajib buktikan restore dengan event, ≥180 VSync, serta screenshot yang cocok dengan adegan checkpoint sebelum melanjutkan permainan. Memory Card diuji sesudah restore tengah Story Mode terbukti.
- Dialog Story Mode dilewati dengan **START**, bukan Circle. Aturan gameplay tetap diberi label **TERVERIFIKASI / HIPOTESIS / BELUM DIUJI** berdasarkan bukti langsung. Pada pemeriksaan setelah run B, **tidak ada Actions runner aktif**.

---

## UPDATE TERBARU — hasil roundtrip savestate mentah (19 Oktober 2026)

- [Run #39252214331](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39252214331) telah selesai. Tahap A/B/C/C2 lulus; tahap D pada checkpoint lama yang tersanitasi tetap SIGSEGV/exit 139 segera setelah `PCSX.loadSaveState()` dipanggil.
- Tahap E membuat savestate mentah baru melalui `PCSX.createSaveState()` (21.124.150 byte); tahap F memuat file mentah tersebut di emulator yang sama. Terverifikasi: `SaveStateLoaded`, `LOAD_CALL_RETURNED=1`, event `ExecutionFlow::Run`, dan 180 VSync pascapemulihan tanpa crash.
- Artifact privat #12186545059 memiliki screenshot pascapemulihan valid 640×508; isinya layar boot/logo Sony Computer Entertainment. State itu dibuat saat boot awal di sekitar `KERNEL SETUP!`, **bukan** di tengah Story Mode.
- Kesimpulan: ada bukti bahwa roundtrip savestate mentah PCSX-Redux dapat bekerja pada GitHub Actions runner. **Belum ada bukti restore checkpoint tengah Story Mode.** Workflow keseluruhan gagal pada gerbang bukti karena tahap D (checkpoint tersanitasi) masih gagal; tahap F yang lulus tidak mengubah hasil D.
- Hambatan utama yang diketahui: jalur checkpoint tersanitasi/rehidrasi crash saat loader native berjalan, sementara savestate mentah buatan emulator sendiri dapat dimuat. Penyebab tepat transformasi atau field yang memicu crash belum diketahui; perlakukan kerusakan struktur/semantik state sebagai hipotesis, bukan fakta.
- Langkah selanjutnya: pertama, uji savestate mentah buatan emulator sebagai artifact lintas-run—buat pada run A, unggah tanpa modifikasi, lalu muat pada proses emulator bersih di run B. Ini memisahkan masalah lintas-proses dari sanitasi, yang sebelumnya berubah bersamaan. Jika raw lintas-run lulus, baru uji varian tersanitasi; jika gagal, fokus pada portabilitas/proses/build terlebih dahulu. Pertahankan checkpoint lama, jangan restart Story Mode, jangan membatalkan runner lain. Memory Card tetap prioritas sesudah restore tengah Story Mode terverifikasi. Dialog Story Mode dilewati dengan **START**, bukan Circle. Game belum terbukti tamat.
- Catatan lengkap: [docs/SAVESTATE_DIAGNOSTIC_2026-10-19.md](docs/SAVESTATE_DIAGNOSTIC_2026-10-19.md).

---

## STATUS AKTUAL — MEMORY CARD + STORY MODE (19 Oktober 2026; snapshot 18.06 WIB)

- Draft PR #1 telah di-merge ke `main` pada commit [9dc876f08d724b6f809c6da4e2dbea1b549b9d62](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/9dc876f08d724b6f809c6da4e2dbea1b549b9d62).
- Runner #39235643517 dibatalkan pada 19 Oktober 2026 pukul 17.54 WIB. Artifact-nya berisi savestate tersanitasi dan bukti screenshot/log, **tidak berisi Memory Card**. Screenshot terakhir yang diperiksa menampilkan layar Mode Select dengan Story Mode disorot; gerbang visual gagal sebelum frame 5999. Ini bukan gameplay aktif.
- Uji pertama setelah merge: [run #39242130783](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39242130783), head commit merge di atas. Pemeriksaan terakhir pukul 18.06 WIB: workflow masih `in_progress`; asset download/verifikasi lulus, langkah restore kartu dan savestate dilewati (cold boot disengaja), langkah emulator sedang berjalan, dan artifact belum tersedia. Periksa status aktual di GitHub sebelum melanjutkan jika snapshot ini sudah lewat.
- Workflow kini memasang kartu pada slot 1 dengan `-memcard1` di jalur emulator normal dan GDB, membatasi job 35 menit dan proses emulator 25 menit, mengunggah `.mcd` bersama manifest ukuran/SHA-256 sebagai artifact privat 7 hari, serta menolak pemulihan yang kehilangan kartu/manifest atau gagal validasi. Savestate tidak dimuat kecuali diminta eksplisit sebagai alat bantu.
- Run #39242130783 adalah **uji pembuatan kartu/artifact awal**, bukan uji pemulihan lintas-run karena `resume_run_id` tidak diberikan. Belum ada bukti save Story Mode di dalam game, pemulihan save pada cold boot, atau Story Mode tamat.
- Setelah run selesai, periksa status job, exit code emulator, screenshot terakhir, artefak bukti, dan isi artifact kartu/manifest. Jika kartu dan manifest valid, lakukan run terpisah via `workflow_dispatch` dengan `resume_run_id=39242130783` dan `load_savestate=false`; pastikan SHA/ukuran sama setelah restore. Jangan mulai run pemulihan bila artifact kartu tidak ada.
- Baru setelah menu save/load di dalam game ditemukan dan save yang nyata terlihat dapat dimuat kembali setelah cold boot, progres boleh ditandai aman. File `.mcd` yang ada, checksum yang cocok, atau status workflow `success` saja bukan bukti save game berhasil.
- Setiap dialog Story Mode dilewati dengan **START**, bukan Circle. Story Mode belum tamat; mekanik gameplay belum boleh diklaim terverifikasi tanpa screenshot dan eksperimen langsung. Jangan mengubah workflow saat run ini aktif karena concurrency dapat membatalkannya.

---

## TEMUAN GDB & UJI CHECKPOINT SAFE-POINT (2026-10-19)

### Temuan GDB run #39235079514
[Run #39235079514](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39235079514) gagal saat restore, tetapi kali ini GDB benar-benar mengikuti proses emulator. Artifact #12178671125 berisi `pcsx.stdout.txt` dan peta memori lengkap. Pada thread 15 `pcsx-redux`, instruksi crash adalah `movzbl (%rsi),%ecx` di PC `0x00007ffff0dd36d0`; RSI bernilai `0xffffffffddd13fff`, alamat yang tidak valid. PC terletak di image executable `AppDir/shared/bin/pcsx-redux`; binary stripped, sehingga nama fungsi tidak tersedia. Log emulator terakhir hanya mencapai `KERNEL SETUP!`; tidak ada screenshot pasca-restore dan restore tetap gagal.
Sebelum ini run #39234894821 bukan uji emulator yang sah: quoting Bash untuk `$pc` membuat shell berhenti sebelum file `pcsx.stdout` dibuat. Itu sudah diperbaiki. Kesimpulan sementara: restore menyebabkan atau membuka jalur ke dereferensi pointer tidak valid di kode native PCSX-Redux, tetapi fungsi penyebab belum dapat dipastikan; ALSA dummy-device warning belum terbukti sebagai penyebab.

### Uji pembuatan checkpoint di safe point
[Run #39235643517](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39235643517) sengaja cold-boot tanpa memuat checkpoint lama, target 12.000 VSync. Perubahan workflow pada commit `be597ce2b4c6da6c8db34be328007806f164ddd7` mengubah semua save: callback VSync hanya meminta pause, sedangkan `PCSX.createSaveState()` dipanggil setelah emulator paused dan callback `PCSX.nextTick` masuk—bukan saat GPU masih mengerjakan callback VSync. Checkpoint periodik 5.000 VSync, pada layar non-dialog stabil, dan frame cutoff kini memakai jalur safe-point yang sama.
Run terbaru masih antre/berjalan saat catatan ini ditulis. Setelah selesai, wajib cek `STORY_CHECKPOINT_SAFE_POINT frame=... save_ok=true`, `STORY_SAVESTATE_SANITIZE=PASS`, file `storymode-checkpoint.sstate` di private artifact, screenshot sekitar checkpoint, lalu jalankan satu restore test dengan GDB. Baru setelah restore menghasilkan screenshot yang cocok, nyatakan penyimpanan dapat digunakan.
Checkpoint lama artifact #12167524755 (run #39205699071) tetap tersedia sampai 26 Oktober 2026 sekitar 13:47 WIB, tetapi berdasarkan tiga crash restore belum terbukti dapat dipakai. Jangan gunakan sebagai satu-satunya salinan progres.
Story Mode belum tamat; layar terakhir yang tervalidasi tetap dialog pembuka yang meredup. Dialog harus selalu dilewati dengan START, bukan Circle. Belum ada aturan gameplay aktif yang terverifikasi.

---

## UPDATE DIAGNOSTIK — tiga restore gagal awal; trace GDB antre (2026-10-19)

- [Run #39233746088](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39233746088) juga gagal dengan segmentation fault (exit 139) sekitar 7 detik setelah proses emulator mulai. Rehidrasi protobuf BIOS lokal lulus (`RESTORE_BIOS_REHYDRATE=PASS bios_bytes=524288 state_bytes=21162546`), tetapi tidak ada screenshot pasca-restore dan tidak ada savestate baru. Menunda load sampai first VSync, lalu pause + `PCSX.nextTick` juga belum menyelesaikan crash.
- Tiga upaya restore berturut-turut (#39232852795, #39233268705, #39233746088) gagal. Jangan retry tanpa diagnostik lagi; belum ada dasar untuk menyebut savestate aman dipulihkan.
- [Run #39234351228](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39234351228) sengaja memakai GDB untuk menangkap native stack trace saat restore gagal. Perubahan hanya untuk eksperimen diagnostik ini: paket gdb dipasang, bila run adalah restore maka AppRun dimulai di bawah `gdb --batch`, pesan Lua `STORY_/` dan `RESTORE_/` disertakan dalam log, serta `pcsx.stdout.txt`/ `pcsx.log.txt` diunggah sebagai teks di artifact privat. Raw GPU/VRAM/RAM dump tetap tidak aktif.
- Run ini masih antre saat catatan ditulis. Begitu selesai, periksa stack trace serta checkpoint loader sequence. Jika GDB menunjukkan crash dalam `SaveStates::load`/deserialisasi, validasi field protobuf dan checkpoint creation; jika crash terjadi sebelum load, periksa startup/SDL/audio or Lua initialization. Ubah hanya satu faktor dalam eksperimen berikutnya.
- Artifact checkpoint sumber #12167524755 dari run #39205699071 tetap tersedia hingga 26 Oktober 2026 sekitar 13:47 WIB. Artifact berisi savestate tersanitasi ~20,6 MB; layar saat save masih dialog pembuka yang meredup, bukan gameplay aktif.
- Story Mode belum tamat. Dialog dilewati dengan **START**, bukan Circle; tidak ada aturan gameplay yang boleh disebut terverifikasi sampai didukung screenshot eksperimen langsung.

---

## STATUS RESTORE TERBARU — rehidrasi BIOS lulus, restore masih crash; pemuatan ditunda (2026-10-19)

- [Run #39233268705](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39233268705) gagal (exit 139/segmentation fault), meskipun log mencatat `RESTORE_BIOS_REHYDRATE=PASS bios_bytes=524288 state_bytes=21162546`. Jadi menyisipkan kembali field BIOS yang tepat ke checkpoint lokal **belum cukup**; tidak ada screenshot pasca-restore, dan artifact run ini hanya ringkasan kegagalan.
- Kode Lua sebelumnya memanggil `PCSX.loadSaveState` saat evaluasi awal skrip. Hipotesis timing kini diperiksa: pemanggilan native loader mungkin dilakukan sebelum siklus emulasi siap. Ini belum terbukti sebagai akar masalah, tetapi cocok dengan crash yang terjadi sebelum log `STORY_SAVESTATE_LOAD_CALL_RETURNED` dan sebelum VSync pertama sempat dicatat.
- Commit workflow `fa220bead2da2418921b2fcc392d16b87201dd42` mengubah alur restore: pada VSync pertama, meminta emulator pause; jalankan pembacaan dan load savestate lewat `PCSX.nextTick`; setelah panggilan load kembali, reset counter observasi dan resume. Jika file tidak ada atau load melempar error, workflow gagal tertutup dan tidak diam-diam cold-boot.
- [Run #39233746088](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39233746088) menguji pemuatan tertunda tersebut; status terakhir antre. Periksa log untuk `RESTORE_BIOS_REHYDRATE=PASS`, `STORY_SAVESTATE_RESTORE_PAUSE_REQUESTED=1`, `STORY_SAVESTATE_LOAD_CALL_RETURNED=1`, exit code, dan screenshot baru. Hanya screenshot visual yang menunjukkan adegan sesuai checkpoint atau transisi yang dapat mengonfirmasi pemulihan.
- Checkpoint sumber tetap artifact privat #12167524755 dari run #39205699071; tersedia hingga 26 Oktober 2026 sekitar 13:47 WIB. Artifact itu berisi savestate tersanitasi tetapi belum bisa dipakai dengan andal sampai salah satu uji restore berhasil. Layar terakhir sebelum save masih berupa dialog pembuka yang sedang meredup, bukan gameplay aktif.
- Story Mode belum tamat. Gunakan START untuk melewati dialog, bukan Circle; identifikasi adegan sebelum aksi gameplay baru, dan verifikasi aturan permainan dengan screenshot dari pengujian aktual.

---

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

## STATUS OPTIMASI RUNNER — crash berulang, guard checkpoint sedang diuji (2026-10-19)

Tujuan pengguna tetap: mempercepat emulator, memakai job timeout 360 menit, dan boleh memindahkan game save/savestate yang telah disanitasi lewat storage private agar Story Mode dapat dilanjutkan antar-job. Timeout GitHub Actions kini 360 menit, tetapi **sesi panjang belum terbukti berjalan** karena emulator masih crash awal.

### Bukti dari dua run terbaru
- [Run #39205262049](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39205262049) berakhir workflow-success secara keliru walau log menunjukkan `Segmentation fault`, `EMULATOR_EXIT_CODE=139`; job lama tidak memeriksa exit code emulator. Gate visual gagal sebelum frame 5999, tidak ada screenshot progres atau savestate.
- [Run #39205556772](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39205556772) sesudah penghapusan panggilan `PCSX.GPU.getDumpFrames()` berakhir **failure** dengan exit 139 dalam sekitar delapan detik. BIOS retail terdeteksi dan log mengenali disc `SLPS03553` serta executable `SLPS_035.53;1`, tetapi gate berhenti sebelum frame 5999. Artifact #12165635987 hanya berisi tiga file teks kecil; `STORY_SAVESTATE_SANITIZE=missing`.
- Maka menghapus `getDumpFrames()` belum menyelesaikan crash. ALSA juga mengeluarkan pesan tak adanya perangkat suara di runner; itu tercatat tetapi belum dipastikan penyebab crash.
- Hipotesis berikutnya yang diuji, belum terbukti: Lua selalu memanggil `Support.File.open("resume/storymode-checkpoint.sstate")` bahkan saat tidak ada artifact restore. Native savestate loader bisa gagal dengan cara yang tidak tertangkap Lua bila menerima File object yang tidak valid. Commit `88d5cfa8833ef39e286431f5e8bedf2584485804` menambahkan probe `io.open` dan hanya memanggil native loader bila file benar-benar ada.
- [Run #39205699071](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39205699071) dibangun dari commit guard tersebut dan masih antre/baru dimulai saat bagian ini ditulis. Periksa screenshot/log dan status job sebelum menganggap perbaikan berhasil.

### Konfigurasi dan perubahan performa yang dipertahankan
- Job timeout `timeout-minutes: 360`; timeout emulator internal 20.400 detik (5 jam 40 menit) untuk menyisakan waktu sanitasi/upload/cleanup.
- BIOS SCPH-7502 (EU); disc `SLPS03553`; executable `SLPS_035.53;1`; PCSX-Redux pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`; SoftGPU; Port 1 Analog/Auto.
- Jalur bermain tidak merekam raw GPU/VRAM terus-menerus dan menonaktifkan polling GDB/RSP serta sampling jendela berkala. Ini dimaksudkan mengurangi overhead, tetapi kecepatan belum terukur karena crash sebelum screenshot pertama yang relevan.
- Dialog tetap dilewati dengan **START**, bukan Circle. Bila layar non-dialog stabil muncul, simpan checkpoint dan berhenti untuk inspeksi; jangan menebak kontrol gameplay.
- Game save/savestate tersanitasi boleh dipindahkan melalui private Actions artifact/cache/private repo sesuai kebijakan baru. Workflow saat ini hanya menggunakan private artifact berumur tujuh hari. Savestate baru boleh diunggah hanya jika sanitizer menyatakan PASS dan field BIOS tertanam terhapus; raw RAM/VRAM/GPU dump tetap dilarang. ROM/ISO, executable game, dan file BIOS retail tersendiri tetap tidak boleh diunggah.

### Langkah selanjutnya
1. Periksa Run #39205699071 dan baca log penuh, bukan hanya kesimpulan workflow. Jika crash masih exit 139, isolasi dengan mengembalikan opsi GDB lama tanpa mengaktifkan kembali raw GPU dump terlebih dahulu; ubah satu variabel per run.
2. Jangan mengklaim checkpoint dapat dipakai sebelum log menunjukkan save state berhasil dibuat, sanitizer PASS, artifact benar-benar memuat file state, dan restore run berikutnya dikonfirmasi oleh screenshot.
3. Setelah emulator stabil, ukur VSync per waktu nyata; baru setelah itu nilai apakah penghematan overhead cukup untuk menyelesaikan Story Mode dalam satu sesi enam jam.

---

## REVISI ATURAN SAVE & CHECKPOINT — instruksi terbaru pengguna (2026-10-19)

Kebijakan ini **menggantikan larangan lama yang melarang semua save/save state di penyimpanan GitHub**. Pengguna sekarang secara eksplisit mengizinkan pemindahan save untuk mempertahankan progres Story Mode.

- Save kartu memori/game save dan **savestate emulator yang telah disanitasi** boleh dipindahkan melalui **private GitHub Actions artifact, GitHub Actions cache, atau repositori private**. Jangan menaruhnya di repositori publik. Default yang dipakai workflow saat ini adalah private artifact berumur 7 hari; cache/repo diizinkan oleh aturan tetapi belum diaktifkan di workflow.
- Savestate PCSX-Redux yang dipindahkan harus melewati sanitizer yang memverifikasi struktur protobuf dan menghapus field BIOS tertanam (Memory.rom). Transfer hanya boleh diunggah jika indikator STORY_SAVESTATE_SANITIZE=PASS; jika sanitasi gagal atau struktur tidak dikenal, jangan unggah file state itu.
- Savestate berisi state emulasi game (termasuk RAM/VRAM sebagai bagian format save); itu diperbolehkan setelah sanitasi sebagai **savestate**, bukan sebagai dump memori terpisah. **Raw RAM dump, raw VRAM dump, dan raw GPU dump tetap tidak boleh diunggah.** File state mentah sebelum sanitasi harus tetap sementara di runner dan dibersihkan.
- ROM/ISO, executable game, dan file BIOS retail tersendiri tetap dilarang di-commit atau diunggah ke artifact/cache/repo. Runner berikutnya harus mengambil aset dari release privat yang sudah ada dan memverifikasi hash sesuai prosedur.
- Untuk melanjutkan sesi, jalankan workflow secara manual (workflow_dispatch) dengan input resume_run_id berisi ID run yang memuat artifact naruto-storymode-checkpoint-private. Loader harus memakai BIOS SCPH-7502 yang diverifikasi secara terpisah. Restore lintas-run harus dikonfirmasi lewat log dan screenshot; jangan menganggap loader berhasil hanya karena artifact ditemukan.
- Workflow terbaru pada commit 58d2e8b18feec9dedbb9fbfd9623fc40c1039175: timeout job 360 menit; SoftGPU tetap dipakai; emulator diberi batas internal 20.400 detik (5 jam 40 menit) agar ada waktu untuk sanitasi, upload, dan cleanup. Untuk jalur bermain, perekaman GPU mentah, GDB/RSP polling, dan sampling jendela berkala dinonaktifkan. Detektor visual meminta START untuk dialog, checkpoint dibuat tiap 5.000 VSync serta saat layar non-dialog stabil, lalu sesi dijeda untuk inspeksi sebelum aksi gameplay yang belum terbukti.
- Run pertama dari workflow baru [#39205262049](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39205262049) masih berstatus antre/menunggu pada pemeriksaan terakhir. Perubahan ini sudah dikomit, tetapi kecepatan aktual, detektor dialog, sanitizer, dan pemulihan savestate **belum dianggap teruji** sampai hasil run diperiksa.
- Setiap dialog Story Mode tetap dilewati dengan **START**, bukan Circle. Circle hanya dipakai untuk konfirmasi menu yang memang memerlukannya. Klaim progres harus didukung screenshot aktual; jangan menyatakan Story Mode tamat sebelum layar akhir yang meyakinkan.

---

## ATURAN KONTROL DIALOG — instruksi pengguna terbaru (2026-10-19)

**Setiap kali Story Mode menampilkan dialog/narasi yang meminta dilanjutkan atau di-skip, gunakan tombol START untuk melewatinya, bukan Circle.** Ini preferensi kontrol yang harus dipertahankan di chat dan eksperimen berikutnya.

- Circle tetap digunakan hanya untuk langkah menu yang telah dibuktikan memerlukannya, termasuk mengonfirmasi pilihan Story Mode dari layar Mode Select. Jangan memakai Circle sebagai tombol skip dialog.
- Kirim satu tap START terkontrol (press dan release terpisah), lalu ambil/baca screenshot sebelum dan sesudahnya. Jangan mengirim input beruntun tanpa inspeksi layar.
- Jika workflow otomatis, gate START dengan fingerprint screenshot dialog aktual yang sudah diverifikasi; catat frame, hasil visual, dan perubahan layar. Readback input emulator tidak cukup untuk mengklaim game merespons.
- Setelah dialog berubah, identifikasi teks/layar baru terlebih dahulu sebelum aksi selanjutnya. Setiap teks Jepang yang dilaporkan harus diikuti terjemahan Bahasa Indonesia dalam tanda kurung.
- Instruksi ini mengoreksi rencana lama yang menggunakan Circle untuk memajukan narasi. Jangan mengikuti langkah Circle lama ketika konteksnya adalah dialog.

---

## HASIL RUN #39189879767 — Circle memajukan narasi ke kalimat berikutnya (2026-10-19)

Run [#39189879767](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39189879767) selesai dengan workflow/job `success`, mencapai 10.000 VSync. Artifact privat #12161482625 telah diunduh dan screenshot aktual diperiksa. Jangan jalankan ulang run ini.

**Bukti visual dari screenshot yang benar-benar diperiksa:**
- Frame 9199 dan 9200 memperlihatkan kalimat pembuka `今日は、アカデミーの卒業試験の日。` (Hari ini adalah hari ujian kelulusan Akademi.).
- Gate `STORY_DIALOG_VISUAL_GATE=PASS` pada frame 8999: crop 280×240 stabil yang tidak mencakup ikon Circle beranimasi cocok dengan baseline screenshot terverifikasi.
- Circle tambahan ditekan pada frame 9200 dan dilepas pada frame 9230. Frame 9229/9230 memperlihatkan kotak dialog kosong; frame 9240 mulai menampilkan teks berikutnya.
- Frame 9299, 9499, dan 9999 stabil dan menampilkan `忍者を目指す者にとって大切な一歩をふみ出す日である。` (Bagi mereka yang bercita-cita menjadi ninja, hari ini adalah hari untuk mengambil langkah penting.). Perubahan sebelum/sesudah ini membuktikan bahwa Circle memajukan narasi, bukan sekadar terbaca oleh API controller.
- Batas kesimpulan: **Story Mode masih pada layar narasi**. Tidak ada gerak karakter atau gameplay aktif yang terverifikasi; mekanik permainan dan tamat Story Mode masih belum terbukti.

**Run dan cleanup:** ringkasan melaporkan `GPU_DUMP_RESULT=parsed`, `GPU_DUMP_TRUNCATED=false`, `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`; langkah penghapusan workspace dijalankan hingga selesai. ZIP artifact sekitar 8,32 MB berisi ringkasan/log dan screenshot PNG pilihan; daftar isi tidak menunjukkan ROM, BIOS, save/save state, raw GPU/VRAM dump, atau aset mentah terlarang.

**Langkah berikutnya yang telah disiapkan:** commit workflow `a561b8196658dd218bedb5a70e34a1796e3ff9cf` menambahkan tap Circle berikutnya pada frame 10200–10230, setelah screenshot frame 9999 lolos gate visual kedua untuk kalimat di atas. Screenshot checkpoint direncanakan pada 10199 (sebelum), 10200, 10229, 10230, 10240, 10299, 10499, dan 10999; observasi sampai 11000 VSync. Periksa run baru yang dipicu commit ini. Bila gate gagal, Circle keempat dilewati. Jangan kirim input tambahan bila screenshot menunjukkan layar yang belum diidentifikasi.

**Baseline tetap:** retail BIOS SCPH-7502 (EU); disc ID `SLPS03553`; executable `SLPS_035.53;1`; PCSX-Redux source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`; SoftGPU; Port 1 Analog/Auto. Jangan mengubah konfigurasi tanpa alasan yang didokumentasikan.

---

## PEMBARUAN HANDOFF — satu tap Circle setelah narasi terverifikasi (2026-10-19)

Run eksperimen baru [#39189879767](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39189879767) dipicu oleh commit workflow `892f16c2b2ea140f41b7e920d09d08261867b377`. Pemeriksaan terakhir menunjukkan job masih `in_progress`; bukti setelah Circle tambahan belum tersedia saat catatan ini ditulis. **Jangan anggap input terbaca emulator atau status workflow sebagai bukti bahwa game sudah maju.**

### Perubahan eksperimen yang sedang berjalan
- Pertahankan cold boot dan urutan terbukti: Start press/release 2650/2680; D-pad DOWN 2710/2720; UP 2740/2750; Circle pertama 2780/2810.
- Gerbang visual Mode Select pada frame 5999 tetap wajib. Circle kedua dijadwalkan 6100/6130 hanya jika gambar menu dan pilihan Story Mode cocok dengan fingerprint terverifikasi.
- Gerbang visual narasi membaca framebuffer frame 8999 dan membandingkan crop stabil 280×240 dengan screenshot terverifikasi (bagian ikon Circle yang berkedip di kanan bawah tidak ikut dihitung). Tap ketiga **hanya** dikirim jika gerbang Mode Select sebelumnya dan crop narasi sama-sama lolos.
- Circle tambahan: press frame 9200, release frame 9230. Screenshot sebelum input diambil pada frame 9199; checkpoint sesudahnya 9200, 9229, 9230, 9240, 9299, 9499, dan 9999. Target observasi akhir VSync 10000.
- Config tetap retail BIOS SCPH-7502 (EU), CD ID `SLPS03553`, executable `SLPS_035.53;1`, PCSX-Redux source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`, SoftGPU, Port 1 Analog/Auto.

### Tindakan setelah run selesai
1. Periksa status terbaru, job log, dan artifact run #39189879767; jangan menjalankan ulang #39178662131 dan jangan mengulang run #39183597316.
2. Buka screenshot aktual frame 9199, 9200, 9229/9230, 9240, 9299, 9499, dan 9999. Bandingkan narasi sebelum/sesudah Circle; gunakan gambar, bukan `PAD_INJECT` readback.
3. Pastikan summary melaporkan `STORY_DIALOG_VISUAL_GATE`, hasil `STORY_CIRCLE3`, target frame akhir, penghapusan raw GPU dump/screenshot sementara, serta penghapusan workspace.
4. Jika scene berubah, identifikasi layar baru sebelum merencanakan input berikutnya. Jika scene tetap sama, frame hitam muncul, atau gate gagal, simpan sebagai hasil negatif/tidak konklusif dan rancang satu eksperimen pembeda—jangan menekan tombol tambahan tanpa inspeksi.
5. Pada saat catatan ini dibuat, gameplay aktif, mekanik, progres stage, dan tamat Story Mode tetap **belum terbukti**.

Privasi: ROM, BIOS, save/save state, raw GPU/VRAM dump, dan aset privat tidak boleh di-commit atau diunggah. Artifact baru harus diperiksa sebelum dibagikan; cleanup yang ditulis dalam workflow tetap harus diverifikasi di log aktual.

---

## HASIL DAN HANDOFF TERBARU — Story Mode telah masuk ke narasi pembuka (run #39183597316, 2026-10-19)

Run [#39183597316](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39183597316) selesai dengan workflow/job `success` pada commit workflow `e9a6f985458ad2dd23c939813881918cb9a7f701`. Run lama #39178662131 tidak diulang. Artifact privat [#12158079662](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39183597316/artifacts/12158079662) telah diunduh, inventaris file diperiksa, dan screenshot aktual dilihat.

**Temuan visual yang membuktikan transisi:**
- Sequence cold boot yang terbukti diulang: Start press/release frame 2650/2680; DOWN 2710/2720; UP 2740/2750; Circle pertama 2780/2810.
- Gerbang visual `STORY_SELECT_VISUAL_GATE=PASS` pada frame 5999: crop judul Mode Select dan crop pilihan Story Mode cocok dengan fingerprint screenshot baseline yang telah diverifikasi. Karena gerbang lulus, Circle kedua benar-benar dikirim: press frame 6100 dan release frame 6130. Readback input hanya catatan pendukung, bukan dasar klaim.
- Frame 6099–6140 masih menunjukkan layar pemilihan mode dengan Story Mode tersorot dan animasi kartu. Frame 6200 dan 6399 hitam seragam; keduanya **tidak** dipakai sebagai bukti Story Mode.
- Frame 6799 menampilkan layar narasi cerita baru; layar serupa bertahan pada 7199, 7599, 7999, 8499, dan 8999. Teks terbaca: `今日は、アカデミーの卒業試験の日。` (Hari ini adalah hari ujian kelulusan Akademi.). Ini adalah bukti visual kuat bahwa konfirmasi kedua membawa game masuk ke pembukaan Story Mode, bukan hanya memilih opsinya di menu. Kesimpulan terverifikasi: **Story Mode telah dimulai sampai adegan narasi pembuka**.
- Batas kesimpulan: adegan pembuka terlihat stabil sampai frame 8999, tetapi kontrol karakter/gameplay aktif, mekanik, progres misi, dan tamat Story Mode **belum** diuji.

**Konfigurasi:** log runtime mencatat BIOS SCPH-7502 (EU), CD ID `SLPS03553`, executable `SLPS_035.53;1`, dan Port 1 connected Analog/Auto. Workflow tetap mematok PCSX-Redux source `0c3572c3db75f97542001e453ae80ba8c3f8acba` dan flag `-softgpu`; konfigurasi wajib lainnya tidak diubah.

**Cleanup dan isi artifact:** log menyatakan `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`, GPU dump ter-parse lengkap (`GPU_DUMP_TRUNCATED=false`), dan workspace runtime dihapus. ZIP 7.6 MB berisi ringkasan/log, RSP summary, gerbang visual dan screenshot PNG checkpoint yang memang diperlukan sebagai bukti; tidak ditemukan file ROM, BIOS, save, raw GPU/VRAM dump, atau file mentah ber-ekstensi terkait di artifact.

**Langkah eksperimen berikutnya:** lakukan cold boot baru dan ulangi urutan lengkap sampai Story Mode. Tunggu layar pembuka tampak; screenshot menunjukkan ikon Circle di kanan bawah kotak narasi. Uji hanya satu tap Circle terkontrol (press/release terpisah) untuk mencoba melanjutkan dialog, capture tepat sebelum/sesudah, dan amati apakah adegan berikutnya/gameplay muncul. Jangan kirim input beruntun dan jangan menandai kontrol gameplay lulus sebelum ada bukti visual/gerakan karakter yang aktual.


---

## Kebijakan gambar bukti — instruksi pengguna (2026-10-19)

Untuk setiap gambar yang ditampilkan atau disebut sebagai tampilan di dalam game Naruto, gunakan **hanya screenshot aktual dari hasil eksperimen riset kita** (misalnya PNG dalam artifact GitHub Actions run yang telah diperiksa). Jangan mengganti, menghias, atau menyamarkan gambar hasil web/pencarian sebagai bukti game kita. Jika screenshot dari eksperimen belum tersedia atau tidak bisa diverifikasi, katakan dengan jelas bahwa bukti visual belum tersedia daripada mengambil gambar web. Jika memungkinkan, beri label run ID dan nomor frame agar asal bukti dapat ditelusuri. Setiap teks Jepang yang ditampilkan wajib disertai terjemahan Bahasa Indonesia di sebelahnya dalam tanda kurung.

---

## Hasil terbaru menggantikan status eksperimen sebelumnya — run #39178662131 (2026-10-19)

Run [#39178662131](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39178662131) **sudah selesai** dengan status success, jadi jangan menjalankan ulang run tersebut. Artifact privat [#12155879252](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39178662131/artifacts/12155879252) telah diunduh dan screenshot dibaca langsung.

**Bukti visual yang baru terverifikasi:**
- Frame 2.670: menu `はじめから` / `ロード`, panah di pilihan pertama.
- DOWN 2.710–2.720: pada frame 2.720 panah berada di `ロード`.
- UP 2.740–2.750: pada frame 2.749/2.750 panah kembali di `はじめから`.
- Circle menu 2.780–2.810: overlay menu menghilang; sesudah beberapa frame gelap/hitam, frame 3.399 langsung memperlihatkan `モードセレクト` dengan `ストーリーモード` tersorot. Layar Mode Select stabil pada checkpoint hingga frame 5.999. Hitam pada frame 2.950–3.199 sendiri tidak dijadikan bukti mode.
- Jadi Start → navigasi DOWN/UP → Circle pada `はじめから` secara visual membawa permainan ke Mode Select. **Story Mode belum dimulai** karena belum ada Circle kedua atau bukti layar gameplay.

Baseline yang wajib dipertahankan: SCPH-7502 (EU); CD ID `SLPS03553`; EXE `SLPS_035.53;1`; PCSX-Redux source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`; SoftGPU; Port 1 Analog/Auto.

Cleanup run terverifikasi: `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`, dan perintah akhir menghapus workspace runtime. Isi ZIP artifact yang diperiksa hanyalah summary/log teks, screenshot PNG pilihan, dan RSP summary; tidak ada ROM, BIOS, save, atau raw GPU/VRAM dump. Artifact berumur tiga hari.

## Rencana langkah berikutnya untuk chat baru

1. Baca bagian hasil terbaru ini, lalu periksa workflow aktif dan dokumen RT-001 sebelum menyunting.
2. Pada cold boot baru ulangi sequence yang telah terbukti: Start press/release 2.650–2.680; DOWN 2.710–2.720; UP 2.740–2.750; Circle pada menu 2.780–2.810.
3. Terus ambil bukti sampai Mode Select terlihat (run ini: frame 3.399 dan stabil hingga 5.999). Karena `ストーリーモード` sudah tersorot pada layar tersebut, rencana Circle kedua pada frame 6.100–6.130, dengan screenshot tepat sebelum/sesudah dan observasi diperpanjang sampai frame 9.000 atau lebih.
4. Klaim Story Mode dimulai hanya jika screenshot setelah Circle kedua menunjukkan transisi nyata ke layar Story Mode/gameplay; jangan membuat inferensi dari frame hitam, `PAD_INJECT PASS`, atau status workflow.
5. Pertahankan SCPH-7502, SLPS03553 / `SLPS_035.53;1`, PCSX-Redux pin, SoftGPU dan Port 1 Analog/Auto. Jangan sentuh Tile Duel. Jangan commit/upload ROM, BIOS, save, raw GPU/VRAM dump atau file privat; cek cleanup sampai akhir.
6. **Jangan membuat run duplikat** untuk #39178662131; run tersebut sudah selesai. Langkah berikutnya adalah eksperimen baru dengan sequence lengkap di atas.

---

# HANDOFF CHAT BARU — Naruto PS1 (2026-10-19)

Dokumen ini dibuat sebagai handoff terbaru. Baca dokumen ini terlebih dahulu saat melanjutkan riset. Instruksi pengguna di sini **menggantikan** instruksi lebih lama yang meminta Start saja dan melarang Circle.

## Instruksi pengguna paling baru

Jika Start sudah membuka menu utama Naruto, gunakan **panah arah (D-pad)** untuk memilih opsi, lalu tekan **Circle/O** untuk menjalankan opsi yang dipilih. Lakukan eksperimen selanjutnya di chat baru, bukan di chat sebelumnya. Jangan berhenti pada menu utama hanya karena instruksi lama menyebut jangan menekan Circle.

Target berikutnya: pilih `はじめから` (“Mulai dari awal”), pastikan layar berikutnya melalui screenshot nyata, lalu lanjut ke Mode Select dan Story Mode setelah setiap layar diidentifikasi.

## Baseline status yang telah dibuktikan

Repositori yang boleh dikerjakan hanya `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`.
Dokumentasi utama: `STATUS.md`, `HANDOFF_LANJUT.md`, `ANALYSIS_LOG.md`, dan `docs/RUNTIME_TEST_PLAN.md`. Workflow aktif untuk uji boot: `.github/workflows/naruto-scph7502-gpu-traffic-summary.yml`.

Konfigurasi runtime yang dipertahankan:
- Game disc ID `SLPS03553`; executable `SLPS_035.53;1`.
- Retail PlayStation BIOS SCPH-7502 (EU).
- PCSX-Redux source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`.
- SoftGPU; Port 1 controller Analog / Auto.
- ROM, BIOS, save, raw GPU/VRAM dump, serta file privat tidak boleh di-commit atau masuk artifact. Artifact hanya perlu ringkasan dan screenshot bukti minimum; hapus aset sementara sebelum upload.

## Hasil run relevan

### Run #39145309203 — menu terbuka (bukti utama)
https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39145309203
Artifact privat #12143433923. Start ditekan di VSync/frame 2650 dan dilepas 2680. Frame 2670 menunjukkan menu dengan panah pada `はじめから` dan opsi kedua `ロード`; menu tetap terlihat sampai frame 2999. Run ini **tidak** mengirim Circle.

### Run #39149443247 — Start lalu Circle, hasil belum tuntas
https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39149443247
Urutan Start 2650–2680 lalu Circle 2750–2780 dalam boot yang sama. Menu menghilang/fade; frame 2900–2999 hitam seragam. Tidak ada tulisan `モードセレクト` yang berhasil dibaca. Jangan simpulkan Mode Select/Story Mode dari layar hitam, tetapi catat bahwa Circle mungkin memicu transisi atau loading yang memerlukan observasi lebih panjang.

### Run #39176328030 — menu tetap stabil dengan Start saja (paling baru)
https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39176328030
Artifact #12155370415 (retensi tiga hari). Frame 2650 menampilkan judul Naruto dan prompt Start; frame 2670 menampilkan menu; frame 2999 tetap menampilkan menu. Input hanya Start press 2650/release 2680. Tidak ada Circle atau tombol arah di run ini. Run selesai pada level workflow, dan visualnya membuktikan Start membuka menu serta menu tetap stabil bila tidak dikonfirmasi.

### Dokumentasi dan workflow saat ini
- HEAD `main` terakhir yang diketahui: `c83fe4ef86992c762533c0712dc2755764ee5b75`.
- Commit tersebut memperbarui `STATUS.md`, `HANDOFF_LANJUT.md`, `ANALYSIS_LOG.md`, dan `docs/RUNTIME_TEST_PLAN.md` untuk merekam hasil Start-only.
- Workflow saat ini masih berisi **Start saja**: press pada frame 2650, release pada frame 2680. Perlu ubah input sequence untuk eksperimen lanjutan di chat baru dan cek file workflow sebelum menyunting.

## Rencana uji berikutnya

1. Periksa file workflow aktual, log terakhir, artifact #12155370415 bila masih ada, dan catatan status. Jangan menjalankan duplikat run lama atau mengandalkan ringkasan tanpa memeriksa file aktual.
2. Setiap GitHub Actions run melakukan **cold boot baru**; jadi skrip harus mengulangi urutan penuh dalam satu boot yang sama: tunggu prompt judul → Start → tunggu hingga menu muncul → gunakan D-pad untuk menavigasi/menegaskan pilihan `はじめから` → Circle/O untuk konfirmasi.
3. Menu yang terlihat saat ini sudah menaruh panah di `はじめから`. Untuk menunjukkan navigasi secara eksplisit tanpa meninggalkan pilihan yang dimaksud, pertimbangkan tap Down lalu Up (dengan press/release terpisah), kemudian Circle; pastikan frame waktunya setelah menu terbuka. Ambil checkpoint sebelum dan sesudah tiap input. Jangan mengirim input menu saat title prompt masih tampil.
4. Observasi melebihi frame 3000 bila perlu, karena eksperimen Start+Circle sebelumnya hanya melihat layar hitam sampai frame 2999. Tangkap checkpoint setelah 3000 (mis. 3300, 3600, 4200, 4800, hingga 6000 bila batas runner memungkinkan) agar transisi/loading dapat dibedakan dari hasil yang belum diketahui. Simpan hanya screenshot minimum yang dibutuhkan.
5. Jika layar baru muncul, baca tulisan/opsi Jepang yang benar-benar ada. Jangan menganggap layar hitam berarti Mode Select. Setelah layar teridentifikasi, baru rancang input berikutnya untuk memilih Story Mode; terus kumpulkan bukti visual, input sequence dan log.
6. Status `PAD_INJECT ... PASS` hanya membuktikan API emulator membaca balik nilai input; respons game harus dibuktikan melalui perubahan visual atau state gameplay yang terukur. Workflow `success` juga bukan bukti gameplay sukses.
7. Jangan menjalankan Story Mode secara spekulatif dengan input beruntun. Lanjutkan selangkah demi selangkah: menu → pilihan mulai dari awal → bukti layar tujuan → Mode Select → Story Mode → kontrol gameplay → progres/tamat.

## Status tujuan RT-001 saat handoff

- Boot game hingga logo DIMPS/title Naruto: **terbukti**.
- Tekan Start dari layar judul untuk membuka menu: **terbukti secara visual**.
- Pilih `はじめから` dengan navigasi arah + Circle: **belum terbukti**.
- Mode Select: **belum terbukti**.
- Story Mode benar-benar dimulai: **belum terbukti**.
- Respons kontrol saat gameplay, pengujian mekanik, dan tamat Story Mode: **belum terbukti**.

Instruksi pengguna terbaru (berlaku mulai handoff ini): gunakan panah arah untuk memilih opsi dan Circle untuk menjalankannya setelah menu dibuka. Instruksi lama “jangan tekan Circle” sudah tidak berlaku untuk eksperimen lanjutan ini.

## Handoff terbaru — 20 Oktober 2026: raw board restore probe

Repo yang boleh diubah tetap hanya zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research.

- Run [#39373493482](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39373493482) selesai failure, tetapi sumber kegagalan bukan crash saat memanggil loader. Source dan staging checkpoint sama byte-per-byte (21.163.286 byte; SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d). Build patched PCSX-Redux selesai sukses; schema baseline dan patched build sama; ExecutionFlow::SaveStateLoaded terdeteksi; loader kembali; screenshot segera pascarestore sama persis dengan sumber (mean diff 0.00000, exact pixels 1.000000).
- Tes berakhir pada timeout 1800 detik dengan exit code 124. Gerbang POST_RESTORE_VSYNC/cross-run tak tercatat, tidak ada checkpoint lanjutan tervalidasi, dan proses kedua tidak dijalankan.
- Penyebab harness yang ditemukan: script Lua menjeda emulator pada frame 180 lalu melakukan polling restore-screenshot-match.flag lewat PCSX.nextTick; callback polling tidak maju saat emulasi dijeda. Workflow diperbaiki pada commit 8bb5c0ed829cc2ff5e004612445c8fdb88836d04 agar VSync tetap berjalan sambil menunggu flag. Pemicu push sementara sudah dihapus dan workflow hanya manual dispatch lagi.
- Run ulang [#39383287999](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39383287999) sedang berlangsung pada pemeriksaan terakhir; build dan restore belum ada hasil final.

Jangan sebut checkpoint #39373493482 sebagai checkpoint baru yang dapat dipakai: manifest mencatat ukuran next-state 0 dan SHA missing. Jangan menyimpulkan fix sudah sepenuhnya terverifikasi sampai run ulang melewati post-restore gate, menghasilkan checkpoint nonkosong, lalu memuat checkpoint itu sukses dalam proses emulator baru. Jangan mengirim input kontrol, memulai ulang 90 menit gameplay, atau mengubah file savestate sumber.

## Handoff lanjutan — malam 20 Oktober 2026

Run [#39383287999](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39383287999) gagal pada gerbang workflow setelah loader berhasil kembali dan screenshot pascarestore lulus tepat per piksel. Run mencatat state source/staging identik (21.163.286 byte; SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`), `ExecutionFlow::SaveStateLoaded`, loader-return=1, dan comparison PASS (mean RGB diff 0; exact pixels=1.0). Namun log tidak mengandung `STORY_RAW_RESTORE_POST_RESTORE_VSYNC=180` / `STORY_RAW_RESTORE_CROSS_RUN=PASS`; emulator maju sampai frame 12000. Manifest menunjukkan checkpoint lanjutan 0 byte dan reload proses kedua dilewati.

Percobaan setelahnya memperbaiki mekanisme kontrol: screenshot gate kini dibaca langsung dalam callback GPU::Vsync, bukan polling rekursif `PCSX.nextTick`; setelah PASS baru jadwalkan save pada safe tick dan berhenti. Batas tunggu flag 900 VSync menghindari loop tak berujung. Workflow file sudah diperbaiki dan pemicu sementara dibersihkan kembali. Run terbaru [#39426068247](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39426068247) berjalan; pada pemeriksaan terakhir baru memulai job, belum ada hasil runtime.

Run #39425629341 dan #39425661897 berhenti tanpa jobs atau artifacts (perubahan harness/trigger perantara), jadi jangan perlakukan sebagai bukti emulator atau savestate. Tidak ada gameplay button yang dikirim, dan source savestate tidak diubah.

## Status terbaru — 21 Oktober 2026: restore savestate sudah PASS

Run [#39426068247](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39426068247) final `success`. Ini hasil validasi penuh, bukan sekadar screenshot awal:
- Checkpoint sumber #39262213468 tidak diubah: 21.163.286 byte, SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`; staging identik.
- Patched emulator memuat raw board, event muncul, loader kembali, 180 VSync lolos, dan screenshot gate PASS.
- Checkpoint baru frame probe 181 tersimpan: 21.162.405 byte, SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`.
- Proses emulator kedua yang baru memuat checkpoint baru dan melewati event, loader-return, 180 VSync dan screenshot gate. Manifest menyatakan `PROBE_NEXT_CHECKPOINT_VALID=PASS`; kedua proses dan comparator exit code 0.
- Build varian memakai base PCSX-Redux `0c3572c3db75f97542001e453ae80ba8c3f8acba` + hanya patch SPU/ADPCM upstream PR #2218. Hash AppImage `f4ffa4b00b7fd8c0966213872c0263ca8637601eb74da3f9523e7914ba93bd56`.
- Artefak privat Actions #12268621845 dapat diakses lewat [run ini](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39426068247), kedaluwarsa 3 Nov 2026.

**Langkah berikutnya:** lanjutkan Story Mode dari checkpoint lanjutan melalui build patched yang sama. Belum ada tombol gameplay yang dikirim oleh probe ini, dan belum ada bukti tamat game atau save/load Memory Card di dalam game. Jangan jalankan source emulator lama yang memicu crash untuk memuat state ini.

