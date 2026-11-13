# Images à fournir

Ce dossier est vide volontairement : les photos et captures contiennent des données personnelles. Chaque balise `[INSÉRER PHOTO : ...]` des chapitres indique ce qu'il faut ajouter.

Règles : voir [vie privée](../docs/PRIVACY.md). Floute (puis exporte en image aplatie) : numéro de série, adresse MAC, adresses IP, nom du serveur, utilisateur, étiquette du NAS. Nomme les fichiers `chapitre-NN-description.png`.

## Liste des photos par chapitre

### 01-materiel-et-outils.md

- [ ] carte mère du DS218, vue d'ensemble avec le connecteur UART J2 repéré. Utiliser des photos du bon appareil
- [ ] branchement de l'adaptateur USB-série sur J2 (masquer toute information personnelle visible)
- [ ] zone des 4 puces de RAM, avec U3 repérée. Utiliser des photos du bon appareil

### 02-console-serie-et-mode-junior.md

- [ ] l'adaptateur USB-série avec le sélecteur de tension sur 3,3 V
- [ ] le connecteur J2 repéré sur la carte
- [ ] fils GND, TX et RX branchés sur J2 (masquer toute information personnelle visible)
- [ ] fenêtre de configuration de PuTTY en mode Serial (115200, 8N1, pas de contrôle de flux)
- [ ] option « All session output » cochée dans Session > Logging
- [ ] invite `DiskStation login:` puis shell BusyBox dans PuTTY (masquer le nom du serveur)
- [ ] sortie de `cat /proc/mtd` en mode junior (une seule partition `RtkSFC`)

### 03-symptomes.md

- [ ] extrait de log avec `skb_over_panic` (masquer toute donnée personnelle)
- [ ] extrait de log avec un blocage à la lecture du noyau (offset `0x002f0000`)
- [ ] état des voyants du NAS pendant un démarrage raté (bouton d'alimentation qui clignote, autres voyants éteints)

### 04-intervention-materielle.md

- [ ] boîtier ouvert, vue d'ensemble
- [ ] carte retirée, côté avant (puces de RAM)
- [ ] carte retirée, côté arrière (puces de RAM)
- [ ] zone chauffée avec la protection des composants voisins
- [ ] plaque utilisée pendant l'opération
- [ ] élément métallique de refroidissement en place, avec la pression sur U3
- [ ] position finale du ventilateur
- [ ] capture du terminal U-Boot avec `bdinfo` (adresses IP et MAC par défaut à masquer si elles apparaissent)
- [ ] capture du terminal U-Boot avec les résultats `mtest` zones basse et haute
- [ ] capture du terminal U-Boot avec `mtest2 ... 0 errors`

### 05-chronologie-et-diagnostic.md

- [ ] capture de Synology Assistant avec le statut « Pouvant être migré » (masquer l'adresse IP, l'adresse MAC et le numéro de série)
- [ ] assistant web avec les choix « Migration » / « Réinstallation »

### 08-procedure-reconstruction-fis.md

- [ ] terminal PuTTY avec les deux commandes `dd` (masquer l'adresse IP)
- [ ] sortie de `ls -l /tmp/fis_new.bin` dans PuTTY
- [ ] `cat /proc/mtd` avant correction (une seule partition)
- [ ] `cat /proc/mtd` après correction (5 partitions)

### 09-reinstallation-dsm.md

- [ ] capture de Synology Assistant après réparation, avec le numéro de série et la MAC affichés (à masquer avant publication)
- [ ] étiquette du NAS (à masquer entièrement avant publication)
- [ ] page de configuration DSM, premier écran
- [ ] Synology Assistant, NAS « Pouvant être migré » (masquer IP, MAC, numéro de série)
- [ ] choix « Réinstallation » dans l'assistant web
- [ ] barre de progression de l'installation
- [ ] écran « Bienvenue » de l'assistant de configuration DSM
- [ ] bureau DSM (masquer le nom du serveur et l'adresse)

### 10-apres-installation.md

- [ ] fenêtre de configuration réseau manuelle (masquer toutes les adresses)
- [ ] assistant de création de dossier partagé
- [ ] File Station, option Télécharger

### 11-tests-de-stabilite.md

- [ ] journal de démarrage à froid avec l'invite de connexion (masquer le nom du serveur)
- [ ] Gestionnaire de stockage avec le volume créé et la vérification en cours
- [ ] informations de santé du disque (masquer le numéro de série du disque)

Total : 43 images.
