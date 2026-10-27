# Laporan penutupan riset reverse engineering — Langkah 4–10

Tanggal: 27 Oktober 2026  
Repositori: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`  
Sumber kriteria: [Audit Reverse Engineering Langkah 1–10](REVERSE_ENGINEERING_AUDIT_STEPS_1_10_2026-10-27.md).  
Batas: laporan ini menutup hanya hal yang benar-benar didukung bukti. Status tiap langkah **TUNTAS**, **SEBAGIAN**, atau **BLOKIR** berdasarkan ruang lingkup dan kriteria; sukses satu Actions run tidak otomatis berarti seluruh langkah selesai.

## Ringkasan status

| Langkah | Status akhir | Cakupan yang benar-benar ditutup |
|---|---|---|
| 4 — RNG, seed, caller, determinisme | **SEBAGIAN** | Formula/state RNG diverifikasi statis dan fungsi utamanya lulus eksekusi terisolasi. Perbandingan runtime pada satu checkpoint roulette menunjukkan stream caller/state serta viewport sama untuk dua pengulangan dan satu jeda berbeda. Seed boot, hubungan caller ke hasil roulette, caller battle, dispatch menyeluruh, dan RNG alternatif tetap terbuka. |
| 5 — perbandingan Ghidra/m2c | **TUNTAS (empat fungsi terpilih)** | Empat fungsi yang sama mempunyai output Ghidra dan m2c; kedelapan output C disimpan permanen. Tidak mengklaim merekonstruksi kode sumber asli atau semua fungsi. |
| 6 — alamat, setter, xref dan call chain | **SEBAGIAN** | Review tambahan atas log dekompilasi #40473737136 mendukung aliran statis `0x8011C0D0`: field record `+0x04` dinegasikan/dijepit ke `-9999` lalu masuk ke setter `0x8001387C`; cabang threshold lain menulis `+0x58B` dan `+0x5D2` sebelum memanggil `0x800EF98C`. Base `0x800D0000`, arti parameter/field, offset delta, serta efek transisi tetap UNKNOWN. [Step 6 addendum](STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md). |
| 7 — loader dan overlay | **SEBAGIAN** | Parser frame shell/Python dan report assembler telah diperbaiki; fixture #40484417534 lulus untuk frames 1,2,3,10,20,30,40 (max 40). Cold boot single-breakpoint terkoreksi [#40484548650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650) selesai `success`; pra-uji frame 50, kontrol listener-only frame maksimum 60, target `0x800AD454` mencapai frame 120 tanpa hit (`SINGLE_BREAKPOINT_HIT=NO`, count 0), exit 124 pada batas 35 detik, cleanup PASS. Artefak teks-only #12724961702 berukuran 3.960 byte, ZIP SHA-256 `27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71`. Runtime base, register/copy-size/checksum buffer, relokasi dan DATA2.BIN/DUMMY.BIN belum dibuktikan. [Laporan](STEP7_RUNTIME_COLD_BOOT_RESULT_2026-10-27.md), [run terkoreksi](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650). |
| 8 — penjelasan fungsi dan aturan game | **SEBAGIAN** | Pseudocode statis memperjelas negasi/clamp pada record `+0x04` dan urutan penulisan `+0x58B`/`+0x5D2` di cabang threshold, tetapi tidak mengidentifikasi semantik transaksi/transisi. Aturan biaya/barrier, battle/roulette/turn, efek kartu, dan syarat menang per mode tetap UNKNOWN. [Step 8 addendum](STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md). |
| 9 — eksekusi fungsi terisolasi | **TUNTAS untuk fungsi RNG `0x80035D78` saja** | Eksekusi MIPS32 terisolasi berhasil pada tujuh state; state baru, register `v0`, dan return sentinel cocok. Bukan pengganti emulator PS1 dan tidak menggeneralisasi ke fungsi lain. |
| 10 — indeks dokumentasi `out/logic.md` | **TUNTAS sebagai indeks audit** | Indeks mengacu ke laporan dan bukti terkini serta mencantumkan UNKNOWN. Status ini tidak berarti semua aturan permainan telah selesai direverse-engineer. |

## Matriks kriteria dan bukti

### Langkah 4 — RNG dan caller

| Kriteria | Status | Bukti / artefak | Yang masih kurang |
|---|---|---|---|
| 4(a) Generator, rumus, state RAM, asal/lifecycle seed | **SEBAGIAN** | [Trace statis](STEP4_RNG_TRACE_2026-10-27.md); [uji fungsi terisolasi Step 9](../out/step9/STEP9_UNICORN_RESULT_2026-10-27.md); runtime run #40474262267 | Getter/update formula teruji, tetapi sumber seed saat boot, seluruh writer/reseed path, dan lifecycle selama boot belum ditelusuri tuntas. Tidak ada setter hit setelah restore pada window yang diuji—ini tidak menentukan apa yang terjadi saat boot. |
| 4(b) Determinisme savestate/input/jeda, caller, viewport, hasil tampak | **SEBAGIAN** | [Runtime report](../out/step4/STEP4_RNG_RUNTIME_RESULT_2026-10-27.md); run [#40474262267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267), artifact [#12719024236](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267/artifacts/12719024236) | Repeat jeda 30 dan kontrol jeda 60 menunjukkan 127 panggilan sequence/caller/state-before yang cocok setelah normalisasi frame, sampel state sama, final state `0xA99DC6E7`, dan viewport crop sama. Frame capture terminal berbeda (167/169/171) dan caller belum dihubungkan ke hasil pemilihan roulette yang terlihat secara independen. |
| 4(c) Direct caller, pointer, jump table, dispatch, kode terdekompresi | **SEBAGIAN** | [Step 4 closure](STEP4_CLOSURE_2026-10-27.md); [Ghidra caller review #40455975408](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455975408); [scan signature](../out/step4_rng_signature_scan_2026-10-27.md) | Empat direct caller main EXE terdokumentasi; entry 0/1 raw call candidate sudah dipilah menurut status decode. Mapping base runtime hipotesis, reachability tertentu tidak pasti, beberapa boundary fungsi belum diketahui, dan scan pointer sempit tidak menyingkirkan seluruh indirect/JT/decompressed paths. |
| 4(d) Caller roulette dan battle | **SEBAGIAN** | Run [#40474262267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267) memakai checkpoint roulette yang diverifikasi | Callsite terlihat pada window roulette, tetapi hasil akhir roulette belum disambungkan kausal ke caller. Tidak ada checkpoint battle autentik yang digunakan dalam run ini; battle RNG caller UNKNOWN. |
| 4(e) RNG alternatif dan randomness non-fungsi | **SEBAGIAN** | [Raw LCG signature scan](../out/step4_rng_signature_scan_2026-10-27.md) dan [Step 4 closure](STEP4_CLOSURE_2026-10-27.md) | Scan mencakup file mentah yang disebut di laporan dan pola pengali/addend tertentu saja. Tidak menyingkirkan algoritme lain, tabel, frame/time-derived values, pointer call, atau kode yang didekompresi/dekripsi setelah loader. |

### Langkah 5 — perbandingan Ghidra dan m2c

**TUNTAS dalam batas empat fungsi yang terpilih.** Run [#40449144521](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40449144521), artifact teks #12710000931, menghasilkan output Ghidra C dan m2c C untuk `0x80015ADC`, `0x80015B7C`, `0x8001A328`, dan `0x80020BF4`. Empat pasang output tersedia pada [laporan Step 5](../out/step5/STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md). Kesesuaian dua decompiler meningkatkan keyakinan struktur kode, bukan bukti source asli atau semantic caller game.

### Langkah 6 — penulis memori, xref, call chain

**SEBAGIAN.** Sumber utama: [Step 6 semantic review](STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md), [artifact teks runner-only #12719587873](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136/artifacts/12719587873).
- Getter target `0x80012A70`: 8 xref terdekode pada address map kandidat; setter `0x8001387C`: 9; getter Chakra pemain `0x800138EC`: 16.
- Fungsi UI/penggambaran seperti `0x8012A9C4` dan `0x80137AD8` turut membaca target; karena itu getter xref tidak sama dengan caller kemenangan.
- `0x80112418` menunjukkan cabang pembandingan record/target dan kandidat panggilan transisi, tetapi dekompilasi transisi/batas fungsi bermasalah.
- Log runner yang telah ada menunjukkan `0x8011C0D0` menegasikan record `+0x04`, membatasi minimum ke `-9999`, lalu memanggil setter; kandidat threshold menulis `+0x58B` dan `+0x5D2` sebelum `0x800EF98C`. Ini adalah temuan statis pada base hipotetis, bukan semantik gameplay.
- Belum terbukti: pemetaan base entry 1 ke RAM runtime, sumber akhir field/delta `+0xB30/+0xB38/+0xB40/+0xB44` atau `+0x2E9/+0x2E5`, formula biaya, atau efek akhir transisi pada game.

### Langkah 7 — loader dan overlay

**SEBAGIAN.** Sumber: [laporan loader/overlay](STEP7_LOADER_OVERLAY_MAPPING_2026-10-27.md), [RESOURCE_CATALOG.md](../docs/RESOURCE_CATALOG.md), [OVERLAY_MAP.md](../docs/OVERLAY_MAP.md).
- Bootstrap DATA.BIN memuat 68 byte awal diikuti tabel direktori `0x2F00) byte dengan 1.504 entry (1.500 aktif).
- Instruksi sekitar kandidat `0x800AD454` mendukung salinan tabel direktori dari `0x800AD494` menuju `0x8006D830`, tetapi ini bukti statis.
- Base entry 0 `0x800AD000` dan entry 1 `0x800D0000` tetap HIPOTESIS; alamat muat nyata, relokasi, urutan load/unload, dan kontribusi executable DATA2.BIN/DUMMY.BIN belum dipetakan menyeluruh.


