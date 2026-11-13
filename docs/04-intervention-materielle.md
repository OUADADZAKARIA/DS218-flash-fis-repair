# Intervention matérielle et tests de la RAM

## Intervention matérielle

> **À savoir avant de lire :** le repère **U3** est celui utilisé par l'auteur sur sa propre carte (`HDR23L1` v1.1). Vérifie le repérage sur la tienne (voir [matériel et outils](01-materiel-et-outils.md)).

> Les champs marqués `[À COMPLÉTER]` sont des détails non fournis. Ne publie pas le document sans les remplir ou les supprimer.

**Ce qui a été fait :**

1. Le boîtier a été ouvert et la carte mère dégagée. [À COMPLÉTER : étapes d'ouverture, vis, ordre]
2. Les **4 puces de RAM ont été chauffées à l'air chaud, plusieurs fois, côté avant et côté arrière de la carte**, avec une attention particulière pour **U3**.
3. La carte a été laissée **refroidir** entre les opérations.
4. Une **plaque** est utilisée pendant l'opération et **brûle au toucher**. [À PRÉCISER : plaque chauffante de préchauffage ou plaque métallique de dissipation]
5. Un **élément métallique de refroidissement** a été ajouté sur les puces. Il sert aussi à **maintenir une pression sur U3**.
6. Un ventilateur a été placé pour refroidir la carte pendant les essais. Au début, il était mal placé.

**Refusion à l'air chaud (à compléter) :**

| Paramètre | Valeur |
|---|---|
| Outil utilisé | [À COMPLÉTER : station à air chaud, décapeur…] |
| Température de consigne | [À COMPLÉTER] |
| Durée par puce et nombre de passes | [À COMPLÉTER] |
| Flux d'air et buse | [À COMPLÉTER] |
| Flux de soudure | [À COMPLÉTER : oui/non, type] |
| Protection des composants voisins | [À COMPLÉTER] |
| Ordre des puces | [À COMPLÉTER] |
| Description de l'élément de refroidissement | [À COMPLÉTER : matière, dimensions, fixation] |

[INSÉRER PHOTO : boîtier ouvert, vue d'ensemble]
[INSÉRER PHOTO : carte retirée, côté avant (puces de RAM)]
[INSÉRER PHOTO : carte retirée, côté arrière (puces de RAM)]
[INSÉRER PHOTO : zone chauffée avec la protection des composants voisins]
[INSÉRER PHOTO : plaque utilisée pendant l'opération]
[INSÉRER PHOTO : élément métallique de refroidissement en place, avec la pression sur U3]
[INSÉRER PHOTO : position finale du ventilateur]

**Résultat observé :** après ces interventions, les **tests de démarrage se sont faits sans erreur**. C'est seulement à ce moment-là que la phase « lignes de commande » a vraiment commencé ([chronologie](05-chronologie-et-diagnostic.md) et [procédure](08-procedure-reconstruction-fis.md)).

**Avertissements propres à cette intervention :**

- La refusion à l'air chaud peut **détruire** la carte (puces, condensateurs, connecteurs voisins) si la température ou la durée sont mal maîtrisées. Les valeurs de ce chapitre ne sont pas une recommandation.
- L'amélioration est un fait, mais on **ne sait pas laquelle des interventions** (refusion répétée, élément de refroidissement et de pression, ventilateur) en est la cause. Elles n'ont pas été testées séparément.
- Un élément métallique posé sur une carte alimentée peut provoquer un court-circuit ou gêner la ventilation. À vérifier avant toute mise sous tension prolongée.
- Les surfaces chauffées brûlent. Laisser refroidir complètement avant de toucher.
- Cette intervention annule la garantie du NAS.

## Tests de la RAM (zones basse et haute)

Des tests de la mémoire ont été faits depuis la **console U-Boot** (prompt `Realtek>`), sur une zone **basse** et une zone **haute** de la mémoire, puis sur la plage étendue. Journal d'origine : session du 21/10/2026.

**Entrer dans la console U-Boot :** pendant le démarrage, quand le message suivant apparaît, appuyer sur **Échap** (ou Tab) :

```text
Hit Esc or Tab key to enter console mode or rescue linux:  0
Press Esc Key
Enter console mode, disable watchdog ...
Realtek>
```

**Informations sur la mémoire (`bdinfo`) :**

```text
DRAM bank   = 0x00000000
-> size     = 0x80000000          (2 Gio)
DDR        =  1600 MHz (0x1a)
DC0 DDR4, total size is 4Gb(x16)x2=8Gb
DC1 DDR4, total size is 4Gb(x16)x2=8Gb
```

**Commandes et résultats :**

| Étape | Commande | Zone testée | Résultat |
|---|---|---|---|
| Désactiver le cache | `dcache off` | | `Data (writethrough) Cache is OFF` |
| Remplir et relire | `mw.l 0x20000000 0x00000000 0x100000` puis `md.l 0x20000000 0x100` | début de la zone basse (4 Mo écrits, 1 Ko affiché) | Tout à `00000000`, aucune différence |
| Test zone basse | `mtest 0x20000000 0x24000000` | 64 Mo à partir de `0x20000000` | Les 4 motifs passent (`00000000`, `FFFFFFFF`, `00000001`, `FFFFFFFE`), pas d'erreur affichée |
| Test zone haute | `mtest 0x60000000 0x64000000` | 64 Mo à partir de `0x60000000` | Idem, pas d'erreur affichée |
| Réactiver le cache | `dcache on` | | `Cache: Enabled` |
| Test étendu 1 | `mtest 0x20000000 0x40000000` | 512 Mo | Idem, pas d'erreur affichée |
| Test étendu 2 | `mtest 0x40000000 0x7F000000` | environ 1 Gio | Idem, pas d'erreur affichée |
| Test de couplage | `mtest2 cf 0x20000000 0x2000000 3` | 32 Mo, 3 passes | `Tested 3 iteration(s) with 0 errors.` |
| Test de motifs | `mtest2 saf 0x20000000 0x4000000 3` | 64 Mo, 3 passes, motifs `FFFFFFFF` et `00000000` montants et descendants | `Tested 3 iteration(s) with 0 errors.` |

Remarques sur les commandes :

- Pour `mtest2`, le deuxième paramètre est interprété comme une **taille**, pas comme une adresse de fin (l'affichage indique par exemple `end 0x23ffffff` pour une taille de `0x4000000`). Une première tentative avec 5 paramètres n'a affiché que l'aide.
- `mtest` n'affiche **pas** de compteur d'erreurs : l'absence de message est le signal. Seul `mtest2` écrit `0 errors`.
- Le test des motifs `FFFFFFFE` et `00000001` vérifie un fil de données à la fois, ce qui convient à la recherche d'un bit bloqué comme le bit 23.

**Interprétation :** aucun de ces tests n'a montré d'erreur de mémoire. Ça confirme que, **au moment du test**, la mémoire se comportait correctement, y compris sur le fil de données du bit 23. Mais **ce n'est pas une preuve de stabilité durable** : le défaut observé avant la réparation était intermittent (il dépendait de la pression sur U3 et sans doute de la chaleur), et un test court en U-Boot peut le manquer. Seuls les démarrages à froid répétés et les longues sessions d'installation sans plantage ([tests de stabilité](11-tests-de-stabilite.md)) apportent cette preuve.

[INSÉRER PHOTO : capture du terminal U-Boot avec `bdinfo` (adresses IP et MAC par défaut à masquer si elles apparaissent)]
[INSÉRER PHOTO : capture du terminal U-Boot avec les résultats `mtest` zones basse et haute]
[INSÉRER PHOTO : capture du terminal U-Boot avec `mtest2 ... 0 errors`]
