# DATA.BIN entry 1 — Ghidra validation caller RNG

Tanggal: 27 Oktober 2026  
Workflow: [Step 4 run #40454881770](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40454881770)  
Artefak teks asli: `step4-ghidra-rng-caller-validation` #12711758728. Biner tidak disertakan.

## Status dan hasil

- Resource yang dianalisis: DATA.BIN entry 1, 596.412 byte, SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`.
- Ghidra: 12.2, `MIPS:LE:32:default`; base impor `0x800D0000) adalah **hipotesis**, bukan hasil verifikasi loader runtime.
- 149.103 kata sejajar dipindai.
- **144** kata JAL mentah yang mengode target `0x80035D78).
- **108** dari kandidat itu ditemukan sebagai instruksi yang didekode Ghidra dan flow pemanggilannya cocok langsung ke `0x80035D78).
- **50** fungsi pemanggil memiliki batas fungsi yang dikenali Ghidra; **1** call site terkonfirmasi tidak terikat ke batas fungsi.
- **36** kandidat mentah tidak terdekode dalam analisis Ghidra saat ini. Statusnya UNKNOWN—bukan bukti bahwa byte tersebut pasti data dan bukan kode.
- Tidak ada panggilan langsung mentah ke kandidat seed setter `0x80035DA8) dalam entry 1.
- Analisis ini statis; tidak ada emulator, gameplay, input, atau savestate yang dijalankan.

**Keyakinan:** pasti bahwa 108 lokasi adalah direct-call flow yang didekode di program Ghidra pada base impor yang dipakai; mungkin bahwa base tersebut mencerminkan pemuatan runtime; belum diketahui apakah semua 36 kandidat yang belum terdekode merupakan caller kode.

## 50 fungsi dengan call site RNG terkonfirmasi

Alamat fungsi dan call site di bawah semuanya dalam address map hipotetis entry 1. Call site dikelompokkan berdasarkan fungsi pemanggil dari Ghidra. Ukuran adalah jumlah byte tubuh fungsi menurut indeks Ghidra; body bisa mengandung blok nonkontigu ketika kontrol alur buruk.

| Entry fungsi | Nama Ghidra | Ukuran body (byte) | Call site ke RNG |
|---:|---|---:|---|
| 0x800E03DC | FUN_800e03dc | 268 | 0x800E0498 |
| 0x800EA168 | FUN_800ea168 | 696 | 0x800EA20C |
| 0x800EA420 | FUN_800ea420 | 444 | 0x800EA4F8 |
| 0x800EAE74 | FUN_800eae74 | 1.580 | 0x800EB3C0 |
| 0x800EB4A0 | FUN_800eb4a0 | 456 | 0x800EB59C |
| 0x800EB6B8 | FUN_800eb6b8 | 2.356 | 0x800EB798, 0x800EB9C0, 0x800EBAD8, 0x800EBEF8 |
| 0x800EC2B8 | FUN_800ec2b8 | 532 | 0x800ECDC0 |
| 0x800EC3A0 | FUN_800ec3a0 | 1.364 | 0x800EC460, 0x800EC7F4 |
| 0x800ECEA0 | FUN_800ecea0 | 2.040 | 0x800ECEA8, 0x800ECF5C, 0x800ED398, 0x800ED454 |
| 0x800ED8C8 | FUN_800ed8c8 | 160 | 0x800ED8E4 |
| 0x800EE064 | FUN_800ee064 | 840 | 0x800EE260 |
| 0x800EF98C | FUN_800ef98c | 2.500 | 0x800EF9D0 |
| 0x800F11D8 | FUN_800f11d8 | 464 | 0x800F1290 |
| 0x800FA7D4 | FUN_800fa7d4 | 272 | 0x800FA800 |
| 0x8010C96C | FUN_8010c96c | 172 | 0x8010C710 |
| 0x8010F49C | FUN_8010f49c | 768 | 0x800ECC08 |
| 0x8010F6C8 | FUN_8010f6c8 | 100 | 0x8010F6C4 |
| 0x80110018 | FUN_80110018 | 612 | 0x80110078 |
| 0x80114618 | FUN_80114618 | 620 | 0x801147C0 |
| 0x801149A8 | FUN_801149a8 | 348 | 0x801149EC, 0x80114A44 |
| 0x80116648 | FUN_80116648 | 184 | 0x80116688 |
| 0x8011C268 | FUN_8011c268 | 1.840 | 0x8011C424, 0x8011C42C, 0x8011C480, 0x8011C4D0, 0x8011C530, 0x8011C580, 0x8011C5E4, 0x8011C638 |
| 0x8011C680 | FUN_8011c680 | 456 | 0x8011C6D8, 0x8011C724, 0x8011C77C |
| 0x80123B70 | FUN_80123b70 | 220 | 0x80123B94 |
| 0x8012940C | FUN_8012940c | 44 | 0x8012942C |
| 0x8012D9C0 | FUN_8012d9c0 | 536 | 0x8012DAE4 |
| 0x8012DC34 | FUN_8012dc34 | 916 | 0x8012DC98 |
| 0x8012ED70 | FUN_8012ed70 | 260 | 0x8012EDBC, 0x8012EDF8 |
| 0x8012F1C4 | FUN_8012f1c4 | 312 | 0x8012F23C |
| 0x80132CC0 | FUN_80132cc0 | 80 | 0x80132CCC |
| 0x80135470 | FUN_80135470 | 180 | 0x801354A4, 0x801354D0, 0x801354F8 |
| 0x80135554 | FUN_80135554 | 228 | 0x80135588, 0x801355B4, 0x801355DC |
| 0x80135638 | FUN_80135638 | 228 | 0x8013566C, 0x80135698, 0x801356C0 |
| 0x8013571C | FUN_8013571c | 224 | 0x80135750, 0x8013577C, 0x801357A4 |
| 0x8013E250 | FUN_8013e250 | 264 | 0x8013E2E4 |
| 0x8013E37C | FUN_8013e37c | 912 | 0x8013E3A4, 0x8013E414, 0x8013E444, 0x8013E490, 0x8013E5D8, 0x8013E61C |
| 0x80140C54 | FUN_80140c54 | 364 | 0x80140D58, 0x80140D84 |
| 0x8014154C | FUN_8014154c | 472 | 0x80141608, 0x8014161C, 0x8014164C |
| 0x80141724 | FUN_80141724 | 652 | 0x80141848 |
| 0x80141AC0 | FUN_80141ac0 | 352 | 0x80141BA4, 0x80141BAC |
| 0x80141EAC | FUN_80141eac | 476 | 0x80142024 |
| 0x80142508 | FUN_80142508 | 632 | 0x8014263C |
| 0x801493FC | FUN_801493fc | 688 | 0x80149460, 0x801494AC, 0x80149548, 0x80149594, 0x80149648 |
| 0x801496AC | FUN_801496ac | 364 | 0x80149708, 0x80149728, 0x80149744 |
| 0x8014CCB4 | FUN_8014ccb4 | 2.492 | 0x8014D0B8, 0x8014D120, 0x8014D150, 0x8014D164, 0x8014D1B8, 0x8014D210, 0x8014D2B4, 0x8014D318, 0x8014D374, 0x8014D444, 0x8014D494 |
| 0x8014E908 | FUN_8014e908 | 600 | 0x8014EAB0, 0x8014EAEC |
| 0x8014EFAC | FUN_8014efac | 912 | 0x8014F2A4 |
| 0x80154128 | FUN_80154128 | 452 | 0x8015422C |
| 0x801554F0 | FUN_801554f0 | 608 | 0x801555E4, 0x80155618, 0x80155688, 0x801556B0 |
| 0x80155C30 | FUN_80155c30 | 544 | 0x80155CFC, 0x80155D6C, 0x80155DDC |

Satu call site langsung yang terdekode tetapi tidak memiliki batas fungsi pada pass ini: **0x80128AF8** (target 0x80035D78).

## 36 kandidat mentah yang belum didekode

Alamat berikut cocok dengan kata JAL target RNG tetapi Ghidra tidak mendekodenya sebagai instruksi dalam pass saat ini. Jangan klasifikasikan sebagai caller terverifikasi maupun sebagai data sampai dianalisis dengan konteks code/data yang lebih kuat:

`0x800E7008`, `0x800EC004`, `0x800EC0C8`, `0x800ED1E0`, `0x800FA278`, `0x80129404`, `0x80132C88`, `0x8013332C`, `0x80133370`, `0x801334A4`, `0x801334E8`, `0x8013D548`, `0x8013D580`, `0x8013D5B8`, `0x8013D5DC`, `0x801454EC`, `0x8014A2F0`, `0x8014A570`, `0x8014DD68`, `0x8014DDC8`, `0x8014DE28`, `0x8014DE88`, `0x8014DEE8`, `0x8014DF48`, `0x8014E0D4`, `0x801558FC`, `0x8015592C`, `0x80155974`, `0x801559B0`, `0x801559CC`, `0x801559E8`, `0x80155A04`, `0x80155AB4`, `0x80156478`, `0x8015657C`, `0x801565B8`.

## Apa yang boleh disimpulkan

- **Pasti secara statis, bersyarat pada base impor:** 108 direct-call flow di entry 1 menuju alamat 0x80035D78 di address map Ghidra.
- **Pasti pada analisis ini:** 50 batas fungsi unik berisi call site langsung tersebut; nama FUN adalah label auto Ghidra, bukan nama gameplay.
- **Mungkin:** resource entry 1 merupakan kode overlay/resource dengan banyak pemanggil RNG. Base RAM sebenarnya belum dibuktikan oleh loader.
- **Belum diketahui:** apakah semua 36 raw-only candidate adalah code call, fungsi gameplay dari setiap caller, dan bagaimana entry ini dimuat pada runtime.
- Beberapa dekompilasi sampel memberi peringatan control-flow/bad-instruction. Karena itu laporan ini tidak memberi label roulette/battle/AI/turn pada fungsi berdasarkan nama atau dekompilasi cacat.

## Langkah 4 berikutnya

Periksa entry 0 secara lokal di sekitar empat kandidat RNG dan satu kandidat seed setter memakai disassembly terbatas tanpa whole-program auto-analysis. Prioritas: call site hipotetis 0x800AF2AC ke 0x80035DA8 untuk mencari nilai/asal argumen $a0. Tetap UNKNOWN sampai alur instruksi dan konteksnya benar-benar mendukung interpretasi seed.
