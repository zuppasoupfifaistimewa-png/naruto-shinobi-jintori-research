# AZ2–AZ3 — audit statis manager dan setter biaya
Tanggal: 2 November 2026
Target: SLPS-03553 / DATA.BIN Entry 1
Bukti instruksi MIPS / p-code statis. Maksimum K4; bukan hasil gameplay.
Input Entry 1: 596,412 byte; file offset 0x10BB000; SHA-256 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a. Base 0x800AD450 adalah kandidat impor statis, bukan pemetaan runtime tervalidasi.

## AZ2 — pembaca manager +0xB38 / +0xB40 / +0xB44

Ekspor fungsi AQ1 menyediakan badan instruksi mentah lengkap untuk tiga fungsi yang memuat pembaca field ini: FUN_80109994, FUN_80109F1C, FUN_80109FEC. Pemeriksaan ulang byte dan disassembly menemukan **17 instruksi load langsung** dalam ruang lingkup tiga badan fungsi tersebut: +0xB38 ada 5 reader, +0xB40 ada 4 reader, +0xB44 ada 8 reader. PC, fungsi, instruksi, byte mentah, dan tepat 12 instruksi sebelumnya (atau jumlah yang tersedia bila fungsi dimulai) ada dalam:
`reports/stage1_economy/AZ2_MANAGER_READERS_2026-11-02.tsv`.

Ringkasan semua reader:

| Field | PC | Fungsi | Instruksi | Pemakaian yang terlihat dari instruksi berikutnya |
|---|---|---|---|---|
| +0xB38 | 0x80109A88 | FUN_80109994 | lw v1,0xB38(a0) | ditambah B30 pada A90; hasil masuk B40 melalui A94 |
| +0xB44 | 0x80109F64 | FUN_80109F1C | lw a2,0xB44(v1) | diteruskan sebagai a2 ke formatter 0x8001B364; label UI TIDAK TAHU |
| +0xB38 | 0x8010A0E0 | FUN_80109FEC | lw v1,0xB38(v0) | disalin ke progress B3C pada A0E8 |
| +0xB40 | 0x8010A0EC | FUN_80109FEC | lw v1,0xB40(v0) | disalin ke B44 pada A0F4 |
| +0xB44 | 0x8010A154 | FUN_80109FEC | lw a1,0xB44(v1) | delay slot setter A15C membentuk a1=Q(i)+B44 |
| +0xB38 | 0x8010A460 | FUN_80109FEC | lw v1,0xB38(v1) | membandingkan progress B3C dengan target B38 |
| +0xB38 | 0x8010A4D8 | FUN_80109FEC | lw v1,0xB38(v1) | membandingkan B3C setelah kenaikan 0x14 terhadap B38 |
| +0xB38 | 0x8010A4F8 | FUN_80109FEC | lw v1,0xB38(v0) | menyalin B38 ke B3C pada terminal state 5 |
| +0xB44 | 0x8010A524 | FUN_80109FEC | lw v0,0xB44(v1) | dipasangkan dengan B40 untuk tes B44<B40 |
| +0xB40 | 0x8010A528 | FUN_80109FEC | lw v1,0xB40(v1) | target pembanding B44 pada state 6 |
| +0xB44 | 0x8010A590 | FUN_80109FEC | lw v0,0xB44(v1) | progress B44 sebelum kenaikan 0x14 |
| +0xB40 | 0x8010A5A0 | FUN_80109FEC | lw v1,0xB40(v1) | target pembanding progress B44 |
| +0xB40 | 0x8010A5C0 | FUN_80109FEC | lw v1,0xB40(v0) | disalin ke B44 pada A5C8; state menjadi 7 |
| +0xB44 | 0x8010A5EC | FUN_80109FEC | lw v0,0xB44(v0) | tes B44<21 untuk memilih ukuran langkah |
| +0xB44 | 0x8010A610 | FUN_80109FEC | lw s1,0xB44(v0) | jika B44<21, s1=B44; jika tidak, delay slot A604 memberi s1=20 |
| +0xB44 | 0x8010A648 | FUN_80109FEC | lw v0,0xB44(v1) | nilai lama sebelum subu di A650; nilai baru ditulis di delay slot A658 |
| +0xB44 | 0x8010A6A8 | FUN_80109FEC | lw v0,0xB44(v1) | tes terminal B44!=0; jika nol state menjadi 8 |

