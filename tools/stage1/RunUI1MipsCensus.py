#!/usr/bin/env python3
"""Linear raw-byte MIPS-I census for EXE, DATA.BIN Entry0 and Entry1."""
from __future__ import annotations
import argparse, csv, hashlib, struct
from collections import Counter
from pathlib import Path

EXE_SIZE=385024
EXE_SHA="a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
DATA_SIZE=66015232
DATA_SHA="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
E0=(403,110536,0x5F800,"56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4")
E1=(8778,596412,0x10BB000,"9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a")
REGS=("zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra")
OPS={0x20:"lb",0x21:"lh",0x23:"lw",0x24:"lbu",0x25:"lhu",0x28:"sb",0x29:"sh",0x2B:"sw"}
STORES={0x1A,0x1C,0x1E,0x20}; LOADS={0x1A,0x1C,0x1E}
FIELDS=["region","pc","file_offset","bytes","instruction","base_register","base_origin","classification"]

def sha(b): return hashlib.sha256(b).hexdigest()

def row(region,data,pos,pc_base,pc_rel,file_base):
    b=data[pos:pos+4]
    if len(b)!=4: return None
    w=int.from_bytes(b,"little"); op=w>>26; m=OPS.get(op)
    if not m: return None
    store=op in (0x28,0x29,0x2B); imm=w&0xffff
    if imm not in (STORES if store else LOADS): return None
    rs=(w>>21)&31; rt=(w>>16)&31; width={0x20:1,0x24:1,0x21:2,0x25:2,0x23:4,0x28:1,0x29:2,0x2B:4}[op]
    pc="TIDAK TAHU" if pc_base is None else f"0x{pc_base+pos-pc_rel:08X}"
    base="$"+REGS[rs]
    origin=("TIDAK TAHU (Entry0 runtime base belum terbukti)" if pc_base is None
            else "TIDAK TAHU (asal register base belum ditelusuri)")
    return {"region":region,"pc":pc,"file_offset":f"0x{file_base+pos:08X}",
      "bytes":" ".join(f"{x:02X}" for x in b),
      "instruction":m+" $"+REGS[rt]+f", 0x{imm:04X}({base})",
      "base_register":base,"base_origin":origin,
      "classification":f"RAW_ALIGNED_MIPS_CANDIDATE_{'STORE' if store else 'LOAD'}_{m.upper()}_WIDTH_{width}; code/function membership TIDAK TAHU"}

def scan(region,data,pc_base,pc_rel,file_base,start=0,end=None):
    stop=len(data) if end is None else min(end,len(data))
    if start<0 or start%4 or stop<start: raise ValueError("invalid aligned scan bounds")
    return [r for p in range(start,stop-3,4) if (r:=row(region,data,p,pc_base,pc_rel,file_base)) is not None]

def entries(data):
    table=data[0x44:0x2F44]
    if len(table)!=1504*8: raise ValueError("DATA.BIN directory table mismatch")
    directory=[struct.unpack_from("<II",table,i*8) for i in range(1504)]
    out=[]
    for idx,expected in ((0,E0),(1,E1)):
        lbn,size,off,digest=expected
        actual_lbn,actual_size=directory[idx]; actual_off=(actual_lbn-212)*2048
        blob=data[actual_off:actual_off+actual_size]
        if (actual_lbn,actual_size,actual_off,len(blob),sha(blob))!=(lbn,size,off,size,digest):
            raise ValueError(f"Entry{idx} identity mismatch")
        out.append(blob)
    return out

