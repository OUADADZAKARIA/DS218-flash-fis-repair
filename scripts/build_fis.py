#!/usr/bin/env python3
"""Génère le bloc « FIS directory » (4096 octets) d'un Synology DS218.

Ce bloc est la table de partitions RedBoot que le noyau Linux cherche à
l'offset 0x7ff000 de la flash SPI de 8 Mo. Voir docs/08-procedure-reconstruction-fis.md.

Utilisation :
    python3 build_fis.py --out fis_new.bin          # écrit le bloc de 4096 octets
    python3 build_fis.py --busybox                  # affiche les commandes à coller dans le shell BusyBox
    python3 build_fis.py --verify fis_recupere.bin  # compare un fichier au bloc attendu

Aucune écriture dans la flash n'est faite par ce script : il ne produit que des fichiers
ou du texte.
"""
import argparse
import struct
import sys

# (nom, flash_base, taille). mem_base et entry_point valent 0, data_length = taille.
ENTRIES = [
    ("RedBoot",       0x000000, 0x100000),
    ("zImage",        0x100000, 0x2F0000),
    ("rd.gz",         0x3F0000, 0x3FF000),
    ("vendor",        0x7EF000, 0x010000),
    ("FIS directory", 0x7FF000, 0x001000),
]
BLOCK_SIZE = 4096   # un secteur d'effacement de la MX25L6445E
ENTRY_SIZE = 256    # taille d'une structure fis_image_desc
FLASH_OFFSET = 0x7FF000


def entry(name: str, base: int, size: int) -> bytes:
    """Une entrée de 256 octets : nom[16], 5 mots de 32 bits (petit-boutiste),
    212 octets à 0xFF, puis 8 octets à zéro (sommes de contrôle ignorées par le noyau)."""
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
    """Commandes sans outil externe (printf intégré + dd), pour le shell du mode junior."""
    lines = [
        "# Construit /tmp/fis_new.bin (4096 octets) dans la RAM du NAS. N'écrit rien dans la flash.",
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
    lines.append("ls -l /tmp/fis_new.bin   # doit afficher exactement 4096")
    return "\n".join(lines) + "\n"


def describe(blk: bytes) -> None:
    for i in range(BLOCK_SIZE // ENTRY_SIZE):
        e = blk[i * ENTRY_SIZE:(i + 1) * ENTRY_SIZE]
        if e[0] == 0xFF:
            break
        name = e[:16].split(b"\0")[0].decode("ascii", "replace")
        base, mem, size, entry_pt, length = struct.unpack("<5I", e[16:36])
        print("  %-14s base=0x%06x taille=0x%06x data_length=0x%06x" % (name, base, size, length))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--out", metavar="FICHIER", help="écrit le bloc de 4096 octets")
    g.add_argument("--busybox", action="store_true", help="affiche les commandes pour le shell BusyBox")
    g.add_argument("--verify", metavar="FICHIER", help="compare un fichier de 4096 octets au bloc attendu")
    a = ap.parse_args()

    blk = build()
    if a.out:
        with open(a.out, "wb") as f:
            f.write(blk)
        print("%s écrit (%d octets). Contenu :" % (a.out, len(blk)))
        describe(blk)
        return 0
    if a.busybox:
        sys.stdout.write(busybox_script())
        return 0
    data = open(a.verify, "rb").read()
    print("taille : %d octets (attendu %d)" % (len(data), BLOCK_SIZE))
    if len(data) != BLOCK_SIZE:
        print("ÉCHEC : taille incorrecte. N'écris rien dans la flash.")
        return 1
    if data == blk:
        print("OK : identique au bloc attendu.")
        return 0
    diff = [i for i in range(BLOCK_SIZE) if data[i] != blk[i]]
    print("DIFFÉRENT : %d octet(s) diffèrent (premier : 0x%x)." % (len(diff), diff[0]))
    print("Contenu du fichier :")
    describe(data)
    print("Si c'est un bloc relu APRÈS une mise à jour de DSM, une différence sur data_length "
          "de zImage est normale (l'installateur met cette valeur à jour).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
