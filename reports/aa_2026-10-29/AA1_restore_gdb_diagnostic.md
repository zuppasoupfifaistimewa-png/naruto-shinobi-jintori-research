# AA1 — GDB diagnosis for checkpoint restore

- Run ID: 40845962644
- Trigger commit: f87fe444d67d8994e20a5048b189375db4e811b8
- Required emulator: PCSX-Redux 0c3572c3d; AppImage SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c
- Target raw state: 21,163,286 bytes; SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d
- Control state: adaptive-cycle-01-f180.sstate; SHA-256 9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492
- Controller: no buttons injected; bounded to 180 post-load VSync or failure.

## Case: target

[Inferior 2 (process 2870) exited normally]
\n=== AA1 NATIVE BACKTRACE ===\nNo stack.
AA1_GDB_EXIT_CODE=1

## Case: control

[Inferior 2 (process 2892) exited normally]
\n=== AA1 NATIVE BACKTRACE ===\nNo stack.
AA1_GDB_EXIT_CODE=1

## Interpretation guard

A target SIGSEGV in the native load call reproduces failure for this build/path but does not prove every restore route impossible. The control case is a wrapper check only if it passes under this exact pinned build.
