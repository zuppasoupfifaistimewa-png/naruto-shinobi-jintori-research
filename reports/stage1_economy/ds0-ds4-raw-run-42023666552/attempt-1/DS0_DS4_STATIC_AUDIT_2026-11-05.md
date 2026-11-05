# DS0–DS4 — audit statis raw-byte (koreksi independen)

Tanggal: 2026-11-05. Proyek: Naruto Shinobi no Sato no Jintori Gassen, SLPS-03553.
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research.
Baseline inklusif: c6204f38495c9be76b18c76a9943f17ca835f2f3.
Snapshot HEAD untuk penghitungan DS0: 88663e7549a6e819b7fe631a4cb903b1eded8c87 (HEAD main sebelum commit koreksi dokumen ini).

## Status keseluruhan

- Mode statis saja; tidak ada emulator yang dijalankan.
- Tidak ada ISO, EXE, DATA.BIN, BIOS, savestate, dump, video, atau frame yang dikomit.
- Batas bukti statis maksimum K4; tidak ada klaim K5.
- Run Actions 42023666552: STATUS=PASS, JOB=raw-static-ds0-ds4, JOB_ID=127232405018, SOURCE_SHA=96e03675286f7b7999eee4549f3b6a71a1765c47, EXIT_CODE=0. Rincian mentah ada di ACTIONS_RUN_SUMMARY.txt. Ini menyatakan status job, bukan bukti runtime permainan.

## DS0 — hitung ulang commit inklusif

GitHub compare dari baseline c6204f... sampai snapshot 88663e... menghasilkan ahead_by=2 dan behind_by=0. Karena baseline ikut dihitung: TOTAL=3, MANUSIA=2, BOT=1.

Rincian setiap commit, klasifikasi, pesan dan daftar berkas yang berubah tercatat di DS0_COMMIT_LEDGER.tsv. Hasil ini berbeda dari ledger yang dibuat run: pada konfigurasi saat itu DS0_AUDIT_HEAD diisi sama dengan DS0_BASELINE, sehingga script hanya menulis satu baris baseline. Hitung ulang ini memakai riwayat Git dari baseline sampai snapshot HEAD yang disebutkan di atas, bukan angka summary lama.

### Berkas berubah per commit dalam rentang

1. c6204f38495c9be76b18c76a9943f17ca835f2f3 — manusia:
   - reports/stage1_economy/dq1-dq3-raw-run-42013037160/attempt-1/ACTIONS_RUN_SUMMARY.txt
   - reports/stage1_economy/dq1-dq3-raw-run-42013037160/attempt-1/DR0_DR3_CORRECTIVE_AUDIT_2026-11-05.md

2. 96e03675286f7b7999eee4549f3b6a71a1765c47 — manusia:
   - .github/workflows/dq1-dq3-raw-static.yml
   - tools/stage1/RunDS0DS4Raw.py

3. 88663e7549a6e819b7fe631a4cb903b1eded8c87 — bot:
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/ACTIONS_RUN_SUMMARY.txt
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS0_COMMIT_LEDGER.tsv
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS0_DS4_STATIC_AUDIT_2026-11-05.md
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS0_SUMMARY.txt
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS1_INDEX_ORIGIN_TRACE.tsv
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS1_PRELOAD_12_RAW.tsv
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS1_TABLE_ADDRESS_TRACE.tsv
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS1_TABLE_POINTER_GLOBAL_WRITERS.tsv
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS2_FUN_80102408_CALLERS.tsv
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS2_FUN_80102408_RAW_DISASSEMBLY.tsv
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS2_FUN_80102408_RETURN_PATHS.tsv
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS2_FUN_80102408_SUMMARY.txt
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS2_FUN_80102408_UNRESOLVED_EDGES.tsv
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS3_FUN_800F3658_PRECALL_CONTEXT.tsv
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS3_INDEX_GLOBAL_READS.tsv
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS3_INDEX_GLOBAL_WRITERS.tsv
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS4_LEVEL_FEE_CANDIDATE_WINDOWS.tsv
   - reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS4_USER_HYPOTHESIS_POINT_TESTS.tsv

## DS1 — writer 0x80139EFC pada FUN_800D15A8

