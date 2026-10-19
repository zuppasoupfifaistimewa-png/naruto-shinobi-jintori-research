## UPDATE TERBARU — hasil roundtrip savestate mentah (19 Oktober 2026)

- [Run #39252214331](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39252214331) telah selesai. Tahap A/B/C/C2 lulus; tahap D pada checkpoint lama yang tersanitasi tetap SIGSEGV/exit 139 segera setelah `PCSX.loadSaveState()` dipanggil.
- Tahap E membuat savestate mentah baru melalui `PCSX.createSaveState()` (21.124.150 byte); tahap F memuat file mentah tersebut di emulator yang sama. Terverifikasi: `SaveStateLoaded`, `LOAD_CALL_RETURNED=1`, event `ExecutionFlow::Run`, dan 180 VSync pascapemulihan tanpa crash.
- Artifact privat #12186545059 memiliki screenshot pascapemulihan valid 640×508; isinya layar boot/logo Sony Computer Entertainment. State itu dibuat saat boot awal di sekitar `KERNEL SETUP!`, **bukan** di tengah Story Mode.
- Kesimpulan: ada bukti bahwa roundtrip savestate mentah PCSX-Redux dapat bekerja pada GitHub Actions runner. **Belum ada bukti restore checkpoint tengah Story Mode.** Workflow keseluruhan gagal pada gerbang bukti karena tahap D (checkpoint tersanitasi) masih gagal; tahap F yang lulus tidak mengubah hasil D.
- Hambatan utama yang diketahui: jalur checkpoint tersanitasi/rehidrasi crash saat loader native berjalan, sementara savestate mentah buatan emulator sendiri dapat dimuat. Penyebab tepat transformasi atau field yang memicu crash belum diketahui; perlakukan kerusakan struktur/semantik state sebagai hipotesis, bukan fakta.
- Langkah selanjutnya: bandingkan struktur/field savestate mentah buatan emulator dengan checkpoint tersanitasi setelah rehidrasi, satu faktor per eksperimen. Pertahankan checkpoint lama, jangan restart Story Mode, jangan membatalkan runner lain. Memory Card tetap prioritas sesudah restore tengah Story Mode terverifikasi. Dialog Story Mode dilewati dengan **START**, bukan Circle. Game belum terbukti tamat.
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

## STATUS TERBARU — Story Mode terverifikasi masuk ke narasi pembuka (run #39183597316, 2026-10-19)

Run [#39183597316](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39183597316) selesai dengan workflow/job `success` pada commit workflow `e9a6f985458ad2dd23c939813881918cb9a7f701`. Run lama #39178662131 tidak diulang. Artifact privat [#12158079662](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39183597316/artifacts/12158079662) telah diunduh, inventaris file diperiksa, dan screenshot aktual dilihat.

**Temuan visual yang membuktikan transisi:**
- Sequence cold boot yang terbukti diulang: Start press/release frame 2650/2680; DOWN 2710/2720; UP 2740/2750; Circle pertama 2780/2810.
- Gerbang visual `STORY_SELECT_VISUAL_GATE=PASS` pada frame 5999: crop judul Mode Select dan crop pilihan Story Mode cocok dengan fingerprint screenshot baseline yang telah diverifikasi. Karena gerbang lulus, Circle kedua benar-benar dikirim: press frame 6100 dan release frame 6130. Readback input hanya catatan pendukung, bukan dasar klaim.
- Frame 6099–6140 masih menunjukkan layar pemilihan mode dengan Story Mode tersorot dan animasi kartu. Frame 6200 dan 6399 hitam seragam; keduanya **tidak** dipakai sebagai bukti Story Mode.
- Frame 6799 menampilkan layar narasi cerita baru; layar serupa bertahan pada 7199, 7599, 7999, 8499, dan 8999. Teks terbaca: `今日は、アカデミーの卒業試験の日。` (Hari ini adalah hari ujian kelulusan Akademi.). Ini adalah bukti visual kuat bahwa konfirmasi kedua membawa game masuk ke pembukaan Story Mode, bukan hanya memilih opsinya di menu. Kesimpulan terverifikasi: **Story Mode telah dimulai sampai adegan narasi pembuka**.
- Batas kesimpulan: adegan pembuka terlihat stabil sampai frame 8999, tetapi kontrol karakter/gameplay aktif, mekanik, progres misi, dan tamat Story Mode **belum** diuji.

**Status acceptance RT-001:**
1. Title screen dan Start membuka menu — **PASS secara visual**.
2. DOWN/UP mengubah pilihan menu serta Circle pertama mencapai Mode Select — **PASS secara visual**.
3. Circle kedua setelah gerbang visual frame 5999; narasi pembuka Story Mode tampil pada frame 6799–8999 — **PASS secara visual**.
4. Kontrol karakter/gameplay aktif dan mekanik — **PENDING**.
5. Menyelesaikan/tamat Story Mode — **PENDING**.

**Konfigurasi:** log runtime mencatat BIOS SCPH-7502 (EU), CD ID `SLPS03553`, executable `SLPS_035.53;1`, dan Port 1 connected Analog/Auto. Workflow tetap mematok PCSX-Redux source `0c3572c3db75f97542001e453ae80ba8c3f8acba` dan flag `-softgpu`; konfigurasi wajib lainnya tidak diubah.

**Cleanup dan isi artifact:** log menyatakan `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`, GPU dump ter-parse lengkap (`GPU_DUMP_TRUNCATED=false`), dan workspace runtime dihapus. ZIP 7.6 MB berisi ringkasan/log, RSP summary, gerbang visual dan screenshot PNG checkpoint yang memang diperlukan sebagai bukti; tidak ditemukan file ROM, BIOS, save, raw GPU/VRAM dump, atau file mentah ber-ekstensi terkait di artifact.

**Langkah eksperimen berikutnya:** lakukan cold boot baru dan ulangi urutan lengkap sampai Story Mode. Tunggu layar pembuka tampak; screenshot menunjukkan ikon Circle di kanan bawah kotak narasi. Uji hanya satu tap Circle terkontrol (press/release terpisah) untuk mencoba melanjutkan dialog, capture tepat sebelum/sesudah, dan amati apakah adegan berikutnya/gameplay muncul. Jangan kirim input beruntun dan jangan menandai kontrol gameplay lulus sebelum ada bukti visual/gerakan karakter yang aktual.


---

## Hasil terverifikasi terbaru — D-pad berpindah; Circle mencapai Mode Select (2026-10-19)

Run [#39178662131](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39178662131) selesai dengan workflow success dan observasi mencapai VSync 6.000. Kesimpulan di bawah berasal dari screenshot aktual pada artifact privat [#12155879252](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39178662131/artifacts/12155879252), bukan dari status workflow.

- Frame 2.649–2.650: layar judul dengan prompt Start. Frame 2.670: menu memuat `はじめから` (baris pertama) dan `ロード` (baris kedua), panah awal pada `はじめから`.
- DOWN ditekan pada frame 2.710 dan dilepas 2.720. Screenshot 2.710 masih menampilkan baris pertama, tetapi pada frame 2.720 panah jelas menunjuk `ロード`: navigasi turun berhasil.
- UP ditekan pada frame 2.740 dan dilepas 2.750. Screenshot 2.740 masih menunjukkan baris kedua, sedangkan frame 2.749–2.750 memperlihatkan panah kembali ke `はじめから`: navigasi naik berhasil.
- Circle ditekan pada frame 2.780 dan dilepas 2.810. Frame 2.780 masih memperlihatkan menu; frame 2.790 overlay menu mulai menghilang, frame 2.800 overlay hilang, frame 2.900 gambar menggelap, dan frame 2.950/2.999/3.199 hitam. **Layar hitam tidak dipakai sebagai bukti mode apa pun.** Bukti visual langsung muncul pada frame 3.399: judul `モードセレクト` (“Mode Select”) terbaca, dengan `ストーリーモード` (“Story Mode”) sedang disorot/terpilih. Layar itu tetap terlihat pada checkpoint 3.599 sampai 5.999.
- Hasil visual rangkaian Start → DOWN → UP → Circle konsisten dengan konfirmasi `はじめから` dan transisi ke Mode Select. Story Mode baru **terpilih**, belum dikonfirmasi/dimasuki; gameplay dan tamat belum terbukti. `PAD_INJECT ... PASS` hanya bukti readback API, bukan bukti respons game.
- Baseline dipertahankan: BIOS retail SCPH-7502 (EU), disc `SLPS03553`, executable `SLPS_035.53;1`, PCSX-Redux pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`, SoftGPU, Port 1 Analog/Auto.
- Cleanup log mengonfirmasi `RAW_GPU_DUMP_REMOVED=1` dan `RAW_TEMP_SCREENSHOTS_REMOVED=1`; langkah `rm -rf "$WORK"` selesai. ZIP artifact berisi ringkasan/log teks dan screenshot PNG pilihan, tanpa ROM, BIOS, save, atau raw GPU/VRAM dump. Retensi artifact sampai sekitar 2026-10-22 00:43 UTC.

**Status RT-001:** title screen PASS; Start membuka menu PASS; DOWN menuju `ロード` PASS; UP kembali ke `はじめから` PASS; Circle membawa ke layar Mode Select PASS secara visual; Story Mode dimulai PENDING; gameplay/mekanik dan tamat PENDING.

**Langkah berikutnya:** eksperimen baru melakukan cold boot, ulangi Start 2.650–2.680 → DOWN 2.710–2.720 → UP 2.740–2.750 → Circle pada menu 2.780–2.810. Pertahankan observasi hingga Mode Select terlihat dan stabil (bukti sebelumnya dari frame 3.399 sampai 5.999). Setelah layar itu teridentifikasi, gunakan Circle kedua untuk mengonfirmasi Story Mode—misalnya press 6.100/release 6.130, dengan screenshot sebelum dan sesudah—dan perluas observasi hingga setidaknya frame 9.000. Jangan menyatakan Story Mode sudah dimulai sampai screenshot pasca-konfirmasi menunjukkan transisi nyata ke Story Mode/gameplay; jangan menyimpulkan dari layar hitam atau workflow success.

---

## Hasil terbaru — Start saja membuka menu dan menu bertahan sampai VSync 3000 (2026-10-19)

- Run [#39176328030](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39176328030) selesai `success` pada commit workflow `69ab7544ef7aaea40dc8af4ab12132e9997b3575`. Input sequence hanya Start press frame 2.650 dan release frame 2.680; tidak ada injeksi Circle atau tombol lain.
- Screenshot framebuffer 640×480 yang diperiksa langsung: frame 2.650 masih menampilkan judul Naruto dan prompt Start; frame 2.670 menunjukkan menu dengan panah di `はじめから` dan pilihan kedua `ロード`; frame 2.999 masih menampilkan menu yang sama. Ini kembali mengonfirmasi Start membuka menu, dan menu tetap stabil selama observasi.
- Log `PAD_INJECT` menunjukkan Start press/release terbaca oleh API, sedangkan bukti transisi game ialah perubahan visual pada screenshot sesudah Start. Artifact privat [#12155370415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39176328030/artifacts/12155370415), retensi 3 hari; raw GPU dump/temp screenshot telah dihapus dan aset runtime dibersihkan.
- Sesuai instruksi pengguna, tidak menekan Circle saat layar judul. Eksperimen ini sengaja berhenti pada menu; `はじめから` belum dikonfirmasi dan Mode Select/Story Mode belum terbukti. Langkah lanjut untuk masuk ke opsi tersebut memerlukan aksi konfirmasi terpisah setelah layar menu dikenali.

## Instruksi terbaru — gunakan Start saja, tanpa Circle (2026-10-19)

- Pengguna mengarahkan bahwa layar yang ingin diuji adalah judul Naruto dengan prompt Start dan input yang dipakai harus **Start, bukan Circle**.
- Run #39149443247 mengirim Start pada 2.650–2.680 lalu Circle pada 2.750–2.780; sesudah Circle, menu menghilang/fade lalu framebuffer hitam pada 2.900–2.999 (320×240, satu warna). Tidak ada tulisan Mode Select yang dapat dibaca, jadi tidak boleh disebut Story Mode atau Mode Select.
- Workflow berikutnya dikoreksi menjadi Start saja: tekan Start pada frame 2.650, release 2.680, tanpa Circle atau tombol lain. Checkpoint sekitar 2.649–2.800 dipakai untuk memastikan transisi dari prompt ke menu, lalu amati sampai VSync 3.000.
- Start→menu sebelumnya sudah pernah terlihat pada #39145309203; eksperimen Start-only ini mengikuti instruksi pengguna dan memastikan layar dibiarkan di menu tanpa mengonfirmasi pilihan.
- RT-001: layar judul terkonfirmasi; Start membuka menu terverifikasi pada run terdahulu; pemilihan `はじめから`, Mode Select, Story Mode, gameplay, dan tamat belum terbukti. Artifact harus tetap berisi screenshot/summary minimum; raw dump dan aset privat dihapus sebelum upload.

## Terbaru — Circle saja tidak mengonfirmasi menu karena run dimulai ulang (2026-10-18)

- Run [#39147391100](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39147391100) selesai `success` dan mencapai 3.000 VSync pada commit `5f89389d3af1f3f6254057ae8b0162667bd5eaf0`. Runtime tetap memakai retail BIOS SCPH-7502 (EU), disc `SLPS03553`, executable `SLPS_035.53;1`, PCSX-Redux pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`, SoftGPU, dan Port 1 Analog/Auto.
- Koreksi penting: setiap GitHub Actions run melakukan boot bersih. Run #39147391100 hanya mengirim Circle pada frame 2.750–2.780 dan **tidak** mengulangi Start. Screenshot frame 2.749–2.800 serta checkpoint sampai 2.999 tetap menampilkan ilustrasi title screen; prompt Start berkedip, tetapi tidak terlihat transisi ke menu atau Mode Select.
- `PAD_INJECT frame=2750 button=CIRCLE ... status=PASS` hanya membuktikan readback API emulator. Karena tombol dikirim saat title screen, ini bukan pengujian konfirmasi `はじめから`; pilihan menu tidak pernah dibuka pada run itu.
- Artifact privat [#12144726606](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39147391100/artifacts/12144726606) memuat bukti visual dan ringkasan saja. `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`, dan aset runtime dibersihkan dari runner.
- Status RT-001: Start membuka menu pada run #39145309203 tetap **terverifikasi**. Memilih mulai dari awal, Mode Select, Story Mode, kontrol gameplay, dan tamat masih **belum terverifikasi**. #39147391100 tidak membantah hasil Start sebelumnya; sesi ini tidak pernah mengirim Start.
- Eksperimen berikutnya wajib mengirim Start lalu Circle pada satu boot yang sama: Start press frame 2.650/release 2.680, Circle press 2.750/release 2.780, tanpa tombol lain; capture dekat kedua input dan amati sampai VSync 3.000.

## Terbaru — Start membuka menu utama; はじめから terpilih (2026-10-18)

- Run [#39145309203](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39145309203) selesai dengan workflow `success`; commit eksperimen `43bab6c337693eff87d5fa996d450299adc31093`. Emulator mencapai target 3.000 VSync dengan BIOS retail SCPH-7502 (EU), disc `SLPS03553`, executable `SLPS_035.53;1`, source PCSX-Redux pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`, SoftGPU, dan Port 1 Analog / Auto. Konfigurasi lain dipertahankan.
- Bukti framebuffer 640×480 aktual: frame 2.649 dan 2.650 masih menunjukkan title prompt; frame 2.660 mulai memperlihatkan kotak transisi; frame 2.670 sudah menampilkan menu dengan panah di `はじめから` dan pilihan kedua `ロード`. Menu tetap terlihat pada 2.680, 2.700, 2.750, 2.800, 2.900, 2.950, dan 2.999.
- Start ditekan frame 2.650 dan dilepas frame 2.680. Readback API lulus, tetapi bukti game memprosesnya adalah perubahan visual sesudah input: prompt title berganti menjadi menu. Circle tidak dikirim dalam run ini.
- Screenshot aktual menu hanya menunjukkan dua pilihan yang terbaca: `はじめから` dan `ロード`. Jangan menganggap `コンティニュー` tersedia pada layar ini hanya karena disebut referensi luar.
- Artifact privat [#12143433923](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39145309203/artifacts/12143433923) berisi ringkasan dan screenshot pilihan; retensi 3 hari. Log menyatakan `RAW_GPU_DUMP_REMOVED=1` dan `RAW_TEMP_SCREENSHOTS_REMOVED=1`; ROM/BIOS/raw dump tidak diunggah.
- **Kemajuan RT-001:** tujuan 1, Start membuka menu, sekarang **terverifikasi**. Tujuan 2–6 masih belum terbukti: memilih mulai dari awal, memasuki mode/story, respons gameplay yang terukur, mekanik, dan menamatkan Story Mode.
- **Langkah berikut:** pertahankan runtime yang sama. Karena panah jelas berada di `はじめから`, kirim hanya Circle/O pada frame 2.750 dan lepas pada 2.780. Ambil checkpoint rapat sebelum/sesudahnya dan amati sampai VSync 3.000. Jika mode select muncul, baca pilihan aktual dari screenshot dan jangan menekan tombol lagi sebelum layar tersebut teridentifikasi.

## Terbaru — layar judul Naruto terkonfirmasi (2026-10-18)

- Run [#39122631591](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39122631591) selesai dengan pipeline success dan menghentikan emulator sesuai target VSync 3.000. BIOS retail SCPH-7502 (EU), disc SLPS03553, dan executable SLPS_035.53;1 terdeteksi. Konfigurasi controller yang tercatat: connected=true, device_type=Analog, input_type=Auto.
- Bukti visual privat: frame 2.399 = latar berpola/copyright; frame 2.499 = ilustrasi karakter/copyright; frame 2.599 = layar judul Naruto dengan logo dan prompt Jepang STARTボタンをおせってはよ! (meminta pemain menekan Start). Prompt terlihat pada frame 2.699, 2.799, dan 2.899; pada frame 2.999 prompt tidak tampak, mungkin karena berkedip, tetapi ilustrasi judul masih sama dan belum ada menu pilihan.
- Start pada run ini dikirim pada frame 2.500, sedikit sebelum prompt judul terlihat di checkpoint 2.599. Circle/O ditekan pada frame 2.700, 2.850, 2.950, padahal prompt meminta Start. Karena itu, menu belum terbukti terbuka. Log PAD_INJECT status=PASS hanya membuktikan override API emulator terbaca kembali, bukan bahwa game memproses tombol.
- Langkah berikut: ulangi dengan BIOS/ROM/emulator/pad yang sama, tetapi kirim Start sesudah prompt title-screen muncul—misalnya frame 2.650—dan ambil checkpoint visual sering sesudahnya. Jika menu dengan はじめから (From the beginning), ロード (Load), dan コンティニュー (Continue) tampak, tekan Circle/O untuk memilih はじめから. Identifikasi mode-select sebelum mencoba masuk Story Mode.
- Status: title screen tercapai; start menu, mode select, dan Story Mode belum terbukti; Story Mode belum tamat. Raw ROM/BIOS/dump tidak diunggah; raw dump dibersihkan sebelum upload ringkasan dan checkpoint privat berumur singkat.

## Hasil terbaru — peringatan berubah menjadi layar hak cipta/latar (2026-10-18)

- Run [#39120694338](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39120694338) selesai dengan pipeline `success`, mencapai 2.400 VSync; BIOS retail **SCPH-7502 (EU)** dan executable `SLPS_035.53;1` terdeteksi. Konfigurasi pad efektif dicatat `connected=true`, `device_type=Analog`, `input_type=Auto`.
- Audit gambar framebuffer aktual memperlihatkan: frame 1.799/1.900/2.000/2.099 = peringatan kesehatan Jepang; frame 2.199 dan 2.299 = hitam; frame 2.399 = framebuffer 640×480 dengan latar bermotif dan copyright Kishimoto/Shueisha/TV Tokyo/Pierrot serta © Bandai 2003. Ini membuktikan grafik berubah setelah peringatan, tetapi tanpa logo judul/menu atau pilihan yang terbaca belum cukup untuk menandai title screen ataupun menu telah dicapai.
- Start diinjeksi pada frame 1.900 dan dilepas pada 1.930; log readback menunjukkan `PAD_INJECT ... status=PASS`. Namun, itu hanya membaca balik override input emulator, bukan respons game. Karena peringatan tetap bertahan hingga frame 2.099 lalu layar berubah beberapa ratus frame kemudian, belum dapat dipastikan apakah Start memicu transisi atau peringatan berakhir secara otomatis.
- Run lanjutan [#39122631591](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39122631591) mengamati sampai VSync 3.000, mengambil checkpoint tambahan 2.499–2.999, mengirim Start pada frame 2.500 dan Circle/O pada 2.700, 2.850, 2.950 untuk mencoba melewati prompt/menu. BIOS, ROM, emulator pin, SoftGPU, serta konfigurasi pad Analog dipertahankan.
- Status tetap **RT-001 OPEN / BELUM KONKLUSIF**. Ada kemajuan tampilan di luar splash/peringatan, tetapi judul/menu Naruto, Story Mode, respons kontrol yang terbukti, dan tamat Story Mode belum terkonfirmasi. ROM/BIOS dan raw dump tetap privat; raw dump dihapus sebelum upload artifact.

## Audit visual koreksi waktu input — run #39119261650 (2026-10-18)

- Run [#39119261650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39119261650) selesai dengan penghentian eksplisit di VSync 2.100, BIOS retail **SCPH-7502 (EU)** dan executable `SLPS_035.53;1` terdeteksi; GPUDump diparse dan file mentah dibersihkan sebelum artifact diunggah.
- Audit screenshot aktual memperjelas urutan untuk run ini: frame 1.499 **DIMPS**, frame 1.600 **DIMPS**, frame 1.700 **hitam**, frame 1.799 **peringatan kesehatan Jepang**, dan layar peringatan masih tampak pada 1.900, 2.000, serta 2.099. Jadi input Start pada frame 1.650 tidak dikirim setelah peringatan; pengujian tersebut terlalu awal. Ini mengoreksi asumsi timing sebelumnya untuk run ini.
- Log `PAD_INJECT ... status=PASS` hanya menunjukkan override internal pada API terbaca sesuai harapan; bukan bukti input diterima/diproses oleh game. PC sampler akhir banyak berada di rentang executable utama sekitar `0x800372d8` / `0x80037320`; ini konsisten dengan rutinitas berulang tetapi belum mengidentifikasi akar masalah.
- Run lanjutan aktif [#39120694338](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39120694338) mengirim Start pada frame 1.900 dan melepas pada 1.930, mempertahankan controller Analog dan semua komponen runtime lain, lalu mengamati sampai VSync 2.400. Konfigurasi pad aktual juga dicatat eksplisit di log.
- Status tetap **RT-001 OPEN / BELUM KONKLUSIF**: belum ada bukti title/menu, Story Mode, respons input yang terkonfirmasi, ataupun tamat Story Mode.

## Hasil terbaru — logo Dimps terkonfirmasi, Start timing dikoreksi (2026-10-18)

- Run [#39117084569](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39117084569) selesai dengan kesimpulan pipeline `success` dan mencapai target 1.800 VSync. Log memverifikasi retail BIOS **SCPH-7502 (EU)**, disc `SLPS03553` / executable `SLPS_035.53;1`, serta boot transfer `EXEC:PC0` + `Execute !`.
- Urutan framebuffer run ini: frame 1.100 = logo **BANDAI**, frame 1.499 = logo **Dimps**, frame 1.600 / 1.700 / 1.799 = layar peringatan kesehatan Jepang. Screenshot jendela emulator pada sekitar 700 detik juga menampilkan peringatan. Ini bukti nyata game menjalankan urutan splash internalnya; DIMPS bukan sekadar splash BIOS/PlayStation. Namun, belum terlihat judul/menu Naruto atau Story Mode.
- Koreksi eksperimen: **Start di frame 1.450 masih terlalu awal**, sebab checkpoint GPU berikutnya (frame 1.499) masih menampilkan logo Dimps dan peringatan baru tampak di frame 1.600. Circle pada frame 1.650 dan 1.750 terjadi saat peringatan sudah terlihat, tetapi tombol itu bukan tombol yang terdokumentasi untuk melewati prompt Start. Readback `PASS` hanya membuktikan status tombol dapat disetel/dibaca kembali, bukan bahwa game merespons.
- Koreksi audit untuk run [#39119261650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39119261650): frame 1.499 dan 1.600 masih logo DIMPS, frame 1.700 hitam, peringatan kesehatan pertama kali terkonfirmasi pada frame 1.799 lalu tetap terlihat pada 1.900/2.000/2.099. Karena itu Start di frame 1.650 masih terlalu awal dan belum menguji respons pada layar peringatan. Run baru [#39120694338](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39120694338) sedang menguji Start di frame 1.900, setelah peringatan terlihat, dengan konfigurasi BIOS/ROM/emulator dan controller Analog tetap sama.
- Status tetap **RT-001 OPEN / BELUM KONKLUSIF**; sudah mencapai splash Dimps dan peringatan kesehatan, tetapi title/menu, Story Mode, respons kontrol yang terkonfirmasi, serta tamat Story Mode belum terbukti. Raw GPU dump/VRAM sementara, ROM, dan BIOS tidak ikut artifact; file sementara dibersihkan.

## Jendela observasi diperpanjang dan referensi timeline — 2026-10-18

- Run [#39101435497](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39101435497) sedang menguji Start + Circle memakai SCPH-7502, pinned PCSX-Redux dan dynarec hingga VSync 900; screen captures tersebar sampai detik 410, PC-only sampling berjeda 25 detik. Input API readback hanya membuktikan injeksi, bukan respons game.
- Referensi TAS publik [video dengan bab Opening 0:00, Menu 0:23, Mission 1 0:49](https://www.youtube.com/watch?v=DfnD_mvqs7g) menunjukkan 900 VSync hanya sekitar 15 detik simulasi pada 60 Hz; bila screenshot di checkpoint 900 masih pada splash, hasil itu saja tidak membuktikan macet. Langkah selanjutnya dapat memperpanjang sampai setidaknya 1.500 VSync (25 detik simulasi) tanpa mengubah BIOS/ROM/emulator.
- Referensi [menu/kontrol game](https://github.com/juanoliveira82/naruto-ps1_translation-english/blob/master/Start-and-Main-Menu.md) memberi Start untuk melewati prompt, `はじめから` (mulai dari awal), O/Circle untuk confirm dan X/Cross untuk cancel. Itu sebabnya otomatisasi diganti dari Cross ke Start/Circle.
- **RT-001 tetap Open / blocked** sampai screenshot valid menunjukkan menu Naruto atau Story Mode; belum ada bukti game dimainkan atau tamat.

## Perbaikan strategi input — Start + Circle, bukan Cross — 2026-10-18

- Referensi kontrol spesifik game yang diperiksa pada [naruto-ps1_translation-english/Start-and-Main-Menu.md](https://github.com/juanoliveira82/naruto-ps1_translation-english/blob/master/Start-and-Main-Menu.md) menyatakan prompt awal meminta Start; opsi Start Menu berurutan `はじめから` (From the beginning), `ロード` (Load), `コンティニュー` (Continue); Mode Select mencatat **X = Return/cancel** dan **O = Confirm**. Halaman promosi resmi TV Tokyo menyebut Story Mode dan Party/Versus Mode sebagai dua mode utama: [TV Tokyo game information](https://www.tv-tokyo.co.jp/anime/naruto2002/goods/playstation.html). Jadi Cross yang dikirim probe terdahulu adalah aksi yang keliru sebagai confirm.
- Workflow pada commit [dcf31d02](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/dcf31d022e43e8eaf32c8a31ae4686720044f354) mengganti input berulang Cross dengan Start pulses pada frame 225/280 lalu Circle confirms sejak frame 320 dan berulang sampai frame 860, sambil menjalankan dynarec dan observasi 900 VSync. Run baru [#39101435497](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39101435497) menguji urutan itu; periksa hasil gambar aktual untuk membuktikan title/menu dan Story Mode, jangan menilai keberhasilan dari readback API saja.
- RT-001 tetap **Open / blocked** sampai screenshot menunjukkan menu Naruto dan terdapat respons game yang bisa diatribusikan pada input Circle/Start.

## Audit lanjutan — korelasi PC dan struktur kode sekitar sample (2026-10-18)

- Run [#39100743589](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39100743589) selesai sukses. RSP minimum berhasil tersambung; delapan sampel PC berjeda 12 detik menunjukkan BIOS pada sampel awal, lalu rentang executable utama (`0x80061cd0`, `0x80067938`, `0x8006796c`) untuk sampel berikutnya. Ini mendukung bahwa CPU mengeksekusi kode di rentang EXE saat splash Sony tetap terlihat, tetapi belum membuktikan startup/game loop selesai.
- Satu baca 64-byte per jendela kode unik menghasilkan ringkasan kategori saja. Jendela berpusat pada sampel `0x80061cd0`: 2 conditional branches, 1 backward branch yang kembali ke dalam jendela 64-byte, 3 load dan 2 store; jendela sekitar `0x8006796c`: 3 conditional branches, 1 backward branch (target di luar jendela), 3 load dan 1 store. Tidak diekspor byte instruksi, nilai register/memori, atau disassembly mentah.
- Run [#39100957600](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39100957600) memakai `-interpreter`, berbeda dengan baseline `-dynarec`. Jadi jangan menggunakan durasi/kecepatan aktual run itu untuk menilai throughput guest. Workflow diperbaiki pada commit [b4d849c4](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/b4d849c4d555f092e1d5b406bdd67c1aa5aa3205) untuk mengembalikan `-dynarec`, sambil mempertahankan RSP PC-only rendah frekuensi serta ringkasan cabang lokal. Run baru [#39101124484](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39101124484) adalah pembandingan yang sesuai.
- Kode eksekusi di RAM dan aliran GP0 aktif berarti BIOS region-lock sebagai penghalang total boot menjadi kurang mungkin, tetapi perbedaan wilayah PAL SCPH-7502 vs disc NTSC-J belum dibuktikan sepenuhnya bukan faktor. Tetap jangan menetapkan root cause berdasarkan region saja.
- **RT-001 tetap Open / blocked.** Layar yang dapat dikenali masih logo Sony/berlian, belum title/menu Naruto, input in-game belum terbukti mengubah state, dan Story Mode belum dijalankan.

## Audit lanjutan — runtime GPU dengan SCPH-7502, 2026-10-18 (run #39100404932)

- Run [#39100404932](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39100404932) selesai sukses pada tingkat workflow. BIOS SCPH-7502 diverifikasi dari asset privat; ROM dan emulator pin sama, SoftGPU, interpreter, Port 1 Analog/remap. Artifact privat [#12125949426](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39100404932/artifacts/12125949426) memuat ringkasan aman dan PNG jendela (retensi 3 hari); raw GPUDump/VRAM/temp capture sudah dihapus sebelum upload.
- GPUDump terurai tanpa truncation. Pada rentang live tercatat 299 paket VSync, 9.126 kata GP0, 1.520 kata GP1; decoder mengurai 2.413 command-family GP0 dan mencapai `end_of_stream`. Bin VSync 200–299 memiliki 4.569 kata GP0/1.702 perintah terurai. VRAM frame 299: 772 warna RGB555 berbeda dan 333.025 piksel nonblack dari 524.288.
- Jendela PCSX-Redux yang nyata masih menunjukkan berlian oranye/kuning lalu logo SONY COMPUTER ENTERTAINMENT sekitar detik 70–85; tidak ada menu/title Naruto atau gameplay. Controller `pad.setOverride/getButton` readback lulus untuk Cross/Start/Up, tetapi karena layar tetap logo, ini hanya membuktikan nilai injeksi diterima oleh API emulator, bukan respons di game.
- Kesimpulan: bukti menolak klaim bahwa GPU sama sekali tidak menerima/menjalankan perintah gambar. Akar masalah startup/handoff belum diketahui. Pesan GP0 tak dikenal dari run sebelumnya belum terbukti menyebabkan kegagalan; stream live run ini didekode sampai akhir.
- Follow-up dipasang pada commit [d1125a9b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/d1125a9b49068f5d55862a87b6c6951c0f0ca101), run [#39100743589](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39100743589): GPU/VRAM probe yang sama ditambah hanya delapan sampel PC eksternal berjeda 12 detik (tanpa breakpoint, pembacaan instruksi/memori, atau callback register di VSync) serta filter log BIOS/CD-ROM. Tujuannya mengetahui apakah PC masih di BIOS atau berada di rentang executable utama saat splash Sony tetap tampil.
- **RT-001 tetap Open / blocked; Story Mode belum dibuktikan dimulai atau tamat.** Jangan ubah BIOS, ROM, emulator pin, renderer atau runner, dan jangan unggah ROM/BIOS/raw GPU dump/VRAM/instruction traces.



## Audit lanjutan RT-001 — 2026-10-18, setelah run #39095269662

- Artifact privat #12123793795 diperiksa secara visual: screenshot jendela PCSX-Redux yang nyata (1280×800), bukan root Xvfb. Pada ~60 detik terlihat logo SONY COMPUTER ENTERTAINMENT; pada ~80 detik layar berubah menjadi bentuk belah ketupat oranye/kuning pada latar abu-abu. Tidak ada title/menu Naruto yang teridentifikasi.
- Screenshot setelah input Return dan Z pada run #39095269662 identik piksel (0 piksel berbeda; 1280×800). Ini membuktikan tidak ada respons visual pada dua input itu di state tersebut, bukan bahwa semua input controller gagal.
- A/B run #39095269662 selesai; OpenBIOS capture seluruhnya hitam/tidak menghasilkan jendela capture valid pada checkpoint terkait. Kesimpulan tetap belum konklusif.
- Audit source pada commit PCSX-Redux 0c3572c3db75f97542001e453ae80ba8c3f8acba, src/core/gpu.cc: parser GP0 untuk cmdType=0 hanya menangani command 0x01 (clear cache) dan 0x02 (fast fill); kata nonzero lainnya dicatat sebagai unknown. Log retail 'Got an unknown GPU data word: 0008a16c (cmdType: 0, command: 0)' berarti sebuah kata GP0 tidak dikenali, tetapi belum membuktikan bahwa kata itu penyebab layar tidak masuk ke game.
- GDB eksternal pada run A/B tidak menghasilkan sampel PC yang sah. Log menunjukkan server menerima paket RSP modern yang tidak didukung (Unknown GDB command: vCont?, vMustReplyEmpty, Hgp0.0, dan lainnya); beberapa koneksi berikutnya ditolak. Jangan gunakan sampel PC tersebut sebagai bukti lokasi eksekusi.
- Langkah diagnostik berikutnya: perbaiki klien RSP agar hanya mengirim paket register minimal yang telah terbukti didukung, validasi respons tanpa polling register berulang, lalu korelasikan satu sampel yang sah dengan pesan GPU dan jejak BIOS. Pertahankan emulator, commit, BIOS, ROM, runner, dan controller yang dipatok. Jangan mengklaim boot game atau Story Mode.
## Latest retail BIOS probe — SCPH-7502 verified; game screen still unconfirmed — 2026-10-18

The user uploaded `scph7502.zip` to the existing **private** release `research-emulator-pcsx-redux-2026-10-15`. Archive size is 283,463 bytes; ZIP SHA-256 is `b436489c574457560489bfaad11b2a2171c684edba34d69de107b7b26dfc0e3a`. Private workflow [#39094479973](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39094479973) safely inspected the archive and matched the embedded 524,288-byte `scph7502/scph7502.bin` against SCPH-7502 reference hashes: MD5 `b9d9a0286c33dc6b7237bb13cd46fdee`, SHA-1 `8d5de56a79954f29e9006929ba3fed9b6a418c1d`, CRC32 `318178BF`; SHA-256 is `5e84a94818cf5282f4217591fefd88be36b9b174b3cc7cb0bcd75199beb450f1`. The ZIP and extracted BIOS were not retained as workflow artifacts or committed to the repository.

Retail BIOS probe [#39094530928](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39094530928) completed successfully in GitHub Actions at 2026-10-18 03:44 UTC (10:44 WIB). It used the pinned PCSX-Redux AnyLinux build from source commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`, same private Naruto BIN/CUE, Ubuntu 26.04, Xvfb/Mesa llvmpipe, and Port 1 Analog remap. Logs explicitly report `Known BIOS detected: SCPH-7502 (EU) (318178bf)`, disc label `SLPS-03553`, ID `SLPS03553`, EXE name `SLPS_035.53;1`, PS-X Realtime Kernel 2.5 setup, and System ROM Version 4.1.

**This is not yet proof of a valid game boot.** The screen capture is black through the early checkpoints; at ~60 seconds it has only two colors, and by ~80 seconds it renders an orange/yellow diamond-like graphic on a gray field (3,109 colors), not a recognizable Naruto title/menu or gameplay screen. Return and Z were sent while the screen was black; no visible input response was established. The log later reports `ResetCallback: _96_remove ..` then `Got an unknown GPU data word: 0008a16c (cmdType: 0, command: 0)`. The emulator was stopped by the 95-second observation cap (`GUI_PROCESS_EXIT=124`); Actions conclusion `success` indicates steps and cleanup completed, not that the game passed. Private evidence artifact [#12123793795](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39094530928/artifacts/12123793795) expires 2026-10-21 03:43 UTC and contains captures/logs, not BIOS or ROM.

**Next step:** do not repeat the same 95-second GUI run unchanged and do not switch emulator/pin or keep tweaking Mesa without new evidence. Trace guest execution around `ResetCallback: _96_remove` and the unknown GPU data word, correlate the current PC and executable/overlay state with GPU command submission, then design a bounded diagnostic run that can distinguish a guest boot stall from a rendering/command-decoding issue. Keep retail BIOS and ROM private; never commit them or publish them as Actions artifacts. `RT-001` remains **Open / blocked** until a recognizable title/menu and visible controller response are proven.

## Status terbaru — host OpenGL tervalidasi, masalah guest tetap terbuka — 2026-10-18

Tes OpenGL mandiri terbaru [#39085422680](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39085422680) lulus pada runner `ubuntu-26.04`. `glxinfo -B` pada jalur default dan `LIBGL_ALWAYS_SOFTWARE=1` sama-sama melaporkan vendor Mesa, renderer `llvmpipe (LLVM 21.1.8, 256 bits)`, dan OpenGL 4.5 Compatibility Profile. Kedua override versi tidak disetel. Program GLX yang secara eksplisit meminta konteks compatibility 3.3 berhasil membuat dan mengaktifkan konteks; versi aktualnya 4.5. Log mencatat `OPENGL_33_COMPAT_CONTEXT=PASS` dan `OPENGL_DIAGNOSTIC_RESULT=PASS`. Artifact teks aman [#12120801333](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39085422680/artifacts/12120801333) menyimpan identitas renderer, versi paket, dan hasil konteks saja.

Run runtime PCSX-Redux OpenGL [#39083372634](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39083372634) mencapai VSync 300 dan exit code 0 tetapi tidak menghasilkan gambar game yang valid: 43 kata GP0/42 command (39 state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP), VRAM frame 299 satu warna RGB555 dengan 0 piksel non-hitam dari 524.288. Source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba` tidak mengimplementasikan `takeScreenShot()` pada backend `OpenGL_GPU`; `getVRAM()` tersedia. Jadi masalah generik pembuatan konteks GLX tidak didukung bukti, tetapi keadaan guest tetap belum menampilkan game.

Probe CPU/wilayah memori terbaru [#39084130154](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39084130154) selesai dan merilis artifact teks [#12119189221](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39084130154/artifacts/12119189221). Pada 14 sampel untuk load yang terkait dengan BNE `0x800372f0 → 0x80037320`, kategori effective region adalah `ram-cached` (14 hitungan); ini bukan MMIO. Dalam jendela hold 8 detik, 29 sampel PC berpusat pada dua titik loop branch yang dianalisis. Klasifikasi ini menggunakan load terbaru dalam jendela kode lokal dan bukan bukti data-flow global penuh.

**Keputusan:** jangan mengulang perubahan Mesa/versi OpenGL ataupun mengganti emulator/pin tanpa bukti baru. Fokus berikutnya adalah melacak asal dan perubahan nilai RAM yang diuji branch, lalu mengaitkannya dengan inisialisasi executable/overlay dan jalur kembali ke BIOS. Jangan menyatakan title/menu, input in-game, atau Story Mode berhasil. **RT-001 tetap Open / blocked.**

## Follow-up source-category probe — 2026-10-18, run #39083850904

Run [#39083850904](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39083850904) sukses sampai VSync 300 dan mengeluarkan artifact teks privat [#12120191058](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39083850904/artifacts/12120191058). Perbaikan [commit 8f75c3d5](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/8f75c3d558afd2261fb644e0fa192d5972ff3236) membuat CPU sampler flush statistik saat menerima SIGTERM; probe sebelumnya #39083701297 menyelesaikan emulator namun summary branch tidak sempat tertulis.

Satu sampel berkelompok pada setiap entry target:
- BNE 0x800372f0 → 0x80037320: 17 sampel unequal; operand kiri terakhir ditulis oleh kategori load, operand kanan oleh immediate arithmetic.
- BNE 0x80037330 → 0x800372d8: 15 sampel unequal; operand kiri terakhir ditulis oleh special arithmetic, operand kanan constant-zero.
- “Terakhir ditulis” merujuk penulis paling dekat yang ditemukan sebelum branch dalam jendela kode 64-byte, bukan data-flow global lengkap. Nilai register mentah, register IDs, byte instruksi dan disassembly tidak diekspor.

GP0 tetap 43 words/42 commands, dan getVRAM tetap satu warna RGB555/0 piksel non-black. Hasil ini menguatkan bahwa branch pertama membandingkan nilai yang baru dibaca oleh instruksi load, tetapi belum mengidentifikasi alamat efektif atau apakah itu RAM biasa maupun MMIO.

Hasil klasifikasi wilayah pada run [#39084130154](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39084130154) menunjukkan `ram-cached` untuk load operand kiri pada BNE pertama (14 sampel); tidak ada klasifikasi MMIO dalam ringkasan target ini. Kesimpulan hanya mencakup load lokal yang ditemukan dan jendela kode 64-byte, bukan data-flow global. Langkah berikutnya: amati apakah nilai RAM tersebut berubah selama startup, telusuri penulis terdekat dan jalur inisialisasi, serta korelasikan dengan marker loader/PC. Ekspor kategori/hitungan saja, bukan alamat efektif individual, nilai register, instruksi mentah, atau dump. RT-001 tetap Open / blocked.

## Hasil akhir sampai branch-relation test — 2026-10-18

### Host OpenGL / Mesa
Run mandiri [#39080977686](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080977686) sukses. Xvfb + Mesa llvmpipe (LLVM 21.1.8, 256 bits) membuat konteks OpenGL 4.5; konteks compatibility yang meminta 3.3 berhasil tanpa version override. Ini membuktikan lapisan GLX/Mesa host sehat, tetapi sebelumnya workflow runtime memakai flag `-softgpu`, jadi hasil standalone tidak sendiri membuktikan OpenGL backend PCSX aktif.

### Guest CPU/GPU dan loop
Run lengkap [#39080987461](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080987461) mencapai VSync 300/exit 0, tetapi hanya 43 kata GP0/42 commands: 39 GPU-state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP; tidak ada triangle/quad/line/textured-sprite. Sampling PC [#39081346569](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39081346569) menunjukkan pengulangan pada `0x80037320` dan `0x800372d8`. Static branch audit [#39082046438](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39082046438) memetakan BNE `0x800372f0 → 0x80037320` dan BNE `0x80037330 → 0x800372d8`.

Run relation [#39082587807](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39082587807) sukses: pada target-entry sample, relasi dibanding BNE pertama `unequal` sebanyak 16 kali, dan BNE kedua `unequal` sebanyak 11 kali. Delay slot tidak menulis operand yang dibandingkan menurut analisis statis. Ini konsisten dengan kedua branch terus diambil, tetapi sumber data/keadaan yang dipertahankan belum diketahui. Tidak ada nilai/register ID mentah di artifact.

### Input dan gambar/VRAM
Run [#39081872155](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39081872155): 12 pulsa tekan/lepas Cross, Start, Up semuanya dibaca kembali PASS via Lua pad API, tetapi pola PC dan GP0 tidak berubah.
Run VRAM [#39082375609](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39082375609): screenshot frame 299 320×240/16-bpp memiliki 1 warna RGB555 dan 0 piksel non-black; VRAM frame 299 (1.048.576 byte, 1024×512/16-bit) juga 1 warna dan 0 piksel non-black. Frame capture awal 235/250/265 0×0. Semua gambar/VRAM mentah dihapus sebelum artifact hanya-teks dibuat.

### OpenGL backend: extended run completed — 2026-10-18

Run [#39083372634](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39083372634) selesai success dengan pilihan backend yang eksplisit: `GPU_BACKEND_SELECTED=-openglgpu`; timeout khusus probe 170s; OpenGL vendor Mesa, renderer llvmpipe (LLVM 21.1.8, 256 bits). Emulator mencapai `GPU_TRAFFIC_VSYNC frame=300`, `GPU_DUMP_STOP observed_vsync_count=300`, dan `EMULATOR_EXIT_CODE=0`. ROM terbaca melalui SYSTEM.CNF, BOOT `SLPS_035.53`, dan marker `Execute !`.

Ringkasan tekstual artifact [#12119877576](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39083372634/artifacts/12119877576) menunjukkan GPUDump valid/tidak truncated, 299 live VSync; GP0 8 paket/43 kata, terurai jadi 42 perintah (39 GPU-state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP). Tidak ada triangle, quad, line, atau textured-sprite command. Pada frame 299, getVRAM berhasil membaca 1.048.576 byte: tepat 1 warna RGB555 dan 0 piksel non-black dari 524.288.

API `takeScreenShot()` gagal pada frame 235/250/265/299; ini sesuai source pin karena `OpenGL_GPU` tidak override metode screenshot tersebut. Capture mentah VRAM, screenshot dan GPUDump dihapus di runner sebelum artifact tekstual dibuat. API pad virtual tetap membaca balik 12 aksi press/release Cross/Start/Up sebagai PASS, tetapi pola GP0 dan VRAM tidak menunjukkan respons game.

Run [#39082912598](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39082912598) ternyata memilih `-softgpu`, bukan OpenGL; jangan jadikan bukti. Selektor diperbaiki pada [commit eb9cb4d2](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/eb9cb4d250c48a926f672b298cc51e2babf29a75), timeout untuk commit bertanda probe diperpanjang pada [commit ca472985](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/ca4729858e8f008660984b0c252ecbceb4463eae). Commit biasa tetap memilih Software GPU.

**Kesimpulan:** host Mesa/GLX dan backend OpenGL PCSX-Redux keduanya bisa berjalan di runner tanpa GPU fisik. Penghambat yang terukur sekarang berada pada sisi guest/game: loop CPU berulang, hampir tidak ada perintah gambar, dan VRAM masih hitam. RT-001 tetap Open / blocked karena belum ada gambar game/title/menu yang valid atau perubahan state game yang dibuktikan akibat input.

**RT-001 tetap Open / blocked:** belum ada screenshot game valid/title/menu dikenali, ataupun bukti game-state berubah karena input. Emulator, AppImage, BIOS dan pin tidak diubah. Setelah OpenGL backend tervalidasi, langkah berikutnya harus menelusuri sumber nilai yang membuat siklus BNE bertahan, bukan kembali mengulang tes Mesa mandiri.


## Hasil PC sampling adaptif di hotspot — 2026-10-18 (Actions #39081346569)

Run [#39081346569](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39081346569) selesai sukses sampai VSync 300, emulator exit code 0. Artifact privat teks [#12118099416](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39081346569/artifacts/12118099416) hanya memuat statistik; raw GPUDump dihapus dan baris sampel cepat tidak disimpan.

Sampler menaikkan laju nominal ke 0,1 s setelah PC masuk rentang 0x800372c0–0x800373ff, menahan mode cepat selama 8 s sejak sampel terakhir di rentang tersebut. Hasil: 31 sampel cepat, seluruhnya di dalam rentang, hanya dua PC unik: 0x80037320 sebanyak 17 sampel dan 0x800372d8 sebanyak 14 sampel. Histogram transisi: 0x80037320→0x80037320 sebanyak 10; 0x800372d8→0x800372d8 sebanyak 7; 0x80037320→0x800372d8 sebanyak 7; 0x800372d8→0x80037320 sebanyak 6. Hasil ini mendukung pola eksekusi/loop yang sangat berulang di sekitar dua alamat itu, tetapi belum membuktikan branch mana yang dieksekusi atau penyebab game tidak maju.

GPUDump tetap sama: 299 live VSync packets; 43 GP0 words / 42 commands, semuanya dalam bucket VSync 200–299; 39 GPU-state-setting, satu clear-cache, satu monochrome rectangle, satu NOP; tanpa triangle/quad/line/textured-sprite command. Jadi sampling lebih rapat belum menghasilkan gambar title/menu atau perubahan input yang terbukti.

Probe pembeda berikutnya sudah terpicu: [Actions #39081524928](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39081524928), yang menghitung edge control-flow statis di jendela hotspot tanpa menerbitkan byte instruksi/disassembly. **RT-001 tetap Open / blocked.**

## Hasil RSP memory-window control-flow summary — 2026-10-18 (Actions #39080987461)

Run [#39080987461](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080987461) menyelesaikan target VSync 300 dan semua cleanup dengan conclusion workflow `success`; emulator exit code 0. RSP tersambung (`qSupported=ok`) dan mengumpulkan 75 sampel bulk register valid sampai sekitar t=98.62s. Marker yang dibaca dari `pcsx.log`: SYSTEM.CNF ~4.66s, BOOT path ~5.95s, EXEC header dan `Execute !` ~36.75s. PC kembali dominan di BIOS setelah ~t=40s sampai ~t=87.73s, lalu muncul lagi di executable mulai ~t=89.01s.

Pembacaan empat jendela memori 64-byte di alamat executable berhasil, tetapi artifact hanya berisi kategori/count; tidak ada instruksi mentah, operand, atau dump memori:
- `0x80050b00`: 0 conditional branch, 0 jump, 2 load, 6 store, 4 immediate arithmetic, 4 special arithmetic.
- `0x8003c080`: 2 conditional branch (keduanya forward), 4 jump, 1 load, 5 immediate arithmetic, 4 special arithmetic.
- `0x80037300`: 1 conditional branch dengan satu backward-branch pada jendela 64-byte, 3 jump, 2 load, 4 immediate arithmetic, 6 special arithmetic.
- `0x800372c0`: 2 conditional branch (keduanya forward), 1 jump, 3 load, 2 store, 3 immediate arithmetic, 5 special arithmetic.
Tidak ditemukan kategori syscall/break/COP0/COP2 dalam keempat jendela ini. Ini statistik isi jendela statis, bukan bukti bahwa branch tertentu pasti dieksekusi. Namun PC runtime mengulang `0x80037320` dan `0x800372d8` di akhir pengamatan, sehingga area `0x800372c0–0x8003733f` layak untuk sampling PC yang lebih rapat.

GPUDump tetap lengkap (299 VSync live packets, 43 GP0 words; semua GP0 hanya pada bin VSync 200–299: 39 GPU-state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP; tidak ada primitive triangle/quad/line/textured sprite). Screenshot Software GPU 320×240 dan capture window X11 1280×800 tetap hitam. Dump mentah dihapus; artifact privat hanya ringkasan/log.

Langkah selanjutnya: ubah sampler RSP agar mengurangi interval jeda hanya ketika PC berada di `0x800372c0–0x800373ff` (tetap simpan hanya PC/CP0 dan histogram kategori) untuk menguji apakah PC mengulang pola yang konsisten; jangan menambah trace instruksi mentah. **RT-001 tetap Open / blocked**.
## Run CPU/GPU terbaru selesai — 2026-10-18 (Actions #39080987461)

Run [#39080987461](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080987461) selesai dengan status success, mencapai target VSync 300 dan keluar normal (EMULATOR_EXIT_CODE=0). Artifact yang diunggah hanya ringkasan teks privat [artifact #12118148960](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080987461/artifacts/12118148960); raw GPUDump dihapus.

GPUDump valid, tidak truncated: 299 live VSync packets; GP0 8 packets / 43 words, GP1 11 packets / 16 words, ThrowAway 5 packets / 5 words. Semua 43 live GP0 words terparse sebagai 42 commands: 39 GPU-state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP. Semua GP0 berada pada bucket VSync 200–299; bucket 0–199 nol. Tidak ada triangle, quad, line, atau textured-sprite command. Marker GPU melaporkan guest FPS 0 pada frame 100/200 dan 1.0 pada frame 300.

RSP terhubung; qSupported sukses; 75 pembacaan bulk register valid (index 0–74). Marker EXEC header dan Execute ! muncul sekitar t=36.75 s; PC memasuki executable pada t=37.03 s (0x80050b30) serta t=38.68 s (0x8003c0b4), lalu sampel kembali dominan ke BIOS sekitar t=40.28–87.73 s (0xbfc03bxx/0xbfc075xx–0xbfc076xx), dan masuk ke executable lagi t=89.01–98.62 s (0x80037320/0x800372d8). Status CP0 umumnya 0x40000401, BadVAddr nol, Cause umumnya 0x400; beberapa sampel Cause 0x20 tidak cukup untuk menetapkan exception/penyebab.

Ringkasan kelas instruksi untuk jendela lokal 64-byte (tanpa byte instruksi atau disassembly mentah):
- 0x80050b00: branch 0, load 2, store 6, immediate arithmetic 4, special arithmetic 4.
- 0x8003c080: conditional branch 2, forward branch 2, jump 4, load 1, immediate arithmetic 5, special arithmetic 4.
- 0x80037300: backward branch 1, conditional branch 1, jump 3, load 2, immediate arithmetic 4, special arithmetic 6.
- 0x800372c0: conditional branch 2, forward branch 2, jump 1, load 3, store 2, immediate arithmetic 3, special arithmetic 5. Tidak terhitung syscall, break, COP0, atau COP2 pada keempat jendela tersebut.

Interpretasi: ini memperkuat bahwa runner GLX bukan hambatan utama; guest mencapai executable sesaat tetapi mengirim hampir tidak ada perintah gambar GP0 sampai VSync 300. Statistik lokal saja belum membuktikan loop tertentu ataupun penyebab kembali ke BIOS. Langkah berikutnya: tingkatkan korelasi transisi PC/branch target secara ringkas dan aman, tetap hindari log byte mesin/disassembly; jangan kembali ke diagnosis GLX dan jangan mengganti emulator/pin. **RT-001 tetap Open / blocked** karena belum ada gambar game, title/menu yang dikenali, atau perubahan state yang dibuktikan berasal dari input controller.


---

## Validasi ulang OpenGL host (mandiri) — 2026-10-18, Actions #39080977686

Run [#39080977686](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080977686) selesai dengan status success setelah workflow naruto-opengl-diagnostic.yml menambahkan validasi field vendor, renderer, dan versi untuk laporan GLX default serta software. Commit: [cf16162c](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/cf16162c85001d1006fee32725ce01407843ac35).

Bukti log:
- Xvfb siap pada :99; MESA_GL_VERSION_OVERRIDE dan MESA_GLSL_VERSION_OVERRIDE keduanya tidak disetel.
- GLX default dan software melaporkan vendor Mesa, renderer llvmpipe (LLVM 21.1.8, 256 bits), Compatibility Profile 4.5 serta Core Profile 4.5; marker GLXINFO_DEFAULT_CONTEXT=PASS dan GLXINFO_SOFTWARE_CONTEXT=PASS.
- Tes GLX C meminta konteks OpenGL 3.3 compatibility; konteks berhasil dibuat dan diaktifkan. Versi aktual dari glGetString(GL_VERSION) adalah 4.5 (Compatibility Profile) Mesa 26.0.8-1ubuntu0.3; marker OPENGL_33_COMPAT_CONTEXT=PASS dan OPENGL_DIAGNOSTIC_RESULT=PASS.

Interpretasi: lapisan host Xvfb/GLX/Mesa tervalidasi dan dapat membuat konteks compatibility yang diperlukan tanpa override versi. Ini tidak menunjukkan bahwa title/menu Naruto tampil dan tidak membebaskan RT-001 dari kriteria gambar game + respons input.

Audit source persis pada pin PCSX-Redux 0c3572c3db75f97542001e453ae80ba8c3f8acba:
- [src/core/gpu.h](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/gpu.h) mendefinisikan implementasi dasar GPU::takeScreenShot() yang melempar “Not yet implemented”; jangan menganggap API screenshot tersebut tersedia pada setiap backend.
- [src/gpu/soft/gpu.cc](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/gpu/soft/gpu.cc) mengisi lebar/tinggi screenshot Software GPU dari DisplayEnd - DisplayPosition. Dimensi 0×0 dari jalur ini konsisten dengan rentang display guest yang belum valid, bukan bukti kegagalan GLX.
- [src/core/pcsxlua.cc](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/pcsxlua.cc) meneruskan PCSX.GPU.takeScreenShot() ke backend GPU; binding getVRAM() tersedia untuk tes VRAM terpisah.

Arah lanjutan: jangan mengulang diagnosis GLX atau mewajibkan GPU fisik. Fokus berikutnya adalah kondisi guest (GPU PS1 display/VRAM dan eksekusi CPU) serta pemeriksaan hasil runtime terakhir sebelum mengubah harness. RT-001 tetap Open / blocked.

---

## Hasil histogram GP0 per rentang VSync — 2026-10-18 (Actions #39080239541)

Run [#39080239541](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080239541) selesai dengan target VSync 300 dan exit code 0. Dump GPU ter-parse lengkap/not truncated, 299 VSync live packets. Bucket GP0 berbasis jumlah VSync live:
- 000–049: 0 words / 0 commands.
- 050–099: 0 words / 0 commands.
- 100–199: 0 words / 0 commands.
- 200–299: 43 words, seluruhnya terparse (42 commands): 39 GPU-state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP; stop reason `end_of_stream`. GP1 live: 16 words; ThrowAway: 5 words. Tidak ada family triangle/quad/line/textured sprite pada capture ini. Dump mentah dihapus; artifact privat hanya menyimpan ringkasan hitungan dan status CPU.

Sampler CPU per run mencatat marker `Execute !` sekitar t=38.01s; PC masuk executable pada t=38.33–40.91s, lalu kembali ke BIOS mulai sekitar t=42.20s, dan masuk executable lagi sekitar t=88.39–98.63s. Semua GP0 words berada di bucket 200–299, selaras dengan kemunculan CPU di executable menjelang akhir observasi. Marker timestamp dari `pcsx.log` dipakai agar buffering stdout tidak merusak korelasi. Ini bukti urutan yang konsisten, belum membuktikan penyebab CPU meninggalkan executable atau mengidentifikasi monochrome rectangle secara visual.

Langkah berikutnya: saat RSP tersambung, ambil window memori kecil secara privat di sekitar PC executable yang sudah teramati (`0x8003717c`, `0x8003c0b4`, `0x80037320`, `0x800372d8`) dan ekspor hanya statistik kategori instruksi/cabang (mis. syscall, branch, jump, load/store, backward-branch count)—tidak pernah menulis byte mesin/disassembly mentah. Tujuannya memeriksa apakah alamat tersebut bagian dari loop tunggu atau jalan kembali ke BIOS. **RT-001 tetap Open / blocked.**
## Hasil korelasi CPU/GP0 dengan marker bertimestamp — 2026-10-18 (Actions #39079981314)

Run [#39079981314](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079981314) selesai dengan conclusion `success`; emulator mencapai target VSync 300 lalu dihentikan normal oleh probe (`EMULATOR_EXIT_CODE=0`). Aset privat serta hash BIOS/ROM/AnyLinux diverifikasi. Tidak ada raw GPUDump atau instruksi/operand mentah di artifact.

**GPUDump setelah TraceBegin:** 299 VSync packets / 598 words; GP0 8 packets / 43 words; GP1 11 packets / 16 words; ThrowAway 5 packets / 5 words; truncated=false. Pretrace GP0 baseline 262153 words adalah reset + VRAM upload untuk state awal dump, bukan rendering game. Parser sementara mengonsumsi semua 43 live GP0 words tanpa sisa dan mengklasifikasikannya sebagai 42 perintah: GPU-state-setting=39, clear-cache=1, monochrome-rectangle=1, NOP=1. Tidak ada keluarga triangle, quad, line, atau textured sprite pada jendela sampai VSync 300. Ini berarti ada sedikit traffic grafis, tetapi belum ada gambar yang terlihat; screenshot Software GPU 320×240 dan screenshot jendela X11 1280×800 tetap hitam pada run sebelumnya.

**Korelasi CPU:** RSP tersambung; `qSupported` berhasil; 76 paket bulk register valid sebelum target berhenti. Marker log yang kini ditimestamp dari `pcsx.log`: SYSTEM.CNF sekitar t=4.85s, BOOT path t=6.14s, EXEC header dan `Execute !` sekitar t=38.01s. Sampel PC segera sesudahnya masuk ke executable utama (t=38.33s `0x8003717c`, t=39.62s `0x8003c0b4`, t=40.91s `0x80037320`), lalu kembali ke BIOS range mulai sekitar t=42.20s. Sampel berada di BIOS sampai sekitar t=87.09s dan masuk lagi ke executable pada t=88.39s (`0x800372d8`), dengan beberapa sampel lanjutan di `0x80037320/0x800372d8` hingga t=98.63s. CP0 Status umumnya `0x40000401`, BadVAddr nol, Cause umumnya `0x400`; dua sampel Cause `0x20` tidak cukup untuk menyimpulkan root cause tanpa sampling lebih rapat. Timestamp dari `pcsx.log` dipilih karena stdout buffered; jangan gunakan timestamp marker lama dari stdout sebagai korelasi akurat.

Interpretasi: host Mesa/GLX sehat; guest CPU masuk ke executable sebentar-sebentar tetapi pada jendela sekitar 100 detik hanya mengirim 43 GP0 words (kebanyakan state command, satu monochrome rectangle), dan tidak menampilkan title/menu. Ini lebih konsisten dengan masalah inisialisasi/looping guest daripada kebutuhan GPU fisik, tetapi akar sebab belum dipastikan. Probe berikutnya akan mengelompokkan waktu GP0 command berdasarkan VSync range agar terlihat apakah semuanya hanya terjadi saat startup.

**RT-001 tetap Open / blocked.** Belum ada title/menu yang dikenali, perubahan state dari input yang diverifikasi, atau Story Mode.
## Hasil final GPUDump sampai timeout dan probe korelasi CPU berikutnya — 2026-10-18

Run [#39079291837](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079291837) selesai dengan conclusion Actions `success` (semua langkah/cleanup berhasil), tetapi proses emulator berakhir pada batas observasi 90 detik (`EMULATOR_EXIT_CODE=124`); jangan mengartikan status workflow sebagai game sukses boot. Log mencapai `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, `EXEC:PC0(80011448)` dan `Execute !`. GPU traffic dump ter-parse lengkap, `GPU_DUMP_TRUNCATED=false`, satu marker `TraceBegin`, dan 268 VSync packets / 536 live words. Sesudah TraceBegin: **GP0 packets=0, words=0; GP1 packets=1, words=1; VSync packets=268**. Baseline pre-trace GP0 262153 words berisi reset dan full 1024×512 VRAM upload untuk merekonstruksi keadaan awal dump, bukan gambar yang dikirim game. Dump mentah dihapus sebelum upload artifact, yang hanya menyimpan ringkasan teks/log. Emulator timeout 124 adalah batas observasi, bukan crash diagnosis.

Untuk menghubungkan hasil grafis dengan CPU, workflow [`naruto-fastboot-gpu-traffic-summary.yml`](.github/workflows/naruto-fastboot-gpu-traffic-summary.yml) kini diperbarui agar satu run men-sample bulk RSP register `g` (PC + CP0 Status/BadVAddr/Cause) dengan timestamp relatif dan marker loader sambil merekam GPUDump, tanpa instruksi/operand mentah. Commit terbaru [`30cd69d6`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/30cd69d61a5ab01761baa7f3a209a386f205b650); run konfirmasi [#39079600379](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079600379) terakhir terlihat pending di antrean ketika entri ini dibuat. Periksa log/run selesai sebelum menafsirkan sampel itu.

Kesimpulan tetap terbatas: host GLX/Mesa sehat; jendela emulator dan screenshot software GPU hitam; tak ada GP0 drawing command yang terekam pada 268 VSync pasca-TraceBegin. Ini menunjuk ke inisialisasi/eksekusi game tamu, tetapi tidak menentukan akar sebab. **RT-001 tetap Open / blocked.**
## Pembuktian GL host dan traffic GPU tamu — 2026-10-18

- Run OpenGL mandiri [#39049689832](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39049689832): Mesa `llvmpipe (LLVM 21.1.8, 256 bits)`, OpenGL 4.5 Core/Compatibility Profile, tanpa version override; konteks Compatibility 3.3 berhasil dibuat. Host GLX/Mesa sehat, dan belum ada alasan teknis untuk menuntut GPU fisik.
- Source build pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`: `GPU::takeScreenShot()` bawaan melempar `Not yet implemented`; backend OpenGL GPU tidak mengimplementasikannya, sedangkan Software GPU punya implementasi screenshot. Run [#39078905140](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078905140) dengan `-softgpu` menghasilkan screenshot frame 300 valid 320×240 tetapi seluruh piksel hitam; VRAM 1024×512 juga satu warna hitam.
- Run window capture [#39079066598](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079066598) mengambil enam screenshot jendela PCSX-Redux non-root XID `0x200034` pada t=5,15,30,45,60,75 detik. Semuanya valid 1280×800 namun seragam hitam. Tidak ada title/menu.
- GPUDump summary parsial dari run [#39079279565](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079279565) (run berhenti/cancel saat workflow diperbarui) berhasil mem-parse dump sampai 136 live VSyncs tanpa truncation. Sesudah TraceBegin: `GP0 packets=0, words=0`, `GP1 packets=1, words=1`, `VSync packets=136, words=272`. Baseline pre-trace berisi 262153 GP0 words karena reset/full VRAM upload untuk merekonstruksi state dump; angka itu bukan trafik gambar game. Raw GPU dump dihapus; artifact privat hanya summary/log.
- Run konfirmasi dengan workflow saat ini [#39079291837](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079291837) sedang merekam sampai target VSync 300 saat catatan dibuat; periksa hasil finalnya sebelum menyatakan hasil penuh.

Interpretasi sementara: masalah yang terlihat tidak lagi cocok dengan kegagalan pembuatan konteks OpenGL host. Data mengarah bahwa executable tamu mencapai marker `Execute !`, tetapi belum mengeluarkan perintah gambar GP0 selama jendela yang direkam. Ini belum mengidentifikasi penyebab di CPU/game loader. RT-001 tetap **Open / blocked**: title/menu dan respons input belum terbukti; Story Mode belum dimulai.
## Lanjutan diagnosis VRAM dan callback UI — 2026-10-18

Run [#39050174557](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39050174557) memakai timer rekursif melalui `PCSX.nextTick()`, tetapi tidak menghasilkan checkpoint (`NO_VALID_TIMED_CAPTURES`). Audit source pada pin `0c3572c3db75f97542001e453ae80ba8c3f8acba` menjelaskan kelemahan harness: `PCSX.nextTick()` menyimpan callback di `AfterPollingCleanup`; pada `src/core/ui.cc`, `UI::tick()` menjalankan callback tersebut lalu membersihkan field yang sama. Penjadwalan ulang dari callback itu dapat tertimpa. Kegagalan ini adalah kegagalan metode sampling, bukan bukti kegagalan OpenGL.

Run [#39078592809](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078592809) mengambil sembilan sampel VRAM langsung saat `GPU::Vsync`: frame 1, 2, 3, 5, 10, 20, 30, 45, dan 60. Semua buffer berukuran 1.048.576 byte, hanya memiliki satu warna 15-bit, rasio non-black 0, dan hash PNG yang identik. Guest FPS bernilai 0 pada checkpoint itu. Namun, semua snapshot tersebut berada sebelum marker log `Execute !`; run kemudian mencatat `GPU::Vsync frame=300 guest_fps=1.0000` setelah handoff. Karena itu, sampel hitam tersebut hanya membuktikan VRAM awal yang kosong sebelum executable berjalan, bukan keadaan pasca-handoff. Run berakhir pada timeout 90 detik (124), lalu menghapus buffer mentah; artifact privat hanya berisi PNG/summary.

Capture langsung dari event GPU bukan pola yang akan diteruskan karena API readback OpenGL perlu dijalankan pada thread UI/konteks grafis yang benar. Workflow telah diubah lagi pada commit [`3a69fcef`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/3a69fcef242563ecf45de8c920bec3443db3e956) untuk menjadwalkan capture dari event ke thread UI melalui `PCSX.nextTick()`, tanpa timer rekursif. Run [#39078732160](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078732160) menguji versi deferred itu pada frame 1 dan 60; status terakhir yang diperiksa: masih berjalan, belum ada hasil yang boleh disimpulkan.

**RT-001 tetap Open / blocked.** Belum ada title/menu yang dikenali dan belum ada perubahan state akibat input yang terverifikasi. Perlu capture pasca-handoff (target VSync sekitar 300, sebagaimana marker runtime) sebelum mengubah hipotesis gameplay/rendering.
## Hasil diagnosis OpenGL mandiri — 2026-10-17 (Actions #39049689832)

Run [#39049689832](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39049689832) menambahkan dan menjalankan workflow mandiri `.github/workflows/naruto-opengl-diagnostic.yml` pada commit [`3e92e100`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/3e92e100abf17a51e4e335e92ea7b70632293933). Hasil: job `mesa-opengl` **success**. Xvfb dan GLX siap; tes `glxinfo -B` sukses baik pada konfigurasi default maupun saat `LIBGL_ALWAYS_SOFTWARE=1`. Keduanya melaporkan OpenGL vendor `Mesa`, renderer `llvmpipe (LLVM 21.1.8, 256 bits)`, OpenGL 4.5 Compatibility Profile dan Core Profile (Mesa 26.0.8); capability report menyatakan max core/compat 4.5. Variabel `MESA_GL_VERSION_OVERRIDE` dan `MESA_GLSL_VERSION_OVERRIDE` tidak disetel. Program GLX C kecil juga membuat/mengaktifkan konteks compatibility yang meminta OpenGL 3.3, lalu membaca versi aktual 4.5; marker `OPENGL_33_COMPAT_CONTEXT=PASS`.

Interpretasi: runner cloud ini dapat membuat konteks OpenGL yang memadai melalui Mesa software rendering; tidak ada bukti GPU fisik diperlukan. Hasil sebelumnya `takeScreenShot()` 0×0 harus dipisahkan dari kesehatan GLX. Source PCSX-Redux yang tepat pada commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`, `src/gpu/soft/gpu.cc`, menghitung dimensi screenshot dari `DisplayEnd - DisplayPosition`; dimensi kosong dapat berarti register display GPU PlayStation belum menginisialisasi rentang gambar. `src/core/pcsxlua.cc` menyediakan `PCSX.GPU.getVRAM()`, jalur diagnosis berikutnya untuk memeriksa VRAM emulasi terpisah dari display screenshot.

Run visual sebelumnya [#39047765424](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39047765424) tetap gagal menghasilkan gambar: satu metadata frame menyatakan ukuran/dimensi 0×0, summary `NO_VALID_GPU_SCREENSHOTS`, emulator dihentikan oleh batas 90 detik (exit 124). Kesuksesan workflow bukan keberhasilan game boot. Belum ada title/menu maupun perubahan state akibat input yang terkonfirmasi.

**Langkah berikutnya:** pertahankan AnyLinux AppImage dan pin yang sama; ambil checkpoint VRAM 1024×512 melalui `PCSX.GPU.getVRAM()` setelah VSync dan konversi di runner ke gambar diagnostik. Jangan sertakan raw VRAM/dump mentah di artifact. Bandingkan beberapa checkpoint sebelum/sesudah input dan catat hanya screenshot diagnostik privat serta statistik ringkas. Jika VRAM kosong/tidak berubah, lanjutkan korelasi dengan polling PC/CP0 dan marker loader—bukan mengganti emulator atau menyimpulkan GPU fisik diperlukan.

**RT-001 tetap Open / blocked.**

---

## Diagnosis CPU polling dan keputusan probe berikutnya — 2026-10-17 (Actions #39029860914)

Run [#39029860914](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39029860914) menyelesaikan semua langkah workflow (`success`), termasuk unggah artefak privat dan cleanup. Emulator yang diuji adalah PCSX-Redux AnyLinux AppImage dengan OpenBIOS fastboot, ROM serta BIOS yang SHA-256-nya diverifikasi, setup Port 1 Analog/remap, dan command line `-exec ... -gdb -gdb-port 3333 -run`. Tidak ada breakpoint atau watchpoint pada eksperimen ini.

Klien RSP minimal tersambung dan `qSupported` berhasil. Polling menghasilkan 41 sampel selama sekitar 65 detik, dengan 14 nilai PC unik. Distribusi: rentang BIOS 31 sampel; rentang executable utama `0x80010000–0x8006d7ff` sebanyak 2; alamat lain sebanyak 8. PC sempat terlihat di `0x8003c0a0` pada sekitar 36,3 detik dan `0x8003bff4` pada sekitar 37,9 detik sejak polling dimulai, kemudian sampel pada sekitar 39,5 detik dan seterusnya kembali berada di BIOS, banyak di `0xbfc075b0–0xbfc07608`. Marker loader `SYSTEM.CNF`, `BOOT = cdrom:\SLPS_035.53;1`, `EXEC:PC0(80011448)`, dan `Execute !` ada di log, tetapi waktu marker tidak direkam di dalam jendela polling. Korelasi waktunya adalah petunjuk, bukan bukti sebab-akibat yang tuntas.

CP0 pada pembacaan bertahap: `BadVAddr=0`; `Status` biasanya `0x40000401` (satu sampel `0x40000000`); `Cause` biasanya `0x00000400`, dengan dua sampel `0x00000020`. Ini bukan snapshot atomik karena PC dan setiap CP0 dibaca melalui paket RSP terpisah. Query `?` menghasilkan `S00`; source GDB-server pada commit AppImage `0c3572c3db75f97542001e453ae80ba8c3f8acba` menyatakan `S00` adalah jawaban query ketika emulator masih running, **bukan stop event**. Jangan menyebut hasil ini sebagai exception loop yang sudah terbukti.

Audit source yang sesuai build: [src/core/gdb-server.cc pada commit 0c3572c3](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/gdb-server.cc) mendefinisikan urutan register RSP; `g` mengembalikan paket semua register, dengan indeks 32=Status, 35=BadVAddr, 36=Cause, dan 37=PC. Karena itulah langkah pembeda berikutnya adalah satu pembacaan bulk `g` per sampel (576 karakter hex untuk 72 register 32-bit), plus cap waktu marker loader yang diamati langsung dari log. Ini mengurangi ketidakselarasan waktu dari query bertahap dan menghubungkan transisi PC dengan `Execute !` tanpa mengulang breakpoint/GPU-watchpoint.

Ringkasan bertanda `CPU_SAMPLER_EXIT=124` dalam log adalah salah label harness: heredoc Python polling berjalan di foreground, sedangkan `$!` masih merujuk proses emulator `timeout`; nilai 124 berasal dari batas observasi emulator 100 detik. Bukti bahwa sampler bekerja adalah 41 baris `CPU_SAMPLE`, diikuti `CPU_SUMMARY`; proses emulator terdeteksi selesai dan cleanup berhasil. Perbaiki label dan pengelolaan PID pada workflow berikutnya.

Artefak privat: [#12100266232](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39029860914/artifacts/12100266232), retensi sampai 2026-10-20 11:46:41 UTC. ROM, BIOS, emulator dan log sementara telah dibersihkan dari runner.

**RT-001 tetap Open / blocked.** Title/menu Naruto, respons input gameplay, dan Story Mode belum terbukti; belum ada aturan gameplay runtime yang boleh ditetapkan.

---

## Hasil Actions terbaru — 2026-10-17 (run #39021127913)

Run [#39021127913](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39021127913) telah selesai dengan status GitHub Actions `success`; itu hanya menandakan langkah workflow dan cleanup selesai, bukan game berhasil boot sampai menu.

Bukti runtime yang terkonfirmasi:
- Klien RSP tersambung ke PCSX-Redux port 3333; `qSupported` sukses dan breakpoint `Z1,80011448,4` mendapat balasan `OK`.
- Konfigurasi eksperimen sudah memasukkan upaya setup controller Port 1 Analog dan remap yang juga dipakai pada probe sebelumnya.
- Log PCSX-Redux mencatat disc `SLPS-03553`, `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, `EXEC:PC0(80011448) T_ADDR(80010000) T_SIZE(0005d800)`, dan `Execute !`.
- Walaupun loader mencatat handoff executable, selama jendela tunggu 40 detik tidak ada stop event breakpoint yang sah. Ctrl-C RSP kemudian menghasilkan `T05`; sampel register sesudah interrupt menunjukkan PC `0x80000080`, CP0 Status `0x40000404`, BadVAddr `0x00000000`, Cause `0x00000400`. Nilai tersebut hanya snapshot ketika interrupt/handler, bukan diagnosis root cause.
- Karena kondisi entry `PC == 0x80011448` tidak pernah diverifikasi, workflow dengan benar **tidak** meneruskan GPU GP0/GP1/DMA2 watchpoints. Jangan menyebut GPU watchpoint hit atau menyimpulkan bahwa game sudah menjalankan rendering.
- Run ini tidak mengambil bukti visual baru. Hasil capture terdahulu tetap layar hitam; title/menu serta respons input belum terbukti.

Artifact privat `naruto-fastboot-gpu-watchpoints-private` (ID `12096697815`) tersedia sampai sekitar 2026-10-20 09:28 UTC. ROM, BIOS, emulator, log dan file sementara telah dibersihkan dari runner.

**Langkah berikutnya:** hentikan sementara eksperimen breakpoint/watchpoint karena breakpoint remote belum terbukti bisa menangkap entry meskipun balasan pemasangan `OK`. Gunakan command line baseline yang telah terbukti mencapai `Execute !` dengan `-exec` Port 1 Analog setup **dan** `-run`, lalu lakukan polling register PC/CP0 minimal dan rapat selama boot (tanpa GDB modern; gunakan klien RSP minimal yang sudah berhasil). Korelasikan sampel PC dengan marker loader untuk menentukan apakah CPU masuk ke kode EXE, tetap berputar di BIOS/exception vector, atau berpindah bolak-balik. Jangan mulai GPU watchpoint lagi sebelum mekanisme breakpoint diverifikasi terpisah dan jangan mengulang tes backend grafis.

**RT-001 tetap Open / blocked.** Story Mode belum dimulai/tamat; jangan menetapkan aturan gameplay berdasarkan dugaan.

---

## Koreksi validitas RSP GPU-watchpoint dan rerun — 2026-10-17

Audit run [#39017636267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017636267) menemukan hasil “entry breakpoint” dan “GPU GP0 watchpoint hit” **tidak valid sebagai hit yang terkonfirmasi**: klien RSP menganggap paket konsol PCSX-Redux berawalan `O` (mis. teks `PCSX::MIPS>`) sebagai stop event. Pada run itu, PC yang dibaca setelah event tetap berada di BIOS (`0xbfc0867c` dan `0xbfc05784`), bukan di entry executable Naruto. Karena itu entry breakpoint belum terbukti tercapai dan GP0 belum boleh dinyatakan terpicu. Watchpoint GP1/DMA2 juga hanya timeout dalam uji terdahulu. Workflow berakhir `success` hanya berarti harness dan cleanup selesai; bukan hasil positif target.

Workflow diperbaiki pada commit `5055074671acf8cb2f2512182f8484dc2815552d`: parser kini mempertahankan buffer lintas paket, mengabaikan paket console `O` saat menunggu stop, serta hanya menerima jawaban stop RSP `T/S/W/X`. Sesudah entry stop, ia memeriksa PC harus tepat `0x80011448` sebelum menghapus breakpoint dan mencoba GP0/GP1/DMA2. Run [#39020901596](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39020901596) kini selesai `success` pada tingkat workflow, tetapi **tidak mencapai entry executable dalam batas 20 detik**: tidak ada stop event breakpoint dan setelah Ctrl-C PC masih `0xbfc03bdc` di BIOS. Log mengenali `SYSTEM.CNF` dan `BOOT = cdrom:\\SLPS_035.53;1`, tetapi tidak mencapai `EXEC:PC0`/`Execute !`. Ini bukan bukti hit GPU; watchpoints tidak diuji karena probe berhenti pada kegagalan entry. Run tersebut juga berbeda dari baseline karena belum menerapkan setup Port 1 Analog yang ada pada run sebelumnya. Commit `a8d8db8a0c3b84967a14c3a0905e046dbed24cf9` kini menerapkan Port 1 Analog + remap yang sama dan memperpanjang masa menunggu entry menjadi 40 detik; run baru [#39021127913](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39021127913) baru dimulai. Baca PC dan log final sebelum hipotesis lanjut.

Layar game belum berubah dari hitam dalam bukti visual sebelumnya; title/menu serta respons input belum terbukti. **RT-001 tetap Open / blocked; Story Mode belum dimulai/tamat.**

## Hasil RSP minimal dan eksperimen GPU-watchpoint — 2026-10-17

Run [#39017271906](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017271906) selesai dengan conclusion Actions `success` dan cleanup berhasil. Klien RSP minimal terhubung ke PCSX-Redux AnyLinux pada port 3333, negosiasi `qSupported` berhasil, dan 10 sampel register PC/CP0 berhasil dibaca tanpa GDB modern yang mengirim command tak didukung. Sampel PC meliputi `0x8003C0A0` dan `0x80037320`, yang berada dalam rentang EXE utama berdasarkan header/load range `0x80010000` dengan text size `0x5D800`; sampel lain juga meliputi alamat BIOS. `BadVAddr=0` konsisten di seluruh sampel dan `Cause=0x400`; jangan tafsirkan nilai ini sebagai diagnosis exception final. Status target RSP `S00` menunjukkan target sedang running saat diperiksa. Karena sampel jarang dan bercampur alamat BIOS/EXE, ini bukan bukti cukup bahwa inisialisasi game selesai.

Jendela non-root PCSX `0x200034` (1280×800) masih uniform black (mean 0, standard deviation 0, satu warna) pada capture sebelum input, setelah Return/Cross, dan sekitar 40/65/90 detik; OCR kosong. Loader tetap mencatat `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, `EXEC:PC0(80011448)`, `Execute !`. Dengan demikian pembacaan register kini bekerja, tetapi title/menu dan respons input masih belum terbukti. Artifact diagnostik privat `12095198494` retensi 3 hari; tidak ada dump memori atau instruksi mentah di artifact.

Eksperimen pembeda berikutnya saat catatan ini diperbarui: workflow [#39017636267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017636267) memasang breakpoint entry `0x80011448` saat emulasi masih paused, lalu memantau write-watchpoint pada register GPU GP0/GP1 dan DMA2 melalui klien RSP minimal. **Run ini masih berlangsung saat catatan ini dibuat; jangan menyimpulkan hasil watchpoint sampai log selesai diperiksa.**

**RT-001 tetap Open / blocked.** Story Mode belum dimulai/tamat; jangan menetapkan aturan gameplay runtime sebelum title/menu dan input terverifikasi.

# Status penelitian

## Keputusan emulator utama dan hasil GDB terbaru — 2026-10-17

**Emulator utama yang dipilih untuk penelitian lanjut: PCSX-Redux AnyLinux prebuilt + OpenBIOS fastboot (`openbios.bin`, SHA-256 `25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d`).** Ini keputusan operasional berdasarkan jalur terjauh yang terkonfirmasi di log: membaca `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, lalu `EXEC:PC0(80011448)` dan `Execute !`. Varian chunked belum mencapai marker entry dalam rentang uji yang sama; DuckStation terblokir oleh wizard yang tidak menerima OpenBIOS sebagai BIOS PS1/PS2 valid. Keputusan ini tidak menyatakan game sudah boot ke title/menu.
Run terakhir [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234) selesai sukses secara workflow, tetapi GDB remote gagal menghasilkan snapshot PC pada t20/t30/t50/t70 (exit 1) dan t90 timeout (exit 124). Jendela PCSX non-root XID `0x200034`/2097204 tetap valid dan frame pre-input, frame 30/50/70s, sesudah Return dan Cross semuanya hitam uniform (1280×800, mean 0, stddev 0, satu warna); OCR kosong. Log fastboot tetap mencatat entry handoff. Cleanup runner sukses, artifact privat #12095276220.
**RT-001 tetap Open / blocked** sampai title/menu Naruto dikenali dan respons input yang mengubah kondisi game terbukti. Story Mode belum dimulai/tamat.


## Diagnostik pasca-entry berikutnya sedang berjalan — 2026-10-17

Karena fastboot GUI tetap hitam baik dengan "-softgpu" maupun backend OpenGL default (Mesa llvmpipe 3.3), workflow privat [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234) telah dimulai. Tes ini mempertahankan fastboot BIOS, ROM dan controller yang sama, lalu mengambil snapshot PC melalui GDB remote eksternal pada beberapa waktu; tidak memakai pembacaan register CPU dalam callback VSync dan tidak mencetak instruksi/operand mentah. Status ketika terakhir diperiksa: masih memasang tool GDB; belum ada snapshot atau hasil boot baru. RT-001 tetap Open / blocked.


## Hasil A/B backend GPU — 2026-10-17

Run [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) menguji fastboot OpenBIOS yang sama pada PCSX-Redux AnyLinux tanpa `-softgpu`, memakai backend OpenGL default melalui Mesa llvmpipe. Kapabilitas GL terkonfirmasi: vendor Mesa, renderer `llvmpipe (LLVM 21.1.8, 256 bits)`, OpenGL 3.3 Compatibility Profile. Capture berasal dari jendela PCSX non-root `0x200034` / XID 2097204, 1280×800. Seluruh frame sebelum input, setelah Return/Cross, dan pada 40/65/90 detik tetap uniform black (mean 0, stddev 0, satu warna); OCR kosong. Tidak ada callback pembaca register CPU. Log fastboot tetap mencapai SYSTEM.CNF/BOOT, `EXEC:PC0(80011448)`, `Execute !`. Jadi backend OpenGL default pun belum membuat title/menu terlihat.
- Artifact privat `12094736241`, cleanup berhasil.
- Hipotesis berikut yang paling informatif adalah mengambil snapshot PC CPU dari luar emulator melalui GDB remote (bukan Lua/VSync callback), untuk membedakan loop pasca-entry dari masalah rendering tanpa mencetak trace instruksi mentah.
**RT-001 tetap Open / blocked.** Story Mode belum dimulai; belum ada aturan gameplay runtime yang terverifikasi.


## Hasil capture fastboot yang sah — 2026-10-17

Run [#39015722771](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015722771) kini menghasilkan capture valid jendela aplikasi PCSX-Redux, XID 2097204 (`0x200034`), 1280×800. Selector membaca `xwininfo -root -tree`, mengecualikan root 543/`0x21f`, dan memakai non-root window bernama `PCSX-Redux`. Lima capture (sebelum input, sesudah Return/Cross, 40/65/90 detik) semuanya uniform black (mean 0, stddev 0, satu warna); OCR kosong. Ini bukan lagi masalah salah mengambil root. Port 1 Analog tetap dikonfigurasi dan input telah dikirim ke jendela aplikasi, tetapi tidak ada perubahan visual/game yang bisa diverifikasi. Tidak ada pembacaan register CPU di callback VSync. Log fastboot mencapai `SYSTEM.CNF`, `BOOT`, `EXEC:PC0(80011448)`, `Execute !`.
Run berikut [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) mengganti satu variabel grafis: menghapus `-softgpu`, mengaktifkan Mesa llvmpipe/OpenGL 3.3, dan mencatat kapabilitas GL. Status saat dicatat: in progress.
**RT-001 tetap Open / blocked** sampai title/menu dikenali dan input nyata menghasilkan perubahan game.


## Koreksi pemilihan window X11 — fastboot probe terbaru, 2026-10-17

Run [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649) benar-benar mengecualikan root, tetapi pencarian kandidatnya masih memakai `xdotool search`; hasilnya tidak mengembalikan aplikasi. Potongan `xwininfo -root -tree` di log menunjukkan child window nyata `0x200034 "PCSX-Redux"`, 1280×800. Jadi kesimpulan yang benar: window ada tetapi selector gagal memilihnya; tidak ada gambar emulator yang diambil. Marker fastboot dari log tetap mencapai `SYSTEM.CNF`, `BOOT`, `EXEC:PC0(80011448)`, `Execute !`.
Workflow diperbarui pada commit `1acd87e9960c0caeb334cffc48ed8aea212212e1` agar mengekstrak XID langsung dari tree, mengecualikan root, dan memakai `windowfocus` sebelum input. Rerun [#39015610296](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015610296) telah dipicu; status awal queued.
**Belum ada capture GUI fastboot yang sah dan belum terbukti title/menu. RT-001 tetap Open / blocked.**


## Koreksi validitas capture fastboot — 2026-10-17

Audit log run [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) menemukan bahwa ID window `543` sama dengan root Xvfb `0x21f`. Selector `xdotool search --onlyvisible --name '.*'` ternyata memasukkan root, sehingga semua metrik hitam dan OCR kosong dari run ini **bukan** capture jendela emulator dan harus ditarik dari bukti visual. Marker boot tetap sah: fastboot BIOS mencapai `SYSTEM.CNF`, BOOT, `EXEC:PC0(80011448)`, dan `Execute !`.
Run [#39015290594](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015290594) menggunakan selector sama dan juga tidak boleh dianggap sebagai capture game bila memilih root; ia sedang digantikan oleh run [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649). Workflow telah diperbaiki pada commit `83173bb10cfbf905a296f59720c0a63c95bc3a32` untuk mengecualikan root ID secara eksplisit sebelum memilih jendela non-root yang layak. Verifikasi hasil run baru dari `X11_ROOT_ID`, `WINDOW_CANDIDATE_SKIPPED=root`, dan `CAPTURE_WINDOW` non-root sebelum menilai gambar.
**RT-001 tetap Open / blocked.** Sampai capture non-root yang sah menunjukkan Naruto dan kontrol merespons, tidak ada bukti title/menu/gameplay.


## Hasil fastboot GUI dengan window discovery generik — 2026-10-17

Run [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) berhasil mengidentifikasi jendela X11 (ID `543`, 1280×800); jadi tangkapan sebelumnya yang gagal mencari nama jendela adalah masalah selector, bukan bukti tidak ada window. Namun semua frame sebelum input, sesudah Return, sesudah Z/Cross, serta 40/65/90 s tetap uniform black (mean 0, stddev 0, satu warna), OCR kosong. Log fastboot kembali mencapai `SYSTEM.CNF`, `BOOT`, `EXEC:PC0(80011448)`, dan `Execute !`. Input memang dikirim ke jendela aplikasi, tetapi karena layar tetap hitam, belum bisa ditafsirkan sebagai kontrol game.
Uji berikut [#39015290594](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015290594) mengulangi fastboot yang sama tanpa pembacaan register CPU di event VSync, karena instrumentasi tersebut pernah mengganggu eksekusi di eksperimen terdahulu. Status saat dibuat: queued. **RT-001 tetap Open / blocked.**


## Hasil eksperimen terbaru — 2026-10-17

### Source-current PCSX-Redux
Run [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) selesai dengan semua langkah workflow `success`: source PCSX-Redux pin `1525a93676dbece9fe70f10ff129aeaa14eec30d` berhasil dibangun, tetapi jendela emulator yang benar-benar ditangkap pada detik 20/40/60/80/95 seluruhnya uniform black (1280×800, mean 0, stddev 0, satu warna), OCR kosong. Log mengenali disc `SLPS-03553` dan OpenBIOS, mencatat Port 1 Analog tersambung, tetapi hanya sampel PC frame 300=`0x000015a4`; tidak ada pembacaan `SYSTEM.CNF`/BOOT atau entry executable. Artifact privat `12094116949` berisi 5 frame hitam dan stdout. Cleanup sukses. Keberhasilan build dan Actions tidak berarti game boot.
### OpenBIOS fastboot vs chunked
Run [#39013612865](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39013612865) menguji build AnyLinux sama dengan dua BIOS. Varian fastboot membaca `SYSTEM.CNF`, `BOOT`, lalu mencatat `EXEC:PC0(80011448)` / `Execute !`. Varian chunked hanya menunjukkan pembacaan payload satu sektor sampai indeks 40 sebelum log berhenti. Namun window detector lama tidak menemukan jendela untuk kedua varian, jadi tidak ada capture visual dan urutan input dilewati. Hasil ini mengisolasi beda jalur loader, bukan bukti title/menu.
### Eksperimen berikutnya
Workflow privat baru [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) memakai fastboot OpenBIOS dan enumerasi generik jendela X11, bukan hanya mencari caption “PCSX”. Status awal: queued; periksa hasil aktualnya.
**RT-001 tetap Open / blocked:** title/menu Naruto dan input game yang responsif belum terbukti. Story Mode belum dimulai/tamat.


## Hasil final DuckStation probe — 2026-10-17

- Run [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) berhasil membuka jendela setelah paket `libegl1` ditambahkan. Capture 760×498 konsisten menampilkan first-run setup wizard DuckStation, termasuk halaman BIOS.
- Layar BIOS secara eksplisit menyatakan DuckStation membutuhkan BIOS PS1/PS2; UI mendeteksi satu berkas BIOS tetapi tetap menyatakan tidak ada BIOS yang dapat dipakai. Log hanya menunjukkan BIOS dipetakan dan pencarian Auto BIOS; tidak ada marker disc/executable Naruto. Return bergerak di wizard; Z/Cross tidak terbukti mencapai game. Ini bukan tes kompatibilitas ROM yang tuntas.
- Artifact privat `12094155047` berisi 8 screenshot dan stdout. Ditinjau lokal untuk membedakan wizard BIOS dari layar game; salinan ZIP/gambar lokal sementara kemudian dibersihkan. Cleanup workspace runner sukses.
- **Tidak meminta atau mengunduh BIOS retail baru.** Dalam batas hanya memakai OpenBIOS yang sudah tersedia, DuckStation saat ini terblokir pada validasi BIOS; emulator ini tidak dinilai sebagai gagal kompatibilitas Naruto.
- PCSX-Redux source-current [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih membangun source ketika terakhir diperiksa; itu jalur prioritas selanjutnya.
- **RT-001 tetap Open / blocked.** Belum ada title/menu Naruto terverifikasi dan belum ada input game terverifikasi.


## Pembaruan status terbaru — 2026-10-17, hasil DuckStation setelah perbaikan GL

- Rerun [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) juga menyelesaikan workflow `success`, tetapi DuckStation keluar dengan kode 127 sebelum membuat jendela: `libEGL.so.1: cannot open shared object file`. Tidak ada frame, OCR, input, atau bukti boot BIOS/disc. Artifact 292 byte tidak berisi PNG.
- Workflow diperbarui lagi pada commit `5afd32eca0d32ee191de7f2963f74b53aed89448` dengan paket `libegl1`. Rerun [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) sedang berada pada langkah boot/capture ketika terakhir diperiksa.
- PCSX-Redux source-current [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih membangun source; belum ada frame yang dapat dinilai.
- **RT-001 tetap Open / blocked.** Belum ada title/menu Naruto dan respons input yang terverifikasi.


## Verifikasi terbaru — 2026-10-17, DuckStation probe dan source-current GUI

- Run privat [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) berakhir dengan conclusion Actions `success`, tetapi **DuckStation tidak diluncurkan**: log aktual menunjukkan `AppRun: error while loading shared libraries: libOpenGL.so.0: cannot open shared object file`. Tidak ada jendela DuckStation, frame/OCR game, input terkirim, atau bukti BIOS/disc dari proses emulator. Artifact ZIP (ID `12093451882`, 293 byte) hanya berisi `duckstation.stdout` sepanjang 183 byte; tidak ada PNG.
- Harness telah diperbaiki pada commit `058aadea1c664712b62a63cf01fcb3e5598ef047`: pasang paket `libopengl0 libglx0 libgl1` dan unggah `captures/*.png` (sebelumnya glob `frame-*.png` tidak cocok dengan nama file capture). Rerun aktual [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) telah dimulai; periksa hasil finalnya.
- Source-current PCSX-Redux [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih pada tahap build source saat diperiksa. Belum ada frame GUI atau OCR yang bisa dinilai.
- Cleanup private workspace pada DuckStation run awal berhasil. Tidak ada bukti title/menu atau input gameplay.
- **RT-001 tetap Open / blocked** sampai title/menu Naruto dikenali secara visual dan respons input terkontrol dibuktikan.


## Uji emulator alternatif tambahan — 2026-10-17

Workflow privat [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) kini menguji rilis DuckStation resmi, dengan AppImage SHA-256 `c5e6f045f6a242082fcafa9f02d56ad895e233b942728788d232ad0c0c765c24`, ROM yang sama dan OpenBIOS `openbios.bin` dari private release. Harness Xvfb mengambil frame jendela dan mengirim Return/Cross lewat pemetaan keyboard sementara, lalu menyimpan capture sebagai artifact privat 3 hari dan menghapus workspace. Status saat catatan ini dibuat: queued; belum ada hasil boot/menu/input yang bisa disimpulkan. Ini uji kandidat, bukan klaim kompatibilitas.

## Pembaruan runtime terbaru — 2026-10-17

- GUI baseline AnyLinux tetap belum membuktikan title/menu: jendela ada tetapi hitam, log GUI belum menyelesaikan pemuatan executable; jalur headless pada build tersebut mencapai 187 chunk dan `EXEC:PC0(80011448)`.
- Run privat [#39011515345](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011515345) mengonfirmasi screenshot Lua pada mode `-no-ui` mengembalikan ukuran 0×0; proses mencapai handoff executable tetapi capture tidak valid dan postprocess gagal. Cleanup berhasil, artefak gambar tidak tersedia.
- Tes source GUI baru [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) memakai source PCSX-Redux pin `1525a93676dbece9fe70f10ff129aeaa14eec30d` (HEAD upstream yang diverifikasi pada saat workflow dibuat), sedang berjalan saat catatan ini ditulis. Source pin CPU-trace sebelumnya 24 commit di belakang.
- Workflow retensi [#39011611436](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39011611436) sukses menghapus run publik lama `#39001985849` secara spesifik. Fetch API untuk run itu sesudah penghapusan mengembalikan 404.
- **RT-001 tetap Open / blocked.** Tidak ada bukti visual title/menu Naruto, input terkontrol, atau gameplay Story Mode. Jangan mengklaim Story Mode dimulai atau tamat.

Terakhir dirangkum: 2026-10-17

## Ringkasan

**Status: analisis statis awal dengan jejak konfigurasi target Chakra yang lebih kuat; belum lengkap dan belum tervalidasi melalui debugging gameplay.**

**Sumber wajib:** kuota internet pengguna sangat terbatas. Jangan meminta upload ROM/ISO sekitar 300 MB dan jangan mengandalkan ROM laptop. Gunakan file hasil ekstraksi di Library pada /Naruto Research Files/. Jika tidak dapat diakses, laporkan kendala alih-alih meminta upload ulang.

Pemeriksaan sebelumnya mengekstrak struktur ISO dari dump PS1 raw-sector, membaca SYSTEM.CNF, mengidentifikasi executable utama, melakukan inspeksi/disassembly awal MIPS, dan menemukan beberapa struktur serta jalur kode. Namun, pemetaan overlay belum lengkap, rumus gameplay belum seluruhnya terhubung ke semua pemanggil, dan sesi emulator/debugger terkontrol belum dijalankan.

## Temuan yang didukung langsung oleh kode/data ROM

1. Executable boot yang dirujuk SYSTEM.CNF adalah SLPS_035.53.
2. Header executable mencatat alamat muat 0x80010000, PC 0x80011448, dan text size 0x5D800.
3. Struktur pemain yang diakses beberapa getter/setter memiliki empat slot; stride struktur 0xB4 byte dan nilai Chakra pada offset +0x18.
4. Setter Chakra yang diperiksa membatasi nilai tersimpan pada rentang -9.999 sampai 99.999. Ini bukan kondisi menang/kalah.
5. Jalur kode membandingkan Chakra pemain dengan target konfigurasi dari getter 0x80012A70; jika kondisi target terkait (bit 0x200) aktif, Chakra yang mencapai/melewati target dapat menetapkan pemain sebagai pemenang. Tabel konfigurasi utama memuat pasangan awal/target 1.500/3.000, 2.000/4.000, 2.500/5.000, 3.000/6.000 serta dua record awal 600/0 yang kondisi pemilihannya belum dipetakan. Jadi 3.000 bukan target universal.
6. Data petak diperlakukan sebagai bitfield; jalur yang diperiksa memakai empat bit teratas sebagai ID pemilik. Arti seluruh bit lainnya belum terpetakan.
7. Kode memeriksa sejumlah flag kondisi akhir, tetapi label yang sesuai dengan semua pilihan menu belum terpetakan secara lengkap.

Alamat dan penjelasan lebih detail ada di docs/ROM_STRUCTURE.md, docs/OVERLAY_MAP.md, dan docs/GAME_RULES.md.

## Temuan dari UI terjemahan/panduan eksternal — bukan bukti formula universal

- Story stage 1 diterjemahkan sebagai Naruto melawan Mizuki dengan target 3.000 Chakra.
- Dalam contoh tampilan, biaya membangun barrier ditampilkan 60 Chakra; suatu contoh barrier level 1 menampilkan nilai 100 dan durability 2/2; suatu contoh peningkatan level 1 ke 2 menampilkan biaya 150.
- Sumber lain menampilkan barrier level 1 bernilai 50, sehingga nilai tidak boleh dianggap tetap tanpa memahami parameter/tipe barrier dan konteksnya.
- Beberapa deskripsi kartu memberi contoh penambahan Chakra, peningkatan statistik, atau manipulasi roulette.

Contoh UI di atas belum membuktikan bahwa 60 dan 150 adalah biaya universal atau bahwa formula seluruh barrier sudah diketahui.

## Pekerjaan terbuka utama

- Petakan loader, offset file, alamat muat, ukuran, entry point, dan lifecycle untuk seluruh overlay.
- Lanjutkan reverse-engineering format resource yang kini terindeks melalui direktori di DATA.BIN; format PK02/BIN0/TPK0, NARUTOSceneV001, PSQ0/PSQ1, serta tujuan penuh XASECT.BIN masih belum diketahui.
- Temukan dan dokumentasikan sumber setiap harga barrier, biaya upgrade, pendapatan, nilai, level, dan durability.
- Petakan seluruh bitfield petak dan struktur barrier berdasarkan pembacaan serta penulisan field.
- Identifikasi jalur transaksi Chakra untuk bangun/upgrade/pendapatan/serangan/kartu dan efek pembatas nilainya.
- Hubungkan setiap flag kondisi menang ke record skenario, pilihan menu, dan tampilan teks.
- Telusuri algoritma roulette dan efek semua kartu sampai ke pemanggil sebenarnya.
- Jalankan skenario terkontrol di emulator/debugger dan bandingkan perubahan memori dengan analisis statis.

## Batas lingkungan saat ini

Pada pemeriksaan sebelumnya, tidak ditemukan emulator PS1 yang tersedia di lingkungan analisis; percobaan eksekusi terminal/Python berikutnya juga gagal karena lingkungan menolak eksekusi. Karena itu belum ada log eksekusi gameplay dari sesi kita. Laporan GameGear Archive bahwa ROM boot di test rig Mednafen adalah sumber eksternal dan bukan pengujian khusus biaya atau rumus permainan.

## Status confidence

- **Tinggi untuk metadata disc/EXE**: didukung header, SYSTEM.CNF, ukuran, hash, dan pencocokan CRC eksternal.
- **Tinggi untuk batas setter Chakra**: instruksi setter terlihat dan rentang penjepitan nilai telah diidentifikasi.
- **Menengah untuk cabang target skenario awal**: nilai target dari record konfigurasi dan jalur perbandingan ditemukan; pemetaan lengkap semua skenario tetap terbuka.
- **Rendah/belum pasti untuk biaya dan formula gameplay**: belum ada call chain lengkap ditambah tes runtime terkontrol.

## Pembaruan hasil pemeriksaan lokal — 2026-10-15

Pemeriksaan byte-level terhadap salinan kerja ROM mengonfirmasi temuan baru berikut. Hasil ini **statis**; belum ada tes gameplay terinstrumentasi.

- SHA-256 ROM cocok dengan catatan yang sudah ada: `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`.
- Di executable utama, offset file `0x46098` (alamat runtime `0x80055898`) berisi pasangan little-endian `0xD4, 0x2F44`: LBN 212 dan panjang 12.100 byte, yang menunjuk ke awal `DATA.BIN`.
- Awal `DATA.BIN` terdiri dari bootstrap sepanjang `0x44) byte diikuti direktori `0x2F00) byte: 1.504 entri × 8 byte, paling kuat ditafsirkan sebagai pasangan `(LBN, byte_length)`.
- 1.500 entri tidak kosong dan 4 kosong (indeks 1491–1494). Semua interval sektor entri aktif berada dalam rentang `DATA.BIN` dan tidak tumpang-tindih; direktori mencakup 32.227 dari 32.234 sektor file.
- Klasifikasi signature awal atas 1.500 resource aktif: 921 `PK02`, 246 struktur TIM valid, 126 `NARUTOSceneV001`, 125 signature lain berawalan `NARU`, 6 `PSQ0`, 2 `PSQ1`, 1 `TXT2`, dan 73 belum diklasifikasikan. Pemindaian longgar mendeteksi 264 kandidat magic TIM; 18 gagal validasi struktur dan tidak dihitung sebagai TIM valid.
- `XASECT.BIN` berisi hitungan 86 diikuti 86 pasangan 32-bit. Konsumen di sekitar `0x80019468` mengindeks pasangan dengan `input >> 4) dan memakai field pertama sebagai offset aditif. Arti semantik lengkap field dan kaitan field kedua dengan stream/media masih belum pasti.

Lihat [docs/RESOURCE_CATALOG.md](docs/RESOURCE_CATALOG.md) untuk hitungan, batas inferensi, hash file hasil ekstraksi, serta langkah analisis berikutnya. Handoff lintas-chat ada di [HANDOFF_LANJUT.md](HANDOFF_LANJUT.md).


## Persistensi file untuk analisis lintas chat

File ekstraksi disimpan di Library ChatGPT pada folder `Naruto Research Files`; `DATA2.BIN` tersedia sebagai ZIP terkompresi. Baca tabel lokasi pada `HANDOFF_LANJUT.md` dan verifikasi hash sesudah pemulihan sebelum melanjutkan analisis.


## Pembaruan analisis aturan gameplay — 2026-10-15

- Tabel konfigurasi executable 0x80057798 ber-stride 0x54; tabel kedua 0x80064918 ber-stride 0x30. Field +0x04 dipakai sebagai Chakra awal, field +0x08 sebagai target pada cabang kemenangan, sementara makna field +0x0C belum ditemukan.
- Nilai teramati pada tabel pertama mencakup 1500/3000, 2000/4000, 2500/5000, 3000/6000; ada dua record 600/0 yang tidak boleh ditafsirkan sebagai kemenangan instan.
- Label lama 0x800EC200 sebagai pembanding target Chakra dan 0x800F70D0 sebagai aritmetika Chakra dicabut karena base/identitas modul belum diverifikasi.
- File Library yang digunakan pada sesi ini: SLPS_035.53, DATA.BIN, XASECT.BIN, DATA2.BIN hasil unzip. Hash DATA2.BIN hasil unzip cocok: be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9.
- Belum ada tes runtime. Prioritas berikutnya: transaksi biaya bangun/upgrade, income, perubahan kepemilikan dan transaksi battle melalui pemanggil setter Chakra dan label event ESTATE/LVUP_ESTATE.


## Trace aturan Chakra — tambahan 2026-10-15

- Kode pembanding target di resource gameplay (base hipotesis 0x800D0000) memastikan syarat cabang target adalah Chakra saat ini >= target konfigurasi bila bit kondisi 0x200 aktif. Target dibaca lewat getter 0x80012A70. Alamat resource masih statis sementara karena loader belum diverifikasi runtime.
- Pemanggilan setter Chakra 0x8001387C banyak berupa sinkronisasi salinan record. State machine sementara pada resource DATA.BIN membentuk +0xB40 dari +0xB30 + +0xB38, lalu pada state +0xB2A == 7 memproses jumlah pending +0xB44 bertahap ke Chakra pemain +0xB2B. Sumber operand dan semantik event belum ditemukan; ini bukan bukti biaya barrier.
- Karena sumber nilai transaksi belum terhubung, biaya build/upgrade universal masih belum terbukti. Angka 60 dan 150 hanya tercatat pada contoh UI tertentu dalam transkripsi komunitas.


## Status emulator/runtime — 2026-10-15

- Emulator/debugger kini ditetapkan sebagai jalur riset utama untuk memvalidasi aturan, bersama reverse-engineering statis; bukan sekadar alternatif opsional.
- Diprioritaskan PCSX-Redux karena dokumentasi resminya mendukung CPU debugger, breakpoint dan GDB server; Mednafen dapat digunakan untuk cek silang. Rujukan dan protokol uji ada di [docs/EMULATOR_WORKFLOW.md](docs/EMULATOR_WORKFLOW.md).
- Pada awal sesi executable emulator tidak tersedia dan DNS container gagal. PCSX-Redux kemudian diunduh dari GitHub Actions artifact/release, diverifikasi, dan antarmukanya berhasil dijalankan lewat Xvfb. Namun, belum ada bukti bahwa game mencapai menu/title atau bahwa gameplay sudah diuji.
- ROM di Library berhasil dimaterialisasikan dan SHA-256 cocok; tidak dibutuhkan upload ulang dari laptop pengguna.


## Emulator tersimpan di repo — 2026-10-15

- PCSX-Redux Linux x86_64 AppImage diunggah sebagai Release asset di [research-emulator-pcsx-redux-2026-10-15](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15), bukan Git history. Ukuran 65.747.557 byte; SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c. GitHub Actions run 38692549397 sukses mendownload dan memverifikasi binary.
- AppImage dapat diluncurkan di Xvfb, tetapi layar menunjukkan “No BIOS loaded, emulation halted”; belum ada boot game ataupun uji gameplay.
- Workflow build OpenBIOS open-source ada di .github/workflows/build-openbios.yml. Run #38693358323 membangun varian shell/menu dan run #38693918169 membangun shell/menu plus `BOOT_MODE=fast`. Hash fastboot `openbios.bin`: 25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d; hash ELF: 2c8d36e2179841935a1d1331777380502cdb22528d086c99c6388cdcfa54b8aa. Uji lokal fastboot menghasilkan layar hitam dan belum membuktikan Naruto mencapai title/menu. OpenBIOS bukan BIOS retail Sony.
- Jangan meminta upload ulang ROM. ROM hash diverifikasi dari Library; CUE dibuat untuk BIN raw-sector MODE2/2352.


## Update OpenBIOS — 2026-10-15

- Run [#38693358323](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693358323) berhasil membangun OpenBIOS dari source upstream PCSX-Redux pada commit 0c3572c3db75f97542001e453ae80ba8c3f8acba dan melampirkan asset ke release.
- Varian OpenBIOS default: `openbios.bin` 524.288 byte, SHA-256 `713ea2aed58606282b3ff5e91d77f8c5892ea36f5adcd279d2c7dd26604a625d`; ELF debug `openbios.elf` SHA-256 `d0d4cc73c9546e1e6af86d38ec894f5a6c81090ccdf97b1a3a39885c56af7bfc`. Checksum lengkap di release asset `OPENBIOS-SHA256SUMS`.
- Uji lokal dengan BIOS ini tidak lagi menampilkan pesan “No BIOS loaded”, tetapi frame yang terekam berupa bentuk geometris/gelap tanpa menu atau title game yang dapat dikonfirmasi. Ini belum membuktikan boot Naruto.
- [Run #38693918169](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693918169) sedang membangun varian `BOOT_MODE=fast` yang melewati shell BIOS dan mencoba boot CD secara langsung, bersama varian shell/menu normal. Periksa hasil workflow dan hash sebelum menggunakan asset tersebut.


## Hasil varian OpenBIOS fastboot — 2026-10-15

- Run [#38693918169](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693918169) sukses membangun dua variant dan mengunggahnya ke release. Varian `openbios.bin` memakai `BOOT_MODE=fast` untuk mencoba boot CD langsung; varian shell/menu tersedia sebagai `openbios-shell.bin`.
- SHA-256 fastboot `openbios.bin`: `25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d`; `openbios.elf`: `2c8d36e2179841935a1d1331777380502cdb22528d086c99c6388cdcfa54b8aa`. Asset release dan `OPENBIOS-SHA256SUMS` tersedia pada [research kit release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15).
- Uji lokal varian fastboot: PCSX-Redux dijalankan dengan OpenBIOS, interpreter, debugger, dan CUE ROM. Layar tetap hitam setelah sekitar 12 detik; log tidak menyatakan BIOS hilang tetapi tidak ada title/menu yang dapat dikonfirmasi. Status: **boot game belum terverifikasi**, bukan test runtime berhasil.
- Workflow diperbarui agar artifact runtime-kit menyertakan shell/default dan fastboot sekaligus, bukan checksum yang merujuk file yang tak ada. Run terbaru akibat perbaikan ini harus diperiksa.

## Status runtime terbaru — 2026-10-16

Game masih belum terkonfirmasi mencapai title/menu; belum ada tes gameplay runtime yang selesai. PCSX-Redux dan varian OpenBIOS diagnostik tersedia pada [release research kit](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15).

- Jalur disc normal: mengenali label `SLPS-03553`, membuka `SYSTEM.CNF;1`, menguraikan `BOOT = cdrom:\\SLPS_035.53;1`, lalu berhenti di `boot file ...` sebelum `EXEC:PC0(80011448)`.
- Main executable: 385.024 byte; payload 382.976 byte (`0x5D800`, 187 sektor setelah header 2.048 byte).
- Chunk 8 sektor berhenti pada log sebelum syscall pertama selesai (`bytes=16384`); chunk 1 sektor berhasil menunjukkan progres pembacaan 2.048 byte, tetapi uji singkat belum membuktikan seluruh payload selesai atau game tampil. Build/asset varian satu sektor sukses melalui [Actions #38697240018](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38697240018).
- Injeksi executable diagnostik mencapai `EXEC:PC0(80011448)`, `Execute !`, dan `CD_init`; layar tetap hitam. Periksa cache (`flushCache`) dan urutan init CD-ROM jika mengulangi jalur ini. Rutin init kartu memori (`buInit`) juga tampak menunggu status yang tidak berubah; bypass sementara belum membuktikan boot sukses.
- Log menunjukkan perintah kontroler `0x43` (Set Config Mode) berulang. Source PCSX-Redux memproses perintah DualShock tersebut hanya pada tipe pad Analog; tipe Digital mencatat `Unknown command for pad: 43`. Ini petunjuk yang belum diuji, bukan akar masalah yang terbukti. Referensi: https://github.com/grumpycoders/pcsx-redux/blob/db9bc8af44e3c77424127b573c17f9583ee2ab95/src/core/pad.cc. Eksperimen berikutnya: ubah Port 1 ke Analog/DualShock lalu ulangi boot.
- File baru dari pengguna `PCSX-Redux-9c6f98a0-linux-x86_64.zip` (90.912.361 byte) belum dapat dievaluasi atau dijalankan karena lingkungan shell/file tool tidak merespons. Periksa lagi sebelum memutuskan apakah build itu menggantikan AppImage release.
- Jangan meminta upload ulang ROM dan jangan mengunggah ROM/EXE, retail BIOS, save state, atau dump memori ke GitHub.


## Percobaan runtime setelah pemulihan ZIP Library — 2026-10-16

ZIP alternatif, ROM BIN, dan CUE berhasil dimaterialisasi lewat Files ke lokasi kerja. Namun `container.exec` bahkan gagal pada `echo runtime-check`, dan tool Python juga mengembalikan `ClientError`. ZIP belum bisa diinspeksi/diekstrak dan PCSX-Redux belum dijalankan dalam percobaan ini. Ini kendala lingkungan eksekusi, bukan bukti ZIP rusak atau gagal menjalankan game. Status boot tetap belum terverifikasi; setelah runtime pulih, uji integritas ZIP, versi/dependensi executable, lalu boot dengan OpenBIOS dan controller Port 1 Analog/DualShock. Kriteria sukses tetap title/menu Naruto terlihat serta input merespons.

## OpenBIOS source-level CD-read stall hypothesis — 2026-10-16

- Static inspection of the OpenBIOS source used by the research AppImage narrowed the normal boot stall to the EXE payload read path. loadExe() reads the 2,048-byte PS-X EXE header and then submits the full 382,976-byte payload (187 sectors) through one syscall_read call. The underlying CD file driver requires 0x800-aligned size/offset and waits for the CD read-completion event.
- The helper's wait for the completion event has no overall timeout. A missing/stuck completion event can block the BIOS indefinitely. This fits the prior stall evidence but is not a proven root cause.
- The uploaded filename PCSX-Redux-9c6f98a0-linux-x86_64.zip points to upstream commit 9c6f98a0ed0581635f9123147e382c248e0f5ddc (2026-09-28); the research AppImage is pinned to 0c3572c3db75f97542001e453ae80ba8c3f8acba (2026-10-01). The ZIP's contents/hash are not yet verified; treat this as filename-based provenance only.
- Next runtime test: use the existing AppImage/known OpenBIOS chunked build, CUE path, -run -interpreter -debugger -stdout -lua_stdout -logfile ..., and a fresh settings directory. Set Port 1 DeviceType=1 (Analog/DualShock) separately from PadType=2 (keyboard as host input) and Connected=true. Repeat the same boot attempt; compare pad 0x43 logs, CD read progress, entry-PC log, title/menu, and input response without changing other variables.
- Current session: the Library service successfully materialized the ROM, CUE, main EXE, DATA2 archive, and alternate emulator ZIP to reported working paths, but shell/Python calls returned ClientError. No new emulator run occurred. Never claim boot/gameplay success without runtime evidence.


## PCSX-Redux ZIP extraction record — 2026-10-16

- Extracted `PCSX-Redux-HEAD-x86_64.AppImage` from the Library ZIP (the ZIP passed `unzip -t` and had exactly one member).
- AppImage size: 91,474,424 bytes; SHA-256 `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`. The Library copy was materialized back and SHA-256 matched the extracted copy.
- Embedded version is `9c6f98a0`, build ID 335, changeset `9c6f98a0ed0581635f9123147e382c248e0f5ddc`, dated 2026-09-28 19:56:29 UTC.
- The source ZIP was replaced in Library by its one extracted AppImage because of the Library storage limit. Extraction manifest is saved at `/Naruto Research Files/PCSX-Redux-EXTRACTION-MANIFEST.md`.
- Runtime is blocked on this host: bundled emulator binary requires GLIBC_2.42/2.43, host has glibc 2.41; mounting the AppImage additionally reports missing FUSE/fusermount. Do not treat this as proof of a corrupted archive or ROM.
- The extracted AppImage is retained in Library; repository stores its provenance/hash/compatibility record in `docs/PCSX_REDUX_PACKAGE.md`. It was not inserted into Git history because the available GitHub connector does not expose binary release-asset upload. The repository's existing 65,747,557-byte AppImage release asset is a distinct build with its own hash.
- No ROM, game EXE, assets, BIOS retail, save state, or RAM dump was uploaded. This extraction did not demonstrate game boot or Story Mode.


## Preferred build for GLIBC 2.41 host — 2026-10-16

- Selected the existing research-release AppImage `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage` as the best candidate for glibc 2.41. Size 65,747,557 bytes; SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`.
- Public package description says AnyLinux packaging uses sharun, bundles dependencies, supports old/musl Linux distributions, and does not require FUSE. Upstream packaging action run 36872881656 succeeded on 2026-10-01; x86_64 log says `quick-sharun --simple-test`: “Test went OK.”
- This supersedes the 91 MB `9c6f98a0` Library build as the preferred candidate. That build's inner binary requires GLIBC_2.42/2.43 but the host is glibc 2.41.
- Critical limit: CI simple-test and GUI launch under Xvfb do not prove the Naruto ROM boots or runs smoothly. A fresh end-to-end game test could not run because container/Python execution tools returned ServerError in this turn. No claim of game boot or Story Mode success.
- Detailed provenance and next steps: `docs/PCSX_REDUX_PACKAGE.md`.


## Current Library package — AnyLinux artifact ZIP (2026-10-16)

- The current Library file is `/Naruto Research Files/PCSX-Redux-0c3572c3d-anylinux-x86_64-artifact.zip`, downloaded from Actions artifact ID `11170447493`; Actions-reported ZIP digest `f6c27070b565cbc0554f1093c1374a16aee2b8635c72ef7b141f9ff7bd857ed0`.
- Preferred binary inside: `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage`, 65,747,557 bytes; SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`.
- The previous 91 MB `9c6f98a0` AppImage and its stale extraction manifest were replaced/removed in Library. Their hashes and incompatibility history are preserved in `docs/PCSX_REDUX_PACKAGE.md`.
- The AnyLinux package's CI smoke test passed but does not load Naruto. Full game boot/controls/stability are unverified because this session's local container/Python tools return ServerError.


## Pembaruan eksperimen controller — 2026-10-17

- Hasil baseline A/B dari runner [Actions #38971848277](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38971848277): AnyLinux dan upstream HEAD sama-sama mencapai `EXEC:PC0` dan sama-sama mencatat `Unknown command for pad: 43`; keduanya masih belum membuktikan title/menu atau input yang berfungsi.
- Runner workflow diperbarui pada commit [0439c1b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/0439c1bbf51d3c1be234150d6bee80c5b812ff1e) agar menyetel Port 1 sebagai `Analog`, `Connected=true`, lalu memanggil `map()` melalui Lua sebelum tes boot. Setup ini mengikuti tes internal upstream PCSX-Redux di `tests/pcsxrunner/rumble.cc`.
- **Status eksperimen baru: hasil belum diverifikasi dalam catatan riset.** Jangan menyimpulkan peringatan `0x43` hilang atau boot berhasil berdasarkan commit workflow saja.
- Langkah wajib berikutnya: baca log run sesudah perubahan dan pastikan marker `PAD_SETUP=port1 analog device connected and remapped` muncul. Bandingkan pesan `0x43`; jika hilang, lanjutkan dengan tes GUI Xvfb dan konfirmasi frame title/menu serta respons input. Jika tetap hitam, pisahkan masalah kontroler dari jalur CD-ROM, boot executable, dan rendering.
- Dilarang menyimpan/unggah ROM, game EXE, BIOS retail, save state, dump RAM atau screenshot game ke repo.

- Koreksi penting: revisi workflow awal salah indentasi pada heredoc Lua; versi final yang berlaku adalah [0439c1b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/0439c1bbf51d3c1be234150d6bee80c5b812ff1e), setelah indentasi YAML dibetulkan. Belum ada hasil runtime terverifikasi yang dicatat dari versi final ini.


## Hasil runtime Port 1 Analog — 2026-10-17

- Runner Actions [#38973267415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973267415) sukses. Marker Lua menyatakan Port 1 sudah `Analog`, terhubung, dan di-remap.
- Kedua build (AnyLinux dan upstream HEAD) mencapai `EXEC:PC0(80011448)` dan `Execute !`. Tidak ada pesan `Unknown command for pad: 43` di kedua log setelah konfigurasi Analog; baseline sebelumnya memunculkan pesan itu pada dua build. Masing-masing dihentikan pada batas waktu 90 detik, bukan crash.
- Kesimpulan terkonfirmasi: konfigurasi controller memperbaiki ketidakcocokan protokol `0x43` pada log. **Belum terbukti** bahwa title/menu tampil atau input dalam game berfungsi.
- Tes rendering GUI ditambahkan pada workflow commit [85c08d9](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85c08d9ea255dc400c0771361abc95817a0a7ba6). Actions [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) terlihat queued; hasil akhir belum diverifikasi. Probe ini menganalisis dua frame lokal (10s dan 20s) dan mencatat metrik/teks, tanpa menerbitkan gambar atau ROM/BIOS.


## GUI probe and CPU trace — 2026-10-17

- Actions [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) completed successfully. Under GUI + Xvfb, frame 10s and frame 20s both measured `1280x800`, `mean=0`, `stddev=0`, `colors=1`; OCR Japan/English returned no text. The captured desktop was entirely black at both points.
- Selected GUI logs did not show `EXEC:PC0` or `Execute !` within its 35-second window, unlike the headless probe. BIOS, disc ID and Analog PAD_SETUP markers did appear. This is a separate GUI/headless discrepancy, not proof that the game executable is invalid.
- New separate CPU trace workflow: [naruto-cpu-trace.yml](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/blob/main/.github/workflows/naruto-cpu-trace.yml), run [#38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045). It samples `PC`, `RA`, `SP` on every 30th `GPU::Vsync` callback, capped at 600 frames. Result not yet verified at time of writing.


## CPU trace attempt 1 — status 2026-10-17

- [Actions #38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045) exited with code 139 about 12 seconds after the VSync trace callback was added; no `PC_TRACE` sample appeared. Treat this as an instrumentation failure until isolated, not evidence against the ROM.
- Retry workflow revision: [9419800](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/941980021c16dee3e779f6cc1066dad70b187ad4). It uses one combined `-exec` script and no longer removes the listener from its callback. Check [run #38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739); if it also crashes, reduce the callback to count VSyncs only.


### CPU trace attempt 2 correction — 2026-10-17

- Run [#38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739) ended with exit 134 because Lua parsing failed: `unexpected symbol near '\\'`. The helper used a doubly escaped newline, passing literal `\n` instead of a newline between chunks. No valid tracing code ran; do not interpret as a ROM crash.
- Workflow commit [7b8ce73](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/7b8ce731378e0115f616b7ff78874f5d17375e80) replaced concatenation with one Lua heredoc. Check retry [Actions #38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869) for setup and VSync samples.


### CPU trace attempt 3 and counter-only isolation — 2026-10-17

- Corrected trace run [#38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869) emitted PC samples from frame 30 through at least 780. Values often point to BIOS routines (`BFC0574C`, `BFC05784`, `BFC03C6C`), with occasional `0xB0` and `0x2998`; the separate log includes `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, `Execute !`. The emulator process still exited 139 (segfault) with an incomplete final sample, so register reads inside the callback could be involved. The trace does not prove the game crashed or remained on one PC.
- Isolation run [#38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602), workflow commit [85d3e4f](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85d3e4ff31732b7788d67e447ea9df136dcb84f5), removes CPU-register reads and prints only a VSync counter. Results pending.


### Counter-only VSync test passed — 2026-10-17

- Run [#38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) reached expected `TRACE_PROCESS_EXIT=124` after the 35-second cap; VSync counter advanced through `frame=2040`. Headless boot markers `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, `Execute !` appeared. Counter-only callback is stable.
- New probe [#38974903834](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974903834), commit [ff0faa5](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/ff0faa598c6e19295229b450c6f9d42c83e590fb), keeps counter and adds sparse PC-only reads from a register view acquired before callback registration. Result pending.


### Emulator trace API mismatch — 2026-10-17

- Run [#38975154606](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975154606) aborted with `attempt to index field 'CPU' (a nil value)` because the pinned AnyLinux build from upstream ref `0c3572c3d` has no `PCSX.CPU.Trace` API. This test did not begin VSync counting; it says nothing negative about the ROM.
- Corrected workflow commit [c994afc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/c994afccfa62efcc01751a7c2b39d89b109d936a) now verifies and uses private-release upstream HEAD AppImage SHA-256 `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`. Run [#38975223698](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975223698) is the new bounded CPU-trace attempt; outcome pending.


### CPU trace API correction and source build — 2026-10-17

- The private upstream HEAD AppImage in [run #38975223698](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975223698) also lacks `PCSX.CPU.Trace`; it aborted before VSync counting. Neither packaged AppImage asset currently available exposes this newer API.
- Current runner workflow commit [8304b7d](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8304b7dd56be13673e83e84bb738458eca0cfc2d) now clones source pinned to upstream commit `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` and compiles it with the official PCSX-Redux builder container. [Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) is building; results pending.


### Catatan interpretasi GUI — 2026-10-17

- Frame hitam pada 10s/20s di [run #38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) diambil sebelum executable game terbukti dijalankan. Counter-only [run #38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) menunjukkan entry point baru dicapai setelah sekitar 27–30 detik dalam tes headless. Karena itu capture 10s/20s bukan bukti bahwa layar tetap hitam sesudah entry. Tes GUI harus diperpanjang hingga setidaknya 60–90 detik dan idealnya menangkap window emulator secara langsung.
- Source-build trace [run #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) sedang mencoba build source pinned agar API CPU trace tersedia tanpa membaca register dari callback. Hasil belum terverifikasi.


### Tes lanjutan sedang berjalan — 2026-10-17

- GUI run terbaru [#38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679), workflow commit [aea4c20](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aea4c20accfd6d1c5089a226f52a2c4183d2d9a8), memperpanjang pengamatan hingga 100 detik dan mengambil frame pada 30/60/90 detik. Saat catatan ini diperbarui, langkah A/B + GUI masih berjalan.
- CPU trace source-build run [#38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) belum melewati langkah build pinned upstream source. Hasil build dan trace tetap pending.


## Verifikasi cloud runner dan koreksi observasi — 2026-10-17

Pemeriksaan ulang repositori mengonfirmasi riset ini tetap **private**, sedangkan `naruto-shinobi-jintori-runner` tetap public. Release `research-emulator-pcsx-redux-2026-10-15` berisi aset ROM/CUE/OpenBIOS yang diperlukan; nama aset ROM dan CUE dinormalisasi dengan titik oleh proses unggah Release. Tidak ada media permainan yang ditambahkan ke Git runner.

Run [runner Actions #38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679) selesai dengan kesimpulan job **success**. Log mengonfirmasi secret read-only hadir tanpa menampilkan nilainya, ukuran ROM 325.989.552 byte, SHA-256 cocok, CUE valid, BIOS OpenBIOS dikenali, disc label `SLPS-03553`, `SYSTEM.CNF` menunjuk `SLPS_035.53`, seluruh 187 chunk executable dibaca, lalu tercatat `EXEC:PC0(80011448)` dan `Execute !`. Konfigurasi Port 1 Analog juga menghilangkan pesan `Unknown command for pad: 43` pada dua build pembanding. Ini membuktikan transfer kendali ke entry executable dalam jalur headless, **bukan** bukti title/menu atau input gameplay.

Capture GUI 30/60/90 detik pada run tersebut melaporkan gambar hitam (mean 0, stddev 0, satu warna) dan OCR kosong. Audit workflow memperlihatkan capture dilakukan dengan `import -window root`, yaitu latar root Xvfb, bukan window emulator secara eksplisit. Karena itu angka tersebut tidak boleh dipakai untuk menyimpulkan bahwa framebuffer game hitam.

CPU trace source-build [Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) membangun emulator tetapi peluncuran di host berhenti dengan `libcapstone.so.5: cannot open shared object file`; belum ada VSync atau instruksi yang direkam. Ini kegagalan dependensi runtime runner, bukan bukti masalah ROM/game.

Koreksi yang sudah dikirim ke repo runner:
- Commit [d965dcc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/d965dcc864c73818e67d6a1e5f9edc19d4a3a17c) menambahkan `libcapstone-dev` dan pemeriksaan `ldd` sebelum trace, supaya dependensi yang hilang terdeteksi sebelum emulasi.
- Commit [8829933](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8829933b3b6815dce694ebe6d46cd2a1f0fee9f0) memasang `xdotool`/`x11-utils` dan menargetkan window PCSX-Redux untuk pengukuran/OCR. Jika window tidak ditemukan, workflow mencatat pohon window dan tidak menggantinya dengan capture root hitam. File gambar tetap lokal di runner dan dihapus saat cleanup.

Retest yang dimulai dari dua commit itu belum selesai pada waktu catatan dibuat: GUI [Actions #39000276365](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365), CPU trace [Actions #39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139). Periksa hasil finalnya sebelum menetapkan status boot. Jangan mulai RT-001/gameplay sampai title/menu yang dikenali dan respons input terbukti.


## GUI-window retest result — 2026-10-17 (Actions #39000276365)

The corrected capture test completed successfully. Its log found the actual PCSX-Redux X11 window (CAPTURE_WINDOW at 30s, 60s and 90s), rather than the Xvfb root. All three captured PCSX-Redux-window frames nevertheless measured 1280x800, mean=0, stddev=0, colors=1; Japanese/English OCR returned no text.

Important distinction: the GUI probe's own log shows BIOS/OpenBIOS and disc metadata, but does not show [CHUNK1] done chunks=187, EXEC:PC0(80011448) or Execute !. Those entry markers are present in the separate headless A/B probes in the same job. Therefore the current evidence does not show a black game frame after executable entry; it shows that GUI mode remains black and did not log the same executable handoff as headless mode. Investigate this GUI/headless boot-path difference before diagnosing the game's renderer.

Run: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365. ROM/BIOS, frames and logs were removed during runner cleanup; no game media or screenshot was committed.


## GUI-init/GL diagnostic rerun queued — 2026-10-17

After the corrected capture proved the PCSX-Redux window itself remained uniformly black and the GUI probe lacked both PAD_SETUP and executable-entry markers, the runner workflow was tightened further. Commit [259d587](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/259d587c6b677be7f6466b0ec61edb1940faec49) adds a Mesa/GLX capability report from the same Xvfb + software-rendering environment, prints the final GUI stdout and emulator logfile tails, and explicitly reports whether the Lua PAD_SETUP marker ran. Cloud rerun [Actions #39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307) was in progress at the latest check.

This experiment distinguishes failure in PCSX-Redux GUI/OpenGL initialization or startup from a guest-game display problem. Do not label the title screen black after game entry unless the GUI run itself logs `[CHUNK1] done chunks=187` and `EXEC:PC0(80011448)` before the measured frames. Source-built CPU-trace dependency retest [Actions #39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) remains in progress; the run must complete its compile/preflight before trace conclusions can be made.


## Perbandingan cloud AnyLinux vs upstream-labelled HEAD — 2026-10-17

Run headless A/B terbaru [#39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307) memakai ROM/CUE dan OpenBIOS yang sama, mode interpreter/software GPU, setup Port 1 Analog yang sama, serta batas observasi 90 detik. Kedua AppImage mengenali disc SLPS-03553, membaca SYSTEM.CNF, menyelesaikan 187 chunk (382.976 byte payload EXE), lalu mencatat EXEC:PC0(80011448) dan Execute !. Keduanya tidak lagi mencatat Unknown command for pad: 43. Kedua proses mencapai batas waktu observasi; ini bukan crash yang terbukti dan bukan bukti game dimainkan.

Build di release:
- AnyLinux PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage, 65.747.557 byte, SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c, source commit 0c3572c3db75f97542001e453ae80ba8c3f8acba.
- AppImage bernama PCSX-Redux-HEAD-x86_64.AppImage, 91.474.424 byte, SHA-256 5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8. Package inventory mencatat source commit 9c6f98a0ed0581635f9123147e382c248e0f5ddc (2026-09-28), bukan source-build CPU-trace terbaru.

Diagnostik GUI [#39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307) mengonfirmasi GLX tersedia: Mesa llvmpipe, OpenGL 3.3. Jendela AnyLinux yang benar berhasil ditangkap pada 30/60/90 detik, tetapi seluruh frame 1280×800 seragam hitam (mean 0, stddev 0, 1 warna) dan OCR kosong. Log GUI mencapai penanda setup Lua dan hanya menampilkan progres chunk awal (indeks 0, 8, 16, 24, 32); tidak ada marker 187 chunk selesai, EXEC:PC0 atau Execute ! pada log GUI. Jadi masalah bukan ketiadaan GLX yang terbukti; jalur GUI masih berhenti sebelum executable handoff.

Workflow runner diperbaiki untuk menangkap jendela GUI kedua AppImage dalam kondisi setara dan membersihkan file frame/log sementara. Rerun [#39002136781](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002136781) baru queued ketika catatan ini ditulis. Source-build CPU trace kini menjalankan binary di dalam image Docker builder yang sama setelah run [#39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) gagal pada preflight host karena FFmpeg/SDL dari builder tidak tersedia di host. Rerun [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) masih berjalan saat pencatatan.

**Rekomendasi bersyarat:** gunakan AnyLinux sebagai kandidat utama operasional di runner standar (lebih kecil dan dipaketkan untuk kompatibilitas Linux), serta pertahankan AppImage berlabel HEAD sebagai pembanding cadangan, bukan sebagai “upstream HEAD terkini”. Untuk analisis instruksi gunakan source-build terpisah dengan API PCSX.CPU.Trace; jangan menganggap API itu tersedia pada kedua AppImage. Belum ada pemenang untuk gameplay/rendering: hasil GUI kedua build masih perlu diperiksa. Title/menu Naruto dan input dalam game belum terbukti; Story Mode belum dimulai.


## Verifikasi identitas build upstream — 2026-10-17

Pengecekan API upstream menunjukkan main/head PCSX-Redux saat diperiksa adalah commit [41f3196257d0962942b60983201aade951ebbd54](https://github.com/grumpycoders/pcsx-redux/commit/41f3196257d0962942b60983201aade951ebbd54), bertanggal 2026-10-17 02:53:17 UTC. Maka asset release dengan nama PCSX-Redux-HEAD-x86_64.AppImage (source 9c6f98a0, 2026-09-28) bukan current upstream HEAD; build AnyLinux menggunakan source 0c3572c3 (2026-10-01), dan source-build trace dipatok ke 6b9df482 (2026-10-16). Perbedaan ini membedakan identitas build, bukan membuktikan penyebab screen hitam.


## Verifikasi GUI A/B terbaru dan perbaikan harness — 2026-10-17

Run GUI A/B [#39002136781](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002136781) berstatus workflow `success`, tetapi **bukan hasil uji GUI yang berhasil**. Langkah headless di job yang sama tetap membuktikan kedua AppImage membaca disc `SLPS-03553`, menuntaskan 187 chunk executable, dan mencatat `EXEC:PC0(80011448)` serta `Execute !`; keduanya tidak lagi mencatat `Unknown command for pad: 43`. Saat masuk bagian GUI, `gui_probe.sh` berhenti untuk kedua build pada `PAD_SETUP: unbound variable` karena variabel shell tidak diekspor. Tidak ada jendela emulator yang ditemukan dan tidak ada frame yang ditangkap. Karena hasil probe tidak dipaksa menjadi kegagalan job, status `success` hanya berarti step berakhir tanpa kegagalan workflow yang terdeteksi; status itu bukan bukti GUI/game berhasil.

Perbaikan minimal sudah didorong ke runner pada commit [aac684d120ec025c4a87197da8d835f90b89f869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aac684d120ec025c4a87197da8d835f90b89f869): ekspor `PAD_SETUP` sebelum skrip probe GUI dipanggil. Rerun ROM privat [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) sudah dipicu dan masih `in_progress` pada pemeriksaan terakhir; hasil frame, OCR, boot-marker GUI, dan cleanup masih harus diperiksa dari log akhirnya.

CPU-trace run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) juga masih `in_progress`. Secret dan pengunduhan/verifikasi file privat telah dilewati; step source-build di container Docker yang dipatok digest masih berjalan, sedangkan capture trace dan cleanup belum dimulai. Belum ada `CPU_TRACE_SIZE` atau `CPU_TRACE_LINE` yang dapat dipakai untuk analisis.

Current upstream PCSX-Redux yang terverifikasi saat cek adalah [41f3196257d0962942b60983201aade951ebbd54](https://github.com/grumpycoders/pcsx-redux/commit/41f3196257d0962942b60983201aade951ebbd54) (2026-10-17 02:53:17 UTC). AppImage berlabel “HEAD” tetap build source 9c6f98a0, bukan upstream HEAD terkini. Tidak ada bukti bahwa judul/menu tampil atau input gameplay merespons; gate RT-001 tetap tertutup dan Story Mode tidak boleh dimulai.


## Hasil final GUI A/B setelah perbaikan PAD_SETUP — 2026-10-17

Run [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) selesai dengan workflow/job `success` pada runner commit [aac684d120ec025c4a87197da8d835f90b89f869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aac684d120ec025c4a87197da8d835f90b89f869). Hasil `success` bukan berarti kedua GUI berhasil menampilkan game. Job ROM selesai dan job smoke dilewati; tidak ada artefak Actions yang dipublikasikan.

- **Headless A/B (baseline terpisah):** kedua AppImage tetap mengenali BIOS OpenBIOS, disc `SLPS-03553`, `SYSTEM.CNF` dan target `SLPS_035.53`; masing-masing mencatat `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, serta `Execute !`. Keduanya mencapai batas observasi headless 90 detik (exit 124), bukan crash yang terbukti.
- **AnyLinux GUI:** `PAD_SETUP=port1 analog device connected and remapped` muncul; BIOS dan metadata disc serta `SYSTEM.CNF`/`BOOT` juga tercatat. Jendela yang ditemukan (X11 ID `2097204`) ditangkap langsung pada 30/60/90 detik, bukan root window Xvfb. Ketiga frame 1280×800 memiliki mean=0, stddev=0 dan 1 warna; OCR Jepang/Inggris kosong. Log GUI tidak memiliki marker chunk 187, `EXEC:PC0`, atau `Execute !`. Proses mencapai batas observasi 100 detik (exit 124). Artinya harness sudah berjalan dan menangkap window, tetapi jalur GUI belum membuktikan handoff executable.
- **AppImage berlabel “HEAD” GUI:** jendela emulator tidak ditemukan dan tidak ada frame pada 30/60/90 detik. Log final: `Unable to create main window: Couldn't find matching GLX visual` serta `SDL failed to create OpenGL 3.2 core context, retrying with any 3.0 profile`. Marker Lua `PAD_SETUP` dan executable-entry tidak muncul. Proses kembali dengan exit 137 sesudah batas observasi/eskalasi timeout; karena kegagalan pembuatan window sudah tercatat, jangan menyebutnya crash guest atau masalah ROM yang terbukti.
- Marker `Unknown command for pad: 43` tidak muncul pada kedua jalur headless maupun log GUI yang diperiksa. Ini tidak membuktikan input gameplay merespons.
- Langkah cleanup sukses dan mencatat bahwa ROM/BIOS/CUE, log, profil, frame, serta dua pohon AppImage sementara dihapus. Inventaris repo runner tetap hanya workflow, dokumentasi, README dan .gitignore; tidak ditemukan file media game atau artefak run.

## Status CPU trace source-build saat pemeriksaan terakhir — 2026-10-17

Run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849), commit workflow [16a6faff066b913480ad121b497db79df03a9de2](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/16a6faff066b913480ad121b497db79df03a9de2), masih `in_progress`. Unduh/verifikasi ROM/CUE/BIOS selesai pada 04:17:26 UTC; step build source pinned masih berjalan saat pengecekan berikutnya (sekitar paruh dari batas job 45 menit). Step capture trace dan cleanup belum mulai. Endpoint unduhan log job mengembalikan `BlobNotFound` sementara run aktif, sehingga belum ada bukti log build yang dapat dianalisis; artefak run belum ada. Belum ada hasil `PCSX_BUILD_RESULT`, `CPU_TRACE_SIZE`, `CPU_TRACE_LINE`, `TRACE_RESULT`, `CPU_TRACE_RESULT`, atau `TRACE_PROCESS_EXIT` yang terverifikasi. Jangan menjalankan duplikat atau menyatakan build gagal sebelum run selesai/batas waktu tercapai; periksa step aktif lagi sebelum deadline 45 menit.

**RT-001 tetap terbuka/terblokir.** Belum ada title/menu Naruto yang dikenali maupun respons input terkontrol. Jangan mulai Story Mode.

## Hasil final CPU trace source-build dan verifikasi GUI — 2026-10-17

Run [CPU trace #39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) telah selesai dengan kesimpulan `success`. Job 117306664750 berjalan 04:17:11–04:44:27 UTC. Download/verifikasi aset selesai 04:17:26; build source pinned selesai 04:43:46; capture trace 04:43:46–04:44:21; cleanup 04:44:21–04:44:25. Semua langkah berhasil. Source commit `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`, image builder `ghcr.io/grumpycoders/pcsx-redux-build@sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`. `PCSX_BUILD_RESULT` menyatakan build sukses; pemeriksaan `ldd` dalam image yang sama tidak menemukan dependency `not found`.

Capture membuktikan `VSYNC_TRACE` berlanjut melewati 1620, 1650, dan 1680; `CPU_TRACE_WINDOW=enabled frame=1620`; `CPU_TRACE_SIZE=16031631`; `TRACE_RESULT=VSync counter callbacks fired.`; `CPU_TRACE_RESULT=Built-in instruction records were printed.`; dan `TRACE_PROCESS_EXIT=124` pada batas observasi 35 detik yang memang dirancang. Run tidak menerbitkan artefak. Cleanup menyatakan ROM/CUE/BIOS, emulator, serta log trace sementara dihapus dari runner.

80 instruksi terakhir menunjukkan loop guest di PC mentah `0x000015a4–0x000015c4`: load dari `0x5de4(a3)` menghasilkan 0, cabang membandingkan dengan 2/1, dan `$v1` dihitung turun sambil kembali ke `0x000015a4`. Penghitung berkurang; ini eksekusi berulang yang bergerak, bukan bukti hang permanen. Run source-build ini tidak merekam `SYSTEM.CNF`, `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, atau `Execute !`. Jangan tetapkan pemilik loop sebagai BIOS, loader, atau overlay sebelum mapping divalidasi. Trace menyimpan `m_regs.pc` mentah menurut source pinned PCSX-Redux; alamat loop berbeda dari entry EXE `0x80011448`.

GUI A/B [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) juga selesai. AnyLinux GUI menjalankan `PAD_SETUP` dan menangkap window sebenarnya pada 30/60/90s, tetapi frame tetap hitam seragam dan tidak ada handoff EXE dalam log GUI. AppImage berlabel “HEAD” gagal membuat window akibat GLX/OpenGL. Kedua build di mode headless lama mencapai entry; bukti itu tidak bisa dipindahkan ke GUI atau source-build trace. RT-001 tetap **Open / blocked** sampai title/menu dikenali dan input terkontrol terbukti responsif.

## Perbandingan versi source terhadap baseline headless — 2026-10-17

Perbandingan GitHub langsung antara source AnyLinux `0c3572c3db75f97542001e453ae80ba8c3f8acba` dan source CPU-trace `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` menghasilkan selisih 803 commit. File yang berubah besar termasuk `src/core/cdrom.cc` (+1.476/-1.392 baris), `src/core/psxinterpreter.cc` (+290/-81), `src/core/pad.cc` (+362/-22), `src/core/psxmem.cc`, dan pointer submodule `src/mips`. Pada interpreter, macro target branch berubah dari memakai `_PC_` langsung menjadi `branchBase()` beserta pelacakan delay slot/exception; CD-ROM juga direstrukturisasi. Ini kandidat area pembandingan, bukan bukti akar masalah.

Kedua perintah headless memakai `-no-ui -exec ... -run -interpreter -softgpu -stdout -lua_stdout -logfile`; jadi jangan menyalahkan dynarec sebagai beda utama. Namun durasi observasi berbeda: AppImage headless diberi 90 detik dan mencapai EXEC:PC0; source-trace build hanya 35 detik dan merekam frames 1620–1680 sebelum timeout. Karena itu belum sah menyebutnya regresi source atau hang tanpa pengujian pada batas waktu yang sebanding. Langkah paling bernilai adalah trace source pinned pada window lebih akhir (mis. frames 4500–4560) dengan logging PC guest pada VSync berkala, serta marker boot dicetak terpisah dari ekor trace agar tidak terpotong oleh `tail`.


## Follow-up CPU trace dengan agregasi aman — 2026-10-17 (run masih aktif)

- Workflow runner diperkeras pada commit publik `d1c5b731befe5afacdfbdf3b9914b9f5e9f9ac64` (blob workflow `b06bb37d23c0fc7ff386ce0846e08f719b46d3bf`): observasi 90 detik, PC guest tiap 30 VSync, trace window frame 1620–1680 dan 4500–4560, ringkasan PC agregat saja, boot markers dipisah, cleanup `if: always()` dipertahankan. Source `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` dan image builder digest tetap sama.
- Run [#39004736399](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39004736399) menggunakan commit workflow tersebut. Pemeriksaan terakhir: secret check, workspace, dan download/verifikasi file lulus; build source masih `in_progress`; capture dan cleanup belum berjalan. Jangan menganggap pengujian runtime berhasil/gagal sebelum status dan log final diperiksa.
- Audit log publik menemukan 80 record instruksi/operand aktual pada run #39001985849; tidak ada artifact Actions. Run CPU-trace lama lain yang diperiksa tidak memuat record instruksi aktual. Workflow baru tak lagi mencetak record mentah. Log run #39001985849 masih dapat diakses; antarmuka GitHub yang tersedia di sesi ini tidak menyediakan tindakan penghapusan run/log.
- RT-001 tetap **Open / blocked**; title/menu Naruto dan respons input terkontrol belum terbukti.

## Hasil final CPU trace 90 detik — Actions #39004736399 (2026-10-17)

Run [#39004736399](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39004736399) selesai dengan status workflow/job `success`. Waktu run 05:01:31–05:29:40 UTC (12:01:31–12:29:40 WIB). Semua step selesai sukses: secret check, persiapan workspace, download/verifikasi aset, build source PCSX-Redux, capture/diagnostik, dan cleanup.

- ROM lulus pemeriksaan ukuran 325.989.552 byte dan SHA-256 `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`. CUE dinormalisasi hanya untuk referensi berkas sementara. Source pin `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`; builder image tetap `ghcr.io/grumpycoders/pcsx-redux-build@sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`.
- Build berlangsung sekitar 26 menit 20 detik, berakhir dengan `PCSX_BUILD_RESULT`. Pemeriksaan dependency `ldd` di image builder yang sama lulus tanpa library bertanda `not found`.
- Capture mencapai sampel VSync dari frame 30 sampai 4740, tiap 30 frame: 158 sampel. PC adalah `0x000015a4` pada 157 sampel; satu pengecualian sampel berada di frame 420 pada `0x00000870`, lalu PC kembali ke `0x000015a4`.
- Ringkasan CPU trace pada frames 1620–1680: 200 record diperiksa, 9 PC unik, total terlapor 16.031.631 record. Pada frames 4500–4560: 200 record, 9 PC unik, total terlapor 16.031.484 record. Kedua jendela memiliki pola hot PC yang sama; alamat teratas `0x000015c0` dan `0x000015c4` masing-masing muncul 23 kali, `0x000015a4` dan beberapa alamat tetangganya sekitar 22 kali.
- Boot marker yang terlihat: OpenBIOS dikenali, disc label `SLPS-03553`, disc ID `SLPS03553`, executable `SLPS_035.53;1`. Tidak terlihat `SYSTEM.CNF`/baris `BOOT =`, `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, atau `Execute !`.
- `TRACE_PROCESS_EXIT=124` adalah batas observasi 90 detik yang disengaja, bukan bukti crash guest. Tidak ada marker FATAL/Exception/ERROR pada bagian runtime yang disaring. Keluaran runtime baru hanya agregat PC dan tidak memuat record instruksi/operand mentah.
- Cleanup menyatakan ROM/CUE/BIOS, emulator hasil build, dan log runtime sementara telah dihapus dari runner ephemeral. Daftar artefak Actions kosong.

**Interpretasi:** pengujian memperkuat bukti adanya loop PC berulang dalam sesi OpenBIOS/disc, tetapi tidak mengidentifikasi pemilik loop dan tidak membuktikan handoff ke executable utama. Jangan menyebutnya kode game, hang permanen, atau akar masalah spesifik sebelum mapping alamat dan jalur pemanggil diverifikasi.

**RT-001 tetap Open / blocked.** Belum ada title/menu Naruto yang dikenali dan belum ada respons input terkontrol yang terbukti. Jangan mulai Story Mode. Log publik lama [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) masih perlu ditinjau karena memuat 80 record instruksi/operand; run baru ini tidak mengulangi keluaran mentah tersebut.
