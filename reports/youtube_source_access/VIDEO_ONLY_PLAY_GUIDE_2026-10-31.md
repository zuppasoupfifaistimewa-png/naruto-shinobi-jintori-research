# Panduan bermain berdasarkan video saja — Naruto Jintori

- Tanggal penyusunan: 31 Oktober 2026
- Game: **Naruto — Shinobi no Sato no Jintori Kassen** (PS1, SLPS-03553)
- Video: https://www.youtube.com/watch?v=r30Rs_NuExc
- Judul metadata: *INILAH GAME NARUTO MONOPOLI PS 1 PRASEJARAH! - Naruto: Shinobi no Sato no Jintori Kassen Indonesia*
- Kanal metadata: Kevin Tedja
- Durasi yang dilaporkan: 2:53:15
- Cakupan analisis visual yang tersedia: 00:00–173:15, sampai briefing Stage 4.
- Laporan sumber yang mendasari: `VIDEO_WATCH_ANALYSIS_2026-10-31.md` dan `TRANSCRIPT_PRELIMINARY_GAMEPLAY_NOTES_2026-10-31.md`.

## 1. Cara membaca status bukti

Status di seluruh dokumen ini sengaja dibatasi menjadi tiga label:

- **TERAMATI** — mekanisme/kejadian dilaporkan terlihat dalam analisis visual video. Ini berarti *video-observed*, bukan otomatis terbukti dari kode ROM. Jika hanya berasal dari ucapan streamer, disebut secara eksplisit sebagai “narasi streamer”.
- **HIPOTESIS** — penjelasan yang masuk akal dari rangkaian adegan atau narasi, tetapi pemicu, aturan, dan penerapannya belum dibuktikan.
- **BELUM DIKETAHUI** — video dan ringkasan yang tersedia tidak memberi bukti cukup untuk menjawabnya.

Tidak ada video mentah, audio, frame, ataupun screenshot privat yang disalin ke repository. Ringkasan visual berasal dari analisis otomatis pihak ketiga atas video publik, bukan inspeksi frame mentah per frame oleh peneliti. Transkrip otomatis berpotensi salah mendengar nama UI Jepang, nama item, angka, dan tombol. Karena itu:
1. “TERAMATI” tidak boleh dipromosikan menjadi “terverifikasi implementasi ROM”.
2. Jika analisis visual dan ucapan streamer tidak sama kuat, analisis visual menjadi dasar adegan; transkrip hanya petunjuk tambahan.
3. Tidak boleh menyimpulkan probabilitas, rumus, atau perilaku AI hanya dari satu playthrough.
4. Video berhenti di briefing Stage 4; tidak ada bukti penyelesaian Stage 4 atau Story Mode tamat.

## 2. Ringkasan cara bermain yang dapat disusun dari video

Game yang diperlihatkan menggabungkan papan bergerak berbasis roulette, kepemilikan petak melalui Barrier (結界 — penghalang), ekonomi Chakra, dan pertarungan antar-pemilik petak. Alur umum yang paling aman untuk dijelaskan adalah:

1. Pilih Story Mode (ストーリーモード — Mode Cerita) dari menu awal.
2. Ikuti prolog dan briefing misi; periksa karakter/pihak yang ikut, Chakra awal, dan target Chakra misi.
3. Saat pertandingan papan dimulai, pemain bergiliran menggunakan roulette untuk menentukan gerak. Di bagian Stage 1 yang dianalisis, rentang hasil gerak biasa dilaporkan 1–8.
4. Bergerak mengikuti jalur petak yang tersambung. Efek kartu/scroll dapat mengubah langkah atau keadaan pemain.
5. Ketika berhenti di petak netral, adegan menunjukkan opsi membangun Barrier untuk mengambil kepemilikan petak dengan membayar Chakra.
6. Ketika berhenti di petak sendiri, pemain dapat meningkatkan level Barrier.
7. Ketika masuk petak lawan, adegan menunjukkan pungutan/toll dan/atau pilihan pertarungan. Hubungan tepat antara pembayaran dan battle belum dapat dipastikan.
8. Jika battle terjadi, pemain memilih teknik/aksi; roulette serangan/pertahanan kemudian menyelesaikan hasil pertarungan dan kerusakan Barrier.
9. Kartu/scroll dapat memberikan efek khusus, antara lain gerak tetap, pemulihan Chakra, jebakan, peningkatan serangan, atau teknik perebutan Barrier.
10. Pantau Chakra dan kepemilikan petak. Video memperlihatkan kemenangan Stage 1–3, tetapi tidak mengisolasi frame pertama ketika syarat menang terpenuhi. Angka target Chakra terlihat pada briefing; apakah perlu syarat node/milestone tambahan masih harus diperlakukan sebagai HIPOTESIS.
11. Di antara misi Story, ikuti adegan cerita/briefing dan save prompt yang ditampilkan.
12. Challenge Stage yang diperlihatkan adalah minigame memanjat pohon yang terpisah dari pertandingan papan biasa.

