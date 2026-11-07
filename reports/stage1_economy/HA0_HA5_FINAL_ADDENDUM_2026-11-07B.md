# HA0–HA5 — addendum akhir setelah probe bound dan CONTROL H6 (2026-11-07)

Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`, branch `main`. Game: SLPS-03553.
Baseline inklusif: `14dccd2e1d2f92b1b919ad7f0686bf019c71dbf4`.
HEAD sebelum commit addendum ini: `cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09`.
EXE SHA-256: `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
DATA.BIN Entry 1 SHA-256: `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`.

## Putusan akhir per tugas

| Tugas | Status | K | Putusan |
|---|---|---:|---|
| HA0 — Ledger | TUNTAS | K4 | 20 commit inklusif: 13 manusia, 7 bot; 9 Actions run bersumber dari SHA dalam rentang. Monitor 42320736860 dicatat terpisah karena SHA-nya sebelum baseline. |
| HA1 — Koreksi | TUNTAS | K4 | Offset Entry 1, dua negu, store windows, excerpt helper 16+3 dan koreksi permalink terdokumentasi. |
| HA2 — Statis helper, bound, tabel, F2A9C dan caller | TUNTAS untuk lingkup statis | K4 | FUN_800154D4, initializer, bound sentinel 52, 52 nilai tabel, tiga store, 9 return logis, dan scan indirect-call diekspor serta diperiksa. Runtime order initializer dan caller komputasi yang mungkin di luar scan tetap TIDAK TAHU. |
| HA3 — Konsumen manager+0x2EE | SEBAGIAN | K3 | 23 akses manager-backed, 12 write register non-zero, dan tiga reader dipetakan. Terminal wallet permanen dan dua indeks zero-writer belum dibuktikan. |
| HA4 — CONTROL H6 | TUNTAS | K4 | Satu launch: SaveStateLoaded lulus, load call kembali, 180 VSync pasca-restore, PCSX exit 0; tanpa input dan tanpa watchpoint. Workflow keseluruhan gagal hanya pada langkah publikasi ringkasan; hasil CONTROL dipulihkan dari log dan dikomit. |
| HA5 — Prediksi simbolik | TUNTAS sebagai katalog prediksi | K3 | Empat model d=1..4 dan prediksi tiga store diturunkan. Rumus biaya game dan hubungan x=d belum dibuktikan. |

K5 tidak diberikan: hanya satu CONTROL launch pada HA4. Hasil tersebut membuktikan pemulihan checkpoint pada satu peluncuran, bukan konsistensi dua peluncuran atau penyelesaian Story Mode.

## HA0 — Ledger Git dan semua Actions run

Dari baseline inklusif sampai HEAD addendum ini terdapat **20 commit: 13 manusia dan 7 bot**. Jumlah ini menghitung commit baseline itu sendiri. Sebelum commit laporan ini, compare mencatat 18 commit sesudah baseline (11 manusia, 7 bot); commit addendum ini menambah satu commit manusia.

### Semua run dengan source SHA dalam rentang baseline–HEAD

| Run | Event | Workflow/job | Source SHA | Hasil Actions | Exit / catatan |
|---:|---|---|---|---|---|
| 42338608063 | push | HA2–HA3 / `ha2-ha3-static` | `58db32c696fe830b6558c6828529a3801be753e0` | job success | analisis skrip exit 1; py_compile 0, dua ekspor Ghidra 0; bukan hasil analisis final |
| 42338608064 | push | Ghidra / `analyze-main-exe` | `58db32c696fe830b6558c6828529a3801be753e0` | success | exit 0; target missing 0 |
| 42339837743 | push | HA2–HA3 / `ha2-ha3-static` | `b65ef33c4fc0f4d67e2258ebf77a528000a78241` | success | exit 0; py_compile, Ghidra EXE/Entry1, scan, cleanup lulus |
| 42342367468 | push | HA2 bound probe | `e5b92bf27e939771699e8b35fdc5e8f92e13d429` | failure | exit 99; py_compile 99; percobaan awal gagal |
| 42342464750 | push | HA2 bound probe | `aeb027f020b8f6c850f6e34ea58e0b04efd483bf` | success | exit 0 |
| 42342593255 | push | HA2 bound probe | `437db807195f75431590ac3989bcbe5591c96bb2` | success | exit 0; compile dan probe lulus |
| 42342725357 | push | HA2 bound probe | `7e10c6d04ec936dd603be8355894d96d0767af42` | success | exit 0; compile, ekstraksi, probe dan cleanup lulus |
| 42349173401 | push | HA4 one-launch CONTROL | `f11b28751b38b44201ca9416c1d77054186b9468` | failure pada job publikasi | script CONTROL exit 0, PCSX exit 0; kegagalan exit 128 karena langkah Git berjalan dari `WORK/source`, bukan checkout |
| 42349259001 | schedule | Story Mode adaptive-player monitor / `monitor` | `f11b28751b38b44201ca9416c1d77054186b9468` | success | exit 0; tidak ada player run yang terlihat pada 50 run terbaru; monitoring-report/artifact tidak dibuat |

