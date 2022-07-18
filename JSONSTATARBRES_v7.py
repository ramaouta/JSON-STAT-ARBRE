## WELCOME IN JSONSTATARBRES APP



from PIL import ImageTk

import PIL.Image


from tkinter import *
from tkinter import messagebox
import webbrowser
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
    'PARIS 20E ARRDT': [48.8654235,2.396509],
    'PARIS 19E ARRDT':[48.8868685,2.381091],
    'PARIS 18E ARRDT': [48.8912045,2.341435],
    'PARIS 17E ARRDT': [48.8855485,2.302854],
    'PARIS 16E ARRDT': [48.8604285,2.254432] ,
    'PARIS 15E ARRDT': [48.8406355,2.29135],
    'PARIS 14E ARRDT': [48.8322955,2.324793],
    'PARIS 13E ARRDT': [48.8297585,2.358486] ,
    'PARIS 12E ARRDT': [48.8378875,2.41616] ,
    'PARIS 11E ARRDT': [48.8605835,2.37619] ,
    'PARIS 10E ARRDT':[48.8779955,2.357376] ,
    'PARIS 9E ARRDT':[48.8777075,2.335891] ,
    'PARIS 8E ARRDT':[48.8735785,2.308818] ,
    'PARIS 7E ARRDT': [48.8547225,2.313494],
    'PARIS 6E ARRDT':[48.8500705,2.331655] ,
    'PARIS 5E ARRDT': [48.8446015,2.348577],
    'PARIS 4E ARRDT': [48.8552175,2.355629],
    'PARIS 3E ARRDT': [48.8631225,2.358078],
    'PARIS 2E ARRDT': [48.8688755,2.340391],
    'PARIS 1ER ARRDT':[48.8630235,2.333578],
    'CENTRE DE PARIS' : [48.8589465,2.2768229],
    'HAUTS-DE-SEINE':[48.8238055,2.216476],
    'BOIS DE BOULOGNE': [48.8626564,2.2466912],
    'BOIS DE VINCENNES': [48.8284295,2.441433],
    'SEINE-SAINT-DENIS': [48.9155755,2.490996],
    'VAL-DE-MARNE': [48.7839795,2.468223],
}

# Dictionnaire de correspondance csv new_arbres / csv arrondissements
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
    'PARIS 1ER ARRDT': 1,
    'BOIS DE BOULOGNE': 16,
    'BOIS DE VINCENNES': 12,
    }

# Dictionnaire de correspondance csv new_arbres / csv départements ...
departement = {
    'HAUTS-DE-SEINE':"HAUTS DE SEINE",
    'SEINE-SAINT-DENIS': "SEINE SAINT DENIS",
    'VAL-DE-MARNE': "VAL DE MARNE"
    }

color = "#3A5F0B"
colorb = '#CCFFBB'
colort = "black"
colorg = '#E9D79E'
colorm = '#E08F4B'


# les variables xxxIsVisible servent à afficher ou effacer les listes box (dans la partie demande) au clic sur le bouton correspondant
arrdtIsVisible = False
arbreIsVisible = False
critereIsVisible = False

# Création d'une variable data correspondant au choix de l'utilisateur. Format : ["Arrpndissement", "Arbre", "Critère"]
data=["TOUS", "TOUS", "Quantité"]


# Initialisation des variables marqueurs et zone relatives à la MAP
marqueurs = {}
zone = []
# Initialisation d'une variable titreGraph pour les graph circulaire
titreGraph=" "

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#                 DATA
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


