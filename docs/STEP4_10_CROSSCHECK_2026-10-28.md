# HASIL FINAL SCAN STEP 6(b) — 28 Oktober 2026, 07:55 WIB

Hasil ini menggantikan catatan sementara “scan pending” yang muncul di bawah/versi sebelumnya. Run [#40611660635](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40611660635) **completed/success** pukul 07:55:13 WIB; job `122564387469`. Artefak teks [#12783307599](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40611660635/artifacts/12783307599), 244.577 byte, SHA-256 ZIP `748eadbfe82980bba8d2088d11affba4310d524eb871b6a34ee5fd43584f2892` cocok dengan digest GitHub. Ghidra scan, cleanup aset input privat, validasi output text-only, dan upload laporan lulus; `source_assets_removed_before_ghidra=PASS`, `private_binary_uploaded=no`.

Hasil baru:
- Exact XREF statis ke alamat numerik `0x8013A554`: **194** (192 READ, 2 WRITE; 74 entry fungsi unik diketahui dan 6 sumber tidak memiliki containing function).
- Dua writer yang terdaftar: `0x80127278` dalam fungsi `0x80127240` — `_sw v0,-0x5aac(s0)`; dan `0x80127364` dalam fungsi `0x8012733c` — `sw zero,-0x5aac(s0)`.
- Heuristik displacement `0xA554`: 200 kandidat load/store, 159 memiliki kandidat `lui reg,0x8014` sebelumnya dalam jendela 24 record instruksi. Ini bukan graph alias/provenance lengkap.
- Dalam view hipotetis entry-1 base `0x800D0000`, bytes pada `0x8013A554` adalah `70 00 B0 AF` (word little-endian `0xAFB00070`), terdekode seperti `sw s0,0x70(sp)`. Ini konflik code/data mapping atau base/relocation yang belum terselesaikan, bukan bukti pointer runtime.

Karena mapping tersebut belum tervalidasi dan trace masih heuristik, **Step 6(b) tetap BLOCKED**; 6(a)/6(c) tetap SEBAGIAN, 6(d) UNKNOWN. Tidak ada status Langkah 4–9 yang dinaikkan. Story Mode **TIDAK TERBUKTI TAMAT**. Tidak ada emulator/gameplay/input/savestate restore atau adaptive-player run yang dilakukan.

Laporan lengkap: [docs/STEP6_GLOBAL_POINTER_SLOT_AUDIT_2026-10-28.md](docs/STEP6_GLOBAL_POINTER_SLOT_AUDIT_2026-10-28.md).

---

## Follow-up scan 6(b) — status sementara, 28 Oktober 2026

Run Ghidra statis [#40611660635](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40611660635) dipicu oleh perubahan alat di commit `ea148ca60af2e3eeaa1b58141532e1ff5a98dd60`, branch `main`. Status terbaru yang terlihat: `in_progress`; job `122564387469`; langkah terakhir `Install disc extraction tools` masih berjalan. Mulai pada `2026-10-28T00:53:40Z` (= 07:53:40 WIB). Belum ada artifact dan log job belum tersedia. Workflow memiliki `timeout-minutes: 35`; batas timeout sekitar 08:28:40 WIB bukan ramalan waktu selesai. Jika scan selesai, verifikasi log dan hasil XREF/pola LUI sebelum memutuskan apakah 6(b) berubah; jika gagal, simpan error dan jangan rerun identik sebelum sebab kegagalan dipahami.

Ini pemindaian kode statis saja. Tidak ada emulator/gameplay, tombol, savestate restore, adaptive player, atau upload biner privat ke artefak yang dimulai oleh perubahan ini.

---

# ADDENDUM LANJUTAN — 28 Oktober 2026

Audit artefak langsung pasca-checkpoint sebelumnya: laporan spesifik [docs/STEP4_10_TARGETED_AUDIT_2026-10-28.md](STEP4_10_TARGETED_AUDIT_2026-10-28.md). Artefak Step 5 #12739676233 dan Step 6 #12741234990 diunduh/dibuka ulang; hash ZIP cocok dengan nilai yang terdokumentasi. Tambahan yang benar-benar baru: 156 mnemonic JALR dalam main-EXE disassembly (target dinamis belum diselesaikan); perbedaan span anotasi `nonmatching` spimdisasm versus body Ghidra untuk `0x80015B7C`; dan direct operand counts terdekode pada view entry-1: +B30 1 READ, +B38 1 READ, +B40 1 WRITE, +B44 1 WRITE + 1 READ. Itu memperjelas coverage lokal tetapi tidak menutup caller graph, effective address, alias/pointer chain atau semantics runtime.

Matriks 17 kriteria tetap sebagaimana status di bawah: Step 4–9 belum memperoleh closure global; 6(b) dan 7(b) BLOCKED; arti field dan aturan gameplay unsupported tetap UNKNOWN; Step 10 TUNTAS sebagai matriks saja. Tidak ada emulasi/gameplay/input/restore dilakukan dan Story Mode TIDAK TERBUKTI TAMAT.

---

# Cross-check Bukti Riset Reverse Engineering — Langkah 4–10
Tanggal: 28 Oktober 2026 (checkpoint sesudah pembaruan 07:06 WIB)
Repositori diizinkan: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research
Parent/checkpoint yang diaudit: https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/7df287bf4ca21f6c32fe2589bc09e8665e62e846
Cakupan sesi: audit statis dan tes CPU/MIPS terisolasi; bukan sesi gameplay.

## Ringkasan keputusan

Audit ini memakai tiga artefak yang benar-benar diunduh/dibuka dalam sesi dan hash-nya cocok dengan catatan repo: keluaran Ghidra/m2c disassembly main EXE, scan field resource DATA.BIN entry 1, dan hasil tes Unicorn Langkah 9. Tidak ada dasar untuk menaikkan status global Langkah 4–9. Langkah 10 tetap tuntas hanya sebagai matriks audit. Story Mode TIDAK TERBUKTI TAMAT.

Temuan yang berhasil dipersempit:
1. Full main-EXE disassembly dalam artefak Step 5 berisi tepat empat instruksi direct JAL ke RNG 0x80035D78: 0x80015B14, 0x80015BF0, 0x8001A460, 0x80020C24. Ini menghitung pemanggilan langsung pada rentang main EXE yang diperiksa, bukan pemanggilan tidak langsung, pemanggil resource, atau reachability gameplay.
2. Pada view Ghidra hipotetis DATA.BIN entry 1, +0xB30 dan +0xB38 dibaca, dijumlahkan, lalu hasilnya ditulis ke +0xB40. +0xB44 diinisialisasi nol dan pada branch lain dibaca sebagai argumen ke 0x8001B364 ketika byte +0xB2A >= 6. Jalur helper kemudian menuju 0x8001B39C dengan tabel dan operasi yang konsisten dengan pengolahan geometri/visual. Arti gameplay field tetap UNKNOWN.
3. Step 9 run #40606159061 mengonfirmasi 7/7 vektor RNG, 8/8 kasus helper negatif-a0, dan 16/16 kasus setter/getter pada CPU/MIPS terisolasi. MMIO menggunakan fixture sintetis konstan, bukan timer PS1.

## Bukti yang dibuka dan diverifikasi

| Sumber | Identitas | Pemeriksaan | Kesimpulan yang didukung |
|---|---|---|---|
| Step 5, run #40515356524, artifact #12739676233 | 941.176 byte; SHA-256 ZIP 94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d | ZIP dibuka; 45 file teks/C/disassembly/log termasuk disassembly main EXE; tidak ada biner game dalam artefak | 13 fungsi terpilih menghasilkan keluaran Ghidra/m2c; direct JAL RNG dapat dihitung dari disassembly lengkap |
| Step 6, run #40522772847, artifact #12741234990 | SHA-256 ZIP 7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9 | ZIP dibuka; teks/log; scanner melaporkan 98.357 instruksi decoded di view entry 1; input privat dihapus sebelum keluaran | Hubungan operand dan field dalam view hipotetis, bukan pemetaan RAM runtime |
| Step 9, run #40606159061, artifact #12779814671 | 5.377 byte; SHA-256 ZIP dd3e559997ce0c9f931f330144de8021bdb3c75fa16b4f21717299c4b2d4d79f | ZIP dibuka; empat file teks/log; hasil tes dan cleanup dibaca | Tes fungsi spesifik dalam model CPU/MIPS saja, bukan emulasi PS1/gameplay |

Identitas executable pada artefak Step 5: SLPS_035.53, 385.024 byte, SHA-256 a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569. Disassembly menggunakan offset file 0x800, base teks 0x80010000 dan rentang 0x5D800 byte; spimdisasm exit 0. Kata instruksi 5ED7000C (JAL target RNG) muncul tepat empat kali pada file disassembly yang diperiksa.

## Bukti runtime historis: referensi saja pada sesi ini

| Referensi | Hasil historis yang tertulis | Cara dipakai dalam audit |
|---|---|---|
| Step 4 roulette #40474262267, artifact #12719024236 | 127 sampel caller/state setelah normalisasi; state akhir 0xA99DC6E7; frame terminal berbeda 167/169/171 | Referensi dokumentasi/hash saja. Isi artifact gambar tidak diunduh/dibuka. Causality antara caller dan hasil roulette belum terbukti |
| Step 7 coldboot #40484548650, artifact #12724961702 | Cold boot bounded tanpa input/restore; breakpoint 0x800AD454 tidak hit sampai frame 120; exit 124 pada batas 35 detik; cleanup PASS | Hasil log telah dicatat di laporan terdahulu; artifact tidak diunduh saat sesi ini. No-hit dalam satu jendela bukan bukti bahwa instruksi tidak pernah berjalan |
| Step 4 setter probe #40485987817 | Kandidat setter 0x80035DA8 tidak hit sampai frame 120; exit 124 pada batas 35 detik | Referensi dokumen saja; bukan bukti setter tidak digunakan di jalur lain |
| Dialog diagnostic #39565014834, artifact #12329546573 | Metadata mencatat nama artifact naruto-storymode-dialog-freeze-diagnostic-private, ukuran 7.101.006 byte dan run gagal | Isi artifact tidak diunduh/dibuka, tidak dipakai sebagai bukti gameplay. Kelola artefak privat melalui proses runner yang terkendali sesuai aturan proyek |
| Adaptive regression #40071317759 dan monitor #40596433514 | Job regression/monitor sukses | CI/monitor success bukan bukti gameplay maju atau Story Mode tamat |

Dokumen dan handoff lama memuat referensi ke screenshot gameplay autentik, checkpoint/savestate dan restore lintas-run. File mentah tersebut tidak dibuka dalam sesi ini; referensi/hash yang tercatat tidak dianggap sebagai pengganti pemeriksaan isi. Tidak ada screenshot tiruan atau gambar dari web yang digunakan sebagai bukti gameplay. Tidak ada klaim baru bahwa savestate tertentu telah dibuka pada sesi ini.

## Temuan statis

### Langkah 4–5 — RNG dan caller

Rutin 0x80035D78 memperbarui global 0x800A3118 dengan:
- new_state = (old_state * 0x41C64E6D + 0x3039) mod 2^32
- output = (new_state >> 16) & 0x7FFF

Direct JAL sites dalam main EXE:
- 0x80015B14 di fungsi 0x80015ADC: RNG dipakai untuk argumen/indeks terbatas dalam pembuatan daftar.
- 0x80015BF0 di fungsi 0x80015B7C: RNG memilih indeks kedua untuk pertukaran byte berulang. Buffer belum diberi arti gameplay.
- 0x8001A460 di fungsi 0x8001A328: setelah pemeriksaan kode/kandidat 0x7F–0x86, memilih RNG modulo count dan menyimpan kandidat ke global 0x80089DA9.
- 0x80020C24 di fungsi 0x80020BF4: setelah guard objek lolos, menyimpan RNG modulo 0x1000 ke offset objek +0x34.

Helper 0x80037138 pada a0 < 0 mengembalikan global 0x80066E7C. Dalam kandidat entry 0, 0x800AF2A4 memanggil helper dengan a0=-1, dan 0x800AF2AC memanggil setter kandidat 0x80035DA8 dengan hasil helper dalam delay slot. Alur ini bersifat statis dan bergantung pada base entry 0 0x800AD000 yang belum diverifikasi. Jangan menyebutnya seed boot/lifecycle RNG runtime.

### Langkah 6 — struktur field

Pada fungsi kandidat entry-1 0x8012C544:
- 0x8012C634 membaca word +0xB30.
- 0x8012C638 membaca word +0xB38.
- 0x8012C640 menjumlahkan nilai.
- 0x8012C644 menulis hasil ke +0xB40.
- 0x8012C604 mengosongkan +0xB44 pada cabang inisialisasi.

Pada fungsi kandidat 0x8012CACC, kondisi 0x8012CAF4–0x8012CAF8 melewati consumer jika byte +0xB2A < 6. Pada jalur yang lolos, 0x8012CB14 memuat +0xB44 ke a2 dan 0x8012CB18 memanggil 0x8001B364 dengan a3=5 pada delay slot. Wrapper 0x8001B364 menuju 0x8001B39C, yang menggunakan tabel dan operasi konsisten dengan pengolahan geometri/visual. Ini membuktikan aliran argumen dalam view statis, bukan arti gameplay field.

Batas: base entry-1 0x800D0000 hipotesis; pointer object berasal dari global slot 0x8013A554 yang nilai runtime-nya belum dilihat; scanner mempunyai trace linear terbatas. Tidak terbukti bahwa field mana pun adalah biaya Chakra, giliran, barrier, atau upgrade.

### Langkah 9 — tes terisolasi dan kegagalan sebelumnya

Run #40606159061:
- RNG 0x80035D78: 7/7 vektor.
- Helper 0x80037138 jalur a0 negatif: 8/8 kasus, input 0xFFFFFFFF dan 0x80000000 pada nilai global sintetis 0, 1, 0x12345678, 0xFFFFFFFF.
- Setter/getter 0x8001387C/0x800138EC: 16/16 kasus, termasuk clamp dan indeks tak valid.
- STEP9_TESTS=PASS, STEP9_PRIVATE_CLEANUP=PASS.

Alamat MMIO yang dirujuk helper dipetakan menjadi word tetap 0x12345678. Ini bukan timer PS1. Riwayat kegagalan: #40605560982 gagal pada SyntaxError sebelum helper diuji; #40605654394 berhenti karena MMIO belum dipetakan; #40605904131 lulus tes namun tabel hasil mengandung kolom duplikat. #40606159061 memperbaiki fixture dan format. Jangan ulangi tes yang sama tanpa kasus baru yang menjawab gap.

## Matriks 17 kriteria

| Kriteria | Status sebelum | Status sesudah | Bukti dan gap |
|---|---|---|---|
| 4(a) RNG state dan seed lifecycle | SEBAGIAN | SEBAGIAN | Rumus/7 vektor dan helper-counter statis; base/reachability entry 0, nilai seed runtime, urutan init/setter dan lifecycle belum terbukti |
| 4(b) Determinisme dan hasil terlihat | SEBAGIAN | SEBAGIAN | 127 sampel historis; perlu state-start terkendali yang mengikat caller/state ke outcome independen |
| 4(c) Direct/indirect callers | SEBAGIAN | SEBAGIAN | Empat JAL langsung main EXE dihitung; indirect/JALR/jump table/resource/decompressed path dan reachability runtime belum tertutup |
| 4(d) Roulette/battle callers | SEBAGIAN; battle BLOCKED | SEBAGIAN; battle BLOCKED | Caller roulette belum kausal; perlu checkpoint battle autentik dan trace caller/state |
| 4(e) Alternatif randomness | SEBAGIAN | SEBAGIAN | Scan signature tak menyingkirkan RNG/tabel/timer/caller tidak langsung/resource lain |
| 5 Cross-check Ghidra/m2c | SEBAGIAN | SEBAGIAN | 13 fungsi main EXE + satu kandidat resource; bukan cakupan seluruh fungsi/call graph/transition |
| 6(a) Census direct memory R/W | SEBAGIAN | SEBAGIAN | 98.357 instruksi decoded pada view hipotesis; B30/B38→sum→B40 dan B44 access. Bukan seluruh akses runtime |
| 6(b) Effective address/pointer/alias | BLOCKED | BLOCKED | Nilai global 0x8013A554, alias lintas branch/callee, split immediates dan alternate base belum terselesaikan |
| 6(c) Dataflow menuju semantik | SEBAGIAN | SEBAGIAN | B44 mencapai helper geometri/visual-like; identitas object, writer dan efek state/game belum terbukti |
| 6(d) Nama/arti field | UNKNOWN | UNKNOWN | Belum ada bukti independen tentang arti B30/B38/B40/B44 |
| 7(a) Static resource/loader | SEBAGIAN | SEBAGIAN | Direktori DATA.BIN terdokumentasi; destination/length/relocation/lifecycle dan DATA2.BIN/DUMMY.BIN belum lengkap |
| 7(b) Runtime mapping/copy | BLOCKED | BLOCKED | Probe 0x800AD454 no-hit sampai frame 120; butuh target copy yang dibenarkan statis dan bukti source/dest/length/checksum |
| 8(a) Semantik operasi terpilih | SEBAGIAN | SEBAGIAN | Operasi caller dan threshold tercatat; base/pointer dan efek aktual belum tervalidasi |
| 8(b) Aturan game | UNKNOWN untuk label yang tak didukung | UNKNOWN | Perlu code flow kondisi→store→hasil plus bukti runtime autentik per biaya/barrier/kartu/battle/turn/menang-kalah |
| 9(a) Tes RNG terisolasi | TUNTAS, hanya 7 vektor | TUNTAS, hanya 7 vektor | #40606159061: 7/7; jangan generalisasikan ke fungsi/hardware/gameplay lain |
| 9(b) Tes helper/accessor dan breadth | SEBAGIAN | SEBAGIAN | 8/8 helper dan 16/16 accessor dalam model; breadth fungsi/gameplay/PS1 belum diuji |
| 10 Audit closure per-kriteria | TUNTAS hanya matriks | TUNTAS hanya matriks | Bukti/status/gap diindeks; bukan klaim seluruh riset atau game sudah selesai |

## Tindakan berikut yang paling bernilai

1. Step 4/5: definisikan batas caller entry-0 yang belum tervalidasi dan petakan direct/indirect references ke 0x35D78, 0x35DA8, global 0x800A3118 serta 0x80066E7C. Jangan gunakan 0x800BDBFC sebagai helper yang tervalidasi: analisis entry 0 timeout dan kandidat itu tidak punya xref tercatat.
2. Step 6: lanjutkan trace CFG-aware dari global 0x8013A554 ke pointer objek dan field B30/B38/B40/B44, merekam dengan eksplisit saat provenance menjadi unknown.
3. Step 7: jangan ulang probe 0x800AD454. Probe non-gameplay hanya bila instruksi copy yang dapat dijangkau telah dipilih dari bukti statis; jika tidak, pertahankan BLOCKED.
4. Step 8: jangan memberi label gameplay sampai caller/callee/dataflow dan bukti state/result autentik independen saling menguatkan.
5. Step 9: jangan ulang tes sama; tambah tes hanya untuk gap dengan oracle eksplisit, dan pisahkan model MMIO sintetis dari klaim perangkat keras nyata.
6. Story Mode/readiness: jangan ubah player, classifier, Revision65 marker atau readiness gate. Target cue UNKNOWN, barrier_level_selection=WAIT, readiness NO-GO, Story Mode NOT COMPLETE. Restore savestate atau input gameplay memerlukan izin baru yang eksplisit dan spesifik karena gate terdahulu.

Tidak ada teks Jepang baru yang dikutip; jika muncul dalam laporan mendatang, sertakan terjemahan Bahasa Indonesia di dekat teks asli.
