#!/usr/bin/env python3
"""Focused recursive follow-up for the smallest crashing SPU channel message."""
import argparse, hashlib, os, re, subprocess, time, shutil
from pathlib import Path
from collections import defaultdict

def sha(b): return hashlib.sha256(b).hexdigest()
def vi(b,p):
    val=shift=start=0
    while p<len(b) and shift<=70:
        c=b[p]; p+=1; val|=(c&127)<<shift
        if not c&128: return val,p,p-start
        shift+=7
    raise ValueError("bad varint at "+str(start))
def encvi(n):
    z=bytearray()
    while n>127: z.append((n&127)|128); n>>=7
    z.append(n); return bytes(z)
def parse(b):
    out=[]; p=0
    while p<len(b):
        st=p; tag,p,_=vi(b,p); n,w=tag>>3,tag&7
        if not n: raise ValueError("field 0")
        if w==0:
            ps=p; _,p,_=vi(b,p); pe=p
        elif w==1: ps=p; pe=p+8; p=pe
        elif w==2:
            ln,p,_=vi(b,p); ps=p; pe=p+ln; p=pe
        elif w==5: ps=p; pe=p+4; p=pe
        else: raise ValueError("unsupported wire "+str(w))
        if p>len(b): raise ValueError("truncated field")
        out.append(dict(n=n,w=w,st=st,ps=ps,pe=pe,end=p,pay=b[ps:pe],enc=b[st:p]))
    return out
def groups(rs):
    d=defaultdict(list)
    for r in rs: d[r["n"]].append(r)
    return d
def one(b,n):
    xs=[r for r in parse(b) if r["n"]==n and r["w"]==2]
    if len(xs)!=1: raise ValueError("expected exactly one field %d wire2, saw %d"%(n,len(xs)))
    return xs[0]["pay"]
def encmsg(n,p): return encvi((n<<3)|2)+encvi(len(p))+p
def replace_occ(b,n,i,newenc):
    rs=parse(b); out=bytearray(); done=False
    for r in rs:
        if r["n"]==n:
            idx=sum(1 for q in rs[:rs.index(r)] if q["n"]==n)
            if idx==i:
                if newenc is not None: out.extend(newenc)
                done=True; continue
        out.extend(r["enc"])
    if not done and newenc is not None:
        # append the field if it is absent; caller uses existing message-field keys in normal cases
        out.extend(newenc)
    return bytes(out)
def replace_top(b,n,newenc):
    rs=parse(b); out=bytearray(); inserted=False
    for r in rs:
        if r["n"]==n:
            if not inserted:
                out.extend(newenc); inserted=True
        else: out.extend(r["enc"])
    if not inserted: out.extend(newenc)
    return bytes(out)
def selective(base,source,keys):
    """Replace selected (field number, zero-based occurrence) with source encoded occurrence."""
    br, sr = parse(base), parse(source); bg,sg=groups(br),groups(sr); keys=set(keys)
    out=bytearray(); seen=defaultdict(int)
    for r in br:
        n=r["n"]; i=seen[n]; seen[n]+=1
        if (n,i) in keys:
            if i<len(sg.get(n,[])): out.extend(sg[n][i]["enc"])
        else: out.extend(r["enc"])
        if i==len(bg[n])-1:
            for extra in range(len(bg[n]),len(sg.get(n,[]))):
                if (n,extra) in keys: out.extend(sg[n][extra]["enc"])
    for n in sorted(set(sg)-set(bg)):
        for i,r in enumerate(sg[n]):
            if (n,i) in keys: out.extend(r["enc"])
    return bytes(out)
def diffs(a,b):
    ag,bg=groups(parse(a)),groups(parse(b)); out=[]
    for n in sorted(set(ag)|set(bg)):
        for i in range(max(len(ag.get(n,[])),len(bg.get(n,[])))):
            aa=ag[n][i]["enc"] if i<len(ag.get(n,[])) else None
            bb=bg[n][i]["enc"] if i<len(bg.get(n,[])) else None
            if aa!=bb: out.append((n,i))
    return out
