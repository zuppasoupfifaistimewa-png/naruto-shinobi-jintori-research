# Ghidra context scan — DATA.BIN entry 0 RNG dan seed setter

Tanggal: 27 Oktober 2026  
Run awal: [#40455197588](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455197588)  
Run yang menambahkan pemindaian edge masuk lokal: [#40455557190](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40455557190)  
Metode: Ghidra 12.2, MIPS little-endian 32-bit, `-noanalysis`, jendela terarah saja. Tidak ada emulator, gameplay, input atau savestate.

## Identitas dan batas

- DATA.BIN entry 0: file offset `0x5F800`, ukuran 110.536 byte, SHA-256 `56ee7d3b195b0708bd5f9163d354f0173a828430c9467d410e822b1793d316d4`.
- Base analisis `0x800AD000) **hipotetis**, bukan hasil verifikasi loader runtime.
- Seluruh penjelasan alamat RAM pada dokumen ini bergantung pada base kandidat tersebut.

## Satu-satunya direct call ke kandidat seed setter

Call site `0x800AF2AC` didekode Ghidra sebagai `jal 0x80035DA8`. Konteks terdekat:

~~~asm
800af2a4  jal 0x80037138
800af2a8  li  a0,-0x1
800af2ac  jal 0x80035da8
800af2b0  move a0,v0
~~~

MIPS menjalankan instruksi delay-slot `0x800AF2B0` setelah fungsi dipanggil; maka nilai argumen saat memasuki `0x80035DA8` adalah `$a0 = -1`. Badan kandidat setter menyimpan `$a0` ke global RNG `0x800A3118` melalui store pada delay slot `jr $ra`.

**Kesimpulan statis:** jika jalur ini berjalan dan entry 0 dimuat pada base kandidat, ia mengatur state RNG menjadi `0xFFFFFFFF` sebelum berpindah ke `0x800AF710`. Ini merupakan bukti lebih kuat daripada sekadar tebakan seed; namun tidak membuktikan kapan/ apakah jalur ini dieksekusi di runtime atau bahwa tidak ada reseed melalui pointer/overlay lain. Scan mentah seluruh file yang dipilih menemukan hanya satu kata JAL menuju `0x80035DA8`, di lokasi ini.

## Empat kandidat JAL entry 0 yang menuju RNG

| Call site hipotetis | Ghidra target flow | Incoming control flow dari jendela terdekode | Penilaian |
|---:|---|---|---|
| `0x800BB2D8` | `0x80035D78` | `bne v0,zero,0x800BB2D8` dari `0x800BB340` | **Pasti** sebagai JAL target dan ada branch masuk lokal. Setelah RNG, caller memanggil helper lalu `divu/mfhi`, konsisten dengan pemilihan modulo berbatas. |
| `0x800BB2FC` | `0x80035D78` | `bne v0,zero,0x800BB2FC` dari `0x800BB2F0` | **Pasti** sebagai JAL target dan cabang masuk eksplisit. Instruksi `break 7` sebelumnya berlaku pada cabang lain. |
| `0x800BB748` | `0x80035D78` | Tidak ditemukan di jendela lokal | **Pasti** bahwa kata didekode sebagai JAL; **UNKNOWN** reachability. Call terletak sesudah `j 0x800BBDE4` di `0x800BB740` beserta delay slot `0x800BB744`; perlu xref lebih luas untuk memastikan ia blok target lain atau dead/unreachable code. |
| `0x800BB770` | `0x80035D78` | `beq s4,s1,0x800BB770` dari `0x800BB798` | **Pasti** sebagai JAL target dan ada branch masuk lokal. Konteks memakai hasil RNG dan operasi pembagian/modulo berikutnya. |

Batas fungsi caller tidak diberikan oleh analisis `-noanalysis`, sehingga nama caller entry 0 masih UNKNOWN.

## Dampak pada seed dan caller inventory

- Ada **satu** direct call seed setter yang teridentifikasi secara statis pada base kandidat entry 0; argumennya `-1`.
- Ada **empat** direct JAL instruction sites di entry 0 yang targetnya RNG. Tiga memiliki incoming conditional branch pada konteks lokal; satu (0x800BB748) masih perlu xref/reachability lebih luas.
- Base entry 0 dan waktu eksekusinya tetap provisional. Tidak ada runtime execution.
