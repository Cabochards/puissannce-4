# Projet de Puissannce 4 en IN200N
Groupe de TD : S2BITD02

Membres du projet : Kier De Castro, Paul Junior Bessong, Maël Fajon

# Principe du Puissance 4
**Le Puissance 4** est un jeu à ***deux joueurs***. Durant une partie, à tour de rôle,
chaque joueur choisit une colonne d’une grille dans laquelle il dépose un jeton
de sa couleur. Ce jeton tombe alors jusqu'à rencontrer un obstacle qui peut être
soit le fond de la grille soit un autre jeton déjà déposé dans la même colonne.
Le gagnant est le premier joueur à aligner ***quatre jetons de sa couleur*** en ligne,
en colonne ou en diagonale.

Ici, Le joueur qui débute la partie est choisi au hasard.

Si la grille est pleine et qu’il n’y a pas de vainqueur, alors la manche est
déclarée nulle.

# Prérequis
Afin d'être sûr que le script fonctionne correctement, veuillez vérifier que vous ayez bien les modules suivants d'installés : ***tkinter, os, random***

# Utilisation
Ouvrez le fichier main.py
> Tout le code est dans ce fichier.

Pour lancer le programme, clickez sur **Exécuter** depuis votre interpréteur. Une fenêtre devrait alors aparaître, vous permettant de choisir la taille de votre grille de Puissance 4, lancer une nouvelle partie, ou bien charger une partie précédente.

Lorsque vous êtes en jeu *(après avoir sélectionné **Nouvelle partie** ou **Charger une partie**)*, vous pourrez cliquer sur un Canevas pour placer des pions.

Le bouton **Annuler** vous permettra d'annuler des coups déjà joués.
> ***attention, lorsqu'une partie sauvegardée est chargée, vous ne pourrez pas annuler les coups déjà joués !***

**Sauvegarder/Quitter** vous permettra de sauvegarder votre partie, ainsi que de revenir au menu principal, de sélection de partie.

> Lorsque vous sauvegarderez, un fichier nommé puissance_4_save.txt sera créé. Il s'agit là de votre sauvegarde. A chaque fois que vous sauvegardez, son contenu est remplacé par celui de la dernière partie. Vous pouvez le supprimer si vous ne voulez pas garder la sauvegarde. Ne pas avoir de fichier de sauvegarde déjà existant fera que le bouton **Charger une partie** lancera une nouvelle partie.

Si un joueur gagne une partie ou qu'il y a match nul, vous aurez directement la possibilité de recommencer une partie avec la même grille (elle sera de même taille que la précédente, mais vide).

Pour fermer la fenêtre et quitter le jeu, cliquez sur la croix en haut à droite de la fenêtre.
![image](https://user-images.githubusercontent.com/90553363/234916328-9c2e334d-584b-43cc-890a-108c1af6eca3.png)
![image](https://user-images.githubusercontent.com/90553363/234916433-cd08c54f-2b27-4935-b3ac-7900c25e87f2.png)


