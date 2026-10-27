# Latest Step 8 evidence boundary — static counter and remaining rules (27 October 2026, 19:22 WIB)

Runner-only audit [#40503223693](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40503223693), artifact #12733512950 (13.079 bytes; SHA-256 ZIP 382773f9a421835bc97c448c630a2ea5d3891309bb34094f5a67027548c03414) validated the Ghidra text artifact #12732952776 (2.255.170 bytes; SHA-256 ZIP 6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6).

- **TERVERIFIKASI-STATIS:** 0x80037B58 clears global 0x80066E7C and eight callback-pointer slots. 0x80037BB0 increments that global and walks the eight slots via JALR. 0x80037138 can return this global when a0 is negative. This supports a callback/tick-counter description of static behavior, not a verified game mechanic or boot seed.
- **HIPOTESIS:** 0x800373F8 called by 0x80037B58 likely registers callback pointer 0x80037BB0; actual indirect target and runtime mapping are not verified.
- **UNKNOWN:** whether this count feeds a game RNG seed; runtime ordering/reachability of entry0 callsite 0x800AF2AC; cost/refund formula; barrier/upgrade rules; battle/roulette/turn rules; card effects; victory logic.
- Step 6 scan does not turn fields into game-rule labels; exact-immediate scan omits computed aliases, split immediates, unknown-base data and undisassembled code. Some target-transition decompiles have bad instruction/control-flow boundaries.
- Japanese strings, where relevant, should appear beside Indonesian translation, but text strings alone are not evidence of code semantics.

Step 8 remains **SEBAGIAN**. Minimum closure: a table per proposed rule with exact function/callers, raw branch/store instructions, fields/register flow, an independent corroborating source and explicit unknowns. Do not label fields Chakra, cost, turn, barrier or level-up without independent support.

---

# Langkah 8 — penjelasan fungsi dan aturan yang didukung bukti (27 Oktober 2026)

Status: **SEBAGIAN**. Beberapa operasi data dapat dijelaskan dengan keyakinan tinggi; nama dan aturan gameplay yang lebih luas tetap ditahan jika hanya disimpulkan dari alamat atau konstanta.

## Aturan memberi label

- **TERVERIFIKASI-STATIS**: didukung instruksi, dekompilasi, raw record, atau cross-reference yang alamat/sumbernya tercatat.
- **TERVERIFIKASI-RUNTIME-TERBATAS**: diamati pada konteks checkpoint/runtime tertentu, tetapi tidak otomatis menjelaskan hasil akhir.
- **HIPOTESIS**: interpretasi masuk akal yang belum dibedakan dari alternatifnya.
- **UNKNOWN**: bukti saat ini belum mendukung kesimpulan.

## Rutin RNG dan caller main EXE

| Alamat / komponen | Yang didukung | Yang belum dibuktikan |
|---|---|---|
| `0x80035D78`, state `0x800A3118` | **TERVERIFIKASI-STATIS**: state 32-bit diperbarui dengan `new = old * 0x41C64E6D + 0x3039 mod 2^32`, hasil `(new >> 16) & 0x7FFF` | Seed saat boot dan seluruh lifecycle state belum didukung runtime |
| `0x80015ADC` | **TERVERIFIKASI-STATIS**: memakai RNG dalam perhitungan indeks terbatas lalu memanggil helper penyisipan ke daftar | Arti gameplay dan label data yang disisipkan UNKNOWN |
| `0x80015B7C` | **TERVERIFIKASI-STATIS**: melakukan pertukaran byte berulang menggunakan hasil RNG dan panjang daftar | Tabel yang di-shuffle belum diberi arti gameplay |
| `0x8001A328` | **TERVERIFIKASI-STATIS**: memfilter kandidat melalui tes bit/kode `0x7F–0x86`, memilih satu kandidat, menyimpan hasil ke `DAT_80089DA9` | Arti kandidat dan pengaruhnya terhadap gameplay UNKNOWN |
| `0x80020BF4` | **TERVERIFIKASI-STATIS**: menginisialisasi struktur pada kondisi tertentu, menyimpan hasil RNG modulo `0x1000` ke field `param_1[0xD]`, lalu memanggil helper | Field tidak boleh dinamai sebagai durasi, battle seed, turn seed, atau mekanik lain tanpa bukti |

## Chakra dan pemeriksaan target

| Alamat / komponen | Temuan | Batas interpretasi |
|---|---|---|
| `0x80012A70` | **TERVERIFIKASI-STATIS**: getter nilai target Chakra konfigurasi | Referensi ke getter tidak otomatis merupakan pemeriksaan kemenangan; beberapa pemanggil digunakan untuk UI |
| `0x8001387C` | **TERVERIFIKASI-STATIS**: setter nilai Chakra utama dengan validasi/clamping indeks/nilai | Caller dapat memperbarui, menyalin, menyinkronkan atau memulihkan nilai; belum otomatis merupakan transaksi biaya |
| `0x800138EC` | **TERVERIFIKASI-STATIS**: getter Chakra pemain | Konteks caller masih diperlukan untuk memaknai nilai |
| `0x8011C0D0` | **TERVERIFIKASI-STATIS pada base entry-1 hipotetis**: ketika argumen tertentu berbeda dari global, memperbarui global/field; cabang nonzero mengiterasi record peserta dengan stride `0x90`, mengubah tanda word field `+0x04`, menjepit minimum ke `-9999`, lalu memanggil setter utama untuk peserta | Base `0x800D0000) belum tervalidasi runtime; trigger dan arti mode/field belum diketahui. Ini bukan bukti bahwa field adalah biaya barrier |
| Enam kandidat threshold `0x80111228`, `0x801112CC`, `0x801113B4`, `0x801114F0`, `0x80111588`, `0x80112418` | **TERVERIFIKASI-STATIS bersyarat base**: mengambil target, menghitung alamat record dengan stride `0x90`, membandingkan field record dengan target, dan pada beberapa jalur menulis state/field atau memanggil kandidat transisi | Makna `+0x58B`, `+0x2E9`, `+0x2E5`, `+0x5D2`, `0x80139F3B`; outcome transisi; aturan setiap mode tetap UNKNOWN |
| `0x8012A9C4` dan `0x80137AD8` | **TERVERIFIKASI-STATIS**: menggunakan getter target dalam kode yang terlihat sebagai UI/penggambaran atau navigasi daftar | Xref getter saja tidak mengidentifikasi fungsi menang |
| `0x800EF98C`, `0x80100D14`, `0x80100DCC` | Dipakai sebagai target/jalur kandidat transisi dari beberapa cabang statis | Hasil dekompilasi mengandung masalah function-boundary/control-flow; efek akhir UNKNOWN |

## Data konfigurasi dan resource

- Tabel konfigurasi main EXE pada `0x80057798` (stride record `0x54`) memuat nilai seperti 1500, 3000, dan 400 pada sejumlah record. Aliran statis di [peta loader/overlay](OVERLAY_MAP.md) menghubungkan field `+0x04` ke global `0x80070C80` yang dipakai pada inisialisasi Chakra, dan field `+0x08` ke getter target `0x80012A70`; hubungan ini berlaku untuk jalur pemuatan konfigurasi yang dianalisis, bukan label semantik semua record. Field `+0x0C` mengalir ke getter `0x80012A90`, tetapi artinya tetap **UNKNOWN**. Pemetaan ID mentah ke mode/stage masih belum lengkap; ini tidak membuktikan formula biaya atau aturan gameplay universal.
- Direktori bootstrap DATA.BIN memiliki 1.504 entry (1.500 aktif). Struktur direktorinya didukung bukti byte-level; makna seluruh resource dan alamat muat runtime belum terbukti.
- Base entry 0 `0x800AD000` dan entry 1 `0x800D0000` tetap **HIPOTESIS**. Peta statis tidak boleh diperlakukan sebagai peta memori aktual game berjalan.

## Bukti runtime dalam konteks roulette

- Run [#40470778244](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40470778244) berhasil memuat checkpoint roulette yang telah diverifikasi dan mencatat caller RNG. Ini bukti aktivitas RNG dalam jendela tersebut, bukan bukti pemetaan hasil roulette ke caller tertentu.
- Run koreksi [#40473505032](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473505032) mencatat input Circle tekan/lepas lulus pada 3 cabang. Namun, harness berhenti dengan timeout saat mengatur capture/branch finish. Satu tangkapan X11 R30A frame 171 lulus pemeriksaan ukuran/warna/hash, sedangkan R30B dan DELAY60 tidak mendapat capture valid. Ringkasan otomatis dari run ini tidak layak digunakan sebagai perbandingan determinisme karena frame/data tidak lengkap dan parser laporan awal rusak. Jangan gunakan run gagal itu untuk menyatakan determinisme hasil atau hasil roulette.
- Caller yang terlihat pada jendela tersebut mencakup `0x8010C20C`, `0x8010C248`, `0x8010C68C`, dan pada fase akhir `0x80105F48`. Labelnya dibatasi sebagai caller yang teramati dalam konteks checkpoint roulette; makna individu dan hubungan kausal dengan nilai akhir masih **UNKNOWN**.

## Klaim yang tidak diizinkan oleh bukti saat ini

1. Tidak ada rumus biaya barrier/level-up yang terbukti.
2. Belum ada aturan universal battle/roulette/turn, logika kartu, atau syarat kemenangan per mode yang berhasil dibuktikan menyeluruh.
3. Tidak satu pun fungsi resource dinamai sebagai caller battle hanya berdasarkan jumlah pemanggilan, alamat, atau nama default Ghidra.
4. Belum ada bukti autentik ending Story Mode; status Story Mode tetap **TIDAK TERBUKTI TAMAT**.
5. Kode sumber asli tidak direkonstruksi: keluaran Ghidra/m2c adalah pseudocode/representasi decompiler dengan batasan masing-masing.

## Langkah lanjut paling bernilai

- Tutup perbandingan Step 4 dengan capture frame yang konsisten dan parser yang diuji, lalu lakukan pengamatan battle secara terpisah hanya dengan checkpoint battle autentik setelah tersedia dan terverifikasi.
- Untuk aturan Chakra, trace sumber operand dan store untuk field record dan pending-delta `+0xB30`, `+0xB38`, `+0xB40`, `+0xB44`; ikat setiap klaim ke branch, callsite, dan perubahan yang dapat diamati.
- Lanjutkan validasi loader/base sebelum menaikkan semantik caller resource dari HIPOTESIS menjadi TERVERIFIKASI.

Kesimpulan: **Langkah 8 = SEBAGIAN**; bagian yang bisa dinyatakan benar dipisahkan eksplisit dari hipotesis dan unknown.

## Addendum — hasil tracing dataflow statis lanjutan (27 Oktober 2026)

Review terhadap raw job log runner-only Step 6 [#40473737136](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136) menambahkan batas fakta berikut, semuanya **statis dan bersyarat pada base entry-1 hipotetis `0x800D0000`**:

- **TERVERIFIKASI-STATIS (pola instruksi/pseudocode):** kandidat `0x8011C0D0` pada cabang argumen nonzero menegasikan word peserta di record `index * 0x90 + 0x04`, menjepit nilai minimum ke `-9999`, menyimpannya, lalu melewatkan indeks dan nilai itu ke setter `0x8001387C`. Ini tidak membuktikan mengapa nilai dinegasikan atau apakah ia merepresentasikan biaya, pengembalian, sinkronisasi, atau nilai sementara.
- **TERVERIFIKASI-STATIS (urutan bersyarat, bukan efek akhir):** cabang kandidat di sekitar `0x80111228`, `0x801112CC`, `0x801113B4`, `0x801114F0`, dan `0x80111588` membaca target melalui `0x80012A70`, membandingkannya dengan word record peserta menggunakan stride `0x90`, lalu pada cabang-cabang tertentu menulis `+0x58B` dan kode 16-bit pada `+0x5D2` sebelum memanggil `0x800EF98C`. Nilai kode yang terlihat mencakup `0`, `4`, `8`, `0x20`, `0x200`, dan `0x1000`; nilai tersebut tidak diberi nama semantik.
- **HIPOTESIS/UNKNOWN:** relasi cabang tersebut dengan perubahan Chakra, barrier, level-up, turn, kemenangan, atau kegagalan. Efek akhir `0x800EF98C`, `0x80100D14`, dan `0x80100DCC` belum didukung batas fungsi dan control-flow yang bersih. `0x800E1188` mengandung peringatan Ghidra tentang bad instruction data.
- **TERVERIFIKASI-STATIS (stores, makna UNKNOWN):** artifact teks penuh runner-review #12719587873 menunjukkan lima candidate functions `0x80111228`, `0x801112CC`, `0x801113B4`, `0x801114F0`, dan `0x80111588` menulis byte `+0x2E9=0x3F`, `+0x2E5=0`, byte selektor di `+0x58B`, dan pada cabang tertentu kode 16-bit `+0x5D2` (`0x200`, `8`, `4`, `0x20` atau `0`/`0x1000`). Nilai kode dan arti offset tidak dapat dinamai barrier/level-up/turn tanpa bukti lain.
- **BELUM TERUJI:** source operand dan seluruh final stores untuk `+0xB30`, `+0xB38`, `+0xB40`, `+0xB44`; juga alias/identitas object-base dan efek runtime bagi `+0x2E9/+0x2E5`. Pencarian baru pada text artifact adalah langkah lebih lengkap daripada grep sebelumnya, tetapi tidak membuktikan tidak adanya penggunaan di kode yang tidak terdekode/tercakup.

Status Langkah 8 tetap **SEBAGIAN**. Temuan statis ini memperjelas bentuk beberapa operasi dan field yang ditulis, tetapi tidak memenuhi aturan gameplay universal, rumus biaya barrier/level-up, atau syarat kemenangan setiap mode.

## Addendum — penajaman status berdasarkan raw MIPS (27 Oktober 2026)

Review [Actions #40473737136 / artifact #12719587873](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136) mendukung rincian control-flow statis, bersyarat pada base entry-1 hipotetis 0x800D0000: enam site 0x80111228, 0x801112CC, 0x801113B4, 0x801114F0, 0x80111588 dan 0x80112418 membandingkan word record +0x04 (stride record 0x90) dengan getter target 0x80012A70. Jalur tertentu mengarah ke 0x8011253C saat record lebih kecil daripada target. Site 0x801112CC memiliki gate bit 0x200 pada halfword record +0x0A; site 0x801114F0 menambahkan gate hasil helper 0x800BDBFC(0x20) terhadap global 0x8013EBB0; site 0x80111588 menggunakan byte sumber berbeda dan menguji bit 0x1000 dari helper 0x80012AD0. Cabang diterima menulis byte +0x58B, +0x2E9, +0x2E5 dan kode halfword +0x5D2 sesuai jalur.

- **TERVERIFIKASI-STATIS (bersyarat base hipotetis):** operand/pembandingan/cabang serta store yang dirinci di report Step 6. Ini bukan mapping runtime atau bukti menang.
- **HIPOTESIS/UNKNOWN:** arti kode 0x200, 8, 4, 0x20, 0 dan 0x1000; arti byte/state; hubungan dengan Chakra, barrier, level-up, turn atau victory.
- **BELUM TERUJI:** sumber dan seluruh pembaca/penulis pending fields +0xB30/+0xB38/+0xB40/+0xB44. Ketiadaan dari artifact terarah tidak membuktikan tidak ada pemakaian di kode lainnya.

Step 8 tetap **SEBAGIAN**. Tidak ada dasar untuk menyatakan formula biaya universal, mekanika battle/roulette/turn, efek kartu atau syarat menang semua mode.

## Addendum — status rinci jalur perubahan Chakra (27 Oktober 2026)

Dekomposisi statis kandidat 0x8011C0D0 pada DATA.BIN entry 1 (base 0x800D0000, masih HIPOTESIS) menunjukkan bahwa input byte dibandingkan dengan global 0x80139F70; nilai yang sama menyebabkan return dini, sementara nilai berbeda disimpan ke global dan ke field +0x618 dari pointer record global. Pada argumen nonzero, fungsi menulis 8 ke +0x22 pada record terpilih, mengiterasi peserta ber-stride 0x90, menegasikan word field +0x04, menjepit minimum -9999, menyimpan hasil, lalu memanggil setter 0x8001387C untuk tiap indeks. Sebuah pemeriksaan (signed short)[base+0x10] + (unsigned short)[base+0x14] < 0x101 memilih antara panggilan 0x8003F5D0 dan jalur yang menulis 1 ke +0x94A; 0x800F96A4 juga dipanggil pada jalur tertentu.

Ini adalah urutan operasi yang didukung dekompilasi statis 408-byte function body. Raw window yang tersimpan hanya menunjukkan bagian awal fungsi; source caller, nilai runtime, makna argumen 0/nonzero, dan efek helper tidak diketahui. Oleh sebab itu, pola negasi/clamp tidak boleh dinamai sebagai harga barrier, level-up, refund, atau transaksi final Chakra. Field +0xB30/+0xB38/+0xB40/+0xB44 tetap BELUM TERUJI secara whole-program. Status Langkah 8 tetap SEBAGIAN.

## Addendum — batas fakta field writes dari full review artifact

`step6-audit-artifact.txt` dari [runner review #40473737136](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136) menyediakan dekompilasi dan instruction windows untuk lima kandidat: semua lima menulis `+0x2E9=0x3F` dan `+0x2E5=0`, bersama `+0x58B` yang diisi selektor/indeks byte. Nilai `+0x5D2` berubah bersyarat pada masing-masing routine. Ini menyempurnakan inventaris stores, bukan semantik permainan. Base entry-1 `0x800D0000`, object-base alias dan runtime stores masih belum tervalidasi. Step 8 tetap **SEBAGIAN**.

## Addendum — sumber return helper dan aliran nilai field (27 Oktober 2026)

Bukti statis yang diperiksa dalam runner-only audit [#40497668341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40497668341) memperjelas dua aliran nilai tanpa memberi nama mekanik.

1. **Helper `0x80037138`:** jika argumen `a0` negatif, raw MIPS memuat global `0x80066E7C` ke `v0` dan mengembalikan nilai itu. Pada callsite kandidat entry 0, delay slot `li a0,-1` memasok input negatif, lalu delay slot `move a0,v0` pada call setter `0x80035DA8` meneruskan return helper. Jadi sumber argumen statis setter adalah global `0x80066E7C` pada jalur tersebut, bukan konstanta -1. Nilai global saat boot, writer/initializer, dan runtime reachability tetap UNKNOWN.
2. **Field entry 1:** raw MIPS menunjukkan `+0xB30 + +0xB38 -> +0xB40`, `+0xB44` diset nol pada satu jalur inisialisasi, dan `+0xB44` kemudian dibaca sebagai argumen `a2` untuk `0x8001B364`. Base `0x800D0000` adalah HIPOTESIS; label cost/turn/barrier/level-up dan makna helper tidak dibuktikan.

Audit runner #40497668341 selesai success 18:38:45 WIB, artifact #12730957210 (9.014 byte, ZIP SHA-256 `695e36bf70237913c0f80c94f0d4100732c92dd8b78155da2ace90d189c5ee24`), cleanup PASS. Step 8 tetap **SEBAGIAN**; hasil ini memetakan operasi statis, bukan aturan gameplay universal atau hasil kemenangan.

## Addendum — referensi global return helper (27 Oktober 2026)

Ghidra direct-xref export untuk global 0x80066E7C mencatat image word awal 0 dan delapan referensi: writer nol pada 0x80037B7C, writer v0 pada 0x80037BDC setelah increment, serta reads di 0x80037BB4, 0x8003719C, 0x80037204, 0x80037260, 0x800372C0, dan 0x80037324. Ini cukup untuk menyebut pola operasi “counter-like” secara deskriptif, bukan untuk menamai makna game. Sumber return statis helper 0x80037138 pada input -1 adalah nilai global tersebut; value saat boot dan callsite runtime belum dibuktikan.

Audit runner-only [#40498386273](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498386273) selesai success 18:44:35 WIB, artifact #12731327556, ZIP SHA-256 7826480f41372d68ddf3f4b1dfe6d99f51bbbb5cd124eb5c3c6169870150ba5c; cleanup PASS. Step 8 tetap SEBAGIAN; tidak ada nama mekanik, formula biaya, aturan battle/roulette/turn, efek kartu, atau syarat menang yang disimpulkan dari xrefs saja.

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
