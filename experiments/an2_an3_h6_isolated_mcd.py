#!/usr/bin/env python3
"""AN2/AN3: H6 C/A/B replay with independent Memory Card copies and byte diffs."""
import argparse, csv, hashlib, os, re, shutil, subprocess, time
from pathlib import Path
from aj2_h6_ram_probe import one, replace_top, encmsg

TARGET="00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL="9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6="d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
CARD="ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5"
CARD_SIZE=131072
RAM_SIZE=0x200000
BASE=0x80000000
FRAMES=(1,60,180,240,360)
DIFF_FRAMES=(180,240,360)
ADDRS=(0x80070EB8,0x80070F6C,0x800A3118,0x8013A554,0x80066E7C)
NAMES={0x80070EB8:"chakra_0",0x80070F6C:"chakra_1",0x800A3118:"rng_0x800A3118",
       0x8013A554:"slot_0x8013A554",0x80066E7C:"word_0x80066E7C"}
LABEL_RANGES=(("CHAKRA",0x80070EB8,4),("CHAKRA",0x80070F6C,4),
 ("RNG",0x800A3118,4),("SLOT_0x8013A554",0x8013A554,4),
 ("BLOCK_0x801CEF08",0x801CEF08,0x1C),("0x80066E7C",0x80066E7C,4))
LABELS=("CHAKRA","RNG","SLOT_0x8013A554","BLOCK_0x801CEF08","0x80066E7C")

def sha(b): return hashlib.sha256(b).hexdigest()
def ram2m(state):
    ram=one(one(state,3),1)
    if len(ram)<RAM_SIZE: raise ValueError("decoded RAM shorter than first 2 MiB")
    return ram[:RAM_SIZE],len(ram)
def words(ram):
    d={}
    for a in ADDRS:
        raw=ram[a-BASE:a-BASE+4]
        if len(raw)!=4: raise ValueError("word outside hashed RAM: "+hex(a))
        d[a]=(hex(int.from_bytes(raw,"little")),raw.hex())
    return d
def schedule_read(path):
    d={}
    with open(path,encoding="utf-8",newline="") as f:
        for r in csv.DictReader(f,delimiter="\t"):
            n=r["schedule"]; p=int(r["press_frame"]); q=int(r["release_frame"])
            if n in d or int(r["launch_count"])!=2: raise ValueError("bad schedule "+str(r))
            if n=="C":
                if r["button"]!="NONE" or p!=0 or q!=0: raise ValueError("C must be no-input")
                d[n]=None
            else:
                if n not in ("A","B") or r["button"]!="CIRCLE" or q!=p+1: raise ValueError("bad Circle schedule")
                d[n]=p
    if d!={"C":None,"A":60,"B":90}: raise ValueError("expected C/A/B schedules, got "+str(d))
    return d

