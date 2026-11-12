#!/usr/bin/env python3
"""UN0: byte-backed forward readers and complete aligned LH/LHU census."""
from __future__ import annotations
import argparse, csv, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
EXE_PC,EXE_OFF,EXE_SIZE=0x80010000,0x800,385024
E1_PC,E1_OFF,E1_SIZE=0x800AD450,0x10BB000,596412
DATA_SIZE=66015232
EXE_SHA="a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
DATA_SHA="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
E1_SHA="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
BASE=ROOT/"reports/ui-audit-2026-11-12/ul/run-43192191539/attempt-1/UL0"
COUNTS={0x0E:18,0x10:7,0x1A:11,0x1C:4,0x1E:4}
R=("zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra")
MEM={0x20:("lb",1,"R"),0x21:("lh",2,"R"),0x22:("lwl",4,"R"),0x23:("lw",4,"R"),0x24:("lbu",1,"R"),0x25:("lhu",2,"R"),0x26:("lwr",4,"R"),0x28:("sb",1,"W"),0x29:("sh",2,"W"),0x2A:("swl",4,"W"),0x2B:("sw",4,"W"),0x2E:("swr",4,"W")}
SP={0:"sll",2:"srl",3:"sra",4:"sllv",6:"srlv",7:"srav",8:"jr",9:"jalr",12:"syscall",13:"break",16:"mfhi",17:"mthi",18:"mflo",19:"mtlo",24:"mult",25:"multu",26:"div",27:"divu",32:"add",33:"addu",34:"sub",35:"subu",36:"and",37:"or",38:"xor",39:"nor",42:"slt",43:"sltu"}
IMM={8:"addi",9:"addiu",10:"slti",11:"sltiu",12:"andi",13:"ori",14:"xori"}
BR={4:"beq",5:"bne",6:"blez",7:"bgtz"}
FWD=["site_id","field_offset","region","load_pc","load_file_offset","match_pc","pointer_origin","instruction_index","pc","file_offset","bytes_4B","instruction","tracked_registers","classification","detail"]
SITES=["site_id","field_offset","region","pc","file_offset","match_pc","pointer_origin","bytes_4B","instruction","classification_union","decoded_count","stop_reason"]
LH=["region","pc","file_offset","bytes_4B","instruction","base_register","displacement","origin_status","origin_expression","origin_evidence","index_level","candidate_field_offset","LV_reader_candidate"]
SUMMARY=["item","value"]

def digest(b): return hashlib.sha256(b).hexdigest()
def read_tsv(p):
    with p.open(encoding="utf-8",newline="") as f: return list(csv.DictReader(f,delimiter="\t"))
