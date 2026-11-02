# Status BB0–BB3 — audit logika Barrier/Chakra
Tanggal: 2 November 2026
Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)

## Catatan penomoran

Pada branch `main` tidak ditemukan dokumen definisi/acceptance criteria bernama BB0, BB1, atau BB2. Karena itu, tabel di bawah adalah pengelompokan bukti Barrier/Chakra yang memang tersedia di repo, bukan klaim bahwa definisi tahap BB yang mungkin berada di percakapan lain sudah berhasil direkonsiliasi.

## Status

| Tahap | Status | Batas |
|---|---|---|
| BB0 — observasi barrier placement dan debit Chakra | SELESAI untuk satu jalur Story Mode | Satu transaksi teramati; tidak universal. |
| BB1 — sumber data biaya dan pemetaan record petak | SELESAI untuk resource 630 pada H6 | Mapping source/runtime valid; tidak membuktikan seluruh resource/board. |
| BB2 — dekompilasi debit transaksi dan kenaikan level | SELESAI statis K4 untuk action byte 3/8 | Nama gameplay action dan kaitannya secara khusus dengan barrier tetap TIDAK TAHU. |
| BB3 — validasi runtime pembacaan/mutasi transaksi | BELUM | Restore H6 ke PCSX-Redux crash; belum ada hit dispatch atau pembacaan RAM pasca-load. |

## BB0 — barrier placement yang benar-benar teramati

Run 39617444912 menggunakan prompt kontekstual:
- `ここに結界をはりますか？` (Apakah akan memasang penghalang di sini?)
- `必要チャクラ 120` (Chakra yang dibutuhkan: 120)
- Pilihan `はい` (Ya) terlihat tersorot.
- Setelah satu Circle confirm yang sesuai konteks, barrier/orb biru terlihat; HUD Naruto berubah 1500 → 1380, sementara Mizuki tetap 1500.
- Bukti screenshot yang dicatat dalam `docs/SIGSEGV_FORENSICS_2026-10-21.md` memperlihatkan kondisi hasil pada f60, f100, dan f120.

Kesimpulan terbatas: placement pada path tersebut mengurangi Chakra Naruto sebesar 120. Ini tidak membuktikan biaya untuk tile lain, level lain, atau semua tipe barrier.

## BB1 — source data petak

Artefak:
- `reports/stage1_economy/BA_FINAL_REPORT_2026-11-02.md`
- `reports/stage1_economy/BA1_STAGE1_RESOURCE_630_RECORDS.tsv`
- `reports/stage1_economy/BA2_TILE_RUNTIME_FIELD_MAP.tsv`
- `reports/stage1_economy/BA3_TILE_FIELD_VALIDATION.tsv`

Temuan:
- Selector pada empat snapshot H6 memilih resource ID 630.
- Resource 630 berisi 22 record dengan source stride 0x1E; runtime tile stride 0x124.
- 18 field salinan: 1.584/1.584 cocok; dua field initializer: 176/176 cocok; total 1.760/1.760 cocok pada empat snapshot H6.
- Source bytes +0x13..+0x14 disalin sebagai halfword little-endian ke runtime tile+0x1A.
- Source bytes +0x15..+0x16 → tile+0x1C; +0x17..+0x18 → tile+0x1E.
- Untuk resource 630, nilai tile+0x1A per index 0–21 adalah:
  `0, 50, 50, 50, 100, 0, 100, 120, 100, 100, 100, 0, 150, 150, 200, 150, 150, 0, 0, 100, 100, 50`.

Penting: nilai tile+0x1A di atas adalah nominal field resource yang dibaca handler action 3/8. Belum terbukti bahwa seluruh angka tersebut adalah biaya pemasangan Barrier; jangan menyamakan angka prompt 120 pada BB0 dengan semua isi field ini.

## BB2 — jalur statis debit action 3/8

Laporan sumber: `reports/stage1_economy/AZ0_AZ3_FINAL_STATUS_2026-11-02.md`.

Rantai yang ditemukan pada `FUN_800D15A8`:
1. Membaca action byte pada participant manager +0x2EB; cabang yang dianalisis adalah nilai 3 atau 8.
2. Memilih index petak melalui `FUN_800BBD9C()`.
3. Membaca `fee = u16(tile+0x1A)`.
4. Memeriksa bahwa fee tidak melebihi saldo kerja participant +0x04.
5. Jika cukup, menulis pending delta participant +0x2EE = `-fee`.
6. Menaikkan nibble tile+0x20 bits 8–11 dan bits 4–7 masing-masing satu.
7. Memanggil `FUN_800BB004` dan `FUN_800BE464` untuk pembaruan representasi/atribut petak.
8. `FUN_800BE5D8` memproses pending signed delta, menyinkronkan saldo lewat setter `0x8001387C` dan getter `0x800138EC`, lalu membersihkan pending slot.

Kesimpulan: jalur biaya action 3/8 secara statis K4. Nama gameplay action 3 vs 8 dan hubungan langsungnya dengan barrier placement yang terlihat di BB0 belum teridentifikasi. Rumus positif `tile+0x1E + level × tile+0x1C` adalah cabang terpisah; label gameplay-nya tetap TIDAK TAHU.

