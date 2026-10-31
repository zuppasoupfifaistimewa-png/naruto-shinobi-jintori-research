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


## Addendum — ukuran resource dan callback pasca-read (31 Oktober 2026)

### Run #41157751728
- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41157751728
- Job: 124408205088 — Trace resource reader, allocation pointer, and payload consumers.
- Commit SHA: eafbe6f8bc7c4a11d2530d6154d076d25785bf1d.
- Status: **completed / success**; exit code **0**.
- Artefak teks: step7-loader-payload-static-trace, ID 13025842594, 45.375 byte.
- SHA-256 ZIP: b7271bdda33055e28271521f8a847a93ba9759268993515d6eec27c23c5ee2fa.
- Semua langkah job selesai/success. Input executable yang sama tervalidasi; private input dan project dibersihkan. Tidak ada game/emulator, input gameplay atau savestate.

### 1. Lookup ukuran berdasarkan directory index
- Fungsi 0x8002DBB8 hanya memanggil 0x8002D4E4 tanpa mengubah register argumen. Pada MIPS, a0 dari caller tetap diteruskan; caller menggunakannya sebagai directory index.
- 0x8002D4E4 membaca uint32 length dari row index*8 + 4, lalu membulatkan ke atas ke kelipatan 0x800 byte.
- Ghidra melaporkan 15 direct xrefs ke 0x8002DBB8. Contoh caller yang terlihat meliputi 0x800196C4, 0x800198E0, 0x8001A648, 0x8001A57C, 0x8001BC04, 0x8002DCF8, 0x8001E9A0, 0x8001EF38, 0x8002409C, 0x8002DD80, 0x8003275C, 0x80024258, 0x80024B70, dan 0x80024464.
- 0x8002D560 merupakan jalur berbeda: memanggil 0x8003A048 untuk menyelesaikan deskriptor/path dan mengembalikan nilai length dari record lokal jika lookup berhasil. Jangan samakan fungsi ini dengan length langsung dari direktori DATA.BIN.

### 2. Pointer direktori aktif
- 0x8002C9B8 secara langsung menyimpan a0 ke GP+0x9C.
- 0x8002D710 adalah wrapper yang memanggil 0x8002C9B8.
- 0x8002C9C4 mengembalikan pointer yang disimpan di GP+0x9C.
- XREF ke 0x8002C9B8 hanya satu, dari 0x8002D710. XREF ke 0x8002D710 dari startup 0x80011560 muncul pada dua callsite; startup memberikan alamat tabel dari struktur bootstrap dan kemudian alamat salinan direktori aktif.
- Ini menutup hubungan setter/getter pointer direktori pada main EXE. Belum membuktikan waktu atau caller yang meminta directory index 0/1.

### 3. Free-list allocator
- 0x8002DDE0 adalah stub kosong (return); tidak terlihat perubahan state.
- 0x8002DFE4 memperbarui penghitung alokasi, menangani slot khusus GP+0xA8, dan pada jalur umum memanggil 0x80035BB8.
- 0x80035BB8 menyisipkan blok ke free list dan menggabungkan blok tetangga yang bersebelahan. Ini bukti kode statis operasi pelepasan/coalescing heap, bukan semantik resource/gameplay.

### 4. Callback dan transformasi setelah read
- 0x80019C10 menerima completion callback, memanggil 0x80019CA4 pada buffer global 0x800891EC, membersihkan status, melepas buffer saat kondisi parse terpenuhi, dan dapat meneruskan hasil ke user callback.
- 0x8001A770 memanggil 0x8001E50C dan 0x8001ECA4 dengan buffer hasil read plus parameter koordinat/descriptor; pada jalur sukses ia melepas buffer dan memanggil callback pengguna. Ini menunjukkan read bisa diikuti pemrosesan resource lain sebelum buffer dilepas.
- 0x8001EBF4 dapat memanggil 0x8001EB08 lalu meneruskan status ke callback aplikasi; 0x8001F048 memanggil 0x8001ECA4, lalu melepas buffer dan meneruskan hasil.
- 0x80024B10 memanggil helper 0x80037138 dengan argumen -1, memperbarui pointer state-machine per-slot dan menaikkan status. Ini callback untuk state-machine 0x80024B70, bukan bukti bahwa helper tersebut merupakan logika seed boot atau gameplay.
- 0x8002DD80 menghitung pointer akhir/aligned dari static buffer DAT_80010498 ditambah ukuran yang diperoleh melalui 0x8002DBB8, lalu memanggil callback tersimpan di GP+0x16C.

### 5. Contoh pemanggilan dengan indeks resource yang diketahui
- 0x800196C4 secara eksplisit meminta directory index 0x5D2 (1490), mengambil ukuran melalui 0x8002DBB8, mengalokasikan buffer, membaca melalui 0x8002D7F8, lalu menyalin data ke alamat statis 0x80089A18 sebelum membebaskan buffer. Ini contoh konkret pola **read → salin ke buffer lain → release**, tetapi resource ini bukan index 0/1.
- 0x8001A4D8 secara eksplisit meminta index 0x307 (775), membaca ke buffer sementara, meneruskan buffer ke helper 0x80035D08 dengan tujuan 0x80089DB8, lalu melepas buffer. Ini contoh kedua bahwa loader dapat menyalin/memproses payload sesudah read.
- 0x8001A648 menghitung index dari (param2 & 0xFF)+0x2A9, sehingga hasilnya berada pada rentang 681–936; ini bukan index 0 atau 1.
- 0x80024464 dan 0x80024B70 adalah state-machine resource loaders. Keduanya menghitung index dari tabel/global descriptor, mengambil size lewat 0x8002DBB8, membuat buffer, lalu membaca melalui 0x8002D838. Callback mengubah state lanjutan. Input descriptor/tabel dan nilai runtime belum teridentifikasi.
- 0x8002DCF8 mempunyai direct caller 0x8002DC90 dan 0x80011F18. Keduanya belum diekspor pada run ini. Ini jalur prioritas berikutnya karena DCF8 meneruskan param1 sebagai directory index ke reader dan menggunakan static buffer DAT_80010498.