PC utama: 0x800D2480, file offset Entry 1 = 0x10E0030. Fungsi berlabel FUN_800d15a8 (nama/boundary mengikuti label fungsi pada artefak).
Instruksi store: sw $v1, -0x6104($v0), byte mentah FC 9E 43 AC. Basis $v0 pada konteks ini adalah 0x80140000, sehingga alamat efektif store adalah 0x80139EFC. Store ada pada delay slot J 0x800d25e4 di PC 0x800D247C; jalur branch di 0x800D2474 menentukan apakah blok tersebut dicapai.

### Asal indeks, pointer tabel dan stride

- PC 0x800D2448, FUN_800d15a8: lw $v1, -0x1450($v0). Dengan $v0=0x80140000, sumber indeks adalah global word 0x8013EBB0. Nilai indeks runtime: TIDAK TAHU; tidak ada snapshot runtime yang diizinkan/dikomit.
- PC 0x800D2450, FUN_800d15a8: lw $a0, -0x157c($v0). Alamat slot pointer = 0x8013EA84.
- Dua writer slot pointer yang terdeteksi:
  - PC 0x800B1F38, FUN_800b1e88 (heuristik): sw $v0,-0x157c($v1), bytes 84 EA 62 AC. $v0 dibentuk oleh 0x800B1F30 lui $v0,0x8014 dan 0x800B1F34 addiu $v0,$v0,-0x47e8, sehingga alamat yang disimpan adalah 0x8013B818.
  12 instruksi sebelumnya: 0x800B1F08 addiu $a0,$zero,0x7d8; 0x800B1F0C sw $v0,-0x1540($s0); 0x800B1F10 jal 0x8002dec4; 0x800B1F14 addiu $a0,$zero,0x2d4; 0x800B1F18 sw $v0,-0x1550($s1); 0x800B1F1C lui $s1,0x8014; 0x800B1F20 jal 0x8002dec4; 0x800B1F24 addiu $a0,$zero,0x950; 0x800B1F28 sw $v0,-0x158c($s1); 0x800B1F2C lui $v1,0x8014; 0x800B1F30 lui $v0,0x8014; 0x800B1F34 addiu $v0,$v0,-0x47e8.
  Excerpt mentah 48 byte: D8 07 04 24 C0 EA 02 AE B1 B7 00 0C D4 02 04 24 B0 EA 22 AE 14 80 11 3C B1 B7 00 0C 50 09 04 24 74 EA 22 AE 14 80 03 3C 14 80 02 3C 18 B8 42 24.
  - PC 0x800B2AC8, FUN_800b2a58 (heuristik): sw $v0,-0x157c($v1), bytes 84 EA 62 AC. $v0 dibentuk oleh 0x800B2AC0 lui $v0,0x8014 dan 0x800B2AC4 addiu $v0,$v0,-0x47e8, sehingga alamat yang disimpan juga 0x8013B818.
  12 instruksi sebelumnya: 0x800B2A98 sw $v0,-0x1540($s0); 0x800B2A9C lui $s0,0x8014; 0x800B2AA0 jal 0x8002dec4; 0x800B2AA4 addiu $a0,$zero,0x2d4; 0x800B2AA8 sw $v0,-0x1550($s0); 0x800B2AAC lui $s2,0x8014; 0x800B2AB0 jal 0x8002dec4; 0x800B2AB4 addiu $a0,$zero,0x950; 0x800B2AB8 sw $v0,-0x158c($s2); 0x800B2ABC lui $v1,0x8014; 0x800B2AC0 lui $v0,0x8014; 0x800B2AC4 addiu $v0,$v0,-0x47e8.
  Excerpt mentah 48 byte: C0 EA 02 AE 14 80 10 3C B1 B7 00 0C D4 02 04 24 B0 EA 02 AE 14 80 12 3C B1 B7 00 0C 50 09 04 24 74 EA 42 AE 14 80 03 3C 14 80 02 3C 18 B8 42 24.
