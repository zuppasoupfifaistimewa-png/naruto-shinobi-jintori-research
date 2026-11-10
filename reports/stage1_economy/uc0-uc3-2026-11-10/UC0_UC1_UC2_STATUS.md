# Status audit UC0–UC3 — 10 November 2026

Baseline repo main: dc18ff4f375680b1f37e7ceca7f64405a4554230 (inclusive). Baseline audit for physical harness deletion remains aa32fbcee97c8f49946a8e589010cfb9ef1a6928. STATUS.md and Releases remain untouched.

## Ringkasan

| Tahap | Status | Bukti dan batas |
|---|---|---|
| UC0 | AUDIT SELESAI DENGAN BATAS | K4 untuk union byte atas 1.936 TSV yang memiliki alias kolom dikenali; 3.264 grup >64 B, 265 konflik, 9 baris malformed, 253 label belum terpetakan. 4.120 TSV terlacak; 2.184 TSV tidak memenuhi pasangan header yang dikenali. Semua grup dan sumber tersedia di artefak run 42755318255. |
| UC1 | PARSIAL | K4 untuk pembacaan delapan record × delapan word pada tabel EXE; empat target memiliki prolog yang cocok pada Entry 1. Empat lainnya tetap TIDAK TAHU sebagai pemetaan fungsi. Graph adalah kandidat statis linear-terbatas, bukan CFG tervalidasi; target kredit/fee belum terbukti. |
| UC2 | PARSIAL; K5 SEMPIT | Empat peluncuran 900 frame selesai. Untuk nilai global MEM32[0x8006D760] yang disampel tiap 10 frame, dua urutan per kondisi identik dan semua titik bernilai 3 (K5 terbatas pada titik sampel). Input CIRCLE readback 28/28 PASS setelah trim. Breakpoint caller/writer tidak terpasang karena instrumented=nil; tidak ada data PC/RA/a0 per hit. |
| UC3 | TUNTAS UNTUK DELTA HINGGA COMMIT REKONSILIASI | Tujuh commit dari baseline hingga commit rekonsiliasi ini, tiga Actions run, dan 58 file-event --no-renames tercatat. Commit publikasi ledger itu sendiri dikecualikan agar tidak self-referential. K4 untuk enumerasi GitHub. |

## UC0 — byte union lintas TSV

Run 42755318255 memindai seluruh 4.120 TSV terlacak di checkout sebelum hasil run tersebut ditambahkan. Sebanyak 1.936 file memiliki pasangan kolom pc atau instruction_pc dan bytes atau instruction_bytes; 1.469 file memakai alias/fallback label. Parser menghasilkan 746.115 baris-byte valid, 767.636 alamat byte unik, dan 71.440 grup kontigu.

Ada 3.264 grup lebih panjang dari 64 byte. Daftar lengkap setiap grup dan daftar sumber TSV-nya ada di UC0_OVER_64B_GROUPS.tsv; union semua grup ada di UC0_BYTE_UNION_GROUPS.tsv. Terdapat 265 konflik byte pada alamat/image yang sama, 9 baris malformed (termasuk baris ringkasan yang terbaca sebagai data), dan 253 label unresolved. Label unresolved dipisahkan per file; tidak digabung lintas file tanpa identitas image yang dapat dipertanggungjawabkan. Ini audit saja: tidak ada TSV historis yang dihapus, dipotong, atau ditulis ulang. Gerbang 64 B tetap berlaku bagi TSV baru.

## UC1 — tabel handler dan graph panggilan

Identitas input statis lolos pemeriksaan hash: EXE SHA-256 a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569; DATA.BIN SHA-256 69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822. Pemetaan EXE menggunakan file offset 0x800 + (PC - 0x80010000). Entry 0/1 DATA.BIN dipakai sebagai image slice statis; basis itu bukan pernyataan basis runtime.

