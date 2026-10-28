# HASIL FINAL SCAN STEP 6(b) — 28 Oktober 2026, 07:55 WIB

Hasil ini menggantikan catatan sementara “scan pending” yang muncul di bawah/versi sebelumnya. Run [#40611660635](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40611660635) **completed/success** pukul 07:55:13 WIB; job `122564387469`. Artefak teks [#12783307599](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40611660635/artifacts/12783307599), 244.577 byte, SHA-256 ZIP `748eadbfe82980bba8d2088d11affba4310d524eb871b6a34ee5fd43584f2892` cocok dengan digest GitHub. Ghidra scan, cleanup aset input privat, validasi output text-only, dan upload laporan lulus; `source_assets_removed_before_ghidra=PASS`, `private_binary_uploaded=no`.

Hasil baru:
- Exact XREF statis ke alamat numerik `0x8013A554`: **194** (192 READ, 2 WRITE; 74 entry fungsi unik diketahui dan 6 sumber tidak memiliki containing function).
- Dua writer yang terdaftar: `0x80127278` dalam fungsi `0x80127240` — `_sw v0,-0x5aac(s0)`; dan `0x80127364` dalam fungsi `0x8012733c` — `sw zero,-0x5aac(s0)`.
- Heuristik displacement `0xA554`: 200 kandidat load/store, 159 memiliki kandidat `lui reg,0x8014` sebelumnya dalam jendela 24 record instruksi. Ini bukan graph alias/provenance lengkap.
- Dalam view hipotetis entry-1 base `0x800D0000`, bytes pada `0x8013A554` adalah `70 00 B0 AF` (word little-endian `0xAFB00070`), terdekode seperti `sw s0,0x70(sp)`. Ini konflik code/data mapping atau base/relocation yang belum terselesaikan, bukan bukti pointer runtime.

Karena mapping tersebut belum tervalidasi dan trace masih heuristik, **Step 6(b) tetap BLOCKED**; 6(a)/6(c) tetap SEBAGIAN, 6(d) UNKNOWN. Tidak ada status Langkah 4–9 yang dinaikkan. Story Mode **TIDAK TERBUKTI TAMAT**. Tidak ada emulator/gameplay/input/savestate restore atau adaptive-player run yang dilakukan.

Laporan lengkap: [docs/STEP6_GLOBAL_POINTER_SLOT_AUDIT_2026-10-28.md](docs/STEP6_GLOBAL_POINTER_SLOT_AUDIT_2026-10-28.md).

---

# HANDOFF STATUS ADDENDUM — Step 6(b) scan pending, 28 Oktober 2026

Static scan [#40611660635](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40611660635) is currently `in_progress` on `main` commit `ea148ca60af2e3eeaa1b58141532e1ff5a98dd60`. Job ID `122564387469`; last visible step `Install disc extraction tools`; no artifact yet. Start 07:53:40 WIB; workflow timeout is 35 minutes, giving a deadline around 08:28:40 WIB, not a guaranteed completion estimate. Inspect this run and its text-only artifact/log when available. Do not rerun if it fails until the exact failure is understood. It is a static Ghidra scan; not an emulator/gameplay run and not an adaptive-player workflow.

# HANDOFF ADDENDUM — targeted audit 28 Oktober 2026

Checkpoint ini menambahkan [audit terarah Step 4–10](STEP4_10_TARGETED_AUDIT_2026-10-28.md). Awal sesi membaca HEAD `4b20564b38c895495755143b2aa777dc7ab6b5e5` pada `main`; sesudah audit dokumen diperbarui, periksa HEAD live sebelum tindakan berikutnya. Actions `queued=0`, `in_progress=0` pada query API; run #40606159061 sudah selesai.

### Bukti baru yang dapat digunakan

- Step 5 artifact #12739676233 SHA-256 ZIP `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d` dibuka langsung: empat direct JAL ke RNG pada main EXE tetap terkonfirmasi; disassembly mempunyai 156 mnemonic JALR, tetapi target dinamis belum dipetakan.
- Ada perbedaan batas yang harus diselesaikan sebelum klaim cakupan caller: output Ghidra fungsi `0x80015B7C` = 240 alamat, end-exclusive `0x80015C6C`; anotasi spimdisasm `nonmatching func_80015B7C, 0x580` memiliki label tambahan `0x80015C6C` dan rentang yang tampak berlanjut ke `0x800160FC`. Call di `0x80015BF0` nyata/terdekode, tetapi jangan menganggap span anotasi panjang sebagai body Ghidra tunggal.
- Step 6 artifact #12741234990 SHA-256 ZIP `7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9` dibuka langsung: pada view entry-1 hipotetis 98.357 instruksi terdekode, +B30 = 1 READ, +B38 = 1 READ, +B40 = 1 WRITE, +B44 = 1 WRITE dan 1 READ. Base `0x800D0000` dan pointer di slot `0x8013A554` tetap tidak tervalidasi.
- Tes Step 9 7/7 RNG, 8/8 helper negative-a0, 16/16 setter/getter tetap CPU/MIPS terisolasi dengan MMIO sintetis; jangan mengulang tes identik.

### Prioritas berikutnya

1. Selesaikan rekonsiliasi batas `0x80015B7C` dari raw MIPS/return/tail jumps dan metadata Ghidra yang sama; jangan menaikkan Step 5 sebelum itu serta cakupan fungsi diwajibkan lebih luas.
2. Untuk 6(b), telusuri pointer slot `0x8013A554`, semua readers/writers dan alias melalui CFG-aware def-use lintas blok/fungsi; pertahankan BLOCKED bila sumber alamat/relokasi terputus.
3. Step 7: jangan ulangi probe no-hit `0x800AD454`; hanya pilih breakpoint jika raw instruction dan reachability baru mendukung.
4. Step 4: JALR count bukan target/callgraph; perlu resolusi target dan bukti seed/helper runtime bila fasilitas yang tersedia memungkinkan tanpa membuat klaim dari no-hit.
5. Pertahankan seluruh matriks dan statuses. Tidak ada adaptive player, emulator gameplay, input ataupun savestate restore yang dijalankan pada audit ini; tidak ada komponen adaptive-player yang diubah. Story Mode tetap NOT COMPLETE / TIDAK TERBUKTI TAMAT.

---

# Handoff Chat Berikutnya — Riset Naruto PS1 Langkah 4–10
Tanggal: 28 Oktober 2026
Repo tunggal: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

## Checkpoint dan laporan utama
- Parent yang diaudit: 7df287bf4ca21f6c32fe2589bc09e8665e62e846.
- Laporan silang bukti: [docs/STEP4_10_CROSSCHECK_2026-10-28.md](STEP4_10_CROSSCHECK_2026-10-28.md).
- Status dan log: STATUS.md, ANALYSIS_LOG.md.
- Laporan kriteria: docs/STEP4_10_LIVE_RECONCILIATION_2026-10-27.md, docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md.
- Temuan teknis: docs/STEP4_RNG_TRACE_2026-10-27.md, docs/STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md, docs/STEP6_CFG_SSA_DATAFLOW_AUDIT_2026-10-27.md, docs/STEP7_RUNTIME_COLD_BOOT_RESULT_2026-10-27.md.
- Gate pemain adaptif: docs/ADAPTIVE_READINESS_NEXT_EVIDENCE_GATE_2026-10-25.md.

## Temuan yang jangan dikerjakan ulang tanpa pertanyaan baru
- Artefak #12739676233 SHA-256 ZIP 94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d mempunyai empat direct JAL ke RNG: 0x80015B14, 0x80015BF0, 0x8001A460, 0x80020C24.
- Artefak #12741234990 SHA-256 ZIP 7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9 menunjukkan B30/B38→sum→B40, dan B44 diinisialisasi nol serta dikirim ke 0x8001B364 pada branch B2A>=6; base 0x800D0000 hipotesis.
- Step 9 #40606159061 artifact #12779814671 SHA-256 ZIP dd3e559997ce0c9f931f330144de8021bdb3c75fa16b4f21717299c4b2d4d79f: 7/7 RNG, 8/8 helper negative-a0, 16/16 setter/getter dengan MMIO sintetis. Jangan ulangi tes yang sama.
- Jangan ulangi probe no-hit #40484548650 (0x800AD454) atau #40485987817 (0x80035DA8) tanpa hipotesis reachability statis baru.

## Gerbang wajib
- Hanya repo zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research; jangan akses/ubah repo Tile Duel atau repo lain.
- Tidak ada gameplay, input tombol, restore savestate, atau adaptive player dijalankan pada sesi sebelumnya.
- Dokumen gate tanggal 25 Oktober mewajibkan izin pengguna yang baru dan eksplisit sebelum operasi yang memulihkan state atau mungkin mengirim input; auto-review menolak percobaan ulang sejenis. Jangan cari jalan memutar.
- Tetap target cue UNKNOWN, barrier_level_selection=WAIT, adaptive readiness NO-GO, Story Mode NOT COMPLETE, Revision65 blob 3754a6ddf45a7570c053d9c149b6d80b0862a127, cue token absent.
- START hanya dipakai untuk dialog yang sudah dikalibrasi setelah gameplay benar-benar dimulai; jangan menggantinya dengan Circle atau directional input tanpa konteks yang terverifikasi. Mask kunai bukan bukti selector.
- Jangan masukkan ROM/BIN/CUE/EXE, BIOS, memory card, savestate, dump RAM atau screenshot privat ke Git/artifact. Hash/ref dalam dokumen bukan bukti file sudah dibuka.
- Monitor, lint, dan regression yang hijau tidak membuktikan progress permainan. Story Mode tidak boleh disebut tamat tanpa ending autentik terverifikasi.

## Prioritas
1. Audit caller boundary/reachability statis untuk 0x80035D78, 0x80035DA8, 0x800A3118 dan 0x80066E7C; jangan gunakan 0x800BDBFC sebagai caller/helper tervalidasi karena entry-0 Ghidra timeout dan referensinya nol.
2. Trace pointer CFG-aware dari global slot 0x8013A554 sampai access field +0xB30/+0xB38/+0xB40/+0xB44; catat batas provenance yang tak diketahui.
3. Step 7 hanya lanjut jika ada copy instruction reachable yang dipilih dari raw disassembly; selain itu pertahankan BLOCKED dan jangan ulang probe generik.
4. Step 8 hanya beri label aturan dengan code flow dan state/result autentik independen yang saling mendukung.
5. Pertahankan matriks 17 baris: Step 4 partial; Step 5 partial; Step 6(a,c) partial, 6(b) blocked, 6(d) unknown; Step 7(a) partial, 7(b) blocked; Step 8(a) partial, 8(b) UNKNOWN; label aturan unsupported tetap tidak dipromosikan; Step 9(a) tuntas hanya 7 vektor RNG, 9(b) partial; Step 10 tuntas sebagai matriks audit saja.


<!-- step4-step8-preset-list-shuffle-audit-2026-10-28 -->
## New evidence from 28 October

Read [`docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md`](STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md) first. Function `0x80015610` loads two lists for selector values <18, but helper `0x80015B7C` zeroes its incoming group arg and only shuffles first buffer `0x80070D0A`, 4*n swaps. The two templates at each selector are byte-identical; selectors 9–17 contain 64 zeros without `0xFF` and are therefore counted as length 64. This is proven static behavior; semantics of ID bytes and intent remain unknown. Next static task: trace all readers and consumers of the second list and connect selector bytes to parent descriptor fields without assigning guessed gameplay names.

Checkpoint restore was attempted twice with no controller input. Raw savestate load and sanitized-plus-BIOS rehydration both crash with `SIGSEGV`/exit 139 before `loadSaveState` returns or `SaveStateLoaded` fires. Rehydrated output hash exactly matches raw checkpoint, so stop repeating this load in the same environment. Use static research until a genuinely different state-format/loader hypothesis is justified. The source checkpoint remains private and was not overwritten.


## Descriptor selector note (same checkpoint)

The two direct callers of `0x80015610` pass field +2 from descriptors. Both audited tables only expose values 0–8; source blocks 9–17 are 64-byte zero blocks not selected by these table records, despite the loader guard permitting indices <18. Keep this limited to the two statically traced paths; don't claim global unreachability. Continue with the consumers/meaning of IDs selected by 0–8 and investigate the second buffer reader path. See [preset-list trace](STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md).


<!-- caller-id-random-insert-audit-2026-10-28 -->
## Caller/dataflow result to continue from

The latest evidence is in [`docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md`](STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md). Main-EXE direct JAL `0x80013B50→0x80015ADC` passes a byte returned by `0x800139FC(group,slot)`, which reads offset +0x0A from a `0x80070EA0)-based record (group <4, slot <3). That byte is range-checked against 52 entries; a pseudo-random position based on `byte[0x80070D02]` and RNG is computed, then the code shifts `0x80070D0A` order bytes, writes the ID to `0x80070C80+0x8A+position`, and increments the distinct count at `0x80070C82` if <64. Keep this static description literal; do not label as a card/deck/turn or infer runtime reachability. Next: identify all readers/writers and call/dispatch paths for `0x80070EA0`, `0x80070C80+0x8A`, `0x80070C82`, and the consumer of `0x80070D0A`, preferably from existing raw/static artifacts before proposing any new emulator experiment. Restore checkpoint remains NO-GO after repeated SIGSEGV; do not rerun same loader path.


<!-- four-record-three-slot-id-operations-2026-10-28 -->
## Latest detailed static behavior

Read the newest tail of [`docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md`](docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md). The `0x80070EA0)-based area is traversed as four records, stride `0xB4), with three adjacent IDs at `+0xA..+0xC`. The raw code body starting at `0x80013A48` adds a valid registry ID to the first invalid slot; the body at `0x80013B10` moves a chosen ID into the random-indexed shared structure, compacts source IDs, and sets the tail slot to `0xFF`. This is static behavior, not yet proven as cards or any named mechanic. Continue by tracing readers/writers of `0x80070C80+0x8A`, `0x80070C82`, and `0x80070D0A` and the dispatch/reachability of bodies `0x80013A48` / `0x80013B10`; do not start another restore run using the checkpoint that crashed twice.


<!-- sequence-pop-and-reshuffle-helper-2026-10-28 -->
## Sequence-shift finding

`0x80015768` saves the first byte from `0x80070D0A`, shifts the sequence left with helper `0x800158E8`, shuffles the configured length with `0x80015B7C`, and returns the saved byte. The shift changes `0x80070C82), not the preset length `0x80070D02`, and does not clear the tail. Treat as static only; next task is understand consumers and the relationship to `0x80070C80+0x8A`, not a guessed deck/roulette label. Latest trace: [preset/list behavior](docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md).


