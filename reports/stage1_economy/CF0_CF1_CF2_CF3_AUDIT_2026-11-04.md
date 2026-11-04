# CF0–CF3 — koreksi CE3, audit statis dan hipotesis ekonomi
Tanggal: 4 November 2026
Game: Naruto — Shinobi no Sato no Jintori Gassen (SLPS-03553)
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Rentang ledger: eksklusif `cd90b281f45cada726e80c3f87661e5ae5494303` sampai inklusif HEAD `012367cf0518e519520fe590845d62792289276a`
Status compare Git: ahead 98, behind 0; 144 path unik dalam diff.

## Skala keyakinan dan batas
- K0: tidak ada bukti.
- K1: hipotesis/pengamatan pengguna saja; bukan konfirmasi kode atau runtime.
- K2: indikasi terbatas dari satu jalur/log/launch.
- K3: beberapa bukti statis saling mendukung, tetapi alias pointer, pemanggil atau cakupan belum lengkap.
- K4: byte/instruksi statis langsung dapat diperiksa.
- K5: perilaku runtime terkonfirmasi pada sedikitnya dua peluncuran independen.
Statis dibatasi maksimum K4. Pengamatan pengguna tidak dinaikkan di atas K1.

## Ringkasan status

| Butir | Status | K | Putusan |
|---|---|---:|---|
| CF0 koreksi CE3 run 41749255678 | TUNTAS | K4 | Status workflow/job dipisahkan dari exit kode script; akar penyebab adalah gate preflight EA8 nonzero. |
| CF1(a) pembeda action 3/8 dan gate action 8 | SEBAGIAN | K4 untuk test action 8 | Bytes pembanding action==8 ditemukan; branch spesifik action==3 tidak terbukti. |
| CF1(b) FUN_80102408 + semua penulis EA8 | SEBAGIAN | K3 | Pembaca EA8 diketahui; semua penulis dan 12 instruksi pra-store BELUM dipastikan. |
| CF1(c) nibble +0x20 di FUN_800E3E74 dan pembaca/caller | SEBAGIAN | K3 | Empat store terbukti sebagai mask/OR dari field sumber; bukan old+1; caller langsung dan asal semantik field belum lengkap. |
| CF1(d) census u16 +0x0E/+0x1A | SEBAGIAN | K3 | 29 instruksi lhu kandidat; displacement/base alias belum terbukti dan scope scanner tidak meliputi seluruh alur kontrol. |
| CF2 hipotesis biaya lompat/bangun + makna event 3 | SEBAGIAN | K1–K3 | Hipotesis bersaing dan falsifier ditulis; biaya lompat d>=2 dan build netral belum diputuskan. |
| CF3 H6 runtime sesuai syarat (2 launch, read-only, semua frame/watchpoint) | BELUM | K2 parsial; K5 BELUM | Run tersedia hanya satu launch dan melakukan fixture pokes; gate menghentikan state 2 sebelum setter. |

---

## CF0 — status, exit code, dan penyebab dari log mentah
**TUNTAS K4 untuk koreksi laporan; uji kredit positif tetap SEBAGIAN K2 / belum membuktikan kredit.**

Run `41749255678`:
- Workflow GitHub Actions: `completed`, `conclusion=success`.
- Job `ce3-h6-positive-credit-probe`, job ID `126309939178`: `completed`, `success`.
- Source SHA: `b2ccb20041c31496b23ce531eec3434753db7868`.
- File ringkasan test: `STATUS=SEBAGIAN`, `EXIT_CODE=2`.
- Proses script CE3 exit desimal **2**; wrapper/launch exit desimal **73**.
- Satu launch, tile 4 / level 0 / attempt 1; durasi 145.779 detik.
- Step 0 build/validasi lulus; error bukan berasal dari Step 0.

**Log mentah yang menentukan** dari `CE3_FIRST_NONPASS_TILE4_LEVEL0_ATTEMPT1.txt`:
```text
CE3_STATE1_RETURN phase=2
CE3_STATE2_GLOBAL_POINTER_8013A22C=0x801CDF80
CE3_STATE2_GATE_POINTER_VALID=YES
CE3_STATE2_GATE_FIELD_PLUS4=0x801CEC88
CE3_STATE2_GATE_FIELD_PLUS_EA8=0xFFFFFFFE
CE3_STATE2_GATE_PREDICTED_RETURN=4294967294
CE3_RAW_ERROR=.../launches/tile-4-level-0-attempt-1/ce3.lua:186: STATE2_GATE_PREFLIGHT_BLOCK field4=0x801CEC88 fieldEA8=0xFFFFFFFE predicted=4294967294
CE3_CALL_STATUS=FAIL
```

Penyebab yang dapat dinyatakan: preflight read-only meniru `FUN_80102408`; pointer global valid, `pointer+4` nonzero, sehingga helper memprediksi return `0xFFFFFFFE` (4294967294), bukan 0. Harness sengaja menghentikan peluncuran sebelum state 2. Ini **bukan** error `8-bit read from unknown address: ffffd138`; pesan alamat tersebut milik run lama `41740957322`, bukan log terbaru. Jangan gunakan error lama sebagai penyebab run 417492.

