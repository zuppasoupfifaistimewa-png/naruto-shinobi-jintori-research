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
