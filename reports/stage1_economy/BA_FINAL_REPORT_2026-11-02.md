# BA1–BA3 — hasil akhir audit resource petak Stage 1
Tanggal: 2 November 2026
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Target: SLPS-03553 / Naruto: Shinobi no Sato no Jintori Gassen

## Status

| Butir | Status | Kepastian | Hasil |
|---|---|---:|---|
| BA1 — identifikasi tabel dan selector | SELESAI | K5 untuk konteks H6 yang diuji | Resource 630 (0x276) dipilih pada keempat snapshot; tabel berisi 22 record × 0x1E byte. |
| BA2 — peta field dan helper nilai | SELESAI | K4 statis + K5 kecocokan layout H6 | 18 field sumber cocok 1.584/1.584; dua field init loader cocok 176/176. Helper FUN_800B770C direkonstruksi. |
| BA3 — validasi runtime berulang | SELESAI | K5 pada H6 hybrid | Dua peluncuran independen, frame 180/360, selector dan RAM identik per frame; Memory Card tidak berubah. |

## BA1 — tabel Stage 1 yang dipakai pada H6

Loader FUN_800B2A58 memanggil FUN_800F7ADC dengan resource ID FUN_800129E4()+0x276. FUN_8002D00C menggunakan indeks resource dikali 8 byte untuk mengakses direktori.

DAT_80070CD0 dibaca oleh FUN_800129E4(). Dua jalur penulis statis ditemukan:
- FUN_80012EAC: mengambil byte pertama row terpilih dari matriks mode/state di 0x80058758, lalu menulisnya ke 0x80070CD0.
- FUN_80012780(param_1): mengambil byte pertama row 0x80064918 + (param_1&0xFF)*0x30 dan menulisnya ke 0x80070CD0. Direct caller tidak ditemukan pada export xref; pemanggilnya TIDAK TAHU.

Pada H6 yang diuji selector aktual adalah 0 pada frame 180 dan 360 dari kedua peluncuran. Jadi ID yang diteruskan ke loader adalah 0x276+0=0x276, entry index 630. Ini spesifik pada konteks H6 tersebut, bukan ID universal untuk semua mode/state.

Entry 630: LBN 9360; ukuran 661 byte; file offset 0x11DE000; SHA-256 12c1a6ff1870f5c6fe33723beef14d93009b509d70caa882c5c6e8de8535e0c8. Header count=22 dan panjang tepat 1+(22×0x1E)=661.

Entry 638 memiliki bentuk ukuran yang sama tetapi nilainya tidak cocok dengan konteks runtime. Perbandingan terdahulu field tile+0x10: entry 630 cocok 88/88; entry 638 hanya 24/88. Pada BA3, selector aktual memilih entry 630 4/4 kali.

## BA2 — layout record dan helper nilai

Sumber memakai byte count pada awal buffer, diikuti record 0x1E byte; runtime tile stride 0x124. Pemetaan lengkap tercatat di BA2_TILE_RUNTIME_FIELD_MAP.tsv.

- 7 field byte dan 11 field halfword yang disalin: 1.584/1.584 cocok dengan record sumber entry 630.
- tile+0x06 diinisialisasi 0: 88/88 cocok.
- tile+0x20 diinisialisasi 0xF020: 88/88 cocok.
- Source record byte +0x05 tidak disalin; source byte +0x06 masuk ke runtime tile+0x05.

Helper FUN_800B770C memilih H=u16(R+0x10+((u16(R+0x20)>>7)&0x1E)), dengan R=[0x8013EA84]+index*0x124. Selector R+0x0B menentukan faktor:
- 0: H; 1: floor(12H/10); 2: floor(15H/10); 3: floor(18H/10); 4: 2H.
- selector >=5 mengembalikan 0 pada dispatch ini.

Koreksi makna field +0x1A: field ini bukan sekadar kandidat. Audit AZ3 statis membuktikan FUN_800D15A8 membaca u16(tile+0x1A) sebagai fee pada cabang action byte 3 atau 8, membandingkannya dengan saldo kerja, lalu menulis pending delta -fee jika cukup. Kode menaikkan dua nibble level tile+0x20. Jadi +0x1A terbukti sebagai sumber nominal biaya untuk dua cabang itu; nama aksi lebih rinci dan cakupan semua jenis build/upgrade belum terbukti.

## BA3 — runtime H6 dua peluncuran

GitHub Actions run 41418131290: SUCCESS; job BA3 two-launch H6 tile source/runtime field validation; job ID 125186874156; source SHA a3f57b45bc57b1cf555d39fef4125c49f59b86f1; skrip exit code 0.

Dua peluncuran independen mencapai dan mem-parsing frame 180 serta 360. RAM 2 MiB SHA frame 180 di kedua peluncuran sama: 5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7. RAM SHA frame 360 sama: 4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907.

Selector 0x80070CD0=0 pada keempat snapshot sehingga resource ID=630. Memory Card SHA sebelum/sesudah kedua peluncuran sama: ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5. Tidak ada input gameplay, RAM poke atau setter; artefak pribadi dihapus sebelum publikasi teks-only.

H6 menggunakan target checkpoint + CONTROL top-level protobuf field 6; H6 HYBRID, bukan checkpoint target murni. K5 di sini hanya berarti snapshot read-only konsisten untuk konteks H6 yang diuji, bukan validasi universal seluruh mode/transaksi.

## Batas yang tetap terbuka

- Nama gameplay yang tepat untuk action byte 3/8 belum dipastikan.
- Apakah biaya +0x1A berlaku pada semua bentuk build/upgrade belum terbukti.
- V dari FUN_800B770C bukan label semantic universal harga/pendapatan/hadiah.
- 0x800AD450 masih kandidat base impor statis; audit ini mencocokkan isi record sumber dengan isi tile runtime, bukan membuktikan base runtime global.
- Pemanggil FUN_80012780 tidak ditemukan pada xref langsung; tetap TIDAK TAHU.

Kesimpulan: BA1, BA2, dan BA3 selesai untuk identifikasi tabel Stage 1, peta field dan validasi snapshot H6 dua peluncuran. Batas semantik di atas tetap dicatat, tidak dinaikkan menjadi kepastian.
