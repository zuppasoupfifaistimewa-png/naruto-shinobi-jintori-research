#!/usr/bin/env python3
"""FA4: bounded H6-hybrid action-8 write-watchpoint probe; text-only output."""
import argparse
import csv
import hashlib
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

from aj2_h6_ram_probe import one, replace_top, encmsg

TARGET_SHA = "00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA = "9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA = "d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
HISTORICAL_SLOWEST_LAUNCH_S = 145.815
TILE_INDEX = 4
TILE_STRIDE = 0x124
TIMEOUT_MINIMUM = 300

def sha(data):
    return hashlib.sha256(data).hexdigest()

def make_lua(difference, attempt):
    lua = r'''
if io.stdout then io.stdout:setvbuf("no") end
local TEST_D = @@D@@
local ATTEMPT = @@ATTEMPT@@
local TILE_INDEX = 4
local TILE_STRIDE = 0x124
local RETURN_PC = 0x80011448
local loaded, started, prepared = false, false, false
local frame, watchdog = 0, 0
local mem, manager, tileBase, tile, pendingAddr = nil, nil, nil, nil, nil
local playerIndex, pendingIndex, actionAddr = nil, nil, nil
local fee, pendingStart, tile20Start, globalEfcStart, globalEb0cStart = nil, nil, nil, nil, nil
local callCount, dispatchHits, selectorHits = 0, 0, 0
local directStatus = "NOT_STARTED"
local callPendingBefore, callTile20Before = nil, nil
local watchpoints = {}
local allBp = {}
local refreshBB004Hits, refreshBE464Hits = 0, 0
local function log(s)
  print(s)
  pcall(function() io.stdout:flush() end)
end
local function readByte(a)
  local b = mem:readAt(1, a)
  return tonumber(b[0])
end
local function readWord(a)
  local b = mem:readAt(4, a)
  return tonumber(b[0]) + tonumber(b[1])*256 + tonumber(b[2])*65536 + tonumber(b[3])*16777216
end
local function readValue(a, n)
  local b = mem:readAt(n, a)
  local v = 0
  for i=0,n-1 do v = v + tonumber(b[i]) * (256^i) end
  return v
end
local function writeValue(a, n, value)
  local b = Support.NewLuaBuffer(n)
  for i=0,n-1 do b[i] = math.floor(value / (256^i)) % 256 end
  mem:writeAt(b, a)
end
local function signed16(v)
  if v >= 32768 then return v - 65536 end
  return v
end
local function hex(v)
  return string.format("0x%08X", tonumber(v) % 4294967296)
end
local function fieldValue(word, address, size)
  local lane = address % 4
  return math.floor(word / (256^lane)) % (256^size)
end
local function decodeStore(pc, regs, wordBase)
  for delta=0,8,4 do
    local ip = (tonumber(pc) - delta) % 4294967296
    if ip >= 0x80000000 and ip + 4 <= 0x80200000 then
      local ins = readWord(ip)
      local op = math.floor(ins / 67108864) % 64
      if op == 0x28 or op == 0x29 or op == 0x2B then
        local rs = math.floor(ins / 2097152) % 32
        local rt = math.floor(ins / 65536) % 32
        local imm = ins % 65536
        if imm >= 32768 then imm = imm - 65536 end
        local base = tonumber(regs.GPR.r[rs]) % 4294967296
        local effective = (base + imm) % 4294967296
        local size = op == 0x28 and 1 or (op == 0x29 and 2 or 4)
        if effective >= wordBase and effective + size <= wordBase + 4 then
          local offset = effective - wordBase
          local bytes = {}
          for i=0,3 do bytes[i] = math.floor(readWord(wordBase) / (256^i)) % 256 end
          local oldPart = 0
          for i=0,size-1 do oldPart = oldPart + bytes[offset+i] * (256^i) end
          local newPart = tonumber(regs.GPR.r[rt]) % (256^size)
          local newWord = readWord(wordBase) - oldPart*(256^offset) + newPart*(256^offset)
          return newWord, ip, op, rs, rt, effective
        end
      end
    end
  end
  return nil
end
local function installWatch(tag, address, size)
  local base = math.floor(address / 4) * 4
  local shadow = readWord(base)
  local bp = PCSX.addBreakpoint(base, "Write", 4, "FA4 "..tag, function(actualAddress, width, cause)
    local ok, err = pcall(function()
      local regs = PCSX.getRegisters()
      local pc = tonumber(regs.pc)
      local now = readWord(base)
      local nextWord, method = nil, nil
      local decodedPc, opcode, rs, rt, effective = nil, nil, nil, nil, nil
      if now ~= shadow then
        nextWord, method = now, "MEMORY_AFTER_OR_AT_CALLBACK"
      else
        nextWord, decodedPc, opcode, rs, rt, effective = decodeStore(pc, regs, base)
        method = nextWord and "LIVE_STORE_REGISTER_DECODE" or "UNRESOLVED"
      end
      if nextWord == nil then nextWord = now end
      local oldField = fieldValue(shadow, address, size)
      local newField = fieldValue(nextWord, address, size)
      if oldField ~= newField then
        log(string.format(
          "FA4_EVENT d=%d attempt=%d frame=%d tag=%s pc=%s field_address=%s access_address=%s access_width=%s old=%s new=%s old_word=%s new_word=%s method=%s decoded_store_pc=%s opcode=%s base_reg=%s value_reg=%s effective=%s cause=%s",
          TEST_D, ATTEMPT, frame, tag, hex(pc), hex(address), hex(tonumber(actualAddress)),
          tostring(width), hex(oldField), hex(newField), hex(shadow), hex(nextWord), method,
          decodedPc and hex(decodedPc) or "TIDAK_TAHU",
          opcode and string.format("0x%02X",opcode) or "TIDAK_TAHU",
          rs and tostring(rs) or "TIDAK_TAHU", rt and tostring(rt) or "TIDAK_TAHU",
          effective and hex(effective) or "TIDAK_TAHU", tostring(cause)))
      end
      shadow = nextWord
    end)
    if not ok then log("FA4_WATCH_CALLBACK_ERROR tag="..tag.." error="..tostring(err)) end
    return true
  end)
  allBp[#allBp+1] = bp
  watchpoints[#watchpoints+1] = {tag=tag,address=address,size=size,bp=bp}
  log("FA4_WATCHPOINT_ARMED tag="..tag.." address="..hex(address)..
      " aligned_base="..hex(base).." field_width="..tostring(size).." bp="..tostring(bp ~= nil))
  return bp ~= nil
end
local function sampleNow(callNo, pendingBefore, tile20Before)
  local pendingNow = signed16(readValue(pendingAddr,2))
  local tile20Now = readValue(tile+0x20,2)
  local tileFeeNow = readValue(tile+0x1A,2)
  local gEfc = readWord(0x80139EFC)
  local gEb0c = readWord(0x8013EB0C)
  log("FA4_ACTION8_CALL_SAMPLE d="..TEST_D.." attempt="..ATTEMPT..
      " call="..callNo.." frame="..frame.." action_byte="..readByte(actionAddr)..
      " pending_before="..pendingBefore.." pending_after="..pendingNow..
      " pending_delta="..(pendingNow-pendingBefore)..
      " pending_cumulative="..(pendingNow-signed16(pendingStart))..
      " tile20_before="..string.format("0x%04X",tile20Before)..
      " tile20_after="..string.format("0x%04X",tile20Now)..
      " tile1A_fee="..tileFeeNow..
      " global_80139EFC="..hex(gEfc).." global_8013EB0C="..hex(gEb0c))
  return pendingNow, tile20Now
end
local function beginCall()
  local ok, err = pcall(function()
    local regs = PCSX.getRegisters()
    local startSp = tonumber(regs.GPR.n.sp)
    local frameSp = startSp - 0x30
    if frameSp < 0x80000000 or frameSp + 0x30 > 0x80200000 then
      error("DIRECT_CALL_FRAME_OUTSIDE_RAM="..hex(frameSp))
    end
    writeValue(frameSp+0x18,4,tonumber(regs.GPR.n.s0))
    writeValue(frameSp+0x1C,4,tonumber(regs.GPR.n.s1))
    writeValue(frameSp+0x20,4,tonumber(regs.GPR.n.s2))
    writeValue(frameSp+0x24,4,tonumber(regs.GPR.n.s3))
    writeValue(frameSp+0x28,4,tonumber(regs.GPR.n.s4))
    writeValue(frameSp+0x2C,4,RETURN_PC)
    local live = PCSX.getRegisters()
    live.GPR.n.sp = frameSp
    live.GPR.n.ra = RETURN_PC
    live.GPR.n.s1 = 0x80140000
    live.GPR.n.s4 = 1
    live.pc = 0x800D4464
    local verify = PCSX.getRegisters()
    if tonumber(verify.pc) ~= 0x800D4464 or
       tonumber(verify.GPR.n.sp) ~= frameSp or
       tonumber(verify.GPR.n.ra) ~= RETURN_PC or
       tonumber(verify.GPR.n.s1) ~= 0x80140000 or
       tonumber(verify.GPR.n.s4) ~= 1 then
      error("DIRECT_CALL_REGISTER_READBACK_MISMATCH")
    end
    callPendingBefore = signed16(readValue(pendingAddr,2))
    callTile20Before = readValue(tile+0x20,2)
    directStatus = "RUNNING"
    log("FA4_ACTION8_CALL_BEGIN d="..TEST_D.." attempt="..ATTEMPT..
        " call="..(callCount+1).." frame="..frame.." pc=0x800D4464")
  end)
  if not ok then
    directStatus = "BEGIN_FAIL"
    log("FA4_DIRECT_CALL_BEGIN_ERROR="..tostring(err))
    PCSX.quit(66)
  end
end
local function finish()
  local pendingNow = signed16(readValue(pendingAddr,2))
  local tile20Now = readValue(tile+0x20,2)
  log("FA4_LUA_STATUS=COMPLETE")
  log("FA4_DIRECT_CALL_STATUS="..directStatus)
  log("FA4_CALLS_RETURNED="..callCount)
  log("FA4_ACTION8_DISPATCH_HITS="..dispatchHits)
  log("FA4_SELECTOR_HITS="..selectorHits)
  log("FA4_REFRESH_BB004_HITS="..refreshBB004Hits)
  log("FA4_REFRESH_BE464_HITS="..refreshBE464Hits)
  log("FA4_WATCHPOINT_COUNT="..#watchpoints)
  log("FA4_MANAGER_POINTER="..hex(manager))
  log("FA4_TILE_ARRAY_POINTER="..hex(tileBase))
  log("FA4_TILE_ADDRESS="..hex(tile))
  log("FA4_PENDING_ADDRESS="..hex(pendingAddr))
  log("FA4_PENDING_INDEX_FROM_8013EB0C="..tostring(pendingIndex))
  log("FA4_PLAYER_INDEX_FROM_8013EA6E="..tostring(playerIndex))
  log("FA4_TILE1A_INITIAL_FEE="..tostring(fee))
  log("FA4_PENDING_INITIAL="..tostring(signed16(pendingStart)))
  log("FA4_PENDING_FINAL="..tostring(pendingNow))
  log("FA4_PENDING_TOTAL_DELTA="..tostring(pendingNow-signed16(pendingStart)))
  log("FA4_TILE20_INITIAL="..string.format("0x%04X",tile20Start))
  log("FA4_TILE20_FINAL="..string.format("0x%04X",tile20Now))
  log("FA4_GLOBAL_80139EFC_INITIAL="..hex(globalEfcStart))
  log("FA4_GLOBAL_8013EB0C_INITIAL="..hex(globalEb0cStart))
  log("FA4_FRAME_FINAL="..frame)
  PCSX.nextTick(function() PCSX.quit(0) end)
end
local function setupAfterLoad()
  local ok, err = pcall(function()
    mem = PCSX.getMemoryAsFile()
    if mem == nil then error("PCSX_GET_MEM_PTR_NIL") end
    manager = readWord(0x8013EA74)
    tileBase = readWord(0x8013EA84)
    local tileCount = readWord(0x8013EAC8)
    playerIndex = readValue(0x8013EA6E,2)
    pendingIndex = readWord(0x8013EB0C)
    if pendingIndex > 3 then error("PENDING_INDEX_FROM_8013EB0C_OUT_OF_RANGE="..pendingIndex) end
    if playerIndex > 3 then error("PLAYER_INDEX_FROM_8013EA6E_OUT_OF_RANGE="..playerIndex) end
    if manager < 0x80000000 or manager+0x600 > 0x80200000 then error("MANAGER_POINTER_INVALID="..hex(manager)) end
    if tileBase < 0x80000000 or tileBase+(TILE_INDEX+1)*TILE_STRIDE > 0x80200000 then error("TILE_POINTER_INVALID="..hex(tileBase)) end
    if tileCount <= TILE_INDEX or tileCount > 512 then error("TILE_COUNT_INVALID="..tileCount) end
    tile = tileBase + TILE_INDEX*TILE_STRIDE
    actionAddr = manager + 0x2EB
    pendingAddr = manager + 0x2EE + pendingIndex*2
    local participant = manager + playerIndex*0x90
    local balanceAddr = participant + 4
    local balanceBefore = readWord(balanceAddr)
    fee = readValue(tile+0x1A,2)
    local balanceStart = balanceBefore
    if balanceStart < fee then
      balanceStart = math.max(1000, fee*4)
      writeValue(balanceAddr,4,balanceStart)
    end
    pendingStart = signed16(readValue(pendingAddr,2))
    writeValue(pendingAddr,2,0)
    local w20 = readValue(tile+0x20,2)
    tile20Start = (w20 - (math.floor(w20/256)%16)*256) + 0*256
    writeValue(tile+0x20,2,tile20Start)
    writeValue(actionAddr,1,8)
    globalEfcStart = readWord(0x80139EFC)
    globalEb0cStart = readWord(0x8013EB0C)
    writeValue(0x80139EC8,1,0)
    writeValue(0x80139F03,1,0)
    writeValue(0x8013EBB0,4,1)
    writeValue(0x80139BD8,4,1)
    pendingStart = readValue(pendingAddr,2)
    tile20Start = readValue(tile+0x20,2)
    log("FA4_H6_LOADED=1")
    log("FA4_TEST_SCOPE=CONTROLLED_ACTION8_DISPATCH_NO_GAMEPLAY_INPUT")
    log("FA4_TARGET_D="..TEST_D.." ATTEMPT="..ATTEMPT)
    log("FA4_BALANCE_BEFORE="..balanceBefore.." BALANCE_TEST_START="..balanceStart)
    log("FA4_MANAGER_POINTER="..hex(manager))
    log("FA4_TILE_ARRAY_POINTER="..hex(tileBase))
    log("FA4_TILE_ADDRESS="..hex(tile))
    log("FA4_TILE_COUNT="..tileCount)
    log("FA4_PENDING_INDEX_FROM_8013EB0C="..pendingIndex)
    log("FA4_PLAYER_INDEX_FROM_8013EA6E="..playerIndex)
    log("FA4_PENDING_ADDRESS="..hex(pendingAddr))
    log("FA4_ACTION_BYTE_ADDRESS="..hex(actionAddr))
    log("FA4_ACTION_BYTE_STAGED="..readByte(actionAddr))
    log("FA4_TILE1A_INITIAL_FEE="..fee)
    log("FA4_TILE20_STAGED="..string.format("0x%04X",tile20Start))
    log("FA4_PENDING_STAGED="..signed16(pendingStart))
    log("FA4_GLOBAL_80139EFC_INITIAL="..hex(globalEfcStart))
    log("FA4_GLOBAL_8013EB0C_INITIAL="..hex(globalEb0cStart))
    local okW = true
    okW = installWatch("MANAGER_PENDING_2EE",pendingAddr,2) and okW
    okW = installWatch("TILE_PLUS20",tile+0x20,2) and okW
    okW = installWatch("TILE_PLUS1A",tile+0x1A,2) and okW
    okW = installWatch("GLOBAL_80139EFC",0x80139EFC,4) and okW
    okW = installWatch("GLOBAL_8013EB0C",0x8013EB0C,4) and okW
    log("FA4_WATCHPOINT_SET count="..#watchpoints)
    if not okW or #watchpoints ~= 5 then error("FA4_WATCHPOINT_INSTALL_FAILED") end
    _G.fa4Selector = PCSX.addBreakpoint(0x800D45D8,"Exec",4,"FA4 selected tile return",function()
      selectorHits = selectorHits + 1
      local regs = PCSX.getRegisters()
      regs.GPR.n.v0 = TILE_INDEX
      local check = PCSX.getRegisters()
      if tonumber(check.GPR.n.v0) ~= TILE_INDEX then error("FA4_SELECTOR_OVERRIDE_FAILED") end
      return false
    end)
    _G.fa4Dispatch = PCSX.addBreakpoint(0x800D4470,"Exec",4,"FA4 action byte dispatch",function()
      dispatchHits = dispatchHits + 1
      log("FA4_ACTION8_DISPATCH frame="..frame.." hit="..dispatchHits.." action="..readByte(actionAddr))
      return false
    end)
    _G.fa4RefreshBB004 = PCSX.addBreakpoint(0x800D4840,"Exec",4,"FA4 refresh BB004",function()
      refreshBB004Hits = refreshBB004Hits + 1
      return false
    end)
    _G.fa4RefreshBE464 = PCSX.addBreakpoint(0x800D4848,"Exec",4,"FA4 refresh BE464",function()
      refreshBE464Hits = refreshBE464Hits + 1
      return false
    end)
    _G.fa4Return = PCSX.addBreakpoint(RETURN_PC,"Exec",4,"FA4 action return sentinel",function()
      callCount = callCount + 1
      local pendingNow, tile20Now = sampleNow(callCount,callPendingBefore,callTile20Before)
      directStatus = "RETURNED"
      if callCount < TEST_D then
        PCSX.nextTick(function() beginCall() end)
      else
        finish()
      end
      return false
    end)
    log("FA4_WATCHPOINTS_AND_EXEC_BREAKPOINTS_READY=1")
    beginCall()
  end)
  if not ok then
    log("FA4_SETUP_ERROR="..tostring(err))
    directStatus = "SETUP_FAIL"
    log("FA4_LUA_STATUS=SETUP_FAIL")
    PCSX.quit(61)
  end
end
_G.fa4Loaded = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
  loaded = true
  frame = 0
  log("FA4_SAVE_STATE_LOADED=1")
end)
_G.fa4Vsync = PCSX.Events.createEventListener("GPU::Vsync",function()
  if not started then
    started = true
    log("FA4_H6_LOAD_BEGIN=1")
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf, f = pcall(function() return assert(Support.File.open("resume/h6-hybrid.sstate")) end)
      if not okf or not f then log("FA4_H6_OPEN_FAIL="..tostring(f)); PCSX.quit(50); return end
      local ok, err = pcall(function() PCSX.loadSaveState(f) end)
      f:close()
      if not ok then log("FA4_H6_LOAD_FAIL="..tostring(err)); PCSX.quit(51); return end
      log("FA4_H6_LOAD_CALL_RETURNED=1")
      PCSX.resumeEmulator()
    end)
    return
  end
  if loaded then
    frame = frame + 1
    if not prepared and frame >= 180 then
      prepared = true
      PCSX.nextTick(function() setupAfterLoad() end)
    elseif directStatus == "RUNNING" then
      watchdog = watchdog + 1
      if watchdog >= 120 then
        local regs = PCSX.getRegisters()
        log("FA4_WATCHDOG=120 frame="..frame.." pc="..hex(tonumber(regs.pc))..
            " sp="..hex(tonumber(regs.GPR.n.sp)).." ra="..hex(tonumber(regs.GPR.n.ra)))
        directStatus = "WATCHDOG"
        log("FA4_LUA_STATUS=WATCHDOG")
        PCSX.quit(67)
      end
    end
  end
end)
log("FA4_READY_NO_GAMEPLAY_INPUT=1 d="..TEST_D.." attempt="..ATTEMPT)
'''
    return lua.replace("@@D@@", str(difference)).replace("@@ATTEMPT@@", str(attempt))

