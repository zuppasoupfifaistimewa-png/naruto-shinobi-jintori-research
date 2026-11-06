# FA0–FA5 — rekonsiliasi akhir berbasis bukti (2026-11-07)

Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Target: SLPS-03553 / Naruto – Shinobi no Sato no Jintori Gassen
Baseline inklusif: b6fbdf25fdaa45b4d05f4dc5055e18fb6597b9b5
HEAD yang diaudit sebelum commit laporan: 0491530cc2bc72338849046572422f5958e4a5b2
Batas bukti: statis maksimum K4; K5 hanya jika runtime konsisten pada sedikitnya dua peluncuran independen.

## Putusan ringkas

| Tahap | Status | K | Yang sudah dibuktikan | Sisa yang belum terbukti |
|---|---|---:|---|---|
| FA0 | TUNTAS | K4 | Ledger commit dan Actions sampai run FA4 terakhir direkonsiliasi | Tidak ada item ledger dalam rentang audit ini yang belum dicatat |
| FA1 | TUNTAS | K4 | Literal loader 0xF020 dan penulisan tile+0x20 terpetakan | Makna gameplay nibble masih di luar klaim yang terbukti |
| FA2 | SEBAGIAN | K3 | Dump F2A9C, empat call helper, argumen helper dari manager+0x530, dan helper lookup statis | Nilai field/tabel dinamis, hubungan nilai ke d=1..4, serta pemicu gameplay belum terikat |
| FA3 | SEBAGIAN | K3 | Reader manager+0x390 dan basis manager+0x2B4 dibedakan; writer tile+0x24 ditemukan | Arti tile+0x24 / manager+0x390 dan konsumen terminal belum dipetakan tuntas |
| FA4 | BELUM | K0 | Kegagalan pengambilan checkpoint CONTROL terdokumentasi | Tidak ada runtime launch/watchpoint/debit; CONTROL harus dipulihkan sebelum percobaan valid |
| FA5 | TUNTAS sebagai katalog hipotesis | K1 | Empat keluarga model dan falsifier ditulis | Rumus game tidak diketahui; tidak ada model yang menjadi rumus terverifikasi |

**Jawaban:** FA0, FA1, dan FA5 selesai sesuai cakupan masing-masing. FA2 dan FA3 tetap sebagian. FA4 belum selesai. Jadi keenam FA belum semuanya selesai.

## FA0 — ledger Git dan Actions

Dari baseline inklusif sampai HEAD 0491530cc2bc72338849046572422f5958e4a5b2: 6 commit = 5 manusia + 1 bot. Daftar urutan dan SHA penuh berada di FA0_FA5_GIT_LEDGER_2026-11-07.tsv.

Actions yang teridentifikasi dalam rentang:
- 42241745858 — Story Mode adaptive-player monitor, schedule, completed/success (run historis; tidak digunakan sebagai bukti ekonomi).
- 42292998488 — Story Mode adaptive-player monitor, schedule, completed/success (run historis; tidak digunakan sebagai bukti ekonomi).
- 42307609951 — DX0–DX4 full-image static economy audit, push, completed/success, source SHA f74961b844d068a164732c08c78a363d5267e569, script exit 0, EA exit 0.
- 42312284099 — FA4 H6 action-8 write-watchpoint runtime, push, completed/failure, source SHA 43d2bed4ceb468583ffa5a03730fdb07939e6677, exit 1. Rincian di FA4.

Tidak ada Actions run lain yang ditambahkan untuk laporan rekonsiliasi ini. Ledger Actions lengkap dan status final ada di FA0_FA5_ACTIONS_LEDGER_2026-11-07.tsv.

## FA1 — loader F020 dan nibble tile

- PC 0x800F7E64 memuat immediate 0xF020; PC 0x800F7E68 menyimpan halfword ke tile+0x20.
- Dari word 0xF020, nibble bit 4–7 bernilai 2 dan nibble bit 8–11 bernilai 0.
- Entry 1 file offset memakai rumus 0x10BB000 + (PC - 0x800AD450): 0x800F7E64 -> 0x010FFA14; 0x800F7E68 -> 0x010FFA18.
- Klasifikasi K4 statis. Ini bukan bukti makna gameplay level/owner dan tidak memperluas klaim ke semua tipe tile.

Run validasi statis 42307609951 menjalankan py_compile dua skrip yang tercatat dan analyzer EA keluar 0. Tidak ada run validasi duplikat.

