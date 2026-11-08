# NA0-NA5 static audit — SLPS-03553

Baseline inklusif: 7bcfef67d0adf89b7ab0cb20e040790f15766017
Source SHA: 4d0a963012c01ecc46cb1d531927205debaaf9b8
EXE SHA-256: a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569
Entry 1 SHA-256: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a
EMULATOR_LAUNCHES=0.

## Status
- NA0: SEBAGIAN K2 — Ghidra=PASS; ledger source/final-parent snapshot 5 commit (3 human, 2 bot); Actions 1254/1254 run, 13 halaman; py_compile 68/68; validasi bukti 15638/15638; kutipan maksimum 124 B.
- NA1: SEBAGIAN K3 — kandidat record scene 39 dalam 1 grup; batas stride utama 0x800558A4..0x80055CE8; pemanggil terindeks dan setter wallet tetap memerlukan closure.
- NA2: SEBAGIAN K3 — penulis EB1C=3, EA6E=13 (lhu EA88=0, 39EFC=0), EC7=3; semua SB terdaftar=5690; kandidat matrix lengkap/parsial=0/0; x=d dan x=ID belum terbukti.
  Byte konstan tersimpan EB1C: TIDAK TAHU,TIDAK TAHU,TIDAK TAHU.
- NA3: SEBAGIAN K3 — call ke B24C8=0, call ke parent=0, pointer parent=1, caller BE5D8=2; parent B24C8=teridentifikasi.
- NA4: TUNTAS K4 — statis saja; tanpa peluncuran emulator/game.
- NA5: BELUM K1 — tidak ada rumus biaya numerik lompat level d>=2.

## Batas bukti
Ghidra instruction listing dan referensi adalah hasil analisis statis; ketiadaan hasil pada scan tidak membuktikan tidak ada jalur alias/dinamis. Tidak ada nilai runtime, hasil fitting, atau formula dari pengamatan streamer.

## Validasi
- ACTIONS_TOTAL=1254; FETCHED=1254; PAGES=13; SCHEDULED=82; NON_COMPLETED_AT_CENSUS=2.
- PY_COMPILE=68/68.
- FILE_OFFSET_RAW_DECODE_CHECKS=15638; DECODED_INSTRUCTIONS=15518; FAIL=0.
- AGGREGATED_MAX_CONTIGUOUS_BYTES=124; OVER_LIMIT_GROUPS=4.

## Ledger final parent (publication commit dikecualikan)

- Baseline inklusif: 7bcfef67d0adf89b7ab0cb20e040790f15766017
- HEAD parent tepat sebelum commit publikasi: 1b13991b29ece205ad26dba656eb9e23d6240af0
- Rentang dihitung: 7bcfef67d0adf89b7ab0cb20e040790f15766017^..1b13991b29ece205ad26dba656eb9e23d6240af0; commit publikasi laporan sendiri tidak dihitung.
- Commit total tanpa publikasi: **6**; manusia: **4**; bot: **2**.
- Dengan commit publikasi bot: **7**; manusia: **4**; bot: **3**.
- Klasifikasi bot memakai heuristik nama/email; identitas ambigu harus ditinjau.
