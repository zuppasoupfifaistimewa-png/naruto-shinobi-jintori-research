# Sumber dan catatan evidensi

Dokumen ini mencatat sumber yang digunakan untuk memverifikasi identitas permainan dan memperoleh petunjuk gameplay. Sumber eksternal membantu orientasi; **bukan pengganti penelusuran kode ROM**.

## Data disc dan identitas

1. **GameGear Archive — Naruto - Shinobi no Sato no Jintori Gassen (PS1, 2003)**  
   https://gamegear.net/archive/games/psx/naruto-shinobi-no-sato-no-jintori-gassen-japan  
   Mencatat serial SLPS-03553 dan CRC32 dfe1f8b3 untuk dump BIN. Halaman juga menyatakan sebuah file CHD hasil repack pernah boot pada test rig Mednafen PSX HW dalam sesi otomatis 64 detik (tanggal pengujian yang ditampilkan situs: 27 Juni 2026). Itu adalah bukti kompatibilitas/boot dari pihak ketiga, bukan verifikasi formula gameplay oleh penelitian ini.

2. **PSX Data Center — SLPS-03553**  
   https://psxdatacenter.com/games/J/N/SLPS-03553.html  
   Referensi identitas rilis: judul, nomor serial, region NTSC-J, platform, genre, publisher/developer, dan tanggal rilis.

3. **TV Tokyo — halaman produk PlayStation Naruto**  
   https://www.tv-tokyo.co.jp/anime/naruto2002/goods/playstation.html  
   Materi promosi resmi era 2003 mengenai mode Story/Versus, pertarungan saat memasuki wilayah lawan, dan Scroll of Seals. Ini deskripsi tingkat tinggi, bukan spesifikasi teknis.

## Transkripsi/terjemahan komunitas

4. **Naruto PS1 English translation — Story Mode**  
   https://github.com/juanoliveira82/naruto-ps1_translation-english/blob/master/Story-mode.md  
   Dipakai sebagai petunjuk membaca teks UI, termasuk skenario awal. Terjemahan fan-made; istilah dan konteks harus diperiksa silang.

5. **Naruto PS1 English translation — Cards**  
   https://github.com/juanoliveira82/naruto-ps1_translation-english/blob/master/Cards.md  
   Dipakai sebagai petunjuk deskripsi kartu. Belum membuktikan seluruh implementasi setiap efek.

6. **Panduan Jepang / unlock dan kondisi Party Mode**  
   https://uw.netlify.app/details/ps/2079  
   Mencatat syarat membuka karakter, map, dan beberapa kondisi kemenangan Party Mode tambahan. Panduan eksternal; perlu pencocokan dengan flag/record game.

7. **Retogenofu — ulasan gameplay Jepang, 20 Maret 2025**  
   https://retogenofu.hatenablog.com/entry/2025/03/20/NARUTO%E3%83%BB%E5%BF%8D%E3%81%AE%E9%87%8C%E3%81%AE%E9%99%A3%E5%8F%96%E3%82%8A%E5%90%88%E6%88%A6_%E3%82%A2%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%8B%E3%81%A8  
   Menjelaskan roulette, barrier petak kosong, kenaikan level/pendapatan, dan serangan pada barrier lawan. Merupakan ulasan sekunder.

8. **Raido — staff credits PS1 Jepang**  
   https://raido.moe/staff/ps1/ps1_naruto.html  
   Referensi kredit staf dan developer/publisher. Tidak digunakan untuk menyimpulkan aturan gameplay.

## Cara mengutip sumber di dokumen

- Tandai sumber kode jika kesimpulan benar-benar ditarik dari instruksi/header/data ROM yang diperiksa.
- Untuk sumber UI terjemahan, sebutkan “contoh dari transkripsi komunitas”.
- Untuk panduan/ulasan, sebutkan “menurut sumber eksternal”.
- Hindari menyalin teks panjang sumber. Ringkas efek atau informasi dengan bahasa sendiri dan tautkan sumbernya.
- Jika sumber eksternal tidak cocok dengan runtime atau kode, catat pertentangan; jangan diam-diam memilih salah satu.

## Hash file

Hash ROM yang diperiksa dicatat di docs/ROM_STRUCTURE.md. CRC32 cocok dengan GameGear Archive. SHA-256 dicatat dari pemeriksaan lokal, tetapi tidak ada pernyataan di dokumen ini bahwa SHA-256 tersebut diverifikasi secara independen oleh GameGear Archive.