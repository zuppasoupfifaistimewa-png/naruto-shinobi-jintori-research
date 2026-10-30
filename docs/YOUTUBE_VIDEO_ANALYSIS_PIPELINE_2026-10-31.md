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


## Koreksi akses video pihak ketiga — 31 Oktober 2026

- Video sumber r30Rs_NuExc adalah video publik milik kanal pihak lain. Pengguna tidak perlu memiliki atau menghubungkan channel YouTube sendiri untuk meminta analisis konten publik.
- Layar "Connect channel" di onboarding VidIQ terutama untuk fitur analitik channel milik pengguna. Itu bukan prasyarat bagi tool riset konten publik.
- VidIQ public-video capabilities tersedia melalui:
  - vidiq_video_transcript: mengambil captions/transcript video publik bila tersedia; biaya 5 kredit per pemanggilan.
  - vidiq_video_watch: analisis scene-by-scene bertimestamp dan momen visual untuk long-form YouTube; mendukung video hingga 6 jam; biaya 25 kredit per pemanggilan.
- Jalankan transcript lebih dahulu bila pengguna menyetujui biaya 5 kredit. Bila captions tidak tersedia, pertimbangkan visual watch dengan biaya 25 kredit setelah persetujuan yang sesuai. Jangan mengasumsikan private analytics, kepemilikan channel, atau akses akun kreator.
- Jangan meminta pengguna menghubungkan channel pribadi untuk menganalisis video orang lain. Gunakan hanya URL publik yang diberikan, dan laporkan bila video private, unavailable, atau tool tidak dapat memprosesnya.
- Setiap penggunaan kredit yang belum disetujui harus dikonfirmasi terlebih dahulu; sampaikan biaya sebelum pemanggilan.



## Addendum — video watch analysis complete, 31 Oktober 2026

### Sumber isi video
- VidIQ transcript retrieval completed for video ID r30Rs_NuExc; transcript Indonesian is summarized in reports/youtube_source_access/TRANSCRIPT_PRELIMINARY_GAMEPLAY_NOTES_2026-10-31.md.
- VidIQ visual scene-by-scene analysis completed for the same video ID. It covers the video from 00:00 to 173:15 and returns scenes covering menu/prologue, Story stages 1–3, a tree-climbing Challenge Stage, and the Stage 4 Land of Waves briefing.
- Timestamped scene report: reports/youtube_source_access/VIDEO_WATCH_ANALYSIS_2026-10-31.md.
- Visual analysis charge: 25 credits, as recorded at submission. Polling the existing completed result did not submit another paid analysis.

### Main video findings (candidate rules)
- Objective Chakra is stage-specific in the scenes: 3,000 (Stage 1), 4,000 (Stage 2), 4,000 (Stage 3), and 5,000 (Stage 4 briefing). Do not treat 3,000 as a universal Story Mode target.
- Ordinary board movement is described as a 1–8 numbered roulette in the analyzed Stage 1 play; avoid calling it a die without confirming the UI.
- Neutral nodes can be claimed by paying Chakra to erect barrier 結界 (barrier/penghalang). Own nodes offer upgrades; levels up to 5 are shown.
- Opponent node encounters involve toll payments and/or battle. Battle shows technique choices and attack/defense roulette; exact costs and damage formula remain unknown.
- Scroll/card effects include movement, Chakra recovery, combat boosts, traps, and a barrier-takeover technique 結界奪取の術 (Jutsu Perebutan Barrier).
- Negative Chakra may cause barrier release 結界開放 (Pelepasan Barrier).
- The Challenge Stage tree-climbing minigame is separate from standard board matches.
- The video ends at the Stage 4 briefing; Stage 4 completion and later story progress are not shown.

### Evidence discipline
- VIDEO-OBSERVED means the external visual analysis model reports an on-screen event at a timestamp. The raw frames were not archived or manually re-read in this repository.
- A video scene observation is not proof of internal program logic. Mathematical formulas, randomizer distributions, AI behavior, and state transitions remain HYPOTHESIS or UNKNOWN until checked against the ROM/emulator with controlled evidence.
- Do not promote transcript-only claims such as Kunai deleting a tile, trap immobilization/backward motion, or a universal 3,000 target without a matching scene and controlled test.
- No screenshot, frame, audio, video, ROM, BIOS, Memory Card, savestate, or RAM dump was committed.

### Next research action
Use the video-derived candidate rules to prioritize the existing ROM research:
1. Determine stage-specific victory target and milestone node gate.
2. Map barrier/node ownership and Levels 1–5, including adjacent-node effects.
3. Identify toll vs battle conditions on opponent nodes.
4. Separate board-movement roulette from battle attack/defense and barrier-takeover roulette.
5. Trace negative-Chakra barrier release and its exact bookkeeping.
6. Map scroll/card/trap effects and the Challenge Stage state machine.

Do not run Story Mode or send gameplay input solely from the video analysis. Reuse existing validated checkpoints and fail-closed WAIT/UNKNOWN gates.
