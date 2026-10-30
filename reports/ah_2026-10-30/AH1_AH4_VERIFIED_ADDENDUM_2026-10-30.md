# AH1–AH4 — addendum hasil terverifikasi (30 Oktober 2026)

## Skala bukti K
- **K0**: tidak ada bukti.
- **K1**: indikasi awal.
- **K2**: satu artefak/observasi terverifikasi; belum membuktikan hasil runtime yang diminta.
- **K3**: satu peluncuran runtime memenuhi kriteria, atau bukti runtime parsial dengan semantik belum terikat.
- **K4**: bukti kuat dan dapat diperiksa ulang, tetapi belum memenuhi replikasi runtime; bukti statis maksimal K4.
- **K5**: kriteria runtime terpenuhi pada sedikitnya dua peluncuran terpisah.

Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Game: Naruto — Shinobi no Sato no Jintori Gassen, PS1, SLPS-03553.
Status Story Mode tamat: **NOT VERIFIED**.

## Ringkasan status

| Butir | Status | K | Run / job / commit | Penilaian |
|---|---|---:|---|---|
| AH1 | **SEBAGIAN** | K2 | run 40966952270; attempt 1 job 123773754840 dibatalkan; attempt 2 job 123874229459 masih aktif; workflow commit 19d26af1a91e273b5c3bb2717af5032823239b09 | Run state dan persiapan terverifikasi, tetapi bisection belum menghasilkan ringkasan per hibrida. |
| AH2 | **SEBAGIAN** | K5 runtime; K3 untuk relasi RSI↔basis SPU | run 40998003879; job 123875562340; workflow source 572e10b76df40f3dc9f5dec21444c377ffe08b55; evidence commit 53fe55ff8d5eeab020bedce9fdfe482eac4cac04; summary commit 86768fd702c110246f98ad3cec6834b1ece9655b | Empat launch selesai dan terulang dua kali per checkpoint. Namun head SHA run bukan literal c9636874; beda hanya dua baris komentar, executable workflow dilaporkan identik. |
| AH3 | **TUNTAS** | K4 | static TSV/field-size tables: commit 53fe55ff8d5eeab020bedce9fdfe482eac4cac04 dan 4e028d91d769eacc09f600a1c9484333218cec61; producer control run 39867730674/job 120134061270 | 20/24 current target out-of-range; size delta +740 B; exit 92 direkonsiliasi sebagai watchdog, bukan emulator exit. |
| AH4 | **TUNTAS** | K5 (kontrol saja) | run 40998003879; job 123875562340; source commit 572e10b76df40f3dc9f5dec21444c377ffe08b55; evidence commit 53fe55ff8d5eeab020bedce9fdfe482eac4cac04 | Dua launch kontrol terpisah memberi hash RAM dan ketiga word identik; scope tegas BUKAN target. |

## AH1 — run 40966952270

Pemeriksaan terakhir pada 2026-10-30 sekitar 10:51 WIB:
- Run attempt 2: `in_progress`; workflow head SHA `19d26af1a91e273b5c3bb2717af5032823239b09`.
- Job attempt 1: `123773754840`; langkah 8 recursive bisection berakhir `cancelled`. Log menulis `The operation was canceled.`; penyebab pembatalan eksternal: **TIDAK TAHU**.
- Retry yang sudah berjalan: job attempt 2 `123874229459`, `bisect`, status `in_progress`.
- Langkah 1–7 success; langkah 8 `Recursive bisection into Channel occurrence 2` aktif; langkah 9 publikasi teks/hash dan 10 cleanup masih pending.
- Attempt 2 dimulai 2026-10-30 10:28:34 WIB. Timeout job 45 menit; batas maksimum 11:13:34 WIB jika belum selesai lebih awal.
- SHA setiap berkas hibrida, hasil dua launch per hibrida, SIGSEGV/POST_LOAD_VSYNC=180, waktu-ke-180 dan exit code final: **BELUM TERSEDIA / TIDAK TAHU**.
- Karena attempt 2 masih aktif saat pemeriksaan, tidak dijalankan retry paralel ketiga. Attempt 1 memang dibatalkan, tetapi retry yang diminta telah terjadi sebagai attempt 2.

Ringkasan status Actions (text):
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/43e56561b00043f20b22cdd93c055a980ed57cd1/reports/ah_2026-10-30/AH1_ACTIONS_RUN_40966952270_STATUS.txt

Run:
https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40966952270

