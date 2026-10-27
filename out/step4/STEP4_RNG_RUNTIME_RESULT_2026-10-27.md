# Langkah 4 — hasil runtime RNG dan roulette (27 Oktober 2026)

Status langkah: **SEBAGIAN**. Uji runtime terkontrol berhasil menghasilkan log dan screenshot valid setelah perbaikan capture, tetapi seed saat boot, hubungan caller dengan hasil roulette, konteks battle, serta cakupan RNG alternatif belum tertutup.

## Sumber dan integritas

- Run utama: [GitHub Actions #40474262267](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267).
- Artefak diagnosis privat: [artifact #12719024236](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40474262267/artifacts/12719024236), ZIP 2.187.882 byte, digest SHA-256 `cec3404b38afbedbae151fc15e9ec66d9c019ff853e4703f8813acac7793bdf4`, tidak kedaluwarsa saat audit.
- Artifact berisi log, metadata, serta tangkapan X11 autentik dari emulator. Screenshot privat tidak dimasukkan ke Git; disc, BIOS, Memory Card, savestate, dan dump RAM tetap berada pada runner privat.
- Status keseluruhan Actions `failure` disebabkan tahap terakhir yang menulis ringkasan ke GitHub Contents API (exit code 22). Tahap eksperimen sendiri mencatat `STEP4_RUNTIME_INFRA_STATUS=PASS`; seluruh cabang berakhir dengan rc=0 dan capture/input lulus. Karena itu, hasil runtime di bawah dihitung dari log asli artefak, bukan dari ringkasan otomatis lama yang keliru.

## Setup dan input

- Ketiga cabang memulihkan checkpoint roulette terverifikasi yang sama; initial RNG state sesudah restore pada ketiganya `0xDB75C114`.
- `R30A` dan `R30B`: Circle ditekan pada frame 30 dan dilepas pada frame 38. Readback tekan dan lepas `PASS`.
- `DELAY60`: Circle ditekan pada frame 60 dan dilepas pada frame 68. Readback tekan dan lepas `PASS`.
- Pengamatan dilakukan dengan CPU interpreter, breakpoint pada entry RNG `0x80035D78), pembacaan global `0x800A3118), sampel state, serta screenshot X11. Screenshot diambil saat event caller terminal `0x80105F48) menghentikan cabang. Frame VSync terminal berbeda antarproses, maka frame-frame itu tidak disamakan.

## Hasil state RNG dan caller

Semua cabang menghasilkan **127 hit** RNG, tanpa hit setter RNG pasca-restore. Urutan 127 panggilan dibandingkan dengan mengabaikan nomor frame tetapi tetap membandingkan nomor urut (sequence), caller, serta state sebelum panggilan. Stream ternormalisasi cocok persis antara `R30A`, `R30B`, dan `DELAY60`.

| Sampel VSync | R30A state / total hit | R30B state / total hit | DELAY60 state / total hit |
|---:|---|---|---|
| 1 | `0xDB75C114` / 0 | `0xDB75C114` / 0 | `0xDB75C114` / 0 |
| 20 | `0xDB75C114` / 0 | `0xDB75C114` / 0 | `0xDB75C114` / 0 |
| 30 | `0xDB75C114` / 0 | `0xDB75C114` / 0 | `0xDB75C114` / 0 |
| 38 | `0x03F64FB2` / 2 | `0x03F64FB2` / 2 | `0x03F64FB2` / 2 |
| 60 | `0x3C3C2CA6` / 126 | `0x3C3C2CA6` / 126 | `0x3C3C2CA6` / 126 |
| 80 | `0x3C3C2CA6` / 126 | `0x3C3C2CA6` / 126 | `0x3C3C2CA6` / 126 |
| 100 | `0x3C3C2CA6` / 126 | `0x3C3C2CA6` / 126 | `0x3C3C2CA6` / 126 |
| 150 | `0x3C3C2CA6` / 126 | `0x3C3C2CA6` / 126 | `0x3C3C2CA6` / 126 |
| 160 | `0x3C3C2CA6` / 126 | `0x3C3C2CA6` / 126 | `0x3C3C2CA6` / 126 |
| 170 | — | — | `0x3C3C2CA6` / 126 |

Caller runtime yang terlihat dalam window checkpoint ini: `0x8010B0E8), `0x8010C20C), `0x8010C248), `0x8010C68C), dan terminal event `0x80105F48). Dua pemanggilan awal berasal dari `0x8010B0E8); panggilan berikutnya yang berjumlah 124 berasal dari tiga alamat `0x8010C20C), `0x8010C248), dan `0x8010C68C); panggilan ke-127 adalah `0x80105F48) dengan state-before `0x3C3C2CA6). Setelah panggilan terminal, state final yang tercatat adalah `0xA99DC6E7) pada semua cabang.

Tidak ada setter hit pasca-restore. Itu hanya membatasi jendela yang diamati; bukan bukti tentang siapa menginisialisasi seed saat boot atau apakah jalur reseed/pointer lain berjalan sebelum checkpoint.

## Screenshot X11 autentik dan perbandingan viewport

Semua tiga tangkapan gambar lolos validasi `1280×800), ukuran berkas `724063` byte, `117603` warna dan nilai `valid=True). SHA-256 data piksel viewport ternormalisasi (crop `(105,22)-(1175,760))) untuk ketiganya sama:

