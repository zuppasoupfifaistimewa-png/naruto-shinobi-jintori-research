# FA0–FA5 — verifikasi sesi dan rekonsiliasi bukti (2026-11-07)

Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`  
Target: SLPS-03553 / Naruto – Shinobi no Sato no Jintori Gassen  
Baseline inklusif: `b6fbdf25fdaa45b4d05f4dc5055e18fb6597b9b5`  
HEAD `main` sebelum addendum ini: `b8a47c1b80611dd2e167323a58b63dfc228f3267`  
Batas: analisis statis maksimum K4; K5 memerlukan runtime yang konsisten pada sedikitnya dua peluncuran.

## Putusan

| FA | Status | K | Hasil |
|---|---|---:|---|
| FA0 | TUNTAS | K4 | Ledger Git dan seluruh Actions run dalam rentang baseline–HEAD direkonsiliasi |
| FA1 | TUNTAS | K4 | 0xF020 dikoreksi sebagai immediate loader; seed nibble awal 2 dan 0 dikonfirmasi statis |
| FA2 | SEBAGIAN | K3 | Dump 408 instruksi F2A9C dan helper 19 instruksi tervalidasi dari dump Ghidra dengan identitas EXE sama; nilai tabel dan pemicu d tetap dinamis |
| FA3 | SEBAGIAN | K3 | Census akses langsung dan kandidat tile+0x24 diperluas; rantai terminal ke ekonomi/koordinat/tampilan belum lengkap |
| FA4 | BELUM | K0 | CONTROL H6 tidak tersedia; nol peluncuran dan nol watchpoint, sehingga tak ada debit runtime |
| FA5 | TUNTAS sebagai katalog hipotesis | K1 | Empat keluarga model dan falsifier dicatat; rumus game tetap TIDAK TAHU |

**Kesimpulan utama:** rumus biaya upgrade untuk lompatan level (d\ge2) masih **TIDAK TAHU**. FUN_800D15A8 menaikkan nibble level satu tingkat per kejadian. Post fee pada PC 0x800D46F8 adalah negasi nilai u16(tile+0x1A), tetapi bukti ini tidak menetapkan berapa kali post terjadi untuk satu perintah lompat level.

## FA0 — ledger Git dan Actions

Dari baseline inklusif sampai HEAD sebelum addendum ini, `b8a47c1b80611dd2e167323a58b63dfc228f3267`: **7 commit = 6 manusia + 1 bot**. Urutan:

1. `b6fbdf25fdaa45b4d05f4dc5055e18fb6597b9b5` — baseline, manusia.
2. `f74961b844d068a164732c08c78a363d5267e569` — pemicu satu kali validasi ulang, manusia.
3. `214326f955b0d8c2c8a7f7cf4ad4574fa71e2e42` — publikasi hasil DX0–DX4, bot.
4. `be22dc10c1264eaa4bd65948c6e48881a38b6117` — addendum audit, manusia.
5. `43d2bed4ceb468583ffa5a03730fdb07939e6677` — workflow dan skrip FA4, manusia.
6. `0491530cc2bc72338849046572422f5958e4a5b2` — catatan kegagalan FA4, manusia.
7. `b8a47c1b80611dd2e167323a58b63dfc228f3267` — ledger dan rekonsiliasi final, manusia.

Actions run yang ditemukan pada rentang ini:

| Run | Workflow / event | Source SHA | Status / job | Exit |
|---|---|---|---|---:|
| 42241745858 | Naruto Story Mode adaptive player monitor / schedule | `b6fbdf25fdaa45b4d05f4dc5055e18fb6597b9b5` | completed / success; monitor terjadwal historis | TIDAK TAHU |
| 42292998488 | Naruto Story Mode adaptive player monitor / schedule | `b6fbdf25fdaa45b4d05f4dc5055e18fb6597b9b5` | completed / success; monitor terjadwal historis | TIDAK TAHU |
| 42307609951 | DX0–DX4 full-image static audit / push | `f74961b844d068a164732c08c78a363d5267e569` | completed / success; job `dx0-dx4-static`, job ID `128200817882` | 0 |
| 42312284099 | FA4 H6 action-8 write-watchpoint / push | `43d2bed4ceb468583ffa5a03730fdb07939e6677` | completed / failure; job ID `128216422129` | 1 |

Run 42307609951 adalah satu-satunya validasi DX/EA yang digunakan: `python3 -m py_compile tools/stage1/RunDX0DX4Raw.py tools/stage1/RunEA0EA4Supplement.py` PASS; `RunEA0EA4Supplement.py` exit 0; cleanup input privat PASS; output hanya TXT/TSV/MD. Tidak ada pemicu workflow DX kedua. Run Story Mode di atas dicatat sebagai run schedule yang sudah terjadi; tidak ada monitor atau autoplay yang dijalankan ulang dalam audit ini. Pemeriksaan antrean saat audit: 0 run `in_progress`, 0 `queued`.

Ringkasan DX run:
`reports/stage1_economy/dx0-dx4-raw-run-42307609951/attempt-1/ACTIONS_RUN_SUMMARY.txt`

## FA1 — literal loader F020

- PC 0x800F7E64 memuat immediate `0xF020`; **0xF020 adalah nilai immediate instruksi, bukan file offset**.
- PC 0x800F7E68 menjalankan `sh` ke `tile+0x20`.
- Untuk word awal 0xF020, nibble bit 4–7 bernilai 2 dan nibble bit 8–11 bernilai 0.
- Dengan peta Entry 1 yang diminta: PC 0x800F7E64 → file offset 0x010FFA14; PC 0x800F7E68 → 0x010FFA18.
- Putusan K4 hanya untuk fakta loader dan nilai nibble awal; arti gameplay dari kedua nibble tidak otomatis terbukti.

Run 42307609951 menjalankan py_compile kedua skrip analisis sebelum input privat diambil. Tidak ada skrip Python yang diubah dalam addendum ini.

## FA2 — F2A9C, helper 1552C dan operand mult

### F2A9C

Dump lengkap berisi 408 baris instruksi dari PC 0x800F2A9C sampai epilog 0x800F30F8. Offset Entry 1 awal: 0x0110064C. Satu JAL caller langsung yang ditemukan berada di PC 0x800F5F54, fungsi caller FUN_800F3658, offset Entry 1 0x01103B04. Def-chain argumen a0–a3 tidak dapat dipastikan karena caller-saved register telah melewati JAL 0x800E6DA4; seluruh argumen tersebut TIDAK TAHU.

Empat call ke helper 0x8001552C di dalam F2A9C berada pada PC 0x800F2B5C, 0x800F2CC8, 0x800F2DF0, dan 0x800F2E48.

### Helper 0x8001552C — dump Ghidra yang direkonsiliasi

Dump Ghidra arsip memuat 19 instruksi helper dan identitas EXE yang sama dengan run DX/EA: SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`. Untuk EXE, offset PC 0x8001552C = 0x00005D2C menurut `0x800+(PC-0x80010000)`.

