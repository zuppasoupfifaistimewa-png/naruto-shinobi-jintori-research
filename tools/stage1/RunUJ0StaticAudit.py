#!/usr/bin/env python3
"""UJ0 static audit: PS-X EXE header, UH1 raw-byte reconciliation and contiguous Entry1 disassembly."""
from __future__ import annotations
import argparse, csv, hashlib, re, struct
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from tools.stage1.RunUI1MipsCensus import entries
EXE_SIZE=385024
EXE_SHA="a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
DATA_SIZE=66015232
DATA_SHA="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
AUDIT="reports/stage1_economy/uh-audit-2026-11-11/UH1_TILE_WRITER_AUDIT.tsv"
ENTRY1_PC=0x800AD450
ENTRY1_OFF=0x10BB000
REGS=("zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra")
OPS={0x20:"lb",0x21:"lh",0x23:"lw",0x24:"lbu",0x25:"lhu",0x28:"sb",0x29:"sh",0x2B:"sw"}
def sha(b): return hashlib.sha256(b).hexdigest()
def decode(b):
    if len(b)!=4: return "TIDAK_TAHU"
    w=int.from_bytes(b,"little"); op=w>>26; rs=(w>>21)&31; rt=(w>>16)&31
    rd=(w>>11)&31; sh=(w>>6)&31; fn=w&63; imm=w&0xffff
    simm=imm if imm<0x8000 else imm-0x10000
    if op in OPS:
        m=OPS[op]; return f"{m} $\{REGS[rt]}, 0x{imm:04X}($\{REGS[rs]})"
    if op==0:
        names={0x00:"sll",0x02:"srl",0x03:"sra",0x08:"jr",0x09:"jalr",0x21:"addu",0x23:"subu",0x24:"and",0x25:"or",0x26:"xor",0x27:"nor",0x2A:"slt",0x2B:"sltu"}
        m=names.get(fn)
        if not m: return f".word 0x{w:08X}"
        if fn in (0,2,3): return f"{m} $\{REGS[rd]}, $\{REGS[rt]}, 0x{sh:X}"
        if fn==8: return f"{m} $\{REGS[rs]}"
        if fn==9: return f"{m} $\{REGS[rd]}, $\{REGS[rs]}"
        return f"{m} $\{REGS[rd]}, $\{REGS[rs]}, $\{REGS[rt]}"
    if op in (8,9,10,11,12,13,14):
        m={8:"addi",9:"addiu",10:"slti",11:"sltiu",12:"andi",13:"ori",14:"xori"}[op]
        v=imm if op in (12,13,14) else simm
        return f"{m} $\{REGS[rt]}, $\{REGS[rs]}, 0x{v & 0xFFFFFFFF:X}"
    if op==0x0F: return f"lui $\{REGS[rt]}, 0x{imm:04X}"
    if op in (2,3): return f"{'jal' if op==3 else 'j'} 0x{((w&0x03FFFFFF)<<2):08X}"
    if op in (4,5): return f"{'beq' if op==4 else 'bne'} $\{REGS[rs]}, $\{REGS[rt]}, 0x{simm & 0xFFFFFFFF:X}"
    return f".word 0x{w:08X}"
def norm(s):
    s=s.lower().replace(" ","")
    return re.sub(r"0x0+([0-9a-f]+)",r"0x\1",s)
def pc_offset(region,pc,t_addr):
    if region=="EXE": return 0x800+(pc-t_addr)
    if region=="ENTRY1": return ENTRY1_OFF+(pc-ENTRY1_PC)
    raise ValueError("unknown region "+region)
def in_segment(region,off,exe,e1):
    if region=="EXE": return 0x800<=off<0x800+len(exe)
    return ENTRY1_OFF<=off<ENTRY1_OFF+len(e1)
def raw_at(region,off,exe,e1):
    if not in_segment(region,off,exe,e1): return b""
    return exe[off:off+4] if region=="EXE" else e1[off-ENTRY1_OFF:off-ENTRY1_OFF+4]
def read_audit(path):
    with path.open(encoding="utf-8",newline="") as f: return list(csv.DictReader(f,delimiter="\t"))
def reconcile(rows,exe,e1,t_addr):
    fields=list(rows[0].keys())+["matched_pc","matched_file_offset","bytes_4B","decode","status"]
    out=[]; counts={"MATCH":0,"SHIFTED(-0x800)":0,"SHIFTED(+0x800)":0,"NONE":0}
    for row in rows:
        region=row["region"]; pc=int(row["pc"],16); direct_off=pc_offset(region,pc,t_addr); hit=None
        for candidate_pc,status in ((pc,"MATCH"),(pc-0x800,"SHIFTED(-0x800)"),(pc+0x800,"SHIFTED(+0x800)")):
            off=pc_offset(region,candidate_pc,t_addr); b=raw_at(region,off,exe,e1)
            if len(b)==4 and norm(decode(b))==norm(row["instruction"]):
                hit=(candidate_pc,off,b,decode(b),status); break
        if hit is None:
            b=raw_at(region,direct_off,exe,e1)
            hit=(None,direct_off,b,decode(b) if len(b)==4 else "TIDAK_TAHU","NONE")
        mpc,off,b,dec,status=hit
        item=dict(row); item.update(matched_pc=(f"0x{mpc:08X}" if mpc is not None else ""),
          matched_file_offset=f"0x{off:08X}" if len(b)==4 else "",bytes_4B=" ".join(f"{x:02X}" for x in b) if len(b)==4 else "TIDAK_TAHU",
          decode=dec,status=status)
        out.append(item); counts[status]+=1
    return fields,out,counts
