# Log analisis dan handoff

Tanggal ringkasan: 2026-10-15

Catatan ini merangkum pekerjaan yang sudah dijalankan dan batasannya agar sesi/agen berikutnya dapat melanjutkan tanpa mengulang asumsi.

## Pemeriksaan file

- File yang dianalisis: Naruto - Shinobi no Sato no Jintori Gassen (Japan).bin.
- Ukuran file: 325.989.552 byte.
- Format yang terdeteksi: PS1 raw sector, stride 2352 byte, 138.601 sektor.
- Payload diekstrak sementara untuk membangun ISO dan membaca filesystem; file asli tidak diubah.
- Serial disc: SLPS-03553.
- CRC32: dfe1f8b3.
- SHA-256: 58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88.
- ISO memuat DATA.BIN, DATA2.BIN, DUMMY.BIN, SLPS_035.53, SYSTEM.CNF, XASECT.BIN; ukuran lengkap tercatat di docs/ROM_STRUCTURE.md.
- SYSTEM.CNF menunjuk ke SLPS_035.53; executable utama header-memuat base 0x80010000, PC 0x80011448, text size 0x5D800.

## Analisis kode statis

- Disassembly awal mengindikasikan instruksi MIPS R3000A di executable utama dan beberapa blok DATA.BIN.
- Tidak ditemukan teks aturan kunci sebagai string Shift-JIS literal biasa di file yang diekstrak pada pencarian awal. Struktur string/resource perlu dipetakan lebih lanjut.
- Struktur pemain yang digunakan beberapa rutin memiliki empat slot, stride 0xB4 byte, field Chakra pada offset +0x18.
- Setter Chakra membatasi rentang ke -9.999 sampai 99.999.
- Target konfigurasi 3.000 ditemukan dan dipakai oleh cabang pemeriksaan target pada jalur akhir pertandingan yang ditelusuri.
- Field kepemilikan petak diperiksa sebagai bagian bitfield, dengan empat bit teratas dipakai sebagai ID owner pada jalur yang diperiksa.
- Sejumlah alamat rutin dan flag akhir permainan masih merupakan label kerja; lihat docs/OVERLAY_MAP.md.

## Sumber gameplay sekunder yang diperiksa

- Transkripsi UI Story Mode dan kartu dari proyek terjemahan fan.
- Panduan Jepang yang menguraikan unlock dan opsi Party Mode.
- Materi promosi TV Tokyo.
- Ulasan gameplay Jepang tahun 2025.
- Data identitas disc dari GameGear Archive dan PSX Data Center.

Informasi eksternal digunakan untuk membuat hipotesis tentang makna kode, bukan menggantikan bukti runtime. Biaya 60/150 yang ditunjukkan oleh contoh UI tidak dinyatakan sebagai formula universal.

## Eksekusi runtime

- Dalam sesi terdahulu, emulator PS1 tidak ditemukan pada lingkungan eksekusi lokal.
- Upaya berikutnya untuk menjalankan terminal/Python ditolak oleh lingkungan, sehingga pemetaan overlay dan tes debugger tidak dapat dilanjutkan.
- GameGear Archive punya catatan pihak ketiga bahwa dump repack CHD boot pada Mednafen PSX HW selama uji otomatis 64 detik. Penelitian ini sendiri belum melaksanakan uji terkontrol terhadap barrier, battle, kartu, atau kondisi menang.

## Arahan untuk kelanjutan

1. Hormati CLAUDE.md: read-only secara default dan jangan melakukan perubahan tanpa instruksi eksplisit pemilik.
2. Jangan mengunggah file ROM/ISO, aset game, dump memori, atau save state ke repositori.
3. Mulai dari memetakan loader dan container DATA.BIN/DATA2.BIN sebelum menyimpulkan alamat fungsi overlay.
4. Uji aturan di emulator/debugger, lalu simpan log dan hasil secara teks/screenshot yang tidak mengandung aset berhak cipta yang tidak diperlukan.
5. Pelihara label confidence dan catat semua koreksi terhadap temuan lama.
6. Jangan pernah menyentuh repo Tile Duel dalam pekerjaan penelitian ini.