## AH2 — target dan kontrol GDB

Workflow yang diminta pada commit `c9636874dd6480a2b6d00bc8a759f6ef8ceeba5b` tidak dijalankan dengan head SHA literal tersebut. Run tersedia `40998003879`, job `123875562340`, menggunakan `572e10b76df40f3dc9f5dec21444c377ffe08b55`. Ringkasan hasil menyatakan perubahan terhadap file workflow di c963 hanya dua baris komentar di akhir; 777 baris executable workflow identik. Status AH2 karena itu SEBAGIAN dalam hal provenance SHA persis, meskipun eksekusi target/kontrol tuntas.

Input:
- Target savestate SHA-256: `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`.
- Kontrol savestate SHA-256: `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`.

Hasil runtime:
| Checkpoint | Launch | Hasil | Waktu-ke-180 | Exit |
|---|---:|---|---:|---|
| Target | 1 | Thread 15 SIGSEGV pada PC 0x7ffff0dd36d0 | tidak mencapai marker | GDB wrapper 0; inferior exit sesudah signal tidak direkam |
| Target | 2 | Thread 15 SIGSEGV pada PC 0x7ffff0dd36d0 | tidak mencapai marker | GDB wrapper 0; inferior exit sesudah signal tidak direkam |
| Kontrol | 1 | POST_LOAD_VSYNC=180, inferior exited normally | 50 s | inferior 0; GDB wrapper 1 karena diagnostik pasca-exit `No registers` |
| Kontrol | 2 | POST_LOAD_VSYNC=180, inferior exited normally | 48 s | inferior 0; GDB wrapper 1 karena diagnostik pasca-exit `No registers` |

Actions job conclusion: `success`. Numeric job exit code tidak diekspos GitHub connector. Wrapper code kontrol 1 bukan exit code emulator.

Target registers yang terekam pada kedua launch:
- RIP = `0x7ffff0dd36d0`
- RSI = `0xffffffffd736da4f` (high32 `0xFFFFFFFF`, low32 `0xD736DA4F`)
- RDI = `0x00000000015885a0`
- RCX = `0x0000000000000001`

Thread/LWP: launch 1 Thread 15 / LWP 2948 / process 2931; launch 2 Thread 15 / LWP 2977 / process 2960.

24 instruksi `x/24i $pc-60` yang tercatat:
```asm
0x7ffff0dd3694: mov    %eax,0x94(%rdi)
0x7ffff0dd369a: ret
0x7ffff0dd369b: xor    %eax,%eax
0x7ffff0dd369d: nopl   (%rax)
0x7ffff0dd36a0: mov    (%rdx,%rax,1),%ecx
0x7ffff0dd36a3: mov    %ecx,0x24(%rdi,%rax,1)
0x7ffff0dd36a7: add    $0x4,%rax
0x7ffff0dd36ab: cmp    $0x70,%rax
0x7ffff0dd36af: jne    0x7ffff0dd36a0
0x7ffff0dd36b1: mov    0x18(%rsp),%rax
0x7ffff0dd36b6: mov    (%rax),%eax
0x7ffff0dd36b8: mov    %eax,0x94(%rdi)
0x7ffff0dd36be: ret
0x7ffff0dd36bf: nop
0x7ffff0dd36c0: push   %rbp
0x7ffff0dd36c1: mov    %rsi,%rax
0x7ffff0dd36c4: mov    0x18(%rdi),%r11d
0x7ffff0dd36c8: lea    0xd149f1(%rip),%r8
0x7ffff0dd36cf: push   %rbx
0x7ffff0dd36d0: movzbl (%rsi),%ecx
0x7ffff0dd36d3: mov    $0x4,%esi
0x7ffff0dd36d8: movzbl 0x2(%rax),%r9d
0x7ffff0dd36dd: movzbl 0x1(%rax),%r10d
0x7ffff0dd36e2: mov    %ecx,%edx
```

Backtrace Thread 15 pada kedua launch:
```text
#0  0x00007ffff0dd36d0
#1  0x0000000001588520
#2  0x00000000014f3490
#3  0x00007ffff0de5870
#4  0x0000000000000000
```