Ringkasan Actions yang telah ada di repo (status, job, SHA, exit code):
`reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/ACTIONS_RUN_SUMMARY.txt`

Permalink raw pada snapshot HEAD audit:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/012367cf0518e519520fe590845d62792289276a/reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/ACTIONS_RUN_SUMMARY.txt

---

## CF1 — bukti statis

### CF1(a) byte pembeda action 3/8 dan gate action 8
**SEBAGIAN K4.** Pada `FUN_800D15A8`, PC `0x800D3E50` membaca action byte manager+`0x2EB`, membandingkannya dengan 8, lalu branch bila bukan 8:

```text
PC 0x800D3E50  EB 02 43 90   lbu v1,0x2eb(v0)
PC 0x800D3E54  08 00 02 24   li  v0,0x8
PC 0x800D3E58  5F 00 62 14   bne v1,v0,0x800D3FD8
raw bytes: EB 02 43 90 08 00 02 24 5F 00 62 14  (12 byte)
```

Interpretasi yang sah: action byte **8** mengambil jalur khusus; nilai selain 8 melewati blok itu. Ini tidak membuktikan bahwa semua nilai non-8 adalah action 3. Branch literal khusus action 3 belum ditemukan, maka jangan menamai jalur default sebagai action 3 tanpa bukti tambahan.

Pemeriksaan gate action 8 yang sudah ditopang byte statis:
- PC `0x800D2614`: baca lagi `lbu v1,0x2EB(v0)`; `0x800D2618` memuat 8; `0x800D261C` branch jika bukan 8 ke `0x800D2630`.
- Jalur berikutnya memanggil `FUN_80100F64`; return nonzero melewati jalur.
- Gate tile yang tercatat pada CE0/CE1: tile type 5, owner bits 12–15 sama dengan pemain aktif, fee `u16(tile+0x1A)` tidak melebihi saldo kerja, dan level nibble bits 8–11 setelah +1 masih di bawah 5.
- `lhu tile+0x0E` pada PC `0x800D2768` bukan bukti bahwa nilai itu menjadi debit transaksi.

### CF1(b) FUN_80102408 dan penulis [pointer+0xEA8]
**SEBAGIAN K3.** Potongan pembaca `FUN_80102408` yang ada pada laporan CE3:

```text
80102408  lui v0,0x8014
8010240c  lw  v1,-0x5dd4(v0)   ; pointer global 0x8013A22C
80102414  lw  v0,0x4(v1)
8010241c  beq v0,zero,0x80102430
80102424  lw  v0,0xea8(v1)
80102428  jr  ra
80102430  jr  ra               ; return -1 disiapkan melalui delay-slot
```

Helper membaca global pointer `0x8013A22C`; apabila `pointer+4 == 0`, return -1; selain itu return nilai `pointer+0xEA8`. Log CF0 mengukur objek runtime `0x801CDF80` dan membaca EA8 sebagai `0xFFFFFFFE`.

**BELUM:** tidak ada census statis lengkap yang mencantumkan semua store ke `[0x801CDF80+0xEA8]`, PC/fungsi dan 12 instruksi sebelum setiap store. File AQ1 yang tersedia tidak membuktikan daftar store itu. Tiga callsite helper yang terlihat (`0x800EA1C8` di `FUN_800ea18c`, `0x800D09BC` di `FUN_800d05b8`, `0x800DFA1C` di `FUN_800df698`) adalah pemanggilan pembaca helper, **bukan** bukti penulis EA8. Pesan cakupan mentah dari artefak census: `interpretation=direct Ghidra references only; indirect aliases and runtime writers may not appear`. Maka daftar penulis dan instruksi pra-store: **TIDAK TAHU**.

### CF1(c) empat store +0x20 di FUN_800E3E74
**SEBAGIAN K3.** Semua empat PC tercatat sebagai `sh` ke displacement `+0x20`. Nilai yang ditulis bukan operasi `old+1`; ini mask atau OR dengan data dari global/field sumber. Alias base-register masih diberi label `DISPLACEMENT_CANDIDATE_BASE_ALIAS_NOT_PROVEN`.

| PC store | Instruksi pembentuk nilai | Nilai yang disimpan | Efek bit yang pasti dari instruksi |
|---|---|---|---|
| 0x800E418C | `lhu v1,0x20(v0)`; `andi v1,v1,0xF0FF` | `old & 0xF0FF` | Bersihkan bits 8–11; bits 12–15 dipertahankan oleh mask. |
| 0x800E41E0 | `lhu a0,-0x1450(a2)`; `sll a0,a0,8`; `lhu v0,0x20(v1)`; `or v0,v0,a0` | `old OR (source_0x1450 << 8)` | Bukan increment; OR dapat meng-set bits 8–15 jika source memuat bit itu, tetapi tidak menghapus bit lama. |
| 0x800E42C0 | `lhu v1,0x20(v0)`; `andi v1,v1,0xFF0F` | `old & 0xFF0F` | Bersihkan bits 4–7; bits 12–15 dipertahankan oleh mask. |
| 0x800E4314 | `lhu a0,-0x14F4(s0)`; `sll a0,a0,4`; `lhu v0,0x20(v1)`; `or v0,v0,a0` | `old OR (source_0x14F4 << 4)` | Bukan increment; OR dapat meng-set bits 4–15 jika source memuat bit tersebut. |

