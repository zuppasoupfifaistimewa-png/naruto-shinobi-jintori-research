# Handoff for Ghidra analysis of SLPS_035.53

## Purpose and current state

Workflow: [Ghidra static analysis — SLPS_035.53](../.github/workflows/ghidra-static-analyze-psx-exe.yml).

Ghidra 12.2 setup was verified in Actions run [#40434733043](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40434733043). The analysis workflow now uses the existing BIN/CUE assets in the repository's [research-tool release](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/releases/tag/research-emulator-pcsx-redux-2026-10-15). **No `PSX_EXE_DOWNLOAD_URL` repository secret is required.**

The workflow downloads the release disc image and CUE file to the temporary GitHub Actions runner, verifies both using their recorded size and SHA-256, extracts `SLPS_035.53`, and independently verifies the extracted executable before Ghidra imports it. It runs static analysis only; it does not launch the game or an emulator.

## Pinned source and executable checks

Release assets used by the workflow:

- `Naruto.-.Shinobi.no.Sato.no.Jintori.Gassen.Japan.bin` — 325,989,552 bytes; SHA-256 `58c389a794375b7b81b3a18877ef7965356a1332285a3590170efbf2359a3b88`.
- `Naruto.-.Shinobi.no.Sato.no.Jintori.Gassen.Japan.cue` — 116 bytes; SHA-256 `be70d64f856e17aadc02cdcba7510234f5a11523216baddb3b247c95cec820b8`.

Extracted executable checks:

- File name: `SLPS_035.53`
- Exact size: `385024` bytes
- PS-X EXE signature: `PS-X EXE`
- Expected SHA-256: `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`

If any source or executable check fails, the workflow stops rather than importing an unverified input.

## Run the analysis

1. Open the repository's **Actions** tab.
2. Select **Ghidra static analysis — SLPS_035.53**.
3. Choose **Run workflow** on branch `main`.

Expected text-only artifact: `ghidra-slps-03553-function-index`, retained for 14 days. It contains the function TSV, RNG-signature scan/caller list, analysis configuration, validation report, and text logs. The disc image, CUE, extracted executable, and Ghidra project are not uploaded as artifacts or committed to the Git tree. The temporary disc extraction is deleted after the executable is verified; the executable and temporary project are deleted by the final cleanup step.

## Boundaries and interpretation

- Static analysis only; no emulator, gameplay input, ROM boot, BIOS, savestate, Memory Card, or screenshot evidence is used.
- The function TSV is an initial index, not proof that a candidate function controls RNG, Chakra transactions, roulette, barrier selection, or victory rules.
- If Ghidra succeeds, step 3 can be marked complete only after checking that `functions.tsv` is non-empty and its analysis-result report records SUCCESS.
- The independent adaptive-player gates remain unchanged: cue UNKNOWN, `barrier_level_selection = WAIT`, readiness NO-GO, Story Mode NOT COMPLETE; Revision65 remains untouched.
