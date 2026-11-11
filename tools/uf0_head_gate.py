#!/usr/bin/env python3
"""UF0: strict, metadata-only byte-union gate over tracked TSVs in the checked-out HEAD."""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

BASELINE = "9a6ccb7969a8cf377006dba01f468fb2c9dc4b05"
BYTE_COLUMNS = (
    "bytes",
    "instruction_bytes",
    "bytes_or_excerpt_hex",
    "bytes_excerpt_hex_max64",
    "contiguous_bytes",
)
LEGACY_COLUMNS = ("bytes", "instruction_bytes")
PC_COLUMNS = ("pc", "instruction_pc", "address", "virtual_address", "start_pc")
OFFSET_COLUMNS = ("file_offset", "offset", "start_offset", "byte_offset")
IMAGE_COLUMNS = (
    "image", "region", "source_image", "image_name", "binary", "binary_name",
    "module", "section_image", "entry", "entry_name", "segment", "segment_image",
    "section", "executable", "rom_image", "image_id", "source_entry",
)
PATH_COLUMNS = (
    "source_file", "file", "filename", "path", "file_path", "binary_path",
    "image_path", "module_path", "rom_path", "source",
)
UNKNOWN = {"", "TIDAK TAHU", "TIDAK_TAHU", "UNKNOWN", "N/A", "NA", "NONE", "NULL", "-"}
RANGES = {
    "EXE": (0x800, 385024, 0x80010000, 385024),
    "ENTRY0": (0x5F800, 110536, 0x800AD000, 110536),
    "ENTRY1": (0x10BB000, 596412, 0x800AD450, 596412),
}
HISTORICAL_RESULT_NUMBERS = {
    "UNRESOLVED_GROUPS_TOTAL": 238660,
    "BYTE_CONFLICTS": 50062,
    "NO_PC_ROWS": 321267,
    "MALFORMED_SOURCE_FIELD_PAIRS": 210,
}


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (value or "").strip().lower()).strip("_")


def parse_address(value: str | None) -> int | None:
    text = (value or "").strip()
    if not text or text.upper() in UNKNOWN:
        return None
    if text.lower().startswith("0x"):
        text = text[2:]
    if not re.fullmatch(r"[0-9a-fA-F]+", text):
        return None
    return int(text, 16)


def parse_byte_cell(value: str | None, column: str) -> tuple[bytes | None, str]:
    text = (value or "").strip()
    if not text or text.upper() in UNKNOWN:
        return None, "UNKNOWN"
    # This column is often a decimal byte-count, not an excerpt. Never treat
    # digit-only lengths as hexadecimal byte payloads.
    if column == "contiguous_bytes" and re.fullmatch(r"[0-9]+", text):
        return None, "DECIMAL_LENGTH_NOT_BYTES"
    tokens = [part for part in re.split(r"[\s,;|]+", text) if part]
    output = bytearray()
    for token in tokens:
        item = token[2:] if token.lower().startswith("0x") else token
        if not item or not re.fullmatch(r"[0-9a-fA-F]+", item) or len(item) % 2:
            return None, "MALFORMED"
        output.extend(int(item[index:index + 2], 16) for index in range(0, len(item), 2))
    if not output:
        return None, "UNKNOWN"
    return bytes(output), "OK"


def image_label(value: str | None) -> str | None:
    raw = (value or "").strip()
    if not raw or raw.upper() in UNKNOWN:
        return None
    compact = re.sub(r"[^A-Z0-9]", "", raw.upper())
    if "ENTRY0" in compact or "DATA0" in compact or compact == "E0":
        return "ENTRY0"
    if "ENTRY1" in compact or "DATA1" in compact or compact == "E1":
        return "ENTRY1"
    if "SLPS03553" in compact or compact in {"EXE", "MAINEXE"}:
        return "EXE"
    return "IMAGE:" + compact[:80]


def range_label(value: int | None, index: int) -> str | None:
    if value is None:
        return None
    for label, (file_start, file_size, pc_start, pc_size) in RANGES.items():
        start, size = (file_start, file_size) if index == 0 else (pc_start, pc_size)
        if start <= value < start + size:
            return label
    return None


