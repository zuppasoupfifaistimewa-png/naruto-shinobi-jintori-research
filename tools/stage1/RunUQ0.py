#!/usr/bin/env python3
"""UQ0: bounded static audit of callers, v0 consumers, selector byte and nibble masks."""
from __future__ import annotations
import argparse
import csv
import hashlib
import re
from pathlib import Path

EXE_SIZE = 385024
DATA_SIZE = 66015232
EXE_SHA = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
DATA_SHA = "69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
ENTRY1_SHA = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
EXE_BASE, EXE_OFF = 0x80010000, 0x800
E1_BASE, E1_OFF, E1_SIZE = 0x800AD450, 0x10BB000, 596412
ENTRY1_IN_DATA = 0x10BB000
RAM_POINTER = 0x8013EA84
STRIDE = 0x124
TARGETS = {0x800B770C, 0x800B76BC}
TARGET_NAMES = {0x800B770C: "FUNCTION_800B770C", 0x800B76BC: "FUNCTION_800B76BC"}
REGS = ("zero", "at", "v0", "v1", "a0", "a1", "a2", "a3", "t0", "t1", "t2", "t3",
        "t4", "t5", "t6", "t7", "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",
        "t8", "t9", "k0", "k1", "gp", "sp", "fp", "ra")
MEMOPS = {
    0x20: ("lb", 1, "R"), 0x21: ("lh", 2, "R"), 0x22: ("lwl", 4, "R"),
    0x23: ("lw", 4, "R"), 0x24: ("lbu", 1, "R"), 0x25: ("lhu", 2, "R"),
    0x26: ("lwr", 4, "R"), 0x28: ("sb", 1, "W"), 0x29: ("sh", 2, "W"),
    0x2A: ("swl", 4, "W"), 0x2B: ("sw", 4, "W"), 0x2E: ("swr", 4, "W")
}
SPECIAL = {0: "sll", 2: "srl", 3: "sra", 4: "sllv", 6: "srlv", 7: "srav",
           8: "jr", 9: "jalr", 16: "mfhi", 17: "mthi", 18: "mflo", 19: "mtlo",
           24: "mult", 25: "multu", 26: "div", 27: "divu", 32: "add", 33: "addu",
           34: "sub", 35: "subu", 36: "and", 37: "or", 38: "xor", 39: "nor",
           42: "slt", 43: "sltu"}
IMMOPS = {8: "addi", 9: "addiu", 10: "slti", 11: "sltiu", 12: "andi", 13: "ori", 14: "xori"}
BRANCH = {4: "beq", 5: "bne", 6: "blez", 7: "bgtz", 1: "regimm"}
FIELDS = {
    "callers": ["region", "call_pc", "file_offset", "jal_bytes", "jal", "target_pc", "target_name",
                "delay_slot_pc", "delay_slot", "setup_a0", "origin_a0", "chain_a0", "status_a0",
                "setup_a1", "origin_a1", "chain_a1", "status_a1", "setup_a2", "origin_a2", "chain_a2",
                "status_a2", "setup_a3", "origin_a3", "chain_a3", "status_a3"],
    "consumers": ["region", "call_pc", "return_pc", "path_id", "step", "consumer_pc", "file_offset",
                  "instruction", "use_kind", "operand_registers", "delay_slot_path", "status"],
    "access": ["region", "pc", "file_offset", "bytes_4B", "instruction", "access_kind", "width",
               "displacement", "base_register", "data_register", "base_class", "base_expression",
               "field_offset_candidate", "access_status"],
    "loaders": ["region", "pc", "file_offset", "instruction", "global_ea", "relationship_to_EA84",
                "nearby_index_scale_pattern", "status"],
    "rmw": ["region", "load_pc", "mask_ops", "store_pc", "store_instruction", "mask_immediates",
            "bit8_effect", "bit9_effect", "bit10_effect", "bit11_effect", "or_source",
            "suspected_clear_mask", "status"],
    "nibble": ["region", "pc", "file_offset", "instruction", "base_register", "base_class",
               "base_expression", "target_offset", "bit8_11_effect", "source_register", "status"],
    "globals": ["region", "load_pc", "instruction", "base_lui_pc", "base_lui", "global_ea",
                "global_role", "static_writer_pcs", "ea84_chain_status"],
    "validation": ["region", "pc", "file_offset", "bytes_4B", "scan_instruction",
                   "independent_instruction", "match"]
}

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def reg(n: int) -> str:
    return "$" + REGS[n]

def signed16(value: int) -> int:
    return value if value < 0x8000 else value - 0x10000

