# BB_STATE — checkpoint audit Barrier/Chakra

Tanggal: 3 November 2026
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Baseline yang diminta: ee4d17f1e9de2e37531bec5934b684712929e976
HEAD aktif sebelum checkpoint: ee4d17f1e9de2e37531bec5934b684712929e976

## Status sementara

| Butir | Status | Kepastian | Bukti/ruang lingkup | Berikutnya |
|---|---|---|---|---|
| BB1 | SEBAGIAN | K4 statis untuk fungsi pengelompokan dan data resource 630 | Penulis +0x0B terindikasi pada FUN_800BE0E4: PC 0x800BE1B0 (reset) dan 0x800BE330 (hasil hitung rantai). Tabel 22 record tersedia dari Entry 630. | Verifikasi ulang census displacement +0x0B/+0x20 setelah memperbaiki parser exporter yang sebelumnya membaca angka heksadesimal sebagai desimal. Lalu tetapkan semua writer dan hasil level. |
| BB2 | SEBAGIAN | K4 untuk cabang transaksi dalam FUN_800D15A8; K2 untuk pemetaan writer action byte | Cabang action byte 3/8 membaca fee tile+0x1A, menulis -fee ke pending +0x2EE, dan menaikkan dua nibble level. Kandidat producer PC 0x800DAA88 (3), 0x800EC3A8 (8), serta kandidat belum pasti 0x800EF3CC. | Audit seluruh producer/base alias dan pemicu cabang kredit positif; pisahkan label aksi dari bukti instruksi. |
| BB3 | BELUM | K2 untuk H6 smoke read-only; K0 untuk transaksi | H6 hybrid SHA-256 d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475; run 41536404671 menghasilkan hanya kasus pertama NO_RESULT, wrapper exit 137 pada timeout 360.044 s. | Perbaiki urutan resume setelah load state, jalankan matriks minimal multi-tile × level 0–4 × action 3/8 × dua launch, kemudian evaluasi syarat K5. |

## PC kunci yang sudah diperiksa

- FUN_800BE0E4: 0x800BE1B0, 0x800BE330; data array kandidat DAT_8013EA84, record stride 0x124, record +0x0B selector, +0x01 link-index, +0x20 owner/level word.
- FUN_800D15A8: 0x800D45D0 selector tile, 0x800D4628 fee read, 0x800D46F8 pending debit, 0x800D4728/0x800D4764 first nibble update, 0x800D47F8/0x800D4834 second nibble update; refresh calls 0x800D4840/0x800D4848.
- Action-byte +0x2EB candidate stores: 0x800DAA88 (FUN_800D9570, candidate value 3), 0x800EC3A8 (FUN_800EB434, candidate value 8), 0x800EF3CC (function/base provenance unresolved).

## Actions/evidence keys

- Static census Actions run 41533205025; job 125578418688; source SHA 111bf1a3f4177f356e513d2fdea1de2c50f6e697; workflow SUCCESS; script exit 0.
- Runtime probe Actions run 41536404671; job 125590686714; source SHA 4159e1b27018cae970eac64013e25a98c78013ee; workflow success as publisher only; BB3 probe SEBAGIAN/NO_RESULT, script exit 1, workflow-process exit 2, wrapper exit 137.
- Exporter correction in this checkpoint fixes hexadecimal parsing in ExportBB2TileNibbleAudit.java; the next push should start Step7 static audit automatically.

## Batas tetap

H6 adalah HIBRIDA, bukan bukti Story Mode murni. Tidak ada klaim K5 dari snapshot smoke atau dari status workflow SUCCESS tanpa hasil transaksi. Tidak ada label Barrier Release untuk B44. Tidak ada upload ISO/BIOS/savestate/RAM dump/video/frame pada pekerjaan ini.
