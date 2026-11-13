# Cause racine : la table de partitions de la flash est vide

Le noyau Linux du DS218 cherche une table de partitions de type **RedBoot** (un bloc appelé « FIS directory ») à l'offset `0x7ff000` de la flash SPI. Cette table dit au noyau où se trouvent `zImage`, `rd.gz` et `vendor`.

Dans le cas étudié, ce bloc ne contenait que des octets `0xFF` (flash effacée). Conséquences :

1. Le noyau n'expose qu'une seule partition `RtkSFC` couvrant les 8 Mo.
2. L'outil `updater` de Synology cherche des partitions **par leur nom** (`RedBoot`, `zImage`, `rd.gz`, `vendor`). Il ne trouve rien, donc il ne peut pas écrire le nouveau système.
3. Il nettoie ce qui a été décompressé et redémarre, ce qui laisse le NAS en mode junior.
4. La partition `vendor` (qui contient l'adresse MAC et le numéro de série d'usine) n'est pas visible non plus, d'où les valeurs vides ou aléatoires.

Les autres zones de la flash étaient intactes (bootloader, noyau, ramdisk, données d'usine). Seul ce secteur de 4 Ko manquait.

## Ce qui a été écarté

| Hypothèse | Pourquoi elle a été écartée |
|---|---|
| Mauvaise date sur le NAS | L'horloge garde le temps et l'installateur la resynchronise |
| Choix « Migration » ou « Réinstallation » | Même résultat dans les deux cas |
| Mauvaise version de DSM | Le fichier `.pat` passe la vérification de signature et de somme de contrôle |
| Erreur de RAM pendant l'envoi du fichier | La somme de contrôle du `.pat` était correcte |
| Perte d'identité (MAC, numéro de série) | Les données d'origine étaient présentes dans la flash |
