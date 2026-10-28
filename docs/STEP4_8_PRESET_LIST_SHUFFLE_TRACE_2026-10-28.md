# Step 4 / Step 8 — trace daftar berindeks 18 preset dan helper pengacak

Tanggal: 28 Oktober 2026 (WIB)  
Fokus: menurunkan operasi yang benar-benar terlihat di main executable, tanpa menebak nama fitur dari angka mentah.

## Bukti sumber

- Workflow/artefak: [run #40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524), [artefak teks #12739676233](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524/artifacts/12739676233).
- SHA-256 ZIP artefak: `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d`.
- Main EXE (private runner input; tidak disimpan dalam repo/artefak): 385,024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
- Bukti kerja: raw MIPS dalam output `spimdisasm`, jendela fungsi Ghidra, referensi alamat, dan perbandingan Ghidra/m2c. Output teks di artefak cukup untuk audit ulang; berkas game mentah tidak diperlukan di laporan.

## Hasil statis

### 1. Pemilih baris dan dua buffer

Fungsi `0x80015610` (body `[0x80015610, 0x80015748)`) memeriksa argumen `param` terhadap `0x12`: nilai 0–17 diterima; nilai >=18 mengembalikan 0.

Untuk masing-masing kelompok `g=0,1`, instruksi menghitung sumber:

`0x8005603C + param * 0x40 + g * 0x480`

Isi disalin byte-per-byte ke buffer aktif:

`0x80070D0A + g * 0x40`

Penyalinan berhenti ketika menemukan byte sentinel `0xFF` atau mencapai 64 byte. Panjang tersimpan sebagai halfword di `0x80070D02 + g*2`; indeks/cursor terkait di-reset ke nol pada `0x80070D06 + g*2`.

Pemanggil langsung yang teridentifikasi:
- `0x80012820`, dari badan fungsi `0x80012780`: argumen berasal dari byte offset `+2` pada record ber-stride `0x30` dalam tabel sekitar `0x80064918`.
- `0x80012F90`, dari badan `0x80012EAC`: argumen berasal dari byte offset `+2` pada descriptor yang dipilih lewat kalkulasi terkait `0x80057798`.

Ini membuktikan jalur pemuatan dua daftar berindeks dari tabel statis. **Belum membuktikan nama fitur daftar, apakah byte berarti kartu, tile, aksi, urutan giliran, atau resource lain.**

### 2. Isi data yang tertanam

Pembacaan tabel dari data EXE menunjukkan dua blok kelompok untuk setiap indeks 0–17 identik byte-per-byte dalam keadaan statis.

| Indeks | Panjang hingga `0xFF` pada masing-masing blok | Catatan |
|---:|---:|---|
| 0 | 51 | Ada sentinel |
| 1 | 55 | Ada sentinel |
| 2 | 59 | Ada sentinel |
| 3 | 57 | Ada sentinel |
| 4 | 61 | Ada sentinel |
| 5 | 62 | Ada sentinel |
| 6 | 62 | Ada sentinel |
| 7 | 62 | Ada sentinel |
| 8 | 11 | Ada sentinel |
| 9–17 | 64 byte | 64 byte sumber seluruhnya `0x00`; tidak ada sentinel dalam blok 64 byte |

Panjang dihitung dari offset awal hingga byte pertama `0xFF`, atau 64 bila tidak ada sentinel. Untuk indeks 9–17, kode loader tidak menafsirkan blok nol itu sebagai daftar kosong: karena tidak menemukan `0xFF`, jalur statis akan menyalin 64 byte nol dan menyimpan panjang 64. Ini adalah fakta implementasi; apakah indeks tersebut tak terpakai, data cadangan, atau konfigurasi khusus **belum diketahui**. Jangan menyimpulkan bahwa ID 0 valid atau invalid secara semantik hanya dari bentuk tabel ini.

### 3. Perilaku helper `0x80015B7C`: kedua pemanggilan memilih daftar pertama

Badan executable yang kembali ke pemanggil pada `0x80015C64` dan memulihkan stack pada delay slot `0x80015C68`, sesuai batas Ghidra `0x80015C6C`. Label spimdisasm `nonmatching func_80015B7C, 0x580` terlalu lebar dan melampaui return sebenarnya; gunakan instruksi return mentah dan batas fungsi Ghidra untuk soal boundary ini.

Pada alamat `0x80015B9C`, fungsi menimpa argumen masuk dengan `addu a0,zero,zero`. Sesudah itu:
- mengambil count dari `0x80070D02` (daftar pertama), bukan `0x80070D04`;
- menggunakan offset buffer `0 << 6 = 0`, sehingga basisnya `0x80070D0A`;
- jika count `n` bukan nol, mengulang `4*n` kali;
- pada iterasi `i`, menukar byte pada indeks `i mod n` dengan indeks `RNG mod n`, menggunakan fungsi RNG `0x80035D78`.

Ini bukan pengacakan Fisher–Yates standar: loop menjalankan empat putaran posisi kiri secara siklik dengan posisi kanan pseudo-acak. Yang lebih penting, argumen kelompok yang dikirim pemanggil diabaikan pada awal helper. Karena `0x80015610` memanggil `0x80015B7C(g)` dua kali untuk `g=0,1`, kedua pemanggilan secara statis mengacak buffer pertama dan menggunakan count pertama; helper ini tidak mengacak buffer kedua.

Helper `0x800158D8` juga secara literal membaca byte dari `0x80070D02` tanpa membaca argumen masuk. Fungsi lain di sekitar `0x800158E8` dan `0x800159BC` menargetkan offset/basis kelompok nol pada jalur yang terlihat dalam jendela instruksi yang diaudit. Ini memperkuat prioritas untuk mengaudit konsumen buffer kedua, tetapi tidak cukup untuk menyebutnya sebagai bug atau mengasumsikan maksud programmer.

### 4. Apa artinya bagi riset logika game

Yang sekarang diketahui secara statis:
1. Ada tabel dengan 18 indeks yang lolos guard fungsi pemuat.
2. Setiap indeks mengarahkan pemuatan dua blok byte 64-entry dari sumber berjarak `0x480`.
3. Untuk indeks 0–8, kedua blok sumber identik dan berakhir dengan sentinel dengan panjang berbeda; indeks 9–17 berisi 64 byte nol tanpa sentinel.
4. Fungsi yang dinamai `0x80015B7C` di laporan lama tidak memakai parameter kelompoknya: operasi swap yang tampak hanya menyasar daftar pertama.

Yang belum diketahui:
- nama/makna record dan tiap byte ID;
- apakah semua 18 indeks benar-benar dipakai oleh gameplay;
- siapa yang mengonsumsi daftar kedua dan apakah ada kode lain yang mengubah/mengacaknya;
- apakah pengacakan ini berhubungan dengan kartu, giliran, roulette, papan, atau pertarungan;
- kaitan runtime antara fungsi, kondisi permainan, dan efek visual/hasilnya.

## Eksperimen savestate terisolasi — hasil dan batas

Sumber checkpoint privat berasal dari run #39262213468. Raw state berukuran 21,163,286 byte dengan SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`; state sanitasi berukuran 20,638,994 byte dengan SHA-256 `b94e61502b63a81107f48153932ccbef21bede8c7f53d4b01e6e013ecb8979eb`.

- [Percobaan restore mentah #40613996374](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40613996374): BIOS/game/state/card terverifikasi; PCSX-Redux crash `SIGSEGV`/exit 139 sesudah `RESTORE_LOAD_BEGIN`. Tidak ada bukti bahwa `loadSaveState` kembali atau event `SaveStateLoaded` berjalan.
- [Percobaan rekonstruksi #40614208610](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40614208610): BIOS dimasukkan kembali ke state sanitasi; hasil SHA-256 identik dengan raw source (`00fab826…f6c3d`), kemudian terjadi `SIGSEGV` pada titik yang sama. Ini mengonfirmasi rekonstruksi byte, **bukan** percobaan dengan representasi state yang berbeda.

Tak ada tombol gameplay dikirim pada kedua percobaan. Karena loader crash dua kali dengan byte state yang sama, pengujian restore dihentikan; pengulangan identik tidak diharapkan memberi bukti baru. Screenshot asal checkpoint tetap hanya jangkar visual, bukan bukti aturan internal. Tidak ada state mentah, ROM/BIN/CUE/EXE, BIOS, Memory Card, atau RAM dump dimasukkan ke Git maupun artefak hasil baru.

## Status dan langkah lanjut

- Step 4: **SEBAGIAN** — hubungan RNG/pengacak dengan pemilihan/hasil gameplay belum terikat.
- Step 5: **SEBAGIAN** — caller terpilih dan struktur lokal ditelusuri, bukan keseluruhan EXE.
- Step 8: **SEBAGIAN**, subkriteria aturan gameplay utama tetap **UNKNOWN**.
- Restore savestate: **FAIL pada dua pemanggilan loader; jangan ulangi tanpa perubahan hipotesis atau emulator/state-format bukti baru**.
- Story Mode: **TIDAK TERBUKTI TAMAT**.
- Adaptive player: tidak dijalankan atau diubah.

Prioritas berikutnya: audit secara statis semua referensi ke count/buffer kedua dan fungsi yang memanggil `0x800158E8`/`0x800159BC`, lalu cocokkan daftar byte dengan tabel descriptor sebelum memilih eksperimen gameplay baru. Sampai ada checkpoint yang terbukti bisa dipulihkan, jangan mengklaim eksperimen A/B dari checkpoint ini dapat direproduksi.


<!-- descriptor-selector-crosscheck-2026-10-28 -->
## Cross-check: selector yang benar-benar muncul pada descriptor

Ada dua pemanggil langsung `jal 0x80015610` di main EXE (`0x80012820` dan `0x80012F90`), dan kedua argumen berasal dari byte `+2` pada tabel descriptor. Pembacaan data mentah memberi hasil berikut:

- Descriptor `0x80064918`, stride `0x30`, 18 record: byte `+2` adalah `[0,1,2,3,4,5,6,7,4,4,4,4,4,4,4,5,8,8]`.
- Descriptor `0x80057798`, stride `0x54`, 18 record: byte `+2` adalah `[0,1,2,8,3,4,8,5,6,6,0,0,0,0,0,0,3,5]`.

Dua tabel descriptor yang ditelusuri hanya memberikan selector 0–8 ke pemanggil langsung tersebut. Jadi blok sumber selector 9–17 yang tersusun sebagai 64 byte nol **tidak dipilih oleh dua descriptor ini**. Fungsi loader sendiri menerima selector hingga 17, tetapi jangan menyebut selector 9–17 reachable dari alur ini tanpa bukti pemanggil lain atau jalur tak langsung. Sebaliknya, ini juga belum membuktikan bahwa selector 9–17 tak pernah dipakai di seluruh game; batas kesimpulan hanya dua callsite dan dua tabel yang diaudit.


<!-- registry-and-list-mutation-trace-2026-10-28 -->
## ID registry and list mutation path

A further trace connects these byte values to a bounded numeric ID registry, without assigning feature labels:

1. Initialization at `0x800121AC–0x800121F4` clears `0x118($gp)`, walks records beginning at `0x80055CEC` with a `0x10)-byte stride, and stops when the first word is `0xFFFFFFFF`. The sentinel is at `0x8005602C`, index 52, so the runtime count written to `0x118($gp)` is 52 (indices 0–51). Function `0x800154D4` returns that count. This is an executable-table count, not a natural-language identification of its records.
2. The statically listed IDs in active source templates 0–8 fall within that range (maximum seen is `0x32`/50). The shuffle/insert helper `0x80015ADC` checks the input byte ID against this 52-entry count before continuing.
3. On the valid branch, `0x80015ADC` reads the count through `0x800158D8` (which actually reads the byte at `0x80070D02` regardless of its input argument), obtains one RNG value from `0x80035D78`, computes a position of the form `floor(n/2) + (RNG mod floor(n/2))`, and calls `0x800159BC` with the ID. The instruction sequence shows a mutation of the byte sequence around that position and a write of the ID to `0x80070C80 + 0x8A + position`; it also increments the halfword at `0x80070C80 + 0x82` when it is below 64.
4. The counterpart `0x800158E8` shifts bytes left in `0x80070D0A` from a supplied position and decrements that same halfword at `0x80070C80 + 0x82`. The target fields and exact byte transformations are statically visible; whether this state represents a card pool, hand, inventory, action queue, or another game concept remains **UNKNOWN**.

These paths give a more concrete rule-level description: a candidate ID is range-checked against a table-derived count, a randomized position is computed from the first-list count, and related list/count state is mutated. They do not prove which visible gameplay mechanic this implements. Runtime verification is blocked by the tested checkpoint's repeatable loader crash, so this finding remains **TERVERIFIKASI-STATIS**, not runtime-verified.


<!-- caller-id-random-insert-audit-2026-10-28 -->
## Caller cross-reference: ID source and exact random-insertion effects

The full main-EXE disassembly in artifact #12739676233 shows one direct `JAL` to `0x80015ADC`, at `0x80013B50` (delay slot `0x80013B54`). In that local code sequence:

- The routine first calls `0x800139FC(group, slot)`; the helper accepts `group < 4` and `slot < 3` and returns the byte at offset `+0x0A` of the indexed record in the data region based at `0x80070EA0`.
- That returned byte is passed as the second argument to `0x80015ADC` in the `0x80013B54` delay slot. The caller sets `a0=0`; the insertion helper's effective ID is `a1 & 0xFF` (the helper subsequently passes that byte as argument `a2` to `0x800159BC`).
- The insertion helper range-checks the ID against the 52-entry registry count returned by `0x800154D4`. It then calculates an insertion position from the first list length `n = byte[0x80070D02]`: `floor(n/2) + (RNG mod floor(n/2))`. For `n >= 2`, this chooses a position in the latter half of the list; if the divisor `floor(n/2)` is zero, raw MIPS reaches a `break` instruction on the zero-divisor path, so a caller must not be assumed safe for a one-item list.
- `0x800159BC` accepts that position and ID; if checks pass, it increments the halfword at `0x80070C82` only while the previous value is <64, shifts the byte sequence in `0x80070D0A` one slot to the right from the end toward the chosen position, and writes the ID to `0x80070C80 + 0x8A + position`.

**Important structure distinction:** `0x80070D02` is the source/template-list length used for the insertion position and buffer shift. `0x80070C82` is a separate halfword count that the insertion/removal helpers increment/decrement. The code does not increment `0x80070D02` in this path. Do not merge these fields into one presumed “deck size” or other gameplay variable without further dataflow evidence.

This narrows the static effect to: **a byte ID read from one of four three-slot records is range-checked, then placed at a pseudo-random position in a coordinated list/record structure while the source-order bytes shift right**. What a record/ID represents in the visible game, why the chosen position is in the latter half, and which runtime event invokes this local routine remain unknown. The raw disassembly proves the local operations and one direct JAL site; it does not prove an item/card/turn name or actual runtime reachability.


<!-- four-record-three-slot-id-operations-2026-10-28 -->
## Four-record / three-ID-slot operations found around the insertion caller

The local MIPS address arithmetic gives a stronger description of the source record than simply “a 12-slot table”:

- The initializer at `0x8001210C` clears the `0x80070EA0)-based region for `0x2D4` bytes. Address calculations in the adjacent helpers use record stride `0xB4` and accept record index 0–3.
- Each record has three adjacent ID bytes at offsets `+0x0A`, `+0x0B`, and `+0x0C`; this is exactly what the getter at `0x800139FC` reads when its second argument is 0, 1, or 2.
- The unlabelled code body starting at `0x80013A48` validates a candidate byte against the 52-entry registry, scans the selected record's three ID bytes, and writes the candidate into the first slot whose current byte is not a valid registry ID. It returns failure if all three slots already contain valid IDs. This is a concrete “put an ID into a free slot” operation; feature semantics remain unknown.
- The unlabelled code body starting at `0x80013B10` checks record index <4 and slot <3, reads the selected ID via `0x800139FC`, then calls the random-insertion helper. When removing slot 0 or 1 it shifts subsequent ID bytes left within that record; when removing slot 2 it skips the shift. It then sets the third slot `record+0x0C` to `0xFF`. This is a concrete remove-and-compact operation, combined with insertion of that ID into the separate shared indexed structure at `0x80070C80+0x8A`.
- The configured template length at `0x80070D02` is loaded by the preset loader and used for bounds/position calculations, whereas the separate halfword at `0x80070C82` is changed by the insert/remove helpers. The raw code does not establish that these two fields are the same counter or that the template length itself grows/shrinks.

The resulting static rule is now: **each of four records can hold up to three registry IDs; adding an ID fills the first invalid slot, while removing a chosen slot transfers its ID to another indexed structure, compacts remaining IDs, and marks the tail slot `0xFF`.** A separate helper chooses an insertion index pseudo-randomly in the latter half of the preset-configured range and shifts the companion order bytes. Do not label the IDs as cards, characters, upgrades, or actions without further evidence; no runtime/gameplay result was obtained.


<!-- sequence-pop-and-reshuffle-helper-2026-10-28 -->
## Sequence-pop and reshuffle helper at 0x80015768

A separate local operation reveals how the preset buffer is consumed:

1. `0x80015768` saves the current first byte `byte[0x80070D0A]`.
2. It calls `0x800158E8(0,0)`, whose raw instructions shift the `0x80070D0A` byte sequence left from position 0 through the configured length minus one and decrement the separate halfword `0x80070C82`.
3. It then calls `0x80015B7C(0)`; as established above, that helper ignores the group parameter and performs `4*n` random swaps only in the first buffer, with `n=halfword[0x80070D02]`.
4. The wrapper returns the saved pre-shift first byte. The tail byte is not explicitly cleared in the remove routine before the shuffle, and the configured length `0x80070D02` itself is not changed in this path.

The exact static operation is: **return the old first entry, shift the first sequence left, adjust a separate count, then re-shuffle the configured number of positions**. The apparent relationship between the shifted sequence, the ID array at `0x80070C80+0x8A`, and count at `0x80070C82` is still not sufficiently understood to call this a normal queue/deck pop or to assert whether the retained tail is intentional. Do not name this roulette/card drawing without consumer and runtime evidence.
