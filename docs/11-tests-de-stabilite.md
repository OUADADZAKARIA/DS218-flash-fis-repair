# Tests de stabilité

| Test | Résultat |
|---|---|
| Redémarrage logiciel depuis DSM (« Redémarrer ») | Réussi. Retour sur l'invite de connexion, services démarrés |
| Démarrage à froid (arrêt DSM, alimentation débranchée environ 10 s) | **3 réussites sur 3**, invite de connexion à environ 50 s, aucune erreur critique |
| Messages à ignorer dans les journaux | `read_env from factory failed`, `hub doesn't have any ports`, redémarrage de `iscsi_pluginserverd` (sans cible iSCSI configurée) |
| Absence de défauts | Aucun `ROM fail`, `panic`, `oops`, erreur de disque ou de mémoire dans les journaux de démarrage à froid |
| Charge | Création d'un volume Btrfs de 3,49 To, vérification en arrière-plan en cours, CPU environ 10 %, RAM environ 13 % |
| Disque de test (WD 4 To) | État « Sain », 0 secteur défectueux, environ 35 °C, test S.M.A.R.T. rapide « Sain » |
| Test S.M.A.R.T. étendu | Lancé, puis interrompu (pas de résultat enregistré). À relancer |

> Le test de stabilité prolongé (plusieurs heures) n'est pas terminé au moment de la rédaction. Voir [incertitudes](12-incertitudes.md).

[INSÉRER PHOTO : journal de démarrage à froid avec l'invite de connexion (masquer le nom du serveur)]
[INSÉRER PHOTO : Gestionnaire de stockage avec le volume créé et la vérification en cours]
[INSÉRER PHOTO : informations de santé du disque (masquer le numéro de série du disque)]
