# Status penelitian

## Hasil A/B backend GPU — 2026-10-17

Run [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) menguji fastboot OpenBIOS yang sama pada PCSX-Redux AnyLinux tanpa `-softgpu`, memakai backend OpenGL default melalui Mesa llvmpipe. Kapabilitas GL terkonfirmasi: vendor Mesa, renderer `llvmpipe (LLVM 21.1.8, 256 bits)`, OpenGL 3.3 Compatibility Profile. Capture berasal dari jendela PCSX non-root `0x200034` / XID 2097204, 1280×800. Seluruh frame sebelum input, setelah Return/Cross, dan pada 40/65/90 detik tetap uniform black (mean 0, stddev 0, satu warna); OCR kosong. Tidak ada callback pembaca register CPU. Log fastboot tetap mencapai SYSTEM.CNF/BOOT, `EXEC:PC0(80011448)`, `Execute !`. Jadi backend OpenGL default pun belum membuat title/menu terlihat.
- Artifact privat `12094736241`, cleanup berhasil.
- Hipotesis berikut yang paling informatif adalah mengambil snapshot PC CPU dari luar emulator melalui GDB remote (bukan Lua/VSync callback), untuk membedakan loop pasca-entry dari masalah rendering tanpa mencetak trace instruksi mentah.
**RT-001 tetap Open / blocked.** Story Mode belum dimulai; belum ada aturan gameplay runtime yang terverifikasi.


## Hasil capture fastboot yang sah — 2026-10-17

