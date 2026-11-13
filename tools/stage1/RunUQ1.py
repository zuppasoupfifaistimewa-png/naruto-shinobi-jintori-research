#!/usr/bin/env python3
"""UQ1: two no-input PCSX-Redux replays with selector-record write watchpoints."""
from __future__ import annotations
import argparse
import csv
import hashlib
import os
import shutil
import subprocess
import time
from pathlib import Path

CHECKPOINT_SHA="705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35"
CHECKPOINT_BYTES=21162799
CARD_SHA="78b6d4ac9ab4d23caf7e5f04f83539bf5d994cccfb0a709d14ac53d05c8e21ef"
CARD_BYTES=131072
STRIDE=0x124
STAGES=(88,300,600)
WATCH_FIELDS=((0x0B,1,"selector_byte"),(0x20,2,"selector_halfword"))
EXEC_FIXED=(0x800B770C,0x800FB5A0)
EXEC_FIELDS=["launch","frame","role","pc","a0","a1","a2","a3","ra","v0","v1","runtime_P","record_index","record_address"]
WRITE_FIELDS=["launch","frame","pc","record_index","record_address","field_offset","field_name","access_width",
 "old_shadow","callback_sample","next_tick_sample","v0","a0","a1","a2","a3","ra","sample_timing"]
LAUNCH_FIELDS=["launch","status","exit_code","frames_requested","frames_observed","exec_hits","write_hits",
 "exec_bp_expected","exec_bp_registered","write_bp_expected","write_bp_registered","stage_88","stage_300","stage_600",
 "checkpoint_before","checkpoint_after","launch_checkpoint_before","launch_checkpoint_after",
 "card_before","card_after","wall_seconds"]
COMPARE_FIELDS=["metric","launch_1","launch_2","same","interpretation"]

def sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda:stream.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def write_tsv(path:Path,fields:list[str],rows:list[dict])->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        writer.writeheader();writer.writerows(rows)

def read_tsv(path:Path)->list[dict]:
    with path.open(encoding="utf-8",newline="") as stream:
        return list(csv.DictReader(stream,delimiter="\t"))

def tail(path:Path,dest:Path,limit:int=160)->None:
    text=path.read_text(encoding="utf-8",errors="replace") if path.exists() else "LOG_FILE_NOT_CREATED"
    dest.write_text("\n".join(text.splitlines()[-limit:])+"\n",encoding="utf-8")

def app_env(appdir:Path,home:Path)->dict:
    env=os.environ.copy()
    env.update({"HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),
      "XDG_DATA_HOME":str(home/".data"),"XDG_RUNTIME_DIR":str(home/"runtime"),
      "DISPLAY":"","LIBGL_ALWAYS_SOFTWARE":"1",
      "LD_LIBRARY_PATH":str(appdir/"usr/lib")+":"+str(appdir/"usr/lib/x86_64-linux-gnu"),
      "QT_PLUGIN_PATH":str(appdir/"usr/plugins"),
      "QT_QPA_PLATFORM_PLUGIN_PATH":str(appdir/"usr/plugins/platforms"),
      "QML2_IMPORT_PATH":str(appdir/"usr/qml")})
    return env

def run_emulator(pcsx:Path,appdir:Path,bios:Path,cue:Path,card:Path,state:Path|None,
                 lua:Path,home:Path,stdout:Path,timeout_s:int)->tuple[int,float]:
    for folder in (home/".config",home/".data",home/"runtime"):
        folder.mkdir(parents=True,exist_ok=True)
    try:(home/"runtime").chmod(0o700)
    except OSError:pass
    command=["timeout","--signal=INT","--kill-after=10s",f"{timeout_s}s",str(pcsx),
      "-noupdate","-no-ui","-debugger","-interpreter","-bios",str(bios),"-iso",str(cue),
      "-memcard1",str(card),"-softgpu","-dofile",str(lua),"-logfile",
      str(stdout.with_suffix(".pcsx.log")),"-run"]
    env=app_env(appdir,home)
    if state is not None:env["UE2_SOURCE_STATE"]=str(state)
    started=time.monotonic()
    with stdout.open("wb") as stream:
        try:rc=subprocess.run(command,cwd=home,env=env,stdout=stream,stderr=subprocess.STDOUT,check=False).returncode
        except Exception as exc:
            rc=255;stream.write(("UQ1_LAUNCH_EXCEPTION="+repr(exc)+"\n").encode())
    return rc,time.monotonic()-started

