# Laporan AR1–AR3 — audit statis dan runtime ekonomi Stage 1 (31 Oktober 2026)

Repository: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research  
Produk: Naruto – Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)  
HEAD awal dari prompt: 120dbabeb253f26435107d25b751a713d3d5d936  
Cakupan: hitung ulang akses record, audit call-site setter Chakra, dan dua peluncuran runtime H6 terbatas.

## Ringkasan hasil

| Bagian | Hasil | Batas kesimpulan |
|---|---|---|
| AR1(a) | 1.188 akses FIELD direkonsiliasi; 1.053 non-sp dan 135 sp | Hitungan operand/candidate, bukan bukti alias lengkap |
| AR1(b) | 97 function_entry unik vs metadata 98 | Fungsi ke-98 TIDAK TAHU |
| AR1(c) | 8 caller helper + 1 caller accessor dengan fungsi TIDAK TAHU | PC dan excerpt hingga 64 byte dicatat |
| AR2 | Semua 14 setter call-site diekspor dengan 12 instruksi pra-jal | 10 field-load; 4 manager path memakai hasil getter dan diklasifikasikan TIDAK TAHU dalam taksonomi yang diminta |
| AR3 | 2/2 peluncuran H6 mencapai frame 360, trace identik dan RAM SHA identik | K5 hanya untuk eksperimen H6 hybrid ini; bukan target-pure |

Tidak ada rumus yang diambil dari ucapan streamer atau transcript. Tidak ada angka ekonomi yang dipromosikan menjadi harga, pendapatan, toll, atau nilai release tanpa rantai kode/data yang mendukung.

## Skala bukti K0–K5

Skala lokal ini mengikuti konvensi Stage 1 sebelumnya:

- K0 — ringkasan visual sekunder yang belum dibaca ulang dari frame mentah.
- K1 — transcript/ASR atau teks terjemahan UI; belum menjadi pembacaan langsung.
- K2 — pembacaan langsung atas sedikitnya dua frame mentah yang berbeda.
- K3 — instruksi/data ROM statis dan aritmetika saling cocok, tetapi semantik atau pemetaan runtime belum tertutup.
- K4 — rantai statis sumber → pembaca → mutasi → penulis tertutup dan pemetaan resource memadai.
- K5 — pengamatan runtime terukur dan reproducible. Label K5 hanya berlaku untuk skenario, state, serta rentang uji yang benar-benar diulang.

AR1 dan AR2 paling tinggi K3. AR3 mencapai K5 untuk trace terbatas H6 di bawah; tidak mengangkat makna ekonomi game secara umum menjadi K5. K4 belum dicapai untuk rumus income, harga build/upgrade, maupun Barrier release.

## Provenance input statis

Sumber recount adalah:

reports/stage1_economy/aq1-run-41208394883/attempt-1/aq1-economy-census.tsv

Run statis AQ1:
- Actions run: 41208394883
- Job ID: 124558086018
- Job: Analyze verified Entry 1 slice at 0x800AD450
- Status: completed / success
- Exit code: 0
- Source SHA: a3cc4bfde7784858840e9cc98cc12e9bd70a2efe
- Entry 1 DATA.BIN slice: offset 0x10BB000, panjang 596.412 byte
- SHA-256 slice: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a
- Candidate import base: 0x800AD450; runtime mapping global tetap NOT VALIDATED.

## AR1 — recount akses +0x00 / +0x0B / +0x20

Metode: seluruh 1.188 baris FIELD dibaca ulang. Base register diambil dari operand memori pada instruksi yang diekspor. Register sp dipisahkan; gp dan fp dihitung terpisah. Kelompok non-sp berarti base yang bukan sp, gp, atau fp.

### AR1(a) tabel per-offset

READ / WRITE / OTHER untuk kelompok non-sp:

| Offset | READ | WRITE | OTHER | Total |
|---|---:|---:|---:|---:|
| +0x00 | 581 | 105 | 17 | 703 |
| +0x0B | 10 | 2 | 0 | 12 |
| +0x20 | 274 | 60 | 4 | 338 |
| **Total non-sp** | **865** | **167** | **21** | **1.053** |

Rekonsiliasi base lainnya:

