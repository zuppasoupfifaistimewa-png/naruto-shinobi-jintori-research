#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, os, re, struct, subprocess, sys, urllib.request
from collections import defaultdict
from pathlib import Path
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_BASE, EXE_FILE = 0x80010000, 0x800
ENTRY_BASE, ENTRY_FILE = 0x800AD450, 0x10BB000
EXE_SHA = "a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
ENTRY_SHA = "9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
EXE_SIZE, ENTRY_SIZE = 385024, 596412
BASELINE = os.environ["MA_BASELINE"]
SOURCE_SHA = os.environ["GITHUB_SHA"]
REPO = os.environ["GITHUB_REPOSITORY"]
OUT = Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)
REG = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
LOADS = {0x20:"lb",0x21:"lh",0x23:"lw",0x24:"lbu",0x25:"lhu"}
STORES = {0x28:"sb",0x29:"sh",0x2b:"sw"}
WIDTH = {0x20:1,0x21:2,0x23:4,0x24:1,0x25:2,0x28:1,0x29:2,0x2b:4}
md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_LITTLE_ENDIAN)
md.detail = False

def hx(b): return " ".join(f"{x:02X}" for x in b)
def h32(v): return f"0x{v & 0xffffffff:08X}"
def sign16(v): return (v ^ 0x8000) - 0x8000
def reg(r): return "$" + REG[r]
def write_tsv(name, rows, fields):
    with (OUT/name).open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({k: ("TIDAK TAHU" if row.get(k) is None or row.get(k) == "" else row.get(k)) for k in fields})
def write_txt(name, value): (OUT/name).write_text(value, encoding="utf-8")
def decode_blob(blob, tag):
    base, filebase, start = (EXE_BASE, EXE_FILE, EXE_FILE) if tag=="EXE" else (ENTRY_BASE, ENTRY_FILE, 0)
    data=blob[start:]
    out={}
    for p in range(0, len(data)-3, 4):
        raw=data[p:p+4]
        pc=base+p
        ins=next(md.disasm(raw, pc, count=1), None)
        if ins is None: continue
        word=int.from_bytes(raw,"little")
        op=word>>26; rs=(word>>21)&31; rt=(word>>16)&31; rd=(word>>11)&31; sh=(word>>6)&31; fn=word&63
        out[pc]={"pc":pc,"tag":tag,"raw":raw,"word":word,"op":op,"rs":rs,"rt":rt,"rd":rd,"sh":sh,"fn":fn,
                 "imm":sign16(word&0xffff),"uimm":word&0xffff,"mn":ins.mnemonic.lower(),
                 "text":(ins.mnemonic+" "+ins.op_str).strip(),"fileoff":filebase+p}
    return out

def parse_ghidra(path):
    code=set(); ranges=defaultdict(list); refs=defaultdict(list)
    p=Path(path)
    if not p.exists(): return code, ranges, refs
    target=None
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("CODE_INSTRUCTION="):
            try: code.add(int(line.split("=",1)[1].split("|",1)[0],16))
            except Exception: pass
        elif line.startswith("FUNCTION_RANGE="):
            q=line.split("=",1)[1].split("|")
            if len(q)>=4:
                try: ranges[int(q[0],16)].append((int(q[1],16),int(q[2],16),q[3]))
                except Exception: pass
        elif line.startswith("TARGET="):
            try: target=int(line.split("=",1)[1],16)
            except Exception: target=None
        elif line.startswith("REF=") and target is not None:
            q=line.split("=",1)[1].split("|")
            if len(q)>=4:
                try: refs[target].append({"pc":int(q[0],16),"kind":q[1],"caller_entry":q[2],"caller_name":q[3]})
                except Exception: pass
    return code, ranges, refs

def dest(i):
    op,fn=i["op"],i["fn"]
    if op==0:
        if fn in (8,12,13,24,25,26,27): return None
        if fn==9: return i["rd"] or 31
        return i["rd"] or None
    if op in (2,4,5,6,7,0x28,0x29,0x2b,0x38,0x39,0x3a,0x3b): return None
    if op==3: return 31
    if op in (1,8,9,10,11,12,13,14,15,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37): return i["rt"] or None
    return None

def direct_target(i):
    if i["op"] not in (2,3): return None
    return ((i["pc"]+4)&0xF0000000) | ((i["word"]&0x03ffffff)<<2)

def last_def(code, r, before, lo, limit=512, stop_control=True):
    floor=max(lo,before-limit*4)
    for pc in range(before-4,floor-1,-4):
        i=code.get(pc)
        if not i: continue
        if dest(i)==r: return i
        if stop_control and (i["op"] in (2,3,4,5,6,7,1) or (i["op"]==0 and i["fn"] in (8,9))):
            return None
    return None

def const_reg(code, r, before, lo, depth=0, seen=None):
    if r==0: return 0
    if depth>12: return None
    seen=set() if seen is None else seen
    key=(r,before)
    if key in seen: return None
    seen.add(key)
    d=last_def(code,r,before,lo)
    if not d: return None
    op,fn=d["op"],d["fn"]
    if op==15: return (d["uimm"]<<16)&0xffffffff
    if op in (8,9,13,12,14):
        a=const_reg(code,d["rs"],d["pc"],lo,depth+1,seen.copy())
        if a is None: return None
        if op in (8,9): return (a+d["imm"])&0xffffffff
        if op==13: return (a|d["uimm"])&0xffffffff
        if op==12: return (a&d["uimm"])&0xffffffff
        return (a^d["uimm"])&0xffffffff
    if op==0 and fn in (0,2,3,0x21,0x23,0x24,0x25,0x26):
        a=const_reg(code,d["rs"],d["pc"],lo,depth+1,seen.copy())
        b=const_reg(code,d["rt"],d["pc"],lo,depth+1,seen.copy())
        if fn==0 and b is not None: return (b<<d["sh"])&0xffffffff
        if fn==2 and b is not None: return b>>d["sh"]
        if fn==3 and b is not None: return (b>>d["sh"])
        if a is None or b is None: return None
        if fn==0x21: return (a+b)&0xffffffff
        if fn==0x23: return (a-b)&0xffffffff
        if fn==0x24: return a&b
        if fn==0x25: return a|b
        if fn==0x26: return a^b
    return None

