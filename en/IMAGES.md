# Images to provide

The repository `images/` folder is intentionally empty: photos and screenshots contain personal data. Each `[INSERT PHOTO: ...]` tag in the chapters says what to add.

Rules: see [privacy](docs/PRIVACY.md). Blur (then export as a flattened image): serial number, MAC address, IP addresses, server name, user, NAS label. Name the files `chapter-NN-description.png`.

## Photo list by chapter

### 01-hardware-and-tools.md

- [ ] DS218 board, overview with the UART connector J2 marked
- [ ] USB-serial adapter connected to J2 (hide any personal information that is visible)
- [ ] the 4 RAM chips area, with U3 marked

### 02-serial-console-and-junior-mode.md

- [ ] the USB-serial adapter with the voltage selector on 3.3 V
- [ ] the J2 connector located on the board
- [ ] GND, TX and RX wires connected to J2 (hide any personal information that is visible)
- [ ] PuTTY configuration window in Serial mode (115200, 8N1, no flow control)
- [ ] "All session output" ticked in Session > Logging
- [ ] `DiskStation login:` prompt then BusyBox shell in PuTTY (hide the server name)
- [ ] output of `cat /proc/mtd` in junior mode (a single `RtkSFC` partition)

### 03-symptoms.md

- [ ] log excerpt with `skb_over_panic` (hide any personal data)
- [ ] log excerpt with a hang while reading the kernel (offset `0x002f0000`)
- [ ] state of the NAS LEDs during a failed boot (blinking power button, other LEDs off)

### 04-hardware-intervention.md

- [ ] open enclosure, overview
- [ ] board removed, front side (RAM chips)
- [ ] board removed, back side (RAM chips)
- [ ] heated area with the neighbouring components protected
- [ ] plate used during the operation
- [ ] metal cooling element in place, pressing on U3
- [ ] final position of the fan
- [ ] U-Boot terminal screenshot with `bdinfo` (hide default IP and MAC addresses if they appear)
- [ ] U-Boot terminal screenshot with `mtest` results, low and high zones
- [ ] U-Boot terminal screenshot with `mtest2 ... 0 errors`

### 05-timeline-and-diagnosis.md

- [ ] Synology Assistant screenshot with the status "Migratable" (hide the IP address, MAC address and serial number)
- [ ] web wizard with the "Migration" / "Reinstall" choices

### 08-rebuilding-the-fis-table.md

- [ ] PuTTY terminal with the two `dd` commands (hide the IP address)
- [ ] output of `ls -l /tmp/fis_new.bin` in PuTTY
- [ ] `cat /proc/mtd` before the fix (a single partition)
- [ ] `cat /proc/mtd` after the fix (5 partitions)

### 09-reinstalling-dsm.md

- [ ] Synology Assistant after the repair, with the serial number and MAC displayed (to be hidden before publishing)
- [ ] NAS label (to be fully hidden before publishing)
- [ ] DSM setup page, first screen
- [ ] Synology Assistant, NAS "Migratable" (hide IP, MAC, serial number)
- [ ] "Reinstall" choice in the web wizard
- [ ] installation progress bar
- [ ] "Welcome" screen of the DSM setup wizard
- [ ] DSM desktop (hide the server name and the address)

### 10-after-installation.md

- [ ] manual network configuration window (hide all addresses)
- [ ] shared folder creation wizard
- [ ] File Station, Download option

### 11-stability-tests.md

- [ ] cold-boot log with the login prompt (hide the server name)
- [ ] Storage Manager with the created volume and the check running
- [ ] disk health information (hide the disk serial number)

Total: 43 images.