def infer_label(row: dict[str, str], header_map: dict[str, str], source: str,
                pc: int | None, file_offset: int | None) -> str:
    explicit = set()
    for column in IMAGE_COLUMNS:
        if column in header_map:
            found = image_label(row.get(header_map[column], ""))
            if found:
                explicit.add(found)
    if len(explicit) == 1:
        return next(iter(explicit))
    if len(explicit) > 1:
        return "UNRESOLVED:CONFLICTING_IMAGE_METADATA"

    path_values = [source]
    for column in PATH_COLUMNS:
        if column in header_map:
            value = (row.get(header_map[column]) or "").strip()
            if value and value.upper() not in UNKNOWN:
                path_values.append(value)
    path_labels = set()
    for value in path_values:
        found = image_label(value)
        if found in {"ENTRY0", "ENTRY1", "EXE"}:
            path_labels.add(found)
        upper = value.upper()
        if re.search(r"ENTRY[_ -]?0|DATA[_ -]?0", upper):
            path_labels.add("ENTRY0")
        if re.search(r"ENTRY[_ -]?1|DATA[_ -]?1", upper):
            path_labels.add("ENTRY1")
        if "SLPS_035.53" in upper or "MAIN_EXE" in upper or "/EXE/" in upper:
            path_labels.add("EXE")
    if len(path_labels) == 1:
        return next(iter(path_labels))
    if len(path_labels) > 1:
        return "UNRESOLVED:CONFLICTING_PATH_METADATA"

    offset_label = range_label(file_offset, 0)
    if offset_label:
        return offset_label
    pc_label = range_label(pc, 1)
    if pc_label:
        return pc_label
    if file_offset is not None:
        return "UNRESOLVED:FILE_OFFSET_OUTSIDE_KNOWN_IMAGES"
    if pc is not None:
        return "UNRESOLVED:PC_OUTSIDE_KNOWN_IMAGES"
    return "UNRESOLVED:NO_IMAGE_OR_ADDRESS_CONTEXT"


def tracked_tsv(root: Path) -> list[str]:
    raw = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"])
    return sorted(
        path for path in raw.decode("utf-8", "replace").split("\0")
        if path and path.lower().endswith(".tsv")
    )


def source_ref_text(ref: tuple[str, int, int, str]) -> str:
    return f"{ref[0]}:{ref[1]}-{ref[2]}:{ref[3]}"


