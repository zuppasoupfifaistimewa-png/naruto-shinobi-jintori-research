# PROMPT CHAT BARU — TUNTASKAN RISET REVERSE ENGINEERING LANGKAH 4–10

Gunakan GPT-6. Lanjutkan pekerjaan langsung dari checkpoint GitHub terbaru dan riwayat percakapan terkait yang tersedia. Jangan meminta saya mengulang konteks. Baca handoff dan laporan sebelum mengambil tindakan; setelah itu lanjutkan pekerjaan, jangan berhenti pada rencana.

## 1. Batas repositori dan keselamatan bukti

Satu-satunya repositori yang boleh diakses atau diubah:
\`zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research\`.

Jangan akses atau ubah repositori lain. Jangan membangun atau mengubah sistem pemain adaptif, classifier, policy, Story Mode runner, atau readiness gate. Fokus hanya reverse engineering Langkah 4–10. Jangan jalankan Story Mode/gameplay, mengirim input gameplay, atau me-restore savestate. Bila suatu kriteria benar-benar mensyaratkan bukti runtime, dahulukan audit statis; usulkan atau jalankan hanya eksperimen diagnostik terisolasi, non-gameplay, berbatas waktu, dan dengan input privat dibersihkan. Jangan mengklaim bukti runtime jika bukti itu tidak ada.

ROM/BIN/CUE, BIOS, memory card, savestate, executable hasil ekstraksi, dan screenshot privat tidak boleh masuk Git atau artefak. Jika analisis dengan GitHub Actions diperlukan, download dan proses file di runner, verifikasi ukuran/checksum, hapus input privat/proyek sementara, dan unggah hanya laporan teks/log yang sudah diverifikasi. Jangan menggunakan gambar dari web sebagai bukti visual game. Bukti screenshot game harus autentik dari emulator/game asli dan jalur asalnya terverifikasi. Labeli setiap klaim sebagai **TERVERIFIKASI**, **TERVERIFIKASI-STATIS**, **HIPOTESIS**, **UNKNOWN**, atau **BLOCKED**, sesuai kekuatan bukti.

## 2. Checkpoint terakhir yang telah diperiksa

Snapshot pada 27 Oktober 2026 sekitar 18:59 WIB:
- Branch \`main\` HEAD yang terakhir diverifikasi saat itu: \`dfa0bf47dff300384c1f9884aa957c7ce1b48658\`, commit “Trace incoming callers of Step 6 pending-field access functions”. **Fetch ulang HEAD sekarang; jangan anggap snapshot ini masih HEAD terkini.**
- Step 6/7 static field-offset/resource profile scan [Run #40500058788](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40500058788) selesai \`success\` pukul 18:59:18 WIB. Artefak #12731474756, 180.174 byte, ZIP SHA-256 \`4aea20e1420292505666f15898ba2db57a875a4fc67fbe2c65336af0a16fc9f4\`. Artefak ini **lebih baru** daripada scan Step 6 yang sebelumnya diaudit; periksa metadata/digest dan isi teksnya melalui runner-only audit sebelum menyimpulkan apa pun dari isinya.
- Runner-only audit [Run #40499884728](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499884728) sukses pukul 18:56:30 WIB, artefak #12731973462, 13.071 byte, ZIP SHA-256 \`2c9ce2c7bf5f234e7cbe948d13ee2ea19dcfff4af08158d32b0a1604019f67dd\`. Audit ini mendahului artefak scan #40500058788, sehingga jangan menyebut artefak terbaru sudah diperiksa jika belum.
- Helper/callback static audit [Run #40499270568](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499270568) sukses pukul 18:53:12 WIB; artefak #12731593532, 11.672 byte, ZIP SHA-256 \`8567a5cad2a00823302ea7b361dd9b6eaab736bce6b77cf51ea136d6bee454b3\`. Raw log: \`STEP4_HELPER_PRIVATE_CLEANUP=PASS\`, \`text_only_output_validation=PASS\`, \`uploaded_input_executable=no\`.
- Full Ghidra analysis [Run #40498208067](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498208067) masih tercatat berjalan pada pemeriksaan terakhir, pada tahap analisis DATA.BIN entry 0. **Periksa status live; jika sudah selesai, baca hasil final. Jika masih aktif, jangan meluncurkan duplikat analisis berat yang sama.**
- Kembalilah memeriksa run terbaru, jobs, artifacts, log, digest ZIP, dan cleanup. Jangan mengandalkan status lama dalam dokumen bila Actions sudah berubah.

## 3. Baca dokumen/handoff terlebih dahulu

Minimal baca dan rekonsiliasi status aktual dari:
- \`STATUS.md\`
- \`ANALYSIS_LOG.md\`
- \`out/logic.md\`
- \`docs/HANDOFF_REVERSE_ENGINEERING_STEPS4_10_2026-10-27.md\`
- \`docs/REVERSE_ENGINEERING_AUDIT_STEPS_1_10_2026-10-27.md\`
- \`docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md\`
- \`docs/STEP4_RNG_TRACE_2026-10-27.md\`
- \`docs/STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md\`
- \`docs/STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md\)

Periksa workflow, skrip Ghidra, dan kriteria di repo yang relevan. Temukan juga commit dan artefak terbaru sebelum mengulang eksperimen. Jangan membuat ulang laporan yang sudah tersedia; perbaiki atau tambahkan bukti baru saja.

## 4. Kriteria penyelesaian Langkah 4–10

**Langkah 4 — panggilan fungsi, caller/callee, argumen, return, dan lifecycle nilai.**
Temuan statis yang sudah tersedia: fungsi main EXE \`0x80037138\` ketika menerima \`a0=-1\` memuat dan mengembalikan global \`0x80066E7C\`. Callsite kandidat pada DATA.BIN entry 0 memanggil helper dengan delay slot \`li a0,-1\`; setter kandidat \`0x80035DA8\` menerima nilai hasil melalui delay slot \`move a0,v0\`, jika call path itu benar-benar berjalan. Base entry 0 \`0x800AD000\` masih HIPOTESIS. Fungsi \`0x8003755C\` punya guard \`0x80065DB4\`; jalur inisialisasinya memanggil \`0x80037B58\`, yang menulis nol ke \`0x80066E7C\`, mengosongkan delapan slot pointer mulai \`0x80066E5C\`, kemudian mengirim pointer \`0x80037BB0\` ke dispatcher tak langsung \`0x800373F8\`. Callback \`0x80037BB0\` menambah \`0x80066E7C\` dan memanggil slot callback nonzero. Semua ini adalah bukti statis tentang pola counter/callback, **bukan** bukti nilai seed saat runtime.
Lanjutkan dengan mencari dan membuktikan urutan initializer/dispatcher, callsite DATA.BIN entry 0 sekitar \`0x800AF2A4–0x800AF2B0\`, pemetaan alamat entry, target setter, dan kapan nilai global dibaca relatif terhadap reset/increment. Gunakan raw MIPS dan instruction delay slot jika Ghidra salah membatasi function boundary. Jangan menyebut lifecycle seed tuntas sampai caller, mapping, urutan, dan batas ketidakpastian terjelaskan dengan bukti yang dapat diperiksa.

**Langkah 5 — verifikasi fungsi secara terarah.**
Baca kriteria dan laporan yang sudah ada. Status sebelumnya hanya menyatakan empat fungsi terpilih telah diverifikasi; jangan menggeneralisasi hasil itu menjadi seluruh fungsi game. Pastikan setiap fungsi yang diklaim tuntas memiliki alamat, bytes/instruksi mentah, caller/xref, calling convention/return yang didukung, dan tes atau bukti yang sesuai kriteria. Tambah cakupan hanya jika ada kriteria yang belum terpenuhi.

**Langkah 6 — pemetaan field, read/write, alias, dan aliran data.**
Gunakan artefak terbaru #12731474756 sebagai prioritas untuk audit berikutnya. Bukti sebelumnya menunjukkan pada view entry 1 dengan base hipotetis \`0x800D0000\`: \`0x8012C634 lw v0,0xB30(a0)\`, \`0x8012C638 lw v1,0xB38(a0)\`, \`0x8012C640 addu v0,v0,v1\`, \`0x8012C644 sw v0,0xB40(a0)\`; offset \`+0xB44\` pernah terlihat ditulis nol di \`0x8012C604\` dan dibaca di \`0x8012CB14\` lalu diteruskan sebagai argumen \`a2\` kepada \`0x8001B364\`. Base \`0x800D0000\` tetap HIPOTESIS. Audit semua writer dan reader yang dapat ditemukan, instruction displacement, perakitan alamat efektif melalui register, register alias, incoming callers, bounds, code tidak terdekode, dan kemungkinan base alternatif. Bedakan bukti akses langsung dari inferensi makna. Jangan menamakan field sebagai chakra/biaya/giliran/barrier/level-up tanpa bukti yang independen. Bila ada batas scanner, catat tepatnya; “tidak ditemukan” bukan bukti “tidak ada”.

**Langkah 7 — loader/copy, mapping alamat, dan bukti runtime yang disyaratkan kriteria.**
Baca kriteria Langkah 7 dan laporan coldboot/loader sebelumnya. Hasil historis pada alamat target \`0x800AD454\` adalah bounded no-hit (tidak ada breakpoint hit, bukti copy size/register/checksum yang menutup jalur loader belum tersedia); itu tidak membuktikan loader tidak ada atau base sudah pasti. Cari jalur data berdasarkan bukti statis lebih dulu. Jika kriteria mewajibkan runtime, desain satu diagnostik terisolasi dengan target/stop condition yang terukur dan cleanup; hindari run duplikat, gameplay input, dan restore save state. Buktikan target instruksi, register, ukuran copy/buffer, sumber/tujuan dan checksum hanya jika benar-benar tertangkap. Catat no-hit, timeout atau stall sebagai hasil terbatas, bukan bukti negatif universal.

**Langkah 8 — semantik fungsi dan aturan game.**
Periksa setiap kandidat fungsi melawan caller/callee, raw instruction, data flow, dan bukti lain yang independen. Beri label TERVERIFIKASI/HIPOTESIS/UNKNOWN. Terjemahkan teks Jepang ke bahasa Indonesia secara berdampingan pada laporan. Jangan mengubah operasi assembly menjadi aturan gameplay tanpa bukti. Target akhir adalah tabel aturan yang membedakan yang terbukti, dugaan dan belum diketahui—bukan sekadar daftar nama fungsi.

**Langkah 9 — validasi terisolasi fungsi RNG.**
Riset sebelumnya sudah menutup cakupan terbatas fungsi \`0x80035D78\`: 7/7 vector, state dan \`v0\` sesuai, sentinel return 12 instruksi, batas 128 instruksi, dan alias RAM fisik 2 MiB. Verifikasi ulang sumber log/test bila diperlukan, tetapi jangan mengulang sweep tanpa alasan. Klaim tuntas hanya untuk fungsi/kriteria yang memang diuji; jangan menggeneralisasi ke seluruh RNG/game.

**Langkah 10 — matriks closure yang dapat diaudit.**
Bangun matriks untuk setiap kriteria resmi Langkah 4, 5, 6, 7, 8, 9, 10: kriteria, status, bukti, sumber/run ID, artifact ID, SHA-256, tes, batas/unknown, dan pekerjaan tersisa. Langkah 10 bukan tuntas hanya karena indeks laporan tersedia; indeks harus mengarah ke bukti untuk setiap kriteria. Putuskan TUNTAS hanya jika seluruh kriteria langkah itu telah memiliki bukti yang memenuhi standar. Jika tidak mungkin ditutup dengan akses/bukti yang tersedia, statusnya BLOCKED/SEBAGIAN dan tuliskan bukti spesifik yang masih diperlukan.

## 5. Prosedur kerja wajib

1. Mulai dengan fetch branch \`main\`, baca handoff/laporan, periksa Actions runs terbaru dan pastikan artefak terbaru mana yang sudah atau belum diaudit.
2. Lakukan satu eksperimen diagnostik yang terarah pada satu waktu; jangan menjalankan analisis berat duplikat saat run setara masih aktif. Untuk run aktif, periksa status/jobs/log secara berkala; jangan mengarang ETA.
3. Setiap eksperimen harus mempunyai hipotesis, alamat/target, metode, stop condition, hasil, bukti mentah, SHA-256, dan cleanup. Periksa raw log, bukan hanya conclusion \`success\`.
4. Inspeksi artifacts melalui workflow runner-only: verifikasi run ID, artifact ID, name, ukuran, expiry, digest; unduh dan ekstrak hanya di runner, tampilkan/olah teks relevan, hapus ZIP/input sementara, lalu konfirmasi \`RUNNER_ARTIFACT_CLEANUP=PASS\`. Jangan mematerialisasi biner privat ke chat atau commit.
5. Simpan perkembangan bermakna di \`STATUS.md\`, \`ANALYSIS_LOG.md\`, \`out/logic.md\`, matriks audit, closure report, serta handoff. Rekonsiliasi status lama yang menjadi stale; jangan menambahkan duplikat berulang. Pastikan commit dan link Actions berfungsi.
6. Saat ada temuan baru yang dapat mendukung klaim, sampaikan hasil konkret yang telah terverifikasi dan lanjutkan pekerjaan. Beri pembaruan singkat dan berguna selama bekerja; jangan hanya mengirim status generik.
7. Jangan mengklaim permainan tamat atau Langkah 4–10 semuanya tuntas tanpa bukti per-kriteria yang autentik dan dapat direproduksi.

## 6. Keluaran akhir yang diwajibkan

Selesaikan semaksimal mungkin dalam percakapan ini. Laporkan per langkah 4–10 apakah TUNTAS, SEBAGIAN, atau BLOCKED; tiap klaim harus dilengkapi tautan commit/run/artifact dan digest yang sesuai. Daftarkan secara eksplisit kriteria yang belum terpenuhi, mengapa belum bisa dipenuhi, serta eksperimen minimum yang diperlukan untuk menutupnya. Perbarui handoff terakhir agar ChatGPT pada chat selanjutnya dapat meneruskan dari HEAD/checkpoint tepat tanpa mengulang pekerjaan.

Targetnya adalah bukti reverse engineering yang dapat diperiksa—bukan kesan bahwa pekerjaan sudah selesai.