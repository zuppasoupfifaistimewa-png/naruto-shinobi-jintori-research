# RA4 — ledger terkoreksi RA0–RA3 dan seluruh Actions relevan

BASELINE_INCLUSIVE=a133f0b266f211a31f26439d3a04ac8705b515e4
PARENT_HEAD=700e772c127e935ee2fe82956a5a3821907ed08e
STATUS=TUNTAS
CONFIDENCE=K4
SCOPE=50 Actions runs / 56 jobs yang tercatat dalam ledger: QA0/QA4, RA2, RA1, delapan run sampingan KA/LA/MA/NA, serta 25 monitor terjadwal. Ini bukan enumerasi seluruh workflow historis repo di luar lingkup audit.

## Status tahapan

| Tahap | Status | Keyakinan | Hasil |
|---|---|---|---|
| RA0 | TUNTAS | K4 | 15/15 baris dihapus fisik dari 10 berkas PA; union byte aktual 266 evidence TSV dari arsip JA/KA/LA/MA/NA/OA/PA/QA maksimum 64 byte; nol grup >64 byte; nol konflik. |
| RA2 | BELUM | K1 untuk aksi upgrade; K5 subklaim fungsi | Dua restore identik dan 180 VSYNC tiap peluncuran. FUN_800D15A8 terkena 48 hit/peluncuran, tetapi tidak ada perubahan level/petak/uang dan tidak ada hit jalur pembacaan biaya. |
| RA1 | SEBAGIAN | K5 untuk observasi stack; K4 untuk decoding statis | Caller langsung BE5D8 = JAL di B54F4 terbukti; B54DC dan B54F4 terdekode dari Entry 1. Stack RA tersimpan 0x80011A30 pada 360/360 hit. Kandidat caller terluar 0x80011A28 belum punya byte/target terverifikasi. |
| RA3 | BELUM | K1 | Tidak ada sampel upgrade independen dengan d berbeda; H1 dan H2 belum dibandingkan. |
| RA4 | TUNTAS | K4 | 50 run / 56 job dicatat, termasuk semua gagal, job terjadwal, dan delapan run sampingan KA/LA/MA/NA. |

## RA0 — verifikasi fisik dan union aktual

Batas audit tetap **64 byte kontigu**. Tidak ada pelonggaran gerbang. Harness QA0 membandingkan sumber baseline dengan HEAD, memverifikasi penghapusan fisik, lalu menggabungkan byte dari kolom heksa aktual per alamat. Overlap identik digabung; konflik byte dihitung terpisah. Berkas QA0 hasil turunan tidak dihitung sebagai sumber byte independen.

Hasil run audit akhir 42531023381:
- TSV kandidat: 677; QA0 generated TSV dikecualikan: 38; evidence TSV yang diaudit: 266.
- Baris byte heksa: 132896; alamat byte unik: 94536; konflik overlap: 0.
- Penghapusan fisik: 15/15 baris dari 10/10 berkas.
- Maksimum union: 64 byte; grup >64 byte: 0.
- Protected callsite rows removed: 0; protected callsite files changed: 0.
- Berkas JA/KA/LA/MA/NA/OA changed: 0.
- STATUS.md atau Release changed: 0.
- Self-test: PASS; Python compile: 75/75; workflow path collision: 0.

**Daftar berkas M terhadap baseline** (baris data sebelum → dihapus → sesudah):

| Berkas | Sebelum | Dihapus | Sesudah |
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

Callsite yang tidak boleh dihapus tetap ada: F5F54, B54DC, dan F5EBC. QA0 physical deletion verification untuk seluruh 15 baris menyatakan rows_remaining_at_head=0. Tidak ada grup >64 byte yang tersisa; tidak ada grup residual untuk dilaporkan.

## RA1 — caller langsung dan pembacaan stack read-only

Rantai lokal Entry 1 menggunakan offset file **0x10BB000 + (PC - 0x800AD450)**:

| PC | Offset Entry 1 | Bytes | Instruksi |
|---|---:|---|---|
| 0x800B54DC | 0x010C308C | 96 CD 03 0C | jal 0x800F3658 |
| 0x800B54F4 | 0x010C30A4 | 76 F9 02 0C | jal 0x800BE5D8 |

Breakpoint Exec pada B54DC dan BE5D8 menghasilkan 90 hit per breakpoint pada setiap peluncuran identik. Register RA saat hit: B54DC → 0x800B54C0; BE5D8 → 0x800B54FC. Pembacaan u32 read-only pada sp+0x14 berhasil 360/360 kali; nilainya selalu 0x80011A30, tanpa error dan tanpa memory/register write.

Jika saved RA 0x80011A30 merupakan return address dari JAL, kandidat callsite outer adalah 0x80011A28 (EXE file offset 0x2228). **Byte instruksi dan target pada 0x80011A28 = TIDAK TAHU** karena belum ditemukan pada laporan statis yang diperiksa. Maka rantai langsung dan satu tingkat saved-RA telah diidentifikasi, tetapi caller terluar belum tertutup.

