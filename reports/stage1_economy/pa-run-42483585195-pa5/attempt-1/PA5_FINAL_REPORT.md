# PA5 — uji simbolik dan falsifier H1/H2

Baseline inklusif: 3f730c73dc628d02f360b7ac12961e6f3e4b1584
PA4 data directory: reports/stage1_economy/pa-run-42482696764-pa4/attempt-1
PA4_CONTROL_SNAPSHOTS=PASS
SCALARS_IDENTICAL=YES
M_REGION_IDENTICAL=YES
M_REGION_BYTES=1344
REASON=TWO_IDENTICAL_CONTROL_SNAPSHOTS

## Uji hipotesis
H1 (x=d): BELUM K1. Tidak ada transaksi berlabel d dan x pada checkpoint CONTROL; dua launch identik adalah uji pengulangan, bukan variasi jarak. Falsifier: pasangan transaksi dengan x!=d atau x tetap saat d berubah.
H2 (x=id efek): BELUM K1. ID efek belum diberi label semantik dan belum ada pemetaan ID->x. Falsifier: ID sama dengan x berbeda, atau pemetaan ID gagal pada kasus terpisah.
Kecocokan byte mentah atau nilai scalar di wilayah M, bila ada, hanya KORELASI; bukan bukti makna variabel.

## Formula biaya
Biaya upgrade petak untuk lompatan d>=2: BELUM K1 — TIDAK TAHU. Tidak menggunakan 400/800/1600 dan tidak melakukan fitting.

## Ledger
Actions runs total fetched=1264; runs after baseline=4 (lihat PA5_RUN_LEDGER.tsv).
Commits baseline-inclusive (tanpa commit publikasi PA5)=16; perubahan A/M/D ada di PA5_COMMIT_LEDGER.tsv.
Laporan ini tidak mengubah STATUS.md, workflow lama, Release, atau berkas biner.

## Commit file list
See PA5_PUBLISH_COMMIT_FILES.tsv.