| Base register | +0x00 R/W/O | +0x0B R/W/O | +0x20 R/W/O | Total |
|---|---|---|---|---:|
| sp | 1 / 2 / 0 | 0 / 0 / 0 | 80 / 51 / 1 | 135 |
| gp | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 |
| fp | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 |

Grand total semua base:
- READ = 946
- WRITE = 220
- OTHER = 22
- TOTAL = 1.188

Dengan demikian 1.188 cocok tepat: 1.053 non-sp + 135 sp + 0 gp + 0 fp. Ini adalah hitungan baris operand/candidate dalam cakupan scanner, bukan klaim bahwa seluruh 1.188 baris telah dibuktikan sebagai alias ke satu record pointer yang sama.

TSV hitungan lengkap:
reports/stage1_economy/AR1_BASE_OFFSET_ACCESS_COUNTS_2026-10-31.tsv

### AR1(b) selisih 97 vs 98 fungsi

Hitung ulang 1.188 baris FIELD menghasilkan 97 nilai function_entry unik. Baris TOTAL metadata scanner menyimpan record_slot_xref_function_count=98.

Fungsi ke-98: TIDAK TAHU.

Alasan: census memuat 97 function_entry dari baris FIELD dan hanya nilai agregat 98 dari metadata scanner. Tidak ada daftar independen 98 entry pembentuk recordFns dalam artefak ini yang dapat dibandingkan untuk mengidentifikasi entry yang hilang. Tidak ada fungsi yang saya tebak untuk menutup selisih tersebut.

### AR1(c) delapan helper caller + satu accessor caller yang fungsinya TIDAK TAHU

Semua function_entry dan function_name pada sembilan baris ini tetap TIDAK TAHU. Setiap excerpt adalah 64 byte atau kurang.

| Target | PC call-site | Entry fungsi | Excerpt hex |
|---|---|---|---|
| FUN_800B770C | 0x800CDD48 | TIDAK TAHU | C3 DD 02 0C 21 20 40 02 20 03 42 28 22 00 40 10 14 80 11 3C 74 EA 30 8E C0 10 14 00 21 10 54 00 00 11 02 00 04 00 10 26 21 80 02 02 C3 DD 02 0C 21 20 40 02 BC 02 42 24 00 00 03 8E 00 00 00 00 |
| FUN_800B770C | 0x800CDD74 | TIDAK TAHU | C3 DD 02 0C 21 20 40 02 BC 02 42 24 00 00 03 8E 00 00 00 00 2A 18 62 00 19 00 60 10 00 00 00 00 B4 4A 00 0C 00 00 00 00 01 00 42 30 15 00 40 10 14 80 10 3C 74 EA 22 8E 00 00 00 00 00 00 43 8C |
| FUN_800B770C | 0x800CDE84 | TIDAK TAHU | C3 DD 02 0C 21 20 40 02 80 20 13 00 18 00 A3 27 21 80 64 00 00 00 03 8E 00 00 00 00 18 FC 63 24 23 18 62 00 B4 4A 00 0C 00 00 03 AE 08 00 42 30 F6 00 40 10 14 80 02 3C 74 EA 44 8C 00 00 00 00 |
| FUN_800B770C | 0x800CDF90 | TIDAK TAHU | C3 DD 02 0C 21 20 40 02 80 18 13 00 18 00 A4 27 21 20 83 00 00 00 83 8C 00 00 00 00 21 10 43 00 CC 38 03 08 00 00 82 AC 14 80 11 3C 74 EA 24 8E 00 00 00 00 00 00 82 8C C0 80 12 00 21 80 12 02 |
| FUN_800B770C | 0x800CE084 | TIDAK TAHU | C3 DD 02 0C 21 20 40 02 80 18 13 00 18 00 A4 27 21 20 83 00 21 10 A2 02 00 00 83 8C 00 00 00 00 21 10 43 00 51 38 03 08 00 00 82 AC 74 EA 42 8C C0 20 14 00 21 20 94 00 00 21 04 00 21 20 44 00 |
| FUN_800B770C | 0x800CE11C | TIDAK TAHU | C3 DD 02 0C 21 20 40 02 80 18 13 00 18 00 A4 27 21 20 83 00 00 00 83 8C 00 00 00 00 18 FC 63 24 23 18 62 00 00 00 83 AC B4 4A 00 0C 00 00 00 00 08 00 42 30 4F 00 40 10 14 80 02 3C 74 EA 44 8C |
| FUN_800B770C | 0x800CE204 | TIDAK TAHU | C3 DD 02 0C 21 20 40 02 80 20 13 00 18 00 A3 27 21 80 64 00 00 00 03 8E 00 00 00 00 18 FC 63 24 23 18 62 00 B4 4A 00 0C 00 00 03 AE 08 00 42 30 16 00 40 10 00 00 00 00 74 EA A4 8E 00 00 00 00 |
| FUN_800B770C | 0x800FEB38 | TIDAK TAHU | C3 DD 02 0C FF 00 C4 32 84 EA 25 8E 00 00 00 00 21 28 05 02 22 00 A4 84 14 80 03 3C CE EA 63 84 00 00 00 00 23 20 83 00 48 FF 84 24 20 00 A3 8F 00 00 00 00 18 00 83 00 12 20 00 00 03 24 04 00 |
| GETTER 0x800138EC | 0x800EE54C | TIDAK TAHU | 3B 4E 00 0C 00 00 00 00 74 EA 25 8E 88 EA 04 96 00 00 00 00 C0 18 04 00 21 18 64 00 00 19 03 00 21 28 A3 00 B4 4A 00 0C 04 00 A2 AC 00 10 42 30 27 00 40 10 14 80 02 3C 0C EB 40 AC 14 80 02 3C |

