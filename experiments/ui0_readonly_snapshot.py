#!/usr/bin/env python3
"""UI0: two 900-frame NO_INPUT read-only RAM snapshots from the immutable UE2 state."""
from __future__ import annotations
import argparse, os, shutil, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

START=0x80000000; END=0x80200000; RAM_BYTES=0x200000
STRIDE=0x124; RECORD_OFF=0x48
LAUNCHES=("NO_INPUT_1","NO_INPUT_2")
SCALARS=(("P",0x8013EA84,4),("index_8013EB20",0x8013EB20,4),
 ("value_8013EAB0",0x8013EAB0,4),("value_8013EA8A",0x8013EA8A,2),
 ("value_8013EA74",0x8013EA74,4),("state_80139F03",0x80139F03,1),
 ("counter_80139EC2",0x80139EC2,2))
FIELDS=(("field_00",0,1),("field_1A",0x1A,2),("field_1C",0x1C,2),("field_1E",0x1E,2),("field_20",0x20,2))
VALUE_FIELDS=["launch","frame","record_index","label","address","width","value_hex"]

def in_ram(a,w): return START<=a<END and a+w<=END

def plan(p):
    result=[("",n,a,w) for n,a,w in SCALARS]
    if not START<=p<END: return result
    for i in range(64):
        rec=p+i*STRIDE+RECORD_OFF
        if START<=rec<END:
            result.extend((str(i),n,rec+off,w) for n,off,w in FIELDS)
    return result

def fake_memory_self_test():
    p=0x80001000; reads=plan(p)
    assert len(reads)==7+64*5
    mem=bytearray(RAM_BYTES)
    def put(a,w,v): mem[a-START:a-START+w]=int(v).to_bytes(w,"little")
    for n,a,w in SCALARS: put(a,w,p if n=="P" else 0)
    for i,(_,_,a,w) in enumerate(reads[7:]): put(a,w,i&((1<<(8*w))-1))
    for _,_,a,w in reads:
        assert in_ram(a,w)
        int.from_bytes(mem[a-START:a-START+w],"little")
    assert len(plan(0x7FFFFFFF))==7

def lua_probe(launch):
    return r'''
local ffi=require("ffi")
local LAUNCH="''' + launch + r'''"
local RAM_START=0x80000000
local RAM_END=0x80200000
local MOD=4294967296
local mem=PCSX.getMemPtr()
local loaded,started,post=false,false,0
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
local function hx(v,w)
 if v==nil then return "TIDAK_TAHU" end
 if w==1 then return string.format("0x%02X",tonumber(v)%256) end
 if w==2 then return string.format("0x%04X",tonumber(v)%65536) end
 return string.format("0x%08X",tonumber(v)%MOD)
end
local function readv(a,w)
 local va=tonumber(a)%MOD; local phys=va%0x20000000
 if va<RAM_START or va>=RAM_END or phys+w>0x200000 then return nil,"OUTSIDE_RAM" end
 local ok,v=pcall(function()
   if w==1 then return tonumber(ffi.cast("const uint8_t *",mem+phys)[0]) end
   if w==2 then return tonumber(ffi.cast("const uint16_t *",mem+phys)[0]) end
   return tonumber(ffi.cast("const uint32_t *",mem+phys)[0])
 end)
 if not ok or v==nil then return nil,"READ_ERROR" end
 return v,nil
end
local function emit(frame,idx,label,a,w,v,err)
 log(table.concat({"UI0_VALUE",LAUNCH,tostring(frame),idx or "",label,
   string.format("0x%08X",tonumber(a)%MOD),"u"..tostring(w),err or hx(v,w)},"\t"))
end
local function snapshot(frame)
 local p=nil
 for _,s in ipairs({
  {"P",0x8013EA84,4},{"index_8013EB20",0x8013EB20,4},
  {"value_8013EAB0",0x8013EAB0,4},{"value_8013EA8A",0x8013EA8A,2},
  {"value_8013EA74",0x8013EA74,4},{"state_80139F03",0x80139F03,1},
  {"counter_80139EC2",0x80139EC2,2}
 }) do
  local v,e=readv(s[2],s[3]); emit(frame,"",s[1],s[2],s[3],v,e)
  if s[1]=="P" then p=v end
 end
 if p==nil or p<RAM_START or p>=RAM_END then
  emit(frame,"","RECORD_SCAN_SKIPPED_POINTER_OUTSIDE_RAM",p or 0,4,nil,"NOT_A_VALID_RAM_POINTER"); return
 end
 local fields={{"field_00",0,1},{"field_1A",0x1A,2},{"field_1C",0x1C,2},{"field_1E",0x1E,2},{"field_20",0x20,2}}
 for i=0,63 do
  local rec=p+i*0x124+0x48
  if rec>=RAM_START and rec<RAM_END then
   for _,f in ipairs(fields) do
    local a=rec+f[2]; local v,e=readv(a,f[3]); emit(frame,tostring(i),f[1],a,f[3],v,e)
   end
  end
 end
end
_G.ui0Loaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
 loaded=true; post=0; log("UI0_SAVE_STATE_LOADED=YES launch="..LAUNCH)
end)
_G.ui0Vsync=PCSX.Events.createEventListener("GPU::Vsync",function()
 if not started then
  started=true; local path=os.getenv("UE2_SOURCE_STATE") or "resume/source.sstate"
  PCSX.pauseEmulator()
  PCSX.nextTick(function()
   local okf,f=pcall(function() return assert(Support.File.open(path)) end)
   if not okf or not f then log("UI0_STATE_OPEN_FAIL="..tostring(f)); PCSX.quit(50); return end
   local ok,e=pcall(function() PCSX.loadSaveState(f) end); f:close()
   if not ok then log("UI0_STATE_LOAD_FAIL="..tostring(e)); PCSX.quit(51); return end
   PCSX.resumeEmulator()
  end)
  return
 end
 if not loaded then return end
 post=post+1
 if post==1 or post==900 then snapshot(post) end
 if post==900 then log("UI0_FRAME_LIMIT_REACHED launch="..LAUNCH.." frames=900"); PCSX.nextTick(function() PCSX.quit(0) end) end
end)
log("UI0_SCRIPT_READY launch="..LAUNCH.." frames=900 memory_write=NO write_watchpoint=NO input=NO")
'''.lstrip()