### Keputusan setelah addendum
**Terbukti secara statis pada main EXE:** pola direktori index → lookup length → sector-rounding → allocation → CD-read queue → callback; pointer directory aktif berada di GP+0x9C; dan ada caller yang menyalin atau memproses payload ke buffer lain setelah read.

**Belum terbukti:** apakah Entry 0 dan Entry 1 diproses oleh callback tertentu, alamat buffer final untuk kedua entry itu, apakah keduanya dieksekusi sebagai kode, dan di mana code relocation/decompression/transfer-of-control dilakukan.

Fokus run berikutnya adalah menelusuri caller 0x80011F18 dan 0x8002DC90, kemudian membuktikan apakah keduanya mengirim index 0 atau 1 ke 0x8002DCF8. Jika tidak, telusuri seluruh dynamic index producers pada state-machine 0x80024464/0x80024B70. Status biaya Barrier, upgrade, toll dan pendapatan Stage 1 tetap UNKNOWN.

## Addendum — koreksi bootstrap awal dan slot pointer buffer (Run #41158277447)

Run #41158277447 (job 124409826948) selesai **completed/success**, exit code 0, pada commit input 7f88eb437fbbb23e317647f3b783a7bd5a5ac744. Artefak teks #13025409336, 59.925 byte, SHA-256 ZIP 129fb7eac55f0624b5c437b88a68323b779c092ca1227a23f093232df1923747. Cleanup private input dan project PASS; tidak ada game/emulator, gameplay, input atau savestate.

Static data dump menemukan:
- Slot global 0x80010498 berisi word 0x800AD450 di executable image. Instruksi 0x8002DCF8 dan callback 0x8002DD80 membaca isi slot ini sebagai pointer destination.
- Tabel sementara di 0x80055898 berisi LBN 212 (0xD4) dan byte_length 0x2F44 (12.100 byte).
- Startup 0x80011560 mengaktifkan pointer sementara tersebut, kemudian memanggil 0x8002DC90(0,0,0).
- Row 0 dari tabel sementara itu menunjuk ke blok bootstrap awal DATA.BIN, bukan ke row 0 direktori lengkap. Jadi klaim terdahulu bahwa startup langsung memuat resource Entry 0 110.536 byte adalah keliru dan ditarik kembali.
- 0x2F44 dibulatkan ke 0x3000 oleh helper length. Callback menambahkannya ke base pointer 0x800AD450 dan menyimpan aligned end pointer 0x800B0450. Startup menggunakan hasil itu untuk menginisialisasi allocator melalui 0x8002DE60.
- Setelah bootstrap read berhasil, startup memanggil kode di 0x800AD454. Kode itu menyalin 0x2F00 byte direktori penuh dari 0x800AD494 ke 0x8006D830, lalu mendaftarkan 0x8006D830 sebagai pointer direktori aktif.

Dengan demikian ada dua row “index 0” berbeda:
1. Tabel sementara startup: index 0 = LBN 212, panjang 0x2F44, yaitu bootstrap awal.
2. Direktori penuh hasil bootstrap: index 0 = LBN 403, panjang 110.536 byte, resource slice di DATA.BIN offset 0x5F800.

Dump lain di 0x800558A8 menunjukkan 16 descriptor 0x1C-byte dengan label TITLE, LOGO, MENU, BOARD, BOARDRET, BAT_INI, BAT_VIEW, PRESTG, AFTSTG, ENDING, MC_* dan BINGO. Record pertama memiliki word pertama 0 dan label TITLE; record kedua word pertama 5 dan label LOGO; beberapa record selanjutnya memuat pointer kode. Karena field tersebut heterogeneous, jangan anggap setiap word pertama sebagai directory index. Fungsi 0x80011F18 memang membaca word pertama record yang dipilih dan mengirimkannya ke 0x8002DCF8, tetapi belum ada bukti reachability: Ghidra melaporkan 0 direct function-entry references ke 0x80011F18.

**Status:** bootstrap awal dan alamat buffer untuk pembacaan awal terverifikasi secara statis. Waktu dan alamat pemuatan resource Entry 0 pada direktori penuh belum terbukti; pemuatan Entry 1 juga belum ditemukan. Alamat 0x800AD450 adalah buffer bootstrap, bukan otomatis runtime base Entry 0/1. Arena allocator berawal di 0x800B0450 setelah pembacaan bootstrap. Tidak ada runtime memory snapshot pada run ini.

Prioritas berikutnya: trace caller 0x80011FB4 ke DC90, callback 0x8001202C, dan referensi table 0x800558A8 dari 0x800118E0, 0x80011918, dan 0x80011FEC. Cari bukti argument provenance untuk directory index 1 sebelum menyambungkan Entry 1 ke handler ESTATE/LVUP_ESTATE.

Run summary:
run_id=41158277447
status=completed/success
job_id=124409826948
job=Trace resource reader, allocation pointer, and payload consumers
commit_sha=7f88eb437fbbb23e317647f3b783a7bd5a5ac744
exit_code=0
artifact_id=13025409336
artifact_name=step7-loader-payload-static-trace
artifact_sha256=129fb7eac55f0624b5c437b88a68323b779c092ca1227a23f093232df1923747
private_input_cleanup=PASS
text_only_artifact=yes
game_or_emulator_executed=no
gameplay_input_sent=no
savestate_restored=no

Status ekonomi Stage 1 tetap UNKNOWN: belum ada rumus pendapatan petak, biaya build/upgrade Barrier atau toll yang terbukti.


## Addendum — state descriptor dan pemicu load resource (Run #41158644685)