**Cakupan penting:** tabel ini adalah seluruh pembaca langsung yang teramati pada tiga badan fungsi lengkap yang dipilih/export oleh AQ1, bukan census seluruh module / semua indirect alias. Di luar tiga badan ini, reader lain bagi B38/B40/B44 = **TIDAK TAHU**. Tidak ada kesimpulan dari nol hit yang tidak diuji. File AW1 yang ada mencatat 14 akses displacement +0xB44 dalam tiga fungsi (termasuk store/init); jumlah itu konsisten dengan delapan reader B44 di atas ditambah store/other.

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

## AZ3 — kandidat biaya bangun/upgrade sebagai getter dikurangi nilai

Seluruh 14 direct JAL yang diekspor pada AX2 menuju setter 0x8001387C sudah direkonsiliasi di:
`reports/stage1_economy/AZ3_SETTER_GETTER_MINUS_COST_CANDIDATES_2026-11-02.tsv`.
Callsite:
0x800B41B0, 0x800B4254, 0x800B4F00, 0x800B4F64, 0x800B6238, 0x800BEC98, 0x800DEB38, 0x800E1BE0, 0x800EC9A4, 0x800F95E8, 0x8010A15C, 0x8010A1B0, 0x8010A638, 0x8010A97C.

Sepuluh caller awal memuat nilai dari participant / field record atau indeks; empat di FUN_80109FEC menghasilkan Q+B44, Q, Q+min(B44,20), Q. Tidak ada dari 14 direct JAL tersebut yang membentuk a1=Q(i)-nilai. Pengurangan B44-s1 pada A650 adalah pengurasan progress, bukan argumen debit harga kepada setter.

**Hasil AZ3: TIDAK TAHU.** Tidak ada getter-minus-cost yang ditemukan pada 14 direct JAL yang diekspor; ini bukan bukti bahwa pola tersebut tidak ada di seluruh game. Indirect JALR dan pemanggil setter di luar ekspor AX2 belum ditelusuri tuntas. Tabel sumber/indeks untuk harga build atau upgrade belum terbukti.

## Hipotesis dan falsifier

### AZ2
- H1: bit caller 0x20 bersama state 7 mengendalikan transfer nilai B44 ke participant +0x18. Falsifier: xref producer bit 0x20 menunjukkan flag itu tidak terkait dengan jalur transfer atau penelusuran register menunjukkan nilai setter tidak mengubah participant +0x18.
- H2: state 7 adalah penyelesaian Barrier-release dan B44 adalah nilai yang dirilis. Falsifier: producer B30/B38 atau asal flag 0x20 terbukti terkait aksi lain, atau runtime original-code pada event Barrier release tidak mengikuti state 6→7.

### AZ3
- H1: harga build/upgrade dikalkulasi sebagai Q(i)-cost dan ditulis lewat setter 0x8001387C. Falsifier: caller + indirect call census lengkap menunjukkan pembelian tidak pernah menurunkan saldo melalui setter tersebut.
- H2: harga berasal dari tabel/field lain atau jalur debit terpisah. Falsifier: bukti producer/consumer original-code mengikat seluruh pembelian ke pola Q(i)-cost dan meniadakan sumber alternatif.

Confidence register/control-flow statis K4. Identitas event, unit B30/B38/B40/B44, cost build/upgrade, dan cakupan indirect reader/caller di luar ekspor: TIDAK TAHU. Nol hit tidak dipakai sebagai kesimpulan.
