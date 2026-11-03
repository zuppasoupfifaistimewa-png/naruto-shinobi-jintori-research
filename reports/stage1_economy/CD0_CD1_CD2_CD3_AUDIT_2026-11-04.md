# CD0–CD3 — audit pemicu, kredit, biaya, dan cakupan runtime
Tanggal: 4 November 2026
Game: Naruto — Shinobi no Sato no Jintori Gassen (SLPS-03553)
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Baseline SHA-1: c7457a73d6378ee62be4f344add796c132ed0144

## Putusan singkat

| Butir | Status | K | Putusan |
|---|---|---:|---|
| CD0 Actions probe | TUNTAS | K4 | Workflow baru terpicu oleh push, job sukses, exit 0; summary dikomit. |
| CD1(a) direct caller + branch | TUNTAS | K4 | FUN_800F3658, switch manager+0x2E9 == 9, JAL di 0x800F5DAC. |
| CD1(b) indirect caller | SEBAGIAN | K3 | Pemindaian bounded EXE/Entry1/DATA mentah menghasilkan nol kandidat pada cakupan terukur; bentuk pointer runtime/tertransformasi belum ditutup. |
| CD1(c) producer event | SEBAGIAN | K3 | Producer 3, 8, 0x1D teridentifikasi; producer event 1 dan satu writer event 8 belum teridentifikasi batas fungsinya. |
| CD1(d) tiga pemicu pengamatan | BELUM | K1 | Kristal, petak sendiri, akhir putaran tetap hipotesis; belum terikat satu-ke-satu ke event. |
| CD1(e) token 0xBE | SEBAGIAN | K4/K0 | Argumen 0xBE ke helper pesan terbukti; teks Jepang dan maknanya tidak diketahui. |
| CD1(f) identitas Barrier Release | BELUM | K1 | Jalur kredit positif terbukti, label gameplay “Barrier Release” TIDAK TAHU. |
| CD2(a) debit dan a1 setter | TUNTAS | K4 | Action 3/8 mengantrekan -u16(tile+0x1A); a1 setter = saldo kerja lama - fee. |
| CD2(b) pengali m(d) | TUNTAS untuk blok 3/8 | K4 | Tidak ada m(d) di blok transaksi yang diperiksa; fee dibaca flat dari +0x1A. |
| CD2(c) relasi TSV 22 record | TUNTAS | K3 | Dua relasi 0,7 konstan ditemukan; field level +0x10..+0x18 tidak memiliki rasio konstan ke +0x0E. |
| CD2(d) producer biaya build netral | BELUM | K1/K2 | Event 3 adalah kandidat jalur transaksi, tetapi label build dari petak netral belum dibuktikan. |
| CD3 runtime kredit | BELUM | K0 | Tidak ada launch runtime kredit dalam sesi ini; harness H6 yang tersedia hanya menguji debit 3/8. |

Skala bukti: statis maksimum K4; K5 mensyaratkan hasil runtime konsisten pada sedikitnya dua peluncuran. Tidak ada hasil K5 baru dalam laporan ini.

## CD0 — probe trigger Actions

Workflow baru:
- Berkas: .github/workflows/cc4-probe.yml
- Commit workflow SHA-1: 7ec489f7f4df87f41677446be413a1fb5383be62
- Run ID: 41728269961
- Job ID: 126238638640
- Event: push
- Workflow/job: completed / success
- Job: “CD0 echo and summary”
- Source SHA-1: 7ec489f7f4df87f41677446be413a1fb5383be62
- Exit code: 0
- Summary text commit SHA-1: 181d3c4bbe78993a0c8c55c53baaddb1e34b97a4
- Summary file: reports/stage1_economy/cd0-run-41728269961/attempt-1/ACTIONS_RUN_SUMMARY.txt

CD0 TUNTAS K4. Ini membuktikan jalur push path filter workflow baru bekerja; tidak membuktikan workflow analisis lain selalu sehat.

## CD1(a) — caller langsung FUN_800D15A8

Fungsi pemanggil: FUN_800F3658, entry/prolog 0x800F3658.
Kondisi dispatch yang masuk ke pemanggilan: switch pada byte manager+0x2E9, case 9. Case 9 menjalankan FUN_800D15A8().

