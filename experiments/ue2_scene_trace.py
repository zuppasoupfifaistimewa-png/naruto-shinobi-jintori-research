#!/usr/bin/env python3
"""UE2: instrumented PCSX-Redux headless trace; all-hit counters are separate from capture caps."""
from __future__ import annotations
import argparse,csv,os,shutil,sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from experiments.ub2_headless_trace import SOURCE_SHA256,EXPECTED_CARD_BYTES,sha,lua_warmup,pad_exec,run_emulator,read_log_text,write_tsv
FRAME_LIMIT=900
BP=((0x800D15A8,"TARGET_800D15A8"),(0x800B54DC,"SCENE_CALL_800B54DC"),
    (0x800F3658,"WRAPPER_800F3658"),(0x800F5DAC,"WRAPPER_CALL_800F5DAC"))
EXPECTED_BP_COUNT=len(BP)
LAUNCHES=("NO_INPUT_1","NO_INPUT_2","CIRCLE_1","CIRCLE_2","DOWN_CIRCLE_1","DOWN_CIRCLE_2")
def hx(v): return f"0x{int(v)&0xffffffff:08X}"
def lua_probe(mode,launch):
    specs=",".join("{"+f"0x{a:08X}"+',"'+n+'"}' for a,n in BP)
    return r'''
local MODE="''' + mode + r'''"
local LAUNCH="''' + launch + r'''"
local FRAME_LIMIT=900
local EXPECTED_BP_COUNT=4
local MOD=4294967296
local loaded,started,post=false,false,0
local handles={}
local totals={}
local windowCaptures={}
local windows={{id="INITIAL_1_30",start=1}}
local inputErrors=0
local function hx(x) if x==nil then return "TIDAK TAHU" end return string.format("0x%08X",tonumber(x)%MOD) end
local function log(s) print(s);pcall(function() io.stdout:flush() end) end
local function hit(address,label)
  totals[label]=(totals[label] or 0)+1
  local r=PCSX.getRegisters();local g=r.GPR
  for _,w in ipairs(windows) do
    if post>=w.start and post<w.start+30 then
      local key=label.."|"..w.id
      local n=windowCaptures[key] or 0
      if n<8 then
        n=n+1;windowCaptures[key]=n
        local z={"UE2_BP",LAUNCH,MODE,tostring(post),label,hx(address),hx(r.pc),hx(g.n.ra),
                 "WINDOW="..w.id,"WINDOW_START="..tostring(w.start),"HIT_IN_WINDOW="..tostring(n)}
        z[#z+1]="a0="..hx(g.n.a0)
        for i=0,31 do z[#z+1]="r"..tostring(i).."="..hx(g.r[i]) end
        log(table.concat(z,"\t"))
      end
    end
  end
  return true
end
local function armAll()
  local specs={''' + specs + r'''}
  local armed=0
  for _,spec in ipairs(specs) do
    local addr,label=spec[1],spec[2]
    local ok,h=pcall(function() return PCSX.addBreakpoint(addr,"Exec",4,"UE2 "..label,function(a) return hit(a,label) end) end)
    if ok and h~=nil then handles[label]=h;totals[label]=0;armed=armed+1
    else log("UE2_BREAKPOINT_INSTALL_FAIL\t"..label.."\t"..tostring(h)) end
  end
  log("instrumented="..tostring(armed==EXPECTED_BP_COUNT).." armed="..tostring(armed))
  return armed
end
local pad,circle,down
if MODE~="NO_INPUT" then
  PCSX.settings.pads[1].DeviceType="Analog";PCSX.settings.pads[1].Connected=true
  PCSX.SIO0.slots[1].pads[1].map();pad=PCSX.SIO0.slots[1].pads[1]
  local B=PCSX.CONSTS.PAD.BUTTON;circle=B.CIRCLE;down=B.DOWN
  if circle==nil or ((MODE=="DOWN_CIRCLE") and down==nil) then
    log("UE2_BUTTON_CONSTANT_MISSING\t"..MODE);PCSX.quit(4)
  end
  pcall(function() pad.clearOverride(circle) end)
  if down~=nil then pcall(function() pad.clearOverride(down) end) end
  log("UE2_PAD_READY mode="..MODE)
else log("UE2_PAD_READY mode=NO_INPUT overrides=NONE") end
local function apply(button,action,name)
  local ok,v=pcall(function()
    if action=="PRESS" then pad.setOverride(button) else pad.clearOverride(button) end
    return pad.getButton(button)
  end)
  local want=(action=="PRESS")
  local pass=ok and v==want
  if not pass then inputErrors=inputErrors+1 end
  log("UE2_INPUT\t"..LAUNCH.."\t"..tostring(post).."\t"..name.."\t"..action.."\t"..tostring(v).."\t"..(pass and "PASS" or "FAIL"))
  local id=name.."_"..action.."_F"..tostring(post)
  windows[#windows+1]={id=id,start=post}
end
_G.ue2Loaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
  loaded=true;post=0
  log("UE2_SAVE_STATE_LOADED=1 launch="..LAUNCH)
  local armed=armAll()
  if armed~=EXPECTED_BP_COUNT then PCSX.nextTick(function() PCSX.quit(3) end) end
end)
_G.ue2Vsync=PCSX.Events.createEventListener("GPU::Vsync",function()
  if not started then
    started=true;local path=os.getenv("UE2_SOURCE_STATE") or "resume/source.sstate"
    log("UE2_LOAD_BEGIN=1 path="..path);PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf,f=pcall(function() return assert(Support.File.open(path)) end)
      if not okf or not f then log("UE2_STATE_OPEN_FAIL="..tostring(f));PCSX.quit(50);return end
      local ok,err=pcall(function() PCSX.loadSaveState(f) end);f:close()
      if not ok then log("UE2_STATE_LOAD_FAIL="..tostring(err));PCSX.quit(51);return end
      log("UE2_LOAD_CALL_RETURNED=1");PCSX.resumeEmulator()
    end);return
  end
  if not loaded then return end
  post=post+1
  if MODE=="CIRCLE" then
    if post==31 then apply(circle,"PRESS","CIRCLE")
    elseif post==37 then apply(circle,"RELEASE","CIRCLE") end
  elseif MODE=="DOWN_CIRCLE" then
    if post==31 then apply(down,"PRESS","DOWN")
    elseif post==37 then apply(down,"RELEASE","DOWN")
    elseif post==43 then apply(circle,"PRESS","CIRCLE")
    elseif post==49 then apply(circle,"RELEASE","CIRCLE") end
  end
  if post==FRAME_LIMIT then
    for _,spec in ipairs({''' + specs + r'''}) do log("UE2_BP_TOTAL\t"..LAUNCH.."\t"..spec[2].."\t"..tostring(totals[spec[2]] or 0)) end
    log("UE2_FRAME_LIMIT_REACHED launch="..LAUNCH.." frames="..post)
    PCSX.nextTick(function() PCSX.quit(inputErrors==0 and 0 or 2) end)
  end
end)
log("UE2_SCRIPT_READY launch="..LAUNCH.." mode="..MODE.." frames=900 requested_breakpoints=4 instrumented=true")
'''.lstrip()
def parse_log(log):
    events=[];inputs=[];totals={};armed=[]
    for line in log.splitlines():
        p=[x.strip() for x in line.rstrip("\r\n").split("\t")]
        if p and p[0]=="UE2_BP" and len(p)>=11:
            r={"launch":p[1],"condition":p[2],"frame":p[3],"label":p[4],"address":p[5],"pc":p[6],"ra":p[7],
               "window":p[8].split("=",1)[-1],"window_start":p[9].split("=",1)[-1],"hit_in_window":p[10].split("=",1)[-1]}
            for item in p[11:]:
                if "=" in item:k,v=item.split("=",1);r[k]=v
            events.append(r)
        elif p and p[0]=="UE2_INPUT" and len(p)>=7:
            inputs.append({"launch":p[1],"frame":p[2],"button":p[3],"action":p[4],"readback":p[5],"status":p[6]})
        elif p and p[0]=="UE2_BP_TOTAL" and len(p)>=4:
            totals[(p[1],p[2])]=int(p[3])
        elif line.strip().startswith("instrumented="):
            armed.append({x.split("=",1)[0]:x.split("=",1)[1] for x in line.strip().split() if "=" in x})
    return events,inputs,totals,armed
