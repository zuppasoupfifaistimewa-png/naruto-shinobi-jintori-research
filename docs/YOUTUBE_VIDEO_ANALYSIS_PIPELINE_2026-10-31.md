# Rencana pipeline analisis video YouTube — 31 Oktober 2026

## Tujuan
Menganalisis video gameplay Naruto – Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553) dari tautan publik, lalu menghasilkan indeks adegan, bukti visual bertimestamp, transkripsi audio bila tersedia, dan laporan aturan permainan dengan label TERverifikasi/HIPOTESIS/UNKNOWN.

Sumber awal:
- URL: https://www.youtube.com/watch?v=r30Rs_NuExc
- Kanal yang teridentifikasi dari halaman playlist: Kevin Tedja.
- Judul yang teridentifikasi: "INILAH GAME NARUTO MONOPOLI PS 1 PRASEJARAH! - Naruto: Shinobi no Sato no Jintori Kassen Indonesia".
- Durasi yang teridentifikasi pada playlist: 2:53:15.
- Catatan: metadata halaman bukan bukti bahwa isi video telah ditonton atau dianalisis.

## Status akses saat perencanaan
- Halaman playlist YouTube dapat dibaca melalui browser terhubung.
- Pemutar untuk video ini gagal dimuat pada sesi ChatGPT: posisi tetap 0:00 / NaN; closed captions dilaporkan tidak tersedia.
- Pembukaan URL langsung melalui pencarian web menghasilkan cache miss.
- Karena itu, belum ada frame, audio, subtitle, atau isi gameplay dari video ini yang berhasil diperoleh. Jangan menyatakan video telah ditonton.

## Batasan penting
1. Jangan mengunduh atau mengekstrak salinan video YouTube melalui cara yang melanggar ketentuan platform atau hak pemilik konten. Prioritaskan player/embed resmi, caption/transcript yang disediakan secara sah, API resmi untuk metadata, atau file rekaman yang pemiliknya berwenang membagikan.
2. Tautan YouTube saja tidak menjamin akses ke stream audiovisual. API metadata dan hasil pencarian tidak sama dengan akses frame/audio.
3. Jangan menyimpan salinan video penuh, audio, frame privat, ROM, BIOS, Memory Card, savestate, atau dump RAM ke repo.
4. Jika penggunaan frame dibutuhkan untuk bukti internal, simpan hanya metadata timestamp, hash, dan ringkasan teks; bukti visual privat tetap di luar repo kecuali ada izin eksplisit dan kebijakan repo yang mengizinkan.
5. Jangan membuat klaim aturan game dari judul/deskripsi/thumbnail. Hanya dari pengamatan langsung yang dapat diulang dan diverifikasi.

## Arsitektur yang disarankan
### Tahap A — pemeriksaan sumber
- Normalisasi URL dan catat video ID.
- Periksa metadata publik via jalur resmi.
- Periksa apakah captions/transcript tersedia melalui antarmuka resmi atau endpoint yang diizinkan.
- Periksa apakah player resmi dapat diputar pada lingkungan browser yang berwenang.
- Catat status akses: METADATA_ONLY / CAPTIONS_ONLY / PLAYER_ACCESSIBLE / BLOCKED.

### Tahap B — pengumpulan bukti audiovisual yang diizinkan
- Jika player resmi dapat diakses, lakukan inspeksi pada rentang waktu terpilih dan catat timestamp.
- Jika pemilik menyediakan file rekaman atau izin pemrosesan, gunakan file itu sebagai input lokal/runner; jangan mengunggahnya ke repo.
- Sampling frame harus adaptif (perubahan adegan/UI/input), bukan menganggap satu frame per interval cukup untuk semua mekanisme.
- Audio diproses hanya jika tersedia dan diizinkan; jangan mengarang transkrip.

### Tahap C — ekstraksi gameplay
- Buat event timeline: timestamp, layar/phase, aktor, input yang terlihat, respons visual/audio, state sebelum/sesudah, tingkat keyakinan.
- Identifikasi menu, giliran, gerakan papan, Chakra, kartu/roulette, perangkap, barrier, battle, hasil giliran, kemenangan/kekalahan.
- Terjemahkan teks Jepang berdampingan dengan teks asli; tandai bacaan yang belum pasti.
- Bedakan observasi langsung dari interpretasi.

### Tahap D — verifikasi dan laporan
- Setiap aturan memiliki bukti timestamp dan minimal satu observasi pembanding bila memungkinkan.
- Label: VERIFIED (pengamatan langsung cukup), HYPOTHESIS (penjelasan sementara), UNKNOWN (bukti tidak cukup).
- Jangan menyimpulkan perilaku AI atau rumus internal hanya dari satu playthrough.
- Hasil Actions harus mempublikasikan ringkasan teks pendek: status, job, source SHA, kode keluar, serta tautan raw permalink dengan SHA penuh.
- Bersihkan semua aset sementara setelah pemrosesan; validasi artefak text-only.

## Tahapan implementasi
1. Audit workflow dan dependensi Actions yang sudah ada agar tidak menduplikasi sistem.
2. Buat pemeriksa akses YouTube yang hanya memakai sumber resmi/diizinkan dan mengembalikan status akses serta metadata.
3. Tambahkan jalur captions/transcript bila tersedia secara sah.
4. Tambahkan jalur analisis frame/audio hanya setelah metode akses player/file input dipastikan sah dan dapat direproduksi.
5. Uji dengan fixture sintetis kecil; jangan menjalankan gameplay emulator atau adaptive player sebagai bagian dari pipeline video.
6. Jalankan video sumber hanya jika tahap pemeriksaan akses membuktikan jalur yang diizinkan dan batasan ukuran/biaya sudah jelas.

## Status pekerjaan
- Perencanaan awal: SELESAI.
- Pemeriksaan isi video: BLOCKED; pemutar gagal dimuat dan captions tidak tersedia.
- Frame/audio extraction: BELUM DIMULAI.
- Analisis gameplay video: BELUM DIMULAI.
- GitHub Actions pipeline: BELUM DIIMPLEMENTASIKAN.
- Story Mode completion: tidak terkait dengan tugas ini dan tetap belum terbukti tamat.

## Checkpoint
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Base commit saat rencana dibuat: 17a83a587031328d841c80bc4b7273efc376e6a0