Dua store mask hanya menghapus nibble sasaran. Dua store OR menambahkan pola dari sumber `-0x1450` dan `-0x14F4`, bukan `old+1`. Apakah sumber itu adalah target `d`, target owner, atau nilai transisi lain: **TIDAK TAHU** sampai producer source dibuktikan.

Pembaca field dalam fungsi:
- `+0x1A`: satu kandidat halfword `0x800E3FBC: lhu v0,0x1A(v0)`.
- `+0x0E`: tidak ada `lhu` tercatat dalam fungsi ini.
- `+0x1C`: `0x800E3E7C sw s3,0x1C(sp)` dan `0x800E4578 lw s3,0x1C(sp)`; ini stack save/restore, bukan bukti field tile.
- `+0x1E`: tidak ada akses tercatat di inventaris fungsi ini.
- Caller langsung `FUN_800E3E74`: **TIDAK TAHU**. Artefak menandai `indirect_JALR=TIDAK_TAHU`; `0x800E40D4` dan `0x800E4210` adalah callsite dari E3E74 ke `FUN_800B770C` (callee), bukan caller E3E74.

### CF1(d) census pembaca u16 +0x0E dan +0x1A
**SEBAGIAN K3.** Filter instruksi `lhu` di `aq1-economy-census.tsv` memberi 29 kandidat (18 pada +0x0E, 11 pada +0x1A). Ini adalah daftar PC yang dapat diperiksa, tetapi belum merupakan bukti alias: tiap baris census menyebut `displacement candidate; base-register alias is not proven`. Cakupan adalah `recordFns` dan helper/caller relevan, bukan pemindaian kontrol-indirek seluruh Entry 1; label loader/non-loader per fungsi tidak tersedia. Jadi ini census kerja, bukan klaim exhaustive seluruh ROM.

| Offset | PC | Fungsi |
|---|---|---|
| +0x0E | 0x800C9990 | FUN_800c88f0 |
| +0x1A | 0x800CA748 | FUN_800c88f0 |
| +0x0E | 0x800CB3BC | FUN_800cadb8 |
| +0x0E | 0x800CBC7C | FUN_800cb4b4 |
| +0x0E | 0x800CBD9C | FUN_800cb4b4 |
| +0x0E | 0x800CCBCC | FUN_800cca18 |
| +0x0E | 0x800CCC0C | FUN_800cca18 |
| +0x1A | 0x800D0AE4 | FUN_800d05b8 |
| +0x1A | 0x800D2520 | FUN_800d15a8 |
| +0x0E | 0x800D2768 | FUN_800d15a8 |
| +0x1A | 0x800D2ADC | FUN_800d15a8 |
| +0x1A | 0x800D2B5C | FUN_800d15a8 |
| +0x0E | 0x800D3BBC | FUN_800d15a8 |
| +0x1A | 0x800D3EE4 | FUN_800d15a8 |
| +0x1A | 0x800D3F74 | FUN_800d15a8 |
| +0x1A | 0x800D4628 | FUN_800d15a8 |
| +0x1A | 0x800D46EC | FUN_800d15a8 |
| +0x1A | 0x800E3FBC | FUN_800e3e74 |
| +0x1A | 0x800EB570 | FUN_800eb434 |
| +0x0E | 0x800F0CD0 | FUN_800f0c10 |
| +0x0E | 0x800F0D34 | FUN_800f0c10 |
| +0x0E | 0x800F0EDC | FUN_800f0c10 |
| +0x0E | 0x800F0EFC | FUN_800f0c10 |
| +0x0E | 0x800FBE30 | FUN_800fb80c |
| +0x0E | 0x800FC68C | FUN_800fc340 |
| +0x0E | 0x800FC930 | FUN_800fc700 |
| +0x0E | 0x800FD654 | FUN_800fca0c |
| +0x0E | 0x800FE234 | FUN_800fe314 |
| +0x0E | 0x800FE5C4 | FUN_800fe314 |

---

## CF2 — hipotesis bersaing dan falsifier

### (i) Biaya lompat d>=2
Semua berikut tetap **HIPOTESIS** sampai ada pembacaan saldo/pending yang membandingkan kondisi sama; laporan pengguna saja = K1.

| Hipotesis | Prediksi bila biaya satu langkah = B | Falsifier |
|---|---|---|
| HJ1 eksponensial | biaya d = B×2^d (d=2 -> 4B; d=3 -> 8B) | Trace target d=2/3 pada kondisi sama; bila pending/debit bukan 4B/8B, HJ1 gugur. |
| HJ2 linear | biaya d = B×d (d=2 -> 2B; d=3 -> 3B) | Jika hasil terukur d=2 bukan 2B atau d=3 bukan 3B, HJ2 gugur. |
| HJ3 tetap/lookup | biaya tidak bergantung langsung pada d atau diambil dari tabel/tier tujuan | Bila trace operand fee menunjukkan formula deterministik B×2^d atau B×d pada beberapa d, HJ3 gugur. |

