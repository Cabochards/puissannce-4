from os.path import isfile, realpath, dirname
from random import randint
# from pygame import mixer
from os import getcwd
import tkinter as tk


mon_chemin = realpath(__file__)                     # Permet de savoir le chemin du script dans l'ordinateur
mon_chemin = dirname(mon_chemin)                    # Permet de savoir dans quel dossier nous sommes (pour la sauvegarde)

# mixer.init()
# pion_sound = mixer.Sound(mon_chemin + "\super-mario-64-thwomp-sound-online-audio-converter.mp3")

fenetre = tk.Tk()
fenetre.title("Puissance 4")

size = 50
tour = randint(0,1)                                 # Choisit aléatoirement quel joueur va jouer en premier
pion = 1
last_moves = []
colors=["red","yellow","dark blue","blue","white"]
Gpuissance4 = []


## savefile
def recuperer(file_name):
    """
    Cette fonction permet de récupérer le contenu d'un fichier texte.
    Elle prend en argument le nom d'un fichier (par exemple : 'test.txt'),
    et renvoie le texte contenu dans ce fichier, si le fichier existe, ou renvoie -1 dans le cas contraire.
    """
    if isfile(file_name):                           # Si le fichier existe,
        file = open(file_name,'r')                  # Ouvre le fichier
        lines = file.readlines()                    # Puis lit le fichier
        file.close()                                # Avant de le refermer
        return lines
    return -1

def modifier(file_name,text='',ligne=None):
    """
    Cette fonction permet de modifier le contenu d'un fichier txt.
    Elle prend en arguments :
        - un nom de fichier (exemple : 'test.txt'),
        - une chaîne de caractères ("" si elle n'est pas mentionnée),
        - ainsi qu'une ligne précise (un entier si elle est mentionnée, None sinon).

    Si le fichier existe, la fonction va lire son contenu.
    Si ligne = None, alors le texte sera ajouté à la fin du fichier. Sinon, le texte sera ajouté à la ligne spécifiée.
    """
    lines = recuperer(file_name)                    # Récupère le contenu du fichier
    if lines == -1:                                 # Si le fichier n'existe pas, on crée une liste vide, qui contiendra notre nouveau texte
        lines = []

    if ligne is None or ligne >= len(lines):        # Si ligne est vide ou plus grand que le nombre de lignes du fichier,
        lines.append(text)                          # On ajoute le texte à la fin
    else:
        lines[ligne] = text                         # Sinon, on l'ajoute à la ligne mentionnée

    file = open(file_name, 'w')                     # Ecrit le nouveau texte dans le fichier
    file.writelines(lines)
    file.close()


def transform_to_tab(file_name):
    """
    Cette fonction permet de transformer le texte d'un fichier txt en tableau.
    Elle prend en argument le nom d'un fichier (par exemple : 'test.txt'), et renvoie une liste de listes.
    """
    tab = []
    text = recuperer(file_name)                             # Récupère le contenu du fichier
    if text == -1:                                          # Si le fichier n'existe pas,
        for i in range(scale_x.get()):
            tab.append([0 for j in range(scale_y.get())])   # On crée un nouveau tableau rempli de 0
    else:
        for row in text:
            stripped = row.strip()                          # Retire les retours à la ligne ('\n')
            splitted = stripped.split()                     # Retire les espaces et transforme le texte en liste
            for case in range(len(splitted)):
                splitted[case] = int(splitted[case],2)      # Convertit les valeurs en entiers
            tab.append(splitted)
    return tab

def transform_to_string(tab):
    """
    Cette fonction transforme un tableau en texte binaire.
    Elle prend en argument une liste de liste, et renvoie une chaîne de caractères.
    """
    text = ''
    for i in range(len(tab)):                       # Parcourt les lignes
        for j in range(len(tab[i])):                # Parcourt les colonnes
            text += bin(tab[i][j])                  # Convertit les pions en binaire
            if j != len(tab[i])-1:                  # Tant qu'on n'est pas à la dernière colonne,
                text += ' '                         # On met un espace
        text += '\n'                                # Une fois à la fin de la ligne, on fait un retour à la ligne
    return text