- Basis pointer tabel statis = 0x8013B818. Slot yang menyimpan pointer tersebut = 0x8013EA84.
- Offset statis pointer dalam Entry 1 = 0x8E3C8; offset file DATA.BIN = 0x11493C8. Ini memakai rumus yang diberikan: 0x10BB000 + (0x8013B818 - 0x800AD450). Pemetaan runtime tetap tidak tervalidasi.
- Perhitungan alamat pada PC 0x800D2454–0x800D2468:
  sll idx,3; addu +idx; sll hasil,3; addu +idx; sll hasil,2; hasil akhir = idx × 292 = idx × 0x124.
- Alamat byte tabel yang dibaca = 0x8013B818 + 0x124 × idx. Stride terbukti 0x124 byte.
- Isi byte tabel pada alamat tersebut: TIDAK TAHU. Artefak run menyimpan instruksi pembentuk alamat tetapi tidak menyimpan bytes DATA.BIN pada offset 0x11493C8 dan rentang berikutnya. Tidak ada nilai isi tabel yang boleh disimpulkan dari instruksi saja.

### 12 instruksi sebelum load byte di 0x800D246C

0x800D2450  lw $a0, -0x157c($v0)
0x800D2454  sll $v0, $v1, 3
0x800D2458  addu $v0, $v0, $v1
0x800D245C  sll $v0, $v0, 3
0x800D2460  addu $v0, $v0, $v1
0x800D2464  sll $v0, $v0, 2
0x800D2468  addu $v0, $v0, $a0
0x800D246C  lbu $v1, ($v0)
0x800D2470  addiu $v0, $zero, 1
0x800D2474  bne $v1, $v0, 0x800d25e4
0x800D2478  lui $v0, 0x8014
0x800D247C  j 0x800d25e4

Excerpt mentah 48 byte (12 word, tidak melebihi 64 B):
84 EA 44 8C C0 10 03 00 21 10 43 00 C0 10 02 00 21 10 43 00 80 10 02 00 21 10 44 00 00 00 43 90 01 00 02 24 5B 00 62 14 14 80 02 3C 79 49 03 08

PC 0x800D2480 adalah delay slot dari J pada 0x800D247C. Branch 0x800D2474 hanya melanjutkan ke J/store bila hasil lbu di 0x800D246C sama dengan 1; karena itu, jika PC 0x800D2480 dieksekusi, nilai yang disimpan ke 0x80139EFC terbukti 1. Isi byte aktual untuk setiap indeks/tabel yang tidak ditempuh tetap TIDAK TAHU karena raw table bytes tidak dipersistenkan.

## DS2 — FUN_80102408

Direct JAL census berisi 25 pemanggilan ke 0x80102408. Semua PC caller dan 12 instruksi sebelum JAL tercatat di DS2_FUN_80102408_CALLERS.tsv. CFG mengunjungi 9 instruksi inti; delay slot branch/jr pada PC 0x80102420 dan 0x8010242C adalah NOP dan dicatat sebagai slot terpisah pada raw disassembly terkoreksi. Delay slot return PC 0x80102430 adalah PC 0x80102434, tetapi byte/instruksinya tidak ada pada artefak yang dipersistenkan.

### Disassembly mentah reachable

0x80102408  14 80 02 3C  lui $v0, 0x8014
0x8010240C  2C A2 43 8C  lw $v1, -0x5dd4($v0)
0x80102410  00 00 00 00  nop
0x80102414  04 00 62 8C  lw $v0, 4($v1)
0x80102418  00 00 00 00  nop
0x8010241C  04 00 40 10  beqz $v0, 0x80102430
0x80102420  00 00 00 00  nop (delay slot)
0x80102424  A8 0E 62 8C  lw $v0, 0xea8($v1)
0x80102428  08 00 E0 03  jr $ra
0x8010242C  00 00 00 00  nop (delay slot)
0x80102430  08 00 E0 03  jr $ra

PC 0x80102434 adalah delay slot untuk jr pada PC 0x80102430; TIDAK TAHU karena instruksi itu tidak tercatat di DS2_FUN_80102408_RAW_DISASSEMBLY.tsv. File offset PC 0x80102408 yang terverifikasi = 0x110FFB8; semua offset lain mengikuti + (PC - 0x80102408).

### Nilai return per jalur

