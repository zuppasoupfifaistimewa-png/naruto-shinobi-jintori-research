#!/usr/bin/env python3
"""UO1: checkpoint-only, no-input, no-write PCSX read-breakpoint observation."""
from __future__ import annotations
import argparse
import csv
import hashlib
import os
import shutil
import subprocess
import time
from collections import Counter
from pathlib import Path

CHECKPOINT_SHA="705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35"
CHECKPOINT_BYTES=21162799
CARD_SHA="78b6d4ac9ab4d23caf7e5f04f83539bf5d994cccfb0a709d14ac53d05c8e21ef"
CARD_BYTES=131072
RAM_START=0x80000000
RAM_END=0x80200000
STRIDE=0x124
NONTRIVIAL=(1,2,3,4,6,7,8,9,10,12,13,14,15,16,19,20,21)
ZERO_RECORDS=(0,5,11,17,18,22,43)
FIELD_OFFSETS=tuple(range(0x0E,0x20,2))
FORWARD_SITES=(0x800B7794,0x800B77D4,0x800B783C,0x800B7884,0x800B78D0,0x800CE0F4,0x800D0D70)
REGS=("zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra")
EVENT_FIELDS=["launch","mode","frame","pc","address","field_offset","record_index",
              "base_register","base_value","value_read","calculated_address","event_type"]
LAUNCH_FIELDS=["launch","status","exit_code","frames_requested","frames_observed",
               "read_bp_registered","breakpoint_mode","event_hits","checkpoint_before",
               "checkpoint_after","card_before","card_after","card_mode_0444","last_marker",
               "wall_seconds"]
AGG_FIELDS=["launch","mode","pc","field_offset","event_type","hit_count","records_seen","frames_seen"]
COMPARE_FIELDS=["metric","probe","measure_1","measure_2","same","interpretation"]
ZERO_FIELDS=["record_index","prior_snapshot_classification","runtime_watch_status"]

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def write_tsv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        w.writeheader(); w.writerows(rows)

def tail_text(source: Path, destination: Path, limit: int=200) -> int:
    if not source.is_file():
        destination.write_text("LOG_FILE_NOT_CREATED\n",encoding="utf-8")
        return 0
    lines=source.read_text(encoding="utf-8",errors="replace").splitlines()
    keep=lines[-limit:]
    destination.write_text("\n".join(keep)+("\n" if keep else ""),encoding="utf-8")
    return len(keep)

def app_env(appdir: Path, home: Path) -> dict:
    e=os.environ.copy()
    e.update({"HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),
      "XDG_DATA_HOME":str(home/".data"),"XDG_RUNTIME_DIR":str(home/"runtime"),
      "DISPLAY":"","LIBGL_ALWAYS_SOFTWARE":"1",
      "LD_LIBRARY_PATH":str(appdir/"usr/lib")+":"+str(appdir/"usr/lib/x86_64-linux-gnu"),
      "QT_PLUGIN_PATH":str(appdir/"usr/plugins"),
      "QT_QPA_PLATFORM_PLUGIN_PATH":str(appdir/"usr/plugins/platforms"),
      "QML2_IMPORT_PATH":str(appdir/"usr/qml")})
    return e

def run_emulator(pcsx: Path, appdir: Path, bios: Path, cue: Path, card: Path,
                 state: Path|None, lua: Path, home: Path, stdout: Path,
                 timeout_s: int) -> tuple[int,float]:
    for p in (home/".config",home/".data",home/"runtime"):
        p.mkdir(parents=True,exist_ok=True)
    try: (home/"runtime").chmod(0o700)
    except OSError: pass
    cmd=["timeout","--signal=INT","--kill-after=10s",f"{timeout_s}s",
         str(pcsx),"-noupdate","-no-ui","-debugger","-interpreter",
         "-bios",str(bios),"-iso",str(cue),"-memcard1",str(card),
         "-softgpu","-dofile",str(lua),"-logfile",str(stdout.with_suffix(".pcsx.log")),"-run"]
    env=app_env(appdir,home)
    if state is not None:
        env["UE2_SOURCE_STATE"]=str(state)
        env["UB2_SOURCE_STATE"]=str(state)
    t=time.monotonic()
    with stdout.open("wb") as f:
        try:
            p=subprocess.run(cmd,cwd=home,env=env,stdout=f,stderr=subprocess.STDOUT,check=False)
            rc=p.returncode
        except Exception as exc:
            rc=255
            f.write(("UO1_LAUNCH_EXCEPTION="+repr(exc)+"\n").encode())
    return rc,time.monotonic()-t