## grille
def creer_grille(x,y):
    """
    Cette fonction permet de créer une grille de taille x*y.
    Elle prend en arguments deux entiers, x et y, et renvoie un tableau de x lignes et y colonnes.
    """
    grille = []
    for i in range(x):                              # Pour chaque ligne,
        grille += [[0 for j in range(y)]]           # Crée une ligne contenant y 0
    return grille

def afficher_grille(grille):
    """
    Cette fonction permet d'afficher un tableau dans la console python.
    """
    for row in grille:
        print (row)

def remplacer_pion(grille,x,y,pion):
    """
    Cette fonction permet de placer un pion dans la case xy.
    Elle prend en arguments une liste de listes (grille), deux entiers x et y, et une valeur (pion),
    et modifie la valeur présente dans grille[x][y] par pion.
    """
    grille[x][y] = pion

def placer_pion(grille,x,pion):
    """
    Cette fonction permet de placer un pion dans la ligne x.
    Elle prend en arguments une liste de listes (grille), un entier x, et une valeur (pion),
    et remplace la première occurence d'un 0 dans la ligne grille[x] par pion.
    S'il n'y a aucun 0, la fonction renvoie -1.
    """
    for y in range(len(grille[x])):                 # Parcourt la ligne x
        if grille[x][y] == 0:                       # Si la valeur présente dans la colonne y est un 0,
            remplacer_pion(grille, x, y, pion)      # On la remplace par pion
            return y                                # Et on renvoie la colonne y
    return -1                                       # S'il n'y a aucun 0, on renvoie -1

## Verifier pions ; cette fonction a été recherchée sur internet, puis légèrement modifiée pour correspondre à ce que l'on désirait.
def verifier_4(grille,pion):
    """
    Cette fonction vérifie si 4 pions sont alignés horizontalement,
    verticalement ou diagonalement dans une grille.
    Elle prend en arguments une liste de listes (grille), ainsi qu'un entier (pion),
    et renvoie True si 4 pions sont alignés, et False sinon.
    """
    for i in range(len(grille)):                   # Pour chaque ligne:
        for j in range(len(grille[i])-3):          # Pour chaque colonne: (attention, on met -3 pour ne pas sortir de la grille)
            if grille[i][j] == pion and grille[i][j+1] == pion and grille[i][j+2] == pion and grille[i][j+3] == pion:
               return True                          # 4 pions sont alignés

    for i in range(len(grille)-3):                  # Pour chaque ligne: (attention, on met -3 pour ne pas sortir de la grille)
        for j in range(len(grille[i])):             # Pour chaque colonne:
            if grille[i][j] == pion and grille[i+1][j] == pion and grille[i+2][j] == pion and grille[i+3][j] == pion:
                return True                         # 4 pions sont alignés

    for i in range(len(grille)-3):                  # Pour chaque ligne: (attention, on met -3 pour ne pas sortir de la grille)
        for j in range(len(grille[i])-3):           # Pour chaque colonne: (attention, on met -3 pour ne pas sortir de la grille)
            if grille[i][j] == pion and grille[i+1][j+1] == pion and grille[i+2][j+2] == pion and grille[i+3][j+3] == pion:
                return True                         # 4 pions sont alignés

    for i in range(len(grille)-3):                  # Pour chaque ligne: (attention, on met -3 pour ne pas sortir de la grille)
        for j in range(3,len(grille[i])):           # Pour chaque colonne: (attention, on met 3 pour ne pas sortir de la grille (on va de droite à gauche ici))
            if grille[i][j] == pion and grille[i+1][j-1] == pion and grille[i+2][j-2] == pion and grille[i+3][j-3] == pion:
                return True                         # 4 pions sont alignés

    return False


