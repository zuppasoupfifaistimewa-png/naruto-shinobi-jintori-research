# Peta loader, modul, dan overlay — status sementara

## Ringkasan

Peta loader/overlay **belum lengkap**. Bagian ini menyimpan titik awal yang ditemukan agar analisis berikutnya dapat dilanjutkan tanpa menganggap alamat statis sebagai pemetaan runtime final.

## Executable utama

- File: SLPS_035.53
- RAM load address: 0x80010000
- Entry PC dari header: 0x80011448
- Text size: 0x5D800
- Format: PS-X EXE

Ini merupakan referensi alamat paling kuat saat ini karena berasal dari header executable.

## Modul data

| File | Observasi | Status |
|---|---|---|
| DATA.BIN | Berisi sejumlah blok yang disassemble sebagai instruksi MIPS, termasuk rutin yang merujuk fungsi executable utama | Belum diketahui peta offset ↔ alamat runtime lengkap |
| DATA2.BIN | File besar dalam filesystem ISO | Format, segmentasi kode/data, dan loader belum dipastikan |
| DUMMY.BIN | File besar dalam filesystem ISO | Tujuan dan kemungkinan penggunaan runtime belum dipastikan |
| XASECT.BIN | File kecil 692 byte | Format dan hubungan dengan loader belum dipastikan |

Pada analisis terdahulu, call dari executable utama menuju alamat sekitar 0x800AD454 terlihat cocok dengan dugaan bahwa suatu blok kode di DATA.BIN dimuat pada rentang tersebut. Ini **indikasi pemetaan awal, bukan peta overlay tervalidasi**. Offset file tepat, ukuran modul saat dimuat, entry point, dan mekanisme relokasi belum dipastikan.

## Lokasi kode yang telah dicatat

Alamat berikut merupakan label kerja dari pembacaan/disassembly terdahulu. Alamat harus dipetakan kembali ke modul yang aktif sebelum dijadikan dasar edit, patch, atau kesimpulan formula.

| Alamat/rentang kerja | Fungsi/perilaku yang diamati | Kepastian |
|---|---|---|
| 0x80012A70 | Jalur getter nilai terkait konfigurasi/pemain pada catatan sebelumnya; perlu konfirmasi konteks lengkap | Menengah |
| 0x8001387C–0x800138E8 | Setter/pembatas nilai Chakra dan jalur terkait | Tinggi untuk rentang batas yang diamati |
| 0x800138EC, 0x80013918 | Fungsi akses data pemain yang dipakai pada analisis struktur | Menengah–tinggi |
| 0x800B1D90 | Rutin pemrosesan atribut/field petak | Menengah |
| 0x800DB114–0x800DB194 | Cabang pemeriksaan akhir yang dalam jalur tertentu menyimpan ID pemenang 0xFF | Menengah; label kondisi belum final |
| 0x800DB1A0–0x800DB280 | Pemeriksaan nilai negatif/status pemain dan transisi kondisi | Menengah; dampak aturan belum final |
| 0x800EC200–0x800EC280 | Jalur kondisi yang membandingkan Chakra pemain dengan target dan dapat menetapkan pemenang | Menengah–tinggi |
| 0x800EC284–0x800EC5FC | Cabang tambahan pemeriksaan kondisi akhir | Menengah untuk adanya percabangan; mapping nama kondisi belum final |
| sekitar 0x800F70D0 | Jalur aritmetika Chakra dengan pembalikan tanda dan batas bawah | Menengah; konteks pemicu/aksi perlu dipetakan |

**Penting:** daftar alamat di atas diwariskan dari catatan disassembly terdahulu dan belum dibangun ulang dengan pemetaan overlay menyeluruh dalam sesi terbaru. Jangan menafsirkan dua rutinitas di alamat serupa sebagai modul yang sama sebelum memastikan overlay yang aktif.

## Data konfigurasi akhir pertandingan

Analisis terdahulu menemukan record konfigurasi dengan nilai yang dibaca melalui offset record berikut:

- +0x04: 1500
- +0x08: 3000
- +0x0C: 400

Jalur pemeriksaan target memakai nilai 3000. Makna 1500 dan 400 belum ditelusuri penuh sampai ke proses inisialisasi dan seluruh pemanggil. Lokasi offset file record, ukuran record, jumlah record, serta pemetaan record ke semua mode belum terdokumentasi lengkap.

## Rencana melengkapi peta overlay

1. Identifikasi format container DATA.BIN/DATA2.BIN dan seluruh header/resource directory.
2. Temukan rutin loader pada executable utama; telusuri pemanggilan CD-ROM, alokasi RAM, dan transfer data.
3. Buat tabel untuk setiap modul: offset file, ukuran file/payload, alamat tujuan, ukuran di RAM, entry point, relokasi, pemicu load, dan kemungkinan alamat tumpang tindih.
4. Kaitkan setiap call/jump dari executable dan overlay ke identitas modul pada waktu panggilan.
5. Verifikasi dengan debugger: breakpoint di titik loader, catat rentang RAM sebelum/sesudah load, lalu bandingkan hash byte overlay dengan payload file.
6. Hanya setelah mapping benar, tetapkan nama fungsi dan rangkaian call chain untuk aturan gameplay.