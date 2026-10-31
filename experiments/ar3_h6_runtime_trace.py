#!/usr/bin/env python3
"""AR3: bounded two-launch H6-hybrid interpreter trace at economy call targets.

Only text summaries are published. The frame-360 savestate and parsed RAM bytes
exist in the private runner work directory and are deleted before publication.
"""
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
RAM_BYTES = 0x200000
EXPECTED_F360_SHA = "a9ac5282e9fb9ad1e77f46ef0c291af8e7e5f27b477b6b31e319f971e7dd9942"
REQUESTED_COMPARISON_SHA = "16880faeccfca1fbd42d199c1543b00ec8a065bcd53545d14ea4657c9a6c2d5c"
HISTORICAL_SLOWEST_WALL_S = 142.696
MIN_TIMEOUT_S = 600

def sha(data):
    return hashlib.sha256(data).hexdigest()

def ram2m(state_bytes):
    memory = one(state_bytes, 3)
    ram = one(memory, 1)
    if len(ram) < RAM_BYTES:
        raise ValueError(f"RAM shorter than 2 MiB: {len(ram)}")
    return ram[:RAM_BYTES], len(ram)

def make_lua():
    return r'''
if io.stdout then io.stdout:setvbuf("no") end
local started, loaded, post, armed, pending = false, false, 0, false, false
local launchEpoch = tonumber(os.getenv("AR3_LAUNCH_START_EPOCH")) or os.time()
local bpKeep, returnKeep = {}, {}
local returnByRA = {}
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
local function event(tag, callbackAddress, frame)
  local pc, ra, a0, a1, v0 = regs()
  log(string.format(
    "AR3_EVENT tag=%s frame=%d callback_pc=%s regs_pc=%s ra=%s a0=%s a1=%s v0=%s",
    tag, frame, hx(callbackAddress), hx(pc), hx(ra), hx(a0), hx(a1), hx(v0)))
  return ra
end
local function armHelperReturn(ra, frame)
  local key = hx(ra)
  if key == "TIDAK_TAHU" or tonumber(ra) == 0 then
    log("AR3_RETURN_ARM_SKIP frame="..frame.." ra="..key)
    return
  end
  local slot = returnByRA[key]
  if not slot then
    slot = { pending = 0, bp = nil }
    returnByRA[key] = slot
  end
  slot.pending = slot.pending + 1
  if not slot.bp then
    slot.bp = PCSX.addBreakpoint(tonumber(ra), "Exec", 4, "AR3_FUN_800B770C_RETURN", function(addr)
      local current = returnByRA[key]
      if current and current.pending > 0 then
        current.pending = current.pending - 1
        event("FUN_800B770C_EXIT", addr, post)
      end
      if not current or current.pending == 0 then
        if current then current.bp = nil end
        return false
      end
      return true
    end)
    returnKeep[#returnKeep+1] = slot
  end
end
local function arm(address, tag)
  local bp = PCSX.addBreakpoint(address, "Exec", 4, "AR3_"..tag, function(addr)
    if tag == "FUN_800B770C_ENTRY" then
      local ra = event(tag, addr, post)
      armHelperReturn(ra, post)
    else
      event(tag, addr, post)
    end
    return true
  end)
  bpKeep[#bpKeep+1] = bp
  log(string.format("AR3_BREAKPOINT_ARMED tag=%s address=%s object=%s",
    tag, hx(address), tostring(bp ~= nil)))
end
local function armAll()
  arm(0x8001387C, "SETTER_8001387C")
  arm(0x800138EC, "GETTER_800138EC")
  arm(0x800B770C, "FUN_800B770C_ENTRY")
  armed = true
  log("AR3_BREAKPOINTS_ARMED=3 post_load_frame="..post)
end
local function snapshot360()
  local ok, err = pcall(function()
    local s = PCSX.createSaveState()
    local f = assert(Support.File.open("runtime/frame360.sstate", "TRUNCATE"))
    f:writeMoveSlice(s)
    f:close()
  end)
  log(ok and "AR3_FRAME360_CAPTURE=PASS" or ("AR3_FRAME360_CAPTURE=FAIL "..tostring(err)))
  if ok then PCSX.quit(0) else PCSX.quit(62) end
end
_G.ar3LoadedListener = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  loaded = true
  post = 0
  log("AR3_SAVE_STATE_LOADED=1")
end)
_G.ar3VsyncListener = PCSX.Events.createEventListener("GPU::Vsync", function()
  if not started then
    started = true
    local path = os.getenv("AR3_H6_STATE") or "resume/h6.sstate"
    log("AR3_LOAD_BEGIN=1 path="..path.." input=NONE")
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf, f = pcall(function() return assert(Support.File.open(path)) end)
      if not okf or not f then log("AR3_STATE_OPEN_FAIL="..tostring(f)); PCSX.quit(50); return end
      local ok, err = pcall(function() PCSX.loadSaveState(f) end)
      f:close()
      if not ok then log("AR3_STATE_LOAD_FAIL="..tostring(err)); PCSX.quit(51); return end
      log("AR3_LOAD_CALL_RETURNED=1")
      PCSX.resumeEmulator()
    end)
    return
  end
  if loaded then
    post = post + 1
    if post == 180 and not armed then
      log("AR3_POST_LOAD_FRAME=180 elapsed_since_launch_s="..tostring(os.time()-launchEpoch))
      armAll()
    end
    if post >= 360 and not pending then
      pending = true
      log("AR3_POST_LOAD_FRAME=360 elapsed_since_launch_s="..tostring(os.time()-launchEpoch))
      PCSX.nextTick(snapshot360)
    end
  end
end)
log("AR3_READY_NO_GAMEPLAY_INPUT=1")
'''.lstrip()