def parse_consumer_sites(path:Path)->list[int]:
    rows=read_tsv(path)
    priority=[]
    for row in rows:
        call=row.get("call_pc","")
        pc=row.get("consumer_pc","")
        if not pc.startswith("0x"):continue
        rank=0 if call=="0x800FB598" else 1 if call=="0x800CE11C" else 2
        priority.append((rank,int(row.get("step","999") or 999),int(pc,16),call))
    seen=set();result=[]
    for _,_,pc,_ in sorted(priority):
        if pc not in seen:
            seen.add(pc);result.append(pc)
        if len(result)==8:break
    return result

def parse_logs(text:str,launch:str)->tuple[list[dict],list[dict],list[str],int]:
    exec_rows=[];write_rows=[];stages=[];frames=0
    for line in text.splitlines():
        if line.startswith("UQ1_EXEC_HIT\t"):
            p=line.split("\t")
            if len(p)>=14:
                exec_rows.append(dict(zip(EXEC_FIELDS,p[1:15])))
        elif line.startswith("UQ1_WRITE_HIT\t"):
            p=line.split("\t")
            if len(p)>=18:
                write_rows.append(dict(zip(WRITE_FIELDS,p[1:19])))
        elif line.startswith("UQ1_STAGE_REACHED\t"):
            p=line.split("\t")
            if len(p)>=4:stages.append(p[2])
        elif line.startswith("UQ1_FRAME_LIMIT\t"):
            p=line.split("\t")
            if len(p)>=3:
                try:frames=max(frames,int(p[2]))
                except ValueError:pass
    return exec_rows,write_rows,stages,frames

def lua_warmup()->str:
    return r'''
local frame=0
_G.uqWarm=PCSX.Events.createEventListener("GPU::Vsync",function()
 frame=frame+1
 if frame==12 then
  print("UQ1_CARD_WARMUP_FRAMES=12")
  PCSX.nextTick(function() PCSX.quit(0) end)
 end
end)
print("UQ1_CARD_WARMUP_READY=YES")
'''.lstrip()

