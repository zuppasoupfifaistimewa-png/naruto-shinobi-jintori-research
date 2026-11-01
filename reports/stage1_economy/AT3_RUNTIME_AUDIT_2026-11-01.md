# AT3 runtime audit — AN2 schedule A/C, K0/K2

Date: 1 November 2026 (Asia/Jakarta)  
Repo: zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research  
Actions run: 41256458701  
Job: 124700549589 — AT3 eight-launch AN2 schedule A/C K0/K2 trace  
Run/job status: completed / success  
Source SHA: 7659306d19bdac7e9a831b4ed7355f60c8dc1dc0  
Actions output commit (workflow publisher): 405431bf61d36e91ad0f5a729968b62773d9caf0  
Script exit code: 0  
H6 SHA-256: d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475 — **HYBRID**, target checkpoint base plus CONTROL top-level protobuf SPU field 6; not target-pure.

## Matrix and validity

Eight independent launches were completed: schedule C (no input) and schedule A (CIRCLE press at post-load GPU::Vsync frame 60, release frame 61), each with K0 (breakpoints disabled) and K2 (three breakpoints), twice per cell.

- All 8 launches reached post-load frame 360, all 24 frame captures (180/240/360) passed.
- Emulator exit code: decimal 0 on all 8 launches.
- Every schedule-A press/release readback was PASS; schedule C had no gameplay input.
- All eight launches used separate copies of Memory Card. Before/after SHA-256 was unchanged in every launch: ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5.
- Timeout was 1,800 seconds per launch. Maximum observed wall time was 170.799 seconds; timeout exceeded twice that maximum.
- RAM hashes are SHA-256 of the first 2 MiB; savestate RAM segment parsed was 8 MiB. Raw savestates and RAM were temporary runner files, not committed.

## RAM hashes at capture frames

| Schedule | Mode | Attempt | Frame 180 | Frame 240 | Frame 360 |
|---|---|---:|---|---|---|
| C | K0 | 1, 2 | 5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7 | 75df26c668759d1a70a4765e87cab077184442381b84e3d1112ce05bf5627ec0 | 4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907 |
| C | K2 | 1, 2 | same as C/K0 | same as C/K0 | same as C/K0 |
| A | K0 | 1, 2 | 0251aeef113a4c1eb58533a7dc5af85488e9bc2d96f42e24f62f8806ab0b6be8 | 3b06642ed54bac03aaf9962f9074b84e550c861c57d7648fcb1f7cc5f14dc70d | 2c53c4a225acccda78ebf67cb39e4922b0ee73d8c2da44928957df36792cc780 |
| A | K2 | 1, 2 | same as A/K0 | same as A/K0 | same as A/K0 |

The two launch attempts were identical per schedule/mode/frame. On this H6 HIBRIDA and these fixed schedules, K2 instrumentation did not change the captured RAM hashes relative to K0 at frames 180/240/360. This does not rule out transient changes between those sampled frames.

## Breakpoint counts and register observations

K0 has breakpoints disabled; its hit columns are NOT_MONITORED_BREAKPOINTS_OFF, not zero.

K2 breakpoints were armed at post-load frame 180 and observed through frame 360. Hit totals below are per condition across two attempts:

| Condition | Setter 0x8001387C | Getter 0x800138EC | Helper 0x800B770C | Getter returns |
|---|---:|---:|---:|---:|
| C | 0 | 720 | 0 | 720 |
| A | 0 | 720 | 0 | 720 |

Getter hits split across their two callsites: 360 hits at caller return address 0x801053CC and 360 at 0x80105420 per condition. Each of these 360 counts spans both attempts and the observed even-frame range 180–358. The corresponding getter-return events all recorded v0=0x000005DC.

At getter entry:
- First callsite (ra=0x801053CC): a0 and a1 each observed as 0 or 1.
- Second callsite (ra=0x80105420): a0 observed as 0 or 1; a1 observed as 0x801CEF08.
- Return events used a0=0x80070EA0 or 0x80070F54; a1 at return was 0 or 1.

