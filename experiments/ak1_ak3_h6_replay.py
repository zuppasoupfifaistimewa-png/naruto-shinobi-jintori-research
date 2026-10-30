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

from aj2_h6_ram_probe import one, replace_top, encmsg, sha, fields

TARGET_SHA = "00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA = "9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA = "d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
FRAMES = (1, 60, 180, 240, 360)
RAM_BYTES = 0x200000
PLAYER_BASE = 0x80070EA0
PLAYER_STRIDE = 0xB4
ADDRESSES = tuple([PLAYER_BASE + n * PLAYER_STRIDE + 0x18 for n in range(4)] +
                  [0x8013A554, 0x801CEF08, 0x800A3118, 0x80066E7C])

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
  [1]="runtime/frame1.sstate",
  [60]="runtime/frame60.sstate",
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
  if frame == 360 then
    log("AK_QUIT0_CALL_BEGIN=1 frame=360 dispatch=direct")
    local qok, qerr = pcall(function() PCSX.quit(0) end)
    log("AK_QUIT0_CALL_RETURNED=1 ok="..tostring(qok).." detail="..tostring(qerr))
  end
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
    for _, frame in ipairs({1,60,180,240,360}) do
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
    # GDB prints the inferior's POSIX exit status in octal.
    m = re.search(r"Inferior\s+\d+.*?exited with code\s+([0-7]+)", log_text, re.I)
    if m:
        return str(int(m.group(1), 8)), "GDB inferior exit status (octal converted to decimal)"
    m = re.search(r"Program exited with code\s+([0-7]+)", log_text, re.I)
    if m:
        return str(int(m.group(1), 8)), "GDB program exit status (octal converted to decimal)"
    return "TIDAK TAHU", "no explicit GDB/PCSX exit status"

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
    emulator_exit, emulator_exit_source = parse_exit(combined)
    watchdog_seen = "AK_POST_LOAD_FRAME_WATCHDOG=1" in combined
    quit0_call_seen = "AK_QUIT0_CALL_BEGIN=1 frame=360" in combined
    quit0_return_seen = "AK_QUIT0_CALL_RETURNED=1" in combined
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
            "emulator_exit_code_decimal": emulator_exit,
            "emulator_exit_code_source": emulator_exit_source,
            "watchdog_seen": str(watchdog_seen).upper(),
            "quit0_call_marker_seen": str(quit0_call_seen).upper(),
            "quit0_return_marker_seen": str(quit0_return_seen).upper(),
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


def diff_positions(a, b):
    if len(a) != len(b):
        raise ValueError("RAM byte lengths differ")
    return {i for i, (x, y) in enumerate(zip(a, b)) if x != y}


def write_al3(out, work, target_ram):
    rows, summaries = [], []
    for attempt in (1, 2):
        snapshots = {}
        for frame in (1, 60, 180):
            p = work / "launches" / f"H6-attempt{attempt}" / "runtime" / f"frame{frame}.sstate"
            if not p.is_file():
                raise ValueError(f"AL3 missing H6 attempt{attempt} frame{frame}")
            snapshots[frame], _ = ram2m(p.read_bytes())
        d1 = diff_positions(target_ram, snapshots[1])
        d60 = diff_positions(target_ram, snapshots[60])
        d180 = diff_positions(target_ram, snapshots[180])
        present = len(d1 & d180)
        later = len(d180 - d1)
        reverted = len(d1 - d180)
        rows.append({
            "attempt": attempt,
            "target_vs_h6_frame1_changed_bytes": len(d1),
            "target_vs_h6_frame60_changed_bytes": len(d60),
            "target_vs_h6_frame180_changed_bytes": len(d180),
            "frame180_differences_already_present_at_frame1": present,
            "frame180_differences_first_appearing_after_frame1": later,
            "frame1_differences_reverted_by_frame180": reverted,
            "new_differences_between_frame1_and_frame60": len(d60 - d1),
            "new_differences_between_frame60_and_frame180": len(d180 - d60),
            "differences_reverted_between_frame1_and_frame60": len(d1 - d60),
            "differences_reverted_between_frame60_and_frame180": len(d60 - d180),
        })
        summaries.append(
            f"H6 attempt{attempt}: D1={len(d1)} D60={len(d60)} D180={len(d180)}; "
            f"@180 already present at @1={present}; first appearing after @1={later}; "
            f"@1 differences reverted by @180={reverted}."
        )
    with (out / "AL3_BYTE_DECOMPOSITION.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    consistent = (
        rows[0]["frame180_differences_already_present_at_frame1"] == rows[1]["frame180_differences_already_present_at_frame1"]
        and rows[0]["frame180_differences_first_appearing_after_frame1"] == rows[1]["frame180_differences_first_appearing_after_frame1"]
        and rows[0]["target_vs_h6_frame180_changed_bytes"] == rows[1]["target_vs_h6_frame180_changed_bytes"]
    )
    return summaries, consistent