def lua_warmup() -> str:
    return r'''
local frame=0
_G.uoWarm=PCSX.Events.createEventListener("GPU::Vsync",function()
 frame=frame+1
 if frame==12 then
  print("UO1_CARD_WARMUP_FRAMES=12")
  PCSX.nextTick(function() PCSX.quit(0) end)
 end
end)
print("UO1_CARD_WARMUP_READY=YES")
'''.lstrip()

def lua_probe(launch: str, card: Path, frames: int, records: list[tuple[int,int]],
              readers: dict[int,tuple[int,int,str]], exec_sites: list[tuple[int,int,int,str]],
              max_hits: int=256) -> str:
    card_s=str(card).replace("\\","\\\\").replace('"','\\"')
    reader_lua=[]
    for pc,(ri,disp,name) in sorted(readers.items()):
        reader_lua.append(f"[0x{pc:08X}]={{{ri},{disp},\"{name}\"}}")
    reader_table=",".join(reader_lua)
    watch=[]
    for idx,first in records:
        for off in FIELD_OFFSETS:
            watch.append(f"{{a=0x{first+off:08X},i={idx},o={off}}}")
    watch_table=",".join(watch)
    exec_l=[]
    for pc,ri,disp,name in exec_sites:
        exec_l.append(f"{{pc=0x{pc:08X},r={ri},d={disp},n=\"{name}\"}}")
    exec_table=",".join(exec_l)
    return r'''
local ffi=require("ffi")
local LAUNCH="''' + launch + r'''"
local CARD_PATH="''' + card_s + r'''"
local FRAME_LIMIT=''' + str(frames) + r'''
local MAX_HITS=''' + str(max_hits) + r'''
local MODE="READ"
local READERS={''' + reader_table + r'''}
local WATCHES={''' + watch_table + r'''}
local EXEC_SITES={''' + exec_table + r'''}
local RAM_START=0x80000000
local RAM_END=0x80200000
local MOD=4294967296
local mem=PCSX.getMemPtr()
local loaded,started,post,finished=false,false,0,false
local readEnabled=false
local totalHits=0
local registered,registerError=0,0
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
local function hx(v,w)
 if v==nil then return "TIDAK_TAHU" end
 if w==2 then return string.format("0x%04X",tonumber(v)%65536) end
 return string.format("0x%08X",tonumber(v)%MOD)
end
local function readv(a,w)
 local va=tonumber(a)%MOD
 local phys=va%0x20000000
 if va<RAM_START or va>=RAM_END or va+w>RAM_END or phys+w>0x200000 then return nil,"OUTSIDE_RAM" end
 local ok,v=pcall(function()
  if w==1 then return tonumber(ffi.cast("const uint8_t *",mem+phys)[0]) end
  if w==2 then return tonumber(ffi.cast("const uint16_t *",mem+phys)[0]) end
  return tonumber(ffi.cast("const uint32_t *",mem+phys)[0])
 end)
 if not ok or v==nil then return nil,"READ_ERROR" end
 return v,nil
end
local function file_size(path)
 local ok,f=pcall(function() return io.open(path,"rb") end)
 if not ok or not f then return -1 end
 local ok2,n=pcall(function() return f:seek("end") end); f:close()
 if not ok2 or n==nil then return -1 end
 return tonumber(n)
end
local function record_read(w,address,width,cause)
 if not readEnabled then return false end
 if totalHits>=MAX_HITS then
  log("UO1_HIT_CAP_REACHED launch="..LAUNCH.." cap="..tostring(MAX_HITS))
  return false
 end
 totalHits=totalHits+1
 local r=PCSX.getRegisters()
 local pc=tonumber(r.pc)%MOD
 local meta=READERS[pc]
 local ri=meta and meta[1] or -1
 local disp=meta and meta[2] or -1
 local name=meta and meta[3] or "TIDAK_TAHU"
 local base=(ri>=0 and tonumber(r.GPR.r[ri])) or nil
 local calculated=(base and disp>=0) and ((base+disp)%MOD) or nil
 local v,err=readv(address or w.a,2)
 log(table.concat({"UO1_READ_HIT",LAUNCH,tostring(post),hx(pc),hx(address or w.a),
   string.format("0x%02X",w.o),tostring(w.i),name,hx(base),err or hx(v,2),
   hx(calculated),"READ"}, "\t"))
 return true
end
local function record_exec(s,address,width,cause)
 if totalHits>=MAX_HITS then
  log("UO1_HIT_CAP_REACHED launch="..LAUNCH.." cap="..tostring(MAX_HITS))
  return false
 end
 totalHits=totalHits+1
 local r=PCSX.getRegisters()
 local base=(s.r>=0) and tonumber(r.GPR.r[s.r]) or nil
 local calc=base and ((base+s.d)%MOD) or nil
 local v,err
 if calc then v,err=readv(calc,2) else err="BASE_REGISTER_UNKNOWN" end
 log(table.concat({"UO1_EXEC_HIT",LAUNCH,tostring(post),hx(r.pc),hx(calc),
   string.format("0x%02X",s.d),"-",s.n,hx(base),err or hx(v,2),hx(calc),"EXEC"}, "\t"))
 return true
end
local function arm_exec()
 local okCount=0
 for _,s in ipairs(EXEC_SITES) do
  local ok,bp=pcall(function()
   return PCSX.addBreakpoint(s.pc,"Exec",4,"UO1 fallback exec "..string.format("%08X",s.pc),
     function(address,width,cause) return record_exec(s,address,width,cause) end)
  end)
  if ok and bp~=nil then okCount=okCount+1
  else registerError=registerError+1; log("UO1_EXEC_BP_ERROR\\t"..LAUNCH.."\\t"..string.format("0x%08X",s.pc).."\\t"..tostring(bp)) end
 end
 log("UO1_EXEC_BP_REGISTERED="..tostring(okCount).." launch="..LAUNCH)
end
local function arm_read()
 local failed=false
 for _,w in ipairs(WATCHES) do
  local ok,bp=pcall(function()
   return PCSX.addBreakpoint(w.a,"Read",2,"UO1 read "..string.format("%08X",w.a),
     function(address,width,cause) return record_read(w,address,width,cause) end)
  end)
  if ok and bp~=nil then registered=registered+1
  else
   registerError=registerError+1; failed=true
   log("UO1_READ_BP_ERROR\\t"..LAUNCH.."\\t"..hx(w.a).."\\t"..tostring(bp))
   break
  end
 end
 if failed then
  readEnabled=false
  log("UO1_READ_BP_REGISTERED=NO launch="..LAUNCH.." count="..tostring(registered))
  arm_exec()
  MODE="EXEC_FALLBACK"
 else
  readEnabled=true
  log("UO1_READ_BP_REGISTERED=YES launch="..LAUNCH.." count="..tostring(registered))
 end
end
_G.uoLoaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
 loaded=true; post=0
 log("UO1_SAVE_STATE_LOADED=YES launch="..LAUNCH)
 arm_read()
end)
_G.uoVsync=PCSX.Events.createEventListener("GPU::Vsync",function()
 if finished then return end
 if not started then
  if file_size(CARD_PATH)~=131072 then return end
  started=true
  local path=os.getenv("UE2_SOURCE_STATE") or "resume/source.sstate"
  log("UO1_LOAD_STATE_START launch="..LAUNCH.." path="..path)
  PCSX.pauseEmulator()
  PCSX.nextTick(function()
   local okf,f=pcall(function() return assert(Support.File.open(path)) end)
   if not okf or not f then log("UO1_STATE_OPEN_FAIL="..tostring(f)); finished=true; PCSX.quit(50); return end
   local ok,e=pcall(function() PCSX.loadSaveState(f) end); f:close()
   if not ok then log("UO1_STATE_LOAD_FAIL="..tostring(e)); finished=true; PCSX.quit(51); return end
   log("UO1_LOAD_STATE_CALL_RETURNED=YES launch="..LAUNCH)
   PCSX.resumeEmulator()
  end)
  return
 end
 if not loaded then return end
 post=post+1
 if post>=FRAME_LIMIT then
  log("UO1_STAGE_FRAME_LIMIT=YES launch="..LAUNCH.." frames="..tostring(post).." hits="..tostring(totalHits).." mode="..MODE)
  finished=true
  PCSX.nextTick(function() PCSX.quit(0) end)
 end
end)
log("UO1_SCRIPT_READY launch="..LAUNCH.." frames="..tostring(FRAME_LIMIT).." input=NONE ram_writes=NONE")
'''.lstrip()