Run [#39015722771](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015722771) kini menghasilkan capture valid jendela aplikasi PCSX-Redux, XID 2097204 (`0x200034`), 1280×800. Selector membaca `xwininfo -root -tree`, mengecualikan root 543/`0x21f`, dan memakai non-root window bernama `PCSX-Redux`. Lima capture (sebelum input, sesudah Return/Cross, 40/65/90 detik) semuanya uniform black (mean 0, stddev 0, satu warna); OCR kosong. Ini bukan lagi masalah salah mengambil root. Port 1 Analog tetap dikonfigurasi dan input telah dikirim ke jendela aplikasi, tetapi tidak ada perubahan visual/game yang bisa diverifikasi. Tidak ada pembacaan register CPU di callback VSync. Log fastboot mencapai `SYSTEM.CNF`, `BOOT`, `EXEC:PC0(80011448)`, `Execute !`.
Run berikut [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) mengganti satu variabel grafis: menghapus `-softgpu`, mengaktifkan Mesa llvmpipe/OpenGL 3.3, dan mencatat kapabilitas GL. Status saat dicatat: in progress.
**RT-001 tetap Open / blocked** sampai title/menu dikenali dan input nyata menghasilkan perubahan game.


## Koreksi pemilihan window X11 — fastboot probe terbaru, 2026-10-17

Run [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649) benar-benar mengecualikan root, tetapi pencarian kandidatnya masih memakai `xdotool search`; hasilnya tidak mengembalikan aplikasi. Potongan `xwininfo -root -tree` di log menunjukkan child window nyata `0x200034 "PCSX-Redux"`, 1280×800. Jadi kesimpulan yang benar: window ada tetapi selector gagal memilihnya; tidak ada gambar emulator yang diambil. Marker fastboot dari log tetap mencapai `SYSTEM.CNF`, `BOOT`, `EXEC:PC0(80011448)`, `Execute !`.
Workflow diperbarui pada commit `1acd87e9960c0caeb334cffc48ed8aea212212e1` agar mengekstrak XID langsung dari tree, mengecualikan root, dan memakai `windowfocus` sebelum input. Rerun [#39015610296](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015610296) telah dipicu; status awal queued.
**Belum ada capture GUI fastboot yang sah dan belum terbukti title/menu. RT-001 tetap Open / blocked.**


## Koreksi validitas capture fastboot — 2026-10-17

Audit log run [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) menemukan bahwa ID window `543` sama dengan root Xvfb `0x21f`. Selector `xdotool search --onlyvisible --name '.*'` ternyata memasukkan root, sehingga semua metrik hitam dan OCR kosong dari run ini **bukan** capture jendela emulator dan harus ditarik dari bukti visual. Marker boot tetap sah: fastboot BIOS mencapai `SYSTEM.CNF`, BOOT, `EXEC:PC0(80011448)`, dan `Execute !`.
Run [#39015290594](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015290594) menggunakan selector sama dan juga tidak boleh dianggap sebagai capture game bila memilih root; ia sedang digantikan oleh run [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649). Workflow telah diperbaiki pada commit `83173bb10cfbf905a296f59720c0a63c95bc3a32` untuk mengecualikan root ID secara eksplisit sebelum memilih jendela non-root yang layak. Verifikasi hasil run baru dari `X11_ROOT_ID`, `WINDOW_CANDIDATE_SKIPPED=root`, dan `CAPTURE_WINDOW` non-root sebelum menilai gambar.
**RT-001 tetap Open / blocked.** Sampai capture non-root yang sah menunjukkan Naruto dan kontrol merespons, tidak ada bukti title/menu/gameplay.


## Hasil fastboot GUI dengan window discovery generik — 2026-10-17

Run [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) berhasil mengidentifikasi jendela X11 (ID `543`, 1280×800); jadi tangkapan sebelumnya yang gagal mencari nama jendela adalah masalah selector, bukan bukti tidak ada window. Namun semua frame sebelum input, sesudah Return, sesudah Z/Cross, serta 40/65/90 s tetap uniform black (mean 0, stddev 0, satu warna), OCR kosong. Log fastboot kembali mencapai `SYSTEM.CNF`, `BOOT`, `EXEC:PC0(80011448)`, dan `Execute !`. Input memang dikirim ke jendela aplikasi, tetapi karena layar tetap hitam, belum bisa ditafsirkan sebagai kontrol game.
Uji berikut [#39015290594](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015290594) mengulangi fastboot yang sama tanpa pembacaan register CPU di event VSync, karena instrumentasi tersebut pernah mengganggu eksekusi di eksperimen terdahulu. Status saat dibuat: queued. **RT-001 tetap Open / blocked.**


## Hasil eksperimen terbaru — 2026-10-17

### Source-current PCSX-Redux
Run [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) selesai dengan semua langkah workflow `success`: source PCSX-Redux pin `1525a93676dbece9fe70f10ff129aeaa14eec30d` berhasil dibangun, tetapi jendela emulator yang benar-benar ditangkap pada detik 20/40/60/80/95 seluruhnya uniform black (1280×800, mean 0, stddev 0, satu warna), OCR kosong. Log mengenali disc `SLPS-03553` dan OpenBIOS, mencatat Port 1 Analog tersambung, tetapi hanya sampel PC frame 300=`0x000015a4`; tidak ada pembacaan `SYSTEM.CNF`/BOOT atau entry executable. Artifact privat `12094116949` berisi 5 frame hitam dan stdout. Cleanup sukses. Keberhasilan build dan Actions tidak berarti game boot.
### OpenBIOS fastboot vs chunked
Run [#39013612865](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39013612865) menguji build AnyLinux sama dengan dua BIOS. Varian fastboot membaca `SYSTEM.CNF`, `BOOT`, lalu mencatat `EXEC:PC0(80011448)` / `Execute !`. Varian chunked hanya menunjukkan pembacaan payload satu sektor sampai indeks 40 sebelum log berhenti. Namun window detector lama tidak menemukan jendela untuk kedua varian, jadi tidak ada capture visual dan urutan input dilewati. Hasil ini mengisolasi beda jalur loader, bukan bukti title/menu.
### Eksperimen berikutnya
Workflow privat baru [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) memakai fastboot OpenBIOS dan enumerasi generik jendela X11, bukan hanya mencari caption “PCSX”. Status awal: queued; periksa hasil aktualnya.
**RT-001 tetap Open / blocked:** title/menu Naruto dan input game yang responsif belum terbukti. Story Mode belum dimulai/tamat.


## Hasil final DuckStation probe — 2026-10-17

- Run [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) berhasil membuka jendela setelah paket `libegl1` ditambahkan. Capture 760×498 konsisten menampilkan first-run setup wizard DuckStation, termasuk halaman BIOS.
- Layar BIOS secara eksplisit menyatakan DuckStation membutuhkan BIOS PS1/PS2; UI mendeteksi satu berkas BIOS tetapi tetap menyatakan tidak ada BIOS yang dapat dipakai. Log hanya menunjukkan BIOS dipetakan dan pencarian Auto BIOS; tidak ada marker disc/executable Naruto. Return bergerak di wizard; Z/Cross tidak terbukti mencapai game. Ini bukan tes kompatibilitas ROM yang tuntas.
- Artifact privat `12094155047` berisi 8 screenshot dan stdout. Ditinjau lokal untuk membedakan wizard BIOS dari layar game; salinan ZIP/gambar lokal sementara kemudian dibersihkan. Cleanup workspace runner sukses.
- **Tidak meminta atau mengunduh BIOS retail baru.** Dalam batas hanya memakai OpenBIOS yang sudah tersedia, DuckStation saat ini terblokir pada validasi BIOS; emulator ini tidak dinilai sebagai gagal kompatibilitas Naruto.
- PCSX-Redux source-current [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih membangun source ketika terakhir diperiksa; itu jalur prioritas selanjutnya.
- **RT-001 tetap Open / blocked.** Belum ada title/menu Naruto terverifikasi dan belum ada input game terverifikasi.


## Pembaruan status terbaru — 2026-10-17, hasil DuckStation setelah perbaikan GL

- Rerun [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) juga menyelesaikan workflow `success`, tetapi DuckStation keluar dengan kode 127 sebelum membuat jendela: `libEGL.so.1: cannot open shared object file`. Tidak ada frame, OCR, input, atau bukti boot BIOS/disc. Artifact 292 byte tidak berisi PNG.
- Workflow diperbarui lagi pada commit `5afd32eca0d32ee191de7f2963f74b53aed89448` dengan paket `libegl1`. Rerun [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) sedang berada pada langkah boot/capture ketika terakhir diperiksa.
- PCSX-Redux source-current [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih membangun source; belum ada frame yang dapat dinilai.
- **RT-001 tetap Open / blocked.** Belum ada title/menu Naruto dan respons input yang terverifikasi.


## Verifikasi terbaru — 2026-10-17, DuckStation probe dan source-current GUI

- Run privat [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) berakhir dengan conclusion Actions `success`, tetapi **DuckStation tidak diluncurkan**: log aktual menunjukkan `AppRun: error while loading shared libraries: libOpenGL.so.0: cannot open shared object file`. Tidak ada jendela DuckStation, frame/OCR game, input terkirim, atau bukti BIOS/disc dari proses emulator. Artifact ZIP (ID `12093451882`, 293 byte) hanya berisi `duckstation.stdout` sepanjang 183 byte; tidak ada PNG.
- Harness telah diperbaiki pada commit `058aadea1c664712b62a63cf01fcb3e5598ef047`: pasang paket `libopengl0 libglx0 libgl1` dan unggah `captures/*.png` (sebelumnya glob `frame-*.png` tidak cocok dengan nama file capture). Rerun aktual [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) telah dimulai; periksa hasil finalnya.
- Source-current PCSX-Redux [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih pada tahap build source saat diperiksa. Belum ada frame GUI atau OCR yang bisa dinilai.
- Cleanup private workspace pada DuckStation run awal berhasil. Tidak ada bukti title/menu atau input gameplay.
- **RT-001 tetap Open / blocked** sampai title/menu Naruto dikenali secara visual dan respons input terkontrol dibuktikan.


## Uji emulator alternatif tambahan — 2026-10-17

Workflow privat [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) kini menguji rilis DuckStation resmi, dengan AppImage SHA-256 `c5e6f045f6a242082fcafa9f02d56ad895e233b942728788d232ad0c0c765c24`, ROM yang sama dan OpenBIOS `openbios.bin` dari private release. Harness Xvfb mengambil frame jendela dan mengirim Return/Cross lewat pemetaan keyboard sementara, lalu menyimpan capture sebagai artifact privat 3 hari dan menghapus workspace. Status saat catatan ini dibuat: queued; belum ada hasil boot/menu/input yang bisa disimpulkan. Ini uji kandidat, bukan klaim kompatibilitas.

## Pembaruan runtime terbaru — 2026-10-17

- GUI baseline AnyLinux tetap belum membuktikan title/menu: jendela ada tetapi hitam, log GUI belum menyelesaikan pemuatan executable; jalur headless pada build tersebut mencapai 187 chunk dan `EXEC:PC0(80011448)`.
- Run privat [#39011515345](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011515345) mengonfirmasi screenshot Lua pada mode `-no-ui` mengembalikan ukuran 0×0; proses mencapai handoff executable tetapi capture tidak valid dan postprocess gagal. Cleanup berhasil, artefak gambar tidak tersedia.
- Tes source GUI baru [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) memakai source PCSX-Redux pin `1525a93676dbece9fe70f10ff129aeaa14eec30d` (HEAD upstream yang diverifikasi pada saat workflow dibuat), sedang berjalan saat catatan ini ditulis. Source pin CPU-trace sebelumnya 24 commit di belakang.
- Workflow retensi [#39011611436](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39011611436) sukses menghapus run publik lama `#39001985849` secara spesifik. Fetch API untuk run itu sesudah penghapusan mengembalikan 404.
- **RT-001 tetap Open / blocked.** Tidak ada bukti visual title/menu Naruto, input terkontrol, atau gameplay Story Mode. Jangan mengklaim Story Mode dimulai atau tamat.

Terakhir dirangkum: 2026-10-17

## Ringkasan

**Status: analisis statis awal dengan jejak konfigurasi target Chakra yang lebih kuat; belum lengkap dan belum tervalidasi melalui debugging gameplay.**

**Sumber wajib:** kuota internet pengguna sangat terbatas. Jangan meminta upload ROM/ISO sekitar 300 MB dan jangan mengandalkan ROM laptop. Gunakan file hasil ekstraksi di Library pada /Naruto Research Files/. Jika tidak dapat diakses, laporkan kendala alih-alih meminta upload ulang.

Pemeriksaan sebelumnya mengekstrak struktur ISO dari dump PS1 raw-sector, membaca SYSTEM.CNF, mengidentifikasi executable utama, melakukan inspeksi/disassembly awal MIPS, dan menemukan beberapa struktur serta jalur kode. Namun, pemetaan overlay belum lengkap, rumus gameplay belum seluruhnya terhubung ke semua pemanggil, dan sesi emulator/debugger terkontrol belum dijalankan.

## Temuan yang didukung langsung oleh kode/data ROM

1. Executable boot yang dirujuk SYSTEM.CNF adalah SLPS_035.53.
2. Header executable mencatat alamat muat 0x80010000, PC 0x80011448, dan text size 0x5D800.
3. Struktur pemain yang diakses beberapa getter/setter memiliki empat slot; stride struktur 0xB4 byte dan nilai Chakra pada offset +0x18.
4. Setter Chakra yang diperiksa membatasi nilai tersimpan pada rentang -9.999 sampai 99.999. Ini bukan kondisi menang/kalah.
5. Jalur kode membandingkan Chakra pemain dengan target konfigurasi dari getter 0x80012A70; jika kondisi target terkait (bit 0x200) aktif, Chakra yang mencapai/melewati target dapat menetapkan pemain sebagai pemenang. Tabel konfigurasi utama memuat pasangan awal/target 1.500/3.000, 2.000/4.000, 2.500/5.000, 3.000/6.000 serta dua record awal 600/0 yang kondisi pemilihannya belum dipetakan. Jadi 3.000 bukan target universal.
6. Data petak diperlakukan sebagai bitfield; jalur yang diperiksa memakai empat bit teratas sebagai ID pemilik. Arti seluruh bit lainnya belum terpetakan.
7. Kode memeriksa sejumlah flag kondisi akhir, tetapi label yang sesuai dengan semua pilihan menu belum terpetakan secara lengkap.

Alamat dan penjelasan lebih detail ada di docs/ROM_STRUCTURE.md, docs/OVERLAY_MAP.md, dan docs/GAME_RULES.md.

## Temuan dari UI terjemahan/panduan eksternal — bukan bukti formula universal

- Story stage 1 diterjemahkan sebagai Naruto melawan Mizuki dengan target 3.000 Chakra.
- Dalam contoh tampilan, biaya membangun barrier ditampilkan 60 Chakra; suatu contoh barrier level 1 menampilkan nilai 100 dan durability 2/2; suatu contoh peningkatan level 1 ke 2 menampilkan biaya 150.
- Sumber lain menampilkan barrier level 1 bernilai 50, sehingga nilai tidak boleh dianggap tetap tanpa memahami parameter/tipe barrier dan konteksnya.
- Beberapa deskripsi kartu memberi contoh penambahan Chakra, peningkatan statistik, atau manipulasi roulette.

Contoh UI di atas belum membuktikan bahwa 60 dan 150 adalah biaya universal atau bahwa formula seluruh barrier sudah diketahui.

## Pekerjaan terbuka utama

- Petakan loader, offset file, alamat muat, ukuran, entry point, dan lifecycle untuk seluruh overlay.
- Lanjutkan reverse-engineering format resource yang kini terindeks melalui direktori di DATA.BIN; format PK02/BIN0/TPK0, NARUTOSceneV001, PSQ0/PSQ1, serta tujuan penuh XASECT.BIN masih belum diketahui.
- Temukan dan dokumentasikan sumber setiap harga barrier, biaya upgrade, pendapatan, nilai, level, dan durability.
- Petakan seluruh bitfield petak dan struktur barrier berdasarkan pembacaan serta penulisan field.
- Identifikasi jalur transaksi Chakra untuk bangun/upgrade/pendapatan/serangan/kartu dan efek pembatas nilainya.
- Hubungkan setiap flag kondisi menang ke record skenario, pilihan menu, dan tampilan teks.
- Telusuri algoritma roulette dan efek semua kartu sampai ke pemanggil sebenarnya.
- Jalankan skenario terkontrol di emulator/debugger dan bandingkan perubahan memori dengan analisis statis.

## Batas lingkungan saat ini

Pada pemeriksaan sebelumnya, tidak ditemukan emulator PS1 yang tersedia di lingkungan analisis; percobaan eksekusi terminal/Python berikutnya juga gagal karena lingkungan menolak eksekusi. Karena itu belum ada log eksekusi gameplay dari sesi kita. Laporan GameGear Archive bahwa ROM boot di test rig Mednafen adalah sumber eksternal dan bukan pengujian khusus biaya atau rumus permainan.

## Status confidence

- **Tinggi untuk metadata disc/EXE**: didukung header, SYSTEM.CNF, ukuran, hash, dan pencocokan CRC eksternal.
- **Tinggi untuk batas setter Chakra**: instruksi setter terlihat dan rentang penjepitan nilai telah diidentifikasi.
- **Menengah untuk cabang target skenario awal**: nilai target dari record konfigurasi dan jalur perbandingan ditemukan; pemetaan lengkap semua skenario tetap terbuka.
- **Rendah/belum pasti untuk biaya dan formula gameplay**: belum ada call chain lengkap ditambah tes runtime terkontrol.

## Pembaruan hasil pemeriksaan lokal — 2026-10-15

Pemeriksaan byte-level terhadap salinan kerja ROM mengonfirmasi temuan baru berikut. Hasil ini **statis**; belum ada tes gameplay terinstrumentasi.

- SHA-256 ROM cocok dengan catatan yang sudah ada: `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`.
- Di executable utama, offset file `0x46098` (alamat runtime `0x80055898`) berisi pasangan little-endian `0xD4, 0x2F44`: LBN 212 dan panjang 12.100 byte, yang menunjuk ke awal `DATA.BIN`.
- Awal `DATA.BIN` terdiri dari bootstrap sepanjang `0x44) byte diikuti direktori `0x2F00) byte: 1.504 entri × 8 byte, paling kuat ditafsirkan sebagai pasangan `(LBN, byte_length)`.
- 1.500 entri tidak kosong dan 4 kosong (indeks 1491–1494). Semua interval sektor entri aktif berada dalam rentang `DATA.BIN` dan tidak tumpang-tindih; direktori mencakup 32.227 dari 32.234 sektor file.
- Klasifikasi signature awal atas 1.500 resource aktif: 921 `PK02`, 246 struktur TIM valid, 126 `NARUTOSceneV001`, 125 signature lain berawalan `NARU`, 6 `PSQ0`, 2 `PSQ1`, 1 `TXT2`, dan 73 belum diklasifikasikan. Pemindaian longgar mendeteksi 264 kandidat magic TIM; 18 gagal validasi struktur dan tidak dihitung sebagai TIM valid.
- `XASECT.BIN` berisi hitungan 86 diikuti 86 pasangan 32-bit. Konsumen di sekitar `0x80019468` mengindeks pasangan dengan `input >> 4) dan memakai field pertama sebagai offset aditif. Arti semantik lengkap field dan kaitan field kedua dengan stream/media masih belum pasti.

Lihat [docs/RESOURCE_CATALOG.md](docs/RESOURCE_CATALOG.md) untuk hitungan, batas inferensi, hash file hasil ekstraksi, serta langkah analisis berikutnya. Handoff lintas-chat ada di [HANDOFF_LANJUT.md](HANDOFF_LANJUT.md).


## Persistensi file untuk analisis lintas chat

File ekstraksi disimpan di Library ChatGPT pada folder `Naruto Research Files`; `DATA2.BIN` tersedia sebagai ZIP terkompresi. Baca tabel lokasi pada `HANDOFF_LANJUT.md` dan verifikasi hash sesudah pemulihan sebelum melanjutkan analisis.


## Pembaruan analisis aturan gameplay — 2026-10-15

- Tabel konfigurasi executable 0x80057798 ber-stride 0x54; tabel kedua 0x80064918 ber-stride 0x30. Field +0x04 dipakai sebagai Chakra awal, field +0x08 sebagai target pada cabang kemenangan, sementara makna field +0x0C belum ditemukan.
- Nilai teramati pada tabel pertama mencakup 1500/3000, 2000/4000, 2500/5000, 3000/6000; ada dua record 600/0 yang tidak boleh ditafsirkan sebagai kemenangan instan.
- Label lama 0x800EC200 sebagai pembanding target Chakra dan 0x800F70D0 sebagai aritmetika Chakra dicabut karena base/identitas modul belum diverifikasi.
- File Library yang digunakan pada sesi ini: SLPS_035.53, DATA.BIN, XASECT.BIN, DATA2.BIN hasil unzip. Hash DATA2.BIN hasil unzip cocok: be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9.
- Belum ada tes runtime. Prioritas berikutnya: transaksi biaya bangun/upgrade, income, perubahan kepemilikan dan transaksi battle melalui pemanggil setter Chakra dan label event ESTATE/LVUP_ESTATE.


## Trace aturan Chakra — tambahan 2026-10-15

- Kode pembanding target di resource gameplay (base hipotesis 0x800D0000) memastikan syarat cabang target adalah Chakra saat ini >= target konfigurasi bila bit kondisi 0x200 aktif. Target dibaca lewat getter 0x80012A70. Alamat resource masih statis sementara karena loader belum diverifikasi runtime.
- Pemanggilan setter Chakra 0x8001387C banyak berupa sinkronisasi salinan record. State machine sementara pada resource DATA.BIN membentuk +0xB40 dari +0xB30 + +0xB38, lalu pada state +0xB2A == 7 memproses jumlah pending +0xB44 bertahap ke Chakra pemain +0xB2B. Sumber operand dan semantik event belum ditemukan; ini bukan bukti biaya barrier.
- Karena sumber nilai transaksi belum terhubung, biaya build/upgrade universal masih belum terbukti. Angka 60 dan 150 hanya tercatat pada contoh UI tertentu dalam transkripsi komunitas.


## Status emulator/runtime — 2026-10-15

- Emulator/debugger kini ditetapkan sebagai jalur riset utama untuk memvalidasi aturan, bersama reverse-engineering statis; bukan sekadar alternatif opsional.
- Diprioritaskan PCSX-Redux karena dokumentasi resminya mendukung CPU debugger, breakpoint dan GDB server; Mednafen dapat digunakan untuk cek silang. Rujukan dan protokol uji ada di [docs/EMULATOR_WORKFLOW.md](docs/EMULATOR_WORKFLOW.md).
- Pada awal sesi executable emulator tidak tersedia dan DNS container gagal. PCSX-Redux kemudian diunduh dari GitHub Actions artifact/release, diverifikasi, dan antarmukanya berhasil dijalankan lewat Xvfb. Namun, belum ada bukti bahwa game mencapai menu/title atau bahwa gameplay sudah diuji.
- ROM di Library berhasil dimaterialisasikan dan SHA-256 cocok; tidak dibutuhkan upload ulang dari laptop pengguna.


## Emulator tersimpan di repo — 2026-10-15

- PCSX-Redux Linux x86_64 AppImage diunggah sebagai Release asset di [research-emulator-pcsx-redux-2026-10-15](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15), bukan Git history. Ukuran 65.747.557 byte; SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c. GitHub Actions run 38692549397 sukses mendownload dan memverifikasi binary.
- AppImage dapat diluncurkan di Xvfb, tetapi layar menunjukkan “No BIOS loaded, emulation halted”; belum ada boot game ataupun uji gameplay.
- Workflow build OpenBIOS open-source ada di .github/workflows/build-openbios.yml. Run #38693358323 membangun varian shell/menu dan run #38693918169 membangun shell/menu plus `BOOT_MODE=fast`. Hash fastboot `openbios.bin`: 25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d; hash ELF: 2c8d36e2179841935a1d1331777380502cdb22528d086c99c6388cdcfa54b8aa. Uji lokal fastboot menghasilkan layar hitam dan belum membuktikan Naruto mencapai title/menu. OpenBIOS bukan BIOS retail Sony.
- Jangan meminta upload ulang ROM. ROM hash diverifikasi dari Library; CUE dibuat untuk BIN raw-sector MODE2/2352.


## Update OpenBIOS — 2026-10-15

- Run [#38693358323](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693358323) berhasil membangun OpenBIOS dari source upstream PCSX-Redux pada commit 0c3572c3db75f97542001e453ae80ba8c3f8acba dan melampirkan asset ke release.
- Varian OpenBIOS default: `openbios.bin` 524.288 byte, SHA-256 `713ea2aed58606282b3ff5e91d77f8c5892ea36f5adcd279d2c7dd26604a625d`; ELF debug `openbios.elf` SHA-256 `d0d4cc73c9546e1e6af86d38ec894f5a6c81090ccdf97b1a3a39885c56af7bfc`. Checksum lengkap di release asset `OPENBIOS-SHA256SUMS`.
- Uji lokal dengan BIOS ini tidak lagi menampilkan pesan “No BIOS loaded”, tetapi frame yang terekam berupa bentuk geometris/gelap tanpa menu atau title game yang dapat dikonfirmasi. Ini belum membuktikan boot Naruto.
- [Run #38693918169](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693918169) sedang membangun varian `BOOT_MODE=fast` yang melewati shell BIOS dan mencoba boot CD secara langsung, bersama varian shell/menu normal. Periksa hasil workflow dan hash sebelum menggunakan asset tersebut.


## Hasil varian OpenBIOS fastboot — 2026-10-15

- Run [#38693918169](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38693918169) sukses membangun dua variant dan mengunggahnya ke release. Varian `openbios.bin` memakai `BOOT_MODE=fast` untuk mencoba boot CD langsung; varian shell/menu tersedia sebagai `openbios-shell.bin`.
- SHA-256 fastboot `openbios.bin`: `25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d`; `openbios.elf`: `2c8d36e2179841935a1d1331777380502cdb22528d086c99c6388cdcfa54b8aa`. Asset release dan `OPENBIOS-SHA256SUMS` tersedia pada [research kit release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15).
- Uji lokal varian fastboot: PCSX-Redux dijalankan dengan OpenBIOS, interpreter, debugger, dan CUE ROM. Layar tetap hitam setelah sekitar 12 detik; log tidak menyatakan BIOS hilang tetapi tidak ada title/menu yang dapat dikonfirmasi. Status: **boot game belum terverifikasi**, bukan test runtime berhasil.
- Workflow diperbarui agar artifact runtime-kit menyertakan shell/default dan fastboot sekaligus, bukan checksum yang merujuk file yang tak ada. Run terbaru akibat perbaikan ini harus diperiksa.

## Status runtime terbaru — 2026-10-16

Game masih belum terkonfirmasi mencapai title/menu; belum ada tes gameplay runtime yang selesai. PCSX-Redux dan varian OpenBIOS diagnostik tersedia pada [release research kit](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15).

- Jalur disc normal: mengenali label `SLPS-03553`, membuka `SYSTEM.CNF;1`, menguraikan `BOOT = cdrom:\\SLPS_035.53;1`, lalu berhenti di `boot file ...` sebelum `EXEC:PC0(80011448)`.
- Main executable: 385.024 byte; payload 382.976 byte (`0x5D800`, 187 sektor setelah header 2.048 byte).
- Chunk 8 sektor berhenti pada log sebelum syscall pertama selesai (`bytes=16384`); chunk 1 sektor berhasil menunjukkan progres pembacaan 2.048 byte, tetapi uji singkat belum membuktikan seluruh payload selesai atau game tampil. Build/asset varian satu sektor sukses melalui [Actions #38697240018](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/38697240018).
- Injeksi executable diagnostik mencapai `EXEC:PC0(80011448)`, `Execute !`, dan `CD_init`; layar tetap hitam. Periksa cache (`flushCache`) dan urutan init CD-ROM jika mengulangi jalur ini. Rutin init kartu memori (`buInit`) juga tampak menunggu status yang tidak berubah; bypass sementara belum membuktikan boot sukses.
- Log menunjukkan perintah kontroler `0x43` (Set Config Mode) berulang. Source PCSX-Redux memproses perintah DualShock tersebut hanya pada tipe pad Analog; tipe Digital mencatat `Unknown command for pad: 43`. Ini petunjuk yang belum diuji, bukan akar masalah yang terbukti. Referensi: https://github.com/grumpycoders/pcsx-redux/blob/db9bc8af44e3c77424127b573c17f9583ee2ab95/src/core/pad.cc. Eksperimen berikutnya: ubah Port 1 ke Analog/DualShock lalu ulangi boot.
- File baru dari pengguna `PCSX-Redux-9c6f98a0-linux-x86_64.zip` (90.912.361 byte) belum dapat dievaluasi atau dijalankan karena lingkungan shell/file tool tidak merespons. Periksa lagi sebelum memutuskan apakah build itu menggantikan AppImage release.
- Jangan meminta upload ulang ROM dan jangan mengunggah ROM/EXE, retail BIOS, save state, atau dump memori ke GitHub.


## Percobaan runtime setelah pemulihan ZIP Library — 2026-10-16

ZIP alternatif, ROM BIN, dan CUE berhasil dimaterialisasi lewat Files ke lokasi kerja. Namun `container.exec` bahkan gagal pada `echo runtime-check`, dan tool Python juga mengembalikan `ClientError`. ZIP belum bisa diinspeksi/diekstrak dan PCSX-Redux belum dijalankan dalam percobaan ini. Ini kendala lingkungan eksekusi, bukan bukti ZIP rusak atau gagal menjalankan game. Status boot tetap belum terverifikasi; setelah runtime pulih, uji integritas ZIP, versi/dependensi executable, lalu boot dengan OpenBIOS dan controller Port 1 Analog/DualShock. Kriteria sukses tetap title/menu Naruto terlihat serta input merespons.

## OpenBIOS source-level CD-read stall hypothesis — 2026-10-16

- Static inspection of the OpenBIOS source used by the research AppImage narrowed the normal boot stall to the EXE payload read path. loadExe() reads the 2,048-byte PS-X EXE header and then submits the full 382,976-byte payload (187 sectors) through one syscall_read call. The underlying CD file driver requires 0x800-aligned size/offset and waits for the CD read-completion event.
- The helper's wait for the completion event has no overall timeout. A missing/stuck completion event can block the BIOS indefinitely. This fits the prior stall evidence but is not a proven root cause.
- The uploaded filename PCSX-Redux-9c6f98a0-linux-x86_64.zip points to upstream commit 9c6f98a0ed0581635f9123147e382c248e0f5ddc (2026-09-28); the research AppImage is pinned to 0c3572c3db75f97542001e453ae80ba8c3f8acba (2026-10-01). The ZIP's contents/hash are not yet verified; treat this as filename-based provenance only.
- Next runtime test: use the existing AppImage/known OpenBIOS chunked build, CUE path, -run -interpreter -debugger -stdout -lua_stdout -logfile ..., and a fresh settings directory. Set Port 1 DeviceType=1 (Analog/DualShock) separately from PadType=2 (keyboard as host input) and Connected=true. Repeat the same boot attempt; compare pad 0x43 logs, CD read progress, entry-PC log, title/menu, and input response without changing other variables.
- Current session: the Library service successfully materialized the ROM, CUE, main EXE, DATA2 archive, and alternate emulator ZIP to reported working paths, but shell/Python calls returned ClientError. No new emulator run occurred. Never claim boot/gameplay success without runtime evidence.


## PCSX-Redux ZIP extraction record — 2026-10-16

- Extracted `PCSX-Redux-HEAD-x86_64.AppImage` from the Library ZIP (the ZIP passed `unzip -t` and had exactly one member).
- AppImage size: 91,474,424 bytes; SHA-256 `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`. The Library copy was materialized back and SHA-256 matched the extracted copy.
- Embedded version is `9c6f98a0`, build ID 335, changeset `9c6f98a0ed0581635f9123147e382c248e0f5ddc`, dated 2026-09-28 19:56:29 UTC.
- The source ZIP was replaced in Library by its one extracted AppImage because of the Library storage limit. Extraction manifest is saved at `/Naruto Research Files/PCSX-Redux-EXTRACTION-MANIFEST.md`.
- Runtime is blocked on this host: bundled emulator binary requires GLIBC_2.42/2.43, host has glibc 2.41; mounting the AppImage additionally reports missing FUSE/fusermount. Do not treat this as proof of a corrupted archive or ROM.
- The extracted AppImage is retained in Library; repository stores its provenance/hash/compatibility record in `docs/PCSX_REDUX_PACKAGE.md`. It was not inserted into Git history because the available GitHub connector does not expose binary release-asset upload. The repository's existing 65,747,557-byte AppImage release asset is a distinct build with its own hash.
- No ROM, game EXE, assets, BIOS retail, save state, or RAM dump was uploaded. This extraction did not demonstrate game boot or Story Mode.


## Preferred build for GLIBC 2.41 host — 2026-10-16

- Selected the existing research-release AppImage `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage` as the best candidate for glibc 2.41. Size 65,747,557 bytes; SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`.
- Public package description says AnyLinux packaging uses sharun, bundles dependencies, supports old/musl Linux distributions, and does not require FUSE. Upstream packaging action run 36872881656 succeeded on 2026-10-01; x86_64 log says `quick-sharun --simple-test`: “Test went OK.”
- This supersedes the 91 MB `9c6f98a0` Library build as the preferred candidate. That build's inner binary requires GLIBC_2.42/2.43 but the host is glibc 2.41.
- Critical limit: CI simple-test and GUI launch under Xvfb do not prove the Naruto ROM boots or runs smoothly. A fresh end-to-end game test could not run because container/Python execution tools returned ServerError in this turn. No claim of game boot or Story Mode success.
- Detailed provenance and next steps: `docs/PCSX_REDUX_PACKAGE.md`.


## Current Library package — AnyLinux artifact ZIP (2026-10-16)

- The current Library file is `/Naruto Research Files/PCSX-Redux-0c3572c3d-anylinux-x86_64-artifact.zip`, downloaded from Actions artifact ID `11170447493`; Actions-reported ZIP digest `f6c27070b565cbc0554f1093c1374a16aee2b8635c72ef7b141f9ff7bd857ed0`.
- Preferred binary inside: `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage`, 65,747,557 bytes; SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`.
- The previous 91 MB `9c6f98a0` AppImage and its stale extraction manifest were replaced/removed in Library. Their hashes and incompatibility history are preserved in `docs/PCSX_REDUX_PACKAGE.md`.
- The AnyLinux package's CI smoke test passed but does not load Naruto. Full game boot/controls/stability are unverified because this session's local container/Python tools return ServerError.


## Pembaruan eksperimen controller — 2026-10-17

- Hasil baseline A/B dari runner [Actions #38971848277](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38971848277): AnyLinux dan upstream HEAD sama-sama mencapai `EXEC:PC0` dan sama-sama mencatat `Unknown command for pad: 43`; keduanya masih belum membuktikan title/menu atau input yang berfungsi.
- Runner workflow diperbarui pada commit [0439c1b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/0439c1bbf51d3c1be234150d6bee80c5b812ff1e) agar menyetel Port 1 sebagai `Analog`, `Connected=true`, lalu memanggil `map()` melalui Lua sebelum tes boot. Setup ini mengikuti tes internal upstream PCSX-Redux di `tests/pcsxrunner/rumble.cc`.
- **Status eksperimen baru: hasil belum diverifikasi dalam catatan riset.** Jangan menyimpulkan peringatan `0x43` hilang atau boot berhasil berdasarkan commit workflow saja.
- Langkah wajib berikutnya: baca log run sesudah perubahan dan pastikan marker `PAD_SETUP=port1 analog device connected and remapped` muncul. Bandingkan pesan `0x43`; jika hilang, lanjutkan dengan tes GUI Xvfb dan konfirmasi frame title/menu serta respons input. Jika tetap hitam, pisahkan masalah kontroler dari jalur CD-ROM, boot executable, dan rendering.
- Dilarang menyimpan/unggah ROM, game EXE, BIOS retail, save state, dump RAM atau screenshot game ke repo.

- Koreksi penting: revisi workflow awal salah indentasi pada heredoc Lua; versi final yang berlaku adalah [0439c1b](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/0439c1bbf51d3c1be234150d6bee80c5b812ff1e), setelah indentasi YAML dibetulkan. Belum ada hasil runtime terverifikasi yang dicatat dari versi final ini.


## Hasil runtime Port 1 Analog — 2026-10-17

- Runner Actions [#38973267415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973267415) sukses. Marker Lua menyatakan Port 1 sudah `Analog`, terhubung, dan di-remap.
- Kedua build (AnyLinux dan upstream HEAD) mencapai `EXEC:PC0(80011448)` dan `Execute !`. Tidak ada pesan `Unknown command for pad: 43` di kedua log setelah konfigurasi Analog; baseline sebelumnya memunculkan pesan itu pada dua build. Masing-masing dihentikan pada batas waktu 90 detik, bukan crash.
- Kesimpulan terkonfirmasi: konfigurasi controller memperbaiki ketidakcocokan protokol `0x43` pada log. **Belum terbukti** bahwa title/menu tampil atau input dalam game berfungsi.
- Tes rendering GUI ditambahkan pada workflow commit [85c08d9](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85c08d9ea255dc400c0771361abc95817a0a7ba6). Actions [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) terlihat queued; hasil akhir belum diverifikasi. Probe ini menganalisis dua frame lokal (10s dan 20s) dan mencatat metrik/teks, tanpa menerbitkan gambar atau ROM/BIOS.


## GUI probe and CPU trace — 2026-10-17

- Actions [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) completed successfully. Under GUI + Xvfb, frame 10s and frame 20s both measured `1280x800`, `mean=0`, `stddev=0`, `colors=1`; OCR Japan/English returned no text. The captured desktop was entirely black at both points.
- Selected GUI logs did not show `EXEC:PC0` or `Execute !` within its 35-second window, unlike the headless probe. BIOS, disc ID and Analog PAD_SETUP markers did appear. This is a separate GUI/headless discrepancy, not proof that the game executable is invalid.
- New separate CPU trace workflow: [naruto-cpu-trace.yml](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/blob/main/.github/workflows/naruto-cpu-trace.yml), run [#38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045). It samples `PC`, `RA`, `SP` on every 30th `GPU::Vsync` callback, capped at 600 frames. Result not yet verified at time of writing.


## CPU trace attempt 1 — status 2026-10-17

- [Actions #38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045) exited with code 139 about 12 seconds after the VSync trace callback was added; no `PC_TRACE` sample appeared. Treat this as an instrumentation failure until isolated, not evidence against the ROM.
- Retry workflow revision: [9419800](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/941980021c16dee3e779f6cc1066dad70b187ad4). It uses one combined `-exec` script and no longer removes the listener from its callback. Check [run #38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739); if it also crashes, reduce the callback to count VSyncs only.


### CPU trace attempt 2 correction — 2026-10-17

- Run [#38974418739](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974418739) ended with exit 134 because Lua parsing failed: `unexpected symbol near '\\'`. The helper used a doubly escaped newline, passing literal `\n` instead of a newline between chunks. No valid tracing code ran; do not interpret as a ROM crash.
- Workflow commit [7b8ce73](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/7b8ce731378e0115f616b7ff78874f5d17375e80) replaced concatenation with one Lua heredoc. Check retry [Actions #38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869) for setup and VSync samples.


### CPU trace attempt 3 and counter-only isolation — 2026-10-17

- Corrected trace run [#38974563869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974563869) emitted PC samples from frame 30 through at least 780. Values often point to BIOS routines (`BFC0574C`, `BFC05784`, `BFC03C6C`), with occasional `0xB0` and `0x2998`; the separate log includes `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, `Execute !`. The emulator process still exited 139 (segfault) with an incomplete final sample, so register reads inside the callback could be involved. The trace does not prove the game crashed or remained on one PC.
- Isolation run [#38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602), workflow commit [85d3e4f](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85d3e4ff31732b7788d67e447ea9df136dcb84f5), removes CPU-register reads and prints only a VSync counter. Results pending.


### Counter-only VSync test passed — 2026-10-17

- Run [#38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) reached expected `TRACE_PROCESS_EXIT=124` after the 35-second cap; VSync counter advanced through `frame=2040`. Headless boot markers `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, `Execute !` appeared. Counter-only callback is stable.
- New probe [#38974903834](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974903834), commit [ff0faa5](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/ff0faa598c6e19295229b450c6f9d42c83e590fb), keeps counter and adds sparse PC-only reads from a register view acquired before callback registration. Result pending.


### Emulator trace API mismatch — 2026-10-17

- Run [#38975154606](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975154606) aborted with `attempt to index field 'CPU' (a nil value)` because the pinned AnyLinux build from upstream ref `0c3572c3d` has no `PCSX.CPU.Trace` API. This test did not begin VSync counting; it says nothing negative about the ROM.
- Corrected workflow commit [c994afc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/c994afccfa62efcc01751a7c2b39d89b109d936a) now verifies and uses private-release upstream HEAD AppImage SHA-256 `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`. Run [#38975223698](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975223698) is the new bounded CPU-trace attempt; outcome pending.


### CPU trace API correction and source build — 2026-10-17

- The private upstream HEAD AppImage in [run #38975223698](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975223698) also lacks `PCSX.CPU.Trace`; it aborted before VSync counting. Neither packaged AppImage asset currently available exposes this newer API.
- Current runner workflow commit [8304b7d](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8304b7dd56be13673e83e84bb738458eca0cfc2d) now clones source pinned to upstream commit `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` and compiles it with the official PCSX-Redux builder container. [Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) is building; results pending.


### Catatan interpretasi GUI — 2026-10-17

- Frame hitam pada 10s/20s di [run #38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926) diambil sebelum executable game terbukti dijalankan. Counter-only [run #38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602) menunjukkan entry point baru dicapai setelah sekitar 27–30 detik dalam tes headless. Karena itu capture 10s/20s bukan bukti bahwa layar tetap hitam sesudah entry. Tes GUI harus diperpanjang hingga setidaknya 60–90 detik dan idealnya menangkap window emulator secara langsung.
- Source-build trace [run #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) sedang mencoba build source pinned agar API CPU trace tersedia tanpa membaca register dari callback. Hasil belum terverifikasi.


### Tes lanjutan sedang berjalan — 2026-10-17

- GUI run terbaru [#38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679), workflow commit [aea4c20](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aea4c20accfd6d1c5089a226f52a2c4183d2d9a8), memperpanjang pengamatan hingga 100 detik dan mengambil frame pada 30/60/90 detik. Saat catatan ini diperbarui, langkah A/B + GUI masih berjalan.
- CPU trace source-build run [#38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) belum melewati langkah build pinned upstream source. Hasil build dan trace tetap pending.


## Verifikasi cloud runner dan koreksi observasi — 2026-10-17

Pemeriksaan ulang repositori mengonfirmasi riset ini tetap **private**, sedangkan `naruto-shinobi-jintori-runner` tetap public. Release `research-emulator-pcsx-redux-2026-10-15` berisi aset ROM/CUE/OpenBIOS yang diperlukan; nama aset ROM dan CUE dinormalisasi dengan titik oleh proses unggah Release. Tidak ada media permainan yang ditambahkan ke Git runner.

Run [runner Actions #38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679) selesai dengan kesimpulan job **success**. Log mengonfirmasi secret read-only hadir tanpa menampilkan nilainya, ukuran ROM 325.989.552 byte, SHA-256 cocok, CUE valid, BIOS OpenBIOS dikenali, disc label `SLPS-03553`, `SYSTEM.CNF` menunjuk `SLPS_035.53`, seluruh 187 chunk executable dibaca, lalu tercatat `EXEC:PC0(80011448)` dan `Execute !`. Konfigurasi Port 1 Analog juga menghilangkan pesan `Unknown command for pad: 43` pada dua build pembanding. Ini membuktikan transfer kendali ke entry executable dalam jalur headless, **bukan** bukti title/menu atau input gameplay.

Capture GUI 30/60/90 detik pada run tersebut melaporkan gambar hitam (mean 0, stddev 0, satu warna) dan OCR kosong. Audit workflow memperlihatkan capture dilakukan dengan `import -window root`, yaitu latar root Xvfb, bukan window emulator secara eksplisit. Karena itu angka tersebut tidak boleh dipakai untuk menyimpulkan bahwa framebuffer game hitam.

CPU trace source-build [Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) membangun emulator tetapi peluncuran di host berhenti dengan `libcapstone.so.5: cannot open shared object file`; belum ada VSync atau instruksi yang direkam. Ini kegagalan dependensi runtime runner, bukan bukti masalah ROM/game.

Koreksi yang sudah dikirim ke repo runner:
- Commit [d965dcc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/d965dcc864c73818e67d6a1e5f9edc19d4a3a17c) menambahkan `libcapstone-dev` dan pemeriksaan `ldd` sebelum trace, supaya dependensi yang hilang terdeteksi sebelum emulasi.
- Commit [8829933](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/8829933b3b6815dce694ebe6d46cd2a1f0fee9f0) memasang `xdotool`/`x11-utils` dan menargetkan window PCSX-Redux untuk pengukuran/OCR. Jika window tidak ditemukan, workflow mencatat pohon window dan tidak menggantinya dengan capture root hitam. File gambar tetap lokal di runner dan dihapus saat cleanup.

Retest yang dimulai dari dua commit itu belum selesai pada waktu catatan dibuat: GUI [Actions #39000276365](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365), CPU trace [Actions #39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139). Periksa hasil finalnya sebelum menetapkan status boot. Jangan mulai RT-001/gameplay sampai title/menu yang dikenali dan respons input terbukti.


## GUI-window retest result — 2026-10-17 (Actions #39000276365)

The corrected capture test completed successfully. Its log found the actual PCSX-Redux X11 window (CAPTURE_WINDOW at 30s, 60s and 90s), rather than the Xvfb root. All three captured PCSX-Redux-window frames nevertheless measured 1280x800, mean=0, stddev=0, colors=1; Japanese/English OCR returned no text.

Important distinction: the GUI probe's own log shows BIOS/OpenBIOS and disc metadata, but does not show [CHUNK1] done chunks=187, EXEC:PC0(80011448) or Execute !. Those entry markers are present in the separate headless A/B probes in the same job. Therefore the current evidence does not show a black game frame after executable entry; it shows that GUI mode remains black and did not log the same executable handoff as headless mode. Investigate this GUI/headless boot-path difference before diagnosing the game's renderer.

Run: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365. ROM/BIOS, frames and logs were removed during runner cleanup; no game media or screenshot was committed.


## GUI-init/GL diagnostic rerun queued — 2026-10-17

After the corrected capture proved the PCSX-Redux window itself remained uniformly black and the GUI probe lacked both PAD_SETUP and executable-entry markers, the runner workflow was tightened further. Commit [259d587](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/259d587c6b677be7f6466b0ec61edb1940faec49) adds a Mesa/GLX capability report from the same Xvfb + software-rendering environment, prints the final GUI stdout and emulator logfile tails, and explicitly reports whether the Lua PAD_SETUP marker ran. Cloud rerun [Actions #39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307) was in progress at the latest check.

This experiment distinguishes failure in PCSX-Redux GUI/OpenGL initialization or startup from a guest-game display problem. Do not label the title screen black after game entry unless the GUI run itself logs `[CHUNK1] done chunks=187` and `EXEC:PC0(80011448)` before the measured frames. Source-built CPU-trace dependency retest [Actions #39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) remains in progress; the run must complete its compile/preflight before trace conclusions can be made.


## Perbandingan cloud AnyLinux vs upstream-labelled HEAD — 2026-10-17

Run headless A/B terbaru [#39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307) memakai ROM/CUE dan OpenBIOS yang sama, mode interpreter/software GPU, setup Port 1 Analog yang sama, serta batas observasi 90 detik. Kedua AppImage mengenali disc SLPS-03553, membaca SYSTEM.CNF, menyelesaikan 187 chunk (382.976 byte payload EXE), lalu mencatat EXEC:PC0(80011448) dan Execute !. Keduanya tidak lagi mencatat Unknown command for pad: 43. Kedua proses mencapai batas waktu observasi; ini bukan crash yang terbukti dan bukan bukti game dimainkan.

Build di release:
- AnyLinux PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage, 65.747.557 byte, SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c, source commit 0c3572c3db75f97542001e453ae80ba8c3f8acba.
- AppImage bernama PCSX-Redux-HEAD-x86_64.AppImage, 91.474.424 byte, SHA-256 5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8. Package inventory mencatat source commit 9c6f98a0ed0581635f9123147e382c248e0f5ddc (2026-09-28), bukan source-build CPU-trace terbaru.

Diagnostik GUI [#39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307) mengonfirmasi GLX tersedia: Mesa llvmpipe, OpenGL 3.3. Jendela AnyLinux yang benar berhasil ditangkap pada 30/60/90 detik, tetapi seluruh frame 1280×800 seragam hitam (mean 0, stddev 0, 1 warna) dan OCR kosong. Log GUI mencapai penanda setup Lua dan hanya menampilkan progres chunk awal (indeks 0, 8, 16, 24, 32); tidak ada marker 187 chunk selesai, EXEC:PC0 atau Execute ! pada log GUI. Jadi masalah bukan ketiadaan GLX yang terbukti; jalur GUI masih berhenti sebelum executable handoff.

Workflow runner diperbaiki untuk menangkap jendela GUI kedua AppImage dalam kondisi setara dan membersihkan file frame/log sementara. Rerun [#39002136781](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002136781) baru queued ketika catatan ini ditulis. Source-build CPU trace kini menjalankan binary di dalam image Docker builder yang sama setelah run [#39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) gagal pada preflight host karena FFmpeg/SDL dari builder tidak tersedia di host. Rerun [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) masih berjalan saat pencatatan.

**Rekomendasi bersyarat:** gunakan AnyLinux sebagai kandidat utama operasional di runner standar (lebih kecil dan dipaketkan untuk kompatibilitas Linux), serta pertahankan AppImage berlabel HEAD sebagai pembanding cadangan, bukan sebagai “upstream HEAD terkini”. Untuk analisis instruksi gunakan source-build terpisah dengan API PCSX.CPU.Trace; jangan menganggap API itu tersedia pada kedua AppImage. Belum ada pemenang untuk gameplay/rendering: hasil GUI kedua build masih perlu diperiksa. Title/menu Naruto dan input dalam game belum terbukti; Story Mode belum dimulai.


## Verifikasi identitas build upstream — 2026-10-17

Pengecekan API upstream menunjukkan main/head PCSX-Redux saat diperiksa adalah commit [41f3196257d0962942b60983201aade951ebbd54](https://github.com/grumpycoders/pcsx-redux/commit/41f3196257d0962942b60983201aade951ebbd54), bertanggal 2026-10-17 02:53:17 UTC. Maka asset release dengan nama PCSX-Redux-HEAD-x86_64.AppImage (source 9c6f98a0, 2026-09-28) bukan current upstream HEAD; build AnyLinux menggunakan source 0c3572c3 (2026-10-01), dan source-build trace dipatok ke 6b9df482 (2026-10-16). Perbedaan ini membedakan identitas build, bukan membuktikan penyebab screen hitam.


## Verifikasi GUI A/B terbaru dan perbaikan harness — 2026-10-17

Run GUI A/B [#39002136781](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002136781) berstatus workflow `success`, tetapi **bukan hasil uji GUI yang berhasil**. Langkah headless di job yang sama tetap membuktikan kedua AppImage membaca disc `SLPS-03553`, menuntaskan 187 chunk executable, dan mencatat `EXEC:PC0(80011448)` serta `Execute !`; keduanya tidak lagi mencatat `Unknown command for pad: 43`. Saat masuk bagian GUI, `gui_probe.sh` berhenti untuk kedua build pada `PAD_SETUP: unbound variable` karena variabel shell tidak diekspor. Tidak ada jendela emulator yang ditemukan dan tidak ada frame yang ditangkap. Karena hasil probe tidak dipaksa menjadi kegagalan job, status `success` hanya berarti step berakhir tanpa kegagalan workflow yang terdeteksi; status itu bukan bukti GUI/game berhasil.

Perbaikan minimal sudah didorong ke runner pada commit [aac684d120ec025c4a87197da8d835f90b89f869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aac684d120ec025c4a87197da8d835f90b89f869): ekspor `PAD_SETUP` sebelum skrip probe GUI dipanggil. Rerun ROM privat [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) sudah dipicu dan masih `in_progress` pada pemeriksaan terakhir; hasil frame, OCR, boot-marker GUI, dan cleanup masih harus diperiksa dari log akhirnya.

CPU-trace run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) juga masih `in_progress`. Secret dan pengunduhan/verifikasi file privat telah dilewati; step source-build di container Docker yang dipatok digest masih berjalan, sedangkan capture trace dan cleanup belum dimulai. Belum ada `CPU_TRACE_SIZE` atau `CPU_TRACE_LINE` yang dapat dipakai untuk analisis.

Current upstream PCSX-Redux yang terverifikasi saat cek adalah [41f3196257d0962942b60983201aade951ebbd54](https://github.com/grumpycoders/pcsx-redux/commit/41f3196257d0962942b60983201aade951ebbd54) (2026-10-17 02:53:17 UTC). AppImage berlabel “HEAD” tetap build source 9c6f98a0, bukan upstream HEAD terkini. Tidak ada bukti bahwa judul/menu tampil atau input gameplay merespons; gate RT-001 tetap tertutup dan Story Mode tidak boleh dimulai.


## Hasil final GUI A/B setelah perbaikan PAD_SETUP — 2026-10-17

Run [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) selesai dengan workflow/job `success` pada runner commit [aac684d120ec025c4a87197da8d835f90b89f869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aac684d120ec025c4a87197da8d835f90b89f869). Hasil `success` bukan berarti kedua GUI berhasil menampilkan game. Job ROM selesai dan job smoke dilewati; tidak ada artefak Actions yang dipublikasikan.

- **Headless A/B (baseline terpisah):** kedua AppImage tetap mengenali BIOS OpenBIOS, disc `SLPS-03553`, `SYSTEM.CNF` dan target `SLPS_035.53`; masing-masing mencatat `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, serta `Execute !`. Keduanya mencapai batas observasi headless 90 detik (exit 124), bukan crash yang terbukti.
- **AnyLinux GUI:** `PAD_SETUP=port1 analog device connected and remapped` muncul; BIOS dan metadata disc serta `SYSTEM.CNF`/`BOOT` juga tercatat. Jendela yang ditemukan (X11 ID `2097204`) ditangkap langsung pada 30/60/90 detik, bukan root window Xvfb. Ketiga frame 1280×800 memiliki mean=0, stddev=0 dan 1 warna; OCR Jepang/Inggris kosong. Log GUI tidak memiliki marker chunk 187, `EXEC:PC0`, atau `Execute !`. Proses mencapai batas observasi 100 detik (exit 124). Artinya harness sudah berjalan dan menangkap window, tetapi jalur GUI belum membuktikan handoff executable.
- **AppImage berlabel “HEAD” GUI:** jendela emulator tidak ditemukan dan tidak ada frame pada 30/60/90 detik. Log final: `Unable to create main window: Couldn't find matching GLX visual` serta `SDL failed to create OpenGL 3.2 core context, retrying with any 3.0 profile`. Marker Lua `PAD_SETUP` dan executable-entry tidak muncul. Proses kembali dengan exit 137 sesudah batas observasi/eskalasi timeout; karena kegagalan pembuatan window sudah tercatat, jangan menyebutnya crash guest atau masalah ROM yang terbukti.
- Marker `Unknown command for pad: 43` tidak muncul pada kedua jalur headless maupun log GUI yang diperiksa. Ini tidak membuktikan input gameplay merespons.
- Langkah cleanup sukses dan mencatat bahwa ROM/BIOS/CUE, log, profil, frame, serta dua pohon AppImage sementara dihapus. Inventaris repo runner tetap hanya workflow, dokumentasi, README dan .gitignore; tidak ditemukan file media game atau artefak run.

## Status CPU trace source-build saat pemeriksaan terakhir — 2026-10-17

Run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849), commit workflow [16a6faff066b913480ad121b497db79df03a9de2](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/16a6faff066b913480ad121b497db79df03a9de2), masih `in_progress`. Unduh/verifikasi ROM/CUE/BIOS selesai pada 04:17:26 UTC; step build source pinned masih berjalan saat pengecekan berikutnya (sekitar paruh dari batas job 45 menit). Step capture trace dan cleanup belum mulai. Endpoint unduhan log job mengembalikan `BlobNotFound` sementara run aktif, sehingga belum ada bukti log build yang dapat dianalisis; artefak run belum ada. Belum ada hasil `PCSX_BUILD_RESULT`, `CPU_TRACE_SIZE`, `CPU_TRACE_LINE`, `TRACE_RESULT`, `CPU_TRACE_RESULT`, atau `TRACE_PROCESS_EXIT` yang terverifikasi. Jangan menjalankan duplikat atau menyatakan build gagal sebelum run selesai/batas waktu tercapai; periksa step aktif lagi sebelum deadline 45 menit.

**RT-001 tetap terbuka/terblokir.** Belum ada title/menu Naruto yang dikenali maupun respons input terkontrol. Jangan mulai Story Mode.

## Hasil final CPU trace source-build dan verifikasi GUI — 2026-10-17

Run [CPU trace #39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) telah selesai dengan kesimpulan `success`. Job 117306664750 berjalan 04:17:11–04:44:27 UTC. Download/verifikasi aset selesai 04:17:26; build source pinned selesai 04:43:46; capture trace 04:43:46–04:44:21; cleanup 04:44:21–04:44:25. Semua langkah berhasil. Source commit `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`, image builder `ghcr.io/grumpycoders/pcsx-redux-build@sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`. `PCSX_BUILD_RESULT` menyatakan build sukses; pemeriksaan `ldd` dalam image yang sama tidak menemukan dependency `not found`.

Capture membuktikan `VSYNC_TRACE` berlanjut melewati 1620, 1650, dan 1680; `CPU_TRACE_WINDOW=enabled frame=1620`; `CPU_TRACE_SIZE=16031631`; `TRACE_RESULT=VSync counter callbacks fired.`; `CPU_TRACE_RESULT=Built-in instruction records were printed.`; dan `TRACE_PROCESS_EXIT=124` pada batas observasi 35 detik yang memang dirancang. Run tidak menerbitkan artefak. Cleanup menyatakan ROM/CUE/BIOS, emulator, serta log trace sementara dihapus dari runner.

80 instruksi terakhir menunjukkan loop guest di PC mentah `0x000015a4–0x000015c4`: load dari `0x5de4(a3)` menghasilkan 0, cabang membandingkan dengan 2/1, dan `$v1` dihitung turun sambil kembali ke `0x000015a4`. Penghitung berkurang; ini eksekusi berulang yang bergerak, bukan bukti hang permanen. Run source-build ini tidak merekam `SYSTEM.CNF`, `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, atau `Execute !`. Jangan tetapkan pemilik loop sebagai BIOS, loader, atau overlay sebelum mapping divalidasi. Trace menyimpan `m_regs.pc` mentah menurut source pinned PCSX-Redux; alamat loop berbeda dari entry EXE `0x80011448`.

GUI A/B [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) juga selesai. AnyLinux GUI menjalankan `PAD_SETUP` dan menangkap window sebenarnya pada 30/60/90s, tetapi frame tetap hitam seragam dan tidak ada handoff EXE dalam log GUI. AppImage berlabel “HEAD” gagal membuat window akibat GLX/OpenGL. Kedua build di mode headless lama mencapai entry; bukti itu tidak bisa dipindahkan ke GUI atau source-build trace. RT-001 tetap **Open / blocked** sampai title/menu dikenali dan input terkontrol terbukti responsif.

## Perbandingan versi source terhadap baseline headless — 2026-10-17

Perbandingan GitHub langsung antara source AnyLinux `0c3572c3db75f97542001e453ae80ba8c3f8acba` dan source CPU-trace `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` menghasilkan selisih 803 commit. File yang berubah besar termasuk `src/core/cdrom.cc` (+1.476/-1.392 baris), `src/core/psxinterpreter.cc` (+290/-81), `src/core/pad.cc` (+362/-22), `src/core/psxmem.cc`, dan pointer submodule `src/mips`. Pada interpreter, macro target branch berubah dari memakai `_PC_` langsung menjadi `branchBase()` beserta pelacakan delay slot/exception; CD-ROM juga direstrukturisasi. Ini kandidat area pembandingan, bukan bukti akar masalah.

Kedua perintah headless memakai `-no-ui -exec ... -run -interpreter -softgpu -stdout -lua_stdout -logfile`; jadi jangan menyalahkan dynarec sebagai beda utama. Namun durasi observasi berbeda: AppImage headless diberi 90 detik dan mencapai EXEC:PC0; source-trace build hanya 35 detik dan merekam frames 1620–1680 sebelum timeout. Karena itu belum sah menyebutnya regresi source atau hang tanpa pengujian pada batas waktu yang sebanding. Langkah paling bernilai adalah trace source pinned pada window lebih akhir (mis. frames 4500–4560) dengan logging PC guest pada VSync berkala, serta marker boot dicetak terpisah dari ekor trace agar tidak terpotong oleh `tail`.


## Follow-up CPU trace dengan agregasi aman — 2026-10-17 (run masih aktif)

- Workflow runner diperkeras pada commit publik `d1c5b731befe5afacdfbdf3b9914b9f5e9f9ac64` (blob workflow `b06bb37d23c0fc7ff386ce0846e08f719b46d3bf`): observasi 90 detik, PC guest tiap 30 VSync, trace window frame 1620–1680 dan 4500–4560, ringkasan PC agregat saja, boot markers dipisah, cleanup `if: always()` dipertahankan. Source `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` dan image builder digest tetap sama.
- Run [#39004736399](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39004736399) menggunakan commit workflow tersebut. Pemeriksaan terakhir: secret check, workspace, dan download/verifikasi file lulus; build source masih `in_progress`; capture dan cleanup belum berjalan. Jangan menganggap pengujian runtime berhasil/gagal sebelum status dan log final diperiksa.
- Audit log publik menemukan 80 record instruksi/operand aktual pada run #39001985849; tidak ada artifact Actions. Run CPU-trace lama lain yang diperiksa tidak memuat record instruksi aktual. Workflow baru tak lagi mencetak record mentah. Log run #39001985849 masih dapat diakses; antarmuka GitHub yang tersedia di sesi ini tidak menyediakan tindakan penghapusan run/log.
- RT-001 tetap **Open / blocked**; title/menu Naruto dan respons input terkontrol belum terbukti.

## Hasil final CPU trace 90 detik — Actions #39004736399 (2026-10-17)

Run [#39004736399](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39004736399) selesai dengan status workflow/job `success`. Waktu run 05:01:31–05:29:40 UTC (12:01:31–12:29:40 WIB). Semua step selesai sukses: secret check, persiapan workspace, download/verifikasi aset, build source PCSX-Redux, capture/diagnostik, dan cleanup.

- ROM lulus pemeriksaan ukuran 325.989.552 byte dan SHA-256 `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`. CUE dinormalisasi hanya untuk referensi berkas sementara. Source pin `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`; builder image tetap `ghcr.io/grumpycoders/pcsx-redux-build@sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`.
- Build berlangsung sekitar 26 menit 20 detik, berakhir dengan `PCSX_BUILD_RESULT`. Pemeriksaan dependency `ldd` di image builder yang sama lulus tanpa library bertanda `not found`.
- Capture mencapai sampel VSync dari frame 30 sampai 4740, tiap 30 frame: 158 sampel. PC adalah `0x000015a4` pada 157 sampel; satu pengecualian sampel berada di frame 420 pada `0x00000870`, lalu PC kembali ke `0x000015a4`.
- Ringkasan CPU trace pada frames 1620–1680: 200 record diperiksa, 9 PC unik, total terlapor 16.031.631 record. Pada frames 4500–4560: 200 record, 9 PC unik, total terlapor 16.031.484 record. Kedua jendela memiliki pola hot PC yang sama; alamat teratas `0x000015c0` dan `0x000015c4` masing-masing muncul 23 kali, `0x000015a4` dan beberapa alamat tetangganya sekitar 22 kali.
- Boot marker yang terlihat: OpenBIOS dikenali, disc label `SLPS-03553`, disc ID `SLPS03553`, executable `SLPS_035.53;1`. Tidak terlihat `SYSTEM.CNF`/baris `BOOT =`, `[CHUNK1] done chunks=187`, `EXEC:PC0(80011448)`, atau `Execute !`.
- `TRACE_PROCESS_EXIT=124` adalah batas observasi 90 detik yang disengaja, bukan bukti crash guest. Tidak ada marker FATAL/Exception/ERROR pada bagian runtime yang disaring. Keluaran runtime baru hanya agregat PC dan tidak memuat record instruksi/operand mentah.
- Cleanup menyatakan ROM/CUE/BIOS, emulator hasil build, dan log runtime sementara telah dihapus dari runner ephemeral. Daftar artefak Actions kosong.

**Interpretasi:** pengujian memperkuat bukti adanya loop PC berulang dalam sesi OpenBIOS/disc, tetapi tidak mengidentifikasi pemilik loop dan tidak membuktikan handoff ke executable utama. Jangan menyebutnya kode game, hang permanen, atau akar masalah spesifik sebelum mapping alamat dan jalur pemanggil diverifikasi.

**RT-001 tetap Open / blocked.** Belum ada title/menu Naruto yang dikenali dan belum ada respons input terkontrol yang terbukti. Jangan mulai Story Mode. Log publik lama [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) masih perlu ditinjau karena memuat 80 record instruksi/operand; run baru ini tidak mengulangi keluaran mentah tersebut.