Catatan runtime final ada pada [laporan Step 7](STEP7_RUNTIME_COLD_BOOT_RESULT_2026-10-27.md). Parser frame memiliki regression fixture yang lulus. Run koreksi #40484548650 menghasilkan report lengkap: target probe mencapai frame 120 tanpa hit pada `0x800AD454`; no-hit dalam jendela observasi bounded tidak membuktikan target tak pernah berjalan.
### Langkah 8 — penjelasan fungsi dan aturan game

**SEBAGIAN.** Sumber: [laporan fungsi/aturan](STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md).
- TERVERIFIKASI statis: LCG, perilaku beberapa caller main EXE (indeks bounded/shuffle/filter-pick/struktur RNG), getter/setter Chakra utama, beberapa pembandingan record ke target, direktori resource.
- HIPOTESIS/UNKNOWN: makna kandidat pilihan, field record, pemicu mode, pending delta, transisi; formula biaya barrier/upgrade; aturan umum battle/roulette/turn, efek kartu, dan syarat menang per mode.
- Tidak ada fungsi yang dilabeli caller battle hanya berdasarkan alamat, nama default Ghidra, atau banyak pemanggilan.

### Langkah 9 — eksekusi MIPS terisolasi

**TUNTAS untuk fungsi RNG utama yang diuji.** Run [#40474891838](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474891838), artifact teks #12720127454, [laporan hasil](../out/step9/STEP9_UNICORN_RESULT_2026-10-27.md).
- Executable terverifikasi pada 385.024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
- Fungsi dijalankan pada alias fisik RAM yang sesuai, dengan 2 MiB RAM, state `0xA3118), return sentinel, serta batas maksimum 128 instruksi/vektor.
- Tujuh input state menghasilkan state baru dan `v0` yang tepat; tiap vektor kembali ke sentinel setelah 12 instruksi. `ISOLATED_RNG_FUNCTION_EXECUTION=PASS`, 7/7.
- Run pertama [#40474699863](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474699863) gagal 0/7 karena memory map KSEG virtual yang salah; diperbaiki pada sumber, dan run berikutnya berhasil. Private cleanup tercatat PASS.
- Batasnya: bukan emulator PS1, tidak menguji helper/caller/loader atau semua fungsi game; tidak menyimpulkan hasil roulette/battle.

### Langkah 10 — indeks dokumentasi

**TUNTAS sebagai indeks audit.** `out/logic.md` diperbarui untuk mengarah ke laporan ini, report per langkah, dan matriks status. Indeks tersebut memisahkan TERVERIFIKASI, HIPOTESIS, dan UNKNOWN; tidak mengklaim semua aturan gameplay sudah selesai.

## Temuan terverifikasi, hipotesis, dan UNKNOWN

### TERVERIFIKASI
- Header/ukuran/hash EXE yang dipatok cocok; Ghidra/m2c memproses empat fungsi terpilih.
- LCG utama: state update `(old × 0x41C64E6D + 0x3039) mod 2^32); output `(new >> 16) & 0x7FFF); fungsi MIPS yang sama lulus tujuh vektor terisolasi.
- Dalam window runtime checkpoint roulette: state awal pasca-restore, 127 hit, normalized caller/state stream, state akhir `0xA99DC6E7), dan crop viewport identik untuk tiga cabang. Bukti ini terbatas pada checkpoint/window tersebut.
- Direktori bootstrap DATA.BIN dan alur penyalinan tabel yang dijelaskan dalam laporan statis.

