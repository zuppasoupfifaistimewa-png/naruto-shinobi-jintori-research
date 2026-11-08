# PA0-PA5 static result

PA static analyzer did not produce a complete report.

## Job and publication details
JOB=pa0-pa3-pa5-static
SOURCE_SHA=9c55c9ded9663b0acb8bb7c0439585db94aaa6bb
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
