# AL1–AL4 — penghentian emulator, relabel RAM, dekomposisi, dan rekonstruksi

Run #41042679829 attempt 1; job ak1-ak3; source commit 7e457a0ccae1fc9d499dc8d1c5020a4bab73b079.

H6 is a hybrid, not target-pure: target base with top-level field 6 (SPU) replaced by field 6 from control. H6_SHA256=d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475.

## Skala bukti K0–K5
K0 = tidak ada bukti/fakta tidak diketahui; K1 = satu petunjuk belum diverifikasi; K2 = observasi eksplisit dari satu artefak/log; K3 = beberapa artefak statis konsisten dengan provenance; K4 = pemetaan/struktur statis direproduksi dan divalidasi independen, tanpa klaim runtime untuk semantik; K5 = observasi runtime memenuhi kriteria dan direplikasi pada sedikitnya dua peluncuran independen. Bukti statis saja maksimum K4.

## AL1 — penghentian emulator
Capture semua frame (1, 60, 180, 240, 360) valid: H6=True; kontrol=True. Baseline H6 AK1 pada frame 180/240/360 cocok di kedua peluncuran=True; expected={180: '4c964aaca0afccc68317acd0726fec680c305b903cd426e70afe3d8ac1f1e741', 240: '16880faeccfca1fbd42d199c1543b00ec8a065bcd53545d14ea4657c9a6c2d5c', 360: 'a9ac5282e9fb9ad1e77f46ef0c291af8e7e5f27b477b6b31e319f971e7dd9942'}. Pada frame360, PCSX.quit(0) dipanggil langsung dari callback nextTick capture, tanpa nextTick tambahan kedua. Ada marker sebelum dan selepas pemanggilan (marker selepas bisa tidak tercetak jika quit menghentikan proses).
H6 attempt1: exit_decimal=0; source=GDB 'exited normally' (normal process exit, decimal zero); watchdog=FALSE; quit0_call_marker=TRUE; wall_seconds=97.414.
H6 attempt2: exit_decimal=0; source=GDB 'exited normally' (normal process exit, decimal zero); watchdog=FALSE; quit0_call_marker=TRUE; wall_seconds=97.197.
CONTROL_NOT_TARGET attempt1: exit_decimal=0; source=GDB 'exited normally' (normal process exit, decimal zero); watchdog=FALSE; quit0_call_marker=TRUE; wall_seconds=99.936.
CONTROL_NOT_TARGET attempt2: exit_decimal=0; source=GDB 'exited normally' (normal process exit, decimal zero); watchdog=FALSE; quit0_call_marker=TRUE; wall_seconds=99.335.
MAX_TIME_TO_FRAME360_S=98.708170175552; timeout_per_launch_s=600; timeout_ge_2x_max_time=True; all_quit0_call_markers=True.
Akar sebab internal mengapa nested nextTick lama tidak menghentikan proses: TIDAK TAHU. Log lama mencatat watchdog frame1200 dan GDB `exited with code 065`; 065 adalah oktal, yaitu 53 desimal. Log lama tidak mempunyai marker pada batas callback nested. Perubahan direct-call adalah perbaikan yang diuji; bukan bukti definitif apakah callback lama tidak dijalankan atau tertunda.
Exit code GDB dikonversi dari basis oktal ke desimal. Field emulator_exit_code_decimal menyimpan hasil; emulator_exit_code_source menyebut sumber teks log GDB. Wrapper exit code tetap kolom terpisah.

## AL2 — koreksi hitung byte (tanpa peluncuran emulator)
Bukti: AK1_REPLAY.tsv + AK2_DIFF_RANGES.tsv run #41042679829; workflow job ak1-ak3, job ID numerik 124019605576; job success. Source SHA 7e457a0ccae1fc9d499dc8d1c5020a4bab73b079; hasil run awal 493e6bf6bc4f2cc54c2221fe29a3e0d69ce70fd4.

Koreksi Chakra dan RNG (perbandingan H6 vs CONTROL, kedua attempt):
- P0 Chakra 0x80070EB8: H6 0x5DC = DC 05 00 00; kontrol 0x564 = 64 05 00 00; **1 byte berbeda**, K5.
- P1 Chakra 0x80070F6C: nilai dan pola byte sama; **1 byte berbeda**, K5.
- RNG 0x800A3118: H6 0x06CF4B77 = 77 4B CF 06; kontrol 0x1962C6BB = BB C6 62 19; **4 byte berbeda**, K5.
- Candidate ID P0–P3=0; Chakra P2/P3=0; pointer slot=0; block first byte=1; counter-like=2.

