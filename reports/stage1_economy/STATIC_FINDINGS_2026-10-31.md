# Stage 1 — temuan statis ekonomi DATA.BIN Entry 1 (31 Oktober 2026)

## Kesimpulan eksekutif

Audit statis menemukan satu rumus numerik per-record dan satu jalur renderer yang menampilkan nilai negatif pada tile milik peserta lain. Ini belum membuktikan debit Chakra saat mendarat, kredit pendapatan bagi pemilik petak, atau waktu payout. Tidak ditemukan jalur lengkap untuk harga build/upgrade Barrier ataupun kredit akibat 結界開放. Semua alamat Entry 1 di bawah memakai **candidate import base 0x800AD450**; lokasi byte Entry 1 dan identitas datanya telah dicocokkan, tetapi pemetaan payload ke alamat RAM aktif belum dikonfirmasi saat runtime.

**Level maksimum temuan dokumen ini: K3.** Tidak ada K4 karena sumber event → handler → pembaruan saldo → perubahan record/pemilik belum ditutup.

## Identitas resource dan batas alamat

Audit direktori DATA.BIN:
- Entry 1 = directory index 1, LBN 8.778, panjang 596.412 byte, DATA.BIN offset `0x10BB000`.
- SHA-256 slice Entry 1: `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`.
- Baris direktori dan byte slice cocok; ini VERIFIKASI identitas resource.
- Import statis Entry 1 pada base `0x800AD450` adalah kandidat dari slot pointer global, **bukan** bukti bahwa semua fungsi di alamat tersebut sedang aktif di RAM saat gameplay.

Referensi repo: `reports/static_audit/LOADER_AND_DIRECTORY_INDEX_AUDIT_2026-10-31.md` (bagian pemetaan Entry 1 dan addendum helper). Artefak Ghidra teks dari Actions #41159805931 juga mencatat `runtime_mapping=NOT_VALIDATED`, `analysis_import_base=0x800AD450`, dan tidak menjalankan emulator/input/savestate.

## 1. Rumus numerik per-record — bukan otomatis income atau cost

### Pembaca

- Fungsi: `FUN_800B770C`, PC entry `0x800B770C`.
- Offset pada slice Entry 1 untuk import base tersebut: `0x800B770C - 0x800AD450 = 0xA2BC`.
- Record array pointer global: slot `DAT_8013EA84` (alamat slot kandidat `0x8013EA84`).
- Stride record: `0x124` byte; record = `DAT_8013EA84 + (index & 0xFF) * 0x124`.
- Field yang dibaca:
  - byte record `+0x0B`: switch/multiplier selector;
  - halfword record `+0x20`: bits 7–11 dipakai untuk memilih nilai dasar;
  - halfword record `+0x10` sampai `+0x2E`: 16 kemungkinan nilai dasar (index byte offset `(u16(record+0x20) >> 7) & 0x1E`).
- Table dispatch switch berada pada alamat kandidat `0x800AD5F4` (dibentuk dari `lui 0x800B; addiu -0x2A0C`). Ini jump table switch, bukan bukti tabel harga Barrier.

### Operasi yang didekode

| byte +0x0B | return dari nilai dasar B | operasi |
|---:|---:|---|
| 0 | B | 100% |
| 1 | floor(B × 12 / 10) | 120% |
| 2 | floor(B × 15 / 10) | 150% |
| 3 | floor(B × 18 / 10) | 180% |
| 4 | 2 × B | 200% |
| selain 0–4 | 0 | default |

Aritmetika ini didukung oleh dekompilasi/raw MIPS dalam artefak run #41159805931. Tetapi semantik byte +0x0B dan hubungan tiap indeks dengan level Barrier belum dipastikan. **TIDAK TAHU** apakah B adalah toll, rent, nilai dasar aset, atau skor penilaian. Tidak boleh mengubahnya menjadi biaya upgrade atau income hanya karena urutan multipliers tampak menyerupai level.

