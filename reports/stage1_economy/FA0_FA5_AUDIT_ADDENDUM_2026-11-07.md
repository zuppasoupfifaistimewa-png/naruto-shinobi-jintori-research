# FA0–FA5 — addendum audit Naruto Jintori (2026-11-07)

Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Target: SLPS-03553 / Naruto – Shinobi no Sato no Jintori Gassen
Scope: statis maksimum K4; K5 hanya bila runtime konsisten pada sedikitnya dua peluncuran.
Baseline inklusif yang diminta: b6fbdf25fdaa45b4d05f4dc5055e18fb6597b9b5.
HEAD saat addendum ini disusun (sebelum commit addendum): 214326f955b0d8c2c8a7f7cf4ad4574fa71e2e42.

## Status akhir per FA

| FA | Status | K | Kesimpulan |
|---|---|---:|---|
| FA0 | TUNTAS | K4 | Ledger Git inklusif dan semua Actions run pada rentang baseline–HEAD teridentifikasi |
| FA1 | TUNTAS | K4 | Koreksi literal 0xF020, seed nibble awal, dan satu run validasi statis PASS |
| FA2 | SEBAGIAN | K3 | Full dump F2A9C tersedia; helper direkonsiliasi dari dump Ghidra dengan hash EXE sama, tetapi TSV helper dari run terbaru bertentangan dan ditolak |
| FA3 | SEBAGIAN | K3 | 15 pembaca manager+0x390 dengan basis 0x8013EA74; tidak ada pembaca manager+0x2B4 dengan basis itu; rantai konsumen akhir belum lengkap |
| FA4 | BELUM | K0 | Tidak dilakukan peluncuran runtime/watchpoint yang sesuai lima target; tidak ada sampel debit |
| FA5 | TUNTAS | K1 | Empat keluarga hipotesis dan falsifier dicatat; tidak ada fit dari observasi pengguna dan rumus game tetap TIDAK TAHU |

Kesimpulan utama: rumus biaya upgrade petak untuk lompatan d>=2 tetap TIDAK TAHU. FUN_800D15A8 menaikkan nibble level tepat +1 per kejadian; post-fee statis di 0x800D46F8 adalah -u16(tile+0x1A), datar. Fakta tersebut tidak membuktikan jumlah kejadian atau biaya total untuk satu lompatan multi-level.

## FA0 — ledger Git dan Actions

Git dihitung dari baseline yang diminta, inklusif:

- Snapshot source SHA f74961b844d068a164732c08c78a363d5267e569: 2 commit inklusif = 2 manusia, 0 bot (baseline b6fbdf... dan commit trigger f74961...).
- HEAD sebelum addendum 214326f955b0d8c2c8a7f7cf4ad4574fa71e2e42: 3 commit inklusif = 2 manusia, 1 bot.
- Commit addendum ini menambah satu commit manusia; hitungan akhir setelah commit addendum = 4 commit inklusif, 3 manusia, 1 bot.

Urutan commit:
1. b6fbdf25fdaa45b4d05f4dc5055e18fb6597b9b5 — manusia; baseline.
2. f74961b844d068a164732c08c78a363d5267e569 — manusia; trigger validasi ulang satu kali.
3. 214326f955b0d8c2c8a7f7cf4ad4574fa71e2e42 — github-actions[bot]; publikasi hasil run 42307609951.
4. Commit addendum ini — manusia.

Semua Actions run yang dibuat pada rentang waktu baseline sampai HEAD pre-addendum:
- 42241745858 — Naruto Story Mode adaptive player monitor; event schedule; head SHA b6fbdf25fdaa45b4d05f4dc5055e18fb6597b9b5; completed/success.
- 42292998488 — Naruto Story Mode adaptive player monitor; event schedule; head SHA b6fbdf25fdaa45b4d05f4dc5055e18fb6597b9b5; completed/success.
- 42307609951 — DX0-DX4 full-image static economy audit; event push; source SHA f74961b844d068a164732c08c78a363d5267e569; job dx0-dx4-static; completed/success; script exit 0; EA exit 0.
Tidak ada Actions run berstatus in_progress pada pemeriksaan akhir.

