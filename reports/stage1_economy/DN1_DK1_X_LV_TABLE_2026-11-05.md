# DN1 — lookup table X → LV1–LV5 dari 12 resource DK1

Status ekstraksi/rekonsiliasi tabel: **TUNTAS — K4 (statis)**.

Sumber: DK1_ALL_12_RESOURCE_RECORDS_2026-11-04.tsv, 12 resource DATA.BIN, 415 record. X diambil dari sumber loader-mapped `+0x08`; LV1–LV5 masing-masing dari `+0x0A,+0x0C,+0x0E,+0x10,+0x12`.

- 415 record seluruhnya terkelompok menjadi 14 nilai X (0 dan 13 nonzero).
- Semua nilai X memiliki satu set nilai LV1–LV5 yang konsisten di seluruh resource yang memuat X tersebut.
- Rumus `LV2 = 10 × ceil(11X/100)` cocok pada 415/415 record.
- Rumus LV1 belum terbukti.
- Dua kandidat rekursif LV3–LV5 yang diuji dalam DM2 tidak universal: H1 lolos 15/39 pemeriksaan level; H2 lolos 1/39. Angka LV3–LV5 karena itu disajikan sebagai lookup value resource, bukan rumus terkonfirmasi.

## Tabel lookup

| X | n | LV1 | LV2 | LV3 | LV4 | LV5 |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 167 | 0 | 0 | 0 | 0 | 0 |
| 60 | 23 | 35 | 70 | 135 | 265 | 530 |
| 100 | 34 | 50 | 110 | 220 | 440 | 880 |
| 120 | 22 | 60 | 140 | 265 | 530 | 1050 |
| 140 | 26 | 70 | 160 | 310 | 620 | 1250 |
| 160 | 25 | 85 | 180 | 360 | 710 | 1410 |
| 180 | 28 | 90 | 200 | 390 | 800 | 1600 |
| 200 | 21 | 100 | 220 | 440 | 880 | 1760 |
| 220 | 17 | 110 | 250 | 490 | 980 | 1940 |
| 240 | 9 | 120 | 270 | 530 | 1050 | 2120 |
| 260 | 20 | 130 | 290 | 580 | 1150 | 2290 |
| 280 | 17 | 140 | 310 | 620 | 1240 | 2470 |
| 300 | 4 | 150 | 330 | 660 | 1320 | 2640 |
| 320 | 2 | 160 | 360 | 710 | 1410 | 2820 |

Ini adalah nilai resource yang tersimpan dan konsisten pada sampel 12 resource DK1; bukan bukti semua game mode menggunakan seluruh X/resource yang sama. Hasil H6 runtime DN2 secara terpisah cocokkan resource `0x276` dengan live tile table 22/22 record pada empat snapshot, tanpa perubahan nilai LV.
