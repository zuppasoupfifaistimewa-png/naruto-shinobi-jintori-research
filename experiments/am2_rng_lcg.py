#!/usr/bin/env python3
"""Compute the minimal LCG transition count between consecutive H6 RNG samples."""
from __future__ import annotations
import argparse
import csv
import re
from pathlib import Path

MULT = 0x41C64E6D
ADD = 0x3039
MASK = 0xFFFFFFFF
MAX_K = 1 << 24
ADDRESS = "0x800A3118"
FRAMES = (1, 60, 180, 240, 360)


def lcg_step(state: int) -> int:
    return (MULT * state + ADD) & MASK


def find_k(before: int, after: int, max_k: int = MAX_K) -> int | None:
    """Return the smallest k in [0,max_k] with LCG**k(before)==after."""
    if before == after:
        return 0
    state = before
    for k in range(1, max_k + 1):
        state = lcg_step(state)
        if state == after:
            return k
    return None


def parse_rng(words: str) -> int:
    match = re.search(re.escape(ADDRESS) + r"\s+bytes=[^;]*?LE32=(0x[0-9A-Fa-f]+)", words)
    if not match:
        raise ValueError(f"missing {ADDRESS} in words column: {words}")
    return int(match.group(1), 16)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-k", type=int, default=MAX_K)
    args = parser.parse_args()
    if args.max_k < 0 or args.max_k > MAX_K:
        raise SystemExit(f"max-k must be in [0,{MAX_K}]")

    values: dict[tuple[int, int], int] = {}
    with args.input.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        required = {"variant", "attempt", "frame", "capture_status", "words"}
        if not required.issubset(reader.fieldnames or []):
            raise SystemExit(f"input missing columns: {sorted(required - set(reader.fieldnames or []))}")
        for row in reader:
            if row["variant"] != "H6" or row["capture_status"] != "PASS":
                continue
            attempt = int(row["attempt"])
            frame = int(row["frame"])
            if frame in FRAMES:
                values[(attempt, frame)] = parse_rng(row["words"])

    expected = {(attempt, frame) for attempt in (1, 2) for frame in FRAMES}
    missing = expected - set(values)
    if missing:
        raise SystemExit(f"missing H6 RNG captures: {sorted(missing)}")

    rows = []
    for attempt in (1, 2):
        for before_frame, after_frame in zip(FRAMES, FRAMES[1:]):
            before = values[(attempt, before_frame)]
            after = values[(attempt, after_frame)]
            k = find_k(before, after, args.max_k)
            rows.append({
                "variant": "H6",
                "attempt": attempt,
                "from_frame": before_frame,
                "to_frame": after_frame,
                "rng_before": f"0x{before:08X}",
                "rng_after": f"0x{after:08X}",
                "k": "tidak ditemukan" if k is None else k,
                "max_k": args.max_k,
                "interpretation": "state sama; k minimum 0, tidak menyimpulkan arti gameplay",
            })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