- Return PC 0x80102428: TIDAK TAHU. $v0 diisi dari lw $v0,0xea8($v1) pada PC 0x80102424; isi word manager+0xea8 bergantung data, bukan konstanta statis.
- Return PC 0x80102430: TIDAK TAHU. Analisis run awal menulis 0xFFFFFFFF sebagai return, tetapi delay-slot jr pada PC 0x80102434 tidak dipersistenkan sehingga klaim konstanta itu tidak dapat diverifikasi dari artefak raw yang tersimpan. Label lama KONSTANTA_TERBUKTI diturunkan menjadi TIDAK TAHU sampai instruksi slot tersedia.
- Global pointer manager dibaca melalui slot 0x8013A22C (lui 0x8014 lalu lw -0x5dd4). PC 0x80102414 membaca field +4; PC 0x80102424 membaca +0xea8 pada jalur nonzero. Nilai kedua load: TIDAK TAHU.

### Kaitannya dengan 39 kandidat writer 0x80139EFC

Tiga writer yang secara langsung menunjukkan jalur call-return FUN_80102408 dalam window 12 instruksi:
- PC 0x800D09C8, FUN_800d05b8: jal 0x80102408 pada 0x800D09BC; 0x800D09C4 move $a0,$v0; store pada 0x800D09C8 memakai $a0. Nilai return yang masuk ke store: TIDAK TAHU.
  12 instruksi: 0x800D0998 j 0x800d0f9c; 0x800D099C nop; 0x800D09A0 lui $s1,0x8014; 0x800D09A4 lui $v0,0x8014; 0x800D09A8 lw $v0,-0x158c($v0); 0x800D09AC nop; 0x800D09B0 lw $v0,0x370($v0); 0x800D09B4 nop; 0x800D09B8 sw $v0,-0x1450($s1); 0x800D09BC jal 0x80102408; 0x800D09C0 lui $s0,0x8014; 0x800D09C4 move $a0,$v0.
- PC 0x800DFA28, FUN_800df698: jal 0x80102408 pada 0x800DFA1C; 0x800DFA24 move $a0,$v0; store menggunakan $a0. Nilai return: TIDAK TAHU.
  12 instruksi: 0x800DF9F8 addiu $a0,$zero,7; 0x800DF9FC bnez $v0,0x800dfed0; 0x800DFA00 lui $s1,0x8014; 0x800DFA04 lui $v0,0x8014; 0x800DFA08 lw $v0,-0x158c($v0); 0x800DFA0C nop; 0x800DFA10 lw $v0,0x370($v0); 0x800DFA14 nop; 0x800DFA18 sw $v0,-0x1450($s1); 0x800DFA1C jal 0x80102408; 0x800DFA20 lui $s0,0x8014; 0x800DFA24 move $a0,$v0.
- PC 0x800EA1D4, FUN_800ea18c: jal 0x80102408 pada 0x800EA1C8; 0x800EA1D0 move $a2,$v0; store menggunakan $a2. Nilai return: TIDAK TAHU.
  12 instruksi: 0x800EA1A4 lui $v0,0x8014; 0x800EA1A8 sb $zero,-0x1544($v0); 0x800EA1AC lui $s2,0x8014; 0x800EA1B0 lui $s1,0x8014; 0x800EA1B4 lw $v0,-0x158c($s1); 0x800EA1B8 nop; 0x800EA1BC lw $v0,0x370($v0); 0x800EA1C0 nop; 0x800EA1C4 sw $v0,-0x1450($s2); 0x800EA1C8 jal 0x80102408; 0x800EA1CC lui $s0,0x8014; 0x800EA1D0 move $a2,$v0.

Dua writer tambahan yang disebut dalam premis "lima penulis": TIDAK TAHU; tidak ada dua baris tambahan dalam 39-row DQ1B TSV yang dapat dihubungkan langsung secara raw dengan hasil FUN_80102408. Dua call-return serupa yang memang terlihat adalah 0x800D5128 -> store selector pada 0x800D5130 dan 0x800D5748 -> store selector pada 0x800D5750; kedua store itu mengisi global indeks 0x8013EBB0, bukan global fee 0x80139EFC. Jadi keduanya bukan bukti dua writer fee tambahan.

## DS3 — global indeks 0x8013EBB0

