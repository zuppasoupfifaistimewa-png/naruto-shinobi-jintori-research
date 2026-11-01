# AU1 — accessor disassembly lengkap

Tanggal: 1 November 2026 (Asia/Jakarta)  
Sumber: Ghidra headless run 41274567492, job 124754117941, source SHA `7def692176e0ac7e21bff0d4a9a5eca8baf70880`, exit code desimal 0.  
Program: PS-X EXE SLPS_035.53, base `0x80010000`. Statis; maksimum K4.

## Setter 0x8001387C

| Alamat | Byte (little-endian) | Instruksi |
|---|---|---|
| 0x8001387C | 21 30 80 00 | move a2,a0 |
| 0x80013880 | 04 00 C2 2C | sltiu v0,a2,0x4 |
| 0x80013884 | 03 00 40 14 | bne v0,zero,0x80013894 |
| 0x80013888 | 01 00 02 3C | _lui v0,0x1 (delay slot) |
| 0x8001388C | 08 00 E0 03 | jr ra |
| 0x80013890 | 21 10 00 00 | _clear v0 (delay slot) |
| 0x80013894 | 9F 86 42 34 | ori v0,v0,0x869f |
| 0x80013898 | 2A 10 45 00 | slt v0,v0,a1 |
| 0x8001389C | 04 00 40 10 | beq v0,zero,0x800138b0 |
| 0x800138A0 | 00 00 00 00 | _nop (delay slot) |
| 0x800138A4 | 01 00 05 3C | lui a1,0x1 |
| 0x800138A8 | 30 4E 00 08 | j 0x800138c0 |
| 0x800138AC | 9F 86 A5 34 | _ori a1,a1,0x869f (delay slot) |
| 0x800138B0 | F1 D8 A2 28 | slti v0,a1,-0x270f |
| 0x800138B4 | 03 00 40 10 | beq v0,zero,0x800138c4 |
| 0x800138B8 | 07 80 04 3C | _lui a0,0x8007 (delay slot) |
| 0x800138BC | F1 D8 05 24 | li a1,-0x270f |
| 0x800138C0 | 07 80 04 3C | lui a0,0x8007 |
| 0x800138C4 | A0 0E 84 24 | addiu a0,a0,0xea0 |
| 0x800138C8 | 40 18 06 00 | sll v1,a2,0x1 |
| 0x800138CC | 21 18 66 00 | addu v1,v1,a2 |
| 0x800138D0 | 00 11 03 00 | sll v0,v1,0x4 |
| 0x800138D4 | 23 10 43 00 | subu v0,v0,v1 |
| 0x800138D8 | 80 10 02 00 | sll v0,v0,0x2 |
| 0x800138DC | 21 20 82 00 | addu a0,a0,v0 |
| 0x800138E0 | 18 00 85 AC | sw a1,0x18(a0) |
| 0x800138E4 | 08 00 E0 03 | jr ra |
| 0x800138E8 | 01 00 02 24 | _li v0,0x1 (delay slot) |

### Operand setter

- `a0` masuk: indeks record; instruksi pertama menyalin ke `a2`. Kemudian `a0` ditimpa menjadi pointer record.
- `a1` masuk: nilai 32-bit yang hendak ditulis; callee dapat membatasi nilainya. Jika nilai lebih besar dari 99999 menjadi 99999; jika lebih kecil dari -9999 menjadi -9999.
- `a2`: salinan indeks untuk pemeriksaan dan kalkulasi offset.
- `v0`: hasil pemeriksaan indeks / clamp dan nilai return (0 bila indeks tidak valid, 1 bila penulisan dilakukan).
- `v1`: temporary kalkulasi stride.
- `ra`: alamat kembali.
- `zero`: register MIPS konstan bernilai 0; dipakai pada branch pembanding dan bukan input yang dapat berubah.
- Record target dibentuk dari `0x80070EA0 + a2*0xB4`; store ke `+0x18`.

## Getter 0x800138EC

