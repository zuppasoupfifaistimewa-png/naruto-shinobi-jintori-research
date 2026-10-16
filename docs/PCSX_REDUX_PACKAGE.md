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