**Batas penting:** ini adalah alur kerja permainan yang direkonstruksi dari adegan video. Ia belum merupakan instruksi tombol lengkap. Tidak ada dasar cukup untuk memetakan tombol PS1 (Cross/Circle/Square/Triangle/L1/R1/Start), input konfirmasi, atau timing input secara universal.

## 3. Kronologi dari menu awal hingga adegan terakhir

### 3.1 00:00–02:40 — Title, menu, pengaturan, pemilihan karakter

| Waktu | Adegan / yang dilaporkan | Panduan dan status |
|---|---|---|
| 00:00–02:40 | Title dan menu utama. Opsi yang dikenali: Story Mode, Party Mode, Bingo Book, Settings. | **TERAMATI:** menu menampilkan Story Mode (ストーリーモード — Mode Cerita), Party Mode (パーティーモード — Mode Party), Bingo Book (ビンゴブック — Buku Bingo), dan Settings (せってい — Pengaturan). |
| Dalam rentang yang sama | Layar settings dan character select; ada karakter yang terbuka dan terkunci. | **TERAMATI:** layar pengaturan dan status karakter terbuka/terkunci dilaporkan terlihat. **BELUM DIKETAHUI:** fungsi lengkap tiap opsi settings, daftar karakter lengkap, serta syarat unlock masing-masing. |
| 01:09–02:14 | Streamer membedakan Story dan Party, serta menyebut unlock karakter melalui Story. | **TERAMATI (narasi streamer):** Party disebut sebagai mode dua pemain dan Story sebagai jalur progres. **HIPOTESIS:** sebagian karakter dibuka melalui progres Story. Syarat dan daftar unlock belum diuji. |

**Panduan yang dapat dipastikan:** untuk mengikuti jalur cerita yang direkam, pilih Story Mode. Jangan menganggap video telah menunjukkan seluruh mode atau seluruh karakter.

### 3.2 02:41–08:33 — Prolog dan persiapan Stage 1

| Waktu | Adegan / yang dilaporkan | Aturan dan status |
|---|---|---|
| 02:41–08:33 | Prolog menghadirkan Naruto, Iruka, dan Mizuki; cerita berkaitan dengan Forbidden Scroll. | **TERAMATI:** adegan cerita dan tokoh tersebut muncul. |
| Dalam prolog | Istilah Forbidden Scroll (封印の書 — Gulungan Terlarang) dan Shadow Clone Jutsu (多重影分身の術 — Teknik Klon Bayangan) muncul dalam konteks cerita. | **TERAMATI:** istilah/teknik disebut pada konteks prolog. **BELUM DIKETAHUI:** apakah dialog ini mengajarkan kontrol tertentu atau hanya narasi cerita. |
| Akhir rentang | Mission 1 melawan Mizuki dimulai; target 3.000 Chakra dan awal 1.500 Chakra per pemain dilaporkan. | **TERAMATI:** angka setup misi yang dilaporkan adalah 1.500 awal dan target 3.000. |

**Panduan:** baca target misi sebagai aturan khusus stage, bukan nilai global semua pertandingan.

### 3.3 08:34–18:00 — Board Stage 1: gerak, petak, upgrade pertama, battle

| Waktu | Adegan / yang dilaporkan | Panduan dan status |
|---|---|---|
| 08:34–18:00 | Giliran Naruto dan Mizuki; roulette gerak bernomor dilaporkan menghasilkan 1–8. | **TERAMATI:** permainan papan memakai roulette angka; rentang 1–8 dilaporkan pada bagian ini. **BELUM DIKETAHUI:** peluang tiap angka, apakah distribusinya seragam, dan apakah rentang ini berlaku di semua stage. |
| Dalam rentang | Pemain bergerak ke node/petak yang saling terhubung. | **TERAMATI:** perpindahan di sepanjang board terlihat. **BELUM DIKETAHUI:** aturan lengkap pemilihan cabang saat ada lebih dari satu jalur. |
| Dalam rentang | Node netral diklaim dengan membayar Chakra dan membangun Barrier Level 1. | **TERAMATI:** mekanisme membangun Barrier di petak netral dilaporkan terlihat. **BELUM DIKETAHUI:** harga universal, syarat saldo, variasi biaya per node, dan apakah semua petak netral bisa diklaim. |
| Dalam rentang | Kartu gerak 7 langkah dan Cup Ramen yang menambah 50 Chakra disebut/terlihat. | **TERAMATI:** efek 7 langkah dan pemulihan Cup Ramen +50 Chakra dilaporkan. **BELUM DIKETAHUI:** nama resmi kartu, kapan harus dimainkan, durasi, batas tumpukan, atau apakah nilainya sama di semua mode. |
| Dalam rentang | Mizuki meningkatkan Barrier hingga Level 3 dan Level 5; toll petak bernilai tinggi dilaporkan sampai 580. | **TERAMATI:** upgrade beberapa level sampai Level 5 dan nilai toll 580 dilaporkan. **BELUM DIKETAHUI:** rumus nilai/toll untuk tiap level. |
| Dalam rentang | Naruto mendarat di Barrier lawan dan adegan menampilkan pilihan defensif serta teknik Shadow Clone melawan respons Mizuki. Roulette battle menyelesaikan hasil. | **TERAMATI:** ada pilihan aksi/pertahanan, teknik ninja, dan roulette dalam battle. **HIPOTESIS:** battle mengurangi durability Barrier lawan. **BELUM DIKETAHUI:** apakah pemain dapat selalu memilih bayar toll alih-alih bertarung, urutan fase, formula damage, dan dampaknya pada Chakra. |

