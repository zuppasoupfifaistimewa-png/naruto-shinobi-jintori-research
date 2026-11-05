# DQ1-DQ3 — audit raw-byte statik

Snapshot HEAD main saat mulai: 2136f3df739937b87a790844bca59e8a837d3484. Baseline inklusif: 2136f3df739937b87a790844bca59e8a837d3484.
Metode: raw disc BIN/CUE -> ISO -> SLPS_035.53 dan DATA.BIN sementara pada runner; validasi SHA; parser MIPS raw little-endian membaca langsung byte EXE dan Entry 1. Ghidra export tidak dipakai sebagai sumber byte.
Biner sementara dibuang sebelum hasil teks di-commit; tidak ada artifact biner.

## Status

- DQ0: TUNTAS K4 — lihat DQ0_SUMMARY.txt dan DQ0_COMMIT_LEDGER.tsv.
- DQ1(a): TUNTAS K4 — 12 instruksi sebelum store 0x800ECBB8 dipetakan ke Entry 1 dan dibaca langsung dari byte mentah.
- DQ1(b): TUNTAS K3 — 39 store kandidat terdeteksi; recount kategori di bawah.
- DQ2: TUNTAS K4 untuk JAL langsung, pemanggil=2; manager+0x2EE akses=25; direct Chakra reads=0; Chakra-tainted subu=0.
- DQ3: BELUM K2 — raw scan belum membuktikan level saat ini vs target -> fee -> pengisian 0x80139EFC.

## DQ1(a) — instruksi sebelum store

PC 0x800ECBB8 di luar EXE. Entry 1 diverifikasi sendiri: directory index 1, LBN 8778, DATA.BIN byte offset 0x10BB000, size 596412, SHA256 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a. Kandidat base statik 0x800AD450 menghasilkan slice offset 0x3f768. Runtime mapping tetap NOT VALIDATED.
Rincian 12 baris PC/word/mnemonik/hex dan window 48 byte ada di DQ1A_PRESTORE_12_RAW.tsv; instruksi store target serta offset diverifikasi di DQ1A_MAPPING_CHECK.txt.

## DQ1(b) — census writer global 0x80139EFC

Recount TSV: total=39, DARI_TILE_1A=0, COMPUTED=20, CLEAR=7, LAIN=12.
DARI_TILE_1A = register sumber terakhir berasal dari lhu offset 0x1A; COMPUTED = operasi aritmetika/logika ditandai di aliran register; CLEAR = zero; LAIN = asal tidak terbukti. Ini klasifikasi aliran register, bukan interpretasi gameplay.
Scope aligned word pada pemetaan EXE dan Entry 1. Function labels adalah nearest JAL/prologue heuristic kecuali FUN_800ec574 diketahui dari target langsung. Indirect/dynamic alias dan code/data separation belum tuntas; nol temuan tidak membuktikan nol writer.
Setiap konteks 12 instruksi mempunyai excerpt hex 48 byte (maksimum 64 byte).

## DQ2 — helper, +0x2EE, indeks, Chakra

JAL target 0x800EC574 dihitung dari encoding word; hasil pemanggil langsung=2. Kolom opcode_guess_match menguji dugaan 0x0C03B15D.
Manager +0x2EE: 25 akses. Hanya MANAGER_ALIAS_CONFIRMED yang membuktikan base dari load global 0x80139EFC; BASE_UNPROVEN tetap kandidat. JALR/tidak langsung tidak lengkap.
Chakra: 0 load langsung ke field record+0x18 pada slot 0..3; 0 subu memiliki operand dengan taint Chakra. Data-flow linear tidak menangkap seluruh indeks dinamis atau aliran lintas fungsi, jadi daftar bukan bukti semua pengurangan Chakra.
Index×2: sll dengan shift=1 di dalam window helper tercantum di DQ2_INDEX_TIMES_TWO_RAW.tsv; skala 2-byte terindikasi, sumber idx belum tentu terbukti.
Setiap PC yang basis manager tidak terikat dilabel BASE_UNPROVEN; cakupan pengurangan Chakra yang tidak ter-taint = TIDAK TAHU.

## DQ3 — jalur fee level d>=2

Status BELUM K2. Tidak ada data-flow raw yang menyambungkan perbandingan level saat ini vs target, operasi fee, dan penulisan global 0x80139EFC. Konteks store kandidat di DQ3_GLOBAL_FILL_PRECONTEXT_RAW.tsv tidak cukup menyimpulkan rumus.

Observasi pengguna (hipotesis, X=120, fee dasar 100):

| Transisi | d | Observasi | fee*2^d | Hasil |
|---|---:|---:|---:|---|
| LV1->LV2 | 1 | 100 | 200 | TIDAK COCOK |
| LV1->LV3 | 2 | 400 | 400 | COCOK |
| LV1->LV4 | 3 | 800 | 800 | COCOK |
| LV1->LV5 | 4 | 1600 | 1600 | COCOK |

H1: fee akhir = fee dasar × 2^d untuk semua d; 3/4 titik cocok, titik LV1->LV2 memfalsifikasi bentuk universal.
H2: d=1 mendapat pengecualian biaya dasar; d>=2 memakai fee × 2^d. Keempat titik pengguna cocok, tetapi H2 hanya hipotesis dari pengamatan pengguna.
Falsifier H2: observasi terkontrol X lain dengan d=1 bukan fee dasar atau d>=2 menyimpang; secara statik, cabang tanpa penyesuaian pada d=1/d>=2 yang memakai operasi sama juga memfalsifikasi H2.
Tidak dilakukan fitting dengan kurang dari tiga titik; ada empat titik hipotesis, tetapi bukan bukti kode.

## Batasan

Audit statik; tidak ada emulator, BIOS, savestate, atau upload raw input. Entry1 static base belum divalidasi runtime.
Commit pembuat pipeline mengubah: .github/workflows/dq1-dq3-raw-static.yml; tools/stage1/RunDQ1DQ3Raw.py.
