#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, os, shutil, subprocess, time
from pathlib import Path

SOURCE_SHA256="705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35"
EXPECTED_OLD_CARD_SHA256="ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5"
EXPECTED_CARD_BYTES=131072
MAX_HITS=64
FRAME_LIMIT=900
CONDITIONS=("NO_INPUT_1","NO_INPUT_2","CIRCLE_1","CIRCLE_2")

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def lua_probe(mode: str, launch: str) -> str:
    return r'''
local ffi = require("ffi")
local MODE = "''' + mode + r'''"
local LAUNCH = "''' + launch + r'''"
local MAX_HITS = 64
local FRAME_LIMIT = 900
local MOD = 4294967296
local loaded, started, post = false, false, 0
local hits, inputErrors, circlePresses, circleReleases = 0, 0, 0, 0
local bpCall, bpHelper = nil, nil
local mem = PCSX.getMemPtr()
local function hx(x)
  if x == nil then return "TIDAK_TAHU" end
  return string.format("0x%08X", tonumber(x) % MOD)
end
local function read32(address)
  local va = tonumber(address) % MOD
  local phys = va % 0x20000000
  if phys < 0 or phys + 4 > 0x200000 then return "TIDAK_TAHU_OUTSIDE_2MIB" end
  local ok, value = pcall(function()
    return tonumber(ffi.cast("const uint32_t *", mem + phys)[0]) % MOD
  end)
  if not ok or value == nil then return "TIDAK_TAHU_READ_ERROR" end
  return hx(value)
end
local function log(s)
  print(s)
  pcall(function() io.stdout:flush() end)
end
local function arm()
  bpCall = PCSX.addBreakpoint(0x80011A28, "Exec", 4, "UB2 caller jalr 80011A28",
    function(address) return onHit(address, "CALL_80011A28", bpCall) end)
  bpHelper = PCSX.addBreakpoint(0x800B50AC, "Exec", 4, "UB2 helper 800B50AC",
    function(address) return onHit(address, "HELPER_800B50AC", bpHelper) end)
  log("UB2_BREAKPOINTS_ARMED call=0x80011A28 helper=0x800B50AC")
end
function onHit(address, label, current)
  local ok, err = pcall(function()
    hits = hits + 1
    local r = PCSX.getRegisters()
    local g = r.GPR
    local a0 = tonumber(g.n.a0) % MOD
    local v1 = tonumber(g.n.v1) % MOD
    local v0 = tonumber(g.n.v0) % MOD
    local requestedAddress = (v1 + ((28 * a0) % MOD) + 8) % MOD
    local actualAddress = (v1 + 8) % MOD
    local preIndexBase = (v1 - ((28 * a0) % MOD)) % MOD
    local fields = {
      "UB2_BP", LAUNCH, tostring(post), label, hx(address), hx(r.pc),
      hx(a0), hx(v1), hx(v0),
      hx(requestedAddress), read32(requestedAddress),
      hx(actualAddress), read32(actualAddress),
      hx(preIndexBase), hx((preIndexBase + ((28 * a0) % MOD) + 8) % MOD)
    }
    for i=0,31 do
      fields[#fields+1] = "r"..tostring(i).."="..hx(g.r[i])
    end
    log(table.concat(fields, "\t"))
    if hits >= MAX_HITS then
      log("UB2_HIT_CAP_REACHED launch="..LAUNCH.." count="..hits)
      if current == bpCall and bpHelper then pcall(function() bpHelper:disable() end) end
      if current == bpHelper and bpCall then pcall(function() bpCall:disable() end) end
      return false
    end
  end)
  if not ok then log("UB2_BREAKPOINT_ERROR launch="..LAUNCH.." error="..tostring(err)); return false end
  return true
end

local pad, circle
if MODE == "CIRCLE" then
  PCSX.settings.pads[1].DeviceType = "Analog"
  PCSX.settings.pads[1].Connected = true
  PCSX.SIO0.slots[1].pads[1].map()
  pad = PCSX.SIO0.slots[1].pads[1]
  circle = PCSX.CONSTS.PAD.BUTTON.CIRCLE
  pcall(function() pad.clearOverride(circle) end)
  log("UB2_PAD_READY mode=CIRCLE")
else
  log("UB2_PAD_READY mode=NO_INPUT overrides=NONE")
end

_G.ub2LoadedListener = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  loaded = true
  post = 0
  log("UB2_SAVE_STATE_LOADED=1 launch="..LAUNCH)
  arm()
end)

_G.ub2VsyncListener = PCSX.Events.createEventListener("GPU::Vsync", function()
  if not started then
    started = true
    local path = os.getenv("UB2_SOURCE_STATE") or "resume/source.sstate"
    log("UB2_LOAD_BEGIN=1 path="..path.." input_mode="..MODE)
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf, f = pcall(function() return assert(Support.File.open(path)) end)
      if not okf or not f then
        log("UB2_STATE_OPEN_FAIL="..tostring(f)); PCSX.quit(50); return
      end
      local ok, err = pcall(function() PCSX.loadSaveState(f) end)
      f:close()
      if not ok then
        log("UB2_STATE_LOAD_FAIL="..tostring(err)); PCSX.quit(51); return
      end
      log("UB2_LOAD_CALL_RETURNED=1")
      PCSX.resumeEmulator()
    end)
    return
  end
  if not loaded then return end
  post = post + 1

  if MODE == "CIRCLE" then
    if post >= 120 and (post - 120) % 120 == 0 then
      local ok, readback = pcall(function()
        pad.setOverride(circle)
        return pad.getButton(circle)
      end)
      local pass = ok and readback == true
      circlePresses = circlePresses + 1
      if not pass then inputErrors = inputErrors + 1 end
      log("UB2_INPUT\t"..LAUNCH.."\t"..tostring(post).."\tCIRCLE\tPRESS\t"..tostring(readback).."\t"..(pass and "PASS" or "FAIL"))
    elseif post >= 126 and (post - 126) % 120 == 0 then
      local ok, readback = pcall(function()
        pad.clearOverride(circle)
        return pad.getButton(circle)
      end)
      local pass = ok and readback == false
      circleReleases = circleReleases + 1
      if not pass then inputErrors = inputErrors + 1 end
      log("UB2_INPUT\t"..LAUNCH.."\t"..tostring(post).."\tCIRCLE\tRELEASE\t"..tostring(readback).."\t"..(pass and "PASS" or "FAIL"))
    end
  end

  if post == FRAME_LIMIT then
    log("UB2_FRAME_LIMIT_REACHED launch="..LAUNCH.." frames="..post.." hits="..hits)
    PCSX.nextTick(function() PCSX.quit(inputErrors == 0 and 0 or 52) end)
  end
end)

log("UB2_SCRIPT_READY launch="..LAUNCH.." mode="..MODE.." frames="..FRAME_LIMIT.." max_hits="..MAX_HITS.." read_only_probe=YES")
'''.lstrip()

