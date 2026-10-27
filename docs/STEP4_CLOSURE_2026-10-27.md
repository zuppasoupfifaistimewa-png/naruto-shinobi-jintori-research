## Additional boundary caution from the entry-0 artifact

The raw context around `0x800BDBFC` shows a function-like stack prologue and preceding control-flow instructions at `0x800BDBE4`–`0x800BDBF8``, followed by `j 0x800BE11C` at `0x800BDBFC`. Thus `0x800BDBFC` is visibly inside an instruction sequence that already has a stack-frame setup; treating that jump as an independently validated function entry is unsupported. Combined with `reference_count=0` and Ghidra body-overlap errors, this candidate cannot currently be used as the setter's caller/helper or as proof of loader reachability. This observation is bounded to the emitted raw window; it does not automatically validate `0x800BDBE4` as a formal Ghidra function boundary.

---

# LIVE ADDENDUM — Full Ghidra entry-0 pass timed out, 27 Oktober 2026 21:56 WIB

Run [#40520635663](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40520635663) is now **completed/success** overall; text artifact #12743796502, 2,299,302 bytes, ZIP SHA-256 `e2d5b496b2310c17110c59710212f7605bf8b3d90b798abb438c1224bf3d0549`. The artifact was downloaded and its digest verified locally before reading.

The artifact adds 36 function-index rows for entry 0 and records the resource hash/size (`0x5F800`, 110,536 bytes, SHA-256 `56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4`) under hypothetical base `0x800AD000`. However, `entry0-ghidra-headless.log` says analysis timed out at 1,800 seconds for `DATA_BIN_ENTRY_0000.bin`. It contains numerous function-body repair/overlap errors. The nominated `candidate_800bdbfc` is 36 bytes in the exported index, but the helper report states `reference_count=0`; the listing/decompilation is not evidence that it is called from the RNG setter path. Treat this resource pass as **PARTIAL / TIMEOUT**, despite the overall workflow conclusion `success`.

This does not replace the bounded caller-window evidence above: at `0x800AF2AC), `move a0,v0` in the delay slot passes the return of `0x80037138` to `0x80035DA8`. It still does not validate caller function boundaries, seed value/lifecycle, runtime base, or gameplay effects. Do not label `0x800BDBFC` as a verified caller/helper for that path.

