# AW2 — konstanta, tabel, Shift-JIS dan font/tile search

Input terverifikasi SHA-256. Entry 1 memakai base statis kandidat 0x800AD450; runtime mapping belum diverifikasi.

| Input | Bytes | SHA-256 |
|---|---:|---|
| SLPS_035.53 | 385024 | a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569 |
| DATA.BIN_ENTRY0 | 110536 | 56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4 |
| DATA.BIN_ENTRY1 | 596412 | 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a |

## Kemunculan angka 50/60/100/150 (LE u8/u16/u32)

Kemunculan byte mentah hanya kandidat. Xref dan konteks instruksi diperlukan sebelum label ekonomi.

| Input | Nilai | Lebar | Jumlah | Offset/VA awal (maks 20) |
|---|---:|---:|---:|---|
| SLPS_035.53 | 50 | 8 | 454 | 0x841/0x80010041; 0xCE8/0x800104E8; 0xEC2/0x800106C2; 0xEDE/0x800106DE; 0x10E2/0x800108E2; 0x10F6/0x800108F6; 0x11F9/0x800109F9; 0x1464/0x80010C64; 0x1469/0x80010C69; 0x146E/0x80010C6E; 0x1643/0x80010E43; 0x1648/0x80010E48; 0x16D3/0x80010ED3; 0x16DA/0x80010EDA; 0x16DD/0x80010EDD; 0x1772/0x80010F72; 0x182C/0x8001102C; 0x1832/0x80011032; 0x1834/0x80011034; 0x193A/0x8001113A |
| SLPS_035.53 | 50 | 16 | 100 | 0x193A/0x8001113A; 0x1A2D/0x8001122D; 0x4E54/0x80014654; 0x4FB8/0x800147B8; 0x85FC/0x80017DFC; 0x8748/0x80017F48; 0x8B2C/0x8001832C; 0xB484/0x8001AC84; 0xB904/0x8001B104; 0xC084/0x8001B884; 0xC0C7/0x8001B8C7; 0xC680/0x8001BE80; 0xD060/0x8001C860; 0xD468/0x8001CC68; 0xD828/0x8001D028; 0xD9C0/0x8001D1C0; 0xDA2C/0x8001D22C; 0xDAF0/0x8001D2F0; 0xDD48/0x8001D548; 0xDD90/0x8001D590 |
| SLPS_035.53 | 50 | 32 | 6 | 0x46784/0x80055F84; 0x4717C/0x8005697C; 0x476B8/0x80056EB8; 0x47820/0x80057020; 0x47E9C/0x8005769C; 0x482A0/0x80057AA0 |
| SLPS_035.53 | 60 | 8 | 4458 | 0xE05/0x80010605; 0x11D0/0x800109D0; 0x1C04/0x80011404; 0x1C34/0x80011434; 0x1C4B/0x8001144B; 0x1C53/0x80011453; 0x1C83/0x80011483; 0x1C93/0x80011493; 0x1C9B/0x8001149B; 0x1CAB/0x800114AB; 0x1CC3/0x800114C3; 0x1CCB/0x800114CB; 0x1CDF/0x800114DF; 0x1D17/0x80011517; 0x1D77/0x80011577; 0x1DAB/0x800115AB; 0x1DD3/0x800115D3; 0x1E7B/0x8001167B; 0x2097/0x80011897; 0x20BF/0x800118BF |
| SLPS_035.53 | 60 | 16 | 376 | 0x2630/0x80011E30; 0x2700/0x80011F00; 0x2CAF/0x800124AF; 0x2D9B/0x8001259B; 0x3474/0x80012C74; 0x3684/0x80012E84; 0x394F/0x8001314F; 0x4DCF/0x800145CF; 0x723F/0x80016A3F; 0x72FB/0x80016AFB; 0x7AF0/0x800172F0; 0x7B58/0x80017358; 0x7B9C/0x8001739C; 0x8567/0x80017D67; 0x8647/0x80017E47; 0x868B/0x80017E8B; 0x90D3/0x800188D3; 0x943B/0x80018C3B; 0x949B/0x80018C9B; 0x9620/0x80018E20 |
| SLPS_035.53 | 60 | 32 | 3 | 0x477D0/0x80056FD0; 0x47A18/0x80057218; 0x5D92C/0x8006D12C |
| SLPS_035.53 | 100 | 8 | 896 | 0xE58/0x80010658; 0xEA0/0x800106A0; 0xECD/0x800106CD; 0xEF1/0x800106F1; 0xEF5/0x800106F5; 0xEF9/0x800106F9; 0xEFD/0x800106FD; 0xF01/0x80010701; 0xF05/0x80010705; 0xF09/0x80010709; 0xF0D/0x8001070D; 0xF11/0x80010711; 0xF15/0x80010715; 0xF19/0x80010719; 0xF1D/0x8001071D; 0xF21/0x80010721; 0xF25/0x80010725; 0xF29/0x80010729; 0xF2D/0x8001072D; 0xF31/0x80010731 |
| SLPS_035.53 | 100 | 16 | 328 | 0x158A/0x80010D8A; 0x1595/0x80010D95; 0x15CE/0x80010DCE; 0x20A2/0x800118A2; 0x21ED/0x800119ED; 0x233D/0x80011B3D; 0x234D/0x80011B4D; 0x235D/0x80011B5D; 0x2375/0x80011B75; 0x272E/0x80011F2E; 0x28C2/0x800120C2; 0x2D82/0x80012582; 0x36F6/0x80012EF6; 0x5746/0x80014F46; 0x65C6/0x80015DC6; 0x6726/0x80015F26; 0x695A/0x8001615A; 0x8BC6/0x800183C6; 0x94ED/0x80018CED; 0x9665/0x80018E65 |
| SLPS_035.53 | 100 | 32 | 30 | 0x5746/0x80014F46; 0x65C6/0x80015DC6; 0x6726/0x80015F26; 0x695A/0x8001615A; 0x8BC6/0x800183C6; 0xA5E2/0x80019DE2; 0xDF3E/0x8001D73E; 0xDF56/0x8001D756; 0x10136/0x8001F936; 0x14DA6/0x800245A6; 0x14F0E/0x8002470E; 0x152CE/0x80024ACE; 0x154CA/0x80024CCA; 0x15AAA/0x800252AA; 0x193BE/0x80028BBE; 0x1A2D6/0x80029AD6; 0x1C31E/0x8002BB1E; 0x2007A/0x8002F87A; 0x202E6/0x8002FAE6; 0x2FFEE/0x8003F7EE |
| SLPS_035.53 | 150 | 8 | 324 | 0x34FC/0x80012CFC; 0x37CE/0x80012FCE; 0x3803/0x80013003; 0x3896/0x80013096; 0x38D0/0x800130D0; 0x63D7/0x80015BD7; 0x63FB/0x80015BFB; 0x7AC0/0x800172C0; 0xA244/0x80019A44; 0xB378/0x8001AB78; 0xB4FF/0x8001ACFF; 0xB62B/0x8001AE2B; 0xB66B/0x8001AE6B; 0xB67F/0x8001AE7F; 0xB697/0x8001AE97; 0xB6AB/0x8001AEAB; 0xB6C7/0x8001AEC7; 0xB76B/0x8001AF6B; 0xB77F/0x8001AF7F; 0xB7AB/0x8001AFAB |
| SLPS_035.53 | 150 | 16 | 149 | 0x3803/0x80013003; 0x63D7/0x80015BD7; 0x63FB/0x80015BFB; 0xB4FF/0x8001ACFF; 0xB66B/0x8001AE6B; 0xB697/0x8001AE97; 0xB6AB/0x8001AEAB; 0xB6C7/0x8001AEC7; 0xB76B/0x8001AF6B; 0xB77F/0x8001AF7F; 0xB7AB/0x8001AFAB; 0xB7EB/0x8001AFEB; 0xB7FB/0x8001AFFB; 0xB81B/0x8001B01B; 0xB85B/0x8001B05B; 0xB877/0x8001B077; 0xB99B/0x8001B19B; 0xB9A7/0x8001B1A7; 0xB9B7/0x8001B1B7; 0xB9EF/0x8001B1EF |
| SLPS_035.53 | 150 | 32 | 111 | 0x3803/0x80013003; 0x63D7/0x80015BD7; 0x63FB/0x80015BFB; 0xB4FF/0x8001ACFF; 0xB66B/0x8001AE6B; 0xB697/0x8001AE97; 0xB6AB/0x8001AEAB; 0xB6C7/0x8001AEC7; 0xB76B/0x8001AF6B; 0xB77F/0x8001AF7F; 0xB7AB/0x8001AFAB; 0xB7EB/0x8001AFEB; 0xB7FB/0x8001AFFB; 0xB81B/0x8001B01B; 0xB85B/0x8001B05B; 0xB877/0x8001B077; 0xB99B/0x8001B19B; 0xB9A7/0x8001B1A7; 0xB9B7/0x8001B1B7; 0xB9EF/0x8001B1EF |
| DATA.BIN_ENTRY0 | 50 | 8 | 120 | 0x48F/TIDAK TAHU (entry0 runtime base); 0x4AF/TIDAK TAHU (entry0 runtime base); 0x517/TIDAK TAHU (entry0 runtime base); 0x537/TIDAK TAHU (entry0 runtime base); 0x173C/TIDAK TAHU (entry0 runtime base); 0x3E1C/TIDAK TAHU (entry0 runtime base); 0x4973/TIDAK TAHU (entry0 runtime base); 0x4AF3/TIDAK TAHU (entry0 runtime base); 0x4DE0/TIDAK TAHU (entry0 runtime base); 0x504C/TIDAK TAHU (entry0 runtime base); 0x54BC/TIDAK TAHU (entry0 runtime base); 0x5527/TIDAK TAHU (entry0 runtime base); 0x5554/TIDAK TAHU (entry0 runtime base); 0x55AB/TIDAK TAHU (entry0 runtime base); 0x56E4/TIDAK TAHU (entry0 runtime base); 0x5A14/TIDAK TAHU (entry0 runtime base); 0x5A6F/TIDAK TAHU (entry0 runtime base); 0x5FC3/TIDAK TAHU (entry0 runtime base); 0x5FD2/TIDAK TAHU (entry0 runtime base); 0x604B/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 50 | 16 | 46 | 0x3E1C/TIDAK TAHU (entry0 runtime base); 0x4DE0/TIDAK TAHU (entry0 runtime base); 0x504C/TIDAK TAHU (entry0 runtime base); 0x54BC/TIDAK TAHU (entry0 runtime base); 0x5554/TIDAK TAHU (entry0 runtime base); 0x56E4/TIDAK TAHU (entry0 runtime base); 0x5A14/TIDAK TAHU (entry0 runtime base); 0x9214/TIDAK TAHU (entry0 runtime base); 0x927C/TIDAK TAHU (entry0 runtime base); 0x99D4/TIDAK TAHU (entry0 runtime base); 0x9A38/TIDAK TAHU (entry0 runtime base); 0x9AE4/TIDAK TAHU (entry0 runtime base); 0x9B58/TIDAK TAHU (entry0 runtime base); 0x9BAC/TIDAK TAHU (entry0 runtime base); 0x9C28/TIDAK TAHU (entry0 runtime base); 0xA4BC/TIDAK TAHU (entry0 runtime base); 0xA73B/TIDAK TAHU (entry0 runtime base); 0xAEC4/TIDAK TAHU (entry0 runtime base); 0xD49C/TIDAK TAHU (entry0 runtime base); 0xD6C0/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 50 | 32 | 0 | none |
| DATA.BIN_ENTRY0 | 60 | 8 | 1000 | 0x178/TIDAK TAHU (entry0 runtime base); 0x21C/TIDAK TAHU (entry0 runtime base); 0x307/TIDAK TAHU (entry0 runtime base); 0x323/TIDAK TAHU (entry0 runtime base); 0x3B3/TIDAK TAHU (entry0 runtime base); 0x407/TIDAK TAHU (entry0 runtime base); 0x40B/TIDAK TAHU (entry0 runtime base); 0x46B/TIDAK TAHU (entry0 runtime base); 0x4DB/TIDAK TAHU (entry0 runtime base); 0x573/TIDAK TAHU (entry0 runtime base); 0x60F/TIDAK TAHU (entry0 runtime base); 0x647/TIDAK TAHU (entry0 runtime base); 0x69F/TIDAK TAHU (entry0 runtime base); 0x6BB/TIDAK TAHU (entry0 runtime base); 0x6DB/TIDAK TAHU (entry0 runtime base); 0x704/TIDAK TAHU (entry0 runtime base); 0x70F/TIDAK TAHU (entry0 runtime base); 0x727/TIDAK TAHU (entry0 runtime base); 0x73F/TIDAK TAHU (entry0 runtime base); 0x77F/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 60 | 16 | 119 | 0x914/TIDAK TAHU (entry0 runtime base); 0xF1F/TIDAK TAHU (entry0 runtime base); 0x1133/TIDAK TAHU (entry0 runtime base); 0x181C/TIDAK TAHU (entry0 runtime base); 0x1C10/TIDAK TAHU (entry0 runtime base); 0x1ECC/TIDAK TAHU (entry0 runtime base); 0x1FA4/TIDAK TAHU (entry0 runtime base); 0x232C/TIDAK TAHU (entry0 runtime base); 0x2593/TIDAK TAHU (entry0 runtime base); 0x2778/TIDAK TAHU (entry0 runtime base); 0x2868/TIDAK TAHU (entry0 runtime base); 0x2894/TIDAK TAHU (entry0 runtime base); 0x2E04/TIDAK TAHU (entry0 runtime base); 0x336C/TIDAK TAHU (entry0 runtime base); 0x34C0/TIDAK TAHU (entry0 runtime base); 0x38C4/TIDAK TAHU (entry0 runtime base); 0x46C0/TIDAK TAHU (entry0 runtime base); 0x4890/TIDAK TAHU (entry0 runtime base); 0x4B08/TIDAK TAHU (entry0 runtime base); 0x5038/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 60 | 32 | 3 | 0xF1F/TIDAK TAHU (entry0 runtime base); 0x1133/TIDAK TAHU (entry0 runtime base); 0x196D8/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 100 | 8 | 308 | 0x88/TIDAK TAHU (entry0 runtime base); 0x204/TIDAK TAHU (entry0 runtime base); 0x47D/TIDAK TAHU (entry0 runtime base); 0x50D/TIDAK TAHU (entry0 runtime base); 0x84D/TIDAK TAHU (entry0 runtime base); 0xC32/TIDAK TAHU (entry0 runtime base); 0xC42/TIDAK TAHU (entry0 runtime base); 0xC52/TIDAK TAHU (entry0 runtime base); 0xD80/TIDAK TAHU (entry0 runtime base); 0xE6A/TIDAK TAHU (entry0 runtime base); 0xE7A/TIDAK TAHU (entry0 runtime base); 0xE8A/TIDAK TAHU (entry0 runtime base); 0x106E/TIDAK TAHU (entry0 runtime base); 0x107E/TIDAK TAHU (entry0 runtime base); 0x108E/TIDAK TAHU (entry0 runtime base); 0x1276/TIDAK TAHU (entry0 runtime base); 0x1286/TIDAK TAHU (entry0 runtime base); 0x1296/TIDAK TAHU (entry0 runtime base); 0x1506/TIDAK TAHU (entry0 runtime base); 0x166E/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 100 | 16 | 145 | 0x47D/TIDAK TAHU (entry0 runtime base); 0x50D/TIDAK TAHU (entry0 runtime base); 0x84D/TIDAK TAHU (entry0 runtime base); 0xC32/TIDAK TAHU (entry0 runtime base); 0xC42/TIDAK TAHU (entry0 runtime base); 0xC52/TIDAK TAHU (entry0 runtime base); 0xE6A/TIDAK TAHU (entry0 runtime base); 0xE7A/TIDAK TAHU (entry0 runtime base); 0xE8A/TIDAK TAHU (entry0 runtime base); 0x106E/TIDAK TAHU (entry0 runtime base); 0x107E/TIDAK TAHU (entry0 runtime base); 0x108E/TIDAK TAHU (entry0 runtime base); 0x1276/TIDAK TAHU (entry0 runtime base); 0x1286/TIDAK TAHU (entry0 runtime base); 0x1296/TIDAK TAHU (entry0 runtime base); 0x1506/TIDAK TAHU (entry0 runtime base); 0x166E/TIDAK TAHU (entry0 runtime base); 0x1A6E/TIDAK TAHU (entry0 runtime base); 0x21BD/TIDAK TAHU (entry0 runtime base); 0x36A8/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 100 | 32 | 13 | 0x1A6E/TIDAK TAHU (entry0 runtime base); 0x72C2/TIDAK TAHU (entry0 runtime base); 0x7662/TIDAK TAHU (entry0 runtime base); 0x767A/TIDAK TAHU (entry0 runtime base); 0x7692/TIDAK TAHU (entry0 runtime base); 0xB6FA/TIDAK TAHU (entry0 runtime base); 0xF296/TIDAK TAHU (entry0 runtime base); 0x10686/TIDAK TAHU (entry0 runtime base); 0x127FE/TIDAK TAHU (entry0 runtime base); 0x12816/TIDAK TAHU (entry0 runtime base); 0x17D16/TIDAK TAHU (entry0 runtime base); 0x194E0/TIDAK TAHU (entry0 runtime base); 0x194F8/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 150 | 8 | 85 | 0xDF2/TIDAK TAHU (entry0 runtime base); 0x3887/TIDAK TAHU (entry0 runtime base); 0x393F/TIDAK TAHU (entry0 runtime base); 0x6CEF/TIDAK TAHU (entry0 runtime base); 0x6D0B/TIDAK TAHU (entry0 runtime base); 0x6D3B/TIDAK TAHU (entry0 runtime base); 0x6D57/TIDAK TAHU (entry0 runtime base); 0x6EA3/TIDAK TAHU (entry0 runtime base); 0x6EBF/TIDAK TAHU (entry0 runtime base); 0x717F/TIDAK TAHU (entry0 runtime base); 0x719F/TIDAK TAHU (entry0 runtime base); 0x7863/TIDAK TAHU (entry0 runtime base); 0x7F4B/TIDAK TAHU (entry0 runtime base); 0x89FC/TIDAK TAHU (entry0 runtime base); 0x921F/TIDAK TAHU (entry0 runtime base); 0x9233/TIDAK TAHU (entry0 runtime base); 0x9287/TIDAK TAHU (entry0 runtime base); 0x929B/TIDAK TAHU (entry0 runtime base); 0x92DF/TIDAK TAHU (entry0 runtime base); 0x92F3/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 150 | 16 | 72 | 0xDF2/TIDAK TAHU (entry0 runtime base); 0x3887/TIDAK TAHU (entry0 runtime base); 0x393F/TIDAK TAHU (entry0 runtime base); 0x6CEF/TIDAK TAHU (entry0 runtime base); 0x6D0B/TIDAK TAHU (entry0 runtime base); 0x6D3B/TIDAK TAHU (entry0 runtime base); 0x6D57/TIDAK TAHU (entry0 runtime base); 0x6EA3/TIDAK TAHU (entry0 runtime base); 0x6EBF/TIDAK TAHU (entry0 runtime base); 0x717F/TIDAK TAHU (entry0 runtime base); 0x719F/TIDAK TAHU (entry0 runtime base); 0x7863/TIDAK TAHU (entry0 runtime base); 0x7F4B/TIDAK TAHU (entry0 runtime base); 0x921F/TIDAK TAHU (entry0 runtime base); 0x9233/TIDAK TAHU (entry0 runtime base); 0x9287/TIDAK TAHU (entry0 runtime base); 0x929B/TIDAK TAHU (entry0 runtime base); 0x92DF/TIDAK TAHU (entry0 runtime base); 0x92F3/TIDAK TAHU (entry0 runtime base); 0x9333/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 150 | 32 | 65 | 0xDF2/TIDAK TAHU (entry0 runtime base); 0x3887/TIDAK TAHU (entry0 runtime base); 0x393F/TIDAK TAHU (entry0 runtime base); 0x6CEF/TIDAK TAHU (entry0 runtime base); 0x6D0B/TIDAK TAHU (entry0 runtime base); 0x6D3B/TIDAK TAHU (entry0 runtime base); 0x6D57/TIDAK TAHU (entry0 runtime base); 0x6EA3/TIDAK TAHU (entry0 runtime base); 0x6EBF/TIDAK TAHU (entry0 runtime base); 0x717F/TIDAK TAHU (entry0 runtime base); 0x719F/TIDAK TAHU (entry0 runtime base); 0x7863/TIDAK TAHU (entry0 runtime base); 0x7F4B/TIDAK TAHU (entry0 runtime base); 0x921F/TIDAK TAHU (entry0 runtime base); 0x9233/TIDAK TAHU (entry0 runtime base); 0x9287/TIDAK TAHU (entry0 runtime base); 0x929B/TIDAK TAHU (entry0 runtime base); 0x92DF/TIDAK TAHU (entry0 runtime base); 0x92F3/TIDAK TAHU (entry0 runtime base); 0x9333/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY1 | 50 | 8 | 470 | 0x9FD/0x800ADE4D (static candidate; runtime unverified); 0x10BD/0x800AE50D (static candidate; runtime unverified); 0x10D9/0x800AE529 (static candidate; runtime unverified); 0x10DD/0x800AE52D (static candidate; runtime unverified); 0x10E1/0x800AE531 (static candidate; runtime unverified); 0x10E5/0x800AE535 (static candidate; runtime unverified); 0x10E9/0x800AE539 (static candidate; runtime unverified); 0x10ED/0x800AE53D (static candidate; runtime unverified); 0x1A2D/0x800AEE7D (static candidate; runtime unverified); 0x1A31/0x800AEE81 (static candidate; runtime unverified); 0x4B84/0x800B1FD4 (static candidate; runtime unverified); 0x555F/0x800B29AF (static candidate; runtime unverified); 0x5C4C/0x800B309C (static candidate; runtime unverified); 0x5E24/0x800B3274 (static candidate; runtime unverified); 0x64A7/0x800B38F7 (static candidate; runtime unverified); 0x6803/0x800B3C53 (static candidate; runtime unverified); 0x68F2/0x800B3D42 (static candidate; runtime unverified); 0x69AF/0x800B3DFF (static candidate; runtime unverified); 0x6CE4/0x800B4134 (static candidate; runtime unverified); 0x72E0/0x800B4730 (static candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 50 | 16 | 169 | 0x4B84/0x800B1FD4 (static candidate; runtime unverified); 0x5C4C/0x800B309C (static candidate; runtime unverified); 0x72E0/0x800B4730 (static candidate; runtime unverified); 0x765C/0x800B4AAC (static candidate; runtime unverified); 0x957C/0x800B69CC (static candidate; runtime unverified); 0xB608/0x800B8A58 (static candidate; runtime unverified); 0xD4BC/0x800BA90C (static candidate; runtime unverified); 0xDD04/0x800BB154 (static candidate; runtime unverified); 0x1B77C/0x800C8BCC (static candidate; runtime unverified); 0x1BCE8/0x800C9138 (static candidate; runtime unverified); 0x1CF40/0x800CA390 (static candidate; runtime unverified); 0x1DC90/0x800CB0E0 (static candidate; runtime unverified); 0x1F784/0x800CCBD4 (static candidate; runtime unverified); 0x27608/0x800D4A58 (static candidate; runtime unverified); 0x28634/0x800D5A84 (static candidate; runtime unverified); 0x294B8/0x800D6908 (static candidate; runtime unverified); 0x2B3FC/0x800D884C (static candidate; runtime unverified); 0x2B770/0x800D8BC0 (static candidate; runtime unverified); 0x2E598/0x800DB9E8 (static candidate; runtime unverified); 0x2E758/0x800DBBA8 (static candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 50 | 32 | 0 | none |
| DATA.BIN_ENTRY1 | 60 | 8 | 10688 | 0x484/0x800AD8D4 (static candidate; runtime unverified); 0xCC8/0x800AE118 (static candidate; runtime unverified); 0xFF0/0x800AE440 (static candidate; runtime unverified); 0x1070/0x800AE4C0 (static candidate; runtime unverified); 0x10C0/0x800AE510 (static candidate; runtime unverified); 0x1175/0x800AE5C5 (static candidate; runtime unverified); 0x1179/0x800AE5C9 (static candidate; runtime unverified); 0x117D/0x800AE5CD (static candidate; runtime unverified); 0x1181/0x800AE5D1 (static candidate; runtime unverified); 0x1185/0x800AE5D5 (static candidate; runtime unverified); 0x1189/0x800AE5D9 (static candidate; runtime unverified); 0x118D/0x800AE5DD (static candidate; runtime unverified); 0x11D8/0x800AE628 (static candidate; runtime unverified); 0x1414/0x800AE864 (static candidate; runtime unverified); 0x1548/0x800AE998 (static candidate; runtime unverified); 0x1614/0x800AEA64 (static candidate; runtime unverified); 0x1A34/0x800AEE84 (static candidate; runtime unverified); 0x1E04/0x800AF254 (static candidate; runtime unverified); 0x1ECC/0x800AF31C (static candidate; runtime unverified); 0x28BC/0x800AFD0C (static candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 60 | 16 | 449 | 0x28BC/0x800AFD0C (static candidate; runtime unverified); 0x4BD8/0x800B2028 (static candidate; runtime unverified); 0x5C9C/0x800B30EC (static candidate; runtime unverified); 0x6920/0x800B3D70 (static candidate; runtime unverified); 0x6938/0x800B3D88 (static candidate; runtime unverified); 0x6950/0x800B3DA0 (static candidate; runtime unverified); 0x6980/0x800B3DD0 (static candidate; runtime unverified); 0x6998/0x800B3DE8 (static candidate; runtime unverified); 0x7EA4/0x800B52F4 (static candidate; runtime unverified); 0x7FD3/0x800B5423 (static candidate; runtime unverified); 0x8023/0x800B5473 (static candidate; runtime unverified); 0x80DF/0x800B552F (static candidate; runtime unverified); 0x8874/0x800B5CC4 (static candidate; runtime unverified); 0x888C/0x800B5CDC (static candidate; runtime unverified); 0x88A4/0x800B5CF4 (static candidate; runtime unverified); 0x88D4/0x800B5D24 (static candidate; runtime unverified); 0x88EC/0x800B5D3C (static candidate; runtime unverified); 0x8D50/0x800B61A0 (static candidate; runtime unverified); 0x8D68/0x800B61B8 (static candidate; runtime unverified); 0x8D80/0x800B61D0 (static candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 60 | 32 | 4 | 0x8C3A1/0x801397F1 (static candidate; runtime unverified); 0x8C595/0x801399E5 (static candidate; runtime unverified); 0x8C6A5/0x80139AF5 (static candidate; runtime unverified); 0x8C725/0x80139B75 (static candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 100 | 8 | 1246 | 0x130/0x800AD580 (static candidate; runtime unverified); 0x1D0/0x800AD620 (static candidate; runtime unverified); 0x1E4/0x800AD634 (static candidate; runtime unverified); 0x244/0x800AD694 (static candidate; runtime unverified); 0x25C/0x800AD6AC (static candidate; runtime unverified); 0x3AD/0x800AD7FD (static candidate; runtime unverified); 0x3E5/0x800AD835 (static candidate; runtime unverified); 0x3F4/0x800AD844 (static candidate; runtime unverified); 0x56C/0x800AD9BC (static candidate; runtime unverified); 0x578/0x800AD9C8 (static candidate; runtime unverified); 0x604/0x800ADA54 (static candidate; runtime unverified); 0x9C4/0x800ADE14 (static candidate; runtime unverified); 0xD2C/0x800AE17C (static candidate; runtime unverified); 0x1240/0x800AE690 (static candidate; runtime unverified); 0x1249/0x800AE699 (static candidate; runtime unverified); 0x1368/0x800AE7B8 (static candidate; runtime unverified); 0x1500/0x800AE950 (static candidate; runtime unverified); 0x152C/0x800AE97C (static candidate; runtime unverified); 0x1664/0x800AEAB4 (static candidate; runtime unverified); 0x16F8/0x800AEB48 (static candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 100 | 16 | 506 | 0x3FF7/0x800B1447 (static candidate; runtime unverified); 0x5572/0x800B29C2 (static candidate; runtime unverified); 0x5FF8/0x800B3448 (static candidate; runtime unverified); 0x7A1E/0x800B4E6E (static candidate; runtime unverified); 0x81F2/0x800B5642 (static candidate; runtime unverified); 0x824E/0x800B569E (static candidate; runtime unverified); 0x92A8/0x800B66F8 (static candidate; runtime unverified); 0x9F54/0x800B73A4 (static candidate; runtime unverified); 0xA76C/0x800B7BBC (static candidate; runtime unverified); 0xA998/0x800B7DE8 (static candidate; runtime unverified); 0xA9AC/0x800B7DFC (static candidate; runtime unverified); 0xAE66/0x800B82B6 (static candidate; runtime unverified); 0xD2DA/0x800BA72A (static candidate; runtime unverified); 0xD306/0x800BA756 (static candidate; runtime unverified); 0xD332/0x800BA782 (static candidate; runtime unverified); 0xD4F2/0x800BA942 (static candidate; runtime unverified); 0xD51E/0x800BA96E (static candidate; runtime unverified); 0xD54A/0x800BA99A (static candidate; runtime unverified); 0xD5F2/0x800BAA42 (static candidate; runtime unverified); 0xD668/0x800BAAB8 (static candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 100 | 32 | 24 | 0xAE66/0x800B82B6 (static candidate; runtime unverified); 0x20A46/0x800CDE96 (static candidate; runtime unverified); 0x20DC6/0x800CE216 (static candidate; runtime unverified); 0x20F72/0x800CE3C2 (static candidate; runtime unverified); 0x5C3AE/0x801097FE (static candidate; runtime unverified); 0x68DA2/0x801161F2 (static candidate; runtime unverified); 0x6B7EE/0x80118C3E (static candidate; runtime unverified); 0x6B82E/0x80118C7E (static candidate; runtime unverified); 0x6BA0E/0x80118E5E (static candidate; runtime unverified); 0x6BA4E/0x80118E9E (static candidate; runtime unverified); 0x6F87A/0x8011CCCA (static candidate; runtime unverified); 0x741D2/0x80121622 (static candidate; runtime unverified); 0x77F1E/0x8012536E (static candidate; runtime unverified); 0x78096/0x801254E6 (static candidate; runtime unverified); 0x814A2/0x8012E8F2 (static candidate; runtime unverified); 0x88242/0x80135692 (static candidate; runtime unverified); 0x8B33E/0x8013878E (static candidate; runtime unverified); 0x8B37E/0x801387CE (static candidate; runtime unverified); 0x8C3AD/0x801397FD (static candidate; runtime unverified); 0x8C567/0x801399B7 (static candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 150 | 8 | 724 | 0x13B1/0x800AE801 (static candidate; runtime unverified); 0x4B74/0x800B1FC4 (static candidate; runtime unverified); 0x4C0C/0x800B205C (static candidate; runtime unverified); 0x4CB8/0x800B2108 (static candidate; runtime unverified); 0x5270/0x800B26C0 (static candidate; runtime unverified); 0x54AC/0x800B28FC (static candidate; runtime unverified); 0x5834/0x800B2C84 (static candidate; runtime unverified); 0x5C38/0x800B3088 (static candidate; runtime unverified); 0x5CD0/0x800B3120 (static candidate; runtime unverified); 0x6368/0x800B37B8 (static candidate; runtime unverified); 0x808C/0x800B54DC (static candidate; runtime unverified); 0x8366/0x800B57B6 (static candidate; runtime unverified); 0x836E/0x800B57BE (static candidate; runtime unverified); 0x9910/0x800B6D60 (static candidate; runtime unverified); 0x9A5F/0x800B6EAF (static candidate; runtime unverified); 0x9A8B/0x800B6EDB (static candidate; runtime unverified); 0x9A94/0x800B6EE4 (static candidate; runtime unverified); 0xC5C7/0x800B9A17 (static candidate; runtime unverified); 0xC6BF/0x800B9B0F (static candidate; runtime unverified); 0xD0FF/0x800BA54F (static candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 150 | 16 | 484 | 0x4C0C/0x800B205C (static candidate; runtime unverified); 0x5CD0/0x800B3120 (static candidate; runtime unverified); 0x9A5F/0x800B6EAF (static candidate; runtime unverified); 0x9A8B/0x800B6EDB (static candidate; runtime unverified); 0x9A94/0x800B6EE4 (static candidate; runtime unverified); 0xC5C7/0x800B9A17 (static candidate; runtime unverified); 0xC6BF/0x800B9B0F (static candidate; runtime unverified); 0xD0FF/0x800BA54F (static candidate; runtime unverified); 0xD217/0x800BA667 (static candidate; runtime unverified); 0xD2CF/0x800BA71F (static candidate; runtime unverified); 0xD2FB/0x800BA74B (static candidate; runtime unverified); 0xD327/0x800BA777 (static candidate; runtime unverified); 0xD3F7/0x800BA847 (static candidate; runtime unverified); 0xD4E7/0x800BA937 (static candidate; runtime unverified); 0xD513/0x800BA963 (static candidate; runtime unverified); 0xD53F/0x800BA98F (static candidate; runtime unverified); 0xEAB3/0x800BBF03 (static candidate; runtime unverified); 0xF54B/0x800BC99B (static candidate; runtime unverified); 0xF58F/0x800BC9DF (static candidate; runtime unverified); 0x10E97/0x800BE2E7 (static candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 150 | 32 | 442 | 0x9A5F/0x800B6EAF (static candidate; runtime unverified); 0x9A8B/0x800B6EDB (static candidate; runtime unverified); 0xC5C7/0x800B9A17 (static candidate; runtime unverified); 0xC6BF/0x800B9B0F (static candidate; runtime unverified); 0xD0FF/0x800BA54F (static candidate; runtime unverified); 0xD217/0x800BA667 (static candidate; runtime unverified); 0xD2CF/0x800BA71F (static candidate; runtime unverified); 0xD2FB/0x800BA74B (static candidate; runtime unverified); 0xD327/0x800BA777 (static candidate; runtime unverified); 0xD3F7/0x800BA847 (static candidate; runtime unverified); 0xD4E7/0x800BA937 (static candidate; runtime unverified); 0xD513/0x800BA963 (static candidate; runtime unverified); 0xD53F/0x800BA98F (static candidate; runtime unverified); 0xEAB3/0x800BBF03 (static candidate; runtime unverified); 0xF54B/0x800BC99B (static candidate; runtime unverified); 0xF58F/0x800BC9DF (static candidate; runtime unverified); 0x10E97/0x800BE2E7 (static candidate; runtime unverified); 0x1354F/0x800C099F (static candidate; runtime unverified); 0x1380F/0x800C0C5F (static candidate; runtime unverified); 0x13887/0x800C0CD7 (static candidate; runtime unverified) |

## Sequence 100/120/150/180/200 (LE u8/u16/u32)

Pencarian exact contiguous. Tabel berpadded/strided perlu disimpulkan melalui instruksi pembaca.
- SLPS_035.53 u8: 0 hits; TIDAK DITEMUKAN
- SLPS_035.53 u16: 0 hits; TIDAK DITEMUKAN
- SLPS_035.53 u32: 0 hits; TIDAK DITEMUKAN
- DATA.BIN_ENTRY0 u8: 0 hits; TIDAK DITEMUKAN
- DATA.BIN_ENTRY0 u16: 0 hits; TIDAK DITEMUKAN
- DATA.BIN_ENTRY0 u32: 0 hits; TIDAK DITEMUKAN
- DATA.BIN_ENTRY1 u8: 0 hits; TIDAK DITEMUKAN
- DATA.BIN_ENTRY1 u16: 0 hits; TIDAK DITEMUKAN
- DATA.BIN_ENTRY1 u32: 0 hits; TIDAK DITEMUKAN

## Dispatch table FUN_800B770C

DATA.BIN Entry 1 file offset 0x1A4 = VA kandidat 0x800AD5F4. Lima word berikut diverifikasi byte-per-byte sebagai pointer dispatch, bukan table berisi angka persentase.

| Selector | VA tabel | Offset | Byte LE | Target |
|---:|---:|---:|---|---|
| 0 | 0x800AD5F4 | 0x1A4 | 60 77 0B 80 | 0x800B7760 |
| 1 | 0x800AD5F8 | 0x1A8 | A0 77 0B 80 | 0x800B77A0 |
| 2 | 0x800AD5FC | 0x1AC | 08 78 0B 80 | 0x800B7808 |
| 3 | 0x800AD600 | 0x1B0 | 50 78 0B 80 | 0x800B7850 |
| 4 | 0x800AD604 | 0x1B4 | 9C 78 0B 80 | 0x800B789C |

Reader: FUN_800B770C at PC 0x800B7750 loads the selected word with lw v0,0x0(v1). The branch boundary is sltiu v0,v1,0x5 at 0x800B7738; selector >=5 returns zero at 0x800B7798.

### Perhitungan faktor ada dalam instruksi (bukan literal table 100/120/150/180/200)

| Selector | Target | Instruksi aritmetika yang terbukti |
|---:|---:|---|
| 0 | 0x800B7760 | return H |
| 1 | 0x800B77A0 | H*12; magic reciprocal 0x66666667 divides by 10 at 0x800B77E8–0x800B7804 |
| 2 | 0x800B7808 | 16H−H=15H; divide by 10 at shared 0x800B77E8–0x800B7804 |
| 3 | 0x800B7850 | 9H*2=18H; divide by 10 at shared 0x800B77E8–0x800B7804 |
| 4 | 0x800B789C | H*2 at 0x800B78D8 |

H = u16(R+0x10+((u16(R+0x20)>>7)&0x1E)); R=[0x8013EA84]+index*0x124. Ini hasil helper; bukan dengan sendirinya pendapatan/biaya gameplay.

## Literal Shift-JIS/ASCII terms

- SLPS_035.53 ASCII Barrier: 0
- SLPS_035.53 Shift-JIS Barrier: 0
- SLPS_035.53 ASCII Chakra: 0
- SLPS_035.53 Shift-JIS Chakra: 0
- SLPS_035.53 ASCII cost: 0
- SLPS_035.53 Shift-JIS cost: 0
- SLPS_035.53 ASCII upgrade: 0
- SLPS_035.53 Shift-JIS upgrade: 0
- SLPS_035.53 ASCII release: 0
- SLPS_035.53 Shift-JIS release: 0
- SLPS_035.53 Shift-JIS 結界: 0
- SLPS_035.53 Shift-JIS チャクラ: 0
- SLPS_035.53 Shift-JIS 費用: 0
- SLPS_035.53 Shift-JIS 強化: 0
- SLPS_035.53 Shift-JIS 建設: 0
- SLPS_035.53 Shift-JIS 解除: 0
- SLPS_035.53 Shift-JIS 解放: 0
- SLPS_035.53 Shift-JIS バリア: 0
- DATA.BIN_ENTRY0 ASCII Barrier: 0
- DATA.BIN_ENTRY0 Shift-JIS Barrier: 0
- DATA.BIN_ENTRY0 ASCII Chakra: 0
- DATA.BIN_ENTRY0 Shift-JIS Chakra: 0
- DATA.BIN_ENTRY0 ASCII cost: 0
- DATA.BIN_ENTRY0 Shift-JIS cost: 0
- DATA.BIN_ENTRY0 ASCII upgrade: 0
- DATA.BIN_ENTRY0 Shift-JIS upgrade: 0
- DATA.BIN_ENTRY0 ASCII release: 0
- DATA.BIN_ENTRY0 Shift-JIS release: 0
- DATA.BIN_ENTRY0 Shift-JIS 結界: 0
- DATA.BIN_ENTRY0 Shift-JIS チャクラ: 0
- DATA.BIN_ENTRY0 Shift-JIS 費用: 0
- DATA.BIN_ENTRY0 Shift-JIS 強化: 0
- DATA.BIN_ENTRY0 Shift-JIS 建設: 0
- DATA.BIN_ENTRY0 Shift-JIS 解除: 0
- DATA.BIN_ENTRY0 Shift-JIS 解放: 0
- DATA.BIN_ENTRY0 Shift-JIS バリア: 0
- DATA.BIN_ENTRY1 ASCII Barrier: 0
- DATA.BIN_ENTRY1 Shift-JIS Barrier: 0
- DATA.BIN_ENTRY1 ASCII Chakra: 0
- DATA.BIN_ENTRY1 Shift-JIS Chakra: 0
- DATA.BIN_ENTRY1 ASCII cost: 0
- DATA.BIN_ENTRY1 Shift-JIS cost: 0
- DATA.BIN_ENTRY1 ASCII upgrade: 0
- DATA.BIN_ENTRY1 Shift-JIS upgrade: 0
- DATA.BIN_ENTRY1 ASCII release: 0
- DATA.BIN_ENTRY1 Shift-JIS release: 0
- DATA.BIN_ENTRY1 Shift-JIS 結界: 0
- DATA.BIN_ENTRY1 Shift-JIS チャクラ: 0
- DATA.BIN_ENTRY1 Shift-JIS 費用: 0
- DATA.BIN_ENTRY1 Shift-JIS 強化: 0
- DATA.BIN_ENTRY1 Shift-JIS 建設: 0
- DATA.BIN_ENTRY1 Shift-JIS 解除: 0
- DATA.BIN_ENTRY1 Shift-JIS 解放: 0
- DATA.BIN_ENTRY1 Shift-JIS バリア: 0

## Run Shift-JIS heuristik

Mengambil run byte yang valid sebagai Shift-JIS multi-byte (minimal tiga pasangan), lalu decode. Ini kandidat string, belum tentu dipakai UI.
### SLPS_035.53: 25 runs
- offset=0xD64; address=0x80010564; bytes=82 6d 82 60 82 71 82 74 82 73 82 6e 81 5b 83 69 83 8b 83 67 81 5b 81 40 94 45 82 cc 97 a2 82 cc 90 77 8e e6 82 e8 8d 87; text=ＮＡＲＵＴＯーナルトー　忍の里の陣取り合戦　　　　　　　　　　　
- offset=0x5B40A; address=0x8006AC0A; bytes=86 f0 ec fb 87 f0 e6 fb 89 f0 e0 fb 8a f0 da; text=������踴解瓔嬉ﾚ
- offset=0x5B43E; address=0x8006AC3E; bytes=9b f0 9d fb 9d f0 97 fb 9f f0 91 fb; text=幤暾晰練溟蛸
- offset=0x5B4EA; address=0x8006ACEA; bytes=ed f0 9c fa ef f0 96 fa; text=��戌��愈
- offset=0x5B85A; address=0x8006B05A; bytes=8e f3 ed f5 92 f3 e8 f5 96 f3 e3 f5 9a f3 de; text=受��汀頷訳脉奕ﾞ
- offset=0x5B8AC; address=0x8006B0AC; bytes=8d f5 e2 f3 88 f5 e7 f3 83 f5 eb f3 7e; text=索糒員銛����~
- offset=0x5BA24; address=0x8006B224; bytes=eb f3 83 f5 e7 f3 88 f5 e2 f3 8d f5 de; text=����銛員糒索ﾞ
- offset=0x5BA74; address=0x8006B274; bytes=9a f3 e3 f5 96 f3 e8 f5 92 f3 ed f5 8e f3; text=奕脉訳頷汀��受
- offset=0x5BDEA; address=0x8006B5EA; bytes=96 fa ef f0 9c fa ed f0 a2; text=愈��戌��｢
- offset=0x5BE92; address=0x8006B692; bytes=91 fb 9f f0 97 fb 9d f0 9d fb 9b f0 a3; text=蛸溟練晰暾幤｣
- offset=0x5BEC4; address=0x8006B6C4; bytes=8a f0 e0 fb 89 f0 e6 fb 87 f0 ec fb 86 f0; text=嬉瓔解踴������
- offset=0x5DC5E; address=0x8006D45E; bytes=38 81 46 81 55 81 64 81 73 81 82 81 91 81 a0 81 af 81 be 81 cd 81 dc 81 eb 81 fa; text=8：ゞ‥《≠¢□�ｯ∪∀⌒����
- offset=0x5DC80; address=0x8006D480; bytes=36 82 45 82 54 82 63 82 72 82 82 82 91 82 a0 82 af 82 be 82 cd 82 dc 82 eb 82 fa; text=6�E５ＤＳｂｑあけだはまろ��
- offset=0x5DCA2; address=0x8006D4A2; bytes=37 83 46 83 55 83 64 83 74 83 83 83 92 83 a1 83 b0 83 c0 83 cf 83 de 83 ed; text=7ェザヅフャヲΓΣβρ�ﾞ��
- offset=0x5DCC4; address=0x8006D4C4; bytes=3a 84 49 84 58 84 68 84 77 84 86 84 95 84 a5 84 b4 84 c3 84 d3 84 e2 84 f1; text=:ИЧ�hжф�符･╋�ﾃ�ﾓ�邃�
- offset=0x5DCE6; address=0x8006D4E6; bytes=3e 85 4e 85 5d 85 6d 85 7c 85 8b 85 9b 85 aa 85 ba 85 c9 85 d9 85 e8 85 f8; text=>�N�]�m�/�球寉ｪ�ｺ�ﾉ�ﾙ�閻�
- offset=0x5DD06; address=0x8006D506; bytes=36 86 45 86 55 86 64 86 74 86 83 86 93 86 a2 86 b2 86 c1 86 d1 86 e0 86 f0; text=6�E�U�d�t�ユ宕｢�ｲ�ﾁ�ﾑ�煕�
- offset=0x5DD28; address=0x8006D528; bytes=3e 87 4e 87 5d 87 6d 87 7d 87 8c; text=>�N�]�m�}��
- offset=0x5DD7E; address=0x8006D57E; bytes=38 81 46 81 55 81 64 81 73 81 82 81 91 81 a0 81 af 81 be 81 cd 81 dc 81 eb 81 fa; text=8：ゞ‥《≠¢□�ｯ∪∀⌒����
- offset=0x5DDA0; address=0x8006D5A0; bytes=36 82 45 82 54 82 63 82 72 82 82 82 91 82 a0 82 af 82 be 82 cd 82 dc 82 eb 82 fa; text=6�E５ＤＳｂｑあけだはまろ��
- offset=0x5DDC2; address=0x8006D5C2; bytes=37 83 46 83 55 83 64 83 74 83 83 83 92 83 a1 83 b0 83 c0 83 cf 83 de 83 ed; text=7ェザヅフャヲΓΣβρ�ﾞ��
- offset=0x5DDE4; address=0x8006D5E4; bytes=3a 84 49 84 58 84 68 84 77 84 86 84 95 84 a5 84 b4 84 c3 84 d3 84 e2 84 f1; text=:ИЧ�hжф�符･╋�ﾃ�ﾓ�邃�
- offset=0x5DE06; address=0x8006D606; bytes=3e 85 4e 85 5d 85 6d 85 7c 85 8b 85 9b 85 aa 85 ba 85 c9 85 d9 85 e8 85 f8; text=>�N�]�m�/�球寉ｪ�ｺ�ﾉ�ﾙ�閻�
- offset=0x5DE26; address=0x8006D626; bytes=36 86 45 86 55 86 64 86 74 86 83 86 93 86 a2 86 b2 86 c1 86 d1 86 e0 86 f0; text=6�E�U�d�t�ユ宕｢�ｲ�ﾁ�ﾑ�煕�
- offset=0x5DE48; address=0x8006D648; bytes=3e 87 4e 87 5d 87 6d 87 7d 87 8c; text=>�N�]�m�}��
### DATA.BIN_ENTRY0: 3 runs
- offset=0x1457; address=TIDAK TAHU (entry0 runtime base); bytes=26 94 67 84 8e e2 83; text=&波ь窿
- offset=0x12DBB; address=TIDAK TAHU (entry0 runtime base); bytes=3c dc 72 42 24 d7 72 64 88 d4 72 64 98 db 72 a3 88 d8 72 a3; text=<ﾜrB$ﾗrd慰rd俚r｣畏r｣
- offset=0x13F17; address=TIDAK TAHU (entry0 runtime base); bytes=3c ec 72 42 24 e7 72 64 88 e4 72 64 98 eb 72 a3 88 e8 72 a3; text=<�rB$輦d井rd俯r｣郁r｣
### DATA.BIN_ENTRY1: 234 runs
- offset=0x530B; address=0x800B275B (static candidate; runtime unverified); bytes=3c 88 ea 62 a4 8a ea 82 a4 d0; text=<一b､伎うﾐ
- offset=0x56A3; address=0x800B2AF3 (static candidate; runtime unverified); bytes=3c 50 ea 42 24 b8 ea 62 ac e0 4c; text=<P鵤$ｸ鹵ｬ澂
- offset=0x6796; address=0x800B3BE6 (static candidate; runtime unverified); bytes=83 a0 74 ea 64 8e c0; text=Βt鹽実
- offset=0x6CB3; address=0x800B4103 (static candidate; runtime unverified); bytes=3c 88 ea 62 a4 8a ea 82 a4 d0; text=<一b､伎うﾐ
- offset=0x6EB0; address=0x800B4300 (static candidate; runtime unverified); bytes=c7 ea e3 90 84 ea c4 8c c0; text=ﾇ�辮��ﾄ限
- offset=0x70CF; address=0x800B451F (static candidate; runtime unverified); bytes=92 84 ea 44 8e c0; text=嫡鵐実
- offset=0x71FC; address=0x800B464C (static candidate; runtime unverified); bytes=c7 ea a3 90 84 ea c4 8c c0; text=ﾇ凜推�ﾄ限
- offset=0x7270; address=0x800B46C0 (static candidate; runtime unverified); bytes=c7 ea a3 90 84 ea c4 8c c0; text=ﾇ凜推�ﾄ限
- offset=0x7298; address=0x800B46E8 (static candidate; runtime unverified); bytes=c7 ea a3 90 84 ea c4 8c c0; text=ﾇ凜推�ﾄ限
- offset=0x768F; address=0x800B4ADF (static candidate; runtime unverified); bytes=3c ce ea 65 84 d2 ea c6; text=<ﾎ麁�ﾒ�ﾆ
- offset=0x77E2; address=0x800B4C32 (static candidate; runtime unverified); bytes=82 a0 8a ea 64 90 4a; text=あ伎d辱
- offset=0x871E; address=0x800B5B6E (static candidate; runtime unverified); bytes=83 a0 74 ea 64 8e c0; text=Βt鹽実
- offset=0x9BEC; address=0x800B703C (static candidate; runtime unverified); bytes=b0 ea 82 8e b4 ea 45; text=ｰ黷雫鵙
- offset=0x9C5C; address=0x800B70AC (static candidate; runtime unverified); bytes=b0 ea 82 8e b4 ea 45; text=ｰ黷雫鵙
- offset=0xD438; address=0x800BA888 (static candidate; runtime unverified); bytes=88 ea 84 96 74 ea 63 8e c0; text=一�釦鹹実
- offset=0xDEB0; address=0x800BB300 (static candidate; runtime unverified); bytes=ee 9b 83 a4 ee 9b; text=�寃､��
- offset=0xE2CE; address=0x800BB71E (static candidate; runtime unverified); bytes=43 90 84 ea c6 8d c0; text=C推�ﾆ座
- offset=0xE3C2; address=0x800BB812 (static candidate; runtime unverified); bytes=83 90 84 ea c4 8d c0; text=ヰ��ﾄ座
- offset=0xE486; address=0x800BB8D6 (static candidate; runtime unverified); bytes=43 90 84 ea c6 8d c0; text=C推�ﾆ座
- offset=0xE57E; address=0x800BB9CE (static candidate; runtime unverified); bytes=83 90 84 ea c4 8d c0; text=ヰ��ﾄ座
- offset=0xF544; address=0x800BC994 (static candidate; runtime unverified); bytes=74 ea 84 8e 88 ea 43; text=t黻肢鵑
- offset=0xF588; address=0x800BC9D8 (static candidate; runtime unverified); bytes=74 ea 85 8e 88 ea 42; text=t黼肢鵤
- offset=0x106FA; address=0x800BDB4A (static candidate; runtime unverified); bytes=48 91 84 ea a5 8d c0; text=H槍�･座
- offset=0x11E4B; address=0x800BF29B (static candidate; runtime unverified); bytes=92 74 ea 43 8e c0; text=稚鵑実
- offset=0x11EBF; address=0x800BF30F (static candidate; runtime unverified); bytes=92 74 ea 43 8e c0; text=稚鵑実
- offset=0x122C7; address=0x800BF717 (static candidate; runtime unverified); bytes=3c ce ea 46 84 74 ea 44; text=<ﾎ鵲д鵐
- offset=0x123FB; address=0x800BF84B (static candidate; runtime unverified); bytes=3c 88 ea 6e 94 74 ea 4a; text=<一n杯鵯
- offset=0x13DBF; address=0x800C120F (static candidate; runtime unverified); bytes=3c ce ea 45 84 74 ea 84; text=<ﾎ鵙д黻
- offset=0x149B6; address=0x800C1E06 (static candidate; runtime unverified); bytes=64 90 84 ea 45 8e c0; text=d推鵙実
- offset=0x14ABE; address=0x800C1F0E (static candidate; runtime unverified); bytes=43 90 84 ea 44 8e c0; text=C推鵐実
- offset=0x14CEC; address=0x800C213C (static candidate; runtime unverified); bytes=74 ea 84 8c 88 ea 43; text=t黻決鵑
- offset=0x16577; address=0x800C39C7 (static candidate; runtime unverified); bytes=3c c0 ea 44 8c e4 ea 62; text=<ﾀ鵐御鹵
- offset=0x16AFB; address=0x800C3F4B (static candidate; runtime unverified); bytes=3c c0 ea a3 8c e4 ea 82; text=<ﾀ凜御黷
- offset=0x16C3E; address=0x800C408E (static candidate; runtime unverified); bytes=82 a0 74 ea a2 8c ca; text=あt瑤弧
- offset=0x170B2; address=0x800C4502 (static candidate; runtime unverified); bytes=85 a0 8a ea 24 96 74; text=��伎$釦
- offset=0x20C5E; address=0x800CE0AE (static candidate; runtime unverified); bytes=82 ac 74 ea 42 8c c0 20; text=ぎt鵤限 
- offset=0x225C6; address=0x800CFA16 (static candidate; runtime unverified); bytes=82 a0 88 ea 24 96 74; text=あ一$釦
- offset=0x22A2D; address=0x800CFE7D (static candidate; runtime unverified); bytes=eb a3 8c 84 ea 44 8d c0; text=�｣隙鵐座
- offset=0x22AF7; address=0x800CFF47 (static candidate; runtime unverified); bytes=3c 74 ea 64 8e 88 ea 43; text=<t鹽肢鵑
- offset=0x22B6A; address=0x800CFFBA (static candidate; runtime unverified); bytes=22 ae 74 ea 64 8e 88 ea 43; text="ｮt鹽肢鵑
- offset=0x22F9E; address=0x800D03EE (static candidate; runtime unverified); bytes=82 94 88 ea e3 94; text=ｔ一續
- offset=0x22FE0; address=0x800D0430 (static candidate; runtime unverified); bytes=74 ea c4 8c 88 ea e3; text=t�ﾄ決��
- offset=0x235E0; address=0x800D0A30 (static candidate; runtime unverified); bytes=74 ea 84 8e 88 ea 63; text=t黻肢鹹
- offset=0x23654; address=0x800D0AA4 (static candidate; runtime unverified); bytes=74 ea 84 8e 88 ea 63; text=t黻肢鹹
- offset=0x23707; address=0x800D0B57 (static candidate; runtime unverified); bytes=ae 74 ea 84 8e 88 ea 63; text=ｮt黻肢鹹
- offset=0x2389A; address=0x800D0CEA (static candidate; runtime unverified); bytes=83 90 84 ea 24 8e c0; text=ヰ��$実
- offset=0x238EE; address=0x800D0D3E (static candidate; runtime unverified); bytes=83 90 84 ea 24 8e c0; text=ヰ��$実
- offset=0x2394A; address=0x800D0D9A (static candidate; runtime unverified); bytes=83 90 84 ea 24 8e c0; text=ヰ��$実
- offset=0x239AA; address=0x800D0DFA (static candidate; runtime unverified); bytes=83 90 84 ea 24 8e c0; text=ヰ��$実
- offset=0x239DC; address=0x800D0E2C (static candidate; runtime unverified); bytes=bc eb a2 ac bc eb a4 90 81 23; text=ｼ�｢ｬｼ�､吹#
- offset=0x23DEB; address=0x800D123B (static candidate; runtime unverified); bytes=3c d2 ea 47 84 88 ea a3; text=<ﾒ鶉ц凜
- offset=0x243C3; address=0x800D1813 (static candidate; runtime unverified); bytes=3c b0 ea 47 8c 74 ea a4 8c 88 ea c2; text=<ｰ鶉荊熙決�ﾂ
- offset=0x24718; address=0x800D1B68 (static candidate; runtime unverified); bytes=ec 9e 82 ac ec 9e; text=�桙ｬ��
- offset=0x2542C; address=0x800D287C (static candidate; runtime unverified); bytes=bc eb a2 ac bc eb a4 90 81 23; text=ｼ�｢ｬｼ�､吹#
- offset=0x258A4; address=0x800D2CF4 (static candidate; runtime unverified); bytes=bc eb a2 ac bc eb a4 90 81 23; text=ｼ�｢ｬｼ�､吹#
- offset=0x2614F; address=0x800D359F (static candidate; runtime unverified); bytes=3c b0 ea 47 8c 74 ea 84 8c 88 ea c2; text=<ｰ鶉荊黻決�ﾂ
- offset=0x263B3; address=0x800D3803 (static candidate; runtime unverified); bytes=3c b0 ea 47 8c 74 ea 84 8c 88 ea c2; text=<ｰ鶉荊黻決�ﾂ
- offset=0x2662F; address=0x800D3A7F (static candidate; runtime unverified); bytes=3c e0 9e 83 8c d8 9b 42; text=<燼レﾘ妝
- offset=0x26F40; address=0x800D4390 (static candidate; runtime unverified); bytes=bc eb a2 ac bc eb a4 90 81 23; text=ｼ�｢ｬｼ�､吹#
- offset=0x27236; address=0x800D4686 (static candidate; runtime unverified); bytes=a3 90 84 ea 46 8e c0; text=｣推鵲実

## Peta font/tile index

Belum ada rantai instruksi yang mengaitkan indeks glyph/tile UI ke tabel font yang dapat diverifikasi. Maka peta index->glyph adalah TIDAK TAHU; tidak ada tabel buatan.
Readable Shift-JIS runs=262. Nihilnya kata kunci literal bukan bukti bahwa text resources tidak ada.

## Batas

- Tidak memberi label Barrier cost/income/Chakra release dari angka semata.
- Xref numeric data candidates tetap TIDAK TAHU tanpa instruksi pembaca.
- Entry 0 runtime base TIDAK TAHU; tidak ada VA yang direka.
- Entry 1 runtime mapping belum dibuktikan; hanya static candidate base.
- Static scan only; no gameplay/emulator.
