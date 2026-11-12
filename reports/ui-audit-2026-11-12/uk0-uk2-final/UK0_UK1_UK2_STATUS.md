# UK0–UK2 — laporan pemeriksaan batas eksekusi

Tanggal pemeriksaan: 2026-11-12 (WIB)
Baseline inklusif: `b54ff5d5e52d5196459ea190a5322d8746b96eb1`
Repo/branch: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research` / `main`

## Ringkasan

| Tahap | Status | Evidensi | Hasil |
|---|---|---|---|
| UK0 | BELUM | K0 untuk hasil scan yang diminta | Alat UK0 yang ada bukan pemindai stride/field yang dispesifikasikan; EXE dan DATA.BIN privat tidak tersedia pada sesi ini untuk menjalankan scan byte. |
| UK1 | BELUM | K0 | Tidak ada run emulator UK1 yang dijalankan. Workflow yang ada tidak dapat menjalankan spesifikasi UK1 baru dan tidak dapat dipicu dari direktori laporan. |
| UK2 | SEBAGIAN | K2 untuk dua run monitor yang diperiksa; inventaris total TIDAK TAHU | Baseline adalah HEAD saat pemeriksaan; sebelum publikasi laporan, commit inklusif = 1 (baseline saja), file events setelah baseline = 0. Inventaris seluruh Actions run tidak dapat diambil dari antarmuka yang tersedia. |

## UK0 — pemeriksaan alat dan cakupan

File yang diperiksa pada baseline:
- `.github/workflows/uj0-uj2-readonly-audit.yml`
- `tools/stage1/RunUJ0StaticAudit.py`

`RunUJ0StaticAudit.py` menjalankan PS-X EXE header check, rekonsiliasi 307 baris UH1 dan mengeluarkan kutipan fungsi yang telah ditentukan. Ia tidak memindai idiom stride 292 yang diminta, tidak membangun tabel akses semua medan rekaman dalam jendela 24 instruksi, dan tidak memisahkan daftar kecocokan idiom dari non-kecocokan. Oleh karena itu tidak ada hit/miss UK0 yang dapat dilaporkan dan tidak ada klaim ketiadaan akses.

Rumus offset yang dipakai alat:
- EXE: `0x800 + (PC - 0x80010000)` (script membaca T_ADDR dari header; laporan script menampilkan nilai header yang terbaca).
- Entry 1: `0x10BB000 + (PC - 0x800AD450)`.

Batas analisis yang harus dipertahankan pada implementasi UK0: pencarian hanya akan menangkap pola pointer yang dibentuk sesuai idiom eksplisit; pointer yang telah dihitung sebelum jendela atau diwariskan sebagai argumen tidak otomatis tertangkap. Asal basis +0x48 dan semantik medan tetap TIDAK TAHU.

Kutipan kode UK0 tidak dibuat karena belum ada hasil disassembly yang memenuhi permintaan. Tidak ada kutipan byte yang direka.

## UK1 — pemeriksaan workflow dan skrip

Skrip `experiments/uj1_readonly_snapshot.py` pada baseline masih:
- mengambil snapshot pada frame 1 dan frame 900, bukan frame 1 saja;
- membaca basis A dan B, masing-masing dengan 44 indeks kandidat;
- mengambil lima medan terpilih per rekaman, bukan seluruh byte 0x00..0x123;
- melakukan bootstrap Memory Card 12 frame sebelum dua launch terukur.

Karena itu menjalankan skrip tersebut akan melanggar spesifikasi UK1 yang diberikan. Tidak ada emulator dijalankan, tidak ada bootstrap, dan tidak ada Memory Card/checkpoint yang diubah atau diklaim telah diverifikasi sebelum/sesudah.

Workflow lama:
- hanya memiliki trigger `push` pada perubahan path tertentu; tidak ada `workflow_dispatch`;
- job audit bergantung pada preflight dan memiliki kondisi SHA sumber tetap `e0ad8bf89ca43dda6b84272382ab468f0bdb28ef`;
- perubahan hanya di direktori laporan tidak termasuk path pemicu;
- menjalankan job tersebut akan menjalankan skrip UJ1 lama yang tidak cocok dengan kebutuhan UK1.

Tidak ada run Actions UK1 baru yang dibuat. Ini disengaja untuk menghindari peluncuran yang diketahui tidak sesuai, bukan hasil emulator yang gagal.

## UK2 — ledger yang dapat dipastikan

Baseline yang diminta sama dengan HEAD yang diberikan saat pemeriksaan. Dengan rentang inklusif yang berakhir tepat sebelum commit publikasi laporan ini:
- commit rows termasuk baseline: 1;
- commit setelah baseline: 0;
- file events `--no-renames` setelah baseline: 0.

Dua run monitor yang secara eksplisit diminta telah diperiksa melalui data job:
- Run `43109652913`: job `monitor`, job ID `130821994581`, completed/success; tidak ada artifact pada daftar artifact yang dikembalikan.
- Run `43145985922`: job `monitor`, job ID `130943778885`, completed/success; tidak ada artifact pada daftar artifact yang dikembalikan.

Untuk kedua run tersebut, daftar langkah yang terlihat: setup, checkout policy monitor, inspect recent adaptive-player run/duration/private evidence artifact, upload monitoring report, post-checkout, complete job. Ini hanya status job monitor, bukan bukti bahwa adaptive player/gameplay dijalankan atau Story Mode selesai.

Inventaris semua Actions run sejak baseline, termasuk semua run lain, status run lengkap, dan source SHA per run: TIDAK TAHU. Antarmuka yang tersedia untuk pemeriksaan ini tidak menyediakan endpoint daftar seluruh workflow runs; halaman Actions GitHub juga tidak dapat di-fetch. Dua run di atas bukan inventaris lengkap.

## Validasi dan integritas

- `py_compile`: BELUM dijalankan untuk implementasi UK0/UK1 baru karena implementasi tersebut tidak dibuat.
- `pyflakes`: BELUM.
- Parse YAML: BELUM sebagai pengujian eksekusi; file workflow dibaca dan diperiksa secara statis.
- `actionlint`: BELUM.
- Run emulator UK1: TIDAK DIJALANKAN.
- ROM/BIOS/Memory Card/savestate/RAM dump/EXE/DATA.BIN atau biner lain dikomit: TIDAK.
- `STATUS.md`, Release, dan workflow lama diubah: TIDAK.

## Berkas yang diubah

- `reports/ui-audit-2026-11-12/uk0-uk2-final/UK0_UK1_UK2_STATUS.md`

Kesimpulan: UK0 dan UK1 BELUM tuntas; UK2 SEBAGIAN. Tidak ada dasar untuk menyatakan hasil scan byte, snapshot runtime frame-1, atau inventaris seluruh Actions telah selesai.