def read_static_readers(path: Path):
    readers={}
    with path.open(encoding="utf-8",newline="") as f:
        for r in csv.DictReader(f,delimiter="\t"):
            if r.get("region")!="ENTRY1": continue
            disp=int(r["displacement"],16) if r["displacement"].lower().startswith("0x") else int(r["displacement"],10)
            name=r["base_register"]
            if name=="$sp" or (disp & 1) or r.get("status")=="DIKECUALIKAN":
                continue
            pc=int(r["pc"],16)
            ri=REGS.index(name[1:]) if name.startswith("$") and name[1:] in REGS else -1
            readers[pc]=(ri,disp,name)
    return readers

def parse_events(text: str, launch: str):
    events=[]
    for line in text.splitlines():
        if not (line.startswith("UO1_READ_HIT\t") or line.startswith("UO1_EXEC_HIT\t")):
            continue
        p=line.split("\t")
        if len(p)!=12: continue
        events.append({"launch":p[1],"mode":"READ" if p[0]=="UO1_READ_HIT" else "EXEC_FALLBACK",
          "frame":p[2],"pc":p[3],"address":p[4],"field_offset":p[5],"record_index":p[6],
          "base_register":p[7],"base_value":p[8],"value_read":p[9],
          "calculated_address":p[10],"event_type":p[11]})
    return events

