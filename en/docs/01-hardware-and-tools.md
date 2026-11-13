# Hardware and tools

## NAS hardware

| Component | Detail |
|---|---|
| Model | Synology DS218 (confirmed by the logs: `Synology Model: DS218`) |
| Board | `HDR23L1` v1.1 (silkscreen read from photos of the DS218 board) |
| SoC | Realtek RTD1296 (64-bit ARM) |
| RAM | 2 GiB of DDR4 at 1600 MHz, in 4 chips. Confirmed by U-Boot's `bdinfo`: `DC0 DDR4, total size is 4Gb(x16)x2=8Gb` and `DC1 DDR4, total size is 4Gb(x16)x2=8Gb` (2 channels × 2 chips of 4 Gbit). [TO VERIFY: exact chip part numbers. The **U3** reference is the one the author used on his own board] |
| Flash | SPI NOR MXIC MX25L6445E, 8 MB, 4 KB sectors |
| Console | UART connector J2, 115200 baud, 8N1, **3.3 V** level |

## Tools used

- A USB-serial adapter (FT232 chip) set to **3.3 V** (never use 5 V on this connector).
- PuTTY (serial, with session logging to a file).
- Synology Assistant (NAS discovery and web installation wizard).
- The installation file `DSM_DS218_25556.pat` (DSM 6.2.4-25556, about 236 MB), downloaded from Synology's official website.
- A Windows PC for downloading and for analysing the dumps.

[INSERT PHOTO: DS218 board, overview with the UART connector J2 marked]
[INSERT PHOTO: USB-serial adapter connected to J2 (hide any personal information that is visible)]
[INSERT PHOTO: the 4 RAM chips area, with U3 marked]
