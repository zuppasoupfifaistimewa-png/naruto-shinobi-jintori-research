# Audit statis ekonomi Stage 1 — Naruto vs Mizuki (31 Oktober 2026)

## Ruang lingkup
- Game: Naruto – Shinobi no Sato no Jintori Kassen (PS1), SLPS-03553.
- Fokus: Stage 1 saja; menelusuri pendapatan petak, biaya bangun Barrier, biaya upgrade Barrier, dan pemisahannya dari toll.
- Metode: inspeksi statis executable/resource dan dataflow MIPS melalui Ghidra pada GitHub Actions.
- Tidak ada game/emulator dijalankan; tidak ada input gameplay atau savestate dipulihkan.
- ROM, BIOS, Memory Card, savestate, RAM dump, video/audio, dan screenshot privat tidak dimasukkan ke repository. Binary sumber hanya diproses sementara pada runner dan dibersihkan; artefak workflow hanya teks/log.

## Status utama
**Belum ditemukan rumus biaya bangun, biaya upgrade, atau pendapatan petak yang bisa dinyatakan terverifikasi.** Audit entry 1 berhasil dan menambahkan dataflow kandidat, tetapi belum menghubungkan call chain ke transaksi Barrier atau penerimaan Chakra yang benar-benar terjadi saat gameplay. Audit helper lintas-resource masih berjalan pada saat laporan sementara ini dibuat.

## Run dan identitas input

### Run #41155800069 — static audit DATA.BIN entry 1
- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41155800069
- Status: completed / success.
- Job: 124402199996 — Verify release inputs, profile data files, scan entry-1 field immediates.
- Commit input: 2ea8aa554a2c9b45187e8d72815dd2282b56bd51.
- Seluruh langkah job completed/success; exit code job: **0**.
- Artefak teks: step6-resource-field-static-scan, ID 13024649665, 287.526 bytes.
- SHA-256 ZIP: 2a0ad3ba79e802d1c7e557fd8e37abbe3e514a4b256917ea962dde8c53339964 (cocok dengan digest API).
- Hasil scanner: field_offset_scan=PASS, stage1_economy_static_trace=PASS.
- Input identity:
  - Disc: 325.989.552 bytes; SHA-256 58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88.
  - DATA.BIN: 66.015.232 bytes; SHA-256 69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822.
  - Entry 1: offset 0x10BB000, 596.412 bytes; SHA-256 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a.
  - entry1_slice_identity=PASS; source_assets_removed_before_ghidra=PASS.
- Marker keselamatan output: game_or_emulator_executed=no, gameplay_input_sent=no, savestate_restored=no, private_binary_uploaded=no.

### Run #41155800065 — targeted DATA.BIN entry 0 helper context
- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41155800065
- Status pada saat laporan sementara ditulis: **in_progress**.
- Job: 124402199666 — Decode only candidate RNG/seed callsite windows.
- Commit input: 2ea8aa554a2c9b45187e8d72815dd2282b56bd51.
- Langkah 1–7 sukses; langkah 8 “Linear decode windows around the five candidate calls only” sedang berjalan. Belum ada exit code atau artefak hasil.
- Workflow memiliki timeout 15 menit dari 08:32:01 WIB; perkiraan batas konfigurasi sekitar 08:47:01 WIB, bukan jaminan selesai pada waktu tersebut.
- Run ini membandingkan helper di beberapa base resource kandidat. Semua base masih hipotesis; hasilnya tidak boleh dianggap runtime mapping sampai loader/payload relocation ditutup.

## Temuan audit entry 1

### 1. Pemanggilan langsung pada candidate resource view
Dengan base impor hipotetis 0x800D0000, scanner menemukan:
- 0x8001387C — 9 direct JAL caller.
- 0x800138EC — 16 direct JAL caller.
- 0x80012A70 — 8 direct JAL caller.
- 0x80012A44 — 0 direct JAL caller dalam rentang instruksi terdekode pada entry 1.
- 0x800BDC4C — 1 direct JAL caller.
- Scan hanya menghitung instruksi jal langsung; jalr/panggilan tidak langsung tidak termasuk.

Hitungan ini adalah call-site di resource import hipotetis, bukan bukti seluruh caller reachable pada runtime atau terkait transaksi Barrier.