| PC | Offset EXE | Bytes | Decode |
|---|---:|---|---|
| 0x8001552C | 0x5D2C | E8 FF BD 27 | addiu sp,sp,-0x18 |
| 0x80015530 | 0x5D30 | 14 00 BF AF | sw ra,0x14(sp) |
| 0x80015534 | 0x5D34 | 10 00 B0 AF | sw s0,0x10(sp) |
| 0x80015538 | 0x5D38 | 35 55 00 0C | jal 0x800154D4 |
| 0x8001553C | 0x5D3C | 21 80 80 00 | move s0,a0 (delay slot) |
| 0x80015540 | 0x5D40 | 2B 10 02 02 | sltu v0,s0,v0 |
| 0x80015544 | 0x5D44 | 07 00 40 10 | beq v0,zero,0x80015564 |
| 0x80015548 | 0x5D48 | 05 80 02 3C | lui v0,0x8005 (delay slot) |
| 0x8001554C | 0x5D4C | EC 5C 42 24 | addiu v0,v0,0x5CEC |
| 0x80015550 | 0x5D50 | 00 19 10 00 | sll v1,s0,4 |
| 0x80015554 | 0x5D54 | 21 10 43 00 | addu v0,v0,v1 |
| 0x80015558 | 0x5D58 | 08 00 42 8C | lw v0,0x8(v0) |
| 0x8001555C | 0x5D5C | 5A 55 00 08 | j 0x80015568 |
| 0x80015560 | 0x5D60 | 00 00 00 00 | nop (delay slot) |
| 0x80015564 | 0x5D64 | 21 10 00 00 | addu v0,zero,zero |
| 0x80015568 | 0x5D68 | 14 00 BF 8F | lw ra,0x14(sp) |
| 0x8001556C | 0x5D6C | 10 00 B0 8F | lw s0,0x10(sp) |
| 0x80015570 | 0x5D70 | 08 00 E0 03 | jr ra |
| 0x80015574 | 0x5D74 | 18 00 BD 27 | addiu sp,sp,0x18 (delay slot) |

