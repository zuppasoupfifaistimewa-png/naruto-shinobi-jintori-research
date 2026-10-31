# Audit loader dan pemetaan indeks resource DATA.BIN — 31 Oktober 2026

## Ringkasan

Dua potongan kode resource yang sebelumnya dianalisis sebagai Entry 0 dan Entry 1 kini berhasil dicocokkan secara tepat dengan dua baris pertama direktori DATA.BIN:

- **Entry 0:** directory index 0, LBN 403, 110.536 byte, DATA.BIN offset 0x5F800.
- **Entry 1:** directory index 1, LBN 8.778, 596.412 byte, DATA.BIN offset 0x10BB000.

Kedua potongan lolos SHA-256 yang telah tercatat sebelumnya. Ini adalah **VERIFIED untuk struktur direktori dan identitas byte resource**. Hasil ini belum memberikan alamat RAM aktual, lokasi payload setelah alokasi, atau bukti bahwa setiap resource benar-benar dieksekusi sebagai kode.

## Run Actions dan identitas output

### Run #41157191546 — percobaan workflow awal
- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41157191546
- Job: 124406471345 — Trace resource reader, allocation pointer, and payload consumers.
- Commit SHA: 9a797fdd6d8918b642cf2ecedcd37d220560e2d6.
- Status: **completed / failure**; exit code **1**.
- Penyebab: environment variable SHA executable mengandung whitespace tambahan, sehingga sha256sum memproses nama file yang salah.
- Ghidra tidak dijalankan; tidak ada hasil analisis yang dihasilkan oleh run ini.

### Run #41157200149 — trace loader utama
- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41157200149
- Job: 124406644742 — Trace resource reader, allocation pointer, and payload consumers.
- Commit SHA: 7c26a58a24739415930c3fe2d786110fa0be53e4.
- Status: **completed / success**; exit code **0**.
- Artefak teks: step7-loader-payload-static-trace, ID 13025377482, 34.934 byte.
- SHA-256 ZIP: f19ad9b66e958718c3393156793413b415ee87126f88b0e41acc2079966d6e81.
- Semua langkah job selesai/success. Input executable tervalidasi: 385.024 byte, SHA-256 a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569; PC awal 0x80011448; load address 0x80010000; text size 0x5D800.
- Private executable dan Ghidra project dibersihkan. PRIVATE_INPUT_AND_PROJECT_CLEANUP=PASS; game_or_emulator_executed=no; gameplay_input_sent=no; savestate_restored=no; private_disc_or_executable_uploaded=no.

### Run #41157546342 — pemetaan direktori DATA.BIN
- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41157546342
- Job: 124407563290 — Map code-slice offsets to actual DATA.BIN directory indices.
- Commit SHA: 44ca8548fe9c4d9d8c66007b020e4987275ad6d8.
- Status: **completed / success**; exit code **0**.
- Artefak teks: databin-directory-resource-map, ID 13025662463, 19.196 byte.
- SHA-256 ZIP: e4dd4f82023b76b65ce94d4eed8e075e5c05d67971c9e0b55bceafeedf0612e0.
- DATA.BIN tervalidasi: 66.015.232 byte; SHA-256 69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822. Direktori berisi 1.504 baris, 1.500 aktif, 4 panjang nol.
- Private disc, extraction tree dan DATA.BIN dihapus; PRIVATE_INPUT_CLEANUP=PASS; artefak hanya teks/log.

## 1. Pemetaan resource ke baris direktori

### Entry 0
- Slice offset: 0x5F800.
- Relative sector dalam DATA.BIN: 191.
- LBN absolut ISO: 212 + 191 = 403.
- Directory index: **0**.
- Directory row: LBN 403, byte_length 110.536.
- File offset hasil row: 0x5F800.
- Panjang baris sama persis dengan slice: yes.
- SHA-256 slice: 56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4 — **PASS**.
- Tepat satu baris mulai pada LBN 403; tepat satu baris overlap dengan slice.

### Entry 1
- Slice offset: 0x10BB000.
- Relative sector dalam DATA.BIN: 8.566.
- LBN absolut ISO: 212 + 8.566 = 8.778.
- Directory index: **1**.
- Directory row: LBN 8.778, byte_length 596.412.
- File offset hasil row: 0x10BB000.
- Panjang baris sama persis dengan slice: yes.
- SHA-256 slice: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a — **PASS**.
- Tepat satu baris mulai pada LBN 8.778; tepat satu baris overlap dengan slice.

**Kesimpulan VERIFIED:** nama Entry 0 dan Entry 1 yang dipakai dalam audit statis cocok dengan nomor baris direktori 0 dan 1, bukan sekadar nama artefak buatan. Keduanya memiliki LBN dan ukuran yang dapat diverifikasi langsung dari direktori DATA.BIN.

## 2. Jalur loader utama yang dapat diartikan secara statis

Semua alamat berikut berasal dari disassembly main executable dengan base PS-X EXE tervalidasi 0x80010000.

