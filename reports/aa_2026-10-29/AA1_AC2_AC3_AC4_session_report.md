# AA1/AC2/AC3/AC4 — laporan sesi 2026-10-29

## Skala K
- K1: dugaan/indikasi, belum diuji.
- K2: bukti tidak langsung atau log parsial.
- K3: bukti yang dapat ditinjau tetapi ada celah penting.
- K4: bukti langsung, artefak/log/permalink dapat diperiksa ulang.
- K5: runtime terulang pada sedikitnya dua run independen. Analisis statis maksimal K4.

## Ringkasan status
- AC1: SEBAGIAN, K2. Run 40848251356 hanya satu run per checkpoint; harness GDB yang dikomit belum menangkap bukti yang diminta. Tidak ada dasar menyimpulkan akar crash.
- AC2: BELUM, K1. Tidak ada parsing/dekompresi savestate atau tabel protobuf field yang dijalankan dalam sesi ini; nilai RAM [0x801CEF04] belum dibaca ulang.
- AC3(i): SEBAGIAN, K3. Provenance artefak kontrol terhubung ke run 39867730674 dan artifact ID 12464258211, tetapi asal persis file .sstate di dalam ZIP belum dibuka/dibuktikan.
- AC3(ii): SEBAGIAN, K2. Metadata langkah dan sebagian log tersedia; tabel komparatif lengkap head/workflow, build, GDB, runner dan gerbang frame belum direkonstruksi.
- AC3(iii): BELUM, K1. Hipotesis build/flag berbeda belum diuji terhadap bukti build yang cukup.
- AC4: BELUM, K1. Permintaan anonim Release API dan HEAD/range aset belum dijalankan. Tidak ada status HTTP yang boleh diklaim.
- AB2: TETAP TERTUTUP. Tidak ada AB2/AB3 tambahan yang dikerjakan.

## AC1 — hasil runtime yang benar-benar ada
Workflow sumber: [aa1-restore-gdb-diagnostic.yml pada commit 64be99b0ea2d927216a7195dd95e85fbf8cd3612](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/64be99b0ea2d927216a7195dd95e85fbf8cd3612/.github/workflows/aa1-restore-gdb-diagnostic.yml).
Run [40848251356](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40848251356), job [123360980473](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40848251356/job/123360980473), menggunakan PCSX-Redux 0c3572c3d, AppImage SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c. Target 21,163,286 byte, SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d; kontrol SHA-256 9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492. Tidak ada input tombol.

