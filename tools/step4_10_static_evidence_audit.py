#!/usr/bin/env python3
"""Read-only MIPS static evidence scan for SLPS-03553. No emulator or gameplay."""
from __future__ import annotations
import argparse, csv, hashlib, json, os, struct
from pathlib import Path

BASES = [0x800AD450, 0x800AD000, 0x800D0000, 0x800CD450]
ENTRY0_BASE = 0x800AD000
ENTRY0_OFFSET, ENTRY0_SIZE = 0x5F800, 110536
ENTRY1_OFFSET, ENTRY1_SIZE = 0x10BB000, 596412
EXE_BASE = 0x80010000
EXE_HEADER = 0x800
EXE_TEXT_SIZE = 0x5D800
RNG = 0x80035D78
TARGET = 0x8013A554
LOW = 0xA554  # sign-extended as -0x5AAC
KNOWN_EXE_FUNCTIONS = {
  0x8001387C,0x800138EC,0x8001392C,0x80013970,
  0x80015ADC,0x80015B7C,0x8001A328,0x80020BF4,
  0x80035D78,0x80037138,0x800373F8,0x8003755C,
  0x80037B58,0x80037BB0,0x80037C48,0x800158D8,
  0x800159BC,0x80016C68,0x80020D48,0x80018300,0x80018468,
}
# MIPS register names in index order
REGS=("zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra")
LOADS={0x20:"lb",0x21:"lh",0x22:"lwl",0x23:"lw",0x24:"lbu",0x25:"lhu",0x26:"lwr",0x27:"lwu",0x30:"ll"}
STORES={0x28:"sb",0x29:"sh",0x2A:"swl",0x2B:"sw",0x2E:"swr",0x38:"sc"}
IMM_NAMES={0x08:"addi",0x09:"addiu",0x0A:"slti",0x0B:"sltiu",0x0C:"andi",0x0D:"ori",0x0E:"xori",0x0F:"lui"}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def u32(data, i): return struct.unpack_from("<I", data, i)[0]
def s16(x): return x-0x10000 if x & 0x8000 else x
def fields(w): return ((w>>26)&63,(w>>21)&31,(w>>16)&31,(w>>11)&31,(w>>6)&31,w&63,w&0xffff)
def jal_target(w): return (0x80000000 | ((w & 0x03ffffff) << 2)) if ((w>>26)&63)==3 else None
def signed_imm(w): return s16(w&0xffff)
def is_stack_prologue(w): return (w & 0xffff0000)==0x27bd0000 and signed_imm(w)<0
def is_jr_ra(w): return w==0x03e00008
def is_control(w):
    op,rs,rt,rd,sh,fn,imm=fields(w)
    if op in (1,2,3,4,5,6,7): return True
    if op in (0x10,0x11,0x12,0x13) and rs==8: return True
    return op==0 and fn in (8,9)  # jr / jalr

def dest_reg(w):
    op,rs,rt,rd,sh,fn,imm=fields(w)
    if op==0:
        if fn in (8,): return None
        if fn==9: return rd if rd else 31
        if fn in (0x10,0x12): return rd
        if fn in (0x0c,0x0d,0x0f): return None
        # R-type arithmetic/logical/shift writes rd
        if fn not in (0x18,0x19,0x1a,0x1b,0x1c,0x1d,0x1e,0x1f): return rd if rd else None
        return None
    if op==3: return 31
    if op in (1,) and rt in (0x10,0x11,0x12,0x13): return 31
    if op in (0x02,0x04,0x05,0x06,0x07,0x10,0x11,0x12,0x13,0x28,0x29,0x2a,0x2b,0x2e,0x38): return None
    if op in IMM_NAMES or op in LOADS: return rt
    return None

