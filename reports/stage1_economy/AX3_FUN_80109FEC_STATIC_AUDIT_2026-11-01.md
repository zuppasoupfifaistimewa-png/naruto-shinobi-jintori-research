# AX3 — audit statis FUN_80109FEC dan manager fields

Tanggal 1 November 2026. Target: SLPS-03553; ekspor fungsi dari AQ1. Jenis bukti: statis, maksimum K4.

## Ringkasan

- Satu direct caller terindeks: PC 0x80104960 di FUN_801048F0. Delay slot 0x80104964 adalah move a0,s0. State number tidak dipasok sebagai argumen; fungsi membaca state byte manager+0xB2A di dalam callee.
- Di FUN_80109FEC, B34 bergerak menuju B30, B3C menuju B38, dan B44 menuju B40 dengan langkah 0x14 (20 desimal) lalu snap ke target.
- Pada state 7, code reads Q(i) through getter 0x800138EC, calls setter 0x8001387C with Q(i)+min(B44,0x14), then subtracts that same increment from B44.
- FUN_80109F1C passes B44 as argument a2 to 0x8001B364 with a0=s2+0xC0, a1=s3+0x80, a3=5. This is the clearest adjacent display/format consumer; exact label contents are TIDAK TAHU.
- FUN_80109994 initializes B34=0, B3C=0, B44=0 and B40=B30+B38. It does not write B30/B38.
- This does not identify square-income sources or Barrier build/upgrade costs.

## A. Direct call and internal state

| Call PC | Caller | Instruction | Value passed |
|---|---|---|---|
| 0x80104960 | FUN_801048F0 | jal 0x80109FEC; delay slot at 0x80104964: move a0,s0 | a0=s0; no explicit state byte/value in arguments |

Inside the target function, state is loaded by 0x8010A094 lbu v0,0xB2A(v1), where v1 is manager base loaded via global pointer slot 0x8013A554. State 7 is compared at 0x8010A134 li v0,7 and 0x8010A138 bne v1,v0,... . The switch later loads the same manager byte at 0x8010A23C.

## B. Direct writes within FUN_80109FEC

Manager base derives from global pointer slot 0x8013A554 (lw ..., -0x5AAC(reg)). Values below follow MIPS loads/stores, with the exact branch predicate.

| Store PC | Offset | Stored value/expression | State/branch predicate |
|---|---:|---|---|
| 0x8010A0DC | +0xB34 | MEM32[manager+0xB30] | (MEM32[param_1+0xC] & 0x20)!=0 and state B2A is 3,4,5,or 6 |
| 0x8010A0E8 | +0xB3C | MEM32[manager+0xB38] | same input-bit and state 3–6 branch |
| 0x8010A0F4 | +0xB44 | MEM32[manager+0xB40] | same input-bit and state 3–6 branch |
| 0x8010A1C4 | +0xB44 | 0 | input bit 0x20 active and state B2A==7; after getter/setter path |
| 0x8010A334 | +0xB34 | old(B34)+0x14 | switch state 3, with B34<B30 before increment; if still below target after update, function returns and remains in state 3 |
| 0x8010A360 | +0xB34 | B30 | terminal state 3 when progress reaches or exceeds B30; then state byte becomes 4 |
| 0x8010A4D4 | +0xB3C | old(B3C)+0x14 | switch state 5, with B3C<B38 before increment; if still below target, function returns and remains in state 5 |
| 0x8010A500 | +0xB3C | B38 | terminal state 5; then state byte becomes 6 |
| 0x8010A59C | +0xB44 | old(B44)+0x14 | switch state 6, with B44<B40 before increment; if still below target, function returns and remains in state 6 |
| 0x8010A5C8 | +0xB44 | B40 | terminal state 6; then state byte becomes 7 |
| 0x8010A658 | +0xB44 | old(B44)-s1 | switch state 7. s1=min(old(B44),0x14): when B44<21, load B44 at 0x8010A610; otherwise jump 0x8010A614 executes delay slot li s1,0x14 at 0x8010A604 and skips that load |

No direct store to manager+0xB30 or manager+0xB38 occurs in this function body. This is scoped to the complete FUN_80109FEC body exported by AQ1, not a whole-ROM writer census.

## C. Manager initializer cross-check

| Function / store PC | Offset | Value |
|---|---:|---|
| FUN_80109994 / 0x80109A48 | +0xB34 | 0 |
| FUN_80109994 / 0x80109A4C | +0xB3C | 0 |
| FUN_80109994 / 0x80109A54 | +0xB44 | 0 (JAL delay slot of jal 0x80012AC0) |
| FUN_80109994 / 0x80109A94 | +0xB40 | MEM32[manager+0xB30] + MEM32[manager+0xB38] |

B30/B38 writers outside these two functions: TIDAK TAHU.

## D. Readers near B44 increment/decrement and candidate display readers

