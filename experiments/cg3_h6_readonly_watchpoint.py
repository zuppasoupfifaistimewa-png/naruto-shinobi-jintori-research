#!/usr/bin/env python3
"""CG3: two independent, no-poke H6 restores with a PCSX Lua Write watchpoint."""
from __future__ import annotations
import argparse
import csv
import hashlib
import math
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

from aj2_h6_ram_probe import (
    TARGET_SHA, CONTROL_SHA, H6_EXPECTED_SHA, one, replace_top, encmsg, sha, ram_info
)

RAM180_REFERENCE = "5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7"
RAM360_REFERENCE = "4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907"
PTR_SLOT = 0x8013A22C
EXPECTED_OBJECT = 0x801CDF80
WATCH_ADDRESS = 0x801CEE28
HISTORICAL_SLOWEST_SECONDS = 145.815
EXPECTED_FRAMES = (1, 60, 180, 360, 600, 1200)

def write_lua(path: Path) -> None:
    path.write_text(r"""
if io.stdout then io.stdout:setvbuf("no") end
local ffi = require("ffi")
local mem = ffi.cast("uint8_t*", PCSX.getMemPtr())
local PTR_SLOT = 0x8013A22C
local EXPECTED_OBJECT = 0x801CDF80
local WATCH_ADDRESS = 0x801CEE28
local loaded, started, finished = false, false, false
local frame = 0
local lastValue = 0
local launchEpoch = tonumber(os.getenv("CG3_LAUNCH_EPOCH")) or os.time()
local statePath = os.getenv("CG3_H6_STATE") or "h6.sstate"
local ramDir = os.getenv("CG3_H6_RAM_DIR") or "runtime"

local function log(s)
  print(s)
  pcall(function() io.stdout:flush() end)
end
local function hex(n)
  return string.format("0x%08X", tonumber(n) % 4294967296)
end
local function u32(addr)
  local off = tonumber(addr) - 0x80000000
  return tonumber(ffi.cast("uint32_t*", mem + off)[0])
end
local function saveRam(label)
  local data = ffi.string(mem, 0x200000)
  local f, err = io.open(ramDir .. "/frame" .. label .. ".ram", "wb")
  if not f then error("RAM_SNAPSHOT_OPEN_FAILED " .. tostring(err)) end
  local ok, msg = f:write(data)
  f:close()
  if not ok then error("RAM_SNAPSHOT_WRITE_FAILED " .. tostring(msg)) end
  log("CG3_RAM_SNAPSHOT=PASS frame=" .. label .. " bytes=" .. tostring(#data))
end
local function recordFrame()
  local ptr = u32(PTR_SLOT)
  local field = u32(WATCH_ADDRESS)
  log("CG3_FRAME_SAMPLE frame=" .. tostring(frame) ..
      " pointer=" .. hex(ptr) .. " object_ea8=" .. hex(WATCH_ADDRESS) ..
      " field_value=" .. hex(field))
end
local function computedStoreValue(pc, regs, oldWord, address)
  -- Recover a pre-write value from the live MIPS store register if the write
  -- callback is invoked before the memory operation commits. No registers or
  -- emulated memory are modified by this helper.
  local addr = tonumber(address)
  for delta = 0, 8, 4 do
    local insPc = (tonumber(pc) - delta) % 4294967296
    local word = u32(insPc)
    local opcode = math.floor(word / 67108864) % 64
    if opcode == 0x28 or opcode == 0x29 or opcode == 0x2B then
      local rs = math.floor(word / 2097152) % 32
      local rt = math.floor(word / 65536) % 32
      local imm = word % 65536
      if imm >= 32768 then imm = imm - 65536 end
      local base = tonumber(regs.GPR.r[rs]) % 4294967296
      local effective = (base + imm) % 4294967296
      local size = opcode == 0x28 and 1 or (opcode == 0x29 and 2 or 4)
      if effective == addr and effective >= WATCH_ADDRESS and effective + size <= WATCH_ADDRESS + 4 then
        local lane = effective - WATCH_ADDRESS
        local shift = lane * 8
        local mod = 256 ^ size
        local oldPart = math.floor(oldWord / (256 ^ lane)) % mod
        local value = tonumber(regs.GPR.r[rt]) % mod
        local newWord = oldWord - oldPart * (256 ^ lane) + value * (256 ^ lane)
        return newWord, insPc, opcode, rs, rt, effective
      end
    end
  end
  return nil
end

_G.cg3LoadedListener = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  loaded = true
  frame = 0
  local ptr = u32(PTR_SLOT)
  local value = u32(WATCH_ADDRESS)
  log("CG3_STATE_LOADED=1 pointer_slot=" .. hex(ptr) ..
      " expected_pointer=" .. hex(EXPECTED_OBJECT) ..
      " field_address=" .. hex(WATCH_ADDRESS) .. " field_initial=" .. hex(value))
  if ptr ~= EXPECTED_OBJECT then
    log("CG3_POINTER_VERIFY=FAIL actual=" .. hex(ptr) .. " expected=" .. hex(EXPECTED_OBJECT))
    PCSX.nextTick(function()
      log("CG3_PCSX_QUIT_DECIMAL=41")
      PCSX.quit(41)
    end)
    return
  end
  if ptr + 0xEA8 ~= WATCH_ADDRESS then
    log("CG3_FIELD_ADDRESS_VERIFY=FAIL")
    PCSX.nextTick(function()
      log("CG3_PCSX_QUIT_DECIMAL=42")
      PCSX.quit(42)
    end)
    return
  end
  lastValue = value
  _G.cg3EA8WriteWatchpoint = PCSX.addBreakpoint(
    WATCH_ADDRESS, "Write", 4, "CG3 watch object+0xEA8",
    function(address, width, cause)
      local regs = PCSX.getRegisters()
      local pc = tonumber(regs.pc)
      local atCallback = u32(WATCH_ADDRESS)
      local old = lastValue
      local frameAtHit = frame
      local decoded, insPc, opcode, rs, rt, effective =
        computedStoreValue(pc, regs, old, address)
      PCSX.nextTick(function()
        local after = u32(WATCH_ADDRESS)
        local newValue = after
        local source = "MEMORY_AFTER_WRITE"
        if newValue == old and atCallback ~= old then
          newValue = atCallback
          source = "MEMORY_AT_CALLBACK"
        elseif newValue == old and decoded ~= nil then
          newValue = decoded
          source = "LIVE_STORE_REGISTER_PREWRITE"
        end
        log("CG3_WATCHPOINT frame=" .. tostring(frameAtHit) ..
            " pc=" .. hex(pc) .. " address=" .. hex(address) ..
            " width=" .. tostring(width) .. " old=" .. hex(old) ..
            " new=" .. hex(newValue) .. " source=" .. source ..
            " decoded_store_pc=" .. (insPc and hex(insPc) or "TIDAK_TAHU") ..
            " decoded_opcode=" .. (opcode and tostring(opcode) or "TIDAK_TAHU") ..
            " base_reg=" .. (rs and tostring(rs) or "TIDAK_TAHU") ..
            " value_reg=" .. (rt and tostring(rt) or "TIDAK_TAHU") ..
            " effective=" .. (effective and hex(effective) or "TIDAK_TAHU") ..
            " cause=" .. tostring(cause))
        lastValue = newValue
      end)
    end,
    "CG3_EA8_WRITE_0x801CEE28"
  )
  log("CG3_WRITE_WATCHPOINT_INSTALLED=1 address=" .. hex(WATCH_ADDRESS) .. " width=4 type=Write")
end)

_G.cg3VsyncListener = PCSX.Events.createEventListener("GPU::Vsync", function()
  if not started then
    started = true
    log("CG3_LOAD_BEGIN=1 input=NONE state=" .. statePath)
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf, f = pcall(function() return assert(Support.File.open(statePath)) end)
      if not okf or not f then
        log("CG3_STATE_OPEN_ERROR=" .. tostring(f))
        log("CG3_PCSX_QUIT_DECIMAL=50")
        PCSX.quit(50)
        return
      end
      local ok, err = pcall(function() PCSX.loadSaveState(f) end)
      f:close()
      if not ok then
        log("CG3_LOAD_ERROR=" .. tostring(err))
        log("CG3_PCSX_QUIT_DECIMAL=51")
        PCSX.quit(51)
        return
      end
      log("CG3_LOAD_CALL_RETURNED=1")
      PCSX.resumeEmulator()
    end)
    return
  end
  if loaded and not finished then
    frame = frame + 1
    if frame == 1 or frame == 60 or frame == 180 or frame == 360 or frame == 600 or frame == 1200 then
      recordFrame()
    end
    if frame == 180 or frame == 360 then
      local ok, err = pcall(function() saveRam(tostring(frame)) end)
      if not ok then
        log("CG3_RAM_SNAPSHOT_ERROR frame=" .. tostring(frame) .. " error=" .. tostring(err))
      end
    end
    if frame >= 1200 then
      finished = true
      log("CG3_COMPLETED_FRAMES=1200 elapsed_since_launch_s=" .. tostring(os.time() - launchEpoch))
      PCSX.nextTick(function()
        log("CG3_PCSX_QUIT_DECIMAL=0")
        PCSX.quit(0)
      end)
    end
  elseif not loaded and frame >= 900 then
    log("CG3_SAVE_STATE_LOAD_TIMEOUT=1")
    PCSX.nextTick(function()
      log("CG3_PCSX_QUIT_DECIMAL=53")
      PCSX.quit(53)
    end)
  end
end)
log("CG3_READY_NO_INPUT_NO_RAM_POKE=1")
""".lstrip(), encoding="utf-8")

