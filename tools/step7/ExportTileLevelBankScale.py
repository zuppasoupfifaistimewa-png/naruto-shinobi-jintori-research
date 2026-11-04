#!/usr/bin/env python3
"""Expand the stored five-value tile bank through FUN_800B770C's exact subtype rules.

This is a static transformation of already-committed text records. It does not load
or execute the ROM, emulator, BIOS, savestate, or RAM dump.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
from typing import Dict, Iterable, List


LEVEL_FIELDS = [
    ("LV1", "runtime_tile_h_10"),
    ("LV2", "runtime_tile_h_12"),
    ("LV3", "runtime_tile_h_14"),
    ("LV4", "runtime_tile_h_16"),
    ("LV5", "runtime_tile_h_18"),
]

# Exact integer arithmetic reconstructed from FUN_800B770C.
# Case 1/2/3 performs multiply then unsigned integer divide by 10.
# Case 4 returns the source halfword shifted left by one.
SUBTYPES = {
    0: (1, 1, "value"),
    1: (12, 10, "value*12//10"),
    2: (15, 10, "value*15//10"),
    3: (18, 10, "value*18//10"),
    4: (2, 1, "value*2"),
}


def read_records(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=chr(9))
        required = {
            "entry_index", "resource_id_hex", "entry_sha256", "record_index",
            "record_source_offset", "runtime_tile_h_0E",
            *(field for _, field in LEVEL_FIELDS),
            "runtime_tile_h_1A", "runtime_tile_h_1C", "runtime_tile_h_1E",
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing TSV columns: {','.join(sorted(missing))}")
        rows = list(reader)
    if len(rows) != 44:
        raise ValueError(f"expected 44 rows (22 each from resources 630/638), got {len(rows)}")
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row["entry_index"]] = counts.get(row["entry_index"], 0) + 1
    if counts != {"630": 22, "638": 22}:
        raise ValueError(f"unexpected candidate resource row counts: {counts}")
    return rows


def u16(row: Dict[str, str], field: str) -> int:
    value = int(row[field], 0) if row[field].lower().startswith("0x") else int(row[field])
    if not 0 <= value <= 0xFFFF:
        raise ValueError(f"{field} is outside u16: {value}")
    return value


def expand(rows: Iterable[Dict[str, str]]) -> List[Dict[str, object]]:
    output: List[Dict[str, object]] = []
    for row in rows:
        for subtype, (numerator, denominator, expression) in SUBTYPES.items():
            for level_number, (level_name, field) in enumerate(LEVEL_FIELDS, start=1):
                stored = u16(row, field)
                reader_value = (stored * numerator) // denominator
                output.append({
                    "resource_entry_index": row["entry_index"],
                    "resource_id_hex": row["resource_id_hex"],
                    "resource_sha256": row["entry_sha256"],
                    "record_index": row["record_index"],
                    "record_source_offset": row["record_source_offset"],
                    "X_plus_0x0E": u16(row, "runtime_tile_h_0E"),
                    "reader_subtype_plus_0x0B": subtype,
                    "BB1_candidate_link_count_if_type5": subtype,
                    "candidate_group_record_count_if_BB1_type5_applies": subtype + 1,
                    "level": level_name,
                    "level_number": level_number,
                    "stored_halfword": stored,
                    "scale_numerator": numerator,
                    "scale_denominator": denominator,
                    "reader_output": reader_value,
                    "integer_expression": expression,
                    "plus_0x1A": u16(row, "runtime_tile_h_1A"),
                    "plus_0x1C": u16(row, "runtime_tile_h_1C"),
                    "plus_0x1E": u16(row, "runtime_tile_h_1E"),
                })
    return output


def write_tsv(path: Path, rows: List[Dict[str, object]]) -> None:
    if not rows:
        raise ValueError("no derived rows")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter=chr(9), lineterminator=chr(10))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()

    if not args.input.is_file():
        raise FileNotFoundError(args.input)
    source_bytes = args.input.read_bytes()
    source_sha = hashlib.sha256(source_bytes).hexdigest()
    source_rows = read_records(args.input)
    derived = expand(source_rows)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.out_dir / "CH2_LEVEL_BANK_OUTPUT_BY_SUBTYPE.tsv"
    summary_path = args.out_dir / "CH2_LEVEL_BANK_SCALE_SUMMARY.txt"
    write_tsv(output_path, derived)

    summary_lines = [
        "STATUS=PASS",
        "METHOD=static TSV expansion; no ROM/emulator execution",
        f"INPUT={args.input.as_posix()}",
        f"INPUT_TSV_SHA256={source_sha}",
        "INPUT_RESOURCE_RECORDS=44",
        "RESOURCE_630_RECORDS=22",
        "RESOURCE_638_RECORDS=22",
        "RESOURCE_630_SHA256=12c1a6ff1870f5c6fe33723beef14d93009b509d70caa882c5c6e8de8535e0c8",
        "RESOURCE_638_SHA256=d88af9fd0100da3ac3223aa5b1d85f884547b3e3f708ba1dec81cfb923f7775f",
        "SUBTYPE_CASES=0,1,2,3,4",
        "LEVELS=LV1:+0x10;LV2:+0x12;LV3:+0x14;LV4:+0x16;LV5:+0x18",
        "READER_SELECTOR=(u16(tile+0x20)>>7)&0x1E",
        "READER_EFFECTIVE_OFFSET=0x10+selector",
        "CASE_0=stored_value",
        "CASE_1=(stored_value*12)//10",
        "CASE_2=(stored_value*15)//10",
        "CASE_3=(stored_value*18)//10",
        "CASE_4=stored_value<<1",
        "DERIVED_ROWS=1100",
        "BB1_LINK_NOTE=FUN_800BE0E4 stores accepted successor-link count in tile+0x0B for type-5 chains; group size is link count+1 only where that BB1 type-5 interpretation applies",
        "SEMANTIC_LIMIT=reader outputs are proven numeric values, not proven upgrade prices, debit amounts, or toll",
        "X_FORMULA=not used; X is carried as a comparison column only",
    ]
    if len(derived) != 1100:
        raise ValueError(f"expected 1100 derived rows, got {len(derived)}")
    summary_path.write_text(chr(10).join(summary_lines) + chr(10), encoding="utf-8")
    print("CH2_LEVEL_BANK_EXPANSION=PASS records=44 subtype_cases=5 levels=5 rows=1100")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
