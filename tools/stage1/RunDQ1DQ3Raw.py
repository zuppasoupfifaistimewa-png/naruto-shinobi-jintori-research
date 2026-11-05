#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, os, struct, subprocess, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

EXE_PATH, DATA_PATH, OUT = map(Path, sys.argv[1:4])
BASELINE=os.environ.get("DQ0_BASELINE","2136f3df739937b87a790844bca59e8a837d3484")
AUDIT_HEAD=os.environ.get("DQ0_AUDIT_HEAD",BASELINE)
GLOBAL=0x80139EFC
ENTRY1_BASE=0x800AD450
EXE_BASE=0x80010000
CHAKRA_BASE=0x80070EA0
CHAKRA_STRIDE=0xB4
CHAKRA_OFF=0x18
PENDING_STORE=0x800ECBB8
HELPER=0x800EC574
JAL_GUESS=0x0C03B15D
EXE_SHA="a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
DATA_SHA="69df081aaeb5dd0cff13a177693f6ef6d62aa2b36417c63f031ec7ee4de51822"
ENTRY_SHA="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def tsv(path,cols,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,delimiter="\t",extrasaction="ignore")
        w.writeheader()
        for r in rows: w.writerow(r)
def git(args): return subprocess.check_output(["git",*args],text=True).strip()
def dq0():
    commits=git(["rev-list","--reverse",f"{BASELINE}^..{AUDIT_HEAD}"]).splitlines()
    rows=[]; humans=bots=0
    for c in commits:
        h=git(["show","-s","--format=%H%x09%an%x09%ae%x09%s",c]).split("\t",3)
        sh,author,email,msg=h
        bot=("github-actions" in author.lower() or "[bot]" in author.lower() or "41898282+github-actions" in email.lower())
        bots+=int(bot); humans+=int(not bot)
        files=git(["diff-tree","--root","--no-commit-id","--name-only","-r",c]).splitlines()
        rows.append({"sha_full":sh,"author_class":"BOT" if bot else "MANUSIA","author_name":author,
                     "author_email":email,"message":msg,"changed_files":";".join(files)})
    tsv(OUT/"DQ0_COMMIT_LEDGER.tsv",["sha_full","author_class","author_name","author_email","message","changed_files"],rows)
    (OUT/"DQ0_SUMMARY.txt").write_text(
        f"STATUS={'TUNTAS' if commits else 'BELUM'}\nK=K4\nBASELINE_INCLUSIVE={BASELINE}\nAUDIT_HEAD_SNAPSHOT={AUDIT_HEAD}\nTOTAL={len(rows)}\nMANUSIA={humans}\nBOT={bots}\nNOTE=Snapshot main saat audit dimulai; commit workflow dan commit publikasi yang dibuat sesudah snapshot tidak termasuk.\n",encoding="utf-8")

def entry1_from_databin(b):
    if len(b)!=66015232 or hashlib.sha256(b).hexdigest()!=DATA_SHA: raise ValueError("DATA_BIN_IDENTITY_MISMATCH")
    lbn,n=struct.unpack_from("<II",b,0x44+8)
    off=(lbn-212)*2048
    x=b[off:off+n]
    if (lbn,n,off,len(x),hashlib.sha256(x).hexdigest())!=(8778,596412,0x10BB000,596412,ENTRY_SHA):
        raise ValueError("ENTRY1_DIRECTORY_MAPPING_MISMATCH")
    return x

if len(EXE_PATH.read_bytes())!=385024 or sha(EXE_PATH)!=EXE_SHA: raise ValueError("EXE_IDENTITY_MISMATCH")
exe=EXE_PATH.read_bytes()
if len(exe)<0x800: raise ValueError("EXE_HEADER_MISSING")
databin=DATA_PATH.read_bytes()
entry1=entry1_from_databin(databin)

