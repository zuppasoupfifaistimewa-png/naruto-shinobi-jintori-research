#!/usr/bin/env python3
"""Bounded raw MIPS scan for indirect-call candidates targeting FUN_800D15A8.

This scans executable code bytes from the PS-X EXE and Entry 1 and exact pointer
words across the complete raw DATA.BIN archive. It does not disassemble packed
DATA.BIN entries or infer function boundaries from raw bytes.
"""
from __future__ import annotations
import argparse
import hashlib
import struct
from pathlib import Path

TARGET = 0x800D15A8
REGS = ("zero","at","v0","v1","a0","a1","a2","a3",
        "t0","t1","t2","t3","t4","t5","t6","t7",
        "s0","s1","s2","s3","s4","s5","s6","s7",
        "t8","t9","k0","k1","gp","sp","fp","ra")

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sign16(v: int) -> int:
    return v - 0x10000 if v & 0x8000 else v

def decode_jalr(word: int) -> int | None:
    if (word >> 26) == 0 and (word & 0x3F) == 9:
        return (word >> 21) & 31
    return None

def write_reg(word: int) -> int | None:
    op = word >> 26
    fn = word & 0x3F
    if op == 0:
        if fn in {0x00,0x02,0x03,0x04,0x06,0x07,0x10,0x12,0x21,0x23,
                  0x24,0x25,0x26,0x27,0x2A,0x2B}:
            return (word >> 11) & 31
        return None
    if op in {0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,
              0x20,0x21,0x23,0x24,0x25,0x26,0x27}:
        return (word >> 16) & 31
    return None

def const_step(word: int, values: dict[int,int]) -> None:
    op = word >> 26
    rs, rt, rd = (word >> 21) & 31, (word >> 16) & 31, (word >> 11) & 31
    imm = word & 0xFFFF
    fn = word & 0x3F
    dest = write_reg(word)
    if dest is None or dest == 0:
        return
    value = None
    if op == 0x0F:  # lui
        value = (imm << 16) & 0xFFFFFFFF
    elif op == 0x09 and rs in values:  # addiu
        value = (values[rs] + sign16(imm)) & 0xFFFFFFFF
    elif op == 0x0D and rs in values:  # ori
        value = (values[rs] | imm) & 0xFFFFFFFF
    elif op == 0 and fn == 0x21 and rs in values and rt in values:  # addu
        value = (values[rs] + values[rt]) & 0xFFFFFFFF
    elif op == 0 and fn == 0x25 and rs in values and rt in values:  # or
        value = (values[rs] | values[rt]) & 0xFFFFFFFF
    elif op == 0 and fn == 0x21 and (rs == 0 or rt == 0):  # move alias
        src = rt if rs == 0 else rs
        if src in values:
            value = values[src]
    values.pop(dest, None)
    if value is not None:
        values[dest] = value
    if 0 in values:
        values.pop(0, None)

def word_line(pc: int, word: int) -> str:
    op = word >> 26
    rs, rt, rd = (word >> 21) & 31, (word >> 16) & 31, (word >> 11) & 31
    if op == 0x0F:
        ins = f"lui {REGS[rt]},0x{word & 0xffff:04x}"
    elif op == 0x09:
        ins = f"addiu {REGS[rt]},{REGS[rs]},{sign16(word & 0xffff)}"
    elif op == 0x0D:
        ins = f"ori {REGS[rt]},{REGS[rs]},0x{word & 0xffff:04x}"
    elif op == 0 and (word & 0x3F) == 9:
        ins = f"jalr {REGS[rs]}"
    else:
        ins = f".word 0x{word:08X}"
    return f"0x{pc:08X} [{word.to_bytes(4,'little').hex(' ').upper()}] {ins}"

