# Dépannage et FAQ

Tableau rapide : **symptôme → cause probable → action**. Les causes sont celles observées sur ce DS218 ; sur un autre cas elles restent des hypothèses.

## Installation et mode junior

| Symptôme | Cause probable | Action |
|---|---|---|
| NAS « Pouvant être migré » en boucle, l'installation échoue | Table FIS vide, ou version de `.pat` inadaptée | Lis le journal (`tail -f /var/log/messages`). Si `find mtd partition [RedBoot] by name fail` → [reconstruction](08-procedure-reconstruction-fis.md) |
| `version magic '4.4.59+' should be '4.4.302+'` | Noyau et modules de versions différentes (installation incomplète) | Refaire une **Réinstallation** avec le `.pat` de la version affichée par Synology Assistant ([réinstallation](09-reinstallation-dsm.md)) |
| `init not health` | L'installation s'est arrêtée sur une erreur | Cherche la vraie erreur quelques lignes plus haut dans le journal |
| Quelle version de `.pat` prendre ? | | Celle que Synology Assistant affiche pour le NAS, pour le **modèle exact**. Pratique observée, non prouvée comme règle |
| Un autre modèle que le DS218 ? | | Non testé. Les offsets et tailles sont propres à ce modèle : ne les réutilise pas sans relever tes propres valeurs ([carte de la flash](07-carte-de-la-flash.md)) |

## Réseau et heure

| Symptôme | Cause probable | Action |
|---|---|---|
| Adresse `169.254.x.x` | Pas de serveur DHCP (NAS branché directement au PC) | Brancher le NAS sur le routeur |
| Pas d'Internet, pas de mise à jour | Pas de passerelle (même cause) | Idem |
| Horloge en 2016 | Pas de NTP | Réseau puis synchronisation NTP ([après l'installation](10-apres-installation.md)) |
| Heure décalée d'une heure certains mois | Fuseau sans heure d'été | Choisir le fuseau de la région qui la gère |
| `change directory failed` sur la console | Pas de volume, donc pas de dossier personnel | Normal, créer le volume |

## Flash et sauvegarde

| Symptôme | Cause probable | Action |
|---|---|---|
| `dd` de `/dev/mtd0ro` donne 1 048 576 octets | Après la réparation, `mtd0ro` est seulement la partition `RedBoot` | Copier `mtd0` à `mtd4` et les concaténer ([après l'installation](10-apres-installation.md)) |
| Le bloc FIS relu est différent de celui écrit | Écriture non terminée | Refaire `sync`, relire, comparer avec `build_fis.py --verify` |
| `check_flash_dump.py` dit « une table existe déjà » | Le NAS a déjà une table (ex. après réparation) | La procédure de reconstruction ne s'applique plus |

## Démarrage et matériel

| Symptôme | Cause probable | Action |
|---|---|---|
| Boucle `verify fsbl fail` | Démarrage instable. Observé avec une RAM défaillante | [intervention matérielle](04-intervention-materielle.md) |
| Plantages différents à chaque démarrage (`Oops`, `kernel BUG`, `skb_over_panic`) | Mémoire instable | Idem, puis [tests de stabilité](11-tests-de-stabilite.md) |
| Démarrage correct seulement en appuyant sur la puce U3 | Contact défectueux (soudure ou refroidissement) | Idem |
| Voyant d'alimentation clignotant, autres voyants éteints | Le démarrage ne va pas jusqu'au bout | Brancher la console série et lire le journal ([console série](02-console-serie-et-mode-junior.md)) |
| Tests de RAM U-Boot sans erreur mais instabilité | Défaut intermittent : un test sans erreur ne prouve pas la stabilité | Multiplier les démarrages à froid |

## Questions fréquentes

**La plaque métallique grise est-elle obligatoire ?** Je n'ai pas de preuve qu'elle le soit. Dans mon cas elle a un rôle de dissipation et d'appui sur la puce U3, mais je ne sais pas si elle est d'origine ou ajoutée. Sur ce point, voir [incertitudes](12-incertitudes.md). Une plaque qui touche un composant sans isolation peut en revanche créer un court-circuit : vérifie ce qu'elle touche.

**Faut-il aussi une console série pour réparer ?** Pour lire les journaux et accéder au shell du mode junior, oui : c'est ce qui permet d'écrire dans la flash.

**Mes données sont-elles en danger ?** Cette procédure n'écrit que dans la flash (4 Ko). Elle ne touche pas aux disques. Cela dit, les installations de DSM, elles, peuvent formater les disques : **sauvegarde avant**.

**Puis-je publier mes journaux pour demander de l'aide ?** Non, pas tels quels : voir [vie privée](PRIVACY.md).
