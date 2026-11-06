# DY0–DY4 — laporan akhir audit statis (6 November 2026)

Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Baseline inklusif: f76a096862ceb88920df19b021a30870c74a9496
HEAD sebelum laporan ini: f56435ad90bd6001a7360b48950eb3585ababe23

## Status DY

DY0 — TUNTAS K4. Baseline inklusif sampai HEAD f56435a: ahead_by=4, total=5 commit, 3 manusia dan 2 bot.
DY1 — TUNTAS K4. Asal hasil branch tiga PC sudah dibatasi pada return JAL dan definisi lokal selepas JAL.
DY2 — SEBAGIAN K4. 730 store +0x20/+0x21 ditemukan; 50 base terbukti lewat slot tile array 0x8013EA84. Field+0x24 bukan level yang terverifikasi.
DY3 — SEBAGIAN K4. 44 direct store ke EFC; satu chain mengonsumsi nibble tile+0x20, satu chain lain melakukan penyesuaian signed. Makna gameplay manager belum terverifikasi.
DY4 — SEBAGIAN K4. Satu post -fee ke +0x2EE; dua store adalah clear. Loop/back-edge tidak terverifikasi karena audit gagal parse pada run 2.

K4 = bukti statis langsung yang dapat diperiksa. Tidak ada klaim K5.

## DY1 — JAL clobber

0x800EC814 bnez $v0: sumber = return JAL 0x8010CDF0; agar fall-through wajib $v0==0.
0x800EC874 bnez $v0: sumber = return JAL 0x8010D0F0; agar fall-through wajib $v0==0.
0x800EC890 beqz $v0: return JAL 0x800154E0 masuk ke $v1; instruksi 0x800EC88C sltiu $v0,$v1,0x10; fall-through wajib $v0!=0 (return unsigned $v1<0x10).
Semua origin berhenti di batas JAL/JALR; argumen caller-saved lainnya = TIDAK TAHU.
Catatan DX1: angka file_offset EXE pada run1 benar, tetapi teks source untuk EXE tidak lengkap; formula yang benar 0x800+(PC-0x80010000). Entry 1: 0x10BB000+(PC-0x800AD450).

## DY2 — store tile +0x20/+0x21

DY2_TILE_PLUS20_PLUS21_WRITERS.tsv memuat 730 store displacement literal: 294 EXE dan 436 Entry 1. Hanya 50 basisnya terbukti berasal dari slot pointer tile-array 0x8013EA84; 680 lainnya tetap unresolved.
DY2_TILE_ARRAY_WRITERS_ANNOTATED.tsv memuat detail 50 row yang terbukti, mask, sumber OR, shift 8/12 dan kategori origin. Global 0x8013EA88 / 0x8013EB0C / 0x8013EBB0 diperlakukan sebagai dynamic loads, bukan konstanta.
Action8 EC3A8: tile+0x24 dibaca di 0x800EC388; global 0x8013EAD2 dibaca di 0x800EC364; subu dilakukan di 0x800EC390 dan hasil ke manager+0x2B4. Ini selisih dua field, bukan bukti d level karena arti +0x24 = TIDAK TAHU.
Action8 EF3CC: sb $a0,0x2eb($v0); sumber $a0 dan basis $v0 = TIDAK TAHU.
Event3 D9570: tile+0x24 dibaca di 0x800DAF2C setelah indeks dari manager +0x1F/active slot; nilai disalin ke manager+0x390 di 0x800DAF34. Tidak ada subtraction di path event3 yang diperiksa; arti +0x24 = TIDAK TAHU.

## DY3 — 0x80139EFC dan helper