TSV yang sama, dengan kolom byte-count terpisah:
reports/stage1_economy/AR1_UNKNOWN_CALLERS_2026-10-31.tsv

## AR2 — 14 pemanggil setter Chakra 0x8001387C

Ekspor Ghidra AQ1 diperluas untuk menyertakan tepat 12 instruksi sebelum tiap direct jal ke 0x8001387C, alamat setiap instruksi, mnemonic, dan byte instruksinya. TSV memuat 14 baris, termasuk delay-slot instruction setelah jal. Empat pemanggil manager +0xB44 adalah subset dari 14 tersebut, bukan empat call-site tambahan.

| PC setter call-site | Entry fungsi | Fungsi | Scope | Kategori asal a1 |
|---|---|---|---|---|
| 0x800B41B0 | 0x800B2A58 | FUN_800b2a58 | RECORD + PARTICIPANT +0x2EE | DIMUAT DARI FIELD RECORD |
| 0x800B4254 | 0x800B2A58 | FUN_800b2a58 | RECORD + PARTICIPANT +0x2EE | DIMUAT DARI FIELD RECORD |
| 0x800B4F00 | 0x800B2A58 | FUN_800b2a58 | RECORD + PARTICIPANT +0x2EE | DIMUAT DARI FIELD RECORD |
| 0x800B4F64 | 0x800B2A58 | FUN_800b2a58 | RECORD + PARTICIPANT +0x2EE | DIMUAT DARI FIELD RECORD |
| 0x800B6238 | 0x800B5D68 | FUN_800b5d68 | RECORD | DIMUAT DARI FIELD RECORD |
| 0x800BEC98 | 0x800BE5D8 | FUN_800be5d8 | PARTICIPANT +0x2EE | DIMUAT DARI FIELD RECORD* |
| 0x800DEB38 | 0x800DE760 | FUN_800de760 | RECORD | DIMUAT DARI FIELD RECORD |
| 0x800E1BE0 | 0x800E1958 | FUN_800e1958 | UNCLASSIFIED DIRECT CALLER | DIMUAT DARI FIELD RECORD |
| 0x800EC9A4 | 0x800EC574 | FUN_800ec574 | RECORD + PARTICIPANT +0x2EE | DIMUAT DARI FIELD RECORD |
| 0x800F95E8 | 0x800F9520 | FUN_800f9520 | UNCLASSIFIED DIRECT CALLER | DIMUAT DARI FIELD RECORD |
| 0x8010A15C | 0x80109FEC | FUN_80109fec | MANAGER +0xB44 | TIDAK TAHU |
| 0x8010A1B0 | 0x80109FEC | FUN_80109fec | MANAGER +0xB44 | TIDAK TAHU |
| 0x8010A638 | 0x80109FEC | FUN_80109fec | MANAGER +0xB44 | TIDAK TAHU |
| 0x8010A97C | 0x80109FEC | FUN_80109fec | MANAGER +0xB44 | TIDAK TAHU |

