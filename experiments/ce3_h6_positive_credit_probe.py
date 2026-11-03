#!/usr/bin/env python3
"""CE3: H6 positive-credit path through FUN_800D15A8 -> FUN_800BE5D8 -> Chakra setter.

Only scalar evidence and SHA-256 hashes are published. ROM/BIOS/savestate,
raw RAM snapshots and Memory Card bytes remain private to each disposable launch.
Each launch tests player records 0 and 1 for one tile/level condition; two
independent launches cover every player x tile(4/7) x level(0..4) condition.
"""
import argparse
import csv
import hashlib
import os
import shutil
import subprocess
import time
from pathlib import Path

from aj2_h6_ram_probe import one, replace_top, encmsg

TARGET_SHA = "00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA = "9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA = "d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
HISTORICAL_SLOWEST_LAUNCH_S = 145.815
MIN_TIMEOUT_S = 300
RAM_BYTES = 0x200000
TILE_STRIDE = 0x124
PLAYER_STRIDE = 0xB4
TILE_INDICES = (4, 7)
LEVEL_VALUES = (0, 1, 2, 3, 4)
PLAYER_INDICES = (0, 1)
TILE_RESOURCE = {4: (84, 70), 7: (112, 84)}  # (tile+0x1E base, tile+0x1C step)
RAM_REFERENCE_180 = "5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7"
RAM_REFERENCE_360 = "4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907"
CANONICAL_PLAYER_RECORD_BASE = 0x80070EA0
RETURN_SENTINEL = 0x80011448

def sha(data):
    return hashlib.sha256(data).hexdigest()

