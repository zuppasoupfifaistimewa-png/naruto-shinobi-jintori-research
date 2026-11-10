#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from experiments.ub2_headless_trace import SOURCE_SHA256,EXPECTED_CARD_BYTES,sha,lua_warmup,pad_exec,run_emulator,read_log_text,write_tsv
FRAME_LIMIT=900
LAUNCHES=("NO_INPUT_SAMPLE","NO_INPUT_TRACE","CIRCLE_SAMPLE","CIRCLE_TRACE")

def lua_probe(mode,launch,instrumented):
    inst="true" if instrumented else "false"
    return r'''
local ffi=require("ffi")
local MODE="''' + mode + r'''"
local LAUNCH="''' + launch + r'''"
local INSTRUMENTED = (LAUNCH:match("_TRACE$") ~= nil)
local MOD=4294967296
local FRAME_LIMIT=900
local WRITER_CAP=32
local CALL_CAP=8
local loaded,started,post=false,false,0
local samples,w1,w2=0,0,0
local callWindow,callCount,callActive=-1,0,false
local bpCall,bpWriter1,bpWriter2=nil,nil,nil
local inputErrors=0
local mem=PCSX.getMemPtr()
local function hx(x) if x==nil then return "TIDAK TAHU" end return string.format("0x%08X",tonumber(x)%MOD) end
local function read32(address)
  local phys=(tonumber(address)%MOD)%0x20000000
  if phys<0 or phys+4>0x200000 then return "TIDAK_TAHU_OUTSIDE_2MIB" end
  local ok,v=pcall(function() return tonumber(ffi.cast("const uint32_t *",mem+phys)[0])%MOD end)
  if not ok or v==nil then return "TIDAK_TAHU_READ_ERROR" end
  return hx(v)
end
local function log(s) print(s);pcall(function() io.stdout:flush() end) end
local function writerHit(address,which)
  local old=(which=="W1_800116C8") and w1 or w2
  if old>=WRITER_CAP then return false end
  if which=="W1_800116C8" then w1=w1+1 else w2=w2+1 end
  local r=PCSX.getRegisters();local g=r.GPR
  log(table.concat({"UC2_WRITER",LAUNCH,tostring(post),which,hx(address),hx(r.pc),hx(g.n.ra),hx(g.n.v0),hx(g.n.a0),hx(g.n.gp),read32(0x8006D760)},"\t"))
  return old+1<WRITER_CAP
end
local function callHit(address)
  if callCount>=CALL_CAP then callActive=false;return false end
  callCount=callCount+1
  local r=PCSX.getRegisters();local g=r.GPR
  local z={"UC2_CALL",LAUNCH,tostring(post),hx(address),hx(r.pc),hx(g.n.ra),hx(g.n.a0),hx(g.n.v1),hx(g.n.v0)}
  for i=0,31 do z[#z+1]="r"..tostring(i).."="..hx(g.r[i]) end
  log(table.concat(z,"\t"))
  if callCount>=CALL_CAP then
    callActive=false
    log("UC2_CALL_WINDOW_CAP launch="..LAUNCH.." frame="..tostring(post).." window="..tostring(callWindow).." hits="..tostring(callCount))
    return false
  end
  return true
end
local function armCall()
  if callActive then return end
  bpCall=PCSX.addBreakpoint(0x80011A28,"Exec",4,"UC2 caller per-window cap",function(a) return callHit(a) end)
  callActive=true
end
local function armAll()
  bpWriter1=PCSX.addBreakpoint(0x800116C8,"Exec",4,"UC2 writer 116C8",function(a) return writerHit(a,"W1_800116C8") end)
  bpWriter2=PCSX.addBreakpoint(0x8001198C,"Exec",4,"UC2 writer 1198C",function(a) return writerHit(a,"W2_8001198C") end)
  armCall()
  log("UC2_BREAKPOINTS_ARMED writers=0x800116C8,0x8001198C caller=0x80011A28 cap_writer=32 cap_call=8_per_100_frames")
end
local pad,circle
if MODE=="CIRCLE" then
  PCSX.settings.pads[1].DeviceType="Analog";PCSX.settings.pads[1].Connected=true
  PCSX.SIO0.slots[1].pads[1].map();pad=PCSX.SIO0.slots[1].pads[1]
  circle=PCSX.CONSTS.PAD.BUTTON.CIRCLE;pcall(function() pad.clearOverride(circle) end)
  log("UC2_PAD_READY mode=CIRCLE")
else log("UC2_PAD_READY mode=NO_INPUT overrides=NONE") end
_G.uc2Loaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
  loaded=true;post=0;callWindow=0;callCount=0
  log("UC2_SAVE_STATE_LOADED=1 launch="..LAUNCH)
  if INSTRUMENTED then armAll() end
end)
_G.uc2Vsync=PCSX.Events.createEventListener("GPU::Vsync",function()
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
  local win=math.floor((post-1)/100)
  if win~=callWindow then callWindow=win;callCount=0;if INSTRUMENTED then armCall() end end
  if not INSTRUMENTED and post%10==0 then
    samples=samples+1;log("UC2_A0_SAMPLE\t"..LAUNCH.."\t"..tostring(post).."\t"..read32(0x8006D760))
  end
  if MODE=="CIRCLE" then
    if post>=120 and (post-120)%120==0 then
      local ok,v=pcall(function() pad.setOverride(circle);return pad.getButton(circle) end)
      local pass=ok and v==true;if not pass then inputErrors=inputErrors+1 end
      log("UC2_INPUT\t"..LAUNCH.."\t"..tostring(post).."\tCIRCLE\tPRESS\t"..tostring(v).."\t"..(pass and "PASS" or "FAIL"))
    elseif post>=126 and (post-126)%120==0 then
      local ok,v=pcall(function() pad.clearOverride(circle);return pad.getButton(circle) end)
      local pass=ok and v==false;if not pass then inputErrors=inputErrors+1 end
      log("UC2_INPUT\t"..LAUNCH.."\t"..tostring(post).."\tCIRCLE\tRELEASE\t"..tostring(v).."\t"..(pass and "PASS" or "FAIL"))
    end
  end
  if post==FRAME_LIMIT then
    log("UC2_FRAME_LIMIT_REACHED launch="..LAUNCH.." frames="..post.." samples="..samples.." writer_hits="..tostring(w1+w2))
    PCSX.nextTick(function() PCSX.quit(inputErrors==0 and 0 or 52) end)
  end
end)
log("UC2_SCRIPT_READY launch="..LAUNCH.." mode="..MODE.." instrumented="..tostring(INSTRUMENTED).." frames=900 read_only=YES")
'''.lstrip()