def lua_probe(launch:str,card:Path,exec_sites:list[int])->str:
    card_s=str(card).replace("\\","\\\\").replace('"','\\"')
    exec_table=",".join("{pc=0x%08X}"%x for x in sorted(set(exec_sites)))
    watches=",".join("{i=%d,o=%d,w=%d,n=%s}"%(i,o,w,'"'+name+'"')
       for i in range(44) for o,w,name in WATCH_FIELDS)
    return r'''
local ffi=require("ffi")
local LAUNCH="'''+launch+r'''"
local CARD_PATH="'''+card_s+r'''"
local BP_SITES={'''+exec_table+r'''}
local WATCH_SPECS={'''+watches+r'''}
local RAM_START=0x80000000
local RAM_END=0x80200000
local MOD=4294967296
local STRIDE=0x124
local mem=PCSX.getMemPtr()
local loaded,started,finished=false,false,false
local post,runtimeP=0,nil
local execHandles,writeHandles={},{}
local shadow={}
local function log(s) print(s);pcall(function()io.stdout:flush()end) end
local function hx(v,w)
 if v==nil then return "TIDAK_TAHU" end
 if w==1 then return string.format("0x%02X",tonumber(v)%256) end
 if w==2 then return string.format("0x%04X",tonumber(v)%65536) end
 return string.format("0x%08X",tonumber(v)%MOD)
end
local function readv(a,w)
 if a==nil then return nil end
 local va=tonumber(a)%MOD
 local phys=va%0x20000000
 if va<RAM_START or va>=RAM_END or va+w>RAM_END or phys+w>0x200000 then return nil end
 local ok,value=pcall(function()
  if w==1 then return tonumber(ffi.cast("const uint8_t *",mem+phys)[0]) end
  if w==2 then return tonumber(ffi.cast("const uint16_t *",mem+phys)[0]) end
  return tonumber(ffi.cast("const uint32_t *",mem+phys)[0])
 end)
 if not ok then return nil end
 return value
end
local function registers()
 local r=PCSX.getRegisters()
 return r,tonumber(r.GPR.r[2])%MOD,tonumber(r.GPR.r[4])%MOD,
   tonumber(r.GPR.r[5])%MOD,tonumber(r.GPR.r[6])%MOD,tonumber(r.GPR.r[7])%MOD,
   tonumber(r.GPR.r[31])%MOD
end
local function record_exec(site)
 local r,v0,a0,a1,a2,a3,ra=registers()
 local pc=tonumber(r.pc)%MOD
 local index="TIDAK_TAHU";local rec="TIDAK_TAHU"
 if runtimeP and a0<64 then
  index=tostring(a0%256)
  rec=hx(runtimeP+(a0%256)*STRIDE)
 end
 log(table.concat({"UQ1_EXEC_HIT",LAUNCH,tostring(post),site.role,hx(pc),hx(a0),hx(a1),hx(a2),hx(a3),
   hx(ra),hx(v0),hx(tonumber(r.GPR.r[3])%MOD),hx(runtimeP),index,rec},"\t"))
 return true
end
local function arm_exec()
 local okCount=0
 for _,site in ipairs(BP_SITES) do
  local selected=site
  local ok,bp=pcall(function()
   return PCSX.addBreakpoint(selected.pc,"Exec",4,"UQ1 exec "..string.format("%08X",selected.pc),
    function(address,width,cause) record_exec(selected);return true end)
  end)
  if ok and bp~=nil then okCount=okCount+1;execHandles[#execHandles+1]=bp
  else log("UQ1_EXEC_BP_ERROR\t"..string.format("0x%08X",selected.pc).."\t"..tostring(bp)) end
 end
 log("UQ1_EXEC_BP_REGISTERED="..tostring(okCount).." expected="..tostring(#BP_SITES).." launch="..LAUNCH)
end
local function record_write(w,address,width,cause)
 local r,v0,a0,a1,a2,a3,ra=registers()
 local pc=tonumber(r.pc)%MOD
 local actualAddress=tonumber(address or w.a)%MOD
 local key=tostring(w.i)..":"..tostring(w.o)
 local old=shadow[key]
 local sample=readv(w.a,w.w)
 local eventFrame=post
 local function finish_sample()
  local after=readv(w.a,w.w)
  local line={"UQ1_WRITE_HIT",LAUNCH,tostring(eventFrame),hx(pc),tostring(w.i),
    hx(runtimeP+w.i*STRIDE),string.format("0x%02X",w.o),w.n,tostring(w.w),
    hx(old,w.w),hx(sample,w.w),hx(after,w.w),hx(v0),hx(a0),hx(a1),hx(a2),hx(a3),hx(ra),
    "NEXT_TICK_SAMPLE_ORDER_UNVERIFIED"}
  log(table.concat(line,"\t"))
  shadow[key]=after
 end
 local ok=pcall(function()PCSX.nextTick(finish_sample)end)
 if not ok then
  log(table.concat({"UQ1_WRITE_HIT",LAUNCH,tostring(eventFrame),hx(pc),tostring(w.i),
    hx(runtimeP+w.i*STRIDE),string.format("0x%02X",w.o),w.n,tostring(w.w),
    hx(old,w.w),hx(sample,w.w),"TIDAK_TAHU",hx(v0),hx(a0),hx(a1),hx(a2),hx(a3),hx(ra),
    "NEXT_TICK_SCHEDULING_FAILED"},"\t"))
 end
 return true
end
local function arm_writes()
 local count=0
 for _,spec in ipairs(WATCH_SPECS) do
  local selected=spec
  selected.a=runtimeP+selected.i*STRIDE+selected.o
  local initial=readv(selected.a,selected.w)
  shadow[tostring(selected.i)..":"..tostring(selected.o)]=initial
  local ok,bp=pcall(function()
   return PCSX.addBreakpoint(selected.a,"Write",selected.w,
    "UQ1 write "..string.format("%08X",selected.a),
    function(address,width,cause) return record_write(selected,address,width,cause) end)
  end)
  if ok and bp~=nil then count=count+1;writeHandles[#writeHandles+1]=bp
  else log("UQ1_WRITE_BP_ERROR\t"..tostring(selected.i).."\t"..string.format("0x%02X",selected.o).."\t"..tostring(bp)) end
 end
 log("UQ1_WRITE_BP_REGISTERED="..tostring(count).." expected="..tostring(#WATCH_SPECS).." launch="..LAUNCH)
end
_G.uqLoaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
 loaded=true;post=0
 runtimeP=readv(0x8013EA84,4)
 log("UQ1_RUNTIME_P="..hx(runtimeP).." launch="..LAUNCH)
 log("UQ1_SAVE_STATE_LOADED=YES launch="..LAUNCH)
 if not runtimeP or runtimeP<RAM_START or runtimeP+43*STRIDE+0x22>=RAM_END then
  log("UQ1_RUNTIME_RECORD_RANGE_INVALID=YES")
  return
 end
 arm_exec();arm_writes()
end)
_G.uqVsync=PCSX.Events.createEventListener("GPU::Vsync",function()
 if finished then return end
 if not started then
  local f=io.open(CARD_PATH,"rb")
  if not f then return end
  local size=f:seek("end");f:close()
  if size~=131072 then return end
  started=true
  local path=os.getenv("UE2_SOURCE_STATE") or "resume/source.sstate"
  log("UQ1_LOAD_STATE_START launch="..LAUNCH.." path="..path)
  PCSX.pauseEmulator()
  PCSX.nextTick(function()
   local okf,state=pcall(function()return assert(Support.File.open(path))end)
   if not okf or not state then
    log("UQ1_STATE_OPEN_FAIL="..tostring(state));finished=true;PCSX.quit(50);return
   end
   local ok,err=pcall(function()PCSX.loadSaveState(state)end)
   state:close()
   if not ok then
    log("UQ1_STATE_LOAD_FAIL="..tostring(err));finished=true;PCSX.quit(51);return
   end
   log("UQ1_LOAD_STATE_CALL_RETURNED=YES launch="..LAUNCH)
   PCSX.resumeEmulator()
  end)
  return
 end
 if not loaded then return end
 post=post+1
 if post==88 or post==300 or post==600 then
  log("UQ1_STAGE_REACHED\t"..LAUNCH.."\t"..tostring(post).."\t"..tostring(#writeHandles))
 end
 if post>=600 then
  log("UQ1_FRAME_LIMIT\t"..LAUNCH.."\t"..tostring(post).."\t"..tostring(#writeHandles))
  finished=true
  PCSX.nextTick(function()PCSX.quit(0)end)
 end
end)
log("UQ1_SCRIPT_READY launch="..LAUNCH.." frame_limit=600 input=NONE ram_writes=NONE; write watchpoints observe only")
'''.lstrip()

