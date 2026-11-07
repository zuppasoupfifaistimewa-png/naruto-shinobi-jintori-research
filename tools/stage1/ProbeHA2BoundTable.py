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
    if not (EXE_BASE <= va < EXE_BASE + EXE_SIZE):
        raise ValueError(f"VA outside EXE image: 0x{va:08X}")
    return EXE_FILE_BASE + (va - EXE_BASE)

def write_tsv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)

def decode_gp_accesses(exe: bytes) -> list[tuple[int, bytes, str]]:
    md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_LITTLE_ENDIAN)
    md.detail = False
    found = []
    pat = re.compile(r"^\s*(-?(?:0x[0-9a-f]+|\d+))\(\$?gp\)\s*$", re.I)
    for off in range(0, len(exe) - 3, 4):
        raw = exe[off:off + 4]
        ins = next(md.disasm(raw, EXE_BASE + off, count=1), None)
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
            found.append((EXE_BASE + off, raw, f"{ins.mnemonic.lower()} {ins.op_str}"))
    return found

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

    b_off = file_offset(BOUND_VA)
    table_off = file_offset(TABLE_VA)
    b_bytes = exe[b_off:b_off + 4]
    if len(b_bytes) != 4:
        raise SystemExit("BOUND_BYTES_UNAVAILABLE")
    bound_image = struct.unpack("<I", b_bytes)[0]
    max_entries = max(0, (len(exe) - table_off - 4) // 16 + 1)
    accesses = decode_gp_accesses(exe)

    gp_rows = []
    for pc, raw, text in accesses:
        gp_rows.append([
            f"0x{pc:08X}",
            f"0x{file_offset(pc):X}",
            " ".join(f"{x:02X}" for x in raw),
            text,
        ])
    for n in range(0, len(gp_rows), 16):
        write_tsv(
            a.out / f"HA2_BOUND_GP_ACCESS_{n // 16:02d}.tsv",
            ["pc", "file_offset", "bytes", "instruksi"],
            gp_rows[n:n + 16],
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
        "BOUND_SEMANTIC=FUN_800154D4 returns the word loaded from GP+0x118 (DAT_8006D794); raw image bytes are an initializer, not proof of runtime value if overwritten.",
        f"TABLE_VA=0x{TABLE_VA:08X}",
        f"TABLE_FILE_OFFSET=0x{table_off:X}",
        "TABLE_STRIDE=0x10",
        f"MAX_ENTRIES_WITHIN_EXE={max_entries}",
        f"GP_PLUS_0x118_DIRECT_ACCESS_CANDIDATES={len(accesses)}",
        f"TABLE_EXTRACTION_STATUS=NOT_ATTEMPTED",
    ]

    if bound_image <= max_entries:
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
            rows.append([
                str(i),
                f"0x{va:08X}",
                f"0x{off:X}",
                " ".join(f"{x:02X}" for x in raw),
                f"0x{value:08X}",
            ])
        for n in range(0, len(rows), 16):
            write_tsv(
                a.out / f"HA2_TABLE_U32_{n // 16:03d}.tsv",
                ["index", "alamat", "file_offset", "bytes", "u32"],
                rows[n:n + 16],
            )
        summary[summary.index("TABLE_EXTRACTION_STATUS=NOT_ATTEMPTED")] = (
            "TABLE_EXTRACTION_STATUS=EXTRACTED_FROM_LOADED_IMAGE_BYTES"
        )
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
        summary.append("TABLE_EXTRACTION_STATUS=BLOCKED_BOUND_EXCEEDS_IMAGE_CAPACITY")
        summary.append("TABLE_ROWS_EXTRACTED=0")
        summary.append("BOUND_RUNTIME_VALUE=TIDAK TAHU; image word cannot be accepted as runtime bound without writer audit.")

    if accesses:
        summary.append("GP_REL_ACCESS_REVIEW=inspect candidate rows; raw sequential disassembly can include data regions.")
    else:
        summary.append("GP_REL_ACCESS_REVIEW=no direct GP+0x118 memory-op candidates found by sequential scan; aliases/indirect writes remain possible.")

    (a.out / "HA2_BOUND_TABLE_SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
