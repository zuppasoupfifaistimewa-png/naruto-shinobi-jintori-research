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

# ADDENDUM TERBARU — audit terarah setelah checkpoint 07:06 WIB, 28 Oktober 2026

Audit langsung artefak teks Step 5/6 menambahkan dua batas penting tanpa menaikkan status: disassembly main EXE memuat 156 mnemonic JALR (target dinamis belum diselesaikan), dan ada perbedaan representasi span `0x80015B7C` antara body Ghidra (240 alamat; end-exclusive `0x80015C6C`) dengan anotasi `nonmatching` spimdisasm sebesar `0x580` yang mencakup label tambahan. Empat direct JAL ke RNG tetap hanya empat pada main EXE yang diperiksa. Pada view entry-1 statis, `+0xB30` dan `+0xB38` masing-masing memiliki satu READ; `+0xB40` satu WRITE; `+0xB44` satu WRITE dan satu READ. Base entry-1 `0x800D0000`, pointer `0x8013A554`, alias runtime dan semantik field tetap belum terverifikasi.

Laporan bukti terbaru: [docs/STEP4_10_TARGETED_AUDIT_2026-10-28.md](docs/STEP4_10_TARGETED_AUDIT_2026-10-28.md). Status Langkah 4–9 tidak berubah; Langkah 10 tuntas hanya sebagai matriks audit. Story Mode **TIDAK TERBUKTI TAMAT**. Adaptive player tetap tidak dijalankan/diubah. Pemeriksaan Actions dengan filter `queued` dan `in_progress` masing-masing menghasilkan 0.

---

# ADDENDUM — cross-check bukti dan checkpoint, 28 Oktober 2026

Audit statis pada parent 7df287bf4ca21f6c32fe2589bc09e8665e62e846 dan tiga artefak yang SHA-nya cocok dengan catatan repo menambah rincian: disassembly main EXE memuat tepat empat direct JAL ke RNG 0x80035D78 pada 0x80015B14, 0x80015BF0, 0x8001A460, dan 0x80020C24; dalam view entry-1 hipotetis, +0xB30/+0xB38 dijumlahkan dan disimpan ke +0xB40, sedangkan +0xB44 diinisialisasi nol lalu dikirim ke helper 0x8001B364 pada branch tertentu. Step 9 artifact telah diperiksa langsung: RNG 7/7, helper negative-a0 8/8, setter/getter 16/16 pada model CPU/MIPS dengan fixture MMIO sintetis.

Laporan lengkap, inventaris bukti yang dibuka versus yang hanya direferensikan, matriks 17 kriteria, hash, batas tes, kegagalan historis dan gap teknis: [docs/STEP4_10_CROSSCHECK_2026-10-28.md](docs/STEP4_10_CROSSCHECK_2026-10-28.md). Handoff: [docs/HANDOFF_REVERSE_ENGINEERING_STEPS4_10_2026-10-28.md](docs/HANDOFF_REVERSE_ENGINEERING_STEPS4_10_2026-10-28.md).

Tidak ada status global Langkah 4–9 yang dinaikkan. Langkah 4 SEBAGIAN; Langkah 5 SEBAGIAN (14 fungsi terpilih, bukan cakupan total); Langkah 6(a,c) SEBAGIAN, 6(b) BLOCKED, 6(d) UNKNOWN; Langkah 7(a) SEBAGIAN, 7(b) BLOCKED; Langkah 8(a) SEBAGIAN, 8(b) UNKNOWN untuk label unsupported; Langkah 9(a) TUNTAS hanya untuk 7 vektor RNG dan 9(b) SEBAGIAN; Langkah 10 TUNTAS hanya sebagai matriks audit. Story Mode TIDAK TERBUKTI TAMAT. Tidak ada gameplay, input, restore savestate, emulator, adaptive player atau workflow dispatch yang dilakukan.
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

# ACTIONS LIVE CORRECTION — 27 Oktober 2026, pemeriksaan 21:54:52 WIB

Run [#40520635663](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40520635663) kini **completed/success** dengan artifact teks #12743796502 (2.299.302 byte; ZIP SHA-256 `e2d5b496b2310c17110c59710212f7605bf8b3d90b798abb438c1224bf3d0549`). Baca artifact menunjukkan bahwa Ghidra entry-0 analysis mencapai **timeout internal 1.800 detik** dan memunculkan banyak error function-body overlap/repair. Export tetap memberi 36 function-index rows, tetapi kandidat `0x800BDBFC` memiliki `reference_count=0`; ini bukan validasi caller/helper RNG. Perlakukan Step 4/5 pada resource entry 0 tetap parsial.

Run [#40521141039](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521141039) masih `in_progress` pada pemeriksaan terakhir, mulai 21:26:36 WIB; tahap entry 1 selesai dan tahap Ghidra entry 0 sedang berjalan; artifact belum tersedia. Pembanding yang sama #40520635663 selesai setelah 31m27s, dengan timeout analysis entry 0 1.800s. Perkiraan kasar untuk run aktif: sekitar **21:58–22:05 WIB**, dengan ketidakpastian karena status log hanya diperbarui berkala. Jangan duplikasi run ini.

---

# STATUS LIVE UPDATE — Langkah 4–10, 27 Oktober 2026 21:41 WIB

**Ringkasan otoritatif terbaru;** snapshot lama di bagian bawah adalah riwayat dan disupersede jika berbeda. HEAD sebelum commit dokumentasi ini: `c36b7407631291afd2a4d303f49a8b03392e2bbc`.

- **Step 4: SEBAGIAN.** RNG utama `0x80035D78` memakai `new_state = (old_state * 0x41C64E6D + 0x3039) mod 2^32`, output `(new_state >> 16) & 0x7FFF`; tes terisolasi 7/7. Entry-0 context run #40521136060 dan entry-1 context #40521136038 lulus. Jendela `0x800AF2A4`–`0x800AF2B0` membuktikan `-1` diterima helper `0x80037138), sedangkan return helper diteruskan ke setter `0x80035DA8). Caller boundary, base resource runtime, seed lifecycle, reachability, efek roulette/battle dan jalur tak langsung masih UNKNOWN.
- **Step 5: SEBAGIAN secara keseluruhan.** Main EXE: 13 fungsi terpilih memiliki output Ghidra/m2c yang berhasil. Tambahan run #40523020556 sukses dengan artifact #12742268706 (1.367.605 byte; ZIP SHA-256 `5f3f767667444f7c956c36fc59cf75b6bb90a5a1dde8ddb92fb69f9e0f797e81`) untuk satu fungsi kandidat entry 1 `0x800ED8C8`: batas 160 byte terverifikasi, dekompilasi Ghidra dan m2c sukses, direct RNG call `0x800ED8E4` terkonfirmasi. Total perbandingan terpilih sekarang 14 fungsi, bukan cakupan lengkap.
- **Step 6: SEBAGIAN.** Run #40522772847 sukses pada 21:38:32 WIB, artifact teks #12741234990 (234.210 byte; SHA-256 ZIP `7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9`). Ekspor CFG/SSA pada fungsi `0x8012C544` dan `0x8012CACC` memperjelas operasi dan jejak def-use lintas blok. Nilai pointer global pada `0x8013A554`, alias, base efektif runtime, dan arti field belum tertutup. 6(a) SEBAGIAN, 6(b) BLOCKED, 6(c) SEBAGIAN, 6(d) UNKNOWN.
- **Step 7: SEBAGIAN.** Struktur direktori dan jalur bootstrap copy didukung bukti statis. Tujuan copy aktual, panjang/checksum yang diterapkan, relokasi, lifecycle dan pemetaan DATA2.BIN/DUMMY.BIN runtime tetap UNKNOWN/BLOCKED. Base `0x800AD000` dan `0x800D0000` adalah hipotesis analisis, bukan base runtime tervalidasi.
- **Step 8: SEBAGIAN.** Fungsi kandidat `0x800ED8C8` secara statis mengembalikan byte helper kecuali saat `RNG % 250 >= byte` pada record yang dibasis oleh pointer yang dimuat dari slot global `0x8013EA74`, ketika mengembalikan `0xFF`. Disassembly mentah mengonfirmasi dereferensi; m2c menampilkan tipe/effective-address global secara berbeda dari Ghidra, jadi cross-check C dibatasi pada struktur fungsi/call, bukan tipe pointer yang identik. Identitas fiturnya tidak diketahui. Biaya, barrier/upgrade, kartu, giliran, aturan battle/roulette, kondisi menang/kalah masih UNKNOWN.
- **Step 9: SEBAGIAN secara keseluruhan.** #40516755810 sukses: RNG 7/7, setter/getter nilai pemain 16/16 kasus terisolasi; seluruh 11 job steps sukses dan cleanup PASS. Ini bukan emulasi PS1/gameplay penuh; tidak ada tes yang mengulang kasus sama pada sesi ini.
- **Step 10: TUNTAS hanya sebagai matriks rekonsiliasi kriteria/dokumentasi setelah pembaruan ini.** Ini bukan pernyataan bahwa semua langkah reverse engineering atau Story Mode selesai.

**Actions terbaru saat pemeriksaan:** #40523020556 Step 5 completed/success; #40522772847 Step 6/7 completed/success; #40521136060 dan #40521136038 context tests completed/success. Run Ghidra #40520635663 masih dilaporkan in_progress, mulai 21:23:22 WIB, di tahap analisis entry 0; API update terakhirnya stale. Run #40521141039 masih pending di concurrency group Ghidra. Run sebanding #40512917437 membutuhkan 34m43s, yang memberi patokan kasar sekitar 21:58 WIB untuk run aktif tersebut; karena status langkahnya tidak diperbarui sejak awal, ETA aktual belum dapat dipastikan. Jangan memulai scan duplikat.

Pekerjaan sesi ini terbatas pada analisis statis dan tes CPU terisolasi: pemain otomatis tidak dijalankan; tidak ada input gameplay, eksperimen tombol, restore savestate, sesi emulator/gameplay, perubahan adaptive player, classifier, input policy, readiness gate, atau workflow `.run-storymode-adaptive-player`. ROM/BIN/CUE, executable, BIOS, Memory Card, savestate, RAM dump, screenshot privat, dan data gameplay privat tidak ditaruh di Git/artefak. **Story Mode TIDAK TERBUKTI TAMAT.**

[Rekonsiliasi live](docs/STEP4_10_LIVE_RECONCILIATION_2026-10-27.md) · [Audit CFG/SSA Step 6](docs/STEP6_CFG_SSA_DATAFLOW_AUDIT_2026-10-27.md) · [Perbandingan Step 5](out/step5/STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md)

---

---

# STATUS LIVE UPDATE — Step 6 bounded register provenance, 27 Oktober 2026 20:25 WIB

## Step 5 — hasil perluasan terverifikasi (27 Oktober 2026, 20:50 WIB)

- Retry [#40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524) **completed/success** pada 20:50:53 WIB. Artefak teks [#12739676233](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524/artifacts/12739676233) berukuran 941.176 byte, digest API dan SHA-256 lokal cocok: `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d`. ZIP memuat 45 file teks/C/disassembly/log, termasuk 26 file C Ghidra/m2c nonempty; tidak ada ROM/BIN/CUE/EXE/BIOS, Memory Card, savestate, RAM dump atau screenshot. Semua langkah job selesai, termasuk penghapusan input/proyek sementara.
- Pemeriksaan aktual: `metadata_parser_fixture=PASS`, `function_metadata=PASS`, `functions_requested=13`, `functions_with_m2c_output=13`, laporan akhir `status=SUCCESS`. Masing-masing fungsi memiliki keluaran C Ghidra dan m2c; exit code m2c 0 untuk 13/13.
- Lingkup 13 target main EXE: empat caller RNG terdahulu; setter/getter nilai pemain pada `0x8001387C`/`0x800138EC`; RNG `0x80035D78`; helper `0x80037138`; dispatcher/initializer/callback routines `0x800373F8`, `0x8003755C`, `0x80037B58`, `0x80037BB0`, `0x80037C48`. Ini cross-check struktur same-address berdasarkan batas fungsi Ghidra, bukan kesamaan source asli atau bukti aturan gameplay.
- Percobaan pertama [#40512956924](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40512956924) gagal karena `0x80012A70` tidak memiliki fungsi Ghidra pada alamat itu dan tak memiliki metadata body. Perbaikan di [commit `2b16e67bfafde873c95b577bc030f6e0c9f84c58`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/2b16e67bfafde873c95b577bc030f6e0c9f84c58) mengeluarkan target itu dari daftar fungsi yang dibandingkan. Identitas/semantik target `0x80012A70` tetap perlu diperjelas; jangan anggap cross-check fungsi tersebut sudah berhasil.
- **Status Langkah 5 secara keseluruhan tetap SEBAGIAN** terhadap cakupan yang diminta: 13 fungsi inti executable utama sudah dibandingkan, tetapi fungsi kandidat di DATA.BIN entry 0/1 (termasuk pembanding target/record dan transisi), semua hubungan caller/callee wajib, serta seluruh executable belum dicakup m2c secara menyeluruh. Status lama “empat fungsi saja” adalah riwayat sebelum perluasan, bukan hasil terbaru.
- Run Ghidra statis terpisah [#40512917437](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40512917437) masih `in_progress`, dimulai 20:32:30 WIB, pada langkah analisis DATA.BIN entry 0 untuk external helper. Pembanding Ghidra sebelumnya #40498208067 membutuhkan sekitar 31 menit 47 detik; perkiraan kasar berdasarkan durasi itu sekitar **21:04 WIB**, bukan ETA terjamin.

---

# STATUS LIVE UPDATE — Step 6 bounded register provenance, 27 Oktober 2026 20:25 WIB

**Checkpoint terbaru Step 6 (27 Oktober 2026, 20:25 WIB):** scanner provenance di https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/0afc0eec4a5c12e4df5a17c771c8b0d28d7a99dd dijalankan oleh [Actions #40511758146](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40511758146) — completed/success pada 20:25:48 WIB. Artifact [#12737611770](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40511758146/artifacts/12737611770), 229.233 byte, SHA-256 ZIP `b84ff017cdbefb8ece6d04a7c8bef66b3fdc27b61412e91e10cc01485225b126`; digest API sama dengan SHA lokal. Enam anggota ZIP hanya teks/log; `text_only_output_count=6`, `private_binary_in_artifact=no`, `STEP6_PRIVATE_CLEANUP=PASS`. Fixture parser operand dan fixture pembentukan alamat `lui/ori/addiu/sign-extension` benar-benar mengeluarkan PASS. Laporan: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/docs/STEP6_REGISTER_PROVENANCE_AUDIT_2026-10-27.md.

- Tool source commit: `0afc0eec4a5c12e4df5a17c771c8b0d28d7a99dd`. Two static fixtures passed: displacement parser and address-construction/sign-extension.
- Scan coverage remains 98,357 decoded instructions. +B30/+B38/+B40/+B44 access counts are unchanged. The new trace narrows the reason aliases remain unresolved: `a0` comes from register-relative `lw a0,-0x5AAC(s0)` at 0x8012C628, but the preceding `s0` chain reaches a control-flow boundary; +B44 read's `v1` chain stops at branch 0x8012CAF8. This is not whole-program pointer/dataflow analysis.
- Status: Step 4 SEBAGIAN; Step 5 TUNTAS for four functions only; Step 6 SEBAGIAN (6b BLOCKED, 6d UNKNOWN); Step 7 SEBAGIAN/7b BLOCKED; Step 8 SEBAGIAN/8b UNKNOWN; Step 9 TUNTAS only for isolated RNG 0x80035D78; Step 10 TUNTAS as audit matrix only. Story Mode TIDAK TERBUKTI TAMAT.
- All steps in #40511758146 completed success; cleanup PASS and artifact validation was text-only. No emulator/game, gameplay input, savestate restore, adaptive-player source or player workflow was used. No private ROM/BIOS/executable/Memory Card/savestate/RAM dump/screenshot was committed or included in the artifact.

---

# STATUS LIVE UPDATE — 27 Oktober 2026: Step 6 inventory audit and criteria reconciliation

- HEAD pra-audit: cc81319cc00037a92a93a3e76552245dd9a9ebf7.
- Step 6 artifact #12733854252 (#40504640855) verified locally: 220.128 byte; ZIP SHA-256 90288a1c8b454cbdc45c75e0244d26508628ecf88bfe8e73ed88524c8cb80891; six text/log members.
- Independent text parsing: 98.357 decoded instructions; 2.104 displacement values; 31.081 direct operands (19.366 read / 11.715 write). B30/B38 loads are added and stored to B40; B44 has a zero-store and a read into argument a2 for candidate callee 0x8001B364, all under hypothetical base 0x800D0000.
- Counts are complete in the decoded-view aggregate, but context snippets are capped at 200 per common offset (+0x2E9: 257 accesses/200 contexts; +0x22: 275/200). B30/B38/B40/B44 are uncapped. Do not treat this as full alias/pointer analysis or field semantics.
- Latest relevant runs #40504640855 and #40504977322 succeeded; run #40506364365 is scheduled monitor-only and has no artifact. API snapshot: no active/queued runs.
- Current acceptance matrix, 17 criteria, exact artifact metadata and blockers: [STEP4_10_LIVE_RECONCILIATION_2026-10-27.md](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/docs/STEP4_10_LIVE_RECONCILIATION_2026-10-27.md). Steps 4/6/7/8/9 are not fully closed; Story Mode TIDAK TERBUKTI TAMAT. No gameplay, input, savestate restore, or adaptive-player edits in this audit.

---

# LIVE UPDATE — Step 6 extended field inventory audited, 27 Oktober 2026 19:35 WIB

- Extended static scan [#40504640855](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504640855) completed success at 19:34:31 WIB. Artifact #12733854252: 220,128 bytes; SHA-256 ZIP `90288a1c8b454cbdc45c75e0244d26508628ecf88bfe8e73ed88524c8cb80891`.
- Runner-only audit [#40504977322](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504977322) completed success at 19:35:51 WIB; artifact #12734840847: 25,756 bytes; SHA-256 ZIP `d022b23548fe95eb34bfbb7a7fb0dd190a498ca54fff11516818138701920398`. Metadata/digest checks passed, cleanup PASS.
- In the entry-1 hypothetical base view, direct memory inventory counts for `+0xB30`: 1 read/0 write; `+0xB38`: 1 read/0 write; `+0xB40`: 0 read/1 write; `+0xB44`: 1 read/1 write. These are statically verified operand observations, not verified field semantics.
- Direct displacement inventory emitted completely between delimiters and below the runner report’s 30,001-line output cap; priority offsets have no per-offset report cap. Still not a whole-program alias/pointer analysis; base `0x800D0000` remains hypothesis. Step 6 SEBAGIAN.
- Overall status stays Step 4 SEBAGIAN; Step 5 TUNTAS for four functions only; Step 6 SEBAGIAN; Step 7 SEBAGIAN; Step 8 SEBAGIAN; Step 9 TUNTAS only for `0x80035D78`; Step 10 TUNTAS as criteria matrix only. Story Mode TIDAK TERBUKTI TAMAT.
- No gameplay, input, savestate restore, adaptive-player changes or private game assets in artifacts/Git.

Detailed evidence and limits: docs/STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md and docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md.

# CHECKPOINT LIVE — reverse engineering Steps 4–10 — 27 Oktober 2026, verifikasi 19:22–19:24 WIB

Current source repo is the only repo used. Latest substantive verified commit before these document updates: runner audit workflow commit 555b84a4d178b41e4d04705e1700104bd41ed1d3. Ghidra analysis #40498208067 completed success at 19:14:42 WIB. Step 6 field scan #40500058788 completed success at 18:59:18 WIB. Runner-only artifact audit [#40503223693](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40503223693) completed success at 19:22:30 WIB and produced text-only artifact #12733512950 (13,079 bytes, ZIP SHA-256 382773f9a421835bc97c448c630a2ea5d3891309bb34094f5a67027548c03414).

Verified artefact identity/digest on runner:
- Ghidra artifact #12732952776 from #40498208067: 2,255,170 bytes; SHA-256 6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6.
- Step6 artifact #12731474756 from #40500058788: 180,174 bytes; SHA-256 4aea20e1420292505666f15898ba2db57a875a4fc67fbe2c65336af0a16fc9f4.
- Helper audit #12731593532 from #40499270568: 11,672 bytes; SHA-256 8567a5cad2a00823302ea7b361dd9b6eaab736bce6b77cf51ea136d6bee454b3.
Audit log passed metadata id/run/name/size/digest/expiry checks, verified ZIP hashes before reading, kept processing runner-side, did not upload private binaries, and reported RUNNER_ARTIFACT_CLEANUP=PASS. The 346,593,927-byte Ghidra entry0 raw log was hashed, not read/materialized; it remains a large-log inspection limit.

CURRENT STATUS:
- Step 4: SEBAGIAN. Main-EXE raw MIPS statically proves reset of global 0x80066E7C at 0x80037B58 and increment/store at 0x80037BB0. Helper 0x80037138 may return that global for negative a0. Candidate entry0 sequence 0x800AF2A4–0x800AF2B0 sends helper return to setter 0x80035DA8 under hypothetical base 0x800AD000. No runtime seed value/order or proof of base; battle caller, roulette-to-visible-result causality, indirect/JT/decompressed paths, RNG alternatives remain open.
- Step 5: TUNTAS only for four chosen functions 0x80015ADC, 0x80015B7C, 0x8001A328, 0x80020BF4 (run #40449144521; artifact #12710000931, SHA-256 b2fdb6dc3213137e98e0ed298402e1d4b02198ed5310f264780bd8e965246b08). No all-functions claim.
- Step 6: SEBAGIAN. Artifact #12731474756 raw operand context includes +0xB30/+0xB38 loads, add and +0xB40 store, plus +0xB44 zero-store/load. Exact immediate scanner covered 98,357 decoded instructions but does not close memory aliases, effective-address construction, pointer arithmetic, alternative bases, or undecoded code. Runtime base and meanings UNKNOWN.
- Step 7: SEBAGIAN. Static resource-directory/copy candidate available; coldboot breakpoint #40484548650 at 0x800AD454 had no hit through frame120, bounded exit124/timebox35s. Runtime copy source/destination/size/checksum/base/relocation unknown. Do not repeat same target without new static reachability evidence.
- Step 8: SEBAGIAN. Code behaviour is described only where raw instructions/dataflow support it. Costs, barrier/upgrade, battle/roulette/turn, card effects and victory conditions remain UNKNOWN/BLOCKED without independent corroboration.
- Step 9: TUNTAS for 0x80035D78 only (run #40474891838, artifact #12720127454, SHA-256 bcbfcd77a532ce34334ed60f720fdeaac566308bf2e6e4d54a7e60f28a5f083b; 7/7 vectors; state/v0 match, sentinel at 12 instructions, bound128, 2MiB PS1 RAM).
- Step 10: TUNTAS only as a criterion-level audit matrix, now in docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md, with artifacts/digests, tests, limits and named gaps. This is not whole-game completion.
- Story Mode: TIDAK TERBUKTI TAMAT.

Next minimum work from this checkpoint: inspect reports already updated at the top first; do not rerun Ghidra or identical no-hit probes. For Step6, first expand a static memory-operand/effective-address + alias inventory without match truncation. For Step7, choose any future runtime probe only from a newly statically justified reachable PC, with a bounded coldboot/no input/no savestate and text-only register/copy/checksum results. For Step4, statically reconcile loader/initializer/callsite order and raw-only/indirect caller candidates; runtime seed claims require actual captured register values. Do not touch adaptive player, Story Mode runner, classifier/policy/readiness gate, and do not commit private game/BIOS/memory-card/savestate/screenshot material.

# Checkpoint terbaru — reverse engineering Langkah 4–10 (27 Oktober 2026)

Checkpoint utama sebelum update ini: `main` SHA `6d4f2b06a586528cb6c43494359e9e172a6ff080`. Pembaruan status ini memajukan HEAD; ambil ulang SHA live untuk kelanjutan. Status working tree lokal tidak tersedia melalui konektor.

## Bukti/pekerjaan terbaru

- Bug parser shell/Python untuk VSync frame sudah diperbaiki. Regression run [#40484417534](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484417534) lulus dengan raw log `STEP7_FRAME_PARSER_FIXTURE_PASS frames=1,2,3,10,20,30,40 max=40`; itu validasi parser, bukan validasi loader.
- Single-breakpoint cold boot awal [#40484519812](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484519812) memakai satu breakpoint `0x800AD454`, tanpa input/restore. Raw log mencatat progress sampai frame 100 tanpa hit, exit 124/35 detik, cleanup PASS; report assembler gagal sintaks sehingga artifact #12723834084 (1.894 byte, ZIP SHA-256 `6188c32e73a0984133c5c1f4ac3a37dcacde677458ec56c7fdf100ba25c73968`) bukan ringkasan lengkap yang valid. Run koreksi [#40484548650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650) selesai `success` pada 10:00:47 UTC (17:00:47 WIB), durasi sekitar 291 detik. Report lengkap/artefak #12724961702 berukuran 3.960 byte, ZIP SHA-256 `27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71`: preflight frame 50; listener-only max frame 60; target `0x800AD454` progress hingga frame 120 tanpa hit (`SINGLE_BREAKPOINT_HIT=NO`, count 0), exit 124 pada batas 35 detik; seluruh steps lulus dan `STEP7_PRIVATE_CLEANUP=PASS`. Tidak ada hit/register/copy-size/checksum buffer, jadi Step 7 tetap SEBAGIAN.
- Parser report assembler diperbaiki pada commit `8326c07f71caeab12924133b0812ec7e86b8b1f7`; run koreksi #40484548650 sudah selesai dengan hasil/log/artefak/cleanup diperiksa. Regression fixture parser terpisah lulus pada #40484417534 dengan `frames=1,2,3,10,20,30,40 max=40`.
- Full text artifact Step 6 #12719587873 juga memperlihatkan lima kandidat entry-1 menulis `+0x2E9=0x3F`, `+0x2E5=0`, selector byte `+0x58B`, serta codes bersyarat `+0x5D2` (`0x200`, `8`, `4`, `0x20`, `0`/`0x1000`). Kandidat `0x8011C0D0` menegasikan record `+0x04`, clamp minimum `-9999`, lalu memanggil setter `0x8001387C`. Semua ini statis di base hipotesis `0x800D0000`; semantics tetap UNKNOWN. Field `+0xB30/+0xB38/+0xB40/+0xB44` belum punya sumber/final writer yang terpetakan menyeluruh. Lihat [Step 6](docs/STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md) dan [Step 8](docs/STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md).
- Audit delay-slot MIPS memperbaiki klaim lama tentang seed: `0x800AF2A8 li a0,-1` memberi argumen kepada helper `0x80037138`; delay slot setter `0x800AF2B0 move a0,v0` meneruskan nilai balik helper ke `0x80035DA8`. Nilai balik dan state tersimpan tetap UNKNOWN sampai bukti statis tambahan.
  
## Status keseluruhan per langkah

- Step 4: **SEBAGIAN** pada seluruh kriteria 4(a–e); rumus RNG benar secara statis dan uji terisolasi berlaku hanya untuk rutinnya. Seed boot/lifecycle, kausalitas roulette, battle caller, dispatch tidak langsung menyeluruh, dan randomness alternatif masih terbuka.
- Step 5: **TUNTAS untuk empat fungsi terpilih saja** (delapan output C Ghidra/m2c tersimpan).
- Step 6: **SEBAGIAN**; static stores `+0x2E9/+0x2E5/+0x58B/+0x5D2` sudah dilihat pada lima kandidat, tetapi field meanings, base runtime, sumber delta `+0xB30/+0xB38/+0xB40/+0xB44`, call boundaries dan semantics masih UNKNOWN.
- Step 7: **SEBAGIAN**; direktori/penyalinan didukung statis, runtime mapping/lifecycle/bases belum terbukti.
- Step 8: **SEBAGIAN**; tidak ada formula universal biaya barrier/level-up, battle/roulette/turn, atau syarat menang per mode yang terverifikasi.
- Step 9: **TUNTAS hanya untuk RNG `0x80035D78`** (7/7 vektor; run #40474891838), bukan emulator PS1 penuh atau fungsi lain.
- Step 10: **TUNTAS sebagai matriks closure audit per-kriteria saja**, bukan bukti seluruh game selesai.

Semua kriteria resmi yang belum terpenuhi harus tetap SEBAGIAN/UNKNOWN sampai bukti spesifik tersedia. Tidak ada workflow pemain adaptif/Story Mode otomatis, input gameplay, savestate restore, classifier/policy/Revision65/readiness-gate change. **Story Mode TIDAK TERBUKTI TAMAT.**

- Run seed-setter [#40485987817](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817) selesai `success` pada 2026-10-27 10:08:48 UTC (17:08:48 WIB). Artefak teks-only #12724933081, 4.003 byte, ZIP SHA-256 `74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6`: preflight VSync frame 50; listener-only max frame 60; target yang benar `0x80035DA8` mencatat progress frame 1–120 dengan `bp_hits=0`; exit 124 pada batas 35 detik; cleanup PASS. Report asli memiliki fallback PC keliru `0x800AD454`, namun raw ready line mengonfirmasi target dan fix fallback diuji pada validator #40486315324.
- Snapshot historis #40487406384 sudah digantikan. Ghidra #40498208067 selesai success pada 19:14:42 WIB; artifact #12732952776 (2.255.170 byte, ZIP SHA-256 6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6) diverifikasi pada runner oleh #40503223693, artifact #12733512950 (SHA-256 ZIP 382773f9a421835bc97c448c630a2ea5d3891309bb34094f5a67027548c03414).
ROM/disc, BIOS, Memory Card, savestate, RAM dump, dan screenshot gameplay privat tidak boleh masuk Git. Hanya repositori `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research` yang boleh diakses/diubah.

Laporan utama:
- [Laporan penutupan Step 4–10](docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md)
- [Kriteria audit langkah 1–10](docs/REVERSE_ENGINEERING_AUDIT_STEPS_1_10_2026-10-27.md)
- [Laporan runtime Step 7](docs/STEP7_RUNTIME_COLD_BOOT_RESULT_2026-10-27.md)
- [Handoff berikutnya](docs/HANDOFF_REVERSE_ENGINEERING_STEPS4_10_2026-10-27.md)

---
---

# Current checkpoint — Step 0 toolchain verified, 27 October 2026

**Langkah 0 berhasil diverifikasi pada GitHub Actions run [#40457860945](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40457860945).** Daftar pin beserta hasil uji dan catatan opsi CLI ada di [out/versions.txt](out/versions.txt); workflow reproduksibel ada di [.github/workflows/toolchain-audit.yml](.github/workflows/toolchain-audit.yml).

- Runtime yang teruji: Ubuntu 24.04, Python 3.13.18, pip 26.2.2, Eclipse Temurin JDK 25.0.4.1, Ghidra 12.2 (checksum arsip resmi terverifikasi dan `analyzeHeadless` tersedia).
- Alat yang teruji: mkpsxiso + dumpsxiso 2.30 (arsip SHA-256 diverifikasi); m2c dipin ke commit `c632946b8cfbe8fce442b522dba92dfa72f1f317`; splat 0.50.1; Unicorn 2.1.4; spimdisasm 1.42.4; binutils-mipsel-linux-gnu 2.42-2ubuntu1cross5.
- Uji Unicorn hanya smoke test membuat engine MIPS32 little-endian. Ini **bukan** pelaksanaan/verifikasi fungsi isolasi pada Langkah 9.
- Artefak run hanya laporan teks (#12712863298). Tidak ada disc image, executable game, BIOS, memory card, savestate, dump RAM atau screenshot privat dalam artefak/Git.
- Workflow adaptive player tetap dijeda. Tidak ada emulator, gameplay atau input yang dijalankan dalam putaran ini.

Catatan kompatibilitas CLI: `splat --version` berhasil; mkpsxiso/dumpsxiso mencantumkan versi lewat header `--help` (flag `--version` tidak didukung); m2c membutuhkan nama file input dan `m2c --help` dipakai sebagai verifikasi CLI; help `analyzeHeadless` mengembalikan exit 1 tetapi menghasilkan usage yang valid.

---

# Current checkpoint — static reverse-engineering audit, 27 October 2026

**This dated section supersedes older “latest checkpoint” headings below.** It records documentation/static-analysis progress only; it does not resume the adaptive player.

- Remote main before documentation updates: `62a4c114b7ac7a55ae9eb6d91bc4c9bfaef1c2ef`. Static Step 5 Actions run [#40449144521](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40449144521) succeeded on that source SHA. Main executable Ghidra/static DATA.BIN run [#40442572534](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40442572534) also succeeded.
- Audit report for the requested **Steps 1–10**: [docs/REVERSE_ENGINEERING_AUDIT_STEPS_1_10_2026-10-27.md](docs/REVERSE_ENGINEERING_AUDIT_STEPS_1_10_2026-10-27.md).
- Permanent Ghidra/m2c output for four same-address RNG callers: [out/step5/STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md](out/step5/STEP5_GHIDRA_M2C_COMPARISON_2026-10-27.md). Current logic index: [out/logic.md](out/logic.md).
- Step status: 1 **SELESAI** (inventory based on prior extraction plus runner validation); 2 **SELESAI**; 3 **SELESAI**; 4 **SELESAI in main-EXE static scope**; 5 **SELESAI for four selected RNG callers**; 6 **SELESAI SEBAGIAN**; 7 **SELESAI SEBAGIAN**; 8 **SELESAI SEBAGIAN**; 9 **TERBLOKIR** (no validated isolated MIPS/Unicorn run); 10 **SELESAI SEBAGIAN**.
- VERIFIED static RNG: LCG at 0x80035D78, state at 0x800A3118, four direct-JAL callers in the main EXE. Runtime seed/indirect callers unknown.
- DATA.BIN entry 1 base 0x800D0000 and entry 0 base 0x800AD000 remain **hypotheses**, not runtime-confirmed. Threshold/target references and setter cross-references are static only; target/record field semantics and candidate delta fields +0xB30/+0xB38/+0xB40/+0xB44 remain unresolved. Do not call any delta a barrier cost or infer a universal Story Mode win rule.
- GitHub Actions status queries returned zero in-progress and zero queued runs. No gameplay/player workflow was dispatched in this audit; no gameplay inputs, save-state restores or emulator runs were performed. The adaptive player remains paused; keep Revision65 marker, classifier/policy, readiness gate, and `barrier_level_selection = WAIT` unchanged. Story Mode completion is **not proved**.
- ROM, BIOS, Memory Card, savestates and private gameplay screenshots remain outside Git. Ghidra/m2c artefacts archived in the new Step 5 report are text decompilation/analysis output only.

---

# Latest checkpoint — one-shot submenu diagnostic stopped before input (25 October 2026)

- The one authorized diagnostic [#40144220503](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40144220503) failed during the first preflight capture. Checkpoint restore event passed, but capture failed with `sh: 1: xwd: not found`; no screenshot frames or F20 parity result exist.
- Runner-only artifact analyses [#40144372685](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40144372685) and [#40144439400](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40144439400) verified the failure text. They report no RIGHT press/release record. No gameplay input was sent and no A/B outcome was observed.
- The failed capture environment omitted the package providing `xwd` (install `x11-apps` in a future runner setup and preflight `command -v xwd`, `command -v convert`, and a bounded root capture before restoring state).
- Temporary diagnostic/analysis workflows and selectors were removed. No gameplay retry was started; another restore/input attempt needs fresh explicit user approval.
- Full runner-only audit: [docs/ONE_SHOT_SUBMENU_RIGHT_AB_RESULT_2026-10-25.md](docs/ONE_SHOT_SUBMENU_RIGHT_AB_RESULT_2026-10-25.md).
- Preserve cue UNKNOWN; `barrier_level_selection = WAIT`; readiness NO-GO; Story Mode NOT COMPLETE; Revision65 marker blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` unchanged; cue token absent.

---

# Latest checkpoint — corrected runner-only control-probe inspection (25 October 2026)

- Corrected runner inspection [Actions run #40141018663](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40141018663) completed successfully. Artifact #12308661246 digest matched GitHub metadata. All ten same-checkpoint pre frames are identical; UP/DOWN/LEFT/RIGHT post frames are identical to NONE despite successful input readbacks. CIRCLE changes the whole frame, but no explicit state label is present.
- Captures are 320×240. Japanese/English OCR on the three unique images was garbled; the checkpoint state and any submenu cue remain unverified. This artifact does not qualify as a same-start `barrier_level_selection` target A/B.
- A first corrected run #40140914545 stopped at a Pillow diff-statistics bug; fixed and completed in #40141018663. No emulator, gameplay input, restore, player workflow, tests, savestate access, local artifact download, or private-evidence commit occurred. All artifact content processing happened on the Actions runner.
- Temporary workflow and selector removed after the run. Full details: [triage report](docs/NON_PLAYER_ACTIONS_ARTIFACT_METADATA_TRIAGE_2026-10-24.md).
- Session-start usage: primary 30-day window 55% used / 45% remaining; secondary unavailable.
- Preserve cue UNKNOWN; `barrier_level_selection = WAIT`; readiness NO-GO; Story Mode NOT COMPLETE; Revision65 blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` unchanged; cue token absent.

---

# Latest checkpoint — one runner-only control-probe artifact inspection (25 October 2026)

- One explicitly authorized runner inspection completed successfully: [Actions run #40110571330](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40110571330). Artifact #12308661246 was downloaded only to the runner; size/digest matched GitHub metadata.
- The artifact describes ten branches from one checkpoint, with identical pre-frame hashes. Captures are 320×240. Every non-CIRCLE post frame matched NONE; CIRCLE differed. The checkpoint state remains unknown. The OCR/image-analysis code skipped the captures because it only accepted 1280×800, so the result is inconclusive for the submenu cue.
- No savestate was present/opened. No emulator, gameplay input, restore, player workflow, tests, local artifact download, or private-evidence commit occurred in the inspection.
- Do not run a corrected inspection without separate authorization. Details: [triage report](docs/NON_PLAYER_ACTIONS_ARTIFACT_METADATA_TRIAGE_2026-10-24.md).
- Usage at this session start: primary 30-day window 42% used / 58% remaining; secondary unavailable.
- Preserve cue UNKNOWN; `barrier_level_selection = WAIT`; readiness NO-GO; Story Mode NOT COMPLETE; Revision65 blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` unchanged; cue token absent.

---

# Latest checkpoint — non-player Actions artifact metadata screen (24 October 2026)

- Session-start `main` HEAD verified at `77f8da107236155b48ffa523c1c47dbb92311131`; ten newest Actions were completed. Latest overall monitor #40102319836 succeeded on older source `2a5fa920...`; latest classifier regression #40071317759 succeeded on `c0b7d489...`. Neither is gameplay evidence.
- Usage: primary 30-day window 39% used / 61% remaining; secondary window unavailable.
- Metadata identified one unconfirmed lead outside the adaptive-player set: control-probe run #39513285641 / artifact #12308661246. Its workflow samples ten button/no-input branches from a shared checkpoint, but run metadata does not reveal that checkpoint's game state. Do not treat it as submenu evidence.
- Neighboring barrier DOWN probes (#39618670884 / artifact #12352978983 and #39619671384 / artifact #12353768685), the single barrier-confirm run #39617444912 / artifact #12354275022, and roulette artifacts #12351098551, #12352271884, #12386841383 were already documented; not re-audited.
- No Actions runner session or existing safe runner-side artifact inspection path is available. The artifact-download connector returns bytes to the caller, so contents were not fetched. Do not dispatch/rerun a workflow solely for inspection.
- Full metadata and exact continuation gate: [docs/NON_PLAYER_ACTIONS_ARTIFACT_METADATA_TRIAGE_2026-10-24.md](docs/NON_PLAYER_ACTIONS_ARTIFACT_METADATA_TRIAGE_2026-10-24.md).
- Required state unchanged: target cue UNKNOWN; `barrier_level_selection = WAIT`; readiness NO-GO; Story Mode NOT COMPLETE; Revision65 marker `3754a6ddf45a7570c053d9c149b6d80b0862a127` unchanged; cue token absent. No emulator, restore, player workflow, gameplay input, tests, or private evidence commit.

---

# Prepared handoff checkpoint — runner-only artifact continuation (24 October 2026)

- Current `main` HEAD before this documentation refresh: `463e94c9c6a9840226b5fa8cc3fe48645376d2b1`.
- Latest Actions checked: 12 newest runs all completed. Latest monitor #40102319836 is `success` on older source `2a5fa920...`; latest classifier regression #40071317759 is `success` (35 tests) on `c0b7d489...`. No recent active run; neither result is new gameplay evidence.
- Usage checker at handoff preparation: 30-day window 38% used / 62% remaining; secondary window unavailable.
- Durable user boundary: process artifact contents **only on a GitHub Actions runner**. Do not download or extract artifact contents onto the user's laptop/local Codex workspace. If runner-side processing is unavailable, use metadata/repository text only and state the limitation.
- The adaptive-player artifact inventory/triage is complete for 66 runs (64 with artifacts); no qualifying same-start submenu A/B was found among 17 previously uncited artifacts. See `docs/REMAINING_PLAYER_ARTIFACT_TRIAGE_2026-10-24.md`.
- State remains target cue UNKNOWN; `barrier_level_selection = WAIT`; adaptive readiness NO-GO; Story Mode NOT COMPLETE. Revision65 marker blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` is unchanged and cue token absent.
- No emulator, gameplay input, player workflow, or tests ran during this preparation.

## Next chat task
Read `STATUS.md`, `ANALYSIS_LOG.md`, `docs/LEVELUP_SUBMENU_CUE_AUDIT_2026-10-24.md`, this handoff, and the remaining-artifact triage report. Verify HEAD and Actions again. Then use GitHub metadata/repository text to identify any **existing** authenticated non-player Actions artifacts that could contain a same-start submenu A/B. Inspect actual artifact contents only through an already available safe runner-side process; do not run a gameplay workflow or dispatch a new workflow just to download evidence. If no suitable runner-side path exists, stop at metadata and report the exact limitation. Never fetch artifact bytes to the laptop. Preserve all cue/readiness/completion/marker gates.

# Latest checkpoint — remaining offline artifact triage (24 October 2026)

- Audit-start `main` HEAD verified at `8fa1b66314dc717e769899bd94a699c2039c3743`, matching the supplied checkpoint.
- Latest Actions at audit start: monitor #40102319836 succeeded on older source `2a5fa920...`; latest classifier regression #40071317759 passed 35 tests on `c0b7d489...`. Neither indicates player progress.
- Usage at session start: primary 30-day window 19% used / 81% remaining; secondary window unavailable.
- Screened 66 adaptive checkpoint-player runs; 64 had artifact metadata and 17 artifacts were not cited in the four continuity docs. The three candidate pairs/sequences are all out of scope for the target submenu: #39767083708 / artifact 12420512625 starts in `menu_or_unknown_choice`; #39877412316 / artifact 12469530414 starts in `card_selection`; #39904672868 / artifact 12479814966 is sequential checkpoint continuation. Other 14 manifests do not contain a complete matched-start submenu A/B. Details: [remaining artifact triage](docs/REMAINING_PLAYER_ARTIFACT_TRIAGE_2026-10-24.md).
- No emulator, restore, continuation, player workflow, gameplay input, or tests ran. Savestate contents/screenshots were not opened. No private evidence was added to Git.
- **Required state unchanged:** target cue UNKNOWN; `barrier_level_selection = WAIT`; adaptive readiness NO-GO; Story Mode NOT COMPLETE; Revision65 marker blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` unchanged; cue token absent.
- Next: retain UNKNOWN/WAIT unless a distinct already-authenticated artifact outside this screened set provides same-start submenu evidence. Do not bypass the cue gate. Consider a new chat at the next work-stage boundary to conserve tokens and monthly usage.

---

# Latest checkpoint — adaptive Story Mode autonomy gap review (24 October 2026)

- Repo boundary: only `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research` was accessed or changed.
- Audit baseline: `main` HEAD `9acbd5eed24bdc81165358d63ed594600dae488c`, a documentation-only child of the prior verified checkpoint `2a5fa920ab544f125041f3fefd8f202ab702601b`.
- Latest code policy remains classifier v0.4.0. Calibrated actions are scoped: dialogue → START; barrier choice → CIRCLE only when YES is visibly highlighted; stable revealed-card detail → CIRCLE only with its confirm glyph; map directions are bounded; roulette waits one window before a contextual CIRCLE. `barrier_level_selection` stays WAIT. Battle, unknown menu, map transition, and unknown states stay WAIT.
- The player workflow is a bounded experiment runner: at most two 180-frame cycles per invocation, five external X11 observations per cycle, press/release readback, and post-exit checkpoint validation. Its progress report only records a map-to-dialogue/battle transition. The current classifier/runner does not establish Story Mode ending or completion.
- Hard blockers to autonomous completion: target cue in the nested barrier submenu is still UNKNOWN; battle policy and result/win/loss classification are untrained; no authenticated ending/results evidence or completion detector exists. More cycles would extend a run without resolving these blockers.
- Actions: latest monitor [#40102319836](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40102319836) succeeded on older source `2a5fa920...` and reports player #39975090690 as `EXPECTED_GATED_SKIP_NO_GO` with no player artifact. Latest classifier regression [#40071317759](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40071317759) passed 35 tests on code checkpoint `c0b7d489...`; it is not a Story Mode completion run. All 12 newest runs were completed when inspected.
- This turn was a static source/workflow review. No emulator, restore, player workflow, gameplay input, marker change, private artifact, or test run occurred. Revision65 marker remains blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`.
- **Required state remains:** target cue UNKNOWN; `barrier_level_selection = WAIT`; adaptive readiness NO-GO; Story Mode NOT COMPLETE; cue token absent.
- Next: inspect only distinct existing authenticated artifacts not already documented for same-start-state target A/B or battle/result evidence. Add policy only when authenticated action/control evidence distinguishes an action from WAIT. Keep unsupported battle/result/ending states fail-closed. Do not enlarge the runner or enable Story Mode until the cue, combat/terminal states, checkpoint path, and stop-on-unknown behavior have evidence.

---

# Latest verified checkpoint — Revision62 matched-state submenu audit remains inconclusive (24 October 2026)

- Audit baseline: live `main` HEAD `2a5fa920ab544f125041f3fefd8f202ab702601b`. The latest 12 Actions runs were completed. Latest run [#40102319836](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40102319836), the scheduled monitor, succeeded; its report identifies player run #39975090690 as `EXPECTED_GATED_SKIP_NO_GO`, with no player evidence artifact. Monitor success is not player progress.
- Latest code regression [#40071317759](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40071317759) succeeded with 35 unit tests and all workflow steps, including the historical Revision62 fail-closed frame check. No tests were rerun for this documentation-only audit.
- Newly inspected for the target-cue question: Revision62 run [#39940196133](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39940196133), private artifact `12495906030`. Downloaded ZIP size `11,441,461` bytes and SHA-256 `b07efa5e448a78ce9f81392a094e645d9089a50baabadbca64646615cff83270` match GitHub artifact metadata.
- Its A/B report records pixel-identical F20 starts (`1,024,000` pixels), common parent `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`, and `barrier_level_selection` in both branches. The action branch sent LEFT at F30–F38 then Circle at F70–F78, with press/release readbacks passing; control stayed WAIT with no input. Both card clones have SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- Authentic screenshots show `レベルアップする結界をえらんでください` (Pilih penghalang yang akan dinaikkan levelnya) and the same confirm/back footer through the sampled frames. LEFT changes the view; after Circle, no unique tile-attached focus cue or matching tile-specific information-panel change is visible. The pink `60` badge is exposed differently because the fixed HUD occludes the branches unequally, so its visibility is not a controlled selection cue. Artifact-reported broad action/control differences at F60/F100/F110/F180 are `693755/693655/693270/693882` pixels and do not isolate a tile cue.
- Candidate screening: Revision47 artifact `12464698050` / run #39868722262 starts at `roulette`, so it is outside the level-up submenu audit; its existing documented result was not repeated. Revision62 was already a classifier regression fixture; this update adds only the visual target-cue assessment.
- **VERIFIED:** Revision62 has a matched initial state and logged LEFT→Circle inputs; screenshots retain the submenu state and do not show a qualifying target cue. **HYPOTHESIS:** the large differences are consistent with view movement, character animation, and HUD unocclusion. **UNKNOWN:** the intended target tile and its unique cue.
- Preserve `barrier_level_selection = WAIT`, target cue **UNKNOWN**, adaptive-player readiness **NO-GO**, Story Mode **NOT COMPLETE**, and the consumed Revision65 marker blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`. Keep the verified-cue marker token absent.
- This audit read only authentic PNG/text/JSON from the private artifacts; `.sstate` entries were not opened or restored. No emulator, gameplay input, player workflow, marker edit, or private-evidence commit occurred.
- Next: continue only with a distinct authenticated same-start-state A/B where the same candidate tile is unobstructed in both branches and a repeatable tile-attached cue changes with selection, preferably with a matching tile-specific panel change. If no such artifact remains, preserve UNKNOWN/WAIT; do not bypass the cue gate.

---

# Latest verified checkpoint — Revision58 artifact triaged; target cue remains UNKNOWN / WAIT (24 October 2026)

- Audit started from live `main` HEAD `6b0a32f6c3e9bd791b701cb5d90adee9ecb0e058`; result is documented in commit created by this update.
- Newly reviewed offline: [historical player run #39905240818](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39905240818), private artifact #12480856146. Its one CIRCLE branch authentically reaches the level-up submenu by F60, but has only C01 frames F20/F60/F100/F110: no C02 control, no F180, no A/B report, and no savestate in the artifact.
- The screenshots verify the prompt `レベルアップする結界をえらんでください` (Pilih penghalang yang akan dinaikkan levelnya), not a selected tile. Frame changes concentrate in character/tile animation; they do not prove a tile-anchored selection cue. This is a new negative triage result, not a gameplay advance.
- No emulator, savestate restore, gameplay input, marker change, or adaptive-player workflow was run. No private evidence was added to Git.
- Preserve `barrier_level_selection = WAIT`, target cue **UNKNOWN**, adaptive-player readiness **NO-GO**, Story Mode **NOT COMPLETE**. Keep Revision65 marker at blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`; keep the cue token absent.
- Next step: continue offline-only search for already-existing, authenticated, same-start-state A/B artifact data. If no such artifact remains, stop rather than invent a cue or bypass the gate.

---

# Latest verified checkpoint — additional authenticated submenu A/B audit; target cue remains UNKNOWN (24 October 2026)

## Live repository and Actions state
- Live `main` HEAD before this documentation-only commit: `ed683f21f856a5def2f4a5ab9d0db09028b78500` (commit message: “Use stable audit baseline in status and next-chat handoff”). The branch ref was checked immediately before preparing this update.
- Latest Actions run: [#40087271642](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40087271642), scheduled adaptive-player monitor, `success`, completed at `2026-10-24T10:47:07Z`. Its report artifact `12557651205` says the player run was #39975090690, `completed/skipped`, with zero player artifacts and classification `EXPECTED_GATED_SKIP_NO_GO`. Monitor success is not player success.
- The ten newest Actions runs checked were all completed; none was active in that recent window. Latest code regression remains [#40071317759](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40071317759): `success`, 35 unit tests and all workflow steps passed. No tests were rerun for this documentation-only audit.

## New historical artifact review (offline only)
- [Run #39908484177, artifact 12481932174](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39908484177): authenticated `LEFT` action versus no-input/`WAIT` control from the same initial `barrier_level_selection` state. `ab-comparison-report.txt` records the two F20 images as pixel-identical (1,024,000 identical pixels). By F60, the action/control images differ in 693,755 pixels (mean absolute RGB difference 17.71671); at F100/F110/F180 they differ in 693,655/693,270/693,882 pixels. Historical runtime logs record successful LEFT press/readback and release/readback, but `state_changed=false` and the classifier remains `barrier_level_selection` / `WAIT` through F180.
- In run #39908484177, the candidate pink badge becomes more exposed in the action image while it remains partly hidden by the fixed HUD in control. An explicitly exploratory, non-classifier color mask in ROI `(525,145,660,225)` using `R>150`, `R>1.3×G`, `B>100`, and `|R−B|<100` counted action/control pixels `146/146` at F20, `1160/172` at F60, `1076/162` at F100, and `852/146` at F110. A bright-pixel mask over the prompt glyph ROI `(170,595,660,690)` had 1,658 pixels in each branch and XOR 0 at F20/F60/F100/F110. This is consistent with viewport movement/HUD unocclusion, not proof that the pink tile is selected. Because the candidate is not equally unobstructed in action and control, this A/B fails the required cue-visibility criterion.
- [Run #39909132189, artifact 12481644668](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39909132189): authenticated `CIRCLE` versus `WAIT` with a matched initial submenu state. Historical logs report a successful CIRCLE press/readback and release/readback, but no state change. Every paired C01/C02 screenshot at F20/F60/F100/F110/F180 is pixel-identical (zero differing pixels; mean absolute RGB difference 0). The pink badge is still partly obscured by HUD in both branches. This does not prove Circle can never act in another context; it provides no visual target-selection evidence here.
- [Run #39946344909, artifact 12498880615](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39946344909) was checked as an incomplete auxiliary UP→CIRCLE artifact: `C02-F180.png` and `ab-comparison-report.txt` are absent. It overlaps the previously documented camera-pan/UP context and is not counted as independent cue evidence.
- Inspection was limited to PNG screenshots, decision JSON and text logs. Savestate files were not opened, read or restored. No emulator, restore, continuation or gameplay input was run in this audit. No private evidence was added to Git.

## In-repository source/resource boundary
- The current Git tree includes the screenshot classifier, its offline cue-audit helper, tests and static-analysis notes. `docs/ROM_STRUCTURE.md` and `docs/RESOURCE_CATALOG.md` explicitly describe ROM/extracted binary files as local/off-repo inputs; neither `SLPS_035.53`, `DATA.BIN`, `DATA2.BIN`, nor a game renderer/UI source implementation exists in the current tree. The classifier is not the game's renderer. A source-level rendering/geometry answer therefore cannot be verified from the checked-in files.

## Evidence classification and decision
- **VERIFIED:** both additional historical A/B artifacts have matched initial submenu states; CIRCLE produces no sampled visual difference in #39909132189; LEFT changes the view while the state remains WAIT and the candidate badge's HUD occlusion differs in #39908484177. The latest monitor reports the player run as gated skip/no-go.
- **HYPOTHESIS:** scene/viewport movement and HUD unocclusion explain the increased pink-badge visibility in the LEFT action branch. This is the strongest explanation consistent with the screenshots, but it is not a verified game-renderer implementation detail.
- **UNKNOWN:** a unique target-selection cue attached to the intended barrier tile in `barrier_level_selection`.
- Keep `barrier_level_selection = WAIT`; adaptive-player readiness **NO-GO**; Story Mode **NOT COMPLETE**. Keep `experiments/.run-storymode-adaptive-player` at Revision65 blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` and keep `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` absent.

## Minimum evidence still needed
A distinct, authenticated, same-start-state action/control A/B where the same candidate tile is clearly and unobstructedly visible in both branches, and a cue uniquely attached to that tile changes reproducibly with its selection (preferably focus indicator plus a matching tile-specific information-panel change). Runtime input/readback and no-input control logs must match the images; screenshot sets must not be duplicates. Until this exists, do not mutate the marker, enable the cue token, or send input through the gate.

---
# Latest verified checkpoint — distinct Revision59 offline audit remains negative for barrier target cue (24 October 2026)

## Current repository and Actions verification
- Audit baseline: `main` HEAD `d253a0f8ef8c7eb5b5acc618314c03acc70c86f1`; code/test checkpoint preserved: `c0b7d48933d37f59914d82a4bfeab4100d836a1e`. The Revision59 audit result was first recorded in [commit `15cd1fb8bed5dffa104c64243c91ce18409bcf7f`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/15cd1fb8bed5dffa104c64243c91ce18409bcf7f). Verify the live `main` HEAD and latest Actions before further work.
- Latest relevant regression remains [GitHub Actions #40071317759](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40071317759), success: 35 unit tests and all workflow steps passed. No regression rerun was needed for this documentation-only audit.
- The ten most recent workflow runs returned by the Actions API were all completed; no active run appeared in that latest-run window.

## New offline evidence examined
- Distinct historical source: adaptive-player run [#39907655833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39907655833), private artifact `12482055310` (Revision59). Screenshot PNGs, decision JSON, and textual run logs were examined offline. Files with savestate extensions were not opened or used; no emulator, restore, continuation, or gameplay-input workflow was launched.
- This run is not an equivalent-state A/B: C01 starts at `barrier_choice` and a Circle confirmation at F20 transitions it to `barrier_level_selection` by F60; C02 starts already at `barrier_level_selection`, and its Circle press did not yield an observed state transition. Therefore cross-branch differences cannot be treated as target-selection evidence.
- In the same calibrated red-mask style as the prior audit, the candidate badge-ring counts at F60/F100/F110/F180 were C01 = `0/67/59/0`, C02 = `52/67/67/64`. All stay below the unknown-context ceiling of 100 and are far below the known positive map-UP reference of 811. The statistics-panel gold-mask footprint around the comparison ROI remained approximately 2,559–2,566 pixels, below the 5,000-pixel map-positive threshold. The bright-text mask in the submenu instruction-panel ROI changed by zero pixels across sampled within-branch submenu frame transitions.
- These are offline negative checks using a map-calibrated reference, not a new universal detector. Combined with the mismatched C01/C02 starting states, generic unchanged submenu prompt/footer, and absence of a matching tile-specific stats-panel composite, they do not identify a unique selected barrier.

## Decision and guardrails
- `barrier_level_selection = WAIT`; independent submenu target cue = **UNKNOWN**.
- Adaptive-player readiness = **NO-GO**; Story Mode = **NOT COMPLETE**.
- Keep `experiments/.run-storymode-adaptive-player` untouched at consumed Revision65 blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`; keep `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` absent.
- Revision64/65 remain pixel-identical duplicate visual evidence and were not counted independently. Revision56 card-confirm A/B supports only the card-detail state, not this submenu.
- No ROM, BIOS, Memory Card, savestate, screenshot, or private evidence was added to Git. The inspected repository contains the screenshot classifier and cue-audit code, not the game’s UI-rendering source or a checked-in game executable suitable for renderer/source-level analysis.

## Next offline action
Search only existing authenticated artifacts for a matched-starting-state action/control comparison where the same candidate barrier remains visible without HUD occlusion. If no such historical evidence exists in the allowed repository artifacts, retain UNKNOWN/WAIT and document that obtaining a new observation would require a separately authorized, gate-reviewed experiment. Do not alter the Revision65 marker, add the cue token, or launch gameplay. For future Story Mode dialog, use START—not Circle—to skip. Translate every Japanese string beside the original in Indonesian.

---

# Latest verified checkpoint — revealed-card Circle policy passes authenticated A/B; barrier cue still UNKNOWN (24 October 2026)

## Code, tests, and authentic evidence

- **Code/test checkpoint:** `c0b7d48933d37f59914d82a4bfeab4100d836a1e`; classifier version **0.4.0**.
- **GitHub Actions:** [#40071317759](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40071317759) — **success**; 35 unit tests in 5.370 seconds; all workflow steps passed, including prior authentic screenshot regressions and the new Revision56 action/control verifier.
- The new regression uses only previously authenticated private artifact **12480355608**, source run [#39904097181](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39904097181). It does not run an emulator or send gameplay input.
- At F20 the CIRCLE-action and no-input-control screenshots are pixel-identical. At F60 the action/control images differ in **127,598 pixels**, with mean absolute RGB difference **9.04858**. The historical runtime log confirms a CIRCLE press/readback on the action branch and zero input on the control branch. The action branch proceeds from the card-detail screen to a dialogue and then the map; the no-input branch stays on the card-detail screen through F180.
- The first implementation attempt [#40071223499](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40071223499) failed one synthetic test because its confirm-glyph region included the orange/gold bottom-panel border. The ROI was narrowed to `(1030,665,1105,712)`; the corrected regression above passes.

## Policy change supported by that A/B

The agent now emits `card_selection_detail` and recommends **CIRCLE** only when the blue/white revealed-card artwork meets its calibrated conditions **and** the small lower-right red Circle-confirm glyph region is present (red-mask ratio ≥ 0.12). Similar card artwork without a clear glyph is classified separately as `card_selection_detail_unconfirmed` and returns **WAIT**. Revision53 authentic action/control evidence also passes this updated boundary: the intermediate F60 reveal without a clear confirm glyph remains WAIT, while the stable detail frames with the glyph can recommend CIRCLE.

Japanese text in the authentic card evidence: `ゲットする札をえらべ!` (Pilih kartu yang akan didapatkan!); `守` (Lindungi/Bertahan); `防御集中` (Konsentrasi Pertahanan); `気合いをいれて守る。防御技の消費チャクラが0になります。` (Bertahan dengan penuh semangat. Konsumsi chakra untuk teknik pertahanan menjadi 0.).

## Safety boundary unchanged

- `barrier_level_selection = WAIT`; unique nested-submenu target cue remains **UNKNOWN**.
- Adaptive-player readiness remains **NO-GO**; Story Mode remains **NOT COMPLETE**.
- The marker `experiments/.run-storymode-adaptive-player` remains the consumed Revision65 blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`; do not change or replace it. `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` remains absent.
- The regression continues to report `LEVELUP_TARGET_CUE_REGRESSION=PASS` only as a fail-closed policy test: map UP ring/panel/text = 811/8,312/635; map WAIT = 62/8,629/15; submenu UP = 66/2,452/3,221; submenu WAIT = 67/2,566/39. Neither submenu context passes the map-only ring/panel/text composite.
- No emulator, restore/continuation, or gameplay-input run was launched during this session. Historical private artifacts were analyzed temporarily; no ROM, BIOS, Memory Card, savestate, screenshot, or private evidence was added to Git.

**Next:** continue offline toward a unique tile-anchored target cue in the level-up submenu, or source-level analysis of UI rendering. Do not reuse duplicate Revision64/65 frames or infer selection from the pink badge, camera movement, the character/kunai sprite, or the generic Circle footer. Do not authorize barrier-selection input until independent cue evidence and the marker/allowlist/pre-download gate have been reviewed. For Story Mode dialogue, use **START**, not Circle.

---

# Latest verified checkpoint — historical LEFT→Circle regression green; readiness still NO-GO (24 October 2026)

## Additional authenticated regression — verified pass

**Workflow/test commit:** `e0f3c49f735a7a518399cef1457e8233affec43e`. **Actions:** [#40069923244](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40069923244) — `success`; 34 unit tests in 5.114 seconds and all workflow steps passed.

The regression now downloads historical private artifact `12495906030` from run [#39940196133](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39940196133), an independent LEFT→Circle A/B. Its ten authentic frames (C01/C02 at F20/F60/F100/F110/F180) all classify as `barrier_level_selection` / `WAIT`: `AUTHENTIC_HISTORICAL_LEFT_CIRCLE_BARRIER_POLICY=PASS checked=10 all_wait=true`. This is classifier safety coverage, not proof of target selection.

Across the UP action artifact from run #39942178665 / artifact `12496637328`, the pink `60` badge is fully visible at F60, but candidate ring counts remain **66 / 58 / 66 / 80** at F60/F100/F110/F180, below the red-ring rejection ceiling 100 and far below the known map-UP cue count 811. The left-action artifact has the badge partly occluded by the fixed HUD. Neither context supplies a unique tile-selection indicator or a tile-specific stats panel.

**Safety state unchanged:** `barrier_level_selection = WAIT`; target cue **UNKNOWN**; adaptive readiness **NO-GO**; Story Mode **NOT COMPLETE**. Marker Revision65 remains consumed and unchanged; cue token remains absent. This was a regression-only change—no emulator, restore, continuation, or gameplay input was run.

**Next:** continue only with distinct existing authenticated evidence or source-level UI analysis that can prove an independently unique submenu target cue. Do not relax the cue gate, alter the consumed marker, or launch gameplay while it remains unknown.

---
## Previous checkpoint — Revision64/65 visual duplicate; submenu target cue remains UNKNOWN (24 October 2026)

## Offline cross-run comparison

New audit: `docs/LEVELUP_SUBMENU_CUE_AUDIT_2026-10-24.md`.

Private, authenticated emulator artifacts from Revision64 run #39942178665 (artifact 12496637328) and Revision65 run #39947481094 (artifact 12498688466) were compared offline. All ten corresponding C01/C02 frames at F20/F60/F100/F110/F180 are pixel-identical across the two artifacts: zero differing pixels and zero mean absolute RGB difference in each pair. Revision64 logs only UP@F30; Revision65 logs UP@F30 plus Circle@F70 with successful PAD readback, but its captured frames show no rendered difference from Revision64. Thus these artifacts are not independent visual confirmations, and Circle delivery did not visibly select/confirm a target in the sampled observations.

The badge/pulse, camera/HUD exposure, character pose, kunai sprite, and the map-only ring-plus-stats-panel signature still do not uniquely identify the nested submenu target. Japanese prompt: `レベルアップする結界をえらんでください` (Pilih penghalang yang akan dinaikkan levelnya); footer: `けってい` (konfirmasi/pilih, Circle), `もどる` (kembali, X).

**Decision unchanged:** `barrier_level_selection = WAIT`; target cue **UNKNOWN**; adaptive readiness **NO-GO**; Story Mode **NOT COMPLETE**. Revision65 marker remains consumed and unchanged; cue token remains absent. No player/emulator/input/restore run was launched in this audit. No private assets were committed.

**Next:** inspect only a distinct existing authenticated artifact where the candidate tile is visible in action and control without fixed-HUD occlusion. Do not reuse Revision64/65 as independent evidence, add the cue token, alter the marker, or launch gameplay before the existing gate is independently satisfied.

---
## Previous verified checkpoint — pink badge pulse excluded as a unique cue (24 October 2026)

## Offline authentic screenshot regression — 24 October 2026

**Code/test commit:** `885d9889215a4fdca6b276daadd8a431f8177c51`. **GitHub Actions:** [run #40066679351](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40066679351), completed `success`; **34 unit tests / 3.176 seconds**, all 15 workflow steps passed. It used only existing private/authenticated screenshots from Revision65 A/B (artifact `12498688466`, source run #39947481094) and map UP-vs-WAIT (artifact `12428777970`, source run #39786019434). No gameplay, emulator, restore, or continuation was run.

### New negative discriminator: badge pulse is not selection

A regression measures the mean RGB of the pink badge's interior in same-phase frames and compares map UP with map WAIT. The same animation/pulse appears in both states, so color/brightness alone cannot uniquely identify a selected target.

| Frame | UP mean RGB | WAIT mean RGB | Euclidean RGB distance |
|---|---|---|---:|
| F60 | (237.5, 39.2, 140.7) | (235.1, 37.5, 138.4) | 3.74 |
| F100 | (215.6, 69.1, 118.5) | (213.4, 65.6, 116.2) | 4.79 |
| F110 | (206.7, 65.1, 103.4) | (202.3, 62.8, 101.0) | 5.48 |
| F180 | (238.2, 39.4, 141.1) | (237.7, 39.5, 140.8) | 0.62 |

The largest same-frame distance is only **5.48 RGB units**, below the fail-closed regression ceiling of 12.0. The helper `same_badge_pulse_across_contexts` rejects missing, malformed, non-finite, mismatched-frame, or changed-pulse data; a test also proves the pink color change cannot bypass the ring/panel composite. Workflow output: `PINK_BADGE_PULSE_REGRESSION=PASS`.

The previously calibrated context remains unchanged: map UP red focus-ring/panel/text = **811 / 8,312 / 635**; map WAIT = **62 / 8,629 / 15**; Revision65 submenu UP = **66 / 2,452 / 3,221**; submenu WAIT = **67 / 2,566 / 39**. The map-UP reference matches the conservative ring + matching stats-panel footprint + panel-text-change composite; map WAIT and both submenu branches are rejected.

The first implementation run, [#40066588970](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40066588970), failed because the workflow had loaded only F20/F60 map frames while the new pulse check also read F100/F110/F180. Commit `885d988` corrected the loader to read the full ten authentic map A/B frames; the corrected run #40066679351 passed. This was a regression-fixture defect, not a gameplay run.

## Safety decision — unchanged

- `barrier_level_selection = WAIT`; target cue in the nested upgrade submenu remains **UNKNOWN**.
- Adaptive-player readiness remains **NO-GO**; Story Mode remains **NOT COMPLETE**.
- Consumed marker `experiments/.run-storymode-adaptive-player` remains Revision65, blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`; `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` remains absent.
- The cue gate still precedes source-artifact download and PAD mutation. No player, emulator, restore/continuation, or gameplay input was launched. ROM, BIOS, Memory Cards, savestates, screenshots, and private evidence remain outside Git.
- The apparent kunai mask remains excluded from cursor/target evidence. The pink badge pulse, tile visibility after camera pan, pixel changes, and character pose are not sufficient to change the state.

**Next:** continue offline against the existing authenticated screenshots, seeking a unique submenu cue spatially attached to the candidate tile and independent of camera movement, HUD exposure, sprite pose, and badge animation. Do not change the consumed marker, add the cue token, or run gameplay until the cue is independently demonstrated and the marker, allowlist, pre-download/PAD gate, and regression are reviewed.

---

# Previous verified checkpoint — kunai proxy excluded from target cues (24 October 2026)

## Verified crop correction — 24 October 2026

**Source/test commit:** `96e9c22089e257facf2be3359ead33deed117583`. **Regression:** [GitHub Actions #40065597290](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40065597290) — `success`; 33 unit tests passed in 4.297 seconds and all 15 workflow steps passed, including authentic screenshot checks for the prior X11/card/Revision65/map evidence.

Visual inspection of the existing private/authenticated crops from Revision65 artifact `12498688466` (run #39947481094) and map UP-vs-WAIT artifact `12428777970` (run #39786019434) identified a classification error in the previous analysis: the blue/orange mask ROI `(620,295,735,390)` is part of the character's hand-held kunai/foreground sprite ROI `(540,290,750,560)`, not an independent UI pointer. Therefore the old 8.38/7.17/5.01/5.03 px motion values and pointer-to-tile distances must **not** be interpreted as cursor evidence. They are superseded as a pointer hypothesis; no target-selection signal can be inferred from this ROI.

The regression now asserts that the former proxy ROI is contained inside the foreground-sprite exclusion ROI, labels it `cursor_or_target_evidence=false` and `cue_eligible=false`, and removes the misleading pointer-centroid and screen-anchor claims. The authentic terrain/camera-pan and ring/panel audit remains unchanged: Map UP ring/panel/text = 811/8312/635; Map WAIT = 62/8629/15; Revision65 submenu UP = 66/2452/3221; submenu WAIT = 67/2566/39. The composite still rejects both submenu branches. The pink badge's +97.46 px visible-centroid shift against a +100 px scene shift remains consistent with camera pan/HUD unocclusion, not proof of target selection.

**Decision remains fail-closed:** `barrier_level_selection = WAIT`; the submenu target cue remains **UNKNOWN**; adaptive-player readiness **NO-GO**; Story Mode **NOT COMPLETE**. Consumed marker `experiments/.run-storymode-adaptive-player` is unchanged at Revision65, blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`; the cue token remains absent. No player, emulator, restore/continuation, or gameplay-input workflow was launched; all screenshots, ROM/BIOS, Memory Cards, savestates, and private evidence remain outside Git.

**Next:** continue offline with the existing authentic screenshots, examining a cue spatially attached to the actual candidate tile and independent of background motion, HUD exposure, and foreground pose. Do not add the cue token, change the consumed marker, or run gameplay before independent verification and explicit review of marker/allowlist/fail-closed gates.

---

# Offline level-up target-cue regression checkpoint — 24 October 2026

**Code/test HEAD:** `d1c0428381581b80814bebf6557f5579594bb9da`. **Regression:** [GitHub Actions #40064182088](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40064182088) — `success`, 33/33 unit tests in 4.872 seconds; all workflow steps passed, including the existing authentic screenshot checks and the new cue-composite audit.

The audit uses only existing private/authenticated screenshots from Revision65 A/B run #39947481094 and map UP-vs-WAIT run #39786019434. No player, emulator, restore/continuation, or gameplay-input workflow was launched.

| Authenticated screenshot context | Red focus-ring pixels | Stats-panel gold-frame pixels | Bright-text mask delta F20→F60 | Composite |
|---|---:|---:|---:|---|
| Map UP reference | 811 | 8,312 | 635 | Match |
| Map WAIT control | 62 | 8,629 | 15 | Reject |
| Revision65 submenu UP | 66 | 2,452 | 3,221 | Reject |
| Revision65 submenu WAIT | 67 | 2,566 | 39 | Reject |

The new conservative regression requires all three signals at once: a focus ring around the candidate tile, the expected statistics-panel footprint, and a text-mask transition inside that panel. It rejects the submenu UP false-positive: 3,221 bright-text mask changes occur in the registered ROI without the matching panel footprint or focus ring. Prompt text masks were stable (zero changed pixels) for all four F20→F60/F60→F100 UP/WAIT comparisons.

**Safety decision unchanged:** `barrier_level_selection = WAIT`; target cue in the nested level-up submenu remains **UNKNOWN**; `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` remains absent; consumed marker `experiments/.run-storymode-adaptive-player` remains Revision65, blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`, unmodified. Adaptive-player readiness is **NO-GO** and Story Mode is **NOT COMPLETE**. Fixed-sequence Story Mode and raw restore/continuation remain disabled. Private screenshots and game assets remain outside Git.

**Next step:** continue offline on existing authentic screenshots, focusing on registered tile boundaries and any independent submenu-specific target indicator. Do not replace the marker, add the cue token, or launch gameplay until the submenu cue is independently verified and the marker, allowlist, pre-download/PAD fail-closed gate, and regression are reviewed.
 
---

# Adaptive readiness checkpoint — 24 October 2026

Latest source/test checkpoint: **6d2fdc4553f5eacabf2607c19ebf69bc012c2c51**. Latest regression: [Actions run #40061967694](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40061967694), **success**, 32/32 unit tests and all workflow steps passed, including all ten authentic X11 observations and the private Revision65/map UP-vs-WAIT screenshot regression. The monitor policy hardening is included in this tested source tree; [run #40061712532](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40061712532) also passed on its then-current source.

## New offline pointer-motion discriminator

Using only the existing authenticated private PNGs from Revision65 A/B (run #39947481094) and map UP-vs-WAIT (run #39786019434), regression now measures the blue-pointer proxy's F20-to-F60 screen displacement with the same ROI and color mask used by the workflow:

- Revision65 UP: **8.38 px**
- Revision65 WAIT: **7.17 px**
- Map UP: **5.01 px**
- Map WAIT: **5.03 px**

On the same frames, UP scene registration is **+100 px** in both contexts while WAIT is **0 px**. The pink badge centroid in Revision65 moves **+97.46 px**, close to the scene shift. The proxy therefore stays nearly screen-anchored while the scene/tile pans under it. POINTER_SCENE_ANCHOR_REGRESSION=PASS verifies this motion contrast, and POINTER_TARGET_GEOMETRY_REGRESSION=PASS still shows that proxy-to-tile proximity is not discriminating. This is evidence against treating the blue proxy or pink badge exposure as a target-active cue; it is **not** proof of selection.

## Monitoring health fix

Added tools/adaptive_monitor_policy.py and integrated it into .github/workflows/naruto-storymode-adaptive-monitor.yml. The monitor only classifies a no-artifact skipped run as EXPECTED_GATED_SKIP_NO_GO when its event is a push, the commit message is known, and the message lacks [RUN-NARUTO-STORYMODE-ADAPTIVE-PLAYER]. A skipped manual dispatch, unknown commit message, marker-bearing push, completed failure, successful run without a valid evidence artifact, or overdue queued/running session remains a warning. Unit tests cover those distinctions. This prevents the known stale, intentionally gated run #39975090690 from being mistaken for gameplay failure, without misreporting it as gameplay success.

## Safety decision — unchanged

- barrier_level_selection remains **WAIT**; the submenu still has no independently demonstrated unique target cue.
- Marker experiments/.run-storymode-adaptive-player remains consumed Revision65, blob 3754a6ddf45a7570c053d9c149b6d80b0862a127, unmodified; AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1 is absent.
- Adaptive-player readiness remains **NO-GO** and Story Mode remains **NOT COMPLETE**.
- No player, restore/continuation, or gameplay-input workflow was launched for this work. Legacy fixed-sequence Story Mode and raw restore/continuation remain disabled. No ROM, BIOS, Memory Card, savestate, screenshot, or private evidence artifact was committed.

## Next step

Continue offline using terrain-registered candidate tile boundaries and the ring-plus-matching-information-panel cue. Do not edit the consumed marker or run gameplay. Only permit a new bounded experiment after a unique cue is independently demonstrated in the submenu with authentic evidence, the allowlist/fail-closed pre-download gate is explicitly reviewed, and a new marker revision is deliberately approved. Keep START for recognized dialogue, not Circle.

---

# Offline pointer geometry and character-pose exclusion — 24 October 2026

Regression-only source commit: `1ec34ac934ee62ba69fe3fe43705de1221a17196`. GitHub Actions [run #40059425253](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40059425253) completed **success** at 03:43:44 UTC / 10:43:44 WIB. All 15 workflow steps passed, including **27 tests in 2.978 s**, authentic external-X11 policy checks, card overlay/detail checks, and the existing Revision65 versus map UP-vs-WAIT screenshot regression plus the new geometry/pose checks. This commit changes only the adaptive regression workflow and its source tests. No emulator, player, restore, or gameplay-input workflow was started.

## Offline measurements on existing private screenshots

Sources are the previously stored private artifacts from Revision65 run #39947481094 and map UP-vs-WAIT run #39786019434. They were downloaded into ephemeral analysis space only; screenshot/save-state assets remain outside Git.

- The secondary blue-pointer proxy is **206.01 px** from the exposed Revision65 pink-60 badge, **76.56 px** from the pink-60 map tile in UP, and **82.83 px** from the same tile in WAIT. The map UP/WAIT distance difference is only **6.27 px**, so pointer proximity alone is not a discriminating target-active feature.
- Between Revision65 F60 and F100, terrain registration estimates **0 px** scene shift in both action and control branches. The foreground-character ROI changed **22.312%** in the action branch and **18.891%** in control, whereas a terrain-only ROI changed **1.467%** and **1.468%** respectively. Treat foreground variation as pose/animation/appearance, not evidence of target focus.
- The instruction panel and Circle/X footer remain pixel-identical from F60 to F100 in both branches (zero changed pixels each).
- Red focus-ring counts surrounding the Revision65 pink badge at frames F60/F100/F110/F180 are **66/58/66/80**, all below the calibrated rejection threshold 100. The known map selection composite remains discriminating: **811** red directional-ring pixels and a matching tile-information panel in map UP, versus **62** pixels in map WAIT and **66** around the Revision65 badge.
- Previously registered F20→F60 terrain motion remains approximately +100 px for both UP contexts and near zero for WAIT. The Revision65 badge visible centroid moves +97.46 px while the background moves approximately +100 px, consistent with camera pan and HUD unocclusion as a confound.

The current best falsifiable visual hypothesis is that an active map tile has a directional focus-arrow ring **and** the corresponding tile-information panel changes to its stats. Neither pink colour/number, a nearby blue icon, isolated pixel changes, nor foreground pose is sufficient. The map-context signature is not yet demonstrated in the nested level-up submenu, so the pink-60 badge's role as the selected upgrade target remains **UNKNOWN**.

## Gate and operational status

- Marker `experiments/.run-storymode-adaptive-player` remains Revision65, blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`, consumed and unchanged; `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` remains absent.
- Classifier policy at `barrier_level_selection` remains **WAIT**. The token gate still blocks before source-checkpoint download and before PAD mutation. Adaptive-player readiness remains **NO-GO**; Story Mode remains **NOT COMPLETE**.
- Legacy fixed-sequence Story Mode and raw restore/continuation jobs remain hard-disabled with `if: false`; input-bearing diagnostics remain manual-dispatch-only. All authentic screenshots, ROM/BIOS, Memory Cards, savestates, and private artifacts remain outside Git.
- Scheduled monitor runs #40010286618, #40034304421, and #40048510714 failed because the monitor inspects stale player run #39975090690, whose conclusion is `skipped` and which has no valid unexpired player evidence artifact. These are monitor/health alerts caused by the intentional no-go/skipped player, not evidence of new gameplay failure or progress. Do not start a player run merely to make the monitor green.

## Next step

Continue offline analysis only: use terrain-registered map coordinates, explicit tile boundaries and the existing arrow-ring/panel reference to distinguish the game pointer from scene motion; keep character/foreground masks separate from terrain registration. Add additional assertions only when grounded in the current private authenticated screenshots. Before any future input, require an independently unique submenu target cue, an explicitly revised marker, successful regression, and the existing fail-closed allowlist/gate. Do not rerun Revision65 or inject input now. For identifiable Story Mode dialogue later, use START—not Circle—and include Indonesian translation immediately beside Japanese text in parentheses.

---

# Current verified checkpoint — 23 October 2026

## Offline target-cue regression

The latest verified regression is [run #39978745505](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39978745505), source commit `1e22c1b37d0233455a5a6cf49ddf98e6e555c93c`, conclusion **success**, all 15 job steps passed. The source tests report **26 tests in 3.189 s; OK**. Authentic screenshot checks include `MAP_FOCUS_ARROW_RING_REGRESSION=PASS`, `CAMERA_SHIFT_REGRESSION=PASS`, and `REV65_BADGE_SHIFT_FOLLOWS_SCENE=PASS` with badge displacement +97.46 px versus scene shift +100 px. The known map-UP cue has 811 red-arrow-ring pixels plus a matching tile panel; map-WAIT and Revision65 submenu regions have only 62 and 66. This preserves the ambiguity decision: target role in the upgrade submenu remains **UNKNOWN**.

## Safety containment

The consumed marker remains Revision65 (blob `3754a6ddf45a7570c053d9c149b6d80b0862a127`), and the cue token remains absent. `barrier_level_selection` stays `WAIT`; readiness **NO-GO**; Story Mode **NOT COMPLETE**. The fixed-sequence Story Mode workflow and raw restore/continuation workflow are both hard-disabled with `if: false`; 11 input-bearing diagnostic jobs are manual-dispatch-only. Replacement push runs for these guarded workflows were all `skipped`.

One superseded regression, [#39978693381](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39978693381), was started on intermediate source commit `79a7fb720d2d828afa2b761c9ae66884aa8e0b8b` and eventually failed its safety-test assertion because the Python literal-newline comparison was over-escaped. The assertion was corrected in source commit `1e22c1b37d0233455a5a6cf49ddf98e6e555c93c`; [run #39978745505](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39978745505) then passed 26/26 tests and all screenshot checks. The superseded failure is regression-only—no emulator/gameplay input. No player or restore workflow is active.

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

---

# Latest checkpoint — terrain registration separates camera pan from target cue (23 October 2026)

Regression-only source commit: `563e34562f4bea0423557755a5c03b4b60077894`. Regression [#39973978654](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39973978654) completed with `success` at 15:00:04Z; run log confirms 25/25 tests and every workflow step passed.

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

## Final result — cross-context pink-60 audit regression passed (23 October 2026)

Regression run [#39952866478](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39952866478) finished with `success` at the cross-context audit commit. It passed 23 synthetic/source tests, 10 authentic X11 policy checks, 5 real card-overlay checks, 10 real revealed-card-detail checks, and the ten private Revision65 barrier-submenu frame validations. The Revision65 replay verifies C01 pink-badge ratio above threshold at F60/F100/F110/F180, C02 WAIT controls below threshold, both F20 baselines absent, and zero prompt/footer crop pixel changes F60→F100 in either branch. The report wording now distinguishes the verified barrier-value symbol in prior map context from the still-unknown role of the badge as a level-up target cursor.

This was a regression/analysis-only run. No player workflow was launched. Marker Revision65 is unchanged and consumed. Current policy remains WAIT in barrier_level_selection; readiness NO-GO; Story Mode NOT COMPLETE.


## Final checkpoint for next chat — Revision65 pink-60 meaning narrowed; readiness remains NO-GO (23 October 2026)

- Current HEAD at this note's start: `7735abe065a33bbb67c40c719530055f06971974`. Regression [#39950309113](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39950309113) finished `success`: 23 synthetic/source tests, 10 authentic X11 policy cases, 5 authentic card-overlay cases, 10 authentic card-detail cases, and 10 Revision65 barrier-submenu screenshot checks. Private screenshot replay measured action-branch badge signature versus WAIT control and found exactly zero changed pixels in prompt/footer ROIs from F60 to F100 in both branches.
- An additional direct visual cross-check compared Revision65 artifact #12498688466 with older authentic map UP-vs-WAIT artifact #12428777970. In the map context, the same pink hexagon marked `60` appears with directional red focus arrows and a data panel `結界価値` (Nilai penghalang) 60, alongside `レベル` (Level) 1 and `耐久値` (Daya tahan) 2/2. Therefore **the number/hexagon shape matches a verified barrier-value symbol in the map context**. In Revision65 barrier-level selection, the pink `60` badge appears after UP but the associated focus arrows/panel are not visible, and Circle does not change the instruction/footer. So the numeric/barrier-value context is better understood; its role as a currently selected level-up target remains UNKNOWN.
- Keep classifier action `WAIT` for `barrier_level_selection`. Do not interpret visual camera/focus changes alone as choosing the target. Revision65 is consumed; marker unchanged. Neither C01 nor C02 output checkpoint is promoted. No player attempt was launched after Revision65.
- Player workflow adds a fail-closed preflight: any future barrier-level A/B must carry `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1` to pass the source gate. Keep this token absent until a distinct target selection cue is independently identified; do not use the gate token merely to get past validation.
- Next useful research: inspect/map the presence and absence of the red directional focus-arrow signature across known map-selection and level-up screens; use only private authenticated emulator artifacts already in Actions and existing controller evidence. Before any new input experiment, define a discriminating visual hypothesis, add tests/state guards, then wait for regression success. Do not select another direction randomly.
- Current regression report wording was refined after the visual comparison to distinguish a known barrier-value symbol match from the still-unknown selection role. It triggers one final regression rerun. The marker is not touched and no gameplay run should be triggered by this change.

## Follow-up — regression repair after first Revision65 visual gate commit (23 October 2026)

Regression run [#39950014349](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39950014349) failed at the synthetic unit-test stage before any authentic-image checks ran. The failure is a static test expecting the documented cue token spelling in the player workflow; the actual fail-closed source gate exists. I also found an escaped GitHub Actions expression in the newly added artifact-download step. Both are implementation defects, not gameplay evidence. Correcting them in a follow-up commit; keep all gameplay runs blocked until regression passes. The player workflow only listens for pushes to the marker, which remains unchanged, so no player run is started by this repair.

## Revision65 indicator audit and new NO-GO gate — 23 October 2026

- HEAD verified after Revision65: `80267c92a413ed6c346bff09b28e018a22e279ff`. The latest gameplay run at audit start was #39947481094 (success) with private artifact #12498688466; regression #39947302492 (20 tests plus authentic screenshot checks) and monitor #39948007642 (success) were complete. No player run was active in the latest Actions page checked.
- Revision65 remains consumed. Do not rerun or repurpose its marker. The immutable source is Revision59 run #39907655833 checkpoint SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`. Neither Revision65 output checkpoint is promoted; independent fresh-process restore is still required.
- Authentic private images were inspected directly. C01's UP@F30 causes a conspicuous pink hexagonal badge labelled `60` to appear in a fixed ROI (x=420..540, y=175..260); it is still present in C01 F60/F100/F110/F180. The calibrated pink-pixel candidate ratio is approximately 0.1301, 0.0948, 0.0288 and 0.1334 respectively. C02 WAIT-control ratios remain below 0.01 and both F20 baselines are about 0.0021.
- The prompt `「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya)` remains visible. The footer reads `けってい` (konfirmasi/pilih) and `もどる` (kembali), with Circle and X glyphs respectively. The instruction-panel and footer crops have exactly zero changed pixels from F60 to F100 in each branch after the Circle input.
- Runtime mapping proves delivery only: UP was pressed at F30/readback true and released at F38/readback false; Circle was pressed at F70/readback true and released at F78/readback false. It does not map the in-game target cursor or explain the numeric badge. The pink `60` meaning remains UNKNOWN (target marker, resource, or other overlay not distinguished); do not call it a selection highlight.
- Action policy remains WAIT at `barrier_level_selection`. The classifier synthetic suite now includes a pink-`60` scene that must still yield WAIT. The regression workflow replays all ten authentic Revision65 screenshots privately, checks the indicator-vs-control region, and asserts the prompt/footer remain pixel-identical after Circle. A preflight gate blocks any future barrier-selection A/B unless the marker explicitly declares `AB_BARRIER_TARGET_CUE=VERIFIED_BARRIER_TARGET_CUE_V1`; this token must not be used until a unique target cue has independent visual evidence.
- Readiness is **NO-GO**; Story Mode completion is unverified and is not a readiness prerequisite. No new gameplay experiment is launched by this checkpoint. Keep ROM, BIOS, Memory Cards, savestates, screenshots and private artifacts out of Git.

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

## CURRENT CHECKPOINT — revision55 restore-only currently running (23 October 2026, 07:40 WIB)

See [docs/HANDOFF_ADAPTIVE_PLAYER_2026-10-23.md](docs/HANDOFF_ADAPTIVE_PLAYER_2026-10-23.md) for detailed evidence and continuation.

Revision54 [#39878936772](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39878936772) independently restored the revision53 face-up card-detail state; SHA `219d03ab90b594c27430f91460319c6a4c9a3b05b6463871406ac777873bedf8`, 21,162,165 bytes, v4. Revision55 restore-only run [#39879445016](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39879445016) is **in progress** and must finish before any card-input A/B is launched. Do not change the marker or start concurrent player runs. The A/B question remains whether a second CIRCLE confirms/acquires the `防御集中` card; this is UNKNOWN.

If run #39879445016 remains stuck, its 20-minute job timeout implies a stop by about 07:59 WIB. Verify the actual five private screenshots, zero-press guard, source load event, and output checkpoint size/header/SHA when it finishes. Story Mode remains **NOT COMPLETE**.

Permanent boundaries: only the Naruto research repository; no other repos; game assets and genuine screenshots remain private/out of Git; START only for true Story Mode dialogue.

---

## ULTIMATE OBJECTIVE — unattended adaptive Story Mode finisher (23 October 2026)

The project goal is not to keep asking ChatGPT for individual inputs or to leave this conversation open. Build a durable player/orchestrator in this repository that can continue across bounded GitHub Actions sessions from independently verified private checkpoints, adapt to observed screens, safely handle dialogs/menus/cards/board/battle, record progress, recover from job/emulator termination, and keep chaining sessions until authentic Story Mode ending evidence is observed. Closing the chat must not stop an already-running Actions job; after the current safety fixes, implement automatic bounded continuation in Actions rather than depending on a human or an active chat to start each segment.

Current maturity: the policy/checkpoint/capture cycle is partly working and revision50 has made partial progress, but the autonomous finisher is NOT done. Do not confuse single-run success with full Story Mode completion. The next immediate blocker is the restore-only no-input safety invariant below; only after that is tested should gameplay resume. Then validate the card overlay on the real screenshot, restore the revision50 output, identify card-screen semantics conservatively, and implement/verify a persistent state machine plus automatic sequential continuation. Use actual emulator images, checkpoint SHA manifests and ending detection. Keep ROM/BIOS/savestates/Memory Cards/gameplay screenshots private and out of Git. Story Mode dialogue is skipped using START only. The only permitted repository is this research repo.

---

## CHAT-TRANSFER CHECKPOINT — adaptive Story Mode player is NOT complete (23 October 2026)

**Direct answer:** the automated adaptive player has made verified partial progress, but it has NOT autonomously completed Story Mode. No authentic game-ending/ending-results screenshot has been verified. No player Actions run is currently active.

### Latest player run: revision50, partial gameplay progress
Run [#39872449049](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39872449049) ended with success; its private artifact #12467281563 was audited. The adaptive policy restored the roulette→board checkpoint, observed the board at F20, sent one DOWN (button press/release readback passed), and the visible move counter changed from 3 to 1 by F60. At F100/F110 an Iruka (`イルカ`) dialogue appeared and the agent skipped it with START, as required. At F180 three card backs overlapped the board. This is partial progression, not a finished Story Mode.

Output candidate from #39872449049: 21,162,772 bytes; header `PCSX-Redux SaveState v4`; SHA-256 `017c6601ad71f7e420cc5406f20c68367497c416663f07065a862f1484b2c9f7`. It has NOT been independently restored. Do not promote it yet.

### Latest classifier regression: passed, but semantic limitation remains
Regression run [#39873273913](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39873273913) completed success at commit `d8082dcdfa8997df65cddf9e6d0d8d806c8da927`. It ran 9 unit tests (including synthetic three-card overlay → `card_selection` / WAIT) and checked 10 authentic screenshots successfully.

Important nuance: the authentic run50 F180 card-overlay screenshot is still labeled `map_after_move` by the offline classifier, with action WAIT, rather than `card_selection`. Thus the synthetic guard test passes and the authentic current frame did not authorize a button press, but semantic recognition of this real overlay is NOT yet VERIFIED. Do not state that the real card screen is correctly classified just because regression succeeded.

### Critical next task before run51
The workflow code still allows normal policy to act at later frames when `RESTORE_TEST=1`; run50 itself continued from F20, so the marker name “restore-only” was not a guarantee of no-input behavior. Before starting a new player:
1. Modify `.github/workflows/naruto-storymode-adaptive-player.yml` so `RESTORE_TEST=1` suppresses all inputs throughout the session—including normal frame-30 policy actions and the frame-110 START dialogue path—while still taking the five screenshots and writing/validating an output checkpoint.
2. Add a regression test proving restore-only never calls any button input even if the classifier recommends DOWN/START/CIRCLE.
3. Re-run regression tests. Do not launch the player until these tests pass.
4. Then set the marker to revision51 restore-only from run #39872449049 / artifact `naruto-storymode-adaptive-player-private` / `adaptive-cycle-01-f180.sstate` / SHA `017c6601ad71f7e420cc5406f20c68367497c416663f07065a862f1484b2c9f7`. Require F20 card-overlay screenshot, explicit `ExecutionFlow::SaveStateLoaded`, five authentic 1280×800 captures, exit accepted, and external output checkpoint size/header/SHA validation. Keep that new output unpromoted until independently restored.
5. After successful restore-only test, determine reliable card overlay behavior on actual image before selecting/confirming any card. Never use Circle to skip dialogue; START only.

Workflow marker currently remains revision50 restore-only:
```
MODE=ADAPTIVE
SOURCE_RUN=39870243073
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=7f8771873b075830b3dadf14ef47a343ceb0f026790b9beba2af0bfb614debea
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=CIRCLE
LOOP_CYCLES=1
REVISION=50
```
Do not trigger it as-is because restore-only input suppression needs fixing first.

Permanent constraints: only repository `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`; never touch runner/Tile Duel or other repos. ROM, BIOS, savestates, Memory Card, and genuine X11 gameplay images stay private/out of Git. Any Japanese text must be immediately followed by Indonesian translation in parentheses. Story Mode remains **NOT COMPLETE**.

---

## CHAT-TRANSFER CHECKPOINT — classifier fix in regression, no active player run (23 October 2026, latest check ~06:46 WIB)

No Story Mode player run is active. The latest player run is revision50, [#39872449049](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39872449049), completed success; private artifact #12467281563. It restored the roulette→board candidate checkpoint and, because RESTORE_TEST still permits policy input after the F20 observation, continued gameplay: observed board at F20, policy sent DOWN (true/false readback), visible counter moved from 3 to 1 by F60, Iruka (`イルカ`) dialogue at F100/F110 with START dialogue skip verified, and three card backs overlaying the board at F180. The output candidate from the run is size 21,162,772 bytes, PCSX-Redux SaveState v4, SHA-256 `017c6601ad71f7e420cc5406f20c68367497c416663f07065a862f1484b2c9f7`. It has not been independently restored; do not promote it yet. The F180 card overlay was misclassified as `map`, risking an unwanted DOWN input.

Classifier code was updated in commit `02f39ca3cdf21120e574923a4e8706d66dd16333` to detect a `card_selection` state from central crop x=370..930,y=220..530 using bright-white and low-chroma-gray ratios, and return WAIT. Regression run [#39873268266](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39873268266) completed success and its logs report 8 tests OK, but it was triggered at the agent-only commit and did not include the new synthetic card-overlay test. A second regression run, [#39873273913](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39873273913), was triggered at test commit `d8082dcdfa8997df65cddf9e6d0d8d806c8da927`; latest API check shows it is still `in_progress` at `Install image dependencies`, with no artifact. Start time 23:39:57Z / 06:39:57 WIB; at the latest check it had not updated past 23:40:01Z. Audit run #39873273913 and verify its checkout includes BOTH classifier commit and synthetic test before accepting result. It is a regression workflow, not a gameplay player; there are no active player runs.

The marker `experiments/.run-storymode-adaptive-player` remains revision50 restore-only (source SHA `7f8771873b075830b3dadf14ef47a343ceb0f026790b9beba2af0bfb614debea`). Do not trigger the player until the regression completes and the real F180 image has been classified offline as `card_selection` / WAIT. If accepted, set revision51 restore-only to test the run50 output checkpoint; require F20 visibly contains all three cards and classifier card_selection, explicit SaveStateLoaded, five authentic 1280×800 frames, accepted shutdown, and external output checkpoint validation. No Circle/confirm until the card UI is understood.

Revision49 verified narrow rule: from a roulette screen, one Circle press/release makes the board visible by F180 while WAIT leaves roulette visible through F180; this is not dialogue skip. Story Mode remains **NOT COMPLETE**. Use START for dialogue; keep ROM/BIOS/states/cards/screenshots private and out of Git.

---

## LATEST VERIFIED CHECKPOINT — revision50 progressed to three-card overlay (23 October 2026, 06:35 WIB)

Run [#39872449049](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39872449049) completed success at 06:34:41 WIB; private artifact #12467281563 passes ZIP integrity. It restored the exact ACTION checkpoint from run #39870243073 / artifact #12466141660 / SHA-256 `7f8771873b075830b3dadf14ef47a343ceb0f026790b9beba2af0bfb614debea` (21,163,504 bytes, v4) in a fresh process, with `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`. Five authentic 1280×800 external-X11 screenshots passed; native shutdown exit124 was accepted only because session-finished marker and external checkpoint validation passed; effective exit0. Output file validated externally: 21,162,772 bytes, v4, SHA-256 `017c6601ad71f7e420cc5406f20c68367497c416663f07065a862f1484b2c9f7`.

Important: despite `RESTORE_TEST=1`, the current workflow still runs the ordinary adaptive policy after capture at F20. At F20 classifier state was `map`, so it sent DOWN (press/release true/false). F60 board screenshot shows the visible counter change from 3 to 1. At F100/F110, authentic screenshot shows Iruka dialogue `ナルト、ここは「札所」といって。` (Naruto, tempat ini disebut “札所”/fudasho; working translation “pos jimat/segel”, translation not finalized). The classifier selected START; START press/release passed and dialogue skip marker passed. F180 shows three card backs over the board. This is a real observed progression sequence; without matched WAIT from the same board checkpoint, the exact causal rule for DOWN remains **HYPOTHESIS**, while the screenshot/input/dialogue/skip sequence itself is directly observed. This is not proof of Story Mode completion.

Checkpoint output from run50, candidate board/card-overlay state: `adaptive-cycle-01-f180.sstate`, SHA-256 `017c6601ad71f7e420cc5406f20c68367497c416663f07065a862f1484b2c9f7`, 21,162,772 bytes, v4. **Not promoted** until a separate fresh process visibly restores it.

### Next step before a new player run
The existing classifier mislabels the three-card-back overlay at F180 as `map` (green background wins the rule) and would choose DOWN again. Add a conservative `card_selection` detector to `tools/storymode_adaptive_agent.py` using a calibrated central-card ROI (observed F180 from private run50 has white ratio 0.1974 and gray ratio 0.1822 in crop x=370..930,y=220..530; prior board/dialogue frames were well below both). Give this state action WAIT/fail-closed. Extend `tests/test_storymode_adaptive_agent.py` with a synthetic three-card overlay case; run tests and verify actual private screenshots offline. Do not commit any screenshot or savestate.

After classifier/tests pass, set revision51 to restore candidate checkpoint from run #39872449049 / artifact `naruto-storymode-adaptive-player-private` / `adaptive-cycle-01-f180.sstate` / SHA above. At F20 require classifier `card_selection`, visible three-card overlay, explicit load event, five authentic X11 screenshots, accepted shutdown, and output state external size/v4-header/SHA validation. Do not send confirm/Circle until the card UI and selection semantics are understood. No player is currently active.

## VERIFIED INPUT RULE — revision49 CIRCLE from roulette returns to board

Run [#39870243073](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39870243073) success. The paired source SHA was `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`; both F20 screenshots exactly matched and classified `roulette`; both processes logged SaveStateLoaded; cloned cards identical; Circle readback true/false; WAIT control; ten authentic 1280×800 captures; both outputs externally validated. ACTION remains on roulette through F110 and shows board by F180. WAIT remains on roulette at F180. Pixel differences F60 328885/MAD18.11568; F100 337474/19.18342; F110 344330/17.23071; F180 842364/39.31341. **VERIFIED, contextual:** Circle from roulette moves the visible screen back to board by F180; this is not dialogue skipping.

Story Mode remains NOT COMPLETE. Keep all gameplay assets private/out of Git. For Story Mode dialogue, use START, never Circle.

---

## ACTIVE RUN — revision50 restore-only board checkpoint after roulette Circle (23 October 2026, 06:35 WIB)

Run [#39872449049](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39872449049) remains the only active player. Marker at checkout `1c30215c9a4b6035b5c24d1bf0befc4819110642` is verified: source run #39870243073 / private artifact naruto-storymode-adaptive-player-private / adaptive-cycle-01-f180.sstate / SHA-256 `7f8771873b075830b3dadf14ef47a343ceb0f026790b9beba2af0bfb614debea`; restore-only, one cycle, revision50. Started 06:32:21 WIB; hard timeout about 06:52:21 WIB. Most recent status: source and assets validated; `Run adaptive observe-decide-act-verify-checkpoint loop` is active; no artifact yet. Do not launch a parallel player.

Audit run50 after it ends: source checksum, `ExecutionFlow::SaveStateLoaded`, `ADAPTIVE_RESTORE_TEST=PASS`, five authentic external-X11 screenshots at 1280×800 showing board retained after Circle, accepted shutdown recovery only after session-finished marker + checkpoint validation, and output checkpoint size/v4-header/SHA validation. Promote the exact input SHA only if the independent restore proves the board state. The output of run50 itself stays unpromoted until that output gets its own restore.

Revision49 run #39870243073 is fully verified: Circle from roulette keeps roulette visible through F110 and returns to board at F180; WAIT leaves roulette through F180. Ten authentic captures, matching parent/F20, load events, input true/false, and both valid checkpoints. Story Mode remains NOT COMPLETE.
---

## ACTIVE RUN — revision50 restore-only for the board-after-Circle checkpoint (23 October 2026, 06:32 WIB)

Run [#39872449049](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39872449049) is the only active player. It uses the committed revision50 marker at head `1c30215c9a4b6035b5c24d1bf0befc4819110642`: source run #39870243073 / artifact `naruto-storymode-adaptive-player-private` / checkpoint `adaptive-cycle-01-f180.sstate` / source SHA-256 `7f8771873b075830b3dadf14ef47a343ceb0f026790b9beba2af0bfb614debea`; `RESTORE_TEST=1`, one cycle, no A/B inputs. Run started at 06:32:21 WIB; hard timeout about 06:52:21 WIB. At last check it was initializing containers; no artifact yet. Do not start another player in parallel.

After completion audit the source validation, explicit `ExecutionFlow::SaveStateLoaded`, restore PASS, five authentic 1280×800 X11 captures, board state visually retained at F20, accepted shutdown path, and external output checkpoint validation (size, v4 header and SHA-256). Promote only the exact input source after independent restore passes. The new checkpoint emitted by run50 remains unpromoted until it is itself restored in another new emulator process.

### Latest rule already VERIFIED — revision49 CIRCLE vs WAIT from roulette
Run #39870243073 completed success at 06:14:50 WIB; private artifact #12466141660 passed ZIP integrity. Ten authentic 1280×800 X11 captures passed. Both fresh emulator processes restored the same source SHA `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`; explicit load events in both; F20 pixels identical; roulette state matched; cloned Memory Cards identical. Circle input readback true/false; WAIT control no input. Both sessions-finished markers existed. Native exits 124/139 were accepted only through the new narrow recovery after external checkpoint validation, then recorded as effective exit 0. Both output checkpoints passed size/v4-header/SHA validation and the comparison report was generated.

Actual screenshots show ACTION on roulette at F60/F100/F110 then back at the board by F180; WAIT still shows roulette at F180. Pixel differences: F60 328,885 (MAD 18.11568); F100 337,474 (19.18342); F110 344,330 (17.23071); F180 842,364 (39.31341). **VERIFIED, context limited:** a Circle press/release from the roulette screen causes a transition to the board by F180, while WAIT leaves the roulette visible through F180. It is not dialogue skipping; use START for all Story Mode dialogue.

Candidate output hashes from private artifact #12466141660:
- ACTION board-after-Circle: 21,163,504 bytes, v4, SHA-256 `7f8771873b075830b3dadf14ef47a343ceb0f026790b9beba2af0bfb614debea` — currently under restore test #39872449049.
- WAIT control: 21,162,411 bytes, v4, SHA-256 `7780743d6f99e5534cd53095bd1fd68126d409ada21fe73993d2100030e4f029`; not promoted.

Story Mode remains **NOT COMPLETE**. No ending, capture or ownership result was established in this test. Keep ROM, BIOS, savestates, Memory Cards and gameplay screenshots private/out of Git.

---

## VERIFIED RESULT — revision49 CIRCLE vs WAIT from roulette (23 October 2026, 06:14 WIB)

Run [#39870243073](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39870243073) completed with Actions success at 06:14:50 WIB. Private artifact #12466141660 was downloaded; ZIP passed `unzip -t`. All ten genuine external-X11 screenshots are 1280×800 and passed image validation. Both fresh emulator processes loaded the same parent checkpoint SHA-256 `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`, and both logged `ExecutionFlow::SaveStateLoaded`. F20 screenshots match pixel-for-pixel (1,024,000 pixels), both classify `roulette`, and disposable Memory Cards are hash-identical. ACTION CIRCLE press/release readback was true/false; control WAIT sent no input. Both emulator branches reached their session-finished marker; native shutdown returned 124 and 139 but the new gated recovery accepted them only after post-session checkpoint validation; normalized session exit codes were 0. Both checkpoint outputs passed size, v4 header and SHA-256 checks. The paired comparison report was generated.

Direct visual review: ACTION remains on the roulette wheel at F60/F100/F110, then shows the board by F180; WAIT remains on the roulette wheel through F180. Pairwise differences: F60 328,885 pixels/MAD 18.11568; F100 337,474/MAD 19.18342; F110 344,330/MAD 17.23071; F180 842,364/MAD 39.31341.

**Rule status: VERIFIED, limited context.** One CIRCLE press/release from the verified roulette screen causes a visual transition back to the board by F180, while WAIT leaves the roulette visible through F180. Do not infer the precise roulette value/sector outcome or other meanings of Circle from this alone. This is not dialogue skipping; use START for Story Mode dialogue.

Checkpoint outputs in private artifact #12466141660 (valid structure, not promoted yet):
- ACTION board-after-Circle candidate: 21,163,504 bytes, v4, SHA-256 `7f8771873b075830b3dadf14ef47a343ceb0f026790b9beba2af0bfb614debea`.
- WAIT control: 21,162,411 bytes, v4, SHA-256 `7780743d6f99e5534cd53095bd1fd68126d409ada21fe73993d2100030e4f029`.

### Next gate — revision50 restore-only of ACTION board checkpoint
Use run #39870243073 / artifact `naruto-storymode-adaptive-player-private` / file `adaptive-cycle-01-f180.sstate` / source SHA `7f8771873b075830b3dadf14ef47a343ceb0f026790b9beba2af0bfb614debea`, `RESTORE_TEST=1`, `CONTINUATION_TEST=0`, `AB_TEST=0`, `LOOP_CYCLES=1`, `REVISION=50`. Require explicit load event, five authentic 1280×800 frames with the board still visible at F20, accepted shutdown, and external source/output size/header/SHA validation. Promote only the exact input checkpoint after the independent restore passes; the new output from revision50 will itself need a separate restore before use.

Story Mode remains **NOT COMPLETE**. No ending, capture or territory-ownership result is established here. Keep ROM, BIOS, savestates, Memory Cards and screenshots private/out of Git.

---

## ACTIVE — revision49 final Circle-vs-WAIT retry with gated timeout recovery

Run [#39870243073](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39870243073) is the only active player, started 06:12:25 WIB; hard timeout about 06:32:25 WIB. Marker at commit `04102a5f79e81a0f91586af3f348b6f2fb3183fe` was verified: source run #39867730674 / artifact `naruto-storymode-adaptive-player-private` / `adaptive-cycle-01-f180.sstate` / SHA-256 `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`; AB_TEST=1, AB_ACTION=CIRCLE, AB_EXPECTED_STATE=roulette, two cycles, revision49.

Run48 produced all screenshots and both output files were externally valid after artifact download, but CONTROL shutdown fault yielded exit124 and workflow didn't accept it. New workflow commit `ef82beb99096e6fd939ce5ebc4f80eedc1158546` adds that narrowly gated path: exit124/134/139 is accepted only when the session-finished marker exists and checkpoint size/v4 header/SHA all validate; the process timeout is 60s. The saved checkpoints still must pass in-workflow external validation and the paired comparison report must be generated.

Expected visual pattern from two prior partial attempts: ACTION Circle on the roulette wheel shows roulette at F60/F100/F110 then returns to board at F180; WAIT stays roulette through F180. This remains HYPOTHESIS until #39870243073 passes every acceptance gate. Do not start another player in parallel.

---

## REVISION48 PARTIAL RESULT — both output states are valid, but the control process timed out after shutdown fault

Run [#39869536734](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39869536734) failed at 23:09:34 UTC / 06:09:34 WIB. Its artifact #12466086061 passes ZIP integrity and contains all 10 authentic 1280×800 screenshots. Both fresh processes loaded the exact roulette parent `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`; both F20 screenshots are pixel-identical, both classify `roulette`; matching disposable Memory Cards; Circle press/release true/false; WAIT control; all captures and input gates passed.

Visual outcome matches revision47: ACTION Circle is roulette at F60/F100/F110, then the wheel slides away and the board is visible at F180; WAIT remains on the spinning wheel at F180. This remains **HYPOTHESIS** until the full workflow run passes all gates.

Unlike revision47, both output checkpoints from this run are externally checked after download and valid:
- ACTION `adaptive-cycle-01-f180.sstate`: 21,163,075 bytes, v4, SHA-256 `7e0a021342f3cf15db2070c5b9512ff0154a4a1adeeb4e14837b930884656e3a`.
- CONTROL `adaptive-cycle-02-f180.sstate`: 21,162,748 bytes, v4, SHA-256 `75098aea814f531a714d7aade45e9802bb44167a122ada4aad6d19e728f4256f`.

The failure is now bounded to process shutdown: after F180, the Lua session-finished marker is logged, then `corrupted size vs. prev_size`; settle-complete does not fire for cycle2 and the inner timeout yields exit124. Workflow commit `ef82beb99096e6fd939ce5ebc4f80eedc1158546` makes the shutdown recovery stricter but more complete: only exits 134/139/124 after a session-finished marker and successful external size/header/SHA validation are accepted, and per-process timeout is reduced to 60 seconds. It still rejects invalid/missing checkpoints and any failure before the session-finished marker.

### Next — revision49 repeat with corrected timeout recovery
Reuse the immutable, independently restored roulette source from run #39867730674/artifact #12464258211/checkpoint `adaptive-cycle-01-f180.sstate`/SHA `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`. Set `AB_TEST=1`, `AB_ACTION=CIRCLE`, `AB_EXPECTED_STATE=roulette`, `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `LOOP_CYCLES=2`, `REVISION=49`. Require the complete report and all source/input/state/checkpoint gates. No parallel runs. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision48 retries roulette Circle-vs-WAIT after post-save settle fix (23 October 2026, 06:06 WIB)

Run [#39869536734](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39869536734) is the only active player, started 06:05:59 WIB; hard timeout about 06:25:59 WIB. Committed marker at head `eb12d63e0daf45179c30f12d525b43cea90390a4` was re-read:
SOURCE_RUN=39867730674; source artifact `naruto-storymode-adaptive-player-private`; checkpoint `adaptive-cycle-01-f180.sstate`; SHA-256 `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`; AB_TEST=1; AB_ACTION=CIRCLE; AB_EXPECTED_STATE=roulette; two cycles; revision48.

Revision47 passed all visual capture/input parity gates but failed final workflow because the CONTROL savestate was only 2 MiB and invalid (exit139 after session-finished). It strongly suggested Circle transitions back to the map by F180 while WAIT retains the spinning wheel, but the rule stays HYPOTHESIS. Workflow blob `ae6aa7e4f945da4322bb08880a38836fa1a3039a` now waits 12 VSync callbacks after the F180 checkpoint is written before native shutdown; state still represents F180, and both output checkpoints must still pass full external validation. Gated recovery of exit 134/139 remains fail-closed.

Do not run another player in parallel. After run completes inspect both checkpoint sizes/headers/SHA and report as well as actual paired frames. The wheel result number must not be claimed unless it is stable and legible. Story Mode NOT COMPLETE.

---

## REVISION47 PARTIAL VISUAL RESULT — Circle appears to leave roulette, but control checkpoint truncated

Run [#39868722262](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39868722262) completed with failure at 23:00:30 UTC / 06:00:30 WIB. Private artifact #12464698050 passed ZIP integrity and all 10 genuine screenshots were reviewed. Both processes loaded the exact trusted roulette parent `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`, each logged `ExecutionFlow::SaveStateLoaded`; F20 pixel parity was exact; Memory Card clones matched; Circle input press/release readback passed true/false; ten 1280×800 X11 captures passed; both branch capture sequences completed and checkpoint files were present.

**Partial visual finding (HYPOTHESIS until a full gate passes):** ACTION Circle remains on the roulette wheel at F60/F100/F110, then at F180 has transitioned back to the board, with part of the wheel sliding out of view. WAIT remains on the roulette wheel through F180. This strongly suggests Circle settles/exits the wheel after the animation, but no selected number is claimed.

Why the workflow correctly failed: ACTION output `adaptive-cycle-01-f180.sstate` passed external validation (21,163,242 bytes, v4, SHA-256 `6abeb30642c9e8c6474b207e7de725619ff858ae9203c24e532e28410e8a31cd`). CONTROL output `adaptive-cycle-02-f180.sstate` was only 2,097,152 bytes and failed size validation; process exit was 139 after the session-finished marker. Hence no `ab-comparison-report.txt` and the A/B experiment is not counted as complete. The source checkpoint remains the independently restored roulette checkpoint `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492` from #39867730674.

Workflow commit `32f9e4172a670cdd14b92992f62a2e6fc970aba5` now keeps the emulator alive for 12 more VSync callbacks after writing the F180 checkpoint, then shuts down. The saved state is still an F180 snapshot; the extra frames allow any deferred file I/O to settle. Existing recovery remains strict: exit 134/139 is tolerated only if the session-finished marker exists and the state passes external size/v4-header/SHA validation.

### Next — revision48 repeat Circle vs WAIT from the same roulette source
Use run #39867730674 / artifact #12464258211 / file `adaptive-cycle-01-f180.sstate` / source SHA `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`. Set `AB_TEST=1`, `AB_ACTION=CIRCLE`, `AB_EXPECTED_STATE=roulette`, `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `LOOP_CYCLES=2`, `REVISION=48`. Require every A/B gate including valid external size/header/SHA on both outputs and the report. Inspect whether Circle returns to map with wheel gone while WAIT wheel stays. Do not choose a roulette number claim unless it is stable and legible; no Circle for dialogue (START only). Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision47 Circle versus WAIT from the restored roulette wheel (23 October 2026, 05:59 WIB)

Run [#39868722262](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39868722262) is the only active player, started 05:58:51 WIB with hard timeout about 06:18:51 WIB. Its exact committed marker:
SOURCE_RUN=39867730674; source artifact `naruto-storymode-adaptive-player-private`; checkpoint `adaptive-cycle-01-f180.sstate`; source SHA-256 `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`; AB_TEST=1; AB_ACTION=CIRCLE; AB_EXPECTED_STATE=roulette; two cycles; revision47.

This source checkpoint was independently restored by run #39868354205: fresh load event and restore PASS, five authentic 1280×800 screenshots all showing the wheel, exit0, and output checkpoint validation. No parallel player may run while #39868722262 is active.

Required A/B gates: exact source hash on both branches, two load events, F20 pixel-perfect parity and both states `roulette`, identical disposable Memory Cards, Circle press/release readback true/false, WAIT control, ten authentic 1280×800 X11 screenshots, both branch processes complete via normal exit or strictly gated session-finished+external-checkpoint recovery, output state files externally validated, comparison report generated. Inspect C01/C02 F60/F100/F110/F180 to decide whether Circle stops the wheel/returns a result while WAIT remains spinning. Do not infer final roulette result without stable UI evidence. Story Mode remains NOT COMPLETE.

---

## RESTORE VERIFIED — Circle-opened roulette wheel is persistent across a new emulator process (revision46, 23 October 2026)

Run [#39868354205](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39868354205) completed with success at 22:56:40 UTC / 05:56:40 WIB. Private artifact #12465131490 passed ZIP integrity. The source checkpoint was from revision45/run #39867730674/artifact #12464258211: `adaptive-cycle-01-f180.sstate`, 21,162,546 bytes, PCSX-Redux SaveState v4 header, SHA-256 `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`.

The new process logged `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`; five authentic external-X11 captures validated at 1280×800. Direct screenshot review confirms the roulette wheel is visible at F20, F60, F100, F110, and F180. Emulator exit was 0; the new output checkpoint passed external validation: 21,162,423 bytes, v4 header, SHA-256 `6d76dbd23d5d01dc1f145d6837b987ae3232fff383ad23eb5262c375ca4828ea`.

**Promoted input checkpoint:** SHA `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492` is now independently restore-proven and is the trusted roulette-state source. The new output SHA `6d76dbd2…ca4828ea` is **not** promoted until it is independently restored.

### Next controlled action — revision47 CIRCLE vs WAIT from roulette state
Workflow commit `11b308f162aa1ef2f5b5167cd17b4340718a03de` permits `AB_EXPECTED_STATE=roulette` only with `AB_ACTION=CIRCLE`. Set source run #39867730674 / artifact `naruto-storymode-adaptive-player-private` / file `adaptive-cycle-01-f180.sstate` / source SHA above, `AB_TEST=1`, `AB_ACTION=CIRCLE`, `AB_EXPECTED_STATE=roulette`, `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `LOOP_CYCLES=2`, `REVISION=47`.

Keep all A/B gates: exact same source SHA in both processes, two SaveStateLoaded events, F20 image parity and `roulette` state, identical Memory Card clones, Circle press/release true/false, WAIT control, ten authentic 1280×800 captures, both processes exit0 or gated session-finished checkpoint recovery, both output checkpoints externally validated, comparison report generated. Inspect whether Circle stops the wheel/returns a result or whether it keeps moving; WAIT should provide the spinning baseline. If Circle results in a dialogue, press START only. No Circle for dialogue. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision46 fresh-process restore of Circle-opened roulette state (23 October 2026, 05:55 WIB)

Run [#39868354205](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39868354205) is the only active player. Exact committed marker at head `096a5cdc411e3ce26fd44f9bde8ff4ed909313c7`:
SOURCE_RUN=39867730674; artifact `naruto-storymode-adaptive-player-private`; checkpoint `adaptive-cycle-01-f180.sstate`; SHA-256 `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`; RESTORE_TEST=1; CONTINUATION_TEST=0; AB_TEST=0; LOOP_CYCLES=1; REVISION=46.

Input checkpoint locally audited from artifact #12464258211: 21,162,546 bytes, header `PCSX-Redux SaveState v4`, SHA-256 matches the marker. Revision45 original emulator had logged `ADAPTIVE_SESSION_FINISHED` but aborted at native shutdown (exit134), after saving this state. No A/B control was run, so the Circle-to-roulette effect remains HYPOTHESIS.

Workflow now (commit `11b308f162aa1ef2f5b5167cd17b4340718a03de`) accepts exit134 only when the session-finished marker is present and the newly saved checkpoint passes external size/header/SHA validation. It also supports expected state `roulette` restricted to Circle A/B. Revision46 will test whether this checkpoint actually restores and retains the roulette wheel. At last check the run was initializing containers; started 05:55:24 WIB; hard timeout about 06:15:24 WIB. Do not launch another player.

Pass requires explicit SaveStateLoaded and `ADAPTIVE_RESTORE_TEST=PASS`, five authentic 1280×800 X11 captures visually showing roulette, accepted process exit or gated shutdown recovery, and external output checkpoint validation. Do not promote the output emitted by revision46 until independently restored. Story Mode remains NOT COMPLETE.

---

## REVISION45 PARTIAL EVIDENCE — Circle opens roulette, but paired A/B failed during native shutdown

Run [#39867730674](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39867730674) completed with failure. Private artifact #12464258211 was downloaded; ZIP integrity passed and authentic screenshots C01-F20/F60/F100/F180 were inspected. ACTION source was the independently restored command menu, source SHA `609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`, F20 showing `ルーレット` (Roulette) highlighted. Circle press/release readback true/false passed. F60/F100/F110/F180 all display the roulette wheel and the classifier reports `roulette`.

However, after the ACTION branch logged `ADAPTIVE_SESSION_FINISHED cycle=1`, the PCSX-Redux process aborted on `corrupted size vs. prev_size`, native exit 134. The WAIT/control branch never ran, no C02 screenshots or A/B comparison report exist. Therefore this is only **partial evidence / HYPOTHESIS**, not a completed A/B gate: contextual Circle appears to open the roulette wheel from the highlighted Roulette menu, but the matched control still needs to be run.

Partial ACTION checkpoint from the private artifact is present and locally validated:
- file `adaptive-cycle-01-f180.sstate`, 21,162,546 bytes
- header `PCSX-Redux SaveState v4`
- SHA-256 `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`
- Artifact #12464258211, run #39867730674.
This is **not promoted** until independently restored in a fresh emulator process and visually confirmed.

Workflow commit `11b308f162aa1ef2f5b5167cd17b4340718a03de` now tolerates post-session exit 134 only when `ADAPTIVE_SESSION_FINISHED` exists and the output checkpoint passes external size/v4-header/SHA validation; it also adds expected state `roulette` guarded to `AB_ACTION=CIRCLE`. This preserves fail-closed checks before any recovered exit is accepted.

### Next — revision46 restore-only of partial roulette checkpoint
Source run #39867730674 / artifact `naruto-storymode-adaptive-player-private` / `adaptive-cycle-01-f180.sstate` / SHA-256 `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`. Set `RESTORE_TEST=1`, `CONTINUATION_TEST=0`, `AB_TEST=0`, `LOOP_CYCLES=1`, `REVISION=46`. Require load event and restore PASS, five authentic 1280×800 screenshots showing the wheel remains open, accepted process shutdown only via normal exit or session-finished + validated checkpoint, and external validation of the new output state. Keep the new restore output unpromoted pending its own restore.

After revision46 verifies the input, use revision47 Circle vs WAIT from explicit `roulette` state, `AB_ACTION=CIRCLE`, all paired gates; inspect whether Circle stops the wheel/chooses a result versus WAIT keeping it spinning. No dialogue skipping with Circle; use START. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision45 Circle-vs-WAIT from the restored Roulette-highlighted menu

Run [#39867730674](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39867730674) is the only active player. Its committed marker was verified at SHA `c9b1438292041f972b712f248fb7052032635b59`: source run #39866820866 / artifact `naruto-storymode-adaptive-player-private` / checkpoint `adaptive-cycle-01-f180.sstate` / SHA-256 `609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`; `AB_TEST=1`, `AB_ACTION=CIRCLE`, `AB_EXPECTED_STATE=menu_or_unknown_choice`, two cycles, revision45. Workflow blob `4021462372a7573132783b21285d35b0da25eab8` allows Circle only for menu-state A/B; map-state branch excludes it.

Started 05:49:51 WIB; hard timeout about 06:09:51 WIB. No artifact/results audited yet. Do not launch another player.

Required gates: exact source hash in both fresh processes, two load events, pixel-identical F20 and expected menu state, identical cloned Memory Cards, Circle press/release true/false, WAIT control, ten authentic 1280×800 X11 captures, both emulator exits0, both output checkpoint size/v4-header/SHA validations, and comparison report. Review F60/F100/F110/F180 screenshots: does Circle open roulette while WAIT remains on the menu? Circle is used only because the source F20 was independently restored and visibly has Roulette highlighted; if a dialogue appears, START only. No claiming Story Mode completion.

---

## RESTORE VERIFIED — command menu with Roulette highlighted survives fresh process (revision44)

Run [#39867381637](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39867381637) completed with success at 22:48:12 UTC / 05:48:12 WIB. Private artifact #12464118614 passed ZIP integrity and authentic C01-F20 screenshot was inspected. It clearly shows the command menu with `ルーレット` (Roulette) highlighted in red. The fresh process logged `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`; five external-X11 captures validated at 1280×800; emulator exit 0; output checkpoint passed external size/v4-header/SHA validation.

**Promoted input checkpoint:** run #39866820866 / artifact #12463489344 / `adaptive-cycle-01-f180.sstate`, 21,162,920 bytes, v4 header, SHA-256 `609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`. This exact hash is independently restore-proven and remains the source for next experiment.

New output from run #39867381637 is not promoted: 21,163,308 bytes, v4 header, SHA-256 `0499c0f73799ac18f53a08bfd2c63a45738d8b56fcd32f157d6b0b7b596c19e3`. It needs its own independent restore.

### Next — revision45 Circle vs WAIT on visibly selected Roulette
Workflow commit `2ec5011c5c81f00e686690570bf4349f9124c531` permits `CIRCLE` only in the `menu_or_unknown_choice` state guard; the map-state guard does not permit Circle. Source is run #39866820866 / artifact `naruto-storymode-adaptive-player-private` / `adaptive-cycle-01-f180.sstate` / SHA above. Marker: `AB_TEST=1`, `AB_ACTION=CIRCLE`, `AB_EXPECTED_STATE=menu_or_unknown_choice`, `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `LOOP_CYCLES=2`, `REVISION=45`.

Require all A/B gates: exact source hashes per branch, two load events, identical F20 pixels and menu state, cloned cards identical, Circle press/release true/false, WAIT control, ten authentic 1280×800 captures, both exit0, both output state size/v4-header/SHA checks, comparison report, and direct image review. If ACTION enters roulette/wheel and WAIT stays on menu, classify only that contextual response VERIFIED. If dialogue appears, START is the only skip action; do not use Circle for dialogue. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision44 restore-only validates Roulette-highlighted menu checkpoint

Run [#39867381637](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39867381637) is the only active player. Marker at its checkout verified:
SOURCE_RUN=39866820866; SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private; SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate; SOURCE_SHA256=`609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`; RESTORE_TEST=1; CONTINUATION_TEST=0; AB_TEST=0; LOOP_CYCLES=1; REVISION=44. Workflow blob `4021462372a7573132783b21285d35b0da25eab8` allows CIRCLE only for map-state A/B? Correction: current workflow permits CIRCLE for menu-state A/B, not the restore test.

Run started at 05:46:45 WIB; hard timeout about 06:06:45 WIB. At last check it was newly in progress; no artifact yet. Do not start another player.

Accept only after explicit `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`, five authentic 1280×800 X11 captures with F20 showing the command menu and `ルーレット` (Roulette) highlighted, exit0, and external output size/v4-header/SHA validation. If F20 retains the expected menu highlight, promote the input source SHA `609823…52bbffb7` as restorable. New output from this restore run remains unpromoted pending its own independent restore.

Next step after this run finishes: revision45 matched CIRCLE vs WAIT from the same source checkpoint. CIRCLE is permitted only under menu-state guard; the selected Roulette row is visually documented by source C01-F100/F180 in run #39866820866. It must not be used on dialogue. Story Mode remains NOT COMPLETE.

---

## VERIFIED — CROSS returns from board map to command menu (revision43, 23 October 2026)

Run [#39866820866](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39866820866) completed with success at 22:43:31 UTC / 05:43:31 WIB. The private artifact #12463489344 passed ZIP integrity and was visually inspected.

Matched A/B gates passed:
- Both new processes restored the exact parent SHA `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`; each logged `ExecutionFlow::SaveStateLoaded`.
- F20 screenshots matched all 1,024,000 pixels; both classified `map_after_move`.
- Disposable Memory Card copies were identical; CROSS press/release readback was true/false; WAIT control sent no input.
- Ten authentic external-X11 captures validated at 1280×800. Both emulator processes exited 0, both output checkpoints passed external size/v4-header/SHA checks, and `ab-comparison-report.txt` was generated.

**Rule: VERIFIED, exact context only.** With the map view open and Naruto's cell selected, one CROSS returns to the command menu. The actual ACTION screenshot C01-F60 shows the two-option transition UI; C01-F100 and C01-F180 show the full menu with `ルーレット` (Roulette) highlighted. The WAIT branch stays in map view with Naruto's panel (`レベル` (Level)1, `結界価値` (Nilai penghalang)60, `耐久値` (Daya tahan)2/2). This proves return navigation, not a gameplay move or capture.

Output states, validated but not promoted until independently restored:
- ACTION/menu candidate: run #39866820866 artifact #12463489344, `adaptive-cycle-01-f180.sstate`, 21,162,920 bytes, v4, SHA-256 `609823871cc2cb7827404fecb1a5b98aa0c8446df405679932eb083d52bbffb7`.
- CONTROL/map state: `adaptive-cycle-02-f180.sstate`, 21,162,981 bytes, v4, SHA-256 `57fd76c4f133dc485e5bbfc49f8cb6e0e86593780812827bee1a43668ae80e84`.

### Next gate — revision44 restore the menu checkpoint
Restore ACTION output above in a fresh process. Require load event and restore PASS, five authentic 1280×800 X11 captures, F20 visibly in the command menu with `ルーレット` (Roulette) highlighted, exit0, and new output state externally validated. Only then promote the input source SHA `609823…52bbffb7`.

After this restore succeeds, conduct revision45 Circle-vs-WAIT from that exact menu checkpoint. The reason is the source F100/F180 screenshot visibly highlights Roulette. The workflow must allow Circle only under the `menu_or_unknown_choice` state guard (dialogue classifier has priority and should fail this precondition); visually verify the restored F20 before running. This is contextual Roulette menu confirmation, not dialogue skipping. If a dialogue appears, press START only. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision43 retries CROSS-vs-WAIT with all gates fixed (23 October 2026, 05:42 WIB)

Run [#39866820866](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39866820866) is the only active player. Revision42 (#39866476856) failed before emulator launch with a 4,505-byte setup-only artifact because the last shell whitelist had not included CROSS. Workflow commit `417663b21ce0cd9218ef8c312913a90d65381788` now includes CROSS in the final allowlist as well as in the selector and Lua map-state gate.

Revision43 checkout marker verified: source run #39786019434 / artifact `naruto-storymode-adaptive-player-private` / checkpoint `adaptive-cycle-01-f180.sstate` / SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`; `AB_TEST=1`, `AB_ACTION=CROSS`, `AB_EXPECTED_STATE=map_after_move`, two cycles, `REVISION=43`. Started 05:41:57 WIB; hard timeout about 06:01:57 WIB. At last check it was initializing containers. Do not launch a parallel player.

Audit the actual artifact and logs after run termination: exact parent SHA both arms, two explicit load events, F20 pixel parity and state, same disposable cards, CROSS press/release true/false, WAIT control, ten genuine 1280×800 X11 captures, both exits0, two post-exit checkpoint validations, comparison report, and direct screenshot review. The observed footer `× もどる` (Cross: Kembali) motivates—but does not prove—the hypothesis that CROSS exits the map. Until that paired test passes, CROSS effect is UNKNOWN.

Story Mode remains NOT COMPLETE.

---

## REVISION42 DIAGNOSTIC — CROSS probe rejected by one stale shell allowlist

Run [#39866476856](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39866476856) failed before emulator launch. Its artifact #12463119868 is only a 4,505-byte setup dump; there are no gameplay screenshots and no conclusion about CROSS behavior is allowed.

The exact failure was the final runtime shell whitelist still restricting `AB_ACTION` to UP/DOWN/LEFT/RIGHT/TRIANGLE after the selector and Lua guard had already accepted CROSS. Workflow fix commit `417663b21ce0cd9218ef8c312913a90d65381788` updates that last allowlist. The other guardrails remain: CROSS allowed only with `AB_EXPECTED_STATE=map_after_move`; menu state still only allows DOWN/TRIANGLE; Circle is not allowed for this navigation test.

Retry as revision43 using the unchanged, restore-proven map checkpoint from run #39786019434 / artifact #12428777970 / file `adaptive-cycle-01-f180.sstate` / SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`. Settings: `AB_TEST=1`, `AB_ACTION=CROSS`, `AB_EXPECTED_STATE=map_after_move`, `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `LOOP_CYCLES=2`, `REVISION=43`. Do not start a parallel player. Require the complete paired A/B evidence gate and inspect actual screenshots to determine whether CROSS exits map to the previous menu. Until then CROSS behavior is UNKNOWN.

---

## ACTIVE — revision42 CROSS-vs-WAIT on map return prompt

Run [#39866476856](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39866476856) is the only active player run. The marker at commit `0fb5636106edc03073517335417db7bf24be2284` was re-read and matches:
- Source run #39786019434, artifact `naruto-storymode-adaptive-player-private`, checkpoint `adaptive-cycle-01-f180.sstate`, SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`.
- `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `AB_TEST=1`, `AB_ACTION=CROSS`, `AB_EXPECTED_STATE=map_after_move`, `LOOP_CYCLES=2`, `REVISION=42`.
- Workflow blob `494baab78b7237fa80674526c583e0fdfc74c140` allows CROSS only in the map-state directional A/B branch; menu-state actions remain constrained to DOWN/TRIANGLE.

Actions reports the run started 22:39 UTC on 22 October (05:39 WIB on 23 October); 20-minute hard timeout is about 05:59 WIB if not completed earlier. At last check it was initializing containers; no artifact yet. Do not start another player.

The screen's verified footer `× もどる` (Cross: Kembali) motivates this matched experiment. Require identical F20 screenshots/state, same source SHA in both new processes, two SaveStateLoaded events, identical disposable cards, CROSS press/release readback true/false, WAIT control, ten authentic 1280×800 X11 captures, exit0 in both, both output checkpoint size/v4-header/SHA validations, and comparison report. Inspect whether ACTION returns to the prior menu while WAIT remains on the map. This is only a return-navigation probe, not a tile confirm. Story Mode remains NOT COMPLETE.

---


---

## RESTORE VERIFIED — Naruto-cell focus persists across a fresh emulator process (revision41, 22 October 2026)

Run [#39786899480](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39786899480) completed with Actions success. Private artifact #12428873919 was downloaded, ZIP integrity passed, and the authentic C01-F20 screenshot was inspected. It visibly shows Naruto's tile panel: `レベル` (Level) 1, `結界価値` (Nilai penghalang) 60, `耐久値` (Daya tahan) 2/2. The fresh emulator process logged `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`; five X11 screenshots of 1280×800 were validated; process exit 0; output checkpoint passed external validation.

Input source now independently restore-proven: run #39786019434 / artifact #12428777970 / file `adaptive-cycle-01-f180.sstate`, 21,163,100 bytes, v4 header, SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`. The output from restore run #39786899480 is not promoted: 21,162,593 bytes, v4, SHA-256 `93bd0c3e401bd7b8c96bc8b405bd46b13fef2afaf317c2ec47af5412c1b52595`; this output requires its own restore before reuse.

### Next experiment — revision42 CROSS vs WAIT on map screen
The visible map footer is `× もどる` (Cross: Kembali). Workflow commit `7ac1b2371b7d0ce48b87b59130a8560db771a962` adds CROSS only to map-state A/B allowlist; menu-state A/B still permits only DOWN or TRIANGLE. This is a guarded test of a visibly labelled return action, not tile confirmation. Use source run #39786019434 / artifact `naruto-storymode-adaptive-player-private` / checkpoint `adaptive-cycle-01-f180.sstate` / SHA `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`. Marker should set `AB_TEST=1`, `AB_ACTION=CROSS`, `AB_EXPECTED_STATE=map_after_move`, `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `LOOP_CYCLES=2`, `REVISION=42`. Keep strict A/B gates; manually inspect whether CROSS exits to prior menu while WAIT remains on map. Never use Circle for dialogue, only START to skip dialogue. Story Mode remains NOT COMPLETE.

---

## ACTIVE — revision41 restore-only for Naruto-cell focus checkpoint (22 October 2026, 20:27 WIB)

Run [#39786899480](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39786899480) is the only active player. It loads the revision40 ACTION output from run #39786019434, private artifact #12428777970, checkpoint adaptive-cycle-01-f180.sstate, SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`, size 21,163,100 bytes, v4. Marker: RESTORE_TEST=1, CONTINUATION_TEST=0, AB_TEST=0, LOOP_CYCLES=1, REVISION=41.

Started 20:26:48 WIB; hard timeout around 20:46:48 WIB. At last check the run was in progress but detailed job steps had not populated; no artifact yet. Do not launch another player.

Acceptance: exact source hash validation, explicit `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`, five authentic external-X11 captures at 1280×800, F20 visibly retains Naruto panel `レベル` (Level) 1 / `結界価値` (Nilai penghalang) 60 / `耐久値` (Daya tahan) 2/2, accepted exit0, and post-exit external checkpoint size/v4-header/SHA validation. Only then promote the input SHA 73947…; the new output from this restore run remains unpromoted until it too is restored.

Story Mode remains NOT COMPLETE.

---

## VERIFIED RESULT — UP selects Naruto's cell from empty-land140 focus (revision40, 22 Oct 2026)

Run [#39786019434](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39786019434) success. Private artifact #12428777970 audited. Matched A/B gates all passed: both fresh processes loaded exact source SHA `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`; SaveStateLoaded event in each; disposable Memory Card copies identical; F20 frames identical across 1,024,000 pixels; both classifier state `map_after_move`; UP input readback true/false; WAIT control; ten authentic X11 screenshots 1280×800; exit0 in both; both output states externally validated; comparison report generated.

**VERIFIED, focus only:** from `空き地` (Tanah kosong), value 140, one UP changes focus/panel to Naruto's occupied cell: `レベル` (Level) 1, `結界価値` (Nilai penghalang) 60, `耐久値` (Daya tahan) 2/2. WAIT preserves the empty-land140 panel. This does not prove actual character movement, capture or ownership.

ACTION candidate: `adaptive-cycle-01-f180.sstate`, 21,163,100 bytes, v4, SHA-256 `73947ce73a321600d7d1850b4f888889675f0e75c47fb05c7ae010e62ccaa7f8`. CONTROL output: 21,162,751 bytes, SHA `eb182a883b1666a7a9badbbf06fda2de960fc84ec4b040799791a174134714a3`. Neither promoted yet.

Next revision41: independently restore the ACTION candidate in a fresh process. Require load event, five authentic 1280×800 captures retaining Naruto's value60 panel, exit0 and external output size/v4-header/SHA checks. Story Mode remains NOT COMPLETE; no ending evidence.

---

## ACTIVE RUN — revision40 UP vs WAIT after revision39 guard fix (22 October 2026, 20:21 WIB)

Run [#39786019434](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39786019434) was triggered with the corrected marker:
- source run #39779256427, private artifact naruto-storymode-adaptive-player-private, file adaptive-cycle-01-f180.sstate
- source SHA-256 58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a
- AB_TEST=1; AB_ACTION=UP; AB_EXPECTED_STATE=map_after_move; RESTORE_TEST=0; CONTINUATION_TEST=0; LOOP_CYCLES=2; REVISION=40.

Revision39 run #39784493293 failed before emulator launch: selector and Lua policy permitted UP, but a later shell gate still hard-coded DOWN/TRIANGLE. Artifact #12427839381 is only a tiny setup dump (4,504 bytes); no screenshots or gameplay evidence exist, so no rule about UP can be inferred. Workflow fix commit #d62a04e831ea185f13efafc5e061d5a8dbb945ce changed the runtime guard to allow UP/DOWN/LEFT/RIGHT/TRIANGLE. Main workflow blob is 73c864d2eba5579be26da732832a467be876b2d1.

Run #39786019434 is queued as of 20:21 WIB; do not launch another player. Once it starts, use the current run status and job step list; audit only after it completes. Required evidence remains strict: exact source hash in both arms, 2 SaveStateLoaded events, F20 map_after_move state and pixel parity, equal card clones, UP press/release true/false, WAIT control, 10 genuine 1280×800 X11 screenshots, both exit0, both output checkpoints validated size/v4-header/SHA, comparison report. Manually inspect whether UP changes focus relative to WAIT. No tile confirmation.

Story Mode remains NOT COMPLETE. No movement/capture/ownership or ending is proven by the current probe series.

---

## ACTIVE RUN — revision39 UP vs WAIT (22 October 2026, 20:11 WIB)

Run [#39784493293](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39784493293) is the only active player. Its checkout was verified at commit 4893e1e0eb6cdcaf9fff052c9c794ae62327858a. Marker: source run #39779256427, artifact naruto-storymode-adaptive-player-private, checkpoint adaptive-cycle-01-f180.sstate, SHA-256 58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a; AB_TEST=1; AB_ACTION=UP; AB_EXPECTED_STATE=map_after_move; two cycles; revision39. The checked workflow supports UP/DOWN/LEFT/RIGHT for map-state A/B.

Run started at 20:10:11 WIB; timeout approximately 20:30:11 WIB. Do not launch another player. After completion require two load events, exact source SHA per arm, F20 pixel parity and map state, identical disposable cards, UP press/release true/false, WAIT control, 10 authentic 1280×800 X11 captures, both exits 0, both output checkpoints size/v4-header/SHA validated, and comparison report. Review screenshots to see whether UP changes focus versus WAIT; no tile confirmation.

Source checkpoint was independently restored in run #39780143613 and displayed 空き地 (Tanah kosong) value 140. Revision38's source loads technically but its first restored frame differs transiently from settled frames, so do not promote its output as a stable semantic checkpoint. Story Mode remains NOT COMPLETE.

---

## ACTIVE RUN — revision39 UP versus WAIT from trusted value-140 map state (22 October 2026, 20:11 WIB)

Run [#39784493293](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39784493293) is the only active player. Its checkout was verified at commit `4893e1e0eb6cdcaf9fff052c9c794ae62327858a`: marker sets `AB_ACTION=UP`, `AB_EXPECTED_STATE=map_after_move`, and source SHA `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`; workflow at blob `5a9b4697b0f19c1c5e8015852f5a90c57261ae9f` supports UP/DOWN/LEFT/RIGHT only for map-state A/B tests. The source is run #39779256427 / private artifact #12425858092 / `adaptive-cycle-01-f180.sstate`, previously restored independently by #39780143613 and visually identified as the map state with `空き地` (Tanah kosong), value 140.

Run started at 20:10:11 WIB; hard timeout about 20:30:11 WIB. No outcome/artifact audited yet; do not launch another player in parallel.

Required gates after completion: both fresh processes load exact source SHA and log SaveStateLoaded; F20 screenshots pixel-identical and both classify `map_after_move`; disposable cards identical; ACTION UP press/release readback true/false; control WAIT; ten authentic external X11 frames at 1280×800; both processes exit0; both output states externally validated for size, v4 header and SHA; report generated. Manually inspect whether UP moves focus toward the Naruto tile (`結界価値` (Nilai penghalang) 60) while WAIT remains at empty land140. Do not confirm a cell. Only classify the narrow focus change as VERIFIED if all gates and screenshots support it.

Revision38 is technically loadable but is not treated as a semantically stable focus checkpoint because F20 after restore transiently looked shifted before later frames settled. Use the stronger source SHA 58d8… for this experiment. Story Mode remains NOT COMPLETE.

---

## ACTIVE RUN — revision39 UP from empty-land140 versus WAIT (22 October 2026, 20:11 WIB)

Run [#39784493293](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39784493293) is the only active player. Its committed marker is verified at head SHA `4893e1e0eb6cdcaf9fff052c9c794ae62327858a` and the checked-out workflow supports map-state UP direction. Exact configuration:
SOURCE_RUN=39779256427; SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private; SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate; SOURCE_SHA256=`58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`; RESTORE_TEST=0; CONTINUATION_TEST=0; AB_TEST=1; AB_ACTION=UP; AB_EXPECTED_STATE=map_after_move; LOOP_CYCLES=2; REVISION=39.

Run started at 20:10:11 WIB; timeout approximately 20:30:11 WIB. Do not launch another player while active. Audit after completion: same source SHA for both processes, two explicit load events, F20 map-state pixel parity, identical cloned Memory Cards, UP press/release true/false, WAIT control, all 10 authentic 1280×800 captures, both exit0, both output checkpoint external size/v4-header/SHA validation, and comparison report. Inspect actual screens to see whether UP returns selection from `空き地` (Tanah kosong) value140 to Naruto's red tile value60. No confirmation input.

Caveat from revision38: post-second-DOWN candidate loads, but its F20 transient view (cell number near 100) settles back near the 140 area by F60. Do not use it as stable cursor source. Story Mode remains NOT COMPLETE.

---

## RESTORE AUDIT — revision38 loads, but second-DOWN focus is not stable across frames (22 October 2026, 20:05 WIB)

Run [#39783158903](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39783158903) completed with success at 20:03:51 WIB. Private artifact #12427598163 was downloaded and audited. It restored the revision37 ACTION output SHA-256 `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177` (21,162,960 bytes, v4), explicitly logged `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`, captured five genuine 1280×800 X11 screenshots, exited 0, and produced a new output checkpoint passing external size/header/SHA validation: `c4acb2b62a9891b597c1195a2dead7ccce902abddf0c5ec9b4c50b76142a7a33`, 21,162,978 bytes, v4.

**Do not promote the source as a semantically stable cursor checkpoint.** The actual C01-F20 screenshot temporarily shows the board scrolled with a visible cell number that appears to be 100; by F60/F100/F110/F180, the scene settles back to the value-140 area. The generic classifier remains `map_after_move` throughout, so it cannot disambiguate the focus. This fresh-process restore proves technical loadability but does not prove the second-DOWN tile/focus persists; the output produced by run38 is also unpromoted until its own separate restore, and it is not the preferred source.

### Next controlled test — revision39 UP vs WAIT from known cell-140 selection
Use the earlier ACTION checkpoint from run #39779256427 / artifact #12425858092 / `adaptive-cycle-01-f180.sstate`, SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`. It was independently restored by run #39780143613; its F20 displays the `空き地` (Tanah kosong) tile value140. Current workflow commit `b3c78426f8c11b406f0fedbffb01bd667e7ffb5e` expands map-state A/B to allow UP/DOWN/LEFT/RIGHT while retaining menu-state guards. Revision39 sets `AB_ACTION=UP`, `AB_EXPECTED_STATE=map_after_move`, `AB_TEST=1`, two cycles, restore/continuation tests off. Require exact source SHA both arms, two load events, F20 parity/state, equal cloned cards, UP press/release readback, WAIT control, ten authentic frames, both exits0, both output checkpoint validations and comparison report. Inspect whether UP returns the focus/panel to Naruto's tile value60 versus WAIT retaining value140. Do not confirm any tile.

Rules: the matched revision33 test remains VERIFIED for one DOWN from Naruto tile60 to `空き地` (Tanah kosong), barrier value140. Later repeated DOWN probes establish viewport/focus animation but not stable second-step selection; keep that semantics HYPOTHESIS/UNKNOWN until UP-vs-WAIT offers stronger paired evidence. Story Mode remains NOT COMPLETE.

---

## REVISION 38 RESTORE VERIFIED — 22 October 2026, 20:04 WIB

Run [#39783158903](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39783158903) completed with success. Private artifact #12427598163 was downloaded again; the retry passed ZIP integrity. Five authentic external-X11 screenshots at 1280×800 were validated, the load event and ADAPTIVE_RESTORE_TEST=PASS were logged, emulator exit was 0, and the new output checkpoint passed size/header/SHA validation.

The input source from run #39782011370, artifact #12426797521, file adaptive-cycle-01-f180.sstate, SHA-256 `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`, size 21,162,960 bytes, v4 header, is now independently restore-proven. Screenshots retain the board/cursor arrangement after the second DOWN. The number over the Naruto-marked cell is partly obscured by foliage in early frames; later frames clearly show 140, so the early apparent 100/142 is not treated as a value change.

The restore run's new output is not promoted: 21,162,978 bytes; v4; SHA-256 `c4acb2b62a9891b597c1195a2dead7ccce902abddf0c5ec9b4c50b76142a7a33`. It needs its own fresh-process restore.

Next: extend the bounded A/B workflow to permit UP, DOWN, LEFT and RIGHT only for map-navigation probes, excluding confirm buttons. Then run RIGHT versus WAIT from the proven source above, require all paired gates, and inspect authentic screenshots before classifying the result. Story Mode is NOT COMPLETE. No character movement, territory capture, ownership change or ending is established.

---

## VERIFIED RESULT — second DOWN shifts focus from empty land toward Naruto-marked cell (revision37, 22 October 2026, 19:56 WIB)

Run [#39782011370](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39782011370) completed with Actions success at 19:54:29 WIB. Private artifact #12426797521 was downloaded and audited, including actual screenshot pairs and all run logs.

All A/B gates passed:
- Both fresh emulator processes loaded exact source SHA-256 `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`, with `ExecutionFlow::SaveStateLoaded` in both sessions.
- Identical source-state frame F20 pixel parity: 1,024,000 of 1,024,000 pixels; both state classifiers `map_after_move`.
- Separate disposable Memory Card copies were byte-identical (SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`).
- ACTION sent one DOWN, press readback `true`, release `false`; CONTROL used WAIT.
- All ten authentic external-X11 captures passed validation at 1280×800. Both emulator sessions exited 0. Both output states passed post-exit size, `PCSX-Redux SaveState v4` header and SHA-256 validation. `ab-comparison-report.txt` was generated.

**VERIFIED, narrow visual effect:** from the scrolled map state with the empty-land tile value 140 selected, a second DOWN changes the board focus/view again. ACTION frames show the viewport shifted upward and the cursor now aligned toward the adjacent lower cell near the red Naruto-marked board position; CONTROL WAIT retains the pink 60 tile above and gray 140 tile under the cursor in the original framing. This supports a change in focused tile/view, not movement of Naruto or capture/ownership. The classifier still reports `map_after_move` for both; classification is based on direct screenshot comparison. Comparison: F60 780,637 differing pixels / mean absolute RGB 22.66488; F100 780,562 / 22.68538; F110 781,298 / 22.66071; F180 780,622 / 22.62887.

Output checkpoints in private artifact #12426797521, structurally validated but not promoted:
- ACTION after second DOWN, `adaptive-cycle-01-f180.sstate`: 21,162,960 bytes, v4 header, SHA-256 `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`.
- CONTROL WAIT, `adaptive-cycle-02-f180.sstate`: 21,163,049 bytes, v4 header, SHA-256 `cd7a70d67001e67177333df0c332e745e28c01c92851f92c21445250d108c63c`.

### Next — revision 38 restore-only checkpoint gate
Independently restore ACTION output SHA `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177` from run #39782011370 / private artifact `naruto-storymode-adaptive-player-private` / file `adaptive-cycle-01-f180.sstate`. Require `ExecutionFlow::SaveStateLoaded`, five authentic 1280×800 captures visibly retaining post-second-DOWN focus/view, emulator exit 0, and external output size/v4 header/SHA validation. The output newly emitted by this restore smoke remains unpromoted until it too is restored.

After promotion, begin actual gameplay interaction cautiously from the Naruto-marked cell. Add only one supported input at a time with paired controls; the current workflow only supports DOWN and TRIANGLE, so inspect `sendAction`/button mapping before adding other directions or any confirm input. Do not use Circle to skip dialogue; START only. Do not confirm a territory while semantics of selection vs movement are unresolved.

Story Mode remains **NOT COMPLETE**; no character movement/capture/ownership or ending is verified. Keep gameplay files private and out of Git.

---

## ACTIVE RUN — revision38 restore-only for second-DOWN board view (22 October 2026, 20:01 WIB)

Run [#39783158903](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39783158903) is the only active player. Its marker was verified:
SOURCE_RUN=39782011370; SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private; SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate; SHA-256 `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`; RESTORE_TEST=1; CONTINUATION_TEST=0; AB_TEST=0; LOOP_CYCLES=1; REVISION=38.

Run started at 20:00:55 WIB; workflow timeout about 20:20:55 WIB. Current outcome not yet available. Do not trigger another player run while active. Required: exact source checksum validation; `ExecutionFlow::SaveStateLoaded`; `ADAPTIVE_RESTORE_TEST=PASS`; five authentic external X11 images at 1280×800; visually confirm the second-DOWN viewport state at F20; exit0; and external output checkpoint size/v4-header/SHA validation. The source hash is promoted only if this restore succeeds. New output remains unpromoted until an additional independent restore.

Story Mode remains NOT COMPLETE. No character movement, capture, territory ownership, or ending is proven by the directional scroll probes. Keep all gameplay assets private and out of Git; skip dialogue with START.

---

## VERIFIED RESULT — second DOWN advances the board view again (revision37, 22 October 2026, 19:55 WIB)

Run [#39782011370](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39782011370) completed with success at 19:54:29 WIB. Private artifact #12426797521 was downloaded and all primary evidence checked.

Paired gates passed:
- Both fresh processes loaded identical input SHA-256 `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff` and each logged `ExecutionFlow::SaveStateLoaded`.
- Identical disposable Memory Card copies (SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`).
- Both F20 classifier state `map_after_move`; images exactly pixel-identical (1,024,000/1,024,000).
- ACTION DOWN press/release readback true/false; CONTROL WAIT/no input.
- Ten authentic external-X11 captures passed 1280×800; both emulator processes exited0; both output checkpoints passed post-exit size/header/SHA validation; A/B comparison report was generated.

**VERIFIED, narrow visual observation:** from the post-DOWN scrolled map state, a second DOWN triggers another upward viewport scroll and keeps the cell-information panel hidden, with the cursor over a lower area near the Naruto marker. WAIT allows the viewport to settle back to the prior board framing and the `空き地` (Tanah kosong) panel/value140 returns. The ACTION/control difference is substantial and consistent: F60 780,637 pixels / mean absolute RGB 22.66488; F100 780,562 / 22.68538; F110 781,298 / 22.66071; F180 780,622 / 22.62887. This verifies the input-dependent board focus/view response, but **not** the precise name/value of the lower target, player movement, capture, ownership change, or turn progression.

Output states in private artifact #12426797521, structurally valid but not yet promoted:
- ACTION after second DOWN: `adaptive-cycle-01-f180.sstate`, 21,162,960 bytes, v4, SHA-256 `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177`.
- CONTROL WAIT: `adaptive-cycle-02-f180.sstate`, 21,163,049 bytes, v4, SHA-256 `cd7a70d67001e67177333df0c332e745e28c01c92851f92c21445250d108c63c`.

### Next gate — revision38 restore-only
Restore the exact ACTION output from run #39782011370 / artifact #12426797521 / SHA `4989fc1f372f82d99e78b17f99b4af75c7bd0565b1aa93e9324b036431db9177` in a fresh emulator process. Require the load event, five authentic 1280×800 screenshots verifying its post-second-DOWN board view, exit0, and external output size/v4-header/SHA checks. Promote only the input source after this restore passes. The new output from revision38 stays unpromoted until its own fresh-process restore.

Story Mode remains **NOT COMPLETE**. No tile-confirmation, capture, ownership or ending is verified. Keep private game artifacts out of Git and use START for dialogue skipping.

---

## ACTIVE RUN — revision37 second DOWN from the scrolled board state (22 October 2026, 19:53 WIB)

Run [#39782011370](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39782011370) is the only active player. Its committed marker was verified:
SOURCE_RUN=39780755350; SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private; SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate; SHA-256 `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`; RESTORE_TEST=0; CONTINUATION_TEST=0; AB_TEST=1; AB_ACTION=DOWN; AB_EXPECTED_STATE=map_after_move; LOOP_CYCLES=2; REVISION=37.

Run started at 19:52:49 WIB; hard timeout about 20:12:49 WIB. Do not start another player while active. Audit only after completion: exact input hash in both fresh processes, two explicit load events, F20 expected state and exact screenshot parity, cloned cards identical, DOWN press/release true/false, WAIT control, ten genuine 1280×800 external-X11 captures, exit0 for both, both output states external size/v4 header/SHA validated, comparison report generated. Directly inspect paired screenshots at F60/F100/F110/F180 to see if a second DOWN changes board focus/view beyond the previous scroll. No tile confirmation, no actual movement/capture/ownership inference.

Story Mode remains NOT COMPLETE. Use START for dialogue, keep all gameplay assets/screenshots private and out of Git.

---

## RESTORE VERIFIED — post-DOWN scrolled board state survives fresh-process load (revision36, 22 October 2026, 19:51 WIB)

Run [#39781495023](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39781495023) completed successfully at 19:50:35 WIB. Its private artifact #12426677790 was downloaded and inspected. It loaded the exact ACTION checkpoint from revision35/run #39780755350: SHA-256 `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`, 21,162,766 bytes, v4. Log explicitly records `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`. Five genuine external-X11 images are 1280×800 and valid. Direct review of C01-F20 confirms the post-DOWN scrolled board framing persists; the previous empty-land info panel is still hidden while the cursor remains near the lower cell/Naruto marker. Emulator exit 0. Its output checkpoint passes external validation: 21,163,103 bytes, header `PCSX-Redux SaveState v4`, SHA-256 `4fd72504031c7aaa73bd7fa18e2f7a8d79b428643cea3c588ea4596ad5e90777`. This new output itself remains unpromoted until a fresh-process restore.

**Promoted source:** exact input checkpoint `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff` is now independently restore-proven and can be used for continuing experiments.

### Next — revision37: a second DOWN vs WAIT from scrolled board state
Use the same trusted input source checkpoint from run #39780755350, artifact `naruto-storymode-adaptive-player-private`, `adaptive-cycle-01-f180.sstate`, SHA above. Set `AB_TEST=1`, `AB_ACTION=DOWN`, `AB_EXPECTED_STATE=map_after_move`, `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `LOOP_CYCLES=2`, `REVISION=37`. Require all prior paired gates: source hash equality, two load events, exact F20 parity, same expected classifier state, identical card clones, DOWN press/release readback, ten authentic captures, both exits0, two external checkpoint validations, and generated comparison report. Inspect whether the board cursor/view advances again or the tile info changes. No Circle, no confirmation/selection; do not infer actual character movement/capture from scrolling or focus alone.

Story Mode remains **NOT COMPLETE**. Only board focus/view movement is established; no capture/territory ownership/ending proof. Keep all gameplay artifacts private/out of Git and use START for actual dialogue.

---

## ACTIVE RUN — revision36 restore-only test of post-DOWN scrolled map focus (22 October 2026, 19:49 WIB)

Run [#39781495023](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39781495023) is the only active player. Its committed marker was re-read and is correct: source run #39780755350, private artifact naruto-storymode-adaptive-player-private, checkpoint adaptive-cycle-01-f180.sstate, source SHA-256 `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`; RESTORE_TEST=1, CONTINUATION_TEST=0, AB_TEST=0, LOOP_CYCLES=1, REVISION=36.

Run started at 19:49:08 WIB; hard timeout about 20:09:08 WIB. Current outcome has not yet been audited. Do not launch any other player concurrently.

Acceptance gates: exact source checksum; `ExecutionFlow::SaveStateLoaded` plus `ADAPTIVE_RESTORE_TEST=PASS`; five genuine external-X11 screenshots at 1280×800; F20 visibly retains post-DOWN scrolled/focused map state (empty-land panel hidden, pointer toward lower cell); emulator exit0; newly emitted output checkpoint passes external size, `PCSX-Redux SaveState v4` header and SHA-256 check. Only if these pass is input hash b9717348… promoted to restorable. New output emitted by this restore run remains unpromoted until its own fresh-process restore.

Story Mode remains NOT COMPLETE. Verified board navigation currently means DOWN changes view/focus from empty-land140 and WAIT preserves it; do not infer capture/territory ownership. Keep all game assets private/out of Git, use START for dialogue.

---

## VERIFIED RESULT — DOWN from empty-land focus advances board focus and scrolls viewport (revision 35, 22 October 2026, 19:46 WIB)

Run [#39780755350](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780755350) completed successfully at 19:45:25 WIB. Raw logs and private artifact #12426786721 were audited, including direct inspection of authentic screenshots.

All matched A/B gates passed:
- Both fresh processes restore exact parent SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a` and explicitly log `ExecutionFlow::SaveStateLoaded`.
- Two Memory Card clones are byte-identical, hash `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- F20 states both classify `map_after_move`, and initial screenshots match pixel-for-pixel (1,024,000/1,024,000).
- ACTION sent one DOWN; press readback true, release false. CONTROL sends WAIT only.
- Ten authentic external-X11 captures validate at 1280×800, both processes exit 0, both checkpoint outputs pass size/header/SHA post-exit validation, and the comparison report was emitted.

**VERIFIED, narrow visual rule:** from the board state with `空き地` (Tanah kosong) value 140 focused, a single DOWN changes the observed board focus/view: the map scrolls upward and the empty-land information panel disappears, with the cursor now visually aligned toward the lower tile near Naruto's marker. WAIT preserves the empty-land panel/focus and the original board framing. This verifies a navigation/focus/view change only, not Naruto's movement, tile capture, ownership, or turn progress. Because the post-DOWN panel does not name the focused tile, do not assert more than the observed shift.

Comparison data: F60 783,594 differing pixels / mean absolute RGB 27.28084; F100 783,324 / 27.36300; F110 783,287 / 27.31514; F180 783,630 / 27.39113.

Output checkpoints (valid structure, not yet promoted):
- ACTION, run #39780755350 artifact #12426786721 `adaptive-cycle-01-f180.sstate`: 21,162,766 bytes, v4 header, SHA-256 `b9717348a478e63660784c9060beee84844fd30f739db5e331f78df12bf846ff`.
- CONTROL `adaptive-cycle-02-f180.sstate`: 21,162,804 bytes, v4 header, SHA-256 `e333d408701dcafb40a4d8489a88492fd772a5dc02bdd0fa7b3775bfc1ddc212`.

### Next gate — independently restore ACTION output
Run one restore-only fresh process against the exact ACTION output above. Require `ExecutionFlow::SaveStateLoaded`, five authentic 1280×800 captures; F20 should visually retain the post-DOWN scrolled/focused state (empty-land panel stays hidden / lower tile near Naruto's marker remains focused); exit 0; and external output size/v4-header/SHA validation. Only then promote the exact input hash `b9717348...` as restorable. The new output from that restore smoke will itself stay unpromoted until a separate restore succeeds.

Story Mode remains **NOT COMPLETE**. No actual capture/movement/ownership or ending is established. Keep ROM, BIOS, state, cards and screenshots private/out of Git. Use START for dialogue skipping.

---

## ACTIVE RUN — revision 35 DOWN versus WAIT from empty-land focus (22 October 2026, 19:44 WIB)

Run [#39780755350](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780755350) is currently `in_progress`, created at 19:43:50 WIB. Latest check: job is checking out the repository; there are no artifacts yet. The 20-minute deadline is approximately 20:03:50 WIB. Do not launch another player run.

Config is the verified/restorable map source run #39779256427 / artifact #12425858092 / `adaptive-cycle-01-f180.sstate`, source SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`; `AB_TEST=1`, `AB_ACTION=DOWN`, `AB_EXPECTED_STATE=map_after_move`, `LOOP_CYCLES=2`, `REVISION=35`. Audit source SHA equality, F20 pixel parity, both load events, actual DOWN press/release true/false and WAIT control, all 10 external-X11 1280×800 captures, exit0 for both processes, and both output state validations. Then manually inspect screenshots and decide the next tile focus only. No tile confirmation. Story Mode remains NOT COMPLETE.

---

## ACTIVE RUN — revision 35 DOWN from empty-land focus versus WAIT (22 October 2026, 19:44 WIB)

Run [#39780755350](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780755350) is the only active player. Marker revision 35 was verified at main: source run #39779256427 / private artifact naruto-storymode-adaptive-player-private / adaptive-cycle-01-f180.sstate / source SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`; `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `AB_TEST=1`, `AB_ACTION=DOWN`, `AB_EXPECTED_STATE=map_after_move`, `LOOP_CYCLES=2`, `REVISION=35`. The checked-out workflow blob `2f3d82359ebbbfeeb705005287c8af7ee3855df0` supports this map-state gate.

Started at 19:43:50 WIB; hard timeout about 20:03:50 WIB. At latest check, no outcome has been audited. Do not trigger a parallel player run.

Goal is only to observe whether DOWN from focused `空き地` (Tanah kosong, barrier value 140) changes which board cell is focused compared with WAIT. Require same source SHA in two fresh processes, explicit load events, exact F20 `map_after_move` visual/state parity, byte-identical Memory Cards, DOWN press/release true/false readback, ten authentic X11 images at 1280×800, both exits 0, external size/v4-header/SHA validation of both output states, and generated comparison report. Manually inspect C01/C02 F60/F100/F110/F180. Never claim movement/capture; no tile confirmation.

Story Mode remains NOT COMPLETE. Preserve privacy; no gameplay assets in Git; use START for dialogue.

---

## RESTORE VERIFIED — focus on empty-land tile 140 survives fresh process (revision 34, 22 October 2026, 19:42 WIB)

Run [#39780143613](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780143613) completed with success at 19:41:31 WIB. Private artifact #12425913759 was downloaded after completion and audited. It restored exact ACTION checkpoint from run #39779256427: 21,162,559 bytes, v4, SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`. Log explicitly states `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`. Five authentic external X11 screenshots were validated at 1280×800; the actual C01-F20 image visibly preserves `空き地` (Tanah kosong), `レベル` (Level) ---, `結界価値` (Nilai penghalang) 140, `耐久値` (Daya tahan) -/-. Emulator exited 0. Newly emitted state passed external validation: 21,163,018 bytes, v4 header, SHA-256 `75f0752616695e0d6d141e3cc051774f5e84defe6944371fb0bc34840c83ce9f`. The new output remains unpromoted because it has not itself been restored.

**Promoted source:** the exact input hash `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a) is now a trusted continuation source due to this fresh-process restore. It represents the board with empty-land tile value 140 focused.

### Next — revision 35: DOWN from empty land versus WAIT
Run one paired experiment from the same known-restorable source above. Use `AB_TEST=1`, `AB_ACTION=DOWN`, `AB_EXPECTED_STATE=map_after_move`, `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `LOOP_CYCLES=2`, `REVISION=35`. Required gates stay strict: exact input hash per arm, both F20 states `map_after_move`, pixel-identical F20 images, two load events, cloned Memory Cards identical, DOWN press/release readback true/false, 10 authentic 1280×800 screenshots, both emulator exits 0, both output checkpoint size/v4-header/SHA checks, and comparison report. Goal is only to observe the next focused tile and its information compared to WAIT. Do not press Circle or confirm/select a tile. If the result is visually clear, document focus movement only; do not infer actual character movement, capture, territory ownership or turn progress.

Story Mode remains NOT COMPLETE. Evidence must remain emulator-authentic and private; all ROM/BIOS/savestate/card/screenshot assets stay out of Git. Use START to skip dialogue.

---

## ACTIVE RUN — revision 34 restore-only for empty-land focus (22 October 2026, 19:40 WIB)

Run [#39780143613](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780143613) is the only active player. The committed marker is verified and correct:
SOURCE_RUN=39779256427; artifact naruto-storymode-adaptive-player-private; checkpoint adaptive-cycle-01-f180.sstate; source SHA-256 58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a; RESTORE_TEST=1; LOOP_CYCLES=1; REVISION=34.

It started at 19:39:28 WIB; hard timeout about 19:59:28 WIB. At the last check it was in Install X11 tools and prepare private workspace; no artifact is yet audited. Do not launch another player.

Acceptance: exact source checksum accepted, explicit ExecutionFlow::SaveStateLoaded, five authentic 1280×800 X11 images, F20 visibly shows 空き地 (Tanah kosong) focus / barrier value 140, emulator exit 0, and external validation of newly emitted checkpoint size, v4 header, SHA. The source candidate 58d8f551… is not promoted until this independent restoration succeeds. The new output from this restore run will itself remain unpromoted until restored again.

Verified board rule remains narrow: DOWN changes focus from Naruto's tile (value 60) to adjacent 空き地 (Tanah kosong, value 140); WAIT retains the Naruto tile. Does not prove a capture or actual character movement. Story Mode remains NOT COMPLETE.

---

## ACTIVE PLAYER — revision 34 restore-only map focus checkpoint (22 October 2026, 19:39 WIB)

Run [#39780143613](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39780143613) is `in_progress`, created 19:39:28 WIB. This restore-only test loads the revision-33 ACTION output SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a` from run #39779256427/private artifact #12425858092. Deadline is approximately 19:59:28 WIB if the 20-minute job limit is reached. No result/artifact yet. Do not launch a parallel player.

Expected checks: exact source validation; `ExecutionFlow::SaveStateLoaded`; `ADAPTIVE_RESTORE_TEST=PASS`; five authentic 1280×800 X11 captures; emulator exit 0; external validation of the new output; visual confirmation that F20 retains `空き地` (Tanah kosong) / barrier value 140 selected. No input should be sent. Do not promote the newly emitted output until it is independently restored.

---

## VERIFIED RESULT — DOWN changes focused tile on board (revision 33, 22 October 2026, 19:38 WIB)

Run [#39779256427](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39779256427) completed with Actions success at 19:37:15 WIB. Private artifact #12425858092 was fully downloaded and audited after upload completed.

All paired A/B gates passed:
- Both fresh processes restored the identical source checkpoint SHA-256 b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc, each with ExecutionFlow::SaveStateLoaded.
- Separate disposable Memory Card clones were byte-identical. Both F20 screenshots classify map_after_move and were pixel-identical across 1,024,000 pixels.
- ACTION sent one DOWN with readback true on press and false on release; CONTROL sent WAIT/no input.
- All 10 genuine external-X11 captures passed 1280×800 validation. Both emulator processes exited 0. Both output state files passed post-exit size, PCSX-Redux SaveState v4 header, and SHA-256 checks. The comparison report was generated.

**Rule: VERIFIED, scoped to this tested board state.** A single DOWN from the selected Naruto tile changes the focused tile to the adjacent empty land tile; WAIT leaves focus on the Naruto tile. ACTION C01-F60 visually shows 空き地 (Tanah kosong), レベル (Level) --- , 結界価値 (Nilai penghalang) 140, and 耐久値 (Daya tahan) -/-. CONTROL C02-F60 remains on Naruto with レベル (Level) 1, 結界価値 (Nilai penghalang) 60, and 耐久値 (Daya tahan) 2/2. This verifies focus/selection movement only; it does NOT prove that Naruto moved, captured the tile, or changed territory ownership. Classifier remains map_after_move in both arms, so direct screenshot review is the visual basis.

Image comparison: F60 719,192 differing pixels / mean absolute RGB 26.80650; F100 719,200 / 26.89202; F110 719,631 / 26.85752; F180 718,997 / 26.84018.

Private checkpoint outputs in artifact #12425858092 (valid structure, not yet promoted):
- ACTION focus-on-empty-land candidate: 21,162,559 bytes, SHA-256 58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a.
- CONTROL focus-on-Naruto: 21,162,390 bytes, SHA-256 3796ff4ba91fef93ddf1078daa1785e043c3d5b5424a03c8cb53a62c6d3858a4.

### Next gate — restore ACTION focus checkpoint
Run one restore-only smoke from run #39779256427/artifact naruto-storymode-adaptive-player-private/checkpoint adaptive-cycle-01-f180.sstate/SHA 58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a. Require ExecutionFlow::SaveStateLoaded, five authentic X11 frames with 空き地 (Tanah kosong) / value 140 still focused, exit 0, and external output checkpoint size/header/SHA validation. Promote only that exact source once it restores successfully; the output produced by the restore-only run would require its own fresh-process restore before promotion. Do not select/confirm the tile yet.

Story Mode remains NOT COMPLETE; no ending/result evidence exists. Keep ROM/BIOS/savestates/Memory Cards/screenshots private and out of Git. Use START for dialogue skipping.

---

## VERIFIED — DOWN changes map focus to the adjacent empty land tile (22 October 2026, 19:37 WIB)

Run [#39779256427](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39779256427), revision 33, completed with `success`. Private artifact #12425858092 was audited (logs, screenshots, comparison report, card clones, and both state files). All required matched A/B gates passed:
- Both fresh emulator processes loaded the exact same verified map source SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`; each logged `ExecutionFlow::SaveStateLoaded`.
- Memory Card clone SHA identical in both arms: `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- F20 captures classified `map_after_move` in both arms and were pixel-identical across 1,024,000 pixels.
- ACTION DOWN button readback passed on press (`true`) and release (`false)); control was NONE/WAIT.
- Ten authentic external-X11 screenshots (five per branch) passed 1280×800 integrity validation; both emulator sessions exited with code 0.
- Both output states passed post-exit external size/header/SHA-256 validation.
- Private comparison report: F60 719,192 different pixels / RGB MAD 26.80650; F100 719,200 / 26.89202; F110 719,631 / 26.85752; F180 718,997 / 26.84018.

**Rule: VERIFIED, scoped to this specific map state.** One DOWN moves the map's selected/focused tile from the Naruto tile with `レベル` (Level) 1, `結界価値` (Nilai penghalang) 60, `耐久値` (Daya tahan) 2/2 to the adjacent tile labeled `空き地` (Tanah kosong), with barrier value 140, level `---`, and durability `-/-`. The WAIT branch stays on the original tile. This is selection/focus movement only; it does **not** establish that Naruto physically moves, captures the tile, or changes ownership. The generic classifier remains `map_after_move` for both images, so direct screenshot comparison is the decisive evidence.

Outputs in artifact #12425858092 (valid structure only, **not promoted yet**):
- ACTION `adaptive-cycle-01-f180.sstate`: 21,162,559 bytes, v4 header, SHA-256 `58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a`.
- CONTROL `adaptive-cycle-02-f180.sstate`: 21,162,390 bytes, v4 header, SHA-256 `3796ff4ba91fef93ddf1078daa1785e043c3d5b5424a03c8cb53a62c6d3858a4`.

### Next checkpoint gate — revision 34 restore-only
Start one restore-only test using the ACTION checkpoint above, then visually confirm the empty-land focus survives in the fresh process:
```
MODE=ADAPTIVE
SOURCE_RUN=39779256427
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=58d8f551ccf3a93fff21bb2cb9ae4930e1e1db033591082597ba4dfb47b20f7a
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=DOWN
LOOP_CYCLES=1
REVISION=34
```
Require explicit load event, five authentic 1280×800 X11 captures, exit 0 and external output state validation; do not send any gameplay input. Promote the source checkpoint only after the fresh-process F20 image visibly retains the `空き地` (Tanah kosong) / 140 focus. The new output emitted by revision 34 is itself unpromoted until independently restored.

Story Mode remains **NOT COMPLETE**. No ending/results screen has been verified. Keep all game artifacts private/out of Git; use START to skip Story Mode dialogue.

---

## ACTIVE PLAYER — revision 33 corrected map DOWN A/B (22 October 2026, 19:33 WIB)

Run [#39779256427](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39779256427) is currently `in_progress`, started at 19:32:59 WIB. Latest step: `Install X11 tools and prepare private workspace`. 20-minute deadline is approximately 19:52:59 WIB. No artifact/result is available yet; do not start any parallel player run.

This is the corrected A/B rerun of revision 32 from the trusted map-view source run #39776518701 / artifact #12425305517 / `adaptive-cycle-01-f180.sstate` / SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`. Marker explicitly has `AB_EXPECTED_STATE=map_after_move`, `AB_TEST=1`, `AB_ACTION=DOWN`, `LOOP_CYCLES=2`, `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `REVISION=33`.

Revision 32's raw screenshots suggested DOWN focuses the empty-land tile `空き地` (Tanah kosong) with displayed barrier value 140 instead of the Naruto tile with value 60, but run32 conclusion was failure because its old checkout hard-coded expected menu state. Do not upgrade this tentative map-navigation rule until run33 completes every expected-state/parity, load/input/capture/exit/checkpoint gate and its private screenshots are visually audited.

---

## ACTIVE RUN — revision 33 map DOWN versus WAIT (22 October 2026, 19:33 WIB)

Run [#39779256427](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39779256427) is the only active player. It uses the corrected marker with AB_EXPECTED_STATE=map_after_move and the proven board checkpoint SHA b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc. The prior revision 32 run #39777917775 completed with failure only because its old checkout hard-coded menu state; its actual DOWN input and captures are diagnostic, not accepted A/B.

Run #39779256427 started at 19:32:59 WIB; hard timeout about 19:52:59 WIB. Do not start a parallel player. When it completes, audit current job steps/logs/artifact and enforce all gates: same source SHA in both processes, two explicit load events, both F20 states exactly map_after_move, pixel-identical F20 screenshots, identical cloned Memory Cards, DOWN press/release readback true/false, 10 genuine X11 screenshots at 1280×800, emulator exits 0, both output checkpoints validated for size/v4 header/SHA, and generated ab-comparison-report.txt. Manually inspect C01/C02 frames F60/F100/F110/F180.

Hypothesis to test (not yet verified): DOWN shifts the board focus from Naruto's tile (Level 1, barrier value 60, durability 2/2) to adjacent 空き地 (Tanah kosong) with barrier value 140, while WAIT preserves the original selection. Only upgrade to VERIFIED if revision 33 passes every required gate and authentic paired images support it. Do not confirm/select a tile.

Story Mode remains NOT COMPLETE. Keep all gameplay images/ROM/BIOS/states/cards private and out of Git; use START for dialogue.

---

## LATEST DIAGNOSTIC — revision 32 captured map DOWN effect, but stale validator rejected it (22 October 2026, 19:30 WIB)

Run [#39777917775](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39777917775) finished with conclusion failure at 19:29:26 WIB. This is a validator/configuration failure, not a failed emulator session: both fresh processes loaded the same known-restorable map parent SHA-256 b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc and each logged ExecutionFlow::SaveStateLoaded. Ten authentic external-X11 screenshots (five per branch) passed 1280×800 validation; F20 images were manually compared and are pixel-identical (0 differing / 1,024,000 pixels); DOWN press/release readbacks were true/false; both emulator processes exited 0; both output checkpoints passed external post-exit size/header/SHA validation. Private artifact #12426395775 contains evidence.

The exact cause of the action workflow failure is that checkout SHA b77f74af5b258dfcd7d8bfbeeeca0c685c5fc7b7 has a state-parity validator hard-coded to expect menu_or_unknown_choice. Actual paired F20 states were both map_after_move, which is correct for the pinned source; its strict Python gate therefore stopped before writing ab-comparison-report.txt. The action branch did send DOWN, logged in pcsx-adaptive-cycle-1.stdout; control sent WAIT. The run must not be counted as a clean A/B workflow pass, and its output checkpoints are not promoted.

Manual inspection of private artifact screenshots suggests this directional effect, still **HYPOTHESIS pending corrected paired run**:
- ACTION C01-F60: panel shows 空き地 (Tanah kosong), レベル (Level) ---, 結界価値 (Nilai penghalang) 140, 耐久値 (Daya tahan) -/-.
- CONTROL C02-F60: panel remains on Naruto with レベル (Level) 1, 結界価値 (Nilai penghalang) 60 and 耐久値 (Daya tahan) 2/2.
The paired image differences are large and consistent (F60 719,192 pixels / mean absolute RGB 26.806502; F100 719,200 / 26.892019; F110 719,631 / 26.857518; F180 718,997 / 26.840178). This appears consistent with DOWN changing the focused tile from Naruto's tile to the neighboring empty land marked 140, but the semantic rule remains a HYPOTHESIS until a rerun passes the corrected workflow's explicit map-state acceptance gate.

Output checkpoint hashes (valid structure, but neither promoted):
- ACTION: 21,162,270 bytes, SHA-256 927d87eb775f375deb47af348d837319ceb65d4baa58c8523042090f377b2efa.
- CONTROL: 21,162,320 bytes, SHA-256 7aaf5fc780748fee27a84669a942c598e8340e9952234e47bab47795755d67a1.

### Corrected revision 33
The current main workflow now supports AB_EXPECTED_STATE; the run above used an older workflow checkout and did not consume that field. Launch exactly one corrected rerun from the unchanged known-restorable parent, with AB_EXPECTED_STATE=map_after_move, AB_ACTION=DOWN, AB_TEST=1, LOOP_CYCLES=2, RESTORE_TEST=0, CONTINUATION_TEST=0, REVISION=33. Require the same strict gates and the comparison report to be generated successfully. Do not promote either revision-32 output checkpoint. Inspect the actual screenshots; do not use Circle/confirm, and do not claim tile movement VERIFIED before the corrected experiment passes.

Story Mode remains NOT COMPLETE. No authenticated ending/results evidence exists. Keep ROM, BIOS, savestates, Memory Card, and gameplay screenshots private and out of Git; use START for dialogue skips.

---

## CORRECTION — revision 32 is not guaranteed to fail closed (22 October 2026, 19:25 WIB)

Inspection of the exact workflow file at run #39777917775's checkout SHA b77f74af5b258dfcd7d8bfbeeeca0c685c5fc7b7 shows the old Lua precondition accepts either menu_or_unknown_choice or map_after_move when the classifier's policy action is WAIT. Thus when this run reaches the known map_after_move F20 state, the ACTION arm may send its configured DOWN. The bug is in later shell validation: it still insists both F20 classifier states are menu_or_unknown_choice, which is inconsistent with this run's map-view source. Therefore this run may collect useful paired screenshots and checkpoints but still fail the final workflow gate. This exact outcome is not known until logs/artifact are audited.

The current player run remains #39777917775, the only active player. Do not launch another run until it finishes. Keep the source pinned to map-view checkpoint SHA b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc. After completion, examine actual input press/release readback, both load events, all 10 real captures, parity, exit codes and checkpoint validation. Classify the directional rule no higher than HYPOTHESIS if the final pair gate fails, even if images suggest a transition. The corrected workflow at commit 4c074472e885c75ce618e4e0f5aefd6a8833a0c9 has explicit AB_EXPECTED_STATE handling; a clean rerun requires a new marker with AB_EXPECTED_STATE=map_after_move after the current run ends.

Story Mode remains NOT COMPLETE.

---

## ACTIVE RUN / CONFIGURATION BLOCKER — revision 32 fail-closed audit (22 October 2026, 19:24 WIB)

Run [#39777917775](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39777917775) is the only active player run. Its marker revision 32 was committed without AB_EXPECTED_STATE=map_after_move, even though its source SHA is the board/map checkpoint. The workflow default for missing AB_EXPECTED_STATE is menu_or_unknown_choice. Therefore the map-view F20 precondition should fail closed and the action branch should be reduced to WAIT rather than sending DOWN; expected final outcome is validator failure. This is an observed configuration mismatch, not a gameplay result. Do not start another player while run #39777917775 is active.

- Source intended by marker: run #39776518701, artifact naruto-storymode-adaptive-player-private, checkpoint adaptive-cycle-01-f180.sstate, SHA-256 b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc.
- Current latest check: run still in progress at Install X11 tools and prepare private workspace; no artifact yet. Started 19:23:17 WIB; hard timeout about 19:43:17 WIB.
- After it terminates, audit its logs/artifact. If it fails at the precondition as expected, retain the source checkpoint as the trusted input. Then correct marker to a new revision (revision 33, not 32) including AB_EXPECTED_STATE=map_after_move. The workflow update commit 4c074472e885c75ce618e4e0f5aefd6a8833a0c9 supports the explicit state gate; do not rerun until the missing marker field is confirmed from the actual committed marker.
- Keep the exact source pinned; no parallel player. Map navigation remains HYPOTHESIS until a corrected, fully paired DOWN-vs-WAIT test completes.

Story Mode remains NOT COMPLETE. Use START to skip dialogue, preserve real emulator screenshots only, translate Japanese labels alongside them, and keep ROM/BIOS/state/cards/screenshots out of Git.

---

## RESTORE VERIFIED — board/map checkpoint independently loaded (22 October 2026, 19:21 WIB)

Run [#39777301626](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39777301626) completed with Actions success. It restored the exact TRIANGLE/ACTION map-view checkpoint from run #39776518701: 21,163,227 bytes, v4 header, SHA-256  b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc. The log explicitly records ExecutionFlow::SaveStateLoaded and ADAPTIVE_RESTORE_TEST=PASS; five authentic external-X11 captures at 1280×800 were validated; the F20/F60/F100/F110/F180 visual sequence retained the board/map view; emulator exit was 0; and the output file passed external size/header/SHA validation. Private artifact #12423949987 contains the screenshots/logs.

The new output from the restore smoke is NOT promoted until it too is independently restored: 21,162,251 bytes, v4 header, SHA-256 a2a3c36918155dc4356da2664bfa7880c9605c62260389b85f85262c942b2fe7.

### Next experiment — revision 32, map DOWN vs WAIT
The adaptive workflow validator previously hard-coded A/B frame-state parity to the right-side menu. Workflow update commit 4c074472e885c75ce618e4e0f5aefd6a8833a0c9 now introduces explicit AB_EXPECTED_STATE, allowing map_after_move A/B only with AB_ACTION=DOWN. Revision 32 tests one DOWN on the map board against a WAIT control, both restoring the already-proven source b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc in independent processes. Required gates: both F20 captures classify exactly map_after_move; pixel parity; two load events; press/release true/false; 10 authentic X11 captures; exit 0; and external validation of both output checkpoints. Inspect screenshots at F60/F100/F110/F180 to see whether the map selection/board state changes. This is a directional probe only: do not use Circle or confirm/select a destination. If a tile or new state appears, stop and inspect before another input.

Story Mode remains NOT COMPLETE. No verified ending/results evidence exists. Continue to classify each rule VERIFIED/HYPOTHESIS/UNKNOWN and keep all game assets/screenshots/savestates/Memory Cards private and out of Git.

---

## ACTIVE PLAYER — revision 32 map DOWN versus WAIT (22 October 2026, 19:23 WIB)

Run [#39777917775](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39777917775) was triggered from marker revision 32 and is currently `in_progress`. It started at 19:23:17 WIB. Latest Actions check shows the `Install X11 tools and prepare private workspace` step active; workflow timeout is 20 minutes (deadline approximately 19:43:17 WIB from start). No artifact or experiment result exists yet. Do not start any other player run.

This is a matched A/B using the trusted map-view checkpoint from run #39776518701 / artifact #12425305517, SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`, with ACTION=DOWN vs control WAIT, two fresh processes. Workflow commit `5f8ae63b4374cb730ef197d797dffd0e823db141` allows the calibrated starting state `map_after_move` only when classifier action is WAIT. Audit the exact run after it completes: F20 image/state parity, press/release true/false readback, two load events, all 10 authentic X11 captures, accepted exits and both post-exit output checkpoint validations. Inspect actual screenshots for what DOWN changes on the map; do not confirm any destination.


---

## RESTORE VERIFIED — map-view checkpoint promoted; next probe map navigation (22 October 2026, 19:20 WIB)

Run [#39777301626](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39777301626) completed with Actions success at 19:20:11 WIB. Private artifact #12423949987 was audited; the actual C01-F20 image was opened and visually confirms the map/tile screen remains visible after restore.

- Source checkpoint from run #39776518701, artifact #12425305517: `adaptive-cycle-01-f180.sstate`, source SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`, size 21,163,227 bytes, `PCSX-Redux SaveState v4` header.
- New emulator process logged `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS` for the exact source SHA. Five authentic external-X11 screenshots validated at 1280×800; F20, F60, F100, F110 and F180 consistently classify as `map_after_move` and manually inspected F20 shows the map, tile values, Naruto panel (`レベル` (Level) 1, `結界価値` (Nilai penghalang) 60, `耐久値` (Daya tahan) 2/2) and `× もどる` (X: Kembali). No gameplay input was sent during restore-only testing.
- Emulator exit code 0. New output checkpoint passed external validation: 21,162,251 bytes, v4 header, SHA-256 `a2a3c36918155dc4356da2664bfa7880c9605c62260389b85f85262c942b2fe7`. **This new output is not promoted** until it itself passes an independent fresh-process restore.
- Promote source `b5715ba7...` as the trusted, restorable map-view checkpoint (not the new `a2a3...` output).

### Agent safety adjustment
The workflow's A/B initial precondition previously accepted only `menu_or_unknown_choice`, which blocked a controlled experiment from this calibrated map screen even though the screenshot classifier reliably returns `map_after_move` with action WAIT. Workflow commit `5f8ae63b4374cb730ef197d797dffd0e823db141` changes the precondition to accept either `menu_or_unknown_choice` or `map_after_move` only when the classifier action is WAIT. The control policy guard already permits `map_after_move` + WAIT. No emulator run was triggered by this workflow-only change.

### Next exact controlled experiment — revision 32: DOWN versus WAIT on the map
Use the promoted map checkpoint from run #39776518701:
```
MODE=ADAPTIVE
SOURCE_RUN=39776518701
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc
RESTORE_TEST=0
CONTINUATION_TEST=0
AB_TEST=1
AB_ACTION=DOWN
LOOP_CYCLES=2
REVISION=32
```
The next test compares one DOWN press against NONE/WAIT from two fresh processes with the exact same source and identical cloned Memory Cards. Require two `ExecutionFlow::SaveStateLoaded` events, pixel-identical/state-identical F20 frames, DOWN press/readback true and release/readback false, ten authentic 1280×800 X11 screenshots, accepted exits and both post-exit checkpoint size/header/SHA validations. Manually inspect F60/F100/F110/F180 to determine whether DOWN moves the map cursor/selection, changes the current tile/position, or does something else. Do not press Circle or confirm any map destination. If the screen response is ambiguous, preserve HYPOTHESIS/UNKNOWN.

Rules now VERIFIED, only in the tested contexts:
1. DOWN from `情報` (Informasi) highlights `マップを見る` (Lihat peta).
2. TRIANGLE while `マップを見る` (Lihat peta) is highlighted opens the tile/map view; WAIT leaves the menu open.
3. Checkpoint SHA `b5715ba7...` restores in a new process and visually retains that map view.

Story Mode remains **NOT COMPLETE**; no ending/result evidence has been observed. Keep all gameplay files private/out of Git and skip Story Mode dialogue with START.

---

## VERIFIED RESULT — revision 30 Triangle opens map view (22 October 2026, 19:15 WIB)

Run [#39776518701](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39776518701) completed with Actions `success`; raw logs and private artifact #12425305517 were audited. Both arms restored the same independently restorable parent SHA-256 `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7` in separate fresh emulator processes. Both logged `ExecutionFlow::SaveStateLoaded`, used equal cloned Memory Cards (SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`), and started with identical F20 pixels (1,024,000/1,024,000) and matched generic classifier state. Triangle press/release readback passed true/false. Ten authentic external-X11 captures were validated at 1280×800; both emulator processes exited 0; both output checkpoints passed external post-exit size/header/SHA verification.

Visual review of the actual screenshot files establishes a narrow **VERIFIED rule**: when `マップを見る` (Lihat peta) is highlighted, one `TRIANGLE` input opens the board/map view; NONE/WAIT leaves the right-side menu open with `マップを見る` (Lihat peta) still highlighted. ACTION F60/F100/F110/F180 are recognized as `map_after_move` by the existing image classifier; control frames remain `menu_or_unknown_choice`. The action/control visual comparisons report: F60 286,259 pixels / mean abs RGB 21.80974; F100 282,661 / 21.70455; F110 279,162 / 21.18977; F180 286,921 / 21.80548. Screenshot details include Naruto's board-marker panel with `レベル` (Level) 1, `結界価値` (Barrier value) 60 and `耐久値` (Durability) 2/2, and the footer `△ マップ` (Triangle: Map). No map destination was selected.

Outputs in private artifact #12425305517:
- ACTION/map-view candidate `adaptive-cycle-01-f180.sstate`: 21,163,227 bytes; header `PCSX-Redux SaveState v4`; SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`.
- CONTROL/menu `adaptive-cycle-02-f180.sstate`: 21,163,215 bytes; v4 header; SHA-256 `dc91b2756581456e75dee8cd836dc7b3c1e43fde88978dbf15545f231a6c0f98`.

**Promotion gate:** the ACTION map-view checkpoint is still a candidate, not yet trusted for continuation. Next run #31 must restore that exact ACTION output in a separate fresh emulator process and verify `ExecutionFlow::SaveStateLoaded`, five authentic X11 captures showing map view, accepted exit, and external output size/header/SHA validation. Do not start a further player experiment until this restore-only run finishes. If restore passes, this checkpoint becomes the next continuation source. Then cautiously test one DOWN from map view versus WAIT only after the restored state is confirmed; do not pick/select tiles without inspecting each result.

Rules verified to date remain narrowly scoped: from the observed menu states, successive DOWN inputs moved Roulette→Ninjutsu, Ninjutsu→Information, and Information→View map; from View map, TRIANGLE opens the board/map view. No territory-selection, tile movement, capture, combat, Chakra cost, turn order, win/loss or ending rule is established by these menu probes.

Story Mode remains **NOT COMPLETE**. No verified ending/results screen exists. Continue START-only dialogue skipping, translate Japanese terms beside them, keep game files/BIOS/savestates/Memory Cards/screenshots private and out of Git.

---

## VERIFIED — TRIANGLE opens the map view from the selected Map row (22 October 2026, 19:15 WIB)

Run [#39776518701](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39776518701) completed with success at 19:14:34 WIB. I audited private artifact #12425305517 including the actual X11 screenshots, branch logs, comparison report, input readback, and output checkpoint validation.

- Both fresh emulator processes loaded the exact independently restored source SHA-256 `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7`, with `ExecutionFlow::SaveStateLoaded` in each. The separate ACTION/CONTROL Memory Cards were hash-identical.
- F20 images matched exactly across 1,024,000 pixels and showed `マップを見る` (Lihat peta) selected. ACTION sent TRIANGLE with press/release readback `true`/`false`; CONTROL sent WAIT. Ten authentic external-X11 captures (five per arm) were validated at 1280×800. Both emulator processes exited 0.
- Actual screenshots show that ACTION enters a tile/map view by F60 and remains there through F180. The screen displays hex/tile positions, visible values such as 60, 100 and 140, and a character panel with `レベル` (Level) 1, `結界価値` (Nilai penghalang) 60, and `耐久値` (Daya tahan) 2/2. Its footer is `× もどる` (X: Kembali). The control stays in the prior right-hand menu with `マップを見る` (Lihat peta) highlighted. No map destination/tile was selected after opening the map.
- Paired image comparison: F60 286,259 differing pixels / mean absolute RGB difference 21.80974; F100 282,661 / 21.70455; F110 279,162 / 21.18977; F180 286,921 / 21.80548. In ACTION the generic classifier changes to `map_after_move`; control remains `menu_or_unknown_choice`. The conclusion is grounded in manual visual review of the genuine paired screenshots, not just the classifier label.
- Output checkpoint validations passed after process exit:
  - ACTION `adaptive-cycle-01-f180.sstate`: 21,163,227 bytes, v4 header, SHA-256 `b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc`.
  - CONTROL `adaptive-cycle-02-f180.sstate`: 21,163,215 bytes, v4 header, SHA-256 `dc91b2756581456e75dee8cd836dc7b3c1e43fde88978dbf15545f231a6c0f98`.
  Both outputs remain unpromoted until individually restored in a new process.

**Rule: VERIFIED, limited to this exact menu/checkpoint state.** With `マップを見る` (Lihat peta) highlighted, one TRIANGLE input opens the tile/map view; WAIT leaves the menu open. This establishes map-view entry, not navigation/selection mechanics or battle rules.

### Immediate next step — revision 31 restore-only
Test the ACTION output itself in a new process (do not send gameplay input):
```
MODE=ADAPTIVE
SOURCE_RUN=39776518701
SOURCE_ARTIFACT=naruto-storymode-adaptive-player-private
SOURCE_CHECKPOINT=adaptive-cycle-01-f180.sstate
SOURCE_SHA256=b5715ba7af58abb8e9e32d32cb489cbf37979d7fd56a2221ad15f39a0cd2a8fc
RESTORE_TEST=1
CONTINUATION_TEST=0
AB_TEST=0
AB_ACTION=DOWN
LOOP_CYCLES=1
REVISION=31
```
Require the load event, five valid authentic 1280×800 X11 captures, exit 0/accepted exit, and external output checkpoint validation. Verify F20 still shows the map/tile view and no input was sent. Only then promote the source state as the trusted map-view checkpoint. Do not start a map-movement probe until this inspection/restore step is complete.

Story Mode remains **NOT COMPLETE**. The game-ending/result screen has not been observed. Keep all gameplay files private/out of Git; use START for dialogue skipping, never Circle for dialogue.

---

## RESTORE VERIFIED — ACTION checkpoint from revision 28 (22 October 2026, 19:11 WIB)

Restore-only run [#39776089816](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39776089816) completed with success at 19:10:59 WIB. Artifact #12425065836 was audited. It loaded the exact revision-28 ACTION output from #39775176728: SHA-256 `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7`, size 21,162,344 bytes, v4 header. The log records `ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS`; five authentic external-X11 screenshots at 1280×800 passed validation, exit code was 0, and F20 visibly retains `マップを見る` (Lihat peta) highlighted. Its source is now proven restorable and is promoted as the trusted menu-selection checkpoint.

The restore run's newly emitted output is structurally valid but not promoted: 21,163,104 bytes, header `PCSX-Redux SaveState v4`, SHA-256 `9d1ed105227c095c42396595bccd51ecf06f564ae5342f01377dec1f3aa94292`. This new output would itself require a fresh-process restore before use.

### Next controlled experiment — revision 30: TRIANGLE vs WAIT
Now perform one matched A/B from the independently restored map-row selection, using the trusted original source checkpoint from run #39775176728 (source SHA above). Run only after revision 29 is complete; it is complete. Set the marker to `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `AB_TEST=1`, `AB_ACTION=TRIANGLE`, `LOOP_CYCLES=2`, `REVISION=30`. ACTION sends one Triangle input; CONTROL waits. Require same source SHA per arm, exact F20 parity, input true/false readback, two load events, ten authentic 1280×800 X11 captures, accepted exits, and post-exit size/header/SHA validation for both outputs. Visually determine whether Triangle opens the map screen. Stop at the map screen, do not choose any destination, and do not use Circle for dialogue skipping. Only classify as VERIFIED if paired evidence clearly shows a map screen in ACTION and not in WAIT.

The narrow rule from revision 28 remains **VERIFIED**: DOWN from `情報` (Informasi) moves the highlight to `マップを見る` (Lihat peta); NONE/WAIT leaves Information highlighted. Story Mode remains **NOT COMPLETE**; no verified ending/results evidence exists.

---

## LATEST VERIFIED RESULT — revision 28 DOWN versus NONE from Information (22 October 2026, 19:05 WIB)

Run [#39775176728](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39775176728) completed with Actions conclusion `success` at 19:04:52 WIB. The raw job log and private artifact #12424660712 were audited; this conclusion is based on the artifact and acceptance evidence, not the Actions badge alone.

- Configuration matched the planned experiment: `SOURCE_RUN=39768787669`, parent SHA-256 `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`, `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `AB_TEST=1`, `AB_ACTION=DOWN`, `LOOP_CYCLES=2`, `REVISION=28`.
- Both branches restored the exact same parent hash in separate fresh emulator processes and logged `ExecutionFlow::SaveStateLoaded`. Separate ACTION/CONTROL Memory Card copies had identical SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- Parent screenshots C01-F20 and C02-F20 were identical pixel-for-pixel (1,024,000 pixels); both showed the right-side menu with `情報` (Informasi) highlighted. DOWN input readback passed on press (`true`) and release (`false); control branch executed WAIT/no input.
- All 10 authentic external-X11 captures were validated as 1280×800, with 5 screenshots per branch. Visual review of the actual images confirms that ACTION C01-F60/F100/F110/F180 highlights `マップを見る` (Lihat peta), while control C02-F60/F100/F110/F180 remains on `情報` (Informasi). The comparison report records 14,636 differing pixels and mean absolute RGB difference 1.05798 at each post-action phase.
- Both emulator processes completed with exit code 0. External post-exit checkpoint validation passed:
  - ACTION `adaptive-cycle-01-f180.sstate`: 21,162,344 bytes, header `PCSX-Redux SaveState v4`, SHA-256 `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7`.
  - CONTROL `adaptive-cycle-02-f180.sstate`: 21,162,426 bytes, header `PCSX-Redux SaveState v4`, SHA-256 `30b062df8985fa79f8c9f79e076cb464f1ff73143103e249dba5d35ca94324d5`.
- Private artifact: [run artifact #12424660712](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39775176728). Gameplay images, savestates and Memory Cards remain private and are not committed to Git.

**Rule: VERIFIED, limited to this exact menu/checkpoint state.** One DOWN from `情報` (Informasi) moves the highlight to `マップを見る` (Lihat peta); NONE/WAIT leaves it at Informasi. This proves selection movement only, not that the map screen has opened. The automated classifier still reports `menu_or_unknown_choice`, so evidence for the row change is the manually inspected paired authentic screenshots plus pixel comparison, not a semantic classifier label.

**Checkpoint promotion gate:** do not use either output checkpoint as the trusted continuation source until that exact output has been loaded and inspected in a separate fresh emulator process. Next run is a single-cycle `RESTORE_TEST=1` from the ACTION checkpoint SHA `0f0ea089fb9f3cdad32bf0d04de399ffa24dd927d3f2bb2731a401ec3bf783b7` in run #39775176728. If the five post-load captures, explicit load event, accepted exit and external output validation pass, the ACTION checkpoint is proven restorable. Then use that restored selection state for a short matched Triangle-versus-WAIT experiment to establish what opens the map; do not select any map destination before inspecting the map screen. Do not start parallel player runs.

Story Mode remains **NOT COMPLETE**. There is no verified ending/results evidence. Continue using START to skip actual Story Mode dialogue and classify every game rule VERIFIED/HYPOTHESIS/UNKNOWN.

---

## CURRENT ACTION — revision 28 matched DOWN/NONE run queued (22 October 2026, 19:02 WIB)

Marker revision 28 was committed at `e31ebb2afbe1145746e480e9a0f020854621a82f`, triggering [run #39775176728](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39775176728). At the latest check it is **in progress**, with the step `Install X11 tools and prepare private workspace` active. It started at 19:02:38 WIB; the workflow job has a 20-minute hard timeout (around 19:22:38 WIB if not completed earlier). It tests ACTION=DOWN against NONE/WAIT from the known-restorable Information parent `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`; 2 cycles, `AB_TEST=1`. Do not start another player run. Next chat must check this exact run, its latest job steps and artifacts/logs, then apply the strict paired-evidence gates documented here. Job timeout is 20 minutes after a runner starts; queued wait has no reliable ETA. Story Mode remains NOT COMPLETE.

---

## LATEST RESULT — restore smoke passed; next matched comparison is prepared (22 October 2026, 18:48 WIB)

Run [#39772650469](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39772650469) completed with **success** at 18:48:23 WIB. Revision 27 loaded the pinned, previously restore-validated source checkpoint from run #39768787669, SHA-256 `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`. The log explicitly records `ExecutionFlow::SaveStateLoaded`; five genuine external-X11 screenshots at 1280×800 were validated; F20 shows `情報` (Informasi) selected; the test correctly chose WAIT/no input. The automated classifier remains `menu_or_unknown_choice`, so do not infer another rule from this smoke.

The emulator exited 0. The output checkpoint was validated after process exit: 21,162,547 bytes, `PCSX-Redux SaveState v4` header, SHA-256 `cb53613ffa09e57d0f6d927d9e82bf603937871a07a9ed24c0955735cf258fdc`, private artifact #12422499045. This confirms the pinned source restore and established single-nextTick shutdown path work in this run. **Do not promote the newly emitted output hash as a source checkpoint yet**; it must itself be restored in a new process before promotion.

Next experiment is marker revision 28: matched ACTION=DOWN versus control NONE/WAIT from the same verified source SHA above, `RESTORE_TEST=0`, `CONTINUATION_TEST=0`, `AB_TEST=1`, `LOOP_CYCLES=2`. Audit F20 pixel/state parity, input press/release readback, two explicit load events, ten authentic images, emulator exits and external post-exit validation of both output checkpoint files. Only then may Information→Map view be classified. Story Mode remains NOT COMPLETE.

---

## ACTIVE SMOKE — restore-only run #39772650469 (22 October 2026, 18:45 WIB)

The established single-nextTick shutdown is now being smoke-tested. Run [#39772650469](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39772650469) is revision 27 with `RESTORE_TEST=1`, `LOOP_CYCLES=1`, source pinned to the known-restorable Information checkpoint SHA-256 `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e` from run #39768787669. At 18:45 WIB its job remained in `Install X11 tools and prepare private workspace` (started 18:43:28 WIB); no emulator frames/artifact are available yet. Do not trigger a parallel player run.
- Current workflow uses single `PCSX.pauseEmulator(); PCSX.nextTick(function() PCSX.quit(0) end)` outside VSync, and the shell must validate the emitted file after the emulator ends. The previous VSync and recursive nextTick drains both stalled with timeout 124.
- Audit this run when it completes: explicit `ExecutionFlow::SaveStateLoaded`, five authentic post-load X11 images, process exit, and external output checkpoint size/v4-header/SHA validation. If it succeeds, repeat paired DOWN-vs-NONE from the same original source SHA. If the job continues to stall during installation or times out, document that result without marking the checkpoint as promoted.

Story Mode remains NOT COMPLETE. The Information→`マップを見る` (Lihat peta) transition is only a HYPOTHESIS because the action-only branch has no completed control comparison.

---

## DIAGNOSTIC UPDATE — chained nextTick drain also timed out; restore established single nextTick and run a one-cycle smoke (22 October 2026, 18:39 WIB)

Run [#39771377339](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39771377339) failed in the second attempted Information-down A/B. The emulator produced all five ACTION-branch X11 frames and the ACTION checkpoint was 21,162,276 bytes with v4 header, SHA-256 `a2d055634da951b8c9703ac1d30ac0981d4508404527604ddf4e803fe08935b5` (inspected in private artifact #12423430123 after the run ended). The output bytes appear structurally complete, but the emulator did not exit because a chain of 12 `PCSX.nextTick` callbacks after pausing did not advance; the watchdog reported rc=124 and the paired run terminated before branch 2. It is not a trusted continuation source and no paired rule result is recorded from this run.
- A similar paused VSync drain attempt in #39770465538 also timed out with rc=124; its artifact has 21,162,494 bytes and the v4 header but likewise did not complete a controlled clean exit. Chained deferred callbacks while paused are therefore unsuitable.
- Workflow commit `df6e3d5afab0a9efeac89aa8bcb0be2e273ef631` restores the established single `PCSX.pauseEmulator(); PCSX.nextTick(function() PCSX.quit(0) end)` shutdown outside VSync; the shell must validate the checkpoint after emulator exit, and will only tolerate native exit 139 when the session-finished marker exists and external checkpoint validation passes.
- Visual inspection of the one-arm image sequence from #39771377339 suggests the red highlight moved from `情報` (Informasi) to `マップを見る` (Lihat peta) after DOWN, but since the control arm was never run, this remains **HYPOTHESIS**, not VERIFIED. Do not update the proven rule set on this evidence alone.

### Next validation
Trigger a one-cycle `RESTORE_TEST=1` smoke from the known-good, already restore-validated Information parent `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`, to verify that direct single-nextTick shutdown finishes and its new checkpoint passes external size/v4-header/SHA validation. Only after smoke passes, repeat matched DOWN-vs-NONE from the same pinned source.

---

## DIAGNOSTIC UPDATE — VSync drain stalled; nextTick-based shutdown retry prepared (22 October 2026, 18:31 WIB)

The second attempt at the Information-menu DOWN/NONE experiment, [run #39770465538](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39770465538), also failed to complete its matched comparison. The 12-VSync drain did not advance: the emulator process remained alive until its 120-second timeout, exiting 124. The uploaded private artifact #12422367156 has a complete-looking checkpoint (21,162,494 bytes, header v4, SHA-256 `0c33a47cb9e6f2dfb09c568410ca125acbae6f46f84692b8589a5c903442f564`) after timeout, and its authentic ACTION screenshots show DOWN moved the red highlight from `情報` (Informasi) to `マップを見る` (Lihat peta). But there was no control branch and the normal external workflow validator was bypassed by timeout exit, so this remains **HYPOTHESIS, not VERIFIED**; do not use that timeout-produced state as the official continuation source.

The VSync countdown was removed in workflow commit `3e052b8e77cfcd966f5e5e05a2f7341ed2ff0374`. It now pauses after a completed write/close and chains 12 `PCSX.nextTick` callbacks before calling `PCSX.quit(0)`, to drain the host event loop without relying on more GPU frames. This is an unverified engineering hypothesis.

Next retry is marker revision 26 from the same known-restorable Information parent: source run #39768787669, artifact `naruto-storymode-adaptive-player-private`, checkpoint `adaptive-cycle-01-f180.sstate`, SHA `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`. Require ACTION=DOWN vs NONE/WAIT, equal F20 frames/states, press/release readback, two full X11 branches, clean/allowed exits and shell validation of both checkpoint outputs. If shutdown again times out or either output is truncated, stop and diagnose; do not assert the Information→Map-view rule.

Story Mode remains NOT COMPLETE.

---

## DIAGNOSTIC UPDATE — checkpoint structurally complete, but shutdown timed out; nextTick drain retry prepared (22 October 2026, 18:31 WIB)

**Story Mode remains NOT COMPLETE.** Do not promote a checkpoint from the failed A/B run.

- Run [#39770465538](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39770465538) failed before control/NONE ran. Five genuine external-X11 frames C01-F20/F60/F100/F110/F180 were valid 1280x800; input DOWN readback passed; parent source SHA was pinned and Memory Card clones were identical. It logged `ADAPTIVE_SESSION_FINISHED cycle=1` and `ADAPTIVE_SHUTDOWN_DRAIN_BEGIN=PASS`, but **never logged drain PASS**; after 120 seconds the process timed out with exit 124.
- Its private artifact #12422367156 included a 21,162,494-byte file with `PCSX-Redux SaveState v4` header and SHA-256 `0c33a47cb9e6f2dfb09c568410ca125acbae6f46f84692b8589a5c903442f564`. External artifact inspection confirms it is full-sized, unlike the previous 2 MiB partial save, but the session did not exit cleanly and no matched control branch ran. Do **not** treat this as a trusted continuation checkpoint.
- Diagnosis: the first drain implementation waited for further `GPU::Vsync` callbacks after `PCSX.createSaveState()`; after F180 those callbacks did not arrive, so the countdown never advanced. Workflow commit [`3e052b8`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/3e052b8e77cfcd966f5e5e05a2f7341ed2ff0374) replaces the VSync drain with 12 bounded `PCSX.nextTick` callbacks after pausing gameplay, then calls `PCSX.quit(0)`. This is a new hypothesis to validate, not yet a proven fix.
- Marker remains revision 25 and pins the immutable, previously restored Information-selection source from run #39768787669 (SHA-256 `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`), with ACTION=DOWN vs NONE and two isolated identical Memory Cards. Once ready, increment revision to 26 to trigger one bounded retry.
- Acceptance requires both branches, five X11 frames each, exact F20 parity, DOWN true/false readback, explicit load events, normal exit 0, and external post-exit size/header/SHA validation for both output checkpoints. Only after that A/B result can the Information→View map row transition be VERIFIED.

---

## DIAGNOSTIC UPDATE — Information-down A/B halted safely on truncated checkpoint; shutdown drain added (22 October 2026, 18:23 WIB)

Run [#39769826213](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39769826213) did **not** complete the matched A/B experiment. Authentic X11 captures C01-F20/F60/F100/F110/F180 were valid, ACTION/CONTROL Memory Cards cloned with identical SHA, source hash stayed pinned to `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`, and the action branch DOWN press/release readbacks passed. However, emulator shutdown exited 139 and its output checkpoint was only 2,097,152 bytes; shell validation explicitly logged `ADAPTIVE_CHECKPOINT_EXTERNAL_VALIDATION=FAIL ... reason=size`. The runner stopped before cycle 2 (watchdog exit 92). Do not infer the menu transition from this run and do not promote its checkpoint. The authentic C01-F20 capture confirms the menu parent still shows `情報` (Informasi) selected.
- To address possible delayed save-slice flush before process exit, workflow commit `13da48ab08ef40d0be8c8bbc850b7babbb9b107e` adds a bounded 12-VSync drain window after checkpoint write/close returns. During the drain, no new input, capture, or cycle action is allowed; then it pauses and schedules quit outside VSync. This is a diagnostic safeguard, not yet proven to fix truncation.
- Next smoke retry remains on the same immutable Information parent SHA above and requires 10 valid frames, parent parity, DOWN readback, two completed branches, normal/allowed exits, and externally valid (>21 MB) v4 checkpoints. If either checkpoint is 2 MB/truncated again, keep the experiment UNKNOWN and diagnose further.

Story Mode remains **NOT COMPLETE**. No authentic ending/results evidence exists.

---

## ACTIVE RUN — DOWN from Information versus NONE/WAIT (22 October 2026, 18:20 WIB)

Run [#39769826213](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39769826213) is active on marker revision 24. Parent checkpoint is the exact, independently restored Information-selection state from run #39768787669: source file `adaptive-cycle-01-f180.sstate`, SHA-256 `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`. Test arms are ACTION=DOWN and control=NONE/WAIT, each with an independent clone of the same Memory Card. This tests whether DOWN from `情報` (Informasi) highlights `マップを見る` (Lihat peta). At last check it had initialized its container; no outcome yet.

Audit exact F20 pixel parity, menu-state match, DOWN press/release readback, both `ExecutionFlow::SaveStateLoaded` events, all 10 real external-X11 frames, normal/allowed exits, and external size/header/SHA checks for both outputs. Keep unknown results UNKNOWN; do not use Circle to confirm a menu row.

---

## VERIFIED UPDATE — Information-highlight checkpoint restored in a fresh emulator (22 October 2026, 18:18 WIB)

Story Mode remains **NOT COMPLETE**. The restore-only test succeeded; five authentic X11 frames from the new process visibly retain the selection on `情報` (Informasi).

- Run [#39769265269](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39769265269) completed success using the ACTION checkpoint from A/B run #39768787669, exact source hash `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`, 21,162,009 bytes.
- Private source-validation evidence confirms immutable read-only source copy and exact hash. Log explicitly includes `ADAPTIVE_LOAD_EVENT=PASS event=ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS` with that hash. Five authentic external-X11 images C01-F20/F60/F100/F110/F180 are 1280x800, valid, and were visually inspected. The selected row is `情報` (Informasi) in the right-side menu.
- Emulator exited normally with code 0. New output checkpoint `adaptive-cycle-01-f180.sstate`, 21,162,446 bytes, SHA-256 `6159214a9006127c70f190f0d64b2ed3fb7f9e58ffddd5e4546a0a18820114c6`, passed external post-exit size/header/SHA validation. It remains a new, unpromoted output because the new output itself has not yet been restored. Source `aa399bd...` has now been proven restorable.
- The next bounded test is a matched DOWN vs NONE/WAIT from that exact source checkpoint with independent identical Memory Card clones. It asks whether DOWN from `情報` (Informasi) moves highlight to `マップを見る` (Lihat peta), with F20 pixel parity and readback required. Circle is not permitted for this menu action. Story Mode remains incomplete.

---

## VERIFIED UPDATE — second DOWN moves Ninjutsu highlight to Information (22 October 2026, 18:14 WIB)

Story Mode remains **NOT COMPLETE**; no authentic ending/results screenshot exists.

- Matched A/B run [#39768787669](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768787669) succeeded from the same parent checkpoint in two fresh processes: 21,163,486 bytes, SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`. F20 frames were pixel-identical across 1,024,000 pixels and both branches classified `menu_or_unknown_choice`.
- Separate cloned Memory Cards were identical at SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`. ACTION sent one DOWN (press readback true, release false); NONE/WAIT sent no button. Both load events and exits 0 were verified.
- Ten authentic external-X11 captures at 1280x800 were reviewed from private artifact #12421302756. In ACTION, the red highlight moved from `忍術` (Ninjutsu) at F20 to `情報` (Information) at F60; NONE remained on `忍術` (Ninjutsu) through F180. F60/F100/F110/F180 differ consistently in 14,606 pixels (mean absolute RGB difference 1.04012).
- Both outputs passed post-exit checkpoint structure/hash validation, but neither output is promoted for continuation because no fresh-process restore of those two outputs has been done:
  - ACTION: 21,162,009 bytes; SHA-256 `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`;
  - NONE: 21,162,184 bytes; SHA-256 `06cea778aaaf838271fafa58734c3e236e7d5aa3f63d578a786012640fbbde52`.
- **VERIFIED, narrow scope:** in this exact right-side menu at the Ninjutsu row, one DOWN moves the highlight to Information; NONE leaves Ninjutsu selected. Do not generalize outside the observed menu.

The clean source for the next Triangle probe is already independently restored checkpoint #39768371975: 21,162,575 bytes, SHA-256 `fa03a1840612749810453566a25805e89a4aa21ad64664695e09ed7222b77a9e`, menu showing `忍術` (Ninjutsu) highlighted and footer `△ マップ` (Triangle: Map). After confirming the Triangle branch starts from that same F20 image as NONE, compare the map view. Stop at map view; do not select a map target, and do not use Circle.

---

## VERIFIED UPDATE — DOWN from Ninjutsu selects Information (22 October 2026, 18:14 WIB)

**Story Mode remains NOT COMPLETE.** No authentic ending/results image exists.

- Matched ACTION-vs-NONE run [#39768787669](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768787669) succeeded from previously restored immutable parent hash `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`, whose menu highlight was `忍術` (Ninjutsu).
- Both branches loaded that same source in separate fresh processes and logged `ExecutionFlow::SaveStateLoaded`; their Memory Cards were separate byte-identical clones (SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`). Ten authentic external-X11 captures passed validation, and both processes exited 0.
- F20 parent parity passed: the screenshots were pixel-identical across 1,024,000 pixels, with both classifiers on `menu_or_unknown_choice`. The ACTION branch's DOWN press/release readbacks passed, while the control branch sent no action.
- Visually, the red selection highlight moves from `忍術` (Ninjutsu) to `情報` (Informasi) by F60 in the action branch. The control branch stays on Ninjutsu through F180. Cross-branch visual differences were 14,606 pixels with mean absolute RGB difference 1.04012 at F60/F100/F110/F180.
- **Rule classification: VERIFIED, scoped to this menu:** DOWN moves the highlighted row one step from Ninjutsu to Information. Combined with the previous A/B result, the observed menu navigation is Roulette → Ninjutsu → Information for successive DOWN presses from those tested parent states. It does not establish what those menu entries do when confirmed.
- Action checkpoint, private artifact #12421302756: 21,162,009 bytes; SHA-256 `aa399bd8004cf3aaf9010ee435dbe7dd45d0b514193ec89e8d4cd4e4b4053f9e`. Control checkpoint: 21,162,184 bytes; SHA-256 `06cea778aaaf838271fafa58734c3e236e7d5aa3f63d578a786012640fbbde52`. Both passed post-exit structural validation, but neither new output may be promoted until fresh-process restoration is verified.

### Next
Restore-only test the ACTION checkpoint above from private artifact #12421302756. Require an explicit `ExecutionFlow::SaveStateLoaded`, five authentic post-restore X11 frames showing the Information row still selected, normal/allowed exit, and external post-exit size/header/SHA checks. Do not assume the output checkpoint is a trusted resume point until then. Do not confirm any non-YES menu item with Circle.

---

## ACTIVE RUN — test DOWN from Ninjutsu to the next menu row (22 October 2026, 18:12 WIB)

Run [#39768787669](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768787669) was triggered at marker revision 22. It uses the verified/restored parent checkpoint from run #39767790829, file `adaptive-cycle-01-f180.sstate`, SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`, in ACTION=DOWN and NONE/WAIT branches with cloned identical Memory Cards. `LOOP_CYCLES=2`, `AB_TEST=1`, `RESTORE_TEST=0`, `CONTINUATION_TEST=0`. Latest status: in progress, at container initialization. This test asks whether DOWN from `忍術` (Ninjutsu) advances to `情報` (Informasi); only authentic matched X11 evidence can decide.

---

## VERIFIED UPDATE — menu-DOWN checkpoint restored in a fresh process (22 October 2026, 18:10 WIB)

Story Mode remains **NOT COMPLETE**; there is no authentic ending/results screenshot.

- Restore-only run [#39768371975](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768371975) succeeded from the ACTION branch checkpoint of #39767790829. Its source was 21,163,486 bytes with SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`.
- The fresh emulator logged `ExecutionFlow::SaveStateLoaded`; five authentic X11 frames at F20/F60/F100/F110/F180 were validated at 1280x800 and visually inspected. The red selector remained on `忍術` (Ninjutsu); the menu also shows `ルーレット` (Roulette), `情報` (Information), and `マップを見る` (View map). Footer `△ マップ` means (Triangle: Map).
- The emulator emitted its session-finished marker and exited 0. The resulting private checkpoint passed post-exit size/header/SHA validation: `adaptive-cycle-01-f180.sstate`, 21,162,575 bytes, SHA-256 `fa03a1840612749810453566a25805e89a4aa21ad64664695e09ed7222b77a9e`. Private artifact #12421326531 only.
- This output is now a trusted checkpoint for the next bounded probe. The next planned run is a matched Triangle-versus-NONE experiment from this exact parent, two new emulator processes and separate byte-identical disposable Memory Cards. It must confirm F20 pixel parity and inspect all ten authentic X11 frames. Do not press Circle; if Triangle opens the map view, stop at that view and inspect before any other action.

---

## VERIFIED UPDATE — menu-DOWN checkpoint restored successfully; second DOWN probe next (22 October 2026, 18:10 WIB)

The ACTION branch checkpoint from the matched DOWN/NONE test has now passed fresh-process restoration and is a valid continuation source.

- Restore run [#39768371975](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768371975) completed success using source checkpoint `adaptive-cycle-01-f180.sstate` from run #39767790829 (21,163,486 bytes; SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`).
- Its stdout explicitly contains `ADAPTIVE_LOAD_EVENT=PASS event=ExecutionFlow::SaveStateLoaded` and `ADAPTIVE_RESTORE_TEST=PASS` with that source hash. Five 1280x800 authentic external-X11 captures were validated after the load. The first frame visually retains the red selection highlight on `忍術` (Ninjutsu). Emulator exit was 0.
- The fresh output checkpoint `adaptive-cycle-01-f180.sstate` is 21,162,575 bytes, SHA-256 `fa03a1840612749810453566a25805e89a4aa21ad64664695e09ed7222b77a9e`; post-exit shell validation passed size/header/SHA. It remains private artifact #12421326531 and is not yet promoted because this *output* has not itself been restored.
- The source checkpoint SHA `76b5962f...` is now confirmed restorable; keep using that immutable source for the next paired direction probe rather than promoting the un-restored output.

### Next controlled menu experiment
Use the same source `76b5962f...` and independent byte-identical Memory Cards. Run ACTION=DOWN versus NONE/WAIT again, with same F20 visual parity required. Expected probe question: does DOWN from selected `忍術` (Ninjutsu) move the highlight to `情報` (Informasi)? Do not assume the answer; use authentic before/after frames and readback. Do not send Circle or infer menu confirmation. If parity/input/checkpoint guards fail, keep result UNKNOWN.

---

## CURRENT NEXT RUN — restore the verified menu-DOWN successor (22 October 2026, 18:08 WIB)

The matched A/B rule above is VERIFIED for this menu state, but its output checkpoint is not yet a trusted resume source. Restore-only run [#39768371975](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39768371975) was triggered from private artifact #12420204586, file `adaptive-cycle-01-f180.sstate`, size 21,163,486 bytes, SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`; marker revision 21 sets `RESTORE_TEST=1`, `AB_TEST=0`, `CONTINUATION_TEST=0`, and `LOOP_CYCLES=1`. At the latest check it was queued. Do not continue from that checkpoint until the new process logs `ExecutionFlow::SaveStateLoaded`, produces five post-restore authentic X11 frames, exits normally/under an explicitly allowed condition, and externally validates its output checkpoint after emulator exit.

---

## VERIFIED UPDATE — matched DOWN-versus-NONE menu test passed (22 October 2026, 18:06 WIB)

Story Mode remains **NOT COMPLETE**; no authentic ending/results screenshot exists.

- Corrected matched experiment [#39767790829](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39767790829) completed successfully. It used immutable parent checkpoint SHA-256 `7679cfbd3576c3202abcc299b907939ab4e4529e3a0aa260e780806b1e21cc92` in two fresh emulator processes.
- The action and control branches each logged `ExecutionFlow::SaveStateLoaded`, each produced 5/5 valid authentic external-X11 captures, both exited with code 0, and both output states passed post-exit shell size/header/SHA validation.
- Parent-frame parity passed: the F20 screenshots are pixel-identical (0 mismatches across 1,024,000 pixels), both classify as `menu_or_unknown_choice`, and the Memory Card template/action/control clone SHA-256 is identical: `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- The ACTION branch sent exactly one DOWN at the scheduled action window; press readback `true` and release readback `false` both passed. The NONE/WAIT control sent no action at that window.
- Authentic frames in private artifact #12420204586 show the selection highlight moving from `ルーレット` (Roulette) at F20 to `忍術` (Ninjutsu) by F60 in the DOWN branch, while the control remained on Roulette through F180. Cross-branch pixel comparison showed 14,609 differing pixels (mean absolute RGB difference 1.04924) at F60/F100/F110/F180, consistent with the persistent highlighted-row change.
- **Rule classification: VERIFIED, narrowly scoped:** in this specific Story Mode right-side menu, one DOWN press moves the selected row down from `ルーレット` (Roulette) to `忍術` (Ninjutsu). Do not generalize to all menus/states.
- Action branch checkpoint: 21,163,486 bytes, SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`. Control branch checkpoint: 21,163,324 bytes, SHA-256 `3da0a41d55e988550ef1a9368652fa909ae06da34c2b4b7bf315f5a820f76aeb`. Both are in private artifact #12420204586 only. Neither is yet a trusted continuation source until one is restored in a fresh emulator process and the load event/post-load frame are verified.
- Two earlier A/B failures were harness/report-guard defects, not contradictory gameplay results: #39766331759 hit a Python Path-format TypeError; #39767083708 generated the complete comparison but failed on an unrelated dialogue-required guard. Workflow fixes now allow A/B mode to complete.

### Next step
Run a one-cycle fresh-process restore test from the ACTION branch checkpoint above. Require exact source checksum, explicit `ExecutionFlow::SaveStateLoaded`, five authentic post-load X11 captures, normal/allowed exit, and external post-exit validation of its new checkpoint. Only then use it to explore subsequent menu inputs. Do not use Circle to confirm a non-YES menu item; keep unknown choice state fail-closed.

All private gameplay evidence remains outside Git; Story Mode is not complete without authentic ending/results evidence.

---

## VERIFIED UPDATE — matched DOWN-versus-NONE menu test passed (22 October 2026, 18:06 WIB)

**Story Mode is NOT complete.** No authentic ending/results screenshot exists.

- Run [#39767790829](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39767790829) passed. It used the same immutable parent checkpoint in two separate emulator processes: run #39765193287's cycle-2 checkpoint, 21,163,013 bytes, SHA-256 `7679cfbd3576c3202abcc299b907939ab4e4529e3a0aa260e780806b1e21cc92`.
- Both arms passed the F20 initial-frame parity test: 1,024,000/1,024,000 pixels identical. Both classified `menu_or_unknown_choice`.
- Two separate disposable Memory Cards were cloned from the same baseline and passed byte-hash equality: `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`. Each arm logged `ExecutionFlow::SaveStateLoaded`; source SHA was identical in both processes; both exited 0.
- Action arm: DOWN press readback true and release readback false. Control: NONE/WAIT, no button press.
- 10 authentic external-X11 images were validated at 1280x800 and inspected from private artifact #12420204586. F20 matches exactly; F60/F100/F110/F180 each differ at 14,609 pixels (mean absolute RGB difference 1.04924). Visual inspection confirms the red menu selection mark moved from `ルーレット` (Roulette) to `忍術` (Ninjutsu) after one DOWN; the NONE branch remained on `ルーレット` (Roulette).
- Both branch checkpoints passed post-exit file size/header/SHA checks:
  - action/DOWN: 21,163,486 bytes, SHA-256 `76b5962f49c351248fbbcf7cfae5a633597908debfe5eb15b24cb9eb931adf28`;
  - control/NONE: 21,163,324 bytes, SHA-256 `3da0a41d55e988550ef1a9368652fa909ae06da34c2b4b7bf315f5a820f76aeb`.
- Rule status: **VERIFIED (narrow scope):** in this exact right-side menu and checkpoint, one DOWN moves the highlight from Roulette to Ninjutsu; no-input leaves Roulette selected. **HYPOTHESIS:** the same one-row behavior generalizes across other menus/screens.

The menu footer visibly includes `△ マップ` (Triangle: Map). The next safe exploratory action may test Triangle versus NONE from the exact same menu checkpoint, still without Circle. Keep results scoped to directly observed behavior. Artifacts stay private; no ROM, BIOS, Memory Card, savestate or screenshot is committed.

---

## EXPERIMENT UPDATE — A/B first attempt reached matched branches; report bug fixed and rerun active (22 October 2026, 17:59 WIB)

Story Mode remains **NOT COMPLETE**. Run #39766331759 failed after gameplay and checkpoint steps, but it did not fail on gameplay evidence: the final comparison script raised `TypeError: unsupported operand type(s) for %: 'PosixPath' and 'int'` while building the path to the F20 verification JSON. The private artifact #12419789546 contains 10 valid authentic X11 frames and two structurally validated output checkpoints, but because the final paired audit did not finish, do not promote either output checkpoint as a trusted continuation.

Direct private-artifact audit independently established:
- Both Memory Card clones and the template were byte-identical, SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- Both branches loaded the identical immutable parent `7679cfbd3576c3202abcc299b907939ab4e4529e3a0aa260e780806b1e21cc92`, and logged `ExecutionFlow::SaveStateLoaded`.
- Both F20 state classifications were `menu_or_unknown_choice`, and pixel-wise comparison found **0 differing pixels out of 1,024,000**; initial parity is therefore supported.
- The ACTION arm's DOWN press/release readback passed. The NONE/WAIT control sent no input. Both arms met the visual precondition and each produced a checkpoint with valid v4 header/size/SHA, but the report builder errored before completing the final paired comparison.

The Python path expression was corrected in workflow commit [0041262a4c83edbabdbfb658ff3c572ad9e3a30c](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/0041262a4c83edbabdbfb658ff3c572ad9e3a30c). The identical-parent A/B experiment was re-triggered as run [#39767083708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39767083708), revision 19, using the same immutable parent and fresh identical Memory Card clones. It was active at this update; no rerun result is yet verified.

Keep rule conclusions conservative until the rerun report has been audited. All screenshots/savestates remain private and out of Git.

---

## VERIFIED UPDATE — bounded two-cycle checkpoint continuation passed (22 October 2026, 17:47 WIB)

**Story Mode is NOT complete.** No authentic ending/results screenshot exists.

- Continuation run [#39765193287](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39765193287) completed **success** from the exact immutable source checkpoint from restore run #39764239171: 21,162,934 bytes, SHA-256 `16f697fa95c16661a639ad46b55f90008e60200d1ee860058b12d7b1110d073b`.
- Ten authentic external-X11 captures passed integrity checks at 1280x800 and were visually reviewed from private artifact #12419528763. The images show cycle 1 opening an Iruka dialogue and START skipping it; the visible phrase `いいかナルト。` translates as (Dengarkan baik-baik, Naruto). By C01-F180 a right-side choice/menu appeared. Cycle 2 classified it as `menu_or_unknown_choice` and correctly chose `WAIT`, not an uncalibrated confirmation.
- Both fresh emulator processes logged `ExecutionFlow::SaveStateLoaded`; cycle 1's source was the pinned restored checkpoint, and cycle 2's source was the exact SHA of cycle 1's new checkpoint. Both processes exited 0.
- Both output checkpoints passed external post-exit size/header/SHA verification:
  - cycle 1, 21,163,161 bytes, SHA-256 `fd46af37af86b0843651ee6baa5d10bd6cb75123d68c87e8319a647130d6b512`;
  - cycle 2, 21,163,013 bytes, SHA-256 `7679cfbd3576c3202abcc299b907939ab4e4529e3a0aa260e780806b1e21cc92`.
- Evidence summary logged `ADAPTIVE_CONTINUATION_TEST=PASS parent_sha256=16f697fa... cycles=2 fresh_processes=2 captures=10 checkpoint_chain=validated policy_guard=PASS`. All states and images remain private; no gameplay image/state is in Git.

### Next controlled experiment
The next safe diagnostic is a matched `DOWN` versus `NONE/WAIT` branch from the same immutable cycle-2 menu checkpoint, using separately cloned disposable Memory Cards. At F20 require both branches to show the same parent state; press/release DOWN only in the action branch; never press Circle or START unless the respective calibrated visual condition requires it. Capture F20/F60/F100/F110/F180 from both branches and compare actual screen, selection highlight and subsequent transition. If pre-action states disagree or the menu state differs from the pinned source, fail the experiment closed. Do not infer a universal rule from a single branch pair.

Only this repository is permitted. Story Mode remains incomplete without authentic ending/results evidence.

---

## VERIFIED UPDATE — fresh-process restore passed; bounded two-cycle continuation active (22 October 2026, 17:43 WIB)

**Story Mode is NOT complete.** No authentic ending/results screen has been captured.

- Smoke run [#39763526377](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39763526377) passed 8 tests and 5/5 authentic X11 frames. Its checkpoint was 21,162,617 bytes, v4 header valid, SHA-256 `b55495934f9ba98165268627b35904918a4dd3983e6d90bb66e2662dfa059e17`.
- Fresh-process restore run [#39764239171](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39764239171) passed. The log explicitly recorded `ExecutionFlow::SaveStateLoaded`; 5 authentic external-X11 post-load frames were validated; emulator exit was 0; the newly produced checkpoint passed post-exit size/header/SHA validation.
- Verified restored-session checkpoint, private artifact #12419357425 only: `adaptive-cycle-01-f180.sstate`, 21,162,934 bytes, SHA-256 `16f697fa95c16661a639ad46b55f90008e60200d1ee860058b12d7b1110d073b`. Never commit or publicly link it.
- Two-cycle continuation run [#39765193287](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39765193287) is active, revision 17, with this exact artifact/file/hash as immutable source, `RESTORE_TEST=0`, `CONTINUATION_TEST=1`, `LOOP_CYCLES=2`. Current status at this update: initializing. It must prove 10/10 X11 captures, two `ExecutionFlow::SaveStateLoaded` events, post-exit structural/SHA checks on both outputs, cycle-2 policy guard, and differing F20/F180 visual hashes per cycle. Do not consider it passed before audit.

Only the allowed research repo has been accessed. Screenshots/states remain private artifacts and out of Git. Keep action/state conclusions conservative; Story Mode remains incomplete absent authentic ending/results evidence.

---

## VERIFIED UPDATE — one-cycle smoke checkpoint validated; restore test pending (22 October 2026, 17:35 WIB)

**Story Mode is NOT complete.** No authentic in-game ending/results screenshot exists. The new smoke checkpoint is structurally validated but is not yet trusted as a continuation source until a fresh emulator process restores it.

- Player smoke run [#39763526377](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39763526377) completed **success** on workflow revision 15 with `LOOP_CYCLES=1`.
- All 8 adaptive-agent tests passed; all five authentic external-X11 captures C01-F20/F60/F100/F110/F180 were valid 1280x800 PNGs and visually inspected from private artifact #12419631005. They show board → visible dialogue → board. DOWN and START press/release readbacks passed; the Japanese dialogue `ここに結界をはります` means (Aku akan memasang penghalang di sini). START was used to skip it.
- The run recorded `ADAPTIVE_GAMEPLAY_PROGRESS=PASS from=map to=dialogue`, emitted the session-finished marker, and the emulator exited normally with code 0.
- Shell validation **after emulator exit** passed the checkpoint length threshold, PCSX-Redux SaveState v4 header, and SHA-256. Private checkpoint `adaptive-cycle-01-f180.sstate` is 21,162,617 bytes, SHA-256 `b55495934f9ba98165268627b35904918a4dd3983e6d90bb66e2662dfa059e17`. It is in private artifact #12419631005 only; do not commit or publish it.
- A fresh-process restore test was then triggered as run [#39764239171](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39764239171) with marker revision 16: `SOURCE_RUN=39763526377`, source artifact `naruto-storymode-adaptive-player-private`, source file and exact SHA above, `RESTORE_TEST=1`, `LOOP_CYCLES=1`. Its success requires an explicit `ExecutionFlow::SaveStateLoaded` event and authentic post-restore external-X11 frame in addition to structural validation of the new checkpoint. At the latest status check it was starting; no restore result was verified yet.
- Chakra/barrier causation remains HYPOTHESIS: the one action branch alone cannot establish a universal cost or Mizuki rule. Do not infer combat outcome from these images.

### Next steps
1. Inspect run #39764239171 logs, all five X11 frames, and private artifact. Verify the named `ExecutionFlow::SaveStateLoaded` event, post-restore frame, exit result, and new checkpoint's external size/header/SHA validation.
2. Only if that restore test passes, set the next marker to the newest validated restore-run checkpoint, `RESTORE_TEST=0`, `LOOP_CYCLES=2`, and a new revision; then audit the bounded continuation.
3. After reliable restoration, do a matched one-action-versus-NONE experiment from the same immutable parent with separate disposable Memory Card copies. Keep every rule VERIFIED/HYPOTHESIS/UNKNOWN based on direct evidence.

All existing boundaries remain: only this repository; gameplay images must be authentic external X11 captures; screenshots, savestates, ROM, BIOS and Memory Cards stay out of Git and private artifacts remain private; START skips dialogue; Circle only when a contextually valid YES is visibly highlighted. Translate Japanese into Indonesian immediately in parentheses. Never claim Story Mode is complete without authentic in-game ending/results evidence.

---

## LATEST VERIFIED RUN STATE — checkpoint visibility race; no two-cycle pass (22 October 2026, 17:20 WIB)

**Story Mode is NOT complete.** No authentic in-game ending/results screen exists. Both latest adaptive-player runs have ended; none is still running or queued.

- Regression [#39759649670](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39759649670) remains **success**: 8 synthetic tests and 10 authentic private external-X11 frame expectations passed.
- Updated player run [#39760914530](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39760914530) ended **failure**. The new fast-fail player run [#39761094445](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39761094445) also ended **failure**. Each passed all 8 agent tests and captured/validated 5/5 authentic external-X11 frames for cycle 1. Input readback passed for DOWN and START; the classifier observed map → dialogue and then map_after_move; START skipped the visible dialogue.
- In both live Lua logs, checkpoint preflight ran immediately after `Support.File:writeMoveSlice(state)` and reported `ADAPTIVE_CHECKPOINT_VALIDATION_FAIL ... bytes=0 header=false`. It then ended the session with code 74 before emitting the session-finished marker. The new watcher correctly failed fast; cycle 2 did not begin.
- Crucial artifact cross-check: after each failed run completed and the private artifact was uploaded, its checkpoint file was full-size and began with the expected PCSX-Redux SaveState v4 header:
  - #39760914530: 21,162,914 bytes; SHA-256 `f1e04a97452d675d6c6a955acd1a3aa6341a13402ca87895d61d29a6edd11124`; private artifact #12417638677.
  - #39761094445: 21,163,014 bytes; SHA-256 `64941480e4ff5eebb8497e7458ec83090d3aa2bf533d5290ac18ae882c5ab5e5`; private artifact #12417554193.
- This mismatch strongly suggests a **checkpoint write/visibility timing race**: the immediate in-emulator read sees a zero-length file, although the later uploaded artifact contains a full-length state. This is a working diagnosis, not a proven root cause. Neither state was resumed in a fresh emulator process; do not promote either to a trusted continuation point merely because its artifact size/header look plausible.
- Current marker revision 14 still requests `LOOP_CYCLES=2`; do not trigger another two-cycle run before correcting the validation timing. The source checkpoint for these experiments remains immutable: run #39685868421, 21,162,945 bytes, SHA-256 `19388b5a9b59c77e443f47abdc7c6f98251ef4a1be1b512378faab217a658ae9`.

### Next actions (strict order)

1. Repair `.github/workflows/naruto-storymode-adaptive-player.yml`: do not reject a checkpoint based on `io.open(...):seek("end")` immediately in the GPU::Vsync save callback. Record that the write/close call returned, schedule emulator shutdown outside VSync as already done, and let the shell orchestrator validate the finished file after the emulator process exits (size >21,000,000, v4 header, SHA-256). Keep failure closed: only promote the file after this external validation.
2. Change the marker to `LOOP_CYCLES=1` for the next run. This push auto-triggers the player workflow; use it as the first smoke test after the code change. Do not start a two-cycle run at the same time.
3. Inspect the run’s 5 authentic X11 captures, input readbacks, clean/allowed shutdown, checkpoint size/header/hash, and progress report. A full-size file alone does not prove savestate restore; after one-cycle smoke succeeds, run a bounded fresh-process restore/two-cycle test and require a LoadState event.
4. Only after checkpoint creation plus fresh-process restore pass, run a matched one-action-versus-NONE gameplay experiment from an immutable validated parent checkpoint and disposable cloned Memory Card.

Privacy and gameplay rules remain fixed: only `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`; no ROM, BIOS, Memory Card, savestate, or gameplay screenshot in Git. Gameplay proof must be genuine external X11 captures, not web images or PCSX’s internal screenshot API. Use START for Story Mode dialogue; Circle only for a visibly highlighted contextual confirmation. Translate Japanese immediately in Indonesian parentheses. Label findings VERIFIED/HYPOTHESIS/UNKNOWN. Never claim completion without authentic in-game ending/results evidence.

---

## LATEST RUN STATE — invalid checkpoint rejected; fresh-session fix in progress (22 October 2026, 17:12 WIB)

**Story Mode is NOT complete.** The latest authentic screenshots are board/dialogue transitions, not an ending/results screen.

- Regression [#39759649670](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39759649670) passed 8 synthetic tests and 10 authentic X11 frame expectations. The board with two HUDs is now classified as map_after_move/WAIT rather than battle_untrained.
- Player run [#39759822818](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39759822818) failed after cycle 1. Its external X11 frames show DOWN -> dialogue, START tap on visible dialogue, then a board scene with a red barrier/seal object. However, the saved state file was only 2,097,152 bytes and therefore invalid; no cycle 2 was attempted. Artifact #12417747322 remains private.
- Checkpoint code now checks the raw file size (>21,000,000 bytes) and PCSX-Redux SaveState v4 header immediately after writing. It defers emulator quit outside the GPU VSync callback; exit code 139 is recoverable only when the session-finished marker and a structurally valid raw checkpoint both exist. This prevents truncated data from being mistakenly passed to a new emulator.
- Watcher code also exits quickly if the session orchestrator dies before emitting required evidence. Player run [#39760914530](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39760914530) was still in progress at last check; it uses the checkpoint-validation/deferred-quit fix but predates the fast-fail watcher. Its outer watcher window is about 240 seconds. Updated run [#39761094445](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39761094445) is queued behind the concurrency lock and includes fast-fail logic; do not add another trigger. Inspect both runs in order.
- Single-run observation remains HYPOTHESIS: route counter 4 -> 3 after DOWN; dialogue ここに結界をはります (Aku akan memasang penghalang di sini); START sent to skip; at F180, a red barrier/seal graphic and Mizuki's displayed Chakra 1380 were visible versus 1500 at F110. No matched NONE branch has confirmed causation or a universal cost rule.
- If a valid two-session pass occurs, take the newest valid checkpoint as a read-only source for a matched one-action-versus-NONE experiment. Until then do not expand cycles. Story Mode completion still requires an authentic in-game ending/results screen.

Privacy boundaries remain unchanged: only this research repo; no ROM, BIOS, Memory Card, savestate, or gameplay screenshot in Git; authentic external X11 only; START skips dialogue; Circle only for visibly highlighted contextual confirmation; Japanese immediately translated to Indonesian parentheses.

---

## VERIFIED UPDATE — checkpoint continuity and map-transition classifier (22 October 2026, 17:03 WIB)

**Story Mode is NOT complete.** No authentic in-game ending/results screen has been captured. No ROM, BIOS, Memory Card, savestate, or gameplay screenshot was committed.

- Classifier regression [#39759649670](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39759649670) completed **success**: 8 synthetic unit tests passed and 10/10 authentic external-X11 frames from private player artifact #12416489109 matched their expected classes.
- The classifier now separates `map_after_move` (green board, route/tile symbols and dual player HUD) from `battle_untrained`. The tested board-transition frames choose `WAIT`; a dual HUD alone no longer implies battle. This is validated only for the specific authentic frames listed in the regression, not for all battle/result variants.
- Fresh-process experiment [#39758737690](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39758737690) captured 10/10 external-X11 images. Both checkpoint files were created and the cycle-2 log shows a successful save-state load event, but the run failed because the outer watcher counted checkpoints before the cycle-2 file and completion marker had appeared. It is not a verified successful run-level continuation.
  - Cycle 1 checkpoint: 21,162,838 bytes, SHA-256 `81487394b180a47c59165b49bae21f4d278b600d9fbf83c14086a9629da1c2b4`.
  - Cycle 2 checkpoint: 21,162,485 bytes, SHA-256 `42c4ad60397ade407508c4393fac21c21db6f12c88c5efc77deb05a2daa827f5`.
  - These are private artifact data only; do not commit or link individual screenshots/savestates publicly.
- Latest bounded player retry [#39759822818](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39759822818) is testing the corrected watcher, which now waits for all screenshots, both structurally valid checkpoints, and the fresh-process completion marker before finishing. Do not duplicate-trigger while it is in progress.
- New direct screenshot observation from #39758737690: at C01-F20 the board counter shows 4; at C01-F60 it shows 3 after DOWN was read back pressed/released. At C01-F100/F110 the game displays `ここに結界をはります` (Aku akan memasang penghalang di sini). START was sent while the dialogue was visible. By C01-F180, the red barrier/seal symbol is on the board, and Mizuki's displayed Chakra changed from 1500 at F100/F110 to 1380 at F180 while Naruto remained at 1380. This is a **single observed sequence**, not yet a confirmed general cost/action rule: preserve as HYPOTHESIS until a matched no-input branch from the same parent checkpoint verifies causation.
- Cycle 2 restored cycle 1's checkpoint hash `81487394b180a47c59165b49bae21f4d278b600d9fbf83c14086a9629da1c2b4`; it showed the same board-transition layout and selected `WAIT`. Do not expand beyond bounded sessions until the corrected run verifies clean exit and both checkpoints together.

**Next:** wait for the current run's final job logs; if it passes, branch from the newest validated checkpoint and run a matched one-action-vs-NONE experiment to test the next board action. Unknown states remain `WAIT`; use START for dialogue; Circle only for visible contextual confirmation. Keep artifacts private and translate Japanese immediately into Indonesian parentheses.

---

## CURRENT STATUS — adaptive player prototype test failed; monitoring added (22 October 2026, 06:xx WIB)

**Story Mode is NOT complete. An autonomous adaptive player capable of completing all Story Mode has NOT been finished or verified.** The first classifier and runner exist, but the eight-cycle emulator test timed out during cycle 2. No ending evidence exists.

- Adaptive code: `tools/storymode_adaptive_agent.py`; synthetic unit tests passed 5/5 inside run #39687675432.
- Private adaptive run [#39687675432](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39687675432) ended **failure**. External X11 captures were valid for C01-F20/F60/F100/F180 and C02-F20. The agent classified the map and chose DOWN in cycle 1; button press/release readback passed. It chose RIGHT in cycle 2, but the loop then stopped advancing and timed out with only 5/32 captures and 1/8 checkpoints. Treat cycle 1 as a harness test, not verified route progress, because the post-DOWN visuals remained classified as map and did not confirm the expected dialogue/route counter change.
- Private artifact #12386984413 (`naruto-storymode-adaptive-player-private`) contains partial authentic X11 frames, decisions, logs and the cycle-1 checkpoint. It expires 4 November 2026. Do not commit or create public links to the screenshots or savestates.
- New scheduled monitor: `.github/workflows/naruto-storymode-adaptive-monitor.yml`. It checks every 15 minutes and after player-run completion for run age (>15 minutes), failure status, and presence of the private evidence artifact. It monitors Actions/artefact health only; it does not prove emulator gameplay progress or Story Mode completion. Monitor runs are visible in GitHub Actions and report to its job summary; a failing check is not an external push notification.
- Latest roulette A/B result remains: in run #39685868421, one Circle press and NONE were pixel-identical at F100 and F180; both returned to the board by F180. Do not spam Circle on a roulette that is already settling.
- Next engineering step is to fix the repeated-cycle pause/hang by making every bounded cycle recoverable from a verified checkpoint and checking the emulator has actually advanced between captures. Add battle/turn-result signatures only from real private emulator frames; unknown states must remain WAIT.

**Rule-evidence protocol:** use identical read-only parent checkpoint and cloned Memory Card in fresh emulator branches; capture authentic X11 before/after a single action; confirm emulator button readback; compare visual state, route position/counter, Chakra/barrier/ownership and subsequent transition against a matched no-input control; repeat on another checkpoint/context. Corroborate observations against static code/reverse engineering. Record rules as VERIFIED only after repeatable direct evidence; otherwise label HYPOTHESIS or UNKNOWN. Verify completion only with authentic in-game ending/results evidence.

Constraints remain: only repo `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`; no Tile Duel or other repo; ROM/BIOS/Memory Card/savestates/screenshots remain private and out of Git. Use START for Story Mode dialogue; Circle only for a visibly highlighted contextual confirmation. Translate Japanese text immediately into Indonesian parentheses.

---

## LATEST VERIFIED CONTINUATION — Mizuki dialogue discovered after barrier (21 October 2026)

This supersedes earlier next-action notes above: the next operation is to skip Mizuki’s visible dialogue with START, not to send another direction press yet. Story Mode is still NOT complete and no ending evidence exists.

### New controlled-probe results
- After barrier placement, a DOWN-vs-NONE test [#39618670884](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39618670884) sent DOWN at relative f30–38 from the post-barrier checkpoint. Button readback passed, but the game viewport was identical to NONE at f100 and f120. Private artifact #12352978983 contains external X11 frames and distinct checkpoint successors.
- A second matched probe [#39619671384](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39619671384) delayed DOWN until f50–58 from the post-barrier continuation. Readback again passed, yet DOWN and NONE stayed visually identical in the game viewport at f60/f100 and still matched at f120. This is not proof DOWN is generally ineffective; both experiments show the action was ineffective in this post-barrier transition context/timing.
- The key visual finding is that both branches automatically reached Mizuki’s dialogue by f100–f120. The screenshot reads `ククク・・・やってやるよ！ (Kukuku… akan kuberi pelajaran!)`. Both branches show Naruto at the pink tile marked 60, enemy Mizuki token on the blue/yellow node, with HUD Naruto Chakra 1380 and Mizuki Chakra 1500. The dialogue is now the active state to resolve.
- Validated source for the next operation comes from the no-input branch of run #39619671384: `barrier-result-delayed-down-none-f120.sstate`, **21,162,244 bytes**, SHA-256 `aeef171e16f99be11d8baebb965e03fa1d47543a0d927b37e4d8e194fc5ff775`. It is copied read-only before each run.
- Current [run #39620432917](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39620432917), “START skips Mizuki dialogue after barrier”, restores this checkpoint and compares one START press/release (relative f30/f38) with a matched NONE branch. It captures authentic external X11 at f20/f60/f100/f120 and saves distinct private successors. At last check it was initializing its container; do not create a duplicate trigger. After completion inspect the job logs, screenshot hashes/visuals, comparison report and checkpoint successor before deciding another input.

### Verified path prior to dialogue
- Roulette source `7c8c8bfa4a15132a6c9a046aa842fc01d2f294d6e04d53262c20287566432222` plus controlled Circle at roulette returns to board with sector 2. Fresh-process map checkpoint `451c59b13ca1dbf93eb23afa94a096c7eb5721c5bb5108b45e9d2054289ffb53`.
- DOWN from that map moved one route and counter 2→1, showing Iruka dialogue. START skipped it and exposed the barrier prompt `ここに結界をはりますか？ (Apakah akan memasang penghalang di sini?)`, `必要チャクラ 120 (Chakra yang dibutuhkan: 120)`, `はい (Ya)` highlighted.
- Contextual Circle then visibly placed the barrier and changed Naruto Chakra 1500→1380 while Mizuki stayed 1500. Post-barrier checkpoint `a1053f965ad8520c1c7f6f59ae14433c5e1d0bb6bc933b65553597b187f65649`; the source has been kept immutable.

### Hard constraints and maturity
Use only `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. Always use START to skip Story Mode dialogue; never use Circle for dialogue skipping. Circle is only appropriate for a visible contextual confirmation choice. All gameplay evidence images are authentic emulator X11 captures, never web images or the internal screenshot API. ROM, BIOS, savestates, Memory Card and images stay private, outside Git. Translate Japanese text directly in parentheses. The checkpoint/input/capture/save cycle works for controlled steps, but general state classification, adaptive policy, generic crash recovery and autonomous multi-session completion remain unverified. Never claim completion without original in-game ending evidence.

---

## LATEST VERIFIED CONTINUATION — barrier placed and Chakra debit observed (21 October 2026)

This supersedes the prior queued-next-action note below. Story Mode is still NOT complete; no original in-game ending has been verified.

### Confirmed barrier result
- Run [#39617444912](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39617444912) restored the immutable post-START prompt checkpoint and sent one contextual Circle press/release at relative frames 30/38; both button readbacks passed. The prompt was `ここに結界をはりますか？ (Apakah akan memasang penghalang di sini?)`, with `必要チャクラ 120 (Chakra yang dibutuhkan: 120)` and `はい (Ya)` highlighted.
- Genuine external X11 screenshots show the prompt gone at f60 and a blue barrier/orb and route marker visible on the board. Naruto’s HUD decreases from **1500 to 1380** while Mizuki stays at **1500**. The same barrier object and 1380/1500 HUD persist in f100 and f120 images. Thus barrier placement and a 120-Chakra debit are verified visually for this path; this does not establish other cost/rule cases.
- Source checkpoint was read-only and unchanged: 21,162,246 bytes, SHA-256 `789585c7c7a6d5e9f5bb1601d0e277e7735380b88d91f882f36a265aff419e4a`.
- Successor checkpoint `after-barrier-circle-f120.sstate`: **21,162,458 bytes**, SHA-256 `a1053f965ad8520c1c7f6f59ae14433c5e1d0bb6bc933b65553597b187f65649`. Private artifact #12354275022, ZIP SHA-256 `708d0225255a7a2419d465a2130279ed76a128ed759e38fd4446510bf8b541d4`. Its images were inspected from the private artifact; no gameplay screenshots or savestate were committed to Git.
- The one-shot trigger was removed in cleanup commit `06a291b03334426d5216ac2a7a3c88a07b443d26`. The workflow job for #39617444912 reports all 15/15 steps completed successfully, though the run-level status endpoint has occasionally lagged behind completed job steps in this session. Trust the detailed job steps, logs, screenshot hashes and artifacts over the run summary alone.

### Next controlled action
- Continue from the successor checkpoint as a read-only source; compare one DOWN press/release (relative f30/f38) against a matched NONE branch in separate fresh emulator processes. Capture genuine external X11 at f20/f60/f100/f120 and save distinct private successors. This tests whether the next DOWN movement advances the board from the confirmed barrier state; it is not an assumption that it will work.
- If a Story Mode dialogue appears, press START to skip it. Never use Circle to skip dialogue; Circle was used in #39617444912 only because `はい (Ya)` was visibly highlighted as the confirm choice.
- Verify the resulting screenshot, position/counter, prompt/transition, log and checkpoint hashes before selecting another action. Keep the new parent checkpoint unchanged.

### Permanent constraints and maturity
Only `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research` is permitted. Keep ROM, BIOS, savestates, Memory Card and gameplay captures private. Use external X11 only for post-checkpoint gameplay evidence, not web images or the internal PCSX screenshot API. Japanese text must be followed immediately by Indonesian translation in parentheses. The validated checkpoint/observe/input/save cycle is working for controlled steps, but general screen classification, robust adaptive decisions, generic crash recovery, a multi-session autonomous loop through all missions, and Story Mode ending detection remain unverified. Never claim completion without original in-game ending evidence.

---

## LATEST VERIFIED CONTINUATION — roulette result, map movement, START dialogue skip (21 October 2026)

This update supersedes earlier “roulette behavior unknown / next test Circle on Roulette menu” guidance below. Story Mode is still NOT complete; there is no verified ending evidence.

### Verified gameplay path
- Run [#39609425942](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39609425942) preserved the roulette wheel checkpoint f120 (21,162,475 bytes; SHA-256 `7c8c8bfa4a15132a6c9a046aa842fc01d2f294d6e04d53262c20287566432222`). A longer no-input observation [#39612126429](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39612126429) reached external X11 f180 with the wheel still moving, then timed out before f300. It is not evidence the wheel stops by itself.
- Controlled branch experiment [#39613929898](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39613929898) compared NONE with one Circle press/release (relative f30/f38). Button readback passed. Circle branch visually showed sector 2 aligned under the pointer at f60/f100 and returned to the board by f180; NONE still showed the wheel at f180. Circle-result checkpoint: 21,163,057 bytes, SHA-256 `0570a687dd8ecc1449c8edaa436f21111e40433d59c6a21b0e64de6b71c07d5d`.
- Fresh-process no-input continuation [#39614665390](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39614665390) confirmed the board and roulette result 2 remained visible through f120. Map checkpoint: 21,162,853 bytes, SHA-256 `451c59b13ca1dbf93eb23afa94a096c7eb5721c5bb5108b45e9d2054289ffb53`.
- Map route experiment [#39615341661](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39615341661) compared NONE with one DOWN press/release (f30/f38). DOWN moved the token down one route and the visible move counter changed from 2 to 1; the subsequent scene/dialogue showed `イルカ (Iruka)` and text beginning `ナルトよく聞け、… (Naruto, dengarkan baik-baik, …; screenshot text is incomplete)`. DOWN branch checkpoint: 21,162,042 bytes, SHA-256 `6d01243a2e2c4b47e13a58373216bda0117a8b6e04324f2a6c3fde9b811ae494`.
- Dialogue skip [#39616129634](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39616129634) restored that checkpoint, sent START only at relative f30–f38 (press/release readback PASS), and captured external X11 screenshots through f120. The dialogue was skipped; the prompt now reads `ここに結界をはりますか？ (Apakah akan memasang penghalang di sini?)`, `必要チャクラ 120 (Chakra yang dibutuhkan: 120)`, with `はい (Ya)` highlighted and `いいえ (Tidak)` available. This only shows a required cost/prompt; it does not yet prove the cost is deducted or the barrier is placed. Current prompt checkpoint: 21,162,246 bytes, SHA-256 `789585c7c7a6d5e9f5bb1601d0e277e7735380b88d91f882f36a265aff419e4a`.

### Next action already queued
- Run [#39617444912](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39617444912), “confirm highlighted barrier YES with Circle”, is queued. It is prepared to restore the read-only prompt checkpoint, send one contextual Circle press/release, capture external X11 at f20/f60/f100/f120, and save a distinct private successor. At last check it had not started a job; there is no reliable completion ETA and no duplicate run should be launched.
- After it terminates, inspect job steps/logs, all four authentic X11 images, result report, source hash, and successor size/hash. Verify whether the prompt disappears, a barrier becomes visible, and the HUD Chakra actually changes from 1500. Do not infer barrier placement or Chakra debit from workflow success alone.
- The source checkpoint `789585c7…aff419e4a` must remain unchanged. The marker `experiments/.run-storymode-barrier-circle-confirm` is intentionally retained until this run is inspected, then must be deleted.

### Permanent constraints / current maturity
- Only this research repo is permitted. Never use Tile Duel or any other repo.
- All post-checkpoint gameplay proof is captured by real external X11 from the emulator; no web images and no internal PCSX screenshot API for these later states.
- Use START for all Story Mode dialogue; never use Circle to skip dialogue. Circle is permitted here only because the in-game YES option `はい (Ya)` is highlighted.
- Japanese text must immediately include Indonesian translation in parentheses.
- ROM, BIOS, savestates, Memory Card and gameplay images stay private; do not commit them to Git.
- The reusable checkpoint/input/X11/successor cycle is working for controlled steps, but an all-screen classifier, resilient adaptive gameplay policy, generic crash recovery and cross-session autonomous loop through all missions are not yet verified. Do not claim Story Mode completion without original in-game ending evidence.

---

## LATEST CONTROLLED INPUT RESULT — DOWN moved the vertical menu highlight (21 October 2026)

- Run [#39607704007](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39607704007) completed with workflow conclusion `success`. It restored independently from the immutable f175 checkpoint into NONE and DOWN processes, both reached relative frame 120 and saved separate private derived states.
- DOWN was pressed at relative frame 30 and released at frame 38; both input readbacks passed. NONE sent no input.
- Genuine external X11 screenshot at relative frame 90 shows the highlight moved from `ルーレット (Roulette)` to `忍術 (Ninjutsu/teknik ninja)`. The post-screen comparison has mean absolute RGB difference 1.049238 and exact-pixel fraction 0.985733; the principal difference is localized to the vertical menu selection. This supports DOWN as a verified menu-navigation input in this screen context.
- Private artifact #12348747349, 6,637,570 bytes, verified ZIP SHA-256 `340ff7064f4b4902122b9ecaeb926a4693716c41c21dc765461d989d34f15730`. All later-state screenshots were external X11 captures; PCSX internal screenshot API was not called.
- DOWN f120 result state: 21,162,252 bytes, SHA-256 `f53d6dbb6890b3798a82864b4cb2b85bc122517b63ca8e7c40eb9daf85ce2aad`. NONE f120 state: 21,162,184 bytes, SHA-256 `95d7c57fa92f9a0c4e51f181f65c1a93a8fea142925175f7c927e21b944c867b`. Keep these as private branch artifacts, not a replacement for f175.
- The earlier RIGHT probe (#39606938717) registered press/release but produced a pixel-identical post capture versus NONE. Do not use RIGHT to navigate this vertical menu.
- Next controlled action: from the original f175 source checkpoint with Roulette still highlighted, test one CIRCLE press/release against a matched NONE control. This tests menu confirmation; it is not using Circle to skip dialog. On any Story Mode dialogue, press START, not Circle.

## LATEST AUTOMATION IMPLEMENTATION — one RIGHT tap compared with NONE from f175 (21 October 2026)

- New workflow: [naruto-storymode-f175-direction-diff.yml](.github/workflows/naruto-storymode-f175-direction-diff.yml). It restores independent fresh emulator processes from the immutable verified f175 checkpoint; external X11 screenshots only; no internal PCSX screenshot API calls on this later state.
- Run [#39606938717](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39606938717) completed `success` in about 74 seconds. Both branches validated the same source checkpoint (21,163,375 bytes, SHA-256 `f8bd00074877ef583e35b8eaf2fc65b3877acda9bebd5f2d8e9a13abee094615`), fired `SaveStateLoaded`, reached relative frame 120, and saved independent private result states.
- RIGHT was pressed at relative frame 30 and released at 38; both controller readbacks passed. NONE sent no controller input. External captures at frames 20 and 90 passed 1280×800/nonuniformity validation.
- At frame 90, NONE and RIGHT images were pixel-identical (`POST_MEAN_ABS_RGB_DIFF=0.000000`, `POST_EXACT_PIXEL_FRACTION=1.000000`). Original game screenshot shows a vertical menu with Roulette highlighted; no visible change was caused by RIGHT. Thus the controller register works, but RIGHT is **not verified as an effective action** in this menu context.
- Private artifact [#12348274409](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39606938717/artifacts/12348274409), 6,680,465 bytes, verified ZIP SHA-256 `8b095bbe8e8d20f9ca639b4c2f3be448339556376f193d7b7487c94830e33027`. It contains external X11 screenshots, logs, validation report and private derived savestates. None were committed to Git.
- Run [#39607704007](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39607704007) is the follow-up DOWN-versus-NONE probe from the same original f175 checkpoint; it is currently in progress at time of this note. Do not infer its outcome until it finishes and screenshots/logs are checked.
- Source checkpoint remains the baseline; do not continue from the RIGHT-derived state. The new workflow reads `ACTION=UP|DOWN|LEFT|RIGHT` from a one-shot marker, validates allowed values, and performs one controlled press/release. The trigger marker must be removed after the run.
- Conclusion so far: controller can restore and advance the source checkpoint in two separate processes and save derived states. The automation is still a controlled probe, not yet a closed gameplay/recovery loop and not evidence of mission/story completion.

## APPROVED LONG-TERM GOAL — otomatisasi Story Mode berbasis checkpoint (21 Oktober 2026)

Pengguna menyetujui rencana membangun loop otomatis untuk meneruskan Story Mode sampai tamat tanpa keterlibatan manual di setiap tombol: pulihkan checkpoint tervalidasi sebagai salinan read-only → lakukan satu tindakan terukur → amati layar/game state lewat bukti emulator asli → verifikasi perubahan → simpan checkpoint turunan dan manifest privat → lanjutkan sesi berikutnya dari checkpoint paling baru yang tervalidasi. Jika crash/stall/timeout, pulihkan baseline tervalidasi dan lanjutkan dengan strategi yang terukur, bukan restart dari awal.

Rencana lengkap dan instruksi lintas-chat ada di [docs/STORYMODE_AUTOMATION_WORKFLOW_2026-10-21.md](docs/STORYMODE_AUTOMATION_WORKFLOW_2026-10-21.md). Otomasi penuh belum tersedia/terbukti hanya dengan adanya dokumen atau Actions `success`; harness masih harus dibangun dan diuji. Jangan menyatakan Story Mode tamat tanpa bukti akhir asli dari game.

**Baseline dan langkah berikutnya:**
- Checkpoint papan Konoha f175 tetap baseline immutable untuk uji directional terkontrol: SHA-256 `f8bd00074877ef583e35b8eaf2fc65b3877acda9bebd5f2d8e9a13abee094615`, ukuran 21,163,375 byte.
- Uji satu arah per proses emulator baru dari salinan read-only f175 dan bandingkan dengan kontrol tanpa input berdurasi setara. Capture visual state lanjut via X11 eksternal saja; jangan gunakan internal screenshot API pada state/frame yang dilarang.
- Run #39599932467 menguji konfirmasi pilihan penghalang pada checkpoint cabang RIGHT/DOWN: angka 100 Chakra dan 140 Chakra terlihat sebelum confirm; belum terbukti Chakra terpotong atau barrier sukses diletakkan.
- Jika dialog Story Mode muncul, gunakan START untuk melewati dialog, bukan Circle. Circle hanya untuk konfirmasi pilihan/menu ketika sesuai konteks.
- Pastikan tidak ada marker satu-kali atau Actions run duplikat yang masih queued/in progress sebelum memulai run berikut.
- Repo tetap satu-satunya yang diizinkan. ROM, BIOS, savestate, Memory Card, dan screenshot gameplay privat tidak boleh di-commit ke Git.

## LATEST STORY MODE CONTINUATION — START skipped the Konoha dialogue; fresh process reached f175 (21 October 2026, 18:20 WIB)

- Run [#39591032125](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39591032125) completed with workflow conclusion `success`. It restored the verified pre-START dialog checkpoint, issued exactly one START press at relative VSync f120 and release at f121 (both controller readbacks PASS), then stopped internal screenshot requests after f130. No Circle input was sent.
- The first process created derived checkpoint `konoha-after-start-f140.sstate`: 21,162,630 bytes, SHA-256 `3a0bb3f37537f393bcb1479f9a478bf90367ae669418523f12a34cfa39984034`.
- A **fresh emulator process** restored that derived checkpoint, sent no controller input, and advanced through relative frame **175**. It successfully created successor checkpoint `konoha-successor-checkpoint-f175.sstate`: 21,163,375 bytes, SHA-256 `f8bd00074877ef583e35b8eaf2fc65b3877acda9bebd5f2d8e9a13abee094615`.
- Internal screenshots: 11 valid original emulator captures; maximum callback frame f130; `KONOHA_P1_SCREENSHOT_PROBLEMS=none`. Phase 2 had **no internal screenshots at all**. Its external X11 capture at relative f9 is valid at 1280×800 (729,022 bytes, 93,474 colors), and shows the Konoha forest board with Naruto/Mizuki HUD values 1500–1500 and no dialogue panel. This is evidence the START transition reached the board/map view; it is not evidence that Story Mode is complete or that a full mission objective was completed.
- Source dialog checkpoint remained unchanged: 21,162,258 bytes, SHA-256 `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`. Parent stable checkpoint likewise remains `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee`.
- Private artifact #12342641041, [run artifact page](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39591032125), is 5,832,046 bytes and ZIP digest `sha256:dbdea33e9b0e05a0ddf0a30242a8827959ca5b1e829f10e77d943d654bfb6009`; the digest was verified after download. Screenshots and savestates remain in the private artifact only; none were committed to Git.
- The one-shot marker `experiments/.run-storymode-konoha-resume` was deleted in cleanup commit `e78e85b6b9ff0be7a95bb8e77934c5d2155c4547`. Follow-up checks must keep the Actions queued/in-progress count at zero.
- Next step: treat the f175 successor state as the new immutable baseline and perform a **single isolated controller test per fresh process**, beginning with a direction input against a no-input control. Later-position visuals must be captured externally via X11 only; do not use internal emulator screenshot APIs on the restored later state. Never use web images as gameplay evidence. If a dialogue appears in a gameplay continuation, use START, not Circle.

## LATEST FORENSIC UPDATE — live GDB observation run #39588281198 (21 October 2026, 17:59 WIB)

- Run [#39588281198](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39588281198) completed with workflow conclusion `success` at 10:59:24 UTC. It launched the PCSX-Redux ELF under GDB with `handle SIGSEGV stop print nopass`, default renderer selection, and **no controller input**. The successful workflow conclusion means diagnostics/upload/cleanup completed, not that a crash was captured.
- The emulator emitted frame callbacks through **f172**, then the watchdog saw no new callback for **2.549 seconds**. The process snapshot showed the emulator in `Sl`, about 141% CPU, and `wchan=futex_do_wait`. The outer 60-second timeout ended the observation with exit code **124**. GDB reported “Detaching after fork from child process 939”; account for child processes in any follow-up debugger design.
- Two external X11 captures were validated at 1280×800: 779,024 bytes / 132,620 colors and 782,555 bytes / 133,528 colors; they were not pixel-identical. The authentic game image still shows the Naruto dialogue box, Circle prompt and HUD 1500–1500. This does **not** establish active mission gameplay or Story Mode completion.
- The artifact contains 28 valid original internal screenshots, limited to f001–f130; `DIAG_SCREENSHOT_PROBLEMS=none`. There were no internal screenshot requests after f130. ZIP artifact #12340928025 is 4,925,017 bytes with digest `sha256:0e56ef7b7fc1288ff232b75b2ca394b9f0a799688f8351b0bf4193d542c7951f` (digest verified locally).
- **No natural SIGSEGV was caught**: `DIAG_GDB_SIGSEGV_CAUGHT=NO_OBSERVED_BEFORE_TIMEOUT`, `DIAG_NATIVE_SIGNAL_TRACE_CAPTURED=NO`, `DIAG_CORE_FOUND=NO`, `DIAG_GDB_POSTMORTEM=NOT_RUN`. The kernel core pattern still pipes to `systemd-coredump`, so `ulimit -c unlimited` alone does not produce a runner-local core file.
- Checkpoints remain unchanged: stable parent 21,163,483 bytes SHA-256 `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee`; pre-START dialog checkpoint 21,162,258 bytes SHA-256 `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`. No input was sent.
- Interpretation: launching under GDB changes the observed stall from the earlier f153–154 region to f172 in this run, but one timeout cannot identify why. The different X11 captures rule out pixel-identical static output only; they do not prove forward game progress. Root cause of SIGSEGV run #39574435847 remains unknown. Do not repeat this configuration unchanged; review fork tracking and direct SIGSEGV capture before deciding on a new diagnostic run.

## LATEST FORENSIC UPDATE — extended natural-crash observation through outer timeout, run #39586201539 (21 October 2026, 17:42 WIB)

- Run [#39586201539](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39586201539) completed with workflow conclusion `success` at 10:41:59 UTC. This continued the lightweight `catchsegv` test without GDB attached to the live emulator. No controller input was sent; the default renderer selection was retained.
- The frame callback stopped at **f154**; the watchdog confirmed no new callback for **2.554 seconds**. The process snapshot at stall showed `Sl`, about 159% CPU in the captured `ps` sample, and `wchan=futex_do_wait`. Unlike run #39585486518, the watchdog did **not** send SIGTERM after the screenshots; it left the emulator untouched until the existing outer 60-second timeout ended the process (exit code **124**).
- Two external X11 captures were valid at 1280×800: 781,067 bytes / 133,238 colors and 778,200 bytes / 131,633 colors. They were not pixel-identical. The original screenshots show a Naruto dialogue box, Circle prompt and HUD 1500–1500; subtle screen elements/sprite position change between captures even though no new frame callback is logged. This still does not prove an active mission or Story Mode completion.
- The extended observation did not produce a natural SIGSEGV, handler backtrace, or local core file. The report records `DIAG_CORE_FOUND=NO`, `DIAG_GDB_POSTMORTEM=NOT_RUN`, `DIAG_NATIVE_SIGNAL_TRACE_CAPTURED=NO`, and `DIAG_NONE_RESULT=STALL_OR_TIMEOUT_WITHOUT_START`. Thus the longer no-interruption window also fails to reproduce the original fatal crash.
- Artifact [#12340070622](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39586201539/artifacts/12340070622): 4,922,274 bytes; ZIP digest `sha256:6dd13863e749ae002bcb64164cfcf2d55b43d8000108b061c57455764ec891d4`. It includes 28 valid original internal screenshots through f130 only (`DIAG_SCREENSHOT_PROBLEMS=none`), two validated X11 captures, watchdog log and process snapshot. ZIP digest was rechecked after download. Parent checkpoint remained unchanged with SHA-256 `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee`; the pre-START dialog checkpoint was restored as a read-only copy with SHA-256 `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`.
- Interpretation: two no-input runs—one stopped by the watchdog after a 3-second post-capture window (#39585486518), the other allowed to run until the 60-second outer timeout (#39586201539)—both stall near f153–154 but fail to reproduce a natural SIGSEGV. X11 contents continue changing, so a total display/process deadlock is not established. Root cause of #39574435847 remains unknown. The one-shot trigger was deleted after this run (cleanup commit `1076dd3bf151915551e4469769e3c79541402dbf`); post-cleanup verification must keep queued/in-progress Actions at zero.

## LATEST FORENSIC UPDATE — lightweight signal-time trace run #39585486518 (21 October 2026, 17:35 WIB)

- Actions run [#39585486518](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39585486518) completed with workflow conclusion `success` at 10:35:18 UTC. This was a diagnostic run only: the emulator was launched through glibc `catchsegv` (`/usr/bin/catchsegv`), without GDB attached to the live process and with **no controller input**.
- The emulator/frame callback last reported **frame 153**. The watchdog confirmed no new callback for **2.571 seconds**. The process snapshot showed `Sl`, about 160% CPU in the captured `ps` sample, and `wchan=futex_do_wait`. Two external X11 captures were valid at 1280×800: 779,626 bytes / 132,431 colors and 780,189 bytes / 132,972 colors. They were not pixel-identical, so the display still changed even though the frame callback had stopped.
- After a further 3-second natural-crash observation window, no natural SIGSEGV, signal-time backtrace, or local core file appeared. The watchdog sent SIGTERM to the emulator. `catchsegv` returned wrapper exit code 255; the run’s original report called this `INCONCLUSIVE rc=255`, which was a classification gap, not evidence of a natural crash. Workflow classifier corrected afterward in commit `5944594eacb4fa89c5bb2df56294ba8ef4b4c65c` to classify this exact watchdog-stop case as a stall with no natural SIGSEGV observed during the window.
- Artifact [#12338379652](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39585486518/artifacts/12338379652): 4,922,798 bytes; ZIP digest `sha256:eccc7922d1e7b8a032768bed20ca8b09f87f86fed0cb7ec3a97b8475c5bc41d4`. The artifact reports 28 valid original internal screenshots only through f130 (`DIAG_SCREENSHOT_PROBLEMS=none`), and both external X11 captures. Core analysis says `DIAG_CORE_FOUND=NO`, `DIAG_GDB_POSTMORTEM=NOT_RUN`, and `DIAG_NATIVE_SIGNAL_TRACE_CAPTURED=NO`.
- Source checkpoint verification passed: parent stable checkpoint SHA-256 remained `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee`; pre-START dialog checkpoint stayed the verified read-only copy (21,162,258 bytes; SHA-256 `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`). The original X11 evidence still shows the Naruto dialogue, Circle prompt and HUD 1500–1500; it does **not** prove an active mission or Story Mode completion.
- Conclusion: running without GDB did not reproduce the natural SIGSEGV and yielded no fatal backtrace. It reproduced the f153 callback stall, while valid X11 captures continued changing. This supports investigating a rendering/timing stall, but neither proves a deadlock nor identifies the cause of the earlier SIGSEGV. The one-shot marker was removed after completion (cleanup commit `9d7ce0e16b077c6d4ef86019ba1f1330dced1fdb`); follow-up verification found 0 queued and 0 in-progress Actions runs.

## PEMBARUAN FORENSIK TERBARU — GDB menemukan stall di jalur renderer; akar SIGSEGV belum terbukti (21 Oktober 2026)

- **Run #39574435847** ([Actions](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39574435847)): frame terakhir 151, proses keluar 139 (`Segmentation fault (core dumped)`), `wchan=vfs_coredump`. Capture X11 pertama valid (1280×800, 777.527 byte, 131.762 warna); capture kedua hitam seragam 458 byte dan ditolak. Screenshot valid memperlihatkan dialog Naruto masih terbuka, prompt Circle, HUD 1500–1500; **bukan** bukti misi aktif.
- **Run #39576146808** ([Actions](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39576146808)): tidak mereproduksi SIGSEGV; frame terakhir 152 lalu timeout 124. Kedua screenshot X11 valid dan berbeda. `/proc/sys/kernel/core_pattern` mengarahkan dump ke `systemd-coredump`, tidak ada file core lokal yang bisa dipakai GDB.
- **Run #39576905583** ([Actions](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39576905583)): di bawah GDB frame terakhir 153; setelah stall, watchdog mengirim SIGINT diagnostik dan stack semua thread terekam. Thread utama berada di `__pthread_cond_wait` melalui `libgallium` → `libGLX_mesa` → `SDL3` → alamat tanpa simbol di binary `pcsx-redux`; thread renderer `llvmpipe` juga terlihat. Tidak ada SIGSEGV pada run ini.
- **Run #39577470148** ([Actions](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39577470148)): hasil sejalan; frame terakhir 153, dua screenshot X11 valid (779.646 byte/133.597 warna dan 779.635 byte/133.175 warna), lalu stack stall GDB dengan SIGINT. Hasil diagnostik `GDB_BACKTRACE_CAPTURED_AFTER_VSYNC_STALL_NO_START`; wrapper exit 0 hanya berarti GDB menyelesaikan capture, bukan mencapai f175.
- **Interpretasi terukur:** dua backtrace stall menempatkan thread utama pada penantian sinkronisasi renderer/OpenGL Mesa/SDL. Ini mengarahkan penyelidikan stall ke jalur renderer, tetapi belum mengidentifikasi penyebab SIGSEGV run #395744 dan bukan bukti Mesa/SDL penyebab crash fatal. Binary `pcsx-redux` stripped; core dump tidak tersedia di ruang kerja.
- Semua run diagnostik ini tanpa input controller; checkpoint dialog pra-START tetap 21.162.258 byte SHA-256 `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`; checkpoint induk tetap 21.163.483 byte SHA-256 `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee`. Screenshot internal hanya sampai f130 dan valid; screenshot eksternal hanya X11 asli. Tidak ada START yang dikirim, checkpoint tidak diganti, dialog masih terlihat; misi aktif/tamat tetap belum terbukti.
- **Run pembanding #39577891131** ([Actions](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39577891131)) selesai `success`: `GALLIUM_DRIVER=softpipe` diminta, frame callback terakhir 153; proses tetap aktif sekitar 98,3% CPU dan GDB menangkap instruction pointer di `libgallium` setelah SIGINT diagnostik, tanpa SIGSEGV alami. Dua screenshot X11 valid 794.275 dan 794.685 byte; keduanya menunjukkan dialog Naruto dan prompt Circle, serta berbeda 6.899 pixel (0,674%). Thread `llvmpipe` tak terlihat, tetapi renderer aktif belum dibuktikan lewat renderer string. Ini mungkin slow frame renderer software, bukan deadlock yang terkonfirmasi. Artefak privat #12334054908, digest ZIP `sha256:2f289d7cceb6673ea7e8ea1ba6d356bea8b71fca9d4f31351a84c91bc72bb7f9`. Workflow setelah uji ini telah dikembalikan ke pemilihan renderer default; `GALLIUM_DRIVER=softpipe` tidak dipaksakan untuk baseline berikutnya.
- **Kesimpulan:** SIGSEGV #395744 tetap belum punya backtrace fatal. GDB run #395769/#395774 menemukan thread utama menunggu melalui `libgallium` → `libGLX_mesa` → `SDL3`; run #395778 dengan softpipe berhenti di `libgallium` sambil menggunakan CPU tinggi. Petunjuk mengarah ke jalur renderer/timing, tetapi **akar penyebab SIGSEGV belum teridentifikasi**. Checkpoint induk hash `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee` tidak berubah; tak ada input controller; screenshot internal tetap dibatasi sampai f130. Detail dan batas kesimpulan: [docs/SIGSEGV_FORENSICS_2026-10-21.md](docs/SIGSEGV_FORENSICS_2026-10-21.md).

---

## DIAGNOSTIK TERBARU — watchdog eksternal dan screenshot X11 pada frame 151 (21 Oktober 2026, 16:08:25 WIB)

- Run [#39574435847](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39574435847) selesai dengan conclusion workflow **success**, tetapi proses emulator berakhir dengan exit code **139 (SIGSEGV)**. Workflow berhasil mengumpulkan bukti; itu tidak berarti emulator menyelesaikan target frame.
- Tidak ada tombol kontrol dikirim. Checkpoint dialog pra-START tetap dialog-entry-f178.sstate (21.162.258 byte, SHA-256 c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c); checkpoint induk sumber 21.163.483 byte, SHA-256 b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee lolos verifikasi dan tidak berubah.
- Observer eksternal terakhir melihat DIAG_NONE_FRAME=151 pada 16:08:10.907 WIB. Setelah 2,576 detik tanpa frame baru, watchdog mengonfirmasi stall pada 16:08:13.485 WIB dan menangkap layar via X11/XWD dari luar emulator, tanpa memanggil PCSX.GPU.takeScreenShot() pada frame 131 ke atas.
- Screenshot X11 pertama valid: 1280×800 RGB, 777.527 byte, 131.762 warna. Gambar asli memperlihatkan layar game dengan dialog Naruto masih terbuka, prompt Circle, dan angka 1500–1500 di HUD. Ini membuktikan tampilan dialog tersebut masih terlihat saat watchdog menangkap layar, **bukan** bahwa misi aktif.
- Screenshot X11 kedua diambil sekitar 2,3 detik kemudian dan berupa gambar seragam hitam (458 byte; satu warna), sehingga ditolak sebagai bukti visual. Snapshot proses ketika stall mencatat AppRun pada state Sl, wchan=vfs_coredump, dengan exit 139 segera setelah itu. Ini mengarah kuat ke jalur core-dump akibat crash fatal; akar penyebab crash belum diketahui.
- Validasi screenshot internal hanya mencakup f001–f130: 28 gambar asli, DIAG_SCREENSHOT_PROBLEMS=none. Tidak ada screenshot internal setelah f130. Artefak privat [#12333511723](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39574435847/artifacts/12333511723), ukuran 4.139.742 byte, digest ZIP sha256:63497731a6e361aff98f9e0f2f0a895010987b87250aadfc72c82a74ba6ed23c.
- Cross-check [#39573924538](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39573924538) memakai timestamp pada callback Lua: frame terakhir 140, stall teramati 2,549 detik, lalu timeout 124. Dua screenshot X11 non-seragam pada run itu berbeda 13.172 piksel dari 1.024.000 (1,286%); area teks dialog tetap identik. Proses saat itu tercatat menunggu di futex_do_wait, bukan vfs_coredump. Run awal [#39573533078](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39573533078) juga berhenti pada f140/timeout 124, tetapi watchdog gate f145 terlalu tinggi sehingga tidak mengambil gambar eksternal.
- **Kesimpulan:** callback/log VSync berhenti pada f151 sebelum proses crash pada run ini. Segfault dapat direproduksi walau screenshot internal di sekitar f150 sengaja tidak dipanggil, sehingga pemanggilan screenshot internal terlambat **bukan syarat yang diperlukan** untuk crash ini, walaupun hubungan kausal pada run lama belum dapat dipastikan. Misi aktif dan Story Mode tamat tetap belum terbukti.
- **Langkah berikutnya:** selidiki crash/core-dump (stderr, status thread, dan cara memperoleh backtrace/core dump secara aman) terlebih dahulu. Jangan mengulang tap START satu-VSync yang sama; jangan mengubah checkpoint; jangan memakai Circle untuk melewati dialog; pertahankan screenshot asli emulator/X11 sebagai satu-satunya bukti visual gameplay.

---

## DIAGNOSTIK TERBARU — screenshot dihentikan pada f130, NONE vs START (21 Oktober 2026, 15:38:40 WIB)

- Run paired [#39570556284](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39570556284) selesai dengan conclusion workflow `success` pada 15:38:40 WIB (durasi sekitar 2 menit 11 detik). Artinya langkah emulator, validasi, upload artefak, dan pembersihan runner berhasil dijalankan; **kedua proses emulator sendiri berakhir timeout, bukan selesai normal**.
- Artefak privat [#12331189717](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39570556284/artifacts/12331189717), ukuran 6.715.120 byte, digest ZIP `sha256:32c4a6313cbad378bf89a118a701b316552622ade57cb0687222c5d1f63c62c1`. Artefak kedaluwarsa 4 November 2026 sekitar 15:38 WIB. Checksum ZIP diperiksa ulang setelah unduh.
- Dua cabang memakai checkpoint dialog pra-START yang sama: 21.162.258 byte, SHA-256 `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`. Checkpoint induk tetap tidak berubah: 21.163.483 byte, SHA-256 `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee`.
- Screenshot dari callback emulator dibatasi sampai frame 130; tidak ada permintaan screenshot pada frame 131 atau lebih sesudahnya. Kontrol `NONE` mencatat VSync/frame sampai f154 lalu timeout (kode 124). Cabang `START` menekan START satu VSync di f120, melepaskannya di f121; readback press/release keduanya PASS. Cabang ini mencatat frame hingga f151 lalu timeout (kode 124). Kedua cabang tidak lagi menghasilkan frame selama sisa timeout 30 detik, tidak mencatat segfault pada run ini, dan tidak mencapai target f175.
- Screenshot asli dua cabang identik pixel-for-pixel pada f1–f125. Divergensi pertama terukur pada f126 (99,7943% piksel tetap identik; MAD 0,108524); f128: 74,3594% piksel identik, MAD 15,380616; f130: 73,7878% identik, MAD 15,748424. Gambar f130 cabang START menampilkan dialog Naruto yang sedang bergerak/bergeser, bukan bukti misi aktif.
- Validasi artefak menerima 56 screenshot asli (28 per cabang); `DIAG_SCREENSHOT_PROBLEMS=none`. Validator secara eksplisit menolak buffer raw kosong, ukuran/dimensi salah, PNG kosong, dan gambar seragam satu warna; bukti f130 wajib tersedia di kedua cabang.
- Run pendahulu [#39570013344](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39570013344) juga mematikan screenshot setelah f130 dan kontrol `NONE` berakhir timeout (124) setelah frame terakhir f151, bukan segmentation fault; artefaknya #12331014609 (3.359.778 byte, digest `sha256:1fae303ee0bbc8cd2c7c816618b6db65f888f7e490eaac52a1e16f1b5fbcacb3`). Ini memperkuat indikasi bahwa permintaan screenshot di sekitar f150 terkait dengan segfault terdahulu, tetapi **belum membuktikan kausalitas**. Pada run paired pun, menekan START tidak menghilangkan stall di sekitar f151.
- Workflow diperbarui lewat commit `227c71808997d4dc94d69d4d483ed4ca77280b1d` (kontrol tanpa input, batas screenshot f130, validasi buffer diperketat) dan `a2f3b20a7e85bfc106175d14cd155ed9d17aa99c` (kontrol NONE vs tap START, target log f175, batas waktu 30 detik). Trigger satu-kali telah dihapus lewat commit `c7ff890e6ecc715712257f23c4c0072793c3c3d7`; workflow pemicu cleanup #39571044132 berstatus `skipped`, tidak ada run aktif pada pemeriksaan terakhir.
- **Status misi:** belum terbukti aktif. Hasil memastikan START masih menyebabkan perubahan visual sebelum f130, tetapi runtime berhenti memajukan VSync sekitar f151–f154. Jangan mengulang tap START yang sama. Langkah berikut yang paling informatif adalah mendiagnosis stall/VSync tanpa memanggil fungsi screenshot internal di sekitar f150, misalnya menguji pengambilan layar eksternal X11 atau watchdog/timestamp VSync; pertahankan kedua checkpoint serta jangan gunakan Circle untuk melewati dialog.

---

## HASIL TERBARU — kontrol setara tanpa input vs START tertunda (21 Oktober 2026, selesai 14:53:39 WIB)

- Run [#39565014834](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39565014834) selesai 14:53:39 WIB dengan conclusion workflow `failure`. Artefak privat [#12329546573](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39565014834/artifacts/12329546573), 7.101.006 byte, digest `sha256:f1052ba271d25e7668cc809455ef7ad59fb7ac84c05e081027f7c4fd4f6f2f45`. Tidak ada eksperimen aktif setelah pemeriksaan; marker pemicu satu-kali sudah dihapus.
- Kedua cabang memulihkan checkpoint dialog pra-START yang sama: 21.162.258 byte, SHA-256 `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`. Checkpoint induk stabil 21.163.483 byte dengan SHA-256 `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee` tetap tidak berubah.
- **Respons visual START terverifikasi:** cabang tanpa input dan cabang START identik pixel-for-pixel pada screenshot frame 1–125. START ditekan satu VSync pada frame 120 dan dilepas frame 121; readback press/release keduanya PASS. Mulai frame 126 terlihat perbedaan kecil (99,794% piksel tetap identik; MAD 0,109), di frame 128 dialog/portrait bergerak ke kiri (74,359% piksel identik; MAD 15,381), dan pada screenshot asli frame 150 panel dialog sudah menghilang sehingga papan/area permainan terlihat kembali. Ini membuktikan START memicu kemajuan visual/animasi penutupan dialog pada konteks ini.
- **Batas bukti:** frame 150 itu belum membuktikan misi berjalan aktif atau Story Mode selesai. Tidak ada input gameplay setelah tap START dan belum ada bukti penyelesaian misi.
- **Runtime belum stabil pada kedua cabang:** cabang tanpa input melaporkan frame 150 lalu segmentation fault (kode 139); screenshot `DIAG-NONE-f150` tercatat tetapi buffer gambarnya nol byte, sehingga verifikasi screenshot menolak artefak itu. Cabang START menghasilkan screenshot asli frame 150, lalu tidak bergerak lagi dan timeout (kode 124) setelah batas 20 detik. Karena kontrol tanpa START juga crash pada frame 150, hang/segfault bukan bukti bahwa START sendirilah penyebab tunggal. Workflow berakhir `failure` akibat validasi buffer screenshot kontrol yang kosong, bukan karena semua eksperimen gagal.
- **Langkah diagnostik selanjutnya:** jangan mengulang tap START yang sama. Jalankan kontrol tanpa input dengan pengambilan screenshot dihentikan sebelum frame 150, sambil tetap mencatat VSync, untuk memisahkan crash emulator dari masalah fungsi screenshot. Setelah itu, lanjutkan dari checkpoint dialog pra-START yang sama jika pemulihan masih lulus. Semua bukti gameplay tetap berasal dari screenshot asli emulator dan artefak run terverifikasi.

## HASIL TERBARU — uji START pada dialog Naruto (21 Oktober 2026, 14:01 WIB)

- Run terbaru [#39558959143](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39558959143) selesai `failure` pada 14:01:53 WIB. Tidak ada run workflow dialog START yang masih aktif pada pemeriksaan setelah selesai. Pemicu satu-kali sudah dihapus agar tidak memicu eksperimen duplikat.
- Artefak screenshot/log privat [#12326872574](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39558959143/artifacts/12326872574), sekitar 1,96 MB; tangkapan asli diperiksa langsung setelah diunduh dari artefak.
- **Terverifikasi:** checkpoint stabil terakhir dapat dipulihkan dalam proses emulator baru. Dialog dengan potret dan nama Naruto tampak pada screenshot asli f179. START ditekan dan dilepas sebagai tap satu-VSync; log readback menandai press f179 dan release f180 sebagai PASS. Screenshot f180 berbeda dari f179 (MAD RGB 16,637; sekitar 28,41% piksel berubah), tetapi f180 dan f181 identik tepat (MAD 0; 100% piksel identik).
- **Kegagalan run:** emulator berhenti menghasilkan frame setelah f181 dan proses berakhir karena timeout (kode 124). Tap START kedua yang direncanakan setelah f182 **tidak pernah terkirim**. Run sebelumnya #39558656073 menunjukkan frame hingga f182 tetapi berakhir segmentation fault (kode 139). Run #39558242453 juga timeout setelah f181 ketika START ditahan lebih lama.
- **Batas kesimpulan:** START memang dikirim sesuai aturan, tetapi perubahan f179→f180 belum membuktikan START menyebabkan transisi karena tidak tersedia kontrol tanpa input yang sepadan pada checkpoint dialog. Dialog tidak terbukti tertutup; belum ada screenshot yang membuktikan misi aktif. Belum ada bukti Story Mode tamat.
- **Langkah berikutnya:** jangan mengulang eksperimen yang sama tanpa mengatasi freeze/crash sekitar frame 181. Pertahankan checkpoint induk dan checkpoint stabil; diagnosis runtime/frame scheduling terlebih dahulu atau ambil checkpoint dialog dari titik yang tidak mengalami crash, lalu uji START dalam cabang yang dipisahkan. Bukti visual gameplay hanya dari screenshot emulator asli.

## PEMBARUAN RISET TERBARU — 21 Oktober 2026, 13:25 WIB

- Validasi setelah perbaikan assertion: run [#39555023915](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39555023915), mulai 13:22:40 dan selesai 13:25:23 WIB (2 menit 43 detik), status akhir `failure`. Assertion sekarang benar menargetkan f180. Kegagalan baru disebabkan cabang kontrol `NONE` timeout 25 detik (kode 124), sehingga frame baseline f180 tidak ada dan perbandingan penuh tidak dapat disahkan. Enam cabang input `UP/DOWN/LEFT/RIGHT/CIRCLE/START` masing-masing berakhir kode 0 dan mencapai f180; proses juga memulihkan checkpoint dan menghasilkan screenshot. Jangan menyebut run ini `success` atau menganggap perbandingan lengkap.
- Artefak privat run terbaru: [#12324829071](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39555023915/artifacts/12324829071), 12.288.355 byte, digest ZIP `sha256:04a010dc88d6b40b8fc7ce1339bff7e03d56d4ad03035682670c749a6254312d`. Checkpoint baru di dalamnya: 21.163.483 byte, SHA-256 `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee`; hash ZIP dicocokkan kembali. Tidak ada ROM, BIOS, atau file Memory Card di artefak.
- Bukti lengkap terbaik tetap run [#39553585285](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39553585285), artefak privat [#12323544613](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39553585285/artifacts/12323544613). Walau status workflow-nya `failure` karena assertion usang yang mencari f60, report dalam artefak membuktikan semua tujuh cabang berhasil mencapai f180 dan screenshot lengkap. Checkpointnya 21.163.261 byte, SHA-256 `1f9da9ca07fb95a8afda5016799852f4e0fdda2d589c8d11e99b0f8e8ade4875`; Circle menghilangkan banner `始め！` dan mencapai tampilan dialog Naruto, sedangkan `NONE`, D-pad, dan `START` identik dengan kontrol di sampel hingga f180.
- Run [#39554130946](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39554130946) sebelumnya juga gagal: cabang `RIGHT` segmentation fault (kode 139) dan cabang `CIRCLE` timeout (kode 124) setelah f150, jadi checkpoint dialog tidak berhasil dibuat. Log ini memperlihatkan ketidakstabilan runtime yang nyata.
- Workflow saat ini tetap pada [`.github/workflows/naruto-storymode-post178-advance.yml`](.github/workflows/naruto-storymode-post178-advance.yml), assertion f180 telah diperbaiki dan percobaan simpan checkpoint dialog yang tidak stabil sudah dibuang (commit `544b96641518cbfc2fafdaa7c38e98ed521dd80b`). Run [#39555023915](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39555023915) adalah hasil aktual pertama sesudah perubahan; belum ada run aktif, dan marker trigger sekali-pakai sudah dihapus.

**Status gameplay:** Circle memberi respons visual terverifikasi dari banner `始め！` menuju papan dan tampilan dialog Naruto pada eksperimen lengkap #39553585285. Belum ada bukti Story Mode tamat, mekanik gerak/perebutan wilayah yang sudah terverifikasi, atau save/load Memory Card in-game. Selanjutnya, atasi timeout pada cabang `NONE` atau gunakan uji kontrol dengan batas yang lebih konservatif sebelum mengklaim perbandingan setara f180 lengkap.

## Pembaruan sebelumnya — 21 Oktober 2026, 13:16 WIB

- Workflow yang benar tetap [`.github/workflows/naruto-storymode-post178-advance.yml`](.github/workflows/naruto-storymode-post178-advance.yml). Run [#39553585285](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39553585285) mengumpulkan eksperimen penuh sampai 180 VSync per cabang, tetapi berakhir `failure` karena assertion shell masih mencari `frame=60` padahal target sudah diubah ke `frame=180`. Pada run tersebut, seluruh cabang mencapai f180 dan screenshot valid; status gagal berasal dari assertion usang, bukan kegagalan seluruh eksperimen.
- Checkpoint pascakonfirmasi yang dipakai pada run tersebut: `stable-postconfirm-checkpoint.sstate`, 21.163.261 byte, SHA-256 `1f9da9ca07fb95a8afda5016799852f4e0fdda2d589c8d11e99b0f8e8ade4875`. Pemulihan checkpoint dalam proses emulator baru berhasil. Checkpoint induk tetap `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`; checkpoint turunan sumber tetap `a87529407736b1b7648785db8644d3c10f0b8d5d12f1557c63d9a3155b22fa83`.
- Bukti privat lengkap: [artefak #12323544613](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39553585285/artifacts/12323544613), ukuran 12.344.333 byte, digest ZIP `sha256:620d857a0e79aa4bec86da50a1c92f1f4563753b16a0fe6ae3935d25c6f50d13`. Hash ZIP dan checkpoint diverifikasi kembali lokal. Artefak tidak menyertakan ROM, BIOS, atau Memory Card.
- Hasil utama: dari checkpoint yang sama, `CIRCLE` ditekan pada f90 dan dilepas f98. Cabang `NONE`, `UP`, `DOWN`, `LEFT`, `RIGHT`, dan `START` tetap identik dengan kontrol di seluruh frame pembanding hingga f180. Cabang `CIRCLE` mulai berbeda di f97 (MAD 1,913; piksel identik 69,432%), perbedaan membesar di f120 (MAD 56,297; piksel identik 7,862%) dan f180 (MAD 70,194; piksel identik 6,029%). Pada kontrol, banner `始め！` tetap ada; pada cabang Circle banner menghilang, papan terlihat tanpa banner, lalu f180 menampilkan panel dialog berpotret Naruto. Ini membuktikan respons visual yang kuat terhadap Circle pada konteks ini, belum membuktikan misi selesai atau Story Mode tamat.
- Uji berikutnya [#39554130946](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39554130946) berakhir `failure` pada 13:16:08 WIB. Cabang `RIGHT` mengalami segmentation fault (kode 139) dan tangkapan f180-nya kosong; cabang `CIRCLE` timeout (kode 124) setelah f150 sehingga tidak menghasilkan checkpoint dialog. Karena perbandingan tidak lengkap, run ini tidak membatalkan temuan visual sebelumnya; sebaliknya, ia menunjukkan ketidakstabilan runtime yang masih perlu ditangani.
- Empat eksperimen pendek #39552282942, #39552697314, #39552998498, dan #39553261685 menyelesaikan validasi checkpoint/restore dan kontrol setara 60 VSync. Dalam konteks lebih awal saat panel masih bergerak, tidak ada perbedaan visual dari Circle/START atau arah D-pad; temuan itu tidak boleh digeneralisasi ke banner `始め！` yang diuji pada f90.
- Workflow sudah dibersihkan dari kode checkpoint dialog yang belum stabil dan assertion diperbaiki agar mengharapkan f180 (commit `544b96641518cbfc2fafdaa7c38e98ed521dd80b`). Run terbaru seluruhnya sudah berhenti; marker trigger sekali-pakai telah dihapus. Tidak ada run aktif pada pemeriksaan terakhir.

**Status gameplay:** checkpoint stabil dapat dipulihkan dan Circle terbukti memajukan layar dari banner `始め！` ke dialog visual. Kemajuan misi/aturan gerak belum sepenuhnya diverifikasi. Belum ada bukti tamat Story Mode atau save/load Memory Card in-game. Langkah berikutnya yang aman adalah mengambil checkpoint pada bagian transisi yang stabil sebelum runtime crash, lalu menguji `START` di konteks dialog dengan proses emulator terisolasi; jangan menimpa checkpoint induk.

## Pembaruan sebelumnya — 21 Oktober 2026, 11:53 WIB

- Run eksperimen [#39546339666](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39546339666) berstatus akhir `success`, mulai 11:51:43 WIB dan selesai 11:53:02 WIB (sekitar 1 menit 19 detik). Workflow berhasil mengumpulkan bukti, membandingkan gambar, mengunggah artefak privat, lalu membersihkan runner.
- Artefak privat [#12321752942](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39546339666/artifacts/12321752942), `naruto-storymode-post178-advance-private`, 3.640.848 byte, digest ZIP `sha256:20df28b96b8e4613c9dd5f298be82443b84f80203c2c7166409d43a51a7f5221`. Laporan rinci: [docs/STORYMODE_POST178_CONTINUATION_2026-10-21.md](docs/STORYMODE_POST178_CONTINUATION_2026-10-21.md).
- Checkpoint turunan privat [#12314982935] dipulihkan dari proses emulator baru dan berjalan 62 VSync tanpa input; proses turunan berakhir kode 0. Checkpoint turunan 21.162.838 byte SHA-256 `a87529407736b1b7648785db8644d3c10f0b8d5d12f1557c63d9a3155b22fa83`. Checkpoint induk 21.162.405 byte SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`; hash keduanya tetap sama setelah runtime.
- Cabang kontrol yang memuat checkpoint induk dan hanya menekan Circle pertama f30–f38 mengambil screenshot sampai f187, lalu crash native kode `139`. Cabang turunan cocok tepat dengan kontrol sampai f181/turunan f3; perbedaan visual mulai f182/turunan f4 (`MAD=3.185, exact=0.96749`) dan membesar di f184/turunan f6 (`MAD=8.204, exact=0.91152`).
- Screenshot turunan f62 memperlihatkan panel `任務内容` masih ada, target `3000チャクラためる` dan `ついか条件なし` tetap terlihat, tetapi prompt `けってい` sudah hilang serta ada cap merah mirip `決`. Ini memverifikasi perubahan UI pascakonfirmasi dan bahwa proses turunan bisa berjalan melewati titik crash kontrol pada jendela observasi; **belum membuktikan gameplay misi aktif atau tamat**.
- Klasifikasi: **terverifikasi** — restore lintas-proses dan 62 VSync tanpa input, hash checkpoint tidak berubah, perbedaan visual pascakonfirmasi; **hipotesis** — konfirmasi mengalihkan UI/runtime dan terkait dengan perbedaan crash; **belum diketahui** — input lanjutan yang diperlukan, masuk gameplay aktif, save/load Memory Card in-game, serta tamat Story Mode.
- Pemicu sekali-pakai sudah dihapus. Pemeriksaan setelah run: tidak ada run eksperimen yang masih aktif. Langkah berikutnya: simpan state baru ketika panel pascakonfirmasi stabil, verifikasi restore-nya, lalu uji Circle/START/tanpa input sebagai cabang terisolasi.

---

## PEMBARUAN RISET TERBARU — 21 Oktober 2026, 09:01 WIB

- Run terbaru [#39530526794](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39530526794) selesai `success` pukul 09:01:53 WIB; tidak ada workflow yang sedang `in_progress` pada pemeriksaan terakhir.
- Eksperimen membandingkan cabang Circle awal lalu menunggu dengan cabang Circle awal lalu Circle kedua pada prompt konfirmasi. Screenshot cabang yang cocok sampai f178 identik: `MAD=0.000, exact=1.00000`. Input kedua tercatat tertekan pada f175 dan dilepas pada f178. **Belum ada bukti kemajuan Story Mode melewati prompt** dari perbandingan ini.
- Yang berhasil diverifikasi: checkpoint privat yang dibuat sesaat setelah tap kedua pada f178 dapat dimuat pada proses emulator baru, kemudian berjalan sampai f10; `FRESH_PROCESS_RESTORE=PASS`.
- Checkpoint turunan privat: 21.162.838 byte; SHA-256 `a87529407736b1b7648785db8644d3c10f0b8d5d12f1557c63d9a3155b22fa83`. Checkpoint induk tetap tidak berubah: 21.162.405 byte; SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`.
- Artefak privat #12314982935 berukuran 6.032.044 byte, digest ZIP `sha256:e23112ce7a6c2a7b65b6cc8dfa15bf41e94528228b6896060337fac68a5d7033`. ROM, BIOS, savestate, dan isi Memory Card tidak masuk Git. Detail: [docs/STORYMODE_CIRCLE_SECOND_CONFIRM_2026-10-21.md](docs/STORYMODE_CIRCLE_SECOND_CONFIRM_2026-10-21.md).
- Langkah lanjutan yang masuk akal: pulihkan checkpoint turunan dalam run terisolasi, jalankan beberapa VSync tanpa input tambahan, lalu bandingkan dengan cabang tunggu dari checkpoint induk. Ini diperlukan untuk menguji apakah game melanjutkan transisi setelah key release; jangan menganggap Story Mode berlanjut atau tamat sebelum ada bukti layar yang berbeda dan konsisten.

---

## HASIL TERBARU — follow-up Circle/START tervalidasi (21 Oktober 2026, 08:21 WIB)

- Run final [#39526690265](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39526690265) selesai `success` pada 08:21:22 WIB (durasi 1 menit 21 detik). Tidak ada Actions run yang masih aktif.
- Artifact privat #12313342874: `naruto-storymode-circle-followup-private`, 2.755.974 byte, digest ZIP `sha256:9988b3d34c24441ad13c8453f2e41af60cde0698a2f7b30130a2fc46c5b02a8d`, kedaluwarsa 4 November 2026 sekitar 08:21:17 WIB.
- Semua cabang berhasil: NONE berhenti pada f150; Circle-awal dan START-awal mencapai f180. Semua checkpoint berhasil dipulihkan dan parent tidak berubah. Frame pembanding yang cocok sampai f150: Circle mulai berbeda f37 (MAD 17.547; 15.772% piksel identik), berbeda pada f90 (MAD 52.710) dan f150 (MAD 42.588); START tetap identik dengan baseline sampai f150.
- Screenshot Circle f180 menampilkan panel `任務内容` (isi misi), target `3000チャクラためる` (mengumpulkan 3.000 Chakra), `ついか条件なし` (tanpa syarat tambahan), dan prompt `けってい` (konfirmasi). Pada f180 cabang START menampilkan papan/efek petak; baseline NONE f180 tidak tersedia, sehingga f180 diperlakukan sebagai observasi tambahan, bukan perbandingan setara.
- Dua follow-up sebelumnya punya status failure dari masalah workflow, bukan kegagalan pemulihan: #39525734387/#39525735032 (path staging salah) dan #39526446924 (path laporan akhir salah). Perbaikan teruji pada [#39526690265](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39526690265).
- Laporan terperinci: [docs/STORYMODE_CIRCLE_FOLLOWUP_2026-10-21.md](docs/STORYMODE_CIRCLE_FOLLOWUP_2026-10-21.md). Hasil probe awal: [docs/STORYMODE_CIRCLE_TIMELINE_2026-10-21.md](docs/STORYMODE_CIRCLE_TIMELINE_2026-10-21.md).
- Langkah berikutnya: bandingkan cabang dari checkpoint parent yang sama—Circle awal lalu tunggu vs Circle awal lalu Circle kedua untuk prompt `けってい`—dan observasi layar setelah konfirmasi. Jangan menimpa checkpoint parent. Target 3.000 Chakra baru terverifikasi sebagai teks tujuan layar; belum terbukti tercapai. Belum ada bukti Story Mode tamat atau save/load Memory Card in-game.
- Checkpoint parent: 21.162.405 byte, SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`. AppImage patched: `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`. ROM, BIOS, savestate, Memory Card tetap di luar Git.

---

---

---

---

---

---

---

## Koreksi hasil run Circle timeline — 21 Oktober 2026

- Run [#39523066920](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39523066920) selesai `failure` pada 21 Oktober 2026 pukul 07:55:38 WIB; mulai 07:43:47 WIB; durasi 11 menit 51 detik. Kegagalan ada pada langkah perbandingan, bukan saat unduh aset atau pemulihan checkpoint. Batas workflow 35 menit tidak tercapai.
- Checkpoint induk tervalidasi ulang: 21.162.405 byte, SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`. Binary patched yang digunakan kembali SHA-256 `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`. Semua cabang memuat checkpoint dan log mencatat `CIRCLE_TIMELINE_LOAD_EVENT=PASS` dan `CIRCLE_TIMELINE_LOAD_RETURNED=1`.
- Artifak privat [#12312483553](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39523066920) diunduh dan screenshot diperiksa. Semua lima cabang berhenti pada screenshot frame 150 tanpa `CIRCLE_TIMELINE_BRANCH_DONE`; tidak ada screenshot frame 180/240/300. Langkah menjalankan tiap cabang memberi batas timeout 120 detik, sehingga kegagalan kemungkinan adalah batas per-cabang sebelum frame 300. Ini keterbatasan harness; tidak menunjukkan kegagalan memulihkan checkpoint.
- Temuan parsial dari screenshot sinkron per frame:
  - `NONE` adalah baseline deterministik.
  - `CIRCLE_TAP_EARLY`: tombol Circle ditekan pada frame 30; screenshot sama dengan baseline pada frame 20–35, lalu berbeda mulai frame 37 (mean absolute RGB difference 17.547; pixel identik 15.772%). Pada frame 150 tampak transisi visual/figur karakter di jalur petak, berbeda dengan baseline. Ini **bukti awal input Circle memicu respons visual pada konteks/timing itu**, tetapi aksi game yang tepat (memilih, menggerakkan, atau konfirmasi) belum dipastikan.
  - `CIRCLE_HOLD30`: pola screenshot identik dengan tap awal pada seluruh frame yang tersedia; belum ada bukti menahan Circle memberi efek tambahan.
  - `CIRCLE_TAP_LATE`: menekan Circle pada frame 90 tidak mengubah screenshot terhadap baseline sampai frame 150.
  - `LEFT_TAP_EARLY`: screenshot identik dengan baseline sampai frame 150.
- Pembacaan tombol `pad.getButton` benar pada press/release, tetapi itu sendiri hanya memverifikasi sisi emulator; simpulan gameplay harus didasarkan pada respons visual di atas.
- Uji berikutnya dipersingkat untuk menyelesaikan cabang sampai frame 90, dengan batas timeout per-cabang yang sesuai. Pakai lagi checkpoint induk dan AppImage patched yang sama, tanpa build ulang; jangan menyentuh atau menimpa checkpoint induk.
- **Status:** checkpoint bisa dipulihkan; ada indikasi Circle awal menimbulkan transisi visual; kontrol gerakan/aksi belum teridentifikasi penuh, Story Mode belum dinyatakan berlanjut secara kanonis atau tamat, dan Memory Card save/load in-game belum terverifikasi.

---

## Hasil terbaru — uji respons tombol dan probe waktu Circle (21 Oktober 2026)

- Run [#39513285641](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39513285641) selesai `success` setelah 39 menit 39 detik (21 Oktober 2026, 06:10–06:50 WIB). Artifact privat [#12308661246](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39513285641) diunduh dan screenshot/log diperiksa.
- Kesepuluh cabang kontrol (NONE, START, CIRCLE, CROSS, TRIANGLE, SQUARE, UP, DOWN, LEFT, RIGHT) berhasil memuat checkpoint yang sama, mencatat event `ExecutionFlow::SaveStateLoaded`, dan mengonfirmasi pembacaan tombol tekan/lepas. Semua kontrol selain CIRCLE memiliki screenshot akhir identik dengan cabang NONE pada frame yang dibandingkan. CIRCLE berbeda nyata: mean absolute RGB difference `52.71042`, pixel identik `7.4453%`.
- Ini **bukan bukti final makna tombol Circle**: screenshot NONE sendiri berubah antara frame 20 dan frame 90 karena scene terus beranimasi. Hasil tersebut hanya membuktikan Circle berasosiasi dengan respons visual yang berbeda; perlu kontrol timing lebih rapat untuk memisahkan respons input dari animasi kamera/scene.
- Binary hasil rebuild dengan source base `0c3572c3db75f97542001e453ae80ba8c3f8acba` dan patch SPU/ADPCM dua-file yang sama diunggah sebagai bagian artifact privat #12308661246. SHA-256 AppImage: `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`; patch SHA-256 `9588ee95651c9841c4bc5e25bd34b4be41ac100a955511817f8a92901245b7b5`; applied diff SHA-256 `754d471acb8b7c468251d20ef19ac7fe8a4f66ec0d7f67807d07ac7aa9b0b46c`.
- Workflow [.github/workflows/naruto-storymode-circle-timeline.yml](.github/workflows/naruto-storymode-circle-timeline.yml) memakai ulang binary tersebut tanpa build ulang dan mengambil snapshot berturut-turut untuk NONE, CIRCLE tap lebih awal, Circle ditahan 30 frame, Circle tap terlambat, dan LEFT tap. Setiap cabang memuat checkpoint yang sama di proses baru dan menggunakan salinan Memory Card sementara; checkpoint induk tidak ditimpa.
- Run baru [#39523066920](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39523066920) sedang `in_progress`; saat pemeriksaan terakhir runner berada di tahap inisialisasi container. Workflow memiliki batas maksimum 35 menit sejak mulai 07:43:47 WIB, jadi batas maksimum waktunya sekitar **08:18:47 WIB pada 21 Oktober 2026**. Perkiraan praktis belum pasti; karena tidak ada rebuild emulator, target kerja sekitar 5–15 menit setelah runner mulai aktif, selama unduhan/runner tidak macet.
- **Story Mode belum dinyatakan berlanjut atau tamat.** Menunggu hasil time-series agar respons Circle bisa ditafsirkan dengan lebih hati-hati. Save/load Memory Card dalam game juga tetap belum diverifikasi. ROM, BIOS, savestate, dan isi Memory Card tetap di luar Git.

---

## Operasional terbaru — checkpoint patched diverifikasi, kontrol gameplay sedang diprobe (21 Oktober 2026)

- Artefak privat [#12268621845 dari run #39426068247](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39426068247) berhasil diunduh langsung. ZIP 2.367.857 byte; SHA-256 ZIP `dc701311a82855c61a95b37a99fd86e2580b0a475682cb7ad8fa9d5a33737358`, cocok dengan digest artifact GitHub.
- Checkpoint lanjutan diekstrak dari `captures/storymode-checkpoint-next.raw.sstate`: 21.162.405 byte, SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`; cocok dengan `probe-manifest.txt`. Screenshot checkpoint menunjukkan papan permainan. Manifest juga mengonfirmasi probe lama tidak memberi input controller (`PROBE_CONTROLLER_INPUT=none`).
- Artifact lama tidak berisi binary AppImage—hanya checkpoint, screenshot, log, schema, patch-diff, dan build manifest. Karena runner lama sudah dibersihkan, workflow baru akan membangun ulang PCSX-Redux dari base `0c3572c3db75f97542001e453ae80ba8c3f8acba` dengan patch dua-file SPU/ADPCM yang sama.
- Workflow [.github/workflows/naruto-storymode-control-probe.yml](.github/workflows/naruto-storymode-control-probe.yml) ditambahkan pada commit [`fde550b`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/fde550b37102d6bbf3890938cca03ce703718d38). Trigger sekali pakai dibuat lalu dihapus; file marker tidak tertinggal di repo.
- Run [#39513285641](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39513285641) sedang berjalan. Rencana probe: pada proses baru, masing-masing cabang memuat ulang checkpoint induk yang sama dan menguji satu input saja (NONE/START/CIRCLE/CROSS/TRIANGLE/SQUARE/UP/DOWN/LEFT/RIGHT), mengambil screenshot sebelum dan sesudah, lalu membandingkan hasil. Tidak ada cabang yang menimpa checkpoint induk; masing-masing memakai salinan Memory Card sementara.
- Run [#39513291249](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39513291249) berstatus `skipped` karena marker dihapus dan bukan eksperimen gameplay.
- **Belum ada input gameplay yang diterapkan sebagai progres Story Mode kanonis.** Tunggu hasil screenshot per tombol sebelum memilih tindakan berikutnya. Game belum terbukti tamat; save/load Memory Card in-game tetap belum terverifikasi. ROM, BIOS, savestate, dan Memory Card tidak dimasukkan ke Git.

---

## CATATAN OPERASIONAL TERBARU — probe SPU/ADPCM dipicu (20 Oktober 2026)

- **Run aktual:** [#39373493482](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39373493482), event `push`, commit pemicu [f1a0d7f0c2a574c07b875e38a3c6f7ffa561daa6](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/f1a0d7f0c2a574c07b875e38a3c6f7ffa561daa6). Run benar-benar terdaftar dan saat pemeriksaan statusnya `in_progress`; unduhan checkpoint dan Memory Card, validasi source/staging tanpa perubahan byte, verifikasi aset runtime, serta schema preflight sudah sukses. Step aktif adalah build emulator varian; artifact final dan hasil restore belum tersedia.
- Analisis log [run #39372712212](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39372712212): unduhan artifact checkpoint berhasil, tetapi unduhan Memory Card gagal `Unable to download artifact(s): Not Found`. Akar kesalahan: langkah Memory Card memakai `inputs.source_run_id` tanpa fallback; pada event `push` nilainya kosong, sehingga artifact dicari pada run yang salah. Tahap validasi staging, schema, build, dan loader pada run itu **tidak berjalan**. Ini bukan bukti savestate rusak.
- Perbaikan dibuat di commit [b44efaab64716db2c018212587989103c9ffa83b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/b44efaab64716db2c018212587989103c9ffa83b): kedua unduhan lintas-run menggunakan fallback source run `39262213468`. Pemicu sementara hanya mencocokkan satu path marker; setelah run #39373493482 terkonfirmasi, pemicu dibuang melalui [commit e925b438](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/e925b438b69bac29003dc73f0908bbc1dd0eae9a) dan marker dihapus lewat [commit 192bf21](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/192bf21d05d1dfc559110d66080e25940354eb29). Workflow main kini kembali hanya `workflow_dispatch` dan mempertahankan fallback fix.
- Run manual sebelumnya [#39372202653](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39372202653) adalah kegagalan terpisah: SDL tidak menemukan display pada schema preflight, sebelum loader. Perbaikan Xvfb/`XDG_RUNTIME_DIR` ada pada workflow yang kini dijalankan. Jangan gunakan rerun attempt lama sebagai pengganti run ini.
- Sumber checkpoint Story Mode tetap run `39262213468`, frame 10055, 21.163.286 byte, SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`; screenshot SHA-256 `101b94a4d171d228e0224948872b65b88bf84fd0d92dc8ddd0b6cfeb21f790a8`. Source raw tidak diubah. **Pemulihan belum terbukti** sampai seluruh gerbang restore dan reload proses baru lolos.

---

---

## PEMBARUAN TERBARU — akar crash paling mungkin ditemukan; probe terisolasi disiapkan (20 Oktober 2026)

**Diagnosis berkeyakinan tinggi, belum dikonfirmasi oleh run perbaikan:** SIGSEGV native saat memuat raw board kemungkinan berasal dari bug sentinel cursor SPU/ADPCM pada PCSX-Redux commit 0c3572c3db75f97542001e453ae80ba8c3f8acba. Upstream memperbaikinya lewat [PR #2218](https://github.com/grumpycoders/pcsx-redux/pull/2218), merged 5 Oktober 2026. Lihat [analisis akar dan rancangan probe](docs/SAVESTATE_ADPCM_SENTINEL_ROOT_CAUSE_2026-10-20.md) untuk bukti, pemetaan field, dan batas kesimpulan.

- API schema yang diminta tersedia dalam source build pinned: PCSX.getSaveStateProtoSchema() mengembalikan schema tanpa memanggil loader. Runtime invocation dari AppImage yang sama akan diuji sebelum pemuatan savestate.
- Mapping terverifikasi: top-level field 6 = spu; di dalamnya field 6 memuat 24 channel; channel.data.current = field 8. Pada raw board, 20/24 cursor berada di luar RAM suara 512 KiB, 18 di antaranya berflag stop=1. Raw boot yang berhasil juga memiliki cursor invalid tetapi channel tampak inactive. Ini mendukung hipotesis, belum menunjukkan channel spesifik penyebab crash.
- Raw source board tidak berubah: 21.163.286 byte, SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d. Probe membangun varian dari commit emulator yang sama dengan hanya patch dua file SPU dari PR #2218; hash source dan staging harus identik. Hash patch, applied diff, AppImage varian, schema, dan checkpoint berikutnya dicatat.
- Run manual pertama [#39372202653](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39372202653) berhenti pada step schema preflight sebelum API Lua terbukti terpanggil, sebelum loader, dan sebelum build varian. Penyebab yang tercatat: SDL gagal start karena tidak ada display (`Failed to initialize SDL: No available video device`), bukan bukti schema API tidak tersedia. Source/staging raw tetap identik pada ukuran 21.163.286 byte dan SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`; artifact diagnostik #12242161565 tersedia untuk pemeriksaan.
- Workflow [probe perbaikan sentinel](.github/workflows/naruto-spu-sentinel-fix-probe.yml) sudah diperbaiki di commit `b8ba2fa7586e83690c38c61ba290fcbb9c7fe836`: schema preflight sekarang menyalakan Xvfb, menetapkan `XDG_RUNTIME_DIR`, dan akan menyertakan log kegagalan pada artifact. Workflow ini perlu dijalankan ulang secara manual; jangan rerun attempt lama karena ia memakai versi workflow yang tanpa virtual display. Default source run tetap `39262213468`. Tidak ada source playthrough 90 menit atau perubahan raw state.
- Pada run berikutnya, tanpa input tombol, probe akan memulihkan board, membuat checkpoint setelah 180 VSync, lalu memuat checkpoint tersebut dalam proses emulator baru. Kedua tahap harus lolos event, loader-return, 180 VSync, dan screenshot sebelum checkpoint dinyatakan valid.
- **Status belum menjadi restore PASS.** Tunggu workflow probe aktual dan periksa semua gerbang: event load, loader kembali normal, minimal 180 VSync, screenshot cocok, serta checkpoint lanjutan valid. Story Mode belum terbukti pulih lintas-run, game belum terbukti tamat, dan aturan gameplay belum boleh disebut terverifikasi.

---

## PEMBARUAN TERBARU — perbandingan struktural raw boot vs raw board (20 Oktober 2026)

Rincian diff read-only: [docs/SAVESTATE_STRUCTURAL_COMPARISON_2026-10-20.md](docs/SAVESTATE_STRUCTURAL_COMPARISON_2026-10-20.md), diperkenalkan pada commit [dbe20783f90971f69a1abc56fb492da736882661](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/dbe20783f90971f69a1abc56fb492da736882661). Ringkasan handoff juga diperbarui pada commit [1eff1e65ad4a18ff5f33e95b941c19e06efea21d](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/1eff1e65ad4a18ff5f33e95b941c19e06efea21d).

- Pembanding raw yang terverifikasi berhasil lintas-run hanya boot [#39255438457 → #39255549341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255549341); belum ada restore tengah Story Mode yang terbukti berhasil.
- Raw boot: 21.124.144 byte, SHA-256 `a4672dd49fbfa76ef60de410c50460d77e115181fc3e205a215ab9f5f1e601d7`. Raw board frame 10055 dari [#39262213468](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468): 21.163.286 byte, SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`. Header SaveState v4 sama, tetapi raw board +39.142 byte.
- Perbedaan ukuran utama ada di top-level protobuf field `6` (+38.943 byte), dengan subfield `3`, `6`, dan `9`–`13` yang memerlukan pemetaan schema. Nama semantik field dan hubungan kausal dengan SIGSEGV **belum terverifikasi**.
- BIOS pada kedua raw state identik (512 KiB, SHA-256 `5e84a94818cf5282f4217591fefd88be36b9b174b3cc7cb0bcd75199beb450f1`). Varian tersanitasi dari artifact board (20.638.994 byte, SHA-256 `b94e61502b63a81107f48153932ccbef21bede8c7f53d4b01e6e013ecb8979eb`) menghapus hanya field BIOS di memory message; payload top-level field `6` tidak berubah.
- **Eksperimen berikutnya:** jangan ulangi receiver identik dan jangan mengubah raw source. Verifikasi dahulu apakah build PCSX-Redux yang sama menyediakan API Lua `PCSX.getSaveStateProtoSchema()`. Jika tersedia, ambil schema tanpa memanggil loader; jika tidak, cari sumber schema read-only yang cocok dengan build tersebut. Petakan field yang berubah sebelum uji faktor tunggal. Jika kelak menguji varian, simpan sebagai eksperimen tersendiri dengan parent hash, transformasi tepat, dan hash varian; hentikan setelah bukti restore dan jangan meneruskan gameplay dari varian.
- Pemeriksaan tidak mengubah file sumber atau memasukkan ROM/BIOS/savestate/Memory Card ke Git. Tidak ada Actions run aktif saat pemeriksaan. Story Mode belum terbukti dipulihkan lintas-run atau tamat; aturan gameplay belum terverifikasi.

---

## HASIL TERBARU — GDB menangkap SIGSEGV di dalam pemuatan raw savestate (20 Oktober 2026)

- **Eksperimen terbaru:** receiver [run #39314115221](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39314115221) menggunakan checkpoint dari source run #39262213468. Validasi sumber dan staging sama-sama PASS: frame 10055, reason=stable_non_dialog, ukuran 21.163.286 byte, SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`. Tidak ada modifikasi terhadap byte savestate.
- **Fase crash kini terlokalisasi:** penanda yang di-flush mencatat `LUA_SCRIPT_START`, `FIRST_GPU_VSYNC_ENTERED`, `NEXT_TICK_ENTERED`, `SAVESTATE_FILE_OPEN_OK`, lalu `PCSX_LOADSAVESTATE_BEGIN`. GDB menerima SIGSEGV pada thread `pcsx-redux` ketika `PCSX.loadSaveState()` sedang berjalan. `STORY_RESTORE_CRASH_PHASE=native_crash_during_load_call`, `STORY_GDB_SIGSEGV_CAPTURED=1`, dan 72 frame stack tercatat.
- **Konteks native:** PC `0x7ffff0fad6d0` berada di kode executable `AppDir/shared/bin/pcsx-redux`; instruksi fault adalah `movzbl (%rsi),%ecx`. Register RSI berisi `0xffffffffd736a15f`, alamat yang tidak termasuk rentang memori proses yang dipetakan. GDB tidak menemukan simbol fungsi (`No symbol matches $pc`) karena biner ter-strip. Ini membuktikan dereferensi alamat tak valid di jalur native ketika loader dipanggil; **fungsi internal yang tepat dan alasan pointer tersebut tidak valid belum diketahui**. Jangan menganggap file raw korup semata-mata dari hasil ini.
- Artefak privat #12216519993 dari run #39314115221 menyimpan `gdb-console.txt`, register/disassembly, peta memori, phase log, stdout, log emulator, dan ringkasan pembanding. Artefak menunjukkan `ExecutionFlow::SaveStateLoaded` dan `PCSX_LOADSAVESTATE_PCALL_RETURNED` tidak muncul. Screenshot pascarestore gagal karena emulator keluar lebih dahulu; tidak ada 180 VSync pascarestore atau checkpoint lanjutan.
- Run sebelumnya #39313917935 juga menangkap SIGSEGV saat `PCSX.loadSaveState()`; run #39313679196 tidak valid untuk crash analysis karena GDB mengikuti helper `mkdir` dan tidak mencapai emulator. Run #39312125361 menjadi bukti awal segfault tanpa loader marker. Run #39313409415 dan #39313520942 gagal sebelum emulator karena masalah pemicu/unduhan dan path skrip diagnostik yang kemudian diperbaiki.
- Diagnostik permanen dipertahankan pada workflow receiver: GDB dipasang, GDB mengikuti parent AppImage sampai `exec` PCSX-Redux, output fase Lua di-flush, serta register/disassembly/simbol/peta memori direkam. **Pemicu push sementara sudah dihapus**; workflow kini hanya memakai `workflow_run` dan `workflow_dispatch`. Workflow terverifikasi pada commit [68639076b5b6a971d62bd8a5a73c60a9ba406d11](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/68639076b5b6a971d62bd8a5a73c60a9ba406d11).
- **Status pemulihan tetap FAIL / belum terbukti.** Jangan lanjutkan Story Mode dari receiver atau menyatakan progres aman dipulihkan. Langkah analisis berikutnya harus memakai source artifact/checkpoint yang sama dan tidak mengubah byte; karena binary stripped, pertimbangkan pembanding kontrol raw state boot yang sudah terbukti pulih atau investigasi format/semantik state secara read-only sebelum mengubah strategi restore. Source run 90 menit tidak diulang. Game belum terbukti tamat, Memory Card save/load di dalam game belum terverifikasi, dan tidak ada ROM/BIOS/savestate/Memory Card di Git.

---

## HASIL TERBARU — raw checkpoint board-screen valid; receiver crash saat startup (20 Oktober 2026)

- Receiver [run #39312125361](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39312125361) mencapai eksperimen emulator pada runner baru. **Source artifact validation PASS**: frame 10055, reason stable_non_dialog, 21.163.286 byte, SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d. Log `STORY_RAW_STATE_STAGED_UNCHANGED=PASS` mengonfirmasi file di staging sama byte demi byte dengan sumber. Tidak ada sanitizer/BIOS rehydration.
- Langkah instal dependensi, unduh/verifikasi emulator/game/BIOS, dan staging raw state semuanya PASS. Perbaikan workspace unduhan sudah benar. `python3-pil` dipindahkan sebelum validasi karena sebelumnya validator berhenti saat `ModuleNotFoundError: No module named 'PIL'`.
- **Hasil restore: gagal / belum konklusif pada tahap native startup.** Emulator exit 139 (segmentation fault) dalam beberapa detik. `pcsx.log` mengidentifikasi BIOS retail SCPH-7502, game SLPS03553 / `SLPS_035.53;1`, lalu berhenti di `KERNEL SETUP!` dan `BIOS Trace1: 0x07`. Tidak ada `STORY_SAVESTATE_RESTORE_PAUSE_REQUESTED`, `ExecutionFlow::SaveStateLoaded`, `STORY_SAVESTATE_LOAD_CALL_RETURNED=1`, atau screenshot segera setelah restore. Karena event panggilan load tak terlihat, bukti ini **belum cukup untuk memastikan tepatnya apakah crash terjadi di loader save-state atau tahap inisialisasi tepat sebelum callback Lua/load**. Jangan menyimpulkan bahwa file sumber rusak hanya dari exit 139.
- Artifact diagnostik privat #12216866405 di run #39312125361 berisi `pcsx.stdout.txt`, `pcsx.log.txt`, important logs, screenshot checkpoint sumber, comparison summary dan manifest baru bertanda `STORY_RAW_STATE_PRESENT=0` (tidak ada checkpoint lanjutan). Ini telah diperiksa. Artifact Memory Card #12216691714 tetap hanya kandidat 131.072 byte; save/load in-game belum dibuktikan.
- Dalam proses perbaikan, receiver sebelumnya gagal dua kali karena folder download tidak cocok (run #39274593965 attempts 1–2); kemudian satu percobaan gagal karena Pillow belum dipasang pada waktu validator. Setelah dua bug itu diperbaiki, run #39312125361 benar-benar mencapai emulator dan segfault. Workflow sekarang bersih dari pemicu push sementara; perubahan permanen yang dipertahankan: unduhan ke `$WORK/source-artifact`/`$WORK/source-card` dan instal dependensi sebelum validator. Commit pembersihan pemicu: [d0b24b64fcc3c6d8d309252a53d0e291d1f2b36f](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/d0b24b64fcc3c6d8d309252a53d0e291d1f2b36f).
- **Langkah berikutnya:** tambahkan diagnostik GDB hanya pada workflow receiver agar stack trace native menangkap titik SIGSEGV; tambahkan log yang di-flush tepat sebelum/selepas permintaan load dan sebelum screenshot. Gunakan lagi source_run_id 39262213468, jangan jalankan ulang emulator sumber, jangan mengubah byte savestate. Jangan klaim pemulihan Story Mode berhasil sampai ada event load, ≥180 VSync pascarestore dan screenshot yang cocok. Game belum terbukti tamat; mekanik gameplay belum terverifikasi.

---

## PEMBARUAN TERBARU — papan permainan terlihat; restore raw lintas-run masih tertahan (20 Oktober 2026)

- **Run sumber #39262213468 selesai sukses** pada 19 Oktober 2026 15:03:41 UTC. Visual gate Mode Select lulus di frame 5999; STORY_DIALOG_VISUAL_GATE=PASS pada frame 8999. Watcher mendeteksi dialog dan meminta START; pada frame 10050 layar non-dialog stabil, lalu raw checkpoint dibuat di frame **10055**, reason=stable_non_dialog.
- Artifact privat sumber [#12196796917](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468/artifacts/12196796917) telah diunduh untuk pemeriksaan. File raw PCSX.createSaveState() **21.163.286 byte**, SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d; SHA/ukuran dicocokkan dengan isi ZIP dan manifest. Screenshot checkpoint aktual 320×240, SHA-256 101b94a4d171d228e0224948872b65b88bf84fd0d92dc8ddd0b6cfeb21f790a8.
- **Bukti visual:** screenshot frame 10055 menunjukkan papan permainan dari sudut atas, bangunan/tile bernomor, token biru-merah dan UI karakter/statistik. Artinya layar telah maju melewati narasi pembuka ke scene papan permainan. Kontrol karakter/gerakan, aturan perebutan wilayah, syarat menang-kalah, progres stage, dan tamat Story Mode **belum** terverifikasi.
- Receiver [run #39274593965](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39274593965) gagal pada attempt 1 dan attempt 2 **sebelum emulator dijalankan**: Missing raw-state manifest, exit 41. Log menunjukkan unduhan disimpan di runner.temp/naruto-storymode-raw-resume, sedangkan langkah validasi menggunakan WORK=/tmp/naruto-storymode-raw-resume. Tidak ada pemanggilan load savestate maupun bukti restore untuk checkpoint Story Mode; jangan klasifikasikan ini sebagai kegagalan savestate.
- Perbaikan workspace receiver sudah ada di commit [4b0bbe0d838e42a688e907372dcb8682fa80c967](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/4b0bbe0d838e42a688e907372dcb8682fa80c967): kedua artifact diunduh ke direktori WORK yang sama dengan langkah verifikasi. Retry run #39274593965 tetap membaca definisi workflow lama dan gagal dengan kesalahan sama; perbaikannya **belum dieksekusi**.
- **Tindakan berikutnya:** dari workflow [Naruto raw Story Mode restore and continuation](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/workflows/naruto-raw-storymode-restore.yml), jalankan **Run workflow** dari main dengan input source_run_id=39262213468. Sesudah itu, verifikasi integritas byte/hash, event ExecutionFlow::SaveStateLoaded, screenshot restore yang cocok, minimal 180 VSync pascarestore, dan checkpoint lanjutan sebelum menyatakan restore lintas-run Story Mode berhasil.
- Memory Card artifact privat [#12196517326](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468/artifacts/12196517326) berisi 131.072 byte, SHA-256 ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5. Status tetap UNVERIFIED_REQUIRES_IN_GAME_SAVE_AND_RELOAD; keberadaan file/checksum saja bukan bukti save/load dalam game.
- Jangan menaruh ROM, BIOS, save state, atau Memory Card di Git. Artifact privat tetap media transfer; game belum terbukti tamat. Dialog dilewati dengan **START**, bukan Circle. Aturan gameplay tetap diklasifikasikan **TERVERIFIKASI / HIPOTESIS / BELUM DIUJI** berdasarkan bukti langsung.

---

## SNAPSHOT LANJUTAN — raw savestate Story Mode lintas-run (19 Oktober 2026)

- **Run aktif saat snapshot dibuat:** [#39262213468](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468), commit `e396eac00631001b7a0e68d7701c70aec10dec19`. Aset emulator/game/BIOS dari release privat sudah terunduh dan terverifikasi. Emulator masih berjalan; belum ada artifact yang diunggah. Jangan membatalkan run ini atau mengubah `.github/workflows/naruto-scph7502-gpu-traffic-summary.yml` selagi run aktif karena concurrency workflow dapat membatalkannya.
- [Run #39261524544](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39261524544) gagal **sebelum eksperimen emulator** karena launcher watcher mengacu pada variabel Bash `raw_resume_verify` yang tidak tersedia (`set -u`, exit 255). Tidak ada checkpoint baru dari run tersebut; bukan bukti kegagalan raw savestate. Perbaikannya ada pada commit `e396eac...`: watcher sumber kini memakai `RAW_RESUME_VERIFY=false`.
- Perubahan workflow utama awal di commit `ded5867641f5b9614af65201f20cc152962a11b5` menaikkan batas job menjadi 100 menit dan emulator menjadi 90 menit, menyalin output mentah `PCSX.createSaveState()` tanpa mengubah byte sebelum artifact, serta menyiapkan manifest SHA-256/ukuran/frame/reason dan screenshot dari safe point yang sama. Artifact privat disetel retensi 14 hari. Salinan tersanitasi lama tetap hanya untuk diagnostik, bukan prasyarat transfer raw.
- Workflow penerima baru: [`.github/workflows/naruto-raw-storymode-restore.yml`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/.github/workflows/naruto-raw-storymode-restore.yml), terakhir diperbarui pada commit `ddcf1e0462bde04a18c65990be1bf9be2e375cbd`. Ia akan dipicu setelah workflow utama selesai dan hanya menerima artifact raw dengan manifest/screenshot cocok; checkpoint pertama harus ditandai `reason=stable_non_dialog`, frame ≥9000 dan dialog visual gate PASS. Runner penerima memverifikasi byte/hash sebelum load, tidak menggunakan sanitizer atau rehidrasi BIOS, lalu mensyaratkan event `ExecutionFlow::SaveStateLoaded`, sekurang-kurangnya 180 VSync, dan perbandingan screenshot sumber/restore PASS sebelum meneruskan permainan.
- Jika run sumber tidak membuat raw checkpoint atau tidak menghasilkan keadaan yang diidentifikasi sebagai layar stabil pascadialog, workflow penerima harus gagal-tertutup; jangan memaksanya memakai checkpoint menu/boot atau menyebutnya progres Story Mode. Push validasi berjudul `.github/workflows/naruto-raw-storymode-restore.yml` (#39262100556/#39262163072/#39262211513) bukan eksperimen emulator—event-nya `push`, bukan workflow_run, dan job eksperiment tidak berjalan.
- **Status game tidak berubah berdasarkan workflow saja:** raw lintas-run sudah terbukti pada boot awal di #39255438457 → #39255549341, tetapi restore tengah Story Mode, Memory Card save/load dalam game, dan tamat Story Mode tetap belum terbukti. Dialog dilewati dengan **START**, bukan Circle. Aturan gameplay diberi label **TERVERIFIKASI / HIPOTESIS / BELUM DIUJI**.

Pemeriksaan berikutnya: cek status #39262213468, log tahap emulator, artifact checkpoint dan manifest. Setelah ia selesai, periksa apakah workflow penerima berjalan. Jangan menandai restore berhasil sebelum screenshot dibandingkan secara aktual.

---

## HASIL BARU — raw savestate benar-benar pulih lintas-run (19 Oktober 2026)

- **TERVERIFIKASI, terbatas pada boot awal:** [Run A #39255438457](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255438457) membuat raw state melalui `PCSX.createSaveState()` pada VSync 60, tanpa sanitasi. File berukuran **21.124.144 byte**, SHA-256 `a4672dd49fbfa76ef60de410c50460d77e115181fc3e205a215ab9f5f1e601d7`. Artifact sumber privat #12187367829: [unduh dari GitHub](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255438457/artifacts/12187367829).
- **TERVERIFIKASI lintas-run:** [Run B #39255549341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255549341) berjalan sebagai workflow-run baru di runner/workspace dan proses emulator yang baru. B mengunduh artifact A, memverifikasi ukuran serta SHA-256 sama (`SOURCE_ARTIFACT_VERIFY=PASS`, `SOURCE_FILE_UNMODIFIED=1)), lalu memulihkannya.
- Bukti restore B: `ExecutionFlow::SaveStateLoaded`, `LOAD_CALL_RETURNED=1`, `ExecutionFlow::Run`, **180 VSync pascarestore**, exit 0, dan gerbang akhir PASS. Screenshot valid **640×508**, PNG 20.521 byte; SHA-256 `90aa21b6943bac231e4c0e888923a5d1e9658de28ce5c715b9328b17c046db21`. Bukti privat artifact #12187962047: [unduh dari GitHub](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255549341/artifacts/12187962047).
- Screenshot menunjukkan **logo boot Sony Computer Entertainment**; raw state dibuat di sekitar `KERNEL SETUP!`, bukan di tengah Story Mode. Jadi hasil ini membuktikan portabilitas savestate mentah lintas runner/proses **untuk state boot awal saja**.
- **BELUM TERBUKTI:** pemulihan checkpoint tengah Story Mode. Restore checkpoint lama yang disanitasi masih SIGSEGV/exit 139 pada tahap D run #39252214331. Akar penyebab sanitizer belum diketahui. Tidak ada progres Story Mode yang boleh dianggap aman; Story Mode belum dilanjutkan dan game belum terbukti tamat.
- Langkah berikutnya: gunakan raw boot state yang sudah terbukti sebagai kontrol positif, bandingkan sanitizer dengan perubahan satu faktor per eksperimen, dan jangan mengubah checkpoint lama. Setelah sanitizer dipahami, buat raw checkpoint baru saat gameplay Story Mode benar-benar aktif dan wajib buktikan restore dengan event, ≥180 VSync, serta screenshot yang cocok dengan adegan checkpoint sebelum melanjutkan permainan. Memory Card diuji sesudah restore tengah Story Mode terbukti.
- Dialog Story Mode dilewati dengan **START**, bukan Circle. Aturan gameplay tetap diberi label **TERVERIFIKASI / HIPOTESIS / BELUM DIUJI** berdasarkan bukti langsung. Pada pemeriksaan setelah run B, **tidak ada Actions runner aktif**.

---

## UPDATE TERBARU — hasil roundtrip savestate mentah (19 Oktober 2026)

- [Run #39252214331](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39252214331) telah selesai. Tahap A/B/C/C2 lulus; tahap D pada checkpoint lama yang tersanitasi tetap SIGSEGV/exit 139 segera setelah `PCSX.loadSaveState()` dipanggil.
- Tahap E membuat savestate mentah baru melalui `PCSX.createSaveState()` (21.124.150 byte); tahap F memuat file mentah tersebut di emulator yang sama. Terverifikasi: `SaveStateLoaded`, `LOAD_CALL_RETURNED=1`, event `ExecutionFlow::Run`, dan 180 VSync pascapemulihan tanpa crash.
- Artifact privat #12186545059 memiliki screenshot pascapemulihan valid 640×508; isinya layar boot/logo Sony Computer Entertainment. State itu dibuat saat boot awal di sekitar `KERNEL SETUP!`, **bukan** di tengah Story Mode.
- Kesimpulan: ada bukti bahwa roundtrip savestate mentah PCSX-Redux dapat bekerja pada GitHub Actions runner. **Belum ada bukti restore checkpoint tengah Story Mode.** Workflow keseluruhan gagal pada gerbang bukti karena tahap D (checkpoint tersanitasi) masih gagal; tahap F yang lulus tidak mengubah hasil D.
- Hambatan utama yang diketahui: jalur checkpoint tersanitasi/rehidrasi crash saat loader native berjalan, sementara savestate mentah buatan emulator sendiri dapat dimuat. Penyebab tepat transformasi atau field yang memicu crash belum diketahui; perlakukan kerusakan struktur/semantik state sebagai hipotesis, bukan fakta.
- Langkah selanjutnya: pertama, uji savestate mentah buatan emulator sebagai artifact lintas-run—buat pada run A, unggah tanpa modifikasi, lalu muat pada proses emulator bersih di run B. Ini memisahkan masalah lintas-proses dari sanitasi, yang sebelumnya berubah bersamaan. Jika raw lintas-run lulus, baru uji varian tersanitasi; jika gagal, fokus pada portabilitas/proses/build terlebih dahulu. Pertahankan checkpoint lama, jangan restart Story Mode, jangan membatalkan runner lain. Memory Card tetap prioritas sesudah restore tengah Story Mode terverifikasi. Dialog Story Mode dilewati dengan **START**, bukan Circle. Game belum terbukti tamat.
- Catatan lengkap: [docs/SAVESTATE_DIAGNOSTIC_2026-10-19.md](docs/SAVESTATE_DIAGNOSTIC_2026-10-19.md).

---

## STATUS AKTUAL — MEMORY CARD + STORY MODE (19 Oktober 2026; snapshot 18.06 WIB)

- Draft PR #1 telah di-merge ke `main` pada commit [9dc876f08d724b6f809c6da4e2dbea1b549b9d62](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/9dc876f08d724b6f809c6da4e2dbea1b549b9d62).
- Runner #39235643517 dibatalkan pada 19 Oktober 2026 pukul 17.54 WIB. Artifact-nya berisi savestate tersanitasi dan bukti screenshot/log, **tidak berisi Memory Card**. Screenshot terakhir yang diperiksa menampilkan layar Mode Select dengan Story Mode disorot; gerbang visual gagal sebelum frame 5999. Ini bukan gameplay aktif.
- Uji pertama setelah merge: [run #39242130783](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39242130783), head commit merge di atas. Pemeriksaan terakhir pukul 18.06 WIB: workflow masih `in_progress`; asset download/verifikasi lulus, langkah restore kartu dan savestate dilewati (cold boot disengaja), langkah emulator sedang berjalan, dan artifact belum tersedia. Periksa status aktual di GitHub sebelum melanjutkan jika snapshot ini sudah lewat.
- Workflow kini memasang kartu pada slot 1 dengan `-memcard1` di jalur emulator normal dan GDB, membatasi job 35 menit dan proses emulator 25 menit, mengunggah `.mcd` bersama manifest ukuran/SHA-256 sebagai artifact privat 7 hari, serta menolak pemulihan yang kehilangan kartu/manifest atau gagal validasi. Savestate tidak dimuat kecuali diminta eksplisit sebagai alat bantu.
- Run #39242130783 adalah **uji pembuatan kartu/artifact awal**, bukan uji pemulihan lintas-run karena `resume_run_id` tidak diberikan. Belum ada bukti save Story Mode di dalam game, pemulihan save pada cold boot, atau Story Mode tamat.
- Setelah run selesai, periksa status job, exit code emulator, screenshot terakhir, artefak bukti, dan isi artifact kartu/manifest. Jika kartu dan manifest valid, lakukan run terpisah via `workflow_dispatch` dengan `resume_run_id=39242130783` dan `load_savestate=false`; pastikan SHA/ukuran sama setelah restore. Jangan mulai run pemulihan bila artifact kartu tidak ada.
- Baru setelah menu save/load di dalam game ditemukan dan save yang nyata terlihat dapat dimuat kembali setelah cold boot, progres boleh ditandai aman. File `.mcd` yang ada, checksum yang cocok, atau status workflow `success` saja bukan bukti save game berhasil.
- Setiap dialog Story Mode dilewati dengan **START**, bukan Circle. Story Mode belum tamat; mekanik gameplay belum boleh diklaim terverifikasi tanpa screenshot dan eksperimen langsung. Jangan mengubah workflow saat run ini aktif karena concurrency dapat membatalkannya.

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

## STATUS TERBARU — Story Mode terverifikasi masuk ke narasi pembuka (run #39183597316, 2026-10-19)

Run [#39183597316](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39183597316) selesai dengan workflow/job `success` pada commit workflow `e9a6f985458ad2dd23c939813881918cb9a7f701`. Run lama #39178662131 tidak diulang. Artifact privat [#12158079662](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39183597316/artifacts/12158079662) telah diunduh, inventaris file diperiksa, dan screenshot aktual dilihat.

**Temuan visual yang membuktikan transisi:**
- Sequence cold boot yang terbukti diulang: Start press/release frame 2650/2680; DOWN 2710/2720; UP 2740/2750; Circle pertama 2780/2810.
- Gerbang visual `STORY_SELECT_VISUAL_GATE=PASS` pada frame 5999: crop judul Mode Select dan crop pilihan Story Mode cocok dengan fingerprint screenshot baseline yang telah diverifikasi. Karena gerbang lulus, Circle kedua benar-benar dikirim: press frame 6100 dan release frame 6130. Readback input hanya catatan pendukung, bukan dasar klaim.
- Frame 6099–6140 masih menunjukkan layar pemilihan mode dengan Story Mode tersorot dan animasi kartu. Frame 6200 dan 6399 hitam seragam; keduanya **tidak** dipakai sebagai bukti Story Mode.
- Frame 6799 menampilkan layar narasi cerita baru; layar serupa bertahan pada 7199, 7599, 7999, 8499, dan 8999. Teks terbaca: `今日は、アカデミーの卒業試験の日。` (Hari ini adalah hari ujian kelulusan Akademi.). Ini adalah bukti visual kuat bahwa konfirmasi kedua membawa game masuk ke pembukaan Story Mode, bukan hanya memilih opsinya di menu. Kesimpulan terverifikasi: **Story Mode telah dimulai sampai adegan narasi pembuka**.
- Batas kesimpulan: adegan pembuka terlihat stabil sampai frame 8999, tetapi kontrol karakter/gameplay aktif, mekanik, progres misi, dan tamat Story Mode **belum** diuji.

**Status acceptance RT-001:**
1. Title screen dan Start membuka menu — **PASS secara visual**.
2. DOWN/UP mengubah pilihan menu serta Circle pertama mencapai Mode Select — **PASS secara visual**.
3. Circle kedua setelah gerbang visual frame 5999; narasi pembuka Story Mode tampil pada frame 6799–8999 — **PASS secara visual**.
4. Kontrol karakter/gameplay aktif dan mekanik — **PENDING**.
5. Menyelesaikan/tamat Story Mode — **PENDING**.

**Konfigurasi:** log runtime mencatat BIOS SCPH-7502 (EU), CD ID `SLPS03553`, executable `SLPS_035.53;1`, dan Port 1 connected Analog/Auto. Workflow tetap mematok PCSX-Redux source `0c3572c3db75f97542001e453ae80ba8c3f8acba` dan flag `-softgpu`; konfigurasi wajib lainnya tidak diubah.

**Cleanup dan isi artifact:** log menyatakan `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`, GPU dump ter-parse lengkap (`GPU_DUMP_TRUNCATED=false`), dan workspace runtime dihapus. ZIP 7.6 MB berisi ringkasan/log, RSP summary, gerbang visual dan screenshot PNG checkpoint yang memang diperlukan sebagai bukti; tidak ditemukan file ROM, BIOS, save, raw GPU/VRAM dump, atau file mentah ber-ekstensi terkait di artifact.

**Langkah eksperimen berikutnya:** lakukan cold boot baru dan ulangi urutan lengkap sampai Story Mode. Tunggu layar pembuka tampak; screenshot menunjukkan ikon Circle di kanan bawah kotak narasi. Uji hanya satu tap Circle terkontrol (press/release terpisah) untuk mencoba melanjutkan dialog, capture tepat sebelum/sesudah, dan amati apakah adegan berikutnya/gameplay muncul. Jangan kirim input beruntun dan jangan menandai kontrol gameplay lulus sebelum ada bukti visual/gerakan karakter yang aktual.


---

## Hasil terverifikasi terbaru — D-pad berpindah; Circle mencapai Mode Select (2026-10-19)

Run [#39178662131](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39178662131) selesai dengan workflow success dan observasi mencapai VSync 6.000. Kesimpulan di bawah berasal dari screenshot aktual pada artifact privat [#12155879252](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39178662131/artifacts/12155879252), bukan dari status workflow.

- Frame 2.649–2.650: layar judul dengan prompt Start. Frame 2.670: menu memuat `はじめから` (baris pertama) dan `ロード` (baris kedua), panah awal pada `はじめから`.
- DOWN ditekan pada frame 2.710 dan dilepas 2.720. Screenshot 2.710 masih menampilkan baris pertama, tetapi pada frame 2.720 panah jelas menunjuk `ロード`: navigasi turun berhasil.
- UP ditekan pada frame 2.740 dan dilepas 2.750. Screenshot 2.740 masih menunjukkan baris kedua, sedangkan frame 2.749–2.750 memperlihatkan panah kembali ke `はじめから`: navigasi naik berhasil.
- Circle ditekan pada frame 2.780 dan dilepas 2.810. Frame 2.780 masih memperlihatkan menu; frame 2.790 overlay menu mulai menghilang, frame 2.800 overlay hilang, frame 2.900 gambar menggelap, dan frame 2.950/2.999/3.199 hitam. **Layar hitam tidak dipakai sebagai bukti mode apa pun.** Bukti visual langsung muncul pada frame 3.399: judul `モードセレクト` (“Mode Select”) terbaca, dengan `ストーリーモード` (“Story Mode”) sedang disorot/terpilih. Layar itu tetap terlihat pada checkpoint 3.599 sampai 5.999.
- Hasil visual rangkaian Start → DOWN → UP → Circle konsisten dengan konfirmasi `はじめから` dan transisi ke Mode Select. Story Mode baru **terpilih**, belum dikonfirmasi/dimasuki; gameplay dan tamat belum terbukti. `PAD_INJECT ... PASS` hanya bukti readback API, bukan bukti respons game.
- Baseline dipertahankan: BIOS retail SCPH-7502 (EU), disc `SLPS03553`, executable `SLPS_035.53;1`, PCSX-Redux pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`, SoftGPU, Port 1 Analog/Auto.
- Cleanup log mengonfirmasi `RAW_GPU_DUMP_REMOVED=1` dan `RAW_TEMP_SCREENSHOTS_REMOVED=1`; langkah `rm -rf "$WORK"` selesai. ZIP artifact berisi ringkasan/log teks dan screenshot PNG pilihan, tanpa ROM, BIOS, save, atau raw GPU/VRAM dump. Retensi artifact sampai sekitar 2026-10-22 00:43 UTC.

**Status RT-001:** title screen PASS; Start membuka menu PASS; DOWN menuju `ロード` PASS; UP kembali ke `はじめから` PASS; Circle membawa ke layar Mode Select PASS secara visual; Story Mode dimulai PENDING; gameplay/mekanik dan tamat PENDING.

**Langkah berikutnya:** eksperimen baru melakukan cold boot, ulangi Start 2.650–2.680 → DOWN 2.710–2.720 → UP 2.740–2.750 → Circle pada menu 2.780–2.810. Pertahankan observasi hingga Mode Select terlihat dan stabil (bukti sebelumnya dari frame 3.399 sampai 5.999). Setelah layar itu teridentifikasi, gunakan Circle kedua untuk mengonfirmasi Story Mode—misalnya press 6.100/release 6.130, dengan screenshot sebelum dan sesudah—dan perluas observasi hingga setidaknya frame 9.000. Jangan menyatakan Story Mode sudah dimulai sampai screenshot pasca-konfirmasi menunjukkan transisi nyata ke Story Mode/gameplay; jangan menyimpulkan dari layar hitam atau workflow success.

---

## Hasil terbaru — Start saja membuka menu dan menu bertahan sampai VSync 3000 (2026-10-19)

- Run [#39176328030](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39176328030) selesai `success` pada commit workflow `69ab7544ef7aaea40dc8af4ab12132e9997b3575`. Input sequence hanya Start press frame 2.650 dan release frame 2.680; tidak ada injeksi Circle atau tombol lain.
- Screenshot framebuffer 640×480 yang diperiksa langsung: frame 2.650 masih menampilkan judul Naruto dan prompt Start; frame 2.670 menunjukkan menu dengan panah di `はじめから` dan pilihan kedua `ロード`; frame 2.999 masih menampilkan menu yang sama. Ini kembali mengonfirmasi Start membuka menu, dan menu tetap stabil selama observasi.
- Log `PAD_INJECT` menunjukkan Start press/release terbaca oleh API, sedangkan bukti transisi game ialah perubahan visual pada screenshot sesudah Start. Artifact privat [#12155370415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39176328030/artifacts/12155370415), retensi 3 hari; raw GPU dump/temp screenshot telah dihapus dan aset runtime dibersihkan.
- Sesuai instruksi pengguna, tidak menekan Circle saat layar judul. Eksperimen ini sengaja berhenti pada menu; `はじめから` belum dikonfirmasi dan Mode Select/Story Mode belum terbukti. Langkah lanjut untuk masuk ke opsi tersebut memerlukan aksi konfirmasi terpisah setelah layar menu dikenali.

## Instruksi terbaru — gunakan Start saja, tanpa Circle (2026-10-19)

- Pengguna mengarahkan bahwa layar yang ingin diuji adalah judul Naruto dengan prompt Start dan input yang dipakai harus **Start, bukan Circle**.
- Run #39149443247 mengirim Start pada 2.650–2.680 lalu Circle pada 2.750–2.780; sesudah Circle, menu menghilang/fade lalu framebuffer hitam pada 2.900–2.999 (320×240, satu warna). Tidak ada tulisan Mode Select yang dapat dibaca, jadi tidak boleh disebut Story Mode atau Mode Select.
- Workflow berikutnya dikoreksi menjadi Start saja: tekan Start pada frame 2.650, release 2.680, tanpa Circle atau tombol lain. Checkpoint sekitar 2.649–2.800 dipakai untuk memastikan transisi dari prompt ke menu, lalu amati sampai VSync 3.000.
- Start→menu sebelumnya sudah pernah terlihat pada #39145309203; eksperimen Start-only ini mengikuti instruksi pengguna dan memastikan layar dibiarkan di menu tanpa mengonfirmasi pilihan.
- RT-001: layar judul terkonfirmasi; Start membuka menu terverifikasi pada run terdahulu; pemilihan `はじめから`, Mode Select, Story Mode, gameplay, dan tamat belum terbukti. Artifact harus tetap berisi screenshot/summary minimum; raw dump dan aset privat dihapus sebelum upload.

## Terbaru — Circle saja tidak mengonfirmasi menu karena run dimulai ulang (2026-10-18)

- Run [#39147391100](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39147391100) selesai `success` dan mencapai 3.000 VSync pada commit `5f89389d3af1f3f6254057ae8b0162667bd5eaf0`. Runtime tetap memakai retail BIOS SCPH-7502 (EU), disc `SLPS03553`, executable `SLPS_035.53;1`, PCSX-Redux pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`, SoftGPU, dan Port 1 Analog/Auto.
- Koreksi penting: setiap GitHub Actions run melakukan boot bersih. Run #39147391100 hanya mengirim Circle pada frame 2.750–2.780 dan **tidak** mengulangi Start. Screenshot frame 2.749–2.800 serta checkpoint sampai 2.999 tetap menampilkan ilustrasi title screen; prompt Start berkedip, tetapi tidak terlihat transisi ke menu atau Mode Select.
- `PAD_INJECT frame=2750 button=CIRCLE ... status=PASS` hanya membuktikan readback API emulator. Karena tombol dikirim saat title screen, ini bukan pengujian konfirmasi `はじめから`; pilihan menu tidak pernah dibuka pada run itu.
- Artifact privat [#12144726606](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39147391100/artifacts/12144726606) memuat bukti visual dan ringkasan saja. `RAW_GPU_DUMP_REMOVED=1`, `RAW_TEMP_SCREENSHOTS_REMOVED=1`, dan aset runtime dibersihkan dari runner.
- Status RT-001: Start membuka menu pada run #39145309203 tetap **terverifikasi**. Memilih mulai dari awal, Mode Select, Story Mode, kontrol gameplay, dan tamat masih **belum terverifikasi**. #39147391100 tidak membantah hasil Start sebelumnya; sesi ini tidak pernah mengirim Start.
- Eksperimen berikutnya wajib mengirim Start lalu Circle pada satu boot yang sama: Start press frame 2.650/release 2.680, Circle press 2.750/release 2.780, tanpa tombol lain; capture dekat kedua input dan amati sampai VSync 3.000.

## Terbaru — Start membuka menu utama; はじめから terpilih (2026-10-18)

- Run [#39145309203](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39145309203) selesai dengan workflow `success`; commit eksperimen `43bab6c337693eff87d5fa996d450299adc31093`. Emulator mencapai target 3.000 VSync dengan BIOS retail SCPH-7502 (EU), disc `SLPS03553`, executable `SLPS_035.53;1`, source PCSX-Redux pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`, SoftGPU, dan Port 1 Analog / Auto. Konfigurasi lain dipertahankan.
- Bukti framebuffer 640×480 aktual: frame 2.649 dan 2.650 masih menunjukkan title prompt; frame 2.660 mulai memperlihatkan kotak transisi; frame 2.670 sudah menampilkan menu dengan panah di `はじめから` dan pilihan kedua `ロード`. Menu tetap terlihat pada 2.680, 2.700, 2.750, 2.800, 2.900, 2.950, dan 2.999.
- Start ditekan frame 2.650 dan dilepas frame 2.680. Readback API lulus, tetapi bukti game memprosesnya adalah perubahan visual sesudah input: prompt title berganti menjadi menu. Circle tidak dikirim dalam run ini.
- Screenshot aktual menu hanya menunjukkan dua pilihan yang terbaca: `はじめから` dan `ロード`. Jangan menganggap `コンティニュー` tersedia pada layar ini hanya karena disebut referensi luar.
- Artifact privat [#12143433923](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39145309203/artifacts/12143433923) berisi ringkasan dan screenshot pilihan; retensi 3 hari. Log menyatakan `RAW_GPU_DUMP_REMOVED=1` dan `RAW_TEMP_SCREENSHOTS_REMOVED=1`; ROM/BIOS/raw dump tidak diunggah.
- **Kemajuan RT-001:** tujuan 1, Start membuka menu, sekarang **terverifikasi**. Tujuan 2–6 masih belum terbukti: memilih mulai dari awal, memasuki mode/story, respons gameplay yang terukur, mekanik, dan menamatkan Story Mode.
- **Langkah berikut:** pertahankan runtime yang sama. Karena panah jelas berada di `はじめから`, kirim hanya Circle/O pada frame 2.750 dan lepas pada 2.780. Ambil checkpoint rapat sebelum/sesudahnya dan amati sampai VSync 3.000. Jika mode select muncul, baca pilihan aktual dari screenshot dan jangan menekan tombol lagi sebelum layar tersebut teridentifikasi.

## Terbaru — layar judul Naruto terkonfirmasi (2026-10-18)

- Run [#39122631591](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39122631591) selesai dengan pipeline success dan menghentikan emulator sesuai target VSync 3.000. BIOS retail SCPH-7502 (EU), disc SLPS03553, dan executable SLPS_035.53;1 terdeteksi. Konfigurasi controller yang tercatat: connected=true, device_type=Analog, input_type=Auto.
- Bukti visual privat: frame 2.399 = latar berpola/copyright; frame 2.499 = ilustrasi karakter/copyright; frame 2.599 = layar judul Naruto dengan logo dan prompt Jepang STARTボタンをおせってはよ! (meminta pemain menekan Start). Prompt terlihat pada frame 2.699, 2.799, dan 2.899; pada frame 2.999 prompt tidak tampak, mungkin karena berkedip, tetapi ilustrasi judul masih sama dan belum ada menu pilihan.
- Start pada run ini dikirim pada frame 2.500, sedikit sebelum prompt judul terlihat di checkpoint 2.599. Circle/O ditekan pada frame 2.700, 2.850, 2.950, padahal prompt meminta Start. Karena itu, menu belum terbukti terbuka. Log PAD_INJECT status=PASS hanya membuktikan override API emulator terbaca kembali, bukan bahwa game memproses tombol.
- Langkah berikut: ulangi dengan BIOS/ROM/emulator/pad yang sama, tetapi kirim Start sesudah prompt title-screen muncul—misalnya frame 2.650—dan ambil checkpoint visual sering sesudahnya. Jika menu dengan はじめから (From the beginning), ロード (Load), dan コンティニュー (Continue) tampak, tekan Circle/O untuk memilih はじめから. Identifikasi mode-select sebelum mencoba masuk Story Mode.
- Status: title screen tercapai; start menu, mode select, dan Story Mode belum terbukti; Story Mode belum tamat. Raw ROM/BIOS/dump tidak diunggah; raw dump dibersihkan sebelum upload ringkasan dan checkpoint privat berumur singkat.

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

## Hasil RSP memory-window control-flow summary — 2026-10-18 (Actions #39080987461)

Run [#39080987461](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39080987461) menyelesaikan target VSync 300 dan semua cleanup dengan conclusion workflow `success`; emulator exit code 0. RSP tersambung (`qSupported=ok`) dan mengumpulkan 75 sampel bulk register valid sampai sekitar t=98.62s. Marker yang dibaca dari `pcsx.log`: SYSTEM.CNF ~4.66s, BOOT path ~5.95s, EXEC header dan `Execute !` ~36.75s. PC kembali dominan di BIOS setelah ~t=40s sampai ~t=87.73s, lalu muncul lagi di executable mulai ~t=89.01s.

Pembacaan empat jendela memori 64-byte di alamat executable berhasil, tetapi artifact hanya berisi kategori/count; tidak ada instruksi mentah, operand, atau dump memori:
- `0x80050b00`: 0 conditional branch, 0 jump, 2 load, 6 store, 4 immediate arithmetic, 4 special arithmetic.
- `0x8003c080`: 2 conditional branch (keduanya forward), 4 jump, 1 load, 5 immediate arithmetic, 4 special arithmetic.
- `0x80037300`: 1 conditional branch dengan satu backward-branch pada jendela 64-byte, 3 jump, 2 load, 4 immediate arithmetic, 6 special arithmetic.
- `0x800372c0`: 2 conditional branch (keduanya forward), 1 jump, 3 load, 2 store, 3 immediate arithmetic, 5 special arithmetic.
Tidak ditemukan kategori syscall/break/COP0/COP2 dalam keempat jendela ini. Ini statistik isi jendela statis, bukan bukti bahwa branch tertentu pasti dieksekusi. Namun PC runtime mengulang `0x80037320` dan `0x800372d8` di akhir pengamatan, sehingga area `0x800372c0–0x8003733f` layak untuk sampling PC yang lebih rapat.

GPUDump tetap lengkap (299 VSync live packets, 43 GP0 words; semua GP0 hanya pada bin VSync 200–299: 39 GPU-state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP; tidak ada primitive triangle/quad/line/textured sprite). Screenshot Software GPU 320×240 dan capture window X11 1280×800 tetap hitam. Dump mentah dihapus; artifact privat hanya ringkasan/log.

Langkah selanjutnya: ubah sampler RSP agar mengurangi interval jeda hanya ketika PC berada di `0x800372c0–0x800373ff` (tetap simpan hanya PC/CP0 dan histogram kategori) untuk menguji apakah PC mengulang pola yang konsisten; jangan menambah trace instruksi mentah. **RT-001 tetap Open / blocked**.
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
## Hasil korelasi CPU/GP0 dengan marker bertimestamp — 2026-10-18 (Actions #39079981314)

Run [#39079981314](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079981314) selesai dengan conclusion `success`; emulator mencapai target VSync 300 lalu dihentikan normal oleh probe (`EMULATOR_EXIT_CODE=0`). Aset privat serta hash BIOS/ROM/AnyLinux diverifikasi. Tidak ada raw GPUDump atau instruksi/operand mentah di artifact.

**GPUDump setelah TraceBegin:** 299 VSync packets / 598 words; GP0 8 packets / 43 words; GP1 11 packets / 16 words; ThrowAway 5 packets / 5 words; truncated=false. Pretrace GP0 baseline 262153 words adalah reset + VRAM upload untuk state awal dump, bukan rendering game. Parser sementara mengonsumsi semua 43 live GP0 words tanpa sisa dan mengklasifikasikannya sebagai 42 perintah: GPU-state-setting=39, clear-cache=1, monochrome-rectangle=1, NOP=1. Tidak ada keluarga triangle, quad, line, atau textured sprite pada jendela sampai VSync 300. Ini berarti ada sedikit traffic grafis, tetapi belum ada gambar yang terlihat; screenshot Software GPU 320×240 dan screenshot jendela X11 1280×800 tetap hitam pada run sebelumnya.

**Korelasi CPU:** RSP tersambung; `qSupported` berhasil; 76 paket bulk register valid sebelum target berhenti. Marker log yang kini ditimestamp dari `pcsx.log`: SYSTEM.CNF sekitar t=4.85s, BOOT path t=6.14s, EXEC header dan `Execute !` sekitar t=38.01s. Sampel PC segera sesudahnya masuk ke executable utama (t=38.33s `0x8003717c`, t=39.62s `0x8003c0b4`, t=40.91s `0x80037320`), lalu kembali ke BIOS range mulai sekitar t=42.20s. Sampel berada di BIOS sampai sekitar t=87.09s dan masuk lagi ke executable pada t=88.39s (`0x800372d8`), dengan beberapa sampel lanjutan di `0x80037320/0x800372d8` hingga t=98.63s. CP0 Status umumnya `0x40000401`, BadVAddr nol, Cause umumnya `0x400`; dua sampel Cause `0x20` tidak cukup untuk menyimpulkan root cause tanpa sampling lebih rapat. Timestamp dari `pcsx.log` dipilih karena stdout buffered; jangan gunakan timestamp marker lama dari stdout sebagai korelasi akurat.

Interpretasi: host Mesa/GLX sehat; guest CPU masuk ke executable sebentar-sebentar tetapi pada jendela sekitar 100 detik hanya mengirim 43 GP0 words (kebanyakan state command, satu monochrome rectangle), dan tidak menampilkan title/menu. Ini lebih konsisten dengan masalah inisialisasi/looping guest daripada kebutuhan GPU fisik, tetapi akar sebab belum dipastikan. Probe berikutnya akan mengelompokkan waktu GP0 command berdasarkan VSync range agar terlihat apakah semuanya hanya terjadi saat startup.

**RT-001 tetap Open / blocked.** Belum ada title/menu yang dikenali, perubahan state dari input yang diverifikasi, atau Story Mode.
## Hasil final GPUDump sampai timeout dan probe korelasi CPU berikutnya — 2026-10-18

Run [#39079291837](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079291837) selesai dengan conclusion Actions `success` (semua langkah/cleanup berhasil), tetapi proses emulator berakhir pada batas observasi 90 detik (`EMULATOR_EXIT_CODE=124`); jangan mengartikan status workflow sebagai game sukses boot. Log mencapai `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, `EXEC:PC0(80011448)` dan `Execute !`. GPU traffic dump ter-parse lengkap, `GPU_DUMP_TRUNCATED=false`, satu marker `TraceBegin`, dan 268 VSync packets / 536 live words. Sesudah TraceBegin: **GP0 packets=0, words=0; GP1 packets=1, words=1; VSync packets=268**. Baseline pre-trace GP0 262153 words berisi reset dan full 1024×512 VRAM upload untuk merekonstruksi keadaan awal dump, bukan gambar yang dikirim game. Dump mentah dihapus sebelum upload artifact, yang hanya menyimpan ringkasan teks/log. Emulator timeout 124 adalah batas observasi, bukan crash diagnosis.

Untuk menghubungkan hasil grafis dengan CPU, workflow [`naruto-fastboot-gpu-traffic-summary.yml`](.github/workflows/naruto-fastboot-gpu-traffic-summary.yml) kini diperbarui agar satu run men-sample bulk RSP register `g` (PC + CP0 Status/BadVAddr/Cause) dengan timestamp relatif dan marker loader sambil merekam GPUDump, tanpa instruksi/operand mentah. Commit terbaru [`30cd69d6`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/30cd69d61a5ab01761baa7f3a209a386f205b650); run konfirmasi [#39079600379](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079600379) terakhir terlihat pending di antrean ketika entri ini dibuat. Periksa log/run selesai sebelum menafsirkan sampel itu.

Kesimpulan tetap terbatas: host GLX/Mesa sehat; jendela emulator dan screenshot software GPU hitam; tak ada GP0 drawing command yang terekam pada 268 VSync pasca-TraceBegin. Ini menunjuk ke inisialisasi/eksekusi game tamu, tetapi tidak menentukan akar sebab. **RT-001 tetap Open / blocked.**
## Pembuktian GL host dan traffic GPU tamu — 2026-10-18

- Run OpenGL mandiri [#39049689832](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39049689832): Mesa `llvmpipe (LLVM 21.1.8, 256 bits)`, OpenGL 4.5 Core/Compatibility Profile, tanpa version override; konteks Compatibility 3.3 berhasil dibuat. Host GLX/Mesa sehat, dan belum ada alasan teknis untuk menuntut GPU fisik.
- Source build pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`: `GPU::takeScreenShot()` bawaan melempar `Not yet implemented`; backend OpenGL GPU tidak mengimplementasikannya, sedangkan Software GPU punya implementasi screenshot. Run [#39078905140](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078905140) dengan `-softgpu` menghasilkan screenshot frame 300 valid 320×240 tetapi seluruh piksel hitam; VRAM 1024×512 juga satu warna hitam.
- Run window capture [#39079066598](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079066598) mengambil enam screenshot jendela PCSX-Redux non-root XID `0x200034` pada t=5,15,30,45,60,75 detik. Semuanya valid 1280×800 namun seragam hitam. Tidak ada title/menu.
- GPUDump summary parsial dari run [#39079279565](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079279565) (run berhenti/cancel saat workflow diperbarui) berhasil mem-parse dump sampai 136 live VSyncs tanpa truncation. Sesudah TraceBegin: `GP0 packets=0, words=0`, `GP1 packets=1, words=1`, `VSync packets=136, words=272`. Baseline pre-trace berisi 262153 GP0 words karena reset/full VRAM upload untuk merekonstruksi state dump; angka itu bukan trafik gambar game. Raw GPU dump dihapus; artifact privat hanya summary/log.
- Run konfirmasi dengan workflow saat ini [#39079291837](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079291837) sedang merekam sampai target VSync 300 saat catatan dibuat; periksa hasil finalnya sebelum menyatakan hasil penuh.

Interpretasi sementara: masalah yang terlihat tidak lagi cocok dengan kegagalan pembuatan konteks OpenGL host. Data mengarah bahwa executable tamu mencapai marker `Execute !`, tetapi belum mengeluarkan perintah gambar GP0 selama jendela yang direkam. Ini belum mengidentifikasi penyebab di CPU/game loader. RT-001 tetap **Open / blocked**: title/menu dan respons input belum terbukti; Story Mode belum dimulai.
## Lanjutan diagnosis VRAM dan callback UI — 2026-10-18

Run [#39050174557](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39050174557) memakai timer rekursif melalui `PCSX.nextTick()`, tetapi tidak menghasilkan checkpoint (`NO_VALID_TIMED_CAPTURES`). Audit source pada pin `0c3572c3db75f97542001e453ae80ba8c3f8acba` menjelaskan kelemahan harness: `PCSX.nextTick()` menyimpan callback di `AfterPollingCleanup`; pada `src/core/ui.cc`, `UI::tick()` menjalankan callback tersebut lalu membersihkan field yang sama. Penjadwalan ulang dari callback itu dapat tertimpa. Kegagalan ini adalah kegagalan metode sampling, bukan bukti kegagalan OpenGL.

Run [#39078592809](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078592809) mengambil sembilan sampel VRAM langsung saat `GPU::Vsync`: frame 1, 2, 3, 5, 10, 20, 30, 45, dan 60. Semua buffer berukuran 1.048.576 byte, hanya memiliki satu warna 15-bit, rasio non-black 0, dan hash PNG yang identik. Guest FPS bernilai 0 pada checkpoint itu. Namun, semua snapshot tersebut berada sebelum marker log `Execute !`; run kemudian mencatat `GPU::Vsync frame=300 guest_fps=1.0000` setelah handoff. Karena itu, sampel hitam tersebut hanya membuktikan VRAM awal yang kosong sebelum executable berjalan, bukan keadaan pasca-handoff. Run berakhir pada timeout 90 detik (124), lalu menghapus buffer mentah; artifact privat hanya berisi PNG/summary.

Capture langsung dari event GPU bukan pola yang akan diteruskan karena API readback OpenGL perlu dijalankan pada thread UI/konteks grafis yang benar. Workflow telah diubah lagi pada commit [`3a69fcef`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/3a69fcef242563ecf45de8c920bec3443db3e956) untuk menjadwalkan capture dari event ke thread UI melalui `PCSX.nextTick()`, tanpa timer rekursif. Run [#39078732160](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078732160) menguji versi deferred itu pada frame 1 dan 60; status terakhir yang diperiksa: masih berjalan, belum ada hasil yang boleh disimpulkan.

**RT-001 tetap Open / blocked.** Belum ada title/menu yang dikenali dan belum ada perubahan state akibat input yang terverifikasi. Perlu capture pasca-handoff (target VSync sekitar 300, sebagaimana marker runtime) sebelum mengubah hipotesis gameplay/rendering.
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

## Koreksi validitas RSP GPU-watchpoint dan rerun — 2026-10-17

Audit run [#39017636267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017636267) menemukan hasil “entry breakpoint” dan “GPU GP0 watchpoint hit” **tidak valid sebagai hit yang terkonfirmasi**: klien RSP menganggap paket konsol PCSX-Redux berawalan `O` (mis. teks `PCSX::MIPS>`) sebagai stop event. Pada run itu, PC yang dibaca setelah event tetap berada di BIOS (`0xbfc0867c` dan `0xbfc05784`), bukan di entry executable Naruto. Karena itu entry breakpoint belum terbukti tercapai dan GP0 belum boleh dinyatakan terpicu. Watchpoint GP1/DMA2 juga hanya timeout dalam uji terdahulu. Workflow berakhir `success` hanya berarti harness dan cleanup selesai; bukan hasil positif target.

Workflow diperbaiki pada commit `5055074671acf8cb2f2512182f8484dc2815552d`: parser kini mempertahankan buffer lintas paket, mengabaikan paket console `O` saat menunggu stop, serta hanya menerima jawaban stop RSP `T/S/W/X`. Sesudah entry stop, ia memeriksa PC harus tepat `0x80011448` sebelum menghapus breakpoint dan mencoba GP0/GP1/DMA2. Run [#39020901596](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39020901596) kini selesai `success` pada tingkat workflow, tetapi **tidak mencapai entry executable dalam batas 20 detik**: tidak ada stop event breakpoint dan setelah Ctrl-C PC masih `0xbfc03bdc` di BIOS. Log mengenali `SYSTEM.CNF` dan `BOOT = cdrom:\\SLPS_035.53;1`, tetapi tidak mencapai `EXEC:PC0`/`Execute !`. Ini bukan bukti hit GPU; watchpoints tidak diuji karena probe berhenti pada kegagalan entry. Run tersebut juga berbeda dari baseline karena belum menerapkan setup Port 1 Analog yang ada pada run sebelumnya. Commit `a8d8db8a0c3b84967a14c3a0905e046dbed24cf9` kini menerapkan Port 1 Analog + remap yang sama dan memperpanjang masa menunggu entry menjadi 40 detik; run baru [#39021127913](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39021127913) baru dimulai. Baca PC dan log final sebelum hipotesis lanjut.

Layar game belum berubah dari hitam dalam bukti visual sebelumnya; title/menu serta respons input belum terbukti. **RT-001 tetap Open / blocked; Story Mode belum dimulai/tamat.**

## Hasil RSP minimal dan eksperimen GPU-watchpoint — 2026-10-17

Run [#39017271906](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017271906) selesai dengan conclusion Actions `success` dan cleanup berhasil. Klien RSP minimal terhubung ke PCSX-Redux AnyLinux pada port 3333, negosiasi `qSupported` berhasil, dan 10 sampel register PC/CP0 berhasil dibaca tanpa GDB modern yang mengirim command tak didukung. Sampel PC meliputi `0x8003C0A0` dan `0x80037320`, yang berada dalam rentang EXE utama berdasarkan header/load range `0x80010000` dengan text size `0x5D800`; sampel lain juga meliputi alamat BIOS. `BadVAddr=0` konsisten di seluruh sampel dan `Cause=0x400`; jangan tafsirkan nilai ini sebagai diagnosis exception final. Status target RSP `S00` menunjukkan target sedang running saat diperiksa. Karena sampel jarang dan bercampur alamat BIOS/EXE, ini bukan bukti cukup bahwa inisialisasi game selesai.

Jendela non-root PCSX `0x200034` (1280×800) masih uniform black (mean 0, standard deviation 0, satu warna) pada capture sebelum input, setelah Return/Cross, dan sekitar 40/65/90 detik; OCR kosong. Loader tetap mencatat `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, `EXEC:PC0(80011448)`, `Execute !`. Dengan demikian pembacaan register kini bekerja, tetapi title/menu dan respons input masih belum terbukti. Artifact diagnostik privat `12095198494` retensi 3 hari; tidak ada dump memori atau instruksi mentah di artifact.

Eksperimen pembeda berikutnya saat catatan ini diperbarui: workflow [#39017636267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39017636267) memasang breakpoint entry `0x80011448` saat emulasi masih paused, lalu memantau write-watchpoint pada register GPU GP0/GP1 dan DMA2 melalui klien RSP minimal. **Run ini masih berlangsung saat catatan ini dibuat; jangan menyimpulkan hasil watchpoint sampai log selesai diperiksa.**

**RT-001 tetap Open / blocked.** Story Mode belum dimulai/tamat; jangan menetapkan aturan gameplay runtime sebelum title/menu dan input terverifikasi.

# Status penelitian

## Keputusan emulator utama dan hasil GDB terbaru — 2026-10-17

**Emulator utama yang dipilih untuk penelitian lanjut: PCSX-Redux AnyLinux prebuilt + OpenBIOS fastboot (`openbios.bin`, SHA-256 `25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d`).** Ini keputusan operasional berdasarkan jalur terjauh yang terkonfirmasi di log: membaca `SYSTEM.CNF`, `BOOT = cdrom:\\SLPS_035.53;1`, lalu `EXEC:PC0(80011448)` dan `Execute !`. Varian chunked belum mencapai marker entry dalam rentang uji yang sama; DuckStation terblokir oleh wizard yang tidak menerima OpenBIOS sebagai BIOS PS1/PS2 valid. Keputusan ini tidak menyatakan game sudah boot ke title/menu.
Run terakhir [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234) selesai sukses secara workflow, tetapi GDB remote gagal menghasilkan snapshot PC pada t20/t30/t50/t70 (exit 1) dan t90 timeout (exit 124). Jendela PCSX non-root XID `0x200034`/2097204 tetap valid dan frame pre-input, frame 30/50/70s, sesudah Return dan Cross semuanya hitam uniform (1280×800, mean 0, stddev 0, satu warna); OCR kosong. Log fastboot tetap mencatat entry handoff. Cleanup runner sukses, artifact privat #12095276220.
**RT-001 tetap Open / blocked** sampai title/menu Naruto dikenali dan respons input yang mengubah kondisi game terbukti. Story Mode belum dimulai/tamat.


## Diagnostik pasca-entry berikutnya sedang berjalan — 2026-10-17

Karena fastboot GUI tetap hitam baik dengan "-softgpu" maupun backend OpenGL default (Mesa llvmpipe 3.3), workflow privat [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234) telah dimulai. Tes ini mempertahankan fastboot BIOS, ROM dan controller yang sama, lalu mengambil snapshot PC melalui GDB remote eksternal pada beberapa waktu; tidak memakai pembacaan register CPU dalam callback VSync dan tidak mencetak instruksi/operand mentah. Status ketika terakhir diperiksa: masih memasang tool GDB; belum ada snapshot atau hasil boot baru. RT-001 tetap Open / blocked.


## Hasil A/B backend GPU — 2026-10-17

Run [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) menguji fastboot OpenBIOS yang sama pada PCSX-Redux AnyLinux tanpa `-softgpu`, memakai backend OpenGL default melalui Mesa llvmpipe. Kapabilitas GL terkonfirmasi: vendor Mesa, renderer `llvmpipe (LLVM 21.1.8, 256 bits)`, OpenGL 3.3 Compatibility Profile. Capture berasal dari jendela PCSX non-root `0x200034` / XID 2097204, 1280×800. Seluruh frame sebelum input, setelah Return/Cross, dan pada 40/65/90 detik tetap uniform black (mean 0, stddev 0, satu warna); OCR kosong. Tidak ada callback pembaca register CPU. Log fastboot tetap mencapai SYSTEM.CNF/BOOT, `EXEC:PC0(80011448)`, `Execute !`. Jadi backend OpenGL default pun belum membuat title/menu terlihat.
- Artifact privat `12094736241`, cleanup berhasil.
- Hipotesis berikut yang paling informatif adalah mengambil snapshot PC CPU dari luar emulator melalui GDB remote (bukan Lua/VSync callback), untuk membedakan loop pasca-entry dari masalah rendering tanpa mencetak trace instruksi mentah.
**RT-001 tetap Open / blocked.** Story Mode belum dimulai; belum ada aturan gameplay runtime yang terverifikasi.


## Hasil capture fastboot yang sah — 2026-10-17

Run [#39015722771](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015722771) kini menghasilkan capture valid jendela aplikasi PCSX-Redux, XID 2097204 (`0x200034`), 1280×800. Selector membaca `xwininfo -root -tree`, mengecualikan root 543/`0x21f`, dan memakai non-root window bernama `PCSX-Redux`. Lima capture (sebelum input, sesudah Return/Cross, 40/65/90 detik) semuanya uniform black (mean 0, stddev 0, satu warna); OCR kosong. Ini bukan lagi masalah salah mengambil root. Port 1 Analog tetap dikonfigurasi dan input telah dikirim ke jendela aplikasi, tetapi tidak ada perubahan visual/game yang bisa diverifikasi. Tidak ada pembacaan register CPU di callback VSync. Log fastboot mencapai `SYSTEM.CNF`, `BOOT`, `EXEC:PC0(80011448)`, `Execute !`.
Run berikut [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) mengganti satu variabel grafis: menghapus `-softgpu`, mengaktifkan Mesa llvmpipe/OpenGL 3.3, dan mencatat kapabilitas GL. Status saat dicatat: in progress.
**RT-001 tetap Open / blocked** sampai title/menu dikenali dan input nyata menghasilkan perubahan game.


## Koreksi pemilihan window X11 — fastboot probe terbaru, 2026-10-17

Run [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649) benar-benar mengecualikan root, tetapi pencarian kandidatnya masih memakai `xdotool search`; hasilnya tidak mengembalikan aplikasi. Potongan `xwininfo -root -tree` di log menunjukkan child window nyata `0x200034 "PCSX-Redux"`, 1280×800. Jadi kesimpulan yang benar: window ada tetapi selector gagal memilihnya; tidak ada gambar emulator yang diambil. Marker fastboot dari log tetap mencapai `SYSTEM.CNF`, `BOOT`, `EXEC:PC0(80011448)`, `Execute !`.
Workflow diperbarui pada commit `1acd87e9960c0caeb334cffc48ed8aea212212e1` agar mengekstrak XID langsung dari tree, mengecualikan root, dan memakai `windowfocus` sebelum input. Rerun [#39015610296](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015610296) telah dipicu; status awal queued.
**Belum ada capture GUI fastboot yang sah dan belum terbukti title/menu. RT-001 tetap Open / blocked.**


## Koreksi validitas capture fastboot — 2026-10-17

Audit log run [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) menemukan bahwa ID window `543` sama dengan root Xvfb `0x21f`. Selector `xdotool search --onlyvisible --name '.*'` ternyata memasukkan root, sehingga semua metrik hitam dan OCR kosong dari run ini **bukan** capture jendela emulator dan harus ditarik dari bukti visual. Marker boot tetap sah: fastboot BIOS mencapai `SYSTEM.CNF`, BOOT, `EXEC:PC0(80011448)`, dan `Execute !`.
Run [#39015290594](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015290594) menggunakan selector sama dan juga tidak boleh dianggap sebagai capture game bila memilih root; ia sedang digantikan oleh run [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649). Workflow telah diperbaiki pada commit `83173bb10cfbf905a296f59720c0a63c95bc3a32` untuk mengecualikan root ID secara eksplisit sebelum memilih jendela non-root yang layak. Verifikasi hasil run baru dari `X11_ROOT_ID`, `WINDOW_CANDIDATE_SKIPPED=root`, dan `CAPTURE_WINDOW` non-root sebelum menilai gambar.
**RT-001 tetap Open / blocked.** Sampai capture non-root yang sah menunjukkan Naruto dan kontrol merespons, tidak ada bukti title/menu/gameplay.


## Hasil fastboot GUI dengan window discovery generik — 2026-10-17

Run [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) berhasil mengidentifikasi jendela X11 (ID `543`, 1280×800); jadi tangkapan sebelumnya yang gagal mencari nama jendela adalah masalah selector, bukan bukti tidak ada window. Namun semua frame sebelum input, sesudah Return, sesudah Z/Cross, serta 40/65/90 s tetap uniform black (mean 0, stddev 0, satu warna), OCR kosong. Log fastboot kembali mencapai `SYSTEM.CNF`, `BOOT`, `EXEC:PC0(80011448)`, dan `Execute !`. Input memang dikirim ke jendela aplikasi, tetapi karena layar tetap hitam, belum bisa ditafsirkan sebagai kontrol game.
Uji berikut [#39015290594](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015290594) mengulangi fastboot yang sama tanpa pembacaan register CPU di event VSync, karena instrumentasi tersebut pernah mengganggu eksekusi di eksperimen terdahulu. Status saat dibuat: queued. **RT-001 tetap Open / blocked.**


## Hasil eksperimen terbaru — 2026-10-17

### Source-current PCSX-Redux
Run [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) selesai dengan semua langkah workflow `success`: source PCSX-Redux pin `1525a93676dbece9fe70f10ff129aeaa14eec30d` berhasil dibangun, tetapi jendela emulator yang benar-benar ditangkap pada detik 20/40/60/80/95 seluruhnya uniform black (1280×800, mean 0, stddev 0, satu warna), OCR kosong. Log mengenali disc `SLPS-03553` dan OpenBIOS, mencatat Port 1 Analog tersambung, tetapi hanya sampel PC frame 300=`0x000015a4`; tidak ada pembacaan `SYSTEM.CNF`/BOOT atau entry executable. Artifact privat `12094116949` berisi 5 frame hitam dan stdout. Cleanup sukses. Keberhasilan build dan Actions tidak berarti game boot.
### OpenBIOS fastboot vs chunked
Run [#39013612865](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39013612865) menguji build AnyLinux sama dengan dua BIOS. Varian fastboot membaca `SYSTEM.CNF`, `BOOT`, lalu mencatat `EXEC:PC0(80011448)` / `Execute !`. Varian chunked hanya menunjukkan pembacaan payload satu sektor sampai indeks 40 sebelum log berhenti. Namun window detector lama tidak menemukan jendela untuk kedua varian, jadi tidak ada capture visual dan urutan input dilewati. Hasil ini mengisolasi beda jalur loader, bukan bukti title/menu.
### Eksperimen berikutnya
Workflow privat baru [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) memakai fastboot OpenBIOS dan enumerasi generik jendela X11, bukan hanya mencari caption “PCSX”. Status awal: queued; periksa hasil aktualnya.
**RT-001 tetap Open / blocked:** title/menu Naruto dan input game yang responsif belum terbukti. Story Mode belum dimulai/tamat.


## Hasil final DuckStation probe — 2026-10-17

- Run [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) berhasil membuka jendela setelah paket `libegl1` ditambahkan. Capture 760×498 konsisten menampilkan first-run setup wizard DuckStation, termasuk halaman BIOS.
- Layar BIOS secara eksplisit menyatakan DuckStation membutuhkan BIOS PS1/PS2; UI mendeteksi satu berkas BIOS tetapi tetap menyatakan tidak ada BIOS yang dapat dipakai. Log hanya menunjukkan BIOS dipetakan dan pencarian Auto BIOS; tidak ada marker disc/executable Naruto. Return bergerak di wizard; Z/Cross tidak terbukti mencapai game. Ini bukan tes kompatibilitas ROM yang tuntas.
- Artifact privat `12094155047` berisi 8 screenshot dan stdout. Ditinjau lokal untuk membedakan wizard BIOS dari layar game; salinan ZIP/gambar lokal sementara kemudian dibersihkan. Cleanup workspace runner sukses.
- **Tidak meminta atau mengunduh BIOS retail baru.** Dalam batas hanya memakai OpenBIOS yang sudah tersedia, DuckStation saat ini terblokir pada validasi BIOS; emulator ini tidak dinilai sebagai gagal kompatibilitas Naruto.
- PCSX-Redux source-current [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih membangun source ketika terakhir diperiksa; itu jalur prioritas selanjutnya.
- **RT-001 tetap Open / blocked.** Belum ada title/menu Naruto terverifikasi dan belum ada input game terverifikasi.


## Pembaruan status terbaru — 2026-10-17, hasil DuckStation setelah perbaikan GL

- Rerun [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) juga menyelesaikan workflow `success`, tetapi DuckStation keluar dengan kode 127 sebelum membuat jendela: `libEGL.so.1: cannot open shared object file`. Tidak ada frame, OCR, input, atau bukti boot BIOS/disc. Artifact 292 byte tidak berisi PNG.
- Workflow diperbarui lagi pada commit `5afd32eca0d32ee191de7f2963f74b53aed89448` dengan paket `libegl1`. Rerun [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) sedang berada pada langkah boot/capture ketika terakhir diperiksa.
- PCSX-Redux source-current [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih membangun source; belum ada frame yang dapat dinilai.
- **RT-001 tetap Open / blocked.** Belum ada title/menu Naruto dan respons input yang terverifikasi.


## Verifikasi terbaru — 2026-10-17, DuckStation probe dan source-current GUI

- Run privat [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) berakhir dengan conclusion Actions `success`, tetapi **DuckStation tidak diluncurkan**: log aktual menunjukkan `AppRun: error while loading shared libraries: libOpenGL.so.0: cannot open shared object file`. Tidak ada jendela DuckStation, frame/OCR game, input terkirim, atau bukti BIOS/disc dari proses emulator. Artifact ZIP (ID `12093451882`, 293 byte) hanya berisi `duckstation.stdout` sepanjang 183 byte; tidak ada PNG.
- Harness telah diperbaiki pada commit `058aadea1c664712b62a63cf01fcb3e5598ef047`: pasang paket `libopengl0 libglx0 libgl1` dan unggah `captures/*.png` (sebelumnya glob `frame-*.png` tidak cocok dengan nama file capture). Rerun aktual [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) telah dimulai; periksa hasil finalnya.
- Source-current PCSX-Redux [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih pada tahap build source saat diperiksa. Belum ada frame GUI atau OCR yang bisa dinilai.
- Cleanup private workspace pada DuckStation run awal berhasil. Tidak ada bukti title/menu atau input gameplay.
- **RT-001 tetap Open / blocked** sampai title/menu Naruto dikenali secara visual dan respons input terkontrol dibuktikan.


## Uji emulator alternatif tambahan — 2026-10-17

Workflow privat [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) kini menguji rilis DuckStation resmi, dengan AppImage SHA-256 `c5e6f045f6a242082fcafa9f02d56ad895e233b942728788d232ad0c0c765c24`, ROM yang sama dan OpenBIOS `openbios.bin` dari private release. Harness Xvfb mengambil frame jendela dan mengirim Return/Cross lewat pemetaan keyboard sementara, lalu menyimpan capture sebagai artifact privat 3 hari dan menghapus workspace. Status saat catatan ini dibuat: queued; belum ada hasil boot/menu/input yang bisa disimpulkan. Ini uji kandidat, bukan klaim kompatibilitas.

## Pembaruan runtime terbaru — 2026-10-17

- GUI baseline AnyLinux tetap belum membuktikan title/menu: jendela ada tetapi hitam, log GUI belum menyelesaikan pemuatan executable; jalur headless pada build tersebut mencapai 187 chunk dan `EXEC:PC0(80011448)`.
- Run privat [#39011515345](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011515345) mengonfirmasi screenshot Lua pada mode `-no-ui` mengembalikan ukuran 0×0; proses mencapai handoff executable tetapi capture tidak valid dan postprocess gagal. Cleanup berhasil, artefak gambar tidak tersedia.
- Tes source GUI baru [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) memakai source PCSX-Redux pin `1525a93676dbece9fe70f10ff129aeaa14eec30d` (HEAD upstream yang diverifikasi pada saat workflow dibuat), sedang berjalan saat catatan ini ditulis. Source pin CPU-trace sebelumnya 24 commit di belakang.
- Workflow retensi [#39011611436](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39011611436) sukses menghapus run publik lama `#39001985849` secara spesifik. Fetch API untuk run itu sesudah penghapusan mengembalikan 404.
- **RT-001 tetap Open / blocked.** Tidak ada bukti visual title/menu Naruto, input terkontrol, atau gameplay Story Mode. Jangan mengklaim Story Mode dimulai atau tamat.

Terakhir dirangkum: 2026-10-17

## Ringkasan

**Status: analisis statis awal dengan jejak konfigurasi target Chakra yang lebih kuat; belum lengkap dan belum tervalidasi melalui debugging gameplay.**

**Sumber wajib:** kuota internet pengguna sangat terbatas. Jangan meminta upload ROM/ISO sekitar 300 MB dan jangan mengandalkan ROM laptop. Gunakan file hasil ekstraksi di Library pada /Naruto Research Files/. Jika tidak dapat diakses, laporkan kendala alih-alih meminta upload ulang.

Pemeriksaan sebelumnya mengekstrak struktur ISO dari dump PS1 raw-sector, membaca SYSTEM.CNF, mengidentifikasi executable utama, melakukan inspeksi/disassembly awal MIPS, dan menemukan beberapa struktur serta jalur kode. Namun, pemetaan overlay belum lengkap, rumus gameplay belum seluruhnya terhubung ke semua pemanggil, dan sesi emulator/debugger terkontrol belum dijalankan.

## Temuan yang didukung langsung oleh kode/data ROM

1. Executable boot yang dirujuk SYSTEM.CNF adalah SLPS_035.53.
2. Header executable mencatat alamat muat 0x80010000, PC 0x80011448, dan text size 0x5D800.
3. Struktur pemain yang diakses beberapa getter/setter memiliki empat slot; stride struktur 0xB4 byte dan nilai Chakra pada offset +0x18.
4. Setter Chakra yang diperiksa membatasi nilai tersimpan pada rentang -9.999 sampai 99.999. Ini bukan kondisi menang/kalah.
5. Jalur kode membandingkan Chakra pemain dengan target konfigurasi dari getter 0x80012A70; jika kondisi target terkait (bit 0x200) aktif, Chakra yang mencapai/melewati target dapat menetapkan pemain sebagai pemenang. Tabel konfigurasi utama memuat pasangan awal/target 1.500/3.000, 2.000/4.000, 2.500/5.000, 3.000/6.000 serta dua record awal 600/0 yang kondisi pemilihannya belum dipetakan. Jadi 3.000 bukan target universal.
6. Data petak diperlakukan sebagai bitfield; jalur yang diperiksa memakai empat bit teratas sebagai ID pemilik. Arti seluruh bit lainnya belum terpetakan.
7. Kode memeriksa sejumlah flag kondisi akhir, tetapi label yang sesuai dengan semua pilihan menu belum terpetakan secara lengkap.

Alamat dan penjelasan lebih detail ada di docs/ROM_STRUCTURE.md, docs/OVERLAY_MAP.md, dan docs/GAME_RULES.md.

## Temuan dari UI terjemahan/panduan eksternal — bukan bukti formula universal

- Story stage 1 diterjemahkan sebagai Naruto melawan Mizuki dengan target 3.000 Chakra.
- Dalam contoh tampilan, biaya membangun barrier ditampilkan 60 Chakra; suatu contoh barrier level 1 menampilkan nilai 100 dan durability 2/2; suatu contoh peningkatan level 1 ke 2 menampilkan biaya 150.
- Sumber lain menampilkan barrier level 1 bernilai 50, sehingga nilai tidak boleh dianggap tetap tanpa memahami parameter/tipe barrier dan konteksnya.
- Beberapa deskripsi kartu memberi contoh penambahan Chakra, peningkatan statistik, atau manipulasi roulette.

Contoh UI di atas belum membuktikan bahwa 60 dan 150 adalah biaya universal atau bahwa formula seluruh barrier sudah diketahui.

## Pekerjaan terbuka utama

- Petakan loader, offset file, alamat muat, ukuran, entry point, dan lifecycle untuk seluruh overlay.
- Lanjutkan reverse-engineering format resource yang kini terindeks melalui direktori di DATA.BIN; format PK02/BIN0/TPK0, NARUTOSceneV001, PSQ0/PSQ1, serta tujuan penuh XASECT.BIN masih belum diketahui.
- Temukan dan dokumentasikan sumber setiap harga barrier, biaya upgrade, pendapatan, nilai, level, dan durability.
- Petakan seluruh bitfield petak dan struktur barrier berdasarkan pembacaan serta penulisan field.
- Identifikasi jalur transaksi Chakra untuk bangun/upgrade/pendapatan/serangan/kartu dan efek pembatas nilainya.
- Hubungkan setiap flag kondisi menang ke record skenario, pilihan menu, dan tampilan teks.
- Telusuri algoritma roulette dan efek semua kartu sampai ke pemanggil sebenarnya.
- Jalankan skenario terkontrol di emulator/debugger dan bandingkan perubahan memori dengan analisis statis.

## Batas lingkungan saat ini

Pada pemeriksaan sebelumnya, tidak ditemukan emulator PS1 yang tersedia di lingkungan analisis; percobaan eksekusi terminal/Python berikutnya juga gagal karena lingkungan menolak eksekusi. Karena itu belum ada log eksekusi gameplay dari sesi kita. Laporan GameGear Archive bahwa ROM boot di test rig Mednafen adalah sumber eksternal dan bukan pengujian khusus biaya atau rumus permainan.

## Status confidence

- **Tinggi untuk metadata disc/EXE**: didukung header, SYSTEM.CNF, ukuran, hash, dan pencocokan CRC eksternal.
- **Tinggi untuk batas setter Chakra**: instruksi setter terlihat dan rentang penjepitan nilai telah diidentifikasi.
- **Menengah untuk cabang target skenario awal**: nilai target dari record konfigurasi dan jalur perbandingan ditemukan; pemetaan lengkap semua skenario tetap terbuka.
- **Rendah/belum pasti untuk biaya dan formula gameplay**: belum ada call chain lengkap ditambah tes runtime terkontrol.

## Pembaruan hasil pemeriksaan lokal — 2026-10-15

Pemeriksaan byte-level terhadap salinan kerja ROM mengonfirmasi temuan baru berikut. Hasil ini **statis**; belum ada tes gameplay terinstrumentasi.

- SHA-256 ROM cocok dengan catatan yang sudah ada: `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`.
- Di executable utama, offset file `0x46098` (alamat runtime `0x80055898`) berisi pasangan little-endian `0xD4, 0x2F44`: LBN 212 dan panjang 12.100 byte, yang menunjuk ke awal `DATA.BIN`.
- Awal `DATA.BIN` terdiri dari bootstrap sepanjang `0x44) byte diikuti direktori `0x2F00) byte: 1.504 entri × 8 byte, paling kuat ditafsirkan sebagai pasangan `(LBN, byte_length)`.
- 1.500 entri tidak kosong dan 4 kosong (indeks 1491–1494). Semua interval sektor entri aktif berada dalam rentang `DATA.BIN` dan tidak tumpang-tindih; direktori mencakup 32.227 dari 32.234 sektor file.
- Klasifikasi signature awal atas 1.500 resource aktif: 921 `PK02`, 246 struktur TIM valid, 126 `NARUTOSceneV001`, 125 signature lain berawalan `NARU`, 6 `PSQ0`, 2 `PSQ1`, 1 `TXT2`, dan 73 belum diklasifikasikan. Pemindaian longgar mendeteksi 264 kandidat magic TIM; 18 gagal validasi struktur dan tidak dihitung sebagai TIM valid.
- `XASECT.BIN` berisi hitungan 86 diikuti 86 pasangan 32-bit. Konsumen di sekitar `0x80019468` mengindeks pasangan dengan `input >> 4) dan memakai field pertama sebagai offset aditif. Arti semantik lengkap field dan kaitan field kedua dengan stream/media masih belum pasti.

Lihat [docs/RESOURCE_CATALOG.md](docs/RESOURCE_CATALOG.md) untuk hitungan, batas inferensi, hash file hasil ekstraksi, serta langkah analisis berikutnya. Handoff lintas-chat ada di [HANDOFF_LANJUT.md](HANDOFF_LANJUT.md).


## Persistensi file untuk analisis lintas chat

File ekstraksi disimpan di Library ChatGPT pada folder `Naruto Research Files`; `DATA2.BIN` tersedia sebagai ZIP terkompresi. Baca tabel lokasi pada `HANDOFF_LANJUT.md` dan verifikasi hash sesudah pemulihan sebelum melanjutkan analisis.


## Pembaruan analisis aturan gameplay — 2026-10-15

- Tabel konfigurasi executable 0x80057798 ber-stride 0x54; tabel kedua 0x80064918 ber-stride 0x30. Field +0x04 dipakai sebagai Chakra awal, field +0x08 sebagai target pada cabang kemenangan, sementara makna field +0x0C belum ditemukan.
- Nilai teramati pada tabel pertama mencakup 1500/3000, 2000/4000, 2500/5000, 3000/6000; ada dua record 600/0 yang tidak boleh ditafsirkan sebagai kemenangan instan.
- Label lama 0x800EC200 sebagai pembanding target Chakra dan 0x800F70D0 sebagai aritmetika Chakra dicabut karena base/identitas modul belum diverifikasi.
- File Library yang digunakan pada sesi ini: SLPS_035.53, DATA.BIN, XASECT.BIN, DATA2.BIN hasil unzip. Hash DATA2.BIN hasil unzip cocok: be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9.
- Belum ada tes runtime. Prioritas berikutnya: transaksi biaya bangun/upgrade, income, perubahan kepemilikan dan transaksi battle melalui pemanggil setter Chakra dan label event ESTATE/LVUP_ESTATE.


## Trace aturan Chakra — tambahan 2026-10-15

- Kode pembanding target di resource gameplay (base hipotesis 0x800D0000) memastikan syarat cabang target adalah Chakra saat ini >= target konfigurasi bila bit kondisi 0x200 aktif. Target dibaca lewat getter 0x80012A70. Alamat resource masih statis sementara karena loader belum diverifikasi runtime.
- Pemanggilan setter Chakra 0x8001387C banyak berupa sinkronisasi salinan record. State machine sementara pada resource DATA.BIN membentuk +0xB40 dari +0xB30 + +0xB38, lalu pada state +0xB2A == 7 memproses jumlah pending +0xB44 bertahap ke Chakra pemain +0xB2B. Sumber operand dan semantik event belum ditemukan; ini bukan bukti biaya barrier.
- Karena sumber nilai transaksi belum terhubung, biaya build/upgrade universal masih belum terbukti. Angka 60 dan 150 hanya tercatat pada contoh UI tertentu dalam transkripsi komunitas.


## Status emulator/runtime — 2026-10-15

- Emulator/debugger kini ditetapkan sebagai jalur riset utama untuk memvalidasi aturan, bersama reverse-engineering statis; bukan sekadar alternatif opsional.
- Diprioritaskan PCSX-Redux karena dokumentasi resminya mendukung CPU debugger, breakpoint dan GDB server; Mednafen dapat digunakan untuk cek silang. Rujukan dan protokol uji ada di [docs/EMULATOR_WORKFLOW.md](docs/EMULATOR_WORKFLOW.md).
- Pada awal sesi executable emulator tidak tersedia dan DNS container gagal. PCSX-Redux kemudian diunduh dari GitHub Actions artifact/release, diverifikasi, dan antarmukanya berhasil dijalankan lewat Xvfb. Namun, belum ada bukti bahwa game mencapai menu/title atau bahwa gameplay sudah diuji.
- ROM di Library berhasil dimaterialisasikan dan SHA-256 cocok; tidak dibutuhkan upload ulang dari laptop pengguna.


## Emulator tersimpan di repo — 2026-10-15

- PCSX-Redux Linux x86_64 AppImage diunggah sebagai Release asset di [research-emulator-pcsx-redux-2026-10-15](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15), bukan Git history. Ukuran 65.747.557 byte; SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c. GitHub Actions run 38692549397 sukses mendownload dan memverifikasi binary.
- AppImage dapat diluncurkan di Xvfb, tetapi layar menunjukkan “No BIOS loaded, emulation halted”; belum ada boot game ataupun uji gameplay.
- Workflow build OpenBIOS open-source ada di .github/workflows/build-openbios.yml. Run #38693358323 membangun varian shell/menu dan run #38693918169 membangun shell/menu plus `BOOT_MODE=fast`. Hash fastboot `openbios.bin`: 25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d; hash ELF: 2c8d36e2179841935a1d1331777380502cdb22528d086c99c6388cdcfa54b8aa. Uji lokal fastboot menghasilkan layar hitam dan belum membuktikan Naruto mencapai title/menu. OpenBIOS bukan BIOS retail Sony.
- Jangan meminta upload ulang ROM. ROM hash diverifikasi dari Library; CUE dibuat untuk BIN raw-sector MODE2/2352.


## Update OpenBIOS — 2026-10-15

- Run [#38693358323](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693358323) berhasil membangun OpenBIOS dari source upstream PCSX-Redux pada commit 0c3572c3db75f97542001e453ae80ba8c3f8acba dan melampirkan asset ke release.
- Varian OpenBIOS default: `openbios.bin` 524.288 byte, SHA-256 `713ea2aed58606282b3ff5e91d77f8c5892ea36f5adcd279d2c7dd26604a625d`; ELF debug `openbios.elf` SHA-256 `d0d4cc73c9546e1e6af86d38ec894f5a6c81090ccdf97b1a3a39885c56af7bfc`. Checksum lengkap di release asset `OPENBIOS-SHA256SUMS`.
- Uji lokal dengan BIOS ini tidak lagi menampilkan pesan “No BIOS loaded”, tetapi frame yang terekam berupa bentuk geometris/gelap tanpa menu atau title game yang dapat dikonfirmasi. Ini belum membuktikan boot Naruto.
- [Run #38693918169](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693918169) sedang membangun varian `BOOT_MODE=fast` yang melewati shell BIOS dan mencoba boot CD secara langsung, bersama varian shell/menu normal. Periksa hasil workflow dan hash sebelum menggunakan asset tersebut.


## Hasil varian OpenBIOS fastboot — 2026-10-15

- Run [#38693918169](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693918169) sukses membangun dua variant dan mengunggahnya ke release. Varian `openbios.bin` memakai `BOOT_MODE=fast` untuk mencoba boot CD langsung; varian shell/menu tersedia sebagai `openbios-shell.bin`.
- SHA-256 fastboot `openbios.bin`: `25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d`; `openbios.elf`: `2c8d36e2179841935a1d1331777380502cdb22528d086c99c6388cdcfa54b8aa`. Asset release dan `OPENBIOS-SHA256SUMS` tersedia pada [research kit release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15).
- Uji lokal varian fastboot: PCSX-Redux dijalankan dengan OpenBIOS, interpreter, debugger, dan CUE ROM. Layar tetap hitam setelah sekitar 12 detik; log tidak menyatakan BIOS hilang tetapi tidak ada title/menu yang dapat dikonfirmasi. Status: **boot game belum terverifikasi**, bukan test runtime berhasil.
- Workflow diperbarui agar artifact runtime-kit menyertakan shell/default dan fastboot sekaligus, bukan checksum yang merujuk file yang tak ada. Run terbaru akibat perbaikan ini harus diperiksa.

## Status runtime terbaru — 2026-10-16

Game masih belum terkonfirmasi mencapai title/menu; belum ada tes gameplay runtime yang selesai. PCSX-Redux dan varian OpenBIOS diagnostik tersedia pada [release research kit](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15).

- Jalur disc normal: mengenali label `SLPS-03553`, membuka `SYSTEM.CNF;1`, menguraikan `BOOT = cdrom:\\SLPS_035.53;1`, lalu berhenti di `boot file ...` sebelum `EXEC:PC0(80011448)`.
- Main executable: 385.024 byte; payload 382.976 byte (`0x5D800`, 187 sektor setelah header 2.048 byte).
- Chunk 8 sektor berhenti pada log sebelum syscall pertama selesai (`bytes=16384`); chunk 1 sektor berhasil menunjukkan progres pembacaan 2.048 byte, tetapi uji singkat belum membuktikan seluruh payload selesai atau game tampil. Build/asset varian satu sektor sukses melalui [Actions #38697240018](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38697240018).
- Injeksi executable diagnostik mencapai `EXEC:PC0(80011448)`, `Execute !`, dan `CD_init`; layar tetap hitam. Periksa cache (`flushCache`) dan urutan init CD-ROM jika mengulangi jalur ini. Rutin init kartu memori (`buInit`) juga tampak menunggu status yang tidak berubah; bypass sementara belum membuktikan boot sukses.
- Log menunjukkan perintah kontroler `0x43` (Set Config Mode) berulang. Source PCSX-Redux memproses perintah DualShock tersebut hanya pada tipe pad Analog; tipe Digital mencatat `Unknown command for pad: 43`. Ini petunjuk yang belum diuji, bukan akar masalah yang terbukti. Referensi: https://github.com/grumpycoders/pcsx-redux/blob/db9bc8af44e3c77424127b573c17f9583ee2ab95/src/core/pad.cc. Eksperimen berikutnya: ubah Port 1 ke Analog/DualShock lalu ulangi boot.
- File baru dari pengguna `PCSX-Redux-9c6f98a0-linux-x86_64.zip` (90.912.361 byte) belum dapat dievaluasi atau dijalankan karena lingkungan shell/file tool tidak merespons. Periksa lagi sebelum memutuskan apakah build itu menggantikan AppImage release.
- Jangan meminta upload ulang ROM dan jangan mengunggah ROM/EXE, retail BIOS, save state, atau dump memori ke GitHub.


## Percobaan runtime setelah pemulihan ZIP Library — 2026-10-16

ZIP alternatif, ROM BIN, dan CUE berhasil dimaterialisasi lewat Files ke lokasi kerja. Namun `container.exec` bahkan gagal pada `echo runtime-check`, dan tool Python juga mengembalikan `ClientError`. ZIP belum bisa diinspeksi/diekstrak dan PCSX-Redux belum dijalankan dalam percobaan ini. Ini kendala lingkungan eksekusi, bukan bukti ZIP rusak atau gagal menjalankan game. Status boot tetap belum terverifikasi; setelah runtime pulih, uji integritas ZIP, versi/dependensi executable, lalu boot dengan OpenBIOS dan controller Port 1 Analog/DualShock. Kriteria sukses tetap title/menu Naruto terlihat serta input merespons.

## OpenBIOS source-level CD-read stall hypothesis — 2026-10-16

- Static inspection of the OpenBIOS source used by the research AppImage narrowed the normal boot stall to the EXE payload read path. loadExe() reads the 2,048-byte PS-X EXE header and then submits the full 382,976-byte payload (187 sectors) through one syscall_read call. The underlying CD file driver requires 0x800-aligned size/offset and waits for the CD read-completion event.
- The helper's wait for the completion event has no overall timeout. A missing/stuck completion event can block the BIOS indefinitely. This fits the prior stall evidence but is not a proven root cause.
- The uploaded filename PCSX-Redux-9c6f98a0-linux-x86_64.zip points to upstream commit 9c6f98a0ed0581635f9123147e382c248e0f5ddc (2026-09-28); the research AppImage is pinned to 0c3572c3db75f97542001e453ae80ba8c3f8acba (2026-10-01). The ZIP's contents/hash are not yet verified; treat this as filename-based provenance only.
- Next runtime test: use the existing AppImage/known OpenBIOS chunked build, CUE path, -run -interpreter -debugger -stdout -lua_stdout -logfile ..., and a fresh settings directory. Set Port 1 DeviceType=1 (Analog/DualShock) separately from PadType=2 (keyboard as host input) and Connected=true. Repeat the same boot attempt; compare pad 0x43 logs, CD read progress, entry-PC log, title/menu, and input response without changing other variables.
- Current session: the Library service successfully materialized the ROM, CUE, main EXE, DATA2 archive, and alternate emulator ZIP to reported working paths, but shell/Python calls returned ClientError. No new emulator run occurred. Never claim boot/gameplay success without runtime evidence.


## PCSX-Redux ZIP extraction record — 2026-10-16

- Extracted `PCSX-Redux-HEAD-x86_64.AppImage` from the Library ZIP (the ZIP passed `unzip -t` and had exactly one member).
- AppImage size: 91,474,424 bytes; SHA-256 `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`. The Library copy was materialized back and SHA-256 matched the extracted copy.
- Embedded version is `9c6f98a0`, build ID 335, changeset `9c6f98a0ed0581635f9123147e382c248e0f5ddc`, dated 2026-09-28 19:56:29 UTC.
- The source ZIP was replaced in Library by its one extracted AppImage because of the Library storage limit. Extraction manifest is saved at `/Naruto Research Files/PCSX-Redux-EXTRACTION-MANIFEST.md`.
- Runtime is blocked on this host: bundled emulator binary requires GLIBC_2.42/2.43, host has glibc 2.41; mounting the AppImage additionally reports missing FUSE/fusermount. Do not treat this as proof of a corrupted archive or ROM.
- The extracted AppImage is retained in Library; repository stores its provenance/hash/compatibility record in `docs/PCSX_REDUX_PACKAGE.md`. It was not inserted into Git history because the available GitHub connector does not expose binary release-asset upload. The repository's existing 65,747,557-byte AppImage release asset is a distinct build with its own hash.
- No ROM, game EXE, assets, BIOS retail, save state, or RAM dump was uploaded. This extraction did not demonstrate game boot or Story Mode.


## Preferred build for GLIBC 2.41 host — 2026-10-16

- Selected the existing research-release AppImage `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage` as the best candidate for glibc 2.41. Size 65,747,557 bytes; SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`.
- Public package description says AnyLinux packaging uses sharun, bundles dependencies, supports old/musl Linux distributions, and does not require FUSE. Upstream packaging action run 36872881656 succeeded on 2026-10-01; x86_64 log says `quick-sharun --simple-test`: “Test went OK.”
- This supersedes the 91 MB `9c6f98a0` Library build as the preferred candidate. That build's inner binary requires GLIBC_2.42/2.43 but the host is glibc 2.41.
- Critical limit: CI simple-test and GUI launch under Xvfb do not prove the Naruto ROM boots or runs smoothly. A fresh end-to-end game test could not run because container/Python execution tools returned ServerError in this turn. No claim of game boot or Story Mode success.
- Detailed provenance and next steps: `docs/PCSX_REDUX_PACKAGE.md`.


## Current Library package — AnyLinux artifact ZIP (2026-10-16)

- The current Library file is `/Naruto Research Files/PCSX-Redux-0c3572c3d-anylinux-x86_64-artifact.zip`, downloaded from Actions artifact ID `11170447493`; Actions-reported ZIP digest `f6c27070b565cbc0554f1093c1374a16aee2b8635c72ef7b141f9ff7bd857ed0`.
- Preferred binary inside: `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage`, 65,747,557 bytes; SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`.
- The previous 91 MB `9c6f98a0` AppImage and its stale extraction manifest were replaced/removed in Library. Their hashes and incompatibility history are preserved in `docs/PCSX_REDUX_PACKAGE.md`.
- The AnyLinux package's CI smoke test passed but does not load Naruto. Full game boot/controls/stability are unverified because this session's local container/Python tools return ServerError.


## Pembaruan eksperimen controller — 2026-10-17

- Hasil baseline A/B dari runner [Actions #38971848277](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38971848277): AnyLinux dan upstream HEAD sama-sama mencapai `EXEC:PC0` dan sama-sama mencatat `Unknown command for pad: 43`; keduanya masih belum membuktikan title/menu atau input yang berfungsi.
- Runner workflow diperbarui pada commit [0439c1b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/0439c1bbf51d3c1be234150d6bee80c5b812ff1e) agar menyetel Port 1 sebagai `Analog`, `Connected=true`, lalu memanggil `map()` melalui Lua sebelum tes boot. Setup ini mengikuti tes internal upstream PCSX-Redux di `tests/pcsxrunner/rumble.cc`.
- **Status eksperimen baru: hasil belum diverifikasi dalam catatan riset.** Jangan menyimpulkan peringatan `0x43` hilang atau boot berhasil berdasarkan commit workflow saja.
- Langkah wajib berikutnya: baca log run sesudah perubahan dan pastikan marker `PAD_SETUP=port1 analog device connected and remapped` muncul. Bandingkan pesan `0x43`; jika hilang, lanjutkan dengan tes GUI Xvfb dan konfirmasi frame title/menu serta respons input. Jika tetap hitam, pisahkan masalah kontroler dari jalur CD-ROM, boot executable, dan rendering.
- Dilarang menyimpan/unggah ROM, game EXE, BIOS retail, save state, dump RAM atau screenshot game ke repo.

- Koreksi penting: revisi workflow awal salah indentasi pada heredoc Lua; versi final yang berlaku adalah [0439c1b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/0439c1bbf51d3c1be234150d6bee80c5b812ff1e), setelah indentasi YAML dibetulkan. Belum ada hasil runtime terverifikasi yang dicatat dari versi final ini.


## Hasil runtime Port 1 Analog — 2026-10-17

- Runner Actions [#38973267415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973267415) sukses. Marker Lua menyatakan Port 1 sudah `Analog`, terhubung, dan di-remap.
- Kedua build (AnyLinux dan upstream HEAD) mencapai `EXEC:PC0(80011448)` dan `Execute !`. Tidak ada pesan `Unknown command for pad: 43` di kedua log setelah konfigurasi Analog; baseline sebelumnya memunculkan pesan itu pada dua build. Masing-masing dihentikan pada batas waktu 90 detik, bukan crash.
- Kesimpulan terkonfirmasi: konfigurasi controller memperbaiki ketidakcocokan protokol `0x43` pada log. **Belum terbukti** bahwa title/menu tampil atau input dalam game berfungsi.
- Tes rendering GUI ditambahkan pada workflow commit [85c08d9](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85c08d9ea255dc400c0771361abc95817a0a7ba6). Actions [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) terlihat queued; hasil akhir belum diverifikasi. Probe ini menganalisis dua frame lokal (10s dan 20s) dan mencatat metrik/teks, tanpa menerbitkan gambar atau ROM/BIOS.


## GUI probe and CPU trace — 2026-10-17

- Actions [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) completed successfully. Under GUI + Xvfb, frame 10s and frame 20s both measured `1280x800`, `mean=0`, `stddev=0`, `colors=1`; OCR Japan/English returned no text. The captured desktop was entirely black at both points.
- Selected GUI logs did not show `EXEC:PC0` or `Execute !` within its 35-second window, unlike the headless probe. BIOS, disc ID and Analog PAD_SETUP markers did appear. This is a separate GUI/headless discrepancy, not proof that the game executable is invalid.
- New separate CPU trace workflow: [naruto-cpu-trace.yml](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/blob/main/.github/workflows/naruto-cpu-trace.yml), run [#38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045). It samples `PC`, `RA`, `SP` on every 30th `GPU::Vsync` callback, capped at 600 frames. Result not yet verified at time of writing.


## CPU trace attempt 1 — status 2026-10-17

- [Actions #38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045) exited with code 139 about 12 seconds after the VSync trace callback was added; no `PC_TRACE` sample appeared. Treat this as an instrumentation failure until isolated, not evidence against the ROM.
- Retry workflow revision: [9419800](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/941980021c16dee3e779f6cc1066dad70b187ad4). It uses one combined `-exec` script and no longer removes the listener from its callback. Check [run #38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739); if it also crashes, reduce the callback to count VSyncs only.


### CPU trace attempt 2 correction — 2026-10-17

- Run [#38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739) ended with exit 134 because Lua parsing failed: `unexpected symbol near '\\'`. The helper used a doubly escaped newline, passing literal `\n` instead of a newline between chunks. No valid tracing code ran; do not interpret as a ROM crash.
- Workflow commit [7b8ce73](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/7b8ce731378e0115f616b7ff78874f5d17375e80) replaced concatenation with one Lua heredoc. Check retry [Actions #38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869) for setup and VSync samples.


### CPU trace attempt 3 and counter-only isolation — 2026-10-17

- Corrected trace run [#38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869) emitted PC samples from frame 30 through at least 780. Values often point to BIOS routines (`BFC0574C`, `BFC05784`, `BFC03C6C`), with occasional `0xB0` and `0x2998`; the separate log includes `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, `Execute !`. The emulator process still exited 139 (segfault) with an incomplete final sample, so register reads inside the callback could be involved. The trace does not prove the game crashed or remained on one PC.
- Isolation run [#38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602), workflow commit [85d3e4f](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85d3e4ff31732b7788d67e447ea9df136dcb84f5), removes CPU-register reads and prints only a VSync counter. Results pending.


### Counter-only VSync test passed — 2026-10-17

- Run [#38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) reached expected `TRACE_PROCESS_EXIT=124` after the 35-second cap; VSync counter advanced through `frame=2040`. Headless boot markers `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, `Execute !` appeared. Counter-only callback is stable.
- New probe [#38974903834](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974903834), commit [ff0faa5](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/ff0faa598c6e19295229b450c6f9d42c83e590fb), keeps counter and adds sparse PC-only reads from a register view acquired before callback registration. Result pending.


### Emulator trace API mismatch — 2026-10-17

- Run [#38975154606](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975154606) aborted with `attempt to index field 'CPU' (a nil value)` because the pinned AnyLinux build from upstream ref `0c3572c3d` has no `PCSX.CPU.Trace` API. This test did not begin VSync counting; it says nothing negative about the ROM.
- Corrected workflow commit [c994afc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/c994afccfa62efcc01751a7c2b39d89b109d936a) now verifies and uses private-release upstream HEAD AppImage SHA-256 `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`. Run [#38975223698](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975223698) is the new bounded CPU-trace attempt; outcome pending.


### CPU trace API correction and source build — 2026-10-17

- The private upstream HEAD AppImage in [run #38975223698](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975223698) also lacks `PCSX.CPU.Trace`; it aborted before VSync counting. Neither packaged AppImage asset currently available exposes this newer API.
- Current runner workflow commit [8304b7d](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8304b7dd56be13673e83e84bb738458eca0cfc2d) now clones source pinned to upstream commit `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` and compiles it with the official PCSX-Redux builder container. [Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) is building; results pending.


### Catatan interpretasi GUI — 2026-10-17

- Frame hitam pada 10s/20s di [run #38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) diambil sebelum executable game terbukti dijalankan. Counter-only [run #38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) menunjukkan entry point baru dicapai setelah sekitar 27–30 detik dalam tes headless. Karena itu capture 10s/20s bukan bukti bahwa layar tetap hitam sesudah entry. Tes GUI harus diperpanjang hingga setidaknya 60–90 detik dan idealnya menangkap window emulator secara langsung.
- Source-build trace [run #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) sedang mencoba build source pinned agar API CPU trace tersedia tanpa membaca register dari callback. Hasil belum terverifikasi.


### Tes lanjutan sedang berjalan — 2026-10-17

- GUI run terbaru [#38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679), workflow commit [aea4c20](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aea4c20accfd6d1c5089a226f52a2c4183d2d9a8), memperpanjang pengamatan hingga 100 detik dan mengambil frame pada 30/60/90 detik. Saat catatan ini diperbarui, langkah A/B + GUI masih berjalan.
- CPU trace source-build run [#38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) belum melewati langkah build pinned upstream source. Hasil build dan trace tetap pending.


## Verifikasi cloud runner dan koreksi observasi — 2026-10-17

Pemeriksaan ulang repositori mengonfirmasi riset ini tetap **private**, sedangkan `naruto-shinobi-jintori-runner` tetap public. Release `research-emulator-pcsx-redux-2026-10-15` berisi aset ROM/CUE/OpenBIOS yang diperlukan; nama aset ROM dan CUE dinormalisasi dengan titik oleh proses unggah Release. Tidak ada media permainan yang ditambahkan ke Git runner.

Run [runner Actions #38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679) selesai dengan kesimpulan job **success**. Log mengonfirmasi secret read-only hadir tanpa menampilkan nilainya, ukuran ROM 325.989.552 byte, SHA-256 cocok, CUE valid, BIOS OpenBIOS dikenali, disc label `SLPS-03553`, `SYSTEM.CNF` menunjuk `SLPS_035.53`, seluruh 187 chunk executable dibaca, lalu tercatat `EXEC:PC0(80011448)` dan `Execute !`. Konfigurasi Port 1 Analog juga menghilangkan pesan `Unknown command for pad: 43` pada dua build pembanding. Ini membuktikan transfer kendali ke entry executable dalam jalur headless, **bukan** bukti title/menu atau input gameplay.

Capture GUI 30/60/90 detik pada run tersebut melaporkan gambar hitam (mean 0, stddev 0, satu warna) dan OCR kosong. Audit workflow memperlihatkan capture dilakukan dengan `import -window root`, yaitu latar root Xvfb, bukan window emulator secara eksplisit. Karena itu angka tersebut tidak boleh dipakai untuk menyimpulkan bahwa framebuffer game hitam.

CPU trace source-build [Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) membangun emulator tetapi peluncuran di host berhenti dengan `libcapstone.so.5: cannot open shared object file`; belum ada VSync atau instruksi yang direkam. Ini kegagalan dependensi runtime runner, bukan bukti masalah ROM/game.

Koreksi yang sudah dikirim ke repo runner:
- Commit [d965dcc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/d965dcc864c73818e67d6a1e5f9edc19d4a3a17c) menambahkan `libcapstone-dev` dan pemeriksaan `ldd` sebelum trace, supaya dependensi yang hilang terdeteksi sebelum emulasi.
- Commit [8829933](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8829933b3b6815dce694ebe6d46cd2a1f0fee9f0) memasang `xdotool`/`x11-utils` dan menargetkan window PCSX-Redux untuk pengukuran/OCR. Jika window tidak ditemukan, workflow mencatat pohon window dan tidak menggantinya dengan capture root hitam. File gambar tetap lokal di runner dan dihapus saat cleanup.

Retest yang dimulai dari dua commit itu belum selesai pada waktu catatan dibuat: GUI [Actions #39000276365](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365), CPU trace [Actions #39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139). Periksa hasil finalnya sebelum menetapkan status boot. Jangan mulai RT-001/gameplay sampai title/menu yang dikenali dan respons input terbukti.


## GUI-window retest result — 2026-10-17 (Actions #39000276365)

The corrected capture test completed successfully. Its log found the actual PCSX-Redux X11 window (CAPTURE_WINDOW at 30s, 60s and 90s), rather than the Xvfb root. All three captured PCSX-Redux-window frames nevertheless measured 1280x800, mean=0, stddev=0, colors=1; Japanese/English OCR returned no text.

Important distinction: the GUI probe's own log shows BIOS/OpenBIOS and disc metadata, but does not show [CHUNK1] done chunks=187, EXEC:PC0(80011448) or Execute !. Those entry markers are present in the separate headless A/B probes in the same job. Therefore the current evidence does not show a black game frame after executable entry; it shows that GUI mode remains black and did not log the same executable handoff as headless mode. Investigate this GUI/headless boot-path difference before diagnosing the game's renderer.

Run: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365. ROM/BIOS, frames and logs were removed during runner cleanup; no game media or screenshot was committed.


## GUI-init/GL diagnostic rerun queued — 2026-10-17

After the corrected capture proved the PCSX-Redux window itself remained uniformly black and the GUI probe lacked both PAD_SETUP and executable-entry markers, the runner workflow was tightened further. Commit [259d587](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/259d587c6b677be7f6466b0ec61edb1940faec49) adds a Mesa/GLX capability report from the same Xvfb + software-rendering environment, prints the final GUI stdout and emulator logfile tails, and explicitly reports whether the Lua PAD_SETUP marker ran. Cloud rerun [Actions #39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307) was in progress at the latest check.

This experiment distinguishes failure in PCSX-Redux GUI/OpenGL initialization or startup from a guest-game display problem. Do not label the title screen black after game entry unless the GUI run itself logs `[CHUNK1] done chunks=187` and `EXEC:PC0(80011448)` before the measured frames. Source-built CPU-trace dependency retest [Actions #39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) remains in progress; the run must complete its compile/preflight before trace conclusions can be made.


## Perbandingan cloud AnyLinux vs upstream-labelled HEAD — 2026-10-17

Run headless A/B terbaru [#39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307) memakai ROM/CUE dan OpenBIOS yang sama, mode interpreter/software GPU, setup Port 1 Analog yang sama, serta batas observasi 90 detik. Kedua AppImage mengenali disc SLPS-03553, membaca SYSTEM.CNF, menyelesaikan 187 chunk (382.976 byte payload EXE), lalu mencatat EXEC:PC0(80011448) dan Execute !. Keduanya tidak lagi mencatat Unknown command for pad: 43. Kedua proses mencapai batas waktu observasi; ini bukan crash yang terbukti dan bukan bukti game dimainkan.

Build di release:
- AnyLinux PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage, 65.747.557 byte, SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c, source commit 0c3572c3db75f97542001e453ae80ba8c3f8acba.
- AppImage bernama PCSX-Redux-HEAD-x86_64.AppImage, 91.474.424 byte, SHA-256 5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8. Package inventory mencatat source commit 9c6f98a0ed0581635f9123147e382c248e0f5ddc (2026-09-28), bukan source-build CPU-trace terbaru.

Diagnostik GUI [#39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307) mengonfirmasi GLX tersedia: Mesa llvmpipe, OpenGL 3.3. Jendela AnyLinux yang benar berhasil ditangkap pada 30/60/90 detik, tetapi seluruh frame 1280×800 seragam hitam (mean 0, stddev 0, 1 warna) dan OCR kosong. Log GUI mencapai penanda setup Lua dan hanya menampilkan progres chunk awal (indeks 0, 8, 16, 24, 32); tidak ada marker 187 chunk selesai, EXEC:PC0 atau Execute ! pada log GUI. Jadi masalah bukan ketiadaan GLX yang terbukti; jalur GUI masih berhenti sebelum executable handoff.

Workflow runner diperbaiki untuk menangkap jendela GUI kedua AppImage dalam kondisi setara dan membersihkan file frame/log sementara. Rerun [#39002136781](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002136781) baru queued ketika catatan ini ditulis. Source-build CPU trace kini menjalankan binary di dalam image Docker builder yang sama setelah run [#39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) gagal pada preflight host karena FFmpeg/SDL dari builder tidak tersedia di host. Rerun [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) masih berjalan saat pencatatan.

**Rekomendasi bersyarat:** gunakan AnyLinux sebagai kandidat utama operasional di runner standar (lebih kecil dan dipaketkan untuk kompatibilitas Linux), serta pertahankan AppImage berlabel HEAD sebagai pembanding cadangan, bukan sebagai “upstream HEAD terkini”. Untuk analisis instruksi gunakan source-build terpisah dengan API PCSX.CPU.Trace; jangan menganggap API itu tersedia pada kedua AppImage. Belum ada pemenang untuk gameplay/rendering: hasil GUI kedua build masih perlu diperiksa. Title/menu Naruto dan input dalam game belum terbukti; Story Mode belum dimulai.


## Verifikasi identitas build upstream — 2026-10-17

Pengecekan API upstream menunjukkan main/head PCSX-Redux saat diperiksa adalah commit [41f3196257d0962942b60983201aade951ebbd54](https://github.com/grumpycoders/pcsx-redux/commit/41f3196257d0962942b60983201aade951ebbd54), bertanggal 2026-10-17 02:53:17 UTC. Maka asset release dengan nama PCSX-Redux-HEAD-x86_64.AppImage (source 9c6f98a0, 2026-09-28) bukan current upstream HEAD; build AnyLinux menggunakan source 0c3572c3 (2026-10-01), dan source-build trace dipatok ke 6b9df482 (2026-10-16). Perbedaan ini membedakan identitas build, bukan membuktikan penyebab screen hitam.


## Verifikasi GUI A/B terbaru dan perbaikan harness — 2026-10-17

Run GUI A/B [#39002136781](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002136781) berstatus workflow `success`, tetapi **bukan hasil uji GUI yang berhasil**. Langkah headless di job yang sama tetap membuktikan kedua AppImage membaca disc `SLPS-03553`, menuntaskan 187 chunk executable, dan mencatat `EXEC:PC0(80011448)` serta `Execute !`; keduanya tidak lagi mencatat `Unknown command for pad: 43`. Saat masuk bagian GUI, `gui_probe.sh` berhenti untuk kedua build pada `PAD_SETUP: unbound variable` karena variabel shell tidak diekspor. Tidak ada jendela emulator yang ditemukan dan tidak ada frame yang ditangkap. Karena hasil probe tidak dipaksa menjadi kegagalan job, status `success` hanya berarti step berakhir tanpa kegagalan workflow yang terdeteksi; status itu bukan bukti GUI/game berhasil.

Perbaikan minimal sudah didorong ke runner pada commit [aac684d120ec025c4a87197da8d835f90b89f869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aac684d120ec025c4a87197da8d835f90b89f869): ekspor `PAD_SETUP` sebelum skrip probe GUI dipanggil. Rerun ROM privat [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) sudah dipicu dan masih `in_progress` pada pemeriksaan terakhir; hasil frame, OCR, boot-marker GUI, dan cleanup masih harus diperiksa dari log akhirnya.

CPU-trace run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) juga masih `in_progress`. Secret dan pengunduhan/verifikasi file privat telah dilewati; step source-build di container Docker yang dipatok digest masih berjalan, sedangkan capture trace dan cleanup belum dimulai. Belum ada `CPU_TRACE_SIZE` atau `CPU_TRACE_LINE` yang dapat dipakai untuk analisis.

Current upstream PCSX-Redux yang terverifikasi saat cek adalah [41f3196257d0962942b60983201aade951ebbd54](https://github.com/grumpycoders/pcsx-redux/commit/41f3196257d0962942b60983201aade951ebbd54) (2026-10-17 02:53:17 UTC). AppImage berlabel “HEAD” tetap build source 9c6f98a0, bukan upstream HEAD terkini. Tidak ada bukti bahwa judul/menu tampil atau input gameplay merespons; gate RT-001 tetap tertutup dan Story Mode tidak boleh dimulai.


## Hasil final GUI A/B setelah perbaikan PAD_SETUP — 2026-10-17

Run [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) selesai dengan workflow/job `success` pada runner commit [aac684d120ec025c4a87197da8d835f90b89f869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aac684d120ec025c4a87197da8d835f90b89f869). Hasil `success` bukan berarti kedua GUI berhasil menampilkan game. Job ROM selesai dan job smoke dilewati; tidak ada artefak Actions yang dipublikasikan.

- **Headless A/B (baseline terpisah):** kedua AppImage tetap mengenali BIOS OpenBIOS, disc `SLPS-03553`, `SYSTEM.CNF` dan target `SLPS_035.53`; masing-masing mencatat `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, serta `Execute !`. Keduanya mencapai batas observasi headless 90 detik (exit 124), bukan crash yang terbukti.
- **AnyLinux GUI:** `PAD_SETUP=port1 analog device connected and remapped` muncul; BIOS dan metadata disc serta `SYSTEM.CNF`/`BOOT` juga tercatat. Jendela yang ditemukan (X11 ID `2097204`) ditangkap langsung pada 30/60/90 detik, bukan root window Xvfb. Ketiga frame 1280×800 memiliki mean=0, stddev=0 dan 1 warna; OCR Jepang/Inggris kosong. Log GUI tidak memiliki marker chunk 187, `EXEC:PC0`, atau `Execute !`. Proses mencapai batas observasi 100 detik (exit 124). Artinya harness sudah berjalan dan menangkap window, tetapi jalur GUI belum membuktikan handoff executable.
- **AppImage berlabel “HEAD” GUI:** jendela emulator tidak ditemukan dan tidak ada frame pada 30/60/90 detik. Log final: `Unable to create main window: Couldn't find matching GLX visual` serta `SDL failed to create OpenGL 3.2 core context, retrying with any 3.0 profile`. Marker Lua `PAD_SETUP` dan executable-entry tidak muncul. Proses kembali dengan exit 137 sesudah batas observasi/eskalasi timeout; karena kegagalan pembuatan window sudah tercatat, jangan menyebutnya crash guest atau masalah ROM yang terbukti.
- Marker `Unknown command for pad: 43` tidak muncul pada kedua jalur headless maupun log GUI yang diperiksa. Ini tidak membuktikan input gameplay merespons.
- Langkah cleanup sukses dan mencatat bahwa ROM/BIOS/CUE, log, profil, frame, serta dua pohon AppImage sementara dihapus. Inventaris repo runner tetap hanya workflow, dokumentasi, README dan .gitignore; tidak ditemukan file media game atau artefak run.

## Status CPU trace source-build saat pemeriksaan terakhir — 2026-10-17

Run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849), commit workflow [16a6faff066b913480ad121b497db79df03a9de2](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/16a6faff066b913480ad121b497db79df03a9de2), masih `in_progress`. Unduh/verifikasi ROM/CUE/BIOS selesai pada 04:17:26 UTC; step build source pinned masih berjalan saat pengecekan berikutnya (sekitar paruh dari batas job 45 menit). Step capture trace dan cleanup belum mulai. Endpoint unduhan log job mengembalikan `BlobNotFound` sementara run aktif, sehingga belum ada bukti log build yang dapat dianalisis; artefak run belum ada. Belum ada hasil `PCSX_BUILD_RESULT`, `CPU_TRACE_SIZE`, `CPU_TRACE_LINE`, `TRACE_RESULT`, `CPU_TRACE_RESULT`, atau `TRACE_PROCESS_EXIT` yang terverifikasi. Jangan menjalankan duplikat atau menyatakan build gagal sebelum run selesai/batas waktu tercapai; periksa step aktif lagi sebelum deadline 45 menit.

**RT-001 tetap terbuka/terblokir.** Belum ada title/menu Naruto yang dikenali maupun respons input terkontrol. Jangan mulai Story Mode.

## Hasil final CPU trace source-build dan verifikasi GUI — 2026-10-17

Run [CPU trace #39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) telah selesai dengan kesimpulan `success`. Job 117306664750 berjalan 04:17:11–04:44:27 UTC. Download/verifikasi aset selesai 04:17:26; build source pinned selesai 04:43:46; capture trace 04:43:46–04:44:21; cleanup 04:44:21–04:44:25. Semua langkah berhasil. Source commit `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`, image builder `ghcr.io/grumpycoders/pcsx-redux-build@sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`. `PCSX_BUILD_RESULT` menyatakan build sukses; pemeriksaan `ldd` dalam image yang sama tidak menemukan dependency `not found`.

Capture membuktikan `VSYNC_TRACE` berlanjut melewati 1620, 1650, dan 1680; `CPU_TRACE_WINDOW=enabled frame=1620`; `CPU_TRACE_SIZE=16031631`; `TRACE_RESULT=VSync counter callbacks fired.`; `CPU_TRACE_RESULT=Built-in instruction records were printed.`; dan `TRACE_PROCESS_EXIT=124` pada batas observasi 35 detik yang memang dirancang. Run tidak menerbitkan artefak. Cleanup menyatakan ROM/CUE/BIOS, emulator, serta log trace sementara dihapus dari runner.

80 instruksi terakhir menunjukkan loop guest di PC mentah `0x000015a4–0x000015c4`: load dari `0x5de4(a3)` menghasilkan 0, cabang membandingkan dengan 2/1, dan `$v1` dihitung turun sambil kembali ke `0x000015a4`. Penghitung berkurang; ini eksekusi berulang yang bergerak, bukan bukti hang permanen. Run source-build ini tidak merekam `SYSTEM.CNF`, `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, atau `Execute !`. Jangan tetapkan pemilik loop sebagai BIOS, loader, atau overlay sebelum mapping divalidasi. Trace menyimpan `m_regs.pc` mentah menurut source pinned PCSX-Redux; alamat loop berbeda dari entry EXE `0x80011448`.

GUI A/B [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) juga selesai. AnyLinux GUI menjalankan `PAD_SETUP` dan menangkap window sebenarnya pada 30/60/90s, tetapi frame tetap hitam seragam dan tidak ada handoff EXE dalam log GUI. AppImage berlabel “HEAD” gagal membuat window akibat GLX/OpenGL. Kedua build di mode headless lama mencapai entry; bukti itu tidak bisa dipindahkan ke GUI atau source-build trace. RT-001 tetap **Open / blocked** sampai title/menu dikenali dan input terkontrol terbukti responsif.

## Perbandingan versi source terhadap baseline headless — 2026-10-17

Perbandingan GitHub langsung antara source AnyLinux `0c3572c3db75f97542001e453ae80ba8c3f8acba` dan source CPU-trace `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` menghasilkan selisih 803 commit. File yang berubah besar termasuk `src/core/cdrom.cc` (+1.476/-1.392 baris), `src/core/psxinterpreter.cc` (+290/-81), `src/core/pad.cc` (+362/-22), `src/core/psxmem.cc`, dan pointer submodule `src/mips`. Pada interpreter, macro target branch berubah dari memakai `_PC_` langsung menjadi `branchBase()` beserta pelacakan delay slot/exception; CD-ROM juga direstrukturisasi. Ini kandidat area pembandingan, bukan bukti akar masalah.

Kedua perintah headless memakai `-no-ui -exec ... -run -interpreter -softgpu -stdout -lua_stdout -logfile`; jadi jangan menyalahkan dynarec sebagai beda utama. Namun durasi observasi berbeda: AppImage headless diberi 90 detik dan mencapai EXEC:PC0; source-trace build hanya 35 detik dan merekam frames 1620–1680 sebelum timeout. Karena itu belum sah menyebutnya regresi source atau hang tanpa pengujian pada batas waktu yang sebanding. Langkah paling bernilai adalah trace source pinned pada window lebih akhir (mis. frames 4500–4560) dengan logging PC guest pada VSync berkala, serta marker boot dicetak terpisah dari ekor trace agar tidak terpotong oleh `tail`.


## Follow-up CPU trace dengan agregasi aman — 2026-10-17 (run masih aktif)

- Workflow runner diperkeras pada commit publik `d1c5b731befe5afacdfbdf3b9914b9f5e9f9ac64` (blob workflow `b06bb37d23c0fc7ff386ce0846e08f719b46d3bf`): observasi 90 detik, PC guest tiap 30 VSync, trace window frame 1620–1680 dan 4500–4560, ringkasan PC agregat saja, boot markers dipisah, cleanup `if: always()` dipertahankan. Source `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` dan image builder digest tetap sama.
- Run [#39004736399](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39004736399) menggunakan commit workflow tersebut. Pemeriksaan terakhir: secret check, workspace, dan download/verifikasi file lulus; build source masih `in_progress`; capture dan cleanup belum berjalan. Jangan menganggap pengujian runtime berhasil/gagal sebelum status dan log final diperiksa.
- Audit log publik menemukan 80 record instruksi/operand aktual pada run #39001985849; tidak ada artifact Actions. Run CPU-trace lama lain yang diperiksa tidak memuat record instruksi aktual. Workflow baru tak lagi mencetak record mentah. Log run #39001985849 masih dapat diakses; antarmuka GitHub yang tersedia di sesi ini tidak menyediakan tindakan penghapusan run/log.
- RT-001 tetap **Open / blocked**; title/menu Naruto dan respons input terkontrol belum terbukti.

## Hasil final CPU trace 90 detik — Actions #39004736399 (2026-10-17)

Run [#39004736399](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39004736399) selesai dengan status workflow/job `success`. Waktu run 05:01:31–05:29:40 UTC (12:01:31–12:29:40 WIB). Semua step selesai sukses: secret check, persiapan workspace, download/verifikasi aset, build source PCSX-Redux, capture/diagnostik, dan cleanup.

- ROM lulus pemeriksaan ukuran 325.989.552 byte dan SHA-256 `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`. CUE dinormalisasi hanya untuk referensi berkas sementara. Source pin `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`; builder image tetap `ghcr.io/grumpycoders/pcsx-redux-build@sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`.
- Build berlangsung sekitar 26 menit 20 detik, berakhir dengan `PCSX_BUILD_RESULT`. Pemeriksaan dependency `ldd` di image builder yang sama lulus tanpa library bertanda `not found`.
- Capture mencapai sampel VSync dari frame 30 sampai 4740, tiap 30 frame: 158 sampel. PC adalah `0x000015a4` pada 157 sampel; satu pengecualian sampel berada di frame 420 pada `0x00000870`, lalu PC kembali ke `0x000015a4`.
- Ringkasan CPU trace pada frames 1620–1680: 200 record diperiksa, 9 PC unik, total terlapor 16.031.631 record. Pada frames 4500–4560: 200 record, 9 PC unik, total terlapor 16.031.484 record. Kedua jendela memiliki pola hot PC yang sama; alamat teratas `0x000015c0` dan `0x000015c4` masing-masing muncul 23 kali, `0x000015a4` dan beberapa alamat tetangganya sekitar 22 kali.
- Boot marker yang terlihat: OpenBIOS dikenali, disc label `SLPS-03553`, disc ID `SLPS03553`, executable `SLPS_035.53;1`. Tidak terlihat `SYSTEM.CNF`/baris `BOOT =`, `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, atau `Execute !`.
- `TRACE_PROCESS_EXIT=124` adalah batas observasi 90 detik yang disengaja, bukan bukti crash guest. Tidak ada marker FATAL/Exception/ERROR pada bagian runtime yang disaring. Keluaran runtime baru hanya agregat PC dan tidak memuat record instruksi/operand mentah.
- Cleanup menyatakan ROM/CUE/BIOS, emulator hasil build, dan log runtime sementara telah dihapus dari runner ephemeral. Daftar artefak Actions kosong.

**Interpretasi:** pengujian memperkuat bukti adanya loop PC berulang dalam sesi OpenBIOS/disc, tetapi tidak mengidentifikasi pemilik loop dan tidak membuktikan handoff ke executable utama. Jangan menyebutnya kode game, hang permanen, atau akar masalah spesifik sebelum mapping alamat dan jalur pemanggil diverifikasi.

**RT-001 tetap Open / blocked.** Belum ada title/menu Naruto yang dikenali dan belum ada respons input terkontrol yang terbukti. Jangan mulai Story Mode. Log publik lama [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) masih perlu ditinjau karena memuat 80 record instruksi/operand; run baru ini tidak mengulangi keluaran mentah tersebut.

## Status terbaru — SPU raw savestate probe, 20 Oktober 2026

Run [#39373493482](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39373493482) selesai dengan workflow **failure**. Sumber checkpoint raw tetap utuh: 21.163.286 byte, SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d; hash staging cocok persis. Build emulator varian yang hanya menambahkan perbaikan upstream PR #2218 berhasil, dan schema save-state binary baseline vs varian sama persis. Event ExecutionFlow::SaveStateLoaded muncul, loader kembali normal, dan screenshot segera setelah restore identik dengan screenshot checkpoint (mean RGB diff 0.00000; exact pixel fraction 1.000000).

Namun workflow mencapai batas observasi 1800 detik dengan exit code 124 saat menunggu pemeriksaan screenshot pasca-180 VSync/checkpoint berikutnya. Analisis skrip menemukan emulator dijeda sebelum polling nextTick membaca file gate dari pembanding; sehingga tahap lanjutan dapat tersendat walaupun pembanding screenshot awal sudah PASS. Ini kegagalan harness/pengujian lanjutan, bukan bukti bahwa state mentah rusak atau bahwa fix sudah lolos semua syarat.

Workflow diperbaiki pada commit 8bb5c0ed829cc2ff5e004612445c8fdb88836d04: emulator tidak lagi dijeda saat loop nextTick menunggu gate screenshot. Pemicu push sementara sudah dibersihkan; workflow kini kembali hanya workflow_dispatch. Percobaan ulang [#39383287999](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39383287999) sedang berjalan pada pemeriksaan terakhir. Belum ada artefak hasil atau checkpoint baru.

**Status savestate: pemulihan awal terbukti sampai event/load-return dan gambar awal, tetapi kelanjutan 180 VSync + checkpoint baru + reload dalam proses kedua belum lulus. Jangan lanjutkan Story Mode dulu.**

## Pembaruan hasil run SPU probe — 20 Oktober 2026, malam

Run ulang [#39383287999](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39383287999) selesai dengan `failure` setelah sekitar 49 menit. Bukan crash loader: log mencatat `ExecutionFlow::SaveStateLoaded`, `STORY_SAVESTATE_LOAD_CALL_RETURNED=1`, dan screenshot comparison `PASS` (mean RGB diff 0.00000; exact pixel fraction 1.000000). Namun gerbang `STORY_RAW_RESTORE_POST_RESTORE_VSYNC=180` dan `STORY_RAW_RESTORE_CROSS_RUN=PASS` tidak pernah muncul; script melanjutkan VSync sampai frame 12000, lalu workflow gagal pada assertion gerbang. Manifest akhir menyatakan next checkpoint 0 byte/missing, sehingga checkpoint hasil tidak dapat digunakan dan reload kedua dilewati.

Akar masalah tambahan pada harness: perbaikan sebelumnya hanya menghapus jeda emulator, tetapi tetap memakai rekursi `PCSX.nextTick(wait_for_screenshot_match)` untuk membaca file gate. Callback itu tidak menjalankan gerbang sukses pada run ini. Workflow kini diperbaiki lebih jauh agar membaca flag pembanding langsung pada callback `GPU::Vsync`, dengan timeout terbatas 900 VSync; sesudah PASS ia baru menjeda pada safe tick, menyimpan checkpoint, dan menghentikan proses. Jika mode validasi proses kedua aktif, callback yang sama hanya menyatakan reload PASS dan keluar.

Run [#39426068247](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39426068247) sedang berjalan; runner dan job sudah mulai, belum ada artefak final. Dua pemicu perantara #39425629341/#39425661897 gagal tanpa job/artefak sehingga bukan hasil eksperimen emulator. Pemicu sementara telah dibersihkan dan workflow kembali hanya manual-dispatch.

**Status:** checkpoint sumber mentah terjaga dan load awal pada patched build terlihat benar. Belum ada bukti checkpoint lanjutan dapat dimuat pada proses kedua. Jangan lanjut Story Mode dari checkpoint probe sampai proses kedua lulus.

## Hasil final: SPU/ADPCM savestate restore PASS — diverifikasi 21 Oktober 2026

Run [#39426068247](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39426068247) selesai `success`; semua 18 langkah job, termasuk pemulihan board dan validasi checkpoint pada proses emulator kedua, berhasil.

Bukti:
- Raw checkpoint sumber #39262213468 tetap tidak berubah: 21.163.286 byte, SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`. Hash staging sama persis.
- Emulator varian dibangun dari base commit `0c3572c3db75f97542001e453ae80ba8c3f8acba` ditambah hanya patch upstream SPU/ADPCM PR #2218. Schema baseline/varian identik.
- Restore menghasilkan event `ExecutionFlow::SaveStateLoaded`, loader kembali normal, lolos 180 VSync, dan screenshot cocok pada gerbang yang diwajibkan.
- Checkpoint lanjutan berhasil disimpan pada frame probe 181. Ukuran 21.162.405 byte, SHA-256 `b23668dd295dc2db7e8e21cd66e663f8055418e794b393434562b9119d41ad8a`; header raw savestate v4 lulus validasi.
- Proses emulator kedua yang baru memuat checkpoint lanjutan tersebut dan lulus event load, loader-return, 180 VSync, serta screenshot compare. Kedua proses dan kedua comparator keluar dengan kode 0.
- `PROBE_NEXT_CHECKPOINT_VALID=PASS`; `PROBE_NEXT_CHECKPOINT_FRESH_PROCESS_VALIDATION=PASS`; tidak ada controller input atau transformasi state sumber.

Artefak privat Actions #12268621845 (`naruto-spu-sentinel-fix-probe-private`) menyimpan checkpoint dan bukti; kedaluwarsa 3 November 2026. ROM, BIOS, dan Memory Card tidak diunggah sebagai artefak ini; tidak ada savestate mentah yang ditaruh di Git.

**Kesimpulan yang diizinkan:** pemulihan raw Story Mode checkpoint dan pemuatan ulang checkpoint berikutnya dapat diandalkan pada build PCSX-Redux yang menyertakan fix SPU/ADPCM ini, menurut kriteria probe tersebut. Run ini tidak mengirim input gameplay; Story Mode belum dilanjutkan, Memory Card save/load di dalam game belum diverifikasi, dan tamat game belum terbukti. Langkah berikutnya ialah melanjutkan Story Mode dari checkpoint baru memakai varian emulator patched yang sama, sambil terus menyimpan checkpoint dan merekam aturan gameplay.

## Adaptive player readiness update — 23 October 2026 (Revision61)

**Readiness: NO-GO.** This is not a Story Mode completion test and completion is not a prerequisite. The short-run checkpoint mechanism passes structural validation, but the agent is not yet ready to play unattended because it still cannot resolve a barrier-selection submenu.

Latest verified runs:
- Regression [#39909012516](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39909012516): success; 17 unit/source regression tests passed.
- Revision60 [#39908484177](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39908484177): matched LEFT-vs-WAIT test, same source checkpoint and identical Memory Card clones. LEFT input readback was verified and visibly changed the character pose, but state stayed `barrier_level_selection`; target selection remains unverified.
- Revision61 [#39909132189](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39909132189): Circle-vs-WAIT using Revision60's LEFT branch output checkpoint. Circle press/release readbacks passed, but frames F60/F100/F110/F180 were pixel-identical in both branches (zero differing pixels), and state stayed `barrier_level_selection`. Thus Circle did not visibly confirm a target from that state.

Next bounded test: implement and test a one-session sequence A/B from pre-LEFT parent checkpoint (run #39907655833, `adaptive-cycle-02-f180.sstate`, SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`). Action branch: LEFT press/release, capture at F60, then CIRCLE press/release in same emulator process; control branch: no inputs. Require identical initial F20, exactly two configured action presses in C01 and none in C02, explicit press/release readbacks, authentic screenshots, and validated private output checkpoints. Add regression tests before triggering the run. Keep normal policy WAIT until the submenu's target/confirm transition is visually verified.

All work stays in this repository. ROM, BIOS, Memory Card, savestates and screenshots stay in private Actions artifacts, never Git. Japanese labels should be followed immediately by Indonesian translation. Use START to skip dialogue only when dialogue is detected. Do not claim Story Mode completed.


## Adaptive player readiness — Revision62 one-session LEFT → CIRCLE A/B (23 October 2026)

**Readiness remains NO-GO.** This is a short autonomous-input qualification experiment, not a Story Mode completion test. Finishing Story Mode is not required for this readiness milestone.

- Regression [#39939979616](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39939979616) completed successfully. The log shows 18 tests passed plus the authentic external-X11 policy checks.
- Revision62 player run [#39940196133](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39940196133) completed successfully; private artifact #12495906030 contains the runtime evidence. Source checkpoint adaptive-cycle-02-f180.sstate from #39907655833 was 21,162,799 bytes, v4 header, SHA-256 705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35. Artifact source was re-read locally for header/size/hash; the immutable-source gate and ADAPTIVE_AB_PARENT_PRESERVED=PASS also passed.
- Both independent emulator processes loaded the same parent. The two Memory Card clones matched SHA-256 ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5. Initial C01/C02 F20 captures were pixel-identical (1,024,000 pixels).
- C01 sent exactly LEFT at F30 (press readback=true), released F38 (readback=false), then CIRCLE at F70 (press readback=true), released F78 (readback=false). C02 sent no button press. All ten authentic external-X11 screenshots (C01/C02 × F20/F60/F100/F110/F180) were valid 1280×800 captures. Both output checkpoints passed v4 header/size/SHA validation:
  - C01: 21,163,248 bytes; SHA-256 cf868811502f65f3cd03b7c860acd9ae30dd705f183e226e530dde7066a82bcc.
  - C02: 21,163,035 bytes; SHA-256 a7062297e5311a67f607fb693597c4ecf963b97f83dacb911815bce40011f5a3.
- **Gameplay interpretation: target selection was not verified.** Both branches remained barrier_level_selection at F20/F60/F100/F110/F180. The prompt 「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya) stayed on screen; visual inspection found no new selected-target highlight or transition. LEFT caused a substantial composition/character-pose difference versus the no-input branch, but this is not evidence that a barrier was selected. Between C01 F60 and F100, only 22,741 pixels differed (MAE 0.74667); idle control C02 F60→F100 differed by 22,679 pixels (MAE 0.80236). The prompt ROI was pixel-identical between C01 F60/F100. Thus Circle produced no verified additional selection/state change after LEFT.
- Keep the adaptive policy at WAIT in barrier_level_selection; never infer selection from pose or screen movement. Revision62's marker has been consumed and must not be rerun. Story Mode completion remains unverified and is not a readiness acceptance criterion.

Next bounded work should discover an authentic target-selection indicator or a different calibrated direction using a fresh matched A/B from a validated parent checkpoint. Add regression coverage before each new probe and keep all game assets, savestates, Memory Cards, and gameplay screenshots in private Actions artifacts only.

## Adaptive player readiness update — Revision63 UP vs WAIT (23 October 2026)

**Readiness remains NO-GO.** This was a short qualified input experiment, not a Story Mode completion run. The barrier-selection target is still unidentified.

- Regression [#39939979616](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39939979616) passed 18 tests and the existing authenticity/policy checks. Revision63 player run [#39942178665](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39942178665) completed success; private evidence artifact #12496637328 was audited.
- Immutable parent checkpoint was Revision59 run #39907655833, `adaptive-cycle-02-f180.sstate`, 21,162,799 bytes, PCSX-Redux SaveState v4, SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`. Its validated staged source remained unchanged.
- Matched A/B gates passed: same initial state `barrier_level_selection`, F20 images identical across 1,024,000 pixels, identical Memory Card clones (SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5)), two fresh emulator processes and explicit `ExecutionFlow::SaveStateLoaded` in each. C01 sent exactly UP at F30 and released it at F38 with true/false readback; C02 sent no input. All ten authentic external-X11 captures passed 1280×800/image validation.
- Output checkpoints passed size/header/SHA validation:
  - C01: 21,163,397 bytes; header `PCSX-Redux SaveState v4`; SHA-256 `5557188cfa2ce12a70030b8bd650c181a2172f2934185290eb7352faa9754e40`.
  - C02: 21,163,426 bytes; header `PCSX-Redux SaveState v4`; SHA-256 `80782b47cf17e8d5bdc414af468c63eb098916c50235f98c092a676cca53b71e`.
  The harness recorded recovered/accepted shutdowns (native exits 139 and 124) only after its session-finished marker/checkpoint validation; don't interpret those codes alone as gameplay success.
- Visual conclusion: UP caused a large reproducible view/scene-composition change by F60, exposing additional coloured map markers including “60”. However the prompt `「レベルアップする結界をえらんでください」` (Pilih penghalang yang akan dinaikkan levelnya) persisted in all observations. The classifier stayed `barrier_level_selection`; no confirmed target highlight or committed selection was observed. From F60 to F100, the instruction and footer regions were exactly pixel-identical; action-frame changes (27,531 pixels, MAE 0.97250) were close to idle control changes (22,679 pixels, MAE 0.80236). Thus UP is a verified input/view response, **not** proof of target selection. Keep normal policy at WAIT in this state.
- **Next experiment candidate:** after adding strict workflow allowlisting and regression coverage, compare UP-at-F30/F38 followed by Circle-at-F70/F78 against a zero-input control, from the same validated Revision59 parent. Re-observe F60 before authorizing Circle and abort on dialogue/unknown state. The current workflow only supports the already-consumed LEFT_THEN_CIRCLE sequence; do not set a new marker for UP_THEN_CIRCLE until the protocol and tests explicitly support it.

All ROM/BIOS/Memory Card/savestate/screenshots remain in private Actions artifacts, never Git. Revision63's marker is consumed and must not be rerun. Story Mode completion remains unverified and is not a readiness prerequisite.


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

**Preflight decision:** allow exactly one Revision64 A/B run with the marker tuple specified in the handoff. Readiness remains **NO-GO** pending actual Revision64 runtime and visual evidence.
 
## Revision64 runtime audit — 23 October 2026

Run [#39946344909](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39946344909) failed in the adaptive loop after the private artifact upload succeeded; private artifact #12498880615 is available. This is a harness timeout failure, **not** an F60 safety-gate rejection.

- The immutable Revision59 source was re-verified at SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`. Both fresh emulator processes logged `ExecutionFlow::SaveStateLoaded`; their F20 images were identical across 1,024,000 pixels. Memory Card clones matched SHA-256 `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- C01 classified F20 and F60 as `barrier_level_selection` / `WAIT`; the F60 authorization gate passed. C01 sent exactly UP at F30/released F38 and Circle at F70/released F78, with successful true/false readbacks. The C02 control branch sent zero input through F110.
- C01 reached F180 and its checkpoint passed external validation: `adaptive-cycle-01-f180.sstate`, 21,163,031 bytes, header `PCSX-Redux SaveState v4`, SHA-256 `35cb550a62732cc6ed757e21914b46c1c0f1b2266182e2ea7761a6d401046014`. **Do not promote this checkpoint**: it has not been independently restored.
- The private artifact has only nine authentic 1280×800 external-X11 screenshots: C01 F20/F60/F100/F110/F180 and C02 F20/F60/F100/F110. C02's emulator hit the 60-second wrapper timeout (exit 124) at F110, so C02 F180 and its output checkpoint are missing. The orchestrator reported `ADAPTIVE_ORCHESTRATOR_EARLY_EXIT missing=['C02-F180'] checkpoints=1/2` and the job failed with exit code 92. Full A/B acceptance therefore failed.
- At C01 F60/F100/F180, `「レベルアップする結界をえらんでください」 (Pilih penghalang yang akan dinaikkan levelnya)` remained visible. From C01 F60 to F100, the instruction-panel ROI (x=140..685,y=565..715) and footer ROI (x=660..1130,y=685..770) each had zero differing pixels; both corresponding control ROIs were also stable. Whole-screen action/control differences mostly reflect the UP-induced view composition change and are not evidence that a target was selected. **Target/confirmation semantics remain UNKNOWN.**
- Required repair: increase only the per-emulator wrapper timeout from 60 to 90 seconds. Keep the Actions job capped at 20 minutes, preserve all shell/Lua allowlists and the F60 fail-closed gate, and add a source regression that verifies this bounded timeout. Do not launch the next player run until the resulting regression workflow is independently verified green. Revision64 is consumed; never rerun it. Use a fresh Revision65 marker against the same immutable Revision59 source only after regression passes.

Readiness remains **NO-GO**. Story Mode completion has not been proved and is not this qualification test's acceptance criterion. ROM, BIOS, Memory Card, savestates, and screenshots remain private and out of Git.

**Next step:** make the bounded timeout-only repair and prove it through CI before preparing Revision65.

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

**Next research direction:** inspect actual map/barrier selection indicators and existing controller-path evidence before another input experiment; do not cycle directions blindly.


### Follow-up chain containment details

- Raw restore-chain run [#39977472612](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39977472612) was triggered because the old `workflow_run` condition excluded `cancelled` but mistakenly accepted `skipped`. It failed at `Download raw checkpoint evidence from the source run`; the run was cancelled before emulator restore/continuation. Its follow-up [#39977746401](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39977746401) was `skipped`.
- `.github/workflows/naruto-raw-storymode-restore.yml` now has `if: false` and `concurrency.cancel-in-progress: true`; the legacy Story Mode playthrough `.github/workflows/naruto-scph7502-gpu-traffic-summary.yml` is `if: false` and therefore cannot be run by push or manual dispatch while the target/readiness gate is NO-GO.
- The 11 identified diagnostic jobs whose scripts contain fixed keyboard/controller tests are manual-dispatch-only (`if: github.event_name == 'workflow_dispatch'`). Their replacement runs from the guard commits completed `skipped`. Run #39978029528 is the regression for the guard source test and remained `in_progress` at this update; no additional workflow runs were active.

## Static reverse-engineering progress — 27 October 2026 (Langkah 4–5 selesai; Langkah 6 berjalan)

- Batas repo dipatuhi: hanya naruto-shinobi-jintori-research diakses/diubah. Tidak ada emulator, boot game, atau input gameplay.
- Langkah 4 selesai pada cakupan statis executable utama. Run [#40439763833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40439763833) sukses. Rutinitas LCG, empat pemanggil langsung, pembentukan/penyisipan/pengacakan daftar byte, serta pemeriksaan kandidat berbasis bitset sudah ditelusuri. Seed runtime dan arti gameplay ID tetap UNKNOWN. Laporan: [docs/STEP4_RNG_TRACE_2026-10-27.md](docs/STEP4_RNG_TRACE_2026-10-27.md).
- Langkah 5 selesai sebagai analisis statis awal DATA.BIN entry 1: offset 0x10BB000, 596.412 byte, SHA-256 potongan 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a. Ghidra dengan base hipotesis 0x800D0000 menemukan enam lokasi yang memanggil getter target Chakra 0x80012A70 dan melakukan pembandingan field record/target. Base runtime belum tervalidasi. Laporan: [docs/STEP5_DATABIN_ENTRY1_ANALYSIS_2026-10-27.md](docs/STEP5_DATABIN_ENTRY1_ANALYSIS_2026-10-27.md).
- Langkah 6 disiapkan: dekompilasi pemanggil tambahan getter target, transisi FUN_800EF98C/FUN_80100D14/FUN_80100DCC, jalur pembanding gagal, serta konsumen setter Chakra. Workflow run terbaru [#40440237256](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40440237256) baru berstatus queued saat catatan ini ditulis.
- Artefak Ghidra yang berhasil berisi teks saja (fungsi TSV/log/dekompilasi); BIN, DATA.BIN, entry resource, BIOS, savestate, Memory Card, dan screenshot privat tidak diunggah atau di-commit.
- Gerbang pemain adaptif tetap fail-closed: target cue UNKNOWN; barrier_level_selection = WAIT; readiness NO-GO; Story Mode NOT COMPLETE; marker Revision65 tetap tidak disentuh.


## Reverse engineering Langkah 4–10 — checkpoint evidence 27 Oktober 2026

Laporan penutupan kriteria dan evidence matrix: [docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md](docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md). Handoff langsung untuk kelanjutan: [docs/HANDOFF_REVERSE_ENGINEERING_STEPS4_10_2026-10-27.md](docs/HANDOFF_REVERSE_ENGINEERING_STEPS4_10_2026-10-27.md).

Status yang didukung bukti:
- **Step 4 — SEBAGIAN (overall).** Runtime run #40474262267 memakai tiga cabang dari checkpoint roulette yang sama, input readback PASS, masing-masing 127 panggilan RNG, state akhir 0xA99DC6E7; urutan sequence/caller/state-before cocok setelah nomor VSync dinormalisasi, dan normalized viewport crop SHA-256 sama. Capture autentik X11 diperiksa; frame event 169/167/171 berbeda. Sumber seed saat boot, caller battle, hubungan kausal ke hasil roulette, indirect dispatch menyeluruh dan RNG alternatif tetap UNKNOWN. Laporan runtime: [out/step4/STEP4_RNG_RUNTIME_RESULT_2026-10-27.md](out/step4/STEP4_RNG_RUNTIME_RESULT_2026-10-27.md). Job Actions keseluruhan gagal hanya di penulisan ringkasan via API; data rekonstruksi berasal dari raw log/artifact #12719024236.
- **Step 5 — TUNTAS untuk empat fungsi terpilih.** Empat pasangan Ghidra/m2c C outputs telah tersimpan; jangan ulang tanpa pertanyaan baru.
- **Step 6 — SEBAGIAN.** Xref getter/setter, kandidat transisi, dan batas semantik terdokumentasi dalam [docs/STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md](docs/STEP6_TARGET_XREF_SEMANTIC_REVIEW_2026-10-27.md); base runtime/field/delta semantics tetap UNKNOWN.
- **Step 7 — SEBAGIAN.** Direktori DATA.BIN dan kandidat bootstrap-copy didukung analisis statis. Workflow cold-boot runner-only #40475950842 sedang memeriksa kandidat copy 0x800AD454/0x800AD45C dan RNG seed-setter 0x80035DA8; tanpa save-state restore/input. Status hasilnya belum boleh dinaikkan hingga log/artifact/cleanup diverifikasi.
- **Step 8 — SEBAGIAN.** Fungsi yang semantiknya didukung kode dijelaskan; aturan umum barrier/cost/battle/roulette/turn belum terbukti. [docs/STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md](docs/STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md).
- **Step 9 — TUNTAS untuk fungsi RNG utama 0x80035D78 saja.** Run #40474891838 sukses: 7/7 state vectors, state baru/v0 tepat, 12 instruksi per vector, physical RAM map valid, runner-private cleanup PASS. Ini bukan emulator PS1 penuh. [out/step9/STEP9_UNICORN_RESULT_2026-10-27.md](out/step9/STEP9_UNICORN_RESULT_2026-10-27.md).
- **Step 10 — TUNTAS sebagai indeks audit.** [out/logic.md](out/logic.md) menunjuk evidence/report mutakhir; ini tidak berarti semua logika game sudah direverse-engineer.

HEAD riset saat catatan ini disiapkan: `1076072f69d83546ecf70923e26304e7af4ac057`; perubahan status ini sendiri akan menghasilkan commit baru. Setelah cold-boot selesai, perbarui status Step 7 dan SHA HEAD secara berurutan.

Story Mode: **TIDAK TERBUKTI TAMAT**. Tidak ada ending autentik pada riset ini. Pengembangan pemain adaptif tetap dijeda; tidak ada classifier, kebijakan input, marker Revision65, atau readiness gate yang diubah. Disc/ROM, BIOS, Memory Card, savestate, RAM dump dan screenshot gameplay privat tidak di-commit ke Git.

## Checkpoint audit tambahan — 27 Oktober 2026

HEAD remote yang diperiksa sebelum entri ini: 52f077114c01de00cac52527af92e38a1d4a1e3e. Status local working tree tidak dapat diperiksa melalui konektor GitHub; tidak ada klaim bersih/kotor.

Bukti baru yang dapat ditautkan: review runner-only [#40473737136](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40473737136), artifact teks #12719587873, ZIP SHA-256 e1ea68c92bcbf645fde3c991c8a47192b815987d8044f2d599c163c1f3ec9fb9. Raw MIPS terpilih memperjelas cabang target-gated pada enam site entry 1 dan urutan negasi/clamp/store pada 0x8011C0D0, dengan base 0x800D0000 yang masih HIPOTESIS. Tidak ada run game atau input di pekerjaan ini.

Status akhir per ruang lingkup: Step 4 SEBAGIAN (seed caller return dan lifecycle masih UNKNOWN); Step 5 TUNTAS untuk empat fungsi terpilih; Step 6 SEBAGIAN (operand/branch/delay slot terpilih sekarang terdokumentasi; field pending/runtime base/transition semantics belum lengkap); Step 7 SEBAGIAN (no-hit bounded bukan bukti loader/base); Step 8 SEBAGIAN (aturan permainan belum dibuktikan); Step 9 TUNTAS untuk RNG 0x80035D78 saja; Step 10 TUNTAS sebagai indeks audit. Step 4 correction terbaru: 0x800AF2AC memasukkan return helper 0x80037138 melalui move a0,v0; -1 adalah input helper. Tidak ada bukti Story Mode tamat.

Tidak ada aksi pemain adaptif, restore savestate atau input gameplay dilakukan. Jangan ulangi eksperimen roulette #40474262267, breakpoint tunggal 0x800AD454 (#40484548650), atau seed kandidat 0x80035DA8 (#40485987817) tanpa hipotesis teknis baru.

## Checkpoint addendum — Step 6 dataflow detail (27 Oktober 2026)

The existing runner-only Step 6 artifact also supports a more specific decompiler trace for candidate 0x8011C0D0 on hypothetical entry-1 base 0x800D0000: byte-masked input compared with global 0x80139F70, early return if unchanged, global and field +0x618 update if changed; nonzero path writes 8 to selected record +0x22 and loops participant records with stride 0x90. Each word +0x04 is negated, clamped to minimum -9999, stored, and passed into setter 0x8001387C alongside index. Short/ushort sum +0x10/+0x14 versus 0x101 gates call to 0x8003F5D0 or alternate byte store +0x94A=1; 0x800F96A4 occurs on certain paths. This is decompilation of a 408-byte function body; full raw instruction loop was not archived. It does not establish cost semantics.

Step 6/8 remain SEBAGIAN; stores of +0x2E9/+0x2E5 were observed but meanings stay UNKNOWN; +0xB30/+0xB38/+0xB40/+0xB44 still need whole-program instruction-level access analysis. No runtime, adaptive player, savestate or gameplay input was used.


## Live Actions / handoff sync — 27 Oktober 2026 17:26 WIB

Remote `main` before this status update: `e128fe86da6dbd3848813a376aa5b63f53e39977` (handoff refresh). Run [#40487406384](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40487406384) is still `in_progress`; job `122132544196`, step “Extract and analyze DATA.BIN entry 0 for external helper” is running. Main EXE and entry 1 steps completed; artifact upload and cleanup have not completed; no artifact was available at this check. No ETA is reliable; a prior full Ghidra run took ~39m43s only as a rough historical comparison. No queued run was found in the latest run list.

The current Step 6 evidence remains static/decompiler-only for `0x8011C0D0`; it does not prove gameplay-cost semantics. `+0xB30/+0xB38/+0xB40/+0xB44` remain untraced across the whole program. Do not repeat no-hit probes #40484548650 or #40485987817 without a different technical hypothesis. Statuses unchanged: Step 4 partial, Step 5 complete only for four selected functions, Step 6 partial, Step 7 partial, Step 8 partial, Step 9 complete only for `0x80035D78`, Step 10 complete as audit index only. Story Mode not verified complete.

## Live audit checkpoint — 27 October 2026, 17:24 WIB

- Re-read the live `main` files and verified that the current commit before this checkpoint was `2ad2c8dcdcaeee718d656e8696d6853f48ec54a8`. GitHub connector does not expose a local working-tree status; no local clean/dirty claim is made.
- Re-fetched raw job logs and metadata for Step 7 run [#40484548650](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650). Job `coldboot-loader` completed `success`; asset provenance in the log confirms disc label/ID `SLPS-03553 / SLPS03553` and BIOS `SCPH-7502 (EU)`. The observation logs show preflight frame 50, listener-only control max frame 60, target `0x800AD454` progress through frame 120 with `bp_hits=0`, and bounded timeout `124`. The report artifact is #12724961702, 3,960 bytes, digest `sha256:27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71`; raw job log explicitly confirms upload digest and `STEP7_PRIVATE_CLEANUP=PASS`. No breakpoint hit or register/copy-size/buffer-checksum evidence exists. The result remains a bounded no-hit, not proof the loader is absent or its base is known.
- Step 9 criteria/report review confirms the isolated-execution criterion is satisfied only for `0x80035D78`: 7/7 vectors, state and `v0` correct, sentinel return in 12 instructions, max bound 128, physical 2 MiB RAM alias. The criterion does not require an indiscriminate all-functions sweep; no extra probe is justified absent a specific new claim.
- Active Actions run: [#40487406384](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40487406384), job `Verify and analyze PS-X EXE` / `122132544196`, step 11 `Extract and analyze DATA.BIN entry 0 for external helper` is `in_progress`. It began 17:18:13 WIB. The prior comparable full Ghidra run took about 39m43s, so an indicative finish is around 17:58 WIB, not a guarantee. Do not launch overlapping diagnostic work; inspect final logs/artifact after this run completes.
- No adaptive-player/Story Mode workflow, gameplay input, savestate restore, classifier/policy/readiness-gate edit, or private asset commit was performed. Story Mode remains `TIDAK TERBUKTI TAMAT`. Remaining Steps 4, 6, 7, and 8 stay partial; Step 5 remains complete only for four selected functions; Step 9 only for the RNG routine; Step 10 is an index, not proof of complete game understanding.

## Checkpoint tambahan — return helper dan field memory operand, 27 Oktober 2026 (bukti runner sampai 18:38 WIB)

Audit runner-only terbaru [#40497668341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40497668341) selesai `success` pada **18:38:45 WIB**. Artefak teks #12730957210 berukuran **9.014 byte**, ZIP SHA-256 `695e36bf70237913c0f80c94f0d4100732c92dd8b78155da2ace90d189c5ee24`; raw log mencatat `RUNNER_ARTIFACT_CLEANUP=PASS`. Audit memvalidasi metadata/digest lalu memeriksa di runner Ghidra artifact #12728867894 dan hasil pemindaian Step 6 terbaru #12729156734. Tidak ada biner game/BIOS atau screenshot privat yang diunggah.

### Langkah 4 — return helper
Output disassembly mentah dari fungsi main EXE `0x80037138` memiliki body 376 byte/94 instruksi. Callsite kandidat pada DATA.BIN entry 0 menjalankan `jal 0x80037138` dengan delay slot `li a0,-1`; untuk input negatif, fungsi helper masuk ke cabang `param_1 < 0`, membaca global `0x80066E7C` (`lui v0,0x8006; lw v0,0x6e7c(v0)`), lalu mengembalikan nilai tersebut. Delay slot setter berikutnya `move a0,v0` meneruskan return helper ke kandidat setter `0x80035DA8`. Jadi argumen setter **bukan konstanta -1**; sumber statis pada jalur ini adalah global `0x80066E7C`. Nilai global saat boot, callsite reachability runtime, dan lifecycle seed tetap UNKNOWN. Dasar alamat entry 0 `0x800AD000` tetap HIPOTESIS.

Percobaan audit helper sebelumnya [#40493608676](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40493608676) gagal di validasi target, bukan karena bukti disassembly tidak ada: teks Ghidra menulis marker `=== TARGET 80037138 ===` / `=== TARGET 80035da8 ===` tanpa prefiks `0x`, sementara pemeriksaan semula mengharuskan prefiks tersebut. Artefak #12730020903 berukuran 8.395 byte, ZIP SHA-256 `00b54f4e8c059f81d0f4d75aea04f2deccece564edff73378096b369e4fd7c79`; raw log cleanup PASS. File workflow juga mempunyai fragmen duplikat sesudah penutup YAML; fragmen itu telah dibuang pada commit `029fdfab8df55dd16001916f0f53b7abd073c334`. Run koreksi #40497723766 sedang berjalan pada snapshot 18:39 WIB saat checkpoint ini dicatat; belum ada hasil final pada pembaruan ini.

### Langkah 6 — field memory operand
Scan #40493556711 (#12729156734, 180.128 byte, ZIP SHA-256 `c9ea5ef0552a0c80a70f0d3a758622a358509de2079e5954dac3ce0032426e93`) memperlihatkan:
- `0x8012C634 lw v0,0xB30(a0)`; `0x8012C638 lw v1,0xB38(a0)`; `0x8012C640 addu v0,v0,v1`; `0x8012C644 sw v0,0xB40(a0)`.
- `0x8012C604 sw zero,0xB44(v0)` di delay slot JAL pada jalur reset/inisialisasi kandidat.
- `0x8012CB14 lw a2,0xB44(v1)`, lalu `jal 0x8001B364` dengan `a3=5` pada delay slot.

Konteks di sekitar akses mencakup delapan instruksi sebelum dan sesudah hit dan byte instruksi mentah. Hubungan aritmetika `+0xB30/+0xB38 -> +0xB40` TERVERIFIKASI-STATIS pada peta entry-1 hipotetis `0x800D0000`; field semantics, alias/object identity, seluruh writer di luar cakupan decode, dan mapping runtime belum terbukti.

Status keseluruhan tidak berubah: Step 4/6/7/8 SEBAGIAN; Step 5 TUNTAS hanya untuk empat fungsi terpilih; Step 9 TUNTAS hanya untuk RNG `0x80035D78`; Step 10 TUNTAS sebagai indeks audit. Story Mode TIDAK TERBUKTI TAMAT; tidak ada gameplay/emulator yang dijalankan pada audit statis ini.

## Checkpoint tambahan — xref global return helper (27 Oktober 2026, 18:44 WIB)

Run helper statis [#40498231825](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498231825) selesai success pada 18:43:58 WIB. Artefak teks #12732006381 berukuran 9.058 byte, ZIP SHA-256 adfdb608af96dd95a7c7e74d9f8b117767aaffa817d0c7eb860757ead868d9ba; raw log mencatat STEP4_HELPER_PRIVATE_CLEANUP=PASS, text_only_output_validation=PASS, dan uploaded_input_executable=no. Pemeriksaan marker telah diperbaiki dengan case-insensitive grep. Target setter 0x80035DA8 masih tidak dikenali sebagai instruction/function oleh ExportFunctionDetail; runtime_call_contract tetap NOT_PROVEN.

Audit runner-only [#40498386273](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498386273) success pada 18:44:35 WIB, artifact #12731327556 berukuran 9.727 byte, ZIP SHA-256 7826480f41372d68ddf3f4b1dfe6d99f51bbbb5cd124eb5c3c6169870150ba5c; raw log RUNNER_ARTIFACT_CLEANUP=PASS. Metadata, nama, run ID, ukuran, expiration dan digest artifact #12732006381 diverifikasi; artefak dianalisis di runner saja.

Penelusuran langsung referensi global 0x80066E7C menghasilkan 8 referensi pada executable utama (6 READ, 2 WRITE pada listing Ghidra). Byte awal dalam image executable pada alamat itu adalah 00 00 00 00, nilai word little-endian 0; ini nilai image sebelum runtime, bukan bukti nilai saat callsite berjalan. Dua writer yang terdeteksi: 0x80037B7C, sw zero,0x6e7c(at) dalam fungsi kandidat 0x80037B58; dan 0x80037BDC, sw v0,0x6e7c(at) di fungsi 0x80037BB0, setelah addiu v0,v0,1 di 0x80037BD4. Fungsi 0x80037BB0 juga membaca nilai global pada 0x80037BB4. Fungsi helper 0x80037138 membaca global di 0x8003719C, 0x80037204, dan 0x80037260; fungsi lain 0x800372B0 membaca pada 0x800372C0 dan 0x80037324. Ini mendukung hipotesis nilai global bersifat counter-like, tetapi label semantik, urutan initializer/caller, dan nilai ketika candidate setter dipanggil belum dibuktikan.

Status Step 4 masih SEBAGIAN: sumber return statis untuk input -1 sekarang terpetakan ke global 0x80066E7C, tetapi siklus hidup global dan runtime reachability tetap terbuka. Step 6 tetap SEBAGIAN; Step 7 tetap SEBAGIAN; Step 8 tetap SEBAGIAN. Step 5 dan Step 9 dipertahankan pada cakupan penutupan yang ada, Step 10 hanya indeks audit. Story Mode TIDAK TERBUKTI TAMAT.

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


<!-- step4-step8-preset-list-shuffle-audit-2026-10-28 -->
## CURRENT ADDENDUM — preset-list loading and shuffle helper, 28 Oktober 2026

New static trace: [`docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md`](docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md), commit `1c895b015894ecce9e536c9c2a36f1ad2b2f75ba`. Based on raw MIPS/Ghidra/m2c output from Actions artifact [#12739676233](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524/artifacts/12739676233): function `0x80015610` accepts index 0–17 and copies two 64-byte source blocks to `0x80070D0A` and `+0x40), storing lengths/cursors. The two source blocks match byte-for-byte for each index. For indices 0–8, first `0xFF` positions are 51,55,59,57,61,62,62,62,11; indices 9–17 are 64 zero bytes without a sentinel and therefore statically counted as length 64.

The shuffle helper `0x80015B7C` overwrites incoming `a0` with zero at `0x80015B9C`, reads only count `0x80070D02`, and performs `4*n` swaps in the first buffer. Thus the two calls from `0x80015610` for group 0 and 1 both target the first list; this is a static fact, not yet a proven gameplay bug. The semantics of each byte ID and the intended role of the second buffer remain UNKNOWN. See the linked trace for exact addresses and limitations.

### Emulator checkpoint restore diagnostic — 28 Oktober 2026

No-input restore attempts [#40613996374](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40613996374) (raw state) and [#40614208610](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40614208610) (sanitized state with BIOS reinserted) both exited 139 with `SIGSEGV` immediately after `RESTORE_LOAD_BEGIN`; the loader call returned neither success nor a `SaveStateLoaded` event. Rehydrated bytes hash exactly to raw-source hash `00fab826…f6c3d`, so this was not an alternate byte representation that independently solved restore. Stop repeated restore tests on this checkpoint unless a new loader/state-format hypothesis is introduced. No buttons were sent. This does not change the rule inventory or prove Story Mode completion.


## CURRENT ADDENDUM — descriptor selector cross-check (28 Oktober 2026)

Cross-check baru pada dua tabel yang mengirim argumen ke `0x80015610`: `0x80064918` (stride `0x30`) menghasilkan selector `[0,1,2,3,4,5,6,7,4,4,4,4,4,4,4,5,8,8]`; `0x80057798` (stride `0x54`) menghasilkan `[0,1,2,8,3,4,8,5,6,6,0,0,0,0,0,0,3,5]`. Keduanya terbatas pada selector 0–8. Dengan demikian, blok selector 9–17 yang berisi 64 byte nol tidak dipilih oleh dua jalur descriptor langsung yang diidentifikasi; ini bukan bukti bahwa seluruh jalur tak langsung/seluruh game tidak pernah memakai indeks tersebut. Pembaruan rinci: [`docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md`](docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md), commit `58340592751b84b7b85ba5cb42185063204a9ec9`.


<!-- caller-id-random-insert-audit-2026-10-28 -->
## CURRENT ADDENDUM — ID source → RNG position → list mutation (28 Oktober 2026)

Raw main-EXE evidence in artifact #12739676233 shows the only direct JAL site found for `0x80015ADC` at `0x80013B50`. In the same local sequence, `0x800139FC(group,slot)` reads a byte at offset +0x0A from a `0x80070EA0)-based record after checks `group<4` and `slot<3`; that byte becomes the ID passed to `0x80015ADC`. The ID is checked against a 52-entry registry (sentinel at `0x8005602C); then the helper computes `floor(n/2)+(RNG mod floor(n/2))`, with `n=byte[0x80070D02]`. For a valid position, `0x800159BC` shifts bytes in `0x80070D0A) right, stores the ID at `0x80070C80+0x8A+position`, and increments a separate halfword `0x80070C82` if below 64. The insertion helper does not increment `0x80070D02`; do not merge these as one size counter.

Detailed trace and caveats: [`docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md`](docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md), latest trace commit `8f78358fc7ce9b8753e95b40ed57d7e344214600`. These are **static code operations**, not a verified item/card/turn rule or runtime observation. Step 4 remains SEBAGIAN; Step 8(a) SEBAGIAN and Step 8(b) UNKNOWN. The savestate loader failure gate remains closed after two identical exit-139 failures; no buttons were sent.


<!-- four-record-three-slot-id-operations-2026-10-28 -->
## CURRENT ADDENDUM — four records, three IDs each, and remove/compact behavior (28 Oktober 2026)

Further raw-MIPS trace in [`docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md`](docs/STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md), latest commit `57be85c59ad6e81e608962ed0ca27472eb6d8dac`: code uses four indexed records based at `0x80070EA0), stride `0xB4), with three adjacent ID bytes at offsets `+0x0A..+0x0C`. The code body at `0x80013A48` validates a new ID against a 52-entry registry and fills the first record slot whose value is not a valid ID; fails if all three slots hold valid IDs. Body `0x80013B10` reads an ID from a selected slot, calls the RNG-position insertion path, compacts subsequent IDs left for source slot 0 or 1, and marks the third slot `0xFF`. This is static evidence for a three-slot add/remove/transfer mechanism, not a confirmed card/character/upgrade label.

Together with the previously traced insertion helper, the code chooses a pseudo-random insertion index from configured list length `0x80070D02`, shifts companion order bytes at `0x80070D0A`, writes the candidate ID to `0x80070C80+0x8A+position`, and separately increments/decrements `0x80070C82`. Do not equate the two lengths/counters. Step 4 and Step 8(a) remain SEBAGIAN; Step 8(b) gameplay label remains UNKNOWN pending runtime/state-result corroboration.