def Verifier_match_nul(grille):
    """
    Cette fonction vérifie si toutes les cases sont pleines.
    Elle prend en arguments une liste de listes (grille),
    et renvoie True la grille ne contient plus aucun 0, et False sinon.
    """
    nul = True
    for ligne in grille:
        nul = nul and all(ligne)
    return nul


## tkinter
def creer_canvas(grille,size):
    """
    Cette fonction crée un canevas et y dessine un jeu de Puissance 4.
    Elle prend en arguments une liste de liste (grille), ainsi qu'un entier (size),
    qui correspond au nombre de pixels d'une case,
    et renvoie un canevas Tkinter de la taille de la grille * size avec des cases comme un vrai Puissance 4.
    """
    canvas = tk.Canvas(fenetre,width=len(grille)*size,height=len(grille[0])*size,bg=colors[3])          # Crée le canevas
    for i in range(len(grille)+1):                                                                      # Pour chaque ligne:
        for j in range(len(grille[0])+1):                                                               # Pour chaque colonne:
            canvas.create_rectangle(i*size,j*size,i*size+size,j*size+size,outline=colors[2],width=4)    # Dessine des lignes pour faire des cases
            
            X = i*size                                                                                  # Taille horizontale d'un cercle
            Y = (len(grille[0])-j)*size                                                                 # Taille verticale d'un cercle
            canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[2])                                # Dessine des cercles pour faire les trous pour les pions
    return canvas

def Placer(event):
    """
    Cette fonction permet de placer un pion dans le tableau Gpuissance4 et sur le canevas.
    A chaque appel, elle vérifie quel pion doit jouer puis si un pion peut être placé à l'endroit cliqué.
    Si le pion peut être placé, elle place le pion dans Gpuissance4,
    garde le coup joué en mémoire dans last_moves (pour l'annuler),
    et modifie la variable tour que le joueur suivant joue.
    """
    global Gpuissance4
    global tour
    global pion
    global last_moves

    x = event.x//size                               # Récupère la colonne

    if tour%2==0:                                   # Choisit quel joueur va jouer
        pion = 2                                    # en fonction du tour
    else:
        pion = 1

    if -1 < x < len(Gpuissance4):                   # Si on ne dépasse pas du tableau, on joue
        y = placer_pion(Gpuissance4, x, pion)       # On place un pion et on récupère où il a été placé
        if y != -1:                                 # S'il a pu être placé,
            # pion_sound.play()                      # On joue un son
            last_moves.append((x,y))                # On ajoute le coup dans les coups joués
            bouton_annuler["state"] = "normal"      # Et le joueur pourra annuler son coup au prochain tour

            X = x*size                                                          # Taille horizontale d'un cercle
            Y = (len(Gpuissance4[0])-y)*size                                    # Taille verticale d'un cercle
            canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[tour%2])   # Dessine un cercle

            if verifier_4(Gpuissance4, pion):       # Si le joueur a aligné 4 pions de sa couleur,
                Gagner(tour%2)                      # Le joueur a gagné
            
            elif Verifier_match_nul(Gpuissance4):   # Si aucun joueur n'a gagné,
                Gagner()                            # Match nul

            tour += 1                               # On passe au tour du joueur adverse

def Annuler():
    """
    Cette fonction permet d'annuler le placement d'un pion dans le tableau Gpuissance4 et sur le canevas.
    A chaque appel, elle vérifie s'il y a un coup à annuler.
    Si le pion peut être supprimé, elle remplace le pion dans Gpuissance4 par un 0,
    retire le coup joué en mémoire dans last_move,
    et modifie la variable tour que le joueur suivant joue.
    """
    global Gpuissance4
    global tour
    global last_moves

    if any(last_moves):                             # S'il y a un coup à annuler,
        x,y = last_moves.pop()                      # On récupère où
        remplacer_pion(Gpuissance4, x, y, 0)        # On met un 0 à la position xy

        X = x*size                                                      # Taille horizontale d'un cercle
        Y = (len(Gpuissance4[0])-y)*size                                # Taille verticale d'un cercle
        canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[2])    # Dessine un cercle bleu pour cacher celui du joueur
        
        tour -= 1                                   # Redonne la main au dernier joueur

        if not any(last_moves):
            bouton_annuler["state"] = "disabled"    # S'il n'y a aucun coup à annuler, on ne peut plus annuler

