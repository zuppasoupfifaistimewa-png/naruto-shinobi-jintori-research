<!-- current-step9-helper-checkpoint-2026-10-28 -->
# CHECKPOINT TERBARU — uji helper counter terisolasi, 28 Oktober 2026, 07:03 WIB

Sumber kode yang diuji: commit [`7f234820f1b83a34654e900592903678365006a5`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/7f234820f1b83a34654e900592903678365006a5). Actions [run #40606159061](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40606159061) **completed/success** pada 07:03:03 WIB. Artefak teks #12779814671: 5.377 byte, SHA-256 ZIP `dd3e559997ce0c9f931f330144de8021bdb3c75fa16b4f21717299c4b2d4d79f`.

Hasil terverifikasi dalam log dan laporan: RNG `0x80035D78` **7/7**; helper `0x80037138` jalur `a0<0` **8/8**; accessor `0x8001387C`/`0x800138EC` **16/16**. Untuk helper, argumen `0xFFFFFFFF` dan `0x80000000` diuji pada global sintetis `0`, `1`, `0x12345678`, `0xFFFFFFFF`; v0 cocok dengan global `0x80066E7C` yang diinjeksi, global tetap, PC mencapai sentinel `0x001FF000` sesudah 33 instruksi dan tanpa error. Log memuat `STEP9_TESTS=PASS` serta `STEP9_PRIVATE_CLEANUP=PASS`.

Batas penting: global pointer `0x80065D34` memuat `0x1F801814`, dan `0x80065D38` memuat `0x1F801110`. Tes memetakan MMIO sebagai fixture sintetis dengan word tetap `0x12345678`, bukan timer/hardware PS1 aktual. Hasil ini mengonfirmasi jalur return negatif pada CPU plus MMIO sintetis saja—bukan seed boot, lifecycle, reachability entry-0, atau aturan gameplay. Step 4 tetap **SEBAGIAN**; Step 9 tetap **SEBAGIAN keseluruhan** (belum semua fungsi/conditions/gameplay tercakup).

Riwayat metode: [#40605560982](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40605560982) gagal karena SyntaxError sebelum kasus berjalan; [#40605654394](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40605654394) gagal pada tes akibat MMIO belum dimodelkan. Keduanya bukan hasil permainan. [#40605904131](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40605904131) menghasilkan tes PASS tetapi laporannya memiliki kolom duplikat; #40606159061 adalah run final yang lulus dengan tabel diperbaiki. Cleanup PASS dan artefak hanya teks/log.

Status lintas langkah tetap: Step 4 SEBAGIAN; Step 5 SEBAGIAN (13 main EXE + satu kandidat resource dibandingkan); Step 6 SEBAGIAN (pointer/alias BLOCKED, arti field UNKNOWN); Step 7 SEBAGIAN (runtime mapping BLOCKED); Step 8 SEBAGIAN, aturan biaya/barrier/kartu/turn/battle/menang-kalah masih UNKNOWN; Step 9 SEBAGIAN; Step 10 TUNTAS hanya sebagai matriks audit. Tidak ada gameplay, input emulator, restore savestate, pemain otomatis, atau perubahan policy/runner. **Story Mode TIDAK TERBUKTI TAMAT.**

---

<!-- verified-live-checkpoint-2026-10-28 -->
# VERIFIED LIVE CHECKPOINT — 28 Oktober 2026, 04:22 WIB

This addendum supersedes earlier snapshots in this file if they conflict. Repository HEAD at inspection: `985a328446295f4b8e526abd9eac9c6f86e70a6e` on `main`. Latest Actions status inspection: **0 queued and 0 in progress**. The most recent unrelated run, [#40561735718](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40561735718), is named “Naruto Story Mode adaptive player monitor”; its success is a monitor result, not evidence that a player ran or that Story Mode completed.

## Step 4 / broad Ghidra run — completed workflow, partial internal analysis

[Run #40521141039](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521141039) completed with workflow conclusion **success** at 22:26:43 WIB on 27 October. Artifact [#12744894595](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521141039/artifacts/12744894595) is 1,694,938 bytes; validated ZIP SHA-256 `a8e10655e5e6145c3b72edd030cfaa991c6cbfb2300c35b232fb458f4028eec6`. However, the raw artifact log `entry0-ghidra-headless.log` explicitly records **analysis timeout at 1,800 seconds** for DATA.BIN entry 0 and repeated function-body overlap/repair failures. The output still exported 38 entry-0 function rows, but this is not successful complete auto-analysis of that resource. Candidate `0x800BDBFC` is decoded as `j 0x800BE11C`, has `reference_count=0`, and does not constitute a validated caller/helper boundary. Entry-0 base `0x800AD000` remains a static hypothesis. Keep Step 4 partial; seed lifecycle, validated caller boundary, runtime reachability and gameplay effect remain unknown.

The successful bounded context runs [#40521136060](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521136060) and [#40521136038](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521136038) added raw instruction bytes/context. At entry-0 candidate `0x800AF2AC`, `-1` is the argument to helper `0x80037138`; its return value is moved to the argument for candidate setter `0x80035DA8`. This is static control/data-flow evidence under the hypothetical mapping, not proof of a runtime boot seed. Three direct JALs were decoded in entry 0, but **zero** caller functions had validated boundaries; two other sites (`0x800BB748`, `0x800BB770`) remain raw-word matches whose instructions did not decode.

## Step 5 — one additional resource function compared

[Run #40523020556](https://github.com/zuppasoupfivaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40523020556) completed success at 21:40:45 WIB. Artifact [#12742268706](https://github.com/zuppasoupfivaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40523020556/artifacts/12742268706), 1,367,605 bytes, validated ZIP SHA-256 `5f3f767667444f7c956c36fc59cf75b6bb90a5a1dde8ddb92fb69f9e0f797e81`. Entry-1 candidate `0x800ED8C8` is a Ghidra function boundary of 160 bytes ending exclusively at `0x800ED968`; Ghidra decompilation and m2c completed, exit code 0, and both outputs show a direct RNG call at `0x800ED8E4`. Together with the 13 main-EXE functions, **14 selected functions** now have structural Ghidra/m2c comparison. Step 5 remains partial overall.

Static behavior of the candidate function: it masks the input index to 16 bits, calls helper `0x800CB4B4`, calls RNG `0x80035D78`, computes a value modulo 250, loads a pointer/value from global slot `0x8013EA74`, uses `index * 0x90` to locate a record and reads byte `+0x29). It returns the helper byte unless the RNG-derived value is greater than or equal to that byte, in which case it returns `0xFF`. The entry-1 base `0x800D0000`, pointer value/table mapping and gameplay feature identity are not runtime verified. This does not prove a card, battle, roulette or victory rule.

## Step 6 — CFG/SSA evidence improves local dataflow, not full pointer closure

[Run #40522772847](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40522772847) completed success at 21:38:32 WIB. Artifact [#12741234990](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40522772847/artifacts/12741234990) is 234,210 bytes; validated ZIP SHA-256 `7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9`. CFG-aware high-level SSA/P-code and raw body output were emitted for functions `0x8012C544` (292 body bytes) and `0x8012CACC` (152 body bytes) within the candidate entry-1 view.

In `0x8012C544`, static instructions show loads from `+0xB30` and `+0xB38`, addition and store to `+0xB40`; the initialization branch also zeros `+0xB44). In `0x8012CACC`, a read of `+0xB44` at `0x8012CB14` is passed as an argument to `0x8001B364) on the branch where byte `+0xB2A > 5). SSA makes these intra-function def/use relationships across decoded basic blocks more explicit, but the base derives from the unknown value in global slot `0x8013A554`; traces terminate at unknown/address-tied input or depth limits. Runtime object identity/base, global pointer writers, aliases across all functions and gameplay field semantics remain unresolved. Keep 6(a) partial, 6(b) blocked, 6(c) partial and 6(d) unknown.

## Overall acceptance snapshot

- Step 4 **SEBAGIAN**: LCG formula and isolated test are verified; seed lifecycle/caller boundaries/runtime effect remain unknown.
- Step 5 **SEBAGIAN**: 13 main-EXE plus one entry-1 candidate function compared; broad resource and transition/caller coverage remains incomplete.
- Step 6 **SEBAGIAN**: local CFG/SSA evidence improved; global pointer/alias and semantic field closure remain blocked/unknown.
- Step 7 **SEBAGIAN**: disc directory/bootstrap copy structure is static evidence; runtime loader destination, relocation, lifecycle, DATA2/DUMMY mapping remain unknown.
- Step 8 **SEBAGIAN**: function behavior can be described where shown by instructions; costs, barrier/upgrade, cards, turn/battle/roulette and victory/loss rules remain unknown.
- Step 9 **SEBAGIAN overall**: RNG 7/7 and player-value accessors 16/16 isolated assertions pass; this is not full PS1 gameplay.
- Step 10 **TUNTAS only as a criterion reconciliation/index**, not as global game reverse-engineering completion.

Safety boundary for this research session: no adaptive player or Story Mode runner was run by this work; no gameplay input or savestate restore occurred; no emulator gameplay session was performed. The monitor-only Actions run is not a completion proof. Private ROM/BIN/CUE/EXE, BIOS, Memory Card, savestate, RAM dump, screenshots or gameplay-private evidence were not committed or uploaded by these static runs. **Story Mode is not verified complete.**

---

## Additional boundary caution from the entry-0 artifact

The raw context around `0x800BDBFC` shows a function-like stack prologue and preceding control-flow instructions at `0x800BDBE4`–`0x800BDBF8``, followed by `j 0x800BE11C` at `0x800BDBFC`. Thus `0x800BDBFC` is visibly inside an instruction sequence that already has a stack-frame setup; treating that jump as an independently validated function entry is unsupported. Combined with `reference_count=0` and Ghidra body-overlap errors, this candidate cannot currently be used as the setter's caller/helper or as proof of loader reachability. This observation is bounded to the emitted raw window; it does not automatically validate `0x800BDBE4` as a formal Ghidra function boundary.

---

# ACTIONS CHECKPOINT OVERRIDE — 27 Oktober 2026 21:54:52 WIB

Newest run state supersedes older snapshots inside this handoff:
- [#40520635663](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40520635663): overall completed/success, artifact #12743796502, 2.299.302 bytes, ZIP SHA-256 `e2d5b496b2310c17110c59710212f7605bf8b3d90b798abb438c1224bf3d0549`. Actual `entry0-ghidra-headless.log` says analysis timed out after 1,800 seconds; the export has 36 function rows but many body-overlap/repair errors. Candidate `0x800BDBFC` has zero recorded references. This is not a validated helper/caller result.
- [#40521141039](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521141039) was still in progress at the last API update (21:54:52 WIB): entry1 completed, entry0 analysis in progress, no artifact yet. Based on the previous same-workflow run taking 31m27s and hitting the 1,800-second analysis timeout, a rough ETA is 21:58–22:05 WIB, not guaranteed. Do not launch a duplicate.

The entry-0 delay-slot context remains valid local instruction evidence; caller boundary, helper return at runtime, seed lifecycle, actual resource base, and gameplay effect remain UNKNOWN.

---

# HANDOFF TERBARU — Rekonsiliasi Step 4–10, 27 Oktober 2026 21:41 WIB

Mulai dari `main` yang sebelumnya berada di `c36b7407631291afd2a4d303f49a8b03392e2bbc`; pembaruan laporan sejak itu membuat commit dokumentasi baru. Prioritaskan [live reconciliation](STEP4_10_LIVE_RECONCILIATION_2026-10-27.md), [CFG/SSA audit Step 6](STEP6_CFG_SSA_DATAFLOW_AUDIT_2026-10-27.md), [Step 5 candidate function report](STEP5_DATABIN_ENTRY1_ANALYSIS_2026-10-27.md), dan [matrix audit](REVERSE_ENGINEERING_AUDIT_STEPS_1_10_2026-10-27.md).

## Checkpoint terbaru

- Step 4 tetap SEBAGIAN. RNG utama dan isolated vectors sudah diverifikasi. Context entry-0 #40521136060 / artifact #12742056745 dan entry-1 #40521136038 / artifact #12741592577 sukses. Pada `0x800AF2AC`, delay slot `move a0,v0` meneruskan return `0x80037138` ke `0x80035DA8); caller boundary dan seed runtime belum terbukti.
- Step 5 tetap SEBAGIAN overall. Run #40523020556 success dengan artifact #12742268706, ZIP SHA-256 `5f3f767667444f7c956c36fc59cf75b6bb90a5a1dde8ddb92fb69f9e0f797e81`; function entry `0x800ED8C8), body 160 bytes, Ghidra/m2c same-address cross-check success. Ini satu fungsi resource kandidat tambahan, bukan cakupan penuh.
- Step 6 tetap SEBAGIAN. Run #40522772847 success; artifact #12741234990 SHA-256 ZIP `7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9`. CFG/SSA memetakan operasi init dan read-add-write, tetapi global pointer value/alias unresolved. 6(a) partial, 6(b) BLOCKED, 6(c) partial, 6(d) UNKNOWN.
- Step 7 remains SEBAGIAN; resource base runtime/loader lifecycle not proven. Step 8 remains SEBAGIAN; function behavior clarified, feature identity and game rules unknown. Step 9 remains SEBAGIAN overall; RNG 7/7 and setter/getter 16/16 isolated tests passed; cleanup PASS. Step 10 is TUNTAS only for criterion-level documentation/matrix.
- Main EXE Ghidra run #40512917437 finished earlier at 21:07:13 WIB. It is not active now.

## Actions live at the last checked snapshot

- #40523020556 Step 5 resource Ghidra/m2c: completed/success, artifact #12742268706.
- #40522772847 Step 6/7 static scan + SSA export: completed/success, artifact #12741234990.
- #40520635663 Ghidra static analysis main workflow: API says in_progress, started 21:23:22 WIB, last update stale and step still says analyzing entry 0. The comparable completed Ghidra run #40512917437 took 34m43s; ~21:58 WIB is only a rough reference, not guaranteed. #40521141039 is pending in the same concurrency group. Do not start duplicate scans; re-check IDs/status and artifact before relying on either result.

## Continuation boundaries

1. Re-check HEAD and run/artifact states first; don't trust embedded historical Actions snapshots.
2. Read the full text artifact/report before drawing conclusions.
3. To continue Step 6, use CFG/SSA data in the new report, especially pointer global `0x8013A554`, `+0xB44` branch/merge and unresolved alias; do not repeat the old offset census alone.
4. Extend Step 5 only when a new target has a validated function boundary and an explicit static hypothesis. `0x80012A70` has not been validated as a Ghidra function entry in the prior comparison view.
5. Do not rerun RNG/accessor tests 7/7 and 16/16 absent a new case or change requiring regression.
6. No adaptive player, Story Mode runner, classifier, input policy, readiness gate, `.run-storymode-adaptive-player`, gameplay input, emulator session or savestate restoration. Keep private game files, BIOS, Memory Card, saves, RAM dumps and screenshots out of Git/artifacts.

Story Mode **TIDAK TERBUKTI TAMAT**. The new function behavior is static evidence under a hypothetical resource base and is not a gameplay victory proof.

---

# HANDOFF TERBARU — Step 9 accessor tests passed, 27 Oktober 2026, 21:02 WIB

## Step 9 — hasil isolasi diperluas final (27 Oktober 2026, 21:02 WIB)

Run [#40516755810](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40516755810) **completed/success** pada 21:02:36 WIB. Artifact teks #12740305973: 4.567 byte, SHA-256 ZIP bf1a702074849b2592bfc5555a0d493b5ed86d3de0b9895a192db7fdf9f80cd4. Raw job log/job summary memastikan semua 11 langkah success, termasuk STEP9_PRIVATE_CLEANUP=PASS. Hasil aktual: RNG 0x80035D78 7/7 vektor dan setter/getter 0x8001387C/0x800138EC 16/16 kasus PASS. Setter membatasi nilai [-9999,99999], valid index 0–3 return 1, invalid 4/0xFFFFFFFF return 0 tanpa perubahan slot; getter membaca slot yang sama untuk indeks valid dan return 0 untuk indeks invalid. Setiap tes memeriksa v0/memory, return sentinel dan batas ≤128 instruksi.

Ini uji CPU/RAM terisolasi dengan teks executable terverifikasi, bukan emulator PS1, BIOS, gameplay/input/savestate, dan bukan bukti formula biaya, aturan barrier/upgrade, giliran atau kemenangan. Step 9(b) kini SEBAGIAN (bukan UNKNOWN) karena dua accessor tambahan sudah diuji; Step 9 overall tetap SEBAGIAN karena target-compare, transisi, helper/caller lain dan semua jalur gagal belum tercakup. [Laporan hasil uji](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/out/step9/STEP9_UNICORN_RESULT_2026-10-27.md).


## Next continuation priorities

1. Check current state/artifact of [Ghidra static run #40512917437](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40512917437) first. It is the only known run still active; no new runtime probe should be started simply because this run takes time.
2. Continue offline Step 4–10 analysis against [live reconciliation](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/docs/STEP4_10_LIVE_RECONCILIATION_2026-10-27.md). Step 5 is partial overall despite 13 main-EXE pairs passing; Step 6(b)/7(b) remain blocked; Step 8 rules remain unknown; Step 9(b) is partial only for two accessors.
3. Do not run or edit adaptive-player, Story Mode runner, classifier, input policy, readiness gate, .run-storymode-adaptive-player, gameplay inputs or savestate restore. Do not infer costs/barrier/turn/victory from field offsets alone. Story Mode is NOT verified complete.

---

## Step 5 — hasil perluasan terverifikasi (27 Oktober 2026, 20:50 WIB)

- Retry [#40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524) **completed/success** pada 20:50:53 WIB. Artefak teks [#12739676233](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524/artifacts/12739676233) berukuran 941.176 byte, digest API dan SHA-256 lokal cocok: `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d`. ZIP memuat 45 file teks/C/disassembly/log, termasuk 26 file C Ghidra/m2c nonempty; tidak ada ROM/BIN/CUE/EXE/BIOS, Memory Card, savestate, RAM dump atau screenshot. Semua langkah job selesai, termasuk penghapusan input/proyek sementara.
- Pemeriksaan aktual: `metadata_parser_fixture=PASS`, `function_metadata=PASS`, `functions_requested=13`, `functions_with_m2c_output=13`, laporan akhir `status=SUCCESS`. Masing-masing fungsi memiliki keluaran C Ghidra dan m2c; exit code m2c 0 untuk 13/13.
- Lingkup 13 target main EXE: empat caller RNG terdahulu; setter/getter nilai pemain pada `0x8001387C`/`0x800138EC`; RNG `0x80035D78`; helper `0x80037138`; dispatcher/initializer/callback routines `0x800373F8`, `0x8003755C`, `0x80037B58`, `0x80037BB0`, `0x80037C48`. Ini cross-check struktur same-address berdasarkan batas fungsi Ghidra, bukan kesamaan source asli atau bukti aturan gameplay.
- Percobaan pertama [#40512956924](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40512956924) gagal karena `0x80012A70` tidak memiliki fungsi Ghidra pada alamat itu dan tak memiliki metadata body. Perbaikan di [commit `2b16e67bfafde873c95b577bc030f6e0c9f84c58`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/2b16e67bfafde873c95b577bc030f6e0c9f84c58) mengeluarkan target itu dari daftar fungsi yang dibandingkan. Identitas/semantik target `0x80012A70` tetap perlu diperjelas; jangan anggap cross-check fungsi tersebut sudah berhasil.
- **Status Langkah 5 secara keseluruhan tetap SEBAGIAN** terhadap cakupan yang diminta: 13 fungsi inti executable utama sudah dibandingkan, tetapi fungsi kandidat di DATA.BIN entry 0/1 (termasuk pembanding target/record dan transisi), semua hubungan caller/callee wajib, serta seluruh executable belum dicakup m2c secara menyeluruh. Status lama “empat fungsi saja” adalah riwayat sebelum perluasan, bukan hasil terbaru.
- Run Ghidra statis terpisah [#40512917437](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40512917437) masih `in_progress`, dimulai 20:32:30 WIB, pada langkah analisis DATA.BIN entry 0 untuk external helper. Pembanding Ghidra sebelumnya #40498208067 membutuhkan sekitar 31 menit 47 detik; perkiraan kasar berdasarkan durasi itu sekitar **21:04 WIB**, bukan ETA terjamin.

---

# HANDOFF TERBARU — Step 6 provenance scan verified (27 Oktober 2026, 20:25 WIB)

**Checkpoint terbaru Step 6 (27 Oktober 2026, 20:25 WIB):** scanner provenance di https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/0afc0eec4a5c12e4df5a17c771c8b0d28d7a99dd dijalankan oleh [Actions #40511758146](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40511758146) — completed/success pada 20:25:48 WIB. Artifact [#12737611770](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40511758146/artifacts/12737611770), 229.233 byte, SHA-256 ZIP `b84ff017cdbefb8ece6d04a7c8bef66b3fdc27b61412e91e10cc01485225b126`; digest API sama dengan SHA lokal. Enam anggota ZIP hanya teks/log; `text_only_output_count=6`, `private_binary_in_artifact=no`, `STEP6_PRIVATE_CLEANUP=PASS`. Fixture parser operand dan fixture pembentukan alamat `lui/ori/addiu/sign-extension` benar-benar mengeluarkan PASS. Laporan: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/docs/STEP6_REGISTER_PROVENANCE_AUDIT_2026-10-27.md.

## Keadaan aktual dan aturan kelanjutan

1. Source code scanner berada pada commit `0afc0eec4a5c12e4df5a17c771c8b0d28d7a99dd`. Laporan run dan hasil fixture: [`docs/STEP6_REGISTER_PROVENANCE_AUDIT_2026-10-27.md`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/docs/STEP6_REGISTER_PROVENANCE_AUDIT_2026-10-27.md). Jangan mengulang scan yang sama tanpa perubahan sumber atau hipotesis baru.
2. Resolver baru hanya melakukan backwards linear trace terbatas dan ekspresi konstanta terbatas; fixture LUI/ORI/ADDIU/sign-extension PASS. Untuk +B30/B38/B40, `a0` berasal dari instruksi `lw a0,-0x5AAC(s0)` di 0x8012C628; peran register `s0` belum dibuktikan dan trace-nya terhenti di control-flow boundary. +B44 read's `v1` berhenti di branch 0x8012CAF8. Step 6(b) tetap BLOCKED dan base 0x800D0000 tetap HIPOTESIS.
3. Lanjutkan hanya dengan analisis luring yang menambah coverage nyata: trace address construction/def-use dengan control-flow-aware dataflow atau audit raw MIPS yang melaporkan seluruh batas/coverage. Jangan menamai field Chakra/cost/turn/barrier/level-up.
4. Jangan ulang breakpoint no-hit 0x800AD454 atau seed-setter no-hit tanpa bukti reachability statis baru. Jangan menjalankan game/emulator, input, restore savestate, adaptive player, classifier/policy/readiness gate, atau workflow `.run-storymode-adaptive-player`.
5. Reconcile setiap perubahan pada `docs/STEP4_10_LIVE_RECONCILIATION_2026-10-27.md`, `docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md`, `STATUS.md`, `ANALYSIS_LOG.md`, dan `out/logic.md`. Story Mode TIDAK TERBUKTI TAMAT.

---

# HANDOFF UPDATE — offline Step 6 scan reconciled, 27 Oktober 2026

Mulai dari [live reconciliation](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/docs/STEP4_10_LIVE_RECONCILIATION_2026-10-27.md) dan matrix 17 kriteria di dalamnya. HEAD pra-audit adalah cc81319cc00037a92a93a3e76552245dd9a9ebf7. Scan terbaru (#40504640855) sudah menghasilkan inventory agregat lengkap pada instruksi direct base+displacement yang dikenali dan didekode; jangan mengulang scan sama. Inventaris independen: 2.104 offsets, 31.081 direct operands, 19.366 read/11.715 write dari 98.357 instruksi terdekode. Konteks per-access untuk offset umum dibatasi 200; B30/B38/B40/B44 tidak terkena cap konteks.

Langkah statis lanjutan bernilai tambah adalah menelusuri raw MIPS address construction, control flow, aliases, split immediates dan alternate base untuk Step 6; cari source/callee B30/B38/B40/B44 tanpa menamai field. Belum ada PC runtime baru yang mendapat dukungan reachability statis untuk loader, jadi jangan ulangi no-hit probe 0x800AD454 atau seed setter. Jangan akses repo lain, jangan ubah adaptive player/Story Mode runner/classifier/policy/readiness gate, dan jangan jalankan gameplay/input atau restore savestate. Story Mode TIDAK TERBUKTI TAMAT.

---

# HANDOFF UPDATE — Step 6 inventory audited, 27 Oktober 2026 19:35 WIB

HEAD `main` before this handoff update: `f3a1797afecfc9240462a3aa5a54838b34830492`; fetch live main on next continuation. The latest scan is [#40504640855](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504640855) success at 19:34:31 WIB; artifact #12733854252, 220,128 bytes, ZIP SHA-256 `90288a1c8b454cbdc45c75e0244d26508628ecf88bfe8e73ed88524c8cb80891`. Runner audit [#40504977322](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504977322) success 19:35:51 WIB; text artifact #12734840847, 25,756 bytes, ZIP SHA-256 `d022b23548fe95eb34bfbb7a7fb0dd190a498ca54fff11516818138701920398`; metadata and digests validated, `RUNNER_ARTIFACT_CLEANUP=PASS`.

Latest direct-memory operand inventory on the hypothetical DATA.BIN entry-1 base `0x800D0000`: `+0xB30` = 1 read/0 writes, `+0xB38` = 1 read/0 writes, `+0xB40` = 0 reads/1 write, `+0xB44` = 1 read/1 write. Full aggregated displacement inventory is between explicit BEGIN/END in the runner output and remained below the audit output cap; the four priority offsets have no per-offset cap. This is a verified static scan over 98,357 Ghidra-decoded instructions with recognized base+displacement syntax, not a complete alias/pointer/undecoded-code proof. Base remains HIPOTESIS; base-register tracing is a bounded 24-instruction linear window/simple-move hint. Do not infer cost/barrier/Chakra/turn/level-up semantics from these offsets.

The latest Step 6 detailed report is `docs/STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md`; closure matrix is `docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md`. Overall step status remains Step4 SEBAGIAN, Step5 TUNTAS only four selected functions, Step6 SEBAGIAN, Step7 SEBAGIAN, Step8 SEBAGIAN, Step9 TUNTAS only for `0x80035D78`, Step10 TUNTAS only as criteria closure matrix. Story Mode TIDAK TERBUKTI TAMAT. No gameplay/input/savestate/adaptive-player changes.

## Recommended continuation
1. Fetch live main and Actions; read this addendum and the current closure matrix.
2. Step6's direct offset census is now improved; next work must trace exact writer/reader callers, register-derived addresses, aliases, split immediates, alternate bases and decompilation failures in raw MIPS. Don't rerun unchanged broad scans unless a parser/code change justifies it.
3. Step4/7 still need mapping/order/runtime evidence; don't repeat the same no-hit breakpoints. Any new runtime diagnostic must be a statically justified target, bounded, no gameplay input/no savestate, text-only registers/copy length/checksum, cleanup confirmed.
4. Step8 rules stay UNKNOWN until raw MIPS/data flow and an independent state/result fact agree. Keep Japanese text and Indonesian translation side by side where relevant.
5. Do not touch any other repository or adaptive-player/Story Mode runner/classifier/policy/readiness gate. No private game assets in Git/artifacts.

---

# HANDOFF TERBARU — Reverse Engineering Naruto PS1, Langkah 4–10

Tanggal snapshot: 27 Oktober 2026, sekitar 19:25 WIB.

## Checkpoint GitHub yang harus dipercaya

Repositori yang diizinkan satu-satunya: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research.

HEAD main yang diverifikasi sebelum penulisan ulang handoff ini: 8d00dd076464584af9dd66553a4dd54b4acc1211. Commit yang menulis ulang handoff ini kemudian menjadi commit terbaru main. Pada awal chat lanjutan, fetch ulang main dan catat SHA live sebelum perubahan; jangan pakai HEAD lama sebagai aktual.

Runner-only audit terbaru: [Actions #40503223693](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40503223693), completed success 19:22:30 WIB; artifact text-only [#12733512950](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40503223693/artifacts/12733512950), 13,079 byte, ZIP SHA-256 382773f9a421835bc97c448c630a2ea5d3891309bb34094f5a67027548c03414. Raw log memverifikasi metadata run/id/nama/size/digest/expiry, hash ZIP sebelum pembacaan, raw_artifacts_or_game_binaries_uploaded=no, dan RUNNER_ARTIFACT_CLEANUP=PASS. Tidak ada emulator/game, input gameplay atau restore savestate dalam audit.

Sumber yang telah diaudit di runner:
- Ghidra full analysis [#40498208067](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498208067) selesai success pukul 19:14:42 WIB. Artifact [#12732952776](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498208067/artifacts/12732952776), 2,255,170 byte, SHA-256 ZIP 6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6. Output: 1.206 baris indeks fungsi main EXE, 1.555 baris entry 1, 38 entry 0. Log raw entry0 346,593,927 byte hanya di-hash, tidak dibaca penuh.
- Step6 field scan [#40500058788](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40500058788) selesai success pukul 18:59:18 WIB. Artifact [#12731474756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40500058788/artifacts/12731474756), 180,174 byte, SHA-256 ZIP 4aea20e1420292505666f15898ba2db57a875a4fc67fbe2c65336af0a16fc9f4. Scanner melaporkan 98.357 instruksi terdekode, tapi hanya mencari exact 16-bit immediate; cap 200 hit per offset; pointer arithmetic, split immediates, alias, kode tak terdekode dan base alternatif tidak seluruhnya ditangani. Raw job mencatat STEP6_PRIVATE_CLEANUP=PASS dan private_binary_in_artifact=no.
- Helper/callback static audit [#40499270568](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499270568), artifact [#12731593532](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499270568/artifacts/12731593532), 11,672 byte, SHA-256 ZIP 8567a5cad2a00823302ea7b361dd9b6eaab736bce6b77cf51ea136d6bee454b3; cleanup PASS.

## Temuan statis baru Step 4

- Main EXE function 0x80037B58 menulis nol ke global 0x80066E7C pada 0x80037B7C dan mengosongkan delapan slot callback yang berawal 0x80066E5C via helper 0x80037C48 dengan jumlah 8 pada delay slot.
- Function 0x80037B58 menyiapkan a0=0 serta a1=0x80037BB0 lalu memanggil dispatcher tak langsung 0x800373F8. Function 0x80037BB0 menaikkan 0x80066E7C, menyimpannya, lalu menelusuri delapan slot dan menjalankan pointer nonnol via JALR. Ini mendukung deskripsi callback/tick-like counter secara statis, bukan makna gameplay yang pasti.
- Function 0x80037138 pada jalur a0 negatif memuat 0x80066E7C ke v0. Candidate callsite DATA.BIN entry0, hanya dengan base hipotesis 0x800AD000: jal 0x80037138 pada 0x800AF2A4; delay slot li a0,-1 pada 0x800AF2A8; jal 0x80035DA8 pada 0x800AF2AC; delay slot move a0,v0 pada 0x800AF2B0. Karena itu -1 adalah argumen helper, dan setter menerima return helper; tidak terbukti bahwa setter menerima -1.
- Belum diketahui: apakah global ini benar seed game; kapan initializer/dispatcher dipanggil relatif ke callsite entry0; runtime base/entry point; nilai register saat setter; reachability caller. Probe setter #40485987817 no-hit sampai frame120, exit124 pada batas 35s. Jangan ulang target yang sama tanpa hipotesis reachability baru.

## Status kriteria Langkah 4–10

| Langkah | Status | Bukti saat ini | Yang belum ditutup |
|---|---|---|---|
| 4 — RNG, seed, callers, determinisme | SEBAGIAN | Static LCG/callers; helper/callback global; roulette checkpoint runtime terbatas. | Seed lifecycle/runtime setter value, urutan dan mapping entry0, hubungan caller roulette ke hasil visual, battle RNG caller, indirect/JT/decompressed paths, RNG alternatif. |
| 5 — perbandingan Ghidra/m2c | TUNTAS untuk empat fungsi saja | Run #40449144521, artifact #12710000931, 926,540 byte; SHA-256 ZIP b2fdb6dc3213137e98e0ed298402e1d4b02198ed5310f264780bd8e965246b08. Empat pasang output C untuk 0x80015ADC, 0x80015B7C, 0x8001A328, 0x80020BF4. | Jangan mengklaim semua fungsi atau kode sumber asli. |
| 6 — field read/write, aliases, xref/dataflow | SEBAGIAN | Run #40500058788 artifact #12731474756; raw window +0xB30/+0xB38 -> addu -> +0xB40, +0xB44 store dan read. Detail dan batas ada di docs/STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md. | Base 0x800D0000 hipotetis; full reader/writer/alias/effective-address inventory, undecoded regions dan field/game semantics unknown. |
| 7 — loader/copy/runtime mapping | SEBAGIAN | Loader directory/copy path statis. Probe #40484548650 artifact #12724961702 (3,960 byte, SHA-256 ZIP 27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71) no-hit di 0x800AD454 sampai frame120, timeout35s dan cleanup pass. | Tidak ada runtime source/dest/size/register/checksum; base/relocation dan lifecycle belum terbukti. |
| 8 — semantik fungsi/aturan game | SEBAGIAN | Instruksi/raw MIPS dan dataflow terbatas yang dijelaskan dalam docs/STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md. | Biaya/barrier/upgrade, battle/roulette/turn, efek kartu, kondisi kemenangan belum verified; tidak menyebut field sebagai Chakra atau biaya tanpa bukti independen. |
| 9 — eksekusi fungsi terisolasi | TUNTAS untuk 0x80035D78 saja | Run #40474891838 artifact #12720127454, 3,201 byte, SHA-256 ZIP bcbfcd77a532ce34334ed60f720fdeaac566308bf2e6e4d54a7e60f28a5f083b. 7/7 vectors, state/v0 cocok, sentinel return12 instruksi/vector, limit128, RAM PS1 fisik 2 MiB. | Tidak menguji fungsi lain atau emulator PS1/gameplay lengkap. |
| 10 — closure matrix | TUNTAS sebagai matriks audit per-kriteria saja | docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md sekarang punya tabel Step4 4(a–e), Step5, Step6(a–c), Step7(a–b), Step8(a–b), Step9, Step10 dengan sumber/artefak/digest, tes, batas dan next action. | Bukan klaim seluruh reverse engineering atau aturan game sudah selesai; refresh matrix setiap ada bukti baru. |

Story Mode: **TIDAK TERBUKTI TAMAT**. Jangan menulis bahwa permainan selesai tanpa bukti ending autentik dari emulator/game dengan asal bukti yang tervalidasi.

## Dokumen terkini yang harus dibaca terlebih dahulu

1. docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md — matriks closure aktual dan blocker per kriteria.
2. STATUS.md lalu ANALYSIS_LOG.md lalu out/logic.md — checkpoint/log/indeks yang baru disegarkan.
3. docs/STEP4_RNG_TRACE_2026-10-27.md — callback global/helper-return dan batas seed.
4. docs/STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md — operand bytes dan keterbatasan scanner.
5. docs/STEP7_RUNTIME_COLD_BOOT_RESULT_2026-10-27.md — hasil bounded no-hit.
6. docs/STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md — semantik dan aturan yang belum didukung.
7. docs/REVERSE_ENGINEERING_AUDIT_STEPS_1_10_2026-10-27.md — kriteria umum.

## Lanjutan yang diizinkan

1. Mulai dengan fetch live main, periksa daftar Actions/artifact terbaru, dan gunakan addendum teratas sebagai status otoritatif; jangan ulang Ghidra yang sama.
2. Prioritas teknis berikutnya: perluas Step6 scanner statis agar memproses semua memory operands, tracking register/effective address, aliases dan batas/cap; catat semua reader/writer dan area tak terdekode tanpa menganggap no-hit universal.
3. Untuk Step4, susun raw MIPS order/caller mapping dan address mapping untuk entry0 sebelum mengajukan probe runtime. Seed claim memerlukan register nyata pada callsite/setter; tidak cukup dengan instruksi statis.
4. Untuk Step7, jangan ulang probe 0x800AD454 no-hit yang sama. Runtime test hanya bila ada PC copy reachable yang dapat dibenarkan statis; coldboot, tanpa input/restore, single breakpoint, frame/time limit, output teks-only, cleanup terverifikasi.
5. Untuk Step8, table per-rule harus mencantumkan function/callers, raw branch/store, register/dataflow, source independent kedua, evidence status dan unknown. Teks Jepang harus ditemani terjemahan Indonesia bila dikutip.
6. Jangan akses repositori lain, jangan mengubah adaptive player / classifier / policy / Story Mode runner / readiness gate. Tidak ada aset privat yang dimasukkan ke Git atau artefak.



## Kelanjutan wajib setelah checkpoint 28 Oktober 2026
Jangan mengulang uji Step 9 #40606159061 (sudah 7/7 RNG, 8/8 helper negative-a0, 16/16 accessor). Lanjutkan audit statis dari [matriks live reconciliation](STEP4_10_LIVE_RECONCILIATION_2026-10-27.md). Prioritas teknis: validasi batas caller/callee dan lifecycle seed Step 4 tanpa gameplay; perluas cakupan Ghidra terarah untuk kandidat resource/Step 5; tutup pointer/alias dengan CFG-aware trace atau nyatakan blocker Step 6(b); petakan loader hanya bila jalurnya dapat ditunjukkan statis tanpa gameplay; Step 8 jangan memberi label pada mekanika yang belum terbukti. Jangan jalankan pemain otomatis, workflow monitor gameplay, input tombol, restore savestate, atau emulator. Latest code-test commit `7f234820f1b83a34654e900592903678365006a5`; latest verified run `#40606159061`, artifact `#12779814671`. Story Mode TIDAK TERBUKTI TAMAT.