**Total run dalam rentang: 9.** Monitor terjadwal 42349259001 termasuk karena source SHA-nya berada dalam rentang, walau event-nya `schedule`.

Monitor terjadwal 42320736860 juga diperiksa dan dicatat, tetapi **di luar rentang**: source SHA `6987a76e12b0adf86f8061d47dcc4078e79cda21` mendahului baseline. Run itu success; log menyatakan tidak menemukan adaptive-player run pada 50 run terbaru, tidak menghasilkan monitoring-report, dan tidak mengunggah artifact. Ini tidak membuktikan kemajuan Story Mode.

### Commit yang dibuat dalam sesi addendum ini

1. `f11b28751b38b44201ca9416c1d77054186b9468` — manusia. Berkas: `.github/workflows/ha4-h6-control.yml`; `experiments/ha4_h6_control.py`.
2. `5f99df7dc7e8caf4678502cf66a192e876af8458` — manusia. Berkas: `reports/stage1_economy/ha4-control-run-42349173401/attempt-1/HA4_CONTROL_SUMMARY.txt`; `ACTIONS_RUN_SUMMARY.txt`; `cleanup.txt`.
3. `cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09` — manusia. Berkas: `reports/stage1_economy/monitor-run-42349259001/ACTIONS_RUN_SUMMARY.txt`.
4. Commit addendum ini — manusia. Berkas: `reports/stage1_economy/HA0_HA5_FINAL_ADDENDUM_2026-11-07B.md`.

Tidak ada berkas lama yang ditimpa. `STATUS.md` tidak diubah; blob yang diperiksa sebelumnya tetap `ee7b9c226631c71cae1c9fb0270994ccf3e67c07`. Release `naruto-checkpoint-39262213468` tidak diubah.

## HA1 — Koreksi final

Rumus Entry 1 yang digunakan:

`file_offset = 0x10BB000 + (PC - 0x800AD450)`.

- `0x800F7E64 - 0x800AD450 = 0x4AA14`; hasil file offset `0x01105A14`.
- `0x800F7E68 - 0x800AD450 = 0x4AA18`; hasil file offset `0x01105A18`.
- PC `0x800F2E0C`, offset `0x011009BC`, bytes `23 10 02 00`: `negu $v0,$v0`.
- PC `0x800F2E64`, offset `0x01100A14`, bytes `23 10 02 00`: `negu $v0,$v0`.

Helper `0x8001552C` dipecah 16+3 instruksi. Window store F2CF8/F2E38/F2E68 berjumlah 6/14/7 instruksi. Excerpt kontigu tetap dibatasi 16 instruksi per file.

Koreksi permalink: tautan lama yang memuat tracking parameter atau SHA tidak utuh 40 karakter dicabut. Hanya raw permalink tanpa query dan SHA penuh yang dipakai pada laporan ini.

## HA2 — FUN_800154D4, bound, tabel, F2A9C

### Bound dan helper

Body `FUN_800154D4` adalah tiga instruksi:
`lw $v0,0x118($gp)`; `jr $ra`; `nop`. Fungsi mengembalikan isi slot GP+0x118, simbol statis `DAT_8006D794`.

Initializer pada `0x800121AC`:
1. Menulis nol ke GP+0x118.
2. Membaca tag pada `0x80055CEC + 16*i`.
3. Membandingkan tag dengan `0xFFFFFFFF`.
4. Menaikkan indeks sampai sentinel pertama.
5. Menulis indeks sebelum sentinel ke GP+0x118.