### Run dan artefak
- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41158644685
- Job: 124410972407 — Trace resource reader, allocation pointer, and payload consumers.
- Commit input: d1f0e9d2ab14885337e18cbc092679518e3086e8.
- Status: **completed / success**, exit code 0.
- Artefak: step7-loader-payload-static-trace, ID 13026375544, 63.085 byte.
- SHA-256 ZIP: f3f376bc4c9b46029141e2c3ab1efac5c8e41214f26db2751decb70fffbdd80f.
- PRIVATE_INPUT_AND_PROJECT_CLEANUP=PASS; hanya teks/log; tidak ada emulator, input gameplay, atau savestate.

### 1. Scene/state dispatcher
Fungsi 0x800117A4 memiliki satu direct caller dari 0x80011540 di startup loop 0x80011504. Ini bukan fungsi yang tidak terhubung; ia merupakan bagian dari pemrosesan state utama.
Dari raw MIPS dan dekompilasi:
- Membaca state aktif/pending dari global GP+0xE4 / GP+0xE0 (file-image addresses 0x8006D760 / 0x8006D75C dalam peta ini).
- Mengakses record dengan stride 0x1C pada tabel descriptor 0x800558A8.
- Memanggil function pointer record +0x0C pada salah satu jalur, +0x04 saat state berubah, dan +0x08 pada jalur update berikutnya.
- Membandingkan token/field record +0 dengan global GP+0xF0 (0x8006D76C). Jika berbeda dan field +0 bukan -1, ia memanggil 0x80011FB4 dengan pending state sebagai argumen.
- Setelah jalur transition, mengambil end pointer dari 0x8002DD74, menginisialisasi ulang allocator melalui 0x8002DE60, memperbarui state globals, dan melanjutkan callback state.

### 2. Fungsi 0x80011FB4 adalah penghubung state → directory read
Raw MIPS pada 0x80011FB4 menunjukkan:
- A0 (pending state index) disimpan di S0.
- Memanggil 0x80011F58(0) dan 0x80037138(0).
- Menghitung record address = 0x800558A8 + pending_state_index*0x1C.
- Membaca word pertama record +0 sebagai A0.
- Mengambil callback/context dari GP+0xF8 dan GP+0xFC.
- Memanggil 0x8002DC90(record[+0], callback, context).
- Jika berhasil, mengosongkan GP+0xF8 dan GP+0xFC dan mengembalikan true.

Jadi ada **direct static chain**:
state loop 0x800117A4 → state descriptor row → 0x80011FB4 → record[+0] → 0x8002DC90 → 0x8002DCF8 → directory reader/queued CD read.

### 3. Makna nilai pada descriptor table tetap heterogeneous
Static data dump:
- Row pertama (label TITLE) memiliki word +0 = 0.
- Row kedua (label LOGO) memiliki word +0 = 5.
- Beberapa row berikutnya memiliki word +0 berupa alamat kode, misalnya 0x800AF640 dan 0x800B1E88, bukan integer kecil.
- Fungsi 0x80011FB4 selalu meneruskan word +0 sebagai argumen loader pada candidate path, sehingga perilaku untuk record pointer-valued belum dapat dijelaskan. Jangan sebut setiap field +0 sebagai directory index.
- 0x80011F18 adalah jalur lain yang membaca field +0 dan memanggil DCF8 dengan callback tetap 0x8001202C; Ghidra tidak menemukan direct function-entry reference ke 0x80011F18. Sementara 0x80011FB4 memiliki satu direct caller dari 0x800117A4.

**Kesimpulan aman:** descriptor row TITLE (field +0 = 0) dan LOGO (field +0 = 5) adalah kandidat kuat resource identifiers, dan state manager memiliki jalur yang meneruskan field +0 ke loader. Namun pemanggilan aktual row mana pada sesi game tertentu serta arti field +0 untuk semua state masih belum ditutup. Tidak ada bukti directory index 1 dimuat melalui tabel ini.

### 4. Implikasi untuk Entry 0 dan Entry 1
- Entry 0 directory index 0 terhubung ke descriptor TITLE pada file image; state manager memiliki pemanggil loader yang dapat meneruskan nilai 0 ke DC90 jika TITLE menjadi pending state dan token saat ini berbeda.
- Entry 1 directory index 1 belum muncul sebagai field +0 numerik di descriptor table yang diekspor; itu tidak membuktikan Entry 1 tidak pernah dimuat, hanya bahwa tabel descriptor 16-record ini belum menunjukkan indeks tersebut.
- Buffer target DCF8 berasal dari isi global slot 0x80010498, yang pada file image bernilai 0x800AD450 untuk bootstrap awal. Apakah pointer ini berubah sebelum load TITLE/LOGO belum dibuktikan karena static XREF scan menemukan tiga READ dan tidak menemukan direct WRITE pada slot tersebut.
- Pemanggil 0x80011FB4 tidak menyetel A0 ke indeks state; ia mengambil field +0 record. Ini penting ketika menguji apakah nilai tersebut merupakan resource index atau tipe descriptor lain.

### Keputusan dan tugas lanjutan
1. Trace fungsi 0x80011F58 dan 0x80011F7C serta semua writer global GP+0xF0/+0xF8/+0xFC dan state GP+0xE0/+0xE4. Ini akan menjelaskan token resource aktif, callback, dan jalur ketika row pointer-valued tidak memicu invalid directory read.
2. Periksa jalur caller 0x800117A4 dan state initialization 0x80011504 untuk nilai awal scene/state pada boot.
3. Cari direct dan indirect path yang meminta directory index 1 secara eksplisit, termasuk resource list selain descriptor table 0x800558A8.
4. Setelah entry1 load path dan payload base diketahui, lanjutkan tracing code di resource tersebut ke ESTATE dan LVUP_ESTATE.

Status ekonomi Stage 1 tetap UNKNOWN: belum ada rumus pendapatan petak, biaya pembangunan/upgrade Barrier, atau toll yang terverifikasi.

## Addendum — state resource token dan jalur kondisional Entry 1 (Run #41158940692)

