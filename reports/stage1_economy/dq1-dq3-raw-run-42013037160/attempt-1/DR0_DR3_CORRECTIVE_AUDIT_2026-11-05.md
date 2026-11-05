# Koreksi dan reanalisis DR0–DR3 — run 42013037160

Tanggal audit: 2026-11-05. Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. Baseline inklusif: `d7f676bc2a87e742867d93f342ecbca4dd094d12`. Snapshot awal: `main=d7f676bc2a87e742867d93f342ecbca4dd094d12`.

## Ringkasan putusan

- **DR0: 1 commit total = 0 manusia + 1 bot** pada snapshot awal. Commit baseline d7 dibuat oleh `github-actions[bot]`; parent `122ef33695c4a1d10bf3829c95d5502f9972c043` berada di luar rentang.
- **DR1: TUNTAS K3 untuk census kandidat**: 39 writer raw; 0 DARI_TILE_1A, 20 COMPUTED, 7 CLEAR, 12 LAIN.
- **DR2: TUNTAS K3/K4 terbatas**: 2 direct JAL caller; 25 akses +0x2EE (22 WRITE, 3 READ). Index helper berasal dari halfword global `0x8013EBB0`, skala 2; setter upstream untuk tiap caller = TIDAK TAHU. Tiga reader +0x2EE belum terbukti berujung pengurangan Chakra.
- **DR3: TIDAK TAHU (K2 hipotesis)**: jalur lengkap perbandingan level saat ini vs target → operasi fee → store ke `0x80139EFC` belum tertaut. Tiga observasi d>=2 cocok dengan hipotesis `fee=X×2^d`, bukan fakta kode.

## DR0 — hitung commit inklusif

`d7f676bc...` adalah HEAD main saat audit dimulai dan batas rentang snapshot. Satu commit tercakup: d7f676bc2a87e742867d93f342ecbca4dd094d12. Git API menyatakan author dan committer `github-actions[bot]`; parent commit `122ef33695c4a1d10bf3829c95d5502f9972c043` tidak termasuk. Hasil: **total 1; manusia 0; bot 1**. Commit koreksi audit ini terjadi setelah snapshot dan tidak dihitung dalam rentang snapshot DR0.

## DR1 — writer 0x80139EFC: recount TSV

| Label | Jumlah |
|---|---:|
| DARI_TILE_1A | 0 |
| COMPUTED | 20 |
| CLEAR | 7 |
| LAIN | 12 |
| **Total** | **39** |

Recount berasal dari seluruh baris data `DQ1B_GLOBAL_80139EFC_WRITERS_RAW.tsv`, bukan angka census yang disalin. Definisi label adalah provenance register scanner: DARI_TILE_1A = sumber akhir dari `lhu +0x1A`; COMPUTED = operasi aritmetika/logika terdeteksi; CLEAR = operand `$zero`; LAIN = asal belum seluruhnya diklasifikasikan. Nama fungsi adalah nearest JAL/prologue heuristic kecuali `FUN_800ec574` yang targetnya diketahui; label fungsi belum identik dengan boundary fungsi yang dibuktikan.

### Pengali, shift, loop di 39 window

- Instruksi `mult`/`multu`: **0** pada 12 instruksi pre-store (cakupan 39 kandidat).
- Window yang mengandung shift (`sll/srl/sra`): **12/39**, PC writer: 0x800D21B0, 0x800D2480, 0x800D25DC, 0x800D6204, 0x800E82C8, 0x800E8350, 0x800E8400, 0x800ECA64, 0x800F0948, 0x800F0B04, 0x800F188C, 0x800F2554. Mayoritas shift membangun offset/stride indeks tabel (contoh 0x800D2480, 0x800D25DC, 0x800E82C8, 0x800E8350/0x800E8400, 0x800F0948/0x800F0B04, 0x800F2554); 0x800F188C membagi signed field dengan 2 memakai koreksi tanda.
- Back-edge conditional branch: **4**: 0x800CFF14→0x800cfe7c (writer 0x800CFF2C, FUN_800cee18); 0x800F0480→0x800f042c (writer 0x800F0490, FUN_800ef9a4); 0x800F39EC→0x800f39b4 (writer 0x800F39F4, FUN_800f3658); 0x800F3AC0→0x800f3a64 (writer 0x800F3ADC, FUN_800f3658). Ini menunjukkan loop/back-edge dalam konteks lokal; bukan bukti bahwa setiap store dijalankan pada setiap iterasi.
- Tidak ditemukannya `mult/multu` di window ini bukan bukti bahwa tidak ada operasi perkalian di bagian fungsi lain/callee.

### Semua 39 writer: PC, fungsi, label, provenance, instruksi, excerpt


### 1. 0x800CFF2C — COMPUTED — FUN_800cee18

- Store: `sw $v0, -0x6104($v1)`; word: `FC 9E 62 AC`.
- Asal nilai: Store bernilai 0x2710 (10.000): 0x800CFF28 `addiu $v0,$zero,0x2710` tepat sebelum store. Increment pada 0x800CFF00 ada di loop lebih awal; register ditimpa konstanta sebelum ditulis.
- 12 instruksi sebelumnya:

  `0x800CFEFC nop
  0x800CFF00 addiu $v0, $v0, 1
  0x800CFF04 sw $v0, -0x14f4($a1)
  0x800CFF08 lw $v1, -0x1538($a3)
  0x800CFF0C nop
  0x800CFF10 slt $v0, $v0, $v1
  0x800CFF14 bnez $v0, 0x800cfe7c
  0x800CFF18 nop
  0x800CFF1C lui $v0, 0x8014
  0x800CFF20 sw $zero, -0x1450($v0)
  0x800CFF24 lui $v1, 0x8014
  0x800CFF28 addiu $v0, $zero, 0x2710`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `00 00 00 00 01 00 42 24 0C EB A2 AC C8 EA E3 8C 00 00 00 00 2A 10 43 00 D9 FF 40 14 00 00 00 00 14 80 02 3C B0 EB 40 AC 14 80 03 3C 10 27 02 24`

### 2. 0x800CFFA8 — LAIN — FUN_800cee18

- Store: `sw $a2, -0x6104($v1)`; word: `FC 9E 66 AC`.
- Asal nilai: Sumber langsung `$a2` = `lh $a2,0xa($s0)` pada 0x800CFF90 (signed halfword struktur `$s0`). Identitas struktur dan makna field TIDAK TAHU.
- 12 instruksi sebelumnya:

  `0x800CFF78 move $a2, $s0
  0x800CFF7C lhu $v0, 0x10($s0)
  0x800CFF80 nop
  0x800CFF84 andi $v0, $v0, 0x40
  0x800CFF88 beqz $v0, 0x800cffac
  0x800CFF8C lui $v1, 0x8014
  0x800CFF90 lh $a2, 0xa($s0)
  0x800CFF94 lw $v0, -0x6104($v1)
  0x800CFF98 nop
  0x800CFF9C slt $v0, $a2, $v0
  0x800CFFA0 beqz $v0, 0x800cffac
  0x800CFFA4 nop`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `21 30 00 02 10 00 02 96 00 00 00 00 40 00 42 30 08 00 40 10 14 80 03 3C 0A 00 06 86 FC 9E 62 8C 00 00 00 00 2A 10 C2 00 02 00 40 10 00 00 00 00`

### 3. 0x800D09C8 — COMPUTED — FUN_800d05b8

- Store: `sw $a0, -0x6104($s0)`; word: `FC 9E 04 AE`.
- Asal nilai: TIDAK TAHU: `$a0` diisi dari `$v0` pada 0x800D09C4 setelah `jal 0x80102408` di 0x800D09BC. Return callee tidak dianalisis dalam artefak ini.
- 12 instruksi sebelumnya:

  `0x800D0998 j 0x800d0f9c
  0x800D099C nop
  0x800D09A0 lui $s1, 0x8014
  0x800D09A4 lui $v0, 0x8014
  0x800D09A8 lw $v0, -0x158c($v0)
  0x800D09AC nop
  0x800D09B0 lw $v0, 0x370($v0)
  0x800D09B4 nop
  0x800D09B8 sw $v0, -0x1450($s1)
  0x800D09BC jal 0x80102408
  0x800D09C0 lui $s0, 0x8014
  0x800D09C4 move $a0, $v0`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `E7 43 03 08 00 00 00 00 14 80 11 3C 14 80 02 3C 74 EA 42 8C 00 00 00 00 70 03 42 8C 00 00 00 00 B0 EB 22 AE 02 09 04 0C 14 80 10 3C 21 20 40 00`

### 4. 0x800D21B0 — CLEAR — FUN_800d15a8

