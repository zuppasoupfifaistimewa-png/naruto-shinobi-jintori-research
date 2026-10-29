#!/usr/bin/env python3
"""Long-timeout AE1 nested-channel probe; no controller input or persisted game data."""
from __future__ import annotations
import argparse, hashlib, os, re, shutil, subprocess, time
from pathlib import Path
from ae1_ae4_restore_bisect import (
    parse, grouped, get_payload, encode_len_field, replace_top_field,
    sha, validate_header, ram_info
)

PIN = "0c3572c3d"
TARGET_SHA = "00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA = "9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
SOURCE_URLS = {
 "sstate.h": "https://github.com/pcsx-redux/pcsx-redux/blob/0c3572c3d/src/core/sstate.h",
 "types.h": "https://github.com/pcsx-redux/pcsx-redux/blob/0c3572c3d/src/spu/types.h",
 "adsr.h": "https://github.com/pcsx-redux/pcsx-redux/blob/0c3572c3d/src/spu/adsr.h",
}
RAM_ADDRS = (0x80070EB8, 0x80070F6C, 0x8013A554)

def encvarint(v):
    out=bytearray()
    while v>0x7f:
        out.append((v & 0x7f)|0x80); v >>= 7
    out.append(v)
    return bytes(out)

def replace_occurrence(payload: bytes, number: int, occurrence: int, new_payload: bytes):
    """Replace one wire-2 occurrence, preserving all sibling bytes and field order."""
    records=parse(payload); out=bytearray(); seen=0; replaced=False
    for r in records:
        if r["num"]==number:
            if seen==occurrence:
                if r["wire"] != 2: raise ValueError("selected field isn't wire-2")
                out.extend(encode_len_field(number,new_payload)); replaced=True
            else:
                out.extend(r["enc"])
            seen += 1
        else:
            out.extend(r["enc"])
    if not replaced:
        raise ValueError("missing field %d occurrence %d" % (number, occurrence+1))
    return bytes(out)

def hybrid_message(base: bytes, source: bytes, selected):
    """Copy only selected (field number, zero-based occurrence) encodings from source.
    Source-only selected fields are inserted before the first higher-numbered field.
    """
    br=parse(base); sr=parse(source); bg=grouped(br); sg=grouped(sr)
    selected=set(selected)
    out=bytearray(); seen={}; inserted=set()
    for r in br:
        n=r["num"]; i=seen.get(n,0); seen[n]=i+1
        if (n,i) in selected:
            if i < len(sg.get(n,[])):
                out.extend(sg[n][i]["enc"])
        else:
            out.extend(r["enc"])
        if i == len(bg.get(n,[]))-1:
            inserted.add(n)
            for extra in range(len(bg[n]),len(sg.get(n,[]))):
                if (n,extra) in selected: out.extend(sg[n][extra]["enc"])
    for n in sorted(set(sg)-set(bg)):
        selected_items=[r for i,r in enumerate(sg[n]) if (n,i) in selected]
        if not selected_items: continue
        anchor=next((i for i,r in enumerate(br) if r["num"]>n),None)
        enc=b"".join(r["enc"] for r in selected_items)
        if anchor is None: out.extend(enc)
        else:
            # Rebuild once for insertion before the first greater field.
            prefix=bytearray(); suffix=bytearray()
            for i,r in enumerate(br):
                (prefix if i<anchor else suffix).extend(r["enc"])
            out=prefix+enc+suffix
    return bytes(out)

def direct_children(state: bytes, top_field: int, child_number: int):
    parent=get_payload(state,top_field)
    return [r["payload"] for r in parse(parent) if r["num"]==child_number and r["wire"]==2]

def classify(logtext, wrapper_rc):
    if re.search(r"(?:received|received signal|Program received|Program terminated with signal) SIGSEGV",logtext):
        return "SIGSEGV"
    if re.search(r"(?:received|received signal|Program received|Program terminated with signal) SIGABRT",logtext):
        return "SIGABRT"
    if "AE_POST_LOAD_VSYNC=180" in logtext and "AE_RAM_STATE_CAPTURE=PASS" in logtext:
        return "POST_LOAD_VSYNC=180"
    if "SIGINT" in logtext or wrapper_rc in (124,137,143,-9,-2):
        return "INCONCLUSIVE_TIMEOUT_OR_INTERRUPTED"
    if "AE_LOAD_LUA_ERROR=" in logtext or "AE_STATE_OPEN_FAIL=" in logtext:
        return "RESTORE_SCRIPT_ERROR"
    return "INCONCLUSIVE"

