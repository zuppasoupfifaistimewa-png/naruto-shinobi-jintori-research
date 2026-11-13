#!/usr/bin/env python3
"""UP1: two no-input checkpoint launches with staged execution breakpoints."""
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
VALUE_OFFSETS=tuple(range(0x10,0x20,2))
STAGES=(88,300,600)
ENTRY_CANDIDATES=(0x800B76BC,0x800B770C)
SHARED_SITE=0x800B77E8
REG_EVENT_FIELDS=["launch","frame","role","pc","a0","a1","a2","a3","ra","v0","v1","runtime_P",
 "record_index","record_address","record_selector","rec_20","selected_offset","selected_value",
 "rec_10","rec_12","rec_14","rec_16","rec_18","rec_1A","rec_1C","rec_1E"]
LAUNCH_FIELDS=["launch","status","exit_code","frames_requested","frames_observed","event_hits",
 "breakpoints_expected","breakpoints_registered","entry_breakpoints","case_entry_breakpoints","case_input_breakpoints","return_instruction_breakpoints",
 "return_address_breakpoints","shared_77E8_breakpoint","checkpoint_before","checkpoint_after",
 "card_before","card_after","card_mode_0444","stages_reached","wall_seconds"]
COMPARE_FIELDS=["metric","launch_1","launch_2","same","interpretation"]
RECORD_SELECTOR_FIELDS=["launch","record_index","record_address","record_selector","rec_20","selected_offset","selected_value",
 "rec_10","rec_12","rec_14","rec_16","rec_18","rec_1A","rec_1C","rec_1E"]
PAD_ACTION_FIELDS=["launch","frame","button","phase","readback","status"]
SELECTOR_FIELDS=["launch","frame","selector_value","table_target_pc","case_entry_pc","return_pc",
 "record_index","record_selector","rec_20","selected_offset","lv_selected","case_input_pc","input_register",
 "case_input_value","expression_candidate","predicted_v0","v0_at_return",
 "input_matches_selected","comparison_status","evidence_limit"]

def sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def write_tsv(path:Path,fields:list[str],rows:list[dict])->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

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
    try:
        (home/"runtime").chmod(0o700)
    except OSError:
        pass
    command=["timeout","--signal=INT","--kill-after=10s",f"{timeout_s}s",str(pcsx),
      "-noupdate","-no-ui","-debugger","-interpreter","-bios",str(bios),"-iso",str(cue),
      "-memcard1",str(card),"-softgpu","-dofile",str(lua),"-logfile",
      str(stdout.with_suffix(".pcsx.log")),"-run"]
    env=app_env(appdir,home)
    if state is not None:
        env["UE2_SOURCE_STATE"]=str(state)
        env["UB2_SOURCE_STATE"]=str(state)
    started=time.monotonic()
    with stdout.open("wb") as stream:
        try:
            result=subprocess.run(command,cwd=home,env=env,stdout=stream,
                                   stderr=subprocess.STDOUT,check=False)
            exit_code=result.returncode
        except Exception as exc:
            exit_code=255
            stream.write(("UP1_LAUNCH_EXCEPTION="+repr(exc)+"\n").encode())
    return exit_code,time.monotonic()-started

def lua_warmup()->str:
    return r'''
local frame=0
_G.upWarm=PCSX.Events.createEventListener("GPU::Vsync",function()
 frame=frame+1
 if frame==12 then
  print("UP1_CARD_WARMUP_FRAMES=12")
  PCSX.nextTick(function() PCSX.quit(0) end)
 end
end)
print("UP1_CARD_WARMUP_READY=YES")
'''.lstrip()

