#!/usr/bin/env python3
"""Compare one DATA.BIN entry-1 function at a Ghidra-derived same-address boundary."""
from __future__ import annotations
import argparse
import hashlib
import re
import subprocess
from pathlib import Path

EXPECTED_BYTES = 596_412
EXPECTED_SHA256 = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
ENTRY = 0x800ED8C8
EXPECTED_SIZE = 160
EXPECTED_END = ENTRY + EXPECTED_SIZE
RNG_CALLSITE = 0x800ED8E4
RNG_TARGET = 0x80035D78

def run_cmd(command: list[str], timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False, timeout=timeout)

def parse_hex_value(report: str, key: str) -> int | None:
    match = re.search(rf"(?m)^{re.escape(key)}=(?:0x)?([0-9a-fA-F]+)\s*$", report)
    return int(match.group(1), 16) if match else None

def parse_decimal_value(report: str, key: str) -> int | None:
    match = re.search(rf"(?m)^{re.escape(key)}=(\d+)\s*$", report)
    return int(match.group(1), 10) if match else None

def find_label_for_addr(asm: str, address: int) -> str | None:
    wanted = f"{address:08x}"
    labels = re.findall(
        r"(?m)^\s*(?:glabel|\.globl|\.global|\.ent)\s+([A-Za-z_.$][\w.$]*)", asm
    )
    for label in labels:
        if any(h.lower() == wanted for h in re.findall(r"[0-9a-fA-F]{8}", label)):
            return label
    return None

def insert_boundary_label(asm: str, address: int, label: str) -> tuple[str, str | None]:
    existing = find_label_for_addr(asm, address)
    if existing:
        return asm, existing
    pattern = re.compile(
        rf"/\*\s*[0-9a-fA-F]+\s+{address:08X}\s+[0-9a-fA-F]+\s+\*/", re.IGNORECASE
    )
    lines = asm.splitlines()
    index = next((i for i, line in enumerate(lines) if pattern.search(line)), None)
    if index is None:
        return asm, None
    lines.insert(index, f"glabel {label} # inserted from Ghidra-verified boundary 0x{address:08X}")
    return "\n".join(lines) + "\n", label