def scan_code(label: str, data: bytes, base: int, start: int, length: int, out: list[str]) -> None:
    segment = data[start:start+length]
    if len(segment) != length:
        raise SystemExit(f"{label}: code slice length mismatch got={len(segment)} expected={length}")
    jalrs = []
    words = struct.iter_unpack("<I", segment[:len(segment)//4*4])
    decoded = [x[0] for x in words]
    for idx, word in enumerate(decoded):
        reg = decode_jalr(word)
        if reg is None:
            continue
        jalrs.append((idx, reg))
    matches = []
    for idx, reg in jalrs:
        lo = max(0, idx-24)
        regs: dict[int,int] = {}
        for j in range(lo, idx):
            const_step(decoded[j], regs)
        computed = regs.get(reg)
        pc = base + start + idx*4
        if computed == TARGET:
            matches.append((pc,reg))
            out.append(f"JALR_TARGET_REGISTER_MATCH module={label} pc=0x{pc:08X} reg={REGS[reg]} value=0x{computed:08X}")
            for j in range(max(0,idx-12),idx+1):
                out.append("  "+word_line(base+start+j*4,decoded[j]))
    out.append(f"MODULE={label} code_bytes={len(segment)} jalr_instruction_count={len(jalrs)} exact_lui_addiu_ori_matches={len(matches)}")
    # Also inspect all aligned .word candidates in this code slice.
    pointer_offsets = [i for i in range(0,len(segment)-3,4) if struct.unpack_from("<I",segment,i)[0] == TARGET]
    out.append(f"MODULE={label} aligned_target_pointer_word_count={len(pointer_offsets)}")
    for off in pointer_offsets:
        out.append(f"  POINTER_WORD module={label} pc=0x{base+start+off:08X} bytes={segment[off:off+4].hex(' ').upper()}")

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--exe",required=True)
    ap.add_argument("--entry1",required=True)
    ap.add_argument("--data",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    exe_path, entry_path, data_path = map(Path,(args.exe,args.entry1,args.data))
    exe, entry, archive = exe_path.read_bytes(), entry_path.read_bytes(), data_path.read_bytes()
    out=[
        "analysis=bounded little-endian MIPS indirect-call and exact pointer scan",
        f"target=0x{TARGET:08X}",
        "target_semantics=FUN_800D15A8 candidate address from verified Entry 1 static import",
        "EXE_code_mapping=raw offset 0x800 + relative PC base 0x80010000; code size 0x5D800",
        "ENTRY1_code_mapping=static import base 0x800AD450; runtime mapping remains unverified",
        "DATA_BIN_scope=whole raw 66,015,232-byte archive scanned only for exact aligned/unaligned pointer words; compressed entries are not disassembled",
        "JALR_constant_scope=24 prior aligned instructions; recognizes LUI+ADDIU, LUI+ORI, and register copies through ADDU/OR",
        "limitation=other register-indirect forms (pointer loads, computed offsets, relocated tables) are not excluded by a zero result",
        f"EXE_bytes={len(exe)} EXE_sha256={sha(exe)}",
        f"ENTRY1_bytes={len(entry)} ENTRY1_sha256={sha(entry)}",
        f"DATA_BIN_bytes={len(archive)} DATA_BIN_sha256={sha(archive)}",
    ]
    if len(exe) != 385024:
        raise SystemExit(f"EXE_SIZE_MISMATCH={len(exe)}")
    if len(entry) != 596412:
        raise SystemExit(f"ENTRY1_SIZE_MISMATCH={len(entry)}")
    scan_code("MAIN_EXE",exe,0x80010000,0x800,0x5D800,out)
    scan_code("DATA_BIN_ENTRY1",entry,0x800AD450,0,len(entry)//4*4,out)
    target_bytes=struct.pack("<I",TARGET)
    hits=[]
    at=archive.find(target_bytes)
    while at>=0:
        hits.append(at)
        at=archive.find(target_bytes,at+1)
    out.append(f"DATA_BIN_raw_target_pointer_occurrences_byte_aligned_and_unaligned={len(hits)}")
    for off in hits[:500]:
        out.append(f"  DATA_BIN_POINTER_WORD_RAW_OFFSET=0x{off:08X} bytes={archive[off:off+4].hex(' ').upper()}")
    if len(hits)>500:
        out.append(f"DATA_BIN_POINTER_WORD_OUTPUT_TRUNCATED={len(hits)-500}")
    target_jalrs=sum(1 for line in out if line.startswith("JALR_TARGET_REGISTER_MATCH "))
    out.append(f"OVERALL_EXACT_JALR_TARGET_REGISTER_MATCHES={target_jalrs}")
    out.append("INTERPRETATION=zero exact matches does not rule out an indirect call through a runtime-loaded or transformed pointer")
    Path(args.out).write_text("\n".join(out)+"\n",encoding="utf-8")
    print(f"CD1_RAW_SCAN=PASS exact_jalr_matches={target_jalrs} raw_DATA_BIN_pointer_hits={len(hits)}")

if __name__ == "__main__":
    main()