def scan(root: Path, selected_columns: tuple[str, ...] = BYTE_COLUMNS,
         conflict_sample_limit: int = 10) -> dict:
    files = tracked_tsv(root)
    maps: dict = defaultdict(dict)
    origins: dict = defaultdict(lambda: defaultdict(set))
    no_pc_groups = []
    malformed = Counter()
    malformed_samples = defaultdict(list)
    field_counts = Counter()
    valid_counts = Counter()
    unknown_counts = Counter()
    decimal_counts = Counter()
    manifest = []
    conflicts = 0
    conflict_samples = []
    eligible_files = 0

    for relative in files:
        path = root / relative
        try:
            with path.open("r", encoding="utf-8-sig", newline="") as stream:
                reader = csv.DictReader(stream, delimiter="\t")
                if not reader.fieldnames:
                    continue
                header_map = {norm(name): name for name in reader.fieldnames if name}
                byte_fields = [(name, header_map[name]) for name in selected_columns if name in header_map]
                if not byte_fields:
                    continue
                eligible_files += 1
                pc_column = next((header_map[name] for name in PC_COLUMNS if name in header_map), None)
                offset_column = next((header_map[name] for name in OFFSET_COLUMNS if name in header_map), None)
                previous_line = reader.line_num
                rows_seen = 0
                for row in reader:
                    row_start = previous_line + 1
                    row_end = reader.line_num
                    previous_line = row_end
                    rows_seen += 1
                    pc = parse_address(row.get(pc_column, "")) if pc_column else None
                    file_offset = parse_address(row.get(offset_column, "")) if offset_column else None
                    label = infer_label(row, header_map, relative, pc, file_offset)
                    for column, original_column in byte_fields:
                        field_counts[column] += 1
                        data, status = parse_byte_cell(row.get(original_column, ""), column)
                        if status == "UNKNOWN":
                            unknown_counts[column] += 1
                            continue
                        if status == "DECIMAL_LENGTH_NOT_BYTES":
                            decimal_counts[column] += 1
                            continue
                        if status == "MALFORMED":
                            malformed[(relative, column)] += 1
                            if len(malformed_samples[(relative, column)]) < 3:
                                malformed_samples[(relative, column)].append(row_start)
                            continue
                        if data is None:
                            continue
                        valid_counts[column] += 1
                        origin = (relative, row_start, row_end, column)
                        if pc is not None:
                            kind, base = "PC", pc
                        elif file_offset is not None:
                            kind, base = "FILE_OFFSET", file_offset
                        else:
                            no_pc_groups.append({
                                "label": label, "kind": "NO_PC", "start": None,
                                "byte_count": len(data), "origin": origin,
                                "sources": {relative}, "fields": {column},
                                "_over_refs": {origin},
                            })
                            continue
                        identity = relative if label.startswith("UNRESOLVED:") else ""
                        key = (label, kind, identity)
                        for displacement, byte_value in enumerate(data):
                            address = base + displacement
                            old_value = maps[key].get(address)
                            if old_value is not None and old_value != byte_value:
                                conflicts += 1
                                if len(conflict_samples) < conflict_sample_limit:
                                    old_refs = sorted(origins[key][address])
                                    conflict_samples.append({
                                        "label": label, "kind": kind, "address": f"0x{address:08X}",
                                        "source_a": source_ref_text(old_refs[0]) if old_refs else "TIDAK TAHU",
                                        "source_b": source_ref_text(origin),
                                        "reason": "same label/address has differing strict-hex values; no version/authority field selects one",
                                    })
                            elif old_value is None:
                                maps[key][address] = byte_value
                            origins[key][address].add(origin)
                manifest.append({
                    "source": relative,
                    "byte_columns": ";".join(column for column, _ in byte_fields),
                    "pc_column": pc_column or "NONE",
                    "file_offset_column": offset_column or "NONE",
                    "rows": rows_seen,
                })
        except (OSError, UnicodeError, csv.Error):
            malformed[(relative, "FILE_READ")] += 1
            if len(malformed_samples[(relative, "FILE_READ")]) < 3:
                malformed_samples[(relative, "FILE_READ")].append(0)

    groups = []
    for key, address_map in maps.items():
        label, kind, _identity = key
        addresses = sorted(address_map)
        if not addresses:
            continue
        start = previous = addresses[0]

        def emit(first: int, last: int) -> None:
            refs = set()
            over_refs = set()
            unique_sources = set()
            unique_fields = set()
            for address in range(first, last + 1):
                current_refs = origins[key][address]
                refs.update(current_refs)
                if address >= first + 64:
                    over_refs.update(current_refs)
            unique_sources.update(ref[0] for ref in refs)
            unique_fields.update(ref[3] for ref in refs)
            groups.append({
                "label": label, "kind": kind, "start": first,
                "end_exclusive": last + 1, "byte_count": last - first + 1,
                "source_count": len(unique_sources), "source_rows_count": len(refs),
                "sources_sample": ";".join(sorted(unique_sources)[:3]),
                "fields_sample": ";".join(sorted(unique_fields)[:5]),
                "_over_refs": over_refs,
            })

        for address in addresses[1:]:
            if address != previous + 1:
                emit(start, previous)
                start = address
            previous = address
        emit(start, previous)

    groups.extend(no_pc_groups)
    groups.sort(key=lambda group: (
        group["label"], group["kind"], group["start"] if group["start"] is not None else -1,
        group.get("sources_sample", ""),
    ))
    return {
        "files": files, "groups": groups, "malformed": malformed,
        "malformed_samples": malformed_samples, "field_counts": field_counts,
        "valid_counts": valid_counts, "unknown_counts": unknown_counts,
        "decimal_counts": decimal_counts, "manifest": manifest,
        "conflicts": conflicts, "conflict_samples": conflict_samples,
        "eligible_files": eligible_files,
        "no_pc_rows": len({(item["origin"][0], item["origin"][1], item["origin"][2]) for item in no_pc_groups}),
        "no_pc_byte_cells": len(no_pc_groups),
        "unique_address_bytes": sum(len(addresses) for addresses in maps.values()),
    }


