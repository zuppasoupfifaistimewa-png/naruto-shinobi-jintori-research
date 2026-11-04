# CG0–CG3 Audit — Naruto Jintori (SLPS-03553)
Tanggal: 4 November 2026
Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`
Main awal: `b841ece9a121c48cc30a14be87813af0ff2b6fa7`
Ledger cutoff (inklusif): `0afef96546fc892bfd8923891a0a664ac19f7dff`
Rentang compare: 17 commit ahead, 0 behind.

## Ringkasan status

| Butir | Status | K | Putusan |
|---|---|---:|---|
| CG0 — ledger commit + blob SHA | TUNTAS | K4 | 17 commit baru; 13 manusia, 4 bot; 157 entri file pada commit, 151 path unik, seluruh hash blob cocok dengan objek Git. |
| CG1 — raw scan EA8, writer/reader, FUN_80102408 | SEBAGIAN | K4 | 4 store EA8 dan 1 reader di Entry 1; tidak ada store EA8 di EXE. Semua store memakai global pointer slot 0x8013A22C; nilai store pertama belum diketahui semantik gameplay-nya. |
| CG2(a) — D9570 event 3, jalur D15A8 dan action==3 | SEBAGIAN | K3–K4 | Byte action 3 di-set pada D9570; parent memanggil D15A8 lebih dulu. Cabang spesifik action==3 di D15A8: TIDAK TAHU. |
| CG2(b) — penulis non-loader +0x1A sebagai fee sebelum D15A8 | BELUM | K2 | Ada kandidat writer +0x1A, tetapi belum ada alias pointer yang membuktikan tile EA84+0x1A atau pending-fee. |
| CG2(c) — HJ1′, HJ2, HJ3, HJ4 dan falsifier | SEBAGIAN | K1 | Empat model dan falsifier ditulis. Belum ada pengukuran pembeda d≥2 yang sah. Pengamatan pengguna saja K1. |
| CG3 — H6, read-only, watchpoint | SEBAGIAN | K5 terbatas | Empat launch pada dua Actions run mengulang enam sampel/frame dengan pointer dan EA8 sama; driver false-negative `0X` vs `0x`; total 0 hit, sehingga PC/old/new writer tetap TIDAK TAHU. |

## CG0 — ledger semua commit baru

Metode: compare objek Git dari `b841ece9a121c48cc30a14be87813af0ff2b6fa7` sampai `0afef96546fc892bfd8923891a0a664ac19f7dff` inklusif. Untuk setiap commit, author type diambil dari metadata author; daftar file dan blob SHA-1 diambil dari `files[]` pada objek commit. Compare mengembalikan 151 path unik; penjumlahan `files[]` per commit menghasilkan 157 entri perubahan. SHA blob tiap entri dicocokkan ulang dengan API objek commit.

Statistik: **17 commit; 13 manusia; 4 bot; 157 entri file; 151 path unik.**

### 1. 2b5326e9d744544a85b76e4429d905525b778675 — MANUSIA
Author: zuppasoupfifaistimewa-png <zuppasoupfifaistimewa@gmail.com>; Add raw MIPS offset candidate scanner
- `tools/step7/ScanRawMipsOffsets.py` — added; Git blob SHA-1 `235d8109d1b67087d0e7e4dcec1e91c72c867876`

### 2. d5420993701c0c636317a4d550aa993fbd094749 — MANUSIA
Author: zuppasoupfifaistimewa-png <zuppasoupfifaistimewa@gmail.com>; Add decoded EA8 and tile fee field audit
- `tools/step7/ExportOffsetMemoryAudit.java` — added; Git blob SHA-1 `ce04105a7c4f6804f28abf708a27050faccb04f4`

### 3. 27a716552d7638feedc09fb103c6f3545431765e — MANUSIA
Author: zuppasoupfifaistimewa-png <zuppasoupfifaistimewa@gmail.com>; Wire raw EA8 and tile-fee offset audits into Step 7
- `.github/workflows/step7-entry1-buffer-base-audit.yml` — modified; Git blob SHA-1 `e296060d3a42f347d586804cc4a62ceae4d98473`

### 4. 8f95b519258eb7bd7fc26624eee8d228b22eef46 — BOT
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>; Publish AQ1 static economy census run 41768087823
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ACTIONS_RUN_SUMMARY.txt` — added; Git blob SHA-1 `2169a2ce2ff87693c5763111fcffaee8eb4a0efc`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/BA1_DATA_BIN_RESOURCE_INVENTORY.tsv` — added; Git blob SHA-1 `9cbdde9fb4603a73572223e652dd05c33edf062c`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/BA1_DATA_SCAN_SUMMARY.txt` — added; Git blob SHA-1 `22902582de6508501314592e06ea7715fd3cd027`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/BA1_RESOURCE_CANDIDATES.tsv` — added; Git blob SHA-1 `ade9a31a5634ed6c79835bf2bd1da126f1c81950`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/BA1_TILE_TABLE_CANDIDATES.tsv` — added; Git blob SHA-1 `ea637569bf5a406915a127b492a654cec2ef988c`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/BA1_TILE_TABLE_RECORDS.tsv` — added; Git blob SHA-1 `076c6cbeea4430227e141ca02e3fbe15bc1ec582`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/BA1_TILE_TABLE_SCAN_SUMMARY.txt` — added; Git blob SHA-1 `06cba738f6ab1478aa1e0b63ddd2ed680fe13d10`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/BB2_FULL_DATABIN_TEXT_SCAN.txt` — added; Git blob SHA-1 `a4b4f10ab9c8ef4039ea29e2d91c7c6092800a6f`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/aq1-deep-context.tsv` — added; Git blob SHA-1 `491fcf2a27fd90d0bb30679d5d0563fe7d6ea483`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/aq1-economy-census.tsv` — added; Git blob SHA-1 `fc530a02596010b54f2b7f3faef951b2765b41a7`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/aq1-recount.txt` — added; Git blob SHA-1 `63624ec5a3fee54eceb765a94a52be79dc549899`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/aw1-helper-call-windows.tsv` — added; Git blob SHA-1 `d74a01e2883fac6006bb20972899792a5963ba54`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/aw1-manager-b38-accesses.tsv` — added; Git blob SHA-1 `1dcf4d0a10efb73ec7c65b185cc274c33d94c35f`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/aw1-manager-b40-accesses.tsv` — added; Git blob SHA-1 `94f77ecd1d51383fca275c351c805bdd9ebf767a`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/aw1-manager-b44-accesses.tsv` — added; Git blob SHA-1 `3243e54bf6e82304bd931322c13d7b05b0b684f0`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/aw1-manager-function-detail.txt` — added; Git blob SHA-1 `1033d0bd7244faf6fe1cb06a0ed3ef931941d015`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/aw1-manager-status.txt` — added; Git blob SHA-1 `9695c0c2b99ba93db09e06cb60ff819e912f9079`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/aw1-tile-field-function-inventory.tsv` — added; Git blob SHA-1 `b4a64d0bb14512bd43dd56eac89ee4720359ac54`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/aw2-numeric-instruction-literals.tsv` — added; Git blob SHA-1 `e4ab7da02d5ce578ba202b2425f12c8ae136f61e`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/aw2-numeric-occurrences.tsv` — added; Git blob SHA-1 `87a1b1b7129a815a6fb0b946453282ea12ceb5de`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/aw2-static-data-scan.md` — added; Git blob SHA-1 `96123fde6fc67ed8c21e3a057455065f7ea1a527`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ay1-ay2-entry1.tsv` — added; Git blob SHA-1 `da7a7bd8f67e644461f8add9f5e7795d7c9ef1b9`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ay1-ay2-exe.tsv` — added; Git blob SHA-1 `f816bddc073d66eda0abbd630433eeb8cd19e539`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ay1-ay2-sha256.txt` — added; Git blob SHA-1 `2e55f1f99f4ce967becb1f203f04565277d74e54`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ay2-exe-random-byte-check.txt` — added; Git blob SHA-1 `edadca7cdcb5c8a3853f1bb929ccd20b6e7ccdfe`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/az3-main-exe-economic-helper-detail.txt` — added; Git blob SHA-1 `eefda3f4f0bd71a78e3d9ee4715ff171d1ee0543`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/az3-resource-economy-function-detail.txt` — added; Git blob SHA-1 `b7684b2dc43ce402432e29e03f9de55681b76c69`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/az3-setter-call-windows-entry1.tsv` — added; Git blob SHA-1 `4d6e7a1723c748ef79af2f78bfc132698789cbb3`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/az3-setter-call-windows-main-exe.tsv` — added; Git blob SHA-1 `85bbf542dfd9920ca2b8a7a13d78d1650dc299ae`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/az3-setter-caller-main-exe-detail.txt` — added; Git blob SHA-1 `35a20f7f527f2f4c0a09d14792653029adcf508e`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/az3-setter-direct-callers-entry1.txt` — added; Git blob SHA-1 `fdf8e77b8a18496bc1941c9485cbe336f0eb131e`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/az3-setter-direct-callers-main-exe.txt` — added; Git blob SHA-1 `3660c5ca674a886c431020dc55b6d7b314a5fb0a`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/az3-starting-balance-global-detail.txt` — added; Git blob SHA-1 `c18c94ca43cad2aabbf3efd0bcb5e4a23919e72b`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ba1-mode-state-resource-selector.tsv` — added; Git blob SHA-1 `1cd785d19eb7eab9bb28491921bad8784bf4f737`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ba1-resource-parser-main-exe.txt` — added; Git blob SHA-1 `0e8e2643afc4e06a5095cb004b60fb1064f42780`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ba1-selector-callers-main-exe.txt` — added; Git blob SHA-1 `e77a468bf9124add2bfae4e5be523db7d7f43885`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ba1-selector-dat80070cd0-xrefs.csv` — added; Git blob SHA-1 `f51aedb7eb69a0ddccf10023367c2d17b7e52ac2`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ba1-selector-main-exe-functions.csv` — added; Git blob SHA-1 `0062409de2e499202a1dccebec07f6b72bc5c95f`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ba1-tile-loader-callers.txt` — added; Git blob SHA-1 `18fb1c41e3f00dcff2804d3563bc2118971210d5`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ba1-tile-resource-loader.txt` — added; Git blob SHA-1 `50013b6b4a923899b9c767c4cb9b9282a2e360a5`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-action-byte-access.tsv` — added; Git blob SHA-1 `8df6f29db6b76aad2370d75ad605c2be0006bd7f`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-d15a8-direct-callers.txt` — added; Git blob SHA-1 `68ed31f405af536e7dd0de8a369e3eb6db464ce1`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-d15a8-focused.txt` — added; Git blob SHA-1 `f317948c8871cd04941f7fdfe3d9c03d6c3bfef4`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-d15a8-function-detail.txt` — added; Git blob SHA-1 `ee64767f0fbd67c200acb565222b139c517d3ef1`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-entry1-numeric-literals.tsv` — added; Git blob SHA-1 `e4ab7da02d5ce578ba202b2425f12c8ae136f61e`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-event-direct-callers.txt` — added; Git blob SHA-1 `8336db9271609aeee81b7c302b1fe38eba1956ef`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-event-function-detail.txt` — added; Git blob SHA-1 `f8c889cc81e48e27bec511e4f655890e40c4767c`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-event-instruction-windows.txt` — added; Git blob SHA-1 `a81b97254aea7d8346efd027b0a00a20b91cdf34`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-full-databin-text-scan.tsv` — added; Git blob SHA-1 `feb671ef2da60c86c584161d482fd76385e32ed6`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-message-object-functions.csv` — added; Git blob SHA-1 `b0b1a289a8f164e72897a674665c440c4f1b05ba`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-message-object-xrefs.csv` — added; Git blob SHA-1 `3cb1b80cacaf689123cd1f594b26b37838d487fc`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/bb2-tile-nibble-access.tsv` — added; Git blob SHA-1 `43eaa7bb5e22ad8e9923f29247f6736c989669be`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/cd1-raw-indirect-call-candidates.txt` — added; Git blob SHA-1 `ba25ed850e6077fd172d1c86718cd5ba1a7a0a7e`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/cg_raw_mips_offset_candidates.tsv` — added; Git blob SHA-1 `e4604a17ad4b1d8c0fa758f27e39d4f6bea515a4`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/cg_raw_mips_offset_scan_summary.txt` — added; Git blob SHA-1 `745fbf7e3630f8feac4d4ad23f5d515d7fb4b174`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ea8-entry1-offset-audit.tsv` — added; Git blob SHA-1 `f4b3c773536862495c7ede0ec0e2caba57394267`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/ea8-exe-offset-audit.tsv` — added; Git blob SHA-1 `de5a06fbc868b5f756b7fcc9016d60a7207c2461`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/entry1-buffer-base-targets.txt` — added; Git blob SHA-1 `ffbaa5628426fc647ceeb06790ead104e2c53040`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/entry1-helper-function-detail.txt` — added; Git blob SHA-1 `28c64af1772e46da2de3d2db93654926de3c092a`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/helper-a1-provenance-status.txt` — added; Git blob SHA-1 `0397600152c96a8ca43dc07478bd8c3f72fcc9f4`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/input-identity.txt` — added; Git blob SHA-1 `24bb56ab3a94ef9761265d7353ba44391541110e`
- `reports/stage1_economy/aq1-run-41768087823/attempt-1/run-summary.txt` — added; Git blob SHA-1 `ac579e5ed81b9bb374deee7e64f8b252824a64a5`