Sentinel pertama ada pada indeks **52** (VA `0x8005602C`, file offset EXE `0x4682C`). Maka nilai yang dihitung initializer secara statis adalah `B=52=0x34`. Namun nilai image mentah di VA `0x8006D794` adalah nol; angka 52 adalah hasil initializer, dan urutan pelaksanaan initializer sebelum pemanggilan helper belum dibuktikan di runtime.

Helper mengambil nilai pada `0x80055CF4 + 16*x` jika `u32(x)<B`; selain itu mengembalikan nol. Caller mendeklarasikan hasil sebagai `short`; nilai mentah tabel diekspor sebagai u32.

### Isi tabel

Keempat TSV memuat indeks 0–51. Hasil cek ulang independen:
- 52 baris tabel: indeks berurutan, alamat, offset, little-endian bytes dan u32 cocok; 0 kesalahan.
- 53 baris sentinel scan: alamat, offset, bytes dan u32 cocok; sentinel pertama indeks 52; 0 kesalahan.
- Tabel memiliki minimum u32 `0x00000000` dan maksimum `0xFFFFFFE7`.
- Ringkasan probe: 48 pasangan rasio berurutan dengan denominator non-zero, 3 pasangan denominator zero; rasio teramati minimum 0 dan maksimum `2147483623/100`. Tidak dilakukan fitting.

Untuk lookup d=1..4, nilai tabel pada indeks 1,2,3,4 adalah **150, 100, 75, 200**. Ini nilai bytes statis, bukan bukti bahwa indeks runtime x sama dengan d.

### Tiga store dan pengisi register

Definisikan `M=u32(0x8013EA74)`, `idx=u32(0x8013EB0C)`, `G=u8(0x8013EA71)`, `Q=u32(0x80139EFC)`, dan `x` sebagai nilai yang dibaca dari manager record `+0x530`. Dengan `H(x)=s16(u32[0x80055CF4+16*x])` jika `x<52`, selain itu nol:

- `0x800F2CF8`: `sh u16(LO32(H(x)*(G-2)))` ke `M+2*idx+0x2EE`.
- `0x800F2E38`: `sh u16(LO32((-H(x))*(G-1-Q)))` ke `M+2*idx+0x2EE`.
- `0x800F2E68`: `sh u16(-H(x))` ke `M+2*idx+0x2EE`.

Register-fill utama di F2A9C diperiksa pada raw instruction TSV: `lbu G`, `lw Q`, `and 0x1000`, `mult/mflo`, `subu`, `addiu`, pembacaan manager `+0x530`, pembacaan `0x8013EB0C), dan tiga store. Negu pada F2E0C/F2E64 menegasikan nilai helper dalam `$v0`, bukan nol.

### Return dan caller

Fungsi F2A9C bertipe C `void`; sembilan return logis berbagi satu epilog fisik di `0x800F30F8`. Maka tidak ada nilai ABI yang sah untuk disebut return `$v0`. Residual MIPS `$v0` pada sembilan jalur:

| Jalur/PC menuju epilog | Residual `$v0` sebelum epilog |
|---|---|
| `0x800F2B2C`, bila `FUN_80104E1C()` non-zero | Return dinamis `FUN_80104E1C` |
| `0x800F2AE8`, jalur struktural `stage<2` nonzero | 1 dari `slti`; secara nilai stage biasa jalur ini didahului guard stage=1 |
| `0x800F2AFC`, stage bukan 2 dan bukan jalur awal | `0x80140000` dari `lui $v0,0x8014` |
| `0x800F2B1C`, setup stage 0 | 1 |
| `0x800F2EF8`, selesai pemrosesan stage 1 | `0x80140000` |
| `0x800F2F94`, jumlah pending belum sama dengan G | Nilai count yang dimuat dari `0x8013EBB0` |
| `0x800F2FB0`, wait counter masih di bawah ambang | `0x80140000` |
| `0x800F30CC`, flag manager mengarahkan state 8 | `0x80140000` |
| jalur akhir melalui `0x800F30E0` | `0x20` pada jalur negatif, atau `0x18` pada jalur lain |

Caller langsung yang ditemukan: JAL di `0x800F5F54` dari `FUN_800F3658`. File kandidat indirect caller `jalr`/table-`jr` kosong; tidak ada kandidat terkonfirmasi dari scan tersebut. Keberadaan dispatch tak langsung yang dibangun secara dinamis di luar cakupan scan tetap TIDAK TAHU.

## HA3 — Konsumen terminal dan indeks

Census manager-backed `+0x2EE` berjumlah 23 akses: **20 WRITE dan 3 READ**. WRITE terdiri atas 12 nilai register/non-literal-zero dan 8 literal-zero. Dua zero-writer tambahan `0x800B24C8` dan `0x800BEDA4` memiliki basis manager teridentifikasi, tetapi derivasi indeks individualnya belum dipulihkan.

Dua belas WRITE non-zero dan asal indeks:
- `0x800D46F8`: indeks dari halfword global `0x8013EA6E`, diskalakan ×2.
- `0x800DC4FC`, `0x800DD088`, `0x800E408C`, `0x800E66E8`, `0x800E9E88`, `0x800F0F08`: indeks dari `0x8013EA88), diskalakan ×2.
- `0x800DD178`: indeks dari nibble owner tile `(u16(tile+0x20)>>12)`, lalu ×2.
- `0x800ECBB8`: indeks dari `0x8013EBB0), diskalakan ×2.
- `0x800F2CF8`, `0x800F2E38`, `0x800F2E68`: indeks dari `0x8013EB0C), diskalakan ×2.