def excerpt(src: Path, dest: Path):
    lines=src.read_text(errors="replace").splitlines()
    if len(lines)>290:
        body=lines[:40]+["[... middle omitted in excerpt; full log is sibling raw file; source lines=%d ...]"%len(lines)]+lines[-250:]
    else: body=lines
    dest.write_text("\n".join(body)+"\n",encoding="utf-8")

def tsv(values):
    return "\t".join(str(x).replace("\t"," ").replace("\n","\\n") for x in values)+"\n"

def main():
    ap=argparse.ArgumentParser()
    for name in ("target","control","source-header","output","work","pcsx-bin","appdir","bios","cue","card"):
        ap.add_argument("--"+name,required=True)
    a=ap.parse_args()
    target_path,control_path=Path(a.target),Path(a.control)
    work,out=Path(a.work),Path(a.output)
    raw=out/"raw"; excerpts=out/"excerpts"
    for d in (out,raw,excerpts,work/"hybrids",work/"logs",work/"runtime",work/"resume",work/"home/.config",work/"home/.local/share",work/"home/runtime"):
        d.mkdir(parents=True,exist_ok=True)
    target=target_path.read_bytes(); control=control_path.read_bytes()
    if sha(target)!=TARGET_SHA: raise ValueError("target input SHA mismatch")
    if sha(control)!=CONTROL_SHA: raise ValueError("control input SHA mismatch")
    validate_header(Path(a.source_header).read_bytes())

    tspu=get_payload(target,6); cspu=get_payload(control,6)
    tchannels=[x["payload"] for x in parse(tspu) if x["num"]==6 and x["wire"]==2]
    cchannels=[x["payload"] for x in parse(cspu) if x["num"]==6 and x["wire"]==2]
    if len(tchannels)<2 or len(cchannels)<2: raise ValueError("SPU Channel occurrence #2 not present")
    tchannel,cchannel=tchannels[1],cchannels[1]
    child_names={1:"data: Message<ChannelData>",2:"adsr: Message<ADSRInfo>",3:"adsr_ex: Message<ADSRInfoEx>"}
    tchild=grouped(parse(tchannel)); cchild=grouped(parse(cchannel))
    static=[
      "AE1 NESTED CHANNEL[2] AUDIT — pinned PCSX-Redux schema, no input",
      "target_sha256="+sha(target),"control_sha256="+sha(control),
      "source_pin="+PIN,"channel_occurrence=SPU.channel[2]",
      "target_channel2_payload_bytes=%d"%len(tchannel),"control_channel2_payload_bytes=%d"%len(cchannel),
      "target_channel2_sha256="+sha(tchannel),"control_channel2_sha256="+sha(cchannel),
      "schema: "+SOURCE_URLS["sstate.h"],
      "schema: "+SOURCE_URLS["types.h"],
      "schema: "+SOURCE_URLS["adsr.h"],
      "SPU.channel is repeated Message<Channel> field 6; Channel fields: field 1 data/ChannelData, field 2 adsr/ADSRInfo, field 3 adsr_ex/ADSRInfoEx.",
      "channel child fields: field | name/type | target payload/encoded SHA256 | control payload/encoded SHA256 | changed",
    ]
    for n in (1,2,3):
        tr=tchild.get(n,[]); cr=cchild.get(n,[])
        for i in range(max(len(tr),len(cr))):
            t=tr[i] if i<len(tr) else None; c=cr[i] if i<len(cr) else None
            static.append("%d#%d | %s | %s/%s/%s | %s/%s/%s | %s" % (
              n,i+1,child_names[n],
              t["payload_len"] if t else "-",t["encoded_len"] if t else "-",sha(t["enc"]) if t else "-",
              c["payload_len"] if c else "-",c["encoded_len"] if c else "-",sha(c["enc"]) if c else "-",
              "YES" if (t is None or c is None or t["enc"]!=c["enc"]) else "no"))
    (out/"AE1_channel2_nested_static.txt").write_text("\n".join(static)+"\n",encoding="utf-8")

    lua=work/"ae-refine.lua"
    lua.write_text(r'''
if io.stdout then io.stdout:setvbuf("no") end
local vsync, started, loaded, after, pending = 0, false, false, 0, false
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
_G.aeLoaded = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  loaded = true; after = 0; log("AE_REFINE_SAVE_STATE_LOADED=1")
end)
local function save_ram()
  local ok, err = pcall(function()
    local state = PCSX.createSaveState()
    local f = assert(Support.File.open("runtime/current.sstate", "TRUNCATE"), "cannot create temp checkpoint")
    f:writeMoveSlice(state); f:close()
  end)
  if ok then log("AE_RAM_STATE_CAPTURE=PASS")
  else log("AE_RAM_STATE_CAPTURE=FAIL detail="..tostring(err)) end
  PCSX.nextTick(function() PCSX.quit(ok and 0 or 62) end)
end
_G.aeVsync = PCSX.Events.createEventListener("GPU::Vsync", function()
  vsync=vsync+1
  if not started then
    started=true
    local path=os.getenv("AE_TEST_STATE") or "resume/case.sstate"
    log("AE_REFINE_LOAD_BEGIN=1 path="..path.." controller=NONE")
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local open_ok,file=pcall(function() return assert(Support.File.open(path),"state open failed") end)
      if not open_ok or not file then log("AE_STATE_OPEN_FAIL="..tostring(file)); PCSX.quit(50); return end
      local load_ok,err=pcall(function() PCSX.loadSaveState(file) end)
      file:close()
      if not load_ok then log("AE_LOAD_LUA_ERROR="..tostring(err)); PCSX.quit(51); return end
      log("AE_LOAD_CALL_RETURNED=1"); PCSX.resumeEmulator()
    end)
    return
  end
  if loaded then
    after=after+1
    if after>=180 and not pending then
      pending=true; log("AE_POST_LOAD_VSYNC=180")
      PCSX.pauseEmulator(); PCSX.nextTick(save_ram)
    end
  elseif vsync>=900 then
    log("AE_LOAD_EVENT_TIMEOUT=1"); PCSX.pauseEmulator()
    PCSX.nextTick(function() PCSX.quit(53) end)
  end
end)
log("AE_REFINE_PROBE_READY_NO_INPUT=1")
'''.lstrip(),encoding="utf-8")
    pad=work/"pad-setup.lua"
    if not pad.exists():
        pad.write_text("PCSX.settings.pads[1].DeviceType = 'Analog'\nPCSX.settings.pads[1].Connected = true\nPCSX.SIO0.slots[1].pads[1].map()\nprint('AE_NO_INPUT_CONTROLLER=1; no button overrides')\n",encoding="utf-8")

    # Prepare control-base hybrids with exactly one target child of SPU.channel[2].
    cases=[]
    cases.append(("ae2-target-spu-field6-control",replace_top_field(target,control,6),
                  "target state with entire SPU field 6 from control (long timeout; necessity test)"))
    for n,name in [(1,"data"),(2,"adsr"),(3,"adsr_ex")]:
        channel_hybrid=hybrid_message(cchannel,tchannel,{(n,0)})
        hybrid_spu=replace_occurrence(cspu,6,1,channel_hybrid)
        hybrid_state=replace_top_field(control,encode_len_field(6,hybrid_spu),6)
        cases.append(("ae1-channel2-child-"+name,hybrid_state,
          "control base; only target Channel[2]."+name+" message from SPU.channel[2] field 6 occurrence"))
    env=os.environ.copy()
    env.update({
      "DISPLAY":":99","HOME":str(work/"home"),"XDG_CONFIG_HOME":str(work/"home/.config"),
      "XDG_DATA_HOME":str(work/"home/.local/share"),"XDG_RUNTIME_DIR":str(work/"home/runtime"),
      "LIBGL_ALWAYS_SOFTWARE":"1",
      "LD_LIBRARY_PATH":str(Path(a.appdir)/"usr/lib")+":"+str(Path(a.appdir)/"usr/lib/x86_64-linux-gnu"),
      "QT_PLUGIN_PATH":str(Path(a.appdir)/"usr/plugins"),
      "QT_QPA_PLATFORM_PLUGIN_PATH":str(Path(a.appdir)/"usr/plugins/platforms"),
      "QML2_IMPORT_PATH":str(Path(a.appdir)/"usr/qml"),
    })
    try:(work/"home/runtime").chmod(0o700)
    except OSError:pass
    result=[]; summaries=[]; snapshots=[]
    def run_case(name,state,definition):
        state_sha=sha(state); state_file=work/"resume"/(name+".sstate"); state_file.write_bytes(state)
        outs=[]; pcs=[]
        for attempt in (1,2):
            label=f"{name}-attempt{attempt}"
            gdb_log=raw/(label+".gdb.txt"); pcsxlog=work/"logs"/(label+".pcsx.txt")
            rawpcsx=raw/(label+".pcsx.txt"); current=work/"runtime/current.sstate"
            for p in (gdb_log,pcsxlog,rawpcsx,current):
                try:p.unlink()
                except FileNotFoundError:pass
            cmds=work/"ae-refine-gdb.commands"
            cmds.write_text("""set pagination off
set confirm off
set print thread-events off
handle SIGSEGV stop print pass
handle SIGABRT stop print pass
run
python
import gdb
inf = gdb.selected_inferior()
if getattr(inf, 'pid', 0):
    print('AE_GDB_CONTEXT_BEGIN')
    for command in ('info threads', 'x/3i $pc', 'info registers', 'info proc mappings', 'bt', 'thread apply all bt 40'):
        print('AE_GDB_COMMAND_BEGIN: ' + command)
        try: gdb.execute(command)
        except Exception as exc: print('AE_GDB_COMMAND_UNAVAILABLE: ' + command + ' :: ' + str(exc))
        print('AE_GDB_COMMAND_END: ' + command)
    print('AE_GDB_CONTEXT_END')
    try: gdb.execute('continue')
    except Exception as exc: print('AE_GDB_FINAL_CONTINUE_RESULT: ' + str(exc))
else:
    print('AE_GDB_CONTEXT_STATUS=NOT_APPLICABLE; inferior exited before post-run context')
end
""",encoding="utf-8")
            envtest=env.copy(); envtest["AE_TEST_STATE"]="resume/"+state_file.name
            cmd=["timeout","--signal=INT","--kill-after=5s","110s",
              "gdb","--quiet","--nx","--batch","--return-child-result","-x",str(cmds),
              "--args",a.pcsx_bin,
              "-noupdate","-no-debugger","-no-gdb","-bios",a.bios,"-iso",a.cue,
              "-memcard1",a.card,"-exec",pad.read_text(encoding="utf-8"),
              "-dofile",str(lua),"-softgpu","-dynarec","-stdout","-lua_stdout",
              "-logfile",str(pcsxlog),"-run"]
            start=time.time()
            with gdb_log.open("wb") as outlog:
                proc=subprocess.run(cmd,cwd=work,env=envtest,stdout=outlog,stderr=subprocess.STDOUT,check=False)
            rc=proc.returncode
            if not pcsxlog.exists():pcsxlog.write_text("AE_PCSX_LOG_NOT_CREATED; inspect complete GDB log\n",encoding="utf-8")
            shutil.copyfile(pcsxlog,rawpcsx)
            logtext=gdb_log.read_text(errors="replace")
            status=classify(logtext,rc)
            sig=re.search(r"(?:Thread \d+ .* received signal|Program received signal|Program terminated with signal) (SIG[A-Z0-9]+)",logtext)
            signal=sig.group(1) if sig else ("NONE" if status=="POST_LOAD_VSYNC=180" else "TIDAK_TAHU")
            pc_match=re.search(r"(?:=>\s*)?(0x[0-9a-fA-F]+):\s+\w",logtext)
            pc=pc_match.group(1) if pc_match else ("NOT_APPLICABLE_NORMAL_EXIT" if status=="POST_LOAD_VSYNC=180" else "TIDAK_TAHU")
            exitmatch=re.search(r"exited with code (\d+)",logtext)
            if exitmatch: inferior_exit=exitmatch.group(1)
            elif re.search(r"exited normally",logtext): inferior_exit="0"
            elif signal in ("SIGSEGV","SIGABRT"): inferior_exit="TIDAK TAHU (signal observed; numeric inferior exit not separately recorded)"
            elif rc in (124,137,143,-9,-2): inferior_exit="TIDAK TAHU (timeout/kill)"
            else: inferior_exit="TIDAK TAHU"
            ramhash="-"; ramlen=0; wordtext="-"
            if status=="POST_LOAD_VSYNC=180" and current.exists():
                try:
                    ramhash,words,ramlen=ram_info(current.read_bytes())
                    wordtext="; ".join("0x%08X bytes=%s LE32=0x%08X"%(ad,b.hex(" "),v) for ad,b,v in words)
                    snapshots.append([name,attempt,state_sha,ramhash,ramlen,wordtext])
                except Exception as e:wordtext="RAM_PARSE_ERROR="+repr(e)
            try: current.unlink()
            except OSError:pass
            duration="%.3f"%(time.time()-start)
            result.append([name,attempt,state_sha,status,signal,pc,rc,inferior_exit,"YES" if "AE_POST_LOAD_VSYNC=180" in logtext else "no",ramhash,ramlen,wordtext,str(gdb_log.relative_to(out)),str(rawpcsx.relative_to(out)),duration])
            excerpt(gdb_log,excerpts/(gdb_log.name+".first40-last250.txt"))
            excerpt(rawpcsx,excerpts/(rawpcsx.name+".first40-last250.txt"))
            outs.append(status); pcs.append(pc)
            print("AE_REFINE_ATTEMPT_DONE case=%s attempt=%d result=%s signal=%s pc=%s wrapper_rc=%s elapsed=%s"%(name,attempt,status,signal,pc,rc,duration),flush=True)
        if outs==["SIGSEGV","SIGSEGV"]: combined="SIGSEGV_BOTH"
        elif outs==["POST_LOAD_VSYNC=180","POST_LOAD_VSYNC=180"]: combined="POST_LOAD_VSYNC_180_BOTH"
        elif outs[0]==outs[1]: combined=outs[0]+"_BOTH"
        else: combined="MIXED_OR_INCONCLUSIVE"
        summaries.append([name,combined,";".join(outs),";".join(pcs),state_sha,definition])
        print("AE_REFINE_CASE_DONE case=%s outcome=%s sha256=%s"%(name,combined,state_sha),flush=True)
    for name,state,definition in cases:run_case(name,state,definition)

    with (out/"AE1_AE4_refinement_results.tsv").open("w",encoding="utf-8") as f:
        f.write(tsv(["case","attempt","hybrid_state_sha256","result","signal","pc_or_status","gdb_wrapper_exit","observed_inferior_exit","post_load_vsync_180","ram_2mib_sha256","serialized_RAM_bytes_not_dumped","raw_words_at_frame","gdb_log","pcsx_log","seconds"]))
        for row in result:f.write(tsv(row))
    with (out/"AE1_AE4_refinement_cases.tsv").open("w",encoding="utf-8") as f:
        f.write(tsv(["case","two_launch_outcome","attempt_outcomes","PC_or_status_each","hybrid_state_sha256","definition"]))
        for row in summaries:f.write(tsv(row))
    with (out/"AE1_AE4_refinement_RAM.tsv").open("w",encoding="utf-8") as f:
        f.write(tsv(["case","attempt","hybrid_state_sha256","RAM_2MiB_sha256","serialized_RAM_bytes_not_dumped","raw_4_bytes_and_LE32_at_addresses"]))
        for row in snapshots:f.write(tsv(row))
    manifest=[]
    for p in sorted(raw.glob("*")):
        if p.is_file():manifest.append("%s  %s  bytes=%d"%(sha(p.read_bytes()),p.relative_to(out),p.stat().st_size))
    (out/"AE1_AE4_refinement_log_sha256.txt").write_text("\n".join(manifest)+"\n",encoding="utf-8")
    report=[
      "AE1-AE4 LONG-TIMEOUT REFINEMENT SUMMARY",
      "This refinement was added because run 40889442511 used an 18-second per-attempt timeout; non-crashing trials ended by SIGINT/kill before POST_LOAD_VSYNC=180, so those outcomes are INCONCLUSIVE.",
      "Target/control state hashes were validated before constructing hybrids.",
      "Target producer AppImage SHA-256=c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c; current run uses GDB and 110-second per-attempt timeout with no controller input.",
      "Nested target Channel[2] child fields tested one-by-one: field1 data/ChannelData, field2 adsr/ADSRInfo, field3 adsr_ex/ADSRInfoEx.",
      "AE2 reversed whole-field test: target base with control's full SPU field 6. Two independent attempts are recorded.",
      "Post-load RAM (if any) only hashed first 2 MiB and reads requested words; no state or RAM dump is published.",
      "Case summary: AE1_AE4_refinement_cases.tsv; per-attempt raw logs: raw/; 40-start/250-end excerpts: excerpts/; SHA-256 manifest: AE1_AE4_refinement_log_sha256.txt.",
      "AE4 qualifying RAM snapshots from this refinement: %d attempts."%len(snapshots),
    ]
    (out/"AE1_AE4_REFINEMENT.txt").write_text("\n".join(report)+"\n",encoding="utf-8")
    print("\n".join(report),flush=True)

if __name__=="__main__":
    main()