def read_m2c_commit(path: Path) -> str:
    content = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"(?m)^m2c_commit=([0-9a-f]{40})\s*$", content)
    return match.group(1) if match else "UNRESOLVED"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resource", required=True)
    parser.add_argument("--ghidra-report", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--tool-versions", required=True)
    args = parser.parse_args()
    resource = Path(args.resource)
    ghidra_path = Path(args.ghidra_report)
    out = Path(args.out_dir)
    report_path = Path(args.report)
    out.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Step 5 — targeted Ghidra/m2c comparison for DATA.BIN entry 1",
        "",
        "scope=one selected candidate function only; not whole-resource coverage",
        "resource_mapping=HYPOTHESIS_ONLY_NOT_RUNTIME_VALIDATED",
        "game_or_emulator_executed=no",
        "gameplay_input_sent=no",
        "savestate_restored=no",
        "source_binary_committed=no",
        "source_binary_uploaded_as_artifact=no",
        "artifact_policy=text_only",
        f"target_function=0x{ENTRY:08X}",
        f"expected_function_body_bytes={EXPECTED_SIZE}",
        f"expected_function_end_exclusive=0x{EXPECTED_END:08X}",
        f"expected_rng_callsite=0x{RNG_CALLSITE:08X}",
        f"expected_rng_target=0x{RNG_TARGET:08X}",
        f"m2c_commit={read_m2c_commit(Path(args.tool_versions))}",
        "m2c_target=mips-ido-c (backend choice only; not an assertion about the original compiler)",
        "",
    ]
    data = resource.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    lines += [f"resource_bytes={len(data)}", f"resource_sha256={digest}"]
    if len(data) != EXPECTED_BYTES or digest != EXPECTED_SHA256:
        lines += ["status=FAILED", "error=DATA.BIN entry-1 size/hash mismatch"]
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return 0

    gtext = ghidra_path.read_text(encoding="utf-8", errors="replace")
    entry = parse_hex_value(gtext, "function_entry")
    size = parse_decimal_value(gtext, "function_body_bytes")
    end = parse_hex_value(gtext, "function_end_exclusive")
    call_direct = re.search(
        r"(?m)^rng_callsite_direct_flow_to_0x80035D78=yes\s*$", gtext, re.I
    ) is not None
    decompile_ok = re.search(r"(?m)^decompile_status=SUCCESS\s*$", gtext) is not None
    lines += [
        f"ghidra_function_entry={('0x%08X' % entry) if entry is not None else 'MISSING'}",
        f"ghidra_function_body_bytes={size if size is not None else 'MISSING'}",
        f"ghidra_function_end_exclusive={('0x%08X' % end) if end is not None else 'MISSING'}",
        f"ghidra_decompile_status={'SUCCESS' if decompile_ok else 'NOT_SUCCESS'}",
        f"ghidra_confirmed_direct_rng_call={str(call_direct).lower()}",
    ]
    boundary_ok = entry == ENTRY and size == EXPECTED_SIZE and end == EXPECTED_END
    lines.append(f"ghidra_boundary_matches_prior_validated_metadata={str(boundary_ok).lower()}")
    if not boundary_ok:
        lines += [
            "status=PARTIAL",
            "comparison_status=NOT_RUN",
            "reason=Ghidra did not expose the exact function entry/body boundary; no m2c equivalence claim",
        ]
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return 0

    asm_dir = out / "spimdisasm"
    asm_dir.mkdir(parents=True, exist_ok=True)
    dis_cmd = [
        "singleFileDisasm", str(resource), str(asm_dir),
        "--start", "0x0", "--end", "0x919BC", "--vram", "0x800D0000",
        "--endian", "little", "--compiler", "PSYQ", "--instr-category", "cpu",
        "--no-write-binary",
    ]
    dis = run_cmd(dis_cmd, timeout=240)
    (out / "spimdisasm.log").write_text(dis.stdout or "", encoding="utf-8")
    assembly_files = sorted(
        (p for p in asm_dir.rglob("*.s") if p.is_file()),
        key=lambda p: p.stat().st_size, reverse=True
    )
    lines += [f"spimdisasm_exit_code={dis.returncode}",
              f"spimdisasm_assembly_files={len(assembly_files)}"]
    if dis.returncode != 0 or not assembly_files:
        lines += ["status=PARTIAL", "comparison_status=NOT_RUN",
                  "reason=spimdisasm did not produce assembly"]
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return 0

    asm_path = assembly_files[0]
    asm = asm_path.read_text(encoding="utf-8", errors="replace")
    asm, start_label = insert_boundary_label(asm, ENTRY, f"func_{ENTRY:08x}")
    asm, end_label = insert_boundary_label(asm, EXPECTED_END, f"func_{EXPECTED_END:08x}")
    asm_path.write_text(asm, encoding="utf-8")
    lines += [
        f"assembly_file={asm_path.relative_to(out).as_posix()}",
        f"assembly_bytes={asm_path.stat().st_size}",
        f"m2c_start_label={start_label or 'NOT_FOUND'}",
        f"m2c_exclusive_end_label={end_label or 'NOT_FOUND'}",
    ]
    if not start_label or not end_label:
        lines += ["status=PARTIAL", "comparison_status=NOT_RUN",
                  "reason=could not bracket the function using the exact Ghidra body boundary"]
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return 0

    m2c_cmd = ["m2c", "--target", "mips-ido-c", "--function", start_label,
               "--no-cache", str(asm_path)]
    result = run_cmd(m2c_cmd, timeout=180)
    m2c_c = result.stdout or ""
    c_path = out / "m2c_800ed8c8.c"
    c_path.write_text(m2c_c, encoding="utf-8")
    (out / "m2c_800ed8c8.log").write_text(
        "command=" + " ".join(m2c_cmd) + "\nexit_code=" + str(result.returncode) + "\n" + m2c_c,
        encoding="utf-8"
    )
    ghidra_c_match = re.search(
        r"--- C_DECOMPILATION_BEGIN ---\s*(.*?)\s*--- C_DECOMPILATION_END ---",
        gtext, re.DOTALL
    )
    ghidra_c = ghidra_c_match.group(1).strip() + "\n" if ghidra_c_match else ""
    (out / "ghidra_800ed8c8.c").write_text(ghidra_c, encoding="utf-8")
    m2c_tokens = {x.lower().zfill(8) for x in re.findall(
        r"(?:func_|FUN_)(?:0x)?([0-9a-fA-F]{6,8})", m2c_c
    )}
    ghidra_tokens = {x.lower().zfill(8) for x in re.findall(
        r"(?:func_|FUN_)(?:0x)?([0-9a-fA-F]{6,8})", ghidra_c
    )}
    m2c_rng = "80035d78" in m2c_tokens or "80035d78" in m2c_c.lower()
    rng_shared = "80035d78" in ghidra_tokens and "80035d78" in m2c_tokens
    m2c_ok = result.returncode == 0 and bool(m2c_c.strip())
    comparison = "SUCCESS" if m2c_ok else "PARTIAL"
    lines += [
        f"m2c_exit_code={result.returncode}",
        f"m2c_output_nonempty={str(bool(m2c_c.strip())).lower()}",
        f"ghidra_c_lines={len(ghidra_c.splitlines())}",
        f"m2c_c_lines={len(m2c_c.splitlines())}",
        f"ghidra_call_tokens={','.join(sorted(ghidra_tokens)) or 'none'}",
        f"m2c_call_tokens={','.join(sorted(m2c_tokens)) or 'none'}",
        f"rng_call_token_visible_in_m2c={str(m2c_rng).lower()}",
        f"rng_call_token_shared_by_both_c_outputs={str(rng_shared).lower()}",
        f"comparison_status={comparison}",
        "status=" + ("SUCCESS" if m2c_ok and decompile_ok and call_direct else "PARTIAL"),
        "interpretation=matching same-address boundary and successful outputs are a structural cross-check, not original-source equivalence or proof of runtime resource loading",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
