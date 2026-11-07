#!/usr/bin/env python3
"""Read-only HA2 bound/table probe for the verified SLPS-03553 PS-X EXE."""
from __future__ import annotations
import argparse
import csv
import hashlib
import re
import struct
from fractions import Fraction
from pathlib import Path
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_BASE = 0x80010000
EXE_FILE_BASE = 0x800
EXE_SIZE = 385024
EXE_SHA256 = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
BOUND_VA = 0x8006D794
TABLE_VA = 0x80055CF4

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def file_offset(va: int) -> int:
    if not (EXE_BASE <= va < EXE_BASE + (EXE_SIZE - EXE_FILE_BASE)):
        raise ValueError(f"VA outside loaded EXE image: 0x{va:08X}")
    return EXE_FILE_BASE + (va - EXE_BASE)

def write_tsv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)

def decoder(exe: bytes) -> Cs:
    md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_LITTLE_ENDIAN)
    md.detail = False
    return md

def decode_at(exe: bytes, md: Cs, pc: int):
    off = file_offset(pc)
    raw = exe[off:off + 4]
    ins = next(md.disasm(raw, pc, count=1), None)
    if ins is None:
        return raw, ".word 0x" + raw[::-1].hex().upper()
    return raw, (ins.mnemonic.lower() + " " + ins.op_str).strip()

def decode_gp_accesses(exe: bytes, md: Cs):
    found = []
    pat = re.compile(r"^\s*(-?(?:0x[0-9a-f]+|\d+))\(\$?gp\)\s*$", re.I)
    # PS-X EXE header occupies file offsets [0, 0x800); loaded bytes begin at 0x800.
    for off in range(EXE_FILE_BASE, len(exe) - 3, 4):
        pc = EXE_BASE + (off - EXE_FILE_BASE)
        raw = exe[off:off + 4]
        ins = next(md.disasm(raw, pc, count=1), None)
        if ins is None or ins.mnemonic.lower() not in {
            "lb", "lbu", "lh", "lhu", "lw", "sb", "sh", "sw"
        }:
            continue
        m = pat.match(ins.op_str.split(",", 1)[-1].strip())
        if not m:
            continue
        try:
            imm = int(m.group(1), 0)
        except ValueError:
            continue
        if imm == 0x118:
            found.append((pc, raw, (ins.mnemonic.lower() + " " + ins.op_str).strip()))
    return found

