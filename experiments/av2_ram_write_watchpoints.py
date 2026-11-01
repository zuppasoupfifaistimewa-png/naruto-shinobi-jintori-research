#!/usr/bin/env python3
"""AV2: PCSX-Redux interpreter write-watchpoint matrix for four record words (H6 HIBRIDA)."""
import argparse, csv, hashlib, os, re, shutil, subprocess, time
from collections import Counter
from pathlib import Path
from aj2_h6_ram_probe import one, replace_top, encmsg

TARGET_SHA = "00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA = "9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA = "d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
MCD_SHA = "ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5"
RAM_SIZE = 0x200000
TARGETS = (0x80070EB8, 0x80070F6C, 0x80071020, 0x800710D4)
HISTORICAL = {
    ("C", 180): "5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7",
    ("C", 360): "4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907",
    ("C", 600): "01dd595f641a3ceb0420655b84d5c4bcb161d466f8a2532e56d7a600f593471a",
    ("A", 180): "0251aeef113a4c1eb58533a7dc5af85488e9bc2d96f42e24f62f8806ab0b6be8",
    ("A", 360): "2c53c4a225acccda78ebf67cb39e4922b0ee73d8c2da44928957df36792cc780",
    ("A", 600): "1164f1e27e9a1257fbf910047126de0e7baabbbd306940978af25ad326463aa2",
}
FRAMES = (180, 360, 600, 900)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def ram2m(state):
    ram = one(one(state, 3), 1)
    if len(ram) < RAM_SIZE:
        raise ValueError("RAM segment < 2 MiB")
    return ram[:RAM_SIZE], len(ram)

def word(data, address):
    off = address - 0x80000000
    if off < 0 or off + 4 > len(data):
        raise ValueError("word outside first 2 MiB: 0x%08X" % address)
    return int.from_bytes(data[off:off+4], "little")

def select_positive_control(before, after):
    candidates = []
    excluded = set(TARGETS)
    for off in range(0x10000, RAM_SIZE - 4, 4):
        a = 0x80000000 + off
        if a in excluded:
            continue
        old = int.from_bytes(before[off:off+4], "little")
        new = int.from_bytes(after[off:off+4], "little")
        if old != new:
            nonzero = int(old != 0 and new != 0)
            changed_bytes = sum(x != y for x, y in zip(before[off:off+4], after[off:off+4]))
            candidates.append((nonzero, changed_bytes, a, old, new))
    if not candidates:
        return None
    candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
    nonzero, changed_bytes, address, old, new = candidates[0]
    return {"address": address, "old": old, "new": new,
            "changed_bytes": changed_bytes, "both_nonzero": bool(nonzero),
            "candidate_count": len(candidates)}

