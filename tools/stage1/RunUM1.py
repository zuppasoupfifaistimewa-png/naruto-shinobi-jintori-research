#!/usr/bin/env python3
"""UM1: bounded read-only frame-1 snapshots, with no game input or write watch."""
from __future__ import annotations
import argparse, csv, hashlib, os, shutil
from collections import defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from experiments import ub2_headless_trace as runner

CHECKPOINT_SHA = "705d4005dacee3b492ae99f273b1572bb5be3e3b66ad32c0b556dd5065e58a35"
CHECKPOINT_BYTES = 21162799
CARD_SHA = "78b6d4ac9ab4d23caf7e5f04f83539bf5d994cccfb0a709d14ac53d05c8e21ef"
CARD_BYTES = 131072
RAM_START = 0x80000000
RAM_END = 0x80200000
STRIDE = 0x124
RECORDS = tuple([f"A:{i}" for i in range(22)] + ["A:22", "A:43"])
SCALARS = (("P", 0x8013EA84, 4), ("index_8013EB20", 0x8013EB20, 4),
           ("value_8013EAB0", 0x8013EAB0, 4), ("value_8013EA8A", 0x8013EA8A, 2),
           ("value_8013EA74", 0x8013EA74, 4), ("state_80139F03", 0x80139F03, 1),
           ("counter_80139EC2", 0x80139EC2, 2))
BYTE_FIELDS = ["launch", "frame", "record", "offset", "address", "byte_hex"]
SCALAR_FIELDS = ["launch", "frame", "name", "address", "width", "value_hex"]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def write_tsv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def tail_text(source: Path, destination: Path, limit: int = 200) -> int:
    if not source.is_file():
        destination.write_text("LOG_FILE_NOT_CREATED\n", encoding="utf-8")
        return 0
    lines = source.read_text(encoding="utf-8", errors="replace").splitlines()
    selected = lines[-limit:]
    destination.write_text("\n".join(selected) + ("\n" if selected else ""), encoding="utf-8")
    return len(selected)


