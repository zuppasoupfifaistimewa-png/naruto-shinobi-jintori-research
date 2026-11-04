#!/usr/bin/env python3
"""Raw aligned MIPS byte scan for EA8 object-field candidates and tile fee +0x1A.

The scan reads only the runner's private verified EXE/Entry-1 inputs. It emits
addresses, opcodes, short raw instruction windows and hashes; it never copies
or publishes source binaries.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
from pathlib import Path

REGS = ("zero","at","v0","v1","a0","a1","a2","a3",
        "t0","t1","t2","t3","t4","t5","t6","t7",
        "s0","s1","s2","s3","s4","s5","s6","s7",
        "t8","t9","k0","k1","gp","sp","fp","ra")
OPS = {
    0x20: ("lb","READ"), 0x21: ("lh","READ"), 0x23: ("lw","READ"),
    0x24: ("lbu","READ"), 0x25: ("lhu","READ"),
    0x28: ("sb","WRITE"), 0x29: ("sh","WRITE"), 0x2B: ("sw","WRITE"),
}

def scan(label: str, path: Path, base: int, file_start: int, scan_bytes: int | None):
    data = path.read_bytes()
    end = len(data) if scan_bytes is None else min(len(data), file_start + scan_bytes)
    if file_start < 0 or end < file_start:
        raise ValueError(f"invalid scan bounds for {label}")
    rows = []
    for pos in range(file_start, end - 3, 4):
        word = int.from_bytes(data[pos:pos+4], "little")
        op = (word >> 26) & 0x3F
        imm = word & 0xFFFF
        if op not in OPS or imm not in (0x0EA8, 0x001A):
            continue
        mnemonic, access = OPS[op]
        if imm == 0x0EA8 and access == "WRITE":
            purpose = "EA8_STORE_CANDIDATE"
        elif imm == 0x0EA8:
            purpose = "EA8_READER_CANDIDATE"
        elif access == "WRITE":
            purpose = "TILE_PLUS_1A_STORE_CANDIDATE"
        else:
            purpose = "TILE_PLUS_1A_READER_CANDIDATE"
        rel = pos - file_start
        pc = base + rel
        rt, rs = (word >> 16) & 31, (word >> 21) & 31
        excerpt_start = max(file_start, pos - 48)
        excerpt_end = min(end, pos + 4)
        excerpt = data[excerpt_start:excerpt_end]
        prev = []
        for n in range(12, 0, -1):
            q = pos - 4*n
            if q < file_start:
                continue
            prev.append(f"{base + q - file_start:08X}:{data[q:q+4].hex().upper()}")
        rows.append({
            "image": label, "pc": f"0x{pc:08X}", "file_offset": f"0x{pos:08X}",
            "purpose": purpose, "access": access, "mnemonic": mnemonic,
            "base_reg": REGS[rs], "rt_or_value_reg": REGS[rt],
            "immediate": f"0x{imm:04X}", "word_le": f"0x{word:08X}",
            "instruction_bytes": data[pos:pos+4].hex(" ").upper(),
            "previous_12_raw_words": " | ".join(prev),
            "raw_excerpt_bytes_le_64": excerpt.hex(" ").upper(),
        })
    return data, rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", required=True, type=Path)
    ap.add_argument("--entry1", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    a = ap.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)
    exe, rows_exe = scan("MAIN_EXE_SLPS_035.53", a.exe, 0x80010000, 0x800, 0x5D800)
    ent, rows_ent = scan("DATA_BIN_ENTRY_0001", a.entry1, 0x800AD450, 0, None)
    rows = rows_exe + rows_ent
    fields = ["image","pc","file_offset","purpose","access","mnemonic","base_reg",
              "rt_or_value_reg","immediate","word_le","instruction_bytes",
              "previous_12_raw_words","raw_excerpt_bytes_le_64"]
    with (a.out_dir / "cg_raw_mips_offset_candidates.tsv").open("w",encoding="utf-8",newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    counts = {}
    for r in rows:
        k = (r["image"], r["purpose"])
        counts[k] = counts.get(k, 0) + 1
    lines = [
        "RAW_MIPS_OFFSET_SCAN=PASS",
        f"EXE_BYTES={len(exe)} EXE_SHA256={hashlib.sha256(exe).hexdigest()}",
        f"ENTRY1_BYTES={len(ent)} ENTRY1_SHA256={hashlib.sha256(ent).hexdigest()}",
        "EXE_MAP=raw file offset 0x800 maps to PC 0x80010000; scanned text length 0x5D800",
        "ENTRY1_MAP=raw byte offset 0 maps to candidate PC 0x800AD450; runtime mapping not independently validated",
        "FILTER=aligned little-endian MIPS I-type words with exact immediate 0x0EA8 or 0x001A and memory opcodes",
        "NOTE=raw opcode candidates are not automatically valid code or proven pointer aliases; Ghidra listing/function review is required",
        f"TOTAL_CANDIDATES={len(rows)}",
    ]
    for (image, purpose), count in sorted(counts.items()):
        lines.append(f"{image} {purpose}={count}")
    (a.out_dir / "cg_raw_mips_offset_scan_summary.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
