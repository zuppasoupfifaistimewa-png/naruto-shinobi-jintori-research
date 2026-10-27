# Langkah 6 — audit def-use CFG/SSA untuk field candidate DATA.BIN entry 1

Tanggal: 27 Oktober 2026, 21:41 WIB  
Status: **SEBAGIAN; alias/pointer closure belum tercapai.**

## Sumber dan reproduksi

- Repositori: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`, branch `main`.
- Script: [`tools/step6/ExportFieldCfgDefUse.java`](../tools/step6/ExportFieldCfgDefUse.java); workflow: [`.github/workflows/step6-resource-field-scan.yml`](../.github/workflows/step6-resource-field-scan.yml).
- Run [#40522772847](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40522772847) completed/success pada 21:38:32 WIB.
- Artifact teks/log #12741234990, 234.210 byte, ZIP SHA-256 `7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9`. Cleanup private working files berhasil. Binary resource tidak di-upload.
- Entry 1: offset file `0x10BB000`, panjang 596.412 byte, SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`. Import base `0x800D0000` hanya asumsi analisis.

## Fungsi 0x8012C544 — operasi inisialisasi dan perhitungan

Ghidra memvalidasi entry `0x8012C544`, body 292 alamat dalam view hipotetis itu. Output mencatat 88 high-level P-code ops dan tujuh offset-constant matches. Instruksi MIPS dan dekompilasi mendukung urutan berikut:

1. Baca flag/counter pada `pointer_global + 0xA1C`; jalur inisialisasi berjalan ketika nilainya nol.
2. Bersihkan beberapa field, termasuk `+0xB48`, `+0xB2D`, `+0xB34`, `+0xB3C`, dan `+0xB44` pada jalur yang dilaporkan.
3. Panggil `0x80012AC0`; simpan nilai byte hasil ke `+0xB2E` lalu salin byte ke `+0xB2F`.
4. Simpan nilai `0x1E` ke `+0xB4A`.
5. Baca word `+0xB30` dan `+0xB38`, jumlahkan, simpan ke `+0xB40`.
6. Kosongkan `+0xB2A` dan set `+0xA1C = 1`.

Ini membuktikan urutan baca–jumlah–tulis dan pola init-guard statis. Ini **tidak** menetapkan nama semantik field atau makna angka `0x1E` bagi permainan.

## Fungsi 0x8012CACC — pembacaan +0xB44 pada jalur bercabang

Ghidra memvalidasi entry `0x8012CACC`, body 152 alamat; output mencatat 47 P-code ops dan dua offset-constant matches. P-code menunjukkan `CBRANCH` pada `0x8012CAF8`, merge `MULTIEQUAL` pada `0x8012CB20`, serta konstruksi effective address yang menambahkan `0xB44` ke pointer register di sekitar `0x8012CB14`. Def-use berhenti pada definisi indirect/address-tied di `0x8012CAD8`; asal nilai pointer di jalur sebelumnya belum terbukti. Karena itu, penulisan nol `+0xB44` pada fungsi pertama belum dapat dihubungkan secara lengkap dengan seluruh efek pembacaan/callee pada fungsi kedua.

## Apa yang ditambahkan oleh SSA

Berbeda dari pemindaian mundur linear sebelumnya, ekspor baru mencatat basic-block IDs, SSA varnodes, operation inputs/outputs, branches, loads/stores, dan `MULTIEQUAL`. Ini mengurangi ketidakpastian aliran lintas blok, tetapi trace dibatasi kedalaman empat dan beberapa definisi bersifat indirect. Ia tidak menyelesaikan aliasing pointer arbitrer, efek call lintas fungsi, relocations, atau nilai runtime dari global slot `0x8013A554`.

| Subkriteria Step 6 | Status | Dasar dan kekurangan |
|---|---|---|
| 6(a) akses field dan hubungan instruksi | **SEBAGIAN** | Read `+B30/+B38`, add, dan write `+B40` terbukti pada body statis. |
| 6(b) pointer provenance / alias lintas branch-callee | **BLOCKED** | SSA memetakan definisi/merge, tetapi nilai pointer global dan alias belum terpecahkan. |
| 6(c) XREF dan read/write lintas fungsi | **SEBAGIAN** | Ada inisialisasi `+B44` dan consumer di fungsi lain; full path ke efek akhir belum dihubungkan. |
| 6(d) semantik gameplay field | **UNKNOWN** | Tidak ada bukti independen untuk nama field atau hasil gameplay. |

## Batas penggunaan

Tidak ada sesi emulator/gameplay, input gameplay, ataupun restore savestate. Tidak ada binary resource privat di artifact. Base `0x800D0000` tetap **HIPOTESIS**, bukan alamat runtime terverifikasi. Status Step 6 tetap **SEBAGIAN**.
