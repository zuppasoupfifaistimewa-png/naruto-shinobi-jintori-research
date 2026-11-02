#!/usr/bin/env python3
"""BB3 smoke test: verify H6 load + safe PCSX memory-file reads before any RAM writes."""
import argparse, hashlib, os, shutil, subprocess, time
from pathlib import Path
from aj2_h6_ram_probe import one, replace_top, encmsg

TARGET_SHA="00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA="9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA="d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"

LUA = r"""
if io.stdout then io.stdout:setvbuf("no") end
local started, loaded, post, pending = false, false, 0, false
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
_G.bb3SmokeLoaded = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  loaded = true
  post = 0
  log("BB3_SMOKE_SAVE_STATE_LOADED=1")
end)
_G.bb3SmokeVsync = PCSX.Events.createEventListener("GPU::Vsync", function()
  if not started then
    started = true
    log("BB3_SMOKE_LOAD_BEGIN=1")
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf, file = pcall(function() return assert(Support.File.open("resume/h6-hybrid.sstate")) end)
      if not okf or not file then log("BB3_SMOKE_OPEN_FAIL="..tostring(file)); PCSX.quit(50); return end
      local ok, err = pcall(function() PCSX.loadSaveState(file) end)
      file:close()
      if not ok then log("BB3_SMOKE_LOAD_FAIL="..tostring(err)); PCSX.quit(51); return end
      log("BB3_SMOKE_LOAD_CALL_RETURNED=1")
      PCSX.resumeEmulator()
    end)
    return
  end
  if loaded then
    post = post + 1
    if post == 2 and not pending then
      pending = true
      PCSX.nextTick(function()
        local ok, result = pcall(function()
          local mem = PCSX.getMemoryAsFile()
          local a = mem:readAt(4, 0x8013EA84)
          local b = mem:readAt(4, 0x8013EAC8)
          local c = mem:readAt(4, 0x8013EA74)
          local function u32(x)
            return tonumber(x[0]) + tonumber(x[1])*256 + tonumber(x[2])*65536 + tonumber(x[3])*16777216
          end
          local base, count, manager = u32(a), u32(b), u32(c)
          log("BB3_SMOKE_TILE_ARRAY="..string.format("0x%08X", base))
          log("BB3_SMOKE_TILE_COUNT="..tostring(count))
          log("BB3_SMOKE_MANAGER="..string.format("0x%08X", manager))
          if base < 0x80000000 or base >= 0x80200000 then error("tile base outside PSX RAM") end
          if count < 1 or count > 512 then error("implausible tile count") end
          if manager < 0x80000000 or manager >= 0x80200000 then error("manager outside PSX RAM") end
          log("BB3_SMOKE_MEMFILE_READ=PASS")
        end)
        if not ok then log("BB3_SMOKE_MEMFILE_READ=FAIL "..tostring(result)); PCSX.quit(61); return end
        PCSX.quit(0)
      end)
    end
  end
end)
log("BB3_SMOKE_READY=1")
"""

