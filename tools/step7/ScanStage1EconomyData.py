#!/usr/bin/env python3
"""AW2 verified-byte scan; occurrences are candidates, not semantic labels."""
import argparse,csv,hashlib
from pathlib import Path
EXE_SHA="a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
E0_SHA="56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4"
E1_SHA="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
VALUES=(50,60,100,150); MULT=(100,120,150,180,200)
PHRASES=("Barrier","Chakra","cost","upgrade","release","結界","チャクラ","費用","強化","建設","解除","解放","バリア")
def sha(b):return hashlib.sha256(b).hexdigest()
def addr(n,o):
    if n=="SLPS_035.53" and o>=0x800:return f"0x{0x80010000+o-0x800:08X}"
    if n=="DATA.BIN_ENTRY1":return f"0x{0x800AD450+o:08X} (candidate; runtime unverified)"
    return "TIDAK TAHU (entry0 runtime base)"
def main():
    ap=argparse.ArgumentParser()
    for x in ("exe","entry0","entry1","markdown","tsv"):ap.add_argument("--"+x,required=True)
    a=ap.parse_args()
    files={"SLPS_035.53":Path(a.exe).read_bytes(),"DATA.BIN_ENTRY0":Path(a.entry0).read_bytes(),"DATA.BIN_ENTRY1":Path(a.entry1).read_bytes()}
    expected={"SLPS_035.53":EXE_SHA,"DATA.BIN_ENTRY0":E0_SHA,"DATA.BIN_ENTRY1":E1_SHA}
    for n,b in files.items():
        if sha(b)!=expected[n]:raise SystemExit(f"{n} SHA mismatch: {sha(b)}")
    notes=["# AW2 — scan numerik dan string literal","",
    "Input SHA diverifikasi. Kemunculan angka adalah kandidat byte, bukan label ekonomi.",
    "","| Input | Bytes | SHA-256 |","|---|---:|---|"]
    for n,b in files.items():notes.append(f"| {n} | {len(b)} | {sha(b)} |")
    rows=[]
    notes+=["","## Angka 50/60/100/150","",
    "| Input | Nilai | Lebar | Jumlah | Offset/VA pertama (maks 25) |","|---|---:|---:|---:|---|"]
    for n,b in files.items():
        for v in VALUES:
            for w in (2,4):
                pat=v.to_bytes(w,"little");hits=[];p=0
                while True:
                    p=b.find(pat,p)
                    if p<0:break
                    hits.append(p);p+=1
                loc="; ".join(f"0x{x:X}/{addr(n,x)}" for x in hits[:25]) or "none"
                notes.append(f"| {n} | {v} | {w*8} | {len(hits)} | {loc} |")
                for x in hits[:25]:rows.append({"input":n,"kind":f"u{w*8}","value":v,"offset":f"0x{x:X}","address":addr(n,x),"bytes":pat.hex(" "),"xref":"TIDAK TAHU"})
    notes+=["","## Sequence 100/120/150/180/200","",
    "Dicari contiguous LE halfword/word; keberadaan sequence tidak menetapkan penggunaannya."]
    anyseq=False
    for n,b in files.items():
        for w in (2,4):
            pat=b"".join(v.to_bytes(w,"little") for v in MULT);hits=[];p=0
            while True:
                p=b.find(pat,p)
                if p<0:break
                hits.append(p);p+=1
            anyseq |= bool(hits)
            notes.append(f"- {n} u{w*8}: {len(hits)} hit; "+("; ".join(f"0x{x:X}/{addr(n,x)}" for x in hits[:20]) or "TIDAK DITEMUKAN"))
            for x in hits[:20]:rows.append({"input":n,"kind":f"sequence_u{w*8}","value":"100,120,150,180,200","offset":f"0x{x:X}","address":addr(n,x),"bytes":pat.hex(" "),"xref":"TIDAK TAHU"})
    if not anyseq:notes.append("TIDAK TAHU: tidak ditemukan sequence contiguous persis; tabel berpadded atau urutan berbeda belum disangkal.")
    notes+=["","## String ASCII/Shift-JIS","",
    "Pencarian literal saja; bila teks UI memakai indeks tile/font, pemetaan glyph belum dibuat."]
    for n,b in files.items():
        for word in PHRASES:
            enc=[]
            try:enc.append(("ASCII",word.encode("ascii")))
            except UnicodeEncodeError:pass
            try:enc.append(("Shift-JIS",word.encode("shift_jis")))
            except UnicodeEncodeError:pass
            for typ,pat in enc:
                hits=[];p=0
                while True:
                    p=b.find(pat,p)
                    if p<0:break
                    hits.append(p);p+=1
                notes.append(f"- {n} {typ} {word}: {len(hits)}")
                for x in hits[:8]:
                    excerpt=b[max(0,x-16):min(len(b),x+len(pat)+24)]
                    try:desc=excerpt.decode("shift_jis",errors="replace").replace("\t"," ")[:96]
                    except Exception:desc="decode unavailable"
                    rows.append({"input":n,"kind":"string_"+typ,"value":word,"offset":f"0x{x:X}","address":addr(n,x),"bytes":excerpt.hex(" "),"xref":"TIDAK TAHU","note":desc})
    notes+=["","## Batas","",
    "- Tidak memberi label Barrier cost/income/Chakra release pada angka tanpa operand flow yang terbukti.",
    "- Xref/pembaca numeric candidate TIDAK TAHU sampai alamat tabel dihubungkan ke instruksi pembaca.",
    "- Pemetaan glyph tile/font TIDAK TAHU.",
    "- Entry 1 menggunakan base statis kandidat 0x800AD450; runtime mapping belum validated.",
    "- Statis saja; tidak ada emulator/gameplay."]
    Path(a.markdown).write_text("\n".join(notes)+"\n",encoding="utf-8")
    with Path(a.tsv).open("w",encoding="utf-8",newline="") as f:
        fields=("input","kind","value","offset","address","bytes","xref","note")
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t");w.writeheader();w.writerows(rows)
    print(f"AW2_SCAN=PASS rows={len(rows)} binary_artifact=no")
if __name__=="__main__":main()