#Lecture des fichiers CSV
path = r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\new_arbres.csv"
new_df = pandas.read_csv(r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\new_arbres.csv", sep = ',', header = 0)
arr_df = pandas.read_csv(r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\arrondissements.csv", sep = ';', header = 0)
arr_departement = pandas.read_csv(r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\departements-et-collectivites-doutre-mer-france.csv", sep = ';', header = 0)

# Fichiers Image
imgArbre = PIL.Image.open("D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\ImgArbre.png")
imgFeuille = PIL.Image.open("D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\ImgFeuille.png")

# google api KEY

apiKey = "AIzaSyAgeWLaNWCpA42a7LBytovrZbHVLPZNYz8"


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

def separateurMilliers(n):
    ## Renvoi un nbre avec séparateur de milliers
    result = "{:,}".format(n).replace(',', ' ').replace('.', ',')
    return result


def affiche_map(marqueurs = {},zone = []):
    ## Affiche la carte avec les marqueurs et les zones
    global map_widget
    #numero d'arrondissement spec
    arr= []
    if type(marqueurs) == dict:
        for i, j  in marqueurs.items():
            arr.append(i)
            map_widget.set_marker(j[0], j[1] , text= i, marker_color_circle="#3a5a40", marker_color_outside="#a3b18a")

    for el in zone :
        map_widget.set_marker(localisation[el][0], localisation[el][1] , text= el)

        res = []
        polygo =[]

        if el in appartenance:
            a = arr_df.loc[(arr_df ["Numéro d’arrondissement"] == appartenance[el] ) & (arr_df["Geometry X Y"])]
            liste = a["Geometry"].to_list()
            string = liste[0][1:-1]
            # change une string en dictionnaire
            res = {key: (val) for key, val in (item.split(':') for item in string.split(', "'))}
            # la valeur de dico[clé] est une string
            # eval("string") → change la string en liste
            res = eval(res['"coordinates"'])
            res = res[0]
            #polygo =[]
        '''
        if el in departement:
            a = arr_departement.loc[(arr_departement ["Nom Officiel Département Majuscule"] == departement[el] ) & (arr_departement["viewport"])]
            liste = a["viewport"].to_list()
            string = liste[0][1:-1]
            # change une string en dictionnaire
            res = {key: (val) for key, val in (item.split(':') for item in string.split(', "'))}
            # la valeur de dico[clé] est une string
            # eval("string") → change la string en liste
            res = eval(res['coordinates"'])
            res = res[0]
        '''
        if  len(res) > 0:
            for coord in res:
                points= [coord[1],coord[0]]
                polygo.append(tuple(points))
                #on a bien un dictionnaire avec des valeur en listes
            map_widget.set_polygon(polygo, name = "TTESTT")

#MANU
'''
def AfficheframeCanvas():
    ## Pack la frameCanvas dans frameGraph
    global f, frameCanvas, canvas
    frameCanvas = Frame(frameGraph, bg=color)
    frameCanvas.pack(fill=BOTH, expand=True)
    canvas = FigureCanvasTkAgg(f, master = frameCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack()

'''

#SEB
def AfficheframeCanvas():
    ## Pack la frameCanvas dans frameGraph pour afficher le graphique
    global f, frameCanvas
    frameCanvas = Frame(frameGraph, bg=colorg, width=400, height=354)
    labelTitre = Label(frameCanvas, text=titreGraph, bg=colorg, font=("Arial", 13))
    labelTitre.pack()
    frameCanvas.pack(fill=BOTH, expand=True)
    canvas = FigureCanvasTkAgg(f, master = frameCanvas)
    canvas.draw()
    frameCanvas.pack_propagate(False)
    canvas.get_tk_widget().pack()


#MANU
'''
def AfficheframeLabelText():
    ## Pack la frameLabelText dans frameReponseTexte
    global answer, frameLabelText, frameLabelImage
    frameLabelImage = Label(frameReponseTexte, image = img)
    frameLabelImage.pack(side = LEFT, fill=BOTH, expand=True)
    frameLabelText = Label(frameReponseTexte, text=answer, bg=colorb, fg="black")
    frameLabelText.place(relx=.5, rely=.5,anchor= CENTER)
'''

#SEB
def AfficheframeLabelText():
    ## Pack la frameLabelText dans frameReponseTexte pour afficher la reponse texte
    global answer, frameLabelText, frameLabelImage
    frameLabelImage = Label(frameReponseTexte, image = img)
    frameLabelImage.pack(side = LEFT, fill=BOTH, expand=True)
    frameLabelText = Label(frameLabelImage, text=answer, bg=colorb)
    frameLabelText.place(relx=.5, rely=.5,anchor= CENTER)

def noData():
    ## Affiche message "noData dans carte, map et text
    global frameCanvas, answer, frameLabelText, frameLabelImage, frameTheMap, map_widget
    frameCanvas = Frame(frameGraph, bg=colorg, width=400, height=354)
    frameCanvas.pack(fill=BOTH, expand=True)
    label = Label(frameCanvas, text="Aucune donnée ne correspond à votre recherche")
    label.pack()

    frameLabelImage = Label(frameReponseTexte, image = img)
    frameLabelImage.pack(side = LEFT, fill=BOTH, expand=True)
    frameLabelText = Label(frameLabelImage, text="Aucune donnée ne correspond à votre recherche", bg=colorb)
    frameLabelText.place(relx=.5, rely=.5,anchor= CENTER)

    map_widget = Frame(frameTheMap, bg=colorm, width=400, height=354)
    map_widget.pack(fill=BOTH, expand=True)
    label2 = Label(map_widget, text="Aucune donnée ne correspond à votre recherche")
    label2.pack()



def apply():
    ## Affiche les réponses, graphes et map relatifs à la demande

    # A chaque demande de l'utilisateur : Destruction des Graphe, Map et Label précédents
    global frameCanvas, f, map_widget, frameLabelText, answer, new_df, frameLabelImage, frameImage, marqueurs, zone, data, titreMap, titreGraph
    try:
        frameImage.destroy()
        #titreMap.destroy()
        frameCanvas.destroy()
        frameLabelText.destroy()
        map_widget.destroy()
        frameLabelText.destroy()
        frameLabelImage.destroy()
        zone=[]
        marqueurs={}
    except:
        pass

    #[TOUS, TOUS, Quantité] = Q1
    if data[0] == 'TOUS' and data[1] == 'TOUS' and data[2] == "Quantité":

        test_df = pandas.read_csv(path, sep = ',', header = 0)
        count=len(test_df)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']>50], inplace=True)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']<2], inplace=True)
        if len(test_df) == 0:
            noData()
        else:

            #CREATION DU GRAPH------------------------------------------------------
            font = {'family' : 'Arial','size'   : 7}                                # Définition de la police et taille de police des axes
            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            dataQ1 = dataQ1.assign(COUNT=1)
            dataQ1 = (pandas.crosstab(dataQ1['ARRONDISSEMENT'], dataQ1['COUNT']))
            dataQ1.columns=['COUNT']
            listeArrdt = dataQ1.index.tolist()
            dataQ1.insert(0, "ARRONDISSEMENT", listeArrdt)
            plt.figure(figsize = (16, 9))
            plt.rc('font', **font)                                                  # Application de la police et taille de police des axes
            f, ax = plt.subplots(figsize=(12, 9))
            f.patch.set_facecolor(colorg)                                           # Couleur de fond de "l'image" graphe
            ax.set_facecolor('black')                                               # Couleur de fond du graphe
            plt.xticks(rotation=85)
            plt.xlabel('ARRONDISSEMENT', fontsize=12)                               # Titre de l'axe x et taille de police
            plt.ylabel('COUNT', fontsize=8)                                         # Titre de l'axe y et taille de police
            f.subplots_adjust(bottom=0.40)                                          # Espace entre le bas du graphe et le bas de "l'image" graphe
            plt.gcf().set_size_inches(8, 8)                                         # Taille de "l'image" graphe
            sns.barplot(x = 'ARRONDISSEMENT', y = 'COUNT',data = dataQ1)
            plt.title(f"Quantité d'arbres par arrondissement", fontsize=13)         # Titre du graphique

            #sns.set(style="white")
            #f.subplots_adjust(bottom=0.30)
            titreGraph=""
            AfficheframeCanvas()


            #CREATION DE LA MAP ----------------------------------------------------
            # create map widget
            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            map_widget = TkinterMapView(frameTheMap, width=600, height=400, corner_radius=20)
            map_widget.pack(  pady = 10, padx = 10)

            map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

            # Zone affichée de la carte = PARIS
            map_widget.set_position(48.860381, 2.338594)

            # Zoom
            map_widget.set_zoom(11)

            marqueurs = {}
            zone = []
            nom_arrond_max = dataQ1["ARRONDISSEMENT"].value_counts().idxmax(axis=0)
            nom_arrond_min = dataQ1["ARRONDISSEMENT"].value_counts().idxmin(axis=0)
            if nom_arrond_max in localisation:

                marqueurs[nom_arrond_max] = localisation[nom_arrond_max]
                #zone.append(appartenance[nom_arrond_max])
                zone.append(nom_arrond_max)

            if nom_arrond_min in localisation:
                marqueurs[nom_arrond_min] = localisation[nom_arrond_min]
                #zone.append(appartenance [nom_arrond_min])
                zone.append(nom_arrond_min)
            affiche_map(marqueurs, zone)


            #CREATION DU TEXTE -----------------------------------------------------
            new_df = pandas.read_csv(path , sep = ',', header = 0)
            nbr_arrMax = new_df["ARRONDISSEMENT"].value_counts().max()
            nbr_arrMin = new_df["ARRONDISSEMENT"].value_counts().min()

            answer = f"\nIl y a {separateurMilliers(count)} arbres dans Paris et les départements dispo \n\nL'arrondissement avec le plus d'arbres est {nom_arrond_max} comptant un total de {separateurMilliers(nbr_arrMax)} arbres.\n\nCelui avec le moins d'arbres est {nom_arrond_min} avec un total de {separateurMilliers(nbr_arrMin)} arbres.\n"
            AfficheframeLabelText()


    #[TOUS, 1, Quantité]
    if data[0] == 'TOUS' and data[1] != 'TOUS' and data[2] == "Quantité":

        test_df = pandas.read_csv(path, sep = ',', header = 0)
        count=len(test_df.loc[test_df['LIBELLE FRANCAIS']== data[1], :])
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']>50], inplace=True)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']<2], inplace=True)
        test_df = test_df.loc[test_df['LIBELLE FRANCAIS']== data[1], :]
        if len(test_df) == 0:
            noData()
        else:

            #CREATION DU GRAPH------------------------------------------------------
            font = {'family' : 'normal','size'   : 7}
            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            dataQ1 = dataQ1.assign(COUNT=1)
            dataQ1 = dataQ1.loc[dataQ1['LIBELLE FRANCAIS']== data[1], :]
            dataQ1 = (pandas.crosstab(dataQ1['ARRONDISSEMENT'], dataQ1['COUNT']))
            dataQ1.columns=['COUNT']
            listeArrdt = dataQ1.index.tolist()
            dataQ1.insert(0, "ARRONDISSEMENT", listeArrdt)
            plt.figure(figsize = (16, 9))
            plt.rc('font', **font)
            f, ax = plt.subplots(figsize=(12, 9))
            #f.subplots_adjust(bottom=0.30)
            f.patch.set_facecolor(colorg)
            ax.set_facecolor('black')
            plt.xticks(rotation=85)
            plt.xlabel('ARRONDISSEMENT', fontsize=12)
            plt.ylabel('COUNT', fontsize=8)
            f.subplots_adjust(bottom=0.40)
            plt.gcf().set_size_inches(8, 8)
            sns.barplot(x = 'ARRONDISSEMENT', y = 'COUNT',data = dataQ1)
            plt.title(f'Quantité de "{data[1]}" par arrondissement', fontsize=13)
            titreGraph=""
            AfficheframeCanvas()


            #CREATION DU TEXTE -----------------------------------------------------
            new_df = pandas.read_csv(path , sep = ',', header = 0)
            dg = new_df.query('`LIBELLE FRANCAIS` == @data[1]')

            df_maxArbre = dg["ARRONDISSEMENT"].value_counts().keys()[0]
            df_minArbre = dg["ARRONDISSEMENT"].value_counts().keys()[-1]
            df_nbrMaxArbre = dg["ARRONDISSEMENT"].value_counts()[0]
            df_nbrMinArbre = dg["ARRONDISSEMENT"].value_counts()[-1]

            answer = f"\nIl y a {separateurMilliers(count)} {data[1].upper()} dans Paris et les départements dispo \n\nL'arrondissement qui compte le plus de {data[1]} est {df_maxArbre} avec {separateurMilliers(df_nbrMaxArbre)} arbre(s).\n\nL'arrondissement qui compte le moins de {data[1]} est {df_minArbre} avec {separateurMilliers(df_nbrMinArbre)} arbre(s)\n"

            AfficheframeLabelText()





            #CREATION DE LA MAP ----------------------------------------------------
            # 10 arbres aléatoires par arrdt

            # create map widget
            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            map_widget = TkinterMapView(frameTheMap, width=600, height=400, corner_radius=20)
            map_widget.pack(  pady = 10, padx = 10)

            map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

            # Zone affichée de la carte = PARIS
            map_widget.set_position(48.860381, 2.338594)

            # Zoom
            map_widget.set_zoom(11)

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

            #Marqueurs sur tous les arbres select pour tous les ardt limité à 20
            for arrdt in groupeArdt:
                for i in range(0,min(20, len(arrdt[1]))):
                    marqueurs[f"{arrdt[0]} - {arrdt[1].iloc[i , 4]} - {i+1}"] = [arrdt[1].iloc[i , 8], arrdt[1].iloc[i , 9]]

            affiche_map(marqueurs)


    #[1, TOUS, Quantité]
    if data[0] != 'TOUS' and data[1] == 'TOUS' and data[2] == "Quantité":

        test_df = pandas.read_csv(path, sep = ',', header = 0)
        count=len(test_df.loc[test_df['ARRONDISSEMENT']== data[0], :])
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']>50], inplace=True)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']<2], inplace=True)
        test_df = test_df.loc[test_df['ARRONDISSEMENT']== data[0], :]
        if len(test_df) == 0:
            noData()
        else:

            #CREATION DU GRAPH------------------------------------------------------
            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            dataQ1 = dataQ1.loc[dataQ1['ARRONDISSEMENT']== data[0], :]
            df1=dataQ1["LIBELLE FRANCAIS"].value_counts().tolist()
            df2=dataQ1["LIBELLE FRANCAIS"].value_counts().keys().tolist()
            font = {'family' : 'Arial','size' : 8}

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
            for i in range(len(labels)-1):
                colors.append(listeColors[i])
                listeExplode.append(0)


            # Chaque cartile correspond à une valeur
            explode = listeExplode



            f = Figure(figsize=(5, 4), dpi=100) # create a figure object
            ax = f.add_subplot(111) # add an Axes to the figure
            plt.subplots(figsize=(12, 9))
            plt.rc('font', **font)
            ax.pie(sizes, radius=1, labels=labels,autopct='%0.2f%%', shadow=True, colors=colors, explode=explode)
            plt.gcf().set_size_inches(5, 5)
            f.patch.set_facecolor(colorg)

            #plt.figure(figsize=(5,5))
            #plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90,normalize=True)
            #f, ax = plt.subplots(figsize=(12, 9))
            #plt.axis('equal')
            #plt.savefig('PieChart02.png')
            #plt.show()

            titreGraph = f"Quantité d'arbres dans {data[0].upper()}"
            AfficheframeCanvas()



            #CREATION DE LA MAP ----------------------------------------------------
            # 10 arbres aléatoires pour l'arrdt select

           # create map widget
            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            map_widget = TkinterMapView(frameTheMap, width=600, height=400, corner_radius=20)
            map_widget.pack(  pady = 10, padx = 10,)

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
            new_df = pandas.read_csv(path , sep = ',', header = 0)
            Arbre_df = new_df[(new_df['ARRONDISSEMENT']==data[0]) & (new_df['LIBELLE FRANCAIS'])]
            nom_df = Arbre_df["LIBELLE FRANCAIS"].value_counts().keys().tolist()[0]
            nbr_df = Arbre_df["LIBELLE FRANCAIS"].value_counts().tolist()[0]

            nom_df_min = Arbre_df["LIBELLE FRANCAIS"].value_counts().keys().tolist()[-1]
            nbr_df_min = Arbre_df["LIBELLE FRANCAIS"].value_counts().tolist()[-1]

            answer = (f"\nIl y a {separateurMilliers(count)} arbres dans {data[0].upper()} \n\nL'arbre le plus présent dans {data[0] } est le {nom_df} avec {separateurMilliers(nbr_df)} specimen\n\nL'arbre le moins présent dans {data[0]} est le {nom_df_min} avec seulement {separateurMilliers(nbr_df_min)} specimen.\n" )
            AfficheframeLabelText()


    #[1, 1, Quantité]
    if data[0] != 'TOUS' and data[1] != 'TOUS' and data[2] == "Quantité" :

        test_df = pandas.read_csv(path, sep = ',', header = 0)
        count=len(test_df.loc[   (test_df['ARRONDISSEMENT']== data[0]) & (test_df['LIBELLE FRANCAIS']== data[1]), :])
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']>50], inplace=True)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']<2], inplace=True)
        test_df = test_df.loc[test_df['ARRONDISSEMENT']== data[0], :]
        test_df = test_df.loc[test_df['LIBELLE FRANCAIS']== data[1], :]
        if len(test_df) == 0:
            noData()
        else:

            #CREATION DU GRAPH------------------------------------------------------
            font = {'family' : 'Arial','size' : 8}
            sns.set(style="white")

            new_df = pandas.read_csv(path , sep = ',', header = 0)
            nbr_arbre_spec =len(new_df.loc[(new_df['ARRONDISSEMENT'] == data[0]) & (new_df['LIBELLE FRANCAIS']==data[1])])
            dataQ1 = new_df.loc[new_df['ARRONDISSEMENT']== data[0], :]

            tous_les_arbres = len(dataQ1)

            sizes = [nbr_arbre_spec , tous_les_arbres-nbr_arbre_spec ]
            labels = [data[1], 'autre']

            colors = sns.color_palette("husl", 2)
            explode = (0, 0.2)
            f = Figure(figsize=(5, 4), dpi=100) # create a figure object
            ax = f.add_subplot(111) # add an Axes to the figure
            plt.subplots(figsize=(12, 9))
            plt.rc('font', **font)
            plt.gcf().set_size_inches(5, 5)

            def libel (pct, allvalues):
                nbr = int(pct / 100.*np.sum(allvalues))  #5315
                return '{:0.0f}%\n \n {:d}'.format(pct, nbr)

            ax.pie(sizes, radius=1, labels=labels,autopct=lambda pct: libel(pct, sizes), shadow=True, colors=colors, explode=explode)
            f.patch.set_facecolor(colorg)
            titreGraph=f"Quantité de {data[1].upper()} dans {data[0].upper()}"
            AfficheframeCanvas()

            #CREATION DE LA MAP ----------------------------------------------------
            # create map widget
            new_df_data = pandas.read_csv(path , sep = ',', header = 0)
            map_widget = TkinterMapView(frameTheMap, width=600, height=400, corner_radius=20)
            map_widget.pack(  pady = 10, padx = 10)

            map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

            # Zone affichée de la carte = PARIS
            #map_widget.set_position(48.860381, 2.338594)
            map_widget.set_position(localisation[data[0]][0],localisation[data[0]][1])
            # Zoom
            map_widget.set_zoom(13)


            marqueurs = {}
            zone = []

            a = new_df.loc[:,['LIBELLE FRANCAIS' ,'LATITUDE' ,'LONGITUDE' ]]

            coord = a.loc[(new_df_data['ARRONDISSEMENT'] == data[0] )&(new_df_data['LIBELLE FRANCAIS'] == data[1] )]

            for i , row in coord.iterrows():
                coordonner = []
                coordonner.append(row['LATITUDE']) ; coordonner.append(row['LONGITUDE'])
                #arrond_index= str(data[0])+"_"+str(i)
                #type_index =
                marqueurs[str(data[1])+"_"+str(i)] = coordonner

            zone.append(data[0])
            affiche_map(marqueurs, zone)

            #CREATION DU TEXTE ----------------------------------------------------


            new_df_Q2 = pandas.read_csv(path , sep = ',', header = 0)
            #new_df_Q2.drop(new_df_Q2.index[new_df_Q2['HAUTEUR (m)']>50], inplace=True)
            #new_df_Q2.drop(new_df_Q2.index[new_df_Q2['HAUTEUR (m)']<2], inplace=True)

            dg = new_df_Q2.query('`ARRONDISSEMENT` == @data[0] & `LIBELLE FRANCAIS` == @data[1]')
            nbr = dg["ARRONDISSEMENT"].value_counts().max()

            answer = f"\nDans  {data[0]} il y a {nbr} arbre(s) de type {data[1].upper()}.\n"

            AfficheframeLabelText()


    #[TOUS, TOUS, Hauteur] = Q2
    if data[0] == 'TOUS' and data[1] == 'TOUS' and data[2] == "Hauteur":


        test_df = pandas.read_csv(path, sep = ',', header = 0)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']>50], inplace=True)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']<2], inplace=True)
        if len(test_df) == 0:
            noData()
        else:

            #CREATION DU GRAPH------------------------------------------------------

            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
            dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)
            font = {'family' : 'Arial','size' : 7}

            #dataQ1 = dataQ1.loc[dataQ1['LIBELLE FRANCAIS']== data[1], :]
            df_nbrMax = dataQ1.groupby(['ARRONDISSEMENT'], sort=True)['HAUTEUR (m)'].max().sort_values(ascending=False).tolist()[0]

            g = dataQ1.groupby('ARRONDISSEMENT')
            dataQ2 = g[['HAUTEUR (m)']].agg([pandas.Series.mean, pandas.Series.max, pandas.Series.min,pandas.Series.count])
            listarro=dataQ2.index.tolist()
            dataQ2.columns=['MEAN', 'MAX', 'MIN','COUNT']
            dataQ2.insert(0,"ARRONDISSEMENT",listarro)


            f, ax = plt.subplots(figsize=(12, 9))
            plt.rc('font', **font)

            sns.set_color_codes("pastel")
            sns.barplot(y="MAX", x="ARRONDISSEMENT", data=dataQ2, label='Maximum', color="b")

            sns.set_color_codes("muted")
            sns.barplot(y='MEAN', x='ARRONDISSEMENT', data=dataQ2, label="Average", color="g")

            sns.set_color_codes("bright")
            sns.barplot(y="MIN", x="ARRONDISSEMENT", data=dataQ2, label='Minimum', color="b")

            ax.legend(ncol=3, loc="upper right", frameon=True, fontsize='medium')
            ax.set(xlim=(-2,len(listarro)+1),ylim=(-1, df_nbrMax*1.2), xlabel="Arrondissement", ylabel="hauteur")
            plt.xlabel('ARRONDISSEMENT', fontsize=12)                               # Titre de l'axe x et taille de police
            plt.ylabel('', fontsize=8)
            plt.rc('font', **font)
            plt.xticks(rotation=85)
            sns.despine(right=True, top=True)
            f.patch.set_facecolor(colorg)
            ax.set_facecolor('black')
            plt.gcf().set_size_inches(8, 8)
            f.subplots_adjust(bottom=0.40)
            plt.title(f"Hauteur mini, moyenne et maxi des arbres par arrondissement", fontsize=11)

            titreGraph=""
            AfficheframeCanvas()




            #CREATION DU TEXTE -----------------------------------------------------

            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
            dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)
            taille = dataQ1.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].max().sort_values(ascending = False).tolist()[0]
            arr = dataQ1.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].max().sort_values(ascending = False).keys().tolist()[0]
            tailleMin = dataQ1.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].min().sort_values(ascending = False).tolist()[-1]
            arr_min = dataQ1.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].min().sort_values(ascending = False).keys().tolist()[-1]
            dgMax = dataQ1.query('`HAUTEUR (m)` == @taille')
            dgMin = dataQ1.query('`HAUTEUR (m)` == @tailleMin')
            boucleMax = dgMax.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].max().sort_values(ascending = False)
            boucleMin = dgMin.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].min().sort_values(ascending = False)

            arrdtMax = ""
            arrdtMin = ""
            for i in range(len(boucleMax)):
                zone.append(dgMax.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].max().sort_values(ascending = False).keys().tolist()[i])
                arrdtMax = f"{dgMax.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].max().sort_values(ascending = False).keys().tolist()[i]}, {arrdtMax} "
                #arrdtMax.append(f"{dgMax.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].max().sort_values(ascending = False).keys().tolist()[i]}, ")


            for i in range(len(boucleMin)):
                if i%3 !=0:
                    arrdtMin = f"{dgMin.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].min().sort_values(ascending = False).keys().tolist()[i]}, {arrdtMin}"
                else:
                    arrdtMin = f"\n{dgMin.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].min().sort_values(ascending = False).keys().tolist()[i]}, {arrdtMin}"

            answer = f"Les arbres les plus hauts font {taille} m et se trouvent dans : {arrdtMax}.\n\nLes arbres les plus petits font {tailleMin} m et se trouvent dans : {arrdtMin}"

            AfficheframeLabelText()


            #CREATION DE LA MAP ----------------------------------------------------
            # L'arbre le plus haut et le plus bas de chaque arrdt
            # create map widget
            map_widget = TkinterMapView(frameTheMap, width=600, height=400, corner_radius=20)
            map_widget.pack(  pady = 10, padx = 10)

            map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

            # Zone affichée de la carte = PARIS
            map_widget.set_position(48.860381, 2.338594)

            # Zoom
            map_widget.set_zoom(11)
            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
            dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)
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
            affiche_map(marqueurs, zone)


    #[TOUS, 1, Hauteur]
    if data[0] == 'TOUS' and data[1] != 'TOUS' and data[2] == "Hauteur":

        test_df = pandas.read_csv(path, sep = ',', header = 0)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']>50], inplace=True)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']<2], inplace=True)
        test_df = test_df.loc[test_df['LIBELLE FRANCAIS']== data[1], :]
        if len(test_df) == 0:
            noData()
        else:

            #CREATION DU GRAPH------------------------------------------------------

            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
            dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)
            font = {'family' : 'Arial','size' : 7}

            dataQ1 = dataQ1.loc[dataQ1['LIBELLE FRANCAIS']== data[1], :]
            df_nbrMax = dataQ1.groupby(['ARRONDISSEMENT'], sort=True)['HAUTEUR (m)'].max().sort_values(ascending=False).tolist()[0]

            g = dataQ1.groupby('ARRONDISSEMENT')
            dataQ2 = g[['HAUTEUR (m)']].agg([pandas.Series.mean, pandas.Series.max, pandas.Series.min,pandas.Series.count])
            listarro=dataQ2.index.tolist()
            dataQ2.columns=['MEAN', 'MAX', 'MIN','COUNT']
            dataQ2.insert(0,"ARRONDISSEMENT",listarro)


            f, ax = plt.subplots(figsize=(12, 9))
            plt.rc('font', **font)

            sns.set_color_codes("pastel")
            sns.barplot(y="MAX", x="ARRONDISSEMENT", data=dataQ2, label='Maximum', color="b")

            sns.set_color_codes("muted")
            sns.barplot(y='MEAN', x='ARRONDISSEMENT', data=dataQ2, label="Average", color="g")

            sns.set_color_codes("bright")
            sns.barplot(y="MIN", x="ARRONDISSEMENT", data=dataQ2, label='Minimum', color="b")

            ax.legend(ncol=3, loc="upper right", frameon=True, fontsize='medium')
            ax.set(xlim=(-2,len(listarro)+1),ylim=(0, df_nbrMax*1.2), xlabel="Arrondissement", ylabel="hauteur")
            plt.xlabel('ARRONDISSEMENT', fontsize=12)                               # Titre de l'axe x et taille de police
            plt.ylabel('', fontsize=8)
            plt.rc('font', **font)
            plt.xticks(rotation=85)
            sns.despine(right=True, top=True)
            f.patch.set_facecolor(colorg)
            ax.set_facecolor('black')
            plt.gcf().set_size_inches(8, 8)
            f.subplots_adjust(bottom=0.40)
            plt.title(f'Hauteur mini, moyenne et maxi des "{data[1]}" par arrondissement', fontsize=11)
            titreGraph=""
            AfficheframeCanvas()



            #CREATION DU TEXTE -----------------------------------------------------

            new_df_Q2 = pandas.read_csv(path , sep = ',', header = 0)
            new_df_Q2.drop(new_df_Q2.index[new_df_Q2['HAUTEUR (m)']>50], inplace=True)
            new_df_Q2.drop(new_df_Q2.index[new_df_Q2['HAUTEUR (m)']<2], inplace=True)

            dg = new_df_Q2.query('`LIBELLE FRANCAIS` == @data[1]')
            df_arrdMax = dg.groupby(['ARRONDISSEMENT'], sort=True)['HAUTEUR (m)'].max().sort_values(ascending=False).keys().tolist()[0]
            df_arrdMin = dg.groupby(['ARRONDISSEMENT'], sort=True)['HAUTEUR (m)'].min().sort_values().keys().tolist()[0]
            df_nbrMax = dg.groupby(['ARRONDISSEMENT'], sort=True)['HAUTEUR (m)'].max().sort_values(ascending=False).tolist()[0]
            df_nbrMin = dg.groupby(['ARRONDISSEMENT'], sort=True)['HAUTEUR (m)'].min().sort_values().tolist()[0]

            answer = f'\nLe "{data[1]}" le plus haut fait {df_nbrMax} mètres et se trouve dans {df_arrdMax}\n\nLe "{data[1]}" le moins haut fait {df_nbrMin} mètres et se trouve dans {df_arrdMin}.\n'

            AfficheframeLabelText()


            #CREATION DE LA MAP ----------------------------------------------------

            new_df_data = pandas.read_csv(path , sep = ',', header = 0)
            new_df_data.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
            new_df_data.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)

            map_widget = TkinterMapView(frameTheMap, width=600, height=400, corner_radius=20)
            map_widget.pack(  pady = 10, padx = 10)

            map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

            # Zone affichée de la carte = PARIS
            #map_widget.set_position(48.860381, 2.338594)
            map_widget.set_position(48.860381, 2.338594)
            # Zoom
            map_widget.set_zoom(11)


            marqueurs = {}
            zone = []

            new_df_data= new_df_data.loc[new_df_data['LIBELLE FRANCAIS'] == data[1], :]
            a = new_df_data.loc[:,['ARRONDISSEMENT' ,'LIBELLE FRANCAIS', 'LATITUDE' ,'LONGITUDE' ]]
            if list(a) != 0 :
                liste_arr = []
                for i , row in a.iterrows():
                    coordonner = []
                    coordonner.append(row['LATITUDE']) ; coordonner.append(row['LONGITUDE'])
                    if (row['ARRONDISSEMENT'] in liste_arr) :
                        liste_arr.append("")
                    else:
                        if (row['ARRONDISSEMENT'] in appartenance)  :
                            liste_arr.append(row['ARRONDISSEMENT'])


                    marqueurs[str(data[1])+"_"+str(i)] = coordonner

                for i in liste_arr :
                    if i in appartenance :
                        zone.append(i)

            affiche_map(marqueurs, zone)



    #[1, TOUS, Hauteur]
    if data[0] != 'TOUS' and data[1] == 'TOUS' and data[2] == "Hauteur":

        test_df = pandas.read_csv(path, sep = ',', header = 0)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']>50], inplace=True)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']<2], inplace=True)
        test_df = test_df.loc[test_df['ARRONDISSEMENT']== data[0], :]
        if len(test_df) == 0:
            noData()
        else:

            #CREATION DU GRAPH------------------------------------------------------

            font = {'family' : 'Arial','size' : 7}
            dataQ = pandas.read_csv(path , sep = ',', header = 0)
            dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']>50], inplace=True)
            dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']<2], inplace=True)

            dataQ1 = dataQ.loc[dataQ['ARRONDISSEMENT']== data[0]]

            g = dataQ1.groupby('LIBELLE FRANCAIS')

            dataQ2 = g[['HAUTEUR (m)']].agg([pandas.Series.max,pandas.Series.min,pandas.Series.mean])
            dataQ2.columns=["max","min","moyenne"]
            dataQ2.insert(0,"Type",dataQ2.index.tolist())
            dataQ3=dataQ2.sort_values(by=["moyenne"],ascending=False)

            types=[]
            types.extend(typ.upper() for typ in dataQ3["Type"][:5])
            types.append("AUTRE")
            types.extend(typ.upper() for typ in dataQ3["Type"][-5:])

            maxi=[]
            maxi.extend(dataQ3["max"][:5])
            maxi.append(int(sum([int(elem) for elem in dataQ3["max"][5:-5]])/len([elem for elem in dataQ3["max"][5:-5]])))
            maxi.extend(dataQ3["max"][-5:])

            mini=[]
            mini.extend(dataQ3["min"][:5])
            mini.append(int(sum([int(elem) for elem in dataQ3["min"][5:-5]])/len([elem for elem in dataQ3["min"][5:-5]])))
            mini.extend(dataQ3["min"][-5:])

            moyenne=[]
            moyenne.extend([int(elem) for elem in dataQ3["moyenne"][:5]])
            moyenne.append(int(sum([int(elem) for elem in dataQ3["moyenne"][5:-5]])/len([elem for elem in dataQ3["moyenne"][5:-5]])))
            moyenne.extend([int(elem) for elem in dataQ3["moyenne"][-5:]])

            f, ax = plt.subplots(figsize=(16, 9))
            plt.rc('font', **font)
            sns.set_color_codes("pastel")
            sns.barplot(x=types, y=maxi,label='Maximum', color="b")

            sns.set_color_codes("bright")
            sns.barplot(x=types, y=moyenne, label='Moyenne', color="g")

            sns.set_color_codes("muted")
            sns.barplot(x=types, y=mini, label="Minimum", color="b")

            ax.legend(ncol=3, loc="upper right", frameon=True,fontsize='medium')
            ax.set(ylim=(0, max(maxi)*1.2),xlim=(-2, 12), ylabel="HAUTEUR", xlabel=f"ARBRE")
            plt.xlabel('ARBRE', fontsize=12)                               # Titre de l'axe x et taille de police
            plt.ylabel('HAUTEUR', fontsize=8)
            plt.xticks(rotation=85)
            sns.despine(right=True, top=True)
            f.patch.set_facecolor(colorg)
            ax.set_facecolor('black')
            plt.gcf().set_size_inches(8, 8)
            f.subplots_adjust(bottom=0.40)
            plt.title(f'Hauteur mini, moyenne et maxi des arbres dans \"{data[0]}\" ', fontsize=11)
            plt.rc('font', **font)
            titreGraph = ""
            AfficheframeCanvas()


            #CREATION DU TEXTE -----------------------------------------------------

            dg = pandas.read_csv(path , sep = ',', header = 0)
            dg.drop(dg.index[dg['HAUTEUR (m)']>50], inplace=True)
            dg.drop(dg.index[dg['HAUTEUR (m)']<2], inplace=True)
            moy_df = dg.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].mean().max()
            Arbre_df = dg[(dg['ARRONDISSEMENT']==data[0]) & (dg['LIBELLE FRANCAIS'])]
            taille_max = Arbre_df["HAUTEUR (m)"].sort_values(ascending = False).max()
            #arbremax = [el for el in dg.drop(dg.index[dg['HAUTEUR (m)'] == taille_max], inplace=True)["LIBELLE FRANCAIS"][0:0]]


            dg2 = pandas.read_csv(path , sep = ',', header = 0)
            dg2.drop(dg2.index[dg2['HAUTEUR (m)'] > 50], inplace=True)
            dg2.drop(dg2.index[dg2['HAUTEUR (m)'] < 2], inplace=True)
            dg2.drop(dg2.index[dg2['HAUTEUR (m)'] != taille_max], inplace=True)
            dg2 = dg2.loc[dg2['ARRONDISSEMENT']== data[0]]



            taille_min = Arbre_df["HAUTEUR (m)"].sort_values(ascending = False).min()

            answer = f"\nLes arbres de {data[0]} mesurent en moyenne {round(moy_df,2)}m.\n\nLe plus haut mesure {taille_max}m, le plus petit mesure {taille_min}m.\n"

            AfficheframeLabelText()

             #CREATION DE LA MAP ----------------------------------------------------
            # Tous les arbres de l'arrdt

            # create map widget
            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            map_widget = TkinterMapView(frameTheMap, width=600, height=400, corner_radius=20)
            map_widget.pack(  pady = 10, padx = 10)

            map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

            # Zone affichée de la carte = PARIS
            map_widget.set_position(localisation[data[0]][0], localisation[data[0]][1])

            # Zoom
            map_widget.set_zoom(13)


            #dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']>50], inplace=True)
            #dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']<2], inplace=True)
            dataQ1 = dataQ.loc[dataQ['ARRONDISSEMENT']== data[0], :]

            groupeArdt = dataQ1.groupby("ARRONDISSEMENT")

            marqueurs = {}

            latitude = []
            longitude = []
            arbre = []

            #Marqueurs sur tous les arbres select pour l'arrdt selectionné limité à 100
            for arrdt in groupeArdt:

                for i in range(0,min(100, len(arrdt[1]))):
                    marqueurs[f"{arrdt[0]} - {arrdt[1].iloc[i , 4]} - {i+1}"] = [arrdt[1].iloc[i , 8], arrdt[1].iloc[i , 9]]

            affiche_map(marqueurs)


    #One, one, hauteur
    if data[0] != 'TOUS' and data[1] != 'TOUS' and data[2] == "Hauteur" :

        test_df = pandas.read_csv(path, sep = ',', header = 0)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']>50], inplace=True)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']<2], inplace=True)
        test_df = test_df.loc[test_df['ARRONDISSEMENT']== data[0], :]
        test_df = test_df.loc[test_df['LIBELLE FRANCAIS']== data[1], :]
        if len(test_df) == 0:
            noData()
        else:

            #CREATION DU GRAPH------------------------------------------------------

            font = {'family' : 'Arial','size' : 7}
            sns.set(style="white")
            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            dataQ2 = pandas.read_csv(path , sep = ',', header = 0)
            dataQ3 = pandas.read_csv(path , sep = ',', header = 0)
            dataQ4 = pandas.read_csv(path , sep = ',', header = 0)

            df_nbrMax = dataQ1.groupby(['ARRONDISSEMENT'], sort=True)['HAUTEUR (m)'].max().sort_values(ascending=False).tolist()[0]

            #suppression de l arbre'hauteur superieur à 50 et inferieur à 2
            dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
            dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)
            dataQ2.drop(dataQ2.index[dataQ2['HAUTEUR (m)']>50], inplace=True)
            dataQ2.drop(dataQ2.index[dataQ2['HAUTEUR (m)']<2], inplace=True)
            dataQ3.drop(dataQ3.index[dataQ3['HAUTEUR (m)']>50], inplace=True)
            dataQ3.drop(dataQ3.index[dataQ3['HAUTEUR (m)']<2], inplace=True)
            dataQ4.drop(dataQ4.index[dataQ4['HAUTEUR (m)']>50], inplace=True)
            dataQ4.drop(dataQ4.index[dataQ4['HAUTEUR (m)']<2], inplace=True)

            df_nbrMax = dataQ4.groupby(['ARRONDISSEMENT'], sort=True)['HAUTEUR (m)'].max().sort_values(ascending=False).tolist()[0]
            ##################     one,one,hauteur      #########################
            dataQ1 = dataQ1.loc[ (dataQ1['ARRONDISSEMENT']== data[0] )&(dataQ1['LIBELLE FRANCAIS'] == data[1] ),  :]
            g = dataQ1.groupby('ARRONDISSEMENT')
            data_one_one = g[['HAUTEUR (m)']].agg([pandas.Series.mean, pandas.Series.max, pandas.Series.min])
            data_one_one.columns=['MEAN', 'MAX', 'MIN']

            data_one_one.insert(0,"TYPE",data[1].upper())
            #####################    one,tous,hauteur    ###############################
            dataQ1_one_tous = dataQ2.loc[(dataQ2['ARRONDISSEMENT']== data[0]) & (dataQ2["LIBELLE FRANCAIS"]!=data[1]), :]
            g = dataQ1_one_tous.groupby('ARRONDISSEMENT')
            data_one_tous = g[['HAUTEUR (m)']].agg([pandas.Series.mean, pandas.Series.max, pandas.Series.min])
            data_one_tous.columns=['MEAN', 'MAX', 'MIN']
            data_one_tous.insert(0,"TYPE","AUTRE ARBRES \nDANS L'ARRDT")


              #####################    tous,tous,hauteur   ###############################
            data_demo_tous_tous=dataQ3.loc[(dataQ3['ARRONDISSEMENT']!= data[0]) & (dataQ3["LIBELLE FRANCAIS"]==data[1]), :]
            g = data_demo_tous_tous.groupby('ARRONDISSEMENT')
            data_tous_tous = g[['HAUTEUR (m)']].agg([pandas.Series.mean, pandas.Series.max, pandas.Series.min])
            data_tous_tous.columns=['MEAN', 'MAX', 'MIN']
            data_tous_tous.sort_values(by=["MAX"],ascending=False)
            data_tous_tous.sort_values(by=["MIN"],ascending=False)
            data_tous_tous.insert(0,"TYPE",f"{data[1].upper()} \nDANS LES AUTRES ARRDT")
            temp_moyenne_valeur=[int(elem) for elem in data_tous_tous["MEAN"]]
            moyenne_autre_arrondissement=[int(int(sum(temp_moyenne_valeur))/len(temp_moyenne_valeur))]



                #####################    listes   ###############################
            element=[]

            element.append(data_one_one["TYPE"][0])
            element.append(data_one_tous["TYPE"][0])
            element.append(data_tous_tous["TYPE"][0])

            maximums=[]
            maximums.extend(data_one_one["MAX"])
            maximums.extend(data_one_tous["MAX"])
            maximums.append(data_tous_tous["MAX"][0])

            minimums=[]
            minimums.extend(data_one_one["MIN"])
            minimums.extend(data_one_tous["MIN"])
            minimums.append(data_tous_tous["MIN"][0])

            moyennes=[]
            moyennes.extend(int(elem) for elem in data_one_one["MEAN"])
            moyennes.extend(int(elem) for elem in data_one_tous["MEAN"])
            moyennes.extend(moyenne_autre_arrondissement)

                ####################### GRAPHE   #################################"


            f, ax = plt.subplots(figsize=(16, 9))
            plt.rc('font', **font)
            plt.title(f'Hauteur mini, moyenne et maxi des "{data[1]}" dans "{data[0]}"', fontsize=10)
            sns.set_color_codes("pastel")
            sns.barplot(x=element, y=maximums, label='Maximum', color="b")

            sns.set_color_codes("muted")
            sns.barplot(x=element, y=moyennes, label="Moyenne", color="g")

            sns.set_color_codes("bright")
            sns.barplot(x=element, y=minimums, label='Minimum', color="b")

            ax.legend(ncol=3, loc="upper right", frameon=True, fontsize='medium')
            ax.set(ylim=(-1,df_nbrMax*1.2),xlim=(-2, 5), ylabel="HAUTEUR", xlabel=f"")
            plt.xlabel('', fontsize=8)                               # Titre de l'axe x et taille de police
            plt.ylabel('HAUTEUR', fontsize=8)
            plt.rc('font', **font)
            plt.xticks(rotation=85, fontsize=8)
            sns.despine(right=True, top=True)
            f.patch.set_facecolor(colorg)
            ax.set_facecolor('black')
            plt.gcf().set_size_inches(8, 8)
            f.subplots_adjust(bottom=0.40)
            titraGraph = ""
            AfficheframeCanvas()



            #CREATION DE LA MAP ----------------------------------------------------
            # create map widget

            new_df_data = pandas.read_csv(path , sep = ',', header = 0)
            new_df_data.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
            new_df_data.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)

            map_widget = TkinterMapView(frameTheMap, width=600, height=400, corner_radius=20)
            map_widget.pack(  pady = 10, padx = 10, )

            map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

            # Zone affichée de la carte = l'arrdt select

            map_widget.set_position(localisation[data[0]][0], localisation[data[0]][1])
            # Zoom
            map_widget.set_zoom(13)
            marqueurs = {}
            zone = []


            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            #suppression de l arbre'hauteur superieur à 50 et inferieur à 2
            dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
            dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)

            dataQ1 = dataQ1.loc[ (dataQ1['ARRONDISSEMENT']== data[0] )&(dataQ1['LIBELLE FRANCAIS']== data[1] ), :]

            if list(dataQ1 ) != 0 :
                liste_arr = []
                for i , row in dataQ1.iterrows():
                    coordonner = []
                    coordonner.append(row['LATITUDE']) ; coordonner.append(row['LONGITUDE'])
                    #liste_hauteur.append(row['HAUTEUR (m)'])
                    marqueurs[str(row['HAUTEUR (m)'])+"(m)_"+str(i)] = coordonner
                zone.append(data[0])
                liste_arr.append(data[0])
            affiche_map(marqueurs, zone)

            #CREATION DE text ----------------------------------------------------

            new_df_Q2 = pandas.read_csv(path , sep = ',', header = 0)

            new_df_Q2.drop(new_df_Q2.index[new_df_Q2['HAUTEUR (m)']>50], inplace=True)
            new_df_Q2.drop(new_df_Q2.index[new_df_Q2['HAUTEUR (m)']<2], inplace=True)

            dg = new_df_Q2.query('`ARRONDISSEMENT` == @data[0] & `LIBELLE FRANCAIS` == @data[1]')
            moy_df = dg.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].mean().max()
            taille_max = dg["HAUTEUR (m)"].sort_values(ascending = False).max()
            taille_min = dg["HAUTEUR (m)"].sort_values(ascending = False).min()


            answer = f'\nLes arbres : " {data[1]} " de {data[0]} font en moyenne {round(moy_df, 2)}m.\n\n le plus haut fait {taille_max}m et le plus petit fait {taille_min}m.\n'
            AfficheframeLabelText()



    #[TOUS, TOUS, Type] = Q3
    if data[0] == 'TOUS' and data[2] == "Type":

        test_df = pandas.read_csv(path, sep = ',', header = 0)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']>50], inplace=True)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']<2], inplace=True)
        if len(test_df) == 0:
            noData()
        else:

            #CREATION DU GRAPH------------------------------------------------------

            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            df1=dataQ1["LIBELLE FRANCAIS"].value_counts().tolist()
            df2=dataQ1["LIBELLE FRANCAIS"].value_counts().keys().tolist()
            font = {'family' : 'Arial','size' : 8}

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

            f = Figure(figsize=(5, 4), dpi=100) # create a figure object
            ax = f.add_subplot(111) # add an Axes to the figure
            plt.subplots(figsize=(12, 9))
            plt.rc('font', **font)
            plt.gcf().set_size_inches(5, 5)
            plt.title(f"Type d'arbres tous les arrondissements confondus", fontsize=11, color = "black")
            ax.pie(sizes, radius=1, labels=labels,autopct='%0.2f%%', shadow=True, colors=colors, explode=explode)
            f.patch.set_facecolor(colorg)


            #plt.figure(figsize=(5,5))
            #plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90,normalize=True)
            #f, ax = plt.subplots(figsize=(12, 9))
            #plt.axis('equal')
            #plt.savefig('PieChart02.png')
            #plt.show()
            if data[1] != 'TOUS':
                titreGraph = "\nTous les arbres sont pris dans la requête\n\n Type d'arbres tous les arrondissements confondus"
            else:
                titreGraph = "\nType d'arbres tous les arrondissements confondus"
            AfficheframeCanvas()



            #CREATION DU TEXTE -----------------------------------------------------

            dataQ = pandas.read_csv(path , sep = ',', header = 0)
            dataQ.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False)
            df_arrdMax2 = dataQ.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False).keys()[0]
            df_nbrMax2 = dataQ.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False)[0]
            df_arrdMin2 = dataQ.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False).keys()[-1]
            df_nbrMin2 = dataQ.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False)[-1]
            if data[1] != 'TOUS':
                answer = f"\nTous les arbres sont pris dans la requête\n\nL'arbre le plus présent dans tous les arrondissements confondus est le {df_arrdMax2} apparaissant {separateurMilliers(df_nbrMax2)} fois\n\nL'arbre le moins présent dans tous les arrondissements confondus est le {df_arrdMin2} apparaissant { separateurMilliers(df_nbrMin2)} fois\n"
            else:
                answer = f"\nL'arbre le plus présent dans tous les arrondissements confondus est le {df_arrdMax2} apparaissant {separateurMilliers(df_nbrMax2)} fois\n\nL'arbre le moins présent dans tous les arrondissements confondus est le {df_arrdMin2} apparaissant { separateurMilliers(df_nbrMin2)} fois\n"


            AfficheframeLabelText()



            #CREATION DE LA MAP ----------------------------------------------------
            # 10 arbres aléatoires par arrdt

            # create map widget
            map_widget = TkinterMapView(frameTheMap, width=600, height=400, corner_radius=20)
            map_widget.pack(  pady = 10, padx = 10)

            map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

            # Zone affichée de la carte = PARIS
            map_widget.set_position(48.860381, 2.338594)

            # Zoom
            map_widget.set_zoom(11)

            dataQ = pandas.read_csv(path , sep = ',', header = 0)
            dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']>50], inplace=True)
            dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']<2], inplace=True)
            groupeArdt = dataQ.groupby("ARRONDISSEMENT")

            marqueurs = {}

            latitude = []
            longitude = []
            arbre = []

            # Création de marqueurs sur tous les arbres
            for arrdt in groupeArdt:
                for i in range(0,len(arrdt[1])):
                    marqueurs[f"{arrdt[1].iloc[i , 4]}"] = [arrdt[1].iloc[i , 8], arrdt[1].iloc[i , 9]]

            affiche_map(marqueurs)


    #[1, TOUS, Type]
    if data[0] != 'TOUS' and data[2] == "Type":

        test_df = pandas.read_csv(path, sep = ',', header = 0)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']>50], inplace=True)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']<2], inplace=True)
        test_df = test_df.loc[test_df['ARRONDISSEMENT']== data[0], :]
        if len(test_df) == 0:
            noData()
        else:


            #CREATION DU GRAPH------------------------------------------------------

            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            dataQ1 = dataQ1.loc[dataQ1['ARRONDISSEMENT']== data[0], :]
            df1=dataQ1["LIBELLE FRANCAIS"].value_counts().tolist()
            df2=dataQ1["LIBELLE FRANCAIS"].value_counts().keys().tolist()
            font = {'family' : 'Arial','size' : 8}

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
            for i in range(len(labels)-1):
                colors.append(listeColors[i])
                listeExplode.append(0)


            # Chaque cartile correspond à une valeur
            explode = listeExplode

            f = Figure(figsize=(5, 4), dpi=100) # create a figure object
            ax = f.add_subplot(111) # add an Axes to the figure
            plt.subplots(figsize=(12, 9))
            plt.rc('font', **font)
            plt.gcf().set_size_inches(5, 5)
            plt.title(f"Type d'arbres tout arrondissement confondu", fontsize=11, color = "black")
            ax.pie(sizes, radius=1, labels=labels,autopct='%0.2f%%', shadow=True, colors=colors, explode=explode)
            f.patch.set_facecolor(colorg)


            #plt.figure(figsize=(5,5))
            #plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90,normalize=True)
            #f, ax = plt.subplots(figsize=(12, 9))
            #plt.axis('equal')
            #plt.savefig('PieChart02.png')
            #plt.show()

            if data[1] != 'TOUS':
                titreGraph = f"\nTous les arbres sont pris dans la requête\n\nType d'arbres dans {data[0].upper()}"
            else:
                titreGraph = f"\nType d'arbres dans {data[0].upper()}"
            AfficheframeCanvas()

            #CREATION DU TEXTE -----------------------------------------------------

            new_df_Q2 = pandas.read_csv(path , sep = ',', header = 0)
            dg = new_df_Q2.query('`ARRONDISSEMENT` == @data[0]')
            df_arrdMax2 = dg.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False).keys()[0]
            df_nbrMax2 = dg.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False)[0]
            df_arrdMin2 = dg.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False).keys()[-1]
            df_nbrMin2 = dg.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False)[-1]
            dg.groupby(['LIBELLE FRANCAIS'])['ARRONDISSEMENT'].count().sort_values(ascending=False)


            if data[1] != 'TOUS':
                answer = f"\nTous les arbres sont pris dans la requête\n\nL'arbre le plus présent dans tous les arrondissements confondus est le {df_arrdMax2} apparaissant {separateurMilliers(df_nbrMax2)} fois\n\nL'arbre le moins présent dans tous les arrondissements confondus est le {df_arrdMin2} apparaissant { separateurMilliers(df_nbrMin2)} fois\n"
            else:
                answer = f"\nL'arbre le plus présent dans {data[0].upper()} est le {df_arrdMax2} apparaissant {separateurMilliers(df_nbrMax2)} fois\n\nL'arbre le moins présent dans {data[0].upper()} est le {df_arrdMin2} apparaissant { separateurMilliers(df_nbrMin2)} fois\n"


            AfficheframeLabelText()



            #CREATION DE LA MAP ----------------------------------------------------
            # 10 arbres aléatoires par arrdt

            # create map widget
            map_widget = TkinterMapView(frameTheMap, width=600, height=400, corner_radius=20)
            map_widget.pack(  pady = 10, padx = 10)

            map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

            # Zone affichée de la carte = PARIS
            map_widget.set_position(localisation[data[0]][0], localisation[data[0]][1])

            # Zoom
            map_widget.set_zoom(12)

            dataQ = pandas.read_csv(path , sep = ',', header = 0)
            dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']>50], inplace=True)
            dataQ.drop(dataQ.index[dataQ['HAUTEUR (m)']<2], inplace=True)
            dataQ = dataQ.query('`ARRONDISSEMENT` == @data[0]')
            groupeArdt = dataQ.groupby("ARRONDISSEMENT")

            marqueurs = {}

            latitude = []
            longitude = []
            arbre = []

            # Création de marqueurs sur tous les arbres
            for arrdt in groupeArdt:

                for i in range(0,len(arrdt[1])):
                    marqueurs[f"{arrdt[1].iloc[i , 4]}"] = [arrdt[1].iloc[i , 8], arrdt[1].iloc[i , 9]]

            affiche_map(marqueurs)


    #[TOUS, TOUS, MAP]
    if data[2] == "MAP":
        print('map : ', data)

        test_df = pandas.read_csv(path, sep = ',', header = 0)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']>50], inplace=True)
        test_df.drop(test_df.index[test_df['HAUTEUR (m)']<2], inplace=True)
        if data[0] != "TOUS":
            test_df = test_df.loc[test_df['ARRONDISSEMENT']== data[0], :]
        if data[1] != "TOUS":
            test_df = test_df.loc[test_df['LIBELLE FRANCAIS']== data[1], :]
        if len(test_df) == 0:
            noData()
        else:

            #CREATION DE LA MAP ----------------------------------------------------

            dataQ1 = pandas.read_csv(path , sep = ',', header = 0)
            #dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
            #dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)
            if data[0] != "TOUS":
                dataQ1 = dataQ1.loc[dataQ1['ARRONDISSEMENT']== data[0], :]
            if data[1] != "TOUS":
                dataQ1 = dataQ1.loc[dataQ1['LIBELLE FRANCAIS']== data[1], :]

            print(len(dataQ1))

            map_widget = TkinterMapView(frameTheMap, width=600, height=400, corner_radius=20)
            map_widget.pack(  pady = 10, padx = 10)

            map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)



            # Zone affichée de la carte = PARIS
            map_widget.set_position(48.860381, 2.338594)
            # Zoom
            map_widget.set_zoom(11)

            marqueurs = {}

            for i in range(0,len(dataQ1)):
                marqueurs[f"{dataQ1.iloc[i , 4]} - {i}"] = [dataQ1.iloc[i , 8], dataQ1.iloc[i , 9]]

            affiche_map(marqueurs)



