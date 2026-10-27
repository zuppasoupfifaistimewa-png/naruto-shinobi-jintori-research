#!/usr/bin/env python3
"""Static cross-resource scan for callers/references to the main-EXE RNG.

Scans only aligned words and narrow MIPS address-construction patterns. It does
not execute code, unpack private assets locally, or claim raw hits are code.
Prints a text-only report; all source binaries stay on the runner.
"""
from __future__ import annotations

import argparse
import hashlib
import struct
from pathlib import Path

RNG = 0x80035D78
SEED_SETTER = 0x80035DA8
RNG_STATE = 0x800A3118
MAIN_EXE_SHA = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
KNOWN = {
    "SLPS_035.53": (385024, MAIN_EXE_SHA),
    "DATA.BIN": (66015232, "69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"),
    "DATA2.BIN": (166428672, "be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9"),
    "DUMMY.BIN": (50667520, "cac5c852e95c90475a2879f51b6b949afea2df0cb540b2a2743bd791af4c47a2"),
    "XASECT.BIN": (692, "df257fbdabdb848f845466246abf4a36fdb6cf17815fc3a76ff7d7585d1953f0"),
    "SYSTEM.CNF": (68, "e5ffa72c5845508ae48b07140c712c9423ff6af733164b57628d1d9cece9ae71"),
}
DATA_BIN_DISC_LBN = 212
DATA_BIN_SECTOR_SIZE = 2048
DATA_BIN_TABLE_OFFSET = 0x44
DATA_BIN_ENTRY_COUNT = 1504


def u32(data: bytes, off: int) -> int:
    return struct.unpack_from("<I", data, off)[0]


def jal_word(target: int) -> int:
    """Encode MIPS JAL to a target in the same 256 MiB region."""
    return 0x0C000000 | ((target >> 2) & 0x03FFFFFF)


def all_aligned_occurrences(data: bytes, pattern: bytes) -> list[int]:
    hits: list[int] = []
    off = data.find(pattern)
    while off >= 0:
        if off % 4 == 0:
            hits.append(off)
        off = data.find(pattern, off + 1)
    return hits


def decode_data_bin_entries(data: bytes) -> list[tuple[int, int, int]]:
    """Return (index, file_start, raw_size) from the catalogued absolute LBNs."""
    if len(data) < DATA_BIN_TABLE_OFFSET + DATA_BIN_ENTRY_COUNT * 8:
        return []
    raw: list[tuple[int, int]] = []
    for i in range(DATA_BIN_ENTRY_COUNT):
        lbn, size = struct.unpack_from("<II", data, DATA_BIN_TABLE_OFFSET + i * 8)
        if size:
            raw.append((i, lbn, size))
    if not raw:
        return []
    # The audited catalogue treats the first field as absolute disc LBN. Verify
    # every resulting range remains inside DATA.BIN before using it for mapping.
    mapped: list[tuple[int, int, int]] = []
    for i, lbn, size in raw:
        start = (lbn - DATA_BIN_DISC_LBN) * DATA_BIN_SECTOR_SIZE
        if lbn < DATA_BIN_DISC_LBN or start < 0 or start + size > len(data):
            return []
        mapped.append((i, start, size))
    return mapped


def entry_for_offset(entries: list[tuple[int, int, int]], off: int) -> str:
    for index, start, size in entries:
        if start <= off < start + size:
            return f"entry={index} entry_offset=0x{off-start:X}"
    return "entry=NONE_OR_PADDING"


