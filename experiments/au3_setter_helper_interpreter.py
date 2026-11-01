#!/usr/bin/env python3
"""AU3: interpreter-only H6-HYBRID probe; setter/helper breakpoints across post-load frames 1..600."""
import argparse
import csv
import hashlib
import os
import re
import shutil
import subprocess
import time
from collections import Counter
from pathlib import Path

from aj2_h6_ram_probe import one, replace_top, encmsg

TARGET_SHA = "00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA = "9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA = "d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
MCD_SHA = "ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5"
RAM_SIZE = 0x200000
CAPTURE_FRAMES = (180, 360, 600)
HISTORICAL_SLOWEST_WALL_S = 143.227
BREAKPOINTS = {
    "SETTER_8001387C": 0x8001387C,
    "HELPER_800B770C": 0x800B770C,
}
def sha(data):
    return hashlib.sha256(data).hexdigest()

def ram2m(state):
    ram = one(one(state, 3), 1)
    if len(ram) < RAM_SIZE:
        raise ValueError("RAM segment < 2 MiB")
    return ram[:RAM_SIZE], len(ram)

def write_tsv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)

def lua_source(condition, press_frame, attempt):
    return r'''
if io.stdout then io.stdout:setvbuf("no") end
local condition = "''' + condition + r'''"
local attempt = ''' + str(attempt) + r'''
local pressFrame = ''' + str(press_frame) + r'''
local started, loaded, post = false, false, 0
local keep = {}
local armed = false
local pad = PCSX.SIO0.slots[1].pads[1]
local circle = PCSX.CONSTS.PAD.BUTTON.CIRCLE

local function log(s)
  print(s)
  pcall(function() io.stdout:flush() end)
end
local function hx(x)
  if x == nil then return "TIDAK_TAHU" end
  return string.format("0x%08X", tonumber(x))
end
local function regs()
  local r = PCSX.getRegisters()
  local g = r.GPR.n
  return r.pc, g.ra, g.a0, g.a1, g.v0
end
local function event(tag, address)
  local pc, ra, a0, a1, v0 = regs()
  local frame = math.max(post, 1)
  log(string.format(
    "AU3_EVENT condition=%s attempt=%d frame=%d tag=%s pc=%s regs_pc=%s a0=%s a1=%s ra=%s v0=%s",
    condition, attempt, frame, tag, hx(address), hx(pc), hx(a0), hx(a1), hx(ra), hx(v0)))
end
local function arm(address, tag)
  local bp = PCSX.addBreakpoint(address, "Exec", 4, "AU3_" .. tag, function(addr)
    event(tag, addr)
    return true
  end)
  keep[#keep + 1] = bp
  log(string.format("AU3_BREAKPOINT_ARMED tag=%s address=%s object=%s frame=1",
    tag, hx(address), tostring(bp ~= nil)))
  return bp ~= nil
end
local function armOnlyRequested()
  local setterOK = arm(0x8001387C, "SETTER_8001387C")
  local helperOK = arm(0x800B770C, "HELPER_800B770C")
  armed = setterOK and helperOK
  log("AU3_BREAKPOINT_SET count=2 getter=OFF active_postload_frames=1..600")
  if not armed then
    log("AU3_BREAKPOINT_INSTALL_FAIL=1")
    PCSX.quit(82)
  end
end
local function input(phase)
  local ok, value = pcall(function()
    if phase == "press" then pad.setOverride(circle) else pad.clearOverride(circle) end
    return pad.getButton(circle)
  end)
  local pass = ok and value == (phase == "press")
  log("AU3_INPUT condition=" .. condition .. " phase=" .. phase ..
      " frame=" .. post .. " readback=" .. tostring(value) ..
      " status=" .. (pass and "PASS" or "FAIL"))
  if not pass then PCSX.quit(83) end
end
local function capture(frame)
  local ok, err = pcall(function()
    local s = PCSX.createSaveState()
    local f = assert(Support.File.open(string.format("runtime/frame%d.sstate", frame), "TRUNCATE"))
    f:writeMoveSlice(s)
    f:close()
  end)
  log(ok and ("AU3_CAPTURE frame=" .. frame .. " status=PASS") or
      ("AU3_CAPTURE frame=" .. frame .. " status=FAIL error=" .. tostring(err)))
  if not ok then PCSX.quit(62); return end
  if frame == 600 then
    log("AU3_QUIT0_AFTER_FRAME600=1")
    PCSX.quit(0)
  end
end

_G.au3Load = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  loaded = true
  post = 0
  log("AU3_STATE_LOADED condition=" .. condition .. " attempt=" .. attempt)
  armOnlyRequested()
end)

_G.au3Vsync = PCSX.Events.createEventListener("GPU::Vsync", function()
  if not started then
    started = true
    local path = os.getenv("AU3_H6_STATE") or "resume/h6-hybrid.sstate"
    log("AU3_LOAD_BEGIN condition=" .. condition .. " attempt=" .. attempt ..
        " path=" .. path .. " INPUT_IS_SCHEDULED_ONLY=1")
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf, f = pcall(function() return assert(Support.File.open(path)) end)
      if not okf or not f then
        log("AU3_STATE_OPEN_FAIL=" .. tostring(f)); PCSX.quit(50); return
      end
      local ok, err = pcall(function() PCSX.loadSaveState(f) end)
      f:close()
      if not ok then
        log("AU3_STATE_LOAD_FAIL=" .. tostring(err)); PCSX.quit(51); return
      end
      log("AU3_LOAD_CALL_RETURNED=1")
      PCSX.resumeEmulator()
    end)
    return
  end
  if loaded then
    post = post + 1
    if pressFrame > 0 then
      if post == pressFrame then input("press") end
      if post == pressFrame + 1 then input("release") end
    end
    if post == 180 or post == 360 or post == 600 then
      local f = post
      PCSX.nextTick(function() capture(f) end)
    end
  end
end)
log("AU3_READY condition=" .. condition .. " attempt=" .. attempt ..
    " mode=INTERPRETER postload_frames=1..600 getter_breakpoint=OFF")
'''

