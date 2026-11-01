# AT3 runtime audit — AN2 schedule A/C, K0/K2

Date: 1 November 2026 (Asia/Jakarta)  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research  
Actions run: 41256458701  
Job: 124700549589 — AT3 eight-launch AN2 schedule A/C K0/K2 trace  
Run/job status: completed / success  
Source SHA: 7659306d19bdac7e9a831b4ed7355f60c8dc1dc0  
Actions output commit (workflow publisher): 405431bf61d36e91ad0f5a729968b62773d9caf0  
Script exit code: 0  
H6 SHA-256: d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475 — **HYBRID**, target checkpoint base plus CONTROL top-level protobuf SPU field 6; not target-pure.

## Matrix and validity

Eight independent launches were completed: schedule C (no input) and schedule A (CIRCLE press at post-load GPU::Vsync frame 60, release frame 61), each with K0 (breakpoints disabled) and K2 (three breakpoints), twice per cell.

- All 8 launches reached post-load frame 360, all 24 frame captures (180/240/360) passed.
- Emulator exit code: decimal 0 on all 8 launches.
- Every schedule-A press/release readback was PASS; schedule C had no gameplay input.
- All eight launches used separate copies of Memory Card. Before/after SHA-256 was unchanged in every launch: ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5.
- Timeout was 1,800 seconds per launch. Maximum observed wall time was 170.799 seconds; timeout exceeded twice that maximum.
- RAM hashes are SHA-256 of the first 2 MiB; savestate RAM segment parsed was 8 MiB. Raw savestates and RAM were temporary runner files, not committed.

## RAM hashes at capture frames

| Schedule | Mode | Attempt | Frame 180 | Frame 240 | Frame 360 |
|---|---|---:|---|---|---|
| C | K0 | 1, 2 | 5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7 | 75df26c668759d1a70a4765e87cab077184442381b84e3d1112ce05bf5627ec0 | 4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907 |
| C | K2 | 1, 2 | same as C/K0 | same as C/K0 | same as C/K0 |
| A | K0 | 1, 2 | 0251aeef113a4c1eb58533a7dc5af85488e9bc2d96f42e24f62f8806ab0b6be8 | 3b06642ed54bac03aaf9962f9074b84e550c861c57d7648fcb1f7cc5f14dc70d | 2c53c4a225acccda78ebf67cb39e4922b0ee73d8c2da44928957df36792cc780 |
| A | K2 | 1, 2 | same as A/K0 | same as A/K0 | same as A/K0 |

The two launch attempts were identical per schedule/mode/frame. On this H6 hybrid and these fixed schedules, K2 instrumentation did not change the captured RAM hashes relative to K0 at frames 180/240/360. This does not rule out transient changes between those sampled frames.

## Breakpoint counts and register observations

K0 has breakpoints disabled; its hit columns are NOT_MONITORED_BREAKPOINTS_OFF, not zero.

K2 breakpoints were armed at post-load frame 180 and observed through frame 360. Hit totals below are per condition across two attempts:

| Condition | Setter 0x8001387C | Getter 0x800138EC | Helper 0x800B770C | Getter returns |
|---|---:|---:|---:|---:|
| C | 0 | 720 | 0 | 720 |
| A | 0 | 720 | 0 | 720 |

Getter hits split across their two callsites: 360 hits at caller return address 0x801053CC and 360 at 0x80105420 per condition. Each of these 360 counts spans both attempts and the observed even-frame range 180–358. The corresponding getter-return events all recorded v0=0x000005DC.

At getter entry:
- First callsite (ra=0x801053CC): a0 and a1 each observed as 0 or 1.
- Second callsite (ra=0x80105420): a0 observed as 0 or 1; a1 observed as 0x801CEF08.
- Return events used a0=0x80070EA0 or 0x80070F54; a1 at return was 0 or 1.

**Scope limitation:** K2 breakpoints are only active from post-load frame 180 to frame 360. Zero hits at the monitored setter/helper addresses mean no execution at those addresses in that window on this H6 experiment only. It is not evidence that these functions are unused in other frames, states, modes, or target-pure gameplay.

## Conclusion

**AT3: TUNTAS — K5 terbatas pada eksperimen H6 HYBRID ini.** Runtime repetitions, input readbacks, captures, exit codes, Memory Card hashes, and timeout bound all passed. No gameplay/economy meaning is assigned to the observed register values or breakpoint counts.


## Follow-up attempt and workflow correction

The qualifying AT3 result above remains run **41256458701** (job **124700549589**, exit code 0). A later replication attempt, run **41258300049**, did not execute the emulator: all eight subprocesses returned **127** almost immediately, and the script returned exit code 2. The workflow had selected `squashfs-root/shared/bin/pcsx-redux`, which was not the executable used by the prior successful run. Its zero breakpoint counts and failed CIRCLE readbacks are therefore **invalid/not monitored**, not game behavior.

The workflow was corrected in commit `968c1a55731e09f815a1d1d385e1bf3edf792279` to use the executable path `$APPDIR/bin/pcsx-redux`, matching the path from successful run 41256458701. A replication run **41259662960** was started with that correction. At the time of this report update it was still in progress; its outcome is not used for the AT3 completion claim. This follow-up is a replication, not a prerequisite for the already-valid eight-launch result above.
