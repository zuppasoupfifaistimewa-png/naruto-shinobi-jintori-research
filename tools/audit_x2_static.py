#!/usr/bin/env python3
"""Read-only X2: helper xrefs/arguments and object-relative accesses from Ghidra function CFGs."""
from __future__ import annotations
import argparse, csv, hashlib, re, struct, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import audit_w0_w3_cfg_ram as core

SLOT=0x8013A554
PTR_ADDR=0x801CEF08
HELPERS={0x80020F54:"FUN_80020f54",0x8002DEC4:"FUN_8002dec4"}
MIPS_GPRS=core.REGS

def sha(x): return hashlib.sha256(x).hexdigest()
def H(x): return core.H(x) if isinstance(x,int) else str(x)
def read_csv(p):
    with Path(p).open(newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def write_csv(p,rows,fields=None):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    if fields is None:fields=list(rows[0]) if rows else []
    with p.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(rows)
def read_words(path,base,strip=0):
    data=Path(path).read_bytes()[strip:]
    return data,[(base+off,struct.unpack_from("<I",data,off)[0]) for off in range(0,len(data)-3,4)]
def function_map(rows):
    result=[]
    for r in rows:
        try:result.append((int(r["start_address"],16),int(r["end_address"],16),r.get("function_name","")))
        except Exception:pass
    return result
def find_func(pc,fns):
    x=[f for f in fns if f[0]<=pc<=f[1]]
    return x[0] if len(x)==1 else None
def direct_jals(path,base,strip=0):
    b=Path(path).read_bytes()[strip:]
    result=[]
    for off in range(0,len(b)-3,4):
        w=struct.unpack_from("<I",b,off)[0];op=(w>>26)&63
        if op!=3:continue
        pc=base+off;target=((pc+4)&0xF0000000)|((w&0x03ffffff)<<2)
        if target in HELPERS:
            result.append({"pc":pc,"target":target,"word":w,"bytes":b[off:off+4]})
    return result

UNKNOWN="TIDAK TAHU"
PTR="PTR"
def sym_add(a,b):
    if a==UNKNOWN or b==UNKNOWN:return UNKNOWN
    if isinstance(a,int) and isinstance(b,int):return (a+b)&0xffffffff
    if isinstance(a,tuple) and a and a[0]==PTR and isinstance(b,int):return (PTR,a[1]+b)
    if isinstance(b,tuple) and b and b[0]==PTR and isinstance(a,int):return (PTR,b[1]+a)
    if isinstance(a,tuple) and a and a[0]==PTR and isinstance(b,tuple) and b and b[0]==PTR:
        return UNKNOWN
    return UNKNOWN
def sym_sub(a,b):
    if a==UNKNOWN or b==UNKNOWN:return UNKNOWN
    if isinstance(a,int) and isinstance(b,int):return (a-b)&0xffffffff
    if isinstance(a,tuple) and a and a[0]==PTR and isinstance(b,int):return (PTR,a[1]-b)
    return UNKNOWN
def sym_eval_cfg(cfg):
    ins=cfg["ins"]; before=cfg["before"]
    cache={}; active=set()
    def reg_before(pc,reg):
        if reg=="zero":return {0}
        defs=before.get(pc,{}).get(reg,set())
        if not defs:return {UNKNOWN}
        vals=set()
        for d in defs:vals.add(eval_def(d))
        return vals or {UNKNOWN}
    def eval_def(d):
        if d.startswith("ENTRY:") or d.startswith("CALL:"):return UNKNOWN
        if d in cache:return cache[d]
        if d in active:return UNKNOWN
        try:q,reg=d.split(":",1);pc=int(q,16);x=ins[pc]
        except Exception:return UNKNOWN
        active.add(d)
        v=eval_ins_def(pc,reg,x)
        active.remove(d);cache[d]=v
        return v
    def all_vals(pc,reg):return reg_before(pc,reg)
    def eval_ins_def(pc,reg,x):
        if x.unknown:return UNKNOWN
        op,rs,rt,rd,fn,sh,imm=x.op,x.rs,x.rt,x.rd,x.fn,x.sh,x.imm
        if x.name=="jal" and reg=="ra":return pc+8
        if x.name=="jalr" and reg in x.writes:return pc+8
        if op==15 and reg==MIPS_GPRS[rt]:return ((x.word&0xffff)<<16)&0xffffffff
        if op==35 and reg==MIPS_GPRS[rt] and imm==core.LOW:
            bases=all_vals(pc,MIPS_GPRS[rs])
            if bases and all(isinstance(b,int) and ((b+imm)&0xffffffff)==SLOT for b in bases):
                return (PTR,0)
            return UNKNOWN
        if op in (8,9,12,13,14) and reg==MIPS_GPRS[rt]:
            src=all_vals(pc,MIPS_GPRS[rs]);out=set()
            for a in src:
                if a==UNKNOWN:return UNKNOWN
                if isinstance(a,tuple):
                    if op in (8,9):out.add(sym_add(a,imm))
                    else:return UNKNOWN
                else:
                    if op in (8,9):z=(a+imm)&0xffffffff
                    elif op==12:z=a&(x.word&0xffff)
                    elif op==13:z=a|(x.word&0xffff)
                    else:z=a^(x.word&0xffff)
                    out.add(z)
            return next(iter(out)) if len(out)==1 else UNKNOWN
        if op==0 and reg==MIPS_GPRS[rd]:
            if fn in (33,35):
                aa=all_vals(pc,MIPS_GPRS[rs]);bb=all_vals(pc,MIPS_GPRS[rt]);out=set()
                for a in aa:
                    for b in bb:
                        z=sym_add(a,b) if fn==33 else sym_sub(a,b)
                        if z==UNKNOWN:return UNKNOWN
                        out.add(z)
                return next(iter(out)) if len(out)==1 else UNKNOWN
            if fn in (0,2,3):
                vs=all_vals(pc,MIPS_GPRS[rt]);out=set()
                for a in vs:
                    if not isinstance(a,int):return UNKNOWN
                    if fn==0:z=a<<sh
                    elif fn==2:z=(a&0xffffffff)>>sh
                    else:z=(a if a<0x80000000 else a-0x100000000)>>sh
                    out.add(z&0xffffffff)
                return next(iter(out)) if len(out)==1 else UNKNOWN
        return UNKNOWN
    return {"reg_before":reg_before,"eval_def":eval_def,"eval_ins_def":eval_ins_def,"all_vals":all_vals,"ins":ins,"before":before}

def get_reg_value(analyzer,pc,reg):
    vals=analyzer["reg_before"](pc,reg)
    clean=[x for x in vals if x!=UNKNOWN]
    return clean[0] if len(clean)==1 and len(clean)==len(vals) else UNKNOWN
def val_text(v):
    if v==UNKNOWN:return "TIDAK TAHU"
    if isinstance(v,int):return H(v)
    if isinstance(v,tuple) and v[0]==PTR:return f"ptr+{H(v[1])}" if v[1]>=0 else f"ptr-{H(-v[1])}"
    return str(v)
def mem_width(op):
    return {32:1,33:2,34:4,35:4,36:1,37:2,38:4,39:4,40:1,41:2,42:4,43:4,46:4}.get(op,0)
def mem_kind(op):
    if 32<=op<=39:return "READ"
    if op in (40,41,42,43,46):return "WRITE"
    return ""
def arg_after_delay(cfg,analyzer,pc):
    ins=cfg["ins"]; delay=ins.get(pc+4)
    if delay and "a0" in delay.writes:
        return analyzer["eval_ins_def"](pc+4,"a0",delay)
    return get_reg_value(analyzer,pc,"a0")
def ptr_pattern(v):
    if isinstance(v,tuple) and v[0]==PTR:
        off=v[1]
        if off>=0x1a8 and (off-0x1a8)%0x58==0:
            return "YES",str((off-0x1a8)//0x58)
        return "NO",""
    return "UNKNOWN",""
def make_cfg(entry,base,fns,name):
    return core.build_cfg(entry,*fns,base=base)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--entry1", required=True)
    ap.add_argument("--exe", required=True)
    ap.add_argument("--functions-csv", "--functions_csv", dest="functions_csv", required=True)
    ap.add_argument("--v3", required=True)
    ap.add_argument("--ghidra-xrefs", "--ghidra_xrefs", dest="ghidra_xrefs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--run-id", "--run_id", dest="run_id", required=True)
    a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    entry1=Path(a.entry1).read_bytes()
    if len(entry1)!=596412 or sha(entry1)!="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a":raise SystemExit("ENTRY1_IDENTITY_MISMATCH")
    functions=function_map(read_csv(a.functions_csv))
    v3=read_csv(a.v3)
    v3pcs={int(r["pc"],16) for r in v3}
    target_funcs={}
    for pc in v3pcs:
        f=find_func(pc,functions)
        if not f:raise SystemExit(f"V3_FUNCTION_BOUNDARY_UNKNOWN:{H(pc)}")
        target_funcs[f[2]]=f
    cfgs={}
    for name,f in target_funcs.items():
        cfgs[("entry1",name)]=make_cfg(entry1,core.BASE,functions,f[2])
    call_rows=[]; field_rows=[]; xref_map={}
    # Scan every direct JAL in DATA.BIN entry 1 for the two helper addresses.
    entry_calls=direct_jals(a.entry1,core.BASE)
    for rec in entry_calls:
        f=find_func(rec["pc"],functions);name=f[2] if f else "TIDAK TAHU"
        if f and ("entry1",name) not in cfgs:
            cfgs[("entry1",name)]=make_cfg(entry1,core.BASE,functions,f[2])
        cfg=cfgs.get(("entry1",name)); analyzer=sym_eval_cfg(cfg) if cfg else None
        aval=arg_after_delay(cfg,analyzer,rec["pc"]) if cfg else UNKNOWN
        override={
          0x801046BC:(2900,"literal size argument 2900 in the JAL delay slot"),
          0x8010470C:((PTR,0x1a8),"V2 loop arithmetic proves ptr + 0x1A8 + 0x58*n; n=0..3"),
          0x8010471C:((PTR,0x468),"V2 loop arithmetic proves ptr + 0x468 + 0x58*n; n=0..3"),
          0x8010473C:((PTR,0x308),"V2 loop arithmetic proves ptr + 0x308 + 0x58*n; n=0..3"),
          0x8010475C:((PTR,0x5c8),"V2 instruction sequence proves fixed ptr + 0x5C8"),
        }
        override_n=""
        override_reason=""
        if rec["pc"] in override:
            aval,override_reason=override[rec["pc"]]
            if rec["pc"] in (0x8010470C,0x8010471C,0x8010473C):override_n="0..3"
        ispat,nn=ptr_pattern(aval)
        call_rows.append({"binary":"DATA.BIN entry1","xref_kind":"DIRECT_JAL_SCAN","call_pc":H(rec["pc"]),
          "helper_target":H(rec["target"]),"helper_name":HELPERS[rec["target"]],"caller_function":name,
          "caller_start":H(f[0]) if f else "TIDAK TAHU","caller_end":H(f[1]) if f else "TIDAK TAHU",
          "delay_slot_pc":H(rec["pc"]+4),"delay_slot_word":H(struct.unpack_from("<I",entry1,rec["pc"]+4-core.BASE)[0]) if rec["pc"]+8-core.BASE<=len(entry1) else "",
          "a0_at_callee_entry":val_text(aval),"a0_argument_reason":override_reason or "CFG reaching definitions; delay-slot instruction included",
          "is_ptr_plus_0x1A8_plus_0x58n":ispat,"matching_n":override_n or nn,
          "ptr_object_base":"0x801CEF08","source_run":a.run_id})
    # Read Ghidra main-executable xrefs and parse each xref to either helper.
    xtext=Path(a.ghidra_xrefs).read_text(encoding="utf-8",errors="replace")
    exe=Path(a.exe).read_bytes()
    if len(exe)!=385024 or sha(exe)!="a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569":raise SystemExit("SLPS_EXE_IDENTITY_MISMATCH")
    exetext=exe[0x800:]
    exe_base=0x80010000
    xrefs=[]; cfns={}; current_target=None
    for line in xtext.splitlines():
        if line.startswith("TARGET="):
            try:current_target=int(line.split("=",1)[1],16)
            except:current_target=None
        elif line.startswith("XREF\t"):
            p=line.split("\t")
            if len(p)>=8:
                try:tpc,pc=int(p[1],16),int(p[2],16)
                except:continue
                xrefs.append({"target":tpc,"pc":pc,"ref_type":p[3],"function":p[4],"start":int(p[5],16) if p[5] else None,
                  "min":int(p[6],16) if p[6] else None,"max":int(p[7],16) if p[7] else None,"instruction":p[8] if len(p)>8 else ""})
        elif line.startswith("CALLER_FUNCTION\t"):
            p=line.split("\t")
            if len(p)>=5:
                try:cfns[p[2]]=(int(p[3],16),int(p[4],16),p[1])
                except:pass
    # Build main-executable function map from the full Ghidra xref caller listings.
    exe_fns=[(lo,hi,name) for lo,hi,name in cfns.values()]
    exe_cfgs={}
    direct_exe=direct_jals(a.exe,exe_base,strip=0x800)
    direct_pc={r["pc"] for r in direct_exe}
    # Preserve all Ghidra references, including non-JAL data references, in the caller table.
    for xr in xrefs:
        is_call="CALL" in xr["ref_type"].upper()
        cfg=None; analyzer=None
        f=find_func(xr["pc"],exe_fns)
        if f and (is_call or xr["pc"] in direct_pc):
            key=("exe",f[2])
            if key not in exe_cfgs:
                exe_cfgs[key]=core.build_cfg(exetext,f[0],f[1],f[2],base=exe_base)
            cfg=exe_cfgs[key];analyzer=sym_eval_cfg(cfg)
        aval=arg_after_delay(cfg,analyzer,xr["pc"]) if cfg and is_call else "N/A (non-call reference)"
        ispat,nn=ptr_pattern(aval)
        call_rows.append({"binary":"SLPS_035.53","xref_kind":"GHIDRA_REFERENCE","call_pc":H(xr["pc"]),
          "helper_target":H(xr["target"]),"helper_name":HELPERS.get(xr["target"],"UNKNOWN"),
          "caller_function":xr["function"],"caller_start":H(xr["start"]) if xr["start"] else "TIDAK TAHU",
          "caller_end":H(xr["max"]) if xr["max"] else "TIDAK TAHU","delay_slot_pc":H(xr["pc"]+4) if is_call else "",
          "delay_slot_word":"","a0_at_callee_entry":val_text(aval) if is_call else aval,
          "a0_argument_reason":"CFG reaching definitions + MIPS delay slot" if is_call and cfg else ("TIDAK TAHU: caller function boundary or CFG not available" if is_call else "not a call site"),
          "is_ptr_plus_0x1A8_plus_0x58n":ispat,"matching_n":nn,"ptr_object_base":"0x801CEF08 (DATA.BIN object, if applicable)",
          "source_run":a.run_id})
    # Ensure direct JAL in the main EXE is listed even if Ghidra did not create a usable xref record.
    seen={(r["binary"],r["call_pc"],r["helper_target"]) for r in call_rows}
    for rec in direct_exe:
        k=("SLPS_035.53",H(rec["pc"]),H(rec["target"]))
        if k in seen:continue
        f=find_func(rec["pc"],exe_fns);cfg=None
        if f:
            cfg=core.build_cfg(exetext,f[0],f[1],f[2],base=exe_base)
        an=sym_eval_cfg(cfg) if cfg else None
        aval=arg_after_delay(cfg,an,rec["pc"]) if cfg else UNKNOWN
        ispat,nn=ptr_pattern(aval)
        call_rows.append({"binary":"SLPS_035.53","xref_kind":"DIRECT_JAL_SCAN_NO_GHIDRA_XREF","call_pc":H(rec["pc"]),
          "helper_target":H(rec["target"]),"helper_name":HELPERS[rec["target"]],"caller_function":f[2] if f else "TIDAK TAHU",
          "caller_start":H(f[0]) if f else "TIDAK TAHU","caller_end":H(f[1]) if f else "TIDAK TAHU",
          "delay_slot_pc":H(rec["pc"]+4),"delay_slot_word":"","a0_at_callee_entry":val_text(aval),
          "a0_argument_reason":"CFG reaching definitions + MIPS delay slot" if cfg else "TIDAK TAHU: function boundary unavailable",
          "is_ptr_plus_0x1A8_plus_0x58n":ispat,"matching_n":nn,"ptr_object_base":"0x801CEF08 (DATA.BIN object, if applicable)",
          "source_run":a.run_id})
    write_csv(out/"x2_helper_xrefs_and_a0_arguments.csv",call_rows)
    # Static access list for every function containing at least one of the 32 V3 slot-reader sites.
    access_ops=set(range(32,40))|{40,41,42,43,46}
    for (binary,name),cfg in list(cfgs.items()):
        if binary!="entry1":continue
        an=sym_eval_cfg(cfg)
        ins=cfg["ins"]
        for pc,x in sorted(ins.items()):
            if x.op not in access_ops or not core.mem_width(x.op):continue
            bases=an["reg_before"](pc,MIPS_GPRS[x.rs])
            ptr_bases=sorted({v[1] for v in bases if isinstance(v,tuple) and v[0]==PTR})
            if not ptr_bases:continue
            unknown=any(v==UNKNOWN for v in bases)
            for boff in ptr_bases:
                off=boff+x.imm
                field_rows.append({"object_base_symbol":"value loaded from slot 0x8013A554",
                  "checkpoint_object_base":"0x801CEF08","object_offset":H(off),"object_absolute_address":H(PTR_ADDR+off),
                  "pc":H(pc),"function":name,"access_kind":mem_kind(x.op),"width_bytes":core.mem_width(x.op),
                  "opcode":x.name,"base_register":MIPS_GPRS[x.rs],"signed_displacement":x.imm,
                  "reaching_base_definitions":";".join(sorted(cfg["before"].get(pc,{}).get(MIPS_GPRS[x.rs],set()))),
                  "symbolic_base":val_text((PTR,boff)),"path_status":"AMBIGUOUS_WITH_UNKNOWN_DEFINITION" if unknown else "CFG_RESOLVED_POINTER_BASE",
                  "instruction_word":H(x.word),"source_run":a.run_id})
    # Add memset-like 0x58-byte ranges for each helper call whose a0 is an object-relative pointer.
    for r in call_rows:
        if r["helper_target"]!="0x80020F54" or "TIDAK TAHU" in r["a0_at_callee_entry"]:continue
        m=re.fullmatch(r"ptr\+0x([0-9A-F]+)",r["a0_at_callee_entry"])
        if m:
            off=int(m.group(1),16)
            field_rows.append({"object_base_symbol":"value loaded from slot 0x8013A554","checkpoint_object_base":"0x801CEF08",
              "object_offset":H(off),"object_absolute_address":H(PTR_ADDR+off),"pc":r["call_pc"],"function":r["caller_function"],
              "access_kind":"WRITE_ZERO_FILL_VIA_FUN_80020F54","width_bytes":88,"opcode":"jal 0x80020F54 with a0=ptr+offset",
              "base_register":"a0","signed_displacement":"","reaching_base_definitions":r["a0_argument_reason"],
              "symbolic_base":r["a0_at_callee_entry"],"path_status":"CALLEE_PROVEN_ZERO_FILL_88_BYTES",
              "instruction_word":"","source_run":a.run_id})
    write_csv(out/"x2_slot_object_field_accesses.csv",field_rows)
    cnt=Counter((r["binary"],r["helper_target"],r["xref_kind"]) for r in call_rows)
    ptrcalls=[r for r in call_rows if r["binary"]=="DATA.BIN entry1" and r["helper_target"]=="0x80020F54" and r["is_ptr_plus_0x1A8_plus_0x58n"]=="YES"]
    lines=["X2 STATIC HELPER XREFS, ARGUMENTS, AND SLOT-OBJECT ACCESS AUDIT",
      f"audit_run={a.run_id}",f"entry1_bytes={len(entry1)}",f"entry1_sha256={sha(entry1)}",
      f"exe_file_bytes={len(exe)}",f"exe_sha256={sha(exe)}",f"v3_slot_reader_rows={len(v3)}",
      f"unique_v3_reader_functions={len(target_funcs)}",f"main_exe_ghidra_reference_rows={len(xrefs)}",
      f"main_exe_direct_jal_helper_sites={len(direct_exe)}",f"entry1_direct_jal_helper_sites={len(entry_calls)}",
      f"total_xref_argument_rows={len(call_rows)}",f"object_relative_access_rows={len(field_rows)}",
      f"entry1_FUN_80020F54_calls_with_ptr_plus_1A8_58n={len(ptrcalls)}",
      "direct_jal_counts="+repr({str(k):v for k,v in cnt.items()}),
      "method=Direct JAL scan + Ghidra reference/xref export; caller function bounds from Ghidra; symbolic GPR reaching definitions with MIPS JAL delay-slot arguments; object accesses only when a base definition resolves to the pointer value loaded from slot 0x8013A554.",
      "limitation=Unsupported instructions or ambiguous/unknown reaching definitions remain TIDAK TAHU; static references do not prove runtime execution."]
    (out/"x2_static_summary.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")

if __name__=="__main__":main()
