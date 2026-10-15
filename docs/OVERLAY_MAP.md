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
| DATA.BIN | Bootstrap 0x44 byte diikuti direktori 0x2F00 byte berisi 1.504 entri resource (LBN, panjang byte); isi resource mencakup kode dan aset | Direktori resource didukung bukti langsung; format resource individual dan seluruh alamat muat masih belum dipetakan |
| DATA2.BIN | File besar dalam filesystem ISO | Format, segmentasi kode/data, dan loader belum dipastikan |
| DUMMY.BIN | File besar dalam filesystem ISO | Tujuan dan kemungkinan penggunaan runtime belum dipastikan |
| XASECT.BIN | File kecil 692 byte | Format dan hubungan dengan loader belum dipastikan |

Analisis byte-level lanjutan memperkuat hubungan bootstrap DATA.BIN dengan alamat sekitar 0x800AD450: rutin pada offset file DATA.BIN +0x04 berada di sekitar 0x800AD454 dan menyalin direktori +0x44 berukuran 0x2F00 ke RAM 0x8006D830. Ini menunjukkan pemetaan untuk blok bootstrap/direktori tersebut, tetapi **tidak berarti seluruh DATA.BIN dimuat sebagai satu overlay kontigu**. Alamat muat dan lifecycle resource lain tetap perlu dipetakan.

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

1. Reverse-engineer format resource yang sudah terindeks oleh direktori DATA.BIN, terutama PK02/BIN0/TPK0 dan NARUTOSceneV001; lanjutkan struktur internal DATA2.BIN.
2. Temukan rutin loader pada executable utama; telusuri pemanggilan CD-ROM, alokasi RAM, dan transfer data.
3. Buat tabel untuk setiap modul: offset file, ukuran file/payload, alamat tujuan, ukuran di RAM, entry point, relokasi, pemicu load, dan kemungkinan alamat tumpang tindih.
4. Kaitkan setiap call/jump dari executable dan overlay ke identitas modul pada waktu panggilan.
5. Verifikasi dengan debugger: breakpoint di titik loader, catat rentang RAM sebelum/sesudah load, lalu bandingkan hash byte overlay dengan payload file.
6. Hanya setelah mapping benar, tetapkan nama fungsi dan rangkaian call chain untuk aturan gameplay.

## Direktori resource DATA.BIN — hasil byte-level 2026-10-15

Temuan berikut menggantikan status sebelumnya yang menganggap keberadaan tabel resource masih sekadar dugaan:

1. Pada executable `SLPS_035.53`, file offset `0x46098` (RAM `0x80055898`) tersimpan pasangan little-endian `0x000000D4, 0x00002F44`. Nilai pertama adalah LBN 212, tepat extent ISO dari `DATA.BIN`; nilai kedua 12.100 byte.
2. Bootstrap yang ditunjuk pasangan tersebut mempunyai ukuran `0x2F44). `DATA.BIN` offset `0x00–0x43` berisi kode bootstrap; mulai offset `0x44` terdapat tabel sebesar `0x2F00) byte.
3. Tabel berisi 1.504 entri berukuran 8 byte. Interpretasi paling kuat untuk setiap entri ialah dua uint32 little-endian: LBN CD dan panjang data dalam byte. Kode mengonversi panjang menjadi jumlah sektor dengan pembulatan ke atas pada batas `0x800) byte.
4. Kode di sekitar `0x800AD454` menyalin `0x2F00) byte dari `0x800AD494` ke alamat `0x8006D830), konsisten dengan menyalin tabel dari offset `+0x44) bootstrap. Lokasi pemanggilan di executable menyetel alamat tujuan pada delay slot.
5. Dari 1.504 entri, 1.500 aktif dan empat berukuran nol (indeks 1491–1494). Interval sektor entri aktif tidak saling tumpang-tindih dan berada di dalam extent `DATA.BIN` pada LBN [212, 32446). Total interval yang tercakup adalah 32.227 sektor dari 32.234 sektor file. Tujuh sektor selisih cocok dengan enam sektor bootstrap yang dibulatkan dan satu sektor akhir yang tidak tercakup.

Ini memberikan keyakinan **tinggi** bahwa executable memakai bootstrap DATA.BIN untuk mendaftarkan direktori resource berbasis LBN/panjang. Ini belum mengidentifikasi format setiap resource atau seluruh pemuatan runtime. Detail signature dan hash tercatat di [RESOURCE_CATALOG.md](RESOURCE_CATALOG.md).