| PC / function | Instruction/data flow | Evidence-bounded interpretation |
|---|---|---|
| 0x8010A648 | lw v0,0xB44(v1) | reads old B44 |
| 0x8010A650 | subu v0,v0,s1 | computes new B44 = old B44 - s1 |
| 0x8010A654 | jal 0x80011C6C | no text pointer or label literal is prepared by instructions in A648–A658; result is tested via andi v0,1 at A65C after the delay-slot store |
| 0x8010A658 | delay slot sw v0,0xB44(v1) | writes the decremented value |
| FUN_80109F1C / 0x80109F64–0x80109F68 | lw a2,0xB44(v1); jal 0x8001B364; a0=s2+0xC0, a1=s3+0x80, a3=5 | B44 is supplied as a numeric argument alongside a buffer/resource pointer; likely format/display consumer, but literal label is TIDAK TAHU |

Other progress states call 0x80011C6C, test its return bit, then call UI/audio-like functions 0x80018300, 0x80018468 and 0x80018508. Their code does not identify the text name of B44. The literal string or resource consumed by 0x8001B364 is not mapped here.

## E. Competing hypotheses and falsifiers

**Question 1 — meaning of B44**

1. **H1 (K3): pending quantity credited to participant field +0x18.** State 6 fills B44 toward B40 in 0x14 increments; state 7 sends Q(i)+min(B44,0x14) through the setter and subtracts the same increment. The getter/setter disassembly identifies participant record +0x18 as the field read/written. **Falsifier:** a controlled original-code runtime run shows the selected participant +0x18 is not increased by the live a1 passed to setter, or a producer/consumer proves B44 is another named variable.
2. **H2 (K2): generic staged transfer/animation quantity, not proven to be square income or Barrier release.** No instruction labels its source as territory income or Barrier release; initializer only sets B40=B30+B38. **Falsifier:** a static producer or runtime UI/action path directly ties B30/B38/B40 to a named Barrier or land-income event.

**Question 2 — meaning of the B30/B34, B38/B3C and B40/B44 pairs**

1. **H1 (K3): target/progress pairs for three staged numeric roll-ups.** States 3,5,6 advance their progress values by 0x14 and snap them to their corresponding target. **Falsifier:** runtime traces of the original branch paths show any pair not following the observed target/increment behavior.
2. **H2 (K2): three separate staged metrics, not necessarily one economic unit.** The three pairs progress in distinct state numbers; only B44 is visibly routed to participant +0x18 by these instructions. **Falsifier:** producer code proves all three values are consistently components of the same named economy quantity and unit.

**Question 3 — display/label for B44**

1. **H1 (K2): B44 is sent as a numeric formatting argument to 0x8001B364.** Caller supplies B44 in a2 with buffer/resource pointer a1=s3+0x80. **Falsifier:** callee disassembly shows a2 is not used as a numeric/text-format argument.
2. **H2 (K1): B44 is merely data passed to a generic widget/buffer renderer, with no specific label encoded in this code range.** The A648–A658 sequence has no string address or literal. **Falsifier:** the resource pointed to by s3+0x80 or the callee implementation reveals an explicit named label.

## F. Confidence and unresolved facts

- **K4 static:** state predicates, direct stores, +0x14 increments, terminal snaps, min(B44,0x14), Q(i)+delta setter argument, and B44 decrement are directly visible in MIPS instructions.
- **K3:** the progress-to-participant-field transfer model is strongly supported by instruction flow; the gameplay identity and source transaction remain unproven.
- **K2/K1:** names/units of B30/B38/B40, exact display label, and relation to square income or Barrier build/upgrade/release remain hypotheses.
- Square-income formula: TIDAK TAHU. Barrier build/upgrade cost: TIDAK TAHU. Barrier-release source linkage: TIDAK TAHU.
- K5 is not available from a static audit.

## Sources

- reports/stage1_economy/aq1-run-41291576229/attempt-1/aw1-manager-function-detail.txt
- reports/stage1_economy/aq1-run-41291576229/attempt-1/aq1-deep-context.tsv
- reports/stage1_economy/AU1_ACCESSOR_DISASSEMBLY_2026-11-01.md
- reports/stage1_economy/AT1_SETTER_CALLS.tsv and AU2_SETTER_ARGUMENTS_2026-11-01.tsv
- reports/stage1_economy/aw3-controlled-run-41291503009/attempt-1/AW3_SUMMARY.txt


## G. Batas xref dan seluruh nilai state yang masuk ke dispatcher

Direct reference list dari ekspor AQ1 mencatat satu instruksi pemanggil yang ditemukan: PC 0x80104960, jal 0x80109FEC di FUN_801048F0; delay slot 0x80104964 adalah move a0,s0. Nilai ABI yang masuk adalah a0=s0 (pointer/objek caller), bukan konstanta state. Xref tidak menunjukkan argumen state eksplisit. Pemanggilan tidak langsung melalui function pointer: TIDAK TAHU; satu xref langsung bukan bukti tidak ada indirect call.

