# AM2 — LCG step-count dari RNG H6

Status: TUNTAS untuk nilai yang tersedia pada AK1_REPLAY.tsv; tidak menggunakan emulator.

Input: reports/ak_2026-10-30/runs/run-41042679829/attempt-1/AK1_REPLAY.tsv, output commit sumber 493e6bf6bc4f2cc54c2221fe29a3e0d69ce70fd4, run #41042679829, job ID 124019605576. H6 SHA-256 d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475 (hybrid, bukan target murni).

RNG 0x800A3118 pada frame 1, 60, 180, 240, 360 adalah 0x06CF4B77 pada kedua attempt. Untuk setiap pasangan frame berurutan, S_after=S_before, sehingga k minimum adalah 0 (tanpa satu langkah LCG pun diperlukan). Tidak ada nilai k positif yang diklaim. Batas pencarian skrip adalah 2^24=16,777,216.

| Attempt | Frame | RNG sebelum | RNG sesudah | k minimum |
|---|---:|---|---|---:|
| 1 | 1→60 | 0x06CF4B77 | 0x06CF4B77 | 0 |
| 1 | 60→180 | 0x06CF4B77 | 0x06CF4B77 | 0 |
| 1 | 180→240 | 0x06CF4B77 | 0x06CF4B77 | 0 |
| 1 | 240→360 | 0x06CF4B77 | 0x06CF4B77 | 0 |
| 2 | 1→60 | 0x06CF4B77 | 0x06CF4B77 | 0 |
| 2 | 60→180 | 0x06CF4B77 | 0x06CF4B77 | 0 |
| 2 | 180→240 | 0x06CF4B77 | 0x06CF4B77 | 0 |
| 2 | 240→360 | 0x06CF4B77 | 0x06CF4B77 | 0 |

Formula: S'=(0x41C64E6D*S+0x3039) mod 2^32. Script SHA-256: b1e000e8d3a592018674a1b465b718754a0fca9d1aa000d086fedd97d5f7c2e6. Output TSV SHA-256: c3b0a206109f4a48d7acd750e2368185d6f89bbca1195615eefa19d8f57ddbe5.

Batas: hanya step-count aritmetika atas word RNG yang direkam. Tidak menyimpulkan kapan/kenapa game memanggil RNG atau apa arti gameplay state konstan.
