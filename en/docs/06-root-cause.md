# Root cause: the flash partition table is blank

The DS218's Linux kernel looks for a **RedBoot**-type partition table (a block called "FIS directory") at offset `0x7ff000` of the SPI flash. This table tells the kernel where `zImage`, `rd.gz` and `vendor` are.

In the case studied, this block contained only `0xFF` bytes (erased flash). Consequences:

1. The kernel exposes only a single `RtkSFC` partition covering the whole 8 MB.
2. Synology's `updater` tool looks for partitions **by name** (`RedBoot`, `zImage`, `rd.gz`, `vendor`). It finds nothing, so it cannot write the new system.
3. It cleans up what it unpacked and reboots, which leaves the NAS in junior mode.
4. The `vendor` partition (which holds the factory MAC address and serial number) is not visible either, hence the empty or random values.

The other flash areas were intact (bootloader, kernel, ramdisk, factory data). Only this 4 KB sector was missing.

## What was ruled out

| Hypothesis | Why it was ruled out |
|---|---|
| Wrong date on the NAS | The clock keeps time and the installer resynchronises it |
| Choosing "Migration" or "Reinstall" | Same result both ways |
| Wrong DSM version | The `.pat` file passes the signature and checksum verification |
| RAM error while uploading the file | The `.pat` checksum was correct |
| Loss of identity (MAC, serial number) | The original data was present in the flash |