# Fonctions pour la mise à jour du texte des bouton en fonction de la sélection
def updateBoutonArrdt():
    ## Affiche l'arrdt selectionné sur le bouton correspondant
    global ArrondissemenrSelect, boutonArrdt
    ArrondissemenrSelect = data[0].upper()
    boutonArrdt.destroy()
    boutonArrdt = Button(frameArrdt, text=ArrondissemenrSelect, bg=colorb, command=creationListeArrdt, width=17)
    boutonArrdt.pack(side=TOP)

def updateBoutonArbre():
    ## Affiche l'arbre selectionné sur le bouton correspondant
    global boutonArbre, ArbreSelect
    ArbreSelect = data[1].upper()
    boutonArbre.destroy()
    boutonArbre = Button(frameArbre, text=ArbreSelect, bg=colorb, command=creationListeArbre, width=17)
    boutonArbre.pack(side=TOP)

def updateBoutonCritere():
    ## Affiche le critère selectionné sur le bouton correspondant
    global CritereSelect, boutonCritere
    CritereSelect = data[2].upper()
    boutonCritere.destroy()
    boutonCritere = Button(frameCritere, text=CritereSelect, bg=colorb, command=creationListeCritere, width=17)
    boutonCritere.pack(side=TOP)


# Fonctions rattachées aux boutons Q1, Q2 et Q3
def demande1():
    ## Affiche la réponse pour la Q1
    global data
    data=["TOUS", "TOUS", "Quantité"]
    updateBoutonArrdt()
    updateBoutonArbre()
    updateBoutonCritere()
    #updateTexteSelection()
    apply()

