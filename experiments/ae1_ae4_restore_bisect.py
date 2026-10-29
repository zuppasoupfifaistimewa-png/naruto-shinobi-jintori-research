#!/usr/bin/env python3
"""AE1-AE4 reproducible raw savestate field audit and no-input GDB restore tests.

All savestates and current RAM snapshots stay in the ephemeral Actions workspace.
Only text logs, hashes, field sizes, and requested RAM words are written to output.
"""
from __future__ import annotations
import argparse, hashlib, os, re, shutil, subprocess, time
from collections import defaultdict
from pathlib import Path

TOP = {
  1: ("save_state_info", "Message<SaveStateInfo>"),
  2: ("thumbnail", "Message<Thumbnail>"),
  3: ("memory", "Message<Memory>"),
  4: ("registers", "Message<Registers>"),
  5: ("gpu", "Message<GPU>"),
  6: ("spu", "Message<SPU>"),
  7: ("sio", "Message<SIO>"),
  8: ("cdrom", "Message<CDRom>"),
  9: ("hardware", "Message<Hardware>"),
  10: ("counters", "Message<Counters>"),
  11: ("mdec", "Message<MDEC>"),
  13: ("pcdrv_files", "RepeatedVariableField<PCdrvFile>"),
  14: ("callstacks", "Message<CallStacks>"),
}
SPU = {
  1: ("ram", "FixedBytes<0x80000>"),
  2: ("ports", "FixedBytes<0x200>"),
  3: ("xa", "Message<XA>"),
  4: ("irq", "UInt32"),
  5: ("irqptr", "UInt64"),
  6: ("channel", "Repeated<Message<Channel>, 24>"),
  7: ("addr", "UInt32"),
  8: ("ctrl", "UInt16"),
  9: ("stat", "UInt16"),
  10: ("cbStartInd", "Int32"),
  11: ("cbCurrInd", "Int32"),
  12: ("cbEndInd", "Int32"),
  13: ("cbVoiceInd", "Int32"),
  14: ("CBLeft", "FixedBytes<32768>"),
  15: ("CBRight", "FixedBytes<32768>"),
  16: ("noiseClock", "UInt32"),
  17: ("noiseCount", "UInt32"),
  18: ("noiseVal", "UInt32"),
  19: ("endx", "UInt32"),
}
RAM_BASE = 0x80000000
RAM_BYTES = 0x200000
RAM_ADDRS = (0x80070EB8, 0x80070F6C, 0x8013A554)
PIN = "0c3572c3d"
HEADER_GIT_BLOB_SHA1 = "72b7ab0dbd4191f9d9ed4cdd9d77898f467258e2"
SOURCE_URL = "https://github.com/pcsx-redux/pcsx-redux/blob/0c3572c3d/src/core/sstate.h"

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def varint(buf: bytes, pos: int):
    value = 0
    shift = 0
    start = pos
    while pos < len(buf) and shift <= 70:
        b = buf[pos]
        pos += 1
        value |= (b & 0x7f) << shift
        if not (b & 0x80):
            return value, pos, pos - start
        shift += 7
    raise ValueError("invalid/truncated varint at offset %d" % start)

def encvarint(value: int) -> bytes:
    if value < 0:
        raise ValueError("negative protobuf varint")
    out = bytearray()
    while value > 0x7f:
        out.append((value & 0x7f) | 0x80)
        value >>= 7
    out.append(value)
    return bytes(out)

def parse(data: bytes):
    out = []
    pos = 0
    while pos < len(data):
        start = pos
        tag, pos, _ = varint(data, pos)
        number, wire = tag >> 3, tag & 7
        if number == 0:
            raise ValueError("protobuf field number 0 at offset %d" % start)
        if wire == 0:
            ps = pos
            _, pos, _ = varint(data, pos)
            pe = pos
        elif wire == 1:
            ps, pe = pos, pos + 8
            pos = pe
        elif wire == 2:
            length, pos, _ = varint(data, pos)
            ps, pe = pos, pos + length
            if pe > len(data):
                raise ValueError("wire-2 overrun field %d at offset %d" % (number, start))
            pos = pe
        elif wire == 5:
            ps, pe = pos, pos + 4
            pos = pe
        else:
            raise ValueError("unsupported wire type %d at offset %d" % (wire, start))
        if pos > len(data):
            raise ValueError("truncated field %d at offset %d" % (number, start))
        out.append({
            "num": number, "wire": wire, "start": start, "ps": ps, "pe": pe,
            "end": pos, "enc": data[start:pos], "payload": data[ps:pe],
            "payload_len": pe-ps, "encoded_len": pos-start,
        })
    return out

def grouped(records):
    g = defaultdict(list)
    for record in records:
        g[record["num"]].append(record)
    return g

def get_payload(data: bytes, num: int) -> bytes:
    found = [r for r in parse(data) if r["num"] == num and r["wire"] == 2]
    if len(found) != 1:
        raise ValueError("expected one top-level field %d wire2, got %d" % (num, len(found)))
    return found[0]["payload"]

def encode_len_field(number: int, payload: bytes) -> bytes:
    return encvarint((number << 3) | 2) + encvarint(len(payload)) + payload