def self_test():
    fake=bytearray()
    specs=[(0x28,3,4,0x1A),(0x29,5,6,0x1C),(0x2B,7,8,0x1E),(0x28,9,10,0x20),
           (0x20,15,16,0x1A),(0x24,17,18,0x1C),(0x21,19,20,0x1E),(0x25,21,22,0x1A),(0x23,23,24,0x1C)]
    for op,rs,rt,imm in specs: fake.extend(((op<<26)|(rs<<21)|(rt<<16)|imm).to_bytes(4,"little"))
    rows=scan("FAKE",bytes(fake),0x80010000,0,0x800)
    assert len(rows)==len(specs) and rows[0]["pc"]=="0x80010000" and rows[0]["file_offset"]=="0x00000800"
    assert row("ENTRY0",bytes(fake),0,None,0,E0[2])["pc"]=="TIDAK TAHU"
    assert row("ENTRY1",bytes(fake),0,0x800AD450,0,E1[2])["file_offset"]=="0x010BB000"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--exe",type=Path); ap.add_argument("--data-bin",type=Path); ap.add_argument("--out-dir",type=Path); ap.add_argument("--self-test",action="store_true"); a=ap.parse_args()
    if a.self_test: self_test(); print("UI1_FAKE_BYTE_SELF_TEST=PASS"); return 0
    if not a.exe or not a.data_bin or not a.out_dir: ap.error("--exe, --data-bin and --out-dir required")
    exe=a.exe.read_bytes(); data=a.data_bin.read_bytes()
    if len(exe)!=EXE_SIZE or sha(exe)!=EXE_SHA: raise SystemExit("UI1_EXE_IDENTITY_MISMATCH")
    if len(data)!=DATA_SIZE or sha(data)!=DATA_SHA: raise SystemExit("UI1_DATA_BIN_IDENTITY_MISMATCH")
    e0,e1=entries(data)
    rows=scan("EXE",exe,0x80010000,0x800,0,0x800,0x5E000)
    rows+=scan("ENTRY0",e0,None,0,E0[2])
    rows+=scan("ENTRY1",e1,0x800AD450,0,E1[2])
    a.out_dir.mkdir(parents=True,exist_ok=True)
    with (a.out_dir/"UI1_MIPS_FIELD_CENSUS.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,delimiter="\t",lineterminator="\n"); w.writeheader(); w.writerows(rows)
    counts=Counter((r["region"],r["instruction"].split()[0]) for r in rows)
    lines=["UI1_RAW_MIPS_FIELD_CENSUS","STATUS=TUNTAS",
      "EVIDENCE=K4 untuk decode byte mentah/offset; K0 untuk membership fungsi dan semantik runtime",
      f"EXE_BYTES={len(exe)} EXE_SHA256={sha(exe)}",f"DATA_BIN_BYTES={len(data)} DATA_BIN_SHA256={sha(data)}",
      f"ENTRY0_BYTES={len(e0)} ENTRY0_OFFSET=0x{E0[2]:X} ENTRY0_SHA256={sha(e0)}",
      "ENTRY0_PC=TIDAK TAHU; hanya file_offset DATA.BIN dilaporkan",
      f"ENTRY1_BYTES={len(e1)} ENTRY1_DATA_BIN_OFFSET=0x{E1[2]:X} ENTRY1_SHA256={sha(e1)}",
      "EXE_PC_FORMULA=0x80010000+(file_offset-0x800)",
      "ENTRY1_PC_FORMULA=0x800AD450+entry_relative_offset; DATA.BIN file offset=0x10BB000+entry_relative_offset",
      "ENTRY1 mapping adalah kandidat statis, bukan validasi runtime",
      "FILTER=SB/SH/SW imm 1A/1C/1E/20; LB/LBU/LH/LHU/LW imm 1A/1C/1E",
      "BASE_ORIGIN=TIDAK TAHU; asal register belum ditelusuri; opcode linier dapat mengenai data/area tak terjangkau",
      f"TOTAL_ROWS={len(rows)}",f"EXE_ROWS={sum(r['region']=='EXE' for r in rows)}",
      f"ENTRY0_ROWS={sum(r['region']=='ENTRY0' for r in rows)}",f"ENTRY1_ROWS={sum(r['region']=='ENTRY1' for r in rows)}",
      "ACTIVE_RECORD_COUNT=TIDAK TAHU","NO_BINARY_OUTPUT=YES"]
    for (region,mn),n in sorted(counts.items()): lines.append(f"COUNT_{region}_{mn}={n}")
    (a.out_dir/"UI1_SUMMARY.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("\n".join(lines)); return 0

if __name__=="__main__": raise SystemExit(main())
