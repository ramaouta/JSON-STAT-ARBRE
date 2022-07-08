## WELCOME IN JSONSTATARBRES APP



from PIL import ImageTk

import PIL.Image


from tkinter import *
from tkinter import messagebox
import pandas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import seaborn as sns
import numpy as np
import random
from tkintermapview import TkinterMapView



# les variables xxxIsVisible servent à afficher ou effacer les listes box (dans la partie demande) au clic sur le bouton correspondant
arrdtIsVisible = False
arbreIsVisible = False
critereIsVisible = False


data=["TOUS", "TOUS", "Quantité"]


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
#                 FONCTION
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

def apply():
    ## Affiche les réponses, graphes et map relatifs à la demande
    global frameCanvas, map_widget
    try:
        frameCanvas.destroy()
        map_widget.destroy()
    except:
        pass


    # create map widget
    map_widget = TkinterMapView(frameGraph, width=500, height=500, corner_radius=0)
    map_widget.pack(fill="both", expand=True)

    # Zone affichée de la carte
    map_widget.set_position(48.860381, 2.338594)

    # Zoom
    map_widget.set_zoom(11)

    # Marqueurs
    map_widget.set_marker(48.867, 2.323, text="2eme")
    map_widget.set_marker(48.8417, 2.2586, text="15eme")


    if data[0] == 'TOUS' and data[1] == 'TOUS' and data[2] == "Quantité":

        sns.set(style="white")

        dataQ1 = pandas.read_csv(r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\new_arbres.csv")
        dataQ1 = dataQ1.assign(COUNT=1)
        dataQ1 = (pandas.crosstab  ( dataQ1['ARRONDISSEMENT'], dataQ1['COUNT'] ))
        dataQ1.columns=['COUNT']
        listeArrdt = dataQ1.index.tolist()
        dataQ1.insert(0, "ARRONDISSEMENT", listeArrdt)


        plt.figure(figsize = (20, 20))
        f, ax = plt.subplots(figsize=(12, 9))
        f.subplots_adjust(bottom=0.50)
        plt.xticks(rotation=80)
        font = {'family' : 'normal','size'   : 8}
        plt.rc('font', **font)
        plt.gcf().set_size_inches(5, 5)
        plt.xlabel('ARRONDISSEMENT')
        sns.barplot(x = 'ARRONDISSEMENT', y = 'COUNT',data = dataQ1)


        frameCanvas = Frame(frameReponseTexte)
        frameCanvas.pack(fill=BOTH)
        canvas = FigureCanvasTkAgg(f, master = frameCanvas)
        canvas.draw()
        canvas.get_tk_widget().pack()


    if data[0] == 'TOUS' and data[1] != 'TOUS' and data[2] == "Quantité":
        dataQ1 = pandas.read_csv(r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\new_arbres.csv")
        dg = dataQ1.query('`LIBELLE FRANCAIS` == @data[1]')
        df_maxArbre = dg["ARRONDISSEMENT"].value_counts().keys()[0]
        df_minArbre = dg["ARRONDISSEMENT"].value_counts().keys()[-1]
        df_nbrMaxArbre = dg["ARRONDISSEMENT"].value_counts()[0]
        df_nbrMinArbre = dg["ARRONDISSEMENT"].value_counts()[-1]

        result = f"L'arrondissement qui compte le plus de {data[1]} est {df_maxArbre} avec {df_nbrMaxArbre} arbre(s).\n\nL'arrondissement qui compte le moins de {data[1]} est {df_minArbre} avec {df_nbrMinArbre} arbre(s)"
        print(f"L'arrondissement qui compte le plus de {data[1]} est {df_maxArbre} avec {df_nbrMaxArbre} arbre(s).\n\nL'arrondissement qui compte le moins de {data[1]} est {df_minArbre} avec {df_nbrMinArbre} arbre(s)")
        frameLabelText = Label(frameMap, text=result)
        frameLabelText.pack(side = LEFT)





def selectArrdt(event):
    ## Mise à jour de l'arrondissement sélectionné dans la demande
    global listeArrdt, data
    arrdt = listeArrdt.selection_get()
    creationListeArrdt()
    data[0] = arrdt
    print('data : ', data)

def selectArbre(event):
    ## Mise à jour du type d'arbre sélectionné dans la demande
    global listeArbre, data
    arbre = listeArbre.selection_get()
    creationListeArbre()
    data[1] = arbre
    print('data : ', data)

def selectCritere(event):
    ## Mise à jour du critère sélectionné dans la demande
    global listeCritere, data
    critere = listeCritere.selection_get()
    creationListeCritere()
    data[2] = critere
    print('data : ', data)


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
        #current_arrdt = StringVar(value=0)
        listeArrdt = Listbox(frameArrdt, width=20,)
        listeArrdt.insert(1, 'TOUS')
        for el in arrondissements:
            index = arrondissements.index(el)
            listeArrdt.insert(index +2, el)
            listeArrdt.bind('<<ListboxSelect>>', selectArrdt)
        listeArrdt.pack()

        arrdtIsVisible = True


def creationListeArbre():
    global listeArbre, arbreIsVisible
    if arbreIsVisible == True:
        listeArbre.destroy()
        arbreIsVisible = False
    else:
        #current_arbre = StringVar(value=0)
        listeArbre = Listbox(frameArbre, width=20)
        listeArbre.insert(1, 'TOUS')
        for el in arbres:
            index = arbres.index(el)
            listeArbre.insert(index +2, el)
            listeArbre.bind('<<ListboxSelect>>', selectArbre)
        listeArbre.pack()
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

frameDemande = Frame(frameGauche, bg='Blue', height = 500)
frameDemande.pack( fill=BOTH, expand=True)








frameMenu = Frame(frameDemande, bg="Pink",)
frameMenu.pack(side=TOP)

# Arrdt
frameArrdt = Frame(frameMenu, bg="Grey", width=500)
frameArrdt.pack(side=LEFT, fill=Y,)

boutonArrdt = Button(frameArrdt, text="Arrondissement", command=creationListeArrdt, width=17)
boutonArrdt.pack(side=TOP)

listeArrdt = Listbox(frameArrdt, width=20,)
listeArrdt.pack()
listeArrdt.destroy()


#Arbre
frameArbre = Frame(frameMenu, bg="Grey", width=500)
frameArbre.pack(side=LEFT, fill=Y,)

boutonArbre = Button(frameArbre, text="Arbre", command=creationListeArbre, width=17)
boutonArbre.pack(side=TOP)


#Critère
frameCritere = Frame(frameMenu, bg="Grey", width=500)
frameCritere.pack(side=LEFT, fill=Y,)

boutonCritere = Button(frameCritere, text="Critere", command=creationListeCritere, width=17)
boutonCritere.pack(side=TOP)



#BoutonAPPLY
frameBouton = Frame(frameDemande, bg="Orange",)
frameBouton.pack(side=BOTTOM, fill=X,)

boutonApply = Button(frameBouton, text="APPLY", command=apply)
boutonApply.pack(side=RIGHT)



#---------- BOTTOM : REPONSE TEXTUELLE ----------


frameReponseTexte = Frame(frameGauche, bg='Black', height = 500, width = 500)
frameReponseTexte.pack( fill=BOTH, expand=False)

'''
frameImage = Frame(frameReponseTexte)
frameImage.pack()

# Création et plug de l'image dans la Frame Image
im = PIL.Image.open("image5.png")
#im = Image.open(r"D:\Manu\FORMATIONS\PYTHON\PENDU\penduGIT\jeuPendu\image5.png")
im = im.resize((250, 250))
photo = ImageTk.PhotoImage(im, master = frameImage)
labelPhoto = Label(frameImage)
labelPhoto.img=photo
labelPhoto.config(image = labelPhoto.img)
labelPhoto.pack(pady=50)
'''


#-----------------------------------------------------------------------
#                 FRAME DROITE
#-----------------------------------------------------------------------

frameDroite = Frame(mainFenetre, bg='Green')
frameDroite.pack(side=RIGHT, expand=True, fill=BOTH)

#---------- TOP : MAP ----------

frameMap = Frame(frameDroite, bg='Yellow')
frameMap.pack(side=TOP, fill=BOTH, expand=True)




#---------- BOTTOM : GRAPH  ----------

frameGraph = Frame(frameDroite, bg='White', height=500, width=500)
frameGraph.pack(side=BOTTOM, fill=BOTH, expand=False)








#boutonArrdt = Button(mainFenetre, command=creationListe)
#boutonArrdt.pack()
















def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        mainFenetre.destroy()
        mainFenetre.quit()

mainFenetre.protocol("WM_DELETE_WINDOW", on_closing)



mainFenetre.mainloop()