At the most recent live check, [#40521141039](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521141039) remained in progress: main executable analysis and setup steps completed, DATA.BIN entry 1 analysis was active; entry 0 step and artifact upload were pending. Do not duplicate that run.

---

## LIVE ADDENDUM — entry-0 helper return versus setter argument, 27 Oktober 2026 21:53 WIB

Run [#40521136060](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521136060) and entry-1 context run [#40521136038](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521136038) succeeded. Their local disassembly windows show:
- `0x800AF2A4 jal 0x80037138`, with delay slot `0x800AF2A8 li a0,-1`: the helper receives `-1`.
- `0x800AF2AC jal 0x80035DA8`, with delay slot `0x800AF2B0 move a0,v0`: the seed-setter candidate receives the helper's return value, not literal `-1`.

This tightens instruction-level interpretation of candidate 4(a); it does not close the formal criterion. The caller boundary remains UNMAPPED; entry-0 base `0x800AD000` is hypothetical; helper return, value of global counter `0x80066E7C` at this site, actual setter execution during boot and downstream RNG/gameplay effects remain UNKNOWN. Historical cold-boot probe did not hit the setter through its bounded observation window, which is not proof the setter never runs elsewhere.

[Live reconciliation](STEP4_10_LIVE_RECONCILIATION_2026-10-27.md) · [Context Actions #40521136060](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521136060).

---

# Penutupan Langkah 4 — RNG dan caller statis, 27 Oktober 2026

## Keputusan status

**Status Langkah 4 secara keseluruhan: SEBAGIAN** menurut matriks resmi (4a–4e). Subbagian inventaris statis dan scan pola sempit telah dituntaskan dalam batas alat yang terdokumentasi melalui run Ghidra #40455975408 dan artefak terkait. Run final memperjelas bahwa tidak semua raw JAL di resource diterima Ghidra sebagai decoded direct call: entry 0 3/5, entry 1 108/144; 36 kandidat entry 1 lain terdekode sebagai JAL pada pass disassembly lokal, tetapi boundary caller masih UNKNOWN. Hasil statis tersebut menutup inventaris terbatas, bukan seed/lifecycle runtime, determinisme hasil roulette secara kausal, caller battle, indirect/dispatch menyeluruh, atau randomness alternatif. Karena itu status keseluruhan tetap SEBAGIAN.

Untuk penutupan inventaris statis di bagian awal, tidak ada input gameplay atau pemulihan savestate. Cold-boot emulator terpisah tanpa input/restore kemudian dilakukan untuk kandidat seed setter dan dicatat pada addendum runtime di bawah; tidak ada breakpoint hit yang mengonfirmasi setter. Biner disc hanya digunakan pada runner privat, tidak dimasukkan ke Git atau artefak.

## Hasil akhir yang terverifikasi

1. **Generator utama:** `0x80035D78`; state global `0x800A3118`; `state = state * 0x41C64E6D + 0x3039 (mod 2^32)`, keluaran `(state >> 16) & 0x7FFF`. SHA-256 executable `SLPS_035.53`: `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
2. **Executable utama:** 4 direct-JAL caller yang dikonfirmasi Ghidra: `0x80015B14`, `0x80015BF0`, `0x8001A460`, `0x80020C24`. Fungsi dan konteks statis tercatat pada laporan utama.
3. **DATA.BIN entry 0:** empat instruksi direct-JAL menuju RNG pada base analisis hipotetis `0x800AD000`. Tiga mempunyai incoming conditional branch pada jendela lokal. `0x800BB748` tetap UNKNOWN untuk reachability karena berada setelah unconditional jump tanpa incoming edge lokal yang ditemukan. Pada kandidat setter `0x800AF2AC → 0x80035DA8`, delay slot `0x800AF2B0 move a0,v0` meneruskan return helper `0x80037138` sebagai input setter; `li a0,-1` di `0x800AF2A8` adalah input helper sebelumnya. Nilai return helper dan nilai state akhir masih UNKNOWN.
4. **DATA.BIN entry 1:** raw scan menemukan 144 kandidat direct-JAL pada base analisis hipotetis `0x800D0000`. Run final Ghidra memvalidasi 108 call site sebagai instruksi direct call dan mengelompokkannya ke 50 fungsi; 36 lainnya berstatus `RAW_WORD_ONLY_INSTRUCTION_NOT_DECODED` pada output Ghidra. Pass disassembly lokal terdahulu mendekode 36 kata itu sebagai `jal 0x80035D78`, tetapi batas fungsi dan konfirmasi Ghidra tetap UNKNOWN. Karena itu, 144 adalah total raw candidate, bukan 144 caller terkonfirmasi Ghidra.
5. **Scan lintas berkas:** raw scan terverifikasi checksum menemukan 152 direct-JAL kata kandidat total (4 main EXE + 148 DATA.BIN). Jumlah tervalidasi Ghidra pada resource adalah 2 caller RNG di entry 0 dan 108 di entry 1, selain 4 caller executable utama. DATA2.BIN, DUMMY.BIN, dan XASECT.BIN tidak memiliki hit direct-JAL ke target RNG atau setter. Signature pengali LCG `0x41C64E6D` + MULT/MULTU hanya ditemukan pada rutin utama di `0x80035D78`.
6. **Pola pointer sempit:** scan tidak menemukan konstruksi alamat `LUI + ADDIU/ORI + JALR` yang cocok dengan alamat literal RNG, setter, atau state dalam lima berkas mentah yang diperiksa. Scan juga tidak menemukan literal alamat target sejajar yang persis. Hasil negatif ini berlaku hanya untuk pola yang dicari.

## Tabel keyakinan dan batas yang ditutup

| Pertanyaan | Hasil akhir |
|---|---|
| Algoritme RNG utama dan global state | **VERIFIED statis; hanya subkriteria** |
| Inventaris direct-JAL dan scan signature/pointer sempit | **TUNTAS hanya dalam cakupan scan yang dinyatakan; tidak menutup 4(a–e)** |
| Raw direct-JAL candidate pada 144 lokasi entry 1 | **VERIFIED sebagai kata mentah; 108 tervalidasi Ghidra, 36 raw-only pada Ghidra** |
| Base RAM dan lifecycle entry 0/1 saat runtime | **UNKNOWN** |
| Reachability entry 0 di `0x800BB748` | **UNKNOWN** |
| Boundary fungsi untuk 36 call site entry 1 | **UNKNOWN** |
| Semua pemanggilan melalui pointer, jump table, atau target runtime hasil kalkulasi | **UNKNOWN** |
| Kode terkompresi/terenkripsi atau yang baru menjadi kode setelah loader | **UNKNOWN; belum dibuktikan tercakup scan** |
| Identitas gameplay caller (roulette/battle/turn/AI) | **UNKNOWN kecuali konteks lokal yang dinyatakan eksplisit pada laporan** |
| Seed awal runtime dan kapan setter dipanggil | **UNKNOWN** |

## Mengapa ini merupakan penutupan yang jujur

Tidak ada hasil statis yang dapat membuktikan absennya semua caller tidak langsung atau semua kode yang baru didekode pada runtime hanya dari pencarian byte mentah. Inventaris JAL/signature/pointer yang didefinisikan telah selesai dijalankan dan dilaporkan; **Langkah 4 keseluruhan tetap SEBAGIAN** sampai kriteria 4(a–e) tercakup. Item UNKNOWN di atas bukan pekerjaan yang boleh ditandai VERIFIED tanpa bukti loader/xref tambahan atau pengamatan runtime yang terotorisasi.

## Referensi

- [Laporan utama Langkah 4](STEP4_RNG_TRACE_2026-10-27.md)
- [Scan referensi lintas resource](../out/rng_resource_reference_scan_2026-10-27.md)
- [Caller entry 1 yang dikelompokkan Ghidra](../out/rng_resource_entry1_ghidra_callers_2026-10-27.md)
- [36 caller entry 1 tanpa boundary fungsi](../out/rng_resource_entry1_unmapped_context_2026-10-27.md)
- [Konteks entry 0](../out/rng_resource_entry0_ghidra_context_2026-10-27.md)
- [Scan signature LCG](../out/step4_rng_signature_scan_2026-10-27.md)
- Actions: [resource reference scan #40454059515](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40454059515), [entry 1 caller validation #40454881770](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40454881770), [entry 1 bounded decode #40455582988](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455582988), [entry 0 bounded context #40455557190](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455557190), [LCG signature scan #40455975609](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455975609).


## Hasil run Ghidra final #40455975408 — 27 Oktober 2026

Run selesai dengan **success** (mulai 05:33:20 UTC, selesai 06:13:03 UTC; sekitar 39 menit 43 detik). Semua langkah analisis dan pembersihan temporary inputs dilaporkan sukses. Artefak teks-only `ghidra-slps-03553-function-index` (ID 12713583805, SHA-256 ZIP `56266b0e5e5ae8407574914bdd2da4e1e6d7783115f6355aa0349a775c63faed`) menyatakan executable utama 1.202 baris fungsi, DATA.BIN entry 1 1.555 baris fungsi, entry 0 38 baris fungsi. Biner disc/resource tidak diunggah; hanya output analisis teks diunggah.

Hasil akhir Ghidra mengoreksi tingkat validasi yang perlu ditulis: entry 0 punya 5 raw JAL candidates (termasuk 1 ke seed setter), dengan 3 decoded direct-call sites total: 2 ke RNG dan 1 ke setter; dua kata RNG di `0x800BB748` dan `0x800BB770` tidak didekode Ghidra. Entry 1 punya 144 raw RNG candidates, 108 decoded direct-call sites dalam 50 fungsi, dan 36 raw-only candidates. 36 raw-only ini pernah cocok dengan `jal 0x80035D78` dalam pass disassembly lokal, tetapi Ghidra tidak mengesahkannya sebagai instruksi decoded direct-flow. Karena itu, angka 152 tetap raw candidates; jangan menyebut semuanya tervalidasi Ghidra.

## Addendum runtime 4(a) — seed-setter candidate probe #40485987817

Eksperimen baru ini ditujukan khusus untuk kandidat setter state RNG `0x80035DA8`, berbeda dari probe loader `0x800AD454`. Workflow pada source commit `e1e346e707254ad617a6cccad43689df908801a6` menjalankan cold boot tanpa input gameplay/restore savestate, memasang satu breakpoint, dan membatasi sesi target ke 35 detik. Run [#40485987817](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817) selesai `success` 10:08:48 UTC (17:08:48 WIB); artefak teks-only #12724933081 berukuran 4.003 byte, ZIP SHA-256 `74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6`. Raw log memverifikasi semua sumber assets (disc/CUE/BIOS/AppImage), pra-uji mencapai VSync frame 50, listener-only kontrol maksimum frame 60, dan cold boot kandidat setter mencatat progress frame 1–120 dengan `bp_hits=0`; exit 124 pada batas 35 detik serta `STEP7_PRIVATE_CLEANUP=PASS`. Tidak ada `STEP7_SINGLE_BP_HIT`, sehingga `$a0`, `$ra`, dan callsite runtime tidak tersedia.

**Peringatan integritas report:** artefak/run ini dibuat sebelum koreksi fallback alamat. Ringkasan no-hit yang diunggah salah menampilkan `SINGLE_BREAKPOINT_PC=0x800AD454`, alamat target run loader sebelumnya. Ini kesalahan fallback report, **bukan** alamat target yang terdaftar pada run ini: baris raw `STEP7_SINGLE_BP_READY` menyebut persis `target=0x80035DA8`, dan seluruh event progress menampilkan hit 0. Source fallback diperbaiki pada commit `a6734d7fc57ff6dfab9b8135cd5661bf0278c437`; validator [#40486315324](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40486315324) lulus dengan `STEP4_SEED_BP_NO_HIT_FALLBACK_PASS target=0x80035DA8`, `STEP4_SEED_BP_PARSER_FIXTURE_PASS`, dan `STEP7_FRAME_PARSER_FIXTURE_PASS`. Fixture parser sintetis menguji ekstraksi field; bukan bukti hit emulator.

Kesimpulan: probe bounded ini **tidak membuktikan** bahwa setter seed dipanggil pada jendela cold boot yang diuji. Karena PC runtime target tidak tercapai/teramati, hasil itu juga tidak membuktikan bahwa setter tidak pernah dipanggil di jalur lain atau boot yang lebih lambat. Callsite statis `0x800AF2AC → 0x80035DA8` masih kandidat pada base entry-0 hipotetis `0x800AD000`; menurut delay slot, argumen setter berasal dari return helper `0x80037138`, sedangkan helper menerima `-1`. Nilai return helper dan state boot tetap UNKNOWN/SEBAGIAN. Tidak ada probe runtime tambahan yang diperlukan tanpa hipotesis baru.