<!-- id-collection-consumer-trace-2026-10-28 -->
## NEW CHECKPOINT — ID collection and downstream consumer trace (28 Oktober 2026)

Detailed report: [`docs/STEP4_8_ID_COLLECTION_CONSUMER_TRACE_2026-10-28.md`](STEP4_8_ID_COLLECTION_CONSUMER_TRACE_2026-10-28.md), added in commit `50f7672e668e2c1983b01a1c0b9097bc7bfbdc6f`.

### What the new pass establishes

- Registry initialization in main EXE walks 16-byte records at `0x80055CEC), stops at the first-word `0xFFFFFFFF` at `0x8005602C` (index 52), and stores count 52; helper `0x800154D4` returns that count.
- `0x80070EA0) is four records of stride `0xB4); each contains three ID bytes at +0xA..+0xC. `0x80013A48` validates ID <52 and fills first slot whose current byte is >=52; fails if all three bytes are valid IDs.
- `0x80013B10` reads the selected ID, calls `0x80015ADC` to pass it through the random insertion path, compacts the record if source slot is 0/1, and sets the tail byte to `0xFF`.
- Counts/cursors are distinct: D02/D04 are configured lengths for list 0/1, D06/D08 are their load-reset cursors, C82 is a different halfword count changed by helpers, C86 is a cursor for the indexed buffer at C8A. Do not equate them.
- The helper family audited (`0x800158D8`, `0x800158E8`, `0x800159BC`, `0x80015B7C`) hardcodes its effective list group to 0. Loader 0x80015610 does copy two lists, but these operations mutate/shuffle only list 0 in the traced paths. Whether this asymmetry is intent or defect is UNKNOWN.
- In a hypothetical DATA.BIN entry-1 map (base `0x800D0000)), direct JALs at `0x800DD2B4` and `0x800DD4CC` reach `0x80013B10`. The surrounding Ghidra decompilation describes conditional checks on fields and values `0x14/0x15), then reads three IDs back and writes them to +0x10..+0x12 of an object record with stride 0x90, alongside other state writes. This is **conditional static cross-resource evidence only**: resource base/pointer slot is not runtime-validated and decompilation explicitly warns about bad instruction data/control-flow truncation.
- No ID labels or visible gameplay mechanic were established. Do not call the structure a deck/cards/character roster/turn order/barrier/tile until independent consumer evidence confirms it.

### Next productive task

1. Continue static reader/writer analysis around `0x80070C80+0x8A`, `0x80070C82`, `0x80070C86`, `0x80070D0A`, D02/D04 and D06/D08; identify the consumer that reads a returned ID and then changes a visible gameplay result, using only existing text artifacts.
2. Attempt ID-to-label mapping from verified string/resource tables if a permitted text-only artifact supports it; otherwise explicitly retain UNKNOWN.
3. Resolve resource loader/relocation/base and global pointer provenance before treating entry-1 callsites as runtime reachability. Step 6(b) stays BLOCKED and Step 7 runtime mapping stays UNKNOWN/BLOCKED.
4. Do not rerun the two identical savestate loads (both exit 139 before the load event), do not repeat the no-hit 0x800AD454 probe absent new reachability evidence, and do not run/edit adaptive player. Keep `barrier_level_selection=WAIT` and Story Mode **TIDAK TERBUKTI TAMAT**.

Current statuses remain: Step 4 partial; Step 5 partial; Step 6(a,c) partial, 6(b) BLOCKED, 6(d) UNKNOWN; Step 7 partial with runtime mapping blocked; Step 8(b) UNKNOWN; Step 9 tests complete only within previously stated isolated fixtures; Step 10 is an audit matrix only.


<!-- registry-numeric-field-consumer-2026-10-28 -->
## Follow-up audit — registry attributes have downstream numeric effects

The ID trace report was extended in commit `07f8b641f354b1ed90e92aedc6e194582c24e714`: [`docs/STEP4_8_ID_COLLECTION_CONSUMER_TRACE_2026-10-28.md`](STEP4_8_ID_COLLECTION_CONSUMER_TRACE_2026-10-28.md).

- The 52-row registry uses four numeric 32-bit words per record. Bounded accessors at `0x800154E0`, `0x80015578`, `0x8001552C`, and `0x800155C4` read offsets +0, +4, +8, and +0xC respectively (invalid-ID fallbacks differ).
- Raw data field +0 contains category-like integer codes used as branch discriminators in candidate resource code; +4 is 0/1/2 in the visible 52 rows; +8 contains signed/positive numbers (range -50..500); +0xC progresses 239..290. These are observed data shapes only; do not label them as character classes, costs, stats, or resource IDs yet.
- In candidate entry-1 routine `FUN_80115728`, accessor `0x8001552C` is used on the value at object offset +0x530. Its returned +8 value enters signed multiplication/negation, is stored in a group-indexed halfword at +0x2EE, and its sign selects byte +0x22 values 2/5 and follow-on functions. This adds a static data→numeric field→state branch link, but not a player-facing interpretation; base `0x800D0000) and pointer resolution remain unvalidated at runtime.
- Indexed-buffer readers/writer: `0x800157C4` reads C8A using cursor C86 without a visible bounds test; `0x80015808` checks index against low-byte D02 then reads C8A or returns FF; `0x80015858` uses the same length bound plus ID<52 before writing C8A.
- No direct JAL to `0x80013A48` was found in the available full main-EXE text disassembly. Body operation is verified locally; caller/reachability remains UNKNOWN.