Cuplikan raw MIPS 16 byte (≤64 byte), PC 0x800F5DAC:
~~~
800F5DAC [6A 45 03 0C] jal 0x800d15a8
800F5DB0 [00 00 00 00] nop
800F5DB4 [17 D8 03 08] j 0x800f605c
800F5DB8 [00 00 00 00] nop
~~~

Kondisi di atas adalah kondisi switch case pada fungsi caller; bukan klaim bahwa urutan instruksi tepat sebelum JAL sendiri merupakan guard lengkap. Status TUNTAS K4 statis.

## CD1(b) — pencarian caller tak langsung

Scanner: tools/step7/ScanIndirectCallCandidates.py.
Run yang benar-benar menjalankan scanner: 41730277650.
Source SHA-1 workflow: f3e666a653b66566cccc56ca386e2275cfb440bc.
Bot output commit SHA-1: 7c0f0bf9236efc2ae39977d82218884d014313fb.
Hasil scanner: reports/stage1_economy/aq1-run-41730277650/attempt-1/cd1-raw-indirect-call-candidates.txt.

Cakupan dan hasil:
- EXE: 385.024 byte; area kode yang discan raw offset 0x800, panjang 0x5D800; 176 instruksi JALR; 0 register-target match persis.
- Entry 1: 596.412 byte pada kandidat mapping statis base 0x800AD450; 37 instruksi JALR; 0 register-target match persis.
- Area kode EXE dan Entry 1: 0 aligned literal pointer word 0x800D15A8.
- DATA.BIN mentah: 66.015.232 byte; 0 kemunculan literal pointer 0x800D15A8 baik aligned maupun unaligned.
- Rekonstruksi konstanta terbatas pada 24 instruksi aligned sebelumnya dan pola LUI+ADDIU, LUI+ORI, serta salinan register ADDU/OR.

Batas penting:
- Entry 1 base 0x800AD450 adalah kandidat static import mapping; mapping runtime belum divalidasi pada scan ini.
- Pointer yang dimuat dari memori/tabel saat runtime, relocated pointers, computed offsets, register flow lebih panjang dari 24 instruksi, dan indirect call yang dibentuk lewat transformasi tidak dikesampingkan.
- DATA.BIN dipindai sebagai arsip mentah untuk kata pointer; entri terkompresi tidak didisassembly sebagai kode.
- Karena batas ini, hasil nol hanya berarti tidak ada kandidat yang memenuhi metode dan cakupan tersebut, bukan bukti global tidak ada indirect caller.

EXE SHA-256: a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569
Entry 1 SHA-256: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a
DATA.BIN SHA-256: 69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822

Status SEBAGIAN K3: pencarian bounded selesai, asal panggilan tak langsung belum ditutup secara menyeluruh.

## CD1(c) — produser event pada manager+0x2EB

| Event | PC store | Fungsi | Kepastian |
|---|---:|---|---|
| 3 | 0x800DAA88 | FUN_800D9570 | batas fungsi dan store teridentifikasi |
| 8 | 0x800EC3A8 | FUN_800EB434 | batas fungsi dan store teridentifikasi |
| 8 | 0x800EF3CC | TIDAK TAHU | store teridentifikasi; batas fungsi belum diketahui |
| 1 | 0x800CF94C | TIDAK TAHU | store +0x2EB; instruksi sebelumnya memuat kandidat 1; boundary tidak ada |
| 0x1D | 0x800E0928 | FUN_800E03B0 | batas fungsi dan store teridentifikasi |

Detail tambahan:
- Event 1 juga menyimpan nilai 1 ke manager+0x2EA pada PC 0x800CF940; byte +0x2EB=1 ditulis pada PC 0x800CF94C.
- Event 0x1D juga menyimpan 0x1D ke manager+0x2EA pada PC 0x800E091C; byte +0x2EB=0x1D ditulis pada PC 0x800E0928.
- Event 8 di 0x800EC3A8 berasal dari FUN_800EB434. Jalur producer menguji petak tipe 5 milik pemain aktif dan level bits 8–11 di bawah 4; label fungsi gameplay sebagai upgrade Barrier didukung oleh konteks kode.
- Event 3 di 0x800DAA88 berasal dari FUN_800D9570. Ia masuk blok transaksi yang sama dengan 8, tetapi belum ada bukti satu-ke-satu bahwa semua event 3 adalah bangun Barrier dari petak netral.

Status SEBAGIAN K3.

## CD1(d/f) — hipotesis pemicu dan identitas Release