* Pada PC 0x800BEC98, a1 dibaca dari field +0x04 struktur participant (basis participant + indeks × 0x90). Ini field pada record participant, bukan tile record pada array 0x8013EA84. Rincian ini tidak boleh digabungkan dengan tile record stride 0x124.

### Asal a1 dan bukti instruksi

- 10 dari 14 call-site memperoleh a1 akhir melalui load field record yang dihitung dari base/index. Pada 0x800B6238, instruksi awal li a1,0x8 tertimpa sebelum jal oleh lw a1,0x4(v0), sehingga konstanta 8 bukan nilai akhir argumen.
- Tidak ada call-site yang memperlihatkan nilai akhir a1 berupa konstanta langsung.
- Tidak ada jendela pra-jal 12 instruksi yang memperlihatkan a1 akhir sebagai hasil FUN_800B770C.
- Empat call-site manager +0xB44 tetap diklasifikasikan TIDAK TAHU menurut pilihan kategori yang diminta, karena nilai a1 akhir dibentuk dari return getter 0x800138EC atau kombinasi return getter dengan field manager +0xB44:
  - 0x8010A15C: instruksi 0x8010A154 memuat lw a1,0xB44(v1); delay slot 0x8010A160 adalah addu a1,v0,a1. v0 berasal dari getter 0x800138EC sebelumnya. Jadi argumen akhir adalah hasil gabungan getter Chakra dan B44, bukan load field langsung.
  - 0x8010A1B0: delay slot 0x8010A1B4 adalah addu a1,v0,zero. Ini menyalin return getter 0x800138EC.
  - 0x8010A638: s1 telah dimuat dari manager +0xB44 pada 0x8010A610; delay slot 0x8010A63C adalah addu a1,v0,s1, dengan v0 dari getter sebelumnya.
  - 0x8010A97C: delay slot 0x8010A980 adalah addu a1,v0,zero, menyalin return getter sebelumnya.
- 12 instruksi pra-jal, instruksi delay-slot, dan kutipan instruksi untuk masing-masing 14 call-site tersimpan per baris di TSV.

TSV lengkap AR2:
reports/stage1_economy/AR2_SETTER_CALLERS_2026-10-31.tsv

### Konteks statis +0xB44

Audit statis sebelumnya (run 41166812039, exit 0) mengidentifikasi bahwa FUN_80109FEC menyalin manager +0xB40 ke +0xB44, lalu menerapkan B44 secara bertahap melalui getter Chakra 0x800138EC dan setter 0x8001387C. B44 berkurang bertahap setelah diterapkan. B40 sendiri dibentuk dari B30 + B38. Ini K3 untuk jalur field penyesuaian Chakra, tetapi asal B30/B38 dan pemicu event tetap TIDAK TAHU. Jalur tersebut tidak membuktikan B44 sebagai income, toll, refund, build/upgrade cost, atau nilai dari KABE/結界開放.

Semua empat setter manager di tabel berada pada FUN_80109FEC. Jangan menyimpulkan bahwa semua empat call-site memuat nilai B44 secara langsung; delay-slot dan getter mengubah nilai akhir a1 seperti dijelaskan di atas.

Label fungsi/transaksi build, upgrade, income, release: TIDAK TAHU. Tidak ada label semantik yang ditarik dari ucapan streamer.

## AR3 — runtime H6 hybrid: frame 180–360, dua peluncuran

### Identitas eksperimen