def launch_stage(name: str, frames: int, indexes: tuple[int,...], supported: bool,
                 source: Path, template: Path, work: Path, out: Path,
                 pcsx: Path, appdir: Path, bios: Path, cue: Path,
                 readers: dict, exec_sites: list, timeout_s: int):
    d=work/name.lower(); d.mkdir(parents=True,exist_ok=True)
    state=d/"source.sstate"; shutil.copyfile(source,state); state.chmod(0o444)
    card=d/"memory-card.mcd"; shutil.copyfile(template,card); card.chmod(0o444)
    # P is intentionally read inside Lua after the immutable checkpoint is restored.
    watch_records=[(i,0) for i in indexes]  # addresses are patched by Lua's runtime P below
    lua=lua_probe(name,card,frames,watch_records,readers,exec_sites)
    if name!="PROBE_READ_BP" and not supported:
        lua=lua.replace('local MODE="READ"','local MODE="EXEC_FALLBACK"')
    # Convert placeholder offsets into an expression based on the runtime P; no source binary is modified.
    lua=lua.replace("local WATCHES={"+",".join(f"{{a=0x{0+off:08X},i={idx},o={off}}}" for idx,_ in watch_records for off in FIELD_OFFSETS)+"}",
                    "local WATCHES={} -- replaced by runtime pointer builder")
    # Replace the literal watcher table with runtime addresses from the RAM pointer after restore.
    old='local WATCHES={} -- replaced by runtime pointer builder'
    new="local WATCHES={}"
    watch_builder=r'''local function build_watches()
 local pval=readv(0x8013EA84,4)
 if not pval then return false end
 local p=tonumber(pval)
 if p<RAM_START or p>=RAM_END then return false end
 for _,ix in ipairs({''' + ",".join(str(i) for i in indexes) + r'''}) do
  local first=p+ix*0x124
  if first<RAM_START or first+0x123>=RAM_END then return false end
  for _,off in ipairs({''' + ",".join(str(x) for x in FIELD_OFFSETS) + r'''}) do
   WATCHES[#WATCHES+1]={a=first+off,i=ix,o=off}
  end
 end
 return true
end'''

    lua=lua.replace(old,new)
    lua=lua.replace("local function file_size(path)",watch_builder+"\nlocal function file_size(path)")
    lua=lua.replace('local function arm_read()\n local failed=false',
      'local function arm_read()\n if MODE=="EXEC_FALLBACK" then log("UO1_READ_BP_REGISTERED=NO launch="..LAUNCH.." reason=probe_read_breakpoint_unavailable"); arm_exec(); return end\n local okw=build_watches()\n if not okw then log("UO1_POINTER_OR_WATCH_RANGE_INVALID=YES launch="..LAUNCH); log("UO1_READ_BP_REGISTERED=NO launch="..LAUNCH.." reason=invalid_runtime_P_or_watch_range"); arm_exec(); MODE="EXEC_FALLBACK"; return end\n local failed=false')
    lua_path=d/"uo1-breakpoints.lua"
    lua_path.write_text(lua,encoding="utf-8")
    stdout=d/"emulator.stdout.txt"; home=d/"home"
    before_state=sha(state); before_source=sha(source); before_card=sha(card)
    start="STAGE_START\t"+name+"\tframes="+str(frames)+"\tindices="+",".join(str(x) for x in indexes)+"\n"
    with (out/"UO1_STAGE_MARKERS.txt").open("a",encoding="utf-8") as f: f.write(start); f.flush()
    (out/f"UO1_STAGE_START_{name}.txt").write_text(start,encoding="utf-8")
    rc,wall=run_emulator(pcsx,appdir,bios,cue,card,state,lua_path,home,stdout,timeout_s)
    textlog=stdout.read_text(encoding="utf-8",errors="replace") if stdout.exists() else ""
    pcx=stdout.with_suffix(".pcsx.log")
    if pcx.exists(): textlog += "\n"+pcx.read_text(encoding="utf-8",errors="replace")
    events=parse_events(textlog,name)
    marker=f"STAGE_DONE\t{name}\texit={rc}\tframes={frames}\thits={len(events)}\n"
    with (out/"UO1_STAGE_MARKERS.txt").open("a",encoding="utf-8") as f: f.write(marker); f.flush()
    (out/f"UO1_STAGE_DONE_{name}.txt").write_text(marker,encoding="utf-8")
    tail_text(stdout,out/f"UO1_{name}_STDOUT_TAIL.txt")
    tail_text(pcx,out/f"UO1_{name}_PCSX_TAIL.txt")
    after_state=sha(state) if state.exists() else "TIDAK TAHU"
    after_source=sha(source) if source.exists() else "TIDAK TAHU"
    after_card=sha(card) if card.exists() else "TIDAK TAHU"
    card_mode=card.exists() and (card.stat().st_mode&0o777)==0o444
    status="PASS" if (rc==0 and before_state==after_state==CHECKPOINT_SHA and
       before_source==after_source==CHECKPOINT_SHA and before_card==after_card==CARD_SHA and card_mode and
       ("UO1_STAGE_FRAME_LIMIT=YES" in textlog)) else "FAIL"
    bp_registered="YES" if "UO1_READ_BP_REGISTERED=YES" in textlog else "NO"
    bp_mode="READ" if bp_registered=="YES" else "EXEC_FALLBACK"
    observed=0
    for line in textlog.splitlines():
        if line.startswith("UO1_STAGE_FRAME_LIMIT=YES"):
            try: observed=int(line.split("frames=")[1].split()[0])
            except (ValueError,IndexError): pass
    row={"launch":name,"status":status,"exit_code":rc,"frames_requested":frames,
      "frames_observed":observed,"read_bp_registered":bp_registered,"breakpoint_mode":bp_mode,
      "event_hits":len(events),"checkpoint_before":before_state,"checkpoint_after":after_state,
      "card_before":before_card,"card_after":after_card,"card_mode_0444":"YES" if card_mode else "NO",
      "last_marker":"FRAME_LIMIT" if observed>=frames else "SEE_TAIL","wall_seconds":f"{wall:.3f}"}
    state.unlink(missing_ok=True); card.unlink(missing_ok=True)
    return row,events,textlog

