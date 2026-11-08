#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,os,re,shutil,subprocess
from pathlib import Path

SOURCE_RUN=39907655833
ARTIFACT_ID=12482055310
ARTIFACT_SHA="a0f45156dfd489f24c8dc8e122c33a048c7b9ac34b935ac828523593d21ca2a8"
STATE_NAME="adaptive-cycle-02-f180.sstate"
STATE_SIZE=21162799
STATE_SHA="705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35"
BPS={0x800D15A8:"FUN_800D15A8",0x800D2520:"FEE_LHU_A1_1A",0x800D46EC:"FEE_LHU_V0_1A"}
MAX_TRACE=3000
MAX_TILES=512
MAX_BOARD_ROWS=2048
FRAMES=180
LUA=r'''
local launch=__LAUNCH__
local STATE="adaptive-cycle-02-f180.sstate"
local BPS={0x800D15A8,0x800D2520,0x800D46EC}
local names={[0x800D15A8]="FUN_800D15A8",[0x800D2520]="FEE_LHU_A1_1A",[0x800D46EC]="FEE_LHU_V0_1A"}
local frame,pre,loaded,restorePending=0,0,0,false
local traceRows,traceOverflow,boardRows,boardOverflow=0,0,0,0
local counts={}
for _,pc in ipairs(BPS) do counts[pc]=0 end
local trace=assert(io.open("trace.tsv","w"))
local board=assert(io.open("board.tsv","w"))
trace:write("launch\tframe\tpc\tlabel\thit\tpc_reg\tsp\tra\tv0\tv1\ta0\ta1\ta2\ta3\ts0\ts1\ts2\ts3\ts4\tmanager\ttile_base\ttile_count\tplayer_index\tcurrent_index\tselected_index\tpending_index\teffect_state\ttile_ptr\ttile_type\tfield_0e\tfee_1a\tpacked_20\tnibble_4_7\tnibble_8_11\tnibble_12_15\tmoney_p0\tmoney_p1\tmoney_p2\tmoney_p3\teffect_id\td\n")
board:write("launch\tframe\ttag\ttile_index\ttile_type\tfield_0e\tfee_1a\tpacked_20\tnibble_4_7\tnibble_8_11\tnibble_12_15\tmoney_p0\tmoney_p1\tmoney_p2\tmoney_p3\n")
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
local mem=nil
local function read(addr,n)
  local ok,v=pcall(function()
    if mem==nil then mem=PCSX.getMemoryAsFile() end
    local b=mem:readAt(n,addr); local x=0
    for i=0,n-1 do x=x+tonumber(b[i])*(256^i) end
    return x
  end)
  if ok then return v end
  return nil
end
local function fmt(v) if v==nil then return "TIDAK_TAHU" end return tostring(v) end
local function globals()
  return read(0x8013EA74,4),read(0x8013EA84,4),read(0x8013EAC8,4),
    read(0x8013EA6E,2),read(0x8013EA8A,2),read(0x8013EBB0,4),
    read(0x8013EB0C,4),read(0x80139F03,1)
end
local function money(m,i)
  if not m or not i or i>3 then return nil end
  return read(m+i*0x90+4,4)
end
local function fields(ptr)
  if not ptr or ptr<0x80000000 or ptr+0x22>0x80200000 then
    return nil,nil,nil,nil,nil,nil
  end
  local typ=read(ptr,1); local x=read(ptr+0x0e,2); local fee=read(ptr+0x1a,2)
  local packed=read(ptr+0x20,2)
  if packed==nil then return typ,x,fee,nil,nil,nil end
  return typ,x,fee,packed,math.floor(packed/16)%16,math.floor(packed/256)%16,math.floor(packed/4096)%16
end
local function snapshot(tag)
  local m,tb,tc,pi,ci,si,pending,es=globals()
  if not m or m<0x80000000 or m+0x400>=0x80200000 or not tb or tb<0x80000000 or tb>=0x80200000 or not tc or tc<1 or tc>MAX_TILES then
    log("RA2_SNAPSHOT_INVALID frame="..frame.." tile_count="..fmt(tc).." tile_base="..fmt(tb)); return
  end
  local ms={money(m,0),money(m,1),money(m,2),money(m,3)}
  for i=0,tc-1 do
    if boardRows>=2048 then boardOverflow=boardOverflow+1; break end
    local p=tb+i*0x124
    local typ,x,fee,packed,n1,n2,n3=fields(p)
    boardRows=boardRows+1
    board:write(table.concat({launch,frame,tag,i,fmt(typ),fmt(x),fmt(fee),fmt(packed),fmt(n1),fmt(n2),fmt(n3),
      fmt(ms[1]),fmt(ms[2]),fmt(ms[3]),fmt(ms[4])},"\t").."\n")
  end
  board:flush()
  log("RA2_SNAPSHOT tag="..tag.." frame="..frame.." tile_count="..tc)
end
local function onHit(pc)
  counts[pc]=(counts[pc] or 0)+1
  if traceRows>=3000 then traceOverflow=traceOverflow+1; return true end
  local ok,err=pcall(function()
    local r=PCSX.getRegisters(); local g=r.GPR.r
    local m,tb,tc,pi,ci,si,pending,es=globals()
    local ptr=nil
    if pc==0x800D2520 then ptr=tonumber(g[5]) elseif pc==0x800D46EC then ptr=tonumber(g[2]) end
    local typ,x,fee,packed,n1,n2,n3=fields(ptr)
    local ms={money(m,0),money(m,1),money(m,2),money(m,3)}
    traceRows=traceRows+1
    trace:write(table.concat({launch,frame,string.format("0x%08X",pc),names[pc],counts[pc],
      fmt(tonumber(r.pc)),fmt(tonumber(g[29])),fmt(tonumber(g[31])),fmt(tonumber(g[2])),fmt(tonumber(g[3])),
      fmt(tonumber(g[4])),fmt(tonumber(g[5])),fmt(tonumber(g[6])),fmt(tonumber(g[7])),
      fmt(tonumber(g[16])),fmt(tonumber(g[17])),fmt(tonumber(g[18])),fmt(tonumber(g[19])),fmt(tonumber(g[20])),
      fmt(m),fmt(tb),fmt(tc),fmt(pi),fmt(ci),fmt(si),fmt(pending),fmt(es),fmt(ptr),fmt(typ),fmt(x),fmt(fee),
      fmt(packed),fmt(n1),fmt(n2),fmt(n3),fmt(ms[1]),fmt(ms[2]),fmt(ms[3]),fmt(ms[4]),
      "TIDAK_TAHU","TIDAK_TAHU"},"\t").."\n")
    trace:flush()
  end)
  if not ok then log("RA2_HIT_READ_ERROR pc="..string.format("0x%08X",pc).." err="..tostring(err)) end
  return true
end
local bpRefs={}
for _,pc in ipairs(BPS) do
  local address=pc
  bpRefs[#bpRefs+1]=PCSX.addBreakpoint(address,"Exec",4,"RA2 read-only "..names[address],
    function(a,w,c) return onHit(address) end,"RA2_"..names[address])
end
local pad=PCSX.SIO0.slots[1].pads[1]
local B=PCSX.CONSTS.PAD.BUTTON
_G.ra2Loaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
  loaded=loaded+1;frame=0;log("RA2_STATE_LOADED=1")
end)
_G.ra2Vsync=PCSX.Events.createEventListener("GPU::Vsync",function()
  pre=pre+1
  if loaded==0 and not restorePending then
    restorePending=true;PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local ok,file=pcall(function() return assert(Support.File.open("resume/"..STATE)) end)
      if not ok or not file then log("RA2_STATE_OPEN_FAIL="..tostring(file));PCSX.quit(50);return end
      local yes,err=pcall(function() PCSX.loadSaveState(file) end);file:close()
      if not yes then log("RA2_RESTORE_FAIL="..tostring(err));PCSX.quit(51);return end
      log("RA2_RESTORE_RETURNED=1");PCSX.resumeEmulator()
    end)
    return
  end
  if loaded>0 then
    frame=frame+1
    if frame==20 then snapshot("BEFORE_CONFIRM") end
    if frame==30 then pad.setOverride(B.CIRCLE);log("RA2_INPUT=CIRCLE_PRESS_FRAME30") end
    if frame==36 then pad.clearOverride(B.CIRCLE);log("RA2_INPUT=CIRCLE_RELEASE_FRAME36") end
    if frame==180 then
      snapshot("AFTER_CONFIRM")
      local ok,err=pcall(function()
        trace:flush();trace:close();board:flush();board:close()
        local c=assert(io.open("counts.tsv","w"));c:write("pc\tlabel\thit_count\n")
        for _,pc in ipairs(BPS) do c:write(string.format("0x%08X\t%s\t%d\n",pc,names[pc],counts[pc] or 0)) end
        c:close()
      end)
      if not ok then log("RA2_OUTPUT_FAIL="..tostring(err));PCSX.quit(54);return end
      log("RA2_TRACE_ROWS="..traceRows);log("RA2_TRACE_OVERFLOW="..traceOverflow)
      log("RA2_BOARD_ROWS="..boardRows);log("RA2_BOARD_OVERFLOW="..boardOverflow)
      log("RA2_FRAMES=180");log("RA2_LAUNCH_COMPLETE=1")
      PCSX.pauseEmulator();PCSX.nextTick(function() PCSX.quit(0) end);return
    end
  elseif pre>=900 then log("RA2_RESTORE_TIMEOUT=1");PCSX.pauseEmulator();PCSX.nextTick(function() PCSX.quit(53) end) end
end)
log("RA2_READY=1 input=CIRCLE frames=30-35 memory=READ_ONLY breakpoints=EXEC")
'''
def sha256(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
def read_tsv(p):
    with p.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f,delimiter="\t"))
