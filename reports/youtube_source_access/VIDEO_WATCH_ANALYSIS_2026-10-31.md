# Analisis visual video gameplay — Naruto Jintori (31 Oktober 2026)

## Identitas dan provenance

- Sumber: https://www.youtube.com/watch?v=r30Rs_NuExc
- Video ID: `r30Rs_NuExc`
- Judul metadata: INILAH GAME NARUTO MONOPOLI PS 1 PRASEJARAH! - Naruto: Shinobi no Sato no Jintori Kassen Indonesia
- Kanal metadata: Kevin Tedja
- Metode: analisis visual scene-by-scene VidIQ `vidiq_video_watch`
- Status hasil: COMPLETED
- Cakupan yang dilaporkan: 00:00–173:15 (sampai pengantar Misi 4)
- Biaya analisis visual yang dicatat pada checkpoint sebelumnya: 25 kredit. Pemeriksaan hasil/job tidak mengirim ulang analisis berbayar.
- Bukti yang disimpan di repo: teks ringkasan dan timestamp saja. Tidak ada video, audio, frame, screenshot, atau media biner yang disalin.

**Batas epistemik:** dokumen ini merekam hasil analisis visual otomatis atas video publik, bukan pembacaan langsung frame mentah oleh peneliti dan bukan pengujian ulang terhadap ROM. Label "terlihat di video" berarti dilaporkan sebagai observasi oleh analisis visual; itu belum otomatis membuktikan implementasi internal game. Aturan matematika dan kontrol masih harus diuji dengan ROM/emulator.

## Ringkasan cakupan video

| Waktu | Adegan yang dilaporkan | Observasi utama |
|---|---|---|
| 00:00–02:40 | Title, mode, settings, character select | Story Mode (ストーリーモード — Mode Cerita), Party Mode (パーティーモード — Mode Party), Bingo Book (ビンゴブック — Buku Bingo), Settings (せってい — Pengaturan), karakter terbuka/terkunci |
| 02:41–08:33 | Prolog dan Stage 1 | Naruto, Iruka, Mizuki; Forbidden Scroll (封印の書 — Gulungan Terlarang); Shadow Clone Jutsu (多重影分身の術 — Teknik Klon Bayangan); Mission 1 vs Mizuki, target 3.000 Chakra, awal 1.500 per pemain |
| 08:34–18:00 | Board Stage 1 | Giliran Naruto/Mizuki; roulette gerak 1–8; klaim node; barrier Level 1; kartu gerak 7 langkah dan Cup Ramen +50 Chakra; Mizuki upgrade Level 3/5; battle di barrier bernilai tinggi |
| 18:01–36:50 | Kontestasi Stage 1 | Scroll technique 結界奪取の術 (Jutsu Perebutan Barrier) untuk mencoba mengambil node; Chakra Mizuki masuk negatif; barrier release 結界開放 (Pelepasan Barrier) |
| 36:51–52:18 | Akhir Stage 1 | Mizuki terus kehilangan Chakra; Naruto dilaporkan mencapai 9.963 Chakra di node milestone tengah; victory banner 大勝利 (Kemenangan Besar); cutscene dan prompt save |
| 52:19–54:55 | Briefing Stage 2 | Naruto dan Konohamaru bersama melawan Sakura; map atap Akademi; target 4.000 Chakra; awal 2.000 tiap peserta |
| 54:56–87:10 | Stage 2, paruh pertama | Tiga pihak bergiliran; Sakura mengambil node bernilai tinggi; caltrops/trap tags; kartu +3 Kunai; battle antar barrier |
| 87:11–118:08 | Stage 2, paruh kedua | Naruto memakai Naruto Rendan (うずまきナルト連弾 — Kombo Naruto Uzumaki); Naruto mencapai 5.806 Chakra; Stage 2 Clear 大勝利 pada sekitar 117:59 |
| 118:09–121:00 | Briefing Stage 3 | Bell Test Team 7; Naruto, Sasuke, Sakura, Kakashi; target 4.000 Chakra; awal 2.000 per peserta |
| 121:01–146:00 | Stage 3 | Board empat pihak; Kakashi barrier Level 4 dengan toll 880; Sasuke memakai Fire Style (火遁・豪火球の術 — Elemen Api: Teknik Bola Api Besar) dan Sharingan (写輪眼); Naruto memakai 結界奪取 (Perebutan Barrier) dan berhasil mengambil node pada roulette takeover bernilai 10+ |
| 146:01–168:35 | Akhir Stage 3 | Kakashi memakai Raikiri (雷切 — Pedang Petir); Naruto bertahan dengan Sexy Jutsu (おいろけの術 — Teknik Seksi); Naruto mencapai 10.690 Chakra dan menang 大勝利 sekitar 167:57 |
| 168:36–171:40 | Challenge Stage | Tree Chakra Control Training (チャレンジステージ — Challenge Stage); Naruto vs Sasuke; target mencapai puncak pohon atau menghabiskan Chakra lawan yang dimulai dari 600; kartu/roulette mengubah langkah; Sasuke menang |
| 171:41–173:15 | Awal Stage 4 | Pengantar Land of Waves, Demon Brothers dan Zabuza; objective Mission 4: 5.000 Chakra, Kakashi ikut di pihak pemain; streamer membuat save state dan menghentikan sesi |