## FA2 — F2A9C, helper 1552C, dan manager+0x2EE

### Dump dan pemanggilan

- Dump F2A9C mencakup 408 instruksi dari PC 0x800F2A9C sampai epilog 0x800F30F8. Contoh offset Entry 1 pada awal fungsi: 0x0110064C.
- Satu direct caller F2A9C yang ditemukan: JAL di PC 0x800F5F54, caller FUN_800F3658. Def-chain argumen caller sebelum call terputus oleh JAL 0x800E6DA4; argumen masuk F2A9C yang tidak dipulihkan tetap TIDAK TAHU.
- Empat call ke FUN_8001552C berada di PC 0x800F2B5C, 0x800F2CC8, 0x800F2DF0, dan 0x800F2E48.
- Pemeriksaan ulang straight-line caller menunjukkan setiap call menyiapkan $a0 dari field manager+0x530: PC 0x800F2B58, 0x800F2CC4, 0x800F2DEC, dan 0x800F2E44 masing-masing memuat lw $a0,0x530(manager). Pointer manager pada tiap jalur diturunkan dari slot global 0x8013EA74. Ini mempersempit asal indeks lookup; nilai runtime manager+0x530 tetap DINAMIS.

### Semantik helper dan koreksi offset

Disassembly Ghidra yang terarsip untuk FUN_8001552C (EXE SHA-256 a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569) menunjukkan:
1. memanggil FUN_800154D4 untuk memperoleh batas;
2. membandingkan parameter $a0 sebagai unsigned dengan batas tersebut;
3. bila parameter lebih kecil, mengambil u32 dari 0x80055CF4 + parameter*0x10 + 8;
4. selain itu mengembalikan nol.

**Koreksi audit:** DW2_FUN_8001552C_RAW.tsv sebelumnya memberi file offset 0x552C untuk PC 0x8001552C. Pemetaan EXE yang benar dalam proyek adalah 0x800 + (PC - 0x80010000), sehingga PC 0x8001552C berada pada offset 0x5D2C. Offset 0x552C kurang 0x800 dan tidak boleh dipakai sebagai byte-source untuk alamat 0x8001552C. Dengan itu, dua dump sebelumnya tidak membuktikan dua versi kode yang berbeda pada alamat yang sama; baris DW2 tersebut salah mapping offset. Bukti helper yang benar adalah dump Ghidra pada PC 0x8001552C dengan input SHA EXE sama. Jangan gunakan baris DW2 yang salah-offset sebagai disassembly helper.

### Debit

- PC 0x800F2CF8 menyimpan hasil perkalian helper-return dengan nilai dinamis dari global 0x8013EA71 dikurangi 2, ke manager+0x2EE dengan indeks/offset yang juga melibatkan global 0x8013EB0C.
- PC 0x800F2E38 menyimpan hasil perkalian yang operand $v0-nya sudah dibuat nol oleh negu $v0,$zero; baris ini bukan debit positif.
- PC 0x800F2E68 menyimpan negasi return helper ke manager+2*global 0x8013EB0C +0x2EE. Ini adalah kandidat perubahan nilai, tetapi belum diikat ke debit Chakra untuk d tertentu.
- Tidak ada bukti yang menghubungkan nilai helper/table secara deterministik ke perbedaan level d=1,2,3,4. Angka 400/800/1600 tidak digunakan sebagai bukti.

**Status FA2 tetap SEBAGIAN K3.** Empat sumber parameter helper kini terbukti sebagai manager+0x530 dan pemetaan helper dikoreksi, tetapi hubungan tabel/field dinamis dengan event upgrade serta rumus biaya d>=2 belum selesai. Rumus biaya = TIDAK TAHU.

## FA3 — tile+0x24, manager+0x2B4, manager+0x390