### Raw excerpt 48 byte pada PC 0x800B7730

```
800B7730  0B 00 43 90   lbu v1,0xb(v0)
800B7734  00 00 00 00   nop
800B7738  05 00 62 2C   sltiu v0,v1,0x5
800B773C  16 00 40 10   beq v0,zero,0x800b7798
800B7740  80 18 03 00   sll v1,v1,0x2
800B7744  0B 80 02 3C   lui v0,0x800b
800B7748  F4 D5 42 24   addiu v0,v0,-0x2a0c
800B774C  21 18 62 00   addu v1,v1,v0
800B7750  00 00 62 8C   lw v0,0x0(v1)
800B7754  00 00 00 00   nop
800B7758  08 00 40 00   jr v0
800B775C  00 00 00 00   nop
```

Raw excerpt pemilih nilai dasar (PC `0x800B7780`, 24 byte):

```
20 00 43 94  00 00 00 00  C2 19 03 00
1E 00 63 30  21 10 43 00  10 00 42 94
```

Dekode: `lhu v1,0x20(v0)`; shift right 7; mask `0x1E`; tambah ke pointer record; `lhu v0,0x10(v0)`. Tabel 16 halfword adalah bagian record yang ditunjuk melalui `DAT_8013EA84`; nilai runtime setiap entri tidak dapat diambil dari frame video dan belum disertakan sebagai snapshot RAM.

## 2. Agregat owned-record — jangan sebut income

- Fungsi: `FUN_800BDC4C`, PC entry `0x800BDC4C`; offset slice `0x107FC`.
- Pointer array: `DAT_8013EA84`; count: `DAT_8013EAC8` (slot alamat kandidat `0x8013EAC8`).
- Stride `0x124`.
- Filter record: byte `record+0 == 5` dan `(u16(record+0x20) >> 12) == selected_id`.
- Untuk tiap record yang lolos, panggil `FUN_800B770C(index & 0xFF)`, jumlahkan hasilnya, lalu return `trunc_toward_zero(sum / 2) + GET_0x80012A8C()`.
- Reader/aggregator ini membuktikan agregasi record menurut filter dan penambahan konfigurasi pada view statis. **TIDAK TAHU** arti status 5, nibble +0x20, nilai konfigurasi, dan apakah hasilnya saldo, estimasi aset, tampilan skor, atau syarat menang.

### Raw excerpt 28 byte pada PC 0x800BDCC4

```
00 00 62 90  09 00 53 14  20 00 62 94
02 13 02 00  04 00 22 16  C3 DD 02 0C
FF 00 04 32
```

Instruksi yang dicatat Ghidra:
- `0x800BDCC4 lbu v0,0x0(v1)`
- `0x800BDCCC bne v0,s3,0x800bdcf4` dengan `s3=5`
- `0x800BDCD4 lhu v0,0x20(v1)`
- `0x800BDCDC srl v0,v0,0xc`
- `0x800BDCE0 bne s1,v0,0x800bdcf4`
- `0x800BDCE8 jal 0x800B770C`; delay slot `andi a0,s0,0xff`
- `0x800BDD10 jal 0x80012A8C`; hasil agregat dibagi dua dengan pembulatan integer bertanda ke arah nol lalu ditambah return getter.

## 3. Fee/toll yang ditampilkan untuk tile peserta lain

- Fungsi renderer kandidat: `FUN_800FC700`, entry PC `0x800FC700`, offset slice `0x4F2B0`.
- Audit statis run #41159805931: renderer memeriksa record status byte `+0 == 5`, mengekstrak owner-like ID dari high nibble `u16(record+0x20) >> 12`, membandingkannya dengan selected participant, dan pada cabang peserta berbeda memanggil `FUN_800B770C(record_index)`.
- Nilai return dinegasikan sebelum dikirim ke drawing helper `0x8001B364`. Raw snippet drawing pada `0x800FC7D8`:
  `A0 00 84 24  78 00 A5 24  23 30 02 00  D9 6C 00 0C  05 00 07 24`
  (dekode termasuk `subu a2,zero,v0`, lalu `jal 0x8001B364`).