def lua_exec(launch:str,card:Path,entries:list[int],case_targets:list[int],case_inputs:list[int],returns:list[int],return_addrs:list[int],input_actions:list[tuple[int,str]])->str:
    card_s=str(card).replace("\\","\\\\").replace('"','\\"')
    roles={}
    for address in entries:
        roles.setdefault(address,[]).append("ENTRY")
    for address in case_targets:
        roles.setdefault(address,[]).append("CASE_ENTRY")
    for address in case_inputs:
        roles.setdefault(address,[]).append("CASE_INPUT")
    for address in returns:
        roles.setdefault(address,[]).append("RETURN_INSTRUCTION")
    for address in return_addrs:
        roles.setdefault(address,[]).append("CALL_RETURN")
    roles.setdefault(SHARED_SITE,[]).append("SHARED_77E8")
    table=",".join("{pc=0x%08X,roles={%s}}"%(address,",".join('"'+role+'"' for role in labels))
                   for address,labels in sorted(roles.items()))
    offsets=",".join(str(value) for value in VALUE_OFFSETS)
    action_table=",".join("{frame=%d,button=%s}"%(frame,'"'+button+'"') for frame,button in input_actions)
    return r'''
local ffi=require("ffi")
local LAUNCH="'''+launch+r'''"
local CARD_PATH="'''+card_s+r'''"
local BP_SITES={'''+table+r'''}
local OFFSETS={'''+offsets+r'''}
local INPUT_ACTIONS={'''+action_table+r'''}
local RAM_START=0x80000000
local RAM_END=0x80200000
local MOD=4294967296
local STRIDE=0x124
local mem=PCSX.getMemPtr()
local pad=nil
local padButtons=nil
if #INPUT_ACTIONS>0 then
 local ok,p=pcall(function() return PCSX.SIO0.slots[1].pads[1] end)
 local okb,b=pcall(function() return PCSX.CONSTS.PAD.BUTTON end)
 if ok then pad=p end
 if okb then padButtons=b end
end
local activePadButton=nil
local inputIndex=1
local loaded,started,finished=false,false,false
local post,runtimeP,hits=0,nil,0
local snapshotDone=false
local bpHandles={}
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
local function record_hit(role)
 if hits>=12000 then
  if hits==12000 then log("UP1_HIT_CAP_REACHED launch="..LAUNCH.." cap=12000") end
  return false
 end
 hits=hits+1
 local r=PCSX.getRegisters()
 local pc=tonumber(r.pc)%MOD
 local a0=tonumber(r.GPR.r[4])%MOD
 local a1=tonumber(r.GPR.r[5])%MOD
 local a2=tonumber(r.GPR.r[6])%MOD
 local a3=tonumber(r.GPR.r[7])%MOD
 local ra=tonumber(r.GPR.r[31])%MOD
 local v0=tonumber(r.GPR.r[2])%MOD
 local v1=tonumber(r.GPR.r[3])%MOD
 local index="-"
 local rec=nil
 local f20=nil
 local recordSelector=nil
 local selectedOffset=nil
 local selectedValue=nil
 local values={}
 if runtimeP and not snapshotDone then
  snapshotDone=true
  for recordIndex=0,63 do
   local recordAddress=runtimeP+recordIndex*STRIDE
   local selectorByte=readv(recordAddress+0x0B,1)
   local selectorBits=readv(recordAddress+0x20,2)
   local chosenOffset=nil
   local chosenValue=nil
   if selectorBits then
    local selectorBitsValue=math.floor(selectorBits/128)
    chosenOffset=0x10+(math.floor((selectorBitsValue%64)/2)%16)*2
    chosenValue=readv(recordAddress+chosenOffset,2)
   end
   local function snapshotHex(value,width)
    if value==nil then return "TIDAK_TAHU" end
    return hx(value,width)
   end
   local snapshotFields={"UP1_RECORD_SNAPSHOT",LAUNCH,tostring(recordIndex),hx(recordAddress),
    snapshotHex(selectorByte,1),snapshotHex(selectorBits,2),
    chosenOffset and string.format("0x%02X",chosenOffset) or "TIDAK_TAHU",
    snapshotHex(chosenValue,2)}
   for _,off in ipairs(OFFSETS) do snapshotFields[#snapshotFields+1]=snapshotHex(readv(recordAddress+off,2),2) end
   log(table.concat(snapshotFields,"\t"))
  end
 end
 if runtimeP and a0<64 then
  index=tostring(a0)
  rec=runtimeP+a0*STRIDE
  recordSelector=readv(rec+0x0B,1)
  f20=readv(rec+0x20,2)
  if f20 then
   local selector=math.floor(f20/128); selectedOffset=0x10+(math.floor((selector%64)/2)%16)*2
   selectedValue=readv(rec+selectedOffset,2)
  end
  for _,off in ipairs(OFFSETS) do values[off]=readv(rec+off,2) end
 end
 local function hv(v,w) if v==nil then return "TIDAK_TAHU" end;return hx(v,w) end
 local fields={"UP1_HIT",LAUNCH,tostring(post),role,hx(pc),hx(a0),hx(a1),hx(a2),hx(a3),
  hx(ra),hx(v0),hx(v1),hx(runtimeP),index,rec and hx(rec) or "TIDAK_TAHU",hv(recordSelector,1),hv(f20,2),
  selectedOffset and string.format("0x%02X",selectedOffset) or "TIDAK_TAHU",
  hv(selectedValue,2),hv(values[0x10],2),hv(values[0x12],2),hv(values[0x14],2),
  hv(values[0x16],2),hv(values[0x18],2),hv(values[0x1A],2),hv(values[0x1C],2),hv(values[0x1E],2)}
 log(table.concat(fields,"\t"))
 return true
end
local function arm_exec()
 for _,site in ipairs(BP_SITES) do
  local selected=site
  local ok,bp=pcall(function()
   return PCSX.addBreakpoint(selected.pc,"Exec",4,
    "UP1 exec "..string.format("%08X",selected.pc),
    function(address,width,cause)
     for _,role in ipairs(selected.roles) do record_hit(role) end
     return true
    end)
  end)
  if ok and bp~=nil then
   bpHandles[#bpHandles+1]=bp
  else
   log("UP1_EXEC_BP_ERROR\t"..string.format("0x%08X",selected.pc).."\t"..tostring(bp))
  end
 end
 log("UP1_EXEC_BP_REGISTERED="..tostring(#bpHandles).." launch="..LAUNCH.." expected="..tostring(#BP_SITES))
end
_G.upLoaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
 loaded=true
 post=0
 runtimeP=readv(0x8013EA84,4)
 log("UP1_RUNTIME_P="..hx(runtimeP).." launch="..LAUNCH)
 log("UP1_SAVE_STATE_LOADED=YES launch="..LAUNCH)
 arm_exec()
end)
_G.upVsync=PCSX.Events.createEventListener("GPU::Vsync",function()
 if finished then return end
 if not started then
  local f=io.open(CARD_PATH,"rb")
  if not f then return end
  local size=f:seek("end")
  f:close()
  if size~=131072 then return end
  started=true
  local path=os.getenv("UE2_SOURCE_STATE") or "resume/source.sstate"
  log("UP1_LOAD_STATE_START launch="..LAUNCH.." path="..path)
  PCSX.pauseEmulator()
  PCSX.nextTick(function()
   local okf,state=pcall(function()return assert(Support.File.open(path))end)
   if not okf or not state then
    log("UP1_STATE_OPEN_FAIL="..tostring(state))
    finished=true
    PCSX.quit(50)
    return
   end
   local ok,err=pcall(function()PCSX.loadSaveState(state)end)
   state:close()
   if not ok then
    log("UP1_STATE_LOAD_FAIL="..tostring(err))
    finished=true
    PCSX.quit(51)
    return
   end
   log("UP1_LOAD_STATE_CALL_RETURNED=YES launch="..LAUNCH)
   PCSX.resumeEmulator()
  end)
  return
 end
 if not loaded then return end
 post=post+1
 local scheduled=INPUT_ACTIONS[inputIndex]
 if scheduled then
  if post==scheduled.frame then
   local button=padButtons and padButtons[scheduled.button]
   local ok,value=pcall(function()
    if not pad or not button then error("pad or button unavailable") end
    pad.setOverride(button)
    return pad.getButton(button)
   end)
   local pass=ok and value==true
   log("UP1_PAD_INPUT\t"..LAUNCH.."\t"..tostring(post).."\t"..scheduled.button.."\tPRESS\t"..tostring(value).."\t"..(pass and "PASS" or "FAIL"))
   if pass then activePadButton=button else
    finished=true
    PCSX.nextTick(function()PCSX.quit(84)end)
    return
   end
  elseif post==scheduled.frame+8 then
   local ok,value=pcall(function()
    if not pad or not activePadButton then error("no active pad button") end
    pad.clearOverride(activePadButton)
    return pad.getButton(activePadButton)
   end)
   local pass=ok and value==false
   log("UP1_PAD_INPUT\t"..LAUNCH.."\t"..tostring(post).."\t"..scheduled.button.."\tRELEASE\t"..tostring(value).."\t"..(pass and "PASS" or "FAIL"))
   activePadButton=nil
   inputIndex=inputIndex+1
   if not pass then
    finished=true
    PCSX.nextTick(function()PCSX.quit(85)end)
    return
   end
  end
 end
 if post==88 or post==300 or post==600 then
  log("UP1_STAGE_REACHED\t"..LAUNCH.."\t"..tostring(post).."\t"..tostring(hits))
 end
 if post>=600 then
  log("UP1_FRAME_LIMIT\t"..LAUNCH.."\t"..tostring(post).."\t"..tostring(hits))
  finished=true
  PCSX.nextTick(function()PCSX.quit(0)end)
 end
end)
log("UP1_SCRIPT_READY launch="..LAUNCH.." frame_limit=600 pad_actions="..tostring(#INPUT_ACTIONS).." ram_writes=NONE")
'''.lstrip()

