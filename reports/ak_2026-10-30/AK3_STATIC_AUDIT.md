# AK3 — koreksi statis dan keputusan sementara

Tanggal: 30 Oktober 2026. Sumber awal: `38e2a891c627ee34d813fddd3a64b187086f8770`. Ini adalah addendum statis; keputusan final host/RSI menunggu hasil runtime AK1–AK2.

## Skala bukti K0–K5

K0 = tidak ada bukti atau fakta belum diketahui; K1 = petunjuk tunggal/hipotesis yang belum diverifikasi; K2 = observasi eksplisit dari satu artefak/log tetapi belum dikorroborasi; K3 = beberapa artefak statis konsisten dengan provenance yang dapat ditelusuri; K4 = validasi statis independen yang dapat diulang dan diperiksa pada byte/digest/struktur, tetapi tanpa bukti runtime untuk klaim yang dinilai; K5 = bukti runtime dari sedikitnya dua peluncuran independen pada kondisi dan titik ukur yang ditetapkan. Bukti statis saja maksimal K4.

## Dua belas SHA AE2 tetap TIDAK TAHU

AJ1 raw audit tidak memiliki digest hibrida yang terpasangkan untuk enam kasus berikut, masing-masing attempt 1 dan 2:
- `ae2-current-bisect-step1`
- `ae2-current-bisect-step2`
- `ae2-current-bisect-step3`
- `ae2-current-bisect-step4`
- `ae2-current-bisect-step5`
- `ae2-target-current-all-24-control`

Total: 12 baris SHA = **TIDAK TAHU**. Bukti: `reports/aj_2026-10-30/runs/run-41028457166/attempt-1/AJ1_RAW_GDB_TABLE.tsv` dan `AJ1_AJ3_COMPLETION_REPORT.md`. Digest log GDB/PCSX bukan digest hibrida; tidak dipakai untuk menebak atau mengganti nilai.

## Rekonsiliasi putusan host/RSI

Dokumen `AJ1_AJ3_FINAL_REPORT.md` dan `AJ3_REPLAY_DETERMINISM_PLAN.md` menyebut pencarian host/RSI tidak diparkir, tetapi dibatasi ke A/B terkendali. Laporan run-scoped `runs/run-41028457166/attempt-1/AJ1_AJ3_COMPLETION_REPORT.md` menyebut pencarian basis RAM SPU host/RSI diparkir sampai replay multi-frame dan pemetaan address-space lebih jelas. Perbedaan ini harus dibaca sebagai status keputusan pada waktu bukti berbeda, bukan bukti runtime baru.

**Putusan sementara AK3:** pencarian host/RSI yang luas/tidak terkendali tetap **DIPARKIR** sampai baseline multi-frame H6/control pada AK1–AK2 selesai dan rentang RAM relevan dapat diklasifikasikan. Bila replay H6 terkonfirmasi deterministik pada 180/240/360 dan kontrol lolos, tahap berikut yang diizinkan hanyalah A/B satu variabel host/RSI yang telah dipraregistrasi, sedikitnya dua launch per kondisi. Bila baseline multi-frame tidak lolos, tetap parkir dan perbaiki harness/provenance lebih dahulu. Tidak ada hasil saat ini yang membuktikan kausalitas host/RSI; kausalitas = **TIDAK TAHU**.

## Batas pemetaan alamat yang sudah diketahui

- `0x80070EA0`: basis rekaman pemain 0. Luas/akhir record tidak disimpulkan dari base saja.
- `0x801CEF08`: alamat target word pointer yang dibaca pada `0x8013A554`; semantik objek yang dituju belum terverifikasi.
- `0x8013A554`: pada runtime checkpoint, bytes `08 EF 1C 80`; tetapi audit statis `STEP6_GLOBAL_POINTER_SLOT_AUDIT_2026-10-28.md` mencatat bahwa pada kandidat base Ghidra `0x800D0000`, bytes di alamat numerik itu berada dalam program view dan terdekode sebagai instruksi MIPS `sw s0,0x70(sp)`. Ini adalah konflik code/data mapping atau relocation yang belum selesai. Jangan kategorikan alamat tersebut sebagai pointer object atau runtime code write tanpa pemetaan runtime independen.
- Alamat/rentang stack dan rentang kode runtime yang cukup presisi untuk memberi label pada setiap delta RAM: **TIDAK TAHU** dari pemetaan statis yang ditelusuri di addendum ini. Delta yang tidak tepat menimpa salah satu rentang yang terverifikasi harus tetap berlabel TIDAK TAHU.

Status addendum: **SEBAGIAN | K4**. AK3 runtime/final menunggu hasil AK1–AK2. Tidak ada savestate, BIOS, ISO, Memory Card, RAM dump, atau biner hibrida yang dikomit.