def demande2():
    ## Affiche la réponse pour la Q2
    global data
    data=["TOUS", "TOUS", "Hauteur"]
    #updateTexteSelection()
    updateBoutonArrdt()
    updateBoutonArbre()
    updateBoutonCritere()
    apply()

def demande3():
    ## Affiche la réponse pour la Q3
    global data
    data=["TOUS", "TOUS", "Type"]
    #updateTexteSelection()
    updateBoutonArrdt()
    updateBoutonArbre()
    updateBoutonCritere()
    apply()


# Fonctions pour récupérer le choix de l'utilisateur et mettre à jour la demande
def selectArrdt(event):
    ## Mise à jour de l'arrondissement sélectionné dans la demande
    global listeArrdt, data
    arrdt = listeArrdt.selection_get()
    creationListeArrdt()
    data[0] = arrdt
    updateBoutonArrdt()
    #updateTexteSelection()
    print('data : ', data)

def selectArbre(event):
    ## Mise à jour du type d'arbre sélectionné dans la demande
    global listeArbre, data, boutonArbre, ArbreSelect
    arbre = listeArbre.selection_get()
    creationListeArbre()
    data[1] = arbre
    updateBoutonArbre()
    #updateTexteSelection()
    print('data : ', data)

def selectCritere(event):
    ## Mise à jour du critère sélectionné dans la demande
    global listeCritere, data, boutonCritere, CritereSelect
    critere = listeCritere.selection_get()
    creationListeCritere()
    data[2] = critere
    updateBoutonCritere()
    #updateTexteSelection()
    print('data : ', data)

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#                 TKINTER
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


