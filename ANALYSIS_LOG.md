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

## Follow-up scan 6(b) — status sementara, 28 Oktober 2026

Run Ghidra statis [#40611660635](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40611660635) dipicu oleh perubahan alat di commit `ea148ca60af2e3eeaa1b58141532e1ff5a98dd60`, branch `main`. Status terbaru yang terlihat: `in_progress`; job `122564387469`; langkah terakhir `Install disc extraction tools` masih berjalan. Mulai pada `2026-10-28T00:53:40Z` (= 07:53:40 WIB). Belum ada artifact dan log job belum tersedia. Workflow memiliki `timeout-minutes: 35`; batas timeout sekitar 08:28:40 WIB bukan ramalan waktu selesai. Jika scan selesai, verifikasi log dan hasil XREF/pola LUI sebelum memutuskan apakah 6(b) berubah; jika gagal, simpan error dan jangan rerun identik sebelum sebab kegagalan dipahami.

Ini pemindaian kode statis saja. Tidak ada emulator/gameplay, tombol, savestate restore, adaptive player, atau upload biner privat ke artefak yang dimulai oleh perubahan ini.

---

# ADDENDUM — targeted static audit 28 Oktober 2026

Dua artefak yang dibuka langsung pada sesi lanjutan: Step 5 ZIP #12739676233 SHA-256 `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d`; Step 6 ZIP #12741234990 SHA-256 `7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9`. Main EXE memiliki empat direct JAL ke RNG yang telah diinventarisasi dan 156 mnemonic JALR; hitungan JALR tidak menyelesaikan target/callee dinamis. Anotasi panjang spimdisasm `nonmatching func_80015B7C, 0x580` perlu direkonsiliasi dengan body Ghidra 240 alamat yang end-exclusive di `0x80015C6C`, sementara disassembly mempunyai label tambahan di alamat itu. Langkah 4(c)/5 tetap SEBAGIAN.

Pada view hipotetis DATA.BIN entry-1 (base `0x800D0000` belum terverifikasi), direct operand census dari 98.357 instruksi terdekode memberi +B30 1 READ, +B38 1 READ, +B40 1 WRITE dan +B44 1 WRITE/1 READ. Nilai pointer dari `0x8013A554` serta alias/writer lintas fungsi tetap terputus; Step 6(b) BLOCKED. Detail, raw instruction bytes, hash, caveat dan matriks 17 kriteria: [docs/STEP4_10_TARGETED_AUDIT_2026-10-28.md](docs/STEP4_10_TARGETED_AUDIT_2026-10-28.md).

Actions filters `queued` dan `in_progress` keduanya menghasilkan nol run. Tidak dijalankan emulator/input/restore, adaptive player, atau workflow pemain adaptif. Tidak ada status teknis Step 4–9 dinaikkan; Step 10 tetap hanya matriks audit. Story Mode **TIDAK TERBUKTI TAMAT**.

---

# ADDENDUM — cross-check bukti dan checkpoint, 28 Oktober 2026

Artefak Step 5 #12739676233 (SHA-256 ZIP 94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d) menunjukkan tepat empat direct JAL ke 0x80035D78 dalam main EXE: 0x80015B14, 0x80015BF0, 0x8001A460, dan 0x80020C24. Artefak Step 6 #12741234990 (SHA-256 ZIP 7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9) mengonfirmasi aliran statis +B30/+B38 → sum → +B40 serta +B44 di-zero-kan lalu digunakan sebagai argumen ke helper 0x8001B364 pada branch +B2A>=6. Base entry-1 0x800D0000 tetap hipotesis.

Step 9 artifact #12779814671 (SHA-256 ZIP dd3e559997ce0c9f931f330144de8021bdb3c75fa16b4f21717299c4b2d4d79f) telah dibuka: RNG 7/7, helper negative-a0 8/8 dan setter/getter 16/16; MMIO sintetis. #40605560982 gagal pada SyntaxError sebelum helper diuji; #40605654394 berhenti karena MMIO belum dipetakan; #40605904131 memiliki kolom laporan duplikat; #40606159061 memperbaiki fixture dan format.

Lihat [laporan silang lengkap](docs/STEP4_10_CROSSCHECK_2026-10-28.md) dan [handoff](docs/HANDOFF_REVERSE_ENGINEERING_STEPS4_10_2026-10-28.md). Status tetap sesuai matriks; Story Mode TIDAK TERBUKTI TAMAT. Target cue UNKNOWN, barrier_level_selection=WAIT, readiness NO-GO. Tidak ada gameplay, input, restore savestate atau adaptive-player run.
---

# ADDENDUM — operasi statis empat caller RNG main EXE, 28 Oktober 2026, 07:06 WIB

Saya meninjau ulang artefak teks [#12739676233](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524/artifacts/12739676233) dari run [#40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524) (completed/success; 941.176 byte; SHA-256 ZIP `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d`). Artefak mencakup raw MIPS, dekompilasi Ghidra dan output m2c untuk caller yang dibatasi di bawah. Operasi yang bisa dipertanggungjawabkan: `0x80015ADC` menghitung argumen pemanggilan berbatas yang mencakup `RNG % divisor`; `0x80015B7C` menjalankan `4*n` pertukaran byte in-place dengan indeks kedua `RNG % n`; `0x8001A328` menyusun kandidat `[0, 1, 2, 3, 4, 5, 8, 9, 11]` sesuai hasil delapan cek `0x7F..0x86`, memilih `RNG % count`, lalu menulis `0x80089DA9`; `0x80020BF4` setelah guard objek lolos menyimpan keluaran RNG modulo `0x1000` ke offset `+0x34` dan memanggil fungsi lanjutan. Ini fakta operasi kode pada batas fungsi yang dibandingkan, bukan bukti bahwa objek adalah kartu/barrier/giliran atau bahwa caller menentukan hasil roulette/battle. Status Step 4(c/d) dan Step 8(a) tetap **SEBAGIAN**; Step 8(b) tetap **UNKNOWN** untuk identitas aturan permainan. Rincian instruksi dan batas interpretasi tercatat di laporan Step 4 dan Step 8.

---

<!-- current-step9-helper-checkpoint-2026-10-28 -->
# CHECKPOINT TERBARU — uji helper counter terisolasi, 28 Oktober 2026, 07:03 WIB

Sumber kode yang diuji pada checkpoint ini: commit [`7f234820f1b83a34654e900592903678365006a5`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/7f234820f1b83a34654e900592903678365006a5). GitHub Actions [run #40606159061](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40606159061) **completed/success** pada 07:03:03 WIB; seluruh langkah job sukses, termasuk eksekusi, unggah laporan teks, dan cleanup. Artefak [#12779814671](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40606159061/artifacts/12779814671) berukuran **5.377 byte**, digest/SHA-256 ZIP `dd3e559997ce0c9f931f330144de8021bdb3c75fa16b4f21717299c4b2d4d79f`.

## Hasil aktual yang diperiksa dari log dan artefak
- RNG main EXE `0x80035D78`: **7/7** vektor cocok dengan rumus/state/output yang diharapkan.
- Jalur argumen negatif helper `0x80037138`: **8/8** kasus lulus; argumen `0xFFFFFFFF` dan `0x80000000`, masing-masing diuji terhadap empat nilai global sintetis `0`, `1`, `0x12345678`, `0xFFFFFFFF`. `v0` cocok dengan nilai `0x80066E7C` yang diinjeksi, global tidak berubah, PC kembali ke sentinel `0x001FF000` setelah 33 instruksi, tanpa error emulator.
- Setter/getter nilai peserta `0x8001387C`/`0x800138EC`: **16/16** kasus lulus. Total cakupan tes yang tercatat sekarang 31 assertion kasus di tiga rutin/jalur ini; status Step 9 keseluruhan tetap **SEBAGIAN**.
- Helper lebih dahulu membaca alamat timer melalui pointer yang dimuat dari global `0x80065D34 -> 0x1F801814` dan `0x80065D38 -> 0x1F801110`. Agar eksekusi terisolasi dapat mencapai cabang negatif, kedua halaman MMIO dipetakan sebagai fixture sintetis dan diberi word `0x12345678`. Ini **bukan** model perangkat keras/timer PS1 asli. Bukti mengonfirmasi perilaku cabang helper hanya pada model CPU plus MMIO sintetis tersebut; tidak membuktikan nilai counter saat boot, waktu runtime, pemetaan entry-0, seed RNG awal, atau dampak gameplay.
- `STEP9_PRIVATE_CLEANUP=PASS`. Artefak run ini berisi laporan/log teks, bukan ROM/BIN/CUE/EXE, BIOS, savestate, RAM dump atau screenshot privat.

## Percobaan sebelumnya dan batas interpretasi
Run [#40605560982](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40605560982) gagal sebelum menjalankan kasus helper karena `SyntaxError: '[' was never closed` pada pembentukan laporan. Run [#40605654394](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40605654394) memperbaiki sintaks namun tes helper awal berhenti di pembacaan MMIO tak terpetakan; hasil awalnya **bukan** bukti return helper gagal. Run [#40605904131](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40605904131) sudah mendapatkan 7/7, 8/8 dan 16/16, tetapi tabel laporannya memiliki kolom status duplikat. Run #40606159061 adalah pengulangan terakhir dengan MMIO sintetis serta tabel yang telah diperbaiki dan diverifikasi.

## Status kriteria yang berlaku
- **Langkah 4 — SEBAGIAN:** bukti statis jalur helper dan uji terisolasi negatif-a0 bertambah kuat; lifecycle seed, caller boundaries, base resource entry-0 `0x800AD000`, reachability dan hubungan RNG dengan hasil roulette/battle belum terbukti.
- **Langkah 5 — SEBAGIAN:** 13 fungsi main EXE dan satu kandidat entry-1 telah dibandingkan secara struktur; cakupan seluruh fungsi/resource/call graph belum menyeluruh.
- **Langkah 6 — SEBAGIAN:** `+0xB30/+0xB38 -> add -> +0xB40` terverifikasi statis; pointer/alias runtime tetap **BLOCKED**, makna field **UNKNOWN**.
- **Langkah 7 — SEBAGIAN:** direktori/struktur loader statis saja; runtime mapping/relokasi/checksum tetap **BLOCKED**, DATA2.BIN/DUMMY.BIN belum dipetakan end-to-end.
- **Langkah 8 — SEBAGIAN:** belum ada bukti yang cukup untuk memberi label biaya Chakra, barrier/upgrade, kartu, giliran, roulette/battle, menang/kalah.
- **Langkah 9 — SEBAGIAN keseluruhan:** 7/7 RNG + 8/8 jalur helper + 16/16 setter/getter lulus dalam pengujian CPU/MIPS terisolasi; belum menguji semua fungsi atau gameplay.
- **Langkah 10 — TUNTAS hanya sebagai matriks audit/rekonsiliasi**, bukan sebagai penyelesaian Langkah 4–9.

**Tidak dilakukan:** menjalankan gameplay, menekan input emulator, menjalankan pemain otomatis/monitor gameplay, memulihkan savestate, atau mengubah classifier/policy/runner. Story Mode **TIDAK TERBUKTI TAMAT**. Entri historis di bawah checkpoint ini harus dibaca sebagai catatan bertanggal, dan tidak mengalahkan status di atas.

---

<!-- historical-checkpoint-2026-10-28-0422-superseded -->
## HISTORICAL CHECKPOINT — 28 Oktober 2026, 04:22 WIB (superseded by checkpoint above)

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

## Actions output audit — entry-0 timeout, 27 Oktober 2026 21:54:52 WIB

Downloaded text artifact #12743796502 from [run #40520635663](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40520635663) and verified ZIP SHA-256 `e2d5b496b2310c17110c59710212f7605bf8b3d90b798abb438c1224bf3d0549` (2.299.302 bytes). The report confirms DATA.BIN entry 0 offset `0x5F800`, 110.536 bytes, SHA-256 `56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4`, hypothetical base `0x800AD000), and 36 exported function rows. But `entry0-ghidra-headless.log` explicitly says analysis timed out after 1,800 seconds, with repeated function body overlap/repair errors. Candidate `0x800BDBFC` is labelled user-defined/candidate and has zero recorded references. Therefore this output does not establish caller boundaries or connect that candidate to the RNG setter.

At last poll [run #40521141039](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521141039) is still in progress at entry-0 analysis; entry1 step succeeded, artifact not yet uploaded. Previous same-workflow run took 31m27s, rough end estimate around 22:25–22:35 WIB for a similar 1,800-second stage; uncertainty remains.

---

## Correction from raw MIPS re-read — 27 Oktober 2026 21:43 WIB

Re-read of the actual emitted body for `0x800ED8C8` confirmed the table addressing operation more precisely than the initial summary: `0x800ED920` builds the global symbol high half and `0x800ED924 lw a0,%lo(D_8013EA74)(v1)` **loads the pointer/value stored in global slot `0x8013EA74`**. The code adds `index*0x90` to the loaded value and reads the byte at `+0x29`. Ghidra C represents the loaded value as `iRam8013ea74`; m2c renders the global symbol differently and does not expose this dereference as clearly. Consequently, treat the successful run #40523020556 as validation of exact function boundary, successful outputs, and structural call/control-flow cross-check—not full pointer-type/effective-address equivalence. Runtime value, table mapping and gameplay feature identity remain unknown.

---

## LIVE LOG — Ghidra/m2c entry-1 dan CFG/SSA Step 6 (27 Oktober 2026, 21:41 WIB)

### Step 5 — resource function cross-check lulus
Run [#40523020556](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40523020556) completed/success pada 21:40:45 WIB. Artifact #12742268706 (1.367.605 B; ZIP SHA-256 `5f3f767667444f7c956c36fc59cf75b6bb90a5a1dde8ddb92fb69f9e0f797e81`). Entry 1 size/hash verified; Ghidra function `0x800ED8C8` boundary 160 B, end-exclusive `0x800ED968`; Ghidra C and m2c comparison SUCCESS, m2c exit 0. Static behavior: input index mask 16 bit, helper byte default, RNG % 250 compared with byte indexed `index*0x90+0x29`, result `0xFF` when remainder >= byte, otherwise helper byte. Runtime base/table identity/feature meaning UNKNOWN.

Percobaan #40521830977 failed because temp Ghidra project directory did not exist; #40522317571 parsed decimal size as hex and #40522919529 failed to match size regex. These are superseded by corrected #40523020556 and not counted as successes.

### Step 6 — CFG/SSA evidence
Run [#40522772847](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40522772847) completed/success pada 21:38:32 WIB, artifact #12741234990 (234.210 B; ZIP SHA-256 `7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9`). New script `tools/step6/ExportFieldCfgDefUse.java` emits high-level SSA/P-code, block IDs, branch/phi nodes and depth-bounded def-use for `0x8012C544` (88 ops, 7 constant-field matches) and `0x8012CACC` (47 ops, 2 matches). Evidence of read `+B30/+B38` → addition → write `+B40`; `+B44` consumer is in a separate branch/merge path. Global pointer slot `0x8013A554` still has unresolved runtime value/alias. Full audit: [STEP6_CFG_SSA_DATAFLOW_AUDIT_2026-10-27.md](docs/STEP6_CFG_SSA_DATAFLOW_AUDIT_2026-10-27.md). Step 6 remains SEBAGIAN.

### Langkah 4 context window
Runs #40521136060 and #40521136038 completed success. Entry0 at `0x800AF2A4` calls helper `0x80037138`, with delay-slot `li a0,-1`; next `0x800AF2AC` calls setter `0x80035DA8` and delay-slot `move a0,v0` forwards helper return. This resolves the instruction-level question but not the value at runtime, function boundary, base load mapping, or gameplay effect. Caller signatures are only heuristics.

### Batas konsisten
No adaptive player or Story Mode runner was run or changed; no gameplay input, emulator session, or savestate restore; no private binary/gameplay assets uploaded. Story Mode TIDAK TERBUKTI TAMAT. Current status and live Actions must be checked before continuing.
---

## Step 9 — hasil isolasi diperluas final (27 Oktober 2026, 21:02 WIB)

Run [#40516755810](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40516755810) **completed/success** pada 21:02:36 WIB. Artifact teks #12740305973: 4.567 byte, SHA-256 ZIP bf1a702074849b2592bfc5555a0d493b5ed86d3de0b9895a192db7fdf9f80cd4. Raw job log/job summary memastikan semua 11 langkah success, termasuk STEP9_PRIVATE_CLEANUP=PASS. Hasil aktual: RNG 0x80035D78 7/7 vektor dan setter/getter 0x8001387C/0x800138EC 16/16 kasus PASS. Setter membatasi nilai [-9999,99999], valid index 0–3 return 1, invalid 4/0xFFFFFFFF return 0 tanpa perubahan slot; getter membaca slot yang sama untuk indeks valid dan return 0 untuk indeks invalid. Setiap tes memeriksa v0/memory, return sentinel dan batas ≤128 instruksi.

Ini uji CPU/RAM terisolasi dengan teks executable terverifikasi, bukan emulator PS1, BIOS, gameplay/input/savestate, dan bukan bukti formula biaya, aturan barrier/upgrade, giliran atau kemenangan. Step 9(b) kini SEBAGIAN (bukan UNKNOWN) karena dua accessor tambahan sudah diuji; Step 9 overall tetap SEBAGIAN karena target-compare, transisi, helper/caller lain dan semua jalur gagal belum tercakup. [Laporan hasil uji](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/out/step9/STEP9_UNICORN_RESULT_2026-10-27.md).

# ANALYSIS LOG — live static evidence reconciliation (27 Oktober 2026)

## Step 5 — hasil perluasan terverifikasi (27 Oktober 2026, 20:50 WIB)

- Retry [#40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524) **completed/success** pada 20:50:53 WIB. Artefak teks [#12739676233](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524/artifacts/12739676233) berukuran 941.176 byte, digest API dan SHA-256 lokal cocok: `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d`. ZIP memuat 45 file teks/C/disassembly/log, termasuk 26 file C Ghidra/m2c nonempty; tidak ada ROM/BIN/CUE/EXE/BIOS, Memory Card, savestate, RAM dump atau screenshot. Semua langkah job selesai, termasuk penghapusan input/proyek sementara.
- Pemeriksaan aktual: `metadata_parser_fixture=PASS`, `function_metadata=PASS`, `functions_requested=13`, `functions_with_m2c_output=13`, laporan akhir `status=SUCCESS`. Masing-masing fungsi memiliki keluaran C Ghidra dan m2c; exit code m2c 0 untuk 13/13.
- Lingkup 13 target main EXE: empat caller RNG terdahulu; setter/getter nilai pemain pada `0x8001387C`/`0x800138EC`; RNG `0x80035D78`; helper `0x80037138`; dispatcher/initializer/callback routines `0x800373F8`, `0x8003755C`, `0x80037B58`, `0x80037BB0`, `0x80037C48`. Ini cross-check struktur same-address berdasarkan batas fungsi Ghidra, bukan kesamaan source asli atau bukti aturan gameplay.
- Percobaan pertama [#40512956924](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40512956924) gagal karena `0x80012A70` tidak memiliki fungsi Ghidra pada alamat itu dan tak memiliki metadata body. Perbaikan di [commit `2b16e67bfafde873c95b577bc030f6e0c9f84c58`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/2b16e67bfafde873c95b577bc030f6e0c9f84c58) mengeluarkan target itu dari daftar fungsi yang dibandingkan. Identitas/semantik target `0x80012A70` tetap perlu diperjelas; jangan anggap cross-check fungsi tersebut sudah berhasil.
- **Status Langkah 5 secara keseluruhan tetap SEBAGIAN** terhadap cakupan yang diminta: 13 fungsi inti executable utama sudah dibandingkan, tetapi fungsi kandidat di DATA.BIN entry 0/1 (termasuk pembanding target/record dan transisi), semua hubungan caller/callee wajib, serta seluruh executable belum dicakup m2c secara menyeluruh. Status lama “empat fungsi saja” adalah riwayat sebelum perluasan, bukan hasil terbaru.
- Run Ghidra statis terpisah [#40512917437](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40512917437) masih `in_progress`, dimulai 20:32:30 WIB, pada langkah analisis DATA.BIN entry 0 untuk external helper. Pembanding Ghidra sebelumnya #40498208067 membutuhkan sekitar 31 menit 47 detik; perkiraan kasar berdasarkan durasi itu sekitar **21:04 WIB**, bukan ETA terjamin.


## Latest live checkpoint — Step 6 bounded base-register provenance (27 Oktober 2026, 20:25 WIB)

**Checkpoint terbaru Step 6 (27 Oktober 2026, 20:25 WIB):** scanner provenance di https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/0afc0eec4a5c12e4df5a17c771c8b0d28d7a99dd dijalankan oleh [Actions #40511758146](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40511758146) — completed/success pada 20:25:48 WIB. Artifact [#12737611770](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40511758146/artifacts/12737611770), 229.233 byte, SHA-256 ZIP `b84ff017cdbefb8ece6d04a7c8bef66b3fdc27b61412e91e10cc01485225b126`; digest API sama dengan SHA lokal. Enam anggota ZIP hanya teks/log; `text_only_output_count=6`, `private_binary_in_artifact=no`, `STEP6_PRIVATE_CLEANUP=PASS`. Fixture parser operand dan fixture pembentukan alamat `lui/ori/addiu/sign-extension` benar-benar mengeluarkan PASS. Laporan: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/docs/STEP6_REGISTER_PROVENANCE_AUDIT_2026-10-27.md.

- Fixture outputs from the actual Ghidra scan: `memory_displacement_parser_fixture=PASS`; `register_provenance_address_constructor_fixtures=PASS cases=lui_ori_addiu_sign-extension`.
- Raw base pointer chain is not closed: target accesses at 0x8012C634/638/644 use `a0` whose last visible definition is `lw a0,-0x5AAC(s0)` at 0x8012C628; prior `s0` provenance stops at a branch boundary. The +B44 read at 0x8012CB14 has `v1` tracing stop at branch 0x8012CAF8.
- Therefore the bounded constant/address expression evaluator is validated for fixtures, but cannot certify real object identity, alternate bases, aliases, global readers/writers or runtime mapping. Step 6 remains SEBAGIAN and 6(b) BLOCKED. No Step 4/7/8/9/10 closure status changes; Story Mode remains TIDAK TERBUKTI TAMAT.


No new runtime experiment is justified by current static evidence. Independent parsing of Step 6 artifact #12733854252 found 2.104 displacement values and 31.081 recognized direct base+displacement operands in 98.357 decoded instructions (19.366 reads/11.715 writes). Static bytes prove B30/B38 loads → addu → B40 store; B44 is zeroed in a candidate initializer and later read into a2 for candidate call 0x8001B364. These are operations on a hypothetical DATA.BIN entry-1 base 0x800D0000, not semantic labels or runtime mapping.

Important distinction: aggregate counts are complete within the recognized/decoded view, but detail contexts for common offsets are capped at 200 (e.g. +0x2E9 has 257 accesses/200 contexts; +0x22 has 275/200). Priority B30/B38/B40/B44 context samples have no per-offset cap. Latest scan #40504640855 and runner audit #40504977322 succeeded; metadata/digests verified and runner cleanup PASS. Full criterion matrix and artifacts: [live reconciliation](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/docs/STEP4_10_LIVE_RECONCILIATION_2026-10-27.md). Story Mode TIDAK TERBUKTI TAMAT.

---

# Research checkpoint update — 27 October 2026, parser repair, one-breakpoint runtime and Step 6/8 trace

- Main HEAD immediately before this checkpoint update: `0fe48bc85451d15fc23b7e2948df7341c1c4f431`. The commit writing this entry advances main; query live main SHA on the next continuation. The GitHub connector does not expose local working tree status.
- The Step 7 report parsers were corrected and protected by a regression fixture. Validator [#40484417534](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484417534) succeeded with raw-log assertion `STEP7_FRAME_PARSER_FIXTURE_PASS frames=1,2,3,10,20,30,40 max=40`.
- Single-breakpoint cold boot awal [#40484519812](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484519812), on workflow source `9edbcb3063a41588ca739e644b9dc9b29c585b3f`, validated disc/CUE/BIOS/emulator hashes and extracted BIOS SHA. No restore or gameplay input occurred. Preflight reached frame 50; debugger listener-only reached frame 50; the candidate breakpoint `0x800AD454` showed progress through frame 100 but no hit before exit 124 at the 35-second boundary. Private cleanup PASS. The report assembler initially failed and its partial artifact is not the authoritative runtime summary.
- The first single-breakpoint run's report assembler failed at `SyntaxError: '[' was never closed`; treat raw logs—not its workflow conclusion or incomplete artifact summary—as authority for that run. Artifact #12723834084, size 1,894 bytes, ZIP SHA-256 `6188c32e73a0984133c5c1f4ac3a37dcacde677458ec56c7fdf100ba25c73968`. The report assembler fix is on `8326c07f71caeab12924133b0812ec7e86b8b1f7`; corrected run [#40484548650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650) finished success at 10:00:47 UTC (~291 seconds). Artifact #12724961702 is 3,960 bytes, ZIP SHA-256 `27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71`. Its raw report says preflight frame 50, debugger-control max frame 60, target progress logged through frame 120, no hit at `0x800AD454`, hit count 0, exit 124 at 35 seconds, and `STEP7_PRIVATE_CLEANUP=PASS`. All steps passed on the corrected run. This still does not establish loader mapping/base because there was no hit or source/destination/register/size/checksum sample.
- Additional static tracing of the already-existing runner log [#40473737136](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136) found that candidate `0x8011C0D0` negates participant record word `+0x04`, clamps a lower bound to `-9999`, and passes the value to main-exe setter `0x8001387C`. Candidate target/flag branches store values at `+0x58B` and `+0x5D2` before calling candidate transition `0x800EF98C`. This is static decompiler evidence only under hypothetical entry-1 base `0x800D0000`; no barrier-cost or win-condition semantics are claimed. Offsets `+0xB30/+0xB38/+0xB40/+0xB44` remain UNKNOWN.
- Status matrix remains: Step 4 **SEBAGIAN** for official criteria 4(a–e); Step 5 **TUNTAS for four chosen functions only**; Step 6 **SEBAGIAN**; Step 7 **SEBAGIAN**; Step 8 **SEBAGIAN**; Step 9 **TUNTAS for isolated RNG `0x80035D78` only**; Step 10 **TUNTAS as audit index only**.
- No adaptive-player/Story Mode workflow, gameplay input, savestate restore, classifier/policy, Revision65 marker, or readiness-gate modification. **Story Mode is NOT PROVEN COMPLETE**. Private disc/BIOS/Memory Card/savestate/RAM dump/private gameplay screenshot assets stay out of Git.

## Incremental checkpoint — seed-setter cold boot result (27 Oktober 2026, 17:18 WIB)

- Main HEAD before this incremental note: `0fe48bc85451d15fc23b7e2948df7341c1c4f431`; subsequent commits update main. Fetch live SHA before further work; working-tree status is unavailable through the connector.
- Bounded run [#40485987817](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817), source workflow commit `e1e346e707254ad617a6cccad43689df908801a6`, completed `success` at 10:08:48 UTC (17:08:48 WIB). Only one breakpoint `0x80035DA8`; no gameplay input/no savestate restore; asset checksum validation passed; preflight max frame 50, listener-only max frame 60, target progress frame 1–120 with `bp_hits=0`, exit 124 at bounded 35-second limit, private cleanup PASS. Text artifact #12724933081 is 4,003 bytes, ZIP SHA-256 `74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6`.
- Runtime result: no `STEP7_SINGLE_BP_HIT`, so no runtime `$a0/$ra/caller` values exist. The first report's no-hit fallback incorrectly printed `SINGLE_BREAKPOINT_PC=0x800AD454`; raw `STEP7_SINGLE_BP_READY targets=1 target=0x80035DA8` is the authoritative target configuration. Do not infer a seed setter hit from the artifact's fallback field.
- Fix and regression validation: fallback corrected on commit `a6734d7fc57ff6dfab9b8135cd5661bf0278c437`; validator [#40486315324](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40486315324) completed `success` with `STEP4_SEED_BP_NO_HIT_FALLBACK_PASS target=0x80035DA8`, `STEP4_SEED_BP_PARSER_FIXTURE_PASS`, and `STEP7_FRAME_PARSER_FIXTURE_PASS`. The parser fixtures are synthetic, not emulator evidence. Step 4(a) and Step 7 remain SEBAGIAN/UNKNOWN for seed lifecycle and runtime mapping.



## Incremental checkpoint — delay-slot correction and helper-return trace (27 Oktober 2026)

- MIPS delay-slot review corrected the previous assumption that the entry-0 callsite `0x800AF2AC → 0x80035DA8` directly passes `$a0=-1`. At `0x800AF2A8`, `li a0,-1` is the delay slot of the prior call to `0x80037138`. At `0x800AF2B0`, `move a0,v0` is the delay slot of the setter JAL and forwards helper return `$v0` to `0x80035DA8`. The setter's actual argument and resulting state are UNKNOWN until helper semantics are established.
- Corrected static source reports: `out/rng_resource_entry0_ghidra_context_2026-10-27.md`, `out/rng_resource_reference_scan_2026-10-27.md`, `out/rng_candidate.md`, `docs/STEP4_RNG_TRACE_2026-10-27.md`, `docs/STEP4_CLOSURE_2026-10-27.md`, `out/logic.md`. The reference scan now asks for helper return analysis, not merely the already-known argument register transfer.
- Added `dumpSimpleFunction(0x80037138)` and reference inventory to `tools/ghidra/ExportRngCallerAnalysis.java` in commit `b92aa084aba62182ed4edc436cf20d68581be984`.
- Run [#40487406384](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40487406384) is `in_progress`; main executable analysis has completed and DATA.BIN entry 1 is in progress; entry 0/helper result not yet available at this checkpoint. No gameplay or emulator execution is part of this Ghidra workflow.
- Step 4 remains **SEBAGIAN**; do not claim seed `0xFFFFFFFF` until return value evidence supports it. Step 7 remains **SEBAGIAN** with both loader and seed-setter probes bounded/no-hit. Story Mode remains **TIDAK TERBUKTI TAMAT**.


## Incremental checkpoint — Step 6 full-artifact store inventory and immediate scan (27 Oktober 2026)

- Full text artifact #12719587873 from runner review #40473737136 confirms five entry-1 candidate routines (`0x80111228`, `0x801112CC`, `0x801113B4`, `0x801114F0`, `0x80111588`) write `+0x2E9=0x3F`, `+0x2E5=0`, selector byte `+0x58B`, and conditional codes at `+0x5D2`; these values are observed stores, not game semantics. Candidate `0x8011C0D0` negates record word `+0x04`, clamps to `-9999`, then calls setter `0x8001387C` under hypothetical entry-1 base `0x800D0000`.
- Bounded scalar-immediate scan [#40488847927](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40488847927) covered 98,357 decoded instructions on entry-1 and reported no exact scalar-immediate hits for offsets `+0xB30/+0xB38/+0xB40/+0xB44/+0x2E9/+0x2E5/+0x58B/+0x5D2`. This scan is not a full memory-displacement/effective-address/register-alias/code-not-decoded scan; it does not contradict explicit store instructions in the decompiler artifact and does not prove offsets unused.
- A preceding field-scan attempt #40488684688 failed at CUE input normalization before static scanning; do not treat it as a negative reverse-engineering result. The corrected scan artifact is the result to inspect, subject to its scalar-immediate scope.
- Step 6 remains **SEBAGIAN**. Still unknown: entry-1 runtime base, meanings of field/code values, source/final writer for `+0xB30/+0xB38/+0xB40/+0xB44`, and effects of candidate transitions. Current Ghidra helper-return run #40487406384 also remains to be checked for `0x80037138`; the delay-slot correction says its `$v0` is forwarded to candidate seed setter `0x80035DA8`, so no value should be assumed.

---
# One-shot RIGHT-vs-NONE diagnostic outcome (25 October 2026) (25 October 2026)

- The one authorized diagnostic [#40144220503](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40144220503) failed during the first preflight capture. Checkpoint restore event passed, but capture failed with `sh: 1: xwd: not found`; no screenshot frames or F20 parity result exist.
- Runner-only artifact analyses [#40144372685](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40144372685) and [#40144439400](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40144439400) verified the failure text. They report no RIGHT press/release record. No gameplay input was sent and no A/B outcome was observed.
- The failed capture environment omitted the package providing `xwd` (install `x11-apps` in a future runner setup and preflight `command -v xwd`, `command -v convert`, and a bounded root capture before restoring state).
- Temporary diagnostic/analysis workflows and selectors were removed. No gameplay retry was started; another restore/input attempt needs fresh explicit user approval.
- Full runner-only audit: [docs/ONE_SHOT_SUBMENU_RIGHT_AB_RESULT_2026-10-25.md](docs/ONE_SHOT_SUBMENU_RIGHT_AB_RESULT_2026-10-25.md).
- Preserve cue UNKNOWN; `barrier_level_selection = WAIT`; readiness NO-GO; Story Mode NOT COMPLETE; Revision65 marker blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` unchanged; cue token absent.

---

# Corrected runner-only control-probe inspection (25 October 2026)

Actions run [#40141018663](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40141018663) completed the corrected inspection of artifact #12308661246 on the GitHub runner. The artifact digest matched GitHub metadata. It records ten same-checkpoint branches with identical pre captures; press/release readbacks pass for each input branch. The directional post captures are pixel-identical to NONE, while CIRCLE changes the full 320×240 frame. OCR over the three unique images was too garbled to establish state. Thus it is not authenticated as a `barrier_level_selection` A/B and provides no target-cue evidence. Details: [triage report](docs/NON_PLAYER_ACTIONS_ARTIFACT_METADATA_TRIAGE_2026-10-24.md).

First corrected run #40140914545 failed only at a Pillow diff-stat computation; fixed and completed in #40141018663. No savestate was present/opened; no emulator, gameplay input, restore, player workflow, tests, local artifact download, or private evidence commit occurred. The temporary runner-only workflow and selector were removed.

Preserve UNKNOWN cue, `barrier_level_selection = WAIT`, readiness NO-GO, Story Mode NOT COMPLETE, Revision65 blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`, and cue token absent.

---

# Runner-only inspection — existing control-probe artifact (25 October 2026)

Authorized one-job Actions inspection [#40110571330](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40110571330) completed successfully. Artifact #12308661246 size and SHA-256 matched its authenticated GitHub metadata. The report describes ten button/no-input branches from a common checkpoint and identical pre-frame hashes; all non-CIRCLE post frames match NONE, while CIRCLE differs. Captures are 320×240. The checkpoint state is unknown, and OCR/image diffs were skipped because the inspection code only accepted 1280×800; no submenu cue conclusion follows. See [full triage](docs/NON_PLAYER_ACTIONS_ARTIFACT_METADATA_TRIAGE_2026-10-24.md).

Artifact was downloaded and processed only on GitHub Actions runner. No savestate was present/opened; no emulator, gameplay input, restore, player workflow, tests, local artifact download, or private-evidence commit occurred. Do not run another inspection without separate authorization. Preserve cue UNKNOWN, `barrier_level_selection = WAIT`, readiness NO-GO, Story Mode NOT COMPLETE, Revision65 blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`, and cue token absent.

---

# Metadata-only follow-up — non-player Actions artifacts (24 October 2026)

See [non-player artifact metadata triage](docs/NON_PLAYER_ACTIONS_ARTIFACT_METADATA_TRIAGE_2026-10-24.md). Verified session-start HEAD `77f8da107236155b48ffa523c1c47dbb92311131`; latest ten Actions completed. Usage: 39% used / 61% remaining on the primary 30-day window; secondary unavailable.

- Possible lead: control-probe run #39513285641 / artifact #12308661246. Its workflow describes ten input/no-input branches from a shared checkpoint, but available metadata does not identify the state. It is not verified as a same-start submenu A/B.
- Already-documented and excluded from repeat inspection: barrier probes #39618670884 and #39619671384; single barrier confirmation #39617444912; roulette artifacts #12351098551, #12352271884, #12386841383.
- No active runner or existing safe runner-side inspection path was available. No artifact contents were fetched. Continue metadata-only unless an already-available compliant runner path exists; do not launch a workflow for artifact retrieval.

State preserved: cue UNKNOWN; `barrier_level_selection = WAIT`; adaptive readiness NO-GO; Story Mode NOT COMPLETE; Revision65 blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` unchanged; cue token absent. No gameplay/emulator/restore/player workflow or tests ran.

---

# Offline follow-up — remaining adaptive-player artifacts (24 October 2026)

Seventeen artifact IDs not referenced in the four current continuity documents were screened from the Actions inventory. The full report, artifact sizes/digests, and decision are in `docs/REMAINING_PLAYER_ARTIFACT_TRIAGE_2026-10-24.md`.

- Run #39767083708 / artifact 12420512625: exact F20 parity; DOWN vs WAIT starts in `menu_or_unknown_choice`, not the nested barrier submenu.
- Run #39877412316 / artifact 12469530414: exact F20 parity; CIRCLE vs WAIT starts in `card_selection`; action reaches dialogue while control remains on card selection.
- Run #39904672868 / artifact 12479814966: sequential checkpoint resume, not matched-start action/control.
- Other 14 manifests lack a complete matched-start submenu A/B.
- Candidate artifact sizes and SHA-256 digests match GitHub metadata. No savestate contents were opened. No emulator, restore, continuation, gameplay input, player workflow, or test ran.

Decision unchanged: target cue UNKNOWN; `barrier_level_selection = WAIT`; adaptive readiness NO-GO; Story Mode NOT COMPLETE; Revision65 marker unchanged and cue token absent. Usage at session start: 30-day window 19% used / 81% remaining; secondary unavailable.

---

# Offline system review — autonomous Story Mode readiness blockers (24 October 2026)

## Scope
Static review from `main` HEAD `9acbd5eed24bdc81165358d63ed594600dae488c` of `tools/storymode_adaptive_agent.py`, `.github/workflows/naruto-storymode-adaptive-player.yml`, its regression workflow/tests, the consumed player marker, and the current status/handoff. No screenshot or private artifact was re-audited in this review.

## Findings
- The agent already has a conservative observe/decide policy for selected menu, map, dialogue, roulette, card, and barrier-choice states. It intentionally returns WAIT at `barrier_level_selection` because the target tile is not identified.
- `battle_untrained` returns WAIT. There is no learned battle action/turn policy for the game’s encounter states, and result/win/loss states are not calibrated.
- The player workflow is a bounded tool for experiments/checkpoint continuation, capped at one or two cycles of 180 emulator frames. It captures external X11 observations, verifies input press/release, and validates each checkpoint after process exit. The progress signal it writes is only map→dialogue/battle; it does not detect authentic Story Mode completion.
- Increasing cycle count cannot safely produce autonomous completion: the submenu cue gate still blocks a required state, and the agent has no supported battle or terminal-state policy.
- Current Actions do not add gameplay evidence: monitor #40102319836 is successful monitoring of a skipped/no-artifact player run; classifier regression #40071317759 is a code-policy result, not game progress.

## Decision
The current repository contains an adaptive-player prototype and reliable bounded experiment/checkpoint machinery, but not a ready Story Mode finisher. No gameplay action is justified by this static review. Preserve target UNKNOWN, `barrier_level_selection = WAIT`, adaptive readiness NO-GO, Story Mode NOT COMPLETE, Revision65 consumed marker unchanged, and cue token absent.

## Fastest compliant work order
1. Inventory only already-existing authenticated private artifacts for an unreviewed matched-start submenu A/B and for matched battle/result outcomes; do not repeat documented artifacts or open savestates.
2. Add classifier/action rules only where paired authentic action/control evidence isolates a repeatable state transition; every other state remains WAIT.
3. Require distinct authentic ending/results captures before implementing a completion detector. Completion must not be inferred from workflow success, a checkpoint, or a map transition.
4. Only after target cue, battle/result policy, terminal detection, checkpoint restore, and stop-on-unknown behavior are independently qualified, continue with short bounded sessions that chain verified checkpoints and stop on any unrecognized state.

No tests were run and no emulator/gameplay input was used. The next session must verify live HEAD and Actions again.
---

# Offline follow-up — Revision62 matched-state submenu A/B still does not identify the target (24 October 2026)

## Provenance and scope
- Audit baseline `main` HEAD: `2a5fa920ab544f125041f3fefd8f202ab702601b`.
- Private artifact: run [#39940196133](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39940196133), artifact `12495906030` (11,441,461 bytes; downloaded ZIP SHA-256 `b07efa5e448a78ce9f81392a094e645d9089a50baabadbca64646615cff83270`, matching the GitHub API digest). The artifact contains C01/C02 PNG captures at F20/F60/F100/F110/F180, comparison/precondition/action reports, JSON observations, and `.sstate` outputs. Only PNGs and text/JSON were read; the `.sstate` members were not opened or restored.
- This artifact was already used by the passing historical-frame policy regression in Actions #40069923244/#40071317759. The present pass is limited to visual discrimination of a selected tile and does not rerun the classifier test.

## Matched start and input trace
- `ab-comparison-report.txt` records F20 parity PASS with `1,024,000` identical pixels and parent SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`; both branch states are `barrier_level_selection`.
- C01 is LEFT then Circle: LEFT press/release at F30/F38 and Circle press/release at F70/F78; each readback passed. C02 is WAIT with zero button presses. Both Memory Card clones match at SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.

## Visual result
- The submenu prompt remains `レベルアップする結界をえらんでください` (Pilih penghalang yang akan dinaikkan levelnya), with footer `けってい` (konfirmasi/pilih) and `もどる` (kembali). The action frames do not show a new tile-specific information panel, a clearly selected-tile outline, or another cue that remains attached to one candidate tile.
- The pink `60` badge is partially obscured by the fixed HUD, with more of it exposed in the LEFT branch than in control. The candidate is therefore not equally unobstructed across the A/B pair. Naruto/foreground pose and scene composition also shift; these broad changes cannot be attributed to target selection.
- The report gives action/control differing-pixel counts of `693755`, `693655`, `693270`, and `693882` at F60/F100/F110/F180. It also records `barrier_level_selection` / `WAIT` across the observed frames. The large whole-frame deltas are not a tile-anchored measurement.
- Revision47 run #39868722262 / artifact `12464698050` was screened as a candidate but is already documented as starting in `roulette`; it cannot answer the submenu question. No screenshot re-audit of that known result was undertaken.

## Classification and decision
- **VERIFIED:** Revision62 has pixel-identical F20 starts, matching submenu classifications, matched card clones, logged action/control inputs, and visible submenu prompts in the sampled captures.
- **HYPOTHESIS:** the observed image deltas are consistent with scene/view movement, animation, and HUD occlusion.
- **UNKNOWN:** which barrier is targeted and what unique visual cue marks it. The prompt/footer, pink-badge visibility, character pose, and broad frame differences do not meet the gate.
- Keep `barrier_level_selection = WAIT`, target cue **UNKNOWN**, readiness **NO-GO**, and Story Mode **NOT COMPLETE**. The Revision65 marker was read at blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` and left unchanged; the cue-token gate remains closed.
- No emulator, restore, continuation, gameplay input, tests, or player workflow was run for this audit. No private artifact or evidence file was added to Git.

## Next offline step
Search only remaining, distinct authenticated artifacts for a same-start-state A/B where the same candidate tile is unobstructed in both branches and a reproducible cue is physically anchored to that tile, preferably corroborated by a matching tile-specific panel change. If none exists, preserve UNKNOWN/WAIT and document that the repo lacks qualifying evidence; do not infer a cue or bypass the gate.

---

# Offline follow-up — Revision58 single-branch submenu artifact does not identify target tile (24 October 2026)

Run [#39905240818](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39905240818), artifact #12480856146 (3,075,304 bytes; API digest `sha256:ca829197c7be852580e0527f071d2fc3711ff2433d17ed020f000fb52dbc4acf`) was newly triaged offline from its authentic screenshots and text/JSON only.

The artifact contains one branch, C01, with F20/F60/F100/F110 images only. `action-cycle-01.txt` records CIRCLE; there is no C02, no A/B report, no F180 frame, and no savestate. F20 shows `結界をレベルアップしますか?` (Apakah ingin menaikkan level penghalang?) with `はい` (Ya) selected. F60/F100/F110 show `レベルアップする結界をえらんでください` (Pilih penghalang yang akan dinaikkan levelnya), with `けってい` (konfirmasi) and `もどる` (kembali) footer hints.

The F60/F100/F110 decision JSON incorrectly classifies these screenshots as `dialogue` and predicts START, while the screenshot is the small submenu panel; the actual action file records only CIRCLE, so no subsequent START input is evidenced. Descriptive RGB diff counts are F60↔F100 47,940 changed pixels (mean absolute RGB 1.72836), F100↔F110 43,590 (1.00860), F60↔F110 53,358 (2.07506). The character/tile ROI `(555,270,700,455)` has 14,375/26,825 pixels changed between F100/F110; prompt panel ROI `(120,560,700,730)` has zero changed pixels over that pair. These measurements capture temporal animation, not a unique target cue.

**Classification:** VERIFIED — this single run reaches the submenu prompt by F60. UNKNOWN — the intended target tile and its unique selection cue. It is not a matched-start-state A/B, so do not promote the sprite, blue tile, or red-orange mark to a verified focus signal. Keep WAIT/UNKNOWN, readiness NO-GO and Story Mode NOT COMPLETE; keep the Revision65 marker and cue token unchanged. No emulator/input/restore action was performed and no evidence files were committed.

---

# Offline follow-up — matched-state historical submenu A/B artifacts examined (24 October 2026)

After verifying live HEAD `ed683f21f856a5def2f4a5ab9d0db09028b78500`, the latest Actions monitor [#40087271642](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40087271642) was confirmed `success`, but its report classifies player run #39975090690 as `EXPECTED_GATED_SKIP_NO_GO` (`completed/skipped`, no player artifact). The latest regression #40071317759 remains green with 35 tests; no test rerun was warranted.

## Run #39908484177 — LEFT vs WAIT

Artifact `12481932174` has a matched F20 initial screenshot (1,024,000 identical pixels); both decisions classify `barrier_level_selection` / `WAIT`. Historical runtime log records LEFT press `readback=true`, release `readback=false`; F60/F100/F110/F180 broad screenshot differences versus control are 693,755/693,655/693,270/693,882 pixels, with mean absolute RGB differences 17.71671/17.62710/17.54281/17.62892. Yet action verification says `state_changed=false`; the state remains WAIT.

The pink badge is more exposed under the HUD in action than control. In diagnostic ROI `(525,145,660,225)`, the explicit exploratory color mask (`R>150`, `R>1.3×G`, `B>100`, `|R−B|<100`) counted action/control `146/146` at F20, `1160/172` at F60, `1076/162` at F100, and `852/146` at F110. These are not classifier thresholds and cannot imply selection. In prompt glyph ROI `(170,595,660,690)`, a `R,G,B>190` mask had 1,658 bright pixels per branch and zero XOR at F20, F60, F100 and F110, so the Japanese instruction panel did not acquire a distinct target identity in these samples.

## Run #39909132189 — CIRCLE vs WAIT

Artifact `12481644668` starts from the same observed submenu state on both branches. Logs confirm the historical CIRCLE press/release readback, but `state_changed=false`. For F20/F60/F100/F110/F180, each action/control pair has zero differing pixels and mean absolute RGB difference 0. The pink badge remains partly obscured by the fixed HUD in both branches. This is a negative observation for these sampled frames, not a universal claim about Circle.

## Auxiliary UP artifact and source availability

Run #39946344909 / artifact `12498880615` lacks `C02-F180.png` and `ab-comparison-report.txt`; it overlaps the already-known UP/camera-pan context and cannot add independent target-cue evidence. Files ending `.sstate` were not opened or restored; only screenshot PNGs and textual logs/JSON were used.

The repo tree has the agent and audit helper, unit tests, workflows, and static-analysis documents. `docs/ROM_STRUCTURE.md` and `docs/RESOURCE_CATALOG.md` state that the analyzed ROM/extracted binaries remain outside Git. No game executable, extracted resource binary, or UI-renderer implementation is available in the allowed repo; the image classifier is not source for the game's renderer.

**Classification:** `VERIFIED` — matched initial states and the observed differences/no-differences described above; latest monitor player result is gated skip/no-go. `HYPOTHESIS` — LEFT-induced viewport movement/HUD unocclusion explains badge exposure. `UNKNOWN` — unique submenu target cue. Maintain `barrier_level_selection=WAIT`, readiness `NO-GO`, Story Mode `NOT COMPLETE`; leave Revision65 marker and cue token unchanged. Minimum acceptable next evidence is a distinct authenticated A/B with the same candidate tile unobstructed in both branches and a repeatable tile-anchored selection cue, ideally accompanied by matching tile-specific stats-panel change.

---
# Offline audit log — Revision59 adds no unique barrier-target discriminator (24 October 2026)

## Checkpoint verified
HEAD `main` at audit start: `d253a0f8ef8c7eb5b5acc618314c03acc70c86f1`; code/test checkpoint `c0b7d48933d37f59914d82a4bfeab4100d836a1e`. Current relevant Actions #40071317759 passed 35 tests and all steps. No active run appeared among the ten newest Actions API results.

## Distinct artifact reviewed offline
Run [#39907655833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39907655833), artifact `12482055310` (Revision59). Inspected only its authentic screenshot PNGs and text logs/decision JSON; no savestate was opened, and no emulator, restore, continuation, or gameplay input was run.

The A/B branches do not begin in the same state:
- C01 begins at `barrier_choice`, where the historical decision was Circle. The prompt `結界をレベルアップしますか?` (Apakah penghalang akan dinaikkan levelnya?) presents `はい` (Ya), `いいえ` (Tidak), and `マップ` (Peta); C01 is in `barrier_level_selection` by F60.
- C02 begins in `barrier_level_selection`; its historical Circle press did not change the observed state by F100.
- Both branches’ submenu prompt is `レベルアップする結界をえらんでください` (Pilih penghalang yang akan dinaikkan levelnya); footer `けってい` (Konfirmasi/pilih, Circle), `もどる` (Kembali, X). These are instructions, not an identifier of the selected tile.

## New offline measurements (negative only)
Using the calibrated mask approach already present in the regression workflow, candidate badge-ring counts around the pink-60 object at F60/F100/F110/F180 were C01 `0, 67, 59, 0` and C02 `52, 67, 67, 64`. No sample exceeds the unknown-context ceiling 100; the known map-UP positive reference is 811. The broad statistics-panel ROI’s gold-mask count stayed around 2,559–2,566 pixels, below the 5,000-pixel map-positive threshold. The bright-text mask in the lower submenu instruction-panel ROI had zero changed pixels across sampled within-branch submenu transitions (F60→F100, F100→F110, F110→F180). Footer-region changes are not treated as a cue because the area includes changing footer/glyph content and is not tile-specific.

Interpretation limits: the thresholds were calibrated in map context; their absence is useful negative evidence, not proof that no other cue exists. Since C01/C02 initial states are mismatched, the artifact cannot establish a controlled action-versus-WAIT selection delta. No unique tile-attached ring + corresponding tile-information panel + panel-text transition was found. The result therefore does not satisfy the target-cue gate.

## Code/source check
`tools/storymode_adaptive_agent.py` v0.4.0 uses screenshot color/ROI features; in `barrier_level_selection` it returns WAIT with reason `barrier_target_not_identified; fail_closed_until_controlled_probe`. `tools/levelup_target_cue_audit.py` explicitly validates only a known map-context signature and is not used to authorize gameplay input. No game UI renderer implementation or game executable is checked into the inspected tree, so repository-local source-rendering analysis cannot currently establish the missing cue.

## Result
**VERIFIED:** Revision59 is a distinct historical artifact; it contains a state transition into the submenu in C01.  
**UNKNOWN:** whether the candidate pink-60 tile is the selected target in the nested submenu.  
**Policy:** `barrier_level_selection = WAIT`; readiness **NO-GO**; Story Mode **NOT COMPLETE**. Keep the Revision65 marker blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` unchanged and keep the cue token absent. No private artifacts were added to Git. The prior successful regression was not rerun because this update is documentation-only.

Next: search existing authenticated evidence for a same-start-state action/control pair with the candidate tile visible and unobscured. If none exists, retain UNKNOWN/WAIT and require explicit review/authorization before any new experiment. Known Story Mode dialogue must be skipped with START, not Circle; Japanese text must carry Indonesian translations inline.

---

# Verified card-detail Circle confirmation from historical authenticated A/B — 24 October 2026

**Policy/test commit:** `c0b7d48933d37f59914d82a4bfeab4100d836a1e`. **Actions #40071317759:** `success`; 35 tests in 5.370 seconds; all workflow steps passed.

## New offline finding

Inspected the authenticated private artifact `12480355608` from historical adaptive run [#39904097181](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39904097181), Revision56, whose explicit A branch presses CIRCLE and whose control branch sends no input. The F20 action/control captures are pixel-identical (1,024,000 identical RGB pixels). At F60, they diverge by 127,598 pixels with mean absolute RGB difference 9.04858. Historical logs confirm CIRCLE press readback `true`, a single action-branch press, zero control-branch presses, and a valid A/B report. The action branch then renders a dialogue at F60 / reaches `map_after_move` by F100; the no-input branch remains on `card_selection_detail` through F180.

This is a verified state transition for the **revealed-card confirmation state**, not for the level-up barrier submenu.

## Policy and regression implementation

The screenshot classifier was advanced to version 0.4.0. `card_selection_detail` is actionable only when the blue/white revealed-card conditions remain true and the narrowed lower-right Circle-glyph ROI `(1030,665,1105,712)` meets red-mask ratio `>= 0.12`. A visually similar reveal without a clearly visible confirm glyph is now classified as `card_selection_detail_unconfirmed` / `WAIT`. Stable, glyph-confirmed `card_selection_detail` recommends `CIRCLE`. The new decision is scoped to this state only; the barrier-submenu branch still always returns `WAIT`.

Updated regression workflow step downloads the already-existing historical Revision56 artifact temporarily and checks:
- all ten expected state/action classifications from C01 action and C02 control frames;
- identical C01/C02 source frames at F20 and a sufficiently large action/control difference at F60;
- historical log evidence for CIRCLE press/readback and a no-input control;
- all prior card-overlay, Revision53, pink-badge, map-vs-submenu composite, and historic LEFT→Circle fail-closed checks.

The first implementation regression [#40071223499](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40071223499) stopped at one synthetic-test failure: the initial glyph ROI overlapped the bottom orange/gold border, so a no-glyph fixture incorrectly exceeded the threshold. The ROI was narrowed to the glyph interior area and the complete corrected suite passed in [#40071317759](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40071317759).

Japanese strings from the authentic card screen:
- `ゲットする札をえらべ!` (Pilih kartu yang akan didapatkan!)
- `守` (Lindungi/Bertahan)
- `防御集中` (Konsentrasi Pertahanan)
- `気合いをいれて守る。防御技の消費チャクラが0になります。` (Bertahan dengan penuh semangat. Konsumsi chakra untuk teknik pertahanan menjadi 0.)

## Decision boundaries

`card_selection_detail` may now recommend Circle only with the specific revealed-card art plus confirm glyph. `card_selection_detail_unconfirmed` is WAIT. The nested barrier level-up target remains `UNKNOWN` / `WAIT`; the map-only focus ring + matching statistics panel + panel-text-change composite still fails in both submenu branches. Pink badge pulse/exposure and the kunai/foreground sprite remain excluded as target cues.

No emulator, restore, continuation, or gameplay input was started in this session; this was an offline review of historical private artifacts and a CI regression. ROM/BIOS/Memory Card/savestates/screenshots/private evidence remain outside Git.

**Next:** find independent evidence for a cue physically tied to the selected barrier tile in the nested level-up submenu, or inspect UI rendering/source-level behavior. Do not alter the consumed marker, add the cue token, or run gameplay before that gate is independently satisfied. Dialogue must use START to skip; translate Japanese inline in Indonesian parentheses.

---

# Historical LEFT→Circle evidence regression — 24 October 2026

**Workflow/test commit:** `e0f3c49f735a7a518399cef1457e8233affec43e`. **Actions #40069923244:** `success`; 34 tests in 5.114 seconds; new authenticated frame step passed.

Added a regression-only download of private artifact `12495906030` from historical run [#39940196133](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39940196133), whose A branch used LEFT then Circle and whose C02 branch was the no-input control. All ten authentic screenshots are classified by the current agent as `barrier_level_selection` / `WAIT`; output: `AUTHENTIC_HISTORICAL_LEFT_CIRCLE_BARRIER_POLICY=PASS checked=10 all_wait=true`. This reduces the chance of an unintended input from that historical submenu composition, but it does not reveal target semantics.

Offline pixel inspection also notes that the separate UP action artifact (#39942178665 / artifact `12496637328`) exposes the pink `60` badge fully; however, the current calibrated red focus-ring metric remains only 66, 58, 66, and 80 pixels at F60/F100/F110/F180. The known map-UP reference is 811 ring pixels plus the corresponding tile-information panel. The fully exposed submenu badge has no matching arrow ring nor a tile-specific stats panel. In the LEFT branch, the badge remains partly behind the fixed HUD. Neither action view establishes a unique selected target.

Decision remains `barrier_level_selection = WAIT`, cue `UNKNOWN`, adaptive readiness `NO-GO`, Story Mode `NOT COMPLETE`. The Revision65 marker blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` stays unchanged, and the cue token stays absent. Regression only; no gameplay input/emulator/restore/continuation was launched. Do not use the new test pass as authority to run the player.

**Next:** inspect a truly new authenticated observation or analyze source-level rendering/UI logic to locate a cue unique to the candidate tile. If not found, preserve UNKNOWN/WAIT. START remains the only dialogue skip button; never use Circle to skip dialogue.

---
## Previous analysis — Revision64/65 cross-run duplicate audit (24 October 2026)

Private authenticated screenshot artifacts from Revision64 (run #39942178665, artifact #12496637328) and Revision65 (run #39947481094, artifact #12498688466) were downloaded to temporary analysis storage and compared. No screenshot or save-state file was added to Git.

## Cross-run duplicate check

All ten same-branch/same-frame PNG pairs (`C01` and `C02` at F20/F60/F100/F110/F180) are pixel-identical across the two artifacts. Each pair has 0 differing pixels and mean absolute RGB difference 0.000000. Revision64 logs one UP@F30 press/release in C01 and no input in C02. Revision65 logs UP@F30 and Circle@F70, with PAD readback true/false, but renders the same ten screenshots as Revision64. Both artifacts classify every capture `barrier_level_selection` / `WAIT`.

This strengthens the negative finding: Circle was delivered in the historical Revision65 experiment but created no visible change in the captured frames. It does not establish that the button is universally ineffective; it establishes only that this evidence does not verify target selection or confirmation. Revision64/65 are duplicate visual observations and must not be treated as independent trials.

## Cue review and disposition

Badge color/pulse and screen position remain non-unique due the existing UP/WAIT shared pulse and the camera/HUD-occlusion confound. The known map-only positive cue remains a red directional arrow ring together with a matching information panel and panel-text transition; the nested submenu does not meet that composite. The blue/orange proxy is within the foreground kunai sprite exclusion area. Character pose is not cursor evidence. The instruction/footer do not change in the captured observations and no tile-specific information panel appears.

Japanese text seen in the authentic submenu: `レベルアップする結界をえらんでください` (Pilih penghalang yang akan dinaikkan levelnya); `けってい` (konfirmasi/pilih, Circle); `もどる` (kembali, X).

Decision remains `barrier_level_selection = WAIT`, unique submenu cue `UNKNOWN`, adaptive readiness `NO-GO`, Story Mode `NOT COMPLETE`. Consumed marker blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` is unchanged and the cue token remains absent. No gameplay input, emulator, restore, or continuation was launched for this analysis. The existing regression run #40066679351 remains the latest verified code test: 34 tests and all 15 steps passed; this evidence update is documentation-only and did not warrant rerunning it.

**Next offline action:** use only a distinct existing authentic artifact that reveals the candidate tile in both action and control without fixed-HUD obstruction. Do not count Revision64 and Revision65 twice. If no suitable artifact is already available, preserve UNKNOWN/WAIT and do not bypass the fail-closed gate.
## Previous analysis — offline badge-pulse cue exclusion (24 October 2026)

**Code/test commit:** `885d9889215a4fdca6b276daadd8a431f8177c51`. **Regression:** [GitHub Actions #40066679351](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40066679351) — `success`, 34 tests in 3.176 s, all 15 workflow steps passed. Inputs were the already-authenticated private screenshot artifacts from runs #39947481094 and #39786019434. No gameplay/emulator/restore workflow ran.

## Finding: pink badge animation is shared across UP and WAIT

The new offline regression samples the interior pink badge at the same frames in map UP and map WAIT, separately from terrain, HUD and the character sprite:

| Frame | Map UP mean RGB | Map WAIT mean RGB | Distance |
|---|---|---|---:|
| F60 | (237.5, 39.2, 140.7) | (235.1, 37.5, 138.4) | 3.74 |
| F100 | (215.6, 69.1, 118.5) | (213.4, 65.6, 116.2) | 4.79 |
| F110 | (206.7, 65.1, 103.4) | (202.3, 62.8, 101.0) | 5.48 |
| F180 | (238.2, 39.4, 141.1) | (237.7, 39.5, 140.8) | 0.62 |

All four frame-pairs differ by at most 5.48 RGB units. This validates the new negative discriminator: the badge's pulse/color alone does not distinguish selected from WAIT in the known map context. The pure helper `same_badge_pulse_across_contexts` validates aligned frames and finite channel values, fails closed on malformed/missing samples, and is kept in the offline audit module rather than the gameplay action policy. Its dedicated test checks shared pulse, malformed/missing samples, stricter thresholds, and a deliberately changed phase.

Regression output from the corrected Actions run:

- `PINK_BADGE_PULSE_REGRESSION=PASS frames=4 max_rgb_distance=5.48 same_phase_across_UP_WAIT=true pulse_alone_is_not_a_unique_selection_cue=true`.
- Existing composite: `map_UP=ring:811,panel_gold:8312,text_delta:635`; `map_WAIT=ring:62,panel_gold:8629,text_delta:15`; `submenu_UP=ring:66,panel_gold:2452,text_delta:3221`; `submenu_WAIT=ring:67,panel_gold:2566,text_delta:39`.
- `LEVELUP_TARGET_CUE_REGRESSION=PASS`, which rejects both submenu branches and retains `target_role=UNKNOWN input_policy=WAIT`. Terrain movement remains +100 px for UP and 0 px for WAIT; kunai mask excluded from cursor evidence.

The earlier run [#40066588970](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40066588970) failed in the new screenshot step because only four map frame filenames had been loaded, despite all ten being present in the private artifact. The loop was corrected in `885d988` to load both branches at F20/F60/F100/F110/F180; run #40066679351 validates the corrected workflow. The earlier failure is a test-fixture issue only.

## Gate remains closed

`barrier_level_selection` remains **WAIT**; submenu cue remains **UNKNOWN**; readiness is **NO-GO** and Story Mode **NOT COMPLETE**. Revision65 marker blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` remains consumed and unchanged. `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` remains absent. The player gate is still before private source-checkpoint download and PAD override. No gameplay input, player, emulator, restore or continuation was launched, and no private screenshot or game asset was committed.

**Next offline task:** seek a unique cue registered to the candidate tile in the nested upgrade submenu. Require the red focus ring plus the corresponding changing tile-information panel in that submenu itself; neither badge pulse nor map-only evidence is sufficient. Retain the full marker/allowlist/fail-closed review before any future input.

---

# Prior checkpoint: screenshot crop correction — foreground kunai is not a target cursor (24 October 2026)

## Verified crop correction — 24 October 2026

**Source/test commit:** `96e9c22089e257facf2be3359ead33deed117583`. **Regression:** [GitHub Actions #40065597290](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40065597290) — `success`; 33 unit tests passed in 4.297 seconds and all 15 workflow steps passed, including authentic screenshot checks for the prior X11/card/Revision65/map evidence.

Visual inspection of the existing private/authenticated crops from Revision65 artifact `12498688466` (run #39947481094) and map UP-vs-WAIT artifact `12428777970` (run #39786019434) identified a classification error in the previous analysis: the blue/orange mask ROI `(620,295,735,390)` is part of the character's hand-held kunai/foreground sprite ROI `(540,290,750,560)`, not an independent UI pointer. Therefore the old 8.38/7.17/5.01/5.03 px motion values and pointer-to-tile distances must **not** be interpreted as cursor evidence. They are superseded as a pointer hypothesis; no target-selection signal can be inferred from this ROI.

The regression now asserts that the former proxy ROI is contained inside the foreground-sprite exclusion ROI, labels it `cursor_or_target_evidence=false` and `cue_eligible=false`, and removes the misleading pointer-centroid and screen-anchor claims. The authentic terrain/camera-pan and ring/panel audit remains unchanged: Map UP ring/panel/text = 811/8312/635; Map WAIT = 62/8629/15; Revision65 submenu UP = 66/2452/3221; submenu WAIT = 67/2566/39. The composite still rejects both submenu branches. The pink badge's +97.46 px visible-centroid shift against a +100 px scene shift remains consistent with camera pan/HUD unocclusion, not proof of target selection.

**Decision remains fail-closed:** `barrier_level_selection = WAIT`; the submenu target cue remains **UNKNOWN**; adaptive-player readiness **NO-GO**; Story Mode **NOT COMPLETE**. Consumed marker `experiments/.run-storymode-adaptive-player` is unchanged at Revision65, blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`; the cue token remains absent. No player, emulator, restore/continuation, or gameplay-input workflow was launched; all screenshots, ROM/BIOS, Memory Cards, savestates, and private evidence remain outside Git.

**Next:** continue offline with the existing authentic screenshots, examining a cue spatially attached to the actual candidate tile and independent of background motion, HUD exposure, and foreground pose. Do not add the cue token, change the consumed marker, or run gameplay before independent verification and explicit review of marker/allowlist/fail-closed gates.

---

# Offline submenu cue composite audit — 24 October 2026

**Code/test commit:** `d1c0428381581b80814bebf6557f5579594bb9da`. **Regression:** [#40064182088](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40064182088) completed `success` at 04:55:20 UTC / 11:55:20 WIB. All 33 tests passed in 4.872 seconds; all 15 workflow steps and existing authenticated screenshot checks passed.

## New measured discriminator

All image measurements are offline, using existing private PNGs only: Revision65 A/B from run #39947481094 and the known map UP-vs-WAIT reference from run #39786019434. The regression computes three features around a candidate target and its expected stats panel:

- red directional focus-ring pixels, with candidate tile body masked out (minimum 500);
- gold-frame pixels in the registered stats-panel ROI `(150,340,545,540)` (minimum 5,000);
- XOR count for a bright-text mask (minimum 100) inside that panel between F20 and F60.

| Context | Ring | Stats-panel frame | Panel bright-text mask delta | Composite outcome |
|---|---:|---:|---:|---|
| Map UP | 811 | 8,312 | 635 | positive reference |
| Map WAIT | 62 | 8,629 | 15 | reject: no ring/text transition |
| Revision65 submenu UP | 66 | 2,452 | 3,221 | reject: ring and panel footprint absent |
| Revision65 submenu WAIT | 67 | 2,566 | 39 | reject |

The stats-panel footprint is a required precondition. The submenu UP bright-text mask changes by 3,221 pixels in the same broad registered ROI, but the expected gold panel frame is only 2,452 pixels and the focus ring is 66; this is a strong false-positive demonstration for text/pixel deltas alone. The four lower-left prompt comparisons (UP F20→F60, UP F60→F100, WAIT F20→F60, WAIT F60→F100) all have zero changed bright-text mask pixels, so the instruction text itself did not change according to this mask. This does not prove what every unmasked pixel means; it establishes that the new composite rejects the known ambiguous submenu frames.

The pure helper `tools/levelup_target_cue_audit.py` applies thresholds fail-closed, rejects missing/malformed/negative inputs, and is not imported into the gameplay agent. Its unit test covers positive map reference, map WAIT, submenu false-positive, missing panel transition, missing footprint, and missing data. The workflow adds `LEVELUP_TARGET_CUE_REGRESSION=PASS` only after verifying map UP matches while map WAIT and both submenu branches do not.

## Decision and operational containment

- `barrier_level_selection` remains **WAIT**; submenu target semantics remain **UNKNOWN**.
- Marker `experiments/.run-storymode-adaptive-player` stays consumed at Revision65 (blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`); cue token stays absent.
- Readiness **NO-GO**; Story Mode **NOT COMPLETE**.
- No player, emulator, restore/continuation, or gameplay-input run was launched. The current run was regression-only and consumed existing screenshot artifacts. No screenshot or game asset was committed.
- Known monitor failures #40048510714, #40034304421 and #40010286618 are from stale gated player run #39975090690 (`skipped`, no valid evidence artifact); they are monitor alerts, not proof of gameplay failure or progress. The monitor-policy regression #40061712532 passed. Do not run gameplay to make the monitor green.

**Next offline work:** inspect existing authenticated submenu screenshots for a unique indicator spatially registered to a candidate tile and independent of scene pan, HUD exposure, and sprite pose. A cue in the map context is not enough to authorize the submenu. Require an independently verified submenu cue, explicit new marker review, full allowlist review, the pre-download/pre-PAD gate, and passing regression before any future bounded input trial.

---

# Offline pointer screen-anchor regression + monitor fail-closed policy — 24 October 2026

**Source/test commit:** 6d2fdc4553f5eacabf2607c19ebf69bc012c2c51.  
**Regression:** [#40061967694](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40061967694) — success; 32 tests passed in 4.630 s, authentic X11 regression passed for 10 observations, and all 15 final job steps completed successfully.  
**Monitor policy hardening:** [#40061712532](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40061712532) — success on its source checkpoint; the current regression re-tests the same helper and integration along with the new screen-anchor check.

## New independent proxy-motion measurement

Existing private/authenticated PNG sources only: Revision65 A/B run #39947481094 and map UP-vs-WAIT run #39786019434. No emulator or player was launched. The blue-pointer proxy uses the regression workflow's exact ROI (620,295,735,390) and mask b > 100, b > 1.35*r, b > 1.15*g. F20-to-F60 centroid displacement:

- Revision65 UP: 8.38 px; Revision65 WAIT: 7.17 px.
- Map UP: 5.01 px; Map WAIT: 5.03 px.

Corresponding independently registered terrain shifts are +100 px for both UP branches and 0 px for both WAIT branches. In Revision65, the pink badge's visible centroid moves +97.46 px while the scene shifts +100 px. The screen-space proxy moves less than the new 20 px ceiling in all four branches while the scene moves by about 100 px in UP branches. New CI label: POINTER_SCENE_ANCHOR_REGRESSION=PASS.

**Interpretation:** the blue proxy stays almost screen-anchored and cannot independently mark the pink tile as selected. The already measured proxy-to-tile distances (Revision65 206.01 px; map UP 76.56 px; map WAIT 82.83 px) likewise fail to discriminate target selection. The calibrated map cue remains a red directional arrow ring **plus** a matching tile-information panel: map UP ring count 811 and panel changes to level 1/value 60/durability 2/2; map WAIT ring count 62 and panel remains empty land/value 140; Revision65 badge region ring count 66. Its prompt/footer remain pixel-identical F60→F100 in both action/control branches. Submenu target role stays **UNKNOWN**.

## Monitor correction

Added a pure-tested fail-closed health policy. Only a completed, no-artifact skipped run from a known push commit that lacks [RUN-NARUTO-STORYMODE-ADAPTIVE-PLAYER] becomes EXPECTED_GATED_SKIP_NO_GO. Manual-dispatch skips, unknown commit message, marker-bearing push, actual failures, successful run missing artifact, and overdue active runs remain warnings. This fixes the monitor's repeated false alerts on intentionally gated run #39975090690, without altering readiness or gameplay policy.

## Gate / status

- barrier_level_selection action remains **WAIT**.
- Marker experiments/.run-storymode-adaptive-player remains consumed Revision65, blob 3754a6ddf45a7570c053d9c149b6d80b0862a127; cue token remains absent.
- Readiness **NO-GO**; Story Mode **NOT COMPLETE**.
- No gameplay input, player run or restore/continuation was launched; private evidence and game assets remain outside Git.
- Next: offline terrain-registered analysis only. Do not promote the proxy or pink badge as a cue. A future trial requires independently unique submenu evidence, a reviewed new marker and the existing gate/regression.

---

# Offline pointer geometry + foreground-pose audit (24 October 2026)

**Scope:** offline analysis of previously authenticated private screenshots and regression/source-test changes only. No gameplay input, emulator run, save-state restore, or Story Mode player run was launched.

**Source code commit:** `1ec34ac934ee62ba69fe3fe43705de1221a17196`.
**Regression:** [#40059425253](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40059425253) — `success`; all 15 workflow steps passed, 27 unit tests passed in 2.978 seconds. Its screenshot evidence stages revalidated the earlier policy, card-overlay, card-detail, Revision65 and map UP-vs-WAIT datasets. The new source-only assertions passed.

## New geometry / pose results

The regression computes a secondary blue-pointer proxy from the authenticated frame ROI and measures Euclidean distance from the pink-60 marker/tile:
- Revision65 F60 badge-to-proxy: 206.01 px.
- Map UP F60 tile-to-proxy: 76.56 px.
- Map WAIT F60 tile-to-proxy: 82.83 px.
- The UP-versus-WAIT difference is 6.27 px, so this proximity feature does not independently identify a selected tile. It cannot be promoted to a verified cue.

The F60→F100 foreground-versus-background control uses separate ROIs and the terrain-shift estimator:
- Branch 1: scene shift 0 px; foreground sprite changed 22.312%; terrain ROI changed 1.467%.
- Branch 2 / WAIT control: scene shift 0 px; foreground sprite changed 18.891%; terrain ROI changed 1.468%.
- Instruction-panel and confirm/back footer crops remain pixel-identical (0 changed pixels) F60→F100 on both branches.
- Revision65 red-ring counts across F60/F100/F110/F180 are 66, 58, 66, 80. None reaches the ring threshold of 100. The positive map reference remains 811 ring pixels plus matching panel in UP, compared with 62 ring pixels in map WAIT.

Together with the already independently registered +100 px F20→F60 terrain shift and +97.46 px visible badge-centroid shift, this supports camera pan/unocclusion as a sufficient alternative explanation for the badge becoming visible. Foreground changes after F60 are not evidence of selection. The geometry assertions and pose-exclusion assertions are now in the workflow and source unit tests.

## Decision — unchanged

The pink `60` badge is associated with a barrier-value tile in map context, but its role as the selected target in the upgrade submenu is still **UNKNOWN**. The testable hypothesis remains: a target cue requires an arrow-ring signal spatially surrounding the candidate tile **and** a matching information-panel transition. The positive map example has both; Revision65 submenu frames do not.

Keep `WAIT` for `barrier_level_selection`; keep the marker at consumed Revision65 with no `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1`; do not launch the player, restore chain, or new gameplay input. Readiness remains **NO-GO**, Story Mode remains **NOT COMPLETE**.

## Repo / workflow validation

The tested code commit is `1ec34ac934ee62ba69fe3fe43705de1221a17196`, and the current run #40059425253 reports success. The only code paths changed by that commit are `.github/workflows/naruto-storymode-adaptive-regression.yml` and `tests/test_storymode_adaptive_agent.py`. The three checkpoint docs are being updated separately after the regression passed. The marker blob remains `3754a6ddf45a7570c053d9c149b6d80b0862a127`.

The scheduled monitor still fails on runs #40010286618, #40034304421 and #40048510714 because it treats the intentional player run #39975090690 (`skipped`, no valid player artifact) as an alert. This is an automation-monitor issue and not an indication of new game progress. The player monitor should eventually understand the deliberate NO-GO state, but modifying that is separate from resolving target semantics.

## Next offline task

Use a registered coordinate system to compare candidate tile boundaries, the blue-pointer proxy and the known red-arrow-ring/panel composite across the existing map UP/WAIT reference and the submenu frames. Keep terrain, fixed HUD/panel and foreground character as separate masks. Only change UNKNOWN if a visually unique cue is supported by independent evidence and an authentic regression. Any later gameplay trial requires a new marker revision, the existing pre-download/pre-PAD cue gate, a tested allowlist, and successful regression. Identifiable dialogue uses START rather than Circle; Japanese text must be followed immediately by its Indonesian translation in parentheses.

---

# Latest checkpoint — measured camera-pan confound regression PASS (23 October 2026)

Run [#39955066779](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39955066779) completed with `success` against code commit `6ac013fc76c8d82417305bfbfabeac4c6a73876a`. The expanded regression passed 24 tests, 10 authentic X11 policy checks, 5 authentic card-overlay checks, 10 authentic revealed-card-detail checks, ten Revision65 frame validations, the map UP-vs-WAIT panel/marker assertions, and the new NumPy scene-shift assertion.

## Measured screenshot findings

- Pixel-only regression estimates: Revision65 UP `+100px`, Revision65 WAIT `0px`, map UP `+100px`, map WAIT `0px`. It passes with `CAMERA_SHIFT_REGRESSION=PASS`.
- Independent offline ORB/RANSAC registration: Revision65 UP estimated translation (x=+0.03,y=+100.40) px, scale 1.0000, 0.01° rotation, 1,372/1,433 inliers (95.7%), median residual 0.49 px. Revision65 WAIT: (x=+0.01,y=+0.01) px, 3,289/3,301 inliers (99.6%), median residual 0.00 px. Map UP: (x=+0.10,y=+100.58) px, scale 0.9999, 682/918 inliers (74.3%), median residual 0.50 px. Map WAIT: (x=+0.01,y=+0.01) px, 2,715/2,738 inliers (99.2%), median residual 0.01 px.
- Registration from Revision65 F60→F100, F100→F110, and F110→F180 estimates no material scene translation in either branch. Separately, instruction-panel and confirm/back-footer crops remain exactly pixel-identical F60→F100 after Circle (zero changed pixels on both branches).
- Cross-context panel assertion remains: map UP panel delta 16,239 pixels versus WAIT delta 94; pink-60 ROI pixels 1,893 in UP versus 75 in control. The Revision65 badge was partly present in the baseline under the HUD (142 pink-mask pixels), then exposed in the UP scene ROI (2,681); WAIT had 0 there.

## Interpretation and gate

This shows that the scene-pan confound is real and reproducible: both UP runs move the visible map scene about 100 px vertically, and both WAIT controls do not. The badge is a barrier-value symbol in known map context, but **its role as a selected target in the level-up submenu is still UNKNOWN**. A camera pan can explain its appearance in the fixed ROI; the measurements do not prove whether a target selection also occurred. The stable scene after F60 and the unchanged prompt/footer after Circle provide no visual confirmation of target selection or level-up confirmation.

Keep classifier action `WAIT` for `barrier_level_selection`; keep `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` absent; do not rerun consumed Revision65 or dispatch another player run. Readiness remains **NO-GO** and Story Mode remains **NOT COMPLETE**. Next work stays offline: register background/terrain landmarks and compare the pink tile's relation to the game cursor separately from viewport movement. Any new input trial requires an independently established, unique target cue plus a pre-tested marker/state gate.

The regression and documentation updates did not modify the player workflow or Revision65 marker. All authentic screenshots/save-state artifacts remain private and out of Git.

---

# Latest checkpoint — cross-context target-cue regression PASS (23 October 2026)

Regression [#39954571305](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39954571305) finished with `success` against code commit `61fd13189de5496631ca7a37900b64f4e50330ee`. It passed 24 unit/source tests, 10 authentic X11 policy checks, 5 authentic card-overlay checks, 10 authentic revealed-card-detail checks, all ten private Revision65 frame checks, and the new cross-context evidence assertions. The immediately preceding run `#39954326794` failed only due to a Python heredoc indentation defect, which was corrected before this successful run.

Measured private screenshot assertions:
- Revision65 F20 had 142 pink-mask pixels in the under-HUD partial-badge ROI; after UP the fixed exposure ROI contained 2,681 pink-mask pixels; WAIT control contained 0. This supports camera-pan/unocclusion as a real confound, not proof of a selected target.
- In map UP-vs-WAIT, the information panel changed 16,239 pixels in the UP branch and 94 in WAIT control; the pink-60 tile ROI contained 1,893 pink-mask pixels in UP and 75 in the same control ROI. Visual reference shows red directional arrows around the selected pink-60 tile and a matching panel: Level 1, barrier value 60, durability 2/2. WAIT retained empty-land / value-140 information.
- Revision65 instruction-panel and confirm/back footer ROIs remain pixel-identical F60→F100 after Circle on both branches.

**Decision:** meaning of pink 60 as a barrier-value symbol in map context is corroborated; role as the level-up target cursor remains **UNKNOWN**. The camera-pan/unocclusion hypothesis is plausible and remains **not conclusively proven**. Keep policy `WAIT` in `barrier_level_selection`, keep `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` absent from the marker, do not rerun Revision65, do not start another player run, and do not authorize random directional input.

HEAD at audit-run completion was `61fd13189de5496631ca7a37900b64f4e50330ee`; this documentation update records the result only. Marker revision65 remains unchanged. Readiness remains **NO-GO** and Story Mode remains **NOT COMPLETE**. Next action: offline visual/ROI registration around map landmarks and the arrow-plus-panel selection cue; define an independently distinguishable target observation before any new input trial. Keep all authentic images and save-state artifacts private/out of Git.

---

## Regression workflow repair — 23 October 2026

The first run with the new cross-context assertions, [#39954326794](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39954326794), failed at the final Python report line because that line had one extra indentation level in the workflow heredoc. The run reached the new cross-context step, and earlier synthetic/authentic checks passed, but the final cross-context assertions did not finish. This was a workflow-source formatting defect, not new gameplay evidence.

The report-line indentation is corrected in the follow-up commit. A fresh regression must finish with `success` before any input experiment is considered. No player workflow or marker was changed; Revision65 remains consumed, target role remains UNKNOWN, barrier submenu policy remains WAIT, readiness remains NO-GO, and Story Mode remains NOT COMPLETE.


---

# Latest checkpoint — cross-context pink-60 / target-cue audit (23 October 2026, WIB)

**Scope:** private authenticated screenshots only; no gameplay run was started. HEAD at the start of this audit was `4b8e9f60cf72354238a98bca32cf7a40baf905b1`. Latest regression [#39952866478](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39952866478) was `success`; Revision65 player run [#39947481094](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39947481094) was `success` and its marker is consumed. The 10 most recent Actions entries checked were completed; no player run is active in that checked set.

## Cross-context evidence

- Private Revision65 artifact `#12498688466` (run `#39947481094`) and earlier map UP-vs-WAIT artifact `#12428777970` (run `#39786019434`) were downloaded for local inspection only. Neither artifact nor any image/save-state was added to Git.
- **Known map-selection reference:** at C01-F20, the map selection panel describes empty land: `空き地` (tanah kosong), `レベル ---` (Level ---), `結界価値 140` (Nilai penghalang 140), `耐久値 -/-` (Daya tahan -/-). A pink hex tile labelled 60 is already visible above the selected tile; red directional arrows surround the selected blue 140 tile. After UP, C01-F60 shows those arrows around the pink 60 tile and the panel changes to `レベル 1` (Level 1), `結界価値 60` (Nilai penghalang 60), `耐久値 2/2` (Daya tahan 2/2). In the WAIT control, the panel remains on empty land / value 140. This cross-reference defines a *known map-selection cue combination*: focus arrows around one tile plus matching tile-information panel—not pink color/number alone.
- **Revision65 submenu:** the pink 60 badge is partially visible beneath/behind the fixed HUD at F20, before UP. After UP, the terrain/character composition shifts and the badge is exposed in a different screen region. There are no visible red focus arrows around that badge, and no tile-specific Level / barrier-value / durability panel; the instruction remains `「レベルアップする結界をえらんでください」` (Pilih penghalang yang akan dinaikkan levelnya). The footer remains `けってい` (konfirmasi/pilih, Circle) and `もどる` (kembali, X). From F60 to F100, the instruction/footer ROIs have exactly zero changed pixels in both A/B branches after Circle.
- **Interpretation:** the badge matches a barrier-value tile in the map context, but its role as a selected level-up target remains **UNKNOWN**. The presence of a pre-input, partly occluded badge plus the camera/scene shift makes camera-pan/unocclusion a concrete alternative hypothesis to cursor selection; it is not yet proven either way. The Revision65 success does not authorize a target-selection claim.

## Safety decision and next steps

- Classifier policy remains `WAIT` in `barrier_level_selection`; readiness remains **NO-GO**; Story Mode remains **NOT COMPLETE**.
- Marker `experiments/.run-storymode-adaptive-player` is intentionally unchanged at Revision65 and contains no `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1`. Do not add that token, dispatch the player, repeat Revision65, or issue random-direction input.
- Add an authentic cross-context regression that loads the old private map UP-vs-WAIT artifact, asserts the map information-panel delta is present only in the action branch, asserts the pre-input pink badge / post-UP exposure pattern in Revision65, and keeps WAIT plus the token gate fail-closed. Run regression only; do not run the player.
- After regression passes, next research is offline screenshot/ROI registration: compare map landmarks across F20/F60 to model pan/pose change and keep focus-cue evidence separate from badge visibility. Any later input experiment requires an independently identified target cue and a new marker revision; the current marker remains consumed.

Do not promote either Revision65 output checkpoint. Keep ROM, BIOS, Memory Card, savestates, and authentic screenshots private/out of Git. For actual dialogue only, use START—not Circle—and translate Japanese text beside it in Indonesian.

---

## Revision57 result — chained gameplay progress, 23 October 2026

Run [#39904672868](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39904672868) completed successfully. It restored revision56's CIRCLE-action checkpoint and ran two bounded sessions in fresh emulator processes, capturing ten authentic 1280x800 external-X11 frames and validating both output savestates. Logs confirm:
- cycle 1: `before=dialogue action=START observed_after=map_after_move state_changed=true`;
- cycle 2: `before=map_after_move action=WAIT observed_after=barrier_choice state_changed=true`;
- sequential fresh-process checkpoint continuation and visual deltas passed.
Output checkpoint cycle 2: `adaptive-cycle-02-f180.sstate`, 21,163,287 bytes, SHA-256 `d487b8ac7cc3d90b543865ef1831acd696df41337e447472f6faa41acdaada1d`.

This is actual observed gameplay-state progression, but **not proof of a completed turn, mission, or Story Mode**. The system is usable for further bounded adaptive continuation but is not yet a proven hands-off Story Mode finisher. The next run continues from the barrier-choice checkpoint and should only take the calibrated CIRCLE branch if YES is visibly selected; otherwise it safely waits. Continue from this checkpoint rather than restarting.
 
---

## Strategy reset — 23 October 2026, after revision56

The objective is to **reach Story Mode completion through adaptive play**, not to prove every single game rule before attempting the game. The previous sequence spent too much time in narrowly-scoped validation; from this checkpoint onward, experiments should be limited to blockers that prevent progress.

### Revision56 result — successful matched action/control run

Run [#39904097181](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39904097181) succeeded. The branches began from identical parent checkpoint SHA-256 `475d40dc3b966060ad110fe46c060058030aa4d7bbd24df8e30f906b90cc1dd9`, with pixel-identical F20 states. Exactly one CIRCLE press/release was registered on the action branch; the control branch did not press a button. The action branch then classified F60 as `dialogue`, F100 as `map_after_move`, and F180 as `dialogue`; control remained `card_selection_detail` through F180. Both output checkpoints passed v4-header, size and SHA validation.

**Verified:** CIRCLE from the revealed-card detail state causes a different downstream visual/game state from waiting, reaching dialogue/map-transition-looking states in this run. **Not yet verified:** whether that action formally acquires the card, its strategic effect, or whether the later board transition counts as a completed turn. Output action checkpoint candidate: `adaptive-cycle-01-f180.sstate`, 21,163,141 bytes, SHA-256 `9df5b924478fb22c427735dc186e481c1cea0ff12900134eab94711352c30742`.

### Immediate strategy

Run revision57 in normal adaptive continuation mode using the action-branch checkpoint above as its source. Perform two bounded sessions chained through a newly written checkpoint; use screenshot observation, classifier decisions, real START presses to skip visible dialogue, and save-state validation. Do not run a restore-only or another matched A/B merely to re-prove already demonstrated mechanics. The immediate success criterion is a safe adaptive action followed by an authentic state change and valid resumed checkpoint. If this succeeds, continue chaining bounded gameplay runs and investigate only blockers such as battle decisions, no-progress loops or crashes.

The classifier still fails closed on untrained battle/unknown states; this can stall progress and should be the next practical blocker to address if encountered, rather than a reason to postpone all gameplay. No claim of full unattended play or Story Mode completion is permitted until a chained player demonstrates sustained progress and an authentic ending/results screen is privately verified.

Permanent boundaries continue: use only this research repository; keep the ROM, BIOS, savestates, Memory Cards and screenshots private (never commit them); translate Japanese text immediately into Indonesian in parentheses; use START for dialogue, not Circle.
 
---

## Catatan kronologis — merge Memory Card dan uji pertama (19 Oktober 2026)

Draft PR #1 telah ditinjau, diperbaiki, dan di-merge sebagai [commit 9dc876f08d724b6f809c6da4e2dbea1b549b9d62](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/9dc876f08d724b6f809c6da4e2dbea1b549b9d62). Perubahan memasang Memory Card slot 1 lewat `-memcard1`, menyimpan file kartu dan manifest ukuran/SHA-256 dalam artifact privat 7 hari, gagal tertutup untuk pemulihan kartu yang hilang/tidak cocok, menjadikan savestate opsional, serta membatasi job 35 menit / proses emulator 25 menit.

Runner #39235643517 dibatalkan pada 17.54 WIB; artifact-nya hanya memuat savestate tersanitasi dan bukti. Screenshot terakhir menunjukkan Mode Select dengan Story Mode disorot, bukan gameplay. Uji pasca-merge [#39242130783](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39242130783) dimulai 18.05 WIB. Snapshot 18.06 WIB: verifikasi aset sukses, restore di-skip karena ini cold boot, langkah emulator berjalan, belum ada artifact/log job final. Catatan ini wajib diperbarui setelah run selesai dengan hasil nyata.

Gate penting: run awal hanya menguji pembuatan kartu/artifact. Jika tersedia, validasi file `.mcd` dan manifest; kemudian uji restore di run baru memakai `resume_run_id=39242130783`, `load_savestate=false`, dan pastikan ukuran/SHA-256 tetap cocok. Ini masih tidak membuktikan save Story Mode di dalam game. Save baru terverifikasi setelah opsi save/load nyata ditemukan, save bisa diload setelah cold boot, dan hasil terlihat pada screenshot. Story Mode belum tamat; semua dialog menggunakan START, bukan Circle.

---

## TEMUAN GDB & UJI CHECKPOINT SAFE-POINT (2026-10-19)

### Temuan GDB run #39235079514
[Run #39235079514](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39235079514) gagal saat restore, tetapi kali ini GDB benar-benar mengikuti proses emulator. Artifact #12178671125 berisi `pcsx.stdout.txt` dan peta memori lengkap. Pada thread 15 `pcsx-redux`, instruksi crash adalah `movzbl (%rsi),%ecx` di PC `0x00007ffff0dd36d0`; RSI bernilai `0xffffffffddd13fff`, alamat yang tidak valid. PC terletak di image executable `AppDir/shared/bin/pcsx-redux`; binary stripped, sehingga nama fungsi tidak tersedia. Log emulator terakhir hanya mencapai `KERNEL SETUP!`; tidak ada screenshot pasca-restore dan restore tetap gagal.
Sebelum ini run #39234894821 bukan uji emulator yang sah: quoting Bash untuk `$pc` membuat shell berhenti sebelum file `pcsx.stdout` dibuat. Itu sudah diperbaiki. Kesimpulan sementara: restore menyebabkan atau membuka jalur ke dereferensi pointer tidak valid di kode native PCSX-Redux, tetapi fungsi penyebab belum dapat dipastikan; ALSA dummy-device warning belum terbukti sebagai penyebab.

### Uji pembuatan checkpoint di safe point
[Run #39235643517](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39235643517) sengaja cold-boot tanpa memuat checkpoint lama, target 12.000 VSync. Perubahan workflow pada commit `be597ce2b4c6da6c8db34be328007806f164ddd7` mengubah semua save: callback VSync hanya meminta pause, sedangkan `PCSX.createSaveState()` dipanggil setelah emulator paused dan callback `PCSX.nextTick` masuk—bukan saat GPU masih mengerjakan callback VSync. Checkpoint periodik 5.000 VSync, pada layar non-dialog stabil, dan frame cutoff kini memakai jalur safe-point yang sama.
Run terbaru masih antre/berjalan saat catatan ini ditulis. Setelah selesai, wajib cek `STORY_CHECKPOINT_SAFE_POINT frame=... save_ok=true`, `STORY_SAVESTATE_SANITIZE=PASS`, file `storymode-checkpoint.sstate` di private artifact, screenshot sekitar checkpoint, lalu jalankan satu restore test dengan GDB. Baru setelah restore menghasilkan screenshot yang cocok, nyatakan penyimpanan dapat digunakan.
Checkpoint lama artifact #12167524755 (run #39205699071) tetap tersedia sampai 26 Oktober 2026 sekitar 13:47 WIB, tetapi berdasarkan tiga crash restore belum terbukti dapat dipakai. Jangan gunakan sebagai satu-satunya salinan progres.
Story Mode belum tamat; layar terakhir yang tervalidasi tetap dialog pembuka yang meredup. Dialog harus selalu dilewati dengan START, bukan Circle. Belum ada aturan gameplay aktif yang terverifikasi.

---

## UPDATE DIAGNOSTIK — tiga restore gagal awal; trace GDB antre (2026-10-19)

- [Run #39233746088](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39233746088) juga gagal dengan segmentation fault (exit 139) sekitar 7 detik setelah proses emulator mulai. Rehidrasi protobuf BIOS lokal lulus (`RESTORE_BIOS_REHYDRATE=PASS bios_bytes=524288 state_bytes=21162546`), tetapi tidak ada screenshot pasca-restore dan tidak ada savestate baru. Menunda load sampai first VSync, lalu pause + `PCSX.nextTick` juga belum menyelesaikan crash.
- Tiga upaya restore berturut-turut (#39232852795, #39233268705, #39233746088) gagal. Jangan retry tanpa diagnostik lagi; belum ada dasar untuk menyebut savestate aman dipulihkan.
- [Run #39234351228](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39234351228) sengaja memakai GDB untuk menangkap native stack trace saat restore gagal. Perubahan hanya untuk eksperimen diagnostik ini: paket gdb dipasang, bila run adalah restore maka AppRun dimulai di bawah `gdb --batch`, pesan Lua `STORY_/` dan `RESTORE_/` disertakan dalam log, serta `pcsx.stdout.txt`/ `pcsx.log.txt` diunggah sebagai teks di artifact privat. Raw GPU/VRAM/RAM dump tetap tidak aktif.
- Run ini masih antre saat catatan ditulis. Begitu selesai, periksa stack trace serta checkpoint loader sequence. Jika GDB menunjukkan crash dalam `SaveStates::load`/deserialisasi, validasi field protobuf dan checkpoint creation; jika crash terjadi sebelum load, periksa startup/SDL/audio or Lua initialization. Ubah hanya satu faktor dalam eksperimen berikutnya.
- Artifact checkpoint sumber #12167524755 dari run #39205699071 tetap tersedia hingga 26 Oktober 2026 sekitar 13:47 WIB. Artifact berisi savestate tersanitasi ~20,6 MB; layar saat save masih dialog pembuka yang meredup, bukan gameplay aktif.
- Story Mode belum tamat. Dialog dilewati dengan **START**, bukan Circle; tidak ada aturan gameplay yang boleh disebut terverifikasi sampai didukung screenshot eksperimen langsung.

---

## STATUS RESTORE TERBARU — rehidrasi BIOS lulus, restore masih crash; pemuatan ditunda (2026-10-19)

- [Run #39233268705](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39233268705) gagal (exit 139/segmentation fault), meskipun log mencatat `RESTORE_BIOS_REHYDRATE=PASS bios_bytes=524288 state_bytes=21162546`. Jadi menyisipkan kembali field BIOS yang tepat ke checkpoint lokal **belum cukup**; tidak ada screenshot pasca-restore, dan artifact run ini hanya ringkasan kegagalan.
- Kode Lua sebelumnya memanggil `PCSX.loadSaveState` saat evaluasi awal skrip. Hipotesis timing kini diperiksa: pemanggilan native loader mungkin dilakukan sebelum siklus emulasi siap. Ini belum terbukti sebagai akar masalah, tetapi cocok dengan crash yang terjadi sebelum log `STORY_SAVESTATE_LOAD_CALL_RETURNED` dan sebelum VSync pertama sempat dicatat.
- Commit workflow `fa220bead2da2418921b2fcc392d16b87201dd42` mengubah alur restore: pada VSync pertama, meminta emulator pause; jalankan pembacaan dan load savestate lewat `PCSX.nextTick`; setelah panggilan load kembali, reset counter observasi dan resume. Jika file tidak ada atau load melempar error, workflow gagal tertutup dan tidak diam-diam cold-boot.
- [Run #39233746088](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39233746088) menguji pemuatan tertunda tersebut; status terakhir antre. Periksa log untuk `RESTORE_BIOS_REHYDRATE=PASS`, `STORY_SAVESTATE_RESTORE_PAUSE_REQUESTED=1`, `STORY_SAVESTATE_LOAD_CALL_RETURNED=1`, exit code, dan screenshot baru. Hanya screenshot visual yang menunjukkan adegan sesuai checkpoint atau transisi yang dapat mengonfirmasi pemulihan.
- Checkpoint sumber tetap artifact privat #12167524755 dari run #39205699071; tersedia hingga 26 Oktober 2026 sekitar 13:47 WIB. Artifact itu berisi savestate tersanitasi tetapi belum bisa dipakai dengan andal sampai salah satu uji restore berhasil. Layar terakhir sebelum save masih berupa dialog pembuka yang sedang meredup, bukan gameplay aktif.
- Story Mode belum tamat. Gunakan START untuk melewati dialog, bukan Circle; identifikasi adegan sebelum aksi gameplay baru, dan verifikasi aturan permainan dengan screenshot dari pengujian aktual.

---

## KOREKSI TERBARU — restore gagal karena field BIOS save-state; uji perbaikan antre (2026-10-19)

- [Run #39232852795](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39232852795) mengunduh artifact #12167524755 dengan sukses, kemudian emulator segfault (exit 139) sebelum menghasilkan screenshot setelah restore. Artifact kegagalannya hanya 1.190 byte; tidak berisi checkpoint baru.
- Bukti kuat mengarah ke sanitizer sebelumnya: ia menghapus field protobuf tetap `Memory.rom` (0x80000/512 KiB). Pada source pin PCSX-Redux, schema `src/core/sstate.h` mendefinisikan ROM sebagai `FixedBytes<0x00080000>`; implementasi protobuf di `src/support/protobuf.h` melakukan commit salinan FixedBytes, sementara state tanpa field itu tidak memiliki buffer valid. Ini konsisten dengan crash segera setelah `STORY_RESUME_ARTIFACT=present` dan BIOS berhasil dimuat. Belum ada bukti screenshot restore; **savestate sanitizer lama belum layak dianggap bisa dipulihkan**.
- Perbaikan pada commit `f4ea6b0169ef23c70be980602f91a65b3457c02c`: artifact tetap menyimpan savestate tanpa BIOS. Sesudah artifact diunduh, workflow memvalidasi BIOS lokal 512 KiB yang sudah diverifikasi, lalu menyisipkan kembali field `Memory.rom` hanya di runner sebelum `PCSX.loadSaveState`. File state yang sudah direkonstruksi dihapus bersama workspace; tidak diunggah ulang sebagai artifact.
- [Run #39233268705](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39233268705) menguji restore dengan rekonstruksi lokal tersebut; status terakhir antre. Periksa log `RESTORE_BIOS_REHYDRATE=PASS`, `EMULATOR_EXIT_CODE`, screenshot sesudah load, dan artifact sebelum mengklaim penyimpanan berhasil.
- Run #39205699071 tetap menyediakan artifact privat #12167524755 sampai 26 Oktober 2026 sekitar 13:47 WIB. Checkpoint menunjukkan adegan pembuka yang mulai meredup, bukan gameplay aktif. Detektor fade sudah diperbaiki dengan ambang kecerahan; itu pun belum dianggap berhasil sampai hasil run baru diperiksa.
- Story Mode belum tamat. Setiap dialog harus dilewati dengan START, bukan Circle; setiap aturan permainan harus didukung screenshot dan eksperimen yang benar-benar teramati.

---

## HASIL TERBARU — checkpoint berhasil dibuat; gameplay belum tercapai (2026-10-19)

### Run #39205699071 selesai
[Run #39205699071](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39205699071) berstatus workflow/job `success`, tetapi ini **bukan tamat Story Mode** dan tidak membuktikan sesi permainan sudah mencapai gameplay aktif.

- Artifact privat `naruto-storymode-checkpoint-private`, ID `12167524755`, berukuran 9.956.624 byte; dapat diakses sampai 26 Oktober 2026 sekitar 13:47 WIB.
- File `storymode-checkpoint.sstate` ada di artifact, ukuran 20.638.254 byte, SHA-256 `6365f18e2ad4531698976932a7d1dacc8834a47beba24e6c65d6d7d8e67a7223`.
- Log sanitizer: `STORY_SAVESTATE_SANITIZE=PASS`; 21.162.546 byte mentah menjadi 20.638.254 byte setelah field BIOS tertanam dihapus. `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`, dan pembersihan workspace berhasil.
- Ini checkpoint nyata, bukan sekadar kode penyimpanan. Namun **restore belum diuji**, jadi belum aman dinyatakan dapat digunakan sampai ada pengujian lintas-run yang sukses.

### Temuan visual yang harus diperhatikan
- Gerbang Mode Select frame 5999 dan adegan narasi frame 8999 lolos.
- Watcher mengirim START pada frame 9035 dan ulang pada frame 9110; readback hanya membuktikan tombol terbaca, bukan bahwa dialog telah maju.
- Screenshot frame 9035 dan 9065 masih menunjukkan dialog pembuka. Screenshot frame 9290 masih memperlihatkan dialog yang sama dengan layar jauh lebih gelap (rata-rata intensitas RGB sekitar 67, dibanding sekitar 146 sebelumnya). Karena itu `STORY_NON_DIALOG_STABLE=PASS frame=9285` adalah **false positive saat fade**, bukan bukti gameplay baru. Checkpoint tersimpan tepat di dekat transisi ini.
- Jangan menganggap START sudah terbukti berhasil melewati dialog ini. Lanjutkan dari checkpoint dan amati transisi; perbaiki klasifikasi layar gelap lebih dulu.

### Run pemulihan terpicu
[Run #39232852795](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39232852795) dibuat dari commit `077f576f33e8f65eea0504382383d6cc67d5cff6`, status terakhir `queued`. Run ini mencoba memuat artifact checkpoint `#39205699071` dan menambahkan syarat kecerahan rata-rata agar fade gelap tidak diklasifikasikan sebagai layar non-dialog. Tunggu status run ini, lalu periksa:
1. Apakah langkah pemulihan benar-benar mengunduh artifact dan log menunjukkan pemanggilan loader.
2. Apakah emulator tetap hidup setelah load tanpa kembali ke cold boot.
3. Screenshot terbaru setelah pemulihan—terutama apakah fade berlanjut ke adegan berikutnya atau kembali ke dialog.
4. Apakah checkpoint selanjutnya disanitasi, diunggah, dan dapat dipulihkan.

Tetap berlaku: setiap dialog dilewati dengan **START**, bukan Circle. Tidak ada aksi gameplay yang boleh ditebak sebelum layar diidentifikasi. Semua teks Jepang yang dicatat harus disertai terjemahan Bahasa Indonesia langsung di sebelahnya. Story Mode belum tamat; kontrol karakter, serangan/pertahanan, Chakra, wilayah/barrier, kartu/roulette, kondisi menang/kalah, dan perpindahan stage tetap belum diverifikasi dari gameplay aktif.

---

## TUJUAN UTAMA YANG TIDAK BOLEH TERLEWAT — tamatkan Story Mode dan pastikan aturan main (2026-10-19)

Jangan berhenti setelah emulator berhasil boot, menu terbuka, atau dialog selesai. **Tujuan akhir riset adalah memainkan Story Mode sampai layar akhir/tamat yang meyakinkan, lalu menyusun aturan main yang pasti berdasarkan pengamatan langsung dalam game dan bukti yang dapat diaudit.**

Setelah emulator stabil:
1. Lanjutkan dari checkpoint valid bila tersedia; dialog Story Mode dilewati dengan **START**, bukan Circle. Circle hanya dipakai untuk menu yang sudah terbukti memerlukannya. Setiap aksi dikirim satu per satu dan diikuti pemeriksaan screenshot.
2. Identifikasi kapan gameplay aktif dimulai, tujuan misi, kendali karakter, pergerakan, aksi/serangan/pertahanan, giliran bila berlaku, biaya aksi dan penggunaan Chakra, perebutan wilayah, barrier/penghalang, kartu, roulette, efek tiap mekanik, syarat menang/kalah, pergantian stage, serta variasi stage.
3. Mainkan setiap tahap Story Mode sampai tamat. Catat urutan tahap, keadaan awal, input, perubahan layar/status/Chakra/wilayah, hasil tiap aksi, dan bukti screenshot sebelum/sesudah. Jangan menebak jika layar hitam, crash, transisi ambigu, atau hasil input tidak jelas; rancang eksperimen pembeda satu variabel pada satu waktu.
4. Simpan tabel aturan dengan tiga label yang tidak boleh dicampur:
   - **TERVERIFIKASI** — terlihat langsung dari gameplay atau eksperimen terkontrol yang berulang, dengan screenshot/log dan kondisi uji tercatat.
   - **HIPOTESIS** — penjelasan yang masuk akal tetapi bukti belum cukup atau masih ada alternatif.
   - **BELUM DIUJI / BELUM DIKETAHUI** — mekanik atau kondisi belum berhasil dipicu/diamati.
   Tambahkan sumber bukti dan langkah pengujian yang diperlukan untuk setiap aturan.
5. Jangan menyatakan aturan sebagai pasti hanya berdasarkan nama fungsi, analisis kode, readback controller, status workflow, atau sumber luar tanpa konfirmasi gameplay. Jangan menyatakan Story Mode tamat tanpa bukti kuat dari layar akhir/ending.
6. Setelah eksperimen penting, perbarui STATUS.md, HANDOFF_LANJUT.md, HANDOFF_CHAT_BARU_2026-10-19.md, ANALYSIS_LOG.md, dan docs/RUNTIME_TEST_PLAN.md agar sesi berikutnya langsung melanjutkan dari hasil terakhir tanpa mengulang run berhasil.
7. Setiap tulisan Jepang yang diperlihatkan ke pengguna harus langsung diikuti terjemahan Bahasa Indonesia di sebelahnya dalam tanda kurung. Utamakan screenshot dari hasil eksperimen kita sendiri, bukan gambar web.

---

## STATUS OPTIMASI RUNNER — crash berulang, guard checkpoint sedang diuji (2026-10-19)

Tujuan pengguna tetap: mempercepat emulator, memakai job timeout 360 menit, dan boleh memindahkan game save/savestate yang telah disanitasi lewat storage private agar Story Mode dapat dilanjutkan antar-job. Timeout GitHub Actions kini 360 menit, tetapi **sesi panjang belum terbukti berjalan** karena emulator masih crash awal.

### Bukti dari dua run terbaru
- [Run #39205262049](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39205262049) berakhir workflow-success secara keliru walau log menunjukkan `Segmentation fault`, `EMULATOR_EXIT_CODE=139`; job lama tidak memeriksa exit code emulator. Gate visual gagal sebelum frame 5999, tidak ada screenshot progres atau savestate.
- [Run #39205556772](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39205556772) sesudah penghapusan panggilan `PCSX.GPU.getDumpFrames()` berakhir **failure** dengan exit 139 dalam sekitar delapan detik. BIOS retail terdeteksi dan log mengenali disc `SLPS03553` serta executable `SLPS_035.53;1`, tetapi gate berhenti sebelum frame 5999. Artifact #12165635987 hanya berisi tiga file teks kecil; `STORY_SAVESTATE_SANITIZE=missing`.
- Maka menghapus `getDumpFrames()` belum menyelesaikan crash. ALSA juga mengeluarkan pesan tak adanya perangkat suara di runner; itu tercatat tetapi belum dipastikan penyebab crash.
- Hipotesis berikutnya yang diuji, belum terbukti: Lua selalu memanggil `Support.File.open("resume/storymode-checkpoint.sstate")` bahkan saat tidak ada artifact restore. Native savestate loader bisa gagal dengan cara yang tidak tertangkap Lua bila menerima File object yang tidak valid. Commit `88d5cfa8833ef39e286431f5e8bedf2584485804` menambahkan probe `io.open` dan hanya memanggil native loader bila file benar-benar ada.
- [Run #39205699071](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39205699071) dibangun dari commit guard tersebut dan masih antre/baru dimulai saat bagian ini ditulis. Periksa screenshot/log dan status job sebelum menganggap perbaikan berhasil.

### Konfigurasi dan perubahan performa yang dipertahankan
- Job timeout `timeout-minutes: 360`; timeout emulator internal 20.400 detik (5 jam 40 menit) untuk menyisakan waktu sanitasi/upload/cleanup.
- BIOS SCPH-7502 (EU); disc `SLPS03553`; executable `SLPS_035.53;1`; PCSX-Redux pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`; SoftGPU; Port 1 Analog/Auto.
- Jalur bermain tidak merekam raw GPU/VRAM terus-menerus dan menonaktifkan polling GDB/RSP serta sampling jendela berkala. Ini dimaksudkan mengurangi overhead, tetapi kecepatan belum terukur karena crash sebelum screenshot pertama yang relevan.
- Dialog tetap dilewati dengan **START**, bukan Circle. Bila layar non-dialog stabil muncul, simpan checkpoint dan berhenti untuk inspeksi; jangan menebak kontrol gameplay.
- Game save/savestate tersanitasi boleh dipindahkan melalui private Actions artifact/cache/private repo sesuai kebijakan baru. Workflow saat ini hanya menggunakan private artifact berumur tujuh hari. Savestate baru boleh diunggah hanya jika sanitizer menyatakan PASS dan field BIOS tertanam terhapus; raw RAM/VRAM/GPU dump tetap dilarang. ROM/ISO, executable game, dan file BIOS retail tersendiri tetap tidak boleh diunggah.

### Langkah selanjutnya
1. Periksa Run #39205699071 dan baca log penuh, bukan hanya kesimpulan workflow. Jika crash masih exit 139, isolasi dengan mengembalikan opsi GDB lama tanpa mengaktifkan kembali raw GPU dump terlebih dahulu; ubah satu variabel per run.
2. Jangan mengklaim checkpoint dapat dipakai sebelum log menunjukkan save state berhasil dibuat, sanitizer PASS, artifact benar-benar memuat file state, dan restore run berikutnya dikonfirmasi oleh screenshot.
3. Setelah emulator stabil, ukur VSync per waktu nyata; baru setelah itu nilai apakah penghematan overhead cukup untuk menyelesaikan Story Mode dalam satu sesi enam jam.

---

## REVISI ATURAN SAVE & CHECKPOINT — instruksi terbaru pengguna (2026-10-19)

Kebijakan ini **menggantikan larangan lama yang melarang semua save/save state di penyimpanan GitHub**. Pengguna sekarang secara eksplisit mengizinkan pemindahan save untuk mempertahankan progres Story Mode.

- Save kartu memori/game save dan **savestate emulator yang telah disanitasi** boleh dipindahkan melalui **private GitHub Actions artifact, GitHub Actions cache, atau repositori private**. Jangan menaruhnya di repositori publik. Default yang dipakai workflow saat ini adalah private artifact berumur 7 hari; cache/repo diizinkan oleh aturan tetapi belum diaktifkan di workflow.
- Savestate PCSX-Redux yang dipindahkan harus melewati sanitizer yang memverifikasi struktur protobuf dan menghapus field BIOS tertanam (Memory.rom). Transfer hanya boleh diunggah jika indikator STORY_SAVESTATE_SANITIZE=PASS; jika sanitasi gagal atau struktur tidak dikenal, jangan unggah file state itu.
- Savestate berisi state emulasi game (termasuk RAM/VRAM sebagai bagian format save); itu diperbolehkan setelah sanitasi sebagai **savestate**, bukan sebagai dump memori terpisah. **Raw RAM dump, raw VRAM dump, dan raw GPU dump tetap tidak boleh diunggah.** File state mentah sebelum sanitasi harus tetap sementara di runner dan dibersihkan.
- ROM/ISO, executable game, dan file BIOS retail tersendiri tetap dilarang di-commit atau diunggah ke artifact/cache/repo. Runner berikutnya harus mengambil aset dari release privat yang sudah ada dan memverifikasi hash sesuai prosedur.
- Untuk melanjutkan sesi, jalankan workflow secara manual (workflow_dispatch) dengan input resume_run_id berisi ID run yang memuat artifact naruto-storymode-checkpoint-private. Loader harus memakai BIOS SCPH-7502 yang diverifikasi secara terpisah. Restore lintas-run harus dikonfirmasi lewat log dan screenshot; jangan menganggap loader berhasil hanya karena artifact ditemukan.
- Workflow terbaru pada commit 58d2e8b18feec9dedbb9fbfd9623fc40c1039175: timeout job 360 menit; SoftGPU tetap dipakai; emulator diberi batas internal 20.400 detik (5 jam 40 menit) agar ada waktu untuk sanitasi, upload, dan cleanup. Untuk jalur bermain, perekaman GPU mentah, GDB/RSP polling, dan sampling jendela berkala dinonaktifkan. Detektor visual meminta START untuk dialog, checkpoint dibuat tiap 5.000 VSync serta saat layar non-dialog stabil, lalu sesi dijeda untuk inspeksi sebelum aksi gameplay yang belum terbukti.
- Run pertama dari workflow baru [#39205262049](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39205262049) masih berstatus antre/menunggu pada pemeriksaan terakhir. Perubahan ini sudah dikomit, tetapi kecepatan aktual, detektor dialog, sanitizer, dan pemulihan savestate **belum dianggap teruji** sampai hasil run diperiksa.
- Setiap dialog Story Mode tetap dilewati dengan **START**, bukan Circle. Circle hanya dipakai untuk konfirmasi menu yang memang memerlukannya. Klaim progres harus didukung screenshot aktual; jangan menyatakan Story Mode tamat sebelum layar akhir yang meyakinkan.

---

## ATURAN KONTROL DIALOG — instruksi pengguna terbaru (2026-10-19)

**Setiap kali Story Mode menampilkan dialog/narasi yang meminta dilanjutkan atau di-skip, gunakan tombol START untuk melewatinya, bukan Circle.** Ini preferensi kontrol yang harus dipertahankan di chat dan eksperimen berikutnya.

- Circle tetap digunakan hanya untuk langkah menu yang telah dibuktikan memerlukannya, termasuk mengonfirmasi pilihan Story Mode dari layar Mode Select. Jangan memakai Circle sebagai tombol skip dialog.
- Kirim satu tap START terkontrol (press dan release terpisah), lalu ambil/baca screenshot sebelum dan sesudahnya. Jangan mengirim input beruntun tanpa inspeksi layar.
- Jika workflow otomatis, gate START dengan fingerprint screenshot dialog aktual yang sudah diverifikasi; catat frame, hasil visual, dan perubahan layar. Readback input emulator tidak cukup untuk mengklaim game merespons.
- Setelah dialog berubah, identifikasi teks/layar baru terlebih dahulu sebelum aksi selanjutnya. Setiap teks Jepang yang dilaporkan harus diikuti terjemahan Bahasa Indonesia dalam tanda kurung.
- Instruksi ini mengoreksi rencana lama yang menggunakan Circle untuk memajukan narasi. Jangan mengikuti langkah Circle lama ketika konteksnya adalah dialog.

---

## HASIL RUN #39189879767 — Circle memajukan narasi ke kalimat berikutnya (2026-10-19)

Run [#39189879767](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39189879767) selesai dengan workflow/job `success`, mencapai 10.000 VSync. Artifact privat #12161482625 telah diunduh dan screenshot aktual diperiksa. Jangan jalankan ulang run ini.

**Bukti visual dari screenshot yang benar-benar diperiksa:**
- Frame 9199 dan 9200 memperlihatkan kalimat pembuka `今日は、アカデミーの卒業試験の日。` (Hari ini adalah hari ujian kelulusan Akademi.).
- Gate `STORY_DIALOG_VISUAL_GATE=PASS` pada frame 8999: crop 280×240 stabil yang tidak mencakup ikon Circle beranimasi cocok dengan baseline screenshot terverifikasi.
- Circle tambahan ditekan pada frame 9200 dan dilepas pada frame 9230. Frame 9229/9230 memperlihatkan kotak dialog kosong; frame 9240 mulai menampilkan teks berikutnya.
- Frame 9299, 9499, dan 9999 stabil dan menampilkan `忍者を目指す者にとって大切な一歩をふみ出す日である。` (Bagi mereka yang bercita-cita menjadi ninja, hari ini adalah hari untuk mengambil langkah penting.). Perubahan sebelum/sesudah ini membuktikan bahwa Circle memajukan narasi, bukan sekadar terbaca oleh API controller.
- Batas kesimpulan: **Story Mode masih pada layar narasi**. Tidak ada gerak karakter atau gameplay aktif yang terverifikasi; mekanik permainan dan tamat Story Mode masih belum terbukti.

**Run dan cleanup:** ringkasan melaporkan `GPU_DUMP_RESULT=parsed`, `GPU_DUMP_TRUNCATED=false`, `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`; langkah penghapusan workspace dijalankan hingga selesai. ZIP artifact sekitar 8,32 MB berisi ringkasan/log dan screenshot PNG pilihan; daftar isi tidak menunjukkan ROM, BIOS, save/save state, raw GPU/VRAM dump, atau aset mentah terlarang.

**Langkah berikutnya yang telah disiapkan:** commit workflow `a561b8196658dd218bedb5a70e34a1796e3ff9cf` menambahkan tap Circle berikutnya pada frame 10200–10230, setelah screenshot frame 9999 lolos gate visual kedua untuk kalimat di atas. Screenshot checkpoint direncanakan pada 10199 (sebelum), 10200, 10229, 10230, 10240, 10299, 10499, dan 10999; observasi sampai 11000 VSync. Periksa run baru yang dipicu commit ini. Bila gate gagal, Circle keempat dilewati. Jangan kirim input tambahan bila screenshot menunjukkan layar yang belum diidentifikasi.

**Baseline tetap:** retail BIOS SCPH-7502 (EU); disc ID `SLPS03553`; executable `SLPS_035.53;1`; PCSX-Redux source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`; SoftGPU; Port 1 Analog/Auto. Jangan mengubah konfigurasi tanpa alasan yang didokumentasikan.

---

## PEMBARUAN HANDOFF — satu tap Circle setelah narasi terverifikasi (2026-10-19)

Run eksperimen baru [#39189879767](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39189879767) dipicu oleh commit workflow `892f16c2b2ea140f41b7e920d09d08261867b377`. Pemeriksaan terakhir menunjukkan job masih `in_progress`; bukti setelah Circle tambahan belum tersedia saat catatan ini ditulis. **Jangan anggap input terbaca emulator atau status workflow sebagai bukti bahwa game sudah maju.**

### Perubahan eksperimen yang sedang berjalan
- Pertahankan cold boot dan urutan terbukti: Start press/release 2650/2680; D-pad DOWN 2710/2720; UP 2740/2750; Circle pertama 2780/2810.
- Gerbang visual Mode Select pada frame 5999 tetap wajib. Circle kedua dijadwalkan 6100/6130 hanya jika gambar menu dan pilihan Story Mode cocok dengan fingerprint terverifikasi.
- Gerbang visual narasi membaca framebuffer frame 8999 dan membandingkan crop stabil 280×240 dengan screenshot terverifikasi (bagian ikon Circle yang berkedip di kanan bawah tidak ikut dihitung). Tap ketiga **hanya** dikirim jika gerbang Mode Select sebelumnya dan crop narasi sama-sama lolos.
- Circle tambahan: press frame 9200, release frame 9230. Screenshot sebelum input diambil pada frame 9199; checkpoint sesudahnya 9200, 9229, 9230, 9240, 9299, 9499, dan 9999. Target observasi akhir VSync 10000.
- Config tetap retail BIOS SCPH-7502 (EU), CD ID `SLPS03553`, executable `SLPS_035.53;1`, PCSX-Redux source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`, SoftGPU, Port 1 Analog/Auto.

### Tindakan setelah run selesai
1. Periksa status terbaru, job log, dan artifact run #39189879767; jangan menjalankan ulang #39178662131 dan jangan mengulang run #39183597316.
2. Buka screenshot aktual frame 9199, 9200, 9229/9230, 9240, 9299, 9499, dan 9999. Bandingkan narasi sebelum/sesudah Circle; gunakan gambar, bukan `PAD_INJECT` readback.
3. Pastikan summary melaporkan `STORY_DIALOG_VISUAL_GATE`, hasil `STORY_CIRCLE3`, target frame akhir, penghapusan raw GPU dump/screenshot sementara, serta penghapusan workspace.
4. Jika scene berubah, identifikasi layar baru sebelum merencanakan input berikutnya. Jika scene tetap sama, frame hitam muncul, atau gate gagal, simpan sebagai hasil negatif/tidak konklusif dan rancang satu eksperimen pembeda—jangan menekan tombol tambahan tanpa inspeksi.
5. Pada saat catatan ini dibuat, gameplay aktif, mekanik, progres stage, dan tamat Story Mode tetap **belum terbukti**.

Privasi: ROM, BIOS, save/save state, raw GPU/VRAM dump, dan aset privat tidak boleh di-commit atau diunggah. Artifact baru harus diperiksa sebelum dibagikan; cleanup yang ditulis dalam workflow tetap harus diverifikasi di log aktual.

---

## ANALISIS VISUAL — Circle kedua membawa game ke narasi pembuka Story Mode (run #39183597316, 2026-10-19)

Run [#39183597316](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39183597316) selesai dengan workflow/job `success` pada commit workflow `e9a6f985458ad2dd23c939813881918cb9a7f701`. Run lama #39178662131 tidak diulang. Artifact privat [#12158079662](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39183597316/artifacts/12158079662) telah diunduh, inventaris file diperiksa, dan screenshot aktual dilihat.

**Temuan visual yang membuktikan transisi:**
- Sequence cold boot yang terbukti diulang: Start press/release frame 2650/2680; DOWN 2710/2720; UP 2740/2750; Circle pertama 2780/2810.
- Gerbang visual `STORY_SELECT_VISUAL_GATE=PASS` pada frame 5999: crop judul Mode Select dan crop pilihan Story Mode cocok dengan fingerprint screenshot baseline yang telah diverifikasi. Karena gerbang lulus, Circle kedua benar-benar dikirim: press frame 6100 dan release frame 6130. Readback input hanya catatan pendukung, bukan dasar klaim.
- Frame 6099–6140 masih menunjukkan layar pemilihan mode dengan Story Mode tersorot dan animasi kartu. Frame 6200 dan 6399 hitam seragam; keduanya **tidak** dipakai sebagai bukti Story Mode.
- Frame 6799 menampilkan layar narasi cerita baru; layar serupa bertahan pada 7199, 7599, 7999, 8499, dan 8999. Teks terbaca: `今日は、アカデミーの卒業試験の日。` (Hari ini adalah hari ujian kelulusan Akademi.). Ini adalah bukti visual kuat bahwa konfirmasi kedua membawa game masuk ke pembukaan Story Mode, bukan hanya memilih opsinya di menu. Kesimpulan terverifikasi: **Story Mode telah dimulai sampai adegan narasi pembuka**.
- Batas kesimpulan: adegan pembuka terlihat stabil sampai frame 8999, tetapi kontrol karakter/gameplay aktif, mekanik, progres misi, dan tamat Story Mode **belum** diuji.

**Konfigurasi:** log runtime mencatat BIOS SCPH-7502 (EU), CD ID `SLPS03553`, executable `SLPS_035.53;1`, dan Port 1 connected Analog/Auto. Workflow tetap mematok PCSX-Redux source `0c3572c3db75f97542001e453ae80ba8c3f8acba` dan flag `-softgpu`; konfigurasi wajib lainnya tidak diubah.

**Cleanup dan isi artifact:** log menyatakan `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`, GPU dump ter-parse lengkap (`GPU_DUMP_TRUNCATED=false`), dan workspace runtime dihapus. ZIP 7.6 MB berisi ringkasan/log, RSP summary, gerbang visual dan screenshot PNG checkpoint yang memang diperlukan sebagai bukti; tidak ditemukan file ROM, BIOS, save, raw GPU/VRAM dump, atau file mentah ber-ekstensi terkait di artifact.

**Langkah eksperimen berikutnya:** lakukan cold boot baru dan ulangi urutan lengkap sampai Story Mode. Tunggu layar pembuka tampak; screenshot menunjukkan ikon Circle di kanan bawah kotak narasi. Uji hanya satu tap Circle terkontrol (press/release terpisah) untuk mencoba melanjutkan dialog, capture tepat sebelum/sesudah, dan amati apakah adegan berikutnya/gameplay muncul. Jangan kirim input beruntun dan jangan menandai kontrol gameplay lulus sebelum ada bukti visual/gerakan karakter yang aktual.


---

## Analisis visual terbaru — DOWN/UP dan hasil Circle (run #39178662131, 2026-10-19)

Run #39178662131 selesai dengan workflow success; artifact privat [#12155879252](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39178662131/artifacts/12155879252) berisi frame-frame PNG yang dibandingkan langsung.

**Urutan yang tampak pada gambar:**
1. Frame 2.670: kotak menu berisi `はじめから` dan `ロード`; panah di baris `はじめから`.
2. DOWN 2.710–2.720: frame 2.710 diambil terlalu dekat dengan press dan masih menunjukkan pilihan atas; frame 2.720 jelas menunjukkan panah di baris `ロード`.
3. UP 2.740–2.750: frame 2.740 masih memperlihatkan pilihan bawah; frame 2.749–2.750 menunjukkan panah kembali ke `はじめから`. Dengan demikian, input arah mengubah pilihan secara visual, dengan jeda beberapa frame sebelum checkpoint menampilkan state baru.
4. Circle 2.780–2.810: frame 2.780 masih punya menu, 2.790 menunjukkan sisa garis overlay, 2.800 menu telah hilang, 2.900 gambar judul menggelap, dan 2.950/2.999/3.199 hitam.
5. Bukti tujuan yang positif bukan layar hitam: frame 3.399 memperlihatkan judul Jepang `モードセレクト` dan `ストーリーモード` terpilih/disorot. Screenshot 3.599, 3.999, 4.499, 4.999, 5.499, dan 5.999 menunjukkan layar itu bertahan.

**Interpretasi:** rangkaian ini konsisten dengan Circle mengonfirmasi `はじめから` dan game bertransisi ke Mode Select. Karena opsi Story Mode terlihat tersorot di Mode Select, itu baru membuktikan state pilihan, bukan Story Mode yang sudah dimulai. Perlu Circle kedua setelah layar ini dicapai, lalu bukti visual pasca-konfirmasi/gameplay. `PAD_INJECT status=PASS` hanya memverifikasi readback API.

Runtime yang tercatat tetap retail SCPH-7502 (EU), CD ID `SLPS03553`, EXE `SLPS_035.53;1`, SoftGPU dan Port 1 Analog/Auto; pin PCSX-Redux tetap `0c3572c3db75f97542001e453ae80ba8c3f8acba`. Cleanup log: `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`; final removal step `rm -rf "$WORK"` selesai. Artifact yang diperiksa tidak memuat ROM/BIOS/save/raw GPU/VRAM dump.

**Eksperimen berikutnya:** lakukan cold boot baru dan ulangi Start→DOWN→UP→Circle pada timing yang terbukti. Setelah Mode Select terlihat dan stabil (pada run ini sudah terlihat dari frame 3.399), kirim Circle kedua sekitar frame 6.100–6.130, ambil gambar di sisi input dan amati hingga sekurangnya frame 9.000. Jangan menginterpretasi black frame atau workflow success sebagai mode/gameplay.

---

## Hasil Start-only — run #39176328030, 2026-10-19

**Input:** Start press frame 2.650 dan release frame 2.680; tidak ada Circle. Emulator mencapai 3.000 VSync, exit code 0, cleanup berhasil.

**Bukti aktual:** frame 2.650 = title screen Naruto dengan prompt Start; frame 2.670 = menu biru dengan panah di `はじめから` dan `ロード` di bawah; frame 2.999 = menu yang sama masih tampil. Resolusi checkpoint 640×480. Log `PAD_INJECT` mengonfirmasi readback Start saja, sementara screenshot sebelum/sesudah membuktikan efek visual pada state game.

**Kesimpulan:** Start membuka main menu dan menu bertahan tanpa Circle. Ini membedakan hasil dari run #39149443247 yang mengirim Circle dan kemudian menampilkan framebuffer hitam setelah transisi. Run ini tidak menguji apakah `はじめから` dapat dikonfirmasi; Mode Select dan Story Mode belum terbukti.

Artifact privat #12155370415 memiliki retensi 3 hari. `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`; folder runtime ephemeral dibersihkan. ROM, BIOS, dan dump mentah tidak diunggah.

## Follow-up terkoreksi — Start saja tanpa Circle (2026-10-19)

Run [#39149443247](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39149443247) menekan Start pada 2.650–2.680 lalu Circle pada 2.750–2.780. Setelah Circle, screenshot frame 2.850 menampilkan fade/transisi; frame 2.900, 2.950, dan 2.999 adalah framebuffer 320×240 hitam seragam. Tidak ada teks Mode Select yang dikenali, sehingga frame hitam tidak cukup untuk menyimpulkan mode atau Story Mode.

Arahan pengguna: **gunakan tombol Start, jangan Circle**, karena state target adalah title screen yang menampilkan prompt Start. Workflow berikutnya menekan Start saja pada 2.650–2.680, tanpa tombol susulan, lalu mencatat apakah menu tetap stabil sampai 3.000 VSync. Ini sengaja membiarkan menu terbuka agar transisi tidak terpengaruh input konfirmasi yang belum diminta. Tetap gunakan baseline runtime yang sama dan jangan unggah raw ROM/BIOS/dump.

## Hasil Run #39147391100 — Circle dikirim saat title screen (2026-10-18)

Run [#39147391100](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39147391100) pada commit `5f89389d3af1f3f6254057ae8b0162667bd5eaf0` berhasil mencapai VSync 3.000 dan menyelesaikan cleanup. Konfigurasi emulator/BIOS/ROM sama dengan run sebelumnya, tetapi input sequence berisi Circle saja (press 2750, release 2780).

**Bukti visual aktual:** frame 2.749–2.800 dan checkpoint 2.850/2.900/2.950/2.999 mempertahankan ilustrasi title screen. Prompt `STARTボタンをおせってばよ!` muncul dan hilang pada beberapa checkpoint, konsisten dengan prompt berkedip. Tidak ada kotak menu atau Mode Select pada frame ini. Log input menampilkan `PAD_INJECT frame=2750 button=CIRCLE action=press readback=true expected=true status=PASS` dan release sukses; readback itu tidak membuktikan game memproses Circle.

**Interpretasi:** percobaan tidak mengonfirmasi `はじめから`, karena sesi Actions mulai dari boot baru dan Start tidak pernah ditekan di dalam run ini. Hasil tersebut juga tidak menguji apakah menu Start bekerja atau tidak; run #39145309203 sebelumnya mempunyai bukti menu yang jelas pada frame 2.670 dengan panah di `はじめから` dan `ロード` di bawahnya. Perbedaan ini menjelaskan mengapa input berikutnya wajib memainkan kedua tombol secara berurutan pada satu sesi.

**Privasi:** artifact privat #12144726606 berisi screenshot/summary minimum; log menyatakan `RAW_GPU_DUMP_REMOVED=1` dan `RAW_TEMP_SCREENSHOTS_REMOVED=1`, kemudian aset runtime dihapus dari runner.

**Eksperimen berikutnya:** Start press 2.650/release 2.680; Circle press 2.750/release 2.780 pada sesi boot sama; capture rapat di 2.649–2.800 lalu 2.850/2.900/2.950/2.999. Identifikasi Mode Select dari tampilan aktual, jangan mengasumsikan urutan mode.

## Hasil — Start menghasilkan transisi visual ke menu utama (run #39145309203, 2026-10-18)

**Perubahan terkontrol:** setelah run [#39122631591](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39122631591) menekan Start terlalu dini dan tidak mengisolasi responsnya, run ini mempertahankan BIOS/ROM/emulator/SoftGPU/controller yang sama lalu hanya menekan Start pada frame 2.650 (release 2.680). Circle ditiadakan agar hanya satu tombol diuji.

**Bukti hasil:** log menegaskan input override dibaca kembali sesuai pada frame 2.650/2.680. Perbandingan screenshot frame 2.649, 2.650, 2.660, dan 2.670 memperlihatkan layar judul dengan prompt berubah menjadi kotak pilihan; pada 2.670 tertulis `はじめから` dengan panah penunjuk dan `ロード` di bawahnya. Pilihan tetap terlihat sampai 2.999. Oleh sebab itu, transisi ke menu merupakan respons game yang terlihat dan selaras waktu dengan Start. Ini tidak membuktikan Circle atau pilihan menu diproses.

**Koreksi referensi:** jangan memaksakan `コンティニュー` sebagai pilihan ketiga. Pada framebuffer aktual yang didapat dalam run ini hanya dua opsi yang tampak jelas, `はじめから` dan `ロード`.

**Keamanan bukti:** artifact privat #12143433923 berisi screenshot framebuffer 640×480 dan ringkasan teks. Parser log menyatakan `RAW_GPU_DUMP_REMOVED=1` serta `RAW_TEMP_SCREENSHOTS_REMOVED=1`. ROM, BIOS, dan GPU dump mentah tetap privat dan tidak masuk artifact.

**Eksperimen berikutnya:** pada baseline yang sama, tekan hanya Circle/O pada frame 2.750 (menu dan panah pertama sudah stabil) lalu lepas pada 2.780; checkpoint 2.749, 2.750, 2.760, 2.770, 2.780, 2.790, 2.800, 2.850, 2.900, 2.950, 2.999. Cari transisi mode select; kalau terlihat, identifikasi opsi aktual sebelum input berikutnya.

## Hasil terbaru — peringatan berubah menjadi layar hak cipta/latar (2026-10-18)

- Run [#39120694338](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39120694338) selesai dengan pipeline `success`, mencapai 2.400 VSync; BIOS retail **SCPH-7502 (EU)** dan executable `SLPS_035.53;1` terdeteksi. Konfigurasi pad efektif dicatat `connected=true`, `device_type=Analog`, `input_type=Auto`.
- Audit gambar framebuffer aktual memperlihatkan: frame 1.799/1.900/2.000/2.099 = peringatan kesehatan Jepang; frame 2.199 dan 2.299 = hitam; frame 2.399 = framebuffer 640×480 dengan latar bermotif dan copyright Kishimoto/Shueisha/TV Tokyo/Pierrot serta © Bandai 2003. Ini membuktikan grafik berubah setelah peringatan, tetapi tanpa logo judul/menu atau pilihan yang terbaca belum cukup untuk menandai title screen ataupun menu telah dicapai.
- Start diinjeksi pada frame 1.900 dan dilepas pada 1.930; log readback menunjukkan `PAD_INJECT ... status=PASS`. Namun, itu hanya membaca balik override input emulator, bukan respons game. Karena peringatan tetap bertahan hingga frame 2.099 lalu layar berubah beberapa ratus frame kemudian, belum dapat dipastikan apakah Start memicu transisi atau peringatan berakhir secara otomatis.
- Run lanjutan [#39122631591](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39122631591) mengamati sampai VSync 3.000, mengambil checkpoint tambahan 2.499–2.999, mengirim Start pada frame 2.500 dan Circle/O pada 2.700, 2.850, 2.950 untuk mencoba melewati prompt/menu. BIOS, ROM, emulator pin, SoftGPU, serta konfigurasi pad Analog dipertahankan.
- Status tetap **RT-001 OPEN / BELUM KONKLUSIF**. Ada kemajuan tampilan di luar splash/peringatan, tetapi judul/menu Naruto, Story Mode, respons kontrol yang terbukti, dan tamat Story Mode belum terkonfirmasi. ROM/BIOS dan raw dump tetap privat; raw dump dihapus sebelum upload artifact.

## Audit visual koreksi waktu input — run #39119261650 (2026-10-18)

- Run [#39119261650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39119261650) selesai dengan penghentian eksplisit di VSync 2.100, BIOS retail **SCPH-7502 (EU)** dan executable `SLPS_035.53;1` terdeteksi; GPUDump diparse dan file mentah dibersihkan sebelum artifact diunggah.
- Audit screenshot aktual memperjelas urutan untuk run ini: frame 1.499 **DIMPS**, frame 1.600 **DIMPS**, frame 1.700 **hitam**, frame 1.799 **peringatan kesehatan Jepang**, dan layar peringatan masih tampak pada 1.900, 2.000, serta 2.099. Jadi input Start pada frame 1.650 tidak dikirim setelah peringatan; pengujian tersebut terlalu awal. Ini mengoreksi asumsi timing sebelumnya untuk run ini.
- Log `PAD_INJECT ... status=PASS` hanya menunjukkan override internal pada API terbaca sesuai harapan; bukan bukti input diterima/diproses oleh game. PC sampler akhir banyak berada di rentang executable utama sekitar `0x800372d8` / `0x80037320`; ini konsisten dengan rutinitas berulang tetapi belum mengidentifikasi akar masalah.
- Run lanjutan aktif [#39120694338](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39120694338) mengirim Start pada frame 1.900 dan melepas pada 1.930, mempertahankan controller Analog dan semua komponen runtime lain, lalu mengamati sampai VSync 2.400. Konfigurasi pad aktual juga dicatat eksplisit di log.
- Status tetap **RT-001 OPEN / BELUM KONKLUSIF**: belum ada bukti title/menu, Story Mode, respons input yang terkonfirmasi, ataupun tamat Story Mode.

## Hasil terbaru — logo Dimps terkonfirmasi, Start timing dikoreksi (2026-10-18)

- Run [#39117084569](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39117084569) selesai dengan kesimpulan pipeline `success` dan mencapai target 1.800 VSync. Log memverifikasi retail BIOS **SCPH-7502 (EU)**, disc `SLPS03553` / executable `SLPS_035.53;1`, serta boot transfer `EXEC:PC0` + `Execute !`.
- Urutan framebuffer run ini: frame 1.100 = logo **BANDAI**, frame 1.499 = logo **Dimps**, frame 1.600 / 1.700 / 1.799 = layar peringatan kesehatan Jepang. Screenshot jendela emulator pada sekitar 700 detik juga menampilkan peringatan. Ini bukti nyata game menjalankan urutan splash internalnya; DIMPS bukan sekadar splash BIOS/PlayStation. Namun, belum terlihat judul/menu Naruto atau Story Mode.
- Koreksi eksperimen: **Start di frame 1.450 masih terlalu awal**, sebab checkpoint GPU berikutnya (frame 1.499) masih menampilkan logo Dimps dan peringatan baru tampak di frame 1.600. Circle pada frame 1.650 dan 1.750 terjadi saat peringatan sudah terlihat, tetapi tombol itu bukan tombol yang terdokumentasi untuk melewati prompt Start. Readback `PASS` hanya membuktikan status tombol dapat disetel/dibaca kembali, bukan bahwa game merespons.
- Koreksi audit untuk run [#39119261650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39119261650): frame 1.499 dan 1.600 masih logo DIMPS, frame 1.700 hitam, peringatan kesehatan pertama kali terkonfirmasi pada frame 1.799 lalu tetap terlihat pada 1.900/2.000/2.099. Karena itu Start di frame 1.650 masih terlalu awal dan belum menguji respons pada layar peringatan. Run baru [#39120694338](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39120694338) sedang menguji Start di frame 1.900, setelah peringatan terlihat, dengan konfigurasi BIOS/ROM/emulator dan controller Analog tetap sama.
- Status tetap **RT-001 OPEN / BELUM KONKLUSIF**; sudah mencapai splash Dimps dan peringatan kesehatan, tetapi title/menu, Story Mode, respons kontrol yang terkonfirmasi, serta tamat Story Mode belum terbukti. Raw GPU dump/VRAM sementara, ROM, dan BIOS tidak ikut artifact; file sementara dibersihkan.

## Jendela observasi diperpanjang dan referensi timeline — 2026-10-18

- Run [#39101435497](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39101435497) sedang menguji Start + Circle memakai SCPH-7502, pinned PCSX-Redux dan dynarec hingga VSync 900; screen captures tersebar sampai detik 410, PC-only sampling berjeda 25 detik. Input API readback hanya membuktikan injeksi, bukan respons game.
- Referensi TAS publik [video dengan bab Opening 0:00, Menu 0:23, Mission 1 0:49](https://www.youtube.com/watch?v=DfnD_mvqs7g) menunjukkan 900 VSync hanya sekitar 15 detik simulasi pada 60 Hz; bila screenshot di checkpoint 900 masih pada splash, hasil itu saja tidak membuktikan macet. Langkah selanjutnya dapat memperpanjang sampai setidaknya 1.500 VSync (25 detik simulasi) tanpa mengubah BIOS/ROM/emulator.
- Referensi [menu/kontrol game](https://github.com/juanoliveira82/naruto-ps1_translation-english/blob/master/Start-and-Main-Menu.md) memberi Start untuk melewati prompt, `はじめから` (mulai dari awal), O/Circle untuk confirm dan X/Cross untuk cancel. Itu sebabnya otomatisasi diganti dari Cross ke Start/Circle.
- **RT-001 tetap Open / blocked** sampai screenshot valid menunjukkan menu Naruto atau Story Mode; belum ada bukti game dimainkan atau tamat.

## Perbaikan strategi input — Start + Circle, bukan Cross — 2026-10-18

- Referensi kontrol spesifik game yang diperiksa pada [naruto-ps1_translation-english/Start-and-Main-Menu.md](https://github.com/juanoliveira82/naruto-ps1_translation-english/blob/master/Start-and-Main-Menu.md) menyatakan prompt awal meminta Start; opsi Start Menu berurutan `はじめから` (From the beginning), `ロード` (Load), `コンティニュー` (Continue); Mode Select mencatat **X = Return/cancel** dan **O = Confirm**. Halaman promosi resmi TV Tokyo menyebut Story Mode dan Party/Versus Mode sebagai dua mode utama: [TV Tokyo game information](https://www.tv-tokyo.co.jp/anime/naruto2002/goods/playstation.html). Jadi Cross yang dikirim probe terdahulu adalah aksi yang keliru sebagai confirm.
- Workflow pada commit [dcf31d02](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/dcf31d022e43e8eaf32c8a31ae4686720044f354) mengganti input berulang Cross dengan Start pulses pada frame 225/280 lalu Circle confirms sejak frame 320 dan berulang sampai frame 860, sambil menjalankan dynarec dan observasi 900 VSync. Run baru [#39101435497](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39101435497) menguji urutan itu; periksa hasil gambar aktual untuk membuktikan title/menu dan Story Mode, jangan menilai keberhasilan dari readback API saja.
- RT-001 tetap **Open / blocked** sampai screenshot menunjukkan menu Naruto dan terdapat respons game yang bisa diatribusikan pada input Circle/Start.

## Audit lanjutan — korelasi PC dan struktur kode sekitar sample (2026-10-18)

- Run [#39100743589](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39100743589) selesai sukses. RSP minimum berhasil tersambung; delapan sampel PC berjeda 12 detik menunjukkan BIOS pada sampel awal, lalu rentang executable utama (`0x80061cd0`, `0x80067938`, `0x8006796c`) untuk sampel berikutnya. Ini mendukung bahwa CPU mengeksekusi kode di rentang EXE saat splash Sony tetap terlihat, tetapi belum membuktikan startup/game loop selesai.
- Satu baca 64-byte per jendela kode unik menghasilkan ringkasan kategori saja. Jendela berpusat pada sampel `0x80061cd0`: 2 conditional branches, 1 backward branch yang kembali ke dalam jendela 64-byte, 3 load dan 2 store; jendela sekitar `0x8006796c`: 3 conditional branches, 1 backward branch (target di luar jendela), 3 load dan 1 store. Tidak diekspor byte instruksi, nilai register/memori, atau disassembly mentah.
- Run [#39100957600](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39100957600) memakai `-interpreter`, berbeda dengan baseline `-dynarec`. Jadi jangan menggunakan durasi/kecepatan aktual run itu untuk menilai throughput guest. Workflow diperbaiki pada commit [b4d849c4](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/b4d849c4d555f092e1d5b406bdd67c1aa5aa3205) untuk mengembalikan `-dynarec`, sambil mempertahankan RSP PC-only rendah frekuensi serta ringkasan cabang lokal. Run baru [#39101124484](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39101124484) adalah pembandingan yang sesuai.
- Kode eksekusi di RAM dan aliran GP0 aktif berarti BIOS region-lock sebagai penghalang total boot menjadi kurang mungkin, tetapi perbedaan wilayah PAL SCPH-7502 vs disc NTSC-J belum dibuktikan sepenuhnya bukan faktor. Tetap jangan menetapkan root cause berdasarkan region saja.
- **RT-001 tetap Open / blocked.** Layar yang dapat dikenali masih logo Sony/berlian, belum title/menu Naruto, input in-game belum terbukti mengubah state, dan Story Mode belum dijalankan.

## Audit lanjutan — runtime GPU dengan SCPH-7502, 2026-10-18 (run #39100404932)

- Run [#39100404932](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39100404932) selesai sukses pada tingkat workflow. BIOS SCPH-7502 diverifikasi dari asset privat; ROM dan emulator pin sama, SoftGPU, interpreter, Port 1 Analog/remap. Artifact privat [#12125949426](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39100404932/artifacts/12125949426) memuat ringkasan aman dan PNG jendela (retensi 3 hari); raw GPUDump/VRAM/temp capture sudah dihapus sebelum upload.
- GPUDump terurai tanpa truncation. Pada rentang live tercatat 299 paket VSync, 9.126 kata GP0, 1.520 kata GP1; decoder mengurai 2.413 command-family GP0 dan mencapai `end_of_stream`. Bin VSync 200–299 memiliki 4.569 kata GP0/1.702 perintah terurai. VRAM frame 299: 772 warna RGB555 berbeda dan 333.025 piksel nonblack dari 524.288.
- Jendela PCSX-Redux yang nyata masih menunjukkan berlian oranye/kuning lalu logo SONY COMPUTER ENTERTAINMENT sekitar detik 70–85; tidak ada menu/title Naruto atau gameplay. Controller `pad.setOverride/getButton` readback lulus untuk Cross/Start/Up, tetapi karena layar tetap logo, ini hanya membuktikan nilai injeksi diterima oleh API emulator, bukan respons di game.
- Kesimpulan: bukti menolak klaim bahwa GPU sama sekali tidak menerima/menjalankan perintah gambar. Akar masalah startup/handoff belum diketahui. Pesan GP0 tak dikenal dari run sebelumnya belum terbukti menyebabkan kegagalan; stream live run ini didekode sampai akhir.
- Follow-up dipasang pada commit [d1125a9b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/d1125a9b49068f5d55862a87b6c6951c0f0ca101), run [#39100743589](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39100743589): GPU/VRAM probe yang sama ditambah hanya delapan sampel PC eksternal berjeda 12 detik (tanpa breakpoint, pembacaan instruksi/memori, atau callback register di VSync) serta filter log BIOS/CD-ROM. Tujuannya mengetahui apakah PC masih di BIOS atau berada di rentang executable utama saat splash Sony tetap tampil.
- **RT-001 tetap Open / blocked; Story Mode belum dibuktikan dimulai atau tamat.** Jangan ubah BIOS, ROM, emulator pin, renderer atau runner, dan jangan unggah ROM/BIOS/raw GPU dump/VRAM/instruction traces.



## Audit lanjutan RT-001 — 2026-10-18, setelah run #39095269662

- Artifact privat #12123793795 diperiksa secara visual: screenshot jendela PCSX-Redux yang nyata (1280×800), bukan root Xvfb. Pada ~60 detik terlihat logo SONY COMPUTER ENTERTAINMENT; pada ~80 detik layar berubah menjadi bentuk belah ketupat oranye/kuning pada latar abu-abu. Tidak ada title/menu Naruto yang teridentifikasi.
- Screenshot setelah input Return dan Z pada run #39095269662 identik piksel (0 piksel berbeda; 1280×800). Ini membuktikan tidak ada respons visual pada dua input itu di state tersebut, bukan bahwa semua input controller gagal.
- A/B run #39095269662 selesai; OpenBIOS capture seluruhnya hitam/tidak menghasilkan jendela capture valid pada checkpoint terkait. Kesimpulan tetap belum konklusif.
- Audit source pada commit PCSX-Redux 0c3572c3db75f97542001e453ae80ba8c3f8acba, src/core/gpu.cc: parser GP0 untuk cmdType=0 hanya menangani command 0x01 (clear cache) dan 0x02 (fast fill); kata nonzero lainnya dicatat sebagai unknown. Log retail 'Got an unknown GPU data word: 0008a16c (cmdType: 0, command: 0)' berarti sebuah kata GP0 tidak dikenali, tetapi belum membuktikan bahwa kata itu penyebab layar tidak masuk ke game.
- GDB eksternal pada run A/B tidak menghasilkan sampel PC yang sah. Log menunjukkan server menerima paket RSP modern yang tidak didukung (Unknown GDB command: vCont?, vMustReplyEmpty, Hgp0.0, dan lainnya); beberapa koneksi berikutnya ditolak. Jangan gunakan sampel PC tersebut sebagai bukti lokasi eksekusi.
- Langkah diagnostik berikutnya: perbaiki klien RSP agar hanya mengirim paket register minimal yang telah terbukti didukung, validasi respons tanpa polling register berulang, lalu korelasikan satu sampel yang sah dengan pesan GPU dan jejak BIOS. Pertahankan emulator, commit, BIOS, ROM, runner, dan controller yang dipatok. Jangan mengklaim boot game atau Story Mode.
## Latest retail BIOS probe — SCPH-7502 verified; game screen still unconfirmed — 2026-10-18

The user uploaded `scph7502.zip` to the existing **private** release `research-emulator-pcsx-redux-2026-10-15`. Archive size is 283,463 bytes; ZIP SHA-256 is `b436489c574457560489bfaad11b2a2171c684edba34d69de107b7b26dfc0e3a`. Private workflow [#39094479973](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39094479973) safely inspected the archive and matched the embedded 524,288-byte `scph7502/scph7502.bin` against SCPH-7502 reference hashes: MD5 `b9d9a0286c33dc6b7237bb13cd46fdee`, SHA-1 `8d5de56a79954f29e9006929ba3fed9b6a418c1d`, CRC32 `318178BF`; SHA-256 is `5e84a94818cf5282f4217591fefd88be36b9b174b3cc7cb0bcd75199beb450f1`. The ZIP and extracted BIOS were not retained as workflow artifacts or committed to the repository.

Retail BIOS probe [#39094530928](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39094530928) completed successfully in GitHub Actions at 2026-10-18 03:44 UTC (10:44 WIB). It used the pinned PCSX-Redux AnyLinux build from source commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`, same private Naruto BIN/CUE, Ubuntu 26.04, Xvfb/Mesa llvmpipe, and Port 1 Analog remap. Logs explicitly report `Known BIOS detected: SCPH-7502 (EU) (318178bf)`, disc label `SLPS-03553`, ID `SLPS03553`, EXE name `SLPS_035.53;1`, PS-X Realtime Kernel 2.5 setup, and System ROM Version 4.1.

**This is not yet proof of a valid game boot.** The screen capture is black through the early checkpoints; at ~60 seconds it has only two colors, and by ~80 seconds it renders an orange/yellow diamond-like graphic on a gray field (3,109 colors), not a recognizable Naruto title/menu or gameplay screen. Return and Z were sent while the screen was black; no visible input response was established. The log later reports `ResetCallback: _96_remove ..` then `Got an unknown GPU data word: 0008a16c (cmdType: 0, command: 0)`. The emulator was stopped by the 95-second observation cap (`GUI_PROCESS_EXIT=124`); Actions conclusion `success` indicates steps and cleanup completed, not that the game passed. Private evidence artifact [#12123793795](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39094530928/artifacts/12123793795) expires 2026-10-21 03:43 UTC and contains captures/logs, not BIOS or ROM.

**Next step:** do not repeat the same 95-second GUI run unchanged and do not switch emulator/pin or keep tweaking Mesa without new evidence. Trace guest execution around `ResetCallback: _96_remove` and the unknown GPU data word, correlate the current PC and executable/overlay state with GPU command submission, then design a bounded diagnostic run that can distinguish a guest boot stall from a rendering/command-decoding issue. Keep retail BIOS and ROM private; never commit them or publish them as Actions artifacts. `RT-001` remains **Open / blocked** until a recognizable title/menu and visible controller response are proven.

## Status terbaru — host OpenGL tervalidasi, masalah guest tetap terbuka — 2026-10-18

Tes OpenGL mandiri terbaru [#39085422680](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39085422680) lulus pada runner `ubuntu-26.04`. `glxinfo -B` pada jalur default dan `LIBGL_ALWAYS_SOFTWARE=1` sama-sama melaporkan vendor Mesa, renderer `llvmpipe (LLVM 21.1.8, 256 bits)`, dan OpenGL 4.5 Compatibility Profile. Kedua override versi tidak disetel. Program GLX yang secara eksplisit meminta konteks compatibility 3.3 berhasil membuat dan mengaktifkan konteks; versi aktualnya 4.5. Log mencatat `OPENGL_33_COMPAT_CONTEXT=PASS` dan `OPENGL_DIAGNOSTIC_RESULT=PASS`. Artifact teks aman [#12120801333](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39085422680/artifacts/12120801333) menyimpan identitas renderer, versi paket, dan hasil konteks saja.

Run runtime PCSX-Redux OpenGL [#39083372634](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39083372634) mencapai VSync 300 dan exit code 0 tetapi tidak menghasilkan gambar game yang valid: 43 kata GP0/42 command (39 state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP), VRAM frame 299 satu warna RGB555 dengan 0 piksel non-hitam dari 524.288. Source pin `0c3572c3db75f97542001e453ae80ba8c3f8acba` tidak mengimplementasikan `takeScreenShot()` pada backend `OpenGL_GPU`; `getVRAM()` tersedia. Jadi masalah generik pembuatan konteks GLX tidak didukung bukti, tetapi keadaan guest tetap belum menampilkan game.

Probe CPU/wilayah memori terbaru [#39084130154](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39084130154) selesai dan merilis artifact teks [#12119189221](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39084130154/artifacts/12119189221). Pada 14 sampel untuk load yang terkait dengan BNE `0x800372f0 → 0x80037320`, kategori effective region adalah `ram-cached` (14 hitungan); ini bukan MMIO. Dalam jendela hold 8 detik, 29 sampel PC berpusat pada dua titik loop branch yang dianalisis. Klasifikasi ini menggunakan load terbaru dalam jendela kode lokal dan bukan bukti data-flow global penuh.

**Keputusan:** jangan mengulang perubahan Mesa/versi OpenGL ataupun mengganti emulator/pin tanpa bukti baru. Fokus berikutnya adalah melacak asal dan perubahan nilai RAM yang diuji branch, lalu mengaitkannya dengan inisialisasi executable/overlay dan jalur kembali ke BIOS. Jangan menyatakan title/menu, input in-game, atau Story Mode berhasil. **RT-001 tetap Open / blocked.**

## Follow-up source-category probe — 2026-10-18, run #39083850904

Run [#39083850904](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39083850904) sukses sampai VSync 300 dan mengeluarkan artifact teks privat [#12120191058](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39083850904/artifacts/12120191058). Perbaikan [commit 8f75c3d5](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/8f75c3d558afd2261fb644e0fa192d5972ff3236) membuat CPU sampler flush statistik saat menerima SIGTERM; probe sebelumnya #39083701297 menyelesaikan emulator namun summary branch tidak sempat tertulis.

Satu sampel berkelompok pada setiap entry target:
- BNE 0x800372f0 → 0x80037320: 17 sampel unequal; operand kiri terakhir ditulis oleh kategori load, operand kanan oleh immediate arithmetic.
- BNE 0x80037330 → 0x800372d8: 15 sampel unequal; operand kiri terakhir ditulis oleh special arithmetic, operand kanan constant-zero.
- “Terakhir ditulis” merujuk penulis paling dekat yang ditemukan sebelum branch dalam jendela kode 64-byte, bukan data-flow global lengkap. Nilai register mentah, register IDs, byte instruksi dan disassembly tidak diekspor.

GP0 tetap 43 words/42 commands, dan getVRAM tetap satu warna RGB555/0 piksel non-black. Hasil ini menguatkan bahwa branch pertama membandingkan nilai yang baru dibaca oleh instruksi load, tetapi belum mengidentifikasi alamat efektif atau apakah itu RAM biasa maupun MMIO.

Hasil klasifikasi wilayah pada run [#39084130154](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39084130154) menunjukkan `ram-cached` untuk load operand kiri pada BNE pertama (14 sampel); tidak ada klasifikasi MMIO dalam ringkasan target ini. Kesimpulan hanya mencakup load lokal yang ditemukan dan jendela kode 64-byte, bukan data-flow global. Langkah berikutnya: amati apakah nilai RAM tersebut berubah selama startup, telusuri penulis terdekat dan jalur inisialisasi, serta korelasikan dengan marker loader/PC. Ekspor kategori/hitungan saja, bukan alamat efektif individual, nilai register, instruksi mentah, atau dump. RT-001 tetap Open / blocked.

## Hasil akhir sampai branch-relation test — 2026-10-18

### Host OpenGL / Mesa
Run mandiri [#39080977686](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080977686) sukses. Xvfb + Mesa llvmpipe (LLVM 21.1.8, 256 bits) membuat konteks OpenGL 4.5; konteks compatibility yang meminta 3.3 berhasil tanpa version override. Ini membuktikan lapisan GLX/Mesa host sehat, tetapi sebelumnya workflow runtime memakai flag `-softgpu`, jadi hasil standalone tidak sendiri membuktikan OpenGL backend PCSX aktif.

### Guest CPU/GPU dan loop
Run lengkap [#39080987461](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080987461) mencapai VSync 300/exit 0, tetapi hanya 43 kata GP0/42 commands: 39 GPU-state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP; tidak ada triangle/quad/line/textured-sprite. Sampling PC [#39081346569](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39081346569) menunjukkan pengulangan pada `0x80037320` dan `0x800372d8`. Static branch audit [#39082046438](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39082046438) memetakan BNE `0x800372f0 → 0x80037320` dan BNE `0x80037330 → 0x800372d8`.

Run relation [#39082587807](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39082587807) sukses: pada target-entry sample, relasi dibanding BNE pertama `unequal` sebanyak 16 kali, dan BNE kedua `unequal` sebanyak 11 kali. Delay slot tidak menulis operand yang dibandingkan menurut analisis statis. Ini konsisten dengan kedua branch terus diambil, tetapi sumber data/keadaan yang dipertahankan belum diketahui. Tidak ada nilai/register ID mentah di artifact.

### Input dan gambar/VRAM
Run [#39081872155](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39081872155): 12 pulsa tekan/lepas Cross, Start, Up semuanya dibaca kembali PASS via Lua pad API, tetapi pola PC dan GP0 tidak berubah.
Run VRAM [#39082375609](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39082375609): screenshot frame 299 320×240/16-bpp memiliki 1 warna RGB555 dan 0 piksel non-black; VRAM frame 299 (1.048.576 byte, 1024×512/16-bit) juga 1 warna dan 0 piksel non-black. Frame capture awal 235/250/265 0×0. Semua gambar/VRAM mentah dihapus sebelum artifact hanya-teks dibuat.

### OpenGL backend: extended run completed — 2026-10-18

Run [#39083372634](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39083372634) selesai success dengan pilihan backend yang eksplisit: `GPU_BACKEND_SELECTED=-openglgpu`; timeout khusus probe 170s; OpenGL vendor Mesa, renderer llvmpipe (LLVM 21.1.8, 256 bits). Emulator mencapai `GPU_TRAFFIC_VSYNC frame=300`, `GPU_DUMP_STOP observed_vsync_count=300`, dan `EMULATOR_EXIT_CODE=0`. ROM terbaca melalui SYSTEM.CNF, BOOT `SLPS_035.53`, dan marker `Execute !`.

Ringkasan tekstual artifact [#12119877576](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39083372634/artifacts/12119877576) menunjukkan GPUDump valid/tidak truncated, 299 live VSync; GP0 8 paket/43 kata, terurai jadi 42 perintah (39 GPU-state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP). Tidak ada triangle, quad, line, atau textured-sprite command. Pada frame 299, getVRAM berhasil membaca 1.048.576 byte: tepat 1 warna RGB555 dan 0 piksel non-black dari 524.288.

API `takeScreenShot()` gagal pada frame 235/250/265/299; ini sesuai source pin karena `OpenGL_GPU` tidak override metode screenshot tersebut. Capture mentah VRAM, screenshot dan GPUDump dihapus di runner sebelum artifact tekstual dibuat. API pad virtual tetap membaca balik 12 aksi press/release Cross/Start/Up sebagai PASS, tetapi pola GP0 dan VRAM tidak menunjukkan respons game.

Run [#39082912598](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39082912598) ternyata memilih `-softgpu`, bukan OpenGL; jangan jadikan bukti. Selektor diperbaiki pada [commit eb9cb4d2](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/eb9cb4d250c48a926f672b298cc51e2babf29a75), timeout untuk commit bertanda probe diperpanjang pada [commit ca472985](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/ca4729858e8f008660984b0c252ecbceb4463eae). Commit biasa tetap memilih Software GPU.

**Kesimpulan:** host Mesa/GLX dan backend OpenGL PCSX-Redux keduanya bisa berjalan di runner tanpa GPU fisik. Penghambat yang terukur sekarang berada pada sisi guest/game: loop CPU berulang, hampir tidak ada perintah gambar, dan VRAM masih hitam. RT-001 tetap Open / blocked karena belum ada gambar game/title/menu yang valid atau perubahan state game yang dibuktikan akibat input.

**RT-001 tetap Open / blocked:** belum ada screenshot game valid/title/menu dikenali, ataupun bukti game-state berubah karena input. Emulator, AppImage, BIOS dan pin tidak diubah. Setelah OpenGL backend tervalidasi, langkah berikutnya harus menelusuri sumber nilai yang membuat siklus BNE bertahan, bukan kembali mengulang tes Mesa mandiri.


## Hasil PC sampling adaptif di hotspot — 2026-10-18 (Actions #39081346569)

Run [#39081346569](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39081346569) selesai sukses sampai VSync 300, emulator exit code 0. Artifact privat teks [#12118099416](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39081346569/artifacts/12118099416) hanya memuat statistik; raw GPUDump dihapus dan baris sampel cepat tidak disimpan.

Sampler menaikkan laju nominal ke 0,1 s setelah PC masuk rentang 0x800372c0–0x800373ff, menahan mode cepat selama 8 s sejak sampel terakhir di rentang tersebut. Hasil: 31 sampel cepat, seluruhnya di dalam rentang, hanya dua PC unik: 0x80037320 sebanyak 17 sampel dan 0x800372d8 sebanyak 14 sampel. Histogram transisi: 0x80037320→0x80037320 sebanyak 10; 0x800372d8→0x800372d8 sebanyak 7; 0x80037320→0x800372d8 sebanyak 7; 0x800372d8→0x80037320 sebanyak 6. Hasil ini mendukung pola eksekusi/loop yang sangat berulang di sekitar dua alamat itu, tetapi belum membuktikan branch mana yang dieksekusi atau penyebab game tidak maju.

GPUDump tetap sama: 299 live VSync packets; 43 GP0 words / 42 commands, semuanya dalam bucket VSync 200–299; 39 GPU-state-setting, satu clear-cache, satu monochrome rectangle, satu NOP; tanpa triangle/quad/line/textured-sprite command. Jadi sampling lebih rapat belum menghasilkan gambar title/menu atau perubahan input yang terbukti.

Probe pembeda berikutnya sudah terpicu: [Actions #39081524928](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39081524928), yang menghitung edge control-flow statis di jendela hotspot tanpa menerbitkan byte instruksi/disassembly. **RT-001 tetap Open / blocked.**

## Run CPU/GPU terbaru selesai — 2026-10-18 (Actions #39080987461)

Run [#39080987461](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080987461) selesai dengan status success, mencapai target VSync 300 dan keluar normal (EMULATOR_EXIT_CODE=0). Artifact yang diunggah hanya ringkasan teks privat [artifact #12118148960](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080987461/artifacts/12118148960); raw GPUDump dihapus.

GPUDump valid, tidak truncated: 299 live VSync packets; GP0 8 packets / 43 words, GP1 11 packets / 16 words, ThrowAway 5 packets / 5 words. Semua 43 live GP0 words terparse sebagai 42 commands: 39 GPU-state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP. Semua GP0 berada pada bucket VSync 200–299; bucket 0–199 nol. Tidak ada triangle, quad, line, atau textured-sprite command. Marker GPU melaporkan guest FPS 0 pada frame 100/200 dan 1.0 pada frame 300.

RSP terhubung; qSupported sukses; 75 pembacaan bulk register valid (index 0–74). Marker EXEC header dan Execute ! muncul sekitar t=36.75 s; PC memasuki executable pada t=37.03 s (0x80050b30) serta t=38.68 s (0x8003c0b4), lalu sampel kembali dominan ke BIOS sekitar t=40.28–87.73 s (0xbfc03bxx/0xbfc075xx–0xbfc076xx), dan masuk ke executable lagi t=89.01–98.62 s (0x80037320/0x800372d8). Status CP0 umumnya 0x40000401, BadVAddr nol, Cause umumnya 0x400; beberapa sampel Cause 0x20 tidak cukup untuk menetapkan exception/penyebab.

Ringkasan kelas instruksi untuk jendela lokal 64-byte (tanpa byte instruksi atau disassembly mentah):
- 0x80050b00: branch 0, load 2, store 6, immediate arithmetic 4, special arithmetic 4.
- 0x8003c080: conditional branch 2, forward branch 2, jump 4, load 1, immediate arithmetic 5, special arithmetic 4.
- 0x80037300: backward branch 1, conditional branch 1, jump 3, load 2, immediate arithmetic 4, special arithmetic 6.
- 0x800372c0: conditional branch 2, forward branch 2, jump 1, load 3, store 2, immediate arithmetic 3, special arithmetic 5. Tidak terhitung syscall, break, COP0, atau COP2 pada keempat jendela tersebut.

Interpretasi: ini memperkuat bahwa runner GLX bukan hambatan utama; guest mencapai executable sesaat tetapi mengirim hampir tidak ada perintah gambar GP0 sampai VSync 300. Statistik lokal saja belum membuktikan loop tertentu ataupun penyebab kembali ke BIOS. Langkah berikutnya: tingkatkan korelasi transisi PC/branch target secara ringkas dan aman, tetap hindari log byte mesin/disassembly; jangan kembali ke diagnosis GLX dan jangan mengganti emulator/pin. **RT-001 tetap Open / blocked** karena belum ada gambar game, title/menu yang dikenali, atau perubahan state yang dibuktikan berasal dari input controller.


---

## Validasi ulang OpenGL host (mandiri) — 2026-10-18, Actions #39080977686

Run [#39080977686](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080977686) selesai dengan status success setelah workflow naruto-opengl-diagnostic.yml menambahkan validasi field vendor, renderer, dan versi untuk laporan GLX default serta software. Commit: [cf16162c](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/cf16162c85001d1006fee32725ce01407843ac35).

Bukti log:
- Xvfb siap pada :99; MESA_GL_VERSION_OVERRIDE dan MESA_GLSL_VERSION_OVERRIDE keduanya tidak disetel.
- GLX default dan software melaporkan vendor Mesa, renderer llvmpipe (LLVM 21.1.8, 256 bits), Compatibility Profile 4.5 serta Core Profile 4.5; marker GLXINFO_DEFAULT_CONTEXT=PASS dan GLXINFO_SOFTWARE_CONTEXT=PASS.
- Tes GLX C meminta konteks OpenGL 3.3 compatibility; konteks berhasil dibuat dan diaktifkan. Versi aktual dari glGetString(GL_VERSION) adalah 4.5 (Compatibility Profile) Mesa 26.0.8-1ubuntu0.3; marker OPENGL_33_COMPAT_CONTEXT=PASS dan OPENGL_DIAGNOSTIC_RESULT=PASS.

Interpretasi: lapisan host Xvfb/GLX/Mesa tervalidasi dan dapat membuat konteks compatibility yang diperlukan tanpa override versi. Ini tidak menunjukkan bahwa title/menu Naruto tampil dan tidak membebaskan RT-001 dari kriteria gambar game + respons input.

Audit source persis pada pin PCSX-Redux 0c3572c3db75f97542001e453ae80ba8c3f8acba:
- [src/core/gpu.h](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/gpu.h) mendefinisikan implementasi dasar GPU::takeScreenShot() yang melempar “Not yet implemented”; jangan menganggap API screenshot tersebut tersedia pada setiap backend.
- [src/gpu/soft/gpu.cc](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/gpu/soft/gpu.cc) mengisi lebar/tinggi screenshot Software GPU dari DisplayEnd - DisplayPosition. Dimensi 0×0 dari jalur ini konsisten dengan rentang display guest yang belum valid, bukan bukti kegagalan GLX.
- [src/core/pcsxlua.cc](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/pcsxlua.cc) meneruskan PCSX.GPU.takeScreenShot() ke backend GPU; binding getVRAM() tersedia untuk tes VRAM terpisah.

Arah lanjutan: jangan mengulang diagnosis GLX atau mewajibkan GPU fisik. Fokus berikutnya adalah kondisi guest (GPU PS1 display/VRAM dan eksekusi CPU) serta pemeriksaan hasil runtime terakhir sebelum mengubah harness. RT-001 tetap Open / blocked.

---

## Hasil histogram GP0 per rentang VSync — 2026-10-18 (Actions #39080239541)

Run [#39080239541](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080239541) selesai dengan target VSync 300 dan exit code 0. Dump GPU ter-parse lengkap/not truncated, 299 VSync live packets. Bucket GP0 berbasis jumlah VSync live:
- 000–049: 0 words / 0 commands.
- 050–099: 0 words / 0 commands.
- 100–199: 0 words / 0 commands.
- 200–299: 43 words, seluruhnya terparse (42 commands): 39 GPU-state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP; stop reason `end_of_stream`. GP1 live: 16 words; ThrowAway: 5 words. Tidak ada family triangle/quad/line/textured sprite pada capture ini. Dump mentah dihapus; artifact privat hanya menyimpan ringkasan hitungan dan status CPU.

Sampler CPU per run mencatat marker `Execute !` sekitar t=38.01s; PC masuk executable pada t=38.33–40.91s, lalu kembali ke BIOS mulai sekitar t=42.20s, dan masuk executable lagi sekitar t=88.39–98.63s. Semua GP0 words berada di bucket 200–299, selaras dengan kemunculan CPU di executable menjelang akhir observasi. Marker timestamp dari `pcsx.log` dipakai agar buffering stdout tidak merusak korelasi. Ini bukti urutan yang konsisten, belum membuktikan penyebab CPU meninggalkan executable atau mengidentifikasi monochrome rectangle secara visual.

Langkah berikutnya: saat RSP tersambung, ambil window memori kecil secara privat di sekitar PC executable yang sudah teramati (`0x8003717c`, `0x8003c0b4`, `0x80037320`, `0x800372d8`) dan ekspor hanya statistik kategori instruksi/cabang (mis. syscall, branch, jump, load/store, backward-branch count)—tidak pernah menulis byte mesin/disassembly mentah. Tujuannya memeriksa apakah alamat tersebut bagian dari loop tunggu atau jalan kembali ke BIOS. **RT-001 tetap Open / blocked.**

---

## Hasil korelasi CPU/GP0 dengan marker bertimestamp — 2026-10-18 (Actions #39079981314)

Run [#39079981314](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079981314) selesai dengan conclusion `success`; emulator mencapai target VSync 300 lalu dihentikan normal oleh probe (`EMULATOR_EXIT_CODE=0`). Aset privat serta hash BIOS/ROM/AnyLinux diverifikasi. Tidak ada raw GPUDump atau instruksi/operand mentah di artifact.

**GPUDump setelah TraceBegin:** 299 VSync packets / 598 words; GP0 8 packets / 43 words; GP1 11 packets / 16 words; ThrowAway 5 packets / 5 words; truncated=false. Pretrace GP0 baseline 262153 words adalah reset + VRAM upload untuk state awal dump, bukan rendering game. Parser sementara mengonsumsi semua 43 live GP0 words tanpa sisa dan mengklasifikasikannya sebagai 42 perintah: GPU-state-setting=39, clear-cache=1, monochrome-rectangle=1, NOP=1. Tidak ada keluarga triangle, quad, line, atau textured sprite pada jendela sampai VSync 300. Ini berarti ada sedikit traffic grafis, tetapi belum ada gambar yang terlihat; screenshot Software GPU 320×240 dan screenshot jendela X11 1280×800 tetap hitam pada run sebelumnya.

**Korelasi CPU:** RSP tersambung; `qSupported` berhasil; 76 paket bulk register valid sebelum target berhenti. Marker log yang kini ditimestamp dari `pcsx.log`: SYSTEM.CNF sekitar t=4.85s, BOOT path t=6.14s, EXEC header dan `Execute !` sekitar t=38.01s. Sampel PC segera sesudahnya masuk ke executable utama (t=38.33s `0x8003717c`, t=39.62s `0x8003c0b4`, t=40.91s `0x80037320`), lalu kembali ke BIOS range mulai sekitar t=42.20s. Sampel berada di BIOS sampai sekitar t=87.09s dan masuk lagi ke executable pada t=88.39s (`0x800372d8`), dengan beberapa sampel lanjutan di `0x80037320/0x800372d8` hingga t=98.63s. CP0 Status umumnya `0x40000401`, BadVAddr nol, Cause umumnya `0x400`; dua sampel Cause `0x20` tidak cukup untuk menyimpulkan root cause tanpa sampling lebih rapat. Timestamp dari `pcsx.log` dipilih karena stdout buffered; jangan gunakan timestamp marker lama dari stdout sebagai korelasi akurat.

Interpretasi: host Mesa/GLX sehat; guest CPU masuk ke executable sebentar-sebentar tetapi pada jendela sekitar 100 detik hanya mengirim 43 GP0 words (kebanyakan state command, satu monochrome rectangle), dan tidak menampilkan title/menu. Ini lebih konsisten dengan masalah inisialisasi/looping guest daripada kebutuhan GPU fisik, tetapi akar sebab belum dipastikan. Probe berikutnya akan mengelompokkan waktu GP0 command berdasarkan VSync range agar terlihat apakah semuanya hanya terjadi saat startup.

**RT-001 tetap Open / blocked.** Belum ada title/menu yang dikenali, perubahan state dari input yang diverifikasi, atau Story Mode.

---

## Hasil final GPUDump sampai timeout dan probe korelasi CPU berikutnya — 2026-10-18

Run [#39079291837](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079291837) selesai dengan conclusion Actions `success` (semua langkah/cleanup berhasil), tetapi proses emulator berakhir pada batas observasi 90 detik (`EMULATOR_EXIT_CODE=124`); jangan mengartikan status workflow sebagai game sukses boot. Log mencapai `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, `EXEC:PC0(80011448)` dan `Execute !`. GPU traffic dump ter-parse lengkap, `GPU_DUMP_TRUNCATED=false`, satu marker `TraceBegin`, dan 268 VSync packets / 536 live words. Sesudah TraceBegin: **GP0 packets=0, words=0; GP1 packets=1, words=1; VSync packets=268**. Baseline pre-trace GP0 262153 words berisi reset dan full 1024×512 VRAM upload untuk merekonstruksi keadaan awal dump, bukan gambar yang dikirim game. Dump mentah dihapus sebelum upload artifact, yang hanya menyimpan ringkasan teks/log. Emulator timeout 124 adalah batas observasi, bukan crash diagnosis.

Untuk menghubungkan hasil grafis dengan CPU, workflow [`naruto-fastboot-gpu-traffic-summary.yml`](.github/workflows/naruto-fastboot-gpu-traffic-summary.yml) kini diperbarui agar satu run men-sample bulk RSP register `g` (PC + CP0 Status/BadVAddr/Cause) dengan timestamp relatif dan marker loader sambil merekam GPUDump, tanpa instruksi/operand mentah. Commit terbaru [`30cd69d6`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/30cd69d61a5ab01761baa7f3a209a386f205b650); run konfirmasi [#39079600379](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079600379) terakhir terlihat pending di antrean ketika entri ini dibuat. Periksa log/run selesai sebelum menafsirkan sampel itu.

Kesimpulan tetap terbatas: host GLX/Mesa sehat; jendela emulator dan screenshot software GPU hitam; tak ada GP0 drawing command yang terekam pada 268 VSync pasca-TraceBegin. Ini menunjuk ke inisialisasi/eksekusi game tamu, tetapi tidak menentukan akar sebab. **RT-001 tetap Open / blocked.**

---

## Pembuktian GL host dan traffic GPU tamu — 2026-10-18

- Run OpenGL mandiri [#39049689832](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39049689832): Mesa `llvmpipe (LLVM 21.1.8, 256 bits)`, OpenGL 4.5 Core/Compatibility Profile, tanpa version override; konteks Compatibility 3.3 berhasil dibuat. Host GLX/Mesa sehat, dan belum ada alasan teknis untuk menuntut GPU fisik.
- Source build pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`: `GPU::takeScreenShot()` bawaan melempar `Not yet implemented`; backend OpenGL GPU tidak mengimplementasikannya, sedangkan Software GPU punya implementasi screenshot. Run [#39078905140](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078905140) dengan `-softgpu` menghasilkan screenshot frame 300 valid 320×240 tetapi seluruh piksel hitam; VRAM 1024×512 juga satu warna hitam.
- Run window capture [#39079066598](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079066598) mengambil enam screenshot jendela PCSX-Redux non-root XID `0x200034` pada t=5,15,30,45,60,75 detik. Semuanya valid 1280×800 namun seragam hitam. Tidak ada title/menu.
- GPUDump summary parsial dari run [#39079279565](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079279565) (run berhenti/cancel saat workflow diperbarui) berhasil mem-parse dump sampai 136 live VSyncs tanpa truncation. Sesudah TraceBegin: `GP0 packets=0, words=0`, `GP1 packets=1, words=1`, `VSync packets=136, words=272`. Baseline pre-trace berisi 262153 GP0 words karena reset/full VRAM upload untuk merekonstruksi state dump; angka itu bukan trafik gambar game. Raw GPU dump dihapus; artifact privat hanya summary/log.
- Run konfirmasi dengan workflow saat ini [#39079291837](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079291837) sedang merekam sampai target VSync 300 saat catatan dibuat; periksa hasil finalnya sebelum menyatakan hasil penuh.

Interpretasi sementara: masalah yang terlihat tidak lagi cocok dengan kegagalan pembuatan konteks OpenGL host. Data mengarah bahwa executable tamu mencapai marker `Execute !`, tetapi belum mengeluarkan perintah gambar GP0 selama jendela yang direkam. Ini belum mengidentifikasi penyebab di CPU/game loader. RT-001 tetap **Open / blocked**: title/menu dan respons input belum terbukti; Story Mode belum dimulai.

---

## Lanjutan diagnosis VRAM dan callback UI — 2026-10-18

Run [#39050174557](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39050174557) memakai timer rekursif melalui `PCSX.nextTick()`, tetapi tidak menghasilkan checkpoint (`NO_VALID_TIMED_CAPTURES`). Audit source pada pin `0c3572c3db75f97542001e453ae80ba8c3f8acba` menjelaskan kelemahan harness: `PCSX.nextTick()` menyimpan callback di `AfterPollingCleanup`; pada `src/core/ui.cc`, `UI::tick()` menjalankan callback tersebut lalu membersihkan field yang sama. Penjadwalan ulang dari callback itu dapat tertimpa. Kegagalan ini adalah kegagalan metode sampling, bukan bukti kegagalan OpenGL.

Run [#39078592809](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078592809) mengambil sembilan sampel VRAM langsung saat `GPU::Vsync`: frame 1, 2, 3, 5, 10, 20, 30, 45, dan 60. Semua buffer berukuran 1.048.576 byte, hanya memiliki satu warna 15-bit, rasio non-black 0, dan hash PNG yang identik. Guest FPS bernilai 0 pada checkpoint itu. Namun, semua snapshot tersebut berada sebelum marker log `Execute !`; run kemudian mencatat `GPU::Vsync frame=300 guest_fps=1.0000` setelah handoff. Karena itu, sampel hitam tersebut hanya membuktikan VRAM awal yang kosong sebelum executable berjalan, bukan keadaan pasca-handoff. Run berakhir pada timeout 90 detik (124), lalu menghapus buffer mentah; artifact privat hanya berisi PNG/summary.

Capture langsung dari event GPU bukan pola yang akan diteruskan karena API readback OpenGL perlu dijalankan pada thread UI/konteks grafis yang benar. Workflow telah diubah lagi pada commit [`3a69fcef`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/3a69fcef242563ecf45de8c920bec3443db3e956) untuk menjadwalkan capture dari event ke thread UI melalui `PCSX.nextTick()`, tanpa timer rekursif. Run [#39078732160](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078732160) menguji versi deferred itu pada frame 1 dan 60; status terakhir yang diperiksa: masih berjalan, belum ada hasil yang boleh disimpulkan.

**RT-001 tetap Open / blocked.** Belum ada title/menu yang dikenali dan belum ada perubahan state akibat input yang terverifikasi. Perlu capture pasca-handoff (target VSync sekitar 300, sebagaimana marker runtime) sebelum mengubah hipotesis gameplay/rendering.

---

## Hasil diagnosis OpenGL mandiri — 2026-10-17 (Actions #39049689832)

Run [#39049689832](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39049689832) menambahkan dan menjalankan workflow mandiri `.github/workflows/naruto-opengl-diagnostic.yml` pada commit [`3e92e100`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/3e92e100abf17a51e4e335e92ea7b70632293933). Hasil: job `mesa-opengl` **success**. Xvfb dan GLX siap; tes `glxinfo -B` sukses baik pada konfigurasi default maupun saat `LIBGL_ALWAYS_SOFTWARE=1`. Keduanya melaporkan OpenGL vendor `Mesa`, renderer `llvmpipe (LLVM 21.1.8, 256 bits)`, OpenGL 4.5 Compatibility Profile dan Core Profile (Mesa 26.0.8); capability report menyatakan max core/compat 4.5. Variabel `MESA_GL_VERSION_OVERRIDE` dan `MESA_GLSL_VERSION_OVERRIDE` tidak disetel. Program GLX C kecil juga membuat/mengaktifkan konteks compatibility yang meminta OpenGL 3.3, lalu membaca versi aktual 4.5; marker `OPENGL_33_COMPAT_CONTEXT=PASS`.

Interpretasi: runner cloud ini dapat membuat konteks OpenGL yang memadai melalui Mesa software rendering; tidak ada bukti GPU fisik diperlukan. Hasil sebelumnya `takeScreenShot()` 0×0 harus dipisahkan dari kesehatan GLX. Source PCSX-Redux yang tepat pada commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`, `src/gpu/soft/gpu.cc`, menghitung dimensi screenshot dari `DisplayEnd - DisplayPosition`; dimensi kosong dapat berarti register display GPU PlayStation belum menginisialisasi rentang gambar. `src/core/pcsxlua.cc` menyediakan `PCSX.GPU.getVRAM()`, jalur diagnosis berikutnya untuk memeriksa VRAM emulasi terpisah dari display screenshot.

Run visual sebelumnya [#39047765424](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39047765424) tetap gagal menghasilkan gambar: satu metadata frame menyatakan ukuran/dimensi 0×0, summary `NO_VALID_GPU_SCREENSHOTS`, emulator dihentikan oleh batas 90 detik (exit 124). Kesuksesan workflow bukan keberhasilan game boot. Belum ada title/menu maupun perubahan state akibat input yang terkonfirmasi.

**Langkah berikutnya:** pertahankan AnyLinux AppImage dan pin yang sama; ambil checkpoint VRAM 1024×512 melalui `PCSX.GPU.getVRAM()` setelah VSync dan konversi di runner ke gambar diagnostik. Jangan sertakan raw VRAM/dump mentah di artifact. Bandingkan beberapa checkpoint sebelum/sesudah input dan catat hanya screenshot diagnostik privat serta statistik ringkas. Jika VRAM kosong/tidak berubah, lanjutkan korelasi dengan polling PC/CP0 dan marker loader—bukan mengganti emulator atau menyimpulkan GPU fisik diperlukan.

**RT-001 tetap Open / blocked.**

---

## Diagnosis CPU polling dan keputusan probe berikutnya — 2026-10-17 (Actions #39029860914)

Run [#39029860914](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39029860914) menyelesaikan semua langkah workflow (`success`), termasuk unggah artefak privat dan cleanup. Emulator yang diuji adalah PCSX-Redux AnyLinux AppImage dengan OpenBIOS fastboot, ROM serta BIOS yang SHA-256-nya diverifikasi, setup Port 1 Analog/remap, dan command line `-exec ... -gdb -gdb-port 3333 -run`. Tidak ada breakpoint atau watchpoint pada eksperimen ini.

Klien RSP minimal tersambung dan `qSupported` berhasil. Polling menghasilkan 41 sampel selama sekitar 65 detik, dengan 14 nilai PC unik. Distribusi: rentang BIOS 31 sampel; rentang executable utama `0x80010000–0x8006d7ff` sebanyak 2; alamat lain sebanyak 8. PC sempat terlihat di `0x8003c0a0` pada sekitar 36,3 detik dan `0x8003bff4` pada sekitar 37,9 detik sejak polling dimulai, kemudian sampel pada sekitar 39,5 detik dan seterusnya kembali berada di BIOS, banyak di `0xbfc075b0–0xbfc07608`. Marker loader `SYSTEM.CNF`, `BOOT = cdrom:\SLPS_035.53;1`, `EXEC:PC0(80011448)`, dan `Execute !` ada di log, tetapi waktu marker tidak direkam di dalam jendela polling. Korelasi waktunya adalah petunjuk, bukan bukti sebab-akibat yang tuntas.

CP0 pada pembacaan bertahap: `BadVAddr=0`; `Status` biasanya `0x40000401` (satu sampel `0x40000000`); `Cause` biasanya `0x00000400`, dengan dua sampel `0x00000020`. Ini bukan snapshot atomik karena PC dan setiap CP0 dibaca melalui paket RSP terpisah. Query `?` menghasilkan `S00`; source GDB-server pada commit AppImage `0c3572c3db75f97542001e453ae80ba8c3f8acba` menyatakan `S00` adalah jawaban query ketika emulator masih running, **bukan stop event**. Jangan menyebut hasil ini sebagai exception loop yang sudah terbukti.

Audit source yang sesuai build: [src/core/gdb-server.cc pada commit 0c3572c3](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/gdb-server.cc) mendefinisikan urutan register RSP; `g` mengembalikan paket semua register, dengan indeks 32=Status, 35=BadVAddr, 36=Cause, dan 37=PC. Karena itulah langkah pembeda berikutnya adalah satu pembacaan bulk `g` per sampel (576 karakter hex untuk 72 register 32-bit), plus cap waktu marker loader yang diamati langsung dari log. Ini mengurangi ketidakselarasan waktu dari query bertahap dan menghubungkan transisi PC dengan `Execute !` tanpa mengulang breakpoint/GPU-watchpoint.

Ringkasan bertanda `CPU_SAMPLER_EXIT=124` dalam log adalah salah label harness: heredoc Python polling berjalan di foreground, sedangkan `$!` masih merujuk proses emulator `timeout`; nilai 124 berasal dari batas observasi emulator 100 detik. Bukti bahwa sampler bekerja adalah 41 baris `CPU_SAMPLE`, diikuti `CPU_SUMMARY`; proses emulator terdeteksi selesai dan cleanup berhasil. Perbaiki label dan pengelolaan PID pada workflow berikutnya.

Artefak privat: [#12100266232](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39029860914/artifacts/12100266232), retensi sampai 2026-10-20 11:46:41 UTC. ROM, BIOS, emulator dan log sementara telah dibersihkan dari runner.

**RT-001 tetap Open / blocked.** Title/menu Naruto, respons input gameplay, dan Story Mode belum terbukti; belum ada aturan gameplay runtime yang boleh ditetapkan.

---

## Hasil Actions terbaru — 2026-10-17 (run #39021127913)

Run [#39021127913](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39021127913) telah selesai dengan status GitHub Actions `success`; itu hanya menandakan langkah workflow dan cleanup selesai, bukan game berhasil boot sampai menu.

Bukti runtime yang terkonfirmasi:
- Klien RSP tersambung ke PCSX-Redux port 3333; `qSupported` sukses dan breakpoint `Z1,80011448,4` mendapat balasan `OK`.
- Konfigurasi eksperimen sudah memasukkan upaya setup controller Port 1 Analog dan remap yang juga dipakai pada probe sebelumnya.
- Log PCSX-Redux mencatat disc `SLPS-03553`, `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, `EXEC:PC0(80011448) T_ADDR(80010000) T_SIZE(0005d800)`, dan `Execute !`.
- Walaupun loader mencatat handoff executable, selama jendela tunggu 40 detik tidak ada stop event breakpoint yang sah. Ctrl-C RSP kemudian menghasilkan `T05`; sampel register sesudah interrupt menunjukkan PC `0x80000080`, CP0 Status `0x40000404`, BadVAddr `0x00000000`, Cause `0x00000400`. Nilai tersebut hanya snapshot ketika interrupt/handler, bukan diagnosis root cause.
- Karena kondisi entry `PC == 0x80011448` tidak pernah diverifikasi, workflow dengan benar **tidak** meneruskan GPU GP0/GP1/DMA2 watchpoints. Jangan menyebut GPU watchpoint hit atau menyimpulkan bahwa game sudah menjalankan rendering.
- Run ini tidak mengambil bukti visual baru. Hasil capture terdahulu tetap layar hitam; title/menu serta respons input belum terbukti.

Artifact privat `naruto-fastboot-gpu-watchpoints-private` (ID `12096697815`) tersedia sampai sekitar 2026-10-20 09:28 UTC. ROM, BIOS, emulator, log dan file sementara telah dibersihkan dari runner.

**Langkah berikutnya:** hentikan sementara eksperimen breakpoint/watchpoint karena breakpoint remote belum terbukti bisa menangkap entry meskipun balasan pemasangan `OK`. Gunakan command line baseline yang telah terbukti mencapai `Execute !` dengan `-exec` Port 1 Analog setup **dan** `-run`, lalu lakukan polling register PC/CP0 minimal dan rapat selama boot (tanpa GDB modern; gunakan klien RSP minimal yang sudah berhasil). Korelasikan sampel PC dengan marker loader untuk menentukan apakah CPU masuk ke kode EXE, tetap berputar di BIOS/exception vector, atau berpindah bolak-balik. Jangan mulai GPU watchpoint lagi sebelum mekanisme breakpoint diverifikasi terpisah dan jangan mengulang tes backend grafis.

**RT-001 tetap Open / blocked.** Story Mode belum dimulai/tamat; jangan menetapkan aturan gameplay berdasarkan dugaan.

---

# Log analisis dan handoff

## Koreksi validitas RSP GPU-watchpoint dan rerun — 2026-10-17

Audit run [#39017636267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017636267) menemukan hasil “entry breakpoint” dan “GPU GP0 watchpoint hit” **tidak valid sebagai hit yang terkonfirmasi**: klien RSP menganggap paket konsol PCSX-Redux berawalan `O` (mis. teks `PCSX::MIPS>`) sebagai stop event. Pada run itu, PC yang dibaca setelah event tetap berada di BIOS (`0xbfc0867c` dan `0xbfc05784`), bukan di entry executable Naruto. Karena itu entry breakpoint belum terbukti tercapai dan GP0 belum boleh dinyatakan terpicu. Watchpoint GP1/DMA2 juga hanya timeout dalam uji terdahulu. Workflow berakhir `success` hanya berarti harness dan cleanup selesai; bukan hasil positif target.

Workflow diperbaiki pada commit `5055074671acf8cb2f2512182f8484dc2815552d`: parser kini mempertahankan buffer lintas paket, mengabaikan paket console `O` saat menunggu stop, serta hanya menerima jawaban stop RSP `T/S/W/X`. Sesudah entry stop, ia memeriksa PC harus tepat `0x80011448` sebelum menghapus breakpoint dan mencoba GP0/GP1/DMA2. Run [#39020901596](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39020901596) kini selesai `success` pada tingkat workflow, tetapi **tidak mencapai entry executable dalam batas 20 detik**: tidak ada stop event breakpoint dan setelah Ctrl-C PC masih `0xbfc03bdc` di BIOS. Log mengenali `SYSTEM.CNF` dan `BOOT = cdrom:\\SLPS_035.53;1`, tetapi tidak mencapai `EXEC:PC0`/`Execute !`. Ini bukan bukti hit GPU; watchpoints tidak diuji karena probe berhenti pada kegagalan entry. Run tersebut juga berbeda dari baseline karena belum menerapkan setup Port 1 Analog yang ada pada run sebelumnya. Commit `a8d8db8a0c3b84967a14c3a0905e046dbed24cf9` kini menerapkan Port 1 Analog + remap yang sama dan memperpanjang masa menunggu entry menjadi 40 detik; run baru [#39021127913](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39021127913) baru dimulai. Baca PC dan log final sebelum hipotesis lanjut.

Layar game belum berubah dari hitam dalam bukti visual sebelumnya; title/menu serta respons input belum terbukti. **RT-001 tetap Open / blocked; Story Mode belum dimulai/tamat.**

## Pembaruan eksperimen — 2026-10-17

## Hasil RSP minimal dan eksperimen GPU-watchpoint — 2026-10-17

Run [#39017271906](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017271906) selesai dengan conclusion Actions `success` dan cleanup berhasil. Klien RSP minimal terhubung ke PCSX-Redux AnyLinux pada port 3333, negosiasi `qSupported` berhasil, dan 10 sampel register PC/CP0 berhasil dibaca tanpa GDB modern yang mengirim command tak didukung. Sampel PC meliputi `0x8003C0A0` dan `0x80037320`, yang berada dalam rentang EXE utama berdasarkan header/load range `0x80010000` dengan text size `0x5D800`; sampel lain juga meliputi alamat BIOS. `BadVAddr=0` konsisten di seluruh sampel dan `Cause=0x400`; jangan tafsirkan nilai ini sebagai diagnosis exception final. Status target RSP `S00` menunjukkan target sedang running saat diperiksa. Karena sampel jarang dan bercampur alamat BIOS/EXE, ini bukan bukti cukup bahwa inisialisasi game selesai.

Jendela non-root PCSX `0x200034` (1280×800) masih uniform black (mean 0, standard deviation 0, satu warna) pada capture sebelum input, setelah Return/Cross, dan sekitar 40/65/90 detik; OCR kosong. Loader tetap mencatat `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, `EXEC:PC0(80011448)`, `Execute !`. Dengan demikian pembacaan register kini bekerja, tetapi title/menu dan respons input masih belum terbukti. Artifact diagnostik privat `12095198494` retensi 3 hari; tidak ada dump memori atau instruksi mentah di artifact.

Eksperimen pembeda berikutnya saat catatan ini diperbarui: workflow [#39017636267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017636267) memasang breakpoint entry `0x80011448` saat emulasi masih paused, lalu memantau write-watchpoint pada register GPU GP0/GP1 dan DMA2 melalui klien RSP minimal. **Run ini masih berlangsung saat catatan ini dibuat; jangan menyimpulkan hasil watchpoint sampai log selesai diperiksa.**

**RT-001 tetap Open / blocked.** Story Mode belum dimulai/tamat; jangan menetapkan aturan gameplay runtime sebelum title/menu dan input terverifikasi.

---

Tanggal ringkasan: 2026-10-15

Catatan ini merangkum pekerjaan yang sudah dijalankan dan batasannya agar sesi/agen berikutnya dapat melanjutkan tanpa mengulang asumsi.

## Pemeriksaan file

- File yang dianalisis: Naruto - Shinobi no Sato no Jintori Gassen (Japan).bin.
- Ukuran file: 325.989.552 byte.
- Format yang terdeteksi: PS1 raw sector, stride 2352 byte, 138.601 sektor.
- Payload diekstrak sementara untuk membangun ISO dan membaca filesystem; file asli tidak diubah.
- Serial disc: SLPS-03553.
- CRC32: dfe1f8b3.
- SHA-256: 58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88.
- ISO memuat DATA.BIN, DATA2.BIN, DUMMY.BIN, SLPS_035.53, SYSTEM.CNF, XASECT.BIN; ukuran lengkap tercatat di docs/ROM_STRUCTURE.md.
- SYSTEM.CNF menunjuk ke SLPS_035.53; executable utama header-memuat base 0x80010000, PC 0x80011448, text size 0x5D800.

## Analisis kode statis

- Disassembly awal mengindikasikan instruksi MIPS R3000A di executable utama dan beberapa blok DATA.BIN.
- Tidak ditemukan teks aturan kunci sebagai string Shift-JIS literal biasa di file yang diekstrak pada pencarian awal. Struktur string/resource perlu dipetakan lebih lanjut.
- Struktur pemain yang digunakan beberapa rutin memiliki empat slot, stride 0xB4 byte, field Chakra pada offset +0x18.
- Setter Chakra membatasi rentang ke -9.999 sampai 99.999.
- Target konfigurasi 3.000 ditemukan dan dipakai oleh cabang pemeriksaan target pada jalur akhir pertandingan yang ditelusuri.
- Field kepemilikan petak diperiksa sebagai bagian bitfield, dengan empat bit teratas dipakai sebagai ID owner pada jalur yang diperiksa.
- Sejumlah alamat rutin dan flag akhir permainan masih merupakan label kerja; lihat docs/OVERLAY_MAP.md.

## Sumber gameplay sekunder yang diperiksa

- Transkripsi UI Story Mode dan kartu dari proyek terjemahan fan.
- Panduan Jepang yang menguraikan unlock dan opsi Party Mode.
- Materi promosi TV Tokyo.
- Ulasan gameplay Jepang tahun 2025.
- Data identitas disc dari GameGear Archive dan PSX Data Center.

Informasi eksternal digunakan untuk membuat hipotesis tentang makna kode, bukan menggantikan bukti runtime. Biaya 60/150 yang ditunjukkan oleh contoh UI tidak dinyatakan sebagai formula universal.

## Eksekusi runtime

- Dalam sesi terdahulu, emulator PS1 tidak ditemukan pada lingkungan eksekusi lokal.
- Upaya berikutnya untuk menjalankan terminal/Python ditolak oleh lingkungan, sehingga pemetaan overlay dan tes debugger tidak dapat dilanjutkan.
- GameGear Archive punya catatan pihak ketiga bahwa dump repack CHD boot pada Mednafen PSX HW selama uji otomatis 64 detik. Penelitian ini sendiri belum melaksanakan uji terkontrol terhadap barrier, battle, kartu, atau kondisi menang.

## Arahan untuk kelanjutan

1. Otorisasi tetap: pemilik memberi ChatGPT izin berkelanjutan untuk memperbarui repo Naruto secara otomatis sesuai kebutuhan penelitian. Izin ini hanya berlaku pada repo ini; Claude ditetapkan khusus untuk Tile Duel dan tidak boleh mengakses repo Naruto.
2. Jangan mengunggah file ROM/ISO, aset game, dump memori, atau save state ke repositori.
3. Mulai dari direktori resource DATA.BIN yang kini dipetakan; selidiki format PK02/BIN0/TPK0, consumer XASECT, dan relasi DATA2.BIN.
4. Uji aturan di emulator/debugger, lalu simpan log dan hasil secara teks/screenshot yang tidak mengandung aset berhak cipta yang tidak diperlukan.
5. Pelihara label confidence dan catat semua koreksi terhadap temuan lama.
6. Jangan pernah menyentuh repo Tile Duel dalam pekerjaan penelitian ini.

## Pembaruan byte-level dan klasifikasi resource — 2026-10-15

- Mengambil kembali ROM sumber dari Library ChatGPT ke folder kerja lokal; hash lengkap cocok dengan nilai yang sudah tercatat di docs/ROM_STRUCTURE.md. Pengguna juga menyimpan salinan di laptop.
- Mengekstrak enam file filesystem ISO ke salinan kerja lokal, tanpa mengubah ROM sumber dan tanpa mengunggah ROM/ISO/aset ke GitHub.
- Memverifikasi direktori di DATA.BIN: 0x44 byte bootstrap, 0x2F00 byte tabel, 1.504 entri × 8 byte; 1.500 entri aktif dan empat entri kosong pada indeks 1491–1494.
- Memverifikasi bahwa entri aktif tidak tumpang-tindih dan seluruh interval yang dibulatkan ke sektor berada dalam extent DATA.BIN. Total cakupan direktori 32.227 dari 32.234 sektor.
- Klasifikasi signature: PK02 921, TIM valid 246 (29 4-bit; 217 8-bit), NARUTOSceneV001 126, NARU lainnya 125, PSQ0 enam, PSQ1 dua, TXT2 satu, belum terklasifikasi 73.
- Pemeriksaan XASECT.BIN menemukan 86 pasangan 32-bit. Consumer di sekitar 0x80019468 menghitung indeks input >> 4, mengindeks pasangan dengan stride 8, lalu menggunakan field pertama sebagai offset aditif. Makna penuh field masih belum ditentukan.
- Semua analisis tersebut statis. Belum ada pengujian gameplay dengan debugger/emulator dan belum ada formula barrier, pendapatan, battle, atau efek kartu yang dinaikkan statusnya menjadi terkonfirmasi runtime.
- Detail lengkap: docs/RESOURCE_CATALOG.md dan HANDOFF_LANJUT.md.


## Arsip file ekstraksi di Library — 2026-10-15

- Menyimpan `DATA.BIN`, `DUMMY.BIN`, `SLPS_035.53`, `SYSTEM.CNF`, dan `XASECT.BIN` di Library pada folder `Naruto Research Files`.
- `DATA2.BIN` mentah gagal disimpan karena batas kapasitas Library; mengompresnya menjadi ZIP sekitar 42 MiB dan berhasil menyimpan `DATA2.BIN.zip`.
- File game tidak ditambahkan ke GitHub. Jangan menghapus item Library lain tanpa izin. Detail pemulihan ada di `HANDOFF_LANJUT.md`.
- Fokus riset selanjutnya tetap mencari aturan gameplay yang pasti: trace jalur transaksi Chakra, barrier/upgrade, income, battle, dan victory flags; bongkar format resource hanya bila jalur kode terbukti bergantung padanya.


## Pembaruan penelusuran aturan gameplay dan aturan sumber data — 2026-10-15

### Sumber file dan batas kuota

- Melanjutkan analisis dari file hasil ekstraksi yang sudah berada di Library; tidak membutuhkan dan tidak meminta upload ulang ROM 300 MB dari laptop.
- Hash SHA-256 yang cocok dengan catatan terdahulu: SLPS_035.53 = a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569; DATA.BIN = 69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822; XASECT.BIN = df257fbdabdb848f845466246abf4a36fdb6cf17815fc3a76ff7d7585d1953f0; DATA2.BIN hasil unzip = be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9. ZIP DATA2.BIN.zip = 67e7a372c6d02379d8cc715d15f3521c0914b8f17ee6e2f66a2bc32695367668.

### Jejak konfigurasi target Chakra

- Dalam executable utama, tabel 0x80057798 (file offset 0x47F98) menggunakan stride 0x54. Record yang diperiksa memuat (ID mentah, +0x04, +0x08, +0x0C): (0xA00,1500,3000,400), (0x10B01,2000,4000,400), (0x20C02,2000,4000,400), (0x81210,600,0,0), (0x31403,2500,5000,400), (0x40E04,2500,5000,400), (0x81211,600,0,0), (0x50F0F,2500,5000,400), (0x61106,3000,6000,400), (0x60809,3000,6000,400).
- Field +0x04 disalin ke global 0x80070C80 dan jalur inisialisasi meneruskannya ke setter Chakra; confidence tinggi bahwa ini nilai awal. Field +0x08 masuk lewat getter 0x80012A70 dan dipakai sebagai target pada cabang hasil dengan kondisi yang mencakup bit 0x200. Confidence tinggi untuk peran target, menengah–tinggi untuk pemetaan modul gameplay karena loader belum dipastikan runtime.
- Tabel kedua di 0x80064918 (file offset 0x55118, stride 0x30) menunjukkan nilai 1500/3000 pada sekurangnya 13 record awal nonnol yang diperiksa.
- Arti field +0x0C (400 atau 0) serta mapping raw ID ke nama stage/mode belum diketahui. Target 0 pada sebuah record tidak boleh diperlakukan sebagai kemenangan otomatis.
- Sumber terjemahan Story Act 01 menyebut target 3000; ini cocok dengan satu record, tetapi mapping ID satu-ke-satu belum terbukti.

### Peta kode dan koreksi

- DATA.BIN entry index 1 berada pada file offset 0x10BB000 dan berukuran 596.412 byte. Pemetaan sementara ke base RAM 0x800D0000 menghasilkan referensi internal konsisten, tetapi belum dikonfirmasi lewat breakpoint loader.
- Dalam peta statis tersebut, cabang sekitar 0x80111228, 0x801112CC, 0x801113B4, 0x801114F0, 0x80111588 dan 0x80112418 memeriksa kondisi target dan Chakra pemain sebelum mengubah pemenang/state hasil.
- Label terdahulu bahwa 0x800EC200 adalah pembanding target dan sekitar 0x800F70D0 aritmetika Chakra ditarik kembali karena identitas/base modul belum dibuktikan.
- Setter Chakra 0x8001387C menjepit ke [-9999, 99999]; nilai Chakra ada di +0x18 dalam struktur empat slot dengan stride 0xB4.

### Yang belum terkonfirmasi dan tugas berikutnya

- Belum ditemukan formula universal biaya barrier/upgrade, income, damage/durability battle, roulette, atau semua efek kartu. Angka UI 60 dan 150 bukan formula universal terkonfirmasi.
- Prioritas berikutnya adalah menelusuri call chain event ESTATE dan LVUP_ESTATE, transaksi Chakra, pendapatan, dan perubahan kepemilikan. Pemanggil setter yang perlu dipilah berdasarkan konteks termasuk 0x800D6D60, 0x800D6E04, 0x800D7AB0, 0x800D7B14, 0x800D8DE8, 0x801016E8, 0x80104790, 0x8010F554, 0x8012CD0C, 0x8012CD60, dan 0x8012D1E8; lokasi pemanggil saja tidak menetapkan makna transaksi.
- Tidak ada tes runtime debugger/emulator yang selesai. Semua klaim di atas tetap analisis statis.


## Penelusuran Chakra: setter, delta event, dan batas inferensi — 2026-10-15

- Pemeriksaan callsite `jal 0x1387C` pada resource yang sementara dipetakan ke `0x800D0000` menunjukkan beberapa panggilan hanya menyalin field Chakra yang sudah ada dari record runtime ke setter pemain aktif. Daftar itu mencakup `0x800D6D60`, `0x800D6E04`, `0x800D7AB0`, `0x800D7B14`, `0x800D8DE8`, `0x801016E8`; jadi daftar pemanggil setter tidak bisa dipakai sebagai daftar transaksi biaya.
- State machine sekitar `0x8012C600` mereset `+0xB44`, lalu membentuk `+0xB40 = +0xB30 + +0xB38`. Dalam state 7 (`+0xB2A == 7`), jalur `0x8012CD04–0x8012CD74` menggunakan `+0xB44` sebagai jumlah pending yang diterapkan bertahap ke Chakra pemain `+0xB2B` melalui getter/setter; pending dikurangi saat diproses dan field dibersihkan setelah selesai. Ini mekanisme perubahan Chakra bertahap, bukan bukti bahwa field itu khusus biaya barrier. Penulis `+0xB30/+0xB38` dan identitas aksi tetap belum ditemukan.
- Jalur di sekitar `0x8011C0D0` mempunyai cabang yang membalik tanda field nilai pemain dan menjepit nilai negatif terendah ke `-9999`, lalu memanggil setter Chakra. Pemicu dan identitas aturan belum dipastikan, sehingga belum diberi label sebagai efek kartu atau kondisi kekalahan.
- Jalur target kemenangan diperiksa lagi di `0x80111200–0x80111280`: getter kondisi menghasilkan bitmask; jika `bit 0x200` aktif, kode memanggil getter target `0x80012A70`, membaca nilai Chakra pemain dari field awal record pemain pada indeks yang dipilih, dan membandingkannya dengan target. `slt(current,target)` membuat jalur non-menang ketika `current < target`; ketika `current >= target`, kode menulis indeks pemain ke field pemenang dan mengubah state hasil. Confidence tinggi untuk arti perbandingan di dalam disassembly, tetapi identitas base modul tetap hasil pemetaan statis sementara.
- Tidak ada uji runtime dijalankan. Tidak ditemukan cukup bukti untuk mengklaim 60 Chakra sebagai harga semua barrier atau 150 Chakra sebagai harga semua upgrade. Prioritas berikutnya: telusuri penulis `+0xB44`, pemanggil event `ESTATE`/`LVUP_ESTATE`, pemeriksaan saldo, dan penulisan data petak untuk menghubungkan angka UI ke rumus/parameter.


## Keputusan emulator-first dan pemeriksaan environment — 2026-10-15

- Menetapkan penggunaan emulator/debugger sebagai jalur riset utama kedua setelah analisis statis. Sasaran: amati perubahan Chakra, field tile, event/state, damage, kepemilikan, dan kondisi pemenang secara langsung, lalu cocokkan dengan call chain.
- PCSX-Redux dipilih sebagai opsi utama karena ada dokumentasi resmi untuk debugger CPU, breakpoint memori, GDB server/watchpoints, command line load image, dan Lua breakpoint. Mednafen adalah alternatif dengan debugger PSX dasar serta breakpoint baca/tulis.
- Sumber rujukan: https://github.com/grumpycoders/pcsx-redux ; https://pcsx-redux.consoledev.net/Debugging/introduction/ ; https://pcsx-redux.consoledev.net/Debugging/gdb-server/ ; https://pcsx-redux.consoledev.net/cli_flags/ ; https://mednafen.github.io/documentation/debugger.html .
- File ROM diambil dari Library, bukan upload ulang laptop; SHA-256 diverifikasi ulang dan cocok: `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`. CUE eksperimen mengidentifikasi satu track MODE2/2352 sesuai mode byte sektor pertama. ROM asli tidak diubah.
- Kendala sesi 2026-10-15: tidak ada executable PS1 emulator yang ditemukan pada path runtime; DNS jaringan container gagal sehingga binary tidak dapat dipasang di sesi ini. Oleh sebab itu tidak ada game boot atau eksperimen runtime yang berhasil dilakukan. Catatan ini mencegah klaim palsu bahwa pengujian sudah berjalan.
- Protokol dan daftar eksperimen baru: [docs/EMULATOR_WORKFLOW.md](docs/EMULATOR_WORKFLOW.md), [docs/RUNTIME_TEST_PLAN.md](docs/RUNTIME_TEST_PLAN.md). Fokus uji awal: breakpoint executable utama di setter/getter Chakra; kemudian telusuri cost/ESTATE, LVUP_ESTATE, income, battle, dan target kemenangan setelah base overlay dikonfirmasi.


## Pemasangan PCSX-Redux dan uji launcher — 2026-10-15

- PCSX-Redux dipaketkan ke Naruto repo melalui workflow `.github/workflows/publish-pcsx-redux.yml` sebagai Release asset, bukan Git object. Release: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15. Ukuran asset 65.747.557 byte; SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`, cocok dengan digest yang diterbitkan package source.
- GitHub Actions run 38692549397 sukses: unduh, validasi hash dan size, best-effort launch smoke test via Xvfb, workflow artifact (retention 90 hari) dan release assets terunggah.
- AppImage dijalankan di environment melalui Xvfb. GUI memang muncul dan teridentifikasi game serial SLPS03553 pada daftar/halaman emulator, tetapi memunculkan dialog “No BIOS loaded, emulation halted”. Tidak ada boot game, tidak ada input gameplay atau runtime game state yang diamati.
- Untuk tahap berikutnya, workflow `.github/workflows/build-openbios.yml` membangun OpenBIOS open-source dari repository upstream PCSX-Redux pinned full source commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`. Workflow awal gagal karena ref commit singkat tidak diterima checkout action; pinned source diperbaiki menjadi full SHA. Run perbaikan #38693323975 harus diverifikasi. OpenBIOS adalah BIOS replacement open-source, bukan Sony retail BIOS.
- ROM didapat dari Library dengan SHA-256 yang cocok, tanpa meminta upload ulang dari laptop. Binary emulator tetap sebagai Release asset terpisah untuk menjaga Git history kecil.


## Uji PCSX-Redux dengan OpenBIOS — 2026-10-15

- OpenBIOS berhasil dikompilasi pada GitHub Actions run `38693358323` dari source PCSX-Redux pinned commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`; workflow merilis asset `openbios.bin`, `openbios.elf`, dan checksum/source provenance.
- Varian default `openbios.bin` berukuran 524.288 byte, SHA-256 `713ea2aed58606282b3ff5e91d77f8c5892ea36f5adcd279d2c7dd26604a625d`. Varian ELF debug SHA-256 `d0d4cc73c9546e1e6af86d38ec894f5a6c81090ccdf97b1a3a39885c56af7bfc`. Keduanya cocok dengan `OPENBIOS-SHA256SUMS` pada artifact yang diunduh dan diverifikasi.
- Launch PCSX-Redux menggunakan `-bios openbios.bin -interpreter -debugger -iso game.cue -run` tidak lagi menampilkan “No BIOS loaded”, tetapi frame yang terekam menunjukkan bentuk geometris besar/gelap dan tidak memberi bukti yang cukup bahwa game mencapai menu/title. Jangan tandai boot game berhasil.
- Workflow run `38693918169` sedang menyiapkan dua variant OpenBIOS: normal shell/menu dan `BOOT_MODE=fast` agar CD boot dicoba langsung. Setelah selesai, ambil asset via release atau GitHub Actions artifact, validasi checksum, lalu ulangi tes boot.
- AppImage emulator tetap sebagai Release asset terpisah dengan hash `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`. Repo tidak menyimpan ROM atau BIOS retail.


## OpenBIOS fast-CD boot attempt — 2026-10-15

- Build workflow [#38693918169](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693918169) sukses membuat shell/menu dan fast boot variants. `openbios.bin` adalah `BOOT_MODE=fast`, yang melewati shell dan mencoba boot disc.
- Hash fast boot `openbios.bin`: `25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d`; ELF: `2c8d36e2179841935a1d1331777380502cdb22528d086c99c6388cdcfa54b8aa`. Checksum dari artifact cocok untuk kedua berkas fastboot; release berisi juga varian shell/menu.
- Pengujian lokal dengan AppImage, fastboot OpenBIOS, interpreter/debugger dan CUE disc dilakukan sekitar 12 detik. BIOS-missing dialog tidak muncul, tetapi layar tetap hitam; tidak ada title atau menu yang bisa dipastikan. Ini **belum merupakan boot game yang terverifikasi**.
- Next: periksa CUE/raw-sector layout dan log/PC state; uji CD-ROM boot dengan debug step atau media header yang dikenal sebagai kontrol. Jangan unggah ROM ke repo, jangan meminta pengguna mengirim ulang ROM, dan jangan klaim rule gameplay runtime sampai ada bukti langsung.

## Diagnostik runtime lanjutan: sektor, init kartu memori, dan pad — 2026-10-16

### Pembacaan payload EXE
- Boot CD normal berhasil membaca file konfigurasi, tetapi `loadExe` tersangkut saat membaca payload utama `SLPS_035.53`. Payload sepanjang `0x5D800` byte = 382.976 byte = 187 sektor.
- Percobaan loop 32 sektor dan 8 sektor tidak menyelesaikan masalah. Varian 8 sektor hanya menghasilkan `[CHUNK8] before idx=0 ... bytes=16384` tanpa `after`, sehingga permintaan 16 KB tidak selesai dalam jendela pengamatan.
- Varian diagnostik satu sektor dibangun/diterbitkan dalam [Actions #38697240018](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38697240018). Runtime menunjukkan read 2.048 byte mulai berjalan dan ada progres setidaknya sampai sekitar sektor kesembilan dalam pengamatan singkat, tetapi belum ada bukti full payload read atau entry game pada jalur disc normal.

### Jalur manual/injeksi EXE
- Injeksi payload ke alamat yang ditetapkan header membuat debugger mencapai `EXEC:PC0(80011448)`, `Execute !`, dan `CD_init`; layar tetap hitam. Pastikan `flushCache` dan urutan init CD-ROM benar sebelum mengulang.
- Breakpoint berikutnya menunjukkan startup menunggu dalam inisialisasi kartu memori (`buInit`) karena status kartu tidak berubah. Bypass eksperimental dapat melewati penantian, tetapi belum menghasilkan layar title/menu; jangan menyebutnya boot berhasil.

### Petunjuk protokol kontroler
- Log berulang menunjukkan perintah pad `0x43` (Set Config Mode). Source PCSX-Redux upstream mengidentifikasi command ini di jalur DualShock/analog; bila tipe controller emulator Digital, kode log menampilkan `Unknown command for pad: 43`. Sumber: https://github.com/grumpycoders/pcsx-redux/blob/db9bc8af44e3c77424127b573c17f9583ee2ab95/src/core/pad.cc.
- Hipotesis selanjutnya: ganti Port 1 ke Analog/DualShock dan ulangi boot sebelum melakukan patch game. Belum ada hasil uji setelah perubahan tipe pad, jadi kausalitas belum terbukti.

### Build alternatif yang diunggah pengguna
- File `PCSX-Redux-9c6f98a0-linux-x86_64.zip`, ukuran 90.912.361 byte, disediakan pengguna pada 2026-10-16. Lingkungan eksekusi shell/file gagal saat inspeksi, sehingga isi paket, hash dan kelayakan menjalankan ROM belum diverifikasi. Lakukan verifikasi terlebih dahulu; jangan menaruh file biner besar ke Git history atau release tanpa alasan yang teruji.

### Syarat bukti
- Status sekarang: *executable mulai berjalan dalam jalur manual*, bukan game terkonfirmasi boot. Bukti yang dibutuhkan: log entry yang valid, title/menu yang dikenali, dan input responsif. Sesudah itu baru validasi aturan gameplay dengan state awal terkontrol.


## Percobaan setelah ZIP emulator tersimpan di Library — 2026-10-16

- Melalui Files berhasil mematerialisasi ZIP emulator (90.912.361 byte), ROM sumber (325.989.552 byte), dan CUE (113 byte) ke `/mnt/data/naruto-runtime/`.
- Pemeriksaan lokal gagal sebelum program dijalankan: `container.exec` memberikan `ClientError` untuk listing/file checks dan bahkan `echo runtime-check`; Python di lingkungan analisis dan jalur Python alternatif juga gagal dengan `ClientError`.
- Akibatnya, belum ada daftar isi ZIP, hash ZIP, hasil ekstraksi, versi PCSX-Redux, log run, atau bukti boot baru. Jangan mengartikan kegagalan tool sebagai kerusakan ZIP atau kegagalan emulator. Tidak ada tes runtime baru yang berhasil dilakukan.
- Tindakan saat runtime pulih: verifikasi integritas dan isi ZIP, ekstrak binary ke direktori sementara, cek versi/dependensi, lalu ulangi boot ROM dengan OpenBIOS dan Port 1 Analog/DualShock sebagai hipotesis terpisah. Sukses harus dibuktikan dengan layar title/menu Naruto dan respons input.


## Refinement of controller `0x43` diagnostic hypothesis — 2026-10-16

The exact upstream PCSX-Redux source commit used for the research-kit AppImage was inspected: [`src/core/pad.cc` at `0c3572c3db75f97542001e453ae80ba8c3f8acba`](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/pad.cc).

- `PadType` defines `Digital = 0` and `Analog = 1`. The serialized setting is named `DeviceType`, with `Digital` as its default.
- When the first received command byte is not the normal read command `0x42`, the pad dispatches the DualShock command handler only when `m_type == PadType::Analog`. Otherwise it logs `Unknown command for pad: %02X`. Thus the existing `Unknown command for pad: 43` log is consistent with Port 1 being configured as a Digital controller.
- Important distinction: the Lua method `setAnalogMode(bool)` writes `m_analogMode`; it does **not** change `m_type` or the serialized `DeviceType` controller type. Calling that Lua method alone is not a valid test of the current hypothesis.
- The GUI's `Controller Type` selector updates `SettingDeviceType` and resets/remaps the pad. The next controlled experiment should set Port 1 `Controller Type` to `Analog` through **Configuration → Controls**, confirm that the pad is connected, then repeat the same CD-boot attempt with all other variables unchanged.
- Compare logs before and after. If the `Unknown command for pad: 43` messages disappear, record that protocol-level effect; if the game still hangs or remains black, the controller mismatch was not a sufficient explanation for the boot failure. Do not infer game boot from that log change alone.

Evidence class: static inspection of the emulator source. **This is not yet a runtime result**: this session could not run the emulator because local execution/file tools returned `ClientError`. The contents and hash of the user-provided alternate ZIP remain unverified.

## OpenBIOS source-level CD-read stall hypothesis — 2026-10-16

### Source trace

Pinned source chain:
- PCSX-Redux AppImage root commit: https://github.com/grumpycoders/pcsx-redux/commit/0c3572c3db75f97542001e453ae80ba8c3f8acba, dated 2026-10-01.
- Its src/mips submodule points to OpenBIOS/Nugget commit https://github.com/pcsx-redux/nugget/commit/d93840921b5ad7ed515e95b0e414f1b1e2038b1a.

Relevant source:
- openbios/kernel/psxexe.c: loadExe() reads the 2,048-byte header, then calls syscall_read(fd, text_addr, text_size) once; it does not check the result count before closing and flushing cache.
- openbios/cdrom/filesystem.c: dev_cd_read() rejects a size or offset not aligned to 0x800 bytes and converts the request into 2,048-byte sectors before calling cdromBlockReading().
- openbios/cdrom/helpers.c: cdromBlockReading() polls seek/read startup with bounded cycle counters, but after starting a read it waits for the DNE completion event while checking error/end events; that final wait has no overall timeout. If completion is never delivered, it may wait indefinitely.

The known executable payload is 0x5D800 = 382,976 bytes = 187 sectors; its request size and file offset satisfy the 0x800 alignment guard. The normal-path stall during payload loading is consistent with a CD-ROM read/event completion issue because the log previously showed SYSTEM.CNF read but not EXEC:PC0(80011448). This remains a root-cause hypothesis until a reproducible runtime trace identifies the exact event/state.

### Controller configuration refined

PCSX-Redux source declares PadType::Digital=0 and PadType::Analog=1 and serializes the emulated console pad protocol to DeviceType (default Digital). Upstream tests/core/pad-config.cc confirms DeviceType: 1 means Analog; PadType: 2 is the keyboard host-input source. These settings are distinct. Toggling the keyboard Analog mode binding or Lua setAnalogMode(true) is not equivalent to setting DeviceType.

- Source used by release: https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/pad.cc
- Upstream config fixture: https://github.com/grumpycoders/pcsx-redux/blob/e7ced7b681296ace22f7847f7bb3c9a206315571/tests/core/pad-config.cc

### Emulator package comparison

The user-provided filename PCSX-Redux-9c6f98a0-linux-x86_64.zip maps by its prefix to upstream root commit https://github.com/grumpycoders/pcsx-redux/commit/9c6f98a0ed0581635f9123147e382c248e0f5ddc, a merge dated 2026-09-28. The research AppImage is pinned to a later root commit dated 2026-10-01. Since ZIP contents could not be inspected in this session, do not claim the uploaded archive actually contains that exact build; the filename is evidence only.

### Next controlled runtime test

1. When shell runtime is available, inspect the ZIP without executing it: unzip -t, list files, SHA-256, architecture and dependencies. Prefer the pinned research AppImage if the ZIP offers no newer/testable functionality.
2. Run a clean isolated test with explicit paths: -bios openbios-chunked.bin -iso naruto-shinobi-jintori.cue -run -interpreter -debugger -stdout -lua_stdout -logfile boot-analog.log.
3. Set Port 1 protocol to Analog (DeviceType: 1), host input to keyboard (PadType: 2), and Connected=true. Compare Unknown command for pad: 43 logs; independently verify the title/menu and input response.
4. The executable payload is 187 sectors. Use a longer observation window and log every per-sector read. Determine whether progress completes, stops at a reproducible sector, or waits on a specific CD event. Early progress is not a completed read.
5. Only start gameplay tests after the title/menu is visible and controls respond. No new runtime test occurred in this session because shell and Python tools returned ClientError; this is an environment blocker, not proof that the ZIP is corrupt or that the game cannot run.


## PCSX-Redux ZIP extraction record — 2026-10-16

### Archive validation and extraction

- Materialized the user Library file `PCSX-Redux-9c6f98a0-linux-x86_64.zip` (90,912,361 bytes) to the working container.
- Source ZIP SHA-256: `7e4c9378524ebfa35068944ba4aa9e3ebf7462678bcae33b3e7ae7c57dd99849`.
- `unzip -t` passed with no errors; archive contained exactly one entry: `PCSX-Redux-HEAD-x86_64.AppImage`, 91,474,424 bytes.
- Extracted AppImage SHA-256: `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`. A second materialization from Library compared byte-identical with the extracted local file.
- Embedded `usr/share/pcsx-redux/resources/version.json`: version `9c6f98a0`, build ID 335, changeset `9c6f98a0ed0581635f9123147e382c248e0f5ddc`, build timestamp 2026-09-28 19:56:29 UTC, channel `dev`.
- The extracted AppImage runtime responded to `--appimage-version`, and the embedded squashfs filesystem could be extracted without FUSE. Running the inner emulator failed due requirements `GLIBC_2.42` and `GLIBC_2.43`; this host provides glibc 2.41. Direct AppImage mounting also failed because no suitable `fusermount`/FUSE device is available.
- The source ZIP was replaced in Library by the AppImage output to avoid storing two nearly identical large files at Library quota. The source hash is recorded here. The Library item retains stale ZIP MIME metadata despite the new AppImage bytes.
- Persistent Library manifest: `/Naruto Research Files/PCSX-Redux-EXTRACTION-MANIFEST.md`.
- New Git documentation records details in `docs/PCSX_REDUX_PACKAGE.md`. The actual 91 MB binary was not added to Git history because the current GitHub connector has no binary Release-asset upload action; a distinct 65,747,557-byte AppImage already exists on the research Release (SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`).
- This work verifies the ZIP and extracted AppImage only. It is **not** a runtime verification of Naruto boot, controls, Story Mode, or the ROM's validity.


## Preferred build for GLIBC 2.41 host — 2026-10-16

### Candidate and compatibility evidence

The best candidate located for the glibc 2.41 research host is the x86_64 `AnyLinux` AppImage built from source changeset `0c3572c3db75f97542001e453ae80ba8c3f8acba` on 2026-10-01. It is attached to the research release and the public packager's release. Size 65,747,557 bytes; SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`.

Sources:
- [Packager README](https://github.com/pkgforge-dev/PCSX-Redux-AppImage-Enhanced): states that AnyLinux AppImage bundles dependencies for old/musl Linux distributions and does not require FUSE.
- [x86_64 GitHub Actions run](https://github.com/pkgforge-dev/PCSX-Redux-AppImage-Enhanced/actions/runs/36872881656), 2026-10-01: successful; the log explicitly says `quick-sharun --simple-test` returned “Test went OK.” The packager embeds cross-libc-dlopen and uruntime.
- The repo's earlier smoke-test notes reported GUI launch under Xvfb with a “no BIOS configured” message. This was not a game boot test.

This is a stronger candidate than the Library's `9c6f98a0` AppImage whose inner binary needs GLIBC_2.42/2.43. However, generic smoke tests and portable packaging do not establish game compatibility or stability. In this turn, container.exec and Python returned ServerError even for basic sanity commands, so no fresh test against the Naruto BIN/CUE was performed. Do not claim title/menu, input, stable gameplay, or Story Mode completion.

Next test when runtime access recovers: obtain the exact candidate by release, verify its SHA; use OpenBIOS chunked with CUE, a clean profile, logs, Port 1 `DeviceType: 1` plus keyboard `PadType: 2`, and connected=true. Confirm title/menu and responsive input, then examine the 187-sector EXE read, repeat boot tests, and only afterwards begin Story Mode.


## Current Library package — AnyLinux artifact ZIP (2026-10-16)

The candidate AnyLinux artifact ZIP was downloaded from the packager's GitHub Actions artifact ID 11170447493 and saved in Library as `/Naruto Research Files/PCSX-Redux-0c3572c3d-anylinux-x86_64-artifact.zip`. Actions-reported ZIP digest: `f6c27070b565cbc0554f1093c1374a16aee2b8635c72ef7b141f9ff7bd857ed0`; reported size 65,673,524 bytes. Its standalone AppImage SHA-256 is known from Release metadata: `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`. This is the preferred candidate for glibc 2.41. The previous 91 MB `9c6f98a0` AppImage and its stale Library manifest were replaced/removed; their hashes remain recorded in `docs/PCSX_REDUX_PACKAGE.md`.

The Actions log confirms a generic `quick-sharun --simple-test` passed. That does not test the ROM. No full Naruto boot, input, runtime stability, or Story Mode result is available. Attempts to run simple local commands now return ServerError, so do not claim an end-to-end test was performed.


## Controlled Analog-port boot probe configured — 2026-10-17

### What changed

- Runner workflow commit: [6bd261a0599f192579f8c091ddcb6d28a4042ec7](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/6bd261a0599f192579f8c091ddcb6d28a4042ec7).
- The workflow now passes a Lua setup to each emulator build before execution:

  ```lua
  PCSX.settings.pads[1].DeviceType = 'Analog'
  PCSX.settings.pads[1].Connected = true
  PCSX.SIO0.slots[1].pads[1].map()
  print("PAD_SETUP=port1 analog device connected and remapped")
  ```

- This matches the upstream PCSX-Redux test fixture at [tests/pcsxrunner/rumble.cc](https://github.com/grumpycoders/pcsx-redux/blob/6b9df482d7b77b9ae218d9c48c1ce1a43c265206/tests/pcsxrunner/rumble.cc). Its comment says safe mode starts Port 1 digital and that the controller type is cached at map() time.
- The A/B workflow continues to use the exact same verified ROM SHA-256 `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`, the same temporary normalized CUE, OpenBIOS, interpreter and 90-second limit for both the AnyLinux and upstream HEAD builds. It now includes the Lua setup marker in the selected logs.

### How to interpret the pending log

- A visible `PAD_SETUP=port1 analog device connected and remapped` marker is needed to confirm the Lua setup ran.
- Compare the presence of `Unknown command for pad: 43` against the baseline from Actions run [#38971848277](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38971848277), where both builds emitted the warning.
- Even if the warning disappears, it proves only that the emulator now accepts the configuration command. It does **not** prove the title/menu is rendered or that input works in the game.
- The resulting run log has not yet been captured into this research log. Do not infer success merely from the workflow commit or a passing CI job.

### Next diagnostic gate

First retrieve the run output and confirm the Lua marker and `0x43` result. If the warning is gone but the frame remains black, treat controller configuration as a solved protocol mismatch but **not** a sufficient explanation for the boot/rendering failure. Then run a separate GUI-under-Xvfb test with the same ROM and Analog-port setup, capture the emulator window locally on the ephemeral runner, and report only derived pixel/screen metrics (do not upload ROM, BIOS, EXE, save-state, RAM dump, or game screenshots to the repository). Confirm title/menu recognition and input response before starting gameplay-rule tests.


## Workflow YAML correction — 2026-10-17

- The initial Analog-port workflow edit [6bd261a](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/6bd261a0599f192579f8c091ddcb6d28a4042ec7) accidentally left the Lua heredoc body without YAML block indentation. Do not treat that revision as a valid completed test.
- The indentation was corrected in final workflow commit [0439c1b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/0439c1bbf51d3c1be234150d6bee80c5b812ff1e). The current file was re-fetched and visually checked: heredoc contents and its closing LUA delimiter are now indented at the YAML run-block level, which YAML removes before the shell executes the script.
- No runtime claim is made from these edits. The next evidence must still come from logs of a run using the corrected commit, including the PAD_SETUP marker and presence/absence of the pad 0x43 warning.


## Runtime result: Port 1 Analog probe — 2026-10-17

Runner test [#38973267415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973267415), job `boot-private-rom`, completed successfully using corrected workflow commit `0439c1bbf51d3c1be234150d6bee80c5b812ff1e`.

- Both AnyLinux and upstream HEAD recorded `PAD_SETUP=port1 analog device connected and remapped`, then loaded OpenBIOS, recognized `SLPS-03553`, completed `[CHUNK1] done chunks=187`, and reached `EXEC:PC0(80011448)` / `Execute !`.
- Unlike the baseline [#38971848277](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38971848277), neither build logged `Unknown command for pad: 43` after the explicit Analog DeviceType + Connected + remap setup. Each build was stopped at the 90-second cap (`PROCESS_EXIT=124`) rather than crashing.
- Conclusion: **confirmed emulator protocol-level effect** — configuring Port 1 as Analog removes the observed `0x43` warning while preserving the executable-entry marker. This does not establish that the game title/menu rendered or that buttons worked in-game. The controller setup warning is now separated from the still-open black-screen/boot/rendering problem.

## GUI rendering probe added — 2026-10-17

- Current runner workflow commit: [85c08d9](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85c08d9ea255dc400c0771361abc95817a0a7ba6). New Actions run [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) was observed queued immediately after commit; its final outcome has not yet been recorded here.
- After the same A/B headless run, the workflow launches AnyLinux in a separate Xvfb GUI session with the same verified ROM, temporary CUE, OpenBIOS and Analog setup. It captures frames at 10s and 20s, prints only image size/mean/stddev/color-count and short Japanese/English OCR output, and logs boot/controller markers. Temporary frames and GUI logs are added to the cleanup list, not uploaded as artifacts.
- GUI result must be checked separately. Non-black pixels or OCR text alone are suggestive only; accept boot only if the frame/text supports Naruto title/menu recognition and a later controlled input probe demonstrates response. If still blank, pursue CD event/init and GPU/rendering causes separately.


## GUI probe result and next trace — 2026-10-17

Runner [Actions #38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) completed successfully, including cleanup. The GUI probe ran AnyLinux with the same verified ROM, temporary normalized CUE, OpenBIOS and Analog Port 1 setup under Xvfb. Two desktop captures at 10s and 20s both reported `1280x800`, `mean=0`, `stddev=0`, `colors=1`, and empty Japanese/English OCR output. This confirms the **captured desktop was entirely black** at both times. The selected GUI log lines included BIOS/Disc/PAD_SETUP but did not include `EXEC:PC0` or `Execute !` within the 35-second GUI observation window; headless tests still reached those markers. No screenshot/artifact was uploaded; frames and logs were deleted by cleanup.

Next experiment: a separate lean workflow [naruto-cpu-trace.yml](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/blob/main/.github/workflows/naruto-cpu-trace.yml) adds a listener for the upstream-tested `GPU::Vsync` event and prints the guest PC/RA/SP every 30 frames, up to 600 frames, using the same private ROM with explicit Analog Port 1. Current run [#38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045) was `in_progress` immediately after commit; obtain its final log and interpret it cautiously. If no VSync callbacks occur, distinguish a stalled emulation/hardware timing path from a CPU loop; if PCs are recorded, map recurring addresses against the executable/temporary overlay assumptions. Do not claim rendered title/menu until independently proven.


## CPU trace attempt 1 — inconclusive — 2026-10-17

The runner job [Actions #38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045) exited with code 139 (segmentation fault) about 12 seconds after starting the headless emulator. It had read the disc label and `SYSTEM.CNF`/`BOOT`, but no `PC_TRACE` sample or executable-entry marker was captured. The instrumented build added a Lua VSync listener that removed itself inside its callback at frame 600, so instrumentation is a confounder. This result does not prove the ROM is invalid or that the game code itself crashed.

A retry was committed as [9419800](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/941980021c16dee3e779f6cc1066dad70b187ad4). It combines the pad setup and tracing code into a single `-exec` block and leaves the VSync listener installed until timeout. Check [Actions #38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739) and require real `PC_TRACE frame=...` rows before interpreting any PC values. If that retry fails, simplify to a counter-only VSync callback before reading registers.


### CPU trace attempt 2: failure was Lua script construction — 2026-10-17

Run [#38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739) exited 134. The exact stdout reason is `[string "cmdline:"]:4: unexpected symbol near '\\'`, followed by `Error loading lua string` and `terminate called without an active exception`. This was caused by shell concatenation `printf '%s\\n%s'` embedding a literal backslash-n between the two Lua chunks instead of a line break. The Lua parser rejected the instrumentation before any PC sample; this is not a ROM failure.

Corrected runner workflow commit: [7b8ce73](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/7b8ce731378e0115f616b7ff78874f5d17375e80). It now constructs pad configuration and VSync tracing in a single heredoc, so source lines are separated normally; the listener stays installed through the timeout. Current retry: [Actions #38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869). Check final job logs for `PAD_SETUP`, `PC_TRACE=listener installed`, and actual `PC_TRACE frame=` lines. If Lua parses but segfaults, strip down to a simple VSync counter callback before any register read.


### CPU trace attempt 3 — VSync samples recorded; process later segfaulted — 2026-10-17

Runner [Actions #38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869) ran the corrected single-heredoc Lua script. It printed `PAD_SETUP` and `PC_TRACE=listener installed`, then produced `PC_TRACE frame=` rows from frame 30 through at least frame 780. Sampled PCs frequently included BIOS addresses `BFC0574C`, `BFC05784`, `BFC03C6C`, plus occasional `000000B0` and `00002998`; RA/SP were also captured. The separate emulator logfile recorded `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, and `Execute !`. The process nevertheless ended with `TRACE_PROCESS_EXIT=139` (segmentation fault) before the 35-second cap and the last output row was incomplete. Because the instrumentation reads `PCSX.getRegisters()` inside the VSync callback, that access/formatting is still a possible confounder; do not infer that the game itself caused the fault or that the PC samples prove a stable gameplay loop.

Next isolating run: [Actions #38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602), workflow commit [85d3e4f](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85d3e4ff31732b7788d67e447ea9df136dcb84f5), uses a counter-only `GPU::Vsync` listener with no CPU-register reads and no self-removal. If it survives until timeout and reports increasing VSync counters, callback plumbing is sound and the register read/format path is implicated. If it still crashes, isolate event registration/callback itself or leave Lua tracing aside and use built-in debugger/logs.


### Counter-only trace result — 2026-10-17

Run [Actions #38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) ended with `TRACE_PROCESS_EXIT=124`, the expected 35-second timeout, not a crash. The counter-only `GPU::Vsync` callback logged increasing counts through `VSYNC_TRACE frame=2040`; the same stdout also recorded `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, and `Execute !`. This demonstrates the event callback itself can remain active stably while the emulator completes headless boot. The prior exit 139 is therefore consistent with the register-read/formatting instrumentation as a confounder, though not yet proven conclusively.

The next test [Actions #38974903834](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974903834), workflow commit [ff0faa5](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/ff0faa598c6e19295229b450c6f9d42c83e590fb), keeps the stable counter and only samples PC every 120 VSync callbacks. It acquires `PCSX.getRegisters()` before event registration (following upstream test style), reads only `regs.pc`, and prints decimal values instead of using `%08X`. If it completes to timeout and emits PC lines without crashing, decode the decimal addresses and compare when they cross from BIOS `0xBFC...` to executable entry space `0x80011448`. If it still exits 139, abandon live register access in the callback and use an upstream-supported CPU execution instrumentation approach.


### Built-in trace API mismatch and emulator correction — 2026-10-17

Workflow run [#38975154606](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975154606) used the pinned AnyLinux package based on upstream PCSX-Redux commit `0c3572c3d`. The process aborted immediately with Lua error `attempt to index field 'CPU' (a nil value)` when accessing `PCSX.CPU.Trace`; it logged no VSync counters. I verified that `src/core/pcsxffi.lua` at ref `0c3572c3d` does not expose `PCSX.CPU.Trace`, although a newer upstream source ref does. This was a build/API mismatch, not a ROM failure.

Corrective runner workflow commit [c994afc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/c994afccfa62efcc01751a7c2b39d89b109d936a) now downloads the user-provided/private-release upstream `PCSX-Redux-HEAD-x86_64.AppImage` and verifies SHA-256 `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`; this build was previously verified to reach `EXEC:PC0` on Ubuntu 26.04. It uses the new `PCSX.CPU.Trace` interface for a bounded frame 1620–1680 capture, then prints only the last 80 records, and deletes all media/trace files during runner cleanup. New test [Actions #38975223698](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975223698) has started; read its final logs before drawing conclusions.


### Packaged emulator also lacks built-in CPU tracing — 2026-10-17 correction

Runner [Actions #38975223698](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975223698) was intended to use the private upstream HEAD AppImage, but it aborted with the same `attempt to index field 'CPU' (a nil value)` message before a VSync sample. The uploaded HEAD binary also predates the `PCSX.CPU.Trace` Lua binding; do not confuse this with a game or ROM failure. Thus **neither packaged build currently available in the research release provides the required trace API**.

Current workflow commit [8304b7d](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8304b7dd56be13673e83e84bb738458eca0cfc2d) instead checks out upstream PCSX-Redux source at pinned commit `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`, verifies `src/core/pcsxffi.lua` exposes `Trace = {`, and builds the native CLI binary using upstream's published builder container. Run [Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) was actively building at the time of this note. Only after build success can the frame-1620-to-1680 bounded built-in instruction trace be interpreted; build failures are infrastructure evidence, not ROM behavior.


### Interpret the first GUI captures against boot timing — 2026-10-17

The 10-second and 20-second all-black frames from GUI run [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) were taken before the headless boot's executable-load point. The stable counter-only test [#38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) reached its VSync count 1620 shortly before the separate log emitted `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, and `Execute !` (the entire 35-second test later reached frame 2040). So the 10s/20s black frames cannot by themselves establish a permanent black-screen failure; the GUI test must observe well beyond the ~27–30s point and ideally capture the emulator window rather than the X root. The earlier 35s GUI window may also be borderline due to UI overhead.

Current source-trace runner [#38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) is still building a pinned upstream source revision so the actual built-in CPU trace API can be tested without live register reads. The result must be checked before analysis proceeds.


### Extended GUI observation launched — 2026-10-17

Runner workflow commit [aea4c20](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aea4c20accfd6d1c5089a226f52a2c4183d2d9a8) extends the GUI phase from 35s to 100s and measures frames at 30s, 60s and 90s, still using temporary local captures which cleanup deletes. Current run [#38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679) has both private asset retrieval steps passing and is in the A/B + GUI step; output has not completed yet. This should distinguish early BIOS-only black captures from a persistent blank frame after the expected executable entry point.

Source build/trace workflow [#38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) is also still in `Build pinned upstream PCSX-Redux with CPU trace support`; no claim is made about build success until the step completes. It uses pinned source commit `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` and the official builder image.


## End-to-end private-ROM run and test-harness corrections — 2026-10-17

Reviewed [Actions #38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679) and [CPU trace Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756).

Confirmed by log: read-only secret was present; normalized release assets were retrieved; ROM byte count and SHA-256 matched; the temporary CUE passed structural validation; OpenBIOS identified disc `SLPS-03553`; `SYSTEM.CNF` selected `SLPS_035.53`; all 187 executable chunks completed; and PCSX-Redux printed `EXEC:PC0(80011448)` / `Execute !`. The Analog Port 1 setup was applied to both compared builds and neither emitted `Unknown command for pad: 43`. Both headless processes reached their 90-second caps; the executable-entry marker is not a title-screen or playable-input result.

The 30/60/90-second GUI probe produced root-window metrics of `mean=0`, `stddev=0`, `colors=1` and no OCR text. Inspecting the workflow exposed a test-harness flaw: it invoked `import -window root`, so those metrics described the Xvfb root background, not necessarily PCSX-Redux's own window. Do not use these frames to diagnose guest rendering. Corrective workflow commit [8829933](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8829933b3b6815dce694ebe6d46cd2a1f0fee9f0) now searches for a visible PCSX-Redux window, captures that window only, reports the window tree if it cannot find one, and does not fall back to the root.

The first source-build trace attempt [#38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) successfully compiled the pinned upstream source but the host executable failed before emulation because `libcapstone.so.5` was missing. No trace callbacks ran. Corrective commit [d965dcc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/d965dcc864c73818e67d6a1e5f9edc19d4a3a17c) adds upstream-documented `libcapstone-dev` and a preflight `ldd` check. Retests [#39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) and [#39000276365](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365) were launched on 2026-10-17; inspect final logs before marking either fix successful.

The runner repo remains free of game media and trace assets: the workflows download private files only to the ephemeral runner, then remove them during cleanup. No gameplay formula was newly confirmed in this run.


## Corrected GUI-window capture — result and interpretation (2026-10-17)

Runner Actions #39000276365 completed successfully after commit 8829933. The capture code found a visible PCSX-Redux window at each 30/60/90-second capture point. This fixes the prior root-window measurement flaw. The actual window frames were still uniformly black by ImageMagick statistics (1280x800, mean 0, standard deviation 0, one color); OCR in Japanese/English returned no text.

Do not conclude that the game framebuffer is black after entry: the GUI probe's own log did not emit [CHUNK1] done chunks=187, EXEC:PC0(80011448), or Execute !. Those markers were seen in the headless A/B probes in the same run. Current result is a GUI-vs-headless discrepancy: headless execution reaches the game executable, while GUI-mode boot remains black and lacks the executable-entry markers within the observation window. Next debug question is why the UI-mode boot path differs (window/context/emulator run state/OpenBIOS progress), not yet which game render routine fails. No frame or private game data was uploaded as an artifact.


## GUI initialization / GLX diagnostic follow-up — 2026-10-17

Because the successful window-targeted run (#39000276365) found a real 1280x800 PCSX-Redux window but no visible pixels, OCR text, GUI PAD_SETUP marker or executable-entry markers, the next test is [Actions #39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307), runner commit [259d587](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/259d587c6b677be7f6466b0ec61edb1940faec49). It adds `glxinfo -B` under the same Xvfb/llvmpipe configuration and emits the last 120 lines of the GUI process stdout and PCSX log, plus an explicit result for whether command-line Lua setup was observed. This can identify whether the GUI process gets past GL initialization and reaches command-line setup. Keep GUI output distinct from headless output; the latter's EXEC marker cannot stand in for the GUI run's own boot progress.


## Cloud AppImage A/B and GUI stall — 2026-10-17

Matched headless comparison: [runner Actions #39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307). Both release AppImages used the same private ROM, normalized temporary CUE, openbios-chunked.bin, interpreter/software GPU, Analog/connected/remapped Port 1, and 90-second cap. Both logged disc SLPS-03553, SYSTEM.CNF boot target, 187 completed executable chunks, EXEC:PC0(80011448) and Execute !. Neither logged Unknown command for pad: 43. The 90-second observation boundary is not evidence of a crash, title-screen render or gameplay.

The same run's GUI path reached GLX diagnostics: Mesa llvmpipe; OpenGL 3.3 core/compatibility. The script captured the actual AnyLinux emulator window at 30/60/90 seconds (not the Xvfb root), but each 1280×800 capture had mean=0, stddev=0 and one color; OCR was empty. GUI stdout/log showed the Lua PAD_SETUP marker and early chunk indices 0/8/16/24/32, but no completed 187-chunk marker or EXEC:PC0/Execute !. Thus GUI is stalled before the known headless executable handoff; lack of an OpenGL context is not supported by the GLX probe, while the exact reason remains open. ALSA dummy-device errors were logged, but no evidence connects them causally to the boot stall.

Release identities from the [private research release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15):
- AnyLinux PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage: 65,747,557 bytes; SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c; source commit 0c3572c3db75f97542001e453ae80ba8c3f8acba.
- Asset named PCSX-Redux-HEAD-x86_64.AppImage: 91,474,424 bytes; SHA-256 5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8; package notes identify source 9c6f98a0ed0581635f9123147e382c248e0f5ddc dated 2026-09-28. “HEAD” is the asset name, not confirmation it is the latest upstream commit. The comparative GUI result remained pending for run #39002136781 at time of note.

Source trace run [#39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) was a host-runtime deployment failure, not a ROM diagnosis: capstone was fixed and the build linked, but host ldd could not locate libavformat.so.62, libavcodec.so.62, libswresample.so.6, libavutil.so.60, and libSDL3.so.0. Workflow commit [16a6faff](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/16a6faff066b913480ad121b497db79df03a9de2) pins the builder image by digest, checks dependencies and launches trace inside that image, and allows 45 minutes for compilation. Rerun [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) was still compiling when this entry was written; trace conclusions remain pending.

No screenshot, ROM, BIOS, save state, memory dump or trace artifact was uploaded. Do not start Story Mode until a recognizable Naruto menu/title and responsive input are independently evidenced.


## Verifikasi GUI A/B terbaru dan perbaikan harness — 2026-10-17

Run GUI A/B [#39002136781](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002136781) berstatus workflow `success`, tetapi **bukan hasil uji GUI yang berhasil**. Langkah headless di job yang sama tetap membuktikan kedua AppImage membaca disc `SLPS-03553`, menuntaskan 187 chunk executable, dan mencatat `EXEC:PC0(80011448)` serta `Execute !`; keduanya tidak lagi mencatat `Unknown command for pad: 43`. Saat masuk bagian GUI, `gui_probe.sh` berhenti untuk kedua build pada `PAD_SETUP: unbound variable` karena variabel shell tidak diekspor. Tidak ada jendela emulator yang ditemukan dan tidak ada frame yang ditangkap. Karena hasil probe tidak dipaksa menjadi kegagalan job, status `success` hanya berarti step berakhir tanpa kegagalan workflow yang terdeteksi; status itu bukan bukti GUI/game berhasil.

Perbaikan minimal sudah didorong ke runner pada commit [aac684d120ec025c4a87197da8d835f90b89f869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aac684d120ec025c4a87197da8d835f90b89f869): ekspor `PAD_SETUP` sebelum skrip probe GUI dipanggil. Rerun ROM privat [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) sudah dipicu dan masih `in_progress` pada pemeriksaan terakhir; hasil frame, OCR, boot-marker GUI, dan cleanup masih harus diperiksa dari log akhirnya.

CPU-trace run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) juga masih `in_progress`. Secret dan pengunduhan/verifikasi file privat telah dilewati; step source-build di container Docker yang dipatok digest masih berjalan, sedangkan capture trace dan cleanup belum dimulai. Belum ada `CPU_TRACE_SIZE` atau `CPU_TRACE_LINE` yang dapat dipakai untuk analisis.

Current upstream PCSX-Redux yang terverifikasi saat cek adalah [41f3196257d0962942b60983201aade951ebbd54](https://github.com/grumpycoders/pcsx-redux/commit/41f3196257d0962942b60983201aade951ebbd54) (2026-10-17 02:53:17 UTC). AppImage berlabel “HEAD” tetap build source 9c6f98a0, bukan upstream HEAD terkini. Tidak ada bukti bahwa judul/menu tampil atau input gameplay merespons; gate RT-001 tetap tertutup dan Story Mode tidak boleh dimulai.


## Hasil GUI A/B setelah fix ekspor PAD_SETUP — 2026-10-17

Run [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) memakai runner commit `aac684d120ec025c4a87197da8d835f90b89f869`. Perbaikan harness terbukti: `PAD_SETUP` berhasil pada GUI AnyLinux dan proses menjalankan pengamatan/capture. Hasil per build:

- **AnyLinux:** GUI log mengenali OpenBIOS, disc `SLPS-03553`, `SLPS_035.53;1`, `SYSTEM.CNF` dan target `BOOT`; marker Analog PAD_SETUP ada. Jendela X11 yang ditemukan (ID `2097204`) ditangkap langsung tiga kali. Frame 30/60/90 masing-masing 1280×800, mean=0, stddev=0, colors=1; OCR jpn+eng kosong. Tidak ada `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, atau `Execute !` pada log GUI. GUI proses exit 124 pada batas observasi 100 detik.
- **AppImage berlabel “HEAD”:** jendela tidak terbentuk. Log menyatakan `Unable to create main window: Couldn't find matching GLX visual`, setelah `SDL failed to create OpenGL 3.2 core context, retrying with any 3.0 profile`. GUI tidak menunjukkan PAD_SETUP atau executable handoff; tidak ada frame. Exit 137 saat proses mencapai penanganan batas observasi/timeout. Bukti yang kuat adalah kegagalan inisialisasi window/GLX pada build ini, bukan crash guest atau kesalahan ROM yang telah dibuktikan.
- **Pembanding headless dalam job yang sama:** kedua build tetap mencapai `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)` dan `Execute !`, dan tidak mencatat warning `Unknown command for pad: 43`. Keduanya berakhir di batas 90 detik (124), bukan bukti crash.

Perbedaan GUI/headless kini lebih spesifik. AnyLinux dapat membuat window dan menjalankan Lua setup tetapi tidak menunjukkan progres yang setara dengan path headless; frame hitam diambil dari window emulator yang ditargetkan, namun karena GUI belum menunjukkan executable handoff, frame itu belum boleh ditafsirkan sebagai layar game setelah entry. Build “HEAD” berhenti lebih awal pada pembuatan window. Langkah lanjut yang masuk akal adalah membandingkan jalur startup GUI dan `-no-ui` pada titik CD/loader/CPU/Lua/OpenGL sebelum mengubah BIOS/ROM atau mendiagnosis renderer guest.

Cleanup step berhasil; tidak ada artefak Actions. Log menyatakan file media privat, profil, frame, log serta ekstraksi AppImage telah dihapus dari workspace runner sementara. Pemeriksaan recursive tree repo publik menemukan hanya workflow, file docs, README dan .gitignore; tidak ditemukan file media game di Git.

## Status source-build CPU trace ketika diperiksa — 2026-10-17

Run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) masih aktif pada step **Build pinned upstream PCSX-Redux with CPU trace support**, yang mulai 04:17:26 UTC setelah download/validasi selesai. Run tetap `in_progress`; capture trace dan cleanup belum mulai. Log archive belum tersedia sementara job aktif (`BlobNotFound` dari endpoint unduh log), jadi durasi build yang panjang belum cukup untuk menyimpulkan penyebab atau hasil. Batas workflow adalah 45 menit; periksa status step/log lagi sebelum deadline dan hindari run duplikat. Belum ada instruction record yang dapat dianalisis pada frame 1620–1680.

## Hasil CPU trace pinned source dan diagnosis boot — 2026-10-17

### Run dan integritas build

[Actions #39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849), workflow commit `16a6faff066b913480ad121b497db79df03a9de2`, job `117306664750`, selesai `success` pada 04:44:27 UTC. Job mulai 04:17:11 UTC. Pengunduhan/validasi privat selesai 04:17:26; source build mulai 04:17:26 dan selesai 04:43:46; capture trace selesai 04:44:21; cleanup selesai 04:44:25. Sumber dipatok pada `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`; image builder dipatok pada `ghcr.io/grumpycoders/pcsx-redux-build@sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`. Log memuat `PCSX_BUILD_RESULT=compiled pinned source with built-in CPU trace API; dependency check and runtime use the same builder image`. Pemeriksaan `ldd` dalam image yang sama sukses; library termasuk `libcapstone.so.5`, FFmpeg, SDL3, dan X11 ter-resolve. Step build memerlukan sekitar 26m20s, bukan hang workflow; tidak perlu mengulang build identik.

### Hasil capture dan makna instruksi

Marker terverifikasi: `PAD_SETUP=port1 analog device connected and remapped`; `VSYNC_TRACE frame=1620`; `CPU_TRACE_WINDOW=enabled frame=1620`; `VSYNC_TRACE frame=1650`; `VSYNC_TRACE frame=1680`; `CPU_TRACE_SIZE=16031631`; `CPU_TRACE_WINDOW=disabled and last 80 records printed`; `TRACE_RESULT=VSync counter callbacks fired.`; `CPU_TRACE_RESULT=Built-in instruction records were printed.`; `TRACE_PROCESS_EXIT=124`. Exit 124 ialah batas capture 35 detik, bukan bukti crash. Tidak ada artefak Actions. Cleanup step sukses dan log menyatakan ROM, CUE, BIOS, emulator, dan log trace temporer dihapus.

Contoh ekor trace (record pra-eksekusi guest):
```
PC 000015a4: lw    $v0, 0x5de4(a3)   # nilai terbaca 00000000
PC 000015a8: nop
PC 000015ac: beq   $v0, $a0, 0x000015c8
PC 000015b0: nop
PC 000015b4: beq   $v0, $a1, 0x000015cc
PC 000015b8: nop
PC 000015bc: addiu $v1, $v1, -1
PC 000015c0: bnez  $v1, 0x000015a4
PC 000015c4: nop
```
Pola ini berulang; nilai register pada disassembly bergerak turun dari sekitar 0x21b ke 0x212 dalam tail terakhir. Ini adalah loop/polling guest yang memiliki penghitung menurun; belum diketahui field/flag apa yang diuji melalui effective address `0x5de4(a3)`. Tidak cukup bukti untuk menyebut infinite loop atau hang permanen.

Provenance kode: source pinned [`psxinterpreter.cc`](https://github.com/grumpycoders/pcsx-redux/blob/6b9df482d7b77b9ae218d9c48c1ce1a43c265206/src/core/psxinterpreter.cc#L1831-L1838) mengambil `const uint32_t pc = m_regs.pc` sebelum memanggil `m_cpuTrace->capture(pc, code)`; [`cputrace.cc`](https://github.com/grumpycoders/pcsx-redux/blob/6b9df482d7b77b9ae218d9c48c1ce1a43c265206/src/core/cputrace.cc#L82-L85) menyimpan nilai itu langsung pada `e.pc`. Maka alamat trace merupakan PC guest mentah, bukan logika PCSX-Redux. Entry dari header EXE utama tetap `0x80011448` dengan load base `0x80010000`; loop pada `0x000015a4–0x000015c4` tidak sama dengan entry tersebut. Physical RAM alias, provenance BIOS/loader, dan alamat overlay belum tervalidasi, sehingga jangan menyebut loop sebagai BIOS atau game code tertentu.

### Perbandingan boot yang penting

Source-build `-no-ui` ini merekam BIOS OpenBIOS, disc `SLPS-03553`, ID `SLPS03553`, executable `SLPS_035.53;1`, serta PAD_SETUP; tetapi log tidak memperlihatkan SYSTEM.CNF/BOOT, chunk selesai, atau EXEC:PC0 selama capture. Ini berbeda dari headless dua AppImage di run GUI A/B #39002846886 yang mencapai 187 chunk dan `EXEC:PC0(80011448)`/ `Execute !`. Karena itu trace ini belum boleh digunakan untuk menyatakan entry game berhasil. Berikutnya bandingkan sumber boot/CD/BIOS pada build source pinned dengan jalur headless AppImage yang sudah mencapai entry, lalu catat guest PC berkala di VSync yang lebih akhir bila dibutuhkan. Jangan ubah ROM atau BIOS tanpa temuan penyebab.

Run GUI A/B #39002846886 terpisah: AnyLinux menjalankan PAD_SETUP dan window sebenarnya tertangkap 30/60/90s, tetapi frame 1280×800 tetap mean=0, stddev=0, satu warna, OCR kosong, tanpa marker handoff executable. AppImage berlabel “HEAD” gagal membuat window dengan `Couldn't find matching GLX visual` serta kegagalan konteks OpenGL 3.2. Hal ini memisahkan diagnosis UI/startup dari guest; belum ada bukti title/menu atau input game responsif.

## Diferensial source terhadap build AnyLinux — 2026-10-17

GitHub compare [PCSX-Redux `0c3572c3` → `6b9df482`](https://github.com/grumpycoders/pcsx-redux/compare/0c3572c3db75f97542001e453ae80ba8c3f8acba...6b9df482d7b77b9ae218d9c48c1ce1a43c265206) memverifikasi head source trace 803 commit di depan source AnyLinux. Diff per-file menonjol: `src/core/cdrom.cc` +1.476/-1.392; `src/core/psxinterpreter.cc` +290/-81; `src/core/pad.cc` +362/-22; `src/core/psxmem.cc` +58/-19; perubahan di `src/core/psxemulator.cc`; dan gitlink `src/mips` berubah dari `d93840921b5ad7ed515e95b0e414f1b1e2038b1a` ke `361f3f6a6f8d8bb98548900d8a231e2d2a2c1dc4`. File interpreter terbaru menerapkan `branchBase()` dan state untuk branch-delay/exception yang tidak ada pada base AnyLinux. Perubahan ini memberi tempat yang konkret untuk inspeksi; compare saja tidak membuktikan mana yang menyebabkan boot berbeda. Kedua workflow masih memakai BIOS diagnostik yang sama dari private release, jadi perubahan gitlink tidak otomatis membuktikan binary BIOS yang dimuat berbeda.

Perintah headless di workflow GUI A/B dan trace source sama-sama mencantumkan `-no-ui`, `-run`, `-interpreter`, `-softgpu`, Lua setup/analog PAD, dan stdout/log. Perbedaan observasi pentingnya: AppImage diberi hingga 90s; source trace hanya 35s. Trace source mencapai VSync frame 2040 dalam proses tersebut, tetapi rekaman instruksi hanya frames 1620–1680 dan ekornya berada pada loop guest PC rendah. Karena itu belum dapat dibedakan apakah versi source punya perubahan boot, tahap BIOS/CD menjadi lebih lambat, atau loop segera keluar setelah capture ditutup.

Lanjutan yang mengisolasi hipotesis: jalankan source pinned dengan batas 90s dan PC guest sampling per 30 VSync, ambil trace window yang lebih akhir (mis. 4500–4560), dan cetak marker `SYSTEM.CNF`/chunk/EXEC terpisah dari `CPU_TRACE_LINE` supaya tidak tersisih oleh `tail -160`. Setelah ada PC kemudian, bandingkan cabang `cdrom.cc` dan perubahan branch/delay-slot interpreter terhadap jalur yang dipetakan; hindari menunjuk commit/file sebagai akar masalah sebelum hasil sebanding tersedia.

## CPU-trace follow-up 90 detik — Actions #39004736399 (2026-10-17)

Sumber bukti utama adalah log final [Actions #39004736399](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39004736399), bukan status workflow semata. Run selesai `success` dari 05:01:31–05:29:40 UTC (12:01:31–12:29:40 WIB). Semua step sukses.

### Build dan integritas input

Source PCSX-Redux dipatok pada `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`; builder image tetap digest `d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`. ROM ukuran 325.989.552 byte dan SHA-256 `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88` terverifikasi; struktur CUE sah setelah referensi FILE sementara dinormalisasi. Build berjalan sekitar 26m20s lalu mengeluarkan `PCSX_BUILD_RESULT`. Pemeriksaan `ldd` pada builder yang sama sukses tanpa `not found`.

### Observasi runtime

Trace berjalan hingga batas observasi 90 detik dan keluar dengan kode 124 yang memang ditetapkan sebagai timeout. PC sampling setiap 30 VSync menghasilkan 158 sampel (frame 30–4740); histogramnya: `0x000015a4` sebanyak 157 sampel, dan `0x00000870` sekali di frame 420. PC kemudian kembali ke `0x000015a4` dan bertahan sampai sampel frame 4740.

Kedua jendela CPU trace selesai:
- Frames 1620–1680: 16.031.631 total records menurut summary, 200 records disampling, 9 PC unik.
- Frames 4500–4560: 16.031.484 total records menurut summary, 200 records disampling, 9 PC unik.
- Pola hot PC konsisten di dua jendela; `0x000015c0` dan `0x000015c4` masing-masing muncul 23 kali pada sampel ringkasan, `0x000015a4` dan alamat tetangga muncul sekitar 22 kali.

Boot marker pada log aktual mengonfirmasi OpenBIOS, disc label `SLPS-03553`, disc ID `SLPS03553`, serta nama EXE `SLPS_035.53;1`. Marker `SYSTEM.CNF`, `BOOT =`, penyelesaian 187 chunk, `EXEC:PC0(80011448)`, dan `Execute !` tidak muncul. Maka sesi tidak membuktikan game executable dicapai.

Workflow baru memfilter CPU trace menjadi agregat PC dan tidak mengeluarkan baris instruksi/operand mentah di hasil runtime. Cleanup step selesai: ROM, CUE, BIOS, emulator dan file trace sementara dihapus; tidak ada artefak Actions. Periksa terpisah isu retensi log lama #39001985849, yang sebelumnya diaudit berisi 80 record instruksi/operand mentah.

### Interpretasi

Bukti mendukung loop PC rendah yang masih muncul hingga akhir observasi, bukan kesimpulan pasti bahwa CPU crash atau hang permanen. Jangan menetapkan fungsi/alamat sebagai OpenBIOS, CD loader, atau kode game tanpa validasi source/mapping. Hipotesis berikutnya perlu menghubungkan alamat loop ke source dan state tunggu yang relevan; jika perlu pengujian baru, tambahkan marker diagnostik yang membedakan progres CD/loader dari polling, tanpa mengeluarkan disassembly mentah.

RT-001 masih **Open / blocked**; title/menu Naruto dan respons input terkontrol belum diverifikasi.

## Catatan eksperimen runtime tambahan — 2026-10-17

### Internal screenshot path
Run privat [#39011515345](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011515345) memvalidasi kembali ROM (325.989.552 byte; SHA-256 yang diharapkan), lalu menjalankan AnyLinux dengan OpenBIOS pada jalur `-no-ui`. Marker BIOS/disc dan `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, `Execute !` tercatat. Tetapi `PCSX.GPU.takeScreenShot()` memberi width=0, height=0, bpp=0 pada frame 1500, 1680, 1800; VSync capture tidak mencapai titik selanjutnya dalam batas 110 detik. Konversi gagal karena buffer/dimensi tidak valid, cleanup selesai, dan daftar artefak Actions kosong. Ini kegagalan metode capture, bukan bukti layar game berhasil tampil atau rusak.

### Source-current GUI probe
Workflow privat [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) dibuat untuk membangun source pin PCSX-Redux `1525a93676dbece9fe70f10ff129aeaa14eec30d` yang diverifikasi sebagai `main` pada saat workflow dibuat, lalu menguji ROM sama di Xvfb, menangkap langsung jendela emulator, dan mencatat ringkasan PC. Ini menghindari penggunaan ulang capture API dalam mode no-UI dan membandingkan source-current terhadap AppImage lama. Status ketika catatan dibuat: workflow masih berjalan; hasil perlu diperiksa sebelum kesimpulan. Capture hanya dimaksudkan sebagai private Actions artifact retensi 3 hari; file media dan capture dibersihkan dari runner.

### Log-retention action
Run [#39011611436](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39011611436) berhasil memanggil DELETE API terhadap **hanya** run publik `#39001985849`, yang sebelumnya berisi 80 record instruksi/operand. GET sesudahnya mengembalikan 404; tidak ada run lain yang ditargetkan. Jangan mengulang keluaran instruksi/operand mentah di log publik.

**Kesimpulan saat ini:** tidak ada bukti title/menu Naruto, input dalam game, atau progres Story Mode. RT-001 tetap Open / blocked. Jangan memperlakukan keberhasilan workflow, CD recognition, atau executable-entry handoff sebagai keberhasilan gameplay.

## Uji emulator alternatif tambahan — 2026-10-17

Workflow privat [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) kini menguji rilis DuckStation resmi, dengan AppImage SHA-256 `c5e6f045f6a242082fcafa9f02d56ad895e233b942728788d232ad0c0c765c24`, ROM yang sama dan OpenBIOS `openbios.bin` dari private release. Harness Xvfb mengambil frame jendela dan mengirim Return/Cross lewat pemetaan keyboard sementara, lalu menyimpan capture sebagai artifact privat 3 hari dan menghapus workspace. Status saat catatan ini dibuat: queued; belum ada hasil boot/menu/input yang bisa disimpulkan. Ini uji kandidat, bukan klaim kompatibilitas.



## Eksperimen runtime — audit DuckStation dan perbaikan harness, 2026-10-17

### Run #39012200147: hasil aktual
- ROM lolos pemeriksaan ukuran dan SHA-256; paket DuckStation yang diunduh lolos pemeriksaan SHA-256.
- Tetapi proses emulator keluar dengan kode 127 sebelum membuat window: `/squashfs-root/AppRun: error while loading shared libraries: libOpenGL.so.0: cannot open shared object file`.
- Lima percobaan capture menghasilkan `no DuckStation window found`; harness mencatat `INPUT_SEQUENCE_SKIPPED=no visible window`. Jadi Return/Cross tidak benar-benar dikirim ke game, dan hasil ini tidak menguji apakah DuckStation/OpenBIOS kompatibel dengan ROM.
- Artifact terdaftar (ID `12093451882`) hanya berukuran 293 byte; pemeriksaan ZIP menunjukkan satu file `duckstation.stdout` 183 byte dan nol gambar. Retensi artifact tiga hari, tetapi tidak ada media game yang ditangkap. Cleanup menyatakan ROM, BIOS, emulator, frame dan log pada runner dihapus.

### Koreksi spesifik, bukan pengulangan build identik
- Workflow `.github/workflows/naruto-duckstation-private-probe.yml` diperbaiki pada commit `058aadea1c664712b62a63cf01fcb3e5598ef047`: menambahkan paket runtime `libopengl0 libglx0 libgl1` untuk library GL yang hilang dan mengubah upload glob menjadi `captures/*.png`, sebab capture dinamai `pre-input-20-sec.png`/ `after-return.png`, bukan `frame-*.png`.
- Rerun [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) menjadi eksperimen berikutnya. Keberhasilan berikutnya hanya berarti launcher/probe berjalan; title/menu dan input harus dibuktikan terpisah.

### PCSX-Redux source-current
Run [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih pada langkah build source pin `1525a93676dbece9fe70f10ff129aeaa14eec30d` ketika diperiksa. Hasil capture belum tersedia; tunggu sampai run final dan evaluasi marker boot, frame metric/OCR, respons pad, serta cleanup.

**Kesimpulan saat catatan ini ditulis:** belum ada title/menu Naruto yang terkonfirmasi; RT-001 tetap Open / blocked dan Story Mode belum dijalankan.


## DuckStation retest #39012504017 — dependensi EGL, 2026-10-17

Setelah `libopengl0 libglx0 libgl1` dipasang, rerun [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) tidak lagi gagal di `libOpenGL.so.0`, tetapi keluar 127 pada pesan `libEGL.so.1: cannot open shared object file`. Semua capture mencari window dan gagal; tidak ada gambar/OCR, input keyboard tidak pernah dikirim ke game. Artifact hanya 292 byte dan tidak berisi PNG. Ini tetap kegagalan dependency host, bukan hasil kompatibilitas ROM/BIOS.

Commit `5afd32eca0d32ee191de7f2963f74b53aed89448` menambahkan paket `libegl1` untuk run berikutnya [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027). Run itu masih pada langkah boot/capture saat diperiksa; periksa exit diagnostics dan artifact aktual. Source-current PCSX [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih membangun source. RT-001 tetap Open / blocked.


## DuckStation probe final — GUI wizard tetapi belum masuk BIOS/game, 2026-10-17

Run [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) memperbaiki dependensi EGL dan membuka window sebenarnya (760×498). Artifact privat `12094155047` berisi delapan frame dan stdout; pemeriksaan visual pada `pre-input-20-sec.png`, `after-return.png`, dan `after-second-return.png` menunjukkan first-run setup wizard DuckStation. Halaman BIOS menampilkan pesan bahwa DuckStation memerlukan BIOS PS1/PS2, walaupun satu file terdeteksi. Log menyebut BIOS dipetakan dan pencarian Auto BIOS, tetapi tidak ada marker disc, SYSTEM.CNF, load executable atau Naruto. `DUCKSTATION_EXIT=137` muncul saat batas observasi; workflow/cleanup tetap sukses.

Input Return pada jendela ini memajukan wizard. Z/Cross tidak menghasilkan bukti perubahan state game. Maka hasilnya bukan game boot maupun input test. Hipotesis yang paling kuat berdasarkan bukti sekarang adalah OpenBIOS yang tersedia tidak diterima DuckStation sebagai BIOS PS1 yang valid; tidak ada dasar untuk menyimpulkan ROM Naruto tidak kompatibel. Tidak meminta retail BIOS atau secret tambahan. Salinan artifak screenshot lokal telah dibersihkan sesudah pemeriksaan.

**Langkah berikut:** utamakan PCSX-Redux source-current [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708), yang masih pada tahap build ketika diperiksa. RT-001 tetap Open / blocked.


## Hasil source-current dan perbandingan OpenBIOS — 2026-10-17

### PCSX-Redux source-current GUI (#39011842708)
Run selesai dengan workflow `success`, source commit pin `1525a93676dbece9fe70f10ff129aeaa14eec30d` berhasil dibangun dan `ldd` lulus. Lima capture jendela pada 20/40/60/80/95 s seluruhnya hitam uniform (1280×800, mean 0/stddev 0/satu warna); OCR kosong. Log memuat disc label `SLPS-03553`, OpenBIOS, dan PAD_SETUP Analog, tetapi hanya satu guest PC sample pada frame 300, `0x000015a4`. Tidak ada `SYSTEM.CNF`, marker BOOT, seluruh 187 chunk, ataupun `EXEC:PC0`. Exit 124 ialah batas observasi. Artifak #12094116949 berisi lima PNG hitam dan stdout; cleanup sukses.
### AnyLinux: fastboot BIOS vs chunked BIOS (#39013612865)
Dengan emulator/AppImage, ROM/CUE, interpreter/software GPU, Port 1 Analog, dan interval sama:
- Fastboot BIOS (`openbios.bin`, hash `25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d`) membaca `SYSTEM.CNF`, `BOOT`, lalu mencatat `EXEC:PC0(80011448)` dan `Execute !`.
- Chunked BIOS (`openbios-chunked.bin`, hash `7644ab45db8519a3621ef9cb0283f0ced5258287f8105c0e9d7e784fef9362b7`) membaca payload satu sektor per call dan berhenti mencatat progres setelah indeks 40, tanpa entry marker selama window observasi.
- Window selector berdasarkan judul tidak menemukan jendela pada kedua run sehingga tidak ada screenshot; input test dilewati. Artifact #12094102119 berisi stdout dan log, bukan PNG. Maka perbedaan BIOS berpengaruh pada progres loader, tetapi belum ada bukti visual boot.
### Follow-up
Workflow [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) mengulang fastboot saja dengan identifikasi jendela X11 generik dan tree dump, agar jendela tanpa caption yang dikenali tidak menyebabkan kesimpulan keliru. Periksa hasil akhirnya.
**Status:** belum ada title/menu Naruto dan input game nyata; RT-001 tetap Open / blocked.


## Fastboot GUI dengan window discovery generik — 2026-10-17 (#39015133027)

- Fastboot OpenBIOS + AnyLinux kembali mengenali disc `SLPS-03553`, membaca `SYSTEM.CNF`/BOOT dan mencapai `EXEC:PC0(80011448)`/ `Execute !`.
- Perbaikan selector X11 berhasil mendeteksi window ID 543 pada 1280×800. Jadi pengujian sebelumnya yang melaporkan no window terlalu sempit dalam pencarian title; sekarang pengambilan pasti berasal dari window aplikasi, bukan root Xvfb.
- Semua capture (before-input, after Return, after Z/Cross, frame 40/65/90s) mempunyai mean 0/stddev 0/satu warna; OCR kosong. Walaupun input event disampaikan ke app window, hasil visual sama persis hitam, jadi respons input game tidak terbukti.
- Workflow selesai dan cleanup sukses; artifact privat #12094179559 disimpan sementara.

Karena pengambilan register CPU melalui `PCSX.getRegisters()` dalam `GPU::Vsync` callback pernah berhubungan dengan pembekuan/segfault pada eksperimen terdahulu, follow-up [#39015290594](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015290594) mempertahankan fastboot/window detection/input sequence namun menghapus callback pembaca register. Hasilnya perlu dibandingkan sebelum memilih diagnosis GPU/rendering vs guest execution.
RT-001 tetap Open / blocked.


## Audit validitas capture — fastboot window probe #39015133027, 2026-10-17

Audit terhadap log aktual menunjukkan `CAPTURE_WINDOW=before-input id=543 name= width=1280 height=800`. Hex ID root yang muncul pada Xvfb adalah `0x21f` (decimal 543); karena selector generik `xdotool search --onlyvisible --name '.*'` cocok dengan root, capture tersebut adalah root Xvfb, bukan window emulator. Karena itu seluruh klaim metrik hitam/OCR kosong dan respons visual input dari run #39015133027 ditarik kembali sebagai **tidak valid**. Ini perbaikan interpretasi penting; jangan teruskan metrik itu ke diagnosis GPU.

Log boot tetap merupakan bukti sah dan menyebut `SYSTEM.CNF`, BOOT, `EXEC:PC0(80011448)`, `Execute !` pada fastboot BIOS. Run #39015290594 mengulang selector yang sama tanpa pembacaan register; jangan tafsirkan gambar sebelum dipastikan bukan root. Workflow diperbaiki pada commit `83173bb10cfbf905a296f59720c0a63c95bc3a32` agar menghitung ID root dan mengecualikannya. Run yang perlu diperiksa berikutnya: [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649). Kriteria frame sah: `CAPTURE_WINDOW` mengarah ke XID non-root dan dimensi cocok dengan window aplikasi; jika tidak ada non-root window, jangan capture root sebagai gantinya.


## Follow-up selector X11: tree menunjukkan window PCSX nyata (#39015419649), 2026-10-17

Run [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649) mengecualikan root `0x21f`, tetapi tidak menghasilkan capture sebab daftar dari `xdotool search --onlyvisible --name '.*'` hanya memberi root. Root tree yang dicetak saat selector gagal memperlihatkan child `0x200034 "PCSX-Redux"` berukuran 1280×800. Maka aplikasi window ada; cara pengambilan XID-nya yang salah. Jangan menafsirkan ketiadaan PNG pada run ini sebagai ketiadaan window ataupun sebagai layar game hitam.
Run [#39015610296](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015610296) yang baru memakai parsing ID langsung dari root tree dan root exclusion, lalu fokuskan XID sebelum input. Probe tetap fastboot dan tidak membaca register CPU di callback VSync. Boot markers yang sudah terkonfirmasi pada run sebelumnya adalah SYSTEM.CNF/BOOT/EXEC:PC0/Execute!; tampilan title/menu masih belum terverifikasi.


## Fastboot dengan capture aplikasi valid dan input tidak mengubah tampilan (#39015722771)

Run [#39015722771](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015722771) berhasil menangkap jendela PCSX-Redux non-root XID `0x200034` / 2097204, 1280×800 dari `xwininfo -root -tree`. Root `0x21f` dikecualikan. Jadi frame ini valid. Semua lima capture—sebelum input, sesudah Return, sesudah Z/Cross, 40/65/90 detik—mempunyai mean 0, stddev 0, satu warna; OCR kosong. Tidak ada register read dalam callback VSync. Port 1 Analog tersambung; event key dihantarkan ke window, tetapi tidak ada perubahan tampilan/game yang terlihat. Boot marker fastboot tetap mencapai SYSTEM.CNF/BOOT, `EXEC:PC0(80011448)` dan `Execute !`. Artifact privat #12095061025 (retensi sampai 2026-10-20 08:02 UTC) dan cleanup sukses.
Ini membuktikan launcher emulator, GUI window dan entry handoff, namun **bukan title/menu/gameplay**. Selanjutnya run [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) mematikan `-softgpu` dan mencoba renderer OpenGL default di bawah Mesa llvmpipe 3.3. Bandingkan metrik frame, OCR, error renderer, dan boot markers untuk mengisolasi backend GPU.


## Fastboot renderer A/B — default OpenGL vs `-softgpu` (#39015919056)

Run selesai `success`. Dengan satu perubahan backend (hapus `-softgpu`, gunakan backend OpenGL default) dan Mesa llvmpipe, `glxinfo -B` mencatat renderer `llvmpipe (LLVM 21.1.8, 256 bits)`, OpenGL 3.3 Compatibility Profile. Jendela PCSX-Redux yang tertangkap adalah XID 2097204/`0x200034`, non-root, 1280×800. Semua lima frame sah—sebelum input, setelah Return, setelah Z/Cross, 40/65/90s—uniform black (mean 0/stddev 0/satu warna), OCR kosong. Boot log mencapai `SYSTEM.CNF`, BOOT, `EXEC:PC0(80011448)`, `Execute !`; proses mencapai batas observasi 100 detik. Port 1 Analog diatur dan input dihantarkan ke jendela, tetapi tidak ada perubahan visual. Tak ada pembaca register CPU dalam callback VSync; cleanup sukses, artifact privat #12094736241.
Perubahan backend GPU tidak memperbaiki layar. Untuk melanjutkan secara diskriminatif, uji PC setelah entry melalui GDB remote eksternal di waktu terpilih, dengan output hanya snapshot PC/hasil wait-state—jangan keluarkan raw instruction/operand dan jangan mengambil PC dari callback VSync. RT-001 tetap Open / blocked.


## GDB remote PC snapshot follow-up dimulai — 2026-10-17

Setelah #39015722771 (fastboot + softgpu) dan #39015919056 (fastboot + OpenGL default/Mesa llvmpipe 3.3) sama-sama menghasilkan jendela PCSX nyata tetapi frame hitam, run privat [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234) ditambahkan. Perubahan eksperimen berikutnya adalah mengambil snapshot PC lewat GDB remote pada t20/t30/t50/t70/t90, dengan timeout pendek dan output ringkas hanya PC. Tidak membaca register dari callback VSync dan tidak menyimpan raw instruction/operand. Status terakhir: installer GDB masih berjalan; belum ada hasil. Kesimpulan rendering/runtime tetap terbuka sampai snapshot dan capture akhir diperiksa.


## Keputusan emulator dan GDB remote probe final — 2026-10-17

Keputusan operasional: **PCSX-Redux AnyLinux prebuilt + OpenBIOS fastboot** tetap jalur utama. Fastboot mencapai `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, `EXEC:PC0(80011448)`, `Execute !`. Chunked BIOS hanya mencatat pembacaan payload sampai indeks 40 pada run A/B sebelumnya. DuckStation dibuka setelah dependensi GL/EGL diinstal tetapi hanya masuk first-run wizard; OpenBIOS tak diterima sebagai BIOS PS1/PS2 valid. Karena itu DuckStation belum menguji kompatibilitas ROM yang sebenarnya.
Run [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234) selesai: capture sah pada window PCSX non-root `0x200034`/2097204 (1280×800) seluruhnya hitam, OCR kosong, termasuk sesudah Return/Cross. Log fastboot mencapai entry handoff. GDB external did not return a PC sample at t20/t30/t50/t70 (exit 1) and timed out at t90 (exit 124); no successful PC snapshots. Cleanup succeeded, artifact #12095276220 (expires 2026-10-20 08:11 UTC). GDB internal raw output was deleted and not uploaded.
Interpretasi: emulator, ROM, fastboot BIOS dan window GUI aktif; tetapi tak ada bukti title/menu atau game-state visual. Tetap pakai jalur fastboot sebagai utama karena jalur loader-nya paling informatif, tetapi jangan mengklaim runtime/gameplay sudah berhasil. RT-001 tetap Open / blocked.



## Adaptive Story Mode reverse engineering — revision53 controlled card reveal (2026-10-23)

Run [#39877412316](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39877412316) is a controlled two-process CIRCLE-vs-WAIT A/B from the independently restored parent checkpoint SHA-256 `36f58e705db5db5272ea0ed31fad07cff588fe1adf817fe795dc8d56ffe0e69e`. The two Memory Card clones matched SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`; initial F20 frames were pixel-identical (1,024,000 pixels compared). Action branch pressed CIRCLE once with successful press/release readback; control branch had zero button presses. All ten 1280×800 external-X11 captures and both v4 candidate checkpoints passed structural validation. The action branch exposed a card (blue `守` emblem) titled `防御集中` (fokus pertahanan); text `気合いをいれて守る。防御技の、消費チャクラが0になります。` translates to “Bertahan dengan penuh semangat. Biaya Chakra untuk teknik pertahanan menjadi 0.” The no-input branch remained on three face-down cards. **Verified only:** at this checkpoint, one CIRCLE reveals the card detail; no evidence yet shows whether the card is acquired or needs a second confirmation.

Action/revealed-card output candidate: `adaptive-cycle-01-f180.sstate`, 21,163,007 bytes, v4, SHA-256 `bd2c4b7f187b21350e5157a11a7b6ab99cf2124a67be11b669f93c982bc25fae`. This is the next restore-only candidate but must independently restore before being promoted. Control output candidate `adaptive-cycle-02-f180.sstate`, SHA-256 `6c90ef08511bda6f5329e2ac65c6af6a542fe3c0884918a33f0f35125a19b135`, remains unpromoted.

The old classifier mistook the opened card + orange lower instruction panel for generic dialogue. Commit `331e2317cc51e386af51dc2d2d0117d459a42391` adds a localized central-card/art signature and fail-closed `card_selection_detail` / WAIT state; unit test passes. Latest regression run #39878572840 failed one *static assertion* because it expected a literal card-selection guard while the workflow correctly parameterizes state through `AB_EXPECTED_STATE`; this was fixed in test commit `a7f9f5da2a8ad2cb39af27aef48e24bf926fc11c`. Re-run [#39878572840](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39878572840) is active as #39878572840 at dependency installation in the last poll; do not proceed to restore-only revision54 until regression is green and the new classifier is confirmed against all ten authentic revision53 frames.

Next planned operation, only after regression succeeds: revision54 restore-only from source run #39877412316, checkpoint SHA `bd2c4b7f187b21350e5157a11a7b6ab99cf2124a67be11b669f93c982bc25fae`, `REVISION=54`, `RESTORE_TEST=1`, one cycle, all authentic frames expected to be `card_selection_detail` / WAIT. Then, only after revision54 confirms fresh-process restore, run revision55 matched CIRCLE-vs-WAIT A/B with `AB_EXPECTED_STATE=card_selection_detail` to determine whether a second CIRCLE acquires/confirms the card.

Full automatic session chaining and Story Mode completion are not yet implemented/verified. No authentic ending screenshot exists. Keep game images, ROM/BIOS, checkpoints and Memory Cards private/out of Git. Only the research repository is permitted for this Naruto task; START is reserved for actual Story Mode dialogue, never card instructions.


## Revision54 — independent restore of CIRCLE-revealed card state (2026-10-23)

Run [#39878936772](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39878936772) independently restored revision53 action output SHA-256 `bd2c4b7f187b21350e5157a11a7b6ab99cf2124a67be11b669f93c982bc25fae` in a new emulator process. Direct private-artifact audit confirmed `ExecutionFlow::SaveStateLoaded`, five valid external-X11 1280×800 captures, `ADAPTIVE_RESTORE_ONLY_NO_INPUT_ASSERT=PASS press_events=0 suppressed_input_calls=1`, and classifier reports for all five frames as `card_selection_detail` / WAIT (confidence .97). Output checkpoint `adaptive-cycle-01-f180.sstate`: 21,162,165 bytes, `PCSX-Redux SaveState v4`, SHA-256 `219d03ab90b594c27430f91460319c6a4c9a3b05b6463871406ac777873bedf8`. This output remains a candidate until a subsequent independent restore succeeds.

Next run revision55 restore-only from #39878936772 using the output SHA above. After it passes, use revision55's output as the parent for a controlled revision56 two-process A/B with `AB_EXPECTED_STATE=card_selection_detail`, one CIRCLE vs no input. One CIRCLE is verified to reveal the card-details panel; whether a second CIRCLE acquires/accepts it remains UNKNOWN.

## 2026-10-23 — Revision61 barrier target investigation

Revision60 LEFT-vs-WAIT established that the one LEFT input is read back and produces a visible sprite pose/facing difference, although the state classifier stays `barrier_level_selection`. This did not prove a barrier target is selected.

Revision61 [run #39909132189](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39909132189) used the action checkpoint from Revision60 C01: 21,163,471 bytes, SHA-256 `702e2f28c28fe78b4732d1876617d19489b27394c24f98ffd4ea2e8259ec30de`. Initial frame parity passed (F20, 1,024,000 identical pixels) and the action/control Memory Card clones were identical. CIRCLE press and release readbacks passed on C01; C02 had no input. Both checkpoints passed the v4 header/size gate: action SHA-256 `9d3ae8dd94348d3cd45c149cae619d08fcdd7c185eeca8a656a3856beba064cf`, control SHA-256 `70283b676653717788cb4a31d7540a0a369f14f977228e7d4b12cf0791fc44a7`. The F60/F100/F110/F180 images had zero differing pixels and both states remained `barrier_level_selection`. Result: pressing Circle in the checkpoint after LEFT has no visible effect; whether LEFT pose change selects a target remains unverified.

Next: add a narrowly-scoped two-action A/B harness mode. From pristine pre-LEFT checkpoint run #39907655833 (`adaptive-cycle-02-f180.sstate`, SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`), C01 presses LEFT at F30, releases at F38, records F60, then presses CIRCLE at F70 and releases at F78. C02 gets no inputs. The test must prove exactly two press events on C01 and zero on C02, all releases succeed, parent F20 frames match, and checkpoints remain private and structurally valid. Add unit/source regressions before running. This is a short rules/readiness experiment only, not a request to finish Story Mode.


## Revision62 — one-session LEFT then CIRCLE A/B (23 October 2026)

Regression #39939979616 passed all 18 unit/source tests and authentic external-X11 policy checks. Player run [#39940196133](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39940196133) completed with private artifact #12495906030. Source checkpoint from #39907655833 was independently checked at 21,162,799 bytes with v4 header and SHA-256 705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35.

A/B gates passed: identical F20 frames (1,024,000 pixels), identical Memory Card hashes ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5, two action-branch presses/releases exactly at LEFT F30/F38 and CIRCLE F70/F78, and zero control-branch presses. Ten external X11 captures passed size checks. Output checkpoints: C01 21,163,248 bytes SHA-256 cf868811502f65f3cd03b7c860acd9ae30dd705f183e226e530dde7066a82bcc; C02 21,163,035 bytes SHA-256 a7062297e5311a67f607fb693597c4ecf963b97f83dacb911815bce40011f5a3; both passed v4 header/size/SHA validation.

Evidence does not verify barrier selection. Classifier remained barrier_level_selection at every captured phase in both branches. The prompt 「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya) did not change and no target highlight or state transition was visible. LEFT changes pose/screen composition relative to the control, but Circle after that has no added verified effect: C01 F60→F100 differed by 22,741 pixels (MAE 0.74667), close to the no-input C02 idle change of 22,679 pixels (MAE 0.80236); the prompt region itself was pixel-identical. Keep barrier_level_selection policy at WAIT.

Next: verify target focus/selection from visual evidence before permitting confirm inputs; use a fresh validated parent and bounded matched A/B, with unit/source regressions first. No Story Mode completion claim or prerequisite.

## Revision63 — matched UP vs WAIT barrier-navigation probe (23 October 2026)

**Question:** Does one UP press visibly identify/select a barrier in `barrier_level_selection`, or produce only navigation/animation?

### Before run and isolation

Regression run [#39939979616](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39939979616) passed 18 unit/source tests at commit `11ea522ef63e0d90f96ff3aabb8ae3f7ccf5451c`. The consumed Revision63 marker pointed to Revision59 run #39907655833, artifact `naruto-storymode-adaptive-player-private`, checkpoint `adaptive-cycle-02-f180.sstate`, immutable SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`, 21,162,799 bytes. Source header/size/hash validation passed; a read-only staged copy was used. The baseline/action/control Memory Card SHA values were identical: `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.

Player run [#39942178665](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39942178665), commit `91b9bbffb3c1a7c8a51ae944f229a29583c021e3`, finished with conclusion success; private evidence artifact #12496637328 was inspected. C01/C02 each loaded the parent in a fresh emulator process with explicit `ExecutionFlow::SaveStateLoaded`. The F20 images were exactly identical (1,024,000 pixels), and both classifiers returned `barrier_level_selection` with WAIT as the normal policy. C01 emitted only UP at F30, readback `true`, and released at F38, readback `false`. C02 emitted zero button presses. Ten actual external-X11 screenshots (C01/C02 × F20/F60/F100/F110/F180) passed image validation at 1280×800.

### Result

The operational A/B assertions passed:
- `ADAPTIVE_AB_INITIAL_PARITY=PASS`, `ADAPTIVE_AB_INITIAL_STATE=PASS`.
- `ADAPTIVE_AB_SINGLE_INPUT_ISOLATION=PASS action_branch_presses=1 control_branch_presses=0`.
- `ADAPTIVE_AB_TEST=PASS`, with two independent processes, identical Memory Card clones, 10 captures, and validated output checkpoints.
- Checkpoints: C01 `adaptive-cycle-01-f180.sstate`, 21,163,397 bytes, header `PCSX-Redux SaveState v4`, SHA-256 `5557188cfa2ce12a70030b8bd650c181a2172f2934185290eb7352faa9754e40`; C02 `adaptive-cycle-02-f180.sstate`, 21,163,426 bytes, same v4 header, SHA-256 `80782b47cf17e8d5bdc414af468c63eb098916c50235f98c092a676cca53b71e`. Both passed external size/header/SHA validation. The runner's native shutdown codes were 139 for C01 and 124 for C02, but the wrapper accepted each only after session completion markers and external checkpoint validation; the Actions job and assertions concluded successfully.

External screenshot inspection shows a clear UP-vs-WAIT view delta by F60: C01's map/scene composition changes and additional coloured node icons, including “60”, become visible, while the game character remains near the central blue barrier. The Japanese prompt remains `「レベルアップする結界をえらんでください」` (Pilih penghalang yang akan dinaikkan levelnya). No unambiguous focus outline/selected-target marker, accepted-level change, or screen-state transition appears; the classifier stays `barrier_level_selection` at F20/F60/F100/F110/F180.

The exact comparison report has: F60 C01-vs-C02 699,552 differing pixels / mean absolute RGB difference 22.48990; F100 699,578 / 22.42131; F110 699,232 / 22.25882; F180 699,873 / 22.34115. Within C01, F60→F100 has 27,531 differing pixels / MAE 0.97250, compared with idle control C02 F60→F100 of 22,679 / MAE 0.80236. The instruction panel ROI (x=140..685, y=565..715) and footer ROI (x=660..1130, y=685..770) each have exactly zero differing pixels from F60 to F100 in both branches. Interpretation: UP provokes a visible navigation/view response; it does **not** establish that a target was selected. Treat target semantics as UNKNOWN and keep the regular policy at WAIT.

### Next bounded experiment to consider

A useful follow-up is a narrowly allowlisted `UP_THEN_CIRCLE` vs no-input A/B from the same immutable Revision59 parent. It must be implemented first because the existing harness supports `NONE` and the consumed `LEFT_THEN_CIRCLE` protocol only. Add shell/Lua allowlists, state-gated F60 authorization for the second Circle, exact frame/readback/zero-control assertions, and a unit/source regression. Only trigger the player after the regression passes. Circle must never be sent if dialogue or an unrecognized screen is detected. Do not reuse Revision63 outputs as a source unless one has been independently restored and promoted. This remains a small qualification test, not a Story Mode completion attempt.

Revision63 marker is consumed; do not rerun it. Keep ROM, BIOS, Memory Card, raw savestates and gameplay images private/out of Git.


## Revision64 protocol implementation checkpoint — 23 October 2026

**Do not launch Revision64 yet.** Private Revision63 evidence was downloaded and visually audited before making code changes. The ten external-X11 screenshots are authentic 1280×800 captures. C01's F60 view differs substantially from C02, but the prompt 「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya) remains; no target highlight/selection is verified. Keep normal barrier_level_selection policy at WAIT.

Implemented in the only permitted repository:
- Player workflow commit 0073b9be0a541f52173a58dd68a32814fdacb625 adds UP_THEN_CIRCLE to the strict shell/Lua allowlists. Only AB_TEST=1, AB_EXPECTED_STATE=barrier_level_selection, AB_ACTION=UP, AB_SECOND_ACTION=CIRCLE, two cycles, RESTORE_TEST=0, and CONTINUATION_TEST=0 are accepted for this sequence.
- Action branch schedules UP press F30/release F38. The external screenshot at F60 must classify as barrier_level_selection with action WAIT; dialogue, unknown, another state, or an unarmed sequence terminates the emulator safely before Circle. Circle at F70 is allowed only after that gate and is released at F78. Post-run checks require exactly these two press/release pairs, no unexpected action, zero control-branch presses, identical F20 pixels, identical Memory Card clones, two SaveStateLoaded events, ten authentic captures, and structurally/hash-validated v4 output checkpoints.
- Regression test commit 813cc644f9898fd58a09f5678d6619c6f610df8f adds assertions for the new allowlist, F60 fail-closed state gate, timing, release counts, and zero-input control.

The regression workflow is configured to run on pushes touching the test file. Its status/conclusion has **not yet been independently verified** through the GitHub Actions run-inspection capability available in this session. Therefore the consumed marker experiments/.run-storymode-adaptive-player remains Revision63 and unchanged; do not edit it or run a player experiment until a green regression result is confirmed.

Immutable source remains Revision59 run #39907655833 artifact naruto-storymode-adaptive-player-private, checkpoint adaptive-cycle-02-f180.sstate, 21,162,799 bytes, v4, SHA-256 705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35. Revision63 marker remains consumed; never rerun it. ROM, BIOS, Memory Card, savestates, and gameplay screenshots remain private and out of Git. Story Mode completion is not this qualification goal.


### Revision64 final regression hardening — 23 October 2026

A source-level audit caught and fixed two regression-compatibility details before any player run:
- The workflow now sets `sequenceAction=nil` and assigns LEFT/UP only for the two explicitly recognized sequence names. This prevents the ordinary `AB_SEQUENCE=NONE` single-action A/B protocol from being mistakenly treated as an armed two-action sequence in Lua.
- The existing LEFT_THEN_CIRCLE source regression now checks the shared `AB_ACTION` timed assertion used by both sequences, while retaining the exact allowlist tuple and explicit LEFT outcome assertions.

Latest workflow commit: `a7e59dee93de44b7958f317a6239eda048e7951d`. Latest test commit: `123efe8480d50a1589d00dc3dd87e003b310e1bb`. A source-level sweep checked 54 literal `assertIn(..., workflow)` expectations in the test module against the current workflow; all 54 matched. This is only a static consistency check, **not a substitute for the actual regression workflow**. The Actions run conclusion still has not been independently retrieved, and the latest test commit should trigger the regression workflow again.

Keep marker `experiments/.run-storymode-adaptive-player` unchanged at consumed Revision63; do not rerun it and do not launch Revision64 until a green regression run is explicitly verified. All private evidence/source-checkpoint constraints above remain in force.

## Revision64 preflight audit — 23 October 2026

- Latest regression run [#39944753664](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39944753664), workflow run 33, completed **success** on test commit `123efe8480d50a1589d00dc3dd87e003b310e1bb`. The completed job log independently records **19 tests / OK**, `AUTHENTIC_X11_REGRESSION=PASS checked=10`, `AUTHENTIC_CARD_OVERLAY_DIALOGUE_PRIORITY=PASS checked=5`, and `AUTHENTIC_REVEALED_CARD_DETAIL=PASS checked=10`; all job steps passed. Main's workflow and test blob SHAs match the regression checkout (`60b613d2d6c7efde32452b16399814962308e541` and `5b60db1a22646a9b4176169462c193ae243b2a66`), so the result covers the current source files.
- The Revision63 player marker was read before any edit and is consumed; it remains unchanged in this preflight record. No concurrent player run was found in the recent Actions run list.
- Downloaded the source artifact for run [#39907655833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39907655833), private artifact `#12482055310`. Inside it, `adaptive-cycle-02-f180.sstate` was independently rechecked: **21,162,799 bytes**, `PCSX-Redux SaveState v4` header, SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`. This matched checkpoint has not been modified. Authentic private screenshot `C02-F180.png` displays `「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya)`, consistent with the intended `barrier_level_selection` parent.
- Audited the current player workflow's shell and Lua guards. Only the exact `AB_TEST=1`, `AB_EXPECTED_STATE=barrier_level_selection`, `AB_ACTION=UP`, `AB_SEQUENCE=UP_THEN_CIRCLE`, `AB_SECOND_ACTION=CIRCLE`, two-cycle tuple, with restore/continuation flags 0, is accepted. Lua independently validates the same sequence; C01 requires F20 state `barrier_level_selection` plus classifier action `WAIT`, presses UP at F30 and releases at F38, then requires the real F60 observation to remain `barrier_level_selection` / `WAIT` before authorizing Circle at F70/release F78. Any F20/F60 mismatch or unarmed sequence quits before the second input. Shell assertions enforce exactly two C01 press/release pairs, no unexpected C01 presses, zero control presses, equal initial F20 pixels, equal Memory Card clones (expected SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`), two `ExecutionFlow::SaveStateLoaded` events, ten authentic external-X11 1280×800 screenshots, and structural/header/size/SHA validation for both private output checkpoints.
- Regression is green and the Revision64 preflight is technically qualified. This is a **bounded qualification experiment only**, not proof that the player is ready for unattended Story Mode completion. If F60 is not the calibrated submenu with WAIT, do not send Circle. Keep all ROM, BIOS, Memory Card, savestate, and gameplay screenshots private and out of Git.

**Audit conclusion:** the static allowlist/gate test plus the green Actions regression support starting the bounded test, but cannot establish the outcome of UP→Circle. The prior Revision63 UP-vs-WAIT visual difference is not target-selection proof; target semantics remain unknown until this new runtime evidence is inspected.
 
## Revision64 runtime audit — 23 October 2026

Run [#39946344909](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39946344909) failed in the adaptive loop after the private artifact upload succeeded; private artifact #12498880615 is available. This is a harness timeout failure, **not** an F60 safety-gate rejection.

- The immutable Revision59 source was re-verified at SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`. Both fresh emulator processes logged `ExecutionFlow::SaveStateLoaded`; their F20 images were identical across 1,024,000 pixels. Memory Card clones matched SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- C01 classified F20 and F60 as `barrier_level_selection` / `WAIT`; the F60 authorization gate passed. C01 sent exactly UP at F30/released F38 and Circle at F70/released F78, with successful true/false readbacks. The C02 control branch sent zero input through F110.
- C01 reached F180 and its checkpoint passed external validation: `adaptive-cycle-01-f180.sstate`, 21,163,031 bytes, header `PCSX-Redux SaveState v4`, SHA-256 `35cb550a62732cc6ed757e21914b46c1c0f1b2266182e2ea7761a6d401046014`. **Do not promote this checkpoint**: it has not been independently restored.
- The private artifact has only nine authentic 1280×800 external-X11 screenshots: C01 F20/F60/F100/F110/F180 and C02 F20/F60/F100/F110. C02's emulator hit the 60-second wrapper timeout (exit 124) at F110, so C02 F180 and its output checkpoint are missing. The orchestrator reported `ADAPTIVE_ORCHESTRATOR_EARLY_EXIT missing=['C02-F180'] checkpoints=1/2` and the job failed with exit code 92. Full A/B acceptance therefore failed.
- At C01 F60/F100/F180, `「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya)` remained visible. From C01 F60 to F100, the instruction-panel ROI (x=140..685,y=565..715) and footer ROI (x=660..1130,y=685..770) each had zero differing pixels; both corresponding control ROIs were also stable. Whole-screen action/control differences mostly reflect the UP-induced view composition change and are not evidence that a target was selected. **Target/confirmation semantics remain UNKNOWN.**
- Required repair: increase only the per-emulator wrapper timeout from 60 to 90 seconds. Keep the Actions job capped at 20 minutes, preserve all shell/Lua allowlists and the F60 fail-closed gate, and add a source regression that verifies this bounded timeout. Do not launch the next player run until the resulting regression workflow is independently verified green. Revision64 is consumed; never rerun it. Use a fresh Revision65 marker against the same immutable Revision59 source only after regression passes.

Readiness remains **NO-GO**. Story Mode completion has not been proved and is not this qualification test's acceptance criterion. ROM, BIOS, Memory Card, savestates, and screenshots remain private and out of Git.

**Interpretation:** the current evidence does not confirm that Circle selected any target; do not change normal policy from WAIT based on this run.

## Timeout repair regression passed — 23 October 2026

The bounded emulator timeout was raised from 60 to 90 seconds, with the Actions job timeout kept at 20 minutes. The change is guarded by `test_bounded_emulator_timeout_allows_capture_cycle_to_finish` in `tests/test_storymode_adaptive_agent.py`; no gameplay actions, UP_THEN_CIRCLE timing, shell/Lua allowlists, or F60 state gate were changed.

Regression run [#39947302492](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39947302492) completed **success** on test commit `23b03a440363cff80f3b718f5fd07c26b67a2e30`. Its log proves **20 tests / OK**, `AUTHENTIC_X11_REGRESSION=PASS checked=10`, `AUTHENTIC_CARD_OVERLAY_DIALOGUE_PRIORITY=PASS checked=5`, and `AUTHENTIC_REVEALED_CARD_DETAIL=PASS checked=10`; every job step passed.

This regression qualifies a bounded retry. It does not alter Revision64's incomplete result: action branch's verified checkpoint is not promoted; its visual change did not prove target selection; target semantics remain UNKNOWN. Next step is a new Revision65 matched A/B from the immutable Revision59 source. Keep all gameplay assets private/out of Git, and keep readiness NO-GO until the new runtime evidence is examined.

## Revision65 UP_THEN_CIRCLE A/B result — 23 October 2026

Player run [#39947481094](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39947481094) completed **success** at marker commit `76387b12c560310937e3f7c468e571317d5bcbac`; private artifact #12498688466 (`naruto-storymode-adaptive-player-private`) was downloaded and audited. This run used the repaired 90-second per-emulator bound and did not rerun Revision64.

### Runtime and safety gates — PASS

- Immutable source remained Revision59 run #39907655833 / private artifact `naruto-storymode-adaptive-player-private` / `adaptive-cycle-02-f180.sstate`, 21,162,799 bytes, PCSX-Redux SaveState v4, SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`. The runtime staged a read-only copy and logged the same source SHA in both branches.
- Both fresh emulator processes logged `ExecutionFlow::SaveStateLoaded`. Initial F20 images were pixel-identical across 1,024,000 pixels and both classifiers reported `barrier_level_selection` / `WAIT`.
- Memory Card baseline/action/control clones matched exactly at SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- C01 action branch registered exactly UP press at F30 and release at F38 (true/false readbacks passed), then Circle at F70 and release at F78 (true/false readbacks passed). The F60 capture stayed `barrier_level_selection` / `WAIT`, so the Circle authorization gate passed. C02 had zero button presses; both branches produced all five external-X11 screenshots.
- All **10 authentic screenshots** are 1280×800. Both output checkpoints passed external file-size/header/SHA-256 validation:
  - C01 `adaptive-cycle-01-f180.sstate`: 21,163,502 bytes; header `PCSX-Redux SaveState v4`; SHA-256 `ee8c768b81e69cc0096045ed05ab57ea7a1e73cb62c26c16894d1c18e584d14c`.
  - C02 `adaptive-cycle-02-f180.sstate`: 21,163,270 bytes; header `PCSX-Redux SaveState v4`; SHA-256 `8b94ef0047ddf64b36cabc4fe70a210b1787f7946adb4384e5eb1b2126d8a325`.
- The runtime wrapper recovered native emulator exit 124 only after the session-finished marker and output checkpoint validation had succeeded; cycle 2 also logged a `corrupted size vs. prev_size` allocator diagnostic during shutdown. The run's declared checkpoint/capture assertions all passed, but treat that shutdown diagnostic as a residual reliability concern. Neither output is promoted as a source because neither has been independently restored.

### Gameplay interpretation — target remains UNKNOWN

The instruction `「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya)` stays on screen at C01 F20/F60/F100/F110/F180 and throughout the control branch. UP moves the visible composition and reveals a pink marker labelled `60`; however, no reliable selected-target outline, target-state classification, instruction-panel change, or confirmation transition is observed after Circle. The instruction-panel ROI (x=140..685,y=565..715) and footer ROI (x=660..1130,y=685..770) each have zero changed pixels from F60 to F100 in both branches. The action/control full-frame differences at later frames largely reflect the UP-induced view difference, so they are **not** causal proof of target selection. The current evidence verifies input delivery and a view response, but **does not verify that UP selected a barrier or that Circle confirmed one**. Normal policy must remain WAIT for `barrier_level_selection`; do not infer selection from pose or camera movement.

The matched A/B harness now completes all structural and capture requirements after the 90-second bound repair. Readiness nevertheless remains **NO-GO** because the target-selection/confirmation semantics are unresolved. Story Mode completion is still unverified and not a prerequisite for this qualification milestone. Revision65 is consumed; do not rerun its marker. Keep both output checkpoints and all evidence private/out of Git.

**Experiment classification:** harness/gate/instrumentation result = PASS; target-selection outcome = INCONCLUSIVE/UNKNOWN; readiness decision = NO-GO.

## Revision65 visual/control audit — pink `60` remains semantically unknown (23 October 2026)

Reviewed the private artifact from Actions run #39947481094 (artifact #12498688466) rather than relying only on the handoff summary. The action arm has authentic screenshots C01-F20/F60/F100/F110/F180; the matched no-input arm has C02 equivalents. All ten screenshots are 1280x800 and the offline classifier labels every one `barrier_level_selection` / `WAIT`.

Observed visual deltas:
- After UP@F30, C01-F60 shows a large pink hexagonal badge with numeric `60` in ROI x=420..540,y=175..260. It persists in later C01 screenshots. The same ROI in C02 no-input screenshots has no comparable large badge; its candidate saturated-pink RGB ratios stay below 0.01. Both F20 baselines are approximately 0.0021. This establishes a correlated visible change after UP, not what the badge means.
- `「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya)` remains on screen. The footer's `けってい` (konfirmasi/pilih) paired with Circle and `もどる` (kembali) paired with X documents confirm/back semantics. It does not reveal how a barrier target is selected.
- The prompt-panel ROI (x=140..685,y=565..715) and confirm/back footer ROI (x=660..1130,y=685..770) have exactly zero changed pixels from C01-F60 to C01-F100, and likewise in the control. The Circle press/release is confirmed by PCSX-Redux PAD override readback (true/false), but there is no visible confirm transition or unique target highlight. The emulator input API's symbol-to-PAD mapping proves button delivery, not game-level target semantics.
- Revision65 outputs: C01 21,163,502 bytes, v4, SHA-256 `ee8c768b81e69cc0096045ed05ab57ea7a1e73cb62c26c16894d1c18e584d14c`; C02 21,163,270 bytes, v4, SHA-256 `8b94ef0047ddf64b36cabc4fe70a210b1787f7946adb4384e5eb1b2126d8a325`. Both remain unpromoted until independent restore. The runtime emitted `corrupted size vs. prev_size` during cycle-2 shutdown, a residual reliability concern despite accepted wrapper exit and checkpoint validation.

Decision: **target cue UNKNOWN; keep WAIT; no-go for autonomous Story Mode attempts.** Added a synthetic pink-badge WAIT regression, a private authentic-image regression against all ten Revision65 screenshots, and a source-validation gate that blocks future barrier A/B input until the marker includes the explicit verified-cue token. No new gameplay run was started. Private game assets and evidence stay out of Git.

## Regression repair note — 23 October 2026

Regression #39950014349 failed in the unit-test stage: `test_barrier_target_probe_requires_verified_visual_cue_before_download_or_input` expected the literal documented marker syntax `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` in the player workflow. The gate itself correctly compares the marker value to `VERIFIED_BARRIER_TARGET_CUE_V1`; a comment will document the precise marker syntax for auditability. Separately, the newly appended authentic Revision65 artifact step accidentally escaped the Actions interpolation expressions `${{ github.token }}` and `${{ runner.temp }}`. This repair removes the backslashes. No player workflow run was launched; marker Revision65 stays consumed, and the barrier-target gate is still NO-GO.

## Cross-context interpretation of Revision65 pink `60` — number likely barrier value, target role unknown (23 October 2026)

Directly inspected authentic images from private artifacts #12498688466 (Revision65) and #12428777970 (older map UP-vs-WAIT run #39786019434). In the older map screenshot C01-F60, the same pink hexagon marked `60` appears with red directional arrows around the tile; the information panel explicitly reads `結界価値` (Nilai penghalang) 60, alongside `レベル` (Level) 1 and `耐久値` (Daya tahan) 2/2. This verifies, for that map UI context, that `60` labels the barrier value and that a separate arrow surround is visible when a map focus is indicated.

In Revision65, UP changes the view and a visually matching pink hexagon marked `60` appears, but the level-up submenu does not show the same red directional arrow surround or the map data panel. The prompt `「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya)` remains. The footer `けってい` (konfirmasi/pilih) / Circle and `もどる` (kembali) / X remains identical from F60 to F100 after Circle. Thus the numeric glyph is consistent with a barrier-value symbol, while whether that tile is selected/highlighted as the upgrade target remains UNKNOWN. No target-selecting behavior is established.

The final regression output will use `60_matches_known_barrier_value_symbol_from_map_context; submenu_target_selection_role_UNKNOWN` rather than saying the number itself is wholly unexplained. Keep adaptive action WAIT at this submenu, and require independent red-focus-arrow/cursor evidence (or equally discriminating visual marker) before authorizing further target-specific input.

## Regression confirmation — run #39952866478 (23 October 2026)

The wording refinement was validated by Actions run #39952866478 at commit d210e75d17591c1ad03a50d539c3746bc1bd53fe; conclusion success. The run completed all steps: 23 tests, authentic X11 classifier regression (10), card-overlay priority (5), opened card-detail validation (10), and Revision65 private A/B replay. In the Revision65 replay, action-branch pink candidate ratios measured 0.1301 / 0.0948 / 0.0288 / 0.1334 at F60/F100/F110/F180; no-input control stayed 0.0044 / 0.0053 / 0.0011 / 0.0077; both F20 baselines approximately 0.0021. Instruction-panel and confirm/back footer crops changed by exactly zero pixels from F60 to F100 in both arms. Current mainline has only analysis/test/doc/workflow guard updates; no marker change or new gameplay run.


---

## Offline screenshot registration and target-cue discrimination — 23 October 2026

### Provenance and safety

The only repository read/modified is `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. The analysis used existing private Actions artifacts #12498688466 (Revision65, run #39947481094) and #12428777970 (map UP-vs-WAIT, run #39786019434); authentic PNGs were extracted to temporary local storage for inspection and kept out of Git. No ROM, BIOS, Memory Card, savestate, screenshot, or private artifact was committed. The marker `experiments/.run-storymode-adaptive-player` remains Revision65, consumed, unchanged, and without `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1`. No gameplay run or emulator input was launched in this analysis.

The safety/regression-only source commit is `563e34562f4bea0423557755a5c03b4b60077894`. Actions regression [#39973978654](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39973978654) completed with `success`; the final screenshot-validation step passed. Verified measurements are recorded below.



### Regression run #39973978654 — VERIFIED PASS

Workflow run: [#39973978654](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39973978654), source code commit `563e34562f4bea0423557755a5c03b4b60077894`, conclusion `success`, completed 23 October 2026 at 15:00:04 UTC. Job `regression` and every step completed successfully. Log reports **25 tests in 4.542s**; authentic classifier checks passed for 10 X11 screenshots, 5 card-overlay frames, and 10 revealed-card-detail frames, then both private Revision65 and map UP-vs-WAIT artifacts were downloaded and verified.

The new authentic-screen outputs are exact:

- `REV65_BADGE_CENTROID pre_count=142 pre_y=164.25 post_count=2681 post_y=261.71 delta_y=97.46 scene_shift_y=100`
- `FOCUS_ARROW_RING_PIXELS map_UP_around_pink60=811 map_WAIT_around_pink60=62 Revision65_around_badge=66`
- `MAP_FOCUS_ARROW_RING_REGRESSION=PASS known_map_ring_plus_matching_panel=true Revision65_ring_absent=true target_role=UNKNOWN`
- `CAMERA_SHIFT_ESTIMATE revision65_UP=100px revision65_WAIT=0px map_UP=100px map_WAIT=0px`
- `CAMERA_SHIFT_REGRESSION=PASS UP_scene_shift_approx_100px WAIT_scene_shift_approx_0px target_selection_not_inferred=true`
- `REV65_BADGE_SHIFT_FOLLOWS_SCENE=PASS badge_delta_y=97.46px registered_scene_delta_y=100px within_tolerance=true camera_pan_confounds_exposure=true selection_not_proven=true`

This proves the new regression reproduces the competing camera-pan/exposure explanation and distinguishes the known map selection's arrow-ring-plus-panel composite. It still does **not** prove a target is selected in the level-up submenu. Code changed only in the regression workflow/test; the player workflow, marker, and inputs remain untouched. Current readiness remains **NO-GO**, barrier-level-selection policy remains **WAIT**, and Story Mode remains **NOT COMPLETE**.

### Independent terrain registration, with foreground pose excluded

ORB descriptors were matched between authentic F20/F60 pairs, using terrain/background areas and excluding the central character/target region and fixed panel area where applicable. BFMatcher ratio filtering and RANSAC partial-affine fitting yielded:

| Authenticated pair | Matches | Inliers | Translation (x, y) | Scale | Rotation | Median inlier residual |
|---|---:|---:|---:|---:|---:|---:|
| Revision65 UP | 1,971 | 1,854 (94.1%) | (+0.03, +100.30) px | 1.00005 | +0.009° | 0.457 px |
| Revision65 WAIT | 4,596 | 4,586 (99.8%) | (−0.00, −0.00) px | 1.00000 | −0.000° | 0.001 px |
| Map UP | 1,121 | 1,068 (95.3%) | (+0.10, +100.26) px | 0.99994 | +0.010° | 0.426 px |
| Map WAIT | 4,699 | 4,696 (99.9%) | (−0.00, −0.00) px | 1.00000 | +0.000° | 0.000 px |

This independently confirms a near-pure vertical viewport/scene pan of approximately 100 px after UP in both contexts, while WAIT is stable. The registration excludes the central foreground character, so character pose/placement does not drive this terrain estimate. The tree roots, foliage, and building/roof landmarks align under the same transform; scale and rotation are effectively unchanged.

### Pink badge relative to scene and the known focus cue

Using the established RGB pink mask `R>180, G<110, B>100, R-G>75`, the Revision65 partially visible F20 badge ROI contained 142 pixels, with a visible-pixel centroid near (508.27, 164.25). At F60 after UP the fixed exposure ROI contained 2,681 pixels and centroid near (487.23, 261.71); visible-pixel centroid vertical change was +97.46 px versus the registered terrain shift +100.30 px. The matched WAIT control had 0 pink-mask pixels in the post-UP ROI. The count increased because the badge became exposed from behind the fixed HUD; the close vertical agreement makes viewport pan/unocclusion a sufficient competing explanation. Since the baseline is partially occluded and the centroid is computed from visible pixels, this metric is **not** treated as proof that the object is selected or as an exact world-coordinate track.

The already-authenticated map reference discriminates a target cue with multiple simultaneous signals: red directional arrows around the pink-60 tile and a matching information panel. The same threshold, counting red pixels outside the tile body, measured 811 ring pixels around the pink-60 map tile after UP, versus 62 around the pink-60 tile in map WAIT and 66 around the Revision65 submenu badge. Existing panel differential was 16,239 changed pixels in map UP versus 94 in map WAIT; the map-UP panel displays `レベル 1` (Level 1), `結界価値 60` (Nilai penghalang 60), and `耐久値 2/2` (Daya tahan 2/2). WAIT retains `空き地` (tanah kosong), barrier value 140, and no durability. The level-up submenu instead shows `レベルアップする結界をえらんでください` (Pilih penghalang yang akan dinaikkan levelnya), without the distinctive arrow ring or matching tile-information panel. Its instruction and Circle/X footer ROIs are pixel-identical from F60 to F100 in both branches (zero changed pixels).

### Decision and CI regression added

**Conclusion:** terrain/camera pan and HUD unocclusion remain the supported explanation for badge exposure; the pink 60 object is consistent with the known barrier-value symbol from map context, but its role as the selected upgrade target remains **UNKNOWN**. Keep classifier action `WAIT` at `barrier_level_selection`, keep the target-cue token absent, and prohibit all new gameplay input until a unique target cue is independently established.

The regression workflow now recomputes the badge centroid-versus-scene displacement and the red focus-ring pixel count on those same authenticated private frames. It requires the known map-UP arrow ring plus panel differential, rejects a comparable ring around the map-WAIT/Revision65 pink badge, keeps WAIT controls and prompt/footer invariance, and fails closed if the new signatures drift. A source test protects these assertions and verifies the token gate remains before private source-checkpoint download and PAD mutation. The player workflow and marker were not modified.

**Next:** verify regression #39973978654 reaches `success`, inspect the `MAP_FOCUS_ARROW_RING_REGRESSION` and `REV65_BADGE_SHIFT_FOLLOWS_SCENE` output, then proceed only with offline cue analysis if anything is still ambiguous. Do not dispatch or rerun the player, do not reuse Revision65, and do not promote its output savestates without fresh-process restore tests. Readiness remains **NO-GO**; Story Mode remains **NOT COMPLETE**.


---

## Safety incident — unintended Actions launches from repository-tree recovery (23 October 2026)

This is an operational incident, not new gameplay evidence. An earlier documentation commit `ed5de51263ee0266c196a2630d122092e4bad314` had an incomplete tree. Recovery commit `98c0577cf7ca026edf861ac307c380745a225d25` restored the complete 82-file tree, but GitHub compared it to the incomplete parent and treated many existing `.github/workflows/*` paths as newly added. Their path-filtered `push` triggers fired automatically. This was caused by my commit-construction error; it was not an intended gameplay experiment.

**Confirmed unintended inputs / runs:**

- Fastboot GPU traffic run [#39975090633](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39975090633) logged controller override readback PASS for `CROSS` at frames 225–235, `START` 238–248, `CROSS` 251–261, `START` 264–274, `UP` 277–287, and `CROSS` 290–298. Game-state effect was not independently established.
- Fastboot GDB/RSP run [#39975090681](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39975090681) logged a `Return then Z/Cross` input test and captured after-input window frames. Its pre-input window was all black; gameplay effect is unknown.
- Retail-BIOS progress run [#39975090632](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39975090632) logged the `Return,Z` keyboard-test begin/end markers and captures; game-state effect is unknown.
- The legacy Story Mode playthrough [#39975090240](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39975090240) was unexpectedly started by the push event and later ended `cancelled`; its script was configured for a fixed START/DOWN/UP/CIRCLE sequence and a visual-gated follow-up, plus START for identified dialogue. Do not use this run as an accepted experiment or progress checkpoint. It emitted a private Memory Card candidate of 131,072 bytes with status `UNVERIFIED_REQUIRES_IN_GAME_SAVE_AND_RELOAD`; its log reported `STORY_RAW_STATE_PRESENT=0`. These artifacts remain outside Git and must not be promoted.
- Window-identification run [#39975090175](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39975090175) and current-source GUI run [#39975090570](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39975090570) were cancelled using their workflow concurrency groups. The adaptive player push run [#39975090690](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39975090690) was `skipped`.
- Additional BIOS/GUI/controller diagnostic workflows also received the accidental push event. Their output is excluded from target-cue classification and must not be promoted as an authorized Story Mode checkpoint.

**Mitigation:** the identified input-bearing diagnostics now have a job-level `if: github.event_name == 'workflow_dispatch'` guard so pushes skip them; their latest replacement push runs are `skipped`. The legacy fixed-sequence Story Mode workflow is set to `if: false`; the raw Story Mode restore/continuation workflow is also `if: false` until the target cue/readiness gate is independently passed. A unit test protects these guards. No ROM, BIOS, screenshot, Memory Card, savestate, or private evidence was added to Git.

**Research decision remains unchanged:** `barrier_level_selection` action `WAIT`; cue token absent; adaptive-player readiness **NO-GO**; Story Mode **NOT COMPLETE**. Nothing from the accidental runs changes those statuses.

### Follow-up chain containment details

- Raw restore-chain run [#39977472612](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39977472612) was triggered because the old `workflow_run` condition excluded `cancelled` but mistakenly accepted `skipped`. It failed at `Download raw checkpoint evidence from the source run`; the run was cancelled before emulator restore/continuation. Its follow-up [#39977746401](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39977746401) was `skipped`.
- `.github/workflows/naruto-raw-storymode-restore.yml` now has `if: false` and `concurrency.cancel-in-progress: true`; the legacy Story Mode playthrough `.github/workflows/naruto-scph7502-gpu-traffic-summary.yml` is `if: false` and therefore cannot be run by push or manual dispatch while the target/readiness gate is NO-GO.
- The 11 identified diagnostic jobs whose scripts contain fixed keyboard/controller tests are manual-dispatch-only (`if: github.event_name == 'workflow_dispatch'`). Their replacement runs from the guard commits completed `skipped`. Run #39978029528 is the regression for the guard source test and remained `in_progress` at this update; no additional workflow runs were active.

## Verified focus-cue regression and safety containment — 23 October 2026

- Current passing regression: [#39978745505](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39978745505), source `1e22c1b37d0233455a5a6cf49ddf98e6e555c93c`, all 15 workflow steps passed, 26 tests in 3.189 s.
- Authentic output: `MAP_FOCUS_ARROW_RING_REGRESSION=PASS known_map_ring_plus_matching_panel=true Revision65_ring_absent=true target_role=UNKNOWN`; `CAMERA_SHIFT_REGRESSION=PASS UP_scene_shift_approx_100px WAIT_scene_shift_approx_0px target_selection_not_inferred=true`; `REV65_BADGE_SHIFT_FOLLOWS_SCENE=PASS badge_delta_y=97.46px registered_scene_delta_y=100px within_tolerance=true camera_pan_confounds_exposure=true selection_not_proven=true`.
- A later source test additionally asserts that `.github/workflows/naruto-raw-storymode-restore.yml` stays `if: false` and its concurrency group has `cancel-in-progress: true`. These assertions passed in the current run.
- Intermediate regression #39978693381 on commit `79a7fb7...` ultimately failed one safety-test assertion because newline matching was over-escaped. Fixed source commit `1e22c1b...` has independent passing run #39978745505. The failure was CI/test-only, not gameplay.
- Containment remains: consumed Revision65 marker unchanged; cue token absent; classifier action `WAIT`; readiness **NO-GO**; Story Mode **NOT COMPLETE**. Story Mode playthrough and raw restore workflow hard-disabled; identified input-bearing probes require explicit manual dispatch.

## Static reverse-engineering progress — 27 October 2026 (Langkah 4–5 selesai; Langkah 6 berjalan)

- Batas repo dipatuhi: hanya naruto-shinobi-jintori-research diakses/diubah. Tidak ada emulator, boot game, atau input gameplay.
- Langkah 4 selesai pada cakupan statis executable utama. Run [#40439763833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40439763833) sukses. Rutinitas LCG, empat pemanggil langsung, pembentukan/penyisipan/pengacakan daftar byte, serta pemeriksaan kandidat berbasis bitset sudah ditelusuri. Seed runtime dan arti gameplay ID tetap UNKNOWN. Laporan: [docs/STEP4_RNG_TRACE_2026-10-27.md](docs/STEP4_RNG_TRACE_2026-10-27.md).
- Langkah 5 selesai sebagai analisis statis awal DATA.BIN entry 1: offset 0x10BB000, 596.412 byte, SHA-256 potongan 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a. Ghidra dengan base hipotesis 0x800D0000 menemukan enam lokasi yang memanggil getter target Chakra 0x80012A70 dan melakukan pembandingan field record/target. Base runtime belum tervalidasi. Laporan: [docs/STEP5_DATABIN_ENTRY1_ANALYSIS_2026-10-27.md](docs/STEP5_DATABIN_ENTRY1_ANALYSIS_2026-10-27.md).
- Langkah 6 disiapkan: dekompilasi pemanggil tambahan getter target, transisi FUN_800EF98C/FUN_80100D14/FUN_80100DCC, jalur pembanding gagal, serta konsumen setter Chakra. Workflow run terbaru [#40440237256](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40440237256) baru berstatus queued saat catatan ini ditulis.
- Artefak Ghidra yang berhasil berisi teks saja (fungsi TSV/log/dekompilasi); BIN, DATA.BIN, entry resource, BIOS, savestate, Memory Card, dan screenshot privat tidak diunggah atau di-commit.
- Gerbang pemain adaptif tetap fail-closed: target cue UNKNOWN; barrier_level_selection = WAIT; readiness NO-GO; Story Mode NOT COMPLETE; marker Revision65 tetap tidak disentuh.


## 27 Oktober 2026 — evidence update Step 4–10

### Step 4 runtime determinism (run #40474262267; raw artifact #12719024236)
- Corrected the prior fixed-F177 observer mismatch: run #40471968654 was invalid/timeout because actual terminal caller event was F171–F172. Run #40473505032 also failed due capture pause/callback lifecycle/parser escaping; it is not used as determinism proof.
- The corrected run produced three successful branches from the authenticated roulette F120 checkpoint: R30A/R30B Circle F30–F38, DELAY60 Circle F60–F68. All press/release readbacks PASS. Initial state 0xDB75C114; each branch recorded 127 RNG calls; no post-restore setter hit; final state 0xA99DC6E7.
- Normalized sequence/caller/state-before stream matched across all three branches when VSync frame number was omitted. Sampled states matched. Authenticated X11 PNGs all validated 1280×800, 724063 bytes, 117603 colors, crop SHA-256 a1b2dfab61a0922e2b466ddbeb6b5b2642a88289be159df4667e4e2bcaa53355. Capture frames differ 169/167/171, so do not claim same-VSync-frame comparison. The causal link between specific caller and visible roulette outcome is not proven.
- The runtime's final report-write step failed with curl exit 22; this is not the same as emulator/test failure. Report rebuilt from raw log/artifact in out/step4/STEP4_RNG_RUNTIME_RESULT_2026-10-27.md.
- Step 4 remains SEBAGIAN: seed boot/lifecycle, pointers/indirect dispatch, battle caller, outcome linkage and alternative randomness are open.

### Step 6 static xref semantic review
- Existing text-only artifact #12713583805 from Ghidra run #40455975408 was audited by runner-only review #40473737136 (text artifact #12719587873). Eight target-getter xrefs to 0x80012A70, nine Chakra setter xrefs to 0x8001387C, sixteen player-Chakra getter refs to 0x800138EC were recorded at the hypothetical entry-1 base. UI functions also read the target; xref alone does not identify win conditions. Report docs/STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md. Status SEBAGIAN.

### Step 9 isolated MIPS CPU execution
- First run #40474699863 failed all 7 vectors with zero executed instructions because Unicorn was mapped at virtual KSEG0 addresses. This diagnoses a memory-map error, not a failed LCG formula.
- Corrected probe uses physical 2 MiB RAM aliases for KSEG0. Run #40474891838 success; artifact #12720127454, ZIP digest bcbfcd77a532ce34334ed60f720fdeaac566308bf2e6e4d54a7e60f28a5f083b. Seven states produced the expected updated state, v0 and sentinel return in 12 instructions each. Cleanup PASS. This closes Step 9 only for RNG routine 0x80035D78, not a PS1 emulator or all game functions. Report out/step9/STEP9_UNICORN_RESULT_2026-10-27.md.

### Step 7 cold-boot diagnostic preparation
- Created .github/workflows/step7-loader-coldboot-diagnostic.yml with hash-pinned source assets, 3000-frame/70-second bound, no save-state restore/input, register/adler checksums at candidate copy addresses 0x800AD454/0x800AD45C, seed setter candidate 0x80035DA8 and RNG entry 0x80035D78. Text-only artifact; no RAM dump or screenshot.
- Initial workflow failed to start because job env used unavailable runner.temp context, and a bounded X11 wait loop had a ShellCheck warning. Those were corrected; lint run #40475950897 passed.
- Diagnostic run #40475950842 is running the bounded cold-boot observation after verifying assets. No final evidence has been accepted yet. Do not dispatch a duplicate. If it produces no candidate hit, record as “no hit inside this window,” not as proof target/path is absent.
- Overall statuses: Step4 SEBAGIAN; Step5 TUNTAS for four selected functions; Step6 SEBAGIAN; Step7 SEBAGIAN pending coldboot result; Step8 SEBAGIAN; Step9 TUNTAS for the primary RNG routine only; Step10 TUNTAS as documentation index.

Story Mode remains TIDAK TERBUKTI TAMAT. Adaptive-player/automatic Story Mode execution remains paused. No classifier/input policy/readiness gate/Revision65 marker changed. No ROM/disc, BIOS, Memory Card, savestate, RAM dump or private gameplay screenshot is in Git.

## Audit continuation — verified raw MIPS trace (27 October 2026)

Parent snapshot when this addendum was prepared: 52f077114c01de00cac52527af92e38a1d4a1e3e. Artifact #12719587873 from runner-only [Actions #40473737136](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136), ZIP SHA-256 e1ea68c92bcbf645fde3c991c8a47192b815987d8044f2d599c163c1f3ec9fb9, was reviewed directly. No runtime experiment was executed.

The targeted MIPS windows now document six entry-1 target-gated sites, record stride 0x90, field +0x04 versus target getter 0x80012A70, failure branch 0x8011253C, a record flag bit 0x200 gate, helper gate 0x800BDBFC(0x20), and conditional byte/halfword stores. Candidate 0x8011C0D0 negates record +0x04, clamps at -9999, stores, then calls main-EXE setter 0x8001387C. DATA.BIN entry-1 base 0x800D0000 remains a static hypothesis; transition and game-rule semantics remain UNKNOWN. Fields +0xB30/+0xB38/+0xB40/+0xB44 are not comprehensively traced.

Separate Step 4 correction: seed candidate callsite 0x800AF2AC forwards return value from helper 0x80037138 to 0x80035DA8 through the JAL delay-slot instruction move a0,v0. The -1 literal goes to the helper, not a proven setter input. Helper return and seed lifecycle remain UNKNOWN.

Statuses unchanged: Step4 SEBAGIAN; Step5 TUNTAS for four selected functions; Step6 SEBAGIAN; Step7 SEBAGIAN; Step8 SEBAGIAN; Step9 TUNTAS only for 0x80035D78; Step10 TUNTAS as audit index only. Story Mode TIDAK TERBUKTI TAMAT. No adaptive-player, Story Mode automatic workflow, gameplay input, or savestate restoration was used. Review latest Actions again before any runtime work.

## Further Step 6 static trace — 27 October 2026

Review of existing artifact #12719587873 adds the bounded decompilation for candidate 0x8011C0D0 (body 408 bytes): input byte-mask; compare with global 0x80139F70; early return if unchanged; update global and field +0x618 if changed. Nonzero input selects a record via global 0x8013EA88, writes 8 at record+0x22, iterates participant count from global 0x8013EA71, negates each record word +0x04, clamps minimum -9999, stores and calls setter 0x8001387C with index/new value. A signed-short +0x10 plus unsigned-short +0x14 sum compared to 0x101 affects calls to 0x8003F5D0 and 0x800F96A4 versus store +0x94A=1. The raw window only contains the function start; these loop details are from decompilation, not full raw listing. Function caller and semantics are UNKNOWN.

Outstanding static gap: no whole-program access inventory of candidate offsets +0xB30/+0xB38/+0xB40/+0xB44 yet. The main-EXE/entry-1 bases remain distinct hypotheses; no runtime semantics are inferred.


## 27 October 2026 17:26 WIB — live run and Step 6 scope check

Verified remote `main` before handoff refresh at `2ad2c8dcdcaeee718d656e8696d6853f48ec54a8`; handoff refresh commit then became `e128fe86da6dbd3848813a376aa5b63f53e39977`. Actions #40487406384 remains `in_progress`, job `122132544196`, with DATA.BIN entry 0/helper `0x80037138` still being analyzed. Main EXE and entry 1 are complete; upload/cleanup pending; artifact not yet available. Do not infer helper return or seed lifecycle until its output can be inspected. Previous full Ghidra run duration ~39m43s is reference only, not a guaranteed ETA.

Reconfirmed that Step 6's `0x8011C0D0` trace is bounded decompiler evidence and cannot label the path as a gameplay cost. Whole-program access/store tracing for `+0xB30/+0xB38/+0xB40/+0xB44` remains an independent static task. Do not overlap runtime probes or repeat the prior no-hit targets absent a distinct hypothesis. No adaptive player, Story Mode automation, gameplay input, or savestate restore was performed; Story Mode remains unverified complete.

## Live audit checkpoint — 27 October 2026, 17:24 WIB

- Re-read the live `main` files and verified that the current commit before this checkpoint was `2ad2c8dcdcaeee718d656e8696d6853f48ec54a8`. GitHub connector does not expose a local working-tree status; no local clean/dirty claim is made.
- Re-fetched raw job logs and metadata for Step 7 run [#40484548650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650). Job `coldboot-loader` completed `success`; asset provenance in the log confirms disc label/ID `SLPS-03553 / SLPS03553` and BIOS `SCPH-7502 (EU)`. The observation logs show preflight frame 50, listener-only control max frame 60, target `0x800AD454` progress through frame 120 with `bp_hits=0`, and bounded timeout `124`. The report artifact is #12724961702, 3,960 bytes, digest `sha256:27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71`; raw job log explicitly confirms upload digest and `STEP7_PRIVATE_CLEANUP=PASS`. No breakpoint hit or register/copy-size/buffer-checksum evidence exists. The result remains a bounded no-hit, not proof the loader is absent or its base is known.
- Step 9 criteria/report review confirms the isolated-execution criterion is satisfied only for `0x80035D78`: 7/7 vectors, state and `v0` correct, sentinel return in 12 instructions, max bound 128, physical 2 MiB RAM alias. The criterion does not require an indiscriminate all-functions sweep; no extra probe is justified absent a specific new claim.
- Active Actions run: [#40487406384](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40487406384), job `Verify and analyze PS-X EXE` / `122132544196`, step 11 `Extract and analyze DATA.BIN entry 0 for external helper` is `in_progress`. It began 17:18:13 WIB. The prior comparable full Ghidra run took about 39m43s, so an indicative finish is around 17:58 WIB, not a guarantee. Do not launch overlapping diagnostic work; inspect final logs/artifact after this run completes.
- No adaptive-player/Story Mode workflow, gameplay input, savestate restore, classifier/policy/readiness-gate edit, or private asset commit was performed. Story Mode remains `TIDAK TERBUKTI TAMAT`. Remaining Steps 4, 6, 7, and 8 stay partial; Step 5 remains complete only for four selected functions; Step 9 only for the RNG routine; Step 10 is an index, not proof of complete game understanding.

## Incremental checkpoint — helper-return source and pending-field MIPS trace (27 Oktober 2026, snapshot terverifikasi 18:38 WIB)

Runner-only audit [#40497668341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40497668341) success at **18:38:45 WIB**. Text artifact #12730957210: 9,014 bytes; ZIP SHA-256 `695e36bf70237913c0f80c94f0d4100732c92dd8b78155da2ace90d189c5ee24`; raw log `RUNNER_ARTIFACT_CLEANUP=PASS`. Audit metadata/digests matched and the latest Step 6 artifact #12729156734 (run #40493556711, 180,128 bytes, ZIP SHA-256 `c9ea5ef0552a0c80a70f0d3a758622a358509de2079e5954dac3ce0032426e93`) was inspected on runner.

**Step 4 return helper:** raw MIPS for main EXE function `0x80037138` shows input `a0<0` branches to code loading `0x80066E7C` into `v0` before the common epilogue. At candidate DATA.BIN entry-0 callsite, `jal 0x80037138` has delay-slot `li a0,-1`; the next `jal 0x80035DA8` has delay-slot `move a0,v0`. Static dataflow therefore connects global value `0x80066E7C` to the candidate setter argument if that callsite executes; it does not prove boot-time value or runtime reachability. Entry-0 base `0x800AD000` remains HIPOTESIS. The function body is 376 bytes (94 MIPS instructions); its other paths compute a 16-bit difference and call helper `0x800372B0`, so the entire function must not be described as a constant-return stub.

Previous run #40493608676 failed because grep expected target markers with `0x`, while Ghidra emitted `=== TARGET 80037138 ===` and lowercase `80035da8`. The artifact #12730020903 remains useful evidence (8,395 bytes, ZIP SHA-256 `00b54f4e8c059f81d0f4d75aea04f2deccece564edff73378096b369e4fd7c79`; cleanup PASS). Duplicate trailing text in the workflow was subsequently removed at commit `029fdfab8df55dd16001916f0f53b7abd073c334`; corrective helper run #40497723766 had not finished in the audit snapshot and must be rechecked rather than presumed successful.

**Step 6 memory operand trace:** within the entry-1 code view, raw instructions show `lw v0,0xB30(a0)` at `0x8012C634`, `lw v1,0xB38(a0)` at `0x8012C638`, `addu v0,v0,v1` at `0x8012C640`, and `sw v0,0xB40(a0)` at `0x8012C644`. A candidate initializer writes zero to `+0xB44` at `0x8012C604` as a JAL delay-slot instruction; another function reads `+0xB44` at `0x8012CB14` into argument `a2` for `0x8001B364`. These are instruction/dataflow facts only under hypothetical entry-1 base `0x800D0000`; object identity, full aliases, runtime mapping, and gameplay semantics are UNKNOWN.

Step 4/6/8 remain SEBAGIAN. No gameplay, emulator, savestate or adaptive-player work was run.

## Incremental checkpoint — data xrefs global 0x80066E7C (27 Oktober 2026, 18:44 WIB)

Helper audit [#40498231825](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498231825) selesai success pada 18:43:58 WIB, artifact #12732006381 (9.058 byte; ZIP SHA-256 adfdb608af96dd95a7c7e74d9f8b117767aaffa817d0c7eb860757ead868d9ba). Raw log membuktikan asset-checksums OK, source image/extraction tree dihapus sebelum Ghidra, STEP4_HELPER_PRIVATE_CLEANUP=PASS, text_only_output_validation=PASS, dan uploaded_input_executable=no.

Runner-only audit [#40498386273](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498386273) selesai success 18:44:35 WIB, artifact #12731327556 (9.727 byte; ZIP SHA-256 7826480f41372d68ddf3f4b1dfe6d99f51bbbb5cd124eb5c3c6169870150ba5c). Metadata dan ZIP digest #12732006381 diverifikasi di runner; cleanup PASS.

Tambahan target export membaca data reference langsung ke 0x80066E7C. Ghidra melaporkan 8 references in loaded EXE view: WRITE 0x80037B7C (sw zero,0x6e7c(at), owner function 0x80037B58); READ 0x80037BB4 (owner 0x80037BB0); WRITE 0x80037BDC (sw v0,0x6e7c(at), preceding addiu v0,v0,1 at 0x80037BD4, owner 0x80037BB0); READ 0x8003719C, 0x80037204, 0x80037260 (helper 0x80037138); and READ 0x800372C0 and 0x80037324 (function 0x800372B0). Loaded image initial bytes at 0x80066E7C are 00000000 (little-endian word 0), but this is not runtime state. Evidence supports only static zero-store and incrementing-store patterns; sequencing, full aliases, indirect/overlay writers and runtime value remain UNKNOWN. The label “counter-like” is a provisional pattern description, not a confirmed gameplay meaning.

Step 4 remains SEBAGIAN until caller/initializer ordering and boot-time value are pinned down. No emulator/gameplay run was performed.

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

The full Ghidra analysis run [#40498208067](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498208067) was still `in_progress` when checked (last API update 18:42:59 WIB; job remained in “Extract and analyze DATA.BIN entry 0 for external helper”). No completion time is available from the API; do not estimate its outcome.

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

The full Ghidra analysis run [#40498208067](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498208067) remained `in_progress` when checked; its last API update was 18:42:59 WIB and it was still on “Extract and analyze DATA.BIN entry 0 for external helper”. No ETA is available from the API, so no completion time or result is inferred.


## Live checkpoint — latest Ghidra/Step 6 runner-only audit (27 October 2026, 19:22 WIB)

- Ghidra run #40498208067 completed success at 19:14:42 WIB. Artifact #12732952776: 2,255,170 bytes; ZIP SHA-256 6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6. The artifact holds a 1,206-row main EXE function list, 1,555 entry-1 rows, 38 entry-0 rows, and text-only focused MIPS/decompilation reports. DATA.BIN entry0 offset 0x5F800, size 110,536 bytes, SHA-256 56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4. The hypothetical load address 0x800AD000 is not runtime validated; entry1 0x800D0000 is also hypothetical.
- Step 6 run #40500058788 completed success at 18:59:18 WIB. Artifact #12731474756: 180,174 bytes; ZIP SHA-256 4aea20e1420292505666f15898ba2db57a875a4fc67fbe2c65336af0a16fc9f4. The scanner covered 98,357 decoded instructions but only exact 16-bit immediate values, output cap 200 per offset; it explicitly misses pointer arithmetic, split immediates, aliases, undisassembled code and alternate bases. It captured operand window +0xB30/+0xB38 -> addu -> +0xB40, plus +0xB44 zero-store and load-to-a2 call flow.
- Runner audit #40503223693 completed success at 19:22:30 WIB. Text-only artifact #12733512950, 13,079 bytes, ZIP SHA-256 382773f9a421835bc97c448c630a2ea5d3891309bb34094f5a67027548c03414. Raw log verifies artifact id/run/name/size/digest/expiry, ZIP hashes before content reads, no raw binary uploads, and RUNNER_ARTIFACT_CLEANUP=PASS. The 346,593,927-byte Ghidra entry0 log was hashed but not read; note as explicit limit.
- Static Step 4 update: 0x80037B58 zeroes 0x80066E7C, clears eight callback slots, and calls the indirect dispatcher prepared with 0x80037BB0. That function increments the global and invokes nonzero callback slots. Helper 0x80037138 returns the global on a negative-a0 path. Candidate DATA.BIN entry0 code sends helper return to setter 0x80035DA8 under base hypothesis 0x800AD000; -1 is passed to helper, not established as setter value. This does not prove boot seed/lifecycle or runtime call ordering.
- Current status: Step4 SEBAGIAN; Step5 TUNTAS for four selected functions only; Step6 SEBAGIAN; Step7 SEBAGIAN; Step8 SEBAGIAN; Step9 TUNTAS only for 0x80035D78 (7/7 vectors); Step10 TUNTAS only as an auditable criterion closure matrix. Story Mode TIDAK TERBUKTI TAMAT. Detailed matrix: docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md. No game/emulator, gameplay input, savestate restore or adaptive-player action occurred.


## Live checkpoint — Step 6 direct memory inventory fully emitted and runner-audited (27 October 2026, 19:35 WIB)

- Scan [#40504640855](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504640855) completed success at 19:34:31 WIB. Artifact #12733854252: 220,128 bytes; ZIP SHA-256 90288a1c8b454cbdc45c75e0244d26508628ecf88bfe8e73ed88524c8cb80891.
- Runner-only audit [#40504977322](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504977322) completed success at 19:35:51 WIB. Artifact #12734840847: 25,756 bytes; ZIP SHA-256 d022b23548fe95eb34bfbb7a7fb0dd190a498ca54fff11516818138701920398. Metadata/digest/expiry checks passed for latest Ghidra, Step6 and helper artifacts; RUNNER_ARTIFACT_CLEANUP=PASS.
- Step6 scan covered 98,357 decoded Ghidra instructions in the hypothetical DATA.BIN entry1 view and emitted its aggregate direct-memory displacement inventory between explicit BEGIN/END markers. The full output block stayed below the runner audit's 30,001-line output cap. Four priority offsets were not subject to per-offset output cap. Direct base+displacement counts: +0xB30 one read, +0xB38 one read, +0xB40 one write, +0xB44 one read and one write. Raw instruction window: 0x8012C634 lw v0,0xB30(a0) [30 0B 82 8C]; 0x8012C638 lw v1,0xB38(a0) [38 0B 83 8C]; 0x8012C640 addu v0,v0,v1 [21 10 43 00]; 0x8012C644 sw v0,0xB40(a0) [40 0B 82 AC]; +0xB44 write at 0x8012C604 and read at 0x8012CB14 forwarded in a2 to 0x8001B364.
- Limitation: this census covers recognized direct base+displacement memory operations in Ghidra-decoded code, not full pointer analysis. Base 0x800D0000 remains hypothetical; alias tracing is bounded linear 24-instruction lookback and simple-MOVE only. Indirect aliases, computed pointers, split immediates, undecoded code, alternate bases, object identity and semantic field meaning remain UNKNOWN. Some Ghidra decompilations fail due to malformed P-code/bad instruction boundaries. Step6 remains SEBAGIAN.
- Overall status remains Step4 SEBAGIAN; Step5 TUNTAS only for four selected functions; Step6 SEBAGIAN; Step7 SEBAGIAN; Step8 SEBAGIAN; Step9 TUNTAS only for 0x80035D78; Step10 TUNTAS only as criterion-level closure matrix. Story Mode TIDAK TERBUKTI TAMAT.
- No emulator/gameplay, gameplay input, savestate restore, adaptive-player changes or private game asset upload was performed.


<!-- step4-step8-preset-list-shuffle-audit-2026-10-28 -->
## 28 Oktober 2026 — two-list preset loader and first-list-only shuffle

See the detailed trace [`docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md`](docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md). Raw main-EXE disassembly and Ghidra/m2c output in artifact #12739676233 prove `0x80015610` accepts a byte-valued selector <18, loads two 64-byte lists from `0x8005603C + selector*0x40 + group*0x480`, stops on `0xFF` or at 64 bytes, and stores counts at `0x80070D02 + group*2`. Groups are byte-identical for each selector. Selectors 0–8 have first-sentinel lengths 51,55,59,57,61,62,62,62,11; selectors 9–17 are 64 zero bytes with no sentinel, hence the static loader computes length 64 for them.

At `0x80015B9C`, `0x80015B7C` overwrites `a0=0`, reads count at `0x80070D02`, sets base offset to zero and performs 4*n random swaps over only the first buffer. Caller passes 0 then 1, but the helper discards the group parameter. Treat as a confirmed static asymmetry, not a confirmed programmer bug or game-rule label; IDs/feature semantics and consumers of the second list remain UNKNOWN.

Checkpoint restore was attempted without controller input in runs #40613996374 and #40614208610. Both reached the game/BIOS setup, then segfaulted during the savestate load before the load call returned or emitted `ExecutionFlow::SaveStateLoaded`. In the second, sanitized state plus reinserted BIOS reproduced the raw state SHA exactly; no third identical load is warranted. Checkpoint integrity is not proof of restorable state. No adaptive player was run.


## Descriptor selector table cross-check — 28 Oktober 2026

The two direct callsites for `0x80015610` obtain their selector from descriptor byte +2. Across the 18 decoded records, `0x80064918` yields `0,1,2,3,4,5,6,7,4,4,4,4,4,4,4,5,8,8`; `0x80057798` yields `0,1,2,8,3,4,8,5,6,6,0,0,0,0,0,0,3,5`. These tables only feed values 0–8 to the identified direct callsites, so source rows 9–17 are not selected by these tables, although the loader's guard allows them. Do not generalize beyond the two audited tables/callsites. See [detailed report](docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md).


<!-- caller-id-random-insert-audit-2026-10-28 -->
## Static caller trace — 28 Oktober 2026

Cross-checked raw MIPS in Step 5 artifact #12739676233. Direct JAL at `0x80013B50` calls `0x80015ADC`; its delay slot `0x80013B54` passes the byte returned by `0x800139FC(group,slot)`. That getter bounds group <4 and slot <3, then reads record byte +0x0A relative to `0x80070EA0) plus calculated record offsets. The inserted ID is validated against the 52-entry registry. The routine derives the index from `byte[0x80070D02]` and RNG: `floor(n/2)+(RNG mod floor(n/2))`; `0x800159BC` shifts the `0x80070D0A` order bytes right, writes the ID to `0x80070C80+0x8A+position`, and increments the separate count `0x80070C82` under a <64 guard. Zero divisor at n<2 reaches a MIPS break instruction; caller precondition/reachability still not proven. No feature name is assigned. See the detailed trace. 


<!-- four-record-three-slot-id-operations-2026-10-28 -->
## Four-record ID-slot operations — 28 Oktober 2026

Additional source-level trace in the preset/list report: `0x80070EA0)-based storage is indexed in four records of stride `0xB4`; each record uses adjacent candidate-ID bytes at `+0xA,+0xB,+0xC`. The raw body at `0x80013A48` inserts a registry-valid byte into the first invalid slot and returns failure when all three slots are occupied. The body at `0x80013B10` reads a slot ID, transfers it through `0x80015ADC` into the pseudo-random insertion path, closes the hole for source slots 0 or 1, and sets the tail byte `+0xC` to `0xFF`. This establishes a three-slot ID collection/transfer pattern. It does not identify the feature represented by these IDs or prove when the routines are reached in visible gameplay.
