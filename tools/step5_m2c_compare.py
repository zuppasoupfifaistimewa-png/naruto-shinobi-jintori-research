#!/usr/bin/env python3
"""Compare Ghidra and m2c output for identical PS1 MIPS functions.

Only text reports/assembly/C output are retained. Executable slices stay in
RUNNER_TEMP and are deleted by the workflow cleanup step.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

EXPECTED_EXE_SHA256 = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
EXPECTED_EXE_BYTES = 385_024
TEXT_OFFSET = 0x800
TEXT_BYTES = 0x5D800
TEXT_BASE = 0x80010000
FUNCTIONS = {
    # Four direct RNG callers from the original required comparison.
    0x80015ADC: ("FUN_80015adc", 160),
    0x80015B7C: ("FUN_80015b7c", 240),
    0x8001A328: ("FUN_8001a328", 376),
    0x80020BF4: ("FUN_80020bf4", 156),
    # Expanded same-address checks of core RNG/state/callback/Chakra functions.
    # Actual function size/end are read from the current Ghidra report.
    0x8001387C: ("FUN_8001387c", None),
    0x800138EC: ("FUN_800138ec", None),
    0x80035D78: ("FUN_80035d78", None),
    0x80037138: ("FUN_80037138", None),
    0x800373F8: ("FUN_800373f8", None),
    0x8003755C: ("FUN_8003755c", None),
    0x80037B58: ("FUN_80037b58", None),
    0x80037BB0: ("FUN_80037bb0", None),
    0x80037C48: ("FUN_80037c48", None),
}


def run_cmd(command: list[str], timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        check=False, timeout=timeout,
    )


def extract_ghidra_section(text: str, address: int) -> tuple[str | None, str | None]:
    """Extract one FUNCTION or HELPER_FUNCTION section without crossing into another."""
    header = re.compile(
        rf"(?m)^=== (?:HELPER_)?FUNCTION entry=(?:0x)?0*{address:08X}\b[^\n]*$",
        re.IGNORECASE,
    )
    match = header.search(text)
    if not match:
        return None, f"Ghidra function section for 0x{address:08X} not found"
    remainder = text[match.end():]
    next_header = re.search(
        r"(?m)^=== (?:HELPER_)?FUNCTION entry=(?:0x)?0*[0-9A-Fa-f]{8}\b",
        remainder,
    )
    end = match.end() + next_header.start() if next_header else len(text)
    return text[match.start():end], None


def extract_ghidra_c(text: str, address: int) -> tuple[str | None, str | None]:
    section, error = extract_ghidra_section(text, address)
    if section is None:
        return None, error
    match = re.search(
        r"--- C_DECOMPILATION_BEGIN ---\s*(.*?)\s*--- C_DECOMPILATION_END ---",
        section,
        re.DOTALL,
    )
    if match:
        return match.group(1).strip() + "\n", None
    return None, f"Ghidra C block for 0x{address:08X} not found inside its own section"


def extract_ghidra_metadata(text: str, address: int, fallback_size: int | None) -> tuple[int | None, int | None, str | None]:
    section, error = extract_ghidra_section(text, address)
    if section is None:
        return fallback_size, (address + fallback_size if fallback_size else None), error
    size_match = re.search(r"(?m)^body_address_count=(\d+)\s*$", section)
    end_match = re.search(r"(?m)^function_end_exclusive=(?:0x)?([0-9A-Fa-f]+)\s*$", section)
    size = int(size_match.group(1)) if size_match else fallback_size
    end = int(end_match.group(1), 16) if end_match else (address + size if size else None)
    if not size:
        return size, end, f"body_address_count unavailable for 0x{address:08X}"
    if end is None or end <= address:
        return size, end, f"valid function_end_exclusive unavailable for 0x{address:08X}"
    return size, end, None


def run_parser_fixtures() -> None:
    """Guard FUNCTION/HELPER_FUNCTION parsing and exclusive end-address handling."""
    sample = (
        "=== FUNCTION entry=0x80015ADC expected_call_site=0x80015B14 ===\n"
        "name=FUN_80015adc\nbody_address_count=160\nfunction_end_exclusive=0x80015B7C\n"
        "--- C_DECOMPILATION_BEGIN ---\nint func_80015ADC(void) { return 0; }\n--- C_DECOMPILATION_END ---\n"
        "=== HELPER_FUNCTION entry=80037138 ===\n"
        "name=FUN_80037138\nbody_address_count=48\nfunction_end_exclusive=0x80037168\n"
        "--- C_DECOMPILATION_BEGIN ---\nint func_80037138(void) { return 1; }\n--- C_DECOMPILATION_END ---\n"
    )
    c1, e1 = extract_ghidra_c(sample, 0x80015ADC)
    s1, z1, m1 = extract_ghidra_metadata(sample, 0x80015ADC, None)
    c2, e2 = extract_ghidra_c(sample, 0x80037138)
    s2, z2, m2 = extract_ghidra_metadata(sample, 0x80037138, None)
    if any((e1, m1, e2, m2)) or not c1 or not c2:
        raise AssertionError(f"section parser errors: {e1}; {m1}; {e2}; {m2}")
    if (s1, z1, s2, z2) != (160, 0x80015B7C, 48, 0x80037168):
        raise AssertionError(f"section metadata mismatch: {(s1, z1, s2, z2)}")


def normalize_addr_call_tokens(code: str) -> set[str]:
    return {
        m.group(1).lower().zfill(8)
        for m in re.finditer(r"(?:FUN_|func_)(?:0x)?([0-9a-fA-F]{6,8})", code)
    }


def find_asm_function_label(asm: str, address: int) -> str | None:
    # Prefer labels generated by spimdisasm for the exact Ghidra function entry.
    wanted = f"{address:08x}"
    labels = re.findall(
        r"(?m)^\s*(?:glabel|\.globl|\.global|\.ent)\s+([A-Za-z_.$][\w.$]*)",
        asm,
    )
    for label in labels:
        hexmatches = re.findall(r"[0-9a-fA-F]{8}", label)
        if any(h.lower() == wanted for h in hexmatches):
            return label
    # Some assembly variants use an address comment preceding an unnamed label.
    for match in re.finditer(r"(?m)^\s*glabel\s+([A-Za-z_.$][\w.$]*)\s*$", asm):
        tail = asm[match.end():match.end() + 240]
        if wanted in tail.lower():
            return match.group(1)
    return None



def inject_missing_function_boundaries(
    asm: str, function_ends: dict[int, int]
) -> tuple[str, list[str]]:
    """Inject starts and Ghidra-derived exclusive ends that spimdisasm omitted."""
    inserted: list[str] = []
    specs: list[tuple[int, str]] = []
    for address, (_, fallback_size) in FUNCTIONS.items():
        specs.append((address, f"func_{address:08x}"))
        end = function_ends.get(address)
        if end is None and fallback_size:
            end = address + fallback_size
        if end is not None and end > address:
            specs.append((end, f"func_{end:08x}"))
    # Process descending so inserting an earlier label cannot invalidate a later search.
    for address, label in sorted(set(specs), reverse=True):
        if find_asm_function_label(asm, address):
            continue
        insn = re.compile(
            rf"/\*\s*[0-9a-fA-F]+\s+{address:08X}\s+[0-9a-fA-F]+\s+\*/",
            re.IGNORECASE,
        )
        lines = asm.splitlines()
        match_index = next((i for i, line in enumerate(lines) if insn.search(line)), None)
        if match_index is None:
            continue
        lines.insert(match_index, f"glabel {label} # Ghidra boundary 0x{address:08X}")
        asm = "\n".join(lines) + "\n"
        inserted.append(f"0x{address:08X}={label}")
    return asm, inserted


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exe", required=True, help="verified SLPS_035.53 extracted by the workflow")
    parser.add_argument("--ghidra", required=True, help="Ghidra ExportRngCallerAnalysis text output")
    parser.add_argument("--out-dir", required=True, help="runner-temporary text output directory")
    parser.add_argument("--report", required=True, help="step5 comparison report path")
    parser.add_argument("--m2c-commit", required=True, help="resolved source commit SHA for m2c")
    args = parser.parse_args()

    exe = Path(args.exe)
    ghidra_path = Path(args.ghidra)
    out = Path(args.out_dir)
    report_path = Path(args.report)
    out.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "# Step 5 — Same-function Ghidra/m2c comparison",
        "",
        "scope=main executable; 13 core RNG/state/callback/Chakra functions are compared at matching addresses in Ghidra and m2c",
        "game_or_emulator_executed=no",
        "gameplay_input_sent=no",
        "source_binary_committed=no",
        "source_binary_uploaded_as_artifact=no",
        "artifact_policy=text_only",
        "expanded_function_scope=4 original RNG callers plus 9 RNG/state/callback/Chakra core functions",
        f"m2c_commit={Path(args.m2c_commit).read_text(encoding='utf-8').strip()}",
        "m2c_target=mips-ido-c (tool backend selection only; not a claim about the original game compiler)",
        "",
    ]
    data = exe.read_bytes()
    actual_hash = hashlib.sha256(data).hexdigest()
    if len(data) != EXPECTED_EXE_BYTES or actual_hash != EXPECTED_EXE_SHA256:
        lines += [f"status=FAILED", f"exe_bytes={len(data)}", f"exe_sha256={actual_hash}",
                  "error=verified executable size/hash mismatch", ""]
        report_path.write_text("\n".join(lines), encoding="utf-8")
        return 2
    lines += [f"exe_bytes={len(data)}", f"exe_sha256={actual_hash}",
              "text_offset=0x800", "text_base=0x80010000", "text_size=0x5D800", ""]

    ghidra_text = ghidra_path.read_text(encoding="utf-8", errors="replace")
    try:
        run_parser_fixtures()
        lines.append("metadata_parser_fixture=PASS cases=FUNCTION_HELPER_FUNCTION_end_address")
    except Exception as exc:
        lines += ["status=FAILED", f"metadata_parser_fixture=FAIL error={exc}", ""]
        report_path.write_text("\n".join(lines), encoding="utf-8")
        return 2

    function_metadata: dict[int, tuple[int | None, int | None]] = {}
    function_ends: dict[int, int] = {}
    missing_metadata: list[str] = []
    for address, (_, fallback_size) in FUNCTIONS.items():
        size, end, metadata_error = extract_ghidra_metadata(ghidra_text, address, fallback_size)
        if metadata_error:
            missing_metadata.append(f"0x{address:08X}:{metadata_error}")
        function_metadata[address] = (size, end)
        if end is not None:
            function_ends[address] = end
    if missing_metadata:
        lines += [
            "status=PARTIAL",
            "function_metadata_missing=" + ";".join(missing_metadata),
            "error=exact function section/body end is required before claiming same-function m2c comparison",
            "",
        ]
        report_path.write_text("\n".join(lines), encoding="utf-8")
        return 0
    lines.append("function_metadata=PASS source=Ghidra body_address_count_and_end_exclusive")

    # Slice to the verified PS-X EXE text in runner temp, then feed that exact
    # machine code image to spimdisasm and m2c.
    work_text = out / "main_text.bin"
    work_text.write_bytes(data[TEXT_OFFSET:TEXT_OFFSET + TEXT_BYTES])
    if work_text.stat().st_size != TEXT_BYTES:
        lines += ["status=FAILED", "error=unexpected text slice length", ""]
        report_path.write_text("\n".join(lines), encoding="utf-8")
        return 2

    asm_dir = out / "spimdisasm-output"
    asm_dir.mkdir(parents=True, exist_ok=True)
    dis_cmd = [
        "singleFileDisasm", str(work_text), str(asm_dir),
        "--start", "0x0", "--end", "0x5D800", "--vram", "0x80010000",
        "--endian", "little", "--compiler", "PSYQ", "--instr-category", "cpu",
        "--no-write-binary",
    ]
    dis = run_cmd(dis_cmd, timeout=180)
    (out / "spimdisasm.log").write_text(dis.stdout or "", encoding="utf-8")
    # Delete the temporary machine-code slice immediately after disassembly;
    # it is never part of the text artifact, even if later parsing fails.
    try:
        work_text.unlink()
    except OSError:
        pass
    assembly_files = sorted(
        (p for p in asm_dir.rglob("*.s") if p.is_file()),
        key=lambda p: p.stat().st_size,
        reverse=True,
    )
    if dis.returncode != 0 or not assembly_files:
        inventory = [
            f"{p.relative_to(out).as_posix()}:{p.stat().st_size}"
            for p in out.rglob("*") if p.is_file()
        ]
        lines += [
            "status=PARTIAL",
            f"spimdisasm_exit_code={dis.returncode}",
            "error=spimdisasm did not produce a .s text file",
            "output_inventory=" + ",".join(inventory),
            f"spimdisasm_log={(dis.stdout or '')[-2000:]}",
            "",
        ]
        report_path.write_text("\\n".join(lines), encoding="utf-8")
        return 0

    asm_path = assembly_files[0]
    asm = asm_path.read_text(encoding="utf-8", errors="replace")
    asm, injected_labels = inject_missing_function_boundaries(asm, function_ends)
    asm_path.write_text(asm, encoding="utf-8")
    lines += [
        f"spimdisasm_exit_code={dis.returncode}",
        f"assembly_file={asm_path.relative_to(out).as_posix()}",
        f"assembly_bytes={asm_path.stat().st_size}",
        f"assembly_file_count={len(assembly_files)}",
        "injected_function_boundaries=" + (",".join(injected_labels) or "none"),
        "",
    ]
    all_ok = True
    for address, (ghidra_name, _) in FUNCTIONS.items():
        expected_size = function_metadata[address][0]
        stem = f"{address:08x}"
        ghidra_c, error = extract_ghidra_c(ghidra_text, address)
        if ghidra_c is None:
            all_ok = False
            lines += [f"## {ghidra_name}", f"address=0x{address:08X}",
                      "status=FAILED", f"error={error}", ""]
            continue
        ghidra_c_path = out / f"ghidra_{stem}.c"
        ghidra_c_path.write_text(ghidra_c, encoding="utf-8")

        asm_label = find_asm_function_label(asm, address)
        if not asm_label:
            all_ok = False
            lines += [f"## {ghidra_name}", f"address=0x{address:08X}",
                      f"ghidra_function_name={ghidra_name}", f"ghidra_body_bytes={expected_size}",
                      "status=PARTIAL", "m2c_assembly_label=NOT_FOUND",
                      "interpretation=spimdisasm did not expose this address as a function label; no equivalence is claimed", ""]
            continue

        m2c_cmd = [
            "m2c", "--target", "mips-ido-c", "--function", asm_label,
            "--no-cache", str(asm_path),
        ]
        m2c_result = run_cmd(m2c_cmd, timeout=120)
        m2c_c = m2c_result.stdout or ""
        m2c_path = out / f"m2c_{stem}.c"
        m2c_path.write_text(m2c_c, encoding="utf-8")
        (out / f"m2c_{stem}.log").write_text(
            "command=" + " ".join(m2c_cmd) + "\n"
            + f"exit_code={m2c_result.returncode}\n" + m2c_c,
            encoding="utf-8",
        )
        # Count function-like references and explicitly compare target RNG call visibility.
        g_calls = normalize_addr_call_tokens(ghidra_c)
        m_calls = normalize_addr_call_tokens(m2c_c)
        shared = sorted(g_calls & m_calls)
        ghidra_rng = "80035d78" in g_calls or "80035d78" in ghidra_c.lower()
        m2c_rng = "80035d78" in m_calls or "80035d78" in m2c_c.lower()
        success = m2c_result.returncode == 0 and bool(re.search(r"\b[A-Za-z_]\w*\s*\(", m2c_c))
        if not success:
            all_ok = False
        lines += [
            f"## {ghidra_name}",
            f"address=0x{address:08X}",
            f"ghidra_function_name={ghidra_name}",
            f"ghidra_body_bytes={expected_size}",
            f"spimdisasm_label={asm_label}",
            f"m2c_exit_code={m2c_result.returncode}",
            f"ghidra_c_lines={len(ghidra_c.splitlines())}",
            f"m2c_output_lines={len(m2c_c.splitlines())}",
            f"m2c_output_nonempty={str(bool(m2c_c.strip())).lower()}",
            f"ghidra_call_tokens={','.join(sorted(g_calls)) or 'none'}",
            f"m2c_call_tokens={','.join(sorted(m_calls)) or 'none'}",
            f"shared_call_tokens={','.join(shared) or 'none'}",
            f"ghidra_contains_rng_address_0x80035D78={str(ghidra_rng).lower()}",
            f"m2c_contains_rng_address_0x80035D78={str(m2c_rng).lower()}",
            f"status={'SUCCESS' if success else 'FAILED'}",
            "comparison_note=structural cross-check only; C text is not expected to match identically and does not prove original source semantics",
            "",
        ]

    status = "SUCCESS" if all_ok else "PARTIAL"
    lines += [
        f"functions_requested={len(FUNCTIONS)}",
        f"functions_with_m2c_output={sum(1 for p in out.glob('m2c_*.c') if p.stat().st_size > 0)}",
        f"status={status}",
        "completion_criteria=Ghidra C and m2c output both exist for all requested same-address functions with Ghidra-derived end addresses; structural comparison only",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    # Remove binary-only temporary data; source executable itself is removed by workflow cleanup.
    try:
        work_text.unlink()
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
