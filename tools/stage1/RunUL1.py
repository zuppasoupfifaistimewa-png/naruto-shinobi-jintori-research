#!/usr/bin/env python3
"""UL1: two frame-1-only read-only PCSX-Redux snapshots of all requested bytes."""
from __future__ import annotations
import argparse,csv,hashlib,os,shutil,subprocess,time
from collections import defaultdict
from pathlib import Path

CHECKPOINT_SHA="705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35"
CHECKPOINT_BYTES=21162799
CARD_SHA="78b6d4ac9ab4d23caf7e5f04f83539bf5d994cccfb0a709d14ac53d05c8e21ef"
CARD_BYTES=131072
RAM_START=0x80000000
RAM_END=0x80200000
STRIDE=0x124
RECORDS=tuple([f"A:{i}" for i in range(22)]+["A:22","A:43"])
SCALARS=(("0x8013EA84",0x8013EA84,4),("0x8013EB20",0x8013EB20,4),("0x8013EAB0",0x8013EAB0,4),
 ("0x8013EA8A",0x8013EA8A,2),("0x8013EA74",0x8013EA74,4),("0x80139F03",0x80139F03,1),("0x80139EC2",0x80139EC2,2))
BYTE_FIELDS=["launch","frame","record","offset","address","byte_hex"]
SCALAR_FIELDS=["launch","frame","name","address","width","value_hex"]
LAUNCH_FIELDS=["launch","status","preload_boot_frames","emulator_exit_code","snapshot_bytes","snapshot_scalars",
 "card_sha256_before_process","card_sha256_before_measurement","card_sha256_after","card_expected_match","card_unchanged","card_mode_0444",
 "checkpoint_sha256_before","checkpoint_sha256_after","checkpoint_source_sha256_before","checkpoint_source_sha256_after",
 "checkpoint_unchanged","ram_addresses_valid","wall_seconds"]

