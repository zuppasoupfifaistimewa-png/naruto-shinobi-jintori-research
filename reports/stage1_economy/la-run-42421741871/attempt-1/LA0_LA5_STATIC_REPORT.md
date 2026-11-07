# LA0-LA5 static audit — SLPS-03553

Baseline inklusif: 5a4cd3167beb3a0dba61a48bc6471496ec6fe34f
Source SHA: 191492f06ffebaec0a34cbfe1f131790f0d89627
HEAD saat analisis: 191492f06ffebaec0a34cbfe1f131790f0d89627
EXE SHA-256: a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569
Entry 1 SHA-256: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a
Runtime: EMULATOR_LAUNCHES=0.

## Status
- LA0=TUNTAS K3 — source SHA saat analisis: 9 commit (8 human, 1 bot); HEAD repository final: 18 commit (16 human, 2 bot), baseline inklusif. Tabel commit final ada di LA0_LEDGER_COMMITS_FINAL_HEAD.tsv. Actions: 1.245 run semua event/13 halaman API; 66/66 Python compile.
- LA1=SEBAGIAN K3 — dua pointer word membentuk pola record kandidat berjarak 0x1C pada offset +0x04; belum ada kode pembaca/index/jalr yang membuktikan dispatch. Semua $a2/$a3 pada tiga callsite tetap TIDAK TAHU. Setter wallet otoritatif TIDAK TAHU.
- LA2=SEBAGIAN K3 — D49D0 EA direkonstruksi dari tiga global dan pointer manager; 13 store sb statis pada 0x80139EC4..0x80139EC7; empat store manager+0x530. Himpunan nilai byte x yang dapat dicapai dan identitas x tetap TIDAK TAHU.
- LA3=SEBAGIAN K3 — fungsi 0x800BE5D8 dimulai dengan prolog pada target itu sendiri; satu direct caller terbukti di 0x800B54F4 dari FUN_800B50AC. Parent function/callers B24C8 tetap TIDAK TAHU.
- LA4=TUNTAS K4 — static only; EMULATOR_LAUNCHES=0.
- LA5=BELUM K1 — H(x) dapat dinyatakan hanya sebagai table lookup bersyarat; tidak ada formula biaya numerik untuk lompatan level d>=2.

## Findings
- LA0: source dan HEAD-at-analysis masing-masing 9 commit (8 human, 1 bot, heuristic); HEAD final 18 commit (16 human, 2 bot). Ledger final ada di LA0_LEDGER_COMMITS_FINAL_HEAD.tsv dan LA0_LEDGER_COMMIT_COUNTS.tsv. Actions 1.245 run/13 halaman API untuk semua event (81 schedule); py_compile 66/66.
- LA1(a): pointer word EXE 0x80055904 dan 0x80055920 berisi 0x800B50AC. Keduanya berada pada +0x04 dari dua record kandidat 0x80055900 dan 0x8005591C; word +0x08 kedua record adalah 0x800B5020. Jarak 0x1C adalah candidate record stride, bukan dispatch table yang terbukti. LA1_B50AC_TABLE_USERS.tsv dan LA1_B50AC_DIRECT_CALLS.tsv tidak menunjukkan indexed load/jalr atau caller langsung.
- LA1(b): callsites terkonfirmasi: 0x800F5F54 -> 0x800F2A9C; 0x800B54DC -> 0x800F3658; 0x800F5EBC -> 0x800DC2E0. Penelusuran caller-saved $a2/$a3 berhenti pada incoming/undefined; semua enam hasil register TIDAK TAHU. Slicing linear tidak membuktikan semua path.
- LA1(c): FUN_80014F10 menulis max-update pada participant record +0x94; ini bukan bukti setter wallet permanen. Kandidat +0x04 dan manager+0x4F4 tetap hipotesis dengan dua dukungan dan falsifier masing-masing. Setter otoritatif TIDAK TAHU.
- LA2(a): alamat efektif byte load D49D0 = M + 0x10 + B + 144*I, dengan M=MEM32[0x8013EA74], B=MEM8[0x8013EB1C], I=MEM16[0x8013EA6E]. Alamat terpilih dinamis; tidak ada himpunan byte statis untuk x.
- LA2(b): 13 resolved sb writers overlap 0x80139EC4..0x80139EC7. 0x80139EC4: satu write nilai 1; 0x80139EC5: tidak ada resolved writer; 0x80139EC6: delapan write (enam zero, dua nilai 2); 0x80139EC7: empat write, semuanya zero. Tidak ada resolved sh/sw overlap pada census ini. Nonconstant alias/writer behavior tetap dibatasi oleh static scan.
- LA2(c): seluruh store offset +0x530: 0x800D49D8 (byte dinamis D49D0), 0x800E8174 (zero clear), 0x800EC844 dan 0x800EC868 (low byte dari global 0x80139EC7). Jadi ada tiga jalur pemberi nilai non-reset yang ditemukan ditambah satu reset; nilai jalur pertama dan global source tetap dinamis.
- LA2(d): helper 0x8001552C membandingkan indeks $s0 (asalnya argumen) dengan return helper 0x800154D4 memakai sltu pada 0x80015540 dan branch pada 0x80015544 sebelum lookup. Bila guard lolos, alamat lookup adalah 0x80055CEC + 16*x + 8 = 0x80055CF4 + 16*x. Namun nilai return 0x800154D4 belum dibuktikan sama dengan 52, sehingga guard x<52 belum terbukti. Di F2A9C hanya ada batas kecil/kondisional lokal yang tercatat; bukan bukti universal x<52.
- LA2(e): x=d dan x=effect/item/action selector tetap dua hipotesis K1 dengan dua dukungan dan falsifier; tidak ada yang terbukti.
- LA3: 0x800BE5D8 sendiri adalah function entry (addiu sp,-0x30 pada target, sw ra berikutnya); caller langsung terverifikasi 0x800B54F4 dari FUN_800B50AC. B24C8 tidak mendapatkan batas fungsi/caller yang dapat dibuktikan, meskipun store dan konteks instruksi langsung terekam.
- LA4: no game/emulator/BIOS/savestate/RAM dump; no binary committed.
- LA5: conditional H(x)=u32[0x80055CF4 + 16*x] only if x is below return value of 0x800154D4 and helper path reaches lookup. The link x=d is not proven; no numerical upgrade-cost formula is established. User-proposed figures were not used or fitted; no MATCH/CONTRADICTS labels were assigned.

## TIDAK TAHU
1. Whether 0x80055900/0x8005591C are a true dispatch table, the full extent/stride, and the exact indexed reader or all dynamic callers of 0x800B50AC.
2. Path-specific origin of $a2/$a3 at the three requested calls; no static reaching definition reduced them from incoming/caller state.
3. Permanent wallet setter and semantic identity of participant record +0x04 or manager+0x4F4.
4. Runtime values of M, B, I, the selected D49D0 byte, and the full reachable x domain.
5. Whether every dynamic/alias store to 0x80139EC4..0x80139EC7 is fully represented by constant-EA census.
6. Whether x=d or x is an effect/item/action selector.
7. Whether the guard limit returned by 0x800154D4 equals 52; out-of-range behavior beyond that return limit.
8. Parent function, wrapper, caller set, and semantic index/role for store 0x800B24C8.
9. Numerical upgrade-cost formula for level jumps d>=2.

Instruction evidence tables include image, PC, file offset, bytes and instruction. Quoted instruction groups are at most 64 contiguous bytes after JA/KA aggregate deduplication. No emulator launch.