def lua_source(condition, press_frame, positive_addr):
    targets = ",".join("0x%08X" % x for x in TARGETS)
    pos = "0" if positive_addr is None else "0x%08X" % positive_addr
    target_frames = ",".join(str(x) for x in FRAMES)
    return r'''
if io.stdout then io.stdout:setvbuf("no") end
local condition = "''' + condition + r'''"
local pressFrame = ''' + str(press_frame) + r'''
local positiveAddress = ''' + pos + r'''
local targetAddresses = {''' + targets + r'''}
local captureFrames = {''' + target_frames + r'''}
local started, loaded, post = false, false, 0
local keep, shadow, mem = {}, {}, nil
local pad = PCSX.SIO0.slots[1].pads[1]
local circle = PCSX.CONSTS.PAD.BUTTON.CIRCLE
local function log(s)
  print(s)
  pcall(function() io.stdout:flush() end)
end
local function hx(v)
  if v == nil then return "TIDAK_TAHU" end
  return string.format("0x%08X", tonumber(v) % 4294967296)
end
local function readByte(address)
  return tonumber(mem[address - 0x80000000])
end
local function readWord(address)
  local o = address - 0x80000000
  return readByte(address) + readByte(address + 1) * 256 +
         readByte(address + 2) * 65536 + readByte(address + 3) * 16777216
end
local function gprValue(r, index)
  return tonumber(r.GPR.r[index])
end
local function calcPreStoreWord(oldWord, address, width, opcode, rtValue)
  local base = math.floor(address / 4) * 4
  local offset = address - base
  local bytes = {}
  for i = 0, 3 do bytes[i] = math.floor(oldWord / (256 ^ i)) % 256 end
  local count = 0
  if opcode == 0x2B and width == 4 and offset == 0 then count = 4
  elseif opcode == 0x29 and width == 2 and offset <= 2 then count = 2
  elseif opcode == 0x28 and width == 1 and offset <= 3 then count = 1
  else return nil end
  for i = 0, count - 1 do
    bytes[offset + i] = math.floor(rtValue / (256 ^ i)) % 256
  end
  return bytes[0] + bytes[1] * 256 + bytes[2] * 65536 + bytes[3] * 16777216
end
local function makeWatch(tag, address)
  local base = math.floor(address / 4) * 4
  shadow[base] = readWord(base)
  local bp = PCSX.addBreakpoint(address, "Write", 4, "AV2 " .. tag, function(actualAddress, width, cause)
    local ok, err = pcall(function()
      actualAddress = tonumber(actualAddress)
      width = tonumber(width)
      local r = PCSX.getRegisters()
      local g = r.GPR.n
      local pc, ra, a0, a1, v0 = tonumber(r.pc), tonumber(g.ra), tonumber(g.a0), tonumber(g.a1), tonumber(g.v0)
      local wordBase = math.floor(actualAddress / 4) * 4
      local oldWord = shadow[wordBase]
      if oldWord == nil then oldWord = readWord(wordBase) end
      local nowWord = readWord(wordBase)
      local pcOffset = pc - 0x80000000
      local instruction = 0
      if pcOffset >= 0 and pcOffset + 4 <= 0x200000 then instruction = readWord(pc) end
      local opcode = math.floor(instruction / 67108864)
      local rt = math.floor(instruction / 65536) % 32
      local rtValue = gprValue(r, rt)
      local newWord, method
      if nowWord ~= oldWord then
        newWord, method = nowWord, "POSTSTORE_MEMORY"
      else
        newWord = calcPreStoreWord(oldWord, actualAddress, tonumber(width), opcode, rtValue)
        method = newWord == nil and "UNRESOLVED_STORE_ENCODING" or "PRESTORE_REGISTER_DERIVED"
      end
      if newWord == nil then newWord = nowWord end
      log(string.format(
        "AV2_EVENT condition=%s frame=%d tag=%s pc=%s ra=%s address=%s width=%d old=%s new=%s a0=%s a1=%s v0=%s method=%s opcode=0x%02X rt=%d cause=%s",
        condition, math.max(post,1), tag, hx(pc), hx(ra), hx(actualAddress), tonumber(width),
        hx(oldWord), hx(newWord), hx(a0), hx(a1), hx(v0), method, opcode, rt, tostring(cause)))
      shadow[wordBase] = newWord
    end)
    if not ok then log("AV2_CALLBACK_ERROR tag=" .. tag .. " err=" .. tostring(err)) end
    return true
  end)
  keep[#keep + 1] = bp
  log(string.format("AV2_WATCHPOINT_ARMED tag=%s address=%s object=%s width=4 type=Write",
    tag, hx(address), tostring(bp ~= nil)))
  return bp ~= nil
end
local function armAll()
  mem = PCSX.getMemPtr()
  local ok = true
  for _, address in ipairs(targetAddresses) do
    ok = makeWatch(string.format("W_%08X", address), address) and ok
  end
  if positiveAddress ~= 0 then
    ok = makeWatch("POSITIVE_CONTROL", positiveAddress) and ok
  end
  log("AV2_WATCHPOINT_SET target_count=4 positive_present=" .. tostring(positiveAddress ~= 0))
  if not ok then log("AV2_WATCHPOINT_INSTALL_FAIL=1"); PCSX.quit(82) end
end
local function input(phase)
  local ok, value = pcall(function()
    if phase == "press" then pad.setOverride(circle) else pad.clearOverride(circle) end
    return pad.getButton(circle)
  end)
  local pass = ok and value == (phase == "press")
  log("AV2_INPUT condition=" .. condition .. " phase=" .. phase ..
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
  log(ok and ("AV2_CAPTURE frame=" .. frame .. " status=PASS") or
      ("AV2_CAPTURE frame=" .. frame .. " status=FAIL error=" .. tostring(err)))
  if not ok then PCSX.quit(62); return end
  if frame == 900 then
    log("AV2_QUIT0_AFTER_FRAME900=1"); PCSX.quit(0)
  end
end
_G.av2Load = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  loaded = true
  post = 0
  log("AV2_STATE_LOADED condition=" .. condition)
  armAll()
end)
_G.av2Vsync = PCSX.Events.createEventListener("GPU::Vsync", function()
  if not started then
    started = true
    local path = os.getenv("AV2_H6_STATE") or "resume/h6-hybrid.sstate"
    log("AV2_LOAD_BEGIN condition=" .. condition .. " path=" .. path)
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf, f = pcall(function() return assert(Support.File.open(path)) end)
      if not okf or not f then log("AV2_STATE_OPEN_FAIL=" .. tostring(f)); PCSX.quit(50); return end
      local ok, err = pcall(function() PCSX.loadSaveState(f) end)
      f:close()
      if not ok then log("AV2_STATE_LOAD_FAIL=" .. tostring(err)); PCSX.quit(51); return end
      log("AV2_LOAD_CALL_RETURNED=1"); PCSX.resumeEmulator()
    end)
    return
  end
  if loaded then
    post = post + 1
    if pressFrame > 0 then
      if post == pressFrame then input("press") end
      if post == pressFrame + 1 then input("release") end
    end
    for _, frame in ipairs(captureFrames) do
      if post == frame then
        local f = frame
        PCSX.nextTick(function() capture(f) end)
        break
      end
    end
  end
end)
log("AV2_READY condition=" .. condition .. " input_frame=" .. tostring(pressFrame) ..
    " mode=INTERPRETER watchpoints=WRITE")
'''
    