- Store: `sw $zero, -0x6104($v0)`; word: `FC 9E 40 AC`.
- Asal nilai: CLEAR: store memakai `$zero`, sehingga nilai tertulis tepat 0.
- 12 instruksi sebelumnya:

  `0x800D2180 lui $v0, 0x8014
  0x800D2184 lw $a3, -0x146c($v0)
  0x800D2188 lw $a0, 0xc($v1)
  0x800D218C sll $a2, $a2, 0x10
  0x800D2190 jal 0x800f7ed4
  0x800D2194 sll $a3, $a3, 0x10
  0x800D2198 lui $v0, 0x8014
  0x800D219C lw $v0, -0x6428($v0)
  0x800D21A0 nop
  0x800D21A4 bnez $v0, 0x800d2d9c
  0x800D21A8 lui $v0, 0x8014
  0x800D21AC lui $v0, 0x8014`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `14 80 02 3C 94 EB 47 8C 0C 00 64 8C 00 34 06 00 B5 DF 03 0C 00 3C 07 00 14 80 02 3C D8 9B 42 8C 00 00 00 00 FD 02 40 14 14 80 02 3C 14 80 02 3C`

### 5. 0x800D2254 — COMPUTED — FUN_800d15a8

- Store: `sw $v0, -0x6104($v1)`; word: `FC 9E 62 AC`.
- Asal nilai: Nilai 1 pada jalur store: 0x800D224C `addiu $v0,$zero,1`; store di 0x800D2254 adalah delay-slot dari `j` 0x800D2250. Branch 0x800D2228 dapat melewati blok ini.
- 12 instruksi sebelumnya:

  `0x800D2224 addiu $v0, $zero, 0xff
  0x800D2228 beq $v1, $v0, 0x800d262c
  0x800D222C lui $v0, 0x8014
  0x800D2230 lw $a0, -0x158c($v0)
  0x800D2234 lui $v1, 0x8014
  0x800D2238 lhu $v0, -0x14b4($a1)
  0x800D223C nop
  0x800D2240 sh $v0, -0x1578($v1)
  0x800D2244 sb $v0, 0x502($a0)
  0x800D2248 lui $v1, 0x8014
  0x800D224C addiu $v0, $zero, 1
  0x800D2250 j 0x800d262c`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `FF 00 02 24 00 01 62 10 14 80 02 3C 74 EA 44 8C 14 80 03 3C 4C EB A2 94 00 00 00 00 88 EA 62 A4 02 05 82 A0 14 80 03 3C 01 00 02 24 8B 49 03 08`

### 6. 0x800D2480 — LAIN — FUN_800d15a8

- Store: `sw $v1, -0x6104($v0)`; word: `FC 9E 43 AC`.
- Asal nilai: Sumber langsung `$v1` = `lbu $v1,($v0)` pada 0x800D246C; pointer tabel/record dibentuk dari indeks dan stride shift/add. Isi byte aktual TIDAK TAHU tanpa data tabel dan alur indeks lengkap.
- 12 instruksi sebelumnya:

  `0x800D2450 lw $a0, -0x157c($v0)
  0x800D2454 sll $v0, $v1, 3
  0x800D2458 addu $v0, $v0, $v1
  0x800D245C sll $v0, $v0, 3
  0x800D2460 addu $v0, $v0, $v1
  0x800D2464 sll $v0, $v0, 2
  0x800D2468 addu $v0, $v0, $a0
  0x800D246C lbu $v1, ($v0)
  0x800D2470 addiu $v0, $zero, 1
  0x800D2474 bne $v1, $v0, 0x800d25e4
  0x800D2478 lui $v0, 0x8014
  0x800D247C j 0x800d25e4`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `84 EA 44 8C C0 10 03 00 21 10 43 00 C0 10 02 00 21 10 43 00 80 10 02 00 21 10 44 00 00 00 43 90 01 00 02 24 5B 00 62 14 14 80 02 3C 79 49 03 08`

### 7. 0x800D25DC — COMPUTED — FUN_800d15a8

- Store: `sw $v0, -0x6104($v1)`; word: `FC 9E 62 AC`.
- Asal nilai: Nilai 1: 0x800D25D8 `addiu $v0,$zero,1` tepat sebelum store; hanya jalur yang lolos branch 0x800D25CC mencapai store.
- 12 instruksi sebelumnya:

  `0x800D25AC sll $v0, $v1, 3
  0x800D25B0 addu $v0, $v0, $v1
  0x800D25B4 sll $v0, $v0, 3
  0x800D25B8 addu $v0, $v0, $v1
  0x800D25BC sll $v0, $v0, 2
  0x800D25C0 addu $v0, $v0, $a0
  0x800D25C4 lbu $v1, ($v0)
  0x800D25C8 addiu $v0, $zero, 4
  0x800D25CC bne $v1, $v0, 0x800d25e4
  0x800D25D0 lui $v0, 0x8014
  0x800D25D4 lui $v1, 0x8014
  0x800D25D8 addiu $v0, $zero, 1`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `C0 10 03 00 21 10 43 00 C0 10 02 00 21 10 43 00 80 10 02 00 21 10 44 00 00 00 43 90 04 00 02 24 05 00 62 14 14 80 02 3C 14 80 03 3C 01 00 02 24`

### 8. 0x800D6204 — COMPUTED — FUN_800d5bc0

- Store: `sw $v0, -0x6104($v1)`; word: `FC 9E 62 AC`.
- Asal nilai: Nilai 0xFF (255): 0x800D6200 `addiu $v0,$zero,0xff` tepat sebelum store. `sll`/`subu` sebelumnya menyiapkan field lain (`0xc($t2)`), bukan operand store ini.
- 12 instruksi sebelumnya:

  `0x800D61D4 addu $v0, $v0, $v1
  0x800D61D8 sll $v0, $v0, 2
  0x800D61DC addu $v0, $v0, $a3
  0x800D61E0 lh $v0, 0x24($v0)
  0x800D61E4 nop
  0x800D61E8 subu $a0, $a0, $v0
  0x800D61EC sw $a0, 0xc($t2)
  0x800D61F0 lui $v1, 0x8014
  0x800D61F4 addiu $v0, $zero, 0x3e8
  0x800D61F8 sw $v0, -0x1478($v1)
  0x800D61FC lui $v1, 0x8014
  0x800D6200 addiu $v0, $zero, 0xff`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `21 10 43 00 80 10 02 00 21 10 47 00 24 00 42 84 00 00 00 00 23 20 82 00 0C 00 44 AD 14 80 03 3C E8 03 02 24 88 EB 62 AC 14 80 03 3C FF 00 02 24`

### 9. 0x800D63B0 — COMPUTED — FUN_800d5bc0

- Store: `sw $v0, -0x6104($v1)`; word: `FC 9E 62 AC`.
- Asal nilai: Nilai 0xFF (255): 0x800D63AC `addiu $v0,$zero,0xff` tepat sebelum store.
- 12 instruksi sebelumnya:

  `0x800D6380 sb $a3, ($v0)
  0x800D6384 lui $v0, 0x8014
  0x800D6388 lw $v0, -0x158c($v0)
  0x800D638C addiu $v1, $zero, 0xff
  0x800D6390 sb $v1, 0x91d($v0)
  0x800D6394 lui $v0, 0x8014
  0x800D6398 sb $v1, -0x1468($v0)
  0x800D639C lui $v1, 0x8014
  0x800D63A0 addiu $v0, $zero, 0x3e8
  0x800D63A4 sw $v0, -0x1478($v1)
  0x800D63A8 lui $v1, 0x8014
  0x800D63AC addiu $v0, $zero, 0xff`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `00 00 47 A0 14 80 02 3C 74 EA 42 8C FF 00 03 24 1D 09 43 A0 14 80 02 3C 98 EB 43 A0 14 80 03 3C E8 03 02 24 88 EB 62 AC 14 80 03 3C FF 00 02 24`

### 10. 0x800D655C — COMPUTED — FUN_800d5bc0

- Store: `sw $v0, -0x6104($v1)`; word: `FC 9E 62 AC`.
- Asal nilai: Nilai 0xFF (255): 0x800D6558 `addiu $v0,$zero,0xff` tepat sebelum store.
- 12 instruksi sebelumnya:

  `0x800D652C sb $a3, ($v0)
  0x800D6530 lui $v0, 0x8014
  0x800D6534 lw $v0, -0x158c($v0)
  0x800D6538 addiu $v1, $zero, 0xff
  0x800D653C sb $v1, 0x91e($v0)
  0x800D6540 lui $v0, 0x8014
  0x800D6544 sb $v1, -0x1467($v0)
  0x800D6548 lui $v1, 0x8014
  0x800D654C addiu $v0, $zero, 0x3e8
  0x800D6550 sw $v0, -0x1474($v1)
  0x800D6554 lui $v1, 0x8014
  0x800D6558 addiu $v0, $zero, 0xff`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `00 00 47 A0 14 80 02 3C 74 EA 42 8C FF 00 03 24 1E 09 43 A0 14 80 02 3C 99 EB 43 A0 14 80 03 3C E8 03 02 24 8C EB 62 AC 14 80 03 3C FF 00 02 24`