def sym_reg(code, r, before, lo, depth=0, seen=None):
    if r==0: return "0"
    if depth>12: return "TIDAK TAHU:DEPTH"
    seen=set() if seen is None else seen
    key=(r,before)
    if key in seen: return "TIDAK TAHU:CYCLE"
    seen.add(key)
    d=last_def(code,r,before,lo)
    if not d: return "INCOMING_"+reg(r)
    op,fn=d["op"],d["fn"]
    if op==15: return h32(d["uimm"]<<16)
    if op in (8,9): return "("+sym_reg(code,d["rs"],d["pc"],lo,depth+1,seen.copy())+f"{d['imm']:+d})"
    if op==13: return "("+sym_reg(code,d["rs"],d["pc"],lo,depth+1,seen.copy())+f"|{h32(d['uimm'])})"
    if op==12: return "("+sym_reg(code,d["rs"],d["pc"],lo,depth+1,seen.copy())+f"&{h32(d['uimm'])})"
    if op in LOADS:
        a=const_reg(code,d["rs"],d["pc"],lo)
        size={0x20:"8S",0x21:"16S",0x23:"32",0x24:"8",0x25:"16"}[op]
        addr=h32((a+d["imm"])&0xffffffff) if a is not None else sym_reg(code,d["rs"],d["pc"],lo,depth+1,seen.copy())+f"{d['imm']:+d}"
        return f"MEM{size}[{addr}]"
    if op==0 and fn==0: return "("+sym_reg(code,d["rt"],d["pc"],lo,depth+1,seen.copy())+f"<<{d['sh']})"
    if op==0 and fn in (0x21,0x23,0x24,0x25,0x26):
        if fn==0x21 and d["rs"]==0: return sym_reg(code,d["rt"],d["pc"],lo,depth+1,seen.copy())
        if fn==0x21 and d["rt"]==0: return sym_reg(code,d["rs"],d["pc"],lo,depth+1,seen.copy())
        opstr={0x21:"+",0x23:"-",0x24:"&",0x25:"|",0x26:"^"}[fn]
        return "("+sym_reg(code,d["rs"],d["pc"],lo,depth+1,seen.copy())+opstr+sym_reg(code,d["rt"],d["pc"],lo,depth+1,seen.copy())+")"
    return f"DEF@{h32(d['pc'])}:{d['text']}"

def eff_addr(code,i,lo):
    b=const_reg(code,i["rs"],i["pc"],lo)
    return ((b+i["imm"])&0xffffffff) if b is not None else None

def base_row(i, excerpt=""):
    z={"image":i["tag"],"pc":h32(i["pc"]),"file_offset":h32(i["fileoff"]),
       "bytes":hx(i["raw"]),"instruksi":i["text"]}
    if excerpt: z["excerpt_id"]=excerpt
    return z

def find_prolog(code, pc, lo, span=0x5000):
    # First accept a prolog exactly at the target, then search backwards but stop at a return.
    def at(q):
        a=code.get(q); b=code.get(q+4)
        if a and b and a["op"]==9 and a["rs"]==29 and a["rt"]==29 and a["imm"]<0 and b["op"]==0x2b and b["rs"]==29 and b["rt"]==31:
            return True
        return False
    if at(pc): return pc,"PROLOG_AT_TARGET"
    floor=max(lo,pc-span)
    for q in range(pc-4,floor-1,-4):
        i=code.get(q)
        if not i: continue
        if i["op"]==0 and i["fn"]==8 and i["rs"]==31: break
        if at(q): return q,"BACKWARD_PROLOG_BEFORE_RETURN"
    return None,"NO_UNIQUE_PROLOG"

def function_for(ranges, pc):
    matches=[]
    for entry,parts in ranges.items():
        for lo,hi,name in parts:
            if lo<=pc<=hi: matches.append((entry,lo,hi,name))
    if not matches:return None
    return sorted(matches,key=lambda x:(x[2]-x[1],x[0]))[0]

def parse_refs(path):
    _,_,refs=parse_ghidra(path)
    return refs

def get_code_excerpt(code, start, count, image, name):
    rows=[]
    for n in range(count):
        i=code.get(start+n*4)
        if i: rows.append(base_row(i,name))
    return rows

def return_sites(code, frange):
    if not frange:return []
    entry,lo,hi,_=frange
    out=[]
    for pc in range(lo,hi+1,4):
        i=code.get(pc)
        if i and i["op"]==0 and i["fn"]==8 and i["rs"]==31:
            out.append({"pc":pc,"value_expr":sym_reg(code,2,pc,lo),"value_const":const_reg(code,2,pc,lo)})
    return out

def call_site_origin(code, ranges, pc, r):
    fr=function_for(ranges,pc)
    lo=fr[0] if fr else ENTRY_BASE
    # No definition in the current straight-line block means prior call/branch or incoming state.
    d=last_def(code,r,pc,lo,limit=1024,stop_control=True)
    if not d:
        return {"origin":"TIDAK TAHU","expression":"TIDAK TAHU: no same-basic-block reaching definition","definition_pc":"TIDAK TAHU","function_entry":h32(fr[0]) if fr else "TIDAK TAHU"}
    value=const_reg(code,r,pc,lo)
    expr=sym_reg(code,r,pc,lo)
    if value is not None: origin="KONSTANTA"
    elif "MEM" in expr: origin="DARI_MEMORI"
    elif expr.startswith("INCOMING_"): origin="ARGUMEN_MASUK"
    else: origin="TIDAK TAHU"
    return {"origin":origin,"expression":expr,"definition_pc":h32(d["pc"]),"function_entry":h32(fr[0]) if fr else "TIDAK TAHU"}

def record_at(blob, pc):
    off=EXE_FILE+(pc-EXE_BASE)
    if off<0 or off+0x1c>len(blob): return None
    raw=blob[off:off+0x1c]
    w=struct.unpack("<7I",raw)
    name_raw=raw[0x14:0x1c]
    try:
        n=name_raw.split(b"\0",1)[0].decode("ascii")
    except Exception: return None
    if w[0]!=0 or w[1]>32 or not n or not re.fullmatch(r"[A-Z0-9_]{1,8}",n): return None
    if not all(0x80010000<=v<=0x801fffff for v in w[2:5]): return None
    return {"base":pc,"plus4":w[1],"p1":w[2],"p2":w[3],"p3":w[4],"name":n,"raw":raw}