def parse(log):
    rows=[]
    for line in log.splitlines():
        if not line.startswith("UI0_VALUE\t"): continue
        p=line.split("\t")
        if len(p)==8:
            rows.append(dict(zip(VALUE_FIELDS,[p[1],p[2],p[3],p[4],p[5],p[6],p[7]])))
    return rows

def validate(rows):
    groups=defaultdict(list)
    for r in rows: groups[(r["launch"],r["frame"])].append(r)
    ok=True; detail=[]
    for launch in LAUNCHES:
        for frame in ("1","900"):
            rs=groups[(launch,frame)]; pr=next((r for r in rs if r["label"]=="P"),None)
            try: p=int(pr["value_hex"],16) if pr else -1
            except ValueError: p=-1
            valid=START<=p<END; expected=plan(p) if valid else []
            actual={(r["record_index"],r["label"],int(r["address"],16),int(r["width"][1:]))
                    for r in rs if r["label"]!="RECORD_SCAN_SKIPPED_POINTER_OUTSIDE_RAM"}
            wanted={(i,n,a,w) for i,n,a,w in expected}
            noerr=all(r["value_hex"] not in ("OUTSIDE_RAM","READ_ERROR","NOT_A_VALID_RAM_POINTER") for r in rs)
            good=valid and len(expected)>7 and actual==wanted and noerr
            ok=ok and good
            detail += [f"{launch}_FRAME_{frame}_P={pr['value_hex'] if pr else 'TIDAK TAHU'}",
              f"{launch}_FRAME_{frame}_P_IN_RAM={'YES' if valid else 'NO'}",
              f"{launch}_FRAME_{frame}_VALUE_ROWS_EXPECTED={len(expected)}",
              f"{launch}_FRAME_{frame}_VALUE_ROWS_OBSERVED={len(actual)}",
              f"{launch}_FRAME_{frame}_RECORD_SLOTS_IN_RAM={(len(expected)-7)//5}",
              f"{launch}_FRAME_{frame}_SNAPSHOT_COMPLETE={'YES' if good else 'NO'}"]
    return ok,detail

