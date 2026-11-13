# Pièges rencontrés et enseignements

## Shell du mode junior (BusyBox v1.16.1)

- **Présents** : `cat`, `cut`, `dd`, `expr`, `printf` (intégré), `seq`, `grep`/`egrep`/`fgrep`, `head`, `tail`, `wc`, `xargs`, `vi`, `wget`, `httpd`, `telnetd`, `tar`, `gunzip`, `xz`, `mount`, `ifconfig`, `ping`.
- **Absents** : `od`, `hexdump`, `xxd`, `tr`, `cmp`, `md5sum`, `sed`, `awk`, `strings`, `uuencode`, `sort`, `uniq`.
- Solution : sauvegarder dans `/tmp` (en RAM) et le récupérer par `httpd -p 8081 -h /tmp`, puis analyser sur le PC.
- `/tmp` est en RAM : tout est perdu au redémarrage. Les dumps doivent être récupérés avant.

## Flash

- Lecture : `/dev/mtd0ro`. Écriture avec effacement automatique : `/dev/mtdblock0`. Le périphérique caractère `/dev/mtd0` n'efface pas.
- L'offset `0x7ff000` correspond à `seek=2047` avec des blocs de 4096 octets.

## Enseignements

1. **Toujours lire le journal de l'installateur** (`/var/log/messages`), pas seulement l'interface web : la vraie erreur y est (`find mtd partition [RedBoot] by name fail`).
2. **« Pouvant être migré » ne signifie pas toujours un problème de disque.** Ici, la cause se trouvait dans la flash.
3. **Sauvegarder la flash avant toute écriture**, avec deux copies et une vérification par somme de contrôle.
4. **Vérifier chaque étape avant d'écrire** : bloc construit, comparé, écrit, relu, comparé.
5. **Séparer les problèmes** : l'instabilité matérielle et la table de partitions vide étaient deux causes indépendantes, qui se masquaient mutuellement.
6. Ne pas confondre « Redémarrer » depuis DSM (la RAM reste alimentée) et un vrai **démarrage à froid** (alimentation coupée environ 10 s) pour tester la stabilité.
7. Un adaptateur série réglé en **3,3 V** est obligatoire pour la console UART.
8. **Première installation : prendre la version que Synology Assistant affiche pour le NAS** (ici 6.2.4-25556), avec le bon modèle. C'est une pratique observée, pas une règle testée contre d'autres versions ([réinstallation de DSM](09-reinstallation-dsm.md)).
9. **Brancher le NAS sur le routeur** (et non directement au PC) pour qu'il ait une adresse, Internet et l'heure. Sans cela, DSM ne détecte pas ses mises à jour.
