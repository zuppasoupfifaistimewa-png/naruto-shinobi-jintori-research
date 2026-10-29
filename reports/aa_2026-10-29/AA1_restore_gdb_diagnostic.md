# AA1 — GDB diagnosis for checkpoint restore

- Run ID: 40846544137
- Trigger commit: 1dc091f31e4bea8bca96fd7171f5ef01c3d3bff1
- Required emulator: PCSX-Redux 0c3572c3d; AppImage SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c
- Target raw state: 21,163,286 bytes; SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d
- Control state: adaptive-cycle-01-f180.sstate; SHA-256 9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492
- Controller: no buttons injected; bounded to 180 post-load VSync or failure.
- Prior attempt #40845962644 tracked a short-lived launcher inferior and produced no emulator stack; it is not restore-failure evidence.

## Case: target

Catchpoint 1 (fork)
AA1_GDB_FORK_EVENT\nThe program is not being run.
Catchpoint 2 (exec)
AA1_GDB_EXEC_EVENT\nThe program is not being run.
Catchpoint 2 (exec'd /usr/bin/dash), 0x00007ffff7fe4540 in ?? () from /lib64/ld-linux-x86-64.so.2
#1  0x0000000000000016 in ?? ()
#2  0x00007fffffffd254 in ?? ()
#3  0x00007fffffffd25c in ?? ()
#4  0x00007fffffffd29b in ?? ()
#5  0x00007fffffffd2a5 in ?? ()
#6  0x00007fffffffd2b2 in ?? ()
#7  0x00007fffffffd2ba in ?? ()
#8  0x00007fffffffd2c0 in ?? ()
#9  0x00007fffffffd2fb in ?? ()
#10 0x00007fffffffd300 in ?? ()
#11 0x00007fffffffd33b in ?? ()
#12 0x00007fffffffd345 in ?? ()
#13 0x00007fffffffd380 in ?? ()
#14 0x00007fffffffd386 in ?? ()
#15 0x00007fffffffd428 in ?? ()
#16 0x00007fffffffd430 in ?? ()
#17 0x00007fffffffd463 in ?? ()
#18 0x00007fffffffd46c in ?? ()
#19 0x00007fffffffd475 in ?? ()
#20 0x00007fffffffd47d in ?? ()
#21 0x00007fffffffd489 in ?? ()
#22 0x00007fffffffd492 in ?? ()
#23 0x00007fffffffd4ce in ?? ()
#24 0x0000000000000000 in ?? ()
AA1_GDB_EXIT_CODE=0

## Case: control

Catchpoint 1 (fork)
AA1_GDB_FORK_EVENT\nThe program is not being run.
Catchpoint 2 (exec)
AA1_GDB_EXEC_EVENT\nThe program is not being run.
Catchpoint 2 (exec'd /usr/bin/dash), 0x00007ffff7fe4540 in ?? () from /lib64/ld-linux-x86-64.so.2
#1  0x0000000000000016 in ?? ()
#2  0x00007fffffffd252 in ?? ()
#3  0x00007fffffffd25a in ?? ()
#4  0x00007fffffffd299 in ?? ()
#5  0x00007fffffffd2a3 in ?? ()
#6  0x00007fffffffd2b0 in ?? ()
#7  0x00007fffffffd2b8 in ?? ()
#8  0x00007fffffffd2be in ?? ()
#9  0x00007fffffffd2f9 in ?? ()
#10 0x00007fffffffd2fe in ?? ()
#11 0x00007fffffffd339 in ?? ()
#12 0x00007fffffffd343 in ?? ()
#13 0x00007fffffffd37e in ?? ()
#14 0x00007fffffffd384 in ?? ()
#15 0x00007fffffffd426 in ?? ()
#16 0x00007fffffffd42e in ?? ()
#17 0x00007fffffffd461 in ?? ()
#18 0x00007fffffffd46a in ?? ()
#19 0x00007fffffffd473 in ?? ()
#20 0x00007fffffffd47b in ?? ()
#21 0x00007fffffffd487 in ?? ()
#22 0x00007fffffffd490 in ?? ()
#23 0x00007fffffffd4cd in ?? ()
#24 0x0000000000000000 in ?? ()
AA1_GDB_EXIT_CODE=0

## Interpretation guard

A target SIGSEGV in the native load call reproduces failure for this build/path but does not prove every restore route impossible. The control case is a wrapper check only if it passes under this exact pinned build.
