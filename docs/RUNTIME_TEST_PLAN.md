## RT-001 follow-up — Start dan Circle perlu diuji dalam satu boot (2026-10-18)

Run [#39147391100](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39147391100) menyelesaikan 3.000 VSync dengan workflow `success`, tetapi tidak mengonfirmasi pilihan menu. Screenshot aktual frame 2.749/2.750 masih menunjukkan title prompt, dan layar tidak berubah ke menu atau Mode Select sampai frame 2.999. Penyebabnya: workflow melakukan boot bersih di setiap run; eksperimen ini hanya menyuntik Circle pada frame 2.750 tanpa mengulangi Start.

**Acceptance status terkini:**
1. Start membuka menu pilihan — **PASS**, berdasarkan transisi screenshot run #39145309203.
2. `はじめから` terkonfirmasi — **PENDING**.
3. Mode Select / Story Mode dimulai — **PENDING**.
4. Input mengubah state gameplay secara nyata — **PENDING**.
5. Gameplay/mekanik diuji — **PENDING**.
6. Story Mode tamat dengan bukti — **PENDING**.

**Langkah berikutnya:** pada boot baru yang sama, tekan Start frame 2.650/release 2.680, kemudian Circle/O frame 2.750/release 2.780. Capture rapat 2.649, 2.650, 2.660, 2.670, 2.680, 2.700, 2.720, 2.749, 2.750, 2.760, 2.770, 2.780, 2.790, 2.800 serta 2.850/2.900/2.950/2.999. Jika Mode Select muncul, identifikasi judul dan opsi sebenarnya sebelum input baru.

Pertahankan SCPH-7502 (EU), SLPS03553/`SLPS_035.53;1`, PCSX-Redux source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`, SoftGPU, Port 1 Analog/Auto. Raw BIOS/ROM/GPU dump tidak boleh diunggah; raw temporary files dihapus sebelum artifact privat tiga-hari diunggah.

## Pembaruan RT-001 — Start → menu terverifikasi; pilih mulai dari awal selanjutnya (2026-10-18)

Run [#39145309203](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39145309203) menyelesaikan target 3.000 VSync dan mengunggah artifact privat #12143433923. Screenshot framebuffer 640×480 menunjukkan title prompt pada frame 2.649/2.650, transisi kotak menu pada 2.660, lalu pilihan `はじめから` (panah berada di pilihan ini) dan `ロード` pada frame 2.670. Menu tetap tampil sampai frame 2.999. Start dipulse pada frame 2.650–2.680; tidak ada Circle atau tombol lain pada run ini.

**Acceptance status:**
1. Start benar-benar membuka menu pilihan — **PASS**, berdasar perubahan screenshot yang terjadi setelah Start.
2. `はじめから` berhasil dikonfirmasi — **PENDING**.
3. Story Mode dimulai — **PENDING**.
4. Input mengubah state gameplay di luar menu — **PENDING**.
5. Gameplay/mekanik diuji — **PENDING**.
6. Story Mode tamat dengan bukti — **PENDING**.

**Langkah tes berikutnya:** pertahankan BIOS SCPH-7502 (EU), disc SLPS03553 / `SLPS_035.53;1`, PCSX-Redux source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`, SoftGPU, Port 1 Analog/Auto, dan target VSync 3.000. Tekan Circle/O di frame 2.750 dan lepas di frame 2.780 saja. Capture 2.749–2.800 dengan jarak rapat lalu checkpoint 2.850/2.900/2.950/2.999. Mode Select hanya dianggap teridentifikasi jika tulisan opsinya terbaca pada bukti visual aktual. Jangan menekan tombol tambahan sampai transisi dibaca.

Bukti tetap privat dan minimum: hanya ringkasan teks dan screenshot; raw GPU dump/temp screenshot dihapus sebelum unggah. Artifact privat memiliki retensi 3 hari. RT-001 belum selesai dan Story Mode belum dimulai/tamat.

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
## BIOS compatibility investigation — 2026-10-18

- Candidate retail BIOS identified from a game-specific working setup: SCPH-7502 at [PSX Data Center](https://psxdatacenter.com/games/J/N/SLPS-03553.html), documented there for ePSXe 2.0. This is not yet tested on our pinned PCSX-Redux build.
- No retail BIOS binary is present in the current private release or Library inventory. Do not download a proprietary BIOS dump from unofficial sources or commit one.
- Extended legal available-BIOS comparison: [Actions #39093727808](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39093727808) adds `openbios-shell.bin` to the existing fastboot/chunked OpenBIOS sequence, same emulator and ROM/CUE. Inspect screenshot/OCR and input-effect evidence after completion.
- Full evidence and decisions: [docs/BIOS_COMPATIBILITY.md](BIOS_COMPATIBILITY.md). RT-001 remains Open / blocked until in-game visuals and responsive controller are verified.

## Status runtime terbaru — 2026-10-18

- Retest mandiri Mesa/GLX [#39085422680](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39085422680) lulus: default dan software sama-sama Mesa/llvmpipe, OpenGL 4.5 Compatibility Profile; explicit 3.3 compatibility context PASS tanpa version override. Artifact teks aman: [#12120801333](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39085422680/artifacts/12120801333).
- PCSX-Redux OpenGL backend nyata lulus sampai VSync 300 di [#39083372634](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39083372634): -openglgpu, Mesa/llvmpipe, emulator exit 0. GP0 43 words/42 commands; VRAM frame299 satu warna RGB555, 0 non-black piksel dari 524.288.
- Branch source categories [#39083850904](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39083850904): BNE 0x800372f0→0x80037320 (17 unequal; latest local writer load vs immediate arithmetic), BNE 0x80037330→0x800372d8 (15 unequal; special arithmetic vs zero). Kategori writer lokal bukan full provenance.
- Uji region alamat efektif load [#39084130154](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39084130154) selesai: 14 sampel load operand terkait BNE pertama diklasifikasikan `ram-cached`; artifact [#12119189221](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39084130154/artifacts/12119189221) berisi ringkasan saja.
- RT-001 tetap Open / blocked sampai gambar game/menu valid dan perubahan game state akibat input terverifikasi.


# Addendum 2026-10-17 — RSP minimal dan GPU-watchpoint

Run [#39017271906](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017271906) menyelesaikan probe register: PCSX-Redux AnyLinux GDB server default port 3333 menerima klien RSP minimal, negosiasi `qSupported` berhasil, lalu `p25` (PC), `p20` (CP0 Status), `p23` (BadVAddr), `p24` (Cause), dan `?` berhasil dibaca pada 10 sampel. Ini menghindari paket GDB modern yang tidak didukung source build ini. Nilai PC bervariasi di alamat BIOS dan rentang main EXE, tetapi sampel berkala tidak membuktikan jalur inisialisasi selesai. Window nyata PCSX tetap hitam pada semua capture termasuk setelah Return/Cross; RT-001 tidak berubah.

Eksperimen selanjutnya adalah [run #39017636267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017636267), yang menetapkan breakpoint entry EXE ketika emulasi paused sebelum `-run` dan mencoba write-watchpoint terarah pada GPU GP0/GP1 serta DMA2. Baca log final dahulu; hasil workflow ini masih in progress saat addendum ini dicatat. Tidak ada izin untuk mengubah RT-001 menjadi pass tanpa title/menu dan respons input nyata.

---

# Status terbaru 2026-10-17 — sesudah tes kontroler Analog

- Run [#38973267415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973267415) sukses. Port 1 disetel ke Analog, tersambung, dan di-remap sebelum boot.
- AnyLinux dan upstream HEAD sama-sama mengenali disc `SLPS-03553`, menyelesaikan pemuatan 187 sektor executable, mencapai `EXEC:PC0(80011448)` lalu `Execute !`. Peringatan `Unknown command for pad: 43` hilang pada kedua log; sebelumnya muncul pada keduanya di run baseline #38971848277.
- Ini mengonfirmasi koreksi protokol controller, tetapi **belum membuktikan** title/menu dan input in-game. Kedua tes headless tetap mencapai batas 90 detik.
- GUI probe baru ada pada workflow commit [85c08d9](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85c08d9ea255dc400c0771361abc95817a0a7ba6), run [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926). Pada saat catatan ini ditambahkan, run masih terlihat in progress; ambil log akhirnya untuk memeriksa dua frame pada detik 10 dan 20, metrik piksel, OCR Jepang/Inggris, dan penanda boot. Frame dan log GUI sementara dihapus oleh cleanup.

---

# Rencana uji runtime PS1

## Tujuan dan status

Emulator/debugger adalah jalur riset utama bersama analisis statis, bukan sekadar opsi terakhir. Gunakan runtime untuk memverifikasi nilai sebelum/sesudah aksi dan menguji cabang kode yang benar-benar berjalan. **Belum ada pengujian gameplay runtime terkontrol yang diselesaikan.** Lihat [EMULATOR_WORKFLOW.md](EMULATOR_WORKFLOW.md) untuk pilihan emulator dan prosedur yang lebih rinci.

Pada 2026-10-15, PCSX-Redux AppImage sudah dipaketkan ke release repo Naruto dan SHA-256-nya diverifikasi via GitHub Actions. GUI berhasil dijalankan pada layar virtual. OpenBIOS default sudah dibangun dan disimpan sebagai Release asset, tetapi uji dengan BIOS tersebut belum menghasilkan bukti visual bahwa game masuk ke menu/title. Workflow #38693918169 berhasil membangun varian shell/menu dan `BOOT_MODE=fast`. Uji lokal dengan `-bios openbios.bin -interpreter -debugger -iso game.cue -run` pada varian fastboot menghasilkan layar hitam setelah sekitar 12 detik; belum terkonfirmasi bahwa game mencapai title/menu. Gunakan asset release beserta checksum, lalu cari sebab boot tidak terlihat sebelum mengklaim runtime berhasil. Jangan meminta upload ulang ROM ~326 MB dari laptop.

## Persiapan

1. Prioritaskan PCSX-Redux untuk breakpoint CPU, memory editor, dan GDB server; lihat [EMULATOR_WORKFLOW.md](EMULATOR_WORKFLOW.md). Mednafen adalah alternatif untuk cek silang.
2. Gunakan image BIN/CUE dengan hash dari `docs/ROM_STRUCTURE.md`; jangan patch ROM asli. CUE harus merujuk file BIN yang sama dan track Mode 2/2352.
3. Catat versi/build emulator, jenis BIOS, setting CPU/interpreter/debugger, hash ROM, mode permainan, skenario, pemain aktif, aksi, nilai awal/akhir, PC breakpoint dan alamat RAM yang berubah.
4. Jalankan baseline dari state awal terkontrol. Untuk pengulangan, simpan state/memory card eksperimen di luar repo dan jangan menimpa save asli.
5. Jangan menganggap alamat overlay statis sebagai RAM live sebelum loader/base overlay dikonfirmasi. Mulai dari breakpoint executable utama dan verifikasi perubahan RAM.

## Variabel yang dipantau

- Empat struktur pemain yang diduga berstride 0xB4 dan field Chakra pada offset +0x18: verifikasi ulang di RAM setelah loader/overlay aktif.
- ID pemain aktif dan penghitung giliran.
- Field petak: owner bits, level/jenis, durability, nilai/harga, dan atribut yang belum dipetakan.
- Konfigurasi target/opsi skenario.
- ID kartu yang dipilih, ID jutsu, hasil roulette, keadaan battle, dan ID pemenang.

Alamat RAM yang diketahui dari static analysis harus diperlakukan sebagai breakpoint awal saja sampai overlay dan alokasi RAM diverifikasi.

## Matriks eksperimen

### A. Inisialisasi Story Stage 1

- Mulai stage pertama dari keadaan bersih.
- Catat Chakra setiap pemain sebelum dan sesudah inisialisasi.
- Temukan record konfigurasi yang dibaca saat stage dimulai.
- Konfirmasi hubungan field +0x04, +0x08, +0x0C dengan nilai awal, target, dan parameter lain.
- Pastikan siapa yang menang jika Chakra sama dengan target dan jika satu angka di bawah target; gunakan keadaan yang aman/reproducible.

### B. Membangun barrier

- Pilih petak kosong dengan saldo Chakra yang cukup.
- Catat saldo sebelum konfirmasi, saat transaksi, dan sesudah barrier muncul.
- Ulangi dengan tipe petak/skenario berbeda bila tersedia.
- Breakpoint pada setter Chakra serta rutin perubahan field petak.
- Temukan asal nilai biaya di register/memori, bukan hanya konstanta yang kebetulan terlihat di disassembly.
- Uji saldo tepat di bawah, sama dengan, dan di atas biaya yang terlihat di UI jika memungkinkan.

### C. Meningkatkan level barrier

- Mulai dari barrier level 1 yang nilai/durability awalnya dicatat.
- Catat saldo, level, nilai, dan durability sebelum/sesudah upgrade.
- Ulangi untuk level dan tipe barrier berbeda.
- Pisahkan biaya upgrade dari biaya bangun dan dari animasi/transisi UI.

### D. Pendapatan dan kunjungan ke petak

- Jalankan satu giliran yang melewati petak sendiri dan petak lawan dengan save state yang sama.
- Catat saldo masing-masing pemain sebelum/sesudah pendaratan dan akhir giliran.
- Uji apakah pendapatan datang pada pemilik, pengunjung, atau keduanya; apakah efek bergantung level/tipe/bonus.
- Ulangi tanpa lawan mendarat untuk mendapat baseline.

### E. Battle, damage, dan pengambilalihan barrier

- Siapkan pertarungan pada barrier musuh dengan kondisi karakter/jutsu yang dapat diulang.
- Catat saldo dan field barrier sebelum battle, di setiap titik damage, setelah menang/kalah.
- Uji jutsu berbeda dan karakter berbeda.
- Bandingkan kemenangan di wilayah tanpa barrier bila bisa dibuat.
- Pisahkan biaya untuk mulai menyerang, biaya jutsu, damage durability, transfer kepemilikan, dan hadiah setelah menang.

### F. Kartu

Untuk setiap kartu:
- Catat ID kartu dan ID handler yang dipanggil.
- Catat semua state sebelum/sesudah: Chakra, statistik, skip-turn/status, hasil roulette berikutnya, kepemilikan Scroll of Seals, serta penghitung.
- Untuk kartu yang memodifikasi beberapa roulette, uji kedua lemparan dan kapan efek habis.
- Uji batas maksimum/minimum dan cara pembulatan.
- Bandingkan hasil dengan transkripsi di docs/GAME_RULES.md dan dokumentasi komunitas.

### G. Kondisi kemenangan alternatif

- Temukan record/bit opsi yang dipilih lewat menu Party Mode.
- Untuk setiap opsi, lakukan satu test case positif (syarat terpenuhi) dan satu negatif (satu syarat tidak terpenuhi).
- Periksa kapan game menetapkan ID pemenang, kapan mengubah screen/state, dan arti field pemenang 0xFF.
- Uji target Chakra tanpa opsi tambahan dan target dengan opsi tambahan untuk melihat prioritas kondisi ketika beberapa syarat terpenuhi bersamaan.

## Format tabel hasil

| Test ID | Kondisi awal | Aksi | Nilai/state sebelum | Nilai/state sesudah | PC/overlay | Hasil | Status |
|---|---|---|---|---|---|---|---|
| RT-001 | Belum dijalankan | — | — | — | — | — | Open |

Setiap test harus dilengkapi screenshot atau log debugger dan, jika relevan, hash/save-state untuk reproduksi. Jangan menyebut formula “terbukti runtime” tanpa hasil yang bisa diulang.

## Kriteria selesai

- Loader/overlay aktif teridentifikasi untuk setiap breakpoint.
- Nilai biaya/pendapatan berasal dari field atau rumus yang terpetakan sampai pemanggilnya.
- Formula yang memiliki cabang berbeda dites pada sekurangnya satu contoh per cabang penting.
- Semua flag opsi kemenangan dapat dikaitkan dengan pilihan menu/data record dan hasil permainan.
- Hasil runtime sesuai analisis statis; bila berbeda, catat perbedaan dan revisi hipotesis.
- Laporan final membedakan aturan normal, variasi skenario, dan kondisi yang hanya tersedia setelah unlock.

## Status boot sebelum uji gameplay — pembaruan 2026-10-17

Jangan mulai test case gameplay RT-001 sampai title/menu yang dikenali benar-benar tampil dan input terbukti direspons.

### Fakta runtime yang sudah dikonfirmasi

- ROM private yang diuji terverifikasi dengan ukuran 325.989.552 byte dan SHA-256 `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`.
- OpenBIOS membaca disc `SLPS-03553`, membaca `SYSTEM.CNF` (`BOOT = cdrom:\\SLPS_035.53;1`), lalu loader menyelesaikan 187 chunk executable. Dalam tes headless, log mencatat `EXEC:PC0(80011448)` dan `Execute !`; ini membuktikan loader menyerahkan kendali ke alamat entry executable, bukan membuktikan menu sudah digambar.
- Peringatan `Unknown command for pad: 43` hilang untuk kedua build setelah Port 1 disetel `Analog`, `Connected=true`, dan di-remap melalui `PCSX.SIO0.slots[1].pads[1].map()`. Catatan pembanding: [Actions #38973267415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973267415).
- Callback penghitung `GPU::Vsync` dapat berjalan stabil sampai lebih dari 2.040 frame dan mencapai marker entry ketika tidak membaca register CPU: [Actions #38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602).

### Pertanyaan yang masih terbuka

- Capture GUI 10s/20s sebelumnya memang seluruhnya hitam, tetapi diambil sebelum titik executable entry (yang pada headless terjadi sekitar frame 1.620, kira-kira 27 detik pada laju sekitar 60 VSync/s). Jadi hasil awal itu **belum membuktikan layar akan terus hitam**.
- Tes GUI yang diperpanjang hingga frame 30s, 60s dan 90s sedang berjalan: [Actions #38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679). Hasil akhirnya perlu memeriksa metrik gambar dan OCR yang dihasilkan dari frame lokal yang dibersihkan saat cleanup.
- Kedua AppImage terkemas yang tersedia tidak memiliki Lua API `PCSX.CPU.Trace`; percobaan tersebut gagal sebelum trace dijalankan. Workflow sekarang membangun source PCSX-Redux pada commit upstream yang dipatok agar built-in trace tersedia: [Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756). Hasil build/trace belum terverifikasi.
- Pembacaan register CPU secara langsung dari callback VSync menyebabkan emulator berakhir dengan segfault pada eksperimen sebelumnya. Jangan memakai hasil trace itu untuk menyatakan bahwa game macet atau ROM rusak.

### Gate sebelum riset aturan main

1. Pastikan capture setelah entry menunjukkan title/menu Naruto yang benar-benar dikenali, bukan sekadar piksel non-hitam.
2. Uji input secara terkendali hanya setelah ada frame/menu yang dapat dikenali.
3. Baru setelah kedua gate tersebut terpenuhi, mulai test case biaya, income, battle, kartu, kepemilikan, dan kondisi kemenangan di bagian berikutnya.

---


## GUI probe result — 2026-10-17

Actions [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926): Xvfb root frames at 10s and 20s were both all-black (`1280x800`, mean 0, standard deviation 0, one color), and OCR returned no text. The GUI probe showed BIOS/disc/controller setup in logs but no `EXEC:PC0`/`Execute !` marker during 35s; do not interpret that as the same boot result as headless mode.

A separate no-UI CPU trace is now implemented in [workflow file](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/blob/main/.github/workflows/naruto-cpu-trace.yml) and running as [Actions #38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045). It logs the PC/RA/SP every 30 `GPU::Vsync` callbacks up to 600 frames. Use the final logs to determine whether frame callbacks occur and whether the guest PC changes; next step depends on that evidence.

---



## Cloud runner retest gate — updated 2026-10-17

The asset/entry test completed successfully in [run #38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679): private release retrieval, ROM size/hash, CUE validation, OpenBIOS and disc recognition, 187 executable chunks, and `EXEC:PC0(80011448)` / `Execute !` were logged. Analog Port 1 suppressed `Unknown command for pad: 43` in both compared builds.

The former GUI metrics are invalid for diagnosing game display because the script captured the Xvfb root, not the emulator window. The corrected probe in [run #39000276365](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365) must produce `CAPTURE_WINDOW` and measurements from that window; a missing window is itself a GUI-startup diagnostic, and the test must not substitute the root background.

The previous source-built CPU trace [run #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) failed before emulation because the host lacked `libcapstone.so.5`. The corrected workflow [run #39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) installs `libcapstone-dev` and verifies linked dependencies. Its final trace output is still required before diagnosing any guest loop or stall.

**Gate remains closed:** no title/menu identified and no controlled in-game input response yet. Keep test row RT-001 open. Do not start gameplay formula experiments until both observations are independently proven.


## GUI window retest — results and gate update (2026-10-17)

Actions #39000276365 captured the actual PCSX-Redux X11 window at 30s, 60s and 90s; all images were uniformly black by pixel statistics, OCR found no text. The GUI probe log did not show executable chunk completion or EXEC:PC0 / Execute !, unlike the headless -no-ui probes in the same job. Treat this as a GUI-vs-headless boot discrepancy; do not interpret the frames as game graphics after entry.

RT-001 remains Open / blocked. Next investigate why GUI-mode execution does not show the headless boot handoff; only after a recognizable title/menu and a controlled, responsive input are observed should Story Mode state-delta tests begin.


## Next diagnostic when GUI window is black — 2026-10-17

The prior run found a real PCSX-Redux window but did not reach the PAD_SETUP Lua marker or game executable entry in GUI mode. The next runner job [#39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307) reports GLX/renderer capability and full tail diagnostics from GUI stdout and emulator logs. Use its GUI-specific boot markers to distinguish UI initialization from a guest boot stall. The headless `EXEC:PC0` marker is separate evidence and cannot establish that the GUI has entered the game. RT-001 remains blocked until a visible Naruto title/menu and responsive input are evidenced.


---

## A/B emulator evidence and GUI gate — 2026-10-17

Matched headless evidence: [Actions #39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307). Both AnyLinux and the AppImage named PCSX-Redux-HEAD-x86_64.AppImage used the same ROM/CUE, chunked OpenBIOS, CPU interpreter/software GPU, Analog connected/remapped Port 1, and 90-second observation cap. Both reached 187 completed executable chunks, EXEC:PC0(80011448) and Execute !; neither logged Unknown command for pad: 43. These are headless handoff results, not title/menu or playable-input evidence.

GUI result from the same run is distinct: GLX returned Mesa llvmpipe/OpenGL 3.3, but the actual AnyLinux window was all-black at 30/60/90 seconds and OCR empty. Its GUI log did not show all chunks completed or executable entry. The latest workflow runs the same GUI probe against both AppImages; inspect [Actions #39002136781](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002136781) for each build's GUI_BOOT_RESULT, GUI_PAD_RESULT, FRAME_METRICS, OCR and cleanup.

CPU tracing is still in progress. Prior run [#39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) compiled pinned source commit 6b9df482d7b77b9ae218d9c48c1ce1a43c265206 but failed dependency preflight because FFmpeg/SDL libraries were available in the builder image but not on the host. Corrected workflow [commit 16a6faff](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/16a6faff066b913480ad121b497db79df03a9de2) checks and launches the binary inside the same digest-pinned container. Inspect [run #39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) for VSYNC_TRACE frame markers, CPU_TRACE_SIZE and CPU_TRACE_LINE rows.

**RT-001 remains blocked.** Do not test Story Mode or transactions until a recognizable Naruto title/menu appears in a GUI frame and a controlled, logged input visibly changes the game or a reliably identified input state.

## Status RT-001 setelah audit GUI A/B — 2026-10-17


## Verifikasi GUI A/B terbaru dan perbaikan harness — 2026-10-17

Run GUI A/B [#39002136781](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002136781) berstatus workflow `success`, tetapi **bukan hasil uji GUI yang berhasil**. Langkah headless di job yang sama tetap membuktikan kedua AppImage membaca disc `SLPS-03553`, menuntaskan 187 chunk executable, dan mencatat `EXEC:PC0(80011448)` serta `Execute !`; keduanya tidak lagi mencatat `Unknown command for pad: 43`. Saat masuk bagian GUI, `gui_probe.sh` berhenti untuk kedua build pada `PAD_SETUP: unbound variable` karena variabel shell tidak diekspor. Tidak ada jendela emulator yang ditemukan dan tidak ada frame yang ditangkap. Karena hasil probe tidak dipaksa menjadi kegagalan job, status `success` hanya berarti step berakhir tanpa kegagalan workflow yang terdeteksi; status itu bukan bukti GUI/game berhasil.

Perbaikan minimal sudah didorong ke runner pada commit [aac684d120ec025c4a87197da8d835f90b89f869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aac684d120ec025c4a87197da8d835f90b89f869): ekspor `PAD_SETUP` sebelum skrip probe GUI dipanggil. Rerun ROM privat [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) sudah dipicu dan masih `in_progress` pada pemeriksaan terakhir; hasil frame, OCR, boot-marker GUI, dan cleanup masih harus diperiksa dari log akhirnya.

CPU-trace run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) juga masih `in_progress`. Secret dan pengunduhan/verifikasi file privat telah dilewati; step source-build di container Docker yang dipatok digest masih berjalan, sedangkan capture trace dan cleanup belum dimulai. Belum ada `CPU_TRACE_SIZE` atau `CPU_TRACE_LINE` yang dapat dipakai untuk analisis.

Current upstream PCSX-Redux yang terverifikasi saat cek adalah [41f3196257d0962942b60983201aade951ebbd54](https://github.com/grumpycoders/pcsx-redux/commit/41f3196257d0962942b60983201aade951ebbd54) (2026-10-17 02:53:17 UTC). AppImage berlabel “HEAD” tetap build source 9c6f98a0, bukan upstream HEAD terkini. Tidak ada bukti bahwa judul/menu tampil atau input gameplay merespons; gate RT-001 tetap tertutup dan Story Mode tidak boleh dimulai.


## Hasil GUI A/B sesudah perbaikan harness — 2026-10-17

Run [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) sudah selesai. Job sukses tidak berarti seluruh kriteria GUI lulus.

- Headless A/B kedua AppImage lulus sampai `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, `Execute !`. `Unknown command for pad: 43` tidak muncul. Proses headless berakhir di batas observasi 90 detik (124).
- GUI AnyLinux: marker PAD_SETUP, BIOS, disc `SLPS-03553`, `SYSTEM.CNF` dan `BOOT` tampak. Window X11 emulator yang ditemukan (ID 2097204) benar-benar ditangkap pada 30/60/90 detik. Semua frame 1280×800 memiliki mean 0, stddev 0, satu warna; OCR kosong. GUI tidak memiliki marker selesai 187 chunk maupun executable entry. Exit 124 adalah batas observasi 100 detik.
- GUI build bernama “HEAD”: gagal membuat window dengan pesan `Unable to create main window: Couldn't find matching GLX visual`; SDL gagal membuat OpenGL 3.2 context dan mencoba profil 3.0. Tidak ada window/frame, PAD_SETUP atau executable entry. Exit 137 pada penanganan timeout bukan diagnosis crash guest.
- Cleanup sukses dan artifact list kosong; frame/log/media privat tetap tidak dipublikasikan.

**RT-001: Open / blocked.** Title/menu belum diidentifikasi dan belum ada demonstrasi input responsif. Tindakan selanjutnya: bandingkan log khusus GUI AnyLinux yang tidak mencapai executable handoff dengan headless `-no-ui`; pisahkan inisialisasi UI/GLX dari progres CD/loader/CPU/Lua. Jangan mulai tes Story Mode dahulu.

## CPU trace source-build: status run saat diperiksa — 2026-10-17

Run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) tetap aktif pada step build pinned source setelah file privat diverifikasi. Step capture trace dan cleanup belum dimulai; log archive belum dapat diunduh selama job berjalan (`BlobNotFound`). Batas workflow 45 menit. Pantau step aktif dan tunggu hasil aktual, tanpa run duplikat. Belum ada hasil CPU trace untuk frame 1620–1680.

## CPU trace source-build selesai — interpretasi dan gerbang berikutnya (2026-10-17)

Run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) berhasil menyelesaikan semua step: download/verifikasi, compile PCSX-Redux source `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` dalam builder image ter-patok, dependency check, CPU trace, dan cleanup. Build berjalan 04:17:26–04:43:46 UTC; trace berjalan 04:43:46–04:44:21; cleanup sukses. `PCSX_BUILD_RESULT` tercatat; pemeriksaan `ldd` tidak menemukan dependency `not found`. Run berakhir pada 04:44:27 UTC.

Hasil capture:
- `VSYNC_TRACE` mencapai frame 1620, 1650, 1680 lalu berlanjut setelah jendela trace; `CPU_TRACE_WINDOW=enabled frame=1620`.
- `CPU_TRACE_SIZE=16031631`; `TRACE_RESULT=VSync counter callbacks fired.`; `CPU_TRACE_RESULT=Built-in instruction records were printed.`.
- 80 record ekor memperlihatkan loop guest `0x000015a4–0x000015c4`: load `0x5de4(a3)` dibaca nol, dua cabang, decrement `$v1`, dan branch kembali ke `0x000015a4`. Penghitung menurun pada sampel, sehingga ada progres dalam loop; identitas flag/modul dan apakah loop berakhir belum diketahui.
- `TRACE_PROCESS_EXIT=124` adalah batas observasi 35 detik yang disengaja, bukan otomatis crash guest.
- Capture `-no-ui` ini tidak menampilkan SYSTEM.CNF/BOOT, `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, atau `Execute !`. Ini berbeda dari jalur headless dua AppImage pada GUI A/B yang mencapai entry. Jangan menyatakan source build/GUI berhasil boot hanya dari VSync atau status job.
- Tidak ada artefak Actions. Cleanup menyatakan ROM/CUE/BIOS, emulator dan trace logs temporer terhapus.

### Diagnosis berikutnya

Bandingkan log startup di source-build pinned dan AnyLinux headless pada titik BIOS/CD read, pemrosesan SYSTEM.CNF, loader/chunk, serta handoff executable. Tambahkan guest-PC sampling periodik atau window trace yang lebih akhir hanya jika diperlukan untuk menguji apakah loop berlanjut; jangan mengulang build yang sama tanpa meningkatkan observasi. Verifikasi alias RAM dan mapping overlay sebelum menamai pemilik PC rendah. Diagnosis GUI terpisah tetap diperlukan: run #39002846886 menunjukkan AnyLinux berhasil membuka window dan menjalankan PAD_SETUP, tetapi tidak mencatat entry; “HEAD” gagal membuat window akibat GLX/OpenGL.

**RT-001 tetap Open / blocked:** jangan mulai Story Mode sampai title/menu dikenali dan respons input terkontrol benar-benar terbukti.

## Isolasi beda versi emulator dan lama observasi — 2026-10-17

Source yang dipakai AnyLinux (`0c3572c3db75f97542001e453ae80ba8c3f8acba`) berbeda 803 commit dari source CPU-trace (`6b9df482d7b77b9ae218d9c48c1ce1a43c265206`). GitHub compare menyorot perubahan besar `src/core/cdrom.cc` (+1.476/-1.392), `src/core/psxinterpreter.cc` (+290/-81), `src/core/pad.cc` dan `src/core/psxmem.cc`; kode branch interpreter berubah untuk mengelola delay slot. Ini hanya calon area inspeksi, bukan akar masalah terverifikasi.

Kedua perintah headless menggunakan `-interpreter`, tetapi AppImage diuji sampai 90s sementara source-trace proses dibatasi 35s. Karena itu absennya EXEC:PC0 di trace run tidak cukup untuk menyatakan regresi/boot gagal. Uji follow-up yang paling diskriminatif:
1. Ulangi source pinned dengan batas 90s; cetak `PCSX.getRegisters().pc` tiap 30 VSync sepanjang run.
2. Capture trace frames 4500–4560 agar PC sesudah periode 35s dapat diperiksa.
3. Cetak boot markers (BIOS/CD label/SYSTEM.CNF/chunk/EXEC) secara terpisah dari tail instruction trace; jangan biarkan 160+ VSync/trace lines memotong marker awal.
4. Bandingkan jalur CD-ROM dan branch/delay-slot interpreter pada source lama/baru setelah data sebanding tersedia.

Tidak ada perubahan ROM/BIOS atau rerun baru dalam pembaruan ini. RT-001 tetap Open / blocked; title/menu dan input terkontrol belum dibuktikan.

## Hasil CPU trace 90 detik — Actions #39004736399 (2026-10-17)

Run [#39004736399](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39004736399) selesai `success`; seluruh step download/verifikasi, build, capture, dan cleanup sukses. Build source pin `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` dan dependency preflight pada builder digest tetap tidak menemukan library `not found`. ROM lolos verifikasi ukuran/hash dan CUE sementara lolos validasi struktur.

| Kriteria | Hasil | Makna |
|---|---|---|
| Boot setup | OpenBIOS terdeteksi; disc `SLPS-03553`, ID `SLPS03553`, EXE `SLPS_035.53;1` | BIOS dan media dikenali |
| Guest PC sampling | 158 sampel frame 30–4740; 157 kali `0x000015a4`, satu kali `0x00000870` di frame 420 | PC kembali ke loop alamat rendah setelah satu sampel yang berbeda |
| Trace awal (1620–1680) | 200 records sampel, 9 PC unik, total 16.031.631 | Pola hot PC berada di sekitar `0x000015a4–0x000015c4` |
| Trace akhir (4500–4560) | 200 records sampel, 9 PC unik, total 16.031.484 | Pola yang sama masih ada mendekati akhir observasi |
| Handoff executable | Tidak ada SYSTEM.CNF/BOOT, 187 chunk selesai, EXEC:PC0, atau Execute ! | Entry executable game tidak terbukti |
| Batas proses | Exit 124 pada batas 90 detik | Timeout observasi yang disengaja; bukan bukti crash |
| Kebersihan | Cleanup sukses; artifact list kosong; tidak ada instruksi/operand mentah pada output runtime baru | File privat tidak diterbitkan sebagai artefak |

**Tafsiran:** ini bukan keberhasilan RT-001. Pencapaian VSync dan summary trace menunjukkan emulator tetap menjalankan callback, sementara guest PC terus berulang pada alamat rendah. Asal loop dan penyebabnya belum terbukti; jangan menggolongkannya sebagai BIOS/game code tertentu tanpa pemetaan tambahan. Gunakan diagnosis source/loader dan marker progres CD sebagai langkah berikut, bukan mengulang tes identik.

**Gerbang RT-001 tetap Open / blocked:** wajib ada title/menu Naruto yang dikenali dan demonstrasi respons terhadap input terkontrol sebelum pengujian Story Mode. Jangan menyatakan gameplay berhasil hanya dari `success` di Actions.

## Perubahan status runtime — 2026-10-17, setelah tes capture internal

Run privat [#39011515345](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011515345) mencapai marker `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, dan `Execute !` pada jalur `-no-ui`. Usaha screenshot melalui `PCSX.GPU.takeScreenShot()` mengembalikan dimensi 0×0 dan bpp 0, jadi konversi/capture tidak valid; cleanup selesai, artifact list kosong. Jangan gunakan API tersebut sebagai bukti tampilan pada mode `-no-ui`.

Run privat [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) dibuka untuk membangun source PCSX-Redux pin current upstream `1525a93676dbece9fe70f10ff129aeaa14eec30d` lalu menguji jalur GUI nyata pada Xvfb dengan capture jendela tiap interval. Status pada saat pembaruan ini belum selesai; periksa log, boot markers, metrik frame, OCR dan artefak privat setelah berakhir. Sumber PIN/build dicatat di workflow. Jangan menampilkan atau mengunggah screenshot di runner publik.

Penghapusan log publik lama telah terverifikasi: cleanup run #39011611436 sukses menghapus spesifik run #39001985849, dan API GET berikutnya memberi 404.

**Gerbang RT-001 tetap Open / blocked:** title/menu yang dikenali dan respons input terkontrol wajib dibuktikan sebelum memulai Story Mode. Belum ada sesi Story Mode terverifikasi.

## Uji emulator alternatif tambahan — 2026-10-17

Workflow privat [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) kini menguji rilis DuckStation resmi, dengan AppImage SHA-256 `c5e6f045f6a242082fcafa9f02d56ad895e233b942728788d232ad0c0c765c24`, ROM yang sama dan OpenBIOS `openbios.bin` dari private release. Harness Xvfb mengambil frame jendela dan mengirim Return/Cross lewat pemetaan keyboard sementara, lalu menyimpan capture sebagai artifact privat 3 hari dan menghapus workspace. Status saat catatan ini dibuat: queued; belum ada hasil boot/menu/input yang bisa disimpulkan. Ini uji kandidat, bukan klaim kompatibilitas.



## Hasil aktual DuckStation probe dan retest dependensi — 2026-10-17

Run [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) berakhir sebagai workflow `success` tetapi emulator tidak pernah start: error `libOpenGL.so.0` hilang, tidak ada window/frame OCR, dan input keyboard dilewati. Artifact ZIP 293 byte hanya berisi stdout 183 byte, tanpa PNG. Ini **bukan** hasil negatif kompatibilitas game; tes gagal pada dependensi host sebelum boot BIOS/disc.

Workflow telah dikoreksi di commit `058aadea1c664712b62a63cf01fcb3e5598ef047` untuk memasang `libopengl0 libglx0 libgl1` dan mengunggah pola capture yang benar `captures/*.png`. Rerun [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) sedang berlangsung ketika diperiksa. Run source-current PCSX-Redux [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) juga masih membangun source dan belum menghasilkan evidence GUI.

### Gerbang tetap
1. Periksa hasil final kedua run, bukan status awal maupun conclusion Actions saja.
2. Bila window DuckStation muncul, periksa OCR/frame dan log BIOS/CD; input synthetic hanya dianggap terkirim jika window benar-benar ditemukan dan UI/game berubah.
3. Nyatakan boot hanya jika title/menu Naruto dikenali pada capture. Nyatakan kontrol bekerja hanya setelah perubahan layar/game state dapat diatribusikan ke input.
4. Pertahankan RT-001 Open / blocked hingga kedua gerbang itu lolos. Story Mode, persistensi progres, dan aturan gameplay tetap belum diuji.


## DuckStation retest dependency status — 2026-10-17

Run [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) keluar dengan 127 karena `libEGL.so.1` masih hilang setelah pemasangan OpenGL/GLX. Window tidak ditemukan dan input dilewati; tidak ada frame untuk menilai game. Ini bukan gagal boot ROM karena emulator belum mulai.

Commit `5afd32eca0d32ee191de7f2963f74b53aed89448` menambah `libegl1`; rerun [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) masih berjalan pada boot/capture ketika dicatat. Periksa log dan artifact setelah selesai. PCSX source-current [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih di tahap build. RT-001 tetap Open / blocked sampai title/menu dikenal dan input terbukti responsif.


## Hasil final DuckStation probe — setup wizard, BIOS gate belum lolos (2026-10-17)

Run [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) kini membuka window 760×498 setelah `libegl1` dipasang. Capture privat menunjukkan setup wizard DuckStation, bukan title/menu Naruto. Halaman BIOS menjelaskan bahwa BIOS PS1/PS2 dibutuhkan; satu file terdeteksi tetapi tidak dinilai valid. Tidak ada marker disc/EXE di runtime log. Tombol Return bergerak dalam wizard, sehingga bukan bukti input ke game; Z/Cross juga belum diuji terhadap game state.

Kriteria RT-001 belum dipenuhi. Jangan meminta atau mengambil BIOS retail baru. DuckStation bukan jalur runtime yang dapat dilanjutkan dengan asset OpenBIOS sekarang. Prioritaskan hasil akhir source-current PCSX-Redux [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708); saat terakhir diperiksa masih pada tahap build. Jangan menyebut Story Mode berjalan/tamat.


## Hasil terbaru — source-current GUI dan BIOS variants (2026-10-17)

- [Source-current PCSX-Redux #39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708): source pin berhasil dibangun. Capture window 20/40/60/80/95 s semua hitam uniform 1280×800 (mean 0/stddev 0/satu warna), OCR kosong. Log mengenali disc/OpenBIOS/Analog port, tetapi guest PC hanya tercatat sekali pada frame 300=`0x000015a4`; tidak ada `SYSTEM.CNF`/BOOT atau executable entry. Ini bukan sukses RT-001.
- [OpenBIOS A/B #39013612865](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39013612865): fastboot OpenBIOS mencapai `EXEC:PC0(80011448)`/ `Execute !`; chunked OpenBIOS hanya mencatat payload read sampai indeks 40. Namun window detector tidak menemukan jendela untuk kedua varian sehingga capture/input dilewati.
- [Follow-up fastboot window-identification #39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) memakai enumerasi X11 semua jendela yang terlihat, memilih jendela aplikasi berukuran wajar, menyimpan window tree saat pencarian gagal, lalu capture/OCR sebelum/sesudah input. Status awal queued; hasil final perlu dinilai dari log/capture.

**RT-001 tetap Open / blocked.** EXEC handoff tidak menggantikan title/menu yang terlihat; input hanya tervalidasi bila perubahan game dapat diamati.


## Fastboot entry dengan capture window generik — 2026-10-17

Run [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) membuktikan bahwa jendela sebenarnya dapat ditemukan bila enumerasi X11 generik digunakan (ID 543). Fastboot BIOS mencapai entry executable, tetapi setiap capture window 1280×800—sebelum/sesudah Return dan Cross serta pada 40/65/90 detik—tetap satu warna hitam; OCR kosong. Input dikirim ke window, tetapi tidak ada perubahan tampilan yang dapat dikaitkan ke game. Jadi RT-001 belum lolos.
Follow-up [#39015290594](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015290594) membuang `PCSX.getRegisters()` dari callback VSync untuk menguji kemungkinan instrumentasi membekukan emulator. Bandingkan frame, marker BOOT dan input sebelum menyimpulkan root cause.


## Koreksi wajib — fastboot selector menangkap root Xvfb (2026-10-17)

Capture run [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) **tidak sah untuk menilai gambar game**. ID 543 = hexadecimal `0x21f` ialah root Xvfb; regex `xdotool search --onlyvisible --name '.*'` mencocokkan root. Jadi frame hitam, OCR kosong, dan tak adanya delta visual Return/Cross dari run tersebut tidak boleh dianggap sebagai observasi window PCSX. Marker fastboot `SYSTEM.CNF`/BOOT/`EXEC:PC0`/ `Execute !` tetap sah dari log terpisah.
Workflow diperbaiki pada commit `83173bb10cfbf905a296f59720c0a63c95bc3a32` dengan pengecualian eksplisit X11 root. Nilai hasil run [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649) hanya boleh dipakai jika `CAPTURE_WINDOW` menyebut ID non-root. Jika tidak ditemukan, root tree adalah diagnosis dan tidak boleh diganti dengan gambar root. RT-001 tetap Open / blocked.


## Koreksi pemilihan window kedua — fastboot tree audit (2026-10-17)

Pada [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649), root Xvfb sudah dikecualikan tetapi selector `xdotool search` tidak memberi child window sebagai kandidat. Root tree menunjukkan child `0x200034 "PCSX-Redux"` 1280×800. Karena capture tidak dilakukan, tidak boleh menyatakan aplikasi tak punya window ataupun bahwa game tampil hitam. Boot markers fastboot sah secara terpisah: SYSTEM.CNF, BOOT, EXEC:PC0, Execute!.
Workflow terbaru [#39015610296](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015610296) mengekstrak XID langsung dari root tree, mengecualikan root, serta memfokuskan window sebelum input. Validasi RT-001 membutuhkan `CAPTURE_WINDOW` atas child non-root dan screenshot/OCR game yang dapat diidentifikasi.


## Hasil fastboot dengan frame non-root yang valid — 2026-10-17

Run [#39015722771](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015722771) sukses mengambil jendela PCSX-Redux yang nyata (`0x200034`/2097204, 1280×800) melalui tree X11 dan secara eksplisit melewati root `0x21f`. Frame sebelum input, sesudah Return/Cross, dan 40/65/90s semuanya uniform black; OCR kosong. Tidak ada pembacaan register CPU di event VSync. Port 1 Analog diset dan tombol dikirim; tidak ada perubahan visual yang dapat dibuktikan. Boot mencapai SYSTEM.CNF/BOOT/EXEC:PC0/Execute!, namun title/menu belum tampil.
Run berikut [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) membandingkan backend OpenGL default melawan `-softgpu` di Mesa llvmpipe 3.3. Ini perubahan renderer saja; gunakan frame aktual serta error GL untuk menentukan langkah selanjutnya. RT-001 tetap Open / blocked.


## Hasil renderer A/B final — 2026-10-17

Run [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) mempertahankan fastboot OpenBIOS, ROM, AnyLinux emulator, dan Port 1 Analog; hanya `-softgpu` yang dihapus. Mesa llvmpipe OpenGL 3.3 Compatibility Profile tersedia. Jendela PCSX-Redux non-root `0x200034`/2097204 ditangkap sah; frame sebelum/sesudah Return dan Cross serta pada 40/65/90s semuanya uniform black dan OCR kosong. Log terpisah tetap mencapai `EXEC:PC0(80011448)`/ `Execute !`. Tidak ada CPU-register read di callback VSync. Peralihan renderer bukan solusi.
Langkah diagnostik berikut: ambil snapshot PC melalui GDB remote dari luar emulator pada beberapa titik waktu, dengan hanya alamat PC/status stop yang diringkas; jangan menerbitkan trace instruksi mentah. RT-001 tetap Open / blocked.


## Tes PC snapshot pasca-entry — sedang berjalan (2026-10-17)

Workflow [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234) telah dimulai untuk mengambil PC melalui GDB remote eksternal, dengan fastboot BIOS/ROM/controller yang sama dan capture non-root yang sama. Output dibatasi ke snapshot PC; tidak mengambil register dari callback VSync atau merekam instruksi mentah. Saat pemeriksaan terakhir job masih memasang GDB; hasil belum tersedia. Gunakan snapshot PC, boot markers dan frame/OCR bersama-sama untuk menentukan langkah berikut. RT-001 tetap Open / blocked.


## Keputusan jalur utama dan GDB probe — 2026-10-17

**Jalur utama berikutnya: PCSX-Redux AnyLinux prebuilt + OpenBIOS fastboot.** Bukti pemilih: log loader mencapai `SYSTEM.CNF`, BOOT, `EXEC:PC0(80011448)`, `Execute !`; varian chunked tertahan sebelum entry dalam window uji; DuckStation terblokir sebelum boot disc karena OpenBIOS tidak diterima wizard BIOS-nya.
GDB run [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234) selesai sukses dari sisi workflow, tetapi snapshot PC eksternal tidak tersedia (t20/t30/t50/t70 exit 1; t90 exit 124 timeout). Frame jendela aplikasi non-root tetap uniform black di 20/30/50/70 detik dan sesudah input, OCR kosong. Jadi belum ada title/menu atau perubahan state gameplay yang terbukti.
Eksperimen berikut tetap di fastboot AnyLinux dan menargetkan diagnosis setelah `EXEC:PC0`. Jangan menandai RT-001 lulus sebelum title/menu bisa dikenali dan respons input nyata terlihat. Story Mode belum dimulai.



## Pembaruan — hasil OpenGL mandiri dan diagnosis screenshot 0×0 (2026-10-17)

- Workflow [naruto-opengl-diagnostic.yml](../.github/workflows/naruto-opengl-diagnostic.yml), run [#39049689832](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39049689832), berhasil pada `ubuntu-26.04`: GLX default dan `LIBGL_ALWAYS_SOFTWARE=1` aktif, renderer `llvmpipe (LLVM 21.1.8, 256 bits)`, Mesa 26.0.8, OpenGL Core/Compatibility Profile 4.5. Tanpa `MESA_GL_VERSION_OVERRIDE` atau `MESA_GLSL_VERSION_OVERRIDE`, konteks compatibility 3.3 dapat dibuat; versi aktual yang dilaporkan 4.5.
- Maka lapisan GLX/Mesa software rendering sudah dibuktikan berfungsi. Jangan ulangi diagnosis backend grafis atau mengasumsikan GPU fisik dibutuhkan tanpa bukti lain.
- Source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`: `src/gpu/soft/gpu.cc` menghitung screenshot dari register batas display PS1 (`DisplayEnd - DisplayPosition`), sehingga ukuran 0×0 konsisten dengan batas display belum disiapkan. `src/core/pcsxlua.cc` juga mengikat `PCSX.GPU.getVRAM()`; ambil snapshot VRAM 1024×512 setelah VSync, tanpa menyimpan/mengunggah raw VRAM. Konversi lokal di runner ke gambar PNG pada artifact Actions privat untuk inspeksi, dan hapus raw file sebelum upload.
- Run capture [#39047765424](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39047765424) menghasilkan `NO_VALID_GPU_SCREENSHOTS`, dimensi 0×0, dan timeout emulator 90 detik (124). Itu bukan bukti boot game. RT-001 masih terblokir; title/menu, input yang mengubah state, serta Story Mode belum terverifikasi.


## Pembaruan rencana — pembacaan VRAM setelah handoff (2026-10-18)

- Jangan memakai `PCSX.nextTick()` sebagai timer rekursif. Pada pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`, implementasi menulis callback ke `AfterPollingCleanup`; `UI::tick()` menghapus field itu sesudah callback dipanggil. Callback lanjutan bisa hilang.
- Snapshot langsung pada GPU::Vsync mengonfirmasi API `PCSX.GPU.getVRAM()` dapat mengembalikan 1 MiB, tetapi sembilan frame 1–60 semuanya satu warna hitam dengan `guest_fps=0`. Log menunjukkan `Execute !` terjadi setelah checkpoint frame 60 dan event VSync frame 300 sesudahnya; jangan memakai checkpoint pra-handoff sebagai bukti keadaan game sesudah launch.
- Capture grafis di event callback perlu didefer ke thread UI/konteks OpenGL dengan `PCSX.nextTick()`. Hindari callback membaca VRAM/screenshot langsung pada thread event GPU. Run [#39078732160](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078732160) menguji capture deferred pada frame 1 dan 60; periksa log/artifact final sebelum menyimpulkan.
- Setelah pemeriksaan thread UI tervalidasi, ambil snapshot tambahan pada VSync pasca-handoff (sekitar frame 300) dan bandingkan dengan pra-handoff. Semua data mentah harus dihapus sebelum artifact privat diunggah.


## Temuan layar hitam dan traffic GPU — 2026-10-18

OpenGL host sudah dibuktikan sehat oleh run #39049689832: renderer llvmpipe, GL 4.5 tanpa override, explicit GLX compatibility context 3.3 lulus. Pada source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`, fungsi screenshot belum diimplementasikan untuk backend OpenGL GPU, sedangkan Software GPU memilikinya. Dengan `-softgpu`, capture setelah handoff di frame 300 menghasilkan screenshot 320×240 valid tetapi hitam seragam; VRAM tetap satu warna. Enam capture eksternal jendela PCSX non-root juga valid 1280×800 dan hitam seragam.

GPUDump partial run #39079279565 parsed lengkap sampai 136 VSyncs live: GP0 packets/words 0/0, GP1 1/1, VSync 136 packets/272 words; not truncated. Baseline upload yang mendahului TraceBegin mencakup full VRAM upload dan tidak boleh ditafsirkan sebagai drawing game. GPUDump mentah dihapus; hanya ringkasan teks privat yang diunggah. Run #39079291837 (target VSync 300) masih perlu diperiksa sebelum klaim data full-window.

Prioritas berikut: korelasikan PC/CP0 dan marker loader pada jendela waktu yang sama. Jangan mengganti emulator atau menyimpulkan GPU fisik dibutuhkan; jangan tandai RT-001 complete sampai title/menu dan perubahan akibat input teramati.


## Hasil final GPU traffic dan pengujian korelasi CPU (2026-10-18)

Run penuh [#39079291837](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079291837) selesai workflow-success tetapi emulator mencapai timeout (exit 124). Boot markers mencakup SYSTEM.CNF, BOOT path, EXEC:PC0 dan Execute !. GPU dump diparse lengkap/not truncated sampai 268 live VSyncs: GP0 packets/words 0/0, GP1 packets/words 1/1, VSync 268 packets/536 words. Pretrace GP0 baseline 262153 words merupakan full VRAM upload untuk state awal GPUDump, bukan output game. Dump mentah dihapus dan tak diunggah.

Workflow kini juga mengambil bulk RSP register `g` per interval, meringkas PC dan CP0 Status/BadVAddr/Cause, serta merekam timestamp marker loader pada run yang sama tanpa trace instruksi mentah. Run konfirmasi [#39079600379](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079600379) terakhir terlihat pending. Periksa hasil final; gunakan korelasi tersebut untuk memilih probe CPU berikutnya. GL host tak lagi jadi hipotesis utama. RT-001 tetap blocked.


## Korelasi CPU/GPU yang sudah tervalidasi — 2026-10-18, run #39079981314

Run [#39079981314](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079981314) mencapai VSync 300 lalu keluar normal. GPUDump valid/tidak terpotong; pasca-TraceBegin ada 299 VSync packets, 43 GP0 words (8 packets), 16 GP1 words (11 packets), dan 5 ThrowAway words. Parser command-family mengonsumsi seluruh GP0 stream tanpa sisa: 39 GPU state commands, 1 clear-cache, 1 monochrome rectangle, 1 NOP; tidak terlihat keluarga triangle/quad/line/textured sprite pada jendela ini. Pretrace GP0 262153 words merupakan baseline reset/full-VRAM upload.

RSP mengembalikan 76 sampel bulk valid. Log marker dibaca dari `pcsx.log` yang timestamp-nya line-buffered: `Execute !` sekitar t=38.01s; sampel PC masuk executable utama pada 38.33–40.91s, lalu sampel kembali dominan di BIOS mulai 42.20s. PC muncul lagi pada executable sekitar 88.39s dan tetap di dua alamat sekitar `0x800372d8/0x80037320` sampai akhir jendela. Ini bukan bukti exception root cause; Cause biasanya 0x400 (interrupt pending), sedangkan dua sampel 0x20 perlu dianalisis terpisah.

Berikutnya, tambahkan bucket waktu GP0 berdasarkan jumlah VSync yang telah lewat (mis. 0–49, 50–99, 100–199, 200–299) dan simpan hanya hitungan command family per bucket, bukan isi words. Tujuannya memastikan apakah satu monochrome rectangle dan state commands seluruhnya muncul saat startup sebelum guest CPU kembali ke BIOS. RT-001 tetap blocked sampai title/menu plus respons input teramati.


## Hasil bucket GP0 per VSync dan probe kontrol-alur berikutnya — 2026-10-18

Run #39080239541 mem-parse dump penuh/tidak terpotong sampai VSync 300. GP0 commands hanya muncul di bin live VSync 200–299 (43 words/42 commands), sementara bin 0–49, 50–99, 100–199 semuanya nol. Decoded family: 39 state setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP; tidak ada triangle/quad/line/textured sprite. GP1 16 words, ThrowAway 5 words. Raw dump dihapus sebelum upload.

Dalam run yang sama, marker Execute ! ~38.01s; PC masuk main EXE sekitar 38.33–40.91s, kembali ke BIOS sekitar 42.20–87.09s, lalu kembali ke EXE pada 88.39–98.63s. Semua GP0 output berada di bucket VSync akhir 200–299, jadi timing ini konsisten dengan PC sampel akhir yang masuk EXE lagi. Jangan menyatakan akar sebab masih terbukti.

Lanjutkan dengan sampling privat instruction window pada alamat PC executable yang sudah teramati, lalu ekspor hanya statistik kategori instruksi (branch/jump/syscall/load-store/COP0/backward branches), bukan bytes/instruction operands. Tujuan membedakan loop wait/kembali BIOS dari jalur yang meneruskan startup. RT-001 tetap blocked.


## Hasil code-window summary dan target sampler CPU lebih rapat — 2026-10-18

Run [#39080987461](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080987461) sukses sampai VSync300, RSP qSupported sukses, 75 bulk register samples valid. Sampel PC masuk EXE di sekitar t=37–38s, kembali ke BIOS t=40–87.73s, lalu PC berulang di 0x80037320 dan 0x800372d8 t=89–98.62s.

Empat jendela 64-byte berhasil dibaca, hanya statistik kategori:
- 0x80050b00: branches/jumps 0, loads 2, stores 6.
- 0x8003c080: conditional branches 2 (forward=2), jumps 4.
- 0x80037300: conditional branches 1, backward branches 1, jumps 3.
- 0x800372c0: conditional branches 2 (forward=2), jumps 1.
Tidak ada syscall/break/COP0/COP2 dalam empat jendela. Jangan simpulkan branch statis dieksekusi. GP0 tetap 43 words semua pada VSync bin 200–299; family hanya 39 GPU-state-setting, 1 clear-cache, 1 monochrome rectangle dan 1 NOP. Screenshot tetap hitam.

Berikutnya, sampling PC/CP0 lebih rapat hanya selama PC berada di 0x800372c0–0x800373ff, mempertahankan keluaran statistik saja. Tujuan melihat apakah perpindahan antar-PC menunjukkan loop yang stabil atau transisi singkat. RT-001 tetap blocked.
