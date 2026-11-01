#!/usr/bin/env python3
"""AT3: AN2 schedules A/C x K0/K2, two launches each, interpreter+debugger."""
import argparse,csv,hashlib,os,re,shutil,subprocess,time
from collections import Counter
from pathlib import Path
from aj2_h6_ram_probe import one,replace_top,encmsg

TARGET_SHA="00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA="9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA="d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
MCD_SHA="ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5"
RAM_SIZE=0x200000
FRAMES=(180,240,360)
HISTORICAL_SLOWEST_WALL_S=142.696
BP={"SETTER_8001387C":0x8001387C,"GETTER_800138EC":0x800138EC,"HELPER_800B770C":0x800B770C}
def sha(b):return hashlib.sha256(b).hexdigest()
def ram2m(state):
 ram=one(one(state,3),1)
 if len(ram)<RAM_SIZE:raise ValueError("RAM segment < 2 MiB")
 return ram[:RAM_SIZE],len(ram)
def write_tsv(path,rows,fields=None):
 if fields is None:fields=list(rows[0]) if rows else ["status"]
 with path.open("w",encoding="utf-8",newline="") as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore");w.writeheader()
  for r in rows:w.writerow(r)
def read_schedule(path):
 schedules={}
 with Path(path).open(encoding="utf-8",newline="") as f:
  for r in csv.DictReader(f,delimiter="\t"):
   name=r["schedule"]
   if name not in ("A","C") or name in schedules or int(r["launch_count"])!=2:raise ValueError("unexpected input schedule row "+str(r))
   if name=="C":
    if r["button"]!="NONE" or int(r["press_frame"])!=0 or int(r["release_frame"])!=0:raise ValueError("schedule C is not no-input")
    schedules[name]=None
   else:
    if r["button"]!="CIRCLE" or int(r["press_frame"])!=60 or int(r["release_frame"])!=61:raise ValueError("schedule A must be CIRCLE frame 60–61")
    schedules[name]=60
 if schedules!={"A":60,"C":None}:raise ValueError("need exactly A and C")
 return schedules
