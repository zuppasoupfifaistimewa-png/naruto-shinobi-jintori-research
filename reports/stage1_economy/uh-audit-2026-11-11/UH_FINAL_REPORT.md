# Audit UH0–UH3 — baseline c7da18…

**Repo baseline:** `c7da18bef75f6e6905d495b72710f50aaf1bb5b0` (inklusif). Audit report-only; kode dan workflow tidak diubah.

| Bagian | Status | Level | Hasil |
|---|---|---:|---|
| UH0 manifest b74d931 | SEBAGIAN | K4 | 319 file modifikasi memiliki rentang baris induk; hitungan rentang cocok dengan total per-file 61.810. Statistik commit menyebut 63.121, selisih 1.311 tidak dapat dialokasikan ke file. |
| UH0 konflik byte | TUNTAS untuk definisi/hitung UG0 | K4 | 14.001 observasi konflik pada gate; 3.512 koordinat unik dengan konflik; selisih 10.489 adalah observasi konflik tambahan pada koordinat yang sama. |
| UH1 writer | SEBAGIAN | K4 untuk instruksi/basis yang terikat; K2 kandidat; K0 ENTRY0 | 42 writer `sh +0x20` punya alias basis ke slot 0x8013EA84, tetapi stride 0x124 belum terbukti per-PC; dua writer `sh +0x1A` adalah loader; 42 kandidat `sb` belum beralias; Entry0 tidak menghasilkan census writer. |
| UH2 runtime watch | BELUM | K0 | Tidak ada run: batas dan jumlah record petak belum terbukti, sehingga alamat watchpoint aman belum diketahui. |
| UH3 ledger | TUNTAS dalam jendela API | K4 | Tiga commit termasuk baseline, 16 event file no-renames; satu Actions run schedule 42977820741; tidak ada push/workflow_dispatch run yang dikembalikan API sejak baseline. |

## UH0 — manifest pemangkasan

Manifest berisi 319 file yang dimodifikasi pada `b74d931cf9855c16c3d3e22b10a11cf94c7c2d04` relatif ke parent `c87e124daeb4e007c555bc07eab811bfe61e6afb`. 84 file memakai baris minus dari patch GitHub; 232 file yang patch-nya dihilangkan direkonstruksi dengan satu alignment LCS deterministik atas baris teks UTF-8, tanpa menyimpan byte konten. Setiap baris rentang dalam manifest telah divalidasi ulang terhadap jumlah deletion per-file API: 0 mismatch. Tiga file modified lain tidak memiliki baris terhapus.

**Batas agregat:** jumlah deletion per-file API adalah 61.810. Statistik commit GitHub mencatat 63.121. Sisa 1.311 tidak memiliki atribusi per-file di respons API yang diterima; manifest tidak membuat-buat rentang untuknya. Tidak ada baris TSV yang dihapus dalam audit ini.

Konflik byte didefinisikan sebagai observasi berikutnya pada koordinat berlabel yang nilainya berbeda dari observasi acuan pertama pada koordinat yang sama. Gate menghitung 14.001 observasi seperti itu. Hitungan independen berdasarkan koordinat unik adalah 3.512. Jadi 10.489 adalah observasi konflik tambahan pada koordinat yang sudah konflik—bukan koordinat konflik baru dan bukan hitungan seluruh pasangan kombinatorial.

## UH1 — penulisan medan record

Di set census yang diperiksa, 42 penulisan `sh` ke displacement `+0x20` dalam ENTRY1 memiliki alias tabel terbukti melalui slot `0x8013EA84`, tersebar pada 16 fungsi. Hanya satu penulisan berada di `FUN_800D15A8`: PC `0x800D5A1C`, sumber immediate di PC sebelumnya adalah `0xF020`. Itu bukan penambahan level aritmetis `+1`.

Dua penulisan `sh +0x1A` di `FUN_800F7ADC` (PC `0x800F7D9C`, `0x800F7DB0`) juga memuat basis dari slot `0x8013EA84`. Rantai indeks yang dilacak membentuk `(73 * index) * 4 = 0x124 * index`. Kedua nilai berasal dari byte loader buffer, sehingga ini merupakan penyalinan/loader record, bukan bukti biaya upgrade.