### 2. Setter/getter peserta dan kemungkinan field Chakra
- 0x8001387C dan 0x800138EC merupakan pasangan setter/getter untuk word pada offset +0x18 dari struktur peserta stride 0xB4, dengan indeks 0–3.
- Audit ketat terdahulu menyatakan bentuk struktur dan akses field didukung statis; nama semantik “Chakra” belum dibuktikan sepenuhnya. Nilai 1.500 pada dua slot checkpoint cocok dengan nilai awal Stage 1, tetapi tidak sendirian membuktikan identitas field.
- Pada candidate entry-1 function 0x800D8918, return dari getter 0x800138EC(index) disalin ke participant-record field +0x04; record stride yang digunakan pada candidate view adalah 0x90. Fungsi ini juga menginisialisasi sejumlah field peserta dan mengirim beberapa nilai kembali ke setter/getter peserta.
- Karena ini semua di bawah base 0x800D0000 yang belum tervalidasi, makna field +0x04 sebagai nilai Chakra sangat didukung oleh hubungan producer/accessor, tetapi tetap merupakan interpretasi statis candidate view, bukan observasi runtime langsung.

### 3. Helper 0x800BDC4C sebagai kontribusi numerik kandidat
- Satu direct call pada entry 1 ditemukan di fungsi candidate 0x8012AAFC, memanggil 0x800BDC4C(selected_index).
- Fungsi yang sama mengambil nilai dari getter 0x800138EC(selected_index), menjumlahkan hasil helper dengan nilai getter itu, membatasi hasil ke -9.999..99.999, lalu meneruskannya ke helper tampilan 0x8001B364.
- Laporan trace terdahulu juga menemukan penggunaan helper yang sama dalam candidate threshold path: record[+0x04] + helper(selected_index) dibandingkan dengan configured target dari 0x80012A70; nilai +0x04 dihasilkan dari getter 0x800138EC pada candidate path.
- Ini merupakan bukti dataflow angka yang ditambahkan ke nilai peserta/Chakra kandidat dan menjadi kandidat penting untuk diteliti sebagai bonus/penyesuaian/proyeksi saldo.
- Tetapi belum dibuktikan bahwa helper itu menghitung pendapatan dari petak, toll, atau pendapatan per putaran. Fungsi 0x8012AAFC mempunyai penggunaan yang tampak seperti menyajikan/menggambar nilai (memanggil 0x8001B364), sehingga penjumlahan itu dapat berupa tampilan/perkiraan, bukan transaksi yang benar-benar mengkredit nilai peserta.
- Arti helper 0x800BDC4C, pointer pemilik data, dan base resource masih belum terselesaikan.

### 4. Kandidat perubahan nilai peserta yang belum dapat dinamai sebagai biaya
- Candidate 0x8011C0D0 mengubah suatu flag global dan, pada cabang tertentu, menegasikan word participant-record +0x04, membatasi nilai bawah ke -9.999, lalu memanggil setter 0x8001387C untuk record. Ini membuktikan operasi perubahan nilai dan clamping pada view kandidat, bukan bahwa operasi tersebut adalah biaya pembangunan/upgrade.
- Candidate 0x800E1188 memproses digit/countdown state yang berkaitan dengan participant-record +0x04, menyesuaikan nilai, dan memanggil setter/getter. Decompilation memperingatkan bad instruction/control flow; jangan gunakan pseudocode terpotong untuk menetapkan efek gameplay.
- Candidate 0x800D5608 dan 0x8010478C gagal didekompilasi karena masalah instruksi/batas fungsi. Raw instruction/call-site yang tersedia tidak cukup untuk memberikan label transaksi.

### 5. Candidate field pending +0xB30/+0xB38/+0xB40/+0xB44
- Bukti CFG/SSA sebelumnya pada fungsi 0x8012C544 menunjukkan load dari object +0xB30 dan +0xB38, penjumlahan, kemudian store ke +0xB40; pada initialization path +0xB44 di-zero-kan.
- Candidate 0x8012CACC membaca object +0xB44 dan meneruskannya ke 0x8001B364 pada guard tertentu.
- Trace terdahulu juga menemukan state yang memproses pending value dengan mengubah field peserta dan mengurangi pending value bertahap.
- Sumber pengisian +0xB30/+0xB38, identitas object pointer, dan aksi gameplay yang memicu state itu belum diketahui. Ini belum dapat disebut biaya bangun, biaya upgrade, toll, atau pendapatan.

### 6. Label teks resource
Literal ASCII berikut ditemukan dekat awal byte entry 1:
- ESTATE pada offset 0x14 dan 0x2D.
- LVUP_ESTATE pada 0x28.
- CHAKRA_DOWN pada 0x1C.
- FUUIN_GET pada 0x34.
- NINJYUTU pada 0x4C.
- KABE pada 0x58.

Kedekatan string tersebut di bagian awal resource tidak membuktikan bahwa ada handler dengan nama yang sama, dan tidak mengungkap biaya/rumusnya. Jangan hubungkan label ke call-site tanpa tabel dispatch/pemilik resource yang tervalidasi.

## Jawaban saat ini terhadap pertanyaan

