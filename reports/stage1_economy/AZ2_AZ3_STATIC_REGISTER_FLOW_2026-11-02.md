# AZ2–AZ3 — audit statis manager dan setter biaya
Tanggal: 2 November 2026
Target: SLPS-03553 / DATA.BIN Entry 1
Bukti instruksi MIPS / p-code statis. Maksimum K4; bukan hasil gameplay.
Input Entry 1: 596,412 byte; file offset 0x10BB000; SHA-256 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a. Base 0x800AD450 adalah kandidat impor statis, bukan pemetaan runtime tervalidasi.

## AZ2 — pembaca manager +0xB38 / +0xB40 / +0xB44

Pemindaian penuh DATA.BIN Entry 1 pada run `41360300335` mengekspor seluruh instruksi yang memakai displacement +0xB38, +0xB40, dan +0xB44, dengan 12 instruksi sebelumnya untuk tiap akses. Setelah review base register dan rantai pemuatan pointer global manager `[0x8013A554]`, seluruh **17 load langsung** berikut terkonfirmasi sebagai reader manager. Hasil konsolidasi 25 akses (read/write) dan bukti base register per PC ada di:
`reports/stage1_economy/AZ2_ENTRY1_FIELD_ACCESS_CENSUS_2026-11-02.tsv`.

Ringkasan pemindaian Entry 1:

| Field | Total akses langsung | Reader | Writer |
|---|---:|---:|---:|
| +0xB38 | 6 | 5 | 1 |
| +0xB40 | 5 | 4 | 1 |
| +0xB44 | 14 | 8 | 6 |
| **Jumlah** | **25** | **17** | **8** |

Reader yang terkonfirmasi:

| Field | PC | Fungsi | Effective base | Bukti pointer manager sebelumnya |
|---|---:|---|---|---:|
| +0xB38 | 0x80109A88 | FUN_80109994 | a0 | 0x80109A78 |
| +0xB38 | 0x8010A0E0 | FUN_80109FEC | v0 | 0x8010A0CC |
| +0xB38 | 0x8010A460 | FUN_80109FEC | v1 | 0x8010A454 |
| +0xB38 | 0x8010A4D8 | FUN_80109FEC | v1 | 0x8010A4C0 |
| +0xB38 | 0x8010A4F8 | FUN_80109FEC | v0 | 0x8010A4F0 |
| +0xB40 | 0x8010A0EC | FUN_80109FEC | v0 | 0x8010A0CC |
| +0xB40 | 0x8010A528 | FUN_80109FEC | v1 | 0x8010A51C |
| +0xB40 | 0x8010A5A0 | FUN_80109FEC | v1 | 0x8010A588 |
| +0xB40 | 0x8010A5C0 | FUN_80109FEC | v0 | 0x8010A5B8 |
| +0xB44 | 0x80109F64 | FUN_80109F1C | v1 | 0x80109F34 |
| +0xB44 | 0x8010A154 | FUN_80109FEC | v1 | 0x8010A14C |
| +0xB44 | 0x8010A524 | FUN_80109FEC | v1 | 0x8010A51C |
| +0xB44 | 0x8010A590 | FUN_80109FEC | v1 | 0x8010A588 |
| +0xB44 | 0x8010A5EC | FUN_80109FEC | v0 | 0x8010A5E4 |
| +0xB44 | 0x8010A610 | FUN_80109FEC | v0 | 0x8010A608 |
| +0xB44 | 0x8010A648 | FUN_80109FEC | v1 | 0x8010A640 |
| +0xB44 | 0x8010A6A8 | FUN_80109FEC | v1 | 0x8010A6A0 |

Untuk setiap PC di atas, 12 instruksi sebelumnya, byte instruction, instruksi load pointer manager, dan register efektif tercatat pada TSV. Tiga displacement tersebut muncul pada empat function entry manager yang terdeteksi: `FUN_80109974`, `FUN_80109994`, `FUN_80109F1C`, dan `FUN_80109FEC`. Ini merupakan census seluruh **direct displacement access** di Entry 1, lebih luas dari AQ1 awal yang mengekspor tiga badan fungsi.

**Batas yang tetap berlaku:** operasi yang menghitung alamat field terlebih dahulu lalu mengakses offset 0, pointer yang didapat lewat struktur lain, atau indirect JALR tidak dapat dipastikan hanya dari displacement scan. Pembaca tak langsung semacam itu tetap **TIDAK TAHU**; tidak ada kesimpulan dari nol hit yang tidak diuji.
### Ekspresi a1 saat setter 0x8001387C dipanggil dari FUN_80109FEC

| Setter PC | Instruksi pembentuk argumen akhir | Ekspresi a1 |
|---|---|---|
| 0x8010A15C | A160 addu a1,v0,a1 | Q(i)+B44 |
| 0x8010A1B0 | A1B4 move a1,v0 | Q(i) |
| 0x8010A638 | A63C addu a1,v0,s1 | Q(i)+min(B44,0x14) |
| 0x8010A97C | A980 move a1,v0 | Q(i) |

Q(i) adalah getter 0x800138EC untuk indeks i=ZEXT8[manager+0xB2B]; getter/setter mengakses participant +0x18. Empat site ini adalah salinan/penambahan, bukan pengurangan harga.

### Pemicu transfer menurut instruksi, bukan label gameplay

