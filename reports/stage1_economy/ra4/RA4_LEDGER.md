# RA4 — ledger hasil RA0–RA3 dan Actions

BASELINE_INCLUSIVE=a133f0b266f211a31f26439d3a04ac8705b515e4
PARENT_HEAD=bd91cb50d1b09fe683cd175223453a98c8d9dc13
STATUS=TUNTAS
CONFIDENCE=K4
SCOPE=Semua run QA0/QA4, RA2, RA1, dan monitor terjadwal yang relevan terhadap pekerjaan ini; bukan klaim enumerasi seluruh workflow lain dalam repo.

## Status tahapan

| Tahap | Status | Keyakinan | Hasil |
|---|---|---|---|
| RA0 | TUNTAS | K4 | 15/15 baris dihapus fisik dari 10 berkas PA; union byte nyata seluruh JA/KA/LA/MA/NA/OA/PA/QA maksimum 64 byte; 0 grup >64 byte; 0 konflik byte. |
| RA2 | BELUM | K1 untuk aksi upgrade | Dua restore identik sukses, tetapi tidak ada perubahan record petak atau uang dan tidak ada hit debit. Subklaim eksekusi FUN_800D15A8 sendiri TUNTAS K5 (48 hit per launch). |
| RA1 | TUNTAS | K5 | Dua restore identik; 90 hit per breakpoint per launch; 360 pembacaan stack berhasil; saved RA pada sp+0x14 konsisten 0x80011A30. Caller outer pada 0x80011A28 masih kandidat; targetnya TIDAK TAHU. |
| RA3 | BELUM | K1 | Tidak ada sampel upgrade independen dengan d berbeda. H1/H2 tidak dibandingkan. |
| RA4 | TUNTAS | K4 | Ledger mencakup 47 job dari 41 run relevan: 6 QA run (12 job), 10 RA2, 1 RA1, 24 monitor terjadwal. |

## RA0 — perubahan fisik

Berkas M terhadap baseline. Semuanya berada di PA; tidak ada arsip JA/KA/LA/MA/NA/OA yang berubah.

| Berkas | Baris sebelum | Dihapus | Baris sesudah |
|---|---:|---:|---:|
| `reports/stage1_economy/pa-run-42482327357-static/attempt-1/PA2_GLOBAL_POINTER_SELECTOR_ACCESSES.tsv` | 2907 | 1 | 2906 |
| `reports/stage1_economy/pa-run-42482327357-static/attempt-1/PA2_V0_STORE_WINDOWS.tsv` | 47 | 2 | 45 |
| `reports/stage1_economy/pa-run-42482696764-static/attempt-1/PA2_GLOBAL_POINTER_SELECTOR_ACCESSES.tsv` | 2907 | 1 | 2906 |
| `reports/stage1_economy/pa-run-42482696764-static/attempt-1/PA2_V0_STORE_WINDOWS.tsv` | 47 | 2 | 45 |
| `reports/stage1_economy/pa-run-42483585195-static/attempt-1/PA2_GLOBAL_POINTER_SELECTOR_ACCESSES.tsv` | 2907 | 1 | 2906 |
| `reports/stage1_economy/pa-run-42483585195-static/attempt-1/PA2_V0_STORE_WINDOWS.tsv` | 47 | 2 | 45 |
| `reports/stage1_economy/pa-run-42484127968-static/attempt-1/PA2_GLOBAL_POINTER_SELECTOR_ACCESSES.tsv` | 2907 | 1 | 2906 |
| `reports/stage1_economy/pa-run-42484127968-static/attempt-1/PA2_V0_STORE_WINDOWS.tsv` | 47 | 2 | 45 |
| `reports/stage1_economy/pa-run-42484169218-static/attempt-1/PA2_GLOBAL_POINTER_SELECTOR_ACCESSES.tsv` | 2907 | 1 | 2906 |
| `reports/stage1_economy/pa-run-42484169218-static/attempt-1/PA2_V0_STORE_WINDOWS.tsv` | 47 | 2 | 45 |

