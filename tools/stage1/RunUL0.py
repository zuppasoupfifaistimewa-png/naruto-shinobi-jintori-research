#!/usr/bin/env python3
"""UL0: complete aligned MIPS census for stride 0x124 and bounded field accesses."""
from __future__ import annotations
import argparse,csv,hashlib,struct
from collections import defaultdict
from pathlib import Path

EXE_SIZE=385024
EXE_SHA="a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
DATA_SIZE=66015232
DATA_SHA="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
E1_SIZE=596412
E1_SHA="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
E1_OFF=0x10BB000
E1_PC=0x800AD450
EXE_PC=0x80010000
EXE_TEXT_OFF=0x800
REGS=("zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra")
MEMOPS={0x20:("lb",1,"R"),0x21:("lh",2,"R"),0x22:("lwl",4,"R"),0x23:("lw",4,"R"),
  0x24:("lbu",1,"R"),0x25:("lhu",2,"R"),0x26:("lwr",4,"R"),
  0x28:("sb",1,"W"),0x29:("sh",2,"W"),0x2A:("swl",4,"W"),0x2B:("sw",4,"W"),0x2E:("swr",4,"W")}
MATCH_FIELDS=["region","kind","pc","file_offset","index_register","result_register","function",
 "pointer_base_register","pointer_origin","pointer_origin_evidence","match_detail"]
WINDOW_FIELDS=["region","match_pc","instruction_index","pc","file_offset","bytes_4B","instruction",
 "registers_tracked","memory_access","access_offset","width_bytes","read_write","stop_reason"]
NON_FIELDS=["region","pc","file_offset","index_register","result_register","candidate_type","status","reason"]
ACCESS_FIELDS=["offset","read_count","write_count","access_count","read_sites","write_sites"]

def sha(b:bytes)->str: return hashlib.sha256(b).hexdigest()

def decode(b:bytes)->dict:
    w=int.from_bytes(b,"little"); op=w>>26; rs=(w>>21)&31; rt=(w>>16)&31
    rd=(w>>11)&31; sh=(w>>6)&31; fn=w&63; imm=w&0xffff
    simm=imm if imm<0x8000 else imm-0x10000
    d={"word":w,"op":op,"rs":rs,"rt":rt,"rd":rd,"sh":sh,"fn":fn,"imm":imm,
       "simm":simm,"writes":None,"text":f".word 0x{w:08X}"}
    if op==0:
        if fn==0: d.update(writes=rd,text=f"sll ${REGS[rd]},${REGS[rt]},{sh}")
        elif fn==0x21: d.update(writes=rd,text=f"addu ${REGS[rd]},${REGS[rs]},${REGS[rt]}")
        elif fn==0x18: d["text"]=f"mult ${REGS[rs]},${REGS[rt]}"
        elif fn==0x19: d["text"]=f"multu ${REGS[rs]},${REGS[rt]}"
        elif fn==0x12: d.update(mflo=rd,text=f"mflo ${REGS[rd]}")
        elif fn==0x08: d["text"]=f"jr ${REGS[rs]}"
        elif fn==0x09: d.update(writes=rd,text=f"jalr ${REGS[rd]},${REGS[rs]}")
        else:
            names={0x23:"subu",0x24:"and",0x25:"or",0x26:"xor",0x27:"nor",0x2a:"slt",0x2b:"sltu"}
            if fn in names: d.update(writes=rd,text=f"{names[fn]} ${REGS[rd]},${REGS[rs]},${REGS[rt]}")
    elif op in (8,9,10,11,12,13,14):
        name={8:"addi",9:"addiu",10:"slti",11:"sltiu",12:"andi",13:"ori",14:"xori"}[op]
        val=imm if op in (12,13,14) else simm
        d.update(writes=rt,text=f"{name} ${REGS[rt]},${REGS[rs]},0x{val&0xffffffff:X}")
    elif op==15: d.update(writes=rt,text=f"lui ${REGS[rt]},0x{imm:04X}")
    elif op in MEMOPS:
        name,width,rw=MEMOPS[op]
        d.update(writes=rt if rw=="R" else None,mem=(width,rw,imm,rs,rt),
                 text=f"{name} ${REGS[rt]},0x{imm:04X}(${REGS[rs]})")
    elif op in (4,5):
        d["text"]=f"{'beq' if op==4 else 'bne'} ${REGS[rs]},${REGS[rt]},0x{simm&0xffffffff:X}"
    return d

