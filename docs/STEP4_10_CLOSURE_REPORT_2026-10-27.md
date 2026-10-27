# CHECKPOINT TERBARU — Step 6 extended scan, 27 Oktober 2026 19:35 WIB

Latest audited field scan: [Actions #40504640855](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504640855), completed success 19:34:31 WIB. Text-only artifact [#12733854252](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504640855/artifacts/12733854252), 220,128 bytes, ZIP SHA-256 `90288a1c8b454cbdc45c75e0244d26508628ecf88bfe8e73ed88524c8cb80891`. Latest runner-only audit [#40504977322](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504977322) succeeded 19:35:51 WIB and validated its artifact metadata/digest; artifact [#12734840847](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504977322/artifacts/12734840847), 25,756 bytes, ZIP SHA-256 `d022b23548fe95eb34bfbb7a7fb0dd190a498ca54fff11516818138701920398`; `RUNNER_ARTIFACT_CLEANUP=PASS`.

## Step 6 direct operand findings — verified statically in hypothetical entry-1 view

The scan covers 98,357 Ghidra-decoded instructions with direct base-plus-displacement load/store syntax in the candidate DATA.BIN entry-1 view. The inventory of recognized direct-memory displacements was emitted between explicit BEGIN/END markers; the runner audit shows the full inventory output stayed below its 30,001-line cap. For the four priority displacements, output cap is explicitly NONE.

- `+0xB30`: total 1 direct-memory access, 1 read, 0 writes.
- `+0xB38`: total 1 direct-memory access, 1 read, 0 writes.
- `+0xB40`: total 1 direct-memory access, 0 reads, 1 write.
- `+0xB44`: total 2 direct-memory accesses, 1 read and 1 write.

The previously inspected instruction window is consistent: `0x8012C634 lw v0,0xB30(a0)` bytes `30 0B 82 8C`; `0x8012C638 lw v1,0xB38(a0)` bytes `38 0B 83 8C`; `0x8012C640 addu v0,v0,v1` bytes `21 10 43 00`; `0x8012C644 sw v0,0xB40(a0)` bytes `40 0B 82 AC`. The +0xB44 write/read include `0x8012C604 sw zero,0xB44(v0)` and `0x8012CB14 lw a2,0xB44(v1)`, with the read value forwarded to call `0x8001B364`.

**Batas penting:** base `0x800D0000` is still HIPOTESIS, not runtime-validated. This closes the direct base+displacement inventory only for recognized instructions decoded by Ghidra in this candidate view. The bounded base-register trace follows a linear window up to 24 prior instructions per link and only simple `move` aliases, stopping at control flow; it is not whole-program pointer analysis. Computed addresses, aliases beyond the bounded trace, split immediates, indirect writes, undecoded code and alternate bases remain UNKNOWN. Do not map these offsets to Chakra, cost, turn, barrier or level-up. Some Ghidra function decompilations still fail from bad instruction/P-code boundaries. Therefore Step 6 remains SEBAGIAN; field semantics/full alias closure are not complete.

No gameplay/emulator run, gameplay input, savestate restore or private binary upload was performed in these scan/audit runs.

---

# REKONSILIASI LIVE DAN MATRIKS CLOSURE PER-KRITERIA — 27 Oktober 2026, 19:22–19:24 WIB

Bagian ini merupakan checkpoint otoritatif terbaru dan menggantikan status operasional historis di bawah bila bertentangan. Branch main pada checkpoint audit sebelum pembaruan laporan adalah commit 555b84a4d178b41e4d04705e1700104bd41ed1d3. Tidak ada gameplay/emulator dijalankan, input gameplay dikirim, savestate dipulihkan, atau sistem pemain adaptif disentuh selama audit ini.

## Provenance run dan artefak

| Sumber | Hasil aktual | Artifact, ukuran, SHA-256 ZIP | Batas |
|---|---|---|---|
| [Ghidra run #40498208067](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498208067) | success, selesai 19:14:42 WIB; indeks 1.206 baris fungsi EXE, 1.555 entry-1, 38 entry-0 | [#12732952776](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498208067/artifacts/12732952776), 2.255.170 byte; 6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6 | Audit #40503223693 memverifikasi metadata dan digest. Log entry0 346.593.927 byte di-hash tetapi tidak dibaca. Entry0 base 0x800AD000 dan entry1 base 0x800D0000 belum divalidasi runtime. |
| [Step 6 scan #40500058788](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40500058788) | success, selesai 18:59:18 WIB; 98.357 instruksi entry-1 terdekode dalam view hipotetis | [#12731474756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40500058788/artifacts/12731474756), 180.174 byte; 4aea20e1420292505666f15898ba2db57a875a4fc67fbe2c65336af0a16fc9f4 | Metadata/digest diverifikasi runner; STEP6_PRIVATE_CLEANUP=PASS; private_binary_in_artifact=no. Scanner dibatasi exact 16-bit immediate, batas 200 match/offset, dan tak mencakup penuh pointer arithmetic, split immediates, alias atau kode tak terdekode. |
| [Runner-only artifact audit #40503223693](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40503223693) | success, selesai 19:22:30 WIB | [#12733512950](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40503223693/artifacts/12733512950), 13.079 byte; 382773f9a421835bc97c448c630a2ea5d3891309bb34094f5a67027548c03414 | Raw log: semua field metadata (artifact_id, workflow_run_id, name, digest, size, expiry) PASS untuk tiga artefak, zip_sha256_verified_before_read=yes, raw_artifacts_or_game_binaries_uploaded=no, RUNNER_ARTIFACT_CLEANUP=PASS. |
| [Helper/callback audit #40499270568](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499270568) | success | [#12731593532](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499270568/artifacts/12731593532), 11.672 byte; 8567a5cad2a00823302ea7b361dd9b6eaab736bce6b77cf51ea136d6bee454b3 | STEP4_HELPER_PRIVATE_CLEANUP=PASS; text_only_output_validation=PASS; executable tidak di-upload. |
| [Step 5 Ghidra/m2c #40449144521](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40449144521) | success | [#12710000931](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40449144521/artifacts/12710000931), 926.540 byte; b2fdb6dc3213137e98e0ed298402e1d4b02198ed5310f264780bd8e965246b08 | Empat pasang output C tersimpan; bukan bukti source asli atau semua fungsi. |
| [Step 9 isolated RNG #40474891838](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474891838) | success | [#12720127454](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474891838/artifacts/12720127454), 3.201 byte; bcbfcd77a532ce34334ed60f720fdeaac566308bf2e6e4d54a7e60f28a5f083b | 7/7 vektor, state dan v0 sesuai, sentinel tercapai 12 instruksi per vektor, cap 128, RAM fisik PS1 2 MiB; hanya 0x80035D78. |
| [Step 7 coldboot loader probe #40484548650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650) | success, bounded no-hit | [#12724961702](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650/artifacts/12724961702), 3.960 byte; 27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71 | Target 0x800AD454 no-hit sampai frame 120; timeout 35 detik/exit 124; cleanup PASS. Tidak ada bukti register/copy-size/buffer checksum runtime. |
| [Step 4 seed-setter probe #40485987817](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817) | success, bounded no-hit | [#12724933081](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817/artifacts/12724933081), 4.003 byte; 74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6 | Target 0x80035DA8 no-hit sampai frame 120; 35 detik/exit 124; cleanup PASS. Ada fallback-PC lama yang salah di summary; raw ready line menetapkan target sebenarnya. |
| [Step 4 roulette repeat #40474262267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267) | Bukti runtime historis, window/checkpoint terbatas | [#12719024236](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267/artifacts/12719024236), 2.187.882 byte; cec3404b38afbedbae151fc15e9ec66d9c019ff853e4703f8813acac7793bdf4 | 127 caller/state-before sequence setelah normalisasi frame dan final state 0xA99DC6E7; caller tidak disambungkan secara kausal ke hasil roulette independen. Jangan unduh ulang atau buat artefak screenshot privat baru. |

## Matriks closure resmi per kriteria

| Kriteria | Status | Bukti dan digest | Batas dan pekerjaan minimum yang belum selesai |
|---|---|---|---|
| 4(a) Generator, state RAM, origin/lifecycle seed | SEBAGIAN | Ghidra #40498208067 artifact #12732952776 SHA 6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6; runner audit #40503223693 SHA 382773f9a421835bc97c448c630a2ea5d3891309bb34094f5a67027548c03414 | Statis: 0x80037B58 reset 0x80066E7C; 0x80037BB0 increment/store; 0x80037138 pada a0 negatif dapat mengembalikan global. Callsite entry0 melewatkan return ke 0x80035DA8 hanya pada base hipotetis 0x800AD000. Belum ada mapping/order runtime atau nilai $a0/$v0/$ra yang tertangkap. Jangan mengulang no-hit yang sama tanpa hipotesis reachability baru. |
| 4(b) Determinisme, wait/input, visible result | SEBAGIAN | Report out/step4/STEP4_RNG_RUNTIME_RESULT_2026-10-27.md; run #40474262267 artifact #12719024236 SHA cec3404b38afbedbae151fc15e9ec66d9c019ff853e4703f8813acac7793bdf4 | 127 sampel caller/state cocok setelah normalisasi, final state 0xA99DC6E7, viewport crop identik dalam window itu. Frame terminal berbeda 167/169/171; hubungan causal ke hasil roulette belum dibuktikan secara independen. |
| 4(c) Direct/indirect callers, JT, decompressed path | SEBAGIAN | Ghidra artifact #12732952776; runner artifact audit #12733512950 | Main EXE direct-JAL map tersedia; entry0 5 raw JAL candidates, 3 validated; entry1 144 raw candidates, 108 decoded direct calls, 36 raw-only. Indirect/JT paths, runtime base/reachability, code unpacked/decrypted remain. |
| 4(d) Roulette and battle callers | SEBAGIAN; battle BLOCKED | Run #40474262267 dan Step4 trace | Roulette call evidence terbatas; belum ada battle checkpoint/caller trace atau bukti caller-ke-hasil roulette secara causal. Minimum: battle checkpoint autentik dan bounded caller/state trace. |
| 4(e) Alternative RNG/randomness | SEBAGIAN | RNG signature/caller report dalam artifact #12732952776 | Signature scan tidak menyingkirkan table/frame/time RNG, algoritme lain, indirect call atau code hasil decompress/decrypt. Perlu sweep statis terarah berikutnya. |
| 5) Four selected functions | TUNTAS dalam batas 4 fungsi | #40449144521 artifact #12710000931 SHA b2fdb6dc3213137e98e0ed298402e1d4b02198ed5310f264780bd8e965246b08; report out/step5/STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md | Ghidra/m2c output 4/4 pasang, m2c exit 0, tokens/callsite cocok untuk 0x80015ADC, 0x80015B7C, 0x8001A328, 0x80020BF4. Bukan validasi seluruh fungsi game. |
| 6(a) Direct read/write and raw bytes | SEBAGIAN | Step6 #40500058788 artifact #12731474756 SHA 4aea20e1420292505666f15898ba2db57a875a4fc67fbe2c65336af0a16fc9f4; internal field-offset-scan.txt 1.323.122 byte SHA 6a6f7fb53b948dbb1a3d71f4fe2469a2edfae4cce73bb13a55684f8305320a9d | Under hypothetical base 0x800D0000: 0x8012C634 lw v0,0xB30(a0), bytes 300B828C; 0x8012C638 lw v1,0xB38(a0), bytes 380B838C; 0x8012C640 addu, bytes 21104300; 0x8012C644 sw v0,0xB40(a0), bytes 400B82AC. Also +0xB44 zero-store at 0x8012C604 and load at 0x8012CB14 forwarded in a2 to 0x8001B364. |
| 6(b) Full alias/effective-address/all-reader-writer inventory | BLOCKED pending wider static sweep | Artifact #12731474756 and audit #12733512950 | Scanner exact immediate only; cap 200 per offset; misses aliases, pointer/split-immediate address builds, undecoded code and alternate bases. Need uncapped complete memory operand sweep, address-construction tracking, raw-disassembly review and report of any truncation. |
| 6(c) Caller/callee/dataflow to game semantics | SEBAGIAN | docs/STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md; #12731474756 | Store and argument flow exist but object meaning and any cost/barrier/turn/level-up effect not proven. |
| 7(a) Static loader/resource directory/copy | SEBAGIAN | Ghidra #40498208067 artifact #12732952776; docs/STEP7_LOADER_OVERLAY_MAPPING_2026-10-27.md | Directory/copy candidates supported statically; base/relocation/load-unload lifecycle, DATA2.BIN/DUMMY.BIN not mapped end-to-end. |
| 7(b) Runtime mapping/copy size/source/destination/checksum | BLOCKED by bounded no-hit | #40484548650 artifact #12724961702 SHA 27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71 | No-hit 0x800AD454 through frame120; no register, copy size or buffer checksum. Minimum: new statically justified reachable PC, one breakpoint, coldboot/no input/no restore, strict timebox, output register/copy/checksum text only, then cleanup. |
| 8(a) Function semantics supported by caller/callee/raw MIPS | SEBAGIAN | docs/STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md; #12732952776 | LCG, callback counter, selected target compares and stores supported statically. Some decompilation has bad instruction/control-flow boundaries; transition function semantics unknown. |
| 8(b) Actual game-rule table: costs/barrier/upgrade/battle/roulette/turn/cards/victory | BLOCKED for unsupported labels | Step8 report and Step4 runtime report | Current assembly does not prove these rule names. Need independent caller/callee/dataflow and state/result corroboration per rule. No field may be named Chakra/cost/barrier/turn/level-up without independent evidence. |
| 9) Isolated function execution | TUNTAS only for 0x80035D78 | #40474891838 artifact #12720127454 SHA bcbfcd77a532ce34334ed60f720fdeaac566308bf2e6e4d54a7e60f28a5f083b; report out/step9/STEP9_UNICORN_RESULT_2026-10-27.md | 7/7 vectors, state/v0 correct, return sentinel 12 instructions, cap 128, 2 MiB physical PS1 RAM. Does not cover other functions or full emulator/game results. |
| 10) Auditable closure matrix: each criterion has source, artifact, digest, test, limitations and next task | TUNTAS as matrix only | This matrix and runner audit #40503223693 artifact #12733512950 SHA 382773f9a421835bc97c448c630a2ea5d3891309bb34094f5a67027548c03414 | Table gives evidence or a named blocker per criterion. Steps 4/6/7/8 remain partial/blocked; Step10 is not blanket closure of the whole game and must be refreshed for new evidence. |

**Kesimpulan:** Step 4 SEBAGIAN; Step 5 TUNTAS hanya untuk empat fungsi; Step 6 SEBAGIAN (inventaris alias lengkap BLOCKED); Step 7 SEBAGIAN (bukti copy runtime BLOCKED); Step 8 SEBAGIAN (aturan tidak didukung BLOCKED); Step 9 TUNTAS hanya untuk 0x80035D78; Step 10 TUNTAS sebagai matriks closure yang diaudit, bukan penyelesaian reverse engineering seluruh game. Story Mode TIDAK TERBUKTI TAMAT.

---

# Laporan penutupan riset reverse engineering — Langkah 4–10

Tanggal: 27 Oktober 2026  
Repositori: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`  
Sumber kriteria: [Audit Reverse Engineering Langkah 1–10](REVERSE_ENGINEERING_AUDIT_STEPS_1_10_2026-10-27.md).  
Batas: laporan ini menutup hanya hal yang benar-benar didukung bukti. Status tiap langkah **TUNTAS**, **SEBAGIAN**, atau **BLOKIR** berdasarkan ruang lingkup dan kriteria; sukses satu Actions run tidak otomatis berarti seluruh langkah selesai.

## Ringkasan status

| Langkah | Status akhir | Cakupan yang benar-benar ditutup |
|---|---|---|
| 4 — RNG, seed, caller, determinisme | **SEBAGIAN** | Formula/state RNG diverifikasi statis dan fungsi utamanya lulus eksekusi terisolasi. Perbandingan runtime pada satu checkpoint roulette menunjukkan stream caller/state serta viewport sama untuk dua pengulangan dan satu jeda berbeda. Seed boot, hubungan caller ke hasil roulette, caller battle, dispatch menyeluruh, dan RNG alternatif tetap terbuka. |
| 5 — perbandingan Ghidra/m2c | **TUNTAS (empat fungsi terpilih)** | Empat fungsi yang sama mempunyai output Ghidra dan m2c; kedelapan output C disimpan permanen. Tidak mengklaim merekonstruksi kode sumber asli atau semua fungsi. |
| 6 — alamat, setter, xref dan call chain | **SEBAGIAN** | Full artifact #12719587873 verifies static stores `+0x2E9=0x3F`, `+0x2E5=0`, selector `+0x58B`, conditional `+0x5D2` codes in five entry-1 candidates, plus negate/clamp record `+0x04` and setter `0x8001387C` at `0x8011C0D0`. Scan #40488847927 checked 98,357 decoded entry-1 instructions for exact scalar immediates, with no hits for target offsets; it does not cover every effective memory displacement/alias and cannot prove non-use. Base `0x800D0000`, field meanings, `+0xB30/+0xB38/+0xB40/+0xB44` source/final writers and transition semantics remain UNKNOWN. [Step 6 review](STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md). |
| 7 — loader dan overlay | **SEBAGIAN** | Loader probe #40484548650 pada `0x800AD454` mencatat progress frame 120 tanpa hit; base/runtime copy/checksum/relokasi belum terbukti. Seed-setter probe terpisah #40485987817 (utama untuk Step 4(a)) menguji hanya `0x80035DA8`, juga tanpa hit sampai frame 120; report fallback PC run itu salah, tetapi raw ready line menetapkan target yang benar dan koreksi parser diverifikasi oleh #40486315324. Kedua run cleanup PASS; hasil no-hit bounded tidak membuktikan target tidak pernah berjalan. [Laporan Step 7](STEP7_RUNTIME_COLD_BOOT_RESULT_2026-10-27.md), [loader run](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650), [seed run](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817). |
| 8 — penjelasan fungsi dan aturan game | **SEBAGIAN** | Raw MIPS clarifies selected threshold branches, extra gates, delay slots and stores, but codes/fields do not identify gameplay semantics. Costs, battle/roulette/turn rules, card effects and victory conditions remain UNKNOWN. [Step 8 report](STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md).
| 9 — eksekusi fungsi terisolasi | **TUNTAS untuk fungsi RNG `0x80035D78` saja** | Eksekusi MIPS32 terisolasi berhasil pada tujuh state; state baru, register `v0`, dan return sentinel cocok. Bukan pengganti emulator PS1 dan tidak menggeneralisasi ke fungsi lain. |
| 10 — indeks dokumentasi `out/logic.md` | **TUNTAS sebagai indeks audit** | Indeks mengacu ke laporan dan bukti terkini serta mencantumkan UNKNOWN. Status ini tidak berarti semua aturan permainan telah selesai direverse-engineer. |

## Matriks kriteria dan bukti

### Langkah 4 — RNG dan caller

| Kriteria | Status | Bukti / artefak | Yang masih kurang |
|---|---|---|---|
| 4(a) Generator, rumus, state RAM, asal/lifecycle seed | **SEBAGIAN** | [Trace statis](STEP4_RNG_TRACE_2026-10-27.md); [uji fungsi terisolasi Step 9](../out/step9/STEP9_UNICORN_RESULT_2026-10-27.md); roulette #40474262267; cold boot seed-setter #40485987817; Ghidra static helper/callback evidence from run #40498208067, audited by #40503223693 | Seed-setter runtime probe tidak mendapat hit sampai frame 120. Koreksi delay-slot: `0x800AF2A8 li a0,-1` memberi argumen ke helper `0x80037138`; delay-slot `0x800AF2B0 move a0,v0` meneruskan return helper ke `0x80035DA8`, jadi argumen setter/state tersimpan belum diketahui. Ghidra run #40498208067 completed; helper/callback evidence is documented above and runner-verified by #40503223693. Seed/lifecycle dan seluruh writer/reseed path tetap UNKNOWN. |
| 4(b) Determinisme savestate/input/jeda, caller, viewport, hasil tampak | **SEBAGIAN** | [Runtime report](../out/step4/STEP4_RNG_RUNTIME_RESULT_2026-10-27.md); run [#40474262267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267), artifact [#12719024236](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267/artifacts/12719024236) | Repeat jeda 30 dan kontrol jeda 60 menunjukkan 127 panggilan sequence/caller/state-before yang cocok setelah normalisasi frame, sampel state sama, final state `0xA99DC6E7`, dan viewport crop sama. Frame capture terminal berbeda (167/169/171) dan caller belum dihubungkan ke hasil pemilihan roulette yang terlihat secara independen. |
| 4(c) Direct caller, pointer, jump table, dispatch, kode terdekompresi | **SEBAGIAN** | [Step 4 closure](STEP4_CLOSURE_2026-10-27.md); [Ghidra caller review #40455975408](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455975408); [scan signature](../out/step4_rng_signature_scan_2026-10-27.md) | Empat direct caller main EXE terdokumentasi; entry 0/1 raw call candidate sudah dipilah menurut status decode. Mapping base runtime hipotesis, reachability tertentu tidak pasti, beberapa boundary fungsi belum diketahui, dan scan pointer sempit tidak menyingkirkan seluruh indirect/JT/decompressed paths. |
| 4(d) Caller roulette dan battle | **SEBAGIAN** | Run [#40474262267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267) memakai checkpoint roulette yang diverifikasi | Callsite terlihat pada window roulette, tetapi hasil akhir roulette belum disambungkan kausal ke caller. Tidak ada checkpoint battle autentik yang digunakan dalam run ini; battle RNG caller UNKNOWN. |
| 4(e) RNG alternatif dan randomness non-fungsi | **SEBAGIAN** | [Raw LCG signature scan](../out/step4_rng_signature_scan_2026-10-27.md) dan [Step 4 closure](STEP4_CLOSURE_2026-10-27.md) | Scan mencakup file mentah yang disebut di laporan dan pola pengali/addend tertentu saja. Tidak menyingkirkan algoritme lain, tabel, frame/time-derived values, pointer call, atau kode yang didekompresi/dekripsi setelah loader. |

### Langkah 5 — perbandingan Ghidra dan m2c

**TUNTAS dalam batas empat fungsi yang terpilih.** Run [#40449144521](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40449144521), artifact teks #12710000931, menghasilkan output Ghidra C dan m2c C untuk `0x80015ADC`, `0x80015B7C`, `0x8001A328`, dan `0x80020BF4`. Empat pasang output tersedia pada [laporan Step 5](../out/step5/STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md). Kesesuaian dua decompiler meningkatkan keyakinan struktur kode, bukan bukti source asli atau semantic caller game.

### Langkah 6 — penulis memori, xref, call chain

**SEBAGIAN.** Sumber utama: [Step 6 semantic review](STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md), [artifact teks runner-only #12719587873](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136/artifacts/12719587873).
- Getter target `0x80012A70`: 8 xref terdekode pada address map kandidat; setter `0x8001387C`: 9; getter Chakra pemain `0x800138EC`: 16.
- Fungsi UI/penggambaran seperti `0x8012A9C4` dan `0x80137AD8` turut membaca target; karena itu getter xref tidak sama dengan caller kemenangan.
- `0x80112418` menunjukkan cabang pembandingan record/target dan kandidat panggilan transisi, tetapi dekompilasi transisi/batas fungsi bermasalah.
- Log runner yang telah ada menunjukkan `0x8011C0D0` menegasikan record `+0x04`, membatasi minimum ke `-9999`, lalu memanggil setter; kandidat threshold menulis `+0x58B` dan `+0x5D2` sebelum `0x800EF98C`. Ini adalah temuan statis pada base hipotetis, bukan semantik gameplay.
- Belum terbukti: pemetaan base entry 1 ke RAM runtime, seluruh pembaca/inisialisasi `+0x2E9/+0x2E5`, sumber final field/delta `+0xB30/+0xB38/+0xB40/+0xB44`, formula biaya, atau efek akhir transisi pada game.

### Langkah 7 — loader dan overlay

**SEBAGIAN.** Sumber: [laporan loader/overlay](STEP7_LOADER_OVERLAY_MAPPING_2026-10-27.md), [RESOURCE_CATALOG.md](../docs/RESOURCE_CATALOG.md), [OVERLAY_MAP.md](../docs/OVERLAY_MAP.md).
- Bootstrap DATA.BIN memuat 68 byte awal diikuti tabel direktori `0x2F00) byte dengan 1.504 entry (1.500 aktif).
- Instruksi sekitar kandidat `0x800AD454` mendukung salinan tabel direktori dari `0x800AD494` menuju `0x8006D830`, tetapi ini bukti statis.
- Base entry 0 `0x800AD000` dan entry 1 `0x800D0000` tetap HIPOTESIS; alamat muat nyata, relokasi, urutan load/unload, dan kontribusi executable DATA2.BIN/DUMMY.BIN belum dipetakan menyeluruh.


Catatan runtime final ada pada [laporan Step 7](STEP7_RUNTIME_COLD_BOOT_RESULT_2026-10-27.md). Parser frame memiliki regression fixture yang lulus. Run koreksi #40484548650 menghasilkan report lengkap: target probe mencapai frame 120 tanpa hit pada `0x800AD454`; no-hit dalam jendela observasi bounded tidak membuktikan target tak pernah berjalan.
### Langkah 8 — penjelasan fungsi dan aturan game

**SEBAGIAN.** Sumber: [laporan fungsi/aturan](STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md).
- TERVERIFIKASI statis: LCG, perilaku beberapa caller main EXE (indeks bounded/shuffle/filter-pick/struktur RNG), getter/setter Chakra utama, beberapa pembandingan record ke target, direktori resource.
- HIPOTESIS/UNKNOWN: makna kandidat pilihan, field record, pemicu mode, pending delta, transisi; formula biaya barrier/upgrade; aturan umum battle/roulette/turn, efek kartu, dan syarat menang per mode.
- Tidak ada fungsi yang dilabeli caller battle hanya berdasarkan alamat, nama default Ghidra, atau banyak pemanggilan.

### Langkah 9 — eksekusi MIPS terisolasi

**TUNTAS untuk fungsi RNG utama yang diuji.** Run [#40474891838](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474891838), artifact teks #12720127454, [laporan hasil](../out/step9/STEP9_UNICORN_RESULT_2026-10-27.md).
- Executable terverifikasi pada 385.024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
- Fungsi dijalankan pada alias fisik RAM yang sesuai, dengan 2 MiB RAM, state `0xA3118), return sentinel, serta batas maksimum 128 instruksi/vektor.
- Tujuh input state menghasilkan state baru dan `v0` yang tepat; tiap vektor kembali ke sentinel setelah 12 instruksi. `ISOLATED_RNG_FUNCTION_EXECUTION=PASS`, 7/7.
- Run pertama [#40474699863](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474699863) gagal 0/7 karena memory map KSEG virtual yang salah; diperbaiki pada sumber, dan run berikutnya berhasil. Private cleanup tercatat PASS.
- Batasnya: bukan emulator PS1, tidak menguji helper/caller/loader atau semua fungsi game; tidak menyimpulkan hasil roulette/battle.

### Langkah 10 — indeks dokumentasi

**TUNTAS sebagai indeks audit.** `out/logic.md` diperbarui untuk mengarah ke laporan ini, report per langkah, dan matriks status. Indeks tersebut memisahkan TERVERIFIKASI, HIPOTESIS, dan UNKNOWN; tidak mengklaim semua aturan gameplay sudah selesai.

## Temuan terverifikasi, hipotesis, dan UNKNOWN

### TERVERIFIKASI
- Header/ukuran/hash EXE yang dipatok cocok; Ghidra/m2c memproses empat fungsi terpilih.
- LCG utama: state update `(old × 0x41C64E6D + 0x3039) mod 2^32); output `(new >> 16) & 0x7FFF); fungsi MIPS yang sama lulus tujuh vektor terisolasi.
- Dalam window runtime checkpoint roulette: state awal pasca-restore, 127 hit, normalized caller/state stream, state akhir `0xA99DC6E7), dan crop viewport identik untuk tiga cabang. Bukti ini terbatas pada checkpoint/window tersebut.
- Direktori bootstrap DATA.BIN dan alur penyalinan tabel yang dijelaskan dalam laporan statis.

### HIPOTESIS
- Base RAM entry 0/1 `0x800AD000)/`0x800D0000).
- Label gameplay untuk sebagian caller/resource, semantics field record, pending amount, dan alasan branch masuk/keluar.
- Fungsi `0x80035DA8` sebagai seed setter yang dipanggil di jalur resource: bentuk instruksi dan static call candidate cocok, tetapi runtime boot lifecycle belum terbukti.

### UNKNOWN / BELUM TERBUKTI
1. Sumber seed saat boot dan seluruh lifecycle reseed, khususnya indirect/call via pointer/overlay.
2. Pemetaan runtime base/relokasi/lifecycle DATA.BIN entry, plus executable/decompressed code di DATA2.BIN dan DUMMY.BIN.
3. Caller tertentu yang secara kausal menentukan hasil roulette yang terlihat, serta runtime RNG caller pada battle dengan checkpoint autentik.
4. Seluruh jalur dispatch indirect/jump table dan RNG alternatif, termasuk berbasis tabel, frame/time, atau kode hasil dekompresi/dekripsi.
5. Makna field/kode `+0x58B`, `+0x2E9`, `+0x2E5`, `+0x5D2` meski store sudah diketahui; sumber operand/final writer `+0xB30/+0xB38/+0xB40/+0xB44`; biaya barrier/level-up/Chakra; aturan battle/roulette/turn; victory logic lintas mode.
6. Eksekusi terisolasi fungsi game selain rutin RNG yang diuji apabila diperlukan untuk pertanyaan fungsi tertentu.

## Perubahan Git yang relevan

- `481ee437d4704da6a10ac7cb9a1406dae5cef9c9` — perbaikan referensi artefak review Step 6.
- `601a7287ec018a66efa1a4160b2bd610ddc9e84a` — laporan semantic review Step 6.
- `0fe56c5f455c397cb012f3978b11bdab9ef7af4e` — laporan loader/overlay Step 7.
- `5b11cacacf56cd97a18c6a9ecd510059cc1639a4` — laporan fungsi/aturan Step 8.
- `85e02a8d717c68f9b3b8b1aa07cd4089eea39aa3` — laporan runtime Step 4 dari log mentah #40474262267.
- `e35ef26390b5c9477f195a7c030897fdde836a22` — retry penulisan laporan Step 4 saat concurrent main update.
- `6d332244607298154c51fbd3f16ff7718483e6b2` — koreksi physical RAM map Step 9.
- `3e5a814c1f277096c73d44804683499ad67de977` — laporan uji MIPS terisolasi Step 9.

SHA HEAD sesudah pembaruan audit/handoff terbaru perlu diambil dari branch `main` pada saat commit terakhir dicatat di `STATUS.md`/handoff.

## Status Story Mode dan batas keselamatan

**Story Mode: TIDAK TERBUKTI TAMAT.** Tidak ada ending autentik yang diverifikasi dalam riset ini. Run Step 4 memakai checkpoint roulette untuk pengamatan RNG; run Step 9 menguji satu fungsi CPU MIPS saja. Tidak ada adaptive-player workflow atau Story Mode otomatis dijalankan/diubah. Tidak ada classifier, kebijakan input, marker Revision65, atau readiness gate diubah. ROM/disc, BIOS, Memory Card, savestate, RAM dump, dan screenshot privat tidak disimpan di Git; screenshot Step 4 hanya berada pada artifact privat Actions dengan masa retensi terbatas. Runner Step 9 menghapus direktori privat setelah tes.

## Handoff berikutnya

Lihat [handoff Langkah 4–10](HANDOFF_REVERSE_ENGINEERING_STEPS4_10_2026-10-27.md). Prioritas adalah analisis tambahan yang dapat diuji dari artefak teks yang sudah ada, atau eksperimen diagnostik terpisah yang benar-benar diperlukan untuk melengkapi seed lifecycle, runtime base mapping, dan caller battle. Jangan mulai kembali sistem pemain adaptif atau mengklaim selesai lebih dari bukti.

## Addendum penutupan — audit statis dan diagnostik terbaru (27 Oktober 2026)

- Workflow parser Step 7: [#40484417534](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484417534) lulus setelah fixture membuktikan ekstraksi frame yang benar. Ini menguji parser, bukan loader game.
- Single-breakpoint experiment [#40484519812](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484519812) memberi bukti dari raw log: progress sampai frame 100, no-hit pada alamat kandidat, exit 124 dari timeout 35 detik, dan cleanup PASS. Laporan otomatis awal gagal karena syntax error Python, sehingga raw log lebih berwenang daripada ringkasan artefak run tersebut.
- Commit koreksi report assembler `8326c07f71caeab12924133b0812ec7e86b8b1f7` diverifikasi oleh #40484548650; artefak #12724961702 memuat no-hit pada `0x800AD454` dengan control max frame 60 dan cleanup PASS. Runtime seed setter [#40485987817](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817) juga sukses sebagai workflow tetapi tidak mendapat hit pada target tunggal `0x80035DA8`: raw progress frame 1–120, exit 124/35 detik, cleanup PASS. Artefak #12724933081 (4.003 byte; ZIP SHA-256 `74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6`) memiliki fallback PC yang keliru (`0x800AD454`) saat no-hit; source fallback diperbaiki dan divalidasi oleh #40486315324. Ini memperbaiki kualitas laporan, bukan membuktikan seed call atau loader/base runtime.
- Pseudocode Step 6 yang sudah ada memperlihatkan operasi negasi/clamp dan beberapa code store bersyarat, tetapi tidak memberi dasar baru untuk menamai mekanik. Step 6/8 tetap SEBAGIAN dan field delta `+0xB30/+0xB38/+0xB40/+0xB44` tetap UNKNOWN.

Matriks langkah final: Step 4 SEBAGIAN; Step 5 TUNTAS untuk empat fungsi terpilih; Step 6 SEBAGIAN; Step 7 SEBAGIAN; Step 8 SEBAGIAN; Step 9 TUNTAS hanya untuk fungsi RNG `0x80035D78`; Step 10 TUNTAS sebagai matriks closure audit per-kriteria saja. Story Mode TIDAK TERBUKTI TAMAT. Run single-breakpoint #40484548650 tidak menyediakan hit/PC/register/copy-size/checksum buffer yang diperlukan untuk menutup Step 7.

## Addendum penutupan — seed-setter probe dan parser fallback (27 Oktober 2026)

Run [#40485987817](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817) adalah cold boot bounded tanpa input/restore, hanya satu breakpoint pada kandidat `0x80035DA8`. Raw log: source checksum lulus; pra-uji frame 50; listener-only max frame 60; target progress frame 1–120 dengan `bp_hits=0`; timeout exit 124 setelah 35 detik; cleanup PASS. Artefak #12724933081, 4.003 byte, ZIP SHA-256 `74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6`. Karena tidak ada hit, tidak ada register `$a0/$ra/caller` runtime. Summary fallback PC pada artefak salah menyebut alamat loader lama; raw `STEP7_SINGLE_BP_READY` membuktikan target yang benar ialah `0x80035DA8`. Fallback dikoreksi pada `a6734d7fc57ff6dfab9b8135cd5661bf0278c437`, dan [validator #40486315324](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40486315324) menguji fallback/parser. Kriteria Step 4(a) tetap SEBAGIAN; Step 7 tetap SEBAGIAN; tidak ada bukti Story Mode tamat.

## Addendum — raw MIPS cross-check, independent of runtime blocker (27 Oktober 2026)

Artifact teks #12719587873 dari [Actions #40473737136](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136), ZIP SHA-256 e1ea68c92bcbf645fde3c991c8a47192b815987d8044f2d599c163c1f3ec9fb9, telah diperiksa langsung. Artifact memuat dekompilasi dan raw instruction windows DATA.BIN entry 1, offset 0x10BB000, ukuran 596.412 byte, SHA-256 entry 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a. Gameplay/emulator tidak dijalankan. Base entry-1 0x800D0000 tetap hipotetis.

- **TERVERIFIKASI-STATIS, bersyarat pada base tersebut:** site 0x80111228/0x801112CC/0x801113B4/0x801114F0/0x80111588/0x80112418 menghitung record stride 0x90, memanggil getter target 0x80012A70, membaca field +0x04, dan mengarahkan record_word < target ke 0x8011253C. Detail delay slot dan gate ada pada laporan Step 6.
- Store pada jalur tertentu mencakup +0x58B, +0x2E9, +0x2E5 dan halfword +0x5D2. Nilai +0x5D2 yang dilaporkan oleh dekompilasi bervariasi (0x200, 8, 4, 0x20, 0, 0x1000), bukan nama aturan. Di site 0x80111228, raw window berakhir sebelum store +0x5D2; nilai 0x200 hanya diklaim pada tingkat dekompilasi.
- 0x8011C0D0 secara kondisional menegasikan word record +0x04, menjepit hasil ke minimum -9999, menyimpannya, lalu meneruskan nilai/index ke setter main EXE 0x8001387C. Ini tidak menjelaskan apakah nilai itu biaya, pengembalian, sinkronisasi atau delta sementara.
- **UNKNOWN/BELUM TERUJI:** base/relocation runtime, arti branch code/transisi, seluruh pemakai +0xB30/+0xB38/+0xB40/+0xB44 dan hubungan kausal dengan gameplay yang terlihat.
- Koreksi Step 4 terpisah: callsite 0x800AF2AC → 0x80035DA8 memasukkan return helper 0x80037138 melalui move a0,v0 di delay slot JAL. Nilai -1 merupakan argumen helper, bukan input setter terverifikasi; return helper tetap UNKNOWN.

Status tetap Step 4 SEBAGIAN; Step 5 TUNTAS untuk empat fungsi terpilih; Step 6 SEBAGIAN; Step 7 SEBAGIAN; Step 8 SEBAGIAN; Step 9 TUNTAS untuk RNG utama saja; Step 10 TUNTAS sebagai matriks closure audit per-kriteria saja. Story Mode **TIDAK TERBUKTI TAMAT**.

## Addendum — audit delay-slot MIPS dan caller setter (27 Oktober 2026)

Bukti MIPS entry-0 pada base hipotesis `0x800AD000` memperlihatkan `jal 0x80037138` di `0x800AF2A4`, delay-slot `li a0,-1` di `0x800AF2A8`, lalu `jal 0x80035DA8` di `0x800AF2AC` dengan delay-slot `move a0,v0` di `0x800AF2B0`. Maka `-1` masuk ke helper, sedangkan setter menerima nilai balik helper. Klaim lama bahwa setter otomatis menerima `-1`/menulis `0xFFFFFFFF` ditarik kembali. `tools/ghidra/ExportRngCallerAnalysis.java` sekarang mengekspor helper `0x80037138` dan xref-nya; run statis #40487406384 belum selesai pada saat addendum ini ditulis. Jangan ubah status Step 4(a) dari SEBAGIAN sampai return/helper path dapat dibuktikan.

## Addendum — lebih rinci untuk candidate 0x8011C0D0 (27 Oktober 2026)

Dekompliasi terarah pada body fungsi kandidat berukuran 408 byte (base entry-1 hipotetis 0x800D0000) menyatakan: input dibatasi ke byte, dibandingkan dengan global efektif 0x80139F70, dan fungsi return dini jika nilainya sama; jika berbeda, global serta field base+0x618 diperbarui. Input nonzero memilih record dengan indeks global 0x8013EA88, menulis 8 di record+0x22, lalu mengiterasi jumlah peserta dari global 0x8013EA71. Untuk setiap record ber-stride 0x90, word +0x04 dinegasikan, dijepit minimum -9999, disimpan, lalu dikirim bersama indeks ke setter 0x8001387C. Perbandingan signed short base+0x10 plus unsigned short base+0x14 terhadap 0x101 memilih call 0x8003F5D0 atau store base+0x94A=1; 0x800F96A4 dipanggil pada jalur tertentu. Raw instruction window yang tersimpan hanya memuat awal fungsi sampai sekitar 0x8011C118, jadi rincian loop berasal dari dekompilasi, bukan seluruh raw listing. Caller, nilai runtime, dan makna transaksi belum dikenal; tidak ada dasar untuk menamai pola ini harga barrier/level-up. Field +0xB30/+0xB38/+0xB40/+0xB44 tidak dilacak menyeluruh. Step 6/8 tetap SEBAGIAN.


## Live checkpoint addendum — 27 Oktober 2026 17:26 WIB

Remote `main` was verified at `2ad2c8dcdcaeee718d656e8696d6853f48ec54a8` before the handoff refresh commit. Ghidra static run [#40487406384](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40487406384) is a historical snapshot superseded by the current live checkpoint at the top: Ghidra #40498208067 completed success at 19:14:42 WIB and its artifact was audited by #40503223693. The previous full Ghidra run took about 39m43s; this is only a historical reference, not a dependable ETA.

The new Step 6 detail for candidate `0x8011C0D0` is bounded decompiler evidence: input byte normalization, compare/update of global `0x80139F70`, record stride `0x90), negate/clamp/store of record word `+0x04`, and calls to setter `0x8001387C`. It does not establish cost/refund/transaction semantics because caller and runtime values are unknown and the raw instruction window does not cover the full loop. Candidate fields `+0xB30/+0xB38/+0xB40/+0xB44` still require whole-program access analysis. Overall statuses remain unchanged; Story Mode is not verified complete. No adaptive player, gameplay input, or savestate restore was run.

## Live audit checkpoint — 27 October 2026, 17:24 WIB

- Re-read the live `main` files and verified that the current commit before this checkpoint was `2ad2c8dcdcaeee718d656e8696d6853f48ec54a8`. GitHub connector does not expose a local working-tree status; no local clean/dirty claim is made.
- Re-fetched raw job logs and metadata for Step 7 run [#40484548650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650). Job `coldboot-loader` completed `success`; asset provenance in the log confirms disc label/ID `SLPS-03553 / SLPS03553` and BIOS `SCPH-7502 (EU)`. The observation logs show preflight frame 50, listener-only control max frame 60, target `0x800AD454` progress through frame 120 with `bp_hits=0`, and bounded timeout `124`. The report artifact is #12724961702, 3,960 bytes, digest `sha256:27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71`; raw job log explicitly confirms upload digest and `STEP7_PRIVATE_CLEANUP=PASS`. No breakpoint hit or register/copy-size/buffer-checksum evidence exists. The result remains a bounded no-hit, not proof the loader is absent or its base is known.
- Step 9 criteria/report review confirms the isolated-execution criterion is satisfied only for `0x80035D78`: 7/7 vectors, state and `v0` correct, sentinel return in 12 instructions, max bound 128, physical 2 MiB RAM alias. The criterion does not require an indiscriminate all-functions sweep; no extra probe is justified absent a specific new claim.
- Active Actions run: [#40487406384](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40487406384), job `Verify and analyze PS-X EXE` / `122132544196`, step 11 `Extract and analyze DATA.BIN entry 0 for external helper` is a historical snapshot superseded by the current live checkpoint at the top. The completed run is #40498208067; do not use #40487406384 as its live status.
- No adaptive-player/Story Mode workflow, gameplay input, savestate restore, classifier/policy/readiness-gate edit, or private asset commit was performed. Story Mode remains `TIDAK TERBUKTI TAMAT`. Remaining Steps 4, 6, 7, and 8 stay partial; Step 5 remains complete only for four selected functions; Step 9 only for the RNG routine; Step 10 is an index, not proof of complete game understanding.

## Addendum penutupan — hasil bounded field-offset scan Step 6

Run statis [#40488847927](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40488847927) memindai 98.357 instruksi terdekode dari DATA.BIN entry-1 dengan base hipotesis `0x800D0000`. Tidak ada exact-immediate scalar hits untuk target offsets; ini terbatas pada klasifikasi scalar immediates dan bukan complete scan atas memory displacement/effective address atau pointer aliases. Hasil no-hit tersebut tidak membatalkan dekompilasi yang sudah menunjukkan `+0x2E9/+0x2E5/+0x58B/+0x5D2` stores, dan tidak cukup untuk menyatakan `+0xB30/+0xB38/+0xB40/+0xB44` tidak dipakai. Status Step 6 tetap SEBAGIAN.

## Addendum penutupan — helper return dan pending-field static dataflow (27 Oktober 2026, bukti sampai 18:38 WIB)

Runner-only audit [#40497668341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40497668341) sukses pada 18:38:45 WIB; artifact #12730957210 9.014 byte, ZIP SHA-256 `695e36bf70237913c0f80c94f0d4100732c92dd8b78155da2ace90d189c5ee24`, raw cleanup PASS.

**Langkah 4:** raw MIPS dan dekompilasi fungsi `0x80037138` menyelesaikan sumber return untuk argumen `-1`: cabang negatif mengembalikan nilai global `0x80066E7C`. Delay slot `move a0,v0` pada callsite setter meneruskan nilai itu ke kandidat `0x80035DA8`. Ini kemajuan pada sumber dataflow, bukan bukti bahwa global diisi nilai tertentu saat boot atau bahwa caller benar-benar dipanggil di runtime. Step 4 tetap **SEBAGIAN**.

**Langkah 6:** `+0xB30` dan `+0xB38` dibaca dan ditambahkan sebelum store ke `+0xB40`; `+0xB44` diinisialisasi nol pada satu jalur, kemudian dibaca sebagai argumen `a2` bagi `0x8001B364`. Semua adalah fakta statis bersyarat pada entry-1 base `0x800D0000`, yang masih HIPOTESIS. Mapping runtime, alias/object identity, writer/source lengkap dan semantic effects belum ditutup. Step 6 tetap **SEBAGIAN**; Step 8 juga tetap **SEBAGIAN**.

Artefak sumber pemindaian Step 6: run #40493556711, artifact #12729156734, 180.128 byte, ZIP SHA-256 `c9ea5ef0552a0c80a70f0d3a758622a358509de2079e5954dac3ce0032426e93`. Run koreksi helper #40497723766 telah dimulai setelah fragmen duplikat pada workflow YAML dihapus pada commit `029fdfab8df55dd16001916f0f53b7abd073c334`; hasil akhirnya harus diperiksa terpisah.

## Addendum — sumber global return helper dan batas kriteria Step 4 (27 Oktober 2026)

Run helper statis [#40498231825](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498231825) success pada 18:43:58 WIB; artifact #12732006381 berukuran 9.058 byte, ZIP SHA-256 adfdb608af96dd95a7c7e74d9f8b117767aaffa817d0c7eb860757ead868d9ba; raw cleanup PASS dan text-only validation PASS. Runner-only audit terbaru [#40498386273](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498386273) success pada 18:44:35 WIB, artifact #12731327556 9.727 byte, ZIP SHA-256 7826480f41372d68ddf3f4b1dfe6d99f51bbbb5cd124eb5c3c6169870150ba5c, cleanup PASS. Artefak helper dan scan Step 6 diperiksa di runner.

Data xref memperluas fakta statis untuk global 0x80066E7C: loaded-image word 0, store nol di 0x80037B7C, increment-store di 0x80037BDC (preceded by addiu v0,v0,1 at 0x80037BD4), dan reads di 0x80037BB4, 0x8003719C, 0x80037204, 0x80037260, 0x800372C0, 0x80037324. Ini memperkuat bahwa helper return untuk input -1 berasal dari global yang diinisialisasi nol di image dan memiliki pola writer nol/increment. Tidak membuktikan urutan init atau nilai pada saat setter dipanggil.

Keputusan status: Step 4 tetap SEBAGIAN karena caller/initialization ordering dan runtime seed lifecycle; Step 6 tetap SEBAGIAN karena field semantics/base mapping; Step 7 dan Step 8 tetap SEBAGIAN. Step 5/9/10 tidak diubah.

## Addendum — callback-counter initialization path and helper-return source (27 Oktober 2026, 18:50 WIB)

Runner-only inspection [#40499154584](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499154584) completed `success` at **18:50:46 WIB**. Text artifact #12731114444: 11,783 bytes; ZIP SHA-256 `d1538c727c5945003d74a4ff7185c168068738bb854eafb61b36a52c348677d5`; raw log says `RUNNER_ARTIFACT_CLEANUP=PASS`. It validated metadata, run IDs, names, sizes, expiry and SHA-256 for the Ghidra index #12728867894, latest Step 6 scan #12729156734, and helper-function audit #12730814693, all inspected on runner. The helper artifact is from [#40499029428](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499029428), size 11,051 bytes, ZIP SHA-256 `abc53716169d19173ee68f9f033fdc14d87e99835f9febbef453e46628fddc07`; raw log records asset checksum checks OK, `STEP4_HELPER_PRIVATE_CLEANUP=PASS`, `text_only_output_validation=PASS`, and `uploaded_input_executable=no`.

### Facts from raw MIPS / static call references
- `0x8003755C` has an initialization guard based on word/halfword location `0x80065DB4`; if nonzero it returns without re-running the setup path. On the zero path, its code executes `jal 0x80037B58` at `0x800375F0`; the delay-slot instruction `sh v0,-0x3c(s0)` at `0x800375F4`, with `s0 = 0x80065DF0`, stores `1` to `0x80065DB4` before entering `0x80037B58`. Thus the guard is set as part of a one-time initialization path.
- `0x80037B58` writes `0x100` through the pointer loaded from `0x80066E80`, zeros global `0x80066E7C`, calls `0x80037C48(&0x80066E5C, 8)`, then constructs `a1 = 0x80037BB0` and calls `0x800373F8` with delay-slot `clear a0`. The static argument flow into that dispatcher is `a0=0, a1=0x80037BB0`.
- `0x800373F8` loads a function pointer through the global pointer at `PTR_PTR_80066E3C + 8` and invokes it with `jalr`. This makes “register callback” a strong hypothesis for the call from `0x80037B58`, but the pointed-to routine itself remains indirect and has not been semantically verified.
- `0x80037BB0` reads `0x80066E7C`, increments it, stores it back, then iterates over eight slots beginning at `0x80066E5C`, calling each nonzero slot by `jalr`. This and the zero-store in `0x80037B58` support describing `0x80066E7C` as a **callback-count/tick-like global** from static behavior, not as a verified gameplay field or seed value.
- Incoming reference evidence: `0x80037B58` has a direct JAL caller at `0x800375F0` in `0x8003755C`; `0x80037BB0` is passed as a function-pointer argument from `0x80037B8C`, not called by a direct JAL at that site. `0x8003755C` itself has a computed-call reference from `0x800373E0` in `0x800373C8` plus a data reference from `0x80066E28`.

### Boundary for Step 4
The helper `0x80037138` with input `a0=-1` returns current global `0x80066E7C`; candidate DATA.BIN entry-0 callsite `0x800AF2AC` passes that return through the setter's delay slot `move a0,v0`. It is now statically supported that this value can come from a zero-initialized and subsequently incremented callback-like counter. However, the order of the entry-0 callsite relative to the initializer/callback path is not established, entry-0 base `0x800AD000` remains HIPOTESIS, and no runtime value at the setter was observed. **Step 4 remains SEBAGIAN**; do not report a verified boot-time seed or a seed-lifecycle closure from this evidence alone.

Historical status superseded by live check: Ghidra run #40498208067 completed success at 19:14:42 WIB; artifact #12732952776 digest 6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6; runner audit #40503223693 validated it.

## Addendum — dispatcher and callback-table static trace (27 October 2026, 18:54 WIB)

Runner-only audit [#40499569324](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499569324) completed success at **18:54:03 WIB**. Text artifact #12731359299 is 12,452 bytes, ZIP SHA-256 `f37812b2932e9743bacc6311cca038a23c0725c3cacf7e4b8a25fdd26079caf6`; raw log records `RUNNER_ARTIFACT_CLEANUP=PASS`. It validated metadata, run ID, name, size, expiry and digest for helper artifact #12731593532 from run [#40499270568](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40499270568): 11,672 bytes, ZIP SHA-256 `8567a5cad2a00823302ea7b361dd9b6eaab736bce6b77cf51ea136d6bee454b3`. That source run had `STEP4_HELPER_PRIVATE_CLEANUP=PASS`, `text_only_output_validation=PASS`, and `uploaded_input_executable=no`. All artifact bytes were processed on the GitHub Actions runner.

### Additional raw-MIPS findings
- Function 0x80037C48 zeroes a caller-supplied array for the number of 32-bit words passed in. Its caller 0x80037B58 passes base 0x80066E5C and count 8 (count is provided in the JAL delay slot), so the initialization path clears eight callback-pointer slots.
- Function 0x80037BB0 increments global 0x80066E7C and then visits eight words starting at 0x80066E5C, invoking each nonzero pointer with JALR. This is a concrete callback-list pattern.
- Function 0x800373F8 dispatches indirectly through the function pointer stored at PTR_PTR_80066E3C + 8. Its caller 0x80037B58 prepares a0=0 and a1=0x80037BB0 before this call, supporting—but not fully proving—the interpretation that 0x80037BB0 is being installed as a callback.
- Function 0x800373C8 dispatches indirectly through PTR_PTR_80066E3C + 0xC. Ghidra records a computed-call reference from 0x800373E0 to function 0x8003755C and a data reference at 0x80066E28; other callers also invoke this dispatcher. The initializer is therefore reached through an indirect dispatch path in the static view, not only through an ordinary direct JAL.
- Function 0x8003755C checks 0x80065DB4 and takes the initialization branch only when that guard is zero. Its call to 0x80037B58 at 0x800375F0 has delay slot SH v0,-0x3c(s0); because s0 is 0x80065DF0 there, this writes 1 to 0x80065DB4 before execution enters 0x80037B58. That function resets 0x80066E7C to zero, initializes the eight callback slots, then passes pointer 0x80037BB0 through the indirect dispatcher.

### Interpretation limits
The reset-then-increment behavior of 0x80066E7C is now **TERVERIFIKASI-STATIS** in the main executable. Its likely role as a callback/tick-like counter is a strongly supported inference from the indirect-dispatch table and eight-slot callback loop, not a verified gameplay-field name. The helper 0x80037138 with input a0=-1 returns the current value of that global. Therefore the candidate entry-0 callsite could pass this counter value to setter candidate 0x80035DA8 *if that callsite executes*. The relative runtime ordering of that resource callsite and the initialization/dispatch path is still unknown; entry-0 base 0x800AD000 remains HIPOTESIS, and no setter argument was captured at runtime. Step 4 remains **SEBAGIAN**.

Historical status superseded: Ghidra run #40498208067 completed success at 19:14:42 WIB; final artifact #12732952776 SHA-256 6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6 was verified by runner audit #40503223693.