State dibaca dari byte manager+0xB2A, bukan argumen caller:
- 0x8010A094 lbu v0,0xB2A(v1), diikuti addiu v0,v0,-3 dan sltiu v0,v0,4 menguji state 3,4,5,6.
- 0x8010A130 lbu v1,0xB2A(a0), lalu li v0,7 dan bne; state 7 memasuki jalur getter/setter yang berhubungan dengan B44.
- 0x8010A23C lbu v1,0xB2A(v0) menjadi indeks jump table: sltiu batas 0x10, sll indeks 2, load alamat dari tabel dan jr. Dekompilasi switch menampilkan case 0, 2, 3, 4, 5, 6, 7, 8; state 1 jatuh ke default path. Makna cabang state 9–15: TIDAK TAHU dari bukti yang diekspor.

## H. Pembaca display yang dapat dibuktikan

Pada rentang tepat 0x8010A648–0x8010A658, instruksinya:
- 0x8010A648 lw v0,0xB44(v1)
- 0x8010A64C nop
- 0x8010A650 subu v0,v0,s1
- 0x8010A654 jal 0x80011C6C
- 0x8010A658 delay slot sw v0,0xB44(v1)

Tidak ada load string, alamat teks, atau literal label pada rentang tersebut.

Pembaca B44 terdekat yang menyiapkannya bersama pointer buffer/teks berada di FUN_80109F1C:
- 0x80109F5C addiu a0,s2,0xC0
- 0x80109F60 addiu a1,s3,0x80
- 0x80109F64 lw a2,0xB44(v1)
- 0x80109F68 jal 0x8001B364; delay slot 0x80109F6C li a3,5

Ini membuktikan B44 dipasok sebagai a2 bersama dua alamat buffer/teks dan parameter a3=5. Caller tidak mengungkap literal string atau label yang dipakai callee. Identitas tulisan yang terlihat: TIDAK TAHU.


## I. Census lengkap akses manager+0xB44 pada tiga fungsi terpetakan

Census statis AW1 mencatat 14 instruksi yang mengakses displacement +0xB44. Tabel ini melengkapi fokus A648–A658 dan membedakan load, store, serta calon angka yang diberikan pada routine tampilan.

| PC | Fungsi | Instruksi | Peran yang dapat dibaca dari alur |
|---|---|---|---|
| 0x80109A54 | FUN_80109994 | delay slot sw zero,0xB44(v0) | inisialisasi B44=0 |
| 0x80109F64 | FUN_80109F1C | lw a2,0xB44(v1) | B44 diberikan sebagai a2 ke jalur 0x8001B364; buffer pointer di a0/a1 dan a3=5. Teks literal TIDAK TAHU |
| 0x8010A0F4 | FUN_80109FEC | sw v1,0xB44(v0) | snapshot B40 ke B44 saat input bit 0x20 dan state B2A 3–6 |
| 0x8010A154 | FUN_80109FEC | lw a1,0xB44(v1) | sumber addend pada a1; delay slot A160 menambahkan getter Q(i) sebelum setter |
| 0x8010A1C4 | FUN_80109FEC | sw zero,0xB44(v0) | reset B44=0 pada jalur state 7 ketika bit input 0x20 aktif |
| 0x8010A524 | FUN_80109FEC | lw v0,0xB44(v1) | dibandingkan dengan B40 oleh slt di A530 untuk state 6 |
| 0x8010A590 | FUN_80109FEC | lw v0,0xB44(v1) | membaca progress lama sebelum penambahan 0x14 di A598/A59C |
| 0x8010A59C | FUN_80109FEC | sw v0,0xB44(v1) | menyimpan old(B44)+0x14 dalam state 6 |
| 0x8010A5C8 | FUN_80109FEC | sw v1,0xB44(v0) | snap B44=B40 ketika state 6 mencapai target, lalu B2A menjadi 7 |
| 0x8010A5EC | FUN_80109FEC | lw v0,0xB44(v0) | input ke pembatasan nilai 0x15 di A5F4 |
| 0x8010A610 | FUN_80109FEC | lw s1,0xB44(v0) | dipilih bila B44<21; bila tidak, jump-delay A604 menetapkan s1=0x14 |
| 0x8010A648 | FUN_80109FEC | lw v0,0xB44(v1) | membaca nilai sebelum pengurangan state 7 |
| 0x8010A658 | FUN_80109FEC | delay slot sw v0,0xB44(v1) | menyimpan old(B44)-s1 |
| 0x8010A6A8 | FUN_80109FEC | lw v0,0xB44(v1) | pemeriksaan terminal: bne v0,zero di A6B0; bila nol, state byte diubah ke 8 |

Census ini mengandung 14 akses dalam 3 fungsi (FUN_80109994, FUN_80109F1C, FUN_80109FEC), bukan 14 label string. Hanya site FUN_80109F1C / 0x80109F64 yang terlihat meneruskan B44 bersama buffer pointer ke formatter/routine 0x8001B364. Tidak ada bukti string teks literal atau label semantik khusus B44 dari call-site itu. Nilai yang diuji secara numerik di FUN_80109FEC adalah B44 vs B40 (A530), B44 vs 0x15/21 (A5F4), serta B44 != 0 (A6B0); tidak satu pun instruksi perbandingan tersebut menamai konsep ekonomi.

