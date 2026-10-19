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