def lua_source(condition,mode,press):
 press_frame=press or 0
 return f'''
if io.stdout then io.stdout:setvbuf("no") end
local started,loaded,post,armed=false,false,0,false
local condition="{condition}"
local mode="{mode}"
local pressFrame={press_frame}
local pad=PCSX.SIO0.slots[1].pads[1]
local circle=PCSX.CONSTS.PAD.BUTTON.CIRCLE
local keep,returnKeep,returnByRA={{}},{{}},{{}}
local function log(s) print(s);pcall(function() io.stdout:flush() end) end
local function hx(x) if x==nil then return "TIDAK_TAHU" end;return string.format("0x%08X",tonumber(x)) end
local function regs()
 local r=PCSX.getRegisters();local g=r.GPR.n
 return r.pc,g.ra,g.a0,g.a1,g.v0
end
local function event(tag,address)
 local pc,ra,a0,a1,v0=regs()
 log(string.format("AT3_EVENT condition=%s mode=%s tag=%s frame=%d callback_pc=%s regs_pc=%s a0=%s a1=%s ra=%s v0=%s",
  condition,mode,tag,post,hx(address),hx(pc),hx(a0),hx(a1),hx(ra),hx(v0)))
 return ra
end
local function armReturn(ra)
 local key=hx(ra)
 if key=="TIDAK_TAHU" or tonumber(ra)==0 then log("AT3_RETURN_ARM_SKIP frame="..post.." ra="..key);return end
 local slot=returnByRA[key]
 if not slot then slot={{pending=0,bp=nil}};returnByRA[key]=slot end
 slot.pending=slot.pending+1
 if not slot.bp then
  slot.bp=PCSX.addBreakpoint(tonumber(ra),"Exec",4,"AT3_GETTER_RETURN",function(addr)
   local cur=returnByRA[key]
   if cur and cur.pending>0 then cur.pending=cur.pending-1;event("GETTER_RETURN",addr) end
   if not cur or cur.pending==0 then if cur then cur.bp=nil end;return false end
   return true
  end)
  returnKeep[#returnKeep+1]=slot
 end
end
local function arm(address,tag)
 local bp=PCSX.addBreakpoint(address,"Exec",4,"AT3_"..tag,function(addr)
  local ra=event(tag,addr)
  if tag=="GETTER_800138EC" then armReturn(ra) end
  return true
 end)
 keep[#keep+1]=bp
 log(string.format("AT3_BREAKPOINT_ARMED condition=%s mode=%s tag=%s address=%s object=%s",
  condition,mode,tag,hx(address),tostring(bp~=nil)))
end
local function armAll()
 if mode=="K2" then
  arm(0x8001387C,"SETTER_8001387C")
  arm(0x800138EC,"GETTER_800138EC")
  arm(0x800B770C,"HELPER_800B770C")
  log("AT3_BREAKPOINT_SET condition="..condition.." mode=K2 count=3 frame=180")
 else
  log("AT3_BREAKPOINT_SET condition="..condition.." mode=K0 count=0 frame=180")
 end
 armed=true
end
local function input(phase)
 local ok,value=pcall(function()
  if phase=="press" then pad.setOverride(circle) else pad.clearOverride(circle) end
  return pad.getButton(circle)
 end)
 local pass=ok and value==(phase=="press")
 log("AT3_INPUT condition="..condition.." phase="..phase.." frame="..post.." readback="..tostring(value).." status="..(pass and "PASS" or "FAIL"))
 if not pass then PCSX.quit(83) end
end
local function capture(frame)
 local ok,err=pcall(function()
  local s=PCSX.createSaveState()
  local f=assert(Support.File.open(string.format("runtime/frame%d.sstate",frame),"TRUNCATE"))
  f:writeMoveSlice(s);f:close()
 end)
 log(ok and ("AT3_CAPTURE condition="..condition.." mode="..mode.." frame="..frame.." status=PASS") or
  ("AT3_CAPTURE condition="..condition.." mode="..mode.." frame="..frame.." status=FAIL error="..tostring(err)))
 if not ok then PCSX.quit(62);return end
 if frame==360 then log("AT3_QUIT0_AFTER_FRAME360=1");PCSX.quit(0) end
end
_G.at3Load=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
 loaded=true;post=0;log("AT3_STATE_LOADED condition="..condition.." mode="..mode)
end)
_G.at3Vsync=PCSX.Events.createEventListener("GPU::Vsync",function()
 if not started then
  started=true;local path=os.getenv("AT3_H6_STATE") or "resume/h6-hybrid.sstate"
  log("AT3_LOAD_BEGIN condition="..condition.." mode="..mode.." path="..path.." INPUT_IS_SCHEDULED_ONLY=1")
  PCSX.pauseEmulator()
  PCSX.nextTick(function()
   local okf,f=pcall(function() return assert(Support.File.open(path)) end)
   if not okf or not f then log("AT3_STATE_OPEN_FAIL="..tostring(f));PCSX.quit(50);return end
   local ok,err=pcall(function() PCSX.loadSaveState(f) end);f:close()
   if not ok then log("AT3_STATE_LOAD_FAIL="..tostring(err));PCSX.quit(51);return end
   log("AT3_LOAD_CALL_RETURNED=1");PCSX.resumeEmulator()
  end)
  return
 end
 if loaded then
  post=post+1
  if pressFrame>0 then
   if post==pressFrame then input("press") end
   if post==pressFrame+1 then input("release") end
  end
  if post==180 and not armed then armAll();PCSX.nextTick(function() capture(180) end)
  elseif post==240 or post==360 then local f=post;PCSX.nextTick(function() capture(f) end) end
 end
end)
log("AT3_READY condition="..condition.." mode="..mode.." postload_press_frame="..pressFrame)
'''
def parse_events(text,condition,mode,attempt):
 out=[]
 pat=re.compile(r"AT3_EVENT condition=(\S+) mode=(\S+) tag=(\S+) frame=(\d+) callback_pc=(\S+) regs_pc=(\S+) a0=(\S+) a1=(\S+) ra=(\S+) v0=(\S+)")
 for line in text.splitlines():
  m=pat.search(line)
  if m:out.append({"condition":condition,"mode":mode,"attempt":attempt,"tag":m.group(3),"frame":m.group(4),
   "pc":m.group(5),"regs_pc":m.group(6),"a0":m.group(7),"a1":m.group(8),"ra":m.group(9),"v0":m.group(10)})
 return out
