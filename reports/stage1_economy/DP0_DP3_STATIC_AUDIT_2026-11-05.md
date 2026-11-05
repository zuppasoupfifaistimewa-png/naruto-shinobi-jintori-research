# DP0–DP3 — audit statis pending debit, event 3, dan nilai +0x1A

Tanggal: 5 November 2026  
Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`  
Baseline ledger inklusif: `d6bf7d1723f2b1bb22041eb94d2526254840c185`  
HEAD `main` pada pembekuan sebelum publikasi: `d6bf7d1723f2b1bb22041eb94d2526254840c185`  
Metode: berkas TSV dan export instruksi statis yang sudah tersimpan. Tidak ada emulator, workflow, BIOS, ISO, savestate, dump, video, atau frame baru.

## Ringkasan

| Butir | Status | K | Hasil |
|---|---|---:|---|
| DP0 ledger pada HEAD beku | TUNTAS | K4 | 1 commit inklusif: 1 manusia, 0 bot. Commit hasil audit ini dipublikasikan sesudah snapshot; hitungan post-publication dilaporkan terpisah di chat. |
| DP1 manager +0x2EE dan action +0x2EB | SEBAGIAN | K3 | TSV 70 PC: 5 store +0x2EE (4 CLEAR, 1 DEBIT_LANGSUNG) dan 65 store +0x2EB (2 CLEAR, 63 LAIN). Enam dari 65 action-store hanya displacement global, alias manager belum terbukti. Satu PC debit hanya memiliki 8 instruksi pra-store di export yang tersimpan. |
| DP2 FUN_800D9570 / event 3 | SEBAGIAN | K3 | Pemanggil langsung diketahui di PC 0x800F5E1C, tetapi batas fungsi pemanggil UNMAPPED. Event return 3 memilih tile lewat slot aktif dan menulis owner; tidak menulis fee +0x1A atau pending +0x2EE, dan mask +0x20 mempertahankan level nibble. Jalur lompat d>=2 TIDAK TAHU. |
| DP3 X → u16 tile+0x1A | TUNTAS | K4 | 415 record dihitung ulang dari DK1 TSV: 14 X unik, 0 X dengan lebih dari satu nilai +0x1A. Semua 7 titik pengamatan nonzero yang disebut pengguna cocok. |

## DP0 — ledger commit

Pada pembekuan sebelum publikasi hasil ini, `main` tepat di baseline. Karena baseline inklusif, rentangnya memuat **1 commit, 1 MANUSIA, 0 BOT**.

| SHA penuh | Tipe author | Pesan | Berkas yang berubah |
|---|---|---|---|
| d6bf7d1723f2b1bb22041eb94d2526254840c185 | MANUSIA: zuppasoupfifaistimewa-png | Complete DO0-DO3 static economy audit and reconcile DN1 | reports/stage1_economy/DN1_DK1_X_LV_TABLE_2026-11-05.tsv; reports/stage1_economy/DN1_DK1_X_LV_TABLE_SUMMARY_2026-11-05.txt; reports/stage1_economy/DN1_VALUE_ORIGIN_UNKNOWN_REASONS_2026-11-05.tsv; reports/stage1_economy/DN1_WHOLE_CENSUS_SUMMARY_2026-11-05.txt; reports/stage1_economy/DO0_DO3_STATIC_AUDIT_2026-11-05.md; reports/stage1_economy/DO2_H6_ALL12_5FIELD_MATCH_2026-11-05.tsv |

Commit publikasi berkas DP1–DP3 dan koreksi jendela konteks adalah commit anak sesudah snapshot beku ini. Metadata dan jumlah ledger setelah publikasi disajikan di laporan chat agar SHA commit anak tidak ditebak.

## DP1 — census penulis manager +0x2EE dan action +0x2EB

Sumber primer: `bb2-action-byte-access.tsv`, `aw1-manager-function-detail.txt`, `cg2-tile-fee-writer-function-detail.txt`, dan `bb2-d15a8-focused.txt`. File hasil berisi satu baris per PC, label, fungsi, status alias base, instruksi store, konteks pra-store, dan excerpt byte little-endian.

### Recount dari TSV hasil

| Label | PC | Arti |
|---|---:|---|
| DEBIT_LANGSUNG | 1 | Store signed pending debit `-u16` ke manager +0x2EE. |
| COMPUTED | 0 | Tidak ada store +0x2EE yang terbukti menyimpan nilai fee hasil multiply/shift ke field itu. |
| CLEAR | 6 | Empat reset +0x2EE dan dua reset byte action +0x2EB. |
| LAIN | 63 | Store action +0x2EB lain; bukan store debit +0x2EE. |
| **Total** | **70** | **5 +0x2EE dan 65 +0x2EB.** |

Rincian +0x2EE (manager pointer/base terkonfirmasi dalam export):

| PC | Fungsi | Label | Excerpt |
|---|---|---|---|
| 0x800B2EEC | FUN_800b2a58 | CLEAR | `sh zero,0x2ee(v0)` |
| 0x800B36BC | FUN_800b2a58 | CLEAR | `sh zero,0x2ee(v0)` |
| 0x800D1738 | FUN_800d15a8 | CLEAR | `sh zero,0x2ee(v0)` |
| 0x800D1764 | FUN_800d15a8 | CLEAR | `sh zero,0x2ee(v0)` |
| 0x800ECBB8 | FUN_800ec574 | DEBIT_LANGSUNG | `sh v0,0x2ee(v1)`; nilai dibentuk dari `lhu -0x6104` lalu `subu zero,value`. |

Untuk +0x2EB, census writer export memiliki 65 PC: 59 berstatus `PARTICIPANT_GLOBAL_XREF_OR_HANDLER` dan 6 hanya `GLOBAL_DISPLACEMENT_ONLY`. Dua store adalah `sb zero,0x2eb`; 63 store lain dilabeli LAIN. Enam displacement-only tetap kandidat, tidak diklaim sebagai alias manager pasti.

**Catatan pengali/shift/loop atas fee:** pada `FUN_800ec574`, PC 0x800ECAA0 menjalankan `mult a0,v0` terhadap nilai yang baru dibaca dari global `-0x6104`; `mflo` di 0x800ECAA4 dan store 0x800ECAA8 menaruh hasil ke `manager+0x4F0`. Store pending di 0x800ECBB8 kemudian membaca ulang `u16 -0x6104`, menegasikannya, dan menulis ke +0x2EE. Karena tujuan hasil multiply adalah +0x4F0 dan hubungan semantiknya dengan pending debit tidak dibuktikan, ini ditandai **KANDIDAT PENGALI SUMBER YANG SAMA**, bukan formula biaya d>=2. Shift `sll v0,0x1` sebelum load halfword di 0x800ECB9C adalah pembentukan indeks alamat; bukan bukti mengalikan nilai fee. Tidak ada loop yang terbukti mengulang debit fee pada writer +0x2EE ini.

Batas census: seluruh 65 writer +0x2EB tersedia dari pemindaian 149 fungsi; 6 alias base masih tidak terurai. Untuk +0x2EE, 5 store ditemukan di export manager/function yang tersimpan, tetapi tidak tersedia export raw memory-operand all-function khusus displacement +0x2EE. Karena itu cakupan universal +0x2EE tetap SEBAGIAN. PC 0x800ECBB8 hanya menyimpan 8 instruksi pra-store yang berurutan dalam export yang tersedia. Empat instruksi pra-store lebih awal (PC 0x800ECB88–0x800ECB94) TIDAK TERSEDIA; instruksi dari fragmen xref lain tidak digabung sebagai konteks palsu.

## DP2 — FUN_800D9570, event return 3, dan PC 0x800DAA84–88

Direct caller yang terpetakan oleh export:
- PC 0x800F5E1C: `jal 0x800D9570` (word `0x0C03655C`).
- Batas/nama fungsi pemanggil pada Ghidra: **UNMAPPED**. Maka fungsi pemanggil = TIDAK TAHU; hanya callsite langsung yang terbukti.

Penting membedakan dua angka “3”:
1. **Event return 3** adalah cabang `FUN_80102408()` hasil 3; dispatch dari 0x800D95D0 menuju 0x800D9C8C.
2. **Action byte 3** di PC 0x800DAA84–0x800DAA88 adalah `li v0,3` lalu `sb v0,0x2eb(v1)`. Ini berada pada tail lain setelah pengecekan `manager+0x360` dan perbandingan action saat ini terhadap 2. Jadi PC itu bukan entry cabang `event return 3`.

Pada cabang event return 3, tile dipilih dari indeks byte `manager + active_slot*0x90 + 0x1F`; pointer tile dihitung sebagai `tile_base + tile_index*0x124` (tile base global `DAT_8013EA84`). Slot aktif berasal dari `DAT_8013EA88`. Jalur ini:
- mengurangi field player-record +0x08 dengan nilai return helper `0x800160D4(3)` (nilai helper/arti gameplay-nya TIDAK TAHU);
- menulis tile+0x20 pada PC 0x800D9D60 dengan pola `lhu; andi 0xFFF0; sh`, yang menghapus nibble rendah tetapi mempertahankan bit 8–11 (level nibble);
- menulis owner byte tile+0x0D pada PC 0x800D9DEC;
- menyalin state manager +0x2E9 ke action byte +0x2EB pada PC 0x800D9E30.

Di seluruh body FUN_800D9570, sembilan store `sh ...,0x20(...)` mengikuti mask `0xFFF0` pada PC: 0x800D9734, 0x800D9908, 0x800D9B38, 0x800D9D60, 0x800D9FAC, 0x800DA18C, 0x800DA368, 0x800DA58C, 0x800DA7B4. Tidak ada akses store/load `tile+0x1A` dalam body yang diekspor, dan tidak ada store `manager+0x2EE`. Khusus action byte literal 3 pada PC 0x800DAA84–88, basic block itu hanya menulis +0x2EB; tidak memilih tile melalui field +0x1F dan tidak menulis tile+0x1A, tile+0x20, atau manager+0x2EE.

**Jalur biaya lompat target-level d>=2: TIDAK TAHU.** Kandidat paling dekat adalah:
- `FUN_800ec574`, PC 0x800ECAA0: `mult a0,v0`; excerpt 20 byte untuk rangkaian `lw; mult; mflo; sw manager+0x4F0`.
- `FUN_800ec574`, PC 0x800ECBB8: `sh v0,0x2ee(v1)`; debit pending adalah negatif dari u16 yang dibaca pada 0x800ECBA8.
Keduanya belum membuktikan bahwa target d dikirim, dikalikan, atau bahwa nilai multiply masuk ke pending +0x2EE. Tidak ada operand target-level d atau store tile+0x1A/+0x20 level nibble pada jalur PC 0x800DAA84–88.

Hipotesis pembeda:
- H1: target d>=2 diproses upstream melalui nilai global `-0x6104` dan kandidat multiply 0x800ECAA0. Prediksi: data-flow/call-chain mengikat nilai pengali ke d dan hasilnya sampai ke debit. Falsifier: hasil multiply hanya dipakai untuk manager+0x4F0 dan pending +0x2EE selalu reload langsung dari u16 yang sama tanpa hubungan d. Bukti yang tersedia saat ini mendukung pemisahan tujuan, belum mengikat d.
- H2: event return 3 hanya melakukan perubahan tile/owner satu event; action byte literal 3 adalah marker dispatcher, bukan target level. Falsifier: ditemukan consumer action 3 yang menerima target d dan pada jalurnya menulis level nibble serta pending debit. Consumer seperti itu belum terbukti dari export tersimpan.

## DP3 — tabel X runtime → u16 tile+0x1A

Recount dilakukan langsung dari seluruh 415 baris DK1. Loader memetakan X dari sumber +0x08 ke tile+0x0E dan nilai +0x1A dari sumber +0x14 ke tile+0x1A. Semua X memiliki satu nilai fee unik; X dengan beberapa nilai: **0**.

| X | Record | u16(tile+0x1A) | Uji hipotesis pengguna |
|---:|---:|---:|---|
| 0 | 167 | 0 | X=0 kosong; fee 0 |
| 60 | 23 | 50 | COCOK |
| 100 | 34 | 50 | COCOK |
| 120 | 22 | 100 | COCOK |
| 140 | 26 | 100 | COCOK |
| 160 | 25 | 120 | COCOK |
| 180 | 28 | 120 | tidak ada pengamatan pengguna |
| 200 | 21 | 150 | COCOK |
| 220 | 17 | 150 | COCOK |
| 240 | 9 | 200 | tidak ada pengamatan pengguna |
| 260 | 20 | 200 | tidak ada pengamatan pengguna |
| 280 | 17 | 220 | tidak ada pengamatan pengguna |
| 300 | 4 | 220 | tidak ada pengamatan pengguna |
| 320 | 2 | 250 | tidak ada pengamatan pengguna |

Pemeriksaan titik pengguna: 7/7 cocok (X=60,100,120,140,160,200,220). X=0 memiliki 167 record fee 0 dan diperlakukan sebagai record kosong, bukan sebagai pelanggaran terhadap hipotesis nonzero. Nilai berulang yang teruji dari TSV ini adalah pemetaan data, bukan bukti rumus pembangkit; tidak dilakukan fitting formula dengan titik terbatas.

## Artefak yang ditambahkan

- `reports/stage1_economy/DP1_MANAGER_PENDING_ACTION_WRITER_CENSUS_2026-11-05.tsv`
- `reports/stage1_economy/DP3_X_TO_TILE_FEE_1A_2026-11-05.tsv`
- `reports/stage1_economy/DP0_DP3_STATIC_AUDIT_2026-11-05.md`

Tidak ada perubahan Release, `STATUS.md`, visibilitas repo, atau workflow.