### 5. 4045f5f6825e5bab9e8c4ddba375a54df674095d — MANUSIA
Author: zuppasoupfifaistimewa-png <zuppasoupfifaistimewa@gmail.com>; Add read-only two-launch H6 write-watchpoint probe
- `experiments/cg3_h6_readonly_watchpoint.py` — added; Git blob SHA-1 `6146cfd3a38c9a81d5c178db7db2c599ff10737b`

### 6. 0ad31c376c8c49f3f8c2ae03cd3b32d797dbc6fb — MANUSIA
Author: zuppasoupfifaistimewa-png <zuppasoupfifaistimewa@gmail.com>; Add two-launch H6 read-only PCSX watchpoint workflow
- `.github/workflows/cg3-h6-readonly-watchpoint.yml` — added; Git blob SHA-1 `20e6e7ccf0a8eea977bd21e9590e48b926f98bd0`

### 7. 773fef1a34643ebb34f832346dd9fb0ca14f98d2 — MANUSIA
Author: zuppasoupfifaistimewa-png <zuppasoupfifaistimewa@gmail.com>; Export full CG1 EA8 writers and CG2 tile fee candidate functions
- `.github/workflows/step7-entry1-buffer-base-audit.yml` — modified; Git blob SHA-1 `1b10ab3f5691b5ba55f2a673e54e8ca8cddd384b`

