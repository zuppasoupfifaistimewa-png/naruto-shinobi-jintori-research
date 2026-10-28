# Step 4 / Step 8 — trace operasi ID dan consumer statis lintas resource

Tanggal: 28 Oktober 2026 (WIB)  
Checkpoint yang diperiksa: `main` = `28dba03ce0198564ddf10d1a199758f0c2440c27`  
Status laporan: temuan **TERVERIFIKASI-STATIS** pada executable utama; jalur consumer DATA.BIN hanya **KUAT BERSYARAT** pada base analisis hipotetis. Semantik fitur game tetap **UNKNOWN**.

## Ringkasan untuk pemain

Kode yang sudah bisa dijelaskan sekarang mengelola kumpulan kode angka dalam dua bentuk berbeda:

1. Empat record memiliki masing-masing tiga tempat penyimpanan byte ID. Penambahan menyimpan ID ke tempat pertama yang nilainya tidak termasuk registry 52 ID. Penghapusan mengambil ID dari tempat pilihan, meneruskannya ke struktur daftar lain, merapatkan byte sesudah tempat yang dihapus, lalu menandai slot terakhir dengan `0xFF`.
2. Struktur daftar lain menyimpan byte ID berurutan. Kode menghitung posisi sisip dengan bilangan acak; pada jalur yang telah ditelusuri, posisi dipilih pada paruh belakang daftar. Kode menggeser byte agar ada tempat untuk ID dan menaikkan counter lain yang terpisah.
3. Ada indikasi statis yang cukup kuat bahwa alur resource lain memanggil operasi penghapusan itu ketika sebuah field berisi nilai `0x14`, `0x15`, atau `0x16`, kemudian menyalin kembali tiga byte ID ke record berukuran `0x90). Namun base RAM resource belum divalidasi dan hasil dekompilasi memuat peringatan instruksi/alur kontrol buruk. Jadi ini belum membuktikan arti nilai tersebut dalam permainan.

**Belum ada bukti yang membenarkan penamaan struktur ini sebagai kartu, inventaris, tim karakter, giliran, daftar gerakan, tile, barrier, atau fitur lain.** Ini adalah aturan operasi data yang berhasil direkonstruksi, bukan nama mekanik permainan.

## 1. Sumber dan batas audit

- Main executable dianalisis dari artefak teks Step 5, run [#40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524), artifact [#12739676233](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524/artifacts/12739676233), SHA-256 ZIP `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d`. Disassembly mentah yang dipakai adalah `main_text_80010000.text.s`.
- Consumer lintas resource diperiksa dari keluaran teks statis Step 6, run [#40611660635](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40611660635), artifact [#12783307599](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40611660635/artifacts/12783307599), SHA-256 ZIP `748eadbfe82980bba8d2088d11affba4310d524eb871b6a34ee5fd43584f2892`. Artefak memuat teks/log; biner privat tidak disertakan.
- View Ghidra untuk DATA.BIN entry 1 memakai base impor `0x800D0000), yang **belum diverifikasi sebagai alamat muat runtime**. Instruksi entry-1 di bawah karenanya bersifat kondisional pada peta analisis itu.
- Tidak ada emulator, tombol gameplay, restore savestate, atau pemain adaptif yang dijalankan. Tidak ada biner game/BIOS/state/RAM dump/screenshot privat yang dimasukkan ke repo atau artefak.

## 2. Registry numerik: apa yang dimaksud ID valid

| Elemen | Bukti kode | Kesimpulan yang diperbolehkan |
|---|---|---|
| Inisialisasi count | `0x800121AC–0x800121F4` mengiterasi record mulai `0x80055CEC` dengan stride `0x10`, berhenti saat word pertama `0xFFFFFFFF` di `0x8005602C` (indeks 52). Count ditulis ke `0x118($gp)`. | Registry memiliki 52 record indeks 0–51 menurut terminator tersebut. |
| Getter count | `0x800154D4` mengembalikan count itu. | Batas validasi adalah nilai ID unsigned di bawah 52. |
| Penambahan ke record | `0x80013A48` memask ID ke 8 bit lalu menolak ID `>= count`; setelah itu memeriksa tiga slot di record terpilih. | ID `0..51` dianggap valid oleh helper ini. ID `52..255` diperlakukan sebagai slot tak valid/kosong ketika memeriksa record. |
| Nama/arti ID | Tabel registry memiliki record 16 byte dengan sejumlah nilai numerik; bukti yang dibuka belum mengaitkannya secara independen ke teks/nama atau objek yang terlihat pemain. | **UNKNOWN.** Jangan menerjemahkan nomor menjadi nama karakter atau item hanya dari angka. |