def lua(when,press):
    p=press or 0
    return f'''if io.stdout then io.stdout:setvbuf("no") end
local begun,loaded,after=false,false,0
local epoch=tonumber(os.getenv("AN2_START_EPOCH")) or os.time()
local schedule="{when}"
local pressFrame={p}
local pad=PCSX.SIO0.slots[1].pads[1]
local circle=PCSX.CONSTS.PAD.BUTTON.CIRCLE
local done,pending={{}},{{}}
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
local function input(phase)
 local ok,value=pcall(function()
  if phase=="press" then pad.setOverride(circle) else pad.clearOverride(circle) end
  return pad.getButton(circle)
 end)
 local pass=ok and value==(phase=="press")
 log("AN2_INPUT schedule="..schedule.." phase="..phase.." frame="..after.." readback="..tostring(value).." status="..(pass and "PASS" or "FAIL"))
 if not pass then PCSX.quit(83) end
end
local function capture(target)
 local ok,err=pcall(function()
  local state=PCSX.createSaveState()
  local f=assert(Support.File.open("runtime/frame"..target..".sstate","TRUNCATE"))
  f:writeMoveSlice(state); f:close()
 end)
 if not ok then log("AN2_CAPTURE_FRAME="..target.."=FAIL "..tostring(err)); PCSX.quit(62); return end
 log("AN2_CAPTURE_FRAME="..target.."=PASS")
 if target==360 then
  log("AN2_QUIT0_DIRECT_BEGIN=1")
  local qok,qerr=pcall(function() PCSX.quit(0) end)
  log("AN2_QUIT0_DIRECT_RETURNED="..tostring(qok).." "..tostring(qerr))
 end
end
_G.an2Load=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
 loaded=true; after=0; log("AN2_LOAD_EVENT=PASS")
end)
_G.an2Vsync=PCSX.Events.createEventListener("GPU::Vsync",function()
 if not begun then
  begun=true
  local path=os.getenv("AN2_STATE_PATH") or "resume/h6.sstate"
  log("AN2_LOAD_BEGIN path="..path.." input=NONE")
  PCSX.pauseEmulator()
  PCSX.nextTick(function()
   local ok,f=pcall(function() return assert(Support.File.open(path)) end)
   if not ok or not f then log("AN2_STATE_OPEN_FAIL "..tostring(f)); PCSX.quit(50); return end
   local good,err=pcall(function() PCSX.loadSaveState(f) end); f:close()
   if not good then log("AN2_LOAD_FAIL "..tostring(err)); PCSX.quit(51); return end
   log("AN2_LOAD_CALL_RETURNED=1"); PCSX.resumeEmulator()
  end)
  return
 end
 if not loaded then return end
 after=after+1
 if pressFrame>0 then
  if after==pressFrame then input("press") end
  if after==pressFrame+1 then input("release") end
 end
 for _,target in ipairs({{1,60,180,240,360}}) do
  if after>=target and not done[target] and not pending[target] then
   pending[target]=true
   log("AN2_POST_LOAD_FRAME="..target.." elapsed="..tostring(os.time()-epoch))
   local t=target
   PCSX.nextTick(function() capture(t); done[t]=true end)
  end
 end
 if after>=1200 then log("AN2_WATCHDOG=1"); PCSX.quit(53) end
end)
log("AN2_READY schedule="..schedule.." press="..p.." release="..(p>0 and p+1 or 0))
'''

def emu_exit(log):
    m=re.search(r"Inferior\s+\d+.*?exited with code\s+([0-7]+)",log,re.I)
    if m: return str(int(m.group(1),8)),"GDB inferior exit status (octal converted to decimal)"
    if re.search(r"Inferior\s+\d+.*?exited normally",log,re.I): return "0","GDB inferior exited normally"
    m=re.search(r"Program exited with code\s+([0-7]+)",log,re.I)
    if m: return str(int(m.group(1),8)),"GDB program exit status (octal converted to decimal)"
    if re.search(r"Program exited normally",log,re.I): return "0","GDB program exited normally"
    return "TIDAK TAHU","no explicit GDB exit status"