def lancer_partie(choix):
    """
    Cette fonction permet de lancer une partie.
    Elle prend en argument une chaîne de caractères (choix), et lance une partie en fonction de choix.
    Si choix = "charger", la fonction va charger une partie déjà sauvegardée (si aucune partie n'a été chargée, une nouvelle partie sera créée).
    Si choix = "standard", la fonction créera un nouveau tableau et lancera une nouvelle partie.
    Si choix = "retry", la fonction recréera un tableau de la même taille que le précédent.
    """
    global canvas
    global Gpuissance4
    if choix == "charger":                                      # Si le joueur veut charger une partie,
        Gpuissance4 = transform_to_tab(mon_chemin + '\Puissance_4_save.txt')  # On charge une partie
        canvas = creer_canvas(Gpuissance4, size)                # On crée un canevas correspondant au tableau Gpuissance4
        
        for i in range(len(Gpuissance4)):           # Pour chaque ligne:
            for j in range(len(Gpuissance4[0])):    # Pour chaque colonne:
                if Gpuissance4[i][j] != 0:          # Si une des cases n'est pas vide (s'il y a un pion), on dessine un pion

                    X = i*size                                                                      # Taille horizontale d'un cercle
                    Y = (len(Gpuissance4[0])-j)*size                                                # Taille verticale d'un cercle
                    canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[Gpuissance4[i][j]%2])  # Dessine un cercle représentant un pion
        
    elif choix == "standard":                       # Si le joueur veut créer une nouvelle partie,
        x,y = scale_x.get(),scale_y.get()           # On récupère la taille du futur tableau
        Gpuissance4 = creer_grille(x,y)             # On crée un nouveau tableau
        canvas = creer_canvas(Gpuissance4, size)    # On crée un canevas correspondant à ce tableau
    
    elif choix == "retry":                                                  # Si le joueur veut réessayer,
        Gpuissance4 = creer_grille(len(Gpuissance4), len(Gpuissance4[0]))   # On crée un nouveau tableau de la même taille que le précédent
        canvas = creer_canvas(Gpuissance4, size)                            # On crée un canevas correspondant à ce tableau
    
    Jouer()                                         # On lance la partie dans tous les cas


## menus/fenetres
def Menu():
    """Cette fonction permet d'afficher le menu (l'écran titre et de sélection),
    tout en masquant ce qui ne devrait pas être affiché sur le menu.
    """

    # Les grid() affichent les widgets, et les grid_remove() les masquent

    label_choix.grid()
    bouton_charger.grid()
    bouton_creer.grid()
    scale_x.grid()
    scale_y.grid()

    canvas.delete("all")
    canvas.grid_remove()
    bouton_annuler.grid_remove()

    bouton_savequit.grid_remove()
    label_quitter.grid_remove()
    save_oui.grid_remove()
    save_non.grid_remove()

    label_gagner.grid_remove()
    retry_oui.grid_remove()
    retry_non.grid_remove()

def Jouer():
    """Cette fonction permet d'afficher le jeu (le canevas de Puissance 4),
    tout en masquant ce qui ne devrait pas être affiché durant la partie.
    """

    # Les grid() affichent les widgets, et les grid_remove() les masquent

    canvas.bind("<Button-1>", Placer)
    canvas.grid(row=2,column=1,rowspan=3,columnspan=3)
    canvas.itemconfig(1, state='normal')
    bouton_annuler["state"] = "disabled"
    bouton_annuler.grid()

    bouton_savequit.grid()

    label_choix.grid_remove()
    bouton_charger.grid_remove()
    bouton_creer.grid_remove()
    scale_x.grid_remove()
    scale_y.grid_remove()

    label_gagner.grid_remove()
    retry_oui.grid_remove()
    retry_non.grid_remove()

