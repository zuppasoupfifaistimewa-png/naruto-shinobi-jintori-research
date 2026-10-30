#!/usr/bin/env python3
"""Run two independent H6 CIRCLE timing conditions in headless PCSX-Redux."""
from __future__ import annotations
import argparse, csv, os, re, shutil, subprocess, time
from pathlib import Path
from aj2_h6_ram_probe import one, replace_top, encmsg, sha

TARGET_SHA = "00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA = "9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA = "d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
FRAMES = (1, 60, 180, 240, 360)
RAM_BYTES = 0x200000
ADDRESSES = (0x80070EB8, 0x80070F6C, 0x800A3118, 0x8013A554)


def ram2m(state):
    ram = one(one(state, 3), 1)
    if len(ram) < RAM_BYTES:
        raise ValueError(f"decoded RAM segment too short: {len(ram)}")
    return ram[:RAM_BYTES], len(ram)


def word_text(ram):
    out = []
    for address in ADDRESSES:
        raw = ram[address - 0x80000000:address - 0x80000000 + 4]
        if len(raw) != 4:
            raise ValueError(f"address outside first 2 MiB RAM: {address:#x}")
        out.append(f"{address:#010x} bytes={raw.hex(' ')} LE32=0x{int.from_bytes(raw,'little'):08X}")
    return "; ".join(out)


def read_schedule(path):
    found = {}
    with Path(path).open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            name, press, release = row["schedule"], int(row["press_frame"]), int(row["release_frame"])
            if row["button"] != "CIRCLE" or int(row["launch_count"]) != 2 or release != press + 1:
                raise ValueError(f"invalid fixed one-frame Circle schedule: {row}")
            if name in found:
                raise ValueError(f"duplicate schedule {name}")
            found[name] = press
    if found != {"A": 60, "B": 90}:
        raise ValueError(f"schedule must be A=60 and B=90; got {found}")
    return found


def lua_source(press_frame):
    return f'''if io.stdout then io.stdout:setvbuf("no") end
local frame, started, loaded, after = 0, false, false, 0
local launchEpoch = tonumber(os.getenv("AM3_LAUNCH_START_EPOCH")) or os.time()
local pressFrame = {press_frame}
local pad = PCSX.SIO0.slots[1].pads[1]
local circle = PCSX.CONSTS.PAD.BUTTON.CIRCLE
local done, pending = {{}}, {{}}
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
local function input(phase)
  local ok, value = pcall(function()
    if phase == "press" then pad.setOverride(circle) else pad.clearOverride(circle) end
    return pad.getButton(circle)
  end)
  local pass = ok and value == (phase == "press")
  log("AM3_INPUT schedule="..(os.getenv("AM3_SCHEDULE") or "?").." action=CIRCLE phase="..phase.." frame="..after.." readback="..tostring(value).." status="..(pass and "PASS" or "FAIL"))
  if not pass then PCSX.quit(83) end
end
local function snap(target)
  local ok, err = pcall(function()
    local state = PCSX.createSaveState()
    local file = assert(Support.File.open("runtime/frame"..target..".sstate", "TRUNCATE"))
    file:writeMoveSlice(state); file:close()
  end)
  if not ok then log("AM3_RAM_CAPTURE_FRAME="..target.."=FAIL "..tostring(err)); PCSX.quit(62); return end
  log("AM3_RAM_CAPTURE_FRAME="..target.."=PASS")
  if target == 360 then
    log("AM3_QUIT0_CALL_BEGIN=1 frame=360 dispatch=direct")
    local qok, qerr = pcall(function() PCSX.quit(0) end)
    log("AM3_QUIT0_CALL_RETURNED=1 ok="..tostring(qok).." detail="..tostring(qerr))
  end
end
_G.am3Loaded = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  loaded = true; after = 0; log("AM3_LOAD_EVENT=PASS")
end)
_G.am3Vsync = PCSX.Events.createEventListener("GPU::Vsync", function()
  if not started then
    started = true
    local statePath = os.getenv("AM3_STATE_PATH") or "resume/h6.sstate"
    log("AM3_LOAD_BEGIN=1 path="..statePath.." input=NONE")
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local opened, file = pcall(function() return assert(Support.File.open(statePath)) end)
      if not opened or not file then log("AM3_STATE_OPEN_FAIL="..tostring(file)); PCSX.quit(50); return end
      local ok, err = pcall(function() PCSX.loadSaveState(file) end); file:close()
      if not ok then log("AM3_LOAD_ERROR="..tostring(err)); PCSX.quit(51); return end
      log("AM3_LOAD_CALL_RETURNED=1"); PCSX.resumeEmulator()
    end)
    return
  end
  if not loaded then return end
  frame = frame + 1; after = after + 1
  if after == pressFrame then input("press") end
  if after == pressFrame + 1 then input("release") end
  for _, target in ipairs({{1,60,180,240,360}}) do
    if after >= target and not done[target] and not pending[target] then
      pending[target] = true
      log("AM3_POST_LOAD_VSYNC="..target.." elapsed_since_launch_s="..tostring(os.time()-launchEpoch))
      local captureFrame = target
      PCSX.nextTick(function() snap(captureFrame); done[captureFrame] = true end)
    end
  end
  if after >= 1200 then log("AM3_WATCHDOG=1 after="..after); PCSX.quit(53) end
end)
log("AM3_READY schedule="..(os.getenv("AM3_SCHEDULE") or "?").." circle_press_frame="..pressFrame.." release_frame="..(pressFrame+1).." captures=1,60,180,240,360")
'''


