#!/usr/bin/env python3
"""AJ2 H6: two independent PCSX-Redux headless restores; only text evidence is emitted."""
import argparse
import hashlib
import os
import re
import subprocess
import time
import math
from pathlib import Path

TARGET_SHA = "00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA = "9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_EXPECTED_SHA = "d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
ADDRESSES = (0x80070EB8, 0x80070F6C, 0x8013A554)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def vi(b, p):
    value = shift = 0
    while p < len(b) and shift <= 70:
        c = b[p]
        p += 1
        value |= (c & 127) << shift
        if not c & 128:
            return value, p
        shift += 7
    raise ValueError("malformed protobuf varint")

def encvi(n):
    out = bytearray()
    while n > 127:
        out.append((n & 127) | 128)
        n >>= 7
    out.append(n)
    return bytes(out)

def parse(b):
    out = []
    p = 0
    while p < len(b):
        start = p
        tag, p = vi(b, p)
        number, wire = tag >> 3, tag & 7
        if number == 0:
            raise ValueError("protobuf field zero")
        if wire == 0:
            _, p = vi(b, p)
            end = p
        elif wire == 1:
            p += 8
            end = p
        elif wire == 2:
            length, p = vi(b, p)
            p += length
            end = p
        elif wire == 5:
            p += 4
            end = p
        else:
            raise ValueError("unsupported protobuf wire type")
        if p > len(b):
            raise ValueError("truncated protobuf field")
        out.append((number, wire, start, end, b[start:end], b[start:end] if wire != 2 else b[p-(end-(p-length if wire==2 else p)):p]))
    return out

def fields(b):
    out = []
    p = 0
    while p < len(b):
        start = p
        tag, p = vi(b, p)
        n, w = tag >> 3, tag & 7
        if not n:
            raise ValueError("field zero")
        if w == 0:
            _, p = vi(b, p)
            payload = b[start:p]
        elif w == 1:
            p += 8
            payload = b[start:p]
        elif w == 2:
            ln, p = vi(b, p)
            payload_start = p
            p += ln
            payload = b[start:p]
            if p > len(b):
                raise ValueError("truncated field")
            out.append({"n": n, "w": w, "enc": payload, "pay": b[payload_start:p]})
            continue
        elif w == 5:
            p += 4
            payload = b[start:p]
        else:
            raise ValueError("unsupported wire type")
        if p > len(b):
            raise ValueError("truncated field")
        out.append({"n": n, "w": w, "enc": payload, "pay": None})
    return out

def one(b, number):
    matches = [x for x in fields(b) if x["n"] == number and x["w"] == 2]
    if len(matches) != 1:
        raise ValueError(f"expected one field {number}, found {len(matches)}")
    return matches[0]["pay"]

def encmsg(number, payload):
    return encvi((number << 3) | 2) + encvi(len(payload)) + payload

def replace_top(b, number, replacement):
    out = bytearray()
    inserted = False
    for item in fields(b):
        if item["n"] == number:
            if not inserted:
                out.extend(replacement)
                inserted = True
        else:
            out.extend(item["enc"])
    if not inserted:
        out.extend(replacement)
    return bytes(out)

def ram_info(state):
    memory = one(state, 3)
    ram = one(memory, 1)
    first_2m = ram[:0x200000]
    if len(first_2m) != 0x200000:
        raise ValueError(f"RAM segment too short: {len(first_2m)}")
    word_rows = []
    for address in ADDRESSES:
        offset = address - 0x80000000
        raw = first_2m[offset:offset+4]
        if len(raw) != 4:
            raise ValueError(f"address {address:08X} outside RAM")
        value = int.from_bytes(raw, "little")
        word_rows.append((f"0x{address:08X}", raw.hex(" "), f"0x{value:08X}"))
    return sha(first_2m), len(ram), word_rows

