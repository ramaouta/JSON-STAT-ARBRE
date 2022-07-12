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
    'PARIS 15E ARRDT': [48.84008537593816,2.292825822424994],
    'PARIS 14E ARRDT': [48.829721,2.3054438],
    'PARIS 13E ARRDT': [48.8302919,2.3480624] ,
    'PARIS 12E ARRDT': [48.8351159,2.3821336] ,
    'PARIS 11E ARRDT': [48.8601,2.36405] ,
    'PARIS 10E ARRDT':[48.8759882,2.3448933] ,
    'PARIS 9E ARRDT':[48.877097,2.3291154] ,
    'PARIS 8E ARRDT':[48.8727208374345,2.3125540224020678] ,
    'PARIS 7E ARRDT': [48.8548603,2.2939732],
    'PARIS 6E ARRDT':[48.8495301,2.3131637] ,
    'PARIS 5E ARRDT': [48.8454734,2.3338198],
    'PARIS 4E ARRDT': [48.8541126,2.3393264],
    'PARIS 3E ARRDT': [48.8625682,2.3505515],
    'PARIS 2E ARRDT': [48.86827922252251,2.342802546891362],
    'PARIS 1ER ARRDT':[48.8620317,2.3183917],
    'CENTRE DE PARIS' : [48.866667,2.3333333],
    'HAUTS-DE-SEINE':[48.828508,2.2188068],
    'BOIS DE BOULOGNE': [48.86842, 2.23473],
    'BOIS DE VINCENNES': [48.8329, 2.4341],
    'SEINE-SAINT-DENIS': [48.9137455, 2.4845729],
    'VAL-DE-MARNE': [48.7931426, 2.4740337],


}