- Ini **K3 untuk jalur tampilan fee bertanda negatif pada record owner berbeda**, di bawah base kandidat. Itu tidak membuktikan saldo pemain benar-benar didebit, pemilik menerima kredit, atau saat kapan transaksi terjadi.

Per-caller census run #41160254539 menemukan 44 direct JAL ke `FUN_800B770C`; dalam body caller yang diperiksa tidak ada direct JAL ke setter `0x8001387C`, getter `0x800138EC`, atau target getter `0x80012A70`. Scanner itu tidak menutup JALR/indirect calls, direct store ke record peserta, atau jalur helper perantara. Maka ini **bukan** bukti bahwa tidak ada transaksi; hanya belum ditemukan call chain debit/kredit.

## 4. Pencarian harga 60, 150, 580 dan 1000

Scan immediate statis pada run #41156493284 menemukan 237 kecocokan `0x3C` (60), 12 kecocokan `0x96` (150), satu `0x244` (580), dan 56 `0x3E8` (1000). Pemeriksaan konteks:
- 60: mayoritas displacement/offset; satu `li a1,0x3C` pada candidate `0x800D96D4` tidak ditautkan ke ESTATE atau transaksi Chakra.
- 150: semua 12 contoh yang diekspor adalah load/store offset `+0x96`, bukan scalar harga 150.
- 580: satu kecocokan `sh v0,0x244(v1)` menunjukkan displacement/field offset, bukan immediate 580 sebagai harga.
- 1000: mayoritas akses/offset; kandidat scalar yang terlihat tidak punya rantai ke Barrier.

Jadi jangkar 60/150 tidak teridentifikasi sebagai konstanta harga pada instruksi; nilai 580 tidak menjadi pendapatan/kredit kode hanya karena angka itu sama dengan tampilan toll yang dilaporkan video.

## 5. Pending Chakra delta, LVUP_ESTATE, KABE, dan release

### Offset yang tidak boleh dicampur

- **+0xB44 — field manager/state yang diterapkan bertahap ke Chakra.** Artefak lama #41155800069 hanya mengekspor reset pada candidate PC 0x80109A54 dan renderer read pada 0x80109F64, sehingga saat itu sumber nonzero belum diketahui. Run #41166812039 menambahkan konteks FUN_80109FEC: B40 disalin ke B44 pada PC 0x8010A5C8; getter Chakra 0x800138EC dipanggil di PC 0x8010A144; B44 dibaca pada 0x8010A154; setter Chakra 0x8001387C dipanggil pada 0x8010A15C dengan Chakra lama + B44 dibentuk di delay slot 0x8010A160. B44 kemudian dikurangi bertahap pada 0x8010A648–0x8010A658. Ini **K3 untuk jalur penerapan nilai penyesuaian Chakra**, bukan bukti jenis event.
- B40 adalah field berbeda: reset FUN_80109994 membentuk B40 = B30 + B38 pada candidate PC 0x80109A84–0x80109A94; reset juga mengosongkan B44 pada 0x80109A54. Penulis B30/B38 dan sumber event-nya belum ditemukan. Karena itu B44 belum boleh dilabeli sebagai income, toll, refund, build/upgrade cost, atau hasil KABE/結界開放.
- **+0x2EE — field participant-array yang terpisah.** FUN_800E1188 membaca halfword per peserta dari DAT_8013EA74 + 0x2EE + participant*2; candidate PC 0x800BE5D8. Jalur memproses angka positif/negatif dan memanggil setter Chakra 0x8001387C di 0x800BEC98, getter 0x800138EC di 0x800BECA0, lalu clear di 0x800BEDA4. Ini K3 parsial; writer nonzero/source event belum ditemukan, dan decompiler memberi warning Control flow encountered bad instruction data.
- Array peserta candidate memakai pointer slot 0x8013EA74, stride 0x90, nilai Chakra di field +0x04. Jangan samakan struktur ini dengan record tile stride 0x124.
- Global 0x8013EBB0 masih sekadar candidate pending-fee/selection value; label skrip bukan bukti semantik.
- Run #41166812039 memindai 24 akses langsung +0x2EE (3 load/19 store/2 other) dan 14 akses langsung +0xB44 (8 load/4 store/2 other). Ringkasan status/job/input SHA/exit code ada di reports/actions/run_41166812039_summary.txt.
- Tidak ada handler KABE/結界開放 yang berhasil dihubungkan ke B30/B38, perubahan saldo, dan mutasi owner/level record. Status Q3 tetap UNKNOWN.

