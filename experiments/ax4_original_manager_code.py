#!/usr/bin/env python3
"""AX4: run original MIPS slices under PCSX-Redux interpreter on two H6 launches.
Lua prepares registers/memory and captures live setter arguments only; MIPS computes a1.
"""
from __future__ import annotations
import argparse,csv,hashlib,os,shutil,subprocess,time
from pathlib import Path
from aj2_h6_ram_probe import one,replace_top,encmsg
TARGET_SHA="00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA="9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA="d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
MCD_SHA="ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5"
TIMEOUT_SECONDS=600
HISTORICAL_MAX_WALL_SECONDS=241.088
RAM_SIZE=0x200000
PLAYER_BASE=0x80070EA0
MANAGER_SLOT=0x8013A554
SENTINEL=0x801FFFE0

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def cases():
    return [{"entry":pc,"label":f"{tag}_B44_{v}","b44":v}
      for pc,tag in ((0x8010A140,"A140"),(0x8010A5EC,"A5EC")) for v in (0,7,25)]

def lua_source():
    table=",\n".join('  {entry=0x%08X,label="%s",b44=%d}'%(x["entry"],x["label"],x["b44"]) for x in cases())
    return r"""
if io.stdout then io.stdout:setvbuf("no") end
local ffi=require("ffi"); local bit=require("bit")
ffi.cdef[[typedef unsigned int ax4_u32; unsigned char *SHA256(const unsigned char *d,unsigned long n,unsigned char *md);]]
local cryptoOk,crypto=pcall(ffi.load,"crypto")
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
local function fail(tag,e) log("AX4_FATAL tag="..tag.." detail="..tostring(e)); pcall(function() PCSX.quit(94) end) end
if not cryptoOk then fail("OPENSSL_LOAD",crypto); return end
local mem=PCSX.getMemPtr(); local RAM_SIZE=0x200000
local PLAYER_BASE=0x80070EA0; local MANAGER_SLOT=0x8013A554; local SENTINEL=0x801FFFE0
local cardPath=os.getenv("AX4_MCD_PATH")
local cases={
__AX4_CASES__
}
local post=0; local preloadTicks=0; local started=false; local loaded=false; local running=false
local managerBase=nil; local baselineRam=nil; local baselineSha=nil; local originalRegs=nil
local currentCase=nil; local currentBeforeSha=nil; local currentCardBefore=nil; local currentStartClock=nil
local setterObservation=nil; local callRows=0; local failedCalls=0; local bpKeep={}
local function phys(a) return bit.band(a,0x1fffffff) end
local function rd32(a) return tonumber(ffi.cast("ax4_u32*",mem+phys(a))[0]) end
local function wr8(a,v) mem[phys(a)]=v%256 end
local function wr32(a,v) ffi.cast("ax4_u32*",mem+phys(a))[0]=v end
local function ramString() return ffi.string(mem,RAM_SIZE) end
local function digest(s)
 local o=ffi.new("unsigned char[32]"); crypto.SHA256(ffi.cast("const unsigned char*",s),#s,o)
 return (ffi.string(o,32):gsub(".",function(c)return string.format("%02x",string.byte(c))end))
end
local function ramSha()
 local o=ffi.new("unsigned char[32]"); crypto.SHA256(ffi.cast("const unsigned char*",mem),RAM_SIZE,o)
 return (ffi.string(o,32):gsub(".",function(c)return string.format("%02x",string.byte(c))end))
end
local function cardSha()
 if not cardPath then error("AX4_MCD_PATH missing") end
 local f=assert(io.open(cardPath,"rb")); local s=f:read("*a"); f:close(); return digest(s)
end
local function s32(v) v=tonumber(v); if v>=0x80000000 then return v-0x100000000 end; return v end
local function saveRegs()
 local r=PCSX.getRegisters(); local t={pc=tonumber(r.pc),g={},cp0={},cp2d={},cp2c={}}
 for i=0,33 do t.g[i]=tonumber(r.GPR.r[i]) end
 for i=0,31 do t.cp0[i]=tonumber(r.CP0.r[i]); t.cp2d[i]=tonumber(r.CP2D.r[i]); t.cp2c[i]=tonumber(r.CP2C.r[i]) end
 return t
end
local function restoreRegs(t)
 local r=PCSX.getRegisters()
 for i=0,33 do r.GPR.r[i]=t.g[i] end
 for i=0,31 do r.CP0.r[i]=t.cp0[i]; r.CP2D.r[i]=t.cp2d[i]; r.CP2C.r[i]=t.cp2c[i] end
 r.pc=t.pc
end
local startNext
startNext=function(i)
 if i>#cases then
  ffi.copy(mem,baselineRam,RAM_SIZE); restoreRegs(originalRegs)
  local finalSha=ramSha(); local unchanged=(finalSha==baselineSha)
  log("AX4_FINAL_RAM baseline_sha="..baselineSha.." final_sha="..finalSha.." unchanged="..tostring(unchanged))
  log("AX4_DONE calls="..callRows.." failed="..failedCalls.." ram_restored="..tostring(unchanged))
  PCSX.quit((failedCalls==0 and unchanged and callRows==#cases) and 0 or 93); return
 end
 local t=cases[i]; currentCase=t; setterObservation=nil
 -- Set manager state only; do not calculate or inject the setter's a1.
 wr8(managerBase+0xB2A,7); wr8(managerBase+0xB2B,0); wr32(managerBase+0xB44,t.b44)
 currentBeforeSha=ramSha(); currentCardBefore=cardSha(); currentStartClock=os.clock()
 local sbp=PCSX.addBreakpoint(SENTINEL,"Exec",4,"AX4 setter return",function()
  PCSX.pauseEmulator()
  PCSX.nextTick(function()
   local obs=setterObservation
   if not obs then fail("SENTINEL_WITHOUT_SETTER","setter breakpoint not observed"); return end
   local afterSha=ramSha(); local cardAfter=cardSha()
   local stored=s32(rd32(PLAYER_BASE+0x18)); local b44After=s32(rd32(managerBase+0xB44))
   local setterReturn=s32(PCSX.getRegisters().GPR.n.v0); local duration=os.clock()-currentStartClock
   ffi.copy(mem,baselineRam,RAM_SIZE); restoreRegs(originalRegs)
   local restoredSha=ramSha(); local restored=(restoredSha==baselineSha)
   local status=(restored and cardAfter==currentCardBefore and obs.setter_pc=="0x8001387C" and setterReturn==1) and "CAPTURED" or "FAIL"
   if status=="FAIL" then failedCalls=failedCalls+1 end
   callRows=callRows+1
   log(table.concat({"AX4_CALL",t.label,
    "entry="..string.format("0x%08X",t.entry),"b44_before="..tostring(t.b44),
    "q_before="..tostring(obs.q_before),"setter_a0="..obs.setter_a0,"setter_a1="..tostring(obs.setter_a1),
    "setter_entry_pc="..obs.setter_pc,"setter_return="..tostring(setterReturn),"stored_chakra="..tostring(stored),
    "b44_after="..tostring(b44After),"ram_before_sha="..currentBeforeSha,"ram_after_sha="..afterSha,
    "ram_restored_sha="..restoredSha,"ram_restored="..tostring(restored),
    "mcd_before_sha="..currentCardBefore,"mcd_after_sha="..cardAfter,"mcd_unchanged="..tostring(cardAfter==currentCardBefore),
    "duration_seconds="..string.format("%.6f",duration),"status="..status},"|"))
   currentCase=nil; setterObservation=nil
   PCSX.nextTick(function() startNext(i+1) end)
  end)
  return true
 end)
 if not sbp then fail("SENTINEL_BP_ADD","cannot install sentinel"); return end
 bpKeep[#bpKeep+1]=sbp

 -- One-shot entry breakpoint observes live a1, then resumes the ORIGINAL setter.
 local ebp=PCSX.addBreakpoint(0x8001387C,"Exec",4,"AX4 live setter a1",function()
  PCSX.pauseEmulator()
  local ok,e=pcall(function()
   local r=PCSX.getRegisters()
   setterObservation={q_before=s32(r.GPR.n.v0),setter_a0=string.format("0x%08X",tonumber(r.GPR.n.a0)),
    setter_a1=s32(r.GPR.n.a1),setter_pc=string.format("0x%08X",tonumber(r.pc))}
   r.GPR.n.ra=SENTINEL
  end)
  if not ok then fail("SETTER_BREAKPOINT",e); return true end
  log("AX4_SETTER_ENTRY label="..t.label.." q_before="..tostring(setterObservation.q_before)..
   " a0="..setterObservation.setter_a0.." a1_live="..tostring(setterObservation.setter_a1))
  PCSX.nextTick(function() PCSX.resumeEmulator() end)
  return true
 end)
 if not ebp then fail("SETTER_BP_ADD","cannot install 0x8001387C"); return end
 bpKeep[#bpKeep+1]=ebp

 local r=PCSX.getRegisters()
 for j=0,33 do r.GPR.r[j]=originalRegs.g[j] end
 for j=0,31 do r.CP0.r[j]=originalRegs.cp0[j]; r.CP2D.r[j]=originalRegs.cp2d[j]; r.CP2C.r[j]=originalRegs.cp2c[j] end
 r.GPR.n.ra=SENTINEL; r.GPR.n.s1=0x80140000
 if t.entry==0x8010A140 then r.GPR.n.a0=managerBase else r.GPR.n.v0=managerBase end
 r.pc=t.entry
 log("AX4_CALL_BEGIN label="..t.label.." entry="..string.format("0x%08X",t.entry)..
  " B44="..t.b44.." RAM_BEFORE="..currentBeforeSha.." MCD_BEFORE="..currentCardBefore)
 PCSX.resumeEmulator()
end
_G.ax4Loaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function() loaded=true; post=0; log("AX4_H6_LOADED=1") end)
_G.ax4Vsync=PCSX.Events.createEventListener("GPU::Vsync",function()
 if not started then
  started=true; PCSX.pauseEmulator()
  PCSX.nextTick(function()
   local p=os.getenv("AX4_H6_STATE") or "resume/h6-hybrid.sstate"
   local okf,f=pcall(function()return assert(Support.File.open(p))end)
   if not okf or not f then fail("STATE_OPEN",f); return end
   local ok,e=pcall(function()PCSX.loadSaveState(f)end); f:close()
   if not ok then fail("STATE_LOAD",e); return end
   log("AX4_H6_LOAD_CALL_RETURNED=1"); PCSX.resumeEmulator()
  end); return
 end
 if loaded then
  post=post+1
  if post==180 and not running then
   running=true; PCSX.pauseEmulator()
   PCSX.nextTick(function()
    local ok,e=pcall(function()
     managerBase=rd32(MANAGER_SLOT)
     if managerBase<0x80000000 or managerBase+0xB48>0x80200000 then error(string.format("manager pointer invalid 0x%08X",managerBase)) end
     originalRegs=saveRegs(); baselineRam=ramString(); baselineSha=ramSha()
     local q0=s32(rd32(PLAYER_BASE+0x18))
     log(string.format("AX4_BASELINE frame=180 manager=0x%08X manager_B44=%d player0_chakra=%d RAM_SHA=%s",
      managerBase,s32(rd32(managerBase+0xB44)),q0,baselineSha))
     if q0~=1500 then error("participant0 field +0x18 precondition is not 1500") end
     startNext(1)
    end)
    if not ok then fail("START_TESTS",e) end
   end
 elseif started then
  preloadTicks=preloadTicks+1
  if preloadTicks>600 then fail("SAVE_STATE_LOADED_EVENT_TIMEOUT","GPU vsync >600 without SaveStateLoaded"); return end
 end
end)
log("AX4_READY interpreter=1 debugger=1 INPUT=NONE H6=HIBRIDA")
""".replace("__AX4_CASES__",table)