**Panduan keputusan yang aman:** saat bertemu node netral, perhatikan biaya dan opsi Barrier; di node sendiri, periksa opsi upgrade; saat memasuki node lawan, jangan mengasumsikan battle selalu wajib atau selalu opsional karena kondisi pemicunya belum dipetakan.

### 3.4 18:01–36:50 — Kontestasi petak Stage 1, perebutan Barrier, saldo negatif

| Waktu | Adegan / yang dilaporkan | Panduan dan status |
|---|---|---|
| 18:01–36:50 | Kontestasi kepemilikan node berlanjut antara Naruto dan Mizuki. | **TERAMATI:** pertukaran/serangan terhadap petak terjadi selama fase ini. |
| Dalam rentang | Naruto memakai scroll technique 結界奪取の術 (Jutsu Perebutan Barrier) untuk mencoba mengambil petak lawan; hasilnya menggunakan roulette takeover. | **TERAMATI:** teknik perebutan Barrier dan roulette berbeda dari roulette gerak dilaporkan muncul. |
| Dalam rentang | Mizuki mengalami saldo Chakra negatif; sesudahnya muncul 結界開放 (Pelepasan Barrier). | **TERAMATI:** saldo negatif dan adegan pelepasan Barrier dilaporkan. **HIPOTESIS:** pelepasan Barrier merupakan mekanisme pengurangan aset/penyeimbang saat ekonomi pemain defisit. |
| Dalam rentang | Naruto menguasai sejumlah node dan laporan menyebut proyeksi pendapatan/bonus di atas 4.000 Chakra. | **TERAMATI:** penguasaan node dan estimasi nilai besar dilaporkan. **BELUM DIKETAHUI:** kapan pendapatan benar-benar dibayarkan dan apakah proyeksi tersebut sama dengan saldo yang masuk. |

**Jangan disimpulkan:** pemain pasti langsung kalah saat Chakra negatif. Video justru melaporkan Mizuki tetap berada dalam pertandingan dan mengalami pelepasan Barrier, tetapi tidak menunjukkan semua kemungkinan akibat saldo negatif.

### 3.5 36:51–52:18 — Akhir Stage 1

| Waktu | Adegan / yang dilaporkan | Status |
|---|---|---|
| 36:51–52:18 | Chakra Mizuki dilaporkan turun sekitar -4.459 sampai -6.219. | **TERAMATI:** nilai negatif ini dilaporkan analisis video. Angka tepat dan frame pembacaannya belum divalidasi frame mentah. |
| Dalam rentang | Naruto dilaporkan mencapai sekitar 9.963 Chakra pada node milestone tengah. | **TERAMATI:** angka akhir tersebut dilaporkan; **BELUM DIKETAHUI:** apakah itulah nilai tepat saat kemenangan dipicu. |
| Sekitar akhir rentang | Banner 大勝利 (Kemenangan Besar), cutscene, dan prompt save. | **TERAMATI:** Stage 1 berakhir dengan banner kemenangan dan adegan lanjutan/save prompt. |
| Sesudah hasil | Nilai kemenangan jauh di atas target 3.000 yang ditampilkan pada briefing. | **HIPOTESIS:** target Chakra mungkin diperiksa bersama kondisi posisi/node atau timing giliran. **BELUM DIKETAHUI:** trigger kemenangan persis, termasuk apakah harus mencapai/melewati node tertentu. |

### 3.6 52:19–54:55 — Briefing Stage 2

| Waktu | Adegan / yang dilaporkan | Status |
|---|---|---|
| 52:19–54:55 | Cutscene Konohamaru, Ebisu, dan Sakura. | **TERAMATI:** adegan briefing dengan tokoh tersebut. |
| Dalam rentang | Naruto dan Konohamaru berada di satu pihak melawan Sakura; map berada di area atap Akademi. | **TERAMATI:** susunan tiga peserta/pihak dengan Naruto dan Konohamaru sebagai sekutu dilaporkan. **BELUM DIKETAHUI:** apakah partner selalu dikendalikan AI atau dapat diganti pengendaliannya di mode lain. |
| Briefing | Target Stage 2 4.000 Chakra dan awal 2.000 per peserta. | **TERAMATI:** angka briefing yang dilaporkan. |