- Census EA3_MANAGER_PLUS2B4_PLUS390_PROVEN_CONSUMERS.tsv menunjukkan 15 direct read manager+0x390 dengan basis slot manager 0x8013EA74 pada PC: 0x800BBC78, 0x800BBD6C, 0x800BBE14, 0x800D1BEC, 0x800D1BFC, 0x800D1C68, 0x800D1C88, 0x800D1D5C, 0x800D1D6C, 0x800D1DDC, 0x800D1DFC, 0x800FA63C, 0x800FA7AC, 0x800FB004, 0x800FF268.
- Tidak ada read manager+0x2B4 yang basisnya terbukti berasal dari slot 0x8013EA74. Dua read +0x2B4 di PC 0x800B3438 dan 0x800B66E8 memakai slot basis 0x8013EAB0, jadi tidak boleh dicampur dengan objek manager EA74.
- Dua writer tile+0x24 pada PC 0x800F7E2C dan 0x800F7E40 memuat pasangan byte dari sumber dinamis lalu menyimpan halfword ke tile array (basis slot 0x8013EA84).
- Ada jalur yang membaca tile+0x24, mengurangi global dinamis 0x8013EAD2, lalu menyimpan hasil ke manager+0x2B4 dengan basis slot EAB0; jalur lain menyalin tile+0x24 ke manager+0x390 berbasis EA74. Ini menunjukkan penggunaan nilai pada jalur berbeda, bukan arti gameplaynya.
- Nilai manager+0x390 dibaca oleh enam fungsi: FUN_800BBC1C, FUN_800BBD9C, FUN_800D15A8, FUN_800FA4C8, FUN_800FAEBC, FUN_800FF00C. Rantai penggunaan nilai hasil load sampai konsumen terminal (koordinat/tampilan/ekonomi) belum direkonsiliasi untuk seluruh fungsi.

Hipotesis koordinat relatif, status tampilan/event, serta owner/level tetap K1 dan tidak boleh dipromosikan menjadi fakta. **Status FA3 tetap SEBAGIAN K3.**

## FA4 — runtime H6 write-watchpoint

Run 42312284099, job 128216422129, source SHA 43d2bed4ceb468583ffa5a03730fdb07939e6677, conclusion failure, exit code 1.

- Target checkpoint, PCSX, disc/CUE, dan BIOS lolos pemeriksaan hash.
- Download checkpoint CONTROL lama dari run 39867730674 gagal: Artifact not found for name: naruto-storymode-adaptive-player-private.
- Tahap ekstraksi PCSX, Xvfb, py_compile, dan script runtime dilewati.
- Peluncuran emulator = 0/8; watchpoint terpasang = 0/5; sampel event = 0; debit d=1..4 = tidak ada; timeout 360 detik hanya konfigurasi, bukan waktu launch aktual.
- Action 8 reachability = TIDAK DIUJI. Kegagalan mendapatkan checkpoint bukan bukti action 8 tidak dapat dicapai.
- Tidak ada retry. Release tidak memiliki CONTROL checkpoint alternatif; target checkpoint tidak boleh disubstitusi untuk CONTROL.

**FA4 tetap BELUM K0.** Prasyaratnya adalah mendapatkan kembali checkpoint CONTROL yang benar. Setelah itu workflow perlu memperbaiki publikasi fallback dan skrip harus lolos py_compile sebelum peluncuran baru.

## FA5 — keluarga model biaya dan falsifier

Empat hipotesis tetap dicatat dengan fee dasar simbolik C:

| Model | Faktor prediksi d=1,2,3,4 | Status |
|---|---|---|
| H1 linear per increment: C*d | 1,2,3,4 | K1 |
| H2 eksponensial: C*2^(d-1) | 1,2,4,8 | K1 |
| H3 akumulasi bertingkat: C*sum(2^k, k=0..d-1) | 1,3,7,15 | K1 |
| H4 lookup: C*L[d] | TIDAK DIISI | K1 |

Masing-masing punya falsifier di addendum FA0–FA5 sebelumnya. Tidak ada nilai d>=2 independen yang dipakai untuk fit. Model lookup tanpa tabel ROM independen tidak memprediksi apa pun. Angka pengguna 400/800/1600 bukan sampel verifikasi. Rumus biaya ROM tetap TIDAK TAHU.

## Integritas

- HEAD yang diaudit: 0491530cc2bc72338849046572422f5958e4a5b2; commit publikasi laporan ini akan menjadi commit setelah HEAD tersebut.
- STATUS.md tidak diubah.
- Release dan visibility repo tidak diubah.
- Tidak ada ISO, EXE, DATA.BIN, BIOS, savestate, Memory Card, RAM dump, gambar, video, frame, atau biner yang dikomit.
- Berkas baru laporan ini hanya Markdown dan TSV; tidak ada Actions baru yang dipicu oleh perubahan dokumen.
