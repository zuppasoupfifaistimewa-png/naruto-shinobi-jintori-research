# Laporan final AN1–AN3 — Naruto: Shinobi no Sato no Jintori Gassen

Tanggal: 30 Oktober 2026  
Game: Naruto – Shinobi no Sato no Jintori Gassen (PS1), SLPS-03553  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

## Putusan akhir

| Task | Status | Tingkat bukti | Cakupan putusan |
|---|---|---:|---|
| AN1 — koreksi laporan dan identitas Actions | TUNTAS | K4 | Audit dokumen/statik; tidak menjalankan emulator |
| AN2 — replay H6 C/A/B dengan Memory Card terisolasi | TUNTAS | K5 | Runtime PCSX-Redux pada checkpoint H6 hybrid, dua launch per jadwal |
| AN3 — diff RAM C/A/B | TUNTAS | K5 | Perbandingan byte runtime H6 hybrid pada frame 180/240/360, dua attempt per pasangan |

**Batas utama:** H6 bukan savestate target murni. H6 dibentuk dari target savestate sebagai basis dan SPU top-level field 6 dari checkpoint CONTROL. Hasil AN2/AN3 tidak boleh digeneralisasi menjadi fakta target-native. Story Mode tidak dinyatakan tamat.

## AN1 — koreksi angka dan identitas Actions (TUNTAS, K4)

Koreksi final untuk masing-masing dari dua perbandingan H6 vs CONTROL:
- 9 byte berbeda yang dapat diberi label/known.
- 56.968 byte berbeda yang belum diketahui (TIDAK TAHU).
- Total 56.977 byte berbeda.

Angka sementara 3 known + 56.974 unknown dicabut. Angka 9 berarti **byte yang berubah dan dapat dipetakan**, bukan byte yang tidak berubah. Rincian label: Chakra word 0x80070EB8 = 1 byte; Chakra word 0x80070F6C = 1; RNG 0x800A3118 = 4; byte pertama block 0x801CEF08 = 1; word 0x80066E7C = 2; pointer slot 0x8013A554 = 0.

Koreksi identitas run:
- Run gagal #41048752354, job ID 124039280097, source SHA 240c448205b047f6dcbcb475c8f8b9cfca20c30a: HTTP 401, shell/curl exit 22, emulator tidak diluncurkan. Commit ringkasan bot: 123654ee3a2159befb477980286d460313a61420.
- Commit 4fbbbdf278ca71e0c84cb651287096561e9b4878 adalah perbaikan workflow, bukan output commit run gagal itu.
- Run AM3 yang berhasil #41048937290 dipublikasikan pada commit 51a66a060f3d4efda7eac7ada408b8d8ac88fe4c.

AN1 tidak menjalankan emulator. Tuntas K4 karena koreksi angka, identitas commit, dan keterkaitan dokumen dapat diperiksa statis/reproduktif.

Dokumen AN1:
- reports/am_2026-10-30/AN1_CORRECTION_ADDENDUM.md — commit daddd3f5147fe6f5b3a6734d1f6cee72f3d519f7.
- docs/HANDOFF_AL1_AL4_2026-10-30.md — commit 675416f94faffdad63bfcb397aedf56a2f7d5d54.
- reports/am_2026-10-30/AM1_AM3_FINAL_REPORT.md — commit a6b9a2efcac68b1490512b1f7a37ee7b7aaf9540.

## AN2 — replay emulator dan capture RAM (TUNTAS, K5)

### Identitas eksperimen

- Workflow run: #41080663095.
- Job: an2-an3-h6-isolated-mcd; numeric job ID: 124148564912.
- Source SHA run: 6800d4452af6e79aae29e394e8130305448b0f12.
- Commit publikasi hasil: 2c047d427c555cd2cebf15404e0cbbf7885e64d7.
- Status Actions: success; skrip exit code 0.
- Emulator: PCSX-Redux headless melalui GitHub Actions.
- Target savestate SHA-256: 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d.
- CONTROL savestate SHA-256: 9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492.
- H6 hybrid SHA-256: d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475.
- Memory Card acuan: 131.072 byte; SHA-256 ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5.

### Jadwal dan validasi peluncuran

C = tanpa input; A = Circle press frame 60/release 61; B = Circle press frame 90/release 91. Masing-masing dijalankan dua kali, total enam peluncuran. Setiap peluncuran membuat salinan Memory Card baru dari baseline identik.

| Jadwal | Attempt | Frame 360 (detik) | Circle press/release readback | Emulator exit |
|---|---:|---:|---|---:|
| C | 1 | 141.18541049957 | tidak berlaku | 0 |
| C | 2 | 141.28066134453 | tidak berlaku | 0 |
| A | 1 | 140.99376130104 | PASS / PASS | 0 |
| A | 2 | 141.19555091858 | PASS / PASS | 0 |
| B | 1 | 141.40045857430 | PASS / PASS | 0 |
| B | 2 | 141.03895092010 | PASS / PASS | 0 |