Target: log mencatat CD-ROM SLPS-03553, BIOS dimuat, AA1_LOAD_BEGIN, lalu frame/backtrace yang tercetak (#1 0x15884b0, #2 0x14f3420, #3 0x7ffff0de5870, #4 0). Tidak tercatat SIGSEGV, SaveStateLoaded, LOAD_CALL_RETURNED atau 180 VSync. Exit code yang dicetak 0 bukan bukti emulator pulih; log tidak memadai untuk menyatakan crash atau hang secara definitif. Harness menjalankan GDB dengan `-ex 'echo \\n...'` dan `tail -n 90`, bukan file perintah GDB seperti yang diminta; informasi yang diperlukan (info threads, thread apply all bt 12, x/3i $pc, register terpilih, mappings) tidak dikumpulkan. Karena itu stack yang ada bukan backtrace crash yang terverifikasi dan akar masalah TIDAK TAHU.

Kontrol: AA1_EVENT_SAVE_STATE_LOADED=1, AA1_LOAD_CALL_RETURNED=1, AA1_POST_LOAD_VSYNC=180, inferior exited normally. Sesudah keluar, perintah backtrace menghasilkan “No stack” dan GDB exit 1; ini adalah backtrace pasca-keluar, bukan kegagalan restore.

Raw laporan yang sudah ada (dibuat workflow, bukan log mentah lengkap): [reports/aa_2026-10-29/AA1_restore_gdb_diagnostic.md pada commit 7593abe](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/7593abe/reports/aa_2026-10-29/AA1_restore_gdb_diagnostic.md). Log job: [job 123360980473](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40848251356/job/123360980473). AC1 belum memenuhi dua run per keadaan atau arsip 40 baris awal + 250 akhir GDB/PCSX yang diminta.

## AC2 — statis
BELUM dikerjakan. Belum ada bukti byte awal target/kontrol, deteksi format/dekompresi, rujukan definisi protobuf pada PCSX-Redux commit 0c3572c3d, tabel field top-level (wire type/length/SHA), field berbeda turun satu tingkat, penjumlahan selisih +740 B, atau word RAM [0x801CEF04] dibanding 0x16C. Ukuran raw target yang sudah dipatok workflow adalah 21,163,286 byte. Ini tidak boleh dicampur dengan ukuran hasil dekompresi yang belum diketahui.

## AC3 — asal dan komparasi run
(i) Run [39867730674](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39867730674), job 120134061270, memiliki artifact [naruto-storymode-adaptive-player-private, ID 12464258211](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39867730674/artifacts/12464258211), 4,913,880 byte, digest ZIP sha256:026c4c38451003e2001a8146ec9a69884ca4aa0fd39a541ece54785be6096328, head SHA c9b1438292041f972b712f248fb7052032635b59. Step “Download selected private source checkpoint artifact” selesai. Namun isi ZIP belum diperiksa di sesi ini, sehingga bahwa file bernama adaptive-cycle-01-f180.sstate persis berasal dari artifact itu: TIDAK TAHU.

(ii) Run [39262213468](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468) menggunakan workflow lama gpu-traffic-summary; job 118092519254. Log menunjukkan cold-start gameplay hingga VSync 10055 dan artefak private checkpoint; itu bukan bukti restore target. Run [40844474886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40844474886), job 123348484949, memakai fixed-schedule RAM compare dan gagal kriterianya; raw identity mencatat emulator SHA c04b3e0..., disc SHA 58c389..., BIOS SHA 5e84a9..., schedule source run 39262213468, final VSync 10055, checkpoint_load=NO (cold boot only). Run 40848251356 memakai workflow AA1 di atas, runner ubuntu-24.04, timeout workflow 18 menit, timeout per kasus 110 detik, GDB dipanggil tanpa skrip perintah; emulator direct ELF /bin/pcsx-redux. Tabel lengkap perbedaan head_sha, cara build/unduh, versi GDB, runner image dan gerbang frame BELUM terverifikasi; jangan isi nilai yang hilang dengan tebakan.

(iii) Hipotesis “target dibuat oleh build/flag berbeda dari loader saat ini”: BELUM DIUJI. Fakta bahwa kontrol dipulihkan sampai 180 VSync sementara target tidak mencetak event restore adalah perbedaan hasil, bukan bukti bahwa build/flag saat penyimpanan berbeda. Tidak ada bukti build saat checkpoint target dibuat yang cukup untuk menerima atau menolak hipotesis.

## AC4 — akses anonim aset Release
BELUM dijalankan. Belum ada daftar Release anonim (tag/draft/prerelease/nama dan ukuran aset), dan belum ada hasil `curl -s -o /dev/null -w '%{http_code} %{redirect_url}'` untuk asset ID 647346873, 652373928, 686794219. Status HTTP per aset: TIDAK TAHU. Tidak ada aset dihapus, visibilitas diubah, atau hash diubah.

## Mitigasi yang dapat dipertimbangkan (belum diterapkan)
1. Pisahkan artefak riset teks publik dari aset runtime privat; audit visibilitas Release dan artifact secara read-only dahulu.
2. Jika aset privat terpapar publik, pemilik repo dapat memutuskan memindahkan aset ke penyimpanan privat atau membatasi akses; jangan menghapus/mengubah visibilitas tanpa keputusan pemilik.
3. Perbaiki harness terlebih dahulu, jalankan minimal dua pengulangan target dan kontrol tanpa input, dan simpan log teks tersanitasi saja. Jangan menyimpulkan akar masalah tanpa signal dan stack pada saat kegagalan.
4. Jangan membuka AB2 sampai restore stabil dibuktikan.

## Batasan dan status
Tidak ada ISO, BIOS, savestate, RAM dump, screenshot privat atau konten unduhan yang dikomit oleh laporan ini. Story Mode tidak terbukti tamat. Semua bagian yang belum memiliki bukti langsung tetap BELUM/TIDAK TAHU.
