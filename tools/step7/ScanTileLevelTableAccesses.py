#!/usr/bin/env python3
"""Raw aligned MIPS scan for tile level-table fields +0x10..+0x18 only.

This scanner deliberately excludes +0xEA8 and +0x1A. It emits byte-derived
candidates, hashes, the prior 12 words, and a raw instruction window <=64 bytes.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
from collections import Counter
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
FIELDS = {0x0E,0x10,0x12,0x14,0x16,0x18}

def scan(label: str, path: Path, base: int, file_start: int, scan_bytes: int | None):
    data = path.read_bytes()
    end = len(data) if scan_bytes is None else min(len(data), file_start + scan_bytes)
    if file_start < 0 or end < file_start:
        raise ValueError(f"invalid scan bounds for {label}")
    rows = []
    for pos in range(file_start, end - 3, 4):
        word = int.from_bytes(data[pos:pos+4], "little")
        op, imm = (word >> 26) & 0x3F, word & 0xFFFF
        if op not in OPS or imm not in FIELDS:
            continue
        mnemonic, access = OPS[op]
        rel = pos - file_start
        pc = base + rel
        rt, rs = (word >> 16) & 31, (word >> 21) & 31
        prev = []
        for n in range(12, 0, -1):
            q = pos - 4*n
            if q < file_start:
                continue
            prev.append(f"{base + q - file_start:08X}:{data[q:q+4].hex().upper()}")
        excerpt_start = max(file_start, pos - 60)
        excerpt_end = min(end, pos + 4)
        excerpt = data[excerpt_start:excerpt_end]
        rows.append({
            "image": label, "pc": f"0x{pc:08X}", "file_offset": f"0x{pos:08X}",
            "field_offset": f"+0x{imm:02X}", "access": access,
            "mnemonic": mnemonic, "base_reg": REGS[rs], "value_reg": REGS[rt],
            "word_le": f"0x{word:08X}", "instruction_bytes": data[pos:pos+4].hex(" ").upper(),
            "previous_12_raw_words": " | ".join(prev),
            "raw_excerpt_bytes_le_max_64": excerpt.hex(" ").upper(),
        })
    return data, rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", required=True, type=Path)
    ap.add_argument("--entry1", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    a = ap.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)
    exe, rexe = scan("MAIN_EXE_SLPS_035.53", a.exe, 0x80010000, 0x800, 0x5D800)
    ent, rent = scan("DATA_BIN_ENTRY_0001", a.entry1, 0x800AD450, 0, None)
    rows = rexe + rent
    fields = ["image","pc","file_offset","field_offset","access","mnemonic","base_reg",
              "value_reg","word_le","instruction_bytes","previous_12_raw_words",
              "raw_excerpt_bytes_le_max_64"]
    out = a.out_dir / "tile-level-raw-mips-candidates.tsv"
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    counts = Counter((r["image"],r["field_offset"],r["access"]) for r in rows)
    lines = [
        "TILE_LEVEL_RAW_MIPS_SCAN=PASS",
        f"EXE_BYTES={len(exe)} EXE_SHA256={hashlib.sha256(exe).hexdigest()}",
        f"ENTRY1_BYTES={len(ent)} ENTRY1_SHA256={hashlib.sha256(ent).hexdigest()}",
        "EXE_MAP=raw file offset 0x800 maps to PC 0x80010000; scan length 0x5D800",
        "ENTRY1_MAP=raw byte offset 0 maps to candidate PC 0x800AD450; runtime mapping unverified",
        "FILTER=aligned little-endian MIPS-I memory instructions with exact signed-positive displacement 0x0E/0x10/0x12/0x14/0x16/0x18",
        "SCOPE=raw opcode candidates only; validity, function and object alias require Ghidra review",
        "EXCLUDES=+0xEA8 and +0x1A (not scanned by this script)",
        f"CANDIDATE_ROWS={len(rows)}",
    ]
    for (image,field,access),count in sorted(counts.items()):
        lines.append(f"{image} {field} {access}={count}")
    (a.out_dir / "tile-level-raw-mips-summary.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
