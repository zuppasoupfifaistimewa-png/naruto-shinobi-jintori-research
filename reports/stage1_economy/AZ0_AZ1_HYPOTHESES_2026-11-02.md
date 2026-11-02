# AZ0–AZ1 — hipotesis, falsifier, dan hasil uji
Tanggal: 2 November 2026
Bukti statis maksimum K4; runtime pada H6 selalu dilabel HIBRIDA, bukan target murni.

## AZ0 — identitas writer dan pemetaan Entry 1

- H1 (K2): tiga PC WRITER_CONFIRMED (0x80109980, 0x80109990, 0x80109A98) berada pada Entry 1 dengan offset file yang dihitung memakai base statis kandidat 0x800AD450. Falsifier: ekstraksi ulang Entry 1 menunjukkan byte pada offset hasil rumus tidak cocok dengan 38 0B 44 AC / 30 0B 44 AC / 2A 0B 80 A0, atau mapping base terbukti berbeda.
- H2 (K3): instruksi tersebut menulis field manager +0xB38, +0xB30, dan +0xB2A karena pointer manager diload melalui slot 0x8013A554; setiap byte raw cocok dengan decode MIPS. Falsifier: pembacaan offset/basis Entry1 alternatif atau decode independen membuktikan base register bukan manager atau byte instruction berbeda.

### AZ0 — census writer field manager pada Entry 1

Census direct-store lengkap untuk offset manager +0xB30, +0xB2A, +0xB38, +0xB40, +0xB44 ada di:
`reports/stage1_economy/AZ0_MANAGER_WRITER_CENSUS_2026-11-02.tsv`.

Sepuluh store yang terkonfirmasi:
- +0xB30: 1 writer, PC 0x80109990.
- +0xB2A: 1 writer, PC 0x80109A98.
- +0xB38: 1 writer, PC 0x80109980.
- +0xB40: 1 writer, PC 0x80109A94 (hasil B30+B38).
- +0xB44: 6 writer, PC 0x80109A54, 0x8010A0F4, 0x8010A1C4, 0x8010A59C, 0x8010A5C8, 0x8010A658.

Semua store mempunyai base register yang dapat ditautkan ke pointer manager `[0x8013A554]` melalui rantai instruksi yang diekspor. Byte mentah/decode MIPS, 12 instruksi sebelumnya, pointer-load PC, dan offset file kandidat dicatat pada TSV. Offset file dihitung menggunakan base impor statis kandidat `0x800AD450`, jadi alamat file tetap tidak boleh disebut pemetaan runtime yang terbukti.

Batas census: semua direct instruction store yang memakai displacement tersebut dalam Entry 1; penyimpanan lewat pointer yang dihitung terlebih dahulu, alias displacement lain, dan indirect JALR tetap TIDAK TAHU.

## AZ1 — manager, tabel B30, dan nilai V petak

### H1 — B38 sama dengan floor(sum seluruh V / 2)

Status hipotesis umum: BELUM TERBUKTI; **dipatahkan pada kondisi H6 yang diamati**. Run4 `41360900093` berstatus PASS, script exit 0, dua peluncuran independen dan frame 180 serta 360. Pada empat snapshot valid, 22 tile menghasilkan sum(V)=1.270, floor(sum(V)/2)=635, sedangkan manager +0xB38=0. SHA RAM identik per frame di dua peluncuran dan Memory Card tidak berubah. Run2 `41359528784` sebelumnya menghasilkan data yang sama tetapi script exit 2 karena bug parser; status run2 tetap INCOMPLETE dan tidak dipakai sebagai bukti PASS. Falsifier untuk hubungan universal: satu kondisi valid di mana B38 berbeda dari floor(sum V/2), seperti empat snapshot H6 run4 ini. Hipotesis alternatif masih mungkin bahwa hubungan itu hanya berlaku pada state/event tertentu atau hanya subset owner/status.

### H2 — B30 mengambil nilai dari tabel mode/state dan menulis ke global 0x80070C88

Bukti statis `FUN_80012EAC`:
`idx = u8[0x80058758 + mode*0x84 + state*0x0C]`;
`table_value = u32[0x80057798 + idx*0x54 + 0x0C]`.
Fungsi yang sama memuat word row+0x0C ke a0 lalu memanggil `FUN_80012A80`; callee itu menyimpan a0 ke `0x80070C88` (store di PC `0x80012A88`). Jadi jalur tabel B30 → global 0x80070C88 terbukti statis K4.

Pada empat snapshot H6 run4 yang valid: mode=0, state byte=0, index=0, selected row=0x80057798, nilai table B30 di 0x800577A4=400. Global 0x80070C88 juga=400 di keempat snapshot. Ini adalah konfirmasi runtime H6 terhadap jalur statis, **bukan sekadar kebetulan angka**.

Manager +0xB30 aktual tetap 0 pada snapshot yang sama. Itu field berbeda di objek manager yang dipakai state machine progress; ia tidak sama dengan table B30/global 0x80070C88. Falsifier untuk hipotesis berbeda "manager+0xB30 selalu sama dengan table B30": mismatch 0 versus 400 pada kondisi H6 ini. Jalur yang mengisi manager+0xB30 belum diketahui.
### H3 — semua V petak dalam record dibaca dari helper FUN_800B770C

Hipotesis kerja K3/K4 untuk aritmetika V: nilai dasar B yang dipilih lewat halfword +0x20 dan selector +0x0B menentukan V menurut dispatch helper. Pada H6 snapshot selector +0x0B semua record=0, sehingga V=nilai dasar terpilih (rasio 1:1), sum V=1.270. Falsifier: eksekusi manual fungsi/helper pada selector 0 tidak mengembalikan nilai dasar yang sama, atau raw record/offset decode tidak cocok. Ini memverifikasi transformasi aritmetika pada selector 0, bukan seluruh selector 1–4 dalam runtime.

Tidak ada hipotesis AZ1 yang mengubah H6 menjadi bukti target murni. Bukti runtime H6 tetap dibatasi oleh identitas hybrid SHA dan state/frame yang dicapture.

## Hipotesis pemicu dan biaya

AZ2 dan AZ3 memiliki hipotesis terpisah beserta falsifier di `AZ2_AZ3_STATIC_REGISTER_FLOW_2026-11-02.md`: jalur transfer saldo memerlukan caller bit 0x20 + manager state7; nama event gameplay tetap TIDAK TAHU. Untuk biaya build/upgrade tidak ada a1=Q(i)-nilai di 14 direct setter callsites AX2; rumus dan sumber harga aktual tetap TIDAK TAHU.

Nol hit tidak digunakan untuk menyimpulkan ketiadaan fitur. Akses berbasis pointer terhitung/indirect JALR yang tidak masuk census langsung tetap TIDAK TAHU.