def dec(raw: bytes, pc: int) -> dict:
    if len(raw) != 4:
        raise ValueError("MIPS_WORD_LENGTH")
    word = int.from_bytes(raw, "little")
    op, rs, rt = word >> 26, (word >> 21) & 31, (word >> 16) & 31
    rd, sh, fn = (word >> 11) & 31, (word >> 6) & 31, word & 63
    imm, simm = word & 0xffff, signed16(word & 0xffff)
    d = {"word": word, "op": op, "rs": rs, "rt": rt, "rd": rd, "sh": sh, "fn": fn,
         "imm": imm, "simm": simm, "mn": ".word", "text": f".word 0x{word:08X}",
         "reads": set(), "writes": None, "control": False, "target": None, "mem": None}
    if op == 0:
        mn = SPECIAL.get(fn, ".word")
        d["mn"] = mn
        if mn in ("sll", "srl", "sra"):
            d.update(reads={rt}, writes=rd, text=f"{mn} {reg(rd)},{reg(rt)},{sh}")
        elif mn in ("sllv", "srlv", "srav"):
            d.update(reads={rt, rs}, writes=rd, text=f"{mn} {reg(rd)},{reg(rt)},{reg(rs)}")
        elif mn == "jr":
            d.update(reads={rs}, control=True, text=f"jr {reg(rs)}")
        elif mn == "jalr":
            d.update(reads={rs}, writes=rd, control=True, text=f"jalr {reg(rd)},{reg(rs)}")
        elif mn in ("mfhi", "mflo"):
            d.update(writes=rd, text=f"{mn} {reg(rd)}")
        elif mn in ("mthi", "mtlo"):
            d.update(reads={rs}, text=f"{mn} {reg(rs)}")
        elif mn in ("mult", "multu", "div", "divu"):
            d.update(reads={rs, rt}, text=f"{mn} {reg(rs)},{reg(rt)}")
        elif mn in ("syscall", "break"):
            d["text"] = mn
        elif mn != ".word":
            d.update(reads={rs, rt}, writes=rd, text=f"{mn} {reg(rd)},{reg(rs)},{reg(rt)}")
        return d
    if op in (2, 3):
        target = (((pc + 4) & 0xF0000000) | ((word & 0x03ffffff) << 2)) & 0xffffffff
        mn = "j" if op == 2 else "jal"
        d.update(mn=mn, control=True, target=target, text=f"{mn} 0x{target:08X}")
        return d
    if op == 1 or op in BRANCH:
        mn = {0: "bltz", 1: "bgez", 16: "bltzal", 17: "bgezal"}.get(rt, "regimm") if op == 1 else BRANCH[op]
        target = (pc + 4 + (simm << 2)) & 0xffffffff
        reads = {rs} if op == 1 or op in (6, 7) else {rs, rt}
        d.update(mn=mn, reads=reads, control=True, target=target,
                 text=f"{mn} " + ",".join(reg(x) for x in sorted(reads)) + f",0x{target:08X}")
        return d
    if op in IMMOPS:
        mn = IMMOPS[op]
        value = imm if op in (12, 13, 14) else simm
        d.update(mn=mn, reads={rs}, writes=rt,
                 text=f"{mn} {reg(rt)},{reg(rs)},0x{value & 0xffffffff:X}")
        return d
    if op == 15:
        d.update(mn="lui", writes=rt, text=f"lui {reg(rt)},0x{imm:04X}")
        return d
    if op in MEMOPS:
        mn, width, rw = MEMOPS[op]
        reads = {rs} if rw == "R" else {rs, rt}
        d.update(mn=mn, reads=reads, writes=rt if rw == "R" else None,
                 mem=(rw, width, simm, rs, rt), text=f"{mn} {reg(rt)},{simm}({reg(rs)})")
        return d
    return d

def independent_decode(raw: bytes, pc: int) -> str:
    if len(raw) != 4:
        raise ValueError("INDEPENDENT_DECODER_WORD_LENGTH")
    w = int.from_bytes(raw, "little")
    op, rs, rt = (w >> 26) & 63, (w >> 21) & 31, (w >> 16) & 31
    rd, sa, fn = (w >> 11) & 31, (w >> 6) & 31, w & 63
    u = w & 65535
    s = u - 65536 if u & 32768 else u
    rr = lambda n: "$" + REGS[n]
    if op == 0:
        name = SPECIAL.get(fn, ".word")
        if name in ("sll", "srl", "sra"):
            return f"{name} {rr(rd)},{rr(rt)},{sa}"
        if name in ("sllv", "srlv", "srav"):
            return f"{name} {rr(rd)},{rr(rt)},{rr(rs)}"
        if name == "jr":
            return f"jr {rr(rs)}"
        if name == "jalr":
            return f"jalr {rr(rd)},{rr(rs)}"
        if name in ("mfhi", "mflo"):
            return f"{name} {rr(rd)}"
        if name in ("mthi", "mtlo"):
            return f"{name} {rr(rs)}"
        if name in ("mult", "multu", "div", "divu"):
            return f"{name} {rr(rs)},{rr(rt)}"
        if name in ("syscall", "break"):
            return name
        if name != ".word":
            return f"{name} {rr(rd)},{rr(rs)},{rr(rt)}"
        return f".word 0x{w:08X}"
    if op in (2, 3):
        dest = (((pc + 4) >> 28) << 28) | ((w & 0x03ffffff) << 2)
        return f"{'j' if op == 2 else 'jal'} 0x{dest:08X}"
    if op in (1, 4, 5, 6, 7):
        name = {0: "bltz", 1: "bgez", 16: "bltzal", 17: "bgezal"}.get(rt, "regimm") if op == 1 else BRANCH[op]
        dest = (pc + 4 + (s << 2)) & 0xffffffff
        args = rr(rs) if op == 1 or op in (6, 7) else rr(rs) + "," + rr(rt)
        return f"{name} {args},0x{dest:08X}"
    if op in IMMOPS:
        name = IMMOPS[op]
        val = u if op in (12, 13, 14) else s
        return f"{name} {rr(rt)},{rr(rs)},0x{val & 0xffffffff:X}"
    if op == 15:
        return f"lui {rr(rt)},0x{u:04X}"
    if op in MEMOPS:
        name = MEMOPS[op][0]
        return f"{name} {rr(rt)},{s}({rr(rs)})"
    return f".word 0x{w:08X}"

def write_tsv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t",
                                extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

def read_tsv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))