def lua_source(n):return LUA.replace("__LAUNCH__",str(n))
def self_test(root):
    assert len(STATE_SHA)==64 and len(ARTIFACT_SHA)==64
    assert set(BPS)=={0x800D15A8,0x800D2520,0x800D46EC}
    assert "PCSX.getMemoryAsFile()" in LUA and ":readAt(n,addr)" in LUA
    assert "writeAt" not in LUA and "PCSX.setGPR" not in LUA and "setMem" not in LUA
    assert "pad.setOverride(B.CIRCLE)" in LUA and "pad.clearOverride(B.CIRCLE)" in LUA
    targets=[".github/workflows/ra2-upgrade-probe.yml","tools/ra/RunRA2UpgradeProbe.py"]
    collisions=[]
    for wf in (root/".github"/"workflows").glob("*.yml"):
        if wf.name=="ra2-upgrade-probe.yml":continue
        lines=wf.read_text(encoding="utf-8",errors="replace").splitlines()
        for i,line in enumerate(lines):
            if line.strip()!="paths:":continue
            indent=len(line)-len(line.lstrip())
            for z in lines[i+1:]:
                if z.strip() and len(z)-len(z.lstrip())<=indent:break
                if z.strip().startswith("-"):
                    pat=z.strip()[1:].strip().strip('"').strip("'")
                    for t in targets:
                        if __import__("fnmatch").fnmatchcase(t,pat):collisions.append((wf.name,pat,t))
    if collisions:raise RuntimeError("WORKFLOW_PATH_COLLISION="+repr(collisions))
    return ["PYTHON_SOURCE=PASS","CHECKPOINT_HASH_FORMAT=PASS","BREAKPOINT_SET=PASS",
            "READ_ONLY_API=PASS","CIRCLE_SCENARIO=PASS","WORKFLOW_PATH_COLLISIONS=0"]
