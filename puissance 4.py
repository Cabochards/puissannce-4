from os.path import exists
import tkinter as tk
import sys

## grille
def creer_grille(x,y):
    grille = []
    for i in range(x):
        grille += [[0 for j in range(y)]]
    return grille

def afficher_grille(grille):
    for row in grille:
        print (row)

def remplacer_pion(grille,x,y,pion):
    grille[x][y] = pion

def placer_pion(grille,x,pion):
    for y in range(len(grille[x])):
        if grille[x][y] == 0:
            remplacer_pion(grille, x, y, pion)
            return y
    return -1

## Verifier pions
def verifier_4(grille,pion):
    for i in range(len(grille)):
        for j in range(len(grille[i])-3):
            if grille[i][j] == pion and grille[i][j+1] == pion and grille[i][j+2] == pion and grille[i][j+3] == pion:
               return True
    
    for i in range(len(grille)-3):
        for j in range(len(grille[i])):
            if grille[i][j] == pion and grille[i+1][j] == pion and grille[i+2][j] == pion and grille[i+3][j] == pion:
                return True
        
    for i in range(len(grille)-3):
        for j in range(len(grille[i])-3):
            if grille[i][j] == pion and grille[i+1][j+1] == pion and grille[i+2][j+2] == pion and grille[i+3][j+3] == pion:
                return True

    for i in range(len(grille)-3):
        for j in range(3,len(grille[i])):
            if grille[i][j] == pion and grille[i+1][j-1] == pion and grille[i+2][j-2] == pion and grille[i+3][j-3] == pion:
                return True

    return False

## Gerer sauvegarde
def modifier(file_name,text='',ligne=None):
    lines = []
    if exists(file_name):
        file = open(file_name,'r')
        lines = file.readlines()
        file.close()
    if ligne is None or ligne >= len(lines):
        lines.append(text)
    else:
        lines[ligne] = text
    file = open(file_name, 'w')
    file.writelines(lines)
    file.close()

def supprimer(file_name):
    file = open(file_name, 'w')
    file.writelines('')
    file.close()

def recuperer(file_name):
    file = open(file_name,'r')
    lines = file.readlines()
    file.close()
    return lines

def transform_to_tab(file_name):
    tab = []
    text = recuperer(file_name)
    for row in text:
        stripped = row.strip() ## removes \n
        splitted = stripped.split() ## removes spaces
        for case in range(len(splitted)):
            splitted[case] = int(splitted[case])
        tab.append(splitted)
    return tab

def transform_to_string(tab):
    text = ''
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            text += str(tab[i][j])
            if j != len(tab[i])-1:
                text += ' '
        text += '\n'
    return text
    
## tkinter
fenetre = tk.Tk()
fenetre.title("Puissance 4")

def creer_canvas(grille,size):
    canvas = tk.Canvas(fenetre,width=len(grille)*size,height=len(grille[0])*size,bg=colors[3])
    for i in range(len(grille)+1):
        for j in range(len(grille[0])+1):
            canvas.create_rectangle(i*size,j*size,i*size+size,j*size+size,outline=colors[2],width=4)
            
            X = i*size
            Y = (len(grille[0])-j)*size
            canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[2])
    return canvas

def Placer(event):
    global G
    global tour
    global pion
    global last_move

    x = event.x//size
    if tour%2==0:
        pion = 2
    else:
        pion = 1

    if -1 < x < len(G):
        y = placer_pion(G, x, pion)
        if y != -1:
            last_move.append((x,y))
            X = x*size
            Y = (len(G[0])-y)*size
            canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[tour%2])
            if verifier_4(G, pion):
                Menu()
            bouton_annuler["state"] = "normal"
            tour += 1

def Annuler():
    global last_move
    global tour
    global G
    if any(last_move):
        x,y = last_move.pop()
        remplacer_pion(G, x, y, 0)
        X = x*size
        Y = (len(G[0])-y)*size
        canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[2])
        tour -= 1
    else:
        bouton_annuler["state"] = "disabled"

def SauvegarderQuitter(G):
    #entree_choix.grid_remove()
    #valider.grid_remove()
    scale_x.grid_remove()
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
    global canvas
    global G
    if choix == "charger":
        G = transform_to_list('Puissance_4_save.txt')
        canvas = creer_canvas(G, size)
        for i in range(len(G)):
            for j in range(len(G[0])):
                if G[i][j] != 0:
                    X = i*size
                    Y = (len(G[0])-j)*size
                    canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[G[i][j]%2])
        Jouer()
        
    elif choix == "standard":
        x,y = scale_x.get(),scale_y.get()
        G = creer_grille(x,y)
        canvas = creer_canvas(G, size)
        Jouer()
    
    # elif "manches" in choix:
    #     for manche in range(int(choix[0])):
    #         x,y = int(choix[2]),int(choix[3])
    #         G = creer_grille(x,y)
    #         canvas = creer_canvas(G, size)
    #         Jouer()

size = 50
tour = 1
pion = 1
last_move = []
colors=["red","yellow","dark blue","blue"]
G = []

label_quitter = tk.Label(fenetre,text="Voulez-vous sauvegarder avant de quitter ?")
oui = tk.Button(fenetre, text="oui",command=lambda:[supprimer('Puissance_4_save.txt'),modifier('Puissance_4_save.txt',transform_to_string(G)),sys.exit()])
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