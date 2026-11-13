# Matériel et outils

## Matériel du NAS

| Composant | Détail |
|---|---|
| Modèle | Synology DS218 (confirmé par les journaux : `Synology Model: DS218`) |
| Carte | `HDR23L1` v1.1 (sérigraphie relevée sur les photos de la carte du DS218) |
| SoC | Realtek RTD1296 (ARM 64 bits) |
| RAM | 2 Gio de DDR4 à 1600 MHz, en 4 puces. Confirmé par la commande `bdinfo` d'U-Boot : `DC0 DDR4, total size is 4Gb(x16)x2=8Gb` et `DC1 DDR4, total size is 4Gb(x16)x2=8Gb` (2 canaux × 2 puces de 4 Gbit). [À VÉRIFIER : référence exacte des puces de RAM. Le repère **U3** est celui utilisé par l'auteur sur sa carte] |
| Flash | SPI NOR MXIC MX25L6445E, 8 Mo, secteurs de 4 Ko |
| Console | Connecteur UART J2, 115200 bauds, 8N1, niveau **3,3 V** |

## Outils utilisés

- Un adaptateur USB-série (puce FT232) réglé sur **3,3 V** (ne jamais utiliser 5 V sur ce connecteur).
- PuTTY (série, avec enregistrement de la session dans un fichier).
- Synology Assistant (détection du NAS et assistant d'installation web).
- Le fichier d'installation `DSM_DS218_25556.pat` (DSM 6.2.4-25556, environ 236 Mo), téléchargé sur le site officiel de Synology.
- Un PC Windows pour le téléchargement et l'analyse des dumps.

[INSÉRER PHOTO : carte mère du DS218, vue d'ensemble avec le connecteur UART J2 repéré]
[INSÉRER PHOTO : branchement de l'adaptateur USB-série sur J2 (masquer toute information personnelle visible)]
[INSÉRER PHOTO : zone des 4 puces de RAM, avec U3 repérée]
