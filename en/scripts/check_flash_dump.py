#!/usr/bin/env python3
"""Checks a DS218 SPI flash dump (8 388 608 bytes) before any write.

Usage:  python3 check_flash_dump.py flash1.bin

The script only READS the file, never prints the content of the "vendor" partition (which
holds the MAC address and the serial number) and changes nothing.
See en/docs/08-rebuilding-the-fis-table.md.
"""
import hashlib
import struct
import sys

SIZE = 0x800000
FIS_OFFSET = 0x7FF000
ENTRY = 256


def nonblank(d: bytes, off: int, n: int = 256) -> bool:
    return any(b != 0xFF for b in d[off:off + n])


def lzma_header(d: bytes, off: int) -> bool:
    """Raw LZMA stream: properties byte 0x5D and unknown uncompressed size (8 × 0xFF)."""
    return d[off] == 0x5D and d[off + 5:off + 13] == b"\xff" * 8


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    d = open(sys.argv[1], "rb").read()
    ok = True
    print("File: %d bytes" % len(d))
    if len(d) != SIZE:
        print("  FAILED: the size must be exactly %d bytes (full flash)." % SIZE)
        print("  If this dump was taken from DSM, /dev/mtd0ro is ONLY the 1st partition: see en/docs/10-after-installation.md.")
        return 1
    print("SHA-256 : %s" % hashlib.sha256(d).hexdigest())

    print("\nExpected areas (offsets = U-Boot addresses minus 0x88100000):")
    checks = [
        ("hwsetting     0x020800", nonblank(d, 0x020800)),
        ("U-Boot        0x021440", nonblank(d, 0x021440)),
        ("FSBL          0x0840E0", nonblank(d, 0x0840E0)),
        ("U-Boot rescue 0x094C00", nonblank(d, 0x094C00)),
        ("zImage        0x100000 (LZMA header)", lzma_header(d, 0x100000)),
        ("rd.gz         0x3f0000 (LZMA header)", lzma_header(d, 0x3F0000)),
        ("vendor        0x7ef000 (not blank)", nonblank(d, 0x7EF000, 0x1000)),
    ]
    for name, good in checks:
        print("  [%s] %s" % ("OK" if good else "??", name))
        ok &= good

    print("\nFIS directory block at 0x%x:" % FIS_OFFSET)
    blk = d[FIS_OFFSET:FIS_OFFSET + 4096]
    if all(b == 0xFF for b in blk):
        print("  BLANK (4096 × 0xFF): this is the case described in this repository.")
        verdict = "blank"
    else:
        names = []
        for i in range(16):
            e = blk[i * ENTRY:(i + 1) * ENTRY]
            if e[0] == 0xFF:
                break
            nm = e[:16].split(b"\0")[0].decode("ascii", "replace")
            base, _mem, size, _ep, length = struct.unpack("<5I", e[16:36])
            names.append(nm)
            print("  %-14s base=0x%06x size=0x%06x data_length=0x%06x" % (nm, base, size, length))
        verdict = "present" if "FIS directory" in names else "other"
    print()
    if verdict == "blank" and ok:
        print("VERDICT: blank table and consistent areas. The procedure of chapter 08 applies.")
    elif verdict == "blank":
        print("VERDICT: blank table BUT some expected areas are missing or different.")
        print("          Write NOTHING: this dump does not look like the one described here. Open a discussion.")
    elif verdict == "present":
        print("VERDICT: a table already exists. DO NOT replace it with this procedure.")
    else:
        print("VERDICT: unexpected content at 0x7ff000. Write nothing.")
    return 0 if (verdict == "blank" and ok) else 1


if __name__ == "__main__":
    sys.exit(main())