## Aturan / mekanisme kandidat dari observasi video

Status di bawah adalah **VIDEO-OBSERVED (hasil analisis visual otomatis)**, bukan kode game VERIFIED.

1. **Objective bervariasi per stage.** Stage 1 target 3.000 Chakra; Stage 2 dan Stage 3 target 4.000; Stage 4 dimulai dengan target 5.000. Jadi 3.000 bukan angka universal untuk semua Story Mode.
2. **Gerak papan memakai roulette bernomor.** Pada board Stage 1, hasil gerak biasa yang dilaporkan adalah 1–8. Kartu/item dapat memodifikasi langkah atau memberi gerak tetap (contoh kartu 7 langkah). Jangan menyebutnya dadu sebelum bentuk UI dan sumber RNG diverifikasi.
3. **Node dapat diklaim dengan barrier.** Mendarat di node netral memungkinkan pemain membayar Chakra untuk membangun barrier dan memiliki node itu; adegan menggambarkan Level 1.
4. **Barrier memiliki level dan toll.** Upgrade level terlihat sampai Level 5; node Level 4 Kakashi dilaporkan memiliki toll 880 dan node Sakura dapat melampaui 1.000. Nilai dan formula scaling belum dibuktikan.
5. **Node milik sendiri dapat ditingkatkan.** Landing pada node sendiri menawarkan upgrade; Level 3 dan Level 5 terlihat pada permainan Mizuki.
6. **Node bersebelahan dapat terhubung.** Analisis melaporkan node yang berdekatan meningkatkan nilai barrier/chain. Formula, aturan warna, dan apakah adjacency selalu memberi bonus masih UNKNOWN.
7. **Mendarat di node lawan memicu pembayaran toll dan/atau battle.** Adegan menampilkan pilihan pertahanan dan aksi teknik; apakah battle opsional atau wajib bergantung kondisi belum diketahui.
8. **Battle punya pilihan teknik dan roulette serang/bertahan.** Contoh yang dilaporkan: Shadow Clone Jutsu (多重影分身の術), guard/evasion, Naruto Rendan (うずまきナルト連弾), Fire Style (火遁・豪火球の術), Sharingan (写輪眼), Raikiri (雷切), dan Sexy Jutsu (おいろけの術). Roulette menyelesaikan damage terhadap durability barrier. Formula damage, biaya Chakra tiap aksi, dan urutan resolusi masih UNKNOWN.
9. **Barrier dapat dilemahkan atau dilepas saat ekonomi pemain buruk.** Mizuki mengalami saldo negatif dan barrier release 結界開放. Syarat pemilihan node yang dilepas, urutan likuidasi dan formula belum diketahui.
10. **Scroll/kartu memberi efek beragam.** Efek yang dilaporkan mencakup gerak tetap, pemulihan Cup Ramen +50, trap/caltrops, attack boost +3 Kunai, dan teknik perebutan barrier. Identitas lengkap tiap kartu serta timing efek masih UNKNOWN.
11. **Perebutan node dapat menggunakan roulette terpisah.** Naruto mengambil Level 4 barrier Kakashi dengan hasil takeover 10+. Itu tidak sama dengan roulette gerak biasa 1–8; mekanisme/ruang angka harus dianalisis terpisah.
12. **Challenge Stage tree climbing adalah minigame terpisah.** Pemenang mencapai puncak terlebih dahulu atau kondisi Chakra lawan habis seperti yang dilaporkan; kartu dapat menambah/mengurangi langkah. Apakah hasilnya memengaruhi reward/branching Story masih UNKNOWN.
13. **Story berlanjut setelah tiga stage dan minigame.** Video baru menunjukkan briefing Stage 4 Land of Waves dan objective 5.000; video ini tidak menunjukkan penyelesaian Stage 4.