FUN_80109FEC membaca flag caller di param_1+0xC dan menguji bit 0x20 pada PC A078–A080. Jika bit tersebut tidak ada, cabang menuju A204 melewati pemrosesan manager. Jika ada, state byte manager +0xB2A mengatur fase. State 3–6 memindahkan target B30/B38/B40 melalui progress B34/B3C/B44. State 6 menaikkan B44 sebesar 0x14 hingga target B40; pada terminal state 6, B40 disalin ke B44 dan state menjadi 7. Jalur state 7 memanggil getter/setter agar nilai Q(i)+B44 atau Q(i)+min(B44,20) ditulis ke participant +0x18; B44 kemudian dikuras dengan mengurangi langkah yang sama.

**Kesimpulan mekanis K4:** kondisi kode untuk jalur transfer ke participant +0x18 adalah caller flag bit 0x20 dan state manager 7, setelah progress state 6 mengisi B44 menuju B40.
**Nama pemicu gameplay = TIDAK TAHU.** Kode yang diekspor tidak memberi bukti bahwa event tersebut adalah akhir putaran, settlement, atau Barrier release. Producer bit 0x20 dan asal semantik B30/B38 juga belum terbukti. Maka tidak ada satu dari tiga nama event itu yang dipilih.

## AZ3 — census direct caller setter saldo dan pemeriksaan argumen biaya

Run Step7 `41367221886` (job `125029837518`, source SHA `e98a2081e7f6573a75705d416f8a727a10634ced`, exit code 0) memindai seluruh aligned MIPS words pada kedua image dengan raw-JAL decode dan validasi direct-flow Ghidra:

| Image | raw JAL candidate | Ghidra direct-flow validated |
|---|---:|---:|
| DATA.BIN Entry 1 (596,412 B) | 14 | 14 |
| MAIN_EXE SLPS_035.53 | 2 | 2 |
| **Total** | **16** | **16** |

Daftar penuh PC, instruksi sebelumnya, delay slot, a0/a1 expression, dan source classification diperbarui pada:
`reports/stage1_economy/AZ3_SETTER_GETTER_MINUS_COST_CANDIDATES_2026-11-02.tsv`.

Callsite MAIN_EXE tambahan yang sebelumnya tidak ada pada AX2:
- `0x80012DD4` di FUN_80012C70; raw bytes `1F 4E 00 0C`; Ghidra direct flow validated. Decompile penuh `FUN_80012C70` membuktikan `uVar4=FUN_80012A44(); FUN_8001387c(uVar7,uVar4);`; raw delay slot `0x80012DD8 move a1,v0`, dengan `a0=s3` = indeks pemain loop `uVar7`. Tidak ada pengurangan lokal pada caller; isi/arti return `FUN_80012A44` masih menunggu decompile callee.
- `0x80013170` di FUN_80012EAC; raw bytes `1F 4E 00 0C`; a1 berasal dari `u32(selected_table_row+0x04)`, a0 berasal dari indeks participant loop. Ini pengisian table-row, bukan Q(i)-cost.

Pada 14 callsite Entry1, sepuluh callsite awal menulis nilai participant/field/slot tanpa ekspresi Q-minus. Empat site FUN_80109FEC menghasilkan Q+B44, Q, Q+min(B44,0x14), dan Q. Tidak ada pola `a1=Q(i)-cost` yang terbukti di 14 site tersebut. Dari dua MAIN_EXE callsite, site 0x80013170 adalah nilai tabel row+0x04; site 0x80012DD4 mengirim hasil fungsi 0x80012A44 dan masih menunggu decompile penuh.

**Hasil debit biaya: TIDAK TAHU.** Census direct-JAL lengkap untuk dua image yang dianalisis, tetapi indirect JALR/computed-target calls, caller pada resource/overlay lain, dan producer nilai 0x80012A44 belum dibuktikan. Tidak ditemukan ekspresi getter-minus-cost dalam 16 direct-JAL callsites yang sudah diuji. Ini bukan bukti bahwa semua biaya build/upgrade tidak ada atau tidak pernah didebit lewat jalur lain. Jangan mengarang rumus atau nama event.

**Status AZ3: SEBAGIAN (direct census selesai; semantic cost incomplete).**
## Hipotesis dan falsifier

### AZ2
- H1: bit caller 0x20 bersama state 7 mengendalikan transfer nilai B44 ke participant +0x18. Falsifier: xref producer bit 0x20 menunjukkan flag itu tidak terkait dengan jalur transfer atau penelusuran register menunjukkan nilai setter tidak mengubah participant +0x18.
- H2: state 7 adalah penyelesaian Barrier-release dan B44 adalah nilai yang dirilis. Falsifier: producer B30/B38 atau asal flag 0x20 terbukti terkait aksi lain, atau runtime original-code pada event Barrier release tidak mengikuti state 6→7.

### AZ3
- H1: harga build/upgrade dikalkulasi sebagai Q(i)-cost dan ditulis lewat setter 0x8001387C. Falsifier: caller + indirect call census lengkap menunjukkan pembelian tidak pernah menurunkan saldo melalui setter tersebut.
- H2: harga berasal dari tabel/field lain atau jalur debit terpisah. Falsifier: bukti producer/consumer original-code mengikat seluruh pembelian ke pola Q(i)-cost dan meniadakan sumber alternatif.

Confidence register/control-flow statis K4. Identitas event, unit B30/B38/B40/B44, cost build/upgrade, dan cakupan indirect reader/caller di luar ekspor: TIDAK TAHU. Nol hit tidak dipakai sebagai kesimpulan.
