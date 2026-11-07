#!/usr/bin/env python3
"""One-launch H6 CONTROL restore check. No gameplay input, watchpoints, screenshots, or RAM export."""
from __future__ import annotations
import argparse
import os
import re
import subprocess
from pathlib import Path

SOURCE_RUN = "39907655833"
ARTIFACT_ID = "12482055310"
ARTIFACT_ZIP_SHA256 = "a0f45156dfd489f24c8dc8e122c33a048c7b9ac34b935ac828523593d21ca2a8"
CHECKPOINT_NAME = "adaptive-cycle-02-f180.sstate"
CHECKPOINT_BYTES = 21162799
CHECKPOINT_SHA256 = "705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35"

def lua_source() -> str:
    return r"""
local started = false
local loaded = false
local loadReturned = false
local preFrames = 0
local postFrames = 0
local function log(s)
  print(s)
  pcall(function() io.stdout:flush() end)
end
_G.ha4ControlLoadedListener = PCSX.Events.createEventListener(
  "ExecutionFlow::SaveStateLoaded", function()
    loaded = true
    postFrames = 0
    log("HA4_CONTROL_LOAD_EVENT=PASS")
  end
)
_G.ha4ControlVsyncListener = PCSX.Events.createEventListener(
  "GPU::Vsync", function()
    preFrames = preFrames + 1
    if not started then
      started = true
      log("HA4_CONTROL_LOAD_BEGIN=1 input=NONE watchpoints=0")
      PCSX.pauseEmulator()
      PCSX.nextTick(function()
        local okFile, file = pcall(function()
          return assert(Support.File.open("resume/adaptive-cycle-02-f180.sstate"))
        end)
        if not okFile or not file then
          log("HA4_CONTROL_OPEN_FAIL=" .. tostring(file))
          PCSX.quit(50)
          return
        end
        local okLoad, err = pcall(function() PCSX.loadSaveState(file) end)
        file:close()
        if not okLoad then
          log("HA4_CONTROL_LOAD_FAIL=" .. tostring(err))
          PCSX.quit(51)
          return
        end
        loadReturned = true
        log("HA4_CONTROL_LOAD_CALL_RETURNED=1")
        PCSX.resumeEmulator()
      end)
      return
    end
    if loaded and loadReturned then
      postFrames = postFrames + 1
      if postFrames == 60 or postFrames == 180 then
        log("HA4_CONTROL_POST_LOAD_VSYNC=" .. tostring(postFrames))
      end
      if postFrames >= 180 then
        log("HA4_CONTROL_RESULT=PASS")
        PCSX.pauseEmulator()
        PCSX.nextTick(function() PCSX.quit(0) end)
        return
      end
    elseif preFrames >= 900 then
      log("HA4_CONTROL_LOAD_EVENT_TIMEOUT=1")
      PCSX.pauseEmulator()
      PCSX.nextTick(function() PCSX.quit(53) end)
    end
  end
)
log("HA4_CONTROL_READY=1 gameplay_input=NONE watchpoints=0")
"""

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pcsx-bin", required=True, type=Path)
    ap.add_argument("--bios", required=True, type=Path)
    ap.add_argument("--cue", required=True, type=Path)
    ap.add_argument("--card", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--timeout-seconds", type=int, default=240)
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    required = (
        args.pcsx_bin, args.bios, args.cue, args.card,
        args.work / "resume" / CHECKPOINT_NAME,
    )
    for path in required:
        if not path.is_file():
            raise SystemExit(f"REQUIRED_INPUT_MISSING={path}")
    if args.pcsx_bin.stat().st_size == 0:
        raise SystemExit("PCSX_BINARY_EMPTY")
    if args.bios.stat().st_size != 524288:
        raise SystemExit("BIOS_SIZE_MISMATCH")
    if args.card.stat().st_size != 131072:
        raise SystemExit("MEMORY_CARD_SIZE_MISMATCH")

    lua = args.work / "ha4-control.lua"
    lua.write_text(lua_source(), encoding="utf-8")
    stdout_path = args.out / "HA4_CONTROL_LAUNCH.txt"
    pcsx_log = args.out / "HA4_CONTROL_PCSX_LOG.txt"
    env = os.environ.copy()
    env["HOME"] = str(args.work / "home")
    env["XDG_CONFIG_HOME"] = str(args.work / "home" / ".config")
    env["XDG_DATA_HOME"] = str(args.work / "home" / ".data")
    env["XDG_RUNTIME_DIR"] = str(args.work / "home" / "runtime")
    for directory in (env["HOME"], env["XDG_CONFIG_HOME"], env["XDG_DATA_HOME"], env["XDG_RUNTIME_DIR"]):
        Path(directory).mkdir(parents=True, exist_ok=True)

    command = [
        "timeout", "--signal=INT", "--kill-after=10s", f"{args.timeout_seconds}s",
        str(args.pcsx_bin), "-noupdate", "-debugger", "-interpreter",
        "-bios", str(args.bios), "-iso", str(args.cue), "-memcard1", str(args.card),
        "-dofile", str(lua), "-softgpu", "-dynarec", "-stdout", "-lua_stdout",
        "-logfile", str(pcsx_log), "-run",
    ]
    with stdout_path.open("w", encoding="utf-8") as stream:
        stream.write("HA4_CONTROL_LAUNCH_COUNT=1\n")
        stream.write("HA4_CONTROL_GAMEPLAY_INPUT=NONE\n")
        stream.write("HA4_CONTROL_WATCHPOINTS=0\n")
        stream.write(f"HA4_CONTROL_CHECKPOINT={CHECKPOINT_NAME}\n")
        stream.flush()
        try:
            wrapper_rc = subprocess.run(
                command, cwd=args.work, env=env, stdout=stream,
                stderr=subprocess.STDOUT, check=False
            ).returncode
        except Exception as exc:
            wrapper_rc = 255
            stream.write("HA4_CONTROL_LAUNCH_EXCEPTION=" + repr(exc) + "\n")

    content = stdout_path.read_text(encoding="utf-8", errors="replace")
    if pcsx_log.exists():
        content += "\n" + pcsx_log.read_text(encoding="utf-8", errors="replace")
    loaded = "HA4_CONTROL_LOAD_EVENT=PASS" in content
    returned = "HA4_CONTROL_LOAD_CALL_RETURNED=1" in content
    passed = "HA4_CONTROL_RESULT=PASS" in content
    marks = re.findall(r"HA4_CONTROL_POST_LOAD_VSYNC=(\d+)", content)
    final_frames = max((int(mark) for mark in marks), default=0)
    status = "PASS" if wrapper_rc == 0 and loaded and returned and passed and final_frames >= 180 else "FAIL"
    summary = [
        f"STATUS={status}",
        f"SOURCE_RUN={SOURCE_RUN}",
        f"ARTIFACT_ID={ARTIFACT_ID}",
        f"ARTIFACT_ZIP_SHA256={ARTIFACT_ZIP_SHA256}",
        f"CHECKPOINT_NAME={CHECKPOINT_NAME}",
        f"CHECKPOINT_BYTES={CHECKPOINT_BYTES}",
        f"CHECKPOINT_SHA256={CHECKPOINT_SHA256}",
        "CONTROL_LAUNCHES=1",
        "GAMEPLAY_INPUT=NONE",
        "WATCHPOINTS=0",
        f"SAVE_STATE_LOADED_EVENT={'PASS' if loaded else 'FAIL'}",
        f"LOAD_CALL_RETURNED={'YES' if returned else 'NO'}",
        f"POST_LOAD_VSYNC={final_frames}",
        f"PCSX_EXIT_CODE={wrapper_rc}",
        "RAM_DUMP_EXPORTED=no",
        "SCREENSHOT_OR_VIDEO_COMMITTED=no",
    ]
    (args.out / "HA4_CONTROL_SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    return 0 if status == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