**Panduan:** periksa apakah misi menggunakan tim atau free-for-all sebelum mengambil keputusan di board. Stage 2 bukan konfigurasi peserta yang sama dengan Stage 1.

### 3.7 54:56–87:10 — Stage 2 paruh pertama

| Waktu | Adegan / yang dilaporkan | Panduan dan status |
|---|---|---|
| 54:56–87:10 | Naruto, Konohamaru, dan Sakura bergiliran di board. | **TERAMATI:** tiga pihak mengambil giliran dalam pertandingan. |
| Dalam rentang | Sakura menguasai petak bernilai tinggi, termasuk toll di atas 1.000. | **TERAMATI:** petak dengan toll besar dilaporkan. **BELUM DIKETAHUI:** level, adjacency, dan konfigurasi yang menentukan nilai tersebut. |
| Dalam rentang | Kartu +3 Kunai dan trap/caltrops atau explosive tags disebut/dilaporkan. | **TERAMATI:** elemen kartu/alat dan jebakan muncul pada ringkasan visual. **BELUM DIKETAHUI:** nama Jepang yang tepat, efek numerik lengkap, target, durasi, dan aturan pemicu trap. |
| Dalam rentang | Konohamaru/Naruto menghadapi Barrier Level 5 milik Sakura; battle menampilkan Inner Sakura sebagai pertahanan melawan serangan Clone Rush. | **TERAMATI:** pertarungan Barrier tingkat tinggi serta pilihan aksi khusus dilaporkan. **BELUM DIKETAHUI:** apakah teknik tersebut mengubah peluang, damage, atau hanya animasi/jenis serangan. |

### 3.8 87:11–118:08 — Stage 2 paruh kedua dan kemenangan

| Waktu | Adegan / yang dilaporkan | Status |
|---|---|---|
| 87:11–118:08 | Sakura menguasai banyak bagian board; Naruto melanjutkan kontestasi petak. | **TERAMATI:** keadaan board berubah dan perebutan petak berlanjut. |
| Dalam rentang | Naruto memakai うずまきナルト連弾 (Naruto Rendan — Kombo Naruto Uzumaki), yang dilaporkan melemahkan Barrier. | **TERAMATI:** teknik Naruto Rendan dan efek terhadap Barrier dilaporkan. **BELUM DIKETAHUI:** formula durability/damage dan apakah teknik itu khusus target Barrier. |
| Akhir rentang | Naruto dilaporkan mencapai 5.806 Chakra; Stage 2 Clear dan 大勝利 muncul sekitar 117:59. | **TERAMATI:** kemenangan Stage 2 dan angka Chakra tersebut dilaporkan. **BELUM DIKETAHUI:** frame pertama target tercapai dan apakah milestone/urutan giliran menjadi syarat. |

### 3.9 118:09–121:00 — Briefing Stage 3: Bell Test

| Waktu | Adegan / yang dilaporkan | Status |
|---|---|---|
| 118:09–121:00 | Bell Test Team 7 menghadirkan Naruto, Sasuke, Sakura, dan Kakashi. | **TERAMATI:** empat pihak/peserta di briefing. |
| Briefing | Target 4.000 Chakra; masing-masing mulai dengan 2.000. | **TERAMATI:** angka setup yang dilaporkan. |
| Konteks | Ini bukan tim Naruto + Konohamaru melawan satu lawan, melainkan empat peserta pada board. | **TERAMATI:** susunan pertandingan Stage 3 berbeda dari Stage 2. |

### 3.10 121:01–146:00 — Stage 3: pertarungan empat pihak

| Waktu | Adegan / yang dilaporkan | Panduan dan status |
|---|---|---|
| 121:01–146:00 | Empat pihak bergerak dan mengklaim node. | **TERAMATI:** board empat peserta aktif. |
| Dalam rentang | Barrier Kakashi memiliki Level 4 dan toll 880. | **TERAMATI:** contoh Level 4/toll 880 dilaporkan; ini bukan konstanta universal. |
| Dalam rentang | Sasuke memakai 火遁・豪火球の術 (Elemen Api: Teknik Bola Api Besar) dan 写輪眼 (Sharingan) pada battle. | **TERAMATI:** teknik dan nama tersebut dilaporkan pada pertarungan. **BELUM DIKETAHUI:** efek mekanis masing-masing teknik. |
| Dalam rentang | Naruto memakai 結界奪取 (Perebutan Barrier) dan berhasil mengambil node Kakashi pada hasil roulette takeover 10+. | **TERAMATI:** perebutan Barrier berhasil pada hasil yang dilaporkan 10+. **BELUM DIKETAHUI:** rentang penuh roulette, probabilitas, dan apakah nilai 10+ adalah ambang tetap atau hanya hasil yang muncul pada percobaan itu. |

### 3.11 146:01–168:35 — Akhir Stage 3 dan kemenangan

