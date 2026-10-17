# Status terbaru 2026-10-17 — sesudah tes kontroler Analog

- Run [#38973267415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973267415) sukses. Port 1 disetel ke Analog, tersambung, dan di-remap sebelum boot.
- AnyLinux dan upstream HEAD sama-sama mengenali disc `SLPS-03553`, menyelesaikan pemuatan 187 sektor executable, mencapai `EXEC:PC0(80011448)` lalu `Execute !`. Peringatan `Unknown command for pad: 43` hilang pada kedua log; sebelumnya muncul pada keduanya di run baseline #38971848277.
- Ini mengonfirmasi koreksi protokol controller, tetapi **belum membuktikan** title/menu dan input in-game. Kedua tes headless tetap mencapai batas 90 detik.
- GUI probe baru ada pada workflow commit [85c08d9](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/85c08d9ea255dc400c0771361abc95817a0a7ba6), run [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926). Pada saat catatan ini ditambahkan, run masih terlihat in progress; ambil log akhirnya untuk memeriksa dua frame pada detik 10 dan 20, metrik piksel, OCR Jepang/Inggris, dan penanda boot. Frame dan log GUI sementara dihapus oleh cleanup.

---

# Rencana uji runtime PS1

## Tujuan dan status

Emulator/debugger adalah jalur riset utama bersama analisis statis, bukan sekadar opsi terakhir. Gunakan runtime untuk memverifikasi nilai sebelum/sesudah aksi dan menguji cabang kode yang benar-benar berjalan. **Belum ada pengujian gameplay runtime terkontrol yang diselesaikan.** Lihat [EMULATOR_WORKFLOW.md](EMULATOR_WORKFLOW.md) untuk pilihan emulator dan prosedur yang lebih rinci.

Pada 2026-10-15, PCSX-Redux AppImage sudah dipaketkan ke release repo Naruto dan SHA-256-nya diverifikasi via GitHub Actions. GUI berhasil dijalankan pada layar virtual. OpenBIOS default sudah dibangun dan disimpan sebagai Release asset, tetapi uji dengan BIOS tersebut belum menghasilkan bukti visual bahwa game masuk ke menu/title. Workflow #38693918169 berhasil membangun varian shell/menu dan `BOOT_MODE=fast`. Uji lokal dengan `-bios openbios.bin -interpreter -debugger -iso game.cue -run` pada varian fastboot menghasilkan layar hitam setelah sekitar 12 detik; belum terkonfirmasi bahwa game mencapai title/menu. Gunakan asset release beserta checksum, lalu cari sebab boot tidak terlihat sebelum mengklaim runtime berhasil. Jangan meminta upload ulang ROM ~326 MB dari laptop.

## Persiapan

1. Prioritaskan PCSX-Redux untuk breakpoint CPU, memory editor, dan GDB server; lihat [EMULATOR_WORKFLOW.md](EMULATOR_WORKFLOW.md). Mednafen adalah alternatif untuk cek silang.
2. Gunakan image BIN/CUE dengan hash dari `docs/ROM_STRUCTURE.md`; jangan patch ROM asli. CUE harus merujuk file BIN yang sama dan track Mode 2/2352.
3. Catat versi/build emulator, jenis BIOS, setting CPU/interpreter/debugger, hash ROM, mode permainan, skenario, pemain aktif, aksi, nilai awal/akhir, PC breakpoint dan alamat RAM yang berubah.
4. Jalankan baseline dari state awal terkontrol. Untuk pengulangan, simpan state/memory card eksperimen di luar repo dan jangan menimpa save asli.
5. Jangan menganggap alamat overlay statis sebagai RAM live sebelum loader/base overlay dikonfirmasi. Mulai dari breakpoint executable utama dan verifikasi perubahan RAM.

## Variabel yang dipantau

- Empat struktur pemain yang diduga berstride 0xB4 dan field Chakra pada offset +0x18: verifikasi ulang di RAM setelah loader/overlay aktif.
- ID pemain aktif dan penghitung giliran.
- Field petak: owner bits, level/jenis, durability, nilai/harga, dan atribut yang belum dipetakan.
- Konfigurasi target/opsi skenario.
- ID kartu yang dipilih, ID jutsu, hasil roulette, keadaan battle, dan ID pemenang.

Alamat RAM yang diketahui dari static analysis harus diperlakukan sebagai breakpoint awal saja sampai overlay dan alokasi RAM diverifikasi.

## Matriks eksperimen

### A. Inisialisasi Story Stage 1

- Mulai stage pertama dari keadaan bersih.
- Catat Chakra setiap pemain sebelum dan sesudah inisialisasi.
- Temukan record konfigurasi yang dibaca saat stage dimulai.
- Konfirmasi hubungan field +0x04, +0x08, +0x0C dengan nilai awal, target, dan parameter lain.
- Pastikan siapa yang menang jika Chakra sama dengan target dan jika satu angka di bawah target; gunakan keadaan yang aman/reproducible.

### B. Membangun barrier

- Pilih petak kosong dengan saldo Chakra yang cukup.
- Catat saldo sebelum konfirmasi, saat transaksi, dan sesudah barrier muncul.
- Ulangi dengan tipe petak/skenario berbeda bila tersedia.
- Breakpoint pada setter Chakra serta rutin perubahan field petak.
- Temukan asal nilai biaya di register/memori, bukan hanya konstanta yang kebetulan terlihat di disassembly.
- Uji saldo tepat di bawah, sama dengan, dan di atas biaya yang terlihat di UI jika memungkinkan.

### C. Meningkatkan level barrier

- Mulai dari barrier level 1 yang nilai/durability awalnya dicatat.
- Catat saldo, level, nilai, dan durability sebelum/sesudah upgrade.
- Ulangi untuk level dan tipe barrier berbeda.
- Pisahkan biaya upgrade dari biaya bangun dan dari animasi/transisi UI.

### D. Pendapatan dan kunjungan ke petak

- Jalankan satu giliran yang melewati petak sendiri dan petak lawan dengan save state yang sama.
- Catat saldo masing-masing pemain sebelum/sesudah pendaratan dan akhir giliran.
- Uji apakah pendapatan datang pada pemilik, pengunjung, atau keduanya; apakah efek bergantung level/tipe/bonus.
- Ulangi tanpa lawan mendarat untuk mendapat baseline.

### E. Battle, damage, dan pengambilalihan barrier

- Siapkan pertarungan pada barrier musuh dengan kondisi karakter/jutsu yang dapat diulang.
- Catat saldo dan field barrier sebelum battle, di setiap titik damage, setelah menang/kalah.
- Uji jutsu berbeda dan karakter berbeda.
- Bandingkan kemenangan di wilayah tanpa barrier bila bisa dibuat.
- Pisahkan biaya untuk mulai menyerang, biaya jutsu, damage durability, transfer kepemilikan, dan hadiah setelah menang.

### F. Kartu

Untuk setiap kartu:
- Catat ID kartu dan ID handler yang dipanggil.
- Catat semua state sebelum/sesudah: Chakra, statistik, skip-turn/status, hasil roulette berikutnya, kepemilikan Scroll of Seals, serta penghitung.
- Untuk kartu yang memodifikasi beberapa roulette, uji kedua lemparan dan kapan efek habis.
- Uji batas maksimum/minimum dan cara pembulatan.
- Bandingkan hasil dengan transkripsi di docs/GAME_RULES.md dan dokumentasi komunitas.

### G. Kondisi kemenangan alternatif

- Temukan record/bit opsi yang dipilih lewat menu Party Mode.
- Untuk setiap opsi, lakukan satu test case positif (syarat terpenuhi) dan satu negatif (satu syarat tidak terpenuhi).
- Periksa kapan game menetapkan ID pemenang, kapan mengubah screen/state, dan arti field pemenang 0xFF.
- Uji target Chakra tanpa opsi tambahan dan target dengan opsi tambahan untuk melihat prioritas kondisi ketika beberapa syarat terpenuhi bersamaan.

## Format tabel hasil

| Test ID | Kondisi awal | Aksi | Nilai/state sebelum | Nilai/state sesudah | PC/overlay | Hasil | Status |
|---|---|---|---|---|---|---|---|
| RT-001 | Belum dijalankan | — | — | — | — | — | Open |

Setiap test harus dilengkapi screenshot atau log debugger dan, jika relevan, hash/save-state untuk reproduksi. Jangan menyebut formula “terbukti runtime” tanpa hasil yang bisa diulang.

## Kriteria selesai

- Loader/overlay aktif teridentifikasi untuk setiap breakpoint.
- Nilai biaya/pendapatan berasal dari field atau rumus yang terpetakan sampai pemanggilnya.
- Formula yang memiliki cabang berbeda dites pada sekurangnya satu contoh per cabang penting.
- Semua flag opsi kemenangan dapat dikaitkan dengan pilihan menu/data record dan hasil permainan.
- Hasil runtime sesuai analisis statis; bila berbeda, catat perbedaan dan revisi hipotesis.
- Laporan final membedakan aturan normal, variasi skenario, dan kondisi yang hanya tersedia setelah unlock.

## Status boot sebelum uji gameplay — pembaruan 2026-10-17

Jangan mulai test case gameplay RT-001 sampai title/menu yang dikenali benar-benar tampil dan input terbukti direspons.

### Fakta runtime yang sudah dikonfirmasi

- ROM private yang diuji terverifikasi dengan ukuran 325.989.552 byte dan SHA-256 `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`.
- OpenBIOS membaca disc `SLPS-03553`, membaca `SYSTEM.CNF` (`BOOT = cdrom:\\SLPS_035.53;1`), lalu loader menyelesaikan 187 chunk executable. Dalam tes headless, log mencatat `EXEC:PC0(80011448)` dan `Execute !`; ini membuktikan loader menyerahkan kendali ke alamat entry executable, bukan membuktikan menu sudah digambar.
- Peringatan `Unknown command for pad: 43` hilang untuk kedua build setelah Port 1 disetel `Analog`, `Connected=true`, dan di-remap melalui `PCSX.SIO0.slots[1].pads[1].map()`. Catatan pembanding: [Actions #38973267415](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973267415).
- Callback penghitung `GPU::Vsync` dapat berjalan stabil sampai lebih dari 2.040 frame dan mencapai marker entry ketika tidak membaca register CPU: [Actions #38974763602](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974763602).

### Pertanyaan yang masih terbuka

- Capture GUI 10s/20s sebelumnya memang seluruhnya hitam, tetapi diambil sebelum titik executable entry (yang pada headless terjadi sekitar frame 1.620, kira-kira 27 detik pada laju sekitar 60 VSync/s). Jadi hasil awal itu **belum membuktikan layar akan terus hitam**.
- Tes GUI yang diperpanjang hingga frame 30s, 60s dan 90s sedang berjalan: [Actions #38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679). Hasil akhirnya perlu memeriksa metrik gambar dan OCR yang dihasilkan dari frame lokal yang dibersihkan saat cleanup.
- Kedua AppImage terkemas yang tersedia tidak memiliki Lua API `PCSX.CPU.Trace`; percobaan tersebut gagal sebelum trace dijalankan. Workflow sekarang membangun source PCSX-Redux pada commit upstream yang dipatok agar built-in trace tersedia: [Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756). Hasil build/trace belum terverifikasi.
- Pembacaan register CPU secara langsung dari callback VSync menyebabkan emulator berakhir dengan segfault pada eksperimen sebelumnya. Jangan memakai hasil trace itu untuk menyatakan bahwa game macet atau ROM rusak.

### Gate sebelum riset aturan main

1. Pastikan capture setelah entry menunjukkan title/menu Naruto yang benar-benar dikenali, bukan sekadar piksel non-hitam.
2. Uji input secara terkendali hanya setelah ada frame/menu yang dapat dikenali.
3. Baru setelah kedua gate tersebut terpenuhi, mulai test case biaya, income, battle, kartu, kepemilikan, dan kondisi kemenangan di bagian berikutnya.

---


## GUI probe result — 2026-10-17

Actions [#38973709926](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38973709926): Xvfb root frames at 10s and 20s were both all-black (`1280x800`, mean 0, standard deviation 0, one color), and OCR returned no text. The GUI probe showed BIOS/disc/controller setup in logs but no `EXEC:PC0`/`Execute !` marker during 35s; do not interpret that as the same boot result as headless mode.

A separate no-UI CPU trace is now implemented in [workflow file](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/blob/main/.github/workflows/naruto-cpu-trace.yml) and running as [Actions #38974255045](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38974255045). It logs the PC/RA/SP every 30 `GPU::Vsync` callbacks up to 600 frames. Use the final logs to determine whether frame callbacks occur and whether the guest PC changes; next step depends on that evidence.

---



## Cloud runner retest gate — updated 2026-10-17

The asset/entry test completed successfully in [run #38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679): private release retrieval, ROM size/hash, CUE validation, OpenBIOS and disc recognition, 187 executable chunks, and `EXEC:PC0(80011448)` / `Execute !` were logged. Analog Port 1 suppressed `Unknown command for pad: 43` in both compared builds.

The former GUI metrics are invalid for diagnosing game display because the script captured the Xvfb root, not the emulator window. The corrected probe in [run #39000276365](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365) must produce `CAPTURE_WINDOW` and measurements from that window; a missing window is itself a GUI-startup diagnostic, and the test must not substitute the root background.

The previous source-built CPU trace [run #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) failed before emulation because the host lacked `libcapstone.so.5`. The corrected workflow [run #39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139) installs `libcapstone-dev` and verifies linked dependencies. Its final trace output is still required before diagnosing any guest loop or stall.

**Gate remains closed:** no title/menu identified and no controlled in-game input response yet. Keep test row RT-001 open. Do not start gameplay formula experiments until both observations are independently proven.


## GUI window retest — results and gate update (2026-10-17)

Actions #39000276365 captured the actual PCSX-Redux X11 window at 30s, 60s and 90s; all images were uniformly black by pixel statistics, OCR found no text. The GUI probe log did not show executable chunk completion or EXEC:PC0 / Execute !, unlike the headless -no-ui probes in the same job. Treat this as a GUI-vs-headless boot discrepancy; do not interpret the frames as game graphics after entry.

RT-001 remains Open / blocked. Next investigate why GUI-mode execution does not show the headless boot handoff; only after a recognizable title/menu and a controlled, responsive input are observed should Story Mode state-delta tests begin.
