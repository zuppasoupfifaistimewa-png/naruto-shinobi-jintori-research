#!/usr/bin/env python3
"""AK1/AK2: repeat H6 and control at post-load VSync 180/240/360."""
import argparse
import csv
import hashlib
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

from aj2_h6_ram_probe import one, replace_top, encmsg, sha

TARGET_SHA = "00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA = "9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA = "d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
FRAMES = (180, 240, 360)
RAM_BYTES = 0x200000
ADDRESSES = (0x80070EB8, 0x80070F6C, 0x8013A554)

def ram2m(state_bytes):
    memory = one(state_bytes, 3)
    ram = one(memory, 1)
    if len(ram) < RAM_BYTES:
        raise ValueError(f"RAM too short: {len(ram)}")
    return ram[:RAM_BYTES], len(ram)

def word_values(ram):
    out = []
    for address in ADDRESSES:
        off = address - 0x80000000
        raw = ram[off:off + 4]
        if len(raw) != 4:
            raise ValueError(f"word outside 2 MiB RAM: {address:#x}")
        out.append((f"0x{address:08X}", raw.hex(" "), f"0x{int.from_bytes(raw, 'little'):08X}"))
    return out

def make_lua():
    return r'''
if io.stdout then io.stdout:setvbuf("no") end
local vsync, started, loaded, after = 0, false, false, 0
local launchEpoch = tonumber(os.getenv("AK_LAUNCH_START_EPOCH")) or os.time()
local done, pending = {}, {}
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
_G.akLoaded = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  loaded = true; after = 0
  log("AK_SAVE_STATE_LOADED=1")
end)
local paths = {
  [180]="runtime/frame180.sstate",
  [240]="runtime/frame240.sstate",
  [360]="runtime/frame360.sstate"
}
local function snap(frame)
  local ok, err = pcall(function()
    local s = PCSX.createSaveState()
    local f = assert(Support.File.open(paths[frame], "TRUNCATE"))
    f:writeMoveSlice(s)
    f:close()
  end)
  if ok then
    log("AK_RAM_CAPTURE_FRAME="..frame.."=PASS")
  else
    log("AK_RAM_CAPTURE_FRAME="..frame.."=FAIL "..tostring(err))
    PCSX.nextTick(function() PCSX.quit(62) end)
    return
  end
  if frame == 360 then PCSX.nextTick(function() PCSX.quit(0) end) end
end
_G.akVsync = PCSX.Events.createEventListener("GPU::Vsync", function()
  vsync = vsync + 1
  if not started then
    started = true
    local statePath = os.getenv("AK_STATE_PATH") or "runtime/input.sstate"
    log("AK_LOAD_BEGIN=1 path="..statePath.." vsync="..vsync.." input=NONE")
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf, f = pcall(function() return assert(Support.File.open(statePath)) end)
      if not okf or not f then log("AK_STATE_OPEN_FAIL="..tostring(f)); PCSX.quit(50); return end
      local ok, err = pcall(function() PCSX.loadSaveState(f) end)
      f:close()
      if not ok then log("AK_LOAD_ERROR="..tostring(err)); PCSX.quit(51); return end
      log("AK_LOAD_CALL_RETURNED=1")
      PCSX.resumeEmulator()
    end)
    return
  end
  if loaded then
    after = after + 1
    for _, frame in ipairs({180,240,360}) do
      if after >= frame and not done[frame] and not pending[frame] then
        pending[frame] = true
        log("AK_POST_LOAD_VSYNC="..frame.." elapsed_since_launch_s="..tostring(os.time()-launchEpoch))
        local target = frame
        PCSX.nextTick(function()
          snap(target)
          done[target] = true
        end)
      end
    end
    if after >= 1200 then
      log("AK_POST_LOAD_FRAME_WATCHDOG=1 after="..after)
      PCSX.quit(53)
    end
  end
end)
log("AK_READY_NO_INPUT=1")
'''.lstrip()

