# BB2 — pembaruan final audit producer action, kredit Chakra, dan batas bukti

Tanggal: 3 November 2026  
Game: Naruto — Shinobi no Sato no Jintori Gassen (PS1, SLPS-03553)  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research

## Putusan gabungan

| Butir | Status | Kelas |
|---|---|---|
| BB1 — field +0x0B, kelompok/link, multiplier dan tabel resource 630 | **TUNTAS** | K4 statis |
| BB2 — mekanisme debit action 3/8, producer dan kredit positif | **SEBAGIAN** | K4 mekanisme; label gameplay / caller dinamis belum tertutup |
| BB3 — matriks runtime action 3/8 pada H6 | **TUNTAS terbatas** | K5 untuk direct function-call pada fixture H6 HIBRIDA |

## BB1 — bukti inti yang dipakai

- FUN_800BE0E4 mengikuti byte link tile+0x01; target harus type 5 dan owner bits 12–15 sama; jumlah target valid ditulis ke tile+0x0B.
- Dua writer record tile: reset di PC 0x800BE1B0 dan hasil hitungan di PC 0x800BE330. Empat writer lain yang ditemukan berada pada object selector DAT_8013A680, bukan record petak.
- Untuk 22 record resource 630, 22/22 link mengarah ke posisi ortogonal satu tile dan menutup ring. Klaim geometri ini dibatasi ke resource/board yang diperiksa.
- FUN_800B770C menerima selector 0–4 dan menghasilkan H×100%, 120%, 150%, 180%, 200%. H = u16(tile+0x10+((u16(tile+0x20)>>7)&0x1E)).
- Record resource index 4: harga netral +0x0E=120; slot nilai +0x10/+0x12/+0x14/+0x16/+0x18 = 60/140/265/530/1050. Angka 60/140/265/530 cocok dengan pengamatan pengguna lv1–lv4; 1050 adalah slot berikut yang belum diamati. +0x1A=100 merupakan fee pada blok transaksi, bukan bukti biaya bangun Barrier.
- Hipotesis HA (+0x0B mengukur jumlah link type-5/owner sama, sehingga ukuran rantai−1) didukung langsung oleh penghitung traversal. Hipotesis HB (+0x0B sebagai tag menu bebas) tidak cocok sebagai penjelasan tunggal karena store tile berasal dari penghitung traversal; falsifier HA ialah contoh valid yang membuat +0x01 menunjuk nonanggota rantai atau jumlah +0x0B berbeda dari jumlah link yang lolos. Label UI +0x0B tetap TIDAK TAHU.

## BB2 — semua immediate producer 3/8 yang teridentifikasi

Census run 41563802704 mengekspor 65 WRITE dan 63 READ pada displacement participant manager +0x2EB. Tiga store immediate yang secara lokal menulis nilai 3 atau 8:

| Nilai | PC store | Fungsi / sumber nilai | Caller |
|---:|---|---|---|
| 3 | 0x800DAA88 | FUN_800D9570; `li v0,3` di 0x800DAA84 lalu store ke +0x2EB | FUN_800F3658, JAL di 0x800F5E1C |
| 8 | 0x800EC3A8 | FUN_800EB434; `li v0,8` di 0x800EC3A4 lalu store ke +0x2EB | FUN_800F3658, JAL di 0x800F5CF8 |
| 8 | 0x800EF3CC | FUN_800EE4E0; `li a0,8` di 0x800EF3C8 lalu store ke +0x2EB | Tidak ditemukan direct-JAL caller ke FUN_800EE4E0 pada scan ini |

Khusus store ketiga, batas fungsi FUN_800EE4E0 meliputi PC 0x800EF3CC. TargetCaller scan memeriksa 149.103 kata aligned dan memvalidasi 176 kandidat raw JAL; tidak ada entri caller dengan target 0x800EE4E0. Ini membuktikan “direct JAL caller tidak ditemukan oleh scan tersebut”, bukan “fungsi tidak pernah dipanggil”. Pemanggilan via dispatch/indirect table masih mungkin tetapi belum terbukti.

Selain immediate store, sejumlah writer +0x2EB membaca manager+0x2E9 lalu menyalin nilainya (contoh jalur FUN_800D9570 dan FUN_800EA18C). Nilai aktual salinan tidak bisa disimpulkan hanya dari nearest immediate di jendela 12 instruksi; jangan hitung sebagai producer 3/8 tanpa menelusuri nilai +0x2E9 saat event bersangkutan. Store nol merupakan clear/reset state.

### Blok transaksi yang menerima action 3 dan 8

Di FUN_800D15A8, byte +0x2EB dibaca di PC 0x800D4470. Cabang 3 dan 8 menuju blok transaksi yang sama:
- Pilih tile melalui FUN_800BBD9C; index terpilih disimpan ke manager+0x4A0.
- Fee adalah u16(tile+0x1A); diperiksa terhadap saldo kerja participant+0x04.
- Pending delta `-fee` ditulis ke manager+0x2EE + participant_index×2.
- Tile+0x20 nibble bits 8–11 bertambah satu dan nibble bits 4–7 bertambah satu; owner bits 12–15 tidak berubah pada blok ini.
- FUN_800BB004 dan FUN_800BE464 dipanggil untuk refresh.

### Hipotesis 3/8 dan falsifier