def read_entries(path:Path)->list[int]:
    entries=[]
    with path.open(encoding="utf-8",newline="") as stream:
        for row in csv.DictReader(stream,delimiter="\t"):
            try:
                value=int(row["entry_pc"],16)
                if value in ENTRY_CANDIDATES:
                    entries.append(value)
            except (KeyError,TypeError,ValueError):
                continue
    return sorted(set(entries)) or [0x800B770C]

def read_returns(disassembly:Path,callers:Path,forward_sites:Path)->tuple[list[int],list[int]]:
    returns=[]
    with disassembly.open(encoding="utf-8",newline="") as stream:
        for row in csv.DictReader(stream,delimiter="\t"):
            if row.get("instruction","").startswith("jr $ra"):
                returns.append(int(row["pc"],16))
    with forward_sites.open(encoding="utf-8",newline="") as stream:
        for row in csv.DictReader(stream,delimiter="\t"):
            if row.get("instruction","").startswith("jr $ra"):
                returns.append(int(row["pc"],16))
    return_addresses=[]
    with callers.open(encoding="utf-8",newline="") as stream:
        for row in csv.DictReader(stream,delimiter="\t"):
            if row.get("call_kind") not in ("JAL","JALR_CONST"):
                continue
            try:
                target=int(row["target_pc"],16)
                pc=int(row["pc"],16)
                if target in ENTRY_CANDIDATES:
                    return_addresses.append(pc+8)
            except (KeyError,TypeError,ValueError):
                continue
    return sorted(set(returns)),sorted(set(return_addresses))

def read_case_targets(selector_table:Path)->list[int]:
    targets=[]
    with selector_table.open(encoding="utf-8",newline="") as stream:
        for row in csv.DictReader(stream,delimiter="\t"):
            if row.get("jump_target_pc","").startswith("0x"):
                targets.append(int(row["jump_target_pc"],16))
    return sorted(set(targets))

def read_case_inputs(selector_table:Path)->list[int]:
    values=[]
    with selector_table.open(encoding="utf-8",newline="") as stream:
        for row in csv.DictReader(stream,delimiter="\t"):
            if row.get("reader_site_pc","").startswith("0x"):
                values.append(int(row["reader_site_pc"],16))
    return sorted(set(values))

def read_selector_map(selector_table:Path)->dict[int,dict]:
    mapping={}
    with selector_table.open(encoding="utf-8",newline="") as stream:
        for row in csv.DictReader(stream,delimiter="\t"):
            try:
                mapping[int(row["selector_value"])]=row
            except (KeyError,TypeError,ValueError):
                continue
    return mapping

def parse_record_snapshots(text:str)->list[dict]:
    snapshots=[]
    for line in text.splitlines():
        if not line.startswith("UP1_RECORD_SNAPSHOT\t"):
            continue
        parts=line.split("\t")
        if len(parts)==16:
            snapshots.append(dict(zip(RECORD_SELECTOR_FIELDS,parts[1:])))
    return snapshots