def make_lua():
    return r'''
if io.stdout then io.stdout:setvbuf("no") end
local TILE_INDEX = tonumber(os.getenv("CE3_TILE_INDEX")) or 4
local TILE_STRIDE = 0x124
local LEVEL = tonumber(os.getenv("CE3_LEVEL")) or 0
local EXPECTED_BASE = tonumber(os.getenv("CE3_EXPECTED_BASE")) or 84
local EXPECTED_STEP = tonumber(os.getenv("CE3_EXPECTED_STEP")) or 70
local EXPECTED_C = EXPECTED_BASE + LEVEL * EXPECTED_STEP
local RETURN_PC = 0x80011448
local started, loaded, postLoadVsync = false, false, 0
local frame180Captured, frame360Captured = false, false
local mem, manager, tileBase, tile, playerCount = nil, nil, nil, nil, 0
local activeCall, activePlayer, consumerCalls = nil, nil, 0
local setterCount, setterLastA0, setterLastA1 = 0, -1, -1
local results = {}
local complete = false
local expectedPlayerOrder = {0, 1}

local function log(s)
  print(s)
  pcall(function() io.stdout:flush() end)
end
local function rb(addr)
  local b = mem:readAt(1, addr); return tonumber(b[0])
end
local function rw(addr)
  local b = mem:readAt(2, addr); return tonumber(b[0]) + tonumber(b[1]) * 256
end
local function rd(addr)
  local b = mem:readAt(4, addr)
  return tonumber(b[0]) + tonumber(b[1]) * 256 + tonumber(b[2]) * 65536 + tonumber(b[3]) * 16777216
end
local function wb(addr, value)
  local b = Support.NewLuaBuffer(1); b[0] = value % 256; mem:writeAt(b, addr)
end
local function ww(addr, value)
  local b = Support.NewLuaBuffer(2)
  b[0] = value % 256; b[1] = math.floor(value / 256) % 256; mem:writeAt(b, addr)
end
local function wd(addr, value)
  local b = Support.NewLuaBuffer(4)
  b[0] = value % 256
  b[1] = math.floor(value / 256) % 256
  b[2] = math.floor(value / 65536) % 256
  b[3] = math.floor(value / 16777216) % 256
  mem:writeAt(b, addr)
end
local function s16(addr)
  local v = rw(addr); if v >= 32768 then return v - 65536 end; return v
end
local function hex(v) return string.format("0x%08X", v) end
local function validPtr(p, span) return p >= 0x80000000 and p + span <= 0x80200000 end
local function poke8(label, addr, value)
  local old = rb(addr); wb(addr, value)
  log("CE3_POKE label="..label.." addr="..hex(addr).." old="..tostring(old).." new="..tostring(value))
end
local function poke16(label, addr, value)
  local old = rw(addr); ww(addr, value)
  log("CE3_POKE label="..label.." addr="..hex(addr).." old="..tostring(old).." new="..tostring(value))
end
local function poke32(label, addr, value)
  local old = rd(addr); wd(addr, value)
  log("CE3_POKE label="..label.." addr="..hex(addr).." old="..tostring(old).." new="..tostring(value))
end
local function captureRamSnapshot(path, label)
  local ok, err = pcall(function()
    local ram = PCSX.getMemPtr()
    if ram == nil then error("PCSX.getMemPtr returned nil") end
    local file = assert(Support.File.open(path, "TRUNCATE"))
    local written = file:write(ram, 0x200000)
    file:close()
    if tonumber(written) ~= 0x200000 then error("RAM_CAPTURE_SHORT_WRITE="..tostring(written)) end
    log(label.."_BYTES="..tostring(written))
  end)
  if not ok then error(label.."_CAPTURE_FAILED="..tostring(err)) end
  log(label.."_CAPTURE=PASS")
end
local function fail(reason)
  if complete then return end
  complete = true
  log("CE3_RAW_ERROR="..tostring(reason))
  log("CE3_CALL_STATUS=FAIL")
  PCSX.quit(73)
end
local function callFunction(address, label)
  if complete then return end
  if activeCall ~= nil then error("CALL_ALREADY_ACTIVE="..tostring(activeCall)) end
  local regs = PCSX.getRegisters()
  local oldPC = tonumber(regs.pc)
  local oldSP = tonumber(regs.GPR.n.sp)
  regs.GPR.n.ra = RETURN_PC
  regs.pc = address
  local verify = PCSX.getRegisters()
  local actualPC = tonumber(verify.pc)
  local actualRA = tonumber(verify.GPR.n.ra)
  if actualPC ~= address or actualRA ~= RETURN_PC then
    error("CALL_REGISTER_READBACK_MISMATCH label="..label.." pc="..hex(actualPC).." ra="..hex(actualRA))
  end
  activeCall = label
  log("CE3_CALL_BEGIN label="..label.." entry="..hex(address).." old_pc="..hex(oldPC).." sp="..hex(oldSP).." ra="..hex(RETURN_PC))
end
local function playerAddresses(player)
  local participant = manager + player * 0x90
  local chakra = 0x80070EA0 + player * 0xB4 + 0x18
  return participant, participant + 4, manager + 0x2EE + player * 2, chakra
end
local function resetConsumerAnimator()
  for p = 0, 3 do
    poke8("anim_state_p"..p, 0x8013B7AC + p, 0)
    poke8("anim_sign_p"..p, 0x8013B7A8 + p, 0)
    poke8("anim_units_p"..p, 0x8013B7B0 + p, 0)
    poke8("anim_tens_p"..p, 0x8013B7B4 + p, 0)
    poke8("anim_hundreds_p"..p, 0x8013B7B8 + p, 0)
    poke8("anim_thousands_p"..p, 0x8013B7BC + p, 0)
    poke8("anim_ten_thousands_p"..p, 0x8013B7C0 + p, 0)
    poke32("anim_start_balance_p"..p, 0x8013B7C8 + p * 4, 0)
  end
end
local function preparePlayer(player)
  activePlayer = player
  consumerCalls = 0
  setterCount, setterLastA0, setterLastA1 = 0, -1, -1
  local participant, balanceAddr, pendingAddr, chakraAddr = playerAddresses(player)
  poke16("active_player_EA6E", 0x8013EA6E, player)
  poke16("active_player_EA88", 0x8013EA88, player)
  poke32("selected_tile_EB20", 0x8013EB20, TILE_INDEX)
  poke32("manager_state_370", manager + 0x370, 1)
  for p = 0, 3 do
    poke16("pending_clear_p"..p, manager + 0x2EE + p * 2, 0)
  end
  resetConsumerAnimator()
  poke32("working_balance_p"..player, balanceAddr, 1500)
  poke32("canonical_chakra_p"..player, chakraAddr, 1500)
  poke8("manager_action_2E9", manager + 0x2E9, 9)
  poke8("manager_action_2EA", manager + 0x2EA, 1)
  poke8("manager_action_2EB", manager + 0x2EB, 1)
  poke8("positive_credit_phase", 0x80139F03, 1)
  log("CE3_PLAYER_FIXTURE player="..player.." participant="..hex(participant).." balance="..hex(balanceAddr).." chakra="..hex(chakraAddr).." pending="..hex(pendingAddr).." expected_C="..EXPECTED_C)
  callFunction(0x800D15A8, "D15A8_STATE1_P"..player)
end
local function finishPlayer()
  local _, balanceAddr, pendingAddr, chakraAddr = playerAddresses(activePlayer)
  local actualBalance = rd(balanceAddr)
  local canonical = rd(chakraAddr)
  local pending = s16(pendingAddr)
  local expectedBalance = 1500 + EXPECTED_C
  log("CE3_PLAYER_RESULT player="..activePlayer.." tile="..TILE_INDEX.." level="..LEVEL..
      " C="..EXPECTED_C.." pending="..pending.." working_balance="..actualBalance..
      " canonical_chakra="..canonical.." expected_balance="..expectedBalance..
      " setter_calls="..setterCount.." setter_last_a0="..setterLastA0.." setter_last_a1="..setterLastA1)
  local pass = pending == 0 and actualBalance == expectedBalance and canonical == expectedBalance
      and setterCount > 0 and setterLastA0 == activePlayer and setterLastA1 == expectedBalance
  results[#results + 1] = {
    player=activePlayer, tile=TILE_INDEX, level=LEVEL, expected_credit=EXPECTED_C,
    expected_balance=expectedBalance, pending=pending, working_balance=actualBalance,
    canonical_chakra=canonical, setter_calls=setterCount,
    setter_last_a0=setterLastA0, setter_last_a1=setterLastA1, status=pass and "PASS" or "FAIL"
  }
  if not pass then error("PLAYER_VALIDATION_FAIL player="..activePlayer.." pending="..pending..
      " working="..actualBalance.." canonical="..canonical.." setters="..setterCount..
      " last_a0="..setterLastA0.." last_a1="..setterLastA1) end
end
local function onCallReturn(label)
  if label:find("^D15A8_STATE1_") then
    local phase = rb(0x80139F03)
    log("CE3_STATE1_RETURN phase="..phase)
    if phase ~= 2 then error("STATE1_DID_NOT_ADVANCE_TO_2 actual="..phase) end
    callFunction(0x800D15A8, "D15A8_STATE2_P"..activePlayer)
    return
  end
  if label:find("^D15A8_STATE2_") then
    local _, _, pendingAddr = playerAddresses(activePlayer)
    local pending = s16(pendingAddr)
    log("CE3_STATE2_RETURN phase="..rb(0x80139F03).." pending="..pending)
    if pending ~= EXPECTED_C then
      error("STATE2_PENDING_MISMATCH expected="..EXPECTED_C.." actual="..pending..
        " phase="..rb(0x80139F03).." manager370="..rd(manager + 0x370))
    end
    callFunction(0x800BE5D8, "BE5D8_P"..activePlayer.."_CALL1")
    return
  end
  if label:find("^BE5D8_") then
    consumerCalls = consumerCalls + 1
    local _, _, pendingAddr = playerAddresses(activePlayer)
    local pending = s16(pendingAddr)
    local _, _, _, chakraAddr = playerAddresses(activePlayer)
    log("CE3_CONSUMER_RETURN player="..activePlayer.." call="..consumerCalls.." pending="..pending..
      " setter_calls="..setterCount.." chakra="..rd(chakraAddr))
    if pending ~= 0 then
      if consumerCalls >= 160 then error("CONSUMER_PENDING_DID_NOT_DRAIN calls="..consumerCalls.." pending="..pending) end
      callFunction(0x800BE5D8, "BE5D8_P"..activePlayer.."_CALL"..(consumerCalls + 1))
      return
    end
    finishPlayer()
    if activePlayer == 0 then
      preparePlayer(1)
    else
      complete = true
      log("CE3_LAUNCH_STATUS=PASS")
      for i, row in ipairs(results) do
        log("CE3_LAUNCH_PLAYER_"..i.."_STATUS="..row.status.." player="..row.player..
          " C="..row.expected_credit.." chakra="..row.canonical_chakra)
      end
      PCSX.quit(0)
    end
    return
  end
  error("UNKNOWN_RETURN_LABEL="..tostring(label))
end

_G.ce3ReturnBreakpoint = PCSX.addBreakpoint(RETURN_PC, "Exec", 4, "CE3 function return sentinel", function()
  local label = activeCall
  activeCall = nil
  if label == nil then
    fail("RETURN_SENTINEL_WITHOUT_ACTIVE_CALL")
    return false
  end
  log("CE3_CALL_RETURN label="..label)
  PCSX.pauseEmulator()
  PCSX.nextTick(function()
    local ok, err = pcall(function() onCallReturn(label) end)
    if not ok then fail(err); return end
    if not complete then PCSX.resumeEmulator() end
  end)
  return false
end)
_G.ce3SetterBreakpoint = PCSX.addBreakpoint(0x800BEC98, "Exec", 4, "CE3 Chakra setter 0x8001387C callsite", function()
  local regs = PCSX.getRegisters()
  setterCount = setterCount + 1
  setterLastA0 = tonumber(regs.GPR.n.a0)
  setterLastA1 = tonumber(regs.GPR.n.a1)
  log("CE3_SETTER_CALL count="..setterCount.." a0="..setterLastA0.." a1="..setterLastA1)
  return false
end)

local function initTest()
  mem = PCSX.getMemoryAsFile()
  if mem == nil then error("PCSX.getMemoryAsFile returned nil") end
  manager = rd(0x8013EA74)
  tileBase = rd(0x8013EA84)
  local tileCount = rd(0x8013EAC8)
  playerCount = rb(0x8013EA71)
  if not validPtr(manager, 0x950) then error("MANAGER_POINTER_OUTSIDE_RAM="..hex(manager)) end
  if not validPtr(tileBase, (TILE_INDEX + 1) * 0x124) then error("TILE_POINTER_OUTSIDE_RAM="..hex(tileBase)) end
  if tileCount <= TILE_INDEX or tileCount > 512 then error("TILE_COUNT_INVALID="..tileCount) end
  if playerCount < 2 or playerCount > 4 then error("PLAYER_COUNT_LT_TWO_OR_INVALID="..playerCount) end
  tile = tileBase + TILE_INDEX * TILE_STRIDE
  for p = 0, 3 do
    poke8("test_isolated_team_p"..p, manager + p * 0x90 + 0x0E, 0xA0 + p)
  end
  local base = rw(tile + 0x1E)
  local step = rw(tile + 0x1C)
  local tile20 = rw(tile + 0x20)
  if base ~= EXPECTED_BASE or step ~= EXPECTED_STEP then
    error("RESOURCE_VALUE_MISMATCH tile="..TILE_INDEX.." base="..base.." step="..step..
      " expected_base="..EXPECTED_BASE.." expected_step="..EXPECTED_STEP)
  end
  local staged = (tile20 % 256) + LEVEL * 256 + math.floor(tile20 / 4096) * 4096
  poke16("tile_level_bits8_11", tile + 0x20, staged)
  log("CE3_H6_LOADED=1")
  log("CE3_TEST_MODE=STATIC_EVENT_STATE1_STATE2_AND_CONSUMER_CALLS_NO_CONTROLLER_INPUT")
  log("CE3_H6_SHA256="..tostring(os.getenv("CE3_H6_SHA256") or "TIDAK TAHU"))
  log("CE3_MANAGER_POINTER="..hex(manager).." tile_base="..hex(tileBase).." player_count="..playerCount)
  log("CE3_TILE_INDEX="..TILE_INDEX.." tile_address="..hex(tile).." tile_type="..rb(tile))
  log("CE3_TILE_1C_STEP="..step.." tile_1E_BASE="..base.." tile_20="..string.format("0x%04X",staged))
  log("CE3_LEVEL_BITS8_11="..LEVEL.." EXPECTED_C="..EXPECTED_C)
  log("CE3_RAM_WRITES=TEMPORARY_DISPOSABLE_LAUNCH_ONLY")
  preparePlayer(0)
end

_G.ce3LoadedListener = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  loaded = true; postLoadVsync = 0
  log("CE3_SAVE_STATE_LOADED=1")
end)
_G.ce3VsyncListener = PCSX.Events.createEventListener("GPU::Vsync", function()
  if not started then
    started = true
    log("CE3_H6_LOAD_BEGIN=1")
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf, file = pcall(function() return assert(Support.File.open("resume/h6-hybrid.sstate")) end)
      if not okf or not file then
        log("CE3_H6_OPEN_FAIL="..tostring(file)); PCSX.quit(50); return
      end
      local ok, err = pcall(function() PCSX.loadSaveState(file) end)
      file:close()
      if not ok then log("CE3_H6_LOAD_FAIL="..tostring(err)); PCSX.quit(51); return end
      log("CE3_H6_LOAD_CALL_RETURNED=1")
      PCSX.resumeEmulator()
    end)
    return
  end
  if loaded and not frame360Captured then
    postLoadVsync = postLoadVsync + 1
    if postLoadVsync == 180 then
      PCSX.nextTick(function()
        local ok, err = pcall(function()
          captureRamSnapshot("runtime/ce3-frame180-2mib.bin", "CE3_RAM_FRAME180")
          frame180Captured = true
        end)
        if not ok then fail(err) end
      end)
    elseif postLoadVsync == 360 then
      PCSX.nextTick(function()
        local ok, err = pcall(function()
          captureRamSnapshot("runtime/ce3-frame360-2mib.bin", "CE3_RAM_FRAME360")
          frame360Captured = true
          log("CE3_POST_LOAD_VSYNC=360")
          initTest()
        end)
        if not ok then fail(err) end
      end)
    end
  end
end)
log("CE3_READY_NO_GAMEPLAY_INPUT=1")
'''.lstrip()