### Resource labels / release

- Literal `ESTATE`, `LVUP_ESTATE`, dan `KABE` muncul pada awal slice Entry 1 (offset masing-masing yang dicatat audit: `0x14/0x2D`, `0x28`, dan `0x58`).
- String ini adalah petunjuk resource; belum menjadi dispatch handler atau fungsi yang bisa dinamai sebagai build, upgrade, atau release.
- Tidak ada handler `結界開放` yang berhasil dipasangkan dengan perubahan saldo dan mutasi owner/level record.
- Tidak ada tabel harga L1–L5 yang ditemukan, dan tidak ada jalur `LVUP_ESTATE → sumber harga → pemeriksaan saldo → setter Chakra → perubahan level` yang tertutup.

## Matriks jawaban statis

| Q | Hasil statis | Level |
|---|---|---|
| Q1 pendapatan petak | Ada formula nilai record `FUN_800B770C`, agregator owner-filter `FUN_800BDC4C`, serta renderer fee negatif `FUN_800FC700`; waktu income dan kredit ke owner tidak ditemukan. | **SEBAGIAN K3** untuk formula per-record/tampilan; income **UNKNOWN** |
| Q2 build/upgrade L1–L5 | Tidak ada scalar/table atau transaksi LVUP_ESTATE/build yang ditautkan ke angka ledger. | **BELUM K3** untuk harga; **UNKNOWN** |
| Q3 Chakra dari 結界開放 | Handler release dan sumber nilai yang mengubah saldo tidak teridentifikasi. +0xB44 dan +0x2EE tetap field kandidat terpisah. | **UNKNOWN** |

## Run statis yang menjadi provenance

- Run #41159510198, job 124413702244, input SHA `934c735a39b7ccc2f650e685d78e0aa91c407840`, completed/success, exit 0; artefak teks 13026796167.
- Run #41159805931, job 124414633147, input SHA `20346f89463bb1ca8792317de1496e228470ebf8`, completed/success, exit 0; artefak teks 13026831655; raw excerpt di atas diambil dari artefak ini.
- Run #41160254539, job 124416042420, input SHA `1b3ee51115342e1d484a019866f0a681067a3639`, completed/success, exit 0; artefak teks 13025909960; direct-caller census.
- Run #41166812039, job 124436038028, input SHA ad1dd4d9c7a05458cda20c1000e83c154bb3e73c, completed/success, exit code 0; artifact 13028438888. Ringkasan teks disimpan pada reports/actions/run_41166812039_summary.txt.
- Semua run di bagian ini adalah analisis statis. Tidak ada emulator/gameplay input/savestate restore; private disc/slice dan proyek Ghidra dibersihkan.

## Langkah statis berikutnya yang dibutuhkan

