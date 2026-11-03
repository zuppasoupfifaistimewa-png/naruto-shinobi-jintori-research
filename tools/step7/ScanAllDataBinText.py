#!/usr/bin/env python3
"""Read-only text-resource census across every DATA.BIN directory entry.

Only text/TSV results are emitted. The source DATA.BIN is verified by size and
SHA-256 before scanning. No source bytes are copied into the report.
"""
from __future__ import annotations
import argparse
import csv
import gzip
import hashlib
import struct
import zlib
from pathlib import Path

EXPECTED_SIZE = 66015232
EXPECTED_SHA256 = "69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
TABLE_OFFSET = 0x44
ENTRY_COUNT = 1504
ENTRY_STRIDE = 8
BASE_LBN = 212
PHRASES = (
    "結界開放", "結界解放", "結界解除", "結界", "チャクラ", "バリア",
    "障壁", "開放", "解放", "解除", "強化", "建設", "建築", "増築", "領地", "防御", "攻撃", "護り", "守り",
    "消費", "費用", "料金", "価格", "所持", "所有", "増加", "獲得",
    "Barrier", "Chakra", "release", "upgrade", "build", "cost",
)
HINTS = ("結界", "チャクラ", "バリア", "障壁", "開放", "解放", "解除",
         "強化", "建設", "建築", "消費", "費用", "料金", "価格", "所持", "所有", "領地", "防御", "攻撃", "護り", "守り",
         "増加", "獲得", "Barrier", "Chakra", "release", "upgrade", "build", "cost")
MAX_RETAINED_MATCHES = 10000
MAX_DECOMPRESSED = 8 * 1024 * 1024

def digest(buf: bytes) -> str:
    return hashlib.sha256(buf).hexdigest()

def clean(text: str) -> str:
    return text.replace("\\", "\\\\").replace("\t", " ").replace("\r", " ").replace("\n", " ").replace("|", "/")

def sjis_runs(buf: bytes):
    """Yield (offset, raw_bytes, decoded_text) for plausible Shift-JIS runs."""
    i = 0
    while i < len(buf):
        start = i
        raw = bytearray()
        pairs = 0
        while i < len(buf):
            b = buf[i]
            if 0x20 <= b <= 0x7e or 0xa1 <= b <= 0xdf:
                raw.append(b)
                i += 1
                continue
            if (0x81 <= b <= 0x9f or 0xe0 <= b <= 0xef) and i + 1 < len(buf):
                t = buf[i + 1]
                if 0x40 <= t <= 0xfc and t != 0x7f:
                    raw.extend((b, t))
                    pairs += 1
                    i += 2
                    continue
            break
        if pairs >= 3:
            try:
                decoded = bytes(raw).decode("shift_jis", errors="strict")
            except UnicodeDecodeError:
                decoded = bytes(raw).decode("shift_jis", errors="replace")
            if any(ord(ch) > 127 for ch in decoded):
                yield start, bytes(raw), decoded
        if i == start:
            i += 1

