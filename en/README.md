# Repairing a Synology DS218 stuck in "junior mode" (blank FIS table)

🇫🇷 [Version française](../README.md)

A complete guide, based on a real repair: a **Synology DS218** that stayed on **"Migratable"** and on which every DSM installation failed. This repository explains everything, from connecting the serial console to the **DSM setup page**, together with the scripts that were used.

> **Warning.** This guide describes what worked on **one** NAS. Writing to a device's flash can make it unusable. Read the [warnings](docs/00-warnings.md) before anything else. This project is neither affiliated with nor endorsed by Synology.

## Summary

| Item | Detail |
|---|---|
| Device | Synology DS218, Realtek RTD1296 SoC, 2 GiB of DDR4 |
| Starting problem | NAS impossible to set up after removing the disks and formatting them with a USB enclosure under Windows 11, then trying to reinstall DSM |
| Main symptom | "Migratable" status in a loop. Every installation ends with `Exit on error [3] init not health` |
| Root cause | The **"FIS directory"** block of the SPI flash (4 KB at offset `0x7ff000`) was **entirely blank (0xFF)**. The `updater` tool could not find the `RedBoot` partition |
| Fix | Rebuild the 4 KB block describing the 5 partitions and write it from the junior-mode shell |
| Result | 5 partitions detected, DSM 6.2.4 installed, then updated to DSM 7.4.1. Original serial number and MAC visible again |
| Other problem | Hardware instability of the RAM, handled **separately** (it was not the cause of the installation blockage) |

## Where to start?

```text
Does your NAS boot stably all the way to "login:"?
├─ No   → docs/02 (serial console) then docs/04 (hardware) then docs/11 (stability)
└─ Yes  → Does the installation fail with "find mtd partition [RedBoot] by name fail"?
          ├─ Yes → docs/06 (cause) → docs/07 (map) → docs/08 (rebuild)
          │        → docs/09 (reinstall) → docs/10 (after the installation)
          └─ No  → docs/14 (troubleshooting / FAQ)
```

A boot log helps you answer: `python scripts/analyze_log.py <log>`.

## Chapters

| Chapter | Content |
|---|---|
| [00 Warnings](docs/00-warnings.md) | Risks, what this guide does not guarantee |
| [01 Hardware and tools](docs/01-hardware-and-tools.md) | What you need |
| [02 Serial console and junior mode](docs/02-serial-console-and-junior-mode.md) | Watching the boot, entering U-Boot, junior shell |
| [03 Symptoms](docs/03-symptoms.md) | What was observed: LEDs, logs |
| [04 Hardware intervention](docs/04-hardware-intervention.md) | Opening, RAM chip reflow, cooling, RAM tests |
| [05 Timeline and diagnosis](docs/05-timeline-and-diagnosis.md) | Sequence of events, log signatures |
| [06 Root cause](docs/06-root-cause.md) | Why the installation fails |
| [07 Flash map](docs/07-flash-map.md) | Offsets and sizes of the areas |
| [08 Rebuilding the FIS table](docs/08-rebuilding-the-fis-table.md) | **The step-by-step procedure** |
| [09 Reinstalling DSM](docs/09-reinstalling-dsm.md) | Up to the installation page |
| [10 After the installation](docs/10-after-installation.md) | Network, time, flash backup, updates |
| [11 Stability tests](docs/11-stability-tests.md) | Validating the hardware |
| [12 Open questions](docs/12-open-questions.md) | What is not proven |
| [13 Pitfalls and lessons](docs/13-pitfalls-and-lessons.md) | Mistakes to avoid |
| [14 Troubleshooting / FAQ](docs/14-troubleshooting-faq.md) | Symptom → cause → action |
| [15 References](docs/15-references.md) | Sources |
| [Appendices](docs/appendices.md) | FIS entry structure, boot stages, checklist |
| [Privacy](docs/PRIVACY.md) | What must never be published |

## Scripts

Python 3, no dependencies. The English versions are in `en/scripts/` (same logic as `scripts/`, English messages).

| Script | Purpose |
|---|---|
| `scripts/build_fis.py` | Builds the 4 096-byte FIS block (`--out`), generates the commands for the BusyBox shell (`--busybox`), compares a block with the reference (`--verify`) |
| `scripts/check_flash_dump.py` | Checks a flash dump (size, areas, FIS table state) before any write |
| `scripts/analyze_log.py` | Looks for error signatures in a PuTTY log |
| `scripts/junior_build_fis.sh` | The block-building commands, ready to paste into the junior-mode shell |

```sh
python scripts/build_fis.py --out fis_new.bin
python scripts/build_fis.py --verify fis_new.bin
python scripts/check_flash_dump.py my_flash.bin
```

## Prerequisites

- A 3.3 V USB-serial adapter (FT232 type), PuTTY, a PC.
- Synology Assistant and the model's `.pat` file (downloaded from Synology).
- A **complete flash backup** before writing anything.
- A NAS that is **stable at boot**: writing to the flash on unstable hardware is a bad idea.

## Content still to fill in

The chapters contain tags the author must fill in before publishing:

- `[INSERT PHOTO: ...]`: see the list in [IMAGES.md](IMAGES.md).
- `[TO COMPLETE: ...]`: details of the hardware intervention (tool, temperature, duration, materials) in [docs/04](docs/04-hardware-intervention.md), and the name in `LICENSE`.

## What this repository deliberately does not contain

Flash dumps, raw logs, `.pat` files, serial number, MAC address, IP addresses, user names. See [privacy](docs/PRIVACY.md).

## License

MIT, see `LICENSE`. "Synology" and "DiskStation" belong to their owners.
