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
