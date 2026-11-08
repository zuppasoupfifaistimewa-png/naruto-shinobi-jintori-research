# PA5 correction addendum — manual reconciliation of committed PA4 TSVs

Baseline inklusif: 3f730c73dc628d02f360b7ac12961e6f3e4b1584
PA4 source run: 42482696764
PA4 publish commit: f30d12e49995d050555f71d2ed5bc85dc2a76b2b
PA5 workflow run: 42482696764
PA5 original report commit: 00a6b15294812f1f176bfa3d94910f859767b63e

## Correction of the PA5 parser result

The original PA5 report states `MISSING_SCALARS` for all six expected addresses. That is a parser/check-out timing error, not missing PA4 data.

PA5 job checked out `main` at 2026-11-08T13:01:20Z, when HEAD was `f30d12e49995d050555f71d2ed5bc85dc2a76b2b`. The address-prefix parser fix `2c6fd1e7b51274945ed9cf2ec8dd465743225df4` appeared on origin/main during the job's later publication rebase (13:01:50Z), after the script had already run. The checked-out version uppercased the whole address, turning `0x...` into `0X...` while the expected scalar keys use lowercase `0x`.

The later prefix fix canonicalizes keys as `"0x" + digits.upper()`. However, its scalar-output loop still uses `s1[addr.upper()]` and `s2[addr.upper()]`, which again changes `0x` to `0X`. A future code rerun must index by canonical `addr` instead. This addendum does **not** claim the PA5 Python script ran successfully.

## Direct reconciliation from committed PA4 TSVs

The two committed scalar TSVs each contain the six expected addresses, with identical decimal values. Both committed M-region TSVs contain exactly 1,344 rows (0x540 bytes), consecutive addresses from 0x801EFBB8 through 0x801F00F7, and identical address/value rows.

| Scalar | RAM address | Launch 1 | Launch 2 | Width |
|---|---:|---:|---:|---:|
| M | 0x8013EA74 | 2149514168 (0x801EFBB8) | 2149514168 (0x801EFBB8) | 4 |
| I | 0x8013EA6E | 0 | 0 | 2 |
| B | 0x8013EB1C | 0 | 0 | 1 |
| EA88 selector | 0x8013EA88 | 5 | 5 | 2 |
| 39EFC selector | 0x80139EFC | 0 | 0 | 2 |
| GP+0x118 | 0x8006D794 | 52 | 52 | 4 |

M-region SHA-256 launch 1 and launch 2:
`a6b6b518d8b4eff42275f2dd574a78f5741870fc33cebacc79e27a4602d281a7` (both).

Manual TSV reconciliation: **TUNTAS K4** for exact schema, key-set, scalar equality, M-region length/address continuity and full row equality. The underlying two-launch CONTROL repeatability remains **TUNTAS K5**. This correction is a deterministic re-read of committed text TSVs; it is not a new emulator run.

## Interpretation boundary

A repeated checkpoint is one CONTROL state replayed twice. It does not encode an independent tile-jump distance `d` or a semantic effect-ID mapping. Therefore:
- H1 `x=d`: **BELUM K1 / TIDAK TAHU**. No paired, known-`d` transaction was observed.
- H2 `x=effect ID`: **BELUM K1 / TIDAK TAHU**. No semantic mapping from selector to effect ID was established.
- Upgrade cost for jump `d>=2`: **BELUM K1 / TIDAK TAHU**. No charge/debit relation is proven.
- No 400/800/1600 inputs and no fitting were used.

The original PA5 report is retained unchanged to preserve the actual run output; this file and PA5_CONTROL_MANUAL_RECONCILIATION.tsv provide the corrected manual reading.
