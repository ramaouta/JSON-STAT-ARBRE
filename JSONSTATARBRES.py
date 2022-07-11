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

localisation= {
    'PARIS 20E ARRDT': [48.8625565,2.3791177],
    'PARIS 19E ARRDT':[48.8871247,2.3702572],
    'PARIS 18E ARRDT': [48.8919626,2.331184],
    'PARIS 17E ARRDT': [48.8874353,2.2875386],
    'PARIS 16E ARRDT': [48.8572065,2.2279586] , 
    'PARIS 15E ARRDT': [48.84008537593816,2.292825822424994],
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
    'PARIS 2E ARRDT': [48.86827922252251,2.342802546891362], 
    'PARIS 1ER ARRDT':[48.8620317,2.3183917],
    'CENTRE DE PARIS' : [48.866667,2.3333333], 
    'HAUTS-DE-SEINE':[48.828508,2.2188068]
     
}

appartenance= {
    'PARIS 20E ARRDT': 20	,
    'PARIS 19E ARRDT': 19,
    'PARIS 18E ARRDT': 18,
    'PARIS 17E ARRDT': 17,
    'PARIS 16E ARRDT': 16 , 
    'PARIS 15E ARRDT': 15,
    'PARIS 14E ARRDT': 14,
    'PARIS 13E ARRDT': 13 ,
    'PARIS 12E ARRDT': 12 ,
    'PARIS 11E ARRDT': 11 ,
    'PARIS 10E ARRDT':10 ,
    'PARIS 9E ARRDT': 9,
    'PARIS 8E ARRDT': 8 ,
    'PARIS 7E ARRDT': 7,
    'PARIS 6E ARRDT': 6,
    'PARIS 5E ARRDT': 5, 
    'PARIS 4E ARRDT': 4 ,
    'PARIS 3E ARRDT':3 ,
    'PARIS 2E ARRDT': 2 , 
    'PARIS 1ER ARRDT': 1
    
}

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#                 DATA
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


#Lecture du fichier CSV
new_df = pandas.read_csv("new_arbres.csv", sep = ',', header = 0)

#Récupération de la liste des arrondissements issus du CSV
arrondissements = list(new_df['ARRONDISSEMENT'].unique())
#print(arrondissements)
arrondissements.sort()

#Récupération de la liste des arbres issus du CSV
arbres = list(new_df['LIBELLE FRANCAIS'].unique())
for arbre in arbres:
    # Suppression des arbres 'non renseignés'
    if str(arbre) != arbre:
        arbres.pop(arbres.index(arbre))
arbres.sort()

#@laf
#lecture arrondissement csv 
arr_frame = pandas.read_csv("arrondissements.csv", sep = ';', header = 0)