def labelled_pc_over64(result: dict) -> int:
    return sum(
        1 for group in result["groups"]
        if group["kind"] == "PC" and not group["label"].startswith("UNRESOLVED:")
        and group["byte_count"] > 64
    )


def over64_groups(result: dict) -> list[dict]:
    return [group for group in result["groups"] if group["byte_count"] > 64]


def row_drop_targets(groups: list[dict]) -> dict[tuple[str, int, int], list[dict]]:
    targets = defaultdict(list)
    for group in groups:
        for ref in group.get("_over_refs", set()):
            targets[(ref[0], ref[1], ref[2])].append(group)
    return targets


def trim_source_rows(root: Path, targets: dict) -> list[dict]:
    by_file = defaultdict(list)
    for (source, line_start, line_end), reasons in targets.items():
        by_file[source].append((line_start, line_end, reasons))
    report = []
    for source, ranges in sorted(by_file.items()):
        path = root / source
        raw = path.read_bytes()
        has_bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig")
        lines = text.splitlines(keepends=True)
        drop_lines = set()
        for line_start, line_end, reasons in ranges:
            drop_lines.update(range(line_start, line_end + 1))
            for group in reasons:
                report.append({
                    "source": source, "line_start": line_start, "line_end": line_end,
                    "label": group["label"], "kind": group["kind"],
                    "group_start": f"0x{group['start']:08X}" if group["start"] is not None else "TIDAK TAHU",
                    "group_bytes": group["byte_count"],
                    "reason": "source row contributes bytes beyond first 64 bytes of an oversized group",
                })
        kept_text = "".join(line for number, line in enumerate(lines, start=1) if number not in drop_lines)
        path.write_bytes((b"\xef\xbb\xbf" if has_bom else b"") + kept_text.encode("utf-8"))
    return report


