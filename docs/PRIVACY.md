# Vie privée : ce qu'il ne faut jamais publier

Un NAS laisse des traces d'identité partout. Avant de publier un fichier, une capture ou une photo, vérifie :

| À masquer / ne pas publier | Où ça apparaît |
|---|---|
| Numéro de série du NAS et des disques | Étiquette, Synology Assistant, journaux, SMART, dumps de la flash |
| Adresse MAC | Étiquette, Synology Assistant, journaux, `ifconfig`, dumps de la flash |
| Adresses IP (internes et publiques) | Captures réseau, `ipconfig`, journaux |
| Nom du serveur et noms d'utilisateurs | Invite `login:`, journaux, captures DSM |
| Adresse e-mail, identifiants QuickConnect | DSM, assistant |
| Chemins de fichiers de ta machine | Captures de l'explorateur, des invites de commande (ils contiennent ton nom d'utilisateur) |
| Marque et modèle de ton routeur, ville, région | Captures réseau, fuseau horaire |
| **Ton identité git** | Le nom et l'e-mail de `git config` se retrouvent dans chaque commit public |

## À ne **jamais** publier

- Les fichiers `.bin` de dump de flash : ils contiennent l'identité d'usine (MAC, numéro de série).
- Les journaux bruts `.log` / `.txt` de PuTTY.
- Les fichiers `.pat` (propriété de Synology).

Le `.gitignore` de ce dépôt bloque ces extensions.

## Identité git

Avant le premier commit, configure une identité qui ne révèle ni ton vrai nom ni ton e-mail, par exemple l'adresse « noreply » fournie par GitHub (GitHub > Settings > Emails > « Keep my email addresses private ») :

```sh
git config user.name  "ton-pseudo"
git config user.email "<id>+<pseudo>@users.noreply.github.com"
```

Vérifie avec `git log --format='%an <%ae>'` avant de pousser. Un commit déjà poussé garde son auteur : le changer oblige à réécrire l'historique.

## Photos et captures

1. Floute **avant** d'enregistrer le fichier final (un flou superposé par un éditeur qui conserve les calques n'est pas sûr : exporte en image aplatie).
2. Pour une étiquette de NAS : ne publie pas la photo, ou masque totalement la zone.
3. Rouvre l'image exportée et vérifie que rien n'est lisible, y compris en zoomant.

## Vérification automatique avant publication

Depuis la racine du dépôt (adapte les motifs à ton cas : ton nom, ton nom de serveur, tes adresses) :

```sh
grep -rniE "[0-9A-F]{2}(:[0-9A-F]{2}){5}|192\.168\.|169\.254\.|@[a-z0-9.-]+\.[a-z]{2,}" . --include="*.md" --include="*.py" --include="*.sh"
grep -rniE "ton_nom|ton_serveur|ton_utilisateur" . 
```

Les adresses IP et MAC doivent apparaître seulement sous forme de modèles (`<IP_NAS>`, `<MAC>`, `169.254.x.x`).
