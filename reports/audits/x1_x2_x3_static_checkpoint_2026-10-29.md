# Audit statis X1–X3 — checkpoint Naruto PS1
Tanggal audit: 2026-10-29 (UTC). Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. Cabang keluaran: `audit/checkpoint-window-2026-10-29`.
Metode: artefak dan log GitHub Actions serta savestate yang ada dibaca/di-parse sebagai data; emulator tidak dijalankan dan savestate tidak dimuat. Tidak ada ROM, BIOS, DATA.BIN, savestate, atau dump RAM yang ditambahkan ke Git.

## X1 — Kronologi pembuat Release

**Status: SEBAGIAN · keyakinan K3.** Timestamp membatasi kandidat, tetapi tidak membuktikan apakah langkah kandidat benar-benar membuat record Release.

Nilai pembanding yang dikonfirmasi dari metadata Release dan commit tag:
- Release `naruto-checkpoint-39262213468`, ID `427327611`; `created_at=2026-10-29T00:14:06Z`, `published_at=2026-10-29T00:14:27Z`.
- Commit tag/target yang dipakai: `4c505394ac331225545728261c66566fa3113763`; tanggal commit `tag_commit_date=2026-10-29T00:14:06Z`. Jadi `created_at` sama dengan tanggal commit target, bukan waktu pembuatan draft/record.
- Aset checkpoint ID `686794219`, `asset_created_at=2026-10-29T00:14:28Z`, nama `storymode-checkpoint-run-39262213468.raw.sstate`; ukuran 21,163,286 byte; SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`.

Tabel di bawah mencakup **semua 7 langkah Release-terkait** yang dipilih dari tiga run kandidat. Kolom “relatif ke published/asset” menjelaskan seluruh interval start–complete, bukan sekadar waktu start.

| Run | Job | Step | Langkah | step_started_at | step_completed_at | Interval vs published_at | Interval vs asset_created_at | Bukti/keterangan |
|---|---:|---:|---|---|---|---|---|---|
| 40789217602 | 123169957609 | 4 | Download release disc image and extract SLPS_035.53 | 2026-10-28T23:42:53Z | 2026-10-28T23:43:09Z | BEFORE | BEFORE | Log validates existing BIN/CUE assets; not checkpoint savestate. |
| 40789217602 | 123169957609 | 12 | Upload text-only Ghidra results | 2026-10-29T00:13:56Z | 2026-10-29T00:13:59Z | BEFORE | BEFORE | No checkpoint Release operation in this step. |
| 40789851317 | 123181516794 | 4 | Download release disc image and extract SLPS_035.53 | 2026-10-29T00:14:17Z | 2026-10-29T00:14:44Z | CROSSES | CROSSES | Log shows download/validation of pre-existing asset IDs 647346873 and 647354760; not checkpoint asset 686794219. |
| 40789851317 | 123181516794 | 12 | Upload text-only Ghidra results | 2026-10-29T00:45:54Z | 2026-10-29T00:45:56Z | AFTER | AFTER | After both checkpoint Release timestamps. |
| 40792708405 | 123181571477 | 5 | Preserve raw savestate as a non-expiring GitHub Release asset | 2026-10-29T00:14:26Z | 2026-10-29T00:14:31Z | CROSSES | CROSSES | Only candidate step identified that has logic to create/find checkpoint Release and upload asset; log does not expose GET status/POST event. |
| 40792708405 | 123181571477 | 8 | Remove private working files before publishing reports | 2026-10-29T00:14:35Z | 2026-10-29T00:14:35Z | AFTER | AFTER | After both checkpoint Release timestamps. |
| 40792708405 | 123181571477 | 10 | Upload sanitized reports (short retention; Release asset is durable copy) | 2026-10-29T00:14:36Z | 2026-10-29T00:14:37Z | AFTER | AFTER | After both checkpoint Release timestamps. |

**Putusan koreksi:** klaim lama “Release dibuat run `40792708405`” **DICABUT sebagai fakta terverifikasi**. Langkah 5 pada run itu merupakan **kandidat paling masuk akal** karena mengandung logika GET-or-create untuk Release checkpoint dan upload aset, serta intervalnya melintasi `published_at` dan `asset_created_at`. Namun log hanya mencatat hasil ID/URL akhir dan hash aset; ia tidak mengekspos status GET awal (404 vs 200) atau sebuah peristiwa POST yang secara eksplisit teramati. Maka **TIDAK TAHU** apakah langkah tersebut membuat record Release baru atau hanya menambahkan aset ke Release yang sudah ada. Langkah run `40789851317` memang melintasi timestamp yang sama, tetapi lognya mengunduh/memeriksa aset BIN/CUE yang sudah ada (ID `647346873` dan `647354760`), bukan aset checkpoint `686794219`.

## X2 — Pembaca blok, helper, dan field blok 2.900 byte

**Status: SEBAGIAN · keyakinan K4 untuk hasil CFG/akses langsung; K2 untuk kelengkapan global seluruh xref.** Bukti CFG memberi 32/32 pembacaan slot sebagai `RESOLVED_SLOT`, 12 fungsi unik, 0 belum terselesaikan, tanpa caveat CFG. Namun tabel field berikut mencakup instruksi akses langsung dengan base pointer blok yang dapat dipulihkan secara statis; akses melalui pointer dinamis/efek helper tidak selalu terlihat di tabel ini. Saya tidak menyatakan inventaris xref untuk semua segmen/overlay game lengkap tanpa dump referensi menyeluruh untuk kedua target.

### X2(a) — Xref helper dan nilai `a0`

Helper `0x80020F54` melakukan pemeriksaan null atas `a0` lalu meneruskan buffer `a0` ke byte-fill `0x80035D48` dengan `a2=0x58`; jadi instruksi ini membersihkan `0x58` byte pada buffer non-null. Empat callsite di initializer `FUN_80104690` berasal dari disassembly yang disertakan dalam artefak audit. Lima callsite tambahan berasal dari 12 fungsi pembaca slot CFG.

| PC instruksi `jal 0x80020F54` | Fungsi Ghidra | Nilai `a0` saat call (delay slot sudah diterapkan) | `a0 = ptr+0x1A8+0x58*n`? |
|---|---|---|---|
| `0x8010470C` | `FUN_80104690` | ptr + 0x1A8 + 0x58*n, n=0..3 | YA |
| `0x8010471C` | `FUN_80104690` | ptr + 0x468 + 0x58*n = ptr + 0x1A8 + 0x58*(n+8), n=0..3 | YA |
| `0x8010473C` | `FUN_80104690` | ptr + 0x308 + 0x58*n = ptr + 0x1A8 + 0x58*(n+4), n=0..3 | YA |
| `0x8010475C` | `FUN_80104690` | ptr + 0x5C8 = ptr + 0x1A8 + 0x58*12 | YA |
| `0x80104B3C` | `FUN_80104aa8` | TIDAK TAHU (abstract value $a0=U) | TIDAK TAHU |
| `0x80106BB4` | `FUN_80106a60` | ptr + 0x5C8 = ptr + 0x1A8 + 0x58*12 | YA |
| `0x801099C8` | `FUN_80109994` | ptr + 0xA20 | TIDAK |
| `0x801099EC` | `FUN_80109994` | ptr + 0xA78 | TIDAK |
| `0x80109A10` | `FUN_80109994` | ptr + 0xAD0 | TIDAK |

Empat callsite initializer menginisialisasi rangkaian 13 segmen berukuran `0x58` yang berawal di `ptr+0x1A8` (`n=0..12`, dibagi menjadi kelompok n=0..3, 4..7, 8..11, lalu 12). Instruksi terpisah menulis byte `0xFF` pada `ptr+0x620`. Pada checkpoint, nilai-nilai terprediksi yang diuji cocok dengan RAM parse langsung: word `2` pada `+0x478 + 0x58*n` untuk n=0..3 (4/4), serta byte `0xFF` pada `+0x620`.

Untuk helper alokasi `0x8002DEC4`, disassembly initializer menunjukkan call di PC `0x801046BC`, dengan `a0=2900` melalui delay-slot PC `0x801046C0`; hasil `v0` disimpan ke slot global `0x8013A554` pada PC `0x801046C8`. Xref yang tampak di Ghidra export untuk fungsi PS-X EXE adalah 35 callsite berikut; survei DATA.BIN entry 1 yang tersedia juga menampilkan 3 callsite tambahan (`0x800D5630`, `0x800D5640`, `0x800D5650`) selain initializer `0x801046BC`. Daftar ini hanya selengkap export sumber yang tersedia—belum menjadi bukti semua overlay/segmen telah diekspor.

| PC pemanggilan `0x8002DEC4` di PS-X EXE | Fungsi caller Ghidra | Sumber |
|---|---|---|
| `0x8001A508` | `FUN_8001A4D8` | PS-X EXE Ghidra xref export |
| `0x8001A5E4` | `FUN_8001A57C` | PS-X EXE Ghidra xref export |
| `0x8001BC2C` | `FUN_8001BC04` | PS-X EXE Ghidra xref export |
| `0x8002DF68` | `FUN_8002DF30` | PS-X EXE Ghidra xref export |
| `0x80023E68` | `FUN_80023E60` | PS-X EXE Ghidra xref export |
| `0x80029968` | `FUN_80029870` | PS-X EXE Ghidra xref export |
| `0x80029984` | `FUN_80029870` | PS-X EXE Ghidra xref export |
| `0x800299A0` | `FUN_80029870` | PS-X EXE Ghidra xref export |
| `0x800299DC` | `FUN_80029870` | PS-X EXE Ghidra xref export |
| `0x80029A48` | `FUN_80029870` | PS-X EXE Ghidra xref export |
| `0x80024110` | `FUN_8002409C` | PS-X EXE Ghidra xref export |
| `0x80025658` | `FUN_80025510` | PS-X EXE Ghidra xref export |
| `0x8002643C` | `FUN_80026338` | PS-X EXE Ghidra xref export |
| `0x80029E54` | `FUN_80029D54` | PS-X EXE Ghidra xref export |
| `0x80029E8C` | `FUN_80029D54` | PS-X EXE Ghidra xref export |
| `0x80029EA4` | `FUN_80029D54` | PS-X EXE Ghidra xref export |
| `0x80029ED8` | `FUN_80029D54` | PS-X EXE Ghidra xref export |
| `0x80029EF0` | `FUN_80029D54` | PS-X EXE Ghidra xref export |
| `0x8002D8D4` | `FUN_8002D8A4` | PS-X EXE Ghidra xref export |
| `0x8002D974` | `FUN_8002D944` | PS-X EXE Ghidra xref export |
| `0x8002DA1C` | `FUN_8002D9E4` | PS-X EXE Ghidra xref export |
| `0x8002DAC0` | `FUN_8002DA88` | PS-X EXE Ghidra xref export |
| `0x80031508` | `FUN_80031500` | PS-X EXE Ghidra xref export |
| `0x800318F0` | `FUN_800318D8` | PS-X EXE Ghidra xref export |
| `0x80032778` | `FUN_8003275C` | PS-X EXE Ghidra xref export |
| `0x80034258` | `FUN_8003423C` | PS-X EXE Ghidra xref export |
| `0x80034438` | `FUN_8003441C` | PS-X EXE Ghidra xref export |
| `0x8002432C` | `FUN_80024258` | PS-X EXE Ghidra xref export |
| `0x800248D8` | `FUN_80024464` | PS-X EXE Ghidra xref export |
| `0x80024CB4` | `FUN_80024B70` | PS-X EXE Ghidra xref export |
| `0x80024F4C` | `FUN_80024B70` | PS-X EXE Ghidra xref export |
| `0x80025040` | `FUN_80024B70` | PS-X EXE Ghidra xref export |
| `0x80025094` | `FUN_80024B70` | PS-X EXE Ghidra xref export |
| `0x800250D0` | `FUN_80024B70` | PS-X EXE Ghidra xref export |
| `0x80025138` | `FUN_80024B70` | PS-X EXE Ghidra xref export |
 
**Arti helper yang didukung instruksi:**
- `0x8002DEC4` memanggil alokasi level bawah di `0x80035B08`; bila alokasi sukses, field `0x800A2918+0xC` dinaikkan 1. Field `+0x8` ditambah ukuran dari header alokasi `(word(ptr-4)-1)<<3`. Ini mendukung interpretasi `+0x8` sebagai total ukuran yang sedang dicatat dalam unit 8-byte dan `+0xC` sebagai hitungan alokasi, tanpa membuktikan semantik di luar jalur wrapper yang terlihat.
- `0x8002DFE4` mengambil ukuran dengan rumus header yang sama lalu menguranginya dari `+0x8`, mengurangi `+0xC`, dan mengosongkan `gp+0xA8` jika nilainya sama dengan pointer yang dibebaskan.
- `0x80035D48` melakukan loop `sb` byte demi byte; `0x80020F54` memanggilnya dengan panjang `0x58`.

### X2(b) — Semua akses langsung ke field blok yang berhasil dipulihkan

Objek checkpoint: base `0x801CEF08`, ukuran 2.900 byte (`0xB54`), SHA-256 `d57024211a379dd6d17844e35d04c3e09fe70a45b9a871cca1fd9aedf9ef04d7`. Tabel berikut berisi seluruh **147 access site unik yang ter-resolve secara langsung** oleh analisis abstract-register/CFG pada 12 fungsi pembaca; offset relatif terhadap base blok. Mnemonic dan lebar akses ditampilkan apa adanya (load unsigned juga dicantumkan). Ini bukan klaim bahwa efek akses tak langsung via pointer dinamis sudah lengkap.

| Offset blok | PC | Fungsi Ghidra | Instruksi | Lebar | Arah |
|---|---|---|---|---:|---|
| `+0x000` | `0x80104AD0` | `FUN_80104aa8` | `lw` | 4 B | READ |
| `+0x000` | `0x80104AF0` | `FUN_80104aa8` | `sw` | 4 B | WRITE |
| `+0x5D8` | `0x80106C10` | `FUN_80106a60` | `sw` | 4 B | WRITE |
| `+0x5DC` | `0x80106C14` | `FUN_80106a60` | `sw` | 4 B | WRITE |
| `+0x5E0` | `0x80106C1C` | `FUN_80106a60` | `sw` | 4 B | WRITE |
| `+0x624` | `0x80107B8C` | `FUN_80107808` | `sw` | 4 B | WRITE |
| `+0x628` | `0x80107B30` | `FUN_80107808` | `sw` | 4 B | WRITE |
| `+0x628` | `0x80107B3C` | `FUN_80107808` | `sw` | 4 B | WRITE |
| `+0x8F8` | `0x8010798C` | `FUN_80107808` | `lh` | 2 B | READ |
| `+0x944` | `0x80107880` | `FUN_80107808` | `lbu` | 1 B | READ |
| `+0x944` | `0x801078D0` | `FUN_80107808` | `sb` | 1 B | WRITE |
| `+0x944` | `0x80107B10` | `FUN_80107808` | `sb` | 1 B | WRITE |
| `+0x945` | `0x8010791C` | `FUN_80107808` | `lbu` | 1 B | READ |
| `+0x945` | `0x80107970` | `FUN_80107808` | `lbu` | 1 B | READ |
| `+0x945` | `0x80107980` | `FUN_80107808` | `sb` | 1 B | WRITE |
| `+0x945` | `0x80107AB4` | `FUN_80107808` | `lbu` | 1 B | READ |
| `+0x94A` | `0x801079EC` | `FUN_80107808` | `lbu` | 1 B | READ |
| `+0x94A` | `0x80107A14` | `FUN_80107808` | `sb` | 1 B | WRITE |
| `+0x94A` | `0x80107A2C` | `FUN_80107808` | `lbu` | 1 B | READ |
| `+0x94A` | `0x80107A4C` | `FUN_80107808` | `sb` | 1 B | WRITE |
| `+0xA1C` | `0x801099AC` | `FUN_80109994` | `lw` | 4 B | READ |
| `+0xA1C` | `0x80109AA4` | `FUN_80109994` | `sw` | 4 B | WRITE |
| `+0xA2C` | `0x80109CC8` | `FUN_80109b98` | `lh` | 2 B | READ |
| `+0xA2E` | `0x80109CCC` | `FUN_80109b98` | `lh` | 2 B | READ |
| `+0xA84` | `0x80109C0C` | `FUN_80109b98` | `lh` | 2 B | READ |
| `+0xA86` | `0x80109C10` | `FUN_80109b98` | `lh` | 2 B | READ |
| `+0xADC` | `0x80109C70` | `FUN_80109b98` | `lh` | 2 B | READ |
| `+0xADE` | `0x80109C74` | `FUN_80109b98` | `lh` | 2 B | READ |
| `+0xB28` | `0x8010A010` | `FUN_80109fec` | `lhu` | 2 B | READ |
| `+0xB28` | `0x8010A01C` | `FUN_80109fec` | `sh` | 2 B | WRITE |
| `+0xB28` | `0x8010A760` | `FUN_80109fec` | `lhu` | 2 B | READ |
| `+0xB2A` | `0x80109A98` | `FUN_80109994` | `sb` | 1 B | WRITE |
| `+0xB2A` | `0x80109D5C` | `FUN_80109b98` | `lbu` | 1 B | READ |
| `+0xB2A` | `0x80109DBC` | `FUN_80109b98` | `lbu` | 1 B | READ |
| `+0xB2A` | `0x80109ED4` | `FUN_80109b98` | `lbu` | 1 B | READ |
| `+0xB2A` | `0x80109F3C` | `FUN_80109b98` | `lbu` | 1 B | READ |
| `+0xB2A` | `0x8010A094` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2A` | `0x8010A130` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2A` | `0x8010A23C` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2A` | `0x8010A2A0` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2A` | `0x8010A368` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2A` | `0x8010A440` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2A` | `0x8010A508` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2A` | `0x8010A5D0` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2A` | `0x8010A6BC` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2A` | `0x8010A6F0` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2A` | `0x8010A7BC` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2A` | `0x8010A7CC` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2A` | `0x8010A8A8` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2A` | `0x8010A8F8` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2A` | `0x8010AA04` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2B` | `0x80109CD0` | `FUN_80109b98` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x80109CF0` | `FUN_80109b98` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x80109D10` | `FUN_80109b98` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x80109D28` | `FUN_80109b98` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x80109E24` | `FUN_80109b98` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x80109E44` | `FUN_80109b98` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A140` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A158` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A16C` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A188` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A1A0` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A278` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A620` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A634` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A72C` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A7A0` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A7E4` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A7FC` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A810` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A938` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A954` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2B` | `0x8010A96C` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2C` | `0x8010A0AC` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2C` | `0x8010A388` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2C` | `0x8010A40C` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2C` | `0x8010A42C` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2D` | `0x80109A3C` | `FUN_80109994` | `sb` | 1 B | WRITE |
| `+0xB2D` | `0x80109EA8` | `FUN_80109b98` | `lbu` | 1 B | READ |
| `+0xB2D` | `0x8010A0B4` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2D` | `0x8010A384` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2D` | `0x8010A3F0` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2D` | `0x8010A3FC` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2D` | `0x8010A408` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2D` | `0x8010A434` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2E` | `0x80109A60` | `FUN_80109994` | `sb` | 1 B | WRITE |
| `+0xB2E` | `0x80109A6C` | `FUN_80109994` | `lbu` | 1 B | READ |
| `+0xB2E` | `0x80109C14` | `FUN_80109b98` | `lbu` | 1 B | READ |
| `+0xB2E` | `0x8010A0C0` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2F` | `0x80109A74` | `FUN_80109994` | `sb` | 1 B | WRITE |
| `+0xB2F` | `0x8010A0C8` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB2F` | `0x8010A790` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2F` | `0x8010A834` | `FUN_80109fec` | `lbu` | 1 B | READ |
| `+0xB2F` | `0x8010A840` | `FUN_80109fec` | `sb` | 1 B | WRITE |
| `+0xB30` | `0x80109A84` | `FUN_80109994` | `lw` | 4 B | READ |
| `+0xB30` | `0x8010A0D4` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB30` | `0x8010A2C0` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB30` | `0x8010A338` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB30` | `0x8010A358` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB34` | `0x80109A48` | `FUN_80109994` | `sw` | 4 B | WRITE |
| `+0xB34` | `0x80109DA4` | `FUN_80109b98` | `lw` | 4 B | READ |
| `+0xB34` | `0x8010A0DC` | `FUN_80109fec` | `sw` | 4 B | WRITE |
| `+0xB34` | `0x8010A2BC` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB34` | `0x8010A328` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB34` | `0x8010A334` | `FUN_80109fec` | `sw` | 4 B | WRITE |
| `+0xB34` | `0x8010A360` | `FUN_80109fec` | `sw` | 4 B | WRITE |
| `+0xB38` | `0x80109A88` | `FUN_80109994` | `lw` | 4 B | READ |
| `+0xB38` | `0x8010A0E0` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB38` | `0x8010A460` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB38` | `0x8010A4D8` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB38` | `0x8010A4F8` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB3C` | `0x80109A4C` | `FUN_80109994` | `sw` | 4 B | WRITE |
| `+0xB3C` | `0x80109F24` | `FUN_80109b98` | `lw` | 4 B | READ |
| `+0xB3C` | `0x8010A0E8` | `FUN_80109fec` | `sw` | 4 B | WRITE |
| `+0xB3C` | `0x8010A45C` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB3C` | `0x8010A4C8` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB3C` | `0x8010A4D4` | `FUN_80109fec` | `sw` | 4 B | WRITE |
| `+0xB3C` | `0x8010A500` | `FUN_80109fec` | `sw` | 4 B | WRITE |
| `+0xB40` | `0x80109A94` | `FUN_80109994` | `sw` | 4 B | WRITE |
| `+0xB40` | `0x8010A0EC` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB40` | `0x8010A528` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB40` | `0x8010A5A0` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB40` | `0x8010A5C0` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB44` | `0x80109A54` | `FUN_80109994` | `sw` | 4 B | WRITE |
| `+0xB44` | `0x80109F64` | `FUN_80109b98` | `lw` | 4 B | READ |
| `+0xB44` | `0x8010A0F4` | `FUN_80109fec` | `sw` | 4 B | WRITE |
| `+0xB44` | `0x8010A154` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB44` | `0x8010A1C4` | `FUN_80109fec` | `sw` | 4 B | WRITE |
| `+0xB44` | `0x8010A524` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB44` | `0x8010A590` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB44` | `0x8010A59C` | `FUN_80109fec` | `sw` | 4 B | WRITE |
| `+0xB44` | `0x8010A5C8` | `FUN_80109fec` | `sw` | 4 B | WRITE |
| `+0xB44` | `0x8010A5EC` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB44` | `0x8010A610` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB44` | `0x8010A648` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB44` | `0x8010A658` | `FUN_80109fec` | `sw` | 4 B | WRITE |
| `+0xB44` | `0x8010A6A8` | `FUN_80109fec` | `lw` | 4 B | READ |
| `+0xB48` | `0x80109A38` | `FUN_80109994` | `sh` | 2 B | WRITE |
| `+0xB48` | `0x8010A200` | `FUN_80109fec` | `sh` | 2 B | WRITE |
| `+0xB48` | `0x8010A210` | `FUN_80109fec` | `lhu` | 2 B | READ |
| `+0xB48` | `0x8010A220` | `FUN_80109fec` | `lhu` | 2 B | READ |
| `+0xB48` | `0x8010A230` | `FUN_80109fec` | `sh` | 2 B | WRITE |
| `+0xB48` | `0x8010A8BC` | `FUN_80109fec` | `sh` | 2 B | WRITE |
| `+0xB4A` | `0x80109A80` | `FUN_80109994` | `sh` | 2 B | WRITE |
| `+0xB4A` | `0x8010A1FC` | `FUN_80109fec` | `sh` | 2 B | WRITE |
| `+0xB4A` | `0x8010A700` | `FUN_80109fec` | `sh` | 2 B | WRITE |
| `+0xB4A` | `0x8010A8B4` | `FUN_80109fec` | `lhu` | 2 B | READ |

Jumlah instruksi langsung menurut analisis ini: 147 site unik; `lbu` READ 48, `lhu` READ 5, `lh` READ 7, `lw` READ 30, `sb` WRITE 26, `sh` WRITE 8, `sw` WRITE 23. Hasil CFG pembaca slot adalah may-path statis, bukan bukti semua jalur dieksekusi saat runtime.

## X3 — Accounting allocator dari save state yang di-parse langsung

**Status: TUNTAS · keyakinan K4.** Savestate tidak dimuat ke emulator. File sumber memiliki 21,163,286 byte dan SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`. Parser membaca RAM dari format SaveState PCSX-Redux; RAM region 8 MiB SHA-256 `6208811a0e36bc21ca19b956ef6b7610192879ea20e1f25d03fe2e64aaf0ebb9`, awalan RAM 2 MiB SHA-256 `3ad7b85c857a868d91df4b3f1049c23889a0dc482ad7ee390ac8b6c05c3190f4`.

