# Procedure: rebuilding the partition table (FIS directory)

> **Read the [warnings](00-warnings.md) before touching the flash.**

## Prerequisites

- Serial console access to the NAS in junior mode (`root` login with Synology's default junior-mode password, to be checked in Synology's documentation).
- A PC on the same network as the NAS, to fetch the files through BusyBox's small web server.
- A **stable** NAS (no crashes for several minutes).
- The `.pat` file of the **version shown by Synology Assistant** for your model (see [reinstalling DSM](09-reinstalling-dsm.md)).

## Step 1: Back up the flash (essential)

In the NAS shell (BusyBox):

```sh
dd if=/dev/mtd0ro of=/tmp/flash1.bin bs=4096
dd if=/dev/mtd0ro of=/tmp/flash2.bin bs=4096
httpd -p 8081 -h /tmp
```

Then on the PC, download `http://<NAS_IP>:8081/flash1.bin` and `http://<NAS_IP>:8081/flash2.bin`.

**Check:** each file must be **8 388 608 bytes** and both must have the **same SHA-256** (on Windows: `certutil -hashfile flash1.bin SHA256`). Without identical copies, do not continue.

[INSERT PHOTO: PuTTY terminal with the two `dd` commands (hide the IP address)]

> Junior mode has no `od`, no `hexdump`, no `md5sum`, no `sed`, no `awk`. The analysis is therefore done on the PC.

## Step 2: Check that the table is really blank

On the PC (Python), check that the 4096 bytes at offset `0x7ff000` are all `0xFF`:

```python
d = open("flash1.bin", "rb").read()
blk = d[0x7ff000:0x800000]
print(len(blk), all(b == 0xFF for b in blk))   # expected: 4096 True
```

The `scripts/check_flash_dump.py` script does this check and several others (size, SHA-256, loaders and kernel areas present).

## Step 3: Confirm the expected partition names

In the NAS shell, mount the temporary system partition and look for the names in the `updater` tool:

```sh
mkdir -p /mnt/d
mount /dev/md0 /mnt/d
grep -a -o -E "RedBoot|zImage|rd\.gz|vendor|FIS directory" /mnt/d/.updater
umount /mnt/d
```

Observed result: `RedBoot`, `vendor`, `FIS directory`, `zImage`, `rd.gz`.

## Step 4: Build the 4 KB block in the NAS RAM

Entry format (256 bytes, 32-bit little-endian values):

| Bytes | Field |
|---|---|
| 0–15 | `name` (text, padded with zeros) |
| 16–19 | `flash_base` |
| 20–23 | `mem_base` (0) |
| 24–27 | `size` |
| 28–31 | `entry_point` (0) |
| 32–35 | `data_length` (= `size`) |
| 36–247 | `0xFF` padding (212 bytes) |
| 248–255 | `desc_cksum` and `file_cksum` (zeros) |

The 5 entries take the first 1280 bytes. The rest of the block is filled with `0xFF`.

The following lines can be pasted as is into the NAS shell. They only use `printf` (built into BusyBox) and `dd`:

```sh
i=0; while [ $i -lt 4096 ]; do printf '\377'; i=$((i+1)); done > /tmp/ff4k
rm -f /tmp/fis_new.bin
{ printf '\122\145\144\102\157\157\164\000\000\000\000\000\000\000\000\000'; printf '\000\000\000\000\000\000\000\000\000\000\020\000\000\000\000\000\000\000\020\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
{ printf '\172\111\155\141\147\145\000\000\000\000\000\000\000\000\000\000'; printf '\000\000\020\000\000\000\000\000\000\000\057\000\000\000\000\000\000\000\057\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
{ printf '\162\144\056\147\172\000\000\000\000\000\000\000\000\000\000\000'; printf '\000\000\077\000\000\000\000\000\000\360\077\000\000\000\000\000\000\360\077\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
{ printf '\166\145\156\144\157\162\000\000\000\000\000\000\000\000\000\000'; printf '\000\360\176\000\000\000\000\000\000\000\001\000\000\000\000\000\000\000\001\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
{ printf '\106\111\123\040\144\151\162\145\143\164\157\162\171\000\000\000'; printf '\000\360\177\000\000\000\000\000\000\020\000\000\000\000\000\000\000\020\000\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
dd if=/tmp/ff4k bs=1 count=2816 2>/dev/null >> /tmp/fis_new.bin
ls -l /tmp/fis_new.bin
```

