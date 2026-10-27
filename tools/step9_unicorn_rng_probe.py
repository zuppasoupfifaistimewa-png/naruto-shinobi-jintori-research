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
    UC_MIPS_REG_A0,
    UC_MIPS_REG_A1,
)

EXE_BYTES = 385_024
TEXT_OFFSET = 0x800
TEXT_VIRTUAL_BASE = 0x80010000
TEXT_BASE = TEXT_VIRTUAL_BASE & 0x1FFFFFFF
TEXT_SIZE = 0x5D800
ENTRY_VIRTUAL = 0x80035D78
ENTRY = ENTRY_VIRTUAL & 0x1FFFFFFF
COUNTER_HELPER_VIRTUAL = 0x80037138
COUNTER_GLOBAL_VIRTUAL = 0x80066E7C
COUNTER_GLOBAL = COUNTER_GLOBAL_VIRTUAL & 0x1FFFFFFF
STATE_VIRTUAL = 0x800A3118
STATE = STATE_VIRTUAL & 0x1FFFFFFF
# PS1 KSEG0 addresses 0x80000000–0x801FFFFF alias physical RAM 0x00000000–0x001FFFFF.
# Unicorn MIPS bypasses KSEG MMU translation; map the physical 2 MiB RAM window.
RAM_BASE = 0x00000000
RAM_SIZE = 0x200000
STACK = 0x001FE000
RETURN_SENTINEL = 0x001FF000
MAX_INSTRUCTIONS = 128
SETTER_VIRTUAL = 0x8001387C
GETTER_VIRTUAL = 0x800138EC
# Cross-checked in Ghidra/m2c at 0x8001387C/0x800138EC:
# four 0xB4-byte records, numeric field at +0x18 => base 0x80070EB8.
# Setter returns 1 for index 0..3 after clamp [-9999,99999], else 0.
# Getter returns slot value for index 0..3, else 0. These are CPU-only tests.
PLAYER_VALUE_SLOT_VIRTUAL = 0x80070EB8
PLAYER_VALUE_SLOT = PLAYER_VALUE_SLOT_VIRTUAL & 0x1FFFFFFF
PLAYER_VALUE_STRIDE = 0xB4
PLAYER_COUNT = 4
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


def run_simple_function(
    code: bytes,
    gp: int,
    entry_virtual: int,
    a0: int,
    a1: int,
    initial_slots: list[int],
) -> dict[str, object]:
    """Run one main-EXE numeric accessor in a fresh RAM-only MIPS machine."""
    if len(initial_slots) != PLAYER_COUNT:
        raise ValueError("expected four initialized participant numeric slots")
    emu = Uc(UC_ARCH_MIPS, UC_MODE_MIPS32 | UC_MODE_LITTLE_ENDIAN)
    emu.mem_map(RAM_BASE, RAM_SIZE)
    emu.mem_write(TEXT_BASE, code)
    for index, value in enumerate(initial_slots):
        emu.mem_write(
            PLAYER_VALUE_SLOT + index * PLAYER_VALUE_STRIDE,
            struct.pack("<I", value & MASK32),
        )
    emu.reg_write(UC_MIPS_REG_GP, gp)
    emu.reg_write(UC_MIPS_REG_SP, STACK)
    emu.reg_write(UC_MIPS_REG_RA, RETURN_SENTINEL)
    emu.reg_write(UC_MIPS_REG_A0, a0 & MASK32)
    emu.reg_write(UC_MIPS_REG_A1, a1 & MASK32)
    entry = entry_virtual & 0x1FFFFFFF
    emu.reg_write(UC_MIPS_REG_PC, entry)
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
        emu.emu_start(entry, RAM_BASE + RAM_SIZE, count=MAX_INSTRUCTIONS + 1)
    except UcError as exc:
        error = str(exc)
    actual_pc = emu.reg_read(UC_MIPS_REG_PC) & MASK32
    actual_v0 = emu.reg_read(UC_MIPS_REG_V0) & MASK32
    actual_slots = [
        struct.unpack("<I", emu.mem_read(PLAYER_VALUE_SLOT + i * PLAYER_VALUE_STRIDE, 4))[0]
        for i in range(PLAYER_COUNT)
    ]
    return {
        "entry_virtual": f"0x{entry_virtual:08X}",
        "a0": f"0x{a0 & MASK32:08X}",
        "a1": f"0x{a1 & MASK32:08X}",
        "actual_v0": f"0x{actual_v0:08X}",
        "actual_pc": f"0x{actual_pc:08X}",
        "return_to_sentinel": bool(state["returned"]),
        "instructions": int(state["instructions"]),
        "budget_exceeded": bool(state["budget_exceeded"]),
        "emulator_error": error or None,
        "actual_slots": actual_slots,
    }


