#!/usr/bin/env python3
"""AW3 controlled direct calls in PCSX-Redux interpreter from a freshly loaded H6-HYBRID.

No user input, adaptive-player execution, or Story Mode automation. The pure tile
helper, getter and setter are called with controlled arguments. All mutated
record bytes and CPU registers are restored after each call. Binary inputs remain
runner-local and are deleted by the workflow.
"""
from __future__ import annotations
import argparse, csv, hashlib, os, re, shutil, subprocess, time
from pathlib import Path
from aj2_h6_ram_probe import one, replace_top, encmsg

TARGET_SHA="00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA="9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA="d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
MCD_SHA="ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5"
TIMEOUT_SECONDS=600
HISTORICAL_MAX_WALL=241.088
RAM_SIZE=0x200000
RECORD_SIZE=0x124

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def signed32(n:int)->int:
    n &= 0xffffffff
    return n-0x100000000 if n & 0x80000000 else n

def tests():
    rows=[]
    for idx in (0,1):
        rows.append({"kind":"GETTER","fn":0x800138EC,"a0":idx,"a1":0xA1A1A1A1,
                     "a2":0xA2A2A2A2,"a3":0xA3A3A3A3,"expected":1500,
                     "label":f"getter_control_index_{idx}"})
    h_values=((0x00,19),(0x02,101),(0x1E,257))
    for selector in range(5):
        for offset,h in h_values:
            numer={0:10,1:12,2:15,3:18,4:20}[selector]
            expected=h if selector==0 else (h*numer)//10
            rows.append({"kind":"TILE_HELPER","fn":0x800B770C,"a0":0,
                         "a1":0xA1A1A1A1,"a2":0xA2A2A2A2,"a3":0xA3A3A3A3,
                         "selector":selector,"halfword_offset":offset,"h":h,
                         "expected":expected,"label":f"selector_{selector}_field_{0x10+offset:02X}_h_{h}"})
    rows.append({"kind":"TILE_HELPER","fn":0x800B770C,"a0":0,"a1":0xA1A1A1A1,
                 "a2":0xA2A2A2A2,"a3":0xA3A3A3A3,"selector":5,
                 "halfword_offset":0x00,"h":101,"expected":0,"label":"selector_5_default_zero"})
    for value in (100,1500,100000,-10000):
        expected=max(-9999,min(99999,value))
        rows.append({"kind":"SETTER","fn":0x8001387C,"a0":0,"a1":value,
                     "a2":0xA2A2A2A2,"a3":0xA3A3A3A3,"input_value":value,
                     "expected":1,"expected_store":expected,
                     "label":f"setter_index_0_value_{value}"})
    return rows

def lua_number(n:int)->str:
    return str(n if n>=0 else n+0x100000000)

