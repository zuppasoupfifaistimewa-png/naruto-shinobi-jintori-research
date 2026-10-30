# AN1 — errata dokumen H6/CONTROL dan identitas Actions

Tanggal: 30 Oktober 2026  
Proyek: Naruto – Shinobi no Sato no Jintori Gassen (PS1), SLPS-03553  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

## (a) Koreksi jumlah byte H6 vs CONTROL

Hitungan sementara 3 byte diketahui + 56.974 byte TIDAK TAHU tidak berlaku setelah AM1 dan harus dianggap superseded. Perhitungan yang telah direkonsiliasi AM1 untuk kedua pasangan H6/CONTROL adalah:

| Perbandingan | Byte diketahui/berlabel | TIDAK TAHU | Total byte berbeda |
|---|---:|---:|---:|
| H6 attempt 1 vs CONTROL attempt 1 | 9 | 56.968 | 56.977 |
| H6 attempt 2 vs CONTROL attempt 2 | 9 | 56.968 | 56.977 |

Jadi angka yang benar adalah 3 → 9 untuk byte diketahui/berlabel, dan 56.974 → 56.968 untuk TIDAK TAHU. Istilah “byte diketahui tidak berubah” tidak tepat untuk jumlah delta ini: 9 berarti byte berbeda yang dapat dialokasikan ke label, bukan byte yang identik. Label yang mendasari angka tersebut: dua word Chakra masing-masing satu byte berubah, word RNG empat byte berubah, satu byte pertama blok 0x801CEF08 berubah, serta dua byte callback/tick-like 0x80066E7C berubah. Pointer slot 0x8013A554 dan Candidate-ID/Chakra P2/P3 tidak menyumbang byte delta pada perbandingan itu. Makna gameplay field tetap tidak ditetapkan.

Sumber pembanding: AM1 final report dan handoff AL1–AL4. AM1 adalah audit dokumen/label atas data runtime yang sudah ada; tidak meluncurkan emulator.

## (b) Koreksi identitas run Actions

| Peran | Nilai terverifikasi |
|---|---|
| Run gagal | 41048752354 |
| Job | am3-h6-circle-ab |
| ID job numerik | 124039280097 |
| Source SHA run | 240c448205b047f6dcbcb475c8f8b9cfca20c30a |
| Output commit ringkasan bot | 123654ee3a2159befb477980286d460313a61420 (123654e) |
| Hasil setup | HTTP 401, exit code 22; emulator launches 0 |
| Commit perbaikan workflow | 4fbbbdf278ca71e0c84cb651287096561e9b4878 |

Dengan demikian 123654e adalah output commit yang dibuat github-actions[bot] untuk run gagal, sedangkan 4fbbbdf memperbaiki workflow dan bukan output commit. Run sukses AM3 41048937290 tetap terpisah; tidak diulang pada AN1.

## Batas

H6 adalah hibrida: target savestate sebagai base dan SPU top-level field 6 dari CONTROL. Tidak boleh disebut target murni. AN1 tidak menjalankan emulator, tidak mengubah Release/visibilitas repo, dan tidak memasukkan ISO, BIOS, Memory Card, savestate, dump RAM, atau biner hybrid. Story Mode tetap tidak diklaim tamat.
