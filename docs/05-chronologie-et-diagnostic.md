# Chronologie du diagnostic

1. **Constat initial** : DSM ne peut pas être configuré, le NAS reste « Pouvant être migré ».
2. **Branchement de la console série UART** pour lire les journaux de démarrage. Le démarrage est instable, des plantages aléatoires apparaissent.
3. **Stabilisation du matériel** : refusion à l'air chaud des 4 puces de RAM (plusieurs fois, avant et arrière, surtout U3), refroidissement, élément métallique de refroidissement qui presse aussi sur U3, ventilateur ([intervention matérielle](04-intervention-materielle.md)). Les tests de démarrage se déroulent ensuite sans erreur.
3b. **Tests de la RAM** (zones basse et haute) en ligne de commande ([tests de la RAM](04-intervention-materielle.md#tests-de-la-ram-zones-basse-et-haute)).
3c. **Début de la phase « lignes de commande »** sur la flash et le système, une fois le matériel stable.
4. **Analyse des journaux d'installation** : l'`updater` signale `find mtd partition [RedBoot] by name fail`. Le noyau ne voit qu'une partition.
5. **Accès au shell du mode junior** (BusyBox v1.16.1) sur la console série.
6. **Sauvegarde de la flash** : deux dumps complets de 8 388 608 octets, identiques (même somme SHA-256).
7. **Analyse du dump** : l'offset `0x7ff000` (FIS directory) est entièrement à `0xFF`. Les autres zones (noyau, ramdisk, données d'usine) sont présentes.
8. **Vérification de l'identité d'origine** : l'adresse MAC et le numéro de série trouvés dans la flash correspondent à l'étiquette collée sous le NAS.
9. **Recherche des noms de partitions attendus** par l'`updater` (chaînes de caractères trouvées dans le binaire) : `RedBoot`, `zImage`, `rd.gz`, `vendor`, `FIS directory`.
10. **Comparaison avec la disposition d'un DS418** décrite sur le forum Synoforum (voir [références](15-references.md)) pour déduire les offsets et tailles.
11. **Construction d'un bloc de 4 Ko** contenant 5 entrées, vérifié octet par octet.
12. **Écriture dans la flash**, relecture, comparaison identique.
13. **Redémarrage** : le noyau détecte 5 partitions.
14. **Réinstallation de DSM** : l'`updater` écrit `zImage` et `rd.gz`, le NAS redémarre sous DSM 6.2.4.
15. **Tests de démarrage à froid** (3 réussites), création du volume.

[INSÉRER PHOTO : capture de Synology Assistant avec le statut « Pouvant être migré » (masquer l'adresse IP, l'adresse MAC et le numéro de série)]
[INSÉRER PHOTO : assistant web avec les choix « Migration » / « Réinstallation »]

## Signatures dans les journaux

Quand tu lis un journal (PuTTY, fichier `.log`), ces lignes disent presque tout. Pour chaque signature : ce que ça signifie et où aller.

| Signature (texte à chercher) | Signification | Chapitre |
|---|---|---|
| `5-5verify fsbl fail` qui se répète | Le tout premier chargeur n'arrive pas à se vérifier : démarrage instable (cas observé avec la RAM défaillante) | [intervention matérielle](04-intervention-materielle.md) |
| `Oops`, `Internal error`, `kernel BUG at` | Plantage du noyau. Aléatoire d'un démarrage à l'autre = matériel (RAM) | [intervention matérielle](04-intervention-materielle.md) |
| `skb_over_panic` | Un compteur mémoire est corrompu (bit inversé) : RAM instable | [intervention matérielle](04-intervention-materielle.md) |
| `FATAL: Audio ROS Unexpected interrupt error` | Plantage précoce du coprocesseur audio, vu avec la RAM instable | [intervention matérielle](04-intervention-materielle.md) |
| `Kernel panic - not syncing` | Arrêt du noyau après une erreur grave | [intervention matérielle](04-intervention-materielle.md) |
| `find mtd partition [RedBoot] by name fail` | L'`updater` ne trouve pas la partition `RedBoot` : **table FIS absente** | [cause racine](06-cause-racine.md) |
| `No RedBoot partition table detected` | Le noyau ne voit pas de table : même cause | [cause racine](06-cause-racine.md) |
| `5 RedBoot partitions found on MTD device` | **Bon signe** : la table est lue, 5 partitions | [reconstruction](08-procedure-reconstruction-fis.md) |
| `version magic '4.4.59+' should be '4.4.302+'` | Modules du ramdisk et noyau de versions différentes (conséquence d'une installation incomplète) | [réinstallation](09-reinstallation-dsm.md) |
| `Exit on error [3] init not health` | L'installation a échoué | [réinstallation](09-reinstallation-dsm.md) |
| `Linux version ...` | Version du noyau réellement lancé | [réinstallation](09-reinstallation-dsm.md) |
| `login:` | Le démarrage est allé jusqu'au bout | |

### Script d'aide

Le script `scripts/analyze_log.py` cherche ces signatures dans un ou plusieurs journaux et propose le chapitre à lire :

```sh
python scripts/analyze_log.py mon_journal.log
```

Il ne modifie rien et n'affiche pas la ligne de connexion (qui contient le nom du serveur). **Ne publie jamais** les journaux eux-mêmes : ils contiennent le nom du serveur, parfois l'adresse IP, le numéro de série ou l'adresse MAC.