## Cross-check dengan transkrip

- Transkrip menyebut target 3.000; analisis visual memperlihatkan angka target stage-spesifik 3.000, 4.000, 4.000, lalu 5.000. Koreksi penting: jangan membuat aturan "semua stage harus 3.000".
- Ucapan streamer tentang "dadu" lebih aman dicatat sebagai roulette gerak 1–8 pada adegan yang dianalisis.
- Klaim "kunai dua kali bisa menghapus tile" belum terkonfirmasi oleh scene breakdown. Yang terlihat dilaporkan adalah +3 Kunai sebagai kartu/attack boost dan damage battle pada barrier.
- Klaim trap dapat membuat lawan mundur atau tidak bergerak belum punya detail visual cukup untuk menetapkan efek. Catat jenis trap dan state sebelum/sesudah pada frame mendatang.
- Scroll tidak boleh dianggap sebagai syarat wajib menang. Scene breakdown mengindikasikan scroll/kartu adalah sumber aksi/efek, sedangkan win banner terkait target Chakra dan node milestone.
- Klaim formula battle "stat lebih tinggi pasti menang" terlalu sederhana. Analisis visual melaporkan teknik, biaya Chakra, roulette serang/bertahan, dan damage durability barrier; tidak mengungkap formula lengkap.

## Matriks kepastian

### Teramati pada video menurut analisis visual
- Mode Story/Party/Bingo Book/Settings.
- Misi 1–3 selesai dengan banner 大勝利; target stage berbeda.
- Node/barrier Level 1–5, toll, upgrade, roulette gerak 1–8 pada adegan board Stage 1.
- Pilihan teknik battle, roulette battle, kartu/scroll, dan barrier release.
- Challenge Stage tree climbing.
- Briefing awal Stage 4 dengan target 5.000; belum selesai.

### Hipotesis aturan yang masih memerlukan pengujian ROM
- Rumus nilai barrier dan bonus adjacency.
- Rumus toll dan waktu pungutan.
- Cara pemilihan barrier yang di-release saat saldo negatif.
- Range/probabilitas roulette gerak dan roulette battle.
- Damage formula, defense, teknik spesial, biaya Chakra, durability.
- Syarat pasti kemenangan: ambang Chakra, milestone node, urutan langkah, dan apakah ada kondisi alternatif.
- Aturan detail scroll, trap, kunai, dan minigame reward.

### UNKNOWN
- Kode state internal, struktur data board, generator angka acak, AI policy.
- Semua nama Jepang item yang tidak dibaca jelas.
- Apakah seluruh stage Story memakai aturan yang sama.
- Isi lanjutan Stage 4 dan stage setelahnya.
- Apakah urutan scene dan setiap angka tepat tanpa inspeksi frame mentah.

## Rekomendasi urutan verifikasi ROM

1. **Stage 1 goal gate:** bedakan target 3.000 dari trigger victory pada node milestone; catat Chakra persis sebelum/sesudah mencapai node.
2. **Node ownership & level:** uji netral → Level 1 → upgrade 2–5, perubahan Chakra, toll, durability, dan efek adjacency.
3. **Opponent node:** uji toll vs battle dan kondisi kapan pilihan muncul.
4. **Battle roulette:** pisahkan roulette gerak 1–8 dari takeover 10+ dan roulette attack/defense; rekam setiap hasil/aksi.
5. **Bankruptcy/barrier release:** identifikasi ambang saldo negatif, urutan barrier yang dilepas, dan nilai Chakra yang dipulihkan.
6. **Cards/traps:** satu efek per uji; catat board state dan langkah sebelum/sesudah.
7. **Story progression:** simpan stage outcomes, challenge result, dan transisi Stage 4 tanpa menyamakan minigame dengan match papan.

**Safety/evidence gate:** gunakan checkpoint emulator yang sah dan sudah diverifikasi; jangan memindahkan atau mengomit ROM, BIOS, Memory Card, savestate, dump RAM, ataupun screenshot privat ke repo. Jangan membuat input gameplay atau mengubah status Story Mode berdasarkan analisis video saja.