def main():
 ap=argparse.ArgumentParser()
 for x in ("target","control","pcsx-bin","appdir","bios","cue","card","work","out","schedule"):ap.add_argument("--"+x,required=True)
 ap.add_argument("--timeout-seconds",type=int,default=1800)
 a=ap.parse_args()
 target=Path(a.target).read_bytes();control=Path(a.control).read_bytes()
 if sha(target)!=TARGET_SHA:raise SystemExit("TARGET_SAVESTATE_SHA_MISMATCH")
 if sha(control)!=CONTROL_SHA:raise SystemExit("CONTROL_SAVESTATE_SHA_MISMATCH")
 h6=replace_top(target,6,encmsg(6,one(control,6)))
 if sha(h6)!=H6_SHA:raise SystemExit("H6_HYBRID_SHA_MISMATCH")
 schedules=read_schedule(a.schedule)
 timeout_s=int(a.timeout_seconds)
 if timeout_s<2*HISTORICAL_SLOWEST_WALL_S:raise SystemExit("TIMEOUT_LT_2X_KNOWN_SLOWEST")
 work,out=Path(a.work),Path(a.out);out.mkdir(parents=True,exist_ok=True)
 for d in ("resume","launches"): (work/d).mkdir(parents=True,exist_ok=True)
 h6path=work/"resume"/"h6-hybrid.sstate";h6path.write_bytes(h6)
 card0=Path(a.card)
 if sha(card0.read_bytes())!=MCD_SHA or card0.stat().st_size!=131072:raise SystemExit("REFERENCE_MCD_MISMATCH")
 app=Path(a.appdir)
 env0=os.environ.copy()
 env0.update({"DISPLAY":":99","LIBGL_ALWAYS_SOFTWARE":"1",
  "LD_LIBRARY_PATH":str(app/"usr/lib")+":"+str(app/"usr/lib/x86_64-linux-gnu"),
  "QT_PLUGIN_PATH":str(app/"usr/plugins"),"QT_QPA_PLATFORM_PLUGIN_PATH":str(app/"usr/plugins/platforms"),
  "QML2_IMPORT_PATH":str(app/"usr/qml")})
 launches=[];frames=[];events=[]
 for cond in ("C","A"):
  for mode in ("K0","K2"):
   for attempt in (1,2):
    root=work/"launches"/f"{cond}-{mode}-attempt-{attempt}"
    runtime,home=root/"runtime",root/"home"
    for d in (runtime,home/".config",home/".data",home/"runtime"):d.mkdir(parents=True,exist_ok=True)
    try:(home/"runtime").chmod(0o700)
    except OSError:pass
    mcd=root/"memory-card.mcd";shutil.copyfile(card0,mcd);mcd_before=sha(mcd.read_bytes())
    luap=root/"at3.lua";luap.write_text(lua_source(cond,mode,schedules[cond]),encoding="utf-8")
    pad="PCSX.settings.pads[1].DeviceType='Analog'\nPCSX.settings.pads[1].Connected=true\nPCSX.SIO0.slots[1].pads[1].map()\nprint('AT3_PAD_READY=PASS')\n"
    env=env0.copy();env.update({"HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),
     "XDG_DATA_HOME":str(home/".data"),"XDG_RUNTIME_DIR":str(home/"runtime"),
     "AT3_H6_STATE":str(h6path)})
    pcsxlog=root/"pcsx.log";stdout=root/"stdout.log"
    command=["timeout","--signal=INT","--kill-after=10s",f"{timeout_s}s",a.pcsx_bin,
     "-noupdate","-debugger","-interpreter","-bios",a.bios,"-iso",a.cue,"-memcard1",str(mcd),
     "-exec",pad,"-dofile",str(luap),"-softgpu","-stdout","-lua_stdout","-logfile",str(pcsxlog),"-run"]
    start=time.monotonic()
    with stdout.open("wb") as fh:
     try:proc=subprocess.run(command,cwd=root,env=env,stdout=fh,stderr=subprocess.STDOUT,check=False);rc=proc.returncode
     except Exception as exc:rc=255;fh.write(("AT3_EXCEPTION="+repr(exc)+"\n").encode())
    wall=time.monotonic()-start
    log=stdout.read_text(encoding="utf-8",errors="replace")
    if pcsxlog.exists():log+="\n"+pcsxlog.read_text(encoding="utf-8",errors="replace")
    timeout_hit=rc in (124,137,143)
    emu_exit="TIDAK TAHU" if timeout_hit else str(rc)
    card_after=sha(mcd.read_bytes()) if mcd.exists() else "TIDAK TAHU"
    ev=parse_events(log,cond,mode,attempt);events.extend(ev)
    pressok=(cond=="C" or "AT3_INPUT condition=A phase=press frame=60" in log and "status=PASS" in log.split("AT3_INPUT condition=A phase=press frame=60")[-1].splitlines()[0])
    relok=(cond=="C" or "AT3_INPUT condition=A phase=release frame=61" in log and "status=PASS" in log.split("AT3_INPUT condition=A phase=release frame=61")[-1].splitlines()[0])
    armed=(mode=="K0" or "AT3_BREAKPOINT_SET condition=A mode=K2 count=3 frame=180" in log or "AT3_BREAKPOINT_SET condition=C mode=K2 count=3 frame=180" in log)
    launches.append({"condition":cond,"mode":mode,"attempt":attempt,"flags":"-debugger -interpreter",
     "breakpoints_armed":"YES" if armed else ("NOT_APPLICABLE" if mode=="K0" else "NO"),
     "circle_press_readback":"NOT_APPLICABLE" if cond=="C" else ("PASS" if pressok else "FAIL"),
     "circle_release_readback":"NOT_APPLICABLE" if cond=="C" else ("PASS" if relok else "FAIL"),
     "emulator_exit_code_decimal":emu_exit,"timeout_wrapper_exit_decimal":rc,"wall_seconds":f"{wall:.3f}",
     "memory_card_sha256_before":mcd_before,"memory_card_sha256_after":card_after,
     "memory_card_unchanged":str(mcd_before==card_after).upper(),"timeout_seconds":timeout_s})
    for frame in FRAMES:
     state=runtime/f"frame{frame}.sstate"
     cap=(f"AT3_CAPTURE condition={cond} mode={mode} frame={frame} status=PASS" in log and state.is_file())
     digest="TIDAK TAHU";seg=0
     if cap:
      try:ram,seg=ram2m(state.read_bytes());digest=sha(ram)
      except Exception:cap=False
     frames.append({"condition":cond,"mode":mode,"attempt":attempt,"frame":frame,
      "capture_status":"PASS" if cap else "FAIL","ram_first_2mib_sha256":digest,"ram_segment_bytes":seg})
     if state.exists():state.unlink()
 write_tsv(out/"AT3_LAUNCHES.tsv",launches)
 write_tsv(out/"AT3_FRAMES.tsv",frames)
 write_tsv(out/"AT3_BREAKPOINT_EVENTS.tsv",events,["condition","mode","attempt","tag","frame","pc","regs_pc","a0","a1","ra","v0"])
 counts=Counter((e["condition"],e["mode"],e["tag"],e["pc"]) for e in events)
 count_rows=[]
 for cond in ("C","A"):
  for mode in ("K0","K2"):
   if mode=="K0":
    for tag,pc in BP.items():count_rows.append({"condition":cond,"mode":mode,"tag":tag,"pc":f"0x{pc:08X}","hits":"NOT_MONITORED_BREAKPOINTS_OFF"})
   else:
    for tag,pc in BP.items():count_rows.append({"condition":cond,"mode":mode,"tag":tag,"pc":f"0x{pc:08X}","hits":sum(v for (c,m,t,p),v in counts.items() if c==cond and m==mode and t==tag and p==f"0x{pc:08X}")})
    ret=sum(v for (c,m,t,p),v in counts.items() if c==cond and m==mode and t=="GETTER_RETURN")
    count_rows.append({"condition":cond,"mode":mode,"tag":"GETTER_RETURN","pc":"CALLER_RA_DYNAMIC","hits":ret})
 write_tsv(out/"AT3_HIT_COUNTS.tsv",count_rows)
 maxwall=max((float(x["wall_seconds"]) for x in launches),default=0.0)
 timeout_ok=timeout_s>=2*maxwall
 complete=(len(launches)==8 and len(frames)==24 and all(x["capture_status"]=="PASS" for x in frames)
  and all(x["emulator_exit_code_decimal"]=="0" and x["memory_card_unchanged"]=="TRUE" for x in launches)
  and all(x["circle_press_readback"] in ("PASS","NOT_APPLICABLE") and x["circle_release_readback"] in ("PASS","NOT_APPLICABLE") for x in launches)
  and all(x["breakpoints_armed"] in ("YES","NOT_APPLICABLE") for x in launches) and timeout_ok)
 report=["AT3 — H6 HYBRID; AN2 SCHEDULE A/C; K0/K2; INTERPRETER + DEBUGGER",
  f"H6_SHA256={H6_SHA}","H6_IDENTITY=target checkpoint base + CONTROL top-level protobuf SPU field 6; HYBRID, NOT TARGET-PURE",
  "SCHEDULE_C=NONE; SCHEDULE_A=CIRCLE press post-load GPU Vsync frame 60, release frame 61",
  "MATRIX=conditions C,A x modes K0,K2 x two independent launches = 8 launches",
  "BREAKPOINTS_K2=0x8001387C setter; 0x800138EC getter; 0x800B770C helper entry; one-shot getter return PC records v0 return",
  f"TIMEOUT_PER_LAUNCH_SECONDS={timeout_s}",f"OBSERVED_MAX_WALL_SECONDS={maxwall:.3f}",
  f"TIMEOUT_GE_2X_OBSERVED_MAX={timeout_ok}",f"RUNTIME_CAPTURE_COMPLETE={complete}",
  "Zero hits only means no execution at monitored PC in the observed window; it is not proof a routine is unused."]
 for x in launches:report.append(f"{x['condition']}/{x['mode']}#{x['attempt']} EXIT={x['emulator_exit_code_decimal']} WALL={x['wall_seconds']} MCD_UNCHANGED={x['memory_card_unchanged']} BP={x['breakpoints_armed']} CIRCLE_PRESS={x['circle_press_readback']} CIRCLE_RELEASE={x['circle_release_readback']}")
 for x in count_rows:report.append(f"HITS {x['condition']}/{x['mode']} {x['tag']} PC={x['pc']} COUNT={x['hits']}")
 (out/"AT3_SUMMARY.txt").write_text("\n".join(report)+"\n",encoding="utf-8")
 rc=0 if complete else 2
 (out/"ACTIONS_RUN_SUMMARY.txt").write_text("\n".join([f"STATUS={'PASS' if complete else 'INCOMPLETE'}","JOB=at3-an2-schedule-k0-k2",
  f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",
  f"H6_SHA256={H6_SHA}",f"EXIT_CODE={rc}",f"TIMEOUT_PER_LAUNCH_SECONDS={timeout_s}",
  f"TIMEOUT_GE_2X_OBSERVED_MAX={timeout_ok}"])+"\n",encoding="utf-8")
 return rc
if __name__=="__main__":raise SystemExit(main())