def parse_rows(s:str):
    rows=[]
    for line in s.splitlines():
        if "AX4_CALL|" not in line: continue
        p=line[line.index("AX4_CALL|"):].strip().split("|")
        if len(p)<3: continue
        d={"label":p[1]}
        for item in p[2:]:
            if "=" in item:
                k,v=item.split("=",1); d[k]=v
        rows.append(d)
    return rows

def main():
    ap=argparse.ArgumentParser()
    for n in ("target","control","pcsx-bin","appdir","bios","cue","card","work","out"): ap.add_argument("--"+n,required=True)
    a=ap.parse_args()
    target=Path(a.target).read_bytes(); control=Path(a.control).read_bytes()
    if sha(target)!=TARGET_SHA: raise SystemExit("TARGET_SSTATE_SHA_MISMATCH")
    if sha(control)!=CONTROL_SHA: raise SystemExit("CONTROL_SSTATE_SHA_MISMATCH")
    h6=replace_top(target,6,encmsg(6,one(control,6)))
    if sha(h6)!=H6_SHA: raise SystemExit("H6_HYBRID_SHA_MISMATCH")
    card=Path(a.card).read_bytes()
    if len(card)!=131072 or sha(card)!=MCD_SHA: raise SystemExit("MEMCARD_IDENTITY_MISMATCH")
    work,out=Path(a.work),Path(a.out); out.mkdir(parents=True,exist_ok=True)
    for d in ("resume","launches"): (work/d).mkdir(parents=True,exist_ok=True)
    h6path=work/"resume"/"h6-hybrid.sstate"; h6path.write_bytes(h6)
    app=Path(a.appdir); env0=os.environ.copy()
    env0.update({"DISPLAY":":99","LIBGL_ALWAYS_SOFTWARE":"1",
     "LD_LIBRARY_PATH":str(app/"usr/lib")+":"+str(app/"usr/lib/x86_64-linux-gnu"),
     "QT_PLUGIN_PATH":str(app/"usr/plugins"),"QT_QPA_PLATFORM_PLUGIN_PATH":str(app/"usr/plugins/platforms"),
     "QML2_IMPORT_PATH":str(app/"usr/qml")})
    launches=[]; allrows=[]; maxwall=0.0
    for attempt in (1,2):
        root=work/"launches"/f"attempt-{attempt}"; home=root/"home"; runtime=root/"runtime"
        for d in (runtime,home/".config",home/".data",home/"runtime"): d.mkdir(parents=True,exist_ok=True)
        try: (home/"runtime").chmod(0o700)
        except OSError: pass
        mcd=root/"memory-card.mcd"; shutil.copyfile(a.card,mcd); mcd_before=sha(mcd.read_bytes())
        lua=root/"ax4.lua"; lua.write_text(lua_source(),encoding="utf-8")
        pad=("PCSX.settings.pads[1].DeviceType='Analog'\nPCSX.settings.pads[1].Connected=true\n"
             "PCSX.SIO0.slots[1].pads[1].map()\nprint('AX4_PAD_NO_INPUT=PASS')\n")
        env=env0.copy()
        env.update({"HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),"XDG_DATA_HOME":str(home/".data"),
         "XDG_RUNTIME_DIR":str(home/"runtime"),"AX4_H6_STATE":str(h6path),"AX4_MCD_PATH":str(mcd)})
        stdout=root/"stdout.log"; pcsxlog=root/"pcsx.log"
        cmd=["timeout","--signal=INT","--kill-after=10s",f"{TIMEOUT_SECONDS}s",a.pcsx_bin,
         "-noupdate","-debugger","-interpreter","-bios",a.bios,"-iso",a.cue,"-memcard1",str(mcd),
         "-exec",pad,"-dofile",str(lua),"-softgpu","-stdout","-lua_stdout","-logfile",str(pcsxlog),"-run"]
        start=time.monotonic()
        with stdout.open("wb") as f:
            try: proc=subprocess.run(cmd,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT,check=False); rc=proc.returncode
            except Exception as e: rc=255; f.write(("AX4_EXCEPTION="+repr(e)+"\n").encode())
        wall=time.monotonic()-start; maxwall=max(maxwall,wall)
        log=stdout.read_text(encoding="utf-8",errors="replace")
        if pcsxlog.exists(): log+="\n"+pcsxlog.read_text(encoding="utf-8",errors="replace")
        rows=parse_rows(log)
        allrows.extend([{**x,"attempt":attempt,"emulator_exit_code_decimal":rc,"launch_wall_seconds":f"{wall:.3f}"} for x in rows])
        diag=[z.strip() for z in log.splitlines() if any(k in z for k in ("AX4_","Lua","lua","error","Error","warning","Warning","SaveState","PCSX"))]
        (out/f"AX4_DIAGNOSTIC_ATTEMPT_{attempt}.txt").write_text("\n".join(diag[:200])+"\n",encoding="utf-8")
        card_after=sha(mcd.read_bytes()) if mcd.exists() else "TIDAK_TAHU"
        launches.append({"attempt":attempt,"emulator_exit_code_decimal":rc,"timeout_seconds":TIMEOUT_SECONDS,
         "wall_seconds":f"{wall:.3f}","memory_card_sha256_before_launch":mcd_before,
         "memory_card_sha256_after_launch":card_after,"memory_card_unchanged":str(mcd_before==card_after).upper(),
         "h6_loaded":"YES" if "AX4_H6_LOADED=1" in log else "NO","calls":len(rows),
         "done":"YES" if "AX4_DONE calls=6 failed=0 ram_restored=true" in log else "NO",
         "h6_hybrid_sha256":H6_SHA,"log_path":str(stdout)})
    verified=[]
    for x in allrows:
        try:
            entry=int(x["entry"],16); b44=int(x["b44_before"]); q=int(x["q_before"])
            actual=int(x["setter_a1"]); stored=int(x["stored_chakra"])
            delta=b44 if entry==0x8010A140 else min(b44,0x14)
            expected=q+delta; expectedStore=max(-9999,min(99999,actual))
            ok=(actual==expected and stored==expectedStore and x.get("status")=="CAPTURED" and
             int(x.get("setter_return","-999"))==1 and x.get("ram_restored")=="true" and
             x.get("mcd_unchanged")=="true" and x.get("setter_a0")=="0x00000000")
            verified.append({**x,"expected_a1_posthoc":expected,"a1_matches_static_expression":str(actual==expected).upper(),
             "expected_stored_from_observed_a1":expectedStore,"stored_matches_observed_a1":str(stored==expectedStore).upper(),
             "verification":"PASS" if ok else "FAIL"})
        except Exception as e: verified.append({**x,"verification":"FAIL","verification_error":repr(e)})
    timeout_ok=TIMEOUT_SECONDS>=2*HISTORICAL_MAX_WALL_SECONDS and all(TIMEOUT_SECONDS>=2*float(x["wall_seconds"]) for x in launches)
    launch_ok=all(x["emulator_exit_code_decimal"]==0 and x["memory_card_unchanged"]=="TRUE" and x["h6_loaded"]=="YES" and x["calls"]==6 and x["done"]=="YES" for x in launches)
    calls_ok=len(verified)==12 and all(x["verification"]=="PASS" for x in verified)
    complete=timeout_ok and launch_ok and calls_ok
    cols=["attempt","label","entry","b44_before","q_before","expected_a1_posthoc","setter_a0","setter_a1",
     "a1_matches_static_expression","setter_entry_pc","setter_return","stored_chakra","expected_stored_from_observed_a1",
     "stored_matches_observed_a1","b44_after","ram_before_sha","ram_after_sha","ram_restored_sha","ram_restored",
     "mcd_before_sha","mcd_after_sha","mcd_unchanged","duration_seconds","emulator_exit_code_decimal",
     "launch_wall_seconds","status","verification"]
    with (out/"AX4_CALL_RESULTS.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,delimiter="\t",extrasaction="ignore"); w.writeheader(); w.writerows(verified)
    with (out/"AX4_LAUNCHES.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(launches[0].keys()),delimiter="\t"); w.writeheader(); w.writerows(launches)
    summary=["AX4 — ORIGINAL MIPS EXECUTION; PCSX-REDUX INTERPRETER; H6 HYBRID (NOT TARGET-PURE)",
     f"H6_SHA256={H6_SHA}","ORIGINAL_CODE_RANGES=0x8010A140-0x8010A160;0x8010A5EC-0x8010A63C",
     "A1_METHOD=one-shot breakpoint at 0x8001387C captures live GPR a1; Lua never computes or sets a1",
     "ENTRY_SETUP=manager B2A=7; B2B=0; B44=0,7,25; original getter computes Q and returns it in v0",
     "MATRIX=two independent emulator launches; each runs both original code ranges for B44=0,7,25",
     "RESTORE=full 2MiB RAM SHA baseline and GPR/CP0/CP2D/CP2C/PC restored after every call",
     "MCD_SHA=launch-local Memory Card file SHA immediately before/after each call and at launch end",
     f"TIMEOUT_SECONDS_PER_LAUNCH={TIMEOUT_SECONDS}",f"HISTORICAL_MAX_WALL_SECONDS={HISTORICAL_MAX_WALL_SECONDS:.3f}",
     f"MAX_LAUNCH_WALL_SECONDS={maxwall:.3f}",f"TIMEOUT_GE_2X_LONGEST={timeout_ok}",
     f"OBSERVED_CALLS={len(verified)}",f"ALL_CALLS_PASS={calls_ok}",f"ALL_LAUNCHES_PASS={launch_ok}",f"ALL_TESTS_PASS={complete}"]
    for x in launches:
        summary.append(f"ATTEMPT={x['attempt']} EXIT_DECIMAL={x['emulator_exit_code_decimal']} WALL={x['wall_seconds']} H6_LOADED={x['h6_loaded']} MCD_UNCHANGED={x['memory_card_unchanged']} CALLS={x['calls']} DONE={x['done']}")
    (out/"AX4_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    rc=0 if complete else 2
    (out/"AX4_SCRIPT_EXIT_CODE.txt").write_text(f"AX4_SCRIPT_EXIT_CODE={rc}\n",encoding="utf-8")
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text("\n".join([f"STATUS={'PASS' if complete else 'INCOMPLETE'}",
     "JOB=ax4-original-manager-code",f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
     f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",f"H6_SHA256={H6_SHA}",f"EXIT_CODE={rc}",
     f"CALLS={len(verified)}",f"TIMEOUT_SECONDS={TIMEOUT_SECONDS}",f"TIMEOUT_GE_2X_LONGEST={timeout_ok}"])+"\n",encoding="utf-8")
    return rc
if __name__=="__main__": raise SystemExit(main())