def write_lua(path):
    path.write_text(r'''
if io.stdout then io.stdout:setvbuf("no") end
local vsync, started, loaded, after, pending = 0, false, false, 0, false
local launchEpoch = tonumber(os.getenv("AE_RUN_START_EPOCH")) or os.time()
local loadEpoch = 0
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
_G.ajH6Loaded = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  loaded=true; after=0; loadEpoch=os.time()
  log("AJ_H6_SAVE_STATE_LOADED=1 epoch="..tostring(loadEpoch))
end)
local function snap()
  local ok, err = pcall(function()
    local s=PCSX.createSaveState()
    local f=assert(Support.File.open("runtime/h6-current.sstate","TRUNCATE"))
    f:writeMoveSlice(s); f:close()
  end)
  log(ok and "AJ_H6_RAM_CAPTURE=PASS" or ("AJ_H6_RAM_CAPTURE=FAIL "..tostring(err)))
  PCSX.nextTick(function() PCSX.quit(ok and 0 or 62) end)
end
_G.ajH6Vsync = PCSX.Events.createEventListener("GPU::Vsync", function()
  vsync=vsync+1
  if not started then
    started=true
    local statePath=os.getenv("AJ_H6_STATE") or "runtime/h6.sstate"
    log("AJ_H6_LOAD_BEGIN=1 path="..statePath.." vsync="..vsync.." input=NONE")
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf, f=pcall(function() return assert(Support.File.open(statePath)) end)
      if not okf or not f then log("AJ_H6_STATE_OPEN_FAIL="..tostring(f)); PCSX.quit(50); return end
      local ok, err=pcall(function() PCSX.loadSaveState(f) end); f:close()
      if not ok then log("AJ_H6_LOAD_ERROR="..tostring(err)); PCSX.quit(51); return end
      log("AJ_H6_LOAD_CALL_RETURNED=1"); PCSX.resumeEmulator()
    end)
    return
  end
  if loaded then
    after=after+1
    if after>=180 and not pending then
      pending=true
      log("AJ_H6_POST_LOAD_VSYNC=180 elapsed_since_launch_s="..tostring(os.time()-launchEpoch).." elapsed_since_loaded_s="..tostring(os.time()-loadEpoch))
      PCSX.nextTick(snap)
    end
  elseif vsync>=900 then
    log("AJ_H6_LOAD_EVENT_TIMEOUT=1"); PCSX.pauseEmulator()
    PCSX.nextTick(function() PCSX.quit(53) end)
  end
end)
log("AJ_H6_READY_NO_INPUT=1")
'''.lstrip(), encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    for name in ("target", "control", "pcsx-bin", "appdir", "bios", "cue", "card", "work", "out"):
        ap.add_argument("--" + name, required=True)
    a = ap.parse_args()
    target_path, control_path = Path(a.target), Path(a.control)
    target, control = target_path.read_bytes(), control_path.read_bytes()
    if sha(target) != TARGET_SHA:
        raise SystemExit("TARGET_SHA_MISMATCH")
    if sha(control) != CONTROL_SHA:
        raise SystemExit("CONTROL_SHA_MISMATCH")
    target_spu, control_spu = one(target, 6), one(control, 6)
    hybrid = replace_top(target, 6, encmsg(6, control_spu))
    hybrid_sha = sha(hybrid)
    if not re.fullmatch(r"[0-9a-f]{64}", hybrid_sha) or hybrid_sha != H6_EXPECTED_SHA:
        raise SystemExit("H6_COMMITTED_REFERENCE_SHA_MISMATCH actual=" + hybrid_sha)
    work, out = Path(a.work), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    resume = work / "resume"
    runtime = work / "runtime"
    logs = work / "logs"
    home = work / "home"
    for d in (resume, runtime, logs, home / ".config", home / ".local/share", home / "runtime"):
        d.mkdir(parents=True, exist_ok=True)
    try:
        (home / "runtime").chmod(0o700)
    except OSError:
        pass
    hybrid_path = resume / "h6.sstate"
    hybrid_path.write_bytes(hybrid)  # Temporary /tmp only; never copied to repo.
    target_ram_sha, target_ram_len, target_words = ram_info(target)
    lua = work / "h6.lua"
    write_lua(lua)
    pad = work / "pad.lua"
    pad.write_text(
        "PCSX.settings.pads[1].DeviceType = 'Analog'\n"
        "PCSX.settings.pads[1].Connected = true\n"
        "PCSX.SIO0.slots[1].pads[1].map()\n"
        "print('AJ_H6_CONTROLLER_NO_INPUT=1')\n",
        encoding="utf-8",
    )
    appdir = Path(a.appdir)
    env = os.environ.copy()
    env.update({
        "DISPLAY": ":99",
        "HOME": str(home),
        "XDG_CONFIG_HOME": str(home / ".config"),
        "XDG_DATA_HOME": str(home / ".local/share"),
        "XDG_RUNTIME_DIR": str(home / "runtime"),
        "LIBGL_ALWAYS_SOFTWARE": "1",
        "LD_LIBRARY_PATH": str(appdir / "usr/lib") + ":" + str(appdir / "usr/lib/x86_64-linux-gnu"),
        "QT_PLUGIN_PATH": str(appdir / "usr/plugins"),
        "QT_QPA_PLATFORM_PLUGIN_PATH": str(appdir / "usr/plugins/platforms"),
        "QML2_IMPORT_PATH": str(appdir / "usr/qml"),
    })
    historical = []
    old_raw = Path("reports/ae_2026-10-29/deep/raw")
    for p in old_raw.glob("ae2-target-spu-field6-control-attempt*.gdb.txt"):
        txt = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"AE_POST_LOAD_VSYNC=180\s+elapsed_since_loaded_s=[0-9.]+\s+elapsed_since_launch_s=([0-9.]+)", txt)
        if m:
            historical.append(float(m.group(1)))
    historical_slowest = max(historical) if historical else 62.745
    timeout_seconds = max(180, math.ceil(2 * historical_slowest + 30))
    if timeout_seconds < 2 * historical_slowest + 30:
        raise SystemExit("TIMEOUT_BOUND_CHECK_FAILED")
    target_words_map = {x[0]: x[1:] for x in target_words}
    rows = []
    for attempt in (1, 2):
        label = f"H6-attempt{attempt}"
        gdb_log = logs / f"{label}.gdb.txt"
        pcsx_log = logs / f"{label}.pcsx.txt"
        current_state = runtime / "h6-current.sstate"
        try:
            current_state.unlink()
        except FileNotFoundError:
            pass
        cmdfile = work / f"{label}.gdb.commands"
        cmdfile.write_text("""set pagination off
set confirm off
set print thread-events off
handle SIGSEGV stop print nopass
handle SIGABRT stop print nopass
run
python
import gdb
inf=gdb.selected_inferior()
if getattr(inf,'pid',0):
 print('AJ_H6_GDB_CONTEXT_BEGIN')
 for c in ('info threads','x/3i $pc','info registers','bt','thread apply all bt 20'):
  print('AJ_H6_GDB_COMMAND_BEGIN: '+c)
  try:gdb.execute(c)
  except Exception as e:print('AJ_H6_GDB_COMMAND_UNAVAILABLE: '+str(e))
  print('AJ_H6_GDB_COMMAND_END: '+c)
 print('AJ_H6_GDB_CONTEXT_END')
 try:gdb.execute('continue')
 except Exception as e:print('AJ_H6_GDB_CONTINUE_RESULT: '+str(e))
else: print('AJ_H6_GDB_CONTEXT_STATUS=INFERIOR_EXITED')
end
""", encoding="utf-8")
        run_env = env.copy()
        run_env["AJ_H6_STATE"] = str(hybrid_path)
        run_env["AE_RUN_START_EPOCH"] = str(time.time())
        command = [
            "timeout", "--signal=INT", "--kill-after=5s", f"{timeout_seconds}s",
            "gdb", "--quiet", "--nx", "--batch", "--return-child-result",
            "-x", str(cmdfile), "--args", a.pcsx_bin,
            "-noupdate", "-no-debugger", "-no-gdb",
            "-bios", a.bios, "-iso", a.cue, "-memcard1", a.card,
            "-exec", pad.read_text(encoding="utf-8"),
            "-dofile", str(lua),
            "-softgpu", "-dynarec", "-stdout", "-lua_stdout",
            "-logfile", str(pcsx_log), "-run",
        ]
        started = time.monotonic()
        with gdb_log.open("wb") as f:
            try:
                p = subprocess.run(command, cwd=work, env=run_env, stdout=f, stderr=subprocess.STDOUT, check=False)
                wrapper_rc = p.returncode
            except Exception as exc:
                wrapper_rc = 255
                f.write(("AJ_H6_LAUNCH_EXCEPTION=" + repr(exc) + "\n").encode())
        elapsed_wall = time.monotonic() - started
        txt = gdb_log.read_text(encoding="utf-8", errors="replace")
        marker = re.search(r"AJ_H6_POST_LOAD_VSYNC=180 elapsed_since_launch_s=([0-9.]+)", txt)
        captured = "AJ_H6_RAM_CAPTURE=PASS" in txt and current_state.exists()
        segv = bool(re.search(r"received signal SIGSEGV|Program received signal SIGSEGV|Program terminated with signal SIGSEGV", txt))
        try:
            ram_sha, ram_len, words = ram_info(current_state.read_bytes()) if captured else ("TIDAK TAHU", 0, [])
            ram_status = "PASS" if captured else ("CAPTURE_MARKER_ONLY" if "AJ_H6_RAM_CAPTURE=PASS" in txt else "TIDAK ADA CAPTURE")
            word_text = "; ".join(f"{a} bytes={b} LE32={v}" for a, b, v in words) if words else "TIDAK TAHU"
            parse_error = ""
        except Exception as exc:
            ram_sha, ram_len, word_text, ram_status = "TIDAK TAHU", 0, "TIDAK TAHU", "PARSE_ERROR"
            parse_error = repr(exc)
        em = re.search(r"(?:Inferior\s+\d+.*?exited with code|Program exited with code)\s*[=:]?\s*(-?\d+)", txt, re.I)
        outcome = "SIGSEGV" if segv else ("POST_LOAD_VSYNC=180 + AE_RAM_STATE_CAPTURE" if marker and captured and ram_status == "PASS" else ("MARKER_180_NO_RAM" if marker else "TIDAK ADA MARKER 180"))
        rows.append({
            "attempt": attempt,
            "outcome": outcome,
            "hybrid_sha256": hybrid_sha,
            "post_load_elapsed_since_launch_s": marker.group(1) if marker else "TIDAK TAHU",
            "gdb_wrapper_exit_code": wrapper_rc,
            "emulator_exit_code_in_log": em.group(1) if em else "TIDAK TAHU",
            "ram_2mib_sha256": ram_sha,
            "ram_segment_bytes": ram_len,
            "ram_capture": ram_status,
            "raw_words": word_text,
            "wall_seconds": f"{elapsed_wall:.3f}",
            "parse_error": parse_error,
            "gdb_log": str(gdb_log),
            "pcsx_log": str(pcsx_log),
        })
        try:
            current_state.unlink()
        except OSError:
            pass
    import csv
    with (out / "H6_TWO_LAUNCH_RAM.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    good = [r for r in rows if r["outcome"] == "POST_LOAD_VSYNC=180 + AE_RAM_STATE_CAPTURE"]
    compare = []
    compare.append("H6 HYBRID (BUKAN TARGET MURNI)")
    compare.append(f"hybrid_sha256={hybrid_sha}")
    compare.append(f"target_source_sha256={TARGET_SHA} bytes={len(target)}")
    compare.append(f"control_source_sha256={CONTROL_SHA} bytes={len(control)}")
    compare.append(f"hybrid_bytes={len(hybrid)} expected_committed_reference_sha256={H6_EXPECTED_SHA}")
    compare.append(f"timeout_per_launch_s={timeout_seconds} historical_slowest_to_180_s={historical_slowest:.3f} required_minimum_s={2*historical_slowest+30:.3f}")
    compare.append(f"target_ram_2mib_sha256={target_ram_sha} target_ram_field_bytes={target_ram_len}")
    for address, raw, value in target_words:
        compare.append(f"target_{address} bytes={raw} LE32={value}")
    for r in rows:
        compare.append("")
        compare.append(f"ATTEMPT {r['attempt']} outcome={r['outcome']} elapsed={r['post_load_elapsed_since_launch_s']} wrapper_exit={r['gdb_wrapper_exit_code']} emulator_exit={r['emulator_exit_code_in_log']}")
        compare.append(f"RAM_2MiB_SHA256={r['ram_2mib_sha256']} capture={r['ram_capture']} segment_bytes={r['ram_segment_bytes']}")
        compare.append("raw_words=" + r["raw_words"])
        if r["parse_error"]:
            compare.append("RAM_PARSE_ERROR=" + r["parse_error"])
        if r["outcome"] == "POST_LOAD_VSYNC=180 + AE_RAM_STATE_CAPTURE":
            compare.append(f"RAM_match_target={'YES' if r['ram_2mib_sha256']==target_ram_sha else 'NO'}")
    if len(good) == 2:
        compare.append("")
        compare.append(f"two_launch_RAM_identical={'YES' if good[0]['ram_2mib_sha256']==good[1]['ram_2mib_sha256'] else 'NO'}")
        compare.append(f"two_launch_words_identical={'YES' if good[0]['raw_words']==good[1]['raw_words'] else 'NO'}")
    else:
        compare.append("")
        compare.append("two_launch_RAM_identical=TIDAK TAHU (tidak dua capture valid)")
    (out / "H6_RUNTIME_EVIDENCE.txt").write_text("\n".join(compare) + "\n", encoding="utf-8")
    status = "PASS" if len(good) == 2 else "INCOMPLETE"
    summary = [
        f"STATUS={status}",
        "JOB=h6",
        f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
        f"RUN_ATTEMPT={os.getenv('GITHUB_RUN_ATTEMPT','TIDAK TAHU')}",
        f"HEAD_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",
        f"H6_SHA256={hybrid_sha}",
        f"TIMEOUT_PER_LAUNCH_S={timeout_seconds}",
    ]
    for r in rows:
        summary.append(f"ATTEMPT_{r['attempt']}_STATUS={r['outcome']} EXIT_CODE={r['gdb_wrapper_exit_code']}")
    (out / "ACTIONS_RUN_SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(compare))
    print("\n".join(summary))
    # The workflow publishes diagnostic evidence even if a runtime attempt is inconclusive.
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