# Fonctions pour créer les menus déroulant
def creationListeArrdt():
    ## Affiche les ardt dispo dans le menu déroulant à partir du csv
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
        listeArrdt.pack(side=BOTTOM)
        arrdtIsVisible = True

def creationListeArbre():
    ## Affiche les arbres dispo dans le menu déroulant à partir du csv
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
        listeArbre.pack(side=BOTTOM)
        arbreIsVisible = True

def creationListeCritere():
    ## Affiche les critères dispo
    global listeCritere, critereIsVisible
    if critereIsVisible == True:
        listeCritere.destroy()
        critereIsVisible = False
    else:
        listeCritere = Listbox(frameCritere)
        listeCritere.insert(1, "Quantité")
        listeCritere.insert(2, "Hauteur")
        listeCritere.insert(3, "Type")
        listeCritere.insert(4, "MAP")
        listeCritere.bind('<<ListboxSelect>>', selectCritere)
        listeCritere.pack(side=BOTTOM)
        critereIsVisible = True


def mapFenetre():
    ## Affiche une MAP dans une fenêtre séparée

    '''
    markers = ""
    for el in marqueurs:

        markers = f"{markers}&markers=color:green%7Clabel:{el}%7C{marqueurs[el][0]},{marqueurs[el][1]}"

    urls=f"https://maps.googleapis.com/maps/api/staticmap?center=Paris,France&size=800x800&style=feature:poi|visibility:off{markers}&key={apiKey}"

    webbrowser.open(urls)
    '''

    global mapFenetre, marqueurs, zone, bigMap
    try:
        mapFenetre.destroy()
    except:
        pass
    mapFenetre = Tk()
    mapFenetre.title('MAP')
    mapFenetre.geometry('1200x900')
    bigMap = TkinterMapView (mapFenetre, corner_radius=0)
    bigMap.pack(fill=BOTH, expand=True)
    bigMap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    #map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    bigMap.set_position(48.860381, 2.338594)
    bigMap.set_zoom(11.5)
     ## Affiche la carte avec les marqueurs et les zones
    #numero d'arrondissement spec
    arr= []
    if type(marqueurs) == dict:
        for i, j  in marqueurs.items():
            arr.append(i)
            bigMap.set_marker(j[0], j[1] , text= i, marker_color_circle="#3a5a40", marker_color_outside="#a3b18a")

    zone= [
        'PARIS 20E ARRDT',
        'PARIS 19E ARRDT',
        'PARIS 18E ARRDT',
        'PARIS 17E ARRDT',
        'PARIS 16E ARRDT',
        'PARIS 15E ARRDT',
        'PARIS 14E ARRDT',
        'PARIS 13E ARRDT',
        'PARIS 12E ARRDT',
        'PARIS 11E ARRDT',
        'PARIS 10E ARRDT',
        'PARIS 9E ARRDT',
        'PARIS 8E ARRDT',
        'PARIS 7E ARRDT',
        'PARIS 6E ARRDT',
        'PARIS 5E ARRDT',
        'PARIS 4E ARRDT',
        'PARIS 3E ARRDT',
        'PARIS 2E ARRDT',
        'PARIS 1ER ARRDT',
        'BOIS DE BOULOGNE',
        'BOIS DE VINCENNES',
    ]


    for el in zone :
        res = []
        polygo =[]

        if el in appartenance:
            a = arr_df.loc[(arr_df ["Numéro d’arrondissement"] == appartenance[el] ) & (arr_df["Geometry X Y"])]
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
                points= [coord[1],coord[0]]
                polygo.append(tuple(points))
                #on a bien un dictionnaire avec des valeur en listes
            bigMap.set_polygon(polygo)
    center(mapFenetre)


    def on_closing():
        mapFenetre.destroy()
        mapFenetre.quit()

    mapFenetre.protocol("WM_DELETE_WINDOW", on_closing)
    mapFenetre.mainloop()