Total: 15 baris dihapus dari 10 berkas; masing-masing file GLOBAL_POINTER turun 1 baris, masing-masing V0_STORE turun 2 baris. Callsite yang dilindungi tidak dihapus. Batas audit tetap 64 byte kontigu; union dihitung dari byte aktual kolom heksa per alamat, overlap identik digabung dan konflik dilaporkan. Hasil final: maksimum 64 byte, 0 grup >64 byte.

## RA2 — interpretasi run terakhir

Checkpoint adaptive-cycle-02-f180 dari run 39907655833 / artifact 12482055310 diverifikasi ukuran dan SHA-256. Dua peluncuran headless identik masing-masing mencapai 180 VSYNC. FUN_800D15A8 terkena 48 hit pada setiap peluncuran; dua breakpoint pembacaan fee 0x800D2520 dan 0x800D46EC masing-masing 0 hit. Seluruh 22 record petak tidak berubah; diff petak 0 baris; uang p0/p1 tetap 1380. Nol hit bukan bukti jalur debit tak terjangkau. Karena tidak ada upgrade aktual, level sebelum/sesudah, effect ID, dan d tetap TIDAK TAHU. Tidak ada fitting atau penggunaan konstanta 400/800/1600.

## RA1 — interpretasi caller chain

Pada dua breakpoint, register RA cocok dengan caller statis: B54DC menerima 0x800B54C0; BE5D8 menerima 0x800B54FC. Baca read-only u32(sp+0x14) berhasil untuk 360/360 hit dan bernilai 0x80011A30. Jika nilai itu adalah return address dari JAL, kandidat callsite outer adalah 0x80011A28 dengan offset main EXE 0x2228. Byte di kandidat itu belum tersedia pada report statis yang diperiksa, jadi target caller outer TIDAK TAHU.

## Ringkasan Actions

| Kelompok | Run | Job | Hasil |
|---|---:|---:|---|
| QA0/QA4 | 6 | 12 | Dua run kedua job TUNTAS; satu run QA0 SEBAGIAN karena audit union keliru dan QA4 TUNTAS; satu run QA0 BELUM/QA4 SEBAGIAN karena comparator; dua run keduanya BELUM. |
| RA2 | 10 | 10 | Sembilan run exit 1; run terakhir exit 0 namun tidak menemukan aksi upgrade, sehingga RA2 keseluruhan BELUM. |
| RA1 | 1 | 1 | TUNTAS K5, exit 0. |
| Monitor terjadwal | 24 | 24 | Semua sukses (exit 0); hanya status monitor, bukan bukti gameplay atau kesiapan player. |

Total cakupan ledger: 41 run, 47 job. Rincian job ID, source SHA, exit code, status, dan path ringkasan ada di `RA4_ACTIONS_RUNS.tsv`. Satu ringkasan teks per QA run dan per monitor terjadwal tersedia di folder `actions/`; ringkasan RA2 dan RA1 berada pada folder run masing-masing.

## Batas dan proteksi

- `STATUS.md` tidak diubah.
- Tidak ada Release yang diubah.
- Sepuluh berkas sumber yang dimodifikasi untuk pruning hanya berkas PA pada tabel di atas; tidak ada arsip JA/KA/LA/MA/NA/OA yang diubah.
- Tidak ada BIOS, ROM, savestate, RAM dump, atau binary runtime masuk Git.
- RA1/RA2 hanya membaca memori/register; tidak ada poke memori atau register.
- Workflow RA1 memakai filter path spesifik dan self-test menyatakan tidak ada benturan.

Daftar setiap berkas yang berubah pada commit terkait ada di `RA4_COMMITS.tsv`; daftar berkas dalam commit ledger ini ada di `RA4_LEDGER_COMMIT_FILES.tsv`.