## RA2 — hasil dua restore terbatas

Checkpoint adaptive-cycle-02-f180 dari source run 39907655833 / artifact 12482055310 diverifikasi ukuran dan SHA-256. PCSX-Redux menjalankan dua restore identik, masing-masing 180 VSYNC, dengan input CIRCLE pada frame 30–35.

- FUN_800D15A8: 48 hit tiap peluncuran (K5 untuk eksekusi fungsi dalam kondisi ini).
- Exec breakpoint fee-read 0x800D2520 dan 0x800D46EC: masing-masing 0 hit pada kedua peluncuran.
- 22 record petak di base 0x8013EA84 dengan stride 0x124; tidak ada perbedaan record.
- Uang p0/p1 sebelum dan sesudah: 1380/1380.
- Tabel aksi upgrade kosong; tidak ada perubahan level atau debit.

Level sebelum/sesudah, effect ID, dan d = **TIDAK TAHU**. Nol hit tidak membuktikan jalur tidak terjangkau. Tidak ada rumus, konstanta 400/800/1600, atau fitting yang dibuat dari hasil ini. Skenario QA1_QA3 yang tercatat hanya mengusulkan satu konfirmasi UI dan, sebagai kondisi terpisah, satu transisi board/tile-action; belum ada urutan yang terverifikasi menghasilkan upgrade.

API yang digunakan telah dicocokkan dengan dokumentasi resmi PCSX-Redux:
- Breakpoint Exec dan retensi objek: https://pcsx-redux.consoledev.net/Lua/breakpoints/
- Memory/register read API: https://pcsx-redux.consoledev.net/Lua/memory-and-registers/
- Pads setOverride/clearOverride dan event: https://pcsx-redux.consoledev.net/Lua/redux-basics/
- Sesi scripted berbasis VSYNC dan input tap: https://pcsx-redux.consoledev.net/Lua/playbook-scripted-session/

## RA3 — gerbang H1/H2

Jumlah sampel upgrade independen: 0. H1 (x=d) dan H2 (x=effect/item/action ID) belum diuji. Support dan falsifier global keduanya tetap TIDAK TAHU. Formula biaya upgrade untuk d>=2 tetap TIDAK TAHU. Tidak ada konstanta 400/800/1600 dan tidak ada curve fitting.

## RA4 — cakupan semua Actions relevan

| Kelompok | Run | Job | Ringkasan |
|---|---:|---:|---|
| QA0/QA4 | 6 | 12 | Termasuk 2 run final lulus; run lama yang salah, gagal, dan comparator error tetap dicatat. |
| RA2 | 10 | 10 | 9 job gagal (exit 1); 1 job selesai exit 0 tetapi tidak menemukan upgrade (RA2 tetap BELUM). |
| RA1 | 1 | 1 | Job sukses (exit 0); stage SEBAGIAN karena caller outer masih TIDAK TAHU. |
| KA/LA/MA/NA side-effect runs | 8 | 8 | 6 sukses; 2 LA gagal pada langkah publikasi setelah analisis statis. |
| Monitor terjadwal | 25 | 25 | Seluruh 25 sukses (exit 0), monitor saja—bukan bukti gameplay/adaptive readiness. |
| **Total** | **50** | **56** | **39 job exit 0; 17 job exit 1.** |

Job ID, source SHA, stage status, exit code, dan path ringkasan setiap run tersedia di `RA4_ACTIONS_RUNS.tsv`. Satu file ringkasan pendek per Actions run tersedia di `ra4/actions/`; run RA1/RA2 juga punya ringkasan khusus pada folder run masing-masing. Permalink raw terverifikasi dicatat di `RA4_ACTIONS_RAW_LINKS.txt`.

## Batas / perlindungan

- `STATUS.md` tidak diubah.
- Release tidak diubah.
- Tidak ada arsip JA/KA/LA/MA/NA/OA yang diubah.
- Tidak ada BIOS, ROM, savestate, raw RAM dump, atau binary runtime di Git.
- RA1/RA2 menggunakan pembacaan memori/register saja; tidak ada poke memory/register.
- Tidak ada workflow baru dalam pembaruan ledger ini; tidak ada filter path workflow lain yang dilonggarkan.
- Semua klaim runtime K5 berasal dari dua peluncuran identik; klaim statis tertinggi K4.

**Koreksi final jumlah ledger:** ringkasan tahap RA4 di tabel telah diselaraskan dengan 50 run unik dan 56 baris job pada `RA4_ACTIONS_RUNS.tsv` (25 monitor terjadwal). Commit koreksi ini hanya mengubah berkas `reports/stage1_economy/ra4/RA4_LEDGER.md`.
