# Après l'installation : réseau, heure, sauvegarde, mises à jour

Une fois l'assistant DSM terminé, voici ce qu'il reste à faire. Rien de cela n'est nécessaire à la réparation, mais plusieurs surprises sont survenues pendant la mise en service.

## 1. Réseau

**Le NAS doit être branché au routeur.** Branché directement au PC, il prend une adresse de secours en `169.254.x.x` (aucun serveur DHCP ne répond). Il est alors accessible depuis le PC, mais n'a ni passerelle, ni Internet, ni heure. Une fois branché sur un port LAN du routeur, il reçoit une adresse et accède à Internet.

**Adresse fixe (recommandé) :** **Panneau de configuration > Réseau > Interface réseau > Modifier**, puis configuration manuelle (adresse, masque, passerelle, DNS). Choisis une adresse **hors de la plage DHCP** du routeur. Variante plus sûre : réserver l'adresse dans le routeur (réservation DHCP) et laisser le NAS en automatique.

[INSÉRER PHOTO : fenêtre de configuration réseau manuelle (masquer toutes les adresses)]

## 2. Heure et fuseau horaire

Sans Internet, l'horloge du NAS était à l'année 2016 (dates fausses dans les journaux et le volume). Avec Internet :

1. **Panneau de configuration > Région > Heure**.
2. Choisis un serveur NTP (par exemple `time.google.com`) et active la synchronisation.
3. Choisis **le fuseau horaire de ta région en prenant la ligne qui gère l'heure d'été**, sinon l'heure est décalée d'une heure une partie de l'année.

## 3. Dossier personnel absent

Tant qu'aucun volume n'existe, un utilisateur n'a pas de dossier personnel. Le message `change directory failed` à la connexion sur la console est normal ; il disparaît après la création du volume et l'activation du service de dossiers personnels.

## 4. Volume

SHR + Btrfs. Avec un seul disque, aucune protection contre une panne. Avec deux disques, SHR apporte la redondance. **La création efface les disques** : mets-y d'abord un disque de test, ou des disques vides. Avant de remplacer des disques, éteins le NAS **proprement depuis DSM**.

Pense à lancer un test S.M.A.R.T. (**Gestionnaire de stockage > HDD/SSD**) : il vérifie le disque, pas le NAS.

## 5. Dossier partagé et File Station (méthode simple pour récupérer des fichiers)

Pour télécharger un fichier du NAS sur le PC sans ligne de commande :

1. **Panneau de configuration > Dossier partagé > Créer** : donne un nom (par exemple `sauvegarde`), laisse les options par défaut, donne ton utilisateur en lecture/écriture.
2. Copie le fichier dans ce dossier (voir la section suivante pour la flash).
3. Ouvre **File Station**, clic droit sur le fichier > **Télécharger**.

[INSÉRER PHOTO : assistant de création de dossier partagé]
[INSÉRER PHOTO : File Station, option Télécharger]

## 6. Sauvegarde de la flash, et un piège

Une fois la table FIS reconstruite, **sauvegarde la flash** : c'est la seule copie de l'identité d'usine (adresse MAC, numéro de série, dans `vendor`) et des chargeurs.

> **Piège : `/dev/mtd0ro` ne contient plus toute la flash.** Avant la réparation, la flash était vue d'un seul bloc de 8 Mio. Une fois la table FIS présente, le noyau la découpe en 5 partitions. `/dev/mtd0ro` n'est plus que la première, `RedBoot` (**1 Mio**). Un `dd` sur `mtd0ro` donne donc un fichier de 1 048 576 octets, **incomplet**.

Il faut copier les cinq partitions et les mettre bout à bout, dans l'ordre :

| Partition | Périphérique | Taille (octets) |
|---|---|---|
| RedBoot | `/dev/mtd0ro` | 1 048 576 |
| zImage | `/dev/mtd1ro` | 3 080 192 |
| rd.gz | `/dev/mtd2ro` | 4 190 208 |
| vendor | `/dev/mtd3ro` | 65 536 |
| FIS directory | `/dev/mtd4ro` | 4 096 |
| **Total** | | **8 388 608** |

Procédure (SSH activé dans **Panneau de configuration > Terminal et SNMP**, puis PuTTY en mode SSH, ou console série) :

```sh
cd /volume1
sudo sh -c 'for i in 0 1 2 3 4; do dd if=/dev/mtd${i}ro of=flash_part${i}.bin bs=4096; done'
sudo sh -c 'cat flash_part0.bin flash_part1.bin flash_part2.bin flash_part3.bin flash_part4.bin > flash_full.bin'
ls -l flash_full.bin        # doit afficher 8388608
```

Place ensuite `flash_full.bin` dans le dossier partagé, télécharge-le avec File Station, puis vérifie-le sur le PC :

```sh
python scripts/check_flash_dump.py flash_full.bin
```

Le script contrôle la taille, affiche la somme SHA-256 et dit si la table FIS est présente. Une table présente après réparation est le résultat attendu.

**Stop :** si `ls -l` n'affiche pas `8388608`, ne conserve pas ce fichier comme sauvegarde.

**Ne publie jamais ce fichier** : il contient l'adresse MAC et le numéro de série d'origine.

## 7. Mises à jour de DSM

- Avant l'accès à Internet, DSM affichait à tort « Votre version de DSM est à jour ». Une fois en ligne, il propose les mises à jour de la même branche (6.2.4, une « Update » plus récente) ainsi que DSM 7.
- Sur ce NAS, j'ai fini sur **DSM 7.4.1-90080 Update 1** (noyau `4.4.302+`). Ce noyau est celui qui était déjà dans la flash avant la réparation : le NAS avait donc fonctionné sous ce DSM auparavant.
- Ces mises à jour réécrivent `zImage` et `rd.gz`, ce qui modifie la table FIS (la taille déclarée de `zImage` change). C'est normal.
- Fais-les **après** les tests de stabilité et avec une sauvegarde de la flash prise **avant**.
- Je n'ai pas vérifié formellement quelles versions de DSM 7 sont officiellement prises en charge pour ce modèle : je constate seulement que 7.4.1 fonctionne ici. Consulte la fiche du modèle chez Synology.
- DSM 6.2 n'est plus maintenue par Synology.

## 8. Température et boîtier

Le NAS a fonctionné ouvert pendant la réparation. Au remontage : refixer le ventilateur, vérifier l'écoulement de l'air, puis surveiller la température du disque et du système dans **Gestionnaire de ressources**. Refaire quelques démarrages à froid une fois le boîtier fermé : un défaut de RAM par intermittence peut revenir avec la chaleur ([tests de stabilité](11-tests-de-stabilite.md)).
