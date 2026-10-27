## LIVE ACTIONS REVISION — 27 Oktober 2026 21:54:52 WIB

[Run #40520635663](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40520635663) is completed/success overall, but the downloaded artifact #12743796502 (2.299.302 B, ZIP SHA-256 `e2d5b496b2310c17110c59710212f7605bf8b3d90b798abb438c1224bf3d0549`) shows **Ghidra resource entry-0 analysis timed out at 1,800 seconds**. It exported 36 index rows while logging many function-body overlap/repair errors; candidate `0x800BDBFC` has zero recorded xrefs. Overall workflow success means outputs/cleanup completed, not that entry-0 analysis fully completed.

Run [#40521141039](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521141039) is still in progress at the latest poll. Entry1 step completed, entry0 analysis active, artifact/upload pending. Previous same-workflow run took 31m27s and entry0 hit the 1,800-second timeout; estimate for the active run is roughly 22:25–22:35 WIB only if the stage duration is similar. This is not guaranteed. Do not start another concurrent scan.

---

## CORRECTION — pointer load cross-check from raw MIPS, 27 Oktober 2026 21:43 WIB

The raw body at `0x800ED920–0x800ED924` executes `lui v1,%hi(D_8013EA74)` then `lw a0,%lo(D_8013EA74)(v1)`: it loads a value from the global slot at `0x8013EA74`, and uses that loaded value as the base after adding `index * 0x90`. Ghidra C reflects the dereference as `iRam8013ea74`; m2c renders the symbol in pointer arithmetic without the same dereference clearly expressed. Thus the boundary and call-structure comparison passes, but exact global pointer typing/effective-address agreement does not. The loaded pointer value, runtime resource base and the meaning of the record remain unknown.

---

## LIVE RECONCILIATION ADDENDUM — 27 Oktober 2026, 21:41 WIB

HEAD sebelum update dokumentasi: `c36b7407631291afd2a4d303f49a8b03392e2bbc`. Snapshot historis di bawah bagian ini tidak boleh mengalahkan run/artifact berikut.

### Step 4 — RNG entry 0/1
- [Run context entry 0 #40521136060](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521136060) success, artifact #12742056745 (5.396 B, ZIP SHA-256 `8b7fb1abfe4371c460ddc6f163295bde1ea4b6025c2ecb3fe2550b3504e477f3`). [Entry 1 #40521136038](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40521136038) success, artifact #12741592577 (15.016 B, ZIP SHA-256 `8f90959c601067480d5718eba6a6f1c819b08c37ac57e8667551dedd9febc1f4`). Hanya jendela lokal didisassemble; boundary caller belum tervalidasi.
- Callsite `0x800AF2AC` ialah direct JAL ke `0x80035DA8`; delay slot `move a0,v0` di `0x800AF2B0` meneruskan return helper `0x80037138` menjadi argumen setter. `li a0,-1` pada delay slot sebelumnya adalah argumen helper, bukan nilai yang langsung ditetapkan sebagai seed.
- Nilai return helper/seed runtime tetap UNKNOWN. Candidate base entry 0 `0x800AD000` dan entry 1 `0x800D0000` tetap hipotesis.

### Step 5 — perbandingan entry 1
[Run #40523020556](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40523020556) completed/success pada 21:40:45 WIB; artifact #12742268706 (1.367.605 B; ZIP SHA-256 `5f3f767667444f7c956c36fc59cf75b6bb90a5a1dde8ddb92fb69f9e0f797e81`). Ghidra memvalidasi function entry `0x800ED8C8`, body 160 byte sampai end-exclusive `0x800ED968); direct RNG call `0x800ED8E4`; Ghidra decompilation sukses, m2c exit 0 dan menghasilkan 17 baris C dibanding 13 baris Ghidra. Kedua output menunjukkan call `0x800CB4B4` dan `0x80035D78`. Artefak text/C/disassembly/log saja dan cleanup berhasil.
- Struktur fungsi: input di-mask 16-bit; hasil awal byte rendah helper; RNG modulo 250 dibandingkan byte pada tabel yang diindeks `index*0x90+0x29); kondisi remainder >= byte mengembalikan `0xFF`, selain itu byte helper. Feature identity dan runtime pointer/table tetap UNKNOWN; jangan melabelinya roulette/battle tanpa caller/effect evidence.
- Percobaan #40521830977 gagal karena project directory belum ada; #40522317571 parse body-size salah; #40522919529 regex tidak menangkap ukuran. Hanya #40523020556 yang lulus full perbandingan.

### Step 6 — CFG/SSA
[Run #40522772847](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40522772847) completed/success pukul 21:38:32 WIB; artifact #12741234990 (234.210 B; ZIP SHA-256 `7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9`). Fungsi `0x8012C544` dan `0x8012CACC` terkonfirmasi function entry pada view entry 1 dengan base hipotesis. Fungsi pertama punya 88 P-code ops (7 offset-constant match); fungsi kedua 47 ops (2 match). Report detail: [Step 6 CFG/SSA](STEP6_CFG_SSA_DATAFLOW_AUDIT_2026-10-27.md).
- `0x8012C544` mendukung init guard `+0xA1C), clear beberapa field termasuk `+0xB44), helper call `0x80012AC0`, store byte ke `+0xB2E/+0xB2F), set `+0xB4A=0x1E), read `+0xB30/+0xB38), add lalu write `+0xB40`, clear `+0xB2A), set guard 1. Field labels belum diketahui.
- SSA menunjukkan branch/merge/effective address untuk consumer `+0xB44), tetapi pointer global `0x8013A554` dan alias cross-function belum resolve. Status 6(a) SEBAGIAN, 6(b) BLOCKED, 6(c) SEBAGIAN, 6(d) UNKNOWN.