def launch(n,pcsx,bios,cue,work,out,state):
    d=work/f"launch{n}";d.mkdir(parents=True,exist_ok=True);(d/"resume").mkdir(exist_ok=True)
    shutil.copy2(state,d/"resume"/STATE_NAME)
    card=d/"control.mcd";card.write_bytes(bytes(131072))
    lua=d/"ra2.lua";lua.write_text(lua_source(n),encoding="utf-8")
    home=d/"home";home.mkdir(exist_ok=True);env=os.environ.copy()
    env.update({"HOME":str(home),"XDG_CONFIG_HOME":str(home/".config"),"XDG_DATA_HOME":str(home/".data"),"XDG_RUNTIME_DIR":str(home/".runtime")})
    for k in ("XDG_CONFIG_HOME","XDG_DATA_HOME","XDG_RUNTIME_DIR"):Path(env[k]).mkdir(parents=True,exist_ok=True)
    Path(env["XDG_RUNTIME_DIR"]).chmod(0o700)
    log=d/"pcsx.stdout.txt"
    cmd=["timeout","--signal=INT","--kill-after=10s","240s",str(pcsx),"-noupdate","-no-ui","-testmode",
         "-debugger","-interpreter","-bios",str(bios),"-iso",str(cue),"-memcard1",str(card),
         "-dofile",str(lua),"-softgpu","-logfile",str(d/"pcsx.log"),"-run"]
    with log.open("w",encoding="utf-8") as f:
        f.write(f"LAUNCH={n}\nGAMEPLAY_INPUT=CIRCLE frame30-35\n");f.flush()
        try:rc=subprocess.run(cmd,cwd=d,env=env,stdout=f,stderr=subprocess.STDOUT,check=False).returncode
        except Exception as e:rc=255;f.write("LAUNCH_EXCEPTION="+repr(e)+"\n")
    content=log.read_text(encoding="utf-8",errors="replace")
    (out/f"RA2_LAUNCH{n}_LOG.txt").write_text(content,encoding="utf-8")
    tr=d/"trace.tsv";bd=d/"board.tsv";co=d/"counts.tsv"
    loaded=content.count("RA2_STATE_LOADED=1")
    frames=max([int(x) for x in re.findall(r"RA2_FRAMES=(\d+)",content)] or [0])
    complete=(rc==0 and loaded==1 and frames==FRAMES and "RA2_LAUNCH_COMPLETE=1" in content and
              "RA2_INPUT=CIRCLE_PRESS_FRAME30" in content and "RA2_INPUT=CIRCLE_RELEASE_FRAME36" in content and
              tr.is_file() and bd.is_file() and co.is_file())
    if complete:
        shutil.copy2(tr,out/f"RA2_LAUNCH{n}_TRACE.tsv")
        shutil.copy2(bd,out/f"RA2_LAUNCH{n}_BOARD.tsv")
        shutil.copy2(co,out/f"RA2_LAUNCH{n}_COUNTS.tsv")
    return {"rc":rc,"loaded":loaded,"frames":frames,"complete":complete,"content":content}
