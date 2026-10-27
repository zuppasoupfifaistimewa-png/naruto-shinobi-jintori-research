# Rekonsiliasi live reverse engineering Langkah 4–10 — 27 Oktober 2026

## Checkpoint dan Actions

HEAD remote \`main\` diverifikasi sebelum audit dokumentasi: \`cc81319cc00037a92a93a3e76552245dd9a9ebf7\` ([commit](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/cc81319cc00037a92a93a3e76552245dd9a9ebf7)). Snapshot API branch menunjukkan 0 run \`in_progress\` dan 0 \`queued\`.

Run terbaru secara keseluruhan pada snapshot adalah [#40506364365](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40506364365), workflow monitor terjadwal, \`completed/success\`, source SHA \`cc81319cc00037a92a93a3e76552245dd9a9ebf7\`, tanpa artefak. Itu hanya hasil job monitor dan bukan bukti reverse engineering/gameplay/tamat. Audit ini tidak memulai monitor tersebut atau workflow gameplay.

Run analisis terbaru yang relevan adalah [#40504640855](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504640855) (\`completed/success\`, source \`486e2590b45efaedd7972accb4561cd647f8a711\)); runner audit berikutnya [#40504977322](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504977322) (\`completed/success\`, source \`4ab16073f770233edffcb13ad8b489361604b64c\)). Semua langkah scan, private-work cleanup, text-only validation, artifact metadata/digest verification dan audit cleanup selesai sukses. Karena tidak ada run aktif/queued, ETA tidak berlaku.

## Temuan statis baru Langkah 6

Artifact scan [#12733854252](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504640855/artifacts/12733854252), \`step6-resource-field-static-scan\`, 220.128 byte, dibuat 27 Okt 2026 19:34:27 WIB, tidak expired pada API snapshot, expiry 10 Nov 2026 19:34:27 WIB, ZIP SHA-256 \`90288a1c8b454cbdc45c75e0244d26508628ecf88bfe8e73ed88524c8cb80891\`. ZIP diunduh untuk pemeriksaan lokal dan checksum cocok; enam anggota adalah teks/log saja (total uncompressed 2.034.490 byte). Tidak ditemukan disc image, executable game, BIOS, Memory Card, savestate, RAM dump atau screenshot di dalam ZIP. [Runner audit artifact #12734840847](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504977322/artifacts/12734840847), 25.756 byte, expiry 10 Nov 2026 19:35:46 WIB, SHA-256 \`d022b23548fe95eb34bfbb7a7fb0dd190a498ca54fff11516818138701920398\`; API metadata dan digest diaudit runner, cleanup PASS.

Parser independen atas \`field-offset-scan.txt\` (1.933.583 byte, 41.496 baris) menghasilkan 2.104 displacement unik dan 31.081 akses base+displacement langsung dalam 98.357 instruksi terdekode (19.366 reads, 11.715 writes). Seluruh baris inventaris agregat berada di antara marker BEGIN/END dan di bawah batas emitter 30.001 baris. Ini menuntaskan inventaris agregat **untuk integer/coprocessor load-store yang dikenali, didekode Ghidra dan memakai syntax displacement(base) dalam view entry-1 kandidat**; bukan semua bentuk akses memori di program.

Base \`0x800D0000\` tetap HIPOTESIS, bukan base RAM runtime yang terverifikasi. Dataflow operand prioritas yang baru cross-check:
- \`0x8012C634 lw v0,0xB30(a0)\`, bytes \`30 0B 82 8C\`, membaca \`+0xB30\` (1 read, 0 write dalam inventory).
- \`0x8012C638 lw v1,0xB38(a0)\`, bytes \`38 0B 83 8C\`, membaca \`+0xB38\` (1 read, 0 write).
- \`0x8012C640 addu v0,v0,v1\`, bytes \`21 10 43 00\`; \`0x8012C644 sw v0,0xB40(a0)\`, bytes \`40 0B 82 AC\`. Jadi yang terbukti statis adalah load dua nilai, menjumlahkan, lalu menyimpan hasil ke \`+0xB40\`.
- \`0x8012C604 sw zero,0xB44(v0)\`, bytes \`44 0B 40 AC\`, men-zero-kan \`+0xB44\` pada jalur inisialisasi kandidat \`0x8012C544\`.
- \`0x8012CB14 lw a2,0xB44(v1)\`, bytes \`44 0B 66 8C\`, memasok nilai ke argumen \`a2\` sebelum call \`0x8001B364\` pada jalur kandidat \`0x8012CACC\`.
Operasi ini mendukung hubungan dataflow terbatas saja. Tidak membuktikan object identity, runtime mapping, arti field, atau aturan gameplay.

**Batas konteks per-instruksi:** inventaris agregat lengkap tidak berarti semua akses punya blok konteks lengkap. Blok \`MEMORY_MATCH\` dibatasi 200 per displacement umum: \`+0x2E9\` mempunyai 257 akses (86 read, 171 write) namun 200 konteks; \`+0x22\` mempunyai 275 (178 read, 97 write) namun 200 konteks. Empat offset prioritas \`+0xB30/+0xB38/+0xB40/+0xB44\` tidak terkena cap konteks per-offset dan seluruh konteks scan yang sesuai tersedia. Base-register trace tetap linear maksimal 24 instruksi/simple \`move\`, berhenti di control flow; computed pointers, indirect aliases, split immediates, alternate bases, undecode code dan boundary/P-code bermasalah masih terbuka.

Tooling sudah berubah sebelum audit ini: commit \`486e2590b45efaedd7972accb4561cd647f8a711\` menormalisasi mnemonic delay-slot \`_\` serta mengenali integer/coprocessor load-store; \`4ab16073f770233edffcb13ad8b489361604b64c\` menaikkan output emitter menjadi 30.001 baris. Scan terbaru sukses dan fixture parser lulus; tidak ditemukan alasan berbukti untuk patch scanner berikutnya hanya demi menambah perubahan.

## Matriks kriteria Langkah 4–10

| Kriteria | Status | Bukti utama | Celah dan syarat penerimaan yang belum dipenuhi |
|---|---|---|---|
| 4(a) Generator/state/origin dan lifecycle seed | **SEBAGIAN** | MIPS RNG \`0x80035D78\`, state \`0x800A3118\`, \`(old×0x41C64E6D+0x3039) mod 2^32\`, output \`(new>>16)&0x7FFF\`; main EXE reset/increment global \`0x80066E7C\); helper \`0x80037138\`; Ghidra #40498208067/artifact #12732952776. | Nilai seed runtime, urutan initializer/callsite, nilai register setter dan semua re-seed/indirect paths belum terbukti. Pada candidate entry-0, \`li a0,-1\` adalah argumen helper, sedangkan delay-slot \`move a0,v0\` meneruskan helper return ke candidate setter \`0x80035DA8\`; tidak ada runtime hit pada #40485987817 sampai frame 120. |
| 4(b) Determinisme dan hasil roulette tampak | **SEBAGIAN** | #40474262267, artifact #12719024236, SHA-256 ZIP \`cec3404b38afbedbae151fc15e9ec66d9c019ff853e4703f8813acac7793bdf4\`: 127 observasi caller/state-before ternormalisasi, final state \`0xA99DC6E7\), crop viewport sama pada window itu. | Terminal capture frame 167/169/171 berbeda; belum ada hubungan kausal independen antara caller/state dan hasil roulette visual. |
| 4(c) Direct/indirect callers, JT, decompressed paths | **SEBAGIAN** | Ghidra #40498208067, audit #40503223693; 5 raw JAL entry-0 (3 decoded); 144 raw candidates entry-1 (108 decoded/50 fungsi, 36 raw-only). | Indirect/JALR/JT menyeluruh, base runtime/reachability, raw-only boundaries, dan code setelah decompress/decrypt belum tersingkir. |
| 4(d) Caller roulette dan battle | **SEBAGIAN** | Observasi roulette dan static RNG trace di laporan Step 4. | Kaitan caller-ke-hasil roulette tidak kausal; battle checkpoint/caller autentik belum ditelusuri. |
| 4(e) RNG alternatif/randomness lain | **SEBAGIAN** | Signature scan pola LCG dan caller inventory. | Signature terbatas tidak menyingkirkan tabel, frame/time, algoritme lain, indirect call atau code terdekompresi. |
| 5) Cross-check Ghidra/m2c untuk empat fungsi yang ditetapkan | **TUNTAS, empat fungsi saja** | #40449144521, source \`62a4c114b7ac7a55ae9eb6d91bc4c9bfaef1c2ef\`, artifact #12710000931 (926.540 byte; ZIP SHA-256 \`b2fdb6dc3213137e98e0ed298402e1d4b02198ed5310f264780bd8e965246b08\`); \`0x80015ADC\`, \`0x80015B7C\`, \`0x8001A328\`, \`0x80020BF4\` masing-masing punya dua output C. | Tidak menyatakan validasi seluruh executable atau source asli; klaim dibatasi ke empat fungsi yang ditetapkan saat ini. |
| 6(a) Census direct memory operand/RW + raw bytes dalam decoded view | **TUNTAS pada scope census ini** | #40504640855 artifact #12733854252, 2.104 displacements/31.081 accesses, agregat lengkap; raw bytes B30/B38/B40/B44 di atas. | Hanya instruksi load/store yang dikenali dan didekode pada view entry-1 kandidat. Base \`0x800D0000\` tidak divalidasi runtime; ini bukan bukti whole-program access closure. |
| 6(b) Effective addresses, pointer aliases, split immediates, semua reader/writer dan alternate base | **BLOCKED** | Inventaris langsung lengkap di scope di atas; audit #40504977322 success/cleanup PASS. | Trace alias bounded dan tidak meliputi computed address, indirect alias, alternate base, undecoded bytes atau split immediate. Perlu analisis raw MIPS/control-flow/address-construction yang lebih luas dengan coverage eksplisit. |
| 6(c) Dataflow/caller/callee yang didukung statis | **SEBAGIAN** | B30+B38→addu→B40; B44 zero-store dan read yang disalurkan ke \`a2\` untuk \`0x8001B364\`. | Seluruh caller/callee, initial/final writer dan lifecycle object belum selesai; semantik efek pada state masih belum diketahui. |
| 6(d) Nama semantik field/kode | **UNKNOWN** | Operasi statis di atas, base hipotetis. | Tidak ada bukti independen bahwa offsets bermakna Chakra, cost, barrier, turn atau level-up. Butuh caller/callee, tipe/validasi nilai dan korelasi state/output independen. |
| 7(a) Static resource directory/loader/copy | **SEBAGIAN** | DATA.BIN bootstrap + 1.504 entri; kandidat directory/copy statis, lihat laporan Step 7. | Base entry 0/1, relocation, load/unload lifecycle, DATA2.BIN/DUMMY.BIN end-to-end belum dipetakan. |
| 7(b) Runtime mapping + copy source/destination/size/checksum | **BLOCKED** | #40484548650/artifact #12724961702 (3.960 byte; SHA-256 ZIP \`27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71\`): no-hit \`0x800AD454\` s.d. frame 120, timeout 35s/exit 124, cleanup PASS. | Tidak ada register/copy-length/checksum runtime. Jangan ulang target sama; PC baru harus terlebih dahulu didukung reachability statis. |
| 8(a) Function semantics dari caller/callee/raw MIPS | **SEBAGIAN** | RNG/helper/counter, getter/setter, beberapa compare/store dan dataflow terpetakan. | Beberapa transition decompile boundaries/P-code bermasalah, dan aliran penuh state belum tersedia. Klaim harus menunjuk instruksi, branch, register dan store/call yang spesifik. |
| 8(b) Aturan aktual cost/barrier/upgrade/battle/roulette/turn/kartu/menang | **UNKNOWN** | Tidak ada label mekanika yang diasumsikan hanya dari offset/nama simbol. | Formula biaya/resource, efek kartu, giliran, win/loss per mode belum ditopang bukti independen. Jangan namai field atau aturan tanpa chain raw MIPS/dataflow dan corroboration. |
| 9(a) Eksekusi isolasi RNG \`0x80035D78\` | **TUNTAS, hanya fungsi ini** | #40474891838/artifact #12720127454 (3.201 byte, SHA-256 ZIP \`bcbfcd77a532ce34334ed60f720fdeaac566308bf2e6e4d54a7e60f28a5f083b\`): 7/7 vektor, state/\`v0\` cocok, sentinel 12 instruksi per vektor, limit 128, physical RAM 2 MiB. | Bukan emulator PS1 penuh; tidak menguji caller, seed, visible roulette, fungsi lain. |
| 9(b) Coverage fungsi/kondisi lain yang diwajibkan | **UNKNOWN** | Hanya RNG utama yang memiliki hasil isolated test dengan oracle. | Belum ada daftar lengkap seluruh rutin/kondisi yang diwajibkan beserta oracle/edge case. Tentukan set coverage dari kriteria dan uji setiap tambahan dengan register/memory/return checks; no gameplay/savestate. |
| 10) Audit matrix: kriteria→bukti primer/run/commit/hash/status/gap | **TUNTAS sebagai proses matriks saja** | Dokumen ini dan closure report, metadata API artifact #40504640855/#40504977322. | Tidak berarti Steps 4–9 semuanya selesai; refresh saat bukti baru tersedia. |

## Inventaris artefak dan cleanup

| Run/artifact | Source SHA | Ukuran ZIP | SHA-256 ZIP (API digest) | Expiry WIB ketika diperiksa |
|---|---|---:|---|---|
| [#40504640855 / #12733854252](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504640855) | \`486e2590b45efaedd7972accb4561cd647f8a711\` | 220.128 | \`90288a1c8b454cbdc45c75e0244d26508628ecf88bfe8e73ed88524c8cb80891\` | 10 Nov 2026 19:34:27 |
| [#40504977322 / #12734840847](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504977322) | \`4ab16073f770233edffcb13ad8b489361604b64c\` | 25.756 | \`d022b23548fe95eb34bfbb7a7fb0dd190a498ca54fff11516818138701920398\` | 10 Nov 2026 19:35:46 |
| [#40498208067 / #12732952776](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498208067) | \`dc5ad30c1ec97329e2829da33da092d1bf43f5ef\` | 2.255.170 | \`6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6\` | 10 Nov 2026 19:14:36 |
| [#40449144521 / #12710000931](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40449144521) | \`62a4c114b7ac7a55ae9eb6d91bc4c9bfaef1c2ef\` | 926.540 | \`b2fdb6dc3213137e98e0ed298402e1d4b02198ed5310f264780bd8e965246b08\` | 10 Nov 2026 11:23:01 |
| [#40474891838 / #12720127454](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474891838) | \`6d332244607298154c51fbd3f16ff7718483e6b2\` | 3.201 | \`bcbfcd77a532ce34334ed60f720fdeaac566308bf2e6e4d54a7e60f28a5f083b\` | 10 Nov 2026 15:38:42 |
| [#40484548650 / #12724961702](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650) | \`8326c07f71caeab12924133b0812ec7e86b8b1f7\` | 3.960 | \`27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71\` | 10 Nov 2026 17:00:43 |
| [#40485987817 / #12724933081](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817) | \`e1e346e707254ad617a6cccad43689df908801a6\` | 4.003 | \`74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6\` | 10 Nov 2026 17:08:44 |
| [#40474262267 / #12719024236](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267) | \`653ada12cbf29a3bffad5aba91b16ecf8b90ce77\` | 2.187.882 | \`cec3404b38afbedbae151fc15e9ec66d9c019ff853e4703f8813acac7793bdf4\` | 10 Nov 2026 15:34:07 |

API metadata checked IDs, names, run mapping, sizes, digests and expiry for the listed existing artifacts; the recent Step 6 ZIP's local SHA-256 and member list were also checked directly. Runner cleanup PASS is reported for scan/audit and the historic runtime jobs that carried it; this audit did not download old private screenshot artifacts or replay their cleanup. A hash proves byte identity only, not program/game semantics.

## Hitungan status (17 baris kriteria)

- **TUNTAS: 4** — 5) dalam cakupan empat fungsi, 6(a) inventory decoded-view direct operands, 9(a) fungsi RNG terisolasi, 10) matriks audit saja.
- **SEBAGIAN: 8** — 4(a–e), 6(c), 7(a), 8(a).
- **UNKNOWN: 3** — 6(d), 8(b), 9(b).
- **BLOCKED: 2** — 6(b), 7(b).
- **HIPOTESIS: 0** — hipotesis dicantumkan pada klaim/base tertentu, bukan dipromosikan menjadi penutupan kriteria.

Total 17 baris. Status tingkat langkah: Step 4 SEBAGIAN; Step 5 TUNTAS hanya untuk empat fungsi; Step 6 tetap parsial dengan subkriteria BLOCKED/UNKNOWN; Step 7 SEBAGIAN/BLOCKED; Step 8 SEBAGIAN/UNKNOWN; Step 9 hanya satu rutin TUNTAS, cakupan lebih luas UNKNOWN; Step 10 matriks saja TUNTAS.

## Batas tugas dan kesimpulan

Tidak ada emulator/game dijalankan, input gameplay dikirim, savestate direstore, atau adaptive-player code diubah. Tidak ada ROM/BIN/CUE, BIOS, executable, Memory Card, savestate, RAM dump atau screenshot yang di-commit. Hasil terpenting audit ini adalah koreksi batas cakupan inventory dan chain dataflow statis; tidak ada penamaan semantik gameplay baru.

**Langkah 4–10 belum tuntas seluruhnya. Story Mode: TIDAK TERBUKTI TAMAT.**