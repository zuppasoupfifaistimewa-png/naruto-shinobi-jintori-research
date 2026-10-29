# AF1–AF5 — ringkasan pendek (30 Oktober 2026)

**Skala K:** K0 tidak ada data; K1 dugaan; K2 indikasi terbatas; K3 beberapa bukti pendukung; K4 bukti langsung yang dapat diperiksa ulang (statis maksimal K4); K5 runtime konsisten pada ≥2 peluncuran terpisah.

| Butir | Status | K | Pokok |
|---|---|---:|---|
| AF1a mapping | TUNTAS | K4 | SPU 6=channels; Channel 1=data, 2=adsr, 3=adsr_ex; ChannelData 7/8/9=start/current/loop. |
| AF1b pointer | TUNTAS | K4 | 72 nilai target/kontrol lengkap di TSV; 19/24 current target di luar RAM 0x80000; schema tidak punya dst. |
| AF1c RSI | SEBAGIAN | K3 | 0xffffffffd736ce0f ada di raw log; 0xffffffffd736aa9f tidak ditemukan di log committed. Hubungan: TIDAK TAHU. |
| AF2 | SEBAGIAN | K3 | Whole field6 control mencapai marker 2× tetapi tak clean exit; only channel2 current control masih SIGSEGV 2×. Clean-exit + all-current test ditambahkan. |
| AF3 | SEBAGIAN | K3 | Push ditolak pada dua run lama; pull--rebase/retry ditambahkan. Raw log lama dan manifest tetap ada. |
| AF4 | SEBAGIAN | K4 | SHA target AppImage persis match upstream; container digest dari log 398677; producer 2fb tidak tersimpan untuk replay. |
| AF5 | BELUM | K2 | Lima hybrid identik; 10 run timeout, belum ada hash RAM/3 word runtime. |

**Perlu/tidak perlu:** seluruh SPU field6 target **PERLU** pada target-base intervention yang dites; menggantinya dengan field6 kontrol menghilangkan SIGSEGV sampai marker. Channel[2].data.current field8 **TIDAK PERLU** untuk crash pada basis target. Subfield pemicu tunggal belum dipastikan. Tidak ada klaim Story Mode tamat.

**Log:** run 40893536464/job 123516385854/commit `9d7c062b8457ecdf118be01fcc6c6fe65bcfe070` dan run 40893599809/job 123524765697/commit `9c1287c436522a5b333a3399d734dd8cc8c566c0` gagal push `fetch first`. Run 40895934142/commit `aaee865b4127b3eeb94f5bf4efcc7eb1692c11b9` gagal sebelum job tersedia; sebab TIDAK TAHU. Dua workflow baru berjalan: [AA1 run 40966952341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40966952341) dan [AE1/AF2/AF5 run 40966952270](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40966952270).

File: [laporan lengkap](AF1_AF5_CONTINUATION_REPORT_2026-10-30.md), [tabel pointer](AF1_SPU_POINTERS_TARGET_VS_CONTROL.tsv), [kutipan log](AF4_PROVENANCE_LOG_EXCERPTS.txt).