def lua_source(cases):
    test_entries=[]
    for x in cases:
        props=[f'kind="{x["kind"]}"',f'fn=0x{x["fn"]:08X}',
               f'a0={lua_number(x["a0"])}',f'a1={lua_number(x["a1"])}',
               f'a2={lua_number(x["a2"])}',f'a3={lua_number(x["a3"])}',
               f'expected={x["expected"]}',f'label="{x["label"]}"']
        for k in ("selector","halfword_offset","h","input_value","expected_store"):
            if k in x:props.append(f'{k}={lua_number(x[k])}')
        test_entries.append("  {"+",".join(props)+"}")
    table=",\n".join(test_entries)
    return r"""
if io.stdout then io.stdout:setvbuf("no") end
local ffi=require("ffi")
local bit=require("bit")
ffi.cdef[[
typedef unsigned char aw3_u8;
typedef unsigned short aw3_u16;
typedef unsigned int aw3_u32;

unsigned char *SHA256(const unsigned char *d, unsigned long n, unsigned char *md);
]]
local cryptoOk,crypto=pcall(ffi.load,"crypto")
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
local function fail(tag,detail)
  log("AW3_FATAL tag="..tag.." detail="..tostring(detail))
  PCSX.quit(92)
end
if not cryptoOk then fail("OPENSSL_LOAD",crypto); return end
local mem=PCSX.getMemPtr()
local SENTINEL=0x801FFFE0
local RAM_SIZE=0x200000
local RECORD_SIZE=0x124
local RECORD_SLOT=0x8013EA84
local PLAYER_BASE=0x80070EA0
local post=0
local preloadTicks=0
local started=false
local loaded=false
local running=false
local testIndex=1
local bp=nil
local cases={
__TEST_TABLE__
}
local originalRegs=nil
local recordBase=nil
local recordPhys=nil
local tileBackup=nil
local playerBackup=nil
local baselineRam=nil
local baselineSha=nil
local callRows=0
local failedCalls=0

local function phys(a) return bit.band(a,0x1fffffff) end
local function rd8(a) return tonumber(mem[phys(a)]) end
local function wr8(a,v) mem[phys(a)]=v%256 end
local function rd16(a) return tonumber(ffi.cast("aw3_u16*",mem+phys(a))[0]) end
local function wr16(a,v) ffi.cast("aw3_u16*",mem+phys(a))[0]=v%65536 end
local function rd32(a) return tonumber(ffi.cast("aw3_u32*",mem+phys(a))[0]) end
local function wr32(a,v) ffi.cast("aw3_u32*",mem+phys(a))[0]=v end
local function ramString() return ffi.string(mem,RAM_SIZE) end
local function ramSha()
  local out=ffi.new("unsigned char[32]")
  crypto.SHA256(ffi.cast("const unsigned char*",mem),RAM_SIZE,out)
  return (ffi.string(out,32):gsub(".",function(c)return string.format("%02x",string.byte(c))end))
end
local function s32(v)
  v=tonumber(v)
  if v>=0x80000000 then return v-0x100000000 end
  return v
end
local function saveRegs()
  local r=PCSX.getRegisters()
  local t={pc=tonumber(r.pc),g={},cp0={},cp2d={},cp2c={}}
  for i=0,33 do t.g[i]=tonumber(r.GPR.r[i]) end
  for i=0,31 do
    t.cp0[i]=tonumber(r.CP0.r[i])
    t.cp2d[i]=tonumber(r.CP2D.r[i])
    t.cp2c[i]=tonumber(r.CP2C.r[i])
  end
  return t
end
local function restoreRegs(t)
  local r=PCSX.getRegisters()
  for i=0,33 do r.GPR.r[i]=t.g[i] end
  for i=0,31 do
    r.CP0.r[i]=t.cp0[i]
    r.CP2D.r[i]=t.cp2d[i]
    r.CP2C.r[i]=t.cp2c[i]
  end
  r.pc=t.pc
end
local function setCallRegs(t)
  local r=PCSX.getRegisters()
  restoreRegs(originalRegs)
  r=PCSX.getRegisters()
  r.GPR.n.a0=t.a0
  r.GPR.n.a1=t.a1
  r.GPR.n.a2=t.a2
  r.GPR.n.a3=t.a3
  r.GPR.n.ra=SENTINEL
  r.pc=t.fn
end
local function restoreInputs(t)
  if t.kind=="TILE_HELPER" then
    ffi.copy(mem+recordPhys,tileBackup,RECORD_SIZE)
  elseif t.kind=="SETTER" then
    ffi.copy(mem+phys(PLAYER_BASE),playerBackup,RECORD_SIZE)
  end
end
local function changedOffsets(before,after,limit)
  local found={}
  for i=0,limit-1 do
    if string.byte(before,i+1)~=string.byte(after,i+1) then
      found[#found+1]=i
      if #found>32 then break end
    end
  end
  return found
end
local function makeInput(t)
  if t.kind=="TILE_HELPER" then
    wr8(recordBase+0x0B,t.selector)
    wr16(recordBase+0x20,t.halfword_offset*128)
    wr16(recordBase+0x10+t.halfword_offset,t.h)
  elseif t.kind=="SETTER" then
    ffi.copy(mem+phys(PLAYER_BASE),playerBackup,RECORD_SIZE)
  end
end
local currentCase=nil
local currentBefore=nil
local currentBeforeSha=nil
local function startNext(i)
  if i>#cases then
    ffi.copy(mem+recordPhys,tileBackup,RECORD_SIZE)
    ffi.copy(mem+phys(PLAYER_BASE),playerBackup,RECORD_SIZE)
    restoreRegs(originalRegs)
    local finalSha=ramSha()
    local unchanged=(finalSha==baselineSha)
    log("AW3_FINAL_RAM baseline_sha="..baselineSha.." final_sha="..finalSha..
        " unchanged="..tostring(unchanged))
    log("AW3_DONE calls="..callRows.." failed="..failedCalls..
        " ram_restored="..tostring(unchanged))
    PCSX.quit((failedCalls==0 and unchanged and callRows==#cases) and 0 or 93)
    return
  end
  testIndex=i
  local t=cases[i]
  makeInput(t)
  currentBefore=ramString()
  currentBeforeSha=ramSha()
  currentCase=t
  setCallRegs(t)
  log("AW3_CALL_BEGIN index="..i.." label="..t.label.." fn="..
      string.format("0x%08X",t.fn).." ra="..string.format("0x%08X",SENTINEL))
  PCSX.resumeEmulator()
end
local function armReturnSentinel()
  bp=PCSX.addBreakpoint(SENTINEL,"Exec",4,"AW3_RETURN_SENTINEL",function(addr)
    local t=currentCase
    if not t then
      fail("UNEXPECTED_SENTINEL",string.format("pc=0x%08X",tonumber(addr)))
      return true
    end
    PCSX.pauseEmulator()
    local actual=tonumber(PCSX.getRegisters().GPR.n.v0)
    local after=ramString()
    local afterSha=ramSha()
    local diffs=changedOffsets(currentBefore,after,RAM_SIZE)
    local memValue="NA"
    local effectOK=true
    local ramUnchanged=(currentBefore==after)
    if t.kind=="SETTER" then
      memValue=s32(rd32(PLAYER_BASE+0x18))
      effectOK=(memValue==s32(t.expected_store))
      local targetStart=phys(PLAYER_BASE+0x18)
      for _,off in ipairs(diffs) do
        if off<targetStart or off>=targetStart+4 then effectOK=false end
      end
    elseif t.kind=="GETTER" or t.kind=="TILE_HELPER" then
      effectOK=ramUnchanged
    end
    local rawStatus=(actual==t.expected and effectOK) and "PASS" or "FAIL"
    local diffText=""
    for k=1,math.min(#diffs,32) do
      if k>1 then diffText=diffText.."," end
      diffText=diffText..string.format("0x%X",diffs[k])
    end
    if diffText=="" then diffText="NONE" end
    restoreInputs(t)
    restoreRegs(originalRegs)
    local restoredSha=ramSha()
    local restored=(restoredSha==baselineSha)
    local status=(rawStatus=="PASS" and restored) and "PASS" or "FAIL"
    if status=="FAIL" then failedCalls=failedCalls+1 end
    callRows=callRows+1
    log(table.concat({"AW3_CALL",t.label,t.kind,string.format("fn=0x%08X",t.fn),
      "a0="..string.format("0x%08X",t.a0),"a1="..string.format("0x%08X",t.a1),
      "a2="..string.format("0x%08X",t.a2),"a3="..string.format("0x%08X",t.a3),
      "expected="..tostring(t.expected),"actual="..tostring(actual),
      "memory_value="..tostring(memValue),"ram_before_sha="..currentBeforeSha,
      "ram_after_sha="..afterSha,"ram_unchanged="..tostring(ramUnchanged),
      "ram_restored_sha="..restoredSha,"ram_restored="..tostring(restored),
      "diff_offsets="..diffText,"status="..status},"|"))
    currentCase=nil
    currentBefore=nil
    currentBeforeSha=nil
    PCSX.nextTick(function() startNext(testIndex+1) end)
    return true
  end)
  log("AW3_SENTINEL_ARMED="..tostring(bp~=nil).." address="..string.format("0x%08X",SENTINEL))
  if not bp then fail("BREAKPOINT_ADD","sentinel breakpoint unavailable") end
end
_G.aw3Loaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
  loaded=true
  post=0
  log("AW3_H6_LOADED=1")
end)
_G.aw3Vsync=PCSX.Events.createEventListener("GPU::Vsync",function()
  if not started then
    started=true
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local path=os.getenv("AW3_H6_STATE") or "resume/h6-hybrid.sstate"
      local okf,f=pcall(function()return assert(Support.File.open(path))end)
      if not okf or not f then fail("STATE_OPEN",f);return end
      local ok,e=pcall(function()PCSX.loadSaveState(f)end)
      f:close()
      if not ok then fail("STATE_LOAD",e);return end
      log("AW3_H6_LOAD_CALL_RETURNED=1")
      PCSX.resumeEmulator()
    end)
    return
  end
  if loaded then
    post=post+1
    if post==180 and not running then
      running=true
      PCSX.pauseEmulator()
      PCSX.nextTick(function()
        local ok,e=pcall(function()
          if not cryptoOk then error("OpenSSL unavailable") end
          recordBase=rd32(RECORD_SLOT)
          if recordBase<0x80000000 or recordBase+RECORD_SIZE>0x80200000 then
            error(string.format("tile base pointer invalid 0x%08X",recordBase))
          end
          recordPhys=phys(recordBase)
          tileBackup=ffi.string(mem+recordPhys,RECORD_SIZE)
          playerBackup=ffi.string(mem+phys(PLAYER_BASE),RECORD_SIZE)
          originalRegs=saveRegs()
          baselineRam=ramString()
          baselineSha=ramSha()
          local p0=s32(rd32(PLAYER_BASE+0x18))
          local p1=s32(rd32(PLAYER_BASE+0xB4+0x18))
          log(string.format("AW3_BASELINE frame=180 tile_slot=0x%08X player0_chakra=%d player1_chakra=%d ram_sha=%s",
             recordBase,p0,p1,baselineSha))
          if p0~=1500 or p1~=1500 then
            error("positive getter precondition mismatch: expected player0/player1 chakra=1500")
          end
          armReturnSentinel()
          startNext(1)
        end)
        if not ok then fail("START_TESTS",e) end
      end)
    end
  else
    if started then
      preloadTicks=preloadTicks+1
      if preloadTicks>600 then fail("SAVE_STATE_LOADED_EVENT_TIMEOUT","GPU vsync continued for >600 frames without SaveStateLoaded"); return end
    end
  end
end)
log("AW3_READY interpreter=1 debugger=1 input=NONE H6=HIBRIDA")
""".replace("__TEST_TABLE__",table)