### 11. 0x800D6708 — COMPUTED — FUN_800d5bc0

- Store: `sw $v0, -0x6104($v1)`; word: `FC 9E 62 AC`.
- Asal nilai: Nilai 0xFF (255): 0x800D6704 `addiu $v0,$zero,0xff` tepat sebelum store.
- 12 instruksi sebelumnya:

  `0x800D66D8 sb $a3, ($v0)
  0x800D66DC lui $v0, 0x8014
  0x800D66E0 lw $v0, -0x158c($v0)
  0x800D66E4 addiu $v1, $zero, 0xff
  0x800D66E8 sb $v1, 0x91f($v0)
  0x800D66EC lui $v0, 0x8014
  0x800D66F0 sb $v1, -0x1466($v0)
  0x800D66F4 lui $v1, 0x8014
  0x800D66F8 addiu $v0, $zero, 0x3e8
  0x800D66FC sw $v0, -0x1474($v1)
  0x800D6700 lui $v1, 0x8014
  0x800D6704 addiu $v0, $zero, 0xff`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `00 00 47 A0 14 80 02 3C 74 EA 42 8C FF 00 03 24 1F 09 43 A0 14 80 02 3C 9A EB 43 A0 14 80 03 3C E8 03 02 24 8C EB 62 AC 14 80 03 3C FF 00 02 24`

### 12. 0x800D6D68 — LAIN — FUN_800d5bc0

- Store: `sw $v0, -0x6104($a0)`; word: `FC 9E 82 AC`.
- Asal nilai: Sumber langsung `$v0` = `lbu $v0,($v0)` pada 0x800D6D60; alamat dibentuk dari base `0x8014-0x1468` dan indeks global `lw -0x1450($a2)`. Isi byte tabel TIDAK TAHU.
- 12 instruksi sebelumnya:

  `0x800D6D38 addiu $v0, $zero, 1
  0x800D6D3C sb $v0, 0x365($v1)
  0x800D6D40 lw $a1, -0x158c($s0)
  0x800D6D44 lui $a0, 0x8014
  0x800D6D48 lui $v1, 0x8014
  0x800D6D4C addiu $v1, $v1, -0x1468
  0x800D6D50 lui $a2, 0x8014
  0x800D6D54 lw $v0, -0x1450($a2)
  0x800D6D58 nop
  0x800D6D5C addu $v0, $v0, $v1
  0x800D6D60 lbu $v0, ($v0)
  0x800D6D64 nop`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `01 00 02 24 65 03 62 A0 74 EA 05 8E 14 80 04 3C 14 80 03 3C 98 EB 63 24 14 80 06 3C B0 EB C2 8C 00 00 00 00 21 10 43 00 00 00 42 90 00 00 00 00`

### 13. 0x800D7324 — LAIN — FUN_800d6e7c

- Store: `sw $v0, -0x6104($a2)`; word: `FC 9E C2 AC`.
- Asal nilai: Sumber langsung `$v0` = `lhu $v0,-0x1578($a1)` pada 0x800D731C. Field halfword di base global `0x8014`; arti field sebagai level/indeks gameplay TIDAK TAHU.
- 12 instruksi sebelumnya:

  `0x800D72F4 jal 0x80100d14
  0x800D72F8 move $a0, $zero
  0x800D72FC j 0x800d7e54
  0x800D7300 lui $v1, 0x8014
  0x800D7304 jal 0x80100f64
  0x800D7308 nop
  0x800D730C j 0x800d7e48
  0x800D7310 nop
  0x800D7314 lui $a2, 0x8014
  0x800D7318 lui $a1, 0x8014
  0x800D731C lhu $v0, -0x1578($a1)
  0x800D7320 nop`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `45 03 04 0C 21 20 00 00 95 5F 03 08 14 80 03 3C D9 03 04 0C 00 00 00 00 92 5F 03 08 00 00 00 00 14 80 06 3C 14 80 05 3C 88 EA A2 94 00 00 00 00`

### 14. 0x800D7910 — LAIN — FUN_800d6e7c

- Store: `sw $v0, -0x6104($a2)`; word: `FC 9E C2 AC`.
- Asal nilai: Sumber langsung `$v0` = `lhu $v0,-0x1578($a1)` pada 0x800D7908; pembacaan field global yang sama, makna gameplay TIDAK TAHU.
- 12 instruksi sebelumnya:

  `0x800D78E0 lbu $a0, 0xf($a0)
  0x800D78E4 jal 0x80100e68
  0x800D78E8 addiu $a0, $a0, 0x248
  0x800D78EC jal 0x80100dcc
  0x800D78F0 addiu $a0, $zero, 0xd4
  0x800D78F4 lui $v1, 0x8014
  0x800D78F8 j 0x800d7e08
  0x800D78FC addiu $v0, $zero, 0xa
  0x800D7900 lui $a2, 0x8014
  0x800D7904 lui $a1, 0x8014
  0x800D7908 lhu $v0, -0x1578($a1)
  0x800D790C nop`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `0F 00 84 90 9A 03 04 0C 48 02 84 24 73 03 04 0C D4 00 04 24 14 80 03 3C 82 5F 03 08 0A 00 02 24 14 80 06 3C 14 80 05 3C 88 EA A2 94 00 00 00 00`

### 15. 0x800DFA28 — COMPUTED — FUN_800df698

- Store: `sw $a0, -0x6104($s0)`; word: `FC 9E 04 AE`.
- Asal nilai: TIDAK TAHU: `$a0` berasal dari `$v0` pada 0x800DFA24 setelah `jal 0x80102408` (0x800DFA1C). Nilai return callee tidak terlihat pada window.
- 12 instruksi sebelumnya:

  `0x800DF9F8 addiu $a0, $zero, 7
  0x800DF9FC bnez $v0, 0x800dfed0
  0x800DFA00 lui $s1, 0x8014
  0x800DFA04 lui $v0, 0x8014
  0x800DFA08 lw $v0, -0x158c($v0)
  0x800DFA0C nop
  0x800DFA10 lw $v0, 0x370($v0)
  0x800DFA14 nop
  0x800DFA18 sw $v0, -0x1450($s1)
  0x800DFA1C jal 0x80102408
  0x800DFA20 lui $s0, 0x8014
  0x800DFA24 move $a0, $v0`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `07 00 04 24 34 01 40 14 14 80 11 3C 14 80 02 3C 74 EA 42 8C 00 00 00 00 70 03 42 8C 00 00 00 00 B0 EB 22 AE 02 09 04 0C 14 80 10 3C 21 20 40 00`

### 16. 0x800E82C8 — CLEAR — FUN_800e8190

- Store: `sw $zero, -0x6104($v0)`; word: `FC 9E 40 AC`.
- Asal nilai: CLEAR: store memakai `$zero`, sehingga nilai tertulis tepat 0.
- 12 instruksi sebelumnya:

  `0x800E8298 lw $a0, -0x158c($s0)
  0x800E829C lui $v0, 0x8014
  0x800E82A0 lhu $v1, -0x1578($v0)
  0x800E82A4 nop
  0x800E82A8 sll $v0, $v1, 3
  0x800E82AC addu $v0, $v0, $v1
  0x800E82B0 sll $v0, $v0, 4
  0x800E82B4 addu $v0, $a0, $v0
  0x800E82B8 lbu $a2, 0x1f($v0)
  0x800E82BC nop
  0x800E82C0 sw $a2, -0x1450($a1)
  0x800E82C4 lui $v0, 0x8014`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `74 EA 04 8E 14 80 02 3C 88 EA 43 94 00 00 00 00 C0 10 03 00 21 10 43 00 00 11 02 00 21 10 82 00 1F 00 46 90 00 00 00 00 B0 EB A6 AC 14 80 02 3C`

### 17. 0x800E8350 — COMPUTED — FUN_800e8190

- Store: `sw $v0, -0x6104($a1)`; word: `FC 9E A2 AC`.
- Asal nilai: Nilai register store = field yang dibaca lewat `lw $v0,-0x6104($a1)` pada 0x800E8344, lalu +1 pada 0x800E834C. Asal register base `$a1` belum dibuktikan dalam 12 instruksi ini.
- 12 instruksi sebelumnya:

  `0x800E8320 sll $v0, $v1, 3
  0x800E8324 addu $v0, $v0, $v1
  0x800E8328 sll $v0, $v0, 3
  0x800E832C addu $v0, $v0, $v1
  0x800E8330 sll $v0, $v0, 2
  0x800E8334 addu $v0, $v0, $a0
  0x800E8338 lbu $v1, 2($v0)
  0x800E833C nop
  0x800E8340 sw $v1, -0x1450($a2)
  0x800E8344 lw $v0, -0x6104($a1)
  0x800E8348 nop
  0x800E834C addiu $v0, $v0, 1`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `C0 10 03 00 21 10 43 00 C0 10 02 00 21 10 43 00 80 10 02 00 21 10 44 00 02 00 43 90 00 00 00 00 B0 EB C3 AC FC 9E A2 8C 00 00 00 00 01 00 42 24`