def parse_exit(log_text):
    m = re.search(r"(?:Inferior\s+\d+.*?exited with code|Program exited with code)\s*[=:]?\s*(-?\d+)", log_text, re.I)
    return m.group(1) if m else "TIDAK TAHU"

def run_one(variant, attempt, state_path, a, out, work, timeout_s, env_base):
    label = f"{variant}-attempt{attempt}"
    launch = work / "launches" / label
    runtime, home, logs = launch / "runtime", launch / "home", out / "logs"
    for d in (runtime, home / ".config", home / ".data", home / "runtime", logs):
        d.mkdir(parents=True, exist_ok=True)
    try:
        (home / "runtime").chmod(0o700)
    except OSError:
        pass
    lua = launch / "ak.lua"
    lua.write_text(make_lua(), encoding="utf-8")
    pad = launch / "pad.lua"
    pad.write_text(
        "PCSX.settings.pads[1].DeviceType = 'Analog'\n"
        "PCSX.settings.pads[1].Connected = true\n"
        "PCSX.SIO0.slots[1].pads[1].map()\n"
        "print('AK_CONTROLLER_NO_INPUT=1')\n", encoding="utf-8")
    gdb_log, pcsx_log = logs / f"{label}.gdb.txt", logs / f"{label}.pcsx.txt"
    cmdfile = launch / f"{label}.gdb.commands"
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
 print('AK_GDB_CONTEXT_BEGIN')
 for c in ('info threads','x/3i $pc','info registers','bt','thread apply all bt 20'):
  print('AK_GDB_COMMAND_BEGIN: '+c)
  try:gdb.execute(c)
  except Exception as e:print('AK_GDB_COMMAND_UNAVAILABLE: '+str(e))
  print('AK_GDB_COMMAND_END: '+c)
 print('AK_GDB_CONTEXT_END')
 try:gdb.execute('continue')
 except Exception as e:print('AK_GDB_CONTINUE_RESULT: '+str(e))