def parse_emulator_exit(rc, log_text):
    # The direct timeout wrapper returns POSIX decimal codes. When it is 124/137,
    # the emulator did not provide an ordinary exit code.
    if rc in (124, 137, 143):
        return "TIDAK TAHU", f"timeout_wrapper_exit_{rc}"
    if "AR3_FRAME360_CAPTURE=PASS" in log_text and rc == 0:
        return "0", "direct emulator process exit (timeout wrapper returned 0)"
    return str(rc), "direct emulator process exit observed by subprocess"

def main():
    ap = argparse.ArgumentParser()
    for name in ("target", "control", "pcsx-bin", "appdir", "bios", "cue", "card", "work", "out"):
        ap.add_argument("--"+name, required=True)
    ap.add_argument("--timeout-seconds", type=int, default=900)
    a = ap.parse_args()

    target = Path(a.target).read_bytes()
    control = Path(a.control).read_bytes()
    if sha(target) != TARGET_SHA:
        raise SystemExit("TARGET_SAVESTATE_SHA_MISMATCH")
    if sha(control) != CONTROL_SHA:
        raise SystemExit("CONTROL_SAVESTATE_SHA_MISMATCH")
    h6 = replace_top(target, 6, encmsg(6, one(control, 6)))
    h6_sha = sha(h6)
    if h6_sha != H6_SHA:
        raise SystemExit("H6_HYBRID_SHA_MISMATCH actual="+h6_sha)

    timeout_s = int(a.timeout_seconds)
    required = 2 * HISTORICAL_SLOWEST_WALL_S
    timeout_bound_ok = timeout_s >= max(MIN_TIMEOUT_S, required)
    if not timeout_bound_ok:
        raise SystemExit(f"TIMEOUT_TOO_SHORT timeout={timeout_s} required_at_least={max(MIN_TIMEOUT_S,required):.3f}")

    work, out = Path(a.work), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name in ("resume", "runtime", "logs", "launches", "home"):
        (work/name).mkdir(parents=True, exist_ok=True)
    h6_path = work/"resume"/"h6-hybrid.sstate"
    h6_path.write_bytes(h6)
    base_card = Path(a.card)
    base_card_sha = sha(base_card.read_bytes())
    expected_card = "ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5"
    if base_card_sha != expected_card:
        raise SystemExit("REFERENCE_MEMORY_CARD_SHA_MISMATCH")

    appdir = Path(a.appdir)
    env_base = os.environ.copy()
    env_base.update({
        "DISPLAY": ":99",
        "LIBGL_ALWAYS_SOFTWARE": "1",
        "LD_LIBRARY_PATH": str(appdir/"usr/lib")+":"+str(appdir/"usr/lib/x86_64-linux-gnu"),
        "QT_PLUGIN_PATH": str(appdir/"usr/plugins"),
        "QT_QPA_PLATFORM_PLUGIN_PATH": str(appdir/"usr/plugins/platforms"),
        "QML2_IMPORT_PATH": str(appdir/"usr/qml"),
    })
    launches = []
    all_events = []
    for attempt in (1, 2):
        launch = work/"launches"/f"attempt-{attempt}"
        runtime, home = launch/"runtime", launch/"home"
        logs = launch/"logs"
        for d in (runtime, home/".config", home/".data", home/"runtime", logs):
            d.mkdir(parents=True, exist_ok=True)
        try:
            (home/"runtime").chmod(0o700)
        except OSError:
            pass
        card = launch/"memory-card.mcd"
        shutil.copyfile(base_card, card)
        card_before = sha(card.read_bytes())
        state_path = runtime/"frame360.sstate"
        lua_path = launch/"ar3.lua"
        lua_path.write_text(make_lua(), encoding="utf-8")
        pad_text = (
            "PCSX.settings.pads[1].DeviceType = 'Analog'\n"
            "PCSX.settings.pads[1].Connected = true\n"
            "PCSX.SIO0.slots[1].pads[1].map()\n"
            "print('AR3_CONTROLLER_MAPPED_NO_INPUT=1')\n"
        )
        env = env_base.copy()
        env.update({
            "HOME":str(home),
            "XDG_CONFIG_HOME":str(home/".config"),
            "XDG_DATA_HOME":str(home/".data"),
            "XDG_RUNTIME_DIR":str(home/"runtime"),
            "AR3_H6_STATE":str(h6_path),
            "AR3_LAUNCH_START_EPOCH":str(time.time()),
        })
        stdout_path = logs/"emulator-stdout.txt"
        pcsx_log_path = logs/"pcsx-redux.log"
        command = [
            "timeout","--signal=INT","--kill-after=10s",f"{timeout_s}s",
            a.pcsx_bin,
            "-noupdate","-debugger","-interpreter",
            "-bios",a.bios,"-iso",a.cue,"-memcard1",str(card),
            "-exec",pad_text,"-dofile",str(lua_path),
            "-softgpu","-stdout","-lua_stdout",
            "-logfile",str(pcsx_log_path),"-run",
        ]
        started = time.monotonic()
        with stdout_path.open("wb") as f:
            try:
                proc = subprocess.run(command,cwd=launch,env=env,stdout=f,stderr=subprocess.STDOUT,check=False)
                wrapper_rc = proc.returncode
            except Exception as exc:
                wrapper_rc = 255
                f.write(("AR3_LAUNCH_EXCEPTION="+repr(exc)+"\n").encode())
        wall = time.monotonic()-started
        log_text = stdout_path.read_text(encoding="utf-8",errors="replace")
        if pcsx_log_path.exists():
            log_text += "\n"+pcsx_log_path.read_text(encoding="utf-8",errors="replace")
        frame_marker = "AR3_POST_LOAD_FRAME=360" in log_text
        capture = "AR3_FRAME360_CAPTURE=PASS" in log_text and state_path.is_file()
        emulator_exit, exit_source = parse_emulator_exit(wrapper_rc, log_text)
        ram_sha = "TIDAK TAHU"
        ram_status = "TIDAK ADA CAPTURE"
        if capture:
            try:
                ram, ram_len = ram2m(state_path.read_bytes())
                ram_sha = sha(ram)
                ram_status = "PASS"
            except Exception as exc:
                ram_status = "PARSE_ERROR"
                (logs/"ram-parse-error.txt").write_text(repr(exc)+"\n",encoding="utf-8")
        elif "AR3_FRAME360_CAPTURE=FAIL" in log_text:
            ram_status = "CAPTURE_FAILED"
        card_after = sha(card.read_bytes()) if card.exists() else "TIDAK TAHU"
        armed = len(re.findall(r"AR3_BREAKPOINT_ARMED tag=", log_text)) == 3
        events = []
        for line in log_text.splitlines():
            if "AR3_EVENT " not in line:
                continue
            m = re.search(r"AR3_EVENT tag=(\S+) frame=(\d+) callback_pc=(\S+) regs_pc=(\S+) ra=(\S+) a0=(\S+) a1=(\S+) v0=(\S+)",line)
            if not m:
                continue
            row = {
                "attempt":attempt,"tag":m.group(1),"frame":m.group(2),
                "callback_pc":m.group(3),"regs_pc":m.group(4),"ra":m.group(5),
                "a0":m.group(6),"a1":m.group(7),"v0":m.group(8),
            }
            events.append(row)
        all_events.extend(events)
        tags = ("SETTER_8001387C","GETTER_800138EC","FUN_800B770C_ENTRY","FUN_800B770C_EXIT")
        counts = {tag:sum(1 for e in events if e["tag"]==tag) for tag in tags}
        launches.append({
            "attempt":attempt,
            "frame180_breakpoints_armed": "YES" if armed else ("NO" if frame_marker else "TIDAK TAHU"),
            "post_load_frame360_reached":"YES" if frame_marker else "NO",
            "frame360_ram_capture":ram_status,
            "ram_first_2mib_sha256":ram_sha,
            "setter_hits":counts["SETTER_8001387C"],
            "getter_hits":counts["GETTER_800138EC"],
            "helper_entry_hits":counts["FUN_800B770C_ENTRY"],
            "helper_exit_hits":counts["FUN_800B770C_EXIT"],
            "emulator_exit_code_decimal":emulator_exit,
            "exit_code_source":exit_source,
            "timeout_wrapper_exit_decimal":str(wrapper_rc),
            "wall_seconds":f"{wall:.3f}",
            "memory_card_sha256_before":card_before,
            "memory_card_sha256_after":card_after,
            "memory_card_unchanged":"YES" if card_before==card_after else "NO",
        })
        try:
            state_path.unlink()
        except OSError:
            pass

    with (out/"AR3_BREAKPOINT_EVENTS.tsv").open("w",encoding="utf-8",newline="") as f:
        cols=["attempt","tag","frame","callback_pc","regs_pc","ra","a0","a1","v0"]
        w=csv.DictWriter(f,fieldnames=cols,delimiter="\t")
        w.writeheader(); w.writerows(all_events)
    with (out/"AR3_LAUNCHES.tsv").open("w",encoding="utf-8",newline="") as f:
        cols=list(launches[0].keys())
        w=csv.DictWriter(f,fieldnames=cols,delimiter="\t")
        w.writeheader(); w.writerows(launches)

    complete = len(launches)==2 and all(
        x["post_load_frame360_reached"]=="YES"
        and x["frame360_ram_capture"]=="PASS"
        and x["memory_card_unchanged"]=="YES"
        and x["emulator_exit_code_decimal"]=="0"
        for x in launches
    )
    hashes = [x["ram_first_2mib_sha256"] for x in launches]
    same = len(hashes)==2 and hashes[0]!="TIDAK TAHU" and hashes[0]==hashes[1]
    max_wall = max(float(x["wall_seconds"]) for x in launches)
    timeout_ok = timeout_s >= 2*HISTORICAL_SLOWEST_WALL_S
    report = [
        "AR3 — H6 HYBRID RUNTIME TRACE, TWO INDEPENDENT LAUNCHES",
        f"H6_SHA256={h6_sha}",
        "H6_IDENTITY=target checkpoint base + CONTROL top-level protobuf SPU field 6; HYBRID, NOT TARGET-PURE",
        f"METHOD=restore H6, no gameplay input, arm CPU execution breakpoints at post-load frame 180, continue through frame 360, capture first 2 MiB RAM at frame 360",
        "BREAKPOINTS=0x8001387C setter; 0x800138EC getter; 0x800B770C FUN entry; one-shot caller-RA execution breakpoints record helper exit v0",
        f"FRAME360_EXPECTED_PRIOR_H6_SHA256={EXPECTED_F360_SHA}",
        f"USER_REQUESTED_COMPARISON_SHA256={REQUESTED_COMPARISON_SHA} (historical AK1/AK3 label is frame 240, not frame 360)",
        f"HISTORICAL_SLOWEST_LAUNCH_WALL_S={HISTORICAL_SLOWEST_WALL_S:.3f}",
        f"TIMEOUT_PER_LAUNCH_S={timeout_s}",
        f"TIMEOUT_GE_2X_HISTORICAL_SLOWEST={timeout_ok}",
        f"OBSERVED_MAX_WALL_SECONDS={max_wall:.3f}",
        f"TWO_LAUNCH_FRAME360_SHA_IDENTICAL={same}",
        f"AR3_RUNTIME_CAPTURE_COMPLETE={complete}",
        "",
        "## Per-launch hit counts",
    ]
    for x in launches:
        report.extend([
            f"ATTEMPT_{x['attempt']}_BREAKPOINTS_ARMED={x['frame180_breakpoints_armed']}",
            f"ATTEMPT_{x['attempt']}_FRAME360_CAPTURE={x['frame360_ram_capture']}",
            f"ATTEMPT_{x['attempt']}_RAM_2MIB_SHA256={x['ram_first_2mib_sha256']}",
            f"ATTEMPT_{x['attempt']}_SETTER_HITS={x['setter_hits']}",
            f"ATTEMPT_{x['attempt']}_GETTER_HITS={x['getter_hits']}",
            f"ATTEMPT_{x['attempt']}_HELPER_ENTRY_HITS={x['helper_entry_hits']}",
            f"ATTEMPT_{x['attempt']}_HELPER_EXIT_HITS={x['helper_exit_hits']}",
            f"ATTEMPT_{x['attempt']}_EMULATOR_EXIT_DECIMAL={x['emulator_exit_code_decimal']}",
            f"ATTEMPT_{x['attempt']}_TIMEOUT_WRAPPER_EXIT_DECIMAL={x['timeout_wrapper_exit_decimal']}",
            f"ATTEMPT_{x['attempt']}_WALL_SECONDS={x['wall_seconds']}",
            f"ATTEMPT_{x['attempt']}_MEMCARD_UNCHANGED={x['memory_card_unchanged']}",
        ])
        if x["frame180_breakpoints_armed"]=="YES" and x["post_load_frame360_reached"]=="YES":
            report.append(f"ATTEMPT_{x['attempt']}_ZERO_HITS_NOTE=Zero means no observed breakpoint execution at the monitored static address in frames 180–360 only; no broader inference.")
        else:
            report.append(f"ATTEMPT_{x['attempt']}_HIT_COUNT_LIMIT=Not all target frames/breakpoints were observed; unobserved hits remain TIDAK TAHU, not zero.")
    report.extend([
        "",
        "## Frame 360 SHA comparison",
        f"ATTEMPT_1_MATCH_KNOWN_F360={launches[0]['ram_first_2mib_sha256']==EXPECTED_F360_SHA}",
        f"ATTEMPT_2_MATCH_KNOWN_F360={launches[1]['ram_first_2mib_sha256']==EXPECTED_F360_SHA}",
        f"ATTEMPT_1_MATCH_USER_SHA16880={launches[0]['ram_first_2mib_sha256']==REQUESTED_COMPARISON_SHA}",
        f"ATTEMPT_2_MATCH_USER_SHA16880={launches[1]['ram_first_2mib_sha256']==REQUESTED_COMPARISON_SHA}",
        "COMPARISON_CAUTION=16880fae...2d5c was recorded historically at frame 240; it is included as requested but is not a same-frame frame360 baseline.",
        "",
        "All emulator inputs, BIOS, disc, savestates, Memory Card copies, and raw RAM state were temporary runner files. Only text logs/counts/digests are publishable.",
    ])
    (out/"AR3_H6_SUMMARY.txt").write_text("\n".join(report)+"\n",encoding="utf-8")
    (out/"AR3_SCRIPT_EXIT_CODE.txt").write_text("AR3_SCRIPT_EXIT_CODE=0\n" if complete else "AR3_SCRIPT_EXIT_CODE=2\n",encoding="utf-8")
    status = "PASS" if complete and timeout_ok else "INCOMPLETE"
    summary = [
        f"STATUS={status}",
        "JOB=ar3-h6-runtime-trace",
        f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
        f"RUN_ATTEMPT={os.getenv('GITHUB_RUN_ATTEMPT','TIDAK TAHU')}",
        f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",
        f"H6_SHA256={h6_sha}",
        f"EXIT_CODE={0 if complete else 2}",
        f"TIMEOUT_PER_LAUNCH_S={timeout_s}",
        f"TIMEOUT_GE_2X_HISTORICAL_SLOWEST={timeout_ok}",
    ]
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary))
    # Failure to reach both frame-360 captures is published as INCOMPLETE.
    return 0

if __name__=="__main__":
    raise SystemExit(main())