''' 
localisation_arbres = {}
loc = new_df.loc[:,['LIBELLE FRANCAIS' ,'LONGITUDE' , 'LATITUDE']]


for i , row in loc.iterrows(): 
    localisation_arbres[ tuple([row['LONGITUDE'], row['LATITUDE']])] = row['LIBELLE FRANCAIS']
print(localisation_arbres)
'''
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#                 FONCTION
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
def affiche_map(tab,app): 
    #numero d'arrondissement spec 
    print("*******************",tab)
    arr= []
    for i, j  in tab.items(): 
        arr.append(i)
        map_widget.set_marker(j[0], j[1] , text= i) 
    
    for i in app : 

        a = arr_frame.loc[(arr_frame ["Numéro d’arrondissement"] == i ) & (arr_frame["Geometry X Y"])]
        print(a)   
        liste = a["Geometry"].to_list()
        print(type(liste[0]))
        string = liste[0][1:-1]
        print('string : ', string)
        # change une string en dictionnaire
        res = {key: (val) for key, val in (item.split(':') for item in string.split(', "'))} 
        print(type(res))
        #print(res)
        # la valeur de dico[clé] est une string
        print("type", type(res['"coordinates"']))
        # eval("string") → change la string en liste
        res = eval(res['"coordinates"'])
        print('newres : ',type(res[0]))
        print('newres2 : ',res[0][0][1])
        res = res[0]
        polygo =[]
        for coord in res:
            print(coord)
            points= [coord[1],coord[0]]
            polygo.append(tuple(points))
            #on a bien un dictionnaire avec des valeur en listes
        print(polygo)

        map_widget.set_polygon(polygo, 
                                fill_color = 'red', 

        )


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
    
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D&s=Ga", max_zoom=22)
    
    

    '''map_widget.set_polygon([(46.0732306, 6.0095215),
                            (46.25,6.38),
                                    (46.3772542, 6.4160156)],
                                   # fill_color=None,
                                   # outline_color="red",
                                   # border_width=12,
                                   name="switzerland_polygon") #list tuple    ::: fill_color, outline_color, border_width
    '''
    # Marqueurs
    
    if data[0] == 'TOUS' and data[1] == 'TOUS' and data[2] == "Quanti":

        sns.set(style="white")

        dataQ1 = pandas.read_csv("new_arbres.csv")
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
        affiche_map()

    if data[0] == 'TOUS' and data[1] != 'TOUS' and data[2] == "Quantité":
        dataQ1 = pandas.read_csv("new_arbres.csv")
        dg = dataQ1.query('`LIBELLE FRANCAIS` == @data[1]')
        df_maxArbre = dg["ARRONDISSEMENT"].value_counts().keys()[0]
        df_minArbre = dg["ARRONDISSEMENT"].value_counts().keys()[-1]
        df_nbrMaxArbre = dg["ARRONDISSEMENT"].value_counts()[0]
        df_nbrMinArbre = dg["ARRONDISSEMENT"].value_counts()[-1]

        result = f"L'arrondissement qui compte le plus de {data[1]} est {df_maxArbre} avec {df_nbrMaxArbre} arbre(s).\n\nL'arrondissement qui compte le moins de {data[1]} est {df_minArbre} avec {df_nbrMinArbre} arbre(s)"
        print(f"L'arrondissement qui compte le plus de {data[1]} est {df_maxArbre} avec {df_nbrMaxArbre} arbre(s).\n\nL'arrondissement qui compte le moins de {data[1]} est {df_minArbre} avec {df_nbrMinArbre} arbre(s)")
        frameLabelText = Label(frameMap, text=result)
        frameLabelText.pack(side = LEFT)
    #@laf
    #map "TOUS" - "TOUS" - Qté 
    if data[0]== 'TOUS' and data[1] == 'TOUS' and data[2] == "Quantité": 
        reponse = {}
        app = []  #app pour détourer l 'arrondissement
        map_arbre = new_df["ARRONDISSEMENT"].value_counts()
        nom_arrond_max = new_df["ARRONDISSEMENT"].value_counts().idxmax(axis=0)
        nom_arrond_min = new_df["ARRONDISSEMENT"].value_counts().idxmin(axis=0) 

        #affiche arrondissement 
        if nom_arrond_max in localisation: 
            reponse[nom_arrond_max] = localisation[nom_arrond_max]
            app.append(appartenance[nom_arrond_max])
        if nom_arrond_min in localisation: 
            #reponse.append(localisation[nom_arrond_min])
            reponse[nom_arrond_min] = localisation[nom_arrond_min]
            app.append(appartenance [nom_arrond_min])

        affiche_map(reponse,app)

    # Arbre le plus haut par arrondissement
    if data[0]== 'TOUS' and data[1]== 'TOUS' and data[2]== 'Hauteur':
        reponse ={}
        #hauteur arrondissement max 
        hautNom_arrMax = new_df.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].mean().sort_values(ascending=False).idxmax(axis=0)        #hauteur nombre max 
        hautNbr_Max = new_df.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].mean().sort_values(ascending=False).max()

        

        #hauteur arrondissement max 
        hautNom_arrMin = new_df.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].mean().sort_values(ascending=False).idxmin(axis=0)
        
        #hauteur nombre max 
        hautNbr_Min = new_df.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].mean().sort_values(ascending=False).min()


        
        if hautNom_arrMax in localisation : 
            reponse[hautNom_arrMax] = localisation [hautNom_arrMax]
            app.append(appartenance[hautNom_arrMax])
        
        
        if hautNom_arrMin in localisation: 
            reponse[hautNom_arrMin] = localisation [hautNom_arrMin]
            app.append(appartenance [hautNom_arrMin])

        affiche_map(reponse,app)

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