def lua_probe(launch: str, card: Path) -> str:
    card_text = str(card).replace("\\", "\\\\").replace('"', '\\"')
    return r'''local ffi=require("ffi")
local LAUNCH="''' + launch + r'''"
local CARD_PATH="''' + card_text + r'''"
local RAM_START=0x80000000
local RAM_END=0x80200000
local MOD=4294967296
local mem=PCSX.getMemPtr()
local loaded,started,post,card_marked=false,false,0,false
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
local function file_size(path)
 local ok,f=pcall(function() return io.open(path,"rb") end)
 if not ok or not f then return -1 end
 local ok2,n=pcall(function() return f:seek("end") end); f:close()
 if not ok2 or n==nil then return -1 end
 return tonumber(n)
end
local function hx(v,w)
 if v==nil then return "TIDAK_TAHU" end
 if w==1 then return string.format("0x%02X",tonumber(v)%256) end
 if w==2 then return string.format("0x%04X",tonumber(v)%65536) end
 return string.format("0x%08X",tonumber(v)%MOD)
end
local function readv(a,w)
 local va=tonumber(a)%MOD; local phys=va%0x20000000
 if va<RAM_START or va>=RAM_END or va+w>RAM_END or phys+w>0x200000 then return nil,"OUTSIDE_RAM" end
 local ok,v=pcall(function()
  if w==1 then return tonumber(ffi.cast("const uint8_t *",mem+phys)[0]) end
  if w==2 then return tonumber(ffi.cast("const uint16_t *",mem+phys)[0]) end
  return tonumber(ffi.cast("const uint32_t *",mem+phys)[0])
 end)
 if not ok or v==nil then return nil,"READ_ERROR" end
 return v,nil
end
local function snapshot()
 log("UM1_POST_LOAD_VSYNC_1=YES launch="..LAUNCH)
 log("UM1_SNAPSHOT_BEGIN launch="..LAUNCH.." frame=1")
 local p=nil
 local specs={
  {"P",0x8013EA84,4},{"index_8013EB20",0x8013EB20,4},{"value_8013EAB0",0x8013EAB0,4},
  {"value_8013EA8A",0x8013EA8A,2},{"value_8013EA74",0x8013EA74,4},
  {"state_80139F03",0x80139F03,1},{"counter_80139EC2",0x80139EC2,2}
 }
 local scalar_bad=0
 for _,s in ipairs(specs) do
  local v,e=readv(s[2],s[3]); if e then scalar_bad=scalar_bad+1 end
  log(table.concat({"UM1_SCALAR",LAUNCH,"1",s[1],string.format("0x%08X",s[2]),"u"..tostring(s[3]),e or hx(v,s[3])},"\t"))
  if s[1]=="P" then p=v end
 end
 if p==nil or p<RAM_START or p>=RAM_END then
  log("UM1_POINTER_INVALID="..tostring(p)); log("UM1_SNAPSHOT_COMPLETE=NO reason=pointer_invalid")
  PCSX.nextTick(function() PCSX.quit(53) end); return
 end
 local wanted={}
 for i=0,21 do wanted[#wanted+1]={"A:"..tostring(i),i} end
 wanted[#wanted+1]={"A:22",22}; wanted[#wanted+1]={"A:43",43}
 local total,invalid=0,scalar_bad
 for _,r in ipairs(wanted) do
  local name=r[1]; local i=r[2]; local first=p+i*0x124; local last=first+0x123
  if first<RAM_START or last>=RAM_END then
   invalid=invalid+1; log("UM1_RECORD_OUTSIDE_RAM\t"..LAUNCH.."\t"..name.."\t"..string.format("0x%08X",first).."\t"..string.format("0x%08X",last))
  else
   for off=0,0x123 do
    local a=first+off; local v,e=readv(a,1)
    if e then invalid=invalid+1 end
    log(table.concat({"UM1_BYTE",LAUNCH,"1",name,string.format("0x%03X",off),string.format("0x%08X",a),e or hx(v,1)},"\t"))
    total=total+1
   end
  end
  if i==43 then
   local finish=first+0x124
   log("UM1_A43_END_EXCLUSIVE="..string.format("0x%08X",finish).." expected=0x8013EA48")
  end
 end
 log("UM1_SNAPSHOT_END\t"..LAUNCH.."\tbytes="..tostring(total).."\tinvalid="..tostring(invalid).."\tpost_load_frame=1")
 local endpoint=p+44*0x124
 local ok=(total==7008 and invalid==0 and endpoint==0x8013EA48)
 log("UM1_SNAPSHOT_COMPLETE="..(ok and "YES" or "NO").." launch="..LAUNCH.." bytes="..tostring(total).." scalars=7 endpoint="..string.format("0x%08X",endpoint))
 PCSX.nextTick(function() PCSX.quit(ok and 0 or 54) end)
end
_G.um1Loaded=PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded",function()
 loaded=true; post=0; log("UM1_SAVE_STATE_LOADED=YES launch="..LAUNCH)
end)
_G.um1Vsync=PCSX.Events.createEventListener("GPU::Vsync",function()
 if not card_marked then
  local n=file_size(CARD_PATH)
  if n==131072 then card_marked=true; log("UM1_CARD_READY launch="..LAUNCH.." bytes="..tostring(n).." read_only_expected=yes") end
 end
 if not started then
  if not card_marked then return end
  started=true
  local path=os.getenv("UE2_SOURCE_STATE") or "resume/source.sstate"
  log("UM1_LOAD_STATE_START launch="..LAUNCH.." path="..path)
  PCSX.pauseEmulator()
  PCSX.nextTick(function()
   local okf,f=pcall(function() return assert(Support.File.open(path)) end)
   if not okf or not f then log("UM1_STATE_OPEN_FAIL="..tostring(f)); PCSX.quit(50); return end
   local ok,e=pcall(function() PCSX.loadSaveState(f) end); f:close()
   if not ok then log("UM1_STATE_LOAD_FAIL="..tostring(e)); PCSX.quit(51); return end
   log("UM1_LOAD_STATE_CALL_RETURNED=YES launch="..LAUNCH)
   PCSX.resumeEmulator()
  end)
  return
 end
 if not loaded then return end
 post=post+1
 if post==1 then snapshot() end
end)
log("UM1_SCRIPT_READY launch="..LAUNCH.." frame1_only=YES memory_write=NO write_watch=NO input=NO")
'''.lstrip()