def nearest_def(ins: list[dict], before: int, register: int, limit: int = 160):
    crossed = []
    for q in range(before - 1, max(-1, before - limit - 1), -1):
        d = ins[q]
        if d["writes"] == register:
            return q, crossed
        if d["control"]:
            crossed.append(q)
    return None, crossed

def absolute_constant(ins: list[dict], before: int, register: int, limit: int = 96,
                      active: set[tuple[int, int]] | None = None):
    if register == 0:
        return 0, []
    active = active or set()
    key = (before, register)
    if key in active:
        return None, []
    active.add(key)
    q, _ = nearest_def(ins, before, register, limit)
    if q is None:
        active.discard(key)
        return None, []
    d = ins[q]
    value = None
    chain = [q]
    if d["mn"] == "lui":
        value = d["imm"] << 16
    elif d["mn"] in ("addiu", "addi", "ori", "andi") and d["rs"] != 0:
        base, sub = absolute_constant(ins, q, d["rs"], limit, active)
        chain.extend(sub)
        if base is not None:
            value = ((base + d["simm"]) if d["mn"] in ("addiu", "addi")
                     else (base | d["imm"]) if d["mn"] == "ori" else base & d["imm"])
    elif d["mn"] in ("addiu", "addi") and d["rs"] == 0:
        value = d["simm"]
    active.discard(key)
    return (value & 0xffffffff if value is not None else None), sorted(set(chain))

def expression(ins: list[dict], before: int, register: int, depth: int = 0,
               active: set[tuple[int, int]] | None = None):
    if register == 0:
        return ("const", 0), []
    if depth > 24:
        return None, []
    active = active or set()
    key = (before, register)
    if key in active:
        return None, []
    active.add(key)
    q, crossed = nearest_def(ins, before, register, 128)
    if q is None:
        active.discard(key)
        return ("sym", REGS[register], 1), []
    d = ins[q]
    chain = [q]
    val = None
    if d["mn"] == "lui":
        val = ("const", d["imm"] << 16)
    elif d["mn"] in ("addiu", "addi", "ori", "andi"):
        a, sub = expression(ins, q, d["rs"], depth + 1, active)
        chain.extend(sub)
        if a and a[0] == "const":
            n = a[1]
            if d["mn"] in ("addiu", "addi"):
                n += d["simm"]
            elif d["mn"] == "ori":
                n |= d["imm"]
            else:
                n &= d["imm"]
            val = ("const", n & 0xffffffff)
        elif a and d["mn"] in ("addiu", "addi"):
            val = ("offset", a, d["simm"])
        elif a:
            val = ("derived", a, d["mn"], d["imm"])
    elif d["mn"] in ("lw", "lh", "lhu", "lb", "lbu"):
        base, sub = expression(ins, q, d["rs"], depth + 1, active)
        chain.extend(sub)
        if base and base[0] == "const":
            ea = (base[1] + d["mem"][2]) & 0xffffffff
            val = ("pointer", ea) if d["mn"] == "lw" and ea == RAM_POINTER else ("load", ea, d["mn"])
        elif base:
            val = ("load_from", base, d["mem"][2], d["mn"])
    elif d["mn"] in ("sll", "srl", "sra"):
        a, sub = expression(ins, q, d["rt"], depth + 1, active)
        chain.extend(sub)
        if a and a[0] == "sym":
            factor = a[2] * (1 << d["sh"]) if d["mn"] == "sll" else None
            val = ("sym", a[1], factor) if factor is not None else ("derived", a, d["mn"], d["sh"])
        elif a and a[0] == "const":
            factor = a[1] << d["sh"] if d["mn"] == "sll" else a[1] >> d["sh"]
            val = ("const", factor & 0xffffffff)
        elif a:
            val = ("derived", a, d["mn"], d["sh"])
    elif d["mn"] in ("addu", "add", "sub", "subu", "or"):
        left, lc = expression(ins, q, d["rs"], depth + 1, active)
        right, rc = expression(ins, q, d["rt"], depth + 1, active)
        chain.extend(lc + rc)
        if d["mn"] == "or" and left == ("const", 0):
            val = right
        elif d["mn"] == "or" and right == ("const", 0):
            val = left
        elif left and right and left[0] == "const" and right[0] == "const":
            n = (left[1] + right[1]) if d["mn"] in ("addu", "add") else (
                left[1] - right[1]) if d["mn"] in ("sub", "subu") else left[1] | right[1]
            val = ("const", n & 0xffffffff)
        elif left and right and left[0] == "sym" and right[0] == "sym" and left[1] == right[1]:
            if d["mn"] in ("addu", "add"):
                val = ("sym", left[1], left[2] + right[2])
        elif left and right and left[0] == "pointer" and right[0] == "sym":
            val = ("record_candidate", left[1], right[1], right[2])
        elif right and left and right[0] == "pointer" and left[0] == "sym":
            val = ("record_candidate", right[1], left[1], left[2])
        elif left and right and left[0] == "offset" and right[0] == "sym":
            val = ("offset_index", left, right)
        elif right and left and right[0] == "offset" and left[0] == "sym":
            val = ("offset_index", right, left)
        elif left and left[0] == "sym" and right == ("const", 0):
            val = left
        elif right and right[0] == "sym" and left == ("const", 0):
            val = right
        elif left and left[0] == "pointer" and right == ("const", 0):
            val = left
        elif right and right[0] == "pointer" and left == ("const", 0):
            val = right
    elif d["mn"] in ("mult", "multu"):
        left, lc = expression(ins, q, d["rs"], depth + 1, active)
        right, rc = expression(ins, q, d["rt"], depth + 1, active)
        chain.extend(lc + rc)
        if left and right and left[0] == "sym" and right[0] == "const":
            val = ("sym", left[1], left[2] * right[1])
        elif right and left and right[0] == "sym" and left[0] == "const":
            val = ("sym", right[1], right[2] * left[1])
    active.discard(key)
    if crossed:
        chain.extend(crossed)
    return val, sorted(set(chain))

