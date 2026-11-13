#!/usr/bin/env python3
"""Finds, in a serial console (PuTTY) log, the signatures described in this repository.

Usage:  python3 analyze_log.py my_log.log

Prints only the first line of each signature (the text of the login prompt line is
masked, because it contains the server name), then a count per category.
Still re-read the output before pasting it into a public message. See en/docs/05-timeline-and-diagnosis.md.
"""
import re
import sys

SIGNATURES = [
    ("Boot loop (FSBL verification)", r"verify fsbl fail"),
    ("Kernel crash: Oops / BUG", r"Internal error: Oops|kernel BUG at"),
    ("Network buffer corruption (skb_over_panic)", r"skb_over_panic"),
    ("Kernel panic", r"Kernel panic - not syncing"),
    ("Audio coprocessor: fatal error", r"FATAL: Audio ROS"),
    ("Installer: RedBoot partition not found", r"find mtd partition \[RedBoot\] by name fail"),
    ("Kernel: no RedBoot table", r"No RedBoot partition table detected"),
    ("Kernel: RedBoot table found", r"\d+ RedBoot partitions found"),
    ("Modules: inconsistent version magic", r"version magic .* should be"),
    ("Junior mode: init not health", r"init not health"),
    ("Kernel version", r"Linux version \S+"),
    ("DSM login prompt reached", r"login:"),
]


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    counts = {name: 0 for name, _ in SIGNATURES}
    first = {}
    with open(sys.argv[1], "rb") as f:
        for n, raw in enumerate(f, 1):
            line = raw.replace(b"\0", b"").decode("utf-8", "replace").rstrip()
            for name, pat in SIGNATURES:
                if re.search(pat, line):
                    counts[name] += 1
                    first.setdefault(name, (n, line.strip()[:160]))
    for name, _ in SIGNATURES:
        if counts[name]:
            n, line = first[name]
            if name == "DSM login prompt reached":
                line = "(text hidden: the line contains the server name)"
            print("%-48s x%-4d (line %d) %s" % (name, counts[name], n, line))
    print()
    if counts["Installer: RedBoot partition not found"] or counts["Kernel: no RedBoot table"]:
        print("=> Partition table missing: see en/docs/06-root-cause.md and en/docs/08-rebuilding-the-fis-table.md")
    if counts["Boot loop (FSBL verification)"] or counts["Kernel crash: Oops / BUG"] \
            or counts["Network buffer corruption (skb_over_panic)"]:
        print("=> Signs of hardware (RAM) instability: see en/docs/04-hardware-intervention.md")
    if counts["Modules: inconsistent version magic"]:
        print("=> Kernel and initial filesystem of different versions: consequence of an installation that never completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
