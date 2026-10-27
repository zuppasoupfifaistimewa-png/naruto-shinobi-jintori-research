# LIVE CRITERION RECONCILIATION — 27 Oktober 2026

## Step 9 final update — all job steps completed success (21:02 WIB)

### Langkah 9 — uji isolasi diperluas

Artifact [#12740305973](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40516755810/artifacts/12740305973) dari run [#40516755810](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40516755810) sudah ada dan telah diperiksa: 4.567 byte, SHA-256 ZIP lokal/API cocok `bf1a702074849b2592bfc5555a0d493b5ed86d3de0b9895a192db7fdf9f80cd4`, empat file teks/log saja. Laporan aktual memuat `ISOLATED_RNG_FUNCTION_EXECUTION=PASS` (7/7), `ISOLATED_PLAYER_VALUE_ACCESSOR_TESTS=PASS` (16/16), `STEP9_ALL_TESTS=PASS`, serta `stage=isolated_function_pass`. Sepuluh kasus setter menguji nilai normal, clamp bawah/atas, nilai ekstrem, batas, dan indeks invalid; enam kasus getter menguji keempat slot, nilai negatif/maximum/all-bits-one dan indeks invalid.

Ada ketidaksesuaian API yang tidak boleh disamarkan: pada snapshot 21:00 WIB, metadata API masih menampilkan run dan job `queued` walaupun artefak yang terikat pada run yang sama sudah mengandung hasil eksekusi dan marker PASS. Karena itu, **hasil tes fungsi terisolasi diverifikasi dari isi artefak**, tetapi run-level conclusion dan cleanup workflow belum dinyatakan terkonfirmasi sampai status API diperbarui. Tidak ada gameplay, PS1 emulator, BIOS, input atau savestate yang digunakan. Rincian dan tabel hasil: [laporan Step 9](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/out/step9/STEP9_UNICORN_RESULT_2026-10-27.md).



## Step 5 — hasil perluasan terverifikasi (27 Oktober 2026, 20:50 WIB)

- Retry [#40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524) **completed/success** pada 20:50:53 WIB. Artefak teks [#12739676233](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524/artifacts/12739676233) berukuran 941.176 byte, digest API dan SHA-256 lokal cocok: `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d`. ZIP memuat 45 file teks/C/disassembly/log, termasuk 26 file C Ghidra/m2c nonempty; tidak ada ROM/BIN/CUE/EXE/BIOS, Memory Card, savestate, RAM dump atau screenshot. Semua langkah job selesai, termasuk penghapusan input/proyek sementara.
- Pemeriksaan aktual: `metadata_parser_fixture=PASS`, `function_metadata=PASS`, `functions_requested=13`, `functions_with_m2c_output=13`, laporan akhir `status=SUCCESS`. Masing-masing fungsi memiliki keluaran C Ghidra dan m2c; exit code m2c 0 untuk 13/13.
- Lingkup 13 target main EXE: empat caller RNG terdahulu; setter/getter nilai pemain pada `0x8001387C`/`0x800138EC`; RNG `0x80035D78`; helper `0x80037138`; dispatcher/initializer/callback routines `0x800373F8`, `0x8003755C`, `0x80037B58`, `0x80037BB0`, `0x80037C48`. Ini cross-check struktur same-address berdasarkan batas fungsi Ghidra, bukan kesamaan source asli atau bukti aturan gameplay.
- Percobaan pertama [#40512956924](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40512956924) gagal karena `0x80012A70` tidak memiliki fungsi Ghidra pada alamat itu dan tak memiliki metadata body. Perbaikan di [commit `2b16e67bfafde873c95b577bc030f6e0c9f84c58`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/2b16e67bfafde873c95b577bc030f6e0c9f84c58) mengeluarkan target itu dari daftar fungsi yang dibandingkan. Identitas/semantik target `0x80012A70` tetap perlu diperjelas; jangan anggap cross-check fungsi tersebut sudah berhasil.
- **Status Langkah 5 secara keseluruhan tetap SEBAGIAN** terhadap cakupan yang diminta: 13 fungsi inti executable utama sudah dibandingkan, tetapi fungsi kandidat di DATA.BIN entry 0/1 (termasuk pembanding target/record dan transisi), semua hubungan caller/callee wajib, serta seluruh executable belum dicakup m2c secara menyeluruh. Status lama “empat fungsi saja” adalah riwayat sebelum perluasan, bukan hasil terbaru.
- Run Ghidra statis terpisah [#40512917437](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40512917437) masih `in_progress`, dimulai 20:32:30 WIB, pada langkah analisis DATA.BIN entry 0 untuk external helper. Pembanding Ghidra sebelumnya #40498208067 membutuhkan sekitar 31 menit 47 detik; perkiraan kasar berdasarkan durasi itu sekitar **21:04 WIB**, bukan ETA terjamin.


## Update terbaru — Step 6 address provenance tool audit, 27 Oktober 2026 20:25 WIB

**Checkpoint terbaru Step 6 (27 Oktober 2026, 20:25 WIB):** scanner provenance di https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/0afc0eec4a5c12e4df5a17c771c8b0d28d7a99dd dijalankan oleh [Actions #40511758146](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40511758146) — completed/success pada 20:25:48 WIB. Artifact [#12737611770](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40511758146/artifacts/12737611770), 229.233 byte, SHA-256 ZIP `b84ff017cdbefb8ece6d04a7c8bef66b3fdc27b61412e91e10cc01485225b126`; digest API sama dengan SHA lokal. Enam anggota ZIP hanya teks/log; `text_only_output_count=6`, `private_binary_in_artifact=no`, `STEP6_PRIVATE_CLEANUP=PASS`. Fixture parser operand dan fixture pembentukan alamat `lui/ori/addiu/sign-extension` benar-benar mengeluarkan PASS. Laporan: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/docs/STEP6_REGISTER_PROVENANCE_AUDIT_2026-10-27.md.

Cakupan trace pointer meningkat, tetapi bukti baru menunjukkan batas konkret alih-alih menutup alias penuh: `a0` pada group +B30/+B38/+B40 didapat dari instruksi `lw a0,-0x5AAC(s0)` di 0x8012C628; peran `s0` belum dibuktikan dan trace source berhenti di control-flow boundary; +B44 read tracing berhenti di branch 0x8012CAF8. Matriks tidak dipromosikan: 6(a) SEBAGIAN, 6(b) BLOCKED, 6(c) SEBAGIAN, 6(d) UNKNOWN. Step 4, 7, 8, 9 dan 10 juga tetap pada status dan cakupan sebelumnya.

---



The latest aggregate Step 6 direct-operand census is complete only for recognized integer/coprocessor load-store operands decoded by Ghidra and rendered as displacement(base) in the hypothetical entry-1 view; per-instance contexts remain capped at 200 for common offsets. This does not validate the entry base at runtime or complete pointer/alias analysis. See the 17-item matrix with status, artifact hashes, acceptance gaps and Actions URLs in [live reconciliation](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/docs/STEP4_10_LIVE_RECONCILIATION_2026-10-27.md).

Use criterion-level status rather than overall workflow success. Current high-level statuses: Step 4 SEBAGIAN; Step 5 SEBAGIAN (13 main-EXE function pairs validated; DATA.BIN candidate-function coverage incomplete); Step 6 SEBAGIAN with alias BLOCKED and field semantics UNKNOWN; Step 7 SEBAGIAN with runtime mapping BLOCKED; Step 8 SEBAGIAN with game-rule semantics UNKNOWN; Step 9 complete only for RNG routine 0x80035D78, broader coverage UNKNOWN; Step 10 TUNTAS only as an audit matrix. Story Mode TIDAK TERBUKTI TAMAT.

---

# Live reconciliation — 27 Oktober 2026, 19:22 WIB

Bagian di bawah merupakan laporan historis yang perlu dibaca dengan koreksi ini: Ghidra run #40498208067 SUDAH SELESAI (success) pada 19:14:42 WIB, bukan masih berjalan. Artefak #12732952776, 2.255.170 byte, SHA-256 ZIP 6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6. Run-only audit [#40503223693](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40503223693), artifact #12733512950 (13.079 byte; ZIP SHA-256 382773f9a421835bc97c448c630a2ea5d3891309bb34094f5a67027548c03414), membuktikan metadata dan digest cocok serta RUNNER_ARTIFACT_CLEANUP=PASS.

Step 6 scan #40500058788 juga success; artifact #12731474756 180.174 byte, ZIP SHA-256 4aea20e1420292505666f15898ba2db57a875a4fc67fbe2c65336af0a16fc9f4; cleanup PASS, private binary not uploaded. Batas scan dan matriks kriterianya dirinci di [closure report](STEP4_10_CLOSURE_REPORT_2026-10-27.md). Step 10 kini TUNTAS hanya sebagai matriks closure audit per-kriteria yang memetakan evidence atau blocker secara eksplisit; bukan bukti bahwa semua langkah gameplay sudah tuntas.

---

# Audit Reverse Engineering Langkah 1–10 — 27 Oktober 2026

## Cakupan dan keselamatan

Satu-satunya repositori yang digunakan: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research. Audit ini menggabungkan analisis statis, eksperimen runtime RNG terukur pada checkpoint roulette, dan satu uji CPU MIPS yang terisolasi. Tidak ada workflow pemain adaptif/Story Mode otomatis dijalankan, tidak ada classifier/policy/Revision65/readiness gate yang diubah, dan tidak ada ending Story Mode yang diklaim. Restore checkpoint hanya terjadi pada eksperimen diagnostik Step 4 yang dibatasi. Aset ROM/disc, BIOS, Memory Card, savestate, dump RAM, dan screenshot gameplay privat tidak ditambahkan ke Git; screenshot diagnostik privat disimpan hanya pada artifact Actions ber-retensi terbatas.

Checkpoint awal remote main: 62a4c114b7ac7a55ae9eb6d91bc4c9bfaef1c2ef.
- Step 5 Ghidra/m2c [run #40449144521](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40449144521): **success** pada SHA checkpoint tersebut; artefak teks #12710000931.
- Ghidra statis executable utama dan survei DATA.BIN [run #40442572534](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40442572534): **success**; artefak teks #12707638949.
- API Actions untuk status in_progress dan queued masing-masing mengembalikan nol run. Tidak ada ETA aktif.

## Tabel status Langkah 1–10 — live reconciliation 27 Oktober 2026, 21:41 WIB

| Langkah | Status | Ringkasan dan batas bukti |
|---|---|---|
| 1 — Struktur disc dan inventaris | **SELESAI** dalam lingkup inventaris/identitas | BIN/CUE dan file utama telah divalidasi pada runner sebelumnya; aset privat tidak di-commit. |
| 2 — Header PS-X EXE | **SELESAI** untuk konsistensi struktur yang diuji | Ukuran/hash/header/entry/load fields cocok pada validasi terdokumentasi. |
| 3 — Ghidra headless | **SELESAI** untuk main EXE import/index | Run #40512917437 sukses dan mengeluarkan 1.206 baris function index main EXE. Ini tidak membuktikan runtime mapping resource. |
| 4 — RNG | **SEBAGIAN (kriteria 4a–4e secara keseluruhan)** | Formula/state/output dan 7/7 vector tests; bounded contexts #40521136060/#40521136038. Entry-0 delay slot membuktikan helper return ke setter. Seed/lifecycle runtime, caller boundary lengkap, reachability dan hubungan ke roulette/battle/indirect RNG masih UNKNOWN. Lihat [Step 4 trace](STEP4_RNG_TRACE_2026-10-27.md). |
| 5 — Ghidra/m2c dan cakupan fungsi | **SEBAGIAN (14 fungsi terpilih cross-checked)** | 13 fungsi main EXE run #40515356524 dan satu fungsi resource entry-1 `0x800ED8C8` run #40523020556 memiliki output Ghidra/m2c sukses pada boundary sama. Target `0x80012A70` belum tervalidasi sebagai function entry pada view sebelumnya; transisi/compare/callgraph dan coverage keseluruhan belum lengkap. |
| 6 — Memory writes, XREF, pointer/alias, call chain | **SEBAGIAN** | #40522772847 memberi CFG/SSA pada `0x8012C544`/`0x8012CACC`: read `+B30/+B38` → add → write `+B40`; `+B44` consumer di jalur bercabang. Pointer global `0x8013A554`, alias lintas fungsi dan semantik field belum terselesaikan. 6(a) partial, 6(b) BLOCKED, 6(c) partial, 6(d) UNKNOWN. Lihat [CFG/SSA audit](STEP6_CFG_SSA_DATAFLOW_AUDIT_2026-10-27.md). |
| 7 — Loader dan overlay | **SEBAGIAN** | Struktur direktori dan jalur bootstrap copy statis terdokumentasi, namun destination/length/checksum runtime, relocation, lifecycle, pemetaan DATA2.BIN/DUMMY.BIN masih UNKNOWN/BLOCKED. Base `0x800AD000` dan `0x800D0000` tetap hipotesis. |
| 8 — Semantik fungsi/aturan permainan | **SEBAGIAN** | Satu candidate function memakai `RNG % 250` untuk dibandingkan dengan byte record; raw MIPS memuat pointer dari slot global `0x8013EA74`. Ghidra dan m2c agree pada boundary/call structure tetapi tidak pada representasi tipe/dereferensi pointer. Identitas fitur, nilai pointer runtime, field semantics, costs, barrier/upgrade, cards, turns, victory/loss rules masih UNKNOWN. |
| 9 — Pengujian fungsi terisolasi | **SEBAGIAN keseluruhan** | #40516755810 success: RNG 7/7; setter/getter nilai pemain 16/16; pemeriksaan register/memori/sentinel dan cleanup PASS. Ini CPU/RAM test terisolasi, bukan emulasi PS1 atau oracle seluruh gameplay. Subset RNG dan accessor yang diuji boleh ditandai TUNTAS hanya pada cakupan kasus tersebut. |
| 10 — Matriks rekonsiliasi | **TUNTAS sebagai audit dokumentasi per-kriteria saja** | Status, bukti, run/artifact, batas, serta blocker diindeks pada matriks dan laporan. Ini bukan pernyataan reverse engineering keseluruhan tuntas atau game tamat. |

## Langkah 1 — struktur disc

**VERIFIED (catatan ekstraksi terdahulu dan validasi runner terbaru):**
- Disc BIN berukuran 325.989.552 byte, dump sektor raw PS1 2.352 byte/sektor, serial SLPS-03553, SHA-256 58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88.
- File dan ukuran: SLPS_035.53 385.024 byte; DATA.BIN 66.015.232 byte; DATA2.BIN 166.428.672 byte; DUMMY.BIN 50.667.520 byte; SYSTEM.CNF 68 byte; XASECT.BIN 692 byte.
- SYSTEM.CNF menunjuk SLPS_035.53 sebagai executable boot. Catatan metode menggunakan bchunk/xorriso untuk ekstraksi BIN/CUE pada runner; tidak ada nilai tambah terverifikasi dari mengulang ekstraksi hanya untuk memakai dumpsxiso.
- Rincian ada di [ROM_STRUCTURE.md](ROM_STRUCTURE.md) dan [RESOURCE_CATALOG.md](RESOURCE_CATALOG.md). Hash file hasil ekstraksi lainnya adalah catatan lama yang terdokumentasi; semuanya tidak dihitung ulang satu per satu pada sesi ini.

## Langkah 2 — header PS-X EXE

**VERIFIED** untuk SLPS_035.53 dengan SHA-256 a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569:
- Magic PS-X EXE; panjang file 385.024 byte (0x5E000).
- Blok text dimulai pada offset file 0x800; load base 0x80010000; text size 0x5D800 (382.976 byte).
- Entry PC 0x80011448 berada dalam rentang text [0x80010000, 0x8006D800).
- 0x800 + 0x5D800 = 0x5E000, cocok dengan panjang file; field data/BSS terpisah pada header bernilai nol.
- Validasi entry PC, load address, text size, header-plus-text, entry-in-text, dan file length lulus pada run #40442572534.
- SYSTEM.CNF STACK 0x801FFF00 dan header initial SP base 0x801FFFF0 berasal dari field berbeda; tidak boleh disamakan atau disebut bug tanpa bukti loader.

## Langkah 3 — Ghidra headless

**VERIFIED:** [run #40442572534](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40442572534) berhasil pada executable dengan hash cocok. Toolchain: Ghidra 12.2, Temurin JDK 25, MIPS:LE:32:default, BinaryLoader, offset 0x800, length 0x5D800, load base 0x80010000, entry 0x80011448; indeks berisi 1.206 baris fungsi. Artefak #12707638949 berisi teks/log saja, bukan executable atau project Ghidra. Jumlah fungsi yang dikeluarkan untuk entry DATA.BIN bergantung konfigurasi/root analisis dan bukan jumlah fungsi sumber asli yang terverifikasi.

## Langkah 4 — RNG

**VERIFIED secara statis:** rutin pada alamat 0x80035D78 membaca/memperbarui global 0x800A3118 dengan operasi 32-bit: state = state × 0x41C64E6D + 0x3039 modulo 2^32; output = (state >> 16) & 0x7FFF.

Empat direct-JAL call sites dari main EXE:
- 0x80015B14 di FUN_80015adc: indeks/offset berbatas melalui helper daftar.
- 0x80015BF0 di FUN_80015b7c: pertukaran byte berulang, konsisten dengan shuffle tabel.
- 0x8001A460 di FUN_8001a328: kandidat berbasis pemeriksaan bit/kode lalu pilihan acak ke DAT_80089DA9.
- 0x80020C24 di FUN_80020bf4: inisialisasi struktur dan penyimpanan hasil RNG modulo 0x1000 ke param_1[0xD].

Instruksi di 0x80035DA8 cocok dengan penulisan argumen pertama ke state yang sama, tetapi penamaan sebagai seed setter masih **PROVISIONAL**: tidak ditemukan direct-JAL caller pada main EXE. Seed awal, call via pointer, dan caller overlay belum diketahui. Jangan menamai domain fungsi sebagai roulette/battle/AI/turn tanpa bukti tambahan. Rujukan: [STEP4_RNG_TRACE_2026-10-27.md](STEP4_RNG_TRACE_2026-10-27.md) dan [rng_candidate.md](../out/rng_candidate.md).

## Langkah 5 — perbandingan m2c

**VERIFIED:** run #40449144521 sukses pada commit sumber 62a4c114b7ac7a55ae9eb6d91bc4c9bfaef1c2ef; artefak #12710000931 (digest ZIP SHA-256 b2fdb6dc3213137e98e0ed298402e1d4b02198ed5310f264780bd8e965246b08). Empat entry yang sama dianalisis oleh Ghidra dan m2c: 0x80015ADC (160 byte), 0x80015B7C (240), 0x8001A328 (376), 0x80020BF4 (156). Semua empat keluaran Ghidra C dan empat keluaran m2c C tidak kosong; alamat RNG 0x80035D78 serta shared call-token set cocok per pasangan fungsi. spimdisasm 1.42.4 exit 0; m2c commit c632946b8cfbe8fce442b522dba92dfa72f1f317. Ini cross-check struktur statis, bukan rekonstruksi sempurna kode sumber asli. Keluaran permanen: [STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md](../out/step5/STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md).

## Langkah 6 — alamat, setter, dan cabang target Chakra

### Main EXE

**VERIFIED secara statis** melalui dokumentasi dan cross-reference:
- 0x80012A70 adalah getter target konfigurasi Chakra.
- 0x8001387C adalah setter Chakra pada executable utama; setter memvalidasi indeks pemain dan menjepit rentang nilai. Getter nilai Chakra pemain ada pada 0x800138EC.
- Pemanggilan setter di resource tidak otomatis berarti transaksi biaya; caller bisa menyalin, menyinkronkan, atau memulihkan nilai.
- Survei entry 1 mencatat sembilan call sites menuju 0x8001387C pada base hipotetis: 0x800D6D60, 0x800D6E04, 0x800D7AB0, 0x800D7B14, 0x800D8DE8, 0x800E1848, 0x8011C198, 0x80104790, dan 0x801016E8. Alamat runtime resource belum terverifikasi.

Dekompilasi statis kandidat entry 1 pada 0x8011C0D0 menunjukkan cabang yang membandingkan argumen dengan global state; jika nilainya berbeda, ia memperbarui global dan sebuah field pada struktur. Pada cabang argumen nonzero, ia mengiterasi peserta dengan stride 0x90, membalik tanda word pada field +0x04, menjepit hasil minimum ke -9999, lalu mengirim nilai itu ke setter main EXE 0x8001387C untuk setiap peserta. Jalur dapat memanggil helper 0x8003F5D0 dan FUN_800F96A4. **VERIFIED hanya sebagai urutan instruksi/dekompilasi pada base kandidat**; pemicu/makna mode dan alamat runtime resource tetap provisional. Ini tidak membuktikan biaya barrier atau nama aturan seperti "red debt".

### Cabang perbandingan target di entry 1

Pada base analisis **hipotetis** 0x800D0000, enam kandidat 0x80111228, 0x801112CC, 0x801113B4, 0x801114F0, 0x80111588, dan 0x80112418 memanggil getter target 0x80012A70. Dua referensi tambahan berada di call sites 0x8012AA2C dan 0x80137C34; referensi itu sendiri tidak menetapkan jalur kemenangan.

Secara statis, keenam kandidat membandingkan field record (alamat record dihitung dengan stride 0x90) dengan target getter. Sejumlah jalur menulis offset struktur +0x58B, +0x2E9, +0x2E5, +0x5D2 atau global sekitar 0x80139F3B, lalu memanggil kandidat transisi 0x800EF98C. Ada pengujian flag 0x200 dan kode yang ditulis ke +0x5D2 berbeda antar cabang: 0x200, 8, 4, 0x20, atau pilihan 0/0x1000. Kode tersebut **belum diberi nama gameplay** karena base, nama field, call chain dan fungsi transisi belum tervalidasi. Ghidra gagal mendekompilasi 0x800EF98C; keluaran kandidat 0x80100DCC juga menunjukkan masalah batas fungsi/register. Efek akhir transisi tetap UNKNOWN.

### Delta/pending yang belum terbukti

**UNKNOWN:** penulis final dan sumber operand untuk field kandidat +0xB30, +0xB38, +0xB40, +0xB44 dan hubungan dengan biaya barrier/level-up. Catatan terdahulu menyebut pending amount diproses bertahap ketika state +0xB2A == 7; itu belum membuktikan bahwa delta tersebut transaksi biaya. Jangan menyebutnya biaya barrier tanpa store/caller/sumber nilai yang terbukti.

**Status Langkah 6:** xref dan disassembly telah dipetakan sebagian, tetapi base runtime resource, dekompilasi sejumlah caller/transisi yang cacat, sumber delta, field record tepat, dan semantik kemenangan per mode tetap menjadi blocker. Perbandingan threshold statis bukan bukti aturan menang universal Story Mode.

## Langkah 7 — resource dan overlay

**VERIFIED:** bootstrap DATA.BIN 0x44 byte diikuti tabel direktori 0x2F00 byte yang memuat 1.504 entry; rincian pada [RESOURCE_CATALOG.md](RESOURCE_CATALOG.md).
- Entry 1: offset file 0x10BB000, 596.412 byte (0x919BC), SHA-256 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a. Base 0x800D0000 masih hipotesis; Ghidra mengekspor 1.555 baris fungsi di konfigurasi analisis itu.
- Entry 0: offset file 0x5F800, 110.536 byte, SHA-256 56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4. Base sekitar 0x800AD000 masih hipotesis. Kandidat alamat 0x800BDBFC muncul pada alur kontrol yang melompat ke alamat lain; jangan anggap label itu entry fungsi runtime yang sah.
- Instruksi MIPS dalam resource mendukung bahwa sebagian entry mungkin memuat kode. Hal itu tidak membuktikan semua resource adalah overlay kode atau DATA.BIN dimuat kontigu.

**UNKNOWN / belum tercakup:** loader runtime, alamat muat, relokasi, lifecycle, serta pemetaan menyeluruh DATA2.BIN dan DUMMY.BIN. Pemeriksaan hanya entry 0 dan 1 tidak boleh ditafsirkan sebagai pencarian menyeluruh yang negatif. Analisis statis #40442572534 bukan bukti breakpoint runtime. Parser VSync telah dikoreksi dan diuji dengan fixture #40484417534. Cold boot satu-breakpoint [#40484548650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650) selesai `success`: preflight no-breakpoint frame 50; kontrol debugger-listener-only max frame 60; breakpoint tunggal pada kandidat `0x800AD454` tidak hit, sementara VSync progress tercatat sampai frame 120; exit 124 pada batas 35 detik dan cleanup PASS. Artefak report teks #12724961702, 3.960 byte, ZIP SHA-256 `27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71`. Hasil bounded no-hit tidak membuktikan alamat loader tidak pernah berjalan; base `0x800AD000` dan `0x800D0000` tetap HIPOTESIS.

## Langkah 8 — penjelasan bahasa biasa

Dengan keyakinan tinggi dapat dijelaskan rumus LCG, empat caller langsung, rutin shuffle byte, pembentukan kandidat terfilter, setter Chakra utama, getter target, dan kelompok cabang resource yang membandingkan record dengan target. Keyakinan menengah berlaku untuk makna struktur/indeks. Semantik offset +0x58B, +0x2E9, +0x2E5, +0x5D2 dan +0xB30/+0xB38/+0xB44 tetap UNKNOWN. Formula biaya barrier, ekonomi Chakra, battle/roulette/turn, efek kartu, dan syarat menang per mode belum ditelusuri tuntas.

## Langkah 9 — verifikasi terisolasi

**SEBELUM uji 27 Oktober: TERBLOKIR.** Snapshot saat itu belum menjalankan rentang instruksi MIPS. Status kemudian berubah setelah probe terisolasi dilakukan: lihat bagian addendum terakhir dan [laporan Step 9](../out/step9/STEP9_UNICORN_RESULT_2026-10-27.md).

## Langkah 10 — indeks logika

Indeks out/logic.md diperbarui agar menautkan checkpoint terkini, laporan audit ini, dan keluaran persisten Step 5. Riwayat terdahulu tidak dihapus; bagian checkpoint bertanggal menjadi ringkasan status saat ini. Langkah 6–9 belum selesai sepenuhnya.

## Ringkasan VERIFIED / HYPOTHESIS / UNKNOWN

### VERIFIED
- Identitas disc, ukuran/hash yang tercatat, SYSTEM.CNF, dan inventaris file.
- Header PS-X EXE konsisten dengan panjang file; alamat load/entry/text.
- Ghidra headless untuk main EXE sukses dengan MIPS LE 32-bit; 1.206 baris fungsi.
- LCG di 0x80035D78, global 0x800A3118, empat direct-JAL caller main EXE.
- Ghidra/m2c berhasil membandingkan empat caller pada alamat sama; keluaran tersimpan permanen.
- Direktori DATA.BIN berisi 1.504 entry; entry 0/1 dianalisis statis; getter/setter Chakra utama dan xref tercatat.

### HYPOTHESIS / PROVISIONAL
- 0x80035DA8 adalah seed setter berdasarkan bentuk instruksi, tapi caller/seed tidak ditemukan di main EXE.
- DATA.BIN entry 1 di base 0x800D0000 dan entry 0 sekitar 0x800AD000.
- Beberapa cabang target terkait perubahan state/transisi pada konteks tertentu, tetapi arti state dan keberlakuan per mode belum ditentukan.
- Sebagian caller setter mungkin menerapkan perubahan tertunda, namun belum terbukti sebagai transaksi biaya.

### UNKNOWN / UNVERIFIED
- Seed runtime RNG serta caller tak langsung/overlay.
- Base RAM, relokasi, dan lifecycle resource sebenarnya.
- Sumber/penulis +0xB30/+0xB38/+0xB40/+0xB44 dan makna field record/kondisi pemicu.
- Formula universal biaya barrier/upgrade, battle/roulette/turn, serta kemenangan lintas mode.
- Pengujian terisolasi untuk fungsi selain RNG `0x80035D78` belum dilakukan; fungsi RNG tersebut sendiri sudah lulus 7/7 vektor Unicorn (lihat laporan Step 9).
- Tamat Story Mode: tidak dibuktikan oleh audit ini.

## Langkah berikutnya yang diizinkan

1. Pertahankan player dijeda; jangan jalankan workflow gameplay atau pulihkan savestate.
2. Lanjutkan tracing statis entry 0/1 atas tabel dan fungsi transisi: dokumentasikan store, caller, sumber operand, dan branch; jangan menamai delta sebagai biaya sebelum terbukti.
3. Validasi loader/base resource melalui bukti statis yang sah. Jika hanya bisa dibuktikan runtime, pertahankan UNKNOWN sampai lingkungan verifikasi yang disetujui tersedia.
4. Uji Unicorn terisolasi untuk RNG `0x80035D78` sudah lulus pada run #40474891838. Tidak ada kewajiban otomatis menguji setiap fungsi game satu per satu jika kriteria resmi tidak menuntutnya; setiap fungsi tambahan yang dijadikan dasar klaim harus memiliki entry/return, helper, register/memori, vektor, serta batas instruksi tersendiri. Jangan menggeneralisasi hasil RNG ke fungsi lain.


## Addendum Langkah 4 — 27 Oktober 2026

Status Langkah 4 pada tabel di atas diperbarui setelah pemindaian lintas resource dan konteks Ghidra. Ringkasan terotorisasi yang terbaru ada di [docs/STEP4_RNG_TRACE_2026-10-27.md](STEP4_RNG_TRACE_2026-10-27.md) dan [out/logic.md](../out/logic.md). Daftar caller resource: [144 call site entry 1](../out/rng_resource_entry1_ghidra_callers_2026-10-27.md), [36 local decode tanpa boundary fungsi](../out/rng_resource_entry1_unmapped_context_2026-10-27.md), dan [entry 0 plus seed setter](../out/rng_resource_entry0_ghidra_context_2026-10-27.md). Scan signature pengali LCG yang diketahui hanya menemukan kecocokan main EXE: [out/step4_rng_signature_scan_2026-10-27.md](../out/step4_rng_signature_scan_2026-10-27.md).

**Batas penting:** “SELESAI” di sini berarti inventaris instruksi direct-JAL yang ditemukan dalam aset raw yang di-scan telah dipetakan/didekode sejauh bukti memungkinkan. Ini bukan bukti absolut bahwa caller tidak langsung, code hasil dekompresi/dekripsi, alternative RNG dengan konstanta lain, atau pemuatan resource runtime tidak ada. Base `0x800AD000` dan `0x800D0000` tetap hipotesis. Tidak ada emulator/gameplay/savestate yang dijalankan.


## Addendum Langkah 0 — toolchain versioned dan terverifikasi (27 Oktober 2026)

Workflow [Step 0 #40457860945](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40457860945) selesai dengan **SUCCESS**. Pin versi, hash, dan hasil pengujian rinci dicatat di [out/versions.txt](../out/versions.txt); workflow ada di [.github/workflows/toolchain-audit.yml](../.github/workflows/toolchain-audit.yml).

| Komponen | Hasil |
|---|---|
| Python + pip | Python 3.13.18 dan pip 26.2.2 terpasang dan terverifikasi |
| Ghidra + Java | Ghidra 12.2 dengan hash arsip resmi tervalidasi; JDK Temurin 25.0.4.1; `support/analyzeHeadless` terdeteksi dan help/usage diverifikasi |
| dumpsxiso + mkpsxiso | Versi 2.30 terverifikasi dari banner `--help`; SHA-256 arsip Linux dicatat dan diverifikasi dalam workflow |
| m2c | Commit `c632946b8cfbe8fce442b522dba92dfa72f1f317` dipin; `m2c --help` berhasil |
| splat64 | 0.50.1; `splat --version` berhasil |
| Unicorn | 2.1.4; import berhasil dan engine MIPS32 little-endian berhasil dibuat |
| spimdisasm | 1.42.4 |
| objdump MIPS little-endian | Paket Ubuntu 24.04 `binutils-mipsel-linux-gnu=2.42-2ubuntu1cross5`; GNU objdump melaporkan versi 2.42 |

Catatan: beberapa CLI tidak menggunakan `--version` sebagai opsi versi mandiri. mkpsxiso/dumpsxiso mencetak versi di banner help, m2c meminta argumen berkas masukan, dan `analyzeHeadless -help` mengembalikan kode keluar 1 walaupun menghasilkan usage yang valid; semua fallback ini ditulis eksplisit di `out/versions.txt`.

**Batas:** ini menyelesaikan setup toolchain Langkah 0, bukan Langkah 9. Unicorn belum menjalankan satu fungsi game secara terisolasi dan tidak ada perbandingan terhadap save state. Run hanya mengunggah artefak teks; tidak ada emulator/gameplay, disc image, executable game, BIOS, memory card, savestate, RAM dump atau screenshot privat yang diunggah atau dimasukkan ke Git.


## Penutupan Langkah 4 — 27 Oktober 2026

Langkah 4 ditutup sebagai **SELESAI dalam cakupan inventaris statis yang dapat direproduksi**, bukan sebagai bukti kelengkapan runtime absolut. Laporan penutupan mengklasifikasikan semua hasil dan UNKNOWN tersisa: [STEP4_CLOSURE_2026-10-27.md](STEP4_CLOSURE_2026-10-27.md).


## Hasil final diperbarui — Langkah 4–10, 27 Oktober 2026 (snapshot Actions 08:38 UTC)

Laporan penutupan yang memuat matriks kriteria, referensi artefak, hipotesis/UNKNOWN, dan sisa pekerjaan: [docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md](STEP4_10_CLOSURE_REPORT_2026-10-27.md).

### Pembaruan Step 4 runtime

Run [#40474262267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267) menghasilkan tiga cabang diagnostik yang seluruhnya selesai pada tahap eksperimen: dua Circle input pada frame 30 lalu release 38, satu Circle input frame 60 lalu release 68; input readback PASS. Masing-masing mencatat 127 panggilan RNG, stream sequence/caller/state-before yang sama setelah nomor frame dinormalisasi, sampled RNG state yang sesuai, state akhir 0xA99DC6E7, serta SHA-256 viewport crop yang sama (a1b2dfab61a0922e2b466ddbeb6b5b2642a88289be159df4667e4e2bcaa53355). Tangkapan autentik X11 lolos validasi; event capture frame berbeda 169, 167, 171. Kesimpulan determinisme dibatasi pada stream dan viewport di checkpoint roulette tersebut; hasil pilihan roulette tidak dihubungkan secara kausal ke caller, dan tidak ada caller battle yang diuji. Job Actions keseluruhan gagal pada tahap penyimpanan laporan via API; laporan disusun ulang dari log mentah/artifact [#12719024236](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267/artifacts/12719024236) pada [out/step4/STEP4_RNG_RUNTIME_RESULT_2026-10-27.md](../out/step4/STEP4_RNG_RUNTIME_RESULT_2026-10-27.md).

**Keputusan Step 4 keseluruhan: SEBAGIAN**, karena subkriteria seed/lifecycle, pointer/dispatch menyeluruh, hubungan caller-ke-hasil roulette, caller battle, dan RNG alternatif masih terbuka. Penutupan statis lama tetap berlaku hanya untuk batas inventory yang dinyatakan eksplisit, bukan bukti lengkap runtime.

### Pembaruan Step 9 — fungsi MIPS terisolasi

Run pertama [#40474699863](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474699863) gagal 0/7: probe memetakan memory map pada KSEG virtual dan tidak mengeksekusi instruksi. Run kedua [#40474891838](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474891838) mengoreksi memory map menjadi alamat fisik RAM dan lulus 7/7 input state. Perubahan state/return register sesuai rumus LCG, masing-masing 12 instruksi, cleanup runner PASS; hanya report teks diunggah, tidak ada disk image/executable/RAM dump/savestate di Git. [Laporan isolasi](../out/step9/STEP9_UNICORN_RESULT_2026-10-27.md).

### Status final per langkah

- Langkah 4 — **SEBAGIAN** (overall; static caller inventory and bounded runtime behavior verified, lifecycle/call-meaning gaps open).
- Langkah 5 — **TUNTAS untuk empat fungsi terpilih** (Ghidra/m2c; eight persistent outputs).
- Langkah 6 — **SEBAGIAN** (xref/call chain statis terdokumentasi; runtime base/field/transitions UNKNOWN).
- Langkah 7 — **SEBAGIAN** (directory/bootstrap copy static; loader runtime and broad resource map UNKNOWN).
- Langkah 8 — **SEBAGIAN** (semantics evidence-backed; general game rules UNKNOWN).
- Langkah 9 — **TUNTAS untuk satu fungsi RNG utama** (7 isolated vectors; not a full PS1 emulator or all-game function test).
- Langkah 10 — **TUNTAS sebagai matriks closure audit per-kriteria**; this does not mean the game is fully reverse-engineered.

Story Mode remains **TIDAK TERBUKTI TAMAT**: no authentic ending was produced or reviewed in this work. Adaptive-player development and Story Mode automation remain paused; no classifier, input policy, readiness gate, or consumed player marker was changed.

## Addendum 27 Oktober — seed setter runtime dan parser fallback

Run #40485987817 (source workflow commit `e1e346e707254ad617a6cccad43689df908801a6`) selesai `success`; raw log memverifikasi checksum disc/CUE/BIOS/AppImage, preflight frame 50, listener-only frame 60, dan satu breakpoint target `0x80035DA8` dengan progress hingga frame 120 tetapi tanpa hit. Exit 124 adalah batas observasi 35 detik, bukan crash yang membuktikan ketiadaan call; cleanup PASS. Artefak teks #12724933081 4.003 byte, ZIP SHA-256 `74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6`. Summary artefak menyimpan fallback `SINGLE_BREAKPOINT_PC=0x800AD454` yang salah; raw `STEP7_SINGLE_BP_READY` menunjukkan target nyata `0x80035DA8`. Fix fallback dan tes regresi lewat validator #40486315324: `STEP4_SEED_BP_NO_HIT_FALLBACK_PASS target=0x80035DA8`, parser callback sintetis lulus, parser frame fixture lulus. Kriteria seed lifecycle Step 4(a) dan mapping Step 7 tetap UNKNOWN/SEBAGIAN.

## Addendum — raw MIPS branch/store audit (27 Oktober 2026)

Artifact #12719587873 from runner-only review [#40473737136](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136), ZIP digest e1ea68c92bcbf645fde3c991c8a47192b815987d8044f2d599c163c1f3ec9fb9, was inspected directly. It supplies raw MIPS windows at 0x80111228, 0x801112CC, 0x801113B4, 0x801114F0, 0x80111588, 0x80112418 and 0x8011C0D0. DATA.BIN entry 1 base 0x800D0000 remains a static hypothesis; no game/emulator was run.

Evidence supports selected-record calculation by index × 0x90, field +0x04, target getter 0x80012A70, and branch to 0x8011253C where record word is below target; site 0x801112CC first checks flag bit 0x200 at record +0x0A; site 0x801114F0 adds helper gate 0x800BDBFC(0x20) compared with global 0x8013EBB0; site 0x80111588 reads a different global byte and tests helper bit 0x1000; site 0x80112418 calls 0x80100D14(1) and 0x80100DCC(0xDF) on the accepted static branch; and 0x8011C0D0 negates/clamps record word +0x04 to minimum -9999, stores it and calls setter 0x8001387C.

These are operation/control-flow facts only. Halfword codes at +0x5D2 (0x200, 8, 4, 0x20, 0, 0x1000) are not assigned gameplay meaning. Pending fields +0xB30/+0xB38/+0xB40/+0xB44 were not present in this focused artifact; this is not a whole-program absence claim. Step 4 also received a correction: callsite 0x800AF2AC passes helper 0x80037138 return via move a0,v0; -1 is the helper input, not a proven setter input. Steps 6 and 8 remain **SEBAGIAN**.

## Addendum — record update path 0x8011C0D0 (27 Oktober 2026)

Bukti dekompilasi statis terarah (body 408 byte, DATA.BIN entry 1, base 0x800D0000 HIPOTESIS) menambah detail: argumen dinormalisasi ke byte, dibandingkan dengan global efektif 0x80139F70; jika sama, return dini. Jika berbeda, global dan field base+0x618 diperbarui. Jalur nonzero menulis 8 ke record terpilih +0x22, mengiterasi record stride 0x90, menegasikan word +0x04, clamp minimum -9999, menyimpan, dan memanggil setter main EXE 0x8001387C dengan indeks/nilai. Penjumlahan (signed short)[base+0x10] + (unsigned short)[base+0x14] < 0x101 memilih helper atau store base+0x94A=1; helper 0x800F96A4 juga dipanggil pada jalur tertentu. Raw MIPS window yang disimpan hanya mencakup awal fungsi; rincian loop berasal dari dekompilasi. Caller, nilai runtime dan arti field/helper UNKNOWN—tidak dapat dinamai sebagai biaya atau aturan gameplay. Field +0xB30/+0xB38/+0xB40/+0xB44 tetap belum dilacak menyeluruh.


## Addendum 27 Oktober — batas scan scalar immediate entry-1

Run [#40488847927](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40488847927) scanned 98,357 decoded instructions of DATA.BIN entry 1 under hypothetical base `0x800D0000`. The scan produced no exact scalar-immediate hits for `+0xB30`, `+0xB38`, `+0xB40`, or `+0xB44`. The scanner is not a complete memory-displacement, effective-address, register-alias, or non-decoded-code scan; this no-hit does not contradict observed `sb` stores at `+0x2E9/+0x2E5` in the Ghidra review artifact and does not prove the larger offsets are unused. Step 6 remains SEBAGIAN.

## Addendum — batas complete field access scan

The bounded immediate scan #40488847927 reports no exact scalar immediate hits for the queried offsets in 98,357 decoded entry-1 instructions. Its operand classifier does not prove the absence of MIPS memory displacement accesses, effective addresses assembled by register arithmetic, aliases, or instructions outside the decoded resource view. Explicit `+0x2E9/+0x2E5/+0x58B/+0x5D2` stores in the previous Ghidra artifact remain valid observations. The `+0xB30/+0xB38/+0xB40/+0xB44` dataflow question remains open.

## Addendum — runner audit terbaru untuk Langkah 4 dan 6 (27 Oktober 2026, 18:38 WIB)

Runner-only audit [#40497668341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40497668341) selesai success pada 18:38:45 WIB. Artifact audit #12730957210 berukuran 9.014 byte, ZIP SHA-256 `695e36bf70237913c0f80c94f0d4100732c92dd8b78155da2ace90d189c5ee24`; raw cleanup PASS. Pemindaian Step 6 terbaru yang diperiksa adalah run #40493556711, artifact #12729156734 (180.128 byte; ZIP SHA-256 `c9ea5ef0552a0c80a70f0d3a758622a358509de2079e5954dac3ce0032426e93`).

- **Langkah 4:** jalur negatif `a0<0` pada `0x80037138` memuat `0x80066E7C` ke `v0` dan mengembalikannya. Delay slot `li a0,-1` pada caller helper dan `move a0,v0` pada caller setter menghubungkan nilai global itu dengan argumen kandidat `0x80035DA8`, bersyarat pada callsite yang tercatat dan base entry-0 hipotetis `0x800AD000`. Nilai global saat boot dan runtime callsite tetap UNKNOWN. Step 4 **SEBAGIAN**.
- **Langkah 6:** `lw +0xB30` dan `lw +0xB38` dijumlahkan, hasil disimpan ke `+0xB40`; `+0xB44` memiliki store nol pada delay slot JAL dan pembacaan lanjutan ke argumen `a2` pada pemanggilan `0x8001B364`. Base entry-1 `0x800D0000`, object identity, runtime mapping, sumber nilai, dan semantik tetap UNKNOWN. Step 6 **SEBAGIAN**.
- Workflow helper pernah gagal karena grep marker terlalu spesifik; Ghidra mengeluarkan alamat tanpa prefiks `0x`. Peninjauan menemukan fragmen teks duplikat setelah akhir YAML; fragmen dibuang pada commit `029fdfab8df55dd16001916f0f53b7abd073c334`. Run koreksi #40497723766 harus diperiksa sebelum dianggap selesai; snapshot awal run tersebut masih berjalan.
- Tidak ada perubahan pada status Step 5/9 yang sudah tertutup dalam ruang lingkup terbatas atau Step 10 sebagai indeks audit. Story Mode tetap tidak terbukti tamat.

## Addendum — direct references untuk global return helper (27 Oktober 2026, 18:44 WIB)

Helper run [#40498231825](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498231825) success; artifact #12732006381, 9.058 byte, ZIP SHA-256 adfdb608af96dd95a7c7e74d9f8b117767aaffa817d0c7eb860757ead868d9ba. Runner-only audit [#40498386273](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498386273) success 18:44:35 WIB; artifact #12731327556, 9.727 byte, ZIP SHA-256 7826480f41372d68ddf3f4b1dfe6d99f51bbbb5cd124eb5c3c6169870150ba5c; cleanup PASS. Metadata, digest, size, artifact identity dan file text-only diverifikasi di runner.

Global executable 0x80066E7C mempunyai loaded-image bytes 00 00 00 00 (word LE 0), direct WRITE xrefs 0x80037B7C (sw zero) dan 0x80037BDC (sw v0 setelah addiu v0,v0,1), serta READ xrefs 0x80037BB4, 0x8003719C, 0x80037204, 0x80037260, 0x800372C0, dan 0x80037324. Fakta ini menyelesaikan sebagian pertanyaan asal data return helper, namun image value bukan runtime value. Initialization/order relative to 0x800AF2AC, caller semantics, indirect/overlay writers, runtime value and seed lifecycle tetap UNKNOWN. Step 4 tetap SEBAGIAN; Step 8 tetap SEBAGIAN.

## Addendum — callback-counter initialization path and helper-return source (27 Oktober 2026, 18:50 WIB)

Runner-only inspection [#40499154584](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499154584) completed `success` at **18:50:46 WIB**. Text artifact #12731114444: 11,783 bytes; ZIP SHA-256 `d1538c727c5945003d74a4ff7185c168068738bb854eafb61b36a52c348677d5`; raw log says `RUNNER_ARTIFACT_CLEANUP=PASS`. It validated metadata, run IDs, names, sizes, expiry and SHA-256 for the Ghidra index #12728867894, latest Step 6 scan #12729156734, and helper-function audit #12730814693, all inspected on runner. The helper artifact is from [#40499029428](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499029428), size 11,051 bytes, ZIP SHA-256 `abc53716169d19173ee68f9f033fdc14d87e99835f9febbef453e46628fddc07`; raw log records asset checksum checks OK, `STEP4_HELPER_PRIVATE_CLEANUP=PASS`, `text_only_output_validation=PASS`, and `uploaded_input_executable=no`.

### Facts from raw MIPS / static call references
- `0x8003755C` has an initialization guard based on word/halfword location `0x80065DB4`; if nonzero it returns without re-running the setup path. On the zero path, its code executes `jal 0x80037B58` at `0x800375F0`; the delay-slot instruction `sh v0,-0x3c(s0)` at `0x800375F4`, with `s0 = 0x80065DF0`, stores `1` to `0x80065DB4` before entering `0x80037B58`. Thus the guard is set as part of a one-time initialization path.
- `0x80037B58` writes `0x100` through the pointer loaded from `0x80066E80`, zeros global `0x80066E7C`, calls `0x80037C48(&0x80066E5C, 8)`, then constructs `a1 = 0x80037BB0` and calls `0x800373F8` with delay-slot `clear a0`. The static argument flow into that dispatcher is `a0=0, a1=0x80037BB0`.
- `0x800373F8` loads a function pointer through the global pointer at `PTR_PTR_80066E3C + 8` and invokes it with `jalr`. This makes “register callback” a strong hypothesis for the call from `0x80037B58`, but the pointed-to routine itself remains indirect and has not been semantically verified.
- `0x80037BB0` reads `0x80066E7C`, increments it, stores it back, then iterates over eight slots beginning at `0x80066E5C`, calling each nonzero slot by `jalr`. This and the zero-store in `0x80037B58` support describing `0x80066E7C` as a **callback-count/tick-like global** from static behavior, not as a verified gameplay field or seed value.
- Incoming reference evidence: `0x80037B58` has a direct JAL caller at `0x800375F0` in `0x8003755C`; `0x80037BB0` is passed as a function-pointer argument from `0x80037B8C`, not called by a direct JAL at that site. `0x8003755C` itself has a computed-call reference from `0x800373E0` in `0x800373C8` plus a data reference from `0x80066E28`.

### Boundary for Step 4
The helper `0x80037138` with input `a0=-1` returns current global `0x80066E7C`; candidate DATA.BIN entry-0 callsite `0x800AF2AC` passes that return through the setter's delay slot `move a0,v0`. It is now statically supported that this value can come from a zero-initialized and subsequently incremented callback-like counter. However, the order of the entry-0 callsite relative to the initializer/callback path is not established, entry-0 base `0x800AD000` remains HIPOTESIS, and no runtime value at the setter was observed. **Step 4 remains SEBAGIAN**; do not report a verified boot-time seed or a seed-lifecycle closure from this evidence alone.

Historical status superseded by live check: Ghidra run #40498208067 completed success at 19:14:42 WIB; artifact #12732952776 digest 6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6; runner audit #40503223693 validated it.

## Addendum — dispatcher and callback-table static trace (27 October 2026, 18:54 WIB)

Runner-only audit [#40499569324](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499569324) completed success at **18:54:03 WIB**. Text artifact #12731359299 is 12,452 bytes, ZIP SHA-256 `f37812b2932e9743bacc6311cca038a23c0725c3cacf7e4b8a25fdd26079caf6`; raw log records `RUNNER_ARTIFACT_CLEANUP=PASS`. It validated metadata, run ID, name, size, expiry and digest for helper artifact #12731593532 from run [#40499270568](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499270568): 11,672 bytes, ZIP SHA-256 `8567a5cad2a00823302ea7b361dd9b6eaab736bce6b77cf51ea136d6bee454b3`. That source run had `STEP4_HELPER_PRIVATE_CLEANUP=PASS`, `text_only_output_validation=PASS`, and `uploaded_input_executable=no`. All artifact bytes were processed on the GitHub Actions runner.

### Additional raw-MIPS findings
- Function 0x80037C48 zeroes a caller-supplied array for the number of 32-bit words passed in. Its caller 0x80037B58 passes base 0x80066E5C and count 8 (count is provided in the JAL delay slot), so the initialization path clears eight callback-pointer slots.
- Function 0x80037BB0 increments global 0x80066E7C and then visits eight words starting at 0x80066E5C, invoking each nonzero pointer with JALR. This is a concrete callback-list pattern.
- Function 0x800373F8 dispatches indirectly through the function pointer stored at PTR_PTR_80066E3C + 8. Its caller 0x80037B58 prepares a0=0 and a1=0x80037BB0 before this call, supporting—but not fully proving—the interpretation that 0x80037BB0 is being installed as a callback.
- Function 0x800373C8 dispatches indirectly through PTR_PTR_80066E3C + 0xC. Ghidra records a computed-call reference from 0x800373E0 to function 0x8003755C and a data reference at 0x80066E28; other callers also invoke this dispatcher. The initializer is therefore reached through an indirect dispatch path in the static view, not only through an ordinary direct JAL.
- Function 0x8003755C checks 0x80065DB4 and takes the initialization branch only when that guard is zero. Its call to 0x80037B58 at 0x800375F0 has delay slot SH v0,-0x3c(s0); because s0 is 0x80065DF0 there, this writes 1 to 0x80065DB4 before execution enters 0x80037B58. That function resets 0x80066E7C to zero, initializes the eight callback slots, then passes pointer 0x80037BB0 through the indirect dispatcher.

### Interpretation limits
The reset-then-increment behavior of 0x80066E7C is now **TERVERIFIKASI-STATIS** in the main executable. Its likely role as a callback/tick-like counter is a strongly supported inference from the indirect-dispatch table and eight-slot callback loop, not a verified gameplay-field name. The helper 0x80037138 with input a0=-1 returns the current value of that global. Therefore the candidate entry-0 callsite could pass this counter value to setter candidate 0x80035DA8 *if that callsite executes*. The relative runtime ordering of that resource callsite and the initialization/dispatch path is still unknown; entry-0 base 0x800AD000 remains HIPOTESIS, and no setter argument was captured at runtime. Step 4 remains **SEBAGIAN**.

Historical status superseded: Ghidra run #40498208067 completed success at 19:14:42 WIB; final artifact #12732952776 SHA-256 6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6 was verified by runner audit #40503223693.
