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
    'PARIS 20E ARRDT': [48.86346057889563,2.401188129284682],
    'PARIS 19E ARRDT':[48.8870756373184,2.384820702561691],
    'PARIS 18E ARRDT': [48.89256926800585,2.348160519562039],
    'PARIS 17E ARRDT': [48.8873265220258,2.306776990574407],
    'PARIS 16E ARRDT': [48.860393639111635,2.2619670441649964] ,
    'PARIS 15E ARRDT': [48.84008537593816,2.292825822424994],
    'PARIS 14E ARRDT': [48.82924450048979,2.326542044198942],
    'PARIS 13E ARRDT': [48.82838803174467,2.362272440420904] ,
    'PARIS 12E ARRDT': [48.83497438148046,2.421324900784684] ,
    'PARIS 11E ARRDT': [48.85905922134244,2.380058308197899] ,
    'PARIS 10E ARRDT':[48.87613003653916,2.360728487847451] ,
    'PARIS 9E ARRDT':[48.87716351732887,2.3374575434825444] ,
    'PARIS 8E ARRDT':[48.8727208374345,2.3125540224020678] ,
    'PARIS 7E ARRDT': [48.85617442877941,2.312187691482013],
    'PARIS 6E ARRDT':[48.8491303585852,2.3328979990533134] ,
    'PARIS 5E ARRDT': [48.84444315053269,2.3507146095752596],
    'PARIS 4E ARRDT': [48.854341426272875,2.3576296203249973],
    'PARIS 3E ARRDT': [48.86287238001697,2.3600009858976905],
    'PARIS 2E ARRDT': [48.86827922252251,2.342802546891362],
    'PARIS 1ER ARRDT':[48.86256270183603,2.3364433620533873],
    'CENTRE DE PARIS' : [48.866667,2.3333333],
    'HAUTS-DE-SEINE':[48.828508,2.2188068],
    'BOIS DE BOULOGNE': [48.86842, 2.23473],
    'BOIS DE VINCENNES': [48.8329, 2.4341],
    'SEINE-SAINT-DENIS': [48.9137455, 2.4845729],
    'VAL-DE-MARNE': [48.7931426, 2.4740337],


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

color = "White"


# les variables xxxIsVisible servent à afficher ou effacer les listes box (dans la partie demande) au clic sur le bouton correspondant
arrdtIsVisible = False
arbreIsVisible = False
critereIsVisible = False

# Création d'une variable data correspondant au choix de l'utilisateur. Format : ["Arrpndissement", "Arbre", "Critère"]
data=["TOUS", "TOUS", "Quantité"]
liste_arr = []


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#                 DATA
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


#Lecture du fichier CSV
new_df = pandas.read_csv(r"C:\Dev\Projet ARBRE DE PARIS\new_arbres.csv", sep = ',', header = 0)
arr_df = pandas.read_csv(r"C:\Dev\Projet ARBRE DE PARIS\Projet\JSON-STAT-ARBRE\arrondissements.csv", sep = ';', header = 0)

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
    ## Affiche la carte avec les marqueurs et les zones
    #numero d'arrondissement spec
    arr= []
    if type(marqueurs) == dict:
        
            for i, j  in marqueurs.items(): 

                arr.append(i)
                #enlever apres "_"
                tag_marqueur = ""
                for k in i : 
                    if k != "_" : 
                        tag_marqueur = str(tag_marqueur)+str(k)
                    else : 
                        break 

                map_widget.set_marker(j[0], j[1] , text= tag_marqueur  , marker_color_circle="#3a5a40", marker_color_outside="#a3b18a")
        

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
            map_widget.set_polygon(polygo, fill_color = 'red')
    print("liste_arrondissement", liste_arr)    
    #arrondissement marqueur
    for el in liste_arr : 
        if el in localisation : 
            print(localisation[el][0])
            map_widget.set_marker(localisation[el][0], localisation[el][1] , text= el)


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
    print("text à afficher ", answer)
    frameLabelText = Label(frameReponseTexte, text=answer, bg=color)
    frameLabelText.pack(side = LEFT)