Dua jalur return helper:
1. Jika `$a0` unsigned lebih kecil dari return FUN_800154D4(), `$v0 = *(u32 *)(0x80055CF4 + $a0*0x10 + 8)` (instruksi lw pada 0x80015558).
2. Jika tidak, branch menuju 0x80015564 membersihkan `$v0=0`.

**Konflik artefak:** `EA2_FUN_8001552C_RETURN_HELPER.tsv` dari run DX/EA terbaru mempunyai bytes/decode yang bertentangan dengan dump Ghidra untuk EXE SHA yang sama. TSV helper otomatis itu ditolak sebagai bukti; tabel instruksi di atas bersumber dari dump Ghidra arsip, bukan disalin dari TSV yang salah.

### Operand store

- Store 0x800F2CF8: `mflo` mengambil hasil `mult` pada 0x800F2CF0. Multiplicand `$v0` berasal dari return helper call 0x800F2CC8; multiplier `$v1` berasal dari `lbu 0x8013EA71` lalu dikurangi 2. Nilai tabel dan global tetap dinamis.
- Store 0x800F2E38: `mult` berada di 0x800F2E2C, tetapi `$v0` telah diisi nol oleh `negu $v0,$zero` di 0x800F2E0C. Produk yang disimpan pada PC 0x800F2E38 karenanya nol. Operand lainnya berasal dari `lbu 0x8013EA71`, dikurangi 1, lalu dikurangi global dinamis 0x80139EFC.
- Store lain di 0x800F2E68 menyimpan negasi helper return; itu kandidat pending delta, bukan bukti biaya d tertentu.
- Tidak satu pun data tersebut mengikat helper/table dinamis ke lompatan level d=1..4.

## FA3 — census manager dan tile+0x24

### Basis pointer dan akses manager

Basis manager yang diminta adalah pointer yang dimuat dari slot global 0x8013EA74. File census manager memuat 55 baris akses langsung untuk displacement +0x2B4 dan +0x390:

| Field | Total akses | READ | WRITE | Basis yang terbukti |
|---|---:|---:|---:|---|
| manager+0x2B4 | 16 | 2 | 14 | Semua baris yang tercatat memakai slot 0x8013EAB0, bukan slot manager 0x8013EA74 |
| manager+0x390 | 39 | 15 | 24 | Semua baris yang tercatat memakai slot 0x8013EA74 |

Tidak ada pembacaan manager+0x2B4 yang dapat dibuktikan berasal dari basis slot 0x8013EA74 dalam census ini. Dua reader +0x2B4 yang harus tetap dipertahankan sebagai kandidat berbeda berada pada PC 0x800B3438 dan 0x800B66E8; basisnya 0x8013EAB0, bukan 0x8013EA74.

15 reader +0x390 dengan basis manager 0x8013EA74:
- FUN_800BBC1C: 0x800BBC78, 0x800BBD6C
- FUN_800BBD9C: 0x800BBE14
- FUN_800D15A8: 0x800D1BEC, 0x800D1BFC, 0x800D1C68, 0x800D1C88, 0x800D1D5C, 0x800D1D6C, 0x800D1DDC, 0x800D1DFC
- FUN_800FA4C8: 0x800FA63C, 0x800FA7AC
- FUN_800FAEBC: 0x800FB004
- FUN_800FF00C: 0x800FF268

Census ini membuktikan akses langsung dan basis pointer. Penelusuran nilai dari seluruh keenam fungsi pembaca hingga konsumen terminal ekonomi/koordinat/tampilan belum lengkap; semantik manager+0x390 tidak diklaim selesai.

### Tile+0x24, tanpa menyamakan seluruh displacement dengan tile

Census full-image `DZ4_TILE_PLUS24_ALL_LH_LHU_SH_CENSUS.tsv` berisi 306 kandidat instruksi LH/LHU/SH displacement +0x24 di EXE dan Entry 1. Dari sana, 160 akses mempunyai lineage basis tile array yang terbukti melalui slot 0x8013EA84: 158 READ dan 2 WRITE. Dua writer yang terbukti:
- PC 0x800F7E2C (FUN_800F7ADC), menyimpan halfword dari byte sumber.
- PC 0x800F7E40 (FUN_800F7ADC), menyimpan gabungan dua byte sumber.

