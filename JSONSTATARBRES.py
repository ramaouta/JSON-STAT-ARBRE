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


# Dictionnaire des coordonnées des Arrondissements de Paris
localisation= {
    'PARIS 20E ARRDT': [48.8625565,2.3791177],
    'PARIS 19E ARRDT':[48.8871247,2.3702572],
    'PARIS 18E ARRDT': [48.8919626,2.331184],
    'PARIS 17E ARRDT': [48.8874353,2.2875386],
    'PARIS 16E ARRDT': [48.8572065,2.2279586] ,
    'PARIS 15E ARRDT': [48.8417055,2.2586112],
    'PARIS 14E ARRDT': [48.829721,2.3054438],
    'PARIS 13E ARRDT': [48.8302919,2.3480624] ,
    'PARIS 12E ARRDT': [48.8351159,2.3821336] ,
    'PARIS 11E ARRDT': [48.8601,2.36405] ,
    'PARIS 10E ARRDT':[48.8759882,2.3448933] ,
    'PARIS 9E ARRDT':[48.877097,2.3291154] ,
    'PARIS 8E ARRDT':[48.8732641,2.2935887] ,
    'PARIS 7E ARRDT': [48.8548603,2.2939732],
    'PARIS 6E ARRDT':[48.8495301,2.3131637] ,
    'PARIS 5E ARRDT': [48.8454734,2.3338198],
    'PARIS 4E ARRDT': [48.8541126,2.3393264],
    'PARIS 3E ARRDT': [48.8625682,2.3505515],
    'PARIS 2E ARRDT': [ 48.8677006,2.3323497],
    'PARIS 1ER ARRDT':[48.8620317,2.3183917],
    'CENTRE DE PARIS' : [48.8589465,2.2768229],
    'HAUTS-DE-SEINE':[48.828508,2.2188068]
}

color = "White"


# les variables xxxIsVisible servent à afficher ou effacer les listes box (dans la partie demande) au clic sur le bouton correspondant
arrdtIsVisible = False
arbreIsVisible = False
critereIsVisible = False