def base_class(ins: list[dict], index: int, base: int) -> tuple[str, str, list[int]]:
    expr, chain = expression(ins, index, base)
    if expr and expr[0] == "record_candidate" and expr[1] == RAM_POINTER and expr[3] == STRIDE:
        return "EA84_PLUS_INDEX_X_0x124", repr(expr), chain
    if expr and expr[0] == "pointer" and expr[1] == RAM_POINTER:
        return "EA84_POINTER", repr(expr), chain
    if expr and expr[0] == "const":
        return "ABSOLUTE_0x%08X" % expr[1], repr(expr), chain
    if expr:
        return "REGISTER_DERIVED_UNPROVEN", repr(expr), chain
    return "TIDAK TAHU", "TIDAK TAHU", chain

def origin_of(ins: list[dict], before: int, register: int, base_pc: int,
              depth: int = 0) -> tuple[str, str, str]:
    if depth > 16:
        return "TIDAK TAHU", "DEPTH_LIMIT", ""
    q, crossed = nearest_def(ins, before, register, 128)
    if q is None:
        kind = "INCOMING_ARGUMENT" if register in (4, 5, 6, 7) else "INCOMING_REGISTER"
        return kind, f"{reg(register)} has no earlier definition in bounded scan", ""
    d = ins[q]
    chain = f"0x{base_pc + 4*q:08X}:{d['text']}"
    if d["mn"] == "addu" and d["rd"] == d["rs"] and d["rt"] == 0:
        kind, detail, sub = origin_of(ins, q, d["rs"], base_pc, depth + 1)
        return kind, detail, chain + (";" + sub if sub else "")
    if d["mn"] in ("addu", "or") and d["rd"] == d["rt"] and d["rs"] == 0:
        kind, detail, sub = origin_of(ins, q, d["rt"], base_pc, depth + 1)
        return kind, detail, chain + (";" + sub if sub else "")
    if d["mn"] in ("lw", "lh", "lhu", "lb", "lbu"):
        address, address_chain = absolute_constant(ins, q, d["rs"])
        if address is not None:
            ea = (address + d["mem"][2]) & 0xffffffff
            relation = "EA84_POINTER_LOAD" if ea == RAM_POINTER and d["mn"] == "lw" else "GLOBAL_MEMORY_LOAD"
            text = f"EA=0x{ea:08X}; {d['mn']} width={d['mem'][1]}"
            return relation, text, chain + ";" + ";".join(
                f"0x{base_pc+4*x:08X}:{ins[x]['text']}" for x in address_chain)
        if d["rs"] == 29:
            return "STACK_LOAD", f"{d['mn']} from {reg(d['rs'])}{d['mem'][2]:+d}", chain
        if d["rs"] == 28:
            return "GP_RELATIVE_LOAD", f"{d['mn']} gp{d['mem'][2]:+d}", chain
        return "MEMORY_LOAD_BASE_UNRESOLVED", d["text"], chain
    if d["mn"] in ("addiu", "addi") and d["rs"] == 0:
        return "CONSTANT", f"{reg(register)}={d['simm']}", chain
    if d["mn"] in ("lui", "ori", "andi", "addiu", "addi", "sll", "srl", "sra",
                   "addu", "add", "sub", "subu", "and", "or", "xor"):
        return "REGISTER_DERIVED", f"defined by {d['text']}", chain
    control_note = "; crossed control-flow predecessor(s)" if crossed else ""
    return "TIDAK TAHU", d["text"] + control_note, chain

def find_instruction(regions: dict[str, tuple[int, list[dict], bytes]], pc: int):
    for name, (base, ins, _) in regions.items():
        idx = (pc - base) // 4
        if 0 <= idx < len(ins) and base + idx * 4 == pc:
            return name, base, ins, idx
    return None