# SEB
mainFenetre = Tk()
mainFenetre.title('JSON STAT ARBRES')
mainFenetre.geometry('1200x790')
img = ImageTk.PhotoImage(imgArbre)
resize_image = imgFeuille.resize((1200, 675))
img2 = ImageTk.PhotoImage(resize_image)

#-----------------------------------------------------------------------
#                 FRAME GAUCHE → HAUT
#-----------------------------------------------------------------------


frameHaut = Frame(mainFenetre, bg=colorg)
frameHaut.pack(side=TOP, expand=True, fill=BOTH)

frameBas = Frame(mainFenetre, bg=colorg)
frameBas.pack(side=BOTTOM, expand=True, fill=BOTH)



#---------- DEMANDE TOP LEFT----------

frameDemande = Frame(frameHaut, bg=color, height = 300, width=600)
frameDemande.pack( fill=BOTH, expand=True)
frameDemande.pack(side=LEFT,  fill=BOTH, expand=True)
frameDemande.pack_propagate(False)

canvas1 = Canvas( frameDemande, )
canvas1.pack(fill = "both", expand = True)
canvas1.create_image( 0, 0, image = img2, anchor = "nw")

canvas1.grid_rowconfigure(0, weight=10)
canvas1.grid_rowconfigure(1, weight=1)
canvas1.grid_rowconfigure(2, weight=1)

