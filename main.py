from pygame import mixer
from os.path import isfile
import tkinter as tk
import sys

mixer.init()
pion_sound = mixer.Sound("super-mario-64-thwomp-sound-online-audio-converter.mp3")

fenetre = tk.Tk()
fenetre.title("Puissance 4")
# fenetre.config(bg = "gray0")

size = 50
tour = 1
pion = 1
last_moves = []
colors=["red","yellow","dark blue","blue"]
Gpuissance4 = []



## savefile
def modifier(file_name,text='',ligne=None):
    lines = []
    if isfile(file_name):
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
    if isfile(file_name):
        file = open(file_name,'r')
        lines = file.readlines()
        file.close()
        return lines
    return -1

def transform_to_tab(file_name):
    tab = []
    text = recuperer(file_name)
    if text == -1:
        text = ["0 "*scale_y.get() + "\n"]*scale_x.get()
    for row in text:
        stripped = row.strip() ## removes \n
        splitted = stripped.split() ## removes spaces
        for case in range(len(splitted)):
            splitted[case] = int(splitted[case],2)
        tab.append(splitted)
    return tab

def transform_to_string(tab):
    text = ''
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            text += bin(tab[i][j])
            if j != len(tab[i])-1:
                text += ' '
        text += '\n'
    return text



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



## tkinter
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
    global Gpuissance4
    global tour
    global pion
    global last_move

    x = event.x//size
    if tour%2==0:
        pion = 2
    else:
        pion = 1

    if -1 < x < len(Gpuissance4):
        y = placer_pion(Gpuissance4, x, pion)
        if y != -1:
            pion_sound.play()
            last_moves.append((x,y))
            X = x*size
            Y = (len(Gpuissance4[0])-y)*size
            canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[tour%2])
            if verifier_4(Gpuissance4, pion):
                Gagner()
            bouton_annuler["state"] = "normal"
            tour += 1

def Annuler():
    global last_moves
    global tour
    global Gpuissance4
    if any(last_moves):
        x,y = last_moves.pop()
        remplacer_pion(Gpuissance4, x, y, 0)
        X = x*size
        Y = (len(Gpuissance4[0])-y)*size
        canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[2])
        tour -= 1
    else:
        bouton_annuler["state"] = "disabled"

def lancer_partie(choix):
    global canvas
    global Gpuissance4
    if choix == "charger":
        Gpuissance4 = transform_to_tab('Puissance_4_save.txt')
        canvas = creer_canvas(Gpuissance4, size)
        for i in range(len(Gpuissance4)):
            for j in range(len(Gpuissance4[0])):
                if Gpuissance4[i][j] != 0:
                    X = i*size
                    Y = (len(Gpuissance4[0])-j)*size
                    canvas.create_oval(X+4,Y-4,X+size-4,Y-size+4,fill=colors[Gpuissance4[i][j]%2])
        
    elif choix == "standard":
        x,y = scale_x.get(),scale_y.get()
        Gpuissance4 = creer_grille(x,y)
        canvas = creer_canvas(Gpuissance4, size)
    
    elif choix == "retry":
        Gpuissance4 = creer_grille(len(Gpuissance4), len(Gpuissance4[0]))
        canvas = creer_canvas(Gpuissance4, size)
    
    Jouer()
    
    # elif "manches" in choix:
    #     for manche in range(int(choix[0])):
    #         x,y = int(choix[2]),int(choix[3])
    #         Gpuissance4 = creer_grille(x,y)
    #         canvas = creer_canvas(Gpuissance4, size)
    #         Jouer()



## menus/fenetres
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
    label_quitter.grid_remove()
    save_oui.grid_remove()
    save_non.grid_remove()

    label_gagner.grid_remove()
    retry_oui.grid_remove()
    retry_non.grid_remove()

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

    label_gagner.grid_remove()
    retry_oui.grid_remove()
    retry_non.grid_remove()

def SauvegarderQuitter():
    scale_x.grid_remove()
    scale_y.grid_remove()

    canvas.delete("all")
    canvas.itemconfig(1, state='hidden')
    canvas.grid_remove()
    bouton_annuler.grid_remove()
    bouton_savequit.grid_remove()

    label_quitter.grid(row=0,column=0,columnspan=2)
    save_oui.grid(row=1,column=0)
    save_non.grid(row=1,column=1)

def Gagner():
    if tour%2 == 1:
        couleur = "jaune"
    else:
        couleur = "rouge"
    label_gagner['text'] = f"Le joueur {couleur} a gagné !\n Voulez-vous recommencer la partie ?"
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
save_oui = tk.Button(fenetre, text="oui",command=lambda:[supprimer('Puissance_4_save.txt'),modifier('Puissance_4_save.txt',transform_to_string(Gpuissance4)),Menu()])
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