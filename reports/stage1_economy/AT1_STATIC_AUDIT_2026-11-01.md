# AT1 — audit statis lanjutan

Tanggal: 1 November 2026 (Asia/Jakarta). Repo tetap `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. Batas: statis, maksimum K4. Tidak ada emulator/gameplay dijalankan untuk AT1.

## Status

AT1(a) **TUNTAS — K4**: 14/14 call-site langsung ke setter `0x8001387C` direkonsiliasi dengan instruksi caller. Tabel lengkap, termasuk 12 instruksi sebelum tiap jal, delay slot, sumber basis, rantai stride, asal final a1, dan label census, ada di `AT1_SETTER_CALLS_RECONCILED_2026-11-01.tsv`.

AT1(b) **TUNTAS — K4**: kedua call memakai a0=s3. Getter pertama menjalankan move a1,a0, sehingga a1=s3 keluar dari getter pertama. Pada edge BLTZ-taken tidak ada instruksi yang menulis a1 sampai getter kedua; jadi a1=s3 saat masuk 0x80105418. Pada edge fall-through, lw a1,-0x5AAC(v0) di 0x801053D4 memuat pointer manager dari slot 0x8013A554 (nilai teramati 0x801CEF08), tetapi getter kedua segera menimpanya dengan move a1,a0.

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
- Pada BLTZ-taken, load manager di 0x801053D4 dilewati. Getter pertama di 0x801053C4 menjalankan move a1,a0; delay slot caller di 0x801053C8 menetapkan a0=s3. Tidak ada instruksi penulis a1 di antara getter pertama dan kedua, maka a1=s3 pada entry getter kedua.
- Pada BLTZ-fall-through, a1 dimuat dari manager slot 0x8013A554 melalui `lw a1,-0x5AAC(v0)` di 0x801053D4; trace terdahulu mengamati 0x801CEF08.
- Getter kedua mengembalikan `v0`, kemudian caller memindahkannya ke `a2` pada 0x80105440 sebelum `jal 0x8001B364`.

Disassembly penuh getter membuktikan a0 masuk adalah indeks; instruksi pertama move a1,a0 menyalin indeks ke a1. Karena getter pertama menerima a0=s3, a1=s3 diwariskan pada edge BLTZ-taken. Fall-through berbeda hanya karena 0x801053D4 memuat pointer manager 0x801CEF08 ke a1.

### Nasib v0 pada BLTZ dan argumen getter

Pada call pertama `0x801053C4`, `v0` return diuji oleh `bltz v0,0x80105414` di `0x801053CC`. **Delay slot MIPS tetap berjalan pada kedua hasil branch**: `0x801053D0: lui v0,0x8014` menimpa nilai return segera setelah branch menguji tandanya.

- **BLTZ-taken**: PC berpindah ke 0x80105414: li s0,0x20; v0 tetap hasil delay slot 0x80140000. Getter pertama telah menyalin a0=s3 ke a1 dan tidak ada penulis a1 pada edge ini; karena itu a1=s3 saat getter kedua mulai.
- **BLTZ-fall-through**: eksekusi menjalankan `0x801053D4: lw a1,-0x5AAC(v0)`, sehingga `a1` menjadi pointer manager dari slot `0x8013A554`. Selanjutnya `v0` digunakan ulang untuk hitung indeks lalu memuat nilai `+0x478` dan `+0x474`; bukan return getter pertama lagi. Cabang-cabang pemeriksaan berikut menentukan apakah jalur mencapai getter kedua.
- Pada kedua jalur ke getter kedua 0x80105418, delay slot 0x8010541C: move a0,s3 memberi a0=s3 sebagai indeks. Getter kedua segera menjalankan move a1,a0, sehingga a1 masukan (s3 pada taken atau pointer manager 0x801CEF08 pada fall-through) tertimpa sebelum guard/offset.
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

Koreksi per-edge: getter pertama menyalin a0 ke a1; caller memberinya a0=s3. Edge BLTZ-taken membawa a1=s3 sampai getter kedua. Fall-through menjalankan lw a1,-0x5AAC(v0) di 0x801053D4 dari global slot 0x8013A554 (pointer teramati 0x801CEF08). Instruksi penuh dari call pertama sampai call kedua:

```asm
0x801053C4  jal   0x800138EC
0x801053C8  move  a0,s3                 ; delay slot: getter pertama menerima a0=s3
0x801053CC  bltz  v0,0x80105414
0x801053D0  lui   v0,0x8014             ; branch delay slot, berjalan pada kedua edge
0x801053D4  lw    a1,-0x5AAC(v0)        ; hanya fall-through: baca slot manager 0x8013A554
0x801053D8  sll   v0,s3,0x1
0x801053DC  addu  v0,v0,s3
0x801053E0  sll   v0,v0,0x2
0x801053E4  subu  v0,v0,s3
0x801053E8  sll   a0,v0,0x3
0x801053EC  addu  v0,a1,a0
0x801053F0  lw    v1,0x478(v0)
0x801053F4  li    v0,0x1
0x801053F8  bne   v1,v0,0x80105418
0x801053FC  clear s0
0x80105400  addu  v0,a1,a0
0x80105404  lh    v0,0x474(v0)
0x80105408  nop
0x8010540C  blez  v0,0x80105418
0x80105410  nop
0x80105414  li    s0,0x20              ; target BLTZ-taken
0x80105418  jal   0x800138EC
0x8010541C  move  a0,s3                 ; delay slot: getter kedua menerima a0=s3
```

Getter kedua mendapat a0=s3 pada delay slot 0x8010541C dan menjalankan move a1,a0 sebagai instruksi pertamanya; a1 masukan tidak menjadi indeks. Return getter kedua diteruskan sebagai a2 di 0x80105440.


## Koreksi AU1 — disassembly penuh accessor

Bukti `seed-helper-detail.txt` dari run 41274567492 berisi `RAW_FUNCTION_BODY` lengkap dan dekompilasi untuk kedua target. Getter: argumen indeks masuk adalah a0; a1 caller-supplied ditimpa oleh `move a1,a0`. Setter: a0 indeks dan a1 nilai. Lihat `AU1_ACCESSOR_DISASSEMBLY_2026-11-01.md` untuk seluruh alamat, byte, instruksi, operand register, dan rekonsiliasi runtime. Tingkat statis K4. Run Ghidra: job 124754117941, run 41274567492, source SHA `7def692176e0ac7e21bff0d4a9a5eca8baf70880`, exit code 0.
