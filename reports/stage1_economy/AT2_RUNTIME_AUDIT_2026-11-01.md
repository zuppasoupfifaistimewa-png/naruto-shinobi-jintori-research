# AT2 — pembandingan flag emulator pada H6 HIBRIDA

Tanggal: 1 November 2026 (Asia/Jakarta)  
Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`  
Run: **41256330348** — job **124700159848** — status **PASS** — source SHA `9e5a60cb468593c7d9049691d55f687e059066e5` — kode keluar desimal **0**.  
H6 SHA-256: `d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475`. **HIBRIDA**: checkpoint target sebagai dasar ditambah top-level protobuf SPU field 6 dari checkpoint CONTROL; bukan checkpoint target murni.

## Kondisi dan validitas

Dua kondisi, masing-masing dua peluncuran independen, tanpa input gameplay dan tanpa breakpoint:

- **F1**: `-no-debugger -no-gdb -dynarec`.
- **F2**: `-interpreter -no-debugger -no-gdb`.

Snapshot SHA-256 atas 2 MiB awal RAM diambil pada post-load GPU::Vsync frame 180, 240, dan 360. Semua 4 peluncuran exit code desimal 0; seluruh 12 capture PASS. Memory Card dipisahkan per peluncuran dan tidak berubah; SHA-256 sebelum/sesudah setiap peluncuran adalah `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`. Timeout per peluncuran 1800 detik; waktu terlama 143.227 detik, jadi timeout >=2x waktu terlama.

## Perbandingan snapshot

| Frame | Baseline AK1 | Baseline AS3 K0 | F1 (-dynarec), 2/2 launch | F2 (-interpreter), 2/2 launch |
|---:|---|---|---|---|
| 180 | `4c964aaca0afccc68317acd0726fec680c305b903cd426e70afe3d8ac1f1e741` | `5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7` | cocok AK1, tidak cocok AS3 K0 | cocok AS3 K0, tidak cocok AK1 |
| 240 | `16880faeccfca1fbd42d199c1543b00ec8a065bcd53545d14ea4657c9a6c2d5c` | `75df26c668759d1a70a4765e87cab077184442381b84e3d1112ce05bf5627ec0` | cocok AK1, tidak cocok AS3 K0 | cocok AS3 K0, tidak cocok AK1 |
| 360 | `a9ac5282e9fb9ad1e77f46ef0c291af8e7e5f27b477b6b31e319f971e7dd9942` | `4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907` | cocok AK1, tidak cocok AS3 K0 | cocok AS3 K0, tidak cocok AK1 |

**Kesimpulan yang terbukti:** pada H6 HIBRIDA, dua peluncuran F1 mereplikasi snapshot AK1 pada tiga frame sampel; dua peluncuran F2 mereplikasi snapshot AS3 K0 pada tiga frame sampel. F1 dan F2 berbeda dari satu sama lain pada setiap frame sampel.

**Tidak terbukti:** identitas seluruh state/runtime di antara frame, alasan internal mengapa dynarec dan interpreter memiliki hash berbeda, efek flag pada logika permainan yang tidak tertangkap snapshot, dan makna ekonomi field RAM. Hash cocok hanya menunjukkan kesamaan byte RAM 2 MiB pertama pada titik capture yang diuji. Tidak ada kesimpulan gameplay/economy yang ditarik dari hash.

## Kegagalan terpisah

Run **41256208915**, job **124699799885**, source SHA `390e989e87840232ee30fb3bc5a2aaf831a3419a`, exit code desimal **22**, status `PRECHECK_FAILED`: HTTP 401 saat mengunduh asset checkpoint target. Emulator belum mulai; hasil ini bukan run F1/F2 dan bukan hasil perilaku game.

## Berkas bukti

- `reports/stage1_economy/at2-h6-flags-run-41256330348/attempt-1/AT2_SUMMARY.txt`
- `AT2_LAUNCHES.tsv`, `AT2_FRAMES.tsv`, `AT2_BASELINE_COMPARISON.tsv`
- `ACTIONS_RUN_SUMMARY.txt` memuat status, job, job ID, run ID, source SHA, dan kode keluar.
  
Status: **AT2 TUNTAS — K5 terbatas pada eksperimen H6 HIBRIDA, dua launch per kondisi dan tiga titik snapshot.** Tidak mengangkat kesimpulan menjadi verifikasi logika game target-pure.