**Scope limitation:** K2 breakpoints are only active from post-load frame 180 to frame 360. Zero hits at the monitored setter/helper addresses mean no execution at those addresses in that window on this H6 experiment only. It is not evidence that these functions are unused in other frames, states, modes, or target-pure gameplay.

## Conclusion

**AT3: TUNTAS — K5 terbatas pada eksperimen H6 HIBRIDA ini.** Runtime repetitions, input readbacks, captures, exit codes, Memory Card hashes, and timeout bound all passed. No gameplay/economy meaning is assigned to the observed register values or breakpoint counts.


## AU0 — replikasi hasil, hash, dan riwayat kegagalan

Replikasi **run 41259662960**, job **124710123732**, status **PASS**, source SHA `968c1a55731e09f815a1d1d385e1bf3edf792279`, kode keluar desimal **0**. Ini memakai binary PCSX-Redux yang sama dengan path terkoreksi `$APPDIR/bin/pcsx-redux`. Ringkasan Actions tersimpan pada `reports/stage1_economy/at3-an2-schedule-k0-k2-run-41259662960/attempt-1/ACTIONS_RUN_SUMMARY.txt`.

Delapan launch pada replikasi lolos, semua memakai `-debugger -interpreter`; semua exit code desimal 0; keempat input CIRCLE pada jadwal A (press frame 60, release frame 61) berstatus PASS; Memory Card masing-masing launch terpisah dan sebelum/sesudah tidak berubah. SHA-256 Memory Card pada setiap salinan: `ac0dbcb89e54bcddf7c698fb6fe52cb0ca71977dba2d28e521d6ed556c7a11b5`. Wall time launch 145.430–146.409 detik; timeout 1800 detik, lebih dari 2x wall time terlama. Seluruh capture frames 180/240/360 PASS.

### Perbandingan file bukti replikasi

Dibanding run **41256458701**, run **41259662960** memiliki file identik, baik isi tekstual maupun Git blob SHA-1. SHA-256 dari keseluruhan konten file (ditulis lengkap 64 digit) juga sama:

| Artefak | Git blob SHA-1 run 41256458701 = 41259662960 | SHA-256 konten run 41256458701 = 41259662960 |
|---|---|---|
| `AT3_FRAMES.tsv` | `de6245baad6eb23582a09ef30d332ca3195ef9a7` | `2203119098ab42d1f914f426a7a87bd4db960867e5c526c12bfbe79c8138039b` |
| `AT3_HIT_COUNTS.tsv` | `f332f7de3b86ebb124c4180bb7fe6c6c2e68610f` | `0f86efe06cdb366231953af711176db5ba113bfdcc0e0b85eccbac1f653031b6` |
| `AT3_BREAKPOINT_EVENTS.tsv` | `dcfde400b5285167d540ae5b08a3e7b0a28d99ba` | `fa58b5a2dc74945267a7aefb2e97348d448daffc9664572aaa22642b14366cff` |

Git blob identifier adalah SHA-1 40 digit; SHA-256 konten ditambahkan untuk memenuhi pemeriksaan hash penuh 64 digit. Isi file di kedua run juga dibandingkan langsung dan identik.

### Selisih jadwal A dan C

Hash RAM 2 MiB pertama berbeda antara schedule C (tanpa input) dan A (CIRCLE frame 60–61) pada ketiga checkpoint. Nilai yang sama muncul pada masing-masing dua attempt, baik K0 maupun K2:

