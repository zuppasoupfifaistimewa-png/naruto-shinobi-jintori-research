# Eksperimen kelanjutan setelah konfirmasi Circle — 21 Oktober 2026

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