def SauvegarderQuitter():
    """Cette fonction permet d'afficher le menu pour sauvegarder et quitter,
    tout en masquant ce qui ne devrait pas être affiché sur ce menu.
    """

    # Les grid() affichent les widgets, et les grid_remove() les masquent

    label_quitter.grid(row=0,column=0,columnspan=2)
    save_oui.grid(row=1,column=0)
    save_non.grid(row=1,column=1)

    scale_x.grid_remove()
    scale_y.grid_remove()

    canvas.delete("all")
    canvas.itemconfig(1, state='hidden')
    canvas.grid_remove()
    bouton_annuler.grid_remove()
    bouton_savequit.grid_remove()

def Gagner(gagnant=None):
    """Cette fonction permet d'afficher l'écran de victoire ainsi que le nom du joueur ayant gagné,
    tout en masquant ce qui ne devrait pas être affiché sur cet écran.
    """
    if gagnant == 1:                                # Si le joueur 1 a gagné, cela affichera jaune
        couleur = "jaune"
    elif gagnant == 0:                              # Si le joueur 2 a gagné, cela affichera jaune
        couleur = "rouge"
    
    if gagnant == None:                             # Si aucun joueur n'a gagné, cela écrira Match nul
        label_gagner['text'] = "Egalité, personne n'a gagné !\n Voulez-vous recommencer la partie ?" # Modifie le message de victoire en fonction du gagnant
    else:
        label_gagner['text'] = f"Le joueur {couleur} a gagné !\n Voulez-vous recommencer la partie ?" # Modifie le message de victoire en fonction du gagnant
    
    # Les grid() affichent les widgets, et les grid_remove() les masquent
    
    label_gagner.grid(row=0,column=0,columnspan=2)
    retry_oui.grid(row=1,column=0)
    retry_non.grid(row=1,column=1)

    canvas.delete("all")
    canvas.itemconfig(1, state='hidden')
    canvas.grid_remove()
    bouton_annuler.grid_remove()
    bouton_savequit.grid_remove()



## widgets
label_quitter = tk.Label(fenetre,text="Voulez-vous sauvegarder avant de quitter ?")
save_oui = tk.Button(fenetre, text="oui",command=lambda:[modifier(mon_chemin + '\Puissance_4_save.txt',transform_to_string(Gpuissance4)),Menu()])
save_non = tk.Button(fenetre, text="non",command=lambda:Menu())

label_choix = tk.Label(fenetre,text="Puissance 4")
bouton_charger = tk.Button(fenetre,text="Charger une partie",command=lambda:lancer_partie("charger"))
bouton_creer = tk.Button(fenetre,text="Nouvelle partie",command=lambda:lancer_partie("standard"))
scale_x = tk.Scale(fenetre,orient="horizontal",label="x",length=80,from_=4,to=10)
scale_y = tk.Scale(fenetre,orient="horizontal",label="y",length=80,from_=4,to=10)
scale_x.set(7)
scale_y.set(6)

canvas = creer_canvas([[0]], 1)

bouton_annuler =tk.Button(fenetre,text="Annuler",bg="black",fg="white",command=Annuler)

bouton_savequit = tk.Button(fenetre,text="Sauvegarder/Quitter",bg="black",fg="white",command=lambda:SauvegarderQuitter())

label_gagner = tk.Label(fenetre,text=f"Le joueur Maël a gagné !\n Voulez-vous recommencer la partie ?")
retry_oui = tk.Button(fenetre, text="oui",command=lambda:lancer_partie("retry"))
retry_non = tk.Button(fenetre, text="non",command=Menu)

## widgets position
label_choix.grid(row=0,column=0,columnspan=2)
bouton_charger.grid(row=1,column=0)
bouton_creer.grid(row=1,column=1)
scale_x.grid(row=0,column=2)
scale_y.grid(row=1,column=2)
bouton_annuler.grid(row=2,column=0)
bouton_savequit.grid(row=0,column=0)



Menu()
fenetre.mainloop()