def replace_channel_in_state(state, channel_number, new_channel):
    spu=one(state,6); sr=parse(spu); seen=0; out=bytearray()
    for r in sr:
        if r["n"]==6 and r["w"]==2:
            if seen==channel_number: out.extend(encmsg(6,new_channel))
            else: out.extend(r["enc"])
            seen+=1
        else: out.extend(r["enc"])
    if seen<=channel_number: raise ValueError("channel index missing")
    return replace_top(state,6,encmsg(6,bytes(out)))
def replace_channel_data(state, channel_number, data_payload):
    spu=one(state,6); channels=[r for r in parse(spu) if r["n"]==6 and r["w"]==2]
    if channel_number>=len(channels): raise ValueError("channel index missing")
    channel=channels[channel_number]["pay"]
    new_channel=replace_top(channel,1,encmsg(1,data_payload))
    return replace_channel_in_state(state,channel_number,new_channel)
def ram_info(state):
    memory=one(state,3); ram=one(memory,1)
    actual=ram[:0x200000]
    words=[]
    for addr in (0x80070EB8,0x80070F6C,0x8013A554):
        raw=actual[addr-0x80000000:addr-0x80000000+4]
        words.append("0x%08X bytes=%s LE32=0x%08X"%(addr,raw.hex(" "),int.from_bytes(raw,"little")))
    return sha(actual),len(ram),"; ".join(words)
def write_excerpt(src,dst):
    lines=src.read_text(errors="replace").splitlines()
    if len(lines)>290: lines=lines[:40]+["[... omitted middle; full raw log retained]"]+lines[-250:]
    dst.write_text("\n".join(lines)+"\n",encoding="utf-8")
def line(*xs): return "\t".join(str(x).replace("\t"," ").replace("\n","\\n") for x in xs)+"\n"

