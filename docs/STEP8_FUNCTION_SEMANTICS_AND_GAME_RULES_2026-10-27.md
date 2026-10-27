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
- **BELUM TERUJI:** penelusuran seluruh source operand dan final store untuk `+0xB30`, `+0xB38`, `+0xB40`, `+0xB44`, `+0x2E9`, dan `+0x2E5`. Offset ini tidak muncul dalam ekstrak dekompilasi terarah yang diperiksa; itu bukan bukti bahwa tak ada pemakainya di bagian kode lainnya.

Status Langkah 8 tetap **SEBAGIAN**. Temuan statis ini memperjelas bentuk beberapa operasi dan field yang ditulis, tetapi tidak memenuhi aturan gameplay universal, rumus biaya barrier/level-up, atau syarat kemenangan setiap mode.

## Addendum — penajaman status berdasarkan raw MIPS (27 Oktober 2026)

Review [Actions #40473737136 / artifact #12719587873](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136) mendukung rincian control-flow statis, bersyarat pada base entry-1 hipotetis 0x800D0000: enam site 0x80111228, 0x801112CC, 0x801113B4, 0x801114F0, 0x80111588 dan 0x80112418 membandingkan word record +0x04 (stride record 0x90) dengan getter target 0x80012A70. Jalur tertentu mengarah ke 0x8011253C saat record lebih kecil daripada target. Site 0x801112CC memiliki gate bit 0x200 pada halfword record +0x0A; site 0x801114F0 menambahkan gate hasil helper 0x800BDBFC(0x20) terhadap global 0x8013EBB0; site 0x80111588 menggunakan byte sumber berbeda dan menguji bit 0x1000 dari helper 0x80012AD0. Cabang diterima menulis byte +0x58B, +0x2E9, +0x2E5 dan kode halfword +0x5D2 sesuai jalur.

- **TERVERIFIKASI-STATIS (bersyarat base hipotetis):** operand/pembandingan/cabang serta store yang dirinci di report Step 6. Ini bukan mapping runtime atau bukti menang.
- **HIPOTESIS/UNKNOWN:** arti kode 0x200, 8, 4, 0x20, 0 dan 0x1000; arti byte/state; hubungan dengan Chakra, barrier, level-up, turn atau victory.
- **BELUM TERUJI:** sumber dan seluruh pembaca/penulis pending fields +0xB30/+0xB38/+0xB40/+0xB44. Ketiadaan dari artifact terarah tidak membuktikan tidak ada pemakaian di kode lainnya.

Step 8 tetap **SEBAGIAN**. Tidak ada dasar untuk menyatakan formula biaya universal, mekanika battle/roulette/turn, efek kartu atau syarat menang semua mode.