`0xFFFFFFFF` pada `0x8005602C` adalah terminator tabel, sedangkan `0xFF` yang ditulis saat mengosongkan slot adalah byte penanda di slot ID; keduanya berada pada konteks berbeda dan tidak boleh dicampur.

## 3. Empat record, masing-masing tiga slot ID

Basis `0x80070EA0` berisi empat record dengan stride `0xB4` (indeks grup 0–3). Byte ID berada di offset `+0x0A`, `+0x0B`, `+0x0C`.

| Operasi | Pemanggil/kondisi yang terlihat | Efek data |
|---|---|---|
| Baca satu slot | `0x800139FC(group, slot)`; syarat `group < 4`, `slot < 3`. | Mengembalikan satu byte pada `record + 0x0A + slot`; argumen tak valid menghasilkan `0xFFFFFFFF` sebagai nilai balik. |
| Tulis slot | Setter di `0x800139B0); syarat grup/slot masih dalam rentang. | Menulis byte ID langsung ke slot yang dipilih. |
| Tambah ke slot kosong | `0x80013A48(group, ID)`; ID harus di bawah 52 dan grup di bawah 4. | Memindai slot dari awal; tempat pertama yang berisi nilai `>= 52` ditimpa dengan ID. Jika ketiganya berisi ID valid, mengembalikan gagal (0). |
| Hapus slot | `0x80013B10(group, slot)`; syarat `group < 4` dan `slot < 3). | Baca ID sebelum perubahan, teruskan ID itu ke helper sisip acak `0x80015ADC` dengan argumen grup yang disetel ke 0, rapatkan slot lokal bila slot 0 atau 1, lalu tulis `0xFF` ke slot ketiga. Pada slot 2 tidak perlu pemindahan slot di dalam record. |
| Uji tiga slot penuh | Badan sekitar `0x80013BF0` membaca tiga ID dan membandingkannya dengan count 52. | Mengembalikan benar hanya jika ketiga byte berada di rentang ID valid; selain itu salah. Ini menguji validitas numeric, bukan arti fitur. |

**Kondisi dan perubahan state yang dapat diuji dari kode:** untuk penambahan, ID invalid atau grup di luar rentang ditolak; record yang ketiga slotnya valid juga ditolak. Untuk penghapusan, grup/slot di luar rentang ditolak. Bila jalurnya lolos, penghapusan membaca ID lama sebelum memanggil helper sisip, merapatkan byte sesudah slot 0/1, dan menulis penanda `0xFF` di slot akhir. Makna aksi ini bagi pemain belum diketahui.

## 4. Daftar sumber, panjang, dan cursor bukan counter yang sama

Loader `0x80015610` menerima selector `0..17`. Untuk dua grup `g = 0,1`, sumber berada di:

`0x8005603C + selector * 0x40 + g * 0x480`

Byte disalin ke buffer aktif `0x80070D0A + g * 0x40`, dihentikan oleh sentinel `0xFF` atau batas 64 byte. Setelah penyalinan, panjang dan cursor disetel terpisah.