def run_player_value_accessor_tests(code: bytes, gp: int) -> list[dict[str, object]]:
    """Check index guards, signed clamping, and shared getter/setter storage."""
    original = [0x11111111, 0x22222222, 0x33333333, 0x44444444]
    setter_inputs = [
        ("setter_normal", 0, 1234),
        ("setter_clamp_min", 1, -12000),
        ("setter_clamp_max", 2, 100000),
        ("setter_min_boundary", 3, -9999),
        ("setter_max_boundary", 0, 99999),
        ("setter_negative_boundary", 1, -9999),
        ("setter_large_positive", 2, 0x7FFFFFFF),
        ("setter_large_negative", 3, -0x80000000),
        ("setter_invalid_index_4", 4, 88),
        ("setter_invalid_unsigned_index", 0xFFFFFFFF, 88),
    ]
    rows: list[dict[str, object]] = []
    for label, index, value in setter_inputs:
        expected_slots = original.copy()
        if index < PLAYER_COUNT:
            clamped = 99999 if value >= 100000 else (-9999 if value < -9999 else value)
            expected_slots[index] = clamped & MASK32
            expected_v0 = 1
        else:
            expected_v0 = 0
        result = run_simple_function(code, gp, SETTER_VIRTUAL, index, value, original)
        actual_slots = result["actual_slots"]
        actual_v0 = int(str(result["actual_v0"]), 16)
        ok = (
            result["emulator_error"] is None
            and result["return_to_sentinel"]
            and not result["budget_exceeded"]
            and result["actual_pc"] == f"0x{RETURN_SENTINEL:08X}"
            and actual_v0 == expected_v0
            and actual_slots == expected_slots
        )
        rows.append({
            "label": label,
            "entry": f"0x{SETTER_VIRTUAL:08X}",
            "a0": f"0x{index & MASK32:08X}",
            "a1": f"0x{value & MASK32:08X}",
            "expected_v0": f"0x{expected_v0:08X}",
            "expected_slots": expected_slots,
            **result,
            "pass": ok,
        })

    initial_getter_slots = [1234 & MASK32, -9999 & MASK32, 99999 & MASK32, -1 & MASK32]
    getter_inputs = [
        ("getter_slot_0", 0, initial_getter_slots[0]),
        ("getter_slot_1_negative", 1, initial_getter_slots[1]),
        ("getter_slot_2_max", 2, initial_getter_slots[2]),
        ("getter_slot_3_minus_one", 3, initial_getter_slots[3]),
        ("getter_invalid_index_4", 4, 0),
        ("getter_invalid_unsigned_index", 0xFFFFFFFF, 0),
    ]
    for label, index, expected_v0 in getter_inputs:
        result = run_simple_function(code, gp, GETTER_VIRTUAL, index, 0, initial_getter_slots)
        actual_v0 = int(str(result["actual_v0"]), 16)
        ok = (
            result["emulator_error"] is None
            and result["return_to_sentinel"]
            and not result["budget_exceeded"]
            and result["actual_pc"] == f"0x{RETURN_SENTINEL:08X}"
            and actual_v0 == expected_v0
            and result["actual_slots"] == initial_getter_slots
        )
        rows.append({
            "label": label,
            "entry": f"0x{GETTER_VIRTUAL:08X}",
            "a0": f"0x{index & MASK32:08X}",
            "a1": "0x00000000",
            "expected_v0": f"0x{expected_v0:08X}",
            "expected_slots": initial_getter_slots,
            **result,
            "pass": ok,
        })
    return rows


