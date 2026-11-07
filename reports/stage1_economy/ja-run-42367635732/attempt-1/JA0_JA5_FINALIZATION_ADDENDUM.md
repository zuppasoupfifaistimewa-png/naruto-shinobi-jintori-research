# JA0-JA5 finalization addendum

Baseline JA inklusif: `09c071e6c496b61b0689499a641faa3aa482b145`.
JA source SHA: `570f19c472b5238349909873ac6c68afc84359df`.
Published HEAD before this addendum: `a762127e097eab2f19fb190559c1b28dba0c50e4`.

## JA0 — ledger final
Pada source SHA, ledger inklusif menghitung 2 commit (1 manusia, 1 bot), 1 Actions run, 0 scheduled, dan 65/65 skrip Python lulus `py_compile`.
Baris `JA0_LEDGER_ACTIONS.tsv` dihasilkan saat job yang sama masih berjalan, sehingga run 42367635732 tertulis sementara sebagai `in_progress`. Status final telah dibaca ulang setelah job selesai: `completed/success`, job `ja0-ja5-static`, job ID 128388959351, exit code 0. Gunakan `JA0_LEDGER_FINALIZATION.tsv` untuk menutup status sementara tersebut.
Run summary: status PASS, Ghidra EXE 0, Entry 1 0, analyzer 0, cleanup PASS; tanpa emulator/game/BIOS/savestate dan tanpa biner di Git.
Ledger final tahap IA tetap: 10 commit (7 manusia, 3 bot), 6 run seluruh event, 0 scheduled, 64/64 py_compile. Rincian lengkap ada pada `JA0_IA_FINAL_LEDGER_*.tsv`.

## JA1 — caller argument dan record +4
Satu JAL langsung untuk FUN_80014F10 terbukti pada Entry 1 PC 0x800DD1CC dalam FUN_800DC2E0.
Argumen a0 berasal dari `lhu $a0,0x20($v0)` lalu diubah pada delay slot menjadi `u16 >> 12`; ini adalah owner nibble.
Argumen a1 berasal dari `lw $a1,0x4f4($a1)`; jalur negatif melakukan `negu`, sehingga nilai yang dipassing adalah nilai absolut dari word tersebut. Identitas base register sebelum load +0x4F4 masih TIDAK TAHU. Tidak ada bukti bahwa argumen itu adalah saldo wallet.
FUN_80014F10 sendiri menghitung alamat owner-record ber-stride 0xB4 pada offset +0x94, membaca nilai lama, lalu menulis a1 hanya jika lebih besar. Ini bukan bukti setter saldo pada record peserta +4.
Census +4: 130 akses = 96 read + 34 write. 52 akses basis/stride terkonfirmasi (47 read + 5 write); 78 sisanya kandidat (49 read + 29 write). Lima write terkonfirmasi tercantum di `JA1_PLUS4_CONFIRMED_WRITES.tsv`. Setter wallet otoritatif tetap TIDAK TAHU.

## JA2 — x dan tabel H
Ketiga site writer store nilai byte. D49D8 menerima hasil `lbu` di D49D0; EC844/EC868 menerima byte dari EA 0x80139EC7 dengan ANDI 0xFF. Rentang tipe yang didukung instruksi adalah 0..255 bila jalur store berjalan.
Tabel H berisi 52 baris, indeks 0..51. Tidak ada bukti statis di JA yang membatasi setiap x menjadi kurang dari 52; karena itu subset indeks H yang benar-benar reachable masih TIDAK TAHU. Indeks 0 hanya teramati sebagai nilai reset kondisional di E8174, bukan bukti bahwa F2A9C membacanya.
Hipotesis x=d dan x=ID efek/item tetap K1. Tidak ada pemetaan x=d yang terbukti. Rincian tambahan nilai-byte dan batas tabel ada di `JA2_H_REACHABILITY_ADDENDUM.tsv`.

## JA3 — koreksi indeks loop
0x800BEDA4 berada dalam fungsi induk `FUN_800BE5D8`. $v0 pada store adalah manager base + 2*$s1. $s1 diinisialisasi nol, kemudian bertambah dan dibandingkan dengan 4; maka indeks pada site adalah loop variable 0..3, bukan konstanta 0. Kesimpulan index=0 dari linear backward slice awal harus dianggap superseded oleh addendum ini.
Satu direct caller ke parent ditemukan pada PC 0x800B54F4, fungsi caller `FUN_800B50AC`; kelengkapan seluruh caller belum dibuktikan.
0x800B24C8 memiliki instruksi store yang tercatat dalam excerpt statis terdahulu, tetapi JA Ghidra range/code census tidak menemukan fungsi induk atau caller. Keduanya TIDAK TAHU.

## JA4 dan JA5
JA4 TUNTAS K4: tidak ada runtime.
JA5 SEBAGIAN K3: hanya rumus simbolik dari store dan domain byte bersyarat; x=0 tetap reset kondisional, bukan x operational yang terbukti. Tidak ada fitting dan tidak ada penggunaan angka 400/800/1600.

## Status final per JA
- JA0 TUNTAS K4.
- JA1 SEBAGIAN K4.
- JA2 SEBAGIAN K3.
- JA3 SEBAGIAN K3.
- JA4 TUNTAS K4.
- JA5 SEBAGIAN K3.

## TIDAK TAHU yang tetap
- Setter wallet otoritatif dan apakah participant+4 adalah saldo permanen.
- Identitas base $a1 pada load +0x4F4 di caller FUN_800DC2E0 serta semantik nilai tersebut.
- Caller argument/value origins lain yang tidak ditutup dari function-entry boundary.
- Nilai byte konkret yang reachable pada tiap x writer dan apakah writer jalurnya berjalan.
- Guard/bounds untuk x terhadap tabel H 52 entri; subset H yang benar-benar reachable.
- Apakah x adalah delta level d atau effect/item/action selector.
- Fungsi induk, $v0 base, index, dan caller untuk zero-writer 0x800B24C8.
- Caller set lengkap untuk parent FUN_800BE5D8.
- Rumus numerik biaya upgrade untuk lompat level d>=2.
