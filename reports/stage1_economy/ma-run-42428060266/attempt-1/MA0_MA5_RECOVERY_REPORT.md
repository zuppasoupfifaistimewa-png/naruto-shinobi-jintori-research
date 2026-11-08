# MA0–MA5 — laporan pemulihan hasil run statis

**STATUS keseluruhan: SEBAGIAN.** Analyzer MA menyelesaikan analisis, tetapi laporan rinci MA tidak berhasil dipublikasikan ke branch. Dokumen ini adalah laporan pemulihan yang direkonstruksi dari log Actions dan bukti LA/KA yang masih bisa diperiksa; ini **bukan** salinan 37 artefak MA yang dibuat di workspace runner.

## Identitas, run, dan ledger MA0

- Baseline inklusif: `662833da768f473349539eb3fe304dc7fa51a16c`.
- Source SHA MA: `819303553e51b0499c81e94c197616e454cfb2a0`.
- MA run: `42428060266`, job `ma0-ma5-static`, job ID `128570549659`.
- Analyzer exit code `0`; publikasi gagal dengan exit code `1` karena `git push` ditolak (`fetch first` / non-fast-forward). Remote `main` sudah lebih dahulu maju ke `fccce38b8cd2aa8fc3ee1ae121ad295e8f1b19fe` dari run KA sampingan.
- Git hanya memiliki dua commit dalam rentang `baseline^..source`: baseline dan commit implementasi MA; keduanya oleh akun pemilik repo (2 human, 0 bot). Commit publikasi laporan tidak masuk ledger MA ini.
- Snapshot Actions: `1248/1248` run, 13 halaman, seluruh event. `py_compile=67/67`; pemeriksaan offset + decode untuk TSV MA `991/991`.
- Audit kutipan gabungan melaporkan **maksimum 72 byte dan 3 kelompok di atas 64 byte**. Lokasi ketiga kelompok tidak tercetak pada log dan file audit asli berada di workspace runner yang telah dihapus. Karena itu syarat kutipan MA0 **gagal**; jangan menganggap hasilnya bersih.
- 37 file output dibuat dan dimasukkan ke commit lokal runner (abbreviated SHA `9ed79ced`), tetapi push ditolak. Objek commit itu tidak dapat dibaca dari GitHub; isi TSV/MD rinci MA tidak tersedia di branch.
- Wrapper Ghidra dan tahap ekstraksi selesai sebagai langkah Actions; kode keluar per perintah Ghidra EXE/ENTRY1 tidak tersimpan di log yang dapat diakses: **TIDAK TAHU**.
- `EMULATOR_LAUNCHES=0`; ekstraksi sumber game hanya sementara untuk analisis statis dan direktori privat dibersihkan. Tidak ada biner dikomit dan tidak ada Release diubah.

## Status per tahap

| Tahap | Status / keyakinan | Kesimpulan yang dapat dipertanggungjawabkan |
|---|---|---|
| MA0 | **SEBAGIAN K3** | Ledger, Actions census, compile, dan 991 validasi selesai; audit excerpt gagal pada 3 kelompok (maksimum 72 B). |
| MA1 | **SEBAGIAN K3** | Enam record scene berurutan terlihat dalam bukti LA sebelumnya. Batas lengkap, pembaca/index*28, prolog manual empat fungsi, dan beberapa asal argumen tetap TIDAK TAHU karena artefak MA tidak terpublikasi. |
| MA2 | **SEBAGIAN K3** | Bukti silang KA memetakan 14 penulis `sh` selector dan 3 penulis `sb`; sumber seluruh sel matrix dan identitas x belum terbukti. Nilai numerik helper 0x800154D4 TIDAK TAHU. |
| MA3 | **BELUM K2/K3** | Parent/pemanggil lengkap 0x800B24C8 belum teridentifikasi. Satu pemanggil langsung 0x800BE5D8 teramati di 0x800B54F4; daftar dinamis belum tertutup. |
| MA4 | **TUNTAS K4** | Statis saja; tidak ada emulator/game launch. |
| MA5 | **BELUM K1** | Tidak ada rumus biaya upgrade untuk lompatan level d≥2. |

## MA1 — tabel scene, pemanggil, dan wallet

Bukti LA baseline menunjukkan enam record 7-word yang berurutan dengan stride `0x1C`. Alamat terendah yang terlihat adalah `0x800558C0`; enam record berakhir pada batas kandidat `0x80055968`. Pemindaian batas sebelum record pertama dan setelah record keenam **tidak dapat diverifikasi** dari artefak MA yang hilang.