def first_v0_consumers(ins: list[dict], start: int, base_pc: int, region: str,
                       call_pc: int, max_steps: int = 32) -> list[dict]:
    queue = [(start, 0, "ROOT")]
    seen = set()
    rows = []
    found_paths = set()
    while queue:
        idx, steps, path = queue.pop(0)
        if idx < 0 or idx >= len(ins) or steps >= max_steps or (idx, steps, path) in seen:
            continue
        seen.add((idx, steps, path))
        d = ins[idx]
        pc = base_pc + 4 * idx
        if 2 in d["reads"]:
            key = (pc, path)
            if key not in found_paths:
                rows.append({"region": region, "call_pc": f"0x{call_pc:08X}",
                    "return_pc": f"0x{base_pc+4*start:08X}", "path_id": path,
                    "step": steps + 1, "consumer_pc": f"0x{pc:08X}",
                    "file_offset": f"0x{(pc - base_pc):08X}",
                    "instruction": d["text"],
                    "use_kind": "READ_BEFORE_OR_WITH_WRITE" if d["writes"] == 2 else "READ",
                    "operand_registers": ",".join(reg(x) for x in sorted(d["reads"])),
                    "delay_slot_path": "DELAY_SLOT" if steps > 0 and ins[idx-1]["control"] else "NORMAL",
                    "status": "FIRST_V0_USE_ON_PATH"})
                found_paths.add(key)
            continue
        if d["writes"] == 2:
            continue
        if d["mn"] in ("jal", "jalr", "jr", "j"):
            delay = idx + 1
            if delay < len(ins) and 2 in ins[delay]["reads"]:
                dd = ins[delay]
                rows.append({"region": region, "call_pc": f"0x{call_pc:08X}",
                    "return_pc": f"0x{base_pc+4*start:08X}", "path_id": path + "_DELAY",
                    "step": steps + 2, "consumer_pc": f"0x{base_pc+4*delay:08X}",
                    "file_offset": f"0x{4*delay:08X}", "instruction": dd["text"],
                    "use_kind": "DELAY_SLOT_READ", "operand_registers": ",".join(reg(x) for x in sorted(dd["reads"])),
                    "delay_slot_path": "DELAY_SLOT", "status": "FIRST_V0_USE_ON_PATH"})
                continue
            if d["mn"] in ("jal", "jalr", "jr"):
                continue
            if d["mn"] == "j" and d["target"] is not None and delay < len(ins) and ins[delay]["writes"] != 2:
                target_index = (d["target"] - base_pc) // 4
                queue.append((target_index, steps + 2, path + "_JUMP"))
            continue
        if d["control"] and d["target"] is not None:
            delay = idx + 1
            if delay < len(ins):
                dd = ins[delay]
                if 2 in dd["reads"]:
                    rows.append({"region": region, "call_pc": f"0x{call_pc:08X}",
                        "return_pc": f"0x{base_pc+4*start:08X}", "path_id": path + "_BR_DELAY",
                        "step": steps + 2, "consumer_pc": f"0x{base_pc+4*delay:08X}",
                        "file_offset": f"0x{4*delay:08X}", "instruction": dd["text"],
                        "use_kind": "DELAY_SLOT_READ", "operand_registers": ",".join(reg(x) for x in sorted(dd["reads"])),
                        "delay_slot_path": "DELAY_SLOT", "status": "FIRST_V0_USE_ON_PATH"})
                elif dd["writes"] != 2:
                    queue.append((idx + 2, steps + 2, path + "_FALLTHROUGH"))
                    target_index = (d["target"] - base_pc) // 4
                    queue.append((target_index, steps + 2, path + "_TAKEN"))
            continue
        queue.append((idx + 1, steps + 1, path))
    return rows

def global_access(ins: list[dict], index: int, d: dict) -> tuple[int | None, int | None, list[int]]:
    base, chain = absolute_constant(ins, index, d["rs"])
    if base is None or d["mem"] is None:
        return None, None, chain
    return (base + d["mem"][2]) & 0xffffffff, base, chain

def nibble_effect(mask_ops: str) -> tuple[list[str], str, str]:
    effects = ["PRESERVED"] * 4
    immediates = []
    or_sources = []
    ops = [x for x in mask_ops.split(";") if x.strip()]
    for raw in ops:
        item = raw.strip()
        match = re.search(r"\b(andi|ori|xori)\s+\$\w+,\$\w+,0x([0-9A-Fa-f]+)", item)
        if match:
            op, text = match.groups()
            imm = int(text, 16) & 0xffff
            immediates.append(f"0x{imm:04X}")
            for bit in range(8, 12):
                index = bit - 8
                if op == "andi" and not (imm & (1 << bit)):
                    effects[index] = "DIBERSIHKAN"
                elif op == "ori" and imm & (1 << bit):
                    effects[index] = "DISET"
                    or_sources.append(f"{item};imm=0x{imm:04X}")
                elif op == "xori" and imm & (1 << bit):
                    effects[index] = "TOGGLE_BERGANTUNG_NILAI_LAMA"
        elif re.search(r"\b(sll|srl|sra|sllv|srlv|srav)\b", item):
            effects = ["TIDAK TAHU"] * 4
        elif re.search(r"\b(or|xor|and)\b", item):
            effects = ["TIDAK TAHU"] * 4
    return effects, ",".join(immediates) or "TIDAK TAHU", ";".join(or_sources) or "TIDAK ADA_OR_IMMEDIATE_TERAMATI"

