# BA1–BA3 — laporan akhir audit resource petak Stage 1
Tanggal: 2 November 2026
Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`
Game: Naruto — Shinobi no Sato no Jintori Gassen, SLPS-03553

## Status akhir

| Audit | Status | Kepastian | Yang ditutup |
|---|---|---|---|
| BA1 — tabel resource dan selector | **SELESAI** | K4 untuk matriks statis; K5 untuk selector pada H6 yang diuji | Jalur selector → resource ID → Entry 630, serta 22 record resource. |
| BA2 — layout record dan helper nilai | **SELESAI** | K4 statis + K5 kecocokan sumber/runtime pada H6 | 18 field salinan dan 2 field inisialisasi cocok pada seluruh snapshot; helper nilai direkonstruksi. |
| BA3 — validasi runtime berulang | **SELESAI** | K5 untuk snapshot read-only H6 | Dua restore independen, dua frame per restore, hash RAM sama per frame, seluruh field cocok. |

**Kesimpulan ruang lingkup:** BA1, BA2, dan BA3 sudah selesai untuk identifikasi tabel, pemetaan data, serta pengulangan snapshot H6. Ini bukan bukti bahwa checkpoint H6 adalah Story Mode murni, bukan validasi transaksi gameplay, dan bukan bukti bahwa seluruh mode/board memakai resource yang sama.

## BA1 — tabel Stage 1 dan jalur selector

Loader `FUN_800B2A58` memanggil `FUN_800F7ADC` dengan resource ID:

`resource_id = 0x276 + u8[0x80070CD0]`

`FUN_800129E4` membaca global `0x80070CD0`. Dua writer statis ditemukan:

1. `FUN_80012EAC` mengambil byte pertama dari row matriks mode/state pada `0x80058758`, lalu menulisnya ke `0x80070CD0`.
2. `FUN_80012780(param_1)` mengambil byte pertama dari row `0x80064918 + (param_1 & 0xFF) × 0x30`, lalu menulisnya ke `0x80070CD0`. Pemanggil langsung fungsi kedua belum ditemukan: **TIDAK TAHU**.

### Matriks mode/state

Ekspor statis berisi 2.816 kombinasi (256 nilai mode × 11 nilai state), semuanya terbaca dan seluruh 2.816 baris berstatus PASS; tidak ada baris unmapped. Berkas:

`reports/stage1_economy/aq1-run-41419756918/attempt-1/ba1-mode-state-resource-selector.tsv`

Distribusi byte selector:

| Selector | Resource ID | Jumlah kombinasi |
|---:|---:|---:|
| 0 | 630 (0x276) | 2.723 |
| 1 | 631 (0x277) | 11 |
| 2 | 632 (0x278) | 13 |
| 3 | 633 (0x279) | 10 |
| 4 | 634 (0x27A) | 17 |
| 5 | 635 (0x27B) | 2 |
| 6 | 636 (0x27C) | 4 |
| 8 | 638 (0x27E) | 1 |
| 9 | 639 (0x27F) | 4 |
| 15 | 645 (0x285) | 7 |
| 16 | 646 (0x286) | 14 |
| 17 | 647 (0x287) | 10 |
| **Total** | | **2.816** |

Pada empat snapshot H6, runtime mode `0x80070734=0` dan state `0x8007073C=0`. Lookup matriks menghasilkan index 0, selector 0, sehingga resource ID yang dipakai loader adalah **630 (0x276)**. Ini terkonfirmasi empat kali (dua frame × dua restore), dan bukan ID universal untuk semua mode/state.

Entry 630:
- LBN 9360
- Ukuran 661 byte
- Offset berkas `0x11DE000`
- SHA-256 `12c1a6ff1870f5c6fe33723beef14d93009b509d70caa882c5c6e8de8535e0c8`
- Header count 22; panjang tepat `1 + 22 × 0x1E = 661` byte.

Entry 638 memiliki ukuran/bentuk yang mirip, tetapi pembandingan terdahulu terhadap tile+0x10 memberi Entry 630 cocok 88/88, sedangkan Entry 638 hanya 24/88. Snapshot H6 juga memilih Entry 630, bukan Entry 638.

**Catatan Actions BA1:** run 41419756918 menghasilkan matriks TSV di atas dengan 2.816/2.816 baris PASS dan skrip analisis exit 0. Namun kesimpulan workflow keseluruhan adalah FAILURE karena langkah validasi artefak menolak dua keluaran teks berekstensi `.csv` (validator hanya mengizinkan `.txt/.log/.tsv/.md`). Kegagalan validasi ekstensi tersebut bukan kegagalan matriks TSV. Ringkasan run telah dikoreksi agar status workflow tidak keliru disebut sukses; allowlist validator juga diperbaiki untuk menerima `.csv` pada run berikutnya. Status run lama tetap FAILURE.

## BA2 — layout sumber ke runtime dan helper nilai

Resource source terdiri dari satu byte count diikuti record ber-stride `0x1E`. Runtime tile array memakai stride `0x124`.

Pemetaan loader yang terkonfirmasi:
- 7 field byte dan 11 field halfword disalin: **1.584/1.584** pemeriksaan cocok (22 record × 18 field × 4 snapshot).
- Dua field hasil inisialisasi loader: tile+0x06 = 0 dan tile+0x20 = 0xF020; **176/176** cocok (22 record × 2 field × 4 snapshot).
- Total **1.760/1.760** pemeriksaan cocok; mismatch 0.
- Source record +0x05 dilewati; source +0x06 masuk ke runtime tile+0x05.
- Source +0x13..+0x14 disalin sebagai halfword little-endian ke runtime tile+0x1A. Source +0x15..+0x16 ke tile+0x1C; source +0x17..+0x18 ke tile+0x1E.

Pemetaan lengkap ada di `BA2_TILE_RUNTIME_FIELD_MAP.tsv`; pencocokan mentah ada di `BA3_TILE_FIELD_VALIDATION.tsv`.

### Helper `FUN_800B770C`

Untuk tile record `R = [0x8013EA84] + index × 0x124`:

`H = u16(R + 0x10 + ((u16(R + 0x20) >> 7) & 0x1E))`

Byte selector R+0x0B memilih faktor hasil:
- 0 → H
- 1 → floor(12H/10)
- 2 → floor(15H/10)
- 3 → floor(18H/10)
- 4 → 2H
- nilai lain pada dispatch ini → 0.

Dalam snapshot H6, selector seluruh 22 tile adalah 0 dan word tile+0x20 adalah 0xF020, sehingga offset yang terpilih adalah +0x10 dan hasil helper sama dengan u16(tile+0x10). Jumlah nilai helper untuk 22 record pada snapshot adalah 1.270. Ini hanya keluaran helper; tidak boleh otomatis disebut harga, pendapatan, nilai wilayah, atau nilai Barrier.

### Hubungan tile+0x1C dan tile+0x1E

Kedua field adalah nilai terpisah. Pada 22 record Entry 630, hasil perbandingan persisnya:

| Record | tile+0x1C | tile+0x1E |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 35 | 42 |
| 2 | 35 | 70 |
| 3 | 35 | 70 |
| 4 | 70 | 84 |
| 5 | 0 | 0 |
| 6 | 70 | 84 |
| 7 | 84 | 112 |
| 8 | 70 | 98 |
| 9 | 70 | 98 |
| 10 | 70 | 84 |
| 11 | 0 | 0 |
| 12 | 105 | 140 |
| 13 | 105 | 154 |
| 14 | 140 | 182 |
| 15 | 105 | 154 |
| 16 | 105 | 140 |
| 17 | 0 | 0 |
| 18 | 0 | 0 |
| 19 | 70 | 98 |
| 20 | 70 | 84 |
| 21 | 35 | 70 |

Jadi pada **tabel Entry 630 ini** tile+0x1E lebih besar pada 17 record nonnol; 5 record sisanya nol pada keduanya. Itu pola data resource 630, bukan aturan universal seluruh resource/game.

Decompilation `FUN_800D15A8` juga memperlihatkan cabang delta positif menggunakan:

`delta = u16(tile+0x1E) + level × u16(tile+0x1C)`

dengan level diambil dari nibble bits 8–11 pada tile+0x20. Rumus instruksinya terlihat; nama gameplay yang tepat (pendapatan/hadiah/settlement atau yang lain) tetap **TIDAK TAHU**.

### Jalur biaya petak yang terkonfirmasi

Pada `FUN_800D15A8`, untuk action byte 3 atau 8:
1. `FUN_800BBD9C()` memilih index tile.
2. Fee dibaca sebagai `u16(tile+0x1A)`.
3. Fee dibandingkan dengan saldo kerja participant +0x04.
4. Bila cukup, pending delta participant pada `+0x2EE` menerima `-fee`.
5. Dua nibble level pada tile+0x20 (bits 8–11 dan 4–7) masing-masing dinaikkan satu.
6. `FUN_800BB004` dan `FUN_800BE464` dipanggil untuk memperbarui tile.

Dengan demikian sumber nominal fee action 3/8 terbukti berasal dari data record resource → runtime tile+0x1A. Identitas nama action 3 versus 8 dan cakupan semua jenis bangun/upgrade masih **TIDAK TAHU**. Tidak ada klaim runtime transaksi pembelian/upgrade dari BA3.

## BA3 — snapshot H6 dua restore independen

Run Actions **41419506538**:
- Job: `ba3-h6-economy-runtime`
- Job ID: `125191389694`
- Source SHA: `7413d48a7eec7be9d97782a5d8b02400b4b83a57`
- Status: PASS; exit code: 0.

Dua restore independen masing-masing mencapai frame 180 dan 360. Pada setiap frame, 22 record tile berhasil diparse. Hash RAM cakupan 2 MiB sama antarpeluncuran untuk frame yang sama:
- Frame 180: `5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7`
- Frame 360: `4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907`

Seluruh 88 record runtime (22 tile × 4 snapshot) cocok dengan source Entry 630 pada field yang dipetakan. Semua 1.760 pemeriksaan (salinan + initializer) PASS. Selector resource 0 dan ID 630 tercatat pada seluruh empat snapshot.

Memory Card SHA-256 sebelum dan sesudah masing-masing restore sama:
`ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.

