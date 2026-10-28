# Step 6(b) — audit XREF slot pointer kandidat 0x8013A554

Tanggal: 28 Oktober 2026  
Run: [#40611660635](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40611660635)  
Artifact: [#12783307599 — step6-resource-field-static-scan](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40611660635/artifacts/12783307599)  
Commit kode analyzer: [ea148ca60af2e3eeaa1b58141532e1ff5a98dd60](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/ea148ca60af2e3eeaa1b58141532e1ff5a98dd60)

## Hasil eksekusi dan identitas

Run selesai **completed/success** pada `2026-10-28T00:55:13Z` (07:55:13 WIB). Job menjalankan analisis Ghidra, menghapus working files privat, memvalidasi teks, dan mengunggah laporan teks; seluruh langkah tersebut PASS. Tidak ada emulator/gameplay, input, atau savestate restore. Tidak ada aset privat diunggah: `private_binary_uploaded=no`; `source_assets_removed_before_ghidra=PASS`.

ZIP artefak berukuran 244.577 byte; SHA-256 dihitung ulang = `748eadbfe82980bba8d2088d11affba4310d524eb871b6a34ee5fd43584f2892`, cocok dengan digest artifact. Identitas entry-1 sesuai dengan artefak sebelumnya: DATA.BIN 66.015.232 byte, SHA-256 `69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822`; entry-1 offset `0x10BB000`, ukuran 596.412 byte, SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`.

## Bukti primer yang diekspor

Analyzer membaca program Ghidra dengan base hipotetis entry-1 `0x800D0000`, mendekode 98.357 instruksi dalam view itu, lalu memeriksa exact reference manager dan pola raw MIPS berbatas untuk target numerik `0x8013A554`.

| Observasi | Hasil | Batas |
|---|---:|---|
| Exact reference manager | 194 XREF | XREF pada address-space view hipotetis; belum bukti runtime |
| Tipe XREF | 192 READ, 2 WRITE | Tidak memverifikasi bahwa bytes di alamat tersebut merupakan pointer/object slot |
| Fungsi yang teridentifikasi | 74 entry fungsi unik; 6 XREF tidak punya containing function | Boundary dan decoding perlu tetap diperiksa |
| Instruksi load/store dengan displacement `0xA554` | 200 kandidat | Pencocokan displacement saja tidak membuktikan base register aktual |
| Kandidat yang memiliki `lui reg,0x8014` sebelumnya pada register base sama, dalam 24 record instruksi | 159 | Heuristik lokal; tidak menyelesaikan dominance, semua path CFG, liveness, alias atau relocation |
| Static bytes di alamat `0x8013A554` | `70 00 B0 AF`, little-endian word `0xAFB00070` | Byte file-view saja, bukan nilai pointer runtime |

Dua store yang ditemukan oleh XREF:
- `0x80127278`, fungsi `0x80127240`: `_sw v0,-0x5aac(s0)`.
- `0x80127364`, fungsi `0x8012733c`: `sw zero,-0x5aac(s0)`.

Contoh pembacaan untuk fungsi yang telah diaudit sebelumnya termasuk `lw v0,-0x5aac(s0)` di `0x8012C554), dan sejumlah akses terkait dalam rentang `0x8012C544`, `0x8012C680`, `0x8012C78C`, `0x8012C934`, serta `0x8012CACC`. Output lengkap alamat, tipe XREF, nama fungsi dan konteks instruksi ada pada file `field-cfg-defuse.txt` di artifact #12783307599.

## Konflik pemetaan yang mencegah closure

Pada kandidat base `0x800D0000`, alamat `0x8013A554` berada di dalam rentang program view entry-1. Empat byte di sana adalah `70 00 B0 AF`, yang terdekode sebagai bentuk instruksi MIPS `sw s0,0x70(sp)` jika dibaca dalam endian dan ISA yang digunakan oleh scan. Nilai word `0xAFB00070` bukan pointer object yang telah dibuktikan. Karena itu ada konflik **code/data mapping atau base/runtime relocation yang belum terselesaikan**: Ghidra melihat banyak instruksi yang mengakses alamat numerik itu seperti suatu global, sementara bytes pada alamat tersebut dalam image view tampak seperti kode instruksi. Ini tidak membuktikan secara mandiri bahwa runtime menulis ke kode; justru base/segmen/runtime mapping tetap perlu dikonfirmasi.

`exact_reference_manager_count=194` adalah fakta tentang XREF statis pada listing tersebut; bukan 194 akses runtime yang teramati. Pola 200/159 juga heuristik terbatas, tidak termasuk semua computed address, alias melalui register, alternate base, split-immediate sequence, code yang tidak terdekode, atau kode/resource yang dimuat-relokasi saat runtime.

## Status setelah hasil

**6(a) SEBAGIAN; 6(b) BLOCKED; 6(c) SEBAGIAN; 6(d) UNKNOWN.** Daftar XREF dan dua store merupakan bukti tambahan untuk pencarian lokal, tetapi tidak menghubungkan nilai pointer dari asal ke consumer runtime, tidak menyelesaikan base/alias chain, dan tidak memberi semantik gameplay kepada `+0xB30/+0xB38/+0xB40/+0xB44`.

Langkah minimum berikut bukan mengulang scan identik: pastikan peta loader/overlay dan segment layout dari kode loader/relocation terlebih dahulu, lalu resolusikan arti `0x8013A554` di map runtime yang valid. Setelah mapping terverifikasi, baru telusuri value provenance dan effects lintas fungsi. Tidak ada dasar untuk mempromosikan biaya Chakra, barrier/level-up, giliran, atau field game lainnya.

Story Mode tetap **TIDAK TERBUKTI TAMAT**. Pemain adaptif tidak dijalankan atau diubah.