| Waktu | Adegan / yang dilaporkan | Status |
|---|---|---|
| 146:01–168:35 | Kakashi menyerang Barrier bernilai tinggi milik Naruto dengan 雷切 (Raikiri — Pedang Petir). | **TERAMATI:** teknik Raikiri dipakai pada konteks serangan Barrier. |
| Dalam rentang | Naruto memilih おいろけの術 (Sexy Jutsu — Teknik Seksi) sebagai pertahanan dan bertahan dari serangan. | **TERAMATI:** pilihan aksi defensif dan hasil bertahan dilaporkan. **BELUM DIKETAHUI:** apakah keberhasilan karena teknik, roulette, stat, atau gabungan faktor. |
| Dalam rentang | Kakashi mengalami saldo negatif yang dilaporkan sekitar -566/-216; Naruto mempertahankan node berdekatan Level 4/5. | **TERAMATI:** defisit dan penguasaan node Naruto dilaporkan. **BELUM DIKETAHUI:** aturan pasti pendapatan/biaya dan bonus petak bersebelahan. |
| Sekitar 167:57 | Naruto dilaporkan melewati milestone dengan 10.690 Chakra; 大勝利 muncul. | **TERAMATI:** kemenangan Stage 3 dilaporkan. **HIPOTESIS:** posisi pada milestone mungkin ikut menentukan timing kemenangan. **BELUM DIKETAHUI:** kondisi pemicu lengkap. |

### 3.12 168:36–171:40 — Challenge Stage: latihan kontrol Chakra di pohon

| Waktu | Adegan / yang dilaporkan | Panduan dan status |
|---|---|---|
| 168:36–171:40 | チャレンジステージ (Challenge Stage) memperlihatkan latihan kontrol Chakra memanjat pohon, Naruto melawan Sasuke. | **TERAMATI:** minigame terpisah dari board wilayah biasa. |
| Awal minigame | Chakra awal dilaporkan 600. | **TERAMATI:** nilai 600 dilaporkan pada konteks minigame. |
| Aturan hasil | Analisis visual melaporkan pemain menang dengan mencapai puncak lebih dahulu atau menghabiskan Chakra lawan sampai 0. | **TERAMATI (ringkasan visual):** dua kondisi tersebut dilaporkan. **BELUM DIKETAHUI:** apakah keduanya benar-benar dua kondisi menang independen, hubungan Chakra dengan langkah, dan apakah ada tie-break. |
| Selama minigame | Roulette dan kartu mengubah langkah; efek pengurang langkah -2/-4 dilaporkan. | **TERAMATI:** modifikasi langkah negatif dilaporkan. **BELUM DIKETAHUI:** daftar lengkap efek, batas langkah minimum, dan interaksi antar-kartu. |
| Akhir rentang | Sasuke menang setelah menggunakan kartu gerak. | **TERAMATI:** hasil minigame yang dilaporkan adalah kemenangan Sasuke. **BELUM DIKETAHUI:** hadiah atau dampaknya pada progres Story berikutnya. |

### 3.13 171:41–173:15 — Briefing Stage 4, adegan terakhir video

| Waktu | Adegan / yang dilaporkan | Status |
|---|---|---|
| 171:41–173:15 | Cerita berpindah ke Land of Waves, dengan Demon Brothers dan Zabuza pada pengantar misi. | **TERAMATI:** tema/karakter briefing Stage 4 dilaporkan. |
| Briefing | Objective Mission 4 adalah 5.000 Chakra; Kakashi ikut pada pihak pemain. | **TERAMATI:** target 5.000 dan kehadiran Kakashi dilaporkan. |
| Akhir video | Streamer menyimpan state dan mengakhiri sesi; tidak ada permainan Stage 4 yang dianalisis. | **TERAMATI:** cakupan video berakhir sebelum gameplay Stage 4. **BELUM DIKETAHUI:** start Chakra Stage 4, susunan lawan lengkap, board, aturan khusus, dan hasil stage. |

## 4. Panduan mekanisme inti

### 4.1 Setup misi dan target Chakra

| Segmen | Susunan peserta yang dilaporkan | Chakra awal | Target Chakra | Status |
|---|---|---:|---:|---|
| Stage 1 | Naruto vs Mizuki | 1.500 masing-masing | 3.000 | **TERAMATI** |
| Stage 2 | Naruto + Konohamaru vs Sakura | 2.000 per peserta | 4.000 | **TERAMATI** |
| Stage 3 | Naruto, Sasuke, Sakura, Kakashi (empat pihak) | 2.000 per peserta | 4.000 | **TERAMATI** |
| Challenge Stage | Naruto vs Sasuke | 600 dilaporkan | 0 sebagai kondisi lawan habis | **TERAMATI**, detail trigger belum teruji |
| Stage 4 briefing | Naruto dengan Kakashi di pihak pemain; lawan terkait Land of Waves | Tidak tercatat pada ringkasan | 5.000 | **TERAMATI** untuk target; start dan susunan detail **BELUM DIKETAHUI** |