### 8. 7b6800c8a3d9d515910038b35f314bc65d4fc045 — BOT
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>; Publish AQ1 static economy census run 41769361956
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ACTIONS_RUN_SUMMARY.txt` — added; Git blob SHA-1 `240aa061d4b736d64bd682b7f6f8b5f73c5da2a0`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/BA1_DATA_BIN_RESOURCE_INVENTORY.tsv` — added; Git blob SHA-1 `9cbdde9fb4603a73572223e652dd05c33edf062c`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/BA1_DATA_SCAN_SUMMARY.txt` — added; Git blob SHA-1 `22902582de6508501314592e06ea7715fd3cd027`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/BA1_RESOURCE_CANDIDATES.tsv` — added; Git blob SHA-1 `ade9a31a5634ed6c79835bf2bd1da126f1c81950`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/BA1_TILE_TABLE_CANDIDATES.tsv` — added; Git blob SHA-1 `ea637569bf5a406915a127b492a654cec2ef988c`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/BA1_TILE_TABLE_RECORDS.tsv` — added; Git blob SHA-1 `076c6cbeea4430227e141ca02e3fbe15bc1ec582`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/BA1_TILE_TABLE_SCAN_SUMMARY.txt` — added; Git blob SHA-1 `06cba738f6ab1478aa1e0b63ddd2ed680fe13d10`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/BB2_FULL_DATABIN_TEXT_SCAN.txt` — added; Git blob SHA-1 `a4b4f10ab9c8ef4039ea29e2d91c7c6092800a6f`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/aq1-deep-context.tsv` — added; Git blob SHA-1 `491fcf2a27fd90d0bb30679d5d0563fe7d6ea483`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/aq1-economy-census.tsv` — added; Git blob SHA-1 `fc530a02596010b54f2b7f3faef951b2765b41a7`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/aq1-recount.txt` — added; Git blob SHA-1 `63624ec5a3fee54eceb765a94a52be79dc549899`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/aw1-helper-call-windows.tsv` — added; Git blob SHA-1 `d74a01e2883fac6006bb20972899792a5963ba54`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/aw1-manager-b38-accesses.tsv` — added; Git blob SHA-1 `1dcf4d0a10efb73ec7c65b185cc274c33d94c35f`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/aw1-manager-b40-accesses.tsv` — added; Git blob SHA-1 `94f77ecd1d51383fca275c351c805bdd9ebf767a`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/aw1-manager-b44-accesses.tsv` — added; Git blob SHA-1 `3243e54bf6e82304bd931322c13d7b05b0b684f0`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/aw1-manager-function-detail.txt` — added; Git blob SHA-1 `765fab85f55f18e2e09ab3c53723e328006a6b8e`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/aw1-manager-status.txt` — added; Git blob SHA-1 `9695c0c2b99ba93db09e06cb60ff819e912f9079`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/aw1-tile-field-function-inventory.tsv` — added; Git blob SHA-1 `b4a64d0bb14512bd43dd56eac89ee4720359ac54`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/aw2-numeric-instruction-literals.tsv` — added; Git blob SHA-1 `0f2ce98aafa1e6f099d6e7badeeb8b0197f4c2ca`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/aw2-numeric-occurrences.tsv` — added; Git blob SHA-1 `87a1b1b7129a815a6fb0b946453282ea12ceb5de`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/aw2-static-data-scan.md` — added; Git blob SHA-1 `96123fde6fc67ed8c21e3a057455065f7ea1a527`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ay1-ay2-entry1.tsv` — added; Git blob SHA-1 `da7a7bd8f67e644461f8add9f5e7795d7c9ef1b9`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ay1-ay2-exe.tsv` — added; Git blob SHA-1 `f816bddc073d66eda0abbd630433eeb8cd19e539`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ay1-ay2-sha256.txt` — added; Git blob SHA-1 `92d616d6a74597e622eefda8809660d08fb4b9ea`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ay2-exe-random-byte-check.txt` — added; Git blob SHA-1 `edadca7cdcb5c8a3853f1bb929ccd20b6e7ccdfe`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/az3-main-exe-economic-helper-detail.txt` — added; Git blob SHA-1 `288d32a051bcbd48b3c304a930d33d32335e9155`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/az3-resource-economy-function-detail.txt` — added; Git blob SHA-1 `d9bc6dcedeeba84662a975be9923686da08393d2`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/az3-setter-call-windows-entry1.tsv` — added; Git blob SHA-1 `4d6e7a1723c748ef79af2f78bfc132698789cbb3`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/az3-setter-call-windows-main-exe.tsv` — added; Git blob SHA-1 `85bbf542dfd9920ca2b8a7a13d78d1650dc299ae`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/az3-setter-caller-main-exe-detail.txt` — added; Git blob SHA-1 `35a20f7f527f2f4c0a09d14792653029adcf508e`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/az3-setter-direct-callers-entry1.txt` — added; Git blob SHA-1 `fdf8e77b8a18496bc1941c9485cbe336f0eb131e`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/az3-setter-direct-callers-main-exe.txt` — added; Git blob SHA-1 `3660c5ca674a886c431020dc55b6d7b314a5fb0a`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/az3-starting-balance-global-detail.txt` — added; Git blob SHA-1 `c18c94ca43cad2aabbf3efd0bcb5e4a23919e72b`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ba1-mode-state-resource-selector.tsv` — added; Git blob SHA-1 `1cd785d19eb7eab9bb28491921bad8784bf4f737`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ba1-resource-parser-main-exe.txt` — added; Git blob SHA-1 `9396b941651f5e273aa3aec5e9a6a0b67d0ba1f7`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ba1-selector-callers-main-exe.txt` — added; Git blob SHA-1 `e77a468bf9124add2bfae4e5be523db7d7f43885`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ba1-selector-dat80070cd0-xrefs.csv` — added; Git blob SHA-1 `f51aedb7eb69a0ddccf10023367c2d17b7e52ac2`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ba1-selector-main-exe-functions.csv` — added; Git blob SHA-1 `0062409de2e499202a1dccebec07f6b72bc5c95f`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ba1-tile-loader-callers.txt` — added; Git blob SHA-1 `b09b3874b9b26aa91f7b2630068dd1a56be71353`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ba1-tile-resource-loader.txt` — added; Git blob SHA-1 `50013b6b4a923899b9c767c4cb9b9282a2e360a5`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-action-byte-access.tsv` — added; Git blob SHA-1 `8df6f29db6b76aad2370d75ad605c2be0006bd7f`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-d15a8-direct-callers.txt` — added; Git blob SHA-1 `f34442a8afa42835294fb94baa5101e00cd35934`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-d15a8-focused.txt` — added; Git blob SHA-1 `374248651a8e4fe8b8675d04563afcc0101003ac`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-d15a8-function-detail.txt` — added; Git blob SHA-1 `2be85719c6bd308ce23ce6f9d8854567a887b0c8`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-entry1-numeric-literals.tsv` — added; Git blob SHA-1 `0f2ce98aafa1e6f099d6e7badeeb8b0197f4c2ca`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-event-direct-callers.txt` — added; Git blob SHA-1 `df7c47a895a304ecbb6621933b65325d13e24233`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-event-function-detail.txt` — added; Git blob SHA-1 `da88c7b00abcb254cad3a95103a65e7bb5513f55`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-event-instruction-windows.txt` — added; Git blob SHA-1 `a81b97254aea7d8346efd027b0a00a20b91cdf34`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-full-databin-text-scan.tsv` — added; Git blob SHA-1 `feb671ef2da60c86c584161d482fd76385e32ed6`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-message-object-functions.csv` — added; Git blob SHA-1 `ea127d8d33b4fef60b3ecd8e8f312d6080c7bb81`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-message-object-xrefs.csv` — added; Git blob SHA-1 `3cb1b80cacaf689123cd1f594b26b37838d487fc`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-tile-nibble-access.tsv` — added; Git blob SHA-1 `43eaa7bb5e22ad8e9923f29247f6736c989669be`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/cd1-raw-indirect-call-candidates.txt` — added; Git blob SHA-1 `ba25ed850e6077fd172d1c86718cd5ba1a7a0a7e`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/cg1-ea8-writer-function-detail.txt` — added; Git blob SHA-1 `ede68b72ffe2e3d8989cb0a207b0f25355850bd1`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/cg2-tile-fee-writer-function-detail.txt` — added; Git blob SHA-1 `10c4af5c0decb2a072897906b819daca026fa36e`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/cg_raw_mips_offset_candidates.tsv` — added; Git blob SHA-1 `e4604a17ad4b1d8c0fa758f27e39d4f6bea515a4`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/cg_raw_mips_offset_scan_summary.txt` — added; Git blob SHA-1 `745fbf7e3630f8feac4d4ad23f5d515d7fb4b174`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ea8-entry1-offset-audit.tsv` — added; Git blob SHA-1 `f4b3c773536862495c7ede0ec0e2caba57394267`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ea8-exe-offset-audit.tsv` — added; Git blob SHA-1 `de5a06fbc868b5f756b7fcc9016d60a7207c2461`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/entry1-buffer-base-targets.txt` — added; Git blob SHA-1 `a47f2a082b43b7dabe6e7abe59177618e0228548`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/entry1-helper-function-detail.txt` — added; Git blob SHA-1 `db52487aaccd73cc8873349afa33bdea51eebb28`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/helper-a1-provenance-status.txt` — added; Git blob SHA-1 `0397600152c96a8ca43dc07478bd8c3f72fcc9f4`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/input-identity.txt` — added; Git blob SHA-1 `24bb56ab3a94ef9761265d7353ba44391541110e`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/run-summary.txt` — added; Git blob SHA-1 `b7ac622fd7446a6e01348fdc60a7a457c20a25ac`