def calibration_lua():
    return r'''
if io.stdout then io.stdout:setvbuf("no") end
local started, loaded, post = false, false, 0
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
local function capture(frame)
  local ok, err = pcall(function()
    local s=PCSX.createSaveState()
    local f=assert(Support.File.open(string.format("runtime/cal-%d.sstate",frame),"TRUNCATE"))
    f:writeMoveSlice(s); f:close()
  end)
  log(ok and ("AV2_CAL_CAPTURE frame="..frame.." status=PASS") or
      ("AV2_CAL_CAPTURE frame="..frame.." status=FAIL error="..tostring(err)))
  if not ok or frame==240 then PCSX.quit(ok and 0 or 62) end
end
_G.av2CalLoad=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
  loaded=true; post=0; log("AV2_CAL_STATE_LOADED=1")
end)
_G.av2CalVsync=PCSX.Events.createEventListener("GPU::Vsync",function()
  if not started then
    started=true
    local path=os.getenv("AV2_H6_STATE") or "resume/h6-hybrid.sstate"
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf,f=pcall(function() return assert(Support.File.open(path)) end)
      if not okf or not f then log("AV2_CAL_OPEN_FAIL="..tostring(f)); PCSX.quit(50); return end
      local ok,err=pcall(function() PCSX.loadSaveState(f) end); f:close()
      if not ok then log("AV2_CAL_LOAD_FAIL="..tostring(err)); PCSX.quit(51); return end
      PCSX.resumeEmulator()
    end)
    return
  end
  if loaded then
    post=post+1
    if post==180 or post==240 then local f=post; PCSX.nextTick(function() capture(f) end) end
  end
end)
log("AV2_CAL_READY=1 input=NONE")
'''