Census statis mengidentifikasi 144 kandidat writer dan 149 reader langsung. DS3_INDEX_GLOBAL_WRITERS.tsv berisi untuk setiap writer: PC, fungsi, register sumber, value_origin spesifik, instruksi store, 12 instruksi sebelumnya dan excerpt hex 48 byte (maksimum yang diminta 64 B). Kategori asal langsung: 70 KONSTANTA, 39 HASIL_OPERASI_DI_PC, 16 HASIL_LOAD_DI_PC, 19 HASIL_RETURN_CALL. Untuk load/call yang bergantung data, nilai numerik aktual per PC = TIDAK TAHU; origin tag menunjukkan titik sumber, bukan nilai runtime. Label fungsi mayoritas nearest-JAL/prologue heuristic, bukan seluruhnya boundary fungsi yang diverifikasi.

Contoh untuk dua call-return yang terkait dengan index global:
- PC 0x800D5130, FUN_800d15a8: sw $v0,-0x1450($s0); asal CALL_RETURN_AT_0x800D5128; 12-instruksi/excerpt tersedia di DS3_INDEX_GLOBAL_WRITERS.tsv.
- PC 0x800D5750, FUN_800d15a8: sw $v0,-0x1450($s0); asal CALL_RETURN_AT_0x800D5748; 12-instruksi/excerpt tersedia di TSV yang sama.

### Helper FUN_800EC574: asal indeks dan penggunaan skala 2

Raw window:
- 0x800ECB88: lui $v0,0x8014 — 14 80 02 3C
- 0x800ECB8C: lw $v1,-0x158c($v0) — 74 EA 43 8C; manager pointer dari slot 0x8013EA74
- 0x800ECB90: lui $v0,0x8014 — 14 80 02 3C
- 0x800ECB94: lw $v0,-0x1450($v0) — B0 EB 42 8C; membaca global indeks 0x8013EBB0
- 0x800ECB98: nop — 00 00 00 00
- 0x800ECB9C: sll $v0,$v0,1 — 40 10 02 00
- 0x800ECBA0: addu $v1,$v1,$v0 — 21 18 62 00
- 0x800ECBA4: lui $v0,0x8014 — 14 80 02 3C
- 0x800ECBA8: lhu $v0,-0x6104($v0) — FC 9E 42 94; mengambil halfword fee global 0x80139EFC
- 0x800ECBAC: nop — 00 00 00 00
- 0x800ECBB0: negu $v0,$v0 — 23 10 02 00
- 0x800ECBB4: j 0x800ec928 — 4A B2 03 08
- PC 0x800ECBB8 (store pada jalur lanjut) menulis nilai negasi ke manager_base + 2×idx + 0x2EE.

### Instruksi sebelum dua JAL dari FUN_800F3658 ke FUN_800EC574

PC 0x800F3830, byte JAL 5D B1 03 0C:
0x800F3800 jal 0x800e87c0
0x800F3804 nop
0x800F3808 bnez $v0,0x800f467c
0x800F380C lui $v0,0x8014 (delay slot)
0x800F3810 j 0x800f605c
0x800F3814 nop
0x800F3818 jal 0x800e9220
0x800F381C nop
0x800F3820 bnez $v0,0x800f467c
0x800F3824 lui $v0,0x8014 (delay slot)
0x800F3828 j 0x800f605c
0x800F382C nop

Excerpt 48 byte:
F0 A1 03 0C 00 00 00 00 9C 03 40 14 14 80 02 3C 17 D8 03 08 00 00 00 00 88 A4 03 0C 00 00 00 00 96 03 40 14 80 02 3C 17 D8 03 08 00 00 00 00

Catatan alur: J di 0x800F3810 atau 0x800F3828 menghentikan fall-through pada cabang terkait. Jadi daftar di atas adalah 12 instruksi berurutan sebelum call, bukan klaim bahwa semua instruksi dilewati pada satu eksekusi linear. JAL 0x800F3830 hanya dieksekusi bila kontrol mencapai PC itu dari jalur lain.

PC 0x800F5D08, byte JAL 5D B1 03 0C:
0x800F5CD8 lw $v0,($v1)
0x800F5CDC nop
0x800F5CE0 jr $v0
0x800F5CE4 nop
0x800F5CE8 jal 0x800edd68
0x800F5CEC nop
0x800F5CF0 j 0x800f5d8c
0x800F5CF4 lui $v0,0x8014 (delay slot)
0x800F5CF8 jal 0x800eb434
0x800F5CFC nop
0x800F5D00 j 0x800f5d8c
0x800F5D04 lui $v0,0x8014 (delay slot)