def exit_code(text):
    match = re.search(r"Inferior\s+\d+.*?exited with code\s+([0-7]+)", text, re.I)
    if match:
        return str(int(match.group(1), 8)), "GDB inferior exit status (octal to decimal)"
    if re.search(r"Inferior\s+\d+.*?exited normally", text, re.I):
        return "0", "GDB inferior exited normally"
    match = re.search(r"Program exited with code\s+([0-7]+)", text, re.I)
    if match:
        return str(int(match.group(1), 8)), "GDB program exit status (octal to decimal)"
    if re.search(r"Program exited normally", text, re.I):
        return "0", "GDB program exited normally"
    return "TIDAK TAHU", "no explicit GDB exit status"


def run_launch(schedule, attempt, press, args, base_env, work, out):
    tag = f"{schedule}-attempt{attempt}"
    launch = work / "launches" / tag
    runtime, home = launch / "runtime", launch / "home"
    for path in (runtime, home/".config", home/".data", home/"runtime"):
        path.mkdir(parents=True, exist_ok=True)
    try: (home/"runtime").chmod(0o700)
    except OSError: pass
    lua = launch / "am3.lua"; lua.write_text(lua_source(press), encoding="utf-8")
    pad = launch / "pad.lua"
    pad.write_text("PCSX.settings.pads[1].DeviceType='Analog'\nPCSX.settings.pads[1].Connected=true\nPCSX.SIO0.slots[1].pads[1].map()\nprint('AM3_CONTROLLER_READY=PASS')\n", encoding="utf-8")
    gdb_log, pcsx_log = out/"logs"/f"{tag}.gdb.txt", out/"logs"/f"{tag}.pcsx.txt"
    gdb_script = launch/"gdb.commands"
    gdb_script.write_text("""set pagination off
set confirm off
set print thread-events off
handle SIGSEGV stop print nopass
handle SIGABRT stop print nopass
run
python
import gdb
inf=gdb.selected_inferior()
if getattr(inf,'pid',0):
 print('AM3_GDB_CONTEXT_BEGIN')
 for c in ('info threads','x/3i $pc','info registers','bt','thread apply all bt 20'):
  try:gdb.execute(c)
  except Exception as e:print('AM3_GDB_COMMAND_UNAVAILABLE: '+str(e))
 print('AM3_GDB_CONTEXT_END')
 try:gdb.execute('continue')
 except Exception as e:print('AM3_GDB_CONTINUE_RESULT: '+str(e))
else: print('AM3_GDB_CONTEXT_STATUS=INFERIOR_EXITED')
end
""", encoding="utf-8")
    env = base_env.copy()
    env.update({"HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),"XDG_DATA_HOME":str(home/".data"),
                "XDG_RUNTIME_DIR":str(home/"runtime"),"AM3_STATE_PATH":str(work/"resume"/"h6.sstate"),
                "AM3_SCHEDULE":schedule,"AM3_LAUNCH_START_EPOCH":str(time.time())})
    command=["timeout","--signal=INT","--kill-after=5s",f"{args.timeout_seconds}s","gdb","--quiet","--nx","--batch","--return-child-result","-x",str(gdb_script),
             "--args",args.pcsx_bin,"-noupdate","-no-debugger","-no-gdb","-bios",args.bios,"-iso",args.cue,"-memcard1",args.card,
             "-exec",pad.read_text(encoding="utf-8"),"-dofile",str(lua),"-softgpu","-dynarec","-stdout","-lua_stdout","-logfile",str(pcsx_log),"-run"]
    start=time.monotonic()
    with gdb_log.open("wb") as stream:
        try: wrapper=subprocess.run(command,cwd=launch,env=env,stdout=stream,stderr=subprocess.STDOUT,check=False).returncode
        except Exception as exc:
            wrapper=255; stream.write(("AM3_LAUNCH_EXCEPTION="+repr(exc)+"\n").encode())
    wall=time.monotonic()-start
    gdb_text=gdb_log.read_text(encoding="utf-8",errors="replace")
    pcsx_text=pcsx_log.read_text(encoding="utf-8",errors="replace") if pcsx_log.exists() else ""
    combined=gdb_text+"\n"+pcsx_text
    emu_exit, emu_source=exit_code(combined)
    press_ok=bool(re.search(r"AM3_INPUT schedule="+schedule+r" action=CIRCLE phase=press .*?status=PASS",combined))
    release_ok=bool(re.search(r"AM3_INPUT schedule="+schedule+r" action=CIRCLE phase=release .*?status=PASS",combined))
    watchdog="AM3_WATCHDOG=1" in combined
    result=[]
    for target in FRAMES:
        state=runtime/f"frame{target}.sstate"
        marker=re.search(rf"AM3_POST_LOAD_VSYNC={target} elapsed_since_launch_s=([0-9.]+)",gdb_text)
        captured=f"AM3_RAM_CAPTURE_FRAME={target}=PASS" in gdb_text and marker and state.is_file()
        status="PASS" if captured else "TIDAK ADA CAPTURE"
        digest,ram_len,words="TIDAK TAHU",0,"TIDAK TAHU"
        if captured:
            try:
                ram,ram_len=ram2m(state.read_bytes()); digest=sha(ram); words=word_text(ram)
            except Exception as exc: status="PARSE_ERROR"; words="TIDAK TAHU: "+repr(exc)
        result.append({"schedule":schedule,"attempt":attempt,"press_frame":press,"release_frame":press+1,"frame":target,
            "capture_status":status,"elapsed_since_launch_s":marker.group(1) if marker else "TIDAK TAHU",
            "ram_first_2mib_sha256":digest,"ram_segment_bytes":ram_len,"words":words,"gdb_wrapper_exit_code":wrapper,
            "emulator_exit_code_decimal":emu_exit,"emulator_exit_code_source":emu_source,"input_press_readback_pass":press_ok,
            "input_release_readback_pass":release_ok,"watchdog_seen":str(watchdog).upper(),"wall_seconds":f"{wall:.3f}",
            "gdb_log":f"logs/{tag}.gdb.txt","pcsx_log":f"logs/{tag}.pcsx.txt"})
    return result