1. Dapatkan output Ghidra dari penambahan PC callback/pending-writer pada HEAD `d0ef96970724c85d8bcd2c5c7fb8ba58bac04072`, lalu cari caller level atas dan indirect calls/direct stores.
2. Tutup hubungan event landing → pending delta → payer balance mutation untuk memisahkan toll dari income owner.
3. Temukan writer record pada `+0`, `+0x0B`, `+0x20`, dan struktur Barrier; telusuri sumber harga untuk build dan tiap upgrade.
4. Temukan dispatch/handler KABE atau 結界開放 yang benar, lalu buktikan pemilihan Barrier, nilai saldo, dan field yang ditulis.

## Rancangan uji runtime nanti (tidak dijalankan sekarang)

Hanya setelah mapping loader/runtime dan fail-closed gate mengizinkan:
- Snapshot sebelum/sesudah satu aksi, tanpa mengubah checkpoint induk.
- Pantau pointer record `0x8013EA84`, count `0x8013EAC8`, global kandidat pending `0x8013EBB0`, setiap record pada stride `0x124` (field `+0`, `+0x0B`, `+0x10..+0x2E`, `+0x20`), nilai peserta melalui accessor yang telah divalidasi, serta objek pending yang field candidate-nya `+0x2EE` atau `+0xB44`. Semua alamat harus dipetakan ulang dari loader sebelum breakpoint; jangan menganggap import base statis sebagai alamat runtime.
- Q1: satu pemain dengan daftar record milik yang diketahui menyelesaikan satu lap; ambil saldo dan record tepat sebelum/sesudah titik transisi lap, lalu ulangi tiga kali. Pisahkan landing pada petak lawan dari akhir lap.
- Q2: pada save/checkpoint yang sama, bangun satu tile netral; lalu uji setiap transisi L1→L2→L3→L4→L5 satu per satu. Catat biaya UI dan delta accessor serta field level record. Untuk menguji ketergantungan tile, ulangi pada sedikitnya dua tile lain tanpa mengubah kondisi lain.
- Q3: amati titik masuk release tanpa input lebih dulu; catat saldo, record yang berubah, dan pending delta. Bila UI menunggu pilihan, lakukan satu input pilihan saja dan capture lagi. Perlu sedikitnya tiga release record terukur untuk menguji rumus; jangan memicu release sampai gate runtime disetujui.

Tidak ada uji runtime dilakukan dalam sesi ini. Semua WAIT/UNKNOWN/NO-GO yang sudah ada tetap tidak berubah.


## Addendum — pending fields +0xB44 vs +0x2EE (31 Oktober 2026)

**Rebasing alamat:** artefak lama #41155800069/#41156493284 mengimpor slice Entry 1 pada candidate base `0x800D0000`. Candidate base yang lebih baru adalah `0x800AD450`. PC di bawah yang disebut “candidate PC” dihitung dengan mempertahankan offset byte terhadap awal slice; ini bukan pembuktian alamat runtime.

### Field manager +0xB44 — penyesuaian Chakra bertahap; sumber event UNKNOWN

Run #41166812039 mengoreksi batas temuan artefak lama: +0xB44 tidak hanya dibaca renderer. FUN_80109FEC menyalin +0xB40 ke +0xB44 pada PC 0x8010A5C8, lalu menggunakan B44 untuk menambah Chakra lewat getter 0x800138EC dan setter 0x8001387C (PC 0x8010A144–0x8010A160). Nilai B44 dikurangi bertahap setelah diterapkan.