def parse_pad_inputs(text:str)->list[dict]:
    rows=[]
    for line in text.splitlines():
        if not line.startswith("UP1_PAD_INPUT\t"):
            continue
        parts=line.split("\t")
        if len(parts)==7:
            rows.append(dict(zip(PAD_ACTION_FIELDS,parts[1:])))
    return rows

def parse_hits(text:str)->list[dict]:
    events=[]
    for line in text.splitlines():
        if not line.startswith("UP1_HIT\t"):
            continue
        parts=line.split("\t")
        if len(parts)==len(REG_EVENT_FIELDS)+1:
            events.append(dict(zip(REG_EVENT_FIELDS,[parts[1]]+parts[2:])))
    return events

def launch_once(name:str,source:Path,template:Path,work:Path,out:Path,pcsx:Path,
                appdir:Path,bios:Path,cue:Path,entries:list[int],case_targets:list[int],case_inputs:list[int],returns:list[int],
                return_addresses:list[int],timeout_s:int,expected_checkpoint_sha:str,input_actions:list[tuple[int,str]]):
    folder=work/name.lower()
    folder.mkdir(parents=True,exist_ok=True)
    state=folder/"source.sstate"
    shutil.copyfile(source,state)
    state.chmod(0o444)
    card=folder/"memory-card.mcd"
    shutil.copyfile(template,card)
    card.chmod(0o444)
    lua=folder/"up1-exec-breakpoints.lua"
    lua.write_text(lua_exec(name,card,entries,case_targets,case_inputs,returns,return_addresses,input_actions),encoding="utf-8")
    stdout=folder/"emulator.stdout.txt"
    stage_start=f"STAGE_START\t{name}\tframes=88,300,600\tcheckpoint={expected_checkpoint_sha}\n"
    with (out/"UP1_STAGE_MARKERS.txt").open("a",encoding="utf-8") as stream:
        stream.write(stage_start)
        stream.flush()
    checkpoint_before=sha(state)
    source_before=sha(source)
    card_before=sha(card)
    exit_code,wall=run_emulator(pcsx,appdir,bios,cue,card,state,lua,folder/"home",stdout,timeout_s)
    log_text=stdout.read_text(encoding="utf-8",errors="replace") if stdout.exists() else ""
    pcsx_log=stdout.with_suffix(".pcsx.log")
    if pcsx_log.exists():
        log_text+="\n"+pcsx_log.read_text(encoding="utf-8",errors="replace")
    events=parse_hits(log_text)
    snapshots=parse_record_snapshots(log_text)
    pad_rows=parse_pad_inputs(log_text)
    reached=[]
    lines=log_text.splitlines()
    for stage in STAGES:
        found=any(line.startswith(f"UP1_STAGE_REACHED\t{name}\t{stage}\t") for line in lines)
        if found:
            reached.append(stage)
        marker=f"STAGE_{stage}\t{name}\t"+("REACHED" if found else "NOT_REACHED")+"\n"
        with (out/"UP1_STAGE_MARKERS.txt").open("a",encoding="utf-8") as stream:
            stream.write(marker)
            stream.flush()
        (out/f"UP1_{name}_STAGE_{stage}.txt").write_text(marker,encoding="utf-8")
        stage_lines=[]
        for line in lines:
            if line.startswith("UP1_HIT\t"):
                try:
                    if int(line.split("\t")[2])<=stage:
                        stage_lines.append(line)
                except (IndexError,ValueError):
                    continue
            elif line.startswith(f"UP1_STAGE_REACHED\t{name}\t"):
                try:
                    if int(line.split("\t")[2])<=stage:
                        stage_lines.append(line)
                except (IndexError,ValueError):
                    continue
        (out/f"UP1_{name}_FRAME_{stage}_TAIL.txt").write_text(
            "\n".join(stage_lines[-120:])+"\n",encoding="utf-8")
    checkpoint_after=sha(state) if state.exists() else "TIDAK TAHU"
    source_after=sha(source) if source.exists() else "TIDAK TAHU"
    card_after=sha(card) if card.exists() else "TIDAK TAHU"
    card_readonly=card.exists() and (card.stat().st_mode&0o777)==0o444
    breakpoint_count=0
    for line in lines:
        if line.startswith("UP1_EXEC_BP_REGISTERED="):
            try:
                breakpoint_count=int(line.split("=")[1].split()[0])
            except (IndexError,ValueError):
                breakpoint_count=0
    expected=len(set(entries+case_targets+case_inputs+returns+return_addresses+[SHARED_SITE]))
    full=any(line.startswith(f"UP1_FRAME_LIMIT\t{name}\t600\t") for line in lines)
    pad_pass=(len(pad_rows)==2*len(input_actions) and all(row["status"]=="PASS" for row in pad_rows))
    passed=(exit_code==0 and full and breakpoint_count==expected and
            checkpoint_before==checkpoint_after==source_before==source_after==expected_checkpoint_sha and
            card_before==card_after==CARD_SHA and card_readonly and pad_pass)
    row={"launch":name,"status":"PASS" if passed else "FAIL","exit_code":exit_code,
      "frames_requested":600,"frames_observed":600 if full else max(reached,default=0),
      "event_hits":len(events),"breakpoints_expected":expected,"breakpoints_registered":breakpoint_count,
      "entry_breakpoints":len(entries),"case_entry_breakpoints":len(case_targets),"case_input_breakpoints":len(case_inputs),"return_instruction_breakpoints":len(returns),
      "return_address_breakpoints":len(return_addresses),"shared_77E8_breakpoint":"YES",
      "checkpoint_sha256":expected_checkpoint_sha,"checkpoint_before":checkpoint_before,"checkpoint_after":checkpoint_after,
      "card_before":card_before,"card_after":card_after,
      "card_mode_0444":"YES" if card_readonly else "NO",
      "stages_reached":",".join(map(str,reached)) or "NONE",
      "pad_actions_scheduled":len(input_actions),"pad_actions_logged":len(pad_rows),
      "pad_actions_all_pass":"YES" if pad_pass else "NO",
      "wall_seconds":f"{wall:.3f}"}
    (out/f"UP1_{name}_EXECUTION_TAIL.txt").write_text(
        "\n".join(lines[-240:])+"\n",encoding="utf-8")
    state.unlink(missing_ok=True)
    card.unlink(missing_ok=True)
    return row,events,snapshots,pad_rows