def main():
    ap=argparse.ArgumentParser()
    for arg in ("target","control","work","output","pcsx-bin","appdir","bios","cue","card"): ap.add_argument("--"+arg,required=True)
    a=ap.parse_args(); work=Path(a.work); out=Path(a.output); raw=out/"raw"; excerpt=out/"excerpts"
    for d in (work/"logs",work/"resume",work/"runtime",work/"home/.config",work/"home/.local/share",work/"home/runtime",raw,excerpt): d.mkdir(parents=True,exist_ok=True)
    target=Path(a.target).read_bytes(); control=Path(a.control).read_bytes()
    assert sha(target)=="00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
    assert sha(control)=="9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
    # The prior AE run identified SPU field 6 / Channel occurrence 2 as a reproducibly sufficient child.
    target_spu,control_spu=one(target,6),one(control,6)
    tc=[r for r in parse(target_spu) if r["n"]==6 and r["w"]==2]
    cc=[r for r in parse(control_spu) if r["n"]==6 and r["w"]==2]
    if len(tc)<2 or len(cc)<2: raise ValueError("expected at least two SPU channel records")
    tchan,cchan=tc[1]["pay"],cc[1]["pay"]
    channel_diff=diffs(cchan,tchan)
    report=["AE1 RECURSIVE FOLLOW-UP: descend into SPU field 6 / repeated Channel occurrence 2",
      "TARGET="+sha(target),"CONTROL="+sha(control),
      "Prior evidence: whole SPU channel occurrence 2 target->control base caused SIGSEGV at same PC twice; reverse replacement in target base also SIGSEGV twice.",
      "Channel occurrence 2 direct field differences (field#occurrence): "+", ".join("%d#%d"%(n,i+1) for n,i in channel_diff),
      "Pin: PCSX-Redux 0c3572c3d; Channel schema: field 1=data (ChannelData), field 2=adsr (message), field 3=adsr_ex (message)."]
    direct_keys=[k for k in channel_diff if k[0] in (1,2,3)]
    report.append("Direct candidate channel message fields: "+", ".join("%d#%d"%(n,i+1) for n,i in direct_keys))
    pad=work/"pad.lua"
    pad.write_text("PCSX.settings.pads[1].DeviceType = 'Analog'\nPCSX.settings.pads[1].Connected = true\nPCSX.SIO0.slots[1].pads[1].map()\nprint('AE_NO_INPUT_CONTROLLER=1')\n",encoding="utf-8")
    lua=work/"restore.lua"
    lua.write_text(r'''
if io.stdout then io.stdout:setvbuf("no") end
local vsync,started,loaded,after,pending=0,false,false,0,false
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
_G.aeLoaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function() loaded=true;after=0;log("AE_EVENT_SAVE_STATE_LOADED=1") end)
local function snap()
 local ok,err=pcall(function() local s=PCSX.createSaveState();local f=assert(Support.File.open("runtime/current.sstate","TRUNCATE"));f:writeMoveSlice(s);f:close() end)
 log(ok and "AE_RAM_STATE_CAPTURE=PASS" or ("AE_RAM_STATE_CAPTURE=FAIL "..tostring(err)))
 PCSX.nextTick(function() PCSX.quit(ok and 0 or 62) end)
end
_G.aeVsync=PCSX.Events.createEventListener("GPU::Vsync",function()
 vsync=vsync+1
 if not started then
  started=true;local path=os.getenv("AE_TEST_STATE") or "resume/case.sstate";log("AE_LOAD_BEGIN=1 path="..path.." vsync="..vsync.." controller=NONE")
  PCSX.pauseEmulator()
  PCSX.nextTick(function()
   local okf,f=pcall(function() return assert(Support.File.open(path)) end)
   if not okf or not f then log("AE_STATE_OPEN_FAIL="..tostring(f));PCSX.quit(50);return end
   local ok,e=pcall(function() PCSX.loadSaveState(f) end);f:close()
   if not ok then log("AE_LOAD_LUA_ERROR="..tostring(e));PCSX.quit(51);return end
   log("AE_LOAD_CALL_RETURNED=1");PCSX.resumeEmulator()
  end);return
 end
 if loaded then after=after+1;if after>=180 and not pending then pending=true;log("AE_POST_LOAD_VSYNC=180");PCSX.pauseEmulator();PCSX.nextTick(snap) end
 elseif vsync>=900 then log("AE_LOAD_EVENT_TIMEOUT=1");PCSX.pauseEmulator();PCSX.nextTick(function() PCSX.quit(53) end) end
end)
log("AE_RESTORE_PROBE_READY_NO_INPUT=1")
'''.lstrip(),encoding="utf-8")
    appdir=Path(a.appdir)
    env=os.environ.copy(); env.update({"DISPLAY":":99","HOME":str(work/"home"),"XDG_CONFIG_HOME":str(work/"home/.config"),"XDG_DATA_HOME":str(work/"home/.local/share"),"XDG_RUNTIME_DIR":str(work/"home/runtime"),"LIBGL_ALWAYS_SOFTWARE":"1","LD_LIBRARY_PATH":str(appdir/"usr/lib")+":"+str(appdir/"usr/lib/x86_64-linux-gnu"),"QT_PLUGIN_PATH":str(appdir/"usr/plugins"),"QT_QPA_PLATFORM_PLUGIN_PATH":str(appdir/"usr/plugins/platforms"),"QML2_IMPORT_PATH":str(appdir/"usr/qml")})
    try:(work/"home/runtime").chmod(0o700)
    except OSError:pass
    results=[]; cases=[]; ram=[]; cache={}
    def run_case(name,state,definition):
      path=work/"resume"/(name+".sstate");path.write_bytes(state); h=sha(state); outs=[]; pcs=[]
      for attempt in (1,2):
        label="%s-attempt%d"%(name,attempt); gl=raw/(label+".gdb.txt"); pl=raw/(label+".pcsx.txt"); current=work/"runtime/current.sstate"
        for x in (gl,pl,current):
          try:x.unlink()
          except FileNotFoundError:pass
        cmd=work/"gdb.commands"
        cmd.write_text("""set pagination off
set confirm off
set print thread-events off
handle SIGSEGV stop print nopass
handle SIGABRT stop print nopass
run
python
import gdb
inf=gdb.selected_inferior()
if getattr(inf,'pid',0):
 print('AE_GDB_CONTEXT_BEGIN')
 for c in ('info threads','x/3i $pc','info registers','info proc mappings','bt','thread apply all bt 40'):
  print('AE_GDB_COMMAND_BEGIN: '+c)
  try:gdb.execute(c)
  except Exception as e:print('AE_GDB_COMMAND_UNAVAILABLE: '+str(e))
  print('AE_GDB_COMMAND_END: '+c)
 print('AE_GDB_CONTEXT_END')
 try:gdb.execute('continue')
 except Exception as e:print('AE_GDB_CONTINUE_RESULT: '+str(e))
else: print('AE_GDB_CONTEXT_STATUS=INFERIOR_EXITED')
end
""",encoding="utf-8")
        te=env.copy();te["AE_TEST_STATE"]="resume/"+path.name
        call=["timeout","--signal=INT","--kill-after=2s","8s","gdb","--quiet","--nx","--batch","--return-child-result","-x",str(cmd),"--args",a.pcsx_bin,"-noupdate","-no-debugger","-no-gdb","-bios",a.bios,"-iso",a.cue,"-memcard1",a.card,"-exec",pad.read_text(),"-dofile",str(lua),"-softgpu","-dynarec","-stdout","-lua_stdout","-logfile",str(pl),"-run"]
        started=time.time()
        with gl.open("wb") as dest:
          try: p=subprocess.run(call,cwd=work,env=te,stdout=dest,stderr=subprocess.STDOUT,check=False);rc=p.returncode
          except Exception as e:rc=255;dest.write(("AE_LAUNCH_ERROR="+repr(e)+"\n").encode())
        if not pl.exists():pl.write_text("AE_PCSX_LOG_NOT_CREATED\n")
        textlog=gl.read_text(errors="replace")
        if re.search(r"(?:Thread \d+ .* received signal|Program received signal|Program terminated with signal)\s+SIGSEGV",textlog):status="SIGSEGV"
        elif re.search(r"(?:Thread \d+ .* received signal|Program received signal|Program terminated with signal)\s+SIGABRT",textlog):status="SIGABRT"
        elif "AE_POST_LOAD_VSYNC=180" in textlog and "AE_RAM_STATE_CAPTURE=PASS" in textlog:status="POST_LOAD_VSYNC=180"
        elif "SIGINT" in textlog or rc in (-9,124,137,143):status="INCONCLUSIVE_TIMEOUT"
        else:status="INCONCLUSIVE"
        pc=re.search(r"(?:=>\s*)?(0x[0-9a-fA-F]+):\s+\w",textlog)
        pcval=pc.group(1) if pc else "-"
        ramhash,rambytes,words="-",0,"-"
        if status=="POST_LOAD_VSYNC=180" and current.exists():
          try:ramhash,rambytes,words=ram_info(current.read_bytes());ram.append([name,attempt,h,ramhash,rambytes,words])
          except Exception as e:words="RAM_PARSE_ERROR="+repr(e)
        try:current.unlink()
        except OSError:pass
        results.append([name,attempt,h,status,pcval,rc,"139" if status=="SIGSEGV" else ("134" if status=="SIGABRT" else ("0" if status=="POST_LOAD_VSYNC=180" else "TIDAK_TAHU")),ramhash,rambytes,words,gl.relative_to(out),pl.relative_to(out),"%.3f"%(time.time()-started)])
        write_excerpt(gl,excerpt/(gl.name+".first40-last250.txt"));write_excerpt(pl,excerpt/(pl.name+".first40-last250.txt"))
        outs.append(status);pcs.append(pcval)
      outcome="SIGSEGV_BOTH" if outs==["SIGSEGV","SIGSEGV"] else ("POST_LOAD_VSYNC_180_BOTH" if outs==["POST_LOAD_VSYNC=180"]*2 else ("INCONCLUSIVE_TIMEOUT_BOTH" if outs==["INCONCLUSIVE_TIMEOUT"]*2 else "MIXED_OR_INCONCLUSIVE"))
      cases.append([name,outcome,";".join(outs),";".join(pcs),h,definition]);return outcome
    def make_channel_candidate(keys):
      chan=selective(cchan,tchan,keys)
      # Channel's fields 1=data, 2=adsr, 3=adsr_ex are protobuf message fields.
      return replace_channel_in_state(control,1,chan)
    # A: test each changed direct field on Channel occurrence 2 in control base.
    direct_out={}
    for key in direct_keys:
      outc=run_case("direct-channel-field-%d"%key[0],make_channel_candidate({key}),
                    "control state; only target SPU channel occurrence 2 field %d from target"%key[0])
      direct_out[key]=outc
    # B: descend into each direct field that is independently sufficient.
    for key,outc in direct_out.items():
      if outc!="SIGSEGV_BOTH": continue
      n,_=key
      c_payload=one(cchan,n)
      t_payload=one(tchan,n)
      nested_diff=diffs(c_payload,t_payload)
      report.append("Field inside Channel #2 field %d: base=control, source=target; child diffs=%d; keys=%s"%(n,len(nested_diff),", ".join("%d#%d"%(x,y+1) for x,y in nested_diff)))
      for child in nested_diff:
        # Copy only one field inside the parent message (data/adsr/adsr_ex) while everything else stays control.
        new_parent=selective(c_payload,t_payload,{child})
        new_channel=replace_top(cchan,n,encmsg(n,new_parent))
        hybrid=replace_channel_in_state(control,1,new_channel)
        run_case("nested-channel-field%d-child%d-occ%d"%(n,child[0],child[1]+1),hybrid,
                 "control state; target channel[2].field%d payload contains only target child field %d occurrence %d"%(n,child[0],child[1]+1))
    # AE2 necessity check for the deepest sufficient field found so far:
    # replace only Channel[2].data.current (field 8 occurrence 1) in target with control bytes.
    control_data = one(cchan,1)
    target_data = one(tchan,1)
    reverse_current_data = selective(target_data,control_data,{(8,0)})
    reverse_current_channel = replace_top(tchan,1,encmsg(1,reverse_current_data))
    reverse_current_state = replace_channel_in_state(target,1,reverse_current_channel)
    reverse_current_outcome = run_case(
      "ae2-target-current-pointer-field8-from-control",
      reverse_current_state,
      "target base; only SPU.channel[2].data.current (field 8 occurrence 1) swapped to control encoding"
    )
    with (out/"runtime-results.tsv").open("w",encoding="utf-8") as f:
      f.write(line("case","attempt","hybrid_sha256","result","pc_or_status","gdb_wrapper_exit","emulator_exit_code","ram_2mib_sha256","serialized_ram_field_bytes","raw_words_at_addresses","gdb_log","pcsx_log","seconds"))
      for r in results:f.write(line(*r))
    with (out/"runtime-case-summary.tsv").open("w",encoding="utf-8") as f:
      f.write(line("case","two_launch_outcome","attempt_outcomes","PC_or_status_each","hybrid_sha256","definition"))
      for r in cases:f.write(line(*r))
    with (out/"ae4_ram_snapshots.tsv").open("w",encoding="utf-8") as f:
      f.write(line("case","attempt","hybrid_sha256","RAM_2MiB_sha256","serialized_ram_field_bytes","raw_words"))
      for r in ram:f.write(line(*r))
    radd=report.append
    radd("Direct Channel field outcomes:")
    for k,v in direct_out.items():radd(" channel[2].field%d => %s"%(k[0],v))
    radd("AE2 necessity check: target base with only Channel[2].data.current (field 8) swapped from control => %s." % reverse_current_outcome)
    radd("Schema mapping: src/spu/types.h at PCSX-Redux pin 0c3572c3d defines Chan::CurrPtr as field 8, TYPESTRING(\"current\"); permalink=https://github.com/pcsx-redux/pcsx-redux/blob/0c3572c3d/src/spu/types.h")
    radd("Runtime cases=%d; two-launch snapshots reaching post-load=180=%d"%(len(cases),len(ram)))
    radd("No SIGINT/timeouts were counted as crashes; timeout outcomes are INCONCLUSIVE_TIMEOUT.")
    radd("The prior AE first-level all-child reconstruction did not match target SPU bytes due serialization ordering/add/remove ordering; therefore use these direct-parent-message trials to establish a narrow sufficient child, not global field byte identity.")
    (out/"AE1_CHANNEL_RECURSIVE_RESULTS.txt").write_text("\n".join(report)+"\n",encoding="utf-8")
    manifest=[]
    for p in sorted(raw.glob("*.txt")):manifest.append("%s  %s  bytes=%d"%(sha(p.read_bytes()),p.relative_to(out),p.stat().st_size))
    (out/"raw-log-sha256.txt").write_text("\n".join(manifest)+"\n",encoding="utf-8")
    print((out/"AE1_CHANNEL_RECURSIVE_RESULTS.txt").read_text())
    print("AE1_CHANNEL_TESTS=%d launch_count=%d RAM_snapshots=%d"%(len(cases),len(results),len(ram)))
if __name__=="__main__":main()