def launch_once(name:str,source:Path,template:Path,work:Path,out:Path,pcsx:Path,appdir:Path,
                bios:Path,cue:Path,exec_sites:list[int],timeout_s:int)->tuple[dict,list[dict],list[dict]]:
    folder=work/name.lower();folder.mkdir(parents=True,exist_ok=True)
    state=folder/"source.sstate";shutil.copyfile(source,state);state.chmod(0o444)
    card=folder/"memory-card.mcd";shutil.copyfile(template,card);card.chmod(0o444)
    lua=folder/"uq1-write-watchpoints.lua"
    lua.write_text(lua_probe(name,card,exec_sites),encoding="utf-8")
    stdout=folder/"emulator.stdout.txt";home=folder/"home"
    start=f"STAGE_START\t{name}\tframes=88,300,600\tcheckpoint={CHECKPOINT_SHA}\tinput=NONE\n"
    with (out/"UQ1_STAGE_MARKERS.txt").open("a",encoding="utf-8") as stream:
        stream.write(start);stream.flush()
    (out/f"UQ1_{name}_STAGE_START.txt").write_text(start,encoding="utf-8")
    before_source=sha(source);before_state=sha(state);before_card=sha(card)
    rc,wall=run_emulator(pcsx,appdir,bios,cue,card,state,lua,home,stdout,timeout_s)
    textlog=stdout.read_text(encoding="utf-8",errors="replace") if stdout.exists() else ""
    pcx=stdout.with_suffix(".pcsx.log")
    if pcx.exists():textlog+="\n"+pcx.read_text(encoding="utf-8",errors="replace")
    exec_rows,write_rows,stages,frames=parse_logs(textlog,name)
    after_state=sha(state) if state.exists() else "TIDAK TAHU"
    after_source=sha(source) if source.exists() else "TIDAK TAHU"
    after_card=sha(card) if card.exists() else "TIDAK TAHU"
    exec_reg=int(next((x.split("=")[1].split()[0] for x in textlog.splitlines() if x.startswith("UQ1_EXEC_BP_REGISTERED=")),"0"))
    write_reg=int(next((x.split("=")[1].split()[0] for x in textlog.splitlines() if x.startswith("UQ1_WRITE_BP_REGISTERED=")),"0"))
    complete=(rc==0 and frames==600 and set(stages)=={"88","300","600"} and
      exec_reg==len(exec_sites) and write_reg==88 and before_source==after_source==CHECKPOINT_SHA and
      before_state==after_state==CHECKPOINT_SHA and before_card==after_card==CARD_SHA)
    row={"launch":name,"status":"PASS" if complete else "PARTIAL","exit_code":rc,
      "frames_requested":600,"frames_observed":frames,"exec_hits":len(exec_rows),"write_hits":len(write_rows),
      "exec_bp_expected":len(exec_sites),"exec_bp_registered":exec_reg,"write_bp_expected":88,
      "write_bp_registered":write_reg,"stage_88":"YES" if "88" in stages else "NO",
      "stage_300":"YES" if "300" in stages else "NO","stage_600":"YES" if "600" in stages else "NO",
      "checkpoint_before":before_source,"checkpoint_after":after_source,
      "launch_checkpoint_before":before_state,"launch_checkpoint_after":after_state,
      "card_before":before_card,"card_after":after_card,"wall_seconds":f"{wall:.3f}"}
    marker=f"STAGE_DONE\t{name}\texit={rc}\tframes={frames}\texec_hits={len(exec_rows)}\twrite_hits={len(write_rows)}\n"
    with (out/"UQ1_STAGE_MARKERS.txt").open("a",encoding="utf-8") as stream:
        stream.write(marker);stream.flush()
    (out/f"UQ1_{name}_STAGE_DONE.txt").write_text(marker,encoding="utf-8")
    tail(stdout,out/f"UQ1_{name}_STDOUT_TAIL.txt")
    tail(pcx,out/f"UQ1_{name}_PCSX_TAIL.txt")
    return row,exec_rows,write_rows