| Alamat | Tipe/arti operasional yang didukung kode | Catatan penting |
|---|---|---|
| `0x80070D02` | Halfword panjang template/list grup 0 | Dipakai sebagai panjang pada sejumlah helper grup 0. |
| `0x80070D04` | Halfword panjang template/list grup 1 | Diisi loader; bukan sumber panjang yang dipakai helper shuffle `0x80015B7C`. |
| `0x80070D06` | Halfword cursor grup 0 | Di-reset ke 0 oleh loader; getter `0x800158C8` membaca cursor ini. |
| `0x80070D08` | Halfword cursor grup 1 | Di-reset ke 0 oleh loader. |
| `0x80070D0A` | Buffer byte grup 0 | Kapasitas 64 byte. |
| `0x80070D4A` | Awal buffer grup 1 (`0x80070D0A + 0x40`) | Kapasitas 64 byte. |
| `0x80070C82` | Halfword counter terpisah di struktur mulai `0x80070C80` | Helper sisip menaikkan (bila nilai lama <64); helper penghapusan daftar menurunkannya. Tidak sama dengan panjang template di D02/D04. |
| `0x80070C86` | Halfword cursor yang dipakai getter `0x800157C4` | Mengindeks byte pada buffer lain di `0x80070C80 + 0x8A). Tidak sama dengan D06/D08. |
| `0x80070C8A` | Awal buffer ID yang diindeks | Getter/setter membaca/menulis byte berdasarkan indeks di sini. |

Untuk selector 0–8, kedua blok sumber statis identik dan panjang hingga sentinel berturut-turut adalah 51, 55, 59, 57, 61, 62, 62, 62, dan 11 byte. Selector 9–17 mempunyai 64 byte nol tanpa sentinel; loader akan menyalin 64 byte nol, bukan memperlakukan sumber itu sebagai daftar kosong. Dua tabel descriptor langsung yang diaudit hanya memberikan selector 0–8. Ini **tidak** membuktikan bahwa selector 9–17 tak pernah dipakai oleh pemanggil lain.

## 5. Ketidaksimetrian helper: parameter grup diabaikan di jalur yang diaudit

Raw MIPS mendukung bahwa bagian keluarga helper ini memaksa grup efektif menjadi 0, meskipun beberapa pemanggil menerima parameter grup:

- `0x800158D8` membaca byte dari `0x80070D02` dan tidak memakai argumen sebagai indeks grup.
- `0x800158E8` menyetel indeks grup internal ke 0, memvalidasi posisi terhadap panjang dari daftar pertama, lalu menggeser byte pada `0x80070D0A) ke kiri. Setelah itu, helper menurunkan `0x80070C82`; ia tidak memperbarui `0x80070D02` dan tidak menghapus byte ekor.
- `0x800159BC` mengatur argumen grup internal ke 0 sebelum mengambil panjang melalui `0x800158D8`. Pada posisi yang valid dan ID valid, ia menaikkan counter `0x80070C82` jika nilai sebelumnya <64, menggeser isi `0x80070D0A` satu posisi ke kanan mulai akhir daftar hingga lokasi sisip, lalu menulis ID di `0x80070C80 + 0x8A + posisi`. Tidak ada penulisan ke panjang D02 di jalur ini.
- `0x80015B7C` menetapkan `a0=0` pada `0x80015B9C`, membaca halfword D02, dan mengacak buffer pertama saja.
- `0x80015768` membaca byte pertama dari buffer pertama, meminta penghapusan posisi 0, lalu memanggil helper pengacak dan mengembalikan byte yang dibaca sebelum perubahan.

Maka loader memang membangun dua buffer; tetapi keluarga operasi sisip/hapus/acakan yang dilihat di atas menarget buffer 0. Secara statis ini adalah **ketidaksimetrian yang nyata**. Apakah itu desain yang disengaja, keterbatasan jalur tertentu, atau cacat implementasi masih **UNKNOWN**. Tidak cukup bukti untuk menyebutnya bug.

### Detail posisi sisip pseudo-acak

`0x80015ADC` terlebih dahulu memvalidasi ID terhadap registry 52 entri. Pada jalur valid, ia memperoleh panjang `n` melalui `0x800158D8`, mengambil output RNG dari `0x80035D78`, dan menghitung:

`position = floor(n / 2) + (RNG % floor(n / 2))`

Kemudian ia memanggil `0x800159BC` dengan posisi dan ID tersebut. Untuk `n >= 2`, rumus memilih posisi pada paruh kedua daftar. Bila `floor(n/2)=0`, kode MIPS memiliki jalur instruksi `break` sesudah pembagian nol; jangan mengasumsikan fungsi ini aman untuk daftar berisi 0 atau 1 byte. Fungsi pemanggil `0x80013B10` tidak menggunakan nilai balik sisip untuk menentukan nilai balik penghapusannya, sehingga sukses dari pemanggil tidak dengan sendirinya membuktikan bahwa counter/daftar sekunder berubah.

## 6. Jalur pemakai lanjutan di DATA.BIN entry 1: temuan bersyarat, belum runtime