Blok debit action 3/8 yang sudah diperiksa di D15A8 memakai `u16(tile+0x1A)` secara langsung dan tidak memperlihatkan shift biaya berdasar d. Ini hanya menggugurkan pengali d **untuk blok transaksi tersebut**, bukan seluruh jalur lompat yang mungkin berbeda.

### (ii) Biaya bangun dari petak netral
| Hipotesis | Prediksi | Falsifier |
|---|---|---|
| HB1 biaya berasal dari `u16(tile+0x0E)` | jalur event 3 membaca +0x0E, membandingkan saldo, lalu pending debit sesuai nilai itu | Temukan pending writer jalur event 3 yang operand-nya +0x1A/konstanta dan tidak memakai +0x0E; HB1 gugur. |
| HB2 biaya berasal dari `u16(tile+0x1A)` | jalur event 3 membaca +0x1A dan mengurangi saldo kerja | Temukan debit event 3 yang secara langsung memakai +0x0E atau field lain, tanpa +0x1A; HB2 gugur. |
| HB3 biaya berasal dari konstanta/tabel/rumus lain | event 3 memuat nilai harga dari sumber lain | Buktikan bahwa pending debit event 3 sama dengan nilai +0x0E atau +0x1A untuk banyak record tanpa transformasi lain; HB3 gugur. |

Belum ada jalur netral event 3 yang menutup pilihan ini. Perbedaan nilai record (+0x0E dan +0x1A) sendiri tidak membuktikan mana yang menjadi biaya.

### Nilai event 3: owner bits dan offset debit
Pada blok transaksi bersama D15A8 yang sudah statis:
- debit memakai `u16(tile+0x1A)`, dinegasikan ke pending; `+0x0E` bukan operand debit di blok itu.
- dua mask `0xF0FF` dan `0xFF0F` membersihkan nibble level/atribut bits 8–11 dan 4–7 sebelum tulis ulang; bits 12–15 dipertahankan mask.
- blok ini dengan sendirinya tidak menunjukkan pergantian owner bits 12–15.
- tetapi branch yang dibuktikan pada CF1(a) hanya action==8 vs non-8; ia belum mengunci semua eksekusi action 3 ke blok yang sama atau membuktikan event 3 = build dari netral.

Kesimpulan event 3 secara gameplay: **TIDAK TAHU**. Klaim yang aman hanya bahwa transaksi bersama yang diaudit memakai +0x1A dan mutasi nibble-nya mempertahankan owner bits yang tidak dimask; tidak sah menyimpulkan label build netral.

---

## CF3 — data run H6 yang tersedia dan syarat yang belum terpenuhi
**BELUM untuk eksperimen yang diminta; SEBAGIAN K2 untuk satu launch diagnostik yang sudah ada. K5 BELUM.**

H6 hybrid SHA-256:
`d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475`
Target source SHA:
`00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`
Control source SHA:
`9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`

| Pemeriksaan | Data yang ada |
|---|---|
| Peluncuran | 1 launch (diminta >=2); 1 kondisi pertama nonpass. |
| Frame 180 RAM | 2,097,152 byte, SHA-256 `5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7`; cocok referensi. |
| Frame 360 RAM | 2,097,152 byte, SHA-256 `4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907`; cocok referensi. |
| Frame 1/60/600/1200 | Tidak tercatat dalam artefak run ini. |
| Write watchpoint `+0xEA8` | Tidak ada rekaman frame/PC/old/new; BELUM. |
| Memory Card | disposable zero-filled 128 KiB; sebelum dan sesudah SHA sama: `fa43239bcee7b97ca62f007cc68487560a39e19f74f3dde7486db3f98df8e471`. |
| Timeout | 1201 s; historical slowest 145.815 s; 1201 s >= 2×145.815 s; summary `TIMEOUT_GE_2X_OBSERVED_MAX=True`. Launch yang diamati 145.779 s. |
| Exit | script 2; wrapper 73; workflow/job GitHub tetap success. |
| State 2 | gate preflight block pada EA8 = FFFFFFFE; tidak mencapai setter/credit. |

**Bukan read-only murni:** log merekam fixture poke pada RAM disposable, antara lain team bytes p0–p3 `0x801EFBC6/FC56/FCE6/FD76` (255/255/0/0 menjadi 160/161/162/163), selected tile `0x8013EB20` (0→4), manager state `0x801EFF28` (0→1), action `0x801EFEA1..A3` (0→9/1/1), dan positive-credit phase 0→1. Chakra p0 tetap 1500. Ini membuat run hanya diagnostik dengan fixture poke, bukan memenuhi syarat strictly read-only.

Tidak ada record bypass gate dan tidak ada bukti pemanggilan `FUN_800BE5D8` sesudah bypass; preflight menghentikan sebelum state 2. K5 tetap BELUM karena hanya satu launch.

Pesan mentah yang menyebabkan stop:
```text
STATE2_GATE_PREFLIGHT_BLOCK field4=0x801CEC88 fieldEA8=0xFFFFFFFE predicted=4294967294
```

