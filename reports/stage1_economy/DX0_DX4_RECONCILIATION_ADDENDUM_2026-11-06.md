# DX0–DX4 — rekonsiliasi audit statis (6 November 2026)

Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`  
Baseline inklusif: `2d5becc3a70716cf78563233504b800b3c9609e0`  
Snapshot sumber: `a1f2b3250afe0819e2b9882677df4c876c8b3027`  
HEAD sebelum laporan ini: `49c274660d01fd96492ba1ca9d29d8150f560297`

## Status

| DX | Status | K | Kesimpulan |
|---|---|---:|---|
| DX0 | TUNTAS | K4 | Snapshot inklusif 5 commit (4 manusia, 1 bot); HEAD sebelum laporan 6 (4 manusia, 2 bot). |
| DX1 | TUNTAS | K4 | Full scan +0x1A: 172 akses; 7 load di FUN_800D15A8 memiliki asal basis slot tile-array 0x8013EA84. |
| DX2 | SEBAGIAN | K4 | CFG dan jalur helper terbukti; computed-pointer consumer mengalir ke setter Chakra. Tiga pembaca displacement literal lain belum diikat satu per satu. |
| DX3 | SEBAGIAN | K4 | Census selesai untuk tiga CFG root; tidak ada selisih level d atau 1<<d yang terbukti. |
| DX4 | TUNTAS | K4 | Tiga model berbeda dibandingkan dengan empat angka HIPOTESIS PENGGUNA; formula ROM tetap TIDAK TAHU. |

## DX0 — ledger inklusif

Ledger mencakup baseline itu sendiri.

| Scope | Total | Manusia | Bot |
|---|---:|---:|---:|
| Baseline inklusif sampai snapshot sumber | 5 | 4 | 1 |
| Baseline inklusif sampai HEAD sebelum laporan ini | 6 | 4 | 2 |
| Setelah commit laporan ini | 7 | 5 | 2 |

Perbedaan snapshot dan HEAD berasal dari satu publikasi bot setelah snapshot. Commit laporan ini menambahkan satu commit manusia lagi.

## Run Actions yang dibuat

Tidak ada run lain selain dua berikut.

| Run | Job / ID | Source SHA | Status | Exit |
|---|---|---|---|---:|
| 42172857714 | dx0-dx4-static / 127744485659 | 43c09007a736a21e9d2b984aed8e1f8d95800ad3 | FAIL; input dan cleanup PASS, analyzer keluar non-zero | 1 |
| 42173196076 | dx0-dx4-static / 127745572232 | a1f2b3250afe0819e2b9882677df4c876c8b3027 | PASS; input dan cleanup PASS | 0 |

Ringkasan terkomit:
- `reports/stage1_economy/dx0-dx4-raw-run-42172857714/attempt-1/ACTIONS_RUN_SUMMARY.txt`
- `reports/stage1_economy/dx0-dx4-raw-run-42173196076/attempt-1/ACTIONS_RUN_SUMMARY.txt`

Kedua run hanya mengeluarkan teks/TSV. Tidak menjalankan game/emulator, tidak memakai BIOS/savestate, dan tidak mengomit biner.

## DX1 — tile+0x1A

Pindaian `DX1_ALL_PLUS1A_ACCESS.tsv` tidak memfilter register basis: 172 hit terdiri dari 123 `sh`, 33 `lhu`, 9 `lbu`, dan 7 `sb`; `lw` dan `sw` tidak ditemukan.

Tujuh akses di `FUN_800D15A8` semuanya `lhu` dengan basis yang ditelusuri ke pointer tile-array melalui slot `0x8013EA84`:

| PC | File offset Entry 1 | Bytes | Instruksi |
|---|---|---|---|
| 0x800D2520 | 0x010E00D0 | 1A 00 A4 94 | lhu $a0,0x1a($a1) |
| 0x800D2ADC | 0x010E068C | 1A 00 44 94 | lhu $a0,0x1a($v0) |
| 0x800D2B5C | 0x010E070C | 1A 00 44 94 | lhu $a0,0x1a($v0) |
| 0x800D3EE4 | 0x010E1A94 | 1A 00 44 94 | lhu $a0,0x1a($v0) |
| 0x800D3F74 | 0x010E1B24 | 1A 00 44 94 | lhu $a0,0x1a($v0) |
| 0x800D4628 | 0x010E21D8 | 1A 00 44 94 | lhu $a0,0x1a($v0) |
| 0x800D46EC | 0x010E229C | 1A 00 42 94 | lhu $v0,0x1a($v0) |

Nilai hasil load tetap dinamis. Trace statis menyatakan asal pointer melalui slot `0x8013EA84`, bukan bahwa nilai alamat aktual selalu literal `0x8013B818`.

`DW4_TILE_PLUS1A_ACCESSES.tsv` kosong karena analyzer DW4 hanya memindai CFG `FUN_80102408`; itu bukan scan seluruh Entry 1 dan tidak mencakup `FUN_800D15A8`. Karena itu hasil kosong bukan bukti bahwa D15A8 tidak membaca +0x1A.

Klaim AZ3/DP3 yang bertahan: cabang action byte 3/8 dalam `FUN_800D15A8` memakai `u16(tile+0x1A)` sebagai nominal fee, membandingkannya dengan saldo kerja, lalu memposting `-fee` ke pending +0x2EE ketika saldo cukup. Loader `FUN_800F7ADC` menyalin byte sumber record +0x14/+0x15 menjadi halfword tile+0x1A. DP3 mengelompokkan 415 record: tiap X mempunyai tepat satu nilai fee +0x1A; tujuh titik nonzero yang dicatat pengguna cocok. Label action dan jalur ini didukung audit AZ3; hasil DX1 sendiri adalah verifikasi load PC/basis.

## DX2 — CFG +0x2EE dan jalur ke setter

Semua target dari root `FUN_800EC574` reachable: `0x800ECAD0`, `0x800ECB4C`, `0x800ECB88`, dan semua PC `0x800ECBA8–0x800ECBBC`. `DX2_PATH_CONDITIONS.tsv` memuat 22 branch PC per target. Delay slot dimodelkan; indirect JR di `0x800EC8AC` diperlakukan sebagai exit, tanpa mengasumsikan fall-through; JR RA di `0x800EDD60` berakhir sesudah delay slot `0x800EDD64`.

Tiga kondisi yang wajib fall-through agar jalur menuju target tetap dapat dicapai:
- `0x800EC814 bnez $v0,0x800EDD48`: perlu `$v0==0`.
- `0x800EC874 bnez $v0,0x800EDBC8`: perlu `$v0==0`.
- `0x800EC890 beqz $v0,0x800ECD60`: perlu `$v0!=0`.

Pada jalur helper:
1. `0x800ECAD4` memanggil `FUN_8001552C`; helper mengembalikan `v0=1` melalui delay slot JR RA.
2. `0x800ECAE0` menyimpan 1 ke global `0x80139EFC`.
3. `0x800ECBA8` membaca u16 global itu.
4. `0x800ECBB0 negu` menghasilkan `0xFFFFFFFF` (-1).
5. `0x800ECBB4 j 0x800EC928` memiliki delay slot `0x800ECBB8 sh $v0,0x2EE($v1)`, sehingga halfword `0xFFFF` ditulis ke pending manager +0x2EE.

Jalur consumer utama tidak terdeteksi sebagai displacement literal +0x2EE karena membentuk pointer lebih dulu. Di `FUN_800BE5D8`:
- `0x800BE620 addiu t1,v0,0x2EE` membentuk manager_base +0x2EE.
- `0x800BE634/0x800BE638` membentuk offset `2*player_index`; `0x800BE63C lh ...,0(pointer)` membaca signed pending.
- `0x800BE6FC/0x800BE700/0x800BE704`, `0x800BE750`, `0x800BE764`, dan `0x800BE778` mengakses/memperbarui slot pending melalui computed pointer.
- `0x800BE7A8/0x800BE7AC/0x800BE7B0` membaca halfword pending untuk diproses; `0x800BE7B8/0x800BE7BC` melakukan sign extension.
- Fungsi memperbarui saldo kerja participant +0x04, kemudian `0x800BEC98 jal 0x8001387C` memanggil setter. Delay slot `0x800BEC9C move a0,s1` memasok indeks pemain; `$a1` telah dibentuk dari participant +0x04. Getter `0x800BECA0 jal 0x800138EC` mengikuti untuk readback. Setter 0x8001387C menulis saldo kanonis participant +0x18 menurut audit AZ3.

**Kesimpulan terbatas:** ya, pada jalur helper ini +0x2EE berisi -1 dan consumer-nya menerapkan delta itu ke saldo Chakra. Ini membuktikan debit satu unit Chakra pada jalur tersebut. Makna gameplay pemicu helper = TIDAK TAHU. Tidak semua 25 akses displacement literal +0x2EE terbukti sebagai transaksi tile; tiga pembaca langsung `0x800DCFE8`, `0x800F2E80`, `0x800FAAEC` tetap belum diikat satu per satu ke setter lewat local def-chain.

Hipotesis:
- H1: +0x2EE adalah signed pending delta Chakra. Falsifier: tunjukkan computed consumer tidak mengalir ke shadow +0x04 lalu setter +0x18.
- H2: +0x2EE adalah antrean delta participant yang dipakai beberapa kelas event (debit, transfer, kredit), bukan selalu biaya tile. Falsifier: buktikan semua writer/consumer hanya beroperasi pada satu kelas transaksi. Makna gameplay setiap writer yang belum terikat = TIDAK TAHU.

## DX3 — selisih level dan nibble +0x20

Census CFG rooted `FUN_800D15A8`, `FUN_800EB434` (mencapai PC action-8 `0x800EC3A8`), dan `0x800EF3CC`:

- 237 `sll` immediate; 1 `sllv`.
- 3 `slti[u]` immediate 2: `0x800D2314`, `0x800D2BC0`, `0x800EF744`. Semua operand asalnya load dinamis; `0x800D2BC0` berasal dari byte action +0x2EB.
- 20 kandidat `subu`; tidak ada yang kedua operandnya terbukti berasal dari dua pembacaan nibble tile+0x20.
- 10 branch membandingkan nilai yang diturunkan dari read u16(tile+0x20), termasuk bits 8–11 dan bits 12–15.
- Tidak ada `mult` atau `mflo` reachable pada tiga root.
- Satu `1 << register`: `0x800EB7AC sllv $v0,$v0,$v1`, bytes `04 10 62 00`; nilai kiri 1 berasal dari `0x800EB7A8`, tetapi shift count berasal dari dynamic load global `0x8013EAEE` + 0xC. Tidak terbukti sama dengan d.
- 11 OR/ORI: 9 ORI di D15A8 berasal dari load global dinamis `0x80139EBF/0x80139EC3`; dua OR di EB434 menggabungkan load dinamis field +0xA dengan global `0x8013EBB0`. Tidak ada def-chain menuju store tile+0x20 dalam root yang diperiksa.

Jadi tidak ada instruksi yang terbukti menghitung d = selisih level atau 1<<d pada tiga root tersebut. Satu `sllv` literal 1 memang ada, tetapi register shift tidak terbukti d. Asal nilai OR yang membentuk nibble level = **TIDAK TAHU**; analisis writer/callee tile+0x20 di luar ketiga root masih diperlukan.

## DX4 — hipotesis pengguna, bukan data ROM

Observasi pengguna: d=1→100, d=2→400, d=3→800, d=4→1600. `fee_dasar` tetap simbolik. Tabel berikut memakai 100 hanya sebagai normalisasi asumsi pengguna.

| Model | Faktor d=1,2,3,4 | Prediksi setelah normalisasi | Konflik |
|---|---|---|---|
| H1 murni 2^d | 2, 4, 8, 16 | 200, 400, 800, 1600 | d=1 |
| H2 kasus khusus d=1 lalu faktor 4,8,16 | 1, 4, 8, 16 | 100, 400, 800, 1600 | Tidak ada pada empat titik |
| H3 tabel level doubling dari d=1 | 1, 2, 4, 8 | 100, 200, 400, 800 | d=2, d=3, d=4 |

H2 cocok dengan empat observasi tetapi belum dibuktikan di ROM. Falsifier H2: cari selector/lookup pada `0x800EC3A8` atau `0x800EF3CC` yang menghasilkan koefisien berbeda pada salah satu d. H1 sudah bertentangan di d=1; H3 sudah bertentangan di d=2–4. Tidak ada formula fee lompat level yang dinyatakan terverifikasi.

## Artefak mentah utama yang sudah ada

- `DX0_COMMIT_LEDGER.tsv`, `DX0_COUNTS.tsv`
- `DX1_ALL_PLUS1A_ACCESS.tsv`, `DX1_D15A8_WINDOW_PLUS1A.tsv`
- `DX2_ALL_PLUS2EE_ACCESS.tsv`, `DX2_PATH_CONDITIONS.tsv`, `DX2_TARGET_REACHABILITY.tsv`, `DX2_2EE_READERS_TO_SETTER.tsv`, `DX2_FUN_800EC574_CFG.tsv`, `DX2_HELPER_ONE_TO_PLUS2EE.tsv`
- `DX3_OPERATION_CENSUS.tsv`, `DX3_LEVEL_DIFFERENCE_CANDIDATES.tsv`, `DX3_LEVEL_NIBBLE_COMPARISONS.tsv`, `DX3_LEVEL_NIBBLE_OR_SOURCES.tsv`, `DX3_ONE_SHIFT_PATTERNS.tsv`, `DX3_TILE_PLUS20_READ_WRITE.tsv`
- `DX4_USER_OBSERVATION_MODEL_COMPARISON.tsv`
- Computed-pointer consumer raw instructions: `reports/stage1_economy/aq1-run-41390871544/attempt-1/aq1-deep-context.tsv`.

Tidak mengubah `STATUS.md`, workflow, visibilitas repo, atau Release. Tidak ada biner, emulator, BIOS, savestate, dump, video atau frame yang dikomit.
