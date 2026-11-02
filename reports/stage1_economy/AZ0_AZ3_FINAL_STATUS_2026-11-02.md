# Laporan akhir AZ0–AZ3 — ekonomi Stage 1
Tanggal: 2 November 2026
Game: Naruto Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Baseline: e2a2f4485dfa258d8a4d25599c26cab0c9ac551a

## Ringkasan status

| Bagian | Status | Kesimpulan |
|---|---|---|
| AZ0 | **SELESAI — lingkup direct writer Entry1** | 10 store langsung ke field manager teridentifikasi; byte, decode, base register, dan rantai pointer manager dicatat. |
| AZ1 | **SELESAI — lingkup H6 HYBRID** | 2 peluncuran × 2 frame; empat snapshot lolos; jalur tabel B30→global C88 terkonfirmasi dan nilai V dihitung ulang. H6 bukan target checkpoint murni. |
| AZ2 | **SELESAI — lingkup direct displacement Entry1** | 25 akses langsung B38/B40/B44 terpetakan: 17 reader dan 8 writer dengan base manager terkonfirmasi. |
| AZ3 | **SELESAI — jalur transaksi petak yang ditemukan** | Getter/setter, saldo awal, jalur transfer, serta jalur debit pembelian/peningkatan petak ditemukan. Biaya dibaca langsung dari tile+0x1A dan diterapkan lewat pending delta +0x2EE. |

**AZ0, AZ1, AZ2, dan AZ3 selesai sesuai lingkup audit statis yang dinyatakan.** Ini bukan klaim bahwa seluruh ekonomi game, semua overlay, semua pemanggilan tidak langsung, atau semua event gameplay sudah terurai. Identitas nama aksi kode 3/8 dan beberapa jalur tidak langsung tetap **TIDAK TAHU**.

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

## AZ3 — saldo, transfer, dan debit pembelian/peningkatan petak

### Saldo kanonis dan nilai awal

Direct caller census setter `0x8001387C`:
- Entry1: 14/14 direct JAL candidates divalidasi Ghidra.
- MAIN_EXE: 2/2 divalidasi.
- Total 16 direct JAL.

`FUN_8001387C(i,value)` memvalidasi `i<4`, membatasi value ke rentang -9999..99999, lalu menyimpan ke `0x80070EA0+i*0xB4+0x18`. Getter `FUN_800138EC(i)` membaca field yang sama (atau mengembalikan 0 untuk indeks tidak valid). Field +0x18 adalah saldo Chakra kanonis pada record pemain. Field participant +0x04 yang dipakai banyak state handler adalah salinan kerja/shadow yang disinkronkan kembali melalui getter/setter.

Callsite MAIN_EXE `0x80012DD4` bukan debit. `FUN_80012A44` membaca global `0x80070C80`, lalu `FUN_80012C70` mengirim nilai itu ke setter untuk setiap indeks pemain. Dua writer langsung C80:
- `FUN_80012780`, PC `0x800127D0`: membaca `MEM32[0x8006491C+(param_1&0xFF)*0x30]`.
- `FUN_80012EAC`, PC `0x80012F64`: membaca selected mode/state row+0x04 di `0x8005779C+idx*0x54`.

Jadi C80 merupakan sumber nilai awal saldo pemain secara statis K4. Makna rinci kolom +0x04 pada kedua sumber tabel dan nilai runtime C80 pada H6 tetap **TIDAK TAHU**.

### Jalur debit transaksi petak — bukti langsung

Fungsi `FUN_800D15A8` memproses state papan dan membaca action byte `participant_manager+0x2EB`. Pada cabang action **3 atau 8**, fungsi:
1. Memilih indeks petak melalui `FUN_800BBD9C()` dan menyimpannya di `participant_manager+0x4A0`.
2. Membaca biaya sebagai unsigned halfword `fee = u16(tile+0x1A)`.
3. Membandingkan biaya dengan saldo kerja pemain `participant[DAT_8013EA6E]+0x04`. Cabang transaksi hanya berjalan bila `fee <= balance`.
4. Menulis pending delta pemain aktif pada array `participant_manager+0x2EE` sebagai `-fee`.
5. Menaikkan dua level nibble pada word petak `tile+0x20` masing-masing satu: nibble bits 8–11 dan nibble bits 4–7.
6. Memanggil `FUN_800BB004` dan `FUN_800BE464` untuk memperbarui representasi/atribut petak setelah level berubah.

**Kesimpulan mekanis K4:** untuk cabang transaksi petak action 3/8 yang dianalisis, biaya tidak dihitung sebagai `Q(i)-cost` tepat sebelum setter. Biaya dibaca langsung dari data record petak `u16(tile+0x1A)`; jika saldo cukup, delta debit `-fee` ditulis ke pending per pemain dan level tile dinaikkan. Dengan kata lain, sumber nominal transaksi adalah field +0x1A pada record petak, bukan rumus V dari `FUN_800B770C`.

Field +0x1A bersifat per-record; nilai biaya konkret untuk setiap tile belum dipetakan satu per satu dalam laporan ini. Label nama gameplay untuk action byte 3 versus 8, dan apakah setiap kode berarti jenis bangun atau tingkat upgrade tertentu, tetap **TIDAK TAHU**. Tidak ada klaim bahwa semua bentuk pembelian atau semua overlay game memakai jalur yang sama.

