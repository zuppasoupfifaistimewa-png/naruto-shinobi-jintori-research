## CORRECTION — raw MIPS clarifies global-pointer dereference, 27 Oktober 2026 21:43 WIB

Cross-check on the emitted MIPS body resolves one important distinction and limits how the two C outputs should be compared. At `0x800ED920), code executes `lui v1, %hi(D_8013EA74)`; at `0x800ED924), `lw a0, %lo(D_8013EA74)(v1)` loads a 32-bit value from the global slot at `0x8013EA74). It then computes `index * 0x90`, adds that offset to the **loaded value**, and reads one byte at offset `0x29` from that derived record address.

Ghidra C represents the value read from the global as `iRam8013ea74`. The m2c C output renders `D_8013EA74` as a static symbol in pointer arithmetic without expressing the same dereference as clearly. Therefore, call tokens/body boundary/control-flow offer a useful structural cross-check, but the C outputs are **not fully equivalent evidence for pointer typing or effective address**. The raw MIPS load is the authoritative basis for this operation-level statement. The actual value stored at `0x8013EA74`, the mapped record table and runtime resource base remain unverified; do not assume the global slot's link-time address is itself the record table.

---

# LIVE ADDENDUM — Same-boundary function analysis, 27 Oktober 2026 21:41 WIB

Run [#40523020556](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40523020556) completed/success, artifact #12742268706 (1.367.605 B; ZIP SHA-256 `5f3f767667444f7c956c36fc59cf75b6bb90a5a1dde8ddb92fb69f9e0f797e81`). Entry 1 hash confirmed: file offset `0x10BB000`, 596.412 B, SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`. Private slice stayed in runner temp and was cleaned; artifact is text/C/disassembly/log only.

Ghidra validates `0x800ED8C8` as entry in the candidate resource view; body size 160 B and end-exclusive `0x800ED968). Direct RNG call is `0x800ED8E4 → 0x80035D78`; the delay slot at `0x800ED8E8` masks and preserves the helper result byte before RNG returns. m2c exit 0. Ghidra and m2c C outputs agree structurally on calls to `0x800CB4B4` and `0x80035D78`.

Decoded static behavior: argument index is truncated to 16 bits; low byte from helper `0x800CB4B4(index)` is default result. RNG output modulo 250 is compared to a table byte at decompiled address `pointer + index*0x90 + 0x29`. If remainder >= table byte, output is `0xFF`; otherwise output is the helper byte. This is verified candidate-function behavior, not a verified name such as roulette/battle/AI, and not a statement about runtime mapping or how game logic consumes its output.

Earlier retries #40521830977, #40522317571 and #40522919529 had setup/parser problems; they are not the successful evidence. Run #40523020556 is the valid same-boundary result. Overall Step 5 stays **SEBAGIAN**.

---

# Langkah 5 — survei statis resource kode DATA.BIN entry 1

Tanggal: 27 Oktober 2026  
Status: **SELESAI sebagai survei statis awal; alamat muat runtime masih hipotesis**.

## Input yang tervalidasi

- Disc BIN SHA-256: `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`.
- `DATA.BIN`: 66.015.232 byte, SHA-256 `69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822`.
- Entry index 1 menurut katalog resource: offset file `0x10BB000`, ukuran 596.412 byte (`0x919BC`), SHA-256 potongan `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`.
- Base import untuk analisis statis: `0x800D0000`, **asumsi**, belum dikonfirmasi dari loader runtime.
- Run: [Actions #40439763833](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40439763833), sukses. Artefak teks saja: [artifact 12705072941](https://api.github.com/repos/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/artifacts/12705072941). Ghidra mengekspor 1.551 baris fungsi pada impor resource ini; ini hitungan Ghidra dengan beberapa target yang sengaja dijadikan root analisis, bukan jumlah fungsi sumber yang telah terbukti.
- Resource potongan tidak di-commit dan tidak di-upload ke artefak.

## Temuan lintas-resource

Di dalam resource, enam call site `0x80111228`, `0x801112CC`, `0x801113B4`, `0x801114F0`, `0x80111588`, dan `0x80112418` masing-masing memanggil getter executable utama `0x80012A70`. Dua referensi tambahan ditemukan pada `0x8012AA2C` dalam fungsi yang dipetakan Ghidra sebagai `FUN_8012a9c4`, dan `0x80137C34` dalam `FUN_80137ad8`.

Dalam enam target yang ditinjau, pola instruksi menghitung alamat record memakai indeks `* 0x90` dan membandingkan sebuah field word record dengan hasil getter target. Beberapa jalur melakukan pemeriksaan flag/bit tambahan sebelum menulis field state dan memanggil `FUN_800EF98C`. Secara terpisah, `0x80112418` mengarah ke `FUN_80100d14(1)` lalu `FUN_80100dcc(0xDF)` setelah pemeriksaan threshold.

Karena dokumentasi executable utama telah mengidentifikasi `0x80012A70` sebagai getter target konfigurasi Chakra, referensi ini adalah **bukti statis kuat bahwa resource memuat jalur yang membandingkan record terhadap target Chakra**. Namun nama scene/event, arti semua flag, dan apakah cabang tertentu merupakan kemenangan Story Mode belum terbukti.

## Interpretasi target yang diperiksa

- `0x80111228`: target Chakra dibandingkan dengan sebuah nilai record; jalur lanjut menulis field state, menginisialisasi `0x200`, dan memanggil `FUN_800EF98C`.
- `0x801112CC`: ada pemeriksaan flag `0x200` pada record sebelum pembandingan target; jalur lanjut menulis field state dan nilai `8`.
- `0x801113B4`: pembandingan target serupa; jalur lanjut menulis nilai `4`.
- `0x801114F0`: pembandingan target diikuti pengecekan tambahan melalui `FUN_800BDBFC(0x20)); jalur lanjut menulis nilai `0x20`.
- `0x80111588`: setelah pembandingan target, hasil `FUN_80012AD0()` diperiksa terhadap bit `0x1000`, dengan cabang yang menulis `0` atau `0x1000`.
- `0x80112418`: setelah threshold terpenuhi, alur memanggil `FUN_80100D14(1)` dan `FUN_80100DCC(0xDF)`; arti parameter/event masih perlu ditelusuri.

Nama `candidate_...` diberikan oleh skrip analisis untuk alamat yang diperiksa, bukan nama asli fungsi. Base `0x800D0000` dipakai agar referensi internal konsisten dalam impor biner; pemetaan runtime tetap harus dianggap provisional.

## Langkah 6 berikutnya

1. Dekompilasi `FUN_8012A9C4` dan `FUN_80137AD8`, dua pemanggil tambahan getter target.
2. Telusuri `FUN_800EF98C`, `FUN_80100D14`, `FUN_80100DCC`, dan `FUN_800BDBFC` untuk mengetahui transisi state/event serta cabang yang menjadi target threshold.
3. Dekompilasi konsumen Chakra setter `0x8001387C`, terutama `FUN_800D5608`, `FUN_800E1188`, `FUN_800D8918`, `FUN_8011C0D0`, `FUN_8010478C`, dan `FUN_80101814`.
4. Lacak sumber pointer/record dan field pada offset `0x58B`, `0x2E9`, `0x2E5`, dan `0x5D2`; jangan memberi nama semantik pada field sebelum ada bukti lintas-reference.
5. Pertahankan pemisahan fakta statis vs hipotesis sampai base/alamat runtime divalidasi secara independen.
