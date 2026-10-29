#!/usr/bin/env python3
"""Read-only comparison of checkpoint RAM against entry 1 and strict A2 XREFs."""
from __future__ import annotations
import argparse,csv,hashlib,json,math,struct,sys
from pathlib import Path

DATA_SHA="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
ENTRY_SHA="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
RAM_SHA="3ad7b85c857a868d91df4b3f1049c23889a0dc482ad7ee390ac8b6c05c3190f4"
DATA_OFFSET=0x10BB000
ENTRY_SIZE=596412
BLOCK_SIZE=4096
RAM_BASE=0x80000000
BASES=(0x800AD450,0x800AD000,0x800AC450,0x800AE450)
TARGET=0x8013A554

def sha(b): return hashlib.sha256(b).hexdigest()
def readcsv(p):
    with Path(p).open(newline="",encoding="utf-8-sig") as f: return list(csv.DictReader(f))
def writecsv(p,rows):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",newline="",encoding="utf-8") as f:
        fields=list(rows[0]) if rows else ["empty"]
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(rows)
def hnum(v): return int(v,16) if isinstance(v,str) and v.lower().startswith("0x") else int(v)

def fn_overlap(funcs,start,n):
    end=start+n; names=[]
    for f in funcs:
        try: fs,fe=hnum(f["start_address"]),hnum(f["end_address"])
        except (KeyError,ValueError,TypeError): continue
        if fs<end and fe+4>start: names.append(f.get("function_name","FUNCTION"))
    return names

def do_ram(entry,ram,funcs_path,out):
    if len(ram)!=0x200000: raise SystemExit(f"RAM_SIZE_MISMATCH={len(ram)}")
    rh=sha(ram)
    if rh!=RAM_SHA: raise SystemExit(f"RAM_SHA_MISMATCH expected={RAM_SHA} actual={rh}; refusing comparison")
    funcs=readcsv(funcs_path)
    blocks=math.ceil(len(entry)/BLOCK_SIZE); last=len(entry)-(blocks-1)*BLOCK_SIZE
    rows=[]; summaries=[]
    for base in BASES:
        off0=base-RAM_BASE
        region=ram[off0:off0+len(entry)]
        if len(region)!=len(entry): raise SystemExit(f"RAM_RANGE_INVALID base={base:#x}")
        same=0; diffblocks=0; diffbytes=0
        for idx in range(blocks):
            off=idx*BLOCK_SIZE; n=min(BLOCK_SIZE,len(entry)-off)
            a=entry[off:off+n]; b=region[off:off+n]
            ds=[k for k,(x,y) in enumerate(zip(a,b)) if x!=y]
            equal=not ds; same+=int(equal); diffblocks+=int(not equal); diffbytes+=len(ds)
            va=base+off; fns=fn_overlap(funcs,va,n)
            rows.append({
              "base":f"0x{base:08X}","block_index":idx,
              "entry_relative_offset":f"0x{off:06X}","virtual_start":f"0x{va:08X}",
              "ram_dump_offset":f"0x{off0+off:06X}","bytes_compared":n,
              "status":"IDENTICAL" if equal else "DIFFERENT","different_byte_count":len(ds),
              "first_difference_entry_offset":f"0x{off+ds[0]:06X}" if ds else "",
              "first_difference_virtual_address":f"0x{va+ds[0]:08X}" if ds else "",
              "last_difference_entry_offset":f"0x{off+ds[-1]:06X}" if ds else "",
              "overlaps_recognized_function":str(bool(fns)).lower(),
              "function_names":";".join(fns),
              "data_bss_assessment":"Ghidra-recognized code/function overlap" if fns else
                "non-function region; initialized DATA vs BSS cannot be distinguished from raw entry"
            })
        pct=100*same/blocks
        summaries.append({
          "base":f"0x{base:08X}","RAM_entry_start_offset":f"0x{off0:06X}",
          "entry_bytes":len(entry),"block_size":BLOCK_SIZE,"total_blocks_including_partial":blocks,
          "last_block_bytes":last,"identical_blocks":same,"different_blocks":diffblocks,
          "identical_percent":f"{pct:.6f}","different_bytes_total":diffbytes,
          "meets_95_percent":str(pct>=95).lower(),"ram_sha256":rh,"entry1_sha256":sha(entry)
        })
    writecsv(out/"t2_ram_block_comparison.csv",rows)
    writecsv(out/"t2_ram_block_summary.csv",summaries)
    roff=TARGET-RAM_BASE; raw=ram[roff:roff+4]; val=struct.unpack("<I",raw)[0]
    (out/"t2_ram_target_value.txt").write_text(
      f"ram_dump_sha256={rh}\naddress=0x{TARGET:08X}\ndump_offset=0x{roff:06X}\nbytes_le={raw.hex(' ').upper()}\nu32_le=0x{val:08X}\nu32_le_decimal={val}\n",
      encoding="utf-8")
    return summaries,raw,val

