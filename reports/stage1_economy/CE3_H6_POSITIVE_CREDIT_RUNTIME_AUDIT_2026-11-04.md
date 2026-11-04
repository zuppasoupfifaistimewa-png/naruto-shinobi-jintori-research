# CE3 — audit runtime kredit positif H6 (4 November 2026)

## KOREKSI TERBARU — run 41749255678 (HEAD audit 012367cf0518e519520fe590845d62792289276a)

**Koreksi ini mengesampingkan bagian “Actions run terbaru” dan “Log runtime mentah” historis di bawah.**

- GitHub workflow: `completed/success`; job `ce3-h6-positive-credit-probe`, ID `126309939178`: `completed/success`.
- Source SHA: `b2ccb20041c31496b23ce531eec3434753db7868`.
- Test summary: `STATUS=SEBAGIAN`, `EXIT_CODE=2`; script exit desimal **2**, wrapper/launch exit desimal **73**.
- Launch 1 (tile 4, level 0, attempt 1) berakhir dalam 145.779 s; timeout dikonfigurasi 1201 s.
- Gate preflight read-only meniru `FUN_80102408`: global `0x8013A22C=0x801CDF80`; `pointer+4=0x801CEC88`; `pointer+0xEA8=0xFFFFFFFE`; hasil prediksi `4294967294`. Gate memblokir state 2 sebelum setter/kredit.

Log mentah:
```text
CE3_STATE1_RETURN phase=2
CE3_STATE2_GLOBAL_POINTER_8013A22C=0x801CDF80
CE3_STATE2_GATE_POINTER_VALID=YES
CE3_STATE2_GATE_FIELD_PLUS4=0x801CEC88
CE3_STATE2_GATE_FIELD_PLUS_EA8=0xFFFFFFFE
CE3_STATE2_GATE_PREDICTED_RETURN=4294967294
CE3_RAW_ERROR=.../launches/tile-4-level-0-attempt-1/ce3.lua:186: STATE2_GATE_PREFLIGHT_BLOCK field4=0x801CEC88 fieldEA8=0xFFFFFFFE predicted=4294967294
CE3_CALL_STATUS=FAIL
```

Pesan `8-bit read from unknown address: ffffd138` pada bagian historis di bawah berasal dari run 41740957322, **bukan** run terbaru. Jangan gunakan pesan lama sebagai penyebab run 41749255678.

Data frame 180/360 masing-masing cocok dengan SHA referensi; memory card disposable sebelum/sesudah tidak berubah. Hanya satu launch tercatat, tanpa hasil pemain/setter/kredit. Run ini bukan read-only murni karena fixture pokes di RAM disposable (lihat laporan CF0–CF3). K5 belum tercapai.

---

## Putusan historis — run 41740957322 (digantikan oleh koreksi di atas)

**CE3: SEBAGIAN — K2 hanya untuk transisi state 1 → phase 2; jalur kredit ke Chakra kanonis BELUM (K0). K5 tidak tercapai.**

Harness CE3 berhasil dikompilasi dan melewati pemeriksaan Langkah 0. Restore H6 dan pembacaan RAM 2 MiB pada frame 180/360 juga lolos. Namun, pada launch pertama (tile 4, level 0, attempt 1), pemanggilan state 1 kembali dan mengubah phase menjadi 2; pemanggilan kedua `FUN_800D15A8` tidak mencapai return sentinel. Tidak ada baris hasil pemain, pending kredit, pemanggilan setter, atau nilai Chakra pasca-kredit yang dihasilkan.

**Penting:** BB3 terdahulu 40/40 PASS adalah uji direct-dispatch debit action 3/8. Itu bukan uji jalur kredit positif CE3 dan tidak boleh dipakai untuk menyatakan CE3 lolos.

## Sumber yang diaudit

- Baseline yang diminta pengguna: `cd90b281f45cada726e80c3f87661e5ae5494303`.
- HEAD main pada saat koreksi terbaru: `012367cf0518e519520fe590845d62792289276a` (98 commit di depan baseline).
- Handoff yang tersedia: `docs/HANDOFF_STAGE1_ECONOMY_2026-10-31.md`.
- Checkpoint yang lebih baru: `reports/stage1_economy/BB_STATE.md` (tanggal 3 November 2026).
- Laporan statis CE0–CE2: `reports/stage1_economy/CE0_CE1_CE2_STATIC_AUDIT_2026-11-04.md`.
- Harness: `experiments/ce3_h6_positive_credit_probe.py`; workflow: `.github/workflows/ce3-h6-positive-credit-probe.yml`.