def replace_top_field(base: bytes, source: bytes, number: int) -> bytes:
    br = parse(base)
    sr = parse(source)
    replacements = [r["enc"] for r in sr if r["num"] == number]
    if not replacements:
        raise ValueError("source has no top-level field %d" % number)
    result = bytearray()
    inserted = False
    for r in br:
        if r["num"] == number:
            if not inserted:
                result.extend(b"".join(replacements))
                inserted = True
        else:
            result.extend(r["enc"])
    if not inserted:
        # Put the new field before the first larger tag, preserving the usual schema order.
        added = False
        result2 = bytearray()
        for r in br:
            if not added and r["num"] > number:
                result2.extend(b"".join(replacements)); added = True
            result2.extend(r["enc"])
        if not added:
            result2.extend(b"".join(replacements))
        result = result2
    return bytes(result)

def nested_replacements(base_payload: bytes, source_payload: bytes, selected):
    """Use source field occurrences selected by (field_number, zero-based occurrence).

    Unselected content remains byte-identical to base. Per-field occurrence order is kept;
    new selected occurrences are inserted at the end of their field-number run.
    """
    base_records, source_records = parse(base_payload), parse(source_payload)
    bg, sg = grouped(base_records), grouped(source_records)
    selected = set(selected)
    out = bytearray()
    seen = defaultdict(int)
    added_empty_groups = set()
    for r in base_records:
        n = r["num"]
        index = seen[n]
        seen[n] += 1
        if (n, index) in selected:
            if index < len(sg.get(n, [])):
                out.extend(sg[n][index]["enc"])
        else:
            out.extend(r["enc"])
        if index == len(bg[n])-1:
            # Insert selected source occurrences beyond the base's repeated count.
            for extra in range(len(bg[n]), len(sg.get(n, []))):
                if (n, extra) in selected:
                    out.extend(sg[n][extra]["enc"])
            added_empty_groups.add(n)
    # Fields present only in source have no base run to anchor them.
    for n in sorted(set(sg) - set(bg)):
        for i, r in enumerate(sg[n]):
            if (n, i) in selected:
                out.extend(r["enc"])
    return bytes(out)

def make_spu_hybrid(base_state: bytes, source_state: bytes, selected):
    base_spu = get_payload(base_state, 6)
    source_spu = get_payload(source_state, 6)
    new_spu = nested_replacements(base_spu, source_spu, selected)
    hybrid = replace_top_field(base_state, encode_len_field(6, new_spu), 6)
    return hybrid

def child_diff_keys(target_spu: bytes, control_spu: bytes):
    tg, cg = grouped(parse(target_spu)), grouped(parse(control_spu))
    changed = []
    for n in sorted(set(tg) | set(cg)):
        for i in range(max(len(tg.get(n, [])), len(cg.get(n, [])))):
            te = tg[n][i]["enc"] if i < len(tg.get(n, [])) else None
            ce = cg[n][i]["enc"] if i < len(cg.get(n, [])) else None
            if te != ce:
                changed.append((n, i))
    return changed

def ram_info(state: bytes):
    memory = get_payload(state, 3)
    ram_fields = [r for r in parse(memory) if r["num"] == 1 and r["wire"] == 2]
    if len(ram_fields) != 1:
        raise ValueError("expected one Memory.ram field, got %d" % len(ram_fields))
    ram = ram_fields[0]["payload"]
    if len(ram) < RAM_BYTES:
        raise ValueError("Memory.ram shorter than PS1's 2 MiB RAM: %d" % len(ram))
    guest_ram = ram[:RAM_BYTES]
    words = []
    for addr in RAM_ADDRS:
        offset = addr - RAM_BASE
        raw = guest_ram[offset:offset+4]
        words.append((addr, raw.hex(" "), int.from_bytes(raw, "little")))
    return sha(guest_ram), words, len(ram)

def excerpt(path: Path, dest: Path):
    lines = path.read_text(errors="replace").splitlines()
    if len(lines) <= 290:
        body = lines
    else:
        body = lines[:40] + ["[... middle omitted in excerpt; complete raw log is a sibling file; source lines=%d ...]" % len(lines)] + lines[-250:]
    dest.write_text("\n".join(body) + "\n", encoding="utf-8")

def tsv_line(values):
    return "\t".join(str(x).replace("\t", " ").replace("\n", "\\n") for x in values) + "\n"

def validate_header(header: bytes):
    text = header.decode("utf-8", errors="strict")
    flat = re.sub(r"\s+", " ", text)
    expected = [
      'TYPESTRING("save_state_info"), 1',
      'TYPESTRING("thumbnail"), 2',
      'TYPESTRING("memory"), 3',
      'TYPESTRING("registers"), 4',
      'TYPESTRING("gpu"), 5',
      'TYPESTRING("spu"), 6',
      'TYPESTRING("sio"), 7',
      'TYPESTRING("cdrom"), 8',
      'TYPESTRING("hardware"), 9',
      'TYPESTRING("counters"), 10',
      'TYPESTRING("mdec"), 11',
      'TYPESTRING("callstacks"), 14',
      'TYPESTRING("ram"), 1',
      'TYPESTRING("channel"), 6',
    ]
    missing = [needle for needle in expected if needle not in flat]
    if missing:
        raise ValueError("pinned source header did not match expected declarations: " + ", ".join(missing))
    return text