Run 42307609951 menjalankan:
- python3 -m py_compile tools/stage1/RunDX0DX4Raw.py tools/stage1/RunEA0EA4Supplement.py — PASS.
- Tahap validasi input privat — PASS.
- RunEA0EA4Supplement.py — EA_EXIT_CODE=0.
- Penghapusan input privat — PASS.
- ACTIONS_STATUS=PASS; output yang dikomit hanya teks/TSV/TXT; GAME_OR_EMULATOR_EXECUTED=no; BIOS_OR_SAVESTATE_USED=no; BINARY_COMMITTED=no.

Ringkasan run terkomit:
reports/stage1_economy/dx0-dx4-raw-run-42307609951/attempt-1/ACTIONS_RUN_SUMMARY.txt

Permalink raw:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/214326f955b0d8c2c8a7f7cf4ad4574fa71e2e42/reports/stage1_economy/dx0-dx4-raw-run-42307609951/attempt-1/ACTIONS_RUN_SUMMARY.txt

## FA1 — literal F020 dan seed nibble

Koreksi interpretasi:
- 0xF020 adalah nilai immediate ori pada loader PC 0x800F7E64, bukan file offset.
- Instruksi sh pada PC 0x800F7E68 menulis nilai itu ke tile+0x20.
- Untuk word awal 0xF020, nibble bit 4–7 = 2 dan nibble bit 8–11 = 0.
- Dengan aturan Entry 1 yang diminta, file_offset PC 0x800F7E64 = 0x010FFA14 dan PC 0x800F7E68 = 0x010FFA18.
- Klasifikasi: K4 statis. Ini mengoreksi teks lama yang menyatakan seed 2 belum terbukti dan salah membaca 0xF020 sebagai file offset.

Validasi ulang yang diizinkan hanya dijalankan satu kali: run 42307609951. Log membuktikan kedua skrip lolos py_compile, analisis tambahan keluar 0, dan job sukses. Tidak ada run duplikat. Tidak ada skrip Python diubah dalam commit trigger ini; kompatibilitas entry yang sudah berada di baseline dibuktikan dengan run tersebut.

## FA2 — FUN_800F2A9C dan helper 0x8001552C

### Dump FUN_800F2A9C

Full instruction dump tersedia dengan 408 baris instruksi, dari PC 0x800F2A9C sampai epilog PC 0x800F30F8. PC 0x800F2A9C memakai file_offset Entry 1 0x0110064C menurut rumus 0x10BB000+(PC-0x800AD450). File mencatat bytes little-endian dan decode tiap instruksi; file_offset divalidasi dengan aturan Entry 1.

Permalink raw:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/214326f955b0d8c2c8a7f7cf4ad4574fa71e2e42/reports/stage1_economy/dx0-dx4-raw-run-42307609951/attempt-1/EA2_FUN_800F2A9C_FULL_TO_RETURN.tsv

Satu direct caller yang ditemukan:
- PC 0x800F5F54, file_offset Entry 1 0x01103B04, bytes A7 CA 03 0C, JAL FUN_800F2A9C, caller FUN_800F3658.
- Def-chain argument di caller terputus oleh JAL sebelumnya; argumen register caller-saved tetap TIDAK TAHU.

JAL helper 0x8001552C di dalam FUN_800F2A9C muncul pada PC 0x800F2B5C, 0x800F2CC8, 0x800F2DF0, dan 0x800F2E48. Satu epilog FUN_800F2A9C berakhir di PC 0x800F30F8 (jr $ra). Return value fungsi F2A9C tidak boleh dianggap konstanta; tergantung jalur dan nilai dinamis yang terakhir mengisi $v0.

### Rekonsiliasi helper 0x8001552C

PENTING: EA2_FUN_8001552C_RETURN_HELPER.tsv yang dihasilkan run 42307609951 berisi bytes/decode yang bertentangan dengan dump Ghidra lama untuk EXE yang SHA-256-nya sama dengan EXE run baru (a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569). Oleh sebab itu TSV otomatis helper tersebut DITOLAK sebagai bukti fungsi. Self-check 788 baris PASS tidak mendeteksi konflik semantik helper ini.

Dump Ghidra archived untuk SLPS_035.53 menyimpan 19 instruksi helper; input-identity.txt pada arsip yang sama mencatat main_exe_sha256 yang identik. Dengan rumus file_offset EXE 0x800+(PC-0x80010000), PC pertama 0x8001552C memiliki file_offset 0x00005D2C. Decode helper:

