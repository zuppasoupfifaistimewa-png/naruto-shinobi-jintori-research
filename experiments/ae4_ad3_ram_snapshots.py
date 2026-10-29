#!/usr/bin/env python3
"""AE4 only: replay prior, byte-identical AD3 hybrids and report RAM hash/three words."""
import argparse, hashlib, os, re, subprocess, time, shutil
from pathlib import Path
from collections import defaultdict

TARGET_SHA="00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA="9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
EXPECTED={
3:"78d937e5dabd8b2ebdf949176fad8557f82d6e0759116511530b18b8c841dca4",
4:"142f82698ab689518a115e0cdff32ce26d9c52a1cfd8a225fe36c2c1827f67ed",
5:"08f907c3b7f630369d7eca7d2157572fda68009a4caaee1d79827317373a3f6a",
8:"967be929b23017796ffc2faaad8a42e1d9d66c26e335d21d2a92ec0c63596967",
10:"0617e540eb1a6d0704a2637a50e37766b622870c08d0b1853f8eabeff1ad02e1"}
ADDRS=(0x80070EB8,0x80070F6C,0x8013A554)

def sha(b): return hashlib.sha256(b).hexdigest()
def vi(b,p):
    value=shift=start=0
    while p<len(b) and shift<=70:
        q=b[p];p+=1;value|=(q&127)<<shift
        if not q&128:return value,p,p-start
        shift+=7
    raise ValueError("bad varint at %d"%start)
def encvi(n):
    z=bytearray()
    while n>127:z.append((n&127)|128);n>>=7
    z.append(n);return bytes(z)
def parse(b):
    out=[];p=0
    while p<len(b):
        start=p;tag,p,_=vi(b,p);n,w=tag>>3,tag&7
        if not n:raise ValueError("field number zero")
        if w==0:ps=p;_,p,_=vi(b,p);pe=p
        elif w==1:ps=p;pe=p+8;p=pe
        elif w==2:ln,p,_=vi(b,p);ps=p;pe=p+ln;p=pe
        elif w==5:ps=p;pe=p+4;p=pe
        else:raise ValueError("unsupported wire %d"%w)
        if p>len(b):raise ValueError("truncated field")
        out.append({"n":n,"w":w,"payload":b[ps:pe],"enc":b[start:p]})
    return out
def one(b,n):
    xs=[r for r in parse(b) if r["n"]==n and r["w"]==2]
    if len(xs)!=1:raise ValueError("expected one field %d; saw %d"%(n,len(xs)))
    return xs[0]["payload"]
def replace_top(base,n,target_record):
    out=bytearray();inserted=False
    for r in parse(base):
        if r["n"]==n:
            if not inserted:out.extend(target_record);inserted=True
        else:out.extend(r["enc"])
    if not inserted:out.extend(target_record)
    return bytes(out)
def ram_info(state):
    ram=one(one(state,3),1)[:0x200000]
    words=[]
    for address in ADDRS:
        raw=ram[address-0x80000000:address-0x80000000+4]
        words.append("0x%08X raw=%s LE32=0x%08X"%(address,raw.hex(" "),int.from_bytes(raw,"little")))
    return sha(ram),"; ".join(words)
def line(*xs):
    return "\t".join(str(x).replace("\t"," ").replace("\n","\\n") for x in xs)+"\n"
def excerpt(src,dst):
    ls=src.read_text(errors="replace").splitlines()
    if len(ls)>290:ls=ls[:40]+["[... middle omitted; full raw log is sibling]"]+ls[-250:]
    dst.write_text("\n".join(ls)+"\n",encoding="utf-8")
