# AZ2–AZ3 — audit statis manager dan setter biaya
Tanggal: 2 November 2026
Target: SLPS-03553 / DATA.BIN Entry 1
Bukti: disassembly dan byte instruction statis; maksimum K4. Bukan hasil gameplay.
Batas input: Entry 1 596,412 byte, file offset 0x10BB000, SHA-256 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a. Import base 0x800AD450 adalah kandidat statis, bukan pemetaan runtime tervalidasi.

## AZ2 — pembaca manager +0xB38 / +0xB40 / +0xB44

### Pembaca yang tampak pada function body yang diekspor

| Field | PC | Fungsi | Instruksi | Makna alur yang langsung terlihat |
|---|---:|---|---|---|
| +0xB38 | 0x80109A88 | FUN_80109994 | lw v1,0xB38(a0) | dipasangkan dengan B30; hasil penjumlahan ditulis ke B40 pada 0x80109A94 |
| +0xB38 | 0x8010A0E0 | FUN_80109FEC | lw v1,0xB38(v0) | disalin ke progress B3C pada 0x8010A0E8 |
| +0xB38 | 0x8010A4D8 | FUN_80109FEC | lw v1,0xB38(v1) | target pembanding progress B3C pada state 5 |
| +0xB38 | 0x8010A4F8 | FUN_80109FEC | lw v1,0xB38(v0) | nilai target disalin ke B3C saat terminal state 5 |
| +0xB40 | 0x8010A0EC | FUN_80109FEC | lw v1,0xB40(v0) | disalin ke B44 saat input flag 0x20 dan manager state 3–6 |
| +0xB40 | 0x8010A5A0 | FUN_80109FEC | lw v1,0xB40(v1) | target pembanding progress B44 pada state 6 |
| +0xB40 | 0x8010A5C0 | FUN_80109FEC | lw v1,0xB40(v0) | nilai target disalin ke B44 ketika state 6 mencapai terminal |
| +0xB44 | 0x80109F64 | FUN_80109F1C | lw a2,0xB44(v1) | B44 diteruskan sebagai a2 ke 0x8001B364 bersama pointer buffer; label teksnya TIDAK TAHU |
| +0xB44 | 0x8010A154 | FUN_80109FEC | lw a1,0xB44(v1) | addend untuk setter pada 0x8010A15C: a1=Q(i)+B44 |
| +0xB44 | 0x8010A524 | FUN_80109FEC | lw v0,0xB44(v1) | dibandingkan dengan B40 dalam state 6 |
| +0xB44 | 0x8010A590 | FUN_80109FEC | lw v0,0xB44(v1) | progress lama sebelum +0x14 |
| +0xB44 | 0x8010A5EC | FUN_80109FEC | lw v0,0xB44(v0) | input untuk clamp 0x15 |
| +0xB44 | 0x8010A610 | FUN_80109FEC | lw s1,0xB44(v0) | dipakai hanya pada cabang B44<21; cabang lain menetapkan s1=0x14 |
| +0xB44 | 0x8010A648 | FUN_80109FEC | lw v0,0xB44(v1) | nilai sebelum dikurangi s1 pada jalur setter |
| +0xB44 | 0x8010A6A8 | FUN_80109FEC | lw v0,0xB44(v1) | tes terminal B44!=0 sebelum state berubah ke 8 |

Census AW1 yang tersedia menghitung 14 akses displacement +0xB44 dalam tiga fungsi: FUN_80109994 (store/init pada delay slot), FUN_80109F1C (satu reader), FUN_80109FEC (reader dan writer). Daftar akses lengkap yang diekspor ada di aq1-run-41319511985/attempt-1/aw1-manager-b44-accesses.tsv. Untuk +0xB38 dan +0xB40, tabel di atas merangkum semua load yang tampak pada tiga function body terpilih, tetapi **census whole-module bagi dua displacement itu belum tersedia: TIDAK TAHU apakah ada reader lain di luar ekspor ini**. Nol temuan di luar ekspor tidak dipakai sebagai kesimpulan.

### Semua jalur setter yang berhubungan langsung dengan getter dalam FUN_80109FEC

| Setter PC | 12 instruksi sebelum JAL (ringkas) | Delay slot / ekspresi final a1 | Status |
|---|---|---|---|
| 0x8010A15C | A130 lbu state B2A; A134 li 7; A138 bne; A140 lbu index i; A144 jal getter; A14C load manager; A154 lw B44; A158 lbu i | A160 addu a1,v0,a1 → **a1=Q(i)+B44** | K4 |
| 0x8010A1B0 | A180 load manager; A188 lbu i; A18C jal 0x800171A4; A194 move s0,v0; A198 load manager; A1A0 lbu i; A1A4 jal getter; A1AC move a0,s0 | A1B4 move a1,v0 → **a1=Q(i)** | K4 |
| 0x8010A638 | A608/A610 branch computes s1; A618 load manager; A620 lbu i; A624 jal getter; A62C load manager; A634 lbu i | A63C addu a1,v0,s1 → **a1=Q(i)+min(B44,0x14)**; jump-delay A604 li s1,0x14 is active when B44>=21 | K4 |
| 0x8010A97C | A94C load manager; A954 lbu i; A958 jal 0x800171A4; A960 move s0,v0; A964 load manager; A96C lbu i; A970 jal getter; A978 move a0,s0 | A980 move a1,v0 → **a1=Q(i)** | K4 |