### 9. 9f2bd9a98c722b57979c62b7ce031d467f6370c4 — MANUSIA
Author: zuppasoupfifaistimewa-png <zuppasoupfifaistimewa@gmail.com>; Fix CG3 report commit cwd and preserve raw driver errors
- `.github/workflows/cg3-h6-readonly-watchpoint.yml` — modified; Git blob SHA-1 `73850e325d8c02e8f5a00f0de73ac6d81bfa61b8`

### 10. 0d26b2f0fe668ef83847c5d9082f7fa2c8ba21fe — MANUSIA
Author: zuppasoupfifaistimewa-png <zuppasoupfifaistimewa@gmail.com>; Fix CG3 report publication from checkout working directory
- `.github/workflows/cg3-h6-readonly-watchpoint.yml` — modified; Git blob SHA-1 `0f1d62f0f3b42a736de416fc2bc41460b2e9cbe4`

### 11. 6fd71b25b8a7e5f1695dd6fd32e5f993958b59f1 — MANUSIA
Author: zuppasoupfifaistimewa-png <zuppasoupfifaistimewa@gmail.com>; Allow CG3 report commit in container checkout
- `.github/workflows/cg3-h6-readonly-watchpoint.yml` — modified; Git blob SHA-1 `df5a0d487e6f37c5e32d20042967ef947b0d1db0`

### 12. f1ee369f670e39a67ab89c22b51da881e5cc9258 — MANUSIA
Author: zuppasoupfifaistimewa-png <zuppasoupfifaistimewa@gmail.com>; Allow CG3 report commit from trusted checkout
- `.github/workflows/cg3-h6-readonly-watchpoint.yml` — modified; Git blob SHA-1 `382fd21cb172fde3f7921dc72f273e0a0f0bb423`

### 13. c7cd70313663c0d5a48adec499fad9d3266d7f36 — MANUSIA
Author: zuppasoupfifaistimewa-png <zuppasoupfifaistimewa@gmail.com>; Record CG3 H6 two-launch run summary 41773084992
- `reports/stage1_economy/cg3-h6-readonly-run-41773084992/attempt-1/ACTIONS_RUN_SUMMARY.txt` — added; Git blob SHA-1 `903e819f5a02c4a68a3dc1002f5c4b7b17a099d5`

### 14. 89b3a74d53fafdabb0f17c82560d62e6cb22fa38 — MANUSIA
Author: zuppasoupfifaistimewa-png <zuppasoupfifaistimewa@gmail.com>; Add CG0-CG3 audit report for raw EA8 writers and H6
- `reports/stage1_economy/CG0_CG1_CG2_CG3_AUDIT_2026-11-04.md` — added; Git blob SHA-1 `657a79d07113901288100e736bf147711c23d57c`

### 15. 7b62ad0c9d48f7ef5fbc41f54e6c058c028daa06 — BOT
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>; Publish CG3 H6 read-only watchpoint run 41775137231
- `reports/stage1_economy/cg3-h6-readonly-run-41775137231/attempt-1/ACTIONS_RUN_SUMMARY.txt` — added; Git blob SHA-1 `4c74dc0e7bff92856332e0367036c46664b03708`
- `reports/stage1_economy/cg3-h6-readonly-run-41775137231/attempt-1/CG3_H6_FRAME_VALUES.tsv` — added; Git blob SHA-1 `f48102c27955c296c28a4831644f475b07c92f89`
- `reports/stage1_economy/cg3-h6-readonly-run-41775137231/attempt-1/CG3_H6_READONLY_SUMMARY.txt` — added; Git blob SHA-1 `b45b25d7b846c0840468fdea5fd9838133d7b950`
- `reports/stage1_economy/cg3-h6-readonly-run-41775137231/attempt-1/CG3_H6_WRITE_WATCHPOINT.tsv` — added; Git blob SHA-1 `ad82d6b78188d87c5ed6c8d04e43fc26d1f1ce87`
- `reports/stage1_economy/cg3-h6-readonly-run-41775137231/attempt-1/CG3_LAUNCH_1_RAW_LOG.txt` — added; Git blob SHA-1 `af5ff956b54473f23576679650cdd8d3bd035338`
- `reports/stage1_economy/cg3-h6-readonly-run-41775137231/attempt-1/CG3_LAUNCH_2_RAW_LOG.txt` — added; Git blob SHA-1 `c1a97fe373633fefd3c5635ccb05f258057a630a`
- `reports/stage1_economy/cg3-h6-readonly-run-41775137231/attempt-1/CG3_PCSX_MANIFEST.txt` — added; Git blob SHA-1 `be07dcbcd9c9e0a7ddc26d859ad0240c48554511`
- `reports/stage1_economy/cg3-h6-readonly-run-41775137231/attempt-1/CG3_PYTHON_DRIVER_RAW.txt` — added; Git blob SHA-1 `b45b25d7b846c0840468fdea5fd9838133d7b950`
- `reports/stage1_economy/cg3-h6-readonly-run-41775137231/attempt-1/CG3_SCRIPT_EXIT_CODE.txt` — added; Git blob SHA-1 `8642dfc899bcd0f5584d0a2eca9b65efb7e8798f`

### 16. b238dd63cd2a790b09331f0ca8c726ee734e5c16 — MANUSIA
Author: zuppasoupfifaistimewa-png; Update CG0 ledger and correct CG3 H6 runtime audit
- `reports/stage1_economy/CG0_CG1_CG2_CG3_AUDIT_2026-11-04.md` — modified; Git blob SHA-1 `9f2bc0f9451b618fba7cbce667eb927bb9add9b7`

