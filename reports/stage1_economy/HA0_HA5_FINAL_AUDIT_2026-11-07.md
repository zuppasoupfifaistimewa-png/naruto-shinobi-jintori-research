# HA0–HA5 — hasil audit final dan status (2026-11-07)

Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research, branch main.

**Batas snapshot HA0:** baseline inklusif 14dccd2e1d2f92b1b919ad7f0686bf019c71dbf4 sampai HEAD sebelum laporan ini, 077941187650cb8e4b4920c48ac8012567ee5b97. Commit laporan ini dibuat sesudah snapshot tersebut dan tidak dihitung dalam angka ledger di bawah. Bukti statis merujuk EXE SHA-256 a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569 dan Entry 1 SHA-256 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a.

## Ringkasan status

| Tugas | Status | K | Hasil yang selesai | Batas yang belum selesai |
|---|---|---:|---|---|
| HA0 | TUNTAS | K4 | Ledger commit inklusif dan pemeriksaan seluruh Actions run dalam rentang | Run scheduled 42320736860 berasal dari SHA sebelum baseline, dicatat sebagai konteks saja |
| HA1 | TUNTAS | K4 | Offset, dua negu, helper excerpt 16+3, tiga jendela store; validasi ulang TSV selesai | Tidak ada kesalahan offset/decode yang tersisa pada 6.275 baris yang diuji |
| HA2 | SEBAGIAN | K3 | Helper/table addressing, seluruh fungsi F2A9C, jalur store, direct caller, analisis return bertipe void | Bound DAT_8006D794 dan nilai tabel tetap TIDAK TAHU; tidak ada indirect caller yang terkonfirmasi |
| HA3 | SEBAGIAN | K3 | 23 akses manager-backed, 12 write bernilai register, tiga reader diekspor dan ditelusuri secara statis; hipotesis dan falsifier ditulis | Dua writer literal-zero belum punya derivasi indeks per-site; makna ekonomi/gameplay akhir belum dibuktikan runtime |
| HA4 | BELUM | K0 | Artifact kandidat aktif dan checkpoint SHA-256 diverifikasi | CONTROL tidak dijalankan karena prasyarat eksplisit HA2 lengkap belum terpenuhi |
| HA5 | TUNTAS untuk katalog simbolik | K3 | Rumus simbolik tiga store, model d=1..4, dan falsifier runtime tersedia | Nilai numerik/rumus biaya final tidak dapat disimpulkan tanpa bound, isi tabel, dan bukti bahwa x=d |

**Jawaban untuk “semua HA selesai?”: belum semuanya.** HA0, HA1, dan lingkup simbolik HA5 selesai. HA2 dan HA3 menghasilkan bukti statis kuat tetapi memiliki batas yang tercantum; HA4 diblokir oleh prasyarat HA2. Mengubah status itu menjadi TUNTAS tanpa bukti akan keliru.

## HA0 — ledger dan Actions

Dari baseline inklusif sampai HEAD audit 077941187650cb8e4b4920c48ac8012567ee5b97 terdapat **7 commit: 4 manusia dan 3 bot**. Rinciannya:

1. 14dccd2e1d2f92b1b919ad7f0686bf019c71dbf4 — manusia; reports/stage1_economy/GA0_GA5_FINAL_ADDENDUM_2026-11-07.md.
2. 58db32c696fe830b6558c6828529a3801be753e0 — manusia; 7 berkas: .github/workflows/ha2-ha3-static-audit.yml; reports/stage1_economy/HA1_CORRECTION_ADDENDUM_2026-11-07.md; reports/stage1_economy/HA1_HELPER_8001552C_00.tsv; reports/stage1_economy/HA1_HELPER_8001552C_01.tsv; reports/stage1_economy/HA1_NEGU_ROWS.tsv; tools/ghidra/EnsureTargetFunctions.java; tools/stage1/RunHA2HA3Static.py.
3. 55aab58da159dec71589ae04c3ecfd1f681256e0 — bot; 3 berkas DN1: reports/stage1_economy/DN1_GHIDRA_ACTIONS_RUN_SUMMARY_2026-11-05.txt; reports/stage1_economy/DN1_WHOLE_CENSUS_SUMMARY_2026-11-05.txt; reports/stage1_economy/DN1_WRITER_DESTINATION_AUDIT_2026-11-05.md.
4. 9509c103be662959909f443118499d25e511d3ae — manusia; reports/stage1_economy/ha0-run-42338608064/ACTIONS_RUN_SUMMARY.txt.
5. ccf5efff1a273227ef216be8c6c49f70ab4d84c7 — bot; 404 berkas output statis dalam reports/stage1_economy/ha2-ha3-static-run-42338608063/attempt-1/: HA1_HELPER_8001552C_00..01.tsv, HA1_NEGU_ROWS.tsv, tiga HA1_STORE_*_WINDOW.tsv; HA2_FUN_800154D4_00.tsv, HA2_FUN_8001552C_00..01.tsv, HA2_FUN_800F2A9C_00..25.tsv, decomp/reference, indirect-candidate, key-instruction, return-path, global-access, dan helper-table summary; HA3_FUN_800D15A8_00..256.tsv, HA3_FUN_800DC2E0_00..83.tsv, HA3_FUN_800FAAC8_00..10.tsv, index-origin, manager census, reader summary, tiga reader decomp, serta dua ekspor Ghidra; ditambah ACTIONS_RUN_SUMMARY.txt, ANALYSIS_FAILURE.txt, dan cleanup.txt.
6. b65ef33c4fc0f4d67e2258ebf77a528000a78241 — manusia; hanya tools/stage1/RunHA2HA3Static.py (memperbaiki KeyError, memperbaiki laporan return void, dan menambahkan validator).
7. 077941187650cb8e4b4920c48ac8012567ee5b97 — bot; 404 berkas output statis dalam reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/. Pola keluaran fungsi sama dengan run sebelumnya; tambahan penting adalah HA2_HA3_STATIC_SUMMARY.txt, HA_TSV_VALIDATION_SUMMARY.txt, dan status run sukses, tanpa ANALYSIS_FAILURE.txt.

Actions run yang source SHA-nya berada dalam rentang baseline:
- 42338608063: job ha2-ha3-static selesai, tetapi skrip analisis sendiri EXIT_CODE=1 akibat nama kolom yang salah. Ekspor Ghidra, py_compile, dan cleanup berhasil; run ini bukan hasil analisis final.
- 42338608064: job Ghidra statis selesai success, EXIT_CODE=0, TARGETS_MISSING_FROM_GHIDRA_EXPORT=0.
- 42339837743: job ha2-ha3-static selesai success, EXIT_CODE=0; py_compile, kedua ekspor Ghidra, analisis MIPS, cleanup input privat, dan commit teks/TSV berhasil.
- Scheduled monitor 42320736860 success, namun source SHA 6987a76e12b0adf86f8061d47dcc4078e79cda21 mendahului baseline. Monitor tidak menemukan adaptive-player run pada 50 run terbaru dan tidak mengunggah laporan. Dicatat sebagai konteks di luar ledger inklusif.

Saat audit ini ditutup: queued=0, in_progress=0. STATUS.md blob tetap ee7b9c226631c71cae1c9fb0270994ccf3e67c07; tidak ada perubahan pada Release naruto-checkpoint-39262213468.

## HA1 — koreksi offset, negu, dan register-fill

Offset Entry 1:
file_offset = 0x10BB000 + (PC - 0x800AD450).

- PC 0x800F7E64 → 0x01105A14.
- PC 0x800F7E68 → 0x01105A18.
- Dua baris negu $v0,$v0: 0x800F2E0C / 0x011009BC, serta 0x800F2E64 / 0x01100A14, bytes keduanya 23 10 02 00.
- Helper 0x8001552C dipisah 16+3 instruksi.
- Jendela store: F2CF8=6 instruksi; F2E38=14; F2E68=7.

Validasi otomatis run 42339837743: **389 TSV instruksi, 6.275 baris, INVALID_ROWS=0**. Formula EXE dan Entry 1 diterapkan; excerpt kontigu maksimum 16 instruksi. Ini menutup validasi HA1 yang belum ada pada addendum pertama.

## HA2 — helper, tabel, store, return, caller

FUN_800154D4 hanya 3 instruksi dan memuat nilai dari GP+0x118, yang didekompilasi sebagai DAT_8006D794. Karena isi runtime global itu tidak dapat dibuktikan dari keluaran statis yang ada:

- B = FUN_800154D4() = DAT_8006D794: **TIDAK TAHU**.
- Helper FUN_8001552C memakai table VA 0x80055CF4, stride 0x10, nilai u32 pada offset +0x8.
- H(x)=u32[0x80055CF4+16*x] jika u32(x)<B, selain itu 0.
- Tidak ada nilai tabel atau jumlah baris tabel yang diterbitkan karena bound tidak diketahui.

