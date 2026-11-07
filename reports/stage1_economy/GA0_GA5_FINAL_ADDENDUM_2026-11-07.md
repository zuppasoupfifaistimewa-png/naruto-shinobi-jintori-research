# Addendum GA0–GA5 — audit biaya upgrade petak (2026-11-07)

Repo `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`  
Baseline inklusif = HEAD awal `6987a76e12b0adf86f8061d47dcc4078e79cda21` (`main`). Pemeriksaan ini statis; tidak menjalankan emulator, adaptive-player, atau watchpoint. Hipotesis pengguna 400/800/1600 tidak dipakai.

## Kesimpulan
Tiga rumus store `manager+0x2EE` dapat direkonstruksi, tetapi belum terbukti bahwa field ini adalah biaya upgrade, terhubung ke selisih level `d`, atau langsung mendebit uang pemain. Rumus biaya upgrade lintas-level d>=2: **TIDAK TAHU**.

## GA0 — Ledger
Rentang inklusif baseline sampai HEAD awal memuat **1 commit** (manusia 1, bot 0); `STATUS.md` tidak disentuh. Satu Actions run pada SHA rentang: `42320736860`, scheduled `Naruto Story Mode adaptive player monitor`, completed/success; job `monitor`, ID `128244394048`, conclusion success. Exit code proses tidak disediakan API; `0` hanya diturunkan dari conclusion job. Log: tidak ada adaptive-player run dalam 50 run terbaru; `monitoring-report.txt` tidak ada, upload tidak menemukan file, artifact tidak dibuat. Queued=0, in_progress=0 saat pemeriksaan. Ringkasan ada di `ga0-run-42320736860/ACTIONS_RUN_SUMMARY.txt`. Tidak meluncurkan run baru.

## GA1 — Koreksi FA0–FA5
Berkas lama `FA0_FA5_SESSION_VERIFICATION_2026-11-07.md` tidak diubah.

**Offset Entry 1:** `0x10BB000 + (PC - 0x800AD450)`.  
`0x800F7E64 - 0x800AD450 = 0x50A14`; hasil `0x01105A14`.  
`0x800F7E68 - 0x800AD450 = 0x50A18`; hasil `0x01105A18`.  
Offset lama `0x010FFA14/18` salah.