### 17. 0afef96546fc892bfd8923891a0a664ac19f7dff — BOT
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>; Publish CG3 H6 read-only watchpoint run 41775298933
- `reports/stage1_economy/cg3-h6-readonly-run-41775298933/attempt-1/ACTIONS_RUN_SUMMARY.txt` — added; Git blob SHA-1 `ccb11718c44ac33952107ba7ed2e6580baa3aef9`
- `reports/stage1_economy/cg3-h6-readonly-run-41775298933/attempt-1/CG3_H6_FRAME_VALUES.tsv` — added; Git blob SHA-1 `f48102c27955c296c28a4831644f475b07c92f89`
- `reports/stage1_economy/cg3-h6-readonly-run-41775298933/attempt-1/CG3_H6_READONLY_SUMMARY.txt` — added; Git blob SHA-1 `32cdf681c6f828e7ab6a023bcbb1041bbae99ae5`
- `reports/stage1_economy/cg3-h6-readonly-run-41775298933/attempt-1/CG3_H6_WRITE_WATCHPOINT.tsv` — added; Git blob SHA-1 `ad82d6b78188d87c5ed6c8d04e43fc26d1f1ce87`
- `reports/stage1_economy/cg3-h6-readonly-run-41775298933/attempt-1/CG3_LAUNCH_1_RAW_LOG.txt` — added; Git blob SHA-1 `622da081cbb7638bd3797687a67a68856a54d085`
- `reports/stage1_economy/cg3-h6-readonly-run-41775298933/attempt-1/CG3_LAUNCH_2_RAW_LOG.txt` — added; Git blob SHA-1 `9a2ab4147cdecb9cc45fbd73b2cc9565de0150b5`
- `reports/stage1_economy/cg3-h6-readonly-run-41775298933/attempt-1/CG3_PCSX_MANIFEST.txt` — added; Git blob SHA-1 `be07dcbcd9c9e0a7ddc26d859ad0240c48554511`
- `reports/stage1_economy/cg3-h6-readonly-run-41775298933/attempt-1/CG3_PYTHON_DRIVER_RAW.txt` — added; Git blob SHA-1 `32cdf681c6f828e7ab6a023bcbb1041bbae99ae5`
- `reports/stage1_economy/cg3-h6-readonly-run-41775298933/attempt-1/CG3_SCRIPT_EXIT_CODE.txt` — added; Git blob SHA-1 `8642dfc899bcd0f5584d0a2eca9b65efb7e8798f`

## CG1 — scan byte mentah dan audit EA8

### Input scan dan jumlah kandidat

```text
RAW_MIPS_OFFSET_SCAN=PASS
EXE_BYTES=385024
EXE_SHA256=a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569
ENTRY1_BYTES=596412
ENTRY1_SHA256=9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a
EXE_MAP=raw file offset 0x800 -> PC 0x80010000; text length 0x5D800
ENTRY1_MAP=raw byte 0 -> candidate PC 0x800AD450; runtime mapping tidak divalidasi independen
TOTAL_CANDIDATES=187
ENTRY1 EA8 reader=1, store=4
ENTRY1 +0x1A read=32, store=87
EXE +0x1A read=20, store=43
EXE EA8 store=0, EA8 read=0
```

Scanner mencari instruksi MIPS little-endian ter-alignment dengan immediate tepat `0x0EA8` atau `0x001A` dan opcode memory. Kandidat raw tidak otomatis kode aktif atau alias pointer; fungsi dan asal register diperiksa lagi pada listing Entry 1. Mapping Entry 1 ke PC `0x800AD450` tetap kandidat, belum divalidasi runtime.

### Identitas pointer dan alamat field

Global pointer slot: `0x8013A22C`.
Objek target yang diminta: `0x801CDF80`.
Alamat field hasil penjumlahan: `0x801CDF80 + 0xEA8 = 0x801CEE28`.

Raw Entry 1 memperlihatkan 4 store `sw` immediate `0x0EA8`, satu reader `lw`. Pada empat penulis, basis store diperoleh dari load global slot `0x8013A22C`; pada dua fungsi, pembentukan alamat slot diperlihatkan eksplisit melalui `lui 0x8014` dan displacement `-0x5DD4`. Ini membuktikan jalur statis ke pointer global, bukan bahwa nilai global saat runtime selalu `0x801CDF80`.

### Empat writer EA8

**1. PC `0x80102300`, `FUN_80101fe8`**

Instruksi store dan asal basis:
```text
801022F4 14 80 02 3C  lui v0,0x8014
801022F8 2C A2 42 8C  lw v0,-0x5dd4(v0)  ; baca slot 0x8013A22C
801022FC 00 00 00 00  nop
80102300 A8 0E 43 AC  sw v1,0xea8(v0)
```
12 instruksi pra-store (alamat, bytes, mnemonic):
```text
801022D0 20 00 42 30  andi v0,v0,0x20
801022D4 23 00 40 10  beq v0,zero,0x80102364
801022D8 40 10 03 00  sll v0,v1,0x1
801022DC 21 10 43 00  addu v0,v0,v1
801022E0 80 10 02 00  sll v0,v0,0x2
801022E4 21 10 22 02  addu v0,s1,v0
801022E8 78 00 42 8C  lw v0,0x78(v0)
801022EC 00 00 00 00  nop
801022F0 10 00 40 10  beq v0,zero,0x80102334
801022F4 14 80 02 3C  lui v0,0x8014
801022F8 2C A2 42 8C  lw v0,-0x5dd4(v0)
801022FC 00 00 00 00  nop
```
Asal nilai `v1`: jalur fungsi sebelumnya memuat field word pada `0x801022C4: lw v1,0x14c(v0)`; register itu dipertahankan sampai store. Objek sumber dan makna gameplay field `+0x14C`: **TIDAK TAHU**.
Raw excerpt 52 byte:
`20 00 42 30 23 00 40 10 40 10 03 00 21 10 43 00 80 10 02 00 21 10 22 02 78 00 42 8C 00 00 00 00 10 00 40 10 14 80 02 3C 2C A2 42 8C 00 00 00 00 A8 0E 43 AC`.

**2. PC `0x80102380`, `FUN_80101fe8`**

```text
80102374 14 80 02 3C  lui v0,0x8014
80102378 2C A2 43 8C  lw v1,-0x5dd4(v0)  ; pointer global
8010237C FF FF 02 24  li v0,-1
80102380 A8 0E 62 AC  sw v0,0xea8(v1)
```
12 instruksi pra-store:
```text
80102350 01 00 04 24  li a0,0x1
80102354 1A 61 00 0C  jal 0x80018468
80102358 B4 00 05 24  li a1,0xb4
8010235C F9 08 04 08  j 0x801023e4
80102360 21 10 00 00  clear v0
80102364 24 00 A2 8F  lw v0,0x24(sp)
80102368 00 00 00 00  nop
8010236C 40 00 42 30  andi v0,v0,0x40
80102370 19 00 40 10  beq v0,zero,0x801023d8
80102374 14 80 02 3C  lui v0,0x8014
80102378 2C A2 43 8C  lw v1,-0x5dd4(v0)
8010237C FF FF 02 24  li v0,-1
```
Asal nilai akhir: konstanta sentinel `0xFFFFFFFF` (-1). Raw excerpt 52 byte:
`01 00 04 24 1A 61 00 0C B4 00 05 24 F9 08 04 08 21 10 00 00 24 00 A2 8F 00 00 00 00 40 00 42 30 19 00 40 10 14 80 02 3C 2C A2 43 8C FF FF 02 24 A8 0E 62 AC`.

