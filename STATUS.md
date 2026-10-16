# Status penelitian

Terakhir dirangkum: 2026-10-15

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
