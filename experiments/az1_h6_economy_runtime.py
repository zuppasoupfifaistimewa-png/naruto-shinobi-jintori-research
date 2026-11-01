#!/usr/bin/env python3
"""AZ1: read-only H6-hybrid RAM sampling at frames 180 and 360, two launches.

The only binary snapshots are temporary under the runner work directory and are
deleted before publication. No gameplay buttons or RAM writes are issued.
"""
import argparse
import csv
import hashlib
import os
import re
import shutil
import subprocess
import time
from collections import defaultdict
from pathlib import Path

from aj2_h6_ram_probe import one, replace_top, encmsg

TARGET_SHA = "00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d"
CONTROL_SHA = "9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492"
H6_SHA = "d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475"
RAM_BASE = 0x80000000
RAM_BYTES = 0x200000
RECORD_ARRAY_SLOT = 0x8013EA84
RECORD_COUNT_SLOT = 0x8013EAC8
RECORD_STRIDE = 0x124
HISTORICAL_SLOWEST_LAUNCH_S = 145.815
MIN_TIMEOUT_S = 600
MULTIPLIERS = {0: (1, 1), 1: (12, 10), 2: (15, 10), 3: (18, 10), 4: (2, 1)}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def ram2m(state_bytes):
    memory = one(state_bytes, 3)
    ram = one(memory, 1)
    if len(ram) < RAM_BYTES:
        raise ValueError("RAM segment shorter than 2 MiB: " + str(len(ram)))
    return ram[:RAM_BYTES]

def read_u8(ram, address):
    off = address - RAM_BASE
    if off < 0 or off >= len(ram):
        raise ValueError("u8 address outside RAM: 0x%08X" % address)
    return ram[off]

def read_u16(ram, address):
    off = address - RAM_BASE
    if off < 0 or off + 2 > len(ram):
        raise ValueError("u16 address outside RAM: 0x%08X" % address)
    return int.from_bytes(ram[off:off+2], "little")

def read_u32(ram, address):
    off = address - RAM_BASE
    if off < 0 or off + 4 > len(ram):
        raise ValueError("u32 address outside RAM: 0x%08X" % address)
    return int.from_bytes(ram[off:off+4], "little")

def fmt32(value):
    return "0x%08X" % value

def helper_value(selected_b, selector):
    ratio = MULTIPLIERS.get(selector)
    if ratio is None:
        return None
    return (selected_b * ratio[0]) // ratio[1]

