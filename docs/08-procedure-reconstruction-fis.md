# Procédure : reconstruire la table des partitions (FIS directory)

> **Lis les [avertissements](00-avertissements.md) avant de toucher à la flash.**

## Prérequis

- Accès console série au NAS en mode junior (connexion `root` avec le mot de passe par défaut du mode junior de Synology, à vérifier dans la documentation Synology).
- Un PC relié au même réseau que le NAS, pour récupérer les fichiers par le petit serveur web de BusyBox.
- Un NAS **stable** (pas de plantages pendant plusieurs minutes).
- Le fichier `.pat` de la **version affichée par Synology Assistant** pour ton modèle (voir [réinstallation de DSM](09-reinstallation-dsm.md)).

## Étape 1 : Sauvegarder la flash (indispensable)

Dans le shell du NAS (BusyBox) :

```sh
dd if=/dev/mtd0ro of=/tmp/flash1.bin bs=4096
dd if=/dev/mtd0ro of=/tmp/flash2.bin bs=4096
httpd -p 8081 -h /tmp
```

Puis sur le PC, télécharge `http://<IP_NAS>:8081/flash1.bin` et `http://<IP_NAS>:8081/flash2.bin`.

**Contrôle :** chaque fichier doit faire **8 388 608 octets** et les deux doivent avoir la **même somme SHA-256** (sous Windows : `certutil -hashfile flash1.bin SHA256`). Sans copies identiques, ne continue pas.