def quote(label,blob,start_pc,end_pc,pc_base):
    rel0=start_pc-pc_base; rel1=end_pc-pc_base+4
    if rel0<0 or rel1>len(blob) or rel1-rel0>64: raise ValueError("quote range invalid")
    lines=[f"[{label}] PC=0x{start_pc:08X}..0x{end_pc:08X} BYTES={rel1-rel0}"]
    for pc in range(start_pc,end_pc+1,4):
        off=pc-pc_base; b=blob[off:off+4]
        lines.append(f"0x{pc:08X}\t{' '.join(f'{x:02X}' for x in b)}\t{decode(b)}")
    return lines
def header(exe):
    if exe[:8]!=b"PS-X EXE": raise ValueError("PS-X EXE magic mismatch")
    pc0=struct.unpack_from("<I",exe,0x10)[0]
    t_addr=struct.unpack_from("<I",exe,0x18)[0]
    t_size=struct.unpack_from("<I",exe,0x1C)[0]
    if t_addr==0 or t_size==0 or 0x800+t_size>len(exe): raise ValueError("invalid PS-X EXE text segment bounds")
    return pc0,t_addr,t_size
def self_test():
    b=((0x23<<26)|(4<<21)|(2<<16)|0x1A).to_bytes(4,"little")
    assert decode(b)=="lw $v0, 0x001A($a0)"
    assert norm(decode(b))==norm("lw $v0, 0x1a($a0)")
    assert pc_offset("EXE",0x80011E48,0x80010000)==0x2648
    assert pc_offset("EXE",0x80011648,0x80010000)==0x1E48
    assert pc_offset("ENTRY1",0x800D5A1C,0x80010000)==0x10E35CC
    print("UJ0_FAKE_BYTE_SELF_TEST=PASS")
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--exe",type=Path); ap.add_argument("--data-bin",type=Path)
    ap.add_argument("--audit",type=Path,default=Path(AUDIT)); ap.add_argument("--out-dir",type=Path); ap.add_argument("--self-test",action="store_true")
    a=ap.parse_args()
    if a.self_test: self_test(); return 0
    if not all((a.exe,a.data_bin,a.out_dir)): ap.error("--exe, --data-bin and --out-dir required")
    exe=a.exe.read_bytes(); data=a.data_bin.read_bytes()
    if len(exe)!=EXE_SIZE or sha(exe)!=EXE_SHA: raise SystemExit("UJ0_EXE_IDENTITY_MISMATCH")
    if len(data)!=DATA_SIZE or sha(data)!=DATA_SHA: raise SystemExit("UJ0_DATA_BIN_IDENTITY_MISMATCH")
    pc0,t_addr,t_size=header(exe); _,e1=entries(data)
    rows=read_audit(a.audit)
    if len(rows)!=307: raise SystemExit(f"UJ0_AUDIT_ROW_COUNT={len(rows)}")
    fields,out,counts=reconcile(rows,exe,e1,t_addr); a.out_dir.mkdir(parents=True,exist_ok=True)
    with (a.out_dir/"UJ0_UH1_RECONCILE.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n"); w.writeheader(); w.writerows(out)
    quotes=quote("FUN_800D15A8",e1,0x800D5A00,0x800D5A1C,ENTRY1_PC)
    quotes+=quote("FUN_800F7ADC",e1,0x800F7D80,0x800F7DB0,ENTRY1_PC)
    (a.out_dir/"UJ0_FUNCTION_BYTES.txt").write_text("\n".join(quotes)+"\n",encoding="utf-8")
    exe1a=[x for x in out if x["region"]=="EXE" and x["field"].lower()=="+0x1a"]
    summary=["UJ0_STATIC_AUDIT","STATUS=TUNTAS" if counts["NONE"]==0 else "STATUS=SEBAGIAN",
      "EVIDENCE=K4 untuk header/byte/decoder; K0 untuk semantik yang belum dibuktikan",
      f"EXE_BYTES={len(exe)}",f"EXE_SHA256={sha(exe)}",f"PSX_EXE_PC0=0x{pc0:08X}",
      f"PSX_EXE_T_ADDR=0x{t_addr:08X}",f"PSX_EXE_T_SIZE=0x{t_size:08X}",
      f"EXE_PC_TO_FILE_OFFSET=0x800+(PC-0x{t_addr:08X})",
      f"EXE_FILE_OFFSET_TO_PC=0x{t_addr:08X}+(file_offset-0x800)",
      f"EXE_TEXT_FILE_RANGE=0x800..0x{0x800+t_size-1:X}",
      f"DATA_BIN_SHA256={sha(data)}",f"ENTRY1_BYTES={len(e1)}",f"ENTRY1_SHA256={sha(e1)}",
      f"ENTRY1_PC_TO_DATA_BIN_OFFSET=0x{ENTRY1_OFF:X}+(PC-0x{ENTRY1_PC:08X})",
      f"UH1_ROWS={len(out)}",*[f"{k}={v}" for k,v in counts.items()],
      f"EXE_PLUS1A_ROWS={len(exe1a)}",f"EXE_PLUS1A_SHIFTED_MINUS_800={sum(x['status']=='SHIFTED(-0x800)' for x in exe1a)}",
      "DX1_UI1_DIFFERENCE=DX1 PC-relative code offset is PC-t_addr; raw PS-X EXE file offset adds 0x800 header. UI1's PC reconstruction subtracts 0x800 from raw byte position. 42 EXE +0x1A candidates are found at DX1 PC-0x800.",
      "PLUS_0x48_ORIGIN=TIDAK TAHU; UI0 script hardcodes RECORD_OFF=0x48 without a source derivation in the examined evidence.",
      "NO_BINARY_OUTPUT=YES"]
    (a.out_dir/"UJ0_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary)); return 0 if counts["NONE"]==0 else 2
if __name__=="__main__": raise SystemExit(main())
