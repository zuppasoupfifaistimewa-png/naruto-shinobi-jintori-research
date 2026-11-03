# CB2 — audit statis biaya Barrier / kredit positif (2026-11-03)

## Batas cakupan

Sumber: artefak statis Entry 1 yang telah ada di repo, terutama `aq1-run-41541667221/attempt-1/az3-resource-economy-function-detail.txt`, `bb2-d15a8-function-detail.txt`, `bb2-d15a8-direct-callers.txt`, dan laporan BB1/BB2. Tidak ada emulator atau runtime yang dijalankan.

Reader inventory di bawah adalah seluruh instruksi halfword `lh/lhu` yang ditemukan di 26 fungsi terpilih pada disassembly resource ekonomi tersebut. Ini bukan bukti bahwa seluruh EXE/ROM telah dipindai tanpa sisa. Global `-0x158c` dari 0x80140000 adalah EA74 / peserta stride 0x90, **bukan tile**. Tile table adalah EA84 / `-0x157c`, stride 0x124. Pembuktian stride memakai `sll 3; addu index; sll 3; addu index; sll 2` = index×0x124 ditambah pointer EA84.

## CB2(a) — pembaca +0x0E dan +0x1A

### +0x0E — tiga pembacaan

| PC | Fungsi | EA84 + index×0x124 | Konteks |
|---|---|---:|---|
| 0x800D2768 | FUN_800D15A8 | Ya | Action byte +0x2EB=4; baca +0x0E lalu panggil FUN_80108DC8 dan setup kode UI 5. Tidak ada debit yang terbukti di blok ini. |
| 0x800D3BBC | FUN_800D15A8 | Ya | Index tile dari participant manager +0x2F8/+0x2FC, kemudian baca +0x0E dan panggil FUN_80108DC8. |
| 0x800C9990 | FUN_800C88F0 | Belum | Pointer petak didereferensi dari field pertama record peserta EA74; aliasnya belum dibuktikan sama dengan EA84. |

### +0x1A — sebelas pembacaan

| PC | Fungsi | EA84 + index×0x124 | Konteks |
|---|---|---:|---|
| 0x800D0AE4 | FUN_800D05B8 | Ya | Index petak diambil dari participant EA74 +0x1F. |
| 0x800D2520 | FUN_800D15A8 | Ya | `a1` dibentuk dari EA84 + index×0x124; periksa type 5, owner, saldo, dan level+1<5. |
| 0x800D2ADC | FUN_800D15A8 | Ya | Index dari participant EA74 +0x4D9. |
| 0x800D2B5C | FUN_800D15A8 | Ya | Index manager +0x1450. |
| 0x800D3EE4 | FUN_800D15A8 | Ya | Index peserta/loop dan base EA84. |
| 0x800D3F74 | FUN_800D15A8 | Ya | Index dari participant manager +0x2F8/+0x2FC. |
| 0x800D4628 | FUN_800D15A8 | Ya | Fee dalam transaksi action 3/8. |
| 0x800D46EC | FUN_800D15A8 | Ya | Fee dibaca kembali sebelum pending debit. |
| 0x800CA748 | FUN_800C88F0 | Belum | Pointer berasal dari field pertama record EA74; alias tile belum terbukti EA84. |
| 0x800E3FBC | FUN_800E3E74 | Ya | Index tile dari field participant +0x1F. |
| 0x800EB570 | FUN_800EB434 | Ya | Index manager +0x14F4 dan base EA84. |

Ringkasan pada cakupan scan ini: 3 pembacaan +0x0E (2 terbukti EA84, 1 alias belum pasti); 11 pembacaan +0x1A (10 terbukti EA84, 1 alias belum pasti). Excerpt instruksi singkat:
- `lw a0,-0x157c(s0)`
- `lhu a0,0xe(v0)`
- `lhu a0,0x1a(v0)`
- `lhu a0,0x1a(a1)`
- `lw v0,-0x158c(s1)`

## CB2(b) — jalur biaya/level dan pemicu

### Pemilihan petak milik sendiri

Di FUN_800D15A8, PC 0x800D24E0 memeriksa tile type 5. PC 0x800D24F8–0x800D2504 mengambil nibble owner dan membandingkannya dengan pemain aktif. PC 0x800D2520 membaca u16(tile+0x1A); PC 0x800D252C membandingkan saldo peserta dengan nilai itu. PC 0x800D2534–0x800D2544 mengambil level nibble bits 8–11, menambah 1, dan menguji hasil <5. PC 0x800D25D8 menetapkan flag seleksi.

Ini membuktikan jalur seleksi/kelayakan pada tile type 5 milik peserta. Namun keterkaitan langsung ke observasi “berhenti tepat di petak milik sendiri” belum dipastikan, dan rangkaian ini tidak sendiri membuktikan mutasi level final.

### Transaksi action byte 3/8