def main_static(exe_path: Path, data_path: Path, rmw_path: Path, out: Path) -> int:
    exe = exe_path.read_bytes()
    data = data_path.read_bytes()
    if len(exe) != EXE_SIZE or sha256(exe) != EXE_SHA:
        raise SystemExit("UQ0_EXE_IDENTITY_MISMATCH")
    if len(data) != DATA_SIZE or sha256(data) != DATA_SHA:
        raise SystemExit("UQ0_DATA_BIN_IDENTITY_MISMATCH")
    e1 = data[ENTRY1_IN_DATA:ENTRY1_IN_DATA + E1_SIZE]
    if len(e1) != E1_SIZE or sha256(e1) != ENTRY1_SHA:
        raise SystemExit("UQ0_ENTRY1_IDENTITY_MISMATCH")
    regions = {}
    for name, base, blob in (("EXE", EXE_BASE, exe[EXE_OFF:]),
                             ("ENTRY1", E1_BASE, e1)):
        instructions = [dec(blob[p:p+4], base+p) for p in range(0, len(blob)-3, 4)]
        regions[name] = (base, instructions, blob)
    caller_rows = []
    call_sites = []
    for name, (base, ins, blob) in regions.items():
        for idx, d in enumerate(ins):
            if d["mn"] != "jal" or d["target"] not in TARGETS:
                continue
            pc = base + 4 * idx
            delay = ins[idx+1] if idx+1 < len(ins) else None
            delay_pc = pc + 4
            setup = {}
            for r in range(4, 8):
                def_idx, crossed = nearest_def(ins, idx + 2, r, 160)
                if def_idx is None:
                    setup[r] = ("TIDAK TAHU", "NO_DEF_WITHIN_160_INSTRUCTIONS", "",
                                "TIDAK TAHU")
                    continue
                q = def_idx
                kind, detail, chain = origin_of(ins, idx + 2, r, base)
                text_chain = chain or f"0x{base+4*q:08X}:{ins[q]['text']}"
                status = "LINEAR_DEF_CROSSES_CONTROL" if crossed else "DEF_FOUND_AFTER_DELAY_SLOT"
                setup[r] = (f"0x{base+4*q:08X}:{ins[q]['text']}", kind, text_chain, status)
            row = {"region": name, "call_pc": f"0x{pc:08X}",
                   "file_offset": f"0x{(pc-base + (EXE_OFF if name=='EXE' else E1_OFF)):08X}",
                   "jal_bytes": " ".join(f"{x:02X}" for x in blob[idx*4:idx*4+4]),
                   "jal": d["text"], "target_pc": f"0x{d['target']:08X}",
                   "target_name": TARGET_NAMES[d["target"]],
                   "delay_slot_pc": f"0x{delay_pc:08X}" if delay else "",
                   "delay_slot": delay["text"] if delay else "TIDAK TAHU"}
            for r in range(4, 8):
                label = f"a{r-4}"
                row[f"setup_{label}"], row[f"origin_{label}"], row[f"chain_{label}"], row[f"status_{label}"] = setup[r]
            caller_rows.append(row)
            call_sites.append((name, base, ins, idx, pc))
    consumer_rows = []
    for name, base, ins, idx, pc in call_sites:
        consumer_rows.extend(first_v0_consumers(ins, idx+2, base, name, pc, 32))
    access_rows = []
    loader_rows = []
    nibble_rows = []
    global_rows = []
    validation_points = set()
    for name, (base, ins, blob) in regions.items():
        for idx, d in enumerate(ins):
            pc = base + 4*idx
            if d["mem"] is None:
                if d["mn"] == "lw":
                    pass
                else:
                    continue
            rw, width, disp, rs, rt = d["mem"] if d["mem"] else ("", 0, 0, 0, 0)
            if d["mem"] and (d["mn"] in ("lbu", "lb") and disp == 11 or
                             d["mn"] in ("sb", "sh", "sw", "swl", "swr") and
                             ((d["mn"] == "sb" and disp == 11) or
                              (d["mn"] == "sh" and disp in (10, 11)) or
                              (d["mn"] == "sw" and 8 <= disp <= 11) or
                              (d["mn"] in ("swl", "swr") and 8 <= disp <= 11))):
                bclass, bexpr, _ = base_class(ins, idx, rs)
                access_rows.append({"region": name, "pc": f"0x{pc:08X}",
                    "file_offset": f"0x{(pc-base + (EXE_OFF if name=='EXE' else E1_OFF)):08X}",
                    "bytes_4B": " ".join(f"{x:02X}" for x in blob[idx*4:idx*4+4]),
                    "instruction": d["text"], "access_kind": rw, "width": width,
                    "displacement": disp, "base_register": reg(rs), "data_register": reg(rt),
                    "base_class": bclass, "base_expression": bexpr,
                    "field_offset_candidate": "0x0B", "access_status":
                    "READER_LB_LBU_DISP_11" if rw == "R" else
                    "STORE_COVERS_0x0B_CANDIDATE; SWL_SWR_BYTE_LANES_REQUIRE_RUNTIME_OR_ENDIAN_CONFIRMATION"})
                validation_points.add((name, idx))
            if d["mem"] and d["mn"] == "lw":
                ea, _, _ = global_access(ins, idx, d)
                if ea == RAM_POINTER:
                    prior = ins[max(0, idx-12):idx]
                    scale = " ".join(x["mn"] for x in prior if x["mn"] in ("sll", "addu", "addiu", "mult", "multu"))
                    loader_rows.append({"region": name, "pc": f"0x{pc:08X}",
                        "file_offset": f"0x{(pc-base + (EXE_OFF if name=='EXE' else E1_OFF)):08X}",
                        "instruction": d["text"], "global_ea": f"0x{ea:08X}",
                        "relationship_to_EA84": "DIRECT_POINTER_LOAD",
                        "nearby_index_scale_pattern": scale or "NONE_VISIBLE",
                        "status": "BYTE_ADDRESS_PROVEN; record-index relationship evaluated at consumer"})
                    validation_points.add((name, idx))
            if d["mem"] and d["mem"][0] == "W":
                bclass, bexpr, _ = base_class(ins, idx, rs)
                overlaps = (d["mn"] == "sb" and disp == 0x21) or (
                    d["mn"] == "sh" and disp in (0x1f, 0x20)) or (
                    d["mn"] == "sw" and 0x1e <= disp <= 0x21) or (
                    d["mn"] in ("swl", "swr") and 0x1d <= disp <= 0x22)
                if overlaps and ("EA84" in bclass or bclass == "REGISTER_DERIVED_UNPROVEN"):
                    nibble_rows.append({"region": name, "pc": f"0x{pc:08X}",
                        "file_offset": f"0x{(pc-base + (EXE_OFF if name=='EXE' else E1_OFF)):08X}",
                        "instruction": d["text"], "base_register": reg(rs), "base_class": bclass,
                        "base_expression": bexpr, "target_offset": f"{disp:#x}",
                        "bit8_11_effect": "TIDAK TAHU; source value path must be classified per store",
                        "source_register": reg(rt), "status": "POTENTIAL_NIBBLE_WRITER"})
                validation_points.add((name, idx))
    # Explicitly resolve caller-loaded globals used by the two named caller setups.
    for name, pc in (("ENTRY1", 0x800D6934), ("ENTRY1", 0x800F04C0)):
        hit = find_instruction(regions, pc)
        if not hit:
            global_rows.append({"region": name, "load_pc": f"0x{pc:08X}",
                "instruction": "TIDAK DITEMUKAN", "global_ea": "TIDAK TAHU",
                "global_role": "TIDAK TAHU", "static_writer_pcs": "TIDAK TAHU",
                "ea84_chain_status": "TIDAK TAHU"})
            continue
        _, base, ins, idx = hit
        d = ins[idx]
        ea, lui_base, chain = global_access(ins, idx, d)
        lui_idx = next((q for q in chain if ins[q]["mn"] == "lui"), None)
        writer_pcs = []
        if ea is not None:
            for rname, (rbase, rins, _) in regions.items():
                for ri, wd in enumerate(rins):
                    if wd["mem"] and wd["mem"][1] == "W":
                        w_ea, _, _ = global_access(rins, ri, wd)
                        if w_ea == ea:
                            writer_pcs.append(f"0x{rbase+4*ri:08X}:{wd['text']}")
        global_rows.append({"region": name, "load_pc": f"0x{pc:08X}",
            "instruction": d["text"],
            "base_lui_pc": f"0x{base+4*lui_idx:08X}" if lui_idx is not None else "TIDAK TAHU",
            "base_lui": ins[lui_idx]["text"] if lui_idx is not None else "TIDAK TAHU",
            "global_ea": f"0x{ea:08X}" if ea is not None else "TIDAK TAHU",
            "global_role": "GLOBAL_LOAD_SOURCE; not proven EA84 pointer/record",
            "static_writer_pcs": ";".join(writer_pcs) or "TIDAK DITEMUKAN",
            "ea84_chain_status": "TIDAK TAHU; no complete pointer+index*0x124 chain to caller's a0"})
        validation_points.add((name, idx))
    prior_rmw = read_tsv(rmw_path)
    rmw_rows = []
    for row in prior_rmw:
        effects, immediates, or_source = nibble_effect(row.get("mask_ops", ""))
        mask_text = row.get("mask_immediates", "")
        mask_values = [int(x, 16) for x in re.findall(r"0x([0-9A-Fa-f]+)", mask_text)]
        clears_all = all((m & 0x0f00) == 0 for m in mask_values) if mask_values else False
        clear_note = "YES" if clears_all and mask_values else (
            "NO" if mask_values and all((m & 0x0f00) == 0x0f00 for m in mask_values) else "MIXED_OR_UNKNOWN")
        rmw_rows.append({"region": row.get("region", ""), "load_pc": row.get("load_pc", ""),
            "mask_ops": row.get("mask_ops", ""), "store_pc": row.get("store_pc", ""),
            "store_instruction": row.get("store_instruction", ""), "mask_immediates": immediates,
            "bit8_effect": effects[0], "bit9_effect": effects[1], "bit10_effect": effects[2],
            "bit11_effect": effects[3], "or_source": or_source, "suspected_clear_mask": clear_note,
            "status": "BYTE_SEQUENCE_MASK_ONLY; old halfword/data source is not inferred"})
    # Add all first-v0-use instructions to the independent decoder cross-check set.
    for row in consumer_rows:
        hit = find_instruction(regions, int(row["consumer_pc"], 16))
        if hit:
            validation_points.add((hit[0], hit[3]))
    # Preserve enough bytes to decode-check every emitted instruction row independently.
    for _, _, _, idx, _ in call_sites:
        pass
    for row in access_rows:
        hit = find_instruction(regions, int(row["pc"], 16))
        if hit:
            validation_points.add((hit[0], hit[3]))
    for row in caller_rows:
        hit = find_instruction(regions, int(row["call_pc"], 16))
        if hit:
            validation_points.add((hit[0], hit[3]))
            validation_points.add((hit[0], hit[3]+1))
    validation_rows = []
    for name, idx in sorted(validation_points):
        base, ins, blob = regions[name]
        pc = base + idx*4
        raw = blob[idx*4:idx*4+4]
        scan_text = ins[idx]["text"]
        independent_text = independent_decode(raw, pc)
        validation_rows.append({"region": name, "pc": f"0x{pc:08X}",
            "file_offset": f"0x{(pc-base + (EXE_OFF if name=='EXE' else E1_OFF)):08X}",
            "bytes_4B": " ".join(f"{x:02X}" for x in raw),
            "scan_instruction": scan_text, "independent_instruction": independent_text,
            "match": "YES" if scan_text == independent_text else "NO"})
    out.mkdir(parents=True, exist_ok=True)
    write_tsv(out/"UQ0_CALLERS.tsv", FIELDS["callers"], caller_rows)
    write_tsv(out/"UQ0_V0_CONSUMERS.tsv", FIELDS["consumers"], consumer_rows)
    write_tsv(out/"UQ0_SELECTOR_BYTE_ACCESS.tsv", FIELDS["access"], access_rows)
    write_tsv(out/"UQ0_RECORD_LOADERS.tsv", FIELDS["loaders"], loader_rows)
    write_tsv(out/"UQ0_NIBBLE_RMW.tsv", FIELDS["rmw"], rmw_rows)
    write_tsv(out/"UQ0_NIBBLE_WRITERS.tsv", FIELDS["nibble"], nibble_rows)
    write_tsv(out/"UQ0_EA84_GLOBALS.tsv", FIELDS["globals"], global_rows)
    write_tsv(out/"UQ0_DECODE_VALIDATION.tsv", FIELDS["validation"], validation_rows)
    # Counts are re-read from the TSVs themselves, not copied from in-memory expectations.
    callers_n = len(read_tsv(out/"UQ0_CALLERS.tsv"))
    f770c = sum(x["target_pc"] == "0x800B770C" for x in read_tsv(out/"UQ0_CALLERS.tsv"))
    f76bc = sum(x["target_pc"] == "0x800B76BC" for x in read_tsv(out/"UQ0_CALLERS.tsv"))
    consumers_n = len(read_tsv(out/"UQ0_V0_CONSUMERS.tsv"))
    access_from_tsv = read_tsv(out/"UQ0_SELECTOR_BYTE_ACCESS.tsv")
    readers_n = sum(x["access_kind"] == "R" for x in access_from_tsv)
    writers_n = sum(x["access_kind"] == "W" for x in access_from_tsv)
    rmw_n = len(read_tsv(out/"UQ0_NIBBLE_RMW.tsv"))
    nibble_n = len(read_tsv(out/"UQ0_NIBBLE_WRITERS.tsv"))
    validation = read_tsv(out/"UQ0_DECODE_VALIDATION.tsv")
    mismatches = sum(x["match"] != "YES" for x in validation)
    globals_rows = read_tsv(out/"UQ0_EA84_GLOBALS.tsv")
    summary = [
        "UQ0_STATIC_CALLER_CONSUMER_SELECTOR_AND_NIBBLE_AUDIT",
        "STATUS=" + ("TUNTAS" if callers_n == 45 and f770c == 44 and f76bc == 1 and rmw_n == 28 and mismatches == 0 else "SEBAGIAN"),
        "EVIDENCE=K4 maksimum; byte statis EXE dan Entry 1; tidak memberi makna gameplay",
        f"EXE_SHA256={EXE_SHA}", f"DATA_BIN_SHA256={DATA_SHA}", f"ENTRY1_SHA256={ENTRY1_SHA}",
        f"DIRECT_CALLER_ROWS={callers_n}", f"CALLS_TO_800B770C={f770c}",
        f"CALLS_TO_800B76BC={f76bc}", f"V0_FIRST_USE_ROWS={consumers_n}",
        f"SELECTOR_BYTE_READ_ROWS={readers_n}", f"SELECTOR_BYTE_WRITE_CANDIDATE_ROWS={writers_n}",
        f"EA84_POINTER_LOAD_ROWS={len(read_tsv(out/'UQ0_RECORD_LOADERS.tsv'))}",
        f"U16_PLUS_0x20_RMW_ROWS={rmw_n}", f"OTHER_NIBBLE_WRITER_CANDIDATES={nibble_n}",
        f"EA84_GLOBAL_SOURCE_ROWS={len(globals_rows)}",
        "EA84_GLOBAL_RELATION_FOR_0x800D6934_AND_0x800F04C0=TIDAK TAHU unless complete EA84+index*0x124 chain is present",
        f"INDEPENDENT_DECODE_ROWS={len(validation)}", f"INDEPENDENT_DECODE_MISMATCHES={mismatches}",
        "SELECTOR_DATA_TABLE_SOURCE=TIDAK TAHU; static byte source/initializer not proven",
        "CALLER_ARG_PROVENANCE=bounded reaching definitions searched after jal delay slot; unresolved or control-flow ambiguous values remain TIDAK TAHU",
        "V0_CONSUMER_SCOPE=32 instructions per CFG path; both outcomes of conditional branches and delay slots included",
        "MASK_BITS=8,9,10,11 of rec+0x20; OR sources without a literal are TIDAK TAHU",
        "GAMEPLAY_MEANING=TIDAK TAHU"
    ]
    (out/"UQ0_SUMMARY.txt").write_text("\n".join(summary)+"\n", encoding="utf-8")
    print("\n".join(summary), flush=True)
    return 0 if "STATUS=TUNTAS" in summary else 2

