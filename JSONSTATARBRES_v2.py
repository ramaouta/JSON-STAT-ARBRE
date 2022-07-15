## WELCOME IN JSONSTATARBRES APP

import pandas
from tkinter import *
arrdtIsVisible = False
arbreIsVisible = False
critereIsVisible = False

new_df = pandas.read_csv(r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\new_arbres.csv", sep = ',', header = 0)


listeArrdt = []
g = new_df.groupby('ARRONDISSEMENT')
for groupe in g:
    print(groupe[0])
    listeArrdt.append(groupe[0])

full=g[["HAUTEUR (m)"]].agg([pandas.Series.mean,pandas.Series.max,pandas.Series.min])
print(full)
full.insert(0, 'ARRONDISSEMENT', listeArrdt)
print(full)
full.to_csv('full.csv')



'''
arrondissements = list(new_df['ARRONDISSEMENT'].unique())
arrondissements.sort()
print('arrondissements : ', arrondissements)

arbres = list(new_df['LIBELLE FRANCAIS'].unique())
for arbre in arbres:
    #print('type(arbre) :', type(arbre))
    if str(arbre) != arbre:
        arbres.pop(arbres.index(arbre))
arbres.sort()
print('arbres : ', arbres)

def creationListeArrdt():
    global listeArrdt, arrdtIsVisible
    if arrdtIsVisible == True:
        listeArrdt.destroy()
        arrdtIsVisible = False
    else:
        listeArrdt = Listbox(frameArrdt)
        for el in arrondissements:
            index = arrondissements.index(el)
            listeArrdt.insert(index +1, el)
        listeArrdt.pack()
        arrdtIsVisible = True

def creationListeArrdt():
    global scrollArrdt, arrdtIsVisible, listeArrdt
    if arrdtIsVisible == True:
        scrollArrdt.destroy()
        listeArrdt.destroy()
        arrdtIsVisible = False
    else:
        scrollArrdt = Scrollbar(frameDemande)
        scrollArrdt.pack(side = RIGHT, fill = Y)
        listeArrdt = Listbox(frameDemande, yscrollcommand = scrollArrdt.set )
        for el in arrondissements:
            index = arrondissements.index(el)
            listeArrdt.insert(END, el)
        listeArrdt.pack(side = LEFT, fill = BOTH)
        scrollArrdt.config(command = listeArrdt.yview)

        arrdtIsVisible = True

def creationListeArbre():
    global listeArbre, arbreIsVisible
    if arbreIsVisible == True:
        listeArbre.destroy()
        arbreIsVisible = False
    else:
        listeArbre = Listbox(frameArbre)
        for el in arbres:
            index = arbres.index(el)
            listeArbre.insert(index +1, el)
        listeArbre.pack()
        arbreIsVisible = True


def creationListeArbre():
    global scrollArbre, arbreIsVisible, listeArbre
    if arbreIsVisible == True:
        scrollArbre.destroy()
        listeArbre.destroy()
        arbreIsVisible = False
    else:
        scrollArbre = Scrollbar(frameArbre)
        scrollArbre.pack(side = RIGHT, fill = Y)
        listeArbre = Listbox(frameArbre, yscrollcommand = scrollArbre.set )
        for el in arbres:
            index = arbres.index(el)
            listeArbre.insert(END, el)
        listeArbre.pack(side = LEFT, fill = BOTH)
        scrollArbre.config(command = listeArbre.yview)

        arbreIsVisible = True

def creationListeCritere():
    global listeCritere, critereIsVisible
    if critereIsVisible == True:
        listeCritere.destroy()
        critereIsVisible = False
    else:
        listeCritere = Listbox(frameCritere)
        listeCritere.insert(1, "Hauteur")
        listeCritere.insert(2, "Quantité")
        listeCritere.insert(3, "3eme")
        listeCritere.insert(4, "4eme")
        listeCritere.insert(5, "5eme")
        listeCritere.pack()
        critereIsVisible = True




mainFenetre = Tk()
mainFenetre.title('JSON STAT ARBRES')
mainFenetre.geometry('1000x800')


#-----------------------------------------------------------------------
#                 FRAME GAUCHE
#-----------------------------------------------------------------------

frameGauche = Frame(mainFenetre, bg='Red',)
frameGauche.pack(side=LEFT, expand=True, fill=BOTH)

#---------- TOP : DEMANDE----------

frameDemande = Frame(frameGauche, bg='Blue')
frameDemande.pack(side=TOP, fill=BOTH, expand=True)


# Arrdt
frameArrdt = Frame(frameDemande, bg="Grey", width=500)
frameArrdt.pack(side=LEFT, fill=Y,)

boutonArrdt = Button(frameDemande, text="Arrondissement", command=creationListeArrdt)
boutonArrdt.pack(side=TOP)


#Arbre
frameArbre = Frame(frameDemande, bg="Grey", width=500)
frameArbre.pack(side=LEFT, fill=Y,)

boutonArbre = Button(frameArbre, text="Arbre", command=creationListeArbre)
boutonArbre.pack(side=TOP)


#Critère
frameCritere = Frame(frameDemande, bg="Grey", width=500)
frameCritere.pack(side=LEFT, fill=Y,)

boutonCritere = Button(frameCritere, text="Critere", command=creationListeCritere)
boutonCritere.pack(side=TOP)

#---------- BOTTOM : REPONSE TEXTUELLE ----------


frameReponseTexte = Frame(frameGauche, bg='Black')
frameReponseTexte.pack(side=BOTTOM, fill=BOTH, expand=True)





#-----------------------------------------------------------------------
#                 FRAME DROITE
#-----------------------------------------------------------------------

frameDroite = Frame(mainFenetre, bg='Green')
frameDroite.pack(side=RIGHT, expand=True, fill=BOTH)

#---------- TOP : MAP ----------

frameMap = Frame(frameDroite, bg='Yellow')
frameMap.pack(side=TOP, fill=BOTH, expand=True)




#---------- BOTTOM : GRAPH  ----------

frameGraph = Frame(frameDroite, bg='White')
frameGraph.pack(side=BOTTOM, fill=BOTH, expand=True)








#boutonArrdt = Button(mainFenetre, command=creationListe)
#boutonArrdt.pack()
mainFenetre.mainloop()
'''


