(OUT/"INPUT_RAW_IDENTITY.txt").write_text(
    "STATUS=PASS\nSOURCE=raw BIN/CUE -> ISO -> extracted SLPS_035.53 and DATA.BIN\n"
    f"EXE_BYTES={len(exe)}\nEXE_SHA256={EXE_SHA}\nEXE_PC_BASE=0x{EXE_BASE:08X}\n"
    "EXE_FILE_OFFSET=0x800+(PC-0x80010000)\n"
    f"DATA_BIN_BYTES={len(databin)}\nDATA_BIN_SHA256={DATA_SHA}\nENTRY1_INDEX=1\nENTRY1_LBN=8778\n"
    "ENTRY1_DATA_BIN_OFFSET=0x10BB000\nENTRY1_BYTES=596412\n"
    f"ENTRY1_SHA256={ENTRY_SHA}\nENTRY1_STATIC_BASE=0x{ENTRY1_BASE:08X}\n"
    "ENTRY1_SLICE_OFFSET=PC-0x800AD450\nRUNTIME_MAPPING=NOT_VALIDATED\nBINARY_OUTPUT=NO\n",encoding="utf-8")

md=Cs(CS_ARCH_MIPS,CS_MODE_MIPS32|CS_MODE_LITTLE_ENDIAN)
def build(name,raw,base,filebase):
    a=[]
    for off in range(0,len(raw)-3,4):
        b=raw[off:off+4]; pc=base+off; w=int.from_bytes(b,"little")
        ins=next(md.disasm(b,pc,count=1),None)
        text=(ins.mnemonic+(" "+ins.op_str if ins and ins.op_str else "")) if ins else f".word 0x{w:08X}"
        a.append({"module":name,"pc":pc,"off":off,"file_off":filebase+off,"bytes":b,"word":w,
            "op":w>>26,"rs":(w>>21)&31,"rt":(w>>16)&31,"rd":(w>>11)&31,"sh":(w>>6)&31,
            "fn":w&63,"imm":((w&65535)^32768)-32768,"target":w&0x03ffffff,"text":text})
    return a