Hasil validasi:
- 30/30 capture PASS: frame 1, 60, 180, 240, 360 pada keenam launch.
- Keenam GDB wrapper exit 0; keenam emulator exit 0 dengan sumber “GDB inferior exited normally”.
- Watchdog tidak muncul; runner timeout tidak terjadi.
- Setiap Memory Card clone memiliki baseline SHA yang benar, ukuran akhir 131.072 byte, dan SHA sebelum/sesudah sama. Tidak ada Memory Card yang berubah.
- Waktu frame 360 paling lambat 141.4004585743 detik. Timeout tiap launch 600 detik, sekitar 4,24 kali waktu paling lambat, sehingga syarat minimal dua kali terpenuhi.
- Dalam setiap jadwal, dua launch menghasilkan RAM SHA yang sama pada kelima frame sampel.

Cakupan SHA RAM adalah 2 MiB pertama, mulai alamat 0x80000000. Kesimpulan determinisme berlaku untuk lima titik pengamatan tersebut; bukan klaim bahwa setiap siklus di antara titik itu identik.

### Nilai word yang diamati

| Frame pasca-load | 0x80070EB8 | 0x80070F6C | RNG 0x800A3118 | Slot 0x8013A554 | Word 0x80066E7C |
|---:|---:|---:|---:|---:|---:|
| 1 | 0x000005DC | 0x000005DC | 0x06CF4B77 | 0x801CEF08 | 0x24D3 |
| 60 | 0x000005DC | 0x000005DC | 0x06CF4B77 | 0x801CEF08 | 0x250E |
| 180 | 0x000005DC | 0x000005DC | 0x06CF4B77 | 0x801CEF08 | 0x2586 |
| 240 | 0x000005DC | 0x000005DC | 0x06CF4B77 | 0x801CEF08 | 0x25C2 |
| 360 | 0x000005DC | 0x000005DC | 0x06CF4B77 | 0x801CEF08 | 0x263A |

**RNG 0x800A3118 tidak berubah pada seluruh 30 capture**: nilainya selalu 0x06CF4B77. Ini hanya menyatakan tidak ada perubahan pada lima titik sampel; tidak membuktikan RNG tidak berubah di antara titik tersebut. Makna gameplay word 0x80066E7C dan pointer slot tetap TIDAK TAHU.

## AN3 — perbandingan diff RAM (TUNTAS, K5)

Perbandingan C/A, C/B, dan A/B dilakukan pada frame 180, 240, dan 360, untuk attempt 1 dan 2. Jadi ada 18 ringkasan perbandingan.

| Pasangan | Frame 180 | Frame 240 | Frame 360 |
|---|---:|---:|---:|
| C vs A | 25.068 byte | 24.994 byte | 24.756 byte |
| C vs B | 2 byte | 6 byte | 5 byte |
| A vs B | 25.068 byte | 24.992 byte | 24.758 byte |

Angka di atas sama untuk attempt 1 dan attempt 2. Diff TSV memiliki 18 SUMMARY rows dan 1.588 RANGE rows (1.606 baris data total). Setiap range menggunakan aturan pengelompokan dengan jarak byte tak berubah <= 32.

Audit konsistensi:
- Semua 18 ringkasan memiliki rekonsiliasi known + TIDAK TAHU = total.
- Semua 1.588 range juga seimbang.
- Jumlah changed bytes pada RANGE rows cocok persis dengan total SUMMARY yang bersangkutan; tidak ada mismatch.
- Semua byte yang berubah dalam diff AN3 masuk kategori TIDAK TAHU. Jumlah pada label yang sudah dikenal—CHAKRA, RNG, SLOT_0x8013A554, byte pertama BLOCK_0x801CEF08, dan 0x80066E7C—adalah nol untuk seluruh 18 perbandingan.

Cross-schedule RAM SHA sama pada frame 1 dan 60 untuk C, A, dan B. Perbedaan pertama pada titik sampel yang dibandingkan terlihat di frame 180, lalu tetap berbeda pada frame 240 dan 360.

### Jawaban eksplisit AN2/AN3

1. **Apakah RNG 0x800A3118 berubah pada capture?** Tidak. Semua 30 capture menunjukkan 0x06CF4B77.
2. **Apakah perbedaan A/B tetap ada dengan Memory Card terpisah?** Ya. Setiap launch memakai clone baseline yang sama; seluruh SHA pra/pasca Memory Card tidak berubah. RAM A dan B berbeda pada frame 180/240/360.
3. **Apakah C berbeda dari A/B?** Ya. C vs A menunjukkan 25.068/24.994/24.756 byte berbeda pada tiga frame; C vs B hanya 2/6/5 byte.
4. **Apa arti gameplay dari byte berbeda tersebut?** Belum diketahui. Semua delta AN3 berada di rentang yang belum berhasil diberi label; eksperimen tidak membuktikan Circle memilih tile, memulai giliran, mengubah chakra, atau memicu aksi gameplay tertentu.

Kesimpulan yang aman: input Circle pada jadwal A dan B benar-benar diterima oleh API input emulator (readback PASS). Pada H6 hybrid, jadwal A menghasilkan pola RAM yang berbeda besar dari C dan B; jadwal B sangat dekat dengan C pada byte yang dibandingkan. Pola ini berulang pada dua launch independen per jadwal dengan Memory Card yang diisolasi. Namun, karena byte berbeda belum dipetakan ke struktur/aturan gameplay, ini adalah temuan korelasi/keadaan memori runtime, bukan penjelasan semantik tindakan Circle.