- Actions run: 41208953906
- Job ID: 124559715251
- Job identifier: ar3-h6-runtime-trace
- Status: completed / success
- Exit code script: 0
- Exit code emulator per peluncuran: 0 desimal
- Source SHA: a6002e5c016f9cdc954eec7c799e4e43df2464b5
- H6 SHA-256: d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475
- Definisi H6: target savestate base ditambah top-level protobuf SPU field 6 dari checkpoint CONTROL. H6 adalah HYBRID, bukan target-pure.
- Input gameplay: NONE.
- Metode: restore H6 secara terpisah pada dua peluncuran; pasang execution breakpoint pada 0x8001387C, 0x800138EC, dan 0x800B770C pada post-load frame 180; lanjut sampai frame 360; simpan hanya hash 2 MiB RAM pertama pada frame 360 dan event teks.
- Timeout setiap peluncuran: 900 detik.

### Hasil per titik breakpoint

| Titik | Launch 1 | Launch 2 |
|---|---:|---:|
| Setter 0x8001387C | 0 hit | 0 hit |
| Getter 0x800138EC | 360 hit | 360 hit |
| Entry FUN_800B770C | 0 hit | 0 hit |
| Exit FUN_800B770C | 0 hit | 0 hit |

Breakpoint logging berjalan; getter memberi 360 event pada masing-masing peluncuran. Event-frame yang tersimpan adalah 180 sampai 358 (90 frame bernomor genap); frame 360 adalah titik capture RAM dan penghentian eksperimen. Nol pada setter dan helper berarti nol event di alamat target yang dipantau selama eksperimen ini, bukan bahwa fungsi tersebut tidak pernah dipakai pada bagian atau state game lain.

### Register getter pada dua peluncuran

Semua event getter menyimpan PC, frame, ra, a0, a1, dan v0. Pada setiap peluncuran, dua RA berikut muncul 180 kali masing-masing:

| PC breakpoint | RA caller-return | Call-site jal yang cocok | Caller statis | Hit per launch |
|---|---|---|---|---:|
| 0x800138EC | 0x801053CC | 0x801053C4 | FUN_801052e8, entry 0x801052E8 | 180 |
| 0x800138EC | 0x80105420 | 0x80105418 | FUN_801052e8, entry 0x801052E8 | 180 |

Caller static census mengklasifikasikan FUN_801052e8 sebagai UNCLASSIFIED_DIRECT_CALLER. RA adalah return address setelah instruksi jal dan delay slot, sehingga call-site jal terkait adalah RA − 8.

Distribusi register per peluncuran:

- RA 0x801053CC: 180 hit; a0=0 sebanyak 90 dan a0=1 sebanyak 90; a1=0 sebanyak 90 dan a1=1 sebanyak 90; v0=0 sebanyak 180.
- RA 0x80105420: 180 hit; a0=0 sebanyak 90 dan a0=1 sebanyak 90; a1=0x801CEF08 sebanyak 180; v0=1 sebanyak 180.
- Pola event Launch 1 dan Launch 2 identik baris demi baris setelah kolom attempt diabaikan.

Karena setter 0x8001387C tidak menghasilkan event, tidak ada sampel register setter dari runtime ini. Karena entry FUN_800B770C tidak menghasilkan event, tidak ada breakpoint return yang dipasang untuk fungsi tersebut; nilai v0 saat helper exit adalah TIDAK TAHU.

### RAM SHA, exit code, waktu, dan timeout

| Ukuran | Launch 1 | Launch 2 |
|---|---|---|
| Capture post-load frame 360 | PASS | PASS |
| SHA-256 2 MiB pertama | 4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907 | 4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907 |
| Emulator exit code desimal | 0 | 0 |
| Timeout wrapper exit | 0 | 0 |
| Wall time | 145.815 s | 144.956 s |
| Memory Card unchanged | YES | YES |

Hash RAM frame 360 identik di dua peluncuran. Hash ini tidak cocok dengan baseline H6 frame 360 dari run sebelumnya: a9ac5282e9fb9ad1e77f46ef0c291af8e7e5f27b477b6b31e319f971e7dd9942. Hash pembanding yang diminta 16880faeccfca1fbd42d199c1543b00ec8a065bcd53545d14ea4657c9a6c2d5c juga tidak cocok; dalam data AK1/AK3, hash tersebut adalah frame 240, bukan frame 360. Penyebab perbedaan SHA dengan baseline lama: TIDAK TAHU; tidak dibuat dugaan.

Timeout 900 s melebihi 2 × waktu terlama historis 142.696 s (=285.392 s), dan juga melebihi 2 × waktu terlama dari dua peluncuran baru 145.815 s (=291.630 s).

