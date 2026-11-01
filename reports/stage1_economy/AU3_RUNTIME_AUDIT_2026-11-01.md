# AU3 — runtime interpreter setter/helper trace (1 November 2026)

## Hasil dan identitas run

<badge>TUNTAS</badge> **K5 terbatas** — dua peluncuran independen per jadwal, seluruh empat peluncuran berhasil.

- Run Actions: **41274625876**
- Job: **124754181385** — `AU3 four-launch A/C interpreter setter/helper trace`
- Status: `success`
- Source SHA yang dijalankan: `214d6641b67b035300d7d8efbd117318d7a3f81b`
- Kode keluar job/script/emulator: desimal **0**
- H6 SHA-256: `d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475`
- **H6 HIBRIDA**: checkpoint target sebagai dasar + top-level protobuf SPU field 6 dari CONTROL; bukan checkpoint target murni.
- Emulator PCSX-Redux headless, mode `-debugger -interpreter`, tanpa dynarec.

## Desain eksperimen yang dijalankan

Dua jadwal, dua peluncuran terpisah per jadwal:

- **C**: tidak ada input.
- **A**: CIRCLE ditekan pada post-load GPU::Vsync frame 60 dan dilepas pada frame 61; pembacaan input kembali PASS di kedua peluncuran A.

Breakpoint yang dipasang **hanya**:
- Setter `0x8001387C`
- Helper `0x800B770C`

Getter `0x800138EC` tidak dipasang. Kedua breakpoint aktif sesegera listener `ExecutionFlow::SaveStateLoaded` dipanggil, sebelum frame post-load pertama, sampai frame 600. Setiap hit (bila ada) direkam dengan frame, PC, a0, a1, ra, v0.

Snapshot SHA-256 diambil dari **2 MiB pertama RAM** pada frame 180, 360, dan 600. Segmen RAM yang diekstrak berukuran 8,388,608 byte; hash dihitung pada 2 MiB pertama saja.

Timeout setiap launch 1800 detik. Waktu launch terlama 241.088 detik; batas timeout adalah 7.46 kali waktu terlama dan dengan demikian melampaui persyaratan >=2x.

## Hasil tiap peluncuran

| Jadwal | Launch | Breakpoint terpasang | Input CIRCLE | Exit emulator desimal | Exit wrapper desimal | Wall time (s) | Memory Card berubah? |
|---|---:|---|---|---:|---:|---:|---|
| C | 1 | Ya, setter+helper | Tidak berlaku | 0 | 0 | 241.088 | Tidak |
| C | 2 | Ya, setter+helper | Tidak berlaku | 0 | 0 | 240.482 | Tidak |
| A | 1 | Ya, setter+helper | Press PASS; release PASS | 0 | 0 | 240.669 | Tidak |
| A | 2 | Ya, setter+helper | Press PASS; release PASS | 0 | 0 | 240.903 | Tidak |

Memory Card disalin terpisah untuk setiap launch. Pada setiap salinan SHA-256 sebelum dan sesudah launch tetap:

`ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.

## Snapshot RAM

Semua 12 capture berstatus PASS. Dua launch dari jadwal yang sama menghasilkan hash identik pada masing-masing frame; jadwal A berbeda dari C pada semua frame yang dibandingkan.

| Frame | C, launch 1 dan 2 | A, launch 1 dan 2 | A berbeda dari C |
|---:|---|---|---|
| 180 | `5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7` | `0251aeef113a4c1eb58533a7dc5af85488e9bc2d96f42e24f62f8806ab0b6be8` | Ya |
| 360 | `4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907` | `2c53c4a225acccda78ebf67cb39e4922b0ee73d8c2da44928957df36792cc780` | Ya |
| 600 | `01dd595f641a3ceb0420655b84d5c4bcb161d466f8a2532e56d7a600f593471a` | `1164f1e27e9a1257fbf910047126de0e7baabbbd306940978af25ad326463aa2` | Ya |

Kesamaan hash antar-dua launch per jadwal adalah reproduksibilitas snapshot pada titik tersebut. Perbedaan A dan C membuktikan snapshot agregat RAM berbeda pada frame sampel. Hash tidak menentukan alamat/field mana yang berubah, alasan perubahan, ataupun makna gameplay/ekonomi.

## Hit breakpoint

| Jadwal | Setter 0x8001387C | Helper 0x800B770C |
|---|---:|---:|
| C (2 launch) | 0 | 0 |
| A (2 launch) | 0 | 0 |

`AU3_BREAKPOINT_EVENTS.tsv` hanya memuat baris header; tidak ada hit yang terekam. File `AU3_HIT_COUNTS.tsv` mencatat nol pada keempat kombinasi jadwal/target. Kedua breakpoint dilaporkan terpasang pada semua launch.

**Batas interpretasi penting:** nol hit hanya berarti breakpoint pada alamat tersebut tidak terpicu selama window post-load frame 1–600 pada eksperimen H6 HIBRIDA, mode interpreter, jadwal A/C ini. Ini **bukan** bukti bahwa setter/helper tidak pernah dijalankan pada frame lain, state lain, mode dynarec, atau gameplay target-pure. Tidak ada hit event yang perlu diberi tuple register; format event disiapkan dan file kosong karena zero observation.

## Kesimpulan

**AU3 TUNTAS — K5 terbatas** pada matriks kondisi berikut: H6 HIBRIDA, PCSX-Redux headless interpreter, tanpa input atau CIRCLE frame 60–61, dua peluncuran per kondisi, breakpoint setter/helper saja, window frame 1–600, dan snapshot frame 180/360/600.

Semua kondisi operasional dan pengamanan terpenuhi: 4/4 exit code 0, 12/12 snapshot PASS, 4/4 pemasangan breakpoint PASS, 2/2 pasangan readback input A PASS, 4/4 Memory Card tidak berubah, dan timeout lebih dari 2x wall time terlama.

**TIDAK TAHU:** apakah setter/helper digunakan di luar window dan kondisi yang diuji; field mana yang menjelaskan perbedaan hash A/C; makna ekonomi/gameplay dari data RAM. Tidak ada interpretasi ekonomi dibuat tanpa bukti instruksi.

## Berkas bukti dan ringkasan Actions

Semua artefak berikut teks/TSV; tidak ada binary savestate, dump RAM, BIOS, ISO, screenshot, atau frame yang dipublikasikan:

- `reports/stage1_economy/au3-setter-helper-run-41274625876/attempt-1/ACTIONS_RUN_SUMMARY.txt`
- `AU3_SUMMARY.txt`
- `AU3_LAUNCHES.tsv`
- `AU3_FRAMES.tsv`
- `AU3_BREAKPOINT_EVENTS.tsv`
- `AU3_HIT_COUNTS.tsv`
- `AU3_SCRIPT_EXIT_CODE.txt`
- `ACTIONS_RUN_STATUS.txt` (final status PASS)

Actions ringkasan: `STATUS=PASS`, job `au3-setter-helper-interpreter`, job ID `124754181385`, run ID `41274625876`, source SHA `214d6641b67b035300d7d8efbd117318d7a3f81b`, exit code `0`.