## Actions run sebelumnya — run 41740957322 (historis)

- Run: `41740957322`
- Job: `ce3-h6-positive-credit-probe`
- Job ID: `126282568335`
- Source SHA: `c9e89ab1f811940349bfd0e61d6b64d89ff6526d`
- `CE3_SCRIPT_EXIT_CODE=2`
- `CE3_WORKFLOW_SCRIPT_PROCESS_EXIT=2`
- Launch pertama: tile=4, level=0, attempt=1; wrapper exit desimal **137**, durasi **600.034 detik**; proses dihentikan timeout.
- Cakupan: 1/20 launch; 0/40 baris kondisi pemain; 0/40 PASS.

### Langkah 0 — build/validasi harness

**PASS**, exit code 0. Isi mentah file `CE3_STEP0_BUILD_VALIDATION.txt`:

```text
CE3_STEP0_PLAYER_CHakra_ADDRESSES=PASS player0=0x80070EB8 player1=0x80070F6C
CE3_STEP0_REQUIRED_TOKENS=PASS
CE3_STEP0_EXIT_CODE=0
```

Jadi **tidak ada error Langkah 0 pada run terbaru**. Riwayat error lama yang sudah dikoreksi:
- Run `41740037209`: `CE3_STEP0_REQUIRED_TOKEN_MISSING=['0x80070F6C']`, exit 1; validasi token lama menuntut alamat literal, padahal alamat pemain 1 dihitung dari base + stride + offset.
- Run `41740281514`: build/validasi lulus, tetapi runtime Lua mengeluarkan error mentah `CE3_RAW_ERROR=.../ce3.lua:245: attempt to perform arithmetic on global 'TILE_STRIDE' (a nil value)`. Ini bukan error Langkah 0 dan versi berikutnya sudah melewati inisialisasi tile tersebut.

### Smoke H6 dan integritas

Smoke-test pemuatan H6 PASS (exit 0; 1.807 detik); event restore dan pembacaan memory-file berhasil. Tidak ada input gameplay.

H6 hybrid yang diuji:
`d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475`

Snapshot RAM:
- Frame 180: 2,097,152 byte; SHA-256 `5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7` — cocok referensi.
- Frame 360: 2,097,152 byte; SHA-256 `4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907` — cocok referensi.

Memory Card disposable:
- Sebelum: `fa43239bcee7b97ca62f007cc68487560a39e19f74f3dde7486db3f98df8e471`
- Sesudah: `fa43239bcee7b97ca62f007cc68487560a39e19f74f3dde7486db3f98df8e471`
- Tidak berubah.

### Log runtime mentah run 41740957322 (historis; bukan penyebab terbaru)

Dari `CE3_FIRST_NONPASS_TILE4_LEVEL0_ATTEMPT1.txt`:

```text
CE3_CALL_BEGIN label=D15A8_STATE1_P0 entry=0x800D15A8 old_pc=0x80037320 sp=0x801FFD90 ra=0x80011448
CE3_CALL_RETURN label=D15A8_STATE1_P0
CE3_STATE1_RETURN phase=2
CE3_CALL_BEGIN label=D15A8_STATE2_P0 entry=0x800D15A8 old_pc=0x80011448 sp=0x801FFD90 ra=0x80011448
CD_init:addr=800672b4
8-bit read from unknown address: ffffd138
```

Tidak ada `CE3_CALL_RETURN label=D15A8_STATE2_P0`, `CE3_STATE2_RETURN`, `CE3_PLAYER_RESULT`, atau `CE3_SETTER_CALL`. Pesan alamat tak dikenal tersebut dicatat apa adanya; belum cukup untuk membuktikan pointer sumbernya.

### Prasyarat statis state 2 yang belum diperiksa harness

Checkpoint BB_STATE dan dekompilasi `FUN_800D15A8` menyatakan state 2 memerlukan **dua kondisi**:
1. `manager + 0x370 == 1`;
2. `FUN_80102408() == 0`.

