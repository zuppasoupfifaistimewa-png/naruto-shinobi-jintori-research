# AS1–AS3 audit report — Naruto Jintori Stage 1 economy

Tanggal pemeriksaan: 31 Oktober 2026  
Produk: Naruto – Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)  
Repository: \`zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research\`  
Checkpoint yang diberikan: \`5f026f9b2f97275ff427b022ab6a4e2156d3d503\`

## Ringkasan status

| Tugas | Status | Kesimpulan / batas |
|---|---|---|
| AS1(a) commit ledger | SELESAI | Dua descendant baru sejak checkpoint ditelusuri; commit AQ1 lama \`e05e454\` ditambahkan ke ledger sebagai commit terlewat |
| AS1(b) hitung ulang FIELD | SELESAI — K4 statis | 1.188 baris; dua WRITE \`s8\` dipertahankan terpisah dari \`fp\` |
| AS1(c) fungsi xref / scope | SELESAI — K4 statis | 98 xref fungsi cocok dengan metadata; 93 FIELD record-xref + 4 helper/caller scope; lima xref lainnya tidak punya FIELD pada displacement yang dipindai |
| AS1(d) 14 setter caller | SELESAI — K4 statis | 10 memakai participant slot EA74 / stride 0x90; 4 manager/getter path; 0 terbukti mengambil argumen a1 dari tile-record EA84 / stride 0x124 |
| AS2 getter call-site | SELESAI — K4 statis | Kedua call berada di FUN_801052E8; return v0 pertama diuji tanda, return v0 kedua diteruskan sebagai a2 |
| AS3 K0/K1/K2 | IN_PROGRESS saat pemeriksaan terakhir | Run 41211621962, job 124567642157 masih berjalan; hash RAM, exit code, wall time, Memory Card after-SHA, dan putusan beda hash: TIDAK TAHU sampai output final tersedia |

Skala K0–K5 tetap berlaku. Static disassembly/Ghidra tidak dinaikkan di atas K4. K5 untuk AS3 belum diberikan: enam peluncuran belum menghasilkan keluaran final yang dapat diaudit pada saat laporan status ini dibuat.

## 1. Checkpoint, commit ledger, dan berkas

### Checkpoint dan descendant

HEAD \`main\` saat tugas dimulai adalah \`5f026f9b2f97275ff427b022ab6a4e2156d3d503\`. Pada pemeriksaan awal tidak ada descendant sesudah checkpoint. Dua commit kemudian dibuat untuk persiapan eksperimen dan hasil AQ1 statis:

**\`8894686395afdca97328a9fb2af5007a29406584\` — Add AS1 AS2 deep Ghidra export and AS3 H6 K0 K1 K2 A/B**
- \`.github/workflows/as3-h6-breakpoint-ab.yml\` (baru)
- \`.github/workflows/step7-entry1-buffer-base-audit.yml\` (diubah)
- \`experiments/as3_h6_breakpoint_ab.py\` (baru)
- \`tools/step7/ExportStage1EconomyDeepContext.java\` (baru)

**\`27f4ae7212a839e6f00d5158ec4996282c03ee7a\` — Publish AQ1 static economy census run 41211621969**
- \`reports/stage1_economy/aq1-run-41211621969/attempt-1/ACTIONS_RUN_SUMMARY.txt\` (baru)
- \`reports/stage1_economy/aq1-run-41211621969/attempt-1/aq1-deep-context.tsv\` (baru)
- \`reports/stage1_economy/aq1-run-41211621969/attempt-1/aq1-economy-census.tsv\` (baru)
- \`reports/stage1_economy/aq1-run-41211621969/attempt-1/aq1-recount.txt\` (baru)
- \`reports/stage1_economy/aq1-run-41211621969/attempt-1/input-identity.txt\` (baru)
- \`reports/stage1_economy/aq1-run-41211621969/attempt-1/run-summary.txt\` (baru)

### Commit AQ1 terlewat yang diminta

\`e05e45401ec58410019bc96448b93c86fa2560cf\` — \`Publish AQ1 static economy census run 41208394883\`. Commit ini sudah ada sebelum checkpoint 5f, jadi bukan descendant baru, tetapi memang terlewat dari ledger yang diminta. Lima berkasnya:
- \`reports/stage1_economy/aq1-run-41208394883/attempt-1/ACTIONS_RUN_SUMMARY.txt\`
- \`reports/stage1_economy/aq1-run-41208394883/attempt-1/aq1-economy-census.tsv\`
- \`reports/stage1_economy/aq1-run-41208394883/attempt-1/aq1-recount.txt\`
- \`reports/stage1_economy/aq1-run-41208394883/attempt-1/input-identity.txt\`
- \`reports/stage1_economy/aq1-run-41208394883/attempt-1/run-summary.txt\`

## 2. AS1 — census FIELD, alias register, dan function xref

### 2.1 Identitas dan jumlah census

AQ1 statis selesai dengan:
- Actions run: \`41211621969\`
- Job ID: \`124567642021\`
- Job: \`Analyze verified Entry 1 slice at 0x800AD450\`
- Status: completed / success
- Exit code: \`0\`
- Source SHA: \`8894686395afdca97328a9fb2af5007a29406584\`
- Entry 1 DATA.BIN slice: offset \`0x10BB000\`, size \`596,412\` byte
- SHA-256 slice: \`9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a\`
- Static import candidate: \`0x800AD450\`; runtime mapping tetap belum tervalidasi.
- Game/emulator dijalankan: tidak.
- Gameplay input dikirim: tidak.

### 2.2 Hitung ulang 1.188 baris

Seluruh baris \`FIELD\` pada \`aq1-economy-census.tsv\` dihitung ulang. Rincian per displacement, semua register base digabung:

| Offset | READ | WRITE | OTHER | Total |
|---|---:|---:|---:|---:|
| +0x00 | 582 | 107 | 17 | 706 |
| +0x0B | 10 | 2 | 0 | 12 |
| +0x20 | 354 | 111 | 5 | 470 |
| **Total** | **946** | **220** | **22** | **1.188** |

Rincian register base:
- \`sp\`: 135 (READ 81, WRITE 53, OTHER 1)
- \`v0\`: 535 (448, 79, 8)
- \`v1\`: 237 (189, 42, 6)
- \`a0\`: 170 (140, 24, 6)
- \`a1\`: 37 (28, 9, 0)
- \`a2\`: 22 (17, 5, 0)
- \`s1\`: 22 (20, 1, 1)
- \`s0\`: 13 (12, 1, 0)
- \`a3\`: 8 (8, 0, 0)
- \`t0\`: 3 (1, 2, 0)
- \`t2\`: 2 (1, 1, 0)
- \`s8\`: 2 (0, 2, 0)
- \`t7\`: 1 (0, 1, 0)
- \`s4\`: 1 (1, 0, 0)
- \`gp\`: 0; \`fp\`: 0.

Alias tidak disatukan: dua operand \`sb v0,0x0(s8)\` adalah:
- PC \`0x800CAE4C\`, function \`0x800CADB8\`
- PC \`0x800CB46C\`, function \`0x800CADB8\`

Keduanya adalah WRITE pada +0x00 dan dihitung sebagai \`s8\`, bukan \`fp\`. Total tetap 1.188. Scanner sendiri mencatat displacement sebagai kandidat; angka ini bukan bukti bahwa semua operand alias ke pointer runtime yang sama.

### 2.3 Daftar 93 fungsi FUNCTION_XREF_RECORD_SLOT

Ekspor Ghidra menghasilkan 98 fungsi xref record-slot berbeda, sesuai \`recordFns_count=98\` dan 98 baris \`RECORD_XREF_FUNCTION\` pada TSV. Dari daftar itu, 93 fungsi juga mempunyai akses displacement FIELD yang dipindai (+0x00/+0x0B/+0x20):

\`\`\`text
0x800B2A58 FUN_800b2a58
0x800B54F4 FUN_800b54f4
0x800B5790 FUN_800b5790
0x800B5D68 FUN_800b5d68
0x800B63F4 FUN_800b63f4
0x800B6B24 FUN_800b6b24
0x800B770C FUN_800b770c
0x800B78E4 FUN_800b78e4
0x800B83FC FUN_800b83fc
0x800B94E8 FUN_800b94e8
0x800B9E30 FUN_800b9e30
0x800BA9F8 FUN_800ba9f8
0x800BB004 FUN_800bb004
0x800BB36C FUN_800bb36c
0x800BB5D8 FUN_800bb5d8
0x800BBC1C FUN_800bbc1c
0x800BBE54 FUN_800bbe54
0x800BD114 FUN_800bd114
0x800BD938 FUN_800bd938
0x800BDA08 FUN_800bda08
0x800BDAB8 FUN_800bdab8
0x800BDC4C FUN_800bdc4c
0x800BDEAC FUN_800bdeac
0x800BE0E4 FUN_800be0e4
0x800BE464 FUN_800be464
0x800C0784 FUN_800c0784
0x800C0A00 FUN_800c0a00
0x800C2570 FUN_800c2570
0x800C4388 FUN_800c4388
0x800C815C FUN_800c815c
0x800C88F0 FUN_800c88f0
0x800CADB8 FUN_800cadb8
0x800CEE18 FUN_800cee18
0x800D05B8 FUN_800d05b8
0x800D10F0 FUN_800d10f0
0x800D15A8 FUN_800d15a8
0x800D5BC0 FUN_800d5bc0
0x800D6E7C FUN_800d6e7c
0x800D7F38 FUN_800d7f38
0x800D8930 FUN_800d8930
0x800D9570 FUN_800d9570
0x800DB29C FUN_800db29c
0x800DC2E0 FUN_800dc2e0
0x800DD7C0 FUN_800dd7c0
0x800DE760 FUN_800de760
0x800DF0C8 FUN_800df0c8
0x800DFEE8 FUN_800dfee8
0x800E0298 FUN_800e0298
0x800E0324 FUN_800e0324
0x800E03B0 FUN_800e03b0
0x800E0B3C FUN_800e0b3c
0x800E2E8C FUN_800e2e8c
0x800E3540 FUN_800e3540
0x800E3E74 FUN_800e3e74
0x800E4F50 FUN_800e4f50
0x800E5350 FUN_800e5350
0x800E5E0C FUN_800e5e0c
0x800E6DA4 FUN_800e6da4
0x800E70C8 FUN_800e70c8
0x800E7B38 FUN_800e7b38
0x800E8190 FUN_800e8190
0x800E87C0 FUN_800e87c0
0x800E9220 FUN_800e9220
0x800EA18C FUN_800ea18c
0x800EB434 FUN_800eb434
0x800EC574 FUN_800ec574
0x800EDD68 FUN_800edd68
0x800EF9A4 FUN_800ef9a4
0x800F0C10 FUN_800f0c10
0x800F1290 FUN_800f1290
0x800F1CCC FUN_800f1ccc
0x800F2050 FUN_800f2050
0x800F2490 FUN_800f2490
0x800F32B4 FUN_800f32b4
0x800F3658 FUN_800f3658
0x800F6988 FUN_800f6988
0x800F6EC4 FUN_800f6ec4
0x800F7450 FUN_800f7450
0x800F7824 FUN_800f7824
0x800F7ADC FUN_800f7adc
0x800FA4C8 FUN_800fa4c8
0x800FAAC8 FUN_800faac8
0x800FAEBC FUN_800faebc
0x800FB340 FUN_800fb340
0x800FB80C FUN_800fb80c
0x800FC340 FUN_800fc340
0x800FC700 FUN_800fc700
0x800FCA0C FUN_800fca0c
0x800FD730 FUN_800fd730
0x800FE314 FUN_800fe314
0x800FEA28 FUN_800fea28
0x800FEC20 FUN_800fec20
0x800FF00C FUN_800ff00c
\`\`\`

Empat fungsi HELPER_OR_CALLER_SCOPE yang terpisah:
- \`0x800CB4B4 FUN_800cb4b4\`
- \`0x800CCA18 FUN_800cca18\`
- \`0x800CD678 FUN_800cd678\`
- \`0x800CF434 FUN_800cf434\`

Lima fungsi lain dari 98 xref metadata tidak memiliki FIELD baris pada tiga displacement yang dihitung:
- \`0x800BBD9C FUN_800bbd9c\`
- \`0x800F6DB0 FUN_800f6db0\`
- \`0x800FAD68 FUN_800fad68\`
- \`0x800FB1D0 FUN_800fb1d0\`
- \`0x800FB598 FUN_800fb598\`

Jadi angka 98 metadata direkonsiliasi sebagai daftar 98 xref fungsi; 93 di antaranya memiliki akses FIELD yang masuk census, sedangkan empat helper/caller FIELD di atas berada di luar daftar 98 tersebut. Lima xref sisanya tidak menjadi FIELD rows. Hasil ini K4 statis, bukan bukti runtime.

## 3. AS1(d) — 14 setter call-sites: participant vs tile record vs manager

Setter langsung adalah \`jal 0x8001387C\`. Ke-14 call-site:
- \`0x800B41B0\` — \`FUN_800B2A58\`
- \`0x800B4254\` — \`FUN_800B2A58\`
- \`0x800B4F00\` — \`FUN_800B2A58\`
- \`0x800B4F64\` — \`FUN_800B2A58\`
- \`0x800B6238\` — \`FUN_800B5D68\`
- \`0x800BEC98\` — \`FUN_800BE5D8\`
- \`0x800DEB38\` — \`FUN_800DE760\`
- \`0x800E1BE0\` — \`FUN_800E1958\`
- \`0x800EC9A4\` — \`FUN_800EC574\`
- \`0x800F95E8\` — \`FUN_800F9520\`
- \`0x8010A15C\` — \`FUN_80109FEC\`
- \`0x8010A1B0\` — \`FUN_80109FEC\`
- \`0x8010A638\` — \`FUN_80109FEC\`
- \`0x8010A97C\` — \`FUN_80109FEC\`

### 3.1 Participant pointer slot EA74 dan stride 0x90

Sepuluh call-site pertama pada kelompok participant adalah:
\`0x800B41B0\`, \`0x800B4254\`, \`0x800B4F00\`, \`0x800B4F64\`, \`0x800B6238\`, \`0x800BEC98\`, \`0x800DEB38\`, \`0x800E1BE0\`, \`0x800EC9A4\`, \`0x800F95E8\`.

Pointer slot \`0x8013EA74\` dibaca sebagai \`lw ..., -0x158C(base=0x80140000)\`. Contoh formula stride participant:
\`\`\`asm
sll   v0,index,0x3
addu  v0,v0,index
sll   v0,v0,0x4
\`\`\`
Ini adalah \`(index*8 + index)*16 = index*0x90\`. Contoh pada \`FUN_800B5D68\`:
\`\`\`asm
800B6110 sll   v0,s2,0x3
800B6114 addu  v0,v0,s2
800B6118 sll   s1,v0,0x4
...
800B6228 lw    v0,-0x158c(s3)
800B622C nop
800B6230 addu  v0,v0,s1
800B6234 lw    a1,0x4(v0)
800B6238 jal   0x8001387c
800B623C _move a0,s2
\`\`\`
Contoh pada \`FUN_800B2A58\`:
\`\`\`asm
800B4164 lw    a0,-0x158c(s0)
800B416C lw    v1,0x598(a0)
800B4174 sll   v0,v1,0x3
800B4178 addu  v0,v0,v1
800B417C sll   v0,v0,0x4
800B4180 addiu a1,a0,0x4
800B4184 addu  v0,a1,v0
...
800B41A8 addu  a1,a1,v0
800B41AC lw    a1,0x0(a1)
800B41B0 jal   0x8001387c
\`\`\`
Dua call-site di 0x800B4F00/4F64 juga membaca dari participant base \`a0\` yang diambil di 0x800B4EA4 melalui slot EA74; index array memakai pola ×0x90.

### 3.2 Tile record pointer slot EA84 dan stride 0x124

Tile-record pointer berbeda: slot \`0x8013EA84\`, dibaca sebagai \`lw ..., -0x157C(base=0x80140000)\`. Contoh di \`FUN_800B2A58\`, instruksi \`0x800B2ACC\` menyimpan pointer tile-record pada slot tersebut. Formula stride tile-record yang benar-benar terlihat:
\`\`\`asm
800B3F08 lw    a0,-0x157c(s0)
800B3F0C sll   v0,s2,0x3
800B3F10 addu  v0,v0,s2
800B3F14 sll   v0,v0,0x3
800B3F18 addu  v0,v0,s2
800B3F1C sll   v0,v0,0x2
800B3F20 addu  a0,v0,a0
\`\`\`
Perhitungannya: \`(index*9)*8 + index = index*73\`, lalu \`*4 = index*292 = index*0x124\`.

Pembedaan penting: instruksi \`sh zero,0x124(v0)\` hanyalah displacement +0x124 pada suatu record, bukan bukti stride array. Bukti stride adalah rantai shift/add di atas.

**Tidak ada dari 14 setter call-site yang terbukti mengambil final argumen \`a1\` dari tile-record pointer EA84 dengan stride 0x124.** Ada penggunaan tile-record array pada jalur lain dalam fungsi yang sama, tetapi argumen setter yang diperiksa berasal dari participant pointer, atau manager/getter. Kedekatan instruksi tile-record di fungsi yang sama bukan bukti bahwa itu sumber a1 setter.

### 3.3 Empat setter manager pada FUN_80109FEC

Manager pointer berada pada slot \`0x8013A554 = 0x80140000 - 0x5AAC\`. Empat call-site dan final \`a1\`:

| Setter PC | Sumber final a1 |
|---|---|
| \`0x8010A15C\` | hasil getter \`v0\` + manager field \`+0xB44\` |
| \`0x8010A1B0\` | hasil getter \`v0\` langsung |
| \`0x8010A638\` | hasil getter \`v0\` + manager field \`+0xB44\` |
| \`0x8010A97C\` | hasil getter \`v0\` langsung |

Kutipan instruksi:
\`\`\`asm
8010A144 jal   0x800138ec
8010A154 lw    a1,0xb44(v1)
8010A15C jal   0x8001387c
8010A160 _addu a1,v0,a1

8010A1A4 jal   0x800138ec
8010A1AC move  a0,s0
8010A1B0 jal   0x8001387c
8010A1B4 _move a1,v0

8010A610 lw    s1,0xb44(v0)
8010A624 jal   0x800138ec
8010A634 lbu   a0,0xb2b(v1)
8010A638 jal   0x8001387c
8010A63C _addu a1,v0,s1

8010A970 jal   0x800138ec
8010A978 move  a0,s0
8010A97C jal   0x8001387c
8010A980 _move a1,v0
\`\`\`
Dua call-site memakai manager field +0xB44; dua lainnya memakai return getter langsung. Ini adalah deskripsi asal operand a1 saja. Nama/peran ekonomi (build, upgrade, income, release) TIDAK TAHU.

## 4. AS2 — dua getter 0x800138EC dari FUN_801052E8

Kedua call-site berada dalam fungsi \`FUN_801052E8\`, entry \`0x801052E8\`.

### 4.1 Getter call PC 0x801053C4

Dua belas instruksi sebelum jal:
\`\`\`asm
80105394 addu  a0,v0,a0
80105398 lh    a0,0x48(sp)
8010539C lh    a1,0x4a(sp)
801053A0 lw    v0,-0x5aac(s1)
801053A4 nop
801053A8 addu  v0,v0,s0
801053AC lh    a2,0x1b4(v0)
801053B0 addiu a0,a0,0x8
801053B4 addiu a1,a1,0x8
801053B8 addiu a2,a2,0x1000
801053BC jal   0x80105bcc
801053C0 _move a3,s5
\`\`\`
Getter dipanggil di \`0x801053C4\`, delay slot di \`0x801053C8: _move a0,s3\`, lalu return address \`0x801053CC\`. Penggunaan langsung pertama hasil getter \`v0\` adalah:
\`\`\`asm
801053CC bltz v0,0x80105414
\`\`\`
Jadi return getter pertama diuji tanda (negative/non-negative) oleh branch tersebut.

### 4.2 Getter call PC 0x80105418

Dua belas instruksi sebelum jal:
\`\`\`asm
801053E8 sll   a0,v0,0x3
801053EC addu  v0,a1,a0
801053F0 lw    v1,0x478(v0)
801053F4 li    v0,0x1
801053F8 bne   v1,v0,0x80105418
801053FC _clear s0
80105400 addu  v0,a1,a0
80105404 lh    v0,0x474(v0)
80105408 nop
8010540C blez  v0,0x80105418
80105410 _nop
80105414 li    s0,0x20
\`\`\`
Getter dipanggil di \`0x80105418\`, delay slot \`0x8010541C _move a0,s3\`, return address \`0x80105420\`. Sesudah return:
\`\`\`asm
80105420 lh    a0,0x48(sp)
80105424 lh    a1,0x4a(sp)
80105428 sw    s0,0x10(sp)
8010542C sw    s5,0x14(sp)
80105430 li    v1,0x1
80105434 sw    v1,0x18(sp)
80105438 addiu a0,a0,0x20
8010543C addiu a1,a1,0x10
80105440 move  a2,v0
80105444 jal   0x8001b364
80105448 _li   a3,0x5
\`\`\`
Return \`v0\` dari getter kedua dipindahkan menjadi \`a2\` untuk pemanggilan \`0x8001B364\`.

### 4.3 Mengapa a1 pada getter kedua bernilai 0x801CEF08

Static source:
\`\`\`asm
801053D0 lui v0,0x8014
801053D4 lw  a1,-0x5aac(v0)
...
80105418 jal 0x800138ec
\`\`\`
\`lui v0,0x8014\` membentuk basis \`0x80140000\`; \`lw a1,-0x5AAC(v0)\` membaca manager pointer dari slot \`0x8013A554\`. Tidak ada instruksi penulis \`a1\` antara load tersebut dan getter kedua, sehingga nilainya tetap hidup sampai call. Runtime AR3 sebelumnya mencatat \`a1=0x801CEF08\` pada return PC \`0x80105420\` (180 event per peluncuran). Nilai konkret 0x801CEF08 dengan demikian didukung oleh pengamatan runtime terdahulu dan konsisten dengan sumber statis; nilai ini bukan hasil menebak label fungsi.

Tidak diberikan label build/upgrade/income/release karena instruksi yang diaudit tidak membuktikannya.

## 5. AS3 — H6 hybrid K0/K1/K2 runtime status

### 5.1 Run dan preflight

- Actions run: \`41211621962\`
- Job ID: \`124567642157\`
- Job: \`K0/K1/K2 six-launch H6 breakpoint comparison\`
- Source SHA: \`8894686395afdca97328a9fb2af5007a29406584\`
- H6 SHA-256: \`d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475\`
- H6 adalah HYBRID: target checkpoint base ditambah top-level protobuf SPU field 6 dari CONTROL; bukan target-pure.
- Setup emulator, disc, BIOS, target savestate, CONTROL savestate, Memory Card, dan Xvfb: semua langkah preflight sukses.
- Gameplay input: NONE.
- Tiga kondisi yang dikodekan: K0 tanpa breakpoint; K1 hanya getter 0x800138EC; K2 setter 0x8001387C + getter 0x800138EC + entry helper 0x800B770C.
- Dua launch per kondisi, independen. Breakpoint dipasang pada post-load frame 180.
- Capture yang diminta: SHA-256 2 MiB RAM pada post-load frame 180, 240, 360.
- Timeout konfigurasi per launch: 1.800 detik; pemeriksaan apakah setidaknya 2× wall time terlama aktual tetap menunggu keenam launch selesai.
- SHA referensi Memory Card awal yang diverifikasi: \`ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5\`.

### 5.2 Status saat laporan dibuat

Pada \`2026-10-31T15:07:03Z\`:
- Run status: \`in_progress\`
- Job status: \`in_progress\`
- Langkah 1–8: success, termasuk seluruh preflight input privat.
- Langkah 9 \`Run K0 K1 K2; two independent launches per condition\`: masih berjalan.
- Cleanup dan commit hasil teks belum dimulai.
- Job log/hasil belum dapat diambil karena job belum selesai; belum ada output commit AS3.

Karena belum tersedia tabel launch/frame hasil:
- 18 hash RAM (6 launch × 3 frame): TIDAK TAHU.
- Kode keluar emulator desimal per launch: TIDAK TAHU.
- Wall time per launch dan waktu maksimum: TIDAK TAHU.
- Memory Card SHA sesudah tiap launch: TIDAK TAHU.
- K0 dibanding AK1 baseline: TIDAK TAHU.
- K2 dibanding AR3 frame 360 \`4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907\`: TIDAK TAHU.
- Apakah breakpoint mengubah RAM, dan kondisi/frame pertama yang berbeda: TIDAK TAHU.
- Nol hit (jika ada) tidak dapat dipakai untuk menyimpulkan fungsi tidak digunakan.

**K5 belum diberikan untuk AS3.** K5 baru dapat dipertimbangkan setelah dua peluncuran terpisah per kondisi benar-benar selesai, ketiga capture per peluncuran tersedia, exit code/waktu/MCD dapat dicek, serta perbandingan hash dapat dihitung. Run ini telah disiapkan untuk mem-publish hanya teks dan hash; tidak ada ROM/BIOS/Memory Card/savestate/RAM/video/frame ke Git.

## 6. Batas kesimpulan game

Tidak ada rumus dari ucapan streamer yang diterima. Tidak ada label semantik build, upgrade, income, atau release yang disimpulkan dari setter/getter. Tidak ada angka saldo, harga bangun, harga upgrade, nilai Chakra release, atau income yang disahkan oleh audit ini. Nama/peran bisnis dan pemetaan runtime alamat global tetap TIDAK TAHU kecuali dinyatakan secara eksplisit oleh instruksi atau trace yang tersedia.

## 7. Safety dan batas repo

Tidak ada Release diubah atau visibilitas repository diubah. Tidak ada ISO, BIOS, Memory Card, savestate, dump RAM, video, atau frame gambar dikomit. Output yang dikomit pada rangkaian AS1 ini berupa source Ghidra, workflow, skrip eksperimen, Markdown, TSV, dan teks ringkasan/hash saja.
