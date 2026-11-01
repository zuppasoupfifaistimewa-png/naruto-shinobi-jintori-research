# AZ0–AZ1 — hipotesis, falsifier, dan hasil uji
Tanggal: 2 November 2026
Bukti statis maksimum K4; runtime pada H6 selalu dilabel HIBRIDA, bukan target murni.

## AZ0 — identitas writer dan pemetaan Entry 1

- H1 (K2): tiga PC WRITER_CONFIRMED (0x80109980, 0x80109990, 0x80109A98) berada pada Entry 1 dengan offset file yang dihitung memakai base statis kandidat 0x800AD450. Falsifier: ekstraksi ulang Entry 1 menunjukkan byte pada offset hasil rumus tidak cocok dengan 38 0B 44 AC / 30 0B 44 AC / 2A 0B 80 A0, atau mapping base terbukti berbeda.
- H2 (K3): instruksi tersebut menulis field manager +0xB38, +0xB30, dan +0xB2A karena pointer manager diload melalui slot 0x8013A554; setiap byte raw cocok dengan decode MIPS. Falsifier: pembacaan offset/basis Entry1 alternatif atau decode independen membuktikan base register bukan manager atau byte instruction berbeda.

## AZ1 — manager, tabel B30, dan nilai V petak

### H1 — B38 sama dengan floor(sum seluruh V / 2)

Status hipotesis umum: BELUM TERBUKTI; **dipatahkan pada kondisi H6 yang diamati**. Run4 `41360900093` berstatus PASS, script exit 0, dua peluncuran independen dan frame 180 serta 360. Pada empat snapshot valid, 22 tile menghasilkan sum(V)=1.270, floor(sum(V)/2)=635, sedangkan manager +0xB38=0. SHA RAM identik per frame di dua peluncuran dan Memory Card tidak berubah. Run2 `41359528784` sebelumnya menghasilkan data yang sama tetapi script exit 2 karena bug parser; status run2 tetap INCOMPLETE dan tidak dipakai sebagai bukti PASS. Falsifier untuk hubungan universal: satu kondisi valid di mana B38 berbeda dari floor(sum V/2), seperti empat snapshot H6 run4 ini. Hipotesis alternatif masih mungkin bahwa hubungan itu hanya berlaku pada state/event tertentu atau hanya subset owner/status.

### H2 — B30 mengambil nilai dari tabel yang dipilih mode/state

Bukti statis FUN_80012EAC: 
`idx = u8[0x80058758 + mode*0x84 + state*0x0C]`;
`table_value = u32[0x80057798 + idx*0x54 + 0x0C]` (alamat row-0 adalah 0x800577A4).
Pada empat snapshot H6 run4 yang valid: mode word [0x80070734]=0, state byte [0x8007073C]=0, index byte di 0x80058758=0, selected row base=0x80057798, nilai tabel di 0x800577A4=400. Manager +0xB30 aktual tetap 0. Ini membuktikan lookup baris dan nilainya untuk mode/state yang tertangkap, tetapi **tidak** membuktikan bahwa nilai tabel 400 sudah disalin ke manager B30 pada state ini. Falsifier untuk hipotesis bahwa manager B30 selalu sama dengan lookup: mismatch aktual 0 versus 400 pada snapshot H6. Untuk membuktikan jalur transfer nilai tabel→manager, perlu melacak caller/argumen setter manager +0xB30 atau snapshot lain ketika manager benar-benar diinisialisasi.

### H3 — semua V petak dalam record dibaca dari helper FUN_800B770C

Hipotesis kerja K3/K4 untuk aritmetika V: nilai dasar B yang dipilih lewat halfword +0x20 dan selector +0x0B menentukan V menurut dispatch helper. Pada H6 snapshot selector +0x0B semua record=0, sehingga V=nilai dasar terpilih (rasio 1:1), sum V=1.270. Falsifier: eksekusi manual fungsi/helper pada selector 0 tidak mengembalikan nilai dasar yang sama, atau raw record/offset decode tidak cocok. Ini memverifikasi transformasi aritmetika pada selector 0, bukan seluruh selector 1–4 dalam runtime.

Tidak ada hipotesis AZ1 yang mengubah H6 menjadi bukti target murni. Bukti runtime H6 tetap dibatasi oleh identitas hybrid SHA dan state/frame yang dicapture.

## Hipotesis pemicu dan biaya

AZ2 dan AZ3 memiliki hipotesis terpisah beserta falsifier di `AZ2_AZ3_STATIC_REGISTER_FLOW_2026-11-02.md`: jalur transfer saldo memerlukan caller bit 0x20 + manager state7; nama event gameplay tetap TIDAK TAHU. Untuk biaya build/upgrade tidak ada a1=Q(i)-nilai di 14 direct setter callsites AX2; rumus dan sumber harga aktual tetap TIDAK TAHU.

Nol hit tidak digunakan untuk menyimpulkan ketiadaan fitur. Akses berbasis pointer terhitung/indirect JALR yang tidak masuk census langsung tetap TIDAK TAHU.