def main():
    ap = argparse.ArgumentParser()
    for name in ("target", "control", "pcsx-bin", "appdir", "bios", "cue", "card", "work", "out"):
        ap.add_argument("--" + name, required=True)
    ap.add_argument("--timeout-seconds", type=int, default=600)
    args = ap.parse_args()

    target = Path(args.target).read_bytes()
    control = Path(args.control).read_bytes()
    if sha(target) != TARGET_SHA:
        raise SystemExit("TARGET_SAVESTATE_SHA_MISMATCH")
    if sha(control) != CONTROL_SHA:
        raise SystemExit("CONTROL_SAVESTATE_SHA_MISMATCH")
    h6 = replace_top(target, 6, encmsg(6, one(control, 6)))
    h6_sha = sha(h6)
    if h6_sha != H6_SHA:
        raise SystemExit("H6_HYBRID_SHA_MISMATCH actual=" + h6_sha)

    timeout_s = int(args.timeout_seconds)
    min_timeout = max(MIN_TIMEOUT_S, int(2 * HISTORICAL_SLOWEST_LAUNCH_S + 0.999))
    if timeout_s < min_timeout:
        raise SystemExit("TIMEOUT_TOO_SHORT required_at_least=%d" % min_timeout)

    work, out = Path(args.work), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name in ("resume", "runtime", "logs", "launches", "home"):
        (work / name).mkdir(parents=True, exist_ok=True)
    h6_path = work / "resume" / "h6-hybrid.sstate"
    h6_path.write_bytes(h6)
    reference_card = Path(args.card)
    reference_card_bytes = reference_card.read_bytes()
    if len(reference_card_bytes) != 131072:
        raise SystemExit("DISPOSABLE_MEMORY_CARD_SIZE_MISMATCH")
    if any(reference_card_bytes):
        raise SystemExit("DISPOSABLE_MEMORY_CARD_NOT_ZERO_FILLED")

    appdir = Path(args.appdir)
    ffmpeg_dir = work / "ffmpeg-libs"
    if not ffmpeg_dir.is_dir() or not (ffmpeg_dir / "libavformat.so.63").is_file():
        raise SystemExit("PCSX_PRIVATE_FFMPEG_LIBS_NOT_PREPARED")
    env_base = os.environ.copy()
    env_base.update({
        "DISPLAY": ":99", "LIBGL_ALWAYS_SOFTWARE": "1",
        "LD_LIBRARY_PATH": ":".join([str(work/"capstone"), str(ffmpeg_dir),
            str(appdir/"usr/lib"), str(appdir/"usr/lib/x86_64-linux-gnu")]),
        "QT_PLUGIN_PATH": str(appdir/"usr/plugins"),
        "QT_QPA_PLATFORM_PLUGIN_PATH": str(appdir/"usr/plugins/platforms"),
        "QML2_IMPORT_PATH": str(appdir/"usr/qml"),
    })

    rows = []
    launch_rows = []
    max_wall = 0.0
    stop_reason = "ALL_CASES_COMPLETED"
    launch_number = 0
    failed = False
    conditions = [(tile, level, attempt)
                  for tile in TILE_INDICES
                  for level in LEVEL_VALUES
                  for attempt in (1, 2)]
    if len(conditions) != 20 or len(set(conditions)) != 20:
        raise SystemExit("CE3_20_LAUNCH_MATRIX_MISMATCH")

    for tile_index, level, attempt in conditions:
        launch_number += 1
        base, step = TILE_RESOURCE[tile_index]
        expected_credit = base + level * step
        launch = work / "launches" / ("tile-%d-level-%d-attempt-%d" % (tile_index, level, attempt))
        home = launch / "home"
        logs = launch / "logs"
        runtime = launch / "runtime"
        for folder in (home/".config", home/".data", home/"runtime", runtime, logs):
            folder.mkdir(parents=True, exist_ok=True)
        (launch / "resume").symlink_to(work / "resume", target_is_directory=True)
        try:
            (home/"runtime").chmod(0o700)
        except OSError:
            pass
        card = launch / "memory-card.mcd"
        shutil.copyfile(reference_card, card)
        card_before = sha(card.read_bytes())
        lua_path = launch / "ce3.lua"
        lua_path.write_text(make_lua(), encoding="utf-8")
        pad_text = (
            "PCSX.settings.pads[1].DeviceType = 'Analog'\n"
            "PCSX.settings.pads[1].Connected = true\n"
            "PCSX.SIO0.slots[1].pads[1].map()\n"
            "print('CE3_CONTROLLER_MAPPED_NO_GAMEPLAY_INPUT=1')\n"
        )
        env = env_base.copy()
        env.update({
            "HOME": str(home), "XDG_CONFIG_HOME": str(home/".config"),
            "XDG_DATA_HOME": str(home/".data"), "XDG_RUNTIME_DIR": str(home/"runtime"),
            "CE3_TILE_INDEX": str(tile_index), "CE3_LEVEL": str(level),
            "CE3_EXPECTED_BASE": str(base), "CE3_EXPECTED_STEP": str(step),
            "CE3_H6_SHA256": h6_sha,
        })
        stdout_path = logs / "emulator-stdout.txt"
        pcsx_log_path = logs / "pcsx-redux.log"
        command = [
            "timeout", "--signal=INT", "--kill-after=10s", "%ds" % timeout_s,
            args.pcsx_bin, "-noupdate", "-debugger", "-interpreter",
            "-bios", args.bios, "-iso", args.cue, "-memcard1", str(card),
            "-exec", pad_text, "-dofile", str(lua_path),
            "-softgpu", "-stdout", "-lua_stdout", "-logfile", str(pcsx_log_path), "-run",
        ]
        print("CE3_LAUNCH_START=%d/20 tile=%d level=%d attempt=%d expected_credit=%d" %
              (launch_number, tile_index, level, attempt, expected_credit), flush=True)
        started = time.monotonic()
        with stdout_path.open("wb") as f:
            try:
                proc = subprocess.run(command, cwd=launch, env=env, stdout=f,
                                      stderr=subprocess.STDOUT, check=False)
                wrapper_rc = proc.returncode
            except Exception as exc:
                wrapper_rc = 255
                f.write(("CE3_LAUNCH_EXCEPTION=" + repr(exc) + "\n").encode())
        wall = time.monotonic() - started
        max_wall = max(max_wall, wall)
        print("CE3_LAUNCH_END=%d/20 tile=%d level=%d attempt=%d wrapper_exit=%d wall_seconds=%.3f" %
              (launch_number, tile_index, level, attempt, wrapper_rc, wall), flush=True)
        log_text = stdout_path.read_text(encoding="utf-8", errors="replace")
        if pcsx_log_path.exists():
            log_text += "\n" + pcsx_log_path.read_text(encoding="utf-8", errors="replace")
        values = {}
        for line in log_text.splitlines():
            if line.startswith("CE3_") and "=" in line:
                k, v = line.split("=", 1)
                values[k] = v.strip()

        def consume_ram_capture(filename, marker):
            capture_path = runtime / filename
            status, digest, byte_count = "NO_RESULT", "TIDAK TAHU", 0
            if capture_path.is_file():
                try:
                    raw = capture_path.read_bytes()
                    byte_count = len(raw)
                    if byte_count == RAM_BYTES:
                        digest = sha(raw)
                        status = "PASS" if values.get(marker) == "PASS" else "MARKER_MISSING"
                    else:
                        status = "SHORT_READ:%d" % byte_count
                except Exception as exc:
                    status = "HASH_FAIL:" + repr(exc)
                finally:
                    capture_path.unlink(missing_ok=True)
            return status, digest, byte_count

        ram180_status, ram180_sha, ram180_bytes = consume_ram_capture(
            "ce3-frame180-2mib.bin", "CE3_RAM_FRAME180_CAPTURE"
        )
        ram360_status, ram360_sha, ram360_bytes = consume_ram_capture(
            "ce3-frame360-2mib.bin", "CE3_RAM_FRAME360_CAPTURE"
        )
        card_after = sha(card.read_bytes()) if card.exists() else "TIDAK TAHU"
        launch_ok = values.get("CE3_LAUNCH_STATUS") == "PASS" and wrapper_rc == 0
        rows_for_launch = []
        result_lines = [x for x in log_text.splitlines() if x.startswith("CE3_PLAYER_RESULT ")]
        for textline in result_lines:
            pairs = {}
            for item in textline.split()[1:]:
                if "=" in item:
                    k, v = item.split("=", 1)
                    pairs[k] = v
            player = int(pairs.get("player", "-1"))
            row = {
                "launch": launch_number, "tile": tile_index, "level": level,
                "attempt": attempt, "player": player, "expected_credit": expected_credit,
                "expected_balance": 1500 + expected_credit,
                "pending": pairs.get("pending", "TIDAK TAHU"),
                "working_balance": pairs.get("working_balance", "TIDAK TAHU"),
                "canonical_chakra": pairs.get("canonical_chakra", "TIDAK TAHU"),
                "setter_calls": pairs.get("setter_calls", "TIDAK TAHU"),
                "setter_last_a0": pairs.get("setter_last_a0", "TIDAK TAHU"),
                "setter_last_a1": pairs.get("setter_last_a1", "TIDAK TAHU"),
                "player_status": "PASS" if pairs.get("pending") == "0"
                    and pairs.get("working_balance") == str(1500+expected_credit)
                    and pairs.get("canonical_chakra") == str(1500+expected_credit)
                    and pairs.get("setter_calls", "0").isdigit()
                    and int(pairs.get("setter_calls", "0")) > 0
                    and pairs.get("setter_last_a0") == str(player)
                    and pairs.get("setter_last_a1") == str(1500+expected_credit) else "FAIL",
                "ram180_status": ram180_status, "ram180_sha256": ram180_sha,
                "ram180_bytes": ram180_bytes, "ram180_matches_reference": "YES" if ram180_sha == RAM_REFERENCE_180 else "NO",
                "ram360_status": ram360_status, "ram360_sha256": ram360_sha,
                "ram360_bytes": ram360_bytes, "ram360_matches_reference": "YES" if ram360_sha == RAM_REFERENCE_360 else "NO",
                "memory_card_sha256_before": card_before, "memory_card_sha256_after": card_after,
                "memory_card_unchanged": "YES" if card_before == card_after else "NO",
                "wrapper_exit_code_decimal": wrapper_rc, "wall_seconds": "%.3f" % wall,
                "timeout_seconds": timeout_s,
            }
            rows_for_launch.append(row)
            rows.append(row)
        launch_pass = launch_ok and len(rows_for_launch) == 2 and all(
            row["player_status"] == "PASS" for row in rows_for_launch
        ) and ram180_status == "PASS" and ram360_status == "PASS"             and ram180_bytes == RAM_BYTES and ram360_bytes == RAM_BYTES             and ram180_sha == RAM_REFERENCE_180 and ram360_sha == RAM_REFERENCE_360             and card_before == card_after
        launch_rows.append({
            "launch": launch_number, "tile": tile_index, "level": level, "attempt": attempt,
            "status": "PASS" if launch_pass else "FAIL", "wrapper_exit_code_decimal": wrapper_rc,
            "wall_seconds": "%.3f" % wall, "ram180_bytes": ram180_bytes, "ram360_bytes": ram360_bytes, "ram180_sha256": ram180_sha, "ram360_sha256": ram360_sha,
            "memory_card_sha256_before": card_before, "memory_card_sha256_after": card_after,
            "raw_log_tail": "\n".join(log_text.splitlines()[-100:]),
        })
        if not launch_pass:
            diag = out / ("CE3_FIRST_NONPASS_TILE%d_LEVEL%d_ATTEMPT%d.txt" % (tile_index, level, attempt))
            diag.write_text(log_text[-40000:], encoding="utf-8")
            stop_reason = "FIRST_NONPASS tile=%d level=%d attempt=%d wrapper_exit=%d player_rows=%d ram180=%s ram360=%s card_unchanged=%s" % (
                tile_index, level, attempt, wrapper_rc, len(rows_for_launch), ram180_status, ram360_status, card_before == card_after
            )
            failed = True
            break

    result_columns = list(rows[0].keys()) if rows else [
        "launch","tile","level","attempt","player","expected_credit","expected_balance","pending",
        "working_balance","canonical_chakra","setter_calls","setter_last_a0","setter_last_a1",
        "player_status","ram180_status","ram180_sha256","ram180_bytes","ram180_matches_reference",
        "ram360_status","ram360_sha256","ram360_bytes","ram360_matches_reference",
        "memory_card_sha256_before","memory_card_sha256_after","memory_card_unchanged",
        "wrapper_exit_code_decimal","wall_seconds","timeout_seconds"
    ]
    with (out / "CE3_H6_CREDIT_RESULTS.tsv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=result_columns, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    with (out / "CE3_H6_CREDIT_LAUNCHES.tsv").open("w", encoding="utf-8", newline="") as f:
        columns = list(launch_rows[0].keys()) if launch_rows else [
            "launch","tile","level","attempt","status","wrapper_exit_code_decimal","wall_seconds",
            "ram180_sha256","ram360_sha256","memory_card_sha256_before","memory_card_sha256_after","raw_log_tail"
        ]
        writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t")
        writer.writeheader()
        writer.writerows(launch_rows)

    expected_conditions = {(p, tile, level) for p in PLAYER_INDICES for tile in TILE_INDICES for level in LEVEL_VALUES}
    coverage = {}
    for row in rows:
        key = (int(row["player"]), int(row["tile"]), int(row["level"]))
        coverage.setdefault(key, set()).add(int(row["attempt"]))
    coverage_ok = len(rows) == 40 and set(coverage) == expected_conditions and all(v == {1, 2} for v in coverage.values())
    max_wall_ok = timeout_s >= 2 * max_wall
    all_player_pass = len(rows) == 40 and all(row["player_status"] == "PASS" for row in rows)
    all_launch_pass = len(launch_rows) == 20 and all(row["status"] == "PASS" for row in launch_rows)
    all_pass = coverage_ok and max_wall_ok and all_player_pass and all_launch_pass and not failed
    status = "K5_TERBATAS" if all_pass else "SEBAGIAN"
    exit_code = 0 if all_pass else 2
    report = [
        "CE3 — H6 HYBRID POSITIVE-CREDIT / CANONICAL CHAKRA PROBE",
        "STATUS=" + status,
        "SCOPE=state1 -> state2 -> FUN_800BE5D8 -> setter 0x8001387C; no controller gameplay input.",
        "H6_SHA256=" + h6_sha,
        "TARGET_SOURCE_SHA256=" + TARGET_SHA,
        "CONTROL_SOURCE_SHA256=" + CONTROL_SHA,
        "RAM_REFERENCE_FRAME180_SHA256=" + RAM_REFERENCE_180,
        "RAM_REFERENCE_FRAME360_SHA256=" + RAM_REFERENCE_360,
        "CONDITION_GRID=player0/1 x tile4/7 x level0..4 x 2 independent launches",
        "LAUNCHES=%d EXPECTED=20" % len(launch_rows),
        "PLAYER_CONDITION_ROWS=%d EXPECTED=40" % len(rows),
        "COVERAGE_TWO_LAUNCHES_PER_PLAYER_TILE_LEVEL=%s" % coverage_ok,
        "PLAYER_ROWS_ALL_PASS=%s" % all_player_pass,
        "LAUNCHES_ALL_PASS=%s" % all_launch_pass,
        "TIMEOUT_SECONDS_PER_LAUNCH=%d" % timeout_s,
        "HISTORICAL_SLOWEST_LAUNCH_SECONDS=%.3f" % HISTORICAL_SLOWEST_LAUNCH_S,
        "TIMEOUT_GE_2X_OBSERVED_MAX=%s" % max_wall_ok,
        "OBSERVED_MAX_LAUNCH_SECONDS=%.3f" % max_wall,
        "FRAME180_RAM_2MIB_HASH_ALL=%s" % all(row["ram180_sha256"] == RAM_REFERENCE_180 and row["ram180_bytes"] == RAM_BYTES for row in launch_rows),
        "FRAME360_RAM_2MIB_HASH_ALL=%s" % all(row["ram360_sha256"] == RAM_REFERENCE_360 and row["ram360_bytes"] == RAM_BYTES for row in launch_rows),
        "MEMORY_CARD_UNCHANGED_ALL=%s" % all(row["memory_card_sha256_before"] == row["memory_card_sha256_after"] for row in launch_rows),
        "STOP_REASON=" + stop_reason,
        "RAM_WRITES=temporary inside disposable PCSX launches only; RAM files are hashed locally and deleted",
        "MEMORY_CARD=disposable zero-filled 128KiB per launch; before/after hash recorded",
        "NO_ROM_BIOS_SAVESTATE_RAM_DUMP_MEMORY_CARD_SCREENSHOT_VIDEO_FRAME_PUBLISHED=YES",
        "BARRIER_RELEASE_LABEL=NOT_ASSERTED",
    ]
    (out / "CE3_H6_CREDIT_SUMMARY.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    (out / "CE3_SCRIPT_EXIT_CODE.txt").write_text("CE3_SCRIPT_EXIT_CODE=%d\n" % exit_code, encoding="utf-8")
    (out / "ACTIONS_RUN_SUMMARY.txt").write_text(
        "STATUS=%s\nJOB=ce3-h6-positive-credit-probe\nRUN_ID=%s\nSOURCE_SHA=%s\nEXIT_CODE=%d\n" %
        ("SUCCESS" if exit_code == 0 else "SEBAGIAN",
         os.getenv("GITHUB_RUN_ID", "TIDAK TAHU"), os.getenv("GITHUB_SHA", "TIDAK TAHU"), exit_code),
        encoding="utf-8")
    raise SystemExit(exit_code)

if __name__ == "__main__":
    main()
