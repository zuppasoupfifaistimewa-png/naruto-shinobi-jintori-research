## Update GDB dan roundtrip native — 19 Oktober 2026

- [Run #39248501957](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39248501957) mengulang A/B/C/C2 dan menjalankan tahap D di bawah GDB. Log D membuktikan `SAVESTATE_PROBE_LOAD_CALL_BEGIN=1`, lalu thread 15 (`pcsx-redux`) menerima SIGSEGV pada PC `0x00007ffff0dd36d0`. Stack teratas `#0 0x00007ffff0dd36d0`, `#1 0x0000000001589a80`, `#2 0x00000000014f49f0`, `#3 0x00007ffff0de5870`. Nilai PC dan stack cocok dengan GDB lama #39235079514. Binary stripped; alamat ini belum bisa dipetakan ke nama fungsi.
- Trace lama #39235079514 pada PC yang sama mencatat `RSI=0xffffffffddd13fff` dan instruksi `movzbl (%rsi),%ecx`, yaitu pembacaan byte dari alamat invalid. Ini memperkuat bahwa jalur native/JIT crash dengan pointer invalid, tetapi belum menentukan field state atau fungsi penyebab.
- Artifak #12184890672 berisi log GDB dan ringkasan; retensi sampai 26 Oktober 2026.
- Capture GPU pada VSync awal di A/B/C/C2 menghasilkan `width=0,height=0`, raw 0 byte; screenshot itu tidak valid sebagai bukti visual.
- Run [#39249046252](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39249046252) menambahkan kontrol independen: buat savestate mentah dengan serializer emulator, lalu coba muat file mentah tanpa sanitasi/rehidrasi. Status terakhir yang diperiksa: masih berjalan pada langkah eksperimen. Periksa hasil A/B/C/C2/D/E/F setelah selesai sebelum menentukan langkah berikutnya.

---

# Diagnostik pemulihan savestate — 19 Oktober 2026

## Status ringkas

Prioritas riset tetap memperbaiki savestate sampai terbukti memulihkan keadaan permainan di tengah Story Mode. Belum ada restore yang berhasil dibuktikan. Tidak ada input gameplay yang dikirim selama pengujian diagnostik ini.

Run Story Mode terbaru yang diperiksa, [#39242130783](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39242130783), berakhir gagal dengan exit 124 sebelum gerbang visual frame 5999. Artifact checkpoint dari run tersebut tidak berisi `storymode-checkpoint.sstate`; file itu tidak boleh dipakai sebagai checkpoint baru.

Checkpoint sumber yang masih berguna berasal dari artifact privat [#12167524755](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39205699071):
- Ukuran: 20.638.254 byte
- SHA-256: `6365f18e2ad4531698976932a7d1dacc8834a47beba24e6c65d6d7d8e67a7223`
- File memuat savestate tersanitasi, tetapi **belum terbukti dapat dipulihkan**.

Memory Card referensi dari run #39242130783:
- Ukuran: 131.072 byte
- SHA-256: `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`
- Hash/ukuran file benar, namun save game nyata di dalam kartu tetap belum terverifikasi.

## Eksperimen terisolasi

Run [#39248081546](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39248081546) menguji sumber checkpoint lama dengan urutan berikut:

| Tahap | Intervensi | Hasil |
|---|---|---|
| A | Cold boot, tanpa file state, tanpa input | LULUS |
| B | File state tersanitasi tersedia, loader tidak dipanggil | LULUS |
| C | Field BIOS direhidrasi ke state, loader tidak dipanggil | LULUS |
| C2 | BIOS sudah direhidrasi; listener `ExecutionFlow::SaveStateLoaded` dipasang; loader tidak dipanggil | LULUS |
| D | Panggil loader savestate pada `nextTick` setelah VSync pertama dan pause emulator | GAGAL, exit 139 / SIGSEGV |

Pada D, log menampilkan `SAVESTATE_PROBE_LOAD_CALL_BEGIN=1`, kemudian proses segfault sebelum `SAVESTATE_PROBE_LOAD_CALL_RETURNED=1`. Berarti crash terlokalisasi pada pemanggilan `PCSX.loadSaveState()` atau kode native yang dijalankannya. Listener saja, file state, dan langkah rehidrasi BIOS tidak mereproduksi crash. Namun, pemulihan state sendiri tidak terjadi dan belum ada bukti visual pascarestore.

Artifact bukti privat run #39248081546: [download di GitHub](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39248081546/artifacts/12184920452). Retensi tercatat sampai 26 Oktober 2026.

## Keterbatasan bukti visual

Pada A/B/C/C2, `PCSX.GPU.takeScreenShot()` menghasilkan metadata `width=0`, `height=0` dan raw capture berukuran 0 byte pada VSync ke-60. PNG diagnostik tersebut tidak valid dan tidak boleh dianggap sebagai bukti visual. Screenshot harus diambil pada keadaan tampilan game yang sudah terinisialisasi, kemudian diverifikasi memiliki dimensi dan ukuran data yang masuk akal.

## Pekerjaan berikutnya

1. [Run GDB #39248501957](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39248501957) menjalankan A/B/C/C2 sebagai kontrol yang sama, tetapi hanya menjalankan tahap D di bawah GDB. Ambil native backtrace tepat saat SIGSEGV. Saat catatan ini disusun, run ini masih berjalan.
2. Berdasarkan backtrace, ubah satu faktor saja. Jangan menganggap penyebabnya sebagai bug protobuf/serializer atau fungsi tertentu sampai stack mendukungnya.
3. Setelah perbaikan native load, buktikan semuanya sekaligus: pemanggilan loader kembali tanpa crash, event/state loaded tercatat, emulator menghasilkan setidaknya 180 VSync pascarestore, dan screenshot valid memperlihatkan keadaan yang sesuai dengan checkpoint.
4. Baru setelah restore tengah Story Mode terbukti, lanjutkan Story Mode. Pengujian Memory Card dalam game tetap prioritas berikutnya.

## Status aturan

- **TERVERIFIKASI (harness diagnostik):** A, B, C, dan C2 berakhir tanpa crash pada eksperimen run #39248081546.
- **HIPOTESIS:** crash terjadi di jalur native pemuatan/deserialisasi yang dipanggil `PCSX.loadSaveState()`; fungsi atau struktur penyebabnya belum diketahui.
- **BELUM DIUJI:** pemulihan savestate berhasil; kelanjutan Story Mode dari pertengahan permainan; save/load nyata melalui Memory Card; Story Mode tamat.

Untuk dialog Story Mode tetap gunakan **START**, bukan Circle. Jangan membatalkan runner lain dan jangan mengklaim game tamat tanpa bukti kuat.