Excerpt 48 byte:
00 00 62 8C 00 00 00 00 08 00 40 00 00 00 00 00 5A B7 03 0C 00 00 00 00 63 D7 03 08 14 80 02 3C 0D AD 03 0C 00 00 00 00 63 D7 03 08 14 80 02 3C

Catatan alur: JR register pada 0x800F5CE0 adalah indirect jump; instruksi setelahnya bukan bukti fall-through yang normal. J di 0x800F5CF0 dan 0x800F5D00 juga mengalihkan flow. Label FUN_800f3658 untuk caller di file bersifat heuristic.

## DS4 — jalur biaya lompat d>=2

Status rantai lengkap current-level vs target-level → fee → store ke 0x80139EFC: TIDAK TAHU.

### Fragmen statis yang ditemukan

1. PC 0x800ECA3C (FUN_800ec574): lhu $a0,0x20($v1), byte 20 00 64 94. PC 0x800ECA44: srl $v0,$a0,0xc; PC 0x800ECA48: bne $t0,$v0,0x800eca68; PC 0x800ECA4C: srl $v0,$a0,8; PC 0x800ECA5C: andi $v0,$v0,0xf. Arti packed halfword dan nilai $t0 dalam konteks level sekarang/target: TIDAK TAHU.
2. PC 0x800ECA50 membaca global fee lama melalui lw $v1,-0x6104($a2); PC 0x800ECA58 addiu $v1,$v1,1; PC 0x800ECA5C mengekstrak nibble; PC 0x800ECA60 addu $v1,$v1,$v0; PC 0x800ECA64 menyimpan $v1 ke global 0x80139EFC menurut census alamat efektif DQ1B. Fragmen ini menunjukkan pola update bersyarat dari nilai lama ditambah 1 dan nibble. Hubungan nibble dengan d tidak terbukti.
   Excerpt 48 byte:
   0C 00 4A 14 00 00 00 00 20 00 64 94 00 00 00 00 02 13 04 00 07 00 02 15 02 12 04 00 FC 9E C3 8C 00 00 00 00 01 00 63 24 0F 00 42 30 21 18 62 00
3. PC 0x800ECAA0: mult $a0,$v0 (18 00 82 00); PC 0x800ECAA4: mflo $v0 (12 10 00 00); PC 0x800ECAA8: sw $v0,0x4f0($a1) (F0 04 A2 AC). Dalam window yang sama $a0 di-load dari global indeks 0x8013EBB0 dan $v0 dari global fee 0x80139EFC; produk masuk ke manager +0x4F0. Tidak terbukti bahwa $a0 adalah d atau hasil ini adalah pembentuk fee global.
   Excerpt 48 byte:
   01 00 42 24 0C EB A2 AC 2A 10 47 00 E3 FF 40 14 00 00 00 00 14 80 02 3C 74 EA 45 8C 14 80 02 3C 14 80 03 3C B0 EB 44 8C FC 9E 62 8C 00 00 00 00
4. PC 0x800ECB94–0x800ECBB8 membaca indeks 0x8013EBB0, mengalikan skala indeks 2, mengambil nilai yang sudah ada di 0x80139EFC, menegasikannya dan menaruhnya ke manager lane +0x2EE. Ini bukti transfer/penggunaan nilai fee yang sudah ada, bukan bukti rumus yang membentuk nilainya.

### Uji H1 dan H2 terhadap observasi pengguna (hipotesis, bukan fakta game)

fee_dasar = 100.

| d | Observasi pengguna (hipotesis) | H1: fee_dasar × 2^d | H1 | H2: multiplier lookup | H2: fee_dasar × multiplier | H2 |
|---:|---:|---:|---|---:|---:|---|
| 2 | 400 | 400 | COCOK | 4 | 400 | COCOK |
| 3 | 800 | 800 | COCOK | 8 | 800 | COCOK |
| 4 | 1600 | 1600 | COCOK | 16 | 1600 | COCOK |

