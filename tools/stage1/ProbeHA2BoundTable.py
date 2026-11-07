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
TABLE_RECORD_BASE_VA = 0x80055CEC
TABLE_VALUE_BASE_VA = 0x80055CF4
SENTINEL = 0xFFFFFFFF
STRIDE = 0x10

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

def make_decoder() -> Cs:
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

def write_window(exe: bytes, md: Cs, start_pc: int, out: Path, name: str) -> int:
    rows = []
    for i in range(16):
        pc = start_pc + i * 4
        if file_offset(pc) + 4 > len(exe):
            break
        raw, text = decode_at(exe, md, pc)
        rows.append([f"0x{pc:08X}", f"0x{file_offset(pc):X}",
                     " ".join(f"{x:02X}" for x in raw), text])
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

    md = make_decoder()
    bound_off = file_offset(BOUND_VA)
    bound_bytes = exe[bound_off:bound_off + 4]
    if len(bound_bytes) != 4:
        raise SystemExit("BOUND_BYTES_UNAVAILABLE")
    bound_image = struct.unpack("<I", bound_bytes)[0]
    max_entries = max(0, (len(exe) - file_offset(TABLE_VALUE_BASE_VA) - 4) // STRIDE + 1)

    accesses = decode_gp_accesses(exe, md)
    writers = [x for x in accesses if x[2].split(" ", 1)[0] in {"sb", "sh", "sw"}]
    write_tsv(
        a.out / "HA2_BOUND_GP_ACCESS_CENSUS.tsv",
        ["pc", "file_offset", "bytes", "instruksi"],
        [[f"0x{pc:08X}", f"0x{file_offset(pc):X}",
          " ".join(f"{x:02X}" for x in raw), ins] for pc, raw, ins in accesses],
    )

    init_context_rows = 0
    if len(exe) > file_offset(0x800121AC) + 4 * 31:
        init_context_rows += write_window(exe, md, 0x800121AC, a.out, "HA2_BOUND_INITIALIZER_00.tsv")
        init_context_rows += write_window(exe, md, 0x800121EC, a.out, "HA2_BOUND_INITIALIZER_01.tsv")

    # The initializer compares each record tag (record base + 0) to 0xFFFFFFFF.
    # The first sentinel index is the count written to GP+0x118.
    sentinel_rows = []
    sentinel_index = None
    for i in range(max_entries):
        va = TABLE_RECORD_BASE_VA + STRIDE * i
        off = file_offset(va)
        raw = exe[off:off + 4]
        if len(raw) != 4:
            break
        tag = struct.unpack("<I", raw)[0]
        sentinel_rows.append([str(i), f"0x{va:08X}", f"0x{off:X}",
                              " ".join(f"{x:02X}" for x in raw), f"0x{tag:08X}"])
        if tag == SENTINEL:
            sentinel_index = i
            break
    for n in range(0, len(sentinel_rows), 16):
        write_tsv(
            a.out / f"HA2_BOUND_SENTINEL_SCAN_{n // 16:03d}.tsv",
            ["index", "alamat", "file_offset", "bytes", "u32"],
            sentinel_rows[n:n + 16],
        )

    summary = [
        "PROBE=HA2_BOUND_SENTINEL_AND_HELPER_TABLE",
        f"EXE_SIZE={len(exe)}",
        f"EXE_SHA256={digest}",
        f"BOUND_VA=0x{BOUND_VA:08X}",
        f"BOUND_FILE_OFFSET=0x{bound_off:X}",
        f"BOUND_IMAGE_BYTES={' '.join(f'{x:02X}' for x in bound_bytes)}",
        f"BOUND_IMAGE_U32={bound_image}",
        "BOUND_IMAGE_VALUE_IS_NOT_RUNTIME_BOUND=YES",
        f"TABLE_RECORD_BASE_VA=0x{TABLE_RECORD_BASE_VA:08X}",
        f"TABLE_VALUE_BASE_VA=0x{TABLE_VALUE_BASE_VA:08X}",
        f"TABLE_VALUE_FILE_OFFSET=0x{file_offset(TABLE_VALUE_BASE_VA):X}",
        f"TABLE_STRIDE=0x{STRIDE:X}",
        f"TABLE_TAG_SENTINEL=0x{SENTINEL:08X}",
        f"GP_PLUS_0x118_DIRECT_ACCESS_CANDIDATES={len(accesses)}",
        f"GP_PLUS_0x118_STORE_CANDIDATES={len(writers)}",
        f"BOUND_INITIALIZER_CONTEXT_ROWS={init_context_rows}",
        f"SENTINEL_SCAN_ROWS={len(sentinel_rows)}",
    ]

    if sentinel_index is None:
        summary += [
            "BOUND_RUNTIME_STATUS=TIDAK TAHU; sentinel not found within verified EXE table bounds.",
            "TABLE_EXTRACTION_STATUS=BLOCKED_NO_SENTINEL",
            "TABLE_ROWS_EXTRACTED=0",
        ]
    else:
        summary += [
            f"BOUND_DERIVED_FROM_SENTINEL_INDEX={sentinel_index}",
            f"BOUND_DERIVED_HEX=0x{sentinel_index:08X}",
            "BOUND_ALGORITHM=first i where u32[0x80055CEC+16*i] == 0xFFFFFFFF; initializer stores i to GP+0x118.",
            "BOUND_RUNTIME_STATUS=STATIC_INITIALIZER_RESULT; execution order not runtime-validated.",
        ]
        values = []
        value_rows = []
        for i in range(sentinel_index):
            va = TABLE_VALUE_BASE_VA + STRIDE * i
            off = file_offset(va)
            raw = exe[off:off + 4]
            if len(raw) != 4:
                raise SystemExit(f"TABLE_WORD_TRUNCATED index={i}")
            value = struct.unpack("<I", raw)[0]
            values.append(value)
            value_rows.append([str(i), f"0x{va:08X}", f"0x{off:X}",
                               " ".join(f"{x:02X}" for x in raw), f"0x{value:08X}"])
        for n in range(0, len(value_rows), 16):
            write_tsv(
                a.out / f"HA2_TABLE_U32_{n // 16:03d}.tsv",
                ["index", "alamat", "file_offset", "bytes", "u32"],
                value_rows[n:n + 16],
            )
        summary += [
            "TABLE_EXTRACTION_STATUS=EXTRACTED_FROM_SENTINEL_BOUND",
            f"TABLE_ROWS_EXTRACTED={len(values)}",
        ]
        if values:
            summary.append(f"TABLE_U32_MIN=0x{min(values):08X}")
            summary.append(f"TABLE_U32_MAX=0x{max(values):08X}")
        if sentinel_index > 16 and values:
            ratios = [Fraction(values[i + 1], values[i])
                      for i in range(len(values) - 1) if values[i] != 0]
            zero_den = sum(1 for i in range(len(values) - 1) if values[i] == 0)
            summary.append(f"CONSECUTIVE_RATIO_PAIRS_NONZERO_DENOMINATOR={len(ratios)}")
            summary.append(f"CONSECUTIVE_RATIO_ZERO_DENOMINATOR_PAIRS={zero_den}")
            if ratios:
                summary.append(f"CONSECUTIVE_RATIO_MIN={min(ratios)}")
                summary.append(f"CONSECUTIVE_RATIO_MAX={max(ratios)}")
            summary.append("NO_FITTING=YES")

    (a.out / "HA2_BOUND_TABLE_SUMMARY.txt").write_text(
        "\n".join(summary) + "\n", encoding="utf-8"
    )
    print("\n".join(summary))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