| Pertanyaan | Hasil saat ini | Status |
|---|---|---|
| Bagaimana pendapatan petak dihitung? | Belum ada formula yang tertutup. Ada helper numerik per peserta yang ditambahkan ke nilai getter peserta sebelum nilai ditampilkan dan dibandingkan dengan target. Belum terbukti sebagai pendapatan petak. | **BELUM DIKETAHUI; kandidat numerik ditemukan** |
| Bagaimana biaya membangun Barrier? | Belum menemukan sumber biaya, pemeriksaan saldo, atau transaksi yang mengikat ke aksi build petak netral. Angka 60 berasal dari contoh UI/transkrip komunitas dan bukan konstanta universal yang terbukti. | **BELUM DIKETAHUI** |
| Bagaimana biaya upgrade Barrier? | Belum menemukan tabel/formula Level 1→2 sampai level berikutnya atau transaksi LVUP_ESTATE yang terhubung ke pengurangan nilai peserta. Angka 150 dari contoh upgrade komunitas hanya petunjuk satu kondisi. | **BELUM DIKETAHUI** |
| Apakah toll sama dengan pendapatan pemilik? | Belum dibuktikan. | **BELUM DIKETAHUI** |

## Langkah penutupan berikutnya
1. Audit hasil helper 0x800BDC4C di entry 0 di beberapa base kandidat, kemudian cocokkan dengan referensi caller dan lifecycle loader. Jangan terjemahkan helper sebagai income sebelum arti return dan consumer-nya tertutup.
2. Trace direct dan indirect callers dari struktur resource yang memiliki label ESTATE/LVUP_ESTATE, menggunakan daftar ID/dispatch yang benar; cek apakah kedua label berada di header/table atau executable logic.
3. Trace jalur transaksi petak: sumber angka harga → cek saldo → setter nilai peserta → mutasi owner/level/barrier → hasil UI.
4. Trace jalur pendapatan: peristiwa board/lap → iterasi petak milik → nilai level/toll/adjacency → akumulasi → setter/getter peserta.
5. Pisahkan toll yang dibayar ketika masuk wilayah lawan dari penghasilan owner ketika event pendapatan dijalankan.
6. Setelah call chain statis selesai, rancang eksperimen emulator satu variabel per percobaan. Tidak ada eksperimen runtime yang dijalankan sekarang.

## Files and outputs
Source script/workflow commit:
2ea8aa554a2c9b45187e8d72815dd2282b56bd51

Changed files in that commit:
- tools/step6/ExportStage1EconomyTrace.java
- .github/workflows/step6-resource-field-scan.yml
- .github/workflows/step4-ghidra-entry0-context.yml

This is a text-only interim report; it is not a claim that formulas or full gameplay rules are solved.


## Hasil Run #41155800065 — pemeriksaan lintas-resource helper (31 Oktober 2026)

- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41155800065
- Status: completed / success.
- Job: 124402199666 — Decode only candidate RNG/seed callsite windows.
- Commit input: 2ea8aa554a2c9b45187e8d72815dd2282b56bd51.
- Semua langkah job completed/success; exit code job: **0**.
- Artefak teks: step4-entry0-rng-context, ID 13024184283, 206.225 bytes.
- SHA-256 ZIP: 823ad3848388f832cf6e1a76d2be7b49fd1f06b1d26933150075e490010ca7f6 (cocok dengan digest API).
- Marker output: whole-program auto-analysis disabled, emulator/gameplay/input/savestate tidak dijalankan, binary tidak diunggah.
- Tujuan: mendecode target 0x800BDC4C di dua peta alamat candidate entry 0 yang berbeda, bukan memvalidasi loader runtime.

### Interpretasi pada base 0x800AD000
Pada impor Entry 0 dengan base hipotesis 0x800AD000, alamat 0x800BDC4C berada pada file offset 0x10C4C. Instruksi yang didecode di alamat itu:
- 0x800BDC4C: li a3, 6
- 0x800BDC50: j 0x800BE11C
- delay slot 0x800BDC54: li v0, 1
- kelanjutan di 0x800BE11C–0x800BE134 menghitung alamat relatif dari a0, menyimpan word ke a0+0x64 dan a0+0x68, lalu return 1.

Ini tampak seperti stub/initializer yang mengharapkan pointer/object pada a0, bukan jelas sebagai fungsi numerik berbasis indeks peserta. Namun candidate caller Entry 1 pada 0x8012AAFC (base Entry 1 juga hipotesis) tampak memanggil 0x800BDC4C dengan byte dari object +0x94A, lalu menggunakan byte yang sama pada getter peserta 0x800138EC yang membatasi indeks ke 0–3. **Konteks pointer-vs-index ini tidak konsisten.** Karena address map/pemanggil tidak tervalidasi runtime, jangan simpulkan bahwa stub ini benar-benar helper yang dipanggil pada jalur gameplay Stage 1.