Delapan zero-writer literal-zero: `0x800B24C8`, `0x800B2EEC`, `0x800B36BC`, `0x800BEDA4`, `0x800D1738`, `0x800D1764`, `0x800E6A78`, `0x800ED6B8`. Asal indeks per-site untuk dua writer yang disebutkan di atas tetap belum dibuktikan.

Tiga reader:
1. `0x800F2E80` dalam F2A9C membaca slot, memeriksa sign dan mengubah byte status participant `+0x22`; kemudian fase menghitung slot pending dan menentukan state manager `+0x2E9).
2. `0x800DCFE8` dalam DC2E0: beberapa state menghitung slot pending non-zero dan menunggu sampai nol. Pada case 1, nilai slot dibawa ke manager `+0x4F4`; case 2 menghitung `manager+0x4F0 = participant_record+4 + manager+0x4F4`, lalu meneruskan owner dan nilai absolut ke `FUN_80014F10`, kemudian menghapus nilai sementara. Ini membuktikan alur nilai sementara/settlement, tetapi bukan store ke wallet permanen. Body terminal `FUN_80014F10` belum diperiksa.
3. `0x800FAAEC` dalam FAAC8 hanya melanjutkan timer/state ketika slot peserta nol dan field manager terkait nol; ia mengurangi timer `+0x350/+0x34C`, menjalankan helper dan membersihkan flag. Ini gerbang timer/animasi, bukan bukti debit wallet.

Hipotesis yang masih terbuka:
- **H1 — antrean delta/settlement signed.** Dukungan: store F2A9C membentuk nilai signed dari H(x), G dan Q; DC2E0 memindahkan nilai slot ke `+0x4F4`, menggabungkannya secara sementara di `+0x4F0`, lalu memanggil fungsi lanjutan dengan owner dan abs(amount). Falsifier: tunjukkan bahwa terminal hanya menggambar/menganimasikan nilai dan tidak ada perubahan wallet otoritatif.
- **H2 — cache/status/presentasi peserta.** Dukungan: tanda nilai slot mengubah status record `+0x22`; reader F2A9C/DC2E0/FAAC8 memakai nol/non-zero untuk menahan atau memajukan fase dan timer. Falsifier: bukti bahwa nilai slot mencapai wallet setter permanen dan saldo berubah dengan jumlah terkait.

Makna gameplay final `+0x2EE`, terminal wallet permanen, dan apakah field participant `+0x4` adalah saldo ekonomi authoritative masih TIDAK TAHU.

## HA4 — Satu CONTROL H6 tanpa watchpoint

Artifact aktif diverifikasi:
- Run sumber `39907655833`, artifact ID `12482055310`.
- Nama artifact `naruto-storymode-adaptive-player-private`, ukuran ZIP 11.407.011 byte, SHA-256 `a0f45156dfd489f24c8dc8e122c33a048c7b9ac34b935ac828523593d21ca2a8`.
- File `adaptive-cycle-02-f180.sstate`, ukuran 21.162.799 byte, SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`.

