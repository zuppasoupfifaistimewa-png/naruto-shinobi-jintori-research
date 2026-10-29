# AF1–AF5 — laporan lanjutan Naruto Jintori (30 Oktober 2026)

## Skala K
K0: tidak ada data; K1: dugaan; K2: indikasi terbatas; K3: beberapa bukti saling mendukung; K4: bukti langsung yang bisa diperiksa ulang (analisis statis maksimal K4); K5: runtime konsisten pada ≥2 peluncuran terpisah.

## Status per butir
| Butir | Status | K | Temuan |
|---|---|---:|---|
| AF1a — mapping field | TUNTAS | K4 | Nama/nomor field dari sumber pin emulator. |
| AF1b — pointer 24 kanal | TUNTAS | K4 | 72 nilai target/kontrol dalam tabel; hex, signed/unsigned decimal, rentang RAM. |
| AF1 overall | SEBAGIAN | K3 | Keseluruhan mengikuti sub-butir terendah AF1c (RSI/korelasi belum terverifikasi). |
| AF1c — RSI | SEBAGIAN | K3 | RSI 0xffffffffd736ce0f muncul pada raw log; RSI 0xffffffffd736aa9f tidak ditemukan dalam raw log committed yang diperiksa. Korelasi: TIDAK TAHU. |
| AF2 — hibrida dan necessity | SEBAGIAN | K3 | Seluruh SPU field6 kontrol mencapai marker dua kali tapi tidak clean exit; swap Channel[2].current saja tidak menghilangkan crash. Clean-exit fix + all-24-current test di workflow. |
| AF3 — raw logs/publikasi | SEBAGIAN | K3 | Raw log lama + manifest SHA committed; dua job tidak berhasil push output baru. Workflow kini pull--rebase/retry. |
| AF4 — provenance | SEBAGIAN | K4 | Digest container, uploader/created_at, serta kecocokan SHA upstream terverifikasi. Producer 2fb… tak tersedia untuk replay. |
| AF5 — RAM runtime | BELUM | K2 | Lima hybrid dibuat byte-identik; 10 launch terdahulu timeout, belum ada RAM snapshot runtime valid. |

## AF1 — field map dan pointer table

