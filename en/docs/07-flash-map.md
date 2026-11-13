# SPI flash map

The SPI flash is 8 MB (`0x800000`). The addresses shown by U-Boot are remapped: **offset in flash = U-Boot address − `0x88100000`**.

| Offset in flash | Size | Content |
|---|---|---|
| `0x000000` | 64 KB | Device tree (DTB) |
| `0x020800` | | `hwsetting` |
| `0x021440` | | U-Boot (first stage) |
| `0x0840E0` | | FSBL |
| `0x094C00` | | Rescue U-Boot |
| `0x0c0000` | `0x40000` | Audio firmware |
| `0x100000` | `0x2f0000` | **zImage** (Linux kernel) |
| `0x3f0000` | `0x3ff000` | **rd.gz** (ramdisk) |
| `0x7ef000` | `0x10000` | **vendor** (MAC, serial number, factory data) |
| `0x7ff000` | `0x1000` | **FIS directory** (the partition table, blank in this case) |

This layout is consistent with the DS418 one described on Synoforum: `RedBoot` 0x000000–0x100000, `zImage` 0x100000–0x3f0000, `rd.gz` 0x3f0000–0x7ef000, `vendor` 0x7ef000–0x7ff000.

## Table to rebuild

| Entry | `flash_base` | `size` |
|---|---|---|
| `RedBoot` | `0x000000` | `0x100000` |
| `zImage` | `0x100000` | `0x2f0000` |
| `rd.gz` | `0x3f0000` | `0x3ff000` |
| `vendor` | `0x7ef000` | `0x10000` |
| `FIS directory` | `0x7ff000` | `0x1000` |

For every entry: `mem_base = 0` and `entry_point = 0`, and `data_length` equal to `size`.