| Index relatif | Base PC | +4 | Pointer +8 | Pointer +C | Pointer +10 | Nama |
|---:|---:|---:|---:|---:|---:|---|
| 0 | 0x800558C0 | 5 | 0x800AD4E0 | 0x800AD5F0 | 0x800AD5A8 | LOGO |
| 1 | 0x800558DC | 0 | 0x800AF640 | 0x800AF748 | 0x800AF724 | MENU |
| 2 | 0x800558F8 | 1 | 0x800B1E88 | 0x800B50AC | 0x800B5020 | BOARD |
| 3 | 0x80055914 | 1 | 0x800B2A58 | 0x800B50AC | 0x800B5020 | BOARDRET |
| 4 | 0x80055930 | 1 | 0x8011C028 | 0x8011CE2C | 0x8011CDDC | BAT_INI |
| 5 | 0x8005594C | 1 | 0x8011C028 | 0x8011CE2C | 0x8011CDDC | BAT_VIEW |

Dua word data yang menunjuk ke `0x800B50AC` terlihat pada `0x80055904` dan `0x80055920`. Ini membuktikan keberadaan word pointer di dua record, **bukan** bahwa kode telah terbukti membaca tabel dengan indeks*28 lalu memanggil hasilnya memakai `jalr/jr`. Tidak ada hasil MA yang dapat dipakai untuk mengonfirmasi rantai kode tersebut.

Prolog manual dan batas fungsi untuk `0x800B1E88`, `0x800B50AC`, `0x800B5020`, dan `0x800B2A58`: **TIDAK TAHU** pada laporan yang dapat dipublikasikan. Untuk call-site `0x800F5F54`, `0x800B54DC`, dan `0x800F5EBC`, asal `$a2` dan `$a3` juga **TIDAK TAHU** pada audit silang KA; tidak ada argumen masuk yang boleh diasumsikan tanpa reaching definition.

**Setter wallet otoritatif: TIDAK TAHU.** Dua kandidat dan falsifier:
- H1: record peserta +`0x04` adalah wallet. Dukungan terbatas: record peserta memakai stride `0xB4` dan terdapat kandidat akses/tulisan field; belum ada rantai reader+writer lengkap yang membuktikan makna wallet. Falsifier: xref lengkap menunjukkan field itu cache/UI/flag atau field lain.
- H2: manager+`0x4F4` menyimpan nilai settlement/delta bertanda. Dukungan: load di `0x800DD1B8`, normalisasi tanda dekat `0x800DD1C8`, lalu reset di `0x800DD1DC`. Falsifier: alur produsen/konsumen lengkap membuktikan field tersebut bukan saldo/delta wallet.
- `FUN_80014F10` tidak boleh disebut setter wallet; bukti JA/KA yang tersedia menunjukkan update maksimum berindeks peserta ke offset record +`0x94`, bukan pembuktian wallet +`0x04`.

## MA2 — selector dan batas helper

Bukti silang KA menemukan 14 instruksi `sh` ke `0x8013EA6E`. Semua 14 sumber nilainya adalah load `lhu`, bukan konstanta langsung:
- 12 sumber dibaca dari `0x8013EA88`: PC `0x800B9774`, `0x800B9AD8`, `0x800D131C`, `0x800D8FD8`, `0x800DAC7C`, `0x800E04AC`, `0x800E3B1C`, `0x800E43C4`, `0x800E488C`, `0x800EBEFC`, `0x800ECF34`, `0x800EEF20`.
- 2 sumber dibaca dari `0x80139EFC`: PC `0x800D734C` dan `0x800D7938`.

Tiga penulis `sb` ke `0x8013EB1C` teramati pada `0x800D77C4`, `0x800D7D4C`, dan `0x800E4840`. Nilai sumber register belum ditelusuri sampai konstanta atau load yang menentukan; klasifikasi nilai: **TIDAK TAHU**, bukan konstanta.

Penulis byte untuk seluruh area dinamis `manager+0x10+B+144*I` belum tertutup. Tidak boleh menggolongkan semua sel sebagai konstanta, salinan, atau selisih level dari scan parsial. H1 `x=d` memprediksi semua sel berasal dari selisih dua level; H2 `x=effect/item/action ID` memprediksi sumber konstanta/tabel selector. Bukti yang ada belum membantah salah satu secara global. Kedua identitas itu **TIDAK TAHU**.

Batas helper `0x800154D4`: nilai kembalian di `$v0` dipakai sebagai batas unsigned untuk membandingkan `x` pada `0x80015540`; angka batasnya **TIDAK TAHU** dan tidak terbukti bernilai 52. Angka 52 hanya jumlah entri tabel H yang terlihat, indeks 0–51; itu tidak membuktikan helper mengembalikan 52. Jika perbandingan gagal, cabang menuju `0x80015564` menjalankan `move $v0,$zero`; jalur itu mengembalikan nol melalui epilog bersama.