Sumber pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`: [src/spu/types.h](https://github.com/pcsx-redux/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/spu/types.h), [src/core/sstate.h](https://github.com/pcsx-redux/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/sstate.h).

Top-level SPU field: 1=`ram` (0x80000 byte), 2=`ports`, 3=`xa`, 4=`irq`, 5=`irqptr`, 6=`channel` (24 entri), 7=`addr`, 8=`ctrl`, 9=`stat`, 10=`cbStartInd`, 11=`cbCurrInd`, 12=`cbEndInd`, 13=`cbVoiceInd`, 14=`CBLeft`, 15=`CBRight`, 16=`noiseClock`, 17=`noiseCount`, 18=`noiseVal`, 19=`endx`.

Channel field 1=`data` (ChannelData), 2=`adsr`, 3=`adsr_ex`. ChannelData: 1=`new`; 2=`sb_pos`; 3=`s_pos`; 4=`s_inc`; 5=`sb`; 6=`sval`; 7=`start`; 8=`current`; 9=`loop`; 10=`on`; 11=`stop`; 12=`reverb`; 13=`act_freq`; 14=`used_freq`; 15=`left_volume`; 16=`left_vol_raw`; 17=`ignore_loop`; 18=`mute`; 19=`right_volume`; 20=`right_vol_raw`; 21=`raw_pitch`; 22=`irq_done`; 23=`s_1`; 24=`s_2`; 25=`rvb_active`; 28=`noise`; 29=`fmod`; 31=`solo`. Slots 26, 27, 30 are legacy reverb fields; 32 is skipped. Field named `dst` is absent from the schema inspected, so I did not map another field to it.

Pointer values: [AF1_SPU_POINTERS_TARGET_VS_CONTROL.tsv](AF1_SPU_POINTERS_TARGET_VS_CONTROL.tsv), 72 rows for fields 7/8/9 across 24 channels. Values interpreted as stored 32-bit offsets. SPU RAM valid offset range is `0x00000–0x7FFFF`.
- Target: 20/24 `current` fields are `0xD5E7578F` (signed −706259057, unsigned 3588708239), outside RAM. Remaining current values are channel #1 `0x00008430`, #8 `0x00008F60`, #19/#20 `0x0000A750`.
- Control has `0xFFFFFFFE` (signed −2, unsigned 4294967294) in several current fields. Source comments document a stopped cursor as a non-null all-ones sentinel; exact interpretation of each −2 field is not expanded beyond the source evidence.
- No serialized `start/current/loop` equals the pattern `0xD736xxxx`. Raw reverse-current log shows PC `0x7ffff0dd36d0`, instruction `movzbl (%rsi),%ecx`, RSI `0xffffffffd736ce0f`. The requested RSI `0xffffffffd736aa9f` for original target was not located in committed raw logs reviewed. Aritmetika bit-pattern `0xd736ce0f - 0xd5e7578f = 0x014F7680` (21.984.896) cocok dengan selisih RSI low32 dan `current` target sebagai nilai 32-bit tak bertanda; ini belum membuktikan bahwa angka tersebut adalah basis RAM SPU host. Cocok/tidaknya dengan mapping RAM SPU host: **TIDAK TAHU** sampai GDB target murni menyediakan disassembly dan mappings. Label AF1 keseluruhan: **K3**, mengikuti AF1c.
- Checkpoint target SHA-256: `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`. Control SHA-256: `9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492`.

## AF2 — runtime, SIGSEGV/marker, necessity

Previous tests, with their caveat:
- Target base + entire SPU field 6 from control; hybrid SHA-256 `d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475`. Run 40893599809 logged `POST_LOAD_VSYNC=180` on both launches, then SIGINT/kill and wrapper rc `-9`. Its `elapsed≈115 s` is the total launch-to-termination duration, **not** the time-to-180; time-to-180 in that run is **TIDAK TAHU**. Marker yes; clean exit no.
- Control base + only target Channel[2].data: hybrid SHA-256 `6bea52c107896f716b68d0174d5cb840c5cf3869a3b8239054584e0e9d92faaa`; two SIGSEGV at PC `0x7ffff0dd36d0`.
- Target base + only control Channel[2].data.current field 8: SHA `7ae71d8620b56879177f825f5d6f68df59cfb7e06b4476f240fee3ab915f2e09`; two SIGSEGV at the same PC. This field is **TIDAK PERLU** for crash on the tested target base.
- Control base + only target Channel[2].data.current field 8: SHA `c4059abcb0573f7a615c7a04e217d1bc383dd662d310003baae971abce25fd01`; two SIGSEGV. Contextual sufficiency on the control base does not mean necessity on the target base.
- Control base + target Channel[2].adsr: SHA `2e67da72470863953558d33180ed859a36745dd84ab1586975b60e8753f4a39c`; marker twice then timeout/kill about 115.015 s; no clean exit.
- Control base + target Channel[2].adsr_ex: SHA `e5612c3c625b3ac29bf197ed9b652610e0f6d2a1b71d69c9dec02d2e3dcfe1d7`; marker twice then timeout/kill about 115.015 s; no clean exit.

**Kutipan Actions log attempt 2 — run 40893599809 / job 123524765697:**
```text
2026-10-29T14:59:54.7199923Z AE_REFINE_ATTEMPT_DONE case=ae2-target-spu-field6-control attempt=2 result=POST_LOAD_VSYNC=180 signal=SIGINT pc=0x7fffe1f3c301 wrapper_rc=-9 elapsed=115.017
2026-10-29T15:03:50.3646145Z AE_REFINE_ATTEMPT_DONE case=ae1-channel2-child-adsr attempt=2 result=POST_LOAD_VSYNC=180 signal=SIGINT pc=0x7fffe1ed71be wrapper_rc=-9 elapsed=115.018
2026-10-29T15:07:40.4209574Z AE_REFINE_ATTEMPT_DONE case=ae1-channel2-child-adsr_ex attempt=2 result=POST_LOAD_VSYNC=180 signal=SIGINT pc=0x7fffe1f30f35 wrapper_rc=-9 elapsed=115.018
```
Interpretasi: ketiga log memperlihatkan marker tercapai, namun proses tidak clean exit; `elapsed` bukan durasi-ke-marker. Karena itu klaim “marker dua kali” dipertahankan dengan caveat eksplisit dan tidak disamakan dengan runtime stabil.

**Jawaban perlu/tidak perlu:** seluruh target SPU field 6 adalah **PERLU** untuk mempertahankan crash pada intervensi berbasis target yang diuji—mengganti field 6 dengan kontrol menghilangkan SIGSEGV hingga marker. Channel[2].data.current field 8 **TIDAK PERLU** untuk crash pada basis target. Sub-field tunggal penyebab crash belum terisolasi.

**Perbaikan yang dikomit pada code commit 19d26af1a91e273b5c3bb2717af5032823239b09:** Lua sebelumnya mem-pause emulator sebelum menjadwalkan snapshot/quit via `PCSX.nextTick`, menyebabkan marker test tertahan hingga timeout. Harness kini tidak mem-pause setelah marker, menulis waktu relatif ke SaveStateLoaded dan launch, menguji hibrida target + seluruh 24 current control, melakukan bisect kanal jika hibrida all-current mencapai clean marker, dan menguji target + seluruh SPU field6 control. Timeout AF2 kritis 120 s; lima AF5 hibrida memakai timeout setidaknya dua kali waktu marker tercepat terukur AF2 ditambah 5 s (fallback 245 s bila belum ada nilai marker terukur). Runtime output baru masih harus dibuktikan oleh Actions.

## AF3 — kegagalan log publish dan raw permalink

- [Run 40893536464](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40893536464), job `123516385854`, commit `9d7c062b8457ecdf118be01fcc6c6fe65bcfe070`: push akhir ditolak `[rejected] HEAD -> main (fetch first)`, job exit 1.
- [Run 40893599809](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40893599809), job `123524765697`, commit `9c1287c436522a5b333a3399d734dd8cc8c566c0`: push akhir ditolak dengan alasan sama.
- [Run 40895934142](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40895934142), commit `aaee865b4127b3eeb94f5bf4efcc7eb1692c11b9`: gagal sebelum job tersedia (0 jobs, logs API 404); sebab **TIDAK TAHU**.
- Perbaikan `git pull --rebase origin main` kemudian push retry sampai tiga kali dipasang pada dua workflow.

Raw permalink dan SHA-256 hasil ekstraksi dari manifest committed:
- [GDB reverse-current attempt 1](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/f71f23126e9c79e53fdbbcb4734c395a91a52e0e/reports/ae_2026-10-29/deep/raw/ae2-target-current-pointer-field8-from-control-attempt1.gdb.txt), SHA-256 `7ed038ededc5848b4ac95411d36d89cb203bccbb2e0dbf628eccc077a53842b2`.
- [PCSX reverse-current attempt 1](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/f71f23126e9c79e53fdbbcb4734c395a91a52e0e/reports/ae_2026-10-29/deep/raw/ae2-target-current-pointer-field8-from-control-attempt1.pcsx.txt), SHA-256 `b01cbc7f4e9eef3bdcb9b64ba50a51aa3a98fe5426ba831ba635e67d47ca466d`.
- [GDB target-data attempt 1](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/f71f23126e9c79e53fdbbcb4734c395a91a52e0e/reports/ae_2026-10-29/deep/raw/direct-channel-field-1-attempt1.gdb.txt), SHA-256 `d36ff111f97cc861298c7795813dfd01368b3862bb2528676db0cf689ff91826`.
- [Full raw log SHA-256 manifest](https://raw.githubusercontent.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/f71f23126e9c79e53fdbbcb4734c395a91a52e0e/reports/ae_2026-10-29/deep/raw-log-sha256.txt).
- Raw per-launch files produced in runs 408935* were not committed before runner workspace cleanup. No claim is made that those files remain available.

## AF4 — provenance build/container

| Item | Evidence |
|---|---|
| Research Release asset 669480936 | Repo `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`, uploader `github-actions[bot]`, asset created_at `2026-10-23T15:05:43Z`, SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`. |
| Matching upstream Release asset | `pkgforge-dev/PCSX-Redux-AppImage-Enhanced`; tag `0c3572c3d@2026-10-01_1790876682`; asset ID `603793691`; `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage`; uploader `github-actions[bot]`; created_at `2026-10-01T17:44:44Z`; identical SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`. |
| Upstream release builder | Workflow in the upstream repo uses `ghcr.io/pkgforge-dev/archlinux:latest`, `make-stable-appimage-release@4ed3d48ccb065352b6e6c0db6d39885b201c54a0` (v1.1), and `quick-sharun` packaging/simple-test. |
| Run 39262213468/job 118092519254 | Commit `e396eac00631001b7a0e68d7701c70aec10dec19`; runner `ubuntu-26.04`; GDB `17.1-2ubuntu1`; flags `-softgpu -dynarec -stdout -lua_stdout`, under Xvfb. Workflow mengambil berkas bernama `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage` dari Release tag `research-emulator-pcsx-redux-2026-10-15` via API lalu memverifikasi SHA `c04b3e0a...fc0c`. Log bertanggal 19 Okt tidak mencatat ID asset yang dipilih. Asset ID `669480936` yang kini diketahui dibuat `2026-10-23T15:05:43Z`, sesudah run tersebut, sehingga tidak boleh dianggap sebagai ID sumber run 19 Okt. ID asset historis: **TIDAK TAHU**. |
| Run 39867730674/job 120134061270 | Commit `c9b1438292041f972b712f248fb7052032635b59`; runner `ubuntu-24.04`; container `ghcr.io/grumpycoders/pcsx-redux-build:latest`; actual job log digest `sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`; producer AppImage SHA `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99`; job exit code 92. Producer GDB version: **TIDAK TAHU**. |
| Producer AppImage `2fb33f…` | Not in retained artifact list; workspace and container were cleaned. Run 392622 checkpoint/Memory Card artifacts expire `2026-11-02T15:03:35Z` and `2026-11-02T15:03:37Z`, but those are not the producer AppImage. |

**PENCABUTAN CATATAN LAMA AC3 — hipotesis build berbeda:** pernyataan sebelumnya yang menolak hipotesis *different build* secara umum **DITARIK**. Run target memakai AppImage SHA `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`, tetapi producer checkpoint kontrol (run 39867730674/job 120134061270) memakai SHA `2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99` dan exit code 92. Jadi producer kontrol memang memakai binary berbeda; hipotesis itu tidak boleh ditolak. Binary `2fb33f…` tidak tersimpan untuk replay, sehingga apakah perbedaan build menyebabkan masalah restore kontrol: **TIDAK TAHU**. SHA `c04b3e0…` hanya membuktikan kesamaan pada jalur producer/consumer target, bukan pada kontrol. Lihat [AF4_PROVENANCE_LOG_EXCERPTS.txt](AF4_PROVENANCE_LOG_EXCERPTS.txt).

## AF5 — RAM 2 MiB / raw words

[Run 40899089356](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40899089356), job `123536139833`, commit `b8ac9eba871fc05eff75baace38d2cdb545eedf7`, reconstructed five AD3 hybrids identically:
- field 3 SHA-256 `78d937e5dabd8b2ebdf949176fad8557f82d6e0759116511530b18b8c841dca4`;
- field 4 SHA-256 `142f82698ab689518a115e0cdff32ce26d9c52a1cfd8a225fe36c2c1827f67ed`;
- field 5 SHA-256 `08f907c3b7f630369d7eca7d2157572fda68009a4caaee1d79827317373a3f6a`;
- field 8 SHA-256 `967be929b23017796ffc2faaad8a42e1d9d66c26e335d21d2a92ec0c63596967`;
- field 10 SHA-256 `0617e540eb1a6d0704a2637a50e37766b622870c08d0b1853f8eabeff1ad02e1`.

Each ran twice; all 10 outcomes were `INCONCLUSIVE_TIMEOUT_BOTH`. No valid 2 MiB runtime RAM SHA-256 exists yet, and the raw words at `0x80070EB8`, `0x80070F6C`, `0x8013A554` are **TIDAK TAHU**. A static extraction from saved-state file, if later used, must be labeled separately as static (max K4), not runtime.

## Run/job/commit crosswalk
| Run | Job | Commit | Result |
|---|---|---|---|
| [39262213468](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39262213468) | 118092519254 | `e396eac00631001b7a0e68d7701c70aec10dec19` | Target checkpoint producer/AppImage c04 |
| [39867730674](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39867730674) | 120134061270 | `c9b1438292041f972b712f248fb7052032635b59` | Control producer/container digest |
| [40893536464](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40893536464) | 123516385854 | `9d7c062b8457ecdf118be01fcc6c6fe65bcfe070` | Push rejected |
| [40893599809](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40893599809) | 123524765697 | `9c1287c436522a5b333a3399d734dd8cc8c566c0` | Push rejected |
| [40895934142](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40895934142) | none | `aaee865b4127b3eeb94f5bf4efcc7eb1692c11b9` | Failed before job; cause TIDAK TAHU |
| [40897542675](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40897542675) | 123530655378 | `65522cd174782e6d65cb765811b43440e95b33c3` | Recursive field audit |
| [40899089356](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40899089356) | 123536139833 | `b8ac9eba871fc05eff75baace38d2cdb545eedf7` | Five AD3 hybrids timeout |
| [40966952341](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40966952341) | `123773755046` | `19d26af1a91e273b5c3bb2717af5032823239b09` | job `success`; dua peluncuran target SIGSEGV pada PC `0x7ffff0dd36d0`; dua peluncuran kontrol mencapai marker 180. Ringkasan output commit `b676881aedccd7a492ebef8817656d8c1dd29e73`; wrapper exit kontrol `1` berasal dari diagnostik pasca-exit `No registers`, bukan bukti crash emulator. Detail per-launch akan dilaporkan terpisah. |
| [40966952270](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40966952270) | `123773754840` | `19d26af1a91e273b5c3bb2717af5032823239b09` | masih `in_progress` pada step `Recursive bisection into Channel occurrence 2`; hasil akhir belum tersedia saat revisi ini. |
