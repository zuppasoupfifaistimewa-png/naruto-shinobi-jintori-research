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
| 6 — alamat, setter, xref dan call chain | **SEBAGIAN** | Full-text artifact #12719587873 mengonfirmasi static stores `+0x2E9=0x3F`, `+0x2E5=0`, selector `+0x58B`, serta kode bersyarat `+0x5D2` pada lima kandidat entry-1; `0x8011C0D0` juga negate/clamp record `+0x04` ke `-9999` lalu memanggil setter `0x8001387C`. Base `0x800D0000`, arti field/kode, sumber final `+0xB30/+0xB38/+0xB40/+0xB44`, dan efek transisi masih UNKNOWN. [Step 6 report](STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md).
| 7 — loader dan overlay | **SEBAGIAN** | Loader probe #40484548650 pada `0x800AD454` mencatat progress frame 120 tanpa hit; base/runtime copy/checksum/relokasi belum terbukti. Seed-setter probe terpisah #40485987817 (utama untuk Step 4(a)) menguji hanya `0x80035DA8`, juga tanpa hit sampai frame 120; report fallback PC run itu salah, tetapi raw ready line menetapkan target yang benar dan koreksi parser diverifikasi oleh #40486315324. Kedua run cleanup PASS; hasil no-hit bounded tidak membuktikan target tidak pernah berjalan. [Laporan Step 7](STEP7_RUNTIME_COLD_BOOT_RESULT_2026-10-27.md), [loader run](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650), [seed run](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817). |
| 8 — penjelasan fungsi dan aturan game | **SEBAGIAN** | Raw MIPS clarifies selected threshold branches, extra gates, delay slots and stores, but codes/fields do not identify gameplay semantics. Costs, battle/roulette/turn rules, card effects and victory conditions remain UNKNOWN. [Step 8 report](STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md).
| 9 — eksekusi fungsi terisolasi | **TUNTAS untuk fungsi RNG `0x80035D78` saja** | Eksekusi MIPS32 terisolasi berhasil pada tujuh state; state baru, register `v0`, dan return sentinel cocok. Bukan pengganti emulator PS1 dan tidak menggeneralisasi ke fungsi lain. |
| 10 — indeks dokumentasi `out/logic.md` | **TUNTAS sebagai indeks audit** | Indeks mengacu ke laporan dan bukti terkini serta mencantumkan UNKNOWN. Status ini tidak berarti semua aturan permainan telah selesai direverse-engineer. |

## Matriks kriteria dan bukti

### Langkah 4 — RNG dan caller