def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser()
    for n in ("target","control","pcsx-bin","appdir","bios","cue","card","work","out"):
        ap.add_argument("--"+n,required=True)
    ap.add_argument("--timeout-seconds",type=int,default=900)
    a=ap.parse_args()
    target=Path(a.target).read_bytes(); control=Path(a.control).read_bytes()
    if sha(target)!=TARGET_SHA: raise SystemExit("TARGET_SHA_MISMATCH")
    if sha(control)!=CONTROL_SHA: raise SystemExit("CONTROL_SHA_MISMATCH")
    h6=replace_top(target,6,encmsg(6,one(control,6)))
    if sha(h6)!=H6_SHA: raise SystemExit("H6_SHA_MISMATCH")
    work,out=Path(a.work),Path(a.out); out.mkdir(parents=True,exist_ok=True)
    for n in ("resume","launch","home","logs"): (work/n).mkdir(parents=True,exist_ok=True)
    (work/"resume/h6-hybrid.sstate").write_bytes(h6)
    card=Path(a.card)
    card_bytes=card.read_bytes()
    if len(card_bytes)!=131072: raise SystemExit("DISPOSABLE_MEMORY_CARD_SIZE_MISMATCH")
    if any(card_bytes): raise SystemExit("DISPOSABLE_MEMORY_CARD_NOT_ZERO_FILLED")
    launch=work/"launch"; home=work/"home"; logs=work/"logs"
    # PCSX runs with cwd=launch and opens resume/h6-hybrid.sstate relative to it.
    (launch/"resume").symlink_to(work/"resume",target_is_directory=True)
    for p in (home/".config",home/".data",home/"runtime"): p.mkdir(parents=True,exist_ok=True)
    try: (home/"runtime").chmod(0o700)
    except OSError: pass
    run_card=launch/"memory-card.mcd"; shutil.copyfile(card,run_card)
    card_before=sha(run_card.read_bytes())
    lua=launch/"bb3-smoke.lua"; lua.write_text(LUA,encoding="utf-8")
    pad=("PCSX.settings.pads[1].DeviceType = 'Analog'\n"
         "PCSX.settings.pads[1].Connected = true\n"
         "PCSX.SIO0.slots[1].pads[1].map()\n"
         "print('BB3_SMOKE_CONTROLLER_MAPPED_NO_GAMEPLAY_INPUT=1')\n")
    appdir=Path(a.appdir); env=os.environ.copy()
    env.update({"DISPLAY":":99","LIBGL_ALWAYS_SOFTWARE":"1",
      "LD_LIBRARY_PATH":str(appdir/"usr/lib")+":"+str(appdir/"usr/lib/x86_64-linux-gnu"),
      "QT_PLUGIN_PATH":str(appdir/"usr/plugins"),
      "QT_QPA_PLATFORM_PLUGIN_PATH":str(appdir/"usr/plugins/platforms"),
      "QML2_IMPORT_PATH":str(appdir/"usr/qml"),
      "HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),
      "XDG_DATA_HOME":str(home/".data"),"XDG_RUNTIME_DIR":str(home/"runtime")})
    cmd=["timeout","--signal=INT","--kill-after=10s",str(a.timeout_seconds)+"s",
      a.pcsx_bin,"-noupdate","-debugger","-interpreter","-bios",a.bios,
      "-iso",a.cue,"-memcard1",str(run_card),"-exec",pad,"-dofile",str(lua),
      "-softgpu","-stdout","-lua_stdout","-logfile",str(logs/"pcsx-redux.log"),"-run"]
    start=time.monotonic()
    with (logs/"emulator-stdout.txt").open("wb") as f:
      proc=subprocess.run(cmd,cwd=launch,env=env,stdout=f,stderr=subprocess.STDOUT,check=False)
    elapsed=time.monotonic()-start
    stdout=(logs/"emulator-stdout.txt").read_text(encoding="utf-8",errors="replace")
    pcsx=(logs/"pcsx-redux.log").read_text(encoding="utf-8",errors="replace") if (logs/"pcsx-redux.log").exists() else ""
    combined=stdout+"\n"+pcsx
    (out/"BB3_SMOKE_EMULATOR_LOG.txt").write_text(combined[-50000:],encoding="utf-8")
    card_after=sha(run_card.read_bytes()) if run_card.exists() else "TIDAK TAHU"
    markers=[x for x in combined.splitlines() if "BB3_SMOKE_" in x]
    mem_pass="BB3_SMOKE_MEMFILE_READ=PASS" in combined
    load_pass="BB3_SMOKE_SAVE_STATE_LOADED=1" in combined
    exit_code=0 if proc.returncode==0 and load_pass and mem_pass and card_after==card_before else 2
    status="PASS" if exit_code==0 else "SEBAGIAN"
    summary=[
      "BB3 SMOKE — H6 LOAD + PCSX MEMORY-FILE READ (NO RAM WRITE)",
      "STATUS="+status,"H6_SHA256="+H6_SHA,
      "RUN_EXIT_CODE="+str(proc.returncode),"WALL_SECONDS=%.3f"%elapsed,
      "H6_LOAD_EVENT="+("PASS" if load_pass else "FAIL"),
      "MEMORY_FILE_READ="+("PASS" if mem_pass else "FAIL"),
      "MEMORY_CARD_UNCHANGED="+("YES" if card_after==card_before else "NO"),
      "MEMORY_CARD_SHA256_BEFORE="+card_before,"MEMORY_CARD_SHA256_AFTER="+card_after,
      "RAM_WRITES=NONE","GAMEPLAY_INPUT=NONE","MARKERS_BEGIN"
    ]+markers+["MARKERS_END"]
    (out/"BB3_SMOKE_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    (out/"BB3_SMOKE_SCRIPT_EXIT_CODE.txt").write_text("BB3_SMOKE_SCRIPT_EXIT_CODE=%d\n"%exit_code,encoding="utf-8")
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text(
      "STATUS=%s\nJOB=bb3-h6-smoke\nRUN_ID=%s\nSOURCE_SHA=%s\nEXIT_CODE=%d\n"%
      (status,os.getenv("GITHUB_RUN_ID","TIDAK TAHU"),os.getenv("GITHUB_SHA","TIDAK TAHU"),exit_code),encoding="utf-8")
    raise SystemExit(exit_code)
if __name__=="__main__": main()