def mips_address_pairs(data: bytes, target: int, max_gap: int = 6) -> list[tuple[int, int, int | None]]:
    """Find LUI + (ORI/ADDIU) construction of target and nearby JALR.

    The returned offsets are byte offsets in the file, not runtime addresses.
    These are candidate patterns; disassembly/context is needed to validate them.
    """
    hi, lo = (target >> 16) & 0xFFFF, target & 0xFFFF
    # Search the low immediate as bytes first; this avoids a full Python loop
    # over every word in large data files.
    low_pattern = struct.pack("<H", lo)
    low_offsets = all_aligned_occurrences(data, low_pattern)
    out: list[tuple[int, int, int | None]] = []
    seen: set[tuple[int, int, int | None]] = set()
    for low_off in low_offsets:
        if low_off + 4 > len(data):
            continue
        low_word = u32(data, low_off)
        low_op = low_word >> 26
        low_rs = (low_word >> 21) & 0x1F
        low_rt = (low_word >> 16) & 0x1F
        if low_op not in (0x09, 0x0D):  # ADDIU or ORI
            continue
        # Address construction should use the LUI result as source register.
        for gap in range(1, max_gap + 1):
            lui_off = low_off - gap * 4
            if lui_off < 0:
                break
            lui_word = u32(data, lui_off)
            if (lui_word >> 26) != 0x0F or (lui_word & 0xFFFF) != hi:
                continue
            lui_rt = (lui_word >> 16) & 0x1F
            if low_rs != lui_rt:
                continue
            result_reg = low_rt
            jalr_off = None
            for j in range(1, 5):
                call_off = low_off + j * 4
                if call_off + 4 > len(data):
                    break
                w = u32(data, call_off)
                # SPECIAL/JALR: funct=9; rs is the jump target register.
                if (w >> 26) == 0 and (w & 0x3F) == 9 and ((w >> 21) & 0x1F) == result_reg:
                    jalr_off = call_off
                    break
            item = (lui_off, low_off, jalr_off)
            if item not in seen:
                seen.add(item)
                out.append(item)
    return sorted(out)