| Hipotesis | Status | Falsifier |
|---|---|---|
| HA: 3 = bangun Barrier, 8 = upgrade Barrier | HIPOTESIS | Gugur bila prompt/menu dan transisi tile pada gameplay normal menunjukkan urutan lain atau operasi bukan Barrier. |
| HB: 3 = upgrade Barrier, 8 = bangun Barrier | HIPOTESIS | Gugur bila prompt/menu dan transisi tile menunjukkan urutan kebalikan HB. |
| HC: satu atau kedua nilai itu bukan pasangan build/upgrade Barrier | HIPOTESIS alternatif | Gugur bila bukti UI normal secara langsung menamai kedua aksi dan perubahan tile mengonfirmasi bangun lalu upgrade. |

Blok transaksi identik tidak membedakan HA dan HB. Biaya bangun/upgrade Barrier sebagai label gameplay: **TIDAK TAHU**. Yang terbukti hanya debit fee tile+0x1A untuk kedua cabang.

## BB2 — jalur kredit positif, Chakra dan Barrier Release

- Dispatcher FUN_800D15A8 menerima +0x2EB=1 atau 0x1D sebagai jalur state kredit positif, mengatur DAT_80139F03=1, memilih tile dan menjalankan C = u16(tile+0x1E) + level(bits8–11)×u16(tile+0x1C).
- Pada state 2, jika prasyarat manager+0x370 dan FUN_80102408 terpenuhi, nilai C ditulis sebagai pending positif ke manager+0x2EE + participant_index×2 dan saldo proyeksi manager+0x51C diperbarui.
- FUN_800BE5D8 memproses signed pending, lalu memanggil FUN_8001387C; setter menulis PlayerRecord+0x18 (base 0x80070EA0, stride 0xB4), yaitu Chakra kanonis. Maka jalur positif terbukti mengkredit Chakra, bukan sekadar preview.
- Producer immediate yang diketahui: byte 1 di-store pada PC 0x800CF94C (function boundary/caller belum diketahui); byte 0x1D di-store pada PC 0x800E0928 dalam FUN_800E03B0. Jalur producer +0x2E9 / +0x2EA lain tidak seluruhnya ditutup.
- Pesan token 0xBE belum dipetakan ke teks `結界開放`. B44 bukan Barrier Release.

### Hipotesis event kredit dan falsifier

| Hipotesis | Status | Falsifier |
|---|---|---|
| HP: event +0x2EB=1/0x1D adalah Barrier Release; C adalah Chakra hasil release | HIPOTESIS K1 | Gugur bila prompt/teks yang terbukti menamai aksi lain atau Barrier tidak dilepas pada event yang memberi C. |
| HQ: event +0x2EB=1/0x1D adalah aksi tile positif lain, bukan Barrier Release | HIPOTESIS K1 | Gugur bila prompt `結界開放` dan perubahan Barrier sebelum/sesudah muncul pada state yang sama. |

Label event positif: **TIDAK TAHU** sampai teks/UI atau transisi Barrier dapat diperiksa langsung.

## BB3 — runtime H6, hasil terukur

Run 41556732137; job 125657970152; source SHA 296785adc21e399d8b4882cc75a9fda6c8539045; workflow SUCCESS; script/process exit code desimal 0.
- 40/40 PASS, 40 kasus unik: tile 4/7 × action 3/8 × level bits 8–11 0–4 × dua launch per kombinasi.
- Pending delta per kasus: tile4 = −100; tile7 = −120. Fee tidak berubah antarlevel. Kedua nibble level +1; helper refresh FUN_800BB004/FUN_800BE464 tercapai.
- RAM pra-poke 2 MiB SHA-256 5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7 cocok di 40/40 launch. Memory Card disposable tidak berubah, SHA fa43239bcee7b97ca62f007cc68487560a39e19f74f3dde7486db3f98df8e471.
- Fixture H6 SHA d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475 adalah HIBRIDA. Ini direct function-call test, bukan input controller atau pembuktian menu Story Mode. K5 berlaku hanya pada cakupan direct-call ini.

## Run static producer trace terakhir

- Run 41563802704; job 125680354426; source SHA 5c50ea0e5f4f361ba548b28322f49ca87a0632b5; workflow SUCCESS; script EXIT_CODE=0.
- Scope: Ghidra static analysis Entry 1; game/emulator tidak dijalankan, input kontrol tidak dikirim, savestate tidak direstore, dan tidak ada binary privat dipublikasikan.
- Raw Action 8 store 0x800EF3CC kini dipastikan berada di FUN_800EE4E0 dan bernilai 8 dari instruksi langsung sebelumnya. Direct caller FUN_800EE4E0 tidak ditemukan oleh scan raw-JAL yang diekspor.
- Berkas yang diubah oleh commit pemicu run: `.github/workflows/step7-entry1-buffer-base-audit.yml`.

## Referensi output raw

Run summary:
`reports/stage1_economy/aq1-run-41563802704/attempt-1/ACTIONS_RUN_SUMMARY.txt`

Data:
- `reports/stage1_economy/aq1-run-41563802704/attempt-1/bb2-action-byte-access.tsv`
- `reports/stage1_economy/aq1-run-41563802704/attempt-1/bb2-d15a8-direct-callers.txt`
- `reports/stage1_economy/aq1-run-41563802704/attempt-1/aq1-deep-context.tsv`
- `reports/stage1_economy/aq1-run-41563802704/attempt-1/run-summary.txt`