- Object/state candidate dirujuk melalui slot 0x8013A554. FUN_80109994 mengosongkan B44 di PC 0x80109A54.
- Pada reset yang sama, B40 = B30 + B38 di PC 0x80109A84–0x80109A94. B40 dan B44 adalah field terpisah.
- FUN_80109FEC menambah B44 sebesar 0x14 (20 desimal) pada PC 0x8010A590–0x8010A59C; ketika tahap transfer dimulai, B40 disalin ke B44 pada PC 0x8010A5C8 dan status byte +0xB2A menjadi 7.
- PC 0x8010A144 memanggil getter Chakra 0x800138EC; PC 0x8010A154 memuat B44; PC 0x8010A15C memanggil setter 0x8001387C dengan delay-slot addu a1,v0,a1 di PC 0x8010A160. Dengan demikian setter menerima Chakra lama + B44.
- Jalur bertahap kembali memakai setter 0x8001387C pada PC 0x8010A638 dan mengurangi B44 di PC 0x8010A648–0x8010A658. Renderer FUN_80109F1C juga membaca B44 di PC 0x80109F64 untuk menampilkan angka.
- Ini membuktikan K3 bahwa B44 adalah nilai penyesuaian Chakra yang diterapkan bertahap dan ditampilkan. Namun penulis/sumber B30 dan B38 serta pemicu event belum ditemukan. Tidak ada bukti yang mengikatnya secara khusus ke toll, income, LVUP_ESTATE, atau KABE/結界開放. Q1 dan Q3 tidak menjadi tuntas.

Raw excerpt 20 byte pembentukan B40 dari B30+B38 (candidate PC 0x80109A84–0x80109A94):

```
30 0B 82 8C  38 0B 83 8C  00 00 00 00
21 10 43 00  40 0B 82 AC
```

Raw excerpt 32 byte jalur getter → B44 → setter Chakra (candidate PC 0x8010A144–0x8010A160):

```
3B 4E 00 0C  00 00 00 00  54 A5 23 8E  00 00 00 00
44 0B 65 8C  2B 0B 64 90  1F 4E 00 0C  21 28 45 00
```

Raw excerpt 32 byte loop progress B44 dan step 20 (candidate PC 0x8010A584–0x8010A5A0):

```
14 80 02 3C  54 A5 43 8C  00 00 00 00  44 0B 62 8C
00 00 00 00  14 00 42 24  44 0B 62 AC
```

Scan operand langsung run #41166812039: +0xB44 = 14 akses (8 load, 4 store, 2 other). Scan tekstual ini tidak menjamin semua akses melalui pointer hasil kalkulasi/alias.

### Field participant +0x2EE — consumer delta per peserta lebih konkret

- Array peserta memakai pointer slot candidate `0x8013EA74`; consumer memakai struktur peserta ber-stride `0x90`, dan membaca halfword `base + 0x2EE + participant*2`.
- Fungsi lama `FUN_800E1188` direbase ke candidate PC `0x800BE5D8`. Ia berjalan pada cabang feature flag `GET_0x80012AD0() & 0x1000`, menyalin nilai antar-peserta yang byte team-code `+0x0E`-nya sama, lalu memproses nilai sebagai animasi angka positif/negatif.
- Pada candidate PC `0x800BEC98` (PC lama `0x800E1848`), fungsi memanggil setter Chakra `0x8001387C` dengan field peserta `+0x04`; lalu memanggil getter `0x800138EC` pada candidate PC `0x800BECA0` dan menyalin hasil getter kembali ke field peserta `+0x04`.
- Setelah alur animasi selesai, field `+0x2EE` dikosongkan pada candidate PC `0x800BEDA4` (PC lama `0x800E1954`). Setup juga mengosongkan slot ini pada candidate PC `0x800B2EEC` (PC lama `0x800D5A9C`).
- Ini mendukung **K3 untuk pemrosesan/animasi nilai delta per peserta yang tersambung ke accessor Chakra**. Namun, penulis nonzero/sumber nilai +0x2EE belum ditemukan; belum ada koneksi yang terbukti dari nilai ini ke toll, income, build/upgrade, atau 結界開放.

Raw excerpt **28 byte** untuk pembentukan dan pembacaan alamat +0x2EE pada PC lama `0x800E11C8`–`0x800E11E4` (candidate PC `0x800BE618`–`0x800BE634`):

```
74 EA 42 8C  00 00 00 00  EE 02 49 24
21 10 2A 02  00 00 42 90  00 00 00 00
22 00 40 14
```