def mnemonic(w):
    op,rs,rt,rd,sh,fn,imm=fields(w)
    if op==0:
        return {8:"jr",9:"jalr",0x10:"mfhi",0x12:"mflo",0x1a:"div",0x1b:"divu"}.get(fn, {0x21:"addu",0x23:"subu",0x24:"and",0x25:"or",0x26:"xor",0x2a:"slt",0x2b:"sltu",0:"sll",2:"srl",3:"sra"}.get(fn,"r-type"))
    if op==3: return "jal"
    if op==2: return "j"
    if op in IMM_NAMES: return IMM_NAMES[op]
    if op in LOADS: return LOADS[op]
    if op in STORES: return STORES[op]
    if op==4: return "beq"
    if op==5: return "bne"
    if op==6: return "blez"
    if op==7: return "bgtz"
    if op==1: return "regimm"
    return f"op{op:02x}"

def simple_decode(w):
    op,rs,rt,rd,sh,fn,imm=fields(w)
    m=mnemonic(w)
    if op in (0,): return f"{m} word=0x{w:08x} rs={REGS[rs]} rt={REGS[rt]} rd={REGS[rd]} sh={sh} fn=0x{fn:02x}"
    if op in (2,3): return f"{m} target=0x{(0x80000000|((w&0x03ffffff)<<2)):08x}"
    if op in LOADS or op in STORES: return f"{m} {REGS[rt]},{signed_imm(w):#x}({REGS[rs]})"
    if op in IMM_NAMES: return f"{m} {REGS[rt]},{REGS[rs]},{signed_imm(w):#x}"
    if op in (4,5,6,7,1): return f"{m} rs={REGS[rs]} rt={REGS[rt]} imm={signed_imm(w):#x}"
    return f"{m} word=0x{w:08x}"

def words(data):
    return [u32(data,i) for i in range(0,len(data)-3,4)]

