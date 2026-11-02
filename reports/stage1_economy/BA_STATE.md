# BA_STATE — final checkpoint BA1 → BA2 → BA3
Tanggal: 2 November 2026
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Laporan: `reports/stage1_economy/BA_FINAL_REPORT_2026-11-02.md`

## Status akhir

| Butir | Status | Kepastian | Lingkup yang selesai |
|---|---|---:|---|
| BA1 | SELESAI | K4 statis + K5 selector H6 | Matriks selector 2.816 kombinasi, semua PASS; H6 mode/state 0/0 memilih resource 630; 22 record diekstrak. |
| BA2 | SELESAI | K4 statis + K5 cocok sumber/runtime H6 | 18 field salinan 1.584/1.584; 2 initializer 176/176; total 1.760/1.760; helper FUN_800B770C direkonstruksi. |
| BA3 | SELESAI | K5 snapshot H6 | Dua restore, frame 180/360, RAM hash identik per frame; seluruh 88 record runtime cocok; Memory Card tidak berubah. |

## Bukti primer
- BA1 records: `BA1_STAGE1_RESOURCE_630_RECORDS.tsv`.
- Matriks selector: `aq1-run-41419756918/attempt-1/ba1-mode-state-resource-selector.tsv` (2.816 baris data, 2.816 PASS, unmapped 0).
- BA2 mapping: `BA2_TILE_RUNTIME_FIELD_MAP.tsv`.
- BA3 field validation: `BA3_TILE_FIELD_VALIDATION.tsv`; ringkasan `BA3_TILE_FIELD_MATCH_SUMMARY.txt`.
- BA3 run: `ba3-h6-tile-resource-runtime-run-41419506538/attempt-1/`.

## Actions dan status
- BA1 matrix: run 41419756918, source SHA `ed788883372aefa1772790e4e8a74e7a677ba633`. Workflow conclusion FAILURE di langkah validator ekstensi karena dua file teks berekstensi CSV ditolak. Ekspor matriks TSV sendiri exit 0 dan terverifikasi 2.816/2.816 PASS. Ringkasan Actions telah dikoreksi; allowlist validator kini menerima CSV untuk run berikutnya. Run lama tetap FAILURE.
- BA3: run 41419506538, job `ba3-h6-economy-runtime`, job ID `125191389694`, source SHA `7413d48a7eec7be9d97782a5d8b02400b4b83a57`, PASS, exit 0.

## Formula/kondisi terbukti
- `resource_id = 0x276 + u8[0x80070CD0]`; mode/state H6 0/0 menghasilkan selector 0 dan resource 630.
- Source stride 0x1E; runtime tile stride 0x124.
- `FUN_800B770C`: `H=u16(R+0x10+((u16(R+0x20)>>7)&0x1E))`; byte selector +0x0B memilih faktor 1, 12/10, 15/10, 18/10, atau 2.
- `u16(tile+0x1A)` adalah fee untuk cabang action byte 3/8; jika saldo kerja cukup, pending delta menjadi `-fee`.
- Cabang delta positif terlihat memakai `tile+0x1E + level × tile+0x1C`; label gameplay tetap TIDAK TAHU.

## Batas yang harus dipertahankan
- H6 = target checkpoint + CONTROL field 6; bukan target murni, tidak ada input gameplay/RAM poke/setter.
- BA3 memvalidasi snapshot dan layout sumber/runtime, bukan transaksi ekonomi.
- Makna action 3/8, tile+0x1C/+0x1E, helper V, manager B30/B38/B40/B44, dan nama event transfer tetap TIDAK TAHU.
- Resource 630 hanya pasti pada kombinasi mode/state H6 0/0; kombinasi lain dapat memilih resource berbeda.
- Base `0x800AD450` masih kandidat impor statis.

Kesimpulan: BA1/BA2/BA3 selesai dalam ruang lingkup audit statis + snapshot H6 yang dinyatakan pada laporan. Status ini tidak boleh diperluas menjadi bukti universal semua mode atau transaksi.