def parse_events(log, condition, attempt):
    rows = []
    pat = re.compile(
        r"AU3_EVENT condition=(\S+) attempt=(\d+) frame=(\d+) tag=(\S+) "
        r"pc=(\S+) regs_pc=(\S+) a0=(\S+) a1=(\S+) ra=(\S+) v0=(\S+)"
    )
    for line in log.splitlines():
        m = pat.search(line)
        if m:
            rows.append({
                "condition": condition,
                "attempt": attempt,
                "frame": m.group(3),
                "tag": m.group(4),
                "pc": m.group(5),
                "regs_pc": m.group(6),
                "a0": m.group(7),
                "a1": m.group(8),
                "ra": m.group(9),
                "v0": m.group(10),
            })
    return rows

def main():
    ap = argparse.ArgumentParser()
    for name in ("target", "control", "pcsx-bin", "appdir", "bios", "cue", "card", "work", "out"):
        ap.add_argument("--" + name, required=True)
    ap.add_argument("--timeout-seconds", type=int, default=1800)
    a = ap.parse_args()

    target = Path(a.target).read_bytes()
    control = Path(a.control).read_bytes()
    if sha(target) != TARGET_SHA:
        raise SystemExit("TARGET_SAVESTATE_SHA_MISMATCH")
    if sha(control) != CONTROL_SHA:
        raise SystemExit("CONTROL_SAVESTATE_SHA_MISMATCH")
    hybrid = replace_top(target, 6, encmsg(6, one(control, 6)))
    if sha(hybrid) != H6_SHA:
        raise SystemExit("H6_HYBRID_SHA_MISMATCH")

    timeout_s = int(a.timeout_seconds)
    if timeout_s < 2 * HISTORICAL_SLOWEST_WALL_S:
        raise SystemExit("TIMEOUT_LT_2X_HISTORICAL_SLOWEST")
    work, out = Path(a.work), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for d in ("resume", "launches"):
        (work / d).mkdir(parents=True, exist_ok=True)
    h6path = work / "resume" / "h6-hybrid.sstate"
    h6path.write_bytes(hybrid)

    card0 = Path(a.card)
    if sha(card0.read_bytes()) != MCD_SHA or card0.stat().st_size != 131072:
        raise SystemExit("REFERENCE_MCD_MISMATCH")

    app = Path(a.appdir)
    env0 = os.environ.copy()
    env0.update({
        "DISPLAY": ":99",
        "LIBGL_ALWAYS_SOFTWARE": "1",
        "LD_LIBRARY_PATH": str(app / "usr/lib") + ":" + str(app / "usr/lib/x86_64-linux-gnu"),
        "QT_PLUGIN_PATH": str(app / "usr/plugins"),
        "QT_QPA_PLATFORM_PLUGIN_PATH": str(app / "usr/plugins/platforms"),
        "QML2_IMPORT_PATH": str(app / "usr/qml"),
    })

    launches, frames, events = [], [], []
    for condition in ("C", "A"):
        press = 0 if condition == "C" else 60
        for attempt in (1, 2):
            root = work / "launches" / f"{condition}-attempt-{attempt}"
            runtime, home = root / "runtime", root / "home"
            for d in (runtime, home / ".config", home / ".data", home / "runtime"):
                d.mkdir(parents=True, exist_ok=True)
            try:
                (home / "runtime").chmod(0o700)
            except OSError:
                pass
            mcd = root / "memory-card.mcd"
            shutil.copyfile(card0, mcd)
            mcd_before = sha(mcd.read_bytes())
            lua = root / "au3.lua"
            lua.write_text(lua_source(condition, press, attempt), encoding="utf-8")

            pad = (
                "PCSX.settings.pads[1].DeviceType='Analog'\n"
                "PCSX.settings.pads[1].Connected=true\n"
                "PCSX.SIO0.slots[1].pads[1].map()\n"
                "print('AU3_PAD_READY=PASS')\n"
            )
            env = env0.copy()
            env.update({
                "HOME": str(home),
                "XDG_CONFIG_HOME": str(home / ".config"),
                "XDG_DATA_HOME": str(home / ".data"),
                "XDG_RUNTIME_DIR": str(home / "runtime"),
                "AU3_H6_STATE": str(h6path),
            })
            pcsxlog, stdout = root / "pcsx.log", root / "stdout.log"
            command = [
                "timeout", "--signal=INT", "--kill-after=10s", f"{timeout_s}s",
                a.pcsx_bin, "-noupdate", "-debugger", "-interpreter",
                "-bios", a.bios, "-iso", a.cue, "-memcard1", str(mcd),
                "-exec", pad, "-dofile", str(lua), "-softgpu",
                "-stdout", "-lua_stdout", "-logfile", str(pcsxlog), "-run",
            ]
            start = time.monotonic()
            with stdout.open("wb") as fh:
                try:
                    proc = subprocess.run(
                        command, cwd=root, env=env, stdout=fh,
                        stderr=subprocess.STDOUT, check=False
                    )
                    rc = proc.returncode
                except Exception as exc:
                    rc = 255
                    fh.write(("AU3_EXCEPTION=" + repr(exc) + "\n").encode())
            wall = time.monotonic() - start
            log = stdout.read_text(encoding="utf-8", errors="replace")
            if pcsxlog.exists():
                log += "\n" + pcsxlog.read_text(encoding="utf-8", errors="replace")

            timeout_hit = rc in (124, 137, 143)
            emu_exit = "TIDAK TAHU" if timeout_hit else str(rc)
            card_after = sha(mcd.read_bytes()) if mcd.exists() else "TIDAK TAHU"
            ev = parse_events(log, condition, attempt)
            events.extend(ev)

            press_line = "AU3_INPUT condition=A phase=press frame=60"
            release_line = "AU3_INPUT condition=A phase=release frame=61"
            press_ok = (
                condition == "C" or
                any(press_line in line and "status=PASS" in line for line in log.splitlines())
            )
            release_ok = (
                condition == "C" or
                any(release_line in line and "status=PASS" in line for line in log.splitlines())
            )
            armed = (
                "AU3_BREAKPOINT_SET count=2 getter=OFF active_postload_frames=1..600" in log and
                "AU3_BREAKPOINT_ARMED tag=SETTER_8001387C" in log and
                "AU3_BREAKPOINT_ARMED tag=HELPER_800B770C" in log and
                "object=true" in log
            )
            launches.append({
                "condition": condition,
                "attempt": attempt,
                "flags": "-debugger -interpreter",
                "breakpoints": "0x8001387C;0x800B770C only; getter OFF",
                "breakpoints_armed": "YES" if armed else "NO",
                "circle_press_readback": "NOT_APPLICABLE" if condition == "C" else ("PASS" if press_ok else "FAIL"),
                "circle_release_readback": "NOT_APPLICABLE" if condition == "C" else ("PASS" if release_ok else "FAIL"),
                "emulator_exit_code_decimal": emu_exit,
                "timeout_wrapper_exit_decimal": str(rc),
                "wall_seconds": f"{wall:.3f}",
                "memory_card_sha256_before": mcd_before,
                "memory_card_sha256_after": card_after,
                "memory_card_unchanged": str(mcd_before == card_after).upper(),
                "timeout_seconds": timeout_s,
            })

            for frame in CAPTURE_FRAMES:
                state = runtime / f"frame{frame}.sstate"
                marker = f"AU3_CAPTURE frame={frame} status=PASS" in log
                cap = marker and state.is_file()
                digest, seg = "TIDAK TAHU", 0
                if cap:
                    try:
                        ram, seg = ram2m(state.read_bytes())
                        digest = sha(ram)
                    except Exception:
                        cap = False
                frames.append({
                    "condition": condition,
                    "attempt": attempt,
                    "frame": frame,
                    "capture_status": "PASS" if cap else "FAIL",
                    "ram_first_2mib_sha256": digest,
                    "ram_segment_bytes": seg,
                })
                if state.exists():
                    state.unlink()

    write_tsv(
        out / "AU3_LAUNCHES.tsv", launches,
        ["condition", "attempt", "flags", "breakpoints", "breakpoints_armed",
         "circle_press_readback", "circle_release_readback", "emulator_exit_code_decimal",
         "timeout_wrapper_exit_decimal", "wall_seconds", "memory_card_sha256_before",
         "memory_card_sha256_after", "memory_card_unchanged", "timeout_seconds"]
    )
    write_tsv(
        out / "AU3_FRAMES.tsv", frames,
        ["condition", "attempt", "frame", "capture_status", "ram_first_2mib_sha256", "ram_segment_bytes"]
    )
    write_tsv(
        out / "AU3_BREAKPOINT_EVENTS.tsv", events,
        ["condition", "attempt", "frame", "tag", "pc", "regs_pc", "a0", "a1", "ra", "v0"]
    )

    counts = Counter((e["condition"], e["tag"]) for e in events)
    count_rows = []
    for condition in ("C", "A"):
        for tag, pc in BREAKPOINTS.items():
            count_rows.append({
                "condition": condition,
                "tag": tag,
                "pc": f"0x{pc:08X}",
                "hits": counts[(condition, tag)],
                "interpretation": "count in frames 1..600 only; zero is not an unused-routine conclusion",
            })
    write_tsv(
        out / "AU3_HIT_COUNTS.tsv", count_rows,
        ["condition", "tag", "pc", "hits", "interpretation"]
    )

    maxwall = max((float(x["wall_seconds"]) for x in launches), default=0.0)
    timeout_ok = timeout_s >= 2 * maxwall
    complete = (
        len(launches) == 4 and len(frames) == 12 and
        all(x["capture_status"] == "PASS" for x in frames) and
        all(x["emulator_exit_code_decimal"] == "0" for x in launches) and
        all(x["memory_card_unchanged"] == "TRUE" for x in launches) and
        all(x["breakpoints_armed"] == "YES" for x in launches) and
        all(x["circle_press_readback"] in ("PASS", "NOT_APPLICABLE") for x in launches) and
        all(x["circle_release_readback"] in ("PASS", "NOT_APPLICABLE") for x in launches) and
        timeout_ok
    )

    report = [
        "AU3 — PCSX-REDUX HEADLESS; H6 HYBRID; INTERPRETER ONLY",
        f"H6_SHA256={H6_SHA}",
        "H6_IDENTITY=target checkpoint base + CONTROL top-level protobuf field 6; HIBRIDA, NOT TARGET-PURE",
        "SCHEDULE_C=no input; SCHEDULE_A=CIRCLE press post-load GPU::Vsync frame 60, release frame 61",
        "MATRIX=C,A x two independent launches = 4 launches total",
        "FLAGS=-debugger -interpreter; no dynarec",
        "BREAKPOINTS_ONLY=0x8001387C setter and 0x800B770C helper; getter 0x800138EC OFF",
        "BREAKPOINT_WINDOW=armed immediately on SaveStateLoaded before first post-load frame; remains active through post-load frame 600",
        "PER_HIT_FIELDS=frame, PC, a0, a1, ra, v0",
        "RAM_HASH=SHA-256 of first 2 MiB at post-load frames 180, 360, 600",
        f"TIMEOUT_PER_LAUNCH_SECONDS={timeout_s}",
        f"OBSERVED_MAX_WALL_SECONDS={maxwall:.3f}",
        f"TIMEOUT_GE_2X_OBSERVED_MAX={timeout_ok}",
        f"RUNTIME_COMPLETE={complete}",
        "Zero hits are recorded as zero observations in this window only; they do not prove a routine is unused.",
    ]
    for x in launches:
        report.append(
            f"{x['condition']}#{x['attempt']} EXIT_DECIMAL={x['emulator_exit_code_decimal']} "
            f"TIMEOUT_WRAPPER_EXIT_DECIMAL={x['timeout_wrapper_exit_decimal']} WALL={x['wall_seconds']} "
            f"MCD_UNCHANGED={x['memory_card_unchanged']} BP={x['breakpoints_armed']} "
            f"CIRCLE_PRESS={x['circle_press_readback']} CIRCLE_RELEASE={x['circle_release_readback']}"
        )
    for x in count_rows:
        report.append(f"HITS {x['condition']} {x['tag']} PC={x['pc']} COUNT={x['hits']}")
    (out / "AU3_SUMMARY.txt").write_text("\n".join(report) + "\n", encoding="utf-8")

    rc = 0 if complete else 2
    (out / "AU3_SCRIPT_EXIT_CODE.txt").write_text(f"AU3_SCRIPT_EXIT_CODE={rc}\n", encoding="utf-8")
    (out / "ACTIONS_RUN_SUMMARY.txt").write_text(
        "\n".join([
            f"STATUS={'PASS' if complete else 'INCOMPLETE'}",
            "JOB=au3-setter-helper-interpreter",
            f"RUN_ID={os.getenv('GITHUB_RUN_ID', 'TIDAK TAHU')}",
            f"SOURCE_SHA={os.getenv('GITHUB_SHA', 'TIDAK TAHU')}",
            f"H6_SHA256={H6_SHA}",
            f"EXIT_CODE={rc}",
            f"TIMEOUT_PER_LAUNCH_SECONDS={timeout_s}",
            f"TIMEOUT_GE_2X_OBSERVED_MAX={timeout_ok}",
        ]) + "\n",
        encoding="utf-8",
    )
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