### Pemrosesan debit dan jenis perubahan saldo yang berbeda

`FUN_800BE5D8` membaca signed pending delta `participant_manager+0x2EE+player*2`. Fungsi ini membagi nominal ke langkah animasi 1, 10, 100, 1000, dan 10000; menambah atau mengurangi saldo kerja participant +0x04 sesuai tanda; memanggil `FUN_8001387C`; kemudian membaca balik melalui `FUN_800138EC` dan menyinkronkan hasil ke field +0x04. Setelah animasi selesai, pending +0x2EE dibersihkan. Ini menghubungkan debit petak dengan saldo kanonis +0x18.

Jalur lain yang juga menggunakan +0x2EE tidak boleh disamakan dengan biaya bangun/upgrade:
- `FUN_800F3658`, pada event code karakter `'r'`, menghitung `amount = FUN_8010BDFC()*500`, membuat delta positif bagi satu peserta dan negatif bagi peserta lain, lalu mengantrekannya di `DAT_80139ECC`. Ini adalah jalur transfer antar peserta, bukan harga petak.
- `FUN_800DB29C` dan `FUN_800E0B3C` memindahkan nilai antrian `DAT_80139ECC` ke array pending +0x2EE dan mengosongkan sumber.
- `FUN_800F2A9C` juga membentuk pending delta dari helper nilai event dan jumlah peserta; ini merupakan distribusi event terpisah.
- Cabang lain `FUN_800D15A8` mengisi delta positif dari `tile+0x1E + level*tile+0x1C`. Rumus nilai positif ini teramati, tetapi label gameplay-nya—pendapatan, hadiah, atau settlement—tetap **TIDAK TAHU**.

### Batas bukti AZ3

- Debit petak action 3/8 dan asal nominal `u16(tile+0x1A)` terbukti secara statis K4 dari dekompilasi Entry1. Belum ada uji runtime untuk tindakan tersebut dalam sesi ini.
- H6 runtime AZ1 adalah checkpoint **HIBRIDA**, bukan target murni; snapshot H6 tidak digunakan sebagai validasi runtime untuk biaya transaksi ini.
- 12 instruksi JALR Entry1 dan 152 JALR MAIN_EXE yang tercatat adalah jumlah seluruh indirect call, bukan daftar pemanggil setter. Target JALR dinamis, overlay lain, dan computed call yang tidak terikat tetap **TIDAK TAHU**.
- Nama semantik action 3/8, makna positif `tile+0x1E + level*tile+0x1C`, dan nilai konkret biaya untuk setiap tile tetap belum ditetapkan.

**Status AZ3: SELESAI untuk jalur transaksi debit petak action 3/8, saldo, dan sinkronisasi yang ditemukan; sisa batas di atas tetap TIDAK TAHU dan tidak diperluas menjadi klaim universal.**

## Run Actions yang relevan

| Run | Job ID | Source SHA | Status | Exit |
|---|---:|---|---|---:|
| 41360900093 AZ1 H6 | 125010827198 | 4c537e3034bd0b2c2c0ad1a51312621843160910 | success | 0 |
| 41367221886 Step7/AZ3 direct census | 125029837518 | e98a2081e7f6573a75705d416f8a727a10634ced | success | 0 |
| 41367906993 Step7 caller/callee decompile | 125031924296 | 253dc96f92d95c76337bdbbf3292d0c388470493 | success | 0 |
| 41368276256 Step7 C80 global reference census | 125033025512 | 5822e40f3698e1b928619ee74ec4cef5a4913f70 | success | 0 |
| 41388731912 Step7 all direct setter caller decompilation | 125095241391 | 1368ad7e983e468a316b3ee283d76b110b9cb279 | success | 0 |
| 41389951934 Step7 event/pending delta decompilation | 125098923954 | 0802559834327f21a72c54ef9de46b2baa4790db | success | 0 |
| 41390225493 Step7 pending-global xref census | 125099758618 | 980485d6680131187c1e7b09322c9aca22d830b6 | success | 0 |
| 41390871544 Step7 extended transaction-state decompilation | 125101751085 | f052a6005bccc852d5fd0a70feaa5f0ec56a9f3f | success | 0 |

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
- AQ1/Step7 latest: aq1-run-41390871544/attempt-1/ (extended function decompilation; see ACTIONS_RUN_SUMMARY.txt and az3-resource-economy-function-detail.txt).

Tidak ada ISO/ROM, BIOS, Memory Card, savestate, raw RAM dump, screenshot, video/frame, atau binary yang dikomit.

## Perubahan analisis AZ

Exporter diperluas agar seluruh caller setter langsung dapat didekompilasi dan fungsi pembaca/penulis global delta dapat diekspor untuk kedua image. Bukti baru mengoreksi kesimpulan awal “tidak ditemukan Q-cost”: jalur pembelian/peningkatan petak memakai computed pointer ke pending delta +0x2EE, sehingga tidak akan muncul sebagai ekspresi `Q(i)-cost` pada direct JAL setter census.

Berkas kode/workflow yang diubah selama audit:
- `tools/ghidra/ExportTargetCallers.java`
- `tools/ghidra/ExportFunctionDetail.java`
- `.github/workflows/step7-entry1-buffer-base-audit.yml`