Next focus should identify the semantic meaning of registry fields using their consumers or verified string/resource tables. Do not infer it from the numerical ranges. Continue to use only existing text artifacts; no runtime experiment is justified until the base/pointer/reachability gap is closed.


<!-- sequence-to-registry-dispatch-trace-2026-10-28 -->
## New static consumer chain — configured byte becomes an ID-driven state branch

Extended evidence is in [`docs/STEP4_8_ID_COLLECTION_CONSUMER_TRACE_2026-10-28.md`](STEP4_8_ID_COLLECTION_CONSUMER_TRACE_2026-10-28.md), latest detail commit `c37d73bd062c68cb12447ebd77a1d61d6385f15b`.

Reopened existing entry-1 raw disassembly artifact #12742268706 from run #40523020556; the local ZIP SHA-256 matches API digest `5f3f767667444f7c956c36fc59cf75b6bb90a5a1dde8ddb92fb69f9e0f797e81`. No game binary was downloaded and no emulator ran.

New chain, static only and conditional on hypothetical entry-1 base `0x800D0000):
- Entry-1 call sites `0x8010F3DC` and `0x8010F400` call main-EXE helper `0x80015768`, which saves the first byte at D0A, removes/shifts first entry, reduces C82, applies RNG swaps, and returns the saved byte.
- Caller stores the returned byte to object +0x530. On the branch where `D_80139EC7==0` and `0x8010D0F0()` returns zero, `0x800154E0` reads that ID's registry field +0; values <16 index jump table `jtbl_800AE900`.
- At branch destinations around `0x8010F464` and `0x8010F4E4`, registry field +8 is stored in object +0x4F4 (or both +0x4F0 and +0x4F4), and its sign sets/clears byte +0x534. A separate path at `0x80115708–0x801158AC` uses field +8 in signed multiplication, stores to +0x2EE, and tests sign to write 2 or 5 to byte +0x22 and choose a continuation.
- The three-byte sequence read path at `0x8010F1D4–0x8010F288` reads list indices 0,1,2, passes them to `0x800C7574`, and copies the bytes to object +0x4E0..+0x4E2. Return semantics for 0x800C7574 remain unknown.
- Raw entry-1 disassembly now establishes decoded direct JAL references to `0x80013A48` at `0x8010F8EC`, `0x8010F908`, `0x801107A8`; and to `0x80013B10` at `0x800D7104`, `0x800DD19C`, `0x800DD2B4`, `0x800DD4CC`, `0x800F78AC`, `0x800FA3D4`, `0x800FAA2C`, `0x80110798`.

This narrows the gap from “possible consumer” to **decoded direct call/dataflow in the static resource view**, but does not verify runtime reachability: resource base/relocation and global pointer provenance remain unclosed; the dispatch table at `0x800AE900` was not included in this entry-1 artifact. Do not name the features or result fields from these addresses alone.

Next: map `jtbl_800AE900` and its owning resource/table using only existing text artifacts if available; identify valid loader/relocation provenance; then compare field +0 branch cases and field +8 effects without renaming them prematurely. Step 4 remains partial, Step 6(b) BLOCKED, Step 7 runtime mapping UNKNOWN/BLOCKED, Step 8(b) UNKNOWN. Story Mode remains TIDAK TERBUKTI TAMAT; adaptive player/gates remain untouched.


<!-- jumptable-address-mapping-conflict-2026-10-28 -->
## New targeted test — 0x800AE900 is not a 16-word table in the entry0 base hypothesis

Added the targeted bounded dump to [`docs/STEP4_8_ID_COLLECTION_CONSUMER_TRACE_2026-10-28.md`](STEP4_8_ID_COLLECTION_CONSUMER_TRACE_2026-10-28.md), latest report commit `ada72c30b44fbd7e0cc1a4edbe9ae75d9a7d934a`.

The entry0 static table-dump run succeeded: Actions [#40619049176](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40619049176), artifact #12786995206, ZIP SHA-256 `01067b46e0a6e15cebd06d4bcd9898ff946d8c1d4083d40a29b80480fca92dc9`. Under the hypothetical `0x800AD000` base, address `0x800AE900) is offset `0x1900) inside entry0; its 64 bytes decode as MIPS instruction forms, including `JAL 0x80021140` and `JAL 0x80037138`, not as 16 plausible absolute pointers. The table-byte hash is `0b5987d2a6307848ab55e87b23f0771fe6afdc345f8c42ede9bfa92eb5ab005b`.

Therefore reject only this specific mapping assumption: the bytes at offset +0x1900 in entry0 **if** imported/mapped at `0x800AD000) cannot be taken as the 16-word table named by entry1. It remains unknown which module actually owns memory `0x800AE900) when entry1's dispatch runs. Entry1 still statically forms that address, adds `4*field0` (with field0 <16), loads a word, and executes `jr` through it. The address calculation is verified; table ownership/target map/runtime dispatch are not.

This result strengthens Step 7's load-base/overlay blocker; do not promote Step 6(b)/7 or label the 16 categories. Next: resolve which code/resource is resident at `0x800AE900) at the time the entry1 routine executes, using loader relocation/copy logic or a new static mapping artifact. No emulator, gameplay, savestate, or adaptive-player run was used.

