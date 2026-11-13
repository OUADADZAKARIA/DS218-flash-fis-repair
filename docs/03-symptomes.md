# Symptômes observés

## Symptômes logiciels (cause du blocage)

- Synology Assistant affiche le NAS avec le statut **« Pouvant être migré »**, y compris après plusieurs réinstallations et même après effacement des disques.
- L'assistant web ne propose que « Migration » ou « Réinstallation ». Le résultat est identique dans les deux cas.
- Après l'envoi du fichier `.pat`, l'installation semble se dérouler, puis le NAS redémarre dans le même état.
- Dans le journal de la console, à chaque tentative :

```text
find mtd partition [RedBoot] by name fail
fail to map all device partition
fail to malloc mtd driver buffer, error = 38
...
No upgrade file exists
Exit on error [3] init not health....
```

- Dans le journal du noyau :

```text
Searching for RedBoot partition table in RtkSFC at offset 0x7ff000
No RedBoot partition table detected
using single partition
```

- Et `/proc/mtd` ne contenait qu'une seule partition :

```text
dev:    size   erasesize  name
mtd0: 00800000 00001000 "RtkSFC"
```

- Tous les modules du noyau échouaient au chargement avec :

```text
phy_rtk_usb2: version magic '4.4.59+ SMP mod_unload aarch64' should be '4.4.302+ SMP mod_unload aarch64'
```

  Cause : la flash contenait un noyau 4.4.302+ avec un système de fichiers initial de la famille 6.2.4-25556 (modules compilés pour 4.4.59+). Cette incohérence ne disparaissait jamais parce que l'installation ne se terminait pas.

- Le numéro de série affiché était vide ou à 0 et l'adresse MAC changeait à chaque démarrage (valeurs aléatoires), car la partition `vendor` n'était pas lisible.

## Symptômes matériels (traités séparément)

### Alimentation et voyants (avant l'intervention)

Avant toute réparation, le comportement à la mise sous tension variait d'un essai à l'autre :

| Cas observé | Description |
|---|---|
| A | Le **bouton d'alimentation clignote en bleu** et **aucun autre voyant** ne s'allume |
| B | Le voyant du bouton d'alimentation est **fixe**, le voyant **Status clignote en vert**, et le NAS émet un **bip** |
| C | Seul le **bouton d'alimentation clignote** |
| D | Les voyants **LAN** et **disque** ne s'allument jamais, même avec des disques insérés |
| E | Avec un disque **non alloué** inséré : retour au cas A (le bouton clignote en bleu, rien d'autre) |
| F | Avec **un seul disque** préalablement formaté sous Windows (système de fichiers de type ext) : le NAS devient **visible sur le réseau**, le voyant Status clignote en vert et le bouton d'alimentation reste fixe. D'après la description de l'auteur, c'était la seule méthode qui rendait le NAS visible au début |

### Blocages de démarrage (journaux de la console série)

Les journaux de la console série (24 fichiers de session PuTTY relevés pendant ce dépannage) montrent plusieurs familles d'échecs. Les extraits ci-dessous sont tirés de ces journaux.

**1. Boucle de redémarrage au tout début du démarrage (vérification du FSBL).** Le démarrage ne dépasse pas la ROM : le NAS répète en boucle les mêmes lignes, jusqu'à ce que, parfois, un essai passe.

```text
C1:80000000
C2
?
C3h
hwsetting size: 00000B94
C4
f
5-5verify fsbl fail
0000003BC7
C1:80000000
C2
?uu3-1
```

**2. Plantage du noyau très tôt (environ 8 s après le démarrage du noyau).** Une erreur d'accès mémoire, puis une boucle d'erreurs du coprocesseur audio, puis un arrêt total :

```text
[    7.982879] Internal error: Oops: 96000006 [#1] SMP
[    8.354466] Internal error: Oops: 96000005 [#2] SMP
FATAL: Audio ROS Unexpected interrupt error!!
FATAL: Audio ROS Unexpected interrupt error!!
[    8.796186] Internal error: Oops - undefined instruction: 0 [#3] SMP
[    9.870675] Kernel panic - not syncing: Fatal exception in interrupt
```

(Le texte de ce journal était en partie déformé : instruction « inexistante », caractères illisibles. C'est cohérent avec une corruption de la mémoire.)

**3. Corruption mémoire plus tard, pendant l'installation ou l'utilisation.** Exemples relevés :

```text
[   55.379818] kernel BUG at mm/slab.c:2816!
[   55.384722] Internal error: Oops - BUG: 0 [#1] SMP
[   55.394723] CPU: 1 PID: 2134 Comm: findhostd Not tainted 4.4.302+ #90080
[   55.412021] PC is at cache_alloc_refill+0x22c/0x560

[  119.840990] skbuff: skb_over_panic: text:ffffffc0006360f4 len:1514 put:1514 head:ffffffc073071000 data:ffffffc073071088 tail:0x800672 end:0x680 dev:<NULL>
[  120.798638] Kernel panic - not syncing: Fatal exception in interrupt
```

Dans le dernier cas, `tail` devrait valoir `0x672` : l'écart avec `0x800672` est exactement le **bit 23** (`0x00800000`). C'est le même bit qui était faux dans d'autres plantages : l'adresse de retour `d65f03c0` lue comme `d6df03c0`, et un compteur de programme `…6aecf0` lu comme `…eaecf0`. Toujours le même bit, toujours de 0 vers 1. Un fil de données de la mémoire ou une soudure marginale correspondent à ce profil, pas un défaut logiciel.

Ces plantages se distinguent bien de la cause finale ([cause racine](06-cause-racine.md)) : celle-ci provoque une erreur **propre et répétable** de l'installateur, sans plantage du noyau.

### Effet de la pression sur la puce U3

**Une pression avec la main sur la puce U3 assurait un bon démarrage.** Sans cette pression, les journaux montraient les blocages décrits plus haut. C'est le meilleur indice d'un contact de soudure défaillant sous cette puce (soudures de type BGA fissurées).

[INSÉRER PHOTO : extrait de log avec `skb_over_panic` (masquer toute donnée personnelle)]
[INSÉRER PHOTO : extrait de log avec un blocage à la lecture du noyau (offset `0x002f0000`)]
[INSÉRER PHOTO : état des voyants du NAS pendant un démarrage raté (bouton d'alimentation qui clignote, autres voyants éteints)]
