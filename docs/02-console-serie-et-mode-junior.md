# Console série (UART) et shell du mode junior

Ce chapitre explique comment **voir ce que fait le NAS pendant qu'il démarre** et comment obtenir un **shell** dessus quand DSM n'est pas installé. Tout le reste du dépôt en dépend : sans journaux de démarrage, impossible de distinguer un problème matériel d'un problème logiciel.

> **Rappel :** ne branche jamais une tension de 5 V sur la console. Le connecteur UART de la carte travaille en **3,3 V**.

## 1. Pourquoi la console série

- L'interface web et Synology Assistant ne montrent qu'un état résumé (« Pouvant être migré »). La vraie raison d'un échec d'installation est dans les journaux du NAS.
- Les erreurs de tout début de démarrage (boucle `verify fsbl fail`, plantage du noyau avant le réseau) n'apparaissent **nulle part ailleurs** que sur la console série.
- La console série donne aussi accès à **U-Boot** (tests de la RAM) et au **shell du mode junior** (sauvegarde et réparation de la flash).

## 2. Matériel nécessaire

| Élément | Détail |
|---|---|
| Adaptateur USB-série | Une puce de type FT232, réglée sur **3,3 V** (cavalier ou interrupteur sur l'adaptateur) |
| Fils | 3 fils de liaison : masse (**GND**), **TX** et **RX**. Pas de fil d'alimentation (VCC) |
| Logiciel | PuTTY (Windows), ou tout terminal série (`screen`, `minicom`, `picocom` sous Linux) |

[INSÉRER PHOTO : l'adaptateur USB-série avec le sélecteur de tension sur 3,3 V]

## 3. Brancher l'adaptateur sur la carte

Le DS218 (carte `HDR23L1` v1.1) dispose d'un connecteur de service repéré **J2** qui est la console UART. Je n'ai pas relevé ici le brochage broche par broche : **identifie-le toi-même avant de brancher**.

1. **Éteins le NAS et débranche l'alimentation.**
2. Repère le connecteur **J2** sur la carte (sérigraphie à côté du connecteur).
3. Identifie la **masse (GND)** au multimètre en mode continuité : elle est reliée à la masse de la carte (par exemple le blindage du connecteur USB ou une vis de fixation métallique).
4. Identifie **TX** et **RX** : pendant le démarrage, la broche **TX du NAS** présente des variations autour de 3,3 V. Elle se branche sur le **RX de l'adaptateur**. La broche **RX du NAS** se branche sur le **TX de l'adaptateur**. Les deux sont **croisés**.
5. Ne branche **aucune** broche d'alimentation (VCC, 3,3 V, 5 V) de l'adaptateur sur la carte : le NAS s'alimente tout seul.
6. Si tu hésites sur une broche, **ne branche pas** : le mauvais fil peut endommager la carte.

**Stop :** si tu n'es pas certain du brochage, arrête-toi. Aucune étape du dépôt ne justifie de brancher « pour essayer ».

[INSÉRER PHOTO : le connecteur J2 repéré sur la carte]
[INSÉRER PHOTO : fils GND, TX et RX branchés sur J2 (masquer toute information personnelle visible)]

## 4. Configurer PuTTY

1. Branche l'adaptateur USB sur le PC. Dans le **Gestionnaire de périphériques** de Windows, ouvre **Ports (COM et LPT)** et note le numéro du port (par exemple `COM6`).
2. Lance PuTTY, choisis **Serial** (et non SSH) et renseigne :

| Paramètre | Valeur |
|---|---|
| Serial line | le port noté (par exemple `COM6`) |
| Speed (baud) | `115200` |
| Data bits | `8` |
| Stop bits | `1` |
| Parity | `None` |
| Flow control | `None` |

3. **Enregistre le journal dans un fichier** : dans la colonne de gauche, ouvre **Session > Logging**, coche **All session output** et mets un nom de fichier comme `ds218_&Y&M&D_&T.log` (PuTTY remplace `&Y&M&D_&T` par la date et l'heure). Tu auras ainsi un journal par session, sans avoir à rien copier à la main.
4. Clique sur **Open**, puis allume le NAS.

[INSÉRER PHOTO : fenêtre de configuration de PuTTY en mode Serial (115200, 8N1, pas de contrôle de flux)]
[INSÉRER PHOTO : option « All session output » cochée dans Session > Logging]

## 5. Lire un démarrage

Les étapes que tu vois défiler, dans l'ordre :

| Ce que tu vois | Étape |
|---|---|
| `C1:80000000`, `C2`, `C3h`, puis des lignes `hwsetting_...` et `secure_fsbl_...` | Boot ROM du SoC, lecture du hwsetting et du FSBL |
| `U-Boot 2012.07 ...` puis `U-Boot 2015.07 ...` | Chargeurs U-Boot |
| `Hit Esc or Tab key to enter console mode or rescue linux` | **Fenêtre pour entrer dans la console U-Boot** (appuie sur Échap) |
| `Starting Kernel ...` | Lancement du noyau Linux |
| `[    0.000000] Linux version ...` | Début du journal du noyau |
| `DiskStation login:` | Le système est démarré |

Un démarrage sain de ce DS218 sous DSM arrive à l'invite de connexion environ **50 s** après la mise sous tension.

Quelques repères pour reconnaître un démarrage raté :
- une **boucle** qui répète `C1:80000000` … `verify fsbl fail` : le démarrage n'avance pas ;
- `Internal error: Oops`, `Kernel panic` ou `FATAL: Audio ROS Unexpected interrupt error!!` : plantage du noyau ;
- un blocage sans message après `reading byte size = 0x002f0000` (lecture du noyau).

Les signatures et leur interprétation sont dans le chapitre [chronologie et diagnostic](05-chronologie-et-diagnostic.md). Le script `scripts/analyze_log.py` les repère automatiquement dans un journal.

## 6. Entrer dans la console U-Boot

1. Éteins le NAS, ouvre la session PuTTY, rallume.
2. Dès que le message `Hit Esc or Tab key to enter console mode or rescue linux` apparaît, appuie plusieurs fois sur **Échap**.
3. L'invite devient `Realtek>`. Tape `help` pour la liste des commandes.

Commandes utiles ici (vérifie avec `help` ce que ton U-Boot propose) : `bdinfo` (informations sur la mémoire et les horloges), `mw` / `md` (écrire et afficher la mémoire), `mtest` et `mtest2` (tests de la RAM, voir le chapitre [intervention matérielle](04-intervention-materielle.md)), `reset` (redémarrer).

**Attention :** U-Boot sert à observer. N'utilise ni `saveenv`, ni `rtkspi`, ni `fatwrite`, ni `keyset`, ni `uart_write` sans savoir exactement ce que tu fais. Une erreur peut effacer le chargeur ou l'identité d'usine.

## 7. Le shell du mode junior

Quand DSM n'est pas (ou plus) installé, le NAS démarre en **mode junior** : un mini-système en RAM, suffisant pour recevoir une installation. C'est dans ce mode que Synology Assistant affiche le statut « Pouvant être migré » ou « Non installé ».

1. Laisse le démarrage aller jusqu'à `DiskStation login:`.
2. Connecte-toi avec l'utilisateur **`root`** et le mot de passe du mode junior de Synology : c'est une valeur par défaut documentée publiquement (cherche « Synology junior mode root password »). Elle est **`101-0101`** sur les DSM 6.2.
3. Tu obtiens un shell BusyBox : `BusyBox v1.16.1 ... built-in shell (ash)`.

**Sois conscient de ce que ça implique :** ce shell est un shell administrateur complet sur le NAS. Une commande mal tapée sur `/dev/mtd*` ou sur un disque est irréversible.

### Outils disponibles et absents

Constaté sur ce NAS (la liste n'est pas exhaustive) :

| Présents (utilisés ici) | Absents (constatés) |
|---|---|
| `cat`, `dd`, `printf`, `ls`, `tail`, `grep`, `ifconfig`, `httpd`, `vi` | `od`, `hexdump`, `md5sum`, `tr`, `cmp`, `sed`, `awk`, `strings` |

Teste toujours un outil avant de compter dessus : `which od` ne renvoie rien s'il manque.

Conséquence pratique : **on ne peut pas analyser une flash sur le NAS**. On la copie sur le PC et on l'analyse là-bas (voir ci-dessous).

### Récupérer un fichier du NAS vers le PC

`/tmp` est en **RAM** : tout est perdu au redémarrage, donc récupère tes fichiers avant. Pour les télécharger, lance un petit serveur web :

```sh
httpd -p 8081 -h /tmp
```

Puis, sur le PC, ouvre `http://<IP_NAS>:8081/<nom_du_fichier>` dans un navigateur. Si le message `bind: Address already in use` apparaît, c'est que le serveur tourne déjà.

Pour connaître l'adresse du NAS en mode junior : `ifconfig` (ou Synology Assistant). Une adresse `169.254.x.x` indique qu'aucun serveur DHCP n'a répondu : voir [après l'installation](10-apres-installation.md).

### Lire les journaux du mode junior

```sh
tail -n 60 /var/log/messages     # derniers messages (installation, erreurs de l'updater)
tail -f /var/log/messages        # suivre en direct (Ctrl+C pour arrêter)
dmesg | tail -n 80               # journal du noyau
cat /proc/mtd                    # partitions de la flash (voir chapitre 07)
```

Si tu lances `tail -f` **avant** une installation et que tu ne touches plus au terminal, le journal reste complet. Si tu ouvres un autre terminal pendant, il peut se perdre.

[INSÉRER PHOTO : invite `DiskStation login:` puis shell BusyBox dans PuTTY (masquer le nom du serveur)]
[INSÉRER PHOTO : sortie de `cat /proc/mtd` en mode junior (une seule partition `RtkSFC`)]