def compare(rows):
    groups=defaultdict(dict)
    for r in rows: groups[(r["frame"],r["record_index"],r["label"],r["width"])][r["launch"]]=r
    out=[]; identical=True
    for key,v in sorted(groups.items()):
        a,b=v.get(LAUNCHES[0]),v.get(LAUNCHES[1])
        result="MISSING" if not a or not b else ("IDENTICAL" if a["value_hex"]==b["value_hex"] and a["address"]==b["address"] else "DIFFERENT")
        if result!="IDENTICAL": identical=False
        out.append({"comparison":"BETWEEN_LAUNCHES_SAME_FRAME","frame":key[0],"record_index":key[1],"label":key[2],"width":key[3],
          "address_launch1":a["address"] if a else "TIDAK TAHU","address_launch2":b["address"] if b else "TIDAK TAHU",
          "value_launch1":a["value_hex"] if a else "TIDAK TAHU","value_launch2":b["value_hex"] if b else "TIDAK TAHU","result":result})
    temporal=defaultdict(dict)
    for r in rows: temporal[(r["launch"],r["record_index"],r["label"])][r["frame"]]=r
    changed=0
    for key,v in sorted(temporal.items()):
        a,b=v.get("1"),v.get("900")
        result="MISSING" if not a or not b else ("IDENTICAL" if a["address"]==b["address"] and a["value_hex"]==b["value_hex"] else "CHANGED")
        changed+=int(result=="CHANGED")
        out.append({"comparison":"WITHIN_LAUNCH_FRAME1_VS_900","frame":"1_vs_900","record_index":key[1],"label":key[2],
          "width":(a or b or {}).get("width","TIDAK TAHU"),"address_launch1":a["address"] if a else "TIDAK TAHU",
          "address_launch2":b["address"] if b else "TIDAK TAHU","value_launch1":a["value_hex"] if a else "TIDAK TAHU",
          "value_launch2":b["value_hex"] if b else "TIDAK TAHU","result":result})
    return out,identical,changed

