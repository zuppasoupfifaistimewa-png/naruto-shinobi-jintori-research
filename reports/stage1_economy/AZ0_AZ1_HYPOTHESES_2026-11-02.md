# AZ0–AZ1 — hipotesis dan falsifier
Tanggal: 2 November 2026
Bukti statis maksimum K4; bukti runtime H6 selalu berlabel HIBRIDA, bukan target murni.

## AZ0 — identitas writer dan pemetaan Entry 1

- H1 (K2): tiga PC WRITER_CONFIRMED (0x80109980, 0x80109990, 0x80109A98) berada pada Entry 1 dengan offset file yang dihitung memakai base statis kandidat 0x800AD450. Falsifier: ekstraksi ulang Entry 1 menunjukkan byte pada offset hasil rumus tidak cocok dengan 38 0B 44 AC / 30 0B 44 AC / 2A 0B 80 A0, atau mapping base terbukti berbeda.
- H2 (K3): instruksi tersebut menulis field manager +0xB38, +0xB30, dan +0xB2A karena dua wrapper memuat pointer dari slot 0x8013A554 dan instruksi ketiga berada pada fungsi yang mengakses manager. Falsifier: base register/slot pada decode raw-byte ternyata bukan pointer manager atau disassembly independen menunjukkan instruksi lain.

## AZ1 — interpretasi snapshot manager dan record petak

- H1 (K1, diuji di runtime): B38 cocok dengan floor(sum seluruh V petak / 2) pada H6 untuk setiap pasangan launch/frame. Falsifier: nilai B38 aktual tidak sama dengan nilai yang dihitung ulang dari semua record pada salah satu capture yang valid.
- H2 (K1): B30 berasal dari satu baris pada tabel yang berawal/beralamat 0x800577A4. Falsifier: trace statis atas semua writer/caller B30 menunjukkan nilai berasal dari input lain, atau ekspresi index tidak mengakses rentang tabel itu. Saat ini index/row terpilih TIDAK TAHU; snapshot hanya mengumpulkan byte 0x800577A4.

Tidak ada hipotesis AZ1 yang boleh dinaikkan menjadi fakta sebelum empat snapshot (2 launch × 2 frame) valid, SHA RAM dan Memory Card cocok, exit code desimal serta timeout memenuhi syarat, dan angka V dihitung dari tiap record.