Pada view Ghidra hipotetis entry 1, analisis menempatkan pemanggil langsung `JAL 0x80013B10` di `0x800DD2B4` dan `0x800DD4CC`, dalam konteks fungsi yang dipetakan sebagai `FUN_800dcfec`. Keluaran teks `field-offset-scan.txt` juga mengandung panggilan serupa dalam konteks fungsi lain (misalnya sekitar `FUN_800f7824` dan blok di sekitar `0x8011C268`).

Di dekompilasi `FUN_800dcfec`, jalur bercabang melakukan hal-hal berikut (ini adalah uraian operasi dekompilasi, bukan penamaan fitur):

1. Memeriksa flag bit `0x200` pada word/halfword di record ber-stride `0x90), membandingkan byte `+0x1F` antarrecord, serta memeriksa bit pada `+0x0D`.
2. Di cabang yang memeriksa byte pada `+0x10+i` sama dengan `0x15` atau `0x14`, memanggil `0x80013B10` dan membaca kembali slot 0, 1, 2 via `0x800139FC`.
3. Menulis tiga hasil baca ke byte `+0x10), `+0x11), dan `+0x12) pada objek ber-stride `0x90), lalu mengubah sejumlah flag dan byte state (misalnya `+0x2E9` menjadi `0x23` pada satu cabang, atau `0x19` di cabang lain).

Ini memperlihatkan hubungan statis antara operasi ID pada empat record dan state/objek konsumen ber-stride 0x90. Tetapi disassembler/decompiler secara eksplisit memperingatkan `Control flow encountered bad instruction data` dan memangkas beberapa jalur dengan `halt_baddata()`. Base pointer resource di slot `0x8013EA74` serta base entry-1 `0x800D0000` belum divalidasi pada runtime. Karena itu belum sah menyatakan kondisi-kondisi tersebut merupakan “memilih karakter”, “bertarung”, “menguasai wilayah”, atau transisi permainan tertentu.

## 7. Matriks pembuktian untuk temuan ini

| Klaim | Kondisi pemicu | Perubahan state teramati secara statis | Efek gameplay | Keyakinan |
|---|---|---|---|---|
| Registry menetapkan batas ID 0–51 | Enumerasi tabel berhenti pada sentinel di indeks 52 | Count disimpan di `0x118($gp)`, diakses lewat `0x800154D4` | Nama dan peran ID belum diketahui | **TERVERIFIKASI-STATIS** |
| Record memiliki tiga slot ID | Grup <4 dan slot <3 | Byte pada offset +0xA..+0xC record stride 0xB4 | Peran record belum diketahui | **TERVERIFIKASI-STATIS** |
| Tambah memilih slot invalid pertama | ID valid dan setidaknya satu slot bernilai >=52 | Menulis ID ke slot itu | Efek yang terlihat pemain belum diketahui | **TERVERIFIKASI-STATIS** |
| Hapus memindahkan ID sebelum merapatkan record | Argumen grup/slot berada dalam rentang | ID lama dikirim ke sisip acak; slot record dirapatkan; tail disetel FF | Makna “memindahkan” dalam gameplay belum diketahui | **TERVERIFIKASI-STATIS** untuk operasi lokal |
| Posisi sisip memakai RNG dan separuh belakang | ID valid dan panjang n >=2 | Perhitungan posisi, shift buffer, penulisan ID dan counter terpisah | Tidak diketahui apakah ini urutan pilihan, resource, atau mekanik lain | **TERVERIFIKASI-STATIS** untuk operasi; semantik **UNKNOWN** |
| Consumer DATA.BIN menghubungkan operasi ID dengan field state lain | Cabang consumer dengan byte `0x14/0x15` atau kondisi sekitar lain | Memanggil remover, membaca kembali tiga ID, menulis ke +0x10..+0x12 serta mengubah beberapa byte state | Belum terhubung ke efek visual/hasil permainan; base/pointer tidak validasi runtime | **KUAT BERSYARAT**, semantik **UNKNOWN** |

## 8. Gap dan langkah terkecil berikutnya

1. **Identitas ID:** temukan data atau resource teks yang memetakan record registry ke label/nama yang dapat dikonfirmasi; jangan menyimpulkan dari angka atau struktur 16-byte saja.
2. **Arti buffer:** cari caller dan consumer tambahan untuk `0x80070C80+0x8A`, `0x80070C82`, `0x80070C86`, D02/D04 dan D06/D08, terutama cabang yang membaca hasil getter setelah perubahan.
3. **Konfirmasi consumer lintas resource:** validasi mapping entry 1/pointer global lewat sumber statis loader-relocation atau bukti runtime baru yang berbeda dari probe lama. Jangan mengulang probe `0x800AD454` tanpa hipotesis reachability baru.
4. **RNG:** boundary `0x80015B7C` harus dibaca dari return raw MIPS `0x80015C64` plus delay slot `0x80015C68`; deklarasi `nonmatching ... 0x580` terlalu lebar. Resolusi call tidak langsung/JALR masih dibutuhkan untuk cakupan yang lebih luas.
5. **Efek game:** bila kemudian ada eksperimen runtime yang layak, ubah satu kondisi saja dan catat input, kondisi awal, state sebelum/sesudah, serta screenshot autentik emulator. Jangan menggunakan checkpoint restore yang telah dua kali gagal dengan representasi state yang sama.

Status Step 4 tetap **SEBAGIAN**, Step 5 tetap **SEBAGIAN**, Step 6 tetap **SEBAGIAN** (6b **BLOCKED**), Step 7 tetap **SEBAGIAN/BLOCKED** sesuai subkriteria, dan Step 8(b) tetap **UNKNOWN**. Tidak ada status audit yang dinaikkan oleh laporan ini. Story Mode **TIDAK TERBUKTI TAMAT**. Adaptive player tidak dijalankan atau diubah; gate `barrier_level_selection=WAIT` tetap dipertahankan.


## 9. Registry row fields: numeric properties and one downstream effect

A separate raw-MIPS cross-check shows that the 52-row table is not only used as a validity bound. Four bounded accessor entrypoints index the record by `ID * 0x10` and read individual 32-bit fields:

| Accessor entry | Word read | Invalid-ID fallback | What is proven |
|---|---:|---:|---|
| `0x800154E0` | `record + 0x00` | `0xFFFFFFFF` | Numeric field read; caller uses it in branch/discriminator comparisons in candidate resource code. |
| `0x80015578` | `record + 0x04` | `0xFFFFFFFF` | Second numeric field can be retrieved; its gameplay meaning is UNKNOWN. |
| `0x8001552C` | `record + 0x08` | `0` | Signed-looking numeric field is consumed in arithmetic in candidate resource code. |
| `0x800155C4` | `record + 0x0C` | `0xFFFFFFFF` | Fourth numeric field can be retrieved; its role is UNKNOWN. |

The entries in `0x80055CEC` are four 32-bit words each, not text/name records. In the raw table view, field +0 contains integer codes such as 0, 1, 3–10, 12–15; field +4 contains 0, 1, or 2; field +8 contains signed or positive numeric values from -50 up to 500; field +0xC increases monotonically from `0xEF` (239) at ID 0 to `0x122` (290) at ID 51. The last field could be an index-like value, but no consumer has yet proven whether it is a resource, animation, lookup-table index, or another number. **Do not assign semantic names to these four fields yet.**

Representative exact row values (decimal unless hex is marked):

| Registry ID | +0 | +4 | +8 | +0xC |
|---:|---:|---:|---:|---:|
| 0 | 0 | 1 | 150 | 239 (`0xEF`) |
| 5 | 0 | 1 | -50 (raw `0xFFFFFFCE`) | 244 (`0xF4`) |
| 10 | 6 | 1 | 0 | 249 (`0xF9`) |
| 20 | 12 | 0 | 0 | 259 (`0x103`) |
| 30 | 15 | 2 | 2 | 269 (`0x10D`) |
| 37 | 0 | 1 | 500 (`0x1F4`) | 276 (`0x114`) |
| 51 | 5 | 2 | 7 | 290 (`0x122`) |

### Provenance from a candidate consumer

In the DATA.BIN entry-1 decompilation view (base `0x800D0000`, still a hypothesis), routine `FUN_80115728` calls accessor `0x8001552C` using the 32-bit value at object offset `+0x530) as its index. In one branch, the returned field +8 is multiplied by `(group_count - 2)` and written to a group-indexed halfword at object base +`0x2EE + group*2`; if the signed result is negative, that group's byte at +`0x22` is set to 2 and the code calls `FUN_800f2d5c`, otherwise it sets the byte to 5 and calls the same continuation. Other branches store the negated field value or another scaled form and route to separate continuation functions based on the sign. This is a direct static link from a registry numeric field to a state field and control-flow choice in the candidate resource view.