### Run dan artefak
- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41158940692
- Job: 124411903548 — Trace resource reader, allocation pointer, and payload consumers.
- Commit input: be061a58fd81886735bef89513735b3e2e4f46ff.
- Status: **completed / success**, exit code 0.
- Artefak: step7-loader-payload-static-trace, ID 13026655433, 66.113 byte.
- SHA-256 ZIP: 5d945a6d25f066a3ab0be5f29dd95e56e58e50f79a675e094e23f0bdfa8775bf.
- PRIVATE_INPUT_AND_PROJECT_CLEANUP=PASS; artifact teks saja; tidak ada game/emulator, input gameplay atau savestate.

### 1. Peran fungsi state helper
- 0x80011F58 adalah getter/setter sederhana: mengambil word GP+0xF4, menyimpan argumen A0 ke slot yang sama, lalu mengembalikan nilai lama. Ia bukan pembaca resource.
- 0x80011F7C hanya berisi jr ra dengan delay slot clear v0, sehingga return-nya selalu 0 dalam body terdekode saat ini. 0x800117A4 menguji nilai ini setelah pemanggilan.
- 0x80011FB4 memanggil 0x80011F58(0) sebelum memanggil helper lain dan loader.

### 2. Global state scene/resource pada file-image view
Alamat berikut adalah file-image global slots pada main EXE, bukan snapshot RAM saat gameplay:
| Slot | Nilai awal di image | Writer/readers yang terlihat | Peran yang didukung kode |
|---|---:|---|---|
| 0x8006D75C (GP+E0) | 0 | ditulis di 0x800116C4; dibaca 0x80011864, 0x800118C4, 0x80011900, 0x80011970, 0x80011984 | pending scene/state index |
| 0x8006D760 (GP+E4) | 0 | ditulis 0x800116C8 dan 0x8001198C; dibaca state manager | current scene/state index |
| 0x8006D764 (GP+E8) | 0 | ditulis 0x800116CC dan 0x80011980 | previous scene/state slot |
| 0x8006D768 (GP+EC) | 0 | ditulis 0x800116D0, dibaca 0x80011874, dibersihkan 0x80011990 | transition/dirty flag slot |
| 0x8006D76C (GP+F0) | 0 | ditulis 0x800116D8 dan 0x80011920; dibaca 0x800118DC | active resource token compared against descriptor[+0] |
| 0x8006D774 (GP+F8) | 0 | ditulis 0x800116E8, dibaca 0x8001192C | completion callback pointer passed to 0x8002DC90 |
| 0x8006D778 (GP+FC) | 0 | ditulis 0x800116EC, dibaca 0x80011944 | callback context passed to 0x8002DC90 |

The static references show startup initialization at function 0x800116B8 (called by 0x80011608), with file-image values initially zero. Exact xref counts are from the bounded Ghidra reference exporter; indirect aliases or un-decoded instructions may not appear.

### 3. Conditional route from scene descriptor to directory index 1
Raw MIPS establishes the following sequence:
1. 0x800117A4 reads pending scene index from GP+0xE0 and forms descriptor address 0x800558A8 + scene_index*0x1C.
2. It reads descriptor word +0 and compares it to active resource token GP+0xF0.
3. When the token differs and descriptor word +0 is not -1, it calls 0x80011FB4 with the pending scene index.
4. 0x80011FB4 calculates the same descriptor record address, reads its word +0 as A0, reads callback/context from GP+0xF8/GP+0xFC, then calls 0x8002DC90(A0, callback, context).
5. 0x8002DC90 calls 0x8002DCF8, which passes the index through 0x8002DBB8/0x8002D4E4 and then 0x8002D838 to the CD read path.

Descriptor dump values that matter:
| Descriptor row index | Label | Word +0 |
|---:|---|---:|
| 0 | TITLE | 0 |
| 1 | LOGO | 5 |
| 4 | BOARDRET | 1 |
| 5 | BAT_INI | 1 |
| 6 | BAT_VIEW | 1 |
| 7 | PRESTG | 2 |
| 8 | AFTSTG | 2 |
| 9 | ENDING | 2 |

**Strong VERIFIED-STATIC conditional route:** if pending scene row 4 (BOARDRET), 5 (BAT_INI), or 6 (BAT_VIEW) is selected while GP+F0 differs from 1, state manager sends directory index 1 through the reader family. Likewise, descriptor rows 7–9 carry value 2 and are candidates for loading directory index 2 under the same token mismatch condition.

This is static control/data flow, not a runtime observation that those states actually occur during the current save/playthrough. The labels identify descriptor rows; the row field +0 value is passed to the resource loader on this conditional path.

### 4. Important semantic guard
The descriptor table is heterogeneous. Some rows have function-address values at word +0 (for example rows with values 0x800AF640 and 0x800B1E88) rather than small integers. Do not treat every row as a directory index. The current chain shows how field +0 is forwarded, but the meaning/path for pointer-valued records remains unresolved. The route for numeric values 0, 1, 2, and 5 is structurally meaningful and is the present investigation focus.

### 5. Current result for Entry 1
- Entry 1 is directory index 1 (LBN 8.778, 596.412 bytes, DATA.BIN offset 0x10BB000), independently verified by directory parsing and slice SHA.
- The scene-state descriptor rows BOARDRET, BAT_INI, and BAT_VIEW contain +0 = 1.
- The state manager compares that field against GP+F0 and, on mismatch, calls the resource loader with the field as directory index.
- The loader uses the pointer value read from global slot 0x80010498 as the destination. File-image value is 0x800AD450, but no runtime memory snapshot exists; the slot has three direct READ xrefs and no direct WRITE xref in this bounded scan. Treat 0x800AD450 as the statically evidenced default buffer destination, not a verified dynamic runtime mapping for every request.
- The rounded Entry 1 size is 0x92000 (596.412 bytes rounded up to 0x800-sector boundary). If the destination remains 0x800AD450, the callback end pointer would be 0x80134450; this is an arithmetic consequence, not a captured runtime pointer or a verified final execution address.

