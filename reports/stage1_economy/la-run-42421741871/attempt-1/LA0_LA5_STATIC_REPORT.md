# LA0-LA5 static audit — SLPS-03553

Baseline inklusif: 5a4cd3167beb3a0dba61a48bc6471496ec6fe34f
Source SHA: 191492f06ffebaec0a34cbfe1f131790f0d89627
HEAD saat analisis: 191492f06ffebaec0a34cbfe1f131790f0d89627
EXE SHA-256: a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569
Entry 1 SHA-256: 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a
Runtime: EMULATOR_LAUNCHES=0.

## Status
- LA0=TUNTAS K3 if commit/run pagination and py_compile ledgers are complete; bot classification is heuristic
- LA1=SEBAGIAN K3; pointer words/direct refs enumerated, table base/stride and wallet setter may remain TIDAK TAHU
- LA2=SEBAGIAN K3; D49D0 address expression and static store sites recorded; selected byte/domain and x semantics remain TIDAK TAHU
- LA3=SEBAGIAN K2/K3; direct/static-resolvable callers plus manual prolog scan; dynamic JALR/table refs remain TIDAK TAHU
- LA4=TUNTAS K4; static-only exclusion explicit (EMULATOR_LAUNCHES=0)
- LA5=BELUM K1; no numerical upgrade cost for d>=2 and x=d not proven

## Findings
- LA0: baseline-inclusive commit ledger, Actions all-event pagination, and py_compile seluruh skrip Python tercatat di LA0_LEDGER_* dan LA0_PYCOMPILE.tsv. Snapshot HEAD adalah sebelum commit publikasi laporan; commit publikasi tidak dapat menghitung dirinya sendiri.
- LA1: pointer words 0x80055904/0x80055920 dan static J/JAL/JALR candidates ke 0x800B50AC dicatat. Selisih 0x1C sendiri belum membuktikan stride; cek LA1_B50AC_TABLE_USERS.tsv. a2/a3 ditelusuri lewat prolog manual/linear defs, bukan path-sensitive. Wallet setter otoritatif tetap TIDAK TAHU.
- LA2: alamat efektif D49D0 harus dibaca dari LA2_D49D0_EFFECTIVE_ADDRESS.txt. Jika alamat bergantung pada pointer manager dan global mutable, byte result lbu tidak dapat dinyatakan sebagai himpunan statis. Store census mencakup dua image dan mencatat basis unresolved.
- LA3: BE5D8 census mencakup direct calls/jumps, constant jalr/jr, pointer words; target indirect tidak diinferensikan tanpa bukti. B24C8 parent memakai manual prolog heuristic.
- LA4: tidak ada emulator, game execution, BIOS, savestate, atau RAM dump.
- LA5: H table dicatat terpisah. Formula simbolik bersyarat bukan formula upgrade yang terbukti karena domain/identitas x unresolved. Hipotesis angka 400/800/1600 tidak dipakai; tidak ada fitting atau MATCH/CONTRADICTS.

## TIDAK TAHU
- Basis/stride tabel pointer dan seluruh pengguna indirect sekitar 0x80055904/0x80055920 bila tidak ada chain LW+JALR yang terpecahkan.
- Definisi path-specific a2/a3 bila berasal dari incoming caller registers atau melintasi cabang.
- Setter wallet permanen otoritatif; H1/H2/H3 tetap hipotesis.
- Nilai runtime 0x8013EA6E, 0x8013EB1C, 0x8013EA74, byte terpilih D49D0, serta domain x yang dapat dicapai.
- Dynamic alias writers yang tidak dapat dipetakan ke effective address konstan.
- Apakah x=d atau effect/item/action selector; guard x<52 dan perilaku di luar tabel.
- Rumus numerik biaya upgrade untuk lompatan level d>=2.

Setiap baris bukti instruksi memiliki image, PC, file offset, bytes, instruksi. Setiap kutipan kontigu dipotong maksimum 64 byte. Static only.
