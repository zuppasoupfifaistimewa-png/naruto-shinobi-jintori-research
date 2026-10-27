#!/usr/bin/env python3
"""Text-only resource signature/profile scan; heuristic data, not code proof."""
from __future__ import annotations
import collections
import hashlib
import math
import mmap
import statistics
import sys
from pathlib import Path

EXPECTED = {
    "SLPS_035.53": (385024, "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"),
    "DATA.BIN": (66015232, "69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"),
    "DATA2.BIN": (166428672, "be19071f293862e3e65975fa051a7a1a4528aeb3883d5cd74abfc268352ea5f9"),
    "DUMMY.BIN": (50667520, "cac5c852e95c90475a2879f51b6b949afea2df0cb540b2a2743bd791af4c47a2"),
    "XASECT.BIN": (692, "df257fbdabdb848f845466246abf4a36fdb6cf17815fc3a76ff7d7585d1953f0"),
}
SIGNATURES = {
    "PK02": b"PK02",
    "BIN0": b"BIN0",
    "TPK0": b"TPK0",
    "NARUTOSceneV001": b"NARUTOSceneV001",
    "NARU_prefix": b"NARU",
    "TIM_magic_candidate_10_00_00_00": bytes.fromhex("10000000"),
    "PS-X EXE": b"PS-X EXE",
    "VAGp": b"VAGp",
    "SEQp": b"SEQp",
    "SShd": b"SShd",
    "SSbd": b"SSbd",
    "STR_header": b"STR",
}

def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def entropy(sample: bytes) -> float:
    if not sample:
        return 0.0
    counts = collections.Counter(sample)
    n = len(sample)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())

def find_file(root: Path, name: str) -> Path:
    matches = [p for p in root.rglob("*") if p.is_file() and p.name.upper() == name.upper()]
    if len(matches) != 1:
        raise SystemExit(f"Expected exactly one {name}, found {len(matches)}")
    return matches[0]

def main() -> int:
    if len(sys.argv) != 3:
        print("usage: psx_resource_profile_scan.py EXTRACTED_ROOT OUTPUT_TXT", file=sys.stderr)
        return 2
    root, output = Path(sys.argv[1]), Path(sys.argv[2])
    lines = [
        "# PS1 resource profile scan (text only)",
        "method=whole-file signature counts plus sampled byte entropy",
        "emulator_or_gameplay_executed=no",
        "source_binary_uploaded_as_artifact=no",
        "interpretation_limit=signature/entropy hits are heuristics, not proof of executable code or absence of code",
        "private_source_cleanup_required=yes",
        "",
    ]
    for name in ("SLPS_035.53", "DATA.BIN", "DATA2.BIN", "DUMMY.BIN", "XASECT.BIN"):
        path = find_file(root, name)
        expected_size, expected_sha = EXPECTED[name]
        size = path.stat().st_size
        digest = sha256_path(path)
        if size != expected_size or digest != expected_sha:
            raise SystemExit(f"IDENTITY_MISMATCH {name} bytes={size} sha256={digest}")
        lines += [f"## {name}", f"bytes={size}", f"sha256={digest}", "identity=PASS"]
        sample_entropies = []
        with path.open("rb") as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as data:
            for off in range(0, size, 1024 * 1024):
                sample = data[off:off + min(8192, size - off)]
                if sample:
                    sample_entropies.append(entropy(sample))
            lines += ["entropy_sampling=first 8192 bytes of each 1 MiB stride; descriptive only",
                      f"entropy_sample_count={len(sample_entropies)}",
                      f"sample_entropy_min={min(sample_entropies):.4f}",
                      f"sample_entropy_median={statistics.median(sample_entropies):.4f}",
                      f"sample_entropy_max={max(sample_entropies):.4f}",
                      "signature_scan=whole file"]
            for label, sig in SIGNATURES.items():
                count, first_offsets = 0, []
                pos = 0
                while True:
                    pos = data.find(sig, pos)
                    if pos < 0:
                        break
                    count += 1
                    if len(first_offsets) < 12:
                        first_offsets.append(pos)
                    pos += 1
                offsets = ",".join(f"0x{x:X}" for x in first_offsets) if first_offsets else "none"
                lines.append(f"signature[{label}] count={count} first_offsets={offsets}")
        lines += [""]
    lines += [
        "## Interpretation guardrails",
        "- DATA2.BIN/DUMMY.BIN are not called executable or data-only from signature counts or entropy.",
        "- No known PS-X EXE/VAGp/SEQp/container signature is not proof of no executable code.",
        "- The existing RNG signature/direct-JAL scan is a separate narrow scan; its zero hits do not rule out different code, indirect dispatch, compressed/decompressed code or other RNGs.",
        "- XASECT.BIN is only 692 bytes and its table interpretation remains documented separately; this scan does not redefine its fields.",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PROFILE_REPORT={output}")
    print(f"PROFILE_FILES={sum(1 for line in lines if line.startswith('## ') and line != '## Interpretation guardrails')}")
    print(f"PRIVATE_SOURCE_BYTES_NOT_UPLOADED=yes")
    print(f"OUTPUT_BYTES={output.stat().st_size}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
