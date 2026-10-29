# AF1–AF5 — ringkasan pendek (30 Oktober 2026)

**Skala K:** K0 tidak ada data; K1 dugaan; K2 indikasi terbatas; K3 beberapa bukti pendukung; K4 bukti langsung yang dapat diperiksa ulang (statis maksimal K4); K5 runtime konsisten pada ≥2 peluncuran terpisah.

| Butir | Status | K | Pokok |
|---|---|---:|---|
| AF1 overall | SEBAGIAN | K3 | Mengikuti sub-butir terendah (RSI/korelasi belum terverifikasi). |
| AF1a mapping | TUNTAS | K4 | SPU 6=channels; Channel 1=data, 2=adsr, 3=adsr_ex; ChannelData 7/8/9=start/current/loop. |
| AF1b pointer | TUNTAS | K4 | 72 nilai target/kontrol lengkap di TSV; 20/24 current target di luar RAM 0x80000; schema tidak punya dst. |
| AF1c RSI | SEBAGIAN | K3 | 0xffffffffd736ce0f ada di raw log; 0xffffffffd736aa9f tidak ditemukan di log committed. Hubungan: TIDAK TAHU. |
| AF2 | SEBAGIAN | K3 | Run 40893599809 attempt 2 untuk field6/adsr/adsr_ex semua mencatat marker 180 lalu SIGINT/kill (`wrapper_rc=-9`); bukan clean exit, dan `elapsed≈115s` bukan waktu-ke-marker. |
| AF3 | SEBAGIAN | K3 | Push ditolak pada dua run lama; pull--rebase/retry ditambahkan. Raw log lama dan manifest tetap ada. |
| AF4 | SEBAGIAN | K4 | Provenance SHA tersedia; catatan AC3 yang menolak hipotesis build berbeda dicabut karena producer kontrol memakai AppImage `2fb33f…`, sedangkan target memakai `c04b3e…`. |
| AF5 | BELUM | K2 | Lima hybrid identik; 10 run timeout, belum ada hash RAM/3 word runtime. |

**Kutipan Actions attempt 2 (run 40893599809/job 123524765697):**
```text
2026-10-29T14:59:54.7199923Z AE_REFINE_ATTEMPT_DONE case=ae2-target-spu-field6-control attempt=2 result=POST_LOAD_VSYNC=180 signal=SIGINT pc=0x7fffe1f3c301 wrapper_rc=-9 elapsed=115.017
2026-10-29T15:03:50.3646145Z AE_REFINE_ATTEMPT_DONE case=ae1-channel2-child-adsr attempt=2 result=POST_LOAD_VSYNC=180 signal=SIGINT pc=0x7fffe1ed71be wrapper_rc=-9 elapsed=115.018
2026-10-29T15:07:40.4209574Z AE_REFINE_ATTEMPT_DONE case=ae1-channel2-child-adsr_ex attempt=2 result=POST_LOAD_VSYNC=180 signal=SIGINT pc=0x7fffe1f30f35 wrapper_rc=-9 elapsed=115.018
```
`elapsed` adalah total waktu sampai kill, bukan time-to-180. Klaim marker bertahan; klaim clean exit tidak berlaku.

**Perlu/tidak perlu:** seluruh SPU field6 target **PERLU untuk mempertahankan SIGSEGV** pada intervensi target-base yang dites; penggantian kontrol tidak SIGSEGV sebelum marker, tetapi proses tetap tidak clean exit. Channel[2].data.current field8 **TIDAK PERLU** untuk crash pada basis target. Subfield pemicu tunggal belum dipastikan. Tidak ada klaim Story Mode tamat.

**Log:** run 40893536464/job 123516385854/commit `9d7c062b8457ecdf118be01fcc6c6fe65bcfe070` dan run 40893599809/job 123524765697/commit `9c1287c436522a5b333a3399d734dd8cc8c566c0` gagal push `fetch first`. Run 40895934142/commit `aaee865b4127b3eeb94f5bf4efcc7eb1692c11b9` gagal sebelum job tersedia; sebab TIDAK TAHU. Dua workflow baru berjalan: [AA1 run 40966952341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40966952341) dan [AE1/AF2/AF5 run 40966952270](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40966952270).

**Koreksi AC3 dan sumber AppImage:** catatan lama yang menolak hipotesis *different build* secara umum **DITARIK**. Target consumer memakai AppImage SHA `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`; producer checkpoint kontrol run 39867730674 memakai `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`, exit 92. Apakah beda build menyebabkan masalah restore kontrol: **TIDAK TAHU** (binary producer tak tersimpan untuk replay). Untuk run 39262213468, log tanggal 19 Okt menunjukkan workflow mengambil asset bernama `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage` dari Release tag `research-emulator-pcsx-redux-2026-10-15` dan memverifikasi SHA `c04b3e…`; asset ID historis tidak dicatat. Asset `669480936` dibuat 23 Okt, jadi tidak dapat dipastikan sebagai ID asset yang diunduh pada run 19 Okt.

File: [laporan lengkap](AF1_AF5_CONTINUATION_REPORT_2026-10-30.md), [tabel pointer](AF1_SPU_POINTERS_TARGET_VS_CONTROL.tsv), [kutipan log](AF4_PROVENANCE_LOG_EXCERPTS.txt).