def parse_log(log: str, launch: str) -> tuple[list[dict], list[dict], bool, str]:
    byte_rows, scalar_rows = [], []
    for line in log.splitlines():
        if line.startswith("UM1_BYTE\t"):
            p = line.split("\t")
            if len(p) == 7:
                byte_rows.append(dict(zip(BYTE_FIELDS, p[1:])))
        elif line.startswith("UM1_SCALAR\t"):
            p = line.split("\t")
            if len(p) == 7:
                scalar_rows.append(dict(zip(SCALAR_FIELDS, p[1:])))
    valid = True
    if len(byte_rows) != 7008 or len(scalar_rows) != 7:
        valid = False
    seen = set()
    for r in byte_rows:
        try:
            key = (r["record"], int(r["offset"], 16))
            address = int(r["address"], 16); value = int(r["byte_hex"], 16)
            off = key[1]
            if key in seen or not 0 <= off <= 0x123 or not RAM_START <= address < RAM_END or not 0 <= value <= 255 or r["frame"] != "1":
                valid = False
            seen.add(key)
        except (ValueError, KeyError, IndexError):
            valid = False
    wanted = {(record, off) for record in RECORDS for off in range(0x124)}
    if seen != wanted:
        valid = False
    scalar_by_name = {r["name"]: r for r in scalar_rows}
    if set(scalar_by_name) != {x[0] for x in SCALARS}:
        valid = False
    try:
        p_value = int(scalar_by_name["P"]["value_hex"], 16)
        if not RAM_START <= p_value < RAM_END:
            valid = False
        for r in byte_rows:
            idx = int(r["record"].split(":", 1)[1]); off = int(r["offset"], 16)
            if int(r["address"], 16) != p_value + idx * STRIDE + off:
                valid = False
        expected_end = p_value + 44 * STRIDE
        endpoint_ok = expected_end == 0x8013EA48
    except (ValueError, KeyError):
        endpoint_ok = False; valid = False
    for _, address, width in SCALARS:
        row = next((r for r in scalar_rows if r["address"] == f"0x{address:08X}"), None)
        try:
            if row is None or row["frame"] != "1" or int(row["width"][1:]) != width or not RAM_START <= address < RAM_END:
                valid = False
            int(row["value_hex"], 16)
        except (ValueError, KeyError, TypeError):
            valid = False
    complete_marker = f"UM1_SNAPSHOT_COMPLETE=YES launch={launch}" in log
    last = "NONE"
    for marker, name in (("UM1_SCRIPT_READY", "SCRIPT_READY"), ("UM1_CARD_READY", "CARD_READY"), ("UM1_LOAD_STATE_START", "LOAD_STATE_START"),
                         ("UM1_SAVE_STATE_LOADED=YES", "SAVE_STATE_LOADED"), ("UM1_POST_LOAD_VSYNC_1=YES", "POST_LOAD_VSYNC_1"),
                         ("UM1_SNAPSHOT_COMPLETE=YES", "SNAPSHOT_COMPLETE")):
        if marker in log:
            last = name
    return byte_rows, scalar_rows, valid and endpoint_ok and complete_marker, last


def read_lv_table(path: Path) -> dict[int, list[int]]:
    rows = {}
    with path.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            rows[int(r["X"])] = [int(r[f"LV{i}"]) for i in range(1, 6)]
    return rows