def mips_memory_pairs(data: bytes, target: int, max_gap: int = 6) -> list[tuple[int, int, int]]:
    """Find LUI + load/store of target; offsets refer to raw file bytes."""
    hi, lo = (target >> 16) & 0xFFFF, target & 0xFFFF
    low_offsets = all_aligned_occurrences(data, struct.pack("<H", lo))
    out: list[tuple[int, int, int]] = []
    seen: set[tuple[int, int, int]] = set()
    for mem_off in low_offsets:
        if mem_off + 4 > len(data):
            continue
        word = u32(data, mem_off)
        op = word >> 26
        # MIPS R3000A byte/halfword/word loads and stores.
        if op not in (0x20, 0x21, 0x23, 0x24, 0x25, 0x28, 0x29, 0x2B):
            continue
        base_reg = (word >> 21) & 0x1F
        for gap in range(1, max_gap + 1):
            lui_off = mem_off - gap * 4
            if lui_off < 0:
                break
            lui_word = u32(data, lui_off)
            if (lui_word >> 26) != 0x0F or (lui_word & 0xFFFF) != hi:
                continue
            lui_rt = (lui_word >> 16) & 0x1F
            if base_reg != lui_rt:
                continue
            item = (lui_off, mem_off, op)
            if item not in seen:
                seen.add(item)
                out.append(item)
    return sorted(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("files", nargs="+", type=Path)
    args = ap.parse_args()
    lines: list[str] = [
        "analysis=static raw-file scan for RNG/seed/state references",
        "rng_target=0x80035D78",
        "rng_state=0x800A3118",
        "seed_setter_candidate=0x80035DA8",
        f"direct_jal_rng_word=0x{jal_word(RNG):08X}",
        f"direct_jal_seed_setter_word=0x{jal_word(SEED_SETTER):08X}",
        "mapping=DATA.BIN directory indices only when LBN-derived intervals validate",
        "warning=Raw hits may be data/compressed bytes; only aligned MIPS code-context hits can be promoted after disassembly",
        "emulator_or_gameplay_executed=no",
        "binary_uploaded_as_artifact=no",
        "",
    ]
    totals = {"rng_jal": 0, "seed_jal": 0, "rng_literal": 0, "seed_literal": 0, "state_literal": 0, "rng_address_pair": 0, "seed_address_pair": 0, "state_address_pair": 0}
    for path in args.files:
        name = path.name.upper()
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        expected = KNOWN.get(name)
        valid = "not-listed"
        if expected:
            valid = "PASS" if (len(data) == expected[0] and digest == expected[1]) else "FAIL"
        lines.extend([
            f"=== FILE {path.name} ===",
            f"bytes={len(data)}",
            f"sha256={digest}",
            f"known_identity_check={valid}",
        ])
        if valid == "FAIL":
            lines.append("scan_status=REFUSED_IDENTITY_MISMATCH")
            lines.append("")
            continue
        entries = decode_data_bin_entries(data) if name == "DATA.BIN" else []
        if name == "DATA.BIN":
            lines.append(f"data_bin_validated_directory_entries={len(entries)}")
            if not entries:
                lines.append("data_bin_entry_mapping=UNAVAILABLE_DIRECTORY_RANGES_DID_NOT_VALIDATE")
        rng_jal = all_aligned_occurrences(data, struct.pack("<I", jal_word(RNG)))
        seed_jal = all_aligned_occurrences(data, struct.pack("<I", jal_word(SEED_SETTER)))
        rng_literal = all_aligned_occurrences(data, struct.pack("<I", RNG))
        seed_literal = all_aligned_occurrences(data, struct.pack("<I", SEED_SETTER))
        state_literal = all_aligned_occurrences(data, struct.pack("<I", RNG_STATE))
        rng_pairs = mips_address_pairs(data, RNG)
        seed_pairs = mips_address_pairs(data, SEED_SETTER)
        state_pairs = mips_address_pairs(data, RNG_STATE)
        state_memory_pairs = mips_memory_pairs(data, RNG_STATE)
        lines.append(f"direct_jal_rng_raw_hits={len(rng_jal)}")
        for off in rng_jal:
            extra = " " + entry_for_offset(entries, off) if name == "DATA.BIN" else ""
            lines.append(f"  direct_jal_rng file_offset=0x{off:X}{extra}")
        lines.append(f"direct_jal_seed_setter_raw_hits={len(seed_jal)}")
        for off in seed_jal:
            extra = " " + entry_for_offset(entries, off) if name == "DATA.BIN" else ""
            lines.append(f"  direct_jal_seed_candidate file_offset=0x{off:X}{extra}")
        lines.append(f"rng_address_literal_aligned_hits={len(rng_literal)}")
        for off in rng_literal[:100]:
            extra = " " + entry_for_offset(entries, off) if name == "DATA.BIN" else ""
            lines.append(f"  rng_literal file_offset=0x{off:X}{extra}")
        if len(rng_literal) > 100:
            lines.append("  rng_literal_output_truncated_after=100")
        lines.append(f"seed_setter_literal_aligned_hits={len(seed_literal)}")
        for off in seed_literal[:100]:
            extra = " " + entry_for_offset(entries, off) if name == "DATA.BIN" else ""
            lines.append(f"  seed_setter_literal file_offset=0x{off:X}{extra}")
        if len(seed_literal) > 100:
            lines.append("  seed_setter_literal_output_truncated_after=100")
        lines.append(f"rng_state_literal_aligned_hits={len(state_literal)}")
        for off in state_literal[:100]:
            extra = " " + entry_for_offset(entries, off) if name == "DATA.BIN" else ""
            lines.append(f"  rng_state_literal file_offset=0x{off:X}{extra}")
        if len(state_literal) > 100:
            lines.append("  rng_state_literal_output_truncated_after=100")
        lines.append(f"rng_lui_low_address_pairs={len(rng_pairs)}")
        for lui_off, low_off, jalr_off in rng_pairs[:100]:
            extra = " " + entry_for_offset(entries, lui_off) if name == "DATA.BIN" else ""
            call = f" jalr_file_offset=0x{jalr_off:X}" if jalr_off is not None else " jalr=NOT_WITHIN_4_FOLLOWING_WORDS"
            lines.append(f"  rng_addr_pair lui_file_offset=0x{lui_off:X} low_file_offset=0x{low_off:X}{call}{extra}")
        if len(rng_pairs) > 100:
            lines.append("  rng_addr_pair_output_truncated_after=100")
        lines.append(f"seed_setter_lui_low_address_pairs={len(seed_pairs)}")
        for lui_off, low_off, jalr_off in seed_pairs[:100]:
            extra = " " + entry_for_offset(entries, lui_off) if name == "DATA.BIN" else ""
            call = f" jalr_file_offset=0x{jalr_off:X}" if jalr_off is not None else " jalr=NOT_WITHIN_4_FOLLOWING_WORDS"
            lines.append(f"  seed_setter_addr_pair lui_file_offset=0x{lui_off:X} low_file_offset=0x{low_off:X}{call}{extra}")
        if len(seed_pairs) > 100:
            lines.append("  seed_setter_addr_pair_output_truncated_after=100")
        lines.append(f"rng_state_lui_low_address_pairs={len(state_pairs)}")
        for lui_off, low_off, jalr_off in state_pairs[:100]:
            extra = " " + entry_for_offset(entries, lui_off) if name == "DATA.BIN" else ""
            call = f" jalr_file_offset=0x{jalr_off:X}" if jalr_off is not None else " jalr=NOT_WITHIN_4_FOLLOWING_WORDS"
            lines.append(f"  rng_state_addr_pair lui_file_offset=0x{lui_off:X} low_file_offset=0x{low_off:X}{call}{extra}")
        if len(state_pairs) > 100:
            lines.append("  rng_state_addr_pair_output_truncated_after=100")
        lines.append(f"rng_state_lui_memory_access_pairs={len(state_memory_pairs)}")
        for lui_off, mem_off, op in state_memory_pairs[:200]:
            extra = " " + entry_for_offset(entries, lui_off) if name == "DATA.BIN" else ""
            lines.append(f"  rng_state_memory_pair lui_file_offset=0x{lui_off:X} access_file_offset=0x{mem_off:X} opcode=0x{op:02X}{extra}")
        if len(state_memory_pairs) > 200:
            lines.append("  rng_state_memory_pair_output_truncated_after=200")
        totals["rng_jal"] += len(rng_jal)
        totals["seed_jal"] += len(seed_jal)
        totals["rng_literal"] += len(rng_literal)
        totals["seed_literal"] += len(seed_literal)
        totals["state_literal"] += len(state_literal)
        totals["rng_address_pair"] += len(rng_pairs)
        totals["seed_address_pair"] += len(seed_pairs)
        totals["state_address_pair"] += len(state_pairs)
        lines.append("scan_status=COMPLETE")
        lines.append("")
    lines.extend([
        "=== TOTALS ===",
        *(f"{k}={v}" for k, v in totals.items()),
        "conclusion_boundary=absence of byte-pattern hits is not proof against computed pointers, indirect dispatch, compressed code, or unscanned/encoded formats",
        "",
    ])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(line for line in lines if line.startswith(("analysis=", "=== FILE", "bytes=", "sha256=", "known_identity_check=", "direct_jal_rng_raw_hits=", "direct_jal_seed_setter_raw_hits=", "rng_address_literal_aligned_hits=", "seed_setter_literal_aligned_hits=", "rng_state_literal_aligned_hits=", "rng_lui_low_address_pairs=", "seed_setter_lui_low_address_pairs=", "rng_state_lui_low_address_pairs=", "rng_state_lui_memory_access_pairs=", "=== TOTALS ===", "rng_jal=", "seed_jal=", "rng_literal=", "seed_literal=", "state_literal=", "rng_address_pair=", "seed_address_pair=", "state_address_pair="))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