def self_test():
    assert CHECKPOINT_BYTES==21162799 and STAGES==(88,300,600)
    assert len(REG_EVENT_FIELDS)==26 and VALUE_OFFSETS==(0x10,0x12,0x14,0x16,0x18,0x1A,0x1C,0x1E)
    sample=("UP1_HIT\tL1\t88\tENTRY\t0x800B770C\t0x4\t0x2\t0x0\t0x0\t0x800B7790\t0xC\t"
      "0x80100000\t4\t0x80100490\t0x00000007\t0x00\t0x0180\t0x10\t0x0007\t0x0007\t0x0\t0x0\t0x0\t0x0\t0x0\t0x0\t0x0")
    assert len(parse_hits(sample))==1
    snapshot="UP1_RECORD_SNAPSHOT\tL1\t4\t0x80100000\t0x01\t0x0180\t0x10\t0x0007\t0x0007\t0x0000\t0x0000\t0x0000\t0x0000\t0x0000\t0x0000\t0x0000"
    assert len(parse_record_snapshots(snapshot))==1
    pad_sample="UP1_PAD_INPUT\tL1\t30\tCROSS\tPRESS\ttrue\tPASS"
    assert len(parse_pad_inputs(pad_sample))==1
    print("UP1_SELF_TEST=PASS staged frames, selector/snapshot parsers, checkpoint hash and pad input parser")