def do_strict_a2(entry,baseline_path,xref_path,out):
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    import step4_10_static_evidence_audit as strict
    rows=strict.a2_scan(entry,"DATA.BIN entry1",0x800AD450,"base_0x800AD450_A1_PASS")
    if len(rows)!=137: raise SystemExit(f"STRICT_SCAN_EXPECTED_137_GOT_{len(rows)}")
    writecsv(out/"t3_strict_scan_recomputed.csv",rows)
    offsets={}
    for r in rows: offsets.setdefault(int(r["file_offset"],16),[]).append(r)
    baseline=readcsv(baseline_path)
    baseoffs={int(r["file_offset"],16) for r in baseline if r.get("scenario")=="base_0x800AD450_A1_PASS"}
    if set(offsets)!=baseoffs: raise SystemExit("STRICT_SCAN_DIFFERS_FROM_STORED_137_HIT_BASELINE")
    gx=readcsv(xref_path)
    if len(gx)!=324: raise SystemExit(f"GHIDRA_XREF_EXPECTED_324_GOT_{len(gx)}")
    g={}
    for r in gx: g.setdefault(int(r["entry1_file_offset"],16),[]).append(r)
    ss=set(offsets); gg=set(g); common=ss&gg; so=ss-gg; go=gg-ss
    merged=[]
    for off in sorted(ss|gg):
        sr=offsets.get(off,[]); gr=g.get(off,[])
        typ="SAMA" if sr and gr else "SCAN_ONLY" if sr else "GHIDRA_ONLY"
        merged.append({
          "entry_relative_offset":f"0x{off:06X}","virtual_address_base_800AD450":f"0x{0x800AD450+off:08X}",
          "classification":typ,"strict_scan_hits":len(sr),"strict_kind":";".join(x["kind"] for x in sr),
          "strict_instruction":";".join(x["instruction"] for x in sr),
          "ghidra_xref_hits":len(gr),"ghidra_types":";".join(x["reference_type"] for x in gr),
          "ghidra_instruction":";".join(x["instruction_mnemonic"] for x in gr),
          "ghidra_functions":";".join(x["containing_function"] for x in gr)
        })
    writecsv(out/"t3_strict_vs_new_ghidra_reconciliation.csv",merged)
    summary=[
      {"metric":"strict_scan_rows","count":len(rows),"criterion":"exact strict scan implementation; expected 137"},
      {"metric":"strict_scan_unique_offsets","count":len(ss),"criterion":"unique entry-relative source offsets"},
      {"metric":"new_ghidra_xref_rows","count":len(gx),"criterion":"rebased Ghidra XREF export"},
      {"metric":"new_ghidra_unique_offsets","count":len(gg),"criterion":"unique entry-relative source offsets"},
      {"metric":"same","count":len(common),"criterion":"source offset appears in both"},
      {"metric":"scan_only","count":len(so),"criterion":"source offset appears only in strict scan"},
      {"metric":"ghidra_only","count":len(go),"criterion":"pass criterion requires <57.5"},
      {"metric":"criterion_ghidra_only_lt_57_5","count":str(len(go)<57.5).lower(),"criterion":"PASS iff Ghidra-only <57.5"}
    ]
    writecsv(out/"t3_strict_vs_new_ghidra_summary.csv",summary)
    return {"strict_rows":len(rows),"strict_unique_offsets":len(ss),"ghidra_rows":len(gx),
      "ghidra_unique_offsets":len(gg),"same":len(common),"scan_only":len(so),"ghidra_only":len(go),
      "criterion_pass":len(go)<57.5}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data-bin",required=True);p.add_argument("--ram-dump",required=True)
    p.add_argument("--functions-csv",required=True);p.add_argument("--strict-baseline-csv",required=True)
    p.add_argument("--ghidra-xrefs-csv",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    data=Path(a.data_bin).read_bytes()
    if len(data)!=66015232 or sha(data)!=DATA_SHA: raise SystemExit(f"DATA_BIN_IDENTITY_FAILURE bytes={len(data)} sha={sha(data)}")
    entry=data[DATA_OFFSET:DATA_OFFSET+ENTRY_SIZE]
    if len(entry)!=ENTRY_SIZE or sha(entry)!=ENTRY_SHA: raise SystemExit(f"ENTRY1_IDENTITY_FAILURE bytes={len(entry)} sha={sha(entry)}")
    ram=Path(a.ram_dump).read_bytes()
    sums,raw,val=do_ram(entry,ram,Path(a.functions_csv),out)
    a2=do_strict_a2(entry,Path(a.strict_baseline_csv),Path(a.ghidra_xrefs_csv),out)
    log=[
      "Read-only analysis. No emulator launch, gameplay input, or savestate restore.",
      f"DATA_BIN_BYTES={len(data)} DATA_BIN_SHA256={sha(data)}",
      f"ENTRY1_OFFSET=0x{DATA_OFFSET:X} ENTRY1_BYTES={len(entry)} ENTRY1_SHA256={sha(entry)}",
      f"RAM_DUMP_BYTES={len(ram)} RAM_DUMP_SHA256={sha(ram)} EXPECTED_RAM_SHA256={RAM_SHA}",
      f"T2_SUMMARIES={json.dumps(sums,sort_keys=True)}",
      f"T2_TARGET=0x{TARGET:08X} BYTES={raw.hex()} U32_LE=0x{val:08X} DECIMAL={val}",
      f"T3_STRICT_VS_GHIDRA={json.dumps(a2,sort_keys=True)}",
      "BSS_NOTE=raw DATA.BIN entry has no segment/BSS allocation metadata; non-function regions cannot be distinguished authoritatively as initialized DATA vs BSS."
    ]
    (out/"t2_t3_checkpoint-audit.txt").write_text("\n".join(log)+"\n",encoding="utf-8")
    (out/"t2_t3_checkpoint-audit.json").write_text(json.dumps({"data_sha256":sha(data),"entry1_sha256":sha(entry),"ram_sha256":sha(ram),"ram_comparison":sums,"target_u32":val,"a2":a2},indent=2)+"\n",encoding="utf-8")
    print("\n".join(log))

if __name__=="__main__": main()
