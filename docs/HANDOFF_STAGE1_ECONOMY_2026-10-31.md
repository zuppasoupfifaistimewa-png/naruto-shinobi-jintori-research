# Handoff — Stage 1 economy Naruto vs Mizuki (31 Oktober 2026)

## Tujuan

Menjawab tiga pertanyaan ekonomi Stage 1:
1. pendapatan petak: pemicu dan rumus;
2. biaya build dan upgrade Barrier L1–L5;
3. nilai/cara hitung Chakra dari 結界開放 (Barrier release).

## Batas kerja sesi ini

- Repository yang dipakai hanya `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`.
- HEAD saat checkpoint dimulai: `d0ef96970724c85d8bcd2c5c7fb8ba58bac04072`; sudah diverifikasi sebagai main pada saat itu.
- HEAD tersebut 70 commit di atas `17a83a587031328d841c80bc4b7273efc376e6a0`.
- Tidak ada emulator, input gameplay, savestate restore, atau uji runtime.
- Tidak ada ROM, BIOS, Memory Card, savestate, dump RAM, video, audio, atau frame gambar dalam commit ini.
- Tidak ada perubahan pada Release/visibilitas repository. Status WAIT/UNKNOWN/NO-GO tidak dinaikkan.

## Evidence scale

`docs/GAME_RULES.md` sebelumnya membedakan temuan kode/data, UI translation/guide, dan yang belum pasti, tetapi tidak memberikan angka K0–K5. Laporan Stage 1 memperkenalkan skala lokal:
- K0 = ringkasan visual sekunder, belum dibaca ulang dari frame mentah.
- K1 = ucapan transcript/ASR atau UI translation text.
- K2 = pembacaan langsung pada minimal dua frame mentah yang berbeda.
- K3 = data/instruksi ROM statis dan aritmetika cocok, tetapi semantik atau mapping runtime belum tertutup.
- K4 = rantai kode/data statis sumber→pembaca→mutasi→penulis tertutup dan resource mapping memadai.
- K5 = runtime terukur/reproducible.
K2 dan K4 belum dicapai untuk Q1–Q3 pada sesi ini.

## Dokumen kerja

1. `reports/stage1_economy/OBSERVATION_LEDGER_2026-10-31.tsv` — catatan peristiwa video dengan BELUM BISA dan jumlah frame mentah 0 bila tidak tersedia.
2. `reports/stage1_economy/HYPOTHESES_2026-10-31.md` — dua hipotesis bersaing per Q, residu, dan pengamatan pemfalsifikasi.
3. `reports/stage1_economy/STATIC_FINDINGS_2026-10-31.md` — Ghidra/Entry 1 findings, raw excerpt, alamat/fungsi, dan rancangan uji runtime (belum dijalankan).
4. Sumber video sebelumnya:
   - `reports/youtube_source_access/STAGE1_NARUTO_VS_MIZUKI_DEEP_DIVE_2026-10-31.md`
   - `reports/youtube_source_access/VIDEO_WATCH_ANALYSIS_2026-10-31.md`
   - `reports/youtube_source_access/TRANSCRIPT_PRELIMINARY_GAMEPLAY_NOTES_2026-10-31.md`

## Apa yang diketahui

### Q1 — pendapatan
- Video scene summary melaporkan toll 580 pada petak bernilai tinggi, tetapi tidak merekam waktu tepat atau delta saldo.
- Transcript 30:33–31:06 mengatakan setiap lap selesai memberi poin dari petak milik. Ini K1, bukan payout yang terukur.
- Static Entry 1 candidate view menemukan `FUN_800B770C` menghitung nilai per-record dari 16 halfword pada record, dengan selector/multiplier byte +0x0B (100/120/150/180/200%, default 0), dan bit dalam halfword +0x20 memilih nilai dasar.
- `FUN_800BDC4C` menjumlahkan nilai record status byte +0 == 5 untuk owner-like ID tertentu, membagi jumlah dengan dua, lalu menambahkan getter konfigurasi `0x80012A8C`. Itu belum terbukti sebagai kredit saldo/income.
- `FUN_800FC700` memakai nilai `FUN_800B770C` yang dinegasikan ketika menggambar fee pada petak dengan owner berbeda. Ini menunjukkan displayed fee/toll, bukan debit/kredit aktual.
- Pendapatan pemilik, timing pembayaran, dan formula income tetap UNKNOWN.

### Q2 — build/upgrade
- Tidak ada observasi video per transaksi yang memiliki nilai Chakra sebelum/sesudah, tile identity, atau biaya.
- Angka UI translation 60 (build), 150 (upgrade L1→L2), nilai L1 100/durability 2/2 dan contoh L1 lain 50 tersimpan di `docs/GAME_RULES.md`; itu bukan universal cost atau ledger frame sample.
- Scan immediate 60/150/580/1000 tidak menemukan hubungan dengan transaksi build/upgrade.
- Harga build dan tiap langkah upgrade L1→L5 tetap UNKNOWN.

### Q3 — 結界開放
- Visual scene analysis melaporkan Mizuki saldo negatif lalu Barrier release terjadi pada rentang 18:01–36:50. Tidak tersedia saldo sebelum/sesudah, tile/level yang dilepas, atau bukti otomatis vs dipilih.
- Label `KABE` dan `LVUP_ESTATE` pada resource bukan dispatch handler tervalidasi.
- Field manager candidate +0xB44 dari audit terdahulu belum tersambung ke release. Scanner Entry 1 terbaru memeriksa participant displacement +0x2EE, offset yang berbeda; jangan gabungkan keduanya.
- Jumlah/rumus Chakra release dan pemilihan tile tetap UNKNOWN.

