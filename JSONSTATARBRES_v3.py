#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emman
#
# Created:     06/07/2022
# Copyright:   (c) emman 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
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

def getValues():
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
        listeArrdt = Listbox(frameListes, width=20,)
        listeArrdt.insert(1, 'TOUS')
        for el in arrondissements:
            index = arrondissements.index(el)
            listeArrdt.insert(index +2, el)
            listeArrdt.bind('<<ListboxSelect>>', selectArrdt)
        listeArrdt.pack(side=LEFT)

        arrdtIsVisible = True


def creationListeArbre():
    global listeArbre, arbreIsVisible
    if arbreIsVisible == True:
        listeArbre.destroy()
        arbreIsVisible = False
    else:
        current_arbre = StringVar(value=0)
        listeArbre = Listbox(frameListes, width=20)
        listeArbre.insert(1, 'TOUS')
        for el in arbres:
            index = arbres.index(el)
            listeArbre.insert(index +2, el)
            listeArbre.bind('<<ListboxSelect>>', selectArbre)
        listeArbre.pack(side=LEFT)
        arbreIsVisible = True

def creationListeCritere():
    global listeCritere, critereIsVisible
    if critereIsVisible == True:
        listeCritere.destroy()
        critereIsVisible = False
    else:
        listeCritere = Listbox(frameListes, width=20)
        listeCritere.insert(1, "Quantité")
        listeCritere.insert(2, "Hauteur")
        listeCritere.insert(3, "Type")
        listeCritere.bind('<<ListboxSelect>>', selectCritere)
        listeCritere.pack(side=LEFT)
        critereIsVisible = True

mainFenetre = Tk()
mainFenetre.title('JSON STAT ARBRES')
mainFenetre.geometry('1000x800')


#-----------------------------------------------------------------------
#                 FRAME GAUCHE
#-----------------------------------------------------------------------

frameGauche = Frame(mainFenetre, bg='Red',)
frameGauche.pack(side=LEFT, fill=Y)

#---------- TOP : DEMANDE----------

frameDemande = Frame(frameGauche, bg='Blue')
frameDemande.pack(side=TOP, fill=BOTH, expand=True)

frameMenu = Frame(frameDemande, bg="Pink",)
frameMenu.pack(side=TOP)

frameBoutons = Frame(frameMenu, bg="Purple", height=200)
frameBoutons.pack(side=TOP)

frameListes = Frame(frameMenu, bg="Brown",)
frameListes.pack(side=TOP)


# Arrdt

boutonArrdt = Button(frameBoutons, text="Arrondissement", command=creationListeArrdt, width=17)
boutonArrdt.pack(side=LEFT)



#Arbre

boutonArbre = Button(frameBoutons, text="Arbre", command=creationListeArbre, width=17)
boutonArbre.pack(side=LEFT)



#Critère

boutonCritere = Button(frameBoutons, text="Critere", command=creationListeCritere, width=17)
boutonCritere.pack(side=LEFT)



#BoutonAPPLY
frameBouton = Frame(frameDemande, bg="Orange",)
frameBouton.pack(side=BOTTOM, fill=X,)

boutonApply = Button(frameBouton, text="APPLY", command=getValues)
boutonApply.pack(side=RIGHT)



#---------- BOTTOM : REPONSE TEXTUELLE ----------


frameReponseTexte = Frame(frameGauche, bg='Black')
frameReponseTexte.pack(side=BOTTOM, fill=BOTH, expand=True)

boutonTexte = Button(frameReponseTexte, text="TEXTE")
boutonTexte.pack()





#-----------------------------------------------------------------------
#                 FRAME DROITE
#-----------------------------------------------------------------------

frameDroite = Frame(mainFenetre, bg='Green')
frameDroite.pack(side=RIGHT, expand=True, fill=BOTH)

#---------- TOP : MAP ----------

frameMap = Frame(frameDroite, bg='Yellow')
frameMap.pack(side=TOP, fill=BOTH, expand=True)

boutonMap = Button(frameMap, text="Map")
boutonMap.pack()


#---------- BOTTOM : GRAPH  ----------

frameGraph = Frame(frameDroite, bg='White')
frameGraph.pack(side=BOTTOM, fill=BOTH, expand=True)


boutonGraph = Button(frameGraph, text="Graph")
boutonGraph.pack()





#boutonArrdt = Button(mainFenetre, command=creationListe)
#boutonArrdt.pack()




















mainFenetre.mainloop()