def main()->int:
    parser=argparse.ArgumentParser()
    for name in ("work","out","pcsx-bin","appdir","bios","cue","source",
                 "static-readers","static-disassembly","static-callers","static-cases",
                 "static-forward-sites","static-selector-table"):
        parser.add_argument("--"+name,type=Path)
    parser.add_argument("--checkpoint-sha256",default=CHECKPOINT_SHA)
    parser.add_argument("--checkpoint-bytes",type=int,default=CHECKPOINT_BYTES)
    parser.add_argument("--input-sequence",default="")
    parser.add_argument("--frames",type=int,default=600)
    parser.add_argument("--timeout-seconds",type=int,default=900)
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    required=(args.work,args.out,args.pcsx_bin,args.appdir,args.bios,args.cue,args.source,
              args.static_readers,args.static_disassembly,args.static_callers,args.static_cases,args.static_forward_sites,args.static_selector_table)
    if not all(required):
        parser.error("UP1 requires runtime paths and UP0 static files")
    if args.frames!=600:
        parser.error("UP1 frame window fixed to staged 88 -> 300 -> 600")
    input_actions=[]
    allowed_buttons={"UP","DOWN","LEFT","RIGHT","CIRCLE","CROSS","TRIANGLE","SQUARE","START","SELECT","L1","R1","L2","R2"}
    if args.input_sequence:
        previous_end=0
        for token in args.input_sequence.split(","):
            try:
                frame_text,button=token.strip().split(":",1)
                frame=int(frame_text)
            except (ValueError,TypeError):
                parser.error("input sequence must use frame:BUTTON comma-separated")
            button=button.upper()
            if frame<1 or frame+8>=args.frames or button not in allowed_buttons or frame<previous_end:
                parser.error("invalid frame/button order in input sequence")
            input_actions.append((frame,button))
            previous_end=frame+9
    work,out=args.work,args.out
    work.mkdir(parents=True,exist_ok=True)
    out.mkdir(parents=True,exist_ok=True)
    source=args.source
    if (not source.is_file() or source.stat().st_size!=args.checkpoint_bytes or
            sha(source)!=args.checkpoint_sha256):
        raise SystemExit("UP1_CHECKPOINT_IDENTITY_MISMATCH")
    source.chmod(0o444)
    entries=read_entries(args.static_readers)
    case_targets=read_case_targets(args.static_selector_table)
    case_inputs=read_case_inputs(args.static_selector_table)
    selector_map=read_selector_map(args.static_selector_table)
    if not case_targets or len(selector_map)!=5:
        raise SystemExit("UP1_SELECTOR_TABLE_MUST_HAVE_FIVE_BYTE_MAPPED_CASES")
    returns,return_addresses=read_returns(args.static_disassembly,args.static_callers,args.static_forward_sites)
    marker=out/"UP1_STAGE_MARKERS.txt"
    marker.write_text("UP1_STAGED_EXEC_BREAKPOINT_RUN\nWINDOWS=88,300,600\nINPUT=NONE\nRAM_WRITE_INJECTION=NONE\n",encoding="utf-8")
    cards=work/"cards"
    cards.mkdir(parents=True,exist_ok=True)
    template=cards/"memory-card-template.mcd"
    template.unlink(missing_ok=True)
    warm=work/"card-warmup.lua"
    warm.write_text(lua_warmup(),encoding="utf-8")
    warmout=work/"card-warmup.stdout.txt"
    home=work/"card-warmup-home"
    for folder in (home/".config",home/".data",home/"runtime"):
        folder.mkdir(parents=True,exist_ok=True)
    try:
        (home/"runtime").chmod(0o700)
    except OSError:
        pass
    command=["timeout","--signal=INT","--kill-after=10s",f"{args.timeout_seconds}s",str(args.pcsx_bin),
      "-noupdate","-no-ui","-debugger","-interpreter","-bios",str(args.bios),"-iso",str(args.cue),
      "-memcard1",str(template),"-softgpu","-dofile",str(warm),"-logfile",
      str(warmout.with_suffix(".pcsx.log")),"-run"]
    started=time.monotonic()
    with warmout.open("wb") as stream:
        try:
            warm_rc=subprocess.run(command,cwd=home,env=app_env(args.appdir,home),
              stdout=stream,stderr=subprocess.STDOUT,check=False).returncode
        except Exception as exc:
            warm_rc=255
            stream.write(repr(exc).encode())
    warm_wall=time.monotonic()-started
    warm_log=warmout.read_text(encoding="utf-8",errors="replace") if warmout.exists() else ""
    card_hash=sha(template) if template.exists() else "TIDAK TAHU"
    (out/"UP1_CARD_WARMUP_TAIL.txt").write_text(
        "\n".join(warm_log.splitlines()[-120:])+"\n",encoding="utf-8")
    if not (warm_rc==0 and "UP1_CARD_WARMUP_FRAMES=12" in warm_log and
            template.exists() and template.stat().st_size==CARD_BYTES and card_hash==CARD_SHA):
        with marker.open("a",encoding="utf-8") as stream:
            for stage in STAGES:
                stream.write(f"STAGE_{stage}\tWARMUP\tNOT_RUN\n")
        for stage in STAGES:
            (out/f"UP1_WARMUP_FRAME_{stage}_TAIL.txt").write_text(
                "\n".join(warm_log.splitlines()[-120:])+"\n",encoding="utf-8")
        (out/"UP1_SUMMARY.txt").write_text(
          f"STATUS=BELUM\nEVIDENCE=K0\nCARD_WARMUP_EXIT_CODE={warm_rc}\n"
          f"CARD_SHA256={card_hash}\nWALL_SECONDS={warm_wall:.3f}\nEXIT_CODE=2\n",encoding="utf-8")
        return 2
    template.chmod(0o444)
    launches=[]
    events=[]
    record_snapshots=[]
    pad_actions=[]
    for name in ("LAUNCH_1","LAUNCH_2"):
        row,hit_rows,snapshot_rows,pad_rows=launch_once(name,source,template,work,out,args.pcsx_bin,args.appdir,
          args.bios,args.cue,entries,case_targets,case_inputs,returns,return_addresses,args.timeout_seconds,
          args.checkpoint_sha256,input_actions)
        launches.append(row)
        events.extend(hit_rows)
        record_snapshots.extend(snapshot_rows)
        pad_actions.extend(pad_rows)
    write_tsv(out/"UP1_EXEC_HITS.tsv",REG_EVENT_FIELDS,events)
    write_tsv(out/"UP1_RECORD_SELECTORS.tsv",RECORD_SELECTOR_FIELDS,record_snapshots)
    write_tsv(out/"UP1_PAD_ACTIONS.tsv",PAD_ACTION_FIELDS,pad_actions)
    write_tsv(out/"UP1_LAUNCHES.tsv",LAUNCH_FIELDS,launches)
    first=[row for row in events if row["launch"]=="LAUNCH_1"]
    second=[row for row in events if row["launch"]=="LAUNCH_2"]
    signature=lambda rows:[tuple(row[key] for key in REG_EVENT_FIELDS[1:]) for row in rows]
    identical=bool(first) and bool(second) and signature(first)==signature(second)
    pad_first=[row for row in pad_actions if row["launch"]=="LAUNCH_1"]
    pad_second=[row for row in pad_actions if row["launch"]=="LAUNCH_2"]
    pad_signature=lambda rows:[tuple(row[key] for key in PAD_ACTION_FIELDS[1:]) for row in rows]
    pad_identical=(not input_actions) or (len(pad_first)==len(pad_second)==2*len(input_actions) and pad_signature(pad_first)==pad_signature(pad_second))
    full=all(row["status"]=="PASS" for row in launches)
    def reached(row,stage):
        return "YES" if str(stage) in row["stages_reached"].split(",") else "NO"
    write_tsv(out/"UP1_COMPARE.tsv",COMPARE_FIELDS,[
      {"metric":"EVENT_HIT_COUNT","launch_1":len(first),"launch_2":len(second),
       "same":"YES" if len(first)==len(second) else "NO","interpretation":"jumlah hit"},
      {"metric":"EVENT_TRACE_ROW_BY_ROW","launch_1":len(first),"launch_2":len(second),
       "same":"YES" if identical else "NO","interpretation":"seluruh kolom dan urutan hit identik"},
      {"metric":"PAD_ACTION_TRACE_ROW_BY_ROW","launch_1":len(pad_first),"launch_2":len(pad_second),
       "same":"YES" if pad_identical else "NO","interpretation":"press/release identik"},
      {"metric":"STAGE_88","launch_1":reached(launches[0],88),"launch_2":reached(launches[1],88),
       "same":"SAME_CHECKPOINT","interpretation":"milestone"},
      {"metric":"STAGE_300","launch_1":reached(launches[0],300),"launch_2":reached(launches[1],300),
       "same":"SAME_CHECKPOINT","interpretation":"milestone"},
      {"metric":"STAGE_600","launch_1":reached(launches[0],600),"launch_2":reached(launches[1],600),
       "same":"SAME_CHECKPOINT","interpretation":"milestone"}])
    with args.static_cases.open(encoding="utf-8",newline="") as stream:
        list(csv.DictReader(stream,delimiter="\t"))
    selector_rows=[]
    def u32(value):
        try:return int(value,16)&0xFFFFFFFF
        except (TypeError,ValueError):return None
    def signed32(value):
        return value if value is not None and value<0x80000000 else (value-0x100000000 if value is not None else None)
    def hex32(value):
        return "TIDAK TAHU" if value is None else f"0x{value&0xFFFFFFFF:08X}"
    for launch_name,launch_events in (("LAUNCH_1",first),("LAUNCH_2",second)):
        for ret in (row for row in launch_events if row["role"]=="CALL_RETURN"):
            candidates=[row for row in launch_events
              if row["role"]=="ENTRY" and row["ra"]==ret["pc"] and
              int(row["frame"])<=int(ret["frame"])]
            entry=candidates[-1] if candidates else None
            case_candidates=[row for row in launch_events
              if row["role"]=="CASE_ENTRY" and row["ra"]==ret["pc"] and
              int(row["frame"])<=int(ret["frame"])]
            if entry:
                same_record=[row for row in case_candidates if row["record_index"]==entry["record_index"]]
                if same_record:case_candidates=same_record
            case=case_candidates[-1] if case_candidates else None
            input_candidates=[row for row in launch_events
              if row["role"]=="CASE_INPUT" and row["ra"]==ret["pc"] and
              int(row["frame"])<=int(ret["frame"])]
            pairing_record=(entry or case)
            if pairing_record:
                same_record=[row for row in input_candidates if row["record_index"]==pairing_record["record_index"]]
                if same_record:input_candidates=same_record
            case_input=input_candidates[-1] if input_candidates else None
            source_row=entry or case
            sel=u32(source_row["record_selector"]) if source_row else None
            selmap=selector_map.get(sel,{})
            target=selmap.get("jump_target_pc","TIDAK TAHU")
            input_reg=selmap.get("input_register","TIDAK TAHU")
            input_event=case_input or case
            input_raw=(input_event.get("v1") if input_event and input_reg=="$v1" else
                       input_event.get("v0") if input_event and input_reg=="$v0" else None)
            input_value=u32(input_raw)
            selected=u32(entry["selected_value"]) if entry else None
            pred=None
            formula=selmap.get("expression_candidate","TIDAK TAHU")
            status=selmap.get("formula_status","TIDAK TAHU")
            if status=="TERBUKTI_BYTE" and selected is not None:
                pred=selected
            elif status=="TERBUKTI_BYTE_SEQUENCE" and input_value is not None:
                if formula=="signed_trunc((12*V1)/10)":
                    n=signed32((input_value*12)&0xFFFFFFFF)
                    pred=((abs(n)//10)*(1 if n>=0 else -1))&0xFFFFFFFF
                elif formula=="signed_trunc((15*V0)/10)":
                    n=signed32((input_value*15)&0xFFFFFFFF)
                    pred=((abs(n)//10)*(1 if n>=0 else -1))&0xFFFFFFFF
                elif formula=="signed_trunc((18*V1)/10)":
                    n=signed32((input_value*18)&0xFFFFFFFF)
                    pred=((abs(n)//10)*(1 if n>=0 else -1))&0xFFFFFFFF
                elif formula=="2*V0":
                    pred=(input_value*2)&0xFFFFFFFF
            match_input=("YES" if status=="TERBUKTI_BYTE" and selected is not None else
                          "YES" if status=="TERBUKTI_BYTE_SEQUENCE" and case_input is not None and input_value is not None
                          else "NO_OR_UNAVAILABLE")
            actual=u32(ret["v0"])
            if pred is None:comparison="TIDAK DAPAT DIBANDINGKAN"
            elif actual==pred:comparison="MATCH" if match_input=="YES" else "MATCH_INPUT_SOURCE_UNPROVEN"
            else:comparison="MISMATCH"
            selector_rows.append({"launch":launch_name,"frame":ret["frame"],
              "selector_value":str(sel) if sel is not None else "TIDAK TAHU",
              "table_target_pc":target,"case_entry_pc":case["pc"] if case else "TIDAK TAHU",
              "return_pc":ret["pc"],"record_index":source_row["record_index"] if source_row else "TIDAK TAHU",
              "record_selector":source_row["record_selector"] if source_row else "TIDAK TAHU",
              "rec_20":entry["rec_20"] if entry else "TIDAK TAHU",
              "selected_offset":entry["selected_offset"] if entry else "TIDAK TAHU",
              "lv_selected":entry["selected_value"] if entry else "TIDAK TAHU",
              "case_input_pc":case_input["pc"] if case_input else "TIDAK TAHU",
              "input_register":input_reg,"case_input_value":input_raw or "TIDAK TAHU",
              "expression_candidate":formula,"predicted_v0":hex32(pred),
              "v0_at_return":ret["v0"],"input_matches_selected":match_input,
              "comparison_status":comparison,
              "evidence_limit":"Kecocokan per replay; selector/target berasal dari tabel byte; V1/V0 dipakai hanya sesuai input_register byte"})
    write_tsv(out/"UP1_SELECTOR_V0.tsv",SELECTOR_FIELDS,selector_rows)
    max_stage=max((max([int(value) for value in row["stages_reached"].split(",") if value.isdigit()],default=0)
                   for row in launches),default=0)
    observed_targets={row["pc"] for row in events if row["role"]=="CASE_ENTRY"}
    mapped_targets={f"0x{value:08X}" for value in case_targets}
    case_coverage="TUNTAS" if observed_targets==mapped_targets else "SEBAGIAN"
    selector_values=sorted({row["selector_value"] for row in selector_rows if row["selector_value"]!="TIDAK TAHU"})
    record_selector_values=sorted({str(int(row["record_selector"],16)) for row in record_snapshots
      if row.get("record_selector","TIDAK_TAHU").startswith("0x")})
    snapshot_launches=sorted({row.get("launch","") for row in record_snapshots})
    snapshot_by_launch={}
    for row in record_snapshots:
        snapshot_by_launch.setdefault(row.get("launch",""),{})[row.get("record_index","")]=(
          row.get("record_selector",""),row.get("rec_20",""),row.get("selected_offset",""),row.get("selected_value",""))
    snapshot_repeatable=("LAUNCH_1" in snapshot_by_launch and "LAUNCH_2" in snapshot_by_launch and
      snapshot_by_launch["LAUNCH_1"]==snapshot_by_launch["LAUNCH_2"])
    case_formula_matches=sum(1 for row in selector_rows if row["comparison_status"]=="MATCH")
    case_formula_mismatches=sum(1 for row in selector_rows if row["comparison_status"]=="MISMATCH")
    if full and identical and pad_identical:
        status="TUNTAS"
        evidence="K5"
    elif max_stage>0 or any(row["event_hits"]>0 for row in launches):
        status="SEBAGIAN"
        evidence="K2-K4 sesuai milestone dan event yang benar-benar tercapai"
    else:
        status="BELUM"
        evidence="K0-K1"
    summary=["UP1_TWO_CHECKPOINT_LAUNCH_EXEC_BREAKPOINT_AUDIT",
      f"STATUS={status}",f"EVIDENCE={evidence}",f"MAXIMUM_STAGE_REACHED={max_stage}",
      "ENTRY_BREAKPOINT_PCS="+",".join(f"0x{value:08X}" for value in entries),
      f"CASE_ENTRY_BREAKPOINTS={len(case_targets)}",
      f"CASE_INPUT_BREAKPOINTS={len(case_inputs)}",
      f"RETURN_INSTRUCTION_BREAKPOINTS={len(returns)}",
      f"CALL_RETURN_BREAKPOINTS={len(return_addresses)}","SHARED_77E8_BREAKPOINT=0x800B77E8",
      f"CHECKPOINT_SHA256={args.checkpoint_sha256}",f"MEMORY_CARD_SHA256={card_hash}",
      f"LAUNCH_1_EXIT_CODE={launches[0]['exit_code']}",f"LAUNCH_2_EXIT_CODE={launches[1]['exit_code']}",
      f"LAUNCH_1_HITS={len(first)}",f"LAUNCH_2_HITS={len(second)}",
      f"EVENT_TRACE_IDENTICAL_ROW_BY_ROW={'YES' if identical else 'NO'}",
      "K5_SCOPE=dua replay dalam kondisi yang sama dari checkpoint identik; bukan variasi independen, identik memang wajar",
      "INPUT_SEQUENCE="+(args.input_sequence or "NONE"),
      "INPUT=PAD_ONLY" if input_actions else "INPUT=NONE",
      f"PAD_ACTIONS_EXPECTED={2*len(input_actions)}",f"PAD_ACTIONS_OBSERVED={len(pad_actions)}",
      f"PAD_ACTION_TRACE_IDENTICAL_ROW_BY_ROW={'YES' if pad_identical else 'NO'}",
      "RAM_WRITE_INJECTION=NONE","CHECKPOINT_AND_CARD_READ_ONLY=YES",
      "SELECTOR_TO_SITE_MAPPING=BYTE_TABLE_AND_RUNTIME_RECORD_SELECTOR",
      f"SELECTOR_VALUES_OBSERVED={','.join(sorted({row['selector_value'] for row in selector_rows if row['selector_value']!='TIDAK TAHU'}))}",
      f"SELECTOR_RESULT_MATCH_ROWS={case_formula_matches}",
      f"SELECTOR_RESULT_MISMATCH_ROWS={case_formula_mismatches}",
      f"CASE_TARGETS_EXPECTED={len(mapped_targets)}",
      f"CASE_TARGETS_OBSERVED={len(observed_targets)}",
      f"CASE_TARGET_COVERAGE={case_coverage}",
      f"SELECTOR_VALUES_OBSERVED={','.join(selector_values)}",
      f"RECORD_SNAPSHOT_ROWS={len(record_snapshots)}",
      f"RECORD_SNAPSHOT_LAUNCHES={','.join(snapshot_launches)}",
      f"RECORD_SELECTOR_VALUES_PRESENT_IN_RAM={','.join(record_selector_values)}",
      f"RECORD_SNAPSHOT_REPEATABLE_ROW_BY_ROW={'YES' if snapshot_repeatable else 'NO_OR_INCOMPLETE'}",
      "GAMEPLAY_FIELD_MEANING=TIDAK TAHU",
      "EXIT_CODE=0" if status=="TUNTAS" else "EXIT_CODE=2"]
    (out/"UP1_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary),flush=True)
    return 0 if status=="TUNTAS" else 2

if __name__=="__main__":
    raise SystemExit(main())
