# Annexes

## A. Format d'une entrée RedBoot FIS (structure `fis_image_desc`)

```c
struct fis_image_desc {
    unsigned char name[16];     // nom, complété par des zéros
    uint32_t flash_base;        // adresse dans la flash
    uint32_t mem_base;          // adresse en mémoire (0 ici)
    uint32_t size;              // taille réservée
    uint32_t entry_point;       // point d'entrée (0 ici)
    uint32_t data_length;       // taille des données (= size ici)
    unsigned char _pad[256 - 16 - 5 * 4 - 2 * 4];  // 212 octets à 0xFF
    uint32_t desc_cksum;        // ignoré par le parseur Linux
    uint32_t file_cksum;        // ignoré par le parseur Linux
};
```

Le parseur Linux (`redboot.c`) cherche l'entrée nommée « FIS directory » dont la taille égale celle d'un secteur d'effacement (`0x1000`), puis lit les entrées. Une entrée libre commence par `0xFF`. L'adresse de base est masquée avec la taille de la flash moins 1.

## B. Étapes de démarrage observées

ROM, `hwsetting`, FSBL, U-Boot 2012.07, U-Boot 2015.07, puis noyau Linux. Avant la réparation, le noyau de la flash était un 4.4.302+ ; après la réinstallation, c'est le 4.4.59+ #25556 de DSM 6.2.4.

## C. Liste de contrôle rapide

- [ ] Console série en 3,3 V, 115200 8N1
- [ ] Deux dumps de la flash identiques (8 388 608 octets)
- [ ] Table vide à `0x7ff000` confirmée
- [ ] Noms de partitions confirmés (`RedBoot`, `zImage`, `rd.gz`, `vendor`, `FIS directory`)
- [ ] Bloc de 4096 octets construit et comparé à l'attendu
- [ ] Écriture, relecture, comparaison identique
- [ ] `/proc/mtd` : 5 partitions après redémarrage
- [ ] Réinstallation de DSM (« Réinstallation », fichier `.pat` officiel **de la version affichée par Synology Assistant**, bon modèle)
- [ ] Trois démarrages à froid réussis
- [ ] NAS branché au routeur, IP fixe (ou réservation DHCP) et heure synchronisée
- [ ] Test de stabilité prolongé terminé
- [ ] Nouvelle sauvegarde de la flash depuis le système fonctionnel

## D. Préparation des disques sous Windows (`diskpart`)

Pendant les essais, des disques ont été remis à zéro sur un PC Windows avant d'être réinsérés dans le NAS (le NAS écrivait parfois des fichiers de démarrage incomplets sur le disque). **`clean` efface tout le disque** : vérifie très soigneusement son numéro.

Dans une invite de commandes **lancée en administrateur** :

```text
diskpart
list disk
select disk <N>
clean
```

Remplace `<N>` par le numéro du disque du NAS (vérifie la taille dans `list disk`). Un script équivalent (`script_diskpart.txt`) contient simplement :

```text
select disk <N>
clean
```

et peut être lancé avec `diskpart /s script_diskpart.txt`.

**Stop :** si tu n'es pas certain du numéro du disque, ne tape pas `clean`. Le mauvais numéro efface un autre disque du PC.