def lua_warmup() -> str:
    return r'''
local frame = 0
_G.ub2WarmupVsync = PCSX.Events.createEventListener("GPU::Vsync", function()
  frame = frame + 1
  if frame == 12 then
    print("UB2_MEMCARD_WARMUP_FRAMES=12")
    PCSX.nextTick(function() PCSX.quit(0) end)
  end
end)
print("UB2_MEMCARD_WARMUP_READY=1")
'''.lstrip()

def pad_exec() -> str:
    return "\n".join([
        "PCSX.settings.pads[1].DeviceType = 'Analog'",
        "PCSX.settings.pads[1].Connected = true",
        "PCSX.SIO0.slots[1].pads[1].map()",
        "print('UB2_PAD_MAPPED_NO_OTHER_BUTTON_OVERRIDES=1')",
    ])

def app_env(appdir: Path, home: Path) -> dict:
    e=os.environ.copy()
    e.update({
      "HOME":str(home),
      "XDG_CONFIG_HOME":str(home/".config"),
      "XDG_DATA_HOME":str(home/".data"),
      "XDG_RUNTIME_DIR":str(home/"runtime"),
      "DISPLAY":"",
      "LIBGL_ALWAYS_SOFTWARE":"1",
      "LD_LIBRARY_PATH":str(appdir/"usr/lib")+":"+str(appdir/"usr/lib/x86_64-linux-gnu"),
      "QT_PLUGIN_PATH":str(appdir/"usr/plugins"),
      "QT_QPA_PLATFORM_PLUGIN_PATH":str(appdir/"usr/plugins/platforms"),
      "QML2_IMPORT_PATH":str(appdir/"usr/qml"),
    })
    return e

