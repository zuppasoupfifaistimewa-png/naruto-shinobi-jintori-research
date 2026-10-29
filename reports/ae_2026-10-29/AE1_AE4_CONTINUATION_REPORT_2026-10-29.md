# Laporan kelanjutan AE1–AE4 — 29 Oktober 2026

## Skala K
- **K1**: dugaan.
- **K2**: indikasi terbatas.
- **K3**: beberapa bukti saling mendukung.
- **K4**: bukti langsung yang dapat diperiksa ulang; analisis statis maksimal K4.
- **K5**: runtime konsisten pada sedikitnya dua peluncuran terpisah.

## Status ringkas

| Butir | Status | K | Temuan yang dapat dinyatakan |
|---|---|---:|---|
| AE1 — peta protobuf dan ukuran field | TUNTAS | K4 | Field top-level 6 adalah pesan SPU. Di dalam `SPU.channel[2]`, field 1 (`data`) saja cukup menghasilkan SIGSEGV pada dua peluncuran; lebih dalam, `ChannelData.current` field 8 sendiri juga cukup dalam konteks kontrol. |
| AE2 — keperluan (necessity) | SEBAGIAN | K5 untuk uji yang selesai | Mengganti `SPU.channel[2].data.current` kembali ke nilai kontrol pada state target tetap SIGSEGV dua kali di PC yang sama. Maka field itu tidak diperlukan untuk mereproduksi crash target. Uji mengganti keseluruhan top-level SPU field 6 di state target berakhir inconclusive/timeout; perlu field 6 secara keseluruhan tetap TIDAK TAHU. |
| AE3 — provenance/build | SEBAGIAN | K4 | Runtime target memverifikasi AppImage SHA-256 `c04b3e0a…bd60fc0c`, source pin `0c3572c3d`, dan flags dalam log. Run 39262213468 mengunduh AppImage yang sudah diterbitkan; log run itu bukan bukti workflow pembuat AppImage. Control producer 39867730674 memakai container `ghcr.io/grumpycoders/pcsx-redux-build:latest` dan AppImage patched SHA-256 `2fb33f63…7035ba99`. |
| AE4 — hash RAM 2 MiB dan tiga word | BELUM TUNTAS | K2 | Lima hibrida AD3 berhasil direkonstruksi dengan SHA-256 yang persis sama seperti hibrida sebelumnya, tetapi setiap percobaan AE4 baru berakhir TIMEOUT pada sekitar 10 detik. Tidak ada snapshot pada POST_LOAD_VSYNC=180; hash RAM dan nilai alamat tidak tersedia. Timeout bukan bukti SIGSEGV atau kesalahan hibrida. |

## AE1: ukuran pesan

Checkpoint target:
- SHA-256: `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`
- 21,163,286 byte.

Checkpoint kontrol:
- SHA-256: `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`
- 21,162,546 byte.

Ukuran seluruh savestate berbeda 740 byte. Ukuran ter-encode top-level field 6/SPU berbeda **+748 byte** (target − kontrol); field 4 berbeda +1 byte dan field 8 −9 byte. Tabel seluruh field dan subfield SPU menyertakan ukuran payload/encoded dan SHA-256.