appartenance= {
    'PARIS 20E ARRDT': 20,
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
arr_df = pandas.read_csv(r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\arrondissements.csv", sep = ';', header = 0)

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
def affiche_map(marqueurs = {},zone = []):
    global map_widget
    ## Affiche la carte avec les marqueurs et les zones
    #numero d'arrondissement spec
    arr= []
    if type(marqueurs) == dict:
        for i, j  in marqueurs.items():
            arr.append(i)
            map_widget.set_marker(j[0], j[1] , text= i)

    for el in zone :
            a = arr_df.loc[(arr_df ["Numéro d’arrondissement"] == el ) & (arr_df["Geometry X Y"])]
            liste = a["Geometry"].to_list()
            string = liste[0][1:-1]
            # change une string en dictionnaire
            res = {key: (val) for key, val in (item.split(':') for item in string.split(', "'))}
            # la valeur de dico[clé] est une string
            # eval("string") → change la string en liste
            res = eval(res['"coordinates"'])
            res = res[0]
            polygo =[]
            for coord in res:
                print(coord)
                points= [coord[1],coord[0]]
                polygo.append(tuple(points))
                #on a bien un dictionnaire avec des valeur en listes
            map_widget.set_polygon(polygo)


def AfficheframeCanvas():
    ## Pack la frameCanvas dans frameGraph
    global f, frameCanvas
    frameCanvas = Frame(frameGraph, bg=color)
    frameCanvas.pack(fill=BOTH, expand=True)
    canvas = FigureCanvasTkAgg(f, master = frameCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack()


def AfficheframeLabelText():
    ## Pack la frameLabelText dans frameReponseTexte
    global answer, frameLabelText
    frameLabelText = Label(frameReponseTexte, text=answer, bg=color)
    frameLabelText.pack(side = LEFT)





def apply():
    ## Affiche les réponses, graphes et map relatifs à la demande

    # A chaque demande del'utilisateur : Destruction des Graphe, Map et Label précédents
    global frameCanvas, f, map_widget, frameLabelText, answer, new_df
    try:
        print(1)
        frameLabelText.destroy()
        frameCanvas.destroy()
        map_widget.destroy()
    except:
        pass


    if data[0] == 'TOUS' and data[1] == 'TOUS' and data[2] == "Quantité":

        #CREATION DU GRAPH------------------------------------------------------
        font = {'family' : 'normal','size'   : 5}
        sns.set(style="white")
        dataQ1 = new_df
        dataQ1 = dataQ1.assign(COUNT=1)
        dataQ1 = (pandas.crosstab(dataQ1['ARRONDISSEMENT'], dataQ1['COUNT']))
        dataQ1.columns=['COUNT']
        listeArrdt = dataQ1.index.tolist()
        dataQ1.insert(0, "ARRONDISSEMENT", listeArrdt)
        plt.figure(figsize = (16, 9))
        plt.rc('font', **font)
        f, ax = plt.subplots(figsize=(12, 9))
        f.subplots_adjust(bottom=0.30)
        plt.xticks(rotation=80)
        plt.gcf().set_size_inches(5, 5)
        plt.xlabel('ARRONDISSEMENT')
        sns.barplot(x = 'ARRONDISSEMENT', y = 'COUNT',data = dataQ1)

        AfficheframeCanvas()


        #CREATION DE LA MAP ----------------------------------------------------
        # create map widget
        dataQ1 = new_df
        map_widget = TkinterMapView(frameTheMap, width=400, height=400, corner_radius=0)
        map_widget.pack(  pady = 10, padx = 10, side=RIGHT)

        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Zone affichée de la carte = PARIS
        map_widget.set_position(48.860381, 2.338594)

        # Zoom
        map_widget.set_zoom(11)

        #marqueurs =[]
        marqueurs = {}
        zone = []
        nom_arrond_max = dataQ1["ARRONDISSEMENT"].value_counts().idxmax(axis=0)
        nom_arrond_min = dataQ1["ARRONDISSEMENT"].value_counts().idxmin(axis=0)
        if nom_arrond_max in localisation:

            marqueurs[nom_arrond_max] = localisation[nom_arrond_max]
            zone.append(appartenance[nom_arrond_max])

        if nom_arrond_min in localisation:
            marqueurs[nom_arrond_min] = localisation[nom_arrond_min]
            zone.append(appartenance [nom_arrond_min])

        affiche_map(marqueurs, zone)


        #CREATION DU TEXTE -----------------------------------------------------
        nbr_arrMax = new_df["ARRONDISSEMENT"].value_counts().max()
        nbr_arrMin = dataQ1["ARRONDISSEMENT"].value_counts().min()

        answer = f"L'arrondissement avec le plus d'arbre est {nom_arrond_max} comptant un total de {nbr_arrMax} arbre.\n\nCelui avec le moins d'arbre est {nom_arrond_min} avec un total de {nbr_arrMin} arbre."
        AfficheframeLabelText()



    if data[0] == 'TOUS' and data[1] == 'TOUS' and data[2] == "Hauteur":

        #CREATION DU GRAPH------------------------------------------------------

        dataQ1 = new_df
        dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
        dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)

        g = dataQ1.groupby('ARRONDISSEMENT')
        dataQ2 = g[['HAUTEUR (m)']].agg([pandas.Series.mean, pandas.Series.max, pandas.Series.min,pandas.Series.count])
        listarro=dataQ2.index.tolist()
        dataQ2.columns=['MEAN', 'MAX', 'MIN','COUNT']
        dataQ2.insert(0,"ARRONDISSEMENT",listarro)

        f, ax = plt.subplots(figsize=(5,5))
        sns.set_color_codes("pastel")
        sns.barplot(x="MAX", y="ARRONDISSEMENT", data=dataQ2, label='Maximum', color="b")


        sns.set_color_codes("muted")
        sns.barplot(x='MEAN', y='ARRONDISSEMENT', data=dataQ2, label="Average", color="g")

        sns.set_color_codes("bright")
        sns.barplot(x="MIN", y="ARRONDISSEMENT", data=dataQ2, label='minimum', color="b")

        ax.legend(ncol=3, loc="upper right", frameon=True)
        ax.set(ylim=(-2,26),xlim=(-1, 60), ylabel="Arrondissement", xlabel="hauteur")
        sns.despine(right=True, top=True)

        AfficheframeCanvas()



        #CREATION DU TEXTE -----------------------------------------------------

        taille = dataQ1.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].max().sort_values(ascending = False).tolist()[0]
        arr = dataQ1.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].max().sort_values(ascending = False).keys().tolist()[0]
        tailleMin = dataQ1.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].min().sort_values(ascending = False).tolist()[-1]
        arr_min = dataQ1.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].min().sort_values(ascending = False).keys().tolist()[-1]
        dgMax = dataQ1.query('`HAUTEUR (m)` == @taille')
        dgMin = dataQ1.query('`HAUTEUR (m)` == @tailleMin')
        boucleMax = dgMax.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].max().sort_values(ascending = False)
        boucleMin = dgMin.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].min().sort_values(ascending = False)


        print(f"Les arbres les plus hauts font {taille} m et se trouve dans :")

        arrdtMax = ""
        arrdtMin = ""
        for i in range(len(boucleMax)):
            arrdtMax = f"{arrdtMax}\n{dgMax.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].max().sort_values(ascending = False).keys().tolist()[i]}"
            #arrdtMax.append(f"{dgMax.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].max().sort_values(ascending = False).keys().tolist()[i]}, ")
            #print(dgMax.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].max().sort_values(ascending = False).keys().tolist()[i])

        print(f"Les arbres les plus petits font {tailleMin}m et se trouves dans:")

        for i in range(len(boucleMin)):
            arrdtMin = f"{arrdtMin}\n{dgMin.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].min().sort_values(ascending = False).keys().tolist()[i]}"
            #arrdtMin.append(f"{dgMin.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].min().sort_values(ascending = False).keys().tolist()[i]}, ")
            #print(dgMin.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].min().sort_values(ascending = False).keys().tolist()[i])

        answer = f"Les arbres les plus hauts font {taille} m et se trouvent dans : {arrdtMax}.\n\nLes arbres les plus petits font {tailleMin} m et se trouvent dans : {arrdtMin}"

        AfficheframeLabelText()


        #CREATION DE LA MAP ----------------------------------------------------
        # L'arbre le plus haut et le plus bas de chaque arrdt
        # create map widget
        map_widget = TkinterMapView(frameTheMap, width=400, height=400, corner_radius=0)
        map_widget.pack(  pady = 10, padx = 10, side=RIGHT)

        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Zone affichée de la carte = PARIS
        map_widget.set_position(48.860381, 2.338594)

        # Zoom
        map_widget.set_zoom(13)

        groupe = dataQ1.groupby("ARRONDISSEMENT")
        hauteur = []
        latitude = []
        longitude = []
        arbre = []
        marqueurs = {}
        for arrdt in groupe:
            arrdtTemp = arrdt[1].sort_values(by="HAUTEUR (m)")

            arbre.append(arrdtTemp.iloc[-1 , 4])
            hauteur.append(pandas.Series.max(arrdtTemp['HAUTEUR (m)']))
            latitude.append(arrdtTemp.iloc[-1 , 8])
            longitude.append(arrdtTemp.iloc[-1 , 9])

            arbre.append(arrdtTemp.iloc[0 , 4])
            hauteur.append(pandas.Series.min(arrdtTemp['HAUTEUR (m)']))
            latitude.append(arrdtTemp.iloc[0 , 8])
            longitude.append(arrdtTemp.iloc[0 , 9])


        for i in range(len(arbre)):
            marqueurs[f"{arbre[i]}, {hauteur[i]}m"] = [latitude[i], longitude[i]]

        affiche_map(marqueurs)



    if data[0] == 'TOUS' and data[1] == 'TOUS' and data[2] == "Type":

        #CREATION DU GRAPH------------------------------------------------------

        df1=new_df["LIBELLE FRANCAIS"].value_counts().tolist()
        df2=new_df["LIBELLE FRANCAIS"].value_counts().keys().tolist()

        dataQ3={"espece":df2,"valeur":df1}
        dataQ3 = pandas.DataFrame(dataQ3, columns=['espece','valeur'])
        dataQ3['pourcentage'] = 100*(dataQ3.valeur/ dataQ3.valeur.sum())
        datatemp=pandas.DataFrame(columns=['espece', 'valeur', 'pourcentage'])
        espece=[]
        valeur=[]
        pourcentage=[]
        compteur=0
        temp=0
        for i in range(len(dataQ3)):
            if dataQ3.pourcentage[i] > 2:
                #print(dataQ3.pourcentage[i])
                espece.append(dataQ3.espece[i])
                valeur.append(dataQ3.valeur[i])
                pourcentage.append(dataQ3.pourcentage[i])
            else:
                temp = temp + dataQ3.pourcentage[i]
                compteur=compteur+dataQ3.valeur[i]

        espece.append('Autres')
        pourcentage.append(temp)
        valeur.append(compteur)


        labels = espece
        sizes = pourcentage
        listeColors = ['#f8961e', '#f9844a', '#90be6d', '#43aa8b','#f9c74f','#277da1','#9f86c0','#84a98c','#d9ed92','#06d6a0', '#f1e3e4', '#f2d0a9']
        colors = ['#f94144']
        listeExplode = [0.2]
        for i in range(len(labels)-1):
            colors.append(listeColors[i])
            listeExplode.append(0)


        # Chaque cartile correspond à une valeur
        explode = listeExplode

        f = Figure() # create a figure object
        ax = f.add_subplot(111) # add an Axes to the figure
        plt.subplots(figsize=(12, 9))
        ax.pie(sizes, radius=1, labels=labels,autopct='%0.2f%%', shadow=True, colors=colors, explode=explode)
        #plt.gcf().set_size_inches(5, 5)

        #plt.figure(figsize=(5,5))
        #plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90,normalize=True)
        #f, ax = plt.subplots(figsize=(12, 9))
        #plt.axis('equal')
        #plt.savefig('PieChart02.png')
        #plt.show()


        AfficheframeCanvas()



        #CREATION DU TEXTE -----------------------------------------------------

        dataQ = new_df
        dataQ.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False)
        df_arrdMax2 = dataQ.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False).keys()[0]
        df_nbrMax2 = dataQ.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False)[0]
        df_arrdMin2 = dataQ.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False).keys()[-1]
        df_nbrMin2 = dataQ.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False)[-1]

        answer = f"L'arbre le plus présent dans tous les arrondissement confondus est le {df_arrdMax2} apparaissant {df_nbrMax2} fois\n\nL'arbre le moins présent dans tous les arrondissement confondus est le {df_arrdMin2} apparaissant { df_nbrMin2} fois"


        AfficheframeLabelText()



        #CREATION DE LA MAP ----------------------------------------------------
        # 10 arbres aléatoires par arrdt

        # create map widget
        dataQ1 = new_df
        map_widget = TkinterMapView(frameTheMap, width=400, height=400, corner_radius=0)
        map_widget.pack(  pady = 10, padx = 10, side=RIGHT)

        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Zone affichée de la carte = PARIS
        map_widget.set_position(48.860381, 2.338594)

        # Zoom
        map_widget.set_zoom(11)

        dataQ = new_df
        dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']>50], inplace=True)
        dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']<2], inplace=True)
        groupeArdt = dataQ.groupby("ARRONDISSEMENT")

        marqueurs = {}

        latitude = []
        longitude = []
        arbre = []

        for arrdt in groupeArdt:
            for i in range(10):
                marqueurs[f"{arrdt[1].iloc[i , 4]}"] = [arrdt[1].iloc[i , 8], arrdt[1].iloc[i , 9]]

        affiche_map(marqueurs)



    if data[0] == 'TOUS' and data[1] != 'TOUS' and data[2] == "Quantité":

        #CREATION DU GRAPH------------------------------------------------------
        font = {'family' : 'normal','size'   : 5}
        sns.set(style="white")
        dataQ1 = new_df
        dataQ1 = dataQ1.assign(COUNT=1)
        dataQ1 = dataQ1.loc[dataQ1['LIBELLE FRANCAIS']== data[1], :]
        dataQ1 = (pandas.crosstab(dataQ1['ARRONDISSEMENT'], dataQ1['COUNT']))
        dataQ1.columns=['COUNT']
        listeArrdt = dataQ1.index.tolist()
        dataQ1.insert(0, "ARRONDISSEMENT", listeArrdt)
        plt.figure(figsize = (16, 9))
        plt.rc('font', **font)
        f, ax = plt.subplots(figsize=(12, 9))
        f.subplots_adjust(bottom=0.30)
        plt.xticks(rotation=80)
        plt.gcf().set_size_inches(5, 5)
        plt.xlabel('ARRONDISSEMENT')
        sns.barplot(x = 'ARRONDISSEMENT', y = 'COUNT',data = dataQ1)

        AfficheframeCanvas()



        #CREATION DU TEXTE -----------------------------------------------------

        dg = new_df.query('`LIBELLE FRANCAIS` == @data[1]')

        df_maxArbre = dg["ARRONDISSEMENT"].value_counts().keys()[0]
        df_minArbre = dg["ARRONDISSEMENT"].value_counts().keys()[-1]
        df_nbrMaxArbre = dg["ARRONDISSEMENT"].value_counts()[0]
        df_nbrMinArbre = dg["ARRONDISSEMENT"].value_counts()[-1]

        answer = f"L'arrondissement qui compte le plus de {data[1]} est {df_maxArbre} avec {df_nbrMaxArbre} arbre(s).\n\nL'arrondissement qui compte le moins de {data[1]} est {df_minArbre} avec {df_nbrMinArbre} arbre(s)"
        #print(f"L'arrondissement qui compte le plus de {data[1]} est {df_maxArbre} avec {df_nbrMaxArbre} arbre(s).\n\nL'arrondissement qui compte le moins de {data[1]} est {df_minArbre} avec {df_nbrMinArbre} arbre(s)")

        AfficheframeLabelText()





        #CREATION DE LA MAP ----------------------------------------------------
        # 10 arbres aléatoires par arrdt

        # create map widget
        dataQ1 = new_df
        map_widget = TkinterMapView(frameTheMap, width=400, height=400, corner_radius=0)
        map_widget.pack(  pady = 10, padx = 10, side=RIGHT)

        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Zone affichée de la carte = PARIS
        map_widget.set_position(48.860381, 2.338594)

        # Zoom
        map_widget.set_zoom(13)

        dataQ = new_df
        #dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']>50], inplace=True)
        #dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']<2], inplace=True)
        dataQ = dataQ.loc[dataQ['LIBELLE FRANCAIS']== data[1], :]
        dataQ.head()

        groupeArdt = dataQ.groupby("ARRONDISSEMENT")

        marqueurs = {}

        latitude = []
        longitude = []
        arbre = []

        #Marqueurs sur tous les arbres select pour tous les ardt limité à 10
        for arrdt in groupeArdt:
            print(len(arrdt[1]))
            for i in range(0,min(10, len(arrdt[1]))):
                marqueurs[f"{arrdt[0]} - {arrdt[1].iloc[i , 4]} - {i+1}"] = [arrdt[1].iloc[i , 8], arrdt[1].iloc[i , 9]]

        affiche_map(marqueurs)



    if data[0] != 'TOUS' and data[1] == 'TOUS' and data[2] == "Quantité":

        #CREATION DU GRAPH------------------------------------------------------

        dataQ1 = new_df.loc[new_df['ARRONDISSEMENT']== data[0], :]
        df1=dataQ1["LIBELLE FRANCAIS"].value_counts().tolist()
        df2=dataQ1["LIBELLE FRANCAIS"].value_counts().keys().tolist()

        dataQ3={"espece":df2,"valeur":df1}
        dataQ3 = pandas.DataFrame(dataQ3, columns=['espece','valeur'])
        dataQ3['pourcentage'] = 100*(dataQ3.valeur/ dataQ3.valeur.sum())
        datatemp=pandas.DataFrame(columns=['espece', 'valeur', 'pourcentage'])
        espece=[]
        valeur=[]
        pourcentage=[]
        compteur=0
        temp=0
        for i in range(len(dataQ3)):
            if dataQ3.pourcentage[i] > 2:
                #print(dataQ3.pourcentage[i])
                espece.append(dataQ3.espece[i])
                valeur.append(dataQ3.valeur[i])
                pourcentage.append(dataQ3.pourcentage[i])
            else:
                temp = temp + dataQ3.pourcentage[i]
                compteur=compteur+dataQ3.valeur[i]

        espece.append('Autres')
        pourcentage.append(temp)
        valeur.append(compteur)


        labels = espece
        sizes = pourcentage
        listeColors = ['#f8961e', '#f9844a', '#90be6d', '#43aa8b','#f9c74f','#277da1','#9f86c0','#84a98c','#d9ed92','#06d6a0', '#f1e3e4', '#f2d0a9', '#f8961e', '#f9844a', '#90be6d', '#43aa8b','#f9c74f','#277da1','#9f86c0','#84a98c','#d9ed92','#06d6a0', '#f1e3e4', '#f2d0a9']
        colors = ['#f94144']
        listeExplode = [0.2]
        print('len(labels : ',len(labels) )
        for i in range(len(labels)-1):
            colors.append(listeColors[i])
            listeExplode.append(0)


        # Chaque cartile correspond à une valeur
        explode = listeExplode

        f = Figure() # create a figure object
        ax = f.add_subplot(111) # add an Axes to the figure
        plt.subplots(figsize=(12, 9))
        ax.pie(sizes, radius=1, labels=labels,autopct='%0.2f%%', shadow=True, colors=colors, explode=explode)
        #plt.gcf().set_size_inches(5, 5)

        #plt.figure(figsize=(5,5))
        #plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90,normalize=True)
        #f, ax = plt.subplots(figsize=(12, 9))
        #plt.axis('equal')
        #plt.savefig('PieChart02.png')
        #plt.show()

        AfficheframeCanvas()



        #CREATION DE LA MAP ----------------------------------------------------
        # 10 arbres aléatoires pour l'arrdt select

       # create map widget
        dataQ1 = new_df
        map_widget = TkinterMapView(frameTheMap, width=400, height=400, corner_radius=0)
        map_widget.pack(  pady = 10, padx = 10, side=RIGHT)

        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Zone affichée de la carte = PARIS
        map_widget.set_position(localisation[data[0]][0], localisation[data[0]][1])

        # Zoom
        map_widget.set_zoom(13)

        dataQ1 = new_df
        dataQ = new_df
        #dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']>50], inplace=True)
        #dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']<2], inplace=True)
        dataQ = dataQ.loc[dataQ['ARRONDISSEMENT']== data[0], :]
        dataQ.head(100)

        # groupeArdt = dataQ.groupby("ARRONDISSEMENT")

        marqueurs = {}

        # latitude = []
        # longitude = []
        # arbre = []

        # #Marqueurs sur tous les arbres select pour tous les ardt limité à 50

        for i in range(0,min(100, len(dataQ))):
        #for i in range(0,len(dataQ)):
            marqueurs[f"{dataQ.iloc[i , 4]} - {i+1}"] = [dataQ.iloc[i , 8], dataQ.iloc[i , 9]]


        affiche_map(marqueurs)


        #CREATION DU TEXTE -----------------------------------------------------
        Arbre_df = new_df[(new_df['ARRONDISSEMENT']==data[0]) & (new_df['LIBELLE FRANCAIS'])]
        nom_df = Arbre_df["LIBELLE FRANCAIS"].value_counts().keys().tolist()[0]
        nbr_df = Arbre_df["LIBELLE FRANCAIS"].value_counts().tolist()[0]

        nom_df_min = Arbre_df["LIBELLE FRANCAIS"].value_counts().keys().tolist()[-1]
        nbr_df_min = Arbre_df["LIBELLE FRANCAIS"].value_counts().tolist()[-1]

        #print(f"L'arbre le plus présent dans {data[0] } est le {nom_df} avec {nbr_df} specimens\nL'arbre le moins présent dans {data[0]} est le {nom_df_min} avec seulement {nbr_df_min} specimen." )
        answer = (f"L'arbre le plus présent dans {data[0] } est le {nom_df} avec {nbr_df} specimens\nL'arbre le moins présent dans {data[0]} est le {nom_df_min} avec seulement {nbr_df_min} specimen." )
        AfficheframeLabelText()


