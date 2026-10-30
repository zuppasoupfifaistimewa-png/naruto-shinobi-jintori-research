# Handoff AN1–AN3 — Naruto Jintori (30 Oktober 2026)

## Checkpoint terkini
- Game: Naruto – Shinobi no Sato no Jintori Gassen (PS1), SLPS-03553.
- Repo satu-satunya: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research.
- Laporan lengkap: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/808a3beff96e7d6fb63ef4e1ce397c63d13d1e65/reports/an_2026-10-30/AN1_AN3_FINAL_REPORT.md
- Status AN1=TUNTAS K4; AN2=TUNTAS K5; AN3=TUNTAS K5.
- Story Mode belum dinyatakan tamat.

## Run final AN2/AN3
- Actions run #41080663095; job `an2-an3-h6-isolated-mcd`; numeric job ID 124148564912.
- Source SHA: 6800d4452af6e79aae29e394e8130305448b0f12.
- Commit publikasi output: 2c047d427c555cd2cebf15404e0cbbf7885e64d7.
- Actions/job success; script exit 0; cleanup success.
- 30/30 capture PASS (6 launch × 5 frame), six emulator exits 0, no watchdog, all Circle readbacks PASS for A/B, and 600s timeout is >2× the slowest frame360 time (141.4004585743s).
- C, A, B each replayed twice. Each launch used its own copy of the same reference Memory Card (131072 bytes, baseline SHA ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5); every before/after hash stayed equal.
- Within each schedule, both launches have identical RAM SHA at frames 1,60,180,240,360.
- RNG 0x800A3118 remained 0x06CF4B77 at every one of the 30 capture points. Only snapshot stability is established, not continuous per-frame stability.
- C/A/B RAM SHA first diverges across schedules at sampled frame180; frame1 and60 match.

## Diff AN3
Counts for frames 180 / 240 / 360; attempt1 and attempt2 have identical counts:
- C vs A: 25068 / 24994 / 24756 changed bytes.
- C vs B: 2 / 6 / 5.
- A vs B: 25068 / 24992 / 24758.
- All 18 SUMMARY rows and 1588 RANGE rows reconcile; no byte-accounting mismatches. All byte changes in these comparisons are TIDAK TAHU; every mapped label count is zero.
- The results establish a repeatable RAM pattern on H6 hybrid. They do **not** explain the gameplay meaning of Circle or the unknown RAM ranges.

## H6 limitation
H6 SHA: d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475. It is target savestate base + SPU top-level field 6 from CONTROL, not a pure target-native savestate. Do not use this result as target-native proof.

## Important earlier runner correction
Run #41067396027 had no valid capture. Logs later showed a Lua runner typo: the final diagnostic line referenced unbound Lua variable `p` instead of `pressFrame`, preventing listener/frame startup; the RNG summary also had an incorrect field key. Both were repaired. Diagnostic run #41079972127 then passed one C launch (5/5 captures, emulator exit 0); the six-launch full run #41080663095 is the source of the AN2/AN3 K5 results. Do not repeat failed pre-fix runs.

## Raw evidence paths
- Main report: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/808a3beff96e7d6fb63ef4e1ce397c63d13d1e65/reports/an_2026-10-30/AN1_AN3_FINAL_REPORT.md
- Actions summary: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2c047d427c555cd2cebf15404e0cbbf7885e64d7/reports/an_2026-10-30/runs/run-41080663095/attempt-1/ACTIONS_RUN_SUMMARY.txt
- Capture TSV: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2c047d427c555cd2cebf15404e0cbbf7885e64d7/reports/an_2026-10-30/runs/run-41080663095/attempt-1/AN2_CAPTURE_SUMMARY.tsv
- Diff TSV: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2c047d427c555cd2cebf15404e0cbbf7885e64d7/reports/an_2026-10-30/runs/run-41080663095/attempt-1/AN3_DIFF_RANGES.tsv

## Next research boundary
Do not rerun AN1–AN3 unchanged. The next meaningful work is to map the currently TIDAK TAHU RAM ranges against code/data references, or design a separate target-native verification; keep conclusions about gameplay semantics at UNKNOWN until independently demonstrated. Never commit ROM, BIOS, Memory Card, savestate, raw RAM, hybrid binary, or private evidence images.
