#!/usr/bin/env python3
"""UM0: backward static value lineage for every UL0 stride-field store site."""
from __future__ import annotations
import argparse, csv, hashlib, re
from collections import Counter, defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.stage1.RunUL0 import decode, REGS  # read-only reuse of the proven decoder

ENTRY1_PC = 0x800AD450
ENTRY1_OFF = 0x10BB000
EXE_EXPECTED_SHA = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
DATA_EXPECTED_SHA = "69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
ENTRY1_EXPECTED_SHA = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
EXE_PC = 0x80010000
EXE_OFF = 0x800
STRIDE = 0x124
EXPECTED_WRITES = 224
CLASSES = ("IMMEDIATE", "RMW_OFFSET_SAMA_PLUS_KONSTANTA", "BACA_OFFSET_LAIN", "BACA_TABEL_STATIS", "PARAMETER_FUNGSI", "TAK_TERSELESAIKAN")
ACCESS = Path("reports/ui-audit-2026-11-12/ul/run-43192191539/attempt-1/UL0/UL0_OFFSET_ACCESS.tsv")
WINDOWS = Path("reports/ui-audit-2026-11-12/ul/run-43192191539/attempt-1/UL0/UL0_WINDOWS.tsv")
MATCHES = Path("reports/ui-audit-2026-11-12/ul/run-43192191539/attempt-1/UL0/UL0_MATCHES.tsv")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})


def map_pc(region: str, pc: int, exe: bytes, entry1: bytes) -> tuple[int, bytes]:
    if region == "ENTRY1":
        off = ENTRY1_OFF + (pc - ENTRY1_PC)
        ix = off - ENTRY1_OFF
        if ix < 0 or ix + 4 > len(entry1):
            raise ValueError(f"ENTRY1_PC_OUT_OF_RANGE 0x{pc:08X}")
        return off, entry1[ix:ix + 4]
    if region == "EXE":
        off = EXE_OFF + (pc - EXE_PC)
        if off < EXE_OFF or off + 4 > len(exe):
            raise ValueError(f"EXE_PC_OUT_OF_RANGE 0x{pc:08X}")
        return off, exe[off:off + 4]
    raise ValueError(f"UNKNOWN_REGION {region}")


