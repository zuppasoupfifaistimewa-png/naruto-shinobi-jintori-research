# Status audit UC0–UC3 — 10 November 2026

Baseline repo `main`: `dc18ff4f375680b1f37e7ceca7f64405a4554230` (inclusive). The baseline audit for physical harness deletion remains `aa32fbcee97c8f49946a8e589010cfb9ef1a6928`. Repo HEAD matched the requested UC baseline before this report-only publication.

## Ringkasan status

| Tahap | Status | Tingkat bukti dan batas |
|---|---|---|
| UC0 | BELUM TUNTAS | QA0 lama K4 untuk skema lama saja; tidak mencakup variasi `instruction_pc` / `instruction_bytes` dan fallback label dari `file_offset` yang diminta sekarang. |
| UC1 | BELUM DIKERJAKAN PADA BASELINE UC | Pembacaan entry 0 `0x800558B0`, delapan pointer handler, seluruh kolom record, dan graph `jal/jalr` depth 3 belum terdapat pada artefak yang diverifikasi di sini. Target kredit/fee: TIDAK TAHU. |
| UC2 | BELUM TUNTAS UNTUK PROTOKOL UC | UB2 lama PASS K5 untuk protokol sebelumnya, tetapi breakpoint lama adalah EXEC `0x80011A28` dan EXEC `0x800B50AC`; bukan dua writer yang diminta. Sampel tiap 10 frame tanpa breakpoint dan batas delapan hit per jendela 100 frame juga belum dibuktikan. |
| UC3 | TUNTAS UNTUK DELTA BASELINE INI | Satu commit HUMAN, tiga file-event tanpa rename, satu Actions run baru dan halaman run tercatat. K4 untuk data GitHub yang diperiksa ulang. |

## Detail UC0

QA0 final lama (`run 42745502822`) mengaudit 4.039 TSV di cakupan Stage 1; 428 file cocok dengan header `image/pc/bytes`, 309.960 baris byte valid, 160.516 alamat unik, union maksimum 64 B, nol grup >64 B, nol konflik dan nol baris malformed. Namun, parser QA0 menerima hanya tiga header tersebut. Audit LA0 sebelumnya lebih sempit lagi: 4.029 file dipindai, 318 byte-eligible. Kedua hasil tersebut bukan audit lintas semua alias/header UC0. Karena itu UC0 tidak dinaikkan menjadi PASS. Tidak ada berkas lama yang dihapus atau dipangkas dalam publikasi ini.

## Detail UC1 dan caller yang sudah diketahui

Artefak UB1 lama menyokong konteks statis caller `0x80011A28`: caller menggunakan `MEM32[0x800558A8 + 28*a0 + 8]`, dan ringkasan UB1 mengaitkan load `a0` dengan `MEM32[0x8006D760]`. Data `UB1_TABLE_BASE_800558FC_WORDS.tsv` hanya membaca kandidat record di sekitar `0x800558FC`; ia bukan pembacaan entry-0 `0x800558B0` dan tidak membuktikan bahwa `0x800558FC` adalah base indeks nol. Penentuan handler dari entry 0–7 dan graph panggilan tetap TIDAK TAHU. Jangkauan ke `FUN_800D15A8`, `0x800D2520`, dan `0x800D46EC` belum dinilai.

Keterangan tentang penulis `a0` di `0x800116C8` dan `0x8001198C`, serta nilai runtime `a0=3` pada frame 1–63 setelah checkpoint, dipertahankan sebagai konteks/observasi yang diberikan untuk tahap UC; belum diklaim sebagai hasil pemeriksaan runtime baru dalam tahap ini.

## Detail UC2

UB2 run lama `42706850980` mencatat NO_INPUT x2 dan CIRCLE x2, masing-masing 900 frame; trace repetisi identik untuk kedua kondisi, dengan pembatas 32 hit per alamat breakpoint. Probe read-only dan tidak menghasilkan dump biner. Akan tetapi, alamat breakpoint-nya adalah EXEC `0x80011A28` dan EXEC `0x800B50AC`. Permintaan UC2 saat ini membutuhkan watchpoint tulis/exec pada dua writer `0x800116C8` dan `0x8001198C`, sampel `MEM32[0x8006D760]` setiap 10 frame pada sesi tanpa breakpoint, serta callsite dengan cap 8 hit per jendela 100 frame. Jadi status UC2 tetap belum tuntas untuk protokol yang diperbarui.

## Detail UC3

Commit inklusif baseline UC adalah `dc18ff4f375680b1f37e7ceca7f64405a4554230`, parent `10fb09a7228f301dbbf4214ffc3013652a14d823`, klasifikasi HUMAN. Diff dengan `--no-renames`: tiga baris file-event, semuanya modified.

Satu Actions run setelah baseline: `42751965600`, event `schedule`, job `monitor` ID `129617431295`, workflow dan job completed/success pada source SHA baseline. Log mengatakan tidak ada adaptive-player run yang terlihat di latest 50 Actions runs, dan menegaskan ini bukan keberhasilan atau penyelesaian Story Mode. Exit code proses tidak dicetak (TIDAK TAHU); upload artefak ringkasan tidak terjadi karena `monitoring-report.txt` tidak ditemukan.

## Batas publikasi

Audit ini bersifat dokumentasi/rekonsiliasi saja. Tidak ada ROM, EXE, DATA.BIN, BIOS, memory card, savestate, dump RAM, video atau biner lain yang dimasukkan. `STATUS.md` dan Release tidak diubah. Tidak ada emulator diluncurkan dan tidak ada Actions run baru dipicu oleh publikasi ledger ini. Kutipan byte tidak ditambahkan.