| PC | File offset EXE | Bytes | Instruksi |
|---|---:|---|---|
| 0x8001552C | 0x00005D2C | E8 FF BD 27 | addiu sp,sp,-0x18 |
| 0x80015530 | 0x00005D30 | 14 00 BF AF | sw ra,0x14(sp) |
| 0x80015534 | 0x00005D34 | 10 00 B0 AF | sw s0,0x10(sp) |
| 0x80015538 | 0x00005D38 | 35 55 00 0C | jal 0x800154D4 |
| 0x8001553C | 0x00005D3C | 21 80 80 00 | move s0,a0 (delay slot JAL) |
| 0x80015540 | 0x00005D40 | 2B 10 02 02 | sltu v0,s0,v0 |
| 0x80015544 | 0x00005D44 | 07 00 40 10 | beq v0,zero,0x80015564 |
| 0x80015548 | 0x00005D48 | 05 80 02 3C | lui v0,0x8005 (delay slot branch) |
| 0x8001554C | 0x00005D4C | EC 5C 42 24 | addiu v0,v0,0x5cec |
| 0x80015550 | 0x00005D50 | 00 19 10 00 | sll v1,s0,4 |
| 0x80015554 | 0x00005D54 | 21 10 43 00 | addu v0,v0,v1 |
| 0x80015558 | 0x00005D58 | 08 00 42 8C | lw v0,0x8(v0) |
| 0x8001555C | 0x00005D5C | 5A 55 00 08 | j 0x80015568 |
| 0x80015560 | 0x00005D60 | 00 00 00 00 | nop (delay slot J) |
| 0x80015564 | 0x00005D64 | 21 10 00 00 | clear v0 / addu v0,zero,zero |
| 0x80015568 | 0x00005D68 | 14 00 BF 8F | lw ra,0x14(sp) |
| 0x8001556C | 0x00005D6C | 10 00 B0 8F | lw s0,0x10(sp) |
| 0x80015570 | 0x00005D70 | 08 00 E0 03 | jr ra |
| 0x80015574 | 0x00005D74 | 18 00 BD 27 | addiu sp,sp,0x18 (delay slot JR) |

Semua return helper:
1. Bila param_1 ($a0) unsigned lebih kecil dari FUN_800154D4(), $v0 = *(u32 *)(0x80055CF4 + param_1*0x10).
2. Bila tidak, $v0 = 0.
Tidak ada jalur return ketiga pada function body ini. Nilai tabel bersifat dinamis; nilainya tidak otomatis sama dengan biaya level.

### Asal operand mult dan store manager+0x2EE

- Store PC 0x800F2CF8: mflo berasal dari mult pada 0x800F2CF0. Multiplicand $v0 berasal dari helper return JAL 0x800F2CC8. Multiplier $v1 berasal dari lbu pada global 0x8013EA71 lalu addiu -2 di PC 0x800F2CEC. Store address dibentuk dari manager pointer slot 0x8013EA74, ditambah 2*global 0x8013EB0C dan 0x2EE. Nilai global/table tetap DINAMIS.
- Store PC 0x800F2E38: mult pada 0x800F2E2C memakai $v0 yang sudah ditimpa menjadi nol oleh negu $v0,$zero pada 0x800F2E0C setelah helper call 0x800F2DF0. Operand $a0 berasal dari lbu 0x8013EA71, addiu -1, lalu dikurangi u32 global 0x80139EFC pada 0x800F2E28. Produk yang disimpan di 0x800F2E38 adalah nol karena operand pertama nol.
- Store terpisah PC 0x800F2E68: $v0 adalah negasi helper return dari JAL 0x800F2E48; store ke manager + 2*0x8013EB0C + 0x2EE. Ini kandidat pending delta, tetapi hubungan ke upgrade d dan debit Chakra belum dibuktikan.

Dengan demikian, baris 0x800F2E38 bukan bukti biaya debit; dan store -helper di 0x800F2E68 juga belum membuktikan rumus biaya d>=2.

Dump helper archived dan identitas input:
reports/stage1_economy/aq1-run-41390225493/attempt-1/az3-main-exe-economic-helper-detail.txt
reports/stage1_economy/aq1-run-41390225493/attempt-1/input-identity.txt

## FA3 — pembaca manager+0x2B4/+0x390 dan tile+0x24