Semua pengamatan pengguna di bawah tetap HIPOTESIS K1, bukan fakta runtime dalam sesi ini.

### Pengamatan: berhenti di bola kristal
- H1: pemicu menulis event 1 melalui kandidat store 0x800CF94C, lalu masuk cabang kredit.
- H2: pemicu menulis event 0x1D melalui FUN_800E03B0 di 0x800E0928, lalu masuk cabang kredit.
- Falsifier: trace PC dan manager+0x2EB saat pemain melewati kristal menunjukkan tidak ada event 1/0x1D atau menunjukkan event lain.

### Pengamatan: berhenti di petak sendiri
- H1: handler petak sendiri menulis event 1.
- H2: handler tersebut menulis event 0x1D.
- Falsifier: trace kondisi owner/type/level pada petak yang dipilih dan byte +0x2EB membuktikan handler menggunakan event lain atau tidak memasuki cabang kredit.

### Pengamatan: akhir putaran
- H1: akhir putaran mengirim event 1 atau 0x1D ke jalur kredit.
- H2: akhir putaran hanya mengakhiri giliran/menjalankan event lain dan bukan pemicu kredit ini.
- Falsifier: trace batas putaran memperlihatkan event byte, producer PC, dan signed pending +0x2EE; bila tidak menuju state kredit 1/2, H1 gugur.

### Identitas event sebagai Barrier Release
- H1: event 1/0x1D adalah Barrier Release; C merupakan hasil pelepasan Barrier.
- H2: event 1/0x1D merupakan aksi positif lain (misalnya konversi/cashout tile), bukan Release.
- Falsifier: pemetaan teks pesan 0xBE dan trace perubahan status/owner/Barrier sebelum-sesudah pada gameplay normal. Prompt/teks yang mengidentifikasi aksi selain Release menggugurkan H1; prompt Release yang sinkron dengan event dan perubahan Barrier menggugurkan H2.

Putusan CD1(f): TIDAK TAHU. Kode statis membuktikan cabang kredit positif untuk event 1/0x1D; belum membuktikan nama “Barrier Release”.

## CD1(e) — token pesan 0xBE

Di FUN_800D15A8:
- PC 0x800D4970: JAL FUN_80100DCC.
- Delay slot 0x800D4974: li a0,0xBE.
- Setelahnya fungsi memanggil FUN_80100D14(1) dan FUN_80108EE8().

Tabel pesan konservatif:
| Event | PC | Helper | Token | Teks Jepang |
|---|---:|---|---:|---|
| 1 / 0x1D | 0x800D4970 | FUN_80100DCC | 0xBE | TIDAK TAHU |

Census objek pesan dan scan teks DATA.BIN yang tersedia belum membuktikan string Jepang untuk token tersebut. Token numerik tidak boleh diterjemahkan sebagai “結界開放” tanpa bukti.

## CD2(a/b) — debit dan a1 setter

Pada FUN_800D15A8, event 3 dan 8 masuk blok transaksi bersama:
- Membaca fee u16(tile+0x1A).
- Memeriksa saldo kerja pemain terhadap fee.
- Menaruh signed pending delta -fee di manager+0x2EE + playerIndex*2.
- Menaikkan nibble bits 8–11 dan nibble bits 4–7 di tile+0x20 sebesar satu langkah masing-masing.
- Tidak ada operasi fee×m(d), sllv fee, atau tabel multiplikasi level pada blok transaksi tersebut.

FUN_800BE5D8 memproses antrean pending signed. Callsite ke setter FUN_8001387C ada di PC 0x800BEC98; lw a1,0x4(v0) tepat sebelumnya (0x800BEC94). v0 menunjuk participant manager + playerIndex×0x90. Maka:
- Action 3/8: a1 = saldo_kerja_lama - u16(tile+0x1A).
- Jalur kredit event 1/0x1D: a1 = saldo_kerja_lama + C, setelah pending positif diproses.

### Hipotesis pengali m(d)
- H1: d=1 → 1×base; d≥2 → base<<d (4×/8×/16× untuk d=2/3/4). Falsifier: instruksi transaksi membaca fee tetap tanpa menghitung d atau runtime pada level berbeda menunjukkan debit tetap.
- H2: tabel m(d)={1,4,8,16}. Falsifier: tidak ada table lookup/branch keyed on d di jalur yang sama, dan operand debit tetap field +0x1A.
- H3: tidak ada multiplier level; debit menggunakan fee petak +0x1A langsung. Didukung K4 untuk blok event 3/8 yang diperiksa. Falsifier: penelusuran lanjutan pada jalur transaksi yang sama menemukan multiplication/table sebelum pending write.