### Kriteria Langkah 4–10 — status aktual
| Langkah | Status | Bukti yang ditutup | Belum terbukti |
|---|---|---|---|
| 4 RNG/lifecycle | **SEBAGIAN** | Formula, state/output, 7/7 vector tests; bounded contexts baru | Seed boot, caller boundaries lengkap, reachability, roulette/battle causality, indirect/alternative RNG |
| 5 Ghidra/m2c | **SEBAGIAN** | 13 main-EXE funcs dan 1 candidate entry-1 function same-boundary cross-check | Cakupan fungsi/transition/compare dan callgraph lengkap; `0x80012A70` bukan function-entry valid di view yang dilaporkan |
| 6 xref/pointer/alias | **SEBAGIAN** | read `+B30/+B38`→sum→write `+B40`, SSA/CFG dua fungsi | Pointer runtime, alias lintas branch/callee, field semantics |
| 7 loader/resource | **SEBAGIAN** | Struktur direktori dan bootstrap copy statis | Destination/length/checksum runtime, relocation, resource lifecycle, DATA2/DUMMY mappings |
| 8 aturan/gameplay | **SEBAGIAN** | Perilaku control-flow fungsi `0x800ED8C8` dijelaskan | Identity feature, costs, barrier/upgrade, cards, turns, victory/loss |
| 9 tests | **SEBAGIAN keseluruhan** | RNG 7/7; accessor setter/getter 16/16; cleanup PASS | Test oracle untuk fungsi lain dan seluruh gameplay |
| 10 audit closure | **TUNTAS hanya sebagai matriks dokumentasi** | Matriks per-langkah, evidence, artifact, limitation, blockers direkonsiliasi | Tidak menyatakan riset reverse engineering atau game seluruhnya selesai |

Pemain otomatis tidak dijalankan selama sesi ini; tidak ada input gameplay, restore savestate, sesi emulator/gameplay ataupun perubahan adaptive player/runner/classifier/policy/readiness gate. Tidak ada aset privat game di Git/artifact. **Story Mode TIDAK TERBUKTI TAMAT.**

---

# Rekonsiliasi live reverse engineering Langkah 4–10 — 27 Oktober 2026

## Step 4/7 — latest Ghidra resource entry-0 result (27 Oktober 2026, 21:07 WIB)

Static-analysis run [#40512917437](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40512917437) **completed/success** at 21:07:13 WIB; the job's 17 steps all completed successfully, including temporary-input cleanup. Text-only artifact [#12738984684](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40512917437/artifacts/12738984684) is 1,720,881 bytes; local SHA-256 matches the API digest `fe83d2edcb1c22a9ef1f6d7193dff799aff0512286b0bf3fdb1caea68c6576e0`. The ZIP contains 22 files ending in text/log/TSV outputs only; no game binary, BIOS, save, RAM dump or screenshot is included. Main executable index reports 1,206 function rows, candidate entry-1 index 1,555 rows, and candidate entry-0 index 38 rows.

### Actual entry-0 observations (still a static candidate mapping)

- DATA.BIN entry 0 identity: file offset `0x5F800`, 110,536 bytes, SHA-256 `56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4`. Candidate base `0x800AD000) remains **NOT runtime validated**.
- Candidate helper address `0x800BDBFC) lies at entry-0-relative offset `0x10BFC) under that hypothesis. Ghidra indexed 38 function rows. It records a jump instruction at the address, and its computed C block/reference context is not a proven runtime call contract; the report explicitly says interpretation static candidate only. `reference_count=0` for this helper in this Ghidra view.
- Entry-0 target scan (`0x80035D78`, `0x80035DA8`) scanned 27,586 aligned words, with 5 raw JAL candidates and 3 decoded direct callsites. `0x800AF2AC → 0x80035DA8` is a Ghidra-validated direct JAL, but the caller function is UNMAPPED. RNG callsites `0x800BB2D8) and `0x800BB2FC) are decoded direct JALs to `0x80035D78), also with caller functions UNMAPPED. `0x800BB748) and `0x800BB770) are raw word matches only; their instructions were not decoded. `unique_validated_caller_functions_with_boundary=0` and no detailed caller decompilation was emitted.
- This improves the static inventory for Step 4(a/c) but still cannot prove the candidate entry's runtime base, whether the sites execute, full caller function boundaries, runtime seed value, or in-game randomness effects. Keep Step 4 overall **SEBAGIAN** and seed lifecycle/indirect paths **UNKNOWN**; do not call this a seed-runtime proof.
- This run supersedes any earlier statement that #40512917437 is still in progress. At the current checkpoint there are **zero Actions runs queued and zero in progress**. No adaptive-player workflow, gameplay input, emulator session or savestate restore was used.