Census global `sb` mencatat 139 instruksi memakai displacement tepat `+0x1A/+0x1C/+0x1E`: 97 menggunakan `$sp` dan dikeluarkan dari kandidat record; 42 non-stack tetap belum terbukti aliasnya ke `0x8013EA84 + index*0x124`. Rinciannya 6/+1A, 18/+1C, 18/+1E; tersebar pada EXE dan ENTRY1. Scan literal `+0x1A` terpisah (DX1) berisi 172 akses, termasuk 130 write (43 EXE, 87 ENTRY1); hanya dua write `FUN_800F7ADC` yang terikat ke slot EA84, dan keduanya loader copy. Tidak tersedia census global `sh/sw` lengkap untuk `+0x1C/+0x1E`.

`ENTRY0` kini diperiksa lewat artefak teks Ghidra run 41290779708. Run mengekspor 38 baris fungsi, tetapi autoanalysis timeout pada 1.800 detik dan ada kegagalan repair body; tidak ada census `sb/sh/sw` per-PC. Basis `0x800AD000` berstatus hipotesis statis dan runtime mapping belum tervalidasi. Jadi writer petak ENTRY0 tetap `TIDAK TAHU` (K0). Rinciannya ada di `UH1_ENTRY0_ARTIFACT_AUDIT.txt`.

`FUN_800D15A8` terlihat dipanggil pada tick ganjil dalam trace UG, tetapi hit fungsi bukan bukti bahwa store terjadi pada setiap pemanggilan. Satu-satunya store array `+0x20` di fungsi tersebut adalah konstanta `0xF020` pada satu jalur. Fungsi memiliki percabangan; predikat yang tepat untuk mencapai store tetap `TIDAK TAHU`. Jadi tidak terbukti bahwa fungsi menaikkan level setiap pemanggilan; juga belum cukup untuk menamai aturan gate gameplay.

Biaya upgrade lompat level `d>=2` dengan nilai 400/800/1600 tetap **K1 / hipotesis**. Rumus biaya: **TIDAK TAHU**, belum ada aritmetika atau tabel konstanta biaya langsung yang terikat ke transaksi upgrade.

## UH2 — runtime

Tidak ada emulator launch. Runner yang ada hanya memasang empat Exec breakpoint dan menjalankan enam kondisi; requested write watch memerlukan rentang alamat petak dan jumlah record yang pasti. Slot `0x8013EA84` adalah lokasi pointer dinamis, bukan alamat dasar RAM yang cukup untuk menetapkan rentang aman tanpa membaca/menentukan pointer dan batas array. Kandidat `sb +1A/+1C/+1E` juga belum beralias ke slot tersebut. Watchpoint spekulatif berisiko merekam objek lain atau melewatkan petak.

Tidak ada TSV nilai frame 1/900, write-hit counters/PC/RA, Memory Card clone/hash, atau status `instrumented=true` dari UH2. Tidak ada run Actions baru yang digunakan. Pyflakes, parse YAML lokal, dan dry fail-fast tidak dijalankan karena tidak ada perubahan skrip/workflow dan checkout lokal tidak dapat diambil (DNS gagal saat mencoba `raw.githubusercontent.com`).

## UH3 — ledger baseline-inclusive

Ledger mencakup baseline c7, commit anak 02ad6, dan commit laporan statis 46948; ada 16 event file berdasarkan status Git (no-renames). Sejak waktu baseline, query Actions API mengembalikan satu run schedule, #42977820741, workflow monitor, job `monitor` sukses. Source SHA run sama dengan baseline. Tidak ada run `push` atau `workflow_dispatch` di rentang query. Job sukses adalah hasil monitor; bukan bukti Story Mode selesai. Ringkasan run terdahulu tersedia pada permalink raw di `UH3_SUMMARY.txt`.

## Validasi dan batas

- Validasi internal laporan: 319 baris manifest; 0 mismatch antara panjang rentang dan deletion per-file; 86 baris tabel writer; 130 write literal `+0x1A` pada EXE/ENTRY1; Entry0 artifact diverifikasi sebagai ekspor parsial; ledger 3 commit/16 event/1 run.
- Tidak ada kode atau workflow yang diubah; tidak ada source SHA emulator UH2 karena run UH2 tidak dilakukan. Code SHA baseline yang dianalisis tetap `c7da18bef75f6e6905d495b72710f50aaf1bb5b0`.
- Tidak mengubah `STATUS.md`, Release, atau menghapus baris TSV. Tidak menyertakan ROM, BIOS, Memory Card, savestate, dump RAM, atau biner.
- Tingkat K5 tidak diberikan: tidak ada runtime UH2 yang dijalankan.