<!-- cross-resource-pointer-jump-table-conflict-2026-10-28 -->
## Further mapping contradiction — entry1 addresses helpers at 0x800AD454 but 0x800AE900 contains code-like words in entry0 view

Detail added to [`docs/STEP4_8_ID_COLLECTION_CONSUMER_TRACE_2026-10-28.md`](STEP4_8_ID_COLLECTION_CONSUMER_TRACE_2026-10-28.md), latest blob `930fd9d253154add0a66db36012bc9db9620dcca`.

The entry1 static prefix at `0x800D0128..0x800D013C` stores six aligned words pointing to `0x800AD454`, `0x800AD45C`, `0x800AD464`, `0x800AD46C`, `0x800AD478`, and `0x800AD484`. Treat them as a **candidate function-address array** until a reader is identified. Main EXE also directly calls `0x800AD454` in startup code at `0x800115DC`.

But a bounded entry0 dump at `0x800AE900..0x800AE93F` under hypothetical base `0x800AD000` finds instruction-like words (including JALs), not 16 jump pointers, whereas entry1 code at `0x8010F444..` computes `0x800AE900+4*field0`, loads a word and `jr`s to it. The existing static address assumptions therefore cannot be collapsed into a single confirmed runtime map. Likely research gap is module lifecycle/base/relocation or another resource owning that address, but these alternatives are not yet distinguished.

Next: static loader/copy/relocation analysis to determine what occupies `0x800AD000..` when entry1 dispatch runs; identify who consumes the six-word pointer group. Do not retry the failed savestate, do not run emulator/adaptive player. Step 6(b) remains BLOCKED; Step 7 runtime map BLOCKED/UNKNOWN; Step 8(b) UNKNOWN. Story Mode remains TIDAK TERBUKTI TAMAT.