Mapping penting dari `info proc mappings`:
- PC executable mapping: `0x7ffff088c000–0x7ffff1892000`, size `0x1006000`, file offset `0x8c000`, perms `r-xp`, path disanitasi sebagai `<RUNNER_PATH>`.
- Heap launch 1: `0x01058000–0x10818000`, `rw-p [heap]`.
- Heap launch 2: `0x01058000–0x10822000`, `rw-p [heap]`.
- RSI `0xffffffffd736da4f` tidak masuk mapping aktif yang dilaporkan. Mapping shared `/dev/shm/pcsx-redux-wram` berukuran 8 MiB adalah WRAM; bukan bukti identitas SPU RAM.

Uji RSI:
- Target `ChannelData.current=0xD5E7578F`.
- `RSI_low32 - current (mod 2^32) = 0x014F82C0`.
- Kandidat `0x014F82C0` berada di dalam mapping generik `[heap]`, sedangkan RSI 64-bit sendiri (high32 FFFFFFFF) tidak dipetakan.
- Ini cocok secara aritmetika jika current diperlakukan sebagai offset bertanda, tetapi mapping tidak membuktikan bahwa kandidat adalah basis RAM SPU host.

**Koreksi ringkasan ekstraksi:** `AG2_AG4_RUNTIME_SUMMARY.txt` menuliskan RSI=TIDAK TAHU karena parser ringkasan gagal menangkap baris register; itu bukan kondisi log mentah. Kedua log target asli secara eksplisit mencatat RSI `0xffffffffd736da4f`. Nilai itu dipakai dalam analisis di atas.

Putusan hubungan `RSI = host SPU RAM base + current`: **TIDAK TAHU**, K3. Klaim historis `RSI=0xffffffffd736aa9f` **DIPERTAHANKAN sebagai observasi historis**, bukan sebagai nilai AH2 sekarang atau nilai universal: kedua raw log AD1 target pada run terdahulu 40860390103/job 123401839796 merekam nilai itu. Nilai AH2 saat ini pada kedua launch adalah `...d736da4f`.

Status klaim K4 AD2: **DIPERTAHANKAN secara terbatas** untuk mapping PC↔ELF path yang sama, file offset `0x5D36D0`, korelasi PT_LOAD, FDE range `0x5D36C0–0x5D3BD5`, dan 16 instruksi disassembly statis dalam AD2. K4 itu tidak mengidentifikasi fungsi crash secara persis dan tidak membuktikan basis RAM SPU. Basis SPU tetap K3.

Actions summary:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/86768fd702c110246f98ad3cec6834b1ece9655b/reports/ah_2026-10-30/AH2_ACTIONS_RUN_40998003879.txt

Runtime summary:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/53fe55ff8d5eeab020bedce9fdfe482eac4cac04/reports/ae_2026-10-30/AG2_AG4_RUNTIME_SUMMARY.txt

Full sanitized GDB log SHA-256 manifest:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/53fe55ff8d5eeab020bedce9fdfe482eac4cac04/reports/ae_2026-10-30/AG2_GDB_SHA256.txt

Full sanitized GDB logs:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/53fe55ff8d5eeab020bedce9fdfe482eac4cac04/reports/ae_2026-10-30/ag2_raw/target-attempt1.gdb.full.txt
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/53fe55ff8d5eeab020bedce9fdfe482eac4cac04/reports/ae_2026-10-30/ag2_raw/target-attempt2.gdb.full.txt
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/53fe55ff8d5eeab020bedce9fdfe482eac4cac04/reports/ae_2026-10-30/ag2_raw/control-attempt1.gdb.full.txt
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/53fe55ff8d5eeab020bedce9fdfe482eac4cac04/reports/ae_2026-10-30/ag2_raw/control-attempt2.gdb.full.txt

AD2 symbolization report:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/ae083f2b8a88f5762ae863c6b685009786c6658f/reports/ad_2026-10-29/AD2_symbolization.txt

## AH3 — 20/24 offset current dan selisih 740 byte

Rentang SPU RAM yang dipakai adalah offset `0x00000–0x7FFFF`. Tabel memuat 24 kanal. Sebanyak **20/24** nilai target `current` berada di luar rentang; 4 yang berada di dalam rentang adalah:
- channel 1: `0x00008430`
- channel 8: `0x00008F60`
- channel 19 dan 20: `0x0000A750`

SHA-256 TSV `AF1_SPU_POINTERS_TARGET_VS_CONTROL.tsv`: `37a8caa1a22436804d87e9d646dc295fe2f4c82ba35a80b0505a5315d4f020c6`.

TSV:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/69538f09f5251d3b91a0d405db671d204b0d4b16/reports/ae_2026-10-30/AF1_SPU_POINTERS_TARGET_VS_CONTROL.tsv