Memory Card SHA sebelum/sesudah pada kedua peluncuran: ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5; tidak berubah. ISO, BIOS, Memory Card kerja, savestate, dan RAM buffer dihapus dari direktori sementara sebelum file teks hasil dikomit.

### Klasifikasi AR3

K5 untuk reproduksibilitas terbatas: dua restore H6 hybrid independen mencapai frame 360, memiliki event getter yang sama, hit counts sama, RAM SHA 2 MiB sama, emulator exit code 0, dan Memory Card tidak berubah. K5 ini tidak membuktikan semantik ekonomi, tidak mengubah H6 menjadi target-pure, dan tidak membuktikan setter/helper tidak berjalan di state lain.

File hasil runtime:
- reports/stage1_economy/ar3-h6-runtime-run-41208953906/attempt-1/ACTIONS_RUN_SUMMARY.txt
- reports/stage1_economy/ar3-h6-runtime-run-41208953906/attempt-1/AR3_H6_SUMMARY.txt
- reports/stage1_economy/ar3-h6-runtime-run-41208953906/attempt-1/AR3_LAUNCHES.tsv
- reports/stage1_economy/ar3-h6-runtime-run-41208953906/attempt-1/AR3_BREAKPOINT_EVENTS.tsv
- reports/stage1_economy/ar3-h6-runtime-run-41208953906/attempt-1/AR3_SCRIPT_EXIT_CODE.txt
- reports/stage1_economy/ar3-h6-runtime-run-41208953906/attempt-1/AR3_WORKFLOW_SCRIPT_PROCESS_EXIT.txt

### Riwayat setup AR3 yang tidak menjadi data runtime

Dua upaya setup sebelum run yang berhasil dicatat terpisah:
- Run 41208693098 berhenti sebelum pengunduhan input, karena ekspresi environment di YAML semula tersimpan dengan backslash dan permintaan GitHub API gagal HTTP 401. Tidak ada peluncuran emulator.
- Run 41208874219 berhasil mengunduh dan memvalidasi input privat tetapi berhenti sebelum emulator dijalankan karena import modul helper Python gagal (ModuleNotFoundError: No module named experiments). Script exit code 1; tidak ada hit runtime. Output teks placeholder disimpan di bawah reports/stage1_economy/ar3-h6-runtime-run-41208874219/attempt-1/.
- Run 41208953906 menggunakan perbaikan ekspresi workflow dan import lokal. Hanya dua peluncuran pada run terakhir inilah yang dihitung untuk K5.

## Hubungan dengan AQ1–AQ3 sebelumnya

Laporan AQ1–AQ3 dibaca ulang sebelum audit ini. Konteks yang tetap berlaku:
- AQ2 sebelumnya menghasilkan dua snapshot H6 frame 180 identik, tetapi H6 juga hybrid. Hasil AR3 tidak boleh dianggap sebagai target pure.
- AQ3 sebelumnya gagal inspeksi langsung frame mentah; seluruh saldo, harga, dan nilai release yang tidak terbaca tetap TIDAK TAHU.
- Formula FUN_800B770C adalah per-record arithmetic statis K3; fungsi agregator FUN_800BDC4C dan renderer fee negatif tidak membuktikan kredit/debit saldo aktual.
- +0xB44 dan +0x2EE merupakan struktur/field yang berbeda. +0xB44 adalah penyesuaian Chakra bertahap K3; pemicu/sumber B30/B38 tetap UNKNOWN. +0x2EE adalah field participant array terpisah yang diproses pada jalur lain dan punya batas decompiler.
- Tidak ada bukti yang menghubungkan +0xB44 atau +0x2EE secara pasti ke income, build/upgrade, atau KABE/結界開放.

## Kesimpulan akhir per pertanyaan

