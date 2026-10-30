# AM3 fixed CIRCLE A/B schedule

This table is the immutable input schedule for the AM3 H6 hybrid replay.
All timings are measured from the first post-load GPU::Vsync callback after SaveStateLoaded.
One-frame press is paired with release at the next post-load VSync.

- A: CIRCLE press frame 60, release frame 61, two independent emulator launches.
- B: CIRCLE press frame 90, release frame 91, two independent emulator launches.

Only H6 hybrid SHA d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475 is run. This experiment does not use a target-pure state and cannot establish target-pure gameplay determinism.

## Verified AM3 run result (30 October 2026)
Run 41048937290; job am3-h6-circle-ab; numeric job ID 124039892346; job conclusion success; output commit 51a66a060f3d4efda7eac7ada408b8d8ac88fe4c; source runner commit 4fbbbdf278ca71e0c84cb651287096561e9b4878.
All four launches passed button readback, 20/20 RAM captures, GDB normal exit (emulator decimal exit 0), no watchdog. A's two RAM sequences are identical; B's two RAM sequences are identical. Between A and B, sampled first-2-MiB RAM SHA first diverges at post-load frame 180. Slowest time-to-frame360 142.59486198425 s; timeout 600 s.
Caveat: the same reference Memory Card file was reused across all four launches without before/after hashing. Observed RAM differences are valid, but timing-only causation is not established.