def run_counter_helper_tests(code: bytes, gp: int) -> list[dict[str, object]]:
    """Verify the negative-argument helper path against a controlled global word."""
    global_values = [0x00000000, 0x00000001, 0x12345678, 0xFFFFFFFF]
    negative_args = [0xFFFFFFFF, 0x80000000]
    rows: list[dict[str, object]] = []
    for global_value in global_values:
        for a0 in negative_args:
            emu = Uc(UC_ARCH_MIPS, UC_MODE_MIPS32 | UC_MODE_LITTLE_ENDIAN)
            emu.mem_map(RAM_BASE, RAM_SIZE)
            emu.mem_write(TEXT_BASE, code)
            emu.mem_write(COUNTER_GLOBAL, struct.pack("<I", global_value))
            emu.reg_write(UC_MIPS_REG_GP, gp)
            emu.reg_write(UC_MIPS_REG_SP, STACK)
            emu.reg_write(UC_MIPS_REG_RA, RETURN_SENTINEL)
            emu.reg_write(UC_MIPS_REG_A0, a0 & MASK32)
            emu.reg_write(UC_MIPS_REG_A1, 0)
            entry = COUNTER_HELPER_VIRTUAL & 0x1FFFFFFF
            emu.reg_write(UC_MIPS_REG_PC, entry)
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
                emu.emu_start(entry, RAM_BASE + RAM_SIZE, count=MAX_INSTRUCTIONS + 1)
            except UcError as exc:
                error = str(exc)
            actual_v0 = emu.reg_read(UC_MIPS_REG_V0) & MASK32
            actual_pc = emu.reg_read(UC_MIPS_REG_PC) & MASK32
            actual_global = struct.unpack("<I", emu.mem_read(COUNTER_GLOBAL, 4))[0]
            ok = (
                not error
                and bool(state["returned"])
                and not bool(state["budget_exceeded"])
                and actual_pc == RETURN_SENTINEL
                and actual_v0 == global_value
                and actual_global == global_value
            )
            rows.append({
                "label": f"helper_negative_a0_{a0:08X}_global_{global_value:08X}",
                "entry": f"0x{COUNTER_HELPER_VIRTUAL:08X}",
                "a0": f"0x{a0:08X}",
                "expected_v0": f"0x{global_value:08X}",
                "actual_v0": f"0x{actual_v0:08X}",
                "expected_global": f"0x{global_value:08X}",
                "actual_global": f"0x{actual_global:08X}",
                "return_to_sentinel": bool(state["returned"]),
                "instructions": int(state["instructions"]),
                "budget_exceeded": bool(state["budget_exceeded"]),
                "emulator_error": error or None,
                "pass": ok,
            })
    return rows


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
    if (entry_pc, load, text_size) != (0x80011448, TEXT_VIRTUAL_BASE, TEXT_SIZE):
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
    helper_rows = run_counter_helper_tests(code, gp)
    helper_pass = all(bool(row["pass"]) for row in helper_rows)
    accessor_rows = run_player_value_accessor_tests(code, gp)
    accessors_pass = all(bool(row["pass"]) for row in accessor_rows)
    all_tests_pass = all_pass and helper_pass and accessors_pass
    exe_hash = hashlib.sha256(data).hexdigest()
    lines = [
        "# Step 9 — validasi fungsi RNG dan accessor nilai pemain secara terisolasi dengan Unicorn",
        "",
        "- Scope: hanya menjalankan rutin main EXE 0x80035D78 (RNG), jalur a0 negatif helper 0x80037138, dan accessor 0x8001387C/0x800138EC di RAM CPU terisolasi; tidak menjalankan emulator PS1/game, BIOS, event loop, atau input gameplay.",
        "- RAM model: 2 MiB virtual RAM PS1 pada 0x80000000–0x801FFFFF, text EXE dimuat pada alamat header 0x80010000; seluruh RAM lain nol kecuali state RNG dan register awal yang dicatat.",
        "- Alamat CPU virtual fungsi/state adalah `0x80035D78`/`0x800A3118`; fungsi dipanggil pada alias fisik `0x00035D78`, state ditulis di physical `0x000A3118`. Register awal: PC=0x00035D78, RA=0x001FF000 (physical sentinel return), SP=0x001FE000; GP diambil dari header PS-X EXE.",
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
        "## Test terisolasi tambahan — helper counter dengan argumen negatif",
        "",
        "- Scope: hanya menguji helper main EXE 0x80037138 dengan a0 bertanda negatif sambil menetapkan global 0x80066E7C ke empat word uji di RAM terisolasi.",
        "- Expected: v0 mengembalikan word global yang disuntikkan dan global tidak berubah; input a0 diuji pada 0xFFFFFFFF dan 0x80000000.",
        "",
        "| Kasus | Entry | a0 | Global harapan | v0 aktual | Global aktual | Instruksi | Return | Status |",
        "|---|---|---|---|---|---|---:|---|---|",
    ]
    for r in helper_rows:
        lines.append(
            f"| {r['label']} | {r['entry']} | {r['a0']} | {r['expected_v0']} | "
            f"{r['actual_v0']} | {r['actual_global']} | {r['instructions']} | "
            f"{'PASS' if r['return_to_sentinel'] else 'NO'} | {'PASS' if r['pass'] else 'FAIL'} |"
        )
    lines += [
    lines += [
        "",
        "## Test terisolasi tambahan — setter/getter nilai peserta",
        "",
        "- Scope: hanya fungsi main EXE 0x8001387C dan 0x800138EC dalam RAM 2 MiB; tidak memuat BIOS atau menjalankan game/emulator PS1.",
        "- Expected setter: indeks 0..3 valid, nilai diklem ke -9999..99999, nilai slot lain tidak berubah; indeks 4/0xFFFFFFFF harus mengembalikan 0 tanpa mengubah tabel.",
        "- Expected getter: baca word dari slot nilai yang sama untuk indeks 0..3; indeks 4/0xFFFFFFFF harus mengembalikan 0.",
        "",
        "| Kasus | Entry | a0 | a1 | v0 harapan | v0 aktual | Slot peserta aktual (hex) | Instruksi | Return | Status |",
        "|---|---|---|---|---|---|---|---:|---|---|",
    ]
    for r in accessor_rows:
        actual_slots = ",".join(f"0x{int(v):08X}" for v in r["actual_slots"])
        lines.append(
            f"| {r['label']} | {r['entry']} | {r['a0']} | {r['a1']} | {r['expected_v0']} | "
            f"{r['actual_v0']} | {actual_slots} | {r['instructions']} | "
            f"{'PASS' if r['return_to_sentinel'] else 'NO'} | {'PASS' if r['pass'] else 'FAIL'} |"
        )
    lines += [
        "",
        "## Penilaian",

        "",
        f"- ISOLATED_RNG_FUNCTION_EXECUTION={'PASS' if all_pass else 'FAIL'}",
        f"- ISOLATED_HELPER_RETURN_TESTS={'PASS' if helper_pass else 'FAIL'}",
        f"- helper_cases_passed={sum(1 for r in helper_rows if r['pass'])}/{len(helper_rows)}",
        f"- ISOLATED_PLAYER_VALUE_ACCESSOR_TESTS={'PASS' if accessors_pass else 'FAIL'}",
        f"- accessor_cases_passed={sum(1 for r in accessor_rows if r['pass'])}/{len(accessor_rows)}",
        f"- STEP9_ALL_TESTS={'PASS' if all_tests_pass else 'FAIL'}",
        f"- vectors_passed={sum(1 for r in rows if r['pass'])}/{len(rows)}",
        "- Status scope: verifikasi dinamis satu rutin RNG dan dua accessor nilai per-peserta saja. Ini tidak memverifikasi seluruh pemanggil, helper RNG/timer di perangkat nyata, caller resource, semua delay-slot/path, atau gameplay.",
        "- Limitasi: Unicorn memodelkan instruksi CPU dan RAM yang disediakan, bukan perangkat keras PS1, BIOS, DMA, GPU, audio, loader game, atau jadwal frame. Tidak ada kesimpulan tentang hasil roulette/battle.",
        "- Data privat: executable hanya dibaca di runner, tidak disimpan pada repo maupun artefak; hanya laporan teks yang boleh diunggah.",
        "",
    ]
    report = "\n".join(lines)
    output_path.write_text(report, encoding="utf-8")
    print(report, end="")
    if not all_tests_pass:
        print("STEP9_TESTS=FAIL", file=sys.stderr)
        return 1
    print("STEP9_ISOLATED_RNG=PASS")
    print("STEP9_HELPER_NEGATIVE_RETURN=PASS")
    print("STEP9_PLAYER_VALUE_ACCESSORS=PASS")
    print("STEP9_TESTS=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