Ukuran raw savestate:
- target 21,163,286 bytes
- kontrol 21,162,546 bytes
- selisih target − kontrol **+740 bytes**.

Protobuf encoded field delta yang menyusun +740 B:
- top-level SPU field 6: +748 B
- registers field 4: +1 B
- CD-ROM field 8: −9 B
- jumlah +748 + 1 − 9 = +740 B.

Field sizes TSV:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/4e028d91d769eacc09f600a1c9484333218cec61/reports/ae_2026-10-29/ae1_field_sizes.tsv

Nested SPU subfields TSV:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/4e028d91d769eacc09f600a1c9484333218cec61/reports/ae_2026-10-29/ae1_spu_subfields.tsv

Rekonsiliasi producer kontrol run 39867730674/job 120134061270:
- Log emulator cycle 1 menulis checkpoint dan `ADAPTIVE_SESSION_FINISHED cycle=1`.
- Setelahnya muncul `corrupted size vs. prev_size`; emulator mencatat `ADAPTIVE_SESSION_EXIT cycle=1 code=134`.
- Orchestrator mendeteksi cycle 2 tidak menghasilkan capture F20/F60/F100/F110/F180 serta checkpoint hanya 1/2; kode Python menjalankan `SystemExit(92)`.
- Maka 134 merupakan kode keluar emulator setelah allocator error; 92 merupakan kode keluar watcher/orchestrator karena sequence/capture tidak lengkap. Penyebab korupsi heap: **TIDAK TAHU**.
- Producer control memakai AppImage SHA `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`; probe AH2 memakai AppImage SHA `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`. Dampak kausal perbedaan build: TIDAK TAHU.

Log provenance (kutipan historis AF4):
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/c0d5b5e7df392b7cb8c42b46dc23e4dd67c55f91/reports/ae_2026-10-30/AF4_PROVENANCE_LOG_EXCERPTS.txt

Potongan log producer kontrol run 39867730674 yang menunjukkan perbedaan exit emulator 134 versus orchestrator 92:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/cea09a6d78adf792c69d59ff63bde243d00301f0/reports/ah_2026-10-30/AH3_CONTROL_PRODUCER_EXIT_92_TRACE.txt

## AH4 — RAM kontrol saja (BUKAN TARGET)

Run 40998003879/job 123875562340. Scope hanya kontrol SHA `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`.

Dua launch terpisah mencapai POST_LOAD_VSYNC=180 pada 50 detik dan 48 detik. Timeout masing-masing 300 detik (6x dan 6.25x waktu-ke-180), lebih besar dari ambang 2x.

Pada kedua launch:
- RAM byte count: 2,097,152 (2 MiB).
- RAM SHA-256: `2a807d5847888d8ba0643cdf86818cfe0f7bb4645a216760f0caea4de91e9d20`.
- `0x80070EB8`: bytes `64 05 00 00`, LE32 `0x00000564`.
- `0x80070F6C`: bytes `64 05 00 00`, LE32 `0x00000564`.
- `0x8013A554`: bytes `08 EF 1C 80`, LE32 `0x801CEF08`.

K5 berlaku **hanya untuk dua launch kontrol ini**. Hash RAM target dan ketiga word target: **TIDAK TAHU**.

## Batas, perubahan repo, dan kelanjutan

Tidak ada ISO, BIOS, savestate, Memory Card, dump RAM atau screenshot gameplay yang dikomit. Snapshot RAM AH4 dikonversi menjadi hash dan word saja; data biner runtime sementara dihapus oleh workflow cleanup. Tidak ada perubahan visibilitas repo atau Release. Tidak ada input tombol pada eksperimen GDB AH2/AH4.

Untuk chat lanjutan:
1. Periksa run 40966952270, attempt 2, job 123874229459 sampai selesai atau timeout 11:13:34 WIB. Ambil summary final hibrida, SHA setiap state, hasil dua launch, waktu-ke-180 dan exit code; bila job gagal/cancelled, baca log dan lakukan retry sesuai hasilnya.
2. Jangan mengklaim AH1 tuntas sebelum hasil bisection dan cleanup dipublikasikan.
3. Jangan mengubah hasil AH2–AH4; bila mengoreksi tafsir RSI, pertahankan perbedaan antara bukti aritmetika dan identifikasi basis host.
4. Story Mode completion tetap **NOT VERIFIED**.