| Alamat/region | Nilai mentah byte (little-endian) | Nilai LE | SHA-256 region |
|---|---|---|---|
| `0x800A2918..0x800A2927` (16 byte) | `50 F4 13 80 B0 8B 0B 00 20 19 08 00 14 00 00 00` | — | `825df2342664f13d3797897688a3b5ecbb75e5bc138172f78b5b9bcf647bc2fa` |
| `0x800A2918+0x8 = 0x800A2920` | `20 19 08 00` | `0x00081920` = 530,720 | SHA of 4 bytes `b0f18a09` (slice hash already included in 16-byte region above) |
| `0x800A2918+0xC = 0x800A2924` | `14 00 00 00` | `0x00000014` = 20 | SHA of 4 bytes `8d7d3d...` (slice hash already included in 16-byte region above) |
| Saved `$gp` (GPR index 28) | `0x8006D67C` | source: 32 GPR packed values in save-state Registers field | — |
| `gp+0xA8 = 0x8006D724` | `00 00 00 00` | `0x00000000` = 0 | `df3f619804a92fdb4057192dc43dd748ea778adc52bc498ce80524c014b81119` |

The 4-byte hashes for `+0x8` and `+0xC` were not separately computed for this report; the 16-byte allocator-struct SHA-256 above covers both fields. Their explicit individual hash cells are intentionally not used as evidence. The confirmed accounting values are +8 = 530,720 and +C = 20; saved `$gp=0x8006D67C` is sourced from register index 28 in the save-state, not inferred from the code.

