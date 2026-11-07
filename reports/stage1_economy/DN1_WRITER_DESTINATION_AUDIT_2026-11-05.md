# DN1 - resolusi tujuan store untuk 272 PC +0x10..+0x18

Status: **TUNTAS - K4 (statis)** untuk tujuan 272 PC yang diminta.

## Cakupan
- Ghidra DATA.BIN Entry 1 base 0x800AD450, panjang 0x919BC, ujung eksklusif 0x8013EE0C.
- 272/272 PC unik ter-decode sebagai store; 272/272 memiliki 12 instruksi pra-store.
- Raw excerpt maksimum 52 byte; tidak ada PC hilang/duplikat.

## Tujuan store
| Kategori | PC | Bukti |
|---|---:|---|
| Stack frame langsung (sp + displacement) | 245 | Base operand adalah sp. |
| Stack frame computed | 5 | Empat addu memakai sp; PC 0x800F7528 menulis local_28 dengan a0=sp+i*4. |
| Auxiliary buffer EA74, stride 0x90 | 22 | Pointer dimuat dari [0x8013EA74], indeks record dikalikan 0x90. |
| Tile array EA84, stride 0x124 | **0** | Tidak satu pun dari 272 store menulis tile array. |

### Bukti 22 auxiliary
- FUN_800B5790: -0x158c(s3) membaca slot 0x8013EA74; index*0x90.
- FUN_800BB36C: a3=0x80140000; lw -0x158c(a3) membaca 0x8013EA74; index*0x90. Fungsi yang sama membaca tile pointer EA84/stride 0x124 untuk seleksi tile, tetapi menulis hasil hitung ke buffer auxiliary +0x14.
- FUN_800D15A8, FUN_800D6E7C, FUN_800EC574: -0x158c(s1) ke a1, kemudian index*0x90.
- FUN_800DF0C8: -0x158c(s0) ke a0, kemudian index*0x90.

### Bukti stack computed
- 0x800B7AE0 dan 0x800B7AEC (FUN_800B78E4): addu v0,sp,a1.
- 0x800CAF50 (FUN_800CADB8): addu v0,sp,t7.
- 0x800B9198 (FUN_800B83FC): addu v0,sp,v1.
- 0x800F7528 (FUN_800F7450): a0=sp+i*4, tujuan local_28.

## Writer tile yang terbukti
Sepuluh store di FUN_800F7ADC: 0x800F7CE8, 0x800F7CFC, 0x800F7D0C, 0x800F7D20, 0x800F7D30, 0x800F7D44, 0x800F7D54, 0x800F7D68, 0x800F7D78, 0x800F7D8C. Store sh ini menyalin resource cursor +0x0A..+0x13 ke EA84 + tile_index*0x124 + lima offset LV. Label: LOADER_COPY, bukan COMPUTED.

Rekonsiliasi census 326 PC langsung: 10 LOADER_COPY, 316 LAIN, 0 COMPUTED. Dari 316 LAIN, 44 sudah diklasifikasi sebelumnya sebagai 24 stack, 17 allocated object, 3 auxiliary; 272 tambahan diselesaikan di sini. Ini bukan klaim bahwa semua jalur pointer-pre-adjusted/indirect di seluruh binary telah dieliminasi.

## HT vs HC
- HT (LV disalin dari resource): didukung K4 dalam scope census; semua sepuluh writer tile yang terbukti adalah copy resource. Tidak ada tujuan tile dari 272 PC.
- Falsifier HT: satu non-loader store dengan destination EA84 + index*0x124 + LV field dan nilai level dihitung, bukan disalin. Belum ditemukan dalam 326 candidate PC.
- HC (ada computed tile writer): tidak ditemukan pada 326 candidate PC; nilai computed yang tampak justru ditulis ke stack/auxiliary.
- Falsifier HC: audit exhaustif terhadap pointer-pre-adjusted/indirect writes menunjukkan semua penulis EA84 LV hanya sepuluh PC loader-copy. Audit global jalur indirect belum tuntas; kesimpulan dibatasi pada census direct-displacement.

## Lookup LV
LV2 = 10 × ceil(11X/100) cocok 415/415 record DK1. LV1, LV3, LV4, LV5 tetap TIDAK TAHU sebagai rumus universal; X/2 cocok 200/248 nonzero; H1 LV3-LV5 15/39 dan H2 1/39.

## Run
Run 42338608064, job id TIDAK_TAHU, job analyze-main-exe, source SHA 58db32c696fe830b6558c6828529a3801be753e0, success, exit code 0. Statis saja; tanpa emulator/savestate. Tidak mengubah STATUS.md, Release, atau visibilitas repo.
