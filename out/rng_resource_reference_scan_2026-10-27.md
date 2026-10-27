# Inventaris referensi RNG lintas resource — 27 Oktober 2026

## Status saat ini

**SELESAI untuk pemindaian byte mentah pada berkas yang diidentifikasi; validasi caller resource memakai disassembly Ghidra masih berjalan.** Jangan samakan hit pola instruksi dengan caller yang sudah terbukti sebelum hasil Ghidra ditambahkan.

Sumber: GitHub Actions [#40454059515](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40454059515), artefak teks step4-rng-resource-reference-scan #12711178537. Workflow melaporkan:
- emulator_or_gameplay_executed=no
- binary_uploaded_as_artifact=no
- Semua file yang mempunyai checksum baseline lolos pemeriksaan ukuran dan SHA-256.

## Sasaran statis

| Simbol kerja | Alamat | Keyakinan |
|---|---:|---|
| Generator LCG | 0x80035D78 | **Pasti** — fungsi pada executable utama telah dikenali oleh Ghidra. |
| State LCG | 0x800A3118 | **Pasti** — rutin LCG membaca dan menulis alamat ini. |
| Kandidat seed setter | 0x80035DA8 | **Pasti untuk instruksi store argumen $a0; mungkin sebagai API seed setter** karena nama/sumber seed tidak tersedia. |

Rumus generator yang sudah ditelusuri:

~~~c
state = state * 0x41C64E6D + 0x3039; // modulo 2^32
return (state >> 16) & 0x7FFF;
~~~

## Hasil pemindaian identitas dan pola langsung

| Berkas | Identitas SHA-256 | Hit kata JAL mentah ke RNG | Hit kata JAL mentah ke seed setter |
|---|---|---:|---:|
| SLPS_035.53 | a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569 | 4 | 0 |
| DATA.BIN | 69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822 | 148 | 1 |
| DATA2.BIN | be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9 | 0 | 0 |
| DUMMY.BIN | cac5c852e95c90475a2879f51b6b949afea2df0cb540b2a2743bd791af4c47a2 | 0 | 0 |
| XASECT.BIN | df257fbdabdb848f845466246abf4a36fdb6cf17815fc3a76ff7d7585d1953f0 | 0 | 0 |

Pemeriksaan SHA-256 sistematis pada kelima berkas yang discan berhasil. Direktori DATA.BIN tervalidasi sebagai 1.500 rentang aktif yang dipakai untuk mengaitkan hit mentah dengan indeks resource.

### Empat caller pada executable utama — pasti

Offset file SLPS_035.53 diterjemahkan ke alamat muat dari header (0x80010000 + file_offset - 0x800). Hasil cocok dengan caller Ghidra yang sudah ada:

| Offset file | Call site | Fungsi pemanggil | Bukti tingkat fungsi |
|---:|---:|---|---|
| 0x6314 | 0x80015B14 | FUN_80015adc | Ghidra, 160 byte |
| 0x63F0 | 0x80015BF0 | FUN_80015b7c | Ghidra, 240 byte |
| 0xAC60 | 0x8001A460 | FUN_8001a328 | Ghidra, 376 byte |
| 0x11424 | 0x80020C24 | FUN_80020bf4 | Ghidra, 156 byte |

### Kandidat caller di DATA.BIN — belum boleh dinaikkan ke VERIFIED

Pola JAL yang tepat muncul 148 kali pada DATA.BIN: empat berada di resource entry 0 dan 144 di entry 1. Hit ini sangat kuat sebagai **kandidat** karena bentuk katanya cocok dengan target, tetapi rentang muat resource masih hipotesis dan sebagian byte/resource mungkin data. Alamat RAM di bawah merupakan hasil base hipotetis, bukan alamat runtime terverifikasi.

**Entry 0** (offset file resource entry 0; base hipotetis 0x800AD000):

| Offset di entry | Call-site RAM hipotetis | Status |
|---:|---:|---|
| 0xE2D8 | 0x800BB2D8 | Kandidat JAL RNG; tunggu validasi Ghidra |
| 0xE2FC | 0x800BB2FC | Kandidat JAL RNG; tunggu validasi Ghidra |
| 0xE748 | 0x800BB748 | Kandidat JAL RNG; tunggu validasi Ghidra |
| 0xE770 | 0x800BB770 | Kandidat JAL RNG; tunggu validasi Ghidra |

Satu kata JAL mentah menuju kandidat seed setter berada di entry 0 pada offset 0x22AC, setara alamat **hipotetis** 0x800AF2AC. Ini penting untuk memeriksa seed, tetapi **belum membuktikan** bahwa instruksi tersebut berada di jalur kode yang dieksekusi ataupun nilai $a0 yang diberikan.

**Entry 1** (base hipotetis 0x800D0000): 144 kandidat JAL RNG. Call-site RAM hipotetis pertama 0x800E0498 (offset entry 0x10498); yang terakhir 0x801565B8 (offset entry 0x865B8). Daftar offset mentah selengkapnya berada pada artefak run #40454059515; laporan ini akan diperbarui dengan daftar call-site dan fungsi setelah pemeriksaan Ghidra selesai.

### Referensi state

Pencarian pola LUI + akses memori ke state menemukan tiga kandidat hanya dalam executable utama, sesuai bentuk baca/tulis pada LCG dan store pada kandidat setter. Tidak ada kata alamat state atau pola pembentukan alamat LCG/seed setter yang ditemukan dengan scan sempit ini pada resource lain. Ini **tidak** menyingkirkan penggunaan pointer yang dihitung, pointer tabel, kompresi/dekompresi saat load, atau encoding lain.

## Batas bukti

- Hit kata JAL mentah bukan otomatis xref yang disahkan oleh disassembler.
- Base 0x800AD000 untuk entry 0 dan 0x800D0000 untuk entry 1 tetap **HIPOTESIS** runtime.
- Hasil nol di DATA2.BIN/DUMMY.BIN hanya berlaku bagi pola byte MIPS/alamat sempit pada isi mentah tersebut; tidak membuktikan tidak ada kode setelah dekompresi/dekripsi.
- Belum diketahui siapa yang menetapkan seed runtime, kapan seed diatur, dan apa konteks gameplay caller-caller resource.
- Tidak ada emulator, gameplay, input, atau savestate yang dijalankan/dipulihkan.

## Pekerjaan validasi berikutnya untuk Langkah 4

1. Gunakan Ghidra pada entry 0 dan entry 1 dengan base yang ditandai hipotesis untuk memeriksa target flow nyata dari semua kandidat JAL.
2. Prioritaskan kandidat 0x800AF2AC untuk menemukan argumen $a0 yang dikirim ke 0x80035DA8 dan apakah ia benar-benar instruksi kode.
3. Laporkan semua call-site yang dikonfirmasi beserta fungsi pemanggil; pisahkan raw hit, verified direct call, dan unresolved indirect/compressed paths.


## Pembaruan — hasil Ghidra untuk entry 1

Run [#40454881770](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40454881770) berhasil: 144 kandidat JAL mentah → 108 direct-flow terdekode Ghidra, 50 fungsi pemanggil dikenali, 1 call site tanpa batas fungsi, 36 kandidat mentah tetap tidak terdekode. Lihat [inventaris lengkap entry 1](rng_resource_entry1_ghidra_callers_2026-10-27.md).

Run konteks entry 0 [#40455197588](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455197588) mengonfirmasi pada base hipotesis: `0x800AF2AC → 0x80035DA8` dengan `$a0=-1), dan `0x800BB2D8 → 0x80035D78`. Kandidat di `0x800BB2FC`, `0x800BB748`, `0x800BB770` masih perlu diperiksa lebih lanjut.

## Koreksi hasil Langkah 4 — 27 Oktober 2026

Run Ghidra entry 1 [#40455582988](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455582988) mendekode 36/36 kandidat yang sebelumnya belum terdekode; kini seluruh 144 lokasi entry 1 terbaca sebagai JAL langsung ke RNG pada base kandidat. Fungsi caller untuk 36 itu belum dipetakan. [Daftar 36 call site dan konteks](rng_resource_entry1_unmapped_context_2026-10-27.md).

Konteks entry 0 [#40455557190](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455557190): empat instruksi JAL RNG terdekode; tiga punya branch masuk lokal, `0x800BB748` reachability belum terbukti. Direct call seed setter `0x800AF2AC → 0x80035DA8` memasukkan `$a0=-1`; state menjadi `0xFFFFFFFF` jika jalur dijalankan. [Laporan entry 0](rng_resource_entry0_ghidra_context_2026-10-27.md).

Status diperbarui: direct-JAL inventory statis pada main EXE + DATA.BIN entry0/entry1 selesai dengan base resource bersifat hipotesis. Indirect/pointer callers, kode terkompresi/hasil dekompresi, runtime loading, caller boundary entry1 yang belum dikenal, dan satu reachability entry0 tetap UNKNOWN.


## Scan signature RNG/LGC tambahan

Run [#40455975609](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455975609) memeriksa kandidat konstruksi LCG `0x41C64E6D` dan MULT/MULTU pada raw lima file disc. Satu hit ada di main EXE pada `0x80035D78); tidak ada kandidat materialisasi yang sama pada DATA.BIN, DATA2.BIN, DUMMY.BIN, atau XASECT.BIN. Immediate `0x3039` ditemukan 29 kali pada DATA.BIN dan 2 kali di DATA2.BIN, tetapi tanpa signature pengali itu tidak boleh dinamai RNG. Laporan: [out/step4_rng_signature_scan_2026-10-27.md](step4_rng_signature_scan_2026-10-27.md).
