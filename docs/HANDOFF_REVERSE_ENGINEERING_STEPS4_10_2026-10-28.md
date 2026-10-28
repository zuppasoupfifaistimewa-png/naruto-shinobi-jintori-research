# HANDOFF ADDENDUM — targeted audit 28 Oktober 2026

Checkpoint ini menambahkan [audit terarah Step 4–10](STEP4_10_TARGETED_AUDIT_2026-10-28.md). Awal sesi membaca HEAD `4b20564b38c895495755143b2aa777dc7ab6b5e5` pada `main`; sesudah audit dokumen diperbarui, periksa HEAD live sebelum tindakan berikutnya. Actions `queued=0`, `in_progress=0` pada query API; run #40606159061 sudah selesai.

### Bukti baru yang dapat digunakan

- Step 5 artifact #12739676233 SHA-256 ZIP `94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d` dibuka langsung: empat direct JAL ke RNG pada main EXE tetap terkonfirmasi; disassembly mempunyai 156 mnemonic JALR, tetapi target dinamis belum dipetakan.
- Ada perbedaan batas yang harus diselesaikan sebelum klaim cakupan caller: output Ghidra fungsi `0x80015B7C` = 240 alamat, end-exclusive `0x80015C6C`; anotasi spimdisasm `nonmatching func_80015B7C, 0x580` memiliki label tambahan `0x80015C6C` dan rentang yang tampak berlanjut ke `0x800160FC`. Call di `0x80015BF0` nyata/terdekode, tetapi jangan menganggap span anotasi panjang sebagai body Ghidra tunggal.
- Step 6 artifact #12741234990 SHA-256 ZIP `7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9` dibuka langsung: pada view entry-1 hipotetis 98.357 instruksi terdekode, +B30 = 1 READ, +B38 = 1 READ, +B40 = 1 WRITE, +B44 = 1 WRITE dan 1 READ. Base `0x800D0000` dan pointer di slot `0x8013A554` tetap tidak tervalidasi.
- Tes Step 9 7/7 RNG, 8/8 helper negative-a0, 16/16 setter/getter tetap CPU/MIPS terisolasi dengan MMIO sintetis; jangan mengulang tes identik.

### Prioritas berikutnya

1. Selesaikan rekonsiliasi batas `0x80015B7C` dari raw MIPS/return/tail jumps dan metadata Ghidra yang sama; jangan menaikkan Step 5 sebelum itu serta cakupan fungsi diwajibkan lebih luas.
2. Untuk 6(b), telusuri pointer slot `0x8013A554`, semua readers/writers dan alias melalui CFG-aware def-use lintas blok/fungsi; pertahankan BLOCKED bila sumber alamat/relokasi terputus.
3. Step 7: jangan ulangi probe no-hit `0x800AD454`; hanya pilih breakpoint jika raw instruction dan reachability baru mendukung.
4. Step 4: JALR count bukan target/callgraph; perlu resolusi target dan bukti seed/helper runtime bila fasilitas yang tersedia memungkinkan tanpa membuat klaim dari no-hit.
5. Pertahankan seluruh matriks dan statuses. Tidak ada adaptive player, emulator gameplay, input ataupun savestate restore yang dijalankan pada audit ini; tidak ada komponen adaptive-player yang diubah. Story Mode tetap NOT COMPLETE / TIDAK TERBUKTI TAMAT.

---

# Handoff Chat Berikutnya — Riset Naruto PS1 Langkah 4–10
Tanggal: 28 Oktober 2026
Repo tunggal: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

## Checkpoint dan laporan utama
- Parent yang diaudit: 7df287bf4ca21f6c32fe2589bc09e8665e62e846.
- Laporan silang bukti: [docs/STEP4_10_CROSSCHECK_2026-10-28.md](STEP4_10_CROSSCHECK_2026-10-28.md).
- Status dan log: STATUS.md, ANALYSIS_LOG.md.
- Laporan kriteria: docs/STEP4_10_LIVE_RECONCILIATION_2026-10-27.md, docs/STEP4_10_CLOSURE_REPORT_2026-10-27.md.
- Temuan teknis: docs/STEP4_RNG_TRACE_2026-10-27.md, docs/STEP8_FUNCTION_SEMANTICS_AND_GAME_RULES_2026-10-27.md, docs/STEP6_CFG_SSA_DATAFLOW_AUDIT_2026-10-27.md, docs/STEP7_RUNTIME_COLD_BOOT_RESULT_2026-10-27.md.
- Gate pemain adaptif: docs/ADAPTIVE_READINESS_NEXT_EVIDENCE_GATE_2026-10-25.md.

