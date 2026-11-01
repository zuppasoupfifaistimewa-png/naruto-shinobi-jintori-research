# AW0–AW3 — status akhir pekerjaan rekayasa balik (2026-11-01)

Repo: `zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research`  
Branch: `main`  
HEAD sebelum penulisan laporan ini: `d4e182b085baa4b93ade0f11e69f14e61143464f`  
Lingkup kerja: AW0, AW1, AW2, AW3; tidak ada perubahan visibilitas repo/Release.

## Definisi skala K

| Skala | Definisi |
|---|---|
| K0 | Belum ada data yang bisa dipakai |
| K1 | Dugaan/pembanding lemah |
| K2 | Indikasi terbatas, rantai instruksi/aksi belum lengkap |
| K3 | Beberapa bukti saling mendukung, masih ada celah semantik penting |
| K4 | Rantai bukti statis langsung yang dapat diperiksa di instruksi/dekompilasi |
| K5 | Runtime konsisten pada sedikitnya dua peluncuran terpisah untuk kondisi uji sama |

Statis maksimum K4. K5 pada AW3 berlaku hanya untuk fungsi/kondisi yang benar-benar diuji, dan selalu memakai checkpoint **H6 HIBRIDA**. Hasil video/`GAME_RULES.md` hanya pembanding K1; tidak dipakai sebagai sumber angka atau rumus.

## Status tahap

| Tahap | Status | K | Hasil dan batas |
|---|---|---:|---|
| AW0 | **TUNTAS** | K4 | Asal `a1` pada kedua edge ke getter kedua dibuktikan lengkap. |
| AW1 | **TUNTAS** | K4 | Helper petak, empat setter-call manager, field `+0xB44`, dan census field petak diekspor/didekompilasi. Makna gameplay field manager belum diberi label. |
| AW2 | **TUNTAS (sensus statis AW2)** | K4 | Scan raw numeric, sequence/stride, exact keyword, seluruh kandidat Shift-JIS, 47 direct-call windows, function index, serta immediate-literal references main EXE/Entry 0/Entry 1 selesai. Batas terbuka bukan scan yang belum dikerjakan: glyph/font/tile mapping dan runtime mapping resource masih TIDAK TAHU; immediate literals bukan otomatis angka ekonomi. |
| AW3 | **TUNTAS dalam ruang lingkup matriks uji AW3** | K5* | Seluruh 56/56 panggilan yang direncanakan pada matriks AW3 lulus dalam dua launch H6 HIBRIDA, termasuk helper, getter, setter dan dua ekspresi setter berbasis B44. Ini menuntaskan suite uji terkontrol AW3; bukan verifikasi seluruh state machine `FUN_80109FEC` atau aksi gameplay Barrier. |

`K5*` tidak berarti seluruh `FUN_80109FEC` atau gameplay Barrier terbukti runtime. Ia hanya berlaku bagi kondisi dan fungsi yang tampil pada matriks AW3.

## Ringkasan temuan yang sudah dibuktikan

### AW0 — a1 pada getter kedua

Getter pertama di `0x801053C4` mengeksekusi `move a1,a0`; delay slot caller `0x801053C8: move a0,s3` memberi `a0=s3`. Pada BLTZ-taken, tidak ada penulis `a1` sampai call getter kedua `0x80105418`; jadi nilai masuk `a1=s3`.

