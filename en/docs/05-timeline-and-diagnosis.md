# Diagnosis timeline

1. **Initial finding**: DSM cannot be configured, the NAS stays "Migratable".
2. **Serial UART console connected** to read the boot logs. The boot is unstable, random crashes appear.
3. **Hardware stabilisation**: hot-air reflow of the 4 RAM chips (several times, front and back, mainly U3), cooling, a metal cooling element that also presses on U3, a fan ([hardware intervention](04-hardware-intervention.md)). Boot tests then run without errors.
3b. **RAM tests** (low and high zones) from the command line ([RAM tests](04-hardware-intervention.md#ram-tests-low-and-high-zones)).
3c. **Start of the "command line" phase** on the flash and the system, once the hardware is stable.
4. **Analysis of the installation logs**: the `updater` reports `find mtd partition [RedBoot] by name fail`. The kernel sees only one partition.
5. **Access to the junior-mode shell** (BusyBox v1.16.1) on the serial console.
6. **Flash backup**: two full dumps of 8 388 608 bytes, identical (same SHA-256).
7. **Dump analysis**: offset `0x7ff000` (FIS directory) is entirely `0xFF`. The other areas (kernel, ramdisk, factory data) are present.
8. **Check of the original identity**: the MAC address and serial number found in the flash match the label stuck under the NAS.
9. **Search for the partition names expected** by the `updater` (strings found in the binary): `RedBoot`, `zImage`, `rd.gz`, `vendor`, `FIS directory`.
10. **Comparison with the layout of a DS418** described on the Synoforum forum (see [references](15-references.md)) to deduce the offsets and sizes.
11. **Construction of a 4 KB block** containing 5 entries, verified byte by byte.
12. **Write to the flash**, read back, identical comparison.
13. **Reboot**: the kernel detects 5 partitions.
14. **DSM reinstallation**: the `updater` writes `zImage` and `rd.gz`, the NAS reboots into DSM 6.2.4.
15. **Cold-boot tests** (3 successes), volume creation.

[INSERT PHOTO: Synology Assistant screenshot with the status "Migratable" (hide the IP address, MAC address and serial number)]
[INSERT PHOTO: web wizard with the "Migration" / "Reinstall" choices]

## Signatures in the logs

When you read a log (PuTTY, `.log` file), these lines tell you almost everything. For each signature: what it means and where to go.

| Signature (text to search for) | Meaning | Chapter |
|---|---|---|
| `5-5verify fsbl fail` repeating | The very first loader cannot verify itself: unstable boot (case observed with the faulty RAM) | [hardware intervention](04-hardware-intervention.md) |
| `Oops`, `Internal error`, `kernel BUG at` | Kernel crash. Random from one boot to the next = hardware (RAM) | [hardware intervention](04-hardware-intervention.md) |
| `skb_over_panic` | A memory counter is corrupted (flipped bit): unstable RAM | [hardware intervention](04-hardware-intervention.md) |
| `FATAL: Audio ROS Unexpected interrupt error` | Early crash of the audio coprocessor, seen with unstable RAM | [hardware intervention](04-hardware-intervention.md) |
| `Kernel panic - not syncing` | Kernel halt after a serious error | [hardware intervention](04-hardware-intervention.md) |
| `find mtd partition [RedBoot] by name fail` | The `updater` cannot find the `RedBoot` partition: **FIS table missing** | [root cause](06-root-cause.md) |
| `No RedBoot partition table detected` | The kernel sees no table: same cause | [root cause](06-root-cause.md) |
| `5 RedBoot partitions found on MTD device` | **Good sign**: the table is read, 5 partitions | [rebuilding the table](08-rebuilding-the-fis-table.md) |
| `version magic '4.4.59+' should be '4.4.302+'` | Ramdisk modules and kernel of different versions (consequence of an incomplete installation) | [reinstalling DSM](09-reinstalling-dsm.md) |
| `Exit on error [3] init not health` | The installation failed | [reinstalling DSM](09-reinstalling-dsm.md) |
| `Linux version ...` | Version of the kernel actually started | [reinstalling DSM](09-reinstalling-dsm.md) |
| `login:` | The boot went all the way | |

### Helper script

The `scripts/analyze_log.py` script (English version in `en/scripts/`) looks for these signatures in a log and suggests the chapter to read:

```sh
python en/scripts/analyze_log.py my_log.log
```

It changes nothing and does not print the login line (which contains the server name). **Never publish the logs themselves**: they contain the server name, sometimes the IP address, the serial number or the MAC address.
