# AM3 fixed CIRCLE A/B schedule

This table is the immutable input schedule for the AM3 H6 hybrid replay.
All timings are measured from the first post-load GPU::Vsync callback after SaveStateLoaded.
One-frame press is paired with release at the next post-load VSync.

- A: CIRCLE press frame 60, release frame 61, two independent emulator launches.
- B: CIRCLE press frame 90, release frame 91, two independent emulator launches.

Only H6 hybrid SHA d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475 is run. This experiment does not use a target-pure state and cannot establish target-pure gameplay determinism.