def self_test():
    assert len(NONTRIVIAL)==17 and len(ZERO_RECORDS)==7
    assert FIELD_OFFSETS==(0x0E,0x10,0x12,0x14,0x16,0x18,0x1A,0x1C,0x1E)
    assert 17*len(FIELD_OFFSETS)==153
    e=parse_events("UO1_READ_HIT\tMEASURE_1\t12\t0x800C9990\t0x8013EA9A\t0x10\t1\t$v0\t0x8013EA8A\t0x0023\t0x8013EA9A\tREAD","MEASURE_1")
    assert len(e)==1 and e[0]["frame"]=="12"
    print("UO1_SELF_TEST=PASS indexes=17 halfword_offsets=9 watches=153 probe_frames=60 measure_frames=122")

def main() -> int:
    ap=argparse.ArgumentParser()
    for name in ("work","out","pcsx-bin","appdir","bios","cue","source","static-readers"):
        ap.add_argument("--"+name,type=Path)
    ap.add_argument("--frames",type=int,default=122)
    ap.add_argument("--timeout-seconds",type=int,default=150)
    ap.add_argument("--self-test",action="store_true")
    a=ap.parse_args()
    if a.self_test:
        self_test(); return 0
    if not all((a.work,a.out,a.pcsx_bin,a.appdir,a.bios,a.cue,a.source,a.static_readers)):
        ap.error("runtime paths required")
    if a.frames!=122 or a.timeout_seconds!=150:
        ap.error("bounded UO1 policy is fixed to 122 measured frames and 150 seconds per process")
    work,out=a.work,a.out; work.mkdir(parents=True,exist_ok=True); out.mkdir(parents=True,exist_ok=True)
    source=a.source
    if not source.is_file() or source.stat().st_size!=CHECKPOINT_BYTES or sha(source)!=CHECKPOINT_SHA:
        raise SystemExit("UO1_CHECKPOINT_IDENTITY_MISMATCH")
    source.chmod(0o444); source_before=sha(source)
    readers=read_static_readers(a.static_readers)
    exec_sites=[]
    for pc in FORWARD_SITES:
        r=readers.get(pc)
        if r: exec_sites.append((pc,r[0],r[1],r[2]))
    if not exec_sites:
        raise SystemExit("UO1_NO_STATIC_EXEC_FALLBACK_SITES")
    cards=work/"cards"; cards.mkdir(parents=True,exist_ok=True)
    template=cards/"memory-card-template.mcd"; template.unlink(missing_ok=True)
    warmup=work/"card-warmup.lua"; warmup.write_text(lua_warmup(),encoding="utf-8")
    warm_stdout=work/"card-warmup.stdout.txt"
    warm_mark="STAGE_START\tCARD_WARMUP\tframes=12\n"
    (out/"UO1_STAGE_MARKERS.txt").write_text(warm_mark,encoding="utf-8")
    (out/"UO1_STAGE_START_CARD_WARMUP.txt").write_text(warm_mark,encoding="utf-8")
    warm_rc,warm_wall=run_emulator(a.pcsx_bin,a.appdir,a.bios,a.cue,template,None,warmup,
                                   work/"card-warmup-home",warm_stdout,a.timeout_seconds)
    warmlog=warm_stdout.read_text(encoding="utf-8",errors="replace") if warm_stdout.exists() else ""
    template_hash=sha(template) if template.exists() else "TIDAK TAHU"
    warm_ok=(warm_rc==0 and "UO1_CARD_WARMUP_FRAMES=12" in warmlog and
             template.exists() and template.stat().st_size==CARD_BYTES and template_hash==CARD_SHA)
    tail_text(warm_stdout,out/"UO1_CARD_WARMUP_STDOUT_TAIL.txt")
    tail_text(warm_stdout.with_suffix(".pcsx.log"),out/"UO1_CARD_WARMUP_PCSX_TAIL.txt")
    warm_done=f"STAGE_DONE\tCARD_WARMUP\texit={warm_rc}\tcard_sha={template_hash}\n"
    with (out/"UO1_STAGE_MARKERS.txt").open("a",encoding="utf-8") as f: f.write(warm_done)
    (out/"UO1_STAGE_DONE_CARD_WARMUP.txt").write_text(warm_done,encoding="utf-8")
    if not warm_ok:
        (out/"UO1_SUMMARY.txt").write_text(
          "STATUS=BELUM\nEVIDENCE=K0\nREASON=Memory Card warmup failed or hash mismatch\n"+
          f"CARD_WARMUP_EXIT_CODE={warm_rc}\nCARD_SHA256={template_hash}\n"+
          f"CHECKPOINT_SOURCE_SHA256={source_before}\nEXIT_CODE=2\n",encoding="utf-8")
        return 2
    template.chmod(0o444)
    # Probe first: one populated record, nine halfword read breakpoints, 60 post-load frames.
    probe_row,probe_events,_probe_log=launch_stage("PROBE_READ_BP",60,(1,),False,source,template,
      work,out,a.pcsx_bin,a.appdir,a.bios,a.cue,readers,exec_sites,a.timeout_seconds)
    read_supported=(probe_row["read_bp_registered"]=="YES" and
                    any(e["event_type"]=="READ" for e in probe_events))
    # Exactly two separately marked no-input measured launches follow the probe.
    launch_rows=[]; all_events=list(probe_events)
    for name in ("MEASURE_1","MEASURE_2"):
        row,events,_logtxt=launch_stage(name,a.frames,NONTRIVIAL,read_supported,source,template,
          work,out,a.pcsx_bin,a.appdir,a.bios,a.cue,readers,exec_sites,a.timeout_seconds)
        launch_rows.append(row); all_events.extend(events)
    write_tsv(out/"UO1_READ_EVENTS.tsv",EVENT_FIELDS,all_events)
    agg=Counter()
    recs={}
    frames={}
    for e in all_events:
        key=(e["launch"],e["mode"],e["pc"],e["field_offset"],e["event_type"])
        agg[key]+=1
        recs.setdefault(key,set()).add(e["record_index"])
        frames.setdefault(key,set()).add(e["frame"])
    agg_rows=[]
    for k,n in sorted(agg.items()):
        agg_rows.append({"launch":k[0],"mode":k[1],"pc":k[2],"field_offset":k[3],
          "event_type":k[4],"hit_count":n,"records_seen":";".join(sorted(recs[k])),
          "frames_seen":";".join(sorted(frames[k],key=lambda x:int(x)))})
    write_tsv(out/"UO1_AGGREGATE.tsv",AGG_FIELDS,agg_rows)
    m1=[e for e in all_events if e["launch"]=="MEASURE_1"]
    m2=[e for e in all_events if e["launch"]=="MEASURE_2"]
    sig=lambda es: sorted((e["mode"],e["frame"],e["pc"],e["address"],e["field_offset"],
                           e["record_index"],e["base_register"],e["base_value"],e["value_read"]) for e in es)
    complete=all(r["status"]=="PASS" for r in launch_rows)
    identical=complete and bool(m1) and bool(m2) and sig(m1)==sig(m2)
    k5="K5" if identical else ("K2" if m1 or m2 else "K0")
    compare=[]
    compare.append({"metric":"READ_BREAKPOINT_API_PROBE_REGISTERED","probe":probe_row["read_bp_registered"],
      "measure_1":launch_rows[0]["read_bp_registered"],"measure_2":launch_rows[1]["read_bp_registered"],
      "same":"YES" if launch_rows[0]["read_bp_registered"]==launch_rows[1]["read_bp_registered"] else "NO",
      "interpretation":"YES = API menerima registrasi; bukan jaminan ada read hit"})
    compare.append({"metric":"MEASURED_TOTAL_HITS","probe":len(probe_events),"measure_1":len(m1),
      "measure_2":len(m2),"same":"YES" if len(m1)==len(m2) else "NO",
      "interpretation":"Banding hit per dua launch"})
    pcs1=sorted({e["pc"] for e in m1}); pcs2=sorted({e["pc"] for e in m2})
    compare.append({"metric":"MEASURED_READER_PC_SET","probe":";".join(sorted({e["pc"] for e in probe_events})),
      "measure_1":";".join(pcs1),"measure_2":";".join(pcs2),
      "same":"YES" if pcs1==pcs2 else "NO","interpretation":"Set PC pembaca yang benar-benar memicu breakpoint"})
    compare.append({"metric":"EVENT_TRACE_IDENTICAL","probe":"N/A","measure_1":len(m1),
      "measure_2":len(m2),"same":"YES" if identical else "NO",
      "interpretation":"K5 hanya untuk dua launch runtime identik yang selesai"})
    write_tsv(out/"UO1_COMPARE.tsv",COMPARE_FIELDS,compare)
    zero_rows=[{"record_index":i,"prior_snapshot_classification":"ZERO/EMPTY in UN1 frame-1 snapshot",
                "runtime_watch_status":"NOT_WATCHED; separated from nontrivial 17"} for i in ZERO_RECORDS]
    write_tsv(out/"UO1_ZERO_RECORDS.tsv",ZERO_FIELDS,zero_rows)
    write_tsv(out/"UO1_LAUNCHES.tsv",LAUNCH_FIELDS,[probe_row]+launch_rows)
    summary=[
      "UO1_CHECKPOINT_READ_BREAKPOINT_OBSERVATION",
      "STATUS="+("TUNTAS" if complete and identical else "SEBAGIAN" if any(r["status"]=="PASS" for r in launch_rows) else "BELUM"),
      "EVIDENCE="+k5,
      "K5_SCOPE=runtime repeatability for exact checkpoint, no-input condition only",
      f"CHECKPOINT_SHA256_EXPECTED={CHECKPOINT_SHA}",
      f"CHECKPOINT_SOURCE_SHA256_BEFORE={source_before}",
      f"CHECKPOINT_SOURCE_SHA256_AFTER={sha(source) if source.exists() else 'TIDAK TAHU'}",
      "CHECKPOINT_MODE=0444; no checkpoint writes",
      f"CARD_SHA256_EXPECTED={CARD_SHA}",f"CARD_WARMUP_SHA256={template_hash}",
      f"CARD_WARMUP_EXIT_CODE={warm_rc}",
      f"CARD_WARMUP_WALL_SECONDS={warm_wall:.3f}",
      f"PROBE_READ_BP_REGISTERED={probe_row['read_bp_registered']}",
      "PROBE_READ_BP_CONFIRMATION="+("CONFIRMED_BY_HIT" if any(e["event_type"]=="READ" for e in probe_events) else "INCONCLUSIVE_NO_HITS_OR_REGISTRATION_FAILED"),
      "PROBE_NO_HITS_POLICY=use EXEC_FALLBACK; API registration alone does not confirm READ breakpoint support",
      "PROBE_FRAMES=60",f"PROBE_EVENT_HITS={len(probe_events)}",
      f"MEASURE_FRAMES={a.frames}",
      "NONTRIVIAL_RECORD_INDICES="+",".join(str(i) for i in NONTRIVIAL),
      "ZERO_RECORD_INDICES="+",".join(str(i) for i in ZERO_RECORDS),
      "WATCH_OFFSETS=0x0E,0x10,0x12,0x14,0x16,0x18,0x1A,0x1C,0x1E",
      f"READ_BREAKPOINTS_PER_MEASURE={len(NONTRIVIAL)*len(FIELD_OFFSETS)}",
      f"MEASURE_1_STATUS={launch_rows[0]['status']}",
      f"MEASURE_1_EXIT_CODE={launch_rows[0]['exit_code']}",
      f"MEASURE_1_HITS={len(m1)}",
      f"MEASURE_2_STATUS={launch_rows[1]['status']}",
      f"MEASURE_2_EXIT_CODE={launch_rows[1]['exit_code']}",
      f"MEASURE_2_HITS={len(m2)}",
      f"MEASURE_READER_PC_SET_IDENTICAL={'YES' if pcs1==pcs2 else 'NO'}",
      f"MEASURE_EVENT_TRACE_IDENTICAL={'YES' if identical else 'NO'}",
      f"BREAKPOINT_MODE={'READ' if read_supported else 'EXEC_FALLBACK'}",
      "FALLBACK_LIMIT=exec breakpoint records register base/effective address; it does not prove memory read",
      "INPUT=NONE",
      "RAM_WRITE_INJECTION=NONE",
      "RAW_RAM_DUMP=NONE",
      "STAGE_MARKERS=UO1_STAGE_MARKERS.txt",
      "FIELD_MEANING=TIDAK TAHU",
      "EXIT_CODE=0" if complete and identical else "EXIT_CODE=2",
    ]
    (out/"UO1_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary),flush=True)
    return 0 if complete and identical else 2

if __name__=="__main__":
    raise SystemExit(main())