---

## Ledger semua commit baru sejak cd90b281f45cada726e80c3f87661e5ae5494303
Sumber: objek commit Git (masing-masing `files[]`), bukan hasil hitung tree. Urutan newest → oldest. 98 commit: 82 bot dan 16 manusia. Total perubahan commit-file 155; 144 path unik. 97 commit mengubah satu file; satu commit bot mengubah 58 file. Ledger ini berhenti pada HEAD yang diminta dan tidak memasukkan commit audit ini sendiri.

| # | SHA penuh | Jenis author | Jumlah file | File yang diubah |
|---:|---|---|---:|---|
| 1 | 012367cf0518e519520fe590845d62792289276a | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/CE3_WORKFLOW_SCRIPT_PROCESS_EXIT.txt |
| 2 | 4581f12904e0630c46569d5229aeda806facd8b2 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/CE3_STEP0_BUILD_VALIDATION.txt |
| 3 | 855fa98b16a684a63b96ceae899e7524786d52f2 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/CE3_STEP0_BUILD_EXIT_CODE.txt |
| 4 | d9144af54c171022006fa0d9741da6a2abe7cbd9 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/CE3_SCRIPT_EXIT_CODE.txt |
| 5 | 31d95c3c0b3db192c99feb1d488c9cd2c44bec2c | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/CE3_PCSX_RELEASE_MANIFEST.txt |
| 6 | 7377c7c16a9f57594211df9102d3b9d35f9f2e0d | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_SUMMARY.txt |
| 7 | 7166be498b2b7b1a4476d8245780f5ff1d8e144a | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_SCRIPT_EXIT_CODE.txt |
| 8 | 91910d418f3612deeefbf0cd19ba9c98ac7a3415 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_EMULATOR_LOG.txt |
| 9 | acf3e59859b8cab1b11280156cd1bf19947a601a | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/CE3_H6_PATCHED_ACTIONS_RUN_SUMMARY.txt |
| 10 | 340ec917a6f97522b3cab258033ee8553ad90f6e | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/CE3_H6_CREDIT_SUMMARY.txt |
| 11 | 1a888a09dec6f2b69ac2e51844004f180e4e4ea0 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/CE3_H6_CREDIT_RESULTS.tsv |
| 12 | 786f708df6d8ce77fbe34877060ad1781716864b | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/CE3_H6_CREDIT_LAUNCHES.tsv |
| 13 | 30980f6fe2829ecc404adb5d4078181124901c8b | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/CE3_FIRST_NONPASS_TILE4_LEVEL0_ATTEMPT1.txt |
| 14 | 9904f41167654f54f99cf7c31ed6d0ba98fc12e5 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41749255678/attempt-1/ACTIONS_RUN_SUMMARY.txt |
| 15 | b2ccb20041c31496b23ce531eec3434753db7868 | MANUSIA | 1 | .github/workflows/ce3-h6-positive-credit-probe.yml |
| 16 | 75d5e5c6f37f9ee4aa7807b3191eef723112424e | MANUSIA | 1 | experiments/ce3_h6_positive_credit_probe.py |
| 17 | 604c25c3c74fd31709dcd6db9e6d6f603922b239 | MANUSIA | 1 | reports/stage1_economy/CE3_H6_POSITIVE_CREDIT_RUNTIME_AUDIT_2026-11-04.md |
| 18 | 9928ee9ed3db578e7ea81b6d23a471082c2a0a51 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/CE3_WORKFLOW_SCRIPT_PROCESS_EXIT.txt |
| 19 | ce7b2d29f9dc93e04db88816ce334bd900df9d33 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/CE3_STEP0_BUILD_VALIDATION.txt |
| 20 | 072da5c4c0bf295e91d0321012c57971adf38eb5 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/CE3_STEP0_BUILD_EXIT_CODE.txt |
| 21 | 06b4997e0b3a9aa46c45bebefb78a38646901df7 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/CE3_SCRIPT_EXIT_CODE.txt |
| 22 | b703996b358d7d43196991eec6a8ccbd71d857f0 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/CE3_PCSX_RELEASE_MANIFEST.txt |
| 23 | f5e943ed8f684c2e1ab656e421209149c51ea9b5 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_SUMMARY.txt |
| 24 | 088297e7d77ac389e85a6c25c7c1b68967cd3a2d | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_SCRIPT_EXIT_CODE.txt |
| 25 | 940662b9e6a55364d613f7c273128c2e2d53d563 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_EMULATOR_LOG.txt |
| 26 | e5f87997438a328eeb5fdeebebe24644c5f728b5 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/CE3_H6_PATCHED_ACTIONS_RUN_SUMMARY.txt |
| 27 | 0551d246ee144003b8c47c6f796ae75aeb5964c3 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/CE3_H6_CREDIT_SUMMARY.txt |
| 28 | 2bf5fcebf0774b7385f4728b5ffa55202d76cf61 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/CE3_H6_CREDIT_RESULTS.tsv |
| 29 | 2ff3f047f9ae433a750bcac116170e92664819ee | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/CE3_H6_CREDIT_LAUNCHES.tsv |
| 30 | f2c52d4a158a81cbffd010f6c0f83424c87ce3df | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/CE3_FIRST_NONPASS_TILE4_LEVEL0_ATTEMPT1.txt |
| 31 | b273ba3a044ccabbb9de76179cac3a12cb271b9e | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740957322/attempt-1/ACTIONS_RUN_SUMMARY.txt |
| 32 | 252743b84ff436760a18e1ca2824e17fb3fb7895 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740884342/attempt-1/CE3_WORKFLOW_SCRIPT_PROCESS_EXIT.txt |
| 33 | 963656b2a5d2016ed315bea3f7bfb0d39311e1bb | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740884342/attempt-1/CE3_STEP0_BUILD_VALIDATION.txt |
| 34 | cfa15216f0b04c0cabee57204fc4276dc7aab5f9 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740884342/attempt-1/CE3_STEP0_BUILD_EXIT_CODE.txt |
| 35 | e151eec84cfd500ec59c455a38702f855358f0d8 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740884342/attempt-1/CE3_SCRIPT_EXIT_CODE.txt |
| 36 | 4ba08135cfd8c57b7883a101052e37ef593922a8 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740884342/attempt-1/CE3_PCSX_RELEASE_MANIFEST.txt |
| 37 | 4dd16b6425eb96fdcd8794f701d402f6ac97555b | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740884342/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_SUMMARY.txt |
| 38 | 95ffd17bf519d57d36b69ed7c5564d98f99153c5 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740884342/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_SCRIPT_EXIT_CODE.txt |
| 39 | a113743b3d3a102b75e848f57de2acaa323d105e | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740884342/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_EMULATOR_LOG.txt |
| 40 | f0a5869170047ab90dfdbf69fd7ea7b80265b739 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740884342/attempt-1/CE3_H6_PATCHED_ACTIONS_RUN_SUMMARY.txt |
| 41 | 28f41afc05fb2cc5f4d4a434c3662061f26d8a64 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740884342/attempt-1/CE3_H6_CREDIT_SUMMARY.txt |
| 42 | 6dc32664840950e57bf0c4a05e4c5d302b872fd2 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740884342/attempt-1/CE3_H6_CREDIT_RESULTS.tsv |
| 43 | 722fa4e146db61bf25dd95b81a72703171d1ab08 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740884342/attempt-1/CE3_H6_CREDIT_LAUNCHES.tsv |
| 44 | c3ffcb9ad8ed9b84d0e86809e74bc68121cda036 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740884342/attempt-1/ACTIONS_RUN_SUMMARY.txt |
| 45 | 2aa7549ddb5bc86ef898147881f0bf0654390f80 | MANUSIA | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/ACTIONS_RUN_SUMMARY.txt |
| 46 | c9e89ab1f811940349bfd0e61d6b64d89ff6526d | MANUSIA | 1 | .github/workflows/ce3-h6-positive-credit-probe.yml |
| 47 | 9fc931e95b081133cfcb8e7398b0a106bde61814 | MANUSIA | 1 | experiments/ce3_h6_positive_credit_probe.py |
| 48 | 6e6ae5472f2bbed763bba8180d68a6d9bce205d6 | MANUSIA | 1 | experiments/ce3_h6_positive_credit_probe.py |
| 49 | 045add220dfcc997fffc10207a68e8bd6673f0f4 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/CE3_WORKFLOW_SCRIPT_PROCESS_EXIT.txt |
| 50 | 53b47e9f974e065def83811c428e2f460ceafe20 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/CE3_STEP0_BUILD_VALIDATION.txt |
| 51 | ef651162d955432c9d750a9843e1d4325011fd47 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/CE3_STEP0_BUILD_EXIT_CODE.txt |
| 52 | db4dace9d83446871866589b7015774c36da2ac8 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/CE3_SCRIPT_EXIT_CODE.txt |
| 53 | 8730f966ffcafad15fdb63c18b881270b2fdb813 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/CE3_PCSX_RELEASE_MANIFEST.txt |
| 54 | 9d424db2a5f42ce0136841ddb9c7a0239ad88dfa | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_SUMMARY.txt |
| 55 | f622d8b50af4379072385fd2d1a59e5dfc57ee90 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_SCRIPT_EXIT_CODE.txt |
| 56 | e3f7946a0c4103844ee0b34c47203209f37aafca | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_EMULATOR_LOG.txt |
| 57 | 39df9589d690525ce612d7fab3cd60ab53312b73 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/CE3_H6_PATCHED_ACTIONS_RUN_SUMMARY.txt |
| 58 | 0929ccdf89622b15beb26bd43495ac48d1a19bee | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/CE3_H6_CREDIT_SUMMARY.txt |
| 59 | 1b6845fedc55a3702e8f8869a55292fd79bce38c | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/CE3_H6_CREDIT_RESULTS.tsv |
| 60 | fc39a6a01e7b94d1355e82e8bf492cd4e3c5a2f3 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/CE3_H6_CREDIT_LAUNCHES.tsv |
| 61 | bb548b21375bc92c9f1205dbafb9ffcb9f723f0b | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/CE3_FIRST_NONPASS_TILE4_LEVEL0_ATTEMPT1.txt |
| 62 | f55088cc281bd6aae5e1acc988c1a9067d322cb2 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740281514/attempt-1/ACTIONS_RUN_SUMMARY.txt |
| 63 | 3abfba705d478a1a0bc44e92003d7a7ef149191c | MANUSIA | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/ACTIONS_RUN_SUMMARY.txt |
| 64 | 416534fc2ad0e928a87319104c3975a708acf60c | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740084140/attempt-1/CE3_WORKFLOW_SCRIPT_PROCESS_EXIT.txt |
| 65 | 088f0c8aebd5a7c28f261b216dc6df0be5b1c70f | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740084140/attempt-1/CE3_STEP0_BUILD_VALIDATION.txt |
| 66 | ca75ab004360fbbb87176c23b14e4bfcf81b89e6 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740084140/attempt-1/CE3_STEP0_BUILD_EXIT_CODE.txt |
| 67 | bf991d537fe5eabaaadf1f8edf05304788ccd4e1 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740084140/attempt-1/CE3_SCRIPT_EXIT_CODE.txt |
| 68 | a5ae814fab45fe1c973bc0fb19bfaed4efbc11c6 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740084140/attempt-1/CE3_PCSX_RELEASE_MANIFEST.txt |
| 69 | 9f7365a6c8e73e61c2cddb33373e9e61c83c25cd | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740084140/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_SUMMARY.txt |
| 70 | c8afa2f98dd13f8ae0346bd1e3e1f1f8809020ab | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740084140/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_SCRIPT_EXIT_CODE.txt |
| 71 | d27fbf6780b220e7137e4f99e31837903f2ce196 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740084140/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_EMULATOR_LOG.txt |
| 72 | 7203b0c38184de1a5296a7b1edeed8c33362d55c | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740084140/attempt-1/CE3_H6_PATCHED_ACTIONS_RUN_SUMMARY.txt |
| 73 | e1bf12113e0cf2f3771330e64427e2671368412a | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740084140/attempt-1/CE3_H6_CREDIT_SUMMARY.txt |
| 74 | 2497eedd2d7f4511c9ae9966f3df3f7732899f93 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740084140/attempt-1/CE3_H6_CREDIT_RESULTS.tsv |
| 75 | f5a906284e8a71014db0db8c5d7129b7a951335b | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740084140/attempt-1/CE3_H6_CREDIT_LAUNCHES.tsv |
| 76 | 89b3e9f461c5f16d41ef8008b0d3f45b7b44b0c2 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740084140/attempt-1/ACTIONS_RUN_SUMMARY.txt |
| 77 | b9b449dddd71455a633ad761c0bbb15a4829a0bb | MANUSIA | 1 | .github/workflows/ce3-h6-positive-credit-probe.yml |
| 78 | 84a073a518611da97fef1166e344fcef2427939e | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/CE3_WORKFLOW_SCRIPT_PROCESS_EXIT.txt |
| 79 | d8491123859ba4f4ba57dd2d554a27b2f7fe773a | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/CE3_STEP0_BUILD_VALIDATION.txt |
| 80 | a0cda6123bd32e3f0f6b299c72fc1c4de54d192f | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/CE3_STEP0_BUILD_EXIT_CODE.txt |
| 81 | 29438355d3cfc0a6fee5b80b9544cf516892575f | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/CE3_SCRIPT_EXIT_CODE.txt |
| 82 | 6cfb94ab332a7b6afeb592d33bcf83ec236f6208 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/CE3_PCSX_RELEASE_MANIFEST.txt |
| 83 | b51fa9d4296aee357c63d71a04842959420c92c1 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_SUMMARY.txt |
| 84 | 0f232128ba564f88b5f1e2ce39b982c020be1dde | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_SCRIPT_EXIT_CODE.txt |
| 85 | 90f0ecdc29125bd3e333a41c80c56de1e21e32de | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/CE3_H6_PATCHED_BB3_SMOKE_EMULATOR_LOG.txt |
| 86 | d566aae9463056b18bc6cc814bbd8343d36babd7 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/CE3_H6_PATCHED_ACTIONS_RUN_SUMMARY.txt |
| 87 | c7fdbc17a660db7919f05af32b5b1fa4af316b04 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/CE3_H6_CREDIT_SUMMARY.txt |
| 88 | e370f170206561221203c52429c1f0ba4f5bbc0f | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/CE3_H6_CREDIT_RESULTS.tsv |
| 89 | a92c9ad6e55742d851db06747cafb30175c61a29 | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/CE3_H6_CREDIT_LAUNCHES.tsv |
| 90 | 8e09cf0010ca90381b323daa8b9592436632793c | BOT | 1 | reports/stage1_economy/ce3-h6-positive-credit-probe-run-41740037209/attempt-1/ACTIONS_RUN_SUMMARY.txt |
| 91 | 7c054c3edc741b1ac8fb4173671fbc6f024edc96 | MANUSIA | 1 | .github/workflows/ce3-h6-positive-credit-probe.yml |
| 92 | f5339ca1af67ea2150c355850c1f7c7386794ef3 | MANUSIA | 1 | .github/workflows/ce3-h6-positive-credit-probe.yml |
| 93 | 4b6c4f2c0801f22c05bd69017a11d408120de48f | MANUSIA | 1 | experiments/ce3_h6_positive_credit_probe.py |
| 94 | cae2cd6305977f50ed4baa289f52bfed3b95e720 | MANUSIA | 1 | experiments/ce3_h6_positive_credit_probe.py |
| 95 | 1175dff10a68a3f44f9d1c822e39951014ac27e7 | MANUSIA | 1 | experiments/ce3_h6_positive_credit_probe.py |
| 96 | d1195d4d14a5e0a8525b91897d837528c0974a5d | BOT | 58 | reports/stage1_economy/aq1-run-41738996928/attempt-1/ (58 files; list below) |
| 97 | 4104626043d012a6c91d09bec8cf7c4e68256b9d | MANUSIA | 1 | .github/workflows/step7-entry1-buffer-base-audit.yml |
| 98 | b51889a0c954b1fec0c33126212320f78f254e9f | MANUSIA | 1 | reports/stage1_economy/CE0_CE1_CE2_STATIC_AUDIT_2026-11-04.md |