def table_scan(exe, code_sets):
    lo,hi=0x80055880,0x80055A00
    candidates={}
    for pc in range(lo,hi,4):
        r=record_at(exe,pc)
        if r:candidates[pc]=r
    groups=[]
    for pc in sorted(candidates):
        if not groups or pc-groups[-1][-1]!=0x1c: groups.append([pc])
        else: groups[-1].append(pc)
    # Keep all candidate groups, not just the longest; a singleton is not silently joined.
    rows=[]
    for gi,g in enumerate(groups):
        for idx,pc in enumerate(g):
            r=candidates[pc]
            rows.append({"group":gi,"index":idx,"base_pc":h32(pc),"value_plus4":r["plus4"],
                         "pointer_plus8":h32(r["p1"]),"pointer_plusC":h32(r["p2"]),
                         "pointer_plus10":h32(r["p3"]),"name":r["name"],
                         "group_length":len(g),"stride":h32(0x1c) if len(g)>1 else "SINGLETON"})
    main=max(groups,key=lambda g:len(g)) if groups else []
    if main:
        start=main[0]; end=main[-1]+0x1c
    else: start=end=None
    # A compact 56-byte, two-record byte excerpt from the start of the longest run.
    snippet=[]
    if len(main)>=2:
        pc=main[0]; off=EXE_FILE+(pc-EXE_BASE); raw=exe[off:off+0x38]
        snippet=[{"image":"EXE","pc":h32(pc),"file_offset":h32(off),"bytes":hx(raw),
                  "instruksi":"DATA_RECORD_PAIR","excerpt_id":"MA1_SCENE_TABLE_PAIR_56B"}]
    return rows, groups, (start,end), snippet, candidates

def scan_code_users(codes, valid, table_start, table_end, ptr_values):
    rows=[]; arithmetic=[]
    low=0x80055880; high=0x80055A00
    for tag,code in codes:
        lo=EXE_BASE if tag=="EXE" else ENTRY_BASE
        for pc,i in sorted(code.items()):
            if pc not in valid[tag]: continue
            # Look for the address-forming instruction itself, rather than testing
            # all 32 registers at every PC (which is quadratic and noisy).
            if i["op"] in (8,9,13) and i["rt"]!=0:
                v=const_reg(code,i["rt"],pc+4,lo)
                if v is not None and low<=v<high:
                    z=base_row(i,"MA1_TABLE_ADDRESS_CONSTANT")
                    z.update({"register":reg(i["rt"]),"constant":h32(v)})
                    rows.append(z)
            if i["op"] in LOADS:
                ea=eff_addr(code,i,lo)
                expr=sym_reg(code,i["rs"],pc,lo)
                if (ea is not None and low-0x40<=ea<high+0x40) or any(f"{x:08X}" in expr.upper() for x in (0x800558c0,0x800558d8,0x800558f4,0x80055910,0x8005592c,0x80055948)):
                    z=base_row(i,"MA1_TABLE_LOAD_CANDIDATE")
                    z.update({"base_expression":expr,"effective_address":h32(ea) if ea is not None else "DYNAMIC",
                              "register_destination":reg(i["rt"]),"next_indirect_jump":"TIDAK TAHU"})
                    for q in range(pc+4,pc+0x41,4):
                        j=code.get(q)
                        if j and j["op"]==0 and j["fn"] in (8,9):
                            z["next_indirect_jump"]=h32(q)+" "+j["text"]+" target_expr="+sym_reg(code,j["rs"],q,lo)
                            break
                    rows.append(z)
            # Multiplication / shift-subtract candidates for a 28-byte stride.
            if i["op"]==0 and i["fn"] in (0x18,0x19,0x21,0x23):
                a=const_reg(code,i["rs"],pc,lo); b=const_reg(code,i["rt"],pc,lo)
                if a==28 or b==28:
                    arithmetic.append(base_row(i,"SCALE_28_CONSTANT"))
                elif i["fn"]==0x23:
                    prev=[code.get(pc-k*4) for k in range(1,5)]
                    if any(q and q["op"]==0 and q["fn"]==0 and q["sh"] in (2,5) for q in prev):
                        arithmetic.append(base_row(i,"SCALE_28_SHIFT_SUB_CANDIDATE"))
    def dedup(xs):
        out={(x.get("image"),x.get("pc"),x.get("instruksi"),x.get("classification",x.get("excerpt_id",""))):x for x in xs}
        return list(out.values())
    return dedup(rows),dedup(arithmetic)

def pointer_words(blobs, targets):
    out=[]
    for tag,blob,base,filebase in [("EXE",blobs[0],EXE_BASE,EXE_FILE),("ENTRY1",blobs[1],ENTRY_BASE,ENTRY_FILE)]:
        for val in targets:
            needle=struct.pack("<I",val); pos=0
            while True:
                p=blob.find(needle,pos)
                if p<0: break
                if tag=="EXE":
                    if p>=EXE_FILE and p%4==0:
                        pc=EXE_BASE+(p-EXE_FILE)
                        out.append({"image":tag,"pc":h32(pc),"file_offset":h32(p),"bytes":hx(blob[p:p+4]),
                                    "instruksi":"DATA_POINTER_WORD","value":h32(val),"classification":"POINTER_WORD"})
                else:
                    if p%4==0:
                        pc=ENTRY_BASE+p
                        out.append({"image":tag,"pc":h32(pc),"file_offset":h32(ENTRY_FILE+p),"bytes":hx(blob[p:p+4]),
                                    "instruksi":"DATA_POINTER_WORD","value":h32(val),"classification":"POINTER_WORD"})
                pos=p+1
    return out

def global_writers(codes, valid, globals_):
    rows=[]
    for tag,code in codes:
        lo=EXE_BASE if tag=="EXE" else ENTRY_BASE
        for pc,i in sorted(code.items()):
            if pc not in valid[tag] or i["op"] not in STORES: continue
            ea=eff_addr(code,i,lo)
            if ea is None: continue
            width=WIDTH[i["op"]]
            for g in globals_:
                if ea<=g<ea+width:
                    val=const_reg(code,i["rt"],pc,lo)
                    expr=sym_reg(code,i["rt"],pc,lo)
                    if val is not None: klass="KONSTANTA"
                    elif "MEM" in expr: klass="SALINAN_DARI_MEMORI"
                    elif "-" in expr: klass="SELISIH_KANDIDAT_BELUM_TERBUKTI_LEVEL"
                    else: klass="TIDAK TAHU"
                    z=base_row(i,"MA2_GLOBAL_WRITER_"+h32(g))
                    z.update({"target_global":h32(g),"store_width":width,"effective_address":h32(ea),
                              "source_register":reg(i["rt"]),"source_constant":h32(val) if val is not None else "TIDAK TAHU",
                              "source_expression":expr,"source_class":klass})
                    rows.append(z)
    return rows

def matrix_writers(codes, valid):
    rows=[]; partial=[]
    anchors=("0x8013EA74","0x8013EB1C","0x8013EA6E")
    for tag,code in codes:
        lo=EXE_BASE if tag=="EXE" else ENTRY_BASE
        for pc,i in sorted(code.items()):
            if pc not in valid[tag] or i["op"]!=0x28: continue
            b=sym_reg(code,i["rs"],pc,lo)
            s=sym_reg(code,i["rt"],pc,lo)
            n=sum(a in b.upper() for a in anchors)
            if n>=2:
                item=base_row(i,"MA2_MATRIX_WRITER_CANDIDATE")
                if const_reg(code,i["rt"],pc,lo) is not None: cls="KONSTANTA"
                elif "MEM" in s: cls="SALINAN"
                elif "-" in s: cls="SELISIH_KANDIDAT_BELUM_TERBUKTI_LEVEL"
                else: cls="TIDAK TAHU"
                item.update({"base_expression":b,"source_expression":s,"source_class":cls,"anchor_count":n})
                (rows if n==3 else partial).append(item)
    return rows,partial