### 18. 0x800E8400 — COMPUTED — FUN_800e8190

- Store: `sw $v0, -0x6104($a1)`; word: `FC 9E A2 AC`.
- Asal nilai: Nilai register store = field yang dibaca lewat `lw $v0,-0x6104($a1)` pada 0x800E83F4, lalu +1 pada 0x800E83FC. Asal register base `$a1` belum dibuktikan dalam window.
- 12 instruksi sebelumnya:

  `0x800E83D0 sll $v0, $v1, 3
  0x800E83D4 addu $v0, $v0, $v1
  0x800E83D8 sll $v0, $v0, 3
  0x800E83DC addu $v0, $v0, $v1
  0x800E83E0 sll $v0, $v0, 2
  0x800E83E4 addu $v0, $v0, $a0
  0x800E83E8 lbu $v1, 1($v0)
  0x800E83EC nop
  0x800E83F0 sw $v1, -0x1450($a2)
  0x800E83F4 lw $v0, -0x6104($a1)
  0x800E83F8 nop
  0x800E83FC addiu $v0, $v0, 1`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `C0 10 03 00 21 10 43 00 C0 10 02 00 21 10 43 00 80 10 02 00 21 10 44 00 01 00 43 90 00 00 00 00 B0 EB C3 AC FC 9E A2 8C 00 00 00 00 01 00 42 24`

### 19. 0x800EA1D4 — COMPUTED — FUN_800ea18c

- Store: `sw $a2, -0x6104($s0)`; word: `FC 9E 06 AE`.
- Asal nilai: TIDAK TAHU: `$a2` disalin dari `$v0` pada 0x800EA1D0 setelah `jal 0x80102408` di 0x800EA1C8. Nilai return callee tidak dibuktikan.
- 12 instruksi sebelumnya:

  `0x800EA1A4 lui $v0, 0x8014
  0x800EA1A8 sb $zero, -0x1544($v0)
  0x800EA1AC lui $s2, 0x8014
  0x800EA1B0 lui $s1, 0x8014
  0x800EA1B4 lw $v0, -0x158c($s1)
  0x800EA1B8 nop
  0x800EA1BC lw $v0, 0x370($v0)
  0x800EA1C0 nop
  0x800EA1C4 sw $v0, -0x1450($s2)
  0x800EA1C8 jal 0x80102408
  0x800EA1CC lui $s0, 0x8014
  0x800EA1D0 move $a2, $v0`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `14 80 02 3C BC EA 40 A0 14 80 12 3C 14 80 11 3C 74 EA 22 8E 00 00 00 00 70 03 42 8C 00 00 00 00 B0 EB 42 AE 02 09 04 0C 14 80 10 3C 21 30 40 00`

### 20. 0x800EC9CC — CLEAR — FUN_800ec574

- Store: `sw $zero, -0x6104($v0)`; word: `FC 9E 40 AC`.
- Asal nilai: CLEAR: store memakai `$zero`, sehingga nilai tertulis tepat 0.
- 12 instruksi sebelumnya:

  `0x800EC99C addu $v1, $v1, $v0
  0x800EC9A0 lw $a1, 4($v1)
  0x800EC9A4 jal 0x8001387c
  0x800EC9A8 move $s3, $zero
  0x800EC9AC j 0x800ecd64
  0x800EC9B0 addiu $v0, $zero, 3
  0x800EC9B4 lbu $a0, 0x18($sp)
  0x800EC9B8 jal 0x8001552c
  0x800EC9BC nop
  0x800EC9C0 lui $v1, 0x8014
  0x800EC9C4 sw $v0, -0x1450($v1)
  0x800EC9C8 lui $v0, 0x8014`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `21 18 62 00 04 00 65 8C 1F 4E 00 0C 21 98 00 00 59 B3 03 08 03 00 02 24 18 00 A4 93 4B 55 00 0C 00 00 00 00 14 80 03 3C B0 EB 62 AC 14 80 02 3C`

### 21. 0x800ECA64 — COMPUTED — FUN_800ec574

- Store: `sw $v1, -0x6104($a2)`; word: `FC 9E C3 AC`.
- Asal nilai: Nilai terhitung: `v1 = field[-0x6104(a2)] + 1 + ((lhu 0x20(v1) >> 8) & 0xF)`. Terlihat dari load 0x800ECA50, increment 0x800ECA58, shift 0x800ECA4C, mask 0x800ECA5C, add 0x800ECA60; store tepat sesudahnya.
- 12 instruksi sebelumnya:

  `0x800ECA34 bne $v0, $t2, 0x800eca68
  0x800ECA38 nop
  0x800ECA3C lhu $a0, 0x20($v1)
  0x800ECA40 nop
  0x800ECA44 srl $v0, $a0, 0xc
  0x800ECA48 bne $t0, $v0, 0x800eca68
  0x800ECA4C srl $v0, $a0, 8
  0x800ECA50 lw $v1, -0x6104($a2)
  0x800ECA54 nop
  0x800ECA58 addiu $v1, $v1, 1
  0x800ECA5C andi $v0, $v0, 0xf
  0x800ECA60 addu $v1, $v1, $v0`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `0C 00 4A 14 00 00 00 00 20 00 64 94 00 00 00 00 02 13 04 00 07 00 02 15 02 12 04 00 FC 9E C3 8C 00 00 00 00 01 00 63 24 0F 00 42 30 21 18 62 00`

### 22. 0x800ECAE0 — LAIN — FUN_800ec574

- Store: `sw $v0, -0x6104($v1)`; word: `FC 9E 62 AC`.
- Asal nilai: TIDAK TAHU: provenance kosong; 12 instruksi sebelum store tidak mendefinisikan `$v0` secara lokal tanpa mengikuti cabang menuju join 0x800EC928.
- 12 instruksi sebelumnya:

  `0x800ECAB0 sw $v0, 0x4f4($a1)
  0x800ECAB4 addiu $v0, $zero, 1
  0x800ECAB8 j 0x800ec928
  0x800ECABC sb $v0, 0x534($a1)
  0x800ECAC0 lui $v0, 0x8014
  0x800ECAC4 lw $v0, -0x158c($v0)
  0x800ECAC8 j 0x800ec928
  0x800ECACC sb $zero, 0x534($v0)
  0x800ECAD0 lbu $a0, 0x18($sp)
  0x800ECAD4 jal 0x8001552c
  0x800ECAD8 addiu $s4, $zero, -1
  0x800ECADC lui $v1, 0x8014`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `F4 04 A2 AC 01 00 02 24 4A B2 03 08 34 05 A2 A0 14 80 02 3C 74 EA 42 8C 4A B2 03 08 34 05 40 A0 18 00 A4 93 4B 55 00 0C FF FF 14 24 14 80 03 3C`

### 23. 0x800EF67C — COMPUTED — FUN_800edd68

- Store: `sw $v0, -0x6104($v1)`; word: `FC 9E 62 AC`.
- Asal nilai: Nilai 1 pada jalur store: 0x800EF678 `addiu $v0,$zero,1` tepat sebelum store. Branch 0x800EF66C bisa melewati blok.
- 12 instruksi sebelumnya:

  `0x800EF64C sb $zero, 0x4ef($v0)
  0x800EF650 lui $v0, 0x8014
  0x800EF654 sb $v1, -0x613f($v0)
  0x800EF658 lui $v1, 0x8014
  0x800EF65C j 0x800ef988
  0x800EF660 addiu $v0, $zero, 0xb
  0x800EF664 lw $a0, -0x1450($v0)
  0x800EF668 nop
  0x800EF66C bnez $a0, 0x800ef7d4
  0x800EF670 lui $s0, 0x8014
  0x800EF674 lui $v1, 0x8014
  0x800EF678 addiu $v0, $zero, 1`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `EF 04 40 A0 14 80 02 3C C1 9E 43 A0 14 80 03 3C 62 BE 03 08 0B 00 02 24 B0 EB 44 8C 00 00 00 00 59 00 80 14 14 80 10 3C 14 80 03 3C 01 00 02 24`

### 24. 0x800F0490 — COMPUTED — FUN_800ef9a4