**Helper 0x8001552C:** excerpt 19 instruksi Ghidra tersimpan dalam laporan lama untuk EXE SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`: `lui v0,0x8005; addiu v0,v0,0x5CEC; sll v1,s0,4; addu v0,v0,v1; lw v0,8(v0)`. Maka `0x80055CEC + u32(a0)*0x10 + 8 = 0x80055CF4 + u32(a0)*0x10`, tanpa +8 kedua. `H(x)=u32[0x80055CF4+16*x]` jika `u32(x)<FUN_800154D4()`, selain itu `H(x)=0`. TSV otomatis `EA2_FUN_8001552C_RETURN_HELPER.tsv` ditolak karena bytes/decode-nya bertentangan dengan excerpt Ghidra untuk EXE SHA sama. Dump Ghidra mentah dan body `FUN_800154D4` tidak ada sebagai file independen dalam tree; excerpt laporan lama bukan verifikasi independen. Batas/helper table belum diverifikasi.

**Negu:** bytes `23 10 02 00` di `0x800F2E0C` dan `0x800F2E64` adalah `negu $v0,$v0` (`subu $v0,$zero,$v0`), bukan negasi nol. `$v0` adalah return helper JAL `0x800F2DF0` / `0x800F2E48`, sehingga hasil `-H(x)` modulo 32-bit. Klaim store `0x800F2E38` pasti nol salah.

Dengan `G=u8(0x8013EA71)`, `Q=u32(0x80139EFC)`, dan `x` dari record `+0x530`, nilai yang ditulis (`sh`, low 16-bit):
| PC | Rumus |
|---|---|
| `0x800F2CF8` | `u16(LO32(H(x1)*(G-2)))` |
| `0x800F2E38` | `u16(LO32((-H(x2))*(G-1-Q)))` |
| `0x800F2E68` | `u16(-H(x3))` |

Basis manager `M=u32(0x8013EA74)`; alamat store `M+2*idx+0x2EE`, `idx` dari `0x8013EB0C`. Hubungan `x=d` belum terbukti.

## GA2 — CFG `FUN_800F2A9C`
Census raw TSV mendukung tiga store utama:
- `0x800F2CF8` scan leg: `0x800F2AD0` harus taken (byte `0x80139F42==1`); `0x800F2B2C` not-taken (return `0x80104E1C==0`); `0x800F2C50` dan `0x800F2C68` not-taken (`(return 0x80012AD0 & 0x1000)!=0`, `G>0`); `0x800F2C84` not-taken (`idx!=u16(0x8013EA8A)`); `0x800F2CBC` not-taken (record byte +0xE sama); loop `0x800F2D54` selama `idx+1<G`, jadi kandidat idx `0..G-1`.
- `0x800F2E38` fallback: `0x800F2D70` not-taken (`G>0`); `0x800F2D90`/`0x800F2DA0` not-taken (idx berbeda dari sentinel di `0x8013EA8A` dan nilai melalui manager-global `0x8013EBB0`, arti kedua belum diketahui); `0x800F2DC8` not-taken (`(record[+0xD]&1)==0`); `0x800F2DDC` not-taken bila masked return `0x80012AD0 & 0x1000` nonzero, memilih store `0x800F2E38`.
- `0x800F2E68` menggunakan fallback sama; `0x800F2DDC` taken bila bit `0x1000` nol, memilih jalur `0x800F2E3C..0x800F2E68`.

Dalam fungsi: `0x8013EA71` dibaca 5 kali (tanpa write lokal); `0x80139EFC` dibaca 2 kali (tanpa write lokal); manager `+0x530` dibaca 4 kali. Di luar fungsi, tersedia 44 writer Entry 1 untuk `0x80139EFC` dan dua ekspresi aritmetika; census semua reader belum ada. Census lengkap semua penulis/pembaca `0x8013EA71` dan manager `+0x530` lintas EXE+Entry 1 belum dilakukan.

Fungsi memiliki satu epilog fisik `jr $ra` di `0x800F30F8`, tetapi nilai `$v0` tiap jalur return belum diekstrak per-path. Satu direct JAL caller `0x800F5F54`; caller tak langsung via jalr/tabel jr lintas EXE+Entry 1 belum ditentukan. Dump `FUN_800154D4`, bound dan isi tabel `u32[0x80055CF4+16*i]` belum tersedia: **TIDAK TAHU**.

## GA3 — Census manager+0x2EE
Scan langsung menemukan 25 operasi `+0x2EE`; dua (`0x800DFF64`, `0x800EB400`) memakai basis `0x8013EA88`, bukan manager slot `0x8013EA74`, jadi dikecualikan. Tersisa **23 manager-backed**: **20 `sh` WRITE dan 3 `lh` READ**, tanpa `lhu/lw/sw` pada scan langsung. Seluruh PC/fungsi/bytes/offset/basis tercantum dalam TSV.

`FUN_800D15A8`, PC `0x800D46F8`: menulis `u16(-u16(tile+0x1A))` ke `manager+2*idx+0x2EE`. Ini membuktikan pembentukan nilai negatif dari tile, bukan bahwa saldo pemain didebit.

READ: `0x800DCFE8` (`FUN_800DC2E0`), `0x800F2E80` (`FUN_800F2A9C`), `0x800FAAEC` (`FUN_800FAAC8`). Jalur reader ke setter langsung belum ditemukan; aliran inter-fungsi/indirect dan terminal use belum tertutup. Apakah nilai dikurangkan dari uang, ditambahkan, atau untuk tampilan/status: **TIDAK TAHU**.

Hipotesis (belum terbukti): H1 = delta resource/debit tertunda; falsifier bila tak ada terminal debit wallet atau tanda/jumlah tidak cocok. H2 = cache/status/presentasi/keputusan non-uang; falsifier bila reader terminal terbukti meneruskan nilai ke setter saldo dan saldo berubah sepadan.

## GA4 — CONTROL H6
Run `39867730674` (2026-10-22, source SHA `c9b1438292041f972b712f248fb7052032635b59`) memang mengunggah artifact `naruto-storymode-adaptive-player-private`, ID `12464258211`, 4,913,880 byte, 23 berkas; upload sukses walau emulator gagal exit `134`. Workflow pada SHA sumber memakai `retention-days:14`. Listing artifact sekarang kosong dan download ID memberi 404; artifact lama expire. `retention-days:90` pada workflow HEAD hanya berlaku untuk artifact baru, tidak retroaktif.

H6 mematok run lama, file `adaptive-cycle-01-f180.sstate`, SHA-256 `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`. Run H6 `42312284099` gagal di `CONTROL_artifact_download`, PCSX launches=0, watchpoints=0. Artifact aktif kandidat: run `39907655833`, ID `12482055310`, 11,407,011 byte, expired=false, expiry `2027-01-21T05:46:51Z`; checkpoint `adaptive-cycle-02-f180.sstate`, SHA-256 `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`. Ini snapshot berbeda, bukan rebuild identik. Perlu ubah run pin, nama file dan checksum H6. Adaptive-player dipause; tidak diluncurkan run/artifact/watchpoint.

## GA5 — Prediksi simbolik
| Model | d=1 | d=2 | d=3 | d=4 |
|---|---:|---:|---:|---:|
| Linear `C*d` | `C` | `2C` | `3C` | `4C` |
| `C*2^(d-1)` | `C` | `2C` | `4C` | `8C` |
| Akumulasi `C*sum(2^k), k=0..d-1` | `C` | `3C` | `7C` | `15C` |
| Lookup | `L[1]` | `L[2]` | `L[3]` | `L[4]` |

Lookup baru terkait `H(x)` bila runtime membuktikan `x=d`; saat ini `x` dari record `+0x530`, `x=d` **TIDAK TAHU**. Falsifier runtime: rekam frame, PC, effective address, nilai lama/baru dan register saat write `managerBase+2*idx+0x2EE` di PC `0x800F2CF8/2E38/2E68` dan `0x800D46F8`; pantau `tile+0x20` (u16 dan nibble `((u16>>8)&0xF)`), `tile+0x1A`, global `0x80139EFC`, `0x8013EA71`, `0x8013EB0C`. Jalankan transisi d=1..4 kondisi petak/karakter sama; temukan wallet terminal lebih dahulu.

## Validasi dan status
TSV baru memakai header `pc,file_offset,bytes,instruksi`; offsets dihitung sesuai peta EXE/Entry 1. Validasi internal: 68 baris instruksi, **0 salah decode, 0 salah offset**. Tidak ada skrip Python berubah/ditambah, jadi py_compile tidak berlaku. Tidak ada ISO/BIOS/savestate/RAM dump/video/frame/biner dikomit. Release `naruto-checkpoint-39262213468` dan `STATUS.md` tidak diubah.

| Tugas | Status | K | Dasar |
|---|---|---:|---|
| GA0 | TUNTAS | K4 | Ledger satu commit, scheduled run dan job diperiksa. |
| GA1 | TUNTAS | K4 | Tiga koreksi spesifik dan rumus store diterbitkan; keterbatasan excerpt dinyatakan. |
| GA2 | SEBAGIAN | K3 | Store/jalur utama ada; bound, tabel, return values, operand global lengkap dan indirect callers belum lengkap. |
| GA3 | SEBAGIAN | K3 | 23 akses manager-backed; terminal use tiga READ belum diketahui. |
| GA4 | SEBAGIAN | K3 | Artifact lama expire; kandidat pengganti berbeda dan pin belum diubah. |
| GA5 | SEBAGIAN | K3 | Prediksi simbolik/falsifier ada; belum ada runtime pembeda model. |

GA0–GA1 selesai pada ruang lingkupnya; GA2–GA5 parsial. **Rumus biaya upgrade lintas-level d>=2 tetap TIDAK TAHU.**