Jendela kode berikut tepat 16 instruksi / 64 byte, dari PC `0x80015538` sampai sebelum `0x80015578`:

| PC | Byte | Instruksi |
|---|---|---|
| 0x80015538 | 35 55 00 0C | jal 0x800154D4 |
| 0x8001553C | 21 80 80 00 | move $s0,$a0 |
| 0x80015540 | 2B 10 02 02 | sltu $v0,$s0,$v0 |
| 0x80015544 | 07 00 40 10 | beqz $v0,0x80015564 |
| 0x80015548 | 05 80 02 3C | lui $v0,0x8005 |
| 0x8001554C | EC 5C 42 24 | addiu $v0,$v0,0x5CEC |
| 0x80015550 | 00 19 10 00 | sll $v1,$s0,4 |
| 0x80015554 | 21 10 43 00 | addu $v0,$v0,$v1 |
| 0x80015558 | 08 00 42 8C | lw $v0,8($v0) |
| 0x8001555C | 5A 55 00 08 | j 0x80015568 |
| 0x80015560 | 00 00 00 00 | nop |
| 0x80015564 | 21 10 00 00 | move $v0,$zero |
| 0x80015568 | 14 00 BF 8F | lw $ra,0x14($sp) |
| 0x8001556C | 10 00 B0 8F | lw $s0,0x10($sp) |
| 0x80015570 | 08 00 E0 03 | jr $ra |
| 0x80015574 | 18 00 BD 27 | addiu $sp,$sp,0x18 |

## MA3 — batas fungsi dan caller

Bukti silang KA untuk `0x800B24C8` memberi instruksi `sh $zero,0x2EE($v0)`; asal `$v0` di `0x800B24C0` adalah load dari alamat pointer global `0x8013EA74`. Namun entry/parent fungsi dan daftar caller lengkap tetap **TIDAK TAHU**. File caller KA hanya berisi header tanpa caller; itu bukan bukti bahwa tidak ada caller. Kandidat parent `0x800B1E88` tidak dapat dipastikan tanpa artefak MA yang hilang dan pemeriksaan batas manual antara dua alamat.

Satu caller langsung `0x800BE5D8` yang teramati: `jal 0x800BE5D8` di `0x800B54F4`, caller yang diindeks Ghidra sebagai `FUN_800B50AC`. Caller dinamis `jalr/jr` dan kelengkapan daftar tetap **TIDAK TAHU**.

## MA4–MA5

MA4 tuntas sebagai batas prosedur: tidak ada eksekusi game/emulator dan `EMULATOR_LAUNCHES=0`.

MA5 tidak menghasilkan rumus biaya upgrade. Bentuk lookup yang masih boleh ditulis bersyarat adalah `H(x)=u32[0x80055CF4+16*x]`; x adalah byte yang ditulis ke manager+`0x530` oleh jalur yang sudah dikenal, sehingga domain kondisional byte `0..255`. Tidak terbukti bahwa x adalah delta level d, bahwa x dibatasi ke indeks tabel 0–51, atau bahwa biaya lompatan level `d≥2` sama dengan lookup itu. Hasil: **TIDAK TAHU**, tanpa angka biaya/fitting.

## Efek samping Actions dan berkas yang berubah

Commit implementasi MA `819303553e51b0499c81e94c197616e454cfb2a0` mengubah empat path:
- Ditambahkan `.github/workflows/ma0-ma5-static.yml`.
- Ditambahkan `tools/ma-static/RunMA0MA5Static.py`.
- Dihapus (sesuai izin eksplisit) `reports/stage1_economy/la-run-42421741871/attempt-1/LA1_B50AC_TABLE_REGION.tsv`.
- Dihapus (sesuai izin eksplisit) `reports/stage1_economy/la-run-42421741871/attempt-1/LA2_BOUNDS_CONTEXT.tsv`.

