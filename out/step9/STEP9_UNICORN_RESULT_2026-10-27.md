# Langkah 9 — eksekusi fungsi RNG MIPS secara terisolasi

Tanggal: 27 Oktober 2026  
Status: **TUNTAS untuk uji fungsi RNG utama yang didefinisikan di bawah; bukan verifikasi seluruh fungsi game.**

## Provenance dan artefak

- Run [GitHub Actions #40474891838](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474891838) berstatus `success`; checkout commit `6d332244607298154c51fbd3f16ff7718483e6b2`.
- Artefak teks-only [#12720127454](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474891838/artifacts/12720127454), 3.201 byte, digest SHA-256 ZIP `bcbfcd77a532ce34334ed60f720fdeaac566308bf2e6e4d54a7e60f28a5f083b`, tidak kedaluwarsa saat pencatatan.
- Executable yang diverifikasi sebelum probe: `SLPS_035.53`, 385.024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`; PS-X EXE entry PC `0x80011448`, text load `0x80010000`, text size `0x5D800`. Disc/CUE diperiksa dengan ukuran dan SHA-256 yang dipatok; executable diekstrak pada runner dan diverifikasi hash-nya.
- Python 3.13.18 dan Unicorn 2.1.4; engine MIPS32 little-endian berhasil dibuat.
- Tidak dijalankan emulator PS1, BIOS, loader game, event loop, tampilan, kontrol/input, atau gameplay. Executable/disc hanya dibaca di runner privat. Artifact hanya berisi laporan teks, stage, log probe dan log ekstraksi; step cleanup mencatat `STEP9_PRIVATE_CLEANUP=PASS`.

## Metode dan memory map

Rutin `0x80035D78` yang memakai global `0x800A3118` dijalankan sebagai rentang instruksi MIPS32 terisolasi dengan 7 state input. Keluaran yang diuji adalah state baru di RAM dan nilai register `v0` yang dikembalikan; fungsi harus mengembalikan kontrol ke sentinel return dalam 128 instruksi maksimum.

- PS1 RAM adalah 2 MiB: alamat virtual KSEG0 `0x80000000–0x801FFFFF` beralias ke alamat fisik `0x00000000–0x001FFFFF`. Percobaan pertama [run #40474699863](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474699863) memetakan RAM hanya pada alamat virtual. Hasilnya 0 instruksi/7 vektor dan tidak ada perubahan state. Hasil itu adalah kegagalan model alamat, bukan bantahan terhadap fungsi RNG.
- Probe dikoreksi untuk memetakan RAM fisik `0x00000000–0x001FFFFF`, menaruh text pada alamat fisik alias `0x00010000`, menaruh state pada `0x000A3118`, memulai fungsi pada alias fisik `0x00035D78`, dan menghentikan eksekusi pada sentinel fisik `0x001FF000`. Akses memory dalam instruksi yang menggunakan alamat KSEG0 mengikuti pemetaan fisik tersebut.
- File source utama tetap diperiksa pada header load base virtual `0x80010000`; pemetaan fisik tersebut hanya untuk model fungsi terisolasi, bukan deklarasi bahwa Unicorn telah memodelkan MMU/perangkat PS1 sepenuhnya.

## Test vectors

Rumus ekspektasi: `state_baru = (state_lama × 0x41C64E6D + 0x3039) mod 2^32`; `v0 = (state_baru >> 16) & 0x7FFF`.

| State awal | State baru harapan | State aktual | `v0` harapan | `v0` aktual | Instruksi | Return | Status |
|---|---|---|---|---|---:|---|---|
| `0x00000000` | `0x00003039` | `0x00003039` | `0x00000000` | `0x00000000` | 12 | PASS | PASS |
| `0x00000001` | `0x41C67EA6` | `0x41C67EA6` | `0x000041C6` | `0x000041C6` | 12 | PASS | PASS |
| `0xFFFFFFFF` | `0xBE39E1CC` | `0xBE39E1CC` | `0x00003E39` | `0x00003E39` | 12 | PASS | PASS |
| `0x12345678` | `0x0B719151` | `0x0B719151` | `0x00000B71` | `0x00000B71` | 12 | PASS | PASS |
| `0x7FFFFFFF` | `0x3E39E1CC` | `0x3E39E1CC` | `0x00003E39` | `0x00003E39` | 12 | PASS | PASS |
| `0x80000000` | `0x80003039` | `0x80003039` | `0x00000000` | `0x00000000` | 12 | PASS | PASS |
| `0xD44FAABC` | `0x75592A45` | `0x75592A45` | `0x00007559` | `0x00007559` | 12 | PASS | PASS |

Hasil pada run kedua: `ISOLATED_RNG_FUNCTION_EXECUTION=PASS`, `vectors_passed=7/7`, `STEP9_ISOLATED_RNG=PASS`; setiap vektor kembali ke sentinel dalam 12 instruksi, memperbarui state yang diuji, dan memberikan hasil `v0` yang benar.

## Batas penutupan

- Kriteria uji isolasi—memuat rentang instruksi yang terverifikasi, mencatat state input/register, memory map, state/output aktual dan harapan, return/control-flow, batas instruksi, provenance serta keterbatasan—**terpenuhi untuk fungsi RNG di executable utama saja**.
- Ini tidak membuktikan seed boot, caller/call chain, jalur resource/overlay, setiap branch dari fungsi game lain, perilaku perangkat PS1, atau kesesuaian seluruh gameplay. Kesimpulan hasil roulette/battle tidak ditarik.
- Jika fungsi lain akan diuji terisolasi, setiap fungsi harus memiliki entry/return/helper dan kebutuhan memory/register yang terpetakan sendiri; hasil fungsi RNG ini tidak dapat digeneralisasi untuk menutup tes tersebut.

