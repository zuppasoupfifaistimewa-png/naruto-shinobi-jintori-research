# PCSX-Redux package inventory for Naruto research

**Updated:** 2026-10-16  
**Scope:** Naruto Shinobi Jintori Research only. No ROM or game data is stored in the repo.

## Current candidate saved in ChatGPT Library

Location: `/Naruto Research Files/PCSX-Redux-0c3572c3d-anylinux-x86_64-artifact.zip`

This is the downloaded GitHub Actions artifact wrapper for the x86_64 AnyLinux AppImage build. The wrapper has not been re-hashed locally because the container runtime is currently returning `ServerError`; the producing Actions log reports the uploaded artifact ZIP digest below.

- Artifact run: [pkgforge-dev run 36872881656](https://github.com/pkgforge-dev/PCSX-Redux-AppImage-Enhanced/actions/runs/36872881656)
- Artifact ID: `11170447493`
- Actions-reported artifact ZIP digest: `f6c27070b565cbc0554f1093c1374a16aee2b8635c72ef7b141f9ff7bd857ed0`
- Artifact size reported by Actions: 65,673,524 bytes
- Main executable inside the artifact/release: `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage`
- AppImage size: 65,747,557 bytes
- AppImage SHA-256 from the GitHub Release metadata: `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`
- Source changeset: `0c3572c3db75f97542001e453ae80ba8c3f8acba` (2026-10-01)

The same standalone AppImage is also attached to the [Naruto research release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15).

## Why this is the preferred candidate for glibc 2.41

This is an unofficial AnyLinux package of PCSX-Redux built with `sharun/quick-sharun`. The packaging project states that it bundles dependencies, aims to work on old/musl Linux distributions, and uses an embedded uruntime so FUSE is not required.

The x86_64 build job on 2026-10-01 succeeded. Its log confirms:
- `cross-libc-dlopen` was added and verified.
- The generated AnyLinux AppImage was produced without errors.
- The `quick-sharun --simple-test` step returned **“Test went OK.”**

The research repo's earlier smoke-test notes also report that this AppImage's GUI appeared under Xvfb and displayed a “no BIOS configured” screen. That is evidence of GUI startup only—not evidence that Naruto booted.

## Historical package ruled out for this host

The following earlier candidate was replaced in Library because its bundled emulator did not match this host's glibc:
- Original ZIP: `PCSX-Redux-9c6f98a0-linux-x86_64.zip`, 90,912,361 bytes; SHA-256 `7e4c9378524ebfa35068944ba4aa9e3ebf7462678bcae33b3e7ae7c57dd99849`.
- Sole member: `PCSX-Redux-HEAD-x86_64.AppImage`, 91,474,424 bytes; SHA-256 `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8`.
- Embedded version: `9c6f98a0`, build ID 335, source changeset `9c6f98a0ed0581635f9123147e382c248e0f5ddc`, timestamp 2026-09-28 19:56:29 UTC.
- Its inner emulator executable required GLIBC_2.42 and GLIBC_2.43 while this host provided glibc 2.41. The outer AppImage runtime answered `--appimage-version`, but direct mounting also failed without FUSE.

The ZIP passed `unzip -t`, and its single member was extracted and hash-checked. Later it was replaced in Library by the smaller preferred AnyLinux artifact ZIP to stay within Library storage limits. The old extraction manifest was removed because it pointed to an obsolete Library path; this section preserves the historical record.

## Critical limit: Naruto boot is still unverified

The AnyLinux candidate is the best build found for the glibc 2.41 host, but its generic build-time smoke test does not test the Naruto ROM. There is still no fresh runtime evidence that the title/menu appears, controls respond, all 187 EXE payload sectors read successfully, or the game remains stable.

The local container and Python tools currently return `ServerError` even on simple commands. This blocked a fresh test in this session. It is a tool/runtime outage, not evidence that the candidate or ROM is corrupt.

No build can be guaranteed to run “without any obstacles” until the exact BIOS, BIN/CUE, display/OpenGL context (upstream PCSX-Redux requires an OpenGL 3.0-capable context), and controller configuration have been tested together.

## Next end-to-end test

1. Materialize the current Library ZIP and extract the AppImage when runtime access is available. Verify the executable SHA-256 above.
2. Use the ROM and matching `naruto-shinobi-jintori.cue` from Library; do not upload the ROM or a retail BIOS to GitHub.
3. Use `openbios-chunked.bin`, an isolated PCSX profile and a log file. Set Port 1 controller protocol to Analog (`DeviceType: 1`), keyboard as host input (`PadType: 2`) and `Connected=true`.
4. Confirm the title/menu and input response. Log CD progress and CPU PC; the main EXE payload is 187 sectors. Repeat boot tests before starting Story Mode.
5. Only claim stability or Story Mode completion after the corresponding runtime evidence exists.


## Cloud-runner result and current compatibility note — 2026-10-17

This section supersedes earlier statements that no remote end-to-end attempt had been made. The public Actions runner successfully downloaded the private-release ROM/CUE and diagnostic OpenBIOS through the configured read-only secret without printing the secret value. It verified ROM size 325,989,552 and SHA-256 `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`, validated a temporary CUE reference, and logged BIOS/disc recognition (`SLPS-03553`), all 187 executable chunks, `EXEC:PC0(80011448)`, and `Execute !`. Port 1 Analog configuration removed `Unknown command for pad: 43` in both headless test builds. See [Actions #38975931679](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975931679).

**Interpretation:** the executable-entry handoff is proven for the headless probes; the visible title/menu, working in-game input, and Story Mode are still not proven. The 30/60/90-second frame metrics from that run must not be used as a game-display diagnosis because the script captured the Xvfb root background rather than an emulator window.

The CPU trace attempt [Actions #38975445756](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/38975445756) compiled the pinned upstream source but failed before emulation because the host could not locate `libcapstone.so.5`. No trace rows were produced. A runner workflow correction at [commit d965dcc](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/d965dcc864c73818e67d6a1e5f9edc19d4a3a17c) installs `libcapstone-dev` and checks the binary's linked libraries before launch.

Two bounded retests were started from corrective runner commits:
- [GUI window-capture retest #39000276365](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000276365), intended to capture the PCSX-Redux window rather than the root background.
- [CPU trace retest #39000257139](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000257139), intended to launch the source-built emulator after dependency preflight.

At the most recent check, both retests remained `in_progress`; neither is recorded as passing yet. Do not start Story Mode rule experiments until a recognizable title/menu and controlled input response are independently evidenced. Keep ROM/BIOS/CUE, captures and trace data out of Git and delete them from the ephemeral runner after each run.


## Cloud A/B comparison — 2026-10-17

These tests use release assets from the [private research release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15), verified by Release SHA-256 metadata, and matched headless tests in [Actions #39000751307](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39000751307).

| Criterion | AnyLinux AppImage | AppImage labelled “HEAD” | Evidence and interpretation |
|---|---|---|---|
| Asset identity | PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage; 65,747,557 bytes; SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c; source commit 0c3572c3db75f97542001e453ae80ba8c3f8acba | PCSX-Redux-HEAD-x86_64.AppImage; 91,474,424 bytes; SHA-256 5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8; package metadata source 9c6f98a0ed0581635f9123147e382c248e0f5ddc (2026-09-28) | Same Release tag; checksums verified in Actions. “HEAD” is an asset name, not proof it is today's upstream HEAD. |
| Headless boot handoff | Pass: disc/CUE and BIOS recognized; 187 executable chunks; EXEC:PC0(80011448) + Execute ! | Same pass | Both in common matched step; proves entry handoff only. |
| Pad protocol warning | No Unknown command for pad: 43 with Port 1 Analog | Same | This doesn't prove game controls respond. |
| GUI/OpenGL | Mesa llvmpipe OpenGL 3.3; real window captured, but AnyLinux frames black at 30/60/90 s; OCR empty; GUI log did not reach executable entry | Matched GUI result pending | Run #39000751307 tested GUI only for AnyLinux; matched A/B GUI rerun #39002136781 was queued at time of writing. |
| Stability/runtime | Headless process reaches 90-s observation cap; no crash marker established | Same | An intentional timeout boundary is not a crash or proof of long-term stability. |
| Debug APIs | Packaged build lacks PCSX.CPU.Trace; GUI/debugger features available but gameplay debugging unproven | Same; not the source build | Source build at commit 6b9df482d7b77b9ae218d9c48c1ce1a43c265206 is required for built-in PCSX.CPU.Trace. Rerun #39001985849 was still building at note time. |
| Compatibility | AnyLinux/sharun package is smaller and aims to bundle dependencies/avoid FUSE | Larger; older package was recorded as requiring GLIBC 2.42/2.43 on prior glibc 2.41 analysis host, though runs under current Ubuntu 26.04 Actions | Prefer AnyLinux as default portable candidate; GUI/gameplay unresolved. |

### Interim selection and limits

Use **AnyLinux as the default cloud runner build** for now because it is smaller, intended for broad Linux compatibility, and observed to reach the same headless executable handoff/controller-protocol result. Keep the 9c6f98a0 AppImage as an A/B fallback, not “latest upstream HEAD”. Use a separate source build for instruction trace. This is a conditional operational choice, not a claim either build displays or plays Naruto better.

OpenGL 3.3 is present in Xvfb/llvmpipe, yet the GUI window captures and GUI-specific boot log do not show a rendered Naruto title or executable entry. The next gate is to inspect the matched GUI A/B rerun. Keep captures and all private media out of Git and public artifacts; cleanup removes per-build temporary GUI logs, frames and profiles from the ephemeral runner.


### Current upstream revision cross-check — 2026-10-17

A direct GitHub API query returned upstream main/head commit [41f3196257d0962942b60983201aade951ebbd54](https://github.com/grumpycoders/pcsx-redux/commit/41f3196257d0962942b60983201aade951ebbd54), timestamped 2026-10-17 02:53:17 UTC. Consequently, neither Release AppImage in this A/B test is built from that current commit: AnyLinux uses source 0c3572c3 (2026-10-01), while the asset named “HEAD” embeds source 9c6f98a0 (2026-09-28). The CPU-trace source pin 6b9df482 is from 2026-10-16 and is distinct from both packaged AppImages and from the latest upstream commit observed.


## Verifikasi GUI A/B terbaru dan perbaikan harness — 2026-10-17

Run GUI A/B [#39002136781](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002136781) berstatus workflow `success`, tetapi **bukan hasil uji GUI yang berhasil**. Langkah headless di job yang sama tetap membuktikan kedua AppImage membaca disc `SLPS-03553`, menuntaskan 187 chunk executable, dan mencatat `EXEC:PC0(80011448)` serta `Execute !`; keduanya tidak lagi mencatat `Unknown command for pad: 43`. Saat masuk bagian GUI, `gui_probe.sh` berhenti untuk kedua build pada `PAD_SETUP: unbound variable` karena variabel shell tidak diekspor. Tidak ada jendela emulator yang ditemukan dan tidak ada frame yang ditangkap. Karena hasil probe tidak dipaksa menjadi kegagalan job, status `success` hanya berarti step berakhir tanpa kegagalan workflow yang terdeteksi; status itu bukan bukti GUI/game berhasil.

Perbaikan minimal sudah didorong ke runner pada commit [aac684d120ec025c4a87197da8d835f90b89f869](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/commit/aac684d120ec025c4a87197da8d835f90b89f869): ekspor `PAD_SETUP` sebelum skrip probe GUI dipanggil. Rerun ROM privat [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) sudah dipicu dan masih `in_progress` pada pemeriksaan terakhir; hasil frame, OCR, boot-marker GUI, dan cleanup masih harus diperiksa dari log akhirnya.

CPU-trace run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) juga masih `in_progress`. Secret dan pengunduhan/verifikasi file privat telah dilewati; step source-build di container Docker yang dipatok digest masih berjalan, sedangkan capture trace dan cleanup belum dimulai. Belum ada `CPU_TRACE_SIZE` atau `CPU_TRACE_LINE` yang dapat dipakai untuk analisis.

Current upstream PCSX-Redux yang terverifikasi saat cek adalah [41f3196257d0962942b60983201aade951ebbd54](https://github.com/grumpycoders/pcsx-redux/commit/41f3196257d0962942b60983201aade951ebbd54) (2026-10-17 02:53:17 UTC). AppImage berlabel “HEAD” tetap build source 9c6f98a0, bukan upstream HEAD terkini. Tidak ada bukti bahwa judul/menu tampil atau input gameplay merespons; gate RT-001 tetap tertutup dan Story Mode tidak boleh dimulai.


## GUI A/B rerun setelah fix PAD_SETUP — 2026-10-17

Run [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) pada commit runner `aac684d120ec025c4a87197da8d835f90b89f869` selesai dengan workflow/job sukses, tanpa artefak Actions. Keberhasilan workflow tidak menjadikan uji GUI lulus.

| Kriteria | AnyLinux AppImage | AppImage berlabel “HEAD” |
|---|---|---|
| Headless | BIOS/disc `SLPS-03553`, SYSTEM.CNF, 187 chunk, `EXEC:PC0(80011448)`, `Execute !`; exit 124 di batas 90 detik | Sama |
| GUI startup | PAD_SETUP dijalankan; window ditemukan dan ditargetkan langsung | Gagal membuat window: `Couldn't find matching GLX visual` |
| GUI boot marker | BIOS/disc/SYSTEM.CNF/BOOT terlihat, tetapi tak ada chunk 187 selesai atau `EXEC:PC0`/`Execute !` | PAD_SETUP dan executable-entry marker tidak muncul |
| Capture 30/60/90 s | Ketiga frame window 1280×800: mean 0, stddev 0, satu warna; OCR jpn+eng kosong | Tidak ada window atau frame untuk ditangkap |
| Exit/interpretasi | Exit 124 = batas observasi 100 s; bukan bukti crash | Exit 137 setelah timeout/eskalasi; kegagalan startup window terverifikasi, crash guest tidak terverifikasi |

GLX/renderer test pada run sebelumnya melihat Mesa llvmpipe/OpenGL 3.3. Dengan demikian jangan menyimpulkan seluruh lingkungan tanpa GLX; namun build “HEAD” ini gagal menciptakan window dengan konfirmasi log yang eksplisit. AnyLinux sudah melewati harness setup dan capture tetapi log GUI belum mencapai handoff executable. Frame hitam belum membuktikan layar game hitam setelah entry karena entry tidak muncul dalam log GUI.

Cleanup step berhasil dan tidak ada artefak. Pemeriksaan recursive tree repo runner publik menemukan hanya file workflow, dokumentasi, README, dan .gitignore—tidak ada media game, dump, capture atau binary emulator.

## Status CPU trace source-build saat pemeriksaan — 2026-10-17

Run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) masih `in_progress` pada step `Build pinned upstream PCSX-Redux with CPU trace support`. Download dan verifikasi ROM/CUE/BIOS berhasil; log archive sementara tak tersedia saat job aktif, dan langkah capture/cleanup masih pending. Batas keseluruhan workflow 45 menit. Source commit yang dipatok `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`; build image digest `sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`. Belum ada hasil kompilasi/dependensi/trace yang dapat dinyatakan lulus. Jangan menyamakan keterlambatan step dengan crash guest dan jangan rerun sebelum state akhir diketahui.

## CPU trace source-build terverifikasi — 2026-10-17

Source-build PCSX-Redux berhasil menggunakan upstream source pin `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` serta builder `ghcr.io/grumpycoders/pcsx-redux-build@sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`. Run [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) berjalan 04:17:11–04:44:27 UTC. Build sukses 04:43:46 dan `PCSX_BUILD_RESULT` muncul; pemeriksaan dependency `ldd` dilakukan dalam image yang sama dan tidak menemukan `not found`. Capture trace sukses dan cleanup selesai. Build butuh kira-kira 26m20s; gunakan source build untuk instruksi saja jika memang ada hipotesis yang dapat diuji, karena AppImage prebuilt tidak memiliki API trace ini dan compile tidak cepat.

Trace aktif pada VSync frame 1620–1680, jumlah instruksi `CPU_TRACE_SIZE=16031631`. Marker memastikan VSync dan instruction records tercatat. Log CPU berakhir dengan loop guest di `0x000015a4–0x000015c4`, bukan entry EXE `0x80011448`; run tidak log SYSTEM.CNF/187 chunk/EXEC:PC0/Execute. Loop belum teridentifikasi sebagai BIOS, loader, atau overlay dan counter yang menurun tidak membuktikan hang permanen. `TRACE_PROCESS_EXIT=124` merupakan observation cap 35s.

[GUI A/B #39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) confirms the earlier distinction: AnyLinux is the conditional default cloud runner candidate (smaller and working in the headless entry test), but the GUI path opens a window and runs PAD_SETUP without logging the EXE handoff; its captured window stayed uniform black. The AppImage named “HEAD” is not upstream current HEAD and fails GUI GLX/OpenGL window creation. Keep AnyLinux as an operational default for headless tests only—not a winner for GUI rendering or gameplay—and keep source trace as a separate pinned build.

No Actions artifact was produced. Cleanup confirmed temporary ROM/CUE/BIOS, built emulator and CPU trace logs were deleted. Runner public Git still has no game media, frame, RAM dump, save state or emulator binary. Title/menu and controlled input remain unverified; RT-001 stays Open / blocked.

## Perbandingan source pins — jangan menyamakan baseline headless dengan source trace (2026-10-17)

Source AnyLinux adalah `0c3572c3db75f97542001e453ae80ba8c3f8acba`; source trace adalah `6b9df482d7b77b9ae218d9c48c1ce1a43c265206`, 803 commit lebih baru menurut GitHub compare. Perubahan yang menonjol meliputi rewrite besar CD-ROM (`src/core/cdrom.cc` +1.476/-1.392) dan perubahan interpreter (`src/core/psxinterpreter.cc` +290/-81), termasuk logika branch-delay. Keduanya menjalankan mode interpreter pada command line cloud, tetapi waktu observasinya tak seimbang: baseline prebuilt 90s, source CPU-trace 35s. Tidak terbukti bahwa perbedaan source adalah akar masalah, dan belum tepat mengklaim satu build lebih stabil berdasarkan tes ini.

Follow-up yang tepat adalah membangun source pinned sekali lagi dengan observasi sampai 90s, guest PC sampling tiap 30 VSync, serta trace akhir sekitar frames 4500–4560; pisahkan output boot markers dari instruction rows. Ini akan menilai apakah PC rendah berlanjut atau keluar dari loop setelah window sebelumnya, kemudian mengarahkan pembandingan pada CD-ROM/interpreter. AnyLinux tetap kandidat operasional headless sementara, bukan pemenang yang telah terbukti untuk GUI/gameplay.

## Build source-trace dan hasil runtime follow-up — Actions #39004736399 (2026-10-17)

Run [#39004736399](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39004736399) mengonfirmasi source-build PCSX-Redux pin `6b9df482d7b77b9ae218d9c48c1ce1a43c265206` dapat dibangun serta dijalankan di builder image `ghcr.io/grumpycoders/pcsx-redux-build@sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4`. Semua step berakhir sukses. ROM hash/ukuran dan struktur CUE diverifikasi; pemeriksaan `ldd` dalam image yang sama tak menemukan `not found`. Compile sekitar 26m20s, disusul observasi 90 detik dan cleanup sukses.

Hasil runtime tetap diagnostik, bukan kelulusan boot game:
- OpenBIOS dan disc `SLPS-03553` dikenali; executable yang terdeteksi bernama `SLPS_035.53;1`.
- 158 sampel PC setiap 30 VSync dari frame 30 hingga 4740: 157 bernilai `0x000015a4`, satu sampel frame 420 bernilai `0x00000870`. Kedua jendela trace frames 1620–1680 dan 4500–4560 melaporkan sembilan PC unik dengan alamat dominan yang sama, sekitar `0x000015a4–0x000015c4`.
- Log tidak memiliki marker SYSTEM.CNF/BOOT, chunk executable 187 selesai, `EXEC:PC0(80011448)`, atau `Execute !`. Exit 124 adalah observation cap 90 detik, bukan otomatis crash.
- Trace runtime hanya dicetak sebagai ringkasan frekuensi PC, tanpa baris instruksi/operand mentah. Cleanup menyatakan ROM/CUE/BIOS, emulator source-build dan log sementara dihapus. Tidak ada Actions artifact.

Hasil ini membuktikan harness source-build, PC sampling, kedua jendela agregasi, dan cleanup bekerja. Hasil ini **tidak membuktikan** title/menu ditampilkan atau input permainan bekerja; RT-001 tetap Open / blocked. AnyLinux AppImage sebelumnya mencapai executable handoff pada jalur headless, tetapi fakta itu tidak boleh dicampur dengan run source-build ini.

Catatan keamanan: public log run lama [#39001985849](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39001985849) masih perlu penanganan terpisah karena memuat 80 record instruksi/operand mentah. Run terbaru telah menghindari pengulangan keluaran tersebut.

## Pembaruan paket dan capture — 2026-10-17

- Baseline AnyLinux AppImage masih berguna untuk pembanding headless, tetapi GUI probe lama [#39002846886](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-runner/actions/runs/39002846886) tidak mencapai executable-entry dalam jalur GUI. Frame jendela 30/60/90 detik hitam seragam; ini bukan bukti title screen karena boot marker executable tidak dicapai.
- Percobaan screenshot internal privat [#39011515345](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011515345) mencapai handoff di jalur no-UI, tetapi `PCSX.GPU.takeScreenShot()` memberi dimensi 0×0; postprocessing gagal dan artifact list kosong. Jangan pakai metode itu untuk mode no-UI.
- Probe source-current [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) membangun source pin `1525a93676dbece9fe70f10ff129aeaa14eec30d` dalam image builder yang dipatok, menggunakan jalur GUI nyata Xvfb dan menangkap hanya jendela PCSX, dengan retensi artefak maksimal tiga hari. Status ketika ditambahkan: belum selesai; periksa hasil final sebelum memilih emulator.
- Run CPU-trace lama #39001985849 pada runner publik telah dihapus secara selektif lewat run #39011611436; API fetch sesudahnya memberi 404. Tidak ada keluaran instruksi mentah yang ditambahkan dari eksperimen baru.
- Tidak ada emulator yang terbukti menampilkan menu/gameplay, dan tidak ada input game yang terbukti berfungsi. RT-001 tetap Open / blocked; emulator alternatif harus dipilih melalui uji aktual jika current-source probe tidak berhasil.

## Uji emulator alternatif tambahan — 2026-10-17

Workflow privat [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) kini menguji rilis DuckStation resmi, dengan AppImage SHA-256 `c5e6f045f6a242082fcafa9f02d56ad895e233b942728788d232ad0c0c765c24`, ROM yang sama dan OpenBIOS `openbios.bin` dari private release. Harness Xvfb mengambil frame jendela dan mengirim Return/Cross lewat pemetaan keyboard sementara, lalu menyimpan capture sebagai artifact privat 3 hari dan menghapus workspace. Status saat catatan ini dibuat: queued; belum ada hasil boot/menu/input yang bisa disimpulkan. Ini uji kandidat, bukan klaim kompatibilitas.



## Pembanding DuckStation dan status source-current — 2026-10-17

Uji kandidat DuckStation resmi [#39012200147](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012200147) **belum memberi hasil kompatibilitas**. Paket lolos hash, tetapi tidak bisa diluncurkan karena host runner tidak memiliki `libOpenGL.so.0`; tidak ada jendela, screenshot, input atau boot BIOS/disc yang dapat dinilai. Artifact ZIP 293 byte hanya berisi stdout 183 byte (tanpa capture PNG). Workflow diperbaiki pada commit `058aadea1c664712b62a63cf01fcb3e5598ef047` dengan paket `libopengl0 libglx0 libgl1` dan pola upload gambar `captures/*.png`; rerun [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) harus menjadi sumber hasil aktual.

Dengan demikian DuckStation belum dapat dinilai lebih baik atau lebih buruk dari PCSX-Redux untuk ROM ini. Source-current PCSX-Redux run [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) masih membangun source di pemeriksaan terakhir; belum ada capture GUI yang terverifikasi. **RT-001 tetap Open / blocked** sampai title/menu dan input kontrol nyata dibuktikan.


### DuckStation dependency retest — 2026-10-17

Setelah GL/GLX dipasang, DuckStation run [#39012504017](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012504017) masih tidak bisa memulai proses GUI karena `libEGL.so.1` hilang. Karena tidak ada window dan input tidak dikirim, ini bukan bukti bahwa DuckStation lebih buruk dalam kompatibilitas game. Commit `5afd32eca0d32ee191de7f2963f74b53aed89448` menambahkan `libegl1`; rerun [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) sedang berlangsung. Source-current PCSX build [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) juga belum selesai.


### Final DuckStation comparison note — 2026-10-17

Setelah runtime GL diperbaiki, run [#39012694027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39012694027) membuka GUI tetapi berhenti pada first-run setup wizard dan pesan BIOS PS1/PS2 yang diperlukan. UI mendeteksi satu file tetapi tidak menerima file itu sebagai BIOS valid; tidak ada marker game disc/executable atau title screen. Return memajukan wizard, bukan game. Kesimpulan terbatas pada **BIOS gate**: DuckStation belum menguji kompatibilitas ROM dalam kondisi OpenBIOS-only ini. Jangan meminta BIOS retail baru. Tetap prioritaskan PCSX-Redux source-current run [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708); hasil build/GUI-nya belum final pada pemeriksaan terakhir.


## Update source-current dan OpenBIOS variants — 2026-10-17

Source-current build pada [#39011842708](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39011842708) selesai dibangun dan link-check lulus, tetapi jendela PCSX hitam pada detik 20/40/60/80/95, OCR kosong, hanya PC sample frame 300=`0x000015a4`, dan tidak ada marker SYSTEM.CNF/BOOT/entry. Artifact #12094116949 berisi lima PNG hitam.
Dalam A/B AnyLinux [#39013612865](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39013612865), fastboot OpenBIOS mencapai `EXEC:PC0`/ `Execute !`, tetapi chunked hanya menunjukkan read progress sampai indeks 40. Detector lama tidak menemukan window; tak ada frame/input evidence. Jadi fastboot saat ini kandidat jalur loader terbaik, tetapi belum terbukti menampilkan game.
Run berikut [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) fokus memperbaiki identifikasi jendela untuk fastboot; periksa hasilnya sebelum klaim lebih lanjut.


### Fastboot GUI detector correction — 2026-10-17

Run [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) menemukan aplikasi PCSX pada window ID 543 setelah pencarian diperlebar; window capture 1280×800 benar-benar berasal dari aplikasi, bukan Xvfb root. Fastboot BIOS mencapai executable entry marker, tetapi seluruh frame sebelum/sesudah input dan sampai 90 detik tetap uniform black, OCR kosong. Return/Cross tidak membuktikan respons game.
Run [#39015290594](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015290594) mengulang jalur fastboot tanpa pengambilan register CPU di callback VSync, sebab pola tersebut pernah bermasalah sebelumnya. Hasil inilah pembanding berikutnya; status boot masih belum terverifikasi secara visual.


### Correction to fastboot capture evidence — 2026-10-17

The apparent black frames from [#39015133027](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015133027) are invalid for visual judgment: window ID 543 is Xvfb root ID `0x21f`, selected because the generic `.*` X11-name regex matches root. Withdraw the claim that those frames prove fastboot's emulator window was black. Only the fastboot boot log (SYSTEM.CNF, BOOT, EXEC:PC0, Execute!) remains valid.
Commit `83173bb10cfbf905a296f59720c0a63c95bc3a32` explicitly excludes root; inspect replacement run [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649). Do not treat a frame as emulator evidence unless the captured XID is non-root.


### X11 window selector follow-up — 2026-10-17

Run [#39015419649](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015419649) properly excluded root Xvfb, but the xdotool candidate list did not contain the child window. The printed X11 tree revealed `0x200034 "PCSX-Redux"` at 1280×800. There was no capture, so this does not indicate a game black screen. Run [#39015610296](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015610296) now parses child XIDs directly from the tree and focuses the non-root window before input; evaluate only its actual window capture and boot markers.


### Fastboot: valid app-window capture, software GPU still black — 2026-10-17

Run [#39015722771](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015722771) used direct X11 tree enumeration, captured the non-root PCSX-Redux window `0x200034` (decimal 2097204), and explicitly skipped root Xvfb. All five valid app-window captures were uniform black (1280×800, one color; OCR empty), even after Return/Cross. No CPU-register read callback was used. The independent boot log reached `EXEC:PC0(80011448)` and `Execute !`; visible gameplay remains unproven.
The next run [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) switches only the graphics backend from `-softgpu` to default OpenGL with Mesa software rendering/OpenGL 3.3 to test a renderer-specific cause.


### Default OpenGL A/B final — 2026-10-17

Run [#39015919056](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39015919056) removed `-softgpu` while retaining fastboot OpenBIOS, AnyLinux, the same ROM and Analog controller. Mesa llvmpipe OpenGL 3.3 Compatibility Profile was present. A valid non-root PCSX-Redux window (XID 2097204/`0x200034`) was captured; all frames before/after Return/Cross and at 40/65/90s were uniform black, OCR empty. The log nevertheless reaches SYSTEM.CNF/BOOT/EXEC:PC0/Execute!. No register sampling occurred in the VSync callback. Changing GPU backend alone does not solve display/guest startup.
Next diagnostic is a few external GDB-remote PC snapshots after entry, not raw instruction logging. RT-001 remains Open / blocked.


### External GDB PC snapshot probe started — 2026-10-17

The next private run [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234) keeps the fastboot BIOS/ROM/controller the same and queries PC through the emulator's external GDB server at bounded intervals. It avoids reading CPU registers inside VSync callbacks and emits only PC snapshots, not instruction/operand traces. At the latest check the runner was still installing GDB; no result is available yet.


### Emulator choice after GDB PC-snapshot run — 2026-10-17

Continue with the **prebuilt PCSX-Redux AnyLinux package plus fastboot OpenBIOS** as the main test path. It reaches SYSTEM.CNF/BOOT/EXEC:PC0/Execute! without DuckStation's additional BIOS wizard gate. This is only the best current loader path; it is not proof the title screen or gameplay has started. The chunked OpenBIOS variant has not reached the same entry marker in the tested window, and DuckStation did not accept the available OpenBIOS as a valid PS1/PS2 BIOS.
GDB run [#39016277234](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39016277234) completed, but external PC snapshots were unavailable at t20/t30/t50/t70 and timed out at t90. Valid PCSX window captures remained uniform black before and after Return/Cross, with empty OCR. Runner cleanup succeeded; private artifact #12095276220 contains temporary evidence and expires 2026-10-20 08:11 UTC. RT-001 remains Open / blocked.



## Diagnosis CPU polling dan keputusan probe berikutnya — 2026-10-17 (Actions #39029860914)

Run [#39029860914](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39029860914) menyelesaikan semua langkah workflow (`success`), termasuk unggah artefak privat dan cleanup. Emulator yang diuji adalah PCSX-Redux AnyLinux AppImage dengan OpenBIOS fastboot, ROM serta BIOS yang SHA-256-nya diverifikasi, setup Port 1 Analog/remap, dan command line `-exec ... -gdb -gdb-port 3333 -run`. Tidak ada breakpoint atau watchpoint pada eksperimen ini.

Klien RSP minimal tersambung dan `qSupported` berhasil. Polling menghasilkan 41 sampel selama sekitar 65 detik, dengan 14 nilai PC unik. Distribusi: rentang BIOS 31 sampel; rentang executable utama `0x80010000–0x8006d7ff` sebanyak 2; alamat lain sebanyak 8. PC sempat terlihat di `0x8003c0a0` pada sekitar 36,3 detik dan `0x8003bff4` pada sekitar 37,9 detik sejak polling dimulai, kemudian sampel pada sekitar 39,5 detik dan seterusnya kembali berada di BIOS, banyak di `0xbfc075b0–0xbfc07608`. Marker loader `SYSTEM.CNF`, `BOOT = cdrom:\SLPS_035.53;1`, `EXEC:PC0(80011448)`, dan `Execute !` ada di log, tetapi waktu marker tidak direkam di dalam jendela polling. Korelasi waktunya adalah petunjuk, bukan bukti sebab-akibat yang tuntas.

CP0 pada pembacaan bertahap: `BadVAddr=0`; `Status` biasanya `0x40000401` (satu sampel `0x40000000`); `Cause` biasanya `0x00000400`, dengan dua sampel `0x00000020`. Ini bukan snapshot atomik karena PC dan setiap CP0 dibaca melalui paket RSP terpisah. Query `?` menghasilkan `S00`; source GDB-server pada commit AppImage `0c3572c3db75f97542001e453ae80ba8c3f8acba` menyatakan `S00` adalah jawaban query ketika emulator masih running, **bukan stop event**. Jangan menyebut hasil ini sebagai exception loop yang sudah terbukti.

Audit source yang sesuai build: [src/core/gdb-server.cc pada commit 0c3572c3](https://github.com/grumpycoders/pcsx-redux/blob/0c3572c3db75f97542001e453ae80ba8c3f8acba/src/core/gdb-server.cc) mendefinisikan urutan register RSP; `g` mengembalikan paket semua register, dengan indeks 32=Status, 35=BadVAddr, 36=Cause, dan 37=PC. Karena itulah langkah pembeda berikutnya adalah satu pembacaan bulk `g` per sampel (576 karakter hex untuk 72 register 32-bit), plus cap waktu marker loader yang diamati langsung dari log. Ini mengurangi ketidakselarasan waktu dari query bertahap dan menghubungkan transisi PC dengan `Execute !` tanpa mengulang breakpoint/GPU-watchpoint.

Ringkasan bertanda `CPU_SAMPLER_EXIT=124` dalam log adalah salah label harness: heredoc Python polling berjalan di foreground, sedangkan `$!` masih merujuk proses emulator `timeout`; nilai 124 berasal dari batas observasi emulator 100 detik. Bukti bahwa sampler bekerja adalah 41 baris `CPU_SAMPLE`, diikuti `CPU_SUMMARY`; proses emulator terdeteksi selesai dan cleanup berhasil. Perbaiki label dan pengelolaan PID pada workflow berikutnya.

Artefak privat: [#12100266232](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39029860914/artifacts/12100266232), retensi sampai 2026-10-20 11:46:41 UTC. ROM, BIOS, emulator dan log sementara telah dibersihkan dari runner.

**RT-001 tetap Open / blocked.** Title/menu Naruto, respons input gameplay, dan Story Mode belum terbukti; belum ada aturan gameplay runtime yang boleh ditetapkan.

## Next CPU probe

Gunakan PCSX-Redux AnyLinux + OpenBIOS fastboot yang sama dan setup Port 1 Analog/remap yang sama. Gunakan klien RSP minimal, tanpa GDB modern, breakpoint, atau GPU/DMA watchpoint. Ambil satu paket RSP `g` per interval untuk membaca PC serta CP0 dalam transaksi yang sama; validasi panjang dan dekode byte sesuai source commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`. Pantau log PCSX selama eksperimen, catat waktu pertama `SYSTEM.CNF`, `BOOT =`, `EXEC:PC0`, dan `Execute !` terlihat, lalu korelasikan dengan kategori PC. Benahi PID/exit label harness. Pilih penyelidikan setelah itu berdasarkan data; jangan mengulang tes backend grafis.


## Hasil verifikasi runtime OpenGL — 2026-10-17

Run mandiri [#39049689832](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39049689832) sukses pada runner `ubuntu-26.04`. `glxinfo -B` default dan dengan `LIBGL_ALWAYS_SOFTWARE=1` sama-sama melaporkan vendor Mesa, renderer `llvmpipe (LLVM 21.1.8, 256 bits)`, OpenGL 4.5 Core/Compatibility Profile, Mesa 26.0.8; dua variabel override versi tidak digunakan. Program GLX menguji penciptaan konteks OpenGL compatibility 3.3 dan konteks berhasil; actual version 4.5. Ini membuktikan kemampuan Mesa software GL pada runner untuk versi tersebut, bukan bukti emulator/game sedang merender layar dengan benar.

Pada pin source `0c3572c3db75f97542001e453ae80ba8c3f8acba`, `src/gpu/soft/gpu.cc` menghitung dimensi screenshot dari `m_softDisplay.DisplayEnd - DisplayPosition`; jika register display PS1 belum menetapkan batas, hasil screenshot bisa 0×0 meskipun OpenGL host sehat. `src/core/pcsxlua.cc` mengikat `PCSX.GPU.getVRAM()`, dan source `src/core/pcsxffi.lua` memaparkan wrapper-nya. Gunakan API VRAM sebagai eksperimen pembeda berikutnya, lalu konversi sementara ke gambar diagnostik privat; jangan unggah raw VRAM/memory dump. Jangan mengganti emulator/pin maupun menyimpulkan kebutuhan GPU fisik berdasarkan screenshot 0×0.


## Temuan API screenshot/VRAM dan timing probe — 2026-10-18

Pada build pin `0c3572c3db75f97542001e453ae80ba8c3f8acba`, Lua API `PCSX.GPU.getVRAM()` sukses menghasilkan checkpoint 1024×512/16-bit (1.048.576 byte) pada sembilan event VSync awal. Kesembilan hasil pra-handoff identik hitam; guest FPS 0. Run log mencatat marker `Execute !` setelah frame 60 dan VSync frame 300 sesudahnya dengan guest FPS 1.0. Jadi diagnosis visual berikutnya harus mengambil checkpoint pasca-handoff, bukan mengulang sampel awal.

Percobaan berbasis timer rekursif via `PCSX.nextTick()` tidak menjalankan checkpoint. Source `src/core/pcsxffi.lua` membungkus fungsi dengan `AfterPollingCleanup`, sedangkan `src/core/ui.cc` menjalankan lalu membersihkan callback itu; penjadwalan ulang dari callback dapat tertimpa. Jangan menggunakannya sebagai timer rekursif. Untuk capture OpenGL, event GPU sebaiknya hanya menjadwalkan readback ke thread UI, karena membaca langsung dari callback event dapat memakai thread/konteks yang salah.

Run terbaru deferred-UI [#39078732160](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39078732160) terakhir dilihat masih berjalan pada 2026-10-18; hasilnya belum terverifikasi saat entri ini ditulis. Tidak ada perubahan keputusan emulator/pin, dan belum ada klaim bahwa title/menu/gameplay berhasil.


## Diagnosis GL host vs PS1 GPU traffic — 2026-10-18

Host OpenGL lulus pada run #39049689832 (Mesa llvmpipe, actual GL 4.5 Core/Compatibility, explicit 3.3 compatibility context pass tanpa override). Di source pin, screenshot API `takeScreenShot()` tidak tersedia pada backend OpenGL GPU, tetapi Software GPU memiliki implementasi. Dengan `-softgpu`, capture pasca-handoff frame 300 sah 320×240 tetapi satu warna hitam; VRAM tetap kosong. Screenshot independen X11 jendela aplikasi 1280×800 pada enam waktu juga valid tetapi hitam.

GPUDump private summary run #39079279565 mem-parse hingga 136 VSync live dengan nol GP0 packets/words, satu GP1 word, 136 VSync packets; complete packet stream, not truncated. Paket pre-trace berisi VRAM baseline upload (262153 GP0 words), bukan gambar yang dikirim game. Dump mentah dihapus pada runner. Run #39079291837 berupaya mengulang sampai VSync 300 dan harus dibaca final sebelum memakai hitungan sebagai jendela observasi penuh.


## Hasil GPUDump penuh dan CPU/GP0 correlation probe — 2026-10-18

Run [#39079291837](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079291837) GPUDump selesai parsing dengan satu TraceBegin, 268 VSync live packets/536 words, GP0 live packets=0 dan words=0, GP1 live packets=1/word=1; truncated=false. Pretrace GP0=262153 words adalah reset/full VRAM upload state baseline. Run timeout 90 s (124) walaupun job conclusion success; tidak boleh dinyatakan sebagai game boot sukses. Raw dump dihapus.

Workflow telah ditambah sampling CPU bulk register `g` dengan PC/CP0 dan marker loader ditimestamp pada run yang sama. Run baru [#39079600379](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079600379) masih pending saat status terakhir diperiksa; validasi kesimpulan menunggu outputnya. Ini pembeda berikutnya untuk menganalisis kegagalan guest executable tanpa mengulang tes OpenGL atau mengunggah trace instruksi.


## Hasil runtime terbaru — pengelompokan command GP0 dan CPU state, 2026-10-18

Run [#39079981314](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39079981314) selesai normal pada target VSync 300. Dump lengkap/tidak terpotong: 299 live VSync packets, 8 GP0 packets/43 words, 11 GP1 packets/16 words, 5 ThrowAway packets/words. Semua 43 live GP0 words diparse menjadi 42 perintah dengan decoder family ringkas: 39 GPU-state-setting, 1 clear-cache, 1 monochrome rectangle, 1 NOP; tidak ada triangle/quad/line/textured-sprite family. Raw dump sudah dihapus sebelum artifact diunggah.

Sampler RSP terkoneksi dan mengumpulkan 76 bulk snapshots valid. Timestamp marker yang dibaca dari log tidak buffered: SYSTEM.CNF ~4.85s, BOOT ~6.14s, EXEC header/Execute ! ~38.01s. PC sampel masuk executable 0x8003717c, 0x8003c0b4, 0x80037320 pada t=38–41s, kemudian dominan BIOS t=42–87s, lalu kembali ke 0x800372d8/0x80037320 pada t=88–99s. Status/Cause CP0 belum membuktikan exception tertentu. Screenshot tetap hitam; prioritas berikutnya adalah bucket histogram GP0 per rentang VSync agar urutan startup/guest transition lebih jelas.
