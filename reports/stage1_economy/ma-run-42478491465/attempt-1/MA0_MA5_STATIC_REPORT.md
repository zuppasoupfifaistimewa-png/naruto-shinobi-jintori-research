# MA0-MA5 static audit — SLPS-03553

Baseline inklusif: 662833da768f473349539eb3fe304dc7fa51a16c
Source SHA: 744a8f2ae7527cf7ef1781667c93735c293acb24
EXE SHA-256: a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569
Entry 1 SHA-256: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a
EMULATOR_LAUNCHES=0.

## Status
- MA0: TUNTAS K3 — Ghidra=PASS; ledger source/final-parent snapshot 18 commit (12 human, 6 bot); Actions 1260/1260 run, 13 halaman; py_compile 70/70; validasi bukti 15638/15638; kutipan maksimum 64 B.
- MA1: SEBAGIAN K3 — kandidat record scene 39 dalam 1 grup; batas stride utama 0x800558A4..0x80055CE8; pemanggil terindeks dan setter wallet tetap memerlukan closure.
- MA2: SEBAGIAN K3 — penulis EB1C=3, EA6E=13 (lhu EA88=0, 39EFC=0), EC7=3; semua SB terdaftar=5690; kandidat matrix lengkap/parsial=0/0; x=d dan x=ID belum terbukti.
  Byte konstan tersimpan EB1C: TIDAK TAHU,TIDAK TAHU,TIDAK TAHU.
- MA3: SEBAGIAN K3 — call ke B24C8=0, call ke parent=0, pointer parent=1, caller BE5D8=2; parent B24C8=teridentifikasi.
- MA4: TUNTAS K4 — statis saja; tanpa peluncuran emulator/game.
- MA5: BELUM K1 — tidak ada rumus biaya numerik lompat level d>=2.

## Batas bukti
Ghidra instruction listing dan referensi adalah hasil analisis statis; ketiadaan hasil pada scan tidak membuktikan tidak ada jalur alias/dinamis. Tidak ada nilai runtime, hasil fitting, atau formula dari pengamatan streamer.

## Validasi
- ACTIONS_TOTAL=1260; FETCHED=1260; PAGES=13; SCHEDULED=83; NON_COMPLETED_AT_CENSUS=5.
- PY_COMPILE=70/70.
- FILE_OFFSET_RAW_DECODE_CHECKS=15638; DECODED_INSTRUCTIONS=15518; FAIL=0.
- AGGREGATED_MAX_CONTIGUOUS_BYTES=64; OVER_LIMIT_GROUPS=0.

## Ledger final parent (publication commit dikecualikan)

- Baseline inklusif: 662833da768f473349539eb3fe304dc7fa51a16c
- HEAD parent tepat sebelum commit publikasi: 151d00dd1844babca09f7254906b45bded0c2640
- Rentang dihitung: 662833da768f473349539eb3fe304dc7fa51a16c^..151d00dd1844babca09f7254906b45bded0c2640; commit publikasi laporan sendiri tidak dihitung.
- Commit total: **19**; manusia: **12**; bot: **7**.
- Klasifikasi bot memakai heuristik nama/email; identitas ambigu harus ditinjau.
