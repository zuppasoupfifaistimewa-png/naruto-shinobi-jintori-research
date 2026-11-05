# DM0–DM3 — audit statis LV writer dan selector resource (rekonsiliasi)

Tanggal: 5 November 2026  
Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`  
Baseline ledger: `6fa859e1f9cfdad7b968cd0df36f19a7fe50a5c1` (inklusif)  
Cutoff ledger: `eee699b1180c0befd8c2e7b4fd97f2bc95b9c929` (HEAD saat sesi ini dimulai, sebelum commit koreksi)  
Metode: rekonsiliasi Git history, AW1 field inventory, TSV level-bank, dan export instruksi MIPS statis yang sudah tersimpan. Tidak ada game/emulator atau job Actions baru.

## Ringkasan status

| Tugas | Status | K | Putusan |
|---|---|---:|---|
| DM0 ledger | TUNTAS | K4 | 2 commit sampai cutoff: 2 MANUSIA, 0 BOT. |
| DM1 writer LV | SEBAGIAN | K2–K4 | 326 PC dari inventaris yang tepat; 64 store PC ditemukan dalam export yang ditinjau (49 dengan 12 instruksi sebelumnya, 15 parsial); 10 LOADER_COPY; 0 COMPUTED yang terkonfirmasi; 262 tanpa store line dalam export yang ditinjau. |
| DM2 LV3–LV5 | SEBAGIAN | K3 | H1=15/39 dan H2=1/39 per-level pada 13 X; tidak ada model 13/13. |
| DM3 selector | SEBAGIAN | K4 untuk penulis; K0 untuk selector Stage 1 | Dua writer langsung ke 0x80070CD0 dan satu reader ditemukan. Selector Story Mode Stage 1 Naruto vs Mizuki tetap TIDAK TAHU. |

K statis maksimum K4. Tidak ada K5.

## DM0 — ledger commit

Rentang inklusif `6fa859e1f9cfdad7b968cd0df36f19a7fe50a5c1` sampai `eee699b1180c0befd8c2e7b4fd97f2bc95b9c929`: **2 commit = 2 MANUSIA + 0 BOT**. TSV mencatat SHA penuh, author, pesan, dan berkas perubahan per commit. Cutoff berhenti di HEAD saat sesi dimulai sehingga commit koreksi ini tidak masuk ledger.

## DM1 — census penulis +0x10..+0x18

**Sumber yang benar:** `reports/stage1_economy/aq1-run-41567757209/attempt-1/aw1-tile-field-function-inventory.tsv`. Sumber ini menghasilkan 326 PC unik. Angka 331 pada draft DM sebelumnya berasal dari file census lain dan tidak cocok dengan target 326 PC pada permintaan ini.

| Field | Candidate WRITE PC |
|---|---:|
| +0x10 | 144 |
| +0x12 | 13 |
| +0x14 | 65 |
| +0x16 | 7 |
| +0x18 | 97 |
| **Total unik** | **326** |

### Rekonsiliasi export instruksi

| Konteks store PC | Jumlah |
|---|---:|
| Store line ditemukan; 12 instruksi sebelumnya tersedia | 49 |
| Store line ditemukan; instruksi sebelumnya parsial | 15 |
| Store line tidak ditemukan dalam export yang ditinjau | 262 |
| **Total** | **326** |

| Label akhir | Jumlah | Makna |
|---|---:|---|
| LOADER_COPY | 10 | Tujuan tile dalam FUN_800F7ADC terbukti |
| COMPUTED | 0 | Writer computed ke tile yang terkonfirmasi |
| LAIN | 316 | Stack/local, objek non-tile, alias belum terbukti, atau instruksi belum tersedia |

**Sepuluh LOADER_COPY** pada FUN_800F7ADC:
`0x800F7CE8`, `0x800F7CFC`, `0x800F7D0C`, `0x800F7D20`, `0x800F7D30`, `0x800F7D44`, `0x800F7D54`, `0x800F7D68`, `0x800F7D78`, `0x800F7D8C`.

Loader merangkai byte little-endian dari source cursor +0x0A..+0x13 menjadi lima u16 di destination tile +0x10..+0x18; store tersebut adalah copy, bukan formula yang menghitung level dari X.

**Batas cakupan:** dalam export function-body statis yang berhasil dicocokkan pada sesi ini, ditemukan 64 dari 326 store PC: 49 mempunyai 12 instruksi pra-store dan 15 konteks parsial. Sisa 262 PC belum memiliki store line dalam kumpulan export yang ditinjau. Catatan CC3 historis menyebut 118 instruction windows; hitungan 118 itu tidak berhasil direproduksi dari file yang diverifikasi di sesi ini, sehingga tidak saya klaim sebagai hitungan baru. Semua 326 PC tetap dicatat di TSV; baris yang belum memiliki instruksi diberi `TIDAK_TERSEDIA`, bukan direka.

Dari instruksi yang tersedia, store dengan base `sp` adalah stack local/save/temporary. Store di FUN_800B2A58 dan FUN_800B63F4 memakai objek alokasi lokal 0x2D4, bukan EA84. Store FUN_800F6988 mengarah ke tabel auxiliary `0x8013ED28 + param_2*0x24`, bukan EA84. Untuk kandidat lain, displacement +0x10..+0x18 saja tidak membuktikan bahwa base register adalah tile base.

**Falsifier tabel tersimpan:** satu writer non-loader dengan base yang terbukti `EA84 + tile_index×0x124`, menghitung nilai LV, lalu menimpanya sebelum reader `FUN_800B770C` menggunakan nilai tersebut. Falsifier seperti itu belum ditemukan dalam export yang dapat diperiksa. Karena 262 PC belum memiliki store line dan sebagian alias base belum dibuktikan, tidak sah menyatakan bahwa writer computed tidak ada di seluruh program.

## DM2 — dua hipotesis rekursif baru LV3–LV5

Data DK1: 12 resource, 415 record, 248 record nonzero, 13 X berbeda (60, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320). Koefisien dan pembulatan ditentukan sebelum scoring; tidak ada fitting menggunakan kurang dari tiga titik.

- **H1:** level berikutnya = nearest-5-half-up(2.0 × prediksi level sebelumnya), rekursif LV2→LV3→LV4→LV5.
- **H2:** level berikutnya = ceil-to-10(1.9 × prediksi level sebelumnya), rekursif.

| Model | LV3 | LV4 | LV5 | Total per-level | X dengan ketiga level cocok |
|---|---:|---:|---:|---:|---:|
| H1 | 6/13 | 5/13 | 4/13 | 15/39 | 3/13 |
| H2 | 1/13 | 0/13 | 0/13 | 1/39 | 0/13 |

TSV DM2 menyimpan X, nilai observed, prediksi per level, status LULUS/GAGAL, dan skor tiap X. Falsifier bagi tiap aturan universal adalah satu level pada satu X yang berbeda dari prediksi; kedua hipotesis sudah difalsifikasi. H1 tetap kandidat parsial, bukan rumus game terverifikasi. H2 tidak didukung data ini. Tidak ada 13/13.

## DM3 — selector u8[0x80070CD0]

XREF statis menemukan dua store langsung dan satu reader:

1. **PC 0x800127E8 — FUN_80012780:** `sb v0,0x50(s0)`, dengan s0=0x80070C80 sehingga destination 0x80070CD0. Nilai berasal dari byte 0 row config `0x80064918 + ((param1 & 0xFF)×0x30)`; kondisi pemilihan row memakai low byte param1. Caller yang mengikat param1 ke mode/state belum ditemukan.
2. **PC 0x80012F4C — FUN_80012EAC:** `sb v0,0x50(s1)`, dengan s1=0x80070C80. Nilai diambil dari byte 0 row `0x80057798 + config_index×0x54`; config index dibaca dari `0x80058758 + 4×(33×mode + 3×state)`, mode=u32[0x80070734], state=u8[0x8007073C]. Writer ini secara langsung bergantung pada mode/state.
3. **Reader PC 0x800129E8 — FUN_800129E4:** `lbu v0,0xCD0(v0)`.

Selector resource memakai `resource_id=0x276+selector`. Inventory mode/state memiliki 2.844 baris, 2.816 selector nonblank. Distribusi: 0=2723; 1=11; 2=13; 3=10; 4=17; 5=2; 6=4; 8=1; 9=4; 15=7; 16=14; 17=10.

### Hipotesis bersaing: Story Mode Stage 1 Naruto vs Mizuki

- **HA:** selector 5 → resource 0x27B / Entry 635. Falsifier: rantai Stage 1 → mode/state/config terbukti menghasilkan selector selain 5.
- **HB:** selector 0 → resource 0x276 / Entry 630. Falsifier: rantai Stage 1 → mode/state/config terbukti menghasilkan byte selain 0.

**TIDAK TAHU — K0.** Tidak ada bukti yang menghubungkan identitas/flow Story Mode Stage 1 Naruto vs Mizuki dengan pasangan mode/state yang dibaca FUN_80012EAC. Caller FUN_80012780 yang menentukan param1 juga belum ditemukan. Mode/state 0/0 atau selector paling sering bukan bukti bahwa Stage 1 memilih selector 0.

## Batas dan integritas

- Statis saja; tanpa game/emulator, BIOS, savestate, ISO, dump, video, atau frame.
- Tidak membuat job Actions baru; tidak ada run/job/exit code baru.
- Tidak mengubah `STATUS.md`, Release, pengaturan Release, atau visibilitas repo.
- Tidak mengejar Chakra release.
- Pengamatan pengguna tidak dipromosikan menjadi fakta.

## Berkas yang diubah pada commit koreksi

- `reports/stage1_economy/DM0_COMMIT_LEDGER_2026-11-05.tsv`
- `reports/stage1_economy/DM1_TILE_LEVEL_WRITER_CENSUS_2026-11-05.tsv`
- `reports/stage1_economy/DM3_SELECTOR_WRITERS_2026-11-05.tsv`
- `reports/stage1_economy/DM0_DM1_DM2_DM3_STATIC_AUDIT_2026-11-05.md`