Pada fall-through, `0x801053D4: lw a1,-0x5AAC(v0)` membaca slot global manager `0x8013A554`; nilai pointer yang diamati adalah `0x801CEF08`. Delay slot getter kedua memberi `a0=s3), lalu body getter menjalankan `move a1,a0` dan menimpa a1 sebelum dipakai sebagai indeks. Pointer manager bukan indeks getter.

### AW1 — formula helper petak

Dari `FUN_800B770C`:
- `G = u32([0x8013EA84])`
- `R = G + (index & 0xFF) * 0x124`
- `sel = u8(R + 0x0B)`
- `slot = (u16(R + 0x20) >> 7) & 0x1E`
- `H = u16(R + 0x10 + slot)`

Hasil:
```
sel 0: H
sel 1: floor(H * 12 / 10)
sel 2: floor(H * 15 / 10)
sel 3: floor(H * 18 / 10)
sel 4: H * 2
sel >=5: 0
```

Dispatch table lima pointer ada pada Entry 1 offset `0x1A4` (VA statis kandidat `0x800AD5F4`), dibaca pada PC `0x800B7750`. Faktor dikodekan di lima target aritmetika, bukan stored array [100,120,150,180,200].

Ini **hasil helper petak**, bukan otomatis pendapatan petak. Ada 44 direct JAL callers dan 47 call windows yang diekspor; helper dipakai di konteks agregasi, pembanding, ambang, dan pengolahan nilai. Caller yang menghubungkan hasil itu sebagai kredit saldo pada aksi commit belum teridentifikasi.

### AW1 — manager dan empat setter-call

Manager pointer: `M=[u32]0x8013A554`. `i=u8(M+0xB2B)`; `Q(i)=getter_0x800138EC(i)`, yang membaca player record `0x80070EA0 + i*0xB4 + 0x18`.

Empat `a1` setter:
1. PC `0x8010A15C`: `Q(i) + u32(M+0xB44)`.
2. PC `0x8010A1B0`: `Q(i)`; setter `a0` berasal dari `0x800171A4(i)`.
3. PC `0x8010A638`: `Q(i) + min(u32(M+0xB44),0x14)`; lalu accumulator B44 dikurangi nilai yang dikreditkan.
4. PC `0x8010A97C`: `Q(i)`; setter `a0` berasal dari `0x800171A4(i)`.

Field manager `+0xB44` di-reset/dibaca/ditulis oleh `FUN_80109994`, `FUN_80109F1C`, `FUN_80109FEC`; inventory memiliki 14 PC akses di tiga fungsi. `+0x14` digunakan pula untuk menaikkan beberapa accumulator manager secara bertahap.

Tidak ada teks atau operand yang membuktikan bahwa `+0xB44` berarti uang, harga Barrier, pendapatan, refund atau Chakra release. Label gameplay itu tidak diberikan.

### AW2 — ruang pencarian data dan teks

Input:
- EXE `SLPS_035.53`: 385,024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
- DATA.BIN Entry 0: 110,536 byte, SHA-256 `56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4`; runtime base TIDAK TAHU.
- DATA.BIN Entry 1: 596,412 byte, SHA-256 `9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a`; file offset `0x10BB000`; base statis kandidat `0x800AD450`, runtime mapping tidak diklaim final.

Raw-byte occurrences nilai 50/60/100/150 dihitung pada u8/u16/u32 dan disimpan di TSV. Semua raw occurrences adalah kandidat, bukan semantik. Sequence multiplier exact contiguous dan strided common values diperiksa pada tiga input: contiguous u8/u16/u32; strided u8 2/4/8/12/16, u16 1/4/8/12/16, u32 1/2/8/12/16. Semua 54 kombinasi yang diuji: 0 hit.

Literal ASCII/Shift-JIS untuk `Barrier`, `Chakra`, `cost`, `upgrade`, `release`, `結界`, `チャクラ`, `費用`, `強化`, `建設`, `解除`, `解放`, `バリア`: 0 hit pada tiga input. Heuristic decode run Shift-JIS: 25 EXE, 3 Entry 0, 234 Entry 1 (262 total); ini hanya run kandidat, belum terhubung ke UI message. Peta glyph/font tile ID: **TIDAK TAHU**.

Run Step 7 paling baru: `41291576229`, job `124803739839`, source SHA `64de9960b60cd0eb629b0c15e9025ca787bf1e84`, status SUCCESS, exit code desimal 0. Run Ghidra utama/Entry0 `41290779708` pada pemeriksaan terakhir masih berjalan di tahap “Extract and analyze DATA.BIN entry 0 for external helper”; hasilnya belum digunakan sebagai bukti final.

### AW3 — runtime H6 HIBRIDA

Run final extended: `41291503009`, job `124803535529`, source SHA `2e53cbb26a1eddce05849580bdcef90113e9368d`, status PASS, script exit code desimal 0.

- 2 peluncuran terpisah, 28 panggilan per peluncuran, 56/56 PASS.
- H6 SHA-256: `d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475` — HIBRIDA (target checkpoint base + CONTROL top-level field 6).
- Helper: 16 kondisi per launch; selector 0–4 untuk H=19,101,257 pada fields +0x10,+0x12,+0x2E dan selector 5 default-zero.
- Getter controls index 0 dan 1: hasil 1500.
- Setter controls input 100,1500,100000,-10000: word yang tersimpan 100,1500,99999,-9999.
- Dua ekspresi a1 manager diisolasi melalui setter: ADD(B44)=0/7/25 dan CAP(B44)=0/7/25; enam kondisi per launch. Getter Q=1500 menghasilkan:
  - ADD: 1500, 1507, 1525.
  - CAP: 1500, 1507, 1520.
- Semua kondisi lulus pada kedua launch. B44 baseline H6=0; manager pointer teramati `0x801CEF08`.
- Memory Card SHA sebelum/sesudah sama: `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`.
- Baseline/final RAM SHA (2 MiB): `5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7` pada kedua launch. Snapshot RAM dan register dipulihkan setelah tiap panggilan. Raw RAM delta direkam; perubahan accessor getter pertama dan setter target tidak disalahtafsirkan sebagai no-write, tetapi baseline penuh dipulihkan.
- Timeout 600 detik; peluncuran terlama 58.880 detik; timeout lebih dari 2× durasi terlama.
- Pengguna tidak mengirim input; Story Mode adaptive player tidak dijalankan.

`FUN_80109FEC` **tidak dipanggil langsung** dalam AW3. Dekompilasi menunjukkan state machine UI/input/audio/state dengan flag caller `param_1+0xC & 0x20`, banyak mutasi manager fields dan chained functions eksternal; direct call tanpa state/init precondition dapat menyebabkan side effect yang tidak terkontrol. Sebagai gantinya, AW3 menyuntikkan `a1` hasil dua ekspresi AW1 ke setter sebenarnya pada B44 terkontrol 0/7/25. Jadi bukti K5 berlaku bagi aritmetika ekspresi yang diinjeksi dan perilaku setter, bukan seluruh state transition Barrier.

## Tiga pertanyaan gameplay utama

| Pertanyaan | Status | K | Alasan |
|---|---|---:|---|
| Pendapatan petak | **SEBAGIAN** | K3 | Helper petak dan faktor 100–200% terbukti K4 dan hasil helper teruji K5 pada dua launch. Belum terbukti bahwa hasil helper adalah jumlah kredit final pada aksi commit petak. |
| Biaya bangun/upgrade Barrier | **BELUM** | K2 | Manager accumulator B44 dan angka +0x14 terbukti secara kode, tetapi belum ada bukti teks/caller yang menghubungkannya dengan harga bangun atau upgrade Barrier. |
| Chakra yang diperoleh dari Barrier release | **BELUM** | K2 | Jalur manager dapat menambah player record +0x18 dari B44, membatasi kredit per update hingga 0x14 lalu mengurangi accumulator. Identitas state itu sebagai “Barrier release” belum dibuktikan oleh UI/message/caller. |

## Ringkasan pekerjaan dan berkas yang diubah

HEAD pada awal audit AW0–AW3: `5954e1839d03313d37c9b90ac5da4ac01a75ba3c`. Repo maju melalui commit sumber, report, dan Actions-generated reports; tidak ada perubahan pada Release/visibility. Daftar commit manual utama dan berkas yang diubah:

| Commit | Berkas yang diubah |
|---|---|
| `272c0728d766187e1b4d431cbae8b472f14f94ac` | `AT1_GETTER_CALLS.tsv`; `AT1_GETTER_CALLS_RECONCILED_2026-11-01.tsv`; `AT1_STATIC_AUDIT_2026-11-01.md`; `AT1_STATIC_FINAL_REPORT_2026-11-01.md`; `AU1_ACCESSOR_DISASSEMBLY_2026-11-01.md` |
| `ee245b6138c418aff4d0b6d895d0cb5447e870af` | `.github/workflows/step7-entry1-buffer-base-audit.yml`; `tools/ghidra/ExportManagerFieldAccesses.java`; `tools/step7/ExportStage1EconomyAQ1.java`; `tools/step7/ExportStage1EconomyDeepContext.java`; `tools/step7/ScanStage1EconomyData.py`; `tools/step7/SummarizeStage1EconomyCensus.py` |
| `c95ad1ffc8834ff660f1dcbb88e681e29dea0546` | `.github/workflows/step7-entry1-buffer-base-audit.yml`; `reports/stage1_economy/aq1-run-41279241109/attempt-1/ACTIONS_RUN_SUMMARY.txt`; `tools/ghidra/ExportManagerFieldAccesses.java` |
| `db3719c54c40d4ea2706894c071e6215205389d0` | `.github/workflows/step7-entry1-buffer-base-audit.yml`; `tools/ghidra/ExportNumericLiteralReferences.java`; `tools/step7/ScanStage1EconomyData.py` |
| `71d7e05449da3bf7f1782d10bb1db9cf614cfd69` | `.github/workflows/step7-entry1-buffer-base-audit.yml`; `tools/ghidra/ExportCallWindows.java`; `tools/step7/ScanStage1EconomyData.py` |
| `80808e81dce62022b7dff3f7c8c23d1e83517c60` | `reports/stage1_economy/AU1_ACCESSOR_DISASSEMBLY_2026-11-01.md` |
| `18b926049fac5126118f545cf46ae2f01e5d84f0` | `.github/workflows/ghidra-static-analyze-psx-exe.yml`; `tools/step7/ScanStage1EconomyData.py` |
| `c5c1c88fe62653b734f7a4311a5feac02eb07440` | `.github/workflows/aw3-controlled-helper-call-interpreter.yml`; `experiments/aw3_controlled_helper_call_interpreter.py` |
| `9445d79af7e192e2a90f2942ed532ed82ff72310` | `experiments/aw3_controlled_helper_call_interpreter.py` |
| `711f4fb22422b79724d5591f55ab72b3a08c77d5` | `experiments/aw3_controlled_helper_call_interpreter.py` |
| `2339c50db8cc1eeba75ac7d65786b0ae7cb1ef9e` | `experiments/aw3_controlled_helper_call_interpreter.py` |
| `4325ccf24132470fb1df5077d285fccd83d8faa0` | `experiments/aw3_controlled_helper_call_interpreter.py` |
| `76a5cd9eb645cb6aa6494523f0c34997436b7d32` | `reports/stage1_economy/AW1_AW2_FINAL_REPORT_2026-11-01.md` |
| `2e53cbb26a1eddce05849580bdcef90113e9368d` | `experiments/aw3_controlled_helper_call_interpreter.py` |
| `64de9960b60cd0eb629b0c15e9025ca787bf1e84` | `tools/step7/ScanStage1EconomyData.py` |

Actions-generated commits menambahkan keluaran teks/TSV ke folder `reports/stage1_economy/aq1-run-<run-id>/attempt-1/` atau `aw3-controlled-run-<run-id>/attempt-1/`; berkas utamanya tercantum di folder output run yang ditautkan pada laporan. Tidak ada biner/ROM/BIOS/savestate/RAM dump dipublikasikan.

## Referensi hasil utama di repo

- AW0: AT1 static audit, AT1 getter call TSV, reconciled getter TSV, AU1 accessor disassembly.
- AW1: `aq1-run-41291576229/attempt-1/aw1-manager-function-detail.txt`, `aw1-manager-b44-accesses.tsv`, `aw1-tile-field-function-inventory.tsv`, `aw1-helper-call-windows.tsv`.
- AW2: `aq1-run-41291576229/attempt-1/aw2-static-data-scan.md`, `aw2-numeric-occurrences.tsv`, `aw2-numeric-instruction-literals.tsv`, `ghidra-main-entry0-run-41290779708/ACTIONS_RUN_SUMMARY.txt`.
- AW3: `aw3-controlled-run-41291503009/attempt-1/ACTIONS_RUN_SUMMARY.txt`, `AW3_SUMMARY.txt`, `AW3_LAUNCHES.tsv`, `AW3_CALL_RESULTS.tsv`, `AW3_SCRIPT_EXIT_CODE.txt`.

**Kesimpulan:** AW0 dan AW1 selesai sebagai audit statis, sensus statis AW2 selesai (termasuk run Ghidra 41290779708 SUCCESS), dan matriks uji terkontrol AW3 selesai 56/56 PASS pada dua launch H6 HIBRIDA. Keempat paket AW0–AW3 tuntas dalam batas pekerjaan masing-masing. Ini bukan berarti logika gameplay keseluruhan tuntas: peta font/tile, runtime mapping Entry 0/1, hubungan helper dengan pendapatan petak, harga Barrier, dan identitas aksi Barrier release masih TIDAK TAHU atau belum terbukti. Tidak ada rumus gameplay yang direka.
