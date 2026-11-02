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

## AZ3 — saldo awal, transfer, dan debit transaksi petak

Run Step7 memperluas analisis dari 16 direct JAL ke setter menjadi dekompilasi caller/callee dan handler state yang memakai array pending. Direct caller setter tetap:
- Entry1: 14/14 direct JAL candidates divalidasi Ghidra.
- MAIN_EXE: 2/2 divalidasi.
- Total 16 direct JAL.

Daftar callsite dan ekspresi awal ada di `AZ3_SETTER_GETTER_MINUS_COST_CANDIDATES_2026-11-02.tsv`. Tidak adanya ekspresi `Q(i)-cost` pada 16 site tersebut bukan bukti bahwa game tidak punya debit: transaksi petak memakai computed pointer store ke pending array +0x2EE, lalu diproses terpisah.

### Saldo kanonis dan seed awal

`FUN_8001387C(i,value)` memvalidasi `i<4`, clamp -9999..99999, dan menulis ke `0x80070EA0+i*0xB4+0x18`. `FUN_800138EC(i)` membaca field yang sama. Field participant +0x18 adalah saldo Chakra kanonis; beberapa state handler memakai mirror/shadow participant +0x04.

MAIN_EXE callsite `0x80012DD4` melalui `FUN_80012A44` hanya mengambil global `0x80070C80`; `FUN_80012C70` meneruskan nilai itu untuk inisialisasi saldo tiap pemain. Dua writer langsung C80:
- `FUN_80012780`, PC `0x800127D0`: sumber `MEM32[0x8006491C+(param_1&0xFF)*0x30]`.
- `FUN_80012EAC`, PC `0x80012F64`: selected mode/state table row+0x04 di `0x8005779C+idx*0x54`.

Identitas kolom +0x04 dan nilai runtime C80 pada snapshot H6 = **TIDAK TAHU**.

### Jalur biaya pembelian/peningkatan petak

Bukti langsung ada pada `FUN_800D15A8`, cabang action byte `participant_manager+0x2EB == 3 || 8`:
1. `FUN_800BBD9C()` memilih indeks tile dan indeks tersebut disimpan pada `participant_manager+0x4A0`.
2. Biaya transaksi dibaca sebagai `fee = u16(tile+0x1A)`.
3. Pemeriksaan mencukupi membandingkan `fee <= participant[DAT_8013EA6E]+0x04`.
4. Bila cukup, kode menulis `pending[DAT_8013EA6E] = -fee` pada array `participant_manager+0x2EE`.
5. Kode menaikkan nibble level bits 8–11 dan bits 4–7 pada word `tile+0x20`, masing-masing satu.
6. `FUN_800BB004` dan `FUN_800BE464` dipanggil untuk memperbarui representasi/atribut tile.

**Kesimpulan K4 statis:** biaya action petak 3/8 dibaca langsung dari field tile record `+0x1A`; transaksi hanya diproses jika saldo kerja cukup dan debit diposting sebagai signed pending delta `-fee`. Field +0x1A adalah sumber nominal biaya yang digunakan handler tersebut. Ini bukan rumus nilai petak `FUN_800B770C` dan bukan rumus transfer B44.

Asal penyimpanan field harga juga dibuktikan melalui `FUN_800F7ADC`: resource petak diambil melalui helper resource, lalu parser berjalan per-record sumber dengan stride `0x1E` byte. Dua byte `pbVar2[0x14]` dan `pbVar2[0x15]` disalin sebagai halfword little-endian ke runtime `tile+0x1A` (runtime tile stride `0x124`). Jadi nominal harga berasal dari data record resource petak; parser tidak menghitung nominal itu. Nilai nominal per record belum dienumerasi, dan nama gameplay yang lebih spesifik untuk action byte 3 versus 8 tetap **TIDAK TAHU**.

### Pemroses pending delta dan jalur ekonomi yang berbeda

