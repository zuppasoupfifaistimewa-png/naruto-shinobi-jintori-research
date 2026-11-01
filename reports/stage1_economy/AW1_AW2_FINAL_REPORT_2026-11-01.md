# AW1–AW2 — laporan akhir audit statis ekonomi Stage 1
Tanggal: 2026-11-01  
Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`  
Branch: `main`  
Input Ghidra/scan berhasil: run Step 7 `41290779721`, sumber commit `18b926049fac5126118f545cf46ae2f01e5d84f0`, job `124801401163`, status `SUCCESS`, exit code desimal `0`.

## Skala bukti K0–K5

- **K0**: belum ada data yang bisa dipakai.
- **K1**: dugaan atau pembanding lemah.
- **K2**: indikasi terbatas; rantai operand/aksi belum lengkap.
- **K3**: beberapa bukti saling mendukung, tetapi masih ada celah penting.
- **K4**: rantai statis langsung yang dapat diperiksa pada instruksi/dekompilasi.
- **K5**: hasil runtime konsisten pada sedikitnya dua peluncuran terpisah untuk kondisi uji yang sama.

Statis maksimum K4. Hasil video atau `GAME_RULES.md` hanya pembanding K1. Tidak ada fitting rumus gameplay dari kurang dari tiga pasangan input/output yang terverifikasi.

## AW0 — provenance register getter kedua

**TUNTAS K4.** Getter pertama di PC `0x801053C4` menjalankan `move a1,a0`. Delay slot caller `0x801053C8: move a0,s3` memberi indeks `a0=s3`, sehingga getter pertama keluar dengan `a1=s3`. Pada edge BLTZ-taken, tidak ada penulis `a1` sebelum getter kedua di `0x80105418`; nilai yang masuk adalah `a1=s3`.

Pada edge fall-through, `0x801053D4: lw a1,-0x5AAC(v0)` membaca pointer dari global slot `0x8013A554`; trace terdahulu mencatat `0x801CEF08`. Delay slot getter kedua `0x8010541C: move a0,s3` memberi indeks, lalu body getter segera menimpa a1 dengan a0. Pointer manager tidak menjadi indeks getter. Urutan instruksi penuh dicatat pada audit AT1 dan rekonsiliasi TSV.

## AW1 — helper petak dan manager

### A. FUN_800B770C

**Body 118 instruksi, dekompilasi Ghidra berhasil. K4 untuk nilai keluaran helper.**

Definisikan:
- `G = u32(0x8013EA84)`
- `R = G + (index & 0xFF) * 0x124`
- `sel = u8(R + 0x0B)`
- `slot = (u16(R + 0x20) >> 7) & 0x1E`
- `H = u16(R + 0x10 + slot)`

Hasil helper:
```
sel 0: H
sel 1: floor(H * 12 / 10)
sel 2: floor(H * 15 / 10)
sel 3: floor(H * 18 / 10)
sel 4: H * 2
sel >=5: 0
```

Rantai pembentukan alamat record pada instruksi:
```asm
0x800B7714  lw   v1,-0x157C(v0)   ; G = [0x8013EA84]
0x800B7718  sll  v0,a0,0x3
0x800B771C  addu v0,v0,a0
0x800B7720  sll  v0,v0,0x3
0x800B7724  addu v0,v0,a0
0x800B7728  sll  v0,v0,0x2       ; index * 0x124
0x800B772C  addu v0,v0,v1       ; R
0x800B7730  lbu  v1,0x0B(v0)     ; selector
0x800B7738  sltiu v0,v1,0x5
0x800B7750  lw   v0,0x0(v1)      ; dispatch pointer
```

Ekstraksi H:
```asm
0x800B7780  lhu  v1,0x20(v0)
0x800B7788  srl  v1,v1,0x7
0x800B778C  andi v1,v1,0x1E
0x800B7790  addu v0,v0,v1
0x800B7794  lhu  v0,0x10(v0)
```

Dispatch table lima word berada di Entry 1 pada file offset `0x1A4` (VA statis kandidat `0x800AD5F4`), dan dibaca oleh `lw v0,0(v1)` di `0x800B7750`. Lima target kode:

| Selector | Word pointer | Target | Makna aritmetika yang dibuktikan |
|---:|---|---:|---|
| 0 | `60 77 0B 80` | `0x800B7760` | H (100%) |
| 1 | `A0 77 0B 80` | `0x800B77A0` | H×12/10 (120%) |
| 2 | `08 78 0B 80` | `0x800B7808` | H×15/10 (150%) |
| 3 | `50 78 0B 80` | `0x800B7850` | H×18/10 (180%) |
| 4 | `9C 78 0B 80` | `0x800B789C` | H×2 (200%) |

Pembagian integer untuk selector 1–3 menggunakan reciprocal `0x66666667` di sekitar `0x800B77E8–0x800B7804`. Jadi pengali bukan disimpan sebagai array data berisi 100/120/150/180/200; ia diterapkan melalui dispatch dan instruksi aritmetika.

**Batas semantik:** ini membuktikan hasil helper yang dihitung dari record petak. Ini belum membuktikan bahwa hasilnya selalu merupakan “pendapatan petak”. Fungsi mempunyai 44 pemanggil JAL langsung, dan jendela panggil memperlihatkan pemakaian berbeda (agregasi, perbandingan, ambang, pengurangan, dan pengolahan nilai). Label pendapatan/biaya tidak diberikan tanpa rantai caller yang mengaitkan hasil ke kredit resource atau pembanding harga.

### B. FUN_80109FEC dan manager field +0xB44

**Dekompilasi lengkap berhasil, K4 untuk operand dan alur state.** Fungsi mengakses manager pointer melalui global slot `0x8013A554`. Dua fungsi lain yang langsung menyentuh field manager `+0xB44` juga didekompilasi:

- `FUN_80109994` — reset `manager+0xB44 = 0`; bentuk `manager+0xB40 = manager+0xB30 + manager+0xB38`.
- `FUN_80109F1C` — load field `+0xB44` dan teruskan ke fungsi lain untuk ditampilkan/diproses; teks label yang menjelaskan artinya belum dibuktikan.
- `FUN_80109FEC` — state machine utama; 14 instruksi read/write `+0xB44` pada tiga fungsi tersebut adalah seluruh temuan direct-displacement dari eksport ini. Alias base register di tiap instruksi perlu dipastikan dengan konteks fungsi; fungsi-fungsi ini juga menunjukkan load global manager slot dalam badan yang sama.

Inventaris PC +0xB44:
```
FUN_80109994: 0x80109A54 sw zero,0xB44(v0)
FUN_80109F1C: 0x80109F64 lw a2,0xB44(v1)
FUN_80109FEC: 0x8010A0F4 sw v1,0xB44(v0)
               0x8010A154 lw a1,0xB44(v1)
               0x8010A1C4 sw zero,0xB44(v0)
               0x8010A524 lw v0,0xB44(v1)
               0x8010A590 lw v0,0xB44(v1)
               0x8010A59C sw v0,0xB44(v1)
               0x8010A5C8 sw v1,0xB44(v0)
               0x8010A5EC lw v0,0xB44(v0)
               0x8010A610 lw s1,0xB44(v0)
               0x8010A648 lw v0,0xB44(v1)
               0x8010A658 sw v0,0xB44(v1)
               0x8010A6A8 lw v0,0xB44(v1)
