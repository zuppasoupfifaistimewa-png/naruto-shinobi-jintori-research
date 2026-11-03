#!/usr/bin/env python3
"""BB3: controlled, non-gameplay calls into FUN_800D15A8 from the H6 hybrid checkpoint.

RAM writes occur only inside disposable PCSX-Redux launches. No controller input is
sent. No savestate, ROM, BIOS, RAM image, screenshots, or Memory Card bytes are
published. Only measured scalar fields and hashes are written as text/TSV.
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
RAM_BASE = 0x80000000
RAM_BYTES = 0x200000
TILE_STRIDE = 0x124
TILE_INDICES = (4, 7)
EXPECTED_FEES = {4: 100, 7: 120}
ACTION_VALUES = (3, 8)
LEVEL_VALUES = (0, 1, 2, 3, 4)
RAM_REFERENCE_A = "5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7"  # frame 180
RAM_REFERENCE_B = "4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907"  # frame 360

def sha(data):
    return hashlib.sha256(data).hexdigest()

def make_lua(action, level):
    return r'''
if io.stdout then io.stdout:setvbuf("no") end
local action = tonumber(os.getenv("BB3_ACTION")) or 3
local level = tonumber(os.getenv("BB3_LEVEL")) or 0
local TILE_INDEX = tonumber(os.getenv("BB3_TILE_INDEX")) or 4
local TILE_STRIDE = 0x124
local EXPECTED_FEE = tonumber(os.getenv("BB3_EXPECTED_FEE")) or 100
local started, loaded, postLoadVsync, prepared = false, false, 0, false
local selectHit = false
local actionDispatchHit = false
local actionAtDispatch = nil
local refreshBB004Hit = false
local refreshBE464Hit = false
local directCallStatus = "NOT_STARTED"
local directCallStarted = false
local directCallFrames = 0
local directCallStartPC = nil
local directCallStartSP = nil
local directCallStartGP = nil
local directCallReturn = 0x80011448
local mem = nil
local manager = nil
local tileBase = nil
local tile = nil
local participant = nil
local balanceAddr = nil
local pendingAddr = nil
local actionAddr = nil
local balanceOriginal = nil
local balanceTestStart = nil
local pendingBefore = nil
local tile20Before = nil
local stateGateBefore = nil
local tileFee = nil
local playerIndex = nil
local cardMarker = "BB3_RAM_TEST_ONLY_NO_CARD_WRITE=1"

local function log(s)
  print(s)
  pcall(function() io.stdout:flush() end)
end
local function rb(addr)
  local b = mem:readAt(1, addr)
  return tonumber(b[0])
end
local function rw(addr)
  local b = mem:readAt(2, addr)
  return tonumber(b[0]) + tonumber(b[1]) * 256
end
local function rd(addr)
  local b = mem:readAt(4, addr)
  return tonumber(b[0]) + tonumber(b[1]) * 256 + tonumber(b[2]) * 65536 + tonumber(b[3]) * 16777216
end
local function wb(addr, value)
  local b = Support.NewLuaBuffer(1)
  b[0] = value % 256
  mem:writeAt(b, addr)
end
local function ww(addr, value)
  local b = Support.NewLuaBuffer(2)
  b[0] = value % 256
  b[1] = math.floor(value / 256) % 256
  mem:writeAt(b, addr)
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
  local v = rw(addr)
  if v >= 32768 then return v - 65536 end
  return v
end
local function hex(v)
  return string.format("0x%08X", v)
end
local function validRamPtr(p, span)
  return p >= 0x80000000 and p + span <= 0x80200000
end
local function captureRamSnapshot(path, label)
  local ok, err = pcall(function()
    local ram = PCSX.getMemPtr()
    if ram == nil then error("PCSX.getMemPtr returned nil") end
    local file = assert(Support.File.open(path, "TRUNCATE"))
    local written = file:write(ram, 0x200000)
    file:close()
    if tonumber(written) ~= 0x200000 then
      error("RAM_CAPTURE_SHORT_WRITE=" .. tostring(written))
    end
    log(label .. "_BYTES=" .. tostring(written))
  end)
  if not ok then error(label .. "_CAPTURE_FAILED=" .. tostring(err)) end
  log(label .. "_CAPTURE=PASS")
end

local function captureRamBeforePoke()
  captureRamSnapshot("runtime/bb3-before-poke-2mib.bin", "BB3_RAM_BEFORE_POKE")
end

local function readResult()
  local bal = rd(balanceAddr)
  local pending = s16(pendingAddr)
  local tile20 = rw(tile + 0x20)
  log("BB3_BALANCE_ORIGINAL_H6=" .. tostring(balanceOriginal))
  log("BB3_BALANCE_TEST_START=" .. tostring(balanceTestStart))
  log("BB3_BALANCE_AFTER=" .. tostring(bal))
  log("BB3_PENDING_BEFORE=" .. tostring(pendingBefore))
  log("BB3_PENDING_AFTER=" .. tostring(pending))
  log("BB3_PENDING_DELTA=" .. tostring(pending - pendingBefore))
  log("BB3_TILE20_BEFORE=" .. string.format("0x%04X", tile20Before))
  log("BB3_TILE20_AFTER=" .. string.format("0x%04X", tile20))
  log("BB3_LEVEL_NIBBLE_8_11_BEFORE=" .. tostring(math.floor(tile20Before / 256) % 16))
  log("BB3_LEVEL_NIBBLE_8_11_AFTER=" .. tostring(math.floor(tile20 / 256) % 16))
  log("BB3_NIBBLE_4_7_BEFORE=" .. tostring(math.floor(tile20Before / 16) % 16))
  log("BB3_NIBBLE_4_7_AFTER=" .. tostring(math.floor(tile20 / 16) % 16))
  log("BB3_TILE0E=" .. tostring(rw(tile + 0x0E)))
  log("BB3_TILE1A_FEE=" .. tostring(rw(tile + 0x1A)))
  log("BB3_TILE1C=" .. tostring(rw(tile + 0x1C)))
  log("BB3_TILE1E=" .. tostring(rw(tile + 0x1E)))
  local selected = rb(manager + 0x4A0)
  local level8Before = math.floor(tile20Before / 256) % 16
  local level8After = math.floor(tile20 / 256) % 16
  local level4Before = math.floor(tile20Before / 16) % 16
  local level4After = math.floor(tile20 / 16) % 16
  local pendingDelta = pending - pendingBefore
  local pass = directCallStatus == "RETURNED"
      and actionDispatchHit and actionAtDispatch == action
      and selectHit and selected == TILE_INDEX
      and refreshBB004Hit and refreshBE464Hit
      and tileFee == EXPECTED_FEE
      and pendingDelta == -tileFee
      and level8After == level8Before + 1
      and level4After == level4Before + 1
  log("BB3_VALIDATION_DIRECT_CALL_RETURNED=" .. tostring(directCallStatus == "RETURNED"))
  log("BB3_VALIDATION_DISPATCH=" .. tostring(actionDispatchHit))
  log("BB3_VALIDATION_ACTION_MATCH=" .. tostring(actionAtDispatch == action))
  log("BB3_VALIDATION_SELECTOR_HIT=" .. tostring(selectHit))
  log("BB3_VALIDATION_SELECTED_INDEX=" .. tostring(selected == TILE_INDEX))
  log("BB3_VALIDATION_REFRESH_BB004=" .. tostring(refreshBB004Hit))
  log("BB3_VALIDATION_REFRESH_BE464=" .. tostring(refreshBE464Hit))
  log("BB3_VALIDATION_FEE=" .. tostring(tileFee == EXPECTED_FEE))
  log("BB3_VALIDATION_PENDING_DELTA=" .. tostring(pendingDelta == -tileFee))
  log("BB3_VALIDATION_LEVEL8=" .. tostring(level8After == level8Before + 1))
  log("BB3_VALIDATION_LEVEL4=" .. tostring(level4After == level4Before + 1))
  log("BB3_EXPECTED_FEE_LUA=" .. tostring(EXPECTED_FEE))
  log("BB3_SELECTED_TILE_INDEX=" .. tostring(selected))
  log("BB3_ACTION_DISPATCH_REACHED=" .. (actionDispatchHit and "1" or "0"))
  log("BB3_ACTION_BYTE_AT_DISPATCH=" .. tostring(actionAtDispatch or "TIDAK TAHU"))
  log("BB3_REFRESH_FUN_800BB004_REACHED=" .. (refreshBB004Hit and "1" or "0"))
  log("BB3_REFRESH_FUN_800BE464_REACHED=" .. (refreshBE464Hit and "1" or "0"))
  log("BB3_DIRECT_CALL_STATUS=" .. tostring(directCallStatus))
  log("BB3_DIRECT_CALL_START_PC=" .. (directCallStartPC and hex(directCallStartPC) or "TIDAK TAHU"))
  log("BB3_DIRECT_CALL_START_SP=" .. (directCallStartSP and hex(directCallStartSP) or "TIDAK TAHU"))
  log("BB3_DIRECT_CALL_START_GP=" .. (directCallStartGP and hex(directCallStartGP) or "TIDAK TAHU"))
  log("BB3_DIRECT_CALL_RETURN=" .. hex(directCallReturn))
  log("BB3_CALL_STATUS=" .. (pass and "PASS" or "VALIDATION_FAIL"))
end

local function initTest()
  local ok, err = pcall(function()
    mem = PCSX.getMemoryAsFile()
    manager = rd(0x8013EA74)
    tileBase = rd(0x8013EA84)
    local tileCount = rd(0x8013EAC8)
    local playerCount = rb(0x8013EA71)
    playerIndex = rw(0x8013EA6E)
    if playerCount < 1 or playerCount > 4 then error("BAD_PLAYER_COUNT=" .. tostring(playerCount)) end
    if playerIndex >= playerCount then playerIndex = 0 end
    if not validRamPtr(manager, 0x600) then error("MANAGER_POINTER_OUTSIDE_RAM=" .. hex(manager)) end
    if not validRamPtr(tileBase, (TILE_INDEX + 1) * TILE_STRIDE) then error("TILE_POINTER_OUTSIDE_RAM=" .. hex(tileBase)) end
    if tileCount <= TILE_INDEX or tileCount > 512 then error("TILE_COUNT_INVALID=" .. tostring(tileCount)) end

    tile = tileBase + TILE_INDEX * TILE_STRIDE
    participant = manager + playerIndex * 0x90
    balanceAddr = participant + 4
    pendingAddr = manager + 0x2EE + playerIndex * 2
    actionAddr = manager + 0x2EB

    balanceOriginal = rd(balanceAddr)
    tileFee = rw(tile + 0x1A)
    tile20Before = rw(tile + 0x20)
    pendingBefore = s16(pendingAddr)
    stateGateBefore = rb(0x80139EC8)
    local balStart = balanceOriginal
    if balStart < tileFee then
      balStart = math.max(1000, tileFee * 4)
      wd(balanceAddr, balStart)
    end
    balanceTestStart = balStart

    -- Isolated fixture: select an explicit participant and board record, zero only
    -- that participant's pending delta, set the tested level nibble, and arm action.
    ww(0x8013EA6E, playerIndex)
    ww(pendingAddr, 0)
    local w20 = rw(tile + 0x20)
    local staged = (w20 % 256) + level * 256 + math.floor(w20 / 4096) * 4096
    ww(tile + 0x20, staged)
    tile20Before = staged
    pendingBefore = s16(pendingAddr)
    wb(actionAddr, action)
    -- H6 can carry a nonzero 0x80139EC8 gate that diverts state-0 input flow
    -- to the alternate branch before the action selector. Neutralize it only
    -- inside this disposable emulator launch; preserve and report its source value.
    wb(0x80139EC8, 0)
    wb(0x80139F03, 0)       -- state-machine phase, not the participant action byte
    wd(0x8013EBB0, 1)       -- bypass the idle guard for this isolated function probe
    wd(0x80139BD8, 1)

    log("BB3_H6_LOADED=1")
    log("BB3_TEST_KIND=UJI_BLOK_DISPATCH_TANPA_INPUT_GAMEPLAY")
    log("BB3_ACTION=" .. tostring(action))
    log("BB3_TARGET_LEVEL_NIBBLE_8_11=" .. tostring(level))
    log("BB3_PARTICIPANT_INDEX=" .. tostring(playerIndex))
    log("BB3_PLAYER_COUNT=" .. tostring(playerCount))
    log("BB3_TILE_COUNT=" .. tostring(tileCount))
    log("BB3_MANAGER_ACTIVE_POINTER=" .. hex(manager))
    log("BB3_TILE_ARRAY_POINTER=" .. hex(tileBase))
    log("BB3_TILE4_ADDRESS=" .. hex(tile))
    log("BB3_ACTION_BYTE_BEFORE_TEST=" .. tostring(rb(actionAddr)))
    log("BB3_STATE_GATE_80139EC8_H6=" .. tostring(stateGateBefore))
    log("BB3_STATE_GATE_80139EC8_TEST=" .. tostring(rb(0x80139EC8)))
    log("BB3_STATE_PHASE_80139F03_TEST=" .. tostring(rb(0x80139F03)))
    log("BB3_BALANCE_ORIGINAL_H6=" .. tostring(balanceOriginal))
    log("BB3_BALANCE_TEST_START=" .. tostring(balanceTestStart))
    log("BB3_PENDING_BEFORE=" .. tostring(pendingBefore))
    log("BB3_TILE20_BEFORE=" .. string.format("0x%04X", tile20Before))
    log("BB3_TILE0E=" .. tostring(rw(tile + 0x0E)))
    log("BB3_TILE1A_FEE=" .. tostring(tileFee))
    log("BB3_TILE1C=" .. tostring(rw(tile + 0x1C)))
    log("BB3_TILE1E=" .. tostring(rw(tile + 0x1E)))
    log("BB3_RAM_WRITE_SCOPE=TEMPORARY_THIS_LAUNCH_ONLY")
    log(cardMarker)

    _G.bb3SelectBreakpoint = PCSX.addBreakpoint(0x800D45D8, "Exec", 4, "BB3 force tile record 4 return", function()
      selectHit = true
      local regs = PCSX.getRegisters()
      regs.GPR.n.v0 = TILE_INDEX
      local verify = PCSX.getRegisters()
      local actual = tonumber(verify.GPR.n.v0)
      log("BB3_SELECTED_TILE_OVERRIDE=" .. tostring(actual))
      if actual ~= TILE_INDEX then
        error("BB3_SELECTOR_REGISTER_WRITE_MISMATCH=" .. tostring(actual))
      end
      return false
    end)
    _G.bb3DispatchBreakpoint = PCSX.addBreakpoint(0x800D4470, "Exec", 4, "BB3 action byte dispatch", function()
      actionDispatchHit = true
      actionAtDispatch = rb(actionAddr)
      log("BB3_ACTION_DISPATCH_REACHED=1")
      log("BB3_ACTION_BYTE_AT_DISPATCH=" .. tostring(actionAtDispatch))
      return false
    end)
    _G.bb3RefreshBB004Breakpoint = PCSX.addBreakpoint(0x800D4840, "Exec", 4, "BB3 refresh helper FUN_800BB004 entry", function()
      refreshBB004Hit = true
      log("BB3_REFRESH_FUN_800BB004_REACHED=1")
      return false
    end)
    _G.bb3RefreshBE464Breakpoint = PCSX.addBreakpoint(0x800D4848, "Exec", 4, "BB3 refresh helper FUN_800BE464 entry", function()
      refreshBE464Hit = true
      log("BB3_REFRESH_FUN_800BE464_REACHED=1")
      return false
    end)
    _G.bb3ReturnBreakpoint = PCSX.addBreakpoint(directCallReturn, "Exec", 4, "BB3 direct function return sentinel", function()
      directCallStatus = "RETURNED"
      log("BB3_DIRECT_CALL_RETURN_SENTINEL=1")
      readResult()
      PCSX.quit(0)
      return false
    end)
    log("BB3_BREAKPOINTS_ARMED=DIRECT_CPU_CALL")
  end)
  if not ok then
    log("BB3_SETUP_ERROR=" .. tostring(err))
    log("BB3_CALL_STATUS=SETUP_FAIL")
    PCSX.quit(61)
    return
  end
end

_G.bb3LoadedListener = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  captureRamSnapshot("runtime/bb3-at-load-event-2mib.bin", "BB3_RAM_AT_LOAD_EVENT")
  loaded = true
  postLoadVsync = 0
  log("BB3_SAVE_STATE_LOADED=1")
end)

_G.bb3VsyncListener = PCSX.Events.createEventListener("GPU::Vsync", function()
  if not started then
    started = true
    log("BB3_H6_LOAD_BEGIN=1")
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf, file = pcall(function() return assert(Support.File.open("resume/h6-hybrid.sstate")) end)
      if not okf or not file then
        log("BB3_H6_OPEN_FAIL=" .. tostring(file))
        PCSX.quit(50)
        return
      end
      local ok, err = pcall(function() PCSX.loadSaveState(file) end)
      file:close()
      if not ok then
        log("BB3_H6_LOAD_FAIL=" .. tostring(err))
        PCSX.quit(51)
        return
      end
      log("BB3_H6_LOAD_CALL_RETURNED=1")
      PCSX.resumeEmulator()
    end)
    return
  end
  if loaded and not prepared then
    postLoadVsync = postLoadVsync + 1
    if postLoadVsync >= 180 then
      prepared = true
      PCSX.nextTick(function()
        log("BB3_POST_LOAD_VSYNC=180")
        captureRamBeforePoke()
        initTest()
        local okRegs, regs = pcall(function() return PCSX.getRegisters() end)
        if not okRegs or regs == nil then
          directCallStatus = "REGISTERS_UNAVAILABLE"
          log("BB3_DIRECT_CALL_REGISTERS_ERROR=" .. tostring(regs))
          readResult()
          PCSX.quit(65)
          return
        end
        local okSet, setErr = pcall(function()
          directCallStartPC = tonumber(regs.pc)
          directCallStartSP = tonumber(regs.GPR.n.sp)
          directCallStartGP = tonumber(regs.GPR.n.gp)
          local s0Original = tonumber(regs.GPR.n.s0)
          local s1Original = tonumber(regs.GPR.n.s1)
          local s2Original = tonumber(regs.GPR.n.s2)
          local s3Original = tonumber(regs.GPR.n.s3)
          local s4Original = tonumber(regs.GPR.n.s4)
          directCallFrameSP = directCallStartSP - 0x30
          if not validRamPtr(directCallFrameSP, 0x30) then
            error("DIRECT_CALL_FRAME_OUTSIDE_RAM=" .. hex(directCallFrameSP))
          end
          -- Recreate FUN_800D15A8's 0x30-byte prologue frame so its epilogue
          -- restores the original stack/registers and returns to the sentinel.
          wd(directCallFrameSP + 0x18, s0Original)
          wd(directCallFrameSP + 0x1C, s1Original)
          wd(directCallFrameSP + 0x20, s2Original)
          wd(directCallFrameSP + 0x24, s3Original)
          wd(directCallFrameSP + 0x28, s4Original)
          wd(directCallFrameSP + 0x2C, directCallReturn)
          -- Enter the actual action-byte switch block after the function's
          -- state/input gating. These saved registers are the block's live
          -- context: s1 is the 0x80140000 global page, s4 is the 1-byte flag.
          local live = PCSX.getRegisters()
          live.GPR.n.sp = directCallFrameSP
          live.GPR.n.ra = directCallReturn
          live.GPR.n.s1 = 0x80140000
          live.GPR.n.s4 = 1
          live.pc = 0x800D4464
          local verify = PCSX.getRegisters()
          local raActual = tonumber(verify.GPR.n.ra)
          local pcActual = tonumber(verify.pc)
          local spActual = tonumber(verify.GPR.n.sp)
          local s1Actual = tonumber(verify.GPR.n.s1)
          local s4Actual = tonumber(verify.GPR.n.s4)
          if raActual ~= directCallReturn or pcActual ~= 0x800D4464
              or spActual ~= directCallFrameSP or s1Actual ~= 0x80140000 or s4Actual ~= 1 then
            error("REGISTER_READBACK_MISMATCH pc=" .. hex(pcActual) .. " sp=" .. hex(spActual)
              .. " ra=" .. hex(raActual) .. " s1=" .. hex(s1Actual) .. " s4=" .. tostring(s4Actual))
          end
          log("BB3_DIRECT_CALL_REGISTER_READBACK=PASS")
          log("BB3_DIRECT_CALL_FRAME_SP=" .. hex(directCallFrameSP))
          log("BB3_DIRECT_CALL_S1=0x80140000")
          log("BB3_DIRECT_CALL_S4=1")
        end)
        if not okSet then
          directCallStatus = "REGISTER_WRITE_FAIL"
          log("BB3_DIRECT_CALL_REGISTER_WRITE_ERROR=" .. tostring(setErr))
          readResult()
          PCSX.quit(66)
          return
        end
        directCallStarted = true
        directCallStatus = "RUNNING"
        log("BB3_DIRECT_CALL_API=DISPATCH_BLOCK_WITH_RECREATED_FRAME")
        log("BB3_DIRECT_CALL_BEGIN=1")
        log("BB3_DIRECT_CALL_PC=0x800D4464")
        log("BB3_DIRECT_CALL_RA=" .. hex(directCallReturn))
      end)
    end
  elseif directCallStarted and directCallStatus == "RUNNING" then
    directCallFrames = directCallFrames + 1
    if directCallFrames >= 120 then
      local okRegs, regs = pcall(function() return PCSX.getRegisters() end)
      log("BB3_DIRECT_CALL_WATCHDOG=120")
      if okRegs and regs then
        log("BB3_DIRECT_CALL_STOP_PC=" .. hex(tonumber(regs.pc)))
        log("BB3_DIRECT_CALL_STOP_SP=" .. hex(tonumber(regs.GPR.n.sp)))
        log("BB3_DIRECT_CALL_STOP_RA=" .. hex(tonumber(regs.GPR.n.ra)))
      end
      directCallStatus = "WATCHDOG"
      readResult()
      PCSX.quit(67)
    end
  end
end)
log("BB3_READY_NO_GAMEPLAY_INPUT=1")
'''.lstrip()

def main():
    ap = argparse.ArgumentParser()
    for name in ("target", "control", "pcsx-bin", "appdir", "bios", "cue", "card", "work", "out"):
        ap.add_argument("--" + name, required=True)
    ap.add_argument("--timeout-seconds", type=int, default=900)
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
    ram_reference_a = RAM_REFERENCE_A
    ram_reference_b = RAM_REFERENCE_B

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
    library_dirs = [str(work/"capstone"), str(ffmpeg_dir),
        str(appdir/"usr/lib"), str(appdir/"usr/lib/x86_64-linux-gnu")
    ]
    env_base = os.environ.copy()
    env_base.update({
        "DISPLAY": ":99", "LIBGL_ALWAYS_SOFTWARE": "1",
        "LD_LIBRARY_PATH": ":".join(library_dirs),
        "QT_PLUGIN_PATH": str(appdir/"usr/plugins"),
        "QT_QPA_PLATFORM_PLUGIN_PATH": str(appdir/"usr/plugins/platforms"),
        "QML2_IMPORT_PATH": str(appdir/"usr/qml"),
    })

    rows = []
    max_wall = 0.0
    launch_total = 0
    stop_reason = "ALL_CASES_COMPLETED"
    stop = False
    test_cases = [(tile, action, level, attempt)
                   for tile in TILE_INDICES
                   for action in ACTION_VALUES
                   for level in LEVEL_VALUES
                   for attempt in (1, 2)]
    for tile_index, action, level, attempt in test_cases:
        expected_fee = EXPECTED_FEES[tile_index]
    launch_total += 1
    launch = work / "launches" / ("tile-%d-action-%d-level-%d-attempt-%d" % (tile_index, action, level, attempt))
    home = launch / "home"
    logs = launch / "logs"
    for folder in (home/".config", home/".data", home/"runtime", launch/"runtime", logs):
        folder.mkdir(parents=True, exist_ok=True)
    # PCSX runs with cwd=launch and opens this relative path from Lua.
    (launch / "resume").symlink_to(work / "resume", target_is_directory=True)
    try:
        (home/"runtime").chmod(0o700)
    except OSError:
        pass
    card = launch / "memory-card.mcd"
    shutil.copyfile(reference_card, card)
    card_before = sha(card.read_bytes())
    lua_path = launch / "bb3.lua"
    lua_path.write_text(make_lua(action, level), encoding="utf-8")
    pad_text = (
        "PCSX.settings.pads[1].DeviceType = 'Analog'\n"
        "PCSX.settings.pads[1].Connected = true\n"
        "PCSX.SIO0.slots[1].pads[1].map()\n"
        "print('BB3_CONTROLLER_MAPPED_NO_GAMEPLAY_INPUT=1')\n"
    )
    env = env_base.copy()
    env.update({
        "HOME": str(home), "XDG_CONFIG_HOME": str(home/".config"),
        "XDG_DATA_HOME": str(home/".data"), "XDG_RUNTIME_DIR": str(home/"runtime"),
        "BB3_ACTION": str(action), "BB3_LEVEL": str(level),
        "BB3_TILE_INDEX": str(tile_index), "BB3_EXPECTED_FEE": str(expected_fee),
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
    started = time.monotonic()
    with stdout_path.open("wb") as f:
        try:
            proc = subprocess.run(command, cwd=launch, env=env, stdout=f,
                                  stderr=subprocess.STDOUT, check=False)
            wrapper_rc = proc.returncode
        except Exception as exc:
            wrapper_rc = 255
            f.write(("BB3_LAUNCH_EXCEPTION=" + repr(exc) + "\n").encode())
    wall = time.monotonic() - started
    max_wall = max(max_wall, wall)
    log_text = stdout_path.read_text(encoding="utf-8", errors="replace")
    if pcsx_log_path.exists():
        log_text += "\n" + pcsx_log_path.read_text(encoding="utf-8", errors="replace")
    values = {}
    for line in log_text.splitlines():
        if line.startswith("BB3_") and "=" in line:
            k, v = line.split("=", 1)
            values[k] = v.strip()
    def consume_ram_capture(filename, marker):
        capture_path = launch / "runtime" / filename
        status = "NO_RESULT"
        digest = "TIDAK TAHU"
        byte_count = 0
        if capture_path.is_file():
            try:
                raw_ram = capture_path.read_bytes()
                byte_count = len(raw_ram)
                if byte_count == 0x200000:
                    digest = sha(raw_ram)
                    status = "PASS" if values.get(marker) == "PASS" else "MARKER_MISSING"
                else:
                    status = "SHORT_READ:%d" % byte_count
            except Exception as exc:
                status = "HASH_FAIL:" + str(exc)
            finally:
                capture_path.unlink(missing_ok=True)
        a_match = "YES" if digest == ram_reference_a else "NO"
        b_match = "YES" if digest == ram_reference_b else "NO"
        either_match = "YES" if a_match == "YES" or b_match == "YES" else "NO"
        return status, digest, byte_count, a_match, b_match, either_match
    ram_capture_status, ram_before_sha, ram_bytes, ram_ref_a, ram_ref_b, ram_reference_match = consume_ram_capture(
        "bb3-before-poke-2mib.bin", "BB3_RAM_BEFORE_POKE_CAPTURE"
    )
    load_capture_status, ram_load_sha, ram_load_bytes, load_ref_a, load_ref_b, load_ref_either = consume_ram_capture(
        "bb3-at-load-event-2mib.bin", "BB3_RAM_AT_LOAD_EVENT_CAPTURE"
    )
    card_after = sha(card.read_bytes()) if card.exists() else "TIDAK TAHU"
    result_status = values.get("BB3_CALL_STATUS", "NO_RESULT")
    if result_status == "PASS" and values.get("BB3_PENDING_DELTA") != str(-int(values.get("BB3_TILE1A_FEE", "0"))):
        result_status = "DELTA_MISMATCH"
    rows.append({
        "tile_index": tile_index, "expected_fee": expected_fee,
        "action_byte": action, "target_level_nibble_8_11": level, "attempt": attempt,
        "test_label": "UJI_PANGGILAN_FUNGSI_NO_GAMEPLAY",
        "call_status": result_status, "action_dispatch_reached": values.get("BB3_ACTION_DISPATCH_REACHED", "NO"),
        "action_byte_at_dispatch": values.get("BB3_ACTION_BYTE_AT_DISPATCH", "TIDAK TAHU"),
        "selected_tile_override": values.get("BB3_SELECTED_TILE_OVERRIDE", "NO"),
        "selected_tile_index": values.get("BB3_SELECTED_TILE_INDEX", "TIDAK TAHU"),
        "refresh_800BB004_reached": values.get("BB3_REFRESH_FUN_800BB004_REACHED", "NO"),
        "refresh_800BE464_reached": values.get("BB3_REFRESH_FUN_800BE464_REACHED", "NO"),
        "participant_index": values.get("BB3_PARTICIPANT_INDEX", "TIDAK TAHU"),
        "balance_original_h6": values.get("BB3_BALANCE_ORIGINAL_H6", "TIDAK TAHU"),
        "balance_test_start": values.get("BB3_BALANCE_TEST_START", "TIDAK TAHU"),
        "balance_after": values.get("BB3_BALANCE_AFTER", "TIDAK TAHU"),
        "pending_before": values.get("BB3_PENDING_BEFORE", "TIDAK TAHU"),
        "pending_after": values.get("BB3_PENDING_AFTER", "TIDAK TAHU"),
        "pending_delta": values.get("BB3_PENDING_DELTA", "TIDAK TAHU"),
        "tile20_before": values.get("BB3_TILE20_BEFORE", "TIDAK TAHU"),
        "tile20_after": values.get("BB3_TILE20_AFTER", "TIDAK TAHU"),
        "level_8_11_before": values.get("BB3_LEVEL_NIBBLE_8_11_BEFORE", "TIDAK TAHU"),
        "level_8_11_after": values.get("BB3_LEVEL_NIBBLE_8_11_AFTER", "TIDAK TAHU"),
        "nibble_4_7_before": values.get("BB3_NIBBLE_4_7_BEFORE", "TIDAK TAHU"),
        "nibble_4_7_after": values.get("BB3_NIBBLE_4_7_AFTER", "TIDAK TAHU"),
        "tile_0E": values.get("BB3_TILE0E", "TIDAK TAHU"),
        "tile_1A_fee": values.get("BB3_TILE1A_FEE", "TIDAK TAHU"),
        "tile_1C": values.get("BB3_TILE1C", "TIDAK TAHU"),
        "tile_1E": values.get("BB3_TILE1E", "TIDAK TAHU"),
        "memory_card_sha256_before": card_before, "memory_card_sha256_after": card_after,
        "memory_card_unchanged": "YES" if card_before == card_after else "NO",
        "ram_before_poke_capture": ram_capture_status,
        "ram_2mib_sha256_before_poke": ram_before_sha,
        "ram_bytes_before_poke": ram_bytes,
        "ram_reference_a_match": ram_ref_a,
        "ram_reference_b_match": ram_ref_b,
        "ram_reference_match_either": ram_reference_match,
        "ram_at_load_event_capture": load_capture_status,
        "ram_2mib_sha256_at_load_event": ram_load_sha,
        "ram_bytes_at_load_event": ram_load_bytes,
        "ram_at_load_reference_a_match": load_ref_a,
        "ram_at_load_reference_b_match": load_ref_b,
        "ram_at_load_reference_match_either": load_ref_either,
        "wrapper_exit_code_decimal": wrapper_rc, "wall_seconds": "%.3f" % wall,
        "timeout_seconds": timeout_s,
    })
    if result_status != "PASS" or wrapper_rc != 0:
        diag_name = "BB3_FIRST_NONPASS_T%d_A%d_L%d_ATTEMPT%d.txt" % (tile_index, action, level, attempt)
        (out / diag_name).write_text(log_text[-30000:], encoding="utf-8")
        stop_reason = ("FIRST_NONPASS tile=%d action=%d level=%d attempt=%d status=%s wrapper_exit=%d wall=%.3f" %
                       (tile_index, action, level, attempt, result_status, wrapper_rc, wall))
        stop = True
        break


    columns = list(rows[0].keys()) if rows else []
    with (out / "BB3_ACTION_CALL_RESULTS.tsv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    expected_rows = 2 * len(TILE_INDICES) * len(ACTION_VALUES) * len(LEVEL_VALUES)
    timeout_twice_observed = timeout_s >= 2 * max_wall
    validation_errors = []
    pass_rows = []
    for row in rows:
        if row["call_status"] != "PASS":
            validation_errors.append("call_status:tile%s:action%s:level%s:attempt%s" % (row["tile_index"], row["action_byte"], row["target_level_nibble_8_11"], row["attempt"]))
            continue
        def number(field):
            value = row[field]
            if isinstance(value, int):
                return value
            try:
                return int(value, 0) if str(value).lower().startswith("0x") else int(value)
            except (TypeError, ValueError):
                return None
        checks = {
            "dispatch": row["action_dispatch_reached"] == "1",
            "action_byte": number("action_byte_at_dispatch") == int(row["action_byte"]),
            "selector_override": row["selected_tile_override"] == str(int(row["tile_index"])),
            "selector_stored": number("selected_tile_index") == int(row["tile_index"]),
            "refresh_800BB004": row["refresh_800BB004_reached"] == "1",
            "refresh_800BE464": row["refresh_800BE464_reached"] == "1",
            "fee": number("tile_1A_fee") == EXPECTED_FEES[int(row["tile_index"])],
            "pending_before_zero": number("pending_before") == 0,
            "pending_after": number("pending_after") == -EXPECTED_FEES[int(row["tile_index"])],
            "pending": number("pending_delta") == -EXPECTED_FEES[int(row["tile_index"])],
            "level_before_requested": number("level_8_11_before") == int(row["target_level_nibble_8_11"]),
            "balance_start_sufficient": number("balance_test_start") is not None and number("balance_test_start") >= EXPECTED_FEES[int(row["tile_index"])],
            "level_8_11": number("level_8_11_after") == number("level_8_11_before") + 1 if number("level_8_11_before") is not None and number("level_8_11_after") is not None else False,
            "level_4_7": number("nibble_4_7_after") == number("nibble_4_7_before") + 1 if number("nibble_4_7_before") is not None and number("nibble_4_7_after") is not None else False,
            "card": row["memory_card_unchanged"] == "YES",
            "ram_capture": row["ram_before_poke_capture"] == "PASS",
            "ram_bytes": number("ram_bytes_before_poke") == 0x200000,
            "ram_load_event_capture": row["ram_at_load_event_capture"] == "PASS",
            "ram_load_event_bytes": number("ram_bytes_at_load_event") == 0x200000,
            "ram_reference_frame180": row["ram_reference_a_match"] == "YES",
            "process_exit": number("wrapper_exit_code_decimal") == 0,
        }
        failed = [name for name, passed in checks.items() if not passed]
        if failed:
            row["call_status"] = "VALIDATION_FAIL"
            validation_errors.append("tile%s/%s/%s/attempt%s:%s" % (row["tile_index"], row["action_byte"], row["target_level_nibble_8_11"], row["attempt"], ",".join(failed)))
        else:
            pass_rows.append(row)
    expected_pairs = {(tile, a, level) for tile in TILE_INDICES for a in ACTION_VALUES for level in LEVEL_VALUES}
    observed_pairs = {}
    for row in rows:
        key = (row["tile_index"], row["action_byte"], row["target_level_nibble_8_11"])
        observed_pairs.setdefault(key, []).append(row["attempt"])
    coverage_ok = len(rows) == expected_rows and set(observed_pairs) == expected_pairs and all(sorted(v) == [1, 2] for v in observed_pairs.values())
    all_pass = coverage_ok and len(pass_rows) == expected_rows and timeout_twice_observed
    control_status = "NOT_RUN"
    overall = "K5_TERBATAS" if all_pass else "SEBAGIAN"
    exit_code = 0 if all_pass else 2
    report = [
        "BB3 — H6 HYBRID TEMPORARY-RAM FUNCTION-CALL PROBE",
        "STATUS=" + overall,
        "SCOPE=Runtime confirmation of action-byte 3/8 shared transaction branch at H6 fixture; not proof that either action is the visible Barrier-placement action.",
        "TEST=UJI PANGGILAN FUNGSI; NOT GAMEPLAY; no controller button press",
        "H6_SHA256=" + h6_sha,
        "RAM_REFERENCE_A_FRAME180_SHA256=" + ram_reference_a,
        "RAM_REFERENCE_B_FRAME360_SHA256=" + ram_reference_b,
        "RAM_BEFORE_POKE_CAPTURE_ALL=" + ("YES" if len(rows) == expected_rows and all(r["ram_before_poke_capture"] == "PASS" for r in rows) else "NO"),
        "RAM_BEFORE_POKE_BYTES_ALL_2097152=" + ("YES" if len(rows) == expected_rows and all(r["ram_bytes_before_poke"] == 0x200000 for r in rows) else "NO"),
        "RAM_BEFORE_POKE_CAPTURE_FRAME=POST_LOAD_VSYNC_180",
        "RAM_BEFORE_POKE_MATCHES_FRAME180_REFERENCE_A_ALL=" + ("YES" if len(rows) == expected_rows and all(r["ram_reference_a_match"] == "YES" for r in rows) else "NO"),
        "RAM_BEFORE_POKE_MATCHES_FRAME360_REFERENCE_B_ALL=" + ("YES" if len(rows) == expected_rows and all(r["ram_reference_b_match"] == "YES" for r in rows) else "NO"),
        "RAM_BEFORE_POKE_MATCHES_EITHER_REFERENCE_ALL=" + ("YES" if len(rows) == expected_rows and all(r["ram_reference_match_either"] == "YES" for r in rows) else "NO"),
        "RAM_AT_LOAD_EVENT_CAPTURE_ALL=" + ("YES" if len(rows) == expected_rows and all(r["ram_at_load_event_capture"] == "PASS" for r in rows) else "NO"),
        "RAM_AT_LOAD_EVENT_MATCHES_REFERENCE_A_ALL=" + ("YES" if len(rows) == expected_rows and all(r["ram_at_load_reference_a_match"] == "YES" for r in rows) else "NO"),
        "RAM_AT_LOAD_EVENT_MATCHES_REFERENCE_B_ALL=" + ("YES" if len(rows) == expected_rows and all(r["ram_at_load_reference_b_match"] == "YES" for r in rows) else "NO"),
        "RAM_AT_LOAD_EVENT_MATCHES_EITHER_REFERENCE_ALL=" + ("YES" if len(rows) == expected_rows and all(r["ram_at_load_reference_match_either"] == "YES" for r in rows) else "NO"),
        "CONDITIONS=tile index 4,7 x action byte 3,8 x tile+0x20 bits8-11 level 0..4 x 2 independent launches",
        "TILE_EXPECTED_FEES=tile4:100;tile7:120",
        "LAUNCHES=%d EXPECTED=%d" % (len(rows), expected_rows),
        "PASS_LAUNCHES=%d" % len(pass_rows),
        "STOP_REASON=" + stop_reason,
        "FIRST_FAILURE_DIAGNOSTIC=" + ("PUBLISHED_TEXT_ONLY" if stop else "NONE"),
        "COVERAGE_2_ATTEMPTS_PER_ACTION_LEVEL=%s" % coverage_ok,
        "VALIDATION_ERRORS=%d" % len(validation_errors),
        "VALIDATION_ERROR_DETAILS=" + (";".join(validation_errors) if validation_errors else "NONE"),
        "TIMEOUT_SECONDS_PER_LAUNCH=%d" % timeout_s,
        "HISTORICAL_SLOWEST_LAUNCH_SECONDS=%.3f" % HISTORICAL_SLOWEST_LAUNCH_S,
        "TIMEOUT_GE_2X_HISTORICAL_SLOWEST=%s" % (timeout_s >= 2 * HISTORICAL_SLOWEST_LAUNCH_S),
        "OBSERVED_MAX_LAUNCH_SECONDS=%.3f" % max_wall,
        "TIMEOUT_GE_2X_OBSERVED_MAX=%s" % timeout_twice_observed,
        "MEMORY_CARD=DISPOSABLE_ZERO_FILLED_128_KIB",
        "MEMORY_CARD_UNCHANGED_ALL=%s" % (len(rows) == expected_rows and all(r["memory_card_unchanged"] == "YES" for r in rows)),
        "CONTROL_POSITIVE_3_OWNED_TILES_FORMULA=" + control_status,
        "CONTROL_FORMULA= floor(sum(values of 3 owned tiles)/2)+400 (user-supplied known control)",
        "NOTE=RAM pre-poke capture is at post-load VSync 180 to match the frame-180 reference. The frame-360 hash is reported as a second comparison, not expected to match the frame-180 capture.",
        "NOTE=Positive control was not executed; the formula is separate from the action-byte 3/8 branch under test.",
        "RAM_WRITES=temporary inside disposable emulator launches only; no RAM dumps or savestates published",
        "RELEASE=unchanged",
    ]
    (out / "BB3_ACTION_CALL_SUMMARY.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    (out / "BB3_SCRIPT_EXIT_CODE.txt").write_text("BB3_SCRIPT_EXIT_CODE=%d\n" % exit_code, encoding="utf-8")
    (out / "ACTIONS_RUN_SUMMARY.txt").write_text(
        "STATUS=%s\nJOB=bb3-h6-action-call-probe\nRUN_ID=%s\nSOURCE_SHA=%s\nEXIT_CODE=%d\n" %
        ("SUCCESS" if exit_code == 0 else "SEBAGIAN",
         os.getenv("GITHUB_RUN_ID", "TIDAK TAHU"), os.getenv("GITHUB_SHA", "TIDAK TAHU"), exit_code),
        encoding="utf-8")
    raise SystemExit(exit_code)

if __name__ == "__main__":
    main()