## Perbaikan runner yang memungkinkan AN2/AN3 selesai

Run awal #41067396027 tidak menghasilkan capture: Lua runner gagal saat inisialisasi karena baris log memakai variabel `p` yang tidak terdefinisi di Lua, padahal variabel yang tersedia adalah `pressFrame`. Log memperlihatkan `attempt to compare number with nil` di `run.lua:67`, sebelum listener mulai menghitung frame. Ada juga salah nama field RNG di ringkasan (`word_0x800A3118` alih-alih `rng_0x800A3118`).

Koreksi:
- Runner diperbaiki agar memakai `pressFrame` dan nama field RNG yang benar.
- Timeout runner diubah agar mengirim sinyal ke seluruh process group GDB/emulator, bukan hanya wrapper.
- Log GDB/PCSX teks dipertahankan dalam output; file privat tetap di scratch sementara.
- Diagnostic run #41079972127, job 124146984375, source c8d344e6879704fae312dfc879148e72617f820a, publication commit f848e7014fa74633282112a896aabaf63dd876dd, exit 0: satu launch C menangkap kelima frame, emulator exit 0, Memory Card tidak berubah. Diagnostic ini hanya validasi boot, bukan AN2/AN3 completion.

## Privasi, pembersihan, dan batas

Langkah cleanup run penuh berhasil menghapus ISO, BIOS, savestate, Memory Card, RAM state, dan emulator sementara. Repo hanya menerima ringkasan teks, TSV, metadata, dan log teks GDB/PCSX. Tidak ada ISO, BIOS, Memory Card, savestate, dump RAM mentah, atau biner hybrid yang dikomit.

AN2/AN3 selesai pada cakupan H6 hybrid dan field RAM yang disampling. Belum ada pemetaan semantik untuk 299.298 akumulasi byte-diff lintas semua pasangan/frame/attempt records; angka ini adalah penjumlahan hitungan antar-perbandingan, bukan jumlah alamat unik global. Story Mode belum dinyatakan tamat.

## Raw permalink bukti utama

Semua URL berikut memakai SHA commit penuh tanpa parameter tracking:

- Actions run: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41080663095
- Ringkasan Actions: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2c047d427c555cd2cebf15404e0cbbf7885e64d7/reports/an_2026-10-30/runs/run-41080663095/attempt-1/ACTIONS_RUN_SUMMARY.txt
- Ringkasan AN2/AN3: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2c047d427c555cd2cebf15404e0cbbf7885e64d7/reports/an_2026-10-30/runs/run-41080663095/attempt-1/AN2_AN3_SUMMARY.txt
- Capture AN2: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2c047d427c555cd2cebf15404e0cbbf7885e64d7/reports/an_2026-10-30/runs/run-41080663095/attempt-1/AN2_CAPTURE_SUMMARY.tsv
- Diff AN3: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2c047d427c555cd2cebf15404e0cbbf7885e64d7/reports/an_2026-10-30/runs/run-41080663095/attempt-1/AN3_DIFF_RANGES.tsv

### GDB text log per launch

- C attempt 1: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2c047d427c555cd2cebf15404e0cbbf7885e64d7/reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/C-attempt1.gdb.txt
- C attempt 2: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2c047d427c555cd2cebf15404e0cbbf7885e64d7/reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/C-attempt2.gdb.txt
- A attempt 1: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2c047d427c555cd2cebf15404e0cbbf7885e64d7/reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/A-attempt1.gdb.txt
- A attempt 2: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2c047d427c555cd2cebf15404e0cbbf7885e64d7/reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/A-attempt2.gdb.txt
- B attempt 1: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2c047d427c555cd2cebf15404e0cbbf7885e64d7/reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/B-attempt1.gdb.txt
- B attempt 2: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/2c047d427c555cd2cebf15404e0cbbf7885e64d7/reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/B-attempt2.gdb.txt

## Berkas yang dipublikasikan oleh run penuh

Commit publikasi hasil: 2c047d427c555cd2cebf15404e0cbbf7885e64d7. Sebanyak 18 berkas teks dibuat:
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/ACTIONS_RUN_SUMMARY.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/AN2_AN3_SCRIPT_EXIT_CODE.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/AN2_AN3_SUMMARY.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/AN2_CAPTURE_SUMMARY.tsv
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/AN3_DIFF_RANGES.tsv
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/PUBLICATION_METADATA.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/A-attempt1.gdb.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/A-attempt1.pcsx.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/A-attempt2.gdb.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/A-attempt2.pcsx.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/B-attempt1.gdb.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/B-attempt1.pcsx.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/B-attempt2.gdb.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/B-attempt2.pcsx.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/C-attempt1.gdb.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/C-attempt1.pcsx.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/C-attempt2.gdb.txt
- reports/an_2026-10-30/runs/run-41080663095/attempt-1/logs/C-attempt2.pcsx.txt