def hx(b): return " ".join(f"{x:02X}" for x in b)
regs=["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
def rn(r): return regs[r]
regions=[("MAIN_EXE",exe[0x800:],EXE_BASE,0x800),("ENTRY1",entry1,ENTRY1_BASE,0)]
by={n:build(n,r,b,f) for n,r,b,f in regions}
allins=[i for n in by for i in by[n]]
pcmap={i["pc"]:i for i in allins}

# Approximate function boundaries from raw direct-JAL destinations and stack-allocation prologues.
starts={n:set() for n in by}
for i in allins:
    if i["op"]==3:
        tgt=((i["pc"]+4)&0xF0000000)|(i["target"]<<2)
        if tgt in pcmap: starts[i["module"]].add(tgt)
    if i["op"]==9 and i["rs"]==29 and i["rt"]==29 and i["imm"]<0: starts[i["module"]].add(i["pc"])
for n,a in by.items():
    if a: starts[n].add(a[0]["pc"])
def func(module,pc):
    cand=[x for x in starts[module] if x<=pc]
    if not cand: return ("TIDAK_TAHU","TIDAK_TAHU")
    ent=max(cand)
    if 0x800EC574<=pc<=0x800ECBB8 and module=="ENTRY1": return ("FUN_800ec574","0x800EC574 (known target)")
    return (f"FUN_{ent:08x}",f"0x{ent:08X} (nearest raw JAL/prologue heuristic)")
def prior(module,pc,n=12):
    a=by[module]; k=next((j for j,x in enumerate(a) if x["pc"]==pc),None)
    if k is None or k<n: return ("TIDAK_TAHU","")
    p=a[k-n:k]
    return (" || ".join(f"0x{x['pc']:08X} {x['text']}" for x in p),hx(b"".join(x["bytes"] for x in p)))
def instrow(i):
    f,e=func(i["module"],i["pc"]); p,ph=prior(i["module"],i["pc"])
    return {"module":i["module"],"pc":f"0x{i['pc']:08X}","file_offset":f"0x{i['file_off']:X}",
        "function":f,"function_entry":e,"hex":hx(i["bytes"]),"mnemonic":i["text"],
        "previous_12":p,"previous_12_hex_excerpt_le_max_64":ph}

# DQ1(a): exact twelve aligned words before the store, read from verified raw Entry 1.
if not (ENTRY1_BASE<=PENDING_STORE<ENTRY1_BASE+len(entry1)): raise ValueError("PENDING_STORE_OUTSIDE_ENTRY1_MAPPING")
ti=(PENDING_STORE-ENTRY1_BASE)//4
pre=[]
for i in by["ENTRY1"][ti-12:ti]:
    r=instrow(i); r["target_store_pc"]="0x800ECBB8"; pre.append(r)
ts=instrow(by["ENTRY1"][ti])
tsrow={"pc":f"0x{PENDING_STORE:08X}","mnemonic":ts["mnemonic"],"hex":ts["hex"]}
tsv(OUT/"DQ1A_PRESTORE_12_RAW.tsv",
    ["module","pc","file_offset","function","function_entry","hex","mnemonic","previous_12","previous_12_hex_excerpt_le_max_64","target_store_pc"],pre)
(OUT/"DQ1A_MAPPING_CHECK.txt").write_text(
    "STATUS=PASS\nTARGET_STORE_PC=0x800ECBB8\nEXE_MAPPING=OUT_OF_RANGE\n"
    f"ENTRY1_BASE=0x{ENTRY1_BASE:08X}\nENTRY1_SLICE_OFFSET=0x{PENDING_STORE-ENTRY1_BASE:X}\n"
    f"DATA_BIN_ABSOLUTE_OFFSET=0x{0x10BB000+PENDING_STORE-ENTRY1_BASE:X}\n"
    "RAW_PRESTORE_INSTRUCTION_COUNT=12\nRAW_PRESTORE_BYTES=48\nMAX_EXCERPT_BYTES=64\n"
    f"STORE_WORD={tsrow['hex']}\nSTORE_MNEMONIC={tsrow['mnemonic']}\n",encoding="utf-8")

# Conservative raw register constant/origin propagation across aligned instructions.
def V(k="unknown",v=None,o=""): return {"kind":k,"value":v,"origin":o}
def C(x): return V("const",x&0xffffffff,"CONST")
def cv(x): return x["value"] if x and x["kind"]=="const" else None
def orgmerge(*vs):
    z=[v.get("origin","") for v in vs if v]
    if any("CHAKRA" in x for x in z): return "COMPUTED_FROM_CHAKRA"
    if any("TILE_1A" in x for x in z): return "COMPUTED_FROM_TILE_1A"
    return "COMPUTED"
writers=[]; accesses=[]; chakra_reads=[]; chakra_sub=[]
for module,a in by.items():
    st={0:C(0)}; hilo=V()
    for i in a:
        op,rs,rt,rd,sh,fn,imm=(i[k] for k in ("op","rs","rt","rd","sh","fn","imm"))
        bv=st.get(rs,V()); base=cv(bv); eff=((base+imm)&0xffffffff) if base is not None else None
        # Reads from the global manager pointer slot create a manager-pointer alias.
        if op in (0x20,0x21,0x23,0x24,0x25):
            width={0x20:1,0x21:2,0x23:4,0x24:1,0x25:2}[op]
            if eff==GLOBAL:
                st[rt]=V("manager_ptr",None,"MANAGER_POINTER_FROM_0x80139EFC")
            elif imm==0x2EE:
                state="MANAGER_ALIAS_CONFIRMED" if bv.get("kind")=="manager_ptr" else "BASE_UNPROVEN"
                accesses.append({"module":module,"pc":f"0x{i['pc']:08X}","access":"READ","width":width,
                    "base_register":rn(rs),"base_origin":bv.get("origin","UNKNOWN"),"status":state,
                    "function":func(module,i["pc"])[0],"hex":hx(i["bytes"]),"mnemonic":i["text"]})
                st[rt]=V("loaded",None,"MANAGER_2EE_READ" if state=="MANAGER_ALIAS_CONFIRMED" else "UNKNOWN_2EE_LOAD")
            elif eff is not None and any(eff==CHAKRA_BASE+s*CHAKRA_STRIDE+CHAKRA_OFF for s in range(4)):
                slot=(eff-CHAKRA_BASE-CHAKRA_OFF)//CHAKRA_STRIDE
                chakra_reads.append({"module":module,"pc":f"0x{i['pc']:08X}","slot":slot,
                    "function":func(module,i["pc"])[0],"hex":hx(i["bytes"]),"mnemonic":i["text"]})
                st[rt]=V("loaded",None,"CHAKRA")
            elif op in (0x21,0x25) and imm==0x1A:
                st[rt]=V("loaded",None,"TILE_1A")
            else: st[rt]=V("loaded",None,f"LOAD_{imm:+#x}")
        elif op in (0x28,0x29,0x2B):
            width={0x28:1,0x29:2,0x2B:4}[op]
            if eff==GLOBAL:
                src=st.get(rt,V())
                label="CLEAR" if rt==0 else ("DARI_TILE_1A" if "TILE_1A" in src.get("origin","") else
                    ("COMPUTED" if "COMPUTED" in src.get("origin","") else "LAIN"))
                p,ph=prior(module,i["pc"]); f,e=func(module,i["pc"])
                writers.append({"module":module,"pc":f"0x{i['pc']:08X}","file_offset":f"0x{i['file_off']:X}",
                    "function":f,"function_entry":e,"label":label,"width":width,"instruction":i["text"],
                    "source_register":rn(rt),"source_origin":src.get("origin","UNKNOWN"),
                    "hex":hx(i["bytes"]),"previous_12":p,"previous_12_hex_excerpt_le_max_64":ph})
            if imm==0x2EE:
                state="MANAGER_ALIAS_CONFIRMED" if bv.get("kind")=="manager_ptr" else "BASE_UNPROVEN"
                accesses.append({"module":module,"pc":f"0x{i['pc']:08X}","access":"WRITE","width":width,
                    "base_register":rn(rs),"base_origin":bv.get("origin","UNKNOWN"),"status":state,
                    "function":func(module,i["pc"])[0],"hex":hx(i["bytes"]),"mnemonic":i["text"]})
        # Known integer constant construction.
        if op==0x0F: st[rt]=C((i["word"]&65535)<<16)
        elif op in (0x08,0x09,0x0C,0x0D,0x0E):
            src=st.get(rs,V())
            if cv(src) is not None:
                v=cv(src)
                x=(v+imm)&0xffffffff if op in (0x08,0x09) else (v|(i["word"]&65535) if op==0x0D else (v&(i["word"]&65535) if op==0x0C else v^(i["word"]&65535)))
                st[rt]=C(x)
            else: st[rt]=V("derived",None,orgmerge(src))
        elif op==0 and fn in (0x00,0x02,0x03,0x21,0x23,0x24,0x25,0x26,0x27):
            x,y=st.get(rs,V()),st.get(rt,V())
            if fn==0x00 and cv(y) is not None: st[rd]=C(cv(y)<<sh)
            elif fn in (0x02,0x03) and cv(y) is not None: st[rd]=C(cv(y)>>sh)
            elif cv(x) is not None and cv(y) is not None:
                a1,b1=cv(x),cv(y)
                z={0x21:a1+b1,0x23:a1-b1,0x24:a1&b1,0x25:a1|b1,0x26:a1^b1,0x27:~(a1|b1)}[fn]
                st[rd]=C(z)
            else:
                o=orgmerge(x,y); st[rd]=V("derived",None,o)
                if fn==0x23 and ("CHAKRA" in o or "MANAGER_2EE_READ" in o):
                    chakra_sub.append({"module":module,"pc":f"0x{i['pc']:08X}","function":func(module,i["pc"])[0],
                        "instruction":i["text"],"origin":o,"hex":hx(i["bytes"])})
        elif op==0 and fn in (0x18,0x19): hilo=V("derived",None,orgmerge(st.get(rs,V()),st.get(rt,V())))
        elif op==0 and fn in (0x10,0x12): st[rd]=V("derived",None,hilo.get("origin","COMPUTED"))
        elif op==3:
            st[31]=V("derived",None,"CALL_RETURN")
            for rr in (2,3,4,5,6,7,8,9,10,11,12,13,14,15,24,25): st[rr]=V()

# DQ1(b): one row per raw store to the exact effective address.
tsv(OUT/"DQ1B_GLOBAL_80139EFC_WRITERS_RAW.tsv",
 ["module","pc","file_offset","function","function_entry","label","width","instruction","source_register",
  "source_origin","hex","previous_12","previous_12_hex_excerpt_le_max_64"],writers)
counts={x:sum(w["label"]==x for w in writers) for x in ("DARI_TILE_1A","COMPUTED","CLEAR","LAIN")}
(OUT/"DQ1B_GLOBAL_WRITER_CENSUS.txt").write_text(
 f"STATUS={'TUNTAS' if writers else 'BELUM'}\nTARGET=0x80139EFC\nCONFIRMED_RAW_STORE_CANDIDATES={len(writers)}\n"+
 "".join(f"{k}={v}\n" for k,v in counts.items())+
 "METHOD=aligned raw MIPS words in verified MAIN_EXE text mapping and Entry 1 slice; direct and propagated register constants including GP if initialized.\n"+
 "LIMIT=indirect/dynamic aliases and code-data distinction in Entry 1 are not fully resolved; zero candidates is not proof of no writer.\n",encoding="utf-8")

# DQ2: verify JAL target decoding and enumerate all direct callsites.
callers=[]
for i in allins:
    if i["op"]==3:
        tgt=((i["pc"]+4)&0xF0000000)|(i["target"]<<2)
        if tgt==HELPER:
            f,e=func(i["module"],i["pc"]); p,ph=prior(i["module"],i["pc"])
            callers.append({"module":i["module"],"pc":f"0x{i['pc']:08X}","word":f"0x{i['word']:08X}",
                "decoded_target":f"0x{tgt:08X}","opcode_guess_match":"YES" if i["word"]==JAL_GUESS else "NO",
                "function":f,"function_entry":e,"instruction":i["text"],"hex":hx(i["bytes"]),
                "previous_12":p,"previous_12_hex_excerpt_le_max_64":ph})
tsv(OUT/"DQ2_FUN_800EC574_DIRECT_CALLERS_RAW.tsv",
 ["module","pc","word","decoded_target","opcode_guess_match","function","function_entry","instruction","hex","previous_12","previous_12_hex_excerpt_le_max_64"],callers)
tsv(OUT/"DQ2_MANAGER_2EE_READ_WRITE_RAW.tsv",
 ["module","pc","access","width","base_register","base_origin","status","function","hex","mnemonic"],accesses)
tsv(OUT/"DQ2_CHAKRA_READS_RAW.tsv",["module","pc","slot","function","hex","mnemonic"],chakra_reads)
tsv(OUT/"DQ2_CHAKRA_SUBTRACTIONS_RAW.tsv",["module","pc","function","instruction","origin","hex"],chakra_sub)
idxrows=[]
for i in by["ENTRY1"]:
    if 0x800EC574<=i["pc"]<=0x800ECBB8 and i["op"]==0 and i["fn"]==0 and i["sh"]==1:
        idxrows.append({"pc":f"0x{i['pc']:08X}","function":"FUN_800ec574 (known target)",
            "instruction":i["text"],"hex":hx(i["bytes"]),
            "note":"sll by 1 is consistent with 2-byte index scaling; origin of idx is not independently proven here."})
tsv(OUT/"DQ2_INDEX_TIMES_TWO_RAW.tsv",["pc","function","instruction","hex","note"],idxrows)
window=[]
for pc in range(0x800ECB88,0x800ECBB8,4):
    i=pcmap.get(pc)
    if i: window.append({"pc":f"0x{pc:08X}","file_offset":f"0x{0x10BB000+pc-ENTRY1_BASE:X}",
        "word":f"0x{i['word']:08X}","instruction":i["text"],"hex":hx(i["bytes"]),"function":"FUN_800ec574"})
tsv(OUT/"DQ2_FUN_800EC574_RAW_WINDOW.tsv",["pc","file_offset","word","instruction","hex","function"],window)

q3rows=[{"module":w["module"],"pc":w["pc"],"function":w["function"],"label":w["label"],
         "instruction":w["instruction"],"previous_12":w["previous_12"],
         "excerpt_hex_le_max_64":w["previous_12_hex_excerpt_le_max_64"]} for w in writers]
tsv(OUT/"DQ3_GLOBAL_FILL_PRECONTEXT_RAW.tsv",["module","pc","function","label","instruction","previous_12","excerpt_hex_le_max_64"],q3rows)
obs=[("LV1->LV2",1,100),("LV1->LV3",2,400),("LV1->LV4",3,800),("LV1->LV5",4,1600)]
pred=[{"transition":n,"d":d,"fee_base_X120":100,"observed_user_hypothesis":v,
       "fee_times_2_pow_d_prediction":100*(2**d),"match":"COCOK" if 100*(2**d)==v else "TIDAK_COCOK"} for n,d,v in obs]
tsv(OUT/"DQ3_USER_OBSERVATION_FORMULA_CHECK.tsv",
 ["transition","d","fee_base_X120","observed_user_hypothesis","fee_times_2_pow_d_prediction","match"],pred)

mdlines=[
"# DQ1-DQ3 — audit raw-byte statik","",
f"Snapshot HEAD main saat mulai: {AUDIT_HEAD}. Baseline inklusif: {BASELINE}.",
"Metode: raw disc BIN/CUE -> ISO -> SLPS_035.53 dan DATA.BIN sementara pada runner; validasi SHA; parser MIPS raw little-endian membaca langsung byte EXE dan Entry 1. Ghidra export tidak dipakai sebagai sumber byte.",
"Biner sementara dibuang sebelum hasil teks di-commit; tidak ada artifact biner.",
"",
"## Status",
"",
"- DQ0: TUNTAS K4 — lihat DQ0_SUMMARY.txt dan DQ0_COMMIT_LEDGER.tsv.",
"- DQ1(a): TUNTAS K4 — 12 instruksi sebelum store 0x800ECBB8 dipetakan ke Entry 1 dan dibaca langsung dari byte mentah.",
f"- DQ1(b): {'TUNTAS K3' if writers else 'BELUM K2'} — {len(writers)} store kandidat terdeteksi; recount kategori di bawah.",
f"- DQ2: {'TUNTAS K4' if callers else 'BELUM K2'} untuk JAL langsung, pemanggil={len(callers)}; manager+0x2EE akses={len(accesses)}; direct Chakra reads={len(chakra_reads)}; Chakra-tainted subu={len(chakra_sub)}.",
"- DQ3: BELUM K2 — raw scan belum membuktikan level saat ini vs target -> fee -> pengisian 0x80139EFC.",
"",
"## DQ1(a) — instruksi sebelum store",
"",
"PC 0x800ECBB8 di luar EXE. Entry 1 diverifikasi sendiri: directory index 1, LBN 8778, DATA.BIN byte offset 0x10BB000, size 596412, SHA256 "+ENTRY_SHA+". Kandidat base statik 0x800AD450 menghasilkan slice offset "+hex(PENDING_STORE-ENTRY1_BASE)+". Runtime mapping tetap NOT VALIDATED.",
"Rincian 12 baris PC/word/mnemonik/hex dan window 48 byte ada di DQ1A_PRESTORE_12_RAW.tsv; instruksi store target serta offset diverifikasi di DQ1A_MAPPING_CHECK.txt.",
"",
"## DQ1(b) — census writer global 0x80139EFC",
"",
f"Recount TSV: total={len(writers)}, DARI_TILE_1A={counts['DARI_TILE_1A']}, COMPUTED={counts['COMPUTED']}, CLEAR={counts['CLEAR']}, LAIN={counts['LAIN']}.",
"DARI_TILE_1A = register sumber terakhir berasal dari lhu offset 0x1A; COMPUTED = operasi aritmetika/logika ditandai di aliran register; CLEAR = zero; LAIN = asal tidak terbukti. Ini klasifikasi aliran register, bukan interpretasi gameplay.",
"Scope aligned word pada pemetaan EXE dan Entry 1. Function labels adalah nearest JAL/prologue heuristic kecuali FUN_800ec574 diketahui dari target langsung. Indirect/dynamic alias dan code/data separation belum tuntas; nol temuan tidak membuktikan nol writer.",
"Setiap konteks 12 instruksi mempunyai excerpt hex 48 byte (maksimum 64 byte).",
"",
"## DQ2 — helper, +0x2EE, indeks, Chakra",
"",
f"JAL target 0x800EC574 dihitung dari encoding word; hasil pemanggil langsung={len(callers)}. Kolom opcode_guess_match menguji dugaan 0x{JAL_GUESS:08X}.",
f"Manager +0x2EE: {len(accesses)} akses. Hanya MANAGER_ALIAS_CONFIRMED yang membuktikan base dari load global 0x80139EFC; BASE_UNPROVEN tetap kandidat. JALR/tidak langsung tidak lengkap.",
f"Chakra: {len(chakra_reads)} load langsung ke field record+0x18 pada slot 0..3; {len(chakra_sub)} subu memiliki operand dengan taint Chakra. Data-flow linear tidak menangkap seluruh indeks dinamis atau aliran lintas fungsi, jadi daftar bukan bukti semua pengurangan Chakra.",
"Index×2: sll dengan shift=1 di dalam window helper tercantum di DQ2_INDEX_TIMES_TWO_RAW.tsv; skala 2-byte terindikasi, sumber idx belum tentu terbukti.",
"Setiap PC yang basis manager tidak terikat dilabel BASE_UNPROVEN; cakupan pengurangan Chakra yang tidak ter-taint = TIDAK TAHU.",
"",
"## DQ3 — jalur fee level d>=2",
"",
"Status BELUM K2. Tidak ada data-flow raw yang menyambungkan perbandingan level saat ini vs target, operasi fee, dan penulisan global 0x80139EFC. Konteks store kandidat di DQ3_GLOBAL_FILL_PRECONTEXT_RAW.tsv tidak cukup menyimpulkan rumus.",
"",
"Observasi pengguna (hipotesis, X=120, fee dasar 100):",
"",
"| Transisi | d | Observasi | fee*2^d | Hasil |",
"|---|---:|---:|---:|---|",
"| LV1->LV2 | 1 | 100 | 200 | TIDAK COCOK |",
"| LV1->LV3 | 2 | 400 | 400 | COCOK |",
"| LV1->LV4 | 3 | 800 | 800 | COCOK |",
"| LV1->LV5 | 4 | 1600 | 1600 | COCOK |",
"",
"H1: fee akhir = fee dasar × 2^d untuk semua d; 3/4 titik cocok, titik LV1->LV2 memfalsifikasi bentuk universal.",
"H2: d=1 mendapat pengecualian biaya dasar; d>=2 memakai fee × 2^d. Keempat titik pengguna cocok, tetapi H2 hanya hipotesis dari pengamatan pengguna.",
"Falsifier H2: observasi terkontrol X lain dengan d=1 bukan fee dasar atau d>=2 menyimpang; secara statik, cabang tanpa penyesuaian pada d=1/d>=2 yang memakai operasi sama juga memfalsifikasi H2.",
"Tidak dilakukan fitting dengan kurang dari tiga titik; ada empat titik hipotesis, tetapi bukan bukti kode.",
"",
"## Batasan",
"",
"Audit statik; tidak ada emulator, BIOS, savestate, atau upload raw input. Entry1 static base belum divalidasi runtime.",
"Commit pembuat pipeline mengubah: .github/workflows/dq1-dq3-raw-static.yml; tools/stage1/RunDQ1DQ3Raw.py."
]
(OUT/"DQ1_DQ3_RAW_STATIC_AUDIT_2026-11-05.md").write_text("\n".join(mdlines)+"\n",encoding="utf-8")
print("RAW_ANALYSIS=PASS")
print(f"DQ1A_ROWS={len(pre)}")
print(f"DQ1B_WRITERS={len(writers)}")
print(f"DQ2_DIRECT_CALLERS={len(callers)}")
print(f"DQ2_2EE_ACCESSES={len(accesses)}")
print(f"DQ2_CHAKRA_READS={len(chakra_reads)}")
print(f"DQ2_CHAKRA_SUBU={len(chakra_sub)}")
