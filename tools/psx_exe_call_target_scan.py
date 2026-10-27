#!/usr/bin/env python3
"""Preliminary PS-X EXE JAL-target indexer; not a replacement for Ghidra.

The supplied executable remains local. This script reads the PS-X EXE header and
scans aligned 32-bit words in its declared text block, then writes text indices.
It does not execute the game or dump/decompile the whole program.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import struct
import sys


def u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exe", type=Path, help="local SLPS_035.53 path (do not commit the binary)")
    parser.add_argument("--output-dir", type=Path, default=Path("out"))
    args = parser.parse_args()

    data = args.exe.read_bytes()
    if len(data) < 0x800 or data[:8] != b"PS-X EXE":
        parser.error("input is not a PS-X EXE with a valid 8-byte magic")
    pc = u32(data, 0x10)
    load = u32(data, 0x18)
    text_size = u32(data, 0x1C)
    if text_size == 0 or text_size % 4:
        parser.error(f"invalid or non-word-aligned text size: 0x{text_size:X}")
    if 0x800 + text_size > len(data):
        parser.error("declared text extends beyond the supplied file")

    text = data[0x800:0x800 + text_size]
    end = load + text_size
    internal: dict[int, list[int]] = defaultdict(list)
    external_ram: dict[int, list[int]] = defaultdict(list)

    for off in range(0, len(text), 4):
        word = u32(text, off)
        if (word >> 26) != 3:  # MIPS JAL opcode
            continue
        callsite = load + off
        target = ((callsite + 4) & 0xF0000000) | ((word & 0x03FFFFFF) << 2)
        if load <= target < end:
            internal[target].append(callsite)
        elif 0x80000000 <= target < 0x80200000:
            external_ram[target].append(callsite)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "main_exe_function_candidates.tsv"
    with out.open("w", encoding="utf-8", newline="\n") as f:
        f.write("# PRELIMINARY heuristic function-entry index; not a Ghidra function database\n")
        f.write(f"# binary={args.exe.name} | file_size={len(data)} | pc=0x{pc:08X} | base=0x{load:08X} | text_size=0x{text_size:X}\n")
        f.write("# Candidate criterion: target of an aligned JAL word; target may be false positive or shared/jump-table/data.\n")
        f.write("address\tcaller_count\tstack_adjust_early\tsaves_ra_early\tfirst_word\tcaller_addresses\n")
        for target, callers in sorted(internal.items()):
            off = target - load
            words = [u32(text, off + i) for i in range(0, min(24, len(text) - off), 4)]
            stack_adjust = any(
                (w >> 26) == 9 and ((w >> 21) & 31) == 29
                and ((w >> 16) & 31) == 29 and (w & 0xFFFF) >= 0x8000
                for w in words[:4]
            )
            saves_ra = any(
                (w >> 26) == 0x2B and ((w >> 21) & 31) == 29
                and ((w >> 16) & 31) == 31
                for w in words[:6]
            )
            f.write(
                f"0x{target:08X}\t{len(callers)}\t{int(stack_adjust)}\t{int(saves_ra)}"
                f"\t0x{u32(text, off):08X}\t"
                + ",".join(f"0x{x:08X}" for x in callers) + "\n"
            )

    external = args.output_dir / "main_exe_external_ram_targets.tsv"
    with external.open("w", encoding="utf-8", newline="\n") as f:
        f.write("# Preliminary JAL targets outside declared main text but inside PS1 RAM range; verify each target.\n")
        f.write("target\tcaller_count\tcaller_addresses\n")
        for target, callers in sorted(external_ram.items()):
            f.write(f"0x{target:08X}\t{len(callers)}\t" + ",".join(f"0x{x:08X}" for x in callers) + "\n")

    print(f"PC=0x{pc:08X} load=0x{load:08X} text_size=0x{text_size:X} ({text_size} bytes)")
    print(f"JAL target candidates inside text: {len(internal)} unique / {sum(map(len, internal.values()))} sites")
    print(f"JAL targets outside text but in PS1 RAM range: {len(external_ram)} unique / {sum(map(len, external_ram.values()))} sites")
    print(f"Wrote {out} and {external}")
    print("These are heuristic candidates, not verified function boundaries. Ghidra is still required for the planned function database.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