- Store: `sw $v0, -0x6104($a1)`; word: `FC 9E A2 AC`.
- Asal nilai: Nilai 1: 0x800F048C `addiu $v0,$zero,1` tepat sebelum store.
- 12 instruksi sebelumnya:

  `0x800F0460 addiu $v1, $v1, 1
  0x800F0464 sw $v1, -0x14f4($a0)
  0x800F0468 lui $v0, 0x8014
  0x800F046C lw $v0, -0x158c($v0)
  0x800F0470 nop
  0x800F0474 lbu $v0, 0x4a2($v0)
  0x800F0478 nop
  0x800F047C slt $v1, $v1, $v0
  0x800F0480 bnez $v1, 0x800f042c
  0x800F0484 nop
  0x800F0488 lui $a1, 0x8014
  0x800F048C addiu $v0, $zero, 1`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `01 00 63 24 0C EB 83 AC 14 80 02 3C 74 EA 42 8C 00 00 00 00 A2 04 42 90 00 00 00 00 2A 18 62 00 EA FF 60 14 00 00 00 00 14 80 05 3C 01 00 02 24`

### 25. 0x800F04BC — CLEAR — FUN_800ef9a4

- Store: `sw $zero, -0x6104($a1)`; word: `FC 9E A0 AC`.
- Asal nilai: CLEAR: store memakai `$zero`, sehingga nilai tertulis tepat 0.
- 12 instruksi sebelumnya:

  `0x800F048C addiu $v0, $zero, 1
  0x800F0490 sw $v0, -0x6104($a1)
  0x800F0494 lui $a0, 0x8014
  0x800F0498 lui $v0, 0x8014
  0x800F049C lw $v0, -0x158c($v0)
  0x800F04A0 nop
  0x800F04A4 lbu $v1, 0x4a2($v0)
  0x800F04A8 lw $v0, -0x145c($a0)
  0x800F04AC nop
  0x800F04B0 slt $v0, $v0, $v1
  0x800F04B4 beqz $v0, 0x800f04c0
  0x800F04B8 lui $v0, 0x8014`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `01 00 02 24 FC 9E A2 AC 14 80 04 3C 14 80 02 3C 74 EA 42 8C 00 00 00 00 A2 04 43 90 A4 EB 82 8C 00 00 00 00 2A 10 43 00 02 00 40 10 14 80 02 3C`

### 26. 0x800F0948 — LAIN — FUN_800ef9a4

- Store: `sw $v0, -0x6104($a3)`; word: `FC 9E E2 AC`.
- Asal nilai: Sumber langsung `$v0` = `lbu $v0,7($v0)` pada 0x800F0940 sesudah pointer tabel dihitung. Isi byte dan makna field TIDAK TAHU.
- 12 instruksi sebelumnya:

  `0x800F0918 sll $v0, $v1, 3
  0x800F091C addu $v0, $v0, $v1
  0x800F0920 sll $v0, $v0, 3
  0x800F0924 addu $v0, $v0, $v1
  0x800F0928 sll $v0, $v0, 2
  0x800F092C addu $v0, $v0, $a0
  0x800F0930 lui $a1, 0x8014
  0x800F0934 lw $v1, -0x1450($a1)
  0x800F0938 nop
  0x800F093C addu $v0, $v0, $v1
  0x800F0940 lbu $v0, 7($v0)
  0x800F0944 nop`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `C0 10 03 00 21 10 43 00 C0 10 02 00 21 10 43 00 80 10 02 00 21 10 44 00 14 80 05 3C B0 EB A3 8C 00 00 00 00 21 10 43 00 07 00 42 90 00 00 00 00`

### 27. 0x800F0B04 — LAIN — FUN_800ef9a4

- Store: `sw $v0, -0x6104($a2)`; word: `FC 9E C2 AC`.
- Asal nilai: Sumber langsung `$v0` = `lbu $v0,0x24($t2)` pada 0x800F0AFC. Isi byte dan semantik field TIDAK TAHU.
- 12 instruksi sebelumnya:

  `0x800F0AD4 sll $v0, $v0, 3
  0x800F0AD8 addu $v0, $v0, $v1
  0x800F0ADC sll $v0, $v0, 2
  0x800F0AE0 addu $v0, $v0, $a1
  0x800F0AE4 lw $v1, -0x6104($a2)
  0x800F0AE8 nop
  0x800F0AEC addu $v0, $v0, $v1
  0x800F0AF0 lbu $v0, 1($v0)
  0x800F0AF4 nop
  0x800F0AF8 sw $v0, -0x14f0($a3)
  0x800F0AFC lbu $v0, 0x24($t2)
  0x800F0B00 nop`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `C0 10 02 00 21 10 43 00 80 10 02 00 21 10 45 00 FC 9E C3 8C 00 00 00 00 21 10 43 00 01 00 42 90 00 00 00 00 10 EB E2 AC 24 00 42 91 00 00 00 00`

### 28. 0x800F1730 — COMPUTED — FUN_800f1290

- Store: `sw $v0, -0x6104($v1)`; word: `FC 9E 62 AC`.
- Asal nilai: Nilai 0x2710 (10.000): 0x800F172C `addiu $v0,$zero,0x2710` tepat sebelum store.
- 12 instruksi sebelumnya:

  `0x800F1700 beq $v1, $v0, 0x800f1714
  0x800F1704 lui $v1, 0x8014
  0x800F1708 lbu $v0, -0x60c1($v1)
  0x800F170C j 0x800f1718
  0x800F1710 addiu $v0, $v0, 1
  0x800F1714 addiu $v0, $zero, 0xa
  0x800F1718 j 0x800f236c
  0x800F171C sb $v0, -0x60c1($v1)
  0x800F1720 lui $v0, 0x8014
  0x800F1724 sw $zero, -0x1450($v0)
  0x800F1728 lui $v1, 0x8014
  0x800F172C addiu $v0, $zero, 0x2710`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `04 00 62 10 14 80 03 3C 3F 9F 62 90 C6 C5 03 08 01 00 42 24 0A 00 02 24 DB C8 03 08 3F 9F 62 A0 14 80 02 3C B0 EB 40 AC 14 80 03 3C 10 27 02 24`

### 29. 0x800F17A4 — LAIN — FUN_800f1290

- Store: `sw $v1, -0x6104($a0)`; word: `FC 9E 83 AC`.
- Asal nilai: Sumber langsung `$v1` = `lh $v1,8($s1)` pada 0x800F1784 (signed halfword struktur +8); semantik gameplay TIDAK TAHU.
- 12 instruksi sebelumnya:

  `0x800F1774 lw $a1, -0x14f4($s0)
  0x800F1778 jal 0x80015d24
  0x800F177C move $a2, $s1
  0x800F1780 lui $a0, 0x8014
  0x800F1784 lh $v1, 8($s1)
  0x800F1788 lw $v0, -0x6104($a0)
  0x800F178C nop
  0x800F1790 slt $v0, $v1, $v0
  0x800F1794 beqz $v0, 0x800f17a8
  0x800F1798 nop
  0x800F179C beqz $v1, 0x800f17a8
  0x800F17A0 nop`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `0C EB 05 8E 49 57 00 0C 21 30 20 02 14 80 04 3C 08 00 23 86 FC 9E 82 8C 00 00 00 00 2A 10 62 00 04 00 40 10 00 00 00 00 02 00 60 10 00 00 00 00`

### 30. 0x800F188C — COMPUTED — FUN_800f1290

- Store: `sw $v0, -0x6104($a2)`; word: `FC 9E C2 AC`.
- Asal nilai: Nilai = pembagian signed field `-0x6104($a2)` dengan 2 memakai koreksi tanda: `srl v1,v0,31; addu v0,v0,v1; sra v0,v0,1` pada 0x800F187C–0x800F1884. Store berada di delay-slot `j` 0x800F1888.
- 12 instruksi sebelumnya:

  `0x800F185C lw $v0, 4($v0)
  0x800F1860 nop
  0x800F1864 slt $v0, $v0, $v1
  0x800F1868 beqz $v0, 0x800f1874
  0x800F186C nop
  0x800F1870 sb $t2, 0x610($a0)
  0x800F1874 lw $v0, -0x6104($a2)
  0x800F1878 nop
  0x800F187C srl $v1, $v0, 0x1f
  0x800F1880 addu $v0, $v0, $v1
  0x800F1884 sra $v0, $v0, 1
  0x800F1888 j 0x800f18ac`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `04 00 42 8C 00 00 00 00 2A 10 43 00 02 00 40 10 00 00 00 00 10 06 8A A0 FC 9E C2 8C 00 00 00 00 C2 1F 02 00 21 10 43 00 43 10 02 00 2B C6 03 08`

### 31. 0x800F2554 — COMPUTED — FUN_800f2490

