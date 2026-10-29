# AA1 — GDB diagnosis for checkpoint restore

- Run ID: 40848251356
- Trigger commit: 64be99b0ea2d927216a7195dd95e85fbf8cd3612
- Required emulator: PCSX-Redux 0c3572c3d; AppImage SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c
- Direct ELF executable: /home/runner/work/_temp/naruto-aa1-gdb/source/squashfs-root/bin/pcsx-redux
- Target raw state: 21,163,286 bytes; SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d
- Control state: adaptive-cycle-01-f180.sstate; SHA-256 9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492
- Controller: no buttons injected; bounded to 180 post-load VSync or failure.
- Prior attempt #40845962644 tracked a short-lived launcher inferior and produced no emulator stack; it is not restore-failure evidence.

## Case: target

CD-ROM Label: SLPS-03553
CD-ROM ID: SLPS03553
Loaded BIOS: /home/runner/work/_temp/naruto-aa1-gdb/source/scph7502.bin
AA1_RESTORE_PROBE_READY_NO_INPUT=1 
AA1_PAD_CONNECTED_NO_BUTTONS_PRESSED 
AA1_LOAD_BEGIN=1 path=resume/target.sstate vsync=1 controller=NONE 
#1  0x00000000015884b0 in ?? ()
#2  0x00000000014f3420 in ?? ()
#3  0x00007ffff0de5870 in ?? ()
#4  0x0000000000000000 in ?? ()
AA1_GDB_EXIT_CODE=0

## Case: control

CD-ROM Label: SLPS-03553
CD-ROM ID: SLPS03553
Loaded BIOS: /home/runner/work/_temp/naruto-aa1-gdb/source/scph7502.bin
AA1_RESTORE_PROBE_READY_NO_INPUT=1 
AA1_PAD_CONNECTED_NO_BUTTONS_PRESSED 
AA1_LOAD_BEGIN=1 path=resume/control.sstate vsync=1 controller=NONE 
AA1_EVENT_SAVE_STATE_LOADED=1 
AA1_LOAD_CALL_RETURNED=1 
AA1_POST_LOAD_VSYNC=180 
[Inferior 1 (process 3090) exited normally]
\n=== AA1 NATIVE BACKTRACE ===\nNo stack.
AA1_GDB_EXIT_CODE=1

## Result interpretation (run 40848251356 / job 123360980473)

- **Control state:** the same direct emulator binary, BIOS, ISO, Memory Card, Lua restore hook, and argument order emitted `AA1_EVENT_SAVE_STATE_LOADED=1`, `AA1_LOAD_CALL_RETURNED=1`, then `AA1_POST_LOAD_VSYNC=180`. This is direct runtime evidence that the chosen loader path can restore at least the control state.
- **Target checkpoint:** emitted `AA1_LOAD_BEGIN=1` at VSync 1, but the captured sanitized report contains neither `AA1_EVENT_SAVE_STATE_LOADED=1` nor `AA1_LOAD_CALL_RETURNED=1` nor `AA1_POST_LOAD_VSYNC=180`. A short native stack excerpt (`#1`–`#4`) appears, but the sanitized report does **not** include an explicit `Program received signal SIGSEGV` line or a reliable signal/exit-code attribution for the target case.
- **Conclusion:** target restore did not complete under this probe while the control state did. This narrows the failure to the target state or its state-specific restore path, but **does not yet prove the cause of the historical exit 139**, does not prove all possible restore paths impossible, and does not justify calling the target load a confirmed SIGSEGV. Likely alternatives still open include savestate-content/format details or state-specific loader behavior.
- **AA1 status:** SEBAGIAN, K2 for a target-specific failure indication. The required root-cause diagnosis is not complete.
- **Downstream gate:** AA2 is NOT RUN / BELUM. No chakra/RNG watchpoint trace, two-CIRCLE-frame comparison, (k) calculation, or PC-to-caller runtime correlation is claimed from this run.

## Interpretation guard

A restore failure is established only if the target GDB log records SIGSEGV and a native backtrace at the actual load call. Missing direct-executable logs, a launcher-only stack, or an early exit is an inconclusive harness result.
