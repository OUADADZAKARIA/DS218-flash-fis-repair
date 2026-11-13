# Cartographie de la flash SPI

La flash SPI fait 8 Mo (`0x800000`). Les adresses affichées par U-Boot sont remappées : **offset dans la flash = adresse U-Boot − `0x88100000`**.

| Offset dans la flash | Taille | Contenu |
|---|---|---|
| `0x000000` | 64 Ko | Arbre de périphériques (DTB) |
| `0x020800` | | `hwsetting` |
| `0x021440` | | U-Boot (premier étage) |
| `0x0840E0` | | FSBL |
| `0x094C00` | | U-Boot de secours (rescue) |
| `0x0c0000` | `0x40000` | Firmware audio |
| `0x100000` | `0x2f0000` | **zImage** (noyau Linux) |
| `0x3f0000` | `0x3ff000` | **rd.gz** (ramdisk) |
| `0x7ef000` | `0x10000` | **vendor** (MAC, numéro de série, données d'usine) |
| `0x7ff000` | `0x1000` | **FIS directory** (la table de partitions, vide dans ce cas) |

Cette disposition est cohérente avec celle d'un DS418 décrite sur Synoforum : `RedBoot` 0x000000–0x100000, `zImage` 0x100000–0x3f0000, `rd.gz` 0x3f0000–0x7ef000, `vendor` 0x7ef000–0x7ff000.

## Table à reconstruire

| Entrée | `flash_base` | `size` |
|---|---|---|
| `RedBoot` | `0x000000` | `0x100000` |
| `zImage` | `0x100000` | `0x2f0000` |
| `rd.gz` | `0x3f0000` | `0x3ff000` |
| `vendor` | `0x7ef000` | `0x10000` |
| `FIS directory` | `0x7ff000` | `0x1000` |

Pour toutes les entrées : `mem_base = 0` et `entry_point = 0`, et `data_length` égal à `size`.