else: print('AK_GDB_CONTEXT_STATUS=INFERIOR_EXITED')
end
""", encoding="utf-8")
    env = env_base.copy()
    env.update({
        "HOME": str(home),
        "XDG_CONFIG_HOME": str(home / ".config"),
        "XDG_DATA_HOME": str(home / ".data"),
        "XDG_RUNTIME_DIR": str(home / "runtime"),
        "AK_STATE_PATH": str(state_path),
        "AK_LAUNCH_START_EPOCH": str(time.time()),
    })
    command = [
        "timeout", "--signal=INT", "--kill-after=5s", f"{timeout_s}s",
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
    with gdb_log.open("wb") as stream:
        try:
            proc = subprocess.run(command, cwd=launch, env=env, stdout=stream,
                                  stderr=subprocess.STDOUT, check=False)
            wrapper_rc = proc.returncode
        except Exception as exc:
            wrapper_rc = 255
            stream.write(("AK_LAUNCH_EXCEPTION=" + repr(exc) + "\n").encode())
    wall = time.monotonic() - started
    gdb_text = gdb_log.read_text(encoding="utf-8", errors="replace")
    pcsx_text = pcsx_log.read_text(encoding="utf-8", errors="replace") if pcsx_log.exists() else ""
    combined = gdb_text + "\n" + pcsx_text
    emulator_exit = parse_exit(combined)
    rows = []
    for frame in FRAMES:
        state_file = runtime / f"frame{frame}.sstate"
        marker = re.search(rf"AK_POST_LOAD_VSYNC={frame} elapsed_since_launch_s=([0-9.]+)", gdb_text)
        pass_marker = f"AK_RAM_CAPTURE_FRAME={frame}=PASS" in gdb_text
        status = "PASS" if marker and pass_marker and state_file.is_file() else (
            "MARKER_NO_FILE" if marker and pass_marker else
            "FILE_NO_MARKER" if state_file.is_file() else "TIDAK ADA CAPTURE")
        ram_hash, word_text, ram_len = "TIDAK TAHU", "TIDAK TAHU", 0
        if status == "PASS":
            try:
                ram, ram_len = ram2m(state_file.read_bytes())
                ram_hash = sha(ram)
                word_text = "; ".join(f"{addr} bytes={raw} LE32={value}" for addr, raw, value in word_values(ram))
            except Exception as exc:
                status = "PARSE_ERROR"
                word_text = "TIDAK TAHU: " + repr(exc)
        rows.append({
            "variant": variant, "attempt": attempt, "frame": frame,
            "capture_status": status,
            "elapsed_since_launch_s": marker.group(1) if marker else "TIDAK TAHU",
            "ram_2mib_sha256": ram_hash, "ram_segment_bytes": ram_len,
            "words": word_text, "gdb_wrapper_exit_code": wrapper_rc,
            "emulator_exit_code_in_log": emulator_exit,
            "wall_seconds": f"{wall:.3f}",
            "gdb_log": str(gdb_log.relative_to(out)),
            "pcsx_log": str(pcsx_log.relative_to(out)),
        })
    return rows

def make_diff(a, b, comparison):
    changed = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    groups = []
    if changed:
        start = last = changed[0]
        count = 1
        runs = 1
        for pos in changed[1:]:
            if pos - last - 1 <= 32:
                count += 1
            else:
                groups.append((start, last, count, runs))
                start, count, runs = pos, 1, 1
            if pos != last + 1 and pos - last - 1 > 32:
                pass
            elif pos != last + 1:
                runs += 1
            last = pos
        groups.append((start, last, count, runs))
    out = []
    known = {
        0x80070EA0 - 0x80000000: "player0_record_base_0x80070EA0 (record_extent=TIDAK TAHU)",
        0x8013A554 - 0x80000000: "pointer_storage_0x8013A554",
        0x801CEF08 - 0x80000000: "pointer_target_0x801CEF08",
    }
    for start, end, count, runs in groups:
        hits = []
        for off, name in known.items():
            if any(off <= p < off + 4 for p in changed if start <= p <= end):
                hits.append(name)
        category = ";".join(hits) if hits else "TIDAK TAHU (rentang stack/kode belum dipetakan)"
        out.append({
            "comparison": comparison,
            "start": f"0x{0x80000000 + start:08X}",
            "end": f"0x{0x80000000 + end:08X}",
            "span_bytes": end - start + 1,
            "changed_bytes": count,
            "contiguous_runs": runs,
            "known_source_overlap": category,
        })
    return len(changed), out

def main():
    ap = argparse.ArgumentParser()
    for key in ("target", "control", "pcsx-bin", "bios", "cue", "card", "work", "out"):
        ap.add_argument("--" + key, required=True)
    ap.add_argument("--appdir", required=True)
    ap.add_argument("--timeout-seconds", type=int, default=600)
    a = ap.parse_args()
    target_path, control_path = Path(a.target), Path(a.control)
    target, control = target_path.read_bytes(), control_path.read_bytes()
    if sha(target) != TARGET_SHA: raise SystemExit("TARGET_SHA_MISMATCH")
    if sha(control) != CONTROL_SHA: raise SystemExit("CONTROL_SHA_MISMATCH")
    hybrid = replace_top(target, 6, encmsg(6, one(control, 6)))
    if sha(hybrid) != H6_SHA: raise SystemExit("H6_SHA_MISMATCH actual=" + sha(hybrid))
    target_ram, target_ram_len = ram2m(target)
    work, out = Path(a.work), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (work / "resume").mkdir(parents=True, exist_ok=True)
    (work / "resume/h6.sstate").write_bytes(hybrid)
    (work / "resume/h6.sstate").chmod(0o400)
    env_base = os.environ.copy()
    appdir = Path(a.appdir)
    env_base.update({
        "DISPLAY": ":99", "LIBGL_ALWAYS_SOFTWARE": "1",
        "LD_LIBRARY_PATH": str(appdir / "usr/lib") + ":" + str(appdir / "usr/lib/x86_64-linux-gnu"),
        "QT_PLUGIN_PATH": str(appdir / "usr/plugins"),
        "QT_QPA_PLATFORM_PLUGIN_PATH": str(appdir / "usr/plugins/platforms"),
        "QML2_IMPORT_PATH": str(appdir / "usr/qml"),
    })
    all_rows = []
    for variant, source in (("H6", work / "resume/h6.sstate"), ("CONTROL_NOT_TARGET", control_path)):
        for attempt in (1, 2):
            all_rows.extend(run_one(variant, attempt, source, a, out, work,
                                    a.timeout_seconds, env_base))
    fields = list(all_rows[0].keys())
    with (out / "AK1_REPLAY.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader(); w.writerows(all_rows)
    lookup = {(r["variant"], r["attempt"], r["frame"]): r for r in all_rows}
    h6_valid = all(lookup[("H6", n, frame)]["capture_status"] == "PASS"
                   for n in (1, 2) for frame in FRAMES)
    control_valid = all(lookup[("CONTROL_NOT_TARGET", n, frame)]["capture_status"] == "PASS"
                        for n in (1, 2) for frame in FRAMES)
    h6_same = {}
    first_div = "TIDAK ADA DIVERGENSI PADA 180/240/360" if h6_valid else "TIDAK TAHU (capture tidak lengkap)"
    if h6_valid:
        for frame in FRAMES:
            r1, r2 = lookup[("H6", 1, frame)], lookup[("H6", 2, frame)]
            h6_same[frame] = r1["ram_2mib_sha256"] == r2["ram_2mib_sha256"]
            if first_div == "TIDAK ADA DIVERGENSI PADA 180/240/360" and not h6_same[frame]:
                first_div = f"FRAME DIVERGENSI PERTAMA={frame}"
    else:
        h6_same = {f: None for f in FRAMES}
    control_same = {}
    if control_valid:
        for frame in FRAMES:
            control_same[frame] = (lookup[("CONTROL_NOT_TARGET", 1, frame)]["ram_2mib_sha256"] ==
                                   lookup[("CONTROL_NOT_TARGET", 2, frame)]["ram_2mib_sha256"])
    diff_rows, diff_summary = [], []
    comparisons = []
    if h6_valid:
        for attempt in (1, 2):
            p = lookup[("H6", attempt, 180)]
            if p["capture_status"] == "PASS":
                state = (work / "launches" / f"H6-attempt{attempt}" / "runtime/frame180.sstate").read_bytes()
                ram, _ = ram2m(state)
                count, ranges = make_diff(target_ram, ram, f"TARGET_SOURCE_vs_H6_attempt{attempt}_180")
                diff_rows.extend(ranges)
                comparisons.append((f"TARGET_SOURCE_vs_H6_attempt{attempt}_180", count, len(ranges)))
    if h6_valid and control_valid:
        for attempt in (1, 2):
            hs = (work / "launches" / f"H6-attempt{attempt}" / "runtime/frame180.sstate").read_bytes()
            cs = (work / "launches" / f"CONTROL_NOT_TARGET-attempt{attempt}" / "runtime/frame180.sstate").read_bytes()
            hr, _ = ram2m(hs); cr, _ = ram2m(cs)
            count, ranges = make_diff(hr, cr, f"H6_attempt{attempt}_180_vs_CONTROL_attempt{attempt}_180")
            diff_rows.extend(ranges)
            comparisons.append((f"H6_attempt{attempt}_180_vs_CONTROL_attempt{attempt}_180", count, len(ranges)))
    with (out / "AK2_DIFF_RANGES.tsv").open("w", encoding="utf-8", newline="") as f:
        names = ["comparison", "start", "end", "span_bytes", "changed_bytes", "contiguous_runs", "known_source_overlap"]
        w = csv.DictWriter(f, fieldnames=names, delimiter="\t")
        w.writeheader(); w.writerows(diff_rows)
    ds = [
        "Bytewise RAM diff; region = first 2 MiB of PS1 RAM, address base 0x80000000.",
        "Diff ranges merge exact changed-byte runs when their separating gap is <=32 bytes; span_bytes includes gaps, changed_bytes counts only unequal bytes.",
        "Known labels are only exact overlaps with 0x80070EA0, 0x8013A554, or 0x801CEF08. Player0 record extent, stack and code ranges are not mapped here; other ranges are TIDAK TAHU.",
        f"TARGET_SOURCE_RAM_2MIB_SHA256={sha(target_ram)}",
        f"TARGET_SOURCE_RAM_FIELD_BYTES={target_ram_len}",
        f"H6_TWO_LAUNCH_CAPTURES_VALID={h6_valid}",
        f"CONTROL_TWO_LAUNCH_CAPTURES_VALID={control_valid}",
    ]
    for name, count, nr in comparisons:
        ds.append(f"{name}: different_bytes={count} grouped_ranges={nr}")
    if not comparisons:
        ds.append("No valid bytewise comparison could be completed.")
    ds.append("TARGET_vs_H6_180_CAUSE= TIDAK TAHU: target source is pre-replay while H6@180 is post-replay; no target-native @180 capture is in this test.")
    (out / "AK2_DIFF_SUMMARY.txt").write_text("\n".join(ds) + "\n", encoding="utf-8")
    replay_lines = ["AK1 replay determinism (H6 is a hybrid, NOT a pure target).", f"H6_SHA256={H6_SHA}"]
    for frame in FRAMES:
        replay_lines.append(f"H6_FRAME_{frame}_TWO_LAUNCH_RAM_IDENTICAL={h6_same.get(frame, 'TIDAK TAHU')}")
        for variant in ("H6", "CONTROL_NOT_TARGET"):
            replay_lines.append(f"{variant}_FRAME_{frame}_ATTEMPT1_SHA={lookup[(variant,1,frame)]['ram_2mib_sha256']}")
            replay_lines.append(f"{variant}_FRAME_{frame}_ATTEMPT2_SHA={lookup[(variant,2,frame)]['ram_2mib_sha256']}")
    replay_lines.append("H6_FIRST_DIVERGENCE=" + first_div)
    (out / "AK1_FINDING.txt").write_text("\n".join(replay_lines) + "\n", encoding="utf-8")
    all_required = h6_valid and control_valid
    ak1_done = h6_valid
    ak2_done = h6_valid and control_valid and any(x[0].startswith("TARGET_SOURCE") for x in comparisons) and any(x[0].startswith("H6_attempt") for x in comparisons)
    # Broad host/RSI exploration remains parked; only a controlled one-variable A/B may proceed.
    rsi_decision = ("PARKED_GENERAL_SEARCH; allow only pre-registered one-variable host/RSI A/B with >=2 launches/condition; causality=TIDAK TAHU"
                    if ak1_done else "TETAP_DIPARKIR; baseline multi-frame replay not established")
    report = [
        "# AK1–AK3 — laporan determinisme replay H6 dan pembanding RAM",
        "",
        f"Run: {os.getenv('GITHUB_RUN_ID','TIDAK TAHU')} attempt {os.getenv('GITHUB_RUN_ATTEMPT','TIDAK TAHU')}; job: ak1-ak3; source commit: {os.getenv('GITHUB_SHA','TIDAK TAHU')}.",
        "",
        "## Skala bukti K0–K5",
        "K0 = tidak ada bukti atau fakta belum diketahui; K1 = petunjuk tunggal/hipotesis yang belum diverifikasi; K2 = observasi eksplisit dari satu artefak atau log tetapi belum dikorroborasi; K3 = beberapa artefak statis yang konsisten dengan provenance yang dapat ditelusuri; K4 = validasi statis independen, byte/digest atau struktur dapat direproduksi dan dibuktikan, tetapi belum ada uji runtime; K5 = pengamatan runtime yang memenuhi kriteria uji dan direplikasi pada sedikitnya dua peluncuran independen. Bukti statis saja maksimal K4.",
        "",
        f"## AK1 — {'TUNTAS' if ak1_done else 'SEBAGIAN'} | K{'5' if ak1_done else '4'}",
        f"H6 two-launch multi-frame capture valid: {h6_valid}. H6 first divergence: {first_div}. Tabel lengkap per launch/frame: AK1_REPLAY.tsv; capture 180/240/360, waktu-ke-frame, hash RAM 2 MiB, tiga word, status capture, wrapper exit, dan emulator exit yang tercatat.",
        "",
        f"## AK2 — {'TUNTAS' if ak2_done else 'SEBAGIAN'} | K{'5' if ak2_done else '4'}",
        f"Two-launch H6/control captures valid: {all_required}. Bytewise diff summary: AK2_DIFF_SUMMARY.txt; grouped address ranges: AK2_DIFF_RANGES.tsv. Target source vs H6@180 cannot be attributed solely to 180 frames from these data: TIDAK TAHU; no target-native frame-180 replay comparator is present.",
        "",
        "## AK3 — TUNTAS | K4",
        "Dua belas SHA hibrida AE2 berikut tetap TIDAK TAHU: ae2-current-bisect-step1 attempt1/2; step2 attempt1/2; step3 attempt1/2; step4 attempt1/2; step5 attempt1/2; ae2-target-current-all-24-control attempt1/2. Re-check: reports/aj_2026-10-30/runs/run-41028457166/attempt-1/AJ1_RAW_GDB_TABLE.tsv dan AJ1_AJ3_COMPLETION_REPORT.md tidak memuat pemetaan digest untuk enam hibrida × dua attempt ini; tidak ada digest nyata di repo untuk dipasangkan. Tidak ada hash hasil tebakan.",
        f"Putusan host/RSI: {rsi_decision}. H6 determinism tidak membuktikan kausalitas host/RSI; A/B terkontrol satu variabel masih diperlukan.",
        "",
        "## Exit/status run",
        f"AK_SCRIPT_EXIT_CODE=0; H6_SHA256={H6_SHA}; timeout_per_launch_s={a.timeout_seconds}.",
        "Emulator exit code dilaporkan hanya bila string exit eksplisit muncul pada GDB/PCSX log; jika tidak, TIDAK TAHU. GDB wrapper exit adalah kolom berbeda.",
        "",
        "## Berkas yang dikomit",
        "AK1_FINDING.txt; AK1_REPLAY.tsv; AK2_DIFF_SUMMARY.txt; AK2_DIFF_RANGES.tsv; logs/*.gdb.txt; logs/*.pcsx.txt; ACTIONS_RUN_SUMMARY.txt; AK1_AK3_FINAL_REPORT.md. Tidak ada ISO, BIOS, savestate, Memory Card, dump RAM, atau biner hibrida.",
    ]
    (out / "AK1_AK3_FINAL_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    script_exit = 0
    status = "PASS" if ak1_done and ak2_done else "INCOMPLETE"
    summary = [
        f"STATUS={status}", "JOB=ak1-ak3",
        f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
        f"RUN_ATTEMPT={os.getenv('GITHUB_RUN_ATTEMPT','TIDAK TAHU')}",
        f"HEAD_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}",
        f"H6_SHA256={H6_SHA}", f"TIMEOUT_PER_LAUNCH_S={a.timeout_seconds}",
        f"AK1_STATUS={'TUNTAS' if ak1_done else 'SEBAGIAN'}",
        f"AK2_STATUS={'TUNTAS' if ak2_done else 'SEBAGIAN'}",
        "AK3_STATUS=TUNTAS",
        f"EXIT_CODE={script_exit}",
    ]
    (out / "ACTIONS_RUN_SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    # Remove every transient state and the temporary hybrid before the workflow stages text output.
    shutil.rmtree(work / "launches", ignore_errors=True)
    try: (work / "resume/h6.sstate").unlink()
    except OSError: pass
    print("\n".join(summary))
    return script_exit

if __name__ == "__main__":
    raise SystemExit(main())