def classify(log_text: str, wrapper_rc: int):
    if re.search(r"(?:received|received signal|Program received|Program terminated with signal) SIGSEGV", log_text):
        return "SIGSEGV"
    if re.search(r"(?:received|received signal|Program received|Program terminated with signal) SIGABRT", log_text):
        return "SIGABRT"
    if "AE_POST_LOAD_VSYNC=180" in log_text and "AE_RAM_STATE_CAPTURE=PASS" in log_text:
        return "POST_LOAD_VSYNC=180"
    if wrapper_rc in (124, 137, 143):
        return "TIMEOUT_OR_KILLED"
    if "AE_LOAD_LUA_ERROR=" in log_text or "AE_STATE_OPEN_FAIL=" in log_text:
        return "RESTORE_SCRIPT_ERROR"
    return "INCONCLUSIVE"

def split_parts(items, n):
    size = (len(items) + n - 1) // n
    return [items[i:i+size] for i in range(0, len(items), size)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--control", required=True)
    ap.add_argument("--source-header", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--pcsx-bin", required=True)
    ap.add_argument("--appdir", required=True)
    ap.add_argument("--bios", required=True)
    ap.add_argument("--cue", required=True)
    ap.add_argument("--card", required=True)
    args = ap.parse_args()
    target_path, control_path = Path(args.target), Path(args.control)
    header_path, outroot, work = Path(args.source_header), Path(args.output), Path(args.work)
    rawroot, excerptroot = outroot / "raw", outroot / "excerpts"
    for d in (outroot, rawroot, excerptroot, work/"hybrids", work/"logs", work/"runtime"):
        d.mkdir(parents=True, exist_ok=True)
    target, control = target_path.read_bytes(), control_path.read_bytes()
    header = header_path.read_bytes()
    validate_header(header)
    # Run inside the pinned schema source checkout/blob, not the current upstream head.
    blob_sha_line = subprocess.run(["git", "hash-object", str(header_path)], capture_output=True, text=True)
    header_git_blob = blob_sha_line.stdout.strip() if blob_sha_line.returncode == 0 else "TIDAK_TAHU"
    htarget, hcontrol = sha(target), sha(control)
    if htarget != "00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d":
        raise ValueError("target input SHA mismatch: " + htarget)
    if hcontrol != "9eef83b1590773159b95180447aaa1f35139468b3ea51c7beec00bfb89f41492":
        raise ValueError("control input SHA mismatch: " + hcontrol)
    tr, cr = parse(target), parse(control)
    tg, cg = grouped(tr), grouped(cr)
    lines = []
    add = lines.append
    add("AE1-AE4 PROTOBUF AND RESTORE AUDIT — raw bytes, no controller input")
    add("Target: bytes=%d sha256=%s" % (len(target), htarget))
    add("Control: bytes=%d sha256=%s" % (len(control), hcontrol))
    add("PCSX source pin=%s; sstate.h git-blob-sha1=%s; sha256=%s" % (PIN, header_git_blob, sha(header)))
    add("Source: " + SOURCE_URL)
    add("Schema premise: top-level numbers/types are read from pinned sstate.h; byte sizes come from parsing exact raw states.")
    add("")
    add("AE1 TOP-LEVEL FIELD SIZE TABLE")
    add("number | name | pinned type | target count/wire/payload B/encoded B | control count/wire/payload B/encoded B | delta encoded bytes (T-C)")
    for n in sorted(set(tg) | set(cg) | set(TOP)):
        ts, cs = tg.get(n, []), cg.get(n, [])
        tn, typ = TOP.get(n, ("unknown_or_reserved", "TIDAK_TAHU"))
        tw = ",".join(str(x["wire"]) for x in ts) or "-"
        cw = ",".join(str(x["wire"]) for x in cs) or "-"
        tpay, cpay = sum(x["payload_len"] for x in ts), sum(x["payload_len"] for x in cs)
        tenc, cenc = sum(x["encoded_len"] for x in ts), sum(x["encoded_len"] for x in cs)
        add("%d | %s | %s | %d/%s/%d/%d | %d/%s/%d/%d | %+d" %
            (n, tn, typ, len(ts), tw, tpay, tenc, len(cs), cw, cpay, cenc, tenc-cenc))
    add("")
    add("AE1 FIELD 6 = SPU MESSAGE: SUBFIELD/OCCURRENCE COMPARISON")
    tspu, cspu = get_payload(target, 6), get_payload(control, 6)
    sr_t, sr_c = parse(tspu), parse(cspu)
    sg_t, sg_c = grouped(sr_t), grouped(sr_c)
    changed = child_diff_keys(tspu, cspu)
    add("SPU payload bytes: target=%d control=%d delta=%+d" % (len(tspu), len(cspu), len(tspu)-len(cspu)))
    add("child key | pinned name/type | target payload/encoded/SHA256 | control payload/encoded/SHA256 | encoded delta | changed")
    for n in sorted(set(sg_t) | set(sg_c) | set(SPU)):
        name, typ = SPU.get(n, ("unknown_or_reserved", "TIDAK_TAHU"))
        for i in range(max(len(sg_t.get(n, [])), len(sg_c.get(n, [])))):
            t = sg_t[n][i] if i < len(sg_t.get(n, [])) else None
            c = sg_c[n][i] if i < len(sg_c.get(n, [])) else None
            tp, cp = (t["payload_len"] if t else 0), (c["payload_len"] if c else 0)
            te, ce = (t["encoded_len"] if t else 0), (c["encoded_len"] if c else 0)
            th, ch = (sha(t["enc"]) if t else "-"), (sha(c["enc"]) if c else "-")
            add("spu.%s[%d] (field %d) | %s | %d/%d/%s | %d/%d/%s | %+d | %s" %
                (name, i+1, n, typ, tp, te, th, cp, ce, ch, te-ce, "YES" if (n,i) in changed else "no"))
    add("CHANGED_SPu_SUBFIELD_OCCURRENCES=%d" % len(changed))
    add("Changed keys (field_number, 1-based occurrence): " +
        (", ".join("%d#%d" % (n, i+1) for n,i in changed) if changed else "none"))
    full_rebuild = nested_replacements(cspu, tspu, changed)
    add("SUBFIELD_REPLACEMENT_ALL_DIFFS_RECONSTRUCTS_TARGET_SPU=" + str(full_rebuild == tspu))
    if full_rebuild != tspu:
        add("WARNING: child-occurrence hybrid serializer did not byte-reconstruct the target SPU payload; bisection conclusions are limited until serializer order is reconciled.")
    add("")
    add("SOURCE-MAPPED TOP-LEVEL TYPE DEFINITIONS")
    add("1 save_state_info: Message<SaveStateInfo>; 2 thumbnail: Message<Thumbnail>; 3 memory: Message<Memory>; 4 registers: Message<Registers>")
    add("5 gpu: Message<GPU>; 6 spu: Message<SPU>; 7 sio: Message<SIO>; 8 cdrom: Message<CDRom>; 9 hardware: Message<Hardware>")
    add("10 counters: Message<Counters>; 11 mdec: Message<MDEC>; 12 reserved; 13 pcdrv_files (repeated PCdrvFile); 14 callstacks: Message<CallStacks>")
    add("SPU field declarations: " + ", ".join("%d=%s:%s" % (n,*SPU[n]) for n in sorted(SPU)))
    (outroot/"ae1_static_field_sizes.txt").write_text("\n".join(lines)+"\n", encoding="utf-8")
    with (outroot/"ae1_field_sizes.tsv").open("w", encoding="utf-8") as f:
        f.write(tsv_line(["field","name","type","target_count","target_payload_bytes","target_encoded_bytes","control_count","control_payload_bytes","control_encoded_bytes","encoded_delta_target_minus_control"]))
        for n in sorted(set(tg)|set(cg)|set(TOP)):
            ts,cs=tg.get(n,[]),cg.get(n,[])
            nm,ty=TOP.get(n,("unknown_or_reserved","TIDAK_TAHU"))
            f.write(tsv_line([n,nm,ty,len(ts),sum(x["payload_len"] for x in ts),sum(x["encoded_len"] for x in ts),len(cs),sum(x["payload_len"] for x in cs),sum(x["encoded_len"] for x in cs),sum(x["encoded_len"] for x in ts)-sum(x["encoded_len"] for x in cs)]))
    with (outroot/"ae1_spu_subfields.tsv").open("w", encoding="utf-8") as f:
        f.write(tsv_line(["field","name","occurrence_1_based","type","target_payload_bytes","target_encoded_bytes","target_sha256","control_payload_bytes","control_encoded_bytes","control_sha256","encoded_delta_target_minus_control","changed"]))
        for n in sorted(set(sg_t)|set(sg_c)|set(SPU)):
            name,typ=SPU.get(n,("unknown_or_reserved","TIDAK_TAHU"))
            for i in range(max(len(sg_t.get(n,[])),len(sg_c.get(n,[])))):
                t=sg_t[n][i] if i<len(sg_t.get(n,[])) else None; c=sg_c[n][i] if i<len(sg_c.get(n,[])) else None
                f.write(tsv_line([n,name,i+1,typ,t["payload_len"] if t else 0,t["encoded_len"] if t else 0,sha(t["enc"]) if t else "-",c["payload_len"] if c else 0,c["encoded_len"] if c else 0,sha(c["enc"]) if c else "-", (t["encoded_len"] if t else 0)-(c["encoded_len"] if c else 0), "YES" if (n,i) in changed else "no"]))
    # Top-level reference proof: the current schema says field 6 is SPU; runtime tests below use no pads/buttons.
    (outroot/"source-schema-verification.txt").write_text(
        "PCSX-Redux pin: "+PIN+"\nURL: "+SOURCE_URL+"\nsstate.h expected Git blob SHA-1: "+HEADER_GIT_BLOB_SHA1+
        "\nObserved Git blob SHA-1: "+header_git_blob+"\nsstate.h SHA-256: "+sha(header)+
        "\nSource declarations verified: save_state_info=1, thumbnail=2, memory=3, registers=4, gpu=5, spu=6, sio=7, cdrom=8, hardware=9, counters=10, mdec=11, PCdrvFiles=13, callstacks=14; SPU channel=6 repeated Channel.\n",
        encoding="utf-8")
    # RAM snapshots are produced only when the emulator itself reaches post-load VSync 180.
    pad_setup = work/"pad-setup.lua"
    if not pad_setup.exists():
        pad_setup.write_text("PCSX.settings.pads[1].DeviceType = 'Analog'\nPCSX.settings.pads[1].Connected = true\nPCSX.SIO0.slots[1].pads[1].map()\nprint('AE_NO_INPUT_CONTROLLER=1; no button overrides')\n", encoding="utf-8")
    restore_lua = work/"ae-restore.lua"
    restore_lua.write_text(r'''
if io.stdout then io.stdout:setvbuf("no") end
local vsync, started, loaded, after, pending = 0, false, false, 0, false
local function log(s) print(s); pcall(function() io.stdout:flush() end) end
_G.aeLoaded = PCSX.Events.createEventListener("ExecutionFlow::SaveStateLoaded", function()
  loaded = true; after = 0; log("AE_EVENT_SAVE_STATE_LOADED=1")
end)
local function save_ram_checkpoint()
  local ok, err = pcall(function()
    local state = PCSX.createSaveState()
    local file = assert(Support.File.open("runtime/current.sstate", "TRUNCATE"), "cannot create temporary RAM checkpoint")
    file:writeMoveSlice(state); file:close()
  end)
  if ok then log("AE_RAM_STATE_CAPTURE=PASS")
  else log("AE_RAM_STATE_CAPTURE=FAIL detail="..tostring(err)) end
  PCSX.nextTick(function() PCSX.quit(ok and 0 or 62) end)
end
_G.aeVsync = PCSX.Events.createEventListener("GPU::Vsync", function()
  vsync = vsync + 1
  if not started then
    started = true
    local path = os.getenv("AE_TEST_STATE") or "resume/case.sstate"
    log("AE_LOAD_BEGIN=1 path="..path.." vsync="..vsync.." controller=NONE")
    PCSX.pauseEmulator()
    PCSX.nextTick(function()
      local open_ok, file = pcall(function() return assert(Support.File.open(path), "state open failed") end)
      if not open_ok or not file then log("AE_STATE_OPEN_FAIL="..tostring(file)); PCSX.quit(50); return end
      local load_ok, err = pcall(function() PCSX.loadSaveState(file) end)
      file:close()
      if not load_ok then log("AE_LOAD_LUA_ERROR="..tostring(err)); PCSX.quit(51); return end
      log("AE_LOAD_CALL_RETURNED=1"); PCSX.resumeEmulator()
    end)
    return
  end
  if loaded then
    after = after + 1
    if after >= 180 and not pending then
      pending = true; log("AE_POST_LOAD_VSYNC=180")
      PCSX.pauseEmulator(); PCSX.nextTick(save_ram_checkpoint)
    end
  elseif vsync >= 900 then
    log("AE_LOAD_EVENT_TIMEOUT=1"); PCSX.pauseEmulator()
    PCSX.nextTick(function() PCSX.quit(53) end)
  end
end)
log("AE_RESTORE_PROBE_READY_NO_INPUT=1")
'''.lstrip(), encoding="utf-8")
    appdir = Path(args.appdir)
    envbase = os.environ.copy()
    envbase.update({
      "DISPLAY": ":99",
      "HOME": str(work/"home"),
      "XDG_CONFIG_HOME": str(work/"home/.config"),
      "XDG_DATA_HOME": str(work/"home/.local/share"),
      "XDG_RUNTIME_DIR": str(work/"home/runtime"),
      "LIBGL_ALWAYS_SOFTWARE": "1",
      "LD_LIBRARY_PATH": str(appdir/"usr/lib")+":"+str(appdir/"usr/lib/x86_64-linux-gnu"),
      "QT_PLUGIN_PATH": str(appdir/"usr/plugins"),
      "QT_QPA_PLATFORM_PLUGIN_PATH": str(appdir/"usr/plugins/platforms"),
      "QML2_IMPORT_PATH": str(appdir/"usr/qml"),
    })
    for d in (work/"home/.config", work/"home/.local/share", work/"home/runtime"):
        d.mkdir(parents=True, exist_ok=True)
    try:
        (work/"home/runtime").chmod(0o700)
    except OSError:
        pass
    flags = "-noupdate -no-debugger -no-gdb -softgpu -dynarec -stdout -lua_stdout"
    metadata = [
      "AE1-AE4 runtime metadata", "runner_os="+subprocess.run(["bash","-lc","grep '^PRETTY_NAME=' /etc/os-release | cut -d= -f2-"],capture_output=True,text=True).stdout.strip().strip('"'),
      "gdb_version="+subprocess.run(["gdb","--version"],capture_output=True,text=True).stdout.splitlines()[0],
      "PCSX_BIN="+args.pcsx_bin, "PCSX_SOURCE_PIN="+PIN,
      "AppImage_SHA256=c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c",
      "flags="+flags, "controller=NONE; no button overrides; Xvfb display=:99",
      "per_attempt_timeout_seconds=18; post-load gate=180 VSync; no screenshots; RAM only hashed and words reported",
      "target_producer_run=39262213468/job=118092519254",
      "control_producer_run=39867730674/job=120134061270; container_digest=sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4",
    ]
    (outroot/"ae3_runtime_environment.txt").write_text("\n".join(metadata)+"\n", encoding="utf-8")
    result_rows = []
    case_summaries = []
    ram_rows = []
    tested_cache = {}
    testcase_counter = 0

    def run_case(case_name: str, state_bytes: bytes, target_keys=(), description=""):
        nonlocal testcase_counter
        testcase_counter += 1
        state_path = work/"resume"/(case_name+".sstate")
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_bytes(state_bytes)
        state_hash = sha(state_bytes)
        outcomes, pcs = [], []
        for attempt in (1,2):
            label = "%s-attempt%d" % (case_name, attempt)
            gdb_log = rawroot/(label+".gdb.txt")
            pcsx_work = work/"logs"/(label+".pcsx.txt")
            runtime_state = work/"runtime/current.sstate"
            for p in (runtime_state, pcsx_work, gdb_log):
                try: p.unlink()
                except FileNotFoundError: pass
            commands = work/"ae-gdb.commands"
            commands.write_text("""set pagination off
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
        try:
            gdb.execute(command)
        except Exception as exc:
            print('AE_GDB_COMMAND_UNAVAILABLE: ' + command + ' :: ' + str(exc))
        print('AE_GDB_COMMAND_END: ' + command)
    print('AE_GDB_CONTEXT_END')
    try:
        gdb.execute('continue')
    except Exception as exc:
        print('AE_GDB_FINAL_CONTINUE_RESULT: ' + str(exc))
else:
    print('AE_GDB_CONTEXT_STATUS=NOT_APPLICABLE; inferior exited before post-run context')
end
""", encoding="utf-8")
            testenv = envbase.copy()
            testenv["AE_TEST_STATE"] = "resume/"+state_path.name
            timeout_cmd = ["timeout","--signal=INT","--kill-after=5s","18s",
              "gdb","--quiet","--nx","--batch","--return-child-result","-x",str(commands),
              "--args",args.pcsx_bin,
              "-noupdate","-no-debugger","-no-gdb","-bios",args.bios,"-iso",args.cue,
              "-memcard1",args.card,"-exec",pad_setup.read_text(encoding="utf-8"),
              "-dofile",str(restore_lua),"-softgpu","-dynarec","-stdout","-lua_stdout",
              "-logfile",str(pcsx_work),"-run"]
            start_time = time.time()
            try:
                with gdb_log.open("wb") as out:
                    proc = subprocess.run(timeout_cmd, cwd=work, env=testenv, stdout=out, stderr=subprocess.STDOUT, check=False)
                wrapper_rc = proc.returncode
            except Exception as exc:
                wrapper_rc = 255
                gdb_log.write_text("AE_LAUNCH_EXCEPTION="+repr(exc)+"\n", encoding="utf-8")
            if not pcsx_work.exists():
                pcsx_work.write_text("AE_PCXS_LOG_NOT_CREATED; inspect complete GDB log\n", encoding="utf-8")
            logtext = gdb_log.read_text(errors="replace")
            status = classify(logtext, wrapper_rc)
            sigmatch = re.search(r"(?:Thread \d+ .* received signal|Program received signal|Program terminated with signal) (SIG[A-Z0-9]+)", logtext)
            signal = sigmatch.group(1) if sigmatch else ("NONE" if status=="POST_LOAD_VSYNC=180" else "TIDAK_TAHU")
            pcmatch = re.search(r"(?:=>\s*)?(0x[0-9a-fA-F]+):\s+\w", logtext)
            pc = pcmatch.group(1) if pcmatch else ("NOT_APPLICABLE_NORMAL_EXIT" if status=="POST_LOAD_VSYNC=180" else "TIDAK_TAHU")
            exit_code = "0" if status=="POST_LOAD_VSYNC=180" else ("139 (SIGSEGV)" if status=="SIGSEGV" else ("134 (SIGABRT)" if status=="SIGABRT" else ("TIMEOUT" if wrapper_rc in (124,137,143) else "TIDAK_TAHU; wrapper_rc=%d"%wrapper_rc)))
            ramsha, wordfield, ram_storage_len = "-", "-", 0
            if status=="POST_LOAD_VSYNC=180" and runtime_state.exists():
                try:
                    ramsha, words, ram_storage_len = ram_info(runtime_state.read_bytes())
                    wordfield = "; ".join("0x%08X bytes=%s LE32=0x%08X" % (addr, raw, val) for addr,raw,val in words)
                    ram_rows.append([case_name,attempt,state_hash,ramsha,ram_storage_len,wordfield])
                except Exception as exc:
                    wordfield = "RAM_PARSE_ERROR="+repr(exc)
                finally:
                    try: runtime_state.unlink()
                    except OSError: pass
            else:
                try: runtime_state.unlink()
                except OSError: pass
            duration = "%.3f" % (time.time()-start_time)
            result_rows.append([case_name,attempt,state_hash,status,signal,pc,wrapper_rc,exit_code,
              "YES" if "AE_POST_LOAD_VSYNC=180" in logtext else "no",
              ramsha,ram_storage_len,wordfield,str(gdb_log.relative_to(outroot)),str(pcsx_work),duration])
            for p in (gdb_log, pcsx_work):
                excerpt(p, excerptroot/(p.name+".first40-last250.txt"))
            outcomes.append(status)
            pcs.append(pc)
        if outcomes == ["SIGSEGV","SIGSEGV"] and pcs[0]==pcs[1]:
            combined = "SIGSEGV_BOTH"
        elif outcomes == ["POST_LOAD_VSYNC=180","POST_LOAD_VSYNC=180"]:
            combined = "POST_LOAD_VSYNC_180_BOTH"
        elif outcomes[0] == outcomes[1]:
            combined = outcomes[0] + "_BOTH"
        else:
            combined = "MIXED_OR_INCONCLUSIVE"
        case_summaries.append([case_name, combined, ";".join(outcomes), ";".join(pcs), state_hash, description])
        return combined

    # Run exact AD3 field6 sufficiency hybrid again under this single pinned headless harness.
    full_keys = set(changed)
    full_hybrid = replace_top_field(control, target, 6)
    if nested_replacements(cspu, tspu, full_keys) == tspu:
        # Same top-level state as replacing field6 raw, barring unrelated wire ordering.
        full_hybrid_nested = make_spu_hybrid(control, target, full_keys)
        if sha(full_hybrid_nested) != sha(full_hybrid):
            add("WARNING: nested all-diff hybrid differs bytewise from raw field-6 replacement; keeping raw full-field hybrid as reference.")
    full_outcome = run_case("ae1-spu-full-target-in-control", full_hybrid, full_keys,
                            "control state with target top-level field 6 (SPU) bytes; AD3 prior expected SIGSEGV x2")
    tested_cache[frozenset(full_keys)] = full_outcome

    def subset_test(keys):
        keyset = frozenset(keys)
        if not keyset:
            return "EMPTY_SUBSET_NOT_RUN"
        if keyset in tested_cache:
            return tested_cache[keyset]
        signature = hashlib.sha256("|".join("%d:%d"%(n,i) for n,i in sorted(keyset)).encode()).hexdigest()[:10]
        name = "ae1-spu-subset-"+signature
        state = make_spu_hybrid(control, target, keyset)
        outcome = run_case(name, state, keyset,
                           "control base; target SPU subfield occurrences selected: "+",".join("%d#%d"%(n,i+1) for n,i in sorted(keyset)))
        tested_cache[keyset] = outcome
        return outcome

    # Exhaustive singleton tests directly establish whether any one SPU field occurrence
    # is independently sufficient; every case has two separate emulator launches.
    singleton_crashes = []
    for key in changed:
        out = subset_test({key})
        if out == "SIGSEGV_BOTH":
            singleton_crashes.append(key)
    # Delta debugging identifies a 1-minimal multi-field combination, if no singleton suffices.
    current = list(singleton_crashes[:1]) if singleton_crashes else list(changed)
    if singleton_crashes:
        min_outcome = subset_test(set(current))
    else:
        n = 2
        while len(current) >= 2:
            chunks = split_parts(current, min(n, len(current)))
            reduced = False
            for chunk in chunks:
                out = subset_test(set(chunk))
                if out == "SIGSEGV_BOTH":
                    current = list(chunk); n = max(2,n-1); reduced = True; break
            if reduced:
                continue
            for chunk in chunks:
                cset = set(chunk)
                complement = [item for item in current if item not in cset]
                if complement and len(complement) < len(current):
                    out = subset_test(set(complement))
                    if out == "SIGSEGV_BOTH":
                        current = complement; n = max(2,n-1); reduced = True; break
            if reduced:
                continue
            if n >= len(current):
                break
            n = min(len(current), n*2)
        min_outcome = subset_test(set(current)) if current else "NO_CHANGED_SUBFIELDS"
    min_keys = set(current)
    min_name = "ae1-spu-minimal-"+hashlib.sha256("|".join("%d:%d"%(n,i) for n,i in sorted(min_keys)).encode()).hexdigest()[:10]
    # Ensure the named minimal case exists even if the selected set is cached under a previous label.
    if min_keys:
        outcome_cached = tested_cache.get(frozenset(min_keys))
        if outcome_cached != "SIGSEGV_BOTH":
            min_outcome = subset_test(min_keys)
            outcome_cached = min_outcome
        # Alias is not a new run; runtime results already include the actual hashed case name.
    else:
        outcome_cached = "NO_CHANGED_SUBFIELDS"

    # AE2 necessity tests: target baseline with all of field 6 from control, then minimal
    # SPU occurrence(s) changed from target to control. No button is pressed.
    target_spu_control = replace_top_field(target, control, 6)
    reverse_field_outcome = run_case("ae2-target-spu-field6-control", target_spu_control, (),
                                     "target base with entire top-level field 6 from control")
    reverse_min_state = make_spu_hybrid(target, control, min_keys)
    reverse_min_outcome = run_case("ae2-target-minimal-spu-subfields-control", reverse_min_state, (),
                                   "target base with minimum crash-causing SPU subfield occurrence set replaced from control")

    # Write complete output records and SHA manifest. Complete .gdb/.pcsx files remain untruncated;
    # excerpts are additional first-40/last-250 line views.
    with (outroot/"runtime-results.tsv").open("w", encoding="utf-8") as f:
        f.write(tsv_line(["case","attempt","hybrid_state_sha256","result","signal","pc_or_status","gdb_wrapper_exit","emulator_exit_code","post_load_vsync_180","ram_2mib_sha256","ram_field_storage_bytes","raw_words_at_frame","gdb_log","pcsx_log","seconds"]))
        for row in result_rows: f.write(tsv_line(row))
    with (outroot/"runtime-case-summary.tsv").open("w", encoding="utf-8") as f:
        f.write(tsv_line(["case","two_launch_outcome","attempt_outcomes","PC_or_status_each","hybrid_state_sha256","definition"]))
        for row in case_summaries: f.write(tsv_line(row))
    with (outroot/"ae4_ram_snapshots.tsv").open("w", encoding="utf-8") as f:
        f.write(tsv_line(["case","attempt","hybrid_state_sha256","RAM_2MiB_sha256","serialized_RAM_field_bytes_not_dumped","raw_4_bytes_and_LE32_at_addresses"]))
        for row in ram_rows: f.write(tsv_line(row))
    # Hash the original unmodified state inputs, every full new log, and the metadata text.
    manifest = []
    for p in sorted(rawroot.glob("*")):
        if p.is_file():
            manifest.append("%s  %s  bytes=%d" % (sha(p.read_bytes()), p.relative_to(outroot), p.stat().st_size))
    (outroot/"ae1-ae4-log-sha256.txt").write_text("\n".join(manifest)+"\n", encoding="utf-8")

    report = []
    radd = report.append
    radd("AE1–AE4 RESULT SUMMARY")
    radd("Target state SHA-256: "+htarget+" (21,163,286 B); control: "+hcontrol+" (21,162,546 B).")
    radd("Pinned source header: "+SOURCE_URL+"; sstate.h Git blob SHA-1 observed="+header_git_blob+"; file SHA-256="+sha(header)+".")
    radd("AE1 field table: ae1_field_sizes.tsv; nested field-6/SPU table: ae1_spu_subfields.tsv; full schema report: ae1_static_field_sizes.txt.")
    radd("Field 6/SPU byte delta (target-control): %+d bytes." % (len(tspu)-len(cspu)))
    radd("Number of changed SPU (field, occurrence) items: %d." % len(changed))
    radd("Byte-reconstruction of target SPU using all changed occurrence items: %s." % ("PASS" if full_rebuild==tspu else "FAIL; nested bisection interpretation limited"))
    radd("Full field-6 target→control hybrid two-launch result: %s (case ae1-spu-full-target-in-control)." % full_outcome)
    radd("Singleton SPU subfields independently causing SIGSEGV twice: "+(", ".join("field%d occurrence %d"%(n,i+1) for n,i in singleton_crashes) if singleton_crashes else "NONE in tested set"))
    radd("Minimal DD-minimised target-SPU subfield set on control base: "+(", ".join("field%d occurrence %d"%(n,i+1) for n,i in sorted(min_keys)) if min_keys else "TIDAK TAHU / no changed keys"))
    radd("Minimal set test status: "+str(outcome_cached)+"; this is 1-minimal under the tested occurrence-level delta-debug procedure.")
    if not singleton_crashes:
        radd("Interpretation: TIDAK ADA SUB-FIELD CUKUP SENDIRIAN (each changed SPU occurrence singleton was tested in two independent launches); the reported minimal sufficient object is a combination if it reproduces SIGSEGV twice.")
    else:
        radd("Interpretation: at least one singleton SPU occurrence is sufficient in the tested control-base context.")
    radd("AE2 target + field 6/SPU from control: "+reverse_field_outcome+" (two launches).")
    radd("AE2 target + minimal SPU occurrence set from control: "+reverse_min_outcome+" (two launches).")
    radd("Necessity scope: only these exact hybrids/build/state are assessed; no universal necessity claim.")
    radd("AE3 producer target run 39262213468/job 118092519254: Ubuntu 26.04; AppImage SHA c04b3e0a592abbb38bac34fb75551694aaf3a7d4ff18e9fc7b8e2c05bd60fc0c; source pin 0c3572c3d; flags -noupdate -no-debugger -no-gdb -softgpu -dynarec -stdout -lua_stdout; target was restored twice with SIGSEGV in AD1/AD4 and this run reuses that exact verified AppImage.")
    radd("AE3 control producer run 39867730674/job 120134061270: Ubuntu 24.04.5 host + ghcr.io/grumpycoders/pcsx-redux-build:latest container digest sha256:d9ae6cbb23a5d0d98d8c3702cc6f512698ee1670bf8d59b236b2baabe99a66e4; patched AppImage SHA 2fb33f631bfd197654d6f4c2dc89b95c4388e68dd1e77ca25a55a80a7035ba99; flags -softgpu -dynarec -stdout -lua_stdout; GDB version in the container remains TIDAK TAHU.")
    radd("RAM evidence rule: ae4_ram_snapshots.tsv reports SHA-256 of exactly the first 2,097,152 bytes of Memory.ram (PS1 2 MiB RAM) plus 4-byte raw memory order and LE32 words at requested addresses for each successful post-load VSync 180 checkpoint. Serialized RAM is 8 MiB; only its first 2 MiB is hashed. No RAM dump/checkpoint is copied to output.")
    radd("AE4 qualifying successful snapshots counted: %d attempts; unique 2MiB RAM hashes: %d." % (len(ram_rows), len(set(r[3] for r in ram_rows if r[3] != "-"))))
    radd("Raw full GDB/PCSX logs: raw/; supplementary excerpts: excerpts/; SHA-256 manifest: ae1-ae4-log-sha256.txt.")
    radd("No ISO, BIOS, savestate, RAM dump, or screenshot is written under reports/. Story Mode completion is not assessed or claimed.")
    (outroot/"AE1_AE4_RESULTS.txt").write_text("\n".join(report)+"\n", encoding="utf-8")
    print((outroot/"AE1_AE4_RESULTS.txt").read_text(encoding="utf-8"))
    print("AE1_AE4_SUMMARY_RUNS=%d CASES=%d RAM_SNAPSHOTS=%d" % (len(result_rows), len(case_summaries), len(ram_rows)))
    # Fail the job only if evidence integrity/parser/source checks failed; experimental crashes are observations.
    if full_rebuild != tspu:
        print("AE_SUBFIELD_RECONSTRUCTION_WARNING=1; interpret bisection cautiously")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