### 4.2 Roulette gerak, jalur board, dan node

- **TERAMATI:** roulette angka digunakan untuk menentukan langkah di board; contoh rentang 1–8 pada Stage 1.
- **TERAMATI:** board memiliki node/petak yang saling terhubung dan pemain berpindah mengikuti jalurnya.
- **HIPOTESIS:** jika ada lebih dari satu cabang, pemain dapat memilih rute yang memengaruhi node lawan yang ditemui. Transkrip streamer menyebut rute bawah, tetapi pilihan cabang dan cara memilihnya belum terkonfirmasi secara visual.
- **HIPOTESIS (narasi streamer):** ada situasi gerak mundur tujuh langkah. Belum dapat ditetapkan apakah itu efek kartu, trap, event board, atau salah dengar transkrip.
- **BELUM DIKETAHUI:** apakah semua stage memakai roulette yang sama; peluang tiap hasil; cara memilih cabang; interaksi langkah ekstra, pengurangan langkah, berhenti paksa, dan efek yang mengubah arah.

### 4.3 Barrier: bangun, milik sendiri, milik lawan

| Situasi | Perilaku yang dilaporkan | Status |
|---|---|---|
| Mendarat di node netral | Membayar Chakra untuk membangun Barrier dan mengambil node. | **TERAMATI** |
| Mendarat di node sendiri | Dapat meningkatkan level Barrier. | **TERAMATI** |
| Level Barrier | Level 1 sampai 5 terlihat/dilaporkan. | **TERAMATI** |
| Barrier milik lawan | Muncul toll dan/atau battle ketika pemain masuk petak lawan. | **TERAMATI** secara adegan; aturan toll-vs-battle **BELUM DIKETAHUI** |
| Node bersebelahan | Analisis melaporkan keterhubungan/peningkatan nilai barrier. | **HIPOTESIS** untuk formula bonus; pengaruh adjacency perlu dicatat terpisah dari efek visual koneksi |
| Saldo negatif | Barrier release 結界開放 terjadi pada Mizuki. | **TERAMATI** |
| Durability | Pertarungan dilaporkan memberi damage pada Barrier. | **TERAMATI** untuk interaksi; satuan, nilai awal, dan formula damage **BELUM DIKETAHUI** |

**Jangan gunakan angka contoh sebagai harga tetap:** toll 580, toll 880, dan toll di atas 1.000 adalah contoh yang dilaporkan pada node tertentu. Video tidak membuktikan satu rumus tunggal atau harga universal.

### 4.4 Battle dan jutsu

Contoh teknik yang dilaporkan oleh analisis visual:

| Jepang | Terjemahan Indonesia | Konteks yang dilaporkan | Status |
|---|---|---|---|
| 多重影分身の術 | Teknik Klon Bayangan | Naruto melawan Mizuki | **TERAMATI** |
| うずまきナルト連弾 | Kombo Naruto Uzumaki (Naruto Rendan) | Serangan Barrier Stage 2 | **TERAMATI** |
| 火遁・豪火球の術 | Elemen Api: Teknik Bola Api Besar | Sasuke dalam battle Stage 3 | **TERAMATI** |
| 写輪眼 | Sharingan | Sasuke dalam battle Stage 3 | **TERAMATI** |
| 雷切 | Pedang Petir (Raikiri) | Kakashi menyerang Barrier Naruto | **TERAMATI** |
| おいろけの術 | Teknik Seksi (Sexy Jutsu) | Pertahanan Naruto terhadap Raikiri | **TERAMATI** |
| 結界奪取の術 / 結界奪取 | Jutsu Perebutan Barrier | Perebutan node lawan | **TERAMATI** |
| 結界開放 | Pelepasan Barrier | Pelepasan Barrier setelah Chakra negatif | **TERAMATI** |

- **TERAMATI:** adegan battle menggunakan pilihan aksi/teknik dan roulette untuk menyelesaikan serangan/pertahanan.
- **HIPOTESIS:** hasil roulette memengaruhi damage atau kemampuan mempertahankan Barrier.
- **BELUM DIKETAHUI:** seluruh daftar aksi, biaya Chakra tiap aksi, urutan pilihan penyerang/bertahan, peluang, stat yang digunakan, formula damage, durability, dan apakah jutsu tertentu hanya tersedia untuk karakter tertentu.

### 4.5 Kartu, scroll, dan jebakan

