# AL1–AL4 — penghentian emulator, relabel RAM, dekomposisi, dan rekonstruksi

Run #41042679829 attempt 1; job ak1-ak3; source commit 7e457a0ccae1fc9d499dc8d1c5020a4bab73b079.

## Skala bukti K0–K5
K0 = tidak ada bukti/fakta tidak diketahui; K1 = satu petunjuk belum diverifikasi; K2 = observasi eksplisit dari satu artefak/log; K3 = beberapa artefak statis konsisten dengan provenance; K4 = pemetaan/struktur statis direproduksi dan divalidasi independen, tanpa klaim runtime untuk semantik; K5 = observasi runtime memenuhi kriteria dan direplikasi pada sedikitnya dua peluncuran independen. Bukti statis saja maksimum K4.

## AL1 — penghentian emulator
Capture semua frame (1, 60, 180, 240, 360) valid: H6=True; kontrol=True. Baseline H6 AK1 pada frame 180/240/360 cocok di kedua peluncuran=True; expected={180: '4c964aaca0afccc68317acd0726fec680c305b903cd426e70afe3d8ac1f1e741', 240: '16880faeccfca1fbd42d199c1543b00ec8a065bcd53545d14ea4657c9a6c2d5c', 360: 'a9ac5282e9fb9ad1e77f46ef0c291af8e7e5f27b477b6b31e319f971e7dd9942'}. Pada frame360, PCSX.quit(0) dipanggil langsung dari callback nextTick capture, tanpa nextTick tambahan kedua. Ada marker sebelum dan selepas pemanggilan (marker selepas bisa tidak tercetak jika quit menghentikan proses).
H6 attempt1: exit_decimal=0; source=GDB 'exited normally' (normal process exit, decimal zero); watchdog=FALSE; quit0_call_marker=TRUE; wall_seconds=97.414.
H6 attempt2: exit_decimal=0; source=GDB 'exited normally' (normal process exit, decimal zero); watchdog=FALSE; quit0_call_marker=TRUE; wall_seconds=97.197.
CONTROL_NOT_TARGET attempt1: exit_decimal=0; source=GDB 'exited normally' (normal process exit, decimal zero); watchdog=FALSE; quit0_call_marker=TRUE; wall_seconds=99.936.
CONTROL_NOT_TARGET attempt2: exit_decimal=0; source=GDB 'exited normally' (normal process exit, decimal zero); watchdog=FALSE; quit0_call_marker=TRUE; wall_seconds=99.335.
MAX_TIME_TO_FRAME360_S=98.708170175552; timeout_per_launch_s=600; timeout_ge_2x_max_time=True; all_quit0_call_markers=True.
Akar sebab internal mengapa nested nextTick lama tidak menghentikan proses: TIDAK TAHU. Log lama mencatat watchdog frame1200 dan GDB code 065 tetapi tidak mempunyai marker pada batas callback nested. Perubahan direct-call adalah perbaikan yang diuji; bukan bukti definitif apakah callback lama tidak dijalankan atau tertunda.
Exit code GDB dikonversi dari basis oktal ke desimal. Field emulator_exit_code_decimal menyimpan hasil; emulator_exit_code_source menyebut sumber teks log GDB. Wrapper exit code tetap kolom terpisah.

## AL2 — pelabelan ulang (tanpa emulator run)
AL2 uses only the committed AK2_DIFF_RANGES.tsv; no emulator was launched for this relabelling.
A grouped range is allocated only when its entire inclusive span fits exactly one mapped field. Groups crossing a label boundary remain TIDAK_TAHU.
Ranges merge exact changed runs separated by gaps <=32 bytes. changed_bytes is exact per group, not per address, so a mixed group cannot be split accurately.
Player records: four records at 0x80070EA0 + n*0xB4. Known fields: candidate ID bytes +0x0A..+0x0C, Chakra word +0x18..+0x1B. Other record bytes remain TIDAK TAHU.
0x8013A554 is address/slot only; pointer semantics unresolved. 0x801CEF08 is only an address start; block extent/meaning unresolved.
H6_attempt1_180_vs_CONTROL_attempt1_180: exact_known=2; TIDAK_TAHU=56975; total=56977.
  0x801CEF08 overlap bound=1..3 bytes; grouped range 0x801CEF08..0x801CEF23 (span=28, changed=3); exact count TIDAK TAHU and stays inside TIDAK_TAHU total.
H6_attempt2_180_vs_CONTROL_attempt2_180: exact_known=2; TIDAK_TAHU=56975; total=56977.
  0x801CEF08 overlap bound=1..3 bytes; grouped range 0x801CEF08..0x801CEF23 (span=28, changed=3); exact count TIDAK TAHU and stays inside TIDAK_TAHU total.
TARGET_SOURCE_vs_H6_attempt1_180: exact_known=2; TIDAK_TAHU=4048; total=4050.
TARGET_SOURCE_vs_H6_attempt2_180: exact_known=2; TIDAK_TAHU=4048; total=4050.
AL2_FIELD_RELABEL.tsv memberi exact totals per label/perbandingan; rentang berkelompok yang melintasi batas label tetap TIDAK TAHU. Untuk 0x801CEF08 hanya overlap batas bawah/atas dari known_source_overlap yang tersedia; byte tepat tidak dipindah dari TIDAK TAHU.

## AL3 — target-source vs H6
H6 attempt1: D1=390 D60=651 D180=4050; @180 already present at @1=235; first appearing after @1=3815; @1 differences reverted by @180=155.
H6 attempt2: D1=390 D60=651 D180=4050; @180 already present at @1=235; first appearing after @1=3815; @1 differences reverted by @180=155.
Frame1 adalah VSync pasca-load pertama yang dilihat listener SaveStateLoaded. Pada tiap attempt, byte yang beda di frame180 dibagi menjadi sudah berbeda di frame1 dan pertama berbeda setelah frame1. Target-native tidak dapat dijadikan pembanding runtime karena restore target murni sebelumnya SIGSEGV; hasil ini tidak menyimpulkan semua selisih disebabkan replay 180 frame.

## AL4 — enam hibrida AE2
Rekonstruksi dari generator eksperimen dan hasil historical GDB dua-peluncuran: complete=True. Hash yang dilaporkan adalah REKONSTRUKSI dari input state tervalidasi; biner hibrida tidak disimpan.
Perincian target-current channels, control-current channels, outcome lama, source SHA, dan reconstructed hybrid SHA: AL4_HYBRID_RECONSTRUCTIONS.tsv.

## Putusan
AL1=LULUS; AL2=SELESAI_DENGAN_BATAS_RENTANG; AL3=KONSISTEN_2_LAUNCH; AL4=SELESAI. Host/RSI tetap DIPARKIR.

## Berkas hasil
AK1_REPLAY.tsv; AK1_FINDING.txt; AK2_DIFF_SUMMARY.txt; AK2_DIFF_RANGES.tsv; AL1_AL4_FINAL_REPORT.md; AL2_FIELD_RELABEL.tsv; AL2_RELABEL_NOTES.txt; AL3_BYTE_DECOMPOSITION.tsv; AL4_HYBRID_RECONSTRUCTIONS.tsv; ACTIONS_RUN_SUMMARY.txt; logs/*.gdb.txt; logs/*.pcsx.txt. Tidak ada ISO, BIOS, savestate, Memory Card, dump RAM mentah, atau biner hibrida yang dikomit.
