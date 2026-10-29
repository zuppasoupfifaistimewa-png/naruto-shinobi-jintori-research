# AA1 — GDB diagnosis for checkpoint restore

- Run ID: 40847605139
- Trigger commit: 13b95e3bab15be767d2a16b5567af8337f98e848
- Required emulator: PCSX-Redux 0c3572c3d; AppImage SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c
- Direct ELF executable: NOT_FOUND
- Target raw state: 21,163,286 bytes; SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d
- Control state: adaptive-cycle-01-f180.sstate; SHA-256 9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492
- Controller: no buttons injected; bounded to 180 post-load VSync or failure.
- Prior attempt #40845962644 tracked a short-lived launcher inferior and produced no emulator stack; it is not restore-failure evidence.

## Case: target

GDB log not produced; earlier workflow step may have failed.

## Case: control

GDB log not produced; earlier workflow step may have failed.

## Interpretation guard

A restore failure is established only if the target GDB log records SIGSEGV and a native backtrace at the actual load call. Missing direct-executable logs, a launcher-only stack, or an early exit is an inconclusive harness result.