### BB2 — pemetaan PC instruksi yang dapat dipakai untuk verifikasi BB3

Pemeriksaan ulang dekompilasi dan raw MIPS untuk `FUN_800D15A8` (Entry 1, ukuran body 17.944 byte) mengonfirmasi bahwa label `case 3` dan `case 8` berada dalam satu blok transaksi pada `LAB_800D4468`. Jadi kedua nilai action-byte itu memang target uji yang benar; kesimpulan tersebut tidak berasal dari menafsirkan nilai jenis petak.

Urutan instruksi raw yang terkait:

| PC | Instruksi/makna |
|---|---|
| `0x800D4468` | Memuat pointer manager; blok `switch(action byte +0x2EB)` dimulai pada label ini. |
| `0x800D4470` | Membaca action byte `manager+0x2EB`; jump table membedakan action. |
| `0x800D45D0` | Memanggil `FUN_800BBD9C()` untuk memilih petak. |
| `0x800D45E0` | Menyimpan indeks terpilih ke `manager+0x4A0`. |
| `0x800D4628` | Membaca `u16(tile+0x1A)` sebagai fee. |
| `0x800D462C`–`0x800D4638` | Membaca saldo kerja `participant+0x04`, membandingkan fee dengan saldo, dan menuju jalur gagal bila saldo kurang. |
| `0x800D46EC`–`0x800D46F8` | Membaca fee, menegasikan nominalnya, lalu menyimpan signed delta ke `participant_manager+0x2EE`. |
| `0x800D4724`–`0x800D4764` | Menghapus dan menulis ulang nibble bits 8–11 dengan level lama +1. |
| `0x800D47F4`–`0x800D4834` | Menghapus dan menulis ulang nibble bits 4–7 dengan level lama +1. |
| `0x800D4840`, `0x800D4848` | Memanggil `FUN_800BB004` dan `FUN_800BE464` sesudah mutasi level. |

Ini memperkuat BB2 sebagai K4 statis. Probe BB3 saat ini memasang breakpoint pada dispatch `0x800D4468`, sesudah return selector `0x800D45D8`, dan sebelum refresh tile `0x800D4838`; ketiga lokasi tersebut berada di dalam blok yang telah dicocokkan dengan instruksi di atas.

Catatan semantik: nama gameplay untuk action byte 3 dan 8 masih **TIDAK TAHU**. Keduanya hanya terbukti masuk ke satu blok transaksi yang sama pada fungsi ini.

## BB3 — hasil uji runtime dan blocker

### Run 41459907683 — function-call probe

- 16/16 peluncuran (action 3 dan 8 × level 0–3 × dua attempt) menghasilkan `NO_RESULT`.
- `action_dispatch_reached=NO`, `selected_tile_override=NO`.
- Wrapper exit code -11 pada seluruh peluncuran; wall time sekitar 2,55–2,75 detik.
- Memory Card tidak berubah.
- Positive-control formula tidak dijalankan.

Berkas: `reports/stage1_economy/bb3-h6-action-call-probe-run-41459907683/attempt-1/`.

### Run 41461812798 — smoke awal

- Timeout 900 detik.
- Log menunjukkan Lua command-line error karena string newline ber-escape ganda; H6 load event tidak tercapai.
- Memory Card tidak berubah; tidak ada RAM write dan tidak ada input gameplay.

### Perbaikan dan run 41464827189 — smoke ulang

Perbaikan:
- Commit `7256c5932a9d34e5ea4d04b0ef39604d1843d586` mengubah escape newline ganda pada `experiments/bb3_h6_smoke.py` menjadi escape newline Python yang benar.

Hasil:
- Workflow/job success hanya berarti pengumpulan dan cleanup selesai.
- Script exit code 2; emulator exit code -11; wall time 2,813 detik.
- Log mencapai `BB3_SMOKE_LOAD_BEGIN=1`, lalu `timeout: the monitored command dumped core`.
- Tidak ada `BB3_SMOKE_SAVE_STATE_LOADED=1`; memory-file read tidak dijalankan.
- Memory Card SHA-256 sebelum/sesudah tetap `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- Tidak ada RAM write dan tidak ada gameplay input.

Ringkasan:
`reports/stage1_economy/bb3-h6-smoke-run-41464827189/attempt-1/`.

Keputusan: jangan ulangi load H6 yang identik. BB3 runtime belum selesai. Lanjutkan analisis dengan static parse/analisis Ghidra; percobaan runtime baru memerlukan jalur checkpoint yang tidak crash dan bukti dispatch yang terukur.

## Kesimpulan akhir

BB0, BB1, dan BB2 selesai hanya dalam batas eksplisit di atas. BB3 belum selesai. Karena nama/criteria BB0–BB2 tidak tercatat di repo, kesesuaian pengelompokan ini terhadap checklist BB asli tidak dapat dipastikan (**TIDAK TAHU**). Tidak ada dasar untuk menyatakan seluruh BB0–BB3 telah selesai.

Tidak ada ROM/ISO, BIOS, savestate, Memory Card, raw RAM, screenshot, video, atau binary yang dikomit dalam laporan ini.
