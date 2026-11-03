# BB2 — audit lanjutan menyeluruh DATA.BIN dan objek pesan

Tanggal: 3 November 2026  
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

## Putusan

BB1 tetap **TUNTAS K4 statis**. BB3 tetap **TUNTAS K5 terbatas** untuk direct function-call pada fixture H6 HIBRIDA. BB2 tetap **SEBAGIAN K4 mekanisme**; nama aksi gameplay dan pemetaan teks/prompt belum terbukti. Pemeriksaan tambahan ini tidak mengubah label gameplay.

## Run 41565392810 — scan semua entri direktori DATA.BIN

- STATUS=SUCCESS; JOB=analyze-entry1-buffer-base; JOB_ID=125685566730; SOURCE_SHA=6d5a70e73ada1d68b279093272a76bf154028213; EXIT_CODE=0.
- DATA.BIN terverifikasi: 66.015.232 byte, SHA-256 `69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822`.
- Seluruh 1.504 slot direktori diperiksa: 1.500 entri non-kosong valid, 0 rentang invalid. Setiap entri valid diberi hash; pencarian byte literal dilakukan pada seluruh entri.
- Pencarian literal istilah Jepang/Inggris yang relevan menghasilkan 0 hit: `結界開放`, `結界解放`, `結界解除`, `結界`, `チャクラ`, `バリア`, `障壁`, `開放`, `解放`, `解除`, `強化`, `建設`, `建築`, `増築`, `消費`, `費用`, `料金`, `価格`, `所持`, `所有`, `増加`, `獲得`, dan istilah Inggris Barrier/Chakra/release/upgrade/build/cost.
- Ekstraksi run Shift-JIS heuristik mencapai batas ekspor 50.000 run; 0 dari 50.000 run yang diekspor memuat petunjuk istilah di atas. Ini **bukan** decoding seluruh string di semua 1.500 entry: keluaran dibatasi 50.000 run dan sebagian hasil terlihat sebagai false-positive/gibberish Shift-JIS.
- Tidak ada varian gzip/zlib standar yang berhasil didekompresi. Format kompresi khusus, tabel glyph/index, atau string di luar DATA.BIN belum diperiksa. Maka nol hit byte literal **tidak membuktikan** bahwa teks UI tidak tersedia.

## Pemeriksaan objek pesan Main EXE

- `FUN_80032A98` meneruskan parameter ID ke `FUN_8001AAD4`, lalu mengatur field objek pesan. Ia memilih kode tambahan `0x21F` atau `0x220` menurut hasil `FUN_8002F698(0)`. Caller yang diekspor memasok beberapa ID, antara lain `0x218`, `0x21A`, `0x22B`, `0x23A`, dan ID sekitar rentang itu. Fungsi ini adalah pembangun objek pesan generik; hasil ini belum menyebut token `0xBE`.
- `FUN_8001BA58` mengembalikan halfword dari tabel yang didapat melalui `FUN_8001A63C()`, pada offset `id*4 + 0x0A`. Dalam jalur yang diperiksa, nilai itu dipakai sebagai metadata inisialisasi objek; belum terbukti merupakan teks atau indeks event Barrier.
- `FUN_80029FF0` membuat parameter pesan dari gabungan parameter pemanggil dan tabel/data manager (`DAT_800657CC`); ID tidak tampak sebagai konstanta event tetap di fungsi ini. Caller langsung yang terdata adalah `FUN_80028C08`.
- Hasil ini menguatkan bahwa pemetaan ID pesan memerlukan tabel/resource dan konteks caller. Tidak ada rantai yang membuktikan `0xBE = 結界開放`.

## Status hipotesis yang tetap terbuka

| Hipotesis | Status | Bukti pembatal |
|---|---|---|
| HA: action 3 membangun Barrier, action 8 meng-upgrade | HIPOTESIS | Prompt/menu normal atau perubahan petak membuktikan urutan/aksi lain |
| HB: action 3 meng-upgrade, action 8 membangun Barrier | HIPOTESIS | Prompt/menu normal atau perubahan petak membuktikan urutan/aksi lain |
| HC: satu/keduanya bukan pasangan build/upgrade Barrier | HIPOTESIS alternatif | Kedua prompt dan transisi petak normal membuktikan pasangan build lalu upgrade |
| HP: +0x2EB=1/0x1D adalah Barrier Release | HIPOTESIS K1 | Prompt/teks atau transisi normal menunjukkan aksi lain/tidak melepas Barrier |
| HQ: +0x2EB=1/0x1D adalah aksi tile positif lain | HIPOTESIS K1 | Prompt `結界開放` dan pelepasan Barrier terjadi pada state yang sama |

Fakta yang tetap terkonfirmasi: cabang action 3/8 berbagi blok debit fee `u16(tile+0x1A)`, menaikkan dua nibble level, dan diuji 40/40 pada BB3 H6 HIBRIDA; jalur positif `+0x2EB=1/0x1D` dapat mengkredit field Chakra kanonis lewat `FUN_800BE5D8 → FUN_8001387C`. Label transaksi dan biaya gameplay Barrier masih **TIDAK TAHU**.

## Referensi output

- Run summary: `reports/stage1_economy/aq1-run-41565392810/attempt-1/ACTIONS_RUN_SUMMARY.txt`
- Laporan scan DATA.BIN: `reports/stage1_economy/aq1-run-41565392810/attempt-1/BB2_FULL_DATABIN_TEXT_SCAN.txt`
- TSV run heuristik: `reports/stage1_economy/aq1-run-41565392810/attempt-1/bb2-full-databin-text-scan.tsv`
- Main EXE objek pesan: `reports/stage1_economy/aq1-run-41565392810/attempt-1/az3-main-exe-economic-helper-detail.txt`

Scope run: Ghidra statis; game/emulator tidak dijalankan; input kontrol tidak dikirim; savestate tidak direstore; source disc/DATA.BIN dan proyek Ghidra dibersihkan; hanya laporan teks/TSV dipublikasikan.