Tiga operasi store utama:
- 0x800F2CF8: u16(LO32(H(x1)*(G-2))).
- 0x800F2E38: u16(LO32((-H(x2))*(G-1-s16(Q)))).
- 0x800F2E68: u16(-H(x3)).
- G=u8(0x8013EA71), Q=u32(0x80139EFC), manager M=u32(0x8013EA74); slot adalah M+0x2EE+2*idx. x dibaca dari manager record +0x530; hubungan x=d tidak terbukti.
- FUN_800F2A9C bertipe C void; sembilan return; bukan sembilan nilai $v0. Satu epilog fisik jr $ra; tidak ada nilai return ABI untuk $v0 yang harus ditafsirkan.
- Satu direct caller tercatat: jal 0x800F2A9C pada 0x800F5F54 dari FUN_800F3658. Scan kandidat indirect caller tidak menghasilkan kandidat terkonfirmasi.

Maka HA2 tetap SEBAGIAN: bound dan tabel adalah gap substantif, bukan sekadar kekurangan format laporan.

## HA3 — census +0x2EE, reader paths, hipotesis

Census gabungan:
- 21 akses manager-backed terindeks pada run terbaru: 18 write dan 3 read.
- Census statis sebelumnya menambahkan dua write literal-zero yang tidak tercantum dalam daftar terindeks baru: 0x800B24C8 dan 0x800BEDA4.
- Gabungan = **23 akses: 20 write + 3 read**. Di antara 20 write, **12 menggunakan nilai register/non-literal-zero** dan 8 literal-zero. Dua write literal-zero tambahan punya manager-slot root terbukti, tetapi derivasi indeks per-site belum diurai tuntas.
- FUN_800D15A8, store 0x800D46F8, menghasilkan u16(-u16(tile+0x1A)) pada slot manager +0x2EE.

Tiga reader berbeda fungsi:
1. 0x800DCFE8 dalam FUN_800DC2E0: fungsi ini menangani alur pending/settlement melalui +0x4F4; state penyelesaian menambahkan nilai pending ke participant record +0x4, memanggil FUN_80014F10(owner, magnitude), lalu membersihkan +0x4F4. Ini membuktikan arus nilai tertunda ke field peserta dan pemanggilan lanjutan, tetapi bukan definisi semantik field sebagai uang.
2. 0x800F2E80 dalam FUN_800F2A9C: signed read menguji tanda nilai dan mengatur participant record +0x22 menjadi status 2 atau 5.
3. 0x800FAAEC dalam FUN_800FAAC8: zero-check pada slot +0x2EE bersama pemeriksaan field manager lain menjadi syarat timer/housekeeping.

Hipotesis H1 (pending transaction/settlement): didukung oleh store negatif berbasis tile+0x1A pada 0x800D46F8 dan alur +0x4F4 → participant+0x4 → FUN_80014F10 pada FUN_800DC2E0. Falsifier: trace runtime menunjukkan slot dan indeks yang sama tidak pernah berkorelasi dengan perubahan +0x4F4, participant +0x4, atau argumen owner/magnitude di FUN_80014F10.

Hipotesis H2 (juga dipakai sebagai status/control gate, bukan hanya nilai settlement): didukung oleh sign-to-status pada FUN_800F2A9C dan zero-gate untuk timer/housekeeping pada FUN_800FAAC8. Falsifier: runtime membuktikan kedua jalur tersebut selalu hanya mencerminkan settlement participant dan tidak pernah mengubah status, timer, atau kontrol secara independen.

HA3 SEBAGIAN K3: rantai reader statis dan ambang 12 nonzero write terpenuhi; dua derivasi indeks zero-writer dan semantik ekonomi akhir belum ditutup runtime.

## HA4 — CONTROL H6

Artifact aktif yang ditemukan pada run 39907655833 adalah naruto-storymode-adaptive-player-private, artifact ID 12482055310, 11.407.011 byte, belum expired saat pemeriksaan. ZIP mengandung adaptive-cycle-02-f180.sstate, 21.162.799 byte, SHA-256 705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35. Ini snapshot baru, bukan checkpoint adaptive-cycle-01-f180.sstate yang dipatok sebelumnya.

Run lama 42312284099 gagal pada unduh artifact lama; PCSX launches=0 dan watchpoints=0. **Tidak ada CONTROL launch baru dan tidak ada watchpoint yang dilakukan dalam audit ini.** Instruksi HA4 sebelumnya mensyaratkan HA2 lengkap dahulu; bound/table HA2 tetap TIDAK TAHU, sehingga syarat tersebut belum dipenuhi. Menjalankan CONTROL sekarang akan melanggar urutan prasyarat dan tidak menyelesaikan celah bound.

