# Langkah 4 — penelusuran statis RNG dan pemanggil langsung

Tanggal: 27 Oktober 2026  
Status: **SELESAI untuk cakupan executable utama dan helper daftar yang dapat ditelusuri statis**. Arti gameplay daftar/kandidat, seed runtime, dan kode overlay tidak dianggap selesai oleh laporan ini.

## Sumber dan reproduksi

- Executable: `SLPS_035.53`, 385.024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
- Run Ghidra + helper/cross-reference trace: [Actions #40439763833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40439763833), sukses.
- Artefak teks saja: [ghidra-slps-03553-function-index, artifact 12705072941](https://api.github.com/repos/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/artifacts/12705072941).
- Untuk run Ghidra/caller trace yang diringkas di bagian statis ini, tidak ada emulator/gameplay yang dijalankan. Cold-boot runtime terpisah tanpa input/restore didokumentasikan pada addendum paling bawah. Executable disc dan resource tidak masuk Git atau artefak; hanya hasil teks yang diarsipkan.

## Generator dan seed

Rutin di `0x80035D78` membaca state global `0x800A3118`, mengalikan dengan `0x41C64E6D`, menambahkan `0x3039` modulo (2^{32}), menyimpan state, dan mengembalikan `(state >> 16) & 0x7FFF`. Bukti instruksi langsung dan empat pemanggil langsung terdeteksi di executable utama.

Di `0x80035DA8` ada urutan instruksi yang cocok dengan setter state berbasis argumen `$a0`, tetapi Ghidra tidak menemukan referensi langsung ke alamat itu pada executable utama. Seed awal dan pemanggil tidak langsung belum diketahui; absennya referensi langsung bukan bukti bahwa setter tidak pernah digunakan melalui pointer/overlay.

## Empat pemanggil langsung

| Call site RNG | Fungsi | Kesimpulan statis yang didukung |
|---|---|---|
| `0x80015B14` | `FUN_80015adc` | Membentuk indeks dari nilai RNG dan helper pembatas, lalu memanggil helper penyisipan. Fungsi berada pada jalur pembentukan/pemilihan elemen daftar berbatas. |
| `0x80015BF0` | `FUN_80015b7c` | Melakukan pertukaran pasangan elemen byte berulang; konsisten dengan pengacakan urutan daftar. |
| `0x8001A460` | `FUN_8001a328` | Memilih secara acak satu nilai dari daftar lokal kandidat yang disaring oleh bitset. Nilai disimpan ke `DAT_80089DA9`. |
| `0x80020C24` | `FUN_80020bf4` | Menyimpan nilai RNG modulo `0x1000` ke field `param_1[0xD]`, lalu memanggil helper yang menulis `0x1000` ke field struktur dan routine tambahan. Hubungan ke mekanik gameplay belum dibuktikan. |

## Helper dan struktur daftar yang ditelusuri

- `FUN_800154d4` mengembalikan `DAT_8006D794`, dipakai sebagai batas/limit pembentukan kandidat.
- `FUN_800158d8` mengembalikan byte penghitung di `DAT_80070D02`.
- `FUN_800159bc` menyisipkan byte ke daftar mulai `DAT_80070D0A), menggeser elemen berikutnya, dan menambah penghitung. Insertion dibatasi oleh nilai `DAT_8006D794` dan ukuran maksimum `0x40`.
- `FUN_80015610` membaca data dari tabel `DAT_8005603C` dengan indeks parameter kurang dari `0x12`; ia menyalin byte sampai sentinel `0xFF` dengan batas 64 entri, menulis penghitung terkait `DAT_80070D02`/field berikutnya, lalu memanggil routine shuffle dan mereset word cursor. Format logis penuh kedua segmen daftar belum dipastikan.
- `FUN_80015768` mengambil byte awal dari `DAT_80070D0A`, memanggil helper pembaru daftar dan shuffle, lalu mengembalikan byte yang tadi dibaca.
- `FUN_800157C4` membaca elemen `DAT_80070D0A` melalui indeks cursor `DAT_80070D06`.
- `FUN_80016c68(code)` menguji bit `code` pada bitset sekitar `DAT_80070770` untuk kode kurang dari `0xA0`. `FUN_8001a328` memeriksa kode `0x7F`–`0x86` dan menambahkan kandidat `0,1,2,3,4,5,8,9,0xB` sesuai hasil test sebelum mengambil satu kandidat acak.

## Hasil dan batas interpretasi

**Keyakinan tinggi:** perilaku aritmetika LCG, empat call site langsung, insertion/shuffle daftar byte, bit-test, dan pemilihan dari daftar kandidat sebagaimana dekompilasi Ghidra.  
**Belum diketahui:** nama/arti gameplay tabel `DAT_8005603C`, kode yang disimpan pada `DAT_80089DA9`, seed runtime, pengaruh helper tambahan pada gameplay, serta pemanggil di modul/overlay lain.

Dengan demikian Langkah 4 selesai sebagai **pemetaan teknis statis atas RNG + helper daftar yang terlihat pada executable utama**. Pemetaan runtime dan semantik gameplay dilanjutkan di Langkah 5 dan 6, bukan ditebak dari label `FUN_...`.


## Pembaruan cakupan lintas resource — 27 Oktober 2026

### Hasil baru yang terverifikasi secara statis

Workflow [Ghidra entry 1 #40454881770](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40454881770) memeriksa DATA.BIN entry 1 (596.412 byte; SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`) sebagai program MIPS little-endian pada base analisis kandidat `0x800D0000`.

- Dari 144 kata JAL mentah ke target `0x80035D78`, **108** menjadi direct-call flow yang benar-benar didekode Ghidra pada address map kandidat.
- 108 call site itu berada pada **50 fungsi pemanggil dengan batas fungsi dikenali**, ditambah satu call site `0x80128AF8` yang tidak memiliki batas fungsi pada pass tersebut.
- **36** kandidat kata JAL tetap tidak terdekode; dicatat terpisah dalam [inventaris caller entry 1](../out/rng_resource_entry1_ghidra_callers_2026-10-27.md), bukan dianggap caller terkonfirmasi atau otomatis dianggap data.
- Tidak ada JAL mentah ke kandidat seed setter `0x80035DA8` dalam entry 1.

### Konteks entry 0

Workflow konteks lokal [#40455197588](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455197588) dengan `-noanalysis` memeriksa lima lokasi, tanpa menjalankan emulator/gameplay. Pada base **hipotetis** `0x800AD000`:

- `0x800AF2AC` didekode sebagai `jal 0x80035DA8`, tetapi delay slot harus ditafsirkan tepat: `0x800AF2B0 move a0,v0` dieksekusi sebelum masuk ke setter dan meneruskan `$v0` dari helper sebelumnya (`0x80037138`). Instruksi `li a0,-1` pada `0x800AF2A8` adalah delay slot dari panggilan helper tersebut, jadi `-1` adalah input helper, bukan terbukti input setter. Tanpa menelusuri nilai balik `0x80037138`, nilai yang disimpan ke state RNG tetap UNKNOWN. Jalur ini juga belum terverifikasi runtime.
- `0x800BB2D8` didekode sebagai `jal 0x80035D78`; konteks berikutnya memanggil helper dan melakukan pembagian unsigned terhadap hasil, konsisten dengan pemilihan modulo berbatas.
- `0x800BB2FC`, `0x800BB748`, dan `0x800BB770` belum dikonfirmasi sebagai instruksi caller pada pass lokal awal. Ketiganya tetap UNKNOWN sampai disassembly tepat di lokasi dan analisis jalur kontrol selesai.

### Status Langkah 4

RNG main EXE dan empat caller langsungnya **SELESAI**. Inventaris statis silang resource sudah jauh lebih lengkap, namun **Langkah 4 keseluruhan masih SELESAI SEBAGIAN**: 36 kecocokan mentah entry 1 belum diklasifikasikan, tiga kandidat entry 0 belum terdekode sebagai call, base resource masih hipotesis, dan caller tak langsung/ruang kode hasil dekompresi tidak bisa disingkirkan dari scan byte mentah saja. Label gameplay (roulette/battle/turn/AI) belum diberikan tanpa bukti call chain/tabel.

Rujukan hasil entry 1: [inventaris caller Ghidra](../out/rng_resource_entry1_ghidra_callers_2026-10-27.md).

## Koreksi final cakupan caller statis — 27 Oktober 2026

Run Ghidra [#40455582988](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455582988) memeriksa ulang 36 alamat entry 1 yang tidak didekode oleh auto-analysis. **36/36** kini didekode secara terarah sebagai `jal 0x80035D78`, menutup status “belum didekode” pada instruksi tersebut. Laporan rinci: [out/rng_resource_entry1_unmapped_context_2026-10-27.md](../out/rng_resource_entry1_unmapped_context_2026-10-27.md). Caller function boundary untuk 36 lokasi tetap UNKNOWN.

Run lokal entry 0 [#40455557190](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455557190) menunjukkan empat instruksi `jal 0x80035D78` di peta alamat kandidat. Tiga memiliki branch masuk eksplisit di jendela lokal; `0x800BB748` tidak, dan terletak selepas `j 0x800BBDE4`, sehingga reachability-nya tetap UNKNOWN. Lokasi `0x800AF2AC` secara statis memanggil kandidat setter `0x80035DA8`; karena `move a0,v0` di `0x800AF2B0` adalah delay slot-nya, argumen setter adalah hasil `$v0` dari helper `0x80037138`. Input `-1` diberikan kepada helper sebelumnya. Nilai return helper dan state akhir masih UNKNOWN. Laporan: [out/rng_resource_entry0_ghidra_context_2026-10-27.md](../out/rng_resource_entry0_ghidra_context_2026-10-27.md).

### Kesimpulan Langkah 4 (versi terkini)

**SELESAI untuk inventaris instruksi direct-JAL pada executable utama dan raw code candidates DATA.BIN yang dipetakan secara statis**, dengan base resource entry 0 (`0x800AD000`) dan entry 1 (`0x800D0000`) tetap hipotesis:
- Main EXE: 4 call site pada fungsi yang batasnya diketahui.
- DATA.BIN entry 0: empat instruksi JAL langsung ke RNG pada konteks lokal (tiga memiliki incoming conditional branch lokal; satu belum terbukti reachable) dan satu direct JAL ke kandidat setter state RNG. Argumen setter belum diketahui: ia meneruskan return helper `0x80037138`.
- DATA.BIN entry 1: 144 instruksi JAL langsung ke RNG; 108 dikelompokkan oleh auto-analysis menjadi 50 fungsi + 1 call site tanpa boundary, 36 lainnya didekode lokal tapi nama fungsi caller belum teridentifikasi.
- Tidak ditemukan kata direct-JAL target sama pada raw DATA2.BIN, DUMMY.BIN, XASECT.BIN; keterbatasan scan raw/non-decompressed tetap UNKNOWN.

Artinya, inventory direct-JAL yang ditemukan sudah ditutup dan semua raw hits penting sudah diperiksa. **Yang tidak boleh diklaim tuntas** adalah panggilan tak langsung/berbasis pointer, kode sesudah dekompresi, base/lifecycle runtime sebenarnya, reachability `0x800BB748`, 36 boundary fungsi yang belum diketahui, atau semantik gameplay caller. Ini batas bukti statis, bukan alasan untuk mengarang kesimpulan.


## Scan signature LCG di raw resource — run #40455975609

Pemindaian tambahan membentuk pola `LUI 0x41C6` + `ORI/ADDIU 0x4E6D` diikuti MULT/MULTU, serta memeriksa immediate `0x3039` pada word MIPS sejajar. Hanya `SLPS_035.53` yang memiliki satu kecocokan pengali + MULT (file offsets `0x26578`, `0x26584`, `0x26588`, yang map ke `0x80035D78`, `0x80035D84`, `0x80035D88`); addend instruction ada pada file offset `0x26590` → `0x80035D90`. Tidak ditemukan konstruksi pengali yang sama dalam raw `DATA.BIN`, `DATA2.BIN`, `DUMMY.BIN`, `XASECT.BIN`. Laporan: [out/step4_rng_signature_scan_2026-10-27.md](../out/step4_rng_signature_scan_2026-10-27.md).

29 immediate `0x3039` di DATA.BIN dan dua di DATA2.BIN tidak cukup untuk menyatakan generator RNG karena tidak disertai pengali yang sama. Ini memperkuat bukti bahwa LCG yang ditemukan adalah generator dengan signature tersebut pada executable utama, tetapi tidak menyingkirkan RNG lain dengan rumus berbeda atau kode terkompresi/decrypted.


## Penutupan akhir Langkah 4 — 27 Oktober 2026

Keputusan status final dan batas bukti disatukan pada [docs/STEP4_CLOSURE_2026-10-27.md](STEP4_CLOSURE_2026-10-27.md). Langkah 4 **SELESAI dalam cakupan inventaris statis yang didefinisikan**: main EXE, seluruh raw direct-JAL hit yang ditemukan, konteks Ghidra entry 0/1, signature LCG, dan pola konstruksi alamat/JALR sempit. Status ini tidak menyatakan semua caller runtime telah ditemukan. Base resource, satu reachability entry 0, 36 boundary fungsi entry 1, caller berbasis pointer/dispatch, serta kode hasil dekompresi/dekripsi tetap UNKNOWN dan tidak boleh dipromosikan menjadi VERIFIED tanpa bukti baru.


## Hasil Ghidra final #40455975408

Run selesai dengan `success`; detail dan batas akhir tercatat pada [penutupan Langkah 4](STEP4_CLOSURE_2026-10-27.md). Final Ghidra caller export mencatat entry 0: 5 raw JAL candidates total, 3 decoded direct-call sites (2 RNG + 1 seed setter), 2 RNG raw-only. Entry 1: 144 raw RNG candidates, 108 decoded direct-call sites dalam 50 fungsi, dan 36 raw-only candidates. Pass disassembly lokal sebelumnya mendekode 36 raw-only entry 1 sebagai JAL, tetapi Ghidra tidak mengesahkan mereka sebagai decoded direct-flow. Maka 152 adalah jumlah raw direct-JAL candidates pada main EXE + DATA.BIN; bukan 152 caller yang seluruhnya tervalidasi Ghidra. Runtime mapping/indirect dispatch tetap UNKNOWN.

## Addendum runtime — seed-setter cold boot #40485987817 (27 Oktober 2026)

Eksperimen baru ini ditujukan khusus untuk kandidat setter state RNG `0x80035DA8`, berbeda dari probe loader `0x800AD454`. Workflow pada source commit `e1e346e707254ad617a6cccad43689df908801a6` menjalankan cold boot tanpa input gameplay/restore savestate, memasang satu breakpoint, dan membatasi sesi target ke 35 detik. Run [#40485987817](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817) selesai `success` 10:08:48 UTC (17:08:48 WIB); artefak teks-only #12724933081 berukuran 4.003 byte, ZIP SHA-256 `74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6`. Raw log memverifikasi semua sumber assets (disc/CUE/BIOS/AppImage), pra-uji mencapai VSync frame 50, listener-only kontrol maksimum frame 60, dan cold boot kandidat setter mencatat progress frame 1–120 dengan `bp_hits=0`; exit 124 pada batas 35 detik serta `STEP7_PRIVATE_CLEANUP=PASS`. Tidak ada `STEP7_SINGLE_BP_HIT`, sehingga `$a0`, `$ra`, dan callsite runtime tidak tersedia.

**Peringatan integritas report:** artefak/run ini dibuat sebelum koreksi fallback alamat. Ringkasan no-hit yang diunggah salah menampilkan `SINGLE_BREAKPOINT_PC=0x800AD454`, alamat target run loader sebelumnya. Ini kesalahan fallback report, **bukan** alamat target yang terdaftar pada run ini: baris raw `STEP7_SINGLE_BP_READY` menyebut persis `target=0x80035DA8`, dan seluruh event progress menampilkan hit 0. Source fallback diperbaiki pada commit `a6734d7fc57ff6dfab9b8135cd5661bf0278c437`; validator [#40486315324](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40486315324) lulus dengan `STEP4_SEED_BP_NO_HIT_FALLBACK_PASS target=0x80035DA8`, `STEP4_SEED_BP_PARSER_FIXTURE_PASS`, dan `STEP7_FRAME_PARSER_FIXTURE_PASS`. Fixture parser sintetis menguji ekstraksi field; bukan bukti hit emulator.

Kesimpulan: probe bounded ini **tidak membuktikan** bahwa setter seed dipanggil pada jendela cold boot yang diuji. Karena PC runtime target tidak tercapai/teramati, hasil itu juga tidak membuktikan bahwa setter tidak pernah dipanggil di jalur lain atau boot yang lebih lambat. Kandidat statis `0x800AF2AC → 0x80035DA8` dan argumen `$a0=-1) tetap hipotesis berdasarkan base entry-0 `0x800AD000`; seed boot/lifecycle pada subkriteria 4(a) tetap UNKNOWN/SEBAGIAN. Tidak ada probe runtime tambahan yang diperlukan tanpa hipotesis baru.
