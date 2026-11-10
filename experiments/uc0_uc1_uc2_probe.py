#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,shutil,sys,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from experiments.ub2_headless_trace import SOURCE_SHA256,EXPECTED_CARD_BYTES,sha,lua_warmup,pad_exec,run_emulator,read_log_text,write_tsv
FRAME_LIMIT=900
LAUNCHES=("NO_INPUT_1","NO_INPUT_2","CIRCLE_1","CIRCLE_2")
ADDRS=((0x80011A28,"CALLER_80011A28"),(0x800D15A8,"TARGET_800D15A8"),
       (0x800D2520,"TARGET_800D2520"),(0x800D46EC,"TARGET_800D46EC"))

def lua_probe(mode,launch):
    specs=",".join("{"+f"0x{a:08X}"+',"'+name+'"}' for a,name in ADDRS)
    return r'''
local MODE="''' + mode + r'''"
local LAUNCH="''' + launch + r'''"
local FRAME_LIMIT=900
local MOD=4294967296
local loaded,started,post=false,false,0
local handles={}
local counts={}
local callWindow,callCount=0,0
local inputErrors=0
local function hx(x) if x==nil then return "TIDAK TAHU" end return string.format("0x%08X",tonumber(x)%MOD) end
local function log(s) print(s);pcall(function() io.stdout:flush() end) end
local function hit(address,label)
  if label=="CALLER_80011A28" then
    local win=math.floor((post-1)/100)
    if win~=callWindow then callWindow=win;callCount=0 end
    if callCount>=8 then return true end
    callCount=callCount+1
    local r=PCSX.getRegisters();local g=r.GPR
    local z={"UC2_BP",LAUNCH,MODE,tostring(post),label,hx(address),hx(r.pc),hx(g.n.ra),hx(g.n.a0),"WINDOW="..tostring(win),"HIT="..tostring(callCount)}
    for i=0,31 do z[#z+1]="r"..tostring(i).."="..hx(g.r[i]) end
    log(table.concat(z,"\t"))
    if callCount==8 then log("UC2_CAP_REACHED\t"..LAUNCH.."\t"..label.."\t"..tostring(post).."\twindow="..tostring(win)) end
    return true
  end
  local n=counts[label] or 0
  if n>=16 then return true end
  n=n+1;counts[label]=n
  local r=PCSX.getRegisters();local g=r.GPR
  local z={"UC2_BP",LAUNCH,MODE,tostring(post),label,hx(address),hx(r.pc),hx(g.n.ra),hx(g.n.a0),"WINDOW=ALL","HIT="..tostring(n)}
  for i=0,31 do z[#z+1]="r"..tostring(i).."="..hx(g.r[i]) end
  log(table.concat(z,"\t"))
  if n==16 then log("UC2_CAP_REACHED\t"..LAUNCH.."\t"..label.."\t"..tostring(post).."\twindow=ALL") end
  return true
end
local function armAll()
  local specs={''' + specs + r'''}
  local armed=0
  for _,spec in ipairs(specs) do
    local address,label=spec[1],spec[2]
    local ok,h=pcall(function() return PCSX.addBreakpoint(address,"Exec",4,"UD2 "..label,function(a) return hit(a,label) end) end)
    if ok and h~=nil then handles[label]=h;armed=armed+1
    else log("UC2_BREAKPOINT_INSTALL_FAIL\t"..label.."\t"..tostring(h)) end
  end
  log("instrumented="..tostring(armed==4).." armed="..tostring(armed))
  return armed
end
local pad,circle
if MODE=="CIRCLE" then
  PCSX.settings.pads[1].DeviceType="Analog";PCSX.settings.pads[1].Connected=true
  PCSX.SIO0.slots[1].pads[1].map();pad=PCSX.SIO0.slots[1].pads[1]
  circle=PCSX.CONSTS.PAD.BUTTON.CIRCLE;pcall(function() pad.clearOverride(circle) end)
  log("UC2_PAD_READY mode=CIRCLE")
else log("UC2_PAD_READY mode=NO_INPUT overrides=NONE") end
_G.ud2Loaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
  loaded=true;post=0;callWindow=0;callCount=0
  log("UC2_SAVE_STATE_LOADED=1 launch="..LAUNCH)
  local armed=armAll()
  if armed~=4 then PCSX.nextTick(function() PCSX.quit(3) end) end
end)
_G.ud2Vsync=PCSX.Events.createEventListener("GPU::Vsync",function()
  if not started then
    started=true;local path=os.getenv("UB2_SOURCE_STATE") or "resume/source.sstate"
    log("UC2_LOAD_BEGIN=1 path="..path.." mode="..MODE);PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf,f=pcall(function() return assert(Support.File.open(path)) end)
      if not okf or not f then log("UC2_STATE_OPEN_FAIL="..tostring(f));PCSX.quit(50);return end
      local ok,err=pcall(function() PCSX.loadSaveState(f) end);f:close()
      if not ok then log("UC2_STATE_LOAD_FAIL="..tostring(err));PCSX.quit(51);return end
      log("UC2_LOAD_CALL_RETURNED=1");PCSX.resumeEmulator()
    end);return
  end
  if not loaded then return end
  post=post+1
  if MODE=="CIRCLE" then
    if post>=120 and (post-120)%120==0 then
      local ok,v=pcall(function() pad.setOverride(circle);return pad.getButton(circle) end)
      local pass=ok and v==true
      if not pass then inputErrors=inputErrors+1 end
      log("UC2_INPUT\t"..LAUNCH.."\t"..tostring(post).."\tCIRCLE\tPRESS\t"..tostring(v).."\t"..(pass and "PASS" or "FAIL"))
    elseif post>=126 and (post-126)%120==0 then
      local ok,v=pcall(function() pad.clearOverride(circle);return pad.getButton(circle) end)
      local pass=ok and v==false
      if not pass then inputErrors=inputErrors+1 end
      log("UC2_INPUT\t"..LAUNCH.."\t"..tostring(post).."\tCIRCLE\tRELEASE\t"..tostring(v).."\t"..(pass and "PASS" or "FAIL"))
    end
  end
  if post==FRAME_LIMIT then
    log("UC2_FRAME_LIMIT_REACHED launch="..LAUNCH.." frames="..post)
    PCSX.nextTick(function() PCSX.quit(inputErrors==0 and 0 or 2) end)
  end
end)
log("UC2_SCRIPT_READY launch="..LAUNCH.." instrumented=true requested_breakpoints=4 frames=900 read_only=YES")
'''.lstrip()

