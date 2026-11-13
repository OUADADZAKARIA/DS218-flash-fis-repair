# Ce qui reste incertain

| Point | État |
|---|---|
| **Comment la table de partitions a été perdue** | **Inconnu.** Hypothèse non confirmée : une écriture interrompue de l'`updater` pendant des essais avec une carte instable |
| **Quelle intervention matérielle a stabilisé la carte** | Inconnu : la refusion répétée des 4 puces de RAM, l'élément métallique de refroidissement et de pression sur U3, le ventilateur ou une combinaison. Elle n'a pas été isolée |
| **Références de la carte et des puces de RAM** | À vérifier : elles avaient été relevées sur des photos qui ne montraient pas un DS218 |
| **Tests de RAM en U-Boot** | Aucune erreur détectée ([tests de la RAM](04-intervention-materielle.md#tests-de-la-ram-zones-basse-et-haute)), mais ils n'ont pas reproduit le défaut intermittent d'origine. Ils ne prouvent donc pas à eux seuls la stabilité |
| **Stabilité matérielle sur la durée** | Partielle : 3 démarrages à froid et plusieurs dizaines de minutes sans plantage. Un test de plusieurs heures reste à faire |
| **Mises à jour DSM** | Une mise à jour réécrit `zImage` et `rd.gz` dans la flash : à faire seulement sur une carte reconnue stable, avec une sauvegarde de la flash prise depuis le système fonctionnel |
| **Dernière version de DSM 7.x supportée par le DS218** | Non vérifiée dans ce dépannage |