H1/H2 tidak cocok dengan blok transaksi 3/8 yang dianalisis; H3 didukung di cakupan itu. Kesimpulan tidak digeneralisasi ke setiap aksi Barrier yang belum diidentifikasi.

### Status formula biaya Barrier
- Upgrade Barrier action 8: debit flat u16(tile+0x1A), K4.
- Action 3: memakai blok debit sama; label gameplay action 3 tetap TIDAK TAHU.
- Build dari petak netral: TIDAK TAHU. Action 4 membaca +0x0E di FUN_800D15A8 untuk helper UI/preview; di blok event4 yang diperiksa tidak ada pending debit negatif. Ini tidak membuktikan +0x0E sebagai biaya build.

Dua hipotesis untuk build netral:
- H1: event 3 adalah bangun Barrier dari petak netral dan field +0x1A menjadi biaya.
- H2: event 3 adalah operasi tile lain yang berbagi blok debit dengan upgrade action 8.
Falsifier: trace kondisi awal petak, prompt/UI, event byte, fee pending, dan perubahan tile saat melakukan satu aksi build normal. Jika tile netral tidak menghasilkan event 3, H1 gugur; jika prompt build dan transisi netral→Barrier terikat ke event 3, H2 gugur.

## CD2(c) — penghitungan ulang relasi TSV 22 record

Sumber: reports/stage1_economy/CB1_RESOURCE_FIELDS_22_RECORDS_2026-11-03.tsv.
- 22 record; 17 record nonnol dan 5 record kolom terkait semuanya nol.
- +0x1E = 0,7 × +0x0E tepat pada 17/17 record nonnol; lima record nol juga cocok.
- +0x1C = 0,7 × +0x1A tepat pada 17/17 record nonnol; lima record nol juga cocok.
- Untuk +0x10, +0x12, +0x14, +0x16, +0x18, masing-masing rasio ke +0x0E tidak konstan pada 17 record nonnol.
- Relasi rasio konstan di atas adalah observasi data K3, bukan bukti bahwa game menghitung field tersebut dari field lain saat transaksi.

Status TUNTAS K3 untuk korelasi TSV; bukan bukti runtime atau producer.

## CD3 — runtime H6

Gerbang CD0 lulus, tetapi CD3 tidak dapat diklaim selesai.
- H6 fixture SHA-256 yang dirujuk oleh harness terdahulu: d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475 (HIBRIDA, bukan target murni).
- Harness tersedia experiments/bb3_h6_action_call_probe.py hanya menguji debit event 3/8 dan level nibble; ia tidak menguji event 1/0x1D sampai pending positif diproses ke PlayerRecord Chakra.
- Jalur kredit butuh state 1 (hitung C), state 2 (manager+0x370==1 dan FUN_80102408()==0), lalu pemrosesan pending oleh FUN_800BE5D8. Belum ada harness tervalidasi untuk menjalankan siklus tersebut pada record 4 dan 7 level 0..4 di dua peluncuran.
- Karena itu tidak ada hasil peluncuran, kode keluar, poke log, RAM SHA-256 frame 180/360, atau Memory Card SHA-256 baru untuk CD3 pada sesi ini.
- Angka kredit statis tetap: record 4 = 84/154/224/294/364; record 7 = 112/196/280/364/448; proyeksi player awal 1500 menjadi 1584/1654/1724/1794/1864 untuk record 4. Ini bukan klaim hasil runtime.
- Optional debit prices 120 and values 100/400/800/1600 were not tested in this CD3 run.
- Kelas CD3 BELUM K0. Tidak ada run emulator baru yang harus diberi label K5.

## Status Actions dan error yang tidak disamarkan