### Direktori aktif
- Bootstrap menyalin direktori 0x2F00 byte dari alamat 0x800AD494 ke buffer 0x8006D830.
- Startup memanggil wrapper 0x8002D710, yang memanggil 0x8002C9B8; getter 0x8002C9C4 membaca pointer direktori aktif dari GP+0x9C.
- Ini mendukung hubungan antara startup directory copy dan pointer direktori aktif, tetapi belum mengidentifikasi kapan Entry 0/1 masing-masing diminta.

### Pembacaan berdasarkan directory index
- 0x8002D4E4(index) mengambil field byte_length pada row index*8 + 4, lalu membulatkannya ke atas ke kelipatan 0x800.
- 0x8002D00C(index, destination, size, context) mengambil pointer direktori aktif, membaca word pertama row index*8 (LBN), kemudian meneruskan LBN dan parameter destination/size/context ke 0x8002CF9C.
- 0x8002D160(index, destination, size, callback, context) juga mengambil row LBN melalui 0x8002C9C4, kemudian memanggil 0x8002D5C0 untuk menyiapkan request baca.
- 0x8002D5C0 menambahkan record request ke antrean baca CD. Ada pemeriksaan kapasitas count <= 14; request menyimpan sumber, pointer tujuan/parameter terkait, ukuran sektor-padded, dan callback/context.
- 0x8002D838 adalah wrapper tipis yang memanggil 0x8002D160. Pada indeks direktori, fungsi ini tidak dengan sendirinya menetapkan alamat payload.
- Ada sembilan caller langsung 0x8002D838 pada fungsi 0x800198E0, 0x8002DCF8, 0x8001A648, 0x8001E9A0, 0x8001EF38, 0x8002409C, 0x80024258, 0x80024464, dan 0x80024B70. Argumen indeks pada sebagian besar caller bersifat dinamis.

### Alokasi buffer
- 0x8002DEC4 meminta blok dari allocator 0x80035B08, lalu mencatat penghitung/alokasi global.
- 0x8002DF30(size) membulatkan ukuran ke kelipatan 8, meminta blok dengan tambahan 0x40 byte, menyiapkan descriptor/wrapper, dan mengembalikan pointer yang disimpan di GP+0xA8.
- 0x8002DFE4(pointer) mengubah penghitung alokasi dan melepaskan/merapikan blok sesuai jalur yang dipakai.
- 0x8002D8A4 dan 0x8002D9E4 memiliki bentuk alur allocation → directory read → release-on-failure → return pointer-on-success pada disassembly kandidat, tetapi tidak ditemukan direct xref ke function entry mereka dalam artefak ini. Jangan anggap keduanya sebagai jalur runtime yang pasti terpakai.

## 3. Yang belum terbukti

1. Caller mana yang meminta directory index 0 dan 1 pada setiap fase boot/Story Mode.
2. Apakah payload dibaca langsung ke pointer alokasi, kemudian dieksekusi dari alamat itu, atau disalin/relokasi ke alamat lain oleh callback/loader lanjutan.
3. Base RAM aktual dan identitas runtime overlay untuk Entry 0 serta Entry 1.
4. Apakah Entry 0/1 mengandung seluruh code path relevan untuk label ESTATE dan LVUP_ESTATE, atau hanya bagian resource tertentu.
5. Kaitan runtime Entry 0/1 dengan helper numerik 0x800BDC4C masih belum ditutup.
6. Jalur transaksi Chakra, sumber biaya Barrier, rumus upgrade dan pendapatan petak masih UNKNOWN.

## 4. Dampak pada audit Stage 1 economy

Perbaikan penting:
- Entry 0 dan Entry 1 sekarang dipastikan sebagai directory index 0 dan 1, dengan ukuran dan LBN yang cocok.
- Audit berikutnya dapat mulai dari call-site yang mengirim a0=0 atau a0=1 ke reader family, serta dari callback yang menerima buffer hasil baca.
- Ini belum menyelesaikan runtime pointer. Index identity tidak boleh disamakan dengan RAM address identity.
- Belum ada perubahan pada status gameplay: belum ada formula pendapatan petak, biaya build Barrier, biaya upgrade Barrier, toll, atau syarat kemenangan yang dipromosikan menjadi VERIFIED.

## 5. Langkah berikutnya
1. Trace fungsi 0x8002DBB8 dan 0x8002D560, yang digunakan caller untuk memperoleh panjang/parameter resource.
2. Trace 0x8002C9B8 dan pemanggil registrasi direktori untuk membuktikan kapan pointer direktori berubah.
3. Trace callback 0x80019C10, 0x8001A770, 0x8001EBF4, 0x8001F048, 0x80024B10, 0x80024448, serta 0x8002DD80 untuk melihat apa yang dilakukan setelah pembacaan selesai.
4. Identifikasi semua path yang meminta index 0 dan 1, lalu cari copy/decompress/relocate and code-execution transfer.
5. Setelah mapping payload ditutup, gunakan indeks 0/1 sebagai anchor untuk meneruskan call-chain ke ESTATE dan LVUP_ESTATE.

Tidak ada emulator/gameplay, input permainan atau restore savestate pada ketiga run loader/directory ini. Story Mode tidak dijalankan dan tidak dinyatakan selesai.
