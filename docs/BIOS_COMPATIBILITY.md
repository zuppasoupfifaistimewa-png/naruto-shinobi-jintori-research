## Koreksi status BIOS — 2026-10-18

Bagian lama di bawah yang menyatakan tidak ada binary retail tersedia sudah kedaluwarsa. Aset scph7502.zip sekarang tersedia pada release privat dan hash BIOS cocok dengan referensi. Run privat #39094530928 memuat SCPH-7502, tetapi belum membuktikan title/menu. A/B #39095269662 juga belum menunjukkan menu valid. Jangan mengulang klaim BIOS tidak tersedia; masalah kompatibilitas tetap belum terisolasi.

# BIOS compatibility for Naruto — evidence and test status

Updated: 2026-10-18

## Finding: SCPH-7502 is the best documented retail-BIOS candidate

The [PSX Data Center entry for Naruto — Shinobi no Sato no Jintori Kassen](https://psxdatacenter.com/games/J/N/SLPS-03553.html) identifies the game as NTSC-J serial `SLPS-03553` and records one tested setup: ePSXe 2.0, Pete's OpenGL2 GPU Core 2.0.0, and console BIOS **SCPH7502** (page lines 82–89). This is meaningful game-specific compatibility evidence for that ePSXe setup. It is **not** a guarantee that SCPH-7502 has been tested with PCSX-Redux on GitHub Actions, and it does not identify a BIOS image's hash.

The official [PCSX-Redux OpenBIOS compatibility list](https://github.com/grumpycoders/pcsx-redux/blob/main/src/mips/openbios/COMPATIBILITY.md) lists Azure Dreams (NTSC) and Wipeout (NTSC-U/C) as incompatible. Naruto is not listed, but this short list is not an exhaustive certification list; absence from the list does not prove Naruto works with OpenBIOS. Official [OpenBIOS documentation](https://github.com/grumpycoders/pcsx-redux/blob/main/src/mips/openbios/README.md) says `BOOT_MODE=fast` skips the shell and attempts CD boot; fastboot is a boot mode, not a game-specific compatibility guarantee.

## Asset availability checked on 2026-10-18

The private research release `research-emulator-pcsx-redux-2026-10-15` contains the pinned PCSX-Redux AnyLinux AppImage, the private Naruto BIN/CUE, and these legal OpenBIOS builds:

- `openbios.bin` — `BOOT_MODE=fast`, SHA-256 `25c789eb66608847907217c367f04a3ec6e62c08530e97c437ce99d29f4c156d`.
- `openbios-shell.bin` — normal OpenBIOS shell/menu, SHA-256 `713ea2aed58606282b3ff5e91d77f8c5892ea36f5adcd279d2c7dd26604a625d`.
- `openbios-chunked.bin` — experimental fastboot variant, SHA-256 `7644ab45db8519a3621ef9cb0283f0ced5258287f8105c0e9d7e784fef9362b7`.

The same release notes explicitly state that it does not contain a retail Sony BIOS. The available ChatGPT Library listing contains the Naruto disc and related research files, but no SCPH-7502 BIOS image. No verified, authorized SCPH-7502 binary or existing download mechanism for one is available to this workflow.

I did not download a copyrighted BIOS dump from an unofficial ROM/BIOS collection and did not place a retail BIOS in the repository. This keeps the private game files and firmware out of repository changes and workflow artifacts.

## Cloud test in progress

A controlled GUI comparison has been extended to run the shell/menu build before fastboot and chunked OpenBIOS, with the same pinned emulator, private BIN/CUE, controller remap, Ubuntu 26.04, Xvfb, Mesa software rendering, and capture procedure:

- [Actions run #39093727808](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39093727808)
- Workflow: [`.github/workflows/naruto-bios-variant-gui-probe.yml`](../.github/workflows/naruto-bios-variant-gui-probe.yml)
- Workflow change: [commit `b5555142`](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/b5555142f58b720e333f124763cfcc47dbf22d0c)

This tests another available open-source BIOS behavior; it does **not** substitute for the game-specific SCPH-7502 candidate. Do not report a successful Naruto boot unless the private captures actually show a recognizable title/menu and visible controller response.

## Decision

Keep the selected emulator **PCSX-Redux AnyLinux AppImage at commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`**. Do not claim BIOS incompatibility is the established root cause. The best documented retail candidate is SCPH-7502, but there is currently no authorized binary available in the existing private assets to test it. Continue controlled tests with the available OpenBIOS variants and keep `RT-001 Open / blocked` until valid in-game visuals and input response are proven.
