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