def parse_launch_log(txt: str):
    samples = {}
    for m in re.finditer(
        r"CG3_FRAME_SAMPLE frame=(\d+) pointer=(0x[0-9A-Fa-f]+) object_ea8=(0x[0-9A-Fa-f]+) field_value=(0x[0-9A-Fa-f]+)",
        txt,
    ):
        samples[int(m.group(1))] = {
            "pointer": m.group(2).upper(), "field": m.group(4).upper(),
            "object_ea8": m.group(3).upper()
        }
    events = []
    for m in re.finditer(
        r"CG3_WATCHPOINT frame=(\d+) pc=(0x[0-9A-Fa-f]+) address=(0x[0-9A-Fa-f]+) width=(\d+) old=(0x[0-9A-Fa-f]+) new=(0x[0-9A-Fa-f]+) source=([^ ]+)",
        txt,
    ):
        events.append({
            "frame": int(m.group(1)), "pc": m.group(2).upper(),
            "address": m.group(3).upper(), "width": int(m.group(4)),
            "old": m.group(5).upper(), "new": m.group(6).upper(),
            "source": m.group(7)
        })
    return samples, events

def main():
    ap = argparse.ArgumentParser()
    for name in ("target","control","pcsx-bin","appdir","bios","cue","work","out"):
        ap.add_argument("--"+name, required=True)
    ap.add_argument("--timeout-seconds", type=int, default=3600)
    a = ap.parse_args()
    target_path, control_path = Path(a.target), Path(a.control)
    target, control = target_path.read_bytes(), control_path.read_bytes()
    if sha(target) != TARGET_SHA:
        raise SystemExit("TARGET_SHA_MISMATCH")
    if sha(control) != CONTROL_SHA:
        raise SystemExit("CONTROL_SHA_MISMATCH")
    hybrid = replace_top(target, 6, encmsg(6, one(control, 6)))
    hybrid_sha = sha(hybrid)
    if hybrid_sha != H6_EXPECTED_SHA:
        raise SystemExit("H6_COMMITTED_REFERENCE_SHA_MISMATCH actual="+hybrid_sha)
    if a.timeout_seconds < 2 * HISTORICAL_SLOWEST_SECONDS:
        raise SystemExit("TIMEOUT_BELOW_2X_HISTORICAL_SLOWEST")
    work, out = Path(a.work), Path(a.out)
    work.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    state_path = work / "h6-hybrid.sstate"
    state_path.write_bytes(hybrid)
    target_ram_sha, _, _ = ram_info(target)
    appdir = Path(a.appdir)
    capstone = work / "capstone"
    ffmpeg = work / "ffmpeg-libs"
    if not ffmpeg.joinpath("libavformat.so.63").is_file():
        raise SystemExit("PCSX_PRIVATE_FFMPEG_LIBS_NOT_PREPARED")
    library_dirs = [str(capstone), str(ffmpeg), str(appdir/"usr/lib"), str(appdir/"usr/lib/x86_64-linux-gnu")]
    env_base = os.environ.copy()
    env_base.update({
        "DISPLAY":":99","LIBGL_ALWAYS_SOFTWARE":"1",
        "LD_LIBRARY_PATH":":".join(library_dirs),
        "QT_PLUGIN_PATH":str(appdir/"usr/plugins"),
        "QT_QPA_PLATFORM_PLUGIN_PATH":str(appdir/"usr/plugins/platforms"),
        "QML2_IMPORT_PATH":str(appdir/"usr/qml"),
    })
    pad = (
        "PCSX.settings.pads[1].DeviceType = 'Analog'\n"
        "PCSX.settings.pads[1].Connected = true\n"
        "PCSX.SIO0.slots[1].pads[1].map()\n"
        "print('CG3_CONTROLLER_CONNECTED_NO_INPUT=1')\n"
    )
    launches = []
    for attempt in (1,2):
        launch_dir = work / f"launch-{attempt}"
        runtime = launch_dir / "runtime"
        logs = launch_dir / "logs"
        home = launch_dir / "home"
        for d in (runtime, logs, home/".config", home/".local/share", home/"runtime"):
            d.mkdir(parents=True, exist_ok=True)
        card = launch_dir / "disposable.mcd"
        card.write_bytes(bytes(131072))
        card_before = sha(card.read_bytes())
        lua_path = launch_dir / "cg3-h6.lua"
        write_lua(lua_path)
        pcsx_log = logs / "pcsx.log"
        env = env_base.copy()
        env.update({
            "HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),
            "XDG_DATA_HOME":str(home/".local/share"),"XDG_RUNTIME_DIR":str(home/"runtime"),
            "CG3_H6_STATE":str(state_path),"CG3_H6_RAM_DIR":str(runtime),
            "CG3_LAUNCH_EPOCH":str(time.time()),
        })
        command = [
            "timeout","--signal=INT","--kill-after=15s",f"{a.timeout_seconds}s",
            str(a.pcsx_bin),"-noupdate","-debugger","-no-gdb","-interpreter",
            "-testmode","-bios",a.bios,"-iso",a.cue,"-memcard1",str(card),
            "-exec",pad,"-dofile",str(lua_path),"-softgpu","-stdout","-lua_stdout",
            "-logfile",str(pcsx_log),"-run",
        ]
        started = time.monotonic()
        try:
            p = subprocess.run(command,cwd=launch_dir,env=env,stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,timeout=a.timeout_seconds+25,check=False)
            wrapper_rc = p.returncode
            stdout = p.stdout.decode("utf-8","replace")
        except subprocess.TimeoutExpired as exc:
            wrapper_rc = 124
            raw = exc.stdout or b""
            stdout = raw.decode("utf-8","replace") if isinstance(raw,bytes) else str(raw)
            stdout += "\nCG3_HOST_SUBPROCESS_TIMEOUT=1\n"
        except Exception as exc:
            wrapper_rc = 255
            stdout = "CG3_LAUNCH_EXCEPTION="+repr(exc)+"\n"
        wall = time.monotonic()-started
        log_text = stdout
        if pcsx_log.is_file():
            log_text += "\n--- PCSX_LOG_FILE_BEGIN ---\n"+pcsx_log.read_text(encoding="utf-8",errors="replace")+"\n--- PCSX_LOG_FILE_END ---\n"
        (out/f"CG3_LAUNCH_{attempt}_RAW_LOG.txt").write_text(log_text,encoding="utf-8")
        card_after = sha(card.read_bytes()) if card.exists() else "TIDAK TAHU"
        samples, events = parse_launch_log(log_text)
        ram_hashes = {}
        ram_lengths = {}
        for frame_no in (180,360):
            dump = runtime/f"frame{frame_no}.ram"
            if dump.is_file():
                raw = dump.read_bytes()
                ram_hashes[frame_no] = sha(raw)
                ram_lengths[frame_no] = len(raw)
                dump.unlink()
            else:
                ram_hashes[frame_no] = "TIDAK TAHU"
                ram_lengths[frame_no] = 0
        m = re.search(r"CG3_PCSX_QUIT_DECIMAL=(-?\d+)",log_text)
        lua_exit = m.group(1) if m else "TIDAK TAHU"
        pointer_ok = (
            "CG3_WRITE_WATCHPOINT_INSTALLED=1" in log_text
            and "CG3_POINTER_VERIFY=FAIL" not in log_text
            and all(samples.get(f,{}).get("pointer")=="0x801CDF80" for f in EXPECTED_FRAMES)
            and all(samples.get(f,{}).get("object_ea8")=="0x801CEE28" for f in EXPECTED_FRAMES)
        )
        samples_complete = all(f in samples for f in EXPECTED_FRAMES)
        ram180_ok = ram_lengths[180]==0x200000 and ram_hashes[180]==RAM180_REFERENCE
        ram360_ok = ram_lengths[360]==0x200000 and ram_hashes[360]==RAM360_REFERENCE
        card_unchanged = card_before == card_after
        completed = "CG3_COMPLETED_FRAMES=1200" in log_text and lua_exit=="0" and wrapper_rc==0
        launch_pass = (completed and pointer_ok and samples_complete and ram180_ok
                       and ram360_ok and card_unchanged)
        launches.append({
            "attempt":attempt,"status":"PASS" if launch_pass else "SEBAGIAN",
            "wrapper_exit_code_decimal":wrapper_rc,"lua_quit_code_decimal":lua_exit,
            "wall_seconds":round(wall,3),"timeout_seconds":a.timeout_seconds,
            "pointer_watchpoint_verified":pointer_ok,"samples_complete":samples_complete,
            "samples":samples,"events":events,
            "ram180_sha256":ram_hashes[180],"ram180_bytes":ram_lengths[180],
            "ram180_matches_reference":ram180_ok,
            "ram360_sha256":ram_hashes[360],"ram360_bytes":ram_lengths[360],
            "ram360_matches_reference":ram360_ok,
            "memory_card_sha256_before":card_before,
            "memory_card_sha256_after":card_after,"memory_card_unchanged":card_unchanged,
            "completed_1200_frames":completed,
        })
    max_wall = max((x["wall_seconds"] for x in launches),default=0)
    timeout_2x = a.timeout_seconds >= 2*max(max_wall,HISTORICAL_SLOWEST_SECONDS)
    same_samples = launches[0]["samples"]==launches[1]["samples"]
    same_events = launches[0]["events"]==launches[1]["events"]
    same_ram = (launches[0]["ram180_sha256"]==launches[1]["ram180_sha256"]
                and launches[0]["ram360_sha256"]==launches[1]["ram360_sha256"])
    overall = (all(x["status"]=="PASS" for x in launches) and timeout_2x
               and same_samples and same_events and same_ram)
    status = "PASS_K5" if overall else "SEBAGIAN"
    rows=[]
    for x in launches:
        for f in EXPECTED_FRAMES:
            sample=x["samples"].get(f,{})
            rows.append({
                "attempt":x["attempt"],"frame":f,
                "pointer":sample.get("pointer","TIDAK TAHU"),
                "field_address":sample.get("object_ea8","TIDAK TAHU"),
                "value_EA8":sample.get("field","TIDAK TAHU")
            })
    with (out/"CG3_H6_FRAME_VALUES.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["attempt","frame","pointer","field_address","value_EA8"],delimiter="\t")
        w.writeheader();w.writerows(rows)
    event_rows=[]
    for x in launches:
        for e in x["events"]:
            event_rows.append({"attempt":x["attempt"],**e})
    with (out/"CG3_H6_WRITE_WATCHPOINT.tsv").open("w",encoding="utf-8",newline="") as f:
        cols=["attempt","frame","pc","address","width","old","new","source"]
        w=csv.DictWriter(f,fieldnames=cols,delimiter="\t");w.writeheader();w.writerows(event_rows)
    lines=[
        "CG3 — H6 READ-ONLY WRITE-WATCHPOINT AUDIT",
        f"STATUS={status}",
        f"H6_SHA256={hybrid_sha}",
        f"TARGET_STATE_SHA256={TARGET_SHA}",
        f"CONTROL_STATE_SHA256={CONTROL_SHA}",
        f"POINTER_SLOT=0x{PTR_SLOT:08X}",
        f"EXPECTED_OBJECT=0x{EXPECTED_OBJECT:08X}",
        f"WATCH_ADDRESS=0x{WATCH_ADDRESS:08X} WIDTH=4 TYPE=WRITE",
        "RAM_POKE=NO (load H6 state; reads, snapshots and debugger breakpoint only)",
        "GAMEPLAY_INPUT=NONE",
        f"TIMEOUT_PER_LAUNCH_SECONDS={a.timeout_seconds}",
        f"HISTORICAL_SLOWEST_SECONDS={HISTORICAL_SLOWEST_SECONDS}",
        f"OBSERVED_MAX_LAUNCH_WALL_SECONDS={max_wall}",
        f"TIMEOUT_AT_LEAST_2X_MAX_HISTORICAL_OR_OBSERVED={timeout_2x}",
        f"FRAME180_REFERENCE_SHA256={RAM180_REFERENCE}",
        f"FRAME360_REFERENCE_SHA256={RAM360_REFERENCE}",
        f"TARGET_STATE_RAM_SHA256={target_ram_sha}",
        f"TWO_LAUNCH_FRAME_VALUES_IDENTICAL={same_samples}",
        f"TWO_LAUNCH_WATCH_EVENTS_IDENTICAL={same_events}",
        f"TWO_LAUNCH_RAM_HASHES_IDENTICAL={same_ram}",
        "RAM_DUMP_PUBLISHED=NO; 2 MiB frames 180/360 hashed locally then deleted",
        "MEMORY_CARD=disposable zeroed 128 KiB card per launch; hashes recorded",
    ]
    for x in launches:
        lines.extend([
            "",
            f"ATTEMPT_{x['attempt']}_STATUS={x['status']}",
            f"ATTEMPT_{x['attempt']}_WRAPPER_EXIT_CODE_DECIMAL={x['wrapper_exit_code_decimal']}",
            f"ATTEMPT_{x['attempt']}_LUA_QUIT_CODE_DECIMAL={x['lua_quit_code_decimal']}",
            f"ATTEMPT_{x['attempt']}_WALL_SECONDS={x['wall_seconds']}",
            f"ATTEMPT_{x['attempt']}_POINTER_AND_WATCHPOINT_VERIFIED={x['pointer_watchpoint_verified']}",
            f"ATTEMPT_{x['attempt']}_SAMPLES_COMPLETE={x['samples_complete']}",
            f"ATTEMPT_{x['attempt']}_RAM180_SHA256={x['ram180_sha256']} bytes={x['ram180_bytes']} ref_match={x['ram180_matches_reference']}",
            f"ATTEMPT_{x['attempt']}_RAM360_SHA256={x['ram360_sha256']} bytes={x['ram360_bytes']} ref_match={x['ram360_matches_reference']}",
            f"ATTEMPT_{x['attempt']}_MEMORY_CARD_BEFORE={x['memory_card_sha256_before']}",
            f"ATTEMPT_{x['attempt']}_MEMORY_CARD_AFTER={x['memory_card_sha256_after']}",
            f"ATTEMPT_{x['attempt']}_MEMORY_CARD_UNCHANGED={x['memory_card_unchanged']}",
            f"ATTEMPT_{x['attempt']}_WRITE_WATCHPOINT_EVENTS={len(x['events'])}",
        ])
    (out/"CG3_H6_READONLY_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    runner_exit = 0 if overall else 2
    (out/"CG3_SCRIPT_EXIT_CODE.txt").write_text(f"CG3_SCRIPT_EXIT_CODE={runner_exit}\n",encoding="utf-8")
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text(
        f"STATUS={'SUCCESS' if overall else 'SEBAGIAN'}\n"
        "JOB=cg3-h6-readonly-watchpoint\n"
        f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}\n"
        f"RUN_ATTEMPT={os.getenv('GITHUB_RUN_ATTEMPT','TIDAK TAHU')}\n"
        f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}\n"
        f"EXIT_CODE={runner_exit}\n"
        f"H6_SHA256={hybrid_sha}\n"
        f"TIMEOUT_PER_LAUNCH_SECONDS={a.timeout_seconds}\n",encoding="utf-8")
    print("\n".join(lines))
    raise SystemExit(runner_exit)

if __name__ == "__main__":
    main()