def parse_events(log, condition, attempt):
    rows=[]
    pat=re.compile(
        r"AV2_EVENT condition=(\S+) frame=(\d+) tag=(\S+) pc=(\S+) ra=(\S+) "
        r"address=(\S+) width=(\d+) old=(\S+) new=(\S+) a0=(\S+) a1=(\S+) "
        r"v0=(\S+) method=(\S+) opcode=(\S+) rt=(\d+) cause=(.*)"
    )
    for line in log.splitlines():
        m=pat.search(line)
        if m:
            keys=("condition","frame","tag","pc","ra","address","width","old_value","new_value",
                  "a0","a1","v0","value_method","store_opcode","store_rt","cause")
            row=dict(zip(keys,m.groups()))
            row["attempt"]=str(attempt)
            rows.append(row)
    return rows

def write_tsv(path, rows, cols):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,delimiter="\t",lineterminator="\n")
        w.writeheader()
        for row in rows: w.writerow({k:row.get(k,"") for k in cols})

def main():
    ap=argparse.ArgumentParser()
    for name in ("target","control","pcsx-bin","appdir","bios","cue","card","work","out"):
        ap.add_argument("--"+name,required=True)
    ap.add_argument("--timeout-seconds",type=int,default=1800)
    a=ap.parse_args()
    target,control=Path(a.target).read_bytes(),Path(a.control).read_bytes()
    if sha(target)!=TARGET_SHA: raise SystemExit("TARGET_SHA_MISMATCH")
    if sha(control)!=CONTROL_SHA: raise SystemExit("CONTROL_SHA_MISMATCH")
    hybrid=replace_top(target,6,encmsg(6,one(control,6)))
    hybrid_sha=sha(hybrid)
    if hybrid_sha!=H6_SHA: raise SystemExit("H6_HYBRIDA_SHA_MISMATCH="+hybrid_sha)
    work,out=Path(a.work),Path(a.out); out.mkdir(parents=True,exist_ok=True)
    (work/"resume").mkdir(parents=True,exist_ok=True)
    h6=work/"resume"/"h6-hybrid.sstate"; h6.write_bytes(hybrid)
    card0=Path(a.card)
    if sha(card0.read_bytes())!=MCD_SHA or card0.stat().st_size!=131072:
        raise SystemExit("REFERENCE_MCD_MISMATCH")
    app=Path(a.appdir)
    env0=os.environ.copy()
    env0.update({
        "DISPLAY":":99","LIBGL_ALWAYS_SOFTWARE":"1",
        "LD_LIBRARY_PATH":str(app/"usr/lib")+":"+str(app/"usr/lib/x86_64-linux-gnu"),
        "QT_PLUGIN_PATH":str(app/"usr/plugins"),
        "QT_QPA_PLATFORM_PLUGIN_PATH":str(app/"usr/plugins/platforms"),
        "QML2_IMPORT_PATH":str(app/"usr/qml"),
    })
    launch_rows,frame_rows,event_rows=[],[],[]
    def run_one(label,condition,attempt,press_frame,pos_addr,calibration=False):
        root=work/"launches"/label
        runtime,home=root/"runtime",root/"home"
        for d in (runtime,home/".config",home/".data",home/"runtime"): d.mkdir(parents=True,exist_ok=True)
        try:(home/"runtime").chmod(0o700)
        except OSError:pass
        mcd=root/"memory-card.mcd"; shutil.copyfile(card0,mcd); mcd_before=sha(mcd.read_bytes())
        lua=root/"av2.lua"
        lua.write_text(calibration_lua() if calibration else lua_source(condition,press_frame,pos_addr),encoding="utf-8")
        pad=("PCSX.settings.pads[1].DeviceType='Analog'\n"
             "PCSX.settings.pads[1].Connected=true\n"
             "PCSX.SIO0.slots[1].pads[1].map()\nprint('AV2_PAD_READY=PASS')\n")
        env=env0.copy()
        env.update({"HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),
                    "XDG_DATA_HOME":str(home/".data"),"XDG_RUNTIME_DIR":str(home/"runtime"),
                    "AV2_H6_STATE":str(h6)})
        stdout,pcsxlog=root/"stdout.log",root/"pcsx.log"
        command=["timeout","--signal=INT","--kill-after=10s",f"{a.timeout_seconds}s",
                 a.pcsx_bin,"-noupdate","-debugger","-interpreter","-bios",a.bios,
                 "-iso",a.cue,"-memcard1",str(mcd),"-exec",pad,"-dofile",str(lua),
                 "-softgpu","-stdout","-lua_stdout","-logfile",str(pcsxlog),"-run"]
        start=time.monotonic()
        with stdout.open("wb") as fh:
            try: rc=subprocess.run(command,cwd=root,env=env,stdout=fh,stderr=subprocess.STDOUT,check=False).returncode
            except Exception as exc:
                rc=255; fh.write(("AV2_EXCEPTION="+repr(exc)+"\n").encode())
        wall=time.monotonic()-start
        log=stdout.read_text(encoding="utf-8",errors="replace")
        if pcsxlog.exists(): log+="\n"+pcsxlog.read_text(encoding="utf-8",errors="replace")
        timeout_hit=rc in (124,137,143)
        emu_exit="TIDAK TAHU" if timeout_hit else str(rc)
        card_after=sha(mcd.read_bytes()) if mcd.exists() else "TIDAK TAHU"
        ev=parse_events(log,condition,attempt) if not calibration else []
        event_rows.extend(ev)
        if calibration:
            armed="NOT_APPLICABLE"; press="NOT_APPLICABLE"; release="NOT_APPLICABLE"
            expected_capture=(180,240)
        else:
            armed=("YES" if "AV2_WATCHPOINT_SET target_count=4" in log and
                   log.count("AV2_WATCHPOINT_ARMED")==(5 if pos_addr else 4) and
                   "object=true" in log else "NO")
            press="NOT_APPLICABLE" if press_frame==0 else ("PASS" if f"AV2_INPUT condition={condition} phase=press frame={press_frame} " in log and "status=PASS" in log else "FAIL")
            release="NOT_APPLICABLE" if press_frame==0 else ("PASS" if f"AV2_INPUT condition={condition} phase=release frame={press_frame+1} " in log and "status=PASS" in log else "FAIL")
            expected_capture=FRAMES
        launch_rows.append({
            "launch":label,"condition":condition,"attempt":attempt,"calibration":str(calibration).upper(),
            "flags":"-debugger -interpreter","watchpoints":"four target words"+("; positive control" if pos_addr else ""),
            "watchpoints_armed":armed,"circle_press_readback":press,"circle_release_readback":release,
            "emulator_exit_code_decimal":emu_exit,"timeout_wrapper_exit_decimal":str(rc),
            "wall_seconds":f"{wall:.3f}","timeout_seconds":a.timeout_seconds,
            "memory_card_sha256_before":mcd_before,"memory_card_sha256_after":card_after,
            "memory_card_unchanged":str(mcd_before==card_after).upper()
        })
        calibration_states={}
        for frame in expected_capture:
            p=runtime/("cal-%d.sstate"%frame if calibration else "frame%d.sstate"%frame)
            marker=(f"AV2_CAL_CAPTURE frame={frame} status=PASS" if calibration else f"AV2_CAPTURE frame={frame} status=PASS") in log
            ok=marker and p.is_file()
            digest="TIDAK TAHU"; segment=0
            if ok:
                try:
                    ram,segment=ram2m(p.read_bytes()); digest=sha(ram)
                    if calibration: calibration_states[frame]=ram
                except Exception: ok=False
            frame_rows.append({"condition":condition,"attempt":attempt,"frame":frame,
                               "capture_status":"PASS" if ok else "FAIL",
                               "ram_first_2mib_sha256":digest,"ram_segment_bytes":segment,
                               "calibration":str(calibration).upper()})
            if p.exists(): p.unlink()
        return log,rc,wall,calibration_states

    # Private calibration: two snapshots are parsed in memory and deleted immediately.
    cal_log,cal_rc,cal_wall,calibration_states=run_one("CALIBRATION-C","CAL",0,0,None,True)
    positive=None
    if cal_rc==0 and 180 in calibration_states and 240 in calibration_states:
        try:
            positive=select_positive_control(calibration_states[180],calibration_states[240])
        except Exception: positive=None
    if positive:
        pos_addr=positive["address"]
    else:
        pos_addr=None
    # C, A, D; two independent launches per schedule. A fresh card copy is made each time.
    maxwalls=[cal_wall]
    for condition,press in (("C",0),("A",60),("D",90)):
        for attempt in (1,2):
            _,rc,wall=run_one(f"{condition}-{attempt}",condition,attempt,press,pos_addr,False)
            maxwalls.append(wall)
    maxwall=max(maxwalls,default=0.0)
    timeout_ok=a.timeout_seconds>=2*maxwall
    counts=Counter((e["condition"],e["attempt"],e["tag"]) for e in event_rows)
    tags=[("W_%08X"%x) for x in TARGETS]+(["POSITIVE_CONTROL"] if pos_addr else [])
    hit_rows=[]
    for cond in ("C","A","D"):
        for attempt in ("1","2"):
            for tag in tags:
                hit_rows.append({"condition":cond,"attempt":attempt,"tag":tag,
                                 "hits":counts[(cond,attempt,tag)],
                                 "meaning":"observed writes only in post-load frames 1..900"})
    # Recompute all event totals from the raw parsed TSV rows, never from callback-side counters.
    raw_total=len(event_rows)
    positive_hits=sum(1 for e in event_rows if e["tag"]=="POSITIVE_CONTROL")
    target_hit_totals={tag:sum(1 for e in event_rows if e["tag"]==tag) for tag in tags if tag!="POSITIVE_CONTROL"}
    historical_rows=[]
    baseline_ok=True
    for cond in ("C","A"):
        for attempt in ("1","2"):
            for frame in (180,360,600):
                matches=[x for x in frame_rows if x["condition"]==cond and str(x["attempt"])==attempt and int(x["frame"])==frame and x["calibration"]=="FALSE"]
                actual=matches[0]["ram_first_2mib_sha256"] if matches else "TIDAK TAHU"
                expected=HISTORICAL[(cond,frame)]
                equal=actual==expected
                baseline_ok=baseline_ok and equal
                historical_rows.append({"condition":cond,"attempt":attempt,"frame":frame,
                                        "expected_AU3_sha256":expected,"actual_AV2_sha256":actual,
                                        "match":str(equal).upper()})
    launches_ok=(len(launch_rows)==7 and
        all(x["emulator_exit_code_decimal"]=="0" for x in launch_rows) and
        all(x["memory_card_unchanged"]=="TRUE" for x in launch_rows) and
        all(x["circle_press_readback"] in ("PASS","NOT_APPLICABLE") for x in launch_rows) and
        all(x["circle_release_readback"] in ("PASS","NOT_APPLICABLE") for x in launch_rows))
    captures_ok=(len(frame_rows)==2+6*4 and all(x["capture_status"]=="PASS" for x in frame_rows))
    watch_ok=all(x["watchpoints_armed"] in ("YES","NOT_APPLICABLE") for x in launch_rows)
    positive_ok=bool(pos_addr) and positive_hits>=1
    complete=launches_ok and captures_ok and watch_ok and timeout_ok and positive_ok and baseline_ok
    write_tsv(out/"AV2_LAUNCHES.tsv",launch_rows,list(launch_rows[0]))
    write_tsv(out/"AV2_FRAMES.tsv",frame_rows,["condition","attempt","frame","capture_status","ram_first_2mib_sha256","ram_segment_bytes","calibration"])
    event_cols=["condition","attempt","frame","tag","pc","ra","address","width","old_value","new_value","a0","a1","v0","value_method","store_opcode","store_rt","cause"]
    write_tsv(out/"AV2_WRITE_EVENTS.tsv",event_rows,event_cols)
    write_tsv(out/"AV2_HIT_COUNTS.tsv",hit_rows,["condition","attempt","tag","hits","meaning"])
    write_tsv(out/"AV2_AU3_HASH_CROSSCHECK.tsv",historical_rows,["condition","attempt","frame","expected_AU3_sha256","actual_AV2_sha256","match"])
    summary=[
      "AV2 PCSX-REDUX HEADLESS INTERPRETER WRITE-WATCHPOINT AUDIT",
      f"STATUS={'PASS' if complete else 'INCOMPLETE'}",
      f"H6_IDENTITY=HIBRIDA target checkpoint base + CONTROL top-level protobuf field 6; NOT TARGET-PURE",
      f"H6_SHA256={hybrid_sha}",
      "SCHEDULES=C no input; A CIRCLE frame 60 press/61 release; D CIRCLE frame 90 press/91 release",
      "TARGET_MATRIX=3 schedules x 2 independent launches = 6; plus 1 private calibration launch",
      "WATCH_API=PCSX.addBreakpoint(address,'Write',4,...), armed from SaveStateLoaded before post-load frame 1",
      "TARGET_WORDS="+",".join("0x%08X"%x for x in TARGETS),
      f"POSITIVE_CONTROL_ADDRESS={'0x%08X'%pos_addr if pos_addr else 'TIDAK_TAHU'}",
      f"POSITIVE_CONTROL_DIFF={'0x%08X'%positive['old']+' -> '+'0x%08X'%positive['new'] if positive else 'TIDAK TAHU'}",
      f"POSITIVE_CONTROL_HITS={positive_hits}",
      "EVENT_FIELDS=frame, store PC, ra, accessed address, width, old word, new word, a0, a1, v0; store method/opcode also recorded",
      "CAPTURE_FRAMES=180,360,600,900; first 2 MiB RAM SHA-256",
      f"EVENT_ROWS_RECOUNTED_FROM_RAW_TSV={raw_total}",
      f"TIMEOUT_PER_LAUNCH_SECONDS={a.timeout_seconds}",
      f"OBSERVED_LONGEST_WALL_SECONDS={maxwall:.3f}",
      f"TIMEOUT_GE_2X_LONGEST={timeout_ok}",
      f"AU3_C_A_HASH_MATCH_180_360_600={baseline_ok}",
      f"POSITIVE_CONTROL_PASS={positive_ok}",
      f"RUNTIME_COMPLETE={complete}",
      "Zero hits mean zero observations only in the tested condition/window; they do not prove a routine/address is unused.",
    ]
    for row in launch_rows:
        summary.append(f"LAUNCH {row['launch']} EXIT_DECIMAL={row['emulator_exit_code_decimal']} WRAPPER_EXIT={row['timeout_wrapper_exit_decimal']} WALL={row['wall_seconds']} WATCH={row['watchpoints_armed']} MCD_UNCHANGED={row['memory_card_unchanged']} CIRCLE_PRESS={row['circle_press_readback']} CIRCLE_RELEASE={row['circle_release_readback']}")
    for row in hit_rows: summary.append(f"HITS {row['condition']}#{row['attempt']} {row['tag']}={row['hits']}")
    for tag,total in target_hit_totals.items(): summary.append(f"TARGET_TOTAL {tag}={total}")
    (out/"AV2_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    script_rc=0 if complete else 2
    (out/"AV2_SCRIPT_EXIT_CODE.txt").write_text(f"AV2_SCRIPT_EXIT_CODE={script_rc}\n",encoding="utf-8")
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text(
      "\n".join([f"STATUS={'PASS' if complete else 'INCOMPLETE'}",
                 "JOB=av2-ram-write-watchpoints",
                 f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
                 f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",
                 f"H6_SHA256={hybrid_sha}",f"EXIT_CODE={script_rc}",
                 f"POSITIVE_CONTROL_ADDRESS={'0x%08X'%pos_addr if pos_addr else 'TIDAK TAHU'}",
                 f"POSITIVE_CONTROL_HITS={positive_hits}",
                 f"EVENT_ROWS={raw_total}"])+"\n",encoding="utf-8")
    return script_rc

if __name__=="__main__":
    raise SystemExit(main())