def build_counts(events,totals):
    rows=[]
    for launch in LAUNCHES:
        condition="NO_INPUT" if launch.startswith("NO_INPUT") else ("CIRCLE" if launch.startswith("CIRCLE") else "DOWN_CIRCLE")
        for addr,label in BP:
            rows.append({"launch":launch,"condition":condition,"address":hx(addr),"label":label,
                "total_hits":totals.get((launch,label),"TIDAK TAHU"),
                "captured_records":sum(1 for e in events if e.get("launch")==launch and e.get("label")==label),
                "cap_rule":"all hits counted; first 8 captured per 30-frame input-relative window and frames 1-30"})
    return rows
def write_failfast(path,launch,armed_count,expected):
    path.write_text(
      f"STATUS=FAIL_FAST\nLAUNCH={launch}\nARMED={armed_count}\nEXPECTED={expected}\n"
      "NO_FURTHER_LAUNCHES=YES\n",encoding="utf-8")
def self_test(reports,out):
    event_path=reports/"UD2_BREAKPOINT_EVENTS.tsv";input_path=reports/"UD2_INPUT_EVENTS.tsv"
    if not event_path.is_file() or not input_path.is_file():raise SystemExit("UE2_SELF_TEST_INPUT_MISSING")
    with event_path.open("r",encoding="utf-8-sig",newline="") as f: events=list(csv.DictReader(f,delimiter="\t"))
    with input_path.open("r",encoding="utf-8-sig",newline="") as f: inputs=list(csv.DictReader(f,delimiter="\t"))
    need={"launch","condition","frame","label","address","pc","ra"}|{f"r{i}" for i in range(32)}
    if not events or not need.issubset(events[0]):raise SystemExit("UE2_SELF_TEST_EVENT_SCHEMA_FAIL")
    by=defaultdict(int)
    for e in events: by[(e["launch"],e["label"])]+=1
    if not inputs:raise SystemExit("UE2_SELF_TEST_INPUT_PARSE_FAIL")
    # Exercise the same counter-table builder and writer used by the live run.
    rows=build_counts(events,{})
    out.mkdir(parents=True,exist_ok=True)
    test_table=out/"UE2_POSTPROCESS_SELF_TEST_COUNTS.tsv"
    write_tsv(test_table,list(rows[0].keys()),rows)
    with test_table.open("r",encoding="utf-8",newline="") as f:
        reread=list(csv.DictReader(f,delimiter="\t"))
    if len(reread)!=len(LAUNCHES)*len(BP):raise SystemExit("UE2_SELF_TEST_COUNTS_ROUNDTRIP_FAIL")
    rendered=[hx(int(e["address"],16)) for e in events[:min(8,len(events))]]
    (out/"UE2_POSTPROCESS_SELF_TEST.txt").write_text(
      "STATUS=PASS\nSOURCE=committed UD2 breakpoint/input TSV\n"
      f"UD2_EVENT_ROWS={len(events)}\nUD2_INPUT_ROWS={len(inputs)}\n"
      f"LAUNCHES={len({e['launch'] for e in events})}\n"
      f"BREAKPOINT_GROUPS={len(by)}\n"
      f"COUNTER_TABLE_ROWS={len(reread)}\n"
      f"ADDRESS_FORMAT_TESTS={len(rendered)}\nNO_NAMEERROR=YES\n",encoding="utf-8")
    failfast_path=out/"UE2_FAILFAST_INJECTION_TEST.txt"
    write_failfast(failfast_path,"INJECTED_FAILURE",2,EXPECTED_BP_COUNT)
    failfast_text=failfast_path.read_text(encoding="utf-8")
    if "ARMED=2" not in failfast_text or "EXPECTED=4" not in failfast_text:
        raise SystemExit("UE2_FAILFAST_INJECTION_TEST_FAIL")
    with failfast_path.open("a",encoding="utf-8") as stream:
        stream.write("INJECTION_TEST=PASS; no NameError\n")
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--work");ap.add_argument("--out",required=True);ap.add_argument("--pcsx-bin");ap.add_argument("--appdir")
    ap.add_argument("--bios");ap.add_argument("--cue");ap.add_argument("--source");ap.add_argument("--card-dir")
    ap.add_argument("--timeout-seconds",type=int,default=180);ap.add_argument("--postprocess-self-test",action="store_true")
    ap.add_argument("--reports")
    a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    if a.postprocess_self_test:
        if not a.reports:raise SystemExit("--reports required for self-test")
        self_test(Path(a.reports),out);print("UE2_POSTPROCESS_SELF_TEST=PASS");return 0
    work=Path(a.work);pcsx,appdir,bios,cue,source,carddir=map(Path,(a.pcsx_bin,a.appdir,a.bios,a.cue,a.source,a.card_dir))
    if sha(source)!=SOURCE_SHA256 or source.stat().st_size!=21162799:raise SystemExit("UE2_CHECKPOINT_IDENTITY_FAIL")
    source.chmod(0o444);carddir.mkdir(parents=True,exist_ok=True)
    template=carddir/"memory-card-template.mcd";warm=work/"ue2-warmup.lua";warm.write_text(lua_warmup(),encoding="utf-8")
    warmrc,_,_=run_emulator(pcsx,appdir,bios,cue,template,None,warm,work/"warm-home",work/"warm.stdout.txt",120)
    if not template.is_file() or template.stat().st_size!=EXPECTED_CARD_BYTES:raise SystemExit("UE2_MEMCARD_WARMUP_FAIL")
    cardhash=sha(template);launchrows=[];all_events=[];all_inputs=[];all_totals={}
    for launch in LAUNCHES:
        mode="NO_INPUT" if launch.startswith("NO_INPUT") else ("CIRCLE" if launch.startswith("CIRCLE") else "DOWN_CIRCLE")
        d=work/launch.lower();d.mkdir(parents=True,exist_ok=True)
        state=d/"source.sstate";shutil.copyfile(source,state);state.chmod(0o444)
        card=d/"memory-card.mcd";shutil.copyfile(template,card);before=sha(card);card.chmod(0o444)
        lua=d/"ue2.lua";lua.write_text(lua_probe(mode,launch),encoding="utf-8")
        stdout=d/"emulator.stdout.txt"
        rc,wall,_=run_emulator(pcsx,appdir,bios,cue,card,state,lua,d/"home",stdout,a.timeout_seconds,pad_exec() if mode!="NO_INPUT" else None)
        log=read_log_text(stdout);ev,ii,tt,aa=parse_log(log);all_events+=ev;all_inputs+=ii
        for k,v in tt.items():all_totals[k]=v
        (out/("UE2_"+launch+"_EMULATOR_LOG.txt")).write_text("\n".join(log.splitlines()[-220:])+"\n",encoding="utf-8")
        frames=900 if "UE2_FRAME_LIMIT_REACHED launch="+launch+" frames=900" in log else 0
        armed_count=max([int(x.get("armed","0")) for x in aa] or [0])
        instrumented=any(x.get("instrumented")=="true" and x.get("armed")==str(EXPECTED_BP_COUNT) for x in aa) and armed_count==EXPECTED_BP_COUNT
        expected={"NO_INPUT":0,"CIRCLE":2,"DOWN_CIRCLE":4}[mode]
        valid=len(ii)==expected and all(x["status"]=="PASS" for x in ii)
        after=sha(card) if card.exists() else "TIDAK TAHU"
        card_read_only=card.exists() and (card.stat().st_mode & 0o222)==0
        launchrows.append({"launch":launch,"condition":mode,"frames_reached":frames,
          "save_state_loaded":"YES" if "UE2_SAVE_STATE_LOADED=1 launch="+launch in log else "NO",
          "instrumented":"true" if instrumented else "false","armed":armed_count,
          "logged_total_counter_rows":len(tt),"captured_event_rows":len(ev),"input_rows":len(ii),"all_bp_total_counters":"YES" if len(tt)==EXPECTED_BP_COUNT else "NO",
          "input_expected":expected,"input_validation":"PASS" if valid else "FAIL","emulator_exit_code":rc,
          "wall_seconds":f"{wall:.3f}","memory_card_sha256_before":before,"memory_card_sha256_after":after,
          "memory_card_unchanged":"YES" if after==before else "NO",
          "memory_card_read_only":"true" if card_read_only else "false",
          "checkpoint_sha256_after":sha(state) if state.exists() else "TIDAK TAHU"})
        if not instrumented or armed_count!=EXPECTED_BP_COUNT:
            write_failfast(out/"UE2_BREAKPOINT_INSTALL_FAILURE.txt",launch,armed_count,EXPECTED_BP_COUNT)
            event_fields=["launch","condition","frame","label","address","pc","ra","a0","window","window_start","hit_in_window"]+[f"r{i}" for i in range(32)]
            write_tsv(out/"UE2_BREAKPOINT_EVENTS.tsv",event_fields,all_events)
            write_tsv(out/"UE2_INPUT_EVENTS.tsv",["launch","frame","button","action","readback","status"],all_inputs)
            partial_counts=build_counts(all_events,all_totals)
            write_tsv(out/"UE2_BREAKPOINT_COUNTS.tsv",list(partial_counts[0].keys()),partial_counts)
            write_tsv(out/"UE2_LAUNCHES.tsv",list(launchrows[0].keys()),launchrows)
            (out/"UE2_SUMMARY.txt").write_text("\n".join([
              "UE2_READ_ONLY_HEADLESS_TRACE","STATUS=FAIL_FAST",
              f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",
              f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
              f"LAUNCHES_ATTEMPTED={len(launchrows)}","NO_FURTHER_LAUNCHES=YES",
              f"BREAKPOINTS={','.join(hx(item[0]) for item in BP)}",
              f"ARMED_COUNT={armed_count}",f"INSTRUMENTED={'true' if instrumented else 'false'}",
              "ALL_HIT_TOTALS=TIDAK TAHU; fail-fast occurred before frame limit",
              f"CAPTURED_EVENTS={len(all_events)}",f"INPUT_ROWS={len(all_inputs)}",
              f"MEMORY_CARD_READ_ONLY={'true' if card_read_only else 'false'}",
              f"MEMORY_CARD_UNCHANGED={'true' if after==before else 'false'}",
              f"CHECKPOINT_SHA256_AFTER={sha(state) if state.exists() else 'TIDAK TAHU'}",
              "EXIT_CODE=3","RAW_DUMP=NONE"
            ])+"\n",encoding="utf-8")
            raise SystemExit(3)
        state.unlink(missing_ok=True);card.unlink(missing_ok=True)
    event_fields=["launch","condition","frame","label","address","pc","ra","a0","window","window_start","hit_in_window"]+[f"r{i}" for i in range(32)]
    write_tsv(out/"UE2_BREAKPOINT_EVENTS.tsv",event_fields,all_events)
    write_tsv(out/"UE2_INPUT_EVENTS.tsv",["launch","frame","button","action","readback","status"],all_inputs)
    counts=build_counts(all_events,all_totals)
    write_tsv(out/"UE2_BREAKPOINT_COUNTS.tsv",list(counts[0].keys()),counts)
    write_tsv(out/"UE2_LAUNCHES.tsv",list(launchrows[0].keys()),launchrows)
    instok=all(x["instrumented"]=="true" and x["armed"]==EXPECTED_BP_COUNT for x in launchrows)
    complete=all(x["frames_reached"]==900 and x["save_state_loaded"]=="YES" and x["instrumented"]=="true" and
                 x["armed"]==EXPECTED_BP_COUNT and x["all_bp_total_counters"]=="YES" and x["emulator_exit_code"]==0 and
                 x["memory_card_unchanged"]=="YES" and x["memory_card_read_only"]=="true" and
                 x["checkpoint_sha256_after"]==SOURCE_SHA256 for x in launchrows)
    inputs_ok=all(x["input_validation"]=="PASS" for x in launchrows)
    rc=0 if complete and inputs_ok else 3
    lines=["UE2_READ_ONLY_HEADLESS_TRACE",f"STATUS={'PASS' if rc==0 else 'INCOMPLETE'}",
      f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
      f"CHECKPOINT_SHA256={SOURCE_SHA256}","CONDITIONS=NO_INPUT,CIRCLE,DPAD_BAWAH_THEN_CIRCLE; TWO_LAUNCHES_EACH",
      "FRAMES_PER_LAUNCH=900","BREAKPOINTS="+",".join(hx(x[0]) for x in BP),
      "TOTAL_HIT_COUNTER=all hits; capture cap is separate (8 per breakpoint/window); exactly 4 breakpoints",
      "CAPTURE=first 8 hits per breakpoint in frames 1-30 and each input-relative 30-frame window; a0, RA and r0-r31 included",
      "INPUT=CIRCLE press 6 frames then release; DPAD_DOWN press 6 frames/release then CIRCLE press 6 frames/release",
      f"MEMCARD_TEMPLATE_SHA256={cardhash}",f"MEMCARD_WARMUP_EXIT_CODE={warmrc}",
      f"CAPTURED_EVENTS={len(all_events)}",f"INPUT_ROWS={len(all_inputs)}",
      f"LAUNCHES_COMPLETE={'YES' if complete else 'NO'}",f"INPUTS_VALID={'YES' if inputs_ok else 'NO'}",
      f"ALL_BREAKPOINT_INSTALLS_VALID={'YES' if instok else 'NO'}",f"EXIT_CODE={rc}",
      "MEMORY_CARD_MODE=read-only (0444) each launch; SHA256 checked before/after",
      "NO_GAME_MEMORY_OR_REGISTER_WRITES=YES; pad overrides only","RAW_DUMP=NONE"]
    (out/"UE2_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text("\n".join([f"STATUS={'completed/success' if rc==0 else 'completed/failure'}",
      "JOB=UF0 direct HEAD TSV gate and UF2 six-launch read-only trace",f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
      f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",f"EXIT_CODE={rc}"])+"\n",encoding="utf-8")
    print("\n".join(lines));return rc
if __name__=="__main__":raise SystemExit(main())
