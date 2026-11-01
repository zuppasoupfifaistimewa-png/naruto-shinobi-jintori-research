# AX2 — tiga pemeriksaan acak langsung terhadap disassembly

Sumber instruksi: aq1-deep-context.tsv dari AQ1 run 41291576229. Pemeriksaan dilakukan terhadap baris INSN dan CALL_CONTEXT, bukan hanya menyalin ekspresi final AU2.

| PC setter | Instruksi mentah yang diperiksa | Hasil pencocokan |
|---|---|---|
| 0x800B41B0 | 0x800B4194 lw a0,0x598(a0); 0x800B419C sll v0,a0,3; 0x800B41A0 addu v0,v0,a0; 0x800B41A4 sll v0,v0,4; 0x800B41A8 addu a1,a1,v0; 0x800B41AC lw a1,0(a1); 0x800B41B0 jal 0x8001387C; delay 0x800B41B4 nop | COCOK. Indeks dikali 9 lalu 16 = stride 0x90; basis participant_base+4; load word menjadi a1. |
| 0x800DEB38 | 0x800DEB18 lw v1,-0x158C(s1) (slot 0x8013EA74); 0x800DEB1C lw a0,-0x14F4(s0); 0x800DEB24 sll v0,a0,3; 0x800DEB28 addu v0,v0,a0; 0x800DEB2C sll v0,v0,4; 0x800DEB30 addu v1,v1,v0; 0x800DEB34 lw a1,4(v1); 0x800DEB38 jal 0x8001387C; delay 0x800DEB3C nop | COCOK. Basis EA74, index dari s0-0x14F4, stride 0x90, field +0x04. |
| 0x8010A638 | 0x8010A600 j 0x8010A614; delay 0x8010A604 li s1,0x14; 0x8010A610 lw s1,0xB44(v0) dilewati; getter pada 0x8010A624; 0x8010A638 jal 0x8001387C; delay 0x8010A63C addu a1,v0,s1 | COCOK. Final a1=Q(i)+0x14, bukan Q(i)+B44. |

## Rekonsiliasi 14 baris terhadap AT1_SETTER_CALLS.tsv

- Jumlah PC sama: 14/14; tidak ada call-site hilang atau tambahan.
- Sepuluh participant call-site memakai slot pointer 0x8013EA74 (EA74) dan stride 0x90.
- Tujuh label census yang menyebut 0x8013EA84 berkonflik dengan rantai a1 akhir yang memakai EA74. Ini perbedaan label census, bukan perbedaan PC atau urutan instruksi.
- Empat manager call-site: 0x8010A15C memakai Q(i)+B44; 0x8010A1B0 dan 0x8010A97C memakai Q(i) langsung; 0x8010A638 memakai Q(i)+0x14 karena jump-delay-slot.
- Dibanding AU2_SETTER_ARGUMENTS, AX2 mempertahankan formula akhir dan menambah 12 instruksi pre-JAL, delay slot, basis pointer/slot, indeks, dan excerpt bytes. Tidak ada perbedaan jumlah PC. Koreksi interpretasi utama adalah branch-delay pada 0x8010A638 dan tidak menyebut manager+0xB44 pada dua setter yang menggunakan getter langsung.

Ketiga sampel di atas cocok dengan disassembly yang diekspor AQ1. Bukti statis maksimum K4; bukan validasi runtime atau semantik ekonomi.
