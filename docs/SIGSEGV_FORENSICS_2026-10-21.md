# Forensik SIGSEGV dan stall VSync — 21 Oktober 2026

## Ruang lingkup dan aturan tetap

Investigasi dilakukan hanya pada repositori `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`. Semua eksperimen diagnostik di bagian ini memakai checkpoint dialog pra-START `dialog-entry-f178.sstate` (21.162.258 byte; SHA-256 `c47d2069ae9b1e589cce35df2dbaaa867b3365acfd501d2666a72ecd5fcc494c`) dan tidak mengirim input controller. Checkpoint induk `stable-postconfirm-checkpoint.sstate` (21.163.483 byte; SHA-256 `b7d86f572f929d13aeb24d9b710e455610c2723f336b68acf32f7cca2e8fe4ee`) hanya dibaca/diverifikasi dan tidak diubah. Screenshot internal emulator dihentikan setelah frame 130; screenshot eksternal dilakukan melalui X11/XWD. Screenshot seragam hitam tidak diterima sebagai bukti gameplay.

## Run #39574435847 — SIGSEGV saat frame berhenti di 151

- Run Actions: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39574435847
- Workflow selesai `success` pada 16:08:25 WIB; proses emulator sendiri keluar 139 dan log shell secara eksplisit mengatakan `Segmentation fault (core dumped)`. Keberhasilan workflow hanya berarti diagnostik dan pengumpulan artefak selesai.
- Watchdog mencatat frame 151 pada 16:08:10.907 WIB, kemudian stall 2,576 detik. Screenshot X11 pertama valid pada 1280×800 RGB, 777.527 byte dan 131.762 warna. Screenshot asli memperlihatkan dialog Naruto masih terbuka, prompt Circle, dan HUD 1500–1500. Screenshot kedua 458 byte hitam seragam dan ditolak validator.
- Snapshot proses saat stall menunjukkan AppRun dalam state `Sl`, `wchan=vfs_coredump`; keadaan itu konsisten dengan proses di jalur core dump sesudah sinyal fatal, tetapi tidak mengidentifikasi fungsi penyebab.
- 28 screenshot internal f001–f130 valid; tidak ada screenshot internal setelah f130. Artefak privat #12333511723 (4.139.742 byte, digest ZIP `sha256:63497731a6e361aff98f9e0f2f0a895010987b87250aadfc72c82a74ba6ed23c`).
- Kesimpulan terbatas: crash terjadi tanpa input controller dan tanpa screenshot internal terlambat; mengambil screenshot internal sekitar f150 bukan syarat yang diperlukan untuk SIGSEGV. Root cause native belum diketahui.

## Run #39576146808 — stall/timeout, tidak ada core lokal

- Run Actions: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39576146808
- Workflow selesai `success`; frame terakhir 152 lalu timeout exit 124. Tidak ada input controller; 28 screenshot internal f001–f130 valid; checkpoint induk tetap memiliki hash yang sama.
- Dua screenshot X11 dari luar emulator valid: yang pertama 779.940 byte/133.543 warna unik, yang kedua 777.991 byte/132.394 warna unik. Keduanya menunjukkan dialog game yang masih terbuka; gambar tidak persis identik sehingga sebagian elemen latar terus bergerak/beranimasi meskipun callback frame berhenti.
- Kernel core pattern runner adalah `|/usr/lib/systemd/systemd-coredump %P %u %g %s %t 9223372036854775808 %h %d`. Tidak ditemukan berkas core di ruang kerja; `gdb` post-mortem tidak berjalan. Ini menjelaskan mengapa frasa `(core dumped)` sendiri tidak memberi backtrace yang bisa diakses oleh workflow. Artefak privat #12334223690 (4.920.632 byte; digest ZIP `sha256:e99fbb5b87f807f9978f46e98394c7dccaafa2a0360b1f6a87cd6f7619c23f1a`).
- Kesimpulan: kasus ini tidak mereproduksi SIGSEGV. Stall serupa dapat berakhir timeout; akar penyebab timeout/crash belum bisa disamakan.

## Run #39576905583 — backtrace live atas stall frame 153

- Run Actions: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39576905583
- Emulator dijalankan di bawah GDB dengan aturan SIGSEGV stop, no-pass. Watchdog melihat frame 153 lalu stall sekitar 2,531 detik; dua screenshot X11 valid diambil sebelum interupsi host. Interupsi `SIGINT` hanya dipakai untuk menghentikan proses native di debugger dan memperoleh stack, bukan input tombol game.
- Proses tidak menerima SIGSEGV pada run ini. Setelah SIGINT diagnostik dari watchdog, GDB mencetak stack semua thread dan keluar normal, sehingga wrapper exit code 0 tidak boleh dianggap sebagai emulator mencapai target f175. Log awal mengklasifikasikan hasil `INCONCLUSIVE rc=0`; inspeksi langsung `pcsx-DIAGNONE.stdout` menemukan stack yang tercetak, kemudian parser workflow diperbaiki untuk mengenali format pesan GDB `Thread 1 "AppRun" received signal SIGINT`.
- Stack thread utama: `__syscall_cancel_arch` → `__futex_abstimed_wait_common64` → `__pthread_cond_wait` → `libgallium` → `libGLX_mesa` → `libSDL3` → alamat tidak tersimbolkan di `pcsx-redux`. Dua thread `llvmpipe` memiliki frame alamat tak bernama di renderer; sejumlah worker thread lain menunggu pada futex/condition variable. Binary `pcsx-redux` stripped, Build ID `a8af2c40eca1eb69865e6b0a28b46ae3184ab13e`.
- Interpretasi: stack ini merupakan bukti langsung bahwa saat stall f153, thread utama sedang menunggu pada jalur sinkronisasi renderer/OpenGL berbasis Mesa/SDL. Ini petunjuk lokasi stall, bukan bukti bahwa Mesa/SDL menyebabkan SIGSEGV pada run #39574435847. Backtrace SIGSEGV belum diperoleh. Artefak privat #12335260015 (4.939.777 byte; digest ZIP `sha256:9e36749e6d9fda93598e75c3a7485daa7a8d4d22bb79df72419fec62d1fb2223`).
- Kedua screenshot X11 dari run ini valid (1280×800); gambar menunjukkan dialog Naruto masih terbuka dengan prompt Circle. Tidak ada bukti visual misi aktif.

## Run berikutnya dan kriteria penilaian

Run #39577470148 sedang berjalan saat dokumen ini mulai ditulis; hasil aktualnya akan ditambahkan setelah log dan artefak diperiksa. Workflow telah diperbarui untuk memberi jendela 0,75 detik setelah capture eksternal agar SIGSEGV alami dapat ditangkap GDB sebelum watchdog mengirim SIGINT untuk backtrace stall, serta agar parser mengenali format signal GDB yang sebenarnya. Hanya teks log/backtrace yang diunggah; core dump besar tidak dimasukkan ke artefak. Marker trigger sekali-pakai harus selalu dihapus sesudah run selesai.

**Status saat ini:** akar penyebab SIGSEGV belum terkonfirmasi. Jangan mengulang tap START satu-VSync yang sama, jangan mengganti/menimpa checkpoint, jangan memakai Circle untuk dialog, dan jangan menyatakan misi aktif atau Story Mode tamat tanpa screenshot asli game yang membuktikannya. Jika dialog muncul saat permainan benar-benar dilanjutkan, operasionalnya gunakan START untuk skip dialog. Semua bukti visual gameplay harus berasal dari screenshot asli emulator/X11, tidak dari web atau gambar buatan.
