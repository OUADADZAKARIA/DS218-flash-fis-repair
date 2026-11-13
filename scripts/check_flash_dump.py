#!/usr/bin/env python3
"""Contrôle un dump de la flash SPI d'un DS218 (8 388 608 octets) avant toute écriture.

Utilisation :  python3 check_flash_dump.py flash1.bin

Le script LIT le fichier, n'affiche jamais le contenu de la partition « vendor » (qui
contient l'adresse MAC et le numéro de série) et ne modifie rien.
Voir docs/08-procedure-reconstruction-fis.md.
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
    """Flux LZMA « brut » : propriétés 0x5D et taille décompressée inconnue (8 × 0xFF)."""
    return d[off] == 0x5D and d[off + 5:off + 13] == b"\xff" * 8


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    d = open(sys.argv[1], "rb").read()
    ok = True
    print("Fichier : %d octets" % len(d))
    if len(d) != SIZE:
        print("  ÉCHEC : la taille doit être exactement %d octets (flash complète)." % SIZE)
        print("  Si c'est un dump pris depuis DSM, /dev/mtd0ro n'est QUE la 1re partition : voir docs/10-apres-installation.md.")
        return 1
    print("SHA-256 : %s" % hashlib.sha256(d).hexdigest())

    print("\nZones attendues (offsets déduits des adresses U-Boot moins 0x88100000) :")
    checks = [
        ("hwsetting     0x020800", nonblank(d, 0x020800)),
        ("U-Boot        0x021440", nonblank(d, 0x021440)),
        ("FSBL          0x0840E0", nonblank(d, 0x0840E0)),
        ("U-Boot rescue 0x094C00", nonblank(d, 0x094C00)),
        ("zImage        0x100000 (en-tête LZMA)", lzma_header(d, 0x100000)),
        ("rd.gz         0x3f0000 (en-tête LZMA)", lzma_header(d, 0x3F0000)),
        ("vendor        0x7ef000 (non vide)", nonblank(d, 0x7EF000, 0x1000)),
    ]
    for name, good in checks:
        print("  [%s] %s" % ("OK" if good else "??", name))
        ok &= good

    print("\nBloc FIS directory à 0x%x :" % FIS_OFFSET)
    blk = d[FIS_OFFSET:FIS_OFFSET + 4096]
    if all(b == 0xFF for b in blk):
        print("  VIDE (4096 × 0xFF) : c'est le cas décrit dans ce dépôt.")
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
            print("  %-14s base=0x%06x taille=0x%06x data_length=0x%06x" % (nm, base, size, length))
        verdict = "present" if "FIS directory" in names else "other"
    print()
    if verdict == "blank" and ok:
        print("VERDICT : table vide et zones cohérentes. La procédure du chapitre 08 s'applique.")
    elif verdict == "blank":
        print("VERDICT : table vide MAIS des zones attendues sont absentes ou différentes.")
        print("          N'écris RIEN : ce dump ne ressemble pas à celui décrit ici. Ouvre une discussion.")
    elif verdict == "present":
        print("VERDICT : une table existe déjà. NE PAS la remplacer avec cette procédure.")
    else:
        print("VERDICT : contenu inattendu à 0x7ff000. N'écris rien.")
    return 0 if (verdict == "blank" and ok) else 1


if __name__ == "__main__":
    sys.exit(main())
