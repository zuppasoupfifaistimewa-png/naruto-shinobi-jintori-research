# AZ1 — laporan runtime final ekonomi Stage 1
Tanggal: 2 November 2026
Game: Naruto Shinobi no Sato no Jintori Gassen (SLPS-03553)
Bukti runtime: **K5 untuk H6 HYBRID** (dua peluncuran independen); bukan bukti target checkpoint murni.

## Identitas dan metode
- Run GitHub Actions: 41360900093
- Job: Restore H6 and inspect manager/tile records across two launches
- Job ID: 125010827198
- Status Actions: PASS; script exit code desimal 0
- Source SHA: 4c537e3034bd0b2c2c0ad1a51312621843160910
- H6 SHA-256: d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475
- Identitas H6: target checkpoint base + protobuf CONTROL top-level SPU field 6; **HIBRIDA, bukan target murni**.
- Tanpa gameplay input, tanpa RAM poke, tanpa setter call. Empat snapshot 2 MiB dibaca dari state capture sementara runner; semua binary sementara dibersihkan sebelum output text-only diterbitkan.

## Validasi per peluncuran

| Item | Launch 1 | Launch 2 |
|---|---:|---:|
| Frame 180 capture | PASS | PASS |
| Frame 360 capture | PASS | PASS |
| Wrapper exit desimal | 0 | 0 |
| Emulator exit desimal | 0 | 0 |
| Wall time | 174.090 s | 173.695 s |
| Memory Card SHA sebelum/sesudah | identik | identik |
| Memory Card SHA-256 | ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5 | ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5 |

Timeout per launch 900 s. Historical slowest 145.815 s; 2× historical=291.630 s. Observed slowest 174.090 s; 2× observed=348.180 s. Timeout 900 s memenuhi kedua batas.

SHA-256 RAM 2 MiB (0x80000000–0x801FFFFF):
- Frame 180, kedua launch: 5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7
- Frame 360, kedua launch: 4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907

Keempat snapshot diparse (ALL_FOUR_RAM_SNAPSHOTS_PARSED=True), SHA per frame identik antar-launch (TWO_LAUNCH_FRAME_SHA_IDENTICAL_PER_FRAME=True), table selection lengkap, script exit code 0.

## Global dan manager
Semua empat snapshot memiliki:
- [0x80070C88] = 400 (0x00000190).
- [0x8013A554] manager pointer = 0x801CEF08; pointer valid dalam RAM 2 MiB.
- Manager +0xB2A=0; +0xB2B=0; +0xB30=0; +0xB38=0; +0xB40=0; +0xB44=0.

## Baris tabel B30 yang dipilih
Fungsi statis FUN_80012EAC:
idx = u8[0x80058758 + mode*0x84 + state*0x0C]
table_B30 = u32[0x80057798 + idx*0x54 + 0x0C]

Pada seluruh empat snapshot: mode word [0x80070734]=0, state byte [0x8007073C]=0, matrix index address=0x80058758, index byte=0. Baris tabel yang terpilih:
- Index = 0
- Row base = 0x80057798
- B30 table field = 0x800577A4
- Nilai B30 pada baris = **400** (0x190)
- Gate byte row+0x2E = 12

Nilai manager +0xB30 tetap **0**, jadi nilai table row 400 tidak sama dengan manager B30 yang sedang tersimpan. [0x80070C88] juga bernilai 400; kesamaan numerik ini **tidak** membuktikan keduanya mempunyai semantik atau jalur data yang sama. Jawaban yang aman: manager B30 aktual=0; selected table row B30=400 pada index0.

## Seluruh record petak dan V
- Pointer record [0x8013EA84] = 0x8013B818.
- Count [0x8013EAC8] = 22; stride=0x124.
- Status per record pada +0x00: status0=1; status1=2; status2=2; status4=17; status5=0 pada snapshot yang diamati.
- Selector +0x0B: 0 untuk seluruh 22 record.
- Owner=(u16@+0x20)>>12: 15 untuk seluruh 22 record.
- Seluruh 88 baris (22 × 2 frame × 2 launch) memiliki validation PASS dan V terhitung; unknown V=0.
- V dihitung ulang dari dispatch FUN_800B770C. Selector 0 memakai rasio 1:1, jadi V sama dengan selected B u16.
- sum(V) semua record = 1.270 pada setiap snapshot; floor(sum(V)/2) = **635**.

### Perbandingan B38
Manager B38 aktual = **0**, sedangkan floor(sum seluruh V/2)=**635**. Jadi hipotesis B38=floor(sum semua V/2) tidak cocok pada state H6 yang direkam. Ini tidak membuktikan hubungan tersebut mustahil pada state/event lain, atau bila hanya subset owner/status tertentu yang diperhitungkan. Status5 tidak memiliki record pada snapshot ini; nol record bukan bukti bahwa status itu tidak dipakai game.

## Batas bukti
K5 di sini hanya untuk konsistensi pengamatan runtime pada H6 HYBRID dan frame/launch yang dinyatakan. Ini bukan bukti target murni. Identitas gameplay B30/B38/B40/B44 sebagai pendapatan, biaya, settlement, akhir putaran, atau Barrier release tetap tidak ditetapkan tanpa jejak instruksi/runtime lanjutan yang mengikat nama event itu.
