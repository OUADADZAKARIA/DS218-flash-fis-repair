# Pitfalls encountered and lessons learned

## Junior-mode shell (BusyBox v1.16.1)

- **Present** (observed): `cat`, `dd`, `printf` (built in), `ls`, `tail`, `grep`, `ifconfig`, `httpd`, `vi`, `mount`.
- **Missing** (observed): `od`, `hexdump`, `md5sum`, `tr`, `cmp`, `sed`, `awk`, `strings`. Test a tool (`which`) before relying on it.
- Solution: save to `/tmp` (in RAM) and fetch it with `httpd -p 8081 -h /tmp`, then analyse on the PC.
- `/tmp` is in RAM: everything is lost at reboot. Dumps must be retrieved beforehand.

## Flash

- Reading: `/dev/mtd0ro`. Writing with automatic erase: `/dev/mtdblock0`. The character device `/dev/mtd0` does not erase.
- Offset `0x7ff000` corresponds to `seek=2047` with 4096-byte blocks.

## Lessons

1. **Always read the installer log** (`/var/log/messages`), not just the web interface: the real error is there (`find mtd partition [RedBoot] by name fail`).
2. **"Migratable" does not always mean a disk problem.** Here, the cause was in the flash.
3. **Back up the flash before any write**, with two copies and a checksum verification.
4. **Verify each step before writing**: block built, compared, written, read back, compared.
5. **Separate the problems**: hardware instability and the blank partition table were two independent causes that masked each other.
6. Do not confuse "Restart" from DSM (RAM stays powered) with a real **cold boot** (power cut for about 10 s) when testing stability.
7. A serial adapter set to **3.3 V** is mandatory for the UART console.
8. **First installation: use the version Synology Assistant shows for the NAS** (here 6.2.4-25556), with the right model. This is an observed practice, not a rule tested against other versions ([reinstalling DSM](09-reinstalling-dsm.md)).
9. **Plug the NAS into the router** (not directly into the PC) so that it gets an address, Internet and the time. Without that, DSM does not detect its updates.