**Check:** `ls -l` must show exactly **4096** bytes. Otherwise, stop.

[INSERT PHOTO: output of `ls -l /tmp/fis_new.bin` in PuTTY]

## Step 5: Verify the block before writing it

Fetch `fis_new.bin` onto the PC with `httpd` (see step 1) and compare it with the expected block. Equivalent Python generator:

```python
import struct
ents = [("RedBoot", 0x0, 0x100000), ("zImage", 0x100000, 0x2f0000),
        ("rd.gz", 0x3f0000, 0x3ff000), ("vendor", 0x7ef000, 0x10000),
        ("FIS directory", 0x7ff000, 0x1000)]

def entry(name, base, size):
    nm = name.encode().ljust(16, b"\0")
    return nm + struct.pack("<5I", base, 0, size, 0, size) + b"\xff" * 212 + b"\0" * 8

blk = b"".join(entry(*e) for e in ents).ljust(4096, b"\xff")
open("fis_expected.bin", "wb").write(blk)
```

Compare with `cmp fis_new.bin fis_expected.bin` (or with the SHA-256 sums); the `scripts/build_fis.py --verify fis_new.bin` option does the same. **Write nothing until they are identical.**

## Step 6: Write the sector to the flash

```sh
dd if=/tmp/fis_new.bin of=/dev/mtdblock0 bs=4096 seek=2047 count=1
sync
```

Expected: `1+0 records in` and `1+0 records out`.

Technical notes:
- `seek=2047` corresponds to offset `2047 × 4096 = 0x7ff000`.
- We write through `/dev/mtdblock0` because the block layer handles erasing the sector before writing. The character device `/dev/mtd0` does not erase.

## Step 7: Read back and compare

```sh
dd if=/dev/mtd0ro of=/tmp/fis_back.bin bs=4096 skip=2047 count=1
ls -l /tmp/fis_back.bin
```

Fetch `fis_back.bin` with `httpd` and compare it with the block you wrote: it must be **identical**. **Do not reboot before confirming this.**

## Step 8: Reboot and check the partitions

After `reboot` and reconnecting in junior mode:

```sh
cat /proc/mtd
dmesg | grep -i -E "redboot|partition|mtd"
```

Result obtained:

```text
dev:    size   erasesize  name
mtd0: 00100000 00001000 "RedBoot"
mtd1: 002f0000 00001000 "zImage"
mtd2: 003ff000 00001000 "rd.gz"
mtd3: 00010000 00001000 "vendor"
mtd4: 00001000 00001000 "FIS directory"

Searching for RedBoot partition table in RtkSFC at offset 0x7ff000
5 RedBoot partitions found on MTD device RtkSFC
Creating 5 MTD partitions on "RtkSFC":
```

**Stop here** if `/proc/mtd` does not list the 5 partitions. Do not start the reinstallation in that case.

[INSERT PHOTO: `cat /proc/mtd` before the fix (a single partition)]
[INSERT PHOTO: `cat /proc/mtd` after the fix (5 partitions)]

## Step 9: Possible rollback

The original state was a sector entirely at `0xFF`. If something goes wrong, you can put it back in that state with the `/tmp/ff4k` file (4096 bytes of `0xFF`):

```sh
dd if=/tmp/ff4k of=/dev/mtdblock0 bs=4096 seek=2047 count=1
sync
```

The two full flash dumps remain the reference backup. Keep them somewhere safe.
