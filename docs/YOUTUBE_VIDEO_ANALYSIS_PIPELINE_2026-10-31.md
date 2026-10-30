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


## Addendum — implementasi Tahap A, 31 Oktober 2026

### Komponen yang ditambahkan
- tools/youtube_source_access_check.py: validasi URL YouTube, normalisasi video ID, dan permintaan metadata saja ke endpoint oEmbed publik YouTube. Tidak meminta stream, tidak memutar video, tidak mengunduh media.
- tests/test_youtube_source_access_check.py: sembilan tes offline untuk URL watch/short/embed, host dan ID invalid, klasifikasi respons, serta penegasan bahwa metadata bukan bukti playback.
- .github/workflows/youtube-source-access-check.yml: workflow manual dan otomatis pada perubahan file pemeriksa. Job menggunakan Python 3.12, menjalankan tes offline, meminta metadata oEmbed, lalu mengomit hanya laporan teks ke repo.
- Action versions: actions/checkout@v7 dan actions/setup-python@v7.1.0.

### Hasil GitHub Actions terverifikasi

| Run | Status | Job | Source SHA | Exit code |
|---|---|---|---|---:|
| 41139666002 | success | check-source (124350580342) | 2769a55f2b71bf227e9717a71900b21cf24685ea | 0 |
| 41139735708 | success | check-source (124350808562) | eff405eeef552cad4fab7e3c6eff0242c2cacd55 | 0 |

Kedua run menuntaskan 9/9 tes offline. Keduanya memperoleh METADATA_ONLY, HTTP 200, untuk video ID r30Rs_NuExc; metadata oEmbed yang dikembalikan menyebut judul INILAH GAME NARUTO MONOPOLI PS 1 PRASEJARAH! - Naruto: Shinobi no Sato no Jintori Kassen Indonesia dan kanal Kevin Tedja.

Laporan Actions terbaru dikomit pada 019414d9497dc7d15f3bb82032196257461b8c19:
reports/youtube_source_access/latest.md

Raw permalink laporan:
https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/019414d9497dc7d15f3bb82032196257461b8c19/reports/youtube_source_access/latest.md

### Batas hasil yang sudah terbukti
- VERIFIED: video ID tervalidasi; endpoint metadata oEmbed merespons HTTP 200; title dan channel metadata berhasil dibaca; workflow dan tes berhasil.
- UNKNOWN / NOT TESTED: apakah official player dapat memutar video pada runner; apakah captions tersedia; isi frame dan audio; urutan mekanisme gameplay; aturan papan, Chakra, giliran, battle, trap, maupun AI.
- METADATA_ONLY bukan status akses audiovisual. Jangan mengubah label ini menjadi PLAYER_ACCESSIBLE tanpa event playback resmi dari IFrame Player API.
- Tidak ada ROM, BIOS, Memory Card, savestate, dump RAM, file video/audio, screenshot privat, atau frame yang dikomit.

### Tahap berikutnya
1. Uji akses melalui YouTube IFrame Player API resmi, tanpa mengunduh stream atau menyimpan salinan media. Catat state event, current time, duration, serta kode error player. Dokumentasi: https://developers.google.com/youtube/iframe_api_reference
2. Periksa captions hanya melalui jalur resmi yang memang diizinkan. Keberadaan oEmbed tidak membuktikan captions.
3. Baru setelah player terbukti dapat diputar, evaluasi cara sampling frame yang diizinkan dan bagaimana hasil visual dapat diperiksa tanpa mengarsipkan media ke repo.
4. Jangan memulai analisis aturan game sampai frame/audio atau transkrip yang dapat ditinjau benar-benar tersedia.


## Addendum — VidIQ dan akses isi video, 31 Oktober 2026

### Status VidIQ
- Status instalasi VidIQ pada pemeriksaan konektor: installed=true.
- Tab VidIQ yang terbuka masih menampilkan layar sambutan dengan tombol Connect channel; koneksi kanal belum terbukti selesai.
- Belum ada transcript, visual analysis, frame, atau hasil analisis VidIQ yang diterima untuk video r30Rs_NuExc.
- Karena itu, keberadaan plugin terpasang tidak boleh ditafsirkan sebagai bukti bahwa konten video sudah dapat dibaca.

### Pemeriksaan tambahan
- Percobaan membuka URL YouTube secara langsung masih gagal dengan Cache miss.
- Pencarian publik menggunakan video ID dan judul video tidak mengembalikan transcript untuk video yang sama.
- Beberapa hasil pencarian membahas judul/video Naruto lain atau uraian umum game. Materi itu tidak dipakai sebagai pengganti rekaman sumber dan tidak boleh digunakan untuk mengklaim apa yang terjadi pada timestamp video ini.
- Tidak ada frame atau audio yang diambil pada checkpoint ini.

### Status akses terkini
- VERIFIED: metadata oEmbed HTTP 200 dan dua workflow metadata-check sukses; 9/9 tes offline pada masing-masing run.
- BLOCKED / PENDING: akses isi audiovisual dari video sumber belum terbukti.
- NOT STARTED: timeline gameplay dari video, identifikasi input yang terlihat, translasi dialog dari frame video, dan verifikasi aturan permainan dari video.
- VidIQ onboarding meminta koneksi kanal; perlu diselesaikan melalui tombol Connect channel di tab VidIQ. Jangan bagikan password atau token di chat.

### Langkah lanjut
1. Selesaikan koneksi kanal melalui alur resmi VidIQ di browser jika pengguna menyetujui izin akun yang diminta.
2. Setelah koneksi benar-benar aktif, jalankan transcript/visual analysis pada URL video yang sama dan verifikasi video ID sebelum menggunakan hasilnya.
3. Bila VidIQ tetap tidak dapat mengambil isi video ini, gunakan player resmi atau materi ekspor yang pemiliknya berhak bagikan; jangan mengunduh stream dengan metode tidak resmi.
4. Setiap klaim gameplay harus merujuk ke timestamp dan bukti visual/audio dari video sumber ini. Jika bukti tidak tersedia, tandai UNKNOWN.