1. AR1 selesai sebagai recount yang dapat diaudit. Selisih fungsi 97 vs 98 belum terjelaskan, dan sembilan caller dengan penetapan fungsi yang hilang tetap TIDAK TAHU.
2. AR2 selesai untuk 14 setter call-site dan empat caller manager +0xB44. Semua 12 instruksi pra-jal beserta delay-slot ada pada TSV. Sepuluh sumber a1 berasal dari field record; empat manager caller memakai hasil getter dan/atau campuran getter+B44 sehingga klasifikasinya TIDAK TAHU dalam kategori yang diminta.
3. AR3 selesai untuk dua peluncuran H6 hybrid. Setter dan FUN_800B770C mencatat nol hit pada rentang yang diuji; getter mencatat 360 hit tiap peluncuran. SHA RAM frame360 dua launch sama, tetapi tidak cocok dengan dua hash pembanding. H6 tetap hybrid.

Pertanyaan ekonomi yang belum dapat dijawab secara terverifikasi: pendapatan pemilik petak, harga build, harga tiap level upgrade, nilai Chakra release, asal event yang mengisi B30/B38, makna field +0x0B, dan apakah release otomatis atau pilihan pemain. Semua tetap TIDAK TAHU.

## Ledger commit dan berkas yang berubah

Setiap commit di bawah dibatasi ke file yang tercantum. Tidak ada perubahan Release atau visibilitas repository.

| Commit SHA penuh | Berkas yang diubah |
|---|---|
| a3cc4bfde7784858840e9cc98cc12e9bd70a2efe | tools/step7/ExportStage1EconomyAQ1.java |
| 612c193c7b72d9791e531d42a7939d2136c4b6f5 | experiments/ar3_h6_runtime_trace.py |
| a7f42355b58541f0558125a34c8574245d6835b8 | .github/workflows/ar3-h6-runtime-trace.yml |
| 2406c86ef5595dae296497734f54c3638b38a6a1 | .github/workflows/ar3-h6-runtime-trace.yml |
| a6002e5c016f9cdc954eec7c799e4e43df2464b5 | experiments/ar3_h6_runtime_trace.py |
| 20d9156fe28275e080376f3e931007b0fb4d1b10 | reports/stage1_economy/ar3-h6-runtime-run-41208874219/attempt-1/ACTIONS_RUN_SUMMARY.txt; AR3_BREAKPOINT_EVENTS.tsv; AR3_H6_SUMMARY.txt; AR3_LAUNCHES.tsv; AR3_WORKFLOW_SCRIPT_PROCESS_EXIT.txt |
| d1faa0e4500fbd3899937b1c55163b43edb4ac93 | reports/stage1_economy/AR2_SETTER_CALLERS_2026-10-31.tsv |
| b6785f741a3e325ab3ed1ddd7dc620225157f249 | reports/stage1_economy/AR1_BASE_OFFSET_ACCESS_COUNTS_2026-10-31.tsv |
| 23256848bcf298aee545bad447669eb26c3da2c7 | reports/stage1_economy/AR1_UNKNOWN_CALLERS_2026-10-31.tsv |
| dbdcd9f49fa7d8edf7cd2ebf264fb6d32a17dd0a | reports/stage1_economy/ar3-h6-runtime-run-41208953906/attempt-1/ACTIONS_RUN_SUMMARY.txt; AR3_BREAKPOINT_EVENTS.tsv; AR3_H6_SUMMARY.txt; AR3_LAUNCHES.tsv; AR3_SCRIPT_EXIT_CODE.txt; AR3_WORKFLOW_SCRIPT_PROCESS_EXIT.txt |
| d3477f4522a01009416da22aec18890671e31426 | reports/stage1_economy/aq1-run-41208394883/attempt-1/ACTIONS_RUN_SUMMARY.txt |
| 8a6e64d0a844394af8376da730a0e714ca80fa6c | reports/stage1_economy/ar3-h6-runtime-run-41208953906/attempt-1/ACTIONS_RUN_SUMMARY.txt |

Commit laporan ini menambahkan satu file:
reports/stage1_economy/AR1_AR2_AR3_FINAL_REPORT_2026-10-31.md

## Safety and repository boundary

Tidak ada perubahan Release/visibilitas repository. Tidak ada ISO, BIOS, Memory Card, savestate, dump RAM, video, atau frame image yang dikomit. File output yang dipublikasi hanya source script/workflow penelitian, laporan Markdown, teks ringkasan, dan TSV. Hash yang dicatat adalah digest saja; bukan data RAM mentah.
