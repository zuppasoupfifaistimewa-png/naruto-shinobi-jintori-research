# Langkah 5 — perbandingan dekompilasi Ghidra dan m2c (27 Oktober 2026)

Status: **SELESAI untuk perbandingan statis empat caller RNG pada executable utama**. Ini bukan pemulihan kode sumber asli dan bukan verifikasi runtime.

## Provenance dan reproduksi

- GitHub Actions [run #40449144521](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40449144521), commit sumber `62a4c114b7ac7a55ae9eb6d91bc4c9bfaef1c2ef`: **success**, semua langkah job berhasil.
- Artefak sumber: [step5-ghidra-m2c-same-functions, artifact #12710000931](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40449144521/artifacts/12710000931); SHA-256 ZIP `b2fdb6dc3213137e98e0ed298402e1d4b02198ed5310f264780bd8e965246b08`; pada saat audit belum kedaluwarsa.
- Executable input: `SLPS_035.53`, 385.024 byte, SHA-256 `a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569`.
- Text range: file offset `0x800`, base `0x80010000`, size `0x5D800`; Ghidra 12.2, `MIPS:LE:32:default`. m2c commit `c632946b8cfbe8fce442b522dba92dfa72f1f317`; spimdisasm 1.42.4; backend `mips-ido-c` hanya pemilih backend, bukan bukti compiler asli game.
- Hasil akhir: 4 fungsi diminta, 4 keluaran Ghidra C dan 4 keluaran m2c C ada; exit code m2c 0 untuk tiap fungsi; token alamat RNG `0x80035D78` hadir pada kedua keluaran tiap fungsi. Call-token sets yang dibandingkan cocok per fungsi sebagaimana tercantum di bawah.
- Kebijakan artefak: hanya teks diunggah; executable, disc image, dan project sementara dihapus dari runner. Tidak ada emulator/gameplay dijalankan dan tidak ada input gameplay dikirim.

## Hasil per fungsi

| Entry | Ukuran fungsi Ghidra | Baris Ghidra C / m2c C | Shared call tokens (alamat heksadesimal tanpa awalan 0x) | Arti statis yang didukung |
|---|---:|---:|---|---|
| `0x80015ADC` `FUN_80015adc` | 160 byte | 22 / 20 | `800154d4, 800158d8, 800159bc, 80015adc, 80035d78` | Membuat indeks/offset terbatas dengan bantuan helper dan RNG, lalu memanggil helper sisip daftar. Makna data yang disisipkan belum diketahui. |
| `0x80015B7C` `FUN_80015b7c` | 240 byte | 33 / 32 | `80015b7c, 80035d78` | Menukar elemen byte pada tabel berbasis jumlah elemen dan nilai RNG; konsisten dengan shuffle/permutasi byte. Tujuan tabel belum diketahui. |
| `0x8001A328` `FUN_8001a328` | 376 byte | 65 / 61 | `80016c68, 8001a328, 80035d48, 80035d78` | Membentuk daftar kandidat berdasarkan uji kode `0x7F..0x86`, lalu mengambil satu kandidat dengan RNG; hasil ditulis ke `DAT_80089DA9`. Arti kode belum diketahui. |
| `0x80020BF4` `FUN_80020bf4` | 156 byte | 25 / 24 | `80018300, 80018468, 80020bf4, 80020d48, 80035d78` | Menginisialisasi struktur bila pointer valid dan field awal belum 1, menulis hasil RNG modulo `0x1000` ke field `param_1[0xD]`, lalu memanggil helper lanjutan. Hubungan gameplay belum terbukti. |

Kecocokan struktur/call token membantu memeriksa bahwa kedua decompiler membahas entry dan pemanggil yang sama. Perbedaan representasi C adalah wajar. Hasil ini **tidak** membuktikan bahwa salah satu keluaran identik dengan source code asli atau menetapkan semantik gameplay.

## Keluaran dekompilasi yang disimpan permanen

Kode berikut disalin dari artefak text-only run #40449144521; nama variabel, tipe, dan pseudocode adalah hasil decompiler otomatis. Jangan menganggapnya source code asli.

### `FUN_80015adc` — Ghidra

```c
undefined4 FUN_80015adc(undefined4 param_1,uint param_2)
{
  uint uVar1;
  undefined4 uVar2;
  int iVar3;
  uint uVar4;
  uVar1 = FUN_800154d4();
  uVar2 = 0;
  if ((param_2 & 0xff) < uVar1) {
    uVar1 = FUN_800158d8(param_1);
    iVar3 = FUN_80035d78();
    uVar4 = FUN_800158d8(param_1);
    uVar4 = uVar4 >> 1 & 0xff;
    if (uVar4 == 0) { trap(7); }
    uVar2 = FUN_800159bc(param_1,(uVar1 >> 1 & 0xff) + iVar3 % (int)uVar4 & 0xffff,param_2 & 0xff);
  }
  return uVar2;
}
```

### `FUN_80015adc` — m2c

```c
u32 func_800154D4();                                /* static */
u32 func_800158D8(s32);                             /* static */
s32 func_800159BC(s32, s32, u32);                   /* static */
s32 func_80035D78();                                /* static */
s32 func_80015ADC(s32 arg0, s32 arg1) {
    s32 temp_s1;
    s32 var_v0;
    u32 temp_s0;
    u32 temp_s3;
    temp_s3 = arg1 & 0xFF;
    var_v0 = 0;
    if (temp_s3 < func_800154D4()) {
        temp_s0 = func_800158D8(arg0);
        temp_s1 = func_80035D78();
        var_v0 = func_800159BC(arg0, (((temp_s0 >> 1) & 0xFF) + (temp_s1 % (s32) ((func_800158D8(arg0) >> 1) & 0xFF))) & 0xFFFF, temp_s3);
    }
    return var_v0;
}
```

### `FUN_80015b7c` — Ghidra

```c
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
undefined4 FUN_80015b7c(void) {
  undefined1 uVar1;
  uint uVar2;
  int iVar3;
  uint uVar4;
  int iVar5;
  uint uVar6;
  uVar6 = (uint)_DAT_80070d02;
  iVar5 = 0;
  if (uVar6 != 0) {
    do {
      uVar2 = (uint)_DAT_80070d02;
      if (uVar2 == 0) { trap(7); }
      iVar3 = FUN_80035d78();
      uVar4 = (uint)_DAT_80070d02;
      if (uVar4 == 0) { trap(7); }
      uVar1 = (&DAT_80070d0a)[iVar5 % (int)uVar2];
      (&DAT_80070d0a)[iVar5 % (int)uVar2] = (&DAT_80070d0a)[iVar3 % (int)uVar4];
      iVar5 = iVar5 + 1;
      (&DAT_80070d0a)[iVar3 % (int)uVar4] = uVar1;
    } while (iVar5 < (int)(uVar6 << 2));
  }
  return 1;
}
```

### `FUN_80015b7c` — m2c

```c
s32 func_80035D78(u8 *);                            /* static */
extern u16 D_80070D02;
extern ? D_80070D0A;
s32 func_80015B7C(void) {
    s32 temp_s0;
    s32 temp_s2;
    s32 temp_s4;
    s32 var_s1;
    u16 *temp_s3;
    u8 *temp_s0_2;
    u8 *var_a0;
    u8 temp_v1;
    var_a0 = NULL;
    temp_s4 = D_80070D02 * 4;
    var_s1 = 0;
    if (temp_s4 != 0) {
        temp_s3 = &(&D_80070D02)[0];
        temp_s2 = 0 << 6;
        do {
            temp_s0 = var_s1 % (s32) *temp_s3;
            temp_s0_2 = temp_s0 + temp_s2 + &D_80070D0A;
            temp_v1 = *temp_s0_2;
            var_a0 = (func_80035D78(var_a0) % (s32) *temp_s3) + temp_s2 + &D_80070D0A;
            *temp_s0_2 = *var_a0;
            var_s1 += 1;
            *var_a0 = temp_v1;
        } while (var_s1 < temp_s4);
    }
    return 1;
}
```

### `FUN_8001a328` — Ghidra

```c
void FUN_8001a328(void) {
  int iVar1;
  uint uVar2;
  uint uVar3;
  undefined1 local_18 [16];
  FUN_80035d48(local_18,0,0xd);
  uVar3 = 1;
  local_18[0] = 0;
  iVar1 = FUN_80016c68(0x7f);
  if (iVar1 != 0) { uVar3 = 2; local_18[1] = 1; }
  iVar1 = FUN_80016c68(0x80);
  uVar2 = uVar3;
  if (iVar1 != 0) { uVar2 = uVar3 + 1; local_18[uVar3] = 2; }
  iVar1 = FUN_80016c68(0x81);
  uVar3 = uVar2;
  if (iVar1 != 0) { uVar3 = uVar2 + 1; local_18[uVar2] = 3; }
  iVar1 = FUN_80016c68(0x82);
  uVar2 = uVar3;
  if (iVar1 != 0) { uVar2 = uVar3 + 1; local_18[uVar3] = 4; }
  iVar1 = FUN_80016c68(0x83);
  uVar3 = uVar2;
  if (iVar1 != 0) { uVar3 = uVar2 + 1; local_18[uVar2] = 5; }
  iVar1 = FUN_80016c68(0x84);
  uVar2 = uVar3;
  if (iVar1 != 0) { uVar2 = uVar3 + 1; local_18[uVar3] = 8; }
  iVar1 = FUN_80016c68(0x85);
  uVar3 = uVar2;
  if (iVar1 != 0) { uVar3 = uVar2 + 1; local_18[uVar2] = 9; }
  iVar1 = FUN_80016c68(0x86);
  uVar2 = uVar3;
  if (iVar1 != 0) { uVar2 = uVar3 + 1 & 0xff; local_18[uVar3] = 0xb; }
  iVar1 = FUN_80035d78();
  if (uVar2 == 0) { trap(7); }
  DAT_80089da9 = local_18[iVar1 % (int)uVar2];
  return;
}
```

### `FUN_8001a328` — m2c

```c
s32 func_80016C68(?);                               /* static */
? func_80035D48(s8 *, ?, ?);                        /* static */
s32 func_80035D78();                                /* static */
extern u8 D_80089DA9;
void func_8001A328(void) {
    s8 sp11;
    s8 sp10;
    s32 temp_v1;
    s32 temp_v1_2;
    s32 temp_v1_3;
    s32 temp_v1_4;
    s32 temp_v1_5;
    s32 temp_v1_6;
    s32 temp_v1_7;
    s32 var_s0;
    func_80035D48(&sp10, 0, 0xD);
    var_s0 = 1;
    sp10 = 0;
    if (func_80016C68(0x7F) != 0) { var_s0 = 2; sp11 = 1; }
    temp_v1 = var_s0;
    if (func_80016C68(0x80) != 0) { var_s0 = (var_s0 + 1) & 0xFF; (sp + temp_v1)->unk10 = 2; }
    temp_v1_2 = var_s0;
    if (func_80016C68(0x81) != 0) { var_s0 = (var_s0 + 1) & 0xFF; (sp + temp_v1_2)->unk10 = 3; }
    temp_v1_3 = var_s0;
    if (func_80016C68(0x82) != 0) { var_s0 = (var_s0 + 1) & 0xFF; (sp + temp_v1_3)->unk10 = 4; }
    temp_v1_4 = var_s0;
    if (func_80016C68(0x83) != 0) { var_s0 = (var_s0 + 1) & 0xFF; (sp + temp_v1_4)->unk10 = 5; }
    temp_v1_5 = var_s0;
    if (func_80016C68(0x84) != 0) { var_s0 = (var_s0 + 1) & 0xFF; (sp + temp_v1_5)->unk10 = 8; }
    temp_v1_6 = var_s0;
    if (func_80016C68(0x85) != 0) { var_s0 = (var_s0 + 1) & 0xFF; (sp + temp_v1_6)->unk10 = 9; }
    temp_v1_7 = var_s0;
    if (func_80016C68(0x86) != 0) { var_s0 = (var_s0 + 1) & 0xFF; (sp + temp_v1_7)->unk10 = 0xB; }
    D_80089DA9 = (sp + (func_80035D78() % var_s0))->unk10;
}
```

### `FUN_80020bf4` — Ghidra

```c
undefined4 FUN_80020bf4(int *param_1) {
  undefined4 uVar1;
  int iVar2;
  int iVar3;
  if ((param_1 == (int *)0x0) || (*param_1 == 1)) {
    uVar1 = 0;
  } else {
    *param_1 = 1;
    iVar2 = FUN_80035d78();
    iVar3 = iVar2;
    if (iVar2 < 0) { iVar3 = iVar2 + 0xfff; }
    param_1[0xd] = iVar2 + (iVar3 >> 0xc) * -0x1000;
    FUN_80020d48(param_1,0x1000);
    FUN_80018300(0x4800,2,3,0,0);
    FUN_80018468(0,0xb4);
    uVar1 = 1;
  }
  return uVar1;
}
```

### `FUN_80020bf4` — m2c

```c
? func_80018300(?, ?, ?, ?, s32);                   /* static */
? func_80018468(?, ?);                              /* static */
? func_80020D48(void *, ?);                         /* static */
s32 func_80035D78();
s32 func_80020bf4(void *arg0) {
    s32 temp_v0;
    s32 var_v0;
    if ((arg0 == NULL) || (arg0->unk0 == 1)) { return 0; }
    arg0->unk0 = 1;
    temp_v0 = func_80035D78();
    var_v0 = temp_v0 >> 0xC;
    if (temp_v0 < 0) { var_v0 = (s32) (temp_v0 + 0xFFF) >> 0xC; }
    arg0->unk34 = (s32) (temp_v0 - (var_v0 << 0xC));
    func_80020D48(arg0, 0x1000);
    func_80018300(0x4800, 2, 3, 0, 0);
    func_80018468(0, 0xB4);
    return 1;
}
```

## Batas interpretasi

- Ghidra/m2c adalah dua dekompiler dari rentang biner yang sama; dua output serupa menambah keyakinan tentang struktur kontrol, tetapi tidak dapat menegaskan bahwa kode C asli direkonstruksi sempurna.
- Kode tidak menunjukkan identitas RNG caller sebagai roulette, battle, AI, atau hadiah tanpa telusur data/caller tambahan.
- Tidak ada tes Unicorn/isolated MIPS atau uji runtime di laporan ini.