| Kriteria | Status | Bukti / artefak | Yang masih kurang |
|---|---|---|---|
| 4(a) Generator, rumus, state RAM, asal/lifecycle seed | **SEBAGIAN** | [Trace statis](STEP4_RNG_TRACE_2026-10-27.md); [uji fungsi terisolasi Step 9](../out/step9/STEP9_UNICORN_RESULT_2026-10-27.md); roulette #40474262267; cold boot seed-setter #40485987817; static helper-return audit #40487406384 (in progress) | Seed-setter runtime probe tidak mendapat hit sampai frame 120. Koreksi delay-slot: `0x800AF2A8 li a0,-1` memberi argumen ke helper `0x80037138`; delay-slot `0x800AF2B0 move a0,v0` meneruskan return helper ke `0x80035DA8`, jadi argumen setter/state tersimpan belum diketahui. Ghidra run #40487406384 sedang menambahkan dekompilasi/xref helper return; hasil belum tersedia. Seed/lifecycle dan seluruh writer/reseed path tetap UNKNOWN. |
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
- Belum terbukti: pemetaan base entry 1 ke RAM runtime, seluruh pembaca/inisialisasi `+0x2E9/+0x2E5`, sumber final field/delta `+0xB30/+0xB38/+0xB40/+0xB44`, formula biaya, atau efek akhir transisi pada game.

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
5. Makna field/kode `+0x58B`, `+0x2E9`, `+0x2E5`, `+0x5D2` meski store sudah diketahui; sumber operand/final writer `+0xB30/+0xB38/+0xB40/+0xB44`; biaya barrier/level-up/Chakra; aturan battle/roulette/turn; victory logic lintas mode.
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
- Commit koreksi report assembler `8326c07f71caeab12924133b0812ec7e86b8b1f7` diverifikasi oleh #40484548650; artefak #12724961702 memuat no-hit pada `0x800AD454` dengan control max frame 60 dan cleanup PASS. Runtime seed setter [#40485987817](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817) juga sukses sebagai workflow tetapi tidak mendapat hit pada target tunggal `0x80035DA8`: raw progress frame 1–120, exit 124/35 detik, cleanup PASS. Artefak #12724933081 (4.003 byte; ZIP SHA-256 `74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6`) memiliki fallback PC yang keliru (`0x800AD454`) saat no-hit; source fallback diperbaiki dan divalidasi oleh #40486315324. Ini memperbaiki kualitas laporan, bukan membuktikan seed call atau loader/base runtime.
- Pseudocode Step 6 yang sudah ada memperlihatkan operasi negasi/clamp dan beberapa code store bersyarat, tetapi tidak memberi dasar baru untuk menamai mekanik. Step 6/8 tetap SEBAGIAN dan field delta `+0xB30/+0xB38/+0xB40/+0xB44` tetap UNKNOWN.

Matriks langkah final: Step 4 SEBAGIAN; Step 5 TUNTAS untuk empat fungsi terpilih; Step 6 SEBAGIAN; Step 7 SEBAGIAN; Step 8 SEBAGIAN; Step 9 TUNTAS hanya untuk fungsi RNG `0x80035D78`; Step 10 TUNTAS sebagai indeks audit saja. Story Mode TIDAK TERBUKTI TAMAT. Run single-breakpoint #40484548650 tidak menyediakan hit/PC/register/copy-size/checksum buffer yang diperlukan untuk menutup Step 7.

## Addendum penutupan — seed-setter probe dan parser fallback (27 Oktober 2026)

