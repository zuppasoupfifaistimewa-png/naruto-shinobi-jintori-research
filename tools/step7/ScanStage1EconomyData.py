#!/usr/bin/env python3
"""AW2 verified-byte scan for constants, table candidates, Shift-JIS and tile/font evidence."""
import argparse,csv,hashlib
from pathlib import Path
EXE_SHA="a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569"
E0_SHA="56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4"
E1_SHA="9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a"
VALUES=(50,60,100,150)
MULT=(100,120,150,180,200)
PHRASES=("Barrier","Chakra","cost","upgrade","release","結界","チャクラ","費用","強化","建設","解除","解放","バリア")
DISPATCH=(0x800B7760,0x800B77A0,0x800B7808,0x800B7850,0x800B789C)
DISPATCH_BYTES=bytes.fromhex("60 77 0B 80 A0 77 0B 80 08 78 0B 80 50 78 0B 80 9C 78 0B 80")
def sha(b): return hashlib.sha256(b).hexdigest()
def addr(n,o):
    if n=="SLPS_035.53" and o>=0x800: return f"0x{0x80010000+o-0x800:08X}"
    if n=="DATA.BIN_ENTRY1": return f"0x{0x800AD450+o:08X} (static candidate; runtime unverified)"
    return "TIDAK TAHU (entry0 runtime base)"
def sjis_runs(data,min_pairs=3):
    out=[];i=0
    while i<len(data):
        start=i;buf=bytearray();pairs=0
        while i<len(data):
            b=data[i]
            if 0x20<=b<=0x7e or 0xa1<=b<=0xdf:
                buf.append(b);i+=1;continue
            if (0x81<=b<=0x9f or 0xe0<=b<=0xef) and i+1<len(data):
                t=data[i+1]
                if 0x40<=t<=0xfc and t!=0x7f:
                    buf.extend((b,t));pairs+=1;i+=2;continue
            break
        if pairs>=min_pairs:
            raw=bytes(buf)
            try: txt=raw.decode("shift_jis",errors="strict")
            except UnicodeDecodeError: txt=raw.decode("shift_jis",errors="replace")
            if any(ord(ch)>127 for ch in txt): out.append((start,raw,txt))
        if i==start: i+=1
    return out