Sumber skema yang dipin:
- [`src/core/sstate.h` pada pin 0c3572c3d](https://github.com/pcsx-redux/pcsx-redux/blob/0c3572c3d/src/core/sstate.h) — Git blob SHA-1 `72b7ab0dbd4191f9d9ed4cdd9d77898f467258e2`.
- [`src/spu/types.h` pada pin yang sama](https://github.com/pcsx-redux/pcsx-redux/blob/0c3572c3d/src/spu/types.h) — `Chan::CurrPtr` ialah field 8, nama `current`.

## Runtime AE1/AE2

Run berakhir sukses: [40897542675](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40897542675). Bukti teks dikomit pada `c3e01889178fe701fa0bfe59c7ffebac9f07c2e8`.

| Hibrida | Dua peluncuran | Arti |
|---|---|---|
| Kontrol + hanya `SPU.channel[2].data` target | SIGSEGV; SIGSEGV, PC `0x7ffff0dd36d0` | Pesan `data` cukup memicu crash pada konteks kontrol. |
| Kontrol + hanya `SPU.channel[2].data.current` target | SIGSEGV; SIGSEGV, PC `0x7ffff0dd36d0` | Field `current` cukup memicu crash pada konteks kontrol. |
| Target + hanya `SPU.channel[2].data.current` kontrol | SIGSEGV; SIGSEGV, PC `0x7ffff0dd36d0` | Field `current` tidak diperlukan bagi crash pada state target. |
| Kontrol + pesan `adsr` target saja | TIMEOUT; TIMEOUT | Inconclusive, bukan bukti tidak cukup. |
| Kontrol + pesan `adsr_ex` target saja | TIMEOUT; TIMEOUT | Inconclusive, bukan bukti tidak cukup. |
| Target + seluruh top-level SPU field 6 kontrol | Inconclusive; Inconclusive | Keperluan field 6 secara keseluruhan tidak dapat ditetapkan. |

Tabel byte-per-field:
- [`ae1_field_sizes.tsv`](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/4e028d91d769eacc09f600a1c9484333218cec61/reports/ae_2026-10-29/ae1_field_sizes.tsv)
- [`ae1_spu_subfields.tsv`](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/4e028d91d769eacc09f600a1c9484333218cec61/reports/ae_2026-10-29/ae1_spu_subfields.tsv)
- [Laporan rekursif Channel](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/c3e01889178fe701fa0bfe59c7ffebac9f07c2e8/reports/ae_2026-10-29/deep/AE1_CHANNEL_RECURSIVE_RESULTS.txt)
- [Ringkasan dua peluncuran](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/c3e01889178fe701fa0bfe59c7ffebac9f07c2e8/reports/ae_2026-10-29/deep/runtime-case-summary.tsv)
- [SHA-256 manifest log GDB/PCSX](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/c3e01889178fe701fa0bfe59c7ffebac9f07c2e8/reports/ae_2026-10-29/deep/raw-log-sha256.txt)

Contoh log mentah:
- [`current` target-only, attempt 1 GDB](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/c3e01889178fe701fa0bfe59c7ffebac9f07c2e8/reports/ae_2026-10-29/deep/raw/nested-channel-field1-child8-occ1-attempt1.gdb.txt)
- [`current` target-only, attempt 2 GDB](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/c3e01889178fe701fa0bfe59c7ffebac9f07c2e8/reports/ae_2026-10-29/deep/raw/nested-channel-field1-child8-occ1-attempt2.gdb.txt)
- [Uji kebutuhan `current`, attempt 1 GDB](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/c3e01889178fe701fa0bfe59c7ffebac9f07c2e8/reports/ae_2026-10-29/deep/raw/ae2-target-current-pointer-field8-from-control-attempt1.gdb.txt)
- [Uji kebutuhan `current`, attempt 2 GDB](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/c3e01889178fe701fa0bfe59c7ffebac9f07c2e8/reports/ae_2026-10-29/deep/raw/ae2-target-current-pointer-field8-from-control-attempt2.gdb.txt)

## AE3: lingkungan produser

Target state dihasilkan oleh [run 39262213468](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468), job `118092519254`, runner `ubuntu-26.04`. Workflow memverifikasi AppImage release dengan SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c` dan menjalankan source pin `0c3572c3d` dengan SoftGPU, dynarec, stdout dan Lua stdout; pada probe diagnostic berikutnya, flags tambahan `-noupdate -no-debugger -no-gdb` digunakan agar tidak ada debugger internal. Run checkpoint tersebut tidak membangun AppImage; file diunduh dari release.

Control state berasal dari [run 39867730674](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39867730674), workflow adaptive checkpoint. Workflow memakai host `ubuntu-24.04`, container `ghcr.io/grumpycoders/pcsx-redux-build:latest`, dan artifact AppImage patched SHA-256 `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`. Digest container pada bukti AD ialah `sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`. GDB versi di container producer control tetap TIDAK TAHU.

Konsistensi target AppImage/state sudah diuji terpisah pada dua runner OS di audit AD4: Ubuntu 24.04 dan 26.04 menghasilkan SIGSEGV di Thread 15 dan PC yang sama dua kali per run. Source build/provenance dari pembuat awal release AppImage tidak dapat disimpulkan dari run checkpoint 392622 sendiri.

## AE4: batas hasil

Run [40899089356](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40899089356) sukses pada level workflow dan cleanup. Kelima hibrida AD3 field 3, 4, 5, 8, 10 direkonstruksi **byte-identik** (SHA-256 sama persis dengan hibrida yang dahulu mencapai 180 VSync dua kali). Namun masing-masing dari 10 peluncuran baru berakhir `INCONCLUSIVE_TIMEOUT` pada sekitar 10 detik; tidak ada `POST_LOAD_VSYNC=180`, jadi tidak ada RAM 2 MiB SHA-256 atau nilai raw di `0x80070EB8`, `0x80070F6C`, `0x8013A554`.

Bukti:
- [Ringkasan AE4/hibrida dan hash](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/46b34c94690d43ae7eeb138695b5af86aa24533b/reports/ae_2026-10-29/deep/AE1_CHANNEL_RECURSIVE_RESULTS.txt)
- [Tabel runtime AE4](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/46b34c94690d43ae7eeb138695b5af86aa24533b/reports/ae_2026-10-29/deep/runtime-results.tsv)
- [Manifest hash log AE4](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/46b34c94690d43ae7eeb138695b5af86aa24533b/reports/ae_2026-10-29/deep/raw-log-sha256.txt)

Skrip tersendiri untuk menjalankan ulang AE4 dengan timeout 25 detik tersedia di [`experiments/ae4_ad3_ram_snapshots.py`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/47db6d3d876cf9c1490425c6c767272e61bac01b/experiments/ae4_ad3_ram_snapshots.py). Eksekusi ulang skrip itu belum terverifikasi oleh run Actions; karena itu **belum ada bukti RAM untuk AE4**. Berkas ISO, BIOS, savestate, dump RAM, dan screenshot tidak dikomit. Pembersihan runner pada run 40899089356 berhasil.

## Batas kesimpulan

- Hasil K5 berlaku untuk kombinasi byte state/build/harness yang diuji; tidak menyatakan penyebab universal untuk seluruh savestate.
- Field 8 `current` cukup memicu crash di base kontrol, tetapi penggantiannya pada base target tidak menghilangkan crash; sifat “perlu” dan “cukup” tidak boleh disamakan.
- Keperluan top-level field 6, penjelasan akar masalah dalam kode C++ yang bernama, AE4 RAM hash/nilai word, dan tamat Story Mode: **TIDAK TAHU / belum dibuktikan**.