canvas1.grid_columnconfigure(0, weight=1)
canvas1.grid_columnconfigure(1, weight=1)
canvas1.grid_columnconfigure(2, weight=1)
canvas1.grid_columnconfigure(3, weight=1)
canvas1.grid_columnconfigure(4, weight=1)
canvas1.grid_columnconfigure(5, weight=1)
canvas1.grid_columnconfigure(6, weight=1)
canvas1.grid_columnconfigure(7, weight=1)
canvas1.grid_columnconfigure(8, weight=1)
canvas1.grid_columnconfigure(9, weight=1)
canvas1.grid_columnconfigure(10, weight=1)

frameMenu = Frame(frameDemande, bg=color,)
frameMenu.pack(side=TOP)


# Arrdt

frameArrdt = Frame(canvas1, bg=color, width=500, height=200)
frameArrdt.grid(row=0, column=1, sticky=N, columnspan=3, pady=5)

boutonArrdt = Button(frameArrdt, text="Arrondissement", bg=colorb, command=creationListeArrdt, width=17)
boutonArrdt.pack(side=TOP)

listeArrdt = Listbox(frameArrdt, width=20,)
listeArrdt.pack()
listeArrdt.destroy()


#Arbre

frameArbre = Frame(canvas1, bg=color, width=500, height=200)
frameArbre.grid(row=0, column=4, sticky=N, columnspan=3, pady=5)