FUN_800D15A8 membaca action byte participant-manager +0x2EB pada PC 0x800D4470; action 3 dan 8 dialihkan ke blok transaksi bersama:
- 0x800D45D0 memanggil FUN_800BBD9C; 0x800D45E0 menyimpan index terpilih di manager +0x4A0.
- 0x800D4628 membaca u16(tile+0x1A) dari EA84 + index×0x124.
- 0x800D4634 membandingkan fee dengan saldo participant +0x04; saldo tidak cukup keluar.
- 0x800D46EC membaca fee lagi; 0x800D46F4 menegasikan; 0x800D46F8 menulis pending delta -fee ke manager +0x2EE.
- 0x800D4724–0x800D4764 menaikkan nibble tile+0x20 bits 8–11 satu tingkat (jalur memiliki batas <5).
- 0x800D47F4–0x800D4834 menaikkan nibble bits 4–7 satu tingkat.
- 0x800D4840 dan 0x800D4848 memanggil helper refresh.

Untuk transaksi 3/8, debit yang dibuktikan adalah **u16(tile+0x1A) flat**. Tidak ada perkalian dengan d, shift fee, atau rumus fee berdasarkan level absolut di blok itu. Kedua nibble yang diubah bertambah satu. Isi transaksi ini K4; label gameplay action 3/8 masih TIDAK TAHU.

### Action byte 4 dan +0x0E

PC 0x800D2678 menguji action byte 4; PC 0x800D2768 membaca u16(tile+0x0E), lalu memanggil FUN_80108DC8. Ini membuktikan +0x0E dipakai dalam jalur action-4/UI. **Tidak terbukti** bahwa nilai ini dinegasikan atau ditulis ke pending +0x2EE. Maka +0x0E baru kandidat nilai harga/preview, bukan debit build yang terkonfirmasi.

### Tiga pemicu yang diamati

Pengamatan “berhenti di bola kristal”, “berhenti di petak sendiri”, dan “menyelesaikan putaran” tetap hipotesis eksternal. Yang terpetakan statis hanya action byte 3/8, 4, 1, dan 0x1D pada state machine. Tidak ditemukan bukti yang mengikat ketiga pemicu itu satu per satu ke tiga ID event tertentu. Stop pada tile type 5 milik sendiri memiliki pemeriksaan owner/fee/level di atas, tetapi trigger input spesifiknya TIDAK TAHU. Tidak ada dasar menyatakan lompat level arbitrer sudah terbukti.

### Dua belas instruksi sebelum setter 0x8001387C

Callsite: FUN_800BE5D8, PC 0x800BEC98 → FUN_8001387C.

| PC | Instruksi |
|---|---|
| 0x800BEC68 | `addiu v1,v1,0x4` |
| 0x800BEC6C | `addu v1,v1,v0` |
| 0x800BEC70 | `lw v0,0x0(v1)` |
| 0x800BEC74 | `nop` |
| 0x800BEC78 | `addiu v0,v0,0x2710` |
| 0x800BEC7C | `sw v0,0x0(v1)` |
| 0x800BEC80 | `lw v0,-0x158c(s2)` |
| 0x800BEC84 | `sll s0,s1,0x3` |
| 0x800BEC88 | `addu s0,s0,s1` |
| 0x800BEC8C | `sll s0,s0,0x4` |
| 0x800BEC90 | `addu v0,v0,s0` |
| 0x800BEC94 | `lw a1,0x4(v0)` |

Pada callsite, a1 berasal dari participant EA74 + playerIndex×0x90 +0x04: saldo kerja peserta. Jadi a1 bukan fee dan bukan fee×m(d). FUN_800BE5D8 memproses signed pending +0x2EE sebelum menyinkronkan saldo via setter. Debit -fee 3/8 berasal dari 0x800D46F8, bukan dihitung di 0x800BEC94.

## CB2(c) — caller FUN_800D15A8 dan token 0xBE

Direct-JAL scan memeriksa 149.103 aligned words dan menemukan satu raw JAL, satu decoded direct callsite, satu caller tervalidasi:
- caller FUN_800F3658;
- PC 0x800F5DAC: `jal 0x800d15a8`.

Detailed caller decompilation pada artefak census tidak berjalan (count 0). Karena itu kondisi upstream persis yang menyebabkan pemanggilan itu: TIDAK TAHU.

Pada jalur action byte 1/0x1D:
- PC 0x800D4970: `jal 0x80100dcc` (FUN_80100DCC);
- delay slot PC 0x800D4974: `li a0,0xbe`;
- lalu FUN_80100D14(1) dan FUN_80108EE8().
Ini membuktikan adanya hubungan cabang 1/0x1D ke helper message-window dengan token 0xBE. Helper itu bukan string lookup; arti Jepang token 0xBE TIDAK TAHU. Token ini bukan bukti Barrier Release.

### Rumus kredit positif yang terpetakan

State 1 di FUN_800D15A8 menghitung:

`C = u16(tile+0x1E) + (((u16(tile+0x20) >> 8) & 0xF) × u16(tile+0x1C))`

Urutan instruksi penting: 0x800D5260–0x5264 ekstrak level nibble; 0x800D5268 load +0x1C; 0x800D5270–0x5274 kalikan level×+0x1C; 0x800D5278 load +0x1E; 0x800D5280 jumlahkan; 0x800D5288 panggil FUN_80108EAC.