def site_tokens(rows: list[dict[str, str]]) -> list[dict]:
    out = []
    for r in rows:
        offset = int(r["offset"], 16)
        for token in filter(None, (r.get("write_sites") or "").split(";")):
            m = re.fullmatch(r"(EXE|ENTRY1)@(0x[0-9A-Fa-f]+)/u(8|16|32)", token)
            if not m:
                raise ValueError(f"BAD_WRITE_SITE_TOKEN {token}")
            out.append({"offset": offset, "region": m.group(1), "pc": int(m.group(2), 16), "width": int(m.group(3)) // 8})
    return out


def is_memory(d: dict) -> bool:
    return d.get("mem") is not None


def is_read(d: dict) -> bool:
    return is_memory(d) and d["mem"][1] == "R"


def immediate_source(ins: list[dict], def_i: int, reg: int) -> tuple[bool, str]:
    d = ins[def_i]
    if d["op"] == 15 and d["rt"] == reg:
        return True, f"LUI_IMMEDIATE_0x{d['imm']:04X}"
    if d["op"] in (8, 9, 12, 13, 14) and d["rt"] == reg and d["rs"] == 0:
        return True, f"{d['text']}"
    if d["op"] in (9, 13) and d["rt"] == reg and def_i > 0:
        p = ins[def_i - 1]
        if p["op"] == 15 and p["rt"] == reg:
            return True, f"LUI+{d['text']}"
    return False, ""


def classify_source(ins: list[dict], store_i: int, store: dict, store_off: int) -> tuple[str, str, int | None]:
    src = store["rt"]
    lo = max(0, store_i - 23)
    def_i = None
    for j in range(store_i - 1, lo - 1, -1):
        if ins[j].get("writes") == src:
            def_i = j
            break
    if def_i is None:
        return "TAK_TERSELESAIKAN", f"no reaching definition for $\{REGS[src]} within {store_i-lo} prior instructions", None
    d = ins[def_i]
    is_imm, imm_ev = immediate_source(ins, def_i, src)
    if is_imm:
        return "IMMEDIATE", imm_ev, def_i
    if d["op"] in (8, 9) and d["rt"] == src and d["rs"] == src:
        const = d["simm"]
        for j in range(def_i - 1, lo - 1, -1):
            q = ins[j]
            if q.get("writes") == src:
                if is_read(q):
                    _, _, qimm, qrs, _ = q["mem"]
                    _, _, simm, srs, _ = store["mem"]
                    read_simm = qimm if qimm < 0x8000 else qimm - 0x10000
                    write_simm = simm if simm < 0x8000 else simm - 0x10000
                    if qrs == srs and read_simm == write_simm and read_simm == store_off:
                        sign = f"+0x{const:X}" if const >= 0 else f"-0x{-const:X}"
                        return "RMW_OFFSET_SAMA_PLUS_KONSTANTA", f"load/store same base+0x{store_off:X}; ADDIU {sign}", j
                    return "BACA_OFFSET_LAIN", f"load base=$\{REGS[qrs]} offset=0x{read_simm & 0xFFFFFFFF:X}; store offset=0x{store_off:X}", j
                break
    if is_read(d):
        _, _, imm, rs, rt = d["mem"]
        read_off = imm if imm < 0x8000 else imm - 0x10000
        _, _, store_imm, store_rs, _ = store["mem"]
        store_simm = store_imm if store_imm < 0x8000 else store_imm - 0x10000
        if rs != store_rs or read_off != store_simm:
            return "BACA_OFFSET_LAIN", f"direct load from base=$\{REGS[rs]} offset=0x{read_off & 0xFFFFFFFF:X}", def_i
        return "TAK_TERSELESAIKAN", "same-offset load found but no proven constant update", def_i
    return "TAK_TERSELESAIKAN", f"reaching definition {d['text']} not safely classifiable", def_i


def analyse(exe: bytes, data: bytes, access_rows: list[dict[str, str]], window_rows: list[dict[str, str]], match_rows: list[dict[str, str]]):
    if len(exe) != 385024 or hashlib.sha256(exe).hexdigest() != EXE_EXPECTED_SHA:
        raise ValueError("EXE_SIZE_OR_SHA256_MISMATCH")
    if len(data) != 66015232 or hashlib.sha256(data).hexdigest() != DATA_EXPECTED_SHA:
        raise ValueError("DATA_BIN_SIZE_OR_SHA256_MISMATCH")
    entry1 = data[ENTRY1_OFF:ENTRY1_OFF + 596412]
    if len(entry1) != 596412 or hashlib.sha256(entry1).hexdigest() != ENTRY1_EXPECTED_SHA:
        raise ValueError("ENTRY1_SLICE_SIZE_OR_SHA256_MISMATCH")
    sites = site_tokens(access_rows)
    expected_sum = sum(int(r["write_count"]) for r in access_rows)
    if expected_sum != EXPECTED_WRITES or len(sites) != expected_sum:
        raise ValueError(f"UL0_WRITE_COUNT_MISMATCH sum={expected_sum} tokens={len(sites)} expected={EXPECTED_WRITES}")
    winmap = {}
    for w in window_rows:
        if w.get("read_write") == "W":
            key = (w["region"], int(w["pc"], 16), int(w["access_offset"], 16))
            winmap[key] = w
    matchmap = {(m["region"], int(m["pc"], 16)): m for m in match_rows}
    trace_rows = []
    site_summaries = []
    for site_id, s in enumerate(sites, 1):
        pc = s["pc"]
        store_file_off, store_b = map_pc(s["region"], pc, exe, entry1)
        store = decode(store_b)
        if not store.get("mem") or store["mem"][1] != "W":
            raise ValueError(f"WRITE_SITE_NOT_STORE {s['region']} 0x{pc:08X} {store['text']}")
        _, _, imm, _, rt = store["mem"]
        store_imm = imm if imm < 0x8000 else imm - 0x10000
        if store_imm != s["offset"]:
            raise ValueError(f"WRITE_SITE_OFFSET_MISMATCH pc=0x{pc:08X} table=0x{s['offset']:03X} insn=0x{store_imm & 0xFFFFFFFF:X}")
        win = winmap.get((s["region"], pc, s["offset"]))
        mrow = matchmap.get((s["region"], int(win["match_pc"], 16))) if win else None
        ptr_origin = mrow.get("pointer_origin", "TIDAK TAHU") if mrow else "TIDAK TAHU"
        ptr_evidence = mrow.get("pointer_origin_evidence", "TIDAK TAHU") if mrow else "TIDAK TAHU"
        start_pc = max((ENTRY1_PC if s["region"] == "ENTRY1" else EXE_PC), pc - 23 * 4)
        decoded_window = []
        for curpc in range(start_pc, pc + 1, 4):
            off, raw = map_pc(s["region"], curpc, exe, entry1)
            decoded_window.append({"pc": curpc, "file_offset": off, "raw": raw, "ins": decode(raw)})
        store_i = len(decoded_window) - 1
        cls, class_evidence, def_i = classify_source([x["ins"] for x in decoded_window], store_i, store, s["offset"])
        for ix, item in enumerate(reversed(decoded_window)):
            orig_ix = store_i - ix
            role = "STORE_SITE" if orig_ix == store_i else "CONTEXT_BACKWARD"
            if orig_ix == def_i:
                role = "SOURCE_DEFINITION"
            if is_read(item["ins"]) and item["ins"].get("writes") == rt:
                role = "SOURCE_MEMORY_READ"
            if ptr_origin == "YA" and item["ins"]["op"] == 35 and item["ins"]["simm"] == -0x157C:
                role = "POINTER_EA84_LOAD_CANDIDATE"
            ins = item["ins"]
            trace_rows.append({
                "site_id": site_id, "region": s["region"], "written_offset": f"0x{s['offset']:03X}",
                "store_pc": f"0x{pc:08X}", "store_file_offset": f"0x{store_file_off:08X}",
                "source_class": cls, "source_evidence": class_evidence,
                "pointer_origin_EA84": ptr_origin, "pointer_origin_evidence": ptr_evidence,
                "pc": f"0x{item['pc']:08X}", "file_offset": f"0x{item['file_offset']:08X}",
                "bytes_4B": " ".join(f"{b:02X}" for b in item["raw"]),
                "instruction": ins["text"], "role": role,
            })
        site_summaries.append({"site_id": site_id, "offset": s["offset"], "pc": pc, "region": s["region"],
                               "file_offset": store_file_off, "source_class": cls, "source_evidence": class_evidence,
                               "pointer_origin": ptr_origin, "function": mrow.get("function", "TIDAK TAHU") if mrow else "TIDAK TAHU"})
    unique = {(x["region"], x["pc"], x["offset"]) for x in sites}
    if len(unique) != EXPECTED_WRITES:
        raise ValueError(f"WRITE_SITE_UNIQUENESS_FAIL {len(unique)}")
    if not any(x["pc"] == 0x800D5A1C and x["offset"] == 0x20 and x["region"] == "ENTRY1" and x["file_offset"] == 0x010E35CC for x in site_summaries):
        raise ValueError("REQUIRED_0x800D5A1C_OFFSET_0x20_MISSING_OR_BAD_FILE_OFFSET")
    byoff = defaultdict(list)
    for x in site_summaries:
        byoff[x["offset"]].append(x)
    summary_rows = []
    rmw_rows = []
    for off in sorted(byoff):
        entries = byoff[off]
        counts = Counter(x["source_class"] for x in entries)
        rmw = [x for x in entries if x["source_class"] == "RMW_OFFSET_SAMA_PLUS_KONSTANTA"]
        summary_rows.append({
            "offset": f"0x{off:03X}", "write_sites": len(entries),
            **{c: counts.get(c, 0) for c in CLASSES},
            "pcs": ";".join(f"{x['region']}@0x{x['pc']:08X}" for x in entries),
            "functions": ";".join(sorted(set(x["function"] for x in entries))) or "TIDAK TAHU",
        })
        for x in rmw:
            try:
                const = x["source_evidence"].split("ADDIU ", 1)[1].split(";", 1)[0]
                value = int(const.replace("+", "").replace("-", ""), 16)
                if value <= 0x20:
                    rmw_rows.append({"offset": f"0x{off:03X}", "pc": f"0x{x['pc']:08X}", "constant": const, "function": x["function"]})
            except (ValueError, IndexError):
                pass
    totals = Counter(x["source_class"] for x in site_summaries)
    summary = [
        "UM0_BACKWARD_STORE_VALUE_LINEAGE", "STATUS=TUNTAS", "EVIDENCE=K4 (verified raw bytes, exact MIPS decode, UL0 writer reconciliation); semantic meaning remains TIDAK TAHU",
        f"SOURCE_UL0_WRITES={len(sites)}", f"TRACE_SITES={len(site_summaries)}", f"TRACE_INSTRUCTION_ROWS={len(trace_rows)}",
        f"OFFSETS_WITH_WRITES={len(byoff)}", "EXPECTED_SPECIAL_SITE_0x800D5A1C_OFFSET_0x020=PASS file_offset=0x010E35CC",
        "EXE_PC_FILE_OFFSET=0x800+(PC-0x80010000)", "ENTRY1_PC_FILE_OFFSET=0x10BB000+(PC-0x800AD450)",
        f"EXE_SHA256={hashlib.sha256(exe).hexdigest()}", f"DATA_BIN_SHA256={hashlib.sha256(data).hexdigest()}", f"ENTRY1_SHA256={hashlib.sha256(entry1).hexdigest()}",
        "TRACE_ORDER=store first, then prior instructions in descending PC order; max 24 aligned instructions per site",
        "POINTER_ORIGIN=carried from UL0_MATCHES/UL0_WINDOWS; no new semantic interpretation",
        "FUNCTION_NAMES=TIDAK TAHU unless supplied by UL0 function mapping", "FIELD_MEANINGS=TIDAK TAHU",
        *[f"CLASS_{c}={totals.get(c, 0)}" for c in CLASSES],
        f"SMALL_CONSTANT_RMW_ROWS={len(rmw_rows)}", "SMALL_CONSTANT_FILTER=absolute ADDIU constant <= 0x20 (explicit report threshold)", "NO_RUNTIME_OR_EMULATOR=YES",
    ]
    return trace_rows, summary_rows, rmw_rows, site_summaries, summary


def self_test() -> None:
    words = [0x94820020, 0x24420003, 0xA4820020]
    ins = [decode(w.to_bytes(4, "little")) for w in words]
    cls, ev, di = classify_source(ins, 2, ins[2], 0x20)
    assert cls == "RMW_OFFSET_SAMA_PLUS_KONSTANTA" and "0x3" in ev and di == 0
    ins2 = [decode(0x24020005.to_bytes(4, "little")), decode(0xA4820020.to_bytes(4, "little"))]
    assert classify_source(ins2, 1, ins2[1], 0x20)[0] == "IMMEDIATE"
    assert len(CLASSES) == 6 and STRIDE == 0x124
    print("UM0_SELF_TEST=PASS")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", type=Path); ap.add_argument("--data-bin", type=Path)
    ap.add_argument("--access", type=Path, default=ACCESS); ap.add_argument("--windows", type=Path, default=WINDOWS); ap.add_argument("--matches", type=Path, default=MATCHES)
    ap.add_argument("--out-dir", type=Path); ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test(); return 0
    if not all((a.exe, a.data_bin, a.out_dir)):
        ap.error("--exe, --data-bin, --out-dir required")
    a.out_dir.mkdir(parents=True, exist_ok=True)
    exe = a.exe.read_bytes(); data = a.data_bin.read_bytes()
    trace, offsets, rmw, sites, summary = analyse(exe, data, read_tsv(a.access), read_tsv(a.windows), read_tsv(a.matches))
    write_tsv(a.out_dir / "UM0_WRITE_SITE_TRACE.tsv", ["site_id","region","written_offset","store_pc","store_file_offset","source_class","source_evidence","pointer_origin_EA84","pointer_origin_evidence","pc","file_offset","bytes_4B","instruction","role"], trace)
    write_tsv(a.out_dir / "UM0_OFFSET_SUMMARY.tsv", ["offset","write_sites",*CLASSES,"pcs","functions"], offsets)
    write_tsv(a.out_dir / "UM0_RMW_SMALL_CONSTANT_OFFSETS.tsv", ["offset","pc","constant","function"], rmw)
    write_tsv(a.out_dir / "UM0_WRITE_SITES.tsv", ["site_id","region","offset","pc","file_offset","source_class","source_evidence","pointer_origin","function"], sites)
    (a.out_dir / "UM0_SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