def parse_results(log):
    rows=[]
    for line in log.splitlines():
        if "AW3_CALL|" not in line:continue
        s=line[line.index("AW3_CALL|"):].strip().split("|")
        if len(s)<16:continue
        d={"label":s[1],"kind":s[2]}
        for item in s[3:]:
            if "=" in item:
                k,v=item.split("=",1);d[k]=v
        rows.append(d)
    return rows

def main():
    ap=argparse.ArgumentParser()
    for n in ("target","control","pcsx-bin","appdir","bios","cue","card","work","out"):
        ap.add_argument("--"+n,required=True)
    a=ap.parse_args()
    target=Path(a.target).read_bytes();control=Path(a.control).read_bytes()
    if sha(target)!=TARGET_SHA:raise SystemExit("TARGET_SSTATE_SHA_MISMATCH")
    if sha(control)!=CONTROL_SHA:raise SystemExit("CONTROL_SSTATE_SHA_MISMATCH")
    h6=replace_top(target,6,encmsg(6,one(control,6)))
    if sha(h6)!=H6_SHA:raise SystemExit("H6_HYBRID_SHA_MISMATCH")
    card=Path(a.card).read_bytes()
    if len(card)!=131072 or sha(card)!=MCD_SHA:raise SystemExit("MEMCARD_IDENTITY_MISMATCH")
    work,out=Path(a.work),Path(a.out);out.mkdir(parents=True,exist_ok=True)
    for d in ("resume","launches"): (work/d).mkdir(parents=True,exist_ok=True)
    h6path=work/"resume"/"h6-hybrid.sstate";h6path.write_bytes(h6)
    app=Path(a.appdir)
    env0=os.environ.copy()
    env0.update({"DISPLAY":":99","LIBGL_ALWAYS_SOFTWARE":"1",
      "LD_LIBRARY_PATH":str(app/"usr/lib")+":"+str(app/"usr/lib/x86_64-linux-gnu"),
      "QT_PLUGIN_PATH":str(app/"usr/plugins"),
      "QT_QPA_PLATFORM_PLUGIN_PATH":str(app/"usr/plugins/platforms"),
      "QML2_IMPORT_PATH":str(app/"usr/qml")})
    launches=[];allrows=[];maxwall=0.0
    for attempt in (1,2):
      root=work/"launches"/f"attempt-{attempt}"
      runtime=root/"runtime";home=root/"home"
      for d in (runtime,home/".config",home/".data",home/"runtime"):d.mkdir(parents=True,exist_ok=True)
      try:(home/"runtime").chmod(0o700)
      except OSError:pass
      mcd=root/"memory-card.mcd";shutil.copyfile(a.card,mcd)
      mcdBefore=sha(mcd.read_bytes())
      lua=root/"aw3.lua";lua.write_text(lua_source(tests()),encoding="utf-8")
      pad=("PCSX.settings.pads[1].DeviceType='Analog'\n"
           "PCSX.settings.pads[1].Connected=true\n"
           "PCSX.SIO0.slots[1].pads[1].map()\n"
           "print('AW3_PAD_NO_INPUT=PASS')\n")
      env=env0.copy()
      env.update({"HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),
        "XDG_DATA_HOME":str(home/".data"),"XDG_RUNTIME_DIR":str(home/"runtime"),
        "AW3_H6_STATE":str(h6path)})
      stdout=root/"stdout.log";pcsxlog=root/"pcsx.log"
      cmd=["timeout","--signal=INT","--kill-after=10s",f"{TIMEOUT_SECONDS}s",
           a.pcsx_bin,"-noupdate","-debugger","-interpreter",
           "-bios",a.bios,"-iso",a.cue,"-memcard1",str(mcd),
           "-exec",pad,"-dofile",str(lua),"-softgpu",
           "-stdout","-lua_stdout","-logfile",str(pcsxlog),"-run"]
      start=time.monotonic()
      with stdout.open("wb") as f:
        try:proc=subprocess.run(cmd,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT,check=False);rc=proc.returncode
        except Exception as e:rc=255;f.write(("AW3_EXCEPTION="+repr(e)+"\n").encode())
      wall=time.monotonic()-start;maxwall=max(maxwall,wall)
      log=stdout.read_text(encoding="utf-8",errors="replace")
      if pcsxlog.exists():log+="\n"+pcsxlog.read_text(encoding="utf-8",errors="replace")
      rows=parse_results(log);allrows.extend([{**x,"attempt":attempt} for x in rows])
      diagnostics=[z.strip() for z in log.splitlines() if any(k in z for k in ("AW3_","Lua","lua","error","Error","warning","Warning","SaveState","PCSX"))]
      (out/f"AW3_DIAGNOSTIC_ATTEMPT_{attempt}.txt").write_text("\n".join(diagnostics[:120])+"\n",encoding="utf-8")
      final=re.search(r"AW3_FINAL_RAM baseline_sha=(\w+) final_sha=(\w+) unchanged=(\w+)",log)
      done=re.search(r"AW3_DONE calls=(\d+) failed=(\d+) ram_restored=(\w+)",log)
      cardAfter=sha(mcd.read_bytes()) if mcd.exists() else "TIDAK_TAHU"
      launches.append({"attempt":attempt,"exit_code_decimal":rc,
        "timeout_seconds":TIMEOUT_SECONDS,"wall_seconds":f"{wall:.3f}",
        "memory_card_sha256_before":mcdBefore,"memory_card_sha256_after":cardAfter,
        "memory_card_unchanged":str(mcdBefore==cardAfter).upper(),
        "h6_loaded":"YES" if "AW3_H6_LOADED=1" in log else "NO",
        "baseline_ram_sha":final.group(1) if final else "TIDAK_TAHU",
        "final_ram_sha":final.group(2) if final else "TIDAK_TAHU",
        "ram_restored":final.group(3) if final else "TIDAK_TAHU",
        "calls":done.group(1) if done else str(len(rows)),
        "failed_calls":done.group(2) if done else "TIDAK_TAHU",
        "log_path":str(stdout)})
    expected=len(tests())
    call_pass=len(allrows)==expected*2 and all(x.get("status")=="PASS" for x in allrows)
    launches_pass=all(x["exit_code_decimal"]==0 and x["memory_card_unchanged"]=="TRUE"
      and x["h6_loaded"]=="YES" and x["ram_restored"]=="true"
      and int(x["calls"])==expected and int(x["failed_calls"])==0 for x in launches)
    timeout_ok=TIMEOUT_SECONDS>=2*HISTORICAL_MAX_WALL
    complete=call_pass and launches_pass and timeout_ok
    with (out/"AW3_CALL_RESULTS.tsv").open("w",encoding="utf-8",newline="") as f:
      cols=["attempt","label","kind","fn","a0","a1","a2","a3","expected","actual","memory_value",
            "ram_before_sha","ram_after_sha","ram_unchanged","diff_offsets","status"]
      w=csv.DictWriter(f,fieldnames=cols,delimiter="\t",extrasaction="ignore");w.writeheader()
      for x in allrows:w.writerow(x)
    with (out/"AW3_LAUNCHES.tsv").open("w",encoding="utf-8",newline="") as f:
      cols=list(launches[0].keys())
      w=csv.DictWriter(f,fieldnames=cols,delimiter="\t");w.writeheader();w.writerows(launches)
    summary=[
      "AW3 — PCSX-REDUX HEADLESS INTERPRETER; H6 HIBRIDA; CONTROLLED DIRECT CALLS",
      f"H6_SHA256={H6_SHA}",
      "H6_IDENTITY=target checkpoint base + CONTROL top-level protobuf field 6; HIBRIDA, NOT TARGET-PURE",
      "USER_INPUT=NONE; STORY_MODE_ADAPTIVE_PLAYER=NOT_RUN",
      "LAUNCH_MATRIX=two independent H6 reloads, two separately copied Memory Cards",
      "FLAGS=-debugger -interpreter; no dynarec",
      "DIRECT_FUNCTIONS=FUN_800B770C; getter_0x800138EC; setter_0x8001387C",
      "MANAGER_FUN_80109FEC=NOT_CALLED_DIRECTLY; state-machine has UI/audio/state side effects and chained calls; direct call lacks safe isolated preconditions",
      "TILE_HELPER_TEST=selectors 0..4 x three halfword fields/values; selector 5 default path; 31? exact counts in TSV",
      "GETTER_POSITIVE_CONTROL=index 0 and 1; expected 1500 each before any write",
      "SETTER_CONTROL=100,1500,100000,-10000; record +0x18 checked and full record restored",
      "REGISTER_STATE=GPR[0..33] including HI/LO, CP0, CP2D, CP2C, PC saved/restored per call",
      "RAM_HASH=SHA256 first 2MiB before/after and after restore for every call",
      f"EXPECTED_CALLS_PER_LAUNCH={expected}",
      f"OBSERVED_CALLS={len(allrows)}",
      f"HISTORICAL_MAX_WALL_SECONDS={HISTORICAL_MAX_WALL:.3f}",
      f"MAX_LAUNCH_WALL_SECONDS={maxwall:.3f}",
      f"TIMEOUT_SECONDS_PER_LAUNCH={TIMEOUT_SECONDS}",
      f"TIMEOUT_GE_2X_HISTORICAL_MAX={timeout_ok}",
      f"ALL_TESTS_PASS={complete}",
    ]
    for x in launches:summary.append(
      f"ATTEMPT={x['attempt']} EXIT_DECIMAL={x['exit_code_decimal']} WALL={x['wall_seconds']} "
      f"H6_LOADED={x['h6_loaded']} MCD_UNCHANGED={x['memory_card_unchanged']} "
      f"RAM_RESTORED={x['ram_restored']} CALLS={x['calls']} FAILED={x['failed_calls']}")
    (out/"AW3_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    rc=0 if complete else 2
    (out/"AW3_SCRIPT_EXIT_CODE.txt").write_text(f"AW3_SCRIPT_EXIT_CODE={rc}\n",encoding="utf-8")
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text("\n".join([
      f"STATUS={'PASS' if complete else 'INCOMPLETE'}",
      "JOB=aw3-controlled-helper-call-interpreter",
      f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
      f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",
      f"H6_SHA256={H6_SHA}",f"EXIT_CODE={rc}",
      f"CALLS={len(allrows)}",f"TIMEOUT_SECONDS={TIMEOUT_SECONDS}",
      f"TIMEOUT_GE_2X_OBSERVED_MAX={timeout_ok}"])+"\n",encoding="utf-8")
    return rc

if __name__=="__main__":raise SystemExit(main())