def read_snapshot(state_path, attempt, frame, fields, tiles, aggregates, table_rows):
    state_bytes = state_path.read_bytes()
    ram = ram2m(state_bytes)
    ram_sha = sha(ram)

    fields_row = {
        "attempt": attempt, "frame": frame, "ram_first_2mib_sha256": ram_sha,
        "global_0x80070C88_u32": str(read_u32(ram, 0x80070C88)),
        "global_0x80070C88_hex": fmt32(read_u32(ram, 0x80070C88)),
    }
    manager = read_u32(ram, 0x8013A554)
    fields_row["manager_slot_0x8013A554"] = fmt32(manager)
    fields_row["manager_pointer_valid"] = "YES" if RAM_BASE <= manager <= RAM_BASE + len(ram) - 0xB50 else "NO"
    manager_values = {}
    if fields_row["manager_pointer_valid"] == "YES":
        fields_row["manager_B2A_u8"] = str(read_u8(ram, manager + 0xB2A))
        fields_row["manager_B2B_u8"] = str(read_u8(ram, manager + 0xB2B))
        for off in (0xB30, 0xB38, 0xB40, 0xB44):
            value = read_u32(ram, manager + off)
            manager_values[off] = value
            fields_row["manager_%03X_u32" % off] = str(value)
            fields_row["manager_%03X_hex" % off] = fmt32(value)
    else:
        for off in (0xB2A, 0xB2B, 0xB30, 0xB38, 0xB40, 0xB44):
            fields_row["manager_%03X_u32" % off] = "TIDAK TAHU"
            fields_row["manager_%03X_hex" % off] = "TIDAK TAHU"
    fields.append(fields_row)

    mode = read_u32(ram, 0x80070734)
    state = read_u8(ram, 0x8007073C)
    matrix_base = 0x80058758
    table_base = 0x80057798
    row_stride = 0x54
    matrix_stride_mode = 0x84
    matrix_stride_state = 0x0C
    table_row = {
        "attempt": attempt, "frame": frame,
        "mode_0x80070734_u32": mode,
        "state_0x8007073C_u8": state,
        "state_read_method": "lbu 0x8007073C (static PC 0x80012EE8)",
        "matrix_base": fmt32(matrix_base),
        "matrix_stride_mode": fmt32(matrix_stride_mode),
        "matrix_stride_state": fmt32(matrix_stride_state),
        "matrix_index_address": "TIDAK TAHU",
        "matrix_index_byte": "TIDAK TAHU",
        "selected_table_index": "TIDAK TAHU",
        "selected_row_base": "TIDAK TAHU",
        "selected_B30_address": "TIDAK TAHU",
        "selected_B30_u32": "TIDAK TAHU",
        "selected_B30_hex": "TIDAK TAHU",
        "selected_row_gate_plus_2E": "TIDAK TAHU",
        "selected_B30_source_expression": "TIDAK TAHU",
        "manager_B30_u32": fields_row.get("manager_B30_u32", "TIDAK TAHU"),
        "matches_manager_B30": "TIDAK TAHU",
        "selection_status": "MODE_OR_STATE_OUT_OF_RANGE",
    }
    if mode < 256 and state < 11:
        index_address = matrix_base + mode * matrix_stride_mode + state * matrix_stride_state
        index = read_u8(ram, index_address)
        selected_row_base = table_base + index * row_stride
        selected_b30_address = selected_row_base + 0x0C
        selected_b30 = read_u32(ram, selected_b30_address)
        gate = read_u8(ram, selected_row_base + 0x2E)
        table_row.update({
            "matrix_index_address": fmt32(index_address),
            "matrix_index_byte": "0x%02X" % index,
            "selected_table_index": str(index),
            "selected_row_base": fmt32(selected_row_base),
            "selected_B30_address": fmt32(selected_b30_address),
            "selected_B30_u32": str(selected_b30),
            "selected_B30_hex": fmt32(selected_b30),
            "selected_row_gate_plus_2E": str(gate),
            "selected_B30_source_expression": (
                "FUN_80012EAC: idx=u8[0x80058758+mode*0x84+state*0x0C]; "
                "B30=u32[0x80057798+idx*0x54+0x0C]"
            ),
            "matches_manager_B30": (
                "YES" if fields_row.get("manager_B30_u32") == str(selected_b30) else "NO"
            ) if fields_row.get("manager_B30_u32") != "TIDAK TAHU" else "TIDAK TAHU",
            "selection_status": "PASS_STATIC_XREF_AND_RUNTIME_INDEX",
        })
    table_rows.append(table_row)

    pointer = read_u32(ram, RECORD_ARRAY_SLOT)
    count = read_u32(ram, RECORD_COUNT_SLOT)
    header = {
        "attempt": attempt, "frame": frame, "ram_first_2mib_sha256": ram_sha,
        "tile_array_pointer_slot": "0x8013EA84", "tile_array_pointer": fmt32(pointer),
        "tile_count_slot": "0x8013EAC8", "tile_count": str(count),
        "record_stride": "0x124",
    }
    if count > 512 or pointer < RAM_BASE or pointer + count * RECORD_STRIDE > RAM_BASE + len(ram):
        header["validation"] = "POINTER_OR_COUNT_OUTSIDE_2MIB_OR_IMPLAUSIBLE"
        aggregates.append(header)
        return ram_sha, fields_row, table_row, header
    header["validation"] = "PASS"
    header["record_count_checked"] = str(count)
    aggregates.append(header)

    owner_acc = defaultdict(lambda: {"all_sum": 0, "all_count": 0, "status5_sum": 0, "status5_count": 0, "unknown": 0})
    all_sum = 0
    all_count = 0
    all_unknown = 0
    for index in range(count):
        address = pointer + index * RECORD_STRIDE
        status = read_u8(ram, address + 0x00)
        selector = read_u8(ram, address + 0x0B)
        hw20 = read_u16(ram, address + 0x20)
        owner = hw20 >> 12
        selected_off = (hw20 >> 7) & 0x1E
        selected_addr = address + 0x10 + selected_off
        selected_b = read_u16(ram, selected_addr)
        value = helper_value(selected_b, selector)
        tile = {
            "attempt": attempt, "frame": frame, "record_index": index,
            "record_address": fmt32(address), "status_plus_00_u8": status,
            "selector_plus_0B_u8": selector, "owner_hw_plus_20": hw20,
            "owner_hw_plus_20_hex": "0x%04X" % hw20, "owner_hw_shift_12": owner,
            "selected_B_offset": "+0x%02X" % (0x10 + selected_off),
            "selected_B_u16": selected_b, "FUN_800B770C_recomputed_V": value if value is not None else "TIDAK TAHU",
            "validation": "PASS" if value is not None else "UNRECOGNIZED_SELECTOR",
        }
        tiles.append(tile)
        acc = owner_acc[owner]
        if value is None:
            acc["unknown"] += 1
            all_unknown += 1
        else:
            acc["all_sum"] += value
            acc["all_count"] += 1
            all_sum += value
            all_count += 1
            if status == 5:
                acc["status5_sum"] += value
                acc["status5_count"] += 1

    manager_b38 = manager_values.get(0xB38)
    active_id = fields_row.get("manager_B2B_u8", "TIDAK TAHU")
    aggregate_specs = [("ALL", "ALL", all_sum, all_count, all_unknown),
                       ("ALL", "STATUS_5", sum(x["status5_sum"] for x in owner_acc.values()),
                        sum(x["status5_count"] for x in owner_acc.values()), all_unknown)]
    for owner, sums in sorted(owner_acc.items()):
        aggregate_specs.append((str(owner), "ALL", sums["all_sum"], sums["all_count"], sums["unknown"]))
        aggregate_specs.append((str(owner), "STATUS_5", sums["status5_sum"], sums["status5_count"], sums["unknown"]))
    for owner, scope, total, n, unknown in aggregate_specs:
        aggregates.append({
            "attempt": attempt, "frame": frame, "aggregate_owner": owner,
            "status_scope": scope, "record_count_with_known_V": n,
            "unknown_V_count": unknown, "sum_V": total, "floor_sum_V_div_2": total // 2,
            "manager_B38": manager_b38 if manager_b38 is not None else "TIDAK TAHU",
            "matches_B38": ("YES" if manager_b38 == total // 2 else "NO") if manager_b38 is not None and unknown == 0 else "TIDAK TAHU",
            "manager_B2B_active_index": active_id,
        })
    return ram_sha, fields_row, table_row, header

def make_lua():
    return r'''
if io.stdout then io.stdout:setvbuf("no") end
local started, loaded, post, pending180, pending360 = false, false, 0, false, false
local launchEpoch = tonumber(os.getenv("AZ1_LAUNCH_START_EPOCH")) or os.time()
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
local function capture(frame, quitAfter)
  local ok, err = pcall(function()
    local state = PCSX.createSaveState()
    local path = "runtime/frame"..tostring(frame)..".sstate"
    local file = assert(Support.File.open(path, "TRUNCATE"))
    file:writeMoveSlice(state)
    file:close()
  end)
  log(ok and ("AZ1_FRAME"..tostring(frame).."_CAPTURE=PASS") or
      ("AZ1_FRAME"..tostring(frame).."_CAPTURE=FAIL "..tostring(err)))
  if quitAfter then PCSX.quit(ok and 0 or 62) end
end
_G.az1LoadedListener = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  loaded = true
  post = 0
  log("AZ1_SAVE_STATE_LOADED=1")
end)
_G.az1VsyncListener = PCSX.Events.createEventListener("GPU::Vsync", function()
  if not started then
    started = true
    local path = os.getenv("AZ1_H6_STATE") or "resume/h6-hybrid.sstate"
    log("AZ1_LOAD_BEGIN=1 path="..path.." input=NONE")
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local okf, file = pcall(function() return assert(Support.File.open(path)) end)
      if not okf or not file then log("AZ1_STATE_OPEN_FAIL="..tostring(file)); PCSX.quit(50); return end
      local ok, err = pcall(function() PCSX.loadSaveState(file) end)
      file:close()
      if not ok then log("AZ1_STATE_LOAD_FAIL="..tostring(err)); PCSX.quit(51); return end
      log("AZ1_LOAD_CALL_RETURNED=1")
      PCSX.resumeEmulator()
    end)
    return
  end
  if loaded then
    post = post + 1
    if post == 180 and not pending180 then
      pending180 = true
      log("AZ1_POST_LOAD_FRAME=180 elapsed_since_launch_s="..tostring(os.time()-launchEpoch).." input=NONE")
      PCSX.nextTick(function() capture(180, false) end)
    end
    if post >= 360 and not pending360 then
      pending360 = true
      log("AZ1_POST_LOAD_FRAME=360 elapsed_since_launch_s="..tostring(os.time()-launchEpoch).." input=NONE")
      PCSX.nextTick(function() capture(360, true) end)
    end
  end
end)
log("AZ1_READY_NO_GAMEPLAY_INPUT=1")
'''.lstrip()

def parse_exit(wrapper_rc, log_text):
    if wrapper_rc in (124, 137, 143):
        return "TIDAK TAHU", "timeout_wrapper_exit_%d" % wrapper_rc
    if "AZ1_FRAME360_CAPTURE=PASS" in log_text and wrapper_rc == 0:
        return "0", "direct_emulator_exit_after_PCXS_quit_0"
    return str(wrapper_rc), "timeout_wrapper_or_emulator_exit_decimal"

def main():
    ap = argparse.ArgumentParser()
    for name in ("target", "control", "pcsx-bin", "appdir", "bios", "cue", "card", "work", "out"):
        ap.add_argument("--" + name, required=True)
    ap.add_argument("--timeout-seconds", type=int, default=900)
    a = ap.parse_args()
    target = Path(a.target).read_bytes()
    control = Path(a.control).read_bytes()
    if sha(target) != TARGET_SHA:
        raise SystemExit("TARGET_SAVESTATE_SHA_MISMATCH")
    if sha(control) != CONTROL_SHA:
        raise SystemExit("CONTROL_SAVESTATE_SHA_MISMATCH")
    h6 = replace_top(target, 6, encmsg(6, one(control, 6)))
    h6_sha = sha(h6)
    if h6_sha != H6_SHA:
        raise SystemExit("H6_HYBRID_SHA_MISMATCH actual=" + h6_sha)

    timeout_s = int(a.timeout_seconds)
    required = 2 * HISTORICAL_SLOWEST_LAUNCH_S
    timeout_ok = timeout_s >= max(MIN_TIMEOUT_S, required)
    if not timeout_ok:
        raise SystemExit("TIMEOUT_TOO_SHORT timeout=%d required_at_least=%.3f" % (timeout_s, max(MIN_TIMEOUT_S, required)))

    work, out = Path(a.work), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name in ("resume", "runtime", "logs", "launches", "home"):
        (work/name).mkdir(parents=True, exist_ok=True)
    h6_path = work / "resume" / "h6-hybrid.sstate"
    h6_path.write_bytes(h6)
    base_card = Path(a.card)
    expected_card_sha = "ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5"
    if sha(base_card.read_bytes()) != expected_card_sha:
        raise SystemExit("REFERENCE_MEMORY_CARD_SHA_MISMATCH")

    appdir = Path(a.appdir)
    env_base = os.environ.copy()
    env_base.update({
        "DISPLAY": ":99", "LIBGL_ALWAYS_SOFTWARE": "1",
        "LD_LIBRARY_PATH": str(appdir/"usr/lib")+":"+str(appdir/"usr/lib/x86_64-linux-gnu"),
        "QT_PLUGIN_PATH": str(appdir/"usr/plugins"),
        "QT_QPA_PLATFORM_PLUGIN_PATH": str(appdir/"usr/plugins/platforms"),
        "QML2_IMPORT_PATH": str(appdir/"usr/qml"),
    })
    launches, manager_rows, tile_rows, aggregate_rows, table_rows = [], [], [], [], []
    all_ram_hashes = {}
    for attempt in (1, 2):
        launch = work / "launches" / ("attempt-%d" % attempt)
        runtime, home, logs = launch/"runtime", launch/"home", launch/"logs"
        for folder in (runtime, home/".config", home/".data", home/"runtime", logs):
            folder.mkdir(parents=True, exist_ok=True)
        try:
            (home/"runtime").chmod(0o700)
        except OSError:
            pass
        card = launch / "memory-card.mcd"
        shutil.copyfile(base_card, card)
        card_before = sha(card.read_bytes())
        lua_path = launch / "az1.lua"
        lua_path.write_text(make_lua(), encoding="utf-8")
        pad_text = (
            "PCSX.settings.pads[1].DeviceType = 'Analog'\n"
            "PCSX.settings.pads[1].Connected = true\n"
            "PCSX.SIO0.slots[1].pads[1].map()\n"
            "print('AZ1_CONTROLLER_MAPPED_NO_GAMEPLAY_INPUT=1')\n"
        )
        env = env_base.copy()
        env.update({
            "HOME": str(home), "XDG_CONFIG_HOME": str(home/".config"),
            "XDG_DATA_HOME": str(home/".data"), "XDG_RUNTIME_DIR": str(home/"runtime"),
            "AZ1_H6_STATE": str(h6_path), "AZ1_LAUNCH_START_EPOCH": str(time.time()),
        })
        stdout_path, pcsx_log_path = logs/"emulator-stdout.txt", logs/"pcsx-redux.log"
        command = [
            "timeout", "--signal=INT", "--kill-after=10s", "%ds" % timeout_s,
            a.pcsx_bin, "-noupdate", "-debugger", "-interpreter",
            "-bios", a.bios, "-iso", a.cue, "-memcard1", str(card),
            "-exec", pad_text, "-dofile", str(lua_path),
            "-softgpu", "-stdout", "-lua_stdout", "-logfile", str(pcsx_log_path), "-run",
        ]
        started = time.monotonic()
        with stdout_path.open("wb") as f:
            try:
                proc = subprocess.run(command, cwd=launch, env=env, stdout=f, stderr=subprocess.STDOUT, check=False)
                wrapper_rc = proc.returncode
            except Exception as exc:
                wrapper_rc = 255
                f.write(("AZ1_LAUNCH_EXCEPTION=" + repr(exc) + "\n").encode())
        wall = time.monotonic() - started
        log_text = stdout_path.read_text(encoding="utf-8", errors="replace")
        if pcsx_log_path.exists():
            log_text += "\n" + pcsx_log_path.read_text(encoding="utf-8", errors="replace")
        frame_results = {}
        for frame in (180, 360):
            state_path = runtime / ("frame%d.sstate" % frame)
            marker = "AZ1_FRAME%d_CAPTURE=PASS" % frame
            reached = "AZ1_POST_LOAD_FRAME=%d" % frame in log_text
            captured = marker in log_text and state_path.is_file()
            frame_results[frame] = {"reached": reached, "captured": captured, "ram_sha": "TIDAK TAHU"}
            if captured:
                try:
                    frame_results[frame]["ram_sha"], _, _, _ = read_snapshot(
                        state_path, attempt, frame, manager_rows, tile_rows, aggregate_rows, table_rows)
                    all_ram_hashes[(attempt, frame)] = frame_results[frame]["ram_sha"]
                except Exception as exc:
                    frame_results[frame]["parse_error"] = repr(exc)
            if state_path.exists():
                try:
                    state_path.unlink()
                except OSError:
                    pass
        emulator_exit, exit_source = parse_exit(wrapper_rc, log_text)
        card_after = sha(card.read_bytes()) if card.exists() else "TIDAK TAHU"
        launches.append({
            "attempt": attempt, "frame180_reached": "YES" if frame_results[180]["reached"] else "NO",
            "frame180_capture": "PASS" if frame_results[180]["captured"] else "FAIL",
            "frame180_ram_2mib_sha256": frame_results[180]["ram_sha"],
            "frame180_parse_error": frame_results[180].get("parse_error", ""),
            "frame360_reached": "YES" if frame_results[360]["reached"] else "NO",
            "frame360_capture": "PASS" if frame_results[360]["captured"] else "FAIL",
            "frame360_ram_2mib_sha256": frame_results[360]["ram_sha"],
            "frame360_parse_error": frame_results[360].get("parse_error", ""),
            "wrapper_exit_code_decimal": str(wrapper_rc), "emulator_exit_code_decimal": emulator_exit,
            "exit_code_source": exit_source, "wall_seconds": "%.3f" % wall,
            "memory_card_sha256_before": card_before, "memory_card_sha256_after": card_after,
            "memory_card_unchanged": "YES" if card_before == card_after else "NO",
        })

    def write_tsv(name, rows, columns):
        with (out/name).open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t", extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

    field_cols = ["attempt","frame","ram_first_2mib_sha256","global_0x80070C88_u32","global_0x80070C88_hex",
                  "manager_slot_0x8013A554","manager_pointer_valid","manager_B2A_u8","manager_B2B_u8",
                  "manager_B30_u32","manager_B30_hex","manager_B38_u32","manager_B38_hex",
                  "manager_B40_u32","manager_B40_hex","manager_B44_u32","manager_B44_hex"]
    tile_cols = ["attempt","frame","record_index","record_address","status_plus_00_u8","selector_plus_0B_u8",
                 "owner_hw_plus_20","owner_hw_plus_20_hex","owner_hw_shift_12","selected_B_offset",
                 "selected_B_u16","FUN_800B770C_recomputed_V","validation"]
    aggregate_cols = ["attempt","frame","aggregate_owner","status_scope","record_count_with_known_V","unknown_V_count",
                     "sum_V","floor_sum_V_div_2","manager_B38","matches_B38","manager_B2B_active_index",
                     "tile_array_pointer_slot","tile_array_pointer","tile_count_slot","tile_count","record_stride","validation"]
    table_cols = ["attempt","frame","mode_0x80070734_u32","state_0x8007073C_u8","state_read_method","matrix_base",
                  "matrix_stride_mode","matrix_stride_state","matrix_index_address","matrix_index_byte",
                  "selected_table_index","selected_row_base","selected_B30_address","selected_B30_u32",
                  "selected_B30_hex","selected_row_gate_plus_2E","selected_B30_source_expression",
                  "manager_B30_u32","matches_manager_B30","selection_status"]
    launch_cols = list(launches[0].keys())
    write_tsv("AZ1_MANAGER_FIELDS.tsv", manager_rows, field_cols)
    write_tsv("AZ1_TILE_RECORDS.tsv", tile_rows, tile_cols)
    write_tsv("AZ1_TILE_AGGREGATES.tsv", aggregate_rows, aggregate_cols)
    write_tsv("AZ1_TABLE_SELECTION.tsv", table_rows, table_cols)
    write_tsv("AZ1_LAUNCHES.tsv", launches, launch_cols)

    all_good = len(launches) == 2 and all(
        x["frame180_capture"] == "PASS" and x["frame360_capture"] == "PASS"
        and x["memory_card_unchanged"] == "YES" and x["emulator_exit_code_decimal"] == "0"
        for x in launches
    )
    complete_pairs = len(all_ram_hashes) == 4
    same_each_frame = all(
        all_ram_hashes.get((1, frame)) == all_ram_hashes.get((2, frame)) and all_ram_hashes.get((1, frame)) != "TIDAK TAHU"
        for frame in (180, 360)
    )
    max_wall = max(float(x["wall_seconds"]) for x in launches) if launches else 0.0
    timeout_twice_observed = timeout_s >= 2 * max_wall
    table_selection_complete = len(table_rows) == 4 and all(r.get("selection_status") == "PASS_STATIC_XREF_AND_RUNTIME_INDEX" for r in table_rows)
    exit_code = 0 if all_good and complete_pairs and same_each_frame and table_selection_complete and timeout_ok and timeout_twice_observed else 2
    status = "PASS" if exit_code == 0 else "INCOMPLETE"
    report = [
        "AZ1 — H6 HYBRID READ-ONLY ECONOMY SNAPSHOT",
        "STATUS=" + status,
        "H6_SHA256=" + h6_sha,
        "H6_IDENTITY=target checkpoint base + CONTROL top-level protobuf SPU field 6; H6 HYBRID, NOT TARGET-PURE",
        "INPUT=NONE; no button presses; no RAM poke or setter call; frame snapshots are copied to temporary files only",
        "FRAMES=180,360; LAUNCHES=2 independent restores",
        "MANAGER=read [0x8013A554], then +0xB2A,+0xB30,+0xB38,+0xB40,+0xB44; plus [0x80070C88]",
        "TILES=pointer [0x8013EA84], count [0x8013EAC8], stride 0x124, status +0x00, selector +0x0B, owner=(hw@+0x20)>>12, V recomputed from FUN_800B770C",
        "B30_TABLE=runtime mode [0x80070734] and state [0x8007073C]; static-confirmed index byte [0x80058758+mode*0x84+state*0x0C]; selected row 0x80057798+index*0x54; B30=u32(row+0x0C) (same as 0x800577A4+index*0x54)",
        "B38_COMPARISON=per-record owner and status 5; floor(sum(V)/2) is exported per owner and all-record aggregate; no semantic inference from zero totals",
        "RAM_COVERAGE=first 2 MiB from 0x80000000, SHA-256 per launch and frame",
        "HISTORICAL_SLOWEST_WALL_S=%.3f" % HISTORICAL_SLOWEST_LAUNCH_S,
        "TIMEOUT_PER_LAUNCH_S=%d" % timeout_s,
        "TIMEOUT_GE_2X_HISTORICAL_SLOWEST=%s" % timeout_ok,
        "OBSERVED_MAX_LAUNCH_WALL_S=%.3f" % max_wall,
        "TIMEOUT_GE_2X_OBSERVED_MAX=%s" % timeout_twice_observed,
        "TWO_LAUNCH_BOTH_FRAMES_CAPTURED=%s" % all_good,
        "TWO_LAUNCH_FRAME_SHA_IDENTICAL_PER_FRAME=%s" % same_each_frame,
        "ALL_FOUR_RAM_SNAPSHOTS_PARSED=%s" % complete_pairs,
        "TABLE_SELECTION_COMPLETE=%s" % table_selection_complete,
    ]
    for x in launches:
        report.extend([
            "ATTEMPT_%d_FRAME180_RAM_SHA256=%s" % (x["attempt"], x["frame180_ram_2mib_sha256"]),
            "ATTEMPT_%d_FRAME360_RAM_SHA256=%s" % (x["attempt"], x["frame360_ram_2mib_sha256"]),
            "ATTEMPT_%d_WRAPPER_EXIT_DECIMAL=%s" % (x["attempt"], x["wrapper_exit_code_decimal"]),
            "ATTEMPT_%d_EMULATOR_EXIT_DECIMAL=%s" % (x["attempt"], x["emulator_exit_code_decimal"]),
            "ATTEMPT_%d_WALL_SECONDS=%s" % (x["attempt"], x["wall_seconds"]),
            "ATTEMPT_%d_MEMCARD_BEFORE=%s" % (x["attempt"], x["memory_card_sha256_before"]),
            "ATTEMPT_%d_MEMCARD_AFTER=%s" % (x["attempt"], x["memory_card_sha256_after"]),
            "ATTEMPT_%d_MEMCARD_UNCHANGED=%s" % (x["attempt"], x["memory_card_unchanged"]),
        ])
    if manager_rows:
        for r in manager_rows:
            report.append("SNAPSHOT_ATTEMPT_%s_FRAME_%s_MANAGER_B30=%s_B38=%s_B40=%s_B44=%s" % (
                r["attempt"], r["frame"], r.get("manager_B30_u32","TIDAK TAHU"),
                r.get("manager_B38_u32","TIDAK TAHU"), r.get("manager_B40_u32","TIDAK TAHU"),
                r.get("manager_B44_u32","TIDAK TAHU")))
    report.append("ZERO_MEANS_ONLY_THE_CAPTURED_VALUE; it is not a semantic conclusion about a transaction or event.")
    report.append("All temporary H6/target/control/BIOS/disc/Memory Card/RAM snapshots were removed before text-only publication.")
    (out/"AZ1_H6_ECONOMY_SUMMARY.txt").write_text("\n".join(report)+"\n", encoding="utf-8")
    (out/"AZ1_SCRIPT_EXIT_CODE.txt").write_text("AZ1_SCRIPT_EXIT_CODE=%d\n" % exit_code, encoding="utf-8")
    job_summary = [
        "STATUS="+status, "JOB=az1-h6-economy-runtime",
        "RUN_ID="+os.getenv("GITHUB_RUN_ID","TIDAK TAHU"),
        "RUN_ATTEMPT="+os.getenv("GITHUB_RUN_ATTEMPT","TIDAK TAHU"),
        "SOURCE_SHA="+os.getenv("GITHUB_SHA","TIDAK TAHU"),
        "H6_SHA256="+h6_sha, "EXIT_CODE="+str(exit_code),
        "TIMEOUT_PER_LAUNCH_S="+str(timeout_s),
    ]
    (out/"ACTIONS_RUN_SUMMARY.txt").write_text("\n".join(job_summary)+"\n", encoding="utf-8")
    print("\n".join(job_summary))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
