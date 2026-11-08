# PA0-PA5 — audit statis dan satu tahap CONTROL runtime

Baseline inklusif: 3f730c73dc628d02f360b7ac12961e6f3e4b1584
Source SHA: ea559aea2c772c97f5a6e027ec1f8db966be945a
EXE SHA-256: a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569
Entry 1 SHA-256: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a

## Ringkasan status
- PA0: SEBAGIAN K1 — self-test PASS; validasi raw/offset/decode=3156/3156 (fail=2987); excerpt strip=FAIL, aggregate max=68B, pelanggaran=3, py_compile=72.
- PA1: SEBAGIAN K2 — tiga callsite dan seluruh edge statis yang dapat dipulihkan dicatat; klasifikasi a2/a3, consumer base table dan indirect dispatch tetap dibatasi oleh CFG/alias closure.
- PA2: SEBAGIAN K2 — read selector, pointer M references, 144*I pattern, global stores dan call/branch paths dicensus; writer/loader M+0x10+B+144*I tidak dianggap tertutup tanpa proof chain.
- PA3: SEBAGIAN K2 — B24C8 direct CFG reachability serta 12 target-register chains dicatat; table/global indirect targets tetap TIDAK TAHU bila pointer content dinamis.
- PA4: ditangani job runtime independen; lihat PA4_RUNTIME_SUMMARY.txt dan TSV angka desimal yang dipublikasikan job PA4.
- PA5: BELUM K1 — x=d dan formula biaya lompat d>=2 TIDAK TAHU; nilai 400/800/1600 tidak dipakai.

## Excerpt audit
Deleted rows: 1; lihat PA0_DELETED_ROWS.tsv. Sisa asal kelompok: PA0_OVERLIMIT_ORIGINS.tsv.
Aggregate max contiguous span=68 B; over-limit groups=3; STATUS=FAIL.
New TSV validations=3156; decoded instructions=169; failures=2987.

## Ledger pre-publication
Commits from baseline inclusive excluding publication=18; human=11; bot=7.
Runs created after baseline=6; see PA0_TRIGGERED_RUNS_AFTER_BASELINE.tsv.

## Scope
Static analysis only for PA0-PA3. Runtime is limited to two identical HA4 checkpoint restores. No game input, no watchpoints, no cold boot fallback. No ROM/BIOS/savestate/RAM binary committed.

## Job and publication details
JOB=pa0-pa3-pa5-static
SOURCE_SHA=ea559aea2c772c97f5a6e027ec1f8db966be945a
PA0_SELFTEST=PASS
PY_COMPILE=72/72
ANALYZER_EXIT_CODE=1

## Static task scope
PA1: callsite a2/a3, incoming edges, scene-base consumers and scene-chain.
PA2: s0 origin, M pointer, 144-byte row candidates, selector writers incl. E3B1C, v0 store paths, gp+0x118 v1 source.
PA3: B24C8 direct CFG reachability and twelve unresolved JALR target chains.
PA5 symbolic result is provisional; final H1/H2 falsifier review is in the PA5 dependent job.

## Commit file list
See PA0_PUBLISH_COMMIT_FILES.tsv and PA0_COMMIT_LEDGER.tsv.
