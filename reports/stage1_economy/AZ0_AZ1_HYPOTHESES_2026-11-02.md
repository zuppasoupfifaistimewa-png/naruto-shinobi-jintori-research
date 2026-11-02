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
### H3 — nilai V petak dihitung oleh FUN_800B770C

Dispatch statis K4 dari `FUN_800B770C` memeriksa selector record +0x0B. B dipilih dari halfword record `+0x10 + ((u16(record+0x20)>>7)&0x1E)`. Rumus lengkap:
- selector 0: V=B
- selector 1: V=floor(12B/10)
- selector 2: V=floor(15B/10)
- selector 3: V=floor(18B/10)
- selector 4: V=2B
- selector lain: V=0

Bukti decompile + raw body lengkap (0x800B770C–0x800B78E0) tersimpan pada AQ1 `entry1-helper-function-detail.txt`; tabel rumus terpisah ada di `AZ1_V_SELECTOR_FORMULAS_2026-11-02.tsv`. Pada H6 run4, selector semua 22 record adalah 0. Karena itu 88/88 V runtime cocok dengan B (empat snapshots), sum V=1.270 pada masing-masing snapshot. Selector 1–4 sudah terbukti statis, tetapi runtime H6 belum mengandung record dengan selector tersebut; runtime untuk selector 1–4 = TIDAK TAHU.

Tidak ada hipotesis AZ1 yang mengubah H6 menjadi bukti target murni. Bukti runtime H6 tetap dibatasi oleh identitas hybrid SHA dan state/frame yang dicapture.

## Hipotesis pemicu dan biaya

AZ2 dan AZ3 memiliki hipotesis terpisah beserta falsifier di `AZ2_AZ3_STATIC_REGISTER_FLOW_2026-11-02.md`: jalur transfer saldo memerlukan caller bit 0x20 + manager state7; nama event gameplay tetap TIDAK TAHU. Untuk biaya build/upgrade, run 41367221886 mengidentifikasi 16 direct JAL tervalidasi ke setter (14 Entry1 + 2 MAIN_EXE). Tidak ada a1=Q(i)-cost di 16 site yang diuji; site 0x80012DD4 di FUN_80012C70 mengirim DAT_80070C80 (return FUN_80012A44()) ke setter untuk indeks pemain loop; sumber global DAT_80070C80 belum diketahui. Site 0x80013170 mengambil selected table row+0x04. Indirect JALR dan overlay di luar dua image tetap TIDAK TAHU; rumus dan sumber harga aktual tetap TIDAK TAHU.

### AZ3 — global C80 adalah sumber nilai awal field chakra participant

Static K4: FUN_80012780 dan FUN_80012EAC adalah dua writer langsung ke global 0x80070C80, masing-masing menyalin word dari tabel/config +0x04. FUN_80012A44 membaca global itu, lalu FUN_80012C70 mengirim nilai tersebut ke setter FUN_8001387C untuk setiap participant loop index; setter menyimpannya ke record +0x18. Karena +0x18 adalah field chakra player, jalur ini adalah inisialisasi nilai awal chakra participant, bukan debit biaya.

Falsifier: producer lain menimpa C80 sesudah loop dan membuktikan field +0x18 bukan chakra atau caller setter bukan setup participant. Identitas detail table field +0x04 dan runtime value C80 masih TIDAK TAHU. Harga build/upgrade tidak disimpulkan dari jalur seed ini.
Nol hit tidak digunakan untuk menyimpulkan ketiadaan fitur. Akses berbasis pointer terhitung/indirect JALR yang tidak masuk census langsung tetap TIDAK TAHU.