`a1b2dfab61a0922e2b466ddbeb6b5b2642a88289be159df4667e4e2bcaa53355`

| Cabang | Event capture/finish frame | Jumlah hit | State akhir | Viewport SHA-256 |
|---|---:|---:|---|---|
| R30A | 169 | 127 | `0xA99DC6E7` | sama |
| R30B | 167 | 127 | `0xA99DC6E7` | sama |
| DELAY60 | 171 | 127 | `0xA99DC6E7` | sama |

Nomor VSync capture tidak identik (169/167/171); jangan menyatakan tangkapan tersebut diambil pada frame yang sama. Bukti yang mendukung determinisme terbatas adalah kesamaan stream RNG ternormalisasi, state yang disampel, state akhir dan piksel viewport saat event terminal yang sama secara semantik. Ini menunjukkan tidak ada perbedaan teramati pada tiga cabang ini antara jeda input 30 dan 60 dalam konteks checkpoint tersebut. Bukti ini **tidak mengidentifikasi hasil pilihan roulette yang terlihat secara independen** atau membuktikan bahwa setiap caller menghasilkan hasil roulette itu.

## Matriks kriteria Langkah 4

| Kriteria | Status | Bukti dan batas |
|---|---|---|
| (a) Generator, formula, state RAM, sumber/lifecycle seed | **SEBAGIAN** | LCG dan global state terverifikasi statis; state runtime serta pembaruan akhir teramati. Sumber seed saat boot/lifecycle penuh belum dibuktikan. |
| (b) Determinisme state/caller/viewport dengan input-delay terkontrol | **SEBAGIAN—inti pengamatan lulus** | Dua repeat jeda 30 dan satu jeda 60 memiliki stream sequence/caller/state yang identik, state sampel dan final sama, viewport pixel-identical. Frame VSync terminal berbeda dan hasil pilihan roulette belum dihubungkan. |
| (c) Caller langsung dan pointer/dispatch | **SEBAGIAN** | Inventaris direct-JAL raw main EXE + kandidat DATA.BIN sudah dianalisis/didekode dalam cakupan laporan statis; base resource masih hipotesis, beberapa boundary/reachability belum selesai; indirect/pointer dispatch dan kode yang hanya tampak setelah decode belum disingkirkan. |
| (d) Caller roulette dan battle | **SEBAGIAN** | Callers diobservasi pada checkpoint roulette terverifikasi; tidak dipastikan caller mana yang menentukan hasil visual. Tidak ada pengamatan checkpoint battle pada run ini. |
| (e) RNG alternatif/non-function randomness | **SEBAGIAN** | Scan signature LCG raw terdokumentasi serta tidak menemukan signature identik pada file raw lain yang discan; scan terbatas itu tidak mengecualikan algoritme lain, table RNG, frame/time input, atau kode terdekompresi/dekripsi. |

**Keputusan:** Langkah 4 keseluruhan tetap **SEBAGIAN**. Pemetaan statis LCG/direct caller dan determinisme runtime yang diamati pada satu checkpoint meningkat; seed boot, hubungan ke hasil roulette, caller battle, indirect dispatch menyeluruh, dan alternative-randomness coverage tetap terbuka.

## Catatan teknis untuk kelanjutan

- Run #40471968654 gagal karena pengamat hanya menunggu F177 walau event terminal RNG terjadi sekitar F171; perbaikannya tidak mengubah checkpoint induk.
- Run #40473505032 memperlihatkan deadlock capture terkait pause/callback dan parser report yang salah; hasil itu tidak dipakai untuk kesimpulan.
- Run #40474262267 memakai capture event yang dinamis dan menyelesaikan semua cabang dengan rc=0. Job keseluruhan gagal hanya pada penulisan ringkasan ke GitHub Contents API; ringkasan ini direkonstruksi dari log asli dan validasi artefak di atas.
- Sumber checkpoint/savestate diperlakukan read-only; cabang Memory Card terpisah; private runner directory dibersihkan pada akhir run.