Census langsung yang mempertahankan akses dengan basis terbukti tersedia di:
reports/stage1_economy/dx0-dx4-raw-run-42307609951/attempt-1/EA3_MANAGER_PLUS2B4_PLUS390_PROVEN_CONSUMERS.tsv

Hasil filter basis:
- Basis manager harus terbukti berasal dari slot pointer 0x8013EA74.
- manager+0x390: 15 pembacaan langsung terbukti pada PC 0x800BBC78, 0x800BBD6C, 0x800BBE14, 0x800D1BEC, 0x800D1BFC, 0x800D1C68, 0x800D1C88, 0x800D1D5C, 0x800D1D6C, 0x800D1DDC, 0x800D1DFC, 0x800FA63C, 0x800FA7AC, 0x800FB004, dan 0x800FF268.
- manager+0x2B4: tidak ada pembacaan dengan basis slot 0x8013EA74.
- Ada dua kandidat pembacaan displacement +0x2B4 pada PC 0x800B3438 dan 0x800B66E8, tetapi register basisnya berasal dari slot 0x8013EAB0, bukan 0x8013EA74. Keduanya dipertahankan sebagai kandidat berbeda dan tidak salah dilabeli sebagai manager+0x2B4.

Fungsi yang menjadi konsumen langsung +0x390:
- FUN_800BBC1C: dua load;
- FUN_800BBD9C: satu load;
- FUN_800D15A8: delapan load;
- FUN_800FA4C8: dua load;
- FUN_800FAEBC: satu load;
- FUN_800FF00C: satu load.

Keterbatasan: daftar ini adalah semua akses langsung yang basis register-nya dapat dibuktikan dalam output tersebut. Pemakaian nilai register hasil load hingga konsumen terminal ekonomi/koordinat/tampilan belum diekstrak tuntas untuk setiap fungsi. Nama fungsi tidak dipakai sebagai bukti semantik. Karena permintaan menyebutkan end-consumer dan tidak membuang kandidat, FA3 tetap SEBAGIAN.

Tile+0x24:
- Writer proven dari tile array berbasis slot 0x8013EA84: PC 0x800F7E2C dan 0x800F7E40 dalam FUN_800F7ADC; keduanya membangun halfword dari byte sumber.
- Pada satu jalur event, tile+0x24 dibaca lalu dikurangi global dinamis 0x8013EAD2 sebelum disimpan ke displacement +0x2B4 dari basis lain. Ini mendukung kemungkinan koordinat relatif, bukan bukti final.
- Pada jalur event lain, nilai tile+0x24 diteruskan ke manager+0x390 tanpa arithmetic lokal. Ini kompatibel dengan status tampilan/event.

Hipotesis dan falsifier:
1. Posisi/koordinat relatif. Falsifier: semua writer/consumer membuktikan nilai sebagai kode kategori dan tidak ada operasi koordinat/perpindahan.
2. Display/event status. Falsifier: pembaca manager+0x390 terbukti hanya menghitung gerak/koordinat atau mengindeks tabel ekonomi, tanpa peran display/event.
3. Owner/level. Falsifier: rentang nilai writer dan transisi consumer terbukti tidak berkaitan dengan owner/level, atau sebaliknya tabel transisi eksklusif ditemukan.
Ketiga makna tersebut tetap hipotesis, bukan fakta.

## FA4 — runtime dan watchpoint

FA4 BELUM dijalankan. Tidak ada PCSX-Redux launch baru dalam sesi ini, sehingga tidak ada frame/PC/old/new runtime sample dan tidak ada nilai debit untuk d=1..4.

Workflow write-watchpoint lama AV2 tidak identik dengan permintaan ini: targetnya adalah empat alamat record Chakra 0x80070EB8, 0x80070F6C, 0x80071020, dan 0x800710D4, bukan lima target manager/tile/global yang diminta. Menggunakannya sebagai bukti FA4 akan salah. Karena tidak ada run yang sesuai, alasan runtime action 8 dapat dicapai/tidak dapat dicapai dari log adalah TIDAK TAHU. Jangan menafsirkan ketiadaan event sebagai nol biaya.

