#!/usr/bin/env python3
"""AQ2: two no-input H6 hybrid frame-180 RAM inspections; never publish raw memory."""
import argparse, csv, hashlib, os, re, shutil, subprocess, time
from collections import Counter
from pathlib import Path

from experiments.aj2_h6_ram_probe import (
    TARGET_SHA, CONTROL_SHA, H6_EXPECTED_SHA, one, replace_top, encmsg, write_lua
)

RAM_BASE = 0x80000000
RAM_SIZE = 0x200000
RECORD_ARRAY_SLOT = 0x8013EA84
RECORD_COUNT_SLOT = 0x8013EAC8
STRIDE = 0x124
EXPECTED_RAM_SHA = "4c964aaca0afccc68317acd0726fec680c305b903cd426e70afe3d8ac1f1e741"
MULTIPLIERS = {0: (1,1), 1: (12,10), 2: (15,10), 3: (18,10), 4: (2,1)}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_u8(buf, address):
    off = address - RAM_BASE
    if off < 0 or off >= len(buf):
        raise ValueError("address outside first 2 MiB: " + hex(address))
    return buf[off]

def read_u16(buf, address):
    off = address - RAM_BASE
    if off < 0 or off + 2 > len(buf):
        raise ValueError("halfword outside first 2 MiB: " + hex(address))
    return int.from_bytes(buf[off:off+2], "little")

def read_u32(buf, address):
    off = address - RAM_BASE
    if off < 0 or off + 4 > len(buf):
        raise ValueError("word outside first 2 MiB: " + hex(address))
    return int.from_bytes(buf[off:off+4], "little")

def recompute(base, selector):
    ratio = MULTIPLIERS.get(selector)
    return 0 if ratio is None else (base * ratio[0]) // ratio[1]

def record_rows(ram, attempt, ram_sha):
    pointer = read_u32(ram, RECORD_ARRAY_SLOT)
    count = read_u32(ram, RECORD_COUNT_SLOT)
    meta = {
        "record_type": "HEADER", "attempt": attempt, "ram_first_2mib_sha256": ram_sha,
        "tile_array_pointer_0x8013EA84": f"0x{pointer:08X}",
        "tile_record_count_0x8013EAC8": str(count),
        "record_stride": f"0x{STRIDE:X}", "validation": "PASS"
    }
    if count == 0:
        meta["validation"] = "COUNT_ZERO"
        return [meta], pointer, count, Counter()
    start = pointer - RAM_BASE
    if pointer < RAM_BASE or start >= len(ram) or start + count * STRIDE > len(ram):
        meta["validation"] = "POINTER_OR_COUNT_OUTSIDE_RAM"
        return [meta], pointer, count, Counter()
    rows = [meta]
    dist = Counter()
    offsets = list(range(0x10, 0x30, 2))
    for index in range(count):
        addr = pointer + index * STRIDE
        selector = read_u8(ram, addr + 0x0B)
        plus00 = read_u8(ram, addr)
        half20 = read_u16(ram, addr + 0x20)
        selected_off = (half20 >> 7) & 0x1E
        selected_b = read_u16(ram, addr + 0x10 + selected_off)
        vals = {off: read_u16(ram, addr + off) for off in offsets}
        row = {
            "record_type": "RECORD", "attempt": attempt,
            "ram_first_2mib_sha256": ram_sha,
            "tile_array_pointer_0x8013EA84": f"0x{pointer:08X}",
            "tile_record_count_0x8013EAC8": str(count),
            "record_index": str(index), "record_address": f"0x{addr:08X}",
            "plus_00_u8": str(plus00), "plus_0B_u8": str(selector),
            "plus_20_u16": str(half20), "selected_B_offset": f"+0x{0x10 + selected_off:02X}",
            "selected_B_u16": str(selected_b),
            "FUN_800B770C_recomputed": str(recompute(selected_b, selector)),
            "validation": "PASS"
        }
        for off, value in vals.items():
            row[f"plus_{off:02X}_u16"] = str(value)
        rows.append(row)
        dist[str(selector)] += 1
    return rows, pointer, count, dist