| Efek/kartu yang dilaporkan | Bukti dan status |
|---|---|
| Gerak 7 langkah | **TERAMATI** dalam analisis Stage 1. Nama dan syarat pemakaian **BELUM DIKETAHUI**. |
| Cup Ramen +50 Chakra | **TERAMATI** dalam analisis Stage 1. Batas pemulihan/durasi **BELUM DIKETAHUI**. |
| +3 Kunai | **TERAMATI** sebagai efek yang dilaporkan Stage 2. Apakah +3 berarti attack power, jumlah senjata, atau nilai lain perlu konfirmasi UI. |
| Trap/caltrops/explosive tag | **TERAMATI** sebagai unsur permainan Stage 2. Efek spesifiknya **BELUM DIKETAHUI**. |
| 結界奪取の術 (Perebutan Barrier) | **TERAMATI** sebagai teknik/scroll untuk mengambil barrier lawan. Kondisi sukses dan probabilitas **BELUM DIKETAHUI**. |
| Gerak mundur 7 langkah | Hanya dari narasi streamer/transkrip. **HIPOTESIS**, bukan aturan final. |
| Trap membuat mundur atau melewatkan giliran | Disebut/diduga dari transkrip; scene breakdown belum cukup jelas. **BELUM DIKETAHUI**. |
| Kunai dua kali menghancurkan petak | Klaim transkrip belum dikuatkan scene breakdown. **BELUM DIKETAHUI**. |

**Catatan istilah:** transkrip otomatis sempat salah dengar istilah yang terdengar seperti “tail/tile”. Jangan mengubahnya menjadi nama fitur atau istilah UI Jepang tanpa bukti visual yang jelas.

### 4.6 Ekonomi Chakra dan kemenangan

- **TERAMATI:** setiap misi yang diringkas memiliki angka Chakra awal dan target berbeda.
- **TERAMATI:** Chakra dapat bertambah/berkurang; pemain yang kalah ekonomi dapat mencapai nilai negatif pada adegan Stage 1 dan Stage 3.
- **TERAMATI:** setidaknya satu efek pemulihan bernilai +50 Chakra dilaporkan.
- **TERAMATI:** hasil Stage 1, 2, dan 3 menunjukkan banner 大勝利 (Kemenangan Besar).
- **HIPOTESIS:** kepemilikan node dan toll/pendapatan berkaitan dengan akumulasi Chakra yang diperlukan untuk menang.
- **HIPOTESIS:** target Chakra dapat terkait dengan pencapaian node milestone/posisi tertentu karena adegan kemenangan dianalisis dekat milestone.
- **BELUM DIKETAHUI:** apakah target diperiksa setiap frame, saat giliran berakhir, ketika melewati node, atau setelah pembayaran pendapatan; apakah target saja cukup; apakah ada kondisi kemenangan alternatif per mode.

### 4.7 Challenge Stage bukan pertandingan papan biasa

- **TERAMATI:** minigame memanjat pohon di antara Stage 3 dan briefing Stage 4.
- **TERAMATI:** Naruto dan Sasuke bersaing; roulette/kartu memengaruhi langkah.
- **TERAMATI:** analisis melaporkan 600 Chakra dan kemenangan melalui mencapai puncak atau menghabiskan Chakra lawan.
- **BELUM DIKETAHUI:** sistem langkah lengkap, efek tiap kartu, penalti, hubungan Chakra dengan jatuh/gerak, hadiah, dan dampak hasil terhadap Story.

## 5. Strategi bermain yang boleh disimpulkan — dan batasnya

### Kesimpulan praktis yang didukung adegan

1. Periksa target Chakra dan jumlah peserta di briefing setiap stage karena angkanya berubah.
2. Perhatikan kepemilikan petak: petak netral dapat dibangun Barrier, petak milik sendiri dapat di-upgrade, dan petak lawan dapat menimbulkan toll atau battle.
3. Pantau nilai toll petak lawan sebelum mengambil risiko melintasinya.
4. Simpan perhatian pada kartu/scroll yang dapat mengubah langkah atau situasi battle.
5. Perhatikan saldo Chakra negatif dan kemungkinan Barrier dilepas.
6. Dalam Challenge Stage, pertimbangkan efek langkah dari roulette/kartu dan kondisi finish yang ditampilkan.

### Jangan dianggap strategi optimal atau aturan pasti

- “Selalu bangun semua petak.”
- “Selalu upgrade sampai Level 5.”
- “Selalu lawan pemilik petak.”
- “Stat terbesar otomatis menang.”
- “Kunai dua kali pasti menghapus petak.”
- “Semua trap membuat lawan mundur.”
- “Setiap stage dimenangkan tepat pada angka target tanpa syarat lain.”
- “AI selalu mengejar petak termahal atau selalu menyerang pemain terdepan.”

Semua pernyataan di atas melampaui apa yang dibuktikan oleh satu video.

## 6. Daftar pertanyaan yang masih terbuka

### Kontrol dan UI
- Tombol PS1 apa yang membuka, memilih, membatalkan, dan mengonfirmasi setiap menu?
- Apakah kontrol berbeda pada menu, board, battle, kartu, dan Challenge Stage?
- Bagaimana pemain memilih cabang jalur dan target petak?
- Apakah ada tombol khusus untuk melihat status, inventory, atau informasi Barrier?

### Board dan gerak
- Apakah roulette 1–8 seragam atau berbobot?
- Adakah modifier karakter, stage, item, atau status yang memengaruhi roulette?
- Kapan langkah mundur/penalti muncul?
- Bagaimana aturan simpang, loop, node milestone, dan berhenti tepat di suatu petak?

