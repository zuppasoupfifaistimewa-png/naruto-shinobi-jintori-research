#!/usr/bin/env python3
"""AT2: H6 hybrid restore, no debugger/breakpoints, no gameplay input."""
import argparse,csv,hashlib,os,re,shutil,subprocess,time
from pathlib import Path
from aj2_h6_ram_probe import one,replace_top,encmsg

TARGET_SHA="00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA="9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA="d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
MCD_SHA="ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5"
RAM_SIZE=0x200000
FRAMES=(180,240,360)
BASELINES={
 "AK1":{180:"4c964aaca0afccc68317acd0726fec680c305b903cd426e70afe3d8ac1f1e741",
        240:"16880faeccfca1fbd42d199c1543b00ec8a065bcd53545d14ea4657c9a6c2d5c",
        360:"a9ac5282e9fb9ad1e77f46ef0c291af8e7e5f27b477b6b31e319f971e7dd9942"},
 "AS3_K0":{180:"5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7",
           240:"75df26c668759d1a70a4765e87cab077184442381b84e3d1112ce05bf5627ec0",
           360:"4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907"}}
FLAGS={
 "F1":["-no-debugger","-no-gdb","-dynarec"],
 "F2":["-interpreter","-no-debugger","-no-gdb"]}
def sha(b): return hashlib.sha256(b).hexdigest()
def ram2m(state):
    ram=one(one(state,3),1)
    if len(ram)<RAM_SIZE: raise ValueError("RAM segment < 2 MiB")
    return ram[:RAM_SIZE],len(ram)
def write_tsv(path,rows,fields=None):
    if fields is None: fields=list(rows[0]) if rows else ["status"]
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore")
        w.writeheader()
        for r in rows:w.writerow(r)
