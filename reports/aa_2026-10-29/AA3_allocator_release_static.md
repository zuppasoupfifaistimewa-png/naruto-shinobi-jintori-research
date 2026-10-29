# AA3 — allocator release path (static evidence)

**Status AA3: SEBAGIAN.**  
**Confidence:** K4 for the instruction-level release/accounting logic; K2 for the identification of one live checkpoint heap block as a 2,900-byte-request-compatible allocation. The requested post-free values have not been observed in a new emulator run.

## Provenance

- Static disassembly came from Actions run [40515356524](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524), job [122227786744](https://github.com/zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research/actions/runs/40515356524/job/122227786744), artifact ID 12739676233.
- Artifact path: `step5-output/compare/spimdisasm-output/main_text_80010000.text.s`
- Extracted text size: 5,842,862 bytes; SHA-256 `d655bda18ee9e87132b63ddc2c85a96da615df92658329490958f7dec9b7d3c7`.
- Runtime snapshot used only for RAM observations: Release checkpoint `naruto-checkpoint-39262213468`, 21,163,286 bytes, SHA-256 `00fab82601f4acee6e250c9009234dfb469d6f4d457cfb8413a1e874204f6c3d`. The savestate and RAM dump are not committed.

## Release routine FUN_8002DFE4 (virtual address = EXE address; EXE base 0x80010000)

Relevant instruction excerpt from the disassembly:

```asm
8002DFE4  addiu $sp, $sp, -0x18
8002DFE8  sw    $ra, 0x10($sp)
8002DFEC  lui   $v0, %hi(D_800A2918)
8002DFF0  addiu $a1, $v0, %lo(D_800A2918)
8002DFF4  lw    $v0, 0xC($a1)
8002DFF8  nop
8002DFFC  beqz  $v0, .L8002E060
8002E000  nop
8002E004  lw    $v0, -0x4($a0)
8002E008  nop
8002E00C  addiu $v0, $v0, -1
8002E010  sll   $v0, $v0, 3
8002E014  lw    $v1, 0x8($a1)
8002E018  nop
8002E01C  subu  $v1, $v1, $v0
8002E020  sw    $v1, 0x8($a1)
8002E024  lw    $v0, 0xA8($gp)
8002E028  nop
8002E02C  bne   $a0, $v0, .L8002E040
8002E030  lui   $v1, %hi(D_800A2918)
8002E034  sw    $zero, 0xA8($gp)
8002E038  j     .L8002E050
8002E03C  addiu $v1, $v1, %lo(D_800A2918)
8002E040  jal   func_80035BB8
8002E044  nop
8002E050  lw    $v0, 0xC($v1)
8002E054  nop
8002E058  addiu $v0, $v0, -1
8002E05C  sw    $v0, 0xC($v1)
8002E060  lw    $ra, 0x10($sp)
8002E064  nop
8002E068  jr    $ra
8002E06C  addiu $sp, $sp, 0x18
```

Direct implications of these instructions:

1. Input `$a0` is treated as the allocated payload pointer. The routine first reads the 32-bit header at `$a0-4`.
2. If `D_800A2918+0xC` (the tracked allocation count) is zero, the bookkeeping body is skipped.
3. Otherwise, it computes `(header - 1) * 8`, subtracts that byte count from `D_800A2918+8`, and decrements the count at `D_800A2918+0xC`.
4. If the pointer equals the cached pointer at `0xA8($gp)`, that cache is cleared. Otherwise it calls `func_80035BB8` to return/coalesce the block in the allocator's free list.

## What the previously overlooked addresses mean

The complete disassembly of allocator `func_8002DEC4` contains:

```asm
8002DEF4  lw    $v0, -0x4($a1)
8002DEF8  nop
8002DEFC  addiu $v0, $v0, -1
8002DF00  sll   $v0, $v0, 3
8002DF04  lw    $v1, 0x8($a0)
8002DF08  nop
8002DF0C  addu  $v0, $v0, $v1
8002DF10  sw    $v0, 0x8($a0)
```

`0x8002DEF8` and `0x8002DF08` are actual NOP instructions in the disassembly, not omitted control-flow targets. Each sits after a load and before the loaded register is consumed; they do no data update themselves. They are executed NOP/load-delay slots, not evidence that the surrounding accounting instructions can be skipped.

## Meaning of header “-1”

The underlying allocator `func_80035B08` rounds the requested payload size to an 8-byte unit and stores a count with one additional 8-byte allocator-header unit. The returned payload pointer is 8 bytes after the allocator block header. Therefore, when accounting or freeing, the code uses `(header - 1) << 3` to remove that one metadata unit and recover the rounded payload capacity. It does **not** mean “minus one byte.”

For a 2,900-byte request:
- `ceil(2900 / 8) = 363) payload units;
- stored header count `= 363 + 1 = 364 = 0x16C`;
- accounted/freed payload capacity `= (0x16C - 1) * 8 = 2,904 = 0xB58` bytes.

The header stores the rounded unit count, so `0x16C` alone cannot distinguish an exact 2,900-byte request from another request in the same 8-byte rounding interval.

## Checkpoint snapshot: one block compatible with that size

The checkpoint's RAM bytes show a word `0x16C` at `0x801D7FBC`; the naturally aligned payload candidate is `a0 = 0x801D7FC0`. This location lies between the free-list nodes, whose observed links are `0x8013F450 -> 0x801F7FF8 -> 0x8013F450`, and is not itself one of those nodes.

| Value | Before (saved checkpoint) | Static projection if this block is freed |
|---|---:|---:|
| `a0` | `0x801D7FC0` | same input pointer |
| header at `[a0-4]` | `0x0000016C` | `0x0000016C` if inserted as a standalone free-list block; not runtime observed |
| `[a0+8]` at `0x801D7FC8` | `0x00000008` | expected unchanged by the traced release path; not runtime observed |
| `D_800A2918+8` total-size counter | `0x00081920` | `0x00080DC8` after subtracting `0xB58` |
| `D_800A2918+0xC` allocation count | `0x00000014` (20) | `0x00000013` (19) |

The “after” column is a **static projection from the instructions and checkpoint snapshot**, not a watchpoint trace and not evidence that `FUN_8002DFE4(0x801D7FC0)` actually executed. The snapshot header is strongly compatible with a 2,900-byte request after rounding, but the original request size/call-site has not been tied to this pointer at runtime. That is the remaining AA3 gap.


## Additional real allocator call-site found in the same verified disassembly

A static allocation/free lifecycle is directly visible at `0x80031508` through the caller region in `main_text_80010000.text.s`:

```asm
80031508  jal   func_8002DEC4
8003150C  addiu $a0, $zero, 0x204C   ; 8268-byte request
80031510  sw    $v0, 0xB0($gp)       ; retain returned payload pointer
...
80031524  lw    $a0, 0xB0($gp)
80031528  jal   func_80035D48
8003152C  addiu $a2, $zero, 0x204C   ; initialize 8268 bytes
...
80031594  lw    $a0, 0xB0($gp)
8003159C  beqz  $a0, .L800315B4
800315A4  jal   func_8002DFE4         ; release pointer when non-null
800315AC  sw    $zero, 0xB0($gp)      ; clear retained pointer
```

For this call-site, the allocator's statically established unit rule predicts `ceil(8268/8)=1034` payload units (8,272 bytes), a header count of `1035 = 0x40B`, and `(0x40B-1)<<3 = 0x2050` bytes of accounted capacity. Here `$a0=0x204C` at the allocation call is the **requested size**, not the returned pointer. The payload pointer returned in `$v0` is stored at `0xB0($gp)`, passed as `$a0` to `FUN_8002DFE4` in the release path, then cleared from the global.

This adds a directly inspectable static call-and-release example (K4 for the instruction sequence and arithmetic), but it still does not provide runtime values for the actual returned pointer's `[a0-4]` header or `[a0+8]` before/after release. Those remain **UNKNOWN / not captured**, because AA1 has not established successful restoration of the target checkpoint and AA2 watchpoints were not run.