## Temuan yang jangan dikerjakan ulang tanpa pertanyaan baru
- Artefak #12739676233 SHA-256 ZIP 94d866f9c991b323a64f283da93359620c04ff8859d4c8fb53f4eb857c745f5d mempunyai empat direct JAL ke RNG: 0x80015B14, 0x80015BF0, 0x8001A460, 0x80020C24.
- Artefak #12741234990 SHA-256 ZIP 7ee636b8e687c5163873cdd40c82a02e8c8617885a0863b1e5a196b6eed1eac9 menunjukkan B30/B38→sum→B40, dan B44 diinisialisasi nol serta dikirim ke 0x8001B364 pada branch B2A>=6; base 0x800D0000 hipotesis.
- Step 9 #40606159061 artifact #12779814671 SHA-256 ZIP dd3e559997ce0c9f931f330144de8021bdb3c75fa16b4f21717299c4b2d4d79f: 7/7 RNG, 8/8 helper negative-a0, 16/16 setter/getter dengan MMIO sintetis. Jangan ulangi tes yang sama.
- Jangan ulangi probe no-hit #40484548650 (0x800AD454) atau #40485987817 (0x80035DA8) tanpa hipotesis reachability statis baru.

## Gerbang wajib
- Hanya repo zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research; jangan akses/ubah repo Tile Duel atau repo lain.
- Tidak ada gameplay, input tombol, restore savestate, atau adaptive player dijalankan pada sesi sebelumnya.
- Dokumen gate tanggal 25 Oktober mewajibkan izin pengguna yang baru dan eksplisit sebelum operasi yang memulihkan state atau mungkin mengirim input; auto-review menolak percobaan ulang sejenis. Jangan cari jalan memutar.
- Tetap target cue UNKNOWN, barrier_level_selection=WAIT, adaptive readiness NO-GO, Story Mode NOT COMPLETE, Revision65 blob 3754a6ddf45a7570c053d9c149b6d80b0862a127, cue token absent.
- START hanya dipakai untuk dialog yang sudah dikalibrasi setelah gameplay benar-benar dimulai; jangan menggantinya dengan Circle atau directional input tanpa konteks yang terverifikasi. Mask kunai bukan bukti selector.
- Jangan masukkan ROM/BIN/CUE/EXE, BIOS, memory card, savestate, dump RAM atau screenshot privat ke Git/artifact. Hash/ref dalam dokumen bukan bukti file sudah dibuka.
- Monitor, lint, dan regression yang hijau tidak membuktikan progress permainan. Story Mode tidak boleh disebut tamat tanpa ending autentik terverifikasi.

## Prioritas
1. Audit caller boundary/reachability statis untuk 0x80035D78, 0x80035DA8, 0x800A3118 dan 0x80066E7C; jangan gunakan 0x800BDBFC sebagai caller/helper tervalidasi karena entry-0 Ghidra timeout dan referensinya nol.
2. Trace pointer CFG-aware dari global slot 0x8013A554 sampai access field +0xB30/+0xB38/+0xB40/+0xB44; catat batas provenance yang tak diketahui.
3. Step 7 hanya lanjut jika ada copy instruction reachable yang dipilih dari raw disassembly; selain itu pertahankan BLOCKED dan jangan ulang probe generik.
4. Step 8 hanya beri label aturan dengan code flow dan state/result autentik independen yang saling mendukung.
5. Pertahankan matriks 17 baris: Step 4 partial; Step 5 partial; Step 6(a,c) partial, 6(b) blocked, 6(d) unknown; Step 7(a) partial, 7(b) blocked; Step 8(a) partial, 8(b) UNKNOWN; label aturan unsupported tetap tidak dipromosikan; Step 9(a) tuntas hanya 7 vektor RNG, 9(b) partial; Step 10 tuntas sebagai matriks audit saja.
