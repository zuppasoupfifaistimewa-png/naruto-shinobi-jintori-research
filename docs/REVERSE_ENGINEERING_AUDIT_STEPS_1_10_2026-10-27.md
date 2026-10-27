# Audit Reverse Engineering Langkah 1–10 — 27 Oktober 2026

## Cakupan dan keselamatan

Satu-satunya repositori yang digunakan: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research. Audit ini menggabungkan analisis statis, eksperimen runtime RNG terukur pada checkpoint roulette, dan satu uji CPU MIPS yang terisolasi. Tidak ada workflow pemain adaptif/Story Mode otomatis dijalankan, tidak ada classifier/policy/Revision65/readiness gate yang diubah, dan tidak ada ending Story Mode yang diklaim. Restore checkpoint hanya terjadi pada eksperimen diagnostik Step 4 yang dibatasi. Aset ROM/disc, BIOS, Memory Card, savestate, dump RAM, dan screenshot gameplay privat tidak ditambahkan ke Git; screenshot diagnostik privat disimpan hanya pada artifact Actions ber-retensi terbatas.

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
| 4 — RNG | **SEBAGIAN (keseluruhan kriteria pengguna)** | Formula/caller statis dan uji RNG terisolasi 7/7 tetap valid. Cold boot satu-breakpoint #40485987817 tidak mendapat hit pada `0x80035DA8` hingga frame 120. Koreksi delay slot menemukan `li a0,-1` adalah input helper `0x80037138`, sementara `move a0,v0` meneruskan helper return ke setter; nilai return/state masih UNKNOWN. Run Ghidra statis #40487406384 sedang menganalisis helper, belum ada artefak final. Caller-ke-roulette, battle, dispatch menyeluruh dan randomness alternatif tetap UNKNOWN. Lihat [trace](STEP4_RNG_TRACE_2026-10-27.md) dan [closure](STEP4_CLOSURE_2026-10-27.md). |
| 5 — Caller RNG dan m2c | **SELESAI untuk empat caller yang dipilih** | Keempat entry fungsi dibandingkan oleh Ghidra dan m2c; semua output ada, perbandingan berhasil. Delapan keluaran C dan ringkasan disimpan permanen di [laporan Step 5](../out/step5/STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md). |
| 6 — Penulis memori, xref, caller dan call chain | **SEBAGIAN** | Artifact #12719587873 confirms static stores `+0x2E9=0x3F`, `+0x2E5=0`, selector `+0x58B`, conditional codes `+0x5D2`, and negate/clamp + Chakra setter flow at `0x8011C0D0`. Scan #40488847927 covered 98,357 entry-1 decoded instructions for exact scalar immediates, not all memory displacements/aliases; no-hit cannot prove fields unused. Base `0x800D0000`, semantics, `+0xB30/+0xB38/+0xB40/+0xB44` source/final writer and transition effects remain UNKNOWN. |
| 7 — Loader dan overlay | **SELESAI SEBAGIAN** | Direktori DATA.BIN dan jalur copy bootstrap didukung statis. Loader probe #40484548650 mencapai frame 120 tanpa hit pada `0x800AD454`; seed-setter probe terpisah #40485987817 mencapai frame 120 tanpa hit pada `0x80035DA8`. Yang kedua terutama menambah bukti batas Step 4(a), bukan pemetaan loader. Kedua run exit 124 pada batas 35 detik dan cleanup PASS. Artefak #12724961702 (ZIP SHA-256 `27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71`) dan #12724933081 (ZIP SHA-256 `74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6`). Base/lifecycle/register/copy-size/checksum runtime belum tervalidasi; DATA2.BIN/DUMMY.BIN belum dipetakan menyeluruh. |
| 8 — Penjelasan fungsi | **SELESAI SEBAGIAN** | Raw MIPS clarifies selected branch/gate/store sequences; branch-code meaning, costs, battle/roulette/turn, cards and victory conditions remain UNKNOWN. Details: Step 8 addendum. |
| 9 — Verifikasi terisolasi | **TUNTAS untuk satu fungsi RNG utama** | Probe Unicorn MIPS32 menjalankan rutin 0x80035D78 pada 7 vektor dengan memory map fisik PS1, return sentinel, pembandingan state/v0, dan batas instruksi. Run #40474891838 sukses; lihat [laporan uji isolasi](../out/step9/STEP9_UNICORN_RESULT_2026-10-27.md). Tidak menggeneralisasi ke fungsi lain atau emulator PS1 penuh. |
| 10 — Indeks out/logic.md | **TUNTAS sebagai indeks audit** | Indeks dan laporan penutupan kini menunjuk ke report per-langkah terkini serta memisahkan TERVERIFIKASI/HIPOTESIS/UNKNOWN. Status ini hanya menutup kebutuhan indeks/dokumentasi, bukan seluruh reverse engineering game. |

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
- Langkah 10 — **TUNTAS sebagai indeks audit**; this does not mean the game is fully reverse-engineered.

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