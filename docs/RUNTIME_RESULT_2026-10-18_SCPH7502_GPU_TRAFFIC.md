# Runtime result — SCPH-7502 GPU traffic and VRAM probe (2026-10-18)

## Run and configuration

- Actions run: [#39100404932](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39100404932)
- Workflow commit: [f68799906a40466a2617daea87c4f72d5a756b9d](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/f68799906a40466a2617daea87c4f72d5a756b9d)
- Private artifact: [#12125949426](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39100404932/artifacts/12125949426), short retention (3 days).
- Emulator: PCSX-Redux AnyLinux, pinned source commit `0c3572c3db75f97542001e453ae80ba8c3f8acba`; runner `ubuntu-26.04`; Mesa software rendering; `-softgpu`; interpreter; Port 1 Analog/remapped.
- BIOS: private SCPH-7502 asset extracted from `scph7502.zip`; the workflow verified the ZIP checksum and extracted BIOS SHA-256 before launch.
- ROM: private BIN/CUE assets re-used and verified. Raw GPUDump and VRAM/screenshots used for statistics were deleted before artifact upload. Artifacts contain only bounded logs/summaries and captured emulator-window PNGs.

## GPU traffic summary

The emulator reached the configured 300 `GPU::Vsync` callbacks and exited via the workflow's explicit stop:

- `GPU_DUMP_RESULT=parsed`; `GPU_DUMP_TRUNCATED=false`; one trace-begin marker.
- In the recorded/live interval: 431 GP0 packets / 9,126 GP0 words; 431 GP1 packets / 1,520 GP1 words; 299 VSync packets.
- The decoder parsed 2,413 GP0 command families from all 9,126 live words and reached `end_of_stream`, not an unknown-opcode stop.
- Counts included 181 flat quads, 127 Gouraud quads, 254 Gouraud triangles, 154 textured rectangles, 57 image-to-VRAM loads, and 1,268 GPU-state-setting commands. These are aggregate family names/counts only; command operands were not exported.
- In the 200–299 VSync bin, 4,569 GP0 words decoded fully into 1,702 commands. This demonstrates continuing GPU command traffic in the later observed interval.
- VRAM checkpoint 299: 1,048,576 bytes, 772 distinct RGB555 colors, 333,025 non-black pixels / 524,288 total.
- Emulator API pad injection readbacks were PASS for Cross, Start, and Up presses/releases. This verifies the emulator pad override API accepted the injected values; it does **not** prove the game reacted to them.

## Visual outcome

The valid non-root PCSX-Redux window captures progressed from mostly black to the orange/yellow diamond and then the **SONY COMPUTER ENTERTAINMENT** logo. Captures around 70 and 85 seconds show the Sony logo/diamond; no Naruto title/menu or gameplay scene was identified. The in-emulator screenshot API also returned 640×508 frames, but the workflow only exported pixel metrics for those API captures, not the raw data.

## Interpretation

**Status remains BELUM KONKLUSIF.** This test rules against a blanket claim that the GPU never receives or decodes drawing commands: the bounded GP0 stream is present and decodes through its end, and VRAM is populated. It does not establish which guest subsystem generated the stream, whether the main EXE is making forward progress at the same time, or why the display remains on the Sony splash instead of the Naruto menu. The earlier `0008a16c` unknown-GP0 log remains an observed anomaly; this capture did not encounter an undecodable GP0 stream in its recorded/live interval, so do not assign that anomaly as the root cause.

## Next experiment

Run the same GPU/VRAM probe with only a low-rate external RSP PC sample added (roughly every 12 seconds, no breakpoints, no VSync callback register reads). Correlate coarse PC region / repeated-PC patterns with the 100/200/300-VSync summaries and the real window screenshots. Include boot/BIOS/CD-ROM markers in safe logs. The key distinction is whether the CPU remains in BIOS code or repeatedly executes the main executable while the Sony splash persists. Keep the retail BIOS, ROM and all raw dumps private; do not upload raw GPUDump/VRAM or instruction traces.


## Follow-up: external PC and local control-flow categories

Run [#39100743589](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39100743589) reused the same retail BIOS/ROM, emulator pin, GPU settings and controller setup. Eight samples approximately 12 seconds apart showed initial BIOS PC then the main executable RAM span at the majority of samples:

- sample 0: BIOS ROM (`0xbfc02b68`)
- samples 1–3: main EXE region near `0x80061cd0`
- samples 4–7: main EXE region near `0x80067938` / `0x8006796c`

One 64-byte code window was read per unique sampled PC window. Only family counts/control-flow summaries were exported, not raw instruction bytes or disassembly. The window around the `0x80061cd0` sample had 2 conditional branches and one backward edge whose target was inside that 64-byte window; the `0x8006796c` window had 3 conditional branches and one backward edge whose target was outside that window. These local structures are compatible with loops but do not prove that the main game is globally stalled; sampled PC addresses themselves are not necessarily branch instructions.

**Important test-control correction:** run #39100743589 used interpreter mode, not the baseline dynarec mode, because of a workflow edit. Do not use its wall-clock performance as representative. Workflow commit [b4d849c4](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/commit/b4d849c4d555f092e1d5b406bdd67c1aa5aa3205) restores `-dynarec` while retaining only low-rate PC samples and one read-only summary per unique sampled code window. Follow-up [#39101124484](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/39101124484) is in progress at the time of writing.

The BIOS-region-lock hypothesis is less likely as a complete blocker because the CPU samples enter the main EXE region and GP0 drawing traffic is present. PAL BIOS versus NTSC-J disc could still influence some startup path, but this has not been proven to be root cause. The screen remains at Sony Computer Entertainment logo/diamond; there is no Naruto menu/gameplay and no verified in-game controller response. RT-001 remains **BELUM KONKLUSIF**.
