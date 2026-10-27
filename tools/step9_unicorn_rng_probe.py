#!/usr/bin/env python3
"""Execute only the verified PS-X EXE LCG routine in a minimal Unicorn MIPS32 RAM map.

STEP9_REPEAT_MARKER: isolated CPU test only; no PS1 emulator or gameplay is launched.

This is function-isolated CPU emulation, not a PS1 emulator and not gameplay.
The input executable must be verified by the calling workflow and is never copied
to the repository/artifact. Only the text report is written to the output path.
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys
from pathlib import Path

from unicorn import Uc, UcError, UC_ARCH_MIPS, UC_MODE_LITTLE_ENDIAN, UC_MODE_MIPS32, UC_HOOK_CODE
from unicorn.mips_const import (
    UC_MIPS_REG_PC,
    UC_MIPS_REG_RA,
    UC_MIPS_REG_SP,
    UC_MIPS_REG_GP,
    UC_MIPS_REG_V0,
)

EXE_BYTES = 385_024
TEXT_OFFSET = 0x800
TEXT_BASE = 0x80010000
TEXT_SIZE = 0x5D800
ENTRY = 0x80035D78
STATE = 0x800A3118
RAM_BASE = 0x80000000
RAM_SIZE = 0x200000
STACK = 0x801FE000
RETURN_SENTINEL = 0x801FF000
MAX_INSTRUCTIONS = 128
MULT = 0x41C64E6D
ADD = 0x3039
MASK32 = 0xFFFFFFFF
TEST_STATES = (
    0x00000000,
    0x00000001,
    0xFFFFFFFF,
    0x12345678,
    0x7FFFFFFF,
    0x80000000,
    0xD44FAABC,
)


def expected(old: int) -> tuple[int, int]:
    new = (old * MULT + ADD) & MASK32
    return new, (new >> 16) & 0x7FFF


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: step9_unicorn_rng_probe.py VERIFIED_EXE OUTPUT_MD")
    exe_path, output_path = map(Path, sys.argv[1:])
    data = exe_path.read_bytes()
    if len(data) != EXE_BYTES or data[:8] != b"PS-X EXE":
        raise SystemExit("FAIL: verified PS-X EXE size/signature mismatch")
    u32 = lambda offset: struct.unpack_from("<I", data, offset)[0]
    entry_pc = u32(0x10)
    gp = u32(0x14)
    load = u32(0x18)
    text_size = u32(0x1C)
    if (entry_pc, load, text_size) != (0x80011448, TEXT_BASE, TEXT_SIZE):
        raise SystemExit("FAIL: PS-X EXE header fields differ from verified baseline")
    code = data[TEXT_OFFSET:TEXT_OFFSET + TEXT_SIZE]
    if len(code) != TEXT_SIZE or not (TEXT_BASE <= ENTRY < TEXT_BASE + TEXT_SIZE):
        raise SystemExit("FAIL: RNG routine is outside verified executable text range")

    rows: list[dict[str, object]] = []
    for old in TEST_STATES:
        emu = Uc(UC_ARCH_MIPS, UC_MODE_MIPS32 | UC_MODE_LITTLE_ENDIAN)
        emu.mem_map(RAM_BASE, RAM_SIZE)
        emu.mem_write(TEXT_BASE, code)
        emu.mem_write(STATE, struct.pack("<I", old))
        emu.reg_write(UC_MIPS_REG_GP, gp)
        emu.reg_write(UC_MIPS_REG_SP, STACK)
        emu.reg_write(UC_MIPS_REG_RA, RETURN_SENTINEL)
        emu.reg_write(UC_MIPS_REG_PC, ENTRY)
        state: dict[str, object] = {"instructions": 0, "returned": False, "budget_exceeded": False}

        def on_instruction(machine: Uc, address: int, size: int, user_data: dict[str, object]) -> None:
            if address == RETURN_SENTINEL:
                user_data["returned"] = True
                machine.emu_stop()
                return
            user_data["instructions"] = int(user_data["instructions"]) + 1
            if int(user_data["instructions"]) > MAX_INSTRUCTIONS:
                user_data["budget_exceeded"] = True
                machine.emu_stop()

        emu.hook_add(UC_HOOK_CODE, on_instruction, state)
        error = ""
        try:
            emu.emu_start(ENTRY, RAM_BASE + RAM_SIZE, count=MAX_INSTRUCTIONS + 1)
        except UcError as exc:
            error = str(exc)
        actual_state = struct.unpack("<I", emu.mem_read(STATE, 4))[0]
        actual_output = emu.reg_read(UC_MIPS_REG_V0) & MASK32
        actual_pc = emu.reg_read(UC_MIPS_REG_PC) & MASK32
        want_state, want_output = expected(old)
        ok = (
            not error
            and bool(state["returned"])
            and not bool(state["budget_exceeded"])
            and actual_pc == RETURN_SENTINEL
            and actual_state == want_state
            and actual_output == want_output
        )
        rows.append({
            "initial_state": f"0x{old:08X}",
            "expected_new_state": f"0x{want_state:08X}",
            "actual_new_state": f"0x{actual_state:08X}",
            "expected_v0": f"0x{want_output:08X}",
            "actual_v0": f"0x{actual_output:08X}",
            "return_to_sentinel": bool(state["returned"]),
            "instructions": int(state["instructions"]),
            "actual_pc": f"0x{actual_pc:08X}",
            "budget_exceeded": bool(state["budget_exceeded"]),
            "emulator_error": error or None,
            "pass": ok,
        })

    all_pass = all(bool(row["pass"]) for row in rows)
    exe_hash = hashlib.sha256(data).hexdigest()
    lines = [
        "# Step 9 — validasi fungsi RNG terisolasi dengan Unicorn",
        "",
        "- Scope: hanya menjalankan fungsi MIPS di 0x80035D78 pada executable text yang telah diverifikasi; tidak menjalankan emulator PS1/game, BIOS, event loop, atau input gameplay.",
        "- RAM model: 2 MiB virtual RAM PS1 pada 0x80000000–0x801FFFFF, text EXE dimuat pada alamat header 0x80010000; seluruh RAM lain nol kecuali state RNG dan register awal yang dicatat.",
        "- Register awal: PC=0x80035D78, RA=0x801FF000 (sentinel return), SP=0x801FE000, GP diambil dari header PS-X EXE.",
        f"- Executable: bytes={len(data)}; SHA-256={exe_hash}; teks={len(code)} bytes; rentang=0x{TEXT_BASE:08X}–0x{TEXT_BASE + TEXT_SIZE:08X}.",
        f"- Fungsi berakhir kembali ke sentinel; batas instruksi maksimum per tes={MAX_INSTRUCTIONS}.",
        "",
        "## Test vectors",
        "",
        "| State awal | State baru yang diharapkan | State aktual | Output v0 yang diharapkan | Output aktual | Instruksi | Return | Hasil |",
        "|---|---|---|---|---|---:|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['initial_state']} | {r['expected_new_state']} | {r['actual_new_state']} | "
            f"{r['expected_v0']} | {r['actual_v0']} | {r['instructions']} | "
            f"{'PASS' if r['return_to_sentinel'] else 'NO'} | {'PASS' if r['pass'] else 'FAIL'} |"
        )
    lines += [
        "",
        "## Penilaian",
        "",
        f"- ISOLATED_RNG_FUNCTION_EXECUTION={'PASS' if all_pass else 'FAIL'}",
        f"- vectors_passed={sum(1 for r in rows if r['pass'])}/{len(rows)}",
        "- Status scope: verifikasi dinamis satu fungsi rutin RNG saja. Ini tidak memverifikasi seluruh pemanggil, helper RNG, caller resource, delay-slot semantics di semua jalur, atau gameplay.",
        "- Limitasi: Unicorn memodelkan instruksi CPU dan RAM yang disediakan, bukan perangkat keras PS1, BIOS, DMA, GPU, audio, loader game, atau jadwal frame. Tidak ada kesimpulan tentang hasil roulette/battle.",
        "- Data privat: executable hanya dibaca di runner, tidak disimpan pada repo maupun artefak; hanya laporan teks yang boleh diunggah.",
        "",
    ]
    report = "\n".join(lines)
    output_path.write_text(report, encoding="utf-8")
    print(report, end="")
    if not all_pass:
        print("STEP9_ISOLATED_RNG=FAIL", file=sys.stderr)
        return 1
    print("STEP9_ISOLATED_RNG=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
