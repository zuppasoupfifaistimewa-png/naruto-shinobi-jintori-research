# Runtime result — retail SCPH-7502, low-rate RSP PC samples (2026-10-18)

## Run and reproducibility

- GitHub Actions run: [#39098622572](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39098622572)
- Workflow commit: [2566da091954aebc641a6126d9ab4959668f1730](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/2566da091954aebc641a6126d9ab4959668f1730)
- Emulator: PCSX-Redux AnyLinux AppImage, pinned to source commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`
- Runner: `ubuntu-26.04`; Xvfb 1280×800; Mesa software rendering; controller Port 1 configured as Analog and remapped.
- BIOS: retail SCPH-7502; the workflow verified ZIP and extracted BIOS SHA-256 against the known hash before launching. Runtime log says `Known BIOS detected: SCPH-7502 (EU) (318178bf)`.
- Disc recognized as label `SLPS-03553`, ID `SLPS03553`, executable filename `SLPS_035.53;1`.
- Private runtime artifact: [#12125881547](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39098622572/artifacts/12125881547), retained for three days. ROM, BIOS, emulator extraction and temporary diagnostics were removed from the runner during cleanup.

## Observations

### CPU progress

A minimal external RSP client negotiated the supported packets and collected five low-rate PC snapshots, 12 seconds apart. It did not set breakpoints and did not poll from a VSync callback:

```
RSP_CONNECT=connected port=3333
RSP_PC_SAMPLE index=0 pc=0x80061cd0 target_status=S00
RSP_PC_SAMPLE index=1 pc=0x80061cd0 target_status=S00
RSP_PC_SAMPLE index=2 pc=0x8006796c target_status=S00
RSP_PC_SAMPLE index=3 pc=0x80067938 target_status=S00
RSP_PC_SAMPLE index=4 pc=0x8006796c target_status=S00
```

These PCs are within the main executable RAM span reported for the same disc by the prior loader probe (`T_ADDR=0x80010000`, `T_SIZE=0x0005d800`, ending at `0x8006d800`). This is evidence that the CPU reached and was executing within the loaded executable range at sampled times; it is **not** proof that initialization completed or the game reached its title screen.

### Visual output and input

The captures are screenshots of the actual non-root `PCSX-Redux` application window (1280×800), not captures of the Xvfb root:

- 12 seconds: black.
- 40 seconds: still almost entirely black (two colors).
- 65 seconds: a gray field with a large animated orange/yellow diamond.
- After Return and Z/Cross: the same general diamond animation remains.
- 90 seconds: the SONY COMPUTER ENTERTAINMENT logo and diamond are visible.

The post-input images differ by tens of thousands of pixels from one another, but the diamond is visibly animated even without evidence of an input-triggered state transition. Do **not** attribute those differences to the controller. No Naruto title/menu, gameplay scene, or confirmed controller response was seen.

### Logs

The runtime log includes the BIOS setup, `ResetCallback: _96_remove ..`, then `Got an unknown GPU data word: 0008a16c (cmdType: 0, command: 0)`. This GP0 message remains an observation, not a proven root cause. The workflow ended at its observation time limit and then cleaned up.

## Conclusion

**Status: BELUM KONKLUSIF — executable-range CPU progress observed; title/menu and gameplay not observed.**

The run adds one important distinction from earlier screen-only probes: retail SCPH-7502 does not leave the sampled CPU exclusively at BIOS addresses; samples fall within the loaded main executable range. However, output remains at the early Sony/diamond display, and Return/Z did not demonstrate a game-state transition. Story Mode has not been shown to start or finish.

## Next bounded experiment

Keep the same BIOS, disc, emulator pin, runner and rendering configuration. Instrument the GPU command/VRAM path using only bounded categorical summaries and private visual captures, and determine whether the unknown GP0 word is isolated or followed by normal frame/draw activity. Avoid repeated display-setting changes, modern GDB clients that the server does not support, breakpoints not independently validated, VSync callbacks, and raw instruction/register dumps. Only begin Story Mode after a recognizable Naruto menu appears and a controlled button sequence demonstrates a visible state change.
