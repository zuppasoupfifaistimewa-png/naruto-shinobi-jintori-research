## PEMBARUAN DIAGNOSIS — dugaan pointer sentinel SPU/ADPCM (20 Oktober 2026)

## Catatan eksekusi terbaru — 20 Oktober 2026

Run [#39373493482](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39373493482) sedang menguji hipotesis sentinel ADPCM pada source raw yang tetap tidak berubah. Percobaan push terdahulu [#39372712212](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39372712212) gagal sebelum staging karena fallback `source_run_id` tidak diterapkan pada unduhan Memory Card; ini adalah bug orkestrasi, bukan hasil uji restore. Run terbaru telah lolos staging sumber, validasi aset, dan schema API pada binary pinned; build patch masih berjalan dan belum ada artifact final/hasil restore. Diagnosis kausal tetap hipotesis sampai log hasil patch diperiksa.

Bagian lama di bawah adalah temuan historis. Setelah pemetaan schema dan pembacaan raw field, diagnosis paling mungkin untuk SIGSEGV receiver board kini adalah bug cursor ADPCM stopped yang dikenal di upstream PCSX-Redux [PR #2218](https://github.com/grumpycoders/pcsx-redux/pull/2218). Build pinned 0c3572c3db75f97542001e453ae80ba8c3f8acba lebih tua dari fix tersebut. Lihat [analisis akar dan probe](SAVESTATE_ADPCM_SENTINEL_ROOT_CAUSE_2026-10-20.md).

- Receiver lama memastikan raw staging identik; PC fault membaca byte melalui movzbl (%rsi),%ecx pada RSI 0xffffffffd736a15f, loader tidak kembali dan event restore tidak terdeteksi.
- API PCSX.getSaveStateProtoSchema() tersedia pada source yang dipatok dan menghasilkan schema protobuf. Workflow baru akan menguji pemanggilan runtime sebelum loader.
- Top-level field 6 adalah spu; channel.data.current adalah field 8. Raw board memiliki 20 cursor out-of-range dan 18 di antaranya berflag stop=1; raw boot juga menyimpan cursor invalid tetapi channel tampak inactive.
- Workflow [workflow probe perbaikan sentinel](.github/workflows/naruto-spu-sentinel-fix-probe.yml) membangun emulator dari commit basis sama dengan patch dua-file upstream #2218 serta raw state yang tidak diubah. Setelah checkpoint baru disimpan, workflow memuatnya pada proses emulator baru dan mengulang gate restore; belum ada hasil run probe.

**Status:** hipotesis berkeyakinan tinggi, bukan restore PASS. Story Mode belum terbukti dilanjutkan dari checkpoint dan game belum terbukti tamat.

---

## PEMBARUAN TERKINI — raw Story Mode checkpoint lintas-run dipersiapkan (19 Oktober 2026)

- Raw state boot awal telah pulih lintas-run (Run A #39255438457 → Run B #39255549341); hasil tersebut bukan checkpoint Story Mode. Run #39257735369 juga membuktikan positive-control sanitizer untuk state boot saja. Restore checkpoint lama yang disanitasi masih pernah SIGSEGV/exit 139.
- Run #39261524544 bukan eksperimen emulator yang sah: berhenti sebelum start karena variabel watcher Bash `raw_resume_verify` tidak ditentukan, exit 255. Perbaikan launcher ada pada commit `e396eac00631001b7a0e68d7701c70aec10dec19`.
- Run aktif #39262213468: [Actions](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468). Aset runtime terverifikasi, emulator sedang berjalan dan belum ada artifact. Jangan batalkan atau mengubah file workflow utama selama run aktif.
- Workflow utama menyimpan salinan raw asli byte-per-byte, hash/ukuran dan screenshot sumber untuk checkpoint; retention 14 hari. Workflow penerima `.github/workflows/naruto-raw-storymode-restore.yml` (commit `ddcf1e0...`) menolak checkpoint yang bukan layar stabil pascadialog, memverifikasi hash sebelum load pada runner baru tanpa sanitizer/rehidrasi BIOS, lalu menuntut event restore, ≥180 VSync, dan perbandingan screenshot PASS sebelum melanjutkan.
- Bila state raw atau screenshot pembanding tidak ada, atau source reason/frame/gate tidak cocok, restore mesti gagal-tertutup. Jangan sebut hasil ini progres Story Mode yang aman tanpa bukti aktual. Memory Card baru sebatas file 131.072 byte dengan status game save belum diverifikasi.

## HASIL BARU — raw savestate benar-benar pulih lintas-run (19 Oktober 2026)

- **TERVERIFIKASI, terbatas pada boot awal:** [Run A #39255438457](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255438457) membuat raw state melalui `PCSX.createSaveState()` pada VSync 60, tanpa sanitasi. File berukuran **21.124.144 byte**, SHA-256 `a4672dd49fbfa76ef60de410c50460d77e115181fc3e205a215ab9f5f1e601d7`. Artifact sumber privat #12187367829: [unduh dari GitHub](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255438457/artifacts/12187367829).
- **TERVERIFIKASI lintas-run:** [Run B #39255549341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255549341) berjalan sebagai workflow-run baru di runner/workspace dan proses emulator yang baru. B mengunduh artifact A, memverifikasi ukuran serta SHA-256 sama (`SOURCE_ARTIFACT_VERIFY=PASS`, `SOURCE_FILE_UNMODIFIED=1)), lalu memulihkannya.
- Bukti restore B: `ExecutionFlow::SaveStateLoaded`, `LOAD_CALL_RETURNED=1`, `ExecutionFlow::Run`, **180 VSync pascarestore**, exit 0, dan gerbang akhir PASS. Screenshot valid **640×508**, PNG 20.521 byte; SHA-256 `90aa21b6943bac231e4c0e888923a5d1e9658de28ce5c715b9328b17c046db21`. Bukti privat artifact #12187962047: [unduh dari GitHub](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255549341/artifacts/12187962047).
- Screenshot menunjukkan **logo boot Sony Computer Entertainment**; raw state dibuat di sekitar `KERNEL SETUP!`, bukan di tengah Story Mode. Jadi hasil ini membuktikan portabilitas savestate mentah lintas runner/proses **untuk state boot awal saja**.
- **BELUM TERBUKTI:** pemulihan checkpoint tengah Story Mode. Restore checkpoint lama yang disanitasi masih SIGSEGV/exit 139 pada tahap D run #39252214331. Akar penyebab sanitizer belum diketahui. Tidak ada progres Story Mode yang boleh dianggap aman; Story Mode belum dilanjutkan dan game belum terbukti tamat.
- Langkah berikutnya: gunakan raw boot state yang sudah terbukti sebagai kontrol positif, bandingkan sanitizer dengan perubahan satu faktor per eksperimen, dan jangan mengubah checkpoint lama. Setelah sanitizer dipahami, buat raw checkpoint baru saat gameplay Story Mode benar-benar aktif dan wajib buktikan restore dengan event, ≥180 VSync, serta screenshot yang cocok dengan adegan checkpoint sebelum melanjutkan permainan. Memory Card diuji sesudah restore tengah Story Mode terbukti.
- Dialog Story Mode dilewati dengan **START**, bukan Circle. Aturan gameplay tetap diberi label **TERVERIFIKASI / HIPOTESIS / BELUM DIUJI** berdasarkan bukti langsung. Pada pemeriksaan setelah run B, **tidak ada Actions runner aktif**.

---

## Hasil terbaru — run #39252214331 (19 Oktober 2026)

Ini mengoreksi catatan sebelum tahap E/F selesai. Hasil sekarang menunjukkan keberhasilan *terbatas* pada savestate mentah di runner cloud, tetapi **belum** pada checkpoint tengah Story Mode.

- Tahap A/B/C/C2 lulus.
- Tahap D: checkpoint lama yang disanitasi lalu direhidrasi BIOS crash (SIGSEGV/exit 139) sesaat setelah `SAVESTATE_PROBE_LOAD_CALL_BEGIN=1`.
- Tahap E: `PCSX.createSaveState()` pada emulator yang boot mencapai `KERNEL SETUP!` menghasilkan state mentah 21.124.150 byte.
- Tahap F: state mentah dimuat lagi dalam lingkungan runner yang sama. Log mencatat `ExecutionFlow::SaveStateLoaded`, `LOAD_CALL_RETURNED=1`, `ExecutionFlow::Run`, dan `SAVESTATE_PROBE_POST_RESTORE_VSYNC=180`. Tidak terjadi crash dalam tahap ini.
- Artifact #12186545059 menyediakan screenshot valid 640×508 (650.240 byte raw) yang menunjukkan logo boot Sony Computer Entertainment. Ini bukti visual emulator render setelah restore, tetapi bukan bukti Story Mode atau save/load lintas runner.
- Keseluruhan workflow diberi conclusion failure karena gerbang akhirnya masih mensyaratkan tahap D checkpoint tersanitasi lulus. Tahap F lulus tidak menghapus kegagalan D.
- Capture A/B/C/C2 masih menghasilkan dimensi 0×0; itu bukan screenshot valid.
- Tidak ada runner aktif setelah run ini selesai pada pemeriksaan terakhir.

**Hambatan utama:** perbedaan antara state mentah yang dibuat/dimuat oleh PCSX-Redux sendiri dan checkpoint tersanitasi yang disimpan sebagai artifact. Penyebab tepatnya belum diketahui. Hipotesis yang perlu diuji adalah field/struktur savestate berubah secara tidak kompatibel saat sanitizer menghapus/menyisipkan BIOS; hipotesis ini harus dibuktikan dengan diff schema dan eksperimen faktor tunggal.

**Uji berikutnya:** jangan ulangi roundtrip mentah dalam satu proses. Jalankan state mentah buatan emulator sebagai artifact lintas-run: run A membuat dan mengunggah file tanpa modifikasi; run B menjalankan emulator dalam proses bersih dan memuat file tersebut, dengan event, kemajuan VSync, dan screenshot valid sebagai gerbang. Ini memisahkan faktor portabilitas lintas-proses dari sanitasi. Jika raw lintas-run lulus, berikutnya bandingkan parse/schema state mentah versus checkpoint tersanitasi dan uji sanitasi sebagai satu-satunya faktor yang berubah. Jika raw lintas-run gagal, investigasi build/version atau komponen state yang bergantung proses. Jangan ubah checkpoint sumber dan jangan mulai ulang Story Mode.

---

## Update GDB dan roundtrip native — 19 Oktober 2026

- [Run #39248501957](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39248501957) mengulang A/B/C/C2 dan menjalankan tahap D di bawah GDB. Log D membuktikan `SAVESTATE_PROBE_LOAD_CALL_BEGIN=1`, lalu thread 15 (`pcsx-redux`) menerima SIGSEGV pada PC `0x00007ffff0dd36d0`. Stack teratas `#0 0x00007ffff0dd36d0`, `#1 0x0000000001589a80`, `#2 0x00000000014f49f0`, `#3 0x00007ffff0de5870`. Nilai PC dan stack cocok dengan GDB lama #39235079514. Binary stripped; alamat ini belum bisa dipetakan ke nama fungsi.
- Trace lama #39235079514 pada PC yang sama mencatat `RSI=0xffffffffddd13fff` dan instruksi `movzbl (%rsi),%ecx`, yaitu pembacaan byte dari alamat invalid. Ini memperkuat bahwa jalur native/JIT crash dengan pointer invalid, tetapi belum menentukan field state atau fungsi penyebab.
- Artifak #12184890672 berisi log GDB dan ringkasan; retensi sampai 26 Oktober 2026.
- Capture GPU pada VSync awal di A/B/C/C2 menghasilkan `width=0,height=0`, raw 0 byte; screenshot itu tidak valid sebagai bukti visual.
- Run [#39252214331](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39252214331) menyelesaikan kontrol independen E/F: savestate mentah buatan emulator (21.124.150 byte) berhasil dimuat, event `SaveStateLoaded` dan `ExecutionFlow::Run` muncul, emulator melewati 180 VSync pascarestore, dan screenshot valid 640×508 menunjukkan logo boot Sony. Ini belum menguji state di tengah Story Mode. Jalur D untuk checkpoint tersanitasi masih crash exit 139; workflow failure sesuai gerbang yang menuntut D lulus.

---

# Diagnostik pemulihan savestate — 19 Oktober 2026

## Status ringkas

Prioritas riset tetap memperbaiki savestate sampai terbukti memulihkan keadaan permainan di tengah Story Mode. Sudah ada satu roundtrip mentah yang berhasil pada boot awal (run #39252214331), tetapi belum ada restore checkpoint tengah Story Mode yang terbukti. Tidak ada input gameplay yang dikirim selama pengujian diagnostik ini.

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
