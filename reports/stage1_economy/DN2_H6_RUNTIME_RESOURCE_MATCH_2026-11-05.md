# DN2 — silang runtime H6 dengan resource DK1

Status: **TUNTAS — K5 untuk keterulangan runtime H6 hybrid**. Ini bukan K5 untuk checkpoint target murni.

Run yang digunakan adalah run BA3 yang sudah tersedia: dua peluncuran terpisah, tanpa input gameplay, tanpa RAM poke, dengan snapshot frame 180 dan 360. Karena workflow telah sukses dan menyimpan seluruh snapshot yang dibutuhkan, tidak dijalankan Actions runtime baru.

## Hasil pembacaan

- `u32[0x80070734]` = 0; `u8[0x8007073C]` = 0; `u8[0x80070CD0]` = 0 pada keempat snapshot.
- Selector 0 memilih resource `0x276` (resource ID 630).
- Slot `0x8013EA84` berisi pointer `0x8013B818`; count dari `0x8013EAC8` adalah 22 dan stride `0x124`.
- Resource DK1 `0x276` berisi tepat 22 record. Kelima halfword live `+0x10..+0x18` dibandingkan dengan kolom loader-mapped LV1–LV5.

Hasil: **88/88 record-snapshot cocok pada seluruh 5 field** (440/440 nilai skalar), yaitu 22/22 pada masing-masing snapshot: launch 1/frame 180, launch 1/frame 360, launch 2/frame 180, dan launch 2/frame 360.

## Integritas runtime

Per launch timeout 900 detik; durasi teramati 145.836 s dan 144.682 s. Wrapper dan emulator masing-masing keluar dengan kode 0 pada kedua launch. Tidak ada timeout.

RAM 2 MiB SHA-256 frame 180 adalah `5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7` pada kedua launch; frame 360 `4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907` pada kedua launch. Keduanya sama dengan nilai referensi RAM180/RAM360 di CG3.

Memory Card SHA-256 sebelum dan sesudah kedua launch tetap `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.

## Batas interpretasi

Ini membuktikan kesesuaian tabel LV resource `0x276` dengan live tile table pada empat snapshot H6 ini. Tidak membuktikan selector/resource mana yang dipakai di seluruh mode permainan atau bahwa angka LV adalah formula yang dihitung saat runtime. H6 adalah gabungan target checkpoint dengan field SPU dari control, bukan target murni.

Berkas derivasi TSV berisi seluruh 88 perbandingan record.