Run CONTROL `42349173401`, source SHA `f11b28751b38b44201ca9416c1d77054186b9468`, job `128333421081`:
- exactly one PCSX-Redux headless launch;
- `ExecutionFlow::SaveStateLoaded` = PASS;
- `PCSX.loadSaveState` returned;
- 180 VSync after restore;
- PCSX/script exit code 0;
- no gameplay input, no watchpoints, no RAM export, no screenshot/video committed;
- private inputs and emulator workspace removed successfully.

**Perbedaan penting:** conclusion job Actions adalah failure karena commit summary step menjalankan Git saat working directory masih `WORK/source`, sehingga muncul `fatal: not in a git directory` (exit 128). CONTROL sendiri telah lulus. Ringkasan teks dari log dipulihkan dan dikomit manual dalam commit `5f99df7dc7e8caf4678502cf66a192e876af8458`; run tidak diulang.

## HA5 — Prediksi simbolik d=1..4

Tabel di bawah adalah prediksi nilai helper untuk tiap model. Tiga formula store di atas diterapkan pada setiap `H_model(d)`; hasil akhir store adalah low 16-bit karena instruksinya `sh`.

| Model | d | H_model(d) | Store F2CF8 sebelum low16 | Store F2E38 sebelum low16 | Store F2E68 sebelum low16 |
|---|---:|---:|---|---|---|
| Linear | 1 | C | C(G-2) | -C(G-1-Q) | -C |
| Linear | 2 | 2C | 2C(G-2) | -2C(G-1-Q) | -2C |
| Linear | 3 | 3C | 3C(G-2) | -3C(G-1-Q) | -3C |
| Linear | 4 | 4C | 4C(G-2) | -4C(G-1-Q) | -4C |
| Eksponensial | 1 | C | C(G-2) | -C(G-1-Q) | -C |
| Eksponensial | 2 | 2C | 2C(G-2) | -2C(G-1-Q) | -2C |
| Eksponensial | 3 | 4C | 4C(G-2) | -4C(G-1-Q) | -4C |
| Eksponensial | 4 | 8C | 8C(G-2) | -8C(G-1-Q) | -8C |
| Akumulasi | 1 | C | C(G-2) | -C(G-1-Q) | -C |
| Akumulasi | 2 | 3C | 3C(G-2) | -3C(G-1-Q) | -3C |
| Akumulasi | 3 | 7C | 7C(G-2) | -7C(G-1-Q) | -7C |
| Akumulasi | 4 | 15C | 15C(G-2) | -15C(G-1-Q) | -15C |
| Lookup | 1 | 150 | 150(G-2) | -150(G-1-Q) | -150 |
| Lookup | 2 | 100 | 100(G-2) | -100(G-1-Q) | -100 |
| Lookup | 3 | 75 | 75(G-2) | -75(G-1-Q) | -75 |
| Lookup | 4 | 200 | 200(G-2) | -200(G-1-Q) | -200 |

Lookup memakai H(1..4) dari tabel static dengan asumsi **x=d**. Jika record `+0x530` memuat nilai lain, baris lookup tidak berlaku untuk perbedaan level d tersebut. Tidak ada angka dari observasi pengguna yang dipakai dan tidak ada fitting.

Falsifier/runtime discriminator yang sesuai: pada event yang sama, catat record pointer, `x=*(u32*)(record+0x530)`, G, Q, `idx=0x8013EB0C`, manager base M, effective address `M+2*idx+0x2EE`, nilai lama/baru serta PC store F2CF8/F2E38/F2E68. Telusuri `FUN_80014F10` dan writer wallet authoritative sebelum memberi label biaya atau debit.

## Validasi TSV dan TIDAK TAHU

Validasi yang dapat dipastikan:
- Validator instruksi run 42339837743: 389 TSV instruksi, 6.275 baris, 0 invalid rows; offset EXE/Entry1 dicatat dan excerpt kontigu maksimum 16 instruksi.
- Pemeriksaan ulang saya untuk tabel helper: 52/52 entry; alamat, file offset, bytes dan u32 cocok.
- Pemeriksaan ulang sentinel: 53/53 entry; alamat, file offset, bytes dan u32 cocok; sentinel pertama pada indeks 52.
- Kedua kelompok TSV tabel tersebut memiliki 0 kesalahan. Total 105 baris data tabel/sentinel diperiksa ulang; tidak dihitung sebagai instruksi.