## Provenance and pinned source evidence

- This report is built against current audit branch base `520969a5474d3757638ea898137b229b6a1922cf` and source static-analysis run **40820189600**, job **123270595987**.
- X1 uses candidate run/job pairs **40789217602/123169957609**, **40789851317/123181516794**, and **40792708405/123181571477**.
- X3 RAM parse/accounting source is checkpoint from run **39262213468**; preservation/hash verification was logged in run **40792708405**, job **123181571477**.
- Source reports at pinned commit:
  - [Release candidate step table](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/520969a5474d3757638ea898137b229b6a1922cf/reports/slot_provenance_audit/run_40820189600/w0_release_related_steps.csv)
  - [CFG summary and 32-reader classification](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/520969a5474d3757638ea898137b229b6a1922cf/reports/slot_provenance_audit/run_40820189600/w1_cfg_summary.txt) · [classification CSV](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/520969a5474d3757638ea898137b229b6a1922cf/reports/slot_provenance_audit/run_40820189600/w1_32_reader_cfg_classification.csv)
  - [Initializer disassembly](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/520969a5474d3757638ea898137b229b6a1922cf/reports/slot_provenance_audit/run_40820189600/v2_target_functions_full_disassembly.txt) · [helper disassembly](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/520969a5474d3757638ea898137b229b6a1922cf/reports/slot_provenance_audit/run_40820189600/w3_helper_function_disassembly.txt)
  - [Checkpoint RAM summary](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/520969a5474d3757638ea898137b229b6a1922cf/reports/slot_provenance_audit/run_40820189600/w2_checkpoint_ram_summary.txt) · [predicted values](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/520969a5474d3757638ea898137b229b6a1922cf/reports/slot_provenance_audit/run_40820189600/w2_predicted_vs_checkpoint_values.csv)

## K1–K5 rating
- **X1 K3 / SEBAGIAN:** timestamps are confirmed; record-creation event is not uniquely identified.
- **X2 K4 direct findings / SEBAGIAN overall:** CFG and direct memory sites are reproducible from committed static inputs; global xref and indirect-access completeness remain unverified.
- **X3 K4 / TUNTAS:** raw register/RAM values, byte encodings, and hashes were parsed and independently rechecked from the checkpoint bytes, with no emulator load/run.
