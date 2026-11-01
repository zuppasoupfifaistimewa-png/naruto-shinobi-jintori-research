# AT1 — static audit

AT1(a): TUNTAS K4. Fourteen setter call sites were inspected; detailed 12-instruction contexts are in the AS1 deep-context AQ1 evidence. Ten calls are participant-slot paths based on EA74 with 0x90 stride; four are manager/getter paths. None of the 14 final a1 chains proves a value loaded from tile-record slot EA84 with stride 0x124. Seven census labels that classify a call as RECORD_0x8013EA84 conflict with the decoded EA74 participant path.

AT1(a) special case 0x8010A638: **s1=0x14**. Control flow at 0x8010A600 is unconditional `j 0x8010A614`; its delay slot `0x8010A604 li s1,0x14` executes. The linear `lw s1,0xB44(v0)` at 0x8010A610 is skipped on the call path. Setter delay slot `0x8010A63C addu a1,v0,s1` therefore gives final a1 = getter_return(0x8010A624) + 0x14; not manager+0xB44.

AT1(b): TUNTAS K4. At 0x80105418, delay slot sets a0=s3, the getter index. The first getter at 0x801053C4 executes move a1,a0 with delay-slot a0=s3; therefore BLTZ-taken carries a1=s3 into the second call (no intervening a1 write). Fall-through executes lw a1,-0x5AAC(v0) at 0x801053D4 from manager slot 0x8013A554; observed pointer 0x801CEF08. The second getter immediately executes move a1,a0, so either incoming a1 is overwritten before use.

AT1(c): TUNTAS K4 comparison. FIELD sets: runs 41208394883, 41211621969, 41249411706, 41249611249 = 1,188 identical rows each (946 READ, 220 WRITE, 22 OTHER); run 41213474394 = 1,163 rows, missing 25 PC rows in FUN_800db29c; run 41249242776 = 1,178 rows, missing 10 PC rows in FUN_800e0b3c. No new rows appeared. Exact cause (exporter coverage, Ghidra function boundary, or run input) TIDAK TAHU; do not blame cfff770 because older 1,188 output exists.

AT1(d): TUNTAS K4. Register is s8 (= $30; fp alias), not fp=0. Two sb writes are s8 WRITE (0 READ, 2 WRITE); fp remains 0.

Static findings max K4. No gameplay semantics or economy field meaning inferred.

## Artefak terstruktur tambahan

- `AT1_GETTER_CALLS.tsv` — dua call-site getter, 12 instruksi pre-JAL, delay slot, a0, asal a1 tiap edge dan hasil cabang. Pada getter kedua, a1=s3 pada BLTZ-taken; fall-through memuat 0x801CEF08 dari slot manager sebelum getter menimpanya.
- `AT1_SETTER_CALLS.tsv` — seluruh 14 setter call-site, basis slot/stride, final a1, 12 instruksi pre-JAL dan delay slot.
- `AT1_FIELD_DIFF_PC_FUNCTION.tsv` dan `AT1_FIELD_DIFF_SUMMARY.tsv` — rekonsiliasi 6 ekspor census.


Full accessor bodies and per-instruction bytes are in `AU1_ACCESSOR_DISASSEMBLY_2026-11-01.md`. The prior getter wording (a0=basis, a1=index) is superseded: a0 is the entry index; callee copies it into a1 and builds the record pointer in a0.
