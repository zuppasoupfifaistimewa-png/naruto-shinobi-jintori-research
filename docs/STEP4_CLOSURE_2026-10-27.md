# Penutupan Langkah 4 — RNG dan caller statis, 27 Oktober 2026

## Keputusan status

**Langkah 4 SELESAI dalam cakupan inventaris statis yang didefinisikan, setelah run Ghidra #40455975408 sukses dan artefaknya diperiksa.** Run final memperjelas bahwa tidak semua raw JAL di resource diterima Ghidra sebagai decoded direct call: entry 0 3/5, entry 1 108/144. Hit raw sisanya tetap dicatat dan dibatasi sebagai UNKNOWN untuk validasi Ghidra, walau 36 hit entry 1 sebelumnya terdekode melalui pass disassembly lokal. Ini adalah penutupan cakupan statis yang terdefinisi, bukan klaim bahwa semua pemanggilan RNG saat runtime telah diketahui.

Tidak ada emulator/gameplay, input, pemulihan savestate, atau eksekusi fungsi game pada pekerjaan ini. Biner disc diambil/diperiksa hanya pada runner; tidak dimasukkan ke Git atau artefak.

## Hasil akhir yang terverifikasi

1. **Generator utama:** `0x80035D78`; state global `0x800A3118`; `state = state * 0x41C64E6D + 0x3039 (mod 2^32)`, keluaran `(state >> 16) & 0x7FFF`. SHA-256 executable `SLPS_035.53`: `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
2. **Executable utama:** 4 direct-JAL caller yang dikonfirmasi Ghidra: `0x80015B14`, `0x80015BF0`, `0x8001A460`, `0x80020C24`. Fungsi dan konteks statis tercatat pada laporan utama.
3. **DATA.BIN entry 0:** 4 instruksi direct-JAL menuju RNG pada base analisis hipotetis `0x800AD000`. Tiga mempunyai incoming conditional branch pada jendela lokal. `0x800BB748` tetap UNKNOWN untuk reachability karena berada setelah unconditional jump tanpa incoming edge lokal yang ditemukan. Pemanggilan kandidat setter `0x800AF2AC → 0x80035DA8` mengirim `$a0=-1`; jika jalur berjalan, state diset ke `0xFFFFFFFF`.
4. **DATA.BIN entry 1:** raw scan menemukan 144 kandidat direct-JAL pada base analisis hipotetis `0x800D0000`. Run final Ghidra memvalidasi 108 call site sebagai instruksi direct call dan mengelompokkannya ke 50 fungsi; 36 lainnya berstatus `RAW_WORD_ONLY_INSTRUCTION_NOT_DECODED` pada output Ghidra. Pass disassembly lokal terdahulu mendekode 36 kata itu sebagai `jal 0x80035D78`, tetapi batas fungsi dan konfirmasi Ghidra tetap UNKNOWN. Karena itu, 144 adalah total raw candidate, bukan 144 caller terkonfirmasi Ghidra.
5. **Scan lintas berkas:** raw scan terverifikasi checksum menemukan 152 direct-JAL kata kandidat total (4 main EXE + 148 DATA.BIN). Jumlah tervalidasi Ghidra pada resource adalah 2 caller RNG di entry 0 dan 108 di entry 1, selain 4 caller executable utama. DATA2.BIN, DUMMY.BIN, dan XASECT.BIN tidak memiliki hit direct-JAL ke target RNG atau setter. Signature pengali LCG `0x41C64E6D` + MULT/MULTU hanya ditemukan pada rutin utama di `0x80035D78`.
6. **Pola pointer sempit:** scan tidak menemukan konstruksi alamat `LUI + ADDIU/ORI + JALR` yang cocok dengan alamat literal RNG, setter, atau state dalam lima berkas mentah yang diperiksa. Scan juga tidak menemukan literal alamat target sejajar yang persis. Hasil negatif ini berlaku hanya untuk pola yang dicari.

## Tabel keyakinan dan batas yang ditutup

| Pertanyaan | Hasil akhir |
|---|---|
| Algoritme RNG utama dan global state | **VERIFIED statis** |
| Semua direct-JAL hit mentah yang terdeteksi pada berkas yang diidentifikasi | **SELESAI dipetakan/diperiksa dalam batas scan; status decoding per-callsite dibedakan** |
| Raw direct-JAL candidate pada 144 lokasi entry 1 | **VERIFIED sebagai kata mentah; 108 tervalidasi Ghidra, 36 raw-only pada Ghidra** |
| Base RAM dan lifecycle entry 0/1 saat runtime | **UNKNOWN** |
| Reachability entry 0 di `0x800BB748` | **UNKNOWN** |
| Boundary fungsi untuk 36 call site entry 1 | **UNKNOWN** |
| Semua pemanggilan melalui pointer, jump table, atau target runtime hasil kalkulasi | **UNKNOWN** |
| Kode terkompresi/terenkripsi atau yang baru menjadi kode setelah loader | **UNKNOWN; belum dibuktikan tercakup scan** |
| Identitas gameplay caller (roulette/battle/turn/AI) | **UNKNOWN kecuali konteks lokal yang dinyatakan eksplisit pada laporan** |
| Seed awal runtime dan kapan setter dipanggil | **UNKNOWN** |

## Mengapa ini merupakan penutupan yang jujur

Tidak ada hasil statis yang dapat membuktikan absennya semua caller tidak langsung atau semua kode yang baru didekode pada runtime hanya dari pencarian byte mentah. Karena itu, pekerjaan yang dapat direproduksi—identifikasi LCG, semua direct-JAL hit yang ditemukan, pemeriksaan Ghidra untuk 144 entry 1 dan empat entry 0, signature scan lintas berkas, serta pola pointer sempit—ditutup sebagai selesai. Item UNKNOWN di atas bukan pekerjaan yang boleh ditandai VERIFIED tanpa bukti loader/xref tambahan atau pengamatan runtime yang terotorisasi.

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
