# Réinstallation de DSM et vérifications

## Choix de la version à installer (important)

> **Pour la première installation, installe la version que Synology Assistant affiche pour le NAS.**
>
> En mode junior, Synology Assistant indique une version dans la colonne « Version » (ici **6.2.4-25556**). Le NAS attend cette version : c'est celle qui correspond au système de fichiers initial déjà présent dans la flash. J'ai donc téléchargé le fichier `.pat` de **cette même version** pour ce modèle (`DSM_DS218_25556.pat`), et l'installation est allée jusqu'au bout.

Précisions pour ne pas surestimer cette règle :

- Il s'agit d'une **pratique observée** : avec la version affichée par Synology Assistant, l'installation a réussi. Je n'ai **pas testé** d'autre version, donc je ne peux pas affirmer qu'une autre version échoue.
- Le blocage initial n'avait **pas** pour cause une mauvaise version : c'était la table de partitions vide ([cause racine](06-cause-racine.md)). Choisir la bonne version ne suffit pas à lui seul.
- Le fichier doit correspondre exactement au **modèle** (DS218 ici, pas DS218+ ni DS218j).
- Après l'installation, le NAS peut proposer des mises à jour (même branche, puis DSM 7). Elles se font **après** la première installation, pas pendant.

**Procédure :**

1. Dans PuTTY, lance `tail -f /var/log/messages` avant l'installation et laisse-le tourner.
2. Dans Synology Assistant, double-clique sur le NAS et choisis **Réinstallation** (pas « Migration »).
3. Sélectionne `DSM_DS218_25556.pat` et laisse l'installation aller jusqu'au bout sans toucher à rien.

## Ce que montre le journal

- L'`updater` ouvre successivement `FIS directory`, `zImage` et `rd.gz`, les écrit, puis le NAS redémarre. L'erreur `find mtd partition [RedBoot] by name fail` a disparu.
- Après le redémarrage, le noyau est le bon :

```text
Linux version 4.4.59+ ... #25556 SMP Tue May  2 17:14:51 CST 2023
5 RedBoot partitions found on MTD device RtkSFC
```

- Plus aucune erreur `version magic`, plus de message `init not health`. Les modules USB, réseau et `synobios` se chargent.
- La console arrive sur l'invite de connexion DSM environ 50 secondes après la mise sous tension.

## Vérification de l'identité

Synology Assistant affiche maintenant le numéro de série et l'adresse MAC d'origine (`<SN>` et `<MAC>`), identiques à l'étiquette du NAS. Ils étaient auparavant vides ou aléatoires. Cela confirme que la partition `vendor` est désormais lisible et que l'identité d'usine n'a jamais été perdue.

[INSÉRER PHOTO : capture de Synology Assistant après réparation, avec le numéro de série et la MAC affichés (à masquer avant publication)]
[INSÉRER PHOTO : étiquette du NAS (à masquer entièrement avant publication)]
[INSÉRER PHOTO : page de configuration DSM, premier écran]

## La page d'installation : l'objectif final

C'est ici que le chemin de ce dépôt s'arrête : arriver à l'assistant d'installation de DSM, puis le terminer. Voici à quoi ressemble chaque écran et quoi vérifier.

### 1. Dans Synology Assistant

Avant la réparation, le NAS apparaît avec le statut **« Pouvant être migré »** mais l'installation échoue. Après la réparation de la table FIS :

1. Le NAS apparaît toujours en **« Pouvant être migré »** (c'est normal : un système est détecté sans être complet). Double-clique dessus.
2. L'assistant web propose **Migration** ou **Réinstallation**. Choisis **Réinstallation** (les disques sont vides ou sans importance).
3. Indique le fichier `.pat` de la bonne version (voir plus haut).
4. L'installation écrit le système, le NAS redémarre. Compte quelques minutes.

[INSÉRER PHOTO : Synology Assistant, NAS « Pouvant être migré » (masquer IP, MAC, numéro de série)]
[INSÉRER PHOTO : choix « Réinstallation » dans l'assistant web]
[INSÉRER PHOTO : barre de progression de l'installation]

### 2. L'assistant de configuration de DSM

Après le redémarrage, Synology Assistant affiche le NAS en **« Prêt »** ou **« Non configuré »**. Double-clique : l'assistant de configuration demande :

| Écran | Que renseigner |
|---|---|
| Nom du serveur | Un nom de ton choix (ne le publie pas) |
| Compte administrateur | Un nom d'utilisateur et un mot de passe **forts**, que tu es seul à connaître |
| Mises à jour de DSM | « Installer automatiquement uniquement les mises à jour importantes » ou notification seule. À toi de voir |
| QuickConnect | Facultatif, tu peux l'ignorer |
| Analyse / statistiques | Facultatif |

Termine, et tu arrives sur le **bureau de DSM**. Le NAS est réparé.

[INSÉRER PHOTO : écran « Bienvenue » de l'assistant de configuration DSM]
[INSÉRER PHOTO : bureau DSM (masquer le nom du serveur et l'adresse)]

### 3. Critères de réussite

Coche chacun de ces points :

- [ ] Plus aucune erreur `find mtd partition [RedBoot] by name fail` dans `/var/log/messages` pendant l'installation.
- [ ] Après redémarrage, `Linux version 4.4.59+ ... #25556` (ou la version installée) et `5 RedBoot partitions found`.
- [ ] La console arrive jusqu'à `login:`.
- [ ] Synology Assistant affiche le numéro de série et l'adresse MAC.
- [ ] L'assistant de configuration de DSM s'ouvre dans le navigateur.
- [ ] Un redémarrage à froid (arrêt complet, débranchement quelques secondes, rallumage) fonctionne **plusieurs fois de suite**.

Si un point échoue : [dépannage](14-depannage-faq.md).
