# Topik 1 — Langkah 4: RNG + roulette (27 Oktober 2026)

**Status langkah: SEBAGIAN.** Inventaris RNG statis yang terdahulu dipakai kembali; ini bukan penutupan ulang Langkah 4 secara absolut dan bukan bukti roulette memakai RNG tertentu.

## Kriteria Langkah 4

| Kriteria | Status | Bukti / celah |
|---|---|---|
| (a) Generator, jenis, state RAM, sumber seed | SEBAGIAN | Kode LCG dan state terpetakan statis. Seed awal/runtime belum terbukti; kandidat setter 0x80035DA8 punya bukti call site di resource pada base analisis hipotetis. |
| (b) Determinisme: savestate sama + jeda sama/berbeda | BELUM DILAKUKAN | Tidak ada uji emulator/savestate pada putaran ini. Tidak bisa menyatakan perilaku deterministik aktual saat game berjalan. |
| (c) Pemanggil statis + pointer/dispatch yang dicurigai | SEBAGIAN | Caller langsung terdaftar dari main EXE dan kandidat DATA.BIN; sebagian candidate belum divalidasi oleh boundary Ghidra. Base resource masih hipotesis. |
| (d) Caller roulette dan battle terverifikasi dinamis | BELUM DILAKUKAN | Tidak ada fungsi yang dapat disebut pemanggil roulette/battle berdasarkan bukti runtime saat ini. |
| (e) RNG ganda serta randomness non-fungsi | SEBAGIAN | Scan konstanta LCG yang dikenal menemukan satu kecocokan di main EXE. Ini tidak menyingkirkan generator dengan rumus lain, tabel, penghitung frame, atau kode terkompresi/terdekripsi. |

## Temuan kode

**MUNGKIN — generator statis:** rutin RNG 0x80035D78 membaca/memperbarui state global 0x800A3118:

state_baru = (state_lama × 0x41C64E6D + 0x3039) mod 2^32

Nilai hasil: (state_baru >> 16) & 0x7FFF.

Tidak diberi keyakinan **PASTI**, karena kriteria keyakinan PASTI memerlukan verifikasi perilaku, sementara tes dinamis belum dilakukan.

**Peta caller yang saat ini tercatat:**
- Main EXE: 4 direct-JAL callers tervalidasi Ghidra pada 0x80015B14, 0x80015BF0, 0x8001A460, 0x80020C24.
- DATA.BIN entry 0, base hipotetis 0x800AD000: Ghidra memvalidasi 2 caller RNG; dua kandidat JAL lain belum tervalidasi sebagai decoded direct-flow oleh Ghidra. Ada kandidat pemanggilan setter seed di 0x800AF2AC menuju 0x80035DA8, tetapi base/lifecycle runtime belum dikonfirmasi.
- DATA.BIN entry 1, base hipotetis 0x800D0000: 108 caller direct-flow tervalidasi Ghidra; 36 kandidat raw-JAL masih belum dipetakan ke boundary fungsi Ghidra. Base/lifecycle runtime belum dikonfirmasi.

**Batas interpretasi caller:** fungsi main EXE yang sudah didekompilasi menunjukkan operasi indeks/offset acak, shuffle byte, pemilihan dari daftar kandidat yang difilter, dan inisialisasi struktur berisi nilai pseudo-acak. Belum ada bukti yang menghubungkan salah satunya secara pasti dengan roulette atau battle. Jangan mengubah nama fungsi atau memberi label mekanik gameplay hanya dari bentuk operasi.

## Bukti permanen yang mendasari

- [Penutupan inventaris statis Langkah 4](../../docs/STEP4_CLOSURE_2026-10-27.md)
- [Trace RNG dan alamat caller](../../docs/STEP4_RNG_TRACE_2026-10-27.md)
- [Perbandingan Ghidra/m2c empat caller main EXE](STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md)
- [Caller Ghidra DATA.BIN entry 1](../rng_resource_entry1_ghidra_callers_2026-10-27.md)
- [Konteks 36 kandidat entry 1 tanpa boundary fungsi](../rng_resource_entry1_unmapped_context_2026-10-27.md)
- [Konteks Ghidra DATA.BIN entry 0 dan kandidat seed setter](../rng_resource_entry0_ghidra_context_2026-10-27.md)
- [Scan signature LCG lintas berkas](../step4_rng_signature_scan_2026-10-27.md)
- [Versi dan verifikasi toolchain](../versions.txt)

## Dampak status SEBAGIAN

Rumus LCG didukung kode statis, tetapi belum boleh diklaim sebagai RNG roulette. Hasil determinisme, caller runtime roulette/battle, seed runtime, pemanggil tak langsung, serta RNG alternatif/non-fungsi tetap UNKNOWN. Karena kriteria sendiri membatasi langkah tanpa emulator menjadi paling tinggi SEBAGIAN, status TUNTAS tidak berlaku.

## Langkah berikutnya

Pada Langkah 5 untuk topik ini, telusuri candidate/helper/table dan xref pemanggil untuk menguji apakah ada jalur kode yang benar-benar terhubung ke roulette. Bandingkan keluaran Ghidra dan m2c untuk setiap fungsi yang dapat didukung bukti. Jangan menamai fungsi sebagai roulette sebelum jalurnya terbukti; tidak menjalankan pemain adaptif.