State 2 menghitung ekspresi setara (0x800D52D8–0x530C), dengan syarat manager+0x370==1 dan FUN_80102408()==0, lalu mengantrekan nilai positif ke manager +0x2EE dan memperbarui saldo proyeksi. FUN_800BE5D8 mengonsumsi antrean tersebut dan menyinkronkannya lewat setter Chakra kanonis FUN_8001387C. Maka rumus kredit positif dan jalur ke saldo Chakra terpetakan K4; identitas aksi itu sebagai Barrier Release tetap TIDAK TAHU.

Contoh:
- Record 4: +0x1C=70, +0x1E=84 → C level index 0..4 = 84/154/224/294/364.
- Record 7: +0x1C=84, +0x1E=112 → C = 112/196/280/364/448.

Kode kredit ini tidak membaca jumlah yang dibayar. Bonus kelompok 100–200% dan batas lima petak tidak terbukti tersambung ke jalur kredit; FUN_800B770C di blok 3/8 digunakan untuk nilai ekonomi tile pre/post, bukan bukti multiplier reward.

## Hipotesis dan falsifier

| ID | Hipotesis | Status bukti | Falsifier |
|---|---|---|---|
| A1 | Bangun memakai h0E; upgrade +1 memakai h1A flat. | Didukung sebagian: action 4 membaca h0E untuk helper UI; action 3/8 mendebit h1A flat. Semantik action belum terikat ke build/upgrade. | Gugur jika trace build yang teridentifikasi menunjukkan pending debit bukan h0E, atau trace upgrade menunjukkan debit bukan h1A. |
| A2 | Bangun dan upgrade sama-sama memakai h1A, atau ada pengali level absolut. | Belum didukung oleh blok yang dipetakan; tetap terbuka untuk jalur lain. | Gugur bila trace dua aksi yang teridentifikasi memperlihatkan debit build h0E dan upgrade h1A konstan pada semua level. |
| A3 | Debit = fee×m(d), m(1)=1 dan m(d>1)=2^d. | Tidak berlaku pada debit action 3/8 K4: fee dibaca langsung, tanpa operasi m(d). Tidak digeneralisasi ke semua trigger. | Gugur bila test sah untuk aksi yang sama membuktikan d=1 bukan fee, d=4 bukan 16×fee, atau m bergantung level absolut; runtime lintas d belum dilakukan di sini. |
| B1 | Kredit positif = h1E + idx×h1C sebelum multiplier kelompok; ini hasil Barrier Release. | Formula kredit positif K4; label Barrier Release belum terbukti. | Gugur untuk aksi release bila trigger release yang teridentifikasi menuju cabang lain atau hasilnya bukan C. |
| B2 | Kredit hanya terjadi pada sale/cashout, bukan release. | HIPOTESIS K1; nama event 1/0x1D belum terungkap. | Gugur bila Barrier Release teridentifikasi masuk ke 1/0x1D dan menghasilkan C pada saldo Chakra. |
| B3 | Kredit bergantung level/field ekonomi, bukan nominal pembayaran sebelumnya. | Didukung K4 untuk cabang kredit: operand berasal dari +1E, +1C, dan level; tidak memakai fee/debit paid. | Gugur bila trace cabang sama menunjukkan nominal paid menjadi operand kredit atau ada multiplier tambahan saat commit. |

Relasi data yang ditemukan terpisah: pada 17 record nonkosong, h1C×10=7×h1A dan h1E×10=7×h0E. Hubungan angka ini bukan bukti label gameplay.

## Putusan

- CB2(a): **SEBAGIAN K4** — reader pada 26 fungsi tercatat; satu alias basis belum jelas untuk masing-masing offset dan tidak diklaim exhaustive seluruh program.
- CB2(b): **SEBAGIAN K4** — debit flat h1A dan kenaikan nibble +1 pada action 3/8 terbukti; action 4 membaca h0E untuk helper UI; tiga trigger gameplay belum dipetakan.
- CB2(c): **SEBAGIAN K4** — satu direct caller dan cabang token 0xBE terbukti; kondisi upstream serta arti token TIDAK TAHU.
- CB2(d): tidak dilakukan (opsional).
- A secara gameplay: **SEBAGIAN K4**; field kandidat terpetakan, pembayaran bangun dan identitas operasi belum.
- B sebagai rumus reward positif: **K4**; B sebagai hasil Barrier Release: **TIDAK TAHU/K1**.

## Gerbang CB0/CB3

Commit text-only probe `87268e54fc501ea2a809010e989602e30a23d675` berhasil, tetapi GET `actions/runs?head_sha=87268e54fc501ea2a809010e989602e30a23d675` mengembalikan `total_count=0`, `workflow_runs=[]`; combined status mengembalikan `statuses=[]`. Tidak ada run/job/exit code. Oleh sebab itu CB3 tidak dijalankan: tidak ada H6 launch, RAM poke, atau perubahan Memory Card.
