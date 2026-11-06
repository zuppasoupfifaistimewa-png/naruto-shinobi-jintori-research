# EA0-EA4 — audit statis terfokus Naruto Jintori
Tanggal: 2026-11-06
Target: SLPS-03553 / Entry 1; batas bukti statis maksimum K4.
Sumber awal: HEAD `5fea251ad45f6a44d31ad92c14452c0bb510323f`.
Baseline ledger inklusif: `c405f9261c3beea2ed4e3695222108c51a7ad636`.

## Status dan hasil ringkas

| EA | Status | Tingkat | Hasil |
|---|---|---:|---|
| EA0 | TUNTAS | K4 | Ledger commit diverifikasi; snapshot dan HEAD dipisahkan |
| EA1 | SEBAGIAN | K4 | Identitas tile high-nibble read/write terbukti; cabang pemilih/event trigger dan seed F020 belum terbukti |
| EA2 | SEBAGIAN | K3 | Operand dan store +0x2EE pada F2A9C terpetakan sebagian; full dump/caller/action trigger belum tersimpan |
| EA3 | SEBAGIAN | K3 | Sumber byte tile+0x24 dan dua writer proven terlihat; census seluruh pembaca manager+2B4/+390 belum selesai |
| EA4 | TUNTAS | K4 | Dua ekspresi DYNAMIC EB0C dikoreksi dan span straight-line diverifikasi |

## EA0 — ledger inklusif

Snapshot sumber analisis untuk Actions adalah `56d1ba6a0ac7e874a3229a494e896336a38e7380`. Ledger inklusif pada snapshot itu: **4 commit, 3 manusia, 1 bot**.

HEAD setelah publikasi hasil run adalah `06baf4f5950a50d6a9abc93d08409c5859255061`: **5 commit inklusif, 3 manusia, 2 bot**. Commit laporan/koreksi ini adalah satu commit manusia tambahan; jadi hitungan HEAD setelah commit ini menjadi **6 total, 4 manusia, 2 bot**. Baseline ikut dihitung; total di atas bukan jumlah commit sesudah baseline saja.

## EA1 — FUN_800D15A8 dan tile+0x20

### Bukti identitas tile untuk pasangan high nibble

`0x800D4688` memuat pointer array tile dari slot global `0x8013EA84` ke `$a2`. `0x800D467C` memuat manager dari slot `0x8013EA74` ke `$a1`. Byte index yang dipakai adalah `lbu 0x4A0($a1)`.

Ekspresi indeks MIPS pada jalur read `0x800D46A4` dan jalur write `0x800D4764` identik: urutan `sll 3; addu index; sll 3; addu index; sll 2` menghasilkan `index * 0x124`; kemudian ditambah base array dari `$a2` (slot `0x8013EA84`). Read index pertama dari `0x800D4684` dan read index kedua di `0x800D472C` sama-sama memakai `$a1` dari `0x800D467C`, offset `0x4A0`. Tidak ada store ke `manager+0x4A0`, branch, atau JAL antara read tile `0x800D46A4` dengan store tile `0x800D4764`. Karena base slot dan ekspresi index sama, **tile yang dibaca pada 0x800D46A4 dan ditulis pada 0x800D4764 adalah tile yang sama** — bukti statis K4.

Cuplikan instruksi (setiap excerpt 4 byte):
- `0x800D46A4`: `20 00 42 94` — `lhu $v0,0x20($v0)`.
- `0x800D46AC`: `02 12 02 00` — `srl $v0,$v0,8`.
- `0x800D46B0`: `0F 00 42 30` — `andi $v0,$v0,0xF`.
- `0x800D46B4`: `01 00 42 24` — `addiu $v0,$v0,1`.
- `0x800D46B8`: `0C EB 02 AE` — store ke global `0x8013EB0C`.
- `0x800D4764`: `20 00 62 A4` — `sh $v0,0x20($v1)`.

Setelah high nibble dibaca, kode menghapus lane high pada tile word lewat mask `0xF0FF` di jalur `0x800D471C..0x800D4728`; nilai dari `0x8013EB0C` kemudian digeser 8 bit, di-OR dengan word tile, lalu ditulis pada `0x800D4764`.

