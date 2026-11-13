#!/usr/bin/env python3
"""UQ1 safe cancel control: two replicated CROSS input replays, no confirm input."""
from __future__ import annotations
import argparse
import csv
import sys
from pathlib import Path
import RunUQ1 as UQ

_ORIGINAL_LUA_PROBE = UQ.lua_probe

def cross_probe(launch: str, card: Path, exec_sites: list[int]) -> str:
    text = _ORIGINAL_LUA_PROBE(launch, card, exec_sites)
    anchor = "local mem=PCSX.getMemPtr()"
    if anchor not in text:
        raise SystemExit("UQ1CANCEL_LUA_MEM_ANCHOR_MISSING")
    text = text.replace(anchor, anchor + """
local pad=PCSX.SIO0.slots[1].pads[1]
local buttons=PCSX.CONSTS.PAD.BUTTON
local crossButton=nil
""", 1)
    anchor = " post=post+1\n"
    pulse = r''' post=post+1
 if post==30 then
  local b=buttons["CROSS"]
  if not b then
   log("UQ1CANCEL_INPUT_EVENT\t"..LAUNCH.."\t"..tostring(post).."\tCROSS\tPRESS\tTIDAK_TAHU\tFAIL_BUTTON_NAME")
   finished=true;PCSX.nextTick(function()PCSX.quit(70)end);return
  end
  local ok,value=pcall(function()pad.setOverride(b);return pad.getButton(b)end)
  local pass=ok and value==true
  log("UQ1CANCEL_INPUT_EVENT\t"..LAUNCH.."\t"..tostring(post).."\tCROSS\tPRESS\t"..tostring(value).."\t"..(pass and "PASS" or "FAIL_READBACK"))
  if not pass then finished=true;PCSX.nextTick(function()PCSX.quit(71)end);return end
  crossButton=b
 end
 if post==39 then
  if not crossButton then
   log("UQ1CANCEL_INPUT_EVENT\t"..LAUNCH.."\t"..tostring(post).."\tCROSS\tRELEASE\tTIDAK_TAHU\tFAIL_NO_ACTIVE_BUTTON")
   finished=true;PCSX.nextTick(function()PCSX.quit(72)end);return
  end
  local ok,value=pcall(function()pad.clearOverride(crossButton);return pad.getButton(crossButton)end)
  crossButton=nil
  local pass=ok and value==false
  log("UQ1CANCEL_INPUT_EVENT\t"..LAUNCH.."\t"..tostring(post).."\tCROSS\tRELEASE\t"..tostring(value).."\t"..(pass and "PASS" or "FAIL_READBACK"))
  if not pass then finished=true;PCSX.nextTick(function()PCSX.quit(73)end);return end
 end
'''
    if anchor not in text:
        raise SystemExit("UQ1CANCEL_LUA_VSYNC_ANCHOR_MISSING")
    text = text.replace(anchor, pulse, 1)
    text = text.replace("input=NONE ram_writes=NONE", "input=CROSS_CANCEL_FRAME_30_38 ram_writes=NONE")
    return text

def write_tsv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