### HIPOTESIS
- Base RAM entry 0/1 `0x800AD000)/`0x800D0000).
- Label gameplay untuk sebagian caller/resource, semantics field record, pending amount, dan alasan branch masuk/keluar.
- Fungsi `0x80035DA8` sebagai seed setter yang dipanggil di jalur resource: bentuk instruksi dan static call candidate cocok, tetapi runtime boot lifecycle belum terbukti.

### UNKNOWN / BELUM TERBUKTI
1. Sumber seed saat boot dan seluruh lifecycle reseed, khususnya indirect/call via pointer/overlay.
2. Pemetaan runtime base/relokasi/lifecycle DATA.BIN entry, plus executable/decompressed code di DATA2.BIN dan DUMMY.BIN.
3. Caller tertentu yang secara kausal menentukan hasil roulette yang terlihat, serta runtime RNG caller pada battle dengan checkpoint autentik.
4. Seluruh jalur dispatch indirect/jump table dan RNG alternatif, termasuk berbasis tabel, frame/time, atau kode hasil dekompresi/dekripsi.
5. Makna field `+0x58B`, `+0x2E9`, `+0x2E5`, `+0x5D2`, `+0xB30), `+0xB38), `+0xB40), `+0xB44`; biaya barrier/level-up/Chakra; aturan battle/roulette/turn; victory logic lintas mode.
6. Eksekusi terisolasi fungsi game selain rutin RNG yang diuji apabila diperlukan untuk pertanyaan fungsi tertentu.

## Perubahan Git yang relevan

- `481ee437d4704da6a10ac7cb9a1406dae5cef9c9` — perbaikan referensi artefak review Step 6.
- `601a7287ec018a66efa1a4160b2bd610ddc9e84a` — laporan semantic review Step 6.
- `0fe56c5f455c397cb012f3978b11bdab9ef7af4e` — laporan loader/overlay Step 7.
- `5b11cacacf56cd97a18c6a9ecd510059cc1639a4` — laporan fungsi/aturan Step 8.
- `85e02a8d717c68f9b3b8b1aa07cd4089eea39aa3` — laporan runtime Step 4 dari log mentah #40474262267.
- `e35ef26390b5c9477f195a7c030897fdde836a22` — retry penulisan laporan Step 4 saat concurrent main update.
- `6d332244607298154c51fbd3f16ff7718483e6b2` — koreksi physical RAM map Step 9.
- `3e5a814c1f277096c73d44804683499ad67de977` — laporan uji MIPS terisolasi Step 9.

SHA HEAD sesudah pembaruan audit/handoff terbaru perlu diambil dari branch `main` pada saat commit terakhir dicatat di `STATUS.md`/handoff.

## Status Story Mode dan batas keselamatan

**Story Mode: TIDAK TERBUKTI TAMAT.** Tidak ada ending autentik yang diverifikasi dalam riset ini. Run Step 4 memakai checkpoint roulette untuk pengamatan RNG; run Step 9 menguji satu fungsi CPU MIPS saja. Tidak ada adaptive-player workflow atau Story Mode otomatis dijalankan/diubah. Tidak ada classifier, kebijakan input, marker Revision65, atau readiness gate diubah. ROM/disc, BIOS, Memory Card, savestate, RAM dump, dan screenshot privat tidak disimpan di Git; screenshot Step 4 hanya berada pada artifact privat Actions dengan masa retensi terbatas. Runner Step 9 menghapus direktori privat setelah tes.

## Handoff berikutnya

Lihat [handoff Langkah 4–10](HANDOFF_REVERSE_ENGINEERING_STEPS4_10_2026-10-27.md). Prioritas adalah analisis tambahan yang dapat diuji dari artefak teks yang sudah ada, atau eksperimen diagnostik terpisah yang benar-benar diperlukan untuk melengkapi seed lifecycle, runtime base mapping, dan caller battle. Jangan mulai kembali sistem pemain adaptif atau mengklaim selesai lebih dari bukti.

## Addendum penutupan — audit statis dan diagnostik terbaru (27 Oktober 2026)

- Workflow parser Step 7: [#40484417534](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484417534) lulus setelah fixture membuktikan ekstraksi frame yang benar. Ini menguji parser, bukan loader game.
- Single-breakpoint experiment [#40484519812](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484519812) memberi bukti dari raw log: progress sampai frame 100, no-hit pada alamat kandidat, exit 124 dari timeout 35 detik, dan cleanup PASS. Laporan otomatis awal gagal karena syntax error Python, sehingga raw log lebih berwenang daripada ringkasan artefak run tersebut.
- Commit koreksi report assembler `8326c07f71caeab12924133b0812ec7e86b8b1f7` diverifikasi melalui run [#40484548650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650), sukses pada 10:00:47 UTC. Artefak #12724961702 berukuran 3.960 byte, ZIP SHA-256 `27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71`; report parser memuat `SINGLE_BREAKPOINT_HIT=NO`, hit count 0, control max frame 60, progress YES, dan cleanup PASS. Ini memperbaiki pelaporan, bukan memvalidasi loader/base runtime.
- Pseudocode Step 6 yang sudah ada memperlihatkan operasi negasi/clamp dan beberapa code store bersyarat, tetapi tidak memberi dasar baru untuk menamai mekanik. Step 6/8 tetap SEBAGIAN dan field delta `+0xB30/+0xB38/+0xB40/+0xB44` tetap UNKNOWN.

Matriks langkah final: Step 4 SEBAGIAN; Step 5 TUNTAS untuk empat fungsi terpilih; Step 6 SEBAGIAN; Step 7 SEBAGIAN; Step 8 SEBAGIAN; Step 9 TUNTAS hanya untuk fungsi RNG `0x80035D78`; Step 10 TUNTAS sebagai indeks audit saja. Story Mode TIDAK TERBUKTI TAMAT. Run single-breakpoint #40484548650 tidak menyediakan hit/PC/register/copy-size/checksum buffer yang diperlukan untuk menutup Step 7.