- Store: `sw $v0, -0x6104($v1)`; word: `FC 9E 62 AC`.
- Asal nilai: Nilai 0x2710 (10.000): 0x800F2550 `addiu $v0,$zero,0x2710` tepat sebelum store.
- 12 instruksi sebelumnya:

  `0x800F2524 sll $v0, $v1, 3
  0x800F2528 addu $v0, $v0, $v1
  0x800F252C sll $v0, $v0, 4
  0x800F2530 addu $a0, $a0, $v0
  0x800F2534 lhu $v0, 0xa($a0)
  0x800F2538 nop
  0x800F253C andi $v0, $v0, 0x100
  0x800F2540 beqz $v0, 0x800f2a68
  0x800F2544 lui $v0, 0x8014
  0x800F2548 sw $zero, -0x1450($v0)
  0x800F254C lui $v1, 0x8014
  0x800F2550 addiu $v0, $zero, 0x2710`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `C0 10 03 00 21 10 43 00 00 11 02 00 21 20 82 00 0A 00 82 94 00 00 00 00 00 01 42 30 49 01 40 10 14 80 02 3C B0 EB 40 AC 14 80 03 3C 10 27 02 24`

### 32. 0x800F25C0 — LAIN — FUN_800f2490

- Store: `sw $v1, -0x6104($a0)`; word: `FC 9E 83 AC`.
- Asal nilai: Sumber langsung `$v1` = `lh $v1,8($s1)` pada 0x800F25A8 (signed halfword struktur +8); semantik gameplay TIDAK TAHU.
- 12 instruksi sebelumnya:

  `0x800F2590 addu $a0, $a0, $v0
  0x800F2594 lbu $a0, 0xf($a0)
  0x800F2598 lw $a1, -0x14f4($s0)
  0x800F259C jal 0x80015d24
  0x800F25A0 move $a2, $s1
  0x800F25A4 lui $a0, 0x8014
  0x800F25A8 lh $v1, 8($s1)
  0x800F25AC lw $v0, -0x6104($a0)
  0x800F25B0 nop
  0x800F25B4 slt $v0, $v1, $v0
  0x800F25B8 beqz $v0, 0x800f25c4
  0x800F25BC nop`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `21 20 82 00 0F 00 84 90 0C EB 05 8E 49 57 00 0C 21 30 20 02 14 80 04 3C 08 00 23 86 FC 9E 82 8C 00 00 00 00 2A 10 62 00 02 00 40 10 00 00 00 00`

### 33. 0x800F2B38 — CLEAR — FUN_800f2a9c

- Store: `sw $zero, -0x6104($s0)`; word: `FC 9E 00 AE`.
- Asal nilai: CLEAR: store memakai `$zero`, sehingga nilai tertulis tepat 0.
- 12 instruksi sebelumnya:

  `0x800F2B08 sb $v0, -0x152c($v1)
  0x800F2B0C lui $v1, 0x8014
  0x800F2B10 lbu $v0, -0x60be($v1)
  0x800F2B14 nop
  0x800F2B18 addiu $v0, $v0, 1
  0x800F2B1C j 0x800f30e4
  0x800F2B20 sb $v0, -0x60be($v1)
  0x800F2B24 jal 0x80104e1c
  0x800F2B28 nop
  0x800F2B2C bnez $v0, 0x800f30e4
  0x800F2B30 lui $s0, 0x8014
  0x800F2B34 jal 0x80012ad0`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `D4 EA 62 A0 14 80 03 3C 42 9F 62 90 00 00 00 00 01 00 42 24 39 CC 03 08 42 9F 62 A0 87 13 04 0C 00 00 00 00 6D 01 40 14 14 80 10 3C B4 4A 00 0C`

### 34. 0x800F2B48 — COMPUTED — FUN_800f2a9c

- Store: `sw $v0, -0x6104($s0)`; word: `FC 9E 02 AE`.
- Asal nilai: Nilai 1 pada jalur store: 0x800F2B44 `addiu $v0,$zero,1` menjadi delay-slot branch 0x800F2B40; store pada jalur non-taken.
- 12 instruksi sebelumnya:

  `0x800F2B18 addiu $v0, $v0, 1
  0x800F2B1C j 0x800f30e4
  0x800F2B20 sb $v0, -0x60be($v1)
  0x800F2B24 jal 0x80104e1c
  0x800F2B28 nop
  0x800F2B2C bnez $v0, 0x800f30e4
  0x800F2B30 lui $s0, 0x8014
  0x800F2B34 jal 0x80012ad0
  0x800F2B38 sw $zero, -0x6104($s0)
  0x800F2B3C andi $v0, $v0, 0x1000
  0x800F2B40 beqz $v0, 0x800f2b4c
  0x800F2B44 addiu $v0, $zero, 1`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `01 00 42 24 39 CC 03 08 42 9F 62 A0 87 13 04 0C 00 00 00 00 6D 01 40 14 14 80 10 3C B4 4A 00 0C FC 9E 00 AE 00 10 42 30 02 00 40 10 01 00 02 24`

### 35. 0x800F3994 — CLEAR — FUN_800f3658

- Store: `sw $zero, -0x6104($v0)`; word: `FC 9E 40 AC`.
- Asal nilai: CLEAR: store memakai `$zero`, sehingga nilai tertulis tepat 0.
- 12 instruksi sebelumnya:

  `0x800F3964 jal 0x800cad18
  0x800F3968 lui $s0, 0x8014
  0x800F396C j 0x800f3980
  0x800F3970 sw $v0, -0x1450($s0)
  0x800F3974 lui $v1, 0x8014
  0x800F3978 addiu $v0, $zero, 0xff
  0x800F397C sw $v0, -0x1450($v1)
  0x800F3980 lui $v0, 0x8014
  0x800F3984 lw $v1, -0x1450($v0)
  0x800F3988 addiu $v0, $zero, 0xff
  0x800F398C beq $v1, $v0, 0x800f3a38
  0x800F3990 lui $v0, 0x8014`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `46 2B 03 0C 14 80 10 3C 60 CE 03 08 B0 EB 02 AE 14 80 03 3C FF 00 02 24 B0 EB 62 AC 14 80 02 3C B0 EB 43 8C FF 00 02 24 2A 00 62 10 14 80 02 3C`

### 36. 0x800F39F4 — COMPUTED — FUN_800f3658

- Store: `sw $v0, -0x6104($s3)`; word: `FC 9E 62 AE`.
- Asal nilai: Nilai 1 pada jalur store: 0x800F39F0 `addiu $v0,$zero,1` adalah delay-slot branch 0x800F39EC; jika branch taken ke 0x800F39B4, store dilewati.
- 12 instruksi sebelumnya:

  `0x800F39C4 lw $a0, -0x14f4($s0)
  0x800F39C8 nop
  0x800F39CC slti $v0, $a0, 0xb
  0x800F39D0 beqz $v0, 0x800f39fc
  0x800F39D4 lui $v0, 0x8014
  0x800F39D8 jal 0x8010be54
  0x800F39DC nop
  0x800F39E0 sw $v0, -0x144c($s2)
  0x800F39E4 lw $v1, -0x1450($s1)
  0x800F39E8 nop
  0x800F39EC bne $v0, $v1, 0x800f39b4
  0x800F39F0 addiu $v0, $zero, 1`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `0C EB 04 8E 00 00 00 00 0B 00 82 28 0A 00 40 10 14 80 02 3C 95 2F 04 0C 00 00 00 00 B4 EB 42 AE B0 EB 23 8E 00 00 00 00 F1 FF 43 14 01 00 02 24`

### 37. 0x800F3A48 — CLEAR — FUN_800f3658

- Store: `sw $zero, -0x6104($v0)`; word: `FC 9E 40 AC`.
- Asal nilai: CLEAR: store memakai `$zero`, sehingga nilai tertulis tepat 0.
- 12 instruksi sebelumnya:

  `0x800F3A18 j 0x800f3b14
  0x800F3A1C lui $v1, 0x8014
  0x800F3A20 lui $v0, 0x8014
  0x800F3A24 lw $a0, -0x144c($v0)
  0x800F3A28 jal 0x8010be90
  0x800F3A2C nop
  0x800F3A30 j 0x800f3b14
  0x800F3A34 lui $v1, 0x8014
  0x800F3A38 lui $v1, 0x8014
  0x800F3A3C addiu $v0, $zero, 0x14
  0x800F3A40 sw $v0, -0x1450($v1)
  0x800F3A44 lui $v0, 0x8014`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `C5 CE 03 08 14 80 03 3C 14 80 02 3C B4 EB 44 8C A4 2F 04 0C 00 00 00 00 C5 CE 03 08 14 80 03 3C 14 80 03 3C 14 00 02 24 B0 EB 62 AC 14 80 02 3C`

### 38. 0x800F3AA8 — LAIN — FUN_800f3658