## HA5 — katalog prediksi dan falsifier

Dengan H(x), G, dan Q seperti di atas, tiga prediksi store diekspresikan pada bagian HA2. Untuk level-d yang belum dipetakan, model simbolik d=1..4 adalah:

| Model | d=1 | d=2 | d=3 | d=4 |
|---|---:|---:|---:|---:|
| Linear C*d | C | 2C | 3C | 4C |
| Eksponensial C*2^(d-1) | C | 2C | 4C | 8C |
| Akumulasi C*sum(2^k), k=0..d-1 | C | 3C | 7C | 15C |
| Lookup | L[1] | L[2] | L[3] | L[4] |

Falsifier/pengukuran pembeda yang dipersiapkan: pada satu kondisi runtime terkendali catat frame, PC, effective address, old/new value, register pada write 0x800F2CF8/0x800F2E38/0x800F2E68/0x800D46F8; sertakan nilai tile+0x20 sebagai u16 dan nibble ((u16>>8)&0xF), tile+0x1A, 0x80139EFC, 0x8013EA71, dan 0x8013EB0C; ikat indeks lookup x ke d dan cari konsumen terminal lebih dahulu. Katalog simbolik HA5 selesai; rumus numerik biaya tetap TIDAK TAHU.

## Ringkasan run dan berkas Actions

Run koreksi HA2–HA3:
- ID 42339837743; source SHA b65ef33c4fc0f4d67e2258ebf77a528000a78241; job ha2-ha3-static, job ID 128304848857; status SUCCESS; exit code 0.
- PY_COMPILE_EXIT_CODE=0, GHIDRA_ENTRY1_EXIT_CODE=0, GHIDRA_EXE_EXIT_CODE=0, PRIVATE_CLEANUP=PASS, tidak ada game/emulator, tidak ada binary privat dikomit.
- Validasi instruksi: 389 file TSV; 6.275 baris; 0 salah decode/offset; maksimal 16 instruksi kontigu per excerpt.

Raw permalinks (SHA penuh, tanpa query):
- Actions summary run koreksi: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/077941187650cb8e4b4920c48ac8012567ee5b97/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/ACTIONS_RUN_SUMMARY.txt
- Validasi TSV: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/077941187650cb8e4b4920c48ac8012567ee5b97/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA_TSV_VALIDATION_SUMMARY.txt
- Ringkasan HA2/HA3: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/077941187650cb8e4b4920c48ac8012567ee5b97/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA2_HA3_STATIC_SUMMARY.txt
- Helper bound/table: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/077941187650cb8e4b4920c48ac8012567ee5b97/reports/stage1_economy/ha2-ha3-static-run-42339837743/attempt-1/HA2_HELPER_TABLE_SUMMARY.txt
- Reader decompilations ada pada path HA3_READ_800DCFE8_IN_DC2E0.txt, HA3_READ_800F2E80_IN_F2A9C.txt, HA3_READ_800FAAEC_IN_FAAC8.txt di direktori output run yang sama.
- Addendum HA1: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/077941187650cb8e4b4920c48ac8012567ee5b97/reports/stage1_economy/HA1_CORRECTION_ADDENDUM_2026-11-07.md
- Skrip analisis yang telah diperbaiki: https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/077941187650cb8e4b4920c48ac8012567ee5b97/tools/stage1/RunHA2HA3Static.py

## TIDAK TAHU yang masih sah

1. Nilai runtime DAT_8006D794 / bound B dari FUN_800154D4.
2. Isi dan jumlah baris tabel u32 0x80055CF4+16*i karena B tidak diketahui.
3. Apakah indeks x dari manager +0x530 sama dengan beda level d.
4. Identitas semantik pasti field participant +0x4 dan apakah satu-satunya saldo ekonomi.
5. Derivasi indeks dua zero-writer 0x800B24C8 dan 0x800BEDA4 per-site.
6. Konfirmasi runtime untuk kedua hipotesis HA3 dan pembeda numerik model HA5.
7. CONTROL H6 belum diuji; tidak ada klaim runtime atau K4/K5 dari checkpoint artifact saja.

Tidak ada ROM/ISO/EXE/DATA.BIN/BIOS/savestate/RAM dump/video/frame/binary yang dikomit. STATUS.md dan Release naruto-checkpoint-39262213468 tidak diubah.
