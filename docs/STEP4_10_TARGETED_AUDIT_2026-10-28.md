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

# Audit Terarah Lanjutan — Langkah 4–10

Tanggal: 28 Oktober 2026  
Checkpoint awal yang diverifikasi: `4b20564b38c895495755143b2aa777dc7ab6b5e5` pada `main`  
Cakupan: pemeriksaan langsung dua artefak teks Actions dan cross-check terhadap laporan/handoff. Ini bukan run emulator, bukan tes gameplay, dan bukan pengembangan pemain adaptif.

## Keputusan

Bukti statis baru memperjelas batas cakupan, tetapi **tidak menutup kriteria teknis Langkah 4–9**. Status tetap konservatif. Langkah 10 tetap tuntas hanya sebagai matriks audit. Story Mode **TIDAK TERBUKTI TAMAT**.

Actions live query untuk `status=queued` mengembalikan `total_count=0`; `status=in_progress` juga `total_count=0`. Tidak ada run aktif yang perlu ditunggu. Run #40606159061 adalah tes MIPS terisolasi dan selesai sukses, bukan run gameplay.

## Sumber yang benar-benar dibuka

| Artefak | Identitas dan pemeriksaan | Hasil yang didukung |
|---|---|---|
| Step 5, run [#40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524), artifact [#12739676233](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524/artifacts/12739676233) | ZIP 941.176 byte; SHA-256 `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d`. Berisi 45 file keluaran teks/C/disassembly/log. Hash ZIP dihitung ulang dan cocok. Executable teridentifikasi sebagai `SLPS_035.53`, 385.024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`. | Main-text disassembly dan laporan caller diperiksa langsung; tidak ada biner game dimasukkan ke laporan publik ini. |
| Step 6, run [#40522772847](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40522772847), artifact [#12741234990](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40522772847/artifacts/12741234990) | ZIP 234.210 byte; SHA-256 `7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9`. Hash ZIP dihitung ulang dan cocok; keluaran hanya teks/log. | Scan 98.357 instruksi terdekode pada view DATA.BIN entry-1 dengan base `0x800D0000` yang tetap HIPOTESIS; CFG/SSA atas dua fungsi dibuka. |
| Step 9, run [#40606159061](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40606159061), artifact [#12779814671](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40606159061/artifacts/12779814671) | Laporan #12779814671 sudah dibuka dan identitas/checksum ZIP cocok dengan laporan silang; tes dan cleanup tercatat PASS. | RNG 7/7, helper `a0<0` 8/8, accessor setter/getter 16/16 hanya pada CPU/MIPS terisolasi; MMIO synthetic word `0x12345678`. Artefak ini bukan bukti hardware/gameplay PS1. |

### Langkah 4 — inventaris direct dan indirect call (cakupan terbatas)

Full disassembly main EXE yang ada di artefak Step 5 diperiksa. Tepat empat instruksi direct `JAL` menuju rutin RNG `0x80035D78` ditemukan dalam rentang main EXE:
- `0x80015B14` dalam kandidat body `0x80015ADC`.
- `0x80015BF0` di kawasan code berlabel `0x80015B7C`.
- `0x8001A460` dalam kandidat body `0x8001A328`.
- `0x80020C24` dalam kandidat body `0x80020BF4`.

Disassembly juga berisi **156 mnemonic `JALR`**. Jumlah ini hanya inventory instruksi register-indirect pada text main EXE, bukan jumlah callee unik; target dinamis, register provenance, runtime reachability, resource caller, dan kode decompressed/runtime belum ditutup. Tidak ditemukan direct `JAL` di main EXE ke kandidat setter `0x80035DA8` dalam scan ini. Tidak ada kesimpulan universal bahwa tidak ada jalur lain.

**Catatan batas fungsi perlu direkonsiliasi:** laporan Ghidra/m2c menetapkan `FUN_80015B7C` sebagai body 240 alamat, dari `0x80015B7C` sampai end-exclusive `0x80015C6C`. Disassembly spimdisasm pada artefak yang sama memberi anotasi `nonmatching func_80015B7C, 0x580`, memuat label tambahan `glabel func_80015c6c`, dan menutup label panjang itu di kawasan `0x800160FC`. Instruksi JAL RNG berada pada `0x80015BF0`, sehingga lokasi panggilan terlihat dan terdekode; namun span anotasi spimdisasm tidak boleh diperlakukan otomatis sebagai satu fungsi Ghidra yang batasnya tervalidasi. Kriteria Step 5 dan caller-boundary Step 4 tetap SEBAGIAN sampai sumber batas tersebut direkonsiliasi secara eksplisit. Deskripsi lokal atas caller ini harus tetap terbatas pada operasi yang ditunjukkan instruksi.

Operasi lokal yang didukung kode statis:
- `0x80015ADC`: menghitung argumen bounded dengan `RNG % divisor` setelah guard divisor tidak nol.
- `0x80015B7C` sekitar `0x80015BF0`: pada `n != 0`, jalur lokal mengambil indeks `RNG % n` dan menukar byte dalam buffer `0x80070D0A`; fungsi dekompilasi Ghidra lokal melaporkan loop hingga `4*n`. Semantik buffer/gameplay tetap tidak diketahui, dan batas badan perlu rekonsiliasi di atas.
- `0x8001A328`: membentuk shortlist dari kandidat dasar 0 plus kandidat `1,2,3,4,5,8,9,11` berdasarkan delapan pemeriksaan kode `0x7F..0x86`; memilih `RNG % count` dan menulis byte ke `0x80089DA9`. Arti kode dan byte tujuan tidak diketahui.
- `0x80020BF4`: setelah null/flag guard lolos, menandai field objek, menghitung `RNG % 0x1000`, menyimpan ke offset `+0x34`, lalu memanggil helper lain. Identitas objek dan arti field tidak diketahui.

### Langkah 6 — tabel operand field (hanya view entry-1 hipotetis)

Artefak #12741234990 mencatat 98.357 instruksi Ghidra terdekode. Direct displacement census yang benar-benar muncul untuk field utama:

| Field relatif | Alamat/instruksi | Access | Makna yang boleh disimpulkan |
|---|---|---|---|
| `+0xB30` | `0x8012C634`, bytes `30 0B 82 8C`, `lw v0,0xB30(a0)` | 1 READ, 0 WRITE | Word dibaca oleh fungsi kandidat `0x8012C544`. |
| `+0xB38` | `0x8012C638`, bytes `38 0B 83 8C`, `lw v1,0xB38(a0)` | 1 READ, 0 WRITE | Word dibaca; nilainya ditambahkan ke nilai `+0xB30`. |
| `+0xB40` | `0x8012C644`, bytes `40 0B 82 AC`, `sw v0,0xB40(a0)` | 0 READ, 1 WRITE | Menerima hasil penjumlahan dua word tersebut. |
| `+0xB44` | `0x8012C604`, bytes `44 0B 40 AC`, `sw zero,0xB44(v0)`; `0x8012CB14`, bytes `44 0B 66 8C`, `lw a2,0xB44(v1)` | 1 READ, 1 WRITE | Di-zero-kan di fungsi pertama; dibaca di fungsi `0x8012CACC` untuk diteruskan sebagai argumen kepada `0x8001B364`. |

Fungsi `0x8012CACC` mencapai consumer `+0xB44` hanya ketika byte `+0xB2A > 5` (nilai minimal 6); call pada `0x8012CB18` meneruskan argumen tersebut ke `0x8001B364`. Jalur helper berujung pada operasi/tabel yang tampak seperti pemrosesan geometri/visual, namun ini hanya petunjuk implementasi statis, bukan penetapan makna gameplay.

Batas dataflow tetap tegas: pointer yang dipakai sebagai base berasal dari slot global `0x8013A554`, sedangkan nilai pointer runtime, alias lintas fungsi/cabang, store writer, split-immediate chain menyeluruh, alternate base, dan relocation belum dibuktikan. SSA output berhenti pada `NO_SSA_DEFINITION` / `DEPTH_LIMIT`; tool itu sendiri membatasi trace depth menjadi empat. Ini belum memenuhi 6(b).

### Status kriteria setelah audit terarah

| Kriteria | Status sebelum | Status kini | Bukti dan alasan belum tuntas | Langkah minimum berikut |
|---|---|---|---|---|
| 4(a) RNG state/seed lifecycle | SEBAGIAN | SEBAGIAN | Rumus dan vektor terisolasi ada; nilai seed dan urutan init runtime tidak ada. | Buktikan caller setter/helper dengan batas fungsi sah dan nilai register/state saat runtime. |
| 4(b) determinisme dan hasil yang terlihat | SEBAGIAN | SEBAGIAN | Sampel roulette historis hanya referensi dokumen; caller-to-outcome causality belum terbukti ulang dari state awal terkontrol. | Buktikan trace state/caller dan hasil aktual dalam eksperimen A/B berpasangan. |
| 4(c) direct/indirect callers | SEBAGIAN | SEBAGIAN | Empat direct JAL ditemukan pada main EXE; 156 JALR tercatat tetapi target dan resource path belum ditutup. Boundary 0x80015B7C perlu rekonsiliasi. | Resolve register targets, call boundaries, resource callers dan runtime reachability. |
| 4(d) roulette/battle | SEBAGIAN; battle BLOCKED | SEBAGIAN; battle BLOCKED | Korelasi historis belum membuktikan sebab-akibat; checkpoint battle/runtime yang bisa dipakai belum terverifikasi saat audit. | Gunakan checkpoint autentik yang tersedia dengan caller/state/outcome trace dan kontrol. |
| 4(e) sumber randomness alternatif | SEBAGIAN | SEBAGIAN | Text-only signature search tidak mengesampingkan tabel, frame/timer, algoritme lain atau kode resource runtime. | Lakukan sweep statis lintas image/resource dengan hasil false-positive dan cakupan jelas. |
| 5) Ghidra/m2c dan batas fungsi | SEBAGIAN | SEBAGIAN | 14 fungsi terpilih sudah dibandingkan, tetapi bukan seluruh fungsi/call graph; ditemukan boundary annotation berbeda pada `0x80015B7C`. | Validasi batas fungsi terhadap raw MIPS, delay-slot, return/tail-jump dan metadata di rentang yang sama. |
| 6(a) direct memory R/W census | SEBAGIAN | SEBAGIAN | Counts field di atas berasal dari 98.357 instruksi terdekode pada base hipotesis. | Perluas dengan effective-address/alias coverage dan dokumentasikan instruksi yang tidak terdekode. |
| 6(b) effective address/pointer/alias | BLOCKED | BLOCKED | Slot `0x8013A554`, alias dan store-writers lintas caller belum terselesaikan. | Gunakan CFG/dataflow engine yang dapat menelusuri pointer load/store lintas block/fungsi, lalu cocokkan raw MIPS/XREF. |
| 6(c) dataflow menuju semantik | SEBAGIAN | SEBAGIAN | Read-add-write dan consumer helper terbukti pada view statis, bukan state/gameplay result. | Hubungkan caller, writer dan hasil state/runtime independen. |
| 6(d) arti field | UNKNOWN | UNKNOWN | Tidak ada bukti independen untuk memberi nama gameplay kepada +B30/B38/B40/B44. | Tunggu bukti kode dan perubahan state autentik yang menguatkan. |
| 7(a) struktur loader/resource | SEBAGIAN | SEBAGIAN | Pemetaan direktori/copy statis parsial. | Lengkapi lifecycle/relocation setelah sumber salin statis yang jelas diidentifikasi. |
| 7(b) runtime mapping/copy | BLOCKED | BLOCKED | Probe lama 0x800AD454 tidak hit sampai frame 120; tidak ada source/destination/length/checksum runtime. | Pilih instruksi copy yang reachable dari bukti statis baru, baru rancang cold boot tanpa input. |
| 8(a) semantik operasi fungsi | SEBAGIAN | SEBAGIAN | Operasi terpilih jelas secara statis, identitas fitur tidak. | Lengkapi caller/callee dan koroborasi state/result yang tepat. |
| 8(b) aturan gameplay | UNKNOWN untuk label unsupported | UNKNOWN untuk label unsupported | Tidak terbukti biaya Chakra, barrier/level-up, cards, turn, roulette/battle atau victory/loss rules. | Satu aturan per eksperimen; kondisi → store/state → hasil, dengan bukti independen. |
| 9(a) tes RNG terisolasi | TUNTAS untuk 7 vektor saja | TUNTAS untuk 7 vektor saja | 7/7 dalam Unicorn, bukan PS1 hardware/gameplay. | Jangan ulang tanpa input oracle atau jalur baru. |
| 9(b) helper/accessor/breadth | SEBAGIAN | SEBAGIAN | Helper negatif-a0 8/8 dan setter/getter 16/16 dengan MMIO sintetis; belum semua fungsi/cabang. | Tambah hanya kasus dengan oracle spesifik dan gap nyata. |
| 10) matriks closure audit | TUNTAS sebagai matriks saja | TUNTAS sebagai matriks saja | Status, bukti, gap telah dipetakan; bukan closure teknis Steps 4–9. | Sinkronkan snapshot ini ke laporan utama/status/handoff setiap perubahan bukti. |

## Batas runtime dan privasi

Tidak ada emulator/gameplay dijalankan dalam sesi audit ini; tidak ada tombol gameplay dikirim dan tidak ada savestate yang dipulihkan. Artefak historis gameplay/savestate hanya disebut jika ada catatan; file mentahnya tidak diasumsikan tersedia atau sudah diverifikasi hanya dari nama/hash lama. Tidak ada ROM/BIN/CUE/EXE, BIOS, Memory Card, savestate, RAM dump, atau screenshot privat ditambahkan ke laporan/artifact. Tidak ada workflow adaptive-player dijalankan atau diedit.

Story Mode tetap **TIDAK TERBUKTI TAMAT**. Adaptive readiness tetap **NO-GO**; target cue tetap **UNKNOWN** dan `barrier_level_selection=WAIT`.


<!-- step4-step8-preset-list-shuffle-audit-2026-10-28 -->
## Additional Step 4/8 evidence — preset list loading

A new static trace is recorded in [`STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md`](STEP4_8_PRESET_LIST_SHUFFLE_TRACE_2026-10-28.md). It establishes a two-buffer preset loader and a mismatch between the caller's group index and the shuffle helper's actual target. This improves static logic coverage but does not name the IDs or prove a gameplay mechanic. Step 4 remains **SEBAGIAN** and Step 8(b) remains **UNKNOWN** pending consumer/context evidence and an independent runtime/gameplay result.

## Restore gate update

Runs [#40613996374](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40613996374) and [#40614208610](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40614208610) both crash with exit 139 at savestate load before load-call return/event; rehydrating BIOS into the sanitized checkpoint yields bytes identical to raw state. Mark this checkpoint **UNRESTORABLE IN THE TESTED PCSx-Redux FLOW / WAIT** and do not repeat identical loads without new evidence. No controller input was sent.
