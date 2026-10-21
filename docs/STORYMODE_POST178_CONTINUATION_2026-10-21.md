## LATEST VERIFIED CONTINUATION — roulette result, map movement, START dialogue skip (21 October 2026)

This update supersedes earlier “roulette behavior unknown / next test Circle on Roulette menu” guidance below. Story Mode is still NOT complete; there is no verified ending evidence.

### Verified gameplay path
- Run [#39609425942](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39609425942) preserved the roulette wheel checkpoint f120 (21,162,475 bytes; SHA-256 `7c8c8bfa4a15132a6c9a046aa842fc01d2f294d6e04d53262c20287566432222`). A longer no-input observation [#39612126429](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39612126429) reached external X11 f180 with the wheel still moving, then timed out before f300. It is not evidence the wheel stops by itself.
- Controlled branch experiment [#39613929898](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39613929898) compared NONE with one Circle press/release (relative f30/f38). Button readback passed. Circle branch visually showed sector 2 aligned under the pointer at f60/f100 and returned to the board by f180; NONE still showed the wheel at f180. Circle-result checkpoint: 21,163,057 bytes, SHA-256 `0570a687dd8ecc1449c8edaa436f21111e40433d59c6a21b0e64de6b71c07d5d`.
- Fresh-process no-input continuation [#39614665390](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39614665390) confirmed the board and roulette result 2 remained visible through f120. Map checkpoint: 21,162,853 bytes, SHA-256 `451c59b13ca1dbf93eb23afa94a096c7eb5721c5bb5108b45e9d2054289ffb53`.
- Map route experiment [#39615341661](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39615341661) compared NONE with one DOWN press/release (f30/f38). DOWN moved the token down one route and the visible move counter changed from 2 to 1; the subsequent scene/dialogue showed `イルカ (Iruka)` and text beginning `ナルトよく聞け、… (Naruto, dengarkan baik-baik, …; screenshot text is incomplete)`. DOWN branch checkpoint: 21,162,042 bytes, SHA-256 `6d01243a2e2c4b47e13a58373216bda0117a8b6e04324f2a6c3fde9b811ae494`.
- Dialogue skip [#39616129634](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39616129634) restored that checkpoint, sent START only at relative f30–f38 (press/release readback PASS), and captured external X11 screenshots through f120. The dialogue was skipped; the prompt now reads `ここに結界をはりますか？ (Apakah akan memasang penghalang di sini?)`, `必要チャクラ 120 (Chakra yang dibutuhkan: 120)`, with `はい (Ya)` highlighted and `いいえ (Tidak)` available. This only shows a required cost/prompt; it does not yet prove the cost is deducted or the barrier is placed. Current prompt checkpoint: 21,162,246 bytes, SHA-256 `789585c7c7a6d5e9f5bb1601d0e277e7735380b88d91f882f36a265aff419e4a`.

### Next action already queued
- Run [#39617444912](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39617444912), “confirm highlighted barrier YES with Circle”, is queued. It is prepared to restore the read-only prompt checkpoint, send one contextual Circle press/release, capture external X11 at f20/f60/f100/f120, and save a distinct private successor. At last check it had not started a job; there is no reliable completion ETA and no duplicate run should be launched.
- After it terminates, inspect job steps/logs, all four authentic X11 images, result report, source hash, and successor size/hash. Verify whether the prompt disappears, a barrier becomes visible, and the HUD Chakra actually changes from 1500. Do not infer barrier placement or Chakra debit from workflow success alone.
- The source checkpoint `789585c7…aff419e4a` must remain unchanged. The marker `experiments/.run-storymode-barrier-circle-confirm` is intentionally retained until this run is inspected, then must be deleted.

### Permanent constraints / current maturity
- Only this research repo is permitted. Never use Tile Duel or any other repo.
- All post-checkpoint gameplay proof is captured by real external X11 from the emulator; no web images and no internal PCSX screenshot API for these later states.
- Use START for all Story Mode dialogue; never use Circle to skip dialogue. Circle is permitted here only because the in-game YES option `はい (Ya)` is highlighted.
- Japanese text must immediately include Indonesian translation in parentheses.
- ROM, BIOS, savestates, Memory Card and gameplay images stay private; do not commit them to Git.
- The reusable checkpoint/input/X11/successor cycle is working for controlled steps, but an all-screen classifier, resilient adaptive gameplay policy, generic crash recovery and cross-session autonomous loop through all missions are not yet verified. Do not claim Story Mode completion without original in-game ending evidence.

---

## UPDATE — DOWN moves the highlighted menu item (21 October 2026)

Run [#39607704007](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39607704007) restored the f175 source independently for NONE and DOWN. DOWN press/release passed controller readback at frames 30/38. The original external X11 capture at frame 90 shows selection changed from `ルーレット (Roulette)` to `忍術 (Ninjutsu/teknik ninja)`. Post screenshot: mean absolute RGB diff 1.049238 and exact-pixel fraction 0.985733 against NONE, concentrated on the selection region. Thus DOWN is verified for moving the highlight one row in this menu; RIGHT remained visually ineffective in the previous matched test.

Private artifact #12348747349 digest: `sha256:340ff7064f4b4902122b9ecaeb926a4693716c41c21dc765461d989d34f15730`. No internal screenshot API was called and no private state or screenshot was committed to Git.

Next test one Circle confirmation from the original f175 checkpoint with Roulette highlighted, against NONE; this is menu confirm, not dialogue skip. Dialogues must be skipped with START.

---

## PEMBARUAN OTOMASI — uji RIGHT tidak mengubah menu; uji DOWN berikutnya (21 Oktober 2026)

Run [#39606938717](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39606938717) memulihkan checkpoint f175 pada proses emulator NONE dan RIGHT terpisah. Kedua proses sampai frame relatif 120 dan menyimpan state privat. RIGHT press f30/release f38 terbaca PASS, tetapi screenshot X11 pada frame 90 identik piksel dengan kontrol tanpa input. Layar asli menunjukkan menu vertikal dengan Roulette tersorot; RIGHT belum terbukti sebagai aksi navigasi yang efektif. Artefak privat #12348274409, ZIP SHA-256 `8b095bbe8e8d20f9ca639b4c2f3be448339556376f193d7b7487c94830e33027`.

Run [#39607704007](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39607704007) sedang menguji DOWN terhadap NONE dari checkpoint sumber f175 yang sama. Tunggu hasil dan periksa capture X11 asli sebelum memutuskan transisi berikutnya. Tidak ada screenshot/savestate yang ditambahkan ke Git.

---

## LATEST CONTINUATION — one START tap exits dialog; Konoha board view and f175 successor verified (21 October 2026, 18:20 WIB)

Run [#39591032125](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39591032125) used the verified pre-START dialog checkpoint, made one START press at relative f120 and release at f121, and sent no Circle input. The f140 state was saved as a derived checkpoint; a **fresh emulator process** then restored it and reached frame 175 without controller input. A successor savestate was created successfully.

The original external X11 capture after restoration shows the Konoha forest board/map, Naruto and Mizuki HUD each at 1500, and no dialogue panel. This confirms the transition from the dialog view to the board view, but not completion of a mission or Story Mode. There were 11 valid internal emulator screenshots up to f130 in phase 1, and phase 2 used external X11 only. No gameplay screenshots or savestates were committed to the repository.

Checkpoint hashes:
- Pre-START source (unchanged): `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`
- Derived after START f140: `3a0bb3f37537f393bcb1479f9a478bf90367ae669418523f12a34cfa39984034`
- Successor f175: `f8bd00074877ef583e35b8eaf2fc65b3877acda9bebd5f2d8e9a13abee094615`

Next: test controller directions one at a time from a read-only copy of f175 against a matched-duration no-input control. Use original X11 captures for later-state visuals; do not take internal emulator screenshots after resuming this later state. If dialog returns in any continued branch, press START, not Circle.

## POST-178 FORENSIC NOTE — dialog checkpoint preserved during GDB run #39588281198 (21 October 2026, 17:59 WIB)

This was a no-input diagnostic restore of the already-verified pre-START dialog checkpoint, not a restart of Story Mode and not a verified transition into active gameplay. Run [#39588281198](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39588281198) reached f172 before the callback stalled; GDB did not observe a natural SIGSEGV before the 60-second timeout (exit 124). The two original X11 captures still show the dialogue and Circle prompt with HUD 1500–1500. There is no new evidence that a mission is active or that Story Mode is complete.

Internal screenshots remain limited to f130 and passed validation. No controller input was sent, and neither the stable parent checkpoint nor the pre-START dialog checkpoint was modified. See [the forensic report](SIGSEGV_FORENSICS_2026-10-21.md) for the GDB/core-dump result.

## LATEST FORENSIC UPDATE — extended natural-crash observation through outer timeout, run #39586201539 (21 October 2026, 17:42 WIB)

- Run [#39586201539](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39586201539) completed with workflow conclusion `success` at 10:41:59 UTC. This continued the lightweight `catchsegv` test without GDB attached to the live emulator. No controller input was sent; the default renderer selection was retained.
- The frame callback stopped at **f154**; the watchdog confirmed no new callback for **2.554 seconds**. The process snapshot at stall showed `Sl`, about 159% CPU in the captured `ps` sample, and `wchan=futex_do_wait`. Unlike run #39585486518, the watchdog did **not** send SIGTERM after the screenshots; it left the emulator untouched until the existing outer 60-second timeout ended the process (exit code **124**).
- Two external X11 captures were valid at 1280×800: 781,067 bytes / 133,238 colors and 778,200 bytes / 131,633 colors. They were not pixel-identical. The original screenshots show a Naruto dialogue box, Circle prompt and HUD 1500–1500; subtle screen elements/sprite position change between captures even though no new frame callback is logged. This still does not prove an active mission or Story Mode completion.
- The extended observation did not produce a natural SIGSEGV, handler backtrace, or local core file. The report records `DIAG_CORE_FOUND=NO`, `DIAG_GDB_POSTMORTEM=NOT_RUN`, `DIAG_NATIVE_SIGNAL_TRACE_CAPTURED=NO`, and `DIAG_NONE_RESULT=STALL_OR_TIMEOUT_WITHOUT_START`. Thus the longer no-interruption window also fails to reproduce the original fatal crash.
- Artifact [#12340070622](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39586201539/artifacts/12340070622): 4,922,274 bytes; ZIP digest `sha256:6dd13863e749ae002bcb64164cfcf2d55b43d8000108b061c57455764ec891d4`. It includes 28 valid original internal screenshots through f130 only (`DIAG_SCREENSHOT_PROBLEMS=none`), two validated X11 captures, watchdog log and process snapshot. ZIP digest was rechecked after download. Parent checkpoint remained unchanged with SHA-256 `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee`; the pre-START dialog checkpoint was restored as a read-only copy with SHA-256 `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`.
- Interpretation: two no-input runs—one stopped by the watchdog after a 3-second post-capture window (#39585486518), the other allowed to run until the 60-second outer timeout (#39586201539)—both stall near f153–154 but fail to reproduce a natural SIGSEGV. X11 contents continue changing, so a total display/process deadlock is not established. Root cause of #39574435847 remains unknown. The one-shot trigger was deleted after this run (cleanup commit `1076dd3bf151915551e4469769e3c79541402dbf`); post-cleanup verification must keep queued/in-progress Actions at zero.

## LATEST FORENSIC UPDATE — lightweight signal-time trace run #39585486518 (21 October 2026, 17:35 WIB)

- Actions run [#39585486518](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39585486518) completed with workflow conclusion `success` at 10:35:18 UTC. This was a diagnostic run only: the emulator was launched through glibc `catchsegv` (`/usr/bin/catchsegv`), without GDB attached to the live process and with **no controller input**.
- The emulator/frame callback last reported **frame 153**. The watchdog confirmed no new callback for **2.571 seconds**. The process snapshot showed `Sl`, about 160% CPU in the captured `ps` sample, and `wchan=futex_do_wait`. Two external X11 captures were valid at 1280×800: 779,626 bytes / 132,431 colors and 780,189 bytes / 132,972 colors. They were not pixel-identical, so the display still changed even though the frame callback had stopped.
- After a further 3-second natural-crash observation window, no natural SIGSEGV, signal-time backtrace, or local core file appeared. The watchdog sent SIGTERM to the emulator. `catchsegv` returned wrapper exit code 255; the run’s original report called this `INCONCLUSIVE rc=255`, which was a classification gap, not evidence of a natural crash. Workflow classifier corrected afterward in commit `5944594eacb4fa89c5bb2df56294ba8ef4b4c65c` to classify this exact watchdog-stop case as a stall with no natural SIGSEGV observed during the window.
- Artifact [#12338379652](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39585486518/artifacts/12338379652): 4,922,798 bytes; ZIP digest `sha256:eccc7922d1e7b8a032768bed20ca8b09f87f86fed0cb7ec3a97b8475c5bc41d4`. The artifact reports 28 valid original internal screenshots only through f130 (`DIAG_SCREENSHOT_PROBLEMS=none`), and both external X11 captures. Core analysis says `DIAG_CORE_FOUND=NO`, `DIAG_GDB_POSTMORTEM=NOT_RUN`, and `DIAG_NATIVE_SIGNAL_TRACE_CAPTURED=NO`.
- Source checkpoint verification passed: parent stable checkpoint SHA-256 remained `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee`; pre-START dialog checkpoint stayed the verified read-only copy (21,162,258 bytes; SHA-256 `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`). The original X11 evidence still shows the Naruto dialogue, Circle prompt and HUD 1500–1500; it does **not** prove an active mission or Story Mode completion.
- Conclusion: running without GDB did not reproduce the natural SIGSEGV and yielded no fatal backtrace. It reproduced the f153 callback stall, while valid X11 captures continued changing. This supports investigating a rendering/timing stall, but neither proves a deadlock nor identifies the cause of the earlier SIGSEGV. The one-shot marker was removed after completion (cleanup commit `9d7ce0e16b077c6d4ef86019ba1f1330dced1fdb`); follow-up verification found 0 queued and 0 in-progress Actions runs.

## PEMBARUAN FORENSIK TERBARU — GDB menemukan stall di jalur renderer; akar SIGSEGV belum terbukti (21 Oktober 2026)

- **Run #39574435847** ([Actions](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39574435847)): frame terakhir 151, proses keluar 139 (`Segmentation fault (core dumped)`), `wchan=vfs_coredump`. Capture X11 pertama valid (1280×800, 777.527 byte, 131.762 warna); capture kedua hitam seragam 458 byte dan ditolak. Screenshot valid memperlihatkan dialog Naruto masih terbuka, prompt Circle, HUD 1500–1500; **bukan** bukti misi aktif.
- **Run #39576146808** ([Actions](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39576146808)): tidak mereproduksi SIGSEGV; frame terakhir 152 lalu timeout 124. Kedua screenshot X11 valid dan berbeda. `/proc/sys/kernel/core_pattern` mengarahkan dump ke `systemd-coredump`, tidak ada file core lokal yang bisa dipakai GDB.
- **Run #39576905583** ([Actions](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39576905583)): di bawah GDB frame terakhir 153; setelah stall, watchdog mengirim SIGINT diagnostik dan stack semua thread terekam. Thread utama berada di `__pthread_cond_wait` melalui `libgallium` → `libGLX_mesa` → `SDL3` → alamat tanpa simbol di binary `pcsx-redux`; thread renderer `llvmpipe` juga terlihat. Tidak ada SIGSEGV pada run ini.
- **Run #39577470148** ([Actions](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39577470148)): hasil sejalan; frame terakhir 153, dua screenshot X11 valid (779.646 byte/133.597 warna dan 779.635 byte/133.175 warna), lalu stack stall GDB dengan SIGINT. Hasil diagnostik `GDB_BACKTRACE_CAPTURED_AFTER_VSYNC_STALL_NO_START`; wrapper exit 0 hanya berarti GDB menyelesaikan capture, bukan mencapai f175.
- **Interpretasi terukur:** dua backtrace stall menempatkan thread utama pada penantian sinkronisasi renderer/OpenGL Mesa/SDL. Ini mengarahkan penyelidikan stall ke jalur renderer, tetapi belum mengidentifikasi penyebab SIGSEGV run #395744 dan bukan bukti Mesa/SDL penyebab crash fatal. Binary `pcsx-redux` stripped; core dump tidak tersedia di ruang kerja.
- Semua run diagnostik ini tanpa input controller; checkpoint dialog pra-START tetap 21.162.258 byte SHA-256 `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`; checkpoint induk tetap 21.163.483 byte SHA-256 `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee`. Screenshot internal hanya sampai f130 dan valid; screenshot eksternal hanya X11 asli. Tidak ada START yang dikirim, checkpoint tidak diganti, dialog masih terlihat; misi aktif/tamat tetap belum terbukti.
- **Run pembanding #39577891131** ([Actions](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39577891131)) selesai `success`: `GALLIUM_DRIVER=softpipe` diminta, frame callback terakhir 153; proses tetap aktif sekitar 98,3% CPU dan GDB menangkap instruction pointer di `libgallium` setelah SIGINT diagnostik, tanpa SIGSEGV alami. Dua screenshot X11 valid 794.275 dan 794.685 byte; keduanya menunjukkan dialog Naruto dan prompt Circle, serta berbeda 6.899 pixel (0,674%). Thread `llvmpipe` tak terlihat, tetapi renderer aktif belum dibuktikan lewat renderer string. Ini mungkin slow frame renderer software, bukan deadlock yang terkonfirmasi. Artefak privat #12334054908, digest ZIP `sha256:2f289d7cceb6673ea7e8ea1ba6d356bea8b71fca9d4f31351a84c91bc72bb7f9`. Workflow setelah uji ini telah dikembalikan ke pemilihan renderer default; `GALLIUM_DRIVER=softpipe` tidak dipaksakan untuk baseline berikutnya.
- **Kesimpulan:** SIGSEGV #395744 tetap belum punya backtrace fatal. GDB run #395769/#395774 menemukan thread utama menunggu melalui `libgallium` → `libGLX_mesa` → `SDL3`; run #395778 dengan softpipe berhenti di `libgallium` sambil menggunakan CPU tinggi. Petunjuk mengarah ke jalur renderer/timing, tetapi **akar penyebab SIGSEGV belum teridentifikasi**. Checkpoint induk hash `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee` tidak berubah; tak ada input controller; screenshot internal tetap dibatasi sampai f130. Detail dan batas kesimpulan: [docs/SIGSEGV_FORENSICS_2026-10-21.md](docs/SIGSEGV_FORENSICS_2026-10-21.md).

---

## HASIL TERBARU — watchdog VSync eksternal mencapai frame 151, lalu SIGSEGV (21 Oktober 2026, 16:08:25 WIB)

### Run, checkpoint, dan metode

- Run [#39574435847](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39574435847) berakhir pada 16:08:25 WIB dengan conclusion workflow **success**. Step emulator mencatat exit code **139**; kesimpulan workflow tidak boleh disamakan dengan emulator mencapai target f175.
- Tidak ada input kontrol selama run. Checkpoint dialog pra-START yang dipulihkan berukuran 21.162.258 byte, SHA-256 c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c. Checkpoint induk 21.163.483 byte, SHA-256 b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee diverifikasi utuh dan tetap read-only.
- Screenshot internal emulator dihentikan pada f130. Lua hanya melaporkan frame; timestamp presisi dan pengamatan stall berasal dari watchdog eksternal Python menggunakan time.monotonic() dan timestamp UTC. Capture luar dilakukan dengan xwd -root lalu konversi PNG, bukan melalui callback screenshot PCSX-Redux.

### Pengamatan terukur

- Watchdog mengamati frame 151 pada 16:08:10.907 WIB. Tidak ada frame baru selama 2,576 detik; stall dikonfirmasi pada 16:08:13.485 WIB.
- Tangkapan X11 pertama dimulai pada 16:08:13.494 WIB dan lolos pemeriksaan: 1280×800, 777.527 byte, 131.762 warna unik. Screenshot asli menunjukkan latar papan game, HUD Naruto dan Mizuki masing-masing 1500, portrait/nama Naruto, dialog berbahasa Jepang yang tetap terbuka, dan ikon prompt Circle.
- Tangkapan kedua dilakukan sekitar 16:08:15.782 WIB. Output hanya 458 byte dan satu warna hitam; validator eksternal menolaknya. Wrapper melaporkan emulator exit 139 sekitar 16:08:16.015 WIB.
- Snapshot process-state-at-stall.txt menunjukkan proses AppRun dalam state Sl, wait channel vfs_coredump, %CPU=76.2 pada sampling tersebut. wchan=vfs_coredump konsisten dengan proses berada di jalur kernel untuk core dump setelah sinyal fatal. Bersama exit code 139 dan layar X11 yang berubah menjadi hitam, ini sangat mendukung bahwa penghentian frame f151 berkaitan dengan crash fatal; belum diketahui fungsi/native path mana yang menyebabkan crash.
- Validasi screenshot internal menerima 28 gambar f001–f130 (DIAG_SCREENSHOT_PROBLEMS=none). Tidak ada permintaan screenshot internal setelah f130, sehingga bukti crash ini tidak bergantung pada screenshot internal pada f150.
- Artefak privat [#12333511723](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39574435847/artifacts/12333511723), 4.139.742 byte, digest ZIP sha256:63497731a6e361aff98f9e0f2f0a895010987b87250aadfc72c82a74ba6ed23c. Screenshot eksternal pertama di artefak bernama X11-stall-first.png; X11-stall-second.png sengaja tetap disimpan untuk mendokumentasikan layar hitam yang ditolak.

### Cross-check tanpa timestamp callback Lua

- Run [#39573924538](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39573924538) menambahkan timestamp pada callback Lua serta watchdog eksternal. Frame terakhir 140, tidak ada frame baru selama 2,549 detik, lalu exit 124 (timeout). Kedua tangkapan eksternal 1280×800 tidak seragam; perbandingan mendapati 13.172 dari 1.024.000 piksel berbeda (1,286%), sementara area teks dialog identik. Snapshot proses mencatat futex_do_wait, bukan vfs_coredump.
- Run [#39573533078](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39573533078) memakai gate awal f145. Frame terakhir yang diamati f140, sehingga watchdog tidak mengambil screenshot X11; timeout 124. Gate kemudian diturunkan ke f135.
- Perubahan titik berhenti dari f140/timeout pada run dengan timestamp Lua ke f151/crash pada run tanpa timestamp Lua berarti instrumentasi dapat mengubah timing atau runtime memang tidak stabil. Data yang ada tidak mengisolasi penyebab pastinya.

### Interpretasi dan langkah lanjut

- **Terverifikasi:** checkpoint sumber tidak berubah; tidak ada input START; tidak ada screenshot internal setelah f130; frame 151 terlihat dari watchdog; screenshot X11 pertama adalah tangkapan layar game asli yang valid; proses berakhir 139 dan snapshot state menunjukkan vfs_coredump.
- **Hipotesis kuat, belum akar sebab:** callback/log VSync berhenti karena jalur fatal crash; tangkapan eksternal kedua hitam karena display/renderer sudah hilang saat proses menuju exit. Belum ada backtrace atau core dump yang mengidentifikasi sumber native crash.
- **Status gameplay:** tangkapan valid memperlihatkan dialog Naruto belum tertutup dan prompt Circle masih tampak. Jangan menyatakan misi aktif, penyelesaian misi, atau Story Mode tamat.
- **Langkah berikutnya:** analisis crash dengan mengumpulkan informasi signal/thread/backtrace atau core dump yang dibatasi ukurannya sebelum eksperimen input baru. Jangan ulangi tap START satu-VSync yang sama. Jika dialog muncul saat permainan benar-benar dilanjutkan, aturan operasional tetap memakai START, bukan Circle. Jangan ganti checkpoint dan tetap gunakan screenshot asli dari emulator.

---

## HASIL TERBARU — paired NONE vs START dengan cutoff screenshot f130 (21 Oktober 2026, 15:38:40 WIB)

### Ringkasan run dan checkpoint

- Run [#39570556284](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39570556284) selesai `success` pada 15:38:40 WIB; durasi sekitar 2 menit 11 detik. Keberhasilan Actions menandakan runner, pemeriksaan, pengunggahan, dan pembersihan berhasil, **bukan** kedua emulator menyelesaikan target frame.
- Artefak privat #12331189717, `naruto-storymode-dialog-freeze-diagnostic-private`: 6.715.120 byte; digest ZIP `sha256:32c4a6313cbad378bf89a118a701b316552622ade57cb0687222c5d1f63c62c1`; kedaluwarsa 4 November 2026 sekitar 15:38 WIB. Digest dicocokkan kembali setelah unduh.
- Checkpoint dialog pra-START yang dipakai dua cabang: 21.162.258 byte, SHA-256 `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`. Checkpoint induk stabil: 21.163.483 byte, SHA-256 `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee`; hash induk tetap cocok dan tidak ditimpa.

### Desain serta hasil terukur

Workflow [`.github/workflows/naruto-storymode-dialog-freeze-diagnostic.yml`](../.github/workflows/naruto-storymode-dialog-freeze-diagnostic.yml) diubah lewat commit `227c71808997d4dc94d69d4d483ed4ca77280b1d` dan `a2f3b20a7e85bfc106175d14cd155ed9d17aa99c`. Kedua cabang memakai checkpoint dan kartu memori sementara terpisah yang sama sumbernya. Screenshot internal emulator hanya diminta sampai f130; log VSync/frame berjalan sampai target f175; timeout per proses 30 detik.

- Cabang `NONE`: frame terakhir tercatat f154; exit code 124 (timeout).
- Cabang `START`: tap START satu VSync pada f120 dan release f121, readback press/release `PASS`; frame terakhir tercatat f151; exit code 124.
- Kedua cabang tidak mencatat segmentation fault pada run paired dan tidak mencapai f175. Keduanya berhenti menghasilkan frame saat timeout, di area frame 151–154.
- Screenshot asli dua cabang identik pixel-for-pixel pada f1–f125. Perbedaan mulai pada f126 (exact pixels 0,997943; MAD 0,108524), membesar di f128 (exact pixels 0,743594; MAD 15,380616) dan f130 (exact pixels 0,737878; MAD 15,748424). Pada f130 panel dialog Naruto masih terlihat bergerak ke kiri; karena gambar sengaja tidak diminta sesudah f130, eksperimen ini tidak menyaksikan sendiri kondisi visual persis pada f150.
- Validasi menyatakan 56 screenshot valid, 28 per cabang, `DIAG_SCREENSHOT_PROBLEMS=none`. Validator menolak raw kosong, byte count/dimensi salah, PNG kosong, label frame di atas cutoff serta gambar satu-warna; f130 wajib ada di kedua cabang.
- Run kontrol [#39570013344](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39570013344), dengan capture berhenti f130 dan tanpa cabang START, mencapai f151 lalu timeout 124; tidak terjadi segfault. Artefak #12331014609 berukuran 3.359.778 byte, digest `sha256:1fae303ee0bbc8cd2c7c816618b6db65f888f7e490eaac52a1e16f1b5fbcacb3`.

### Interpretasi, batas, dan langkah berikutnya

- **Terverifikasi:** checkpoint sumber dapat dipulihkan; hash induk stabil tidak berubah; screenshot asli sampai f130 lolos validasi; tap START memiliki readback benar; dua cabang berhenti menghasilkan log VSync pada kisaran f151–f154 dan timeout 124.
- **Hipotesis:** permintaan `PCSX.GPU.takeScreenShot()` pada sekitar f150 mungkin berkaitan dengan segfault yang pernah terjadi pada #39565014834, karena tanpa permintaan screenshot terlambat run sekarang timeout tanpa segfault. Namun, belum ada bukti kausalitas. Stall VSync tampaknya tetap ada dan tap START tidak menghilangkannya.
- **Belum diketahui:** apakah emulator benar-benar membekukan eksekusi inti atau berhenti hanya mengirim callback VSync; apakah fungsi screenshot internal memicu native segfault; dan apakah papan yang pernah tampak pada screenshot f150 setelah START merupakan gameplay misi aktif.
- **Status misi:** tidak terbukti aktif. Tidak ada klaim penyelesaian misi ataupun tamat Story Mode.
- **Langkah yang disarankan:** jangan ulang tap START yang sama. Tambahkan timestamp/watchdog untuk VSync atau uji tangkapan layar eksternal X11 setelah log VSync berhenti, agar keadaan visual dapat diamati tanpa memanggil screenshot internal pada frame bermasalah. Jangan mengubah/menimpa checkpoint terverifikasi, jangan gunakan Circle untuk dialog, dan tetap hanya memakai screenshot asli emulator.

Trigger sekali-pakai sudah dihapus melalui commit `c7ff890e6ecc715712257f23c4c0072793c3c3d7`. Run cleanup #39571044132 selesai `skipped`; tidak ada run aktif pada pemeriksaan terakhir.

---

## HASIL TERBARU — kontrol setara tanpa input vs START tertunda (21 Oktober 2026, selesai 14:53:39 WIB)

- Run [#39565014834](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39565014834) selesai 14:53:39 WIB dengan conclusion workflow `failure`. Artefak privat [#12329546573](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39565014834/artifacts/12329546573), 7.101.006 byte, digest `sha256:f1052ba271d25e7668cc809455ef7ad59fb7ac84c05e081027f7c4fd4f6f2f45`. Tidak ada eksperimen aktif setelah pemeriksaan; marker pemicu satu-kali sudah dihapus.
- Kedua cabang memulihkan checkpoint dialog pra-START yang sama: 21.162.258 byte, SHA-256 `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`. Checkpoint induk stabil 21.163.483 byte dengan SHA-256 `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee` tetap tidak berubah.
- **Respons visual START terverifikasi:** cabang tanpa input dan cabang START identik pixel-for-pixel pada screenshot frame 1–125. START ditekan satu VSync pada frame 120 dan dilepas frame 121; readback press/release keduanya PASS. Mulai frame 126 terlihat perbedaan kecil (99,794% piksel tetap identik; MAD 0,109), di frame 128 dialog/portrait bergerak ke kiri (74,359% piksel identik; MAD 15,381), dan pada screenshot asli frame 150 panel dialog sudah menghilang sehingga papan/area permainan terlihat kembali. Ini membuktikan START memicu kemajuan visual/animasi penutupan dialog pada konteks ini.
- **Batas bukti:** frame 150 itu belum membuktikan misi berjalan aktif atau Story Mode selesai. Tidak ada input gameplay setelah tap START dan belum ada bukti penyelesaian misi.
- **Runtime belum stabil pada kedua cabang:** cabang tanpa input melaporkan frame 150 lalu segmentation fault (kode 139); screenshot `DIAG-NONE-f150` tercatat tetapi buffer gambarnya nol byte, sehingga verifikasi screenshot menolak artefak itu. Cabang START menghasilkan screenshot asli frame 150, lalu tidak bergerak lagi dan timeout (kode 124) setelah batas 20 detik. Karena kontrol tanpa START juga crash pada frame 150, hang/segfault bukan bukti bahwa START sendirilah penyebab tunggal. Workflow berakhir `failure` akibat validasi buffer screenshot kontrol yang kosong, bukan karena semua eksperimen gagal.
- **Langkah diagnostik selanjutnya:** jangan mengulang tap START yang sama. Jalankan kontrol tanpa input dengan pengambilan screenshot dihentikan sebelum frame 150, sambil tetap mencatat VSync, untuk memisahkan crash emulator dari masalah fungsi screenshot. Setelah itu, lanjutkan dari checkpoint dialog pra-START yang sama jika pemulihan masih lulus. Semua bukti gameplay tetap berasal dari screenshot asli emulator dan artefak run terverifikasi.

# Eksperimen kelanjutan setelah konfirmasi Circle — 21 Oktober 2026

## Follow-up terbaru — START pada dialog Naruto (14:01 WIB)

## HASIL TERBARU — uji START pada dialog Naruto (21 Oktober 2026, 14:01 WIB)

- Run terbaru [#39558959143](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39558959143) selesai `failure` pada 14:01:53 WIB. Tidak ada run workflow dialog START yang masih aktif pada pemeriksaan setelah selesai. Pemicu satu-kali sudah dihapus agar tidak memicu eksperimen duplikat.
- Artefak screenshot/log privat [#12326872574](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39558959143/artifacts/12326872574), sekitar 1,96 MB; tangkapan asli diperiksa langsung setelah diunduh dari artefak.
- **Terverifikasi:** checkpoint stabil terakhir dapat dipulihkan dalam proses emulator baru. Dialog dengan potret dan nama Naruto tampak pada screenshot asli f179. START ditekan dan dilepas sebagai tap satu-VSync; log readback menandai press f179 dan release f180 sebagai PASS. Screenshot f180 berbeda dari f179 (MAD RGB 16,637; sekitar 28,41% piksel berubah), tetapi f180 dan f181 identik tepat (MAD 0; 100% piksel identik).
- **Kegagalan run:** emulator berhenti menghasilkan frame setelah f181 dan proses berakhir karena timeout (kode 124). Tap START kedua yang direncanakan setelah f182 **tidak pernah terkirim**. Run sebelumnya #39558656073 menunjukkan frame hingga f182 tetapi berakhir segmentation fault (kode 139). Run #39558242453 juga timeout setelah f181 ketika START ditahan lebih lama.
- **Batas kesimpulan:** START memang dikirim sesuai aturan, tetapi perubahan f179→f180 belum membuktikan START menyebabkan transisi karena tidak tersedia kontrol tanpa input yang sepadan pada checkpoint dialog. Dialog tidak terbukti tertutup; belum ada screenshot yang membuktikan misi aktif. Belum ada bukti Story Mode tamat.
- **Langkah berikutnya:** jangan mengulang eksperimen yang sama tanpa mengatasi freeze/crash sekitar frame 181. Pertahankan checkpoint induk dan checkpoint stabil; diagnosis runtime/frame scheduling terlebih dahulu atau ambil checkpoint dialog dari titik yang tidak mengalami crash, lalu uji START dalam cabang yang dipisahkan. Bukti visual gameplay hanya dari screenshot emulator asli.

### Kronologi run dialog START

- [Run #39557821644](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39557821644): segmentation fault kode 139 sebelum START pada f179; artefak [#12326123328](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39557821644/artifacts/12326123328).
- [Run #39558242453](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39558242453): START press terbaca PASS pada f179, emulator timeout kode 124; screenshot tersedia sampai f181. Artefak [#12326777425](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39558242453/artifacts/12326777425).
- [Run #39558656073](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39558656073): tap START satu-VSync terbaca; screenshot tersedia hingga f182, kemudian segmentation fault kode 139. Artefak [#12326946348](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39558656073/artifacts/12326946348).
- [Run #39558959143](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39558959143): menguji tap kedua setelah f182, tetapi proses timeout pada tahap setelah f181; tap kedua tidak tercatat. Artefak [#12326872574](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39558959143/artifacts/12326872574).


## Validasi workflow setelah perbaikan assertion — 21 Oktober 2026, 13:25 WIB

Run [#39555023915](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39555023915) dimulai 13:22:40 dan selesai 13:25:23 WIB dengan status `failure`. Perubahan assertion f180 bekerja; kali ini penyebabnya adalah cabang `NONE` timeout 25 detik (exit code 124) dan gagal menghasilkan baseline f180. Cabang `UP`, `DOWN`, `LEFT`, `RIGHT`, `CIRCLE`, dan `START` masing-masing mencapai frame 180 dengan exit code 0. Karena baseline `NONE` tidak lengkap, report dengan benar menandai perbandingan penuh sebagai tidak lengkap, walau sampel visual sampai f150 tersedia.

Artefak privat [#12324829071](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39555023915/artifacts/12324829071) berukuran 12.288.355 byte, digest ZIP `sha256:04a010dc88d6b40b8fc7ce1339bff7e03d56d4ad03035682670c749a6254312d`. Checkpoint terbaru: 21.163.483 byte, SHA-256 `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee`. ZIP dan manifest cocok; artefak tidak menyertakan ROM, BIOS, atau Memory Card.

Workflow terkini tetap [`.github/workflows/naruto-storymode-post178-advance.yml`](../.github/workflows/naruto-storymode-post178-advance.yml), dengan assertion f180 serta tanpa langkah simpan dialog yang belum stabil. Validasi #39555023915 merupakan run pertama sesudah perbaikan ini. Tidak ada run aktif; trigger marker sekali-pakai telah dihapus. Hasil visual utama tetap dirujuk ke run #39553585285, karena semua cabangnya mencapai f180 dan report-nya lengkap meski conclusion workflow gagal pada assertion lama.


## Pembaruan hasil kontrol pascakonfirmasi — 21 Oktober 2026, 13:16 WIB

### Run dan checkpoint utama

Run [#39553585285](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39553585285) berlangsung 13:08:16–13:10:14 WIB dan mengumpulkan screenshot sampai 180 VSync untuk cabang `NONE`, `UP`, `DOWN`, `LEFT`, `RIGHT`, `CIRCLE`, dan `START`. Status workflow akhir `failure` disebabkan assertion akhir yang masih mengharapkan `frame=60`; cabang sudah memakai target 180. Laporan perbandingan dan tangkapan layar menunjukkan semua cabang mencapai f180 dan sampel valid pada run tersebut.

Checkpoint pascakonfirmasi yang dibuat oleh langkah stabilisasi, setelah restore checkpoint turunan lalu 62 VSync tanpa input:
- Ukuran: 21.163.261 byte.
- SHA-256: `1f9da9ca07fb95a8afda5016799852f4e0fdda2d589c8d11e99b0f8e8ade4875`.
- Artefak privat [#12323544613](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39553585285/artifacts/12323544613), `naruto-storymode-post178-advance-private`, 12.344.333 byte, digest ZIP `sha256:620d857a0e79aa4bec86da50a1c92f1f4563753b16a0fe6ae3935d25c6f50d13`.
- Hash checkpoint induk tetap `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`; hash checkpoint turunan sumber tetap `a87529407736b1b7648785db8644d3c10f0b8d5d12f1557c63d9a3155b22fa83`. File induk tidak ditimpa.
- ZIP dan hash checkpoint dicek ulang setelah unduh; artefak tidak mengandung ROM, BIOS, atau Memory Card.

### Temuan input pada layar banner 「始め！」

Semua cabang memulihkan checkpoint baru dalam proses emulator terpisah. Tombol cabang non-`NONE` ditahan selama delapan VSync dari f90 sampai f98; tiap cabang berjalan 180 VSync. Pada semua frame pembanding hingga f180, `UP`, `DOWN`, `LEFT`, `RIGHT`, dan `START` identik piksel dengan `NONE`. Ini hanya berlaku untuk konteks layar dan timing percobaan tersebut, bukan bukti universal bahwa tombol itu tidak memiliki fungsi.

`CIRCLE` berbeda:
- f97: MAD 1,913; proporsi piksel identik 0,69432.
- f98–f100: perbedaan visual tumbuh saat banner mulai bergeser.
- f120: MAD 56,297; proporsi piksel identik 0,07862. Cabang `NONE` masih menampilkan banner `始め！`; cabang Circle menampilkan papan tanpa banner.
- f150: pemain/token terlihat berpindah ke bagian papan berikutnya.
- f180: cabang Circle menampilkan tampilan dialog dengan potret dan nama Naruto; cabang `NONE` masih menampilkan banner `始め！` (MAD 70,194; piksel identik 0,06029).

Kesimpulan terverifikasi: Circle menghasilkan perubahan visual konsisten dan memajukan layar dari banner `始め！` ke tampilan papan/dialog dalam eksperimen ini. Makna input sangat mungkin merupakan konfirmasi untuk memulai/lanjut dari banner tersebut, tetapi mekanik misi dan kondisi menang belum diverifikasi.

Contoh screenshot asli dari artefak run:
- [NONE f120](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39553585285/artifacts/12323544613) — gambar ada di artefak privat.
- [CIRCLE f120 dan f180](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39553585285/artifacts/12323544613) — banner hilang lalu dialog Naruto terlihat.

### Ketidakstabilan pada replikasi dan batas status

Run [#39554130946](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39554130946), 13:13:44–13:16:08 WIB, mencoba checkpoint dialog setelah cabang Circle. Hasilnya tidak lengkap:
- Cabang `RIGHT` mengalami segmentation fault, exit 139; metadata screenshot f180 tertulis tetapi buffer raw berukuran 0 byte.
- Cabang `CIRCLE` berakhir timeout, exit 124 setelah f150; tidak ada screenshot f180 sehingga checkpoint dialog tidak dibuat.
- Langkah pengumpulan artefak dan pembersihan runner berhasil, tetapi langkah eksperimen gagal karena screenshot tidak lengkap. Jangan menafsirkannya sebagai hasil kontrol setara sampai f180.

Eksperimen yang lebih awal:
- [#39552282942](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39552282942): checkpoint 21.163.482 byte, SHA-256 `fc17e5752a036ca3301c1d58de863af8105015f8bbb608bc4d87d4fa76244d90`; restore baru berhasil, 60 VSync pada NONE/CIRCLE/START, gambar sama.
- [#39552697314](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39552697314): checkpoint 21.163.751 byte, SHA-256 `39ae2c2c719ab206946829b4fae67712cc52b0b72dd24b1ad46641b35db014c9`; input Circle/START sesudah panel bergeser, 60 VSync, gambar sama.
- [#39552998498](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39552998498): checkpoint 21.163.570 byte, SHA-256 `11321efd96f5225d03613d2ae4f66e595b4cbd28c0ab6ba63057a1ff3e42b6d9`; Circle/START ditahan 8 VSync mulai f45, gambar sama hingga f60.
- [#39553261685](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39553261685): checkpoint 21.163.366 byte, SHA-256 `b310f2ffb086e872b6166b729c0304122506a39270ec84812968c100ac001b99`; D-pad ditahan 8 VSync mulai f45, gambar sama hingga f60.

Ukuran/hash checkpoint hasil create-save dapat bervariasi antar-run walau keadaan visual sumber serupa; catat masing-masing dengan run-nya dan jangan saling mengganti. Belum ada bukti tamat Story Mode atau save/load Memory Card in-game.

### Workflow dan langkah berikutnya

Workflow yang benar adalah [`.github/workflows/naruto-storymode-post178-advance.yml`](../.github/workflows/naruto-storymode-post178-advance.yml). Commit `544b96641518cbfc2fafdaa7c38e98ed521dd80b` menghapus percobaan save checkpoint dialog yang belum stabil serta memperbaiki assertion agar mencari f180, bukan f60. Setelah perbaikan, run #39555023915 dijalankan dan berakhir failure karena cabang NONE timeout; tidak ada run aktif dan marker satu-kali sudah dihapus.

Langkah berikut: gunakan checkpoint stabil dari artefak #12323544613 sebagai rujukan, ambil state tepat sebelum transisi layar dialog pada jendela yang aman (sebelum titik timeout/crash), lalu uji START dibanding Circle dan tanpa input dalam proses baru dengan timeout per cabang pendek. Tetap simpan ROM/BIOS/savestate/Memory Card hanya di artefak privat/runner; jangan pernah commit berkas-berkas itu ke Git.


## Tujuan dan desain

Eksperimen menguji apakah checkpoint turunan yang disimpan setelah Circle kedua ditekan pada f175 dan dilepas pada f178 bisa terus berjalan tanpa input, serta membandingkannya dengan cabang kontrol yang memuat checkpoint induk, menekan Circle pertama pada f30–f38, lalu menunggu tanpa Circle kedua.

- Workflow: [.github/workflows/naruto-storymode-post178-advance.yml](../.github/workflows/naruto-storymode-post178-advance.yml)
- Run: [#39546339666](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39546339666)
- Mulai 11:51:43 WIB; selesai 11:53:02 WIB, 21 Oktober 2026. Status Actions akhir: `success` (durasi sekitar 1 menit 19 detik).
- Artefak privat: [#12321752942](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39546339666/artifacts/12321752942), nama `naruto-storymode-post178-advance-private`, 3.640.848 byte, digest ZIP `sha256:20df28b96b8e4613c9dd5f298be82443b84f80203c2c7166409d43a51a7f5221`. Artefak memuat PNG, raw screenshot, metadata dan log; tidak memuat ROM/BIOS atau savestate hasil baru.

## Validasi checkpoint

Checkpoint turunan diunduh dari artefak privat #12314982935, diverifikasi sebelum dimuat, dan digunakan hanya sebagai berkas baca untuk restore:

- Turunan: 21.162.838 byte; SHA-256 `a87529407736b1b7648785db8644d3c10f0b8d5d12f1557c63d9a3155b22fa83`.
- Induk: 21.162.405 byte; SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`.
- Kedua hash diperiksa ulang setelah proses emulasi dan tetap cocok: `POST178_PARENT_CHECKPOINT_UNCHANGED=PASS`, `POST178_DERIVED_CHECKPOINT_HASH_STABLE=PASS`.
- Restore checkpoint turunan dalam proses emulator baru berhasil: `POST178_LOAD_EVENT=PASS`, `POST178_LOAD_RETURNED=1`, screenshot f1 dan f10 tercatat, serta cabang turunan menyelesaikan 62 VSync dengan kode keluar 0. Tidak ada input tombol setelah state turunan dimuat.
- Checkpoint induk tidak ditimpa. Masing-masing cabang memakai file Memory Card sementara terpisah.

## Hasil runtime dan perbandingan screenshot

### Cabang kontrol: checkpoint induk + Circle pertama saja

- Restore, event/load-return, serta pembacaan tekan Circle f30 dan release f38 lulus.
- Snapshot tersedia pada frame logis f179 sampai f187.
- Proses emulator mengalami native segmentation fault setelah screenshot f187 dan keluar dengan kode `139`; tidak ada screenshot f188. Jadi cabang kontrol tidak menyelesaikan target f240, dan screenshot setelah f187 tidak tersedia.

### Cabang turunan: restore checkpoint sesudah Circle kedua, tanpa input

- Proses baru memuat checkpoint turunan, lalu menyelesaikan 62 VSync tambahan tanpa menekan tombol, sampai `POST178_BRANCH_DONE mode=DERIVED_CONTINUE frame=62 load_event=true load_returned=true`.
- Screenshot dibandingkan pada jumlah VSync pascakondisi yang setara: control f179 vs turunan f1, f180 vs f2, f181 vs f3, dan seterusnya.
- Hasil cocok tepat sampai control f181/turunan f3 (`MAD=0.000, exact=1.00000`).
- Perbedaan mulai terukur pada control f182/turunan f4 (`MAD=3.185, exact=0.96749`). Perbedaan membesar pada control f184/turunan f6 (`MAD=8.204, exact=0.91152`), kemudian control f186/turunan f8 (`MAD=6.863, exact=0.92570`).
- Pada screenshot turunan f62, panel `任務内容` masih tampil, dengan target `3000チャクラためる` dan `ついか条件なし`. Prompt `けってい` yang terlihat pada f178 sudah tidak tampak; cap/tanda merah menyerupai kanji `決` muncul di sisi kanan bawah panel. Ini merupakan perubahan visual pascakonfirmasi yang stabil pada screenshot akhir, bukan sekadar pembacaan input controller.

### Interpretasi yang dibatasi bukti

- Kode keluar workflow `success` berarti pemeriksaan checkpoint, pengumpulan screenshot, komparator, dan upload berhasil. Itu **tidak** berarti kedua proses emulator berakhir normal: kontrol berhenti dengan kode 139, sedangkan cabang turunan berakhir normal dengan kode 0.
- Fakta bahwa cabang turunan mencapai f62 lokal—sekitar titik ekuivalen control f240—sedangkan kontrol crash setelah f187 mendukung bahwa state pascakonfirmasi mengubah perilaku runtime dan menghindari crash yang terlihat di cabang kontrol selama jendela observasi ini. Penyebab native crash secara keseluruhan masih belum diketahui.
- Pergeseran panel, cap merah, dan hilangnya prompt adalah bukti UI berubah setelah konfirmasi. Karena panel isi misi tetap muncul sampai 62 VSync tanpa input, bukti ini **belum** membuktikan gameplay misi sudah aktif atau Story Mode berlanjut ke papan/pertarungan berikutnya.

## Klasifikasi

- **Terverifikasi:** checkpoint turunan sesuai ukuran/hash, dapat dipulihkan dalam proses emulator baru, dan berjalan 62 VSync tanpa input; checkpoint induk dan turunan tidak berubah; cabang kontrol mencapai f187 lalu crash (kode 139); perbedaan visual pascakonfirmasi mulai tampak pada f182/ f4 turunan; prompt `けってい` hilang dan cap merah tampak pada gambar akhir.
- **Hipotesis:** konfirmasi Circle memicu animasi/tahap UI pascakonfirmasi dan berhubungan dengan penghindaran crash yang dialami cabang kontrol. Hubungan kausal untuk crash native belum terbukti.
- **Belum diketahui:** apakah harus ada input lanjutan untuk menutup panel isi misi; apakah state berikutnya sudah gameplay aktif; syarat dan mekanik gameplay; save/load Memory Card dari dalam game; dan tamat Story Mode.

## Langkah berikutnya

Simpan state turunan baru setelah panel pascakonfirmasi stabil (misalnya pada 62 VSync) di artefak privat, lalu verifikasi restore state itu dalam proses baru. Setelah ada state tersebut, uji satu input terisolasi per cabang (misalnya Circle vs START vs tanpa input), ambil screenshot sepadan, dan tentukan tindakan berikutnya dari respons layar yang benar-benar terlihat. Jangan menebak bahwa misi sudah dimulai hanya karena prompt awal hilang.