- Store: `sw $v1, -0x6104($a0)`; word: `FC 9E 83 AC`.
- Asal nilai: Sumber langsung `$v1` = `lw $v1,-0x144c($s2)` pada 0x800F3A90; identitas/semantik field TIDAK TAHU.
- 12 instruksi sebelumnya:

  `0x800F3A78 lw $v0, -0x1450($s1)
  0x800F3A7C nop
  0x800F3A80 slt $v0, $v1, $v0
  0x800F3A84 beqz $v0, 0x800f3a90
  0x800F3A88 lui $a0, 0x8014
  0x800F3A8C sw $v1, -0x1450($s1)
  0x800F3A90 lw $v1, -0x144c($s2)
  0x800F3A94 lw $v0, -0x6104($a0)
  0x800F3A98 nop
  0x800F3A9C slt $v0, $v0, $v1
  0x800F3AA0 beqz $v0, 0x800f3aac
  0x800F3AA4 nop`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `B0 EB 22 8E 00 00 00 00 2A 10 62 00 02 00 40 10 14 80 04 3C B0 EB 23 AE B4 EB 43 8E FC 9E 82 8C 00 00 00 00 2A 10 43 00 02 00 40 10 00 00 00 00`

### 39. 0x800F3ADC — LAIN — FUN_800f3658

- Store: `sw $v0, -0x6104($s0)`; word: `FC 9E 02 AE`.
- Asal nilai: TIDAK TAHU: instruksi terakhir sebelum store adalah `jal 0x80035d78` di 0x800F3AD8; `$v0` dapat merupakan return helper/RNG tersebut. Nilai return dan relasinya ke store tidak dibuktikan.
- 12 instruksi sebelumnya:

  `0x800F3AAC lw $v0, -0x14f4($s0)
  0x800F3AB0 nop
  0x800F3AB4 addiu $v0, $v0, 1
  0x800F3AB8 sw $v0, -0x14f4($s0)
  0x800F3ABC slti $v0, $v0, 0xb
  0x800F3AC0 bnez $v0, 0x800f3a64
  0x800F3AC4 move $v1, $s0
  0x800F3AC8 lui $s0, 0x8014
  0x800F3ACC lw $v0, -0x6104($s0)
  0x800F3AD0 nop
  0x800F3AD4 addiu $v0, $v0, 1
  0x800F3AD8 jal 0x80035d78`
- Excerpt mentah 48 byte (maksimum diizinkan 64 B): `0C EB 02 8E 00 00 00 00 01 00 42 24 0C EB 02 AE 0B 00 42 28 E8 FF 40 14 21 18 00 02 14 80 10 3C FC 9E 02 8E 00 00 00 00 01 00 42 24 5E D7 00 0C`

## DR2 — manager +0x2EE

Recount: **25 akses = 22 WRITE + 3 READ**. Seluruh baris census berstatus `BASE_UNPROVEN`: instruksi dengan displacement +0x2EE terdeteksi, tetapi alias objek manager belum dikunci untuk masing-masing register base.

| # | Akses | PC | Fungsi | Instruksi | Word (excerpt 4 B) | Asal base / status |
|---:|---|---|---|---|---|---|
| 1 | WRITE | `0x800B24C8` | `FUN_800b1e88` | `sh $zero, 0x2ee($v0)` | `EE 02 40 A4` | LOAD_-0x158c; **BASE_UNPROVEN** |
| 2 | WRITE | `0x800B2EEC` | `FUN_800b2a58` | `sh $zero, 0x2ee($v0)` | `EE 02 40 A4` | LOAD_-0x158c; **BASE_UNPROVEN** |
| 3 | WRITE | `0x800B36BC` | `FUN_800b2a58` | `sh $zero, 0x2ee($v0)` | `EE 02 40 A4` | LOAD_-0x158c; **BASE_UNPROVEN** |
| 4 | WRITE | `0x800BEDA4` | `FUN_800be5d8` | `sh $zero, 0x2ee($v0)` | `EE 02 40 A4` | COMPUTED; **BASE_UNPROVEN** |
| 5 | WRITE | `0x800D1738` | `FUN_800d15a8` | `sh $zero, 0x2ee($v0)` | `EE 02 40 A4` | LOAD_-0x158c; **BASE_UNPROVEN** |
| 6 | WRITE | `0x800D1764` | `FUN_800d15a8` | `sh $zero, 0x2ee($v0)` | `EE 02 40 A4` | LOAD_-0x158c; **BASE_UNPROVEN** |
| 7 | WRITE | `0x800D46F8` | `FUN_800d15a8` | `sh $v0, 0x2ee($a0)` | `EE 02 82 A4` | COMPUTED; **BASE_UNPROVEN** |
| 8 | WRITE | `0x800DC4FC` | `FUN_800dc2e0` | `sh $v1, 0x2ee($v0)` | `EE 02 43 A4` | COMPUTED; **BASE_UNPROVEN** |
| 9 | READ | `0x800DCFE8` | `FUN_800dc2e0` | `lh $v0, 0x2ee($v0)` | `EE 02 42 84` | COMPUTED; **BASE_UNPROVEN** |
| 10 | WRITE | `0x800DD088` | `FUN_800dc2e0` | `sh $v1, 0x2ee($v0)` | `EE 02 43 A4` | COMPUTED; **BASE_UNPROVEN** |
| 11 | WRITE | `0x800DD178` | `FUN_800dc2e0` | `sh $v1, 0x2ee($v0)` | `EE 02 43 A4` | COMPUTED; **BASE_UNPROVEN** |
| 12 | WRITE | `0x800DFF64` | `FUN_800dfee8` | `sh $v0, 0x2ee($v1)` | `EE 02 62 A4` | COMPUTED; **BASE_UNPROVEN** |
| 13 | WRITE | `0x800E408C` | `FUN_800e3e74` | `sh $v0, 0x2ee($v1)` | `EE 02 62 A4` | COMPUTED; **BASE_UNPROVEN** |
| 14 | WRITE | `0x800E66E8` | `FUN_800e6470` | `sh $v1, 0x2ee($v0)` | `EE 02 43 A4` | COMPUTED; **BASE_UNPROVEN** |
| 15 | WRITE | `0x800E6A78` | `FUN_800e6470` | `sh $zero, 0x2ee($v0)` | `EE 02 40 A4` | COMPUTED; **BASE_UNPROVEN** |
| 16 | WRITE | `0x800E9E88` | `FUN_800e9220` | `sh $v1, 0x2ee($v0)` | `EE 02 43 A4` | COMPUTED; **BASE_UNPROVEN** |
| 17 | WRITE | `0x800EB400` | `FUN_800eb290` | `sh $v1, 0x2ee($v0)` | `EE 02 43 A4` | COMPUTED; **BASE_UNPROVEN** |
| 18 | WRITE | `0x800ECBB8` | `FUN_800ec574` | `sh $v0, 0x2ee($v1)` | `EE 02 62 A4` | COMPUTED; **BASE_UNPROVEN** |
| 19 | WRITE | `0x800ED6B8` | `FUN_800ec574` | `sh $zero, 0x2ee($v0)` | `EE 02 40 A4` | LOAD_-0x158c; **BASE_UNPROVEN** |
| 20 | WRITE | `0x800F0F08` | `FUN_800f0c10` | `sh $v0, 0x2ee($v1)` | `EE 02 62 A4` | COMPUTED; **BASE_UNPROVEN** |
| 21 | WRITE | `0x800F2CF8` | `FUN_800f2a9c` | `sh $v0, 0x2ee($a0)` | `EE 02 82 A4` | COMPUTED; **BASE_UNPROVEN** |
| 22 | WRITE | `0x800F2E38` | `FUN_800f2a9c` | `sh $v0, 0x2ee($a1)` | `EE 02 A2 A4` | COMPUTED; **BASE_UNPROVEN** |
| 23 | WRITE | `0x800F2E68` | `FUN_800f2a9c` | `sh $v0, 0x2ee($a0)` | `EE 02 82 A4` | COMPUTED; **BASE_UNPROVEN** |
| 24 | READ | `0x800F2E80` | `FUN_800f2a9c` | `lh $v0, 0x2ee($v0)` | `EE 02 42 84` | COMPUTED; **BASE_UNPROVEN** |
| 25 | READ | `0x800FAAEC` | `FUN_800faac8` | `lh $v0, 0x2ee($v1)` | `EE 02 62 84` | LOAD_-0x158c; **BASE_UNPROVEN** |

### Dua direct caller FUN_800EC574

| PC caller | Fungsi (heuristik) | Instruksi | Word (4 B) | 12 instruksi sebelum JAL |
|---|---|---|---|---|
| `0x800F3830` | `FUN_800f3658` | `jal 0x800ec574` | `5D B1 03 0C` | `0x800F3800 jal 0x800e87c0; 0x800F3804 nop; 0x800F3808 bnez $v0, 0x800f467c; 0x800F380C lui $v0, 0x8014; 0x800F3810 j 0x800f605c; 0x800F3814 nop; 0x800F3818 jal 0x800e9220; 0x800F381C nop; 0x800F3820 bnez $v0, 0x800f467c; 0x800F3824 lui $v0, 0x8014; 0x800F3828 j 0x800f605c; 0x800F382C nop` |
| `0x800F5D08` | `FUN_800f3658` | `jal 0x800ec574` | `5D B1 03 0C` | `0x800F5CD8 lw $v0, ($v1); 0x800F5CDC nop; 0x800F5CE0 jr $v0; 0x800F5CE4 nop; 0x800F5CE8 jal 0x800edd68; 0x800F5CEC nop; 0x800F5CF0 j 0x800f5d8c; 0x800F5CF4 lui $v0, 0x8014; 0x800F5CF8 jal 0x800eb434; 0x800F5CFC nop; 0x800F5D00 j 0x800f5d8c; 0x800F5D04 lui $v0, 0x8014` |

