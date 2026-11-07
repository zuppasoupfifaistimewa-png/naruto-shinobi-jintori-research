IA0-IA5 - audit statis helper, participant record, dan x
Baseline inklusif: b9bd69a5c59ca5103a2144deef3604a6b5f5c4a9
Source SHA: 60639dbac379c5eb201cd261fcee1cde12d6ea58
EXE SHA-256: a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569; Entry 1 SHA-256: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a
Tidak ada emulator/game, input kontrol, BIOS, savestate, atau runtime replay.

STATUS
IA0=TUNTAS (K4); 7 commit inklusif; 5 run semua event; py_compile 64/64.
IA1=BELUM (K4); 0 akses dari fungsi yang memuat slot manager; wallet setter otoritatif belum terbukti.
IA2=BELUM (K3); 0 writer/calon writer; x terjangkau=TIDAK TAHU (writer/value provenance not closed).
IA3=SEBAGIAN (K4); pointer counts={'EXE_F2A9C': 0, 'EXE_F3658': 0, 'ENTRY1_F2A9C': 0, 'ENTRY1_F3658': 0}.
IA4=TUNTAS (K4); peluncuran emulator/game=0.
IA5=SEBAGIAN (K3); prediksi dibatasi oleh x yang terbukti IA2; G/Q simbolik.

IA1 FUN_80014F10 DAN RECORD +4
Dekompilasi disimpan di IA1_FUN_80014F10_DECOMPILE.txt. Akses per-site ada di IA1_RECORD_PLUS4_CENSUS.tsv. RECORD_EA74_INDEX_STRIDE_0x90_CONFIRMED hanya diberikan jika ekspresi alamat membuktikan pointer EA74 ditambah satu indeks berkoefisien 0x90. CANDIDATE_NOT_PROVEN tetap kandidat, bukan akses peserta terkonfirmasi.
IA1_WALLET_TRACE.txt berisi JAL langsung dan alasan status setter.
TIDAK TAHU: apakah FUN_80014F10/callee mengubah saldo otoritatif; pemanggilan fungsi tidak membuktikan setter wallet.

IA2 MANAGER+0x530 (x)
IA2_X_WRITER_PROVENANCE.tsv berisi setiap store kandidat, asal base, dan asal nilai. Nilai literal/konstanta dapat dikenali; nilai load memori, argumen masuk, dan asal dinamis tetap TIDAK TAHU sampai provenance tertutup.
Himpunan x: TIDAK TAHU (writer/value provenance not closed). Himpunan lengkap tidak diklaim apabila writer dinamis/calon base unresolved atau store tanpa reload global manager terlewat.
Dua hipotesis K1:
Hx1 - x terkait selisih level d. Dukungan: (1) x menjadi indeks H pada jalur F2A9C; (2) jalur terpisah DC2E0 meneruskan delta participant-record ke FUN_80014F10, sehingga mekanisme tetangga memang memproses delta. Falsifier: satu writer manager+0x530 terbukti memasok ID efek/item atau nilai non-delta.
Hx2 - x adalah ID efek/item/aksi. Dukungan: (1) H adalah lookup heterogen signed; (2) x adalah field manager terpisah dan tidak dihitung di F2A9C, sehingga selector eksternal masih mungkin. Falsifier: semua writer manager+0x530 yang terjangkau terbukti menyalin tepat selisih level d dan tidak ada writer selector lain.
Keduanya dugaan K1; tidak ada angka observasi eksternal, fitting, atau komparasi.

IA3 POINTER LITERAL DAN ZERO-WRITER
IA3_POINTER_WORD_SCAN.tsv berisi semua byte-word 0x800F2A9C/0x800F3658 di EXE dan Entry 1 termasuk unaligned. PC/file offset memakai formula masing-masing image. IA3_ZERO_WRITER_INDICES.tsv menurunkan basis/indeks untuk 0x800B24C8 dan 0x800BEDA4; tiap window per-site maksimum 16 instruksi/64 byte.

IA5 PREDIKSI SIMBOLIK
Hanya x yang terbukti oleh IA2 yang dipakai untuk lookup H. Store:
F2CF8 = low16(H(x)*(G-2))
F2E38 = low16(-H(x)*(G-1-Q))
F2E68 = low16(-H(x))
Jika domain x tidak tertutup, output mempertahankan H(x) dan rumus simbolik; x tidak disamakan dengan d.

TIDAK TAHU TERSISA
- Setter wallet otoritatif FUN_80014F10/callee dan kepastian record+4 sebagai saldo permanen.
- Akses +4 dari pointer yang diwariskan caller/alias tanpa reload slot global dalam fungsi yang sama.
- Writer +0x530 melalui pointer alias/caller, nilai tabel dinamis, dan domain x lengkap.
- Apakah x sama dengan d atau ID efek/item; kedua hipotesis K1.
- Apakah word pointer di scan adalah instruksi call, data tabel, atau literal tak dieksekusi; scan byte tidak membuktikan dispatch.
- Semantik transaksi runtime berada di luar tahap statis ini.