## Snapshot kerja terbaru — 27 Oktober 2026, 21:02 WIB

### Langkah 5 — cross-check dekompilasi

Run [#40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524) selesai **completed/success** pada 20:50:53 WIB. Artefak teks [#12739676233](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524/artifacts/12739676233), 941.176 byte, SHA-256 ZIP `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d`. Validasi lokal mencocokkan digest API. Hasil report yang benar-benar tercatat: `metadata_parser_fixture=PASS`, `function_metadata=PASS`, `functions_requested=13`, `functions_with_m2c_output=13`, overall `status=SUCCESS`; semua m2c exit code 0, semua 13 pasangan C nonempty. Artifact hanya C/disassembly/log teks dan tidak memiliki binary game/BIOS/save/RAM/screenshot; cleanup runner sukses.

Cakupan 13 fungsi: 4 caller RNG awal, setter/getter `0x8001387C`/`0x800138EC`, RNG `0x80035D78`, helper counter/timer `0x80037138`, dispatcher `0x800373F8`, initializer `0x8003755C`, reset slot `0x80037B58`, callback runner `0x80037BB0`, dan slot-clear `0x80037C48`. **Step 5 overall masih SEBAGIAN**: fungsi candidate di DATA.BIN entry 0/1, fungsi pembanding/transisi dan keseluruhan caller/callee belum dicakup m2c secara lengkap. Target `0x80012A70` tidak ditemukan sebagai function entry dengan body di view Ghidra run pertama (#40512956924), sehingga alamat itu tidak dihitung sebagai fungsi cross-checked; identitas exact target tetap provisional.

### Langkah 6 — penelusuran pointer

Run static scan [#40511758146](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40511758146) sukses 20:25:48 WIB. Artifact #12737611770: 229.233 byte, ZIP SHA-256 `b84ff017cdbefb8ece6d04a7c8bef66b3fdc27b61412e91e10cc01485225b126`; 6 berkas teks/log, `private_binary_in_artifact=no`, cleanup PASS. Fixture parser displacement dan fixture konstanta `lui/ori/addiu/sign-extension` lulus.

Dalam 98.357 instruksi Ghidra-terdekode pada view kandidat entry-1, hasil utama tetap: `lw +0xB30` dan `lw +0xB38` → `addu` → `sw +0xB40`; `+0xB44` di-zero-kan pada satu jalur dan dibaca ke `a2` sebelum call candidate `0x8001B364` pada jalur lain. Trace base pada `0x8012C628` membaca `lw a0,-0x5AAC(s0)`, tetapi sumber `s0` tidak dapat dibuktikan melewati control-flow boundary; trace `v1` untuk `+0xB44` berhenti di branch `0x8012CAF8`. Base `0x800D0000` masih HIPOTESIS. Status: 6(a) SEBAGIAN, 6(b) BLOCKED, 6(c) SEBAGIAN, 6(d) UNKNOWN. Laporan: [Step 6 provenance](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/blob/main/docs/STEP6_REGISTER_PROVENANCE_AUDIT_2026-10-27.md).

### Langkah 4 dan 8 — arti fungsi yang makin terpetakan, aturan tetap terbuka

Cross-check 13 fungsi mendukung bahwa `0x80037138` dapat mengembalikan global `0x80066E7C` pada argumen negatif, mengembalikan delta timer 16-bit pada argumen `1`, atau berinteraksi dengan `0x800372B0` pada jalur lain. `0x80037B58` mereset global dan membersihkan delapan callback slot; `0x80037BB0` menaikkan global dan menjalankan callback nonzero. Ini mendukung deskripsi callback/tick-counter **secara statis**, bukan penghitung giliran atau seed boot yang telah dibuktikan pada runtime.

Setter `0x8001387C` menerima indeks 0–3, membatasi nilai ke −9999…99999, dan menulis per-peserta slot; getter `0x800138EC` membaca slot tersebut dan mengembalikan 0 untuk indeks invalid. Ini belum membuktikan formula biaya/refund atau efek mekanika tertentu. **Step 4 dan Step 8 tetap SEBAGIAN**; seed/runtime reachability, cost/barrier/upgrade, battle/roulette/turn, efek kartu, dan syarat menang/kalah tetap HIPOTESIS/UNKNOWN sesuai bukti.

### Langkah 9 — hasil terisolasi final

Run [#40516755810](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40516755810) berstatus **completed/success** pada 21:02:36 WIB. Job #122232466902 menyelesaikan semua 11 langkah dengan success; log terkonfirmasi berisi `STEP9_ALL_TESTS=PASS`, `STEP9_PRIVATE_CLEANUP=PASS` dan artefak teks [#12740305973](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40516755810/artifacts/12740305973). Artefak 4.567 byte, SHA-256 ZIP `bf1a702074849b2592bfc5555a0d493b5ed86d3de0b9895a192db7fdf9f80cd4`; empat anggota hanya teks/log. Metadata sempat stale pada snapshot 21:00 tetapi kemudian terbarui; **tidak ada lagi caveat run status**.

Hasil: RNG `0x80035D78` 7/7 vektor dan setter/getter numeric accessors `0x8001387C`/`0x800138EC` 16/16. Setter mengembalikan 1 dan menulis slot valid setelah clamp ([-9999,99999]); indeks 4/`0xFFFFFFFF` mengembalikan 0 tanpa perubahan. Getter membaca 4 slot yang disiapkan dan mengembalikan 0 untuk indeks invalid. Setiap kasus kembali ke sentinel dalam ≤128 instruksi. Ini uji CPU/RAM terisolasi, bukan emulasi PS1 atau bukti biaya/barrier/turn/aturan gameplay.

### GitHub Actions yang aktif pada snapshot 20:59 WIB

- [Ghidra statis #40512917437](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40512917437): `in_progress`, mulai 20:32:30 WIB; langkah aktif “Extract and analyze DATA.BIN entry 0 for external helper”. API terakhir diperbarui 20:34:49 WIB, jadi tahap itu belum memberi indikasi progres baru selama sekitar 24 menit. Run Ghidra pembanding #40498208067 pernah memerlukan 31 menit 47 detik; perkiraan kasar berdasar durasi tersebut sekitar 21:04 WIB, tetapi **bukan ETA terjamin** karena tahapan saat ini dan aktivitas job berbeda.
- [Uji Step 9 #40516755810](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40516755810): **completed/success** pada 21:02:36 WIB; semua 11 langkah job success, cleanup PASS. Tidak perlu memicu ulang tes.
- Tidak ada run adaptif/gameplay yang dijalankan dalam pekerjaan ini. Status Story Mode: **TIDAK TERBUKTI TAMAT**.

## Checkpoint dan Actions historis — sebelum perluasan terbaru

HEAD remote `main` pra-audit: `cc81319cc00037a92a93a3e76552245dd9a9ebf7` ([commit](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/cc81319cc00037a92a93a3e76552245dd9a9ebf7)). Audit utama multi-file berada pada commit dokumentasi `a40517a5c132aebf69344a9b6eeea20a7e4ab254` ([commit](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/a40517a5c132aebf69344a9b6eeea20a7e4ab254)); perbaikan Markdown laporan diterapkan setelahnya. Snapshot API menunjukkan 0 run `in_progress` dan 0 `queued`.

Run terbaru secara keseluruhan pada snapshot adalah [#40506364365](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40506364365), workflow monitor terjadwal, `completed/success`, source SHA `cc81319cc00037a92a93a3e76552245dd9a9ebf7`, tanpa artefak. Itu hanya hasil job monitor dan bukan bukti reverse engineering/gameplay/tamat. Audit ini tidak memulai monitor tersebut atau workflow gameplay.

Run analisis terbaru yang relevan adalah [#40504640855](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504640855) (`completed/success`, source `486e2590b45efaedd7972accb4561cd647f8a711\)); runner audit berikutnya [#40504977322](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504977322) (`completed/success`, source `4ab16073f770233edffcb13ad8b489361604b64c\)). Semua langkah scan, private-work cleanup, text-only validation, artifact metadata/digest verification dan audit cleanup selesai sukses. Karena tidak ada run aktif/queued, ETA tidak berlaku.

## Temuan statis baru Langkah 6

Artifact scan [#12733854252](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504640855/artifacts/12733854252), `step6-resource-field-static-scan`, 220.128 byte, dibuat 27 Okt 2026 19:34:27 WIB, tidak expired pada API snapshot, expiry 10 Nov 2026 19:34:27 WIB, ZIP SHA-256 `90288a1c8b454cbdc45c75e0244d26508628ecf88bfe8e73ed88524c8cb80891`. ZIP diunduh untuk pemeriksaan lokal dan checksum cocok; enam anggota adalah teks/log saja (total uncompressed 2.034.490 byte). Tidak ditemukan disc image, executable game, BIOS, Memory Card, savestate, RAM dump atau screenshot di dalam ZIP. [Runner audit artifact #12734840847](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504977322/artifacts/12734840847), 25.756 byte, expiry 10 Nov 2026 19:35:46 WIB, SHA-256 `d022b23548fe95eb34bfbb7a7fb0dd190a498ca54fff11516818138701920398`; API metadata dan digest diaudit runner, cleanup PASS.

Parser independen atas `field-offset-scan.txt` (1.933.583 byte, 41.496 baris) menghasilkan 2.104 displacement unik dan 31.081 akses base+displacement langsung dalam 98.357 instruksi terdekode (19.366 reads, 11.715 writes). Seluruh baris inventaris agregat berada di antara marker BEGIN/END dan di bawah batas emitter 30.001 baris. Ini menuntaskan inventaris agregat **untuk integer/coprocessor load-store yang dikenali, didekode Ghidra dan memakai syntax displacement(base) dalam view entry-1 kandidat**; bukan semua bentuk akses memori di program.

Base `0x800D0000` tetap HIPOTESIS, bukan base RAM runtime yang terverifikasi. Dataflow operand prioritas yang baru cross-check:
- `0x8012C634 lw v0,0xB30(a0)`, bytes `30 0B 82 8C`, membaca `+0xB30` (1 read, 0 write dalam inventory).
- `0x8012C638 lw v1,0xB38(a0)`, bytes `38 0B 83 8C`, membaca `+0xB38` (1 read, 0 write).
- `0x8012C640 addu v0,v0,v1`, bytes `21 10 43 00`; `0x8012C644 sw v0,0xB40(a0)`, bytes `40 0B 82 AC`. Jadi yang terbukti statis adalah load dua nilai, menjumlahkan, lalu menyimpan hasil ke `+0xB40`.
- `0x8012C604 sw zero,0xB44(v0)`, bytes `44 0B 40 AC`, men-zero-kan `+0xB44` pada jalur inisialisasi kandidat `0x8012C544`.
- `0x8012CB14 lw a2,0xB44(v1)`, bytes `44 0B 66 8C`, memasok nilai ke argumen `a2` sebelum call `0x8001B364` pada jalur kandidat `0x8012CACC`.
Operasi ini mendukung hubungan dataflow terbatas saja. Tidak membuktikan object identity, runtime mapping, arti field, atau aturan gameplay.

**Batas konteks per-instruksi:** inventaris agregat lengkap tidak berarti semua akses punya blok konteks lengkap. Blok `MEMORY_MATCH` dibatasi 200 per displacement umum: `+0x2E9` mempunyai 257 akses (86 read, 171 write) namun 200 konteks; `+0x22` mempunyai 275 (178 read, 97 write) namun 200 konteks. Empat offset prioritas `+0xB30/+0xB38/+0xB40/+0xB44` tidak terkena cap konteks per-offset dan seluruh konteks scan yang sesuai tersedia. Base-register trace tetap linear maksimal 24 instruksi/simple `move`, berhenti di control flow; computed pointers, indirect aliases, split immediates, alternate bases, undecode code dan boundary/P-code bermasalah masih terbuka.

Tooling sudah berubah sebelum audit ini: commit `486e2590b45efaedd7972accb4561cd647f8a711` menormalisasi mnemonic delay-slot `_` serta mengenali integer/coprocessor load-store; `4ab16073f770233edffcb13ad8b489361604b64c` menaikkan output emitter menjadi 30.001 baris. Scan terbaru sukses dan fixture parser lulus; tidak ditemukan alasan berbukti untuk patch scanner berikutnya hanya demi menambah perubahan.

## Dampak terbaru untuk semantik (Step 4 dan Step 8, 20:50 WIB)

Cross-check Ghidra/m2c [#40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524), artifact #12739676233, mendukung bahwa `0x80037138` pada argumen negatif mengembalikan `0x80066E7C`, pada argumen 1 mengembalikan delta timer 16-bit, dan pada argumen lain dapat memanggil `0x800372B0`. `0x80037B58` mereset global dan delapan callback slot; `0x80037BB0` menaikkan global serta menjalankan callback nonzero. Callsite entry-0 ke helper/setter masih memakai base `0x800AD000` hipotetis dan belum terbukti runtime, jadi tidak mengubah Step 4 dari SEBAGIAN atau membuktikan RNG seed boot.

Pasangan `0x8001387C`/`0x800138EC` berhasil dibandingkan: setter/g getter menyentuh slot nilai yang sama, setter membatasi indeks 0–3 dan nilai −9999…99999. Interpretasi konteks sebagai nilai Chakra tetap terpisah dari formula biaya/refund. Target `0x80012A70` tidak ditemukan sebagai function entry/body pada view Ghidra perluasan; label fungsi getter-target di alamat persis tersebut ditahan sebagai provisional sampai raw boundary/reference direkonsiliasi. Step 8 tetap SEBAGIAN dan aturan biaya/barrier/battle/turn/kartu/kemenangan masih UNKNOWN.

## Matriks kriteria Langkah 4–10

| Kriteria | Status | Bukti utama | Celah dan syarat penerimaan yang belum dipenuhi |
|---|---|---|---|

| 4(a) Generator/state/origin dan lifecycle seed | **SEBAGIAN** | Fungsi LCG main EXE `0x80035D78`, state `0x800A3118`, formula `(old × 0x41C64E6D + 0x3039) mod 2^32` dan output `(new >> 16) & 0x7FFF`; fungsi `0x80037138` pada argumen negatif mengembalikan counter `0x80066E7C`; `0x80037B58` reset counter/callback slots dan `0x80037BB0` increment/callback; Ghidra/m2c cross-check #40515356524. | Nilai counter saat boot, urutan initializer/callsite, dan nilai runtime pada setter kandidat `0x80035DA8` belum terbukti. Entry-0 base `0x800AD000` masih hipotetis; probe cold boot sebelumnya tidak hit sampai frame 120. Relasi dengan RNG seed/roulette/battle masih belum terverifikasi. |
| 4(b) Determinisme dan hasil roulette tampak | **SEBAGIAN** | #40474262267, artifact #12719024236, SHA-256 ZIP `cec3404b38afbedbae151fc15e9ec66d9c019ff853e4703f8813acac7793bdf4`: 127 observasi caller/state-before ternormalisasi, final state `0xA99DC6E7\), crop viewport sama pada window itu. | Terminal capture frame 167/169/171 berbeda; belum ada hubungan kausal independen antara caller/state dan hasil roulette visual. |
| 4(c) Direct/indirect callers, JT, decompressed paths | **SEBAGIAN** | Ghidra #40498208067, audit #40503223693; 5 raw JAL entry-0 (3 decoded); 144 raw candidates entry-1 (108 decoded/50 fungsi, 36 raw-only). | Indirect/JALR/JT menyeluruh, base runtime/reachability, raw-only boundaries, dan code setelah decompress/decrypt belum tersingkir. |
| 4(d) Caller roulette dan battle | **SEBAGIAN** | Observasi roulette dan static RNG trace di laporan Step 4. | Kaitan caller-ke-hasil roulette tidak kausal; battle checkpoint/caller autentik belum ditelusuri. |
| 4(e) RNG alternatif/randomness lain | **SEBAGIAN** | Signature scan pola LCG dan caller inventory. | Signature terbatas tidak menyingkirkan tabel, frame/time, algoritme lain, indirect call atau code terdekompresi. |
| 5) Cross-check fungsi Ghidra/m2c yang diwajibkan | **SEBAGIAN (13 fungsi inti main EXE lulus)** | [#40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524), artifact #12739676233; SHA-256 ZIP `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d`; `functions_requested=13`, `functions_with_m2c_output=13`, per-function status success. | Candidate `0x80012A70` tidak merupakan function entry yang ditemukan Ghidra pada view itu; fungsi kandidat DATA.BIN entry 0/1, transisi/compare functions dan cakupan call graph belum dibandingkan secara menyeluruh. Tidak mengklaim semua executable/source asli. |
| 6(a) Census direct memory operand/RW + raw bytes dalam decoded view | **SEBAGIAN** | Scan #40511758146/artifact #12737611770: 98.357 instruksi terdekode, inventory displacement yang sama, fixture parser dan address-construction PASS; raw MIPS B30/B38 → addu → B40 serta B44 store/load dipertahankan. | Cakupan hanya instruksi recognized/decoded dalam entry-1 view; base 0x800D0000 dan pemetaan runtime belum tervalidasi, jadi census tidak membuktikan seluruh access di game. Lihat docs/STEP6_REGISTER_PROVENANCE_AUDIT_2026-10-27.md. |
| 6(b) Effective addresses, pointer aliases, split immediates, semua reader/writer dan alternate base | **BLOCKED** | Resolver baru di #40511758146 mengikuti `lui/ori/addiu/move/addu` dan operasi terbatas; fixture PASS. Namun pointer `a0` pada +B30/+B38/+B40 berasal dari `lw a0,-0x5AAC(s0)` di 0x8012C628, dan trace sumber `s0` terhenti pada control-flow boundary; trace `v1` di +B44 juga berhenti pada branch 0x8012CAF8. | Resolver hanya bounded backward linear trace dan tidak melintasi CFG/call, tidak membuktikan semua alias/reader/writer atau base aktual; unresolved branches, split address constructions, indirect pointers, undecoded bytes dan alternate bases masih terbuka. Status tetap BLOCKED. |
| 6(c) Dataflow/caller/callee yang didukung statis | **SEBAGIAN** | B30+B38→addu→B40; B44 zero-store dan read yang disalurkan ke `a2` untuk `0x8001B364`. | Seluruh caller/callee, initial/final writer dan lifecycle object belum selesai; semantik efek pada state masih belum diketahui. |
| 6(d) Nama semantik field/kode | **UNKNOWN** | Operasi statis di atas, base hipotetis. | Tidak ada bukti independen bahwa offsets bermakna Chakra, cost, barrier, turn atau level-up. Butuh caller/callee, tipe/validasi nilai dan korelasi state/output independen. |
| 7(a) Static resource directory/loader/copy | **SEBAGIAN** | DATA.BIN bootstrap + 1.504 entri; kandidat directory/copy statis, lihat laporan Step 7. | Base entry 0/1, relocation, load/unload lifecycle, DATA2.BIN/DUMMY.BIN end-to-end belum dipetakan. |
| 7(b) Runtime mapping + copy source/destination/size/checksum | **BLOCKED** | #40484548650/artifact #12724961702 (3.960 byte; SHA-256 ZIP `27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71`): no-hit `0x800AD454` s.d. frame 120, timeout 35s/exit 124, cleanup PASS. | Tidak ada register/copy-length/checksum runtime. Jangan ulang target sama; PC baru harus terlebih dahulu didukung reachability statis. |
| 8(a) Function semantics dari caller/callee/raw MIPS | **SEBAGIAN** | RNG/helper/counter, getter/setter, beberapa compare/store dan dataflow terpetakan. | Beberapa transition decompile boundaries/P-code bermasalah, dan aliran penuh state belum tersedia. Klaim harus menunjuk instruksi, branch, register dan store/call yang spesifik. |
| 8(b) Aturan aktual cost/barrier/upgrade/battle/roulette/turn/kartu/menang | **UNKNOWN** | Tidak ada label mekanika yang diasumsikan hanya dari offset/nama simbol. | Formula biaya/resource, efek kartu, giliran, win/loss per mode belum ditopang bukti independen. Jangan namai field atau aturan tanpa chain raw MIPS/dataflow dan corroboration. |
| 9(a) Eksekusi isolasi RNG `0x80035D78` | **TUNTAS, hanya fungsi ini** | #40474891838/artifact #12720127454 (3.201 byte, SHA-256 ZIP `bcbfcd77a532ce34334ed60f720fdeaac566308bf2e6e4d54a7e60f28a5f083b`): 7/7 vektor, state/`v0` cocok, sentinel 12 instruksi per vektor, limit 128, physical RAM 2 MiB. | Bukan emulator PS1 penuh; tidak menguji caller, seed, visible roulette, fungsi lain. |
| 9(b) Coverage fungsi/kondisi lain yang diwajibkan | **SEBAGIAN** | Artifact #12740305973 dari run #40516755810 menyatakan 16/16 kasus setter/getter `0x8001387C`/`0x800138EC` PASS (register v0, memory slots, return sentinel, budget ≤128 instruksi); 7/7 vektor RNG dipertahankan PASS. Digest ZIP `bf1a702074849b2592bfc5555a0d493b5ed86d3de0b9895a192db7fdf9f80cd4`. | Ini menutup hanya dua accessor di CPU/RAM terisolasi. Oracle/cakupan masih belum lengkap untuk target compare, transisi, semua caller/helper, fungsi candidate resource, dan jalur gagal lainnya. Artifact dan raw log membuktikan tes 7/7 + 16/16 PASS serta `STEP9_PRIVATE_CLEANUP=PASS`; semua 11 langkah job success. Aggregate run API masih `in_progress`, jadi run-level conclusion belum dicatat `completed/success`. |
| 10) Audit matrix: kriteria→bukti primer/run/commit/hash/status/gap | **TUNTAS sebagai proses matriks saja** | Dokumen ini dan closure report, metadata API artifact #40504640855/#40504977322. | Tidak berarti Steps 4–9 semuanya selesai; refresh saat bukti baru tersedia. |

## Inventaris artefak dan cleanup

| Run/artifact | Source SHA | Ukuran ZIP | SHA-256 ZIP (API digest) | Expiry WIB ketika diperiksa |
|---|---|---:|---|---|
| [#40504640855 / #12733854252](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504640855) | `486e2590b45efaedd7972accb4561cd647f8a711` | 220.128 | `90288a1c8b454cbdc45c75e0244d26508628ecf88bfe8e73ed88524c8cb80891` | 10 Nov 2026 19:34:27 |
| [#40504977322 / #12734840847](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40504977322) | `4ab16073f770233edffcb13ad8b489361604b64c` | 25.756 | `d022b23548fe95eb34bfbb7a7fb0dd190a498ca54fff11516818138701920398` | 10 Nov 2026 19:35:46 |
| [#40498208067 / #12732952776](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40498208067) | `dc5ad30c1ec97329e2829da33da092d1bf43f5ef` | 2.255.170 | `6d78dfc9727932dca67ec7867a35b2a83f7c02237c2d16dc7dfefb34fcf188b6` | 10 Nov 2026 19:14:36 |
| [#40449144521 / #12710000931](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40449144521) | `62a4c114b7ac7a55ae9eb6d91bc4c9bfaef1c2ef` | 926.540 | `b2fdb6dc3213137e98e0ed298402e1d4b02198ed5310f264780bd8e965246b08` | 10 Nov 2026 11:23:01 |
| [#40474891838 / #12720127454](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474891838) | `6d332244607298154c51fbd3f16ff7718483e6b2` | 3.201 | `bcbfcd77a532ce34334ed60f720fdeaac566308bf2e6e4d54a7e60f28a5f083b` | 10 Nov 2026 15:38:42 |
| [#40484548650 / #12724961702](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40484548650) | `8326c07f71caeab12924133b0812ec7e86b8b1f7` | 3.960 | `27376e9b78eca7e686843034d8d6e44587e1e2969bf6fcc93dc98d3c6cc0bc71` | 10 Nov 2026 17:00:43 |
| [#40485987817 / #12724933081](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40485987817) | `e1e346e707254ad617a6cccad43689df908801a6` | 4.003 | `74fcb5b8958ce26ab7fd1091bd7c2ee8dbfc073bb09ac9c4ca70d1a6e2a204c6` | 10 Nov 2026 17:08:44 |
| [#40474262267 / #12719024236](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267) | `653ada12cbf29a3bffad5aba91b16ecf8b90ce77` | 2.187.882 | `cec3404b38afbedbae151fc15e9ec66d9c019ff853e4703f8813acac7793bdf4` | 10 Nov 2026 15:34:07 |

API metadata checked IDs, names, run mapping, sizes, digests and expiry for the listed existing artifacts; the recent Step 6 ZIP's local SHA-256 and member list were also checked directly. Runner cleanup PASS is reported for scan/audit and the historic runtime jobs that carried it; this audit did not download old private screenshot artifacts or replay their cleanup. A hash proves byte identity only, not program/game semantics.

## Hitungan status (17 baris kriteria)

- **TUNTAS: 2** — 9(a) fungsi RNG terisolasi dan 10) matriks audit saja.
- **SEBAGIAN: 11** — 4(a–e), 5) cakupan fungsi belum lengkap meskipun 13 fungsi inti lulus, 6(a), 6(c), 7(a), 8(a), 9(b) uji terisolasi hanya dua accessor.
- **UNKNOWN: 2** — 6(d), 8(b).
- **BLOCKED: 2** — 6(b), 7(b).
- **HIPOTESIS: 0** — hipotesis dicantumkan pada klaim/base tertentu, bukan dipromosikan menjadi penutupan kriteria.

Total 17 baris. Status tingkat langkah: Step 4 SEBAGIAN; Step 5 SEBAGIAN (13 fungsi inti main EXE lulus, DATA.BIN/call graph belum lengkap); Step 6 tetap parsial dengan subkriteria BLOCKED/UNKNOWN; Step 7 SEBAGIAN/BLOCKED; Step 8 SEBAGIAN/UNKNOWN; Step 9 SEBAGIAN overall (9a RNG TUNTAS, 9b dua accessor teruji; coverage lain masih terbuka); Step 10 matriks saja TUNTAS.

## Batas tugas dan kesimpulan

Tidak ada emulator/game dijalankan, input gameplay dikirim, savestate direstore, atau adaptive-player code diubah. Tidak ada ROM/BIN/CUE, BIOS, executable, Memory Card, savestate, RAM dump atau screenshot yang di-commit. Hasil terpenting audit ini adalah koreksi batas cakupan inventory dan chain dataflow statis; tidak ada penamaan semantik gameplay baru.

**Langkah 4–10 belum tuntas seluruhnya. Story Mode: TIDAK TERBUKTI TAMAT.**