### 58 berkas pada commit bot d1195d4d14a5e0a8525b91897d837528c0974a5d
Prefix untuk semua berikut: `reports/stage1_economy/aq1-run-41738996928/attempt-1/`

- `ACTIONS_RUN_SUMMARY.txt`
- `BA1_DATA_BIN_RESOURCE_INVENTORY.tsv`
- `BA1_DATA_SCAN_SUMMARY.txt`
- `BA1_RESOURCE_CANDIDATES.tsv`
- `BA1_TILE_TABLE_CANDIDATES.tsv`
- `BA1_TILE_TABLE_RECORDS.tsv`
- `BA1_TILE_TABLE_SCAN_SUMMARY.txt`
- `BB2_FULL_DATABIN_TEXT_SCAN.txt`
- `aq1-deep-context.tsv`
- `aq1-economy-census.tsv`
- `aq1-recount.txt`
- `aw1-helper-call-windows.tsv`
- `aw1-manager-b38-accesses.tsv`
- `aw1-manager-b40-accesses.tsv`
- `aw1-manager-b44-accesses.tsv`
- `aw1-manager-function-detail.txt`
- `aw1-manager-status.txt`
- `aw1-tile-field-function-inventory.tsv`
- `aw2-numeric-instruction-literals.tsv`
- `aw2-numeric-occurrences.tsv`
- `aw2-static-data-scan.md`
- `ay1-ay2-entry1.tsv`
- `ay1-ay2-exe.tsv`
- `ay1-ay2-sha256.txt`
- `ay2-exe-random-byte-check.txt`
- `az3-main-exe-economic-helper-detail.txt`
- `az3-resource-economy-function-detail.txt`
- `az3-setter-call-windows-entry1.tsv`
- `az3-setter-call-windows-main-exe.tsv`
- `az3-setter-caller-main-exe-detail.txt`
- `az3-setter-direct-callers-entry1.txt`
- `az3-setter-direct-callers-main-exe.txt`
- `az3-starting-balance-global-detail.txt`
- `ba1-mode-state-resource-selector.tsv`
- `ba1-resource-parser-main-exe.txt`
- `ba1-selector-callers-main-exe.txt`
- `ba1-selector-dat80070cd0-xrefs.csv`
- `ba1-selector-main-exe-functions.csv`
- `ba1-tile-loader-callers.txt`
- `ba1-tile-resource-loader.txt`
- `bb2-action-byte-access.tsv`
- `bb2-d15a8-direct-callers.txt`
- `bb2-d15a8-focused.txt`
- `bb2-d15a8-function-detail.txt`
- `bb2-entry1-numeric-literals.tsv`
- `bb2-event-direct-callers.txt`
- `bb2-event-function-detail.txt`
- `bb2-event-instruction-windows.txt`
- `bb2-full-databin-text-scan.tsv`
- `bb2-message-object-functions.csv`
- `bb2-message-object-xrefs.csv`
- `bb2-tile-nibble-access.tsv`
- `cd1-raw-indirect-call-candidates.txt`
- `entry1-buffer-base-targets.txt`
- `entry1-helper-function-detail.txt`
- `helper-a1-provenance-status.txt`
- `input-identity.txt`
- `run-summary.txt`

---

## Perubahan yang dilakukan oleh commit laporan ini
- `reports/stage1_economy/CF0_CF1_CF2_CF3_AUDIT_2026-11-04.md` — laporan ini.
- `reports/stage1_economy/CE3_H6_POSITIVE_CREDIT_RUNTIME_AUDIT_2026-11-04.md` — ditambahkan corrigendum CF0 yang menggantikan status/run/error “terbaru” lama dengan run 41749255678.
Tidak ada perubahan ke Release `naruto-checkpoint-39262213468`, `STATUS.md`, visibilitas repo, atau data biner terlarang.
