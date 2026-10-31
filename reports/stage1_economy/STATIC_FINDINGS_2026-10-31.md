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

### Raw excerpt 36 byte pada PC 0x800B7730

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

- `+0xB44`: artefak run #41155800069 (Entry 1 pada import-base lama `0x800D0000`) menunjukkan `FUN_8012C544` menginisialisasi field ini menjadi nol pada PC lama `0x8012C604`; `FUN_8012CACC` membaca `+0xB44` pada PC lama `0x8012CB14` untuk menggambar angka jika state byte `+0xB2A > 5`; `FUN_8012C78C` juga menggambarnya pada fase yang sama. Dalam cakupan output itu **tidak ditemukan penulis nonzero**. Jadi nama “pending Chakra delta” untuk +0xB44 belum terbukti; bukti langsung yang ada adalah reset dan pembacaan UI. `+0xB40` secara terpisah diinisialisasi sebagai `+0xB30 + +0xB38` pada PC lama `0x8012C644`; jangan satukan field B40 dan B44 sebagai satu transaksi.
  - Rebase berdasarkan file offset yang sama dari base lama `0x800D0000` ke candidate base `0x800AD450` memberi PC kandidat: reset routine `0x80109994`, store-zero `0x80109A54`, reader functions `0x80109BDC` dan `0x80109F1C`, serta load `0x80109F64`. Raw bytes tidak berubah karena yang bergeser hanya alamat import. Runtime mapping tetap belum tervalidasi.
- `+0x2EE`: ini offset participant-array yang berbeda dan memiliki konsumen lebih konkret. Dalam import-base lama, `FUN_800E1188` membaca halfword per peserta pada `DAT_8013EA74 + 0x2EE + participant*2`; dengan base candidate baru fungsi itu berada pada PC `0x800BE5D8`. Fungsi menyalin nilai antar-peserta yang team-code `+0x0E)-nya sama pada kondisi flag `0x1000), memformat nilai positif/negatif untuk animasi, memanggil setter Chakra `0x8001387C` pada PC kandidat `0x800BEC98`, membaca balik melalui getter `0x800138EC` pada `0x800BECA0`, dan akhirnya mengosongkan field pada PC kandidat `0x800BEDA4`. Setup juga mengosongkan slot `+0x2EE) pada PC kandidat `0x800B2EEC`. Ini mendukung **K3 untuk jalur pemrosesan/animasi delta per peserta**, tetapi sumber penulis nonzero belum ditemukan; belum ada link ke toll, income, build/upgrade, atau release.
- Global pointer slot `0x8013EA74` mengarah ke array peserta candidate; struktur peserta yang dibaca fungsi ini ber-stride `0x90` dan nilai Chakra berada pada field `+0x04` dalam jalur tersebut. Jangan samakan stride `0x90` ini dengan record tile stride `0x124`.
- Global `0x8013EBB0` diberi komentar `candidate pending fee value` oleh skrip; label itu masih hipotesis, bukan bukti bahwa nilainya pending income atau refund.
- HEAD workflow `d0ef969...` menambahkan target rebased `0x800BE5D8`, `0x80109994`, dan `0x80109F1C` di antara PC lain untuk analisis toll callback/pending writers. Pada waktu update ini, belum ada hasil workflow baru yang dikomit untuk menutup sumber delta +0x2EE atau menghubungkan +0xB44 dengan transaksi; status Q terkait tetap UNKNOWN.

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
- Tidak ada emulator, gameplay input, atau savestate restore dalam run-run tersebut.
- Tidak ada workflow baru yang dijalankan untuk tugas ini; tidak ada ringkasan run baru yang perlu diklaim.

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


## Addendum — raw MIPS untuk B44 dan participant delta +2EE (31 Oktober 2026)

Raw excerpt 24 byte pada PC lama `0x8012C5E8`–`0x8012C604` (candidate PC setelah rebase: `0x80109938`–`0x80109954`):

```
48 0B 40 A4  2D 0B 40 A0  54 A5 02 8E  44 0B 40 AC
```

Raw excerpt 32 byte sekitar PC lama `0x8012C634`–`0x8012C644` (candidate PC `0x80109984`–`0x80109994`):

```
30 0B 82 8C  38 0B 83 8C  00 00 00 00  21 10 43 00
40 0B 82 AC
```

Instruksi mengosongkan `+0xB44) ada pada `0x8012C604` (`sw zero,0xB44(v0)`); instruksi menjumlahkan B30+B38 dan menyimpan ke B40 ada pada `0x8012C644`. Fungsi UI membaca B44 melalui `lw a2,0xB44(v1)` di `0x8012CB14`.

Raw excerpt 32 byte pembaca delta per-peserta (PC lama `0x800E11C8)–`0x800E11E4`; setelah rebase Entry 1 candidate PC menjadi `0x800BE610)–`0x800BE62C`:

```
74 EA 42 8C  00 00 00 00  EE 02 49 24  21 10 2A 02
00 00 42 90  00 00 00 00  22 00 40 14
```

Ini memuat pengambilan pointer peserta, pembentukan alamat offset `+0x2EE), dan pemeriksaan slot. Raw excerpt update Chakra 20 byte pada PC lama `0x800E1844)–`0x800E1858` (candidate PC `0x800BEC94)–`0x800BECA8`):

```
04 00 45 8C  1F 4E 00 0C  21 20 20 02  3B 4E 00 0C
21 20 20 02
```

Ini menunjukkan field Chakra +4 diberikan ke setter `0x8001387C), kemudian nilai dibaca kembali melalui `0x800138EC). Raw bytes pada PC lama `0x800E1954) (`EE 02 40 A4`) menunjukkan slot delta +2EE dihapus setelah tahapan animasi; candidate PC `0x800BEDA4`.

Catatan: import-base lama dan baru adalah dua alamat virtual untuk slice Entry 1 yang sama; rebasing menggunakan offset file, bukan klaim pemetaan runtime. Artefak #41155800069/#41156493284 dekompilasi juga memperingatkan boundary Ghidra dan beberapa blok control flow yang tidak bersih. Gunakan instruksi di atas sebagai bukti statis parsial, bukan definisi lengkap semantic state.
