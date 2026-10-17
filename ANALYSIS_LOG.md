## Hasil histogram GP0 per rentang VSync — 2026-10-18 (Actions #39080239541)

Run [#39080239541](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080239541) selesai dengan target VSync 300 dan exit code 0. Dump GPU ter-parse lengkap/not truncated, 299 VSync live packets. Bucket GP0 berbasis jumlah VSync live:
- 000–049: 0 words / 0 commands.
- 050–099: 0 words / 0 commands.
- 100–199: 0 words / 0 commands.
- 200–299: 43 words, seluruhnya terparse (42 commands): 39 GPU-state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP; stop reason `end_of_stream`. GP1 live: 16 words; ThrowAway: 5 words. Tidak ada family triangle/quad/line/textured sprite pada capture ini. Dump mentah dihapus; artifact privat hanya menyimpan ringkasan hitungan dan status CPU.

Sampler CPU per run mencatat marker `Execute !` sekitar t=38.01s; PC masuk executable pada t=38.33–40.91s, lalu kembali ke BIOS mulai sekitar t=42.20s, dan masuk executable lagi sekitar t=88.39–98.63s. Semua GP0 words berada di bucket 200–299, selaras dengan kemunculan CPU di executable menjelang akhir observasi. Marker timestamp dari `pcsx.log` dipakai agar buffering stdout tidak merusak korelasi. Ini bukti urutan yang konsisten, belum membuktikan penyebab CPU meninggalkan executable atau mengidentifikasi monochrome rectangle secara visual.

Langkah berikutnya: saat RSP tersambung, ambil window memori kecil secara privat di sekitar PC executable yang sudah teramati (`0x8003717c`, `0x8003c0b4`, `0x80037320`, `0x800372d8`) dan ekspor hanya statistik kategori instruksi/cabang (mis. syscall, branch, jump, load/store, backward-branch count)—tidak pernah menulis byte mesin/disassembly mentah. Tujuannya memeriksa apakah alamat tersebut bagian dari loop tunggu atau jalan kembali ke BIOS. **RT-001 tetap Open / blocked.**

---

## Hasil korelasi CPU/GP0 dengan marker bertimestamp — 2026-10-18 (Actions #39079981314)

Run [#39079981314](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079981314) selesai dengan conclusion `success`; emulator mencapai target VSync 300 lalu dihentikan normal oleh probe (`EMULATOR_EXIT_CODE=0`). Aset privat serta hash BIOS/ROM/AnyLinux diverifikasi. Tidak ada raw GPUDump atau instruksi/operand mentah di artifact.

**GPUDump setelah TraceBegin:** 299 VSync packets / 598 words; GP0 8 packets / 43 words; GP1 11 packets / 16 words; ThrowAway 5 packets / 5 words; truncated=false. Pretrace GP0 baseline 262153 words adalah reset + VRAM upload untuk state awal dump, bukan rendering game. Parser sementara mengonsumsi semua 43 live GP0 words tanpa sisa dan mengklasifikasikannya sebagai 42 perintah: GPU-state-setting=39, clear-cache=1, monochrome-rectangle=1, NOP=1. Tidak ada keluarga triangle, quad, line, atau textured sprite pada jendela sampai VSync 300. Ini berarti ada sedikit traffic grafis, tetapi belum ada gambar yang terlihat; screenshot Software GPU 320×240 dan screenshot jendela X11 1280×800 tetap hitam pada run sebelumnya.

**Korelasi CPU:** RSP tersambung; `qSupported` berhasil; 76 paket bulk register valid sebelum target berhenti. Marker log yang kini ditimestamp dari `pcsx.log`: SYSTEM.CNF sekitar t=4.85s, BOOT path t=6.14s, EXEC header dan `Execute !` sekitar t=38.01s. Sampel PC segera sesudahnya masuk ke executable utama (t=38.33s `0x8003717c`, t=39.62s `0x8003c0b4`, t=40.91s `0x80037320`), lalu kembali ke BIOS range mulai sekitar t=42.20s. Sampel berada di BIOS sampai sekitar t=87.09s dan masuk lagi ke executable pada t=88.39s (`0x800372d8`), dengan beberapa sampel lanjutan di `0x80037320/0x800372d8` hingga t=98.63s. CP0 Status umumnya `0x40000401`, BadVAddr nol, Cause umumnya `0x400`; dua sampel Cause `0x20` tidak cukup untuk menyimpulkan root cause tanpa sampling lebih rapat. Timestamp dari `pcsx.log` dipilih karena stdout buffered; jangan gunakan timestamp marker lama dari stdout sebagai korelasi akurat.

Interpretasi: host Mesa/GLX sehat; guest CPU masuk ke executable sebentar-sebentar tetapi pada jendela sekitar 100 detik hanya mengirim 43 GP0 words (kebanyakan state command, satu monochrome rectangle), dan tidak menampilkan title/menu. Ini lebih konsisten dengan masalah inisialisasi/looping guest daripada kebutuhan GPU fisik, tetapi akar sebab belum dipastikan. Probe berikutnya akan mengelompokkan waktu GP0 command berdasarkan VSync range agar terlihat apakah semuanya hanya terjadi saat startup.

**RT-001 tetap Open / blocked.** Belum ada title/menu yang dikenali, perubahan state dari input yang diverifikasi, atau Story Mode.

---

## Hasil final GPUDump sampai timeout dan probe korelasi CPU berikutnya — 2026-10-18

Run [#39079291837](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079291837) selesai dengan conclusion Actions `success` (semua langkah/cleanup berhasil), tetapi proses emulator berakhir pada batas observasi 90 detik (`EMULATOR_EXIT_CODE=124`); jangan mengartikan status workflow sebagai game sukses boot. Log mencapai `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, `EXEC:PC0(80011448)` dan `Execute !`. GPU traffic dump ter-parse lengkap, `GPU_DUMP_TRUNCATED=false`, satu marker `TraceBegin`, dan 268 VSync packets / 536 live words. Sesudah TraceBegin: **GP0 packets=0, words=0; GP1 packets=1, words=1; VSync packets=268**. Baseline pre-trace GP0 262153 words berisi reset dan full 1024×512 VRAM upload untuk merekonstruksi keadaan awal dump, bukan gambar yang dikirim game. Dump mentah dihapus sebelum upload artifact, yang hanya menyimpan ringkasan teks/log. Emulator timeout 124 adalah batas observasi, bukan crash diagnosis.

Untuk menghubungkan hasil grafis dengan CPU, workflow [`naruto-fastboot-gpu-traffic-summary.yml`](.github/workflows/naruto-fastboot-gpu-traffic-summary.yml) kini diperbarui agar satu run men-sample bulk RSP register `g` (PC + CP0 Status/BadVAddr/Cause) dengan timestamp relatif dan marker loader sambil merekam GPUDump, tanpa instruksi/operand mentah. Commit terbaru [`30cd69d6`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/30cd69d61a5ab01761baa7f3a209a386f205b650); run konfirmasi [#39079600379](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079600379) terakhir terlihat pending di antrean ketika entri ini dibuat. Periksa log/run selesai sebelum menafsirkan sampel itu.

Kesimpulan tetap terbatas: host GLX/Mesa sehat; jendela emulator dan screenshot software GPU hitam; tak ada GP0 drawing command yang terekam pada 268 VSync pasca-TraceBegin. Ini menunjuk ke inisialisasi/eksekusi game tamu, tetapi tidak menentukan akar sebab. **RT-001 tetap Open / blocked.**

---

## Pembuktian GL host dan traffic GPU tamu — 2026-10-18

- Run OpenGL mandiri [#39049689832](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39049689832): Mesa `llvmpipe (LLVM 21.1.8, 256 bits)`, OpenGL 4.5 Core/Compatibility Profile, tanpa version override; konteks Compatibility 3.3 berhasil dibuat. Host GLX/Mesa sehat, dan belum ada alasan teknis untuk menuntut GPU fisik.
- Source build pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`: `GPU::takeScreenShot()` bawaan melempar `Not yet implemented`; backend OpenGL GPU tidak mengimplementasikannya, sedangkan Software GPU punya implementasi screenshot. Run [#39078905140](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078905140) dengan `-softgpu` menghasilkan screenshot frame 300 valid 320×240 tetapi seluruh piksel hitam; VRAM 1024×512 juga satu warna hitam.
- Run window capture [#39079066598](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079066598) mengambil enam screenshot jendela PCSX-Redux non-root XID `0x200034` pada t=5,15,30,45,60,75 detik. Semuanya valid 1280×800 namun seragam hitam. Tidak ada title/menu.
- GPUDump summary parsial dari run [#39079279565](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079279565) (run berhenti/cancel saat workflow diperbarui) berhasil mem-parse dump sampai 136 live VSyncs tanpa truncation. Sesudah TraceBegin: `GP0 packets=0, words=0`, `GP1 packets=1, words=1`, `VSync packets=136, words=272`. Baseline pre-trace berisi 262153 GP0 words karena reset/full VRAM upload untuk merekonstruksi state dump; angka itu bukan trafik gambar game. Raw GPU dump dihapus; artifact privat hanya summary/log.
- Run konfirmasi dengan workflow saat ini [#39079291837](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079291837) sedang merekam sampai target VSync 300 saat catatan dibuat; periksa hasil finalnya sebelum menyatakan hasil penuh.

Interpretasi sementara: masalah yang terlihat tidak lagi cocok dengan kegagalan pembuatan konteks OpenGL host. Data mengarah bahwa executable tamu mencapai marker `Execute !`, tetapi belum mengeluarkan perintah gambar GP0 selama jendela yang direkam. Ini belum mengidentifikasi penyebab di CPU/game loader. RT-001 tetap **Open / blocked**: title/menu dan respons input belum terbukti; Story Mode belum dimulai.

---

## Lanjutan diagnosis VRAM dan callback UI — 2026-10-18

Run [#39050174557](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39050174557) memakai timer rekursif melalui `PCSX.nextTick()`, tetapi tidak menghasilkan checkpoint (`NO_VALID_TIMED_CAPTURES`). Audit source pada pin `0c3572c3db75f97542001e453ae80ba8c3f8acba` menjelaskan kelemahan harness: `PCSX.nextTick()` menyimpan callback di `AfterPollingCleanup`; pada `src/core/ui.cc`, `UI::tick()` menjalankan callback tersebut lalu membersihkan field yang sama. Penjadwalan ulang dari callback itu dapat tertimpa. Kegagalan ini adalah kegagalan metode sampling, bukan bukti kegagalan OpenGL.

Run [#39078592809](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078592809) mengambil sembilan sampel VRAM langsung saat `GPU::Vsync`: frame 1, 2, 3, 5, 10, 20, 30, 45, dan 60. Semua buffer berukuran 1.048.576 byte, hanya memiliki satu warna 15-bit, rasio non-black 0, dan hash PNG yang identik. Guest FPS bernilai 0 pada checkpoint itu. Namun, semua snapshot tersebut berada sebelum marker log `Execute !`; run kemudian mencatat `GPU::Vsync frame=300 guest_fps=1.0000` setelah handoff. Karena itu, sampel hitam tersebut hanya membuktikan VRAM awal yang kosong sebelum executable berjalan, bukan keadaan pasca-handoff. Run berakhir pada timeout 90 detik (124), lalu menghapus buffer mentah; artifact privat hanya berisi PNG/summary.

Capture langsung dari event GPU bukan pola yang akan diteruskan karena API readback OpenGL perlu dijalankan pada thread UI/konteks grafis yang benar. Workflow telah diubah lagi pada commit [`3a69fcef`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/3a69fcef242563ecf45de8c920bec3443db3e956) untuk menjadwalkan capture dari event ke thread UI melalui `PCSX.nextTick()`, tanpa timer rekursif. Run [#39078732160](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078732160) menguji versi deferred itu pada frame 1 dan 60; status terakhir yang diperiksa: masih berjalan, belum ada hasil yang boleh disimpulkan.

**RT-001 tetap Open / blocked.** Belum ada title/menu yang dikenali dan belum ada perubahan state akibat input yang terverifikasi. Perlu capture pasca-handoff (target VSync sekitar 300, sebagaimana marker runtime) sebelum mengubah hipotesis gameplay/rendering.

---

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

# Log analisis dan handoff

## Koreksi validitas RSP GPU-watchpoint dan rerun — 2026-10-17

Audit run [#39017636267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017636267) menemukan hasil “entry breakpoint” dan “GPU GP0 watchpoint hit” **tidak valid sebagai hit yang terkonfirmasi**: klien RSP menganggap paket konsol PCSX-Redux berawalan `O` (mis. teks `PCSX::MIPS>`) sebagai stop event. Pada run itu, PC yang dibaca setelah event tetap berada di BIOS (`0xbfc0867c` dan `0xbfc05784`), bukan di entry executable Naruto. Karena itu entry breakpoint belum terbukti tercapai dan GP0 belum boleh dinyatakan terpicu. Watchpoint GP1/DMA2 juga hanya timeout dalam uji terdahulu. Workflow berakhir `success` hanya berarti harness dan cleanup selesai; bukan hasil positif target.

Workflow diperbaiki pada commit `5055074671acf8cb2f2512182f8484dc2815552d`: parser kini mempertahankan buffer lintas paket, mengabaikan paket console `O` saat menunggu stop, serta hanya menerima jawaban stop RSP `T/S/W/X`. Sesudah entry stop, ia memeriksa PC harus tepat `0x80011448` sebelum menghapus breakpoint dan mencoba GP0/GP1/DMA2. Run [#39020901596](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39020901596) kini selesai `success` pada tingkat workflow, tetapi **tidak mencapai entry executable dalam batas 20 detik**: tidak ada stop event breakpoint dan setelah Ctrl-C PC masih `0xbfc03bdc` di BIOS. Log mengenali `SYSTEM.CNF` dan `BOOT = cdrom:\\SLPS_035.53;1`, tetapi tidak mencapai `EXEC:PC0`/`Execute !`. Ini bukan bukti hit GPU; watchpoints tidak diuji karena probe berhenti pada kegagalan entry. Run tersebut juga berbeda dari baseline karena belum menerapkan setup Port 1 Analog yang ada pada run sebelumnya. Commit `a8d8db8a0c3b84967a14c3a0905e046dbed24cf9` kini menerapkan Port 1 Analog + remap yang sama dan memperpanjang masa menunggu entry menjadi 40 detik; run baru [#39021127913](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39021127913) baru dimulai. Baca PC dan log final sebelum hipotesis lanjut.

Layar game belum berubah dari hitam dalam bukti visual sebelumnya; title/menu serta respons input belum terbukti. **RT-001 tetap Open / blocked; Story Mode belum dimulai/tamat.**

## Pembaruan eksperimen — 2026-10-17

## Hasil RSP minimal dan eksperimen GPU-watchpoint — 2026-10-17

Run [#39017271906](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017271906) selesai dengan conclusion Actions `success` dan cleanup berhasil. Klien RSP minimal terhubung ke PCSX-Redux AnyLinux pada port 3333, negosiasi `qSupported` berhasil, dan 10 sampel register PC/CP0 berhasil dibaca tanpa GDB modern yang mengirim command tak didukung. Sampel PC meliputi `0x8003C0A0` dan `0x80037320`, yang berada dalam rentang EXE utama berdasarkan header/load range `0x80010000` dengan text size `0x5D800`; sampel lain juga meliputi alamat BIOS. `BadVAddr=0` konsisten di seluruh sampel dan `Cause=0x400`; jangan tafsirkan nilai ini sebagai diagnosis exception final. Status target RSP `S00` menunjukkan target sedang running saat diperiksa. Karena sampel jarang dan bercampur alamat BIOS/EXE, ini bukan bukti cukup bahwa inisialisasi game selesai.

Jendela non-root PCSX `0x200034` (1280×800) masih uniform black (mean 0, standard deviation 0, satu warna) pada capture sebelum input, setelah Return/Cross, dan sekitar 40/65/90 detik; OCR kosong. Loader tetap mencatat `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, `EXEC:PC0(80011448)`, `Execute !`. Dengan demikian pembacaan register kini bekerja, tetapi title/menu dan respons input masih belum terbukti. Artifact diagnostik privat `12095198494` retensi 3 hari; tidak ada dump memori atau instruksi mentah di artifact.

Eksperimen pembeda berikutnya saat catatan ini diperbarui: workflow [#39017636267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017636267) memasang breakpoint entry `0x80011448` saat emulasi masih paused, lalu memantau write-watchpoint pada register GPU GP0/GP1 dan DMA2 melalui klien RSP minimal. **Run ini masih berlangsung saat catatan ini dibuat; jangan menyimpulkan hasil watchpoint sampai log selesai diperiksa.**

**RT-001 tetap Open / blocked.** Story Mode belum dimulai/tamat; jangan menetapkan aturan gameplay runtime sebelum title/menu dan input terverifikasi.

---

Tanggal ringkasan: 2026-10-15

Catatan ini merangkum pekerjaan yang sudah dijalankan dan batasannya agar sesi/agen berikutnya dapat melanjutkan tanpa mengulang asumsi.

## Pemeriksaan file

- File yang dianalisis: Naruto - Shinobi no Sato no Jintori Gassen (Japan).bin.
- Ukuran file: 325.989.552 byte.
- Format yang terdeteksi: PS1 raw sector, stride 2352 byte, 138.601 sektor.
- Payload diekstrak sementara untuk membangun ISO dan membaca filesystem; file asli tidak diubah.
- Serial disc: SLPS-03553.
- CRC32: dfe1f8b3.
- SHA-256: 58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88.
- ISO memuat DATA.BIN, DATA2.BIN, DUMMY.BIN, SLPS_035.53, SYSTEM.CNF, XASECT.BIN; ukuran lengkap tercatat di docs/ROM_STRUCTURE.md.
- SYSTEM.CNF menunjuk ke SLPS_035.53; executable utama header-memuat base 0x80010000, PC 0x80011448, text size 0x5D800.

## Analisis kode statis

- Disassembly awal mengindikasikan instruksi MIPS R3000A di executable utama dan beberapa blok DATA.BIN.
- Tidak ditemukan teks aturan kunci sebagai string Shift-JIS literal biasa di file yang diekstrak pada pencarian awal. Struktur string/resource perlu dipetakan lebih lanjut.
- Struktur pemain yang digunakan beberapa rutin memiliki empat slot, stride 0xB4 byte, field Chakra pada offset +0x18.
- Setter Chakra membatasi rentang ke -9.999 sampai 99.999.
- Target konfigurasi 3.000 ditemukan dan dipakai oleh cabang pemeriksaan target pada jalur akhir pertandingan yang ditelusuri.
- Field kepemilikan petak diperiksa sebagai bagian bitfield, dengan empat bit teratas dipakai sebagai ID owner pada jalur yang diperiksa.
- Sejumlah alamat rutin dan flag akhir permainan masih merupakan label kerja; lihat docs/OVERLAY_MAP.md.

## Sumber gameplay sekunder yang diperiksa

- Transkripsi UI Story Mode dan kartu dari proyek terjemahan fan.
- Panduan Jepang yang menguraikan unlock dan opsi Party Mode.
- Materi promosi TV Tokyo.
- Ulasan gameplay Jepang tahun 2025.
- Data identitas disc dari GameGear Archive dan PSX Data Center.

Informasi eksternal digunakan untuk membuat hipotesis tentang makna kode, bukan menggantikan bukti runtime. Biaya 60/150 yang ditunjukkan oleh contoh UI tidak dinyatakan sebagai formula universal.

## Eksekusi runtime

- Dalam sesi terdahulu, emulator PS1 tidak ditemukan pada lingkungan eksekusi lokal.
- Upaya berikutnya untuk menjalankan terminal/Python ditolak oleh lingkungan, sehingga pemetaan overlay dan tes debugger tidak dapat dilanjutkan.
- GameGear Archive punya catatan pihak ketiga bahwa dump repack CHD boot pada Mednafen PSX HW selama uji otomatis 64 detik. Penelitian ini sendiri belum melaksanakan uji terkontrol terhadap barrier, battle, kartu, atau kondisi menang.

## Arahan untuk kelanjutan

1. Otorisasi tetap: pemilik memberi ChatGPT izin berkelanjutan untuk memperbarui repo Naruto secara otomatis sesuai kebutuhan penelitian. Izin ini hanya berlaku pada repo ini; Claude ditetapkan khusus untuk Tile Duel dan tidak boleh mengakses repo Naruto.
2. Jangan mengunggah file ROM/ISO, aset game, dump memori, atau save state ke repositori.
3. Mulai dari direktori resource DATA.BIN yang kini dipetakan; selidiki format PK02/BIN0/TPK0, consumer XASECT, dan relasi DATA2.BIN.
4. Uji aturan di emulator/debugger, lalu simpan log dan hasil secara teks/screenshot yang tidak mengandung aset berhak cipta yang tidak diperlukan.
5. Pelihara label confidence dan catat semua koreksi terhadap temuan lama.
6. Jangan pernah menyentuh repo Tile Duel dalam pekerjaan penelitian ini.

## Pembaruan byte-level dan klasifikasi resource — 2026-10-15

- Mengambil kembali ROM sumber dari Library ChatGPT ke folder kerja lokal; hash lengkap cocok dengan nilai yang sudah tercatat di docs/ROM_STRUCTURE.md. Pengguna juga menyimpan salinan di laptop.
- Mengekstrak enam file filesystem ISO ke salinan kerja lokal, tanpa mengubah ROM sumber dan tanpa mengunggah ROM/ISO/aset ke GitHub.
- Memverifikasi direktori di DATA.BIN: 0x44 byte bootstrap, 0x2F00 byte tabel, 1.504 entri × 8 byte; 1.500 entri aktif dan empat entri kosong pada indeks 1491–1494.
- Memverifikasi bahwa entri aktif tidak tumpang-tindih dan seluruh interval yang dibulatkan ke sektor berada dalam extent DATA.BIN. Total cakupan direktori 32.227 dari 32.234 sektor.
- Klasifikasi signature: PK02 921, TIM valid 246 (29 4-bit; 217 8-bit), NARUTOSceneV001 126, NARU lainnya 125, PSQ0 enam, PSQ1 dua, TXT2 satu, belum terklasifikasi 73.
- Pemeriksaan XASECT.BIN menemukan 86 pasangan 32-bit. Consumer di sekitar 0x80019468 menghitung indeks input >> 4, mengindeks pasangan dengan stride 8, lalu menggunakan field pertama sebagai offset aditif. Makna penuh field masih belum ditentukan.
- Semua analisis tersebut statis. Belum ada pengujian gameplay dengan debugger/emulator dan belum ada formula barrier, pendapatan, battle, atau efek kartu yang dinaikkan statusnya menjadi terkonfirmasi runtime.
- Detail lengkap: docs/RESOURCE_CATALOG.md dan HANDOFF_LANJUT.md.


## Arsip file ekstraksi di Library — 2026-10-15

- Menyimpan `DATA.BIN`, `DUMMY.BIN`, `SLPS_035.53`, `SYSTEM.CNF`, dan `XASECT.BIN` di Library pada folder `Naruto Research Files`.
- `DATA2.BIN` mentah gagal disimpan karena batas kapasitas Library; mengompresnya menjadi ZIP sekitar 42 MiB dan berhasil menyimpan `DATA2.BIN.zip`.
- File game tidak ditambahkan ke GitHub. Jangan menghapus item Library lain tanpa izin. Detail pemulihan ada di `HANDOFF_LANJUT.md`.
- Fokus riset selanjutnya tetap mencari aturan gameplay yang pasti: trace jalur transaksi Chakra, barrier/upgrade, income, battle, dan victory flags; bongkar format resource hanya bila jalur kode terbukti bergantung padanya.


## Pembaruan penelusuran aturan gameplay dan aturan sumber data — 2026-10-15

### Sumber file dan batas kuota

- Melanjutkan analisis dari file hasil ekstraksi yang sudah berada di Library; tidak membutuhkan dan tidak meminta upload ulang ROM 300 MB dari laptop.
- Hash SHA-256 yang cocok dengan catatan terdahulu: SLPS_035.53 = a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569; DATA.BIN = 69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822; XASECT.BIN = df257fbdabdb848f845466246abf4a36fdb6cf17815fc3a76ff7d7585d1953f0; DATA2.BIN hasil unzip = be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9. ZIP DATA2.BIN.zip = 67e7a372c6d02379d8cc715d15f3521c0914b8f17ee6e2f66a2bc32695367668.

### Jejak konfigurasi target Chakra

- Dalam executable utama, tabel 0x80057798 (file offset 0x47F98) menggunakan stride 0x54. Record yang diperiksa memuat (ID mentah, +0x04, +0x08, +0x0C): (0xA00,1500,3000,400), (0x10B01,2000,4000,400), (0x20C02,2000,4000,400), (0x81210,600,0,0), (0x31403,2500,5000,400), (0x40E04,2500,5000,400), (0x81211,600,0,0), (0x50F0F,2500,5000,400), (0x61106,3000,6000,400), (0x60809,3000,6000,400).
- Field +0x04 disalin ke global 0x80070C80 dan jalur inisialisasi meneruskannya ke setter Chakra; confidence tinggi bahwa ini nilai awal. Field +0x08 masuk lewat getter 0x80012A70 dan dipakai sebagai target pada cabang hasil dengan kondisi yang mencakup bit 0x200. Confidence tinggi untuk peran target, menengah–tinggi untuk pemetaan modul gameplay karena loader belum dipastikan runtime.
- Tabel kedua di 0x80064918 (file offset 0x55118, stride 0x30) menunjukkan nilai 1500/3000 pada sekurangnya 13 record awal nonnol yang diperiksa.
- Arti field +0x0C (400 atau 0) serta mapping raw ID ke nama stage/mode belum diketahui. Target 0 pada sebuah record tidak boleh diperlakukan sebagai kemenangan otomatis.
- Sumber terjemahan Story Act 01 menyebut target 3000; ini cocok dengan satu record, tetapi mapping ID satu-ke-satu belum terbukti.

### Peta kode dan koreksi

- DATA.BIN entry index 1 berada pada file offset 0x10BB000 dan berukuran 596.412 byte. Pemetaan sementara ke base RAM 0x800D0000 menghasilkan referensi internal konsisten, tetapi belum dikonfirmasi lewat breakpoint loader.
- Dalam peta statis tersebut, cabang sekitar 0x80111228, 0x801112CC, 0x801113B4, 0x801114F0, 0x80111588 dan 0x80112418 memeriksa kondisi target dan Chakra pemain sebelum mengubah pemenang/state hasil.
- Label terdahulu bahwa 0x800EC200 adalah pembanding target dan sekitar 0x800F70D0 aritmetika Chakra ditarik kembali karena identitas/base modul belum dibuktikan.
- Setter Chakra 0x8001387C menjepit ke [-9999, 99999]; nilai Chakra ada di +0x18 dalam struktur empat slot dengan stride 0xB4.

### Yang belum terkonfirmasi dan tugas berikutnya

- Belum ditemukan formula universal biaya barrier/upgrade, income, damage/durability battle, roulette, atau semua efek kartu. Angka UI 60 dan 150 bukan formula universal terkonfirmasi.
- Prioritas berikutnya adalah menelusuri call chain event ESTATE dan LVUP_ESTATE, transaksi Chakra, pendapatan, dan perubahan kepemilikan. Pemanggil setter yang perlu dipilah berdasarkan konteks termasuk 0x800D6D60, 0x800D6E04, 0x800D7AB0, 0x800D7B14, 0x800D8DE8, 0x801016E8, 0x80104790, 0x8010F554, 0x8012CD0C, 0x8012CD60, dan 0x8012D1E8; lokasi pemanggil saja tidak menetapkan makna transaksi.
- Tidak ada tes runtime debugger/emulator yang selesai. Semua klaim di atas tetap analisis statis.


## Penelusuran Chakra: setter, delta event, dan batas inferensi — 2026-10-15

- Pemeriksaan callsite `jal 0x1387C` pada resource yang sementara dipetakan ke `0x800D0000` menunjukkan beberapa panggilan hanya menyalin field Chakra yang sudah ada dari record runtime ke setter pemain aktif. Daftar itu mencakup `0x800D6D60`, `0x800D6E04`, `0x800D7AB0`, `0x800D7B14`, `0x800D8DE8`, `0x801016E8`; jadi daftar pemanggil setter tidak bisa dipakai sebagai daftar transaksi biaya.
- State machine sekitar `0x8012C600` mereset `+0xB44`, lalu membentuk `+0xB40 = +0xB30 + +0xB38`. Dalam state 7 (`+0xB2A == 7`), jalur `0x8012CD04–0x8012CD74` menggunakan `+0xB44` sebagai jumlah pending yang diterapkan bertahap ke Chakra pemain `+0xB2B` melalui getter/setter; pending dikurangi saat diproses dan field dibersihkan setelah selesai. Ini mekanisme perubahan Chakra bertahap, bukan bukti bahwa field itu khusus biaya barrier. Penulis `+0xB30/+0xB38` dan identitas aksi tetap belum ditemukan.
- Jalur di sekitar `0x8011C0D0` mempunyai cabang yang membalik tanda field nilai pemain dan menjepit nilai negatif terendah ke `-9999`, lalu memanggil setter Chakra. Pemicu dan identitas aturan belum dipastikan, sehingga belum diberi label sebagai efek kartu atau kondisi kekalahan.
- Jalur target kemenangan diperiksa lagi di `0x80111200–0x80111280`: getter kondisi menghasilkan bitmask; jika `bit 0x200` aktif, kode memanggil getter target `0x80012A70`, membaca nilai Chakra pemain dari field awal record pemain pada indeks yang dipilih, dan membandingkannya dengan target. `slt(current,target)` membuat jalur non-menang ketika `current < target`; ketika `current >= target`, kode menulis indeks pemain ke field pemenang dan mengubah state hasil. Confidence tinggi untuk arti perbandingan di dalam disassembly, tetapi identitas base modul tetap hasil pemetaan statis sementara.
- Tidak ada uji runtime dijalankan. Tidak ditemukan cukup bukti untuk mengklaim 60 Chakra sebagai harga semua barrier atau 150 Chakra sebagai harga semua upgrade. Prioritas berikutnya: telusuri penulis `+0xB44`, pemanggil event `ESTATE`/`LVUP_ESTATE`, pemeriksaan saldo, dan penulisan data petak untuk menghubungkan angka UI ke rumus/parameter.


## Keputusan emulator-first dan pemeriksaan environment — 2026-10-15

- Menetapkan penggunaan emulator/debugger sebagai jalur riset utama kedua setelah analisis statis. Sasaran: amati perubahan Chakra, field tile, event/state, damage, kepemilikan, dan kondisi pemenang secara langsung, lalu cocokkan dengan call chain.
- PCSX-Redux dipilih sebagai opsi utama karena ada dokumentasi resmi untuk debugger CPU, breakpoint memori, GDB server/watchpoints, command line load image, dan Lua breakpoint. Mednafen adalah alternatif dengan debugger PSX dasar serta breakpoint baca/tulis.
- Sumber rujukan: https://github.com/grumpycoders/pcsx-redux ; https://pcsx-redux.consoledev.net/Debugging/introduction/ ; https://pcsx-redux.consoledev.net/Debugging/gdb-server/ ; https://pcsx-redux.consoledev.net/cli_flags/ ; https://mednafen.github.io/documentation/debugger.html .
- File ROM diambil dari Library, bukan upload ulang laptop; SHA-256 diverifikasi ulang dan cocok: `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`. CUE eksperimen mengidentifikasi satu track MODE2/2352 sesuai mode byte sektor pertama. ROM asli tidak diubah.
- Kendala sesi 2026-10-15: tidak ada executable PS1 emulator yang ditemukan pada path runtime; DNS jaringan container gagal sehingga binary tidak dapat dipasang di sesi ini. Oleh sebab itu tidak ada game boot atau eksperimen runtime yang berhasil dilakukan. Catatan ini mencegah klaim palsu bahwa pengujian sudah berjalan.
- Protokol dan daftar eksperimen baru: [docs/EMULATOR_WORKFLOW.md](docs/EMULATOR_WORKFLOW.md), [docs/RUNTIME_TEST_PLAN.md](docs/RUNTIME_TEST_PLAN.md). Fokus uji awal: breakpoint executable utama di setter/getter Chakra; kemudian telusuri cost/ESTATE, LVUP_ESTATE, income, battle, dan target kemenangan setelah base overlay dikonfirmasi.


## Pemasangan PCSX-Redux dan uji launcher — 2026-10-15

- PCSX-Redux dipaketkan ke Naruto repo melalui workflow `.github/workflows/publish-pcsx-redux.yml` sebagai Release asset, bukan Git object. Release: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15. Ukuran asset 65.747.557 byte; SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`, cocok dengan digest yang diterbitkan package source.
- GitHub Actions run 38692549397 sukses: unduh, validasi hash dan size, best-effort launch smoke test via Xvfb, workflow artifact (retention 90 hari) dan release assets terunggah.
- AppImage dijalankan di environment melalui Xvfb. GUI memang muncul dan teridentifikasi game serial SLPS03553 pada daftar/halaman emulator, tetapi memunculkan dialog “No BIOS loaded, emulation halted”. Tidak ada boot game, tidak ada input gameplay atau runtime game state yang diamati.
- Untuk tahap berikutnya, workflow `.github/workflows/build-openbios.yml` membangun OpenBIOS open-source dari repository upstream PCSX-Redux pinned full source commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`. Workflow awal gagal karena ref commit singkat tidak diterima checkout action; pinned source diperbaiki menjadi full SHA. Run perbaikan #38693323975 harus diverifikasi. OpenBIOS adalah BIOS replacement open-source, bukan Sony retail BIOS.
- ROM didapat dari Library dengan SHA-256 yang cocok, tanpa meminta upload ulang dari laptop. Binary emulator tetap sebagai Release asset terpisah untuk menjaga Git history kecil.


## Uji PCSX-Redux dengan OpenBIOS — 2026-10-15

- OpenBIOS berhasil dikompilasi pada GitHub Actions run `38693358323` dari source PCSX-Redux pinned commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`; workflow merilis asset `openbios.bin`, `openbios.elf`, dan checksum/source provenance.
- Varian default `openbios.bin` berukuran 524.288 byte, SHA-256 `713ea2aed58606282b3ff5e91d77f8c5892ea36f5adcd279d2c7dd26604a625d`. Varian ELF debug SHA-256 `d0d4cc73c9546e1e6af86d38ec894f5a6c81090ccdf97b1a3a39885c56af7bfc`. Keduanya cocok dengan `OPENBIOS-SHA256SUMS` pada artifact yang diunduh dan diverifikasi.
- Launch PCSX-Redux menggunakan `-bios openbios.bin -interpreter -debugger -iso game.cue -run` tidak lagi menampilkan “No BIOS loaded”, tetapi frame yang terekam menunjukkan bentuk geometris besar/gelap dan tidak memberi bukti yang cukup bahwa game mencapai menu/title. Jangan tandai boot game berhasil.
- Workflow run `38693918169` sedang menyiapkan dua variant OpenBIOS: normal shell/menu dan `BOOT_MODE=fast` agar CD boot dicoba langsung. Setelah selesai, ambil asset via release atau GitHub Actions artifact, validasi checksum, lalu ulangi tes boot.
- AppImage emulator tetap sebagai Release asset terpisah dengan hash `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`. Repo tidak menyimpan ROM atau BIOS retail.


## OpenBIOS fast-CD boot attempt — 2026-10-15

- Build workflow [#38693918169](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693918169) sukses membuat shell/menu dan fast boot variants. `openbios.bin` adalah `BOOT_MODE=fast`, yang melewati shell dan mencoba boot disc.
- Hash fast boot `openbios.bin`: `25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d`; ELF: `2c8d36e2179841935a1d1331777380502cdb22528d086c99c6388cdcfa54b8aa`. Checksum dari artifact cocok untuk kedua berkas fastboot; release berisi juga varian shell/menu.
- Pengujian lokal dengan AppImage, fastboot OpenBIOS, interpreter/debugger dan CUE disc dilakukan sekitar 12 detik. BIOS-missing dialog tidak muncul, tetapi layar tetap hitam; tidak ada title atau menu yang bisa dipastikan. Ini **belum merupakan boot game yang terverifikasi**.
- Next: periksa CUE/raw-sector layout dan log/PC state; uji CD-ROM boot dengan debug step atau media header yang dikenal sebagai kontrol. Jangan unggah ROM ke repo, jangan meminta pengguna mengirim ulang ROM, dan jangan klaim rule gameplay runtime sampai ada bukti langsung.

## Diagnostik runtime lanjutan: sektor, init kartu memori, dan pad — 2026-10-16

### Pembacaan payload EXE
- Boot CD normal berhasil membaca file konfigurasi, tetapi `loadExe` tersangkut saat membaca payload utama `SLPS_035.53`. Payload sepanjang `0x5D800` byte = 382.976 byte = 187 sektor.
- Percobaan loop 32 sektor dan 8 sektor tidak menyelesaikan masalah. Varian 8 sektor hanya menghasilkan `[CHUNK8] before idx=0 ... bytes=16384` tanpa `after`, sehingga permintaan 16 KB tidak selesai dalam jendela pengamatan.
- Varian diagnostik satu sektor dibangun/diterbitkan dalam [Actions #38697240018](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38697240018). Runtime menunjukkan read 2.048 byte mulai berjalan dan ada progres setidaknya sampai sekitar sektor kesembilan dalam pengamatan singkat, tetapi belum ada bukti full payload read atau entry game pada jalur disc normal.

### Jalur manual/injeksi EXE
- Injeksi payload ke alamat yang ditetapkan header membuat debugger mencapai `EXEC:PC0(80011448)`, `Execute !`, dan `CD_init`; layar tetap hitam. Pastikan `flushCache` dan urutan init CD-ROM benar sebelum mengulang.
- Breakpoint berikutnya menunjukkan startup menunggu dalam inisialisasi kartu memori (`buInit`) karena status kartu tidak berubah. Bypass eksperimental dapat melewati penantian, tetapi belum menghasilkan layar title/menu; jangan menyebutnya boot berhasil.

### Petunjuk protokol kontroler
- Log berulang menunjukkan perintah pad `0x43` (Set Config Mode). Source PCSX-Redux upstream mengidentifikasi command ini di jalur DualShock/analog; bila tipe controller emulator Digital, kode log menampilkan `Unknown command for pad: 43`. Sumber: https://github.com/grumpycoders/pcsx-redux/blob/db9bc8af44e3c77424127b573c17f9583ee2ab95/src/core/pad.cc.
- Hipotesis selanjutnya: ganti Port 1 ke Analog/DualShock dan ulangi boot sebelum melakukan patch game. Belum ada hasil uji setelah perubahan tipe pad, jadi kausalitas belum terbukti.

### Build alternatif yang diunggah pengguna
- File `PCSX-Redux-9c6f98a0-linux-x86_64.zip`, ukuran 90.912.361 byte, disediakan pengguna pada 2026-10-16. Lingkungan eksekusi shell/file gagal saat inspeksi, sehingga isi paket, hash dan kelayakan menjalankan ROM belum diverifikasi. Lakukan verifikasi terlebih dahulu; jangan menaruh file biner besar ke Git history atau release tanpa alasan yang teruji.

### Syarat bukti
- Status sekarang: *executable mulai berjalan dalam jalur manual*, bukan game terkonfirmasi boot. Bukti yang dibutuhkan: log entry yang valid, title/menu yang dikenali, dan input responsif. Sesudah itu baru validasi aturan gameplay dengan state awal terkontrol.


## Percobaan setelah ZIP emulator tersimpan di Library — 2026-10-16

- Melalui Files berhasil mematerialisasi ZIP emulator (90.912.361 byte), ROM sumber (325.989.552 byte), dan CUE (113 byte) ke `/mnt/data/naruto-runtime/`.
- Pemeriksaan lokal gagal sebelum program dijalankan: `container.exec` memberikan `ClientError` untuk listing/file checks dan bahkan `echo runtime-check`; Python di lingkungan analisis dan jalur Python alternatif juga gagal dengan `ClientError`.
- Akibatnya, belum ada daftar isi ZIP, hash ZIP, hasil ekstraksi, versi PCSX-Redux, log run, atau bukti boot baru. Jangan mengartikan kegagalan tool sebagai kerusakan ZIP atau kegagalan emulator. Tidak ada tes runtime baru yang berhasil dilakukan.
- Tindakan saat runtime pulih: verifikasi integritas dan isi ZIP, ekstrak binary ke direktori sementara, cek versi/dependensi, lalu ulangi boot ROM dengan OpenBIOS dan Port 1 Analog/DualShock sebagai hipotesis terpisah. Sukses harus dibuktikan dengan layar title/menu Naruto dan respons input.


## Refinement of controller `0x43` diagnostic hypothesis — 2026-10-16

The exact upstream PCSX-Redux source commit used for the research-kit AppImage was inspected: [`src/core/pad.cc` at `0c3572c3db75f97542001e453ae80ba8c3f8acba`](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/pad.cc).

- `PadType` defines `Digital = 0` and `Analog = 1`. The serialized setting is named `DeviceType`, with `Digital` as its default.
- When the first received command byte is not the normal read command `0x42`, the pad dispatches the DualShock command handler only when `m_type == PadType::Analog`. Otherwise it logs `Unknown command for pad: %02X`. Thus the existing `Unknown command for pad: 43` log is consistent with Port 1 being configured as a Digital controller.
- Important distinction: the Lua method `setAnalogMode(bool)` writes `m_analogMode`; it does **not** change `m_type` or the serialized `DeviceType` controller type. Calling that Lua method alone is not a valid test of the current hypothesis.
- The GUI's `Controller Type` selector updates `SettingDeviceType` and resets/remaps the pad. The next controlled experiment should set Port 1 `Controller Type` to `Analog` through **Configuration → Controls**, confirm that the pad is connected, then repeat the same CD-boot attempt with all other variables unchanged.
- Compare logs before and after. If the `Unknown command for pad: 43` messages disappear, record that protocol-level effect; if the game still hangs or remains black, the controller mismatch was not a sufficient explanation for the boot failure. Do not infer game boot from that log change alone.

Evidence class: static inspection of the emulator source. **This is not yet a runtime result**: this session could not run the emulator because local execution/file tools returned `ClientError`. The contents and hash of the user-provided alternate ZIP remain unverified.

## OpenBIOS source-level CD-read stall hypothesis — 2026-10-16

### Source trace

Pinned source chain:
- PCSX-Redux AppImage root commit: https://github.com/grumpycoders/pcsx-redux/commit/0c3572c3db75f97542001e453ae80ba8c3f8acba, dated 2026-10-01.
- Its src/mips submodule points to OpenBIOS/Nugget commit https://github.com/pcsx-redux/nugget/commit/d93840921b5ad7ed515e95b0e414f1b1e2038b1a.

Relevant source:
- openbios/kernel/psxexe.c: loadExe() reads the 2,048-byte header, then calls syscall_read(fd, text_addr, text_size) once; it does not check the result count before closing and flushing cache.
- openbios/cdrom/filesystem.c: dev_cd_read() rejects a size or offset not aligned to 0x800 bytes and converts the request into 2,048-byte sectors before calling cdromBlockReading().
- openbios/cdrom/helpers.c: cdromBlockReading() polls seek/read startup with bounded cycle counters, but after starting a read it waits for the DNE completion event while checking error/end events; that final wait has no overall timeout. If completion is never delivered, it may wait indefinitely.

The known executable payload is 0x5D800 = 382,976 bytes = 187 sectors; its request size and file offset satisfy the 0x800 alignment guard. The normal-path stall during payload loading is consistent with a CD-ROM read/event completion issue because the log previously showed SYSTEM.CNF read but not EXEC:PC0(80011448). This remains a root-cause hypothesis until a reproducible runtime trace identifies the exact event/state.

### Controller configuration refined

PCSX-Redux source declares PadType::Digital=0 and PadType::Analog=1 and serializes the emulated console pad protocol to DeviceType (default Digital). Upstream tests/core/pad-config.cc confirms DeviceType: 1 means Analog; PadType: 2 is the keyboard host-input source. These settings are distinct. Toggling the keyboard Analog mode binding or Lua setAnalogMode(true) is not equivalent to setting DeviceType.

- Source used by release: https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/pad.cc
- Upstream config fixture: https://github.com/grumpycoders/pcsx-redux/blob/e7ced7b681296ace22f7847f7bb3c9a206315571/tests/core/pad-config.cc

### Emulator package comparison

The user-provided filename PCSX-Redux-9c6f98a0-linux-x86_64.zip maps by its prefix to upstream root commit https://github.com/grumpycoders/pcsx-redux/commit/9c6f98a0ed0581635f9123147e382c248e0f5ddc, a merge dated 2026-09-28. The research AppImage is pinned to a later root commit dated 2026-10-01. Since ZIP contents could not be inspected in this session, do not claim the uploaded archive actually contains that exact build; the filename is evidence only.

### Next controlled runtime test

1. When shell runtime is available, inspect the ZIP without executing it: unzip -t, list files, SHA-256, architecture and dependencies. Prefer the pinned research AppImage if the ZIP offers no newer/testable functionality.
2. Run a clean isolated test with explicit paths: -bios openbios-chunked.bin -iso naruto-shinobi-jintori.cue -run -interpreter -debugger -stdout -lua_stdout -logfile boot-analog.log.
3. Set Port 1 protocol to Analog (DeviceType: 1), host input to keyboard (PadType: 2), and Connected=true. Compare Unknown command for pad: 43 logs; independently verify the title/menu and input response.
4. The executable payload is 187 sectors. Use a longer observation window and log every per-sector read. Determine whether progress completes, stops at a reproducible sector, or waits on a specific CD event. Early progress is not a completed read.
5. Only start gameplay tests after the title/menu is visible and controls respond. No new runtime test occurred in this session because shell and Python tools returned ClientError; this is an environment blocker, not proof that the ZIP is corrupt or that the game cannot run.


## PCSX-Redux ZIP extraction record — 2026-10-16

### Archive validation and extraction

- Materialized the user Library file `PCSX-Redux-9c6f98a0-linux-x86_64.zip` (90,912,361 bytes) to the working container.
- Source ZIP SHA-256: `7e4c9378524ebfa35068944ba4aa9e3ebf7462678bcae33b3e7ae7c57dd99849`.
- `unzip -t` passed with no errors; archive contained exactly one entry: `PCSX-Redux-HEAD-x86_64.AppImage`, 91,474,424 bytes.
- Extracted AppImage SHA-256: `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`. A second materialization from Library compared byte-identical with the extracted local file.
- Embedded `usr/share/pcsx-redux/resources/version.json`: version `9c6f98a0`, build ID 335, changeset `9c6f98a0ed0581635f9123147e382c248e0f5ddc`, build timestamp 2026-09-28 19:56:29 UTC, channel `dev`.
- The extracted AppImage runtime responded to `--appimage-version`, and the embedded squashfs filesystem could be extracted without FUSE. Running the inner emulator failed due requirements `GLIBC_2.42` and `GLIBC_2.43`; this host provides glibc 2.41. Direct AppImage mounting also failed because no suitable `fusermount`/FUSE device is available.
- The source ZIP was replaced in Library by the AppImage output to avoid storing two nearly identical large files at Library quota. The source hash is recorded here. The Library item retains stale ZIP MIME metadata despite the new AppImage bytes.
- Persistent Library manifest: `/Naruto Research Files/PCSX-Redux-EXTRACTION-MANIFEST.md`.
- New Git documentation records details in `docs/PCSX_REDUX_PACKAGE.md`. The actual 91 MB binary was not added to Git history because the current GitHub connector has no binary Release-asset upload action; a distinct 65,747,557-byte AppImage already exists on the research Release (SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`).
- This work verifies the ZIP and extracted AppImage only. It is **not** a runtime verification of Naruto boot, controls, Story Mode, or the ROM's validity.


## Preferred build for GLIBC 2.41 host — 2026-10-16

### Candidate and compatibility evidence

The best candidate located for the glibc 2.41 research host is the x86_64 `AnyLinux` AppImage built from source changeset `0c3572c3db75f97542001e453ae80ba8c3f8acba` on 2026-10-01. It is attached to the research release and the public packager's release. Size 65,747,557 bytes; SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`.

Sources:
- [Packager README](https://github.com/pkgforge-dev/PCSX-Redux-AppImage-Enhanced): states that AnyLinux AppImage bundles dependencies for old/musl Linux distributions and does not require FUSE.
- [x86_64 GitHub Actions run](https://github.com/pkgforge-dev/PCSX-Redux-AppImage-Enhanced/actions/runs/36872881656), 2026-10-01: successful; the log explicitly says `quick-sharun --simple-test` returned “Test went OK.” The packager embeds cross-libc-dlopen and uruntime.
- The repo's earlier smoke-test notes reported GUI launch under Xvfb with a “no BIOS configured” message. This was not a game boot test.

This is a stronger candidate than the Library's `9c6f98a0` AppImage whose inner binary needs GLIBC_2.42/2.43. However, generic smoke tests and portable packaging do not establish game compatibility or stability. In this turn, container.exec and Python returned ServerError even for basic sanity commands, so no fresh test against the Naruto BIN/CUE was performed. Do not claim title/menu, input, stable gameplay, or Story Mode completion.

Next test when runtime access recovers: obtain the exact candidate by release, verify its SHA; use OpenBIOS chunked with CUE, a clean profile, logs, Port 1 `DeviceType: 1` plus keyboard `PadType: 2`, and connected=true. Confirm title/menu and responsive input, then examine the 187-sector EXE read, repeat boot tests, and only afterwards begin Story Mode.


## Current Library package — AnyLinux artifact ZIP (2026-10-16)

The candidate AnyLinux artifact ZIP was downloaded from the packager's GitHub Actions artifact ID 11170447493 and saved in Library as `/Naruto Research Files/PCSX-Redux-0c3572c3d-anylinux-x86_64-artifact.zip`. Actions-reported ZIP digest: `f6c27070b565cbc0554f1093c1374a16aee2b8635c72ef7b141f9ff7bd857ed0`; reported size 65,673,524 bytes. Its standalone AppImage SHA-256 is known from Release metadata: `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`. This is the preferred candidate for glibc 2.41. The previous 91 MB `9c6f98a0` AppImage and its stale Library manifest were replaced/removed; their hashes remain recorded in `docs/PCSX_REDUX_PACKAGE.md`.

The Actions log confirms a generic `quick-sharun --simple-test` passed. That does not test the ROM. No full Naruto boot, input, runtime stability, or Story Mode result is available. Attempts to run simple local commands now return ServerError, so do not claim an end-to-end test was performed.


## Controlled Analog-port boot probe configured — 2026-10-17

### What changed

- Runner workflow commit: [6bd261a0599f192579f8c091ddcb6d28a4042ec7](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/6bd261a0599f192579f8c091ddcb6d28a4042ec7).
- The workflow now passes a Lua setup to each emulator build before execution:

  ```lua
  PCSX.settings.pads[1].DeviceType = 'Analog'
  PCSX.settings.pads[1].Connected = true
  PCSX.SIO0.slots[1].pads[1].map()
  print("PAD_SETUP=port1 analog device connected and remapped")
  ```

- This matches the upstream PCSX-Redux test fixture at [tests/pcsxrunner/rumble.cc](https://github.com/grumpycoders/pcsx-redux/blob/6b9df482d7b77b9ae218d9c48c1ce1a43c265206/tests/pcsxrunner/rumble.cc). Its comment says safe mode starts Port 1 digital and that the controller type is cached at map() time.
- The A/B workflow continues to use the exact same verified ROM SHA-256 `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`, the same temporary normalized CUE, OpenBIOS, interpreter and 90-second limit for both the AnyLinux and upstream HEAD builds. It now includes the Lua setup marker in the selected logs.

### How to interpret the pending log

- A visible `PAD_SETUP=port1 analog device connected and remapped` marker is needed to confirm the Lua setup ran.
- Compare the presence of `Unknown command for pad: 43` against the baseline from Actions run [#38971848277](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38971848277), where both builds emitted the warning.
- Even if the warning disappears, it proves only that the emulator now accepts the configuration command. It does **not** prove the title/menu is rendered or that input works in the game.
- The resulting run log has not yet been captured into this research log. Do not infer success merely from the workflow commit or a passing CI job.

### Next diagnostic gate

First retrieve the run output and confirm the Lua marker and `0x43` result. If the warning is gone but the frame remains black, treat controller configuration as a solved protocol mismatch but **not** a sufficient explanation for the boot/rendering failure. Then run a separate GUI-under-Xvfb test with the same ROM and Analog-port setup, capture the emulator window locally on the ephemeral runner, and report only derived pixel/screen metrics (do not upload ROM, BIOS, EXE, save-state, RAM dump, or game screenshots to the repository). Confirm title/menu recognition and input response before starting gameplay-rule tests.


## Workflow YAML correction — 2026-10-17

- The initial Analog-port workflow edit [6bd261a](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/6bd261a0599f192579f8c091ddcb6d28a4042ec7) accidentally left the Lua heredoc body without YAML block indentation. Do not treat that revision as a valid completed test.
- The indentation was corrected in final workflow commit [0439c1b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/0439c1bbf51d3c1be234150d6bee80c5b812ff1e). The current file was re-fetched and visually checked: heredoc contents and its closing LUA delimiter are now indented at the YAML run-block level, which YAML removes before the shell executes the script.
- No runtime claim is made from these edits. The next evidence must still come from logs of a run using the corrected commit, including the PAD_SETUP marker and presence/absence of the pad 0x43 warning.


## Runtime result: Port 1 Analog probe — 2026-10-17

Runner test [#38973267415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973267415), job `boot-private-rom`, completed successfully using corrected workflow commit `0439c1bbf51d3c1be234150d6bee80c5b812ff1e`.

- Both AnyLinux and upstream HEAD recorded `PAD_SETUP=port1 analog device connected and remapped`, then loaded OpenBIOS, recognized `SLPS-03553`, completed `[CHUNK1] done chunks=187`, and reached `EXEC:PC0(80011448)` / `Execute !`.
- Unlike the baseline [#38971848277](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38971848277), neither build logged `Unknown command for pad: 43` after the explicit Analog DeviceType + Connected + remap setup. Each build was stopped at the 90-second cap (`PROCESS_EXIT=124`) rather than crashing.
- Conclusion: **confirmed emulator protocol-level effect** — configuring Port 1 as Analog removes the observed `0x43` warning while preserving the executable-entry marker. This does not establish that the game title/menu rendered or that buttons worked in-game. The controller setup warning is now separated from the still-open black-screen/boot/rendering problem.

## GUI rendering probe added — 2026-10-17

- Current runner workflow commit: [85c08d9](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85c08d9ea255dc400c0771361abc95817a0a7ba6). New Actions run [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) was observed queued immediately after commit; its final outcome has not yet been recorded here.
- After the same A/B headless run, the workflow launches AnyLinux in a separate Xvfb GUI session with the same verified ROM, temporary CUE, OpenBIOS and Analog setup. It captures frames at 10s and 20s, prints only image size/mean/stddev/color-count and short Japanese/English OCR output, and logs boot/controller markers. Temporary frames and GUI logs are added to the cleanup list, not uploaded as artifacts.
- GUI result must be checked separately. Non-black pixels or OCR text alone are suggestive only; accept boot only if the frame/text supports Naruto title/menu recognition and a later controlled input probe demonstrates response. If still blank, pursue CD event/init and GPU/rendering causes separately.


## GUI probe result and next trace — 2026-10-17

Runner [Actions #38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) completed successfully, including cleanup. The GUI probe ran AnyLinux with the same verified ROM, temporary normalized CUE, OpenBIOS and Analog Port 1 setup under Xvfb. Two desktop captures at 10s and 20s both reported `1280x800`, `mean=0`, `stddev=0`, `colors=1`, and empty Japanese/English OCR output. This confirms the **captured desktop was entirely black** at both times. The selected GUI log lines included BIOS/Disc/PAD_SETUP but did not include `EXEC:PC0` or `Execute !` within the 35-second GUI observation window; headless tests still reached those markers. No screenshot/artifact was uploaded; frames and logs were deleted by cleanup.

Next experiment: a separate lean workflow [naruto-cpu-trace.yml](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/blob/main/.github/workflows/naruto-cpu-trace.yml) adds a listener for the upstream-tested `GPU::Vsync` event and prints the guest PC/RA/SP every 30 frames, up to 600 frames, using the same private ROM with explicit Analog Port 1. Current run [#38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045) was `in_progress` immediately after commit; obtain its final log and interpret it cautiously. If no VSync callbacks occur, distinguish a stalled emulation/hardware timing path from a CPU loop; if PCs are recorded, map recurring addresses against the executable/temporary overlay assumptions. Do not claim rendered title/menu until independently proven.


## CPU trace attempt 1 — inconclusive — 2026-10-17

The runner job [Actions #38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045) exited with code 139 (segmentation fault) about 12 seconds after starting the headless emulator. It had read the disc label and `SYSTEM.CNF`/`BOOT`, but no `PC_TRACE` sample or executable-entry marker was captured. The instrumented build added a Lua VSync listener that removed itself inside its callback at frame 600, so instrumentation is a confounder. This result does not prove the ROM is invalid or that the game code itself crashed.

A retry was committed as [9419800](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/941980021c16dee3e779f6cc1066dad70b187ad4). It combines the pad setup and tracing code into a single `-exec` block and leaves the VSync listener installed until timeout. Check [Actions #38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739) and require real `PC_TRACE frame=...` rows before interpreting any PC values. If that retry fails, simplify to a counter-only VSync callback before reading registers.


### CPU trace attempt 2: failure was Lua script construction — 2026-10-17

Run [#38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739) exited 134. The exact stdout reason is `[string "cmdline:"]:4: unexpected symbol near '\\'`, followed by `Error loading lua string` and `terminate called without an active exception`. This was caused by shell concatenation `printf '%s\\n%s'` embedding a literal backslash-n between the two Lua chunks instead of a line break. The Lua parser rejected the instrumentation before any PC sample; this is not a ROM failure.

Corrected runner workflow commit: [7b8ce73](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/7b8ce731378e0115f616b7ff78874f5d17375e80). It now constructs pad configuration and VSync tracing in a single heredoc, so source lines are separated normally; the listener stays installed through the timeout. Current retry: [Actions #38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869). Check final job logs for `PAD_SETUP`, `PC_TRACE=listener installed`, and actual `PC_TRACE frame=` lines. If Lua parses but segfaults, strip down to a simple VSync counter callback before any register read.


### CPU trace attempt 3 — VSync samples recorded; process later segfaulted — 2026-10-17

Runner [Actions #38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869) ran the corrected single-heredoc Lua script. It printed `PAD_SETUP` and `PC_TRACE=listener installed`, then produced `PC_TRACE frame=` rows from frame 30 through at least frame 780. Sampled PCs frequently included BIOS addresses `BFC0574C`, `BFC05784`, `BFC03C6C`, plus occasional `000000B0` and `00002998`; RA/SP were also captured. The separate emulator logfile recorded `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, and `Execute !`. The process nevertheless ended with `TRACE_PROCESS_EXIT=139` (segmentation fault) before the 35-second cap and the last output row was incomplete. Because the instrumentation reads `PCSX.getRegisters()` inside the VSync callback, that access/formatting is still a possible confounder; do not infer that the game itself caused the fault or that the PC samples prove a stable gameplay loop.

Next isolating run: [Actions #38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602), workflow commit [85d3e4f](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85d3e4ff31732b7788d67e447ea9df136dcb84f5), uses a counter-only `GPU::Vsync` listener with no CPU-register reads and no self-removal. If it survives until timeout and reports increasing VSync counters, callback plumbing is sound and the register read/format path is implicated. If it still crashes, isolate event registration/callback itself or leave Lua tracing aside and use built-in debugger/logs.


### Counter-only trace result — 2026-10-17

Run [Actions #38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) ended with `TRACE_PROCESS_EXIT=124`, the expected 35-second timeout, not a crash. The counter-only `GPU::Vsync` callback logged increasing counts through `VSYNC_TRACE frame=2040`; the same stdout also recorded `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, and `Execute !`. This demonstrates the event callback itself can remain active stably while the emulator completes headless boot. The prior exit 139 is therefore consistent with the register-read/formatting instrumentation as a confounder, though not yet proven conclusively.

The next test [Actions #38974903834](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974903834), workflow commit [ff0faa5](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/ff0faa598c6e19295229b450c6f9d42c83e590fb), keeps the stable counter and only samples PC every 120 VSync callbacks. It acquires `PCSX.getRegisters()` before event registration (following upstream test style), reads only `regs.pc`, and prints decimal values instead of using `%08X`. If it completes to timeout and emits PC lines without crashing, decode the decimal addresses and compare when they cross from BIOS `0xBFC...` to executable entry space `0x80011448`. If it still exits 139, abandon live register access in the callback and use an upstream-supported CPU execution instrumentation approach.


### Built-in trace API mismatch and emulator correction — 2026-10-17

Workflow run [#38975154606](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975154606) used the pinned AnyLinux package based on upstream PCSX-Redux commit `0c3572c3d`. The process aborted immediately with Lua error `attempt to index field 'CPU' (a nil value)` when accessing `PCSX.CPU.Trace`; it logged no VSync counters. I verified that `src/core/pcsxffi.lua` at ref `0c3572c3d` does not expose `PCSX.CPU.Trace`, although a newer upstream source ref does. This was a build/API mismatch, not a ROM failure.

Corrective runner workflow commit [c994afc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/c994afccfa62efcc01751a7c2b39d89b109d936a) now downloads the user-provided/private-release upstream `PCSX-Redux-HEAD-x86_64.AppImage` and verifies SHA-256 `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`; this build was previously verified to reach `EXEC:PC0` on Ubuntu 26.04. It uses the new `PCSX.CPU.Trace` interface for a bounded frame 1620–1680 capture, then prints only the last 80 records, and deletes all media/trace files during runner cleanup. New test [Actions #38975223698](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975223698) has started; read its final logs before drawing conclusions.


### Packaged emulator also lacks built-in CPU tracing — 2026-10-17 correction

Runner [Actions #38975223698](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975223698) was intended to use the private upstream HEAD AppImage, but it aborted with the same `attempt to index field 'CPU' (a nil value)` message before a VSync sample. The uploaded HEAD binary also predates the `PCSX.CPU.Trace` Lua binding; do not confuse this with a game or ROM failure. Thus **neither packaged build currently available in the research release provides the required trace API**.

Current workflow commit [8304b7d](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8304b7dd56be13673e83e84bb738458eca0cfc2d) instead checks out upstream PCSX-Redux source at pinned commit `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`, verifies `src/core/pcsxffi.lua` exposes `Trace = {`, and builds the native CLI binary using upstream's published builder container. Run [Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) was actively building at the time of this note. Only after build success can the frame-1620-to-1680 bounded built-in instruction trace be interpreted; build failures are infrastructure evidence, not ROM behavior.


### Interpret the first GUI captures against boot timing — 2026-10-17

The 10-second and 20-second all-black frames from GUI run [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) were taken before the headless boot's executable-load point. The stable counter-only test [#38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) reached its VSync count 1620 shortly before the separate log emitted `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, and `Execute !` (the entire 35-second test later reached frame 2040). So the 10s/20s black frames cannot by themselves establish a permanent black-screen failure; the GUI test must observe well beyond the ~27–30s point and ideally capture the emulator window rather than the X root. The earlier 35s GUI window may also be borderline due to UI overhead.

Current source-trace runner [#38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) is still building a pinned upstream source revision so the actual built-in CPU trace API can be tested without live register reads. The result must be checked before analysis proceeds.


### Extended GUI observation launched — 2026-10-17

Runner workflow commit [aea4c20](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aea4c20accfd6d1c5089a226f52a2c4183d2d9a8) extends the GUI phase from 35s to 100s and measures frames at 30s, 60s and 90s, still using temporary local captures which cleanup deletes. Current run [#38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679) has both private asset retrieval steps passing and is in the A/B + GUI step; output has not completed yet. This should distinguish early BIOS-only black captures from a persistent blank frame after the expected executable entry point.

Source build/trace workflow [#38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) is also still in `Build pinned upstream PCSX-Redux with CPU trace support`; no claim is made about build success until the step completes. It uses pinned source commit `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` and the official builder image.


## End-to-end private-ROM run and test-harness corrections — 2026-10-17

Reviewed [Actions #38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679) and [CPU trace Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756).

Confirmed by log: read-only secret was present; normalized release assets were retrieved; ROM byte count and SHA-256 matched; the temporary CUE passed structural validation; OpenBIOS identified disc `SLPS-03553`; `SYSTEM.CNF` selected `SLPS_035.53`; all 187 executable chunks completed; and PCSX-Redux printed `EXEC:PC0(80011448)` / `Execute !`. The Analog Port 1 setup was applied to both compared builds and neither emitted `Unknown command for pad: 43`. Both headless processes reached their 90-second caps; the executable-entry marker is not a title-screen or playable-input result.

The 30/60/90-second GUI probe produced root-window metrics of `mean=0`, `stddev=0`, `colors=1` and no OCR text. Inspecting the workflow exposed a test-harness flaw: it invoked `import -window root`, so those metrics described the Xvfb root background, not necessarily PCSX-Redux's own window. Do not use these frames to diagnose guest rendering. Corrective workflow commit [8829933](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8829933b3b6815dce694ebe6d46cd2a1f0fee9f0) now searches for a visible PCSX-Redux window, captures that window only, reports the window tree if it cannot find one, and does not fall back to the root.

The first source-build trace attempt [#38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) successfully compiled the pinned upstream source but the host executable failed before emulation because `libcapstone.so.5` was missing. No trace callbacks ran. Corrective commit [d965dcc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/d965dcc864c73818e67d6a1e5f9edc19d4a3a17c) adds upstream-documented `libcapstone-dev` and a preflight `ldd` check. Retests [#39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) and [#39000276365](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365) were launched on 2026-10-17; inspect final logs before marking either fix successful.

The runner repo remains free of game media and trace assets: the workflows download private files only to the ephemeral runner, then remove them during cleanup. No gameplay formula was newly confirmed in this run.


## Corrected GUI-window capture — result and interpretation (2026-10-17)

Runner Actions #39000276365 completed successfully after commit 8829933. The capture code found a visible PCSX-Redux window at each 30/60/90-second capture point. This fixes the prior root-window measurement flaw. The actual window frames were still uniformly black by ImageMagick statistics (1280x800, mean 0, standard deviation 0, one color); OCR in Japanese/English returned no text.

Do not conclude that the game framebuffer is black after entry: the GUI probe's own log did not emit [CHUNK1] done chunks=187, EXEC:PC0(80011448), or Execute !. Those markers were seen in the headless A/B probes in the same run. Current result is a GUI-vs-headless discrepancy: headless execution reaches the game executable, while GUI-mode boot remains black and lacks the executable-entry markers within the observation window. Next debug question is why the UI-mode boot path differs (window/context/emulator run state/OpenBIOS progress), not yet which game render routine fails. No frame or private game data was uploaded as an artifact.


## GUI initialization / GLX diagnostic follow-up — 2026-10-17

Because the successful window-targeted run (#39000276365) found a real 1280x800 PCSX-Redux window but no visible pixels, OCR text, GUI PAD_SETUP marker or executable-entry markers, the next test is [Actions #39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307), runner commit [259d587](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/259d587c6b677be7f6466b0ec61edb1940faec49). It adds `glxinfo -B` under the same Xvfb/llvmpipe configuration and emits the last 120 lines of the GUI process stdout and PCSX log, plus an explicit result for whether command-line Lua setup was observed. This can identify whether the GUI process gets past GL initialization and reaches command-line setup. Keep GUI output distinct from headless output; the latter's EXEC marker cannot stand in for the GUI run's own boot progress.


## Cloud AppImage A/B and GUI stall — 2026-10-17

Matched headless comparison: [runner Actions #39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307). Both release AppImages used the same private ROM, normalized temporary CUE, openbios-chunked.bin, interpreter/software GPU, Analog/connected/remapped Port 1, and 90-second cap. Both logged disc SLPS-03553, SYSTEM.CNF boot target, 187 completed executable chunks, EXEC:PC0(80011448) and Execute !. Neither logged Unknown command for pad: 43. The 90-second observation boundary is not evidence of a crash, title-screen render or gameplay.

The same run's GUI path reached GLX diagnostics: Mesa llvmpipe; OpenGL 3.3 core/compatibility. The script captured the actual AnyLinux emulator window at 30/60/90 seconds (not the Xvfb root), but each 1280×800 capture had mean=0, stddev=0 and one color; OCR was empty. GUI stdout/log showed the Lua PAD_SETUP marker and early chunk indices 0/8/16/24/32, but no completed 187-chunk marker or EXEC:PC0/Execute !. Thus GUI is stalled before the known headless executable handoff; lack of an OpenGL context is not supported by the GLX probe, while the exact reason remains open. ALSA dummy-device errors were logged, but no evidence connects them causally to the boot stall.

Release identities from the [private research release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15):
- AnyLinux PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage: 65,747,557 bytes; SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c; source commit 0c3572c3db75f97542001e453ae80ba8c3f8acba.
- Asset named PCSX-Redux-HEAD-x86_64.AppImage: 91,474,424 bytes; SHA-256 5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8; package notes identify source 9c6f98a0ed0581635f9123147e382c248e0f5ddc dated 2026-09-28. “HEAD” is the asset name, not confirmation it is the latest upstream commit. The comparative GUI result remained pending for run #39002136781 at time of note.

Source trace run [#39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) was a host-runtime deployment failure, not a ROM diagnosis: capstone was fixed and the build linked, but host ldd could not locate libavformat.so.62, libavcodec.so.62, libswresample.so.6, libavutil.so.60, and libSDL3.so.0. Workflow commit [16a6faff](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/16a6faff066b913480ad121b497db79df03a9de2) pins the builder image by digest, checks dependencies and launches trace inside that image, and allows 45 minutes for compilation. Rerun [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) was still compiling when this entry was written; trace conclusions remain pending.

No screenshot, ROM, BIOS, save state, memory dump or trace artifact was uploaded. Do not start Story Mode until a recognizable Naruto menu/title and responsive input are independently evidenced.


## Verifikasi GUI A/B terbaru dan perbaikan harness — 2026-10-17

Run GUI A/B [#39002136781](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002136781) berstatus workflow `success`, tetapi **bukan hasil uji GUI yang berhasil**. Langkah headless di job yang sama tetap membuktikan kedua AppImage membaca disc `SLPS-03553`, menuntaskan 187 chunk executable, dan mencatat `EXEC:PC0(80011448)` serta `Execute !`; keduanya tidak lagi mencatat `Unknown command for pad: 43`. Saat masuk bagian GUI, `gui_probe.sh` berhenti untuk kedua build pada `PAD_SETUP: unbound variable` karena variabel shell tidak diekspor. Tidak ada jendela emulator yang ditemukan dan tidak ada frame yang ditangkap. Karena hasil probe tidak dipaksa menjadi kegagalan job, status `success` hanya berarti step berakhir tanpa kegagalan workflow yang terdeteksi; status itu bukan bukti GUI/game berhasil.

Perbaikan minimal sudah didorong ke runner pada commit [aac684d120ec025c4a87197da8d835f90b89f869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aac684d120ec025c4a87197da8d835f90b89f869): ekspor `PAD_SETUP` sebelum skrip probe GUI dipanggil. Rerun ROM privat [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) sudah dipicu dan masih `in_progress` pada pemeriksaan terakhir; hasil frame, OCR, boot-marker GUI, dan cleanup masih harus diperiksa dari log akhirnya.

CPU-trace run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) juga masih `in_progress`. Secret dan pengunduhan/verifikasi file privat telah dilewati; step source-build di container Docker yang dipatok digest masih berjalan, sedangkan capture trace dan cleanup belum dimulai. Belum ada `CPU_TRACE_SIZE` atau `CPU_TRACE_LINE` yang dapat dipakai untuk analisis.

Current upstream PCSX-Redux yang terverifikasi saat cek adalah [41f3196257d0962942b60983201aade951ebbd54](https://github.com/grumpycoders/pcsx-redux/commit/41f3196257d0962942b60983201aade951ebbd54) (2026-10-17 02:53:17 UTC). AppImage berlabel “HEAD” tetap build source 9c6f98a0, bukan upstream HEAD terkini. Tidak ada bukti bahwa judul/menu tampil atau input gameplay merespons; gate RT-001 tetap tertutup dan Story Mode tidak boleh dimulai.


## Hasil GUI A/B setelah fix ekspor PAD_SETUP — 2026-10-17

Run [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) memakai runner commit `aac684d120ec025c4a87197da8d835f90b89f869`. Perbaikan harness terbukti: `PAD_SETUP` berhasil pada GUI AnyLinux dan proses menjalankan pengamatan/capture. Hasil per build:

- **AnyLinux:** GUI log mengenali OpenBIOS, disc `SLPS-03553`, `SLPS_035.53;1`, `SYSTEM.CNF` dan target `BOOT`; marker Analog PAD_SETUP ada. Jendela X11 yang ditemukan (ID `2097204`) ditangkap langsung tiga kali. Frame 30/60/90 masing-masing 1280×800, mean=0, stddev=0, colors=1; OCR jpn+eng kosong. Tidak ada `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, atau `Execute !` pada log GUI. GUI proses exit 124 pada batas observasi 100 detik.
- **AppImage berlabel “HEAD”:** jendela tidak terbentuk. Log menyatakan `Unable to create main window: Couldn't find matching GLX visual`, setelah `SDL failed to create OpenGL 3.2 core context, retrying with any 3.0 profile`. GUI tidak menunjukkan PAD_SETUP atau executable handoff; tidak ada frame. Exit 137 saat proses mencapai penanganan batas observasi/timeout. Bukti yang kuat adalah kegagalan inisialisasi window/GLX pada build ini, bukan crash guest atau kesalahan ROM yang telah dibuktikan.
- **Pembanding headless dalam job yang sama:** kedua build tetap mencapai `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)` dan `Execute !`, dan tidak mencatat warning `Unknown command for pad: 43`. Keduanya berakhir di batas 90 detik (124), bukan bukti crash.

Perbedaan GUI/headless kini lebih spesifik. AnyLinux dapat membuat window dan menjalankan Lua setup tetapi tidak menunjukkan progres yang setara dengan path headless; frame hitam diambil dari window emulator yang ditargetkan, namun karena GUI belum menunjukkan executable handoff, frame itu belum boleh ditafsirkan sebagai layar game setelah entry. Build “HEAD” berhenti lebih awal pada pembuatan window. Langkah lanjut yang masuk akal adalah membandingkan jalur startup GUI dan `-no-ui` pada titik CD/loader/CPU/Lua/OpenGL sebelum mengubah BIOS/ROM atau mendiagnosis renderer guest.

Cleanup step berhasil; tidak ada artefak Actions. Log menyatakan file media privat, profil, frame, log serta ekstraksi AppImage telah dihapus dari workspace runner sementara. Pemeriksaan recursive tree repo publik menemukan hanya workflow, file docs, README dan .gitignore; tidak ditemukan file media game di Git.

## Status source-build CPU trace ketika diperiksa — 2026-10-17

Run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) masih aktif pada step **Build pinned upstream PCSX-Redux with CPU trace support**, yang mulai 04:17:26 UTC setelah download/validasi selesai. Run tetap `in_progress`; capture trace dan cleanup belum mulai. Log archive belum tersedia sementara job aktif (`BlobNotFound` dari endpoint unduh log), jadi durasi build yang panjang belum cukup untuk menyimpulkan penyebab atau hasil. Batas workflow adalah 45 menit; periksa status step/log lagi sebelum deadline dan hindari run duplikat. Belum ada instruction record yang dapat dianalisis pada frame 1620–1680.

## Hasil CPU trace pinned source dan diagnosis boot — 2026-10-17

### Run dan integritas build

[Actions #39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849), workflow commit `16a6faff066b913480ad121b497db79df03a9de2`, job `117306664750`, selesai `success` pada 04:44:27 UTC. Job mulai 04:17:11 UTC. Pengunduhan/validasi privat selesai 04:17:26; source build mulai 04:17:26 dan selesai 04:43:46; capture trace selesai 04:44:21; cleanup selesai 04:44:25. Sumber dipatok pada `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`; image builder dipatok pada `ghcr.io/grumpycoders/pcsx-redux-build@sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`. Log memuat `PCSX_BUILD_RESULT=compiled pinned source with built-in CPU trace API; dependency check and runtime use the same builder image`. Pemeriksaan `ldd` dalam image yang sama sukses; library termasuk `libcapstone.so.5`, FFmpeg, SDL3, dan X11 ter-resolve. Step build memerlukan sekitar 26m20s, bukan hang workflow; tidak perlu mengulang build identik.

### Hasil capture dan makna instruksi

Marker terverifikasi: `PAD_SETUP=port1 analog device connected and remapped`; `VSYNC_TRACE frame=1620`; `CPU_TRACE_WINDOW=enabled frame=1620`; `VSYNC_TRACE frame=1650`; `VSYNC_TRACE frame=1680`; `CPU_TRACE_SIZE=16031631`; `CPU_TRACE_WINDOW=disabled and last 80 records printed`; `TRACE_RESULT=VSync counter callbacks fired.`; `CPU_TRACE_RESULT=Built-in instruction records were printed.`; `TRACE_PROCESS_EXIT=124`. Exit 124 ialah batas capture 35 detik, bukan bukti crash. Tidak ada artefak Actions. Cleanup step sukses dan log menyatakan ROM, CUE, BIOS, emulator, dan log trace temporer dihapus.

Contoh ekor trace (record pra-eksekusi guest):
```
PC 000015a4: lw    $v0, 0x5de4(a3)   # nilai terbaca 00000000
PC 000015a8: nop
PC 000015ac: beq   $v0, $a0, 0x000015c8
PC 000015b0: nop
PC 000015b4: beq   $v0, $a1, 0x000015cc
PC 000015b8: nop
PC 000015bc: addiu $v1, $v1, -1
PC 000015c0: bnez  $v1, 0x000015a4
PC 000015c4: nop
```
Pola ini berulang; nilai register pada disassembly bergerak turun dari sekitar 0x21b ke 0x212 dalam tail terakhir. Ini adalah loop/polling guest yang memiliki penghitung menurun; belum diketahui field/flag apa yang diuji melalui effective address `0x5de4(a3)`. Tidak cukup bukti untuk menyebut infinite loop atau hang permanen.

Provenance kode: source pinned [`psxinterpreter.cc`](https://github.com/grumpycoders/pcsx-redux/blob/6b9df482d7b77b9ae218d9c48c1ce1a43c265206/src/core/psxinterpreter.cc#L1831-L1838) mengambil `const uint32_t pc = m_regs.pc` sebelum memanggil `m_cpuTrace->capture(pc, code)`; [`cputrace.cc`](https://github.com/grumpycoders/pcsx-redux/blob/6b9df482d7b77b9ae218d9c48c1ce1a43c265206/src/core/cputrace.cc#L82-L85) menyimpan nilai itu langsung pada `e.pc`. Maka alamat trace merupakan PC guest mentah, bukan logika PCSX-Redux. Entry dari header EXE utama tetap `0x80011448` dengan load base `0x80010000`; loop pada `0x000015a4–0x000015c4` tidak sama dengan entry tersebut. Physical RAM alias, provenance BIOS/loader, dan alamat overlay belum tervalidasi, sehingga jangan menyebut loop sebagai BIOS atau game code tertentu.

### Perbandingan boot yang penting

Source-build `-no-ui` ini merekam BIOS OpenBIOS, disc `SLPS-03553`, ID `SLPS03553`, executable `SLPS_035.53;1`, serta PAD_SETUP; tetapi log tidak memperlihatkan SYSTEM.CNF/BOOT, chunk selesai, atau EXEC:PC0 selama capture. Ini berbeda dari headless dua AppImage di run GUI A/B #39002846886 yang mencapai 187 chunk dan `EXEC:PC0(80011448)`/ `Execute !`. Karena itu trace ini belum boleh digunakan untuk menyatakan entry game berhasil. Berikutnya bandingkan sumber boot/CD/BIOS pada build source pinned dengan jalur headless AppImage yang sudah mencapai entry, lalu catat guest PC berkala di VSync yang lebih akhir bila dibutuhkan. Jangan ubah ROM atau BIOS tanpa temuan penyebab.

Run GUI A/B #39002846886 terpisah: AnyLinux menjalankan PAD_SETUP dan window sebenarnya tertangkap 30/60/90s, tetapi frame 1280×800 tetap mean=0, stddev=0, satu warna, OCR kosong, tanpa marker handoff executable. AppImage berlabel “HEAD” gagal membuat window dengan `Couldn't find matching GLX visual` serta kegagalan konteks OpenGL 3.2. Hal ini memisahkan diagnosis UI/startup dari guest; belum ada bukti title/menu atau input game responsif.

## Diferensial source terhadap build AnyLinux — 2026-10-17

GitHub compare [PCSX-Redux `0c3572c3` → `6b9df482`](https://github.com/grumpycoders/pcsx-redux/compare/0c3572c3db75f97542001e453ae80ba8c3f8acba...6b9df482d7b77b9ae218d9c48c1ce1a43c265206) memverifikasi head source trace 803 commit di depan source AnyLinux. Diff per-file menonjol: `src/core/cdrom.cc` +1.476/-1.392; `src/core/psxinterpreter.cc` +290/-81; `src/core/pad.cc` +362/-22; `src/core/psxmem.cc` +58/-19; perubahan di `src/core/psxemulator.cc`; dan gitlink `src/mips` berubah dari `d93840921b5ad7ed515e95b0e414f1b1e2038b1a` ke `361f3f6a6f8d8bb98548900d8a231e2d2a2c1dc4`. File interpreter terbaru menerapkan `branchBase()` dan state untuk branch-delay/exception yang tidak ada pada base AnyLinux. Perubahan ini memberi tempat yang konkret untuk inspeksi; compare saja tidak membuktikan mana yang menyebabkan boot berbeda. Kedua workflow masih memakai BIOS diagnostik yang sama dari private release, jadi perubahan gitlink tidak otomatis membuktikan binary BIOS yang dimuat berbeda.

Perintah headless di workflow GUI A/B dan trace source sama-sama mencantumkan `-no-ui`, `-run`, `-interpreter`, `-softgpu`, Lua setup/analog PAD, dan stdout/log. Perbedaan observasi pentingnya: AppImage diberi hingga 90s; source trace hanya 35s. Trace source mencapai VSync frame 2040 dalam proses tersebut, tetapi rekaman instruksi hanya frames 1620–1680 dan ekornya berada pada loop guest PC rendah. Karena itu belum dapat dibedakan apakah versi source punya perubahan boot, tahap BIOS/CD menjadi lebih lambat, atau loop segera keluar setelah capture ditutup.

Lanjutan yang mengisolasi hipotesis: jalankan source pinned dengan batas 90s dan PC guest sampling per 30 VSync, ambil trace window yang lebih akhir (mis. 4500–4560), dan cetak marker `SYSTEM.CNF`/chunk/EXEC terpisah dari `CPU_TRACE_LINE` supaya tidak tersisih oleh `tail -160`. Setelah ada PC kemudian, bandingkan cabang `cdrom.cc` dan perubahan branch/delay-slot interpreter terhadap jalur yang dipetakan; hindari menunjuk commit/file sebagai akar masalah sebelum hasil sebanding tersedia.

## CPU-trace follow-up 90 detik — Actions #39004736399 (2026-10-17)

Sumber bukti utama adalah log final [Actions #39004736399](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39004736399), bukan status workflow semata. Run selesai `success` dari 05:01:31–05:29:40 UTC (12:01:31–12:29:40 WIB). Semua step sukses.

### Build dan integritas input

Source PCSX-Redux dipatok pada `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`; builder image tetap digest `d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`. ROM ukuran 325.989.552 byte dan SHA-256 `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88` terverifikasi; struktur CUE sah setelah referensi FILE sementara dinormalisasi. Build berjalan sekitar 26m20s lalu mengeluarkan `PCSX_BUILD_RESULT`. Pemeriksaan `ldd` pada builder yang sama sukses tanpa `not found`.

### Observasi runtime

Trace berjalan hingga batas observasi 90 detik dan keluar dengan kode 124 yang memang ditetapkan sebagai timeout. PC sampling setiap 30 VSync menghasilkan 158 sampel (frame 30–4740); histogramnya: `0x000015a4` sebanyak 157 sampel, dan `0x00000870` sekali di frame 420. PC kemudian kembali ke `0x000015a4` dan bertahan sampai sampel frame 4740.

Kedua jendela CPU trace selesai:
- Frames 1620–1680: 16.031.631 total records menurut summary, 200 records disampling, 9 PC unik.
- Frames 4500–4560: 16.031.484 total records menurut summary, 200 records disampling, 9 PC unik.
- Pola hot PC konsisten di dua jendela; `0x000015c0` dan `0x000015c4` masing-masing muncul 23 kali pada sampel ringkasan, `0x000015a4` dan alamat tetangga muncul sekitar 22 kali.

Boot marker pada log aktual mengonfirmasi OpenBIOS, disc label `SLPS-03553`, disc ID `SLPS03553`, serta nama EXE `SLPS_035.53;1`. Marker `SYSTEM.CNF`, `BOOT =`, penyelesaian 187 chunk, `EXEC:PC0(80011448)`, dan `Execute !` tidak muncul. Maka sesi tidak membuktikan game executable dicapai.

Workflow baru memfilter CPU trace menjadi agregat PC dan tidak mengeluarkan baris instruksi/operand mentah di hasil runtime. Cleanup step selesai: ROM, CUE, BIOS, emulator dan file trace sementara dihapus; tidak ada artefak Actions. Periksa terpisah isu retensi log lama #39001985849, yang sebelumnya diaudit berisi 80 record instruksi/operand mentah.

### Interpretasi

Bukti mendukung loop PC rendah yang masih muncul hingga akhir observasi, bukan kesimpulan pasti bahwa CPU crash atau hang permanen. Jangan menetapkan fungsi/alamat sebagai OpenBIOS, CD loader, atau kode game tanpa validasi source/mapping. Hipotesis berikutnya perlu menghubungkan alamat loop ke source dan state tunggu yang relevan; jika perlu pengujian baru, tambahkan marker diagnostik yang membedakan progres CD/loader dari polling, tanpa mengeluarkan disassembly mentah.

RT-001 masih **Open / blocked**; title/menu Naruto dan respons input terkontrol belum diverifikasi.

## Catatan eksperimen runtime tambahan — 2026-10-17

### Internal screenshot path
Run privat [#39011515345](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011515345) memvalidasi kembali ROM (325.989.552 byte; SHA-256 yang diharapkan), lalu menjalankan AnyLinux dengan OpenBIOS pada jalur `-no-ui`. Marker BIOS/disc dan `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, `Execute !` tercatat. Tetapi `PCSX.GPU.takeScreenShot()` memberi width=0, height=0, bpp=0 pada frame 1500, 1680, 1800; VSync capture tidak mencapai titik selanjutnya dalam batas 110 detik. Konversi gagal karena buffer/dimensi tidak valid, cleanup selesai, dan daftar artefak Actions kosong. Ini kegagalan metode capture, bukan bukti layar game berhasil tampil atau rusak.

### Source-current GUI probe
Workflow privat [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) dibuat untuk membangun source pin PCSX-Redux `1525a93676dbece9fe70f10ff129aeaa14eec30d` yang diverifikasi sebagai `main` pada saat workflow dibuat, lalu menguji ROM sama di Xvfb, menangkap langsung jendela emulator, dan mencatat ringkasan PC. Ini menghindari penggunaan ulang capture API dalam mode no-UI dan membandingkan source-current terhadap AppImage lama. Status ketika catatan dibuat: workflow masih berjalan; hasil perlu diperiksa sebelum kesimpulan. Capture hanya dimaksudkan sebagai private Actions artifact retensi 3 hari; file media dan capture dibersihkan dari runner.

### Log-retention action
Run [#39011611436](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39011611436) berhasil memanggil DELETE API terhadap **hanya** run publik `#39001985849`, yang sebelumnya berisi 80 record instruksi/operand. GET sesudahnya mengembalikan 404; tidak ada run lain yang ditargetkan. Jangan mengulang keluaran instruksi/operand mentah di log publik.

**Kesimpulan saat ini:** tidak ada bukti title/menu Naruto, input dalam game, atau progres Story Mode. RT-001 tetap Open / blocked. Jangan memperlakukan keberhasilan workflow, CD recognition, atau executable-entry handoff sebagai keberhasilan gameplay.

## Uji emulator alternatif tambahan — 2026-10-17

Workflow privat [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) kini menguji rilis DuckStation resmi, dengan AppImage SHA-256 `c5e6f045f6a242082fcafa9f02d56ad895e233b942728788d232ad0c0c765c24`, ROM yang sama dan OpenBIOS `openbios.bin` dari private release. Harness Xvfb mengambil frame jendela dan mengirim Return/Cross lewat pemetaan keyboard sementara, lalu menyimpan capture sebagai artifact privat 3 hari dan menghapus workspace. Status saat catatan ini dibuat: queued; belum ada hasil boot/menu/input yang bisa disimpulkan. Ini uji kandidat, bukan klaim kompatibilitas.



## Eksperimen runtime — audit DuckStation dan perbaikan harness, 2026-10-17

### Run #39012200147: hasil aktual
- ROM lolos pemeriksaan ukuran dan SHA-256; paket DuckStation yang diunduh lolos pemeriksaan SHA-256.
- Tetapi proses emulator keluar dengan kode 127 sebelum membuat window: `/squashfs-root/AppRun: error while loading shared libraries: libOpenGL.so.0: cannot open shared object file`.
- Lima percobaan capture menghasilkan `no DuckStation window found`; harness mencatat `INPUT_SEQUENCE_SKIPPED=no visible window`. Jadi Return/Cross tidak benar-benar dikirim ke game, dan hasil ini tidak menguji apakah DuckStation/OpenBIOS kompatibel dengan ROM.
- Artifact terdaftar (ID `12093451882`) hanya berukuran 293 byte; pemeriksaan ZIP menunjukkan satu file `duckstation.stdout` 183 byte dan nol gambar. Retensi artifact tiga hari, tetapi tidak ada media game yang ditangkap. Cleanup menyatakan ROM, BIOS, emulator, frame dan log pada runner dihapus.

### Koreksi spesifik, bukan pengulangan build identik
- Workflow `.github/workflows/naruto-duckstation-private-probe.yml` diperbaiki pada commit `058aadea1c664712b62a63cf01fcb3e5598ef047`: menambahkan paket runtime `libopengl0 libglx0 libgl1` untuk library GL yang hilang dan mengubah upload glob menjadi `captures/*.png`, sebab capture dinamai `pre-input-20-sec.png`/ `after-return.png`, bukan `frame-*.png`.
- Rerun [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) menjadi eksperimen berikutnya. Keberhasilan berikutnya hanya berarti launcher/probe berjalan; title/menu dan input harus dibuktikan terpisah.

### PCSX-Redux source-current
Run [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih pada langkah build source pin `1525a93676dbece9fe70f10ff129aeaa14eec30d` ketika diperiksa. Hasil capture belum tersedia; tunggu sampai run final dan evaluasi marker boot, frame metric/OCR, respons pad, serta cleanup.

**Kesimpulan saat catatan ini ditulis:** belum ada title/menu Naruto yang terkonfirmasi; RT-001 tetap Open / blocked dan Story Mode belum dijalankan.


## DuckStation retest #39012504017 — dependensi EGL, 2026-10-17

Setelah `libopengl0 libglx0 libgl1` dipasang, rerun [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) tidak lagi gagal di `libOpenGL.so.0`, tetapi keluar 127 pada pesan `libEGL.so.1: cannot open shared object file`. Semua capture mencari window dan gagal; tidak ada gambar/OCR, input keyboard tidak pernah dikirim ke game. Artifact hanya 292 byte dan tidak berisi PNG. Ini tetap kegagalan dependency host, bukan hasil kompatibilitas ROM/BIOS.

Commit `5afd32eca0d32ee191de7f2963f74b53aed89448` menambahkan paket `libegl1` untuk run berikutnya [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027). Run itu masih pada langkah boot/capture saat diperiksa; periksa exit diagnostics dan artifact aktual. Source-current PCSX [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih membangun source. RT-001 tetap Open / blocked.


## DuckStation probe final — GUI wizard tetapi belum masuk BIOS/game, 2026-10-17

Run [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) memperbaiki dependensi EGL dan membuka window sebenarnya (760×498). Artifact privat `12094155047` berisi delapan frame dan stdout; pemeriksaan visual pada `pre-input-20-sec.png`, `after-return.png`, dan `after-second-return.png` menunjukkan first-run setup wizard DuckStation. Halaman BIOS menampilkan pesan bahwa DuckStation memerlukan BIOS PS1/PS2, walaupun satu file terdeteksi. Log menyebut BIOS dipetakan dan pencarian Auto BIOS, tetapi tidak ada marker disc, SYSTEM.CNF, load executable atau Naruto. `DUCKSTATION_EXIT=137` muncul saat batas observasi; workflow/cleanup tetap sukses.

Input Return pada jendela ini memajukan wizard. Z/Cross tidak menghasilkan bukti perubahan state game. Maka hasilnya bukan game boot maupun input test. Hipotesis yang paling kuat berdasarkan bukti sekarang adalah OpenBIOS yang tersedia tidak diterima DuckStation sebagai BIOS PS1 yang valid; tidak ada dasar untuk menyimpulkan ROM Naruto tidak kompatibel. Tidak meminta retail BIOS atau secret tambahan. Salinan artifak screenshot lokal telah dibersihkan sesudah pemeriksaan.

**Langkah berikut:** utamakan PCSX-Redux source-current [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708), yang masih pada tahap build ketika diperiksa. RT-001 tetap Open / blocked.


## Hasil source-current dan perbandingan OpenBIOS — 2026-10-17

### PCSX-Redux source-current GUI (#39011842708)
Run selesai dengan workflow `success`, source commit pin `1525a93676dbece9fe70f10ff129aeaa14eec30d` berhasil dibangun dan `ldd` lulus. Lima capture jendela pada 20/40/60/80/95 s seluruhnya hitam uniform (1280×800, mean 0/stddev 0/satu warna); OCR kosong. Log memuat disc label `SLPS-03553`, OpenBIOS, dan PAD_SETUP Analog, tetapi hanya satu guest PC sample pada frame 300, `0x000015a4`. Tidak ada `SYSTEM.CNF`, marker BOOT, seluruh 187 chunk, ataupun `EXEC:PC0`. Exit 124 ialah batas observasi. Artifak #12094116949 berisi lima PNG hitam dan stdout; cleanup sukses.
### AnyLinux: fastboot BIOS vs chunked BIOS (#39013612865)
Dengan emulator/AppImage, ROM/CUE, interpreter/software GPU, Port 1 Analog, dan interval sama:
- Fastboot BIOS (`openbios.bin`, hash `25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d`) membaca `SYSTEM.CNF`, `BOOT`, lalu mencatat `EXEC:PC0(80011448)` dan `Execute !`.
- Chunked BIOS (`openbios-chunked.bin`, hash `7644ab45db8519a3621ef9cb0283f0ced5258287f8105c0e9d7e784fef9362b7`) membaca payload satu sektor per call dan berhenti mencatat progres setelah indeks 40, tanpa entry marker selama window observasi.
- Window selector berdasarkan judul tidak menemukan jendela pada kedua run sehingga tidak ada screenshot; input test dilewati. Artifact #12094102119 berisi stdout dan log, bukan PNG. Maka perbedaan BIOS berpengaruh pada progres loader, tetapi belum ada bukti visual boot.
### Follow-up
Workflow [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) mengulang fastboot saja dengan identifikasi jendela X11 generik dan tree dump, agar jendela tanpa caption yang dikenali tidak menyebabkan kesimpulan keliru. Periksa hasil akhirnya.
**Status:** belum ada title/menu Naruto dan input game nyata; RT-001 tetap Open / blocked.


## Fastboot GUI dengan window discovery generik — 2026-10-17 (#39015133027)

- Fastboot OpenBIOS + AnyLinux kembali mengenali disc `SLPS-03553`, membaca `SYSTEM.CNF`/BOOT dan mencapai `EXEC:PC0(80011448)`/ `Execute !`.
- Perbaikan selector X11 berhasil mendeteksi window ID 543 pada 1280×800. Jadi pengujian sebelumnya yang melaporkan no window terlalu sempit dalam pencarian title; sekarang pengambilan pasti berasal dari window aplikasi, bukan root Xvfb.
- Semua capture (before-input, after Return, after Z/Cross, frame 40/65/90s) mempunyai mean 0/stddev 0/satu warna; OCR kosong. Walaupun input event disampaikan ke app window, hasil visual sama persis hitam, jadi respons input game tidak terbukti.
- Workflow selesai dan cleanup sukses; artifact privat #12094179559 disimpan sementara.

Karena pengambilan register CPU melalui `PCSX.getRegisters()` dalam `GPU::Vsync` callback pernah berhubungan dengan pembekuan/segfault pada eksperimen terdahulu, follow-up [#39015290594](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015290594) mempertahankan fastboot/window detection/input sequence namun menghapus callback pembaca register. Hasilnya perlu dibandingkan sebelum memilih diagnosis GPU/rendering vs guest execution.
RT-001 tetap Open / blocked.


## Audit validitas capture — fastboot window probe #39015133027, 2026-10-17

Audit terhadap log aktual menunjukkan `CAPTURE_WINDOW=before-input id=543 name= width=1280 height=800`. Hex ID root yang muncul pada Xvfb adalah `0x21f` (decimal 543); karena selector generik `xdotool search --onlyvisible --name '.*'` cocok dengan root, capture tersebut adalah root Xvfb, bukan window emulator. Karena itu seluruh klaim metrik hitam/OCR kosong dan respons visual input dari run #39015133027 ditarik kembali sebagai **tidak valid**. Ini perbaikan interpretasi penting; jangan teruskan metrik itu ke diagnosis GPU.

Log boot tetap merupakan bukti sah dan menyebut `SYSTEM.CNF`, BOOT, `EXEC:PC0(80011448)`, `Execute !` pada fastboot BIOS. Run #39015290594 mengulang selector yang sama tanpa pembacaan register; jangan tafsirkan gambar sebelum dipastikan bukan root. Workflow diperbaiki pada commit `83173bb10cfbf905a296f59720c0a63c95bc3a32` agar menghitung ID root dan mengecualikannya. Run yang perlu diperiksa berikutnya: [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649). Kriteria frame sah: `CAPTURE_WINDOW` mengarah ke XID non-root dan dimensi cocok dengan window aplikasi; jika tidak ada non-root window, jangan capture root sebagai gantinya.


## Follow-up selector X11: tree menunjukkan window PCSX nyata (#39015419649), 2026-10-17

Run [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649) mengecualikan root `0x21f`, tetapi tidak menghasilkan capture sebab daftar dari `xdotool search --onlyvisible --name '.*'` hanya memberi root. Root tree yang dicetak saat selector gagal memperlihatkan child `0x200034 "PCSX-Redux"` berukuran 1280×800. Maka aplikasi window ada; cara pengambilan XID-nya yang salah. Jangan menafsirkan ketiadaan PNG pada run ini sebagai ketiadaan window ataupun sebagai layar game hitam.
Run [#39015610296](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015610296) yang baru memakai parsing ID langsung dari root tree dan root exclusion, lalu fokuskan XID sebelum input. Probe tetap fastboot dan tidak membaca register CPU di callback VSync. Boot markers yang sudah terkonfirmasi pada run sebelumnya adalah SYSTEM.CNF/BOOT/EXEC:PC0/Execute!; tampilan title/menu masih belum terverifikasi.


## Fastboot dengan capture aplikasi valid dan input tidak mengubah tampilan (#39015722771)

Run [#39015722771](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015722771) berhasil menangkap jendela PCSX-Redux non-root XID `0x200034` / 2097204, 1280×800 dari `xwininfo -root -tree`. Root `0x21f` dikecualikan. Jadi frame ini valid. Semua lima capture—sebelum input, sesudah Return, sesudah Z/Cross, 40/65/90 detik—mempunyai mean 0, stddev 0, satu warna; OCR kosong. Tidak ada register read dalam callback VSync. Port 1 Analog tersambung; event key dihantarkan ke window, tetapi tidak ada perubahan tampilan/game yang terlihat. Boot marker fastboot tetap mencapai SYSTEM.CNF/BOOT, `EXEC:PC0(80011448)` dan `Execute !`. Artifact privat #12095061025 (retensi sampai 2026-10-20 08:02 UTC) dan cleanup sukses.
Ini membuktikan launcher emulator, GUI window dan entry handoff, namun **bukan title/menu/gameplay**. Selanjutnya run [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) mematikan `-softgpu` dan mencoba renderer OpenGL default di bawah Mesa llvmpipe 3.3. Bandingkan metrik frame, OCR, error renderer, dan boot markers untuk mengisolasi backend GPU.


## Fastboot renderer A/B — default OpenGL vs `-softgpu` (#39015919056)

Run selesai `success`. Dengan satu perubahan backend (hapus `-softgpu`, gunakan backend OpenGL default) dan Mesa llvmpipe, `glxinfo -B` mencatat renderer `llvmpipe (LLVM 21.1.8, 256 bits)`, OpenGL 3.3 Compatibility Profile. Jendela PCSX-Redux yang tertangkap adalah XID 2097204/`0x200034`, non-root, 1280×800. Semua lima frame sah—sebelum input, setelah Return, setelah Z/Cross, 40/65/90s—uniform black (mean 0/stddev 0/satu warna), OCR kosong. Boot log mencapai `SYSTEM.CNF`, BOOT, `EXEC:PC0(80011448)`, `Execute !`; proses mencapai batas observasi 100 detik. Port 1 Analog diatur dan input dihantarkan ke jendela, tetapi tidak ada perubahan visual. Tak ada pembaca register CPU dalam callback VSync; cleanup sukses, artifact privat #12094736241.
Perubahan backend GPU tidak memperbaiki layar. Untuk melanjutkan secara diskriminatif, uji PC setelah entry melalui GDB remote eksternal di waktu terpilih, dengan output hanya snapshot PC/hasil wait-state—jangan keluarkan raw instruction/operand dan jangan mengambil PC dari callback VSync. RT-001 tetap Open / blocked.


## GDB remote PC snapshot follow-up dimulai — 2026-10-17

Setelah #39015722771 (fastboot + softgpu) dan #39015919056 (fastboot + OpenGL default/Mesa llvmpipe 3.3) sama-sama menghasilkan jendela PCSX nyata tetapi frame hitam, run privat [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234) ditambahkan. Perubahan eksperimen berikutnya adalah mengambil snapshot PC lewat GDB remote pada t20/t30/t50/t70/t90, dengan timeout pendek dan output ringkas hanya PC. Tidak membaca register dari callback VSync dan tidak menyimpan raw instruction/operand. Status terakhir: installer GDB masih berjalan; belum ada hasil. Kesimpulan rendering/runtime tetap terbuka sampai snapshot dan capture akhir diperiksa.


## Keputusan emulator dan GDB remote probe final — 2026-10-17

Keputusan operasional: **PCSX-Redux AnyLinux prebuilt + OpenBIOS fastboot** tetap jalur utama. Fastboot mencapai `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, `EXEC:PC0(80011448)`, `Execute !`. Chunked BIOS hanya mencatat pembacaan payload sampai indeks 40 pada run A/B sebelumnya. DuckStation dibuka setelah dependensi GL/EGL diinstal tetapi hanya masuk first-run wizard; OpenBIOS tak diterima sebagai BIOS PS1/PS2 valid. Karena itu DuckStation belum menguji kompatibilitas ROM yang sebenarnya.
Run [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234) selesai: capture sah pada window PCSX non-root `0x200034`/2097204 (1280×800) seluruhnya hitam, OCR kosong, termasuk sesudah Return/Cross. Log fastboot mencapai entry handoff. GDB external did not return a PC sample at t20/t30/t50/t70 (exit 1) and timed out at t90 (exit 124); no successful PC snapshots. Cleanup succeeded, artifact #12095276220 (expires 2026-10-20 08:11 UTC). GDB internal raw output was deleted and not uploaded.
Interpretasi: emulator, ROM, fastboot BIOS dan window GUI aktif; tetapi tak ada bukti title/menu atau game-state visual. Tetap pakai jalur fastboot sebagai utama karena jalur loader-nya paling informatif, tetapi jangan mengklaim runtime/gameplay sudah berhasil. RT-001 tetap Open / blocked.