### 6. Next evidence gate
1. Determine whether the pointer in 0x80010498 changes indirectly or through an unobserved writer before loads of resources 1/2/5.
2. Identify initialization and actual writes of scene state indices GP+E0/GP+E4 and transitions into descriptor rows 4–9.
3. Confirm callback/context behavior through GP+F8/GP+FC for resource reads of index 1.
4. Determine whether Entry 1 is read as an executable overlay, a data package, or both; trace its callbacks and any copy/relocation/decompression after read.
5. Once the Entry 1 payload ownership is established, resume function tracing for ESTATE and LVUP_ESTATE.

No gameplay economy rule was upgraded. Pendapatan petak, biaya build/upgrade Barrier, and toll remain **UNKNOWN**.

## Addendum — Entry 1 dianalisis pada base buffer loader 0x800AD450 (Run #41159301877)

### Run dan artefak
- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41159301877
- Job: 124413051125 — Analyze verified Entry 1 slice at 0x800AD450.
- Commit input: 9a6dc0532e865701c654f7650967857c3c8c2c8a.
- Status: completed / success, exit code 0.
- Artefak: entry1-loader-buffer-base-static-audit, ID 13026790772, 26.174 byte.
- SHA-256 ZIP: d72d97209e3afd1ec9c26f837cfba65764e4c3b840f512830be4bad08aac9cf0.
- Entry 1 row 1, LBN 8.778, byte_length 596.412, offset 0x10BB000 dan slice SHA 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a tervalidasi ulang.
- Input slice dan project dibersihkan; PRIVATE_INPUT_AND_PROJECT_CLEANUP=PASS. Artifact hanya teks/log. Tidak ada emulator, gameplay/input atau savestate.

### 1. Fungsi 0x800BDC4C pada Entry 1
Di base buffer 0x800AD450, alamat 0x800BDC4C jatuh pada file offset **0x107FC** dalam Entry 1 dan raw MIPS membentuk fungsi yang koheren:
- Prolog menyimpan RA dan S0–S4.
- A0 dipotong menjadi 16 bit sebagai selected value.
- Nilai itu dibandingkan dengan byte global DAT_8013EA71; bila tidak di bawah batas, ia diganti dengan halfword DAT_8013EA8A.
- Loop berjalan sampai count DAT_8013EAC8.
- Record ke-i berasal dari DAT_8013EA84 + i*0x124.
- Record diterima bila byte +0 == 5 dan (uint16(record+0x20) >> 12) == selected_value.
- Untuk setiap record yang cocok, fungsi memanggil FUN_800B770C(i & 0xFF) dan menjumlahkan hasilnya.
- Setelah loop, fungsi memanggil getter konfigurasi 0x80012A8C; return = jumlah kontribusi dibagi dua dengan pembulatan integer ke arah nol, ditambah nilai getter tersebut.

Bentuk pseudocode aman (nama field tetap belum diketahui):

    p = (selected < DAT_8013EA71) ? selected : DAT_8013EA8A
    S = 0
    for i in [0, DAT_8013EAC8):
        r = DAT_8013EA84 + i * 0x124
        if byte(r+0) == 5 and (u16(r+0x20) >> 12) == p:
            S += FUN_800B770C(i & 0xFF)
    return trunc_toward_zero(S / 2) + GET_80012A8C()

Ini adalah VERIFIED-STATIC untuk operasi dan dataflow MIPS di candidate Entry 1 view. Arti natural-language byte status 5, nibble/flag halfword +0x20, FUN_800B770C, dan config 0x80012A8C masih UNKNOWN. Jangan sebut S sebagai income/rent sebelum helper 0x800B770C diartikan.

### 2. Dua penggunaan helper dalam code path Entry 1
**UI candidate 0x80107F4C (alamat terkoreksi dari kandidat lama 0x8012AAFC):**
- Mengambil byte selected ID dari object +0x94A.
- Menampilkan hasil 0x80013CBC(ID) melalui drawing helper 0x8001B364.
- Memanggil 0x800BDC4C(ID) dan menampilkan nilainya sendiri.
- Mengambil participant value melalui 0x800138EC(ID), menjumlahkannya dengan hasil BDC4C, clamp ke -9.999..99.999, lalu menampilkan jumlah itu dengan helper drawing 0x8001B364.
- Ini membuktikan helper digunakan dalam tampilan nilai yang berdampingan dengan participant Chakra getter. Belum membuktikan helper adalah pembayaran atau kredit saldo.

**Target-threshold candidate 0x800CF434 (alamat kandidat lama 0x800F1FE4):**
- Instruksi raw memanggil 0x800BDC4C, mengambil participant record field +4, memanggil target getter 0x80012A70, dan membandingkan hasil penjumlahan helper + record +4 terhadap target.
- Dekompilasi fungsi ini memiliki register/provenance yang tidak lengkap karena alamat target di-seed manual di tengah alur dan bukan function entry tervalidasi. Gunakan hanya raw instruction window untuk menyatakan adanya operasi addition/comparison lokal; jangan menafsirkan seluruh C pseudocode sebagai fungsi utuh.
- Jalur threshold masih multi-guard dan belum membuktikan kemenangan dengan sendirinya.

### 3. Mengapa analisis lama bertentangan: alamat yang sama, resource berbeda
Alamat virtual 0x800BDC4C menunjuk ke byte file berbeda tergantung base resource:
- Entry 0 pada hipotesis base 0x800AD000: offset 0x10C4C. Di sini isi berupa fungsi yang membaca pointer A0 dan menulis field relatif +0x64/+0x68.
- Entry 1 pada candidate loader-buffer base 0x800AD450: offset 0x107FC. Di sini isi berupa fungsi akumulator yang membaca struktur stride 0x124 dan memanggil FUN_800B770C.

Karena base resource berubah 0x450 byte, satu alamat virtual dapat memuat kode berbeda setelah overlay/resource diganti. Ini menjelaskan kontradiksi helper sebelumnya tanpa menggabungkan kedua bytecode sebagai satu fungsi yang sama. Entry 1 base 0x800AD450 masih STATIC CANDIDATE, karena slot global destination dan state->index path sudah ditemukan secara statis tetapi belum direkam sebagai snapshot RAM runtime.