def write_csv(path, rows, fields=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    if fields is None:
        fields=list(rows[0].keys()) if rows else []
    with path.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        wr.writeheader()
        wr.writerows(rows)

def a1(entry1,out):
    ws=words(entry1); nbytes=len(entry1)
    bases=sorted(set(BASES))
    # Controls are +/-0x1000 around EACH candidate, in 4-byte increments.
    sweepbases=sorted({b+d for b in BASES for d in range(-0x1000,0x1000+1,4)})
    def count_for(base):
        jals=[]
        for i,w in enumerate(ws):
            t=jal_target(w)
            if t is not None: jals.append((i,t,w))
        within=[]; starts=[]; exe_hits=[]; known_hits=[]
        for i,t,w in jals:
            if base <= t < base+nbytes and (t-base)%4==0:
                toff=t-base
                within.append((i,t,toff))
                tw=ws[toff//4]
                pro=is_stack_prologue(tw)
                afterjr=toff>=8 and is_jr_ra(ws[(toff//4)-2])
                if pro or afterjr: starts.append((i,t,"stack-prologue" if pro else "after-jr-ra-delay"))
            if EXE_BASE <= t < EXE_BASE+EXE_TEXT_SIZE:
                exe_hits.append((i,t))
            if t in KNOWN_EXE_FUNCTIONS:
                known_hits.append((i,t))
        b=len(within); c=len(starts)
        return {"base":f"0x{base:08X}","entry1_bytes":nbytes,"jal_count":len(jals),
                "targets_inside_entry1_b":b,"targets_at_function_start_c":c,
                "c_over_b":(c/b if b else 0.0),"targets_in_exe_text_range":len(exe_hits),
                "targets_at_known_exe_function_entry_d":len(known_hits),
                "unique_known_exe_targets":len({t for _,t in known_hits})}
    sweep=[count_for(b) for b in sweepbases]
    cand=[count_for(b) for b in bases]
    best=max(sweep,key=lambda x:x["c_over_b"])
    bestbase=int(best["base"],16)
    other=max((x["c_over_b"] for x in sweep if int(x["base"],16)!=bestbase),default=0.0)
    passA=(best["targets_inside_entry1_b"]>0 and best["c_over_b"]>=0.70 and best["c_over_b"]>=3*other)
    with (out/"a1_base_sweep.csv").open("w",newline="",encoding="utf8") as f:
        wr=csv.DictWriter(f,fieldnames=list(sweep[0].keys()));wr.writeheader();wr.writerows(sweep)
    with (out/"a1_candidate_scores.csv").open("w",newline="",encoding="utf8") as f:
        wr=csv.DictWriter(f,fieldnames=list(cand[0].keys()));wr.writeheader();wr.writerows(cand)
    # add exact criterion into concise log
    return {"entry1_sha256":hashlib.sha256(entry1).hexdigest(),"entry1_bytes":len(entry1),
            "candidate_base_best":best["base"],"peak_ratio_c_b":best["c_over_b"],
            "best_other_sweep_ratio":other,"peak_over_second":best["c_over_b"]/other if other else None,
            "criterion_pass":passA,"sweep_points":len(sweep),"nearest_sweep_peak":best}

def leaders_for(data,base):
    ws=words(data); n=len(ws); leaders={0}
    for i,w in enumerate(ws):
        op,rs,rt,rd,sh,fn,imm=fields(w)
        pc=base+4*i
        target=None
        if op in (4,5,6,7) or op==1:
            target=pc+4+(signed_imm(w)<<2)
        elif op in (2,3):
            target=((pc+4)&0xf0000000)|((w&0x03ffffff)<<2)
        if target is not None and base<=target<base+len(data) and (target-base)%4==0:
            leaders.add((target-base)//4)
        if is_control(w) and i+2<n:
            leaders.add(i+2)
    return ws,leaders

def a2_scan(data,filename,base,scenario):
    ws,leaders=leaders_for(data,base)
    defs={}
    block_start=0
    rows=[]
    delay_clear=False
    for i,w in enumerate(ws):
        if i in leaders:
            defs.clear(); block_start=i
        op,rs,rt,rd,sh,fn,imm=fields(w)
        pc=base+i*4
        if op in LOADS|STORES or (op==9 and rs==rt):
            lui=defs.get(rs)
            if (w&0xffff)==LOW and lui and lui["imm"]==0x8014:
                if op in LOADS: kind="READ"
                elif op in STORES: kind="WRITE"
                else: kind="ADDRESS"
                rows.append({"file":filename,"scenario":scenario,"virtual_pc":f"0x{pc:08X}",
                    "file_offset":f"0x{i*4:08X}","instruction":f"0x{w:08X}",
                    "mnemonic":mnemonic(w),"kind":kind,"base_reg":REGS[rs],
                    "rt_reg":REGS[rt],"immediate_signed":signed_imm(w),
                    "lui_pc":f"0x{base+lui['i']*4:08X}","lui_file_offset":f"0x{lui['i']*4:08X}",
                    "block_start":f"0x{base+block_start*4:08X}",
                    "effective_address":f"0x{((0x80140000+signed_imm(w))&0xffffffff):08X}",
                    "decoded":simple_decode(w)})
        # invalidate registers written by this instruction after checking memory use
        dest=dest_reg(w)
        if dest is not None: defs.pop(dest,None)
        if op==0x0f: defs[rt]={"imm":imm,"i":i}
        if is_control(w): delay_clear=True
        elif delay_clear:
            defs.clear(); delay_clear=False
    return rows

def a2(datafiles,out):
    allrows=[]
    for name,raw,scenarios in datafiles:
        for scenario,base in scenarios:
            allrows.extend(a2_scan(raw,name,base,scenario))
    write_csv(out/"a2_xref_hits.csv",allrows)
    summary=[]
    for name,raw,scenarios in datafiles:
        for scenario,base in scenarios:
            rows=[r for r in allrows if r["file"]==name and r["scenario"]==scenario]
            summary.append({"file":name,"scenario":scenario,"base":f"0x{base:08X}",
                "read":sum(r["kind"]=="READ" for r in rows),
                "write":sum(r["kind"]=="WRITE" for r in rows),
                "address":sum(r["kind"]=="ADDRESS" for r in rows),
                "total":len(rows),
                "scope_note":"linear instruction-word scan; candidate MIPS code bytes; same-block LUI 0x8014 provenance only"})
    write_csv(out/"a2_xref_summary.csv",summary)
    return {"hits":len(allrows),"summary":summary}

def a3():
    # Exact instruction facts from verified main-EXE spimdisasm artifact:
    return [
      {"routine":"setter","instruction_address":"0x800138DC","word":"0x00822021","operation":"addu a0,a0,v0","role":"computed record base"},
      {"routine":"setter","instruction_address":"0x800138E0","word":"0xAC850018","operation":"sw a1,0x18(a0)","role":"write 32-bit field"},
      {"routine":"getter","instruction_address":"0x80013918","word":"0x8C820018","operation":"lw v0,0x18(a0)","role":"read 32-bit field"},
    ]

def caller_audit(datafiles,out,exe_words):
    rows=[]
    for name,raw,scenarios in datafiles:
      for scenario,base in scenarios:
        ws=words(raw)
        for i,w in enumerate(ws):
          if jal_target(w)!=RNG: continue
          pc=base+4*i
          prior=max(0,i-0x100//4)
          fnstart=None
          for j in range(i,prior-1,-1):
            if is_stack_prologue(ws[j]): fnstart=base+4*j;break
            if j<i and is_jr_ra(ws[j]): break
          # raw observations in the next twelve instructions, including decoded operations only
          seq=[]
          for k in range(i+2,min(len(ws),i+14)):
            ww=ws[k]; op,rs,rt,rd,sh,fn,imm=fields(ww)
            seq.append(f"{base+k*4:08X}:{simple_decode(ww)}")
          decs=[mnemonic(ws[k]) for k in range(i+2,min(len(ws),i+14))]
          masks=[f"0x{ws[k]&0xffff:04X}" for k in range(i+2,min(len(ws),i+14)) if ((ws[k]>>26)&63)==0x0c]
          divs=[f"0x{base+k*4:08X}" for k in range(i+2,min(len(ws),i+14)) if ((ws[k]>>26)&63)==0 and (ws[k]&63) in (0x1a,0x1b)]
          mfhi=[f"0x{base+k*4:08X}" for k in range(i+2,min(len(ws),i+14)) if ((ws[k]>>26)&63)==0 and (ws[k]&63)==0x10]
          caller_uppers=[]
          if fnstart is not None:
            for kn,raw2,scen2 in datafiles:
              for s2,b2 in scen2:
                for j,ww in enumerate(words(raw2)):
                  if jal_target(ww)==fnstart: caller_uppers.append(f"{kn}/{s2}:0x{b2+4*j:08X}")
          rows.append({"file":name,"scenario":scenario,"call_pc":f"0x{pc:08X}",
            "call_word":f"0x{w:08X}","callee":"0x80035D78","caller_function_start":f"0x{fnstart:08X}" if fnstart else "TIDAK TERBUKTI",
            "window_andi_immediates":";".join(masks),"div_addresses":";".join(divs),
            "mfhi_addresses":";".join(mfhi),"caller_above_direct_sites":";".join(caller_uppers) if caller_uppers else "TIDAK TERBUKTI",
            "following_instructions":" | ".join(seq)})
    write_csv(out/"a4_rng_callers.csv",rows)
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--exe",required=True); ap.add_argument("--data",required=True); ap.add_argument("--out",required=True)
    args=ap.parse_args(); out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    exe=Path(args.exe).read_bytes(); dat=Path(args.data).read_bytes()
    if len(exe)!=385024 or exe[:8]!=b"PS-X EXE": raise SystemExit(f"EXE identity/size mismatch {len(exe)}")
    if len(dat)!=66015232: raise SystemExit(f"DATA.BIN size mismatch {len(dat)}")
    text_size=struct.unpack_from("<I",exe,0x1c)[0]
    text_base=struct.unpack_from("<I",exe,0x18)[0]
    if text_base!=EXE_BASE or text_size!=EXE_TEXT_SIZE: raise SystemExit(f"PS-X EXE load mismatch base=0x{text_base:08X} size=0x{text_size:X}")
    text=exe[EXE_HEADER:EXE_HEADER+text_size]
    ent0=dat[ENTRY0_OFFSET:ENTRY0_OFFSET+ENTRY0_SIZE]
    ent1=dat[ENTRY1_OFFSET:ENTRY1_OFFSET+ENTRY1_SIZE]
    if hashlib.sha256(ent0).hexdigest()!="56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4": raise SystemExit("Entry0 SHA mismatch")
    if hashlib.sha256(ent1).hexdigest()!="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a": raise SystemExit("Entry1 SHA mismatch")
    datafiles=[
      ("SLPS_035.53 text",text,[("exe_text",EXE_BASE)]),
      ("DATA.BIN entry0",ent0,[("base_0x800AD000",ENTRY0_BASE)]),
      ("DATA.BIN entry1",ent1,[(f"base_0x{b:08X}",b) for b in BASES]),
    ]
    result_a1=a1(ent1,out)
    result_a2=a2(datafiles,out)
    write_csv(out/"a3_getter_setter.csv",a3())
    result_a4=caller_audit(datafiles,out,words(text))
    direct_rng=[f"0x{EXE_BASE+4*i:08X}" for i,w in enumerate(words(text)) if jal_target(w)==RNG]
    exe_jals=[(EXE_BASE+4*i, jal_target(w)) for i,w in enumerate(words(text)) if jal_target(w) is not None]
    log=[
      "STATIC AUDIT ONLY — no emulator/gameplay/input/savestate restore",
      f"SLPS_035.53 bytes={len(exe)} sha256={sha(exe)}",
      f"EXE text base=0x{EXE_BASE:08X} bytes={len(text)}",
      f"DATA.BIN bytes={len(dat)} sha256={sha(Path(args.data))}",
      f"entry0 offset=0x{ENTRY0_OFFSET:X} bytes={len(ent0)} sha256={hashlib.sha256(ent0).hexdigest()} base=HYPOTHESIS 0x{ENTRY0_BASE:08X}",
      f"entry1 offset=0x{ENTRY1_OFFSET:X} bytes={len(ent1)} sha256={hashlib.sha256(ent1).hexdigest()}",
      "A1: "+json.dumps(result_a1,sort_keys=True),
      "A2: same-block proven linear LUI source hits="+str(result_a2["hits"])+" (not equivalent to Ghidra reference-manager XREF count)",
      "A4 main EXE direct JAL addresses to RNG: "+", ".join(direct_rng),
      "A4 detected direct RNG callers rows="+str(len(result_a4)),
      "CAVEAT: entry0/entry1 are statically scanned as aligned MIPS words; resource may contain data/overlay bytes and base mappings are not assumed runtime-valid.",
    ]
    (out/"static-audit.log").write_text("\n".join(log)+"\n",encoding="utf8")
    meta={"exe_bytes":len(exe),"exe_sha256":sha(Path(args.exe)),"data_bytes":len(dat),"data_sha256":sha(Path(args.data)),
          "entry0_sha256":hashlib.sha256(ent0).hexdigest(),"entry1_sha256":hashlib.sha256(ent1).hexdigest(),
          "a1":result_a1,"a2_hits":len(result_a2["summary"]),"a4_rng_call_rows":len(result_a4),"direct_exe_rng_calls":direct_rng}
    (out/"static-audit.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf8")
    print("\n".join(log))
if __name__=="__main__": main()