`FUN_800BE5D8` membaca signed pending +0x2EE per pemain, menguraikannya untuk animasi dalam langkah 1/10/100/1000/10000, menerapkan plus/minus ke saldo shadow participant +0x04, lalu memanggil setter `FUN_8001387C` dan getter `FUN_800138EC` untuk menyinkronkan saldo kanonis +0x18. Setelah nominal habis, slot pending dibersihkan.

Jalur lain yang sama-sama menggunakan pending saldo tetapi tidak boleh dinamai biaya pembelian:
- `FUN_800F3658`, event code `'r'`: `FUN_8010BDFC()*500` membentuk transfer antarpemain; array `DAT_80139ECC` menampung delta positif/negatif sebelum dipindahkan oleh `FUN_800DB29C` / `FUN_800E0B3C` ke +0x2EE.
- `FUN_800F2A9C`: membentuk delta berbasis helper nilai event dan jumlah peserta untuk peserta-peserta yang terlibat.
- Cabang lain `FUN_800D15A8`: delta positif memakai `tile+0x1E + level*tile+0x1C`; formula terlihat tetapi label gameplay (pendapatan/hadiah/settlement) = **TIDAK TAHU**.

### Asal data harga petak

Dalam `FUN_800F7ADC`, helper `func_0x8002dbb8`/`func_0x8002dec4` menyediakan buffer resource yang diproses oleh `func_0x8002d7f8`. Parser kemudian melangkah pada record sumber setiap `0x1E` byte. Untuk setiap petak, offset sumber `+0x14` dan `+0x15` disalin ke offset runtime `tile+0x1A` sebagai halfword. Ini menutup rantai: data resource record → runtime tile +0x1A → pemeriksaan saldo → pending debit -fee → pemroses saldo +0x18.

### Batas AZ3

Static K4 menetapkan sumber harga, asal field harga dari record resource, dan mekanisme debit untuk branch petak action 3/8. Belum ada runtime replay transaksi pembelian/upgrade dalam sesi ini. H6 runtime AZ1 adalah HIBRIDA, bukan target checkpoint murni. 12 JALR Entry1 dan 152 JALR MAIN_EXE yang diekspor adalah jumlah semua indirect call; target dinamis yang tidak terikat, overlay lain, dan kemungkinan transaksi lain di luar branch yang ditelusuri tetap **TIDAK TAHU**.

**Status AZ3: SELESAI untuk jalur transaksi petak action 3/8, saldo, dan sinkronisasinya dalam audit statis ini; batas semantik dan coverage di atas tetap dicatat sebagai TIDAK TAHU.**

## Hipotesis dan falsifier

### AZ2
- H1: bit caller 0x20 bersama state 7 mengendalikan transfer nilai B44 ke participant +0x18. Falsifier: xref producer bit 0x20 menunjukkan flag itu tidak terkait dengan jalur transfer atau penelusuran register menunjukkan nilai setter tidak mengubah participant +0x18.
- H2: state 7 adalah penyelesaian Barrier-release dan B44 adalah nilai yang dirilis. Falsifier: producer B30/B38 atau asal flag 0x20 terbukti terkait aksi lain, atau runtime original-code pada event Barrier release tidak mengikuti state 6→7.

### AZ3
- H1 yang kini didukung K4 statis: pada handler `FUN_800D15A8`, action byte 3/8 memakai `u16(tile+0x1A)` sebagai biaya; bila saldo participant +0x04 cukup, pending +0x2EE mendapat `-fee` dan dua level nibble tile+0x20 naik satu.
- Falsifier untuk H1: decode independen atau penelusuran register membuktikan nilai +0x1A bukan operand perbandingan dan debit pending bukan berasal dari nilai yang sama.
- H2: semua action bangun/upgrade dalam game memakai jalur tersebut. **Belum terbukti**; action lain, indirect calls, dan overlay lain masih harus diaudit.

Confidence control-flow dan dataflow action 3/8 = K4 statis. Tidak ada klaim K5 runtime untuk transaksi ini. Identitas nama action, nominal setiap tile, label delta positif tile+0x1E/1C, nama event B30/B38/B40/B44, dan coverage indirect handler lain tetap TIDAK TAHU. Nol hit tidak dipakai sebagai kesimpulan.
