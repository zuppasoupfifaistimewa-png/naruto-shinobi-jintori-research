# AT1 — static audit

AT1(a): TUNTAS K4. Fourteen setter call sites were inspected; detailed 12-instruction contexts are in the AS1 deep-context AQ1 evidence. Ten calls are participant-slot paths based on EA74 with 0x90 stride; four are manager/getter paths. None of the 14 final a1 chains proves a value loaded from tile-record slot EA84 with stride 0x124. Seven census labels that classify a call as RECORD_0x8013EA84 conflict with the decoded EA74 participant path.

AT1(a) special case 0x8010A638: s1 is 0x14 on the path through 0x8010A604 (li s1,0x14), or manager+0xB44 on the path through 0x8010A610 (lw s1,0xB44(v0)). The setter delay slot adds that s1 to getter return v0.

AT1(b): TUNTAS K4. Both getter sites are in FUN_801052E8. At 0x801053C4, delay slot sets a0=s3; return v0 is tested by bltz, with taken edge entering li s0,0x20. At 0x80105418, delay slot sets a0=s3; on fall-through from the first branch sequence, a1 remains the manager pointer loaded by lw a1,-0x5AAC(v0) at 0x801053D4 (historically observed as 0x801CEF08). On bltz-taken edge, a1 origin is TIDAK TAHU because the preceding helper call may clobber caller-saved a1. The second getter return v0 is passed as a2 to 0x8001B364.

AT1(c): TUNTAS K4 comparison. FIELD sets: runs 41208394883, 41211621969, 41249411706, 41249611249 = 1,188 identical rows each (946 READ, 220 WRITE, 22 OTHER); run 41213474394 = 1,163 rows, missing 25 PC rows in FUN_800db29c; run 41249242776 = 1,178 rows, missing 10 PC rows in FUN_800e0b3c. No new rows appeared. Exact cause (exporter coverage, Ghidra function boundary, or run input) TIDAK TAHU; do not blame cfff770 because older 1,188 output exists.

AT1(d): TUNTAS K4. Register is s8 (= $30; fp alias), not fp=0. Two sb writes are s8 WRITE (0 READ, 2 WRITE); fp remains 0.

Static findings max K4. No gameplay semantics or economy field meaning inferred.

## Artefak terstruktur tambahan

- `AT1_GETTER_CALLS.tsv` — dua call-site getter, 12 instruksi pre-JAL, delay slot, a0, asal a1 pada jalur teramati, cabang return v0, serta batas caller-saved. Pada bltz-taken menuju getter kedua, a1 tetap TIDAK TAHU.
- `AT1_SETTER_CALLS.tsv` — seluruh 14 setter call-site, basis slot/stride, final a1, 12 instruksi pre-JAL dan delay slot.
- `AT1_FIELD_DIFF_PC_FUNCTION.tsv` dan `AT1_FIELD_DIFF_SUMMARY.tsv` — rekonsiliasi 6 ekspor census.
