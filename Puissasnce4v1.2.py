#importe les modules
from os.path import exists 
import tkinter as tk
import sys


def creer_grille(x,y): 
    '''
    creer une grille de taille variable a partir d'une liste vide
    '''
    grille = []
    for i in range(x): #permet de creer des lignes
        grille += [[0 for j in range(y)]]#permet de creer des colonnes
    return grille

def afficher_grille(grille):
    '''
    affiche la grille (peut etre utiliser pour le debug)
    '''
    for row in grille:
        print (row)

def remplacer_pion(grille,x,y,pion):
    '''
    modifie la valeur d'une case aux coordonnees x y
    '''
    grille[x][y] = pion

def placer_pion(grille,x,pion):
    '''
    permet de savoir si la case est vide est de placer un pion par dessus le
    pion precedent. Si jamais il n'y a plus de place plus aucun pion ne se 
    place
    '''
    for y in range(len(grille[x])):
        if grille[x][y] == 0:
            remplacer_pion(grille, x, y, pion)
            return y
    return -1 


def verifier_4(grille,pion):
    '''
    parcours la grille et verifie si 4 pions a la suite a l'horizontal,vertical
    et diagonal sont les memes
    '''
    
    for i in range(len(grille)): # verification a la vertical
        for j in range(len(grille[i])-3): # comme on verifie 4 pions si jamais on sort de la ligne on fait donc en sorte de ne pas le faire
            if grille[i][j] == pion and grille[i][j+1] == pion and grille[i][j+2] == pion and grille[i][j+3] == pion:
               return True
    
    for i in range(len(grille)-3): # verification a l'horizontal
        for j in range(len(grille[i])):
            if grille[i][j] == pion and grille[i+1][j] == pion and grille[i+2][j] == pion and grille[i+3][j] == pion:
                return True
        
    for i in range(len(grille)-3): # verification en diagonal gauche
        for j in range(len(grille[i])-3):
            if grille[i][j] == pion and grille[i+1][j+1] == pion and grille[i+2][j+2] == pion and grille[i+3][j+3] == pion:
                return True

    for i in range(len(grille)-3): # verification en diagonal droit
        for j in range(3,len(grille[i])):
            if grille[i][j] == pion and grille[i+1][j-1] == pion and grille[i+2][j-2] == pion and grille[i+3][j-3] == pion:
                return True

    return False #si aucun pions sont alignes alors la partie continue

def modifier(file_name,text='',ligne=None):
    """
    Prend en argument le nom de ton fichier un txt et si besoin d'une ligne
    """
    lines = []
    if exists(file_name): # verification de l existtance du fichier
        file = open(file_name,'r') # ouvre le fichier
        lines = file.readlines()  # lecture des lignes
        file.close() # fermeture du fichier
    if ligne == None or ligne >= len(lines): # si lignes vides ou si on depasse ca rajoute le txt a la fin au lieu d un endroit specifique
        lines.append(text) # ajoute le texte a la fin 
    else:
        lines[ligne] = text # met dans le texte dans la ligne specifiee
    file = open(file_name, 'w')
    file.writelines(lines)
    file.close()

def recuperer(file_name):
    """ 
    Lis le fichier 
    """
    file = open(file_name,'r')
    lines = file.readlines()
    file.close()
    return lines

def transform_to_tab(file_name):
    """
    Transforme le fichier texte en tableau
    """
    tab = []
    text = recuperer(file_name)
    for row in text:
        stripped = row.strip() # supprime les retours a la ligne
        splitted = stripped.split() # retire les espaces et transforme en liste
        for case in range(len(splitted)): # retransforme toute les valeurs en entier
            splitted[case] = int(splitted[case])
        tab.append(splitted)
    return tab

def transform_to_string(tab):
    """
    Retransforme le tableau en texte
    """
    text = ''
    for i in range(len(tab)): # parcours le tableau
        for j in range(len(tab[i])):
            text += str(tab[i][j]) # retransforme tout en str
            if j != len(tab[i])-1: # si on est pas la derniere valeur on met des espaces
                text += ' ' 
        text += '\n'#retour a la ligne
    return text
    
#
fenetre = tk.Tk() # creation de la fenetre tk
fenetre.title("Puissance 4") # donne un titre a la fenetre

def creer_canvas(grille,size): # creer un canvas
    canvas = tk.Canvas(fenetre,width=len(grille)*size,height=len(grille[0])*size,bg=colors[3]) # creer un canvas de la taille choisi avec des cases de 50 px
    for i in range(len(grille)+1): # parcours les lignes 
        for j in range(len(grille[0])+1): # parcours les colonnes 
            canvas.create_rectangle(i*size,j*size,i*size+size,j*size+size,outline=colors[2],width=4) #creer la grille
            X = i*size # taille du rond
            Y = (len(grille[0])-j)*size # taille vertical
            canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[2]) # creer un rond dans les cases
    return canvas