Formula slot: 0x800558A8 + 28*entry + 8. Delapan word pointer pada slot +8:
- entry 0, slot 0x800558B0 → 0x800AD9A4 (tidak ada prolog yang terkonfirmasi; pemetaan fungsi TIDAK TAHU)
- entry 1, slot 0x800558CC → 0x800AD5F0 (TIDAK TAHU)
- entry 2, slot 0x800558E8 → 0x800AF748 (TIDAK TAHU)
- entry 3, slot 0x80055904 → 0x800B50AC (prolog cocok di Entry 1)
- entry 4, slot 0x80055920 → 0x800B50AC (prolog cocok di Entry 1)
- entry 5, slot 0x8005593C → 0x8011CE2C (prolog cocok di Entry 1)
- entry 6, slot 0x80055958 → 0x8011CE2C (prolog cocok di Entry 1)
- entry 7, slot 0x80055974 → 0x800ADF3C (TIDAK TAHU)

Seluruh kolom word +0x0 sampai +0x1C untuk setiap record dibaca. Graph menghasilkan 7.760 baris: 7.696 kandidat JAL, 46 JALR, dan 18 penanda batas fungsi. Graph hanya dapat dimulai dari entry 3–6 yang punya prolog terkonfirmasi; entry 0,1,2,7 tidak diberi pemetaan fungsi. Scan bersifat linear dan dibatasi sampai jr ra atau 0x1000 byte, tidak merekonstruksi CFG lengkap. Tidak ditemukan edge langsung dalam keluaran ke FUN_800D15A8, 0x800D2520, atau 0x800D46EC; untuk entry 3–6 statusnya tetap TIDAK TAHU_DYNAMIC_OR_UNBOUNDED karena JALR dinamis/pemindaian tidak tuntas. Untuk entry 0,1,2,7 status TIDAK TAHU_NO_HANDLER_MAPPING. Tidak ada kesimpulan bahwa kredit/fee tidak pernah dipanggil.

## UC2 — headless read-only

Checkpoint identik: 21.162.799 byte, SHA-256 705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35. Run 42755318255 menyelesaikan empat peluncuran masing-masing 900 frame; semua proses emulator exit 0, save-state load terkonfirmasi, hash memory-card sebelum/sesudah sama, dan cleanup aset privat lulus.

Nilai MEM32[0x8006D760] pada 90 titik frame 10..900 per peluncuran selalu 0x00000003. Dua urutan NO_INPUT identik dan dua urutan CIRCLE identik: K5 hanya untuk nilai global pada titik sampling ini. CIRCLE readback menghasilkan true saat tekan dan false saat lepas, 14 event per peluncuran × dua peluncuran = 28 event PASS setelah whitespace di-trim.

Namun dua log peluncuran trace mencatat instrumented=nil, sehingga cabang pemasangan breakpoint tidak berjalan. Karena itu nol hit pada 0x800116C8, 0x8001198C, dan 0x80011A28 tidak dapat ditafsirkan sebagai ketiadaan eksekusi. Nilai $a0 per-call, variasi $a0 pada hit, serta PC/RA/nilai writer tetap TIDAK TAHU. UC2_RECONCILIATION.txt menjelaskan parser false-negative input dan cacat flag trace. Kode parser dan pemasangan breakpoint diperbaiki dalam commit rekonsiliasi [skip ci], tanpa run tambahan.

## UC3 — ledger inkremental

Baseline inklusif dc18ff4f375680b1f37e7ceca7f64405a4554230, parent 10fb09a7228f301dbbf4214ffc3013652a14d823. Hingga commit rekonsiliasi run 7: 7 commit (5 HUMAN, 2 BOT), 58 file-event tanpa rename (50 added, 8 modified, 0 deleted), dan 3 Actions run:
- 42751965600: monitor terjadwal, completed/success; process exit code TIDAK TAHU (log tidak mencetak kode).
- 42755015135: run UC0–UC2 pertama, completed/failure, exit code 2.
- 42755318255: run UC0–UC2 koreksi, completed/failure, exit code 2; hasil statis dan sampel runtime tetap dipublikasikan.
Tidak ada klaim penyelesaian Story Mode. Commit yang memublikasikan ledger ini dikecualikan dari hitungan karena ledger tidak dapat menyertakan SHA dirinya sendiri; akan menjadi titik awal delta selanjutnya.

## Batas

Tidak ada ROM/EXE/DATA.BIN/BIOS/memory card/savestate/dump RAM/video/biner yang dikomit. STATUS.md dan Releases tidak berubah. Semua perubahan laporan/ledger memakai [skip ci]; tidak ada run baru setelah run 7.