- H1: fee = fee_dasar × 2^d untuk d>=2. Falsifier: satu uji terkontrol pada d>=2 dengan fee_dasar diketahui menghasilkan fee selain nilai tersebut; secara statis, aliran data yang membuktikan faktor bukan 2^d atau operand bukan d juga menggugurkan H1.
- H2: multiplier diambil dari tabel menurut d, dengan kandidat multiplier 4, 8, 16 untuk d=2,3,4. Falsifier: raw data-flow membuktikan tidak ada lookup menurut d, atau lookup/observasi terkontrol menghasilkan multiplier berbeda.
- Ketiga titik d=2,3,4 diuji tanpa fitting parameter dari kurang dari tiga titik. H1 dan H2 sama-sama cocok 3/3 dan belum dapat dibedakan.
- Tidak ada bukti kode yang menghubungkan level sekarang, target, d dan pembentukan nilai akhir 0x80139EFC. Tetap TIDAK TAHU.

## Batas bukti

- DS1 stride dan alur pointer/index adalah bukti statis instruksi. Isi tabel byte, indeks aktual dan runtime mapping: TIDAK TAHU.
- DS2 nilai return bergantung pada data yang dibaca; return kedua juga membutuhkan byte delay slot yang tidak tersimpan. Nilai kedua return: TIDAK TAHU.
- DS3 144/149 adalah census kandidat aligned raw word/read dalam mapping yang digunakan. Writer via pointer alias/dynamic yang tidak tertangkap scanner: TIDAK TAHU.
- DS4 fragmen fee ditemukan, tetapi relasi gameplay-nya dengan jarak level d belum tertaut; H1/H2 tetap hipotesis.
- Nama fungsi selain target JAL yang pasti adalah heuristik nearest-JAL/prologue; jangan perlakukan seluruhnya sebagai boundary terverifikasi.

## Berkas koreksi yang dibuat setelah snapshot DS0

Commit koreksi dokumen setelah snapshot 88663e mengubah:
- reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS0_COMMIT_LEDGER.tsv
- reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS0_SUMMARY.txt
- reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS0_DS4_STATIC_AUDIT_2026-11-05.md
- reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS2_FUN_80102408_RAW_DISASSEMBLY.tsv
- reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS2_FUN_80102408_RETURN_PATHS.tsv
- reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS2_FUN_80102408_SUMMARY.txt

Commit koreksi ini berada setelah snapshot dan tidak dihitung pada TOTAL=3 DS0 di atas.


### Errata sesudah commit koreksi pertama (di luar snapshot DS0)

Commit errata berikutnya mengubah hanya dua berkas:
- reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS0_COMMIT_LEDGER.tsv
- reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS0_DS4_STATIC_AUDIT_2026-11-05.md

Errata ini membetulkan path tabel pointer DS1 di ledger dan menambahkan excerpt raw 12-instruksi untuk kedua writer slot pointer. Kedua commit koreksi berada setelah snapshot 88663e dan tidak mengubah hitungan DS0=3.


### Koreksi akhir path ledger

Pada validasi permalink, path DS1_TABLE_POINTER_GLOBAL_WRITERS.tsv di kolom changed_files ledger masih tertinggal di direktori lama. Path diperbaiki ke direktori ds0-ds4-raw-run-42023666552/attempt-1. Berkas yang diubah pada commit koreksi path ini:
- reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS0_COMMIT_LEDGER.tsv
- reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS0_DS4_STATIC_AUDIT_2026-11-05.md

Koreksi ini pasca-snapshot dan tidak mengubah rentang atau hasil hitung DS0.


### Errata akhir DS1 — nilai store bersyarat

Pembacaan ulang branch 0x800D2474 menunjukkan bahwa PC 0x800D2480 hanya terjadi bila byte lbu sama dengan 1. Jadi nilai store pada jalur tersebut adalah 1; yang belum diketahui adalah isi byte tabel untuk indeks-indeks lain dan apakah jalur store itu tercapai pada runtime. Berkas yang diubah pada errata akhir ini:
- reports/stage1_economy/ds0-ds4-raw-run-42023666552/attempt-1/DS0_DS4_STATIC_AUDIT_2026-11-05.md