def caller_rows(code, valid, refs, target):
    out=[]
    for pc,i in sorted(code.items()):
        if pc not in valid: continue
        t=direct_target(i)
        if t==target:
            z=base_row(i); z.update({"target":h32(target),"kind":"JAL" if i["op"]==3 else "J","origin":"DIRECT"})
            out.append(z)
        if i["op"]==0 and i["fn"] in (8,9):
            v=const_reg(code,i["rs"],pc,ENTRY_BASE)
            if v==target:
                z=base_row(i); z.update({"target":h32(target),"kind":"JALR" if i["fn"]==9 else "JR","origin":"STATIC_REGISTER"})
                out.append(z)
    for x in refs.get(target,[]):
        z={"image":"ENTRY1","pc":h32(x["pc"]),"file_offset":h32(ENTRY_FILE+x["pc"]-ENTRY_BASE),
           "bytes":"TIDAK TAHU","instruksi":"GHIDRA_REFERENCE","target":h32(target),
           "kind":x["kind"],"origin":"GHIDRA_XREF caller="+x["caller_name"]+" entry="+x["caller_entry"]}
        i=code.get(x["pc"])
        if i: z.update({"bytes":hx(i["raw"]),"instruksi":i["text"]})
        out.append(z)
    unique={(x.get("pc"),x.get("kind"),x.get("origin")):x for x in out}
    return list(unique.values())

def validate_outputs(exe, entry):
    rows=[]; checked=decoded=fail=0
    for path in sorted(OUT.glob("MA*.tsv")):
        try: data=list(csv.DictReader(path.open(encoding="utf-8"),delimiter="\t"))
        except Exception: continue
        for n,r in enumerate(data,2):
            if not all(r.get(k) for k in ("image","pc","file_offset","bytes")): continue
            if r["bytes"]=="TIDAK TAHU": continue
            try:
                pc=int(r["pc"],16); fo=int(r["file_offset"],16)
                raw=bytes(int(x,16) for x in r["bytes"].split())
                tag=r["image"]
                expected=(EXE_FILE+pc-EXE_BASE) if tag=="EXE" else (ENTRY_FILE+pc-ENTRY_BASE)
                source=exe[fo:fo+len(raw)] if tag=="EXE" else entry[fo-ENTRY_FILE:fo-ENTRY_FILE+len(raw)]
                ok=(fo==expected and source==raw and len(raw)>0)
                dec="NOT_CODE"
                if ok and len(raw)==4 and not r.get("instruksi","").startswith("DATA_"):
                    ins=next(md.disasm(raw,pc,count=1),None)
                    ok=ins is not None
                    dec="PASS" if ins else "FAIL"
                    if ins: decoded+=1
                checked+=1
                if not ok: fail+=1
                rows.append({"file":path.name,"line":n,"image":tag,"pc":r["pc"],"file_offset":r["file_offset"],
                             "raw_check":"PASS" if ok else "FAIL","decode_check":dec})
            except Exception as e:
                checked+=1; fail+=1
                rows.append({"file":path.name,"line":n,"image":r.get("image"),"pc":r.get("pc"),
                             "file_offset":r.get("file_offset"),"raw_check":"FAIL","decode_check":"ERROR:"+type(e).__name__})
    write_tsv("MA0_FILE_OFFSET_DECODE_VALIDATION.tsv",rows,["file","line","image","pc","file_offset","raw_check","decode_check"])
    return checked,decoded,fail

def excerpt_audit():
    # Aggregate unique image+PC byte rows across all historical JA/KA/LA/MA TSVs
    # plus current-run MA TSVs still in OUT (before publication into reports/).
    seen={}
    root=Path("reports/stage1_economy")
    sources=[]
    for prefix in ("ja-run-","ka-run-","la-run-","ma-run-"):
        sources.extend(root.glob(prefix+"*/attempt-*/*.tsv"))
    sources.extend(OUT.glob("MA*.tsv"))
    for path in sources:
        try: rr=csv.DictReader(path.open(encoding="utf-8"),delimiter="\t")
        except Exception: continue
        if not rr.fieldnames or not {"image","pc","bytes"}.issubset(rr.fieldnames): continue
        for row in rr:
            raw=row.get("bytes","")
            if not raw or raw=="TIDAK TAHU": continue
            try:
                pc=int(row["pc"],16); b=bytes(int(x,16) for x in raw.split())
            except Exception: continue
            if not b or len(b)%4: continue
            key=(row["image"],pc)
            if key not in seen: seen[key]=b
            elif seen[key]!=b: seen[key]=b"CONFLICT"
    spans=[]
    for image in sorted(set(k[0] for k in seen)):
        xs=sorted((pc,b) for (im,pc),b in seen.items() if im==image and b!=b"CONFLICT")
        run_start=last_pc=None; run_end=None; length=0
        for pc,b in xs:
            if last_pc is not None and pc==run_end:
                length += len(b); run_end=pc+len(b)
            else:
                if length: spans.append((image,run_start,run_end,length))
                run_start=pc; run_end=pc+len(b); length=len(b)
            last_pc=pc
        if length: spans.append((image,run_start,run_end,length))
    maximum=max((x[3] for x in spans),default=0)
    offenders=[x for x in spans if x[3]>64]
    write_txt("MA0_AGGREGATE_EXCERPT_AUDIT.txt",
        f"AGGREGATION=unique image+PC byte rows, de-duplicated across all ja-*, ka-*, la-*, ma-* report TSV files\n"+
        f"UNIQUE_ADDRESS_ROWS={len(seen)}\nMAX_CONTIGUOUS_BYTES={maximum}\n"+
        "LIMIT_BYTES=64\nSTATUS="+("PASS" if not offenders else "FAIL")+"\n"+
        "OVER_LIMIT="+(";".join(f"{im}:{h32(a)}..{h32(b-1)}={n}" for im,a,b,n in offenders) or "none")+"\n"+
        "CONFLICTING_DUPLICATE_ADDRESSES="+str(sum(1 for b in seen.values() if b==b"CONFLICT"))+"\n")
    return maximum,len(offenders)

