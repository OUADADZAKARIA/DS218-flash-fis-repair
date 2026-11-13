# Avertissements (à lire en premier)

- **Écrire dans la flash d'un NAS peut le rendre inutilisable** (« brique »). Cette procédure a été appliquée sur un seul appareil, dans un contexte précis (table de partitions entièrement vide, dumps vérifiés). Elle n'est pas garantie sur un autre.
- **Ne l'applique que si tu as constaté le même symptôme** : table vide à `0x7ff000` et erreur `find mtd partition [RedBoot] by name fail`. Si ta table n'est pas vide, ne l'écrase pas.
- **Les valeurs des offsets viennent d'une analyse du dump de ce DS218** et d'une comparaison avec un DS418. Contrôle-les sur ta propre sauvegarde avant d'écrire quoi que ce soit.
- **Sauvegarde toujours la flash en deux copies identiques** avant de commencer.
- **Ne partage jamais tes dumps de flash tels quels** : ils contiennent l'adresse MAC, le numéro de série et d'autres données d'usine.
- Ce document est fourni tel quel, sans garantie. Il n'est ni affilié ni approuvé par Synology.
- Le contenu de ce dépôt ne remplace pas le support officiel. Pour un NAS sous garantie, contacte d'abord Synology.
