# KA0-KA5 static audit

Baseline inklusif: 656503e9e21cb4baf3185969abf7b15d05a149c6
Source SHA: 207408634a7a67e7777b03a8e18bab1bee7749e5
EXE SHA-256: a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569
Entry 1 SHA-256: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a
Runtime: EMULATOR_LAUNCHES=0.

## Status
- KA0=SEBAGIAN K3 (ledger/compile snapshot; run snapshot status finalized externally)
- KA1=SEBAGIAN K3/K4 (byte/code evidence; wallet setter TIDAK TAHU)
- KA2=SEBAGIAN K3 (three x writer chains; global dynamic writers and reachable x subset TIDAK TAHU)
- KA3=SEBAGIAN K3 (caller census; B24C8 boundary may remain TIDAK TAHU)
- KA4=TUNTAS K4 (EMULATOR_LAUNCHES=0)
- KA5=SEBAGIAN K2 (conditional H(x), no numeric cost formula)

## Findings
- KA1: direct call/reference candidates to FUN_800B50AC are in KA1_B50AC_CALLERS.tsv; argument origin slices at the three requested call PCs are in KA1_CALL_ARGUMENT_ORIGINS.tsv. Wallet-authoritative setter remains TIDAK TAHU.
- KA2: direct constant effective-address stores to globals 0x80139EC7, 0x8013EA6E and 0x8013EB1C are enumerated in KA2_GLOBAL_WRITERS.tsv. Indirect/dynamic bases remain TIDAK TAHU. Three manager+0x530 source chains have byte-limited conditional domain 0..255; no proof that x is delta d or that x<52.
- KA3: all Ghidra/direct references found for FUN_800BE5D8 are in KA3_BE5D8_CALLERS.tsv. B24C8 inferred function and $v0 origin are in KA3_B24C8_FUNCTION_V0_CONTEXT.tsv; missing ranges remain TIDAK TAHU.
- KA4: static-only; no emulator launch.
- KA5: only conditional H(x) expression for x in 0..51; out-of-range behavior unknown. No use of 400/800/1600, no fitting, no MATCH/CONTRADICTS labels.

## TIDAK TAHU
- Wallet-authoritative setter and exact semantics of participant record +0x04.
- Complete caller set for B50AC if indirect dispatch or Ghidra references are unresolved.
- Dynamic/indirect writers to the three global addresses and upstream origins of unresolved bases.
- Full reachable values for x and whether x represents d or effect/item/action selector.
- Whether x is guarded to 0..51 before H table lookup and out-of-range behavior.
- B24C8's parent function/callers/$v0 base/index if Ghidra fails to establish a function boundary.
- Any numeric upgrade cost for level jumps d>=2.

## Files
All instruction evidence TSV excerpts include image, PC, file offset, bytes and decoded instruction. Any single excerpt must remain <=64 contiguous bytes. Runtime was not used.
