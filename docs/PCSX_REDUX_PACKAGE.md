# PCSX-Redux package inventory for Naruto research

**Updated:** 2026-10-16  
**Scope:** Naruto Shinobi Jintori Research only. No ROM/game data is included here.

## Extracted package now in ChatGPT Library

Location: `/Naruto Research Files/PCSX-Redux-HEAD-x86_64.AppImage`

| Property | Verified value |
|---|---|
| Source archive | `PCSX-Redux-9c6f98a0-linux-x86_64.zip` |
| Source archive size | 90,912,361 bytes |
| Source archive SHA-256 | `7e4c9378524ebfa35068944ba4aa9e3ebf7462678bcae33b3e7ae7c57dd99849` |
| Archive test | `unzip -t` passed; exactly one member |
| Member | `PCSX-Redux-HEAD-x86_64.AppImage` |
| Extracted member size | 91,474,424 bytes |
| Extracted member SHA-256 | `5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8` |
| Format | ELF 64-bit PIE, x86-64, AppImage Type 2 runtime marker |
| Embedded version | `9c6f98a0`, build ID `335`, channel `dev` |
| Changeset | `9c6f98a0ed0581635f9123147e382c248e0f5ddc` |
| Embedded build timestamp | 2026-09-28 19:56:29 UTC |

The extracted local file and the Library copy were byte-compared; both SHA-256 values matched. The Library storage limit had been reached, so the archive was replaced with its sole extracted member rather than retaining two near-identical 90 MB files. The Library item still reports stale `application/zip` MIME metadata after replacement/rename; the actual bytes were verified as the AppImage by SHA-256, `file`, embedded `version.json`, and the AppImage runtime check.

## Runtime compatibility finding

The AppImage runtime itself responds to `--appimage-version`. However, executing the bundled emulator binary on the current research host fails with missing version requirements `GLIBC_2.42` and `GLIBC_2.43`; the host provides glibc 2.41. The AppImage also cannot mount directly because FUSE/fusermount is unavailable. Therefore the extracted package is preserved but is **not currently runnable in this host environment without a compatible newer userspace or a different build**. This is a host compatibility issue, not evidence of a corrupt ZIP, corrupt AppImage, or invalid Naruto ROM.

## The existing GitHub release is a different build

The private research repo already has [a PCSX-Redux + OpenBIOS release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15). It contains `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage` (65,747,557 bytes, SHA-256 `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`) and OpenBIOS variants. That is a **distinct build** pinned to source commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`; do not confuse it with the extracted `9c6f98a0` AppImage.

The 91 MB extracted AppImage is stored in Library. It has not been inserted into Git history or uploaded as a new GitHub Release asset: the available GitHub connector exposes repository text/Git-data operations and read/download actions, but not a binary release-asset upload operation. The repo keeps this inventory, provenance, checksum, compatibility findings and the link to the existing research release so later chats can locate the right files without assuming the two builds are the same.

## Reproduction commands

Verify the Library copy after materializing it:

```sh
sha256sum PCSX-Redux-HEAD-x86_64.AppImage
# expected:
# 5b2bf850afea345ff1428a38ea75d1776a1857832acf873d9d72d3f4d214b0f8
```

Inspect or extract the inner AppImage filesystem without FUSE:

```sh
./PCSX-Redux-HEAD-x86_64.AppImage --appimage-extract
```

Before trying to launch the game again, choose a PCSX-Redux build compatible with the host glibc and available display/graphics environment. No game boot, menu/input response, or Story Mode progress was demonstrated by this package extraction.


## Preferred build for GLIBC 2.41 host — 2026-10-16

### Recommended candidate: AnyLinux AppImage (not the 9c6f98a0 ZIP)

Use the x86-64 AnyLinux AppImage produced by [pkgforge-dev/PCSX-Redux-AppImage-Enhanced](https://github.com/pkgforge-dev/PCSX-Redux-AppImage-Enhanced/releases/tag/0c3572c3d%402026-10-01_1790876682). The same binary is already attached to the research repo's [PCSX-Redux + OpenBIOS research release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15).

- File: `PCSX-Redux-0c3572c3d-anylinux-x86_64.AppImage`
- Size: 65,747,557 bytes
- SHA-256: `c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c`
- Source changeset: `0c3572c3db75f97542001e453ae80ba8c3f8acba` (2026-10-01)
- Packaging: unofficial AnyLinux AppImage built with `sharun/quick-sharun`; the packager says it bundles dependencies, supports old/musl Linux distributions, and does not require FUSE.
- Build evidence: the packager's x86_64 GitHub Actions run [36872881656](https://github.com/pkgforge-dev/PCSX-Redux-AppImage-Enhanced/actions/runs/36872881656) completed successfully on 2026-10-01. Its job log states that the `quick-sharun --simple-test` returned “Test went OK” (about 8 seconds). The packaged environment also bundles cross-libc-dlopen and an embedded uruntime.
- Earlier repo smoke-test notes say the same AppImage GUI opened under Xvfb and showed a “no BIOS configured” screen, which proves only GUI launch, not game boot.
- The 91 MB `9c6f98a0` AppImage in Library is **not the preferred build**: its inner executable explicitly needs GLIBC_2.42 and GLIBC_2.43, while this work host reports glibc 2.41.

### What is and is not verified

The AnyLinux package is the **best candidate found for the glibc-2.41 host** based on its packaging design and successful generic launch test. Do not overstate that evidence:
- The build smoke test does not load the Naruto ROM.
- There is no completed runtime log proving the Naruto title/menu appears, controls respond, CD reads finish, or the game remains stable.
- The currently available analysis container returns `ServerError` on even trivial shell commands, so this turn could not repeat the launch against the actual ROM. This is a tool/runtime outage, not a new result about emulator or ROM compatibility.
- No binary build can be promised to run “without any obstacles” before testing the exact BIOS, BIN/CUE, graphics context (upstream PCSX-Redux needs an OpenGL 3.0-capable context), and input configuration.

### Next end-to-end test

1. Materialize the exact ROM and matching CUE from Library. Keep ROM/retail BIOS out of GitHub.
2. Obtain the AnyLinux AppImage above and verify the SHA-256 before execution.
3. Configure OpenBIOS `openbios-chunked.bin`; use the CUE, isolated profile and logging. Configure Port 1 emulated controller protocol as Analog (`DeviceType: 1`) while using keyboard host input (`PadType: 2`) and `Connected=true`.
4. Confirm title/menu and input response first. Record CD reads and CPU PC. Then test a repeatable boot and later Story Mode; don't infer smooth gameplay from GUI launch or packaging CI alone.
