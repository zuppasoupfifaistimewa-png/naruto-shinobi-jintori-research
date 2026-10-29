# AA1 — GDB diagnosis for checkpoint restore

- Run ID: 40846881777
- Trigger commit: 2946c9f754942bd89ab3e1ba834b6fd743a4aec3
- Required emulator: PCSX-Redux 0c3572c3d; AppImage SHA-256 c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c
- Target raw state: 21,163,286 bytes; SHA-256 00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d
- Control state: adaptive-cycle-01-f180.sstate; SHA-256 9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492
- Controller: no buttons injected; bounded to 180 post-load VSync or failure.
- Prior attempt #40845962644 tracked a short-lived launcher inferior and produced no emulator stack; it is not restore-failure evidence.

## Case: target

Catchpoint 1 (fork)
Catchpoint 2 (exec)
AA1_GDB_EXEC_EVENT
#0  0x00007ffff7d1084c in vfork () from /lib/x86_64-linux-gnu/libc.so.6
#1  0x000055555555e9c1 in ?? ()
#2  0x00005555555665d5 in ?? ()
#3  0x000055555555d1b0 in ?? ()
#4  0x000055555555d173 in ?? ()
#5  0x000055555555d1b0 in ?? ()
#6  0x000055555555d173 in ?? ()
#7  0x000055555555d1b0 in ?? ()
#8  0x000055555556563d in ?? ()
#9  0x00005555555673a1 in ?? ()
#10 0x0000555555563bd2 in ?? ()
#11 0x000055555556674b in ?? ()
#12 0x000055555555d1b0 in ?? ()
#13 0x000055555555d1b0 in ?? ()
#14 0x000055555555d52a in ?? ()
#15 0x000055555555d1b0 in ?? ()
#16 0x000055555555d1b0 in ?? ()
#17 0x000055555555d1b0 in ?? ()
#18 0x000055555556563d in ?? ()
#19 0x0000555555558d7f in ?? ()
#20 0x00007ffff7c2a1ca in ?? () from /lib/x86_64-linux-gnu/libc.so.6
#21 0x00007ffff7c2a28b in __libc_start_main () from /lib/x86_64-linux-gnu/libc.so.6
#22 0x0000555555558f35 in ?? ()
AA1_GDB_EXIT_CODE=0

## Case: control

Catchpoint 1 (fork)
Catchpoint 2 (exec)
AA1_GDB_EXEC_EVENT
#0  0x00007ffff7d1084c in vfork () from /lib/x86_64-linux-gnu/libc.so.6
#1  0x000055555555e9c1 in ?? ()
#2  0x00005555555665d5 in ?? ()
#3  0x000055555555d1b0 in ?? ()
#4  0x000055555555d173 in ?? ()
#5  0x000055555555d1b0 in ?? ()
#6  0x000055555555d173 in ?? ()
#7  0x000055555555d1b0 in ?? ()
#8  0x000055555556563d in ?? ()
#9  0x00005555555673a1 in ?? ()
#10 0x0000555555563bd2 in ?? ()
#11 0x000055555556674b in ?? ()
#12 0x000055555555d1b0 in ?? ()
#13 0x000055555555d1b0 in ?? ()
#14 0x000055555555d52a in ?? ()
#15 0x000055555555d1b0 in ?? ()
#16 0x000055555555d1b0 in ?? ()
#17 0x000055555555d1b0 in ?? ()
#18 0x000055555556563d in ?? ()
#19 0x0000555555558d7f in ?? ()
#20 0x00007ffff7c2a1ca in ?? () from /lib/x86_64-linux-gnu/libc.so.6
#21 0x00007ffff7c2a28b in __libc_start_main () from /lib/x86_64-linux-gnu/libc.so.6
#22 0x0000555555558f35 in ?? ()
AA1_GDB_EXIT_CODE=0

## Interpretation guard

A target SIGSEGV in the native load call reproduces failure for this build/path but does not prove every restore route impossible. The control case is a wrapper check only if it passes under this exact pinned build.