This still does **not** tell us the player-facing meaning of that numeric value or the +0x2EE/+0x22 fields. The imported resource base and pointer source remain unverified, and the decompiler output has malformed-control-flow warnings. Therefore this linkage is **KUAT BERSYARAT**, not a verified gameplay rule.

### Read/write coverage update

- `0x800157C4` returns the byte at `0x80070C80 + 0x8A + cursor`, with cursor from halfword `0x80070C86`; this entrypoint does not visibly bounds-check the cursor.
- `0x80015808` checks index < the first-list length returned by `0x800158D8` (which reads the low byte of D02), then returns byte from `0x80070C80 + 0x8A + index`; otherwise it returns `0xFF`.
- `0x80015858` uses the same first-list-length bound and checks value <52 before writing to `0x80070C80 + 0x8A + index`.
- No direct JAL to `0x80013A48` appears in the available full main-EXE text disassembly. Its static body is understood locally, but its caller/reachability is still UNKNOWN in this evidence set; it may be called from resource/indirect code, which is not yet proven.

These additional accesses strengthen the static ID-to-numeric-field chain, but the report's status matrix and game-mechanic labels remain unchanged.


## 10. Newly reopened DATA.BIN entry-1 artifact: list byte → registry dispatch → state fields

The existing raw disassembly artifact was downloaded from Actions run [#40523020556](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40523020556), artifact [#12742268706](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40523020556/artifacts/12742268706). Local ZIP SHA-256 matched the API digest: `5f3f767667444f7c956c36fc59cf75b6bb90a5a1dde8ddb92fb69f9e0f797e81`. Its `DATA_BIN_ENTRY_0001_800D0000.text.s` is raw static disassembly text for the 596,412-byte entry-1 slice. Base `0x800D0000` remains hypothetical; this is not a runtime observation.

### 10.1 Sequence consumption and ID storage

At `0x8010F3DC` and `0x8010F400), code calls `0x80015768`. That main-EXE helper:
1. saves byte `0x80070D0A` before mutation;
2. calls `0x800158E8(0,0)` to shift the first sequence left and decrement the separate counter `0x80070C82`;
3. calls `0x80015B7C(0)` to perform its bounded RNG swaps over the configured first-list length;
4. returns the saved byte.

In the surrounding entry-1 sequence, the returned byte is also saved at stack offset `+0x18), masked to a byte, and written as a 32-bit value to the object reached through global pointer slot `0x8013EA74` at object offset `+0x530). This establishes a static dataflow from the first byte of the configured sequence into an object field. The pointer value and the object's player-facing meaning remain unknown.

A related branch at `0x8010F1D4–0x8010F288) calls `0x800157E4` for indices 0, 1, and 2, passes the three returned list bytes to `0x800C7574` along with the current selector, stores that helper's result in `0x8013EBB0), and copies the three bytes from object offsets +0x10..+0x12 to +0x4E0..+0x4E2. This proves another consumer of the sequence bytes, but the helper's output semantics are unknown.