def run_emulator(pcsx: Path, appdir: Path, bios: Path, cue: Path, card: Path,
                 state: Path|None, lua: Path, home: Path, stdout: Path, timeout_s: int,
                 extra_exec: str|None=None) -> tuple[int,float,str]:
    for p in (home/".config",home/".data",home/"runtime"):
        p.mkdir(parents=True,exist_ok=True)
    try: (home/"runtime").chmod(0o700)
    except OSError: pass
    cmd=[
      "timeout","--signal=INT","--kill-after=10s",f"{timeout_s}s",
      str(pcsx),"-noupdate","-no-ui","-debugger","-interpreter",
      "-bios",str(bios),"-iso",str(cue),"-memcard1",str(card),
      "-softgpu","-dofile",str(lua),"-logfile",str(stdout.with_suffix(".pcsx.log")),
    ]
    if extra_exec:
        cmd.extend(["-exec",extra_exec])
    cmd.append("-run")
    env=app_env(appdir,home)
    if state is not None: env["UB2_SOURCE_STATE"]=str(state)
    t=time.monotonic()
    with stdout.open("wb") as f:
        try:
            p=subprocess.run(cmd,cwd=home,env=env,stdout=f,stderr=subprocess.STDOUT,check=False)
            rc=p.returncode
        except Exception as exc:
            rc=255
            f.write(("UB2_LAUNCH_EXCEPTION="+repr(exc)+"\n").encode())
    return rc,time.monotonic()-t,stdout.read_text(encoding="utf-8",errors="replace")

def read_log_text(stdout: Path) -> str:
    s=stdout.read_text(encoding="utf-8",errors="replace") if stdout.exists() else ""
    side=stdout.with_suffix(".pcsx.log")
    if side.exists(): s+="\n"+side.read_text(encoding="utf-8",errors="replace")
    return s

def parse_log(launch: str, log: str):
    hits=[]; inputs=[]
    for line in log.splitlines():
        if line.startswith("UB2_BP\t"):
            p=line.split("\t")
            if len(p) < 15: continue
            row={
              "launch":p[1],"frame":p[2],"breakpoint":p[3],"pc":p[4],
              "a0":p[6],"v1":p[7],"v0":p[8],
              "requested_mem_address":p[9],"requested_mem32":p[10],
              "actual_v1_plus8_address":p[11],"actual_v1_plus8_mem32":p[12],
              "preindex_base":p[13],"equivalent_from_preindex":p[14],
            }
            for item in p[15:]:
                if "=" in item:
                    k,v=item.split("=",1);row[k]=v
            hits.append(row)
        elif line.startswith("UB2_INPUT\t"):
            p=line.split("\t")
            if len(p)>=7:
                inputs.append({"launch":p[1],"frame":p[2],"button":p[3],
                               "action":p[4],"readback":p[5],"status":p[6]})
    return hits,inputs

def write_tsv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        w.writeheader()
        for row in rows: w.writerow({k:row.get(k,"TIDAK TAHU") for k in fields})

def sig(rows: list[dict]) -> tuple:
    fields=["frame","breakpoint","pc","a0","v1","v0","requested_mem_address",
            "requested_mem32","actual_v1_plus8_address","actual_v1_plus8_mem32",
            "preindex_base","equivalent_from_preindex"]+[f"r{i}" for i in range(32)]
    return tuple(tuple(r.get(k,"") for k in fields) for r in rows)

