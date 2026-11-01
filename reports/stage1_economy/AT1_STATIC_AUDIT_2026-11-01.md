# AT1 — audit statis lanjutan

Tanggal: 1 November 2026 (Asia/Jakarta). Repo tetap `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. Batas: statis, maksimum K4. Tidak ada emulator/gameplay dijalankan untuk AT1.

## Status

AT1(a) **TUNTAS — K4**: 14/14 call-site langsung ke setter `0x8001387C` direkonsiliasi dengan instruksi caller. Tabel lengkap, termasuk 12 instruksi sebelum tiap jal, delay slot, sumber basis, rantai stride, asal final a1, dan label census, ada di `AT1_SETTER_CALLS_RECONCILED_2026-11-01.tsv`.

AT1(b) **TUNTAS — K4**: dua call-site getter dan kedua edge BLTZ dianalisis. `a0=s3` terbukti pada kedua call; v0 hasil getter pertama diuji oleh BLTZ lalu ditimpa instruksi delay-slot `lui v0,0x8014` pada kedua edge. Nilai konkret a1 pada jalur BLTZ-taken adalah **TIDAK TAHU** (a1 caller-saved setelah helper `0x80105BCC`), dan ketidakpastian itu dicatat eksplisit, bukan diisi tebakan. Pada fall-through, a1 berasal dari manager slot `0x8013A554`. Detail lengkap ada di TSV per-edge.

AT1(c) **TUNTAS — K4**: himpunan FIELD enam run dibandingkan per PC/fungsi. Jumlah: 1.188, 1.188, 1.163, 1.178, 1.188, 1.188. Diff TSV berisi 35 PC yang beda; 25 hilang pada run 41213474394, 10 pada run 41249242776. Penyebab eksporternya **TIDAK TAHU** dari bukti ini saja. Run 41208394883 sudah 1.188 sebelum perubahan exporter cfff770; jadi cfff770 tidak dinyatakan sebagai penyebab kenaikan/selisih.

AT1(d) **TUNTAS — K4**: tabel hitungan operand berikut mempertahankan nama register yang benar-benar muncul di disassembly.

| Operand yang dihitung | Nomor GPR | READ | WRITE | OTHER | Total |
|---|---:|---:|---:|---:|---:|
| `s8` | $30 (alias ABI frame-pointer `fp`) | 0 | **2** | 0 | **2** |
| `fp` sebagai token operand | $30 | 0 | 0 | 0 | 0 |

Register numeriknya sama ($30), tetapi nama operand dalam dua baris census adalah `s8`: `sb v0,0x0(s8)` pada PC `0x800CAE4C` dan `0x800CB46C`. Jadi nilai yang harus dilaporkan adalah **s8 = 2 WRITE, bukan fp = 0**.

## AT1(a) — 14 setter call-site

Tabel lengkap ada di TSV yang menyertakan kutipan instruksi 12 langkah sebelum jal dan delay slot.

Ringkasan sumber:

| Kelompok | Setter PC | Slot yang benar | Stride |
|---|---|---|---|
| Participant | 0x800B41B0, 0x800B4254, 0x800B4F00, 0x800B4F64 | EA74 = 0x8013EA74 (load -0x158C) | 0x90 |
| Participant | 0x800B6238 | EA74 | 0x90 (s1 sudah dibentuk dari index*9<<4) |
| Participant | 0x800BEC98 | EA74 | 0x90 |
| Participant | 0x800DEB38 | EA74 | 0x90 |
| Participant | 0x800E1BE0 | EA74 | 0x90 |
| Participant | 0x800EC9A4 | EA74 | 0x90 |
| Participant | 0x800F95E8 | EA74 | 0x90 |
| Manager | 0x8010A15C, 0x8010A1B0, 0x8010A638, 0x8010A97C | manager slot 0x8013A554 (load -0x5AAC) | tidak ada stride array pada argumen ini |

Census memberi label `RECORD_0x8013EA84` pada tujuh site: 0x800B41B0, 0x800B4254, 0x800B4F00, 0x800B4F64, 0x800B6238, 0x800DEB38, 0x800EC9A4. **Ketujuh label tersebut bertentangan** dengan rantai a1 yang diaudit: pemuat basis adalah `lw ..., -0x158C` (EA74), bukan `-0x157C` (EA84), dan rantai indeks participant memakai stride 0x90. EA84 memang muncul pada fungsi yang sama untuk tile-record di bagian lain; itu tidak menjadikannya sumber final a1 setter.

Empat call-site manager perlu dibedakan:
- `0x8010A15C`: final `a1 = getter_return + manager[0xB44]`; label manager+0xB44 cocok sebagian.
- `0x8010A1B0` dan `0x8010A97C`: final `a1` adalah getter return langsung; tidak ada load manager+0xB44 pada rantai a1.
- `0x8010A638`: instruksi linear `lw s1,0xB44(v0)` di `0x8010A610` tidak dijalankan dari jalur yang menuju call. `0x8010A600 j 0x8010A614`; delay slot `0x8010A604 li s1,0x14` **dijalankan**, sehingga final `a1 = getter_return + 0x14`. Inilah koreksi untuk s1.

Di antara 14 caller, tidak ada yang terbukti memperoleh final a1 dari slot tile-record EA84 dan stride 0x124. Rantai EA84/0x124 yang ada pada fungsi `FUN_800B2A58` terpisah dari final a1 ke setter yang sedang direkonsiliasi.

## AT1(b) — getter 0x800138EC di FUN_801052E8

**Call PC 0x801053C4**
- 12 instruksi sebelumnya dan delay slot `0x801053C8 move a0,s3` dicatat di `AT1_GETTER_CALLS.tsv`.
- Getter menerima `a0=s3`; `a1` tepat sebelum call tidak dapat dipulihkan hanya dari caller: sebelumnya ada `jal 0x80105BCC`, dan a1 caller-saved.
- Return `v0` diuji oleh `bltz v0,0x80105414` di `0x801053CC`: jika negatif, branch-taken ke 0x80105414; jika non-negatif, fall-through ke instruksi pemuatan manager pointer.

**Call PC 0x80105418**
- Kedua jalur menuju call, jal taken dan fall-through, memakai delay slot `0x8010541C move a0,s3`: jadi `a0=s3`.
- Pada BLTZ-taken, instruksi `lw a1,-0x5AAC(v0)` di 0x801053D4 dilewati. a1 yang sampai ke getter kedua mewarisi nilai a1 dari first getter path; nilai konkret **TIDAK TAHU** karena asalnya melibatkan a1 caller-saved di sekitar helper 0x80105BCC.
- Pada BLTZ-fall-through, a1 dimuat dari manager slot 0x8013A554 melalui `lw a1,-0x5AAC(v0)` di 0x801053D4; trace terdahulu mengamati 0x801CEF08.
- Getter kedua mengembalikan `v0`, kemudian caller memindahkannya ke `a2` pada 0x80105440 sebelum `jal 0x8001B364`.

Disassembly getter di data statis lama menunjukkan a1 dipakai untuk pemeriksaan indeks `<4` dan untuk offset record `index*0xB4`; a0 dipakai sebagai basis record. Karena itu dua argumen yang dibaca accessor adalah a0 (basis/pointer record) dan a1 (indeks). Nilai a1 konkret pada jalur BLTZ-taken tetap TIDAK TAHU, bukan diasumsikan sebagai 0 atau manager pointer.

### Nasib v0 pada BLTZ dan argumen getter

Pada call pertama `0x801053C4`, `v0` return diuji oleh `bltz v0,0x80105414` di `0x801053CC`. **Delay slot MIPS tetap berjalan pada kedua hasil branch**: `0x801053D0: lui v0,0x8014` menimpa nilai return segera setelah branch menguji tandanya.

- **BLTZ-taken**: PC berpindah ke `0x80105414: li s0,0x20`; `v0` tetap hasil delay slot `0x80140000` saat call getter kedua mulai. `a1` tidak dimuat ulang; isinya diwarisi dari call getter pertama dan TIDAK TAHU.
- **BLTZ-fall-through**: eksekusi menjalankan `0x801053D4: lw a1,-0x5AAC(v0)`, sehingga `a1` menjadi pointer manager dari slot `0x8013A554`. Selanjutnya `v0` digunakan ulang untuk hitung indeks lalu memuat nilai `+0x478` dan `+0x474`; bukan return getter pertama lagi. Cabang-cabang pemeriksaan berikut menentukan apakah jalur mencapai getter kedua.
- Pada kedua jalur yang sampai ke getter kedua `0x80105418`, delay slot `0x8010541C: move a0,s3` memberi `a0=s3`. Getter menerima dua operand relevan: `a0` sebagai basis record dan `a1` sebagai indeks. Body accessor `0x800138EC` memvalidasi `a1<4`, membentuk offset `a1×0xB4`, lalu membaca word di `+0x18`. Maka pada jalur fall-through, caller mengirim pointer manager pada tempat a1 yang diperlakukan callee sebagai indeks; jangan mengubahnya menjadi dugaan indeks valid. Pada BLTZ-taken, nilai a1 tetap TIDAK TAHU.
- Return v0 dari getter kedua selanjutnya diteruskan sebagai `a2` ke `0x8001B364` lewat `move a2,v0` di `0x80105440`.

## AT1(c) — perbandingan FIELD

| Run | Job | Commit sumber | FIELD |
|---|---:|---|---:|
| 41208394883 | 124558086018 | a3cc4bfde7784858840e9cc98cc12e9bd70a2efe | 1.188 |
| 41211621969 | 124567642021 | 8894686395afdca97328a9fb2af5007a29406584 | 1.188 |
| 41213474394 | 124573087130 | 1c7ff2f85861020af859f152f68d4cd71f1b6f20 | 1.163 |
| 41249242776 | 124679086530 | 3016fa0a10f3d672d52c1d1101d1daa403a07f95 | 1.178 |
| 41249411706 | 124679584699 | d74cf2aaa162c399d31362b9421f567be294f27c | 1.188 |
| 41249611249 | 124680174749 | cfff7709f745f1f68ba01134e49c65b991528eb2 | 1.188 |

Run 41213474394 kurang 25 baris yang seluruhnya berada dalam `FUN_800DB29C` (entry 0x800DB29C). Run 41249242776 kurang 10 baris, seluruhnya berada dalam `FUN_800E0B3C` (entry 0x800E0B3C). Empat run lain memakai himpunan yang identik pada seluruh 1.188 PC/fungsi. Ini temuan diff; mengapa dua versi exporter melewatkan subset tersebut TIDAK TAHU. SHA blob TSV yang identik: 41208394883/41211621969/41249411706/41249611249 = `120a5d79d6280642f00697830d25f52ff2a78dc2`; run 41213474394 = `c4ee7fe35b58bbb7ed12ec18998556545efb451f`; run 41249242776 = `07b217ffe1f080dd9d288a1cbaead740467ad7fb`.

## AT1(d) — register
`s8` (= $30; alias frame pointer) = **2 WRITE**, `fp` = **0**. Jangan gabungkan alias tersebut atau mengganti label menjadi fp.

## Berkas bukti sumber
AQ1 census: `reports/stage1_economy/aq1-run-41249611249/attempt-1/aq1-economy-census.tsv` dan deep-context. Legacy getter disassembly: `reports/step4_10_static_evidence_audit/run_40783998364/a3_getter_setter.csv`. Semua kesimpulan statis maksimum K4. Nol hit bukan bukti fungsi tidak dipakai; rumus streamer tidak dipakai.


## Klarifikasi getter (call-site 0x801053C4/0x80105418)

Koreksi dan tabel lengkap per-edge tersedia dalam `AT1_GETTER_CALLS_RECONCILED_2026-11-01.tsv`. Pada `0x801053CC`, `bltz` menguji return v0 dari getter pertama. Delay slot `0x801053D0 lui v0,0x8014` tetap dieksekusi pada kedua edge dan menimpa return v0 menjadi basis `0x80140000`. Jika BLTZ-taken, load manager pointer `lw a1,-0x5AAC(v0)` di 0x801053D4 dilewati; a1 pada getter kedua diwarisi dari call pertama. Karena call pertama didahului `jal 0x80105BCC`, dan a1 caller-saved, nilai konkret pada jalur ini **TIDAK TAHU**. Pada fall-through, a1 dimuat dari manager slot 0x8013A554 dengan basis v0=0x80140000 (trace lama mengamati a1=0x801CEF08). Kedua getter menerima a0=s3 melalui delay slot. Return v0 dari getter kedua dipindah menjadi a2 pada 0x80105440. Callee accessor memeriksa a1<4, menggunakan a1*0xB4 untuk record stride, dan membaca word pada +0x18; tidak ada alasan menyamakan manager pointer dengan indeks.
