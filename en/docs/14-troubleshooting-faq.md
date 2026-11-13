# Troubleshooting and FAQ

Quick table: **symptom → likely cause → action**. The causes are those observed on this DS218; on another case they remain hypotheses.

## Installation and junior mode

| Symptom | Likely cause | Action |
|---|---|---|
| NAS "Migratable" in a loop, installation fails | Blank FIS table, or unsuitable `.pat` version | Read the log (`tail -f /var/log/messages`). If `find mtd partition [RedBoot] by name fail` → [rebuilding the table](08-rebuilding-the-fis-table.md) |
| `version magic '4.4.59+' should be '4.4.302+'` | Kernel and modules of different versions (incomplete installation) | Redo a **Reinstall** with the `.pat` of the version shown by Synology Assistant ([reinstalling DSM](09-reinstalling-dsm.md)) |
| `init not health` | The installation stopped on an error | Look for the real error a few lines higher in the log |
| Which `.pat` version should I take? | | The one Synology Assistant displays for the NAS, for the **exact model**. Observed practice, not proven as a rule |
| A model other than the DS218? | | Not tested. The offsets and sizes are specific to this model: do not reuse them without reading your own values ([flash map](07-flash-map.md)) |

## Network and time

| Symptom | Likely cause | Action |
|---|---|---|
| `169.254.x.x` address | No DHCP server (NAS connected directly to the PC) | Plug the NAS into the router |
| No Internet, no updates | No gateway (same cause) | Same |
| Clock in 2016 | No NTP | Network, then NTP synchronisation ([after the installation](10-after-installation.md)) |
| Time off by one hour in some months | Time zone without daylight saving time | Pick the region's time zone that handles it |
| `change directory failed` on the console | No volume, so no home folder | Normal, create the volume |

## Flash and backup

| Symptom | Likely cause | Action |
|---|---|---|
| `dd` of `/dev/mtd0ro` gives 1 048 576 bytes | After the repair, `mtd0ro` is only the `RedBoot` partition | Copy `mtd0` to `mtd4` and concatenate them ([after the installation](10-after-installation.md)) |
| The FIS block read back differs from the one written | Write not completed | Redo `sync`, read back, compare with `build_fis.py --verify` |
| `check_flash_dump.py` says "a table already exists" | The NAS already has a table (e.g. after the repair) | The rebuilding procedure no longer applies |

## Boot and hardware

| Symptom | Likely cause | Action |
|---|---|---|
| `verify fsbl fail` loop | Unstable boot. Observed with faulty RAM | [hardware intervention](04-hardware-intervention.md) |
| Different crashes at each boot (`Oops`, `kernel BUG`, `skb_over_panic`) | Unstable memory | Same, then [stability tests](11-stability-tests.md) |
| Boots correctly only when pressing on chip U3 | Defective contact (solder or cooling) | Same |
| Blinking power LED, other LEDs off | The boot does not go all the way | Connect the serial console and read the log ([serial console](02-serial-console-and-junior-mode.md)) |
| U-Boot RAM tests without errors but instability | Intermittent fault: a test with no errors does not prove stability | Multiply the cold boots |

## Frequently asked questions

**Is the grey metal plate mandatory?** I have no proof that it is. In my case it plays a heat-dissipation role and presses on chip U3, but I do not know whether it is original or added. On this point, see [open questions](12-open-questions.md). A plate touching a component without insulation can however create a short circuit: check what it touches.

**Do I also need a serial console to repair?** To read the logs and reach the junior-mode shell, yes: that is what lets you write to the flash.

**Is my data at risk?** This procedure only writes to the flash (4 KB). It does not touch the disks. That said, DSM installations can format the disks: **back up first**.

**Can I publish my logs to ask for help?** No, not as they are: see [privacy](PRIVACY.md).