def main():
    ap=argparse.ArgumentParser()
    for n in ("target","control","work","output","pcsx-bin","appdir","bios","cue","card"):ap.add_argument("--"+n,required=True)
    a=ap.parse_args();work=Path(a.work);out=Path(a.output);raw=out/"raw";ex=out/"excerpts"
    for p in (work/"logs",work/"resume",work/"runtime",work/"home/.config",work/"home/.local/share",work/"home/runtime",raw,ex):p.mkdir(parents=True,exist_ok=True)
    target=Path(a.target).read_bytes();control=Path(a.control).read_bytes()
    if sha(target)!=TARGET_SHA or sha(control)!=CONTROL_SHA:raise ValueError("checkpoint SHA mismatch")
    metas=["AE4 only; PCSX-Redux pin 0c3572c3d","Target SHA256="+sha(target),"Control SHA256="+sha(control),
      "AppImage SHA256=c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c",
      "Flags=-noupdate -no-debugger -no-gdb -softgpu -dynarec -stdout -lua_stdout",
      "Per-launch timeout=25s; timeout is inconclusive, never counted as crash",
      "No controller input; VSync marker target=180 after SaveStateLoaded; RAM snapshots stay in ephemeral workspace"]
    app=Path(a.appdir);env=os.environ.copy()
    env.update({"DISPLAY":":99","HOME":str(work/"home"),"XDG_CONFIG_HOME":str(work/"home/.config"),
      "XDG_DATA_HOME":str(work/"home/.local/share"),"XDG_RUNTIME_DIR":str(work/"home/runtime"),
      "LIBGL_ALWAYS_SOFTWARE":"1","LD_LIBRARY_PATH":str(app/"usr/lib")+":"+str(app/"usr/lib/x86_64-linux-gnu"),
      "QT_PLUGIN_PATH":str(app/"usr/plugins"),"QT_QPA_PLATFORM_PLUGIN_PATH":str(app/"usr/plugins/platforms"),"QML2_IMPORT_PATH":str(app/"usr/qml")})
    try:(work/"home/runtime").chmod(0o700)
    except OSError:pass
    pad=work/"pad.lua"
    pad.write_text("PCSX.settings.pads[1].DeviceType = 'Analog'\nPCSX.settings.pads[1].Connected = true\nPCSX.SIO0.slots[1].pads[1].map()\nprint('AE_NO_INPUT_CONTROLLER=1')\n",encoding="utf-8")
    lua=work/"restore.lua"
    lua.write_text(r'''
if io.stdout then io.stdout:setvbuf("no") end
local vsync,started,loaded,after,pending=0,false,false,0,false
local function log(s) print(s);pcall(function()io.stdout:flush()end) end
_G.aeLoaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()loaded=true;after=0;log("AE_EVENT_SAVE_STATE_LOADED=1")end)
local function snap()
 local ok,err=pcall(function()
  local s=PCSX.createSaveState()
  local f=assert(Support.File.open("runtime/current.sstate","TRUNCATE"))
  f:writeMoveSlice(s);f:close()
 end)
 log(ok and "AE_RAM_STATE_CAPTURE=PASS" or ("AE_RAM_STATE_CAPTURE=FAIL "..tostring(err)))
 PCSX.nextTick(function()PCSX.quit(ok and 0 or 62)end)
end
_G.aeVsync=PCSX.Events.createEventListener("GPU::Vsync",function()
 vsync=vsync+1
 if not started then
  started=true;local path=os.getenv("AE_TEST_STATE") or "resume/case.sstate"
  log("AE_LOAD_BEGIN=1 path="..path.." vsync="..vsync.." controller=NONE")
  PCSX.pauseEmulator();PCSX.nextTick(function()
   local okf,f=pcall(function()return assert(Support.File.open(path))end)
   if not okf or not f then log("AE_STATE_OPEN_FAIL="..tostring(f));PCSX.quit(50);return end
   local ok,e=pcall(function()PCSX.loadSaveState(f)end);f:close()
   if not ok then log("AE_LOAD_LUA_ERROR="..tostring(e));PCSX.quit(51);return end
   log("AE_LOAD_CALL_RETURNED=1");PCSX.resumeEmulator()
  end);return
 end
 if loaded then
  after=after+1
  if after>=180 and not pending then pending=true;log("AE_POST_LOAD_VSYNC=180");PCSX.pauseEmulator();PCSX.nextTick(snap) end
 elseif vsync>=1200 then log("AE_LOAD_EVENT_TIMEOUT=1");PCSX.pauseEmulator();PCSX.nextTick(function()PCSX.quit(53)end) end
end)
log("AE_RESTORE_PROBE_READY_NO_INPUT=1")
'''.lstrip(),encoding="utf-8")
    results=[];summary=[];ramrows=[]
    for field,expected in EXPECTED.items():
        rec=[r for r in parse(target) if r["n"]==field]
        if len(rec)!=1:raise ValueError("field %d count=%d"%(field,len(rec)))
        hybrid=replace_top(control,field,rec[0]["enc"]); h=sha(hybrid); identical=h==expected
        case="ae4-ad3-field%d-target-in-control"%field
        statefile=work/"resume"/(case+".sstate");statefile.write_bytes(hybrid)
        outcomes=[]
        for attempt in (1,2):
            label="%s-attempt%d"%(case,attempt);g=raw/(label+".gdb.txt");p=raw/(label+".pcsx.txt");snapfile=work/"runtime/current.sstate"
            for q in (g,p,snapfile):
                try:q.unlink()
                except FileNotFoundError:pass
            gc=work/"gdb.commands"
            gc.write_text("""set pagination off
set confirm off
set print thread-events off
handle SIGSEGV stop print pass
handle SIGABRT stop print pass
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
            te=env.copy();te["AE_TEST_STATE"]="resume/"+statefile.name
            cmd=["timeout","--signal=INT","--kill-after=5s","25s","gdb","--quiet","--nx","--batch","--return-child-result","-x",str(gc),"--args",a.pcsx_bin,
              "-noupdate","-no-debugger","-no-gdb","-bios",a.bios,"-iso",a.cue,"-memcard1",a.card,"-exec",pad.read_text(),
              "-dofile",str(lua),"-softgpu","-dynarec","-stdout","-lua_stdout","-logfile",str(p),"-run"]
            start=time.time()
            with g.open("wb") as dest:
                try:proc=subprocess.run(cmd,cwd=work,env=te,stdout=dest,stderr=subprocess.STDOUT,check=False);rc=proc.returncode
                except Exception as er:rc=255;dest.write(("AE_LAUNCH_EXCEPTION="+repr(er)+"\n").encode())
            if not p.exists():p.write_text("AE_PCSX_LOG_NOT_CREATED\n")
            txt=g.read_text(errors="replace")
            if re.search(r"(?:Thread \d+ .* received signal|Program received signal|Program terminated with signal)\s+SIGSEGV",txt):status="SIGSEGV"
            elif re.search(r"(?:Thread \d+ .* received signal|Program received signal|Program terminated with signal)\s+SIGABRT",txt):status="SIGABRT"
            elif "AE_POST_LOAD_VSYNC=180" in txt and "AE_RAM_STATE_CAPTURE=PASS" in txt:status="POST_LOAD_VSYNC=180"
            elif rc in (-9,124,137,143) or "SIGINT" in txt:status="INCONCLUSIVE_TIMEOUT"
            else:status="INCONCLUSIVE"
            pcm=re.search(r"(?:=>\s*)?(0x[0-9a-fA-F]+):\s+\w",txt);pc=pcm.group(1) if pcm else "-"
            ramhash,words="-","-"
            if status=="POST_LOAD_VSYNC=180" and snapfile.exists():
                try:
                    ramhash,words=ram_info(snapfile.read_bytes())
                    ramrows.append([case,attempt,h,ramhash,words])
                except Exception as er:words="RAM_PARSE_ERROR="+repr(er)
            try:snapfile.unlink()
            except OSError:pass
            results.append([case,attempt,h,status,pc,rc,ramhash,words,"%.3f"%(time.time()-start),
              "raw/"+g.name,"raw/"+p.name])
            excerpt(g,ex/(g.name+".first40-last250.txt"));excerpt(p,ex/(p.name+".first40-last250.txt"))
            outcomes.append(status)
        outc="POST_LOAD_VSYNC_180_BOTH" if outcomes==["POST_LOAD_VSYNC=180"]*2 else ("SIGSEGV_BOTH" if outcomes==["SIGSEGV"]*2 else ("SIGABRT_BOTH" if outcomes==["SIGABRT"]*2 else ("INCONCLUSIVE_TIMEOUT_BOTH" if outcomes==["INCONCLUSIVE_TIMEOUT"]*2 else "MIXED_OR_INCONCLUSIVE")))
        summary.append([case,field,expected,h,identical,";".join(outcomes),outc,";".join(r[4] for r in results[-2:])])
        metas.append("Field %d expected_sha=%s reconstructed_sha=%s byte_identical=%s result=%s"%(field,expected,h,identical,outc))
    (out/"ae4-runtime-environment.txt").write_text("\n".join(metas)+"\n",encoding="utf-8")
    with (out/"ae4-case-summary.tsv").open("w",encoding="utf-8") as f:
        f.write(line("case","field","expected_sha","actual_sha","byte_identical","attempt_outcomes","two_launch_outcome","pcs_each"))
        for r in summary:f.write(line(*r))
    with (out/"ae4-runtime-results.tsv").open("w",encoding="utf-8") as f:
        f.write(line("case","attempt","hybrid_sha256","result","pc_or_status","wrapper_rc","ram_2mib_sha256","raw_words_at_addresses","seconds","gdb_log","pcsx_log"))
        for r in results:f.write(line(*r))
    with (out/"ae4_ram_snapshots.tsv").open("w",encoding="utf-8") as f:
        f.write(line("case","attempt","hybrid_sha256","RAM_2MiB_sha256","raw_words"))
        for r in ramrows:f.write(line(*r))
    manifest=[]
    for q in sorted(raw.glob("*.txt")):manifest.append("%s  %s  bytes=%d"%(sha(q.read_bytes()),q.relative_to(out),q.stat().st_size))
    (out/"raw-log-sha256.txt").write_text("\n".join(manifest)+"\n",encoding="utf-8")
    print((out/"ae4-case-summary.tsv").read_text())
    print("AE4_SUCCESSFUL_RAM_SNAPSHOTS=%d"%len(ramrows))
if __name__=="__main__":main()
