# Analisis akar SIGSEGV: sentinel cursor SPU/ADPCM (20 Oktober 2026)

## Kesimpulan sementara

**Hipotesis berkeyakinan tinggi, belum terkonfirmasi lewat eksperimen perbaikan:** receiver board-screen kemungkinan jatuh karena bug lama PCSX-Redux ketika memulihkan cursor suara ADPCM yang sudah berhenti. Build yang dikunci di workflow adalah PCSX-Redux commit `0c3572c3db75f97542001e453ae80ba8c3f8acba` (1 Oktober 2026). Bug itu diperbaiki di upstream melalui PR [#2218](https://github.com/grumpycoders/pcsx-redux/pull/2218), digabung pada 5 Oktober 2026 di commit `807e5cc809c7aceb1d81b973e60313577aa1ad95`.

Ini belum membuktikan Story Mode bisa dipulihkan. Pemulihan board-screen hanya dinyatakan berhasil setelah workflow probe khusus lulus seluruh gerbang di bawah.

## Sumber checkpoint dan integritas

| Item | Nilai |
|---|---|
| Run sumber | [#39262213468](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468) |
| Frame / keadaan | 10055 / layar papan permainan stabil, `stable_non_dialog` |
| Raw source | 21.163.286 byte |
| SHA-256 raw source | `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d` |
| Screenshot sumber | 320×240, SHA-256 `101b94a4d171d228e0224948872b65b88bf84fd0d92dc8ddd0b6cfeb21f790a8` |
| Receiver gagal | [#39314115221](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39314115221) |
| Build emulator saat crash | PCSX-Redux commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`; AppImage SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c` |

Staging source pada receiver cocok byte-per-byte dengan nilai di atas. GDB mencatat instruksi `movzbl (%rsi),%ecx` saat `PCSX.loadSaveState()` berlangsung; RSI `0xffffffffd736a15f` tidak menunjuk memori terpetakan. Loader tidak kembali, event `ExecutionFlow::SaveStateLoaded` tidak muncul, dan tidak ada screenshot pascapulih/180 VSync/checkpoint lanjutan.

Raw state asli **tidak diubah**. Varian tersanitasi lama menghapus BIOS di field 3 dan tidak mengubah field 6; itu bukan eksperimen untuk penyebab ini.

## Schema protobuf sudah dipetakan dari source build yang dipatok

Source commit yang sama mendaftarkan API Lua `PCSX.getSaveStateProtoSchema()` di [`src/core/pcsxlua.cc`](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/pcsxlua.cc#L219-L228). API memanggil `SaveStates::ProtoFile::dumpSchema()` lalu mengembalikan teks schema; tidak perlu memanggil loader atau mengubah state. Keberadaannya telah diverifikasi dalam source yang sama dengan build, **runtime smoke test terhadap binary masih menunggu**. Workflow probe khusus melakukan smoke test tersebut sebelum build varian dan menyimpan teks schema sebagai artifact.

Path field protobuf yang kini diketahui:

- Top-level field `6` bernama `spu` (`SPUField`).
- Di dalam `spu`, field `6` adalah repeated `channel` (24 channel).
- Di dalam tiap `channel`, field `1` adalah `data` (`ChannelData`).
- `channel.data.current` adalah field `8`; `start` field `7`; `loop` field `9`; `on` field `10`; `stop` field `11`. Field `stop` berarti sampel telah berhenti, namun suara masih mungkin berada di fase ADSR release.
- Subfield SPU `3` bernama `xa`; payload 32.781 byte tersebut hadir di board, tidak di boot.

Referensi schema dalam source yang dipatok: [`src/core/sstate.h`](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/sstate.h) dan [`src/spu/types.h`](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/spu/types.h).

## Temuan pembanding field cursor

Analisis protobuf dilakukan read-only pada salinan artifact sementara. SHA state di atas sudah diverifikasi setelah dibaca.

| Pengukuran | Raw boot yang berhasil dipulihkan | Raw board yang gagal dipulihkan |
|---|---:|---:|
| Panjang top-level field `6` / `spu` | 593.790 byte | 632.733 byte |
| Jumlah channel | 24 | 24 |
| Channel dengan `current` di luar sound RAM 512 KiB | 24/24 | 20/24 |
| Nilai cursor invalid utama (lower 32-bit) | `0xe9dfc75f` = int32 `-371210401` | `0xd5e7578f` = int32 `-706259057` |
| `SBPos` | 28 seluruh channel | 28 seluruh channel |
| Channel out-of-range dengan flag `stop=1` | 0 | 18 dari 20 |
| Channel yang memiliki flag `on=1` | 0 | 4 (channel 1, 8, 19, 20) |
| SPU subfield `xa` | tidak ada | 32.781 byte |

**Penting:** nilai `current` invalid juga ada di raw boot. Itu tidak menggugurkan hipotesis: boot state berisi 24 channel yang tampak quiescent/inactive (`on` dan `stop` tidak diserialisasi sebagai true), sedangkan board memiliki keadaan channel yang lebih beragam dan 18 channel dengan cursor invalid berflag `stop=1`. Bukti ini menunjukkan nilai cursor bermasalah dan konteks board yang lebih aktif, tetapi tidak mengidentifikasi channel spesifik penyebab fault.

## Hubungan dengan bug upstream

Pada source commit yang digunakan run gagal, `src/spu/adpcm.cc` menyimpan pointer cursor sebagai selisih pointer ke RAM suara yang ditulis ke `int32`. Sentinel `AdpcmDecoder::kStopped` adalah pointer non-null dengan semua bit bernilai 1. Pada mesin 64-bit, selisih itu dapat terpotong saat disimpan. Saat load, kode lama hanya memperlakukan `-1` sebagai null lalu menjumlahkan offset lain ke base RAM; nilai terpotong menjadi pointer liar. Jalur `decodeNextBlock` hanya mengenali sentinel `kStopped` yang tepat, kemudian `decodeBlock` melakukan dereference pada alamat tersebut.

Ini cocok dengan gejala GDB: fault pada pembacaan byte dan alamat tak terpetakan ketika loader berjalan. Laporan upstream [issue #2175](https://github.com/grumpycoders/pcsx-redux/issues/2175) menjelaskan gejala dan penyebab yang sama. [PR #2218](https://github.com/grumpycoders/pcsx-redux/pull/2218) menambah sentinel eksplisit `kStoppedOffset=-2` (null tetap `-1`) dan memulihkan offset di luar batas RAM sebagai stopped. Perbaikan itu juga dirancang memperbaiki state lama yang sudah tersimpan dengan offset terpotong.

## Eksperimen terisolasi yang disiapkan

Workflow baru `.github/workflows/naruto-spu-sentinel-fix-probe.yml` adalah `workflow_dispatch` saja; ia tidak dijalankan otomatis oleh push. Input default source run adalah `39262213468`. Eksperimen ini membangun PCSX-Redux dari commit yang sama dengan binary gagal, lalu menerapkan hanya perubahan dua file `src/spu/adpcm.cc` dan `src/spu/adpcm.h` dari PR #2218 melalui patch yang tersimpan di `experiments/pcsx-redux-spu-adpcm-stopped-cursor.patch`.

**Variabel tunggal yang diubah: binary/source emulator (perbaikan sentinel SPU).** Savestate board raw tetap sama persis; tidak ada rewrite protobuf, sanitizer atau rehidrasi BIOS. Source yang sama pernah gagal dalam receiver sebelumnya sehingga kontrol gagal tersedia.

Workflow merekam dalam artifact privat:
- SHA source raw dan SHA file staging (harus sama);
- commit base source emulator, SHA-256 file patch dan diff sumber yang diterapkan;
- SHA-256 AppImage varian yang dibangun;
- schema dari binary pinned asli dan schema dari build varian serta SHA keduanya;
- event load, penanda loader kembali normal, exit code, penghitung VSync pascarestore;
- hasil perbandingan screenshot dengan gate `mean_abs_rgb_diff <= 6.0` dan exact-pixel fraction `>= 0.70`;
- SHA, ukuran, dan screenshot untuk checkpoint lanjutan yang dibuat setelah 180 VSync.

Probe **tidak menekan tombol dan tidak melanjutkan gameplay**. Setelah restore board melewati event, loader-return, 180 VSync, dan screenshot gate, ia menyimpan checkpoint lanjutan. Proses emulator kedua yang baru kemudian memuat checkpoint itu lagi tanpa input dan harus melewati event, loader-return, 180 VSync, serta screenshot gate yang sama. Checkpoint baru hanya dinyatakan valid bila reload kedua ini juga lulus; eksperimen berhenti tanpa gameplay. Pada fail, artifact menyimpan diagnosis tanpa mengubah raw sumber.

### Kriteria penerimaan

Status hanya boleh ditandai **RESTORE PASS** bila semua syarat ini terpenuhi pada run yang benar-benar dijalankan:

1. source dan staging raw memiliki SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d` serta ukuran 21.163.286 byte;
2. `ExecutionFlow::SaveStateLoaded` terdeteksi dan pemanggilan loader tercatat kembali normal;
3. sedikitnya 180 VSync terverifikasi setelah restore dan proses keluar dengan kode 0;
4. screenshot pascarestore cocok dengan screenshot checkpoint sumber lewat ambang yang tercatat;
5. checkpoint lanjutan nonkosong dibuat, ukurannya serta SHA-256 tercatat dan diverifikasi.

Sebelum workflow manual dijalankan dan hasilnya diperiksa, status tetap **RESTORE BELUM TERBUKTI**. Bila lulus, lanjutkan Story Mode dari checkpoint valid dengan build yang memuat perbaikan yang sama, kemudian buat checkpoint berikut secara berkala.

## Batas kesimpulan saat ini

- **Terverifikasi:** schema API tersedia pada source build pinned; path SPU/channel/current sudah dipetakan; cursor out-of-range terukur pada raw boot dan board; bug upstream yang sangat sesuai sudah ditemukan.
- **Hipotesis berkeyakinan tinggi:** sentinel ADPCM stopped yang salah dipulihkan menjadi pointer liar menyebabkan SIGSEGV board.
- **Belum terverifikasi:** API schema berhasil dipanggil dari binary dalam runner; varian patched memulihkan board; checkpoint lanjutan aman dipakai; Memory Card save/load di dalam game; tamat Story Mode; aturan gameplay.
- Tidak ada sumber 90 menit yang dijalankan ulang. Raw boot/board asli, BIOS, ROM dan Memory Card tidak dimodifikasi atau ditambahkan ke Git.