def run_one(name,attempt,press,args,env,work,card_sha):
    tag=f"{name}-attempt{attempt}"
    root=work/"launches"/tag; rt=root/"runtime"; home=root/"home"
    for p in (rt,home/".config",home/".data",home/"runtime"): p.mkdir(parents=True,exist_ok=True)
    try: (home/"runtime").chmod(0o700)
    except OSError: pass
    card=root/"launch.mcd"; shutil.copyfile(args.card,card)
    before=sha(card.read_bytes())
    if before!=card_sha: raise ValueError(tag+" MCD baseline mismatch")
    script=root/"run.lua"; script.write_text(lua(name,press),encoding="utf-8")
    pad=root/"pad.lua"; pad.write_text("PCSX.settings.pads[1].DeviceType='Analog'\nPCSX.settings.pads[1].Connected=true\nPCSX.SIO0.slots[1].pads[1].map()\nprint('AN2_PAD_READY=PASS')\n",encoding="utf-8")
    glog=work/"logs"/(tag+".gdb.txt"); plog=work/"logs"/(tag+".pcsx.txt")
    gcmd=root/"gdb.commands"
    gcmd.write_text("""set pagination off
set confirm off
set print thread-events off
handle SIGSEGV stop print nopass
handle SIGABRT stop print nopass
run
python
import gdb
i=gdb.selected_inferior()
if getattr(i,'pid',0):
 print('AN2_GDB_CONTEXT_BEGIN')
 for c in ('info threads','x/3i $pc','info registers','bt','thread apply all bt 20'):
  try:gdb.execute(c)
  except Exception as e:print('AN2_GDB_COMMAND_ERROR '+str(e))
 print('AN2_GDB_CONTEXT_END')
 try:gdb.execute('continue')
 except Exception as e:print('AN2_GDB_CONTINUE '+str(e))
else: print('AN2_GDB_INFERIOR_ALREADY_EXITED')
end
""",encoding="utf-8")
    e=env.copy(); e.update({"HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),
      "XDG_DATA_HOME":str(home/".data"),"XDG_RUNTIME_DIR":str(home/"runtime"),
      "AN2_STATE_PATH":str(work/"resume"/"h6.sstate"),"AN2_START_EPOCH":str(time.time())})
    cmd=["timeout","--signal=INT","--kill-after=5s",str(args.timeout)+"s","gdb","--quiet","--nx","--batch","--return-child-result","-x",str(gcmd),
      "--args",args.pcsx_bin,"-noupdate","-no-debugger","-no-gdb","-bios",args.bios,"-iso",args.cue,"-memcard1",str(card),
      "-exec",pad.read_text(encoding="utf-8"),"-dofile",str(script),"-softgpu","-dynarec","-stdout","-lua_stdout","-logfile",str(plog),"-run"]
    start=time.monotonic()
    with glog.open("wb") as f:
        try: wrapper=subprocess.run(cmd,cwd=root,env=e,stdout=f,stderr=subprocess.STDOUT,check=False).returncode
        except Exception as ex: wrapper=255; f.write(repr(ex).encode())
    wall=time.monotonic()-start
    gt=glog.read_text(encoding="utf-8",errors="replace")
    pt=plog.read_text(encoding="utf-8",errors="replace") if plog.exists() else ""
    both=gt+"\n"+pt; exitcode,source=emu_exit(both); watchdog="AN2_WATCHDOG=1" in both
    pressok=name=="C" or bool(re.search(r"AN2_INPUT schedule="+name+r" phase=press .*status=PASS",both))
    releaseok=name=="C" or bool(re.search(r"AN2_INPUT schedule="+name+r" phase=release .*status=PASS",both))
    after=sha(card.read_bytes()) if card.exists() else "TIDAK TAHU"
    rows=[]; ram_by_frame={}
    for frame in FRAMES:
        state=rt/f"frame{frame}.sstate"
        m=re.search(rf"AN2_POST_LOAD_FRAME={frame} elapsed=([0-9.]+)",gt)
        ok=f"AN2_CAPTURE_FRAME={frame}=PASS" in gt and bool(m) and state.is_file()
        status="PASS" if ok else "TIDAK ADA CAPTURE"
        digest="TIDAK TAHU"; segment=0; w={}
        if ok:
            try:
                ram,segment=ram2m(state.read_bytes()); digest=sha(ram); w=words(ram); ram_by_frame[frame]=ram
            except Exception: status="PARSE_ERROR"
        row={"schedule":name,"attempt":attempt,"frame":frame,"capture_status":status,
          "time_to_frame_s":m.group(1) if m else "TIDAK TAHU","ram_first_2mib_sha256":digest,"ram_segment_bytes":segment,
          "gdb_wrapper_exit_code":wrapper,"emulator_exit_code_decimal":exitcode,"emulator_exit_code_source":source,
          "watchdog_seen":str(watchdog).upper(),"circle_press_readback":("NOT_APPLICABLE" if name=="C" else "PASS" if pressok else "FAIL"),
          "circle_release_readback":("NOT_APPLICABLE" if name=="C" else "PASS" if releaseok else "FAIL"),
          "mcd_sha256_before":before,"mcd_sha256_after":after,"mcd_changed":("YES" if before!=after else "NO"),
          "mcd_bytes_after":card.stat().st_size if card.exists() else 0,"wall_seconds":f"{wall:.3f}"}
        for a in ADDRS:
            row[NAMES[a]]=w.get(a,("TIDAK TAHU",""))[0]
            row[NAMES[a]+"_bytes"]=w.get(a,("","TIDAK TAHU"))[1]
        rows.append(row)
    meta={"schedule":name,"attempt":attempt,"mcd_before":before,"mcd_after":after,
      "mcd_bytes_after":card.stat().st_size if card.exists() else 0,"wrapper_exit":wrapper,
      "exit":exitcode,"exit_source":source,"watchdog":watchdog,"pressok":pressok,"releaseok":releaseok,
      "frame360":next((x["time_to_frame_s"] for x in rows if x["frame"]==360),"TIDAK TAHU")}
    return rows,meta,ram_by_frame

def label(address):
    for n,start,length in LABEL_RANGES:
        if start<=address<start+length: return n
    return "TIDAK_TAHU"