def parse_log(log):
    samples,writers,calls,inputs=[],[],[],[]
    for line in log.splitlines():
        if line.startswith("UC2_A0_SAMPLE\t"):
            p=line.split("\t")
            if len(p)>=4:samples.append({"launch":p[1].strip(),"frame":p[2].strip(),"value":p[3].strip()})
        elif line.startswith("UC2_WRITER\t"):
            p=line.split("\t")
            if len(p)>=11:writers.append({"launch":p[1],"frame":p[2],"writer":p[3],"breakpoint_pc":p[4],"pc":p[5],
               "ra":p[6],"value_v0":p[7],"a0":p[8],"gp":p[9],"mem_before":p[10]})
        elif line.startswith("UC2_CALL\t"):
            p=line.split("\t")
            if len(p)>=9:
                r={"launch":p[1],"frame":p[2],"breakpoint_pc":p[3],"pc":p[4],"ra":p[5],"a0":p[6],"v1":p[7],"v0":p[8]}
                for item in p[9:]:
                    if "=" in item:k,v=item.split("=",1);r[k]=v
                calls.append(r)
        elif line.startswith("UC2_INPUT\t"):
            p=line.split("\t")
            if len(p)>=7:inputs.append({"launch":p[1].strip(),"frame":p[2].strip(),"button":p[3].strip(),"action":p[4].strip(),"readback":p[5].strip(),"status":p[6].strip()})
    return samples,writers,calls,inputs

