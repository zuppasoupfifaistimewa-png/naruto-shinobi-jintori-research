# DO0–DO3 — audit statis terarah Naruto Jintori
Tanggal pemeriksaan: 5 November 2026
Repositori: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`
Baseline inklusif yang diminta: `a2416ef822266f4f566d6f745d6136a2345fe9ce`
HEAD saat mulai audit: `a2416ef822266f4f566d6f745d6136a2345fe9ce`

## Ringkasan keputusan

| Butir | Status | Tingkat | Putusan |
|---|---|---|---|
| DO0 — commit ledger | TUNTAS pada snapshot awal | K4 | Baseline sudah sama dengan HEAD; rentang inklusif pada saat mulai audit tepat 1 commit: 1 manusia, 0 bot. Commit publikasi laporan ini adalah commit anak baru dan dihitung terpisah pada laporan chat setelah metadata commit diverifikasi. |
| DO1 — 55 value-origin | TUNTAS untuk alasan per PC dan koreksi tabel | K4 | 272 writer PC; 55 source value tidak terdefinisi dalam 12 instruksi lokal. Setiap PC diberi alasan spesifik dalam TSV tambahan; seluruh 55 store bukan tujuan record tile EA84 stride 0x124. |
| DO1 — total X/LV | TUNTAS | K4 | Recount 415 record, 12 resource, 14 X; LV2 formula 415/415; header kolom diperbaiki dan summary kontradiktif direkonsiliasi. |
| DO2 — 22 tile × 12 resource | TUNTAS untuk pencocokan lima nilai | K4 | Keempat snapshot identik; resource 0x276 cocok 22/22, tetapi hanya satu dari 12 resource yang benar-benar dipilih oleh selector H6. |
| DO2 — arti mode/state | TUNTAS untuk peran kode; BELUM untuk identitas Stage 1 | K4 / K0 | mode u32 0x80070734 dan state u8 0x8007073C memang indeks matriks selector. Pasangan mode/state Story Mode Stage 1 Naruto vs Mizuki tetap TIDAK TAHU. |
| DO3 — debit action 8 | TUNTAS untuk transaksi satu langkah | K4 | Action byte 8 adalah jalur upgrade Barrier; debit = u16(tile+0x1A), ditulis sebagai pending -fee; level dinaikkan satu langkah. |
| DO3 — biaya lompat d>=2 | SEBAGIAN | K3 | Tidak ada pengali d di blok debit action 3/8 yang sudah dipetakan, tetapi tidak ditemukan UI/handler tervalidasi untuk target level d>=2. Rumus lintas seluruh kemungkinan jalur tetap TIDAK TAHU. |

## DO0 — jumlah commit inklusif

Compare API pada awal audit menyatakan `status=identical`, `ahead_by=0`, `behind_by=0`, `total_commits=0` antara baseline dan `main`. Karena baseline ikut dihitung, snapshot awal memuat **1 commit total, 1 manusia, 0 bot**. Metadata commit `a2416ef822266f4f566d6f745d6136a2345fe9ce` menunjukkan author dan committer `zuppasoupfifaistimewa-png`; parent-nya `087e0e9a91d50c824352fa0ab0d823a7cf471858`. Tidak ada commit bot di rentang satu-commit tersebut.

Audit ini dipublikasikan sebagai satu commit anak. Metadata author commit publikasi diverifikasi setelah commit dibuat; laporan chat menyajikan hitungan akhir yang mencakup commit publikasi tersebut, sebab commit tidak dapat menulis SHA dirinya sendiri ke dalam konten yang dibuat pada saat bersamaan.

## DO1 — 55 register sumber TIDAK_TAHU

Input: `DN1_WRITER_DESTINATION_AUDIT_2026-11-05.tsv`. Hitung ulang dilakukan langsung dari baris TSV, bukan dari teks summary.

**Recount 272 baris writer:**
- `value_origin=TIDAK_TAHU`: 55
- `DEF_LOKAL_ARITMETIK_ATAU_IMMEDIATE`: 110
- `KONSTANTA_NOL`: 20
- `DEF_LOKAL_LAIN`: 28
- `LOAD_MEMORI_LOKAL`: 58
- `SALIN_REG_LOKAL`: 1
- total = 272.

Tujuan store dari seluruh 272 PC:
- stack direct: 245
- stack computed: 5
- auxiliary buffer EA74 stride 0x90: 22
- tile array EA84 stride 0x124: 0.

Khusus 55 source register TIDAK_TAHU:
- destination auxiliary EA74 stride 0x90: 17
- stack computed: 3
- stack direct: 35.
Tidak satu pun dari 55 baris menulis langsung ke record tile EA84 stride 0x124. Ini kesimpulan tujuan store, bukan klaim bahwa seluruh 272 candidate census adalah census universal dari seluruh bentuk pointer tidak langsung.

**Alasan sumber per PC** tersedia di `DN1_VALUE_ORIGIN_UNKNOWN_REASONS_2026-11-05.tsv`. File tersebut mempertahankan instruksi store, source register, 12 instruksi sebelumnya beserta store, tujuan, klasifikasi register, JAL terdekat bila ada, dan alasan mengapa definisi nilai belum dapat dibuktikan:
- nilai $v0 yang mengikuti helper JAL: return-value candidate; helper call diketahui, tetapi nilai/semantik return tidak dibuktikan hanya oleh jendela lokal;
- $s0–$s7: nilai callee-saved/live-state atau register yang diteruskan, tanpa reaching-definition dalam jendela;
- $ra: return address yang disimpan di stack frame;
- $a2/$a3: argument register yang diteruskan ke outgoing stack slot, tetapi asal callsite tidak ada di jendela;
- $t4: temporary caller-saved tanpa definisi lokal, sehingga tidak boleh diasumsikan sebagai argumen;
- PC 0x800F13B8: kontrol alir bercabang setelah call 0x80018508; return-value candidate tidak dapat dipastikan tanpa analisis predecessor/CFG.
Caller-chain yang tidak tersedia ditandai secara eksplisit; tidak ada asal nilai yang direka.

**Koreksi kontradiksi census:** sebelumnya baris `VALUE_ORIGIN_TIDAK_TAHU_WITHIN_LOCAL_WINDOW=0` berlawanan dengan 55 baris TIDAK_TAHU di TSV. Summary telah dikoreksi menjadi 55 unknown, 217 kategori lain terisi, total 272. Nilai nol lama tidak konsisten dengan data primer dan tidak dipertahankan.

**Koreksi header X/LV:** header lama meletakkan `LV2_formula` sebelum LV3–LV5, padahal isi baris sudah berurutan LV1, LV2, LV3, LV4, LV5, formula, match. Header baru disusun sesuai urutan nilai aktual; baris data tidak diubah.

Recount DK1 dari 415 record mentah:
- 12 resource; 14 X unik: 0, 60, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320.
- X=0 sebanyak 167 record; X nonzero sebanyak 248.
- Untuk setiap grup X, setiap field LV1–LV5 memiliki satu nilai unik di semua record yang terkumpul.
- LV2 = `10 × ceil(11X/100)` cocok 415/415.
- Rumus universal LV1: TIDAK TAHU (X/2 hanya cocok 200/248 record nonzero).
- Formula universal LV3–LV5: TIDAK TAHU; hipotesis numerik yang diuji tidak menghasilkan dukungan universal (H1 15/39; H2 1/39). Nilai tersebut adalah resource lookup/copy, bukan bukti bahwa kode game menghitungnya dari X.

## DO2 — H6 lima-field cross-resource

Pencocokan tuple penuh membandingkan kelima nilai LV dari setiap 22 tile runtime pada setiap frame terhadap tiap record di masing-masing 12 resource. Syarat match adalah lima field LV1–LV5 bersamaan, bukan satu nilai atau lima kecocokan yang berasal dari record yang berbeda.

Hasil per resource pada setiap snapshot (4 snapshot, 22 tile per snapshot; sama pada keempatnya):

| Resource ID | Entry | Record di resource | Tile H6 match 5/5 |
|---|---:|---:|---:|
| 0x276 | 630 | 22 | 22/22 |
| 0x277 | 631 | 33 | 19/22 |
| 0x278 | 632 | 33 | 18/22 |
| 0x279 | 633 | 34 | 21/22 |
| 0x27A | 634 | 33 | 22/22 |
| 0x27B | 635 | 43 | 21/22 |
| 0x27C | 636 | 38 | 20/22 |
| 0x27E | 638 | 22 | 16/22 |
| 0x27F | 639 | 38 | 20/22 |
| 0x285 | 645 | 43 | 21/22 |
| 0x286 | 646 | 36 | 5/22 |
| 0x287 | 647 | 40 | 5/22 |

Per-resource, per-snapshot hit count, non-match indices, selector live, serta jumlah scalar 5-field disimpan dalam `DO2_H6_ALL12_5FIELD_MATCH_2026-11-05.tsv`. Resource 0x27A juga mempunyai 22/22 tuple yang cocok, tetapi H6 tidak memilihnya. Live selector H6 = 0, sehingga resource terpilih adalah 0x276 / entry 630.

### Arti mode dan state

Rantai kode statis pada `FUN_80012EAC`:
1. Baca `mode = u32[0x80070734]` dan `state = u8[0x8007073C]`.
2. Bentuk indeks matriks konfigurasi `33×mode + 3×state`.
3. Ambil config index dari tabel `0x80058758 + 4×(33×mode + 3×state)`.
4. Ambil byte selector dari `0x80057798 + config_index×0x54`.
5. Tulis selector ke `u8[0x80070CD0]`.
6. Jalur resource memakai `resource_id = 0x276 + selector`.

Matriks memiliki 2.816 baris PASS/nonblank, hasil distribusi selector:
- selector 0: 2.723 baris → resource 0x276 / entry 630
- 1: 11 → 0x277 / 631
- 2: 13 → 0x278 / 632
- 3: 10 → 0x279 / 633
- 4: 17 → 0x27A / 634
- 5: 2 → 0x27B / 635
- 6: 4 → 0x27C / 636
- 8: 1 → 0x27E / 638
- 9: 4 → 0x27F / 639
- 15: 7 → 0x285 / 645
- 16: 14 → 0x286 / 646
- 17: 10 → 0x287 / 647.

Dua hipotesis selector yang dapat diuji:
- **H1 — mode/state matrix adalah pemilih selector utama.** Prediksi: pasangan mode/state memilih config index, byte selector, lalu resource 0x276+selector. Falsifier: ada satu row PASS yang byte selector tidak sama dengan selector yang dibaca loader atau resource ID tidak memenuhi 0x276+selector.
- **H2 — konfigurasi alternatif via FUN_80012780.** Fungsi ini menulis global selector yang sama dari byte-0 row `0x80064918 + ((param1 & 0xFF)×0x30)`. Prediksi: ada caller yang memasok param1 sehingga row alternatif mengisi selector sebelum resource load. Falsifier: callsite lengkap membuktikan fungsi ini tidak dipanggil pada alur resource atau param1 tidak mempengaruhi selector pada jalur tersebut. Direct caller yang mengikat param1 ke mode/state belum ditemukan; jadi H2 belum dipilih sebagai jalur utama.

H6 dua restore yang telah tercatat memuat mode=0, state=0, selector=0 dan resource 0x276 pada empat snapshot. Ini adalah fixture H6 hibrida dan tidak identik dengan bukti Story Mode Stage 1 Naruto vs Mizuki. Pemetaan label Stage 1 → pasangan mode/state tetap **TIDAK TAHU (K0)**. Frekuensi terbesar selector 0 tidak cukup untuk menetapkan Stage 1.

**Run yang digunakan (sudah ada di repo; tidak dijalankan ulang):** status SUCCESS, workflow `ba3-h6-tile-resource-runtime`, job `ba3-h6-economy-runtime`, run 41419506538, job ID 125191389694, source SHA `7413d48a7eec7be9d97782a5d8b02400b4b83a57`, exit code 0, dua independent H6 restores. Ringkasan teks yang tersimpan: `DN2_H6_ACTIONS_RUN_SUMMARY_2026-11-05.txt`.

## DO3 — debit upgrade dan kemungkinan lompatan d>=2

### Bukti action byte 8 → upgrade Barrier

- `FUN_800F3658` memanggil `FUN_800EB434` pada PC 0x800F5CF8.
- `FUN_800EB434` memilih kandidat tile bertipe 5 yang owner-nya pemain aktif, dan hanya jika level nibble bits 8–11 masih di bawah 4.
- PC 0x800EC3A4 memuat kode 8 (`li v0,8`); PC 0x800EC3A8 menulis byte 8 ke manager `+0x2EB`.
- Dispatcher `FUN_800D15A8` membaca action byte itu pada PC 0x800D4470 dan masuk blok transaksi 3/8.

### Excerpt MIPS transaksi (setiap excerpt <64 byte)

| PC | Fungsi | Instruksi | Implikasi |
|---|---|---|---|
| 0x800D4628 | FUN_800D15A8 | `lhu a0,0x1a(v0)` | fee dibaca langsung sebagai u16(tile+0x1A) |
| 0x800D4634 | FUN_800D15A8 | `slt v0,v0,a0` | saldo kerja dibandingkan dengan fee |
| 0x800D46EC | FUN_800D15A8 | `lhu v0,0x1a(v0)` | fee dibaca ulang dari tile+0x1A |
| 0x800D46F4 | FUN_800D15A8 | `subu v0,zero,v0` | bentuk delta negatif -fee; tidak ada multiply/shift atas d |
| 0x800D46F8 | FUN_800D15A8 | `sh v0,0x2ee(a0)` | simpan pending debit signed -fee |
| 0x800D46AC | FUN_800D15A8 | `srl v0,v0,0x8` | ekstrak level nibble |
| 0x800D46B0 | FUN_800D15A8 | `andi v0,v0,0xf` | level saat ini |
| 0x800D46B4 | FUN_800D15A8 | `addiu v0,v0,0x1` | naik satu level, bukan target d |
| 0x800D4764 | FUN_800D15A8 | `sh v0,0x20(v1)` | tulis level nibble hasil +1 kembali ke tile |

Pada blok debit yang teridentifikasi, operand biaya hanya `u16(tile+0x1A)`. Tidak ada `mult`, shift fee, loop pengulangan debit, atau table lookup dengan kunci d sebelum penulisan pending. Jalur action 8 hanya menerima tile dengan level masih di bawah maksimum dan menaikkan nibble satu kali. Dengan demikian:

- **Terbukti K4 untuk satu langkah action 8:** debit = `u16(tile+0x1A)`; pending = `-fee`; level menjadi `level+1`.
- **Tidak terbukti untuk d>=2:** belum ada UI/handler target-level yang mengirim nilai d ke blok transaksi atau jalur lain yang dapat ditetapkan sebagai lompat dua/lebih tingkat. Bukti action 8 saat ini justru merupakan operasi satu langkah. Tidak boleh menyimpulkan bahwa semua jalur upgrade game memakai fee flat.

Action byte 3 ditulis pada PC 0x800DAA84–0x800DAA88 oleh `FUN_800D9570`, lalu juga masuk blok transaksi bersama. Identitas gameplay action byte 3 tetap **TIDAK TAHU**; jangan otomatis menyebutnya build Barrier. Ada pula call `FUN_80113E6C(a0=3)` setelah action byte 8 ditulis oleh producer; angka argumen helper ini berbeda domain dengan action byte manager +0x2EB dan tidak boleh dicampuradukkan.

### Hipotesis d>=2 dan falsifier

- **H1 — eksponensial:** `cost(d)=B×2^d`. Prediksi d=2 →4B, d=3 →8B, d=4 →16B. Falsifier: satu trace transaksi target-level d=2/3/4 menunjukkan pending tidak sama dengan nilai tersebut, atau jalur target-level memanggil blok datar tanpa pengali. Tidak ada titik d>=2 tervalidasi di data ini; rumus belum dapat dipilih.
- **H2 — biaya per langkah:** `cost(d)=d×B`, baik sebagai satu debit agregat atau beberapa debit +B. Falsifier: trace d=2 menunjukkan satu pending -B dan tidak ada dua debit/loop per langkah, atau pengukuran transaksi terverifikasi menunjukkan bukan 2B. Belum ada trace pemilih target-level d>=2.
- **H3 — tier/lookup/upstream:** fee untuk target d dipilih dari tabel/atribut tujuan atau telah dihitung upstream sebelum D15A8 membaca +0x1A. Falsifier: census seluruh writer membuktikan tak ada penulis EA84+0x1A relevan dan trace target d memperlihatkan operand selalu langsung B yang konstan tanpa lookup/operand lain. Kandidat writer +0x1A yang sudah disisir tidak membuktikan alias ke tile EA84+0x1A: base yang terurai mengarah ke tabel/struct lain atau loader, dan beberapa base masih tidak teralias.

Kesimpulan DO3: **SEBAGIAN K3 untuk pertanyaan d>=2**, dengan mekanisme transaksi satu langkah action 8 **TUNTAS K4**. Nilai B dapat dibaca dari tile+0x1A pada transaksi; upstream writer yang mengisi fee tile tersebut belum dibuktikan secara menyeluruh. Tidak ada fitting terhadap dua/kurang titik pengamatan pengguna; observasi pengguna tetap hipotesis K1 dan tidak dipakai sebagai formula.

## File yang diubah pada publikasi audit ini

- `reports/stage1_economy/DN1_WHOLE_CENSUS_SUMMARY_2026-11-05.txt` — koreksi unknown source count 0→55.
- `reports/stage1_economy/DN1_DK1_X_LV_TABLE_2026-11-05.tsv` — perbaikan urutan header LV3–LV5 vs formula.
- `reports/stage1_economy/DN1_DK1_X_LV_TABLE_SUMMARY_2026-11-05.txt` — recount/penjelasan tabel setelah validasi ulang.
- `reports/stage1_economy/DN1_VALUE_ORIGIN_UNKNOWN_REASONS_2026-11-05.tsv` — 55 penjelasan sumber register per PC dan 12-instruction context.
- `reports/stage1_economy/DO2_H6_ALL12_5FIELD_MATCH_2026-11-05.tsv` — 48 baris per-resource × snapshot.
- `reports/stage1_economy/DO0_DO3_STATIC_AUDIT_2026-11-05.md` — laporan gabungan DO0–DO3.

Tidak ada perubahan terhadap Release, visibilitas repo, `STATUS.md`, workflow, emulator, atau binary game.