def main():
    ap = argparse.ArgumentParser()
    for arg in ("target", "control", "pcsx-bin", "appdir", "bios", "cue", "card", "work", "out"):
        ap.add_argument("--" + arg, required=True)
    a = ap.parse_args()
    target_path, control_path = Path(a.target), Path(a.control)
    target, control = target_path.read_bytes(), control_path.read_bytes()
    if sha(target) != TARGET_SHA:
        raise SystemExit("TARGET_SAVESTATE_SHA_MISMATCH")
    if sha(control) != CONTROL_SHA:
        raise SystemExit("CONTROL_SAVESTATE_SHA_MISMATCH")
    hybrid = replace_top(target, 6, encmsg(6, one(control, 6)))
    hybrid_sha = sha(hybrid)
    if hybrid_sha != H6_EXPECTED_SHA:
        raise SystemExit("H6_HYBRID_SHA_MISMATCH actual=" + hybrid_sha)

    work, out = Path(a.work), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name in ("resume", "runtime", "logs", "dumps", "launches", "home"):
        (work/name).mkdir(parents=True, exist_ok=True)
    h6_path = work / "resume" / "h6-hybrid.sstate"
    h6_path.write_bytes(hybrid)
    lua_path = work / "h6-no-input.lua"
    write_lua(lua_path)
    appdir = Path(a.appdir)
    baseline_card = Path(a.card)
    card_sha = sha(baseline_card.read_bytes())
    if card_sha != "ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5":
        raise SystemExit("REFERENCE_MEMORY_CARD_SHA_MISMATCH")
    pad_text = (
        "PCSX.settings.pads[1].DeviceType = 'Analog'\n"
        "PCSX.settings.pads[1].Connected = true\n"
        "PCSX.SIO0.slots[1].pads[1].map()\n"
        "print('AQ2_CONTROLLER_READY_NO_GAMEPLAY_INPUT=1')\n"
    )
    env_base = os.environ.copy()
    home = work / "home"
    for d in (home / ".config", home / ".data", home / "runtime"):
        d.mkdir(parents=True, exist_ok=True)
    env_base.update({
        "DISPLAY": ":99", "HOME": str(home),
        "XDG_CONFIG_HOME": str(home / ".config"),
        "XDG_DATA_HOME": str(home / ".data"),
        "XDG_RUNTIME_DIR": str(home / "runtime"),
        "LIBGL_ALWAYS_SOFTWARE": "1",
        "LD_LIBRARY_PATH": str(appdir / "usr/lib") + ":" + str(appdir / "usr/lib/x86_64-linux-gnu"),
        "QT_PLUGIN_PATH": str(appdir / "usr/plugins"),
        "QT_QPA_PLATFORM_PLUGIN_PATH": str(appdir / "usr/plugins/platforms"),
        "QML2_IMPORT_PATH": str(appdir / "usr/qml"),
    })

    attempts = []
    all_rows = []
    distributions = {}
    for attempt in (1, 2):
        launch = work / "launches" / f"attempt-{attempt}"
        runtime = launch / "runtime"
        logs = launch / "logs"
        home_i = launch / "home"
        for d in (runtime, logs, home_i / ".config", home_i / ".data", home_i / "runtime"):
            d.mkdir(parents=True, exist_ok=True)
        card = launch / "memory-card.mcd"
        shutil.copyfile(baseline_card, card)
        card_before = sha(card.read_bytes())
        state_path = runtime / "h6-current.sstate"
        if state_path.exists():
            state_path.unlink()
        pad = launch / "pad.lua"
        pad.write_text(pad_text, encoding="utf-8")
        gdb_log = logs / "pcsx-gdb.txt"
        pcsx_log = logs / "pcsx.txt"
        gdb_commands = launch / "gdb.commands"
        gdb_commands.write_text("""set pagination off
set confirm off
set print thread-events off
handle SIGSEGV stop print nopass
handle SIGABRT stop print nopass
run
python
import gdb
inf=gdb.selected_inferior()
if getattr(inf,'pid',0):
 print('AQ2_GDB_CONTEXT_BEGIN')
 for c in ('info threads','x/3i $pc','info registers','bt','thread apply all bt 12'):
  try:gdb.execute(c)
  except Exception as e:print('AQ2_GDB_COMMAND_ERROR '+str(e))
 print('AQ2_GDB_CONTEXT_END')
 try:gdb.execute('continue')
 except Exception as e:print('AQ2_GDB_CONTINUE '+str(e))
else: print('AQ2_GDB_INFERIOR_ALREADY_EXITED')
end
""", encoding="utf-8")
        run_env = env_base.copy()
        run_env.update({
            "HOME": str(home_i), "XDG_CONFIG_HOME": str(home_i / ".config"),
            "XDG_DATA_HOME": str(home_i / ".data"), "XDG_RUNTIME_DIR": str(home_i / "runtime"),
            "AJ_H6_STATE": str(h6_path), "AE_RUN_START_EPOCH": str(time.time()),
        })
        command = [
            "timeout", "--signal=INT", "--kill-after=5s", "600s",
            "gdb", "--quiet", "--nx", "--batch", "--return-child-result",
            "-x", str(gdb_commands), "--args", a.pcsx_bin,
            "-noupdate", "-no-debugger", "-no-gdb",
            "-bios", a.bios, "-iso", a.cue, "-memcard1", str(card),
            "-exec", pad_text, "-dofile", str(lua_path),
            "-softgpu", "-dynarec", "-stdout", "-lua_stdout",
            "-logfile", str(pcsx_log), "-run",
        ]
        started = time.monotonic()
        with gdb_log.open("wb") as f:
            try:
                proc = subprocess.run(command, cwd=launch, env=run_env, stdout=f, stderr=subprocess.STDOUT, check=False)
                wrapper_exit = proc.returncode
            except Exception as exc:
                wrapper_exit = 255
                f.write(("AQ2_LAUNCH_EXCEPTION=" + repr(exc) + "\n").encode())
        wall = time.monotonic() - started
        log_text = gdb_log.read_text(encoding="utf-8", errors="replace")
        marker = re.search(r"AJ_H6_POST_LOAD_VSYNC=180 elapsed_since_launch_s=([0-9.]+)", log_text)
        capture_marker = "AJ_H6_RAM_CAPTURE=PASS" in log_text
        segv = bool(re.search(r"received signal SIGSEGV|Program received signal SIGSEGV|Program terminated with signal SIGSEGV", log_text))
        em = re.search(r"(?:Inferior\s+\d+.*?exited with code|Program exited with code)\s*[=:]?\s*(-?\d+)", log_text, re.I)
        emulator_exit = em.group(1) if em else ("0" if re.search(r"(?:Inferior\s+\d+.*?exited normally|Program exited normally)", log_text, re.I) else "TIDAK TAHU")
        card_after = sha(card.read_bytes()) if card.exists() else "TIDAK TAHU"
        outcome = "TIDAK ADA CAPTURE"
        ram_sha = "TIDAK TAHU"
        rows = []
        pointer = count = None
        dist = Counter()
        dump_path = work / "dumps" / f"attempt-{attempt}.ram2mib.bin"
        if marker and capture_marker and state_path.is_file() and not segv:
            try:
                state = state_path.read_bytes()
                ram_full = one(one(state, 3), 1)
                if len(ram_full) < RAM_SIZE:
                    raise ValueError("RAM segment shorter than 2 MiB")
                ram = ram_full[:RAM_SIZE]
                dump_path.write_bytes(ram)
                ram_sha = sha(dump_path.read_bytes())
                rows, pointer, count, dist = record_rows(ram, attempt, ram_sha)
                outcome = "PASS" if rows and rows[0].get("validation") == "PASS" else rows[0].get("validation", "PARSE_ERROR")
            except Exception as exc:
                outcome = "PARSE_ERROR:" + repr(exc)
            finally:
                try:
                    dump_path.unlink()
                except OSError:
                    pass
        elif segv:
            outcome = "SIGSEGV"
        elif marker and not state_path.is_file():
            outcome = "CAPTURE_MARKER_WITHOUT_STATE"
        all_rows.extend(rows)
        distributions[str(attempt)] = dict(sorted(dist.items(), key=lambda x: int(x[0])))
        attempts.append({
            "attempt": attempt, "outcome": outcome, "ram_sha": ram_sha,
            "pointer": f"0x{pointer:08X}" if pointer is not None else "TIDAK TAHU",
            "count": str(count) if count is not None else "TIDAK TAHU",
            "gdb_wrapper_exit": wrapper_exit, "emulator_exit": emulator_exit,
            "wall_s": f"{wall:.3f}", "post_load_to_180_s": marker.group(1) if marker else "TIDAK TAHU",
            "memory_card_before": card_before, "memory_card_after": card_after,
            "memory_card_unchanged": "YES" if card_before == card_after else "NO",
            "record_count_rows": max(0, len(rows)-1),
        })
        try:
            state_path.unlink()
        except OSError:
            pass

    columns = [
        "record_type", "attempt", "ram_first_2mib_sha256",
        "tile_array_pointer_0x8013EA84", "tile_record_count_0x8013EAC8",
        "record_index", "record_address", "plus_00_u8", "plus_0B_u8",
        "plus_20_u16", "selected_B_offset", "selected_B_u16",
        "FUN_800B770C_recomputed",
    ] + [f"plus_{off:02X}_u16" for off in range(0x10, 0x30, 2)] + ["record_stride", "validation"]
    tsv_path = out / "AQ2_H6_FRAME180_RECORDS.tsv"
    with tsv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)

    summary = [
        "AQ2 — H6 HYBRID, BUKAN TARGET MURNI",
        f"H6_SHA256={hybrid_sha}",
        f"TARGET_SOURCE_SHA256={TARGET_SHA} bytes={len(target)}",
        f"CONTROL_SOURCE_SHA256={CONTROL_SHA} bytes={len(control)}",
        "METHOD=two independent emulator launches; no gameplay input; capture after 180 post-load GPU VSync frames",
        "RAM_SHA_COVERAGE=first 2 MiB from 0x80000000",
        f"EXPECTED_AK1_AQ2_RAM_SHA256={EXPECTED_RAM_SHA}",
        "REFERENCE_VALUES_NOTE=60,100,50,150,580,2700 are comparison-only coincidences; not evidence for cost/income/release semantics",
    ]
    for r in attempts:
        summary.extend([
            "",
            f"ATTEMPT_{r['attempt']}_STATUS={r['outcome']}",
            f"ATTEMPT_{r['attempt']}_RAM_2MIB_SHA256={r['ram_sha']}",
            f"ATTEMPT_{r['attempt']}_RAM_SHA_MATCH_EXPECTED={'YES' if r['ram_sha']==EXPECTED_RAM_SHA else 'NO' if r['ram_sha']!='TIDAK TAHU' else 'TIDAK TAHU'}",
            f"ATTEMPT_{r['attempt']}_POINTER_0x8013EA84={r['pointer']}",
            f"ATTEMPT_{r['attempt']}_COUNT_0x8013EAC8={r['count']}",
            f"ATTEMPT_{r['attempt']}_PLUS_0B_DISTRIBUTION={distributions.get(str(r['attempt']),{})}",
            f"ATTEMPT_{r['attempt']}_RECORD_ROWS={r['record_count_rows']}",
            f"ATTEMPT_{r['attempt']}_GDB_WRAPPER_EXIT={r['gdb_wrapper_exit']}",
            f"ATTEMPT_{r['attempt']}_EMULATOR_EXIT={r['emulator_exit']}",
            f"ATTEMPT_{r['attempt']}_MEMCARD_UNCHANGED={r['memory_card_unchanged']}",
            f"ATTEMPT_{r['attempt']}_SECONDS_TO_FRAME180={r['post_load_to_180_s']}",
        ])
    hashes = [r["ram_sha"] for r in attempts]
    summary.append("")
    summary.append("TWO_LAUNCH_RAM_IDENTICAL=" + ("YES" if len(hashes)==2 and hashes[0]==hashes[1] and hashes[0]!="TIDAK TAHU" else "NO" if len(hashes)==2 else "TIDAK TAHU"))
    summary.append("TWO_LAUNCH_BOTH_EXPECTED_SHA=" + ("YES" if len(hashes)==2 and all(x==EXPECTED_RAM_SHA for x in hashes) else "NO" if all(x!="TIDAK TAHU" for x in hashes) else "TIDAK TAHU"))
    status = "PASS" if len(attempts)==2 and all(r["outcome"]=="PASS" and r["ram_sha"]==EXPECTED_RAM_SHA and r["memory_card_unchanged"]=="YES" for r in attempts) and len(hashes)==2 and hashes[0]==hashes[1] else "INCOMPLETE"
    summary.append(f"AQ2_STATUS={status}")
    (out / "AQ2_H6_SUMMARY.txt").write_text("\n".join(summary)+"\n", encoding="utf-8")
    (out / "AQ2_LAUNCHES.tsv").write_text(
        "attempt\tstatus\tram_sha256\tpointer\tcount\tgdb_wrapper_exit\temulator_exit\tcard_unchanged\twall_seconds\tseconds_to_frame180\n"+
        "".join("\t".join(str(r[k]) for k in ("attempt","outcome","ram_sha","pointer","count","gdb_wrapper_exit","emulator_exit","memory_card_unchanged","wall_s","post_load_to_180_s"))+"\n" for r in attempts),
        encoding="utf-8"
    )
    print("\n".join(summary))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