def main():
    ap=argparse.ArgumentParser()
    for name in ("work","out","pcsx-bin","appdir","bios","cue","source","card-dir"): ap.add_argument("--"+name,type=Path)
    ap.add_argument("--timeout-seconds",type=int,default=180); ap.add_argument("--self-test",action="store_true"); a=ap.parse_args()
    if a.self_test:
        fake_memory_self_test(); p=lua_probe("FAKE")
        for token in ("0x8013EA84","0x8013EB20","0x8013EAB0","0x8013EA8A","0x8013EA74","0x80139F03","0x80139EC2","0x124","0x48","0x1A","0x1C","0x1E","0x20"): assert token in p
        assert "addBreakpoint" not in p and "setOverride" not in p
        print("UI0_FAKE_MEMORY_SELF_TEST=PASS"); return 0
    paths=(a.work,a.out,a.pcsx_bin,a.appdir,a.bios,a.cue,a.source,a.card_dir)
    if any(x is None for x in paths): ap.error("runtime arguments missing")
    work,out,pcsx,appdir,bios,cue,source,carddir=paths
    from experiments.ub2_headless_trace import EXPECTED_CARD_BYTES,SOURCE_SHA256,lua_warmup,read_log_text,run_emulator,sha,write_tsv
    work.mkdir(parents=True,exist_ok=True); out.mkdir(parents=True,exist_ok=True); carddir.mkdir(parents=True,exist_ok=True)
    source_before=sha(source)
    if source_before!=SOURCE_SHA256 or source.stat().st_size!=21162799: raise SystemExit("UI0_CHECKPOINT_IDENTITY_MISMATCH")
    source.chmod(0o444)
    # PCSX bootstrap only creates a valid blank Memory Card; the two measured launches are below.
    template=carddir/"memory-card-template.mcd"; warm=work/"memcard-bootstrap.lua"; warm.write_text(lua_warmup(),encoding="utf-8")
    warm_rc,warm_wall,warm_log=run_emulator(pcsx,appdir,bios,cue,template,None,warm,work/"bootstrap-home",work/"bootstrap.stdout.txt",120)
    if warm_rc!=0 or "UB2_MEMCARD_WARMUP_FRAMES=12" not in warm_log or not template.is_file() or template.stat().st_size!=EXPECTED_CARD_BYTES:
        raise SystemExit("UI0_MEMCARD_BOOTSTRAP_FAILED")
    template_hash=sha(template); template.chmod(0o444)
    launches=[]; values=[]
    for launch in LAUNCHES:
        d=work/launch.lower(); d.mkdir(parents=True,exist_ok=True)
        state=d/"source.sstate"; shutil.copyfile(source,state); sb=sha(state); state.chmod(0o444)
        card=d/"memory-card.mcd"; shutil.copyfile(template,card); cb=sha(card); card.chmod(0o444)
        lua=d/"ui0.lua"; lua.write_text(lua_probe(launch),encoding="utf-8"); stdout=d/"emulator.stdout.txt"
        rc,wall,_=run_emulator(pcsx,appdir,bios,cue,card,state,lua,d/"home",stdout,a.timeout_seconds)
        log=read_log_text(stdout); captured=parse(log); values+=captured
        frames=900 if f"UI0_FRAME_LIMIT_REACHED launch={launch} frames=900" in log else 0
        loaded=f"UI0_SAVE_STATE_LOADED=YES launch={launch}" in log
        ca=sha(card) if card.exists() else "TIDAK TAHU"; sa=sha(state) if state.exists() else "TIDAK TAHU"
        ro=card.exists() and (card.stat().st_mode&0o222)==0
        launches.append({"launch":launch,"condition":"NO_INPUT","frames_reached":frames,"save_state_loaded":"YES" if loaded else "NO",
          "emulator_exit_code":rc,"snapshot_rows":len(captured),"memory_card_sha256_before":cb,"memory_card_sha256_after":ca,
          "memory_card_unchanged":"YES" if cb==ca else "NO","memory_card_read_only_0444":"YES" if ro else "NO",
          "checkpoint_sha256_before":sb,"checkpoint_sha256_after":sa,"checkpoint_unchanged":"YES" if sb==sa else "NO","wall_seconds":f"{wall:.3f}"})
        state.unlink(missing_ok=True); card.unlink(missing_ok=True)
    write_tsv(out/"UI0_VALUES.tsv",VALUE_FIELDS,values)
    comparisons,identical,changed=compare(values)
    cf=["comparison","frame","record_index","label","width","address_launch1","address_launch2","value_launch1","value_launch2","result"]
    write_tsv(out/"UI0_COMPARISON.tsv",cf,comparisons)
    write_tsv(out/"UI0_LAUNCHES.tsv",list(launches[0]),launches)
    source_after=sha(source); snapshots_ok,detail=validate(values)
    complete=warm_rc==0 and snapshots_ok and source_before==source_after==SOURCE_SHA256 and all(
      x["frames_reached"]==900 and x["save_state_loaded"]=="YES" and x["emulator_exit_code"]==0 and
      x["memory_card_unchanged"]=="YES" and x["memory_card_read_only_0444"]=="YES" and x["checkpoint_unchanged"]=="YES" for x in launches)
    k5=complete and identical
    summary=["UI0_READ_ONLY_RUNTIME_SNAPSHOT",f"STATUS={'TUNTAS' if k5 else ('SEBAGIAN' if complete else 'BELUM')}",
      f"EVIDENCE={'K5' if k5 else ('K2' if complete else 'K0')}","JOB=ui0-ui1-audit",
      f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
      "CHECKPOINT_ARTIFACT_RUN_ID=39907655833",f"CHECKPOINT_SHA256_EXPECTED={SOURCE_SHA256}",
      f"CHECKPOINT_SHA256_SOURCE_BEFORE={source_before}",f"CHECKPOINT_SHA256_SOURCE_AFTER={source_after}",
      "CONDITIONS=NO_INPUT_1,NO_INPUT_2","POST_LOAD_FRAMES_PER_LAUNCH=900",
      "GAME_MEMORY_READ_ONLY=YES; no write-watchpoint; no input override",
      "MEMORY_CARD_BOOTSTRAP=one 12-frame setup-only startup before measured launches",
      f"MEMORY_CARD_TEMPLATE_SHA256={template_hash}",f"MEMORY_CARD_TEMPLATE_BYTES={template.stat().st_size}",
      f"MEMORY_CARD_BOOTSTRAP_WALL_SECONDS={warm_wall:.3f}","MEMORY_CARD_MODE_PER_LAUNCH=0444",
      "SCALARS=EA84:u32;EB20:u32;EAB0:u32;EA8A:u16;EA74:u32;9F03:u8;9EC2:u16",
      "RECORDS=P+i*0x124+0x48; i=0..63; fields +00:u8,+1A:u16,+1C:u16,+1E:u16,+20:u16",
      "ACTIVE_RECORD_COUNT=TIDAK TAHU; max 64 candidate slots, not inferred active count",
      "VALUE_RANGE_ASSESSMENT=TIDAK TAHU; semantics/ranges unknown; raw hex retained",
      f"SNAPSHOT_ROWS={len(values)}",f"SNAPSHOTS_COMPLETE={'YES' if snapshots_ok else 'NO'}",*detail,
      f"SAME_FRAME_LAUNCH_VALUES_IDENTICAL={'YES' if identical else 'NO'}",
      f"FRAME1_VS_900_CHANGED_ROWS={changed}",f"BOTH_LAUNCHES_COMPLETE={'YES' if complete else 'NO'}",
      f"K5_REPEATABILITY={'PASS' if k5 else 'NOT_ESTABLISHED'}",f"EXIT_CODE={0 if k5 else 2}","RAW_DUMP=NONE"]
    (out/"UI0_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary)); return 0 if k5 else 2

if __name__=="__main__": raise SystemExit(main())