TIDAK TAHU yang masih sah:
1. Apakah initializer bound sudah selalu dijalankan sebelum setiap panggilan helper di seluruh alur runtime.
2. Apakah `x` dari manager record `+0x530` sama dengan selisih level d.
3. Apakah `FUN_80014F10` mengubah wallet permanen, menampilkan angka, atau melakukan keduanya.
4. Apakah participant record `+0x4` adalah wallet authoritative dan semua jalur perubahan saldo.
5. Indeks per-site untuk zero-writer `0x800B24C8` dan `0x800BEDA4`.
6. Ada/tidaknya caller indirect yang dibangun dinamis di luar scan jalr/table-jr yang diekspor.
7. Semantik gameplay menyeluruh dari manager `+0x2EE`, tabel lookup, dan terminal settlement.
8. Story Mode selesai atau tidak; monitor Actions bukan pengukur penyelesaian permainan.

## Raw evidence permalinks

Seluruh URL berikut memakai raw.githubusercontent.com, SHA penuh 40 karakter, tanpa query parameter.

### HA1
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/HA1_CORRECTION_ADDENDUM_2026-11-07.md
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/HA1_HELPER_8001552C_00.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/HA1_HELPER_8001552C_01.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/HA1_NEGU_ROWS.tsv

### HA2–HA3
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA2_FUN_800154D4_00.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA2_F2A9C_KEY_INSTRUCTIONS.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA2_F2A9C_RETURN_PATHS.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA2_F2A9C_INDIRECT_CALL_CANDIDATES.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA2_HA3_STATIC_SUMMARY.txt
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA_TSV_VALIDATION_SUMMARY.txt
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA3_MANAGER_2EE_INDEXED_CENSUS.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA3_INDEX_ORIGIN_INSTRUCTIONS.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA3_READ_800F2E80_IN_F2A9C.txt
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA3_READ_800DCFE8_IN_DC2E0.txt
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA3_READ_800FAAEC_IN_FAAC8.txt

### Bound dan isi tabel
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-bound-table-run-42342725357/attempt-1/ACTIONS_RUN_SUMMARY.txt
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-bound-table-run-42342725357/attempt-1/HA2_BOUND_TABLE_SUMMARY.txt
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-bound-table-run-42342725357/attempt-1/HA2_BOUND_INITIALIZER_00.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-bound-table-run-42342725357/attempt-1/HA2_BOUND_INITIALIZER_01.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-bound-table-run-42342725357/attempt-1/HA2_TABLE_U32_000.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-bound-table-run-42342725357/attempt-1/HA2_TABLE_U32_001.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-bound-table-run-42342725357/attempt-1/HA2_TABLE_U32_002.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-bound-table-run-42342725357/attempt-1/HA2_TABLE_U32_003.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-bound-table-run-42342725357/attempt-1/HA2_BOUND_SENTINEL_SCAN_000.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-bound-table-run-42342725357/attempt-1/HA2_BOUND_SENTINEL_SCAN_001.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-bound-table-run-42342725357/attempt-1/HA2_BOUND_SENTINEL_SCAN_002.tsv
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha2-bound-table-run-42342725357/attempt-1/HA2_BOUND_SENTINEL_SCAN_003.tsv

### HA4 dan monitor
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/experiments/ha4_h6_control.py
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/.github/workflows/ha4-h6-control.yml
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha4-control-run-42349173401/attempt-1/HA4_CONTROL_SUMMARY.txt
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha4-control-run-42349173401/attempt-1/ACTIONS_RUN_SUMMARY.txt
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/ha4-control-run-42349173401/attempt-1/cleanup.txt
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cf23c20cda4bd6731f2aaa4c90780a3a9d6fdb09/reports/stage1_economy/monitor-run-42349259001/ACTIONS_RUN_SUMMARY.txt

## Batas bukti akhir

Tidak ada ISO/ROM/EXE/DATA.BIN/BIOS/savestate/RAM dump/video/frame/biner yang dikomit. Satu CONTROL launch memang dijalankan sebagai satu-satunya tugas runtime; tidak ada watchpoint dan tidak ada input gameplay. Status CONTROL tidak membuktikan biaya upgrade atau penyelesaian Story Mode.