**3. PC `0x801025E4`, `FUN_80102510`**

```text
8010257C 14 80 10 3C  lui s0,0x8014
801025DC 2C A2 03 8E  lw v1,-0x5dd4(s0)  ; pointer global
801025E0 FE FF 02 24  li v0,-2
801025E4 A8 0E 62 AC  sw v0,0xea8(v1)
```
12 instruksi pra-store:
```text
801025B4 9C 01 82 AC  sw v0,0x19c(a0)
801025B8 21 10 80 00  move v0,a0
801025BC A0 01 40 AC  sw zero,0x1a0(v0)
801025C0 70 00 40 AC  sw zero,0x70(v0)
801025C4 21 20 66 00  addu a0,v1,a2
801025C8 21 30 40 00  move a2,v0
801025CC 10 00 C5 84  lh a1,0x10(a2)
801025D0 12 00 C6 84  lh a2,0x12(a2)
801025D4 57 84 00 0C  jal 0x8002115c
801025D8 18 00 84 24  addiu a0,a0,0x18
801025DC 2C A2 03 8E  lw v1,-0x5dd4(s0)
801025E0 FE FF 02 24  li v0,-2
```
Asal nilai akhir: sentinel `0xFFFFFFFE` (-2). Raw excerpt 52 byte:
`9C 01 82 AC 21 10 80 00 A0 01 40 AC 70 00 40 AC 21 20 66 00 21 30 40 00 10 00 C5 84 12 00 C6 84 57 84 00 0C 18 00 84 24 2C A2 03 8E FE FF 02 24 A8 0E 62 AC`.

**4. PC `0x80102838`, `FUN_80102738`**

```text
801027AC 14 80 12 3C  lui s2,0x8014
80102830 2C A2 43 8E  lw v1,-0x5dd4(s2)  ; pointer global
80102834 FE FF 02 24  li v0,-2
80102838 A8 0E 62 AC  sw v0,0xea8(v1)
```
12 instruksi pra-store:
```text
80102808 60 01 05 24  li a1,0x160
8010280C 2C A2 42 8E  lw v0,-0x5dd4(s2)
80102810 00 00 00 00  nop
80102814 21 88 22 02  addu s1,s1,v0
80102818 21 10 50 00  addu v0,v0,s0
8010281C 10 00 24 26  addiu a0,s1,0x10
80102820 10 00 45 84  lh a1,0x10(v0)
80102824 12 00 46 84  lh a2,0x12(v0)
80102828 A3 84 00 0C  jal 0x8002128c
8010282C 06 00 07 24  li a3,0x6
80102830 2C A2 43 8E  lw v1,-0x5dd4(s2)
80102834 FE FF 02 24  li v0,-2
```
Asal nilai akhir: sentinel `0xFFFFFFFE` (-2). Raw excerpt 52 byte:
`60 01 05 24 2C A2 42 8E 00 00 00 00 21 88 22 02 21 10 50 00 10 00 24 26 10 00 45 84 12 00 46 84 A3 84 00 0C 06 00 07 24 2C A2 43 8E FE FF 02 24 A8 0E 62 AC`.

### Reader `FUN_80102408` — tepat 12 instruksi

PC `0x80102424` melakukan `lw v0,0xEA8(v1)`. Basis `v1` berasal dari global pointer slot `0x8013A22C`. Jalur lebih dulu memeriksa `pointer+4`; bila nol fungsi kembali dengan -1 (delay-slot); selain itu membaca EA8.

```text
80102408 14 80 02 3C  lui v0,0x8014
8010240C 2C A2 43 8C  lw v1,-0x5dd4(v0)
80102410 00 00 00 00  nop
80102414 04 00 62 8C  lw v0,0x4(v1)
80102418 00 00 00 00  nop
8010241C 04 00 40 10  beq v0,zero,0x80102430
80102420 00 00 00 00  nop
80102424 A8 0E 62 8C  lw v0,0xea8(v1)
80102428 08 00 E0 03  jr ra
8010242C 00 00 00 00  nop
80102430 08 00 E0 03  jr ra
80102434 FF FF 02 24  li v0,-1
```
Raw reader excerpt: `14 80 02 3C 2C A2 43 8C 00 00 00 00 04 00 62 8C 00 00 00 00 04 00 40 10 00 00 00 00 A8 0E 62 8C`.

Putusan CG1: raw scan dan instruksi di atas mengonfirmasi struktur store/read EA8 pada Entry 1 secara statis (K4). Identitas nilai dinamis yang ditulis PC 80102300, kapan masing-masing cabang mengeksekusi store, dan isi pointer saat gameplay: **TIDAK TAHU**. Empat store yang terlihat di raw text Entry 1 bukan bukti tidak adanya indirect/dynamic writers lain yang tak termuat di potongan image/code yang dipetakan.

## CG2 — event 3, action byte, dan penulis fee

### CG2(a) `FUN_800D9570` pada `0x800DAA88`

12 instruksi sekitar store (address + byte mentah + disassembly):
```text
800DAA7C 14 80 02 3C  lui v0,0x8014
800DAA80 74 EA 43 8C  lw v1,-0x158c(v0)
800DAA84 03 00 02 24  li v0,0x3
800DAA88 EB 02 62 A0  sb v0,0x2eb(v1)
800DAA8C 14 80 05 3C  lui a1,0x8014
800DAA90 74 EA A4 8C  lw a0,-0x158c(a1)
800DAA94 00 00 00 00  nop
800DAA98 E9 02 83 90  lbu v1,0x2e9(a0)
800DAA9C 09 00 02 24  li v0,0x9
800DAAA0 F7 01 62 14  bne v1,v0,0x800DB280
800DAAA4 0F 00 02 24  li v0,0xf
800DAAA8 EB 02 82 A0  sb v0,0x2eb(a0)
```
Store di PC `0x800DAA88` menulis konstanta 3 ke manager object `+0x2EB`. Sebelumnya, PC `0x800DAA30` memuat 2, PC `0x800DAA34` membaca `+0x2EB`, lalu PC `0x800DAA3C` branch jika nilainya bukan 2 ke `0x800DAA6C`. Jadi potongan ini menunjukkan transisi dari kondisi manager action==2 ke store action=3; label gameplay/event 3 masih perlu bukti lain.

Direct-call sequence pada parent `FUN_800F3658`:
```text
800F5DAC 6A 45 03 0C  jal 0x800D15A8
800F5DFC 4C 62 03 0C  jal 0x800D8930
800F5E1C 5C 65 03 0C  jal 0x800D9570
```
Urutan statisnya: D15A8 → D8930 → D9570. Ini adalah urutan call dalam satu caller; bukan bukti bahwa D15A8 mendapat parameter action=3 dari D9570 (D9570 dipanggil sesudahnya).

Di D15A8, PC `0x800D3E50` membaca `+0x2EB`, PC `0x800D3E54` memuat 8, PC `0x800D3E58` branch bila bukan 8. Tabel access action-byte juga memuat beberapa pembacaan lain dengan tes value 7, 0xF, 0x54, 0x51/0x52 dan sebagainya. Dalam bukti yang diekspor ini **tidak ada branch eksplisit action==3 yang dapat dipastikan**. Action==3 branch path di D15A8: **TIDAK TAHU**.

### CG2(b) +0x1A: kandidat writer bukan bukti fee

Raw scan mencatat 87 store Entry 1 dan 43 store EXE untuk displacement immediate +0x1A. Banyak adalah stack-local; daftar ini tidak boleh ditafsirkan seluruhnya sebagai writer tile. Hanya instruksi berikut yang layak dicatat sebagai kandidat base selain `sp`:

| PC | Fungsi | Instruksi | Apa yang diketahui | Status |
|---|---|---|---|---|
| 0x800B331C | FUN_800b2a58 | `sh t1,0x1a(v1)` | Base dihitung dari `DAT_8013EAB0 + index*0x24`; store value t1 tidak terurai pada 12 instruksi sebelumnya | alias tile/fee tidak terbukti |
| 0x800B396C | FUN_800b2a58 | `sb v0,0x1a(v1)` | Base dari `DAT_8013EA74 + index`, stride 0x24 | alias tile/fee tidak terbukti |
| 0x800B589C | FUN_800b5790 | `sb v0,0x1a(v1)` | pola base `DAT_8013EA74 + index`, stride 0x24 | alias tile/fee tidak terbukti |
| 0x800B5E2C | FUN_800b5d68 | `sb v0,0x1a(v1)` | pola base `DAT_8013EA74 + index`, stride 0x24 | alias tile/fee tidak terbukti |
| 0x800B65CC | FUN_800b63f4 | `sh t1,0x1a(v1)` | Base dihitung dari `DAT_8013EAB0 + index*0x24` | alias tile/fee tidak terbukti |
| 0x800BB338 | FUN_800bb284 | `sh v1,0x1a(v0)` | Base `DAT_8013EAB0 + index*0x24`; value `0x20 - lbu(-0x6414(a3))` | base berbeda dari EA84/0x124 |
| 0x800F6DA4 | FUN_800f6988 | `sh v0,0x1a(a0)` | Value hasil signed average/2 dari word `*(v1)`; base `a0` tidak teralias | kandidat generic struct update; tile/fee tak terbukti |
| 0x800F7D9C, 0x800F7DB0 | FUN_800f7adc | `sh v1,0x1a(a0)` | Mengurai dua byte berurutan dari `s1` menjadi u16 dan menulis ke +0x1A; base `a0` belum teralias | pola parser/loader, bukan kandidat non-loader yang terverifikasi |
| 0x80120F18, 0x80120FC0 | FUN_80120c94 / FUN_80120f44 | `sh v0,0x1a(v1)` | Base belum terurai | alias tile/fee tidak terbukti |
| 0x801218FC, 0x80125EE8, 0x80127548, 0x8012A3E0, 0x80130A90, 0x801323AC, 0x80137910 | beragam | store +0x1A | base berasal dari register/objek/stack lain; tidak terhubung statis ke EA84 atau pending debit | alias tile/fee tidak terbukti |

Candidate detail utama:
```text
800BB30C 14 80 02 3C  lui v0,0x8014
800BB310 B0 EA 45 8C  lw a1,-0x1550(v0)
800BB314 14 80 07 3C  lui a3,0x8014
800BB318 20 00 06 24  li a2,0x20
800BB31C C0 10 04 00  sll v0,a0,0x3
800BB320 21 10 44 00  addu v0,v0,a0
800BB324 80 10 02 00  sll v0,v0,0x2
800BB328 21 10 A2 00  addu v0,a1,v0
800BB32C EC 9B E3 90  lbu v1,-0x6414(a3)
800BB330 00 00 00 00  nop
800BB334 23 18 C3 00  subu v1,a2,v1
800BB338 1A 00 43 A4  sh v1,0x1a(v0)
```
Raw excerpt 52 byte:
`21 20 00 00 14 80 02 3C B0 EA 45 8C 14 80 07 3C 20 00 06 24 C0 10 04 00 21 10 44 00 80 10 02 00 21 10 A2 00 EC 9B E3 90 00 00 00 00 23 18 C3 00 1A 00 43 A4`.
Bukti ini menunjuk ke tabel base `DAT_8013EAB0` stride 0x24, bukan struktur tile `DAT_8013EA84` stride 0x124. Fungsi `FUN_800f7adc` memuat data byte berurutan dan menulis 16-bit ke +0x1A, sehingga pola lebih mirip deserialisasi; tidak memenuhi kriteria non-loader yang diminta.

Kesimpulan: **TIDAK TAHU** writer non-loader yang benar-benar menuliskan fee tile EA84+0x1A sebelum D15A8. Tidak ada bukti statis yang menghubungkan kandidat di atas ke tile base atau pending fee, dan tidak ada bukti urutan waktu sebelum D15A8 untuk kandidat tersebut.

### CG2(c) hipotesis biaya lompat d≥2 dan falsifier

Semua model berikut HIPOTESIS K1. B adalah biaya satu langkah pada kondisi yang sama.

| Model | Prediksi | Falsifier |
|---|---|---|
| HJ1′ eksponensial | d=1: B; d≥2: B×2^d (d=2 → 4B; d=3 → 8B) | Pengukuran saldo/pending dengan kondisi sama menunjukkan d=2 bukan 4B atau d=3 bukan 8B. |
| HJ2 linear | biaya(d)=B×d (d=2 → 2B; d=3 → 3B) | Pengukuran setara menunjukkan d=2 bukan 2B atau d=3 bukan 3B. |
| HJ3 lookup | biaya dipilih dari tabel/tier berdasarkan tujuan, jarak, tile type atau atribut lain | Buktikan operand fee dihitung langsung sebagai B×2^d atau B×d pada beberapa nilai d, tanpa lookup; HJ3 gugur. |
| HJ4 upstream/pending | fee dihitung lebih awal, lalu ditulis ke tile+0x1A atau field pending sebelum D15A8 membacanya | Trace statis/runtime menunjukkan debit D15A8 dibentuk independen dari seluruh penulis +0x1A/pending, atau watchpoint memperlihatkan tidak ada upstream store terkait; HJ4 gugur. |

Audit statis yang ada menyebut D15A8 menggunakan u16 tile+0x1A pada blok transaksi bersama; ini tidak memutuskan rumus untuk d≥2. Pengamatan pengguna tetap K1, bukan bukti final.

## CG3 — H6 headless, dua peluncuran, read-only

Target H6 SHA-256:
`d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475`.
Target state SHA-256:
`00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`.
Control state SHA-256:
`9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`.

### Run 41775137231 — dua peluncuran yang memiliki artefak lengkap

- Workflow `completed/success`; job `CG3 two independent PCSX-Redux H6 read-only launches`, job ID `126393618513`. Semua step termasuk headless run, cleanup, validasi laporan teks, dan commit laporan selesai `success`.
- Source SHA `6fd71b25b8a7e5f1695dd6fd32e5f993958b59f1`; H6 SHA sesuai target di atas.
- Dua proses PCSX-Redux independen, masing-masing mencapai 1.200 frame. Gameplay input `NONE`; RAM poke `NO`; CPU interpreter; debugger dan Lua write breakpoint aktif.
- Pada **kedua** raw log, restore menyatakan:
  `pointer_slot=0x801CDF80 expected_pointer=0x801CDF80 field_address=0x801CEE28 field_initial=0x00000000`.
  Baris berikutnya menyatakan `CG3_WRITE_WATCHPOINT_INSTALLED=1 address=0x801CEE28 width=4 type=Write`.