boutonArbre = Button(frameArbre, text="Arbre", bg=colorb, command=creationListeArbre, width=17)
boutonArbre.pack(side=TOP)



#Critère

frameCritere = Frame(canvas1, bg=color, width=500, height=200)
frameCritere.grid(row=0, column=7, sticky=N, columnspan=3, pady=5)

boutonCritere = Button(frameCritere, text="Critere", bg=colorb, command=creationListeCritere, width=17)
boutonCritere.pack(side=TOP)


# Selection actuelle
def updateTexteSelection():
    global labelSelection
    try:
        labelSelection.destroy()
    except:
        pass
    if data[0] == "TOUS" and data[1] == "TOUS":
        selection = f'Sélection actuelle : {data[2].upper()} pour TOUS les arbres dans TOUS les arrondissements.'
    if data[0] != "TOUS" and data[1] == "TOUS":
        selection = f'Sélection actuelle : {data[2].upper()} pour TOUS les arbres dans "{data[0].upper()}".'
    if data[0] == "TOUS" and data[1] != "TOUS":
        selection = f'Sélection actuelle : {data[2].upper()} pour les arbres "{data[1].upper()}" dans TOUS les arrondissements.'
    if data[0] != "TOUS" and data[1] != "TOUS":
        selection = f'Sélection actuelle : {data[2].upper()} pour les arbres "{data[1].upper()}" dans "{data[0].upper()}".'
    labelSelection = Label(canvas1, text=selection)
    labelSelection.grid(row=1, column=1, pady=0, columnspan=10)

#updateTexteSelection()

# Boutons
boutonApply = Button(canvas1, text="APPLY", command=apply, bg=colorb)
boutonApply.grid(row=2, column=8, sticky=S, pady=5)

boutonQ1 = Button(canvas1, text="Q1", command = demande1, bg=colorb)
boutonQ1.grid(row=2, column=2, sticky=S, pady=5)

boutonQ2 = Button(canvas1, text="Q2", command = demande2, bg=colorb)
boutonQ2.grid(row=2, column=4, sticky=S, pady=5)

boutonQ3 = Button(canvas1, text="Q3", command = demande3, bg=colorb)
boutonQ3.grid(row=2, column=6, sticky=S, pady=5)




#---------- REPONSE TEXTE TOP RIGHT----------

frameReponseTexte = Frame(frameHaut, bg=color, width = 600)
frameReponseTexte.pack_propagate(False)
frameReponseTexte.pack(side=RIGHT, fill=BOTH, expand=True)
frameImage = Label(frameReponseTexte, image = img)
frameImage.pack()



#----------  GRAPHE BOTTOM LEFT----------

frameGraph = Frame(frameBas, bg=colorg, height=500, width=600)
frameGraph.pack(fill=BOTH, expand=True)
frameGraph.pack(side=LEFT, fill=BOTH, expand=True)
frameGraph.pack_propagate(False)

frameTitreGraph = Frame(frameGraph, bg=colorg,)
frameTitreGraph.pack(side=BOTTOM)

titreGraph = Label(frameTitreGraph, text="GRAPH", bg=colorb, fg = colort, height=2, width=30)
titreGraph.pack(side=BOTTOM, pady = 5)


frameGraph = Frame(frameGraph, bg=colorg, height = 500, pady = 5)
frameGraph.pack( side=TOP, fill=BOTH, expand=True)




#---------- MAP BOTTOM RIGHT  ----------

frameMap = Frame(frameBas, bg=colorm, height=500, width=600)
frameMap.pack(fill=BOTH, expand=True)
frameMap.pack(side=RIGHT, fill=BOTH, expand=True)
frameMap.pack_propagate(False)

frameTitreMap = Frame(frameMap, bg=colorm,)
frameTitreMap.pack(side=BOTTOM)

titreMap = Button(frameTitreMap, text="MAP", bg=colorb, fg = colort, height=2, width=30, command=mapFenetre)
titreMap.pack(side=LEFT, padx=10, pady = 5)

frameTheMap = Frame(frameMap, bg=colorm, height = 500, pady = 15)
frameTheMap.pack(side=TOP,fill=BOTH, expand=True)








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