def main():
    parser=argparse.ArgumentParser()
    for name in ("target","control","pcsx-bin","appdir","bios","cue","card","work","out","schedule"):
        parser.add_argument("--"+name,required=True)
    parser.add_argument("--timeout-seconds",type=int,default=600)
    args=parser.parse_args()
    target,control=Path(args.target).read_bytes(),Path(args.control).read_bytes()
    if sha(target)!=TARGET_SHA: raise SystemExit("AM3_TARGET_SHA_MISMATCH")
    if sha(control)!=CONTROL_SHA: raise SystemExit("AM3_CONTROL_SHA_MISMATCH")
    hybrid=replace_top(target,6,encmsg(6,one(control,6)))
    if sha(hybrid)!=H6_SHA: raise SystemExit("AM3_H6_SHA_MISMATCH actual="+sha(hybrid))
    work,out=Path(args.work),Path(args.out); schedules=read_schedule(args.schedule)
    (work/"resume").mkdir(parents=True,exist_ok=True); (work/"resume"/"h6.sstate").write_bytes(hybrid)
    (work/"resume"/"h6.sstate").chmod(0o400); (out/"logs").mkdir(parents=True,exist_ok=True)
    app=Path(args.appdir); env=os.environ.copy(); env.update({"DISPLAY":":99","LIBGL_ALWAYS_SOFTWARE":"1",
      "LD_LIBRARY_PATH":str(app/"usr/lib")+":"+str(app/"usr/lib/x86_64-linux-gnu"),"QT_PLUGIN_PATH":str(app/"usr/plugins"),
      "QT_QPA_PLATFORM_PLUGIN_PATH":str(app/"usr/plugins/platforms"),"QML2_IMPORT_PATH":str(app/"usr/qml")})
    rows=[]
    for name in ("A","B"):
        for attempt in (1,2): rows.extend(run_launch(name,attempt,schedules[name],args,env,work,out))
    with (out/"AM3_REPLAY.tsv").open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),delimiter="\t"); writer.writeheader(); writer.writerows(rows)
    lookup={(r["schedule"],r["attempt"],r["frame"]):r for r in rows}
    valid=all(r["capture_status"]=="PASS" for r in rows)
    input_ok=all(r["input_press_readback_pass"] and r["input_release_readback_pass"] for r in rows if r["frame"]==360)
    times=[float(r["elapsed_since_launch_s"]) for r in rows if r["frame"]==360 and r["elapsed_since_launch_s"]!="TIDAK TAHU"]
    max_time=max(times) if valid and len(times)==4 else None
    timeout_ok=max_time is not None and args.timeout_seconds>=2*max_time
    exits_ok=all(r["emulator_exit_code_decimal"]=="0" and r["watchdog_seen"]=="FALSE" for r in rows if r["frame"]==360)
    lines=["AM3 H6 hybrid headless PCSX-Redux CIRCLE timing A/B replay",f"H6_SHA256={H6_SHA}",
      "RAM_SHA_COVERAGE=first 2 MiB of PS1 RAM, base 0x80000000","RAM_SEGMENT_BYTES=8388608 (decoded RAM field length, not hash coverage)",
      "A=CIRCLE press post-load frame 60, release 61; two launches","B=CIRCLE press post-load frame 90, release 91; two launches"]
    for name in ("A","B"):
        same={f:lookup[(name,1,f)]["ram_first_2mib_sha256"]==lookup[(name,2,f)]["ram_first_2mib_sha256"] for f in FRAMES} if valid else {}
        first=next((f for f in FRAMES if not same.get(f,True)),None)
        lines.append(f"SCHEDULE_{name}_IDENTICAL_ACROSS_LAUNCHES={('YA' if valid and all(same.values()) else 'TIDAK' if valid else 'TIDAK TAHU')}")
        lines.append(f"SCHEDULE_{name}_FIRST_DIVERGENCE={('FRAME '+str(first) if first else 'TIDAK ADA DIVERGENSI SAMPEL' if valid else 'TIDAK TAHU')}")
    ab={f:any(lookup[("A",n,f)]["ram_first_2mib_sha256"]!=lookup[("B",n,f)]["ram_first_2mib_sha256"] for n in (1,2)) for f in FRAMES} if valid else {}
    first_ab=next((f for f in FRAMES if ab.get(f,False)),None)
    lines.append(f"A_VS_B_DIFFERENT_ON_SAMPLED_RAM={('YA' if valid and any(ab.values()) else 'TIDAK' if valid else 'TIDAK TAHU')}")
    lines.append(f"A_VS_B_FIRST_DIVERGENCE={('FRAME '+str(first_ab) if first_ab else 'TIDAK ADA PERBEDAAN SAMPEL' if valid else 'TIDAK TAHU')}")
    for f in FRAMES:
        for name in ("A","B"):
            for n in (1,2):
                r=lookup[(name,n,f)]
                lines.extend([f"{name}_ATTEMPT{n}_FRAME{f}_RAM_SHA256={r['ram_first_2mib_sha256']}",
                              f"{name}_ATTEMPT{n}_FRAME{f}_ELAPSED_S={r['elapsed_since_launch_s']}",
                              f"{name}_ATTEMPT{n}_FRAME{f}_WORDS={r['words']}"])
    lines.extend([f"MAX_TIME_TO_FRAME360_S={max_time}",f"TIMEOUT_PER_LAUNCH_S={args.timeout_seconds}",f"TIMEOUT_GE_2X_MAX_TIME={timeout_ok}",
                  f"ALL_CAPTURE_ROWS_VALID={valid}",f"ALL_INPUT_PRESS_RELEASE_READBACK_PASS={input_ok}",f"ALL_EMULATOR_EXITS_ZERO={exits_ok}",
                  f"AM3_STATUS={'PASS' if valid and input_ok and timeout_ok and exits_ok else 'INCOMPLETE'}"])
    (out/"AM3_COMPARISON_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    exit_status=0 if valid and input_ok and timeout_ok and exits_ok else 1
    summary=[f"STATUS={'PASS' if exit_status==0 else 'INCOMPLETE'}","JOB=am3-h6-circle-ab","JOB_ID=TIDAK TAHU (diisi publisher)",
      f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",f"HEAD_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",f"H6_SHA256={H6_SHA}",
      f"TIMEOUT_PER_LAUNCH_S={args.timeout_seconds}",f"MAX_TIME_TO_FRAME360_S={max_time}",f"ALL_CAPTURE_ROWS_VALID={valid}",
      f"ALL_INPUT_READBACK_PASS={input_ok}",f"ALL_EMULATOR_EXITS_ZERO={exits_ok}",f"TIMEOUT_GE_2X_MAX_TIME={timeout_ok}",f"EXIT_CODE={exit_status}"]
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    shutil.rmtree(work/"launches",ignore_errors=True)
    try: (work/"resume"/"h6.sstate").unlink()
    except OSError: pass
    if exit_status: raise SystemExit(exit_status)

if __name__=="__main__": main()