def demande1():
    global data
    data=["TOUS", "TOUS", "Quantité"]
    apply()

def demande2():
    global data
    data=["TOUS", "TOUS", "Hauteur"]
    apply()

def demande3():
    global data
    data=["TOUS", "TOUS", "Type"]
    apply()



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
frameDemande = Frame(frameGauche, bg=color, height = 500, width=600)
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
frameBouton.pack(side=BOTTOM,  pady=20, padx=20)

boutonApply = Button(frameBouton, text="APPLY", command=apply)
boutonApply.pack(side=RIGHT, padx=40)

boutonQ1 = Button(frameBouton, text="Q1", command = demande1)
boutonQ1.pack(side=LEFT, padx=10)

boutonQ2 = Button(frameBouton, text="Q2", command = demande2)
boutonQ2.pack(side=LEFT, padx=10)

boutonQ3 = Button(frameBouton, text="Q3", command = demande3)
boutonQ3.pack(side=LEFT, padx=10)



#---------- BOTTOM : GRAPHE ----------


#frameGraph = Frame(frameGauche, bg='Black', height = 500, width = 500)
frameGraph = Frame(frameGauche, bg=color, height = 500, width = 600)
frameGraph.pack( fill=BOTH, expand=False)



#-----------------------------------------------------------------------
#                 FRAME DROITE
#-----------------------------------------------------------------------

#frameDroite = Frame(mainFenetre, bg='Green')
frameDroite = Frame(mainFenetre, bg=color)
frameDroite.pack(side=RIGHT, expand=True, fill=BOTH)

#---------- TOP : REPONSE TEXTE ----------

#frameReponseTexte = Frame(frameDroite, bg='Yellow')
frameReponseTexte = Frame(frameDroite, bg=color, width = 600)
frameReponseTexte.pack(side=TOP, fill=BOTH, expand=True)




#---------- BOTTOM : MAP  ----------

#frameMap = Frame(frameDroite, bg='White', height=500, width=500)
frameMap = Frame(frameDroite, bg=color, height=700, width=600)
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
    '''code permettant de centrer la fenêtre quand on la lance'''
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


center(mainFenetre)
mainFenetre.mainloop()