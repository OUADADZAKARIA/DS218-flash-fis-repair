# After the installation: network, time, backup, updates

Once the DSM wizard is finished, here is what remains to be done. None of it is required for the repair itself, but several surprises came up during commissioning.

## 1. Network

**The NAS must be plugged into the router.** Connected directly to the PC, it takes a fallback `169.254.x.x` address (no DHCP server answers). It is then reachable from the PC but has no gateway, no Internet and no time. Once plugged into a LAN port of the router, it gets an address and reaches the Internet.

**Fixed address (recommended):** **Control Panel > Network > Network Interface > Edit**, then manual configuration (address, mask, gateway, DNS). Pick an address **outside the DHCP range** of the router. Safer variant: reserve the address in the router (DHCP reservation) and leave the NAS on automatic.

[INSERT PHOTO: manual network configuration window (hide all addresses)]

## 2. Time and time zone

Without Internet, the NAS clock was at the year 2016 (wrong dates in logs and on the volume). With Internet:

1. **Control Panel > Regional Options > Time**.
2. Choose an NTP server (for example `time.google.com`) and enable synchronisation.
3. Choose **your region's time zone, picking the entry that handles daylight saving time**, otherwise the time is off by one hour for part of the year.

## 3. Missing home folder

As long as no volume exists, a user has no home folder. The `change directory failed` message when logging in on the console is normal; it disappears after the volume is created and the home service is enabled.

## 4. Volume

SHR + Btrfs. With a single disk, there is no protection against a failure. With two disks, SHR provides redundancy. **Creating it erases the disks**: put a test disk or empty disks in first. Before replacing disks, shut the NAS down **cleanly from DSM**.

Remember to run an S.M.A.R.T. test (**Storage Manager > HDD/SSD**): it checks the disk, not the NAS.

## 5. Shared folder and File Station (the simple way to get files)

To download a file from the NAS to the PC without a command line:

1. **Control Panel > Shared Folder > Create**: give a name (for example `backup`), keep the default options, give your user read/write access.
2. Copy the file into this folder (see the next section for the flash).
3. Open **File Station**, right-click the file > **Download**.

[INSERT PHOTO: shared folder creation wizard]
[INSERT PHOTO: File Station, Download option]

## 6. Flash backup, and a trap

Once the FIS table is rebuilt, **back up the flash**: it is the only copy of the factory identity (MAC address, serial number, in `vendor`) and of the loaders.

> **Trap: `/dev/mtd0ro` no longer contains the whole flash.** Before the repair, the flash was seen as a single 8 MiB block. Once the FIS table is present, the kernel splits it into 5 partitions. `/dev/mtd0ro` is now only the first one, `RedBoot` (**1 MiB**). A `dd` on `mtd0ro` therefore gives a file of 1 048 576 bytes, which is **incomplete**.

You must copy the five partitions and concatenate them, in order:

| Partition | Device | Size (bytes) |
|---|---|---|
| RedBoot | `/dev/mtd0ro` | 1 048 576 |
| zImage | `/dev/mtd1ro` | 3 080 192 |
| rd.gz | `/dev/mtd2ro` | 4 190 208 |
| vendor | `/dev/mtd3ro` | 65 536 |
| FIS directory | `/dev/mtd4ro` | 4 096 |
| **Total** | | **8 388 608** |

Procedure (SSH enabled in **Control Panel > Terminal & SNMP**, then PuTTY in SSH mode, or the serial console):

```sh
cd /volume1
sudo sh -c 'for i in 0 1 2 3 4; do dd if=/dev/mtd${i}ro of=flash_part${i}.bin bs=4096; done'
sudo sh -c 'cat flash_part0.bin flash_part1.bin flash_part2.bin flash_part3.bin flash_part4.bin > flash_full.bin'
ls -l flash_full.bin        # must show 8388608
```

Then put `flash_full.bin` in the shared folder, download it with File Station, and check it on the PC:

```sh
python en/scripts/check_flash_dump.py flash_full.bin
```

The script checks the size, prints the SHA-256 and says whether the FIS table is present. A table present after the repair is the expected result.

**Stop:** if `ls -l` does not show `8388608`, do not keep this file as a backup.

**Never publish this file**: it contains the original MAC address and serial number.

## 7. DSM updates

- Before Internet access, DSM wrongly displayed "Your DSM version is up to date". Once online, it offers updates of the same branch (6.2.4, a newer "Update") as well as DSM 7.
- On this NAS, I ended up on **DSM 7.4.1-90080 Update 1** (kernel `4.4.302+`). This kernel is the one that was already in the flash before the repair: the NAS had therefore run this DSM before.
- These updates rewrite `zImage` and `rd.gz`, which changes the FIS table (the declared size of `zImage` changes). This is normal.
- Do them **after** the stability tests and with a flash backup taken **beforehand**.
- I did not formally verify which DSM 7 versions are officially supported for this model: I only observe that 7.4.1 works here. Check Synology's model page.
- DSM 6.2 is no longer maintained by Synology.

## 8. Temperature and enclosure

The NAS ran open during the repair. When reassembling: refit the fan, check the airflow, then monitor the disk and system temperature in **Resource Monitor**. Do a few cold boots again once the enclosure is closed: an intermittent RAM fault can come back with heat ([stability tests](11-stability-tests.md)).