Dua fan-out nilai tile+0x24 yang dikaitkan langsung dalam audit:
- 0x800EC388 membaca tile+0x24; jalur mengurangkan global 0x8013EAD2 dan menulis hasil ke displacement manager+0x2B4, dengan basis 0x8013EAB0.
- 0x800DAF2C membaca tile+0x24; jalur meneruskan nilai ke manager+0x390 dengan basis 0x8013EA74.

Hipotesis, bukan fakta:
1. **Koordinat/posisi relatif.** Indikasi: subtract global 0x8013EAD2 sebelum forwarding ke +0x2B4. Falsifier: seluruh konsumen menunjukkan kode kategorikal tanpa aritmetika koordinat/perpindahan.
2. **Status tampilan/event.** Indikasi: forwarding ke manager+0x390 tanpa aritmetika lokal. Falsifier: seluruh reader +0x390 terbukti hanya dipakai untuk kalkulasi gerak/posisi atau tabel ekonomi.
3. **Owner/level.** Masih mungkin, tetapi belum ada tabel owner/level langsung. Falsifier: rentang writer/consumer membuktikan nilai tidak terhubung ke owner/level atau tabel transisi eksklusif menunjukkan sebaliknya.

Jumlah akses yang terbukti bukan pengganti trace terminal. FA3 tetap K3/SEBAGIAN.

## FA4 — status runtime dan blocker

Run 42312284099 gagal dengan job exit code 1, job ID 128216422129. Target checkpoint, PCSX pinned, disc, dan BIOS lolos validasi. Langkah download CONTROL gagal karena artifact `naruto-storymode-adaptive-player-private` dari run 39867730674 tidak ditemukan. Pemeriksaan daftar artifact run sumber menghasilkan array kosong.

Akibat yang tercatat:
- H6 hybrid tidak terbentuk; payload CONTROL top-level field 6 tidak tersedia.
- PCSX tidak diekstrak/dijalankan; Xvfb, py_compile FA4, 8 peluncuran, dan 5 watchpoint dilewati.
- Peluncuran aktual 0/8; watchpoint 0/5; action-8 dispatch TIDAK DIUJI; debit d=1..4 tidak ada.
- Timeout 360 detik per peluncuran hanya dikonfigurasi; tidak ada peluncuran aktual yang mengalami timeout.
- Kegagalan publikasi akhir workflow mempunyai exit code 2 karena berkas script-exit-code tidak pernah dibuat setelah prasyarat download gagal.

Ini bukan bukti action 8 tidak terjangkau dan bukan nilai debit nol. Workflow FA4 tidak diulang karena artifact prasyarat yang dikunci telah diverifikasi tidak tersedia. FA4 tetap K0/BELUM.

## FA5 — hipotesis fee d=1..4

Fee dasar increment tetap simbolik `C`. Tidak ada fitting ke angka pengguna 400/800/1600 dan tidak ada debit independen.

| Model | Faktor prediksi d=1,2,3,4 | Falsifier |
|---|---|---|
| Linear per level: `C*d` | 1, 2, 3, 4 | Debit independen atau alur ROM menunjukkan faktor bukan d |
| Eksponensial: `C*2^(d-1)` | 1, 2, 4, 8 | Debit independen menyimpang atau disassembly membuktikan tidak ada pemilihan eksponen |
| Akumulasi increment: `C*sum(2^k, k=0..d-1)` | 1, 3, 7, 15 | Debit independen tidak cocok atau call closure membuktikan hanya satu post dengan koefisien lain |
| Lookup: `C*L[d]` | TIDAK DIISI | Tabel ROM asli plus pengukuran independen d>=2 harus menentukan L |

Semua model K1. Model lookup dengan nilai yang disalin dari angka pengamatan pengguna adalah **TAUTOLOGI**, bukan bukti.

## Integritas dan file perubahan

- Addendum verifikasi ini menambahkan **satu file**: `reports/stage1_economy/FA0_FA5_SESSION_VERIFICATION_2026-11-07.md`.
- Tidak ada skrip Python atau workflow yang diubah dalam addendum ini; tidak ada workflow baru yang dipicu. Karena tidak ada skrip yang diubah, tidak ada py_compile tambahan sebelum commit.
- `STATUS.md` tetap 693844 byte, blob `ee7b9c226631c71cae1c9fb0270994ccf3e67c07`.
- Release `naruto-checkpoint-39262213468` tidak diubah.
- Tidak ada ISO, BIOS, savestate, RAM dump, Memory Card, video, frame, atau biner dikomit.