def make_diff(left,right,attempt,frame,a,b):
    pos=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
    groups=[]
    for x in pos:
        if not groups or x-groups[-1][-1]-1>32: groups.append([x])
        else: groups[-1].append(x)
    counts={x:0 for x in LABELS}; unknown=0
    for x in pos:
        n=label(BASE+x)
        if n=="TIDAK_TAHU": unknown+=1
        else: counts[n]+=1
    comp=f"{left}_vs_{right}_attempt{attempt}"
    rows=[{"record_type":"SUMMARY","group_index":0,"comparison":comp,"attempt":attempt,"frame":frame,
      "start_address":"","end_address_inclusive":"","span_bytes":0,"changed_bytes_in_range":len(pos),
      "total_diff_bytes":len(pos),**counts,"TIDAK_TAHU":unknown,
      "label_plus_unknown_equals_total":sum(counts.values())+unknown==len(pos),"group_gap_rule":"unchanged gap <= 32"}]
    for i,g in enumerate(groups,1):
        c={x:0 for x in LABELS}; u=0
        for x in g:
            n=label(BASE+x)
            if n=="TIDAK_TAHU": u+=1
            else: c[n]+=1
        lo,hi=g[0],g[-1]
        rows.append({"record_type":"RANGE","group_index":i,"comparison":comp,"attempt":attempt,"frame":frame,
          "start_address":f"0x{BASE+lo:08X}","end_address_inclusive":f"0x{BASE+hi:08X}",
          "span_bytes":hi-lo+1,"changed_bytes_in_range":len(g),"total_diff_bytes":len(pos),
          **c,"TIDAK_TAHU":u,"label_plus_unknown_equals_total":sum(c.values())+u==len(g),
          "group_gap_rule":"unchanged gap <= 32"})
    return rows

