#!/usr/bin/env python3
"""AS3: K0/K1/K2 two-launch H6 breakpoint A/B; only text and digests are published."""
import argparse,csv,hashlib,os,re,shutil,subprocess,time
from pathlib import Path
from aj2_h6_ram_probe import one,replace_top,encmsg

TARGET_SHA="00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA="9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA="d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
AK1={180:"4c964aaca0afccc68317acd0726fec680c305b903cd426e70afe3d8ac1f1e741",
     240:"16880faeccfca1fbd42d199c1543b00ec8a065bcd53545d14ea4657c9a6c2d5c",
     360:"a9ac5282e9fb9ad1e77f46ef0c291af8e7e5f27b477b6b31e319f971e7dd9942"}
AR3_K2_360="4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907"
RAM_BYTES=0x200000
BP={"K0":[],"K1":[(0x800138EC,"GETTER_800138EC")],
    "K2":[(0x8001387C,"SETTER_8001387C"),(0x800138EC,"GETTER_800138EC"),(0x800B770C,"FUN_800B770C_ENTRY")]}

def sha(b): return hashlib.sha256(b).hexdigest()
def get_ram(state):
    ram=one(one(state,3),1)
    if len(ram)<RAM_BYTES: raise ValueError("RAM segment shorter than 2 MiB")
    return ram[:RAM_BYTES],len(ram)

def lua_source():
 return r'''
if io.stdout then io.stdout:setvbuf("no") end
local loaded,post,started,armed=false,0,false,false
local condition=os.getenv("AS3_CONDITION") or "UNKNOWN"
local bpKeep,returnKeep,returnByRA={},{},{}
local function log(s) print(s);pcall(function() io.stdout:flush() end) end
local function hx(x) if x==nil then return "TIDAK_TAHU" end;return string.format("0x%08X",tonumber(x)) end
local function regs() local r=PCSX.getRegisters();local g=r.GPR.n;return r.pc,g.ra,g.a0,g.a1,g.v0 end
local function event(tag,address)
 local pc,ra,a0,a1,v0=regs()
 log(string.format("AS3_EVENT condition=%s tag=%s frame=%d callback_pc=%s regs_pc=%s ra=%s a0=%s a1=%s v0=%s",condition,tag,post,hx(address),hx(pc),hx(ra),hx(a0),hx(a1),hx(v0)))
 return ra
end
local function armReturn(ra)
 local key=hx(ra)
 if key=="TIDAK_TAHU" or tonumber(ra)==0 then log("AS3_RETURN_ARM_SKIP frame="..post.." ra="..key);return end
 local slot=returnByRA[key];if not slot then slot={pending=0,bp=nil};returnByRA[key]=slot end
 slot.pending=slot.pending+1
 if not slot.bp then
  slot.bp=PCSX.addBreakpoint(tonumber(ra),"Exec",4,"AS3_HELPER_RETURN",function(addr)
   local cur=returnByRA[key]
   if cur and cur.pending>0 then cur.pending=cur.pending-1;event("FUN_800B770C_EXIT",addr) end
   if not cur or cur.pending==0 then if cur then cur.bp=nil end;return false end
   return true
  end)
  returnKeep[#returnKeep+1]=slot
 end
end
local function arm(addr,tag)
 local bp=PCSX.addBreakpoint(addr,"Exec",4,"AS3_"..tag,function(pc)
  local ra=event(tag,pc);if tag=="FUN_800B770C_ENTRY" then armReturn(ra) end;return true
 end)
 bpKeep[#bpKeep+1]=bp
 log(string.format("AS3_BREAKPOINT_ARMED condition=%s frame=%d tag=%s address=%s object=%s",condition,post,tag,hx(addr),tostring(bp~=nil)))
end
local function armCondition()
 if condition=="K0" then log("AS3_BREAKPOINT_SET condition=K0 count=0 frame=180")
 elseif condition=="K1" then arm(0x800138EC,"GETTER_800138EC");log("AS3_BREAKPOINT_SET condition=K1 count=1 frame=180")
 elseif condition=="K2" then
  arm(0x8001387C,"SETTER_8001387C");arm(0x800138EC,"GETTER_800138EC");arm(0x800B770C,"FUN_800B770C_ENTRY")
  log("AS3_BREAKPOINT_SET condition=K2 count=3 frame=180")
 else log("AS3_UNKNOWN_CONDITION="..condition);PCSX.quit(64) end
 armed=true
end
local function capture(frame)
 local ok,err=pcall(function()
  local s=PCSX.createSaveState();local path=string.format("runtime/frame%d.sstate",frame)
  local f=assert(Support.File.open(path,"TRUNCATE"));f:writeMoveSlice(s);f:close()
 end)
 log(ok and ("AS3_FRAME_CAPTURE frame="..frame.." status=PASS") or ("AS3_FRAME_CAPTURE frame="..frame.." status=FAIL error="..tostring(err)))
 if not ok then PCSX.quit(62);return end
 if frame==360 then PCSX.nextTick(function() PCSX.quit(0) end) end
end
_G.as3Loaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
 loaded=true;post=0;log("AS3_SAVE_STATE_LOADED=1 condition="..condition)
end)
_G.as3Vsync=PCSX.Events.createEventListener("GPU::Vsync",function()
 if not started then
  started=true;local path=os.getenv("AS3_H6_STATE") or "resume/h6.sstate"
  log("AS3_LOAD_BEGIN condition="..condition.." path="..path.." gameplay_input=NONE")
  PCSX.pauseEmulator()
  PCSX.nextTick(function()
   local okf,f=pcall(function() return assert(Support.File.open(path)) end)
   if not okf or not f then log("AS3_STATE_OPEN_FAIL="..tostring(f));PCSX.quit(50);return end
   local ok,err=pcall(function() PCSX.loadSaveState(f) end);f:close()
   if not ok then log("AS3_STATE_LOAD_FAIL="..tostring(err));PCSX.quit(51);return end
   log("AS3_LOAD_CALL_RETURNED=1");PCSX.resumeEmulator()
  end)
  return
 end
 if loaded then
  post=post+1
  if post==180 and not armed then
   log("AS3_POST_LOAD_FRAME=180 condition="..condition);armCondition()
   PCSX.nextTick(function() capture(180) end)
  elseif post==240 or post==360 then
   local f=post;log("AS3_POST_LOAD_FRAME="..f.." condition="..condition)
   PCSX.nextTick(function() capture(f) end)
  end
 end
end)
log("AS3_READY_NO_INPUT=1 condition="..condition)
'''