def write_tsv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=fields, delimiter="\t", extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def public_group(group: dict) -> dict:
    return {key: value for key, value in group.items() if not key.startswith("_")}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--baseline-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--baseline", default=BASELINE)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    baseline_root = Path(args.baseline_root).resolve()
    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)

    baseline_legacy = scan(baseline_root, LEGACY_COLUMNS, conflict_sample_limit=0)
    baseline_expanded = scan(baseline_root, BYTE_COLUMNS, conflict_sample_limit=0)
    current_initial = scan(root)
    initial_over = over64_groups(current_initial)
    over_rows = [public_group(group) for group in initial_over]

    trim_report = []
    current = current_initial
    for _pass in range(3):
        oversized = over64_groups(current)
        if not oversized:
            break
        targets = row_drop_targets(oversized)
        if not targets:
            break
        trim_report.extend(trim_source_rows(root, targets))
        current = scan(root)

    final_over = over64_groups(current)
    files_unchanged = set(current_initial["files"]) == set(current["files"])
    unresolved_initial = sum(
        1 for group in current_initial["groups"] if group["label"].startswith("UNRESOLVED:")
    )
    unresolved_total = sum(
        1 for group in current["groups"] if group["label"].startswith("UNRESOLVED:")
    )
    malformed_cells = sum(current_initial["malformed"].values())
    label_counts = Counter(group["label"] for group in current["groups"])
    label_unique_bytes = Counter()
    for group in current["groups"]:
        label_unique_bytes[group["label"]] += group["byte_count"]

    write_tsv(
        output / "UF0_OVER64_GROUPS.tsv",
        ["label", "kind", "start", "end_exclusive", "byte_count", "source_count",
         "source_rows_count", "sources_sample", "fields_sample"],
        over_rows,
    )
    write_tsv(
        output / "UF0_TRIMMED_ROWS.tsv",
        ["source", "line_start", "line_end", "label", "kind", "group_start", "group_bytes", "reason"],
        trim_report,
    )
    write_tsv(
        output / "UF0_BYTE_CONFLICTS_SAMPLE.tsv",
        ["label", "kind", "address", "source_a", "source_b", "reason"],
        current_initial["conflict_samples"],
    )
    label_rows = [
        {"label": label, "groups_after_prune": count,
         "unique_or_record_bytes_after_prune": label_unique_bytes[label],
         "unresolved": "YES" if label.startswith("UNRESOLVED:") else "NO"}
        for label, count in sorted(label_counts.items())
    ]
    write_tsv(
        output / "UF0_LABEL_COUNTS.tsv",
        ["label", "groups_after_prune", "unique_or_record_bytes_after_prune", "unresolved"],
        label_rows,
    )
    write_tsv(
        output / "UF0_SOURCE_MANIFEST.tsv",
        ["source", "byte_columns", "pc_column", "file_offset_column", "rows"],
        current_initial["manifest"],
    )

    legacy_count = labelled_pc_over64(baseline_legacy)
    expanded_count = labelled_pc_over64(baseline_expanded)
    reconciliation = legacy_count == 18 and expanded_count == 31
    summary = [
        "UF0_HEAD_DIRECT_TSV_UNION_GATE",
        f"HEAD_SOURCE={subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()}",
        f"BASELINE_RECONCILIATION_COMMIT={args.baseline}",
        f"HEAD_TRACKED_TSV_FILES={len(current_initial['files'])}",
        f"HEAD_ELIGIBLE_BYTE_TSV_FILES={current_initial['eligible_files']}",
        "BYTE_COLUMNS=bytes;instruction_bytes;bytes_or_excerpt_hex;bytes_excerpt_hex_max64;contiguous_bytes",
        f"CONTIGUOUS_BYTES_DECIMAL_CELLS_SKIPPED={sum(current_initial['decimal_counts'].values())}",
        f"HEAD_INITIAL_GROUPS={len(current_initial['groups'])}",
        f"HEAD_INITIAL_GROUPS_OVER_64B={len(initial_over)}",
        f"HEAD_UNIQUE_SOURCE_ROWS_TRIMMED={len({(row['source'],row['line_start'],row['line_end']) for row in trim_report})}",
        f"HEAD_ROW_TO_OVERSIZED_GROUP_ASSOCIATIONS={len(trim_report)}",
        f"HEAD_FILES_WITH_ROWS_TRIMMED={len({row['source'] for row in trim_report})}",
        f"HEAD_POST_PRUNE_GROUPS_OVER_64B={len(final_over)}",
        f"HEAD_UNRESOLVED_GROUPS_INITIAL={unresolved_initial}",
        f"HEAD_UNRESOLVED_GROUPS_AFTER_PRUNE={unresolved_total}",
        f"HEAD_BYTE_CONFLICTS_INITIAL={current_initial['conflicts']}",
        f"HEAD_NO_PC_SOURCE_ROWS_INITIAL={current_initial['no_pc_rows']}",
        f"HEAD_NO_PC_BYTE_CELLS_INITIAL={current_initial['no_pc_byte_cells']}",
        f"HEAD_MALFORMED_BYTE_CELLS_INITIAL={malformed_cells}",
        f"HEAD_MALFORMED_SOURCE_FIELD_PAIRS_INITIAL={len(current_initial['malformed'])}",
        f"HEAD_UNIQUE_ADDRESS_BYTES_AFTER_PRUNE={current['unique_address_bytes']}",
        f"BASELINE_9A6_LEGACY_COLUMNS_LABELED_PC_GROUPS_OVER_64B={legacy_count}",
        f"BASELINE_9A6_EXPANDED_COLUMNS_LABELED_PC_GROUPS_OVER_64B={expanded_count}",
        f"BASELINE_18_VS_31_RECONCILIATION={'PASS' if reconciliation else 'NOT_RECONCILED'}",
        f"BASELINE_RECONCILIATION_DELTA={expanded_count - legacy_count}",
        "GROUP_RULE=union by image label, coordinate kind, and contiguous address; unresolved groups isolated per source TSV",
        "ADDRESS_RULE=PC if present; else file_offset; else each valid no-PC byte cell is its own group",
        "HEX_RULE=strict even-length hex only; TIDAK TAHU/UNKNOWN/N/A/NA/NONE/NULL/- are not bytes",
        "CONTIGUOUS_BYTES_RULE=digit-only decimal cells are counts, not bytes; other values must pass strict hex parser",
        "CONFLICT_RULE=count each overlapping coordinate where observed strict-hex values differ; never select a winner",
        "CONFLICT_CAUSE=same image/address is represented by inconsistent TSV rows or byte fields; no version/authority field resolves precedence",
        "CONFLICT_SAMPLE=UF0_BYTE_CONFLICTS_SAMPLE.tsv contains metadata only; no byte values",
        "OVERSIZED_REGISTRY=UF0_OVER64_GROUPS.tsv contains every initial >64-byte group as metadata only",
        "TRIM_REGISTRY=UF0_TRIMMED_ROWS.tsv records each source row removed; no bytes emitted",
        "UNION_PUBLICATION=compact label counts and metadata only; full union omitted",
        "FILE_POLICY=no files deleted; tracked TSV path set unchanged",
        f"HISTORICAL_RESULTS_UNRESOLVED_GROUPS_TOTAL={HISTORICAL_RESULT_NUMBERS['UNRESOLVED_GROUPS_TOTAL']}",
        f"UNRESOLVED_GROUPS_DELTA_VS_HISTORICAL={unresolved_initial-HISTORICAL_RESULT_NUMBERS['UNRESOLVED_GROUPS_TOTAL']}",
        f"HISTORICAL_RESULTS_BYTE_CONFLICTS={HISTORICAL_RESULT_NUMBERS['BYTE_CONFLICTS']}",
        f"BYTE_CONFLICTS_DELTA_VS_HISTORICAL={current_initial['conflicts']-HISTORICAL_RESULT_NUMBERS['BYTE_CONFLICTS']}",
        f"HISTORICAL_RESULTS_NO_PC_ROWS={HISTORICAL_RESULT_NUMBERS['NO_PC_ROWS']}",
        f"NO_PC_BYTE_CELLS_DELTA_VS_HISTORICAL={current_initial['no_pc_byte_cells']-HISTORICAL_RESULT_NUMBERS['NO_PC_ROWS']}",
        f"HISTORICAL_RESULTS_MALFORMED_SOURCE_FIELD_PAIRS={HISTORICAL_RESULT_NUMBERS['MALFORMED_SOURCE_FIELD_PAIRS']}",
        f"MALFORMED_SOURCE_FIELD_PAIRS_DELTA_VS_HISTORICAL={len(current_initial['malformed'])-HISTORICAL_RESULT_NUMBERS['MALFORMED_SOURCE_FIELD_PAIRS']}",
        "HISTORICAL_COMPARISON_RULE=compare using matching metric definitions; deltas are descriptive until historical parser semantics are reproduced byte-for-byte",
        "UNRESOLVED_METRIC=initial union groups with unresolved image label; key includes source TSV identity",
        "BYTE_CONFLICT_METRIC=per labelled coordinate with a differing strict-hex value encountered; no winner is chosen",
        "NO_PC_METRICS=source TSV rows and byte-field cells without PC or file_offset are counted separately",
        "MALFORMED_METRICS=malformed byte cells and distinct source-file/byte-column pairs with at least one malformed cell are counted separately",
        f"TRACKED_TSV_PATH_SET_UNCHANGED={str(files_unchanged).upper()}",
        "NO_TSV_FILES_DELETED=YES",
        f"STATUS={'PASS' if not final_over and files_unchanged and reconciliation else 'FAIL'}",
        f"EXIT_CODE={0 if not final_over and files_unchanged and reconciliation else 1}",
    ]
    (output / "UF0_SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    return 0 if not final_over and files_unchanged and reconciliation else 1


if __name__ == "__main__":
    raise SystemExit(main())