```

#### Empat pemanggilan setter

Setter `0x8001387C` menulis word ke record player pada `0x80070EA0 + index*0xB4 + 0x18`. Getter `0x800138EC` membaca word `+0x18`. Dengan notasi `M=[u32]0x8013A554`, `i=u8(M+0xB2B)`, dan `Q(i)=getter_0x800138EC(i)`:

1. **PC `0x8010A15C` — setter argumen a1 = `Q(i) + u32(M+0xB44)`.**
   ```asm
   0x8010A140  lbu  a0,0xB2B(a0)
   0x8010A144  jal  0x800138EC
   0x8010A148  nop
   0x8010A14C  lw   v1,-0x5AAC(s1)  ; M
   0x8010A154  lw   a1,0xB44(v1)
   0x8010A158  lbu  a0,0xB2B(v1)   ; i
   0x8010A15C  jal  0x8001387C
   0x8010A160  addu a1,v0,a1       ; a1 = Q(i)+M.B44
   ```

2. **PC `0x8010A1B0` — setter argumen a1 = `Q(i)`; a0 = return `0x800171A4(i)`.**
   ```asm
   0x8010A188  lbu  a0,0xB2B(v0)   ; i
   0x8010A18C  jal  0x800171A4
   0x8010A190  nop
   0x8010A194  move s0,v0
   0x8010A1A0  lbu  a0,0xB2B(v0)   ; i
   0x8010A1A4  jal  0x800138EC
   0x8010A1A8  nop
   0x8010A1AC  move a0,s0
   0x8010A1B0  jal  0x8001387C
   0x8010A1B4  move a1,v0          ; a1 = Q(i)
   ```

3. **PC `0x8010A638` — setter argumen a1 = `Q(i) + min(u32(M+0xB44),0x14)`.**
   ```asm
   0x8010A5EC  lw   v0,0xB44(v0)
   0x8010A5F4  slti v0,v0,0x15
   0x8010A5F8  bne  v0,zero,0x8010A608
   0x8010A5FC  lui  v0,0x8014       ; branch delay slot
   0x8010A600  j    0x8010A614
   0x8010A604  li   s1,0x14          ; jump delay slot: clamp 20
   0x8010A608  lw   v0,-0x5AAC(v0)
   0x8010A610  lw   s1,0xB44(v0)    ; B44 when <0x15
   0x8010A620  lbu  a0,0xB2B(v0)    ; i
   0x8010A624  jal  0x800138EC
   0x8010A628  nop
   0x8010A634  lbu  a0,0xB2B(v1)    ; i
   0x8010A638  jal  0x8001387C
   0x8010A63C  addu a1,v0,s1        ; a1 = Q(i)+min(B44,20)
   0x8010A648  lw   v0,0xB44(v1)
   0x8010A650  subu v0,v0,s1
   0x8010A654  jal  0x80011C6C
   0x8010A658  sw   v0,0xB44(v1)    ; consumes the credited amount
   ```

4. **PC `0x8010A97C` — setter argumen a1 = `Q(i)`; a0 = return `0x800171A4(i)`.**
   ```asm
   0x8010A954  lbu  a0,0xB2B(v0)    ; i
   0x8010A958  jal  0x800171A4
   0x8010A95C  nop
   0x8010A960  move s0,v0
   0x8010A96C  lbu  a0,0xB2B(v0)    ; i
   0x8010A970  jal  0x800138EC
   0x8010A974  nop
   0x8010A978  move a0,s0
   0x8010A97C  jal  0x8001387C
   0x8010A980  move a1,v0           ; a1 = Q(i)
   ```

Immediate `0x14` pada state machine juga dipakai untuk menaikkan `manager+0xB34`, `+0xB3C`, dan `+0xB44` bertahap hingga nilai tujuan. Tidak ada instruksi yang menamai field `+0xB44` “uang”, “harga Barrier”, “pendapatan”, atau “refund”. Secara mekanis field itu menjadi accumulator/delta yang dipakai untuk mengubah word player record `+0x18`, lalu dikurangi; identitas aksi gameplay belum ditetapkan.

### C. Semua fungsi pengakses field record petak

`aw1-tile-field-function-inventory.tsv` memuat fungsi dan PC read/write dari census AQ1 untuk `+0x0B` serta halfword `+0x10..+0x2E`. Ringkasan jumlah baris fungsi per displacement:

| Field | Fungsi tercatat | Fungsi READ | Fungsi WRITE |
|---:|---:|---:|---:|
| +0x0B | 7 | 7 | 1 |
| +0x10 | 87 | 47 | 78 |
| +0x12 | 13 | 8 | 9 |
| +0x14 | 45 | 29 | 39 |
| +0x16 | 5 | 0 | 5 |
| +0x18 | 76 | 56 | 70 |
| +0x1A | 11 | 5 | 6 |
| +0x1C | 57 | 47 | 52 |
| +0x1E | 12 | 5 | 9 |
| +0x20 | 75 | 73 | 54 |
| +0x22 | 57 | 47 | 18 |
| +0x24 | 81 | 77 | 47 |
| +0x26 | 7 | 5 | 5 |
| +0x28 | 45 | 34 | 39 |
| +0x2A | 0 | 0 | 0 |
| +0x2C | 29 | 25 | 21 |
| +0x2E | 12 | 5 | 7 |

Read dan write dapat overlap pada fungsi yang sama. Census mencatat displacement operand dan PC; label `DISPLACEMENT_ONLY_BASE_REGISTER_NOT_PROVEN` dipertahankan karena displacement saja tidak cukup membuktikan alias base register sebagai record petak. TSV merupakan daftar lengkap untuk diperiksa, bukan pengganti review tiap fungsi.

Direct-call census: `FUN_800B770C` 44 JAL; `FUN_800BDC4C` 3 JAL. Indirect JALR belum tercakup (`TIDAK TAHU`). 47 jendela caller diekspor pada `aw1-helper-call-windows.tsv`.

## AW2 — pencarian data, konstanta dan teks

### Identitas input scan

| Input | Bytes | SHA-256 |
|---|---:|---|
| `SLPS_035.53` | 385024 | `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569` |
| `DATA.BIN` Entry 0 | 110536 | `56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4` |
| `DATA.BIN` Entry 1 | 596412 | `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a` |

Entry 1 berada pada file offset `0x10BB000`; base `0x800AD450` dipakai sebagai **static candidate** dari global-pointer analysis, bukan dianggap mapping runtime yang sudah dibuktikan. Base runtime Entry 0 adalah TIDAK TAHU.

### Angka mentah 50/60/100/150

Hitungan kemunculan byte LE berurutan u8/u16/u32; setiap hit bukan otomatis konstanta ekonomi:

| Input | Nilai | u8 | u16 | u32 |
|---|---:|---:|---:|---:|
| SLPS_035.53 | 50 | 454 | 100 | 6 |
| SLPS_035.53 | 60 | 4458 | 376 | 3 |
| SLPS_035.53 | 100 | 896 | 328 | 30 |
| SLPS_035.53 | 150 | 324 | 149 | 111 |
| Entry 0 | 50 | 120 | 46 | 0 |
| Entry 0 | 60 | 1000 | 119 | 3 |
| Entry 0 | 100 | 308 | 145 | 13 |
| Entry 0 | 150 | 85 | 72 | 65 |
| Entry 1 | 50 | 470 | 169 | 0 |
| Entry 1 | 60 | 10688 | 449 | 4 |
| Entry 1 | 100 | 1246 | 506 | 24 |
| Entry 1 | 150 | 724 | 484 | 442 |

Kumpulan lokasi pertama yang lengkap dan setiap hit tambahan berada pada `aw2-numeric-occurrences.tsv`. PC immediate numerik di kode ada pada `aw2-numeric-instruction-literals.tsv`; formatnya mencatat PC, fungsi, byte instruksi dan literal. Kemunculan angka di code atau data belum diberi pembaca/xref ekonomi kecuali dispatch helper yang dibuktikan langsung di atas.

Sequence contiguous LE `100,120,150,180,200` tidak ditemukan pada u8/u16/u32 di tiga input. Helper petak justru membuktikan multiplier melalui lima target dispatch dan instruksi aritmetika, bukan satu tabel persentase data.

### Kata kunci dan Shift-JIS

Pencarian literal ASCII/Shift-JIS terhadap:
- `Barrier`, `Chakra`, `cost`, `upgrade`, `release`;
- `結界`, `チャクラ`, `費用`, `強化`, `建設`, `解除`, `解放`, `バリア`;

menghasilkan 0 hit literal pada main EXE, Entry 0 dan Entry 1. Pencarian run Shift-JIS yang dapat didecode mengembalikan 25 run pada EXE, 3 pada Entry 0, dan 234 pada Entry 1 (262 keseluruhan). Run itu kandidat potongan teks/font/resource, belum terbukti sebagai message UI atau label ekonomi.

Peta font/tile index ke glyph tidak berhasil dibangun karena belum ada rantai kode yang menghubungkan index message/glyph ke tabel font. Status peta glyph: **TIDAK TAHU**. Ketiadaan literal keyword tidak membuktikan tidak ada teks; teks mungkin dirender dari indeks tile atau resource lain.

## Hipotesis bersaing dan falsifier

Tidak ada formula gameplay yang di-fit dari angka video atau dari kandidat byte.

### Pendapatan petak
- **H1:** helper petak menghitung nilai yang dikreditkan saat commit petak menggunakan selector `+0x0B`, halfword yang dipilih oleh `+0x20`, dan faktor 100–200%.  
  *Falsifier:* commit path tidak meneruskan return helper ke saldo/score, dan return hanya dipakai untuk UI/threshold lain.
- **H2:** helper menghitung nilai petak untuk perbandingan/penilaian; kredit ekonomi berasal dari pending-delta manager atau state lain.  
  *Falsifier:* ditemukan jalur commit yang secara langsung menambah saldo dengan return helper pada sedikitnya tiga tipe petak.
- **H3:** helper hanya salah satu komponen nilai/validasi (mis. kelas petak), sedangkan pendapatan dihitung pada caller dari beberapa field/lookup.  
  *Falsifier:* caller menunjukkan helper return langsung menjadi jumlah final tanpa operand ekonomi tambahan.

### Biaya bangun/upgrade Barrier
- **H1:** biaya adalah nilai lookup berdasarkan level/selector petak atau tabel data lain.  
  *Falsifier:* jalur validasi/subtract biaya terbukti tidak membaca tabel/selector tersebut.
- **H2:** manager accumulator `+0xB44` dan penambahan `+0x14` merupakan delta biaya/transaksi untuk aksi ini.  
  *Falsifier:* state manager `FUN_80109FEC` terbukti bukan aksi Barrier atau field +0xB44 digunakan untuk sistem lain.
- **H3:** biaya tetap per aksi; state Barrier mengubah atribut selain jumlah biaya.  
  *Falsifier:* instruksi compare/subtract biaya menunjukkan nilai berubah langsung menurut level/selector.

### Chakra dari Barrier release
- **H1:** state release mengirim kredit ke accessor player `+0x18` dari accumulator manager `+0xB44`, dibatasi maksimum 0x14 per update, lalu mengurangi accumulator.  
  *Falsifier:* state switch di `FUN_80109FEC` tidak terkait release Barrier.
- **H2:** setter Chakra di state machine hanya sinkronisasi nilai dan bukan refund; transfer resource terjadi di caller lain.  
  *Falsifier:* label UI/action dan caller membuktikan state 7 merupakan release dengan amount yang sama.
- **H3:** manager `+0xB44` adalah nilai dari aksi berbeda; release Barrier hanya menghapus state tanpa kredit.  
  *Falsifier:* instruksi release mengirim jumlah positif ke setter `0x8001387C`.

**Kesimpulan AW1–AW2:** rantai angka helper dan ekspresi setter telah K4. Label bisnis/gameplay “pendapatan petak”, “harga Barrier”, dan “refund release” belum ditautkan ke teks atau aksi UI secara langsung, sehingga harus tetap diberi status parsial/belum. Tidak ada nilai yang dipaksakan menjadi label.


## Addendum AW2 — scan stride dan status run lanjutan

Run Step 7 terbaru yang menyelesaikan scan Entry 1:
- RUN_ID: `41291576229`
- JOB_ID: `124803739839`
- SOURCE_SHA: `64de9960b60cd0eb629b0c15e9025ca787bf1e84`
- STATUS: `SUCCESS`
- EXIT_CODE desimal: `0`

Pencarian sequence `100,120,150,180,200` dilakukan sebagai LE u8/u16/u32 pada ketiga input, untuk sequence contiguous dan jarak elemen umum. Seluruh 54 kombinasi yang diuji menghasilkan **0 hit**:
- contiguous: u8/u16/u32;
- strided: u8 stride 2/4/8/12/16; u16 stride 1/4/8/12/16; u32 stride 1/2/8/12/16;
- input: `SLPS_035.53`, DATA.BIN Entry 0, DATA.BIN Entry 1.

Kesimpulannya hanya bahwa tidak ditemukan susunan lima nilai itu dalam tipe/stride yang diuji. Ini tidak meniadakan tabel dengan urutan, encoding, skala, stride, atau padding lain. Khusus helper `FUN_800B770C`, persentase 100/120/150/180/200 terbukti diimplementasikan melalui dispatch ke lima fungsi dan operasi aritmetika, bukan sequence data.

Pencarian string literal ASCII/Shift-JIS exact menghasilkan 0 hit untuk kata kunci English/Japanese yang dicatat pada bagian sebelumnya. Heuristik run Shift-JIS menghasilkan 25 run di EXE, 3 di Entry 0, 234 di Entry 1 (262 total). Run itu tidak terbukti sebagai message UI; sebagian hasil Entry 0 tampak seperti decoding byte acak. Peta indeks glyph/tile ke font tetap **TIDAK TAHU**.

Ekspor immediate literal Ghidra pada Entry 1 tersedia pada `aw2-numeric-instruction-literals.tsv`. Run Ghidra terpisah untuk EXE utama dan DATA.BIN Entry 0 (`41290779708`) masih berstatus berjalan pada saat laporan final ini dibuat; karena itu daftar xref semua literal numerik untuk dua input tersebut belum lengkap. Byte-scan raw numeric occurrences untuk ketiga input sudah selesai dan disimpan.
