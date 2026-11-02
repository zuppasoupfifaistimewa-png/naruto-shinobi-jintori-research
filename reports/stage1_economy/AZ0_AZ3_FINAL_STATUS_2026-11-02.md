# Laporan akhir AZ0–AZ3 — ekonomi Stage 1
Tanggal: 2 November 2026
Game: Naruto Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Baseline: e2a2f4485dfa258d8a4d25599c26cab0c9ac551a

## Ringkasan status

| Bagian | Status | Kesimpulan |
|---|---|---|
| AZ0 | **SELESAI dalam lingkup direct writer Entry1** | 10 store langsung ke field manager teridentifikasi dengan byte, decode, base register, dan instruksi pemuat pointer manager. |
| AZ1 | **SELESAI untuk H6 HYBRID** | 2 launch × 2 frame; 4 snapshot RAM lolos; dataflow tabel B30→global C88 terkonfirmasi; V petak dihitung ulang. Bukan target checkpoint murni. |
| AZ2 | **SELESAI dalam lingkup direct displacement Entry1** | 25 akses langsung B38/B40/B44; 17 reader dan 8 writer dengan base manager terkonfirmasi. |
| AZ3 | **SEBAGIAN** | 16 direct JAL ke setter terverifikasi; getter/setter dan seed chakra awal terurai. Rumus biaya build/upgrade belum ditemukan/dibuktikan; indirect caller belum terikat. |

**Jadi AZ0, AZ1, dan AZ2 selesai sesuai batas audit yang dinyatakan. AZ3 belum selesai sebagai rekonstruksi biaya ekonomi penuh.** Jangan menyebut seluruh AZ0–AZ3 tuntas secara menyeluruh.

## AZ0 — writer manager

Sepuluh direct store di Entry1:
- +0xB30: 1 writer, PC 0x80109990.
- +0xB2A: 1 writer, PC 0x80109A98.
- +0xB38: 1 writer, PC 0x80109980.
- +0xB40: 1 writer, PC 0x80109A94 (menulis hasil B30+B38).
- +0xB44: 6 writer, PC 0x80109A54, 0x8010A0F4, 0x8010A1C4, 0x8010A59C, 0x8010A5C8, 0x8010A658.

Semua base register terhubung secara statis ke pointer manager [0x8013A554]. TSV writer berisi instruksi mentah, decode MIPS, rantai instruksi sebelumnya, register efektif, serta offset file kandidat. Base impor 0x800AD450 tetap STATIC_CANDIDATE, bukan runtime mapping yang sudah dibuktikan.

## AZ1 — H6 runtime dan tabel ekonomi

Run runtime final: 41360900093; job ID 125010827198; source SHA 4c537e3034bd0b2c2c0ad1a51312621843160910; Actions PASS; script exit code 0.
Dua peluncuran independen pada frame 180 dan 360 menghasilkan empat snapshot valid. Emulator exit code decimal 0; Memory Card tidak berubah. SHA RAM 2 MiB:
- Frame 180: 5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7
- Frame 360: 4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907

H6 adalah target checkpoint base + CONTROL protobuf SPU field 6; **HIBRID, bukan target murni**. Tidak ada gameplay input atau RAM poke. K5 hanya berlaku untuk konsistensi pengamatan H6 ini.

Fungsi FUN_80012EAC memilih row:
idx=u8[0x80058758+mode*0x84+state_u8*0x0C]
table_B30=u32[0x80057798+idx*0x54+0x0C]
Pada semua snapshot mode=0, state byte=0, idx=0, row=0x80057798, B30 row+0x0C=400. Nilai itu mengalir melalui FUN_80012A80 ke global [0x80070C88]; global tersebut juga bernilai 400 di empat snapshot. Manager +0xB30=0 adalah field staging terpisah.

Array petak: pointer 0x8013B818, 22 record, stride 0x124. Semua selector=0 dan owner=15. 88 hitungan V lolos; sum(V)=1270 dan floor(sum/2)=635 pada tiap snapshot. Manager B38=0, sehingga B38=floor(sum semua V/2) tidak cocok pada H6 yang direkam; ini bukan penolakan untuk seluruh state game.

Helper statis FUN_800B770C: selector 0→B; 1→floor(12B/10); 2→floor(15B/10); 3→floor(18B/10); 4→2B; selector lain→0. Rumus selector 1–4 K4 statis; runtime H6 hanya menguji selector 0.

## AZ2 — reader/writer state manager