def sha(path:Path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def in_ram(address,width=1): return RAM_START<=address and address+width<=RAM_END

def lua_probe(launch:str,card_path:Path,gate_path:Path):
    card=str(card_path).replace("\\","\\\\").replace('"','\\"')
    gate=str(gate_path).replace("\\","\\\\").replace('"','\\"')
    return r'''
local ffi=require("ffi")
local LAUNCH="''' + launch + r'''"
local CARD_PATH="''' + card + r'''"
local GATE_PATH="''' + gate + r'''"
local RAM_START=0x80000000
local RAM_END=0x80200000
local MOD=4294967296
local mem=PCSX.getMemPtr()
local boot_frames,loaded,started,post=0,false,false,0
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
local function file_size(path)
 local ok,f=pcall(function() return io.open(path,"rb") end)
 if not ok or not f then return -1 end
 local ok2,n=pcall(function() return f:seek("end") end); f:close()
 if not ok2 or n==nil then return -1 end
 return tonumber(n)
end
local function readv(a,w)
 local va=tonumber(a)%MOD; local phys=va%0x20000000
 if va<RAM_START or va+w>RAM_END or phys+w>0x200000 then return nil,"OUTSIDE_RAM" end
 local ok,v=pcall(function()
  if w==1 then return tonumber(ffi.cast("const uint8_t *",mem+phys)[0]) end
  if w==2 then return tonumber(ffi.cast("const uint16_t *",mem+phys)[0]) end
  return tonumber(ffi.cast("const uint32_t *",mem+phys)[0])
 end)
 if not ok or v==nil then return nil,"READ_ERROR" end
 return v,nil
end
local function hx(v,w)
 if v==nil then return "TIDAK_TAHU" end
 if w==1 then return string.format("0x%02X",tonumber(v)%256) end
 if w==2 then return string.format("0x%04X",tonumber(v)%65536) end
 return string.format("0x%08X",tonumber(v)%MOD)
end
local function emit_scalar(name,a,w,v,e)
 log(table.concat({"UL1_SCALAR",LAUNCH,"1",name,string.format("0x%08X",a),"u"..tostring(w),e or hx(v,w)},"\t"))
end
local function snapshot()
 local p=nil
 local specs={{"0x8013EA84",0x8013EA84,4},{"0x8013EB20",0x8013EB20,4},{"0x8013EAB0",0x8013EAB0,4},
  {"0x8013EA8A",0x8013EA8A,2},{"0x8013EA74",0x8013EA74,4},{"0x80139F03",0x80139F03,1},{"0x80139EC2",0x80139EC2,2}}
 for _,s in ipairs(specs) do
  local v,e=readv(s[2],s[3]); emit_scalar(s[1],s[2],s[3],v,e)
  if s[2]==0x8013EA84 then p=v end
 end
 if p==nil or p<RAM_START or p>=RAM_END then
  log("UL1_POINTER_INVALID="..tostring(p)); PCSX.nextTick(function() PCSX.quit(53) end); return
 end
 local wanted={}
 for i=0,21 do wanted[#wanted+1]={"A:"..tostring(i),i} end
 wanted[#wanted+1]={"A:22",22}; wanted[#wanted+1]={"A:43",43}
 local total=0; local invalid=0
 for _,r in ipairs(wanted) do
  local name=r[1]; local i=r[2]; local first=p+i*0x124; local last=first+0x123
  if first<RAM_START or last>=RAM_END then
   invalid=invalid+1; log("UL1_RECORD_OUTSIDE_RAM\t"..LAUNCH.."\t"..name.."\t"..string.format("0x%08X",first).."\t"..string.format("0x%08X",last))
  else
   for off=0,0x123 do
    local a=first+off; local v,e=readv(a,1)
    if e then invalid=invalid+1 end
    log(table.concat({"UL1_BYTE",LAUNCH,"1",name,string.format("0x%03X",off),string.format("0x%08X",a),e or hx(v,1)},"\t"))
    total=total+1
   end
  end
 end
 log("UL1_SNAPSHOT_END\t"..LAUNCH.."\tbytes="..tostring(total).."\tinvalid="..tostring(invalid).."\tpost_load_frame=1")
 PCSX.nextTick(function() PCSX.quit(invalid==0 and total==7008 and 0 or 54) end)
end
local function await_gate()
 local ok,f=pcall(function() return io.open(GATE_PATH,"rb") end)
 if ok and f then f:close()
  local state=os.getenv("UE2_SOURCE_STATE") or "resume/source.sstate"
  local okf,sf=pcall(function() return assert(Support.File.open(state)) end)
  if not okf or not sf then log("UL1_STATE_OPEN_FAIL="..tostring(sf)); PCSX.quit(50); return end
  local okload,err=pcall(function() PCSX.loadSaveState(sf) end); sf:close()
  if not okload then log("UL1_STATE_LOAD_FAIL="..tostring(err)); PCSX.quit(51); return end
  PCSX.resumeEmulator()
  return
 end
 PCSX.nextTick(await_gate)
end
_G.ul1Loaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
 loaded=true; post=0; log("UL1_SAVE_STATE_LOADED=YES launch="..LAUNCH)
end)
_G.ul1Vsync=PCSX.Events.createEventListener("GPU::Vsync",function()
 if not loaded then
  boot_frames=boot_frames+1
  if not started and boot_frames>=12 and file_size(CARD_PATH)==131072 then
   started=true; PCSX.pauseEmulator(); log("UL1_CARD_READY\t"..LAUNCH.."\tpreload_boot_frames="..tostring(boot_frames))
   PCSX.nextTick(await_gate)
  end
  return
 end
 post=post+1
 if post==1 then snapshot() end
end)
log("UL1_SCRIPT_READY launch="..LAUNCH.." frame1_only=YES memory_write=NO write_watch=NO input=NO")
'''.lstrip()

def app_env(appdir:Path,home:Path):
    e=os.environ.copy()
    e.update({"HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),"XDG_DATA_HOME":str(home/".data"),
      "XDG_RUNTIME_DIR":str(home/"runtime"),"DISPLAY":"","LIBGL_ALWAYS_SOFTWARE":"1",
      "LD_LIBRARY_PATH":str(appdir/"usr/lib")+":"+str(appdir/"usr/lib/x86_64-linux-gnu"),
      "QT_PLUGIN_PATH":str(appdir/"usr/plugins"),"QT_QPA_PLATFORM_PLUGIN_PATH":str(appdir/"usr/plugins/platforms"),
      "QML2_IMPORT_PATH":str(appdir/"usr/qml")})
    return e

def wait_text(path:Path,needle:str,proc,timeout:float):
    end=time.monotonic()+timeout
    while time.monotonic()<end:
        if path.exists():
            try:
                s=path.read_text(encoding="utf-8",errors="replace")
                if needle in s: return True,s
            except OSError: pass
        if proc.poll() is not None: break
        time.sleep(.05)
    return False,(path.read_text(encoding="utf-8",errors="replace") if path.exists() else "")

def run_one(launch,pcsx,appdir,bios,cue,source,card,work,timeout_s):
    d=work/launch.lower(); d.mkdir(parents=True,exist_ok=True)
    state=d/"source.sstate"; shutil.copyfile(source,state); state.chmod(0o444)
    gate=d/"allow-load.flag"; gate.unlink(missing_ok=True)
    lua=d/"ul1.lua"; lua.write_text(lua_probe(launch,card,gate),encoding="utf-8")
    stdout=d/"emulator.stdout.txt"; pcxlog=d/"emulator.pcsx.log"
    home=d/"home"
    for p in (home/".config",home/".data",home/"runtime"): p.mkdir(parents=True,exist_ok=True)
    try: (home/"runtime").chmod(0o700)
    except OSError: pass
    cmd=["timeout","--signal=INT","--kill-after=10s",f"{timeout_s}s",str(pcsx),"-noupdate","-no-ui","-debugger","-interpreter",
      "-bios",str(bios),"-iso",str(cue),"-memcard1",str(card),"-softgpu","-dofile",str(lua),"-logfile",str(pcxlog),"-run"]
    env=app_env(appdir,home); env["UE2_SOURCE_STATE"]=str(state); env["UB2_SOURCE_STATE"]=str(state)
    source_before=sha(source); state_before=sha(state)
    card_process_before=sha(card) if card.exists() and card.stat().st_size==CARD_BYTES else "NOT_CREATED_BEFORE_FIRST_PROCESS"
    t=time.monotonic(); rc=255; card_before="TIDAK_TAHU"; ready=False; proc=None; log=""
    with stdout.open("wb") as f:
        try:
            proc=subprocess.Popen(cmd,cwd=home,env=env,stdout=f,stderr=subprocess.STDOUT)
            ready,log=wait_text(stdout,"UL1_CARD_READY",proc,min(timeout_s,90))
            if ready and card.is_file() and card.stat().st_size==CARD_BYTES:
                card_before=sha(card); card.chmod(0o444)
                gate.write_text("ALLOW_LOAD_CHECKPOINT_AFTER_CARD_HASH\n",encoding="ascii")
                try: rc=proc.wait(timeout=max(1,timeout_s-(time.monotonic()-t)))
                except subprocess.TimeoutExpired: proc.kill(); rc=124; proc.wait()
            else:
                if proc.poll() is None: proc.terminate()
                try: proc.wait(timeout=5)
                except subprocess.TimeoutExpired: proc.kill(); proc.wait()
                rc=proc.returncode if proc.returncode is not None else 124
        except Exception as exc:
            if proc and proc.poll() is None: proc.kill(); proc.wait()
            f.write(("UL1_LAUNCH_EXCEPTION="+repr(exc)+"\n").encode())
    wall=time.monotonic()-t
    if stdout.exists(): log=stdout.read_text(encoding="utf-8",errors="replace")
    if pcxlog.exists(): log+="\n"+pcxlog.read_text(encoding="utf-8",errors="replace")
    parsed=parse_log(log,launch)
    card_after=sha(card) if card.exists() and card.stat().st_size==CARD_BYTES else "TIDAK_TAHU"
    card_unchanged=(card_before==card_after and card_before!="TIDAK_TAHU")
    card_mode=card.exists() and (card.stat().st_mode&0o777)==0o444
    source_after=sha(source) if source.exists() else "TIDAK_TAHU"
    state_after=sha(state) if state.exists() else "TIDAK_TAHU"
    info={"launch":launch,"status":"PASS" if ready and rc==0 and card_unchanged and card_mode and
      state_before==state_after==CHECKPOINT_SHA and source_before==source_after==CHECKPOINT_SHA and
      parsed["valid"] and card_before==CARD_SHA else "SEBAGIAN",
      "preload_boot_frames":next((x.split("preload_boot_frames=",1)[1] for x in log.splitlines()
        if "UL1_CARD_READY" in x and "preload_boot_frames=" in x),"TIDAK TAHU"),
      "emulator_exit_code":rc,"snapshot_bytes":len(parsed["bytes"]),"snapshot_scalars":len(parsed["scalars"]),
      "card_sha256_before_process":card_process_before,"card_sha256_before_measurement":card_before,
      "card_sha256_after":card_after,"card_expected_match":"YES" if card_before==CARD_SHA else "NO",
      "card_unchanged":"YES" if card_unchanged else "NO","card_mode_0444":"YES" if card_mode else "NO",
      "checkpoint_sha256_before":state_before,"checkpoint_sha256_after":state_after,
      "checkpoint_source_sha256_before":source_before,"checkpoint_source_sha256_after":source_after,
      "checkpoint_unchanged":"YES" if state_before==state_after==CHECKPOINT_SHA and source_before==source_after==CHECKPOINT_SHA else "NO",
      "ram_addresses_valid":"YES" if parsed["valid"] else "NO","wall_seconds":f"{wall:.3f}"}
    state.unlink(missing_ok=True)
    return info,parsed,log

def parse_log(log,launch):
    byte_rows=[]; scalar_rows=[]; valid=True
    for line in log.splitlines():
        if line.startswith("UL1_BYTE\t"):
            p=line.split("\t")
            if len(p)==7:
                row=dict(zip(BYTE_FIELDS,p[1:])); byte_rows.append(row)
                try:
                    addr=int(row["address"],16); off=int(row["offset"],16); value=int(row["byte_hex"],16)
                    if not in_ram(addr,1) or not 0<=off<=0x123 or not 0<=value<=255 or row["frame"]!="1": valid=False
                except ValueError: valid=False
            else: valid=False
        elif line.startswith("UL1_SCALAR\t"):
            p=line.split("\t")
            if len(p)==7:
                row=dict(zip(SCALAR_FIELDS,p[1:])); scalar_rows.append(row)
                try:
                    addr=int(row["address"],16); width=int(row["width"][1:]); int(row["value_hex"],16)
                    if not in_ram(addr,width) or row["frame"]!="1": valid=False
                except ValueError: valid=False
            else: valid=False
    if len(byte_rows)!=7008 or len(scalar_rows)!=7: valid=False
    wanted={(record,off) for record in RECORDS for off in range(0x124)}; seen=set()
    for r in byte_rows:
        key=(r["record"],int(r["offset"],16))
        if key in seen: valid=False
        seen.add(key)
    if seen!=wanted: valid=False
    if {r["address"] for r in scalar_rows}!={f"0x{a:08X}" for _,a,_ in SCALARS}: valid=False
    scalar_by_addr={r["address"]:r for r in scalar_rows}; p_row=scalar_by_addr.get("0x8013EA84")
    try:
        p_value=int(p_row["value_hex"],16) if p_row else -1
        if not in_ram(p_value,1): valid=False
        for r in byte_rows:
            idx=int(r["record"].split(":",1)[1]); off=int(r["offset"],16)
            expected=p_value+idx*STRIDE+off
            if int(r["address"],16)!=expected or not in_ram(expected,1): valid=False
    except (ValueError,KeyError): valid=False
    widths={f"0x{a:08X}":w for _,a,w in SCALARS}
    for r in scalar_rows:
        try:
            if int(r["width"][1:])!=widths[r["address"]]: valid=False
        except (ValueError,KeyError): valid=False
    return {"bytes":byte_rows,"scalars":scalar_rows,"valid":valid}

def write_tsv(path,fields,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        w.writeheader(); w.writerows(rows)

def read_lv_table(path):
    rows={}
    with path.open(encoding="utf-8",newline="") as f:
        for r in csv.DictReader(f,delimiter="\t"):
            rows[int(r["X"])]=[int(r[f"LV{i}"]) for i in range(1,6)]
    return rows

def derive(rows,table):
    byte_groups=defaultdict(list)
    for r in rows: byte_groups[(r["launch"],r["offset"])].append(int(r["byte_hex"],16))
    variation=[]
    for (launch,off),values in sorted(byte_groups.items(),key=lambda x:(x[0][0],int(x[0][1],16))):
        distinct=sorted(set(values))
        variation.append({"launch":launch,"offset":off,"record_count":len(values),"distinct_values":len(distinct),
          "status":"KONSTAN" if len(distinct)==1 else "BERVARIASI","values_hex":";".join(f"0x{x:02X}" for x in distinct)})
    grouped=defaultdict(dict)
    for r in rows: grouped[(r["launch"],r["record"])][int(r["offset"],16)]=int(r["byte_hex"],16)
    lv_rows=[]
    for (launch,record),bmap in sorted(grouped.items()):
        x=2*(bmap[0x1a]+(bmap[0x1b]<<8)); vals=table.get(x)
        for lv_i in range(5):
            target=vals[lv_i] if vals is not None else None; offsets=[]
            if target is not None:
                for off in range(0x123):
                    v=bmap.get(off); v2=bmap.get(off+1)
                    if v is not None and v2 is not None and (v+(v2<<8))==target: offsets.append(f"0x{off:03X}")
            lv_rows.append({"launch":launch,"record":record,"x_2xu16_plus1a":x,"lv":"LV"+str(lv_i+1),
              "table_value":target if target is not None else "TIDAK ADA","matching_u16_offsets":";".join(offsets),
              "match_status":"MATCH_SCAN_COMPLETE" if target is not None else "X_NOT_IN_SOURCE_TABLE"})
    return variation,lv_rows

def self_test():
    assert len(RECORDS)==24 and 292*24==7008
    fake=[]
    for record in RECORDS:
        for off in range(0x124):
            fake.append({"launch":"NO_INPUT_1","record":record,"offset":f"0x{off:03X}","byte_hex":"0x00"})
    variation,lv=derive(fake,{0:[0,1,2,3,4]})
    assert len(variation)==0x124 and all(x["distinct_values"]==1 and x["record_count"]==24 for x in variation)
    assert len(lv)==24*5 and lv[0]["x_2xu16_plus1a"]==0 and lv[0]["matching_u16_offsets"]==";".join(f"0x{i:03X}" for i in range(0x123))
    assert all(in_ram(0x8013B818+i*STRIDE+0x123,1) for i in (0,21,22,43))
    assert 0x8013B818+44*STRIDE==0x8013EA48
    print("UL1_SELF_TEST=PASS 24 records x 292 bytes; byte/u16 scan; scalar widths; RAM bounds; A:43 end")

def main():
    ap=argparse.ArgumentParser()
    for n in ("work","out","pcsx-bin","appdir","bios","cue","source","card-dir","lv-table"): ap.add_argument("--"+n,type=Path)
    ap.add_argument("--timeout-seconds",type=int,default=180); ap.add_argument("--self-test",action="store_true"); a=ap.parse_args()
    if a.self_test: self_test(); return 0
    paths=(a.work,a.out,a.pcsx_bin,a.appdir,a.bios,a.cue,a.source,a.card_dir,a.lv_table)
    if any(x is None for x in paths): ap.error("runtime arguments missing")
    work,out,pcsx,appdir,bios,cue,source,carddir,lv_table=paths
    if not source.exists() or source.stat().st_size!=CHECKPOINT_BYTES or sha(source)!=CHECKPOINT_SHA: raise SystemExit("UL1_CHECKPOINT_IDENTITY_MISMATCH")
    source.chmod(0o444); carddir.mkdir(parents=True,exist_ok=True); out.mkdir(parents=True,exist_ok=True); work.mkdir(parents=True,exist_ok=True)
    card=carddir/"memory-card-template.mcd"; card.unlink(missing_ok=True)
    launches=[]; allbytes=[]; allscalars=[]
    for index,launch in enumerate(("NO_INPUT_1","NO_INPUT_2")):
        if index==1:
            if not card.is_file() or card.stat().st_size!=CARD_BYTES: raise SystemExit("UL1_FIRST_LAUNCH_DID_NOT_CREATE_128K_CARD")
            shutil.copyfile(card,carddir/"memory-card-launch2.mcd")
            card=carddir/"memory-card-launch2.mcd"; card.chmod(0o444)
        info,parsed,_=run_one(launch,pcsx,appdir,bios,cue,source,card,work,a.timeout_seconds)
        launches.append(info); allbytes.extend(parsed["bytes"]); allscalars.extend(parsed["scalars"])
        if index==0:
            # There is no file to hash before the first process; the exact expected card is
            # created during its first 12 no-input boot frames, hashed and made 0444 before load.
            if not card.is_file() or sha(card)!=CARD_SHA or (card.stat().st_mode&0o777)!=0o444:
                raise SystemExit("UL1_FIRST_LAUNCH_CARD_TEMPLATE_NOT_IMMUTABLE_OR_HASH_MISMATCH")
    write_tsv(out/"UL1_BYTES.tsv",BYTE_FIELDS,allbytes); write_tsv(out/"UL1_SCALARS.tsv",SCALAR_FIELDS,allscalars)
    table=read_lv_table(lv_table); variation,lv_rows=derive(allbytes,table)
    write_tsv(out/"UL1_OFFSET_VARIATION.tsv",["launch","offset","record_count","distinct_values","status","values_hex"],variation)
    write_tsv(out/"UL1_LV_U16_MATCHES.tsv",["launch","record","x_2xu16_plus1a","lv","table_value","matching_u16_offsets","match_status"],lv_rows)
    write_tsv(out/"UL1_LAUNCHES.tsv",LAUNCH_FIELDS,launches)
    first={(r["record"],r["offset"]):(r["address"],r["byte_hex"]) for r in allbytes if r["launch"]=="NO_INPUT_1"}
    second={(r["record"],r["offset"]):(r["address"],r["byte_hex"]) for r in allbytes if r["launch"]=="NO_INPUT_2"}
    sf={r["address"]:(r["width"],r["value_hex"]) for r in allscalars if r["launch"]=="NO_INPUT_1"}
    ss={r["address"]:(r["width"],r["value_hex"]) for r in allscalars if r["launch"]=="NO_INPUT_2"}
    same=first==second and len(first)==len(second)==7008 and sf==ss and len(sf)==len(ss)==7
    p_row=next((r for r in allscalars if r["launch"]=="NO_INPUT_1" and r["address"]=="0x8013EA84"),None)
    try: a43_end_match=bool(p_row) and int(p_row["value_hex"],16)+44*STRIDE==0x8013EA48
    except ValueError: a43_end_match=False
    allpass=(len(launches)==2 and all(x["status"]=="PASS" and x["card_expected_match"]=="YES" for x in launches)
      and len(allbytes)==14016 and len(allscalars)==14 and len(variation)==2*0x124 and
      len(lv_rows)==2*len(RECORDS)*5 and same and a43_end_match)
    evidence="K5" if allpass else ("K2" if allbytes else "K0")
    summary=["UL1 FRAME-1 FULL-BYTE READ-ONLY SNAPSHOT",
      f"STATUS={'TUNTAS' if allpass else ('SEBAGIAN' if allbytes else 'BELUM')}",f"EVIDENCE={evidence}",
      f"CHECKPOINT_EXPECTED_SHA256={CHECKPOINT_SHA}",f"MEMORY_CARD_EXPECTED_SHA256={CARD_SHA}",
      "CONDITIONS=NO_INPUT_1,NO_INPUT_2","POST_LOAD_FRAME=1 only","EMULATOR_PROCESS_LAUNCHES=2 maximum",
      "INITIALIZATION=card created by PCSX during first process's initial 12 no-input boot frames; hashed and chmod 0444 before checkpoint load",
      "FIRST_CARD_PREPROCESS_HASH=NOT_AVAILABLE because card file does not exist before first process; before-measurement and after hashes recorded",
      "PROBE=read-only FFI; no input override; no write-watch; no emulated memory writes",
      f"RECORDS={len(RECORDS)}; offsets 0x000..0x123; bytes per launch=7008",
      f"BYTE_ROWS={len(allbytes)}",f"SCALAR_ROWS={len(allscalars)}",
      f"TWO_LAUNCH_FULL_BYTES_AND_SCALARS_IDENTICAL={'YES' if same else 'NO'}",
      f"A43_END_EXCLUSIVE_MATCH_0x8013EA48={'YES' if a43_end_match else 'NO'}",
      f"ALL_CHECKPOINT_CARD_RAM_CAPTURE_CHECKS_PASS={'YES' if allpass else 'NO'}","FIELD_SEMANTICS=TIDAK TAHU"]
    if p_row:
        try:
            p_value=int(p_row["value_hex"],16); end43=p_value+44*STRIDE
            summary += [f"P_FRAME1=0x{p_value:08X}",f"A43_FIRST_BYTE=0x{p_value+43*STRIDE:08X}",
              f"A43_LAST_BYTE=0x{end43-1:08X}",f"A43_END_EXCLUSIVE=0x{end43:08X}"]
        except ValueError: summary += ["P_FRAME1=TIDAK TAHU","A43_FIRST_BYTE=TIDAK TAHU","A43_LAST_BYTE=TIDAK TAHU","A43_END_EXCLUSIVE=TIDAK TAHU"]
    for x in launches:
        summary += [f"{x['launch']}_STATUS={x['status']}",f"{x['launch']}_EXIT_CODE={x['emulator_exit_code']}",
          f"{x['launch']}_CARD_BEFORE_PROCESS={x['card_sha256_before_process']}",
          f"{x['launch']}_CARD_BEFORE_MEASUREMENT={x['card_sha256_before_measurement']}",
          f"{x['launch']}_CARD_AFTER={x['card_sha256_after']}",f"{x['launch']}_CARD_0444={x['card_mode_0444']}",
          f"{x['launch']}_CHECKPOINT_BEFORE={x['checkpoint_sha256_before']}",
          f"{x['launch']}_CHECKPOINT_AFTER={x['checkpoint_sha256_after']}",f"{x['launch']}_RAM_VALID={x['ram_addresses_valid']}"]
    (out/"UL1_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary)); return 0 if allpass else 2

if __name__=="__main__": raise SystemExit(main())
