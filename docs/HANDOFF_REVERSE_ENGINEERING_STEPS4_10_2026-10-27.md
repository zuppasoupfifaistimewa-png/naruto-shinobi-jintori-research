# Handoff — reverse engineering Naruto PS1, Langkah 4–10

Pembaruan: 27 Oktober 2026, setelah run Step 9 #40474891838.  
Repo yang diizinkan: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research` saja. Jangan akses atau ubah repo lain.

## Checkpoint terbaru — Step 7 observability A/B (27 Oktober 2026)

Checkpoint remote yang diverifikasi sebelum pembaruan handoff ini: main HEAD 1513f0d3265707a1ef27c39644b9376b910b7c91. Selalu fetch main HEAD/commit dan cek Actions lagi; commit yang memperbarui handoff ini sendiri akan memajukan HEAD.

- Run terbaru [#40479865235](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40479865235) completed/success, 157 detik, pada source commit 51cce7fe07ce5b73b83a5296b4a1d1d86b424ce6. Artefak teks #12722187784, SHA-256 ZIP b9537035eb6ffed66a0aadd5ab48db88715ed2e2128bcf46a48f374c7306ac26, ukuran 3801 byte, retensi belum kedaluwarsa saat audit.
- Run memasukkan kontrol cold-boot -debugger dengan VSync listener saja, lalu probe empat breakpoint memakai -no-debugger. Pra-uji tanpa breakpoint mencapai frame 50; kontrol debugger tanpa breakpoint mencatat frame 1,2,3,10,20,30,40; probe empat breakpoint hanya frame 1–3 lalu timeout 124 pada batas 70 detik. Tidak ada hit loader/seed/RNG yang diterima; job dan private cleanup PASS. Ini bukan bukti target tidak pernah berjalan.
- Bug pelaporan: metrik DEBUGGER_CONTROL_MAX_VSYNC_FRAME otomatis bernilai 0 karena regex salah escaping; raw log adalah sumber benar. Perbaiki parser pada run berikutnya.
- Langkah 4 secara keseluruhan SEBAGIAN untuk resmi subkriteria 4(a–e); laporan STEP4_CLOSURE kini sudah dikoreksi dari TUNTAS keseluruhan menjadi SEBAGIAN. Inventaris statis tertentu selesai, tetapi seed/lifecycle runtime, kausalitas roulette, caller battle, dispatch indirect penuh, randomness alternatif masih UNKNOWN/terbuka.
- Langkah 5 TUNTAS untuk empat fungsi terpilih; Step 6 SEBAGIAN; Step 7 SEBAGIAN; Step 8 SEBAGIAN; Step 9 TUNTAS hanya untuk RNG 0x80035D78 (7/7 state vector, 12 instruksi/vektor, sentinel return, physical RAM alias); Step 10 TUNTAS sebagai indeks audit, bukan keseluruhan logika game.
- Perubahan dokumentasi terbaru: laporan Step 7 runtime, peta Step 7, laporan closure gabungan, STATUS.md, ANALYSIS_LOG.md, out/logic.md telah diperbarui. OVERLAY_MAP/Step 8 menahan klaim pemenang yang belum tervalidasi; audit utama tidak lagi menyebut Step 9 terblokir untuk RNG yang sudah lulus.

### Aksi berikutnya — jangan ulangi run identik

1. Ambil lagi main HEAD, status semua Actions (terutama queued/in_progress) dan artefak terbaru. Jangan jalankan workflow pemain adaptif.
2. Perbaiki parser metrik frame dalam workflow Step 7 dan tambahkan pemeriksaan sederhana yang membuktikan regex mengekstrak angka dari sample log. Lakukan sebagai perubahan kode yang terarah, bukan pengulangan cold boot identik.
3. Uji satu breakpoint per cold boot, tanpa savestate restore dan tanpa input gameplay, dengan batas waktu yang singkat dan sumber (disc/CUE/BIOS/emulator) diverifikasi. Mulai dari satu target paling informatif, rekam VSync per-frame awal, PC/hit count, exit code, screenshot hanya jika diperlukan dan harus autentik X11. Bila callback breakpoint tunggal pun menghentikan progress, lakukan kontrol listener-only dan uji breakpoint tanpa log; jangan menambah target sampai penyebab observabilitas dipahami.
4. Perbarui docs/STEP7_RUNTIME_COLD_BOOT_RESULT_2026-10-27.md dan closure hanya berdasarkan log/artefak terverifikasi. Tidak boleh mengubah status Step 7 ke TUNTAS tanpa bukti loader/base/lifecycle yang benar.
5. Lanjutkan kerja independen statis Step 6/8: telusuri operand → branch → store → caller untuk offset +0xB30/+0xB38/+0xB40/+0xB44 dan +0x58B/+0x2E9/+0x2E5/+0x5D2; jangan menganggap getter target sebagai win check atau setter sebagai transaksi biaya. Gunakan hanya output Ghidra statis yang sudah ada bila belum ada pertanyaan baru; jangan menjalankan ulang analisis setara.
6. Tidak perlu mengulang Step 4 roulette determinism #40474262267 maupun Step 9 RNG Unicorn #40474891838. Tidak ada kewajiban otomatis menguji tiap fungsi secara terisolasi kecuali kriteria resminya menuntutnya atau klaim baru memerlukan bukti eksekusi; jangan generalisasi hasil RNG ke fungsi lain.
7. Setelah seluruh pekerjaan independen yang aman dikerjakan, perbarui laporan penutupan, STATUS.md, ANALYSIS_LOG.md, out/logic.md, dan handoff; gunakan TUNTAS/SEBAGIAN/BLOKIR secara tepat. Story Mode tidak boleh dinyatakan tamat tanpa bukti ending autentik.

## Aturan utama untuk chat berikutnya

- Jangan mengembangkan atau menjalankan pemain adaptif. Jangan jalankan Story Mode otomatis, jangan ubah classifier/input policy/readiness gate, jangan mengubah marker Revision65, dan jangan menafsirkan WAIT/UNKNOWN/NO-GO sebagai izin input.
- ROM/disc, BIOS, Memory Card, savestate, RAM dump dan screenshot gameplay privat tidak masuk Git. Gunakan Actions artifact dan laporan teks metadata saja sesuai pola repo. Semua screenshot gameplay harus X11 autentik dari emulator.
- Lanjutkan dari laporan/checkpoint di bawah; jangan ulang eksperimen yang telah sukses hanya untuk memperoleh status Actions hijau. Jika run aktif ditemukan, jangan tumpang tindih eksperimen yang sama.
- Hanya nyatakan langkah TUNTAS bila semua kriteria resminya terpenuhi sesuai cakupannya. Bedakan status subkriteria dari status seluruh langkah.
- Story Mode completion: **TIDAK TERBUKTI TAMAT**. Tidak ada ending autentik diverifikasi pada rangkaian audit ini.

## Prioritas dokumen

1. [Laporan penutupan gabungan Step 4–10](STEP4_10_CLOSURE_REPORT_2026-10-27.md) — matriks status/kriteria, bukti dan UNKNOWN.
2. [Audit resmi langkah 1–10](REVERSE_ENGINEERING_AUDIT_STEPS_1_10_2026-10-27.md) — status terotorisasi dan cakupan sumber.
3. [Step 4 runtime](../out/step4/STEP4_RNG_RUNTIME_RESULT_2026-10-27.md), [Step 4 static trace](STEP4_RNG_TRACE_2026-10-27.md), [Step 4 closure statis](STEP4_CLOSURE_2026-10-27.md).
4. [Step 5 Ghidra/m2c](../out/step5/STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md).
5. [Step 6 xref/semantic review](STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md).
6. [Step 7 loader/overlay](STEP7_LOADER_OVERLAY_MAPPING_2026-10-27.md).
7. [Step 8 function semantics/game rules](STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md).
8. [Step 9 isolated MIPS RNG probe](../out/step9/STEP9_UNICORN_RESULT_2026-10-27.md).
9. [Index logic](../out/logic.md), plus final status and analysis-log tail.

## Keputusan per langkah saat handoff

| Langkah | Status | Berikutnya |
|---|---|---|
| 4 — RNG | **SEBAGIAN** | Sumber seed saat boot/lifecycle, direct vs indirect/dispatch lengkap, hubungan caller-ke-hasil roulette, caller battle di checkpoint autentik, dan sumber randomness alternatif belum terbukti. |
| 5 — Ghidra/m2c | **TUNTAS untuk empat fungsi terpilih** | Tidak perlu mengulang delapan output C yang sudah disimpan; lanjut hanya jika pertanyaan baru menuntut fungsi lain. |
| 6 — xref/call chain | **SEBAGIAN** | Base resource runtime, control flow fungsi transisi yang gagal didekompilasi, sumber delta +0xB30/+0xB38/+0xB40/+0xB44 dan semantik record masih UNKNOWN. |
| 7 — loader/overlay | **SEBAGIAN** | Peta directory/bootstrap statis ada; loader runtime, base/lifecycle dan relokasi belum diuji; DATA2/DUMMY belum dipetakan menyeluruh. |
| 8 — aturan | **SEBAGIAN** | Tidak ada formula biaya barrier/upgrade atau aturan battle/roulette/turn universal yang telah dibuktikan. |
| 9 — MIPS terisolasi | **TUNTAS untuk rutin RNG 0x80035D78** | Run #40474891838: 7/7 vektor lulus setelah pemetaan RAM fisik yang benar. Ini tidak menutup uji fungsi lain atau emulasi PS1. |
| 10 — indeks dokumentasi | **TUNTAS sebagai indeks audit** | Pertahankan tautan/report dan status UNKNOWN; jangan mengklaim seluruh game sudah reverse-engineered. |

## Bukti runtime yang sudah final

### Step 4 — roulette window, bukan battle

- Run eksperimen: [#40474262267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267). Keseluruhan Actions job berstatus failure karena tahap akhir commit report via API gagal; log eksperimen sendiri menyatakan runtime infra PASS dan semua cabang/test input lulus.
- Artefak privat: [#12719024236](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267/artifacts/12719024236). Laporan disusun ulang dari raw log dan metadata ke file repo; tidak mengunduh atau menyimpan screenshot privat ke Git.
- Cabang R30A/R30B input Circle F30/releases F38; DELAY60 input F60/releases F68. State awal 0xDB75C114 pada semua cabang.
- Masing-masing 127 hit RNG, post-restore seed-setter hit 0, final state 0xA99DC6E7. Sequence/caller/state-before stream cocok sesudah nomor VSync dikeluarkan dari perbandingan; sampled state juga sama.
- Ketiga X11 screenshot 1280×800 lolos validasi dan normalized viewport crop SHA-256 sama: a1b2dfab61a0922e2b466ddbeb6b5b2642a88289be159df4667e4e2bcaa53355. Event capture frame 169/167/171 tidak sama; jangan mengklaim frame identik. Belum ada hubungan kausal ke hasil roulette yang terlihat.

### Step 9 — function isolation

- Percobaan pertama [#40474699863](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474699863) gagal 0/7 karena virtual-KSEG memory map; zero instructions, tidak membuktikan rumus salah.
- Run kedua [#40474891838](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474891838) sukses; artifact #12720127454 digest SHA-256 ZIP bcbfcd77a532ce34334ed60f720fdeaac566308bf2e6e4d54a7e60f28a5f083b.
- Fungsi MIPS utama dijalankan melalui alias fisik RAM 2 MiB dengan 7 initial-state vectors. State baru, v0 dan sentinel-return sesuai harapan; 12 instruksi per vektor. Cleanup runner PASS. Hanya report/log/metadata teks diunggah.

## Eksperimen berikut yang bernilai (jangan kerjakan jika tidak memenuhi prasyarat)

1. **Boot seed lifecycle:** jalankan hanya workflow diagnostik khusus dengan cold boot, breakpoint pada kandidat setter 0x80035DA8 dan log lokasi/state/waktu; jangan infer seed dari no-hit pasca-restore.
2. **Loader mapping:** jika alat checkpoint boot/BIOS yang telah diverifikasi dapat digunakan, capture PC/register/copy-size/hash/alamat tujuan saat directory/bootstrap disalin. Kalau cold boot loader instrumentation belum punya alat teruji, lanjutkan xref statis dengan batas yang eksplisit dan jangan menandai base sebagai runtime-confirmed.
3. **Battle caller:** cari artefak yang ada di repo ini untuk checkpoint battle autentik terverifikasi. Jika tidak tersedia, jangan mengarang atau mengasumsikan checkpoint roulette adalah battle. Siapkan diagnostic-only method, no adaptive player/Story Mode automatic.
4. **Langkah 6/8 semantics:** lanjutkan statis pada pembaca/penulis field serta branch/call target. Nama mekanik baru hanya jika operand, call path dan efek teramati menyanggah interpretasi alternatif.
5. **Alternative RNG:** tulis batas scan, decoder/loader yang dipakai, dan pola aktual. Hasil negatif raw signature tidak dapat menutup RNG rumus lain/tabel/frame/time/decompressed code.

Sebelum setiap run baru: ambil HEAD main dan Actions active/queued terbaru, konfirmasi tidak ada run tumpang tindih, pakai source/checkpoint salinan read-only, beri timeout keras, unggah laporan teks saja, lalu periksa cleanup/exit code/artifact. Tidak ada pekerjaan asinkron di luar run yang sedang dipantau.