def self_test() -> None:
    probe = cross_probe("TEST", Path("card.mcd"), [0x800B770C])
    required = ('buttons["CROSS"]', 'post==30', 'post==39', 'pad.setOverride',
                'pad.clearOverride', 'UQ1CANCEL_INPUT_EVENT')
    for marker in required:
        if marker not in probe:
            raise SystemExit("UQ1CANCEL_SELF_TEST_MISSING=" + marker)
    if 'buttons["CIRCLE"]' in probe:
        raise SystemExit("UQ1CANCEL_SELF_TEST_CONFIRM_BUTTON_FORBIDDEN")
    print("UQ1CANCEL_SELF_TEST=PASS safe CROSS pulse frame 30-38; no Circle")

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--work", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--self-test", action="store_true")
    args, _ = p.parse_known_args()
    if args.self_test:
        self_test()
        return 0
    if not args.work or not args.out:
        p.error("--work and --out required")
    UQ.lua_probe = cross_probe
    rc = UQ.main()
    events = []
    for launch in ("LAUNCH_1", "LAUNCH_2"):
        log = args.work / launch.lower() / "emulator.stdout.txt"
        if log.exists():
            for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("UQ1CANCEL_INPUT_EVENT\t"):
                    p = line.split("\t")
                    if len(p) >= 7:
                        events.append(dict(zip(
                            ["launch", "frame", "action", "phase", "readback", "status"], p[1:7]
                        )))
    write_tsv(args.out / "UQ1CANCEL_INPUT_EVENTS.tsv",
              ["launch", "frame", "action", "phase", "readback", "status"], events)
    launch_rows = []
    with (args.out / "UQ1_LAUNCHES.tsv").open(encoding="utf-8", newline="") as f:
        launch_rows = list(csv.DictReader(f, delimiter="\t"))
    input_ok = (
        len(events) == 4
        and all(e["action"] == "CROSS" for e in events)
        and all(e["status"] == "PASS" for e in events)
        and all(e["readback"] == "true" for e in events if e["phase"] == "PRESS")
        and all(e["readback"] == "false" for e in events if e["phase"] == "RELEASE")
        and [e["phase"] for e in events] == ["PRESS", "RELEASE", "PRESS", "RELEASE"]
        and [e["frame"] for e in events] == ["30", "39", "30", "39"]
    )
    complete = rc == 0 and input_ok and len(launch_rows) == 2 and all(x["status"] == "PASS" for x in launch_rows)
    source_summary = args.out / "UQ1_SUMMARY.txt"
    if source_summary.exists():
        original = source_summary.read_text(encoding="utf-8", errors="replace").splitlines()
    else:
        original = []
    write_hits = 0
    for name in ("UQ1_WRITE_EVENTS.tsv",):
        path = args.out / name
        if path.exists():
            with path.open(encoding="utf-8", newline="") as f:
                write_hits = max(0, sum(1 for _ in csv.DictReader(f, delimiter="\t")))
    lines = [
        "UQ1_REPLICATED_SAFE_CROSS_CANCEL_RUNTIME_PROBE",
        "STATUS=" + ("TUNTAS" if complete else "SEBAGIAN" if rc == 0 or events else "BELUM"),
        "EVIDENCE=K5 terbatas bila dua launch PASS dan input PRESS/RELEASE identik; bukan variasi checkpoint independen",
        "CHECKPOINT_SHA256=" + UQ.CHECKPOINT_SHA,
        "MEMORY_CARD_TEMPLATE_SHA256=" + UQ.CARD_SHA,
        "INPUT_ACTION=CROSS (X/back/cancel prompt on checkpoint screenshot)",
        "INPUT_SCHEDULE=PRESS frame 30; RELEASE frame 39; same schedule in both launches",
        "INPUT_API=PCSX.CONSTS.PAD.BUTTON.CROSS; setOverride/getButton/clearOverride readback",
        "CONFIRM_INPUT_CIRCLE=NONE",
        "RAM_WRITE_INJECTION=NONE",
        "TWO_LAUNCHES_FROM_IDENTICAL_CHECKPOINT=YES" if len(launch_rows) == 2 else "TWO_LAUNCHES_FROM_IDENTICAL_CHECKPOINT=NO",
        "PRESS_RELEASE_READBACK=" + ("PASS" if input_ok else "FAIL_OR_INCOMPLETE"),
        "INPUT_EVENT_ROWS=" + str(len(events)),
        "WRITE_EVENT_ROWS=" + str(write_hits),
        "GAME_SIDE_SCREEN_TRANSITION=TIDAK TAHU; no screenshot state classifier in this probe",
        "CHECKPOINT_AND_CARD_INTEGRITY=see UQ1_LAUNCHES.tsv; run exit=" + str(rc),
        "ORIGINAL_NO_INPUT_UQ1_SUMMARY_LINES=" + str(len(original)),
        "GAMEPLAY_MEANING=TIDAK TAHU",
    ]
    summary = "\n".join(lines) + "\n"
    (args.out / "UQ1CANCEL_SUMMARY.txt").write_text(summary, encoding="utf-8")
    # Replace the generic imported summary so this output folder cannot be mistaken for a no-input run.
    source_summary.write_text(summary, encoding="utf-8")
    for old, new in (
        ("UQ1_LAUNCHES.tsv", "UQ1CANCEL_LAUNCHES.tsv"),
        ("UQ1_WRITE_EVENTS.tsv", "UQ1CANCEL_WRITE_EVENTS.tsv"),
        ("UQ1_EXEC_HITS.tsv", "UQ1CANCEL_EXEC_HITS.tsv"),
    ):
        src = args.out / old
        if src.exists():
            (args.out / new).write_bytes(src.read_bytes())
    print(summary, end="")
    return 0 if complete else 2

if __name__ == "__main__":
    raise SystemExit(main())