def apply():
    ## Affiche les réponses, graphes et map relatifs à la demande

    # A chaque demande del'utilisateur : Destruction des Graphe, Map et Label précédents
    global frameCanvas, f, map_widget, frameLabelText, answer, new_df , data , liste_arr
    try:
        print(1)
        frameLabelText.destroy()
        frameCanvas.destroy()
        map_widget.destroy()

    except:
        pass

    #@laf 
    #TOUS , ONE , Hauteur
    if data[0] == 'TOUS' and data[1] != 'TOUS' and data[2] == "Hauteur" : 
        #CREATION DU GRAPH------------------------------------------------------    
        font = {'family' : 'normal','size'   : 5}
        sns.set(style="white")
        #@laf2
        dataQ1 = new_df
        #suppression de l arbre'hauteur superieur à 50 et inferieur à 2
        dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
        dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)

        dataQ1 = dataQ1.loc[dataQ1['LIBELLE FRANCAIS']== data[1], :]
        
        g = dataQ1.groupby('ARRONDISSEMENT')
        dataQ2 = g[['HAUTEUR (m)']].agg([pandas.Series.mean, pandas.Series.max, pandas.Series.min,pandas.Series.count])
        list_arro=dataQ2.index.tolist()
        dataQ2.columns=['MEAN', 'MAX', 'MIN','COUNT']
        dataQ2.insert(0,"ARRONDISSEMENT",list_arro)
        #print(dataQ2)
        
        f, ax = plt.subplots(figsize=(5,5))
        sns.set_color_codes("pastel")
        sns.barplot(x="MAX", y="ARRONDISSEMENT", data=dataQ2 , label='Maximum', color="b")


        sns.set_color_codes("muted")
        sns.barplot(x='MEAN', y='ARRONDISSEMENT', data=dataQ2, label="Average", color="g")

        sns.set_color_codes("bright")
        sns.barplot(x="MIN", y="ARRONDISSEMENT", data=dataQ2,
                        label='minimum', color="b")

        ax.legend(ncol=3, loc="upper right", frameon=True)
        ax.set(ylim=(-2,26),xlim=(-1, 60), ylabel="Arrondissement",
                xlabel="hauteur")
        sns.despine(right=True, top=True)

        AfficheframeCanvas()        
        
        #CREATION DE LA MAP ----------------------------------------------------
        # create map widget
        
        new_df_data = new_df
        new_df_data.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
        new_df_data.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)

        map_widget = TkinterMapView(frameTheMap, width=400, height=400, corner_radius=0)
        map_widget.pack(  pady = 10, padx = 10, side=RIGHT)

        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Zone affichée de la carte = PARIS
        #map_widget.set_position(48.860381, 2.338594)
        map_widget.set_position(localisation[data[0]])
        # Zoom
        map_widget.set_zoom(19)

        
        marqueurs = {}
        zone = []         
        
        new_df_data= new_df_data.loc[new_df_data['LIBELLE FRANCAIS'] == data[1], :]
        a = new_df_data.loc[:,['ARRONDISSEMENT' ,'LIBELLE FRANCAIS', 'LATITUDE' ,'LONGITUDE' ]]
        #print(a)
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
            print("nom_arr", liste_arr )
            for i in liste_arr :    
                if i in appartenance : 
                    zone.append(appartenance[i])    
        print("zone contour::::",zone)
        affiche_map(marqueurs, zone) 
        #CREATION DE text ----------------------------------------------------

        new_df = pandas.read_csv("new_arbres.csv", sep = ',', header = 0)
        new_df_Q2 = new_df
        new_df_Q2.drop(new_df_Q2.index[new_df_Q2['HAUTEUR (m)']>50], inplace=True)
        new_df_Q2.drop(new_df_Q2.index[new_df_Q2['HAUTEUR (m)']<2], inplace=True)

        dg = new_df_Q2.query('`LIBELLE FRANCAIS` == @data[1]')
        df_arrdMax = dg.groupby(['ARRONDISSEMENT'], sort=True)['HAUTEUR (m)'].max().sort_values(ascending=False).keys().tolist()[0]
        df_arrdMin = dg.groupby(['ARRONDISSEMENT'], sort=True)['HAUTEUR (m)'].min().sort_values().keys().tolist()[0]
        df_nbrMax = dg.groupby(['ARRONDISSEMENT'], sort=True)['HAUTEUR (m)'].max().sort_values(ascending=False).tolist()[0]
        df_nbrMin = dg.groupby(['ARRONDISSEMENT'], sort=True)['HAUTEUR (m)'].min().sort_values().tolist()[0]

        answer = f"L'arbre {data[1]} le plus haut fait {df_nbrMax} mètres et se trouve dans {df_arrdMax}\nLe {data[1]} le moins haut fait {df_nbrMin} mètres et se trouve dans {df_arrdMin}."
        AfficheframeLabelText()

    #One, one, hauteur
    if data[0] != 'TOUS' and data[1] != 'TOUS' and data[2] == "Hauteur" : 
        #CREATION DU GRAPH------------------------------------------------------
        print("one one")
        font = {'family' : 'normal','size'   : 5}
        sns.set(style="white")
        dataQ1 = new_df ; dataQ2 = new_df; dataQ3 = new_df
        #suppression de l arbre'hauteur superieur à 50 et inferieur à 2
        dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
        dataQ1.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)
        ##################     one,one,hauteur      #########################
        dataQ1 = dataQ1.loc[ (dataQ1['ARRONDISSEMENT']== data[0] )&(dataQ1['LIBELLE FRANCAIS'] == data[1] ),  :]
        g = dataQ1.groupby('ARRONDISSEMENT')
        data_one_one = g[['HAUTEUR (m)']].agg([pandas.Series.mean, pandas.Series.max, pandas.Series.min])
        data_one_one.columns=['MEAN', 'MAX', 'MIN']

        data_one_one.insert(0,"TYPE",data[1])
        #####################    one,tous,hauteur    ###############################
        dataQ1_one_tous = dataQ2.loc[(dataQ2['ARRONDISSEMENT']== data[0]) & (dataQ2["LIBELLE FRANCAIS"]!=data[1]), :]
        g = dataQ1_one_tous.groupby('ARRONDISSEMENT')
        data_one_tous = g[['HAUTEUR (m)']].agg([pandas.Series.mean, pandas.Series.max, pandas.Series.min])
        data_one_tous.columns=['MEAN', 'MAX', 'MIN']
        data_one_tous.insert(0,"TYPE","AUTRE")
        #print("tous tous hauteur", data_one_tous)

          #####################    tous,tous,hauteur   ###############################
        data_demo_tous_tous=dataQ3.loc[(dataQ3['ARRONDISSEMENT']!= data[0]) & (dataQ3["LIBELLE FRANCAIS"]==data[1]), :]
        g = data_demo_tous_tous.groupby('ARRONDISSEMENT')
        data_tous_tous = g[['HAUTEUR (m)']].agg([pandas.Series.mean, pandas.Series.max, pandas.Series.min])
        data_tous_tous.columns=['MEAN', 'MAX', 'MIN']
        data_tous_tous.sort_values(by=["MAX"],ascending=False)
        data_tous_tous.sort_values(by=["MIN"],ascending=False)
        data_tous_tous.insert(0,"TYPE",f"{data[1]} dans les autres arrondissements")
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
        f, ax = plt.subplots(figsize=(5,5))
        font = {'family' : 'Arial','size' : 12}
        plt.rc('font', **font)
        plt.title(f'la compariason entre les moyennes ,les maximums et les minimums hauteurs de \"{data[1]}\" avec tous les types presents \n dans \"{data[0]}\" et tous les types dans les autres arrondissements \n\n', fontsize=8)

        sns.set_color_codes("pastel")
        sns.barplot(x=element, y=maximums,
                    label='Maximum', color="g")

        sns.set_color_codes("muted")
        sns.barplot(x=element, y=moyennes,
                    label="Moyenne", color="y")

        sns.set_color_codes("bright")
        sns.barplot(x=element, y=minimums,
                    label='Minimum', color="r")

        ax.legend(ncol=3, loc="upper right", frameon=True)
        ax.set(ylim=(0,50),xlim=(-0.5, 3), ylabel="Hauteur",
            xlabel=f"\n\n\n - premiere barre : les éléments chosis \n deuxième barre : tous les types presents dans l'arrondissement choisi \n troisième barre : le type choisi dans les autres arrondissements ")
        # plt.xticks(rotation=20)
        sns.despine(right=True, top=True)

        AfficheframeCanvas()
        #CREATION DE LA MAP ----------------------------------------------------
        # create map widget
        
        new_df_data = new_df
        new_df_data.drop(dataQ1.index[dataQ1['HAUTEUR (m)']>50], inplace=True)
        new_df_data.drop(dataQ1.index[dataQ1['HAUTEUR (m)']<2], inplace=True)

        map_widget = TkinterMapView(frameTheMap, width=400, height=400, corner_radius=0)
        map_widget.pack(  pady = 10, padx = 10, side=RIGHT)

        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Zone affichée de la carte = PARIS

        map_widget.set_position(48.860381, 2.338594)
        # Zoom
        map_widget.set_zoom(11)
        marqueurs = {}
        zone = []         
        
        new_df = pandas.read_csv("new_arbres.csv") 
        dataQ1 = new_df
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
            zone.append(appartenance[data[0]])
            liste_arr.append(data[0])
        affiche_map(marqueurs, zone)

        #CREATION DE text ----------------------------------------------------

        new_df = pandas.read_csv("new_arbres.csv", sep = ',', header = 0)
        new_df_Q2 = new_df
        
        dg = new_df_Q2.query('`ARRONDISSEMENT` == @data[0] & `LIBELLE FRANCAIS` == @data[1]')
        moy_df = dg.groupby(['ARRONDISSEMENT'])['HAUTEUR (m)'].mean().max()
        taille_max = dg["HAUTEUR (m)"].sort_values(ascending = False).max()
        taille_min = dg["HAUTEUR (m)"].sort_values(ascending = False).min()

        
        answer = f'Les arbres : " {data[1]} " de {data[0]} font en moyenne {moy_df}m. \n le plus haut fait {taille_max}m et le plus petit fait {taille_min}m.'
        AfficheframeLabelText()


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
mainFenetre.geometry('1200x600')


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
frameBouton.pack(side=BOTTOM, fill=X, pady=5, padx=5)

boutonApply = Button(frameBouton, text="APPLY", command=apply)
boutonApply.pack(side=RIGHT)



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