def lua_script():
 return r'''
if io.stdout then io.stdout:setvbuf("no") end
local begun,loaded,post=false,false,0
local epoch=os.time()
local function log(s) print(s);pcall(function() io.stdout:flush() end) end
local function capture(frame)
 local ok,err=pcall(function()
  local state=PCSX.createSaveState()
  local path=string.format("runtime/frame%d.sstate",frame)
  local f=assert(Support.File.open(path,"TRUNCATE"));f:writeMoveSlice(state);f:close()
 end)
 log(ok and ("AT2_CAPTURE frame="..frame.." status=PASS elapsed="..tostring(os.time()-epoch)) or
     ("AT2_CAPTURE frame="..frame.." status=FAIL error="..tostring(err)))
 if not ok then PCSX.quit(62);return end
 if frame==360 then log("AT2_QUIT0_AFTER_FRAME360=1");PCSX.quit(0) end
end
_G.at2Load=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
 loaded=true;post=0;log("AT2_STATE_LOADED=1")
end)
_G.at2Vsync=PCSX.Events.createEventListener("GPU::Vsync",function()
 if not begun then
  begun=true;local path=os.getenv("AT2_H6_STATE") or "resume/h6-hybrid.sstate"
  log("AT2_LOAD_BEGIN path="..path.." GAMEPLAY_INPUT=NONE")
  PCSX.pauseEmulator()
  PCSX.nextTick(function()
   local okf,f=pcall(function() return assert(Support.File.open(path)) end)
   if not okf or not f then log("AT2_STATE_OPEN_FAIL="..tostring(f));PCSX.quit(50);return end
   local ok,err=pcall(function() PCSX.loadSaveState(f) end);f:close()
   if not ok then log("AT2_STATE_LOAD_FAIL="..tostring(err));PCSX.quit(51);return end
   log("AT2_LOAD_CALL_RETURNED=1");PCSX.resumeEmulator()
  end)
  return
 end
 if loaded then
  post=post+1
  for _,frame in ipairs({180,240,360}) do
   if post==frame then
    log("AT2_POST_LOAD_FRAME="..frame.." elapsed="..tostring(os.time()-epoch))
    local n=frame;PCSX.nextTick(function() capture(n) end)
   end
  end
 end
end)
log("AT2_READY_NO_INPUT_NO_BREAKPOINTS=1")
'''
def main():
 ap=argparse.ArgumentParser()
 for x in ("target","control","pcsx-bin","appdir","bios","cue","card","work","out"):ap.add_argument("--"+x,required=True)
 ap.add_argument("--timeout-seconds",type=int,default=1800)
 a=ap.parse_args()
 target=Path(a.target).read_bytes();control=Path(a.control).read_bytes()
 if sha(target)!=TARGET_SHA:raise SystemExit("TARGET_SAVESTATE_SHA_MISMATCH")
 if sha(control)!=CONTROL_SHA:raise SystemExit("CONTROL_SAVESTATE_SHA_MISMATCH")
 h6=replace_top(target,6,encmsg(6,one(control,6)))
 if sha(h6)!=H6_SHA:raise SystemExit("H6_HYBRID_SHA_MISMATCH")
 timeout_s=int(a.timeout_seconds)
 if timeout_s<2*142.696:raise SystemExit("TIMEOUT_LT_2X_KNOWN_SLOWEST_142.696")
 work,out=Path(a.work),Path(a.out);out.mkdir(parents=True,exist_ok=True)
 (work/"resume").mkdir(parents=True,exist_ok=True);(work/"launches").mkdir(parents=True,exist_ok=True)
 h6path=work/"resume"/"h6-hybrid.sstate";h6path.write_bytes(h6)
 card0=Path(a.card)
 if sha(card0.read_bytes())!=MCD_SHA or card0.stat().st_size!=131072:raise SystemExit("REFERENCE_MCD_MISMATCH")
 app=Path(a.appdir)
 env0=os.environ.copy()
 env0.update({"DISPLAY":":99","LIBGL_ALWAYS_SOFTWARE":"1",
  "LD_LIBRARY_PATH":str(app/"usr/lib")+":"+str(app/"usr/lib/x86_64-linux-gnu"),
  "QT_PLUGIN_PATH":str(app/"usr/plugins"),"QT_QPA_PLATFORM_PLUGIN_PATH":str(app/"usr/plugins/platforms"),
  "QML2_IMPORT_PATH":str(app/"usr/qml")})
 launches=[];frames=[]
 for mode in ("F1","F2"):
  for attempt in (1,2):
   root=work/"launches"/f"{mode}-attempt-{attempt}"
   runtime,home=root/"runtime",root/"home"
   for d in (runtime,home/".config",home/".data",home/"runtime"):d.mkdir(parents=True,exist_ok=True)
   try:(home/"runtime").chmod(0o700)
   except OSError:pass
   mcd=root/"memory-card.mcd";shutil.copyfile(card0,mcd);mcd_before=sha(mcd.read_bytes())
   luap=root/"at2.lua";luap.write_text(lua_script(),encoding="utf-8")
   pad="PCSX.settings.pads[1].DeviceType='Analog'\nPCSX.settings.pads[1].Connected=true\nPCSX.SIO0.slots[1].pads[1].map()\nprint('AT2_PAD_READY_NO_INPUT=1')\n"
   env=env0.copy();env.update({"HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),
    "XDG_DATA_HOME":str(home/".data"),"XDG_RUNTIME_DIR":str(home/"runtime"),
    "AT2_H6_STATE":str(h6path)})
   pcsxlog=root/"pcsx.log";stdout=root/"stdout.log"
   command=["timeout","--signal=INT","--kill-after=10s",f"{timeout_s}s",a.pcsx_bin,
    "-noupdate",*FLAGS[mode],"-bios",a.bios,"-iso",a.cue,"-memcard1",str(mcd),
    "-exec",pad,"-dofile",str(luap),"-softgpu","-stdout","-lua_stdout","-logfile",str(pcsxlog),"-run"]
   start=time.monotonic()
   with stdout.open("wb") as fh:
    try:proc=subprocess.run(command,cwd=root,env=env,stdout=fh,stderr=subprocess.STDOUT,check=False);rc=proc.returncode
    except Exception as exc:rc=255;fh.write(("AT2_EXCEPTION="+repr(exc)+"\n").encode())
   wall=time.monotonic()-start
   log=stdout.read_text(encoding="utf-8",errors="replace")
   if pcsxlog.exists():log+="\n"+pcsxlog.read_text(encoding="utf-8",errors="replace")
   timed=rc in (124,137,143)
   emu_exit="TIDAK TAHU" if timed else str(rc)
   frame360=("AT2_CAPTURE frame=360 status=PASS" in log and (runtime/"frame360.sstate").is_file())
   mcd_after=sha(mcd.read_bytes()) if mcd.exists() else "TIDAK TAHU"
   marker360=bool(re.search(r"AT2_POST_LOAD_FRAME=360 elapsed=(\d+)",log))
   launches.append({"mode":mode,"attempt":attempt,"flags":" ".join(FLAGS[mode]),"emulator_exit_code_decimal":emu_exit,
    "timeout_wrapper_exit_decimal":rc,"wall_seconds":f"{wall:.3f}","frame360_marker":str(marker360).upper(),
    "frame360_capture":"PASS" if frame360 else "FAIL","memory_card_sha256_before":mcd_before,
    "memory_card_sha256_after":mcd_after,"memory_card_unchanged":str(mcd_before==mcd_after).upper(),
    "timeout_seconds":timeout_s})
   for frame in FRAMES:
    state=runtime/f"frame{frame}.sstate"
    marker=re.search(rf"AT2_POST_LOAD_FRAME={frame} elapsed=(\d+)",log)
    cap=f"AT2_CAPTURE frame={frame} status=PASS" in log and state.is_file() and marker is not None
    digest="TIDAK TAHU";segment=0
    if cap:
     try:ram,segment=ram2m(state.read_bytes());digest=sha(ram)
     except Exception:cap=False
    frames.append({"mode":mode,"attempt":attempt,"frame":frame,"capture_status":"PASS" if cap else "FAIL",
      "elapsed_seconds":marker.group(1) if marker else "TIDAK TAHU","ram_first_2mib_sha256":digest,
      "ram_segment_bytes":segment})
   for frame in FRAMES:
    if (runtime/f"frame{frame}.sstate").exists():(runtime/f"frame{frame}.sstate").unlink()
 write_tsv(out/"AT2_LAUNCHES.tsv",launches)
 write_tsv(out/"AT2_FRAMES.tsv",frames)
 comparisons=[]
 for x in frames:
  if x["capture_status"]!="PASS":continue
  for baseline,hashes in BASELINES.items():
   comparisons.append({"mode":x["mode"],"attempt":x["attempt"],"frame":x["frame"],"baseline":baseline,
    "baseline_sha256":hashes[x["frame"]],"observed_sha256":x["ram_first_2mib_sha256"],
    "match":str(x["ram_first_2mib_sha256"]==hashes[x["frame"]]).upper()})
 write_tsv(out/"AT2_BASELINE_COMPARISON.tsv",comparisons)
 maxwall=max((float(x["wall_seconds"]) for x in launches),default=0.0)
 timeout_ok=timeout_s>=2*maxwall
 complete=(len(launches)==4 and len(frames)==12 and all(x["capture_status"]=="PASS" for x in frames)
  and all(x["emulator_exit_code_decimal"]=="0" and x["memory_card_unchanged"]=="TRUE" for x in launches)
  and timeout_ok)
 report=[
  "AT2 — H6 HYBRID FLAG COMPARISON; NO GAMEPLAY INPUT; NO BREAKPOINTS",
  f"H6_SHA256={H6_SHA}",
  "H6_IDENTITY=target checkpoint base + CONTROL top-level protobuf SPU field 6; HYBRID, NOT TARGET-PURE",
  "CONDITIONS=F1 -no-debugger -no-gdb -dynarec; F2 -interpreter -no-debugger -no-gdb",
  "REPLAY=two independent launches per condition; capture post-load GPU::Vsync frames 180, 240, 360; no gameplay input; no breakpoints",
  f"TIMEOUT_PER_LAUNCH_SECONDS={timeout_s}",
  f"OBSERVED_MAX_WALL_SECONDS={maxwall:.3f}",
  f"TIMEOUT_GE_2X_OBSERVED_MAX={timeout_ok}",
  f"RUNTIME_CAPTURE_COMPLETE={complete}",
  "AK1_BASELINES=frame 180 4c964aac...e741; frame 240 16880fae...2d5c; frame 360 a9ac5282...9942",
  "AS3_K0_BASELINES=frame 180 5167f48f...09b7; frame 240 75df26c6...7ec0; frame 360 4d002df6...a7907",
  "Cause of hash differences, when any: TIDAK TAHU unless explained by controlled comparison."
 ]
 for x in launches:report.append(f"{x['mode']}_ATTEMPT_{x['attempt']} EXIT={x['emulator_exit_code_decimal']} WALL={x['wall_seconds']} MCD_UNCHANGED={x['memory_card_unchanged']} FRAME360={x['frame360_capture']}")
 for x in comparisons:report.append(f"COMPARE {x['mode']}#{x['attempt']} frame{x['frame']} vs {x['baseline']} match={x['match']}")
 (out/"AT2_SUMMARY.txt").write_text("\n".join(report)+"\n",encoding="utf-8")
 status="PASS" if complete else "INCOMPLETE"
 exitcode=0 if complete else 2
 (out/"ACTIONS_RUN_SUMMARY.txt").write_text("\n".join([
  f"STATUS={status}","JOB=at2-h6-flags-ab",f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
  f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",f"H6_SHA256={H6_SHA}",f"EXIT_CODE={exitcode}",
  f"TIMEOUT_PER_LAUNCH_SECONDS={timeout_s}",f"TIMEOUT_GE_2X_OBSERVED_MAX={timeout_ok}"])+"\n",encoding="utf-8")
 return exitcode
if __name__=="__main__":raise SystemExit(main())