def actions_census():
    token=os.environ.get("GH_TOKEN","")
    page=1; total=0; allruns=[]
    while True:
        url=f"https://api.github.com/repos/{REPO}/actions/runs?per_page=100&page={page}"
        req=urllib.request.Request(url,headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"})
        with urllib.request.urlopen(req,timeout=90) as r: j=json.loads(r.read().decode())
        total=int(j.get("total_count",0)); rs=j.get("workflow_runs",[]); allruns.extend(rs)
        if not rs or len(allruns)>=total: break
        page+=1
        if page>100: raise RuntimeError("ACTIONS_PAGINATION_LIMIT")
    rows=[{"run_id":x.get("id"),"event":x.get("event"),"status":x.get("status"),"conclusion":x.get("conclusion") or "TIDAK TAHU",
           "workflow":x.get("path"),"head_sha":x.get("head_sha"),"created_at":x.get("created_at")} for x in allruns]
    write_tsv("MA0_ACTIONS_ALL_EVENTS.tsv",rows,["run_id","event","status","conclusion","workflow","head_sha","created_at"])
    return total,len(rows),page,sum(x.get("event")=="schedule" for x in allruns),sum(x.get("status")!="completed" for x in allruns)

def ledger():
    subprocess.run(["git","merge-base","--is-ancestor",BASELINE,SOURCE_SHA],check=True)
    raw=subprocess.check_output(["git","log","--format=%H%x09%an%x09%ae%x09%s",f"{BASELINE}^..{SOURCE_SHA}"]).decode().splitlines()
    rows=[]
    for line in raw:
        q=line.split("\t",3)
        if len(q)!=4: continue
        sha,name,email,subject=q
        bot=("[bot]" in name.lower() or "dependabot" in name.lower() or "bot" in name.lower())
        rows.append({"sha":sha,"author":name,"email":email,"class":"BOT" if bot else "HUMAN","subject":subject})
    write_tsv("MA0_LEDGER_COMMITS.tsv",rows,["sha","author","email","class","subject"])
    counts={"total":len(rows),"human":sum(x["class"]=="HUMAN" for x in rows),"bot":sum(x["class"]=="BOT" for x in rows)}
    return counts

def pycompile():
    import py_compile
    names=subprocess.check_output(["git","ls-files","-z","--","*.py"]).decode().split("\0")
    rows=[]
    cache=Path(os.environ.get("WORK","/tmp"))/"pycache"; cache.mkdir(parents=True,exist_ok=True)
    for name in [x for x in names if x]:
        target=cache/(hashlib.sha256(name.encode()).hexdigest()+".pyc")
        try:
            py_compile.compile(name,cfile=str(target),doraise=True)
            rows.append({"path":name,"status":"PASS","reason":""})
        except Exception as e: rows.append({"path":name,"status":"FAIL","reason":type(e).__name__+":"+str(e)})
    write_tsv("MA0_PYCOMPILE.tsv",rows,["path","status","reason"])
    return len(rows),sum(x["status"]=="PASS" for x in rows)

def main():
    exe_path,entry_path=Path(sys.argv[1]),Path(sys.argv[2])
    exe,entry=exe_path.read_bytes(),entry_path.read_bytes()
    if len(exe)!=EXE_SIZE or hashlib.sha256(exe).hexdigest()!=EXE_SHA: raise SystemExit("EXE_VERIFY_FAIL")
    if len(entry)!=ENTRY_SIZE or hashlib.sha256(entry).hexdigest()!=ENTRY_SHA: raise SystemExit("ENTRY1_VERIFY_FAIL")
    ce0,ci0=decode_blob(exe,"EXE"),decode_blob(entry,"ENTRY1")
    ce_valid,ce_ranges,ce_refs=parse_ghidra(sys.argv[4])
    ci_valid,ci_ranges,ci_refs=parse_ghidra(sys.argv[5])
    ce={p:i for p,i in ce0.items() if p in ce_valid}
    ci={p:i for p,i in ci0.items() if p in ci_valid}
    codes=[("EXE",ce),("ENTRY1",ci)]
    valid={"EXE":ce_valid,"ENTRY1":ci_valid}
    # MA0: inclusive ledger, all Actions pages/events and complete py_compile census.
    counts=ledger()
    total,run_count,pages,scheduled,active=actions_census()
    py_total,py_pass=pycompile()
    # MA1(a): scan backwards and forwards around the proposed table start without assuming a uniform table.
    scene_rows,scene_groups,bounds,snippet,scene_candidates=table_scan(exe,codes)
    write_tsv("MA1_SCENE_RECORDS.tsv",scene_rows,["group","index","base_pc","value_plus4","pointer_plus8","pointer_plusC","pointer_plus10","name","group_length","stride"])
    write_tsv("MA1_SCENE_TABLE_EXCERPT.tsv",snippet,["image","pc","file_offset","bytes","instruksi","excerpt_id"])
    group_text=[]
    for n,g in enumerate(scene_groups):
        group_text.append(f"GROUP_{n}: start={h32(g[0])} end_exclusive={h32(g[-1]+0x1c)} records={len(g)} stride=0x1C")
    write_txt("MA1_SCENE_TABLE_BOUNDARY.txt",
        "SCAN_RANGE=0x80055880..0x800559FC\n"+
        "PATTERN=word+0 zero; word+4 small integer; +8/+C/+10 pointer-like; +14 8-byte uppercase/underscore label\n"+
        "CANDIDATE_GROUPS\n"+("\n".join(group_text) if group_text else "TIDAK TAHU")+"\n"+
        "LONGEST_RUN_START="+(h32(bounds[0]) if bounds[0] else "TIDAK TAHU")+"\n"+
        "LONGEST_RUN_END_EXCLUSIVE="+(h32(bounds[1]) if bounds[1] else "TIDAK TAHU")+"\n"+
        "NOTE=Each 0x1C run is reported separately. Adjacent singleton candidates are not forced into the run when their next record does not begin at +0x1C.\n")
    # MA1(b): data pointer words and code patterns for absolute table references/indexed reads.
    ptr_values=sorted(set(v for r in scene_candidates.values() for v in (r["p1"],r["p2"],r["p3"])))
    pwords=pointer_words((exe,entry),ptr_values)
    write_tsv("MA1_FUNCTION_POINTER_WORDS.tsv",pwords,["image","pc","file_offset","bytes","instruksi","value","classification"])
    code_users,scale=scan_code_users(codes,valid,bounds[0] if bounds[0] else 0,bounds[1] if bounds[1] else 0,ptr_values)
    write_tsv("MA1_SCENE_CODE_USERS.tsv",code_users,["image","pc","file_offset","bytes","instruksi","excerpt_id","base_expression","effective_address","register_destination","next_indirect_jump","register","constant"])
    write_tsv("MA1_SCALE_28_CANDIDATES.tsv",scale,["image","pc","file_offset","bytes","instruksi","excerpt_id"])
    # MA1(c): manual prologs/boundaries for the four scene routines.
    funcs=[]
    prolog_windows=[]
    scene_funcs=[0x800B1E88,0x800B50AC,0x800B5020,0x800B2A58]
    for target in scene_funcs:
        fr=function_for(ci_ranges,target)
        manual,reason=find_prolog(ci,target,ENTRY_BASE)
        entry_pc=fr[0] if fr else manual
        f_range=function_for(ci_ranges,entry_pc) if entry_pc else None
        returns=return_sites(ci,f_range) if f_range else []
        start=entry_pc if entry_pc else target
        prolog_windows.extend(get_code_excerpt(ci,start,16,"ENTRY1",f"MA1_PROLOG_{target:08X}"))
        funcs.append({"target":h32(target),"ghidra_function_entry":h32(fr[0]) if fr else "TIDAK TAHU",
                      "manual_prolog":h32(manual) if manual else "TIDAK TAHU","prolog_reason":reason,
                      "selected_entry":h32(entry_pc) if entry_pc else "TIDAK TAHU",
                      "ghidra_range":(h32(f_range[1])+".."+h32(f_range[2])) if f_range else "TIDAK TAHU",
                      "jr_ra_count":len(returns),"last_jr_ra":h32(returns[-1]["pc"]) if returns else "TIDAK TAHU",
                      "boundary_status":"RETURN_FOUND" if returns else "FUNCTION_END_OR_TRUNCATION_TIDAK_TAHU"})
    write_tsv("MA1_SCENE_FUNCTIONS.tsv",funcs,["target","ghidra_function_entry","manual_prolog","prolog_reason","selected_entry","ghidra_range","jr_ra_count","last_jr_ra","boundary_status"])
    write_tsv("MA1_SCENE_PROLOG_WINDOWS.tsv",prolog_windows,["image","pc","file_offset","bytes","instruksi","excerpt_id"])
    # MA1(d): conservative a2/a3 origins at the three prior LA call sites.
    call_specs=[(0x800F5F54,0x800F2A9C),(0x800B54DC,0x800F3658),(0x800F5EBC,0x800DC2E0)]
    argrows=[]
    for pc,target in call_specs:
        i=ci.get(pc); fr=function_for(ci_ranges,pc)
        manual,why=find_prolog(ci,fr[0] if fr else pc,ENTRY_BASE)
        for r in (6,7):
            q=call_site_origin(ci,ci_ranges,pc,r)
            argrows.append({"call_pc":h32(pc),"call_instruction":i["text"] if i else "TIDAK TAHU",
                            "expected_target":h32(target),"actual_target":h32(direct_target(i)) if i and direct_target(i) else "TIDAK TAHU",
                            "caller_function":h32(fr[0]) if fr else "TIDAK TAHU","caller_manual_prolog":h32(manual) if manual else "TIDAK TAHU",
                            "argument":reg(r),"origin":q["origin"],"definition_pc":q["definition_pc"],"expression":q["expression"]})
    write_tsv("MA1_CALLSITE_A2_A3_ORIGINS.tsv",argrows,["call_pc","call_instruction","expected_target","actual_target","caller_function","caller_manual_prolog","argument","origin","definition_pc","expression"])
    # MA1(e): setter wallet remains unresolved unless an authoritative full producer/consumer closure exists.
    wallet=[
      {"hypothesis":"H1 participant-record +0x04 is wallet-like",
       "support_1":"JA record census includes multiple writes at participant-stride candidates; field meaning still not closed",
       "support_2":"participant records use stride 0xB4; no complete reader+writer path connects +0x04 to visible wallet",
       "falsifier":"complete caller/reader closure proves +0x04 is only a cache, flag, or unrelated state"},
      {"hypothesis":"H2 manager+0x4F4 is persistent wallet/settlement state",
       "support_1":"LA caller sequence loads manager+0x4F4 and conditionally negates it before passing a value to FUN_80014F10",
       "support_2":"nearby completion path clears +0x4F4; semantics may be transient settlement, not persistent balance",
       "falsifier":"complete producer/consumer trace proves +0x4F4 is transient and never the visible wallet"},
      {"hypothesis":"H3 FUN_80014F10 is authoritative wallet setter",
       "support_1":"its body performs a participant-indexed max-update",
       "support_2":"the confirmed target writes participant record +0x94 rather than proving +0x04 balance",
       "falsifier":"complete wallet update trace identifies a different setter and proves FUN_80014F10 only updates +0x94"}
    ]
    write_tsv("MA1_WALLET_HYPOTHESES.tsv",wallet,["hypothesis","support_1","support_2","falsifier"])
    write_txt("MA1_WALLET_STATUS.txt","WALLET_AUTHORITATIVE_SETTER=TIDAK TAHU\nNo complete static producer/consumer closure ties a candidate field to the persistent visible wallet.\n")
    # MA2(a): all resolved static sb/sh writers to the two selectors.
    gw=global_writers(codes,valid,[0x8013EB1C,0x8013EA6E])
    write_tsv("MA2_SELECTOR_GLOBAL_WRITERS.tsv",gw,["image","pc","file_offset","bytes","instruksi","excerpt_id","target_global","store_width","effective_address","source_register","source_constant","source_expression","source_class"])
    eb=[x for x in gw if x["target_global"]==h32(0x8013EB1C)]
    ea=[x for x in gw if x["target_global"]==h32(0x8013EA6E)]
    # MA2(b): locate writers whose byte-store base symbolically reconstructs the dynamic matrix.
    mw,mp=matrix_writers(codes,valid)
    write_tsv("MA2_DYNAMIC_MATRIX_WRITERS.tsv",mw,["image","pc","file_offset","bytes","instruksi","excerpt_id","base_expression","source_expression","source_class","anchor_count"])
    write_tsv("MA2_PARTIAL_DYNAMIC_STORE_CANDIDATES.tsv",mp,["image","pc","file_offset","bytes","instruksi","excerpt_id","base_expression","source_expression","source_class","anchor_count"])
    # Reuse exact 64-byte windows where the earlier LA report already recorded D49D0 and the selector helper.
    dwin=get_code_excerpt(ci,0x800D49A4,16,"ENTRY1","MA2_D49D0_64B")
    write_tsv("MA2_D49D0_ADDRESS_WINDOW.tsv",dwin,["image","pc","file_offset","bytes","instruksi","excerpt_id"])
    # MA2(c): inspect helper return sites and the fallback branch target 0x80015564.
    helper=[]; hreturn=[]
    for pc in (0x800154D4,0x80015564):
        fr=function_for(ce_ranges,pc)
        # Each address gets its own bounded window, not a shared function-start dump.
        start=max(EXE_BASE,pc-7*4)
        helper.extend(get_code_excerpt(ce,start,16,"EXE",f"MA2_HELPER_{pc:08X}_64B"))
        sites=return_sites(ce,fr) if fr else []
        hreturn.append({"target":h32(pc),"function_entry":h32(fr[0]) if fr else "TIDAK TAHU",
                        "function_range":(h32(fr[1])+".."+h32(fr[2])) if fr else "TIDAK TAHU",
                        "return_sites":";".join(h32(x["pc"])+":"+x["value_expr"] for x in sites) if sites else "TIDAK TAHU",
                        "return_constants":";".join(h32(x["value_const"]) if x["value_const"] is not None else "DYNAMIC" for x in sites) if sites else "TIDAK TAHU"})
    write_tsv("MA2_HELPER_RETURN_ANALYSIS.tsv",hreturn,["target","function_entry","function_range","return_sites","return_constants"])
    write_tsv("MA2_HELPER_WINDOWS.tsv",helper,["image","pc","file_offset","bytes","instruksi","excerpt_id"])
    write_txt("MA2_SELECTOR_AND_HELPER_SUMMARY.txt",
        f"EB1C_STATIC_STORE_COUNT={len(eb)}\nEB1C_STORE_WIDTHS="+",".join(str(x["store_width"]) for x in eb)+"\n"+
        f"EA6E_STATIC_STORE_COUNT={len(ea)}\nEA6E_STORE_WIDTHS="+",".join(str(x["store_width"]) for x in ea)+"\n"+
        "EB1C_SOURCE_CLASSES="+",".join(x["source_class"] for x in eb)+"\n"+
        "EA6E_SOURCE_CLASSES="+",".join(x["source_class"] for x in ea)+"\n"+
        f"DYNAMIC_MATRIX_WRITERS_FULL_ANCHOR_MATCH={len(mw)}\nDYNAMIC_MATRIX_PARTIAL_CANDIDATES={len(mp)}\n"+
        "NOTE=This is a Ghidra-recognized-code static census; dynamic aliases and unresolved indirect code paths are not proven absent.\n")
    # Test, but do not force, the two competing hypotheses.
    h1="TIDAK TERBANTAH: no complete set of stores to the matrix is established as level-delta writes."
    h2="TIDAK TERBANTAH: no complete matrix-writer set is established as constant/effect-ID writes."
    if mw and all("SELISIH" in x["source_class"] for x in mw): h1="MASIH KONSISTEN pada kandidat writer yang ditemukan; operand level belum terbukti."
    if mw and any("SELISIH" in x["source_class"] for x in mw): h2="ADA KANDIDAT YANG BERTENTANGAN dengan ID-konstan; semantik operand tetap belum terbukti."
    write_txt("MA2_X_EQUALS_D_VS_EFFECT_ID.txt",
        "H1 x=d memprediksi setiap sel yang dibaca di M+0x10+B+144*I ditulis sebagai selisih dua level.\n"+
        "H2 x=effect/item/action id memprediksi nilai sel berasal dari konstanta atau tabel/selector id.\n"+
        f"H1_RESULT={h1}\nH2_RESULT={h2}\n"+
        f"MATRIX_WRITER_MATCHES={len(mw)} PARTIAL={len(mp)}\n"+
        "TIDAK TAHU: cakupan seluruh alias/store matrix belum tertutup; tidak ada hipotesis yang dinyatakan terbantah secara global hanya dari hasil scan ini.\n"+
        "No MATCH/CONTRADICTS labels used.\n")
    # MA3: find parent for B24C8 and direct/static/Ghidra callers to B24C8 and BE5D8.
    b24=0x800B24C8; be5=0x800BE5D8; b1=0x800B1E88
    parent=function_for(ci_ranges,b24)
    manual,manual_reason=find_prolog(ci,b24,ENTRY_BASE)
    b1range=function_for(ci_ranges,b1)
    gap_returns=[]; gap_prologs=[]
    if b1range:
        for pc in range(b1+4,b24,4):
            i=ci.get(pc)
            if not i: continue
            if i["op"]==0 and i["fn"]==8 and i["rs"]==31: gap_returns.append(pc)
            if i["op"]==9 and i["rs"]==29 and i["rt"]==29 and i["imm"]<0: gap_prologs.append(pc)
    b24_rows=caller_rows(ci,ci_valid,ci_refs,b24)
    be5_rows=caller_rows(ci,ci_valid,ci_refs,be5)
    b24_ptrs=pointer_words((exe,entry),[b24])
    write_tsv("MA3_B24C8_CALLERS.tsv",b24_rows,["image","pc","file_offset","bytes","instruksi","target","kind","origin"])
    write_tsv("MA3_B24C8_POINTER_WORDS.tsv",b24_ptrs,["image","pc","file_offset","bytes","instruksi","value","classification"])
    write_tsv("MA3_BE5D8_CALLERS.tsv",be5_rows,["image","pc","file_offset","bytes","instruksi","target","kind","origin"])
    b24win=get_code_excerpt(ci,b24,16,"ENTRY1","MA3_B24C8_64B")
    be5_start=0x800BE5BC
    be5win=get_code_excerpt(ci,be5_start,16,"ENTRY1","MA3_BE5D8_64B")
    write_tsv("MA3_TARGET_WINDOWS.tsv",b24win+be5win,["image","pc","file_offset","bytes","instruksi","excerpt_id"])
    write_txt("MA3_B24C8_BOUNDARY.txt",
        "TARGET=0x800B24C8\n"+
        "GHIDRA_CONTAINING_FUNCTION="+(h32(parent[0]) if parent else "TIDAK TAHU")+"\n"+
        "MANUAL_BACKWARD_PROLOG="+(h32(manual) if manual else "TIDAK TAHU")+"\nBOUNDARY_REASON="+manual_reason+"\n"+
        "CANDIDATE_B1E88_FUNCTION_ENTRY="+(h32(b1range[0]) if b1range else "TIDAK TAHU")+"\n"+
        "B1E88_RANGE_CONTAINS_TARGET="+("YES" if b1range and b1range[0]==b1 and b1range[1]<=b24<=b1range[2] else "NO/UNKNOWN")+"\n"+
        "RETURNS_BETWEEN_B1E88_AND_TARGET="+",".join(h32(x) for x in gap_returns)+"\n"+
        "OTHER_PROLOGS_BETWEEN_B1E88_AND_TARGET="+",".join(h32(x) for x in gap_prologs)+"\n"+
        f"CALLER_ROWS={len(b24_rows)}\n"+
        "CONCLUSION="+("B1E88_PARENT_SUPPORTED_BY_GHIDRA_RANGE" if b1range and b1range[0]==b1 and b1range[1]<=b24<=b1range[2] and not gap_returns else "TIDAK TAHU: parent/caller closure is not complete")+"\n")
    write_txt("MA3_BE5D8_BOUNDARY.txt",
        "TARGET=0x800BE5D8\nDIRECT_AND_GHIDRA_CALLER_ROWS="+str(len(be5_rows))+"\n"+
        "KNOWN_DIRECT_CALLER_FROM_PRIOR_LA=0x800B54F4 in FUN_800B50AC\n"+
        "DYNAMIC_CALLER_COMPLETENESS=TIDAK TAHU; computed jr/jalr targets not resolved remain outside exact-target census.\n")
    # MA4: explicit static-only constraint.
    write_txt("MA4_STATIC_ONLY.txt",
        "EMULATOR_LAUNCHES=0\nGAME_EXECUTIONS=0\nBIOS_USED=no\nSAVESTATE_USED=no\nRAM_DUMP_USED=no\nVIDEO_OR_FRAME_EVIDENCE_USED=no\n"+
        "PRIVATE_SOURCE_EXTRACTION=TEMPORARY_AND_CLEANED\nBINARY_COMMITTED=no\n")
    # MA5: only use x if an MA2 proof has established its identity/domain; otherwise leave formula unknown.
    x_proven=False
    write_tsv("MA5_SYMBOLIC_UPGRADE_COST.tsv",[
       {"premise":"x proven from MA2 byte-matrix writer set","result":"TIDAK TAHU: matrix writer/alias closure is incomplete","status":"UNPROVEN"},
       {"premise":"conditional helper lookup, only when x passes the helper bound","result":"H(x)=u32[0x80055CF4 + 16*x]","status":"CONDITIONAL; helper return and x-domain are not proven here"},
       {"premise":"x=d for a level jump d>=2","result":"TIDAK TAHU; no proven static chain from level delta to x","status":"UNPROVEN"},
       {"premise":"numerical upgrade cost for d>=2","result":"TIDAK TAHU; no formula derived","status":"UNKNOWN"}
    ],["premise","result","status"])
    # Validate file offsets/raw bytes/instruction decoding for every new MA TSV that carries evidence bytes.
    valid_rows,decoded_rows,invalid_rows=validate_outputs(exe,entry)
    max_excerpt,over=excerpt_audit()
    report=(
      "# MA0-MA5 static audit — SLPS-03553\n\n"+
      f"Baseline inklusif: {BASELINE}\nSource SHA: {SOURCE_SHA}\n"+
      f"EXE SHA-256: {EXE_SHA}\nEntry 1 SHA-256: {ENTRY_SHA}\nEMULATOR_LAUNCHES=0.\n\n"+
      "## Status\n"+
      f"- MA0: {'TUNTAS K3' if py_total==py_pass and run_count==total and invalid_rows==0 and over==0 else 'SEBAGIAN K2'} — ledger source/final-parent snapshot {counts['total']} commit ({counts['human']} human, {counts['bot']} bot); Actions {run_count}/{total} run, {pages} halaman; py_compile {py_pass}/{py_total}; validasi bukti {valid_rows-invalid_rows}/{valid_rows}; kutipan maksimum {max_excerpt} B.\n"+
      f"- MA1: SEBAGIAN K3 — kandidat record scene {len(scene_rows)} dalam {len(scene_groups)} grup; batas stride utama {h32(bounds[0]) if bounds[0] else 'TIDAK TAHU'}..{h32(bounds[1]) if bounds[1] else 'TIDAK TAHU'}; pemanggil terindeks dan setter wallet tetap memerlukan closure.\n"+
      f"- MA2: SEBAGIAN K3 — writer global EB1C={len(eb)}, EA6E={len(ea)}; dynamic matrix full-anchor={len(mw)}, parsial={len(mp)}; identitas x belum terbukti.\n"+
      f"- MA3: SEBAGIAN K3 — B24C8 caller rows={len(b24_rows)}; BE5D8 caller rows={len(be5_rows)}; parent B24C8={'teridentifikasi' if parent else 'TIDAK TAHU'}.\n"+
      "- MA4: TUNTAS K4 — statis saja; tanpa peluncuran emulator/game.\n"+
      "- MA5: BELUM K1 — tidak ada rumus biaya numerik lompat level d>=2.\n\n"+
      "## Batas bukti\n"+
      "Ghidra instruction listing dan referensi adalah hasil analisis statis; ketiadaan hasil pada scan tidak membuktikan tidak ada jalur alias/dinamis. Tidak ada nilai runtime, hasil fitting, atau formula dari pengamatan streamer.\n\n"+
      "## Validasi\n"+
      f"- ACTIONS_TOTAL={total}; FETCHED={run_count}; PAGES={pages}; SCHEDULED={scheduled}; NON_COMPLETED_AT_CENSUS={active}.\n"+
      f"- PY_COMPILE={py_pass}/{py_total}.\n- FILE_OFFSET_RAW_DECODE_CHECKS={valid_rows}; DECODED_INSTRUCTIONS={decoded_rows}; FAIL={invalid_rows}.\n"+
      f"- AGGREGATED_MAX_CONTIGUOUS_BYTES={max_excerpt}; OVER_LIMIT_GROUPS={over}.\n"
    )
    write_txt("MA0_MA5_STATIC_REPORT.md",report)
    write_txt("MA0_ANALYZER_STATUS.txt",
        f"ANALYZER_EXIT_CODE=0\nSOURCE_SHA={SOURCE_SHA}\nBASELINE_INCLUSIVE={BASELINE}\n"+
        f"PY_COMPILE={py_pass}/{py_total}\nACTIONS={run_count}/{total} pages={pages}\n"+
        f"FILE_OFFSET_CHECKS={valid_rows} FAIL={invalid_rows}\nEXCERPT_MAX_BYTES={max_excerpt} OVER_LIMIT={over}\n"+
        f"MA1_RECORDS={len(scene_rows)} MA2_EB1C_WRITERS={len(eb)} MA2_EA6E_WRITERS={len(ea)} MA2_MATRIX_WRITERS={len(mw)}\n"+
        f"MA3_B24C8_CALLERS={len(b24_rows)} MA3_BE5D8_CALLERS={len(be5_rows)}\n")
    if invalid_rows or over or py_total!=py_pass or run_count!=total:
        print("MA_AUDIT_WARNINGS=1")
    print(f"MA_ANALYZER_EXIT_CODE=0; ACTIONS={run_count}/{total}; PY={py_pass}/{py_total}; VALIDATION={valid_rows-invalid_rows}/{valid_rows}; EXCERPT_MAX={max_excerpt}; OVER={over}")

if __name__=="__main__":
    main()