### Interpretasi pada base 0x800B0450
Base 0x800B0450 berasal dari awal arena setelah bootstrap, tetapi bukan alamat payload/resource yang sudah dibuktikan. Pada peta ini:
- File offset 0x10C4C dipetakan ke 0x800C109C. Byte di sana berisi li a3,6; j 0x800BE11C; delay slot li v0,1; hasil lokal yang didecompile hanya return 1.
- Akan tetapi, literal call target 0x800BDC4C berada pada file offset **0xD7FC** (hasil aritmetika 0x800BDC4C - 0x800B0450), bukan offset 0x10C4C. Byte di 0x800BDC4C pada peta ini adalah NOP di tengah blok/fungsi yang lebih besar; ia bukan awal helper yang teridentifikasi. Dump fungsi luas ini juga memiliki warning overlap/bad instruction sehingga pseudocode gabungannya tidak dipakai sebagai semantic proof.
- Artefak memberi metadata target_offset_under_hypothesis=0xC7FC untuk literal 0x800BDC4C pada base ini. Itu **kesalahan metadata emitter/post-processing**; perhitungan alamat yang benar adalah 0xD7FC. Raw bytes dan alamat target tetap diperiksa langsung, tetapi offset tercetak tersebut jangan digunakan.

### Keputusan helper
Run ini **tidak mengonfirmasi** bahwa 0x800BDC4C menghitung pendapatan petak. Dua peta base yang diuji tidak memberi interpretasi yang cocok dengan pasangan caller/argumen:
- Pada base AD000, body mengakses field melalui pointer a0, sedangkan candidate caller memberi byte yang juga dipakai sebagai indeks peserta 0–3.
- Pada base B0450, literal target call berada di tengah fungsi, bukan function entry.
Dengan demikian, semantik helper 0x800BDC4C dan pemetaan resource tetap **UNKNOWN/BLOCKED**. Jalur penjumlahan getter + helper yang ditemukan di Entry 1 tetap hanya candidate dataflow; jangan namai sebagai income, rent, atau bonus pendapatan.

## Ringkasan dua run Actions pada commit 2ea8aa554a2c9b45187e8d72815dd2282b56bd51

| Run | Job | Status | Exit code |
|---|---|---|---:|
| #41155800069 | 124402199996 — static field/resource scan | completed/success | 0 |
| #41155800065 | 124402199666 — bounded Entry 0 helper decode | completed/success | 0 |

Kedua run selesai sukses secara tooling. Itu **bukan** berarti pertanyaan gameplay telah selesai; output yang berhasil adalah hasil audit statis dan kontrol keluaran, bukan verifikasi rumus biaya/pendapatan melalui emulator.

## Kesimpulan setelah kedua run
| Pertanyaan | Status final audit statis sesi ini |
|---|---|
| Rumus pendapatan petak Stage 1 | **BELUM DIKETAHUI** — helper penjumlahan kandidat belum terbukti sebagai pendapatan |
| Pemicu dan waktu pendapatan (lap/round/pass/landing) | **BELUM DIKETAHUI** |
| Biaya pembangunan Barrier | **BELUM DIKETAHUI** — belum ditemukan transaksi/rumus yang terhubung |
| Biaya upgrade Barrier per level | **BELUM DIKETAHUI** — belum ditemukan tabel/rumus LVUP_ESTATE yang terhubung |
| Toll petak lawan | **BELUM DIKETAHUI** — belum terbukti apakah sama dengan pendapatan pemilik |
| Mapping Entry 0/Entry 1 ke alamat runtime | **UNKNOWN/BLOCKED** |

Angka 60 (pembangunan) dan 150 (contoh upgrade Level 1→2) tetap merupakan nilai contoh dari UI/transkripsi komunitas yang dicatat sebelumnya, bukan angka yang berhasil diturunkan dari rumus kode. Toll 580 yang dilaporkan pada video juga tidak boleh disamakan dengan pendapatan.

Langkah berikutnya harus dimulai dari pemetaan loader/payload Entry 0 dan Entry 1 yang valid, lalu menautkan label ESTATE/LVUP_ESTATE ke dispatch handler yang benar. Setelah itu baru telusuri source price → balance check → participant setter → node owner/level mutation untuk biaya, serta board event → node ownership/level/toll → accumulator → setter untuk income. Eksperimen emulator Stage 1 baru dirancang setelah call chain ini cukup jelas dan gate runtime mengizinkan.

**Tidak ada gameplay/emulator atau input permainan dalam kedua run ini. Story Mode tidak dijalankan dan tidak dinyatakan selesai.**