Tidak ada input gameplay, RAM poke, atau pemanggilan setter. Target checkpoint + CONTROL top-level protobuf field 6 membentuk H6 **HIBRIDA**, bukan checkpoint target murni. Artefak privat sementara dihapus sebelum publikasi teks/TSV.

### Ketidakcocokan yang tidak boleh ditafsirkan

Pada lookup mode/state 0/0, B30 di row tabel terpilih bernilai 400, sedangkan manager B30 runtime bernilai 0 (tidak cocok). Agregat floor(sum V/2) dari helper bernilai 635 sedangkan manager B38 bernilai 0 (tidak cocok); filter status 5 juga berisi 0 record. Karena itu BA3 **tidak** membuktikan bahwa B30 adalah target agregat, B38 adalah nilai Barrier, atau helper V adalah saldo/pendapatan. Makna field manager tersebut tetap TIDAK TAHU.

## Batas akhir

- H6 bukan bukti Story Mode murni atau label Stage 1 gameplay secara independen.
- Belum diuji transaksi build/upgrade dengan input gameplay; BA3 hanya snapshot read-only.
- Nama gameplay action byte 3/8 belum diketahui; coverage seluruh jenis action belum lengkap.
- Makna gameplay tile+0x1C, tile+0x1E, helper V, B30/B38/B40/B44, dan event pemicu transfer tidak dinaikkan menjadi klaim.
- Base impor statis Entry 1 `0x800AD450` tetap kandidat; BA ini membuktikan kecocokan data record sumber ke runtime pada H6, bukan pemetaan universal seluruh modul.
- Resource 630 dipastikan untuk selector mode/state H6 0/0. Matriks menunjukkan selector lain pada kombinasi mode/state berbeda.

**Putusan:** BA1 = SELESAI; BA2 = SELESAI; BA3 = SELESAI untuk ruang lingkup yang didefinisikan di atas. Tidak ada klaim K5 untuk transaksi ekonomi atau semua mode/gameplay.