### 4. Koreksi metadata offset pada artefak run ini
Post-processing versi pertama gagal mengenali header TARGET tanpa prefix 0x pada alamat. Akibatnya field target_offset_under_hypothesis di artefak run 41159301877 masih memakai offset dari base lama 0x800AD000, yakni 0x450 terlalu besar. Ini adalah kesalahan metadata saja; alamat, raw MIPS, body dan dekompilasi yang dicetak berada pada target address yang diminta.
Offset yang benar pada base 0x800AD450:
- 0x800BDC4C = +0x107FC
- 0x80107F4C = +0x5AAFC
- 0x800BE5D8 = +0x11188
- 0x800F9520 = +0x4C0D0
- 0x800B5D68 = +0x8918
- 0x800EE4E0 = +0x41090
- 0x800CF434 = +0x21FE4
- 0x80108054 = +0x5AC04
- 0x80109994 = +0x5C544
- 0x80109F1C = +0x5CACC
Workflow sudah diperbaiki pada commit 934c735a39b7ccc2f650e685d78e0aa91c407840: regex menerima header dengan atau tanpa 0x, dan memeriksa helper offset +0x107FC. Run ulang 41159510198 sedang berjalan untuk mengeluarkan hasil perbaikan serta target tambahan.

### 5. Kesimpulan Stage 1 setelah base diperbaiki
- Helper 0x800BDC4C kini jelas memiliki logika agregasi berbasis sejumlah record, bukan sekadar stub pointer.
- Helper tersebut menambahkan kontribusi agregat ke getter config 0x80012A8C.
- Satu UI path menambahkan hasil helper ke Chakra getter dan menampilkannya.
- Satu target-gate candidate membandingkan helper result + participant record +4 dengan configured target.
- Belum dibuktikan bahwa record status 5 adalah petak yang dimiliki player, bahwa FUN_800B770C adalah nilai toll/income, atau bahwa akumulasi ini dikreditkan ke saldo pemain. FUN_800B770C adalah next dependency yang wajib diurai.
- Biaya build Barrier, biaya upgrade Barrier, dan toll mendarat di petak lawan masih UNKNOWN.

Prioritas berikutnya: periksa 0x800B770C, 0x800BDBFC, dan 0x800B7464 pada base Entry 1 yang sama; telusuri incoming callers dan record-field reads/writes untuk DAT_8013EA84, status byte +0, halfword +0x20, dan stride 0x124. Jangan mengubah nama field menjadi owner/estate sebelum konsumen atau perubahan state terkait dapat dibuktikan.

## Addendum — nilai per-record yang membentuk kontribusi 0x800BDC4C (Run #41159510198)

### Run dan artefak
- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41159510198
- Job: 124413702244 — Analyze verified Entry 1 slice at 0x800AD450.
- Commit input: 934c735a39b7ccc2f650e685d78e0aa91c407840.
- Status: completed / success, exit code 0.
- Artefak: entry1-loader-buffer-base-static-audit, ID 13026796167, 30.317 byte.
- SHA-256 ZIP: 2911f19a826743f8dc46151c04a79b28f412d1da275be7b5a34f6c359f100d8f.
- Entry 1 SHA tervalidasi ulang; private input/project cleanup PASS; artefak hanya teks/log; tidak ada game/emulator, gameplay/input, atau savestate.
- Metadata offset sudah diperbaiki: target 0x800BDC4C dicatat dengan offset Entry 1 +0x107FC pada base 0x800AD450.

### 1. FUN_800B770C — lookup nilai per-record dan multiplier
Raw/decompile pada Entry 1 candidate base 0x800AD450 menunjukkan:
- Parameter index dipotong menjadi 8 bit.
- Alamat record = DAT_8013EA84 + index*0x124.
- Byte record +0x0B memilih salah satu dari 5 cabang.
- Field halfword dasar dipilih melalui index bit yang berasal dari halfword record +0x20:
  base = u16(record + 0x10 + ((u16(record + 0x20) >> 7) & 0x1E)).
- Nilai hasil berdasarkan byte tipe +0x0B:
  - 0: base (100%).
  - 1: base*12/10 (120%).
  - 2: base*15/10 (150%).
  - 3: base*18/10 (180%).
  - 4: base*2 (200%).
  - selain 0–4: 0.
- Pembagian integer dipakai pada cabang 1–3.

Ini adalah VERIFIED-STATIC untuk rumus numerik per-record, tetapi label semantik byte +0x0B, halfword +0x20, dan tabel halfword +0x10 masih UNKNOWN. Jangan sebut base sebagai harga bangun, toll, atau income sampai mutator/consumer field tersebut teridentifikasi.

### 2. Hubungan FUN_800BDC4C dan FUN_800B770C
Helper utama 0x800BDC4C:
- Iterasi semua record sampai DAT_8013EAC8.
- Memilih record bila byte +0 == 5 dan (u16(record+0x20) >> 12) == selected_id.
- Menambahkan hasil FUN_800B770C(record_index) untuk setiap record yang cocok.
- Membagi jumlah agregat dengan 2 menggunakan pembulatan signed integer ke arah nol, lalu menambah getter konfigurasi 0x80012A8C.

Karena byte status +0 == 5 adalah filter penting, kita tahu aggregate hanya mencakup subset record tertentu. Arti status 5 dan apakah subset itu adalah properti ber-Barrier/owned tiles belum terbukti.

### 3. XREF pemanggil FUN_800B770C
Ghidra menemukan banyak direct callers. Yang terlihat pada artefak mencakup:
- 0x800FC700, 0x800FCA0C, 0x800FCB44, 0x800FD730, 0x800FD868,
- 0x800FE314, 0x800FE42C, 0x800FE6A0, 0x800FE7B8, 0x800FEA28,
- 0x800FEB38, 0x800FB598, 0x800C815C, 0x800CD678, 0x800E0324,
- 0x800F1CCC, 0x800F1D08, 0x800F1DF0, 0x800F1F4C, 0x800F2050,
serta helper aggregate 0x800BDC4C.
- Direct caller count lebih besar dari jumlah contoh di atas; daftar lengkap berada dalam bagian REFERENCES_TO_TARGET artefak teks.
- Ini berarti per-record amount helper dipakai oleh beberapa gameplay candidate call paths, bukan hanya fungsi tampilan total.