def decoded_variants(chunk: bytes):
    yield "RAW", chunk
    # Try only identifiable zlib/gzip headers; unsupported/custom LZ formats stay unknown.
    if chunk.startswith(b"\x1f\x8b"):
        try:
            out = gzip.decompress(chunk)
            if len(out) <= MAX_DECOMPRESSED:
                yield "GZIP", out
        except Exception:
            pass
    if len(chunk) >= 2 and chunk[0] == 0x78 and ((chunk[0] << 8) | chunk[1]) % 31 == 0:
        try:
            out = zlib.decompress(chunk)
            if len(out) <= MAX_DECOMPRESSED:
                yield "ZLIB", out
        except Exception:
            pass

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--tsv", required=True)
    args = ap.parse_args()

    data = Path(args.data).read_bytes()
    actual_sha = digest(data)
    if len(data) != EXPECTED_SIZE or actual_sha != EXPECTED_SHA256:
        raise SystemExit(f"DATA.BIN identity mismatch bytes={len(data)} sha256={actual_sha}")
    table_end = TABLE_OFFSET + ENTRY_COUNT * ENTRY_STRIDE
    if table_end > len(data):
        raise SystemExit("directory table exceeds DATA.BIN")

    entries = [struct.unpack_from("<II", data, TABLE_OFFSET + i * ENTRY_STRIDE)
               for i in range(ENTRY_COUNT)]
    phrase_bytes = []
    for phrase in PHRASES:
        encodings = set()
        for codec in ("ascii", "shift_jis"):
            try:
                encodings.add(phrase.encode(codec))
            except UnicodeEncodeError:
                pass
        for needle in encodings:
            phrase_bytes.append((phrase, needle))

    report = [
        "# BB2 — full DATA.BIN text-resource census",
        "",
        f"DATA.BIN bytes={len(data)}",
        f"DATA.BIN SHA256={actual_sha}",
        f"directory_table_offset=0x{TABLE_OFFSET:X}",
        f"directory_entries={ENTRY_COUNT}",
        "directory_entry_format=<u32 LBN, u32 byte_length>; source LBN base=212; sector=2048 bytes",
        "scope=all valid non-empty directory entries; raw Shift-JIS/ASCII phrase search plus full uncapped heuristic Shift-JIS candidate scan",
        "decompression=only standard gzip and zlib signatures; custom LZ/other containers are not decoded",
        "result=static byte scan only; candidate strings do not prove UI linkage or event identity",
        "",
        "| Metric | Count |",
        "|---|---:|",
    ]
    tsv_path = Path(args.tsv)
    tsv_path.parent.mkdir(parents=True, exist_ok=True)
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ("record_type", "entry_index", "lbn", "entry_offset", "entry_length",
                  "entry_sha256", "variant", "offset_in_variant", "data_bin_offset",
                  "matched_phrase", "text", "bytes_hex", "note")
    totals = {"active": 0, "invalid": 0, "phrase_hits": 0, "sjis_runs": 0,
              "matched_sjis_runs": 0, "compressed_variants": 0, "retained_match_rows": 0}
    rows = []
    entry_summary = []

    for idx, (lbn, length) in enumerate(entries):
        if length == 0:
            continue
        offset = (lbn - BASE_LBN) * 2048
        if lbn < BASE_LBN or offset < 0 or offset + length > len(data):
            totals["invalid"] += 1
            entry_summary.append((idx, lbn, length, "INVALID_RANGE", ""))
            continue
        chunk = data[offset:offset + length]
        sha = digest(chunk)
        totals["active"] += 1
        entry_summary.append((idx, lbn, length, "VALID", sha))
        for phrase, needle in phrase_bytes:
            pos = 0
            while True:
                hit = chunk.find(needle, pos)
                if hit < 0:
                    break
                totals["phrase_hits"] += 1
                rows.append({
                    "record_type": "RAW_PHRASE", "entry_index": idx, "lbn": lbn,
                    "entry_offset": f"0x{offset:X}", "entry_length": length,
                    "entry_sha256": sha, "variant": "RAW", "offset_in_variant": f"0x{hit:X}",
                    "data_bin_offset": f"0x{offset+hit:X}", "matched_phrase": phrase,
                    "text": "", "bytes_hex": needle.hex(" "),
                    "note": "literal byte occurrence; context/UI use not established",
                })
                pos = hit + 1
        for variant, payload in decoded_variants(chunk):
            if variant != "RAW":
                totals["compressed_variants"] += 1
            for rel, raw, text_value in sjis_runs(payload):
                totals["sjis_runs"] += 1
                matching = [hint for hint in HINTS if hint.lower() in text_value.lower()]
                if matching:
                    totals["matched_sjis_runs"] += 1
                    if totals["retained_match_rows"] < MAX_RETAINED_MATCHES:
                        rows.append({
                            "record_type": "SJIS_RUN_MATCH", "entry_index": idx, "lbn": lbn,
                            "entry_offset": f"0x{offset:X}", "entry_length": length,
                            "entry_sha256": sha, "variant": variant, "offset_in_variant": f"0x{rel:X}",
                            "data_bin_offset": f"0x{offset+rel:X}" if variant == "RAW" else "NOT_APPLICABLE",
                            "matched_phrase": ";".join(matching),
                            "text": clean(text_value[:240]), "bytes_hex": raw[:80].hex(" "),
                            "note": "heuristic Shift-JIS run containing a search hint; not proven to be a UI string",
                        })
                        totals["retained_match_rows"] += 1
    
    report.extend([
        f"| Valid non-empty entries scanned | {totals['active']} |",
        f"| Invalid directory ranges skipped | {totals['invalid']} |",
        f"| Literal ASCII/Shift-JIS phrase occurrences | {totals['phrase_hits']} |",
        f"| Heuristic Shift-JIS candidate runs examined (uncapped) | {totals['sjis_runs']} |",
        f"| Matching Shift-JIS runs | {totals['matched_sjis_runs']} |",
        f"| Matching Shift-JIS rows retained | {totals['retained_match_rows']} |",
        
        f"| Standard compressed variants decoded | {totals['compressed_variants']} |",
        "",
        "## Per-entry inventory",
        "",
        "| Entry | LBN | Bytes | SHA-256 | Status |",
        "|---:|---:|---:|---|---|",
    ])
    for idx, lbn, length, status, sha in entry_summary:
        report.append(f"| {idx} | {lbn} | {length} | {sha or 'TIDAK TAHU'} | {status} |")
    report.extend([
        "",
        "## Interpretation boundary",
        "",
        "- A raw phrase hit is only an exact byte occurrence, not proof that the game renders it.",
        "- A Shift-JIS run is heuristic; binary data can accidentally decode as Japanese.",
        "- A zero hit does not exclude compressed resources, custom LZ, glyph-index text, or strings outside DATA.BIN.",
        "- No message ID (including 0xBE) is assigned to an entry unless a separate reference chain proves the mapping.",
    ])

    with tsv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("BB2_FULL_DATABIN_TEXT_SCAN=PASS "
          f"entries={totals['active']} invalid={totals['invalid']} "
          f"phrase_hits={totals['phrase_hits']} sjis_runs_examined={totals['sjis_runs']} "
          f"hint_runs={totals['matched_sjis_runs']} decoded_variants={totals['compressed_variants']}")

if __name__ == "__main__":
    main()