### Jalur low nibble dan pertanyaan cabang

Jalur low nibble memuat word tile di `0x800D47B4`, lalu `srl 4`, `andi 0xF`, `addiu 1`; hasil disimpan sementara ke `0x8013EB0C` di `0x800D47C8`. Lane low kemudian dibersihkan menggunakan mask `0xFF0F` di `0x800D47F4`, digabung dengan nilai yang digeser 4 bit di `0x800D4824/0x800D4830`, dan ditulis di `0x800D4834`.

**Tidak ada branch kondisional di rentang instruksi nibble `0x800D4640..0x800D4840` yang memilih salah satu lane.** Keduanya merupakan urutan instruksi straight-line yang dieksekusi berurutan; di antaranya terdapat pemanggilan `0x800B770C` pada `0x800D4780`. Pemanggilan itu memisahkan dua kelompok, sehingga identitas tile antara pasangan high-lane dan pasangan low-lane tidak otomatis dianggap sama. Branch scan lokal yang ditulis dalam run tidak menghasilkan baris cabang. Dengan demikian kondisi pemilih lane dan event gameplay pemicu tidak terbukti; tidak boleh disebut sebagai dua cabang alternatif.

Satu-satunya direct caller yang ditemukan untuk `FUN_800D15A8` adalah JAL di `0x800F5DAC`, dari fungsi pemanggil yang ditebak `FUN_800F3658`. Def-chain argumen caller tidak dapat dipulihkan karena register caller-saved telah ter-clobber oleh JAL `0x800F2490` sebelumnya. Hubungan ke aksi gameplay tertentu: **TIDAK TAHU**.

Setiap lane yang diproses di potongan ini mendapat operasi `+1`, bukan perkalian atau penambahan lebih dari satu pada satu jalur. Tidak ada branch pengulangan di bagian nibble ini. Ini tidak membuktikan level maksimum, clamp, atau jumlah pemanggilan selama satu event di luar potongan.

Pernyataan bahwa low nibble 4–7 mulai dari nilai 2 berdasarkan loader `0xF020` **belum terbukti**. Kandidat alamat/loader yang diperiksa dalam run tidak menghasilkan kecocokan yang cukup untuk mengikat seed 2 ke tile+0x20. Anggap sebagai hipotesis pengguna, bukan fakta ROM.

## EA2 — fee d>=2 dan FUN_800F2A9C

Bukti yang tersimpan pada census +0x2EE:

| PC | Instruksi/store | Provenance nilai tersimpan |
|---|---|---|
| `0x800F2CF8` | `sh $v0,0x2EE($a0)` | `mflo` dari `mult $v0,$v1`; multiplier `$v1` berasal dari `lbu 0x8013EA71` lalu `-2`; multiplicand `$v0` adalah return JAL `0x8001552C` |
| `0x800F2E38` | `sh $v0,0x2EE($a1)` | `mflo` dari `mult $v0,$a0`; `$a0` dibentuk dari `lbu 0x8013EA71` lalu `-1`, dikurangi nilai load dinamis dari global `0x80139EFC`; multiplicand `$v0` berasal dari `negu` atas return JAL `0x8001552C` |
| `0x800F2E68` | `sh $v0,0x2EE($a0)` | `negu` atas return JAL `0x8001552C` |

Basis untuk store F2A9C berasal dari manager pointer slot `0x8013EA74`. Nilai global `0x80139EFC` dan byte `0x8013EA71` diperlakukan sebagai **DINAMIS**, bukan konstanta. Berdasarkan analisis helper sebelumnya, return pada exit yang diaudit dari `0x8001552C` adalah nilai `$v0=1`, ditentukan oleh instruksi return/slot delay pada kode helper, bukan oleh nama fungsi. Jalur return lain yang tidak tercakup oleh def-chain tetap **TIDAK TAHU**.