### 4. Arti ekonomi masih belum ditentukan
Temuan ini mempersempit pertanyaan, tetapi belum menjawab seluruh rumus game:
- Field halfword record+0x10 sampai +0x2E tampak sebagai nilai dasar yang berubah sesuai indeks 0–15.
- Byte +0x0B memilih multiplier 1.0/1.2/1.5/1.8/2.0 atau zero.
- Halfword +0x20 mengandung dua grup bit yang dipakai helper utama: bit 7–11 membentuk indeks tabel, bit 12–15 dibandingkan dengan selected participant id.
- Byte record +0 = 5 menjadi filter agregasi total untuk satu peserta.
- Belum terbukti apakah nilai ini adalah toll yang dibayar saat mendarat, rent yang diterima owner, pendapatan saat menyelesaikan satu lap, atau penilaian nilai aset yang hanya dipakai UI/target score.

### 5. Next audit gate
1. Dump dan trace semua direct callers FUN_800B770C, prioritaskan beberapa lokasi berdekatan di 0x800FCxxx, 0x800FDxxx, 0x800FExxx, 0x800F1xxx, dan 0x800C8xxx.
2. Cari writer ke record byte +0, byte +0x0B, halfword +0x10..+0x2E dan halfword +0x20. Korelasikan perubahan dengan state Barrier level/owner.
3. Trace fungsi yang menggunakan hasil FUN_800B770C untuk mengubah participant Chakra melalui setter 0x8001387C, bukan hanya untuk tampilan/perbandingan target.
4. Pisahkan call path saat landing di tile lawan dengan call path saat reward/penghitungan turn/lap.
5. Pertahankan label status 5, tile type byte +0x0B, level code +0x20[7..11], owner code +0x20[12..15] sebagai field names sementara, bukan semantic truth.

Kesimpulan ekonomi Stage 1 masih BELUM DIKETAHUI. Rumus numerik per-record sudah ditemukan; maknanya dan peristiwa transaksi yang menjalankannya masih perlu dibuktikan.

## Addendum — call-site FUN_800B770C dan tampilan fee petak lawan (Run #41159805931)

### Provenance run
- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41159805931
- Job: 124414633147 — Analyze verified Entry 1 slice at 0x800AD450.
- Commit input: 20346f89463bb1ca8792317de1496e228470ebf8.
- Status: completed / success; exit code 0.
- Artifact: entry1-loader-buffer-base-static-audit, ID 13026831655, 84.546 bytes.
- ZIP SHA-256: 6dcb92f6b333308bfb67afe43d92259a223b743a3d534a5c9c989d776c78520a.
- Entry 1 slice identity PASS; cleanup PASS; artifact text/log only; no emulator, gameplay input or savestate.

### 1. Strong static evidence: negative fee shown on other-owned type-5 tile
Candidate board renderer 0x800FC700 (Entry 1 imported at the loader-derived candidate base 0x800AD450):
- Tests board record byte +0 == 5.
- Extracts owner-like code from (u16(record+0x20) >> 12) and compares it with selected participant ID DAT_8013EA88.
- On the not-equal branch, calls FUN_800B770C(record_index).
- Passes the negated return value to drawing helper 0x8001B364 at a board-tile display position.

The code therefore establishes that the calculated per-record amount is displayed with a negative sign on a status-5 tile whose owner code differs from the selected participant. This is **STRONG VERIFIED-STATIC evidence for a displayed toll/fee amount**. It does not prove the actual account debit, transfer recipient, or payment timing.

### 2. Other direct caller roles
The same helper is called from multiple Entry 1 candidate functions. Examples from the bounded caller audit:
- 0x800C815C: combines the amount with a flag-derived adjustment and compares candidate values to select an index; likely AI/selection scoring, not direct balance mutation.
- 0x800CD678: compares the amount to one quarter of a participant score/Chakra-like value and may adjust an AI score by -10,000; this is not a setter call.
- 0x800E0324: scans status-5 records for the selected owner code and chooses a low-valued candidate after flag adjustment.
- 0x800F1CCC: uses several computed values in comparisons with a third of a participant value and RNG thresholds before sending a status to another helper.
- 0x800FB598: draws a value near record/board coordinates.
- Other render-related calls appear in the 0x800FCxxx and 0x800FDxxx regions.

These caller shapes show the value is reused for display, ranking/selection, and AI decisions. The inspected callers do not yet close a debit-to-Chakra plus owner-credit transaction.

### 3. Current economy evidence matrix
| Mechanism | Evidence now available | Status |
|---|---|---|
| Per-record value formula | Halfword base selected by bits 7–11 of record +0x20; byte +0x0B selects 100%, 120%, 150%, 180%, 200%, otherwise zero | **VERIFIED-STATIC for arithmetic** |
| Fee shown on other-owned tile | Renderer checks status 5 and owner != selected participant, then draws -FUN_800B770C(record_index) | **STRONG VERIFIED-STATIC** |
| Actual payer debit on landing | No closed path to participant-value setter 0x8001387C found yet | **UNKNOWN** |
| Owner credit / income trigger | No closed path showing positive credit to tile owner; no lap/turn trigger established | **UNKNOWN** |
| Owned-tile aggregate | 0x800BDC4C sums per-record values for status-5 records matching selected owner code, divides by two and adds config getter 0x80012A8C | **VERIFIED-STATIC for dataflow; meaning UNKNOWN** |
| Barrier build cost | No source price → balance check → Chakra setter → owner/status mutation chain found | **UNKNOWN** |
| Barrier upgrade cost | No level price table/formula or complete LVUP_ESTATE transaction chain found | **UNKNOWN** |

