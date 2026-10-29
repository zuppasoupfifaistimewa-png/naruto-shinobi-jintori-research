# V1 reconciliation — evidence chain

## (a) Run 40792708405 metadata
- Workflow: 'Preserve Naruto checkpoint and compare RAM / strict A2'
- Workflow file: '.github/workflows/preserve-checkpoint-and-compare.yml'
- Branch: 'main'
- head_sha: '4c505394ac331225545728261c66566fa3113763'
- Run: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40792708405
- Head commit permalink: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/4c505394ac331225545728261c66566fa3113763
- Follow-on sanitized report commit: 'b26455720d19b6e78ada49bfe0698d1a289bc91a'. The same workflow log shows '4c50539..b264557 HEAD -> main' after the step 'Commit only sanitized text, JSON and CSV reports'. These SHAs identify different stages, not conflicting identities.
- Follow-on commit permalink: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/b26455720d19b6e78ada49bfe0698d1a289bc91a

## (b) Release record, target commit, publication and asset attribution
          - Release API: created_at=2026-10-29T00:14:06Z, published_at=00:14:27Z, release ID 427327611, asset ID 686794219 created at 00:14:28Z.
          - Tag refs directly to commit 4c505394ac331225545728261c66566fa3113763; target commit author/committer date is 00:14:06Z, equal to API created_at. Do not treat this equality as a Release-record creation-event timestamp. Who first created the Release record: TIDAK TAHU.
          - Both run 40789851317 step 4 (00:14:17–00:14:44Z) and run 40792708405 step 5 (00:14:26–00:14:31Z) overlap published_at and asset_created_at. Timestamp overlap alone is not unique attribution.
          - The overlapping 40789851317 step is named 'Download release disc image and extract SLPS_035.53' and that workflow uses contents:read; run 40792708405 step 5 is explicitly 'Preserve raw savestate as a non-expiring GitHub Release asset' and that workflow has contents:write. Evidence supports run 40792708405 as publisher and checkpoint-asset uploader, but does not identify the initial creator of the Release record or the author of the tag target commit.
          - Release API: https://api.github.com/repos/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tags/naruto-checkpoint-39262213468
          - Release URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/naruto-checkpoint-39262213468

## (c) 'extended scan 32' vs '191 all appear'
- '326' is the expanded-scan candidate count. Its 'effective_address_if_pair' field has 294 candidates with heuristic same-register LUI-pair effective address '0x8013A554' and 32 candidates marked 'UNRESOLVED' because no same-register LUI was found within the fixed 32-word backward window.
- In the 191-row comparison against the strict scan, every row occurs in the expanded candidate file ('extended_scan_326_candidate=YES'). This is candidate-site membership, not 191 independently proved effective addresses.
- Exactly 32 of those 191 rows are READ/LW rows categorized as lacking a same-register 'lui 0x8014' within the 32-word window; these correspond to the 32 unresolved effective-address rows in the expanded candidate table. '32' is a row/site count; the window itself is 32 instruction words.
- Scan run: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40789339014
- Scan commit permalink: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/8b70e004f0df21bbb250a3c0b918a19e76ce0a21
- Reconciliation commit permalink: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/4c505394ac331225545728261c66566fa3113763

Caveat: LUI pairing is a linear local heuristic, not proof of CFG dominance, aliasing, or runtime access. V3 therefore uses a separate in-function backtrace.