def write_al2(out):
    source = Path("reports/ak_2026-10-30/runs/run-41032514102/attempt-1/AK2_DIFF_RANGES.tsv")
    if not source.is_file():
        raise FileNotFoundError(f"AL2 source TSV missing: {source}")
    with source.open("r", encoding="utf-8", newline="") as f:
        ranges = list(csv.DictReader(f, delimiter="\t"))
    labels = []
    for n in range(4):
        base = PLAYER_BASE + n * PLAYER_STRIDE
        labels.append({
            "label": f"P{n}_candidate_ID_slots", "start": base + 0x0A, "end": base + 0x0C,
            "K": "K4",
            "source": "ANALYSIS_LOG.md:2352,2358,2373; docs/STEP4_8_ID_COLLECTION_CONSUMER_TRACE_2026-10-28.md:37,108",
            "notes": "Tiga byte ID; fitur/gameplay yang memilikinya tetap UNKNOWN."
        })
        labels.append({
            "label": f"P{n}_Chakra", "start": base + 0x18, "end": base + 0x1B,
            "K": "K4",
            "source": "ANALYSIS_LOG.md:1327,1398; STATUS.md:3246; setter/getter 0x8001387C/0x800138EC",
            "notes": "Word Chakra pada offset +0x18; tidak menyimpulkan aturan gameplay dari diff."
        })
    labels.extend([
        {"label":"slot_0x8013A554_address_only","start":0x8013A554,"end":0x8013A557,"K":"K3",
         "source":"ANALYSIS_LOG.md:5-9,29,99,143; STATUS.md:6-9,97,133",
         "notes":"Slot XREF; nilai, alias runtime dan arti pointer belum terpecahkan."},
        {"label":"block_start_0x801CEF08_address_only","start":0x801CEF08,"end":0x801CEF0B,"K":"K2",
         "source":"AK2_DIFF_RANGES.tsv known_source_overlap=pointer_target_0x801CEF08",
         "notes":"Hanya alamat awal yang dikenali; extent/isi blok TIDAK TAHU."},
        {"label":"RNG_state_0x800A3118","start":0x800A3118,"end":0x800A311B,"K":"K4",
         "source":"STATUS.md:276-277; ANALYSIS_LOG.md:56; RNG routine 0x80035D78",
         "notes":"State word LCG terverifikasi statis; seed/runtime callers lain tetap UNKNOWN."},
        {"label":"callback_tick_counter_0x80066E7C","start":0x80066E7C,"end":0x80066E7F,"K":"K4/K5",
         "source":"ANALYSIS_LOG.md:2278-2310; STATUS.md:205-206",
         "notes":"K4 untuk pola statis reset/increment callback-like; K5 hanya untuk diff runtime berulang pada dua H6 launches."},
    ])
    comparisons = sorted({r["comparison"] for r in ranges})
    output, summaries = [], {}
    for comparison in comparisons:
        subset = [r for r in ranges if r["comparison"] == comparison]
        totals = {x["label"]: 0 for x in labels}
        unknown = 0
        partial_block = None
        for r in subset:
            start, end = int(r["start"], 16), int(r["end"], 16)
            changed = int(r["changed_bytes"])
            hits = [x for x in labels if start <= x["end"] and x["start"] <= end]
            if len(hits) == 1 and start >= hits[0]["start"] and end <= hits[0]["end"]:
                totals[hits[0]["label"]] += changed
            else:
                unknown += changed
                if ("pointer_target_0x801CEF08" in r.get("known_source_overlap", "")
                    and start <= 0x801CEF0B and end >= 0x801CEF08):
                    partial_block = {
                        "lower": 1, "upper": changed, "group_changed": changed,
                        "start": r["start"], "end": r["end"], "span": int(r["span_bytes"])
                    }
        totals["TIDAK_TAHU"] = unknown
        total = sum(int(r["changed_bytes"]) for r in subset)
        if sum(totals.values()) != total:
            raise ValueError("AL2 byte accounting mismatch")
        summaries[comparison] = {"totals":totals,"total":total,"partial_block":partial_block}
        for item in labels:
            is_block = item["label"] == "block_start_0x801CEF08_address_only" and partial_block
            output.append({
                "comparison":comparison,"label":item["label"],
                "exact_changed_bytes":totals[item["label"]],
                "partial_lower_bound":str(partial_block["lower"] if is_block else 0),
                "partial_upper_bound":str(partial_block["upper"] if is_block else 0),
                "evidence_K":item["K"],"source":item["source"],"notes":item["notes"]
            })
        output.append({
            "comparison":comparison,"label":"TIDAK_TAHU",
            "exact_changed_bytes":unknown,"partial_lower_bound":"0","partial_upper_bound":"0",
            "evidence_K":"K0","source":"AK2_DIFF_RANGES.tsv",
            "notes":"Semua rentang yang tidak sepenuhnya berada di satu label dikenal tetap TIDAK TAHU."
        })
    with (out / "AL2_FIELD_RELABEL.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(output[0]), delimiter="\t")
        w.writeheader()
        w.writerows(output)
    notes = [
        "AL2 uses only the committed AK2_DIFF_RANGES.tsv; no emulator was launched for this relabelling.",
        "A grouped range is allocated only when its entire inclusive span fits exactly one mapped field. Groups crossing a label boundary remain TIDAK_TAHU.",
        "Ranges merge exact changed runs separated by gaps <=32 bytes. changed_bytes is exact per group, not per address, so a mixed group cannot be split accurately.",
        "Player records: four records at 0x80070EA0 + n*0xB4. Known fields: candidate ID bytes +0x0A..+0x0C, Chakra word +0x18..+0x1B. Other record bytes remain TIDAK TAHU.",
        "0x8013A554 is address/slot only; pointer semantics unresolved. 0x801CEF08 is only an address start; block extent/meaning unresolved.",
    ]
    for cmp, info in summaries.items():
        totals = info["totals"]
        exact = sum(v for k, v in totals.items() if k != "TIDAK_TAHU")
        notes.append(f"{cmp}: exact_known={exact}; TIDAK_TAHU={totals['TIDAK_TAHU']}; total={info['total']}.")
        p = info["partial_block"]
        if p:
            notes.append(f"  0x801CEF08 overlap bound={p['lower']}..{p['upper']} bytes; grouped range {p['start']}..{p['end']} (span={p['span']}, changed={p['group_changed']}); exact count TIDAK TAHU and stays inside TIDAK_TAHU total.")
    (out / "AL2_RELABEL_NOTES.txt").write_text("\n".join(notes) + "\n", encoding="utf-8")
    return notes, summaries


def selective_occurrence(base, source, selected):
    br, sr = fields(base), fields(source)
    bg, sg = {}, {}
    for item in br:
        bg.setdefault(item["n"], []).append(item)
    for item in sr:
        sg.setdefault(item["n"], []).append(item)
    selected = set(selected)
    out, seen = bytearray(), {}
    for item in br:
        n = item["n"]
        i = seen.get(n, 0)
        seen[n] = i + 1
        if (n, i) in selected:
            if i < len(sg.get(n, [])):
                out.extend(sg[n][i]["enc"])
        else:
            out.extend(item["enc"])
        if i == len(bg[n]) - 1:
            for extra in range(len(bg[n]), len(sg.get(n, []))):
                if (n, extra) in selected:
                    out.extend(sg[n][extra]["enc"])
    for n in sorted(set(sg) - set(bg)):
        for i, item in enumerate(sg[n]):
            if (n, i) in selected:
                out.extend(item["enc"])
    return bytes(out)


def replace_channel_in_state(state, channel_number, new_channel):
    spu = one(state, 6)
    out, seen = bytearray(), 0
    for item in fields(spu):
        if item["n"] == 6 and item["w"] == 2:
            out.extend(encmsg(6, new_channel) if seen == channel_number else item["enc"])
            seen += 1
        else:
            out.extend(item["enc"])
    if seen <= channel_number:
        raise ValueError(f"SPU channel {channel_number} missing")
    return replace_top(state, 6, encmsg(6, bytes(out)))


def current_hybrid(target, control, keep_target_current):
    target_spu, control_spu = one(target, 6), one(control, 6)
    target_channels = [x for x in fields(target_spu) if x["n"] == 6 and x["w"] == 2]
    control_channels = [x for x in fields(control_spu) if x["n"] == 6 and x["w"] == 2]
    if len(target_channels) != 24 or len(control_channels) != 24:
        raise ValueError(f"expected 24 SPU channels; target={len(target_channels)} control={len(control_channels)}")
    state = target
    for i in range(24):
        if i in keep_target_current:
            continue
        tdata = one(target_channels[i]["pay"], 1)
        cdata = one(control_channels[i]["pay"], 1)
        new_data = selective_occurrence(tdata, cdata, {(8, 0)})
        new_channel = replace_top(target_channels[i]["pay"], 1, encmsg(1, new_data))
        state = replace_channel_in_state(state, i, new_channel)
    return state


def historical_two_launch_outcome(case, repo_root):
    statuses = []
    for attempt in (1, 2):
        p = repo_root / "reports/ae_2026-10-29/deep/raw" / f"{case}-attempt{attempt}.gdb.txt"
        if not p.is_file():
            statuses.append("TIDAK TAHU")
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if re.search(r"received signal SIGSEGV", text):
            statuses.append("SIGSEGV")
        elif "AE_POST_LOAD_VSYNC=180" in text and "AE_RAM_STATE_CAPTURE=PASS" in text:
            statuses.append("POST_LOAD_VSYNC_180")
        else:
            statuses.append("TIDAK TAHU")
    if statuses == ["SIGSEGV", "SIGSEGV"]:
        return "SIGSEGV_BOTH"
    if statuses == ["POST_LOAD_VSYNC_180", "POST_LOAD_VSYNC_180"]:
        return "POST_LOAD_VSYNC_180_BOTH"
    return "MIXED_OR_TIDAK_TAHU:" + ";".join(statuses)


def write_al4(out, target, control):
    repo_root = Path(__file__).resolve().parents[1]
    all_outcome = historical_two_launch_outcome("ae2-target-current-all-24-control", repo_root)
    rows = []
    state = current_hybrid(target, control, set())
    rows.append({
        "case":"ae2-target-current-all-24-control",
        "definition_status":"REKONSTRUKSI" if all_outcome == "POST_LOAD_VSYNC_180_BOTH" else "REKONSTRUKSI_HASH; historical gate TIDAK TAHU",
        "target_current_channels_1based":"",
        "control_current_channels_1based":",".join(str(i+1) for i in range(24)),
        "historical_two_launch_outcome":all_outcome,
        "target_source_sha256":sha(target),"control_source_sha256":sha(control),
        "reconstructed_hybrid_sha256":sha(state),
        "notes":"Target base; copy only ChannelData.current (SPU field6 -> Channel field6 -> data field1 -> field8 occurrence1) from control across all 24 channels."
    })
    candidates = list(range(24))
    proceed = all_outcome == "POST_LOAD_VSYNC_180_BOTH"
    for step in range(1, 6):
        case = f"ae2-current-bisect-step{step}"
        if not proceed or len(candidates) <= 1:
            rows.append({
                "case":case,"definition_status":"TIDAK TAHU",
                "target_current_channels_1based":"","control_current_channels_1based":"",
                "historical_two_launch_outcome":"NOT_REACHED_BY_VERIFIED_GATE",
                "target_source_sha256":sha(target),"control_source_sha256":sha(control),
                "reconstructed_hybrid_sha256":"TIDAK TAHU",
                "notes":"Tidak dibuat hash karena keputusan bisection sebelumnya tidak tervalidasi."
            })
            continue
        mid = len(candidates) // 2
        left = candidates[:mid]
        outcome = historical_two_launch_outcome(case, repo_root)
        hybrid = current_hybrid(target, control, set(left))
        if outcome == "SIGSEGV_BOTH":
            chosen = left
        elif outcome == "POST_LOAD_VSYNC_180_BOTH":
            chosen = candidates[mid:]
        else:
            chosen = None
        rows.append({
            "case":case,"definition_status":"REKONSTRUKSI" if chosen is not None else "TIDAK TAHU",
            "target_current_channels_1based":",".join(str(i+1) for i in left),
            "control_current_channels_1based":",".join(str(i+1) for i in range(24) if i not in set(left)),
            "historical_two_launch_outcome":outcome,
            "target_source_sha256":sha(target),"control_source_sha256":sha(control),
            "reconstructed_hybrid_sha256":sha(hybrid),
            "notes":"Tested object is current_hybrid(left); SIGSEGV_BOTH keeps left, POST_LOAD_VSYNC_180_BOTH selects right."
        })
        if chosen is None:
            proceed = False
        else:
            candidates = chosen
    with (out / "AL4_HYBRID_RECONSTRUCTIONS.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    return rows

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