| Frame | Schedule C — no input | Schedule A — CIRCLE 60–61 |
|---:|---|---|
| 180 | `5167f48febe55bacd61088286b5a900b32bc95a1efb899225a429e33924609b7` | `0251aeef113a4c1eb58533a7dc5af85488e9bc2d96f42e24f62f8806ab0b6be8` |
| 240 | `75df26c668759d1a70a4765e87cab077184442381b84e3d1112ce05bf5627ec0` | `3b06642ed54bac03aaf9962f9074b84e550c861c57d7648fcb1f7cc5f14dc70d` |
| 360 | `4d002df6902a6de6aa0724b4284da8decb1725cf693fd1ed80ce0132c45a7907` | `2c53c4a225acccda78ebf67cb39e4922b0ee73d8c2da44928957df36792cc780` |

Perbedaan hash menunjukkan snapshot berbeda di kondisi yang dibandingkan, bukan penjelasan perubahan state maupun bukti bahwa input CIRCLE mengubah satu variabel game tertentu. Sebab rinci perubahan state tetap **TIDAK TAHU** dari hash agregat ini.

### Hit breakpoint yang benar-benar teramati pada K2

Di masing-masing schedule C dan A, agregat dua launch K2 (jendela frame 180–360) mencatat:

| Jadwal | Setter 0x8001387C | Getter 0x800138EC | Helper 0x800B770C | Getter return |
|---|---:|---:|---:|---:|
| C | 0 | 720 | 0 | 720 |
| A | 0 | 720 | 0 | 720 |

K0 mencatat `NOT_MONITORED_BREAKPOINTS_OFF`, bukan hit count nol. Getter return yang diamati pada RA `0x801053CC` dan `0x80105420` menunjukkan `a0=0x80070EA0` atau `0x80070F54`, `a1=0` atau `1`, dan `v0=0x000005DC`. Di entry getter, `a0=0` atau `1`; pada call RA `0x80105420`, `a1=0x801CEF08) dapat tampak saat masuk, tetapi body penuh membuktikan a1 tersebut ditimpa oleh `move a1,a0`. Perincian register dan instruksi berada di laporan AU1.

Hit count setter/helper bernilai nol hanya pada breakpoint dan jendela ini. Tidak ada inferensi bahwa setter/helper tidak dipanggil di frame, state, mode, atau jalur lain.

### Percobaan yang gagal

| Run | Job | Source SHA | Kode keluar desimal | Hasil |
|---|---:|---|---:|---|
| 41256334815 | 124700189639 | `832ccdfe2cc15f0622be23fbfff33f8d104e0a6a` | 1 | `read_schedule` menolak jadwal B; emulator belum start; tidak ada runtime evidence |
| 41258300049 | — | — | 2 (script), subprocess 127 | executable path yang dipilih tidak ada; nol hit/input readback tidak valid untuk ditafsirkan |
| 41256208915 (AT2 precheck) | 124699799885 | `390e989e87840232ee30fb3bc5a2aaf831a3419a` | 22 | HTTP 401 unduh checkpoint target; emulator belum start |

Run 41258300049 diperbaiki dengan menunjuk executable `$APPDIR/bin/pcsx-redux`; run 41259662960 membuktikan replikasi berhasil setelah perbaikan. Run gagal 41256334815 dan 41256208915 tidak dihitung sebagai observasi game.

## Kesimpulan AT3 setelah replikasi

**AT3 TUNTAS — K5 terbatas pada matriks A/C × K0/K2 di H6 HIBRIDA.** Ada dua run yang lolos, masing-masing dua peluncuran per kondisi, dengan file hasil FRAMES/HITS/EVENTS identik. Pada jendela K2 yang lama (frame 180–360), getter 0x800138EC teramati; setter 0x8001387C dan helper 0x800B770C bernilai nol pada jendela tersebut. Nol hit hanya berarti tidak tertangkap pada alamat dan jendela yang diawasi. Kesimpulan ini tidak berlaku di luar H6 HIBRIDA, mode, dan jendela itu.

Run 41259662960 tidak memperluas window breakpoint lama; AU3 baru yang diminta terpisah memperluas observasi menjadi frame 1–600 dan menonaktifkan breakpoint getter. Hasil AU3 dilaporkan terpisah.