DY3_GLOBAL_80139EFC_WRITERS.tsv adalah scan direct effective address dan berisi 44 stores ke global 0x80139EFC. DY3_GLOBAL_80139EFC_ORIGIN_AUDIT.tsv menambahkan klasifikasi per-PC. Hanya dua local expression slices dalam kategori operasi yang diminta: (a) 0x800ECA64 memakai nilai EFC lama +1 dan nibble bits 8–11 dari tile+0x20 yang dibaca di 0x800ECA3C; (b) 0x800F188C melakukan sign/round adjustment dari EFC lama. Tidak ada dependency tile+0x1A atau resource +0x14/+0x15 yang terbukti dalam kedua slice.
File DS3_INDEX_GLOBAL_WRITERS.tsv lama sebenarnya memindai displacement -0x1450, yaitu global 0x8013EBB0, bukan EFC (-0x6104). Jadi jumlah 39 COMPUTED dari file DS3 itu bukan census writer EFC. Klaim tepat 20 COMPUTED writers EFC = TIDAK TAHU/tidak tereproduksi.
Helper RNG: counter 50 diset di 0x800ECAE8, disimpan 0x800ECAEC, dibaca/decrement di 0x800ECB00/08; stop saat -1 di 0x800ECB0C. RNG jal 0x80035D78 di 0x800ECB14; div/mfhi membentuk kandidat; kandidat ditulis ke EBB0 di 0x800ECB38; active-index dibaca dari slot 0x8013EA88 di 0x800ECB3C; retry jika sama di 0x800ECB44. Maksimum 50 percobaan.
DY3_MANAGER_FIELD_READERS.tsv adalah filter read access dengan manager base proven=YES dari tabel run1. Reader +0x4F0/+0x4F4/+0x534 tercatat dengan PC. Makna gameplay tetap hipotesis dalam DY3_HELPER_STATUS_HYPOTHESES.tsv; tidak diklaim.

## DY4 — posting debit dan hipotesis fee

Di direct call closure D15A8, tiga store ke +0x2EE: 0x800D1738 dan 0x800D1764 adalah clear nol; 0x800D46F8 satu-satunya post negatif yang terbukti. Jalur: 0x800D46EC lhu tile+0x1A; 0x800D46F4 negu; 0x800D46F8 sh ke +0x2EE.
Apakah post tunggal itu diulang oleh back-edge atau jalur indirect/JALR = TIDAK TAHU. Run 2 bermaksud menjalankan audit back-edge, tetapi script gagal parse sebelum analisis dimulai; tidak boleh menyimpulkan tidak ada loop.
DY4_FEE_HYPOTHESES_D1_D4.tsv: fee_dasar simbolik; 100/400/800/1600 adalah hipotesis pengguna, bukan data ROM. H1 2^d [2,4,8,16] bertentangan pada d=1. H2 lookup [1,4,8,16] TAUTOLOGI karena disalin dari empat titik pengguna. H3 linear d [1,2,3,4] bertentangan d=2..4. H4 akumulasi doubling [1,3,7,15] bertentangan d=2..4. Formula ROM = TIDAK TAHU.

## Dua run Actions

42185794833 — job dx0-dx4-static, job ID 127785690950, source SHA c191c117ba567607df0feab8e4fc11adce015807, PASS, exit 0. Input, analisis, cleanup, dan publikasi teks PASS.
42188220758 — job dx0-dx4-static, job ID 127793554443, source SHA 2c462adc93cc7e3088e88202d07883887c224f0e, FAIL, exit 1. Input verify dan cleanup PASS. Analyzer tidak berjalan: SyntaxError pada line 1148 karena list dy4_loop_summary ditutup dengan }) bukan }]. Summary/failure sudah dikomit.
Tidak ada run ketiga. Tidak ada game/emulator, BIOS/savestate, atau biner yang dikomit.

## Berkas yang diubah pada commit dalam rentang DY0

f76a096: reports/stage1_economy/DX0_DX4_RECONCILIATION_ADDENDUM_2026-11-06.md
c191c11: .github/workflows/dx0-dx4-raw-static.yml; tools/stage1/RunDX0DX4Raw.py
f8b9e9b: 38 files di reports/stage1_economy/dx0-dx4-raw-run-42185794833/attempt-1/ — nama lengkap ada pada DY0_FINAL_COMMIT_LEDGER.tsv
2c462ad: tools/stage1/RunDX0DX4Raw.py
f56435a: reports/stage1_economy/dx0-dx4-raw-run-42188220758/attempt-1/ACTIONS_RUN_SUMMARY.txt; reports/stage1_economy/dx0-dx4-raw-run-42188220758/attempt-1/ANALYSIS_FAILURE.txt

## Batas TIDAK TAHU

- Makna field tile+0x24 dan apakah selisih action8 benar-benar d level.
- Level target event3 dan makna gameplay field manager+0x390.
- Makna gameplay manager fields +0x4F0/+0x4F4/+0x534.
- Nilai runtime semua load dinamis, RNG hasil percobaan, dan isi tabel resource yang raw bytes-nya tidak dipersistenkan.
- Apakah jalur indirect/JALR mengulang post -fee; audit back-edge run2 tidak berjalan.
- Rumus biaya ROM berdasarkan d, serta identitas set tepat 20 COMPUTED EFC writers.

Statis saja; bukti maksimum K4. STATUS.md, Release naruto-checkpoint-39262213468 dan visibilitas repo tidak diubah.
