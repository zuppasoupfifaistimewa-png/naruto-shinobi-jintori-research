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