- `CG3_H6_FRAME_VALUES.tsv` mencatat pada frame **1/60/180/360/600/1200** di kedua launch: pointer `0x801CDF80`, field address `0x801CEE28`, nilai EA8 `0x00000000`. Tidak ada selisih antar-launch pada sampel ini.
- `CG3_H6_WRITE_WATCHPOINT.tsv` hanya berisi header; tercatat **0 hit**. Karena itu tidak tersedia PC/old/new untuk penulis EA8. Ini berarti tidak ada hit yang direkam oleh probe; tidak cukup untuk menyimpulkan penulis tertentu atau membuktikan tidak ada penulisan di luar cakupan/perilaku breakpoint.
- RAM frame 180 (2.097.152 byte) SHA-256 `5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7` pada kedua launch; cocok referensi.
- RAM frame 360 (2.097.152 byte) SHA-256 `4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907` pada kedua launch; cocok referensi.
- Memory Card disposable 128 KiB: SHA sebelum dan sesudah pada setiap launch `fa43239bcee7b97ca62f007cc68487560a39e19f74f3dde7486db3f98df8e471`; tidak berubah.
- Wall time launch 1 `413.593 s`, launch 2 `415.671 s`; timeout `3600 s` per launch, lebih dari 2× waktu terlama teramati (415.671 s). RAM snapshots lokal frame 180/360 di-hash lalu dihapus; tidak dipublikasikan.
- PCSX wrapper exit desimal `0` dan Lua quit desimal `0` pada tiap launch. Python driver exit desimal `2`; Actions job/workflow tetap `success`, tetapi `ACTIONS_RUN_SUMMARY.txt` sengaja mencatat `STATUS=SEBAGIAN`, `JOB=cg3-h6-readonly-watchpoint`, `SOURCE_SHA=6fd71b25b8a7e5f1695dd6fd32e5f993958b59f1`, `EXIT_CODE=2`.

### Run 41775298933 — pengulangan dua peluncuran

- Workflow `completed/success`; job `CG3 two independent PCSX-Redux H6 read-only launches`, job ID `126398319693`; seluruh step headless, cleanup, validasi teks, dan commit laporan berstatus success.
- Source SHA `f1ee369f670e39a67ab89c22b51da881e5cc9258`; H6 SHA tetap `d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475`.
- Dua peluncuran PCSX-Redux tambahan masing-masing mencapai frame 1.200, `GAMEPLAY_INPUT=NONE`, `RAM_POKE=NO`, restore pointer benar dan write-breakpoint dipasang.
- Pada kedua peluncuran: pointer `0x801CDF80`, alamat EA8 `0x801CEE28`, dan nilai EA8 `0x00000000` pada frame **1/60/180/360/600/1200**.
- Write watchpoint TSV hanya berisi header (**0 hit**); tidak ada PC/old/new yang bisa dilaporkan.
- RAM frame 180 dan 360 pada kedua launch kembali cocok dengan hash referensi: `5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7` dan `4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907` (masing-masing 2.097.152 byte).
- Memory Card disposable 128 KiB sebelum dan sesudah tiap launch: `fa43239bcee7b97ca62f007cc68487560a39e19f74f3dde7486db3f98df8e471`; tidak berubah.
- Wall time launch 1 `479.441 s`, launch 2 `480.465 s`; timeout `3600 s` per launch, lebih dari 2× waktu terlama. Cleanup RAM dan input private pass; tidak ada dump/frame dipublikasikan.
- PCSX wrapper exit desimal `0` dan Lua quit desimal `0` per launch. Python driver exit desimal `2`; ACTIONS summary `STATUS=SEBAGIAN`, `EXIT_CODE=2`, karena bug parser `0X` vs `0x` yang sama. Audit ulang raw log mengonfirmasi pointer dan alamat benar.
- Tidak ditemukan pesan `fatal`, `traceback`, atau `error:` pada raw log kedua peluncuran.

### Koreksi interpretasi flag pointer driver

Flag summary `POINTER_AND_WATCHPOINT_VERIFIED=False` adalah false-negative parser, bukan bukti pointer runtime salah. Di `experiments/cg3_h6_readonly_watchpoint.py`, parser mengubah token alamat dengan `.upper()`, sehingga `0x801CDF80` menjadi `0X801CDF80`; hasil itu lalu dibandingkan dengan literal `0x801CDF80` (huruf `x` kecil), dan tes string gagal. Saya mencocokkan ulang kedua raw log dengan parser-equivalent: keenam sampel per launch ada dan alamat cocok; juga tidak ada baris `CG3_POINTER_VERIFY=FAIL`. Keluaran mentah kedua launch mengonfirmasi nilai pointer dan field di atas. Akibatnya exit 2 adalah kegagalan gate Python akibat normalisasi prefix, bukan exit/crash emulator.

Kesimpulan CG3: **runtime repeatability untuk enam sampel frame H6 mencapai K5 terbatas** (empat peluncuran independen pada dua Actions run, semua enam sampel cocok, hash RAM dan Memory Card konsisten). Status butir tetap **SEBAGIAN**, sebab total empat launch menghasilkan 0 hit watchpoint; PC/old/new penulis EA8 = **TIDAK TAHU**. Ini tidak membuktikan tidak ada penulisan di luar cakupan/batas kemampuan breakpoint dan tidak membuktikan perilaku EA8 pada gameplay dengan input.

Artefak run:
- `reports/stage1_economy/cg3-h6-readonly-run-41775137231/attempt-1/ACTIONS_RUN_SUMMARY.txt`
- `reports/stage1_economy/cg3-h6-readonly-run-41775137231/attempt-1/CG3_H6_READONLY_SUMMARY.txt`
- `reports/stage1_economy/cg3-h6-readonly-run-41775137231/attempt-1/CG3_H6_FRAME_VALUES.tsv`
- `reports/stage1_economy/cg3-h6-readonly-run-41775137231/attempt-1/CG3_H6_WRITE_WATCHPOINT.tsv`
- Raw launch logs: `CG3_LAUNCH_1_RAW_LOG.txt` dan `CG3_LAUNCH_2_RAW_LOG.txt` pada direktori yang sama.

## Runner setelah koreksi publikasi

- Run `41775137231`: `completed/success`; hasil dua launch dan ringkasan teks sudah terkomit pada HEAD cutoff laporan ini.
- Run `41775298933` (source `f1ee369f670e39a67ab89c22b51da881e5cc9258`): `completed/success`, job `126398319693`; dua launch selesai dan artefak teks terkomit oleh bot pada `0afef96546fc892bfd8923891a0a664ac19f7dff`. Hasilnya sama-sama SEBAGIAN karena false-negative parser dan 0 hit watchpoint.
- Run `41773084992` sebelumnya berakhir `failure` pada langkah commit laporan karena `fatal: detected dubious ownership in repository`; hasilnya tidak dipakai untuk menggantikan artefak lengkap run 41775137231.

## File sumber audit statis di repo

- `reports/stage1_economy/aq1-run-41769361956/attempt-1/cg_raw_mips_offset_scan_summary.txt`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/cg_raw_mips_offset_candidates.tsv`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ea8-entry1-offset-audit.tsv`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/ea8-exe-offset-audit.tsv`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/cg1-ea8-writer-function-detail.txt`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/cg2-tile-fee-writer-function-detail.txt`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-event-function-detail.txt`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-d15a8-function-detail.txt`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-action-byte-access.tsv`
- `reports/stage1_economy/aq1-run-41769361956/attempt-1/bb2-d15a8-direct-callers.txt`

---
Catatan batas: ledger CG0 mencakup seluruh 17 commit dari baseline sampai HEAD cutoff `0afef96546fc892bfd8923891a0a664ac19f7dff`. Commit laporan revisi yang sedang diterbitkan ini sendiri tidak dimasukkan ke ledger (cutoff audit dinyatakan eksplisit). Tidak ada perubahan terhadap Release, `STATUS.md`, visibilitas repo, atau berkas biner.