def compare_boards(path1,path2,out):
    changes=[]
    for launch_id,path in (("1",path1),("2",path2)):
        keyed={}
        for row in read_tsv(path):
            keyed[(row["tag"],int(row["tile_index"]))]=row
        before={idx:r for (tag,idx),r in keyed.items() if tag=="BEFORE_CONFIRM"}
        after={idx:r for (tag,idx),r in keyed.items() if tag=="AFTER_CONFIRM"}
        for idx in sorted(set(before)&set(after)):
            b,a=before[idx],after[idx]
            fields=("tile_type","field_0e","fee_1a","packed_20","nibble_4_7","nibble_8_11","nibble_12_15")
            changed=[k for k in fields if b[k]!=a[k]]
            money=[k for k in ("money_p0","money_p1","money_p2","money_p3") if b[k]!=a[k]]
            if changed or money:
                changes.append([launch_id,idx,",".join(changed),b["field_0e"],a["field_0e"],
                    b["fee_1a"],a["fee_1a"],b["packed_20"],a["packed_20"],
                    b["nibble_4_7"],a["nibble_4_7"],b["nibble_8_11"],a["nibble_8_11"],
                    b["nibble_12_15"],a["nibble_12_15"],",".join(money),
                    ",".join(b["money_p"+str(i)] for i in range(4)),
                    ",".join(a["money_p"+str(i)] for i in range(4))])
    with (out/"RA2_ACTION_TILE_DIFFS.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,delimiter="\t",lineterminator="\n")
        w.writerow(["launch","tile_index","changed_fields","field_0e_before","field_0e_after",
          "fee_1a_before","fee_1a_after","packed_20_before","packed_20_after",
          "nibble_4_7_before","nibble_4_7_after","nibble_8_11_before","nibble_8_11_after",
          "nibble_12_15_before","nibble_12_15_after","changed_money_fields","money_p0_p3_before","money_p0_p3_after"])
        w.writerows(changes)
    return changes

def main():
    ap=argparse.ArgumentParser()
    for x in ("pcsx","bios","cue","work","out","state"):ap.add_argument("--"+x,required=True,type=Path)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);a.work.mkdir(parents=True,exist_ok=True)
    tests=self_test(Path(os.environ.get("GITHUB_WORKSPACE",str(Path.cwd()))));(a.out/"RA2_SELFTEST.txt").write_text("\n".join(tests)+"\n",encoding="utf-8")
    if not a.state.is_file() or a.state.stat().st_size!=STATE_SIZE or sha256(a.state)!=STATE_SHA:raise SystemExit("RA2_CHECKPOINT_VALIDATION_FAIL")
    r1=launch(1,a.pcsx,a.bios,a.cue,a.work,a.out,a.state)
    r2=launch(2,a.pcsx,a.bios,a.cue,a.work,a.out,a.state) if r1["complete"] else None
    identical=False;counts=[]
    if r1["complete"] and r2 and r2["complete"]:
        with (a.out/"RA2_LAUNCH1_TRACE.tsv").open(encoding="utf-8") as f:t1=list(csv.DictReader(f,delimiter="\t"))
        with (a.out/"RA2_LAUNCH2_TRACE.tsv").open(encoding="utf-8") as f:t2=list(csv.DictReader(f,delimiter="\t"))
        identical=[{k:v for k,v in r.items() if k!="launch"} for r in t1]==[{k:v for k,v in r.items() if k!="launch"} for r in t2]
        c1={r["pc"]:int(r["hit_count"]) for r in read_tsv(a.out/"RA2_LAUNCH1_COUNTS.tsv")}
        c2={r["pc"]:int(r["hit_count"]) for r in read_tsv(a.out/"RA2_LAUNCH2_COUNTS.tsv")}
        counts=[[f"0x{pc:08X}",label,c1.get(f"0x{pc:08X}",0),c2.get(f"0x{pc:08X}",0)] for pc,label in BPS.items()]
        with (a.out/"RA2_BREAKPOINT_COUNTS.tsv").open("w",encoding="utf-8",newline="") as f:
            w=csv.writer(f,delimiter="\t",lineterminator="\n");w.writerow(["pc","label","hits_launch1","hits_launch2"]);w.writerows(counts)
        tile_diffs=compare_boards(a.out/"RA2_LAUNCH1_BOARD.tsv",a.out/"RA2_LAUNCH2_BOARD.tsv",a.out)
    else:
        tile_diffs=[]
        with (a.out/"RA2_BREAKPOINT_COUNTS.tsv").open("w",encoding="utf-8",newline="") as f:
            w=csv.writer(f,delimiter="\t",lineterminator="\n");w.writerow(["pc","label","hits_launch1","hits_launch2"])
            for pc,label in BPS.items():w.writerow([f"0x{pc:08X}",label,"TIDAK_TAHU","TIDAK_TAHU"])
    overflow=sum(int(x) for content in (r1["content"],r2["content"] if r2 else "") for x in re.findall(r"RA2_TRACE_OVERFLOW=(\d+)",content))
    lines=["STATUS=BELUM","CONFIDENCE=K1",f"SOURCE_RUN={SOURCE_RUN}",f"ARTIFACT_ID={ARTIFACT_ID}",
      f"ARTIFACT_ZIP_SHA256={ARTIFACT_SHA}",f"CHECKPOINT={STATE_NAME}",f"CHECKPOINT_SHA256={STATE_SHA}",
      "LAUNCHES_REQUESTED=2",f"LAUNCH1_EXIT={r1['rc']}",f"LAUNCH1_RESTORE_EVENTS={r1['loaded']}",
      f"LAUNCH1_FRAMES={r1['frames']}",f"LAUNCH2_EXIT={r2['rc'] if r2 else 'NOT_RUN'}",
      f"LAUNCH2_RESTORE_EVENTS={r2['loaded'] if r2 else 'NOT_RUN'}",f"LAUNCH2_FRAMES={r2['frames'] if r2 else 'NOT_RUN'}",
      f"IDENTICAL_TRACE={'YES' if identical else 'NO_OR_TIDAK_TAHU'}",f"TRACE_OVERFLOW={overflow}",
      "GAMEPLAY_INPUT=CIRCLE at frames 30-35 after checkpoint restore",
      "BREAKPOINTS=EXEC 0x800D15A8,0x800D2520,0x800D46EC",
      "MEMORY_API=PCSX.getMemoryAsFile:readAt only","MEMORY_WRITE=NONE","REGISTER_WRITE=NONE",
      "TILE_RECORD=base 0x8013EA84 + index*0x124; read fields +0,+0x0E,+0x1A,+0x20",
      "PLAYER_MONEY=manager 0x8013EA74 + player*0x90 + 4 (read-only)",
      "EFFECT_ID=TIDAK TAHU","D=TIDAK TAHU",
      "LEVEL_MAPPING=TIDAK TAHU; packed +0x20 nibbles recorded without assigning semantics",
      "HIT_ZERO_MEANS=not hit under this bounded confirmation scenario; not proof unreachable",
      f"ACTION_TILE_DIFF_ROWS={len(tile_diffs) if r1['complete'] and r2 and r2['complete'] else 'TIDAK_TAHU'}",
      "ACTUAL_UPGRADE=TIDAK TAHU unless a level-field change is tied to the confirmation action",
      "BIOS_ROM_SAVESTATE_RAM_DUMP_COMMITTED=no"]
    (a.out/"RA2_RUNTIME_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines))
    if not r1["complete"] or not r2 or not r2["complete"] or overflow:raise SystemExit(1)
if __name__=="__main__":main()