def write_tsv(p,fields,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n"); w.writeheader(); w.writerows(rows)
def reg(i): return "$"+R[i]
def decode(raw,pc):
    if len(raw)!=4: raise ValueError("instruction_not_4_bytes")
    w=int.from_bytes(raw,"little"); op=w>>26; rs=(w>>21)&31; rt=(w>>16)&31; rd=(w>>11)&31; sh=(w>>6)&31; fn=w&63
    imm=w&0xffff; simm=imm if imm<0x8000 else imm-0x10000
    d={"word":w,"op":op,"rs":rs,"rt":rt,"rd":rd,"sh":sh,"fn":fn,"imm":imm,"simm":simm,"mn":".word","text":f".word 0x{w:08X}","writes":None,"reads":(),"mem":None,"control":False}
    if op==0:
        n=SP.get(fn)
        if n is None: return d
        d["mn"]=n
        if n in ("sll","srl","sra"): d.update(writes=rd,reads=(rt,),text=f"{n} {reg(rd)},{reg(rt)},{sh}")
        elif n in ("sllv","srlv","srav"): d.update(writes=rd,reads=(rt,rs),text=f"{n} {reg(rd)},{reg(rt)},{reg(rs)}")
        elif n=="jr": d.update(reads=(rs,),control=True,text=f"jr {reg(rs)}")
        elif n=="jalr": d.update(writes=rd,reads=(rs,),control=True,text=f"jalr {reg(rd)},{reg(rs)}")
        elif n in ("mfhi","mflo"): d.update(writes=rd,text=f"{n} {reg(rd)}")
        elif n in ("mthi","mtlo"): d.update(reads=(rs,),text=f"{n} {reg(rs)}")
        elif n in ("mult","multu","div","divu"): d.update(reads=(rs,rt),text=f"{n} {reg(rs)},{reg(rt)}")
        elif n in ("syscall","break"): d["text"]=n
        else: d.update(writes=rd,reads=(rs,rt),text=f"{n} {reg(rd)},{reg(rs)},{reg(rt)}")
        return d
    if op==1:
        n={0:"bltz",1:"bgez",16:"bltzal",17:"bgezal"}.get(rt,"regimm")
        d.update(mn=n,reads=(rs,),control=True,text=f"{n} {reg(rs)},0x{simm&0xffffffff:X}"); return d
    if op in (2,3):
        n="j" if op==2 else "jal"; target=((pc+4)&0xF0000000)|((w&0x03ffffff)<<2)
        d.update(mn=n,control=True,text=f"{n} 0x{target:08X}"); return d
    if op in BR:
        n=BR[op]; rdset=(rs,rt) if op in (4,5) else (rs,)
        d.update(mn=n,reads=rdset,control=True,text=f"{n} "+",".join(reg(x) for x in rdset)+f",0x{simm&0xffffffff:X}"); return d
    if op in IMM:
        n=IMM[op]; val=imm if op in (12,13,14) else simm
        d.update(mn=n,writes=rt,reads=(rs,),text=f"{n} {reg(rt)},{reg(rs)},0x{val&0xffffffff:X}"); return d
    if op==15: d.update(mn="lui",writes=rt,text=f"lui {reg(rt)},0x{imm:04X}"); return d
    if op in MEM:
        n,width,rw=MEM[op]; d.update(mn=n,writes=rt if rw=="R" else None,reads=(rs,) if rw=="R" else (rs,rt),mem=(width,rw,simm,rs,rt),text=f"{n} {reg(rt)},{simm}({reg(rs)})"); return d
    if op in (0x2f,0x32,0x3a):
        n={0x2f:"cache",0x32:"lwc2",0x3a:"swc2"}[op]; d.update(mn=n,reads=(rs,),mem=(4,"R" if op==0x32 else "W",simm,rs,rt),text=f"{n} 0x{rt:X},{simm}({reg(rs)})"); return d
    if op in (0x10,0x11,0x12,0x13):
        cop=op-0x10; sub=(w>>21)&31
        if sub==0: d.update(mn=f"mfc{cop}",writes=rt,text=f"mfc{cop} {reg(rt)},$c{rd}")
        elif sub==4: d.update(mn=f"mtc{cop}",reads=(rt,),text=f"mtc{cop} $c{rd},{reg(rt)}")
        elif op==0x10 and fn==0x10: d.update(mn="rfe",text="rfe")
        else: d.update(mn=f"cop{cop}",text=f"cop{cop} 0x{w&0x1ffffff:07X}")
        return d
    d.update(mn=f"op_{op:02X}",text=f"op_{op:02X} 0x{w&0x3ffffff:07X}"); return d

def classify(d,tainted):
    used=set(d["reads"])&tainted; n=d["mn"]
    if n=="jal" and tainted&{4,5,6,7}: return "ARGUMEN_JAL","jal; argument register(s) "+",".join(reg(x) for x in sorted(tainted&{4,5,6,7}))
    if not used: return "",""
    if n in ("slt","sltu","slti","sltiu","beq","bne","blez","bgtz","bltz","bgez","bltzal","bgezal"): return "DIBANDINGKAN",n
    if d["mem"]:
        _,rw,disp,base,value=d["mem"]
        if rw=="W" and base in tainted: return "DISIMPAN_BASIS_OFFSET",f"{n}; basis register + displacement {disp}"
        if rw=="W" and value in tainted: return "DISIMPAN_NILAI",n
        if base in tainted: return "INDEKS_ALAMAT",f"{n}; base register + displacement {disp}"
    if n in ("mult","multu","div","divu"): return "DIKALI",n
    if n in ("sll","srl","sra","sllv","srlv","srav"): return "DISHIFT",n
    if n in ("sub","subu"): return "DIKURANGKAN_KE_REGISTER_LAIN",n
    if n in ("add","addu","addi","addiu"): return "DITAMBAHKAN_KE_REGISTER_LAIN",n
    return "DIGUNAKAN",n

def get_sites():
    access=read_tsv(BASE/"UL0_OFFSET_ACCESS.tsv"); matches=read_tsv(BASE/"UL0_MATCHES.tsv"); windows=read_tsv(BASE/"UL0_WINDOWS.tsv")
    mm={(x["region"],x["pc"]):x for x in matches}; wm={}
    for x in windows:
        if x.get("read_write")=="R" and x.get("width_bytes")=="2": wm[(x["region"],x["pc"],x["access_offset"])]=x
    out=[]
    for off,count in COUNTS.items():
        row=next((x for x in access if int(x["offset"],16)==off),None)
        if row is None or int(row["read_count"])!=count or int(row["write_count"])!=0: raise ValueError(f"UL0_access_mismatch_0x{off:X}")
        tokens=[t for t in row["read_sites"].split(";") if t]
        if len(tokens)!=count: raise ValueError("UL0_site_token_count_mismatch")
        for token in tokens:
            m=re.fullmatch(r"(ENTRY1|EXE)@(0x[0-9A-Fa-f]+)/u16",token)
            if not m: raise ValueError("bad_UL0_token_"+token)
            region,pc=m.group(1),int(m.group(2),16); pcstr=f"0x{pc:08X}"
            win=wm.get((region,pcstr,f"0x{off:03X}"))
            if win is None: raise ValueError(f"UL0_window_missing_{pcstr}")
            mr=mm.get((region,win["match_pc"]))
            if mr is None: raise ValueError(f"UL0_match_missing_{win['match_pc']}")
            out.append({"region":region,"pc":pc,"off":off,"match_pc":win["match_pc"],"origin":"YA" if mr["pointer_origin"]=="YA" else "TAK TERSELESAIKAN"})
    return out

def forward(sites,blobs):
    output=[]; summary=[]
    for sid,s in enumerate(sites,1):
        blob,baseoff=s["blob"]; fo=(E1_OFF+s["pc"]-E1_PC) if s["region"]=="ENTRY1" else (EXE_OFF+s["pc"]-EXE_PC); pos=fo-baseoff
        first=decode(blob[pos:pos+4],s["pc"])
        if first["mn"] not in ("lh","lhu") or first["mem"][2]!=s["off"]: raise ValueError(f"raw_load_mismatch_{s['pc']:08X}")
        tainted={first["mem"][4]}; cats=set(); stop="LIMIT_32"; used_count=0
        for j in range(32):
            raw=blob[pos+4*j:pos+4*j+4]
            if len(raw)!=4: stop="END_OF_REGION"; break
            pc=s["pc"]+4*j; d=decode(raw,pc); category,detail=classify(d,tainted)
            if category: cats.add(category)
            output.append({"site_id":sid,"field_offset":f"0x{s['off']:03X}","region":s["region"],"load_pc":f"0x{s['pc']:08X}","load_file_offset":f"0x{fo:08X}","match_pc":s["match_pc"],"pointer_origin":s["origin"],"instruction_index":j,"pc":f"0x{pc:08X}","file_offset":f"0x{fo+4*j:08X}","bytes_4B":" ".join(f"{b:02X}" for b in raw),"instruction":d["text"],"tracked_registers":";".join(reg(x) for x in sorted(tainted)),"classification":category or "TIDAK_MENGGUNAKAN_NILAI","detail":detail})
            used=set(d["reads"])&tainted
            if d["writes"] is not None:
                tainted.discard(d["writes"])
                if used: tainted.add(d["writes"])
            used_count+=1
            if not tainted: stop=f"TAINT_END_AFTER_0x{pc+4:08X}"; break
        summary.append({"site_id":sid,"field_offset":f"0x{s['off']:03X}","region":s["region"],"pc":f"0x{s['pc']:08X}","file_offset":f"0x{fo:08X}","match_pc":s["match_pc"],"pointer_origin":s["origin"],"bytes_4B":" ".join(f"{b:02X}" for b in blob[pos:pos+4]),"instruction":first["text"],"classification_union":";".join(sorted(cats)) if cats else "TAK_TERSELESAIKAN","decoded_count":used_count,"stop_reason":stop})
    return output,summary

def stride_result(ins,i):
    if i<0 or i+4>=len(ins): return None
    a,b,c,d,e=ins[i:i+5]; x,y=a["rd"],a["rt"]
    ok=(a["mn"]=="sll" and a["sh"]==3 and b["mn"]=="addu" and b["rd"]==x and b["rs"]==x and b["rt"]==y and c["mn"]=="sll" and c["rd"]==x and c["rt"]==x and c["sh"]==3 and d["mn"]=="addu" and d["rd"]==x and d["rs"]==x and d["rt"]==y and e["mn"]=="sll" and e["rd"]==x and e["rt"]==x and e["sh"]==2)
    return x if ok else None

def scan_lh_lhu(blob,region,basepc,baseoff):
    ins=[decode(blob[i:i+4],basepc+i) for i in range(0,len(blob)-3,4)]; expr={0:"ZERO"}; rows=[]; lo=False; pending_reset=False
    for i,d in enumerate(ins):
        pc=basepc+4*i; raw=blob[4*i:4*i+4]; disp=d["mem"][2] if d["mem"] else 0
        stride=stride_result(ins,i-4)
        if d["mn"]=="lui" and d["imm"]==0x8014: expr[d["rt"]]="ABS_0x80140000"
        elif d["mem"] and d["mem"][1]=="R":
            width,_,disp,base,dst=d["mem"]
            if width==4 and disp==-0x157C and expr.get(base)=="ABS_0x80140000": expr[dst]="EA84_POINTER"
            elif d["mn"] in ("lh","lhu") and 0x0E<=disp<=0x18:
                origin=expr.get(base,"UNKNOWN"); yes=origin in ("RECORD_BASE_0x124","RECORD_BASE_INDEX2","EA84_POINTER")
                rows.append({"region":region,"pc":f"0x{pc:08X}","file_offset":f"0x{baseoff+4*i:08X}","bytes_4B":" ".join(f"{b:02X}" for b in raw),"instruction":d["text"],"base_register":reg(base),"displacement":disp,"origin_status":"YA" if yes else "TAK TERSELESAIKAN","origin_expression":origin,"origin_evidence":"EA84 pointer plus proven index*0x124/index*2 or direct pointer" if yes else "basis register def-chain tidak terbukti dari EA84","index_level":{"RECORD_BASE_0x124":"INDEX_0x124","RECORD_BASE_INDEX2":"INDEX_TIMES_2","EA84_POINTER":"DIRECT_EA84"}.get(origin,"TIDAK TAHU"),"candidate_field_offset":f"0x{disp:02X}","LV_reader_candidate":("YES_PROVEN" if yes else "CANDIDATE_BASE_UNRESOLVED") if 0x10<=disp<=0x18 else "NO"})
                if d["writes"] is not None: expr.pop(d["writes"],None)
            elif d["writes"] is not None: expr.pop(d["writes"],None)
        elif d["mn"] in ("sll","srl","sra"):
            if d["mn"]=="sll" and d["sh"]==1: expr[d["rd"]]="INDEX_TIMES_2"
            else: expr.pop(d["rd"],None)
        elif d["mn"] in ("addiu","addi") and expr.get(d["rs"]) in ("EA84_POINTER","RECORD_BASE_0x124","RECORD_BASE_INDEX2") and d["simm"]==0:
            expr[d["rt"]]=expr[d["rs"]]
        elif d["mn"]=="addu" or (d["mn"]=="or" and (d["rs"]==0 or d["rt"]==0)):
            x,y=expr.get(d["rs"],"UNKNOWN"),expr.get(d["rt"],"UNKNOWN")
            if "EA84_POINTER" in (x,y) and "STRIDE_0x124" in (x,y): expr[d["rd"]]="RECORD_BASE_0x124"
            elif "EA84_POINTER" in (x,y) and "INDEX_TIMES_2" in (x,y): expr[d["rd"]]="RECORD_BASE_INDEX2"
            elif y=="ZERO": expr[d["rd"]]=x
            elif x=="ZERO": expr[d["rd"]]=y
            else: expr.pop(d["rd"],None)
        elif d["writes"] is not None: expr.pop(d["writes"],None)
        if stride is not None: expr[stride]="STRIDE_0x124"
        if d["mn"] in ("addiu","ori") and d["rs"]==0 and d["imm"]==0x124: expr[d["rt"]]="CONST_0x124"
        if d["mn"] in ("mult","multu","div","divu"):
            lo=d["mn"] in ("mult","multu") and "CONST_0x124" in (expr.get(d["rs"]),expr.get(d["rt"]))
        if d["mn"] in ("mflo","mfhi"):
            if lo: expr[d["rd"]]="STRIDE_0x124"
            lo=False
        if d["control"]: pending_reset=True
        elif pending_reset: expr={0:"ZERO"}; lo=False; pending_reset=False
    return rows

def self_test():
    assert decode(bytes.fromhex("02 00 03 00"),0x80010000)["mn"]=="srl"
    assert decode((3<<26).to_bytes(4,"little"),0x80010000)["mn"]=="jal"
    assert decode((0x18).to_bytes(4,"little"),0x80010000)["mn"]=="mult"
    assert decode((0x12).to_bytes(4,"little"),0x80010000)["mn"]=="mflo"
    assert decode((0x2a).to_bytes(4,"little"),0x80010000)["mn"]=="slt"
    assert decode((0x21<<26).to_bytes(4,"little"),0x80010000)["mn"]=="lh"
    print("UN0_SELF_TEST=PASS MIPS srl/sra/j/jal/jr/mult/mflo/slt/lh/lhu decoder")
def main():
    p=argparse.ArgumentParser(); p.add_argument("--exe",type=Path); p.add_argument("--data-bin",type=Path); p.add_argument("--out-dir",type=Path); p.add_argument("--self-test",action="store_true"); a=p.parse_args()
    if a.self_test: self_test(); return 0
    if not a.exe or not a.data_bin or not a.out_dir: p.error("--exe --data-bin --out-dir required")
    exe=a.exe.read_bytes(); data=a.data_bin.read_bytes()
    if len(exe)!=EXE_SIZE or digest(exe)!=EXE_SHA: raise SystemExit("UN0_EXE_SIZE_SHA_MISMATCH")
    if len(data)!=DATA_SIZE or digest(data)!=DATA_SHA: raise SystemExit("UN0_DATA_SIZE_SHA_MISMATCH")
    e1=data[E1_OFF:E1_OFF+E1_SIZE]
    if len(e1)!=E1_SIZE or digest(e1)!=E1_SHA: raise SystemExit("UN0_ENTRY1_SIZE_SHA_MISMATCH")
    sites=get_sites(); blobs={}
    for s in sites:
        if s["region"] not in blobs: blobs[s["region"]]=(exe[EXE_OFF:],EXE_OFF) if s["region"]=="EXE" else (e1,E1_OFF)
        s["blob"]=blobs[s["region"]]
    fwd,site_sums=forward(sites,blobs)
    lh=scan_lh_lhu(exe[EXE_OFF:],"EXE",EXE_PC,EXE_OFF)+scan_lh_lhu(e1,"ENTRY1",E1_PC,E1_OFF)
    verified=next((s for s in sites if s["region"]=="ENTRY1" and s["pc"]==0x800C9990 and s["off"]==0x0E),None)
    if verified is None: raise SystemExit("UN0_VERIFIED_SELF_TEST_SITE_MISSING")
    pos=verified["pc"]-E1_PC; vd=decode(e1[pos:pos+4],verified["pc"])
    if vd["mn"] not in ("lh","lhu") or vd["mem"][2]!=0x0E: raise SystemExit("UN0_VERIFIED_SITE_BYTES_FAIL")
    out=a.out_dir; out.mkdir(parents=True,exist_ok=True)
    write_tsv(out/"UN0_FORWARD_READS.tsv",FWD,fwd); write_tsv(out/"UN0_READ_SITE_CLASSIFICATION.tsv",SITES,site_sums); write_tsv(out/"UN0B_ALL_LH_LHU_0E_18.tsv",LH,lh)
    proven=[x for x in lh if x["origin_status"]=="YA"]; cand=[x for x in lh if x["LV_reader_candidate"]!="NO"]
    summary=[("STATUS","SEBAGIAN"),("EVIDENCE_LEVEL","K4 maximum; static bytes/disassembly"),("K5_BLOCKER","UN0 static-only; no repeated runtime launches"),("FIELD_MEANING","TIDAK TAHU"),("UN0_READ_SITES_TOTAL",len(sites)),("UN0_POINTER_ORIGIN_YA",sum(x["origin"]=="YA" for x in sites)),("UN0_POINTER_ORIGIN_UNRESOLVED",sum(x["origin"]!="YA" for x in sites)),("UN0_FORWARD_INSTRUCTION_ROWS",len(fwd)),("UN0_FORWARD_MAX_INSTRUCTIONS_PER_SITE",32),("UN0B_ALL_LH_LHU_DISPLACEMENT_0E_18",len(lh)),("UN0B_EA84_POINTER_BASE_YA",len(proven)),("UN0B_BASE_UNRESOLVED",len(lh)-len(proven)),("UN0B_LV1_LV5_CANDIDATES",len(cand)),("UN0B_CANDIDATE_BASE_YA",sum(x["LV_reader_candidate"]=="YES_PROVEN" for x in cand)),("UN0B_CANDIDATE_BASE_UNRESOLVED",sum(x["LV_reader_candidate"]=="CANDIDATE_BASE_UNRESOLVED" for x in cand)),("VERIFIED_SITE","ENTRY1 PC=0x800C9990; "+vd["text"]),("EXE_MAPPING","0x800+(PC-0x80010000)"),("ENTRY1_MAPPING","0x10BB000+(PC-0x800AD450)"),("EXE_SHA256",digest(exe)),("DATA_BIN_SHA256",digest(data)),("ENTRY1_SHA256",digest(e1))]
    write_tsv(out/"UN0_SUMMARY.tsv",SUMMARY,[{"item":k,"value":v} for k,v in summary])
    print(f"UN0_SEBAGIAN_K4 sites={len(sites)} forward_rows={len(fwd)} LH_LHU={len(lh)} proven={len(proven)} candidates={len(cand)}")
    return 2
if __name__=="__main__": raise SystemExit(main())
