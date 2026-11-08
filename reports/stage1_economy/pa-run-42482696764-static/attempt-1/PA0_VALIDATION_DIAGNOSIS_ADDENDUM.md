# PA0 diagnosis addendum — run 42482696764

Baseline inklusif: 3f730c73dc628d02f360b7ac12961e6f3e4b1584
Static job: 128737896245
Source SHA: 5e03369540f34c45f2eea587be926924749939dd
Analyzer exit: 1
PY_COMPILE: 72/72 PASS
Harness self-test: PASS

## PA0 self-test

- Fixture kutipan kontigu 65 byte: DETECTED (ditolak).
- Fixture 64 byte: PASS.
- Delimiter TSV: panjang 1 karakter, tab; parse PASS.
- Literal delimiter lama `delimiter="\\\\t"`: ABSENT.

Self-test membuktikan harness dasar, bukan validasi kutipan historis atau byte ROM.

## Diagnosa offset/raw/decode

Tabel `PA0_FILE_OFFSET_RAW_DECODE.tsv` memuat 3.157 baris; semuanya diberi `OFFSET_OR_RAW_MISMATCH`, dengan 0 instruksi terdekode. Distribusi file: PA1_CALL_WINDOWS 51, PA2_GLOBAL_POINTER_SELECTOR_ACCESSES 2.907, PA2_V0_STORE_WINDOWS 48, PA2_SELECTOR_STORE_WRITERS 80, PA3_B24C8_WINDOWS 12, PA3_UNRESOLVED_JALR_WINDOWS 59. Seluruh baris adalah ENTRY1.

Penyebab yang dapat dibuktikan adalah indeks pemeriksaan pada validator, bukan formula file offset. Baris contoh PA1 memuat PC `0x800F5F14` dan file offset `0x01103AC4`. Formula ENTRY1 yang diminta menghasilkan `0x10BB000 + (0x800F5F14 - 0x800AD450) = 0x01103AC4`, cocok dengan TSV. Tetapi validator memakai `got=entry[off:off+len(raw)]` sementara `entry` adalah buffer ENTRY1 yang sudah diekstrak mulai offset lokal nol. `off` adalah offset absolut di DATA.BIN, sehingga slice berada di luar buffer. Indeks byte yang benar untuk membaca buffer ENTRY1 adalah `pc - ENTRY_BASE`; pemeriksaan kolom `file_offset` tetap harus membandingkan formula DATA.BIN absolut.

Dengan demikian, 3.157 kegagalan ini **tidak membuktikan** 3.157 baris raw salah. Validasi raw yang benar dan decode tetap **TIDAK TAHU / BELUM**, karena validator belum membandingkan bytes pada indeks buffer yang tepat.

## Diagnosa excerpt union

Audit lintas JA/KA/LA/MA/NA/OA/PA:
- UNIQUE_IMAGE_PC=20.956
- MAX_CONTIGUOUS_BYTES=124
- OVER_LIMIT_GROUPS=7
- CONFLICTS=0
- DELETED_ROWS=0
- STATUS=FAIL

Tujuh kelompok ENTRY1:
- 0x800B549C..0x800B5517 = 124 B
- 0x800D7784..0x800D77C7 = 68 B
- 0x800D7D0C..0x800D7D4F = 68 B
- 0x800E4800..0x800E4843 = 68 B
- 0x800F5D8C..0x800F5DCF = 68 B
- 0x800F5E7C..0x800F5EDF = 100 B
- 0x800F5F14..0x800F5F5B = 72 B

Empat kelompok lama yang memang diizinkan untuk dipisah masih ada; tiga kelompok 68 B tambahan membuat strip routine berhenti pada 0x800D7784..0x800D77C7 sebagai kelompok tidak terotorisasi. Tidak ada baris yang dihapus. Tidak boleh disebut PASS. Perlu audit asal baris untuk tiga kelompok baru dan penentuan pemotongan minimum sebelum pembersihan dilakukan.

## Status butir

- PA0: SEBAGIAN K2 — self-test dan py_compile lulus; offset/raw/decode serta excerpt union gagal/tidak sah.
- PA1: SEBAGIAN K2 — keluaran ada, tetapi semua klasifikasi $a2/$a3 TIDAK TAHU karena JAL sebelumnya dapat mengubah argumen; scene chain tidak menutup consumer seluruh jalur.
- PA2: SEBAGIAN K2 — census selector, M references dan 144*I pattern tersedia; $s0 effective address, M alias/loader, nilai v0 dan $v1 di GP+0x118 belum tertutup. 144*I tetap kandidat pola, bukan bukti indeks record aktual.
- PA3: SEBAGIAN K2 — target 0x800B24C8 reachable dari entry 0x800B1E88 pada CFG direct-only; 12 JALR chain masih tidak diketahui karena target register berasal dari data dinamis.
- PA4: job independen sukses; detail nilai dan perbandingan terbit di PA4_RUNTIME_SUMMARY.txt dan TSV pada direktori pa4.
- PA5: analisis simbolik terbit pada report PA5; H1/H2 dan formula biaya tetap BELUM K1.

## Legacy workflow path filters

108 YAML workflow lama dipindai pada baseline. Filter generik `**/*.py` yang relevan terdapat pada LA/MA/NA; file PA memakai suffix `.pytxt`, sehingga tidak cocok. Path filter eksplisit lain yang ditinjau tidak cocok dengan `.github/workflows/pa0-pa5.yml` atau `tools/pa/*.pytxt`. Run ledger setelah baseline untuk periode audit ini mencatat tiga run PA push; tidak ada run lama terjadwal atau legacy yang terpicu oleh setup PA.

Tidak ada workflow lama, STATUS.md, Release atau berkas biner diubah oleh analisis ini.