Karena workflow LA dan KA lama juga memfilter `**/*.py`, commit analyzer MA memicu kedua workflow sampingan. Akses GitHub yang tersedia di sesi ini tidak menyediakan pembatalan run. KA lebih dahulu memublikasikan satu commit `fccce38b8cd2aa8fc3ee1ae121ad295e8f1b19fe` yang menambah **28 berkas** di `reports/stage1_economy/ka-run-42428060234/attempt-1/`; tidak ada workflow KA yang diubah. LA juga gagal publikasi karena push non-fast-forward. Daftar 28 path KA:
- `ACTIONS_RUN_SUMMARY.txt`
- `KA0_KA5_FINAL_REPORT.md`
- `KA0_LEDGER_ACTIONS.tsv`
- `KA0_LEDGER_COMMITS.tsv`
- `KA0_LEDGER_SUMMARY.txt`
- `KA0_PUBLISH_COMMIT_FILES.tsv`
- `KA0_PYCOMPILE.tsv`
- `KA0_SOURCE_COMMIT_FILES.tsv`
- `KA1_B50AC_CALLERS.tsv`
- `KA1_B50AC_CALLER_WINDOWS.tsv`
- `KA1_CALL_ARGUMENT_ORIGINS.tsv`
- `KA1_WALLET_HYPOTHESES.tsv`
- `KA1_WALLET_STATUS.txt`
- `KA2_GLOBAL_WRITERS.tsv`
- `KA2_GLOBAL_WRITER_VALUE_ORIGINS.tsv`
- `KA2_H_TABLE_52.tsv`
- `KA2_MANAGER_530_X_PROVENANCE.tsv`
- `KA2_X_DOMAIN.txt`
- `KA2_X_HYPOTHESES.tsv`
- `KA3_B24C8_FUNCTION_V0_CONTEXT.tsv`
- `KA3_B24C8_PARENT_CALLERS.tsv`
- `KA3_B24C8_WINDOW.tsv`
- `KA3_BE5D8_CALLERS.tsv`
- `KA3_BE5D8_CALLER_WINDOWS.tsv`
- `KA3_BOUNDARY_STATUS.txt`
- `KA4_STATIC_ONLY.txt`
- `KA5_SYMBOLIC_COST.tsv`
- `cleanup.txt`

KA adalah bukti silang dari run sampingan dan memakai baseline KA berbeda (`656503e9e21cb4baf3185969abf7b15d05a149c6`), bukan ledger MA. Jangan menyatukan ledger dua tahap tersebut. Tidak ada perubahan ke `STATUS.md`, workflow KA, atau Release.

## Referensi raw yang bisa diperiksa

LA pada baseline MA:
- `https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/662833da768f473349539eb3fe304dc7fa51a16c/reports/stage1_economy/la-run-42421741871/attempt-1/LA1_B50AC_TABLE_REGION.tsv`
- `https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/662833da768f473349539eb3fe304dc7fa51a16c/reports/stage1_economy/la-run-42421741871/attempt-1/LA2_BOUNDS_BRANCHES.tsv`

KA cross-check (run sampingan, bukan hasil MA):
- `https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/fccce38b8cd2aa8fc3ee1ae121ad295e8f1b19fe/reports/stage1_economy/ka-run-42428060234/attempt-1/KA1_CALL_ARGUMENT_ORIGINS.tsv`
- `https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/fccce38b8cd2aa8fc3ee1ae121ad295e8f1b19fe/reports/stage1_economy/ka-run-42428060234/attempt-1/KA1_WALLET_STATUS.txt`
- `https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/fccce38b8cd2aa8fc3ee1ae121ad295e8f1b19fe/reports/stage1_economy/ka-run-42428060234/attempt-1/KA2_GLOBAL_WRITERS.tsv`
- `https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/fccce38b8cd2aa8fc3ee1ae121ad295e8f1b19fe/reports/stage1_economy/ka-run-42428060234/attempt-1/KA2_GLOBAL_WRITER_VALUE_ORIGINS.tsv`
- `https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/fccce38b8cd2aa8fc3ee1ae121ad295e8f1b19fe/reports/stage1_economy/ka-run-42428060234/attempt-1/KA2_X_DOMAIN.txt`
- `https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/fccce38b8cd2aa8fc3ee1ae121ad295e8f1b19fe/reports/stage1_economy/ka-run-42428060234/attempt-1/KA3_B24C8_FUNCTION_V0_CONTEXT.tsv`
- `https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/fccce38b8cd2aa8fc3ee1ae121ad295e8f1b19fe/reports/stage1_economy/ka-run-42428060234/attempt-1/KA3_BOUNDARY_STATUS.txt`
- `https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/fccce38b8cd2aa8fc3ee1ae121ad295e8f1b19fe/reports/stage1_economy/ka-run-42428060234/attempt-1/KA3_BE5D8_CALLERS.tsv`
- `https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/fccce38b8cd2aa8fc3ee1ae121ad295e8f1b19fe/reports/stage1_economy/ka-run-42428060234/attempt-1/KA5_SYMBOLIC_COST.tsv`