def write_tsv(path, rows, columns):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def parse_values(log_text):
    values = {}
    for line in log_text.splitlines():
        if line.startswith("FA4_") and "=" in line:
            k, v = line.split("=", 1)
            values[k] = v.strip()
    return values

def main():
    ap = argparse.ArgumentParser()
    for name in ("target","control","pcsx-bin","appdir","bios","cue","card","work","out"):
        ap.add_argument("--"+name, required=True)
    ap.add_argument("--timeout-seconds", type=int, default=360)
    a = ap.parse_args()
    if a.timeout_seconds < max(TIMEOUT_MINIMUM, int(2*HISTORICAL_SLOWEST_LAUNCH_S+0.999)):
        raise SystemExit("TIMEOUT_TOO_SHORT_FOR_HISTORICAL_RUNTIME")
    target, control = Path(a.target).read_bytes(), Path(a.control).read_bytes()
    if sha(target) != TARGET_SHA:
        raise SystemExit("TARGET_CHECKPOINT_SHA_MISMATCH")
    if sha(control) != CONTROL_SHA:
        raise SystemExit("CONTROL_CHECKPOINT_SHA_MISMATCH")
    h6 = replace_top(target, 6, encmsg(6, one(control,6)))
    h6_sha = sha(h6)
    if h6_sha != H6_SHA:
        raise SystemExit("H6_HYBRID_SHA_MISMATCH="+h6_sha)
    work, out = Path(a.work), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name in ("resume","launches","ffmpeg-libs","capstone"):
        (work/name).mkdir(parents=True, exist_ok=True)
    h6path = work/"resume"/"h6-hybrid.sstate"
    h6path.write_bytes(h6)
    refcard = Path(a.card).read_bytes()
    if len(refcard) != 131072 or any(refcard):
        raise SystemExit("REFERENCE_CARD_MUST_BE_ZERO_FILLED_128K")
    appdir = Path(a.appdir)
    ffmpeg = work/"ffmpeg-libs"
    capstone = work/"capstone"
    if not (ffmpeg/"libavformat.so.63").is_file() or not (capstone/"libcapstone.so.5").is_file():
        raise SystemExit("PCSX_PRIVATE_LIBRARIES_NOT_READY")
    env0 = os.environ.copy()
    env0.update({
        "DISPLAY":":99","LIBGL_ALWAYS_SOFTWARE":"1",
        "LD_LIBRARY_PATH":":".join([str(capstone),str(ffmpeg),str(appdir/"usr/lib"),str(appdir/"usr/lib/x86_64-linux-gnu")]),
        "QT_PLUGIN_PATH":str(appdir/"usr/plugins"),
        "QT_QPA_PLATFORM_PLUGIN_PATH":str(appdir/"usr/plugins/platforms"),
        "QML2_IMPORT_PATH":str(appdir/"usr/qml"),
    })
    launches, samples, events, diagnostics = [], [], [], []
    max_wall = 0.0
    stop_after_d = None
    for d in (1,2,3,4):
        for attempt in (1,2):
            label = "d%d-attempt%d" % (d,attempt)
            root = work/"launches"/label
            home = root/"home"
            logs = root/"logs"
            runtime = root/"runtime"
            for p in (home/".config",home/".data",home/"runtime",logs,runtime):
                p.mkdir(parents=True,exist_ok=True)
            try: (home/"runtime").chmod(0o700)
            except OSError: pass
            (root/"resume").symlink_to(work/"resume",target_is_directory=True)
            card = root/"memory-card.mcd"
            card.write_bytes(refcard)
            card_before = sha(card.read_bytes())
            lua = root/"fa4.lua"
            lua.write_text(make_lua(d,attempt),encoding="utf-8")
            pad_text = (
                "PCSX.settings.pads[1].DeviceType='Analog'\n"
                "PCSX.settings.pads[1].Connected=true\n"
                "PCSX.SIO0.slots[1].pads[1].map()\n"
                "print('FA4_CONTROLLER_MAPPED_NO_INPUT=1')\n"
            )
            env = env0.copy()
            env.update({
                "HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),
                "XDG_DATA_HOME":str(home/".data"),"XDG_RUNTIME_DIR":str(home/"runtime")
            })
            stdout = logs/"emulator-stdout.txt"
            pcsxlog = logs/"pcsx-redux.log"
            command = [
                "timeout","--signal=INT","--kill-after=10s",str(a.timeout_seconds)+"s",
                a.pcsx_bin,"-noupdate","-debugger","-interpreter",
                "-bios",a.bios,"-iso",a.cue,"-memcard1",str(card),
                "-exec",pad_text,"-dofile",str(lua),
                "-softgpu","-stdout","-lua_stdout","-logfile",str(pcsxlog),"-run"
            ]
            start = time.monotonic()
            with stdout.open("wb") as f:
                try:
                    wrapper_rc = subprocess.run(command,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT,check=False).returncode
                except Exception as exc:
                    wrapper_rc = 255
                    f.write(("FA4_LAUNCH_EXCEPTION="+repr(exc)+"\n").encode())
            wall = time.monotonic()-start
            max_wall = max(max_wall,wall)
            txt = stdout.read_text(encoding="utf-8",errors="replace")
            if pcsxlog.exists():
                txt += "\n"+pcsxlog.read_text(encoding="utf-8",errors="replace")
            values = parse_values(txt)
            event_pat = re.compile(
                r"FA4_EVENT d=(\d+) attempt=(\d+) frame=(\d+) tag=(\S+) pc=(\S+) field_address=(\S+) access_address=(\S+) access_width=(\S+) old=(\S+) new=(\S+) old_word=(\S+) new_word=(\S+) method=(\S+) decoded_store_pc=(\S+) opcode=(\S+) base_reg=(\S+) value_reg=(\S+) effective=(\S+) cause=(.*)"
            )
            seen = set()
            for m in event_pat.finditer(txt):
                key = m.groups()
                if key in seen: continue
                seen.add(key)
                events.append({
                    "difference_d":key[0],"attempt":key[1],"frame":key[2],"tag":key[3],
                    "pc":key[4],"field_address":key[5],"access_address":key[6],
                    "access_width":key[7],"old_value":key[8],"new_value":key[9],
                    "old_aligned_word":key[10],"new_aligned_word":key[11],
                    "value_source":key[12],"decoded_store_pc":key[13],
                    "opcode":key[14],"base_register":key[15],"value_register":key[16],
                    "effective_address":key[17],"cause":key[18]
                })
            sample_pat = re.compile(
                r"FA4_ACTION8_CALL_SAMPLE d=(\d+) attempt=(\d+) call=(\d+) frame=(\d+) action_byte=(\d+) pending_before=(-?\d+) pending_after=(-?\d+) pending_delta=(-?\d+) pending_cumulative=(-?\d+) tile20_before=(0x[0-9A-Fa-f]+) tile20_after=(0x[0-9A-Fa-f]+) tile1A_fee=(\d+) global_80139EFC=(\S+) global_8013EB0C=(\S+)"
            )
            for m in sample_pat.finditer(txt):
                k=m.groups()
                samples.append({
                    "difference_d":k[0],"attempt":k[1],"call":k[2],"frame":k[3],
                    "action_byte":k[4],"pending_before":k[5],"pending_after":k[6],
                    "pending_delta_this_call":k[7],"pending_cumulative":k[8],
                    "tile20_before":k[9],"tile20_after":k[10],"tile1A_fee_sample":k[11],
                    "global_80139EFC":k[12],"global_8013EB0C":k[13],
                    "evidence_label":"SAMPLE_RUNTIME_CONTROLLED_DISPATCH"
                })
            card_after = sha(card.read_bytes()) if card.exists() else "TIDAK_TAHU"
            lua_status = values.get("FA4_LUA_STATUS","NO_RESULT")
            call_status = values.get("FA4_DIRECT_CALL_STATUS","NO_RESULT")
            launch_row = {
                "difference_d":d,"attempt":attempt,
                "h6_restore":"PASS" if "FA4_H6_LOAD_CALL_RETURNED=1" in txt and "FA4_SAVE_STATE_LOADED=1" in txt else "FAIL",
                "watchpoint_count":values.get("FA4_WATCHPOINT_COUNT","TIDAK_TAHU"),
                "calls_returned":values.get("FA4_CALLS_RETURNED","0"),
                "action8_dispatch_hits":values.get("FA4_ACTION8_DISPATCH_HITS","0"),
                "selector_hits":values.get("FA4_SELECTOR_HITS","0"),
                "pending_address":values.get("FA4_PENDING_ADDRESS","TIDAK_TAHU"),
                "pending_index":values.get("FA4_PENDING_INDEX_FROM_8013EB0C","TIDAK_TAHU"),
                "tile_address":values.get("FA4_TILE_ADDRESS","TIDAK_TAHU"),
                "tile_fee":values.get("FA4_TILE1A_INITIAL_FEE","TIDAK_TAHU"),
                "pending_total_delta":values.get("FA4_PENDING_TOTAL_DELTA","TIDAK_TAHU"),
                "lua_status":lua_status,"direct_call_status":call_status,
                "wrapper_exit_code_decimal":wrapper_rc,"wall_seconds":"%.3f"%wall,
                "timeout_seconds":a.timeout_seconds,
                "memory_card_unchanged":"YES" if card_before==card_after else "NO",
                "memory_card_sha256":card_after
            }
            launches.append(launch_row)
            if lua_status not in ("COMPLETE",) or int(launch_row["calls_returned"]) != d or int(launch_row["action8_dispatch_hits"]) != d or launch_row["watchpoint_count"] != "5" or wrapper_rc != 0:
                diagnostics.append({
                    "difference_d":d,"attempt":attempt,"reason":lua_status,
                    "h6_restore":launch_row["h6_restore"],
                    "watchpoint_count":launch_row["watchpoint_count"],
                    "calls_returned":launch_row["calls_returned"],
                    "action8_dispatch_hits":launch_row["action8_dispatch_hits"],
                    "wrapper_exit_code_decimal":wrapper_rc,
                    "log_tail":txt[-12000:]
                })
                if attempt == 2 and launch_row["h6_restore"] == "PASS" and int(launch_row["action8_dispatch_hits"]) == 0:
                    stop_after_d = d
            print("FA4_LAUNCH d=%d attempt=%d wrapper_exit=%d wall=%.3f calls=%s dispatch=%s status=%s" %
                  (d,attempt,wrapper_rc,wall,launch_row["calls_returned"],launch_row["action8_dispatch_hits"],lua_status),flush=True)
        if stop_after_d == d:
            break
    launch_cols = list(launches[0].keys()) if launches else ["difference_d","attempt","lua_status"]
    sample_cols = ["difference_d","attempt","call","frame","action_byte","pending_before","pending_after",
                   "pending_delta_this_call","pending_cumulative","tile20_before","tile20_after",
                   "tile1A_fee_sample","global_80139EFC","global_8013EB0C","evidence_label"]
    event_cols = ["difference_d","attempt","frame","tag","pc","field_address","access_address",
                  "access_width","old_value","new_value","old_aligned_word","new_aligned_word",
                  "value_source","decoded_store_pc","opcode","base_register","value_register","effective_address","cause"]
    write_tsv(out/"FA4_LAUNCHES.tsv",launches,launch_cols)
    write_tsv(out/"FA4_ACTION8_SAMPLES.tsv",samples,sample_cols)
    write_tsv(out/"FA4_WRITE_EVENTS.tsv",events,event_cols)
    if diagnostics:
        with (out/"FA4_FAILURE_DIAGNOSTICS.txt").open("w",encoding="utf-8") as f:
            for x in diagnostics:
                f.write("D=%s ATTEMPT=%s REASON=%s H6=%s WATCHPOINTS=%s CALLS=%s DISPATCH=%s EXIT=%s\n" %
                        (x["difference_d"],x["attempt"],x["reason"],x["h6_restore"],x["watchpoint_count"],x["calls_returned"],x["action8_dispatch_hits"],x["wrapper_exit_code_decimal"]))
                f.write(x["log_tail"]+"\n---\n")
    expected = {(d,a) for d in (1,2,3,4) for a in (1,2)}
    observed = {(int(x["difference_d"]),int(x["attempt"])) for x in launches}
    coverage = observed == expected
    all_pass = coverage and len(launches)==8 and all(
        x["h6_restore"]=="PASS" and x["lua_status"]=="COMPLETE" and
        int(x["calls_returned"])==int(x["difference_d"]) and
        int(x["action8_dispatch_hits"])==int(x["difference_d"]) and
        x["watchpoint_count"]=="5" and x["memory_card_unchanged"]=="YES" and
        int(x["wrapper_exit_code_decimal"])==0 for x in launches
    )
    timeout_ok = a.timeout_seconds >= 2*max_wall
    action8_reached = any(int(x["action8_dispatch_hits"])>0 for x in launches)
    if all_pass and timeout_ok:
        status = "K5_TERBATAS"
        exit_code = 0
    elif action8_reached:
        status = "SEBAGIAN"
        exit_code = 2
    else:
        status = "BELUM"
        exit_code = 2
    lines = [
        "FA4 — H6 HYBRID ACTION-8 WRITE-WATCHPOINT RUNTIME",
        "STATUS="+status,
        "H6_SHA256="+h6_sha,
        "LAUNCHES=%d EXPECTED_MAX=8" % len(launches),
        "COVERAGE_ALL_D1_D4_TWO_LAUNCHES="+str(coverage),
        "ACTION8_DISPATCH_REACHED="+("YES_CONTROLLED_DISPATCH" if action8_reached else "NO_OR_UNKNOWN"),
        "NORMAL_GAMEPLAY_INPUT_REACHABILITY=TIDAK_DIUJI_NO_CONTROLLER_INPUT",
        "TEST_SCOPE=temporary register/RAM setup then controlled entry at PC 0x800D4464; not normal UI/gameplay execution",
        "WATCHPOINTS=manager+0x2EE+2*global_0x8013EB0C;tile+0x20;tile+0x1A;global_0x80139EFC;global_0x8013EB0C",
        "WATCHPOINT_EVENT_COUNT=%d" % len(events),
        "ACTION8_CALL_SAMPLE_COUNT=%d" % len(samples),
        "TIMEOUT_SECONDS_PER_LAUNCH=%d" % a.timeout_seconds,
        "HISTORICAL_SLOWEST_LAUNCH_SECONDS=%.3f" % HISTORICAL_SLOWEST_LAUNCH_S,
        "OBSERVED_MAX_LAUNCH_SECONDS=%.3f" % max_wall,
        "TIMEOUT_GE_2X_OBSERVED_MAX="+str(timeout_ok),
        "NO_GAMEPLAY_BUTTON_INPUT=YES",
        "RAM_WRITES=temporary per disposable emulator process; not published",
        "SAVESTATE_ROM_BIOS_RAM_DUMP_VIDEO_FRAME=NOT_COMMITTED",
        "MEMORY_CARD=disposable zero-filled copy; unchanged="+str(all(x["memory_card_unchanged"]=="YES" for x in launches)),
        "FORMULA_CONCLUSION=TIDAK_DITETAPKAN; runtime values are samples only",
        "RELEASE=unchanged",
        "SCRIPT_EXIT_CODE=%d" % exit_code
    ]
    (out/"FA4_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text(
        "STATUS=%s\nJOB=fa4-h6-upgrade-watchpoints\nRUN_ID=%s\nSOURCE_SHA=%s\nEXIT_CODE=%d\n" %
        (status,os.getenv("GITHUB_RUN_ID","TIDAK_TAHU"),os.getenv("GITHUB_SHA","TIDAK_TAHU"),exit_code),
        encoding="utf-8")
    raise SystemExit(exit_code)

if __name__ == "__main__":
    main()