Syarat bukti runtime selanjutnya tetap: setidaknya dua peluncuran H6 hybrid terpisah; watchpoint tulis pada manager+0x2EE, tile+0x20, tile+0x1A, 0x80139EFC, 0x8013EB0C; catat frame, PC, old/new; timeout per launch dicatat; output hanya TXT/TSV; sampel runtime tidak dipromosikan menjadi rumus.

## FA5 — keluarga hipotesis fee d=1..4

Tidak ada nilai debit independen yang digunakan untuk mem-fit model. Fee dasar per increment ditulis C dan tetap simbolik.

| Model | Prediksi faktor untuk d=1,2,3,4 | Falsifier |
|---|---|---|
| H1 linear per tingkat: fee(d)=C*d | 1,2,3,4 | Satu pengukuran independen d>=2 atau dataflow ROM yang menunjukkan faktor bukan d |
| H2 eksponensial: fee(d)=C*2^(d-1) | 1,2,4,8 | Satu pengukuran independen yang menyimpang atau disassembly membuktikan tidak ada pemilihan eksponen berbasis d |
| H3 akumulasi bertingkat: fee(d)=C*sum(2^k, k=0..d-1) | 1,3,7,15 | Debit independen tidak sesuai jumlah post berulang; atau call closure membuktikan hanya satu post dengan koefisien lain |
| H4 lookup khusus: fee(d)=C*L[d] | TIDAK DIISI | Tabel ROM asli dan pengukuran independen d>=2 harus membuktikan L; tabel salinan angka pengguna tidak punya nilai prediktif |

Setiap model adalah hipotesis K1; tidak ada model yang dinyatakan sebagai rumus game. Model lookup yang sebelumnya memakai faktor yang disalin langsung dari angka pengamatan pengguna harus diberi label TAUTOLOGI dan tidak dihitung sebagai bukti. Data pengguna 400/800/1600 tidak dipakai sebagai sampel pembuktian.

## Larangan, integritas, dan berkas berubah