def main():
    p=argparse.ArgumentParser()
    for n in ("target","control","pcsx-bin","appdir","bios","cue","card","work","out","schedule"): p.add_argument("--"+n,required=True)
    p.add_argument("--timeout",type=int,default=600); a=p.parse_args()
    work,out=Path(a.work),Path(a.out)
    t,c=Path(a.target).read_bytes(),Path(a.control).read_bytes()
    if sha(t)!=TARGET or sha(c)!=CONTROL: raise SystemExit("target/control SHA mismatch")
    h=replace_top(t,6,encmsg(6,one(c,6)))
    if sha(h)!=H6: raise SystemExit("H6 hybrid SHA mismatch")
    card=Path(a.card).read_bytes()
    if len(card)!=CARD_SIZE or sha(card)!=CARD: raise SystemExit("reference Memory Card size/SHA mismatch")
    sched=schedule_read(a.schedule)
    for q in (work/"resume",work/"logs",work/"launches"): q.mkdir(parents=True,exist_ok=True)
    (work/"resume"/"h6.sstate").write_bytes(h); (work/"resume"/"h6.sstate").chmod(0o400)
    app=Path(a.appdir); env=os.environ.copy()
    env.update({"DISPLAY":":99","LIBGL_ALWAYS_SOFTWARE":"1","LD_LIBRARY_PATH":str(app/"usr/lib")+":"+str(app/"usr/lib/x86_64-linux-gnu"),
      "QT_PLUGIN_PATH":str(app/"usr/plugins"),"QT_QPA_PLATFORM_PLUGIN_PATH":str(app/"usr/plugins/platforms"),"QML2_IMPORT_PATH":str(app/"usr/qml")})
    allrows=[]; metas=[]; memories={}
    for name in ("C","A","B"):
        for attempt in (1,2):
            rows,meta,ram=run_one(name,attempt,sched[name],a,env,work,sha(card))
            allrows.extend(rows); metas.append(meta)
            for frame,data in ram.items(): memories[(name,attempt,frame)]=data
    out.mkdir(parents=True,exist_ok=True)
    with (out/"AN2_CAPTURE_SUMMARY.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(allrows[0]),delimiter="\t"); w.writeheader(); w.writerows(allrows)
    diffs=[]
    for x,y in (("C","A"),("C","B"),("A","B")):
        for attempt in (1,2):
            for frame in DIFF_FRAMES:
                k1=(x,attempt,frame); k2=(y,attempt,frame)
                if k1 in memories and k2 in memories: diffs.extend(make_diff(x,y,attempt,frame,memories[k1],memories[k2]))
                else:
                    diffs.append({"record_type":"SUMMARY","group_index":0,"comparison":f"{x}_vs_{y}_attempt{attempt}",
                      "attempt":attempt,"frame":frame,"start_address":"","end_address_inclusive":"","span_bytes":0,
                      "changed_bytes_in_range":"TIDAK TAHU","total_diff_bytes":"TIDAK TAHU",
                      **{z:"TIDAK TAHU" for z in LABELS},"TIDAK_TAHU":"TIDAK TAHU",
                      "label_plus_unknown_equals_total":False,"group_gap_rule":"unchanged gap <= 32"})
    diffcols=["record_type","group_index","comparison","attempt","frame","start_address","end_address_inclusive","span_bytes",
      "changed_bytes_in_range","total_diff_bytes",*LABELS,"TIDAK_TAHU","label_plus_unknown_equals_total","group_gap_rule"]
    with (out/"AN3_DIFF_RANGES.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=diffcols,delimiter="\t",extrasaction="ignore"); w.writeheader(); w.writerows(diffs)
    summary=["AN2/AN3 H6 hybrid headless PCSX-Redux C/A/B with isolated Memory Cards",f"H6_SHA256={H6}",
      f"REFERENCE_MCD_SHA256={CARD}",f"REFERENCE_MCD_SIZE_BYTES={CARD_SIZE}",
      "H6=target savestate base + SPU top-level field 6 from CONTROL (hybrid, not target-pure)",
      "C=no input; A=CIRCLE frame60 press/release61; B=CIRCLE frame90 press/release91",
      "CAPTURE_FRAMES=1,60,180,240,360","RAM_SHA_COVERAGE=first 2 MiB at 0x80000000",
      "EACH_LAUNCH_USES_SEPARATE_COPY_OF_IDENTICAL_MEMORY_CARD=TRUE"]
    for m in metas:
        n=m["schedule"]; q=m["attempt"]
        summary += [f"{n}_ATTEMPT{q}_MCD_SHA256_BEFORE={m['mcd_before']}",
          f"{n}_ATTEMPT{q}_MCD_SHA256_AFTER={m['mcd_after']}",f"{n}_ATTEMPT{q}_MCD_BYTES_AFTER={m['mcd_bytes_after']}",
          f"{n}_ATTEMPT{q}_MCD_CHANGED={str(m['mcd_before']!=m['mcd_after']).upper()}",
          f"{n}_ATTEMPT{q}_GDB_WRAPPER_EXIT={m['wrapper_exit']}",f"{n}_ATTEMPT{q}_EMULATOR_EXIT_DECIMAL={m['exit']}",
          f"{n}_ATTEMPT{q}_EMULATOR_EXIT_SOURCE={m['exit_source']}",f"{n}_ATTEMPT{q}_WATCHDOG={str(m['watchdog']).upper()}",
          f"{n}_ATTEMPT{q}_CIRCLE_PRESS_READBACK={'NOT_APPLICABLE' if n=='C' else 'PASS' if m['pressok'] else 'FAIL'}",
          f"{n}_ATTEMPT{q}_CIRCLE_RELEASE_READBACK={'NOT_APPLICABLE' if n=='C' else 'PASS' if m['releaseok'] else 'FAIL'}",
          f"{n}_ATTEMPT{q}_TIME_TO_FRAME360_S={m['frame360']}"]
    by={(r["schedule"],r["attempt"],r["frame"]):r for r in allrows}
    for n in ("C","A","B"):
        ok=all(by[(n,q,f)]["capture_status"]=="PASS" for q in (1,2) for f in FRAMES)
        same=ok and all(by[(n,1,f)]["ram_first_2mib_sha256"]==by[(n,2,f)]["ram_first_2mib_sha256"] for f in FRAMES)
        first=next((f for f in FRAMES if ok and by[(n,1,f)]["ram_first_2mib_sha256"]!=by[(n,2,f)]["ram_first_2mib_sha256"]),None)
        summary += [f"SCHEDULE_{n}_CAPTURES_ALL_PASS={str(ok).upper()}",
          f"SCHEDULE_{n}_RAM_IDENTICAL_TWO_LAUNCHES={str(same).upper() if ok else 'TIDAK TAHU'}",
          f"SCHEDULE_{n}_FIRST_DIVERGENCE={('FRAME_'+str(first)) if first else 'NONE' if ok else 'TIDAK TAHU'}"]
    measured=[]
    for r in allrows:
        if r["frame"]==360 and r["time_to_frame_s"]!="TIDAK TAHU":
            try: measured.append(float(r["time_to_frame_s"]))
            except ValueError: pass
    max_t=max(measured) if len(measured)==6 else None
    timeout_ok=max_t is not None and a.timeout>=2*max_t
    summary += [f"MAX_TIME_TO_FRAME360_S={max_t if max_t is not None else 'TIDAK TAHU'}",
      f"TIMEOUT_PER_LAUNCH_S={a.timeout}",f"TIMEOUT_GE_2X_SLOWEST={str(timeout_ok).upper() if max_t is not None else 'TIDAK TAHU'}"]
    rng=[r["word_0x800A3118"] for r in allrows]
    unique=sorted(set(x for x in rng if x!="TIDAK TAHU"))
    summary += [f"RNG_0x800A3118_CHANGED_ANY_CAPTURE={'YES' if len(unique)>1 and len(unique)==len(set(rng)) else 'NO' if len(unique)==1 and len(rng)==30 else 'TIDAK TAHU'}",
      "RNG_0x800A3118_UNIQUE_VALUES="+(",".join(unique) if unique else "TIDAK TAHU")]
    paircounts={}
    for d in diffs:
        if d["record_type"]=="SUMMARY": paircounts[(d["comparison"],d["frame"],d["attempt"])]=d["total_diff_bytes"]
    for x,y in (("C","A"),("C","B"),("A","B")):
        vals=[paircounts.get((f"{x}_vs_{y}_attempt{q}",f,q),"TIDAK TAHU") for q in (1,2) for f in DIFF_FRAMES]
        known=all(isinstance(v,int) for v in vals)
        status="YES" if known and any(v>0 for v in vals) else "NO" if known else "TIDAK TAHU"
        summary += [f"{x}_VS_{y}_DIFF_VISIBLE={status}",
          f"{x}_VS_{y}_DIFF_COUNTS_ATTEMPT1_THEN2_FRAME180_240_360="+",".join(map(str,vals))]
    capture_ok=len(allrows)==30 and all(r["capture_status"]=="PASS" for r in allrows)
    mcd_ok=len(metas)==6 and all(m["mcd_before"]==CARD and m["mcd_bytes_after"]==CARD_SIZE for m in metas)
    exit_ok=len(metas)==6 and all(m["exit"]=="0" and not m["watchdog"] for m in metas)
    input_ok=all(m["pressok"] and m["releaseok"] for m in metas)
    diff_balance=all(d["label_plus_unknown_equals_total"] for d in diffs)
    diff_known=all(isinstance(d["total_diff_bytes"],int) for d in diffs if d["record_type"]=="SUMMARY")
    complete=capture_ok and mcd_ok and exit_ok and input_ok and timeout_ok and diff_balance and diff_known
    summary += [f"ALL_30_CAPTURE_ROWS_PASS={str(capture_ok).upper()}",f"ALL_SIX_MCD_COPIES_VERIFIED={str(mcd_ok).upper()}",
      f"ALL_SIX_EMULATOR_EXIT_ZERO_NO_WATCHDOG={str(exit_ok).upper()}",f"INPUT_READBACKS_PASS={str(input_ok).upper()}",
      f"ALL_DIFF_LABEL_PLUS_UNKNOWN_BALANCED={str(diff_balance).upper()}",f"ALL_DIFF_SUMMARY_ROWS_KNOWN={str(diff_known).upper()}",
      f"AN2_AN3_STATUS={'PASS' if complete else 'INCOMPLETE'}"]
    (out/"AN2_AN3_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    code=0 if complete else 1
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text("\n".join([
      f"STATUS={'PASS' if complete else 'INCOMPLETE'}","JOB=an2-an3-h6-isolated-mcd","JOB_ID=TIDAK TAHU",
      f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",
      f"ALL_30_CAPTURE_ROWS_PASS={str(capture_ok).upper()}",f"ALL_SIX_MCD_COPIES_VERIFIED={str(mcd_ok).upper()}",
      f"ALL_SIX_EMULATOR_EXIT_ZERO_NO_WATCHDOG={str(exit_ok).upper()}",f"TIMEOUT_GE_2X_SLOWEST={str(timeout_ok).upper() if max_t is not None else 'TIDAK TAHU'}",
      f"EXIT_CODE={code}"])+"\n",encoding="utf-8")
    shutil.rmtree(work/"launches",ignore_errors=True); shutil.rmtree(work/"logs",ignore_errors=True)
    try: (work/"resume"/"h6.sstate").unlink()
    except OSError: pass
    raise SystemExit(code)

if __name__=="__main__": main()