JAL keduanya mengarah tepat ke `0x800EC574`; label fungsi caller `FUN_800f3658` bersifat heuristic. Fungsi helper membaca index dari global, bukan argumen caller yang terbukti dalam window.

### Asal index dan skala 2

- `0x800ECB88`: lui $v0, 0x8014 — `14 80 02 3C`
- `0x800ECB8C`: lw $v1, -0x158c($v0) — `74 EA 43 8C`
- `0x800ECB90`: lui $v0, 0x8014 — `14 80 02 3C`
- `0x800ECB94`: lw $v0, -0x1450($v0) — `B0 EB 42 8C`
- `0x800ECB98`: nop — `00 00 00 00`
- `0x800ECB9C`: sll $v0, $v0, 1 — `40 10 02 00`
- `0x800ECBA0`: addu $v1, $v1, $v0 — `21 18 62 00`
- `0x800ECBA4`: lui $v0, 0x8014 — `14 80 02 3C`
- `0x800ECBA8`: lhu $v0, -0x6104($v0) — `FC 9E 42 94`
- `0x800ECBAC`: nop — `00 00 00 00`
- `0x800ECBB0`: negu $v0, $v0 — `23 10 02 00`
- `0x800ECBB4`: j 0x800ec928 — `4A B2 03 08`

Rantai helper: (1) 0x800ECB8C `lw $v1,-0x158c($v0)` dari `0x80140000` → pointer manager tersimpan di global `0x8013EA74`; (2) 0x800ECB94 `lw $v0,-0x1450($v0)` → selector halfword global `0x8013EBB0`; (3) 0x800ECB9C `sll $v0,$v0,1` → `idx×2`; (4) 0x800ECBA0 menjumlahkan offset itu ke manager base; (5) 0x800ECBB8 menulis ke `manager_base + 2×idx + 0x2EE`. Nilai yang ditulis berasal dari halfword `0x80139EFC` yang dibaca di 0x800ECBA8 lalu dinegasikan di 0x800ECBB0.

Untuk kedua caller 0x800F3830 dan 0x800F5D08, asal index ketika helper dipanggil adalah field global sama `0x8013EBB0`. Namun 12 instruksi sebelum masing-masing JAL tidak membuktikan siapa yang mengisi global tersebut pada path itu. **Setter upstream untuk caller pertama dan kedua: TIDAK TAHU.**

### Reader +0x2EE ke pengurangan Chakra

| PC | Fungsi | Instruksi | Status kaitan Chakra |
|---|---|---|---|
| `0x800DCFE8` | `FUN_800dc2e0` | `lh $v0,0x2ee($v0)` | **TIDAK TAHU** — aliran setelah load tidak ditautkan ke operasi pengurangan Chakra. |
| `0x800F2E80` | `FUN_800f2a9c` | `lh $v0,0x2ee($v0)` | **TIDAK TAHU** — perlu trace lintas cabang/fungsi. |
| `0x800FAAEC` | `FUN_800faac8` | `lh $v0,0x2ee($v1)` | **TIDAK TAHU** — perlu trace lintas cabang/fungsi. |

`DQ2_CHAKRA_READS_RAW.tsv` dan `DQ2_CHAKRA_SUBTRACTIONS_RAW.tsv` kosong: 0 load Chakra langsung dan 0 `subu` ber-taint Chakra di scan ini. Itu bukan bukti tidak ada pengurangan Chakra; linear taint tidak mencakup sepenuhnya indeks dinamis, alias pointer, maupun aliran lintas fungsi.

## DR3 — jalur lompat d>=2 dan fee

### Jalur yang terlihat / celah pembuktian

- **0x800ECB94–0x800ECB9C, `FUN_800ec574`**: mengambil selector `0x8013EBB0`, lalu mengalikannya secara skala indeks dengan shift 1-bit. Tidak ada current-level vs target-level compare dalam potongan itu.
- **0x800ECBA8–0x800ECBB8, `FUN_800ec574`**: membaca nilai yang sudah ada di `0x80139EFC`, menegasikannya, lalu menulis ke manager lane `+0x2EE`. Ini membuktikan transfer nilai global yang sudah ada, bukan pembentukan rumus fee.
- **0x800ECA3C–0x800ECA64, `FUN_800ec574`**: packed halfword `+0x20` diuji/diurai; field `-0x6104(a2)` dinaikkan 1 lalu ditambah nibble `((packed>>8)&0xF)`. Ini bukan bukti biaya `X×2^d`.
- **0x800CFF00–0x800CFF2C, `FUN_800cee18`**: increment/loop terlihat, tetapi store ke target memakai konstanta `0x2710`; tak ada rantai jarak level → fee.
- **0x800F1874–0x800F188C, `FUN_800f1290`**: field dibagi 2; tidak terbukti merupakan faktor fee yang terkait d.

Jalur lengkap **TIDAK TAHU**. Data statik tidak membuktikan satu rantai yang menghubungkan (1) perbandingan level sekarang vs target, (2) fee yang berubah menurut d, (3) store hasil akhir ke `0x80139EFC`. Status jalur ini K2 (indikasi/hipotesis, bukan bukti kode).

### Uji observasi X=120, fee dasar=100

Hipotesis terbatas: **untuk d>=2, fee=X×2^d**. Tiga titik dalam domain d>=2 tersedia; tidak ada fitting parameter dari kurang dari tiga titik.

| Transisi | d | Observasi | Prediksi X×2^d | Kesesuaian H>=2 |
|---|---:|---:|---:|---|
| LV1→LV2 | 1 | 100 | 200 | Di luar domain; formula universal **TIDAK COCOK** |
| LV1→LV3 | 2 | 400 | 400 | **COCOK** |
| LV1→LV4 | 3 | 800 | 800 | **COCOK** |
| LV1→LV5 | 4 | 1600 | 1600 | **COCOK** |

Tiga pengamatan d>=2 konsisten dengan hipotesis. LV1→LV2=100 menggugurkan versi universal semua d, tetapi tidak menguji hipotesis terbatas d>=2.

**Falsifier:** satu pengukuran terkontrol pada d>=2 dengan X diketahui dan fee aktual ≠ X×2^d menggugurkan H>=2. Secara statik, jalur terverifikasi yang membentuk fee konstan/linear atau pengali lain lalu menulisnya ke `0x80139EFC` juga menggugurkan hipotesis.

## Koreksi status run 42013037160

Log job menyatakan `RAW_INPUT_STAGE=PASS`, analisis `EXIT_CODE=0`, dan `PRIVATE_BINARY_CLEANUP=PASS`. Workflow membaca seluruh file stage-status multi-baris sebagai satu string, lalu membandingkannya dengan literal satu baris `RAW_INPUT_STAGE=PASS`. File berisi metadata tambahan, sehingga string keseluruhan tidak sama dengan literal: summary yang dibuat workflow menjadi INCOMPLETE secara keliru. Penyebabnya bug agregasi status, bukan kegagalan ekstraksi/analisis/cleanup.

`ACTIONS_RUN_SUMMARY.txt` diperbaiki ke **STATUS=PASS**, exit code 0, disertai alasan koreksi. Run telah selesai; tidak ada run baru atau emulator yang dijalankan. Tidak ada biner privat/ISO/BIOS/savestate/dump/video/frame yang dikomit.

## Batasan dan sumber

- EXE dan DATA.BIN Entry 1 digunakan hanya sementara pada runner untuk raw-byte run; identitas SHA disimpan dalam laporan sumber asli; biner tidak di-commit.
- Entry 1 static base `0x800AD450`; runtime mapping belum tervalidasi.
- 39 writer adalah kandidat aligned raw store; indirect/dynamic alias dan pemisahan kode/data belum tuntas.
- Sumber primer: `DQ1B_GLOBAL_80139EFC_WRITERS_RAW.tsv`, `DQ2_MANAGER_2EE_READ_WRITE_RAW.tsv`, `DQ2_FUN_800EC574_DIRECT_CALLERS_RAW.tsv`, `DQ2_FUN_800EC574_RAW_WINDOW.tsv`, `DQ2_CHAKRA_READS_RAW.tsv`, `DQ2_CHAKRA_SUBTRACTIONS_RAW.tsv`, `DQ3_USER_OBSERVATION_FORMULA_CHECK.tsv`.