1. Run 41728269961 — job 126238638640 — source SHA-1 7ec489f7f4df87f41677446be413a1fb5383be62 — SUCCESS — exit 0.
2. Run 41729541613 — job 126242985654 — source SHA-1 de1e4c9568e543b6dc5af6f7c54c25e5123cbd11 — FAILURE — exit 127. Error mentah: /home/runner/work/_temp/24e23679-4075-4bfa-9880-b49922bab328.sh: line 241: bounded: command not found. Summary status scanner untuk run ini dikoreksi menjadi NOT_RUN.
3. Run 41729988835 — job 126244498612 — source SHA-1 95e6d8a2277cb4efa985f8a47277ff9f2089f362 — SUCCESS — exit 0. Run dimulai sebelum invocation scanner masuk workflow; summary dikoreksi menjadi CD1 scanner NOT_RUN.
4. Run 41730277650 — job 126246081862 — source SHA-1 f3e666a653b66566cccc56ca386e2275cfb440bc — FAILURE — exit 1. Scanner CD1(b) sudah selesai dan menulis output PASS, tetapi tahap Ghidra selanjutnya gagal: java.lang.NullPointerException: Cannot invoke "ghidra.program.model.listing.Instruction.getAddress()" because "i" is null pada ExportStage1EconomyDeepContext.java:24 (recoverExplicitRecordSlotEA84:39). Summary diperbaiki untuk menyatakan job failure exit 1 sambil mempertahankan scanner PASS. Input private dan project sementara dibersihkan; tidak ada binary diunggah.

## Batasan dan integritas artefak

- Semua perubahan yang dibuat pada sesi ini berupa teks: YAML workflow, Python scanner, Markdown/TSV/CSV/TXT hasil analisis dan ringkasan.
- Tidak mengunggah/mengubah ISO, ROM, BIOS, savestate, RAM dump, Memory Card, video, screenshot/frame, atau data biner.
- Tidak ada operasi Release atau perubahan visibilitas repository.
- STATUS.md tetap 693.844 byte (693844 B); tidak diubah.
- Kelas hash: commit di laporan adalah SHA-1 40 hex; file input/output yang disebut SHA-256 64 hex.
- Status negatif selalu dibatasi pada cakupan scan/branch yang disebutkan.

## Ledger commit sejak baseline

Empat belas commit dibuat sebelum laporan ini:
1. 7ec489f7f4df87f41677446be413a1fb5383be62 — .github/workflows/cc4-probe.yml
2. 181d3c4bbe78993a0c8c55c53baaddb1e34b97a4 — reports/stage1_economy/cd0-run-41728269961/attempt-1/ACTIONS_RUN_SUMMARY.txt
3. 1b1341cdab80da2c92004edf3364a584cf8e3e2f — tools/step7/ScanIndirectCallCandidates.py
4. de1e4c9568e543b6dc5af6f7c54c25e5123cbd11 — .github/workflows/step7-entry1-buffer-base-audit.yml
5. eeba76256c6b2c7299c65e4e30db0f36dd42b7f — 57 text outputs under reports/stage1_economy/aq1-run-41729541613/attempt-1/ (file names listed below)
6. 95e6d8a2277cb4efa985f8a47277ff9f2089f362 — .github/workflows/step7-entry1-buffer-base-audit.yml
7. ab0ac17c29dc96ec6b727b631a8feba72943394c — reports/stage1_economy/aq1-run-41729541613/attempt-1/ACTIONS_RUN_SUMMARY.txt
8. f3e666a653b66566cccc56ca386e2275cfb440bc — .github/workflows/step7-entry1-buffer-base-audit.yml
9. cc5f979c2b55fc31909950582ba23a85df8aeb7e — 57 text outputs under reports/stage1_economy/aq1-run-41729988835/attempt-1/ (same relative names below)
10. 83182ea678cb820c498f4d44801503b286036d00 — reports/stage1_economy/aq1-run-41729988835/attempt-1/run-summary.txt
11. fffa1b6bfbb5ea23b27db89fbd12c138e881097b — reports/stage1_economy/aq1-run-41729988835/attempt-1/ACTIONS_RUN_SUMMARY.txt
12. 7c0f0bf9236efc2ae39977d82218884d014313fb — 38 text outputs under reports/stage1_economy/aq1-run-41730277650/attempt-1/ (file names listed below)
13. a433ec2c7a0a1a557c3d784570bc5c1d133948d4 — reports/stage1_economy/aq1-run-41730277650/attempt-1/run-summary.txt
14. 072b251e620c86cbe72742ffccfe74282445b7ea — reports/stage1_economy/aq1-run-41730277650/attempt-1/ACTIONS_RUN_SUMMARY.txt