def derive(rows: list[dict], table: dict[int, list[int]]):
    groups = defaultdict(list)
    grouped = defaultdict(dict)
    for r in rows:
        value = int(r["byte_hex"], 16)
        groups[(r["launch"], int(r["offset"], 16))].append(value)
        grouped[(r["launch"], r["record"])][int(r["offset"], 16)] = value
    offset_rows = []
    for (launch, off), values in sorted(groups.items()):
        distinct = sorted(set(values))
        offset_rows.append({"launch": launch, "offset": f"0x{off:03X}", "record_count": len(values),
                            "distinct_values": len(distinct), "status": "KONSTAN" if len(distinct) == 1 else "BERVARIASI",
                            "values_hex": ";".join(f"0x{x:02X}" for x in distinct)})
    lv_rows = []
    for (launch, record), bmap in sorted(grouped.items()):
        x = 2 * (bmap[0x1A] + (bmap[0x1B] << 8))
        vals = table.get(x)
        if vals is None:
            lv_rows.append({"launch": launch, "record": record, "X_2xu16_plus_1A": x, "status": "X_NOT_IN_SOURCE_TABLE",
                            "LV": "", "table_value": "TIDAK ADA", "match_count": 0, "matching_u16_offsets": ""})
            continue
        for lv_i, target in enumerate(vals, 1):
            matches = [off for off in range(0x123) if bmap.get(off) is not None and bmap.get(off + 1) is not None
                       and bmap[off] + (bmap[off + 1] << 8) == target]
            lv_rows.append({"launch": launch, "record": record, "X_2xu16_plus_1A": x, "status": "TABLE_X_MATCHED",
                            "LV": f"LV{lv_i}", "table_value": target, "match_count": len(matches),
                            "matching_u16_offsets": ";".join(f"0x{o:03X}" for o in matches)})
    return offset_rows, lv_rows


def self_test() -> None:
    p = 0x8013B818
    assert len(RECORDS) == 24 and 24 * 0x124 == 7008
    assert p + 44 * STRIDE == 0x8013EA48
    assert lua_probe("SELFTEST", Path("/tmp/test-card.mcd")).count("UM1_POST_LOAD_VSYNC_1") == 1
    fake = []
    for record in RECORDS:
        for off in range(0x124):
            fake.append({"launch": "L1", "record": record, "offset": f"0x{off:03X}", "byte_hex": "0x00"})
    offsets, matches = derive(fake, {0: [0, 1, 2, 3, 4]})
    assert len(offsets) == 0x124 and len(matches) == 24 * 5
    assert all(x["match_count"] == 0x123 for x in matches if x["LV"] == "LV1")
    print("UM1_SELF_TEST=PASS records=24 bytes_per_record=292 frame=1 scalars=7 A43_end_exclusive=0x8013EA48")