def Placer(event):
    """
    Placer un pion dans une case SI il peut etre place
    """
    global G # recupere les variables qui existent dans les autres fonctions
    global tour
    global pion
    global last_move
   
    x = event.x//size # recupere la ligne ou on a clique
    if tour%2==0:  # recupere le tour du joueur permet de dire quel joueur joue
        pion = 2
    else:
        pion = 1

    if -1 < x < len(G): # Verifier si le clique est dans le canvas
        y = placer_pion(G, x, pion) # place un pion
        if y != -1: # verifie si le pion n est pas en dehors
            last_move.append((x,y)) # ajoute dans la liste des coups joues
            X = x*size 
            Y = (len(G[0])-y)*size
            canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[tour%2])# creer un cercle de la couleur correspondante au joueur
            if verifier_4(G, pion): # verifie si victoire
                Menu()
            bouton_annuler["state"] = "normal"
            tour += 1

def Annuler():
    """
    Permet d'annuler un coup jouer
    """
    global last_move
    global tour
    global G
    if any(last_move): # verifier si un coup peut etre annule 
        x,y = last_move.pop() # recupere les coordonees du pion
        remplacer_pion(G, x, y, 0) # remplace par une case vide
        X = x*size
        Y = (len(G[0])-y)*size
        canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[2]) # creer un rond bleu pour cacher 
        tour -= 1
    else:
        bouton_annuler["state"] = "disabled"

def SauvegarderQuitter(G):
    """
    Affiche un menu qui permet de sauvegarder une partie 
    """
    scale_x.grid_remove() # cache tout
    scale_y.grid_remove()

    canvas.delete("all")
    canvas.itemconfig(1, state='hidden')
    canvas.grid_remove()
    bouton_annuler.grid_remove()
    bouton_savequit.grid_remove()

    label_quitter.grid(row=0,column=0,columnspan=2)
    oui.grid(row=1,column=0)
    non.grid(row=1,column=1)

def lancer_partie(choix):
    """
    Soit on lance une partie existante soit nv partie
    """
    global canvas
    global G
    if choix == "charger": #si on charge une partie relance la partie
        G = transform_to_list('Puissance_4_save.txt') # recreation de la grille
        canvas = creer_canvas(G, size)
        for i in range(len(G)):
            for j in range(len(G[0])):
                if G[i][j] != 0:
                    X = i*size
                    Y = (len(G[0])-j)*size
                    canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[G[i][j]%2])
        Jouer() # lance la partie
        
    elif choix == "standard":
        x,y = scale_x.get(),scale_y.get()
        G = creer_grille(x,y)
        canvas = creer_canvas(G, size)
        Jouer()
        

size = 50
tour = 1
pion = 1
last_move = []
colors=["red","yellow","dark blue","blue"]
G = []

label_quitter = tk.Label(fenetre,text="Voulez-vous sauvegarder avant de quitter ?")
oui = tk.Button(fenetre, text="oui",command=lambda:[modifier('Puissance_4_save.txt',transform_to_string(G)),sys.exit()])
non = tk.Button(fenetre, text="non",command=lambda:sys.exit())

label_choix = tk.Label(fenetre,text="Puissance 4")
bouton_charger = tk.Button(fenetre,text="Charger une partie",command=lambda:lancer_partie("charger"))
bouton_creer = tk.Button(fenetre,text="Nouvelle partie",command=lambda:lancer_partie("standard"))
scale_x = tk.Scale(fenetre,orient="horizontal",label="x",length=80,from_=4,to=10)
scale_y = tk.Scale(fenetre,orient="horizontal",label="y",length=80,from_=4,to=10)
scale_x.set(7)
scale_y.set(6)

canvas = creer_canvas([[0]], 1)

bouton_annuler =tk.Button(fenetre,text="Annuler",bg="black",fg="white",command=Annuler)
bouton_savequit = tk.Button(fenetre,text="Sauvegarder/Quitter",bg="black",fg="white",command=lambda:SauvegarderQuitter(G))

label_choix.grid(row=0,column=0,columnspan=2)
bouton_charger.grid(row=1,column=0)
bouton_creer.grid(row=1,column=1)
scale_x.grid(row=0,column=2)
scale_y.grid(row=1,column=2)
bouton_annuler.grid(row=2,column=0)
bouton_savequit.grid(row=0,column=0)

def Menu(): 
    """
    affiche un menu 
    """
    label_choix.grid()
    bouton_charger.grid()
    bouton_creer.grid()
    scale_x.grid()
    scale_y.grid()

    canvas.delete("all")
    canvas.grid_remove()
    bouton_annuler.grid_remove()
    bouton_savequit.grid_remove()

def Jouer():
    """
    Affiche la partie
    """
    
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

Menu()

fenetre.mainloop()