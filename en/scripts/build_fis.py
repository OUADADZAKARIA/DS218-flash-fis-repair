#!/usr/bin/env python3
"""Builds the "FIS directory" block (4096 bytes) of a Synology DS218.

This block is the RedBoot partition table that the Linux kernel looks for at
offset 0x7ff000 of the 8 MB SPI flash. See en/docs/08-rebuilding-the-fis-table.md.

Usage:
    python3 build_fis.py --out fis_new.bin          # writes the 4096-byte block
    python3 build_fis.py --busybox                  # prints the commands to paste into the BusyBox shell
    python3 build_fis.py --verify fis_read_back.bin # compares a file with the expected block

This script never writes to the flash: it only produces files or text.
"""
import argparse
import struct
import sys

# (name, flash_base, size). mem_base and entry_point are 0, data_length = size.
ENTRIES = [
    ("RedBoot",       0x000000, 0x100000),
    ("zImage",        0x100000, 0x2F0000),
    ("rd.gz",         0x3F0000, 0x3FF000),
    ("vendor",        0x7EF000, 0x010000),
    ("FIS directory", 0x7FF000, 0x001000),
]
BLOCK_SIZE = 4096   # one erase sector of the MX25L6445E
ENTRY_SIZE = 256    # size of a fis_image_desc structure
FLASH_OFFSET = 0x7FF000


def entry(name: str, base: int, size: int) -> bytes:
    """One 256-byte entry: name[16], 5 little-endian 32-bit words,
    212 bytes of 0xFF, then 8 zero bytes (checksums, ignored by the kernel)."""
    nm = name.encode("ascii").ljust(16, b"\0")
    fields = struct.pack("<5I", base, 0, size, 0, size)
    out = nm + fields + b"\xff" * 212 + b"\0" * 8
    assert len(out) == ENTRY_SIZE
    return out


def build() -> bytes:
    blk = b"".join(entry(*e) for e in ENTRIES).ljust(BLOCK_SIZE, b"\xff")
    assert len(blk) == BLOCK_SIZE
    return blk


def octal(data: bytes) -> str:
    return "".join("\\%03o" % b for b in data)


def busybox_script() -> str:
    """Commands needing no external tool (built-in printf + dd), for the junior-mode shell."""
    lines = [
        "# Builds /tmp/fis_new.bin (4096 bytes) in the NAS RAM. Writes nothing to the flash.",
        "i=0; while [ $i -lt 4096 ]; do printf '\\377'; i=$((i+1)); done > /tmp/ff4k",
        "rm -f /tmp/fis_new.bin",
    ]
    for name, base, size in ENTRIES:
        nm = name.encode("ascii").ljust(16, b"\0")
        fields = struct.pack("<5I", base, 0, size, 0, size)
        lines.append(
            "{ printf '%s'; printf '%s'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; "
            "printf '%s'; } >> /tmp/fis_new.bin" % (octal(nm), octal(fields), octal(b"\0" * 8))
        )
    rest = BLOCK_SIZE - len(ENTRIES) * ENTRY_SIZE
    lines.append("dd if=/tmp/ff4k bs=1 count=%d 2>/dev/null >> /tmp/fis_new.bin" % rest)
    lines.append("ls -l /tmp/fis_new.bin   # must show exactly 4096")
    return "\n".join(lines) + "\n"


def describe(blk: bytes) -> None:
    for i in range(BLOCK_SIZE // ENTRY_SIZE):
        e = blk[i * ENTRY_SIZE:(i + 1) * ENTRY_SIZE]
        if e[0] == 0xFF:
            break
        name = e[:16].split(b"\0")[0].decode("ascii", "replace")
        base, mem, size, entry_pt, length = struct.unpack("<5I", e[16:36])
        print("  %-14s base=0x%06x size=0x%06x data_length=0x%06x" % (name, base, size, length))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--out", metavar="FILE", help="writes the 4096-byte block")
    g.add_argument("--busybox", action="store_true", help="prints the commands for the BusyBox shell")
    g.add_argument("--verify", metavar="FILE", help="compares a 4096-byte file with the expected block")
    a = ap.parse_args()

    blk = build()
    if a.out:
        with open(a.out, "wb") as f:
            f.write(blk)
        print("%s written (%d bytes). Content:" % (a.out, len(blk)))
        describe(blk)
        return 0
    if a.busybox:
        sys.stdout.write(busybox_script())
        return 0
    data = open(a.verify, "rb").read()
    print("size: %d bytes (expected %d)" % (len(data), BLOCK_SIZE))
    if len(data) != BLOCK_SIZE:
        print("FAILED: wrong size. Write nothing to the flash.")
        return 1
    if data == blk:
        print("OK: identical to the expected block.")
        return 0
    diff = [i for i in range(BLOCK_SIZE) if data[i] != blk[i]]
    print("DIFFERENT: %d byte(s) differ (first: 0x%x)." % (len(diff), diff[0]))
    print("File content:")
    describe(data)
    print("If this is a block read back AFTER a DSM update, a difference on zImage's "
          "data_length is normal (the installer updates that value).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