def main() -> int:
    ap = argparse.ArgumentParser()
    for n in ("work", "out", "pcsx-bin", "appdir", "bios", "cue", "source", "lv-table"):
        ap.add_argument("--" + n, type=Path)
    ap.add_argument("--timeout-seconds", type=int, default=120)
    ap.add_argument("--max-launches", type=int, default=4)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test(); return 0
    if not all((a.work, a.out, a.pcsx_bin, a.appdir, a.bios, a.cue, a.source, a.lv_table)):
        ap.error("runtime arguments missing")
    if a.timeout_seconds != 120 or a.max_launches != 4:
        ap.error("UM1 policy fixed to 120 seconds and at most four total emulator launches")
    work, out = a.work, a.out
    work.mkdir(parents=True, exist_ok=True); out.mkdir(parents=True, exist_ok=True)
    source = a.source
    if not source.is_file() or source.stat().st_size != CHECKPOINT_BYTES or sha(source) != CHECKPOINT_SHA:
        raise SystemExit("UM1_CHECKPOINT_IDENTITY_MISMATCH")
    source.chmod(0o444)
    source_before = sha(source)
    card_dir = work / "cards"; card_dir.mkdir(parents=True, exist_ok=True)
    template = card_dir / "memory-card-template.mcd"
    template.unlink(missing_ok=True)
    warm_lua = work / "card-warmup.lua"; warm_lua.write_text(runner.lua_warmup(), encoding="utf-8")
    warm_stdout = work / "card-warmup.stdout.txt"
    warm_home = work / "card-warmup-home"
    warm_rc, warm_wall, _ = runner.run_emulator(a.pcsx_bin, a.appdir, a.bios, a.cue, template, None,
                                                warm_lua, warm_home, warm_stdout, a.timeout_seconds)
    warm_log = runner.read_log_text(warm_stdout)
    warm_hash = sha(template) if template.is_file() else "TIDAK TAHU"
    if template.is_file() and template.stat().st_size == CARD_BYTES:
        warm_marker = "CARD_READY_HASH_MATCH" if warm_hash == CARD_SHA else "CARD_READY_HASH_MISMATCH"
    elif "UB2_MEMCARD_WARMUP_READY=1" in warm_log:
        warm_marker = "WARMUP_READY"
    else:
        warm_marker = "NONE"
    warm_ok = warm_rc == 0 and "UB2_MEMCARD_WARMUP_FRAMES=12" in warm_log and template.is_file() and template.stat().st_size == CARD_BYTES and warm_hash == CARD_SHA
    launch_rows = [{"launch": "CARD_WARMUP", "kind": "CARD_INITIALIZATION", "status": "PASS" if warm_ok else "FAIL",
                    "exit_code": warm_rc, "checkpoint_sha256_before": source_before, "checkpoint_sha256_after": sha(source),
                    "card_sha256_before": "NOT_CREATED", "card_sha256_after": warm_hash, "card_unchanged": "N/A",
                    "card_mode_0444": "N/A", "snapshot_bytes": 0, "snapshot_scalars": 0, "last_marker": warm_marker,
                    "wall_seconds": f"{warm_wall:.3f}"}]
    tail_text(warm_stdout, out / "UM1_CARD_WARMUP_STDOUT_TAIL.txt")
    tail_text(warm_stdout.with_suffix(".pcsx.log"), out / "UM1_CARD_WARMUP_PCSX_TAIL.txt")
    all_bytes, all_scalars = [], []
    validated_bytes = []
    successful = []
    if warm_ok:
        template.chmod(0o444)
        for attempt in range(1, 4):
            launch = f"MEASURE_{attempt}"
            d = work / launch.lower(); d.mkdir(parents=True, exist_ok=True)
            state = d / "source.sstate"; shutil.copyfile(source, state); state.chmod(0o444)
            card = d / "memory-card.mcd"; shutil.copyfile(template, card); card.chmod(0o444)
            lua = d / "um1.lua"; lua.write_text(lua_probe(launch, card), encoding="utf-8")
            stdout = d / "emulator.stdout.txt"
            source_hash_before = sha(source); state_hash_before = sha(state); card_hash_before = sha(card)
            rc, wall, _ = runner.run_emulator(a.pcsx_bin, a.appdir, a.bios, a.cue, card, state,
                                              lua, d / "home", stdout, a.timeout_seconds)
            log = runner.read_log_text(stdout)
            tail_text(stdout, out / f"UM1_{attempt:02d}_STDOUT_TAIL.txt")
            tail_text(stdout.with_suffix(".pcsx.log"), out / f"UM1_{attempt:02d}_PCSX_TAIL.txt")
            b_rows, s_rows, parsed_ok, last = parse_log(log, launch)
            all_bytes.extend(b_rows); all_scalars.extend(s_rows)
            state_hash_after = sha(state) if state.exists() else "TIDAK TAHU"
            source_hash_after = sha(source) if source.exists() else "TIDAK TAHU"
            card_hash_after = sha(card) if card.exists() else "TIDAK TAHU"
            card_readonly = card.exists() and (card.stat().st_mode & 0o777) == 0o444
            checkpoint_ok = state_hash_before == state_hash_after == CHECKPOINT_SHA and source_hash_before == source_hash_after == CHECKPOINT_SHA
            card_ok = card_hash_before == card_hash_after == CARD_SHA and card_readonly
            success = rc == 0 and parsed_ok and checkpoint_ok and card_ok
            launch_rows.append({"launch": launch, "kind": "FRAME1_READ_ONLY", "status": "PASS" if success else "FAIL",
                                "exit_code": rc, "checkpoint_sha256_before": state_hash_before, "checkpoint_sha256_after": state_hash_after,
                                "checkpoint_source_sha256_before": source_hash_before, "checkpoint_source_sha256_after": source_hash_after,
                                "card_sha256_before": card_hash_before, "card_sha256_after": card_hash_after,
                                "card_unchanged": "YES" if card_hash_before == card_hash_after else "NO",
                                "card_mode_0444": "YES" if card_readonly else "NO", "snapshot_bytes": len(b_rows),
                                "snapshot_scalars": len(s_rows), "last_marker": last, "wall_seconds": f"{wall:.3f}"})
            if success:
                validated_bytes.extend(b_rows)
                successful.append((launch, b_rows, s_rows))
                if len(successful) >= 2:
                    found_pair = None
                    for i in range(len(successful)):
                        for j in range(i + 1, len(successful)):
                            def signature(item):
                                _, br, sr = item
                                b = tuple(sorted((r["record"], r["offset"], r["address"], r["byte_hex"]) for r in br))
                                s = tuple(sorted((r["name"], r["address"], r["width"], r["value_hex"]) for r in sr))
                                return b, s
                            if signature(successful[i]) == signature(successful[j]):
                                found_pair = (successful[i][0], successful[j][0])
                                break
                        if found_pair:
                            break
                    if found_pair:
                        break
            state.unlink(missing_ok=True); card.unlink(missing_ok=True)
    else:
        (out / "UM1_CARD_WARMUP_REASON.txt").write_text(f"CARD_WARMUP_STATUS=FAIL\nEXIT_CODE={warm_rc}\nCARD_SHA256={warm_hash}\nEXPECTED_CARD_SHA256={CARD_SHA}\nLAST_MARKER=WARMUP_FAILED\n", encoding="utf-8")
    source_after = sha(source) if source.exists() else "TIDAK TAHU"
    write_tsv(out / "UM1_BYTES.tsv", BYTE_FIELDS, all_bytes)
    write_tsv(out / "UM1_SCALARS.tsv", SCALAR_FIELDS, all_scalars)
    offset_rows, lv_rows = derive(validated_bytes, read_lv_table(a.lv_table)) if validated_bytes else ([], [])
    write_tsv(out / "UM1_OFFSET_SUMMARY.tsv", ["launch","offset","record_count","distinct_values","status","values_hex"], offset_rows)
    write_tsv(out / "UM1_LV_U16_MATCHES.tsv", ["launch","record","X_2xu16_plus_1A","status","LV","table_value","match_count","matching_u16_offsets"], lv_rows)
    write_tsv(out / "UM1_LAUNCHES.tsv", list(dict.fromkeys(k for row in launch_rows for k in row.keys())), launch_rows)
    zero = sum(1 for r in lv_rows if r.get("match_count") == 0 and r.get("status") == "TABLE_X_MATCHED")
    matched = sum(int(r.get("match_count", 0)) for r in lv_rows if r.get("status") == "TABLE_X_MATCHED")
    pair_identical = bool('found_pair' in locals() and found_pair)
    if pair_identical:
        status, evidence = "TUNTAS", "K5"
    elif successful:
        status, evidence = "SEBAGIAN", "K4"
    else:
        status, evidence = "BELUM", "K0"
    last_overall = next((r["last_marker"] for r in reversed(launch_rows) if r.get("kind") == "FRAME1_READ_ONLY"), launch_rows[-1].get("last_marker", "NONE"))
    summary = [
        "UM1_FRAME1_POST_LOAD_READ_ONLY_SNAPSHOT", f"STATUS={status}", f"EVIDENCE={evidence}",
        "JOB=um-audit", f"SOURCE_SHA={os.getenv('GITHUB_SHA','TIDAK TAHU')}", f"RUN_ID={os.getenv('GITHUB_RUN_ID','TIDAK TAHU')}",
        f"CHECKPOINT_SHA256_EXPECTED={CHECKPOINT_SHA}", f"CHECKPOINT_SOURCE_SHA256_BEFORE={source_before}", f"CHECKPOINT_SOURCE_SHA256_AFTER={source_after}",
        "CHECKPOINT_MODE=0444; no checkpoint writes", f"CARD_SHA256_EXPECTED={CARD_SHA}", f"CARD_SHA256_FROM_WARMUP={warm_hash}",
        f"CARD_WARMUP_EXIT_CODE={warm_rc}", f"CARD_WARMUP_WALL_SECONDS={warm_wall:.3f}", f"CARD_WARMUP_STATUS={'PASS' if warm_ok else 'FAIL'}",
        "CARD_WARMUP_COUNTS_AS_LAUNCH=YES", "LAUNCH_BUDGET_TOTAL=4 (one card warmup + at most three measured launches)",
        f"MEASURED_LAUNCHES={len(launch_rows)-1}", f"SUCCESSFUL_SNAPSHOTS={len(successful)}", f"BYTE_ROWS_RAW_ALL_LAUNCHES={len(all_bytes)}", f"SCALAR_ROWS_RAW_ALL_LAUNCHES={len(all_scalars)}",
        f"BYTE_ROWS_VALIDATED_SNAPSHOTS={len(validated_bytes)}",
        "RECORDS=A:0..21;A:22;A:43; each 0x124 bytes", "SCALARS=P:u32,0x8013EB20:u32,0x8013EAB0:u32,0x8013EA8A:u16,0x8013EA74:u32,0x80139F03:u8,0x80139EC2:u16",
        "FRAME=first GPU::Vsync after ExecutionFlow::SaveStateLoaded only; no input; no write-watch; all loads const/read-only",
        f"A43_END_EXCLUSIVE_CHECK={'PASS' if any('UM1_A43_END_EXCLUSIVE=0x8013EA48' in (work / f'measure_{i}' / 'emulator.stdout.txt').read_text(encoding='utf-8',errors='replace') for i in range(1,4) if (work / f'measure_{i}' / 'emulator.stdout.txt').exists()) else 'NOT_PASSED'} expected=0x8013EA48",
        f"LAST_STAGE_MARKER={last_overall if last_overall != 'NONE' else warm_marker}", f"IDENTICAL_SUCCESSFUL_LAUNCH_PAIR={'YES' if pair_identical else 'NO'}",
        f"IDENTICAL_PAIR_NAMES={found_pair if pair_identical else 'TIDAK ADA'}", f"TABLE_X_RECORD_ROWS={sum(1 for r in lv_rows if r.get('status')=='TABLE_X_MATCHED')}",
        f"U16_MATCH_COUNT_TOTAL={matched}", f"TABLE_X_LV_ROWS_WITH_ZERO_MATCHES={zero}",
        "MEANING_OF_SCALARS_AND_RECORD_FIELDS=TIDAK TAHU", "RAW_RAM_DUMP=NONE", "EXIT_CODE=0" if pair_identical else "EXIT_CODE=2",
    ]
    (out / "UM1_SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    return 0 if pair_identical else 2

if __name__ == "__main__":
    raise SystemExit(main())