def write_context(exe: bytes, md: Cs, center_pc: int, out: Path, name: str) -> int:
    start_pc = max(EXE_BASE, center_pc - 8 * 4)
    start_pc = EXE_BASE + ((start_pc - EXE_BASE) // 4) * 4
    rows = []
    for i in range(16):
        pc = start_pc + i * 4
        if file_offset(pc) + 4 > len(exe):
            break
        raw, ins = decode_at(exe, md, pc)
        rows.append([f"0x{pc:08X}", f"0x{file_offset(pc):X}", " ".join(f"{x:02X}" for x in raw), ins])
    write_tsv(out / name, ["pc", "file_offset", "bytes", "instruksi"], rows)
    return len(rows)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    exe = a.exe.read_bytes()
    if len(exe) != EXE_SIZE:
        raise SystemExit(f"EXE_SIZE_MISMATCH={len(exe)}")
    digest = sha256(exe)
    if digest != EXE_SHA256:
        raise SystemExit(f"EXE_SHA256_MISMATCH={digest}")

    md = decoder(exe)
    b_off = file_offset(BOUND_VA)
    table_off = file_offset(TABLE_VA)
    b_bytes = exe[b_off:b_off + 4]
    if len(b_bytes) != 4:
        raise SystemExit("BOUND_BYTES_UNAVAILABLE")
    bound_image = struct.unpack("<I", b_bytes)[0]
    max_entries = max(0, (len(exe) - table_off - 4) // 16 + 1)
    accesses = decode_gp_accesses(exe, md)
    writers = [x for x in accesses if x[2].split(" ", 1)[0] in {"sb", "sh", "sw"}]

    census_rows = []
    for pc, raw, text in accesses:
        census_rows.append([f"0x{pc:08X}", f"0x{file_offset(pc):X}",
                            " ".join(f"{x:02X}" for x in raw), text])
    write_tsv(a.out / "HA2_BOUND_GP_ACCESS_CENSUS.tsv",
              ["pc", "file_offset", "bytes", "instruksi"], census_rows)

    context_instruction_count = 0
    for idx, (pc, raw, text) in enumerate(writers):
        context_instruction_count += write_context(
            exe, md, pc, a.out, f"HA2_BOUND_WRITER_CONTEXT_{idx:02d}.tsv"
        )

    summary = [
        "PROBE=HA2_BOUND_AND_TABLE_RAW_EXE",
        f"EXE_SIZE={len(exe)}",
        f"EXE_SHA256={digest}",
        f"BOUND_VA=0x{BOUND_VA:08X}",
        f"BOUND_FILE_OFFSET=0x{b_off:X}",
        f"BOUND_IMAGE_BYTES={' '.join(f'{x:02X}' for x in b_bytes)}",
        f"BOUND_IMAGE_U32={bound_image}",
        f"BOUND_IMAGE_HEX=0x{bound_image:08X}",
        "BOUND_SEMANTIC=FUN_800154D4 returns the word loaded from GP+0x118 (DAT_8006D794).",
        f"TABLE_VA=0x{TABLE_VA:08X}",
        f"TABLE_FILE_OFFSET=0x{table_off:X}",
        "TABLE_STRIDE=0x10",
        f"MAX_ENTRIES_WITHIN_EXE={max_entries}",
        f"GP_PLUS_0x118_DIRECT_ACCESS_CANDIDATES={len(accesses)}",
        f"GP_PLUS_0x118_STORE_CANDIDATES={len(writers)}",
        f"WRITER_CONTEXT_INSTRUCTIONS_EXPORTED={context_instruction_count}",
        "GP_ACCESS_SCAN_SCOPE=loaded PS-X EXE bytes only (file offset starts at 0x800)",
    ]

    if writers:
        summary.append("BOUND_RUNTIME_STATUS=TIDAK TAHU; GP+0x118 has direct store candidate(s), so zero image initializer is not a runtime bound.")
        summary.append("TABLE_EXTRACTION_STATUS=BLOCKED_RUNTIME_BOUND_UNKNOWN")
        summary.append("TABLE_ROWS_EXTRACTED=0")
    elif bound_image <= max_entries:
        vals = []
        rows = []
        for i in range(bound_image):
            va = TABLE_VA + 16 * i
            off = file_offset(va)
            raw = exe[off:off + 4]
            if len(raw) != 4:
                raise SystemExit(f"TABLE_WORD_TRUNCATED index={i}")
            value = struct.unpack("<I", raw)[0]
            vals.append(value)
            rows.append([str(i), f"0x{va:08X}", f"0x{off:X}",
                         " ".join(f"{x:02X}" for x in raw), f"0x{value:08X}"])
        for n in range(0, len(rows), 16):
            write_tsv(a.out / f"HA2_TABLE_U32_{n // 16:03d}.tsv",
                      ["index", "alamat", "file_offset", "bytes", "u32"], rows[n:n + 16])
        summary.append("BOUND_RUNTIME_STATUS=IMAGE_INITIALIZER_ONLY; no direct writer candidate found by this scan.")
        summary.append("TABLE_EXTRACTION_STATUS=EXTRACTED_FROM_LOADED_IMAGE_BYTES")
        summary.append(f"TABLE_ROWS_EXTRACTED={len(vals)}")
        if vals:
            summary.append(f"TABLE_U32_MIN=0x{min(vals):08X}")
            summary.append(f"TABLE_U32_MAX=0x{max(vals):08X}")
        if bound_image > 16 and vals:
            ratios = [Fraction(vals[i + 1], vals[i]) for i in range(len(vals) - 1) if vals[i] != 0]
            zero_den = sum(1 for i in range(len(vals) - 1) if vals[i] == 0)
            summary.append(f"CONSECUTIVE_RATIO_PAIRS_NONZERO_DENOMINATOR={len(ratios)}")
            summary.append(f"CONSECUTIVE_RATIO_ZERO_DENOMINATOR_PAIRS={zero_den}")
            if ratios:
                summary.append(f"CONSECUTIVE_RATIO_MIN={min(ratios)}")
                summary.append(f"CONSECUTIVE_RATIO_MAX={max(ratios)}")
            summary.append("NO_FITTING=YES")
    else:
        summary.append("BOUND_RUNTIME_STATUS=TIDAK TAHU; image value outside table capacity.")
        summary.append("TABLE_EXTRACTION_STATUS=BLOCKED_BOUND_EXCEEDS_IMAGE_CAPACITY")
        summary.append("TABLE_ROWS_EXTRACTED=0")

    (a.out / "HA2_BOUND_TABLE_SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