### 4. Correction to wording
Use "displayed fee/toll candidate" for FUN_800B770C. Do not state that this is definitely paid on landing until an actual event handler changes the payer's participant value. Do not call the aggregate FUN_800BDC4C player income; it may instead be a property valuation/projection or target-score component.

### 5. Next audit gate
Search the full set of direct callers of FUN_800B770C for functions that also call 0x8001387C or directly write the participant value field; inspect callers of those functions to locate the landing/toll event. In parallel, find writers to record byte +0, byte +0x0B, halfwords +0x10..+0x2E and halfword +0x20. Keep the owner-credit path and build/upgrade cost path separate.

## Addendum — kegagalan pemanggil graph akibat konfigurasi scriptPath (Run #41160186973)

- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41160186973
- Job: 124415827585 — Analyze verified Entry 1 slice at 0x800AD450.
- Commit input: dc168c2eed2914210d4f199142cc97243b65d5af.
- Status: completed / failure, exit code 1.
- Penyebab: Ghidra headless tidak memecah nilai scriptPath yang berisi dua folder dipisahkan titik dua. Ia membaca seluruh string sebagai satu direktori, kemudian gagal menemukan ExportEntry0TargetFunction.java dan ExportPerRecordCallerGraph.java.
- Langkah verifikasi input Entry 1, Java, dan cache Ghidra selesai. Gagal pada awal langkah analisis sebelum script dijalankan. Cleanup private slice/project PASS dan artifact hanya text/log.
- Ini adalah kegagalan konfigurasi workflow, bukan hasil analisis game. Tidak ada kesimpulan gameplay baru.

Perbaikan:
- ExportPerRecordCallerGraph.java diduplikasi ke folder tools/ghidra, agar kedua postScript berada pada satu script path.
- Workflow kembali memakai satu folder tools/ghidra.
- Run perbaikan baru diharapkan dari perubahan workflow; belum dinilai sebelum hasilnya tersedia.


## Addendum — inventaris seluruh direct caller FUN_800B770C (Run #41160254539)

### Run dan artefak
- URL: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/41160254539
- Job: 124416042420 — Analyze verified Entry 1 slice at 0x800AD450.
- Commit input: 1b3ee51115342e1d484a019866f0a681067a3639.
- Status: completed / success; exit code 0.
- Artifact: entry1-loader-buffer-base-static-audit, ID 13025909960, 94.255 bytes.
- SHA-256 ZIP: 6f7c045c0c63135cc4d6aad55f8385e875135972919ada316200f5ad5ae9f84f.
- Entry 1 identity PASS; private input/project cleanup PASS; artifact teks/log only; tidak ada emulator, gameplay/input atau savestate.

### 1. Cakupan pemanggilan langsung
Ghidra menemukan **44 direct JAL call-site** yang menuju FUN_800B770C dalam decoded Entry 1 view. Caller function yang valid dan teridentifikasi antara lain:
- 0x800BDC4C (aggregator).
- 0x800C815C.
- 0x800CADB8.
- 0x800CB4B4.
- 0x800CCA18.
- 0x800CD678.
- 0x800D15A8.
- 0x800DC2E0.
- 0x800E0324.
- 0x800E03B0.
- 0x800E3E74.
- 0x800F1CCC.
- 0x800F2050.
- 0x800FB598.
- 0x800FC700.
- 0x800FCA0C.
- 0x800FD730.
- 0x800FE314.
- 0x800FEA28.
Beberapa call-site tidak memiliki containing-function boundary valid pada Ghidra output; tetap dicatat sebagai raw MIPS, tetapi tidak dipaksakan menjadi caller bernama.

### 2. Hasil scan helper transaksi pada body caller
Dalam fungsi caller dengan boundary valid yang diekspor, pemeriksaan direct JAL tidak menemukan pemanggilan langsung ke:
- 0x8001387C — participant-value setter.
- 0x800138EC — participant-value getter.
- 0x80012A70 — configured target getter.
Helper yang terlihat langsung pada subset caller ini terutama 0x8001B364 (drawing helper), 0x800BDBFC, serta helper internal lain di luar daftar watch yang diinginkan.
Batas penting: scan ini menghitung instruksi JAL langsung di dalam body yang Ghidra petakan. Ia tidak menyelesaikan JALR/indirect calls, store langsung pada struktur participant, pemanggilan oleh caller tingkat atas, atau helper perantara yang akhirnya mengubah saldo. Maka ketiadaan direct setter dalam caller body bukan bukti bahwa nilai tidak pernah ditransaksikan.

### 3. Caller yang perlu dibedah berikutnya
- 0x800CADB8 dan 0x800CB4B4 berisi beberapa perbandingan status/owner sebelum atau sesudah menghitung toll; berpotensi berada dekat board/tile event logic.
- 0x800D15A8 berisi banyak pemanggilan B770C dalam satu fungsi besar; kandidat penting untuk memahami loop/iterasi banyak petak atau proses nilai.
- 0x800E03B0 dan 0x800E3E74 memanggil helper tersebut pada jalur lain; perlu dibandingkan apakah hanya decision score atau bagian turn transition.
- 0x800C815C, 0x800CD678, 0x800E0324 dan 0x800F1CCC mempunyai penggunaan scoring/selection yang sudah terlihat; jangan menyebutnya transaksi saldo tanpa bukti setter/store.
- 0x800FC700, 0x800FCA0C, 0x800FD730, 0x800FE314, 0x800FEA28, 0x800FB598 memiliki pemanggilan drawing helper, sehingga sebagian pemakaian jelas terkait UI.

### 4. Kesimpulan
Hasil direct-caller census memperkuat bahwa FUN_800B770C dipakai luas untuk menghitung/menilai fee per record, tetapi **belum menemukan direct debit/credit saldo Chakra di dalam fungsi caller yang diverifikasi**. Jalur aktual pembayaran toll kemungkinan berada di helper perantara, caller tingkat lebih tinggi, atau direct store yang belum terinventarisasi. Jangan promosikan fee display menjadi transaksi aktual.