Harness saat ini menyiapkan syarat pertama dengan poke `manager+0x370=1`, tetapi tidak membaca/memvalidasi nilai hasil syarat kedua sebelum memanggil state 2.

Fungsi `FUN_80102408` pada Entry 1 (base analisis statis yang dipakai: `0x800AD450`) mempunyai potongan berikut:

```text
80102408 [14 80 02 3C] lui v0,0x8014
8010240c [2C A2 43 8C] lw v1,-0x5dd4(v0)  ; membaca pointer global 0x8013A22C
80102414 [04 00 62 8C] lw v0,0x4(v1)
8010241c [04 00 40 10] beq v0,zero,0x80102430
80102424 [A8 0E 62 8C] lw v0,0xea8(v1)
80102428 [08 00 E0 03] jr ra
80102430 [08 00 E0 03] jr ra            ; delay slot: li v0,-1
```

Arti statis:
- bila field `*(u32 *)(pointer + 4)` sama dengan 0, helper mengembalikan `-1`;
- selain itu, helper mengembalikan `*(u32 *)(pointer + 0xEA8)`;
- untuk cabang kredit positif state 2, nilai return harus tepat 0.

**Hipotesis diagnostik, belum fakta runtime:** pembacaan `0xFFFFD138` mungkin berkaitan dengan pointer global `0x8013A22C` yang tidak valid (misalnya pointer sekitar `0xFFFFD134` bila alamat yang dibaca memang pointer+4). Harness tidak pernah mencatat nilai global pointer tersebut, sehingga hubungan ini **BELUM TERBUKTI**. Jangan poke/fiksasi pointer sebelum nilai dan objek yang semestinya dibuktikan.

### Timeout run 41740957322 (historis)

Timeout disetel 600 detik. Riwayat mencatat peluncuran terlama yang selesai 145.815 detik, tetapi run terbaru sendiri mencapai timeout 600.034 detik. Ringkasan script menyatakan `TIMEOUT_GE_2X_OBSERVED_MAX=False`. Karena tidak ada penyelesaian launch terbaru, persyaratan timeout ≥2× waktu terlama pada rangkaian ini **belum dapat dinyatakan terpenuhi**. Jangan menyamakan timeout dengan durasi launch yang selesai.

## Langkah lanjutan yang tepat

1. Tambahkan pembacaan **read-only** pointer global `0x8013A22C`; hanya jika menunjuk rentang RAM yang valid, baca `+4` dan `+0xEA8`, lalu log hasil prediksi `FUN_80102408()`.
2. Jika pointer tidak valid atau hasil bukan 0, hentikan sebelum state 2. Telusuri initializer/producer objek itu dari state H6; jangan menulis pointer/field spekulatif.
3. Jika hasil gate 0, pasang PC trace pada callsite state 2 (mulai `0x800D5128`, `0x800D5134`, `0x800D513C`) agar helper terakhir yang dicapai diketahui bila state 2 kembali macet.
4. Baru setelah satu diagnostic launch berhasil, jalankan matriks lengkap tile 4/7 × level 0–4 × dua launch independen; setiap launch wajib membaca kedua record pemain dan setter/Chakra kanonis. K5 hanya bila semua kondisi memenuhi ulangan dan pemeriksaan RAM/Memory Card/timeout/exit-code.

## Batas integritas

- Tidak ada perubahan pada Release `naruto-checkpoint-39262213468` atau visibilitas repository.
- Tidak ada upload ROM/ISO, BIOS, savestate, dump RAM, Memory Card, screenshot, video, atau frame ke repo.
- Tidak mengubah `STATUS.md`; ukuran di HEAD audit `9928ee9ed3db578e7ea81b6d23a471082c2a0a51` diverifikasi **693,844 byte**.
- BB3 K5 lama tetap terbatas untuk direct-call debit action 3/8 pada H6 hibrida. CE3 kredit positif tidak boleh mewarisi status itu.
- Event 1/0x1D belum boleh dinamai Barrier Release; token pesan 0xBE dan B44 bukan bukti label itu.


## Riwayat koreksi file
Koreksi CF0 run 41749255678 ditambahkan pada snapshot yang berangkat dari HEAD `012367cf0518e519520fe590845d62792289276a`. Daftar berkas yang diubah pada commit koreksi terdapat di `CF0_CF1_CF2_CF3_AUDIT_2026-11-04.md`.
