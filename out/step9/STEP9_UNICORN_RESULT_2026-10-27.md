# LIVE ADDENDUM — setter/getter CPU-isolated tests, 27 Oktober 2026 21:00 WIB

Artifact [#12740305973](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40516755810/artifacts/12740305973) was created by run [#40516755810](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40516755810). Artifact size 4,567 bytes; API digest and local SHA-256 match `bf1a702074849b2592bfc5555a0d493b5ed86d3de0b9895a192db7fdf9f80cd4`. It contains four text/log files only: the report, stage marker, probe log and disc extraction log. The report's observed result markers are `ISOLATED_RNG_FUNCTION_EXECUTION=PASS`, `ISOLATED_PLAYER_VALUE_ACCESSOR_TESTS=PASS`, `accessor_cases_passed=16/16`, `vectors_passed=7/7`, `STEP9_ALL_TESTS=PASS`, and `stage=isolated_function_pass`.

**Important metadata caveat:** when checked at 21:00 WIB, the GitHub API still reported the run and job as `queued` despite the artifact already being present and containing actual output for all tests. Therefore this report treats the test output as verified from the artifact contents but does **not** infer a run-level conclusion or claim cleanup success from the stale API status. Recheck the run/job metadata later before marking the whole Actions workflow completed. This inconsistency does not alter the test assertions visible in the artifact.

### Final workflow/cleanup status — 27 Oktober 2026, 21:02 WIB

A subsequent read of the GitHub job summary and decoded job log for [#40516755810](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40516755810), job `122232466902`, shows all 11 job steps completed with `success`, including “Remove all private runner files”. The raw job log contains `STEP9_PRIVATE_CLEANUP=PASS`. So the earlier 21:00 observation (run/job API showing queued) is stale/inconsistent; the latest API now shows the aggregate run `in_progress` while the job steps and output artifact already show completion. Cleanup is confirmed by the job log. Do not describe the aggregate run as `completed/success` until that final API field updates.

## Additional test set — player value setter/getter

Functions are executed in fresh RAM-only Unicorn instances using the verified main EXE text, 2 MiB RAM, GP from the verified header, SP `0x001FE000`, RA sentinel `0x001FF000), and a 128-instruction budget. No PS1 emulator, BIOS, game loop, gameplay input or savestate is used. The tested slot base is `0x80070EB8`, stride `0xB4`, four slots. The address/stride/field relationship comes from Ghidra/m2c cross-check of `0x8001387C` and `0x800138EC); field meaning is not independently renamed by this test.

### Setter `0x8001387C` — 10/10 assertions passed

| Case | Index (`a0`) | Input (`a1`) | Expected return `v0` | Expected slot result | Actual | Status |
|---|---:|---:|---:|---|---|---|
| Normal value | 0 | 1234 | 1 | slot 0 = 1234; other slots unchanged | Return/slots match | PASS |
| Clamp minimum | 1 | −12000 | 1 | slot 1 = −9999 | Return/slots match | PASS |
| Clamp maximum | 2 | 100000 | 1 | slot 2 = 99999 | Return/slots match | PASS |
| Minimum boundary | 3 | −9999 | 1 | slot 3 = −9999 | Return/slots match | PASS |
| Maximum boundary | 0 | 99999 | 1 | slot 0 = 99999 | Return/slots match | PASS |
| Negative boundary repeat | 1 | −9999 | 1 | slot 1 = −9999 | Return/slots match | PASS |
| Extreme positive | 2 | 2147483647 | 1 | slot 2 = 99999 | Return/slots match | PASS |
| Extreme negative | 3 | −2147483648 | 1 | slot 3 = −9999 | Return/slots match | PASS |
| Invalid index | 4 | 88 | 0 | no slots change | Return/slots match | PASS |
| Unsigned invalid index | `0xFFFFFFFF` | 88 | 0 | no slots change | Return/slots match | PASS |

### Getter `0x800138EC` — 6/6 assertions passed

| Case | Index (`a0`) | Slot contents prepared | Expected `v0` | Actual | Status |
|---|---:|---|---:|---:|---|
| Slot 0 | 0 | 1234 | 1234 | 1234 | PASS |
| Slot 1 negative | 1 | −9999 | −9999 | −9999 | PASS |
| Slot 2 maximum | 2 | 99999 | 99999 | 99999 | PASS |
| Slot 3 all-bits-one | 3 | `0xFFFFFFFF` | `0xFFFFFFFF` | `0xFFFFFFFF` | PASS |
| Invalid index | 4 | — | 0 | 0 | PASS |
| Unsigned invalid index | `0xFFFFFFFF` | — | 0 | 0 | PASS |

## Acceptance change and remaining coverage

- **VERIFIED (isolated function execution):** the seven RNG vectors remain 7/7; the setter clamps to signed bounds ([-9999,99999]), returns 1 for indices 0–3, and returns 0 without mutation for invalid indices; the getter returns the contents of the same slot for valid indices and returns 0 for invalid indices. All 16 setter/getter cases returned to the sentinel with no instruction-budget overflow and matched expected register/memory values.
- **SCOPE LIMIT:** this proves the two routines' behavior under the tested register/memory setup. It does not prove which gameplay event calls them, whether the slot is charged/refunded in a specific rule, runtime resource mapping, all caller contexts, or PS1 hardware/runtime behavior. Do not derive barrier/upgrade/turn/victory rules from this test alone.
- **Step 9(b) changes from UNKNOWN to SEBAGIAN**, because meaningful additional functions and boundary conditions now have test oracles and assertions. It is not TUNTAS: other required helper, target-compare, transition and failure paths have not been enumerated/tested completely. Step 9 overall therefore remains **SEBAGIAN**; only 9(a) (RNG routine) is TUNTAS and the new accessor subset is verified.
- The original RNG-only report below is retained as historical provenance for run #40474891838; this addendum supplements it rather than replacing its input vectors/results.

---

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

