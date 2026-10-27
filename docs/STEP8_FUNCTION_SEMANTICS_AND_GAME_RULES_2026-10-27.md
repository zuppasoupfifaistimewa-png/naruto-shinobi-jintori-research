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