Raw excerpt **20 byte** untuk sinkronisasi Chakra pada PC lama `0x800E1844`–`0x800E1858` (candidate PC `0x800BEC94`–`0x800BECA8`):

```
04 00 45 8C  1F 4E 00 0C  21 20 20 02
3B 4E 00 0C  21 20 20 02
```

Raw excerpt **20 byte** untuk clear +0x2EE pada PC lama `0x800E1948`–`0x800E1958` (candidate PC `0x800BED98`–`0x800BEDA8`):

```
74 EA 42 8E  40 18 11 00  21 10 43 00
EE 02 40 A4  21 10 35 02
```

**Batas:** fungsi `FUN_800E1188` memuat warning Ghidra `Control flow encountered bad instruction data` pada dekompilasi dan fungsi ini berasal dari import view lama yang direbase berdasarkan offset slice. Perlakukan sebagai jalur statis parsial. Run #41166812039 mengaudit ulang candidate base 0x800AD450: +0x2EE memiliki 24 akses langsung (3 load, 19 store, 2 other). Candidate FUN_800E1188/PC 0x800BE5D8 memiliki warning Ghidra Control flow encountered bad instruction data; klasifikasi tetap K3 parsial, bukan K4. Ringkasan ada di reports/actions/run_41166812039_summary.txt.


## Addendum run #41166812039 — jalur penyesuaian Chakra +0xB44

Hasil Ghidra pada candidate import base 0x800AD450 memperbaiki kesimpulan artefak terdahulu: +0xB44 bukan hanya field tampilan. FUN_80109FEC menyalin +0xB40 ke +0xB44 pada PC 0x8010A5C8, lalu menggunakan B44 untuk menambah Chakra melalui getter 0x800138EC dan setter 0x8001387C (PC 0x8010A144–0x8010A160). Nilai B44 diproses bertahap: maksimum step 0x14 (20) pada PC 0x8010A590–0x8010A59C; getter/setter dipanggil kembali pada PC 0x8010A624–0x8010A638; B44 dikurangi pada PC 0x8010A648–0x8010A658. FUN_80109F1C juga membaca B44 untuk ditampilkan di PC 0x80109F64.

B40 dibentuk dari B30+B38 di FUN_80109994 pada PC 0x80109A84–0x80109A94. Reset mengosongkan B44 pada PC 0x80109A54. Ini membuktikan **K3 untuk field penyesuaian Chakra bertahap**, tetapi makna dan penulis sumber B30/B38 belum teridentifikasi; hubungan dengan toll, income, LVUP_ESTATE, atau handler KABE/結界開放 tetap TIDAK TAHU. Q1/Q3 tidak dinaikkan statusnya.

Raw excerpt 20 byte B30+B38→B40:
```
30 0B 82 8C  38 0B 83 8C  00 00 00 00
21 10 43 00  40 0B 82 AC
```

Raw excerpt 32 byte getter→B44→setter Chakra:
```
3B 4E 00 0C  00 00 00 00  54 A5 23 8E  00 00 00 00
44 0B 65 8C  2B 0B 64 90  1F 4E 00 0C  21 28 45 00
```

Raw excerpt 32 byte loop bertahap:
```
14 80 02 3C  54 A5 43 8C  00 00 00 00  44 0B 62 8C
00 00 00 00  14 00 42 24  44 0B 62 AC
```

Run #41166812039 menemukan 14 operand langsung B44 (8 load, 4 store, 2 other) dan 24 operand langsung +0x2EE (3 load, 19 store, 2 other). +0x2EE adalah field array peserta berbeda (base slot 0x8013EA74, stride 0x90); consumer candidate FUN_800E1188/PC 0x800BE5D8 mengakses Chakra setter/getter, tetapi mempunyai warning decompiler. Kedua field tak boleh digabung. Candidate base bukan runtime mapping yang tervalidasi.