def main():
    ap=argparse.ArgumentParser()
    for k in ("work","out","pcsx-bin","appdir","bios","cue","source","card-dir"):ap.add_argument("--"+k,required=True)
    ap.add_argument("--timeout-seconds",type=int,default=120);a=ap.parse_args()
    work,out=Path(a.work),Path(a.out);out.mkdir(parents=True,exist_ok=True)
    pcsx,appdir,bios,cue,source,carddir=map(Path,(a.pcsx_bin,a.appdir,a.bios,a.cue,a.source,a.card_dir))
    if sha(source)!=SOURCE_SHA256 or source.stat().st_size!=21162799:raise SystemExit("UC2_CHECKPOINT_IDENTITY_FAIL")
    source.chmod(0o444);carddir.mkdir(parents=True,exist_ok=True)
    template=carddir/"memory-card-template.mcd";warm=work/"uc2-warmup.lua";warm.write_text(lua_warmup(),encoding="utf-8")
    warmrc,_,_=run_emulator(pcsx,appdir,bios,cue,template,None,warm,work/"uc2-warmup-home",work/"uc2-warmup.stdout.txt",120)
    if not template.is_file() or template.stat().st_size!=EXPECTED_CARD_BYTES:raise SystemExit("UC2_MEMCARD_WARMUP_FAIL")
    cardhash=sha(template);launchrows=[];samples=[];writers=[];calls=[];inputs=[]
    for launch in LAUNCHES:
        mode="CIRCLE" if launch.startswith("CIRCLE") else "NO_INPUT";inst=launch.endswith("_TRACE")
        d=work/launch.lower();d.mkdir(parents=True,exist_ok=True)
        state=d/"source.sstate";shutil.copyfile(source,state);state.chmod(0o444)
        card=d/"memory-card.mcd";shutil.copyfile(template,card);cardbefore=sha(card)
        lua=d/"uc2.lua";lua.write_text(lua_probe(mode,launch,inst),encoding="utf-8")
        stdout=d/"emulator.stdout.txt"
        rc,wall,_=run_emulator(pcsx,appdir,bios,cue,card,state,lua,d/"home",stdout,a.timeout_seconds,pad_exec() if mode=="CIRCLE" else None)
        log=read_log_text(stdout);ss,ww,cc,ii=parse_log(log)
        (out/("UC2_"+launch+"_EMULATOR_LOG.txt")).write_text("\\n".join(log.splitlines()[-160:])+"\\n",encoding="utf-8")
        samples+=ss;writers+=ww;calls+=cc;inputs+=ii
        frames=0
        for line in log.splitlines():
            if line.startswith("UC2_FRAME_LIMIT_REACHED"):
                try:frames=int(line.split("frames=",1)[1].split()[0])
                except Exception:pass
        loaded="UC2_SAVE_STATE_LOADED=1" in log;loadok="UC2_LOAD_CALL_RETURNED=1" in log
        expected=14 if mode=="CIRCLE" else 0;cardafter=sha(card) if card.exists() else "TIDAK TAHU"
        launchrows.append({"launch":launch,"condition":mode,"capture":"BREAKPOINTS" if inst else "SAMPLE_ONLY",
          "frames_reached":frames,"save_state_loaded":"YES" if loaded else "NO","load_call_returned":"YES" if loadok else "NO",
          "sample_count":len(ss),"writer_hit_count":len(ww),"call_hit_count":len(cc),"input_events":len(ii),
          "input_events_expected":expected,"input_validation":"PASS" if len(ii)==expected and all(x["status"]=="PASS" for x in ii) else "FAIL",
          "emulator_exit_code":rc,"wall_seconds":f"{wall:.3f}","memory_card_sha256_before":cardbefore,
          "memory_card_sha256_after":cardafter,"memory_card_unchanged":"YES" if cardafter==cardbefore else "NO",
          "checkpoint_sha256_after":sha(state) if state.exists() else "TIDAK TAHU"})
        state.unlink(missing_ok=True);card.unlink(missing_ok=True)
    sampleok=all(sum(1 for x in samples if x["launch"]==n)==90 for n in ("NO_INPUT_SAMPLE","CIRCLE_SAMPLE"))
    complete=all(x["frames_reached"]==FRAME_LIMIT and x["save_state_loaded"]=="YES" and x["load_call_returned"]=="YES" and
                 x["emulator_exit_code"]==0 and x["memory_card_unchanged"]=="YES" for x in launchrows)
    inputok=all(x["input_validation"]=="PASS" for x in launchrows)
    st="PASS" if sampleok and complete and inputok else "INCOMPLETE"
    write_tsv(out/"UC2_A0_SAMPLES.tsv",["launch","frame","value"],samples)
    write_tsv(out/"UC2_WRITER_EVENTS.tsv",["launch","frame","writer","breakpoint_pc","pc","ra","value_v0","a0","gp","mem_before"],writers)
    write_tsv(out/"UC2_CALLSITE_EVENTS.tsv",["launch","frame","breakpoint_pc","pc","ra","a0","v1","v0"]+[f"r{i}" for i in range(32)],calls)
    write_tsv(out/"UC2_INPUT_EVENTS.tsv",["launch","frame","button","action","readback","status"],inputs)
    write_tsv(out/"UC2_LAUNCHES.tsv",list(launchrows[0].keys()),launchrows)
    writer1=sum(x["writer"]=="W1_800116C8" for x in writers);writer2=sum(x["writer"]=="W2_8001198C" for x in writers)
    a0sets={n:sorted({x["a0"] for x in calls if x["launch"]==n}) for n in ("NO_INPUT_TRACE","CIRCLE_TRACE")}
    lines=["UC2_READ_ONLY_CHECKPOINT_TRACE",f"STATUS={st}",f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",
      f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",f"CHECKPOINT_SHA256={SOURCE_SHA256}",
      "LAUNCH_PLAN=NO_INPUT sample-only + instrumented; CIRCLE sample-only + instrumented; 900 post-load frames each",
      "SAMPLE=MEM32[0x8006D760] every 10 frames in SAMPLE_ONLY launches; no breakpoints",
      "WRITERS=EXEC breakpoints 0x800116C8 and 0x8001198C; 32 hits/address/trace launch",
      "CALLSITE=EXEC 0x80011A28; cap 8 hits in each 100-frame window; records PC, RA and r0-r31/a0/v1/v0",
      "WRITER_VALUE=v0 before store; MEM32[0x8006D760] read before store",
      "PROBE_MEMORY_OR_REGISTER_WRITES=NONE; CIRCLE pad override only", "RAW_DUMP=NONE",
      f"MEMCARD_TEMPLATE_SHA256={cardhash}","CHECKPOINT_ENV=UB2_SOURCE_STATE (matches legacy run_emulator helper)",f"MEMCARD_WARMUP_EXIT_CODE={warmrc}",
      f"NO_INPUT_SAMPLE_ROWS={sum(x['launch']=='NO_INPUT_SAMPLE' for x in samples)}",
      f"CIRCLE_SAMPLE_ROWS={sum(x['launch']=='CIRCLE_SAMPLE' for x in samples)}",
      f"WRITER_800116C8_HITS={writer1}",f"WRITER_8001198C_HITS={writer2}",
      f"CALLSITE_HITS={len(calls)}",f"CALLSITE_A0_VALUES={a0sets}",
      "K5_NOT_CLAIMED=two launches per condition use complementary capture modes; no identical repeated-trace comparison",
      f"LAUNCHES_COMPLETE={'YES' if complete else 'NO'}",f"SAMPLES_COMPLETE={'YES' if sampleok else 'NO'}",
      f"INPUTS_VALID={'YES' if inputok else 'NO'}",f"EXIT_CODE={0 if st=='PASS' else 2}"]
    (out/"UC2_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text("\n".join([f"STATUS={st}","JOB=uc0-uc2-combined",
      f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",
      f"EXIT_CODE={0 if st=='PASS' else 2}"])+"\n",encoding="utf-8")
    print("\n".join(lines));return 0 if st=="PASS" else 2
if __name__=="__main__":raise SystemExit(main())
