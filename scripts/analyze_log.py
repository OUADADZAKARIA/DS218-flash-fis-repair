#!/usr/bin/env python3
"""Repère dans un journal de console série (PuTTY) les signatures décrites dans ce dépôt.

Utilisation :  python3 analyze_log.py mon_journal.log

N'affiche que la première ligne de chaque signature (le texte de la ligne d'invite de
connexion est masqué, car il contient le nom du serveur), puis un compte par catégorie.
Relis quand même la sortie avant de la copier dans un message public. Voir docs/05-chronologie-et-diagnostic.md.
"""
import re
import sys

SIGNATURES = [
    ("Boucle de démarrage (vérification du FSBL)", r"verify fsbl fail"),
    ("Plantage noyau : Oops / BUG", r"Internal error: Oops|kernel BUG at"),
    ("Corruption réseau (skb_over_panic)", r"skb_over_panic"),
    ("Kernel panic", r"Kernel panic - not syncing"),
    ("Coprocesseur audio : erreur fatale", r"FATAL: Audio ROS"),
    ("Installateur : partition RedBoot introuvable", r"find mtd partition \[RedBoot\] by name fail"),
    ("Noyau : pas de table RedBoot", r"No RedBoot partition table detected"),
    ("Noyau : table RedBoot trouvée", r"\d+ RedBoot partitions found"),
    ("Modules : version magic incohérente", r"version magic .* should be"),
    ("Mode junior : init not health", r"init not health"),
    ("Version du noyau", r"Linux version \S+"),
    ("Invite de connexion DSM atteinte", r"login:"),
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
            if name == "Invite de connexion DSM atteinte":
                line = "(texte masqué : la ligne contient le nom du serveur)"
            print("%-48s x%-4d (ligne %d) %s" % (name, counts[name], n, line))
    print()
    if counts["Installateur : partition RedBoot introuvable"] or counts["Noyau : pas de table RedBoot"]:
        print("=> Table de partitions absente : voir docs/06-cause-racine.md et docs/08-procedure-reconstruction-fis.md")
    if counts["Boucle de démarrage (vérification du FSBL)"] or counts["Plantage noyau : Oops / BUG"] \
            or counts["Corruption réseau (skb_over_panic)"]:
        print("=> Signes d'instabilité matérielle (RAM) : voir docs/04-intervention-materielle.md")
    if counts["Modules : version magic incohérente"]:
        print("=> Noyau et système de fichiers initial de versions différentes : conséquence d'une installation jamais terminée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