def main():
    ap=argparse.ArgumentParser()
    for x in ("exe","entry0","entry1","markdown","tsv"): ap.add_argument("--"+x,required=True)
    a=ap.parse_args()
    files={"SLPS_035.53":Path(a.exe).read_bytes(),
           "DATA.BIN_ENTRY0":Path(a.entry0).read_bytes(),
           "DATA.BIN_ENTRY1":Path(a.entry1).read_bytes()}
    expected={"SLPS_035.53":EXE_SHA,"DATA.BIN_ENTRY0":E0_SHA,"DATA.BIN_ENTRY1":E1_SHA}
    for n,b in files.items():
        if sha(b)!=expected[n]: raise SystemExit(f"{n} SHA mismatch: {sha(b)}")
    notes=["# AW2 — konstanta, tabel, Shift-JIS dan font/tile search","",
      "Input terverifikasi SHA-256. Entry 1 memakai base statis kandidat 0x800AD450; runtime mapping belum diverifikasi.",
      "","| Input | Bytes | SHA-256 |","|---|---:|---|"]
    for n,b in files.items(): notes.append(f"| {n} | {len(b)} | {sha(b)} |")
    rows=[]
    notes += ["","## Kemunculan angka 50/60/100/150 (LE u8/u16/u32)","",
      "Kemunculan byte mentah hanya kandidat. Xref dan konteks instruksi diperlukan sebelum label ekonomi.",
      "","| Input | Nilai | Lebar | Jumlah | Offset/VA awal (maks 20) |","|---|---:|---:|---:|---|"]
    for n,b in files.items():
        for v in VALUES:
            for w in (1,2,4):
                pat=v.to_bytes(w,"little");hits=[];p=0
                while True:
                    p=b.find(pat,p)
                    if p<0: break
                    hits.append(p);p+=1
                loc="; ".join(f"0x{x:X}/{addr(n,x)}" for x in hits[:20]) or "none"
                notes.append(f"| {n} | {v} | {w*8} | {len(hits)} | {loc} |")
                for x in hits[:20]:
                    rows.append({"input":n,"kind":f"u{w*8}","value":v,"offset":f"0x{x:X}",
                                 "address":addr(n,x),"bytes":pat.hex(" "),"xref":"TIDAK TAHU"})
    notes += ["","## Sequence 100/120/150/180/200 (LE u8/u16/u32)","",
      "Pencarian exact contiguous. Tabel berpadded/strided perlu disimpulkan melalui instruksi pembaca."]
    for n,b in files.items():
        for w in (1,2,4):
            pat=b"".join(v.to_bytes(w,"little") for v in MULT);hits=[];p=0
            while True:
                p=b.find(pat,p)
                if p<0: break
                hits.append(p);p+=1
            notes.append(f"- {n} u{w*8}: {len(hits)} hits; "+("; ".join(f"0x{x:X}/{addr(n,x)}" for x in hits[:12]) or "TIDAK DITEMUKAN"))
            for x in hits[:12]:
                rows.append({"input":n,"kind":f"multiplier_sequence_u{w*8}","value":"100,120,150,180,200",
                             "offset":f"0x{x:X}","address":addr(n,x),"bytes":pat.hex(" "),"xref":"TIDAK TAHU"})
    notes += ["","## Dispatch table FUN_800B770C","",
      "DATA.BIN Entry 1 file offset 0x1A4 = VA kandidat 0x800AD5F4. Lima word berikut diverifikasi byte-per-byte sebagai pointer dispatch, bukan table berisi angka persentase.",
      "","| Selector | VA tabel | Offset | Byte LE | Target |","|---:|---:|---:|---|---|"]
    e1=files["DATA.BIN_ENTRY1"];off=0x1A4;got=e1[off:off+len(DISPATCH_BYTES)]
    if got!=DISPATCH_BYTES: raise SystemExit(f"FUN_800B770C dispatch table byte mismatch got={got.hex()}")
    for i,target in enumerate(DISPATCH):
        pos=off+i*4;chunk=e1[pos:pos+4]
        notes.append(f"| {i} | 0x{0x800AD5F4+i*4:08X} | 0x{pos:X} | {chunk.hex(' ').upper()} | 0x{target:08X} |")
        rows.append({"input":"DATA.BIN_ENTRY1","kind":"jump_table_u32","value":i,"offset":f"0x{pos:X}",
                     "address":f"0x{0x800AD5F4+i*4:08X}","bytes":chunk.hex(" "),"xref":"FUN_800B770C PC 0x800B7750"})
    notes += ["","Reader: FUN_800B770C at PC 0x800B7750 loads the selected word with lw v0,0x0(v1). The branch boundary is sltiu v0,v1,0x5 at 0x800B7738; selector >=5 returns zero at 0x800B7798.",
      "","### Perhitungan faktor ada dalam instruksi (bukan literal table 100/120/150/180/200)","",
      "| Selector | Target | Instruksi aritmetika yang terbukti |","|---:|---:|---|",
      "| 0 | 0x800B7760 | return H |",
      "| 1 | 0x800B77A0 | H*12; magic reciprocal 0x66666667 divides by 10 at 0x800B77E8–0x800B7804 |",
      "| 2 | 0x800B7808 | 16H−H=15H; divide by 10 at shared 0x800B77E8–0x800B7804 |",
      "| 3 | 0x800B7850 | 9H*2=18H; divide by 10 at shared 0x800B77E8–0x800B7804 |",
      "| 4 | 0x800B789C | H*2 at 0x800B78D8 |",
      "",
      "H = u16(R+0x10+((u16(R+0x20)>>7)&0x1E)); R=[0x8013EA84]+index*0x124. Ini hasil helper; bukan dengan sendirinya pendapatan/biaya gameplay."]
    notes += ["","## Literal Shift-JIS/ASCII terms",""]
    for n,b in files.items():
        for word in PHRASES:
            enc=[]
            try: enc.append(("ASCII",word.encode("ascii")))
            except UnicodeEncodeError: pass
            try: enc.append(("Shift-JIS",word.encode("shift_jis")))
            except UnicodeEncodeError: pass
            for typ,pat in enc:
                hits=[];p=0
                while True:
                    p=b.find(pat,p)
                    if p<0: break
                    hits.append(p);p+=1
                notes.append(f"- {n} {typ} {word}: {len(hits)}")
                for x in hits[:8]:
                    rows.append({"input":n,"kind":"string_"+typ,"value":word,"offset":f"0x{x:X}",
                                 "address":addr(n,x),"bytes":b[x:x+len(pat)].hex(" "),"xref":"TIDAK TAHU"})
    notes += ["","## Run Shift-JIS heuristik","",
      "Mengambil run byte yang valid sebagai Shift-JIS multi-byte (minimal tiga pasangan), lalu decode. Ini kandidat string, belum tentu dipakai UI."]
    sjtotal=0
    for n,b in files.items():
        runs=sjis_runs(b);sjtotal+=len(runs)
        notes.append(f"### {n}: {len(runs)} runs")
        for off,raw,txt in runs[:60]:
            safe=txt.replace("|","/").replace("\n"," ")[:96]
            notes.append(f"- offset=0x{off:X}; address={addr(n,off)}; bytes={raw[:40].hex(' ')}; text={safe}")
            rows.append({"input":n,"kind":"sjis_run","value":safe,"offset":f"0x{off:X}",
                         "address":addr(n,off),"bytes":raw[:40].hex(" "),"xref":"TIDAK TAHU",
                         "note":"decode candidate only; UI linkage unknown"})
    notes += ["","## Peta font/tile index","",
      "Belum ada rantai instruksi yang mengaitkan indeks glyph/tile UI ke tabel font yang dapat diverifikasi. Maka peta index->glyph adalah TIDAK TAHU; tidak ada tabel buatan.",
      f"Readable Shift-JIS runs={sjtotal}. Nihilnya kata kunci literal bukan bukti bahwa text resources tidak ada.",
      "","## Batas","",
      "- Tidak memberi label Barrier cost/income/Chakra release dari angka semata.",
      "- Xref numeric data candidates tetap TIDAK TAHU tanpa instruksi pembaca.",
      "- Entry 0 runtime base TIDAK TAHU; tidak ada VA yang direka.",
      "- Entry 1 runtime mapping belum dibuktikan; hanya static candidate base.",
      "- Static scan only; no gameplay/emulator."]
    Path(a.markdown).write_text("\n".join(notes)+"\n",encoding="utf-8")
    with Path(a.tsv).open("w",encoding="utf-8",newline="") as f:
        cols=("input","kind","value","offset","address","bytes","xref","note")
        w=csv.DictWriter(f,fieldnames=cols,delimiter="\t");w.writeheader();w.writerows(rows)
    print(f"AW2_SCAN=PASS candidate_rows={len(rows)} sjis_runs={sjtotal} dispatch=verified")
if __name__=="__main__": main()