Census direct displacement Entry1:
- +0xB38: 6 akses (5 read, 1 write).
- +0xB40: 5 akses (4 read, 1 write).
- +0xB44: 14 akses (8 read, 6 write).
Total 25 akses langsung: 17 reader + 8 writer. Base register semua reader ditautkan ke pointer global manager [0x8013A554].

FUN_80109FEC menguji caller flag bit 0x20. Bila aktif, state manager +0xB2A mengatur fase 3–7. State 6 mengisi progress B44 menuju B40 dengan langkah 0x14; state 7 memindahkan Q(i)+B44 atau Q(i)+min(B44,0x14) ke participant +0x18 lalu menguras B44. Nama event gameplay di balik bit 0x20/state7—akhir putaran, settlement, atau Barrier release—tetap **TIDAK TAHU**.

## AZ3 — setter/getter, seed chakra, dan biaya

Direct caller census setter 0x8001387C:
- Entry1: 14/14 direct JAL candidates divalidasi Ghidra.
- MAIN_EXE: 2/2 divalidasi.
- Total 16 direct JAL.

FUN_8001387C(i,value) validasi i<4, clamp nilai ke -9999..99999, lalu store ke 0x80070EA0+i*0xB4+0x18. Getter FUN_800138EC(i) membaca field yang sama atau return 0 untuk index tidak valid.

Callsite 0x80012DD4 bukan pola debit. FUN_80012A44 hanya membaca global 0x80070C80; FUN_80012C70 mengirim nilai tersebut ke setter bagi setiap indeks pemain. Dua writer langsung C80 ditemukan:
- FUN_80012780, PC 0x800127D0: menulis dari 0x8006491C+(param_1&0xFF)*0x30.
- FUN_80012EAC, PC 0x80012F64: menulis dari selected mode/state row+0x04 di 0x8005779C+idx*0x54.
Ini membuktikan C80 adalah sumber nilai awal field chakra participant +0x18 secara statis K4. Nilai runtime C80 pada empat snapshot H6 sebelumnya tidak direkam; angka runtime C80 = TIDAK TAHU.

Callsite MAIN_EXE 0x80013170 mengirim selected table row+0x04 ke setter. Empat callsite state-machine mengirim Q, Q+B44 atau Q+min(B44,20). Tidak satu pun dari 16 direct JAL menghasilkan ekspresi Q(i)-cost.

Exporter juga mencatat 12 instruksi JALR di Entry1 dan 152 di MAIN_EXE, tetapi target register belum diikat ke setter. Itu bukan jumlah setter caller. Indirect/computed calls dan caller overlay lain tetap TIDAK TAHU. Dengan demikian **rumus harga bangun/upgrade = TIDAK TAHU**; AZ3 tetap SEBAGIAN.

## Run Actions yang relevan

| Run | Job ID | Source SHA | Status | Exit |
|---|---:|---|---|---:|
| 41360900093 AZ1 H6 | 125010827198 | 4c537e3034bd0b2c2c0ad1a51312621843160910 | success | 0 |
| 41367221886 Step7/AZ3 direct census | 125029837518 | e98a2081e7f6573a75705d416f8a727a10634ced | success | 0 |
| 41367906993 Step7 caller/callee decompile | 125031924296 | 253dc96f92d95c76337bdbbf3292d0c388470493 | success | 0 |
| 41368276256 Step7 C80 global reference census | 125033025512 | 5822e40f3698e1b928619ee74ec4cef5a4913f70 | success | 0 |

## Artefak teks utama

- AZ0_MANAGER_WRITER_CENSUS_2026-11-02.tsv
- AZ0_AZ1_HYPOTHESES_2026-11-02.md
- AZ1_FINAL_RUNTIME_REPORT_2026-11-02.md
- AZ1_V_SELECTOR_FORMULAS_2026-11-02.tsv
- AZ2_ENTRY1_FIELD_ACCESS_CENSUS_2026-11-02.tsv
- AZ2_MANAGER_READERS_2026-11-02.tsv
- AZ2_AZ3_STATIC_REGISTER_FLOW_2026-11-02.md
- AZ3_GLOBAL_70C80_SEED_FLOW_2026-11-02.tsv
- AZ3_SETTER_GETTER_MINUS_COST_CANDIDATES_2026-11-02.tsv
- Runtime H6: az1-h6-economy-runtime-run-41360900093/attempt-1/
- AQ1/Step7 latest: aq1-run-41368276256/attempt-1/

Tidak ada ISO/ROM, BIOS, Memory Card, savestate, raw RAM dump, screenshot, video/frame, atau binary yang dikomit.
