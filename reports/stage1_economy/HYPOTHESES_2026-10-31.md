# Stage 1 — hipotesis ekonomi dari ledger video (31 Oktober 2026)

## Batas dan skala bukti

Repositori `docs/GAME_RULES.md` memisahkan bukti kode/data, UI terjemahan/panduan, dan hal yang belum pasti, tetapi tidak menetapkan tangga numerik K0–K5. Untuk laporan Stage 1 ini dipakai skala operasional:

- **K0:** hanya ringkasan adegan visual sekunder; belum ada frame mentah yang dibaca ulang.
- **K1:** transkrip/ASR atau teks terjemahan; tidak membuktikan angka UI/game.
- **K2:** angka/perubahan UI dibaca langsung dan cocok pada sedikitnya dua frame berbeda dengan timestamp terikat.
- **K3:** instruksi/data ROM statis dan aritmetika cocok, tetapi semantik atau pemetaan runtime masih sebagian.
- **K4:** call chain statis ditutup (sumber, pembacaan tabel, mutasi state, dan pembaca/penulis relevan) dengan identitas resource terverifikasi; belum berarti runtime.
- **K5:** perilaku runtime diuji dan direproduksi dengan kontrol.

Skala ini tambahan laporan, bukan kutipan skala resmi yang sudah ada. K2 dan K4 tidak dicapai pada bukti video / analisis ini. Maksimum hipotesis di dokumen ini K1 karena ledger hanya memuat ringkasan K0 dan transkrip K1.

## Q1 — pendapatan dari petak: kapan dibayar dan rumusnya?

### Hipotesis A — kredit dibayar pada akhir satu lap
Streamer menyatakan tiap lap selesai memberi poin dari petak yang dimiliki sampai target (30:33–31:06; ledger O-005, K1). Hipotesisnya, transisi akhir lap menjalankan agregasi record petak milik pemain lalu menambahkan hasilnya ke saldo.

**Residu terhadap ledger:** tidak dapat dihitung. O-005 tidak memiliki saldo sebelum/sesudah, daftar petak, level, nilai per petak, atau satu event payout yang terlihat. Tidak ada tiga pengamatan numerik independen.

**Pengamatan pemfalsifikasi:** rekam saldo dan daftar petak tepat sebelum/sesudah tiga transisi akhir lap. Bila saldo tidak bertambah pada transisi tersebut tetapi berubah ketika pemain mendarat di petak lawan/aksi lain, hipotesis A gugur.

### Hipotesis B — tidak ada kredit otomatis akhir lap; angka petak adalah nilai fee/score yang direalisasikan pada interaksi lain
Ringkasan visual hanya melaporkan sebuah angka toll 580 (O-004, K0), sedangkan klaim payout akhir lap hanya berasal dari ucapan streamer (O-005, K1). Kemungkinan lain ialah angka per-petak dipakai sebagai fee yang timbul ketika pemain masuk petak lawan atau sebagai nilai skor/proyeksi; kenaikan saldo, bila ada, dipicu kejadian lain.

**Residu terhadap ledger:** juga tidak dapat dihitung. Tidak ada saldo sebelum/sesudah saat masuk tile, tidak ada konfirmasi pembayaran, dan O-004 tidak mencatat transfer aktual.

**Pengamatan pemfalsifikasi:** satu siklus yang memisahkan (a) melewati petak milik sendiri, (b) mendarat di petak lawan, dan (c) akhir lap. Jika saldo bertambah hanya pada akhir lap, B gugur; jika saldo hanya berubah pada landing, A gugur.

**Keputusan Q1:** ledger belum dapat memilih A atau B. Tidak ada rumus pendapatan yang layak dihitung.

## Q2 — biaya build dan upgrade Barrier L1–L5

### Hipotesis A — jadwal harga tetap per aksi/level
Pembangunan dan setiap tingkat upgrade mungkin menggunakan harga tetap untuk setiap jenis aksi (misalnya satu biaya build universal dan satu harga untuk tiap langkah upgrade), tanpa bergantung pada tile.

**Residu terhadap ledger:** nol titik harga yang dibaca dari dua frame. O-001 hanya melaporkan pembangunan L1; O-002/O-003 hanya melaporkan Mizuki mencapai L3/L5. Chakra sebelum/sesudah dan harga semuanya BELUM BISA.

