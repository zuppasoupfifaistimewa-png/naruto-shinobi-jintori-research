# Audit Reverse Engineering Langkah 1–10 — 27 Oktober 2026

## Cakupan dan keselamatan

Satu-satunya repositori yang digunakan: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research. Audit ini statis dan dokumenter. Tidak ada workflow gameplay/player di-dispatch, input gameplay dikirim, savestate dipulihkan, emulator dijalankan, classifier/policy/Revision65/readiness gate diubah, atau percobaan Story Mode dilakukan. Aset ROM/BIOS/Memory Card/savestate/screenshot gameplay tidak ditambahkan ke Git. Artefak yang diperiksa pada sesi ini hanya output statis berbentuk teks.

Checkpoint awal remote main: 62a4c114b7ac7a55ae9eb6d91bc4c9bfaef1c2ef.
- Step 5 Ghidra/m2c [run #40449144521](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40449144521): **success** pada SHA checkpoint tersebut; artefak teks #12710000931.
- Ghidra statis executable utama dan survei DATA.BIN [run #40442572534](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40442572534): **success**; artefak teks #12707638949.
- API Actions untuk status in_progress dan queued masing-masing mengembalikan nol run. Tidak ada ETA aktif.

## Tabel status Langkah 1–10

| Langkah | Status | Ringkasan dan batas bukti |
|---|---|---|
| 1 — Struktur disc dan inventaris | **SELESAI** | Inventaris ekstraksi terdahulu terdokumentasi dan source BIN/CUE/EXE divalidasi pada runner. Tidak dibongkar ulang hanya demi mengganti alat. |
| 2 — Header PS-X EXE | **SELESAI** | Ukuran, hash, header, entry point, load base, text length, dan panjang file konsisten; validasi header pada run terbaru lulus. |
| 3 — Ghidra headless | **SELESAI** | Ghidra 12.2, Temurin JDK 25, MIPS little-endian 32-bit; analisis berhasil dan ekspor indeks berisi 1.206 baris fungsi main EXE. |
| 4 — RNG | **SELESAI dalam cakupan statis main EXE** | LCG, state global, empat direct-JAL caller dan perilaku umum caller ditelusuri. Seed runtime, caller tak langsung, semantik gameplay/overlay tetap belum diketahui. |
| 5 — Caller RNG dan m2c | **SELESAI untuk empat caller yang dipilih** | Keempat entry fungsi dibandingkan oleh Ghidra dan m2c; semua output ada, perbandingan berhasil. Delapan keluaran C dan ringkasan disimpan permanen di [laporan Step 5](../out/step5/STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md). |
| 6 — Alamat, penulis memori, dan call chain | **SELESAI SEBAGIAN** | Setter Chakra utama dan beberapa cabang perbandingan target dapat dipetakan statis. Base resource hipotesis; beberapa dekompilasi gagal; sumber nilai dan semantik field penting belum terbukti. |
| 7 — Loader dan overlay | **SELESAI SEBAGIAN** | Direktori DATA.BIN dikenal; entry 0 dan 1 dianalisis statis. Base/lifecycle/runtime loader belum tervalidasi; DATA2.BIN dan DUMMY.BIN belum dipetakan menyeluruh sebagai kode executable. |
| 8 — Penjelasan fungsi | **SELESAI SEBAGIAN** | Penjelasan RNG, caller, dan kelompok threshold Chakra tersedia; semantik sejumlah field/state dan mekanik battle/roulette/turn belum diketahui. |
| 9 — Verifikasi terisolasi | **TERBLOKIR** | Belum ada eksekusi fungsi MIPS terisolasi via Unicorn atau emulator fungsi setara yang tervalidasi. Disassembly/decompiler adalah bukti statis, bukan verifikasi runtime. |
| 10 — Indeks out/logic.md | **SELESAI SEBAGIAN** | Indeks diperbarui untuk menunjuk audit dan keluaran Step 5 terbaru. Karena Langkah 6–9 belum tuntas, indeks tidak mengklaim semua aturan gameplay selesai. |

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

**UNKNOWN / belum tercakup:** loader runtime, alamat muat, relokasi, lifecycle, serta pemetaan menyeluruh DATA2.BIN dan DUMMY.BIN. Pemeriksaan hanya entry 0 dan 1 tidak boleh ditafsirkan sebagai pencarian menyeluruh yang negatif. Run #40442572534 adalah analisis statis, bukan breakpoint/debugger loader.

## Langkah 8 — penjelasan bahasa biasa

Dengan keyakinan tinggi dapat dijelaskan rumus LCG, empat caller langsung, rutin shuffle byte, pembentukan kandidat terfilter, setter Chakra utama, getter target, dan kelompok cabang resource yang membandingkan record dengan target. Keyakinan menengah berlaku untuk makna struktur/indeks. Semantik offset +0x58B, +0x2E9, +0x2E5, +0x5D2 dan +0xB30/+0xB38/+0xB44 tetap UNKNOWN. Formula biaya barrier, ekonomi Chakra, battle/roulette/turn, efek kartu, dan syarat menang per mode belum ditelusuri tuntas.

## Langkah 9 — verifikasi terisolasi

**TERBLOKIR.** Sesi ini tidak menjalankan rentang instruksi MIPS dengan Unicorn atau harness emulator fungsi setara yang tervalidasi. Ghidra, spimdisasm dan m2c adalah analisis statis saja. Tidak dilakukan probe gameplay/runtime. Penutupan blocker memerlukan emulator fungsi terisolasi yang dapat memodelkan register, branch/delay slot, dan memory map tanpa menjalankan game; setiap uji perlu mencatat state awal, register/memori, output yang diharapkan dan aktual, serta keterbatasan. Jika input biner tidak tersedia lewat lokasi yang disetujui tanpa memindahkan aset privat, status harus tetap UNVERIFIED.

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
- Verifikasi fungsi terisolasi menggunakan Unicorn/emulator setara.
- Tamat Story Mode: tidak dibuktikan oleh audit ini.

## Langkah berikutnya yang diizinkan

1. Pertahankan player dijeda; jangan jalankan workflow gameplay atau pulihkan savestate.
2. Lanjutkan tracing statis entry 0/1 atas tabel dan fungsi transisi: dokumentasikan store, caller, sumber operand, dan branch; jangan menamai delta sebagai biaya sebelum terbukti.
3. Validasi loader/base resource melalui bukti statis yang sah. Jika hanya bisa dibuktikan runtime, pertahankan UNKNOWN sampai lingkungan verifikasi yang disetujui tersedia.
4. Buat harness MIPS terisolasi hanya jika dapat membuktikan ia tidak menjalankan game/emulator gameplay; selain itu Langkah 9 tetap TERBLOKIR.