def main() -> int:
    ap=argparse.ArgumentParser()
    for k in ("work","out","pcsx-bin","appdir","bios","cue","source","card-dir"):
        ap.add_argument("--"+k,required=True)
    ap.add_argument("--timeout-seconds",type=int,default=600)
    a=ap.parse_args()
    work=Path(a.work);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    pcsx=Path(a.pcsx_bin);appdir=Path(a.appdir);bios=Path(a.bios);cue=Path(a.cue)
    source=Path(a.source);card_dir=Path(a.card_dir)
    digest=sha(source)
    if digest != SOURCE_SHA256: raise SystemExit("UB2_SOURCE_CHECKPOINT_SHA256_MISMATCH")
    if source.stat().st_size != 21162799: raise SystemExit("UB2_SOURCE_CHECKPOINT_SIZE_MISMATCH")
    source.chmod(0o444)
    card_dir.mkdir(parents=True,exist_ok=True)

    # A brief no-input setup launch lets the emulator create its own valid blank card.
    template=card_dir/"memory-card-template.mcd"
    warmup_lua=work/"warmup.lua"
    warmup_lua.write_text(lua_warmup(),encoding="utf-8")
    warm_home=work/"warmup-home"
    warm_stdout=work/"warmup.stdout.txt"
    warm_rc,warm_wall,warm_log=run_emulator(pcsx,appdir,bios,cue,template,None,
        warmup_lua,warm_home,warm_stdout,120)
    if not template.is_file() or template.stat().st_size != EXPECTED_CARD_BYTES:
        raise SystemExit("UB2_MEMORY_CARD_CREATION_FAILED")
    card_hash=sha(template)
    card_matches_old=(card_hash==EXPECTED_OLD_CARD_SHA256)

    launches=[];all_hits=[];all_inputs=[];logs=[]
    for launch in CONDITIONS:
        mode="CIRCLE" if launch.startswith("CIRCLE") else "NO_INPUT"
        launch_dir=work/launch.lower()
        launch_dir.mkdir(parents=True,exist_ok=True)
        state_copy=launch_dir/"source.sstate"
        shutil.copyfile(source,state_copy)
        state_copy.chmod(0o444)
        card=launch_dir/"memory-card.mcd"
        shutil.copyfile(template,card)
        card_before=sha(card)
        lua=launch_dir/"ub2.lua"
        lua.write_text(lua_probe(mode,launch),encoding="utf-8")
        stdout=launch_dir/"emulator.stdout.txt"
        rc,wall,raw=run_emulator(pcsx,appdir,bios,cue,card,state_copy,lua,
            launch_dir/"home",stdout,a.timeout_seconds,
            pad_exec() if mode=="CIRCLE" else None)
        log=read_log_text(stdout)
        hits,inputs=parse_log(launch,log)
        all_hits.extend(hits);all_inputs.extend(inputs);logs.append(log)
        frames=0
        for line in log.splitlines():
            if line.startswith("UB2_FRAME_LIMIT_REACHED"):
                try: frames=int(line.split("frames=",1)[1].split()[0])
                except Exception: pass
        loaded="UB2_SAVE_STATE_LOADED=1" in log
        load_ok="UB2_LOAD_CALL_RETURNED=1" in log
        hit_cap="UB2_HIT_CAP_REACHED" in log
        input_ok=all(x["status"]=="PASS" for x in inputs)
        expected_inputs=16 if mode=="CIRCLE" else 0
        launches.append({
          "launch":launch,"mode":mode,"frames_reached":frames,
          "save_state_loaded":"YES" if loaded else "NO",
          "load_call_returned":"YES" if load_ok else "NO",
          "breakpoint_hits":len(hits),"hit_cap_reached":"YES" if hit_cap else "NO",
          "input_events":len(inputs),"input_events_expected":expected_inputs,
          "input_readback":"PASS" if input_ok and len(inputs)==expected_inputs else "FAIL" if mode=="CIRCLE" else "NOT_APPLICABLE",
          "emulator_wrapper_exit_code":rc,"wall_seconds":f"{wall:.3f}",
          "memory_card_sha256_before":card_before,
          "memory_card_sha256_after":sha(card) if card.exists() else "TIDAK_TAHU",
          "memory_card_unchanged":"YES" if card.exists() and sha(card)==card_before else "NO",
          "source_checkpoint_sha256_after":sha(state_copy) if state_copy.exists() else "TIDAK_TAHU",
        })
        state_copy.unlink(missing_ok=True)
        card.unlink(missing_ok=True)

    # Repeated launches must match event-by-event within each condition.
    pairs=[]
    for mode,one,two in (("NO_INPUT",launches[0],launches[1]),("CIRCLE",launches[2],launches[3])):
        h1=[x for x in all_hits if x["launch"]==one["launch"]]
        h2=[x for x in all_hits if x["launch"]==two["launch"]]
        same=sig(h1)==sig(h2)
        complete=all(x["frames_reached"]==FRAME_LIMIT and x["save_state_loaded"]=="YES" and
                     x["load_call_returned"]=="YES" and x["emulator_wrapper_exit_code"]==0 and
                     x["memory_card_unchanged"]=="YES" for x in (one,two))
        input_ok=all(x["input_readback"] in ("PASS","NOT_APPLICABLE") for x in (one,two))
        pairs.append({"condition":mode,"launch1":one["launch"],"launch2":two["launch"],
                      "launch1_hit_count":len(h1),"launch2_hit_count":len(h2),
                      "event_trace_identical":"YES" if same else "NO",
                      "both_launches_complete":"YES" if complete else "NO",
                      "inputs_valid":"YES" if input_ok else "NO",
                      "repeat_K5":"PASS" if complete and same and input_ok else "INCOMPLETE"})

    full=all(x["repeat_K5"]=="PASS" for x in pairs)
    overall="PASS" if full else "INCOMPLETE"
    # The PCSX-created card can be a valid same-template control even when the historical
    # Memory Card bytes are no longer retrievable; never call it the old card unless hashes match.
    memcard_status="MATCHES_HISTORICAL" if card_matches_old else "NEW_PCSX_BLANK_CARD_IDENTICAL_ACROSS_RUNS"
    register_fields=[f"r{i}" for i in range(32)]
    hit_fields=["launch","frame","breakpoint","pc","a0","v1","v0",
       "requested_mem_address","requested_mem32","actual_v1_plus8_address",
       "actual_v1_plus8_mem32","preindex_base","equivalent_from_preindex"]+register_fields
    input_fields=["launch","frame","button","action","readback","status"]
    launch_fields=list(launches[0].keys())
    write_tsv(out/"UB2_BREAKPOINT_EVENTS.tsv",hit_fields,all_hits)
    write_tsv(out/"UB2_INPUT_EVENTS.tsv",input_fields,all_inputs)
    write_tsv(out/"UB2_LAUNCHES.tsv",launch_fields,launches)
    write_tsv(out/"UB2_REPEAT_COMPARISON.tsv",
        ["condition","launch1","launch2","launch1_hit_count","launch2_hit_count",
         "event_trace_identical","both_launches_complete","inputs_valid","repeat_K5"],pairs)
    summary=[
      "UB2_STATICALLY_GATED_RUNTIME_TRACE",
      f"STATUS={overall}",
      "JOB=ub2-headless-trace",
      f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK_TAHU')}",
      f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK_TAHU')}",
      f"CHECKPOINT_RUN_ID=39907655833",
      f"CHECKPOINT_ARTIFACT_ID=12482055310",
      f"CHECKPOINT_BYTES={source.stat().st_size}",
      f"CHECKPOINT_SHA256={digest}",
      "CONDITIONS=NO_INPUT x2; CIRCLE press 6 frames at post-load frames 120,240,360,480,600,720,840 x2",
      f"POST_LOAD_FRAMES_PER_LAUNCH={FRAME_LIMIT}",
      f"MAX_BREAKPOINT_HITS_PER_LAUNCH={MAX_HITS}",
      "BREAKPOINTS=Exec 0x80011A28 and 0x800B50AC",
      "REGISTERS=r0-r31 plus a0,v1,v0; no writes",
      "MEMORY_READS=read-only 32-bit values at requested current-v1+28*a0+8 and actual current-v1+8",
      "CALLSITE_SEMANTIC=at 0x80011A28, 1A1C has already applied 28*a0; actual lw at 1A20 reads MEM32[current $v1+8]. Both addresses are recorded to prevent double counting.",
      "RAW_DUMP=NONE",
      "GAMEPLAY_SCREENSHOT=NONE",
      "SETUP_WARMUP_LAUNCHES=1 (12 frames, no gameplay input, initializes emulator-created Memory Card)",
      f"MEMORY_CARD_STATUS={memcard_status}",
      f"MEMORY_CARD_BYTES={template.stat().st_size}",
      f"MEMORY_CARD_SHA256={card_hash}",
      f"MEMORY_CARD_HISTORICAL_SHA256={EXPECTED_OLD_CARD_SHA256}",
      f"MEMORY_CARD_HISTORICAL_HASH_MATCH={'YES' if card_matches_old else 'NO'}",
      "ALL_TEST_LAUNCHES_START_FROM_IMMUTABLE_IDENTICAL_CHECKPOINT=YES",
      "NO_REGISTER_OR_EMULATED_MEMORY_WRITES_BY_PROBE=YES",
      f"NO_INPUT_REPEAT_K5={pairs[0]['repeat_K5']}",
      f"CIRCLE_REPEAT_K5={pairs[1]['repeat_K5']}",
      f"EXIT_CODE={0 if full else 2}",
    ]
    (out/"UB2_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    action_summary=[
      f"STATUS={overall}","JOB=ub2-headless-trace",
      f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK_TAHU')}",
      f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK_TAHU')}",
      f"EXIT_CODE={0 if full else 2}",
    ]
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text("\n".join(action_summary)+"\n",encoding="utf-8")
    print("\n".join(summary))
    return 0 if full else 2

if __name__=="__main__":
    raise SystemExit(main())