**Pengamatan pemfalsifikasi:** bandingkan tiga tile berbeda pada kondisi stage/pemain yang sama untuk build, lalu bandingkan masing-masing transaksi L1→L2, L2→L3, L3→L4, dan L4→L5. Harga yang berbeda pada aksi/level identik memfalsifikasi jadwal tetap universal.

### Hipotesis B — harga bergantung pada tile/record, tipe Barrier, level, atau konfigurasi stage
Harga bisa berasal dari tabel/field petak atau faktor kondisi, sehingga biaya untuk aksi yang tampak sama dapat berbeda antar petak atau stage.

**Residu terhadap ledger:** juga tidak dapat dihitung; O-001 s.d. O-003 tidak mempunyai identitas tile, harga, atau delta Chakra.

**Pengamatan pemfalsifikasi:** tunjukkan beberapa build pada tile dengan atribut/record berbeda tetapi harga sama, lalu ulangi untuk seluruh transisi level. Bila harga identik di seluruh kondisi yang relevan dan perubahan level saja menjelaskan semuanya, versi hipotesis yang bergantung tile/tipe gugur.

**Jangkar lama bukan sampel ledger:** angka 60 (build), 150 (L1→L2), L1 bernilai 100/durability 2/2, dan L1 lain bernilai 50 tercatat dalam `docs/GAME_RULES.md` sebagai contoh UI dari terjemahan komunitas. Itu bukti K1/teks eksternal, bukan pembacaan frame Stage 1 di ledger; angka tersebut tidak dipakai untuk mem-fit harga.

**Keputusan Q2:** tidak ada biaya L1–L5 yang terverifikasi. Khususnya, biaya untuk upgrade L2→L3 hingga L4→L5 masih belum diketahui.

## Q3 — Chakra dari 結界開放 (Barrier release)

### Hipotesis A — pelepasan otomatis ketika saldo melewati ambang negatif; hasil dihitung dari nilai/level aset
O-006 (K0) hanya menunjukkan secara garis besar bahwa pelepasan Barrier terjadi setelah saldo Mizuki negatif. Mekanisme bisa otomatis, dengan pemilihan aset dan kredit/penyesuaian Chakra berdasar nilai record atau level.

**Residu terhadap ledger:** tidak ada jumlah Chakra sebelum/sesudah, tile yang dilepas, levelnya, urutan pelepasan, atau angka hasil. Jadi tidak ada perhitungan yang dapat diuji.

**Pengamatan pemfalsifikasi:** frame berurutan menunjukkan prompt pilihan yang menunggu input pemain dan tile hanya dilepas setelah pilihan/konfirmasi. Itu memfalsifikasi versi otomatis tanpa input.

### Hipotesis B — pelepasan dipilih pemain/AI sebagai tindakan, dengan refund tetap atau nilai salvage
Pelepasan mungkin meminta pemilik atau AI memilih Barrier, lalu mengembalikan nilai tetap atau proporsi dari harga/nilai aset.

**Residu terhadap ledger:** tidak ada bukti prompt, cursor, input, nilai refund, atau petak yang dilepas. Hipotesis ini tidak lebih kuat dari A.

**Pengamatan pemfalsifikasi:** jalankan observasi tanpa input sesudah keadaan pemicu tercapai. Jika beberapa Barrier dilepas otomatis dan event selesai tanpa prompt/pilihan, versi pilihan manual gugur. Untuk menguji rumus, harus ada sekurangnya tiga pelepasan terpisah dengan nilai/level aset dan delta Chakra terukur.

**Keputusan Q3:** tidak diketahui apakah release otomatis/dipilih, serta tidak diketahui jumlah maupun formula Chakra yang dikembalikan/diubah.

## Ringkasan

Ketiga Q tetap BELUM TUNTAS pada tingkat video. Satu-satunya klaim tentang payout per lap (O-005) adalah K1 dari streamer; adegan build/upgrade/release hanya tersedia sebagai K0 dari ringkasan adegan. Tidak ada regresi numerik yang valid karena ledger tidak memiliki tiga titik perubahan saldo dan inventory yang dapat dibaca. Tidak ada status WAIT/UNKNOWN/NO-GO yang diubah.