def parse_log(log):
    events=[];inputs=[];caps=[];armed=[]
    for line in log.splitlines():
        p=[x.strip() for x in line.rstrip("\r\n").split("\t")]
        if p and p[0]=="UC2_BP" and len(p)>=11:
            r={"launch":p[1],"condition":p[2],"frame":p[3],"label":p[4],"address":p[5],"pc":p[6],"ra":p[7],"a0":p[8],"window":p[9].split("=",1)[-1],"hit":p[10].split("=",1)[-1]}
            for item in p[11:]:
                if "=" in item:
                    k,v=item.split("=",1);r[k]=v
            events.append(r)
        elif p and p[0]=="UC2_INPUT" and len(p)>=7:
            inputs.append({"launch":p[1],"frame":p[2],"button":p[3],"action":p[4],"readback":p[5],"status":p[6]})
        elif p and p[0]=="UC2_CAP_REACHED" and len(p)>=5:
            caps.append({"launch":p[1],"label":p[2],"frame":p[3],"window":p[4].split("=",1)[-1]})
        elif line.strip().startswith("instrumented="):
            s=line.strip().split()
            d={x.split("=",1)[0]:x.split("=",1)[1] for x in s if "=" in x}
            armed.append(d)
    return events,inputs,caps,armed

def main():
    ap=argparse.ArgumentParser()
    for k in ("work","out","pcsx-bin","appdir","bios","cue","source","card-dir"):ap.add_argument("--"+k,required=True)
    ap.add_argument("--timeout-seconds",type=int,default=120);a=ap.parse_args()
    work,out=Path(a.work),Path(a.out);out.mkdir(parents=True,exist_ok=True)
    pcsx,appdir,bios,cue,source,carddir=map(Path,(a.pcsx_bin,a.appdir,a.bios,a.cue,a.source,a.card_dir))
    if sha(source)!=SOURCE_SHA256 or source.stat().st_size!=21162799:raise SystemExit("UD2_CHECKPOINT_IDENTITY_FAIL")
    source.chmod(0o444);carddir.mkdir(parents=True,exist_ok=True)
    template=carddir/"memory-card-template.mcd";warm=work/"ud2-warmup.lua";warm.write_text(lua_warmup(),encoding="utf-8")
    warmrc,_,_=run_emulator(pcsx,appdir,bios,cue,template,None,warm,work/"warm-home",work/"warm.stdout.txt",120)
    if not template.is_file() or template.stat().st_size!=EXPECTED_CARD_BYTES:raise SystemExit("UD2_MEMCARD_WARMUP_FAIL")
    cardhash=sha(template);launchrows=[];events=[];inputs=[];caps=[]
    for launch in LAUNCHES:
        mode="CIRCLE" if launch.startswith("CIRCLE") else "NO_INPUT"
        d=work/launch.lower();d.mkdir(parents=True,exist_ok=True)
        state=d/"source.sstate";shutil.copyfile(source,state);state.chmod(0o444)
        card=d/"memory-card.mcd";shutil.copyfile(template,card);cardbefore=sha(card)
        lua=d/"ud2.lua";lua.write_text(lua_probe(mode,launch),encoding="utf-8")
        stdout=d/"emulator.stdout.txt"
        rc,wall,_=run_emulator(pcsx,appdir,bios,cue,card,state,lua,d/"home",stdout,a.timeout_seconds,pad_exec() if mode=="CIRCLE" else None)
        log=read_log_text(stdout);ee,ii,cc,aa=parse_log(log);events+=ee;inputs+=ii;caps+=cc
        (out/("UD2_"+launch+"_EMULATOR_LOG.txt")).write_text("\n".join(log.splitlines()[-180:])+"\n",encoding="utf-8")
        frames=0
        for line in log.splitlines():
            if line.startswith("UC2_FRAME_LIMIT_REACHED"):
                try:frames=int(line.split("frames=",1)[1].split()[0])
                except Exception:pass
        cardafter=sha(card) if card.exists() else "TIDAK TAHU"
        instrumented=any(x.get("instrumented")=="true" and x.get("armed")=="4" for x in aa)
        expected=14 if mode=="CIRCLE" else 0
        valid=(len(ii)==expected and all(x["status"]=="PASS" for x in ii))
        launchrows.append({"launch":launch,"condition":mode,"frames_reached":frames,
          "save_state_loaded":"YES" if "UC2_SAVE_STATE_LOADED=1 launch="+launch in log else "NO",
          "instrumented":"YES" if instrumented else "NO","armed":max([int(x.get("armed","0")) for x in aa] or [0]),
          "breakpoint_hits":len(ee),"input_events":len(ii),"input_expected":expected,
          "input_validation":"PASS" if valid else "FAIL","emulator_exit_code":rc,
          "wall_seconds":f"{wall:.3f}","memory_card_sha256_before":cardbefore,
          "memory_card_sha256_after":cardafter,"memory_card_unchanged":"YES" if cardafter==cardbefore else "NO"})
        state.unlink(missing_ok=True);card.unlink(missing_ok=True)
    write_tsv(out/"UD2_BREAKPOINT_EVENTS.tsv",["launch","condition","frame","label","address","pc","ra","a0","window","hit"]+[f"r{i}" for i in range(32)],events)
    write_tsv(out/"UD2_INPUT_EVENTS.tsv",["launch","frame","button","action","readback","status"],inputs)
    write_tsv(out/"UD2_CAP_EVENTS.tsv",["launch","label","frame","window"],caps)
    write_tsv(out/"UD2_LAUNCHES.tsv",list(launchrows[0].keys()),launchrows)
    counts=[]
    for launch in LAUNCHES:
        for address,label in ADDRS:
            relevant=[x for x in events if x["launch"]==launch and x["label"]==label]
            cap=8 if label=="CALLER_80011A28" else 16
            reached=[x for x in caps if x["launch"]==launch and x["label"]==label]
            counts.append({"launch":launch,"condition":"CIRCLE" if launch.startswith("CIRCLE") else "NO_INPUT",
              "address":hx(address),"label":label,"recorded_hits":len(relevant),"cap_per_window_or_launch":cap,
              "cap_exhausted":"YES" if reached else "NO","first_exhausted_frame":reached[0]["frame"] if reached else "TIDAK TAHU",
              "cap_exhausted_in_first_100_frames":"YES" if reached and int(reached[0]["frame"])<=100 else "NO"})
    write_tsv(out/"UD2_BREAKPOINT_COUNTS.tsv",list(counts[0].keys()),counts)
    a0rows=[]
    for cond in ("NO_INPUT","CIRCLE"):
        for address,label in ADDRS:
            subset=[x for x in events if x["condition"]==cond and x["label"]==label]
            vals=sorted({x["a0"] for x in subset})
            a0rows.append({"condition":cond,"address":hx(address),"label":label,"hits":len(subset),
              "unique_a0_count":len(vals),"a0_values":";".join(vals) if vals else "TIDAK TAHU"})
    write_tsv(out/"UD2_A0_VARIATION.tsv",["condition","address","label","hits","unique_a0_count","a0_values"],a0rows)
    repeat=[]
    for cond in ("NO_INPUT","CIRCLE"):
        l1,l2=(cond+"_1",cond+"_2")
        s1=sorted(tuple(x.get(k,"") for k in ["frame","label","address","pc","ra","a0"]+[f"r{i}" for i in range(32)]) for x in events if x["launch"]==l1)
        s2=sorted(tuple(x.get(k,"") for k in ["frame","label","address","pc","ra","a0"]+[f"r{i}" for i in range(32)]) for x in events if x["launch"]==l2)
        repeat.append({"condition":cond,"launch_1":l1,"launch_2":l2,"events_1":len(s1),"events_2":len(s2),
          "exact_trace_equal":"YES" if s1==s2 and len(s1)>0 else ("EMPTY_BOTH" if not s1 and not s2 else "NO"),
          "K5_scope":"observed nonempty breakpoint trace only" if s1==s2 and len(s1)>0 else "NOT_CLAIMED"})
    write_tsv(out/"UD2_REPEAT_COMPARISON.tsv",list(repeat[0].keys()),repeat)
    complete=all(x["frames_reached"]==FRAME_LIMIT and x["save_state_loaded"]=="YES" and x["instrumented"]=="YES" and
                 x["armed"]==4 and x["emulator_exit_code"]==0 and x["memory_card_unchanged"]=="YES" for x in launchrows)
    inputok=all(x["input_validation"]=="PASS" for x in launchrows)
    instok=all(x["instrumented"]=="YES" and x["armed"]==4 for x in launchrows)
    rc=0 if complete and inputok else (3 if not instok else 2)
    lines=["UD2_READ_ONLY_HEADLESS_TRACE",f"STATUS={'PASS' if rc==0 else 'INCOMPLETE'}",
      f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
      f"CHECKPOINT_SHA256={SOURCE_SHA256}","LAUNCHES=NO_INPUT_1,NO_INPUT_2,CIRCLE_1,CIRCLE_2",
      "FRAMES_PER_LAUNCH=900","BREAKPOINTS=0x80011A28 (8 per 100-frame window), 0x800D15A8/0x800D2520/0x800D46EC (16 per address per launch)",
      "CAPTURE=frame,pc,ra,a0,r0-r31; breakpoint handles retained in Lua locals",
      "CIRCLE_INPUT=7 press/release cycles per launch at frames 120..840; 6-frame hold; input readbacks parsed with whitespace trim",
      f"MEMCARD_TEMPLATE_SHA256={cardhash}",f"MEMCARD_WARMUP_EXIT_CODE={warmrc}",
      f"TOTAL_BREAKPOINT_EVENTS={len(events)}",f"INPUT_ROWS={len(inputs)}",
      "A0_VARIATION_REPORT=UD2_A0_VARIATION.tsv","CONDITION_COMPARISON=NO_INPUT vs CIRCLE grouped by address in UD2_A0_VARIATION.tsv",
      "CAP_EXHAUSTION=UD2_BREAKPOINT_COUNTS.tsv; early exhaustion is frame <=100",
      f"LAUNCHES_COMPLETE={'YES' if complete else 'NO'}",f"INPUTS_VALID={'YES' if inputok else 'NO'}",
      f"INSTRUMENTATION_VALID={'YES' if instok else 'NO'}",f"EXIT_CODE={rc}",
      "NO_GAME_MEMORY_OR_REGISTER_WRITES=YES; CIRCLE pad override only","RAW_DUMP=NONE"]
    (out/"UD2_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text("\n".join([f"STATUS={'PASS' if rc==0 else 'INCOMPLETE'}",
      "JOB=UD0-UD2-combined",f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
      f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",f"EXIT_CODE={rc}"])+"\n",encoding="utf-8")
    print("\n".join(lines));return rc
if __name__=="__main__":raise SystemExit(main())