### 10.2 Registry category dispatch and numeric effect

When the branch has `D_80139EC7 == 0) and `0x8010D0F0()` returns zero, the returned ID is passed to `0x800154E0`, which reads registry field +0. Values below 16 index a jump table at `jtbl_800AE900`. The table bytes themselves are not part of the entry-1 slice, so individual category-to-destination mappings cannot yet be reconstructed from this artifact alone.

Two branch destinations independently show the registry field +8 affects state:

- Near `0x8010F464), the code obtains the same ID's field +8 through `0x8001552C`, stores the result in object +0x4F4, tests its sign, and sets object byte +0x534 to 1 on the negative branch or clears it on the nonnegative branch.
- Near `0x8010F4E4), another path obtains field +8, writes it to object +0x4F0 and +0x4F4, and again branches on sign to set/clear +0x534.

Thus a bounded sequence byte becomes an ID, its registry +0 field chooses a dispatch branch, and at least some branches use registry +8 to change numeric object fields and a separate status byte. The exact meaning of +0x4F0/+0x4F4/+0x534 and the visible gameplay consequence remain **UNKNOWN**. The imported resource base/global pointer and dispatch-table contents remain unverified.

A separate path at `0x80115708–0x801158AC) uses the same field +8 in signed arithmetic: it multiplies the value by `(byte[0x8013EA71] - 2)`, stores the result in a group-indexed halfword at object +0x2EE, and tests the sign; the branches write 2 or 5 to a byte at +0x22 and route to different continuation functions. This adds a second static link from registry numeric attributes to control flow and object state, but not a verified player-facing rule.

