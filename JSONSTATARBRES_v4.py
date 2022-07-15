## WELCOME IN JSONSTATARBRES APP

import pandas
from tkinter import *
# les variables xxxIsVisible servent à afficher ou effacer les listes box (dans la partie demande) au clic sur le bouton correspondant
arrdtIsVisible = False
arbreIsVisible = False
critereIsVisible = False

current_arrdt = ""
current_arbre = ""
current_critere = ""
request=["TOUS", "TOUS", "Quantité"]


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#                 DATA
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


#Lecture du fichier CSV
new_df = pandas.read_csv(r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\new_arbres.csv", sep = ',', header = 0)

#Récupération de la liste des arrondissements issus du CSV
arrondissements = list(new_df['ARRONDISSEMENT'].unique())
arrondissements.sort()


#Récupération de la liste des arbres issus du CSV
arbres = list(new_df['LIBELLE FRANCAIS'].unique())
for arbre in arbres:
    # Suppression des arbres 'non renseignés'
    if str(arbre) != arbre:
        arbres.pop(arbres.index(arbre))
arbres.sort()

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#                 FONCTIONS
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------



def apply():
    lineArrdt = listeArrdt.curselection()[0]
    itemArrdt = listeArrdt.get(lineArrdt)
    current_arrdt.set(itemArrdt)
    print('current_arrdt : ', current_arrdt.get())
    lineArbre = listeArbre.curselection()[0]
    itemArbre = listeArbre.get(lineArbre)
    current_arbre.set(itemArbre)
    print('current_arbre : ', current_arbre.get())


def selectArrdt(event):
    global listeArrdt, request
    arrdt = listeArrdt.selection_get()
    creationListeArrdt()
    request[0] = arrdt
    print('request : ', request)

def selectArbre(event):
    global listeArbre, request
    arbre = listeArbre.selection_get()
    creationListeArbre()
    request[1] = arbre
    print('request : ', request)

def selectCritere(event):
    global listeCritere, request
    critere = listeCritere.selection_get()
    creationListeCritere()
    request[2] = critere
    print('request : ', request)


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#                 TKINTER
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

def creationListeArrdt():
    global listeArrdt, arrdtIsVisible, current_arrdt
    if arrdtIsVisible == True:
        listeArrdt.destroy()
        arrdtIsVisible = False
    else:
        current_arrdt = StringVar(value=0)
        listeArrdt = Listbox(frameArrdt, width=20,)
        listeArrdt.insert(1, 'TOUS')
        for el in arrondissements:
            index = arrondissements.index(el)
            listeArrdt.insert(index +2, el)
            listeArrdt.bind('<<ListboxSelect>>', selectArrdt)
        listeArrdt.grid(row=1, column=0)

        arrdtIsVisible = True


def creationListeArbre():
    global listeArbre, arbreIsVisible
    if arbreIsVisible == True:
        listeArbre.destroy()
        arbreIsVisible = False
    else:
        current_arbre = StringVar(value=0)
        listeArbre = Listbox(frameArbre, width=20)
        listeArbre.insert(1, 'TOUS')
        for el in arbres:
            index = arbres.index(el)
            listeArbre.insert(index +2, el)
            listeArbre.bind('<<ListboxSelect>>', selectArbre)
        listeArbre.grid(row=1, column=1)
        arbreIsVisible = True

def creationListeCritere():
    global listeCritere, critereIsVisible
    if critereIsVisible == True:
        listeCritere.destroy()
        critereIsVisible = False
    else:
        listeCritere = Listbox(frameCritere)
        listeCritere.insert(1, "Quantité")
        listeCritere.insert(2, "Hauteur")
        listeCritere.insert(3, "Type")
        listeCritere.bind('<<ListboxSelect>>', selectCritere)
        listeCritere.grid(row=1, column=2)
        critereIsVisible = True

mainFenetre = Tk()
mainFenetre.title('JSON STAT ARBRES')
mainFenetre.geometry('1000x800')

mainFenetre.grid_columnconfigure(0, weight=1)
mainFenetre.grid_columnconfigure(1, weight=1)


#-----------------------------------------------------------------------
#                 FRAME GAUCHE
#-----------------------------------------------------------------------

frameGauche = Frame(mainFenetre, bg='Red',width=500)
frameGauche.grid(row=0, column=0)

frameGauche.grid_rowconfigure(0, weight=1)
frameGauche.grid_rowconfigure(1, weight=1)

#---------- TOP : DEMANDE----------

labelDemande = Label(frameGauche, text='DEMANDE', width=50)
labelDemande.grid(row=0, column=0)

frameDemande = Frame(frameGauche, bg='Blue', height=1000)
frameDemande.grid(row=1, column=0)



frameMenu = Frame(frameDemande, bg="Pink", height=500)
frameMenu.grid(row=0, column=0)

# Arrdt
frameArrdt = Frame(frameMenu, bg="Grey", width=500)
frameArrdt.pack(side=LEFT, fill=Y,)
#frameArrdt.grid(row=0, column=0)

boutonArrdt = Button(frameArrdt, text="Arrondissement", command=creationListeArrdt, width=17)
boutonArrdt.grid(row=0, column=0)


#Arbre
frameArbre = Frame(frameMenu, bg="Grey", width=500)
frameArbre.pack(side=LEFT, fill=Y,)
#frameArbre.grid(row=0, column=1)

boutonArbre = Button(frameArbre, text="Arbre", command=creationListeArbre, width=17)
boutonArbre.grid(row=0, column=1)


#Critère
frameCritere = Frame(frameMenu, bg="Grey", width=500)
frameCritere.pack(side=LEFT, fill=Y,)
#frameCritere.grid(row=0, column=2)

boutonCritere = Button(frameCritere, text="Critere", command=creationListeCritere, width=17)
boutonCritere.grid(row=0, column=2)



#BoutonAPPLY
frameBouton = Frame(frameDemande, bg="Orange",)
frameBouton.grid(row=1, column=0)

boutonApply = Button(frameBouton, text="APPLY", command=apply)
boutonApply.pack(side=RIGHT)



#---------- BOTTOM : REPONSE TEXTUELLE ----------


frameReponseTexte = Frame(frameGauche, bg='Black')
frameReponseTexte.grid(row=2, column=0)

boutonTexte = Button(frameReponseTexte, text="TEXTE")
boutonTexte.pack()




#-----------------------------------------------------------------------
#                 FRAME DROITE
#-----------------------------------------------------------------------

frameDroite = Frame(mainFenetre, bg='Green', width=500)
frameDroite.grid(row=0, column=1)

frameDroite.grid_rowconfigure(0, weight=1)
frameDroite.grid_rowconfigure(1, weight=1)

#---------- TOP : MAP ----------

frameMap = Frame(frameDroite, bg='Yellow', height=1000)
frameMap.grid(row=0, column=0)

boutonMap = Button(frameMap, text="Map")
boutonMap.pack()




#---------- BOTTOM : GRAPH  ----------

frameGraph = Frame(frameDroite, bg='White')
frameGraph.grid(row=1, column=0)

boutonGraph = Button(frameGraph, text="Graph")
boutonGraph.pack()







#boutonArrdt = Button(mainFenetre, command=creationListe)
#boutonArrdt.pack()




















mainFenetre.mainloop()