Tidak ada provenance langsung tile+0x1A pada tiga store F2A9C di census yang tersedia. Namun, karena full function dump terhenti sebelum dihasilkan, kesimpulan global “F2A9C tidak pernah memakai tile+0x1A” **belum boleh dibuat**. Hubungan pemanggil langsung F2A9C dan aksi/event pemicunya juga **TIDAK TAHU** dalam hasil yang tersimpan.

Store +0x2EE lain yang diminta:
- `0x800E408C`: store dari nilai negatif yang dibaca melalui alamat global `0x8013EBB4`.
- `0x800F0F08`: store dari `negu` atas `lhu 0xE($a2)`; base sumber dinamis.
- `0x800DC4FC` dan `0x800DD088`: store dari `lhu 0x4F4($a0)`; base runtime dinamis.
- `0x800E66E8`: store dari `lhu 0x4F4($a0)`; base runtime dinamis.

### Model biaya d=1..4

Angka `100/400/800/1600` adalah hipotesis pengamatan pengguna, bukan konstanta ROM. Normalisasi di bawah memakai 100 sebagai fee dasar hipotetis.

| Model | Faktor d=1,2,3,4 | Prediksi | Banding |
|---|---|---|---|
| H1 `fee_dasar * 2^d` | 2, 4, 8, 16 | 200, 400, 800, 1600 | d=1 bertentangan; d=2..4 cocok |
| H2 `fee_dasar * lookup[d]`, lookup={1:1,2:4,3:8,4:16} | 1, 4, 8, 16 | 100, 400, 800, 1600 | cocok semua, tetapi **TAUTOLOGI** karena lookup disalin dari empat angka pengguna |
| H3 `fee_dasar * (1+2+...+2^(d-1))` | 1, 3, 7, 15 | 100, 300, 700, 1500 | d=2..4 bertentangan |

Falsifier:
- H1 gugur bila kode/tabel ROM mengandung koefisien atau selector lain, atau lima nilai d independen tidak mengikuti rasio 2^d. Urutan D15A8 `lhu tile+1A -> negu -> store` sendiri tidak memuat shift/multiply sebelum fee post.
- H2 tidak memiliki nilai prediksi independen; gugur saat satu nilai d kelima atau tabel ROM independen tidak sesuai lookup yang di-fit.
- H3 gugur bila tidak ada post fee berulang per step dan pengamatan independen pada d=2..4 tetap 400/800/1600.

Pada handler D15A8 terdapat satu negative tile-fee post yang terkonfirmasi dari `u16(tile+0x1A)` pada `0x800D46F8`, dan tidak ada direct back-edge setelah post yang kembali ke fee load. Itu membatasi hipotesis loop akumulasi pada handler tersebut; tidak otomatis menjelaskan formula di FUN_800F2A9C yang merupakan jalur berbeda.

## EA3 — tile+0x24, manager+0x2B4/+0x390, dan 0x8013EAD2

Dua writer tile+0x24 yang lolos bukti base array slot `0x8013EA84` dalam census `lh/lhu/sh +0x24` berada di `FUN_800F7ADC`:
- `0x800F7E2C`: `sh $v1,0x24($a0)`; sumber nilai dari `lbu ($s1)`.
- `0x800F7E40`: `sh $v1,0x24($a0)`; sumbernya byte pada `1($s1)` yang digeser 8 bit lalu di-OR dengan byte sebelumnya.

Ini membuktikan field tile+0x24 dimuat dari pasangan byte sumber dalam loader; tidak membuktikan apakah pasangan byte itu koordinat, owner, level, atau status.

Fan-out yang teridentifikasi:
- `0x800EC388` membaca tile+0x24 lewat slot EA84. `0x800EC364` membaca halfword global `0x8013EAD2` (nilai **DINAMIS**). `0x800EC390` mengurangkan global itu dari tile+0x24 dan `0x800EC398` meneruskan hasil ke manager+0x2B4; base manager dibuktikan lewat slot `0x8013EAB0`.
- `0x800DAF2C` membaca tile+0x24 lewat EA84 dan `0x800DAF34` meneruskannya ke manager+0x390; base manager dibuktikan lewat slot `0x8013EA74`. Pada jalur lokal itu, slot aktif `0x8013EA88` dipakai membentuk index record, bukan terbukti sebagai operand pembanding tile+0x24.
- CFG helper juga memuat store `0x800ED640`, `0x800ED81C`, `0x800ED9C0` ke displacement +0x390, tetapi file CFG yang tersedia tidak membuktikan asal base register untuk ketiganya. Tidak boleh diklaim sebagai manager-base proven.

Census lengkap seluruh pembaca manager+0x2B4 dan manager+0x390 dengan filter base proven tidak berhasil dipublikasikan karena supplemental analyzer berhenti sebelum EA3. Daftar seluruh readers: **TIDAK TAHU**.

Hipotesis:
1. **Posisi/koordinat relatif** — indikasi: tile+0x24 dikurangkan dari global EAD2 lalu diteruskan ke manager+0x2B4. Falsifier: writer/consumer menunjukkan nilainya hanya kode kategori/owner, tidak pernah digunakan sebagai koordinat/perpindahan.
2. **Status tampilan/event** — indikasi: jalur event-3 hanya meneruskan tile+0x24 ke manager+0x390 tanpa arithmetic lokal. Falsifier: pembaca manager+0x390 terbukti melakukan hitungan movement/koordinat atau lookup ekonomi, bukan display/event.
3. **Owner atau level** — masih mungkin tetapi belum didukung tabel transisi atau rentang nilai. Falsifier: pemetaan writer/consumer lengkap memperlihatkan range eksklusif dan transisi owner/level yang teridentifikasi.

Karena penulis proven yang terlihat adalah loader byte-source, hipotesis semantik tidak boleh dinaikkan dari kemungkinan menjadi fakta.

## EA4 — koreksi DYNAMIC untuk 0x8013EB0C

Census `DZ2_GLOBAL_8013EB0C_READ_WRITE_CENSUS.tsv` diperbarui pada dua store berikut:
- `0x800D46B8` — ekspresi tertulis `((tile+0x20)>>8 & 0xF)+1`.
- `0x800D47C8` — ekspresi tertulis `((tile+0x20)>>4 & 0xF)+1`.

Keduanya diklasifikasikan `DYNAMIC_FROM_TILE_PLUS20_NIBBLE`, bukan konstanta. Bukti straight-line:
- high: `0x800D46A4 lhu`, `0x800D46AC srl 8`, `0x800D46B0 andi 0xF`, `0x800D46B4 addiu 1`, `0x800D46B8 sw`.
- low: `0x800D47B4 lhu`, `0x800D47BC srl 4`, `0x800D47C0 andi 0xF`, `0x800D47C4 addiu 1`, `0x800D47C8 sw`.

Tidak ada branch/JAL/JALR di masing-masing span sumber-ke-store. Dua pasangan file_offset diverifikasi dengan aturan Entry 1 `0x10BB000+(PC-0x800AD450)`; instruction bytes 4-byte dan mnemonic cocok dengan decode census.

## Status Actions dan keterbatasan run

Satu run baru saja dijalankan: `42227045813`, job `dx0-dx4-static`, source SHA `56d1ba6a0ac7e874a3229a494e896336a38e7380`, status akhir **FAIL**, exit code 1, EA exit code 1. Penyebab teknis: helper supplemental mewarisi objek `entry` berjenis integer dari namespace analyzer lalu memanggil `len()`; skrip kompatibilitas diperbaiki di commit laporan ini. Step py_compile, pengunduhan/validasi input privat, eksekusi analyzer DZ, dan penghapusan input privat berhasil. Run menghasilkan file EA1 parsial saja sebelum TypeError; karena itu **EA_SELF_CHECK penuh tidak tersedia**. DZ self-check dari run lama tetap 5.175 rows / 0 failures.

Tidak ada emulator/game/BIOS/savestate yang dijalankan atau dipakai. Tidak ada ISO, binary, dump, video, atau frame dikomit. Semua output tambahan berupa teks/TSV.