## Video evidence blocker

Dokumen sumber yang tersedia hanya berupa scene summary (rentang adegan) dan transcript otomatis, bukan raw frame-by-frame notes. Raw video/frame tidak tersedia untuk inspeksi ulang pada sesi ini. Karena itu:
- jumlah frame unik yang membaca angka = 0 pada ledger;
- tidak dapat memenuhi minimum ≥3 build tile berbeda, ≥3 payout per pemain, semua level upgrade, atau 1 release transaction lengkap;
- tidak boleh menebak timestamp, Chakra delta, tile ID, level, atau nilai yang hilang.
Sumber YouTube yang tercatat: `https://www.youtube.com/watch?v=r30Rs_NuExc`.

## Status kerja dan langkah berikut

- Fase 0: dibaca; HEAD main baseline dan 70 commits sejak 17a83a5 ditinjau.
- Fase 1: SEBAGIAN; ledger dibuat, tetapi target observasi tidak terpenuhi karena tidak ada raw frames.
- Fase 2: SEBAGIAN; hipotesis bersaing dan falsifier ditulis, tetapi tidak ada fit rumus karena tidak ada ≥3 titik data.
- Fase 3: SEBAGIAN; per-record arithmetic dan displayed fee static path ditemukan; build/upgrade/release transaction belum tertutup. K maksimum K3.
- Fase 4: hanya rencana uji kecil; tidak dijalankan.
- Lanjutkan dengan membaca hasil Ghidra yang dipicu commit HEAD `d0ef969...` bila sudah tersedia. Jangan mengasumsikan workflow run telah selesai jika belum ada job/artifact/summary yang committed.
- Setelah itu telusuri callback toll → pending delta → perubahan balance, source table → LVUP_ESTATE transaction, dan handler KABE/release secara terpisah.
- Jangan gunakan angka pada video summary/transcript untuk mengubah WAIT/UNKNOWN/NO-GO atau menaikkan K ke K2/K4.


## Koreksi penting untuk pending fields (audit artefak Ghidra tambahan)

- Pada artefak lama, +0xB44 hanya terlihat di-reset dan dibaca renderer, sehingga asal dan maknanya belum diketahui. Run #41166812039 kemudian menemukan jalur tambahan `FUN_80109FEC`: B40 disalin ke B44, lalu B44 diterapkan bertahap ke Chakra melalui getter 0x800138EC/setter 0x8001387C (PC 0x8010A144–0x8010A160), dan dikurangi di PC 0x8010A648–0x8010A658. Maka B44 adalah field penyesuaian Chakra K3; asal B30/B38 dan event pemicu tetap UNKNOWN.
- Candidate PC setelah rebase old import `0x800D0000` ke `0x800AD450`: init `0x80109994`, store-zero `0x80109A54`, reader `0x80109BDC`/`0x80109F1C`, load `0x80109F64`.
- Field participant `+0x2EE` lebih dekat pada jalur delta per peserta: fungsi `FUN_800E1188` (candidate PC `0x800BE5D8`) membaca slot `DAT_8013EA74 + 0x2EE + participant*2`, lalu sinkronisasi lewat Chakra setter/getter di candidate PC `0x800BEC98`/`0x800BECA0`, dan membersihkan slot di `0x800BEDA4`. Sumber penulis nonzero belum ditemukan; belum ada kaitan terbukti dengan Q1/Q2/Q3.
- Offset +0xB44 dan +0x2EE tetap berbeda. Keduanya memiliki jalur pemrosesan Chakra, tetapi tidak ada yang terhubung secara statis ke event toll atau Barrier release.

## Actions provenance
Ringkasan teks run statis terdahulu beserta status, job, input SHA, kode keluar, dan artifact ID: `reports/stage1_economy/ACTIONS_STATIC_RUNS_2026-10-31.txt`. Untuk dua job lama yang log tersimpannya tidak menampilkan exit-code eksplisit, file tersebut menandai `NOT_LOGGED` dan tidak mengarang angka. Tidak ada workflow baru diluncurkan dalam sesi handoff ini.


## Addendum terbaru — run #41166812039 (mengoreksi catatan +0xB44 sebelumnya)

Run 41166812039/job 124436038028 selesai success, exit 0; input commit ad1dd4d9c7a05458cda20c1000e83c154bb3e73c. Ringkasan teks: reports/actions/run_41166812039_summary.txt; indeks: reports/stage1_economy/ACTIONS_STATIC_RUNS_2026-10-31.txt.

Keterangan sebelumnya bahwa +0xB44 hanya di-reset dan ditampilkan sudah dikoreksi oleh output baru. FUN_80109FEC menyalin B40 ke B44, lalu menambah Chakra lewat getter 0x800138EC (PC 0x8010A144) dan setter 0x8001387C (PC 0x8010A15C; delay slot 0x8010A160 menambah Chakra lama + B44). B40 = B30+B38 pada PC 0x80109A84–0x80109A94; nilai B44 kemudian dikurangi bertahap. Asal B30/B38 dan sumber event masih UNKNOWN; jangan label sebagai toll, income, refund, atau release.

+0x2EE adalah field participant-array yang terpisah dan memiliki consumer Chakra candidate FUN_800E1188/0x800BE5D8; warning decompiler tetap berlaku. Keduanya K3 parsial, bukan K4. Candidate import base 0x800AD450 belum runtime-validated.
Q1 income tetap UNKNOWN; Q2 semua harga Barrier UNKNOWN; Q3 release amount/formula/auto-vs-selected UNKNOWN. Tidak ada emulator, gameplay input, atau restore savestate.