### 10.3 Direct resource callers now visible

The same entry-1 raw disassembly contains decoded direct calls to the main-EXE slot helpers under the assumed base map:

- `0x80013A48` (add ID to first invalid slot): call sites `0x8010F8EC`, `0x8010F908`, and `0x801107A8`.
- `0x80013B10` (remove/transfer selected slot): call sites `0x800D7104`, `0x800DD19C`, `0x800DD2B4`, `0x800DD4CC`, `0x800F78AC`, `0x800FA3D4`, `0x800FAA2C`, and `0x80110798`.

These references narrow the earlier gap: the functions are **directly called by decoded instructions in the candidate resource disassembly**, rather than merely hypothesized as possible external consumers. Their actual reachability at runtime remains unverified because the resource base/relocation/pointer provenance has not closed. Some decompiler paths also report malformed control-flow/instruction data.

### 10.4 Updated interpretation and evidence limits

The strongest supported sequence is now:

`configured list byte → pop/shift/reshuffle helper → ID stored at object +0x530 → registry field +0 dispatch → field +8 arithmetic → object fields +0x4F0/+0x4F4/+0x534 or +0x2EE/+0x22`.

Separately, resource code invokes add/remove helpers on the four-record, three-slot ID collection. This proves a connected **static data/control-flow mechanism**, stronger than an isolated byte-shift observation. It still does not identify the feature as a card, character, move, turn, tile, battle action, or victory/loss rule. No emulator/gameplay input was used and no runtime value was captured. Step 4 stays **SEBAGIAN**; Step 6(b) stays **BLOCKED**; Step 7 runtime mapping stays **UNKNOWN/BLOCKED**; Step 8(b) stays **UNKNOWN**.


## 11. Jump-table hypothesis test: the candidate address collides with instruction-like bytes in entry 0

To test whether the referenced `jtbl_800AE900` could be the expected 16-word dispatch table in DATA.BIN entry 0, the existing entry0-only context workflow was extended with a bounded raw-memory dump (no whole-program analysis and no code execution). The run completed successfully:

- Actions run [#40619049176](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40619049176), artifact [#12786995206](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40619049176/artifacts/12786995206).
- ZIP SHA-256: `01067b46e0a6e15cebd06d4bcd9898ff946d8c1d4083d40a29b80480fca92dc9` (matches GitHub API digest).
- Dumped region: `0x800AE900..0x800AE93F`, 64 bytes, in the imported `DATA_BIN_ENTRY_0000` block under the **hypothetical** base `0x800AD000`. Table-byte SHA-256: `0b5987d2a6307848ab55e87b23f0771fe6afdc345f8c42ede9bfa92eb5ab005b`.
- The 16 words are `000217C2, 00A21021, 00021043, 2442FEF8, 00629823, AFA50010, 0C008450, 248446D0, 14400081, 2402001F, A622000C, A6200010, 240201FF, A6220012, 0C00DC4E, 2404FFFF`. They decode as a sequence of ordinary MIPS instruction forms (SRL, ADDU, SRA, ADDIU, SUBU, SW, JAL, ADDIU, BNE, ADDIU, SH, SH, ADDIU, SH, JAL, ADDIU), not as 16 plausible absolute code addresses. The JAL words themselves resolve to `0x80021140` and `0x80037138` under MIPS decoding.
- The dump is from a text-only artifact. No binary resource is published; the runner removed the extracted private resource after the job.

### What this proves—and what it does not

This **rejects the specific assumption** that, when entry 0 is mapped contiguously at `0x800AD000`, its bytes at offset `0x1900` are the 16-pointer table referenced by entry-1 code. Those bytes are instruction-like instead. It does not prove whether entry 0 is actually loaded at that base during the entry-1 path, whether another resource is mapped at `0x800AE900` at that time, or whether the entry-1 pointer requires a mapping/relocation interpretation not captured by the present view.

The entry-1 sequence at `0x8010F444–0x8010F45C` does statically compute `0x800AE900 + 4*field0`, load one word, and branch through it for field0 <16. The **address use is verified in static instructions**; table ownership and runtime targets remain **UNKNOWN/BLOCKED**. Do not label the 16 category cases, and do not promote Step 6(b) or Step 7 runtime mapping based on this test. The new next step is to trace loader/relocation logic that explains which resource owns `0x800AE900` when this entry-1 dispatch runs.


## 12. Cross-resource pointer evidence sharpens the address conflict

The same entry-1 raw disassembly begins with six aligned 32-bit words at assumed addresses `0x800D0128..0x800D013C`:

| Entry-1 address | Raw word | Absolute value |
|---|---:|---:|
| `0x800D0128` | `0x800AD454` | `0x800AD454` |
| `0x800D012C` | `0x800AD45C` | `0x800AD45C` |
| `0x800D0130` | `0x800AD464` | `0x800AD464` |
| `0x800D0134` | `0x800AD46C` | `0x800AD46C` |
| `0x800D0138` | `0x800AD478` | `0x800AD478` |
| `0x800D013C` | `0x800AD484` | `0x800AD484` |

These are address-shaped constants packed consecutively in the entry-1 prefix, consistent with a candidate function-address array, but the consumer of this six-word group has not yet been proven. Independently, main-EXE code at `0x800115DC` directly calls `0x800AD454` during the bootstrap/initialization path. The entry0 targeted artifact decoded that same address as a candidate function entry under base `0x800AD000`.

Together with the instruction-like bytes observed at entry0 offset +`0x1900` (numeric address `0x800AE900`), this means the present mapping hypotheses cannot safely be combined into one confirmed runtime memory map: entry1 statically refers to functions around `0x800AD454`, but its dispatch at `0x8010F444` also expects pointer words at `0x800AE900), where the entry0 candidate view contains code-like words. Possible explanations include overlay replacement/lifecycle, relocated or patched module data, a different runtime base, or a different resource owning the dispatch table. The current static artifacts do not choose between these explanations.

**Next evidence required:** recover the loader/relocation/copy rule that determines what occupies `0x800AD000..` at the time the entry1 branch runs, and prove whether the six entry1 constants are relocated or consumed. Keep this as **UNKNOWN/BLOCKED**; neither table ownership nor runtime reachability is promoted.


## 13. Full 52-row registry distribution cross-check

Using the complete raw MIPS table listing at `D_80055CEC` in the existing main-EXE text artifact (52 records before sentinel `0xFFFFFFFF` at `0x8005602C`), I parsed all 52 four-word rows and checked each field rather than relying on examples only.

| Field offset | Exact observed distribution in all 52 rows | Safe interpretation |
|---|---|---|
| +0 | Code 0: 14 rows; 1: 1; 3: 2; 4: 4; 5: 14; 6: 5; 7: 1; 8: 1; 9: 3; 10: 1; 12: 2; 13: 2; 14: 1; 15: 1. Codes 2 and 11 do not occur. | Small discriminator/category-like code; caller branches on it and the entry1 path bounds it to <16, but case meanings unknown. |
| +4 | 0: 7 rows; 1: 26; 2: 19. | Small enumerated field; semantic label unknown. |
| +8 | Unique values: -50, -30, -25, 0, 1–7, 25, 50, 75, 100, 150, 200, 250, 350, 400, 500. | Signed numeric parameter; multiple consumers use its sign and/or multiply it into state. It is not safe to name this “cost”, “power”, or any specific stat yet. |
| +0xC | Every one of the 52 rows satisfies `field_+0xC = registry_ID + 239`; IDs 0..51 map to 239..290. | Exact derived sequential code, but the field's consumer/meaning remains unknown. Do not call it a resource/animation index without proof. |

This makes the dispatch relationship sharper but not semantically complete: +0 holds one of 14 observed category-like codes (all in 0..15), fitting the caller's `<16` jump-table guard; the table's real runtime contents and owners remain unresolved due to the mapping conflict in sections 11–12. The full-distribution counts are static facts from the existing main-EXE text artifact. No game binary was downloaded again for this calculation.