def self_test()->None:
    assert len(WATCH_FIELDS)==2 and len(range(44))*len(WATCH_FIELDS)==88
    assert len(EXEC_FIXED)==2 and 0x124==292
    assert CHECKPOINT_BYTES==21162799 and CARD_BYTES==131072
    print("UQ1_SELF_TEST=PASS write-watch table 44x2, checkpoint/card identities, staged windows")

def main()->int:
    parser=argparse.ArgumentParser()
    for name in ("work","out","pcsx-bin","appdir","bios","cue","source","static-consumers"):
        parser.add_argument("--"+name,type=Path)
    parser.add_argument("--checkpoint-sha256",default=CHECKPOINT_SHA)
    parser.add_argument("--checkpoint-bytes",type=int,default=CHECKPOINT_BYTES)
    parser.add_argument("--timeout-seconds",type=int,default=900)
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    if args.self_test:self_test();return 0
    required=(args.work,args.out,args.pcsx_bin,args.appdir,args.bios,args.cue,args.source,args.static_consumers)
    if not all(required):parser.error("UQ1 requires emulator paths, checkpoint and UQ0 consumer TSV")
    if args.checkpoint_sha256!=CHECKPOINT_SHA or args.checkpoint_bytes!=CHECKPOINT_BYTES:
        parser.error("UQ1 checkpoint identity is fixed")
    source=args.source
    if not source.is_file() or source.stat().st_size!=CHECKPOINT_BYTES or sha(source)!=CHECKPOINT_SHA:
        raise SystemExit("UQ1_CHECKPOINT_IDENTITY_MISMATCH")
    source.chmod(0o444)
    args.work.mkdir(parents=True,exist_ok=True);args.out.mkdir(parents=True,exist_ok=True)
    consumer_sites=parse_consumer_sites(args.static_consumers)
    exec_sites=sorted(set(EXEC_FIXED+tuple(consumer_sites)))
    (args.out/"UQ1_EXEC_SITES.txt").write_text(
      "FIXED_EXEC_SITES="+",".join(f"0x{x:08X}" for x in EXEC_FIXED)+"\n"+
      "UQ0_FIRST_CONSUMER_SITES="+",".join(f"0x{x:08X}" for x in consumer_sites)+"\n"+
      "EXEC_SITES_TOTAL="+str(len(exec_sites))+"\n",encoding="utf-8")
    if not consumer_sites:
        (args.out/"UQ1_SUMMARY.txt").write_text(
          "STATUS=SEBAGIAN\nEVIDENCE=K1\nREASON=UQ0 consumer TSV contains no first-use PCs\nEXIT_CODE=2\n",encoding="utf-8")
        return 2
    cards=args.work/"cards";cards.mkdir(parents=True,exist_ok=True)
    template=cards/"memory-card-template.mcd";template.unlink(missing_ok=True)
    warm=args.work/"card-warmup.lua";warm.write_text(lua_warmup(),encoding="utf-8")
    home=args.work/"card-warmup-home";stdout=args.work/"card-warmup.stdout.txt"
    for folder in (home/".config",home/".data",home/"runtime"):
        folder.mkdir(parents=True,exist_ok=True)
    try:(home/"runtime").chmod(0o700)
    except OSError:pass
    command=["timeout","--signal=INT","--kill-after=10s",f"{args.timeout_seconds}s",str(args.pcsx_bin),
      "-noupdate","-no-ui","-debugger","-interpreter","-bios",str(args.bios),"-iso",str(args.cue),
      "-memcard1",str(template),"-softgpu","-dofile",str(warm),"-logfile",
      str(stdout.with_suffix(".pcsx.log")),"-run"]
    with stdout.open("wb") as stream:
        try:warm_rc=subprocess.run(command,cwd=home,env=app_env(args.appdir,home),
             stdout=stream,stderr=subprocess.STDOUT,check=False).returncode
        except Exception as exc:warm_rc=255;stream.write(repr(exc).encode())
    warm_log=stdout.read_text(encoding="utf-8",errors="replace") if stdout.exists() else ""
    card_hash=sha(template) if template.exists() else "TIDAK TAHU"
    tail(stdout,args.out/"UQ1_CARD_WARMUP_STDOUT_TAIL.txt")
    tail(stdout.with_suffix(".pcsx.log"),args.out/"UQ1_CARD_WARMUP_PCSX_TAIL.txt")
    if not (warm_rc==0 and "UQ1_CARD_WARMUP_FRAMES=12" in warm_log and
            template.exists() and template.stat().st_size==CARD_BYTES and card_hash==CARD_SHA):
        (args.out/"UQ1_SUMMARY.txt").write_text(
          f"STATUS=BELUM\nEVIDENCE=K0\nCARD_WARMUP_EXIT_CODE={warm_rc}\nCARD_SHA256={card_hash}\nEXIT_CODE=2\n",
          encoding="utf-8")
        return 2
    template.chmod(0o444)
    launches=[];all_exec=[];all_writes=[]
    for name in ("LAUNCH_1","LAUNCH_2"):
        row,exec_rows,write_rows=launch_once(name,source,template,args.work,args.out,args.pcsx_bin,
          args.appdir,args.bios,args.cue,exec_sites,args.timeout_seconds)
        launches.append(row);all_exec.extend(exec_rows);all_writes.extend(write_rows)
    write_tsv(args.out/"UQ1_EXEC_HITS.tsv",EXEC_FIELDS,all_exec)
    write_tsv(args.out/"UQ1_WRITE_EVENTS.tsv",WRITE_FIELDS,all_writes)
    write_tsv(args.out/"UQ1_LAUNCHES.tsv",LAUNCH_FIELDS,launches)
    first=[r for r in all_writes if r["launch"]=="LAUNCH_1"]
    second=[r for r in all_writes if r["launch"]=="LAUNCH_2"]
    sig=lambda rows:[tuple(r[k] for k in WRITE_FIELDS[1:]) for r in rows]
    identical=bool(first or second) and sig(first)==sig(second)
    exec_identical=(
      [tuple(r[k] for k in EXEC_FIELDS[1:]) for r in all_exec if r["launch"]=="LAUNCH_1"]==
      [tuple(r[k] for k in EXEC_FIELDS[1:]) for r in all_exec if r["launch"]=="LAUNCH_2"])
    complete=all(x["status"]=="PASS" for x in launches) and identical and exec_identical
    zero_both=len(first)==0 and len(second)==0
    status="TUNTAS" if complete else "SEBAGIAN" if any(x["frames_observed"]>0 or x["exec_hits"]>0 for x in launches) else "BELUM"
    evidence="K5 terbatas: dua replay dari checkpoint yang sama; bukan variasi independen" if complete else "K2-K4 sesuai stage/BP/hash yang lolos" if status=="SEBAGIAN" else "K0-K1"
    summary=["UQ1_TWO_REPLAY_SELECTOR_RECORD_WRITE_WATCH_AUDIT",
      f"STATUS={status}",f"EVIDENCE={evidence}","CHECKPOINT_SHA256="+CHECKPOINT_SHA,
      "MEMORY_CARD_SHA256="+CARD_SHA,"INPUT=NONE","RAM_WRITE_INJECTION=NONE",
      "WATCH_TARGETS=44 records x {u8(+0x0B),u16(+0x20)}",
      "WRITE_BREAKPOINT_KIND=PCSX.addBreakpoint(address,'Write',width); callback sample timing not independently established",
      "WRITE_BP_EXPECTED_PER_LAUNCH=88",
      f"LAUNCH_1_WRITE_BP_REGISTERED={launches[0]['write_bp_registered']}",
      f"LAUNCH_2_WRITE_BP_REGISTERED={launches[1]['write_bp_registered']}",
      f"LAUNCH_1_FRAMES={launches[0]['frames_observed']}",
      f"LAUNCH_2_FRAMES={launches[1]['frames_observed']}",
      f"LAUNCH_1_WRITE_HITS={len(first)}",f"LAUNCH_2_WRITE_HITS={len(second)}",
      f"WRITE_TRACE_IDENTICAL_ROW_BY_ROW={'YES' if identical else 'NO'}",
      f"EXEC_TRACE_IDENTICAL_ROW_BY_ROW={'YES' if exec_identical else 'NO'}",
      "ZERO_WRITE_RESULT="+("0 penulisan dalam 600 frame pada masing-masing replay" if zero_both and all(x["frames_observed"]==600 for x in launches) else "TIDAK"),
      f"LAUNCH_1_CHECKPOINT_BEFORE_AFTER={launches[0]['checkpoint_before']}/{launches[0]['checkpoint_after']}",
      f"LAUNCH_2_CHECKPOINT_BEFORE_AFTER={launches[1]['checkpoint_before']}/{launches[1]['checkpoint_after']}",
      f"LAUNCH_1_CARD_BEFORE_AFTER={launches[0]['card_before']}/{launches[0]['card_after']}",
      f"LAUNCH_2_CARD_BEFORE_AFTER={launches[1]['card_before']}/{launches[1]['card_after']}",
      "OLD_NEW_VALUE_LIMIT=old_shadow from initial/post-write samples; callback_sample and next_tick_sample are reported separately because callback ordering is not independently verified",
      "GAMEPLAY_MEANING=TIDAK TAHU"]
    (args.out/"UQ1_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary),flush=True)
    return 0 if status=="TUNTAS" else 2

if __name__=="__main__":
    raise SystemExit(main())