- STATUS.md tidak berubah: 693844 byte; blob SHA ee7b9c226631c71cae1c9fb0270994ccf3e67c07.
- Release naruto-checkpoint-39262213468 tidak diubah.
- Tidak ada ISO, BIOS, savestate, raw dump, video, frame, atau biner dikomit oleh pekerjaan ini.
- Tidak ada skrip Python diubah dalam addendum; karena itu tidak ada skrip lokal tambahan yang perlu dikompilasi. Run 42307609951 sendiri menjalankan py_compile pada kedua skrip di atas sebelum analisis.
- Commit trigger f74961b mengubah satu berkas: .github/workflows/dx0-dx4-raw-static.yml (satu komentar pemicu).
- Commit bot 214326f menambahkan 80 berkas TXT/TSV/MD di reports/stage1_economy/dx0-dx4-raw-run-42307609951/attempt-1/:
ACTIONS_RUN_SUMMARY.txt; DX0_COMMIT_LEDGER.tsv; DX0_COUNTS.tsv; DX0_DX4_STATIC_AUDIT.md; DX1_ALL_PLUS1A_ACCESS.tsv; DX1_D15A8_WINDOW_PLUS1A.tsv; DX2_2EE_READERS_TO_SETTER.tsv; DX2_ALL_PLUS2EE_ACCESS.tsv; DX2_CFG_JR_AND_EXTERNAL_EXITS.tsv; DX2_FUN_800EC574_CFG.tsv; DX2_HELPER_ONE_TO_PLUS2EE.tsv; DX2_PATH_CONDITIONS.tsv; DX2_SETTER_8001387C_CALLS.tsv; DX2_SETTER_8001387C_EXITS.tsv; DX2_SETTER_8001387C_RAW.tsv; DX2_TARGET_REACHABILITY.tsv; DX3_LEVEL_DIFFERENCE_CANDIDATES.tsv; DX3_LEVEL_NIBBLE_COMPARISONS.tsv; DX3_LEVEL_NIBBLE_OR_SOURCES.tsv; DX3_ONE_SHIFT_PATTERNS.tsv; DX3_OPERATION_CENSUS.tsv; DX3_SEED_REACHABILITY.tsv; DX3_TILE_PLUS20_READ_WRITE.tsv; DX4_USER_OBSERVATION_MODEL_COMPARISON.tsv; DX_ANALYSIS_SUMMARY.txt; DY0_COMMIT_LEDGER.tsv; DY0_COUNTS.tsv; DY0_DY4_STATIC_AUDIT.md; DY1_CALLER_CLOBBER_BRANCHES.tsv; DY2_ACTION8_EVENT3_LEVEL_ADJUDICATION.tsv; DY2_ACTION8_EVENT3_LEVEL_FINDINGS.tsv; DY2_ACTION8_EVENT3_LEVEL_SOURCE_WINDOWS.tsv; DY2_TILE_PLUS20_PLUS21_WRITERS.tsv; DY3_GLOBAL_80139EFC_ARITHMETIC_EXPRESSIONS.tsv; DY3_GLOBAL_80139EFC_WRITERS.tsv; DY3_HELPER_RNG_RETRY_LOOP.tsv; DY3_HELPER_STATUS_HYPOTHESES.tsv; DY3_MANAGER_FIELDS_4F0_4F4_534.tsv; DY3_MANAGER_FIELD_READERS.tsv; DY4_ACTION8_DIRECT_BACKEDGES.tsv; DY4_ACTION8_FEE_POSTS_CALL_CLOSURE.tsv; DY4_ACTION8_POST_LOOP_AUDIT.tsv; DY4_FEE_HYPOTHESES_D1_D4.tsv; DY_ANALYSIS_SUMMARY.txt; DZ0_DZ4_STATIC_AUDIT.md; DZ1_ALL_TSV_FILE_OFFSET_AND_DECODE_SELF_CHECK.tsv; DZ1_SELF_CHECK_SUMMARY.txt; DZ2_ACTION8_OLD_NIBBLE_VS_EB0C_COMPARE_SUBTRACT.tsv; DZ2_D15A8_FEE_WINDOW_800D46B0_800D4840.tsv; DZ2_GLOBAL_8013EB0C_READ_WRITE_CENSUS.tsv; DZ2_LEVEL_NIBBLE_OR_GLOBAL_SOURCE_SITES.tsv; DZ3_ACTION8_ALL_PLUS2EE_STORE_PATHS.tsv; DZ3_ACTION8_CLOSURE_JR_JALR_CENSUS.tsv; DZ3_D15A8_ALL_LOCAL_BRANCH_JUMP_TARGETS_LE_46EC.tsv; DZ3_F5CE0_JR_TABLE_9_TARGET_AUDIT.tsv; DZ4_TILE_PLUS24_ALL_LH_LHU_SH_CENSUS.tsv; DZ4_TILE_PLUS24_SEMANTIC_HYPOTHESES.tsv; DZ4_TILE_PLUS24_VALUE_REFERENCE_FANOUT.tsv; DZ_ANALYSIS_SUMMARY.txt; EA0_COMMIT_COUNTS.tsv; EA0_COMMIT_LEDGER.tsv; EA1_D15A8_BRANCHES.tsv; EA1_D15A8_DIRECT_CALLERS.tsv; EA1_D15A8_WINDOW_800D4640_800D4840.tsv; EA1_LOADER_F020_CANDIDATE_WINDOWS.tsv; EA1_TILE_PLUS20_READ_WRITE_LINEAGE.tsv; EA2_F2A9C_TILE_PLUS1A_ACCESS.tsv; EA2_FEE_HYPOTHESES_D1_D4.tsv; EA2_FUN_8001552C_RETURN_HELPER.tsv; EA2_FUN_800F2A9C_DIRECT_CALLERS.tsv; EA2_FUN_800F2A9C_FULL_TO_RETURN.tsv; EA2_REQUESTED_PLUS2EE_STORE_COMPARISON.tsv; EA3_GLOBAL_8013EAD2_ALL_ACCESSES.tsv; EA3_MANAGER_PLUS2B4_PLUS390_PROVEN_CONSUMERS.tsv; EA3_TILE_PLUS24_PROVEN_WRITERS.tsv; EA3_TILE_PLUS24_SEMANTIC_HYPOTHESES.tsv; EA4_8013EB0C_DYNAMIC_EXPRESSION_CORRECTION.tsv; EA4_STRAIGHT_LINE_INSTRUCTIONS.tsv; EA_SELF_CHECK.tsv; EA_SELF_CHECK_SUMMARY.txt.
- Addendum commit ini menambahkan satu berkas: reports/stage1_economy/FA0_FA5_AUDIT_ADDENDUM_2026-11-07.md.
