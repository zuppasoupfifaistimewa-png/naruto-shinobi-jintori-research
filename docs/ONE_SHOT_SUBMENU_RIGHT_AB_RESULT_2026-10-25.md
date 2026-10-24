# One-shot submenu RIGHT-vs-NONE diagnostic — setup failure (25 October 2026)

## Scope and provenance

- Only repository accessed or changed: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`.
- The user authorized the next bounded diagnostic. Actions run [#40144220503](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40144220503) was the single attempted emulator diagnostic; it ended `failure`.
- The private output artifact was [#12580165346](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40144220503/artifacts/12580165346), 3,644 bytes (uploaded ZIP SHA-256 `2b55119d1312ba9c1a9239f618b9890e7adbeb36bd9eb1d485642379c2df2abe`). Artifact contents were inspected only on GitHub Actions runners by [#40144372685](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40144372685) and [#40144439400](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40144439400). No screenshot bytes or private artifact contents were downloaded to the user's machine.
- Source checkpoint SHA-256 validation passed: `705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35`. Patched emulator, source Memory Card, Memory Card clones and SCPH-7502 BIOS validations also passed.

## Exact outcome

- The emulator booted and reported `LOAD_EVENT=PASS` after attempting to restore the checkpoint.
- The first preflight capture then emitted `sh: 1: xwd: not found`, followed by `CAPTURE_FAIL=PREFLIGHT_ACTION-F20`.
- The failing utility is part of the runner capture setup: the container's installed packages did not provide `xwd`. Although Xvfb and the emulator shared the same step/process lifetime, the required capture command was unavailable.
- Only the `PREFLIGHT_ACTION` process started. No preflight control, frame-20 pixel-parity comparison, action branch, or control branch completed.
- The runtime output contains no `INPUT action=RIGHT` press/release record. Therefore **RIGHT was not sent**, and no gameplay A/B result or usable screenshot frame was produced. The workflow failed before input; do not interpret this as a game response.
- Runner-side inspection reports no image files for either preflight or action/control frames. The only artifact content includes small runtime logs, validation text and an empty Xvfb log.

## Cleanup and gate disposition

- The temporary diagnostic and runner-only analysis workflows and their selectors have been removed from `main`.
- No retry was started. A future attempt must first receive fresh explicit approval for another restore/input attempt, then install the package providing `xwd` (for this Ubuntu container, add `x11-apps`), and explicitly test `command -v xwd`, `command -v convert`, and a bounded root-screen capture before restoring private state. Stop immediately if any capture utility check fails.
- Preserve target cue **UNKNOWN**, `barrier_level_selection = WAIT`, adaptive readiness **NO-GO**, Story Mode **NOT COMPLETE**, Revision65 marker blob `3754a6ddf45a7570c053d9c149b6d80b0862a127` unchanged, and the verified-cue token absent.
- No successful gameplay experiment or story progress was established. ROM, BIOS, savestate, Memory Card and screenshots remain uncommitted.
