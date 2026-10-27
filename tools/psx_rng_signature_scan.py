#!/usr/bin/env python3
"""Find an exact LCG signature in a local PS-X EXE and list direct JAL callers.

Narrow static scanner only; not a disassembler or replacement for Ghidra.
"""
from __future__ import annotations
import argparse, hashlib, struct
from pathlib import Path

EXPECTED_SHA256 = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
RNG_WORDS = (0x3C0341C6,0x3C02800A,0x8C423118,0x34634E6D,0x00430018,0x00002012,0x24823039,0x3C01800A,0xAC223118,0x00021402,0x03E00008,0x30427FFF)
SEED_WORDS = (0x3C01800A,0x03E00008,0xAC243118)

def u32(b: bytes, o: int) -> int:
    return struct.unpack_from("<I", b, o)[0]

def find_words(text: bytes, base: int, words: tuple[int, ...]) -> list[int]:
    pat = struct.pack("<" + "I"*len(words), *words)
    out, start = [], 0
    while (idx := text.find(pat, start)) >= 0:
        if idx % 4 == 0: out.append(base+idx)
        start = idx+4
    return out

def calls_to(text: bytes, base: int, target: int) -> list[int]:
    out=[]
    for off in range(0,len(text),4):
        w=u32(text,off)
        if w >> 26 == 3:
            site=base+off
            dest=((site+4)&0xF0000000)|((w&0x03FFFFFF)<<2)
            if dest==target: out.append(site)
    return out

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("exe",type=Path)
    ap.add_argument("--allow-hash-mismatch",action="store_true")
    a=ap.parse_args(); data=a.exe.read_bytes()
    if len(data)<0x800 or data[:8]!=b"PS-X EXE": ap.error("invalid PS-X EXE header")
    pc,base,size=u32(data,0x10),u32(data,0x18),u32(data,0x1C)
    if not size or size%4 or 0x800+size>len(data): ap.error("invalid text size")
    sha=hashlib.sha256(data).hexdigest()
    if sha!=EXPECTED_SHA256 and not a.allow_hash_mismatch: ap.error(f"unexpected SHA-256: {sha}")
    text=data[0x800:0x800+size]
    rng=find_words(text,base,RNG_WORDS); seed=find_words(text,base,SEED_WORDS)
    print(f"file={a.exe.name} bytes={len(data)} sha256={sha}")
    print(f"entry=0x{pc:08X} text_base=0x{base:08X} text_size=0x{size:X}")
    print("exact_lcg_signature="+(",".join(f"0x{x:08X}" for x in rng) if rng else "NONE"))
    print("exact_seed_setter_signature="+(",".join(f"0x{x:08X}" for x in seed) if seed else "NONE"))
    for addr in rng:
        for caller in calls_to(text,base,addr): print(f"direct_jal_caller rng=0x{addr:08X} caller=0x{caller:08X}")
    for addr in seed:
        hits=calls_to(text,base,addr)
        print(f"direct_jal_callers_seed_setter=0x{addr:08X}: "+(",".join(f"0x{x:08X}" for x in hits) if hits else "NONE"))
    print("result="+("LCG_SIGNATURE_MATCH; only direct JAL callers in main EXE were counted" if rng else "NO_MATCH"))
    return 0 if rng else 1

if __name__=="__main__": raise SystemExit(main())