def self_test() -> None:
    pc = 0x80010000
    raw = ((5 << 26) | (8 << 21) | (9 << 16) | 3).to_bytes(4, "little")
    assert dec(raw, pc)["text"] == "bne $t0,$t1,0x80010010"
    assert independent_decode(raw, pc) == dec(raw, pc)["text"]
    assert dec((0x03 << 26 | (0x000B770C >> 2)).to_bytes(4, "little"), pc)["mn"] == "jal"
    assert nibble_effect("0x800D471C:andi $v1,$v1,0xF0FF")[0] == [
        "DIBERSIHKAN", "DIBERSIHKAN", "DIBERSIHKAN", "DIBERSIHKAN"]
    assert nibble_effect("0x800B441C:andi $v1,$v1,0x0F0F")[0] == [
        "PRESERVED", "PRESERVED", "PRESERVED", "PRESERVED"]
    print("UQ0_SELF_TEST=PASS MIPS decode, independent decoder, jal and nibble mask effects")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exe", type=Path)
    parser.add_argument("--data-bin", type=Path)
    parser.add_argument("--prior-rmw-tsv", type=Path)
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not all((args.exe, args.data_bin, args.prior_rmw_tsv, args.out_dir)):
        parser.error("--exe --data-bin --prior-rmw-tsv --out-dir required")
    return main_static(args.exe, args.data_bin, args.prior_rmw_tsv, args.out_dir)

if __name__ == "__main__":
    raise SystemExit(main())