Relative filenames for both 57-file bot commits (prefix each name with its own run-specific path shown in items 5 and 9):
ACTIONS_RUN_SUMMARY.txt; BA1_DATA_BIN_RESOURCE_INVENTORY.tsv; BA1_DATA_SCAN_SUMMARY.txt; BA1_RESOURCE_CANDIDATES.tsv; BA1_TILE_TABLE_CANDIDATES.tsv; BA1_TILE_TABLE_RECORDS.tsv; BA1_TILE_TABLE_SCAN_SUMMARY.txt; BB2_FULL_DATABIN_TEXT_SCAN.txt; aq1-deep-context.tsv; aq1-economy-census.tsv; aq1-recount.txt; aw1-helper-call-windows.tsv; aw1-manager-b38-accesses.tsv; aw1-manager-b40-accesses.tsv; aw1-manager-b44-accesses.tsv; aw1-manager-function-detail.txt; aw1-manager-status.txt; aw1-tile-field-function-inventory.tsv; aw2-numeric-instruction-literals.tsv; aw2-numeric-occurrences.tsv; aw2-static-data-scan.md; ay1-ay2-entry1.tsv; ay1-ay2-exe.tsv; ay1-ay2-sha256.txt; ay2-exe-random-byte-check.txt; az3-main-exe-economic-helper-detail.txt; az3-resource-economy-function-detail.txt; az3-setter-call-windows-entry1.tsv; az3-setter-call-windows-main-exe.tsv; az3-setter-caller-main-exe-detail.txt; az3-setter-direct-callers-entry1.txt; az3-setter-direct-callers-main-exe.txt; az3-starting-balance-global-detail.txt; ba1-mode-state-resource-selector.tsv; ba1-resource-parser-main-exe.txt; ba1-selector-callers-main-exe.txt; ba1-selector-dat80070cd0-xrefs.csv; ba1-selector-main-exe-functions.csv; ba1-tile-loader-callers.txt; ba1-tile-resource-loader.txt; bb2-action-byte-access.tsv; bb2-d15a8-direct-callers.txt; bb2-d15a8-focused.txt; bb2-d15a8-function-detail.txt; bb2-entry1-numeric-literals.tsv; bb2-event-direct-callers.txt; bb2-event-function-detail.txt; bb2-event-instruction-windows.txt; bb2-full-databin-text-scan.tsv; bb2-message-object-functions.csv; bb2-message-object-xrefs.csv; bb2-tile-nibble-access.tsv; entry1-buffer-base-targets.txt; entry1-helper-function-detail.txt; helper-a1-provenance-status.txt; input-identity.txt; run-summary.txt

Relative filenames for 38-file bot commit 7c0f0bf9236efc2ae39977d82218884d014313fb (prefix each name with reports/stage1_economy/aq1-run-41730277650/attempt-1/):
ACTIONS_RUN_SUMMARY.txt; BA1_DATA_BIN_RESOURCE_INVENTORY.tsv; BA1_DATA_SCAN_SUMMARY.txt; BA1_RESOURCE_CANDIDATES.tsv; BA1_TILE_TABLE_CANDIDATES.tsv; BA1_TILE_TABLE_RECORDS.tsv; BA1_TILE_TABLE_SCAN_SUMMARY.txt; BB2_FULL_DATABIN_TEXT_SCAN.txt; aq1-recount.txt; aw1-helper-call-windows.tsv; aw1-manager-b38-accesses.tsv; aw1-manager-b40-accesses.tsv; aw1-manager-b44-accesses.tsv; aw1-manager-function-detail.txt; aw2-numeric-instruction-literals.tsv; ay1-ay2-entry1.tsv; ay1-ay2-exe.tsv; az3-resource-economy-function-detail.txt; az3-setter-call-windows-entry1.tsv; az3-setter-direct-callers-entry1.txt; ba1-tile-loader-callers.txt; ba1-tile-resource-loader.txt; bb2-action-byte-access.tsv; bb2-d15a8-direct-callers.txt; bb2-d15a8-focused.txt; bb2-d15a8-function-detail.txt; bb2-entry1-numeric-literals.tsv; bb2-event-direct-callers.txt; bb2-event-function-detail.txt; bb2-event-instruction-windows.txt; bb2-full-databin-text-scan.tsv; bb2-message-object-functions.csv; bb2-message-object-xrefs.csv; bb2-tile-nibble-access.tsv; cd1-raw-indirect-call-candidates.txt; entry1-buffer-base-targets.txt; entry1-helper-function-detail.txt; input-identity.txt; run-summary.txt