### Barrier dan ekonomi
- Berapa biaya membangun/upgrade untuk setiap tipe node dan level?
- Bagaimana toll dihitung?
- Kapan toll/pendapatan dikreditkan?
- Apa yang dimaksud node terhubung/adjacent dan bagaimana bonusnya dihitung?
- Bagaimana durability Barrier ditentukan dan dikurangi?
- Apa ambang, pemilihan node, dan urutan Barrier release ketika saldo negatif?

### Battle
- Apa semua pilihan serang/bertahan?
- Apakah roulette serang, pertahanan, dan takeover menggunakan range/rumus berbeda?
- Apa arti hasil takeover 10+ yang dilaporkan?
- Bagaimana teknik, karakter, stat, Chakra, dan kartu memengaruhi hasil?
- Kapan Barrier dihancurkan, direbut, atau hanya kehilangan durability?

### Kartu dan AI
- Apa katalog lengkap kartu/scroll dan seluruh effect ID?
- Kapan kartu ditarik, dipilih, digunakan, dibuang, atau dicuri?
- Bagaimana trap ditempatkan dan dipicu?
- Bagaimana AI memilih langkah, rute, upgrade, battle, teknik, dan kartu?
- Apakah strategi AI berbeda menurut karakter, stage, tingkat kesulitan, atau keadaan Chakra?

### Story dan progres
- Apa seluruh stage Story setelah Stage 4?
- Apa syarat unlock karakter dan konten tambahan?
- Apakah hasil Challenge Stage mengubah hadiah atau cabang cerita?
- Apa syarat final menyelesaikan Story Mode?

## 7. Batas cakupan dan langkah riset berikutnya

Panduan ini selesai sebagai **panduan video-only untuk adegan 00:00–173:15 yang tersedia**. Ia belum menuntaskan logika game penuh. Langkah paling bernilai untuk memperdalam sumber video, tanpa mengarang, adalah memperoleh timestamp/frame spesifik untuk:
1. menu dan setiap layar kontrol;
2. satu contoh lengkap landing di node netral, own node, dan enemy node;
3. satu battle dari pilihan teknik sampai perubahan durability/Chakra;
4. satu transaksi upgrade Level 1→2 dan Level 4→5;
5. satu efek kartu/trap dengan state sebelum dan sesudah;
6. frame pertama ketika target Chakra tercapai dan frame yang memicu 大勝利;
7. setiap aksi Challenge Stage hingga hasil akhir.

Setelah data visual video cukup rinci, mekanisme internal harus dipisahkan lagi lewat analisis kode ROM dan uji runtime terkendali. Jangan menyalin ROM, BIOS, Memory Card, savestate, dump RAM, video/audio, atau screenshot privat ke Git. Jangan menjalankan permainan atau adaptive player hanya berdasarkan panduan ini; gate runtime dan izin eksplisit yang sudah berlaku tetap harus dipatuhi.

## 8. Ringkasan status akhir

| Area | Status terbaik saat ini |
|---|---|
| Menu dan pilihan Story | **TERAMATI** |
| Setup dan target Stage 1–4 | **TERAMATI** untuk nilai yang dilaporkan; detail Stage 4 belum lengkap |
| Board dan giliran | **TERAMATI** pada tingkat alur umum |
| Roulette gerak 1–8 | **TERAMATI** untuk adegan Stage 1; generalisasi ke semua stage **BELUM DIKETAHUI** |
| Build/upgrade Barrier | **TERAMATI** untuk keberadaan aksi dan level; formula **BELUM DIKETAHUI** |
| Toll, adjacency, durability | **TERAMATI** untuk contoh; formula **BELUM DIKETAHUI** |
| Battle dan jutsu | **TERAMATI** untuk contoh aksi; formula hasil **BELUM DIKETAHUI** |
| Scroll, kartu, trap | **TERAMATI** sebagian; katalog/efek penuh **BELUM DIKETAHUI** |
| Negative Chakra dan Barrier release | **TERAMATI** pada contoh; pemicu lengkap **BELUM DIKETAHUI** |
| Challenge Stage | **TERAMATI** untuk alur; aturan rinci **BELUM DIKETAHUI** |
| AI dan probabilitas | **BELUM DIKETAHUI** |
| Stage 4 dan kelanjutan Story | Briefing **TERAMATI**; gameplay dan hasil **BELUM DIKETAHUI** |
| Seluruh logika game | **BELUM LENGKAP** |

**Kesimpulan:** video memberikan dasar untuk menjelaskan putaran permainan dan contoh mekanisme utama, tetapi tidak cukup untuk menuliskan manual lengkap yang memuat semua kontrol, cabang, formula, kartu, AI, dan stage. Panduan ini sengaja mempertahankan ketidakpastian tersebut agar penelitian berikutnya tidak membangun aturan palsu.
