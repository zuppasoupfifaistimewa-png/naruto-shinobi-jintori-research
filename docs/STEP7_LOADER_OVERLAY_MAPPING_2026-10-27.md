# Langkah 7 — peta loader/overlay berbasis bukti statis (27 Oktober 2026)

Status: **SEBAGIAN**. Struktur direktori dan salah satu jalur salin bootstrap terverifikasi secara statis, tetapi pemuatan resource ke RAM, base runtime, relokasi, dan lifecycle belum tervalidasi menggunakan bukti runtime.

## Sumber bukti

- [RESOURCE_CATALOG.md](RESOURCE_CATALOG.md) dan [OVERLAY_MAP.md](OVERLAY_MAP.md).
- Analisis main EXE: [run Ghidra #40438574949](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40438574949), artifact teks #12704922603.
- Survei resource: [run #40439763833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40439763833), artifact teks #12705072941. Validasi lanjutan entry 1: [run #40455975408](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455975408).
- Ekstraksi dan pemeriksaan file disc terdahulu memvalidasi hash; seluruh BIN/CUE/executable hanya digunakan di runner privat, bukan di Git.

## Struktur data disc yang terverifikasi

- Executable utama `SLPS_035.53`: 385.024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`; header PS-X EXE memuat base text `0x80010000`, ukuran text `0x5D800`, dan entry PC `0x80011448`.
- Di main EXE file offset `0x46098` (RAM executable `0x80055898`) terdapat pasangan uint32 little-endian `0xD4, 0x2F44`; `0xD4` cocok dengan LBN 212 tempat extent `DATA.BIN` dimulai, dan `0x2F44` = 12.100 byte.
- Bootstrap awal `DATA.BIN[0x00:0x44]` memiliki 68 byte kode/data awal; `DATA.BIN[0x44:0x2F44]` adalah tabel direktori `0x2F00` byte dengan 1.504 entry. Terdapat 1.500 entry aktif dan empat ukuran nol (indeks 1491–1494).
- Interval sektor entry aktif tidak tumpang tindih, seluruhnya berada di dalam extent ISO `DATA.BIN` LBN `[212,32446)`. Total interval aktif mencakup 32.227 sektor dibanding 32.234 sektor pada extent file; selisih itu telah didokumentasikan, tidak otomatis menunjukkan resource hilang.
- Analisis instruksi di sekitar `0x800AD454` mendukung salinan `0x2F00` byte dari `0x800AD494` ke `0x8006D830`. Ini konsisten dengan penyalinan direktori dari `+0x44` bootstrap. Temuan ini adalah alur kode statis dan tidak membuktikan bahwa seluruh `DATA.BIN` menjadi satu overlay kontigu.

## Resource yang dianalisis dan batas base

| Sumber | Offset file / ukuran | Temuan statis | Status alamat RAM |
|---|---|---|---|
| DATA.BIN entry 0 | offset `0x5F800`, 110.536 byte, SHA-256 `56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4` | Instruksi direct-JAL RNG dan kandidat setter RNG ditemukan pada analisis lokal | Base sekitar `0x800AD000` adalah **HIPOTESIS**; jangan samakan tanpa bukti dengan alamat kerja bootstrap `0x800AD454` |
| DATA.BIN entry 1 | offset `0x10BB000`, 596.412 byte, SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a` | Banyak instruksi MIPS langsung, cross-reference dan kelompok target/getter/setter dianalisis | Base `0x800D0000` adalah **HIPOTESIS**; belum diukur saat loader berjalan |
| DATA2.BIN | 166.428.672 byte, SHA-256 `be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9` | Catatan statis berisi tabel kandidat field/offets; pemetaan menyeluruh belum dilakukan | **UNKNOWN** |
| DUMMY.BIN | 50.667.520 byte, SHA-256 `cac5c852e95c90475a2879f51b6b949afea2df0cb540b2a2743bd791af4c47a2` | Tujuan/pemakaian executable belum diketahui | **UNKNOWN** |
| XASECT.BIN | 692 byte, SHA-256 `df257fbdabdb848f845466246abf4a36fdb6cf17815fc3a76ff7d7585d1953f0` | File kecil teridentifikasi; hubungan seluruh tabel dan loader belum dibuktikan | **UNKNOWN** |

## Kaitannya dengan jalur kontrol

- Main EXE memiliki referensi kontrol yang efektif menuju alamat `0x800AD454`, berada di luar rentang text utama `[0x80010000,0x8006D800)`. Alamat tersebut konsisten dengan analisis bootstrap statis.
- Direktori berbasis LBN dan panjang adalah temuan kuat; identitas setiap entry, kode versus aset data, urutan pemuatan, alamat aktual, relokasi, pelepasan, dan re-use rentang RAM belum dibuktikan.
- 144 direct-JAL RNG candidates pada entry 1 dan empat direct-JAL RNG sites pada entry 0 telah dipetakan/didekode sesuai batas Ghidra pada base kandidat. Ini menunjukkan ada instruksi MIPS yang relevan di resource tersebut, tetapi tidak memvalidasi base mapping/lifecycle pada permainan berjalan.

## Kriteria yang belum terpenuhi

1. Menangkap breakpoint eksekusi loader/resource sebelum, selama, dan sesudah memuat entry 0/1, lalu mencatat PC, register sumber/tujuan copy, panjang, hash isi RAM, dan alamat tujuan.
2. Menentukan apakah entry 0, entry 1, bootstrap, dan aset resource lain memiliki base RAM yang konsisten, berbeda, atau berubah sesuai lifecycle. Untuk alamat yang hanya ditebak dari referensi internal, label tetap **HIPOTESIS**.
3. Menguji apakah DATA2.BIN dan DUMMY.BIN menyumbang executable code, tabel, aset, atau konten yang didekompresi/dekripsi; hasil nol pada scan direct-JAL/LCG raw bukan bukti bahwa tidak ada kode.
4. Memetakan relokasi, indirect call/pointer dispatch, dan urutan load/unload.

## Kesimpulan

**Langkah 7 = SEBAGIAN.** Struktur direktori dan jalur penyalinan bootstrap memiliki dukungan statis yang kuat. Klaim overlay runtime final ditahan sampai base/lifecycle loader didukung pengamatan langsung. Tidak ada ROM, BIOS, Memory Card, savestate, RAM dump, atau screenshot privat yang disimpan pada repo.


## Addendum runtime #40479865235 — 27 Oktober 2026

Run [#40479865235](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40479865235) selesai sukses sebagai workflow dalam 157 detik, tetapi tidak menghasilkan breakpoint hit yang dapat diterima. Pra-uji tanpa breakpoint mencapai frame 50; kontrol `-debugger` listener-only mencapai frame 40; probe empat-breakpoint memakai `-no-debugger` hanya mencapai frame 1–3 lalu timeout 124. Artefak teks-only #12722187784 berukuran 3.801 byte dengan SHA-256 ZIP `b9537035eb6ffed66a0aadd5ab48db88715ed2e2128bcf46a48f374c7306ac26`; cleanup privat PASS. Report otomatis memiliki bug regex pada metrik maksimal frame kontrol (mencetak 0, padahal raw log berisi 1,2,3,10,20,30,40); raw log adalah sumber yang lebih berwenang untuk angka ini. Hasil ini membuat Step 7 tetap **SEBAGIAN** dan menyarankan pengujian satu breakpoint per cold boot, tanpa input atau savestate restore. Detail lengkap: [hasil runtime Step 7](STEP7_RUNTIME_COLD_BOOT_RESULT_2026-10-27.md).

## Addendum — batas runtime diperbarui setelah single-breakpoint probe (27 Oktober 2026)

Run cold boot satu-breakpoint [#40484519812](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484519812) mengonfirmasi source disc/CUE/BIOS/emulator cocok dengan checksum yang dipatok dan cleanup privat PASS. Kontrol debugger listener-only mencapai frame 50; callback minimal satu breakpoint pada kandidat `0x800AD454` mencatat progres hingga frame 100 tanpa hit sebelum timeout 124 pada batas 35 detik. Laporan otomatis dari run awal gagal karena kesalahan sintaks Python saat menyusun ringkasan; raw log, bukan status Actions atau artefak laporan itu, adalah sumber data runtime. Koreksi pembentuk laporan berada pada commit `8326c07f71caeab12924133b0812ec7e86b8b1f7`; run koreksinya perlu diperiksa sebelum dinyatakan tervalidasi.

Hasil ini mengurangi kemungkinan bahwa **satu** breakpoint dengan callback ringan pasti menghentikan seluruh progres emulator; hasil empat-breakpoint terdahulu tetap menunjukkan penurunan observabilitas yang tajam. Tidak ada hit di `0x800AD454`, tidak ada sampel register atau checksum copy, dan base entry 0/1 tidak berubah status. Alamat itu tetap kandidat statis, bukan base/mapping runtime yang terverifikasi. Jangan membuat klaim positif/negatif tentang loader dari no-hit berbatas waktu.
