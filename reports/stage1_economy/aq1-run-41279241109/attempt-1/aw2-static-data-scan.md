# AW2 — scan numerik dan string literal

Input SHA diverifikasi. Kemunculan angka adalah kandidat byte, bukan label ekonomi.

| Input | Bytes | SHA-256 |
|---|---:|---|
| SLPS_035.53 | 385024 | a97b3ebea329b267c186ae52fd21edb1891d66377d475cef32db5f133c296569 |
| DATA.BIN_ENTRY0 | 110536 | 56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4 |
| DATA.BIN_ENTRY1 | 596412 | 9c531036e66c88849bc8fd16ee1717f10b1a7e42132f2a616635c122c809c60a |

## Angka 50/60/100/150

| Input | Nilai | Lebar | Jumlah | Offset/VA pertama (maks 25) |
|---|---:|---:|---:|---|
| SLPS_035.53 | 50 | 16 | 100 | 0x193A/0x8001113A; 0x1A2D/0x8001122D; 0x4E54/0x80014654; 0x4FB8/0x800147B8; 0x85FC/0x80017DFC; 0x8748/0x80017F48; 0x8B2C/0x8001832C; 0xB484/0x8001AC84; 0xB904/0x8001B104; 0xC084/0x8001B884; 0xC0C7/0x8001B8C7; 0xC680/0x8001BE80; 0xD060/0x8001C860; 0xD468/0x8001CC68; 0xD828/0x8001D028; 0xD9C0/0x8001D1C0; 0xDA2C/0x8001D22C; 0xDAF0/0x8001D2F0; 0xDD48/0x8001D548; 0xDD90/0x8001D590; 0xDDC8/0x8001D5C8; 0xDE00/0x8001D600; 0xDEFC/0x8001D6FC; 0xE240/0x8001DA40; 0xE51C/0x8001DD1C |
| SLPS_035.53 | 50 | 32 | 6 | 0x46784/0x80055F84; 0x4717C/0x8005697C; 0x476B8/0x80056EB8; 0x47820/0x80057020; 0x47E9C/0x8005769C; 0x482A0/0x80057AA0 |
| SLPS_035.53 | 60 | 16 | 376 | 0x2630/0x80011E30; 0x2700/0x80011F00; 0x2CAF/0x800124AF; 0x2D9B/0x8001259B; 0x3474/0x80012C74; 0x3684/0x80012E84; 0x394F/0x8001314F; 0x4DCF/0x800145CF; 0x723F/0x80016A3F; 0x72FB/0x80016AFB; 0x7AF0/0x800172F0; 0x7B58/0x80017358; 0x7B9C/0x8001739C; 0x8567/0x80017D67; 0x8647/0x80017E47; 0x868B/0x80017E8B; 0x90D3/0x800188D3; 0x943B/0x80018C3B; 0x949B/0x80018C9B; 0x9620/0x80018E20; 0x9764/0x80018F64; 0x9967/0x80019167; 0x9FF8/0x800197F8; 0xA040/0x80019840; 0xA26C/0x80019A6C |
| SLPS_035.53 | 60 | 32 | 3 | 0x477D0/0x80056FD0; 0x47A18/0x80057218; 0x5D92C/0x8006D12C |
| SLPS_035.53 | 100 | 16 | 328 | 0x158A/0x80010D8A; 0x1595/0x80010D95; 0x15CE/0x80010DCE; 0x20A2/0x800118A2; 0x21ED/0x800119ED; 0x233D/0x80011B3D; 0x234D/0x80011B4D; 0x235D/0x80011B5D; 0x2375/0x80011B75; 0x272E/0x80011F2E; 0x28C2/0x800120C2; 0x2D82/0x80012582; 0x36F6/0x80012EF6; 0x5746/0x80014F46; 0x65C6/0x80015DC6; 0x6726/0x80015F26; 0x695A/0x8001615A; 0x8BC6/0x800183C6; 0x94ED/0x80018CED; 0x9665/0x80018E65; 0x97C1/0x80018FC1; 0x98C5/0x800190C5; 0x98CD/0x800190CD; 0x99C9/0x800191C9; 0x9A31/0x80019231 |
| SLPS_035.53 | 100 | 32 | 30 | 0x5746/0x80014F46; 0x65C6/0x80015DC6; 0x6726/0x80015F26; 0x695A/0x8001615A; 0x8BC6/0x800183C6; 0xA5E2/0x80019DE2; 0xDF3E/0x8001D73E; 0xDF56/0x8001D756; 0x10136/0x8001F936; 0x14DA6/0x800245A6; 0x14F0E/0x8002470E; 0x152CE/0x80024ACE; 0x154CA/0x80024CCA; 0x15AAA/0x800252AA; 0x193BE/0x80028BBE; 0x1A2D6/0x80029AD6; 0x1C31E/0x8002BB1E; 0x2007A/0x8002F87A; 0x202E6/0x8002FAE6; 0x2FFEE/0x8003F7EE; 0x3009A/0x8003F89A; 0x39ED6/0x800496D6; 0x3AD3E/0x8004A53E; 0x40976/0x80050176; 0x40FF6/0x800507F6 |
| SLPS_035.53 | 150 | 16 | 149 | 0x3803/0x80013003; 0x63D7/0x80015BD7; 0x63FB/0x80015BFB; 0xB4FF/0x8001ACFF; 0xB66B/0x8001AE6B; 0xB697/0x8001AE97; 0xB6AB/0x8001AEAB; 0xB6C7/0x8001AEC7; 0xB76B/0x8001AF6B; 0xB77F/0x8001AF7F; 0xB7AB/0x8001AFAB; 0xB7EB/0x8001AFEB; 0xB7FB/0x8001AFFB; 0xB81B/0x8001B01B; 0xB85B/0x8001B05B; 0xB877/0x8001B077; 0xB99B/0x8001B19B; 0xB9A7/0x8001B1A7; 0xB9B7/0x8001B1B7; 0xB9EF/0x8001B1EF; 0xBA03/0x8001B203; 0xC2EF/0x8001BAEF; 0xC6FF/0x8001BEFF; 0xC793/0x8001BF93; 0xC99F/0x8001C19F |
| SLPS_035.53 | 150 | 32 | 111 | 0x3803/0x80013003; 0x63D7/0x80015BD7; 0x63FB/0x80015BFB; 0xB4FF/0x8001ACFF; 0xB66B/0x8001AE6B; 0xB697/0x8001AE97; 0xB6AB/0x8001AEAB; 0xB6C7/0x8001AEC7; 0xB76B/0x8001AF6B; 0xB77F/0x8001AF7F; 0xB7AB/0x8001AFAB; 0xB7EB/0x8001AFEB; 0xB7FB/0x8001AFFB; 0xB81B/0x8001B01B; 0xB85B/0x8001B05B; 0xB877/0x8001B077; 0xB99B/0x8001B19B; 0xB9A7/0x8001B1A7; 0xB9B7/0x8001B1B7; 0xB9EF/0x8001B1EF; 0xBA03/0x8001B203; 0xC2EF/0x8001BAEF; 0xC6FF/0x8001BEFF; 0xC793/0x8001BF93; 0xC99F/0x8001C19F |
| DATA.BIN_ENTRY0 | 50 | 16 | 46 | 0x3E1C/TIDAK TAHU (entry0 runtime base); 0x4DE0/TIDAK TAHU (entry0 runtime base); 0x504C/TIDAK TAHU (entry0 runtime base); 0x54BC/TIDAK TAHU (entry0 runtime base); 0x5554/TIDAK TAHU (entry0 runtime base); 0x56E4/TIDAK TAHU (entry0 runtime base); 0x5A14/TIDAK TAHU (entry0 runtime base); 0x9214/TIDAK TAHU (entry0 runtime base); 0x927C/TIDAK TAHU (entry0 runtime base); 0x99D4/TIDAK TAHU (entry0 runtime base); 0x9A38/TIDAK TAHU (entry0 runtime base); 0x9AE4/TIDAK TAHU (entry0 runtime base); 0x9B58/TIDAK TAHU (entry0 runtime base); 0x9BAC/TIDAK TAHU (entry0 runtime base); 0x9C28/TIDAK TAHU (entry0 runtime base); 0xA4BC/TIDAK TAHU (entry0 runtime base); 0xA73B/TIDAK TAHU (entry0 runtime base); 0xAEC4/TIDAK TAHU (entry0 runtime base); 0xD49C/TIDAK TAHU (entry0 runtime base); 0xD6C0/TIDAK TAHU (entry0 runtime base); 0xD858/TIDAK TAHU (entry0 runtime base); 0xD94C/TIDAK TAHU (entry0 runtime base); 0xED40/TIDAK TAHU (entry0 runtime base); 0xF014/TIDAK TAHU (entry0 runtime base); 0xF09C/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 50 | 32 | 0 | none |
| DATA.BIN_ENTRY0 | 60 | 16 | 119 | 0x914/TIDAK TAHU (entry0 runtime base); 0xF1F/TIDAK TAHU (entry0 runtime base); 0x1133/TIDAK TAHU (entry0 runtime base); 0x181C/TIDAK TAHU (entry0 runtime base); 0x1C10/TIDAK TAHU (entry0 runtime base); 0x1ECC/TIDAK TAHU (entry0 runtime base); 0x1FA4/TIDAK TAHU (entry0 runtime base); 0x232C/TIDAK TAHU (entry0 runtime base); 0x2593/TIDAK TAHU (entry0 runtime base); 0x2778/TIDAK TAHU (entry0 runtime base); 0x2868/TIDAK TAHU (entry0 runtime base); 0x2894/TIDAK TAHU (entry0 runtime base); 0x2E04/TIDAK TAHU (entry0 runtime base); 0x336C/TIDAK TAHU (entry0 runtime base); 0x34C0/TIDAK TAHU (entry0 runtime base); 0x38C4/TIDAK TAHU (entry0 runtime base); 0x46C0/TIDAK TAHU (entry0 runtime base); 0x4890/TIDAK TAHU (entry0 runtime base); 0x4B08/TIDAK TAHU (entry0 runtime base); 0x5038/TIDAK TAHU (entry0 runtime base); 0x5333/TIDAK TAHU (entry0 runtime base); 0x57F0/TIDAK TAHU (entry0 runtime base); 0x5930/TIDAK TAHU (entry0 runtime base); 0x5BE8/TIDAK TAHU (entry0 runtime base); 0x5C27/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 60 | 32 | 3 | 0xF1F/TIDAK TAHU (entry0 runtime base); 0x1133/TIDAK TAHU (entry0 runtime base); 0x196D8/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 100 | 16 | 145 | 0x47D/TIDAK TAHU (entry0 runtime base); 0x50D/TIDAK TAHU (entry0 runtime base); 0x84D/TIDAK TAHU (entry0 runtime base); 0xC32/TIDAK TAHU (entry0 runtime base); 0xC42/TIDAK TAHU (entry0 runtime base); 0xC52/TIDAK TAHU (entry0 runtime base); 0xE6A/TIDAK TAHU (entry0 runtime base); 0xE7A/TIDAK TAHU (entry0 runtime base); 0xE8A/TIDAK TAHU (entry0 runtime base); 0x106E/TIDAK TAHU (entry0 runtime base); 0x107E/TIDAK TAHU (entry0 runtime base); 0x108E/TIDAK TAHU (entry0 runtime base); 0x1276/TIDAK TAHU (entry0 runtime base); 0x1286/TIDAK TAHU (entry0 runtime base); 0x1296/TIDAK TAHU (entry0 runtime base); 0x1506/TIDAK TAHU (entry0 runtime base); 0x166E/TIDAK TAHU (entry0 runtime base); 0x1A6E/TIDAK TAHU (entry0 runtime base); 0x21BD/TIDAK TAHU (entry0 runtime base); 0x36A8/TIDAK TAHU (entry0 runtime base); 0x39A8/TIDAK TAHU (entry0 runtime base); 0x411C/TIDAK TAHU (entry0 runtime base); 0x41D8/TIDAK TAHU (entry0 runtime base); 0x42A0/TIDAK TAHU (entry0 runtime base); 0x435C/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 100 | 32 | 13 | 0x1A6E/TIDAK TAHU (entry0 runtime base); 0x72C2/TIDAK TAHU (entry0 runtime base); 0x7662/TIDAK TAHU (entry0 runtime base); 0x767A/TIDAK TAHU (entry0 runtime base); 0x7692/TIDAK TAHU (entry0 runtime base); 0xB6FA/TIDAK TAHU (entry0 runtime base); 0xF296/TIDAK TAHU (entry0 runtime base); 0x10686/TIDAK TAHU (entry0 runtime base); 0x127FE/TIDAK TAHU (entry0 runtime base); 0x12816/TIDAK TAHU (entry0 runtime base); 0x17D16/TIDAK TAHU (entry0 runtime base); 0x194E0/TIDAK TAHU (entry0 runtime base); 0x194F8/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 150 | 16 | 72 | 0xDF2/TIDAK TAHU (entry0 runtime base); 0x3887/TIDAK TAHU (entry0 runtime base); 0x393F/TIDAK TAHU (entry0 runtime base); 0x6CEF/TIDAK TAHU (entry0 runtime base); 0x6D0B/TIDAK TAHU (entry0 runtime base); 0x6D3B/TIDAK TAHU (entry0 runtime base); 0x6D57/TIDAK TAHU (entry0 runtime base); 0x6EA3/TIDAK TAHU (entry0 runtime base); 0x6EBF/TIDAK TAHU (entry0 runtime base); 0x717F/TIDAK TAHU (entry0 runtime base); 0x719F/TIDAK TAHU (entry0 runtime base); 0x7863/TIDAK TAHU (entry0 runtime base); 0x7F4B/TIDAK TAHU (entry0 runtime base); 0x921F/TIDAK TAHU (entry0 runtime base); 0x9233/TIDAK TAHU (entry0 runtime base); 0x9287/TIDAK TAHU (entry0 runtime base); 0x929B/TIDAK TAHU (entry0 runtime base); 0x92DF/TIDAK TAHU (entry0 runtime base); 0x92F3/TIDAK TAHU (entry0 runtime base); 0x9333/TIDAK TAHU (entry0 runtime base); 0x9343/TIDAK TAHU (entry0 runtime base); 0xA942/TIDAK TAHU (entry0 runtime base); 0xAE73/TIDAK TAHU (entry0 runtime base); 0xAE87/TIDAK TAHU (entry0 runtime base); 0xB65B/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY0 | 150 | 32 | 65 | 0xDF2/TIDAK TAHU (entry0 runtime base); 0x3887/TIDAK TAHU (entry0 runtime base); 0x393F/TIDAK TAHU (entry0 runtime base); 0x6CEF/TIDAK TAHU (entry0 runtime base); 0x6D0B/TIDAK TAHU (entry0 runtime base); 0x6D3B/TIDAK TAHU (entry0 runtime base); 0x6D57/TIDAK TAHU (entry0 runtime base); 0x6EA3/TIDAK TAHU (entry0 runtime base); 0x6EBF/TIDAK TAHU (entry0 runtime base); 0x717F/TIDAK TAHU (entry0 runtime base); 0x719F/TIDAK TAHU (entry0 runtime base); 0x7863/TIDAK TAHU (entry0 runtime base); 0x7F4B/TIDAK TAHU (entry0 runtime base); 0x921F/TIDAK TAHU (entry0 runtime base); 0x9233/TIDAK TAHU (entry0 runtime base); 0x9287/TIDAK TAHU (entry0 runtime base); 0x929B/TIDAK TAHU (entry0 runtime base); 0x92DF/TIDAK TAHU (entry0 runtime base); 0x92F3/TIDAK TAHU (entry0 runtime base); 0x9333/TIDAK TAHU (entry0 runtime base); 0x9343/TIDAK TAHU (entry0 runtime base); 0xAE73/TIDAK TAHU (entry0 runtime base); 0xAE87/TIDAK TAHU (entry0 runtime base); 0xB65B/TIDAK TAHU (entry0 runtime base); 0xD387/TIDAK TAHU (entry0 runtime base) |
| DATA.BIN_ENTRY1 | 50 | 16 | 169 | 0x4B84/0x800B1FD4 (candidate; runtime unverified); 0x5C4C/0x800B309C (candidate; runtime unverified); 0x72E0/0x800B4730 (candidate; runtime unverified); 0x765C/0x800B4AAC (candidate; runtime unverified); 0x957C/0x800B69CC (candidate; runtime unverified); 0xB608/0x800B8A58 (candidate; runtime unverified); 0xD4BC/0x800BA90C (candidate; runtime unverified); 0xDD04/0x800BB154 (candidate; runtime unverified); 0x1B77C/0x800C8BCC (candidate; runtime unverified); 0x1BCE8/0x800C9138 (candidate; runtime unverified); 0x1CF40/0x800CA390 (candidate; runtime unverified); 0x1DC90/0x800CB0E0 (candidate; runtime unverified); 0x1F784/0x800CCBD4 (candidate; runtime unverified); 0x27608/0x800D4A58 (candidate; runtime unverified); 0x28634/0x800D5A84 (candidate; runtime unverified); 0x294B8/0x800D6908 (candidate; runtime unverified); 0x2B3FC/0x800D884C (candidate; runtime unverified); 0x2B770/0x800D8BC0 (candidate; runtime unverified); 0x2E598/0x800DB9E8 (candidate; runtime unverified); 0x2E758/0x800DBBA8 (candidate; runtime unverified); 0x2E838/0x800DBC88 (candidate; runtime unverified); 0x2F328/0x800DC778 (candidate; runtime unverified); 0x33E50/0x800E12A0 (candidate; runtime unverified); 0x3441C/0x800E186C (candidate; runtime unverified); 0x347C4/0x800E1C14 (candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 50 | 32 | 0 | none |
| DATA.BIN_ENTRY1 | 60 | 16 | 449 | 0x28BC/0x800AFD0C (candidate; runtime unverified); 0x4BD8/0x800B2028 (candidate; runtime unverified); 0x5C9C/0x800B30EC (candidate; runtime unverified); 0x6920/0x800B3D70 (candidate; runtime unverified); 0x6938/0x800B3D88 (candidate; runtime unverified); 0x6950/0x800B3DA0 (candidate; runtime unverified); 0x6980/0x800B3DD0 (candidate; runtime unverified); 0x6998/0x800B3DE8 (candidate; runtime unverified); 0x7EA4/0x800B52F4 (candidate; runtime unverified); 0x7FD3/0x800B5423 (candidate; runtime unverified); 0x8023/0x800B5473 (candidate; runtime unverified); 0x80DF/0x800B552F (candidate; runtime unverified); 0x8874/0x800B5CC4 (candidate; runtime unverified); 0x888C/0x800B5CDC (candidate; runtime unverified); 0x88A4/0x800B5CF4 (candidate; runtime unverified); 0x88D4/0x800B5D24 (candidate; runtime unverified); 0x88EC/0x800B5D3C (candidate; runtime unverified); 0x8D50/0x800B61A0 (candidate; runtime unverified); 0x8D68/0x800B61B8 (candidate; runtime unverified); 0x8D80/0x800B61D0 (candidate; runtime unverified); 0x8DB0/0x800B6200 (candidate; runtime unverified); 0x8DC8/0x800B6218 (candidate; runtime unverified); 0x95A4/0x800B69F4 (candidate; runtime unverified); 0x9A84/0x800B6ED4 (candidate; runtime unverified); 0x9B2B/0x800B6F7B (candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 60 | 32 | 4 | 0x8C3A1/0x801397F1 (candidate; runtime unverified); 0x8C595/0x801399E5 (candidate; runtime unverified); 0x8C6A5/0x80139AF5 (candidate; runtime unverified); 0x8C725/0x80139B75 (candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 100 | 16 | 506 | 0x3FF7/0x800B1447 (candidate; runtime unverified); 0x5572/0x800B29C2 (candidate; runtime unverified); 0x5FF8/0x800B3448 (candidate; runtime unverified); 0x7A1E/0x800B4E6E (candidate; runtime unverified); 0x81F2/0x800B5642 (candidate; runtime unverified); 0x824E/0x800B569E (candidate; runtime unverified); 0x92A8/0x800B66F8 (candidate; runtime unverified); 0x9F54/0x800B73A4 (candidate; runtime unverified); 0xA76C/0x800B7BBC (candidate; runtime unverified); 0xA998/0x800B7DE8 (candidate; runtime unverified); 0xA9AC/0x800B7DFC (candidate; runtime unverified); 0xAE66/0x800B82B6 (candidate; runtime unverified); 0xD2DA/0x800BA72A (candidate; runtime unverified); 0xD306/0x800BA756 (candidate; runtime unverified); 0xD332/0x800BA782 (candidate; runtime unverified); 0xD4F2/0x800BA942 (candidate; runtime unverified); 0xD51E/0x800BA96E (candidate; runtime unverified); 0xD54A/0x800BA99A (candidate; runtime unverified); 0xD5F2/0x800BAA42 (candidate; runtime unverified); 0xD668/0x800BAAB8 (candidate; runtime unverified); 0xD6A2/0x800BAAF2 (candidate; runtime unverified); 0xD718/0x800BAB68 (candidate; runtime unverified); 0xD746/0x800BAB96 (candidate; runtime unverified); 0xD7BC/0x800BAC0C (candidate; runtime unverified); 0xD7EA/0x800BAC3A (candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 100 | 32 | 24 | 0xAE66/0x800B82B6 (candidate; runtime unverified); 0x20A46/0x800CDE96 (candidate; runtime unverified); 0x20DC6/0x800CE216 (candidate; runtime unverified); 0x20F72/0x800CE3C2 (candidate; runtime unverified); 0x5C3AE/0x801097FE (candidate; runtime unverified); 0x68DA2/0x801161F2 (candidate; runtime unverified); 0x6B7EE/0x80118C3E (candidate; runtime unverified); 0x6B82E/0x80118C7E (candidate; runtime unverified); 0x6BA0E/0x80118E5E (candidate; runtime unverified); 0x6BA4E/0x80118E9E (candidate; runtime unverified); 0x6F87A/0x8011CCCA (candidate; runtime unverified); 0x741D2/0x80121622 (candidate; runtime unverified); 0x77F1E/0x8012536E (candidate; runtime unverified); 0x78096/0x801254E6 (candidate; runtime unverified); 0x814A2/0x8012E8F2 (candidate; runtime unverified); 0x88242/0x80135692 (candidate; runtime unverified); 0x8B33E/0x8013878E (candidate; runtime unverified); 0x8B37E/0x801387CE (candidate; runtime unverified); 0x8C3AD/0x801397FD (candidate; runtime unverified); 0x8C567/0x801399B7 (candidate; runtime unverified); 0x8C5A1/0x801399F1 (candidate; runtime unverified); 0x8C677/0x80139AC7 (candidate; runtime unverified); 0x8C6B1/0x80139B01 (candidate; runtime unverified); 0x8CB54/0x80139FA4 (candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 150 | 16 | 484 | 0x4C0C/0x800B205C (candidate; runtime unverified); 0x5CD0/0x800B3120 (candidate; runtime unverified); 0x9A5F/0x800B6EAF (candidate; runtime unverified); 0x9A8B/0x800B6EDB (candidate; runtime unverified); 0x9A94/0x800B6EE4 (candidate; runtime unverified); 0xC5C7/0x800B9A17 (candidate; runtime unverified); 0xC6BF/0x800B9B0F (candidate; runtime unverified); 0xD0FF/0x800BA54F (candidate; runtime unverified); 0xD217/0x800BA667 (candidate; runtime unverified); 0xD2CF/0x800BA71F (candidate; runtime unverified); 0xD2FB/0x800BA74B (candidate; runtime unverified); 0xD327/0x800BA777 (candidate; runtime unverified); 0xD3F7/0x800BA847 (candidate; runtime unverified); 0xD4E7/0x800BA937 (candidate; runtime unverified); 0xD513/0x800BA963 (candidate; runtime unverified); 0xD53F/0x800BA98F (candidate; runtime unverified); 0xEAB3/0x800BBF03 (candidate; runtime unverified); 0xF54B/0x800BC99B (candidate; runtime unverified); 0xF58F/0x800BC9DF (candidate; runtime unverified); 0x10E97/0x800BE2E7 (candidate; runtime unverified); 0x1354F/0x800C099F (candidate; runtime unverified); 0x1380F/0x800C0C5F (candidate; runtime unverified); 0x13887/0x800C0CD7 (candidate; runtime unverified); 0x146D3/0x800C1B23 (candidate; runtime unverified); 0x14743/0x800C1B93 (candidate; runtime unverified) |
| DATA.BIN_ENTRY1 | 150 | 32 | 442 | 0x9A5F/0x800B6EAF (candidate; runtime unverified); 0x9A8B/0x800B6EDB (candidate; runtime unverified); 0xC5C7/0x800B9A17 (candidate; runtime unverified); 0xC6BF/0x800B9B0F (candidate; runtime unverified); 0xD0FF/0x800BA54F (candidate; runtime unverified); 0xD217/0x800BA667 (candidate; runtime unverified); 0xD2CF/0x800BA71F (candidate; runtime unverified); 0xD2FB/0x800BA74B (candidate; runtime unverified); 0xD327/0x800BA777 (candidate; runtime unverified); 0xD3F7/0x800BA847 (candidate; runtime unverified); 0xD4E7/0x800BA937 (candidate; runtime unverified); 0xD513/0x800BA963 (candidate; runtime unverified); 0xD53F/0x800BA98F (candidate; runtime unverified); 0xEAB3/0x800BBF03 (candidate; runtime unverified); 0xF54B/0x800BC99B (candidate; runtime unverified); 0xF58F/0x800BC9DF (candidate; runtime unverified); 0x10E97/0x800BE2E7 (candidate; runtime unverified); 0x1354F/0x800C099F (candidate; runtime unverified); 0x1380F/0x800C0C5F (candidate; runtime unverified); 0x13887/0x800C0CD7 (candidate; runtime unverified); 0x146D3/0x800C1B23 (candidate; runtime unverified); 0x14743/0x800C1B93 (candidate; runtime unverified); 0x1478B/0x800C1BDB (candidate; runtime unverified); 0x1499F/0x800C1DEF (candidate; runtime unverified); 0x149E3/0x800C1E33 (candidate; runtime unverified) |

## Sequence 100/120/150/180/200

Dicari contiguous LE halfword/word; keberadaan sequence tidak menetapkan penggunaannya.
- SLPS_035.53 u16: 0 hit; TIDAK DITEMUKAN
- SLPS_035.53 u32: 0 hit; TIDAK DITEMUKAN
- DATA.BIN_ENTRY0 u16: 0 hit; TIDAK DITEMUKAN
- DATA.BIN_ENTRY0 u32: 0 hit; TIDAK DITEMUKAN
- DATA.BIN_ENTRY1 u16: 0 hit; TIDAK DITEMUKAN
- DATA.BIN_ENTRY1 u32: 0 hit; TIDAK DITEMUKAN
TIDAK TAHU: tidak ditemukan sequence contiguous persis; tabel berpadded atau urutan berbeda belum disangkal.

## String ASCII/Shift-JIS

Pencarian literal saja; bila teks UI memakai indeks tile/font, pemetaan glyph belum dibuat.
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

## Batas

- Tidak memberi label Barrier cost/income/Chakra release pada angka tanpa operand flow yang terbukti.
- Xref/pembaca numeric candidate TIDAK TAHU sampai alamat tabel dihubungkan ke instruksi pembaca.
- Pemetaan glyph tile/font TIDAK TAHU.
- Entry 1 menggunakan base statis kandidat 0x800AD450; runtime mapping belum validated.
- Statis saja; tidak ada emulator/gameplay.