Q(i) means getter 0x800138EC using index i=ZEXT8[manager+0xB2B], returning participant record +0x18. Setter 0x8001387C writes that field. The call-site values above are additions or direct copies, not getter-minus-cost.

### Pemicu transfer/kredit menurut instruksi

FUN_80109FEC first tests caller flag: lw v0,0xC(s2); andi v0,v0,0x20 at 0x8010A078–0x8010A080. If the bit is clear, control branches to 0x8010A204 and skips the staged manager logic. If set, it reads manager state +0xB2A. States 3–6 stage B30/B38/B40 into B34/B3C/B44. The state-7 path reads Q(i), passes Q(i)+B44 to setter at 0x8010A15C (and has a further direct-Q(i) setter path at 0x8010A1B0), then clears B44 at 0x8010A1C4. The separate switch-state-7 processing path at 0x8010A638 transfers Q(i)+min(B44,0x14) and subtracts the same amount from B44.

**Kesimpulan mekanis K4:** jalur pengiriman nilai ke participant +0x18 memerlukan bit 0x20 pada caller flag dan state manager 7; state 6 lebih dulu menyiapkan B44 hingga target B40.  
**Identitas peristiwa gameplay: TIDAK TAHU.** Instruksi yang diekspor tidak menyebut “akhir putaran”, “settlement”, atau “Barrier release”, tidak mengungkap producer yang memberi makna pada bit 0x20, dan tidak memberi label teks B44. Maka saya tidak memilih salah satu dari tiga nama peristiwa tersebut.

## AZ3 — setter dengan pola getter dikurangi nilai (calon biaya bangun/upgrade)

Semua 14 direct JAL setter yang diekspor dalam AX2:
0x800B41B0, 0x800B4254, 0x800B4F00, 0x800B4F64, 0x800B6238, 0x800BEC98, 0x800DEB38, 0x800E1BE0, 0x800EC9A4, 0x800F95E8, 0x8010A15C, 0x8010A1B0, 0x8010A638, 0x8010A97C.

- Sepuluh callsite awal memuat nilai a1 dari participant/field record atau slot indeks; ekspresinya bukan hasil getter dikurangi nilai.
- Empat callsite FUN_80109FEC di atas menghasilkan Q(i)+B44, Q(i), Q(i)+min(B44,0x14), Q(i).
- Tidak ada ekspresi a1 = Q(i)-nilai yang dibuktikan di 14 direct callsite tersebut.
- Direct call census bukan bukti bahwa indirect JALR tidak ada; indirect JALR dan setter calls di luar cakupan ekspor: **TIDAK TAHU**.

**Hasil AZ3:** kandidat harga Barrier bangun/upgrade melalui pola getter-minus-nilai tidak ditemukan di 14 direct caller yang diekspor; rumus biaya aktual = **TIDAK TAHU**. Jangan menafsirkan pengurangan internal B44 sebagai biaya: instruksi 0x8010A650 menghitung B44-s1 untuk menguras progress transfer, bukan menyusun a1 setter sebagai Q(i)-cost.

## Hipotesis dan falsifier

### AZ2
- H1: bit caller 0x20 + state 7 mengawali settlement/transfer bertahap B44 ke participant +0x18. Falsifier: xref producer untuk bit 0x20 membuktikan flag itu adalah aksi lain yang tidak terkait settlement atau state 7 runtime tidak mengubah participant field.
- H2: state 7 adalah penyelesaian Barrier-release dan B44 merupakan jumlah yang dirilis. Falsifier: producer B30/B38/B40 dan flag 0x20 terbukti terkait event non-Barrier atau jalur state 7 dapat berjalan tanpa event release.

### AZ3
- H1: harga build/upgrade dihitung sebagai Q(i)-cost lalu masuk ke setter 0x8001387C. Falsifier: seluruh setter callsites langsung (termasuk di luar Entry 1) menunjukkan tidak ada ekspresi pengurangan dari getter dan saldo tidak didebit lewat setter ini.
- H2: harga berasal dari tabel/field lain atau didebit melalui setter/indirect call yang belum diekspor. Falsifier: census seluruh direct+indirect callers menunjukkan semua perubahan saldo pembelian berasal dari jalur getter-minus-konstanta yang sama dan tidak ada sumber tabel/field lain.

Confidence: alur register dan kondisi branch K4 statis; identitas gameplay dan unit field B30/B38/B40/B44 belum terverifikasi. Nol hit tidak dijadikan kesimpulan.