def parse_events(text,cond,attempt):
    out=[]
    pat=re.compile(r"AS3_EVENT condition=(\S+) tag=(\S+) frame=(\d+) callback_pc=(\S+) regs_pc=(\S+) ra=(\S+) a0=(\S+) a1=(\S+) v0=(\S+)")
    for line in text.splitlines():
        m=pat.search(line)
        if m: out.append({"condition":cond,"attempt":attempt,"tag":m.group(2),"frame":m.group(3),
          "callback_pc":m.group(4),"regs_pc":m.group(5),"ra":m.group(6),"a0":m.group(7),"a1":m.group(8),"v0":m.group(9)})
    return out

def write_tsv(path,rows):
    if not rows: path.write_text("status\tTIDAK_TAHU\n",encoding="utf-8");return
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter="\t");w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    for n in ("target","control","pcsx-bin","appdir","bios","cue","card","work","out"): ap.add_argument("--"+n,required=True)
    ap.add_argument("--timeout-seconds",type=int,default=1800);a=ap.parse_args()
    target=Path(a.target).read_bytes();control=Path(a.control).read_bytes()
    if sha(target)!=TARGET_SHA: raise SystemExit("TARGET_SAVESTATE_SHA_MISMATCH")
    if sha(control)!=CONTROL_SHA: raise SystemExit("CONTROL_SAVESTATE_SHA_MISMATCH")
    h6=replace_top(target,6,encmsg(6,one(control,6)))
    if sha(h6)!=H6_SHA: raise SystemExit("H6_HYBRID_SHA_MISMATCH")
    timeout_s=int(a.timeout_seconds)
    if timeout_s<661: raise SystemExit("TIMEOUT_LT_TWICE_KNOWN_AK1_MAX_WALL")
    work,out=Path(a.work),Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (work/"resume").mkdir(parents=True,exist_ok=True);(work/"launches").mkdir(parents=True,exist_ok=True)
    h6path=work/"resume"/"h6-hybrid.sstate";h6path.write_bytes(h6)
    base_card=Path(a.card);base_card_sha=sha(base_card.read_bytes())
    if base_card_sha!="ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5": raise SystemExit("REFERENCE_MCD_SHA_MISMATCH")
    app=Path(a.appdir);base_env=os.environ.copy()
    base_env.update({"DISPLAY":":99","LIBGL_ALWAYS_SOFTWARE":"1",
      "LD_LIBRARY_PATH":str(app/"usr/lib")+":"+str(app/"usr/lib/x86_64-linux-gnu"),
      "QT_PLUGIN_PATH":str(app/"usr/plugins"),"QT_QPA_PLATFORM_PLUGIN_PATH":str(app/"usr/plugins/platforms"),
      "QML2_IMPORT_PATH":str(app/"usr/qml")})
    runs=[];frames=[];events=[]
    for cond in ("K0","K1","K2"):
      for attempt in (1,2):
        launch=work/"launches"/f"{cond}-attempt-{attempt}"
        runtime,home,logs=launch/"runtime",launch/"home",launch/"logs"
        for d in (runtime,home/".config",home/".data",home/"runtime",logs): d.mkdir(parents=True,exist_ok=True)
        try:(home/"runtime").chmod(0o700)
        except OSError:pass
        mcd=launch/"memory-card.mcd";shutil.copyfile(base_card,mcd);mcd_before=sha(mcd.read_bytes())
        lua=launch/"as3.lua";lua.write_text(lua_source(),encoding="utf-8")
        pad=("PCSX.settings.pads[1].DeviceType = 'Analog'\nPCSX.settings.pads[1].Connected = true\n"
          "PCSX.SIO0.slots[1].pads[1].map()\nprint('AS3_CONTROLLER_MAPPED_NO_INPUT=1')\n")
        env=base_env.copy();env.update({"HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),
          "XDG_DATA_HOME":str(home/".data"),"XDG_RUNTIME_DIR":str(home/"runtime"),
          "AS3_H6_STATE":str(h6path),"AS3_CONDITION":cond})
        stdout=logs/"stdout.txt";pcsxlog=logs/"pcsx.log"
        cmd=["timeout","--signal=INT","--kill-after=10s",f"{timeout_s}s",a.pcsx_bin,
          "-noupdate","-debugger","-interpreter","-bios",a.bios,"-iso",a.cue,"-memcard1",str(mcd),
          "-exec",pad,"-dofile",str(lua),"-softgpu","-stdout","-lua_stdout","-logfile",str(pcsxlog),"-run"]
        start=time.monotonic()
        with stdout.open("wb") as f:
            try:rc=subprocess.run(cmd,cwd=launch,env=env,stdout=f,stderr=subprocess.STDOUT,check=False).returncode
            except Exception as e:rc=255;f.write(("AS3_LAUNCH_EXCEPTION="+repr(e)+"\n").encode())
        wall=time.monotonic()-start
        log=stdout.read_text(encoding="utf-8",errors="replace")
        if pcsxlog.exists():log+="\n"+pcsxlog.read_text(encoding="utf-8",errors="replace")
        expected=len(BP[cond]);armed=len(re.findall(r"AS3_BREAKPOINT_ARMED condition=",log))
        bp_frame="AS3_POST_LOAD_FRAME=180" in log;complete=True
        for frame in (180,240,360):
            state=runtime/f"frame{frame}.sstate";marker=f"AS3_FRAME_CAPTURE frame={frame} status=PASS"
            valid=marker in log and state.is_file();status="PASS" if valid else ("CAPTURE_FAILED" if f"AS3_FRAME_CAPTURE frame={frame} status=FAIL" in log else "TIDAK ADA CAPTURE")
            digest="TIDAK TAHU";ram_len=0
            if valid:
                try:ram,ram_len=get_ram(state.read_bytes());digest=sha(ram)
                except Exception as e:status="PARSE_ERROR";(logs/f"ram-{frame}-error.txt").write_text(repr(e)+"\n",encoding="utf-8")
            if status!="PASS":complete=False
            frames.append({"condition":cond,"attempt":attempt,"frame":frame,"capture_status":status,"ram_2mib_sha256":digest,"ram_segment_bytes":ram_len})
            try:state.unlink()
            except OSError:pass
        mcd_after=sha(mcd.read_bytes()) if mcd.exists() else "TIDAK TAHU"
        ev=parse_events(log,cond,attempt);events.extend(ev)
        counts={tag:sum(1 for x in ev if x["tag"]==tag) for tag in ("SETTER_8001387C","GETTER_800138EC","FUN_800B770C_ENTRY","FUN_800B770C_EXIT")}
        if rc in (124,137,143):emulator_exit="TIDAK TAHU";exit_source=f"timeout wrapper rc={rc}"
        elif rc==0 and "AS3_FRAME_CAPTURE frame=360 status=PASS" in log:emulator_exit="0";exit_source="PCSX quit(0) after frame360 capture"
        else:emulator_exit=str(rc);exit_source="timeout-wrapped process rc (not independently confirmed guest exit)"
        runs.append({"condition":cond,"attempt":attempt,"frame180_marker":"YES" if bp_frame else "NO",
          "breakpoint_expected":expected,"breakpoint_armed":armed,"breakpoints_armed":"YES" if bp_frame and armed==expected else "NO",
          "all_frames_captured":"YES" if complete else "NO","emulator_exit_code_decimal":emulator_exit,"exit_source":exit_source,
          "timeout_wrapper_exit_decimal":rc,"wall_seconds":f"{wall:.3f}","memory_card_sha256_before":mcd_before,
          "memory_card_sha256_after":mcd_after,"memory_card_unchanged":"YES" if mcd_before==mcd_after else "NO",
          "setter_hits":counts["SETTER_8001387C"],"getter_hits":counts["GETTER_800138EC"],
          "helper_entry_hits":counts["FUN_800B770C_ENTRY"],"helper_exit_hits":counts["FUN_800B770C_EXIT"]})
    runmap={(r["condition"],r["attempt"]):r for r in runs}
    for x in frames:
        m=runmap[(x["condition"],x["attempt"])]
        for k in ("emulator_exit_code_decimal","wall_seconds","memory_card_sha256_before","memory_card_sha256_after"):x[k]=m[k]
    write_tsv(out/"AS3_LAUNCHES.tsv",frames);write_tsv(out/"AS3_RUNS.tsv",runs)
    with (out/"AS3_BREAKPOINT_EVENTS.tsv").open("w",encoding="utf-8",newline="") as f:
        cols=["condition","attempt","tag","frame","callback_pc","regs_pc","ra","a0","a1","v0"]
        w=csv.DictWriter(f,fieldnames=cols,delimiter="\t");w.writeheader();w.writerows(events)
    h={(x["condition"],x["attempt"],int(x["frame"])):x["ram_2mib_sha256"] for x in frames}
    lines=["AS3 — H6 HYBRID BREAKPOINT A/B; K0/K1/K2; TWO LAUNCHES EACH",
      f"H6_SHA256={H6_SHA}","H6=target checkpoint base plus CONTROL protobuf field6; HYBRID, NOT TARGET-PURE",
      "GAMEPLAY_INPUT=NONE","K0=NO_BREAKPOINTS","K1=GETTER_ONLY_0x800138EC",
      "K2=AR3_SETTER_0x8001387C_GETTER_0x800138EC_HELPER_0x800B770C",
      "BREAKPOINT_INSTALL_FRAME=180","RAM_SHA256=first 2 MiB after load at frames 180,240,360",
      f"TIMEOUT_PER_LAUNCH_SECONDS={timeout_s}",f"AK1_BASELINE_180={AK1[180]}",
      f"AK1_BASELINE_240={AK1[240]}",f"AK1_BASELINE_360={AK1[360]}",f"AR3_K2_FRAME360={AR3_K2_360}",""]
    for r in runs:lines.append(f"{r['condition']}_ATTEMPT_{r['attempt']} armed={r['breakpoints_armed']} bp={r['breakpoint_armed']}/{r['breakpoint_expected']} frames={r['all_frames_captured']} emulator_exit={r['emulator_exit_code_decimal']} wrapper_rc={r['timeout_wrapper_exit_decimal']} wall_s={r['wall_seconds']} MCD_unchanged={r['memory_card_unchanged']}")
    lines.extend(["","## RAM hashes by condition/launch/frame"])
    for x in frames:lines.append(f"{x['condition']}_ATTEMPT_{x['attempt']}_FRAME_{x['frame']}={x['ram_2mib_sha256']} capture={x['capture_status']}")
    lines.extend(["","## K0 versus AK1 baseline"]);k0_ok=[]
    for attempt in (1,2):
        for frame,expected in AK1.items():
            actual=h.get(("K0",attempt,frame),"TIDAK TAHU");same=actual==expected;k0_ok.append(same)
            lines.append(f"K0_ATTEMPT_{attempt}_FRAME_{frame}_MATCH_AK1={same} actual={actual} expected={expected}")
    lines.extend(["","## K1/K2 breakpoint condition versus paired K0 launch"]);anydiff=False
    for cond in ("K1","K2"):
        diffs=[]
        for attempt in (1,2):
            for frame in (180,240,360):
                a0=h.get(("K0",attempt,frame),"TIDAK TAHU");ac=h.get((cond,attempt,frame),"TIDAK TAHU")
                if a0!="TIDAK TAHU" and ac!="TIDAK TAHU" and a0!=ac:diffs.append((frame,attempt,a0,ac))
        if diffs:
            anydiff=True;first=min(x[0] for x in diffs);lines.append(f"{cond}_FIRST_HASH_DIFFERENCE_FROM_K0=FRAME_{first}")
            for frame,attempt,a0,ac in diffs:
                if frame==first:lines.append(f"{cond}_DIFF_ATTEMPT_{attempt}_FRAME_{frame}_K0={a0}_{cond}={ac}")
        elif all(h.get((c,a,f),"TIDAK TAHU")!="TIDAK TAHU" for c in ("K0",cond) for a in (1,2) for f in (180,240,360)):
            lines.append(f"{cond}_HASH_DIFFERENCE_FROM_K0=NONE_AT_CAPTURED_FRAMES_180_240_360")
        else:lines.append(f"{cond}_HASH_DIFFERENCE_FROM_K0=TIDAK TAHU_INCOMPLETE")
    lines.extend(["","## K2 versus AR3 frame360"])
    for a in (1,2):
        actual=h.get(("K2",a,360),"TIDAK TAHU");lines.append(f"K2_ATTEMPT_{a}_MATCH_AR3={actual==AR3_K2_360} actual={actual} expected={AR3_K2_360}")
    lines.extend(["","## Breakpoint hit counts"])
    for r in runs:lines.append(f"{r['condition']}_ATTEMPT_{r['attempt']}: setter={r['setter_hits']} getter={r['getter_hits']} helper_entry={r['helper_entry_hits']} helper_exit={r['helper_exit_hits']}")
    maxwall=max(float(r["wall_seconds"]) for r in runs);timeout_ok=timeout_s>=2*maxwall
    complete=all(r["all_frames_captured"]=="YES" and r["breakpoints_armed"]=="YES" and r["emulator_exit_code_decimal"]=="0" and r["memory_card_unchanged"]=="YES" for r in runs)
    status="PASS" if complete and timeout_ok else "INCOMPLETE"
    lines.extend(["",f"OBSERVED_MAX_WALL_SECONDS={maxwall:.3f}",f"TIMEOUT_GE_2X_OBSERVED_MAX_WALL={timeout_ok}",
      f"ALL_SIX_LAUNCHES_COMPLETE={complete}","ZERO_HITS=No observed execution only; not proof of function non-use.",
      "EFFECT_LIMIT=Equal sampled RAM hashes mean no observed difference at 180/240/360 only; no inference about intermediate frames.",
      f"K0_ALL_SIX_SAMPLES_MATCH_AK1={all(k0_ok)}"])
    (out/"AS3_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    script_rc=0 if status=="PASS" else 2
    (out/"AS3_SCRIPT_EXIT_CODE.txt").write_text(f"AS3_SCRIPT_EXIT_CODE={script_rc}\n",encoding="utf-8")
    actions=[f"STATUS={status}","JOB=as3-h6-breakpoint-ab",f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
      f"RUN_ATTEMPT={os.getenv('GITHUB_RUN_ATTEMPT','TIDAK TAHU')}",f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",
      f"H6_SHA256={H6_SHA}",f"EXIT_CODE={script_rc}",f"TIMEOUT_PER_LAUNCH_S={timeout_s}",
      f"TIMEOUT_GE_2X_OBSERVED_MAX_WALL={timeout_ok}",f"OBSERVED_MAX_WALL_SECONDS={maxwall:.3f}"]
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text("\n".join(actions)+"\n",encoding="utf-8")
    print("\n".join(actions));return 0

if __name__=="__main__":raise SystemExit(main())