# Création d'une variable data correspondant au choix de l'utilisateur. Format : ["Arrpndissement", "Arbre", "Critère"]
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

    # A chaque demande del'utilisateur : Destruction des Graphe, Map et Label précédents
    global frameCanvas, map_widget, frameLabelText
    try:
        print(1)
        frameLabelText.destroy()
        frameCanvas.destroy()
        map_widget.destroy()
    except:
        pass


    if data[0] == 'TOUS' and data[1] == 'TOUS' and data[2] == "Quantité":

        #CREATION DU GRAPH------------------------------------------------------
        sns.set(style="white")
        dataQ1 = pandas.read_csv(r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\new_arbres.csv")
        dataQ1 = dataQ1.assign(COUNT=1)
        dataQ1 = (pandas.crosstab  ( dataQ1['ARRONDISSEMENT'], dataQ1['COUNT'] ))
        dataQ1.columns=['COUNT']
        listeArrdt = dataQ1.index.tolist()
        dataQ1.insert(0, "ARRONDISSEMENT", listeArrdt)
        font = {'family' : 'normal','size'   : 5}
        plt.figure(figsize = (40, 30))
        plt.rc('font', **font)
        f, ax = plt.subplots(figsize=(12, 9))
        f.subplots_adjust(bottom=0.50)
        plt.xticks(rotation=80)
        plt.gcf().set_size_inches(5, 5)

        #plt.xlabel('ARRONDISSEMENT')
        sns.barplot(x = 'ARRONDISSEMENT', y = 'COUNT',data = dataQ1)
        frameCanvas = Frame(frameGraph)
        frameCanvas.pack(fill=BOTH)
        canvas = FigureCanvasTkAgg(f, master = frameCanvas)
        canvas.draw()
        canvas.get_tk_widget().pack()

        #CREATION DE LA MAP ----------------------------------------------------
        # create map widget
        map_widget = TkinterMapView(frameTheMap, width=400, height=400, corner_radius=0)
        map_widget.pack(  pady = 10, padx = 10, side=RIGHT)

        # Zone affichée de la carte = PARIS
        map_widget.set_position(48.860381, 2.338594)

        # Zoom
        map_widget.set_zoom(11)

        if data[0]== "TOUS" and data[1]== "TOUS" and data[2]== "Quantité":
            reponse =[]
            nom_arrond_max = new_df["ARRONDISSEMENT"].value_counts().idxmax(axis=0)
            nom_arrond_min = new_df["ARRONDISSEMENT"].value_counts().idxmin(axis=0)
            if nom_arrond_max in localisation:

                reponse.append(localisation[nom_arrond_max])
                reponse[0].append(nom_arrond_max)

            if nom_arrond_min in localisation:
                reponse.append(localisation[nom_arrond_min])
                reponse[1].append(nom_arrond_min)


        # Marqueurs
        map_widget.set_marker(reponse[0][0], reponse[0][1], text = reponse[0][2], marker_color_circle="#3a0ca3", marker_color_outside="#4361ee")
        map_widget.set_marker(reponse[1][0], reponse[1][1], text = reponse[1][2], marker_color_circle="#a4161a", marker_color_outside="#df7373")


        #CREATION DU TEXTE -----------------------------------------------------
        #nom_arrMax = new_df["ARRONDISSEMENT"].value_counts().idxmax(axis=0)
        nbr_arrMax = new_df["ARRONDISSEMENT"].value_counts().max()
        #nom_arrMin = new_df["ARRONDISSEMENT"].value_counts().idxmin(axis=0)
        nbr_arrMin = new_df["ARRONDISSEMENT"].value_counts().min()

        answer = f"L'arrondissement avec le plus d'arbre est {nom_arrond_max} comptant un total de {nbr_arrMax} arbre.\n\nCelui avec le moins d'arbre est {nom_arrond_min} avec un total de {nbr_arrMin} arbre."
        frameLabelText = Label(frameReponseTexte, text=answer)
        frameLabelText.pack(side = LEFT)



    if data[0] == 'TOUS' and data[1] != 'TOUS' and data[2] == "Quantité":

        dataQ1 = pandas.read_csv(r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\new_arbres.csv")
        dg = dataQ1.query('`LIBELLE FRANCAIS` == @data[1]')
        df_maxArbre = dg["ARRONDISSEMENT"].value_counts().keys()[0]
        df_minArbre = dg["ARRONDISSEMENT"].value_counts().keys()[-1]
        df_nbrMaxArbre = dg["ARRONDISSEMENT"].value_counts()[0]
        df_nbrMinArbre = dg["ARRONDISSEMENT"].value_counts()[-1]

        result = f"L'arrondissement qui compte le plus de {data[1]} est {df_maxArbre} avec {df_nbrMaxArbre} arbre(s).\n\nL'arrondissement qui compte le moins de {data[1]} est {df_minArbre} avec {df_nbrMinArbre} arbre(s)"
        #print(f"L'arrondissement qui compte le plus de {data[1]} est {df_maxArbre} avec {df_nbrMaxArbre} arbre(s).\n\nL'arrondissement qui compte le moins de {data[1]} est {df_minArbre} avec {df_nbrMinArbre} arbre(s)")
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
mainFenetre.geometry('1200x900')


#-----------------------------------------------------------------------
#                 FRAME GAUCHE
#-----------------------------------------------------------------------

#frameGauche = Frame(mainFenetre, bg='Red',)
frameGauche = Frame(mainFenetre, bg=color,)
frameGauche.pack(side=LEFT, expand=True, fill=BOTH)

#---------- TOP : DEMANDE----------

#frameDemande = Frame(frameGauche, bg='Blue', height = 500)
frameDemande = Frame(frameGauche, bg=color, height = 500)
frameDemande.pack( fill=BOTH, expand=True)








#frameMenu = Frame(frameDemande, bg="Pink",)
frameMenu = Frame(frameDemande, bg=color,)
frameMenu.pack(side=TOP)

# Arrdt
#frameArrdt = Frame(frameMenu, bg="Grey", width=500)
frameArrdt = Frame(frameMenu, bg=color, width=500)
frameArrdt.pack(side=LEFT, fill=Y,)

boutonArrdt = Button(frameArrdt, text="Arrondissement", command=creationListeArrdt, width=17)
boutonArrdt.pack(side=TOP)

listeArrdt = Listbox(frameArrdt, width=20,)
listeArrdt.pack()
listeArrdt.destroy()


#Arbre
#frameArbre = Frame(frameMenu, bg="Grey", width=500)
frameArbre = Frame(frameMenu, bg=color, width=500)
frameArbre.pack(side=LEFT, fill=Y,)

boutonArbre = Button(frameArbre, text="Arbre", command=creationListeArbre, width=17)
boutonArbre.pack(side=TOP)


#Critère
#frameCritere = Frame(frameMenu, bg="Grey", width=500)
frameCritere = Frame(frameMenu, bg=color, width=500)
frameCritere.pack(side=LEFT, fill=Y,)

boutonCritere = Button(frameCritere, text="Critere", command=creationListeCritere, width=17)
boutonCritere.pack(side=TOP)



#BoutonAPPLY
#frameBouton = Frame(frameDemande, bg="Orange",)
frameBouton = Frame(frameDemande, bg=color,)
frameBouton.pack(side=BOTTOM, fill=X, pady=5, padx=5)

boutonApply = Button(frameBouton, text="APPLY", command=apply)
boutonApply.pack(side=RIGHT)



#---------- BOTTOM : REPONSE TEXTUELLE ----------


#frameGraph = Frame(frameGauche, bg='Black', height = 500, width = 500)
frameGraph = Frame(frameGauche, bg=color, height = 600, width = 450)
frameGraph.pack( fill=BOTH, expand=False)

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

#frameDroite = Frame(mainFenetre, bg='Green')
frameDroite = Frame(mainFenetre, bg=color)
frameDroite.pack(side=RIGHT, expand=True, fill=BOTH)

#---------- TOP : MAP ----------

#frameReponseTexte = Frame(frameDroite, bg='Yellow')
frameReponseTexte = Frame(frameDroite, bg=color)
frameReponseTexte.pack(side=TOP, fill=BOTH, expand=True)




#---------- BOTTOM : GRAPH  ----------

#frameMap = Frame(frameDroite, bg='White', height=500, width=500)
frameMap = Frame(frameDroite, bg=color, height=600, width=450)
frameMap.pack(side=BOTTOM, fill=BOTH, expand=False)

frameTitreMap = Frame(frameMap, bg=color,)
frameTitreMap.pack(side=TOP)

titreMap = Label(frameTitreMap, text="MAP", bg = "Purple", fg = color)
titreMap.pack(side=LEFT, padx=10)

frameTheMap = Frame(frameMap, bg=color,)
frameTheMap.pack(side=TOP)






#boutonArrdt = Button(mainFenetre, command=creationListe)
#boutonArrdt.pack()






def center(win):
    '''code permetaatn de centrer la fenêtre quand on la lance'''
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()









def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        mainFenetre.destroy()
        mainFenetre.quit()

mainFenetre.protocol("WM_DELETE_WINDOW", on_closing)



mainFenetre.mainloop()