def canonical(ins,i):
    if i+4>=len(ins): return None,"TRUNCATED_WINDOW"
    a,b,c,d,e=ins[i:i+5]; x=a["rd"]; y=a["rt"]
    checks=(a["op"]==0 and a["fn"]==0 and a["sh"]==3,
      b["op"]==0 and b["fn"]==0x21 and b["rd"]==x and b["rs"]==x and b["rt"]==y,
      c["op"]==0 and c["fn"]==0 and c["sh"]==3 and c["rd"]==x and c["rt"]==x,
      d["op"]==0 and d["fn"]==0x21 and d["rd"]==x and d["rs"]==x and d["rt"]==y,
      e["op"]==0 and e["fn"]==0 and e["sh"]==2 and e["rd"]==x and e["rt"]==x)
    if all(checks):
        return {"index":y,"result":x,"start":i,"end":i+4,"kind":"CANONICAL_SLL_ADDU_0x124",
                "detail":"sll3/addu/sll3/addu/sll2"}, "MATCH"
    return None,"STEP_MISMATCH"

def alternative(ins):
    hits=[]; rejected=[]
    for i,d in enumerate(ins):
        if d["op"] not in (9,13) or d["rs"]!=0 or d["imm"]!=0x124: continue
        cr=d["rt"]; reason="NO_MULT_OR_MULTU_USING_CONSTANT_REGISTER"; found=False
        for j in range(i+1,min(len(ins),i+25)):
            m=ins[j]
            if m.get("writes")==cr: reason="CONSTANT_REGISTER_OVERWRITTEN_BEFORE_MULT"; break
            if m["op"]==0 and m["fn"] in (0x18,0x19) and cr in (m["rs"],m["rt"]):
                reason="MULT_FOUND_BUT_NO_MFLO_WITHIN_24_INSTRUCTIONS"
                index=m["rt"] if m["rs"]==cr else m["rs"]
                for k in range(j+1,min(len(ins),j+25)):
                    if ins[k]["op"]==0 and ins[k]["fn"] in (0x18,0x19):
                        reason="LO_OVERWRITTEN_BEFORE_MFLO"; break
                    if ins[k].get("mflo") is not None:
                        hits.append({"index":index,"result":ins[k]["mflo"],"start":i,"end":k,
                          "kind":"CONST_0x124_MULT_MFLO","detail":f"constant_index={i};mult_index={j};mflo_index={k}"})
                        found=True; break
                break
        if not found: rejected.append((i,reason))
    return hits,rejected

def pointer_origin(ins,match_i,base_reg):
    lo=max(0,match_i-64); lui_regs=set(); found=[]
    for j in range(lo,match_i):
        d=ins[j]
        if d["op"]==15 and d["imm"]==0x8014:
            lui_regs.add(d["rt"]); continue
        if d.get("mem"):
            width,rw,imm,rs,rt=d["mem"]; simm=imm if imm<0x8000 else imm-0x10000
            # Read the source alias before removing an LW destination overwritten in-place.
            if rw=="R" and width==4 and simm==-0x157c and rs in lui_regs and rt==base_reg: found.append(j)
        if d["writes"] is not None and d["writes"] in lui_regs: lui_regs.remove(d["writes"])
    if found: return "YA",f"LUI 0x8014 + LW -0x157C -> ${REGS[base_reg]}; slot=0x8013EA84",found[-1]
    if base_reg==0: return "TIDAK","base register $zero; no read of pointer slot",None
    for j in range(lo,match_i):
        d=ins[j]
        if d["op"]==15 and d["imm"]==0x8014:
            for k in range(j+1,min(match_i,j+12)):
                m=ins[k]
                if m.get("mem"):
                    width,rw,imm,rs,rt=m["mem"]; simm=imm if imm<0x8000 else imm-0x10000
                    if rw=="R" and width==4 and simm==-0x157c and rs==d["rt"] and rt!=base_reg:
                        return "TAK TERSELESAIKAN",f"pair menunjuk ${REGS[rt]}, bukan base ${REGS[base_reg]}",k
    return "TAK TERSELESAIKAN","def-chain slot tidak ditemukan dalam 64 instruksi sebelumnya",None

def scan_region(region,blob,pc_base,pc_rel,file_base):
    ins=[decode(blob[p:p+4]) for p in range(0,len(blob)-3,4)]
    pcs=[None if region=="EXE" and p<pc_rel else pc_base+(p-pc_rel) for p in range(0,len(blob)-3,4)]
    hits=[]; non=[]
    for i,d in enumerate(ins):
        if d["op"]==0 and d["fn"]==0 and d["sh"]==3:
            h,reason=canonical(ins,i)
            if h: h.update(region=region,pc=pcs[i],file=file_base+i*4); hits.append(h)
            else:
                non.append({"region":region,"pc":f"0x{pcs[i]:08X}" if pcs[i] is not None else "TIDAK TAHU",
                  "file_offset":f"0x{file_base+i*4:08X}","index_register":f"${REGS[d['rt']]}",
                  "result_register":f"${REGS[d['rd']]}","candidate_type":"SLL_SHIFT3_START",
                  "status":"NONMATCH","reason":reason})
    alts,alt_non=alternative(ins)
    for h in alts: h.update(region=region,pc=pcs[h["start"]],file=file_base+h["start"]*4)
    hits.extend(alts)
    for i,reason in alt_non:
        non.append({"region":region,"pc":f"0x{pcs[i]:08X}" if pcs[i] is not None else "TIDAK TAHU",
          "file_offset":f"0x{file_base+i*4:08X}","index_register":"TIDAK TAHU","result_register":"TIDAK TAHU",
          "candidate_type":"CONST_0x124_MULT_MFLO","status":"NONMATCH","reason":reason})
    for h in hits:
        tracked={h["result"]}; base=None
        if h["end"]+1<len(ins):
            nxt=ins[h["end"]+1]
            if nxt["op"]==0 and nxt["fn"]==0x21 and h["result"] in (nxt["rs"],nxt["rt"]):
                base=nxt["rt"] if nxt["rs"]==h["result"] else nxt["rs"]
                tracked.add(nxt["rd"])
        if base is None:
            origin,evidence="TAK TERSELESAIKAN","ADDU pembentuk basis pointer tidak ditemukan tepat setelah stride"
            base_name="TAK TERSELESAIKAN"
        else:
            origin,evidence,_=pointer_origin(ins,h["start"],base); base_name=f"${REGS[base]}"
        pc=h["pc"]
        h.update(function="FUN_800D15A8" if region=="ENTRY1" and pc is not None and 0x800D5A00<=pc<=0x800D5B5C else "TIDAK TAHU",
          pointer_origin=origin,pointer_evidence=evidence,pointer_base=base_name,window=[],accesses=[])
        first=h["end"]+1; stop="WINDOW_LIMIT_24"
        for j in range(first,min(len(ins),first+24)):
            d=ins[j]; memory="NO"; off=""; width=""; rw=""; mem=d.get("mem")
            if mem:
                wb,rw0,imm,rs,rt=mem
                if rs in tracked:
                    if 0<=imm<=0x123:
                        memory="YES"; off=imm; width=wb; rw=rw0
                        h["accesses"].append({"offset":imm,"width":wb,"rw":rw0,"pc":pcs[j],"region":region})
                    else: memory="OUT_OF_RANGE"
            # ADDU using a tracked result is treated as pointer derivation; all result aliases persist.
            if d["op"]==0 and d["fn"]==0x21 and d["writes"] is not None and d["writes"] not in tracked and (d["rs"] in tracked or d["rt"] in tracked):
                tracked.add(d["writes"])
            elif d["op"]==0 and d["fn"]==0x21 and d["rd"] in tracked and (d["rs"] in tracked or d["rt"] in tracked):
                pass
            elif d["writes"] is not None and d["writes"] in tracked:
                stop=f"RESULT_REGISTER_OVERWRITTEN_${REGS[d['writes']]}"
            b=blob[j*4:j*4+4]; pcj=pcs[j]
            h["window"].append({"region":region,"match_pc":f"0x{pc:08X}" if pc is not None else "TIDAK TAHU",
              "instruction_index":j-first+1,"pc":f"0x{pcj:08X}" if pcj is not None else "TIDAK TAHU",
              "file_offset":f"0x{file_base+j*4:08X}","bytes_4B":" ".join(f"{v:02X}" for v in b),
              "instruction":d["text"],"registers_tracked":";".join(f"${REGS[x]}" for x in sorted(tracked)),
              "memory_access":memory,"access_offset":f"0x{off:03X}" if off!="" else "",
              "width_bytes":width,"read_write":rw,"stop_reason":stop if stop!="WINDOW_LIMIT_24" else ""})
            if stop.startswith("RESULT_REGISTER_OVERWRITTEN"): break
    return hits,non

def get_entry1(data):
    directory=data[0x44:0x2f44]
    if len(directory)!=1504*8: raise ValueError("DATA.BIN_DIRECTORY_SIZE_MISMATCH")
    rows=[struct.unpack_from("<II",directory,i*8) for i in range(1504)]
    lbn,size=rows[1]; off=(lbn-212)*2048; blob=data[off:off+size]
    if off!=E1_OFF or size!=E1_SIZE or sha(blob)!=E1_SHA: raise ValueError("ENTRY1_IDENTITY_MISMATCH")
    return blob

def write_tsv(path,fields,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        w.writeheader(); w.writerows(rows)

def self_test():
    def r(rs,rt,rd=0,sh=0,fn=0): return ((rs<<21)|(rt<<16)|(rd<<11)|(sh<<6)|fn).to_bytes(4,"little")
    def it(op,rs,rt,imm): return ((op<<26)|(rs<<21)|(rt<<16)|(imm&0xffff)).to_bytes(4,"little")
    blob=bytearray(E1_SIZE)
    writer=[r(0,3,2,3),r(2,3,2,0,0x21),r(0,2,2,3),r(2,3,2,0,0x21),r(0,2,2,2),
      r(2,5,2,0,0x21),it(13,0,3,0xf020),it(0x29,2,3,0x20)]
    reader=[it(0x23,2,5,0x1a)]
    for pc,seq in ((0x800D5A00,writer),(0x800D5B3C,reader)):
        start=pc-E1_PC
        for n,b in enumerate(seq): blob[start+n*4:start+n*4+4]=b
    pre=[it(15,0,4,0x8014),it(0x23,4,5,0xea84)]
    for n,b in enumerate(pre):
        start=0x800D5900-E1_PC+n*4; blob[start:start+4]=b
    alt=[it(13,0,8,0x124),r(8,9,0,0,0x18),r(0,0,10,0,0x12),it(0x23,10,11,0x24)]
    for n,b in enumerate(alt):
        start=0x800D5C00-E1_PC+n*4; blob[start:start+4]=b
    hits,_=scan_region("ENTRY1",bytes(blob),E1_PC,0,E1_OFF); pcs={x["pc"] for x in hits}
    assert 0x800D5A00 in pcs,pcs
    target=decode(bytes(blob[(0x800D5B3C-E1_PC):(0x800D5B3C-E1_PC)+4]))
    assert target.get("mem") is not None and target["mem"][1]=="R",target
    assert next(x for x in hits if x["pc"]==0x800D5A00)["pointer_origin"]=="YA"
    assert target["mem"][1]=="R" and target["mem"][2]==0x1a,target
    alt_hit=next(x for x in hits if x["pc"]==0x800D5C00)
    assert alt_hit["kind"]=="CONST_0x124_MULT_MFLO" and any(x["offset"]==0x24 for x in alt_hit["accesses"])
    header=bytearray(16); header[:4]=it(9,0,7,0x124)
    _,header_non=scan_region("EXE",bytes(header),EXE_PC,EXE_TEXT_OFF,0)
    assert any(x["pc"]=="TIDAK TAHU" and x["file_offset"]=="0x00000000" for x in header_non)
    print("UL0_SELF_TEST=PASS anchors, slot provenance, MULT/MFLO, 24-instruction memory windows, header PC guard")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--exe",type=Path); ap.add_argument("--data-bin",type=Path); ap.add_argument("--out-dir",type=Path)
    ap.add_argument("--self-test",action="store_true"); a=ap.parse_args()
    if a.self_test: self_test(); return 0
    if not a.exe or not a.data_bin or not a.out_dir: ap.error("--exe --data-bin --out-dir required")
    exe=a.exe.read_bytes(); data=a.data_bin.read_bytes()
    if len(exe)!=EXE_SIZE or sha(exe)!=EXE_SHA: raise SystemExit("UL0_EXE_IDENTITY_MISMATCH")
    if len(data)!=DATA_SIZE or sha(data)!=DATA_SHA: raise SystemExit("UL0_DATA_BIN_IDENTITY_MISMATCH")
    if exe[:8]!=b"PS-X EXE": raise SystemExit("UL0_PSX_EXE_MAGIC_MISMATCH")
    e1=get_entry1(data)
    # Full EXE includes header bytes; PC is intentionally unknown for file offsets below 0x800.
    hm,hn=scan_region("EXE",exe,EXE_PC,EXE_TEXT_OFF,0)
    em,en=scan_region("ENTRY1",e1,E1_PC,0,E1_OFF)
    hits=hm+em; non=hn+en; a.out_dir.mkdir(parents=True,exist_ok=True)
    match_rows=[]; window_rows=[]; all_access=[]
    for h in hits:
        match_rows.append({"region":h["region"],"kind":h["kind"],"pc":f"0x{h['pc']:08X}" if h["pc"] is not None else "TIDAK TAHU",
          "file_offset":f"0x{h['file']:08X}","index_register":f"${REGS[h['index']]}","result_register":f"${REGS[h['result']]}",
          "function":h["function"],"pointer_base_register":h["pointer_base"],"pointer_origin":h["pointer_origin"],
          "pointer_origin_evidence":h["pointer_evidence"],"match_detail":h["detail"]})
        window_rows.extend(h["window"]); all_access.extend(h["accesses"])
    by_offset=defaultdict(list)
    for x in all_access: by_offset[x["offset"]].append(x)
    access_rows=[]
    for off in range(0x124):
        reads=[x for x in by_offset[off] if x["rw"]=="R"]; writes=[x for x in by_offset[off] if x["rw"]=="W"]
        def site(x):
            pc=f"0x{x['pc']:08X}" if x["pc"] is not None else "TIDAK TAHU"
            return f"{x['region']}@{pc}/u{x['width']*8}"
        access_rows.append({"offset":f"0x{off:03X}","read_count":len(reads),"write_count":len(writes),
          "access_count":len(reads)+len(writes),"read_sites":";".join(site(x) for x in reads),
          "write_sites":";".join(site(x) for x in writes)})
    write_tsv(a.out_dir/"UL0_MATCHES.tsv",MATCH_FIELDS,match_rows)
    write_tsv(a.out_dir/"UL0_WINDOWS.tsv",WINDOW_FIELDS,window_rows)
    write_tsv(a.out_dir/"UL0_NONMATCHES.tsv",NON_FIELDS,non)
    write_tsv(a.out_dir/"UL0_OFFSET_ACCESS.tsv",ACCESS_FIELDS,access_rows)
    writer=next((h for h in hits if h["region"]=="ENTRY1" and h["pc"]==0x800D5A00 and h["kind"]=="CANONICAL_SLL_ADDU_0x124"),None)
    target_pc=0x800D5B3C
    target_file=E1_OFF+(target_pc-E1_PC)
    target_pos=target_pc-E1_PC
    target_bytes=e1[target_pos:target_pos+4]
    target_dec=decode(target_bytes)
    target_mem=target_dec.get("mem")
    reader=target_mem is not None and target_mem[1]=="R"
    target_row={"region":"ENTRY1","pc":f"0x{target_pc:08X}","file_offset":f"0x{target_file:08X}",
      "bytes_4B":" ".join(f"{v:02X}" for v in target_bytes),"instruction":target_dec["text"],
      "memory_operation":"LOAD" if reader else ("STORE" if target_mem else "NOT_MEMORY_ACCESS"),
      "read_write":target_mem[1] if target_mem else "TIDAK TAHU",
      "width_bytes":target_mem[0] if target_mem else "TIDAK TAHU",
      "immediate":f"0x{target_mem[2]:04X}" if target_mem else "TIDAK TAHU",
      "base_register":f"${REGS[target_mem[3]]}" if target_mem else "TIDAK TAHU",
      "data_register":f"${REGS[target_mem[4]]}" if target_mem else "TIDAK TAHU"}
    write_tsv(a.out_dir/"UL0_TARGET_READER.tsv",["region","pc","file_offset","bytes_4B","instruction","memory_operation","read_write","width_bytes","immediate","base_register","data_register"],[target_row])
    quote_lines=[]
    if writer:
        quote_lines.append("[EXPECTED_WRITER_0x800D5A00]")
        off=writer["pc"]-E1_PC
        for k in range(5):
            b=e1[off+k*4:off+k*4+4]
            quote_lines.append(f"0x{writer['pc']+k*4:08X}\t{' '.join(f'{v:02X}' for v in b)}\t{decode(b)['text']}")
    else: quote_lines.append("[EXPECTED_WRITER_0x800D5A00]=CONTRADICTION_NOT_FOUND")
    quote_lines.append("[EXPECTED_READER_INSTRUCTION_0x800D5B3C]")
    quote_lines.append(f"0x{target_pc:08X}\t{' '.join(f'{v:02X}' for v in target_bytes)}\t{target_dec['text']}")
    (a.out_dir/"UL0_ANCHOR_QUOTES.txt").write_text("\n".join(quote_lines)+"\n",encoding="utf-8")
    status="TUNTAS" if writer and reader else "SEBAGIAN"
    summary=["UL0 STATIC STRIDE AND FIELD-ACCESS AUDIT",f"STATUS={status}",
      "EVIDENCE=K4 for raw byte matches/decode and complete aligned scan; K0 for semantic meaning",
      f"EXE_BYTES={len(exe)} EXE_SHA256={sha(exe)}",f"DATA_BIN_BYTES={len(data)} DATA_BIN_SHA256={sha(data)}",
      f"ENTRY1_BYTES={len(e1)} ENTRY1_FILE_OFFSET=0x{E1_OFF:X} ENTRY1_SHA256={sha(e1)}",
      "EXE_PC_FILE_OFFSET=0x800+(PC-0x80010000)","ENTRY1_PC_FILE_OFFSET=0x10BB000+(PC-0x800AD450)",
      f"ALL_CANONICAL_AND_ALTERNATIVE_MATCHES={len(hits)}",f"NONMATCH_CANDIDATES={len(non)}",
      f"EXPECTED_WRITER_0x800D5A00={'PASS' if writer else 'CONTRADICTION'}",
      f"EXPECTED_READER_INSTRUCTION_0x800D5B3C={'PASS' if reader else 'CONTRADICTION'}",
      f"TARGET_READER_INSTRUCTION={target_dec['text']}",
      f"WINDOW_INSTRUCTION_ROWS={len(window_rows)}",f"WINDOW_MEMORY_ACCESS_ROWS={len(all_access)}",
      "WINDOW=up to 24 instructions after stride-result instruction; every row is one 4-byte instruction; stops on tracked result overwrite",
      "OFFSET_ACCESS_TABLE=292 rows for offsets 0x000..0x123; read/write widths and PC sites included",
      "POINTER_ORIGIN=YA/TIDAK/TAK TERSELESAIKAN only; exact semantic meaning of every field=TIDAK TAHU",
      "ENTRY1_MAPPING=static offset formula; runtime alias not inferred"]
    if not writer: summary.append("CONTRADICTION=expected actual-data stride idiom at 0x800D5A00 was not found")
    if not reader: summary.append("CONTRADICTION=instruction at 0x800D5B3C is not a decoded memory read")
    (a.out_dir/"UL0_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary)); return 0 if writer and reader else 2

if __name__=="__main__": raise SystemExit(main())