Empat total AL2 (label + TIDAK TAHU = total):
- H6 attempt1 vs CONTROL attempt1: P0 Chakra 1 + P1 Chakra 1 + block first byte 1 + RNG 4 + callback/tick-like 2 + candidate ID/pointer/P2-P3 Chakra 0 + TIDAK TAHU 56,968 = **56,977**.
- H6 attempt2 vs CONTROL attempt2: nilai sama, **56,968 + 9 = 56,977**.
- TARGET_SOURCE vs H6 attempt1: seluruh label known kecuali callback/tick-like 2 adalah 0; TIDAK TAHU 4,048; **4,050** total.
- TARGET_SOURCE vs H6 attempt2: sama, **4,050** total.

K5 di atas adalah replikasi nilai byte runtime pada dua peluncuran; K4 tetap untuk identifikasi field statis. Arti gameplay RNG, counter, dan area pointer tetap TIDAK TAHU.

### Cakupan SHA RAM
ram_2mib_sha256 menghitung 2 MiB pertama: RAM_BYTES=0x200000, ram[:RAM_BYTES], lalu SHA-256. ram_segment_bytes=8388608 melaporkan panjang field RAM hasil decode, yaitu 8 MiB; bukan jumlah byte yang di-hash. AK2_DIFF_SUMMARY menyatakan area diff 2 MiB pertama. Apakah segmen 8 MiB merupakan mirror 2 MiB adalah **TIDAK TAHU**. Nama kolom ram_2mib_sha256 benar dan dipertahankan.

## AL3 — target-source vs H6
H6 attempt1: D1=390 D60=651 D180=4050; @180 already present at @1=235; first appearing after @1=3815; @1 differences reverted by @180=155.
H6 attempt2: D1=390 D60=651 D180=4050; @180 already present at @1=235; first appearing after @1=3815; @1 differences reverted by @180=155.
Frame1 adalah VSync pasca-load pertama yang dilihat listener SaveStateLoaded. Pada tiap attempt, byte yang beda di frame180 dibagi menjadi sudah berbeda di frame1 dan pertama berbeda setelah frame1. Target-native tidak dapat dijadikan pembanding runtime karena restore target murni sebelumnya SIGSEGV; hasil ini tidak menyimpulkan semua selisih disebabkan replay 180 frame.

## AL4 — enam hibrida AE2 (REKONSTRUKSI)
Rekonstruksi dari generator eksperimen dan hasil historical GDB dua-peluncuran: complete=True. Hash yang dilaporkan adalah REKONSTRUKSI dari input state tervalidasi; biner hibrida tidak disimpan.
Perincian target-current channels, control-current channels, outcome lama, source SHA, dan reconstructed hybrid SHA: AL4_HYBRID_RECONSTRUCTIONS.tsv.

## Putusan
AL1=LULUS; AL2=DIKOREKSI (total byte dijaga); AL3=KONSISTEN_2_LAUNCH; AL4=REKONSTRUKSI. Host/RSI tetap DIPARKIR.

## Berkas hasil
AK1_REPLAY.tsv; AK1_FINDING.txt; AK2_DIFF_SUMMARY.txt; AK2_DIFF_RANGES.tsv; AL1_AL4_FINAL_REPORT.md; AL2_FIELD_RELABEL.tsv; AL2_RELABEL_NOTES.txt; AL2_RUNTIME_CROSSCHECK.txt; AL3_BYTE_DECOMPOSITION.tsv; AL4_HYBRID_RECONSTRUCTIONS.tsv; ACTIONS_RUN_SUMMARY.txt; logs/*.gdb.txt; logs/*.pcsx.txt. Tidak ada ISO, BIOS, savestate, Memory Card, dump RAM mentah, atau biner hibrida yang dikomit.

## AM1 correction provenance
AM1 tidak menjalankan emulator. Koreksi AL2 ini memakai AK1_REPLAY.tsv dan AK2_DIFF_RANGES.tsv yang sudah dikomit. Run #41042679829, job ak1-ak3, ID job numerik 124019605576, conclusion success. Cakupan SHA RAM dijelaskan di bagian AL2.
