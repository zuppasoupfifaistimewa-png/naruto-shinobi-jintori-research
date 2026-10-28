#!/usr/bin/env python3
"""Read-only PCSX-Redux SaveState v4 parser for a bounded 2 MiB memory prefix.

This tool never launches an emulator. It writes an extracted binary only to the
requested output path and emits a sanitized CSV manifest. Do not commit savestates
or extracted RAM dumps to the research repository.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import struct
from pathlib import Path

HEADER_TEXT = b"PCSX-Redux SaveState v4"
RAM_BYTES = 0x200000
FIELD_MEMORY = 3
FIELD_RAM_REGION = 1
ADDRESSES = (0x80070EB8, 0x80070F6C)

def read_varint(buf: bytes, pos: int) -> tuple[int, int]:
    value = shift = 0
    while pos < len(buf) and shift <= 63:
        b = buf[pos]
        pos += 1
        value |= (b & 0x7F) << shift
        if not (b & 0x80):
            return value, pos
        shift += 7
    raise ValueError("invalid/truncated protobuf varint")

def parse_fields(buf: bytes):
    """Yield (field_number, wire_type, value) for protobuf wire types 0/1/2/5."""
    pos = 0
    while pos < len(buf):
        key, pos = read_varint(buf, pos)
        number, wire = key >> 3, key & 7
        if number == 0:
            raise ValueError("invalid protobuf field number 0")
        if wire == 0:
            value, pos = read_varint(buf, pos)
        elif wire == 1:
            if pos + 8 > len(buf):
                raise ValueError("truncated fixed64")
            value, pos = buf[pos:pos + 8], pos + 8
        elif wire == 2:
            size, pos = read_varint(buf, pos)
            if pos + size > len(buf):
                raise ValueError("truncated length-delimited field")
            value, pos = buf[pos:pos + size], pos + size
        elif wire == 5:
            if pos + 4 > len(buf):
                raise ValueError("truncated fixed32")
            value, pos = buf[pos:pos + 4], pos + 4
        else:
            raise ValueError(f"unsupported protobuf wire type {wire}")
        yield number, wire, value

def one(fields, number, wire, label):
    hits = [value for n, w, value in fields if n == number and w == wire]
    if len(hits) != 1:
        raise ValueError(
            f"expected one {label} (field {number}, wire {wire}), found {len(hits)}"
        )
    return hits[0]

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("state", type=Path, help="path to private PCSX-Redux .sstate")
    ap.add_argument("output_ram", type=Path,
                    help="destination for extracted 2 MiB region (keep private)")
    ap.add_argument("--csv", type=Path,
                    help="sanitized output CSV; default: OUTPUT.csv")
    ap.add_argument("--run-id", default="unknown",
                    help="source GitHub Actions run ID for the manifest")
    args = ap.parse_args()

    state = args.state.read_bytes()
    top = list(parse_fields(state))
    header_payload = one(top, 1, 2, "header message")
    header_fields = list(parse_fields(header_payload))
    header_text = one(header_fields, 1, 2, "header text")
    version = one(header_fields, 2, 0, "save-state version")
    if header_text != HEADER_TEXT or version != 4:
        raise ValueError(
            f"unsupported save state: header={header_text!r}, version={version!r}"
        )

    memory_payload = one(top, FIELD_MEMORY, 2, "memory message")
    memory_fields = list(parse_fields(memory_payload))
    region = one(memory_fields, FIELD_RAM_REGION, 2, "memory region 1")
    if len(region) < RAM_BYTES:
        raise ValueError(f"memory region too small: {len(region)} bytes")
    ram = region[:RAM_BYTES]

    args.output_ram.parent.mkdir(parents=True, exist_ok=True)
    args.output_ram.write_bytes(ram)
    csv_path = args.csv or args.output_ram.with_suffix(args.output_ram.suffix + ".csv")
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    columns = [
        "source_run_id", "state_file_name", "state_bytes", "state_sha256",
        "memory_field", "memory_field_bytes", "ram_dump_file_name",
        "ram_dump_bytes", "ram_dump_sha256", "virtual_address",
        "ram_offset_hex", "raw_bytes_le", "u32_le_decimal", "semantic_label",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for va in ADDRESSES:
            offset = va - 0x80000000
            if offset < 0 or offset + 4 > len(ram):
                raise ValueError(f"address {va:#x} does not map into extracted region")
            raw = ram[offset:offset + 4]
            writer.writerow({
                "source_run_id": args.run_id,
                "state_file_name": args.state.name,
                "state_bytes": len(state),
                "state_sha256": sha256(state),
                "memory_field": "top-level field 3 / nested field 1 prefix",
                "memory_field_bytes": len(region),
                "ram_dump_file_name": args.output_ram.name,
                "ram_dump_bytes": len(ram),
                "ram_dump_sha256": sha256(ram),
                "virtual_address": f"0x{va:08X}",
                "ram_offset_hex": f"0x{offset:06X}",
                "raw_bytes_le": raw.hex(" ").upper(),
                "u32_le_decimal": struct.unpack("<I", raw)[0],
                "semantic_label": "UNKNOWN: structural record field only; not proven Chakra",
            })

    print(f"STATE_BYTES={len(state)}")
    print(f"STATE_SHA256={sha256(state)}")
    print(f"HEADER={header_text.decode('ascii')} VERSION={version}")
    print(f"MEMORY_FIELD3_BYTES={len(memory_payload)} MEMORY_FIELD1_BYTES={len(region)}")
    print(f"RAM_DUMP={args.output_ram} BYTES={len(ram)} SHA256={sha256(ram)}")
    print(f"SANITIZED_CSV={csv_path}")
    for va in ADDRESSES:
        offset = va - 0x80000000
        raw = ram[offset:offset + 4]
        value = struct.unpack("<I", raw)[0]
        print(f"U32 address=0x{va:08X} offset=0x{offset:06X} "
              f"bytes={raw.hex()} value={value}")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        raise SystemExit(f"ERROR: {exc}")