| Alamat | Byte (little-endian) | Instruksi |
|---|---|---|
| 0x800138EC | 21 28 80 00 | move a1,a0 |
| 0x800138F0 | 04 00 A2 2C | sltiu v0,a1,0x4 |
| 0x800138F4 | 0B 00 40 10 | beq v0,zero,0x80013924 |
| 0x800138F8 | 07 80 04 3C | _lui a0,0x8007 (delay slot) |
| 0x800138FC | A0 0E 84 24 | addiu a0,a0,0xea0 |
| 0x80013900 | 40 18 05 00 | sll v1,a1,0x1 |
| 0x80013904 | 21 18 65 00 | addu v1,v1,a1 |
| 0x80013908 | 00 11 03 00 | sll v0,v1,0x4 |
| 0x8001390C | 23 10 43 00 | subu v0,v0,v1 |
| 0x80013910 | 80 10 02 00 | sll v0,v0,0x2 |
| 0x80013914 | 21 20 82 00 | addu a0,a0,v0 |
| 0x80013918 | 18 00 82 8C | lw v0,0x18(a0) |
| 0x8001391C | 08 00 E0 03 | jr ra |
| 0x80013920 | 00 00 00 00 | _nop (delay slot) |
| 0x80013924 | 08 00 E0 03 | jr ra |
| 0x80013928 | 21 10 00 00 | _clear v0 (delay slot) |

### Operand getter

- `a0` masuk: indeks record. Instruksi pertama menyalin indeks ke `a1`; `a0` kemudian ditimpa menjadi basis `0x80070EA0 + index*0xB4`.
- `a1`: salinan indeks yang dibuat oleh callee; guard `a1<4` dan offset `a1*0xB4` menggunakan salinan ini. Nilai a1 dari caller tidak digunakan.
- `v0`: temporary pemeriksaan indeks, lalu word hasil getter; return 0 bila indeks tidak valid.
- `v1`: temporary kalkulasi stride.
- `ra`: alamat kembali.
- `zero`: register MIPS konstan bernilai 0; dipakai pada branch pembanding dan instruksi clear, bukan input yang dapat berubah.
- Load word berada pada offset `+0x18` dari record terpilih.

## Rekonsiliasi event runtime AT3

Disassembly mengunci urutan register: saat breakpoint entry `0x800138EC`, a0 masih indeks; pada instruksi pertama a1 disetel sama dengan a0. Setelah kalkulasi stride, a0 menjadi pointer record. Ini cocok dengan event yang mencatat:

| Call return RA | a0 pada entry | a1 pada entry | a0 pada return | a1 pada return | v0 |
|---|---:|---:|---:|---:|---:|
| 0x801053CC | 0 atau 1 | 0 atau 1 | 0x80070EA0 atau 0x80070F54 | 0 atau 1 | 0x000005DC |
| 0x80105420 | 0 atau 1 | 0x801CEF08 (fall-through) / s3 (BLTZ-taken) | 0x80070EA0 atau 0x80070F54 | 0 atau 1 | 0x000005DC |

`0x80070F54 - 0x80070EA0 = 0xB4`, sama dengan stride record. Nilai `a1=0x801CEF08` saat masuk getter kedua tidak menjadi indeks; `move a1,a0` langsung menimpanya. Pada call pertama, a1 caller-supplied yang tidak diketahui juga tidak relevan untuk indeks.

Kesimpulan di atas membuktikan mekanika akses record pada dua fungsi. Identitas ekonomi/gameplay dari field di `+0x18` **TIDAK DITETAPKAN** oleh disassembly ini saja.

## Koreksi asal a1 pada getter kedua

Getter pertama dipanggil di 0x801053C4; delay slot caller 0x801053C8: move a0,s3. Instruksi pertamanya, 0x800138EC: move a1,a0, mengubah a1 menjadi s3. Pada BLTZ-taken tidak ada penulis a1 lagi sebelum getter kedua, sehingga a1=s3. Pada fall-through jalur menjalankan:

```asm
0x801053D0  lui v0,0x8014
0x801053D4  lw a1,-0x5AAC(v0)   ; effective global slot 0x8013A554
```

Trace lama mengamati isi slot manager tersebut sebagai 0x801CEF08. Delay slot getter kedua 0x8010541C memberi a0=s3 dan instruksi pertama getter kedua move a1,a0 mengganti a1 masuk. Pointer manager bukan indeks getter.
