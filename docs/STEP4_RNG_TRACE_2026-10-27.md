# LIVE ADDENDUM — helper/callback cross-check di Langkah 5 (27 Oktober 2026, 20:50 WIB)

Run [#40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524) membandingkan Ghidra/m2c pada 13 fungsi main EXE; artefak [#12739676233](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524/artifacts/12739676233), 941.176 byte, SHA-256 ZIP `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d). Semua 13 pasangan C nonempty, m2c exit 0 dan parser body/end fixture PASS; cleanup selesai. Ini bukti struktur statis lintas decompiler, bukan observasi game runtime.

Cross-check fungsi `0x80037138` kini mendukung detail tambahan: ketika argumen pertama negatif, fungsi mengembalikan `DAT_80066E7C`; ketika argumennya 1, ia mengembalikan selisih timer 16-bit; argumen lain dapat memanggil `0x800372B0` dan memperbarui state timer. Bersama `0x80037B58` yang mereset `0x80066E7C` dan delapan callback slot, serta `0x80037BB0` yang menaikkan global dan memanggil callback nonzero, ini memperkuat interpretasi **callback/tick-counter internal** pada alur statis. Ia belum membuktikan penghitung giliran gameplay.

Dalam callsite entry-0 kandidat pada base hipotetis `0x800AD000`, argumen `-1` dikirim ke helper `0x80037138`, dan nilai balik helper diteruskan ke kandidat setter state RNG `0x80035DA8`. Jadi jika callsite tersebut benar-benar berjalan, nilai yang diteruskan adalah global `0x80066E7C`, bukan literal `-1`. Namun target base/lifecycle entry-0 dan reachability runtime belum terbukti, sementara probe setter terdahulu tidak mendapat hit sampai frame 120. **Status Step 4 tetap SEBAGIAN**; jangan menyebut ini sebagai seed awal yang sudah terverifikasi atau sebagai RNG yang pasti menentukan roulette/menang.

---

# Latest checkpoint — helper-return/callback counter statically traced (27 October 2026, 19:22 WIB)

Run #40498208067 completed success at 19:14:42 WIB. Text-only artifact #12732952776 is 2,255,170 bytes, SHA-256 ZIP 6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6. Runner audit [#40503223693](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40503223693), artifact #12733512950 (13.079 bytes, ZIP SHA-256 382773f9a421835bc97c448c630a2ea5d3891309bb34094f5a67027548c03414), validated artifact id/run id/name/size/digest/expiry for the latest Ghidra, Step 6, and helper artifacts. The audit log confirms ZIP digest verification before reading and RUNNER_ARTIFACT_CLEANUP=PASS.

## New static facts, not runtime seed proof

- Main EXE function 0x80037B58 writes zero to global 0x80066E7C at 0x80037B7C and clears eight 32-bit callback slots beginning at 0x80066E5C by calling 0x80037C48 with count 8 in the JAL delay slot.
- It prepares a0=0 and a1=0x80037BB0, then calls indirect dispatcher 0x800373F8; this dispatcher invokes a pointer through PTR_PTR_80066E3C + 8. Callback-registration semantics are strongly supported statically, but not runtime-confirmed.
- Function 0x80037BB0 reads global 0x80066E7C, increments at 0x80037BD4, writes at 0x80037BDC and iterates the eight slots, calling nonzero pointers via JALR.
- Function 0x8003755C uses guard 0x80065DB4 and its zero path calls 0x80037B58 at 0x800375F0. Delay slot SH v0,-0x3c(s0) at 0x800375F4 stores 1 to 0x80065DB4 given s0=0x80065DF0, before the target executes.
- Function 0x80037138 returns global 0x80066E7C in v0 on its negative-a0 path at 0x8003719C. Other paths calculate a difference and call 0x800372B0; it is not a constant-return stub.
- Candidate DATA.BIN entry0 chain under hypothetical base 0x800AD000: JAL 0x80037138 at 0x800AF2A4, delay-slot LI a0,-1 at 0x800AF2A8, JAL 0x80035DA8 at 0x800AF2AC, setter's delay slot MOVE a0,v0 at 0x800AF2B0. Thus -1 is the helper argument; the setter receives the helper return. Runtime base/order/actual execution remain UNKNOWN.
- Static direct xrefs to 0x80066E7C include write 0x80037B7C, increment/store 0x80037BDC, read 0x80037BB4, and reads 0x8003719C, 0x80037204, 0x80037260, 0x800372C0, 0x80037324. Loaded-image bytes 00000000 are not runtime RAM.

**Step 4 remains SEBAGIAN.** We have static reset/increment/access evidence for a callback/tick-like global, not a verified gameplay seed. Entry0 base 0x800AD000 is only a hypothesis; initializer order relative to setter callsite, runtime reachability, roulette result causality, battle caller, indirect/jump-table/decompressed paths and alternative RNG are unresolved. Existing coldboot setter probe #40485987817 had no hit through frame120, exit124 at 35s; do not repeat unchanged probe without a newly justified PC/reachability hypothesis.

Closure matrix: [STEP4_10_CLOSURE_REPORT_2026-10-27.md](STEP4_10_CLOSURE_REPORT_2026-10-27.md).

---

# Langkah 4 — penelusuran statis RNG dan pemanggil langsung

Tanggal: 27 Oktober 2026  
Cakupan laporan ini: **SELESAI untuk cakupan executable utama dan helper daftar yang dapat ditelusuri statis**. Status keseluruhan Step 4 tetap **SEBAGIAN** karena seed/lifecycle, caller-to-roulette causality, battle caller, dispatch tidak langsung/decompressed code, dan randomness alternatif belum terpenuhi.

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

Dengan demikian subcakupan **pemetaan teknis statis atas RNG dan helper daftar yang terlihat pada executable utama** selesai. Ini bukan penutupan Langkah 4 secara keseluruhan: seed/lifecycle, caller roulette/battle, dispatch/pointer menyeluruh, kode yang baru tampak sesudah decoding, dan randomness alternatif tetap UNKNOWN/SEBAGIAN. Semantik gameplay tidak boleh ditebak dari label `FUN_...`.


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

Kesimpulan: probe bounded ini **tidak membuktikan** bahwa setter seed dipanggil pada jendela cold boot yang diuji. Karena PC runtime target tidak tercapai/teramati, hasil itu juga tidak membuktikan bahwa setter tidak pernah dipanggil di jalur lain atau boot yang lebih lambat. Callsite statis `0x800AF2AC → 0x80035DA8` tetap kandidat berdasarkan base entry-0 `0x800AD000`; argumen setter berasal dari nilai return helper `0x80037138`, bukan langsung dari `li a0,-1`. Nilai return helper dan seed boot/lifecycle pada subkriteria 4(a) tetap UNKNOWN/SEBAGIAN. Tidak ada probe runtime tambahan yang diperlukan tanpa hipotesis baru.

## Addendum — audit return helper setter masih berjalan (27 Oktober 2026)

Audit delay slot memisahkan input helper dari input setter: `0x800AF2A8 li a0,-1` adalah delay slot milik `jal 0x80037138`; `0x800AF2B0 move a0,v0` adalah delay slot milik `jal 0x80035DA8`. Maka setter menerima return `$v0` dari `0x80037138`, bukan nilai `-1` yang diterapkan ke helper. Fungsi setter menyimpan `$a0` ke global state, tetapi nilai spesifik yang sampai ke sana belum dibuktikan.

Untuk menjawab celah tersebut, `tools/ghidra/ExportRngCallerAnalysis.java` menambahkan `dumpSimpleFunction(0x80037138)` dan xref helper. Run statis [#40487406384](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40487406384) pada source commit `b92aa084aba62182ed4edc436cf20d68581be984` merupakan snapshot historis; status terbaru adalah Ghidra #40498208067 success dan artifact #12732952776 sudah diverifikasi runner-side oleh #40503223693. Seed-setter probe runtime #40485987817 tidak memperoleh hit; itu tidak menggantikan pembuktian statis.

## Addendum — return helper menuju kandidat seed setter (27 Oktober 2026, audit runner 18:38 WIB)

Runner-only audit [#40497668341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40497668341) memeriksa ekspor Ghidra dari artefak #12728867894 dan raw target helper. Artefak audit #12730957210 berukuran 9.014 byte, ZIP SHA-256 `695e36bf70237913c0f80c94f0d4100732c92dd8b78155da2ace90d189c5ee24`; cleanup runner-only PASS. Ekspor helper menunjukkan `0x80037138` berukuran 376 byte/94 instruksi, dengan raw MIPS dan C dekompilasi.

Untuk input negatif, cabang `bgez a0,0x800371a8` tidak diambil; delay slot `andi s1,v0,0xffff` dijalankan, kemudian `lui v0,0x8006; lw v0,0x6e7c(v0); j 0x8003729c`. Return aktual di jalur ini berasal dari isi global `0x80066E7C`. Callsite kandidat entry 0 sebelumnya terverifikasi statis sebagai `jal 0x80037138` dengan delay slot `li a0,-1`; panggilan setter berikutnya `jal 0x80035DA8` memiliki delay slot `move a0,v0`. Inferensi dataflow: apabila callsite kandidat terjadi, nilai global `0x80066E7C` diteruskan sebagai argumen setter. Ini bukan bukti bahwa nilainya -1, bukan bukti nilai global pada boot, dan bukan bukti runtime callsite benar-benar berjalan. Base `0x800AD000` masih HIPOTESIS.

Fungsi helper juga mempunyai jalur nonnegatif yang menghitung selisih `*DAT_80065d38 - DAT_80065d3c` yang dimask 16 bit dan memanggil helper `0x800372B0`; karena itu helper tidak boleh digeneralisasi sebagai stub konstan. Xrefs/initializer semua data global `0x80066E7C` dan lifecycle nilainya masih perlu ditelusuri.

Run helper [#40493608676](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40493608676) gagal pada pengecekan marker saja: teks target di Ghidra tanpa prefiks `0x` dan alamat setter lowercase. Raw log tetap menunjukkan cleanup PASS dan artefak teks #12730020903 (8.395 byte, digest ZIP `00b54f4e8c059f81d0f4d75aea04f2deccece564edff73378096b369e4fd7c79`). Fragmen YAML duplikat pada akhir workflow kemudian ditemukan dan dibuang pada `029fdfab8df55dd16001916f0f53b7abd073c334`; run koreksi #40497723766 perlu diverifikasi live.

## Addendum — reference audit global helper-return 0x80066E7C (27 Oktober 2026, 18:44 WIB)

Ekspor xref baru lewat run helper statis [#40498231825](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498231825) menunjukkan 8 referensi langsung ke global 0x80066E7C dalam view executable utama. Loaded-image bytes adalah 00 00 00 00 (word LE 0), sedangkan fungsi yang ditunjuk instruksi adalah:
- WRITE 0x80037B7C: sw zero,0x6e7c(at), di fungsi 0x80037B58.
- READ 0x80037BB4 dan WRITE 0x80037BDC dalam fungsi 0x80037BB0; write didahului addiu v0,v0,1 pada 0x80037BD4.
- READ 0x8003719C, 0x80037204, 0x80037260 dalam fungsi 0x80037138.
- READ 0x800372C0 dan 0x80037324 dalam fungsi 0x800372B0.

Runner-only inspection [#40498386273](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498386273) selesai success 18:44:35 WIB, artifact #12731327556 9.727 byte, ZIP SHA-256 7826480f41372d68ddf3f4b1dfe6d99f51bbbb5cd124eb5c3c6169870150ba5c, cleanup PASS. Metadata/digest artifact helper terbaru #12732006381 (run #40498231825, 9.058 byte, SHA-256 adfdb608af96dd95a7c7e74d9f8b117767aaffa817d0c7eb860757ead868d9ba) cocok.

Data awal 0 dan pola store-nol/increment membuat global ini COUNTER-LIKE sebagai deskripsi operasi statis saja; belum terbukti sebagai jenis penghitung tertentu atau seed aktual pada boot. Harus telusuri caller fungsi 0x80037B58/0x80037BB0 dan urutannya terhadap callsite candidate 0x800AF2AC. Indirect references/overlay/runtime writers belum dicakup lengkap. Step 4 tetap SEBAGIAN.

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
