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
