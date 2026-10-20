# Perbandingan struktural savestate raw: boot vs Story Mode (20 Oktober 2026)

## Tujuan dan batasan

Pemeriksaan dilakukan secara **read-only** pada ZIP artifact GitHub Actions. File sumber dalam artifact tidak diubah, tidak ada state atau aset game yang ditulis ke Git, dan tidak ada emulator/source run 90 menit yang dijalankan ulang. Salinan sementara untuk perhitungan hash/diff hanya berada di lingkungan analisis.

## Checkpoint yang dibandingkan

| Peran | Run / artifact | Ukuran state | SHA-256 |
|---|---|---:|---|
| Raw boot, diketahui berhasil dipulihkan lintas-run | [Run A #39255438457, artifact #12187367829](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255438457) | 21.124.144 byte | `a4672dd49fbfa76ef60de410c50460d77e115181fc3e205a215ab9f5f1e601d7` |
| Raw Story Mode, layar board frame 10055 | [Run sumber #39262213468, artifact #12196796917](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468) | 21.163.286 byte | `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d` |
| Bukti restore boot berhasil | [Run B #39255549341, artifact #12187962047](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39255549341) | — | Screenshot pascarestore SHA-256 `90aa21b6943bac231e4c0e888923a5d1e9658de28ce5c715b9328b17c046db21` |
| Receiver board gagal pada native loader | [Run #39314115221, artifact diagnostik #12216519993](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39314115221) | — | SIGSEGV selama `PCSX.loadSaveState()` |

Kedua state raw memiliki header `PCSX-Redux SaveState v4`. State Story Mode berukuran 39.142 byte lebih besar. Dalam panjang bersama 21.124.144 byte, 2.579.414 posisi byte berbeda (sekitar 12,21%); angka ini hanya menunjukkan perbedaan keadaan serialisasi, bukan bukti korupsi.

## Hasil struktur yang terukur

Top-level field `1` memiliki isi identik. Ringkasan lain:

| Field top-level protobuf | Boot raw | Board raw | Perbedaan |
|---|---:|---:|---|
| `3` | 19.464.215 byte payload | 19.464.215 | Panjang sama, isi berbeda |
| `4` | 8.443 | 8.597 | +154 |
| `5` | 1.049.613 | 1.049.613 | Panjang sama, isi berbeda |
| `6` | 593.790 | 632.733 | **+38.943; perubahan ukuran terbesar** |
| `7` | 4.387 | 4.400 | +13 |
| `8` | 2.449 | 2.474 | +25 |
| `10` | 82 | 89 | +7 |
| `11` | 1.109 | 1.109 | Panjang sama, isi berbeda |

Perubahan ukuran field 4, 6, 7, 8, dan 10 menjumlah tepat 39.142 byte. Nama semantik field harus dikonfirmasi dari schema yang dikeluarkan build emulator ini; nomor field di atas adalah fakta penguraian wire-format, bukan nama subsistem yang sudah disahkan.

Dalam top-level field `3`, struktur memory memiliki ukuran subfield yang sama pada kedua state. Subfield `2` (512 KiB) cocok byte-per-byte dengan BIOS ber-SHA-256 `5e84a94818cf5282f4217591fefd88be36b9b174b3cc7cb0bcd75199beb450f1`. Subfield `1` (8 MiB) dan `4` (64 KiB) berbeda isi; subfield `3` (8 MiB) dan `5` (2 MiB) identik.

Top-level field `6` adalah kandidat utama untuk inspeksi schema berikutnya, sebab ia menyumbang +38.943 byte. Di dalamnya:
- subfield `3` berpayload 32.781 byte muncul pada board tetapi tidak pada boot;
- terdapat 24 kemunculan subfield `6` pada keduanya, tetapi payload per-kemunculannya 139 byte pada boot, dibanding 203–481 byte pada board;
- subfield `9` sampai `13` hadir pada board tetapi tidak pada boot;
- payload subfield `1` (524.288 byte) dan `2` (512 byte) juga berbeda isi.

Pola ini konsisten dengan state perangkat/aktivitas emulasi yang lebih kaya di scene board, tetapi tanpa pemetaan field ke schema yang tepat belum boleh disimpulkan bahwa salah satu subfield tersebut adalah penyebab SIGSEGV.

## Perbandingan raw board vs varian tersanitasi dari checkpoint yang sama

Artifact sumber #12196796917 juga berisi `storymode-checkpoint.sstate`, yakni varian tersanitasi:
- Raw: 21.163.286 byte, SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`.
- Tersanitasi: 20.638.994 byte, SHA-256 `b94e61502b63a81107f48153932ccbef21bede8c7f53d4b01e6e013ecb8979eb`.
- Selisih ukuran tepat 524.292 byte. Perubahan strukturnya hanya menghapus subfield `2` sepanjang 524.288 byte di dalam top-level field `3` (payload BIOS), termasuk 4 byte framing tag/panjang yang dihapus; panjang pesan induk diperbarui.
- Payload top-level fields `1`, `4`, `5`, `6`, `7`, `8`, `10`, dan `11` sama persis antara raw board dan varian tersanitasi. Jadi field `6` yang menunjukkan perubahan terbesar **tidak diubah oleh sanitasi BIOS tersebut**.

Artinya, menguji varian tersanitasi ini hanya mengisolasi ada/tidaknya field BIOS di state, bukan mengisolasi perubahan di field `6`. Varian itu bukan pengganti otomatis untuk raw checkpoint. Menghapus BIOS juga tidak boleh diasumsikan memperbaiki native crash.

## Kesimpulan dan eksperimen berikutnya

**Terverifikasi**
1. Raw boot dari #39255438457 berhasil dipulihkan pada runner/proses baru di #39255549341, dengan `SaveStateLoaded`, loader kembali, 180 VSync, screenshot valid, dan exit 0.
2. Raw board dari #39262213468 tiba tanpa perubahan byte pada staging receiver #39314115221, tetapi crash di dalam `PCSX.loadSaveState()`.
3. BIOS di dalam kedua state raw identik; file varian tersanitasi dari board menghapus hanya field BIOS pada memory submessage.
4. Belum ada bukti restore Story Mode, 180 VSync pascarestore, screenshot pascarestore, atau checkpoint Story Mode lanjutan yang valid.

**Hipotesis**
- Penyebab lebih mungkin terkait nilai/perangkat state yang aktif di checkpoint board daripada kesalahan transfer file. Top-level field `6` merupakan kandidat untuk diteliti terlebih dahulu karena perubahan ukuran terbesar, tetapi kaitan kausal ke crash belum terbukti.
- Perbedaan besar dalam payload memory serta field lain wajar terjadi antara boot dan Story Mode; ukuran/hash yang berbeda bukan indikasi kerusakan.

**Langkah eksperimen yang dipilih**
1. Jangan mengulangi receiver raw board dengan setup identik.
2. Pertama verifikasi apakah **build PCSX-Redux yang sama** menyediakan API Lua `PCSX.getSaveStateProtoSchema()`. Jika tersedia, ambil schema tanpa memanggil loader dan tanpa mengubah state; jika tidak tersedia, cari sumber schema read-only yang cocok dengan build tersebut. Jangan menganggap API itu ada sebelum diverifikasi. Gunakan schema tersebut untuk memberi nama subfield `6`, `3`, `9`–`13`, dan membandingkan boot vs board.
3. Setelah pemetaan schema diketahui, rancang satu eksperimen faktor-tunggal pada **salinan eksperimen** saja bila ada subfield spesifik yang layak diuji. Catat parent hash, transformasi field/path/byte yang tepat, dan hash varian. Uji diagnostik harus berhenti setelah bukti pemulihan (event, loader kembali, ≥180 VSync, screenshot) dan tidak melanjutkan gameplay dari varian.
4. Pertahankan raw board asli dan manifest/hash-nya tanpa perubahan. Jangan jalankan ulang sumber 90 menit; jangan commit ROM, BIOS, savestate, atau Memory Card.

Game belum terbukti tamat. Aturan main tetap hanya dapat ditandai terverifikasi dari bukti gameplay langsung.
