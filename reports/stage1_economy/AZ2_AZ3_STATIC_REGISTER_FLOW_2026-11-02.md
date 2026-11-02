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

## AZ3 — census direct caller setter saldo dan sumber nilai awal participant

Run Step7 `41367221886` memindai seluruh aligned MIPS words pada Entry1 dan MAIN_EXE. Direct JAL ke setter 0x8001387C tervalidasi:

| Image | raw JAL candidate | Ghidra direct-flow validated |
|---|---:|---:|
| DATA.BIN Entry 1 (596,412 B) | 14 | 14 |
| MAIN_EXE SLPS_035.53 | 2 | 2 |
| **Total** | **16** | **16** |

Daftar PC, ekspresi argumen, source classification dan instruksi sebelumnya berada pada `AZ3_SETTER_GETTER_MINUS_COST_CANDIDATES_2026-11-02.tsv`.

### Setter/getter participant +0x18

`FUN_8001387C(i,value)` memvalidasi `i<4`, membatasi value ke rentang -9999..99999, lalu menulis ke `0x80070EA0 + i*0xB4 + 0x18`. Getter `FUN_800138EC(i)` membaca field yang sama (atau 0 untuk indeks tidak valid). Field +0x18 teridentifikasi sebagai chakra pada record pemain; kode yang diuji menunjukkan setter/getter mentahnya.

### Sumber nilai awal dari global 0x80070C80

Decompile run `41367906993` mengungkapkan bahwa callsite MAIN_EXE `0x80012DD4` bukan debit biaya. Alirannya:
- `FUN_80012A44` pada PC `0x80012A48` hanya membaca `MEM32[0x80070C80]` dan mengembalikannya.
- `FUN_80012C70` menjalankan loop `uVar7` atas pemain, memanggil `FUN_80012A44()`, lalu memanggil `FUN_8001387C(uVar7,uVar4)`. Jadi nilai dari global C80 diinisialisasikan ke field participant +0x18.
- `FUN_8001387C` hanya melakukan validasi index, clamp dan store; tidak ada pengurangan saldo atau biaya pada fungsi ini.

Run Step7 `41368276256` (job `125033025512`, source SHA `5822e40f3698e1b928619ee74ec4cef5a4913f70`, exit code 0) kemudian menemukan dua writer langsung ke global C80:
- `FUN_80012780`, PC `0x800127D0`, `sw v0,0xc80(s2)`; base s2 dibentuk oleh `lui s2,0x8007`. Nilainya datang dari `MEM32[0x8006491C + (param_1 & 0xFF)*0x30]`.
- `FUN_80012EAC`, PC `0x80012F64`, `sw v0,0xc80(s0)`; base s0 berasal dari `lui s0,0x8007`. Nilainya datang dari `MEM32[0x8005779C + idx*0x54]`, dengan idx mode/state yang sama seperti tabel B30.

Jadi global C80 adalah **sumber nilai awal field chakra participant +0x18**, yang dapat diisi oleh dua jalur pemilih tabel/config. Label makna field +0x04 tabel dan identitas nilai `param_1` di FUN_80012780 belum dipastikan lebih jauh. C80 sendiri tidak diambil dalam empat H6 runtime snapshots sebelumnya; nilai runtime pada snapshot itu = TIDAK TAHU.

Bukti instruksi dan base provenance C80 ada di `AZ3_GLOBAL_70C80_SEED_FLOW_2026-11-02.tsv`.

### Mengapa AZ3 biaya masih belum tuntas

Pada 14 callsite Entry1, sepuluh caller awal memberi nilai participant/field/slot; empat di FUN_80109FEC memberi Q+B44, Q, Q+min(B44,0x14), dan Q. Dua MAIN_EXE caller: `0x80013170` memberi word selected table row+0x04; `0x80012DD4` memberi global C80 sebagai nilai awal. **Tidak satu pun dari 16 direct-JAL callsite tervalidasi membentuk `Q(i)-cost`.**

Exporter menghitung 12 instruksi JALR di Entry1 dan 152 di MAIN_EXE. Target JALR tersebut dinamis dan tidak terikat ke setter 0x8001387C; angka itu adalah jumlah semua indirect calls, bukan callsite setter. Computed target, overlay/image lain, dan sumber harga build/upgrade tetap **TIDAK TAHU**.

**Hasil debit biaya: TIDAK TAHU.** Tidak ada dasar untuk mengarang formula build/upgrade. AZ3 direct setter census dan jalur seed awal telah selesai; pencarian jalur debit biaya secara keseluruhan belum selesai.

**Status AZ3: SEBAGIAN (setter/getter dan seed initialization terbukti; biaya build/upgrade belum terbukti).**
## Hipotesis dan falsifier

### AZ2
- H1: bit caller 0x20 bersama state 7 mengendalikan transfer nilai B44 ke participant +0x18. Falsifier: xref producer bit 0x20 menunjukkan flag itu tidak terkait dengan jalur transfer atau penelusuran register menunjukkan nilai setter tidak mengubah participant +0x18.
- H2: state 7 adalah penyelesaian Barrier-release dan B44 adalah nilai yang dirilis. Falsifier: producer B30/B38 atau asal flag 0x20 terbukti terkait aksi lain, atau runtime original-code pada event Barrier release tidak mengikuti state 6→7.

### AZ3
- H1: harga build/upgrade dikalkulasi sebagai Q(i)-cost dan ditulis lewat setter 0x8001387C. Falsifier: caller + indirect call census lengkap menunjukkan pembelian tidak pernah menurunkan saldo melalui setter tersebut.
- H2: harga berasal dari tabel/field lain atau jalur debit terpisah. Falsifier: bukti producer/consumer original-code mengikat seluruh pembelian ke pola Q(i)-cost dan meniadakan sumber alternatif.

Confidence register/control-flow statis K4. Identitas event, unit B30/B38/B40/B44, cost build/upgrade, dan cakupan indirect reader/caller di luar ekspor: TIDAK TAHU. Nol hit tidak dipakai sebagai kesimpulan.