Run [#40485987817](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817) adalah cold boot bounded tanpa input/restore, hanya satu breakpoint pada kandidat `0x80035DA8`. Raw log: source checksum lulus; pra-uji frame 50; listener-only max frame 60; target progress frame 1–120 dengan `bp_hits=0`; timeout exit 124 setelah 35 detik; cleanup PASS. Artefak #12724933081, 4.003 byte, ZIP SHA-256 `74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6`. Karena tidak ada hit, tidak ada register `$a0/$ra/caller` runtime. Summary fallback PC pada artefak salah menyebut alamat loader lama; raw `STEP7_SINGLE_BP_READY` membuktikan target yang benar ialah `0x80035DA8`. Fallback dikoreksi pada `a6734d7fc57ff6dfab9b8135cd5661bf0278c437`, dan [validator #40486315324](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40486315324) menguji fallback/parser. Kriteria Step 4(a) tetap SEBAGIAN; Step 7 tetap SEBAGIAN; tidak ada bukti Story Mode tamat.

## Addendum — raw MIPS cross-check, independent of runtime blocker (27 Oktober 2026)

Artifact teks #12719587873 dari [Actions #40473737136](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136), ZIP SHA-256 e1ea68c92bcbf645fde3c991c8a47192b815987d8044f2d599c163c1f3ec9fb9, telah diperiksa langsung. Artifact memuat dekompilasi dan raw instruction windows DATA.BIN entry 1, offset 0x10BB000, ukuran 596.412 byte, SHA-256 entry 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a. Gameplay/emulator tidak dijalankan. Base entry-1 0x800D0000 tetap hipotetis.

- **TERVERIFIKASI-STATIS, bersyarat pada base tersebut:** site 0x80111228/0x801112CC/0x801113B4/0x801114F0/0x80111588/0x80112418 menghitung record stride 0x90, memanggil getter target 0x80012A70, membaca field +0x04, dan mengarahkan record_word < target ke 0x8011253C. Detail delay slot dan gate ada pada laporan Step 6.
- Store pada jalur tertentu mencakup +0x58B, +0x2E9, +0x2E5 dan halfword +0x5D2. Nilai +0x5D2 yang dilaporkan oleh dekompilasi bervariasi (0x200, 8, 4, 0x20, 0, 0x1000), bukan nama aturan. Di site 0x80111228, raw window berakhir sebelum store +0x5D2; nilai 0x200 hanya diklaim pada tingkat dekompilasi.
- 0x8011C0D0 secara kondisional menegasikan word record +0x04, menjepit hasil ke minimum -9999, menyimpannya, lalu meneruskan nilai/index ke setter main EXE 0x8001387C. Ini tidak menjelaskan apakah nilai itu biaya, pengembalian, sinkronisasi atau delta sementara.
- **UNKNOWN/BELUM TERUJI:** base/relocation runtime, arti branch code/transisi, seluruh pemakai +0xB30/+0xB38/+0xB40/+0xB44 dan hubungan kausal dengan gameplay yang terlihat.
- Koreksi Step 4 terpisah: callsite 0x800AF2AC → 0x80035DA8 memasukkan return helper 0x80037138 melalui move a0,v0 di delay slot JAL. Nilai -1 merupakan argumen helper, bukan input setter terverifikasi; return helper tetap UNKNOWN.

Status tetap Step 4 SEBAGIAN; Step 5 TUNTAS untuk empat fungsi terpilih; Step 6 SEBAGIAN; Step 7 SEBAGIAN; Step 8 SEBAGIAN; Step 9 TUNTAS untuk RNG utama saja; Step 10 TUNTAS sebagai indeks audit. Story Mode **TIDAK TERBUKTI TAMAT**.

## Addendum — audit delay-slot MIPS dan caller setter (27 Oktober 2026)

Bukti MIPS entry-0 pada base hipotesis `0x800AD000` memperlihatkan `jal 0x80037138` di `0x800AF2A4`, delay-slot `li a0,-1` di `0x800AF2A8`, lalu `jal 0x80035DA8` di `0x800AF2AC` dengan delay-slot `move a0,v0` di `0x800AF2B0`. Maka `-1` masuk ke helper, sedangkan setter menerima nilai balik helper. Klaim lama bahwa setter otomatis menerima `-1`/menulis `0xFFFFFFFF` ditarik kembali. `tools/ghidra/ExportRngCallerAnalysis.java` sekarang mengekspor helper `0x80037138` dan xref-nya; run statis #40487406384 belum selesai pada saat addendum ini ditulis. Jangan ubah status Step 4(a) dari SEBAGIAN sampai return/helper path dapat dibuktikan.

## Addendum — lebih rinci untuk candidate 0x8011C0D0 (27 Oktober 2026)

Dekompliasi terarah pada body fungsi kandidat berukuran 408 byte (base entry-1 hipotetis 0x800D0000) menyatakan: input dibatasi ke byte, dibandingkan dengan global efektif 0x80139F70, dan fungsi return dini jika nilainya sama; jika berbeda, global serta field base+0x618 diperbarui. Input nonzero memilih record dengan indeks global 0x8013EA88, menulis 8 di record+0x22, lalu mengiterasi jumlah peserta dari global 0x8013EA71. Untuk setiap record ber-stride 0x90, word +0x04 dinegasikan, dijepit minimum -9999, disimpan, lalu dikirim bersama indeks ke setter 0x8001387C. Perbandingan signed short base+0x10 plus unsigned short base+0x14 terhadap 0x101 memilih call 0x8003F5D0 atau store base+0x94A=1; 0x800F96A4 dipanggil pada jalur tertentu. Raw instruction window yang tersimpan hanya memuat awal fungsi sampai sekitar 0x8011C118, jadi rincian loop berasal dari dekompilasi, bukan seluruh raw listing. Caller, nilai runtime, dan makna transaksi belum dikenal; tidak ada dasar untuk menamai pola ini harga barrier/level-up. Field +0xB30/+0xB38/+0xB40/+0xB44 tidak dilacak menyeluruh. Step 6/8 tetap SEBAGIAN.


## Live checkpoint addendum — 27 Oktober 2026 17:26 WIB

Remote `main` was verified at `2ad2c8dcdcaeee718d656e8696d6853f48ec54a8` before the handoff refresh commit. Ghidra static run [#40487406384](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40487406384) remains `in_progress`: job `122132544196` has completed main EXE analysis and DATA.BIN entry 1; entry 0/helper `0x80037138` is still running, and artifact upload/cleanup are pending. No result is yet available for the helper return or seed lifecycle. The previous full Ghidra run took about 39m43s; this is only a historical reference, not a dependable ETA.

The new Step 6 detail for candidate `0x8011C0D0` is bounded decompiler evidence: input byte normalization, compare/update of global `0x80139F70`, record stride `0x90), negate/clamp/store of record word `+0x04`, and calls to setter `0x8001387C`. It does not establish cost/refund/transaction semantics because caller and runtime values are unknown and the raw instruction window does not cover the full loop. Candidate fields `+0xB30/+0xB38/+0xB40/+0xB44` still require whole-program access analysis. Overall statuses remain unchanged; Story Mode is not verified complete. No adaptive player, gameplay input, or savestate restore was run.

## Live audit checkpoint — 27 October 2026, 17:24 WIB

- Re-read the live `main` files and verified that the current commit before this checkpoint was `2ad2c8dcdcaeee718d656e8696d6853f48ec54a8`. GitHub connector does not expose a local working-tree status; no local clean/dirty claim is made.
- Re-fetched raw job logs and metadata for Step 7 run [#40484548650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650). Job `coldboot-loader` completed `success`; asset provenance in the log confirms disc label/ID `SLPS-03553 / SLPS03553` and BIOS `SCPH-7502 (EU)`. The observation logs show preflight frame 50, listener-only control max frame 60, target `0x800AD454` progress through frame 120 with `bp_hits=0`, and bounded timeout `124`. The report artifact is #12724961702, 3,960 bytes, digest `sha256:27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71`; raw job log explicitly confirms upload digest and `STEP7_PRIVATE_CLEANUP=PASS`. No breakpoint hit or register/copy-size/buffer-checksum evidence exists. The result remains a bounded no-hit, not proof the loader is absent or its base is known.
- Step 9 criteria/report review confirms the isolated-execution criterion is satisfied only for `0x80035D78`: 7/7 vectors, state and `v0` correct, sentinel return in 12 instructions, max bound 128, physical 2 MiB RAM alias. The criterion does not require an indiscriminate all-functions sweep; no extra probe is justified absent a specific new claim.
- Active Actions run: [#40487406384](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40487406384), job `Verify and analyze PS-X EXE` / `122132544196`, step 11 `Extract and analyze DATA.BIN entry 0 for external helper` is `in_progress`. It began 17:18:13 WIB. The prior comparable full Ghidra run took about 39m43s, so an indicative finish is around 17:58 WIB, not a guarantee. Do not launch overlapping diagnostic work; inspect final logs/artifact after this run completes.
- No adaptive-player/Story Mode workflow, gameplay input, savestate restore, classifier/policy/readiness-gate edit, or private asset commit was performed. Story Mode remains `TIDAK TERBUKTI TAMAT`. Remaining Steps 4, 6, 7, and 8 stay partial; Step 5 remains complete only for four selected functions; Step 9 only for the RNG routine; Step 10 is an index, not proof of complete game understanding.