[INSÉRER PHOTO : terminal PuTTY avec les deux commandes `dd` (masquer l'adresse IP)]

> Le mode junior n'a ni `od`, ni `hexdump`, ni `md5sum`, ni `sed`, ni `awk`. L'analyse se fait donc sur le PC.

## Étape 2 : Vérifier que la table est bien vide

Sur le PC (Python), contrôle que 4096 octets à l'offset `0x7ff000` sont tous à `0xFF` :

```python
d = open("flash1.bin", "rb").read()
blk = d[0x7ff000:0x800000]
print(len(blk), all(b == 0xFF for b in blk))   # attendu : 4096 True
```

## Étape 3 : Confirmer les noms de partitions attendus

Dans le shell du NAS, monte la partition système temporaire et cherche les noms dans l'outil `updater` :

```sh
mkdir -p /mnt/d
mount /dev/md0 /mnt/d
grep -a -o -E "RedBoot|zImage|rd\.gz|vendor|FIS directory" /mnt/d/.updater
umount /mnt/d
```

Résultat observé : `RedBoot`, `vendor`, `FIS directory`, `zImage`, `rd.gz`.

## Étape 4 : Construire le bloc de 4 Ko dans la RAM du NAS

Format d'une entrée (256 octets, valeurs de 32 bits en petit-boutiste) :

| Octets | Champ |
|---|---|
| 0–15 | `name` (texte, complété par des zéros) |
| 16–19 | `flash_base` |
| 20–23 | `mem_base` (0) |
| 24–27 | `size` |
| 28–31 | `entry_point` (0) |
| 32–35 | `data_length` (= `size`) |
| 36–247 | remplissage `0xFF` (212 octets) |
| 248–255 | `desc_cksum` et `file_cksum` (zéros) |

Les 5 entrées occupent les 1280 premiers octets. Le reste du bloc est rempli de `0xFF`.

Les lignes suivantes se collent telles quelles dans le shell du NAS. Elles utilisent seulement `printf` (intégré à BusyBox) et `dd` :

```sh
i=0; while [ $i -lt 4096 ]; do printf '\377'; i=$((i+1)); done > /tmp/ff4k
rm -f /tmp/fis_new.bin
{ printf '\122\145\144\102\157\157\164\000\000\000\000\000\000\000\000\000'; printf '\000\000\000\000\000\000\000\000\000\000\020\000\000\000\000\000\000\000\020\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
{ printf '\172\111\155\141\147\145\000\000\000\000\000\000\000\000\000\000'; printf '\000\000\020\000\000\000\000\000\000\000\057\000\000\000\000\000\000\000\057\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
{ printf '\162\144\056\147\172\000\000\000\000\000\000\000\000\000\000\000'; printf '\000\000\077\000\000\000\000\000\000\360\077\000\000\000\000\000\000\360\077\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
{ printf '\166\145\156\144\157\162\000\000\000\000\000\000\000\000\000\000'; printf '\000\360\176\000\000\000\000\000\000\000\001\000\000\000\000\000\000\000\001\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
{ printf '\106\111\123\040\144\151\162\145\143\164\157\162\171\000\000\000'; printf '\000\360\177\000\000\000\000\000\000\020\000\000\000\000\000\000\000\020\000\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
dd if=/tmp/ff4k bs=1 count=2816 2>/dev/null >> /tmp/fis_new.bin
ls -l /tmp/fis_new.bin
```

**Contrôle :** `ls -l` doit afficher exactement **4096** octets. Sinon, arrête-toi.

[INSÉRER PHOTO : sortie de `ls -l /tmp/fis_new.bin` dans PuTTY]

## Étape 5 : Vérifier le bloc avant de l'écrire

Récupère `fis_new.bin` sur le PC par `httpd` (voir l'étape 1) et compare-le au bloc attendu. Générateur Python équivalent :

```python
import struct
ents = [("RedBoot", 0x0, 0x100000), ("zImage", 0x100000, 0x2f0000),
        ("rd.gz", 0x3f0000, 0x3ff000), ("vendor", 0x7ef000, 0x10000),
        ("FIS directory", 0x7ff000, 0x1000)]

def entry(name, base, size):
    nm = name.encode().ljust(16, b"\0")
    return nm + struct.pack("<5I", base, 0, size, 0, size) + b"\xff" * 212 + b"\0" * 8

blk = b"".join(entry(*e) for e in ents).ljust(4096, b"\xff")
open("fis_expected.bin", "wb").write(blk)
```

Compare avec `cmp fis_new.bin fis_expected.bin` (ou avec les sommes SHA-256). **N'écris rien tant qu'ils ne sont pas identiques.**

## Étape 6 : Écrire le secteur dans la flash

```sh
dd if=/tmp/fis_new.bin of=/dev/mtdblock0 bs=4096 seek=2047 count=1
sync
```

Attendu : `1+0 records in` et `1+0 records out`.

Notes techniques :
- `seek=2047` correspond à l'offset `2047 × 4096 = 0x7ff000`.
- On écrit par `/dev/mtdblock0` parce que la couche bloc gère l'effacement du secteur avant l'écriture. Le périphérique caractère `/dev/mtd0` n'efface pas.

## Étape 7 : Relire et comparer

```sh
dd if=/dev/mtd0ro of=/tmp/fis_back.bin bs=4096 skip=2047 count=1
ls -l /tmp/fis_back.bin
```

Récupère `fis_back.bin` par `httpd` et compare-le au bloc écrit : il doit être **identique**. **Ne redémarre pas avant d'avoir confirmé cette identité.**

## Étape 8 : Redémarrer et contrôler les partitions

Après `reboot` et reconnexion en mode junior :

```sh
cat /proc/mtd
dmesg | grep -i -E "redboot|partition|mtd"
```

Résultat obtenu :

```text
dev:    size   erasesize  name
mtd0: 00100000 00001000 "RedBoot"
mtd1: 002f0000 00001000 "zImage"
mtd2: 003ff000 00001000 "rd.gz"
mtd3: 00010000 00001000 "vendor"
mtd4: 00001000 00001000 "FIS directory"

Searching for RedBoot partition table in RtkSFC at offset 0x7ff000
5 RedBoot partitions found on MTD device RtkSFC
Creating 5 MTD partitions on "RtkSFC":
```

**Arrête-toi ici** si `/proc/mtd` ne liste pas les 5 partitions. Ne lance pas la réinstallation dans ce cas.

[INSÉRER PHOTO : `cat /proc/mtd` avant correction (une seule partition)]
[INSÉRER PHOTO : `cat /proc/mtd` après correction (5 partitions)]

## Étape 9 : Retour arrière possible

L'état d'origine était un secteur entièrement à `0xFF`. En cas de problème, on peut le remettre à cet état avec le fichier `/tmp/ff4k` (4096 octets à `0xFF`) :

```sh
dd if=/tmp/ff4k of=/dev/mtdblock0 bs=4096 seek=2047 count=1
sync
```

Les deux dumps complets de la flash restent la sauvegarde de référence. Garde-